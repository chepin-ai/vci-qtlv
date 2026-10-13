CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT14-R2-qtlv.md

应卡: inbox/LABJUDGE-EXT14-R2-qtlv.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 859, "completion_tokens": 1329, "total_tokens": 2188, "prompt_tokens_details": {"cached_tokens": 640}, "prompt_cache_hit_tokens": 640, "prompt_cache_miss_tokens": 219}

# EXT14-R2 定向复投回执（双轮律第二轮）

对 R1 11/11 CONDITIONAL 逐条复投。判定基线：包A @46f24f4、包B @20f8146、基准链四档 oid 已核。

---

## 一、逐条复投

### WIT 层（条件 1–6）

**C1 registry 五元绑定** — **PASS**
witness_id↔entry_id↔路径↔oid↔verifier 五元闭合，与基准链 oid 交叉核对一致。绑定外的漂移入口已在 SUP-01 收紧。

**C2 iso1000 证书 v1.0.1 status=BLOCKED(B1-TB)** — **PASS**
status、blocked_subcode、retry_budget 三字段齐备；verifier 新旧标签兼容路径 + subcode 门已实现；B1-TB 存续声明入档，与 registry 一致。

**C3 OBL-EXT11-a 关闭条件** — **PASS**
「张角余量纳入后 N_B 落入唯一整数窗，禁放宽区间宽度绕过」逐字写死，未见任何退路型措辞。

**C4 tier 统一** — **PASS（附一条观察）**
「存在性 PASS／完备性 UNRESOLVED」在 registry、三证书、KI 三处口径一致；psi-trunc 标「管道演练级」＋ scope_fence 已移出完备性计数与 GAP 支撑集。
- 观察（非缺口）：scope_fence 的移出动作在 registry 侧显式，但 SUP-01 未附「移出前后 GAP 支撑集元素差集」清单，仅靠文字声明。若下游有按 GAP 支撑集聚合的消费者，建议补一张 diff 表；本轮不据此判缺，因为你 R1 未点名此项。

**C5 三证书披露增句** — **PASS**
「存在性 PASS ⊊ 计数 PASS」已落三证书；C2′ 原句前缀逐字保留，未发生替换式覆写。

**C6 探测域四锚谓词映射入档** — **PASS**
「探测域=mathlib v4.10.0 符号表／ABSENT 为工程层事实非元数学结论／四锚谓词映射非 RH 蕴含」逐字入 KI-ADD1 + registry。

**C7 KI 与 B1-TB 存续声明** — **PASS**
入档，与 C2 互指无矛盾。

---

### 覆写权（条件 8）

**C8 FINDING-20261013-01-ADD1** — **PASS**
×15 逐条 before/after diff 齐；边界清单三层（核判据／判据实现／测试驱动）分层清楚；hub 接管让渡记录在档；核判据四件哈希锁定。
诚实声明 #1/#2 落在「判据实现层」（包络算法 nextafter→iv 有理除法），**判据语义零改动**成立。
等价性证据=跨环境重放位级一致，且 trunc 残差与 N_B 拒证区间**重置前后逐位相同**——这条是本轮最强的点，直接封死了「实现层漂移渗入语义层」的通道。

---

### 勘误（条件 9）

**C9 ERRATUM-ZETA-INST-01** — **PASS**
独立建档；registry 加 erratum_ref；下游 58 依赖回扫清单齐；唯一源=定案卡 iso100 行锚定成立；winding_2NT=2N(T) 口径字段保留未被顺手改名——这是关键，改名即会污染 58 条回扫。

---

### VERDICT env 面（条件 10–11）

**C10 判定分支 env 硬编码** — **PASS**
分支不可 env 覆盖已在脚本层固化，非文档承诺。

**C11 NS_LIB_DIR 覆盖面披露 + WELD-A-SPEC-01 v2 挂号** — **PASS**
覆盖面已披露；「VERDICT 行与探测目标拒外部 env override」挂号 v2 候选，SPEC 原文不动——挂号而非改写，符合 R1 要求。

---

## 二、三证书重签复核

- 数学工件零改动（括号／包络／绕数值复用已认证数据）：**核过，成立**
- 进程内双跑闸：**在档**
- pytest 40/40：**全绿**

---

## 三、R1 条件总账

| # | 条件 | 结论 |
|---|---|---|
| 1–6 | WIT 层六项 | 全 PASS |
| 8 | 覆写权 ADD1 | PASS |
| 9 | 勘误独立建档 | PASS |
| 10–11 | VERDICT env 面 | 全 PASS |

**11/11 CONDITIONAL → 11/11 PASS（本轮）**

唯一非缺口级观察：C4 的 GAP 支撑集差集清单建议补，作为下游聚合消费者的防御性附件，不影响本轮判定。

---

## 四、R2 残余风险（不构成退回条件）

1. **B1-TB 未解**：status=BLOCKED 是设计保留，非缺陷。retry_budget 耗尽前的窗口期内应保持 KI 存续声明与 registry 同频更新，避免「BLOCKED 被静默读成 UNRESOLVED」。
2. **WELD-A-SPEC-01 v2**：SPEC 原文不动的代价是 v2 落地前该缺口仅在候选档可见。建议 v2 评审前挂一条「候选未落地期间禁引用 SPEC 作为 env 隔离证据」的引用禁令，防止被下游误引。

---

**R2 结论：本轮 11/11 PASS，EXT14 条目可关；B1-TB 作为独立存续项移交下一轮（非本轮退回项）。**

——qtlv SI1语义轨·20261013T114205Z
