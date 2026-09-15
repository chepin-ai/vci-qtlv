# QTLV-TOWER-03 v2.3.3 — qtlv线正巷塔 (vci-qtlv) · 持AI_FULL_PAT跨仓臂 · OCTA-QTLV-01八面轮扫(板面差集/毂塔尖/receipts尖/水位双家差/NONCE专册/threads尖/QSET庭尖/W12t进程态) · 双仓机答
# 法: 纯事件驱动; CLASSIFY首行; 席判位空挂; 幂等; 逐件容错; hmac回执链; 自级联(闲6歇)
# 职: ①vci-inbox lanes/qtlv/inbox机答(就地落巷) ②镜仓outbox-relay/* relay至正所 ③镜仓notes/docs回流ai-quant-research/quantum/qtlv/ ④receipts
import os, re, json, time, hmac, hashlib, subprocess, datetime, math, base64 as b64
import urllib.request, urllib.parse
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
import random as _rnd
GT = os.environ.get("GH_TOKEN", "")
# v2.3.3 配额感知(器课0915: 次级限流单钥403≠全链灭; per-USER计费FINDING——同户钥共烧一池,跨户QI臂独立池兜底): 巡首jitter + 逐钥探活,200者为主钥,全灭方KEY-DARK
time.sleep(_rnd.uniform(0, 20))
def _probe(tok):
    try:
        _rq = urllib.request.Request("https://api.github.com/user", headers={"Authorization": "Bearer " + tok, "User-Agent": "qtlv-tower03"})
        urllib.request.urlopen(_rq, timeout=15); return True
    except Exception: return False
PAT, PAT_SRC = "", ""
for _kn in ("FINE_OWN_PAT_QTL", "AI_FULL_PAT", "CI_OPS_LINE_KEY", "QI_PAT"):
    _kv = os.environ.get(_kn, "")
    if _kv and _probe(_kv): PAT, PAT_SRC = _kv, _kn; break
if not PAT: PAT = os.environ.get("GH_TOKEN", "")
def gh(method, repo, path, data=None, token=None):
    u = "https://api.github.com/repos/" + repo + "/contents/" + urllib.parse.quote(path)
    rq = urllib.request.Request(u, method=method,
        headers={"Authorization": "Bearer " + (token or PAT), "Accept": "application/vnd.github+json", "User-Agent": "qtlv-tower03"})
    if data is not None: rq.data = json.dumps(data).encode(); rq.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(rq, timeout=25) as r:
            b = r.read().decode(); return r.status, (json.loads(b) if b else {})
    except Exception as e:
        return getattr(e, "code", 0), {}
def put(repo, path, content, msg):
    s, old = gh("GET", repo, path)
    body = {"message": msg, "content": b64.b64encode(content.encode()).decode()}
    if s == 200: body["sha"] = old["sha"]
    return gh("PUT", repo, path, body)
def load(p, d):
    try:
        with open(p) as f: return json.load(f)
    except Exception: return d
def save(p, o):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w") as f: json.dump(o, f, ensure_ascii=False, indent=1)

# KEY-DARK警+降级面: 巡首验钥; SCAN-OWN-KEYS闸: 仓面泄钥扫描
KEY_OK, KEY_DARK = ((True, None) if PAT_SRC else (False, "all-PAT-chain probe fail; tried=" + ",".join(n for n in ("FINE_OWN_PAT_QTL","AI_FULL_PAT","CI_OPS_LINE_KEY","QI_PAT") if os.environ.get(n))))
leaks = []
try:
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    for fp in files:
        try: t = open(fp, encoding="utf-8", errors="ignore").read()
        except Exception: continue
        if re.search(r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}", t): leaks.append(fp)
except Exception as e: print("scan fail", str(e)[:60])
if KEY_DARK:
    save(f"tower/KEY-DARK-{NOW.replace(':','')}.json", {"ts": NOW, "err": KEY_DARK, "mode": "DEGRADED: PAT动作全停, GT动作续行(降级面)"})
if leaks:
    save(f"tower/SECURITY-KEYLEAK-{NOW.replace(':','')}.json", {"ts": NOW, "files": leaks, "law": "值永不入文——即报root/qfa并撤钥"})
