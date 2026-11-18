| Manuscript location | Value | Source |
|---|---|---|
| Table 2: launches subset | 1,240,719 | flow.csv |
| Table 2: SOL-quoted (KI-03) | 1,016,047 | flow.csv |
| Table 2: decoder complete (KI-02) | 1,015,473 | flow.csv |
| Table 2: outcome resolved (KI-08) | 1,004,717 | flow.csv |
| Table 2: has f10 snapshot (KI-01) | 951,035 | flow.csv |
| Table 2: create lag <= 1 s | 951,035 | flow.csv |
| Table 2: non-negative snapshot age (KI-11) | 951,035 | flow.csv |
| Table 2: not rugged before the snapshot | 935,262 | flow.csv |
| Table 2: not migrated before the snapshot | 924,742 | flow.csv |
| Table 2: no rug within 60 s after the snapshot | 473,335 | flow.csv |
| 5.1 classic: launches / creators | 385,212 / 161,073 | table1_descriptives.csv |
| 5.1 classic: rug300 / graduated / first launch | 29.5% / 1.809% / 36.9% | table1_descriptives.csv |
| 5.1 mayhem: launches / creators | 88,123 / 11,672 | table1_descriptives.csv |
| 5.1 mayhem: rug300 / graduated / first launch | 63.7% / 0.040% / 6.2% | table1_descriptives.csv |
| 5.1 creators; top-1% share; max; median | 166,962; 38.0%; 9,851; 1 | creator_concentration.csv |
| Table 3 P1_random_mint causalrep | prev 0.358; PR 0.773 [0.758, 0.788]; ROC 0.880 [0.872, 0.889]; ECE 0.003 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P1_random_mint vendorrep | prev 0.358; PR 0.768 [0.752, 0.784]; ROC 0.877 [0.869, 0.886]; ECE 0.004 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P2_creator_grouped causalrep | prev 0.371; PR 0.753 [0.733, 0.772]; ROC 0.868 [0.853, 0.880]; ECE 0.008 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P2_creator_grouped vendorrep | prev 0.371; PR 0.745 [0.725, 0.764]; ROC 0.862 [0.848, 0.876]; ECE 0.010 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P3_time_forward causalrep | prev 0.382 ± 0.018; PR 0.752 ± 0.010 (hold-out 0.755 [0.725, 0.780]); ROC 0.862 ± 0.008; ECE 0.013 ± 0.002; fold upper limits 0.760–0.790 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P3_time_forward vendorrep | prev 0.382 ± 0.018; PR 0.746 ± 0.011 (hold-out 0.746 [0.717, 0.771]); ROC 0.858 ± 0.010; ECE 0.015 ± 0.003; fold upper limits 0.756–0.793 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P4_time_unseen_creator causalrep | prev 0.322 ± 0.022; PR 0.690 ± 0.014 (hold-out 0.695 [0.669, 0.723]); ROC 0.862 ± 0.013; ECE 0.013 ± 0.003; fold upper limits 0.684–0.725 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P4_time_unseen_creator vendorrep | prev 0.322 ± 0.022; PR 0.675 ± 0.012 (hold-out 0.685 [0.657, 0.714]); ROC 0.854 ± 0.017; ECE 0.016 ± 0.007; fold upper limits 0.673–0.714 | all_runs.csv, E1_protocol_CIs.csv |
| 5.3 agreement c_rep_rug | n 288,692; exact 61.3%; MAE 0.018; r 0.985 | E2_reputation_agreement.csv |
| 5.3 agreement o_rep_rug | n 289,129; exact 41.0%; MAE 0.051; r 0.924 | E2_reputation_agreement.csv |
| 5.3 agreement rep_n_vs_c_rep_n_res | n 473,335; exact 47.3%; MAE 42.251; r nan | E2_reputation_agreement.csv |
| 5.3 agreement rep_n_vs_o_rep_n_res | n 473,335; exact 68.3%; MAE 33.585; r nan | E2_reputation_agreement.csv |
| 5.3 S1 lgbm rep=vendor minus rep=causal | -0.0088 [-0.0131, -0.0046], p 0.000 | S1_reputation_diff.csv |
| 5.3 S1 lgbm rep=oracle minus rep=causal | 0.0017 [-0.0006, 0.0043], p 0.143 | S1_reputation_diff.csv |
| 5.3 S1 lgbm rep=none minus rep=causal | -0.0832 [-0.0994, -0.0671], p 0.000 | S1_reputation_diff.csv |
| Table 3b E2b|holdout|embargo=600s rule_rep_e600 | PR 0.648; ROC 0.780; ECE 0.016 | all_runs.csv |
| Table 3b E2b|holdout|embargo=600s lgbm | PR 0.757; ROC 0.867; ECE 0.012 | all_runs.csv |
| Table 3b E2b|holdout|embargo=86400s rule_rep_e86400 | PR 0.595; ROC 0.750; ECE 0.025 | all_runs.csv |
| Table 3b E2b|holdout|embargo=86400s lgbm | PR 0.750; ROC 0.864; ECE 0.014 | all_runs.csv |
| Table 3b E2|holdout|rep=causal lgbm | PR 0.755; ROC 0.866; ECE 0.013 | all_runs.csv |
| Table 3b E2|holdout|rep=causal logreg | PR 0.697; ROC 0.838; ECE 0.041 | all_runs.csv |
| Table 3b E2|holdout|rep=none lgbm | PR 0.671; ROC 0.826; ECE 0.021 | all_runs.csv |
| Table 3b E2|holdout|rep=none logreg | PR 0.647; ROC 0.809; ECE 0.039 | all_runs.csv |
| Table 3b E2|holdout|rep=oracle lgbm | PR 0.756; ROC 0.867; ECE 0.013 | all_runs.csv |
| Table 3b E2|holdout|rep=oracle logreg | PR 0.699; ROC 0.839; ECE 0.043 | all_runs.csv |
| Table 3b E2|holdout|rep=vendor lgbm | PR 0.746; ROC 0.863; ECE 0.011 | all_runs.csv |
| Table 3b E2|holdout|rep=vendor logreg | PR 0.684; ROC 0.831; ECE 0.050 | all_runs.csv |
| Table 4 prior | PR 0.376; lift 1.000; ROC 0.500; MCC 0.000; Brier 0.235; ECE 0.025; P@1% 0.376; P@5% 0.376; P@10% 0.376 | all_runs.csv |
| Table 4 rule_mayhem | PR 0.470; lift 1.252; ROC 0.621; MCC 0.000; Brier 0.216; ECE 0.016; P@1% 0.629; P@5% 0.629; P@10% 0.629 | all_runs.csv |
| Table 4 rule_dev | PR 0.603; lift 1.607; ROC 0.786; MCC 0.354; Brier 0.172; ECE 0.017; P@1% 0.652; P@5% 0.652; P@10% 0.652 | all_runs.csv |
| Table 4 rule_insider | PR 0.592; lift 1.578; ROC 0.774; MCC 0.325; Brier 0.177; ECE 0.026; P@1% 0.689; P@5% 0.689; P@10% 0.645 | all_runs.csv |
| Table 4 rule_rep | PR 0.633; lift 1.684; ROC 0.773; MCC 0.439; Brier 0.181; ECE 0.017; P@1% 0.786; P@5% 0.780; P@10% 0.760 | all_runs.csv |
| Table 4 logreg | PR 0.697; lift 1.856; ROC 0.838; MCC 0.472; Brier 0.159; ECE 0.041; P@1% 0.810; P@5% 0.765; P@10% 0.754 | all_runs.csv |
| Table 4 rf | PR 0.754; lift 2.007; ROC 0.866; MCC 0.512; Brier 0.144; ECE 0.007; P@1% 0.932; P@5% 0.877; P@10% 0.827 | all_runs.csv |
| Table 4 hgb | PR 0.755; lift 2.010; ROC 0.866; MCC 0.508; Brier 0.143; ECE 0.010; P@1% 0.936; P@5% 0.879; P@10% 0.833 | all_runs.csv |
| Table 4 lgbm | PR 0.755; lift 2.009; ROC 0.866; MCC 0.508; Brier 0.144; ECE 0.013; P@1% 0.929; P@5% 0.877; P@10% 0.835 | all_runs.csv |
| Table 4 / 5.6 Δ lgbm vs prior | 0.379 [0.352, 0.403], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_mayhem | 0.284 [0.263, 0.304], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_dev | 0.151 [0.127, 0.173], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_insider | 0.162 [0.141, 0.183], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_rep | 0.122 [0.105, 0.139], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs logreg | 0.057 [0.044, 0.070], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rf | 0.001 [-0.002, 0.004], BH q 0.810 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs hgb | -0.000 [-0.003, 0.002], BH q 0.828 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_reputation | 0.083 [0.067, 0.099], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_holder_structure | 0.002 [-0.000, 0.004], BH q 0.080 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_flow | 0.003 [-0.001, 0.007], BH q 0.131 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_mayhem_flag | 0.000 [-0.002, 0.002], BH q 0.938 | E3_E4_paired_tests.csv |
| 5.4 S2 lgbm vs prior (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.318; Δ 0.377 [0.345, 0.408]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_mayhem (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.384; Δ 0.311 [0.281, 0.339]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_dev (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.579; Δ 0.116 [0.091, 0.142]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_insider (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.549; Δ 0.146 [0.125, 0.169]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_rep (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.486; Δ 0.209 [0.183, 0.236]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs logreg (P4 hold-out n 18,337, prev 0.318) | 0.695 vs 0.649; Δ 0.046 [0.034, 0.058]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 Friedman | chi2 39.0, df 8, p 7e-06; ranks lgbm 1.6, hgb 1.8, rf 2.6, logreg 4.0, rule_dev 5.0, rule_insider 6.0, rule_rep 7.0, rule_mayhem 8.0, prior 9.0 | E3_friedman_P4.csv |
| 5.5 calibration logreg raw | ECE 0.0403; Brier 0.1596; PR 0.696 | E3_calibration.csv |
| 5.5 calibration logreg isotonic | ECE 0.0142; Brier 0.1560; PR 0.682 | E3_calibration.csv |
| 5.5 calibration logreg platt | ECE 0.0410; Brier 0.1591; PR 0.696 | E3_calibration.csv |
| 5.5 calibration rf raw | ECE 0.0077; Brier 0.1447; PR 0.747 | E3_calibration.csv |
| 5.5 calibration rf isotonic | ECE 0.0122; Brier 0.1449; PR 0.739 | E3_calibration.csv |
| 5.5 calibration rf platt | ECE 0.0098; Brier 0.1448; PR 0.747 | E3_calibration.csv |
| 5.5 calibration hgb raw | ECE 0.0119; Brier 0.1449; PR 0.746 | E3_calibration.csv |
| 5.5 calibration hgb isotonic | ECE 0.0120; Brier 0.1449; PR 0.737 | E3_calibration.csv |
| 5.5 calibration hgb platt | ECE 0.0105; Brier 0.1448; PR 0.746 | E3_calibration.csv |
| 5.5 calibration lgbm raw | ECE 0.0142; Brier 0.1450; PR 0.748 | E3_calibration.csv |
| 5.5 calibration lgbm isotonic | ECE 0.0102; Brier 0.1448; PR 0.740 | E3_calibration.csv |
| 5.5 calibration lgbm platt | ECE 0.0110; Brier 0.1448; PR 0.748 | E3_calibration.csv |
| 5.5 drift ranges | n 14,040–19,076; PR 0.730–0.766; ROC 0.845–0.880; ECE 0.010–0.026; prev 0.335–0.409 | E3_daily_drift_frozen_model.csv |
| Table 5 E5|label=y_rug120 prior | n 31,142; prev 0.200; PR 0.200; lift 1.00; ROC 0.500; ECE 0.020 | all_runs.csv |
| Table 5 E5|label=y_rug120 rule_rep | n 31,142; prev 0.200; PR 0.383; lift 1.92; ROC 0.748; ECE 0.012 | all_runs.csv |
| Table 5 E5|label=y_rug120 lgbm | n 31,142; prev 0.200; PR 0.495; lift 2.48; ROC 0.822; ECE 0.014 | all_runs.csv |
| Table 5 E5|label=y_rug3600 prior | n 31,142; prev 0.423; PR 0.423; lift 1.00; ROC 0.500; ECE 0.022 | all_runs.csv |
| Table 5 E5|label=y_rug3600 rule_rep | n 31,142; prev 0.423; PR 0.695; lift 1.65; ROC 0.783; ECE 0.017 | all_runs.csv |
| Table 5 E5|label=y_rug3600 lgbm | n 31,142; prev 0.423; PR 0.849; lift 2.01; ROC 0.902; ECE 0.010 | all_runs.csv |
| Table 5 E5|label=y_rug_any prior | n 31,142; prev 0.431; PR 0.431; lift 1.00; ROC 0.500; ECE 0.023 | all_runs.csv |
| Table 5 E5|label=y_rug_any rule_rep | n 31,142; prev 0.431; PR 0.700; lift 1.63; ROC 0.781; ECE 0.015 | all_runs.csv |
| Table 5 E5|label=y_rug_any lgbm | n 31,142; prev 0.431; PR 0.864; lift 2.01; ROC 0.907; ECE 0.009 | all_runs.csv |
| Table 5 E5|label=y_rug_drain prior | n 31,142; prev 0.160; PR 0.160; lift 1.00; ROC 0.500; ECE 0.004 | all_runs.csv |
| Table 5 E5|label=y_rug_drain rule_rep | n 31,142; prev 0.160; PR 0.284; lift 1.77; ROC 0.707; ECE 0.009 | all_runs.csv |
| Table 5 E5|label=y_rug_drain lgbm | n 31,142; prev 0.160; PR 0.843; lift 5.27; ROC 0.950; ECE 0.008 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump prior | n 31,142; prev 0.271; PR 0.271; lift 1.00; ROC 0.500; ECE 0.019 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump rule_rep | n 31,142; prev 0.271; PR 0.489; lift 1.81; ROC 0.751; ECE 0.011 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump lgbm | n 31,142; prev 0.271; PR 0.700; lift 2.58; ROC 0.883; ECE 0.015 | all_runs.csv |
| Table 5 E5|label=y_collapse90 prior | n 31,142; prev 0.318; PR 0.318; lift 1.00; ROC 0.500; ECE 0.002 | all_runs.csv |
| Table 5 E5|label=y_collapse90 rule_rep | n 31,142; prev 0.318; PR 0.454; lift 1.43; ROC 0.684; ECE 0.013 | all_runs.csv |
| Table 5 E5|label=y_collapse90 lgbm | n 31,142; prev 0.318; PR 0.889; lift 2.80; ROC 0.938; ECE 0.012 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_classic prior | n 24,192; prev 0.303; PR 0.303; lift 1.00; ROC 0.500; ECE 0.017 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_classic lgbm | n 24,192; prev 0.303; PR 0.694; lift 2.29; ROC 0.879; ECE 0.014 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_mayhem prior | n 6,950; prev 0.629; PR 0.629; lift 1.00; ROC 0.500; ECE 0.344 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_mayhem lgbm | n 6,950; prev 0.629; PR 0.721; lift 1.15; ROC 0.610; ECE 0.125 | all_runs.csv |
| Table 5 E5|regime=train_mayhem_test_mayhem prior | n 6,950; prev 0.629; PR 0.629; lift 1.00; ROC 0.500; ECE 0.012 | all_runs.csv |
| Table 5 E5|regime=train_mayhem_test_mayhem lgbm | n 6,950; prev 0.629; PR 0.799; lift 1.27; ROC 0.713; ECE 0.047 | all_runs.csv |
| Table 5 E5|filter=exclude_silence3s lgbm | n 31,000; prev 0.376; PR 0.757; lift 2.02; ROC 0.867; ECE 0.012 | all_runs.csv |
| Table 5 E5|filter=exclude_multihop_seam lgbm | n 31,142; prev 0.376; PR 0.753; lift 2.00; ROC 0.865; ECE 0.014 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators prior | n 8,011; prev 0.341; PR 0.341; lift 1.00; ROC 0.500; ECE 0.009 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators rule_rep | n 8,011; prev 0.341; PR 0.341; lift 1.00; ROC 0.500; ECE 0.107 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators lgbm | n 8,011; prev 0.341; PR 0.634; lift 1.86; ROC 0.823; ECE 0.016 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators prior | n 23,131; prev 0.387; PR 0.387; lift 1.00; ROC 0.500; ECE 0.037 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators rule_rep | n 23,131; prev 0.387; PR 0.693; lift 1.79; ROC 0.828; ECE 0.047 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators lgbm | n 23,131; prev 0.387; PR 0.779; lift 2.01; ROC 0.877; ECE 0.014 | all_runs.csv |
| Table 5 E5|seed=20261030 lgbm | n 31,142; prev 0.376; PR 0.755; lift 2.01; ROC 0.866; ECE 0.013 | all_runs.csv |
| Table 5 E5|seed=20261031 lgbm | n 31,142; prev 0.376; PR 0.755; lift 2.01; ROC 0.866; ECE 0.015 | all_runs.csv |
| Table 5 E5|seed=20261032 lgbm | n 31,142; prev 0.376; PR 0.755; lift 2.01; ROC 0.865; ECE 0.014 | all_runs.csv |
| Table 5 E5|seed=20261033 lgbm | n 31,142; prev 0.376; PR 0.754; lift 2.01; ROC 0.866; ECE 0.012 | all_runs.csv |
| Table 5 E5|seed=20261034 lgbm | n 31,142; prev 0.376; PR 0.754; lift 2.01; ROC 0.865; ECE 0.012 | all_runs.csv |
| Table 5 E5|train_legacy_harness_sample->test_complete lgbm | n 31,142; prev 0.376; PR 0.727; lift 1.93; ROC 0.854; ECE 0.040 | all_runs.csv |
| Table 5 five seeds | PR 0.7545 ± 0.0003; ROC 0.8655 ± 0.0001; ECE 0.0131 ± 0.0011 | all_runs.csv |
| 5.8 top-3 P1_random_mint | f10_rep_rug 0.139; f10_dev_share 0.072; f10_rep_n 0.043 | E6_permutation_importance.csv |
| 5.8 top-3 P4_time_unseen_creator | f10_rep_rug 0.082; f10_dev_share 0.064; f10_insider_share 0.048 | E6_permutation_importance.csv |
| 5.8 Kendall tau | 0.74 | E6_summary.json |
