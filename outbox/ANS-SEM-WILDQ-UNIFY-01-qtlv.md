CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-UNIFY-01-qtlv.md

应卡: inbox/WILDQ-UNIFY-01-qtlv.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 435, "completion_tokens": 990, "total_tokens": 1425, "prompt_tokens_details": {"cached_tokens": 256}, "prompt_cache_hit_tokens": 256, "prompt_cache_miss_tokens": 179}

A) 最深映射：**共性4「刚性等号即分类」**。

机制级对应（非比喻）：

- 贵线机制里，**单调量取等号 ⇒ 结构塌缩为极简类**，这和 OT 里「单调性公式取常数 ⇒ 爆破极限是锥+齐次」是同一台机器。
- 具体到联邦映射草案：
  - `级名不滥` = 单调量等号刚性。  
    即：如果一个量在允许变换下不变且单调，那么它取临界常数时，系统不能再“分级”，只能落入唯一正则类。对应 OT：等号成立时，弱同构/锥齐次性被迫成立。
  - `fp互锚` = 距离0 ⇒ 弱同构。  
    即：两个对象在耦合空间中的最优距离为0，不是“很像”，而是结构等价类相同。对应 OT：Wasserstein距离为0 ⇔ 测度同分布；在富化超图情形下 ⇔ 弱同构。
  - `fail-closed` = 凸性假设。  
    凸性不是技术便利，而是保证“等号刚性”可判定的底座：凸泛函 + 线性约束 ⇒ 对偶无间隙 ⇒ 等号条件可分类。
- 为什么这条最深：  
  贵线其它机制大多在“构造耦合/松弛/熵惩罚”，而**刚性等号**是最终判定层。没有它，耦合空间再富、熵惩罚再唯一，也无法把“最优”转成“分类”。这正是 OT 三文共有的元套路：先证单调性/对偶等号，再由等号反推结构。

B) 可操作可判定的「耦合/统一」实验：

**对象**  
取两条贵线候选统一机制 \(M_1, M_2\)，各自诱导一个边缘约束下的联合可行集：
\[
\Pi(\mu_1,\mu_2)=\{\pi: \text{边缘分别为 }\mu_1,\mu_2\}
\]
再取一个代价泛函 \(C(\pi)\)，例如：
\[
C(\pi)=\int c\,d\pi+\lambda\,\mathrm{Ent}(\pi)
\]
其中 \(\mathrm{Ent}\) 是相对熵，\(\lambda>0\)。

**代价泛函**  
定义耦合代价：
\[
\mathrm{OT}_\lambda(\mu_1,\mu_2)=\inf_{\pi\in\Pi(\mu_1,\mu_2)} C(\pi)
\]
若贵线有自家距离/损失 \(d_{\text{line}}\)，则做加权：
\[
F=\mathrm{OT}_\lambda(\mu_1,\mu_2)+\alpha d_{\text{line}}(M_1,M_2)
\]

**判定谓词**  
判定统一是否成立：
\[
P:\quad \mathrm{OT}_\lambda(\mu_1,\mu_2)=0
\]
且最优耦合 \(\pi^\*\) 满足：
\[
\pi^\*=\mu_1\otimes\mu_2 \quad\text{或}\quad \pi^\*\text{ 是确定性排列/等距图}
\]
若 \(P\) 成立，则 \(M_1,M_2\) 在该耦合意义下弱同构。

**预期刚性等号**  
- 当 \(\lambda\to 0\)：退化为经典 OT，等号 ⇒ 两个边缘可经保测变换匹配。  
- 当 \(\lambda>0\)：熵惩罚使最优耦合唯一；若代价为0，则唯一耦合必为乘积或排列，对应“距离0 ⇒ 弱同构”。  
- 若加入凸性约束 \(M_i\in\mathcal{C}\)（凸集），则对偶等号条件给出：  
  \[
  \text{等号成立} \iff \text{存在共同势函数 } \phi \text{ 使两边同步}
  \]
  这就是“级名不滥”的机制版：一旦等号，分类层级塌缩为单一正则类。

**可判定操作**  
1. 固定 \(\mu_1,\mu_2\) 的有限样本。  
2. 解熵正则 OT，得 \(\mathrm{OT}_\lambda\) 和 \(\pi^\*\)。  
3. 检查 \(\mathrm{OT}_\lambda<\epsilon\) 且 \(\pi^\*\) 的支撑是否集中在排列/等距图上。  
4. 若成立，则判定两机制在该耦合下统一；否则不统一。  
5. 改变 \(\lambda\)，观察等号是否稳定；稳定则刚性成立。

——qtlv SI1语义轨·20261007T144344Z