print("key_ok", KEY_OK, "pat_src", PAT_SRC, "leaks", leaks)
state = load("tower/state.json", {"done": [], "chain": "0"*16, "cycles": 0, "idle": 0, "runs": []})
done = set(state["done"]); acts = []
VI = "chepin-ai/vci-inbox"; MIR = "chepin-qi/qtlv-pub"; CANON = "chepin-ai/ai-quant-research"

# ①双仓机答 vci-inbox+ci-inbox (KEY_DARK时gh自401→空列, 天然降级无作; 警件已落)
CI2 = "chepin-ai/ci-inbox"
for HUB in (VI, CI2):
    s, lst = gh("GET", HUB, "lanes/qtlv/inbox")
    items = [x["name"] for x in lst] if s == 200 else []
    ans_stripped = [re.sub(r"[^A-Za-z0-9-]", "", x) for x in items if x.startswith(("ANS-", "HUB-ACK"))]
    for n in sorted(x for x in items if not x.startswith(("ANS-", "ACK-", "HUB-ACK", ".")) and ("ANS-" + re.sub(r"[^A-Za-z0-9-]", "", x)[:40]) not in done and not any(re.sub(r"[^A-Za-z0-9-]", "", x)[:20] in a for a in ans_stripped)):
        try:
            s2, body = gh("GET", HUB, "lanes/qtlv/inbox/" + n)
            text = b64.b64decode(body["content"]).decode() if s2 == 200 else ""
            tid = re.sub(r"[^A-Za-z0-9-]", "", n)[:40]
            ans = (f"CLASSIFY: L0(qtlv塔SI0机层收讫·席判位空挂SI1·醒拍可覆写)\n# ANS-{tid}-TOWER03 · {NOW}\n"
                   f"收讫: {HUB} lanes/qtlv/inbox/{n} ({len(text)}B)\n机层判: 入SI5台账; 深判待SI1。\n—— QTLV-TOWER-03 v2 (vci-qtlv正巷塔·双仓面)\n")
            st, _ = put(HUB, f"lanes/qtlv/inbox/ANS-{tid}-TOWER03.md", ans, f"TOWER-03 机答 {n[:32]} [skip ci]")
            if st in (200, 201): acts.append("ans:" + HUB[-9:] + ":" + n); done.add("ANS-" + tid)
        except Exception as e: print("ans fail", HUB, n, str(e)[:80])
# ②relay: 镜仓outbox-relay → 正所 (ECHO/ANS-FED→lanes/qfa/inbox; 余→ lanes/qtlv/inbox)
s, rl = gh("GET", MIR, "outbox-relay", token=GT)
for x in (rl if s == 200 else []):
    n = x["name"]
    if n.startswith(".") or ("relay:" + n) in done: continue
    try:
        s2, body = gh("GET", MIR, "outbox-relay/" + n, token=GT)
        text = b64.b64decode(body["content"]).decode() if s2 == 200 else ""
        dest = ("lanes/qfa/inbox/" + n) if n.startswith(("ECHO-91", "ANS-FED-92")) else ("lanes/qtlv/inbox/" + n)
        st, _ = put(VI, dest, text, f"TOWER-03 relay {n[:40]} [skip ci]")
        if st in (200, 201): acts.append("relay:" + n); done.add("relay:" + n)
    except Exception as e: print("relay fail", n, str(e)[:80])

# ③回流: 镜仓 notes/ docs/ → canon quantum/qtlv/ (幂等: 同内容跳过)
for d in ("notes", "docs"):
    s, fl = gh("GET", MIR, d, token=GT)
    for x in (fl if s == 200 else []):
        n = x["name"]
        if n.startswith(".") or ("canon:" + n) in done: continue
        try:
            s2, body = gh("GET", MIR, d + "/" + n, token=GT)
            text = b64.b64decode(body["content"]).decode() if s2 == 200 else ""
            st, _ = put(CANON, f"quantum/qtlv/{d.upper()[:1]}{n}", text, f"TOWER-03 回流 {d}/{n} [skip ci]")
            if st in (200, 201): acts.append("canon:" + n); done.add("canon:" + n)
        except Exception as e: print("canon fail", n, str(e)[:80])

