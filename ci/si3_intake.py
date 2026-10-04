#!/usr/bin/env python3
# QTLV SI3-LOOP intake sidecar v1.0 — 对接/轮询/候取机道
# 事件驱动(由 qtlv-intake-watch.yml 或 SI1 拍首手跑)；公仓匿名读 + 私仓 FINE PAT 读面；零私域 Actions 额度
# 产物: receipts/intake/INTAKE-<ts>.md + receipts/si3_intake_watermark.json 差分水位
import json, os, re, sys, time, urllib.request, urllib.parse

FINE = os.environ.get("FINE_PAT") or ""
QI2 = os.environ.get("QI_READ") or ""  # 请求级降级链 (T62)
UA = {"User-Agent": "qtlv-si3-intake"}
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

WATCH = [
    # (repo, path, auth?)  auth=False=匿名公仓读
    ("chepin-ai/vci-inbox", "lanes/qtlv/inbox", False),
    ("chepin-ai/vci-inbox", "公告板", False),
    # pulses 目录不存在(404)已退役; spool 404=drain 信号保留语义但降噪: 仅在有件时报
    ("chepin-ai/vci-inbox", "spool-public/results", False),
    ("chepin-ai/ci-inbox", "shared", True),
    ("chepin-ai/ci-inbox", "讨论室/threads", True),
    ("chepin-ai/ci-inbox", "公告板", True),
]
PRIO = re.compile(r"(DEMAND|TASK|KEY-INSTALL|RECEIPT|VOTE|RULING|VERDICT|CAST|FIELD|REQ-|CONSULT|ASK|ESCAL|ROOT)", re.I)

def gh(repo, path, auth):
    # 钥亡不停车·请求级降级: FINE 先试, 403/401 即换 QI_READ 复测 (T62 RCA 卡一)
    url = "https://api.github.com/repos/%s/contents/%s" % (repo, urllib.parse.quote(path))
    creds = []
    if auth:
        if FINE: creds.append(FINE)
        if QI2 and QI2 != FINE: creds.append(QI2)
    else:
        creds.append("")
    last = "?"
    for tok in creds:
        h = dict(UA)
        if tok: h["Authorization"] = "token " + tok
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as f:
                j = json.load(f)
            return {x["name"]: x.get("sha", "")[:10] for x in j if x["type"] == "file"}
        except Exception as e:
            last = str(e)[:80]
            if "403" in last or "401" in last: continue
            break
    return {"__ERR__": last}

import time
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

