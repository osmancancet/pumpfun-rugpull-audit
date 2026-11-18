| tag                        | model           |   pr_auc |   roc_auc |   ece |
|:---------------------------|:----------------|---------:|----------:|------:|
| E2|holdout|rep=none        | lgbm            |    0.671 |     0.826 | 0.021 |
| E2|holdout|rep=none        | logreg          |    0.647 |     0.809 | 0.039 |
| E2|holdout|rep=causal      | lgbm            |    0.755 |     0.866 | 0.013 |
| E2|holdout|rep=causal      | logreg          |    0.697 |     0.838 | 0.041 |
| E2|holdout|rep=vendor      | lgbm            |    0.746 |     0.863 | 0.011 |
| E2|holdout|rep=vendor      | logreg          |    0.684 |     0.831 | 0.050 |
| E2|holdout|rep=oracle      | lgbm            |    0.756 |     0.867 | 0.013 |
| E2|holdout|rep=oracle      | logreg          |    0.699 |     0.839 | 0.043 |
| E2b|holdout|embargo=600s   | rule_rep_e600   |    0.648 |     0.780 | 0.016 |
| E2b|holdout|embargo=600s   | lgbm            |    0.757 |     0.867 | 0.012 |
| E2b|holdout|embargo=86400s | rule_rep_e86400 |    0.595 |     0.750 | 0.025 |
| E2b|holdout|embargo=86400s | lgbm            |    0.750 |     0.864 | 0.014 |