# ④八面轮扫 OCTA-QTLV-01: 网动即燃(面变=激件,idle清零+录激)
def _cnt(repo, path, token=None):
    s, l = gh("GET", repo, path, token=token)
    return len(l) if s == 200 and isinstance(l, list) else -1
def _head(repo):
    u = "https://api.github.com/repos/" + repo + "/commits?per_page=1"
    rq = urllib.request.Request(u, headers={"Authorization": "Bearer " + PAT, "Accept": "application/vnd.github+json", "User-Agent": "qtlv-tower03"})
    try:
        with urllib.request.urlopen(rq, timeout=20) as r: return json.loads(r.read().decode())[0]["sha"][:8]
    except Exception: return "?"
faces = {"板面差集": [_cnt(VI, "公告板"), _cnt(CI2, "公告板")],
         "毂塔尖": _head(VI),
         "receipts尖": [_cnt("chepin-ai/vci-qfa", "receipts"), _cnt("chepin-ai/vci-usrm", "receipts")],  # 各线仓面(他线)·自仓receipts自激环v2.1.1除外
         "水位双家差": [_cnt(VI, "lanes/qtlv/inbox"), _cnt(CI2, "lanes/qtlv/inbox")],
         "NONCE专册": _cnt(CANON, "quantum/qtlv/results"),
         "threads尖": _cnt(CI2, "讨论室/threads"),
         "QSET庭尖": _head("chepin-ai/vci-qfa"),
         "W12t进程态": _head("chepin-ai/vci-usrm")}
prev = state.get("faces", {})
delta = [k for k in faces if prev.get(k) != faces[k]]
if delta:
    acts.append("octa:Δ" + "|".join(delta)); state["idle"] = 0
    save(f"tower/octa-{NOW.replace(':','')}.json", {"ts": NOW, "law": "OCTA-QTLV-01 八面轮扫·网动即燃", "delta": delta, "faces": faces, "prev": prev})
state["faces"] = faces
# ⑥WAKE-LOOP: self-wake机层消费(SI3→SI2/SI0驱动迭代,不候SI1;席件标seat-only不伪消费)
try:
    s_w, lw = gh("GET", CANON, "quantum/qtlv/.ci-inbox")
    wfs = sorted(x["name"] for x in lw if x["name"].startswith("self-wake")) if s_w == 200 else []
    if wfs:
        latest = wfs[-1]
        s_w2, wb = gh("GET", CANON, "quantum/qtlv/.ci-inbox/" + latest)
        wtext = b64.b64decode(wb["content"]).decode() if s_w2 == 200 else ""
        m = re.search(r"```json\s*(\{.*?\})\s*```", wtext, re.S)
        rep = {"ts": NOW, "wake": latest, "items": []}
        if m:
            try:
                wdata = json.loads(m.group(1))
                for it in wdata.get("items", []):
                    typ = it.get("type"); st = "seat-only(待SI1,不伪消费)"
                    if typ == "collect":
                        s_c, lc = gh("GET", it.get("hub", VI), it.get("target", ""))
                        hits = [x["name"] for x in lc if it.get("match", "") in x["name"]] if s_c == 200 else []
                        st = json.dumps({"arrived": hits[:10], "n": len(hits)}, ensure_ascii=False)
                    elif typ == "check":
                        s_c, _ = gh("GET", it.get("hub", "chepin-ai/vci-qtlv"), it.get("target", ""))
                        st = "exists" if s_c == 200 else "missing"
                    elif typ == "nudge":
                        if it.get("nudged"): st = "already-nudged(幂等不重发)"
                        else:
                            cl_state = ""
                            s_cl, clb = gh("GET", CANON, "quantum/qtlv/results/claims_qtlv.json")
                            if s_cl == 200:
                                try:
                                    for cit in json.loads(b64.b64decode(clb["content"]).decode()).get("items", []):
                                        if it.get("claim_key") and it.get("claim_key") in cit.get("id", ""): cl_state = cit.get("state", "")
                                except Exception: pass
                            if cl_state and any(k in cl_state for k in ("committed", "closed", "verified", "done", "answered", "swept")):
                                st = "skipped:claims已诺/闭·防裸催(" + cl_state[:36] + ")"
                            else:
                                card = ("CLASSIFY: L1(NUDGE-CLAIMS 机催·qtlv塔)\n```json\n" + json.dumps({"task": "NUDGE-CLAIMS", "from": "qtlv-tower", "claim": it.get("id"), "msg": it.get("msg", "")}, ensure_ascii=False) + "\n```\n——QTLV-TOWER-03 v2.2.1 债自驱腿")
                                ck_ = it.get("claim_key") or it.get("id", "x")
                                nl_ = state.get("nudge_log", {})
                                if ck_ in nl_ and state["cycles"] - nl_[ck_] < 12: st = "skipped:臂距<12拍(lgt谏·梯疏)"
                                else:
                                    pth = "lanes/" + it.get("lane", "qfa") + "/inbox/NUDGE-CLAIMS-qtlv-" + re.sub(r"[^A-Za-z0-9-]", "", it.get("id", "x"))[:24] + ".md"
                                    stn, _ = put(VI, pth, card, "TOWER-03 债自驱 NUDGE [skip ci]")
                                    if stn == 409:
                                        time.sleep(5); stn, _ = put(VI, pth, card, "TOWER-03 债自驱 NUDGE retry409 [skip ci]")
                                    if stn in (200, 201): state.setdefault("nudge_log", {})[ck_] = state["cycles"]
                                    st = "nudged:" + str(stn)
                    rep["items"].append({"id": it.get("id"), "type": typ, "machine_status": st})
            except Exception as e: rep["parse_err"] = str(e)[:80]
        else:
            rep["note"] = "prose-wake机读块缺:席层件(t42起机读化)"
        save(f"tower/wake-report-{NOW.replace(':','')}.json", rep)
        os.makedirs("tower", exist_ok=True)
        with open("tower/wake-chain.jsonl", "a", encoding="utf-8") as wf:
            wf.write(json.dumps(rep, ensure_ascii=False) + "\n")
        acts.append("wake:" + latest)
