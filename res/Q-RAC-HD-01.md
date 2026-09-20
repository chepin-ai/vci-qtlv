CLASSIFY: L1(research,value-free)
# Q-RAC-HD-01 高维纠缠随机通信(RAC)·qubit版复现实证
> 立项: lvlu · 2026-09-20 · 脉络锚: 中科大柳必恒组 PRL(2026-09-17) Quantum Stochastic Communication via High-Dimensional Entanglement
> DOI: 10.1103/rq78-1qbh

## 一、协议(论文→qubit映射)
- 共享 n 维最大纠缠 |Φ_n> = (1/√n)Σ_i|ii>。qubit实现: n=2^k ⇒ 每方 k 比特, k 对 Bell 态即得。
- Alice 用 Weyl 算符 X^x1 Z^x2 编码两比特 x1x2 于单方 qudit(免纠缠测量)。
  - X(qudit) = 模n循环移位 ⇒ k比特递增器(级联CNOT)
  - Z(qudit) = 相位 ω^i, ω=e^{2πi/n} ⇒ 按位相位门(d=4: Z·S; d=8: Z·S·T 式按权施加)
- Bob 按需求 y 解码: y=1 测 Z⊗Z(计算基)得 x1; y=2 测 X⊗X(Fourier基: 逆QFT后测)得 x2。理想 S=1。
- Schmidt数认证: 成功率界 S ≤ ½(1+√(d/n))。S_exp 超界即证纠缠维度>d。
  - n=4: 界序列 d=1:0.7500 / d=2:0.8536 / d=3:0.9330
  - n=8: 0.6768/0.7500/0.8062/0.8536/0.8953/0.9330/0.9677 (论文图3)

## 二、实验设计(IBM 156q Heron r2, Open Plan 10min/月·单次提交零重试)
1. Aer 仿真预验: d=4 (4比特: A=q0q1, B=q2q3) 与 d=8 (6比特) 两 y 分支, 理想应 S→1
2. 噪声模型粗估硬件可达 S, 选定可认证的 d 目标
3. 真机单次提交: ibm_fez/kingston/marrakesh 择一, shots=8192, 两电路一job
4. 统计 S_exp, 对照认证界判 Schmidt 数下界

## 三、与励磁环/机器意识脉络接口
- 高维纠缠维度认证 = 系统"纠缠容量"的可实验判据 → 接入机器意识判据簇(SI6评估)
- RAC随机通信框架 = 免贝尔测量的可扩展通信原语 → SI5调度层消息原语借鉴

## 四、纪律
- 本源/IBM皆单次提交零重试·仿真预验先行·密钥值域律