def main():
    root = os.environ.get("SI3_ROOT", ".")
    wm_path = os.path.join(root, "receipts/si3_intake_watermark.json")
    prio_path = os.path.join(root, "receipts/prio_open.json")
    os.makedirs(os.path.join(root, "receipts/intake"), exist_ok=True)
    wm = {}
    if os.path.exists(wm_path):
        wm = json.load(open(wm_path))
    prio_open = {}
    if os.path.exists(prio_path):
        prio_open = json.load(open(prio_path))
    new_wm, report, prio = {}, [], []
    for repo, path, auth in WATCH:
        key = repo + "/" + path
        cur = gh(repo, path, auth)
        new_wm[key] = cur
        if "__ERR__" in cur:
            new_wm[key] = wm.get(key, cur)  # 读失败保旧水位, 防回退
            report.append("- `%s`: READ-ERR %s" % (key, cur["__ERR__"]))
            continue
        old = wm.get(key, {})
        new_files = sorted(n for n in cur if n not in old)
        chg_files = sorted(n for n in cur if n in old and cur[n] != old[n])
        if new_files or chg_files:
            report.append("- `%s`: +%d new, ~%d changed" % (key, len(new_files), len(chg_files)))
            for n in new_files + chg_files:
                mark = "NEW" if n in new_files else "CHG"
                tag = " **PRIO**" if PRIO.search(n) else ""
                report.append("    - [%s] %s%s" % (mark, n, tag))
                if PRIO.search(n):
                    prio.append({"where": key, "file": n, "mark": mark})
                    pid = key + "::" + n
                    ent = prio_open.get(pid, {"first_seen": TS, "hits": 0})
                    ent["last_seen"] = TS; ent["hits"] = ent.get("hits", 0) + 1
                    ent["file"] = n; ent["where"] = key  # T65-RCA: 台账条目须自带坐标, 否则渲染KeyError
                    prio_open[pid] = ent
        else:
            report.append("- `%s`: 无差分" % key)
    # PRIO 滚动台账: ANS 闭环检测 (同道 ANS-<stem> 出现) + 陈情滚动
    lane_cur = dict(new_wm.get("chepin-ai/vci-inbox/lanes/qtlv/inbox", {}))
    # D12(T65): 跨库ANS闭环检测——ci-inbox lanes/qtlv/inbox 亦为本线应答落点(73件在册)
    try:
        lane_cur.update(gh("chepin-ai/ci-inbox", "lanes/qtlv/inbox", True))
    except Exception:
        pass  # 辅面读败不阻主闭环
    closed = []
    for pid in list(prio_open):
        stem = pid.split("::", 1)[1]
        base = stem.rsplit(".", 1)[0]
        # T67: 检测面=vci/ci我线inbox ∪ vci公告板(本线板面应答); 自匹配守卫 x!=stem
        scan = dict(lane_cur); scan.update(new_wm.get("chepin-ai/vci-inbox/公告板", {}))
        if any(x != stem and any(x.startswith(px + base[:40]) or (px in x and base[:30] in x) for px in ("ANS-", "ECHO-", "REPLY-")) for x in scan):
            closed.append(pid); del prio_open[pid]
        elif prio_open[pid].get("hits", 0) > 20:
            del prio_open[pid]  # 陈情20拍后归档, 防胀
    open_lines = ["    - [OPEN-PRIO] %s ← %s (首见 %s, 旗标×%d)" % (
        p.get("file", pid.split("::",1)[-1]), p.get("where", "?"), p.get("first_seen", "?")[:15], p.get("hits", 1))
        for p in sorted(prio_open.values(), key=lambda e: e.get("first_seen", ""))[:15]]
    body = (["CLASSIFY: L0(qtlv SI3-LOOP intake 机层摘要·席判位空挂SI1)", "",
            "## 未闭环 PRIO 滚动台账 (拍首必读律·机层提醒)"] + (open_lines or ["    - 无"]) + ["",
            "# INTAKE-%s ｜ qtlv si3_intake v1.0" % TS, "",
            "## 差分（水位自上拍）"] + report + ["", "## 优先件（应答矩阵分流位）"])
    if prio:
        body += ["- `%s` ← %s [%s]" % (p["file"], p["where"], p["mark"]) for p in prio]
    else:
        body.append("- 无")
    body += ["", "—— qtlv SI3-LOOP 机层（纯事件驱动·零私域额度） #noauto"]
    out = os.path.join(root, "receipts/intake/INTAKE-%s.md" % TS)
    open(out, "w").write("\n".join(body))
    # union-merge 写水位: 迟到run不得以旧视图回退新水位 (T64 RCA-D10 修)
    try:
        disk = json.load(open(wm_path))
        for k, v in disk.items():
            if k in new_wm and isinstance(v, dict) and isinstance(new_wm[k], dict):
                merged = dict(v); merged.update(new_wm[k])  # 现测sha优先, 旧条目并集保留
                new_wm[k] = merged
            elif k not in new_wm:
                new_wm[k] = v
    except Exception:
        pass
    json.dump(new_wm, open(wm_path, "w"), ensure_ascii=False, indent=1)
    json.dump(prio_open, open(prio_path, "w"), ensure_ascii=False, indent=1)
    print("INTAKE_OK", out, "prio=", len(prio))

if __name__ == "__main__":
    main()