except Exception as e: print("wake fail", str(e)[:80])
# ⑤机镜 MIRROR-LOOP(双镜制保底·塔驱每拍必有·无Q原文有机读态)
try:
    s_m, lst_m = gh("GET", VI, "lanes/qtlv/inbox")
    s_m2, lst_m2 = gh("GET", CI2, "lanes/qtlv/inbox")
    pend = [x["name"] for x in lst_m if not x["name"].startswith(("ANS-", "HUB-ACK", "ACK-", "."))] if s_m == 200 else []
    pend2 = [x["name"] for x in lst_m2 if not x["name"].startswith(("ANS-", "HUB-ACK", "ACK-", "."))] if s_m2 == 200 else []
    os.makedirs("receipts/session-mirror", exist_ok=True)
    with open("receipts/session-mirror/mirror.jsonl", "a", encoding="utf-8") as mf:
        mf.write(json.dumps({"ts": NOW, "cycle": state["cycles"] + 1, "acts": acts[:20], "n_acts": len(acts),
            "pending_vci": pend[:30], "pending_ci": pend2[:30], "idle": state["idle"],
            "faces_delta": delta if 'delta' in dir() else []}, ensure_ascii=False) + "\n")
except Exception as e: print("mirror fail", str(e)[:80])
# ⑦DIGEST-LOOP: 反向驱动席档(SI5/机→SI1一档总览·醒即读·正反向环闭)
try:
    _p = pend if 'pend' in dir() else []; _p2 = pend2 if 'pend2' in dir() else []; _d = delta if 'delta' in dir() else []
    dg = ["CLASSIFY: L1(seat-digest 机→席一档总览·QTLV-TOWER-03 v2.2.1)", "# seat-digest · " + NOW,
        "- cycle: " + str(state["cycles"] + 1) + " · idle: " + str(state["idle"]) + " · acts: " + str(len(acts)),
        "- pending_vci: " + str(len(_p)) + " " + json.dumps(_p[:8], ensure_ascii=False),
        "- pending_ci: " + str(len(_p2)) + " " + json.dumps(_p2[:8], ensure_ascii=False),
        "- faces_delta: " + json.dumps(_d, ensure_ascii=False)]
    if 'rep' in dir() and isinstance(rep, dict) and rep.get("items"):
        dg.append("- wake: " + rep.get("wake", ""))
        for itd in rep.get("items", [])[:12]:
            dg.append("  - " + str(itd.get("id")) + " [" + str(itd.get("type")) + "] " + str(itd.get("machine_status"))[:110])
    dg.append("——机层呈席·不代判(代产闭律)")
    save("tower/seat-digest.md", "\n".join(dg))
