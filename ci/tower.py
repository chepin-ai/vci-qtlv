# QTLV-TOWER-03 v2.0 — qtlv线正巷塔 (vci-qtlv) · 持AI_FULL_PAT跨仓臂 · OCTA-QTLV-01八面轮扫(板面差集/毂塔尖/receipts尖/水位双家差/NONCE专册/threads尖/QSET庭尖/W12t进程态) · 双仓机答
# 法: 纯事件驱动; CLASSIFY首行; 席判位空挂; 幂等; 逐件容错; hmac回执链; 自级联(闲6歇)
# 职: ①vci-inbox lanes/qtlv/inbox机答(就地落巷) ②镜仓outbox-relay/* relay至正所 ③镜仓notes/docs回流ai-quant-research/quantum/qtlv/ ④receipts
import os, re, json, time, hmac, hashlib, subprocess, datetime, base64 as b64
import urllib.request, urllib.parse
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
PAT = os.environ.get("AI_FULL_PAT") or os.environ.get("CI_OPS_LINE_KEY") or os.environ.get("GH_TOKEN", "")
GT = os.environ.get("GH_TOKEN", "")
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
KEY_OK, KEY_DARK = True, None
try:
    _rq = urllib.request.Request("https://api.github.com/user", headers={"Authorization": "Bearer " + PAT, "User-Agent": "qtlv-tower03"})
    urllib.request.urlopen(_rq, timeout=15)
except Exception as e:
    KEY_OK = False; KEY_DARK = str(e)[:60]
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
print("key_ok", KEY_OK, "leaks", leaks)
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
                   f"收讫: {HUB} lanes/qtlv/inbox/{n} ({len(text)}B)
机层判: 入SI5台账; 深判待SI1。
—— QTLV-TOWER-03 v2 (vci-qtlv正巷塔·双仓面)
")
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
         "receipts尖": _cnt("chepin-ai/vci-qtlv", "receipts"),
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
