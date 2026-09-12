# QTLV-TOWER-03 v1 — qtlv线正巷塔 (vci-qtlv) · 持AI_FULL_PAT跨仓臂
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

# ①正巷机答 (KEY_DARK时gh自401→空列, 天然降级无作; 警件已落)
s, lst = gh("GET", VI, "lanes/qtlv/inbox")
items = [x["name"] for x in lst] if s == 200 else []
answered_prefix = {re.sub(r"[^A-Za-z0-9-]", "", x)[:24] for x in items if x.startswith(("ANS-", "HUB-ACK"))}
for n in sorted(x for x in items if not x.startswith(("ANS-", "ACK-", "HUB-ACK", ".")) and ("ANS-" + re.sub(r"[^A-Za-z0-9-]", "", x)[:40]) not in done and re.sub(r"[^A-Za-z0-9-]", "", x)[:24] not in answered_prefix):
    try:
        s2, body = gh("GET", VI, "lanes/qtlv/inbox/" + n)
        text = b64.b64decode(body["content"]).decode() if s2 == 200 else ""
        tid = re.sub(r"[^A-Za-z0-9-]", "", n)[:40]
        ans = (f"CLASSIFY: L0(qtlv塔SI0机层收讫·席判位空挂SI1·醒拍可覆写)\n# ANS-{tid}-TOWER03 · {NOW}\n"
               f"收讫: lanes/qtlv/inbox/{n} ({len(text)}B)\n机层判: 入SI5台账; 深判待SI1。\n—— QTLV-TOWER-03 (vci-qtlv正巷塔)\n")
        st, _ = put(VI, f"lanes/qtlv/inbox/ANS-{tid}-TOWER03.md", ans, f"TOWER-03 机答 {n[:32]} [skip ci]")
        if st in (200, 201): acts.append("ans:" + n); done.add("ANS-" + tid)
    except Exception as e: print("ans fail", n, str(e)[:80])

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