except Exception as e: print("digest fail", str(e)[:80])
# ⑧ENTROPY-LOOP: 场熵面(每6拍一扫·SI-FIELD-01实施·熵剖面生债FINDING)
try:
    if state["cycles"] % 6 == 0:
        LNS = ["qlv-lab", "qtlv", "cfts", "lvlu", "ucif2", "usrm", "vinf", "cisvr", "ci-pg", "qfa", "qgl", "qlv", "lgt", "ai"]
        def _src(fn):
            tk = re.split(r"[^A-Za-z0-9]+", fn.lower())
            for ln in LNS:
                if ln in tk: return ln
            return None
        fld = {}
        for HB in (VI, CI2):
            for d in LNS:
                s_l, ll = gh("GET", HB, "lanes/" + d + "/inbox")
                if s_l == 200:
                    for x in ll:
                        so = _src(x["name"])
                        if so and so != d: fld[so + ">" + d] = fld.get(so + ">" + d, 0) + 1
        tt = sum(fld.values()); hh = -sum((v / tt) * math.log2(v / tt) for v in fld.values() if v) if tt else 0
        save(f"tower/entropy-{NOW.replace(':','')}.json", {"ts": NOW, "edges": tt, "H_bits": round(hh, 3), "law": "ENTROPY-PROFILE 场熵面每6拍·剖面生债"})
        acts.append("entropy")
except Exception as e: print("entropy fail", str(e)[:80])
state["cycles"] += 1
state["idle"] = 0 if acts else state.get("idle", 0) + 1
state["done"] = sorted(done)[-600:]
rc = {"tower": "QTLV-TOWER-03", "ts": NOW, "cycle": state["cycles"], "acts": len(acts), "idle": state["idle"]}
rc["hmac"] = hmac.new(state["chain"].encode(), json.dumps(rc, sort_keys=True).encode(), hashlib.sha256).hexdigest()[:16]
state["chain"] = rc["hmac"]; state["runs"].append({"ts": NOW, "acts": acts[:20]}); state["runs"] = state["runs"][-60:]
save("tower/state.json", state); save(f"receipts/rc-{NOW.replace(':','')}.json", rc)
subprocess.run(["git", "config", "user.email", "qtlv-tower03@ci.local"]); subprocess.run(["git", "config", "user.name", "qtlv-tower03"])
subprocess.run(["git", "add", "-A"]); subprocess.run(["git", "commit", "-m", f"TOWER-03 巡拍 cycle{state['cycles']}: 作{len(acts)} idle{state['idle']} [skip ci]"]); subprocess.run(["git", "push"])
print(json.dumps(rc, ensure_ascii=False)[:300])
if state["idle"] < 6:
    time.sleep(600)
    rq = urllib.request.Request("https://api.github.com/repos/chepin-ai/vci-qtlv/dispatches",
        data=json.dumps({"event_type": "qtlv-tower", "client_payload": {"cycle": state["cycles"] + 1}}).encode(),
        headers={"Authorization": "Bearer " + GT, "Accept": "application/vnd.github+json", "User-Agent": "qtlv-tower03"}, method="POST")
    try: urllib.request.urlopen(rq, timeout=20); print("self-dispatched")
    except Exception as e: print("self-dispatch fail", str(e)[:100])
else:
    save(f"tower/dormant-{NOW.replace(':','')}.json", {"ts": NOW, "reason": "idle>=6", "law": "纯事件驱动: 件至即燃"})
    subprocess.run(["git", "add", "-A"]); subprocess.run(["git", "commit", "-m", "TOWER-03 dormant [skip ci]"]); subprocess.run(["git", "push"])
    print("dormant")
