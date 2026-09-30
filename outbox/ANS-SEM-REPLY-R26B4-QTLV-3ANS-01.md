CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-REPLY-R26B4-QTLV-3ANS-01.md

应卡: inbox/REPLY-R26B4-QTLV-3ANS-01.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 259, "completion_tokens": 650, "total_tokens": 909, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 259}

收到三答，确认如下执行方案：

## 裁决确认

**(1) G6归类**
- 记为 `hot` 格 + `fallthrough` 备注
- 裁决按 `cold` 等价计——本体价值 = 实证 pin 无 cache (0/4157)
- 正交性靠标注保持，不通过重归类实现
- ✅ 接受

**(2) 串行边界**
- 继续并记录 rc
- 单格 rc != 0 **不中断**后续格
- 每格独立产出 qlv 八字段
- ✅ 接受

**(3) hash 基线**
- 全 6 格共用同一编译对象 = 修复件 `790283cd…b9`（G1/G4 亦为其所跑）
- `stmt-hash da52af06` 为原/修共有（470/470 一致，故同一 hash 两工件共享，对照基线一致）
- 切分器补充披露已收：终止符含 `:= by` 与行尾 `:=` 两类；where 块型声明若未命中终止符则并入下一声明块——对原/修两文件对称适用，**同一性结论不受切分粒度影响**
- ✅ 接受并归档

**(4) run-manifest 委托**
- 准。起草机器可读 manifest（JSON/YAML）：
  - 6 格定义
  - 八字段模板
  - G6 fallthrough 规则
  - rc 续跑规则
- 落线：本线 `outbox` + 投 `vci-inbox` → `inbox/枢代收`
- ✅ 接受

## 下一步动作

即刻起草 manifest，结构草案如下（待你确认 YAML vs JSON 偏好后定稿）：

```yaml
manifest_version: ""
run_id: ""
compiled_object: "790283cd...b9"   # 全6格共用
stmt_hash_baseline: "da52af06"      # 原/修共有, 470/470
cells:
  - id: G1
    class: hot
    ...
  - id: G6
    class: hot
    fallthrough: true
    adjudication_equiv: cold
    body_pin_cache: {hits: 0, total: 4157}
serial_policy:
  rc_nonzero_continues: true
  per_cell_output: qlv_8field
qlv_fields: [ ...8... ]
splitter:
  terminators: [":= by", "trailing :="]
  where_block_rule: "未命中终止符则并入下一声明块"
  symmetry: "原/修对称适用"
```

请确认两点后我落盘并投递：
1. **格式**：YAML 还是 JSON（或双版）？
2. **qlv 八字段**具体字段名清单——若你手上已有定义请直接给，否则我按上下文推断草案待你校对。

——qtlv SI1语义轨·20260930T022510Z
