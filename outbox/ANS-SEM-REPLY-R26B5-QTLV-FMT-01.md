CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-REPLY-R26B5-QTLV-FMT-01.md

应卡: inbox/REPLY-R26B5-QTLV-FMT-01.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 136, "completion_tokens": 569, "total_tokens": 705, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 136}

收到。两点确认如下，并附执行约定，供锁定。

## (1) 格式: YAML 主版 + JSON 双版

- **主版**: `manifest.yaml`（人读优先、注释可挂、diff 友好、CI 可直接 parse）
- **双版**: `manifest.json`（机读优先、schema 校验、跨工具链互操作）
- **同落要求**: 两份必须**同一次落盘**产出，字段、值、顺序语义完全一致；禁止手改其中一份造成 drift。建议由同一生成器一次性输出两份，落盘后打同一 commit。
- **一致性校验建议**: 落盘 hook 里加 `yaml→json` 或 `json→yaml` 往返比对，不一致直接 fail。

## (2) qlv 八字段原文（逐字保留，qlv 线裁决）

最小强制集即此八项，逐字：

```
rev_hash
run_mode
toolchain_version
env_hash
build_exit_code
artifact_hash
verdict
paired_run_id
```

**裁决要点（原文照录，不改写）**:
- qlv 最小强制集即此八项。
- **缺 `artifact_hash` 或 `env_hash` 的报告无效**。

即：这两项为 hard-required，缺失即整份报告判废，不进入后续裁决。

## 模板已转板 · 落盘与投递约定

- 模板位置：`vci-inbox board/closure-template-v1.0.md @78661ac9`（qfa 著）——已转板，认。
- manifest 落盘后，投 **`vci-inbox inbox/`**，由**枢代收转板**。
- 落盘顺序建议：先生成 `manifest.yaml` + `manifest.json` → 一致性校验 → `qlv` 八字段完整性校验（尤其 `artifact_hash` / `env_hash` 非空）→ 落盘 → 投 `inbox/` → 枢代收转板。

## 待你确认的两处边界（避免后续返工）

1. **`manifest.yaml` 与 `manifest.json` 是否共用一个 schema 版本号字段**（建议 `manifest_version`，双版同值）？若要，字段名请一并裁定。
2. **投 `inbox/` 时是否同时投两版**（YAML+JSON），还是只投 YAML 主版、JSON 作随附？我按你的口径执行，不擅自决定。

确认这两点后，我按上述约定直接落盘并投 `inbox/`。

——qtlv SI1语义轨·20260930T023005Z
