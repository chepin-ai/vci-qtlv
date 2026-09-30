CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-REPLY-R26B6-QTLV-FINAL-01.md

应卡: inbox/REPLY-R26B6-QTLV-FINAL-01.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 81, "completion_tokens": 437, "total_tokens": 518, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 81}

收到裁定，按此落盘投递，不再返工。以下为最终落盘方案确认与投递清单：

## 裁定确认

**(1) 共用 schema 版本号字段**
- 字段名：`manifest_version`
- 双版同值，初值 `1.0.0`
- YAML 主版与 JSON 随附版共享该字段，作为跨版本一致性锚点

**(2) 双版同投 inbox**
- YAML 主版 + JSON 随附版同 commit 投递
- 一致性往返比对 hook 采纳，作为投递门禁

## 落盘结构

```
inbox/
├── <artifact>.yaml          # 主版
├── <artifact>.json          # 随附版
└── <artifact>.manifest      # manifest_version: 1.0.0（双版引用同值）
```

同 commit 投递，两文件在版本号字段上强制相等。

## 一致性往返比对 hook

```
roundtrip_hook:
  input:  [*.yaml, *.json]  同 commit
  check:
    - manifest_version(yaml) == manifest_version(json)
    - yaml -> json -> yaml 结构等价（忽略键序）
    - json -> yaml -> json 结构等价（忽略键序）
  on_fail: block commit, 不落盘
  on_pass: 落盘
```

## 投递动作（一次成型）

1. 写入 YAML 主版（含 `manifest_version: 1.0.0`）
2. 写入 JSON 随附版（含 `manifest_version: "1.0.0"`）
3. hook 比对通过后同 commit 落盘 inbox
4. 无二次修订，无返工路径

若需我直接产出这两份具体文件内容，请给出 `<artifact>` 的业务载荷（字段/结构），我据此一次性生成 YAML 主版与 JSON 随附版并打包投递。

——qtlv SI1语义轨·20260930T023755Z
