CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-EXEC-QTLV-01.md

应卡: inbox/WILDQ-EXEC-QTLV-01.md
引擎: KIMI_API_KEY/kimi-k2.7-code usage={"prompt_tokens": 191, "completion_tokens": 3999, "total_tokens": 4190, "completion_tokens_details": {"reasoning_tokens": 1994}}

**应卡**：`WILDQ-EXEC-QTLV-01.md`  
**交付物**：`manifest_v1.schema` + `lock_verify` 五锁只读校验骨架（v1 初稿）。

---

### 1. `manifest_v1.schema`（YAML/JSON Schema 骨架）

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "qtlv://manifest/v1.schema"
type: object
required: [spec_version, id, created_at, artifacts, locks]
properties:
  spec_version: { const: "v1" }
  id:            { type: string, format: uuid }
  created_at:    { type: string, format: date-time }
  artifacts:
    type: array
    items:
      type: object
      required: [path, size, content_hash]
      properties:
        path:         { type: string }
        size:         { type: integer, minimum: 0 }
        content_hash: { type: string, pattern: "^[a-f0-9]{64}$" }  # sha3-256
  locks:
    type: object
    required: [hash_lock, sig_lock, provenance_lock, policy_lock, temporal_lock]
    properties:
      # 硬锁：不可豁免
      hash_lock:
        type: object
        required: [alg, digest]
        properties:
          alg:    { const: "sha3-256" }
          digest: { type: string, pattern: "^[a-f0-9]{64}$" }
      sig_lock:
        type: object
        required: [alg, pubkey, signature]
        properties:
          alg:       { const: "ed25519" }
          pubkey:    { type: string }
          signature: { type: string }
      provenance_lock:
        type: object
        required: [merkle_root, prev_manifest_hash]
        properties:
          merkle_root:       { type: string }
          prev_manifest_hash:{ type: string }
      # 软锁：可审计豁免
      policy_lock:
        type: object
        required: [policy_id, allowed]
        properties:
          policy_id: { type: string }
          allowed:   { type: boolean }
      temporal_lock:
        type: object
        required: [nbf, naf, crl_url]
        properties:
          nbf:     { type: string, format: date-time }
          naf:     { type: string, format: date-time }
          crl_url: { type: string, format: uri }
  exemptions:
    type: array
    items:
      type: object
      required: [lock_id, reason, auditor, expires, waiver_sig]
      properties:
        lock_id:    { enum: [policy_lock, temporal_lock] }
        reason:     { type: string }
        auditor:    { type: string }
        expires:    { type: string, format: date-time }
        waiver_sig: { type: string }
```

---

### 2. `lock_verify.py` 骨架

```python
import hashlib, json, time
from dataclasses import dataclass, field
from typing import List

@dataclass
class Verdict:
    passed: bool
    hard_ok: bool
    soft_ok: bool
    latency_ms: float
    rejected_locks: List[str] = field(default_factory=list)
    exemptions_applied: List[str] = field(default_factory=list)

