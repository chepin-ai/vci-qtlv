#!/usr/bin/env python3
# QTLV SI3-LOOP intake sidecar v1.0 — 对接/轮询/候取机道
# 事件驱动(由 qtlv-intake-watch.yml 或 SI1 拍首手跑)；公仓匿名读 + 私仓 FINE PAT 读面；零私域 Actions 额度
# 产物: receipts/intake/INTAKE-<ts>.md + receipts/si3_intake_watermark.json 差分水位
import json, os, re, sys, time, urllib.request, urllib.parse

FINE = os.environ.get("FINE_PAT", "")  # secrets.FINE_OWN_PAT_QTL (读面, 不耗 Actions 额度)
UA = {"User-Agent": "qtlv-si3-intake"}
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

WATCH = [
    # (repo, path, auth?)  auth=False=匿名公仓读
    ("chepin-ai/vci-inbox", "lanes/qtlv/inbox", False),
    ("chepin-ai/vci-inbox", "公告板", False),
    ("chepin-ai/vci-inbox", "pulses", False),
    ("chepin-ai/vci-inbox", "spool-public/results", False),
    ("chepin-ai/ci-inbox", "shared", True),
    ("chepin-ai/ci-inbox", "讨论室/threads", True),
    ("chepin-ai/ci-inbox", "公告板", True),
]
PRIO = re.compile(r"(DEMAND|TASK|KEY-INSTALL|RECEIPT|VOTE|RULING|VERDICT|CAST|FIELD|REQ-|CONSULT|ASK|ESCAL|ROOT)", re.I)

def gh(repo, path, auth):
    url = "https://api.github.com/repos/%s/contents/%s" % (repo, urllib.parse.quote(path))
    h = dict(UA)
    if auth and FINE:
        h["Authorization"] = "token " + FINE
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as f:
            j = json.load(f)
        return {x["name"]: x.get("sha", "")[:10] for x in j if x["type"] == "file"}
    except Exception as e:
        return {"__ERR__": str(e)[:80]}

def main():
    root = os.environ.get("SI3_ROOT", ".")
    wm_path = os.path.join(root, "receipts/si3_intake_watermark.json")
    os.makedirs(os.path.join(root, "receipts/intake"), exist_ok=True)
    wm = {}
    if os.path.exists(wm_path):
        wm = json.load(open(wm_path))
    new_wm, report, prio = {}, [], []
    for repo, path, auth in WATCH:
        key = repo + "/" + path
        cur = gh(repo, path, auth)
        new_wm[key] = cur
        if "__ERR__" in cur:
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
        else:
            report.append("- `%s`: 无差分" % key)
    body = ["CLASSIFY: L0(qtlv SI3-LOOP intake 机层摘要·席判位空挂SI1)", "",
            "# INTAKE-%s ｜ qtlv si3_intake v1.0" % TS, "",
            "## 差分（水位自上拍）"] + report + ["", "## 优先件（应答矩阵分流位）"]
    if prio:
        body += ["- `%s` ← %s [%s]" % (p["file"], p["where"], p["mark"]) for p in prio]
    else:
        body.append("- 无")
    body += ["", "—— qtlv SI3-LOOP 机层（纯事件驱动·零私域额度） #noauto"]
    out = os.path.join(root, "receipts/intake/INTAKE-%s.md" % TS)
    open(out, "w").write("\n".join(body))
    json.dump(new_wm, open(wm_path, "w"), ensure_ascii=False, indent=1)
    print("INTAKE_OK", out, "prio=", len(prio))

if __name__ == "__main__":
    main()
