CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-TASK-BEAT171-ANSWER-SELF-CHECK-02-qtlv-20261120.md

应卡: inbox/TASK-BEAT171-ANSWER-SELF-CHECK-02-qtlv-20261120.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 69, "completion_tokens": 1987, "total_tokens": 2056, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 69}

我先说明一点：我无法在本会话内实际执行命令、访问网络或读取你仓库中的真实 commit / run / artifact。因此下面这份回卡**不能**声称包含“真实 run、真实 SHA256、独立重放”的结果——如果我们把它写成那样，就是在伪造证据。下面我按可执行规格给出回卡，其中所有需要真实执行的位置都标记为 **待执行占位**，并给出你（或 CI）可以直接照跑的命令、正负控设计与独立重放流程。你跑完后把输出填入即可成为真实回卡。

---

## outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-qtlv

### 0. 结论（当前状态）
- 真实结构校验器：**规格已给出，待在你的仓库+CI 上执行**
- 语义反例搜索：**规格已给出，至少 1 个反例用例已定义，待执行**
- 固定 commit / 真实 run / artifact SHA256 / 正负控 / 独立重放：**未执行，全部为占位**
- 本回卡**不构成**已完成的 qtlv 线补证；它是可执行补证规格 + 回卡模板

---

### 1. 固定 commit（占位）
```
QT_COMMIT=<40-hex SHA>          # 待填：git rev-parse HEAD
QT_BRANCH=<branch>
QT_TAG=<tag 或 none>
```
约束：补证所用 commit 必须与 artifact 构建 commit 一致；若不一致，需在 §6 说明差异。

---

### 2. 真实结构校验器（规格）

**目的**：对 qtlv 输出做结构级校验（不是语义正确性），确保：
- 帧头/长度/类型字段自洽
- 每个 record 的边界不越界、不重叠、不遗漏
- 尾部 checksum/terminator 存在且位置正确
- 空文件 / 单 record / 最大 record 边界行为确定

**接口（建议）**：
```
qtlv-structcheck --input <artifact.bin> --schema <schema.json> --strict
  exit 0  => 结构合法
  exit 2  => 结构非法（打印 first-failure path）
  exit 3  => 输入不可读/环境错误
```

**必须覆盖的结构断言（正控基线）**：
1. magic 匹配
2. version 在允许集合内
3. record_count 与实际解析数一致
4. 每条 record 的 length 字段 == 实际载荷长度
5. record 偏移单调递增且不重叠
6. 文件末尾 offset == 文件大小（无尾随垃圾）
7. checksum 覆盖范围 = 声明的 record 区间

**负控（必须全部被拒绝，exit 2）**：
- N1：截断最后 1 字节（破坏 terminator/checksum）
- N2：把某 record length 字段 +1（越界）
- N3：把某 record length 字段 -1（重叠/错位）
- N4：翻转 magic 首字节
- N5：在尾部追加 1 字节垃圾
- N6：把 record_count 改成 count+1

正控：**未修改的原始 artifact 必须 exit 0**。

---

### 3. 语义反例搜索（至少 1 个运行）

**目的**：结构合法但语义错误——用来证明结构校验器**不**足以替代语义检查。

**反例 S1（已定义，待执行）**：
- 构造：取原始 artifact，把某条 record 的语义字段（例如 `opcode` 或 `payload.key`）改成另一个**结构合法但语义非法**的值（例如把 `opcode=0x01` 改为 `0x7F`，或把必填 key 置空）。
- 期望：
  - `qtlv-structcheck --strict` → **exit 0**（结构仍合法）
  - 语义校验器（如 `qtlv-semcheck`）→ **exit 非 0**，并定位到该 record
- 这证明：结构校验通过 ≠ 语义正确；补证链条必须同时包含语义层。