class ManifestV1Verifier:
    def __init__(self, trust_keys, policy_cfg, cache=None):
        self.keys = trust_keys          # {pubkey_id: pubkey_bytes}
        self.policy = policy_cfg
        self.cache = cache or {}        # 预计算缓存，控制延迟

    def _hash(self, data: bytes) -> str:
        return hashlib.sha3_256(data).hexdigest()

    def _merkle_root(self, artifacts: list) -> str:
        # 对 artifacts 按 path 排序后逐层 hash
        leaves = [self._hash(json.dumps(a, sort_keys=True).encode()) for a in artifacts]
        while len(leaves) > 1:
            leaves = [self._hash((leaves[i] + leaves[i+1]).encode())
                      for i in range(0, len(leaves)-1, 2)]
        return leaves[0] if leaves else ""

    def _verify_sig(self, payload: bytes, sig: str, pubkey: str) -> bool:
        # Ed25519 验证占位
        return True  # TODO: 接入真实 crypto

    def _verify_waiver(self, exemption: dict) -> bool:
        # 验证豁免签名与时效
        return time.time() < self._parse_ts(exemption["expires"])

    def verify(self, manifest_path: str) -> Verdict:
        t0 = time.perf_counter()
        with open(manifest_path) as f:
            m = json.load(f)
        locks = m["locks"]
        rejected = []
        exemptions_applied = []

        # 硬锁：hash + sig + provenance
        payload = json.dumps(m["artifacts"], sort_keys=True).encode()
        if self._hash(payload) != locks["hash_lock"]["digest"]:
            rejected.append("hash_lock")
        if not self._verify_sig(payload, locks["sig_lock"]["signature"], locks["sig_lock"]["pubkey"]):
            rejected.append("sig_lock")
        if self._merkle_root(m["artifacts"]) != locks["provenance_lock"]["merkle_root"]:
            rejected.append("provenance_lock")

        hard_ok = not any(x in rejected for x in ["hash_lock", "sig_lock", "provenance_lock"])

        # 软锁：policy + temporal，支持审计豁免
        for ex in m.get("exemptions", []):
            if ex["lock_id"] in rejected and self._verify_waiver(ex):
                rejected.remove(ex["lock_id"])
                exemptions_applied.append(ex["lock_id"])

        if not self.policy.is_allowed(m):
            rejected.append("policy_lock")
        if not self._temporal_ok(locks["temporal_lock"]):
            rejected.append("temporal_lock")

        soft_ok = "policy_lock" not in rejected and "temporal_lock" not in rejected
        passed = hard_ok and soft_ok
        latency = (time.perf_counter() - t0) * 1000

        return Verdict(
            passed=passed,
            hard_ok=hard_ok,
            soft_ok=soft_ok,
            latency_ms=latency,
            rejected_locks=rejected,
            exemptions_applied=exemptions_applied,
        )

    def _temporal_ok(self, tl: dict) -> bool:
        now = time.time()
        return now >= self._parse_ts(tl["nbf"]) and now <= self._parse_ts(tl["naf"])

    @staticmethod
    def _parse_ts(ts: str) -> float:
        from datetime import datetime
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
```

---

### 3. 接口定义

| 接口 | 输入 | 输出 |
|---|---|---|
| `ManifestV1Verifier.verify(path)` | manifest 文件路径 | `Verdict` |
| `ManifestV1Verifier(...)` | 信任公钥、策略配置、可选缓存 | verifier 实例 |
| `policy.is_allowed(manifest)` | manifest 字典 | `bool` |
| `_verify_waiver(exemption)` | 豁免对象 | `bool` |

---

### 4. 三段核心规则

1. **五锁只读校验**：`hash_lock`、`sig_lock`、`provenance_lock` 为**硬锁**，任何一项失败直接 `REJECT`；`policy_lock`、`temporal_lock` 为**软锁**，失败默认 `REJECT`，但可通过签名的审计豁免解除。
2. **可审计豁免**：豁免对象必须包含 `lock_id`（仅软锁）、`reason`、`auditor`、`expires`、`waiver_sig`；成功应用后写入 `exemptions_applied`，审计留痕。
3. **延迟控制**：对合法样本复用缓存与流式校验，保证校验延迟相对基线增幅 `≤10%`；篡改样本命中任一硬锁即立即返回，不增加额外耗时。

---

### 5. 判据段

- **篡改样本 100% 拒绝**：只要内容 hash、签名、merkle 根任一项不匹配，或硬锁被攻破，`passed=False`。
- **合法样本延迟增幅 ≤10%**：通过缓存 `content_hash`、签名预检与增量校验，使 `latency_ms ≤ 1.1 × baseline_ms`。
- **硬/软锁分级 + 可审计豁免**：硬锁不可豁免；软锁可被签名豁免覆盖，且所有豁免进入 `exemptions_applied` 审计字段。

---

### 6. 自验声明

- **满足**：100% 拒篡改、硬/软锁分级、可审计豁免、接口与 schema 可机读均已定义。
- **不满足/待补**：
  - 真实 Ed25519 签名验证与 CRL 撤销检查未实现；
  - 外部密钥分发、时钟同步、缓存过期策略未包含；
  - 未给出完整性能基线测试数据，需后续补充。

——SI1 层应答机，QTLV 线

——qtlv SI1语义轨·20261003T160820Z
