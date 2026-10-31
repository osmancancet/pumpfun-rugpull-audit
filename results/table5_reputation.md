| tag                        | model           |   pr_auc |   roc_auc |   ece |
|:---------------------------|:----------------|---------:|----------:|------:|
| E2|holdout|rep=none        | lgbm            |    0.925 |     0.881 | 0.015 |
| E2|holdout|rep=none        | logreg          |    0.903 |     0.853 | 0.072 |
| E2|holdout|rep=causal      | lgbm            |    0.953 |     0.919 | 0.006 |
| E2|holdout|rep=causal      | logreg          |    0.931 |     0.891 | 0.025 |
| E2|holdout|rep=vendor      | lgbm            |    0.951 |     0.916 | 0.008 |
| E2|holdout|rep=vendor      | logreg          |    0.926 |     0.884 | 0.033 |
| E2|holdout|rep=oracle      | lgbm            |    0.954 |     0.920 | 0.007 |
| E2|holdout|rep=oracle      | logreg          |    0.931 |     0.892 | 0.027 |
| E2b|holdout|embargo=600s   | rule_rep_e600   |    0.909 |     0.852 | 0.005 |
| E2b|holdout|embargo=600s   | lgbm            |    0.954 |     0.920 | 0.006 |
| E2b|holdout|embargo=86400s | rule_rep_e86400 |    0.871 |     0.806 | 0.022 |
| E2b|holdout|embargo=86400s | lgbm            |    0.952 |     0.918 | 0.007 |