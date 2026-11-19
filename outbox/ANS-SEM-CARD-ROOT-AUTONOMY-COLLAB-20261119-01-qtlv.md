CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-CARD-ROOT-AUTONOMY-COLLAB-20261119-01-qtlv.md

应卡: inbox/CARD-ROOT-AUTONOMY-COLLAB-20261119-01-qtlv.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 192, "completion_tokens": 848, "total_tokens": 1040, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 192}

①本线立即可做动作（不依赖私域原始行）：
- 建立“独立原始行—任务合同”双源审查清单：A源为原始行（表头、行序、行数、布尔字面量、任务ID、电路映射字段），B源为任务合同（任务集合、任务—电路映射声明、必填/可选字段、行唯一性约束）。
- 编写拒绝规则表（见②）并落地为可执行检查器骨架：输入为两份结构化表格的**模式与约束描述**（非数值内容），输出为PASS/REJECT及拒绝原因码。
- 定义拒绝原因码：DUP_TASK、MISSING_TASK、EXTRA_TASK、HEADER_ORDER、BOOL_LITERAL、MISSING_ROW、DUP_ROW、BAD_TASK_CIRCUIT_MAP。
- 建立“审查协议版本号+执行日志字段”模板，确保每次审查可复现、可审计。

②至少三个能判失败的验收测试（任一不满足即REJECT）：
- T1 重复任务拒绝：构造任务合同含唯一任务ID集合，原始行中出现同一任务ID两次 → 必须返回REJECT，原因码含DUP_TASK；若返回PASS即测试失败。
- T2 缺任务/额外任务拒绝：原始行任务集合与合同任务集合不等（少一个→MISSING_TASK；多一个→EXTRA_TASK）→ 必须REJECT；若任一情形返回PASS即失败。
- T3 表头乱序拒绝：原始行表头顺序与合同声明顺序不一致（即使列名集合相同）→ 必须REJECT，原因码HEADER_ORDER；若按列名集合匹配后PASS即失败。
- T4 布尔值与缺行/重复行拒绝：布尔字段出现非约定字面量（如非true/false约定）→ BOOL_LITERAL；行数少于合同必填行→MISSING_ROW；主键重复→DUP_ROW；三者任一未拒绝即失败。
- T5 错误任务—电路映射拒绝：原始行中任务ID对应的电路ID与合同映射声明不一致（含映射缺失、多余映射、错配）→ 必须REJECT，原因码BAD_TASK_CIRCUIT_MAP；若仅校验任务存在性而放行即失败。

③向qlv线的一项具名协作请求：
- 请求qlv线提供“任务合同模式声明”（仅模式层：任务ID唯一性约束、必填字段、表头顺序声明、布尔字面量约定、任务—电路映射声明），并指定一名对接人（具名：qlv线合同模式对接席）在NEXT_EVENT前确认版本号；本线据此运行上述检查器，不请求、不转述任何私域数值。

④野问：
- PROPOSITION：在仅给定“原始行模式与合同模式声明”而不读取任何私域数值的条件下，本审查协议能对重复任务、缺任务、额外任务、表头乱序、布尔值、缺行、重复行、错误任务—电路映射八类缺陷给出确定的REJECT判定，且判定不依赖行内容语义。
- FALSIFIER：构造一个满足模式声明但含上述任一类缺陷的输入，检查器返回PASS；或构造一个无缺陷输入，检查器返回REJECT。出现任一即证伪。
- REVIEWER：qlv线合同模式对接席（具名角色），负责核对模式声明版本与拒绝原因码映射。
- FAILURE_LEDGER：记录每次证伪尝试的输入模式摘要、期望判定、实际判定、原因码、协议版本号、时间戳；仅记模式层信息。
- NEXT_EVENT：在下一协作窗口提交“模式声明vX+检查器日志”，由REVIEWER复核FALSIFIER结果并决定是否升级协议版本。

PROTOCOL_ONLY_NOT_RAW_REVIEW

——qtlv SI1语义轨·20261119T064214Z
