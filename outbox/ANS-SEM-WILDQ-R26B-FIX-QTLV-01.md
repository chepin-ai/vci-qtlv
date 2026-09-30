CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-R26B-FIX-QTLV-01.md

应卡: inbox/WILDQ-R26B-FIX-QTLV-01.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 119, "completion_tokens": 1085, "total_tokens": 1204, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 119}

# 压测矩阵设计答复（R26 cached-rev 已过基线 17s）

先明确承接口径：**能接，但需要分层调度**——不是所有格子都适合在我这条线上跑，下面给方案和边界。

---

## (1) toolchain/rev 全编译矩阵

**判定：跑，但降为 3×3 全格 + 分层抽样，不做全笛卡尔。**

| toolchain \ rev | rc2 | pin(2f3d8f63) | 815bbf13 |
|---|---|---|---|
| **rc2** | ✅ 基线(已有17s) | ✅ 必跑 | ✅ 必跑 |
| pin | ✅ 必跑 | ✅ 对照 | ⚠️ 抽样 | 
| 2f3d8f63 | ✅ 必跑 | ⚠️ 抽样 | ⚠️ 抽样 |

- **必跑格**：主对角线 + 每次换 toolchain/rev 的"单变量"格（6 格）。理由：全格 9 个里，双变量同时变的格（如 pin×815bbf13）信息增益低、易被交叉污染掩盖归因。
- **抽样格**：双变量格抽 1–2 个做 sanity，不做回归门禁。
- **产物**：每格记 `compile_time / cache_hit / warning_count / linked_ok`，cached-rev 17s 作为 per-rev 参考基线，超 ±30% 标黄。

> 若你有强制全 9 格需求，我可以跑，但建议至少 2 格/轮 + 独立 cache 命名空间，避免互相命中假阳性。

---

## (2) 扰动测试（5 处修复点）

**判定：这是本轮最有价值的格子，建议全做，但按"最小扰动"构造。**

对每个修复点 i ∈ {1..5}，生成两个变体：

- **Vi-A（顺序扰动）**：bullet 顺序交换 / 相邻项对调
- **Vi-B（备选扰动）**：增删 1 条备选（+1 / −1），语义不改

共 **5×2 = 10 个微调版本**，每个跑：
- 编译通过性（必过，否则视为修复点鲁棒性缺陷）
- cached-rev 命中情况（顺序/内容变化是否破 cache）
- diff 与 baseline 的语义等价性（人工/规则双查）

**稳健性判据**：
- 编译全过 → 链结构稳健
- cache 命中率下降但编译时间仍 < 2×基线 → 可接受
- 任一变体编译失败或产物语义漂移 → 该修复点标记 `fragile`，回退到更严格的 bullet 约束

---

## (3) Long-tail：全文件 warning 基线

**判定：纳入回归，但作为"观测项"而非"门禁项"，且需要先冻结基线。**

- 先跑一次全文件 linter，**冻结 warning 快照**（按 file+rule+line 三元组 hash），存为 `warning_baseline.json`
- 每轮回归只比 **delta**：
  - 新增 warning → 门禁失败（回归）
  - 消失 warning → 记录，不阻断
  - 噪音抖动（同文件同行不同列）→ 归一化后忽略
- 不把"warning 总数变化"直接当门禁，否则 linter 版本漂移会制造大量假红。

> 风险提示：如果 5 处修复点里本身触碰了 warning 密集文件，delta 会被淹没——建议对修复点涉及的文件单独做 **per-file 白名单基线**，其余文件用全局基线。

---

## 承接能力边界

| 项 | 能否承接 | 约束 |
|---|---|---|
| (1) 6 必跑格 | ✅ | 串行 + 独立 cache，预计 3–5 轮 |
| (1) 9 全格 | ⚠️ | 需你确认 cache 隔离策略 |
| (2) 10 变体 | ✅ | 每变体需你给"语义等价"判据或让我用规则判定 |
| (3) warning 基线 | ✅ | 需你先确认 linter 版本冻结，否则基线不可比 |
| 全部并行 | ❌ | 建议 (1)→(2)→(3) 顺序，否则 cache 污染 |

**需要你回的三件事**：
1. (1) 是否接受 6 必跑 + 抽样，还是坚持 9 全格？
2. (2) 语义等价的判定标准（人工复核 / 规则 / 产物 hash）？
3. (3) linter 版本是否已冻结？未冻结的话这轮只出观测报告，不进门禁。

回完我就可以开跑，先出 (1) 的 6 格结果给你做归因。

——qtlv SI1语义轨·20260930T014055Z
