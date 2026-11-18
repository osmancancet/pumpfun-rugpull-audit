| Analysis | n (test) | Prevalence | PR-AUC [95% CI] | ROC-AUC [95% CI] |
|---|---|---|---|---|
| Lead time: rugs ≥ 120 s after the snapshot vs all non-rugs | 24,815 | 0.216 | 0.546 [0.509, 0.580] | 0.850 [0.834, 0.865] |
| Lead time: rugs ≥ 180 s after the snapshot vs all non-rugs | 22,115 | 0.121 | 0.357 [0.319, 0.399] | 0.845 [0.826, 0.863] |
| Peak reserves ≥ 1 SOL | 10,686 | 0.577 | 0.762 [0.735, 0.785] | 0.725 [0.708, 0.741] |
| Peak reserves ≥ 5 SOL | 5,404 | 0.613 | 0.739 [0.717, 0.760] | 0.662 [0.645, 0.680] |
| P1 test, creator seen in P1 training | 67,390 | 0.373 | 0.792 [0.773, 0.810] | 0.885 [0.874, 0.896] |
| P1 test, creator unseen in P1 training | 27,277 | 0.321 | 0.707 [0.697, 0.717] | 0.864 [0.860, 0.868] |
| P3 hold-out, creator seen in training | 12,805 | 0.458 | 0.799 [0.758, 0.831] | 0.853 [0.824, 0.875] |
| P3 hold-out, creator unseen (= P4) | 18,337 | 0.318 | 0.695 [0.669, 0.723] | 0.868 [0.851, 0.884] |
| Classic launches only, P1 | 76,854 | 0.293 | 0.728 [0.714, 0.744] | 0.889 [0.881, 0.897] |
| Classic launches only, P4 hold-out | 15,384 | 0.272 | 0.678 [0.661, 0.698] | 0.887 [0.874, 0.900] |
| Mayhem hold-out, trained on classic | 6,950 | 0.629 | 0.721 [0.691, 0.752] | 0.610 [0.553, 0.664] |
| Mayhem hold-out, trained on mayhem | 6,950 | 0.629 | 0.799 [0.753, 0.836] | 0.713 [0.678, 0.744] |
| Mayhem hold-out, pooled training | 6,950 | 0.629 | 0.819 [0.775, 0.852] | 0.735 [0.701, 0.764] |
| DRAIN label, one-feature reserves rule | 31,142 | 0.160 | 0.783 [0.763, 0.802] | 0.942 [0.935, 0.949] |
| collapse90 label, one-feature reserves rule | 31,142 | 0.318 | 0.847 [0.830, 0.864] | 0.916 [0.904, 0.926] |
| Logistic scorecard (reputation, creator and insider share), hold-out | 31,142 | 0.376 | 0.650 [0.629, 0.671] | 0.811 [0.794, 0.826] |
| Logistic scorecard, P4 hold-out | 18,337 | 0.318 | 0.601 [0.578, 0.625] | 0.809 [0.789, 0.827] |

| Threshold set on the validation days | Share flagged (test) | Precision | Recall | MCC | Rugs among unflagged | Graduated tokens flagged |
|---|---|---|---|---|---|---|
| Training-prevalence share | 0.346 | 0.711 | 0.654 | 0.503 | 0.199 | 177 of 397 (44.6%) |
| Budget 10% | 0.084 | 0.835 | 0.187 | 0.287 | 0.333 | 19 of 397 (4.8%) |
| Budget 5% | 0.037 | 0.882 | 0.088 | 0.206 | 0.356 | 4 of 397 (1.0%) |
| Budget 1% | 0.008 | 0.939 | 0.020 | 0.103 | 0.371 | 0 of 397 (0.0%) |