**反例搜索运行方式（建议脚本化）**：
```
# 生成 S1
python tools/mutate_semantic.py \
  --in  artifact/qtlv.bin \
  --out artifact/qtlv_S1.bin \
  --record <idx> --field opcode --value 0x7F \
  --keep-structure

# 结构层应通过
qtlv-structcheck --input artifact/qtlv_S1.bin --schema schema.json --strict; echo "struct_exit=$?"
# 语义层应失败
qtlv-semcheck    --input artifact/qtlv_S1.bin --schema schema.json; echo "sem_exit=$?"
```
期望记录：`struct_exit=0` 且 `sem_exit!=0`。

---

### 4. artifact SHA256（占位）
```
ARTIFACT=artifact/qtlv.bin
SHA256=$(sha256sum "$ARTIFACT" | awk '{print $1}')
# 待填：<64-hex>
# 同时记录：
#   - artifact 构建 run URL / ID
#   - schema.json 的 SHA256
#   - 校验器二进制的 SHA256（保证重放一致）
```

---

### 5. 命令（可复现清单）
```bash
set -euo pipefail
git checkout <QT_COMMIT>
git rev-parse HEAD                      # 记录 commit
sha256sum artifact/qtlv.bin             # 记录 artifact hash
sha256sum schema.json                   # 记录 schema hash
sha256sum "$(command -v qtlv-structcheck)"  # 记录校验器 hash

# 正控
qtlv-structcheck --input artifact/qtlv.bin --schema schema.json --strict
echo "POS_EXIT=$?"

# 负控 N1..N6（逐个生成并断言 exit 2）
for n in N1 N2 N3 N4 N5 N6; do
  python tools/mutate_struct.py --case $n --in artifact/qtlv.bin --out /tmp/qtlv_$n.bin
  set +e; qtlv-structcheck --input /tmp/qtlv_$n.bin --schema schema.json --strict
  code=$?; set -e
  [ "$code" -eq 2 ] || { echo "NEG CONTROL FAIL: $n exit=$code"; exit 1; }
done

# 语义反例 S1
python tools/mutate_semantic.py --in artifact/qtlv.bin --out /tmp/qtlv_S1.bin \
  --record <idx> --field opcode --value 0x7F --keep-structure
set +e
qtlv-structcheck --input /tmp/qtlv_S1.bin --schema schema.json --strict; s=$?
qtlv-semcheck    --input /tmp/qtlv_S1.bin --schema schema.json;         m=$?
set -e
echo "S1 struct_exit=$s sem_exit=$m"   # 期望 0 与非 0
```

---

### 6. 独立重放（流程）
1. 在**干净容器/干净 clone** 中 `git checkout <QT_COMMIT>`。
2. 用记录的校验器二进制 SHA256 校验工具本体未被替换。
3. 重跑 §5 全部命令。
4. 断言：
   - artifact SHA256 与 §4 一致
   - 正控 exit 0
   - N1–N6 全部 exit 2
   - S1 结构 exit 0 / 语义 非0
5. 输出重放日志 SHA256 与本次 run ID。
   - 若与首轮任何一项不一致 → 判定补证失败，需在 §7 记录差异。

---

### 7. 已知限制 / 待填清单
- [ ] QT_COMMIT 未填
- [ ] 真实 run ID / URL 未填
- [ ] artifact SHA256 未填
- [ ] schema SHA256 未填
- [ ] 校验器二进制 SHA256 未填
- [ ] 正控 & N1–N6 实际 exit code 未填
- [ ] S1 实际 `struct_exit` / `sem_exit` 未填
- [ ] 独立重放日志 SHA256 未填

---

### 8. 声明
本回卡为**可执行补证规格 + 回卡模板**，不包含任何伪造的真实 run / SHA256 / 重放结果。待你在固定 commit 上执行 §5 并回填 §1/§4/§7 后，本卡才升级为真实 qtlv 线补证回卡。若需要，我可以下一步把 `qtlv-structcheck` / `mutate_struct.py` / `mutate_semantic.py` 的参考实现写成代码，供你直接落到仓库里跑。

——qtlv SI1语义轨·20261120T051930Z
