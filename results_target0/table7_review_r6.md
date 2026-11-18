| Analysis | n (test) | Prevalence | PR-AUC [95% CI] | ROC-AUC [95% CI] |
|---|---|---|---|---|
| Lead time: rugs ≥ 30 s after the snapshot vs all non-rugs | 38,789 | 0.499 | 0.861 [0.845, 0.876] | 0.886 [0.873, 0.898] |
| Lead time: rugs ≥ 60 s after the snapshot vs all non-rugs | 31,142 | 0.376 | 0.746 [0.719, 0.769] | 0.865 [0.850, 0.878] |
| Peak reserves ≥ 1 SOL | 29,740 | 0.848 | 0.956 [0.950, 0.962] | 0.819 [0.806, 0.831] |
| Peak reserves ≥ 5 SOL | 16,700 | 0.875 | 0.955 [0.948, 0.960] | 0.780 [0.764, 0.794] |
| P1 test, creator seen in P1 training | 142,857 | 0.699 | 0.966 [0.962, 0.970] | 0.935 [0.928, 0.941] |
| P1 test, creator unseen in P1 training | 42,091 | 0.577 | 0.898 [0.894, 0.902] | 0.895 [0.892, 0.898] |
| P3 hold-out, creator seen in training | 31,810 | 0.778 | 0.967 [0.960, 0.973] | 0.914 [0.895, 0.929] |
| P3 hold-out, creator unseen (= P4) | 30,030 | 0.588 | 0.923 [0.909, 0.934] | 0.911 [0.898, 0.923] |
| Classic launches only, P1 | 127,380 | 0.573 | 0.935 [0.931, 0.940] | 0.929 [0.923, 0.934] |
| Classic launches only, P4 hold-out | 22,976 | 0.517 | 0.909 [0.900, 0.918] | 0.922 [0.911, 0.931] |
| Mayhem hold-out, trained on classic | 20,134 | 0.872 | 0.947 [0.932, 0.959] | 0.735 [0.683, 0.784] |
| Mayhem hold-out, trained on mayhem | 20,134 | 0.872 | 0.965 [0.953, 0.973] | 0.819 [0.791, 0.840] |
| Mayhem hold-out, pooled training | 20,134 | 0.872 | 0.968 [0.957, 0.975] | 0.831 [0.805, 0.851] |
| DRAIN label, one-feature reserves rule | 61,840 | 0.262 | 0.907 [0.894, 0.918] | 0.956 [0.951, 0.961] |
| collapse90 label, one-feature reserves rule | 61,840 | 0.464 | 0.919 [0.906, 0.930] | 0.923 [0.911, 0.933] |
| Logistic scorecard (reputation, creator and insider share), hold-out | 61,840 | 0.686 | 0.904 [0.895, 0.913] | 0.865 [0.852, 0.877] |
| Logistic scorecard, P4 hold-out | 30,030 | 0.588 | 0.854 [0.837, 0.870] | 0.853 [0.836, 0.868] |

| Threshold set on the validation days | Share flagged (test) | Precision | Recall | MCC | Rugs among unflagged | Graduated tokens flagged |
|---|---|---|---|---|---|---|
| Training-prevalence share | 0.667 | 0.900 | 0.875 | 0.654 | 0.256 | 308 of 483 (63.8%) |
| Budget 10% | 0.114 | 0.983 | 0.164 | 0.230 | 0.647 | 10 of 483 (2.1%) |
| Budget 5% | 0.057 | 0.990 | 0.082 | 0.161 | 0.667 | 3 of 483 (0.6%) |
| Budget 1% | 0.019 | 0.997 | 0.027 | 0.093 | 0.680 | 0 of 483 (0.0%) |
