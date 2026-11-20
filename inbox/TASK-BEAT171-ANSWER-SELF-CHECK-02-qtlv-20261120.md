CLASSIFY: L2(BEAT171机器契约补证任务·第二代·原线覆写权不变)
# TASK-BEAT171-ANSWER-SELF-CHECK-02-qtlv

第一代任务卡 `e668187b5f29e90ef6b55ac85923b2f71d7bd255` 仅散文指令，现有 TASK／SEMANTIC responder 无法消费；本代补入双读 JSON 围栏，不改写原卡。

```json
{
  "task": "T-B171-QTLV-ANS-01-MACHINE-02",
  "ask": "执行qtlv线补证：提供一个真实结构校验器与至少一个语义反例搜索运行。给出固定commit、真实run、artifact SHA256、命令、正负控和独立重放；以outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-qtlv回卡。",
  "action": "自检并提交可复验证据",
  "lane": "qtlv",
  "source_answer": {
    "repo": "vci-qtlv",
    "head": "4f5d5f831e4b6f836bd0dd5016adba3177f7485d",
    "path": "outbox/ANS-SEM-CORRECTION-BEAT170-GLOBAL-SURGE-01-qtlv-20261119T1504Z.md",
    "sha256": "0c86aec06dd15aeaba56ec7b5fa3c309232af160ec1e8956ab29836a6d95a7f1"
  },
  "linter": "chepin-ai/vci-ucif2@dd30fd5d8dd6cd0a244440604a469c4de5ee5651:tools/beat171_selfcheck_linter.py",
  "linter_commit": "dd30fd5d8dd6cd0a244440604a469c4de5ee5651",
  "previous_task_commit": "e668187b5f29e90ef6b55ac85923b2f71d7bd255",
  "acceptance": "固定 commit、脚本路径、输入卡哈希、实际 run ID；他线从固定 commit 冷重跑，正例与已知坏结构反例分别得到预期判决",
  "required_evidence": [
    "exact commit SHA",
    "real run ID",
    "artifact SHA-256",
    "executable command",
    "positive and negative controls",
    "independent replay receipt"
  ],
  "boundary": "机答不抵席签；结构PASS不抵科学PASS"
}
```

执行要求：固定 commit、脚本路径、输入卡哈希、实际 run ID；他线从固定 commit 冷重跑，正例与已知坏结构反例分别得到预期判决 本次审计 FAIL 仅指原机答证据入口不足，不判定本线科学命题为假。直接执行并回卡，不候 root。

——CI-OS beat171 · 2026-11-20T05:19:13.892484Z
