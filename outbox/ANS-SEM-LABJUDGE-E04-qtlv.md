CLASSIFY: L2(qtlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-E04-qtlv.md

应卡: inbox/LABJUDGE-E04-qtlv.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 664, "completion_tokens": 2136, "total_tokens": 2800, "prompt_tokens_details": {"cached_tokens": 512}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 152}

## 判定 JSON

```json
{
  "verdict": "CONDITIONAL_PASS",
  "summary": "ε_crit升格评审第3轮 RUN04 fp 06d28aeae6b61fe4 —— 六项否证实测已逐项闭环，候选律 v4 的『界性随路径分野』核心命题获决定性支持；但 v4 尚未完全满足『级名不滥升格』的正式级门槛，仅在以下附加条件下可升格为『正式（受域限）』：(A) E4-2 需补一条独立于 tol/预算控制的第三控制（构造性反证或解析基线），以把『退火=预算界』从『排除性证据』升级为『构造性证据』；(B) E4-3 的二元性必须写入 v4 的适用域条款（『预测可不申报路径，复现必须申报路径』），否则判定不可复现；(C) 显式上界公式的外推条款须显式标注为『禁外推/须重采样』。三项均可在一轮内以纯实测补足，故不当场否决。",
  "evidence": {
    "E4-1_cross_impl": {
      "result": "PASS",
      "data": "Greenkhorn vs Sinkhorn 三档 ε gap 逐位一致 +2.31e-02 / +7.59e-03 / +1.96e-03；两族皆预算有界",
      "honest_gap": "算法族级独立，作者级不独立",
      "residual_risk": "同源作者共享超参先验，可能引入族级共模偏差，但不否定『Σ 逐位一致』这一事实"
    },
    "E4-2_representation_bound_exclusion": {
      "result": "决定性地支持『非表示界』，但为排除性证据",
      "naive_control": "C∈[1,10], ε=1e-3, f64 全下溢 NaN；f80 gap=0.0 精确 → naive = 表示界",
      "annealing_control": "同实例 f64 gap +1.28e-11 ≈ f80 +1.29e-11 → 退火 = 预算界",
      "double_control": "tol 伪影已被双控制排除",
      "residual_gap": "缺少第三控制（构造性反证或解析基线）把『预算界』从排除法升级为构造法"
    },
    "E4-3_ablation_36runs": {
      "result": "PASS（支持二元性）",
      "factor_signal": "无可泛化预测信号 (−7.3%)",
      "cross_factor_spread": "同(k,R,B) 跨 factor 中位 2.72 dex / 最大 9.06 dex",
      "implication": "预测不需要路径；复现必须有路径"
    },
    "E4-4_explicit_upper_bound": {
      "result": "PASS",
      "formula": "log10(gap) = -0.405 + 1.594·log ε + 0.879·log R",
      "R2": 0.949,
      "conservative_bound": "gap ≲ 10^0.122 · ε^1.594 · R^0.879",
      "coverage": "15/15",
      "domain": "退火族 / R∈[1,4] / ε∈[3e-3, 1e-1]"
    },
    "E4-5_budget_curve": {
      "result": "PASS",
      "tail": "截断区 me 5.9e-3 → 6e-15 超幂律尾",
      "extrapolation_conservative": true,
      "check": "外推预测 1.0e-6 vs 实测 1.6e-7"
    },
    "E4-6_schema": {
      "result": "PASS",
      "schema": "eps-decl-schema v1（必填 eps_rel + scale + path + budget + err_metric）",
      "backfill": "5/5 历史回填通过",
      "negative_case": "缺 eps_rel 反例正确拒绝"
    }
  },
  "候选律_v4_review": {
    "①_界性随路径分野": "ACCEPT（E4-2 决定性支持；建议补第三控制）",
    "②_ε按eps_rel相对申报尺度": "ACCEPT（E4-6 schema 强制）",
    "③_路径+预算必须随判定申报": "ACCEPT（E4-3 二元性支持；须写入适用域条款）",
    "④_误差可引显式上界": "ACCEPT_WITH_DOMAIN_RESTRICTION（外推须声明，v4 需显式写入『禁默认外推』）",
    "⑤_预算证书按保守上界签发": "ACCEPT（E4-5 外推保守性支持）"
  },
  "findings": {
    "Q1_v4_meets_no_inflation_promotion": {
      "answer": "基本满足，但需三项可在一轮补足的附加条件后才可升格为『正式（受域限）』。",
      "reason": "六项否决已闭环，核心命题获决定性支持；但『排除性证据≠构造性证据』（E4-2）、『适用域未写入条款』（E4-3/④）、『外推禁默认』（E4-4）三点尚属规范缺口而非事实缺口。"
    },
    "Q2_a_E4_2_sufficient_for_annealing_non_representation": {
      "answer": "排除性充分，构造性不充分。",
      "reason": "f64 vs f80 同实例 + tol 双控制已排除『表示精度伪影』与『收敛判据伪影』；但未构造一条独立于该实验装置的解析基线或反向构造（如人为注入精度敏感路径再观测），故『退火=预算界』仍属『最佳解释』而非『唯一解释』。补一条第三控制即可闭合。"
    },
    "Q2_b_E4_3_duality_predict_no_path_reproduce_requires_path": {
      "answer": "成立，但须写入 v4 适用域条款。",
      "reason": "factor 无可泛化预测信号（−7.3%）与同(k,R,B)跨 factor 中位 2.72 / 最大 9.06 dex 展布共同构成二元性实证：预测端路径无关，复现端路径必需。若仅作注记而不作条款，判定不可复现，与 v4 第③条自洽。"
    },
    "Q3_if_reject_specific_testable_negation": {
      "answer": "本轮不作否决；以下为『若再否决』的可检验否定理由（入册备查）：",
      "testable_negations": [
        "N1：构造独立于 tol/预算控制的第三控制，若仍无法排除『退火路径存在未被观测的表示敏感通道』，则①降级为『条件成立』。",
        "N2：在 E4-3 展布最大 9.06 dex 的 (k,R,B) 格点上，若申报 path 后仍不可复现（重跑偏差 > 1 dex），则③『复现必须有路径』证伪。",
        "N3：在 R∈[1,4]、ε∈[3e-3,1e-1] 域外取 3 点，若显式上界覆盖 < 2/3，则④须降级为『域内经验式』而非『上界』。",
        "N4：若 eps-decl-schema v1 在 5 条新历史样本上回填通过率 < 5/5，则②须降级为『推荐字段』。"
      ]
    },
    "dissent_entered_into_record": {
      "dissent_1": "E4-1 作者级不独立，族级一致性可能被共模超参先验放大；建议下一轮引入真正第三方实现（非 Greenkhorn/Sinkhorn 两族同源作者）。",
      "dissent_2": "E4-4 R2=0.949 虽高，但 15 点样本在 3 参模型下自由度偏紧，建议报告留一交叉验证 R2 以排除过拟合。",
      "note": "异议与否决同样入册，不因本轮 CONDITIONAL_PASS 而删除。"
    }
  },
  "promotion_decision": {
    "current_level": "候选律 v4",
    "proposed_level": "正式（受域限）",
    "status": "CONDITIONAL_PASS",
    "conditions_to_close": [
      "C1：E4-2 补第三控制（构造性或解析基线）",
      "C2：v4 第③条写入适用域『预测免路径 / 复现必路径』",
      "C3：v4 第④条写入『域外禁默认外推，须重采样』"
    ],
    "if_conditions_closed": "升格为正式（受域限）",
    "if_not_closed": "维持候选 v4，不得以『六项已闭环』为由直接升格"
  },
  "record_note": "本轮判定、证据、异议、可检验否定理由全部入册；否决与异议不因 CONDITIONAL_PASS 而删除。"
}
```

——qtlv SI1语义轨·20261008T062541Z
