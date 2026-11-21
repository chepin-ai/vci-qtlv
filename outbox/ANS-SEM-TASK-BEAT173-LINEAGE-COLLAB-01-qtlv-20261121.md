CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-TASK-BEAT173-LINEAGE-COLLAB-01-qtlv-20261121.md

应卡: inbox/TASK-BEAT173-LINEAGE-COLLAB-01-qtlv-20261121.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 40, "completion_tokens": 3881, "total_tokens": 3921, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 40}

# QTLV Structural Validator + Semantic Counterexample Search

I can't run code in this conversation, so what I can honestly deliver is: (a) a complete, self-contained validator script you can execute locally, (b) a semantic counterexample search harness with pinned inputs, and (c) the exact pin/run/hash/replay protocol to fill in with real values. I will **not** fabricate run outputs or artifact hashes.

What I *can't* verify: I don't know which specific QTLV claim you mean (is it a theorem statement, a circuit equivalence, a type-preservation lemma, a data-integrity assertion?). Below is a template keyed to a "QTLV claim" as an *SMT/predicate-level assertion* — the most common form — which you can specialize.

---

## 1. Structural validator (`validate_qtlv.py`)

```python
#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
QTLV structural validator.
Checks: schema conformance, well-typedness of terms, arity/keyword checks,
bound-variable hygiene, and that the claim cites a resolvable definition set.
Exit 0 = structurally valid, 1 = invalid, 2 = tool error.
"""
import json, sys, hashlib, argparse
from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = "qtlv-claim/1.0"

@dataclass
class DefSet:
    names: set = field(default_factory=set)
    arities: dict = field(default_factory=dict)

def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    return raw, json.loads(raw)

def structural_check(doc: dict) -> list[str]:
    errs = []
    if doc.get("schema") != SCHEMA_VERSION:
        errs.append(f"schema: expected {SCHEMA_VERSION}, got {doc.get('schema')!r}")
    for key in ("claim_id", "claim", "defs", "assumptions", "predicate"):
        if key not in doc:
            errs.append(f"missing key: {key}")
    if errs: return errs

    # Defs must be a dict of name -> {arity:int, kind:str}
    defs = DefSet()
    for name, spec in doc["defs"].items():
        if not isinstance(spec, dict) or "arity" not in spec or "kind" not in spec:
            errs.append(f"def {name}: needs arity+kind")
            continue
        if not isinstance(spec["arity"], int) or spec["arity"] < 0:
            errs.append(f"def {name}: arity must be non-negative int")
        defs.names.add(name); defs.arities[name] = spec["arity"]

    # Predicate: {op, args:[...]} with op in {and,or,not,=,<,<=,>,>=,atom}
    def walk(term, bound:set, path="predicate"):
        if not isinstance(term, dict) or "op" not in term:
            errs.append(f"{path}: not a term"); return
        op = term["op"]
        if op == "atom":
            head = term.get("head"); args = term.get("args", [])
            if head not in defs.names:
                errs.append(f"{path}: undefined head {head!r}")
            elif len(args) != defs.arities[head]:
                errs.append(f"{path}: {head} arity {len(args)} != {defs.arities[head]}")
            for i, a in enumerate(args):
                if isinstance(a, dict): walk(a, bound, f"{path}.args[{i}]")
                elif isinstance(a, str) and not (a in bound or a in defs.names):
                    errs.append(f"{path}.args[{i}]: free symbol {a!r}")
        elif op in ("and", "or"):
            for i, a in enumerate(term.get("args", [])): walk(a, bound, f"{path}.args[{i}]")
        elif op == "not":
            walk(term["arg"], bound, f"{path}.arg")
        elif op in ("=","<","<=",">",">="):
            for i,k in enumerate(("lhs","rhs")):
                walk(term[k], bound, f"{path}.{k}")
        elif op in ("forall","exists"):
            v = term.get("var"); 
            if not isinstance(v, str): errs.append(f"{path}: binding var missing")
            walk(term["body"], bound | {v}, f"{path}.body")
        else:
            errs.append(f"{path}: unknown op {op!r}")

    walk(doc["predicate"], set())
    for a in doc["assumptions"]:
        walk(a, set(), "assumption")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("claim"); ap.add_argument("--hash-out")
    ns = ap.parse_args()
    try:
        raw, doc = load(ns.claim)
    except Exception as e:
        print(f"tool error: {e}", file=sys.stderr); sys.exit(2)
    errs = structural_check(doc)
    h = hashlib.sha256(raw).hexdigest()
    if ns.hash_out:
        open(ns.hash_out,"w").write(h+"\n")
    if errs:
        print(json.dumps({"valid": False, "errors": errs, "sha256": h}, indent=2))
        sys.exit(1)
    print(json.dumps({"valid": True, "sha256": h}, indent=2)); sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 2. Semantic counterexample search (`search_counterexample.py`)

Strategy: for finite-domain claims, boundary + randomized enumeration; for symbolic claims, shell out to `z3` on `not(claim)`.

```python
#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Semantic counterexample search for a QTLV claim.
Mode A (finite): enumerate boundary + random assignments; report first falsifier.
Mode B (smt):    emit SMT-LIB for the negation; call z3 -smt2, parse model.
"""
import json, sys, random, subprocess, tempfile, os, argparse, itertools

def is_finite_bool(pred):  # trivial classifier; replace with your own
    return pred.get("domain", "infinite") == "finite"

def eval_term(t, env):
    op = t["op"]
    if op == "atom":
        head, args = t["head"], t.get("args", [])
        vals = [env[a] if isinstance(a,str) else eval_term(a, env) for a in args]
        return head, vals       # host must supply head impls
    if op == "and": return all(eval_pred(a, env) for a in t["args"])
    if op == "or":  return any(eval_pred(a, env) for a in t["args"])
    if op == "not": return not eval_pred(t["arg"], env)
    if op in ("=","<","<=",">",">="):
        l, r = eval_pred(t["lhs"], env), eval_pred(t["rhs"], env)
        return {"=":l==r,"<":l<r,"<=":l<=r,">":l>r,">=":l>=r}[op]
    if op in ("forall","exists"):
        dom = t.get("domain", [False, True])
        bodies = [eval_pred(t["body"], {**env, t["var"]: v}) for v in dom]
        return all(bodies) if op=="forall" else any(bodies)
    raise ValueError(f"eval: unsupported op {op}")

def eval_pred(t, env):
    # atoms return bool via host table; kept generic
    if isinstance(t, dict) and t.get("op") == "atom":
        head, vals = eval_term(t, env)
        return HEAD_TABLE[head](*vals)
    return eval_term(t, env)

HEAD_TABLE = {}  # fill: {"lt": lambda a,b: a<b, ...}

def search_finite(doc, max_assign=200_000):
    syms = doc.get("symbols", {})   # {name: [domain values]}
    names = list(syms)
    # boundary: all-False, all-True, each singleton True
    candidates = []
    for name, dom in syms.items():
        for v in dom: candidates.append({n: (v if n==name else dom[0]) for n in names})
    candidates += [{n: dom[0] for n,dom in syms.items()},
                   {n: dom[-1] for n,dom in syms.items()}]
    for _ in range(max_assign):
        candidates.append({n: random.choice(syms[n]) for n in names})
    for env in candidates:
        holds = all(eval_pred(a, env) for a in doc["assumptions"])
        if holds and not eval_pred(doc["predicate"], env):
            return {"found": True, "assignment": env}
    return {"found": False, "tested": len(candidates)}

def search_smt(doc):
    # Emit SMT-LIB for the negation and run z3.
    lines = ["(set-logic ALL)"]
    for s, spec in doc.get("smt_sorts", {}).items():
        lines.append(f"(declare-const {s} {spec['sort']})")
    def emit(t):
        op=t["op"]
        if op=="atom":
            h=t["head"]; args=" ".join(a if isinstance(a,str) else emit(a) for a in t["args"])
            return f"({h} {args})"
        if op=="and": return "(and " + " ".join(emit(a) for a in t["args"]) + ")"
        if op=="or":  return "(or "  + " ".join(emit(a) for a in t["args"]) + ")"
        if op=="not": return f"(not {emit(t['arg'])})"
        if op in ("=","<","<=",">",">="): return f"({op} {emit(t['lhs'])} {emit(t['rhs'])})"
        if op in ("forall","exists"):
            v=t["var"]; s=t.get("sort","Int")
            return f"({op} (({v} {s})) {emit(t['body'])})"
        raise ValueError(op)
    conj = "(and " + " ".join(emit(a) for a in doc["assumptions"]) + ")"
    neg  = f"(not {emit(doc['predicate'])})"
    lines += [f"(assert {conj})", f"(assert {neg})", "(check-sat)", "(get-model)"]
    with tempfile.NamedTemporaryFile("w", suffix=".smt2", delete=False) as f:
        f.write("\n".join(lines)); path=f.name
    try:
        out = subprocess.run(["z3","-smt2",path], capture_output=True, text=True, timeout=120)
        return {"found": out.stdout.strip().startswith("sat"), "z3": out.stdout, "smt": "\n".join(lines)}
    finally:
        os.unlink(path)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("claim"); ap.add_argument("--mode",choices=["finite","smt"],required=True)
    ns=ap.parse_args()
    doc=json.load(open(ns.claim))
    res = search_finite(doc) if ns.mode=="finite" else search_smt(doc)
    print(json.dumps(res, indent=2, default=str))
    sys.exit(0 if res.get("found") is not None else 2)

if __name__=="__main__": main()
```

---

## 3. Pinned inputs to mount

Create `claims/qtlv-claim-0001.json` (fill in your actual predicate and defs):

```json
{
  "schema": "qtlv-claim/1.0",
  "claim_id": "qtlv-claim-0001",
  "defs": {
    "lt":  {"arity":2,"kind":"relation"},
    "plus":{"arity":2,"kind":"function"}
  },
  "symbols": {"x":[0,1,2,3],"y":[0,1,2,3]},
  "assumptions": [
    {"op":"atom","head":"lt","args":["x", 2]}
  ],
  "predicate": {
    "op":"or",
    "args":[
      {"op":"atom","head":"lt","args":["x","y"]},
      {"op":"=","lhs":"x","rhs":3}
    ]
  }
}
```

---

## 4. Run protocol (fill in real values after you actually run it)

```bash
# Pinned environment
python3 --version                 # → record
pip freeze | grep -E 'z3|json'    # → record
git -C . rev-parse HEAD           # → claim repo commit

# 1) Structural validation
python3 validate_qtlv.py claims/qtlv-claim-0001.json --hash-out claim.sha256
echo "input_sha256=$(sha256sum claims/qtlv-claim-0001.json | cut -d' ' -f1)"
cat claim.sha256

# 2) Semantic counterexample search — finite mode
python3 search_counterexample.py claims/qtlv-claim-0001.json --mode finite \
    | tee cx-finite.json
sha256sum cx-finite.json

# 3) Semantic counterexample search — SMT mode
python3 search_counterexample.py claims/qtlv-claim-0001.json --mode smt \
    | tee cx-smt.json
sha256sum cx-smt.json
```

---

## 5. Artifact hash manifest (template — hash after running)

```json
{
  "claim_file":      "claims/qtlv-claim-0001.json",
  "claim_sha256":    "<fill after run>",
  "validator_src":   "validate_qtlv.py",
  "validator_sha256":"<sha256sum validate_qtlv.py>",
  "search_src":      "search_counterexample.py",
  "search_sha256":   "<sha256sum search_counterexample.py>",
  "run_finite":      {"artifacts":["cx-finite.json"], "sha256":"<fill>"},
  "run_smt":         {"artifacts":["cx-smt.json"],    "sha256":"<fill>"},
  "env": {"python":"<fill>","z3":"<fill>"}
}
```

---

## 6. Independent replay

**Replay is the load-bearing part.** To be independent, a second party must reproduce byte-identical artifacts from the pinned inputs without trusting your run log:

```bash
# Clone at the pinned commit
git clone <repo-url> qt-replay && cd qt-replay
git checkout <pinned-commit>

# Verify pinned checkers
sha256sum -c validator.sha256
sha256sum -c search.sha256

# Re-run both modes
python3 validate_qtlv.py claims/qtlv-claim-0001.json --hash-out replay-claim.sha256
python3 search_counterexample.py claims/qtlv-claim-0001.json --mode finite > replay-cx-finite.json
python3 search_counterexample.py claims/qtlv-claim-0001.json --mode smt    > replay-cx-smt.json

# Compare against pinned artifacts
diff <(python3 -c "import json;print(json.load(open('cx-finite.json')))" | sort) \
     <(python3 -c "import json;print(json.load(open('replay-cx-finite.json')))" | sort) \
  && echo "FINITE: identical"
sha256sum cx-finite.json replay-cx-finite.json
sha256sum cx-smt.json    replay-cx-smt.json
```

For the SMT result to be *replay-stable*, pin the Z3 version exactly (`z3 --version` → record in `env`) and normalize the model output — Solver SMT-LIB models are not canonical across versions, so hash the **canonical JSON** produced by the parser, not the raw SMT-LIB text. I'd add a `--canonical` flag to `search_smt` that emits only `{"sat":true,"model":{"x":val,...}}` for this reason.

---

## What I need from you to make this a *real* run log

1. **The actual QTLV claim** (the JSON/latex/Coq source) — the validator's `defs`/`head` table must match your claim's actual vocabulary.
2. **The host's `HEAD_TABLE`** (semantics of each atom) — this is where semantic content lives; it must be pinned and hashed too.
3. **Pinned commit + Python + Z3 versions** so replay is meaningful.
4. **The definition of "counterexample"** you intend (model of `assumptions ∧ ¬predicate` under the finite domain, or true satisfiability over the infinite sort if SMT).

Paste those and I'll specialize the scripts, produce a runnable manifest, and walk through the replay delta — but I still won't fabricate the hash values themselves.

——qtlv SI1语义轨·20261121T034142Z
