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
| 5.1 classic: launches / creators | 638,024 / 247,665 | table1_descriptives.csv |
| 5.1 classic: rug300 / graduated / first launch | 57.4% / 1.286% / 36.1% | table1_descriptives.csv |
| 5.1 mayhem: launches / creators | 286,718 / 13,932 | table1_descriptives.csv |
| 5.1 mayhem: rug300 / graduated / first launch | 88.8% / 0.016% / 2.7% | table1_descriptives.csv |
| 5.1 creators; top-1% share; max; median | 254,537; 49.7%; 10,006; 1 | creator_concentration.csv |
| Table 3 P1_random_mint causalrep | prev 0.671; PR 0.957 [0.953, 0.962]; ROC 0.928 [0.922, 0.934]; ECE 0.004 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P1_random_mint vendorrep | prev 0.671; PR 0.955 [0.951, 0.960]; ROC 0.925 [0.919, 0.931]; ECE 0.003 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P2_creator_grouped causalrep | prev 0.687; PR 0.958 [0.945, 0.969]; ROC 0.924 [0.913, 0.935]; ECE 0.003 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P2_creator_grouped vendorrep | prev 0.687; PR 0.956 [0.942, 0.968]; ROC 0.921 [0.910, 0.932]; ECE 0.003 | E1_protocol_CIs.csv, all_runs.csv |
| Table 3 P3_time_forward causalrep | prev 0.691 ± 0.014; PR 0.953 ± 0.001 (hold-out 0.953 [0.946, 0.959]); ROC 0.917 ± 0.005; ECE 0.007 ± 0.001; fold upper limits 0.959–0.961 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P3_time_forward vendorrep | prev 0.691 ± 0.014; PR 0.951 ± 0.002 (hold-out 0.951 [0.944, 0.958]); ROC 0.913 ± 0.007; ECE 0.010 ± 0.003; fold upper limits 0.957–0.961 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P4_time_unseen_creator causalrep | prev 0.593 ± 0.020; PR 0.922 ± 0.005 (hold-out 0.923 [0.909, 0.934]); ROC 0.907 ± 0.010; ECE 0.013 ± 0.005; fold upper limits 0.926–0.941 | all_runs.csv, E1_protocol_CIs.csv |
| Table 3 P4_time_unseen_creator vendorrep | prev 0.593 ± 0.020; PR 0.914 ± 0.007 (hold-out 0.918 [0.903, 0.931]); ROC 0.899 ± 0.014; ECE 0.016 ± 0.008; fold upper limits 0.923–0.936 | all_runs.csv, E1_protocol_CIs.csv |
| 5.3 agreement c_rep_rug | n 647,746; exact 57.0%; MAE 0.021; r 0.983 | E2_reputation_agreement.csv |
| 5.3 agreement o_rep_rug | n 648,265; exact 42.4%; MAE 0.039; r 0.941 | E2_reputation_agreement.csv |
| 5.3 agreement rep_n_vs_c_rep_n_res | n 924,742; exact 46.1%; MAE 83.487; r nan | E2_reputation_agreement.csv |
| 5.3 agreement rep_n_vs_o_rep_n_res | n 924,742; exact 60.5%; MAE 78.872; r nan | E2_reputation_agreement.csv |
| 5.3 S1 lgbm rep=vendor minus rep=causal | -0.0017 [-0.0027, -0.0006], p 0.001 | S1_reputation_diff.csv |
| 5.3 S1 lgbm rep=oracle minus rep=causal | 0.0008 [0.0003, 0.0013], p 0.002 | S1_reputation_diff.csv |
| 5.3 S1 lgbm rep=none minus rep=causal | -0.0275 [-0.0329, -0.0220], p 0.000 | S1_reputation_diff.csv |
| Table 3b E2b|holdout|embargo=600s rule_rep_e600 | PR 0.909; ROC 0.852; ECE 0.005 | all_runs.csv |
| Table 3b E2b|holdout|embargo=600s lgbm | PR 0.954; ROC 0.920; ECE 0.006 | all_runs.csv |
| Table 3b E2b|holdout|embargo=86400s rule_rep_e86400 | PR 0.871; ROC 0.806; ECE 0.022 | all_runs.csv |
| Table 3b E2b|holdout|embargo=86400s lgbm | PR 0.952; ROC 0.918; ECE 0.007 | all_runs.csv |
| Table 3b E2|holdout|rep=causal lgbm | PR 0.953; ROC 0.919; ECE 0.006 | all_runs.csv |
| Table 3b E2|holdout|rep=causal logreg | PR 0.931; ROC 0.891; ECE 0.025 | all_runs.csv |
| Table 3b E2|holdout|rep=none lgbm | PR 0.925; ROC 0.881; ECE 0.015 | all_runs.csv |
| Table 3b E2|holdout|rep=none logreg | PR 0.903; ROC 0.853; ECE 0.072 | all_runs.csv |
| Table 3b E2|holdout|rep=oracle lgbm | PR 0.954; ROC 0.920; ECE 0.007 | all_runs.csv |
| Table 3b E2|holdout|rep=oracle logreg | PR 0.931; ROC 0.892; ECE 0.027 | all_runs.csv |
| Table 3b E2|holdout|rep=vendor lgbm | PR 0.951; ROC 0.916; ECE 0.008 | all_runs.csv |
| Table 3b E2|holdout|rep=vendor logreg | PR 0.926; ROC 0.884; ECE 0.033 | all_runs.csv |
| Table 4 prior | PR 0.686; lift 1.000; ROC 0.500; MCC 0.000; Brier 0.216; ECE 0.022; P@1% 0.686; P@5% 0.686; P@10% 0.686 | all_runs.csv |
| Table 4 rule_mayhem | PR 0.763; lift 1.113; ROC 0.641; MCC 0.000; Brier 0.200; ECE 0.029; P@1% 0.872; P@5% 0.872; P@10% 0.872 | all_runs.csv |
| Table 4 rule_dev | PR 0.867; lift 1.264; ROC 0.801; MCC 0.535; Brier 0.140; ECE 0.018; P@1% 0.933; P@5% 0.933; P@10% 0.928 | all_runs.csv |
| Table 4 rule_insider | PR 0.866; lift 1.263; ROC 0.799; MCC 0.485; Brier 0.140; ECE 0.024; P@1% 0.928; P@5% 0.928; P@10% 0.929 | all_runs.csv |
| Table 4 rule_rep | PR 0.899; lift 1.312; ROC 0.841; MCC 0.404; Brier 0.142; ECE 0.009; P@1% 0.978; P@5% 0.973; P@10% 0.968 | all_runs.csv |
| Table 4 logreg | PR 0.931; lift 1.358; ROC 0.891; MCC 0.632; Brier 0.109; ECE 0.025; P@1% 0.984; P@5% 0.969; P@10% 0.963 | all_runs.csv |
| Table 4 rf | PR 0.951; lift 1.387; ROC 0.916; MCC 0.653; Brier 0.096; ECE 0.008; P@1% 0.998; P@5% 0.989; P@10% 0.984 | all_runs.csv |
| Table 4 hgb | PR 0.952; lift 1.389; ROC 0.918; MCC 0.656; Brier 0.095; ECE 0.007; P@1% 0.998; P@5% 0.991; P@10% 0.984 | all_runs.csv |
| Table 4 lgbm | PR 0.953; lift 1.390; ROC 0.919; MCC 0.660; Brier 0.095; ECE 0.006; P@1% 1.000; P@5% 0.993; P@10% 0.984 | all_runs.csv |
| Table 4 / 5.6 Δ lgbm vs prior | 0.267 [0.244, 0.292], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_mayhem | 0.190 [0.167, 0.214], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_dev | 0.086 [0.078, 0.094], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_insider | 0.087 [0.079, 0.095], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rule_rep | 0.054 [0.045, 0.063], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs logreg | 0.022 [0.019, 0.026], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs rf | 0.002 [0.001, 0.003], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm vs hgb | 0.001 [0.000, 0.001], BH q 0.046 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_reputation | 0.027 [0.022, 0.033], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_holder_structure | 0.001 [0.001, 0.002], BH q <0.001 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_flow | 0.001 [0.000, 0.002], BH q 0.008 | E3_E4_paired_tests.csv |
| Table 4 / 5.6 Δ lgbm|full vs lgbm|no_mayhem_flag | 0.000 [-0.000, 0.001], BH q 0.555 | E3_E4_paired_tests.csv |
| 5.4 S2 lgbm vs prior (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.588; Δ 0.335 [0.308, 0.363]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_mayhem (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.662; Δ 0.260 [0.227, 0.296]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_dev (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.809; Δ 0.113 [0.101, 0.124]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_insider (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.815; Δ 0.107 [0.097, 0.117]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs rule_rep (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.769; Δ 0.154 [0.129, 0.182]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 S2 lgbm vs logreg (P4 hold-out n 30,030, prev 0.588) | 0.923 vs 0.892; Δ 0.030 [0.024, 0.038]; q 0 | S2_P4_holdout_tests.csv |
| 5.4 Friedman | chi2 40.0, df 8, p 4.8e-06; ranks lgbm 1.0, hgb 2.0, rf 3.0, logreg 4.0, rule_insider 5.0, rule_dev 6.0, rule_rep 7.0, rule_mayhem 8.0, prior 9.0 | E3_friedman_P4.csv |
| 5.5 calibration logreg raw | ECE 0.0238; Brier 0.1091; PR 0.930 | E3_calibration.csv |
| 5.5 calibration logreg isotonic | ECE 0.0143; Brier 0.1076; PR 0.926 | E3_calibration.csv |
| 5.5 calibration logreg platt | ECE 0.0225; Brier 0.1093; PR 0.930 | E3_calibration.csv |
| 5.5 calibration rf raw | ECE 0.0087; Brier 0.0966; PR 0.950 | E3_calibration.csv |
| 5.5 calibration rf isotonic | ECE 0.0093; Brier 0.0968; PR 0.948 | E3_calibration.csv |
| 5.5 calibration rf platt | ECE 0.0107; Brier 0.0969; PR 0.950 | E3_calibration.csv |
| 5.5 calibration hgb raw | ECE 0.0090; Brier 0.0957; PR 0.952 | E3_calibration.csv |
| 5.5 calibration hgb isotonic | ECE 0.0075; Brier 0.0957; PR 0.950 | E3_calibration.csv |
| 5.5 calibration hgb platt | ECE 0.0077; Brier 0.0958; PR 0.952 | E3_calibration.csv |
| 5.5 calibration lgbm raw | ECE 0.0104; Brier 0.0957; PR 0.951 | E3_calibration.csv |
| 5.5 calibration lgbm isotonic | ECE 0.0078; Brier 0.0958; PR 0.950 | E3_calibration.csv |
| 5.5 calibration lgbm platt | ECE 0.0076; Brier 0.0958; PR 0.951 | E3_calibration.csv |
| 5.5 drift ranges | n 29,663–36,455; PR 0.943–0.958; ROC 0.906–0.929; ECE 0.008–0.016; prev 0.652–0.725 | E3_daily_drift_frozen_model.csv |
| Table 5 E5|label=y_rug60 prior | n 61,840; prev 0.490; PR 0.490; lift 1.00; ROC 0.500; ECE 0.013 | all_runs.csv |
| Table 5 E5|label=y_rug60 rule_rep | n 61,840; prev 0.490; PR 0.747; lift 1.52; ROC 0.791; ECE 0.010 | all_runs.csv |
| Table 5 E5|label=y_rug60 lgbm | n 61,840; prev 0.490; PR 0.845; lift 1.72; ROC 0.871; ECE 0.011 | all_runs.csv |
| Table 5 E5|label=y_rug3600 prior | n 61,840; prev 0.709; PR 0.709; lift 1.00; ROC 0.500; ECE 0.020 | all_runs.csv |
| Table 5 E5|label=y_rug3600 rule_rep | n 61,840; prev 0.709; PR 0.917; lift 1.29; ROC 0.852; ECE 0.008 | all_runs.csv |
| Table 5 E5|label=y_rug3600 lgbm | n 61,840; prev 0.709; PR 0.970; lift 1.37; ROC 0.940; ECE 0.006 | all_runs.csv |
| Table 5 E5|label=y_rug_any prior | n 61,840; prev 0.713; PR 0.713; lift 1.00; ROC 0.500; ECE 0.020 | all_runs.csv |
| Table 5 E5|label=y_rug_any rule_rep | n 61,840; prev 0.713; PR 0.919; lift 1.29; ROC 0.852; ECE 0.008 | all_runs.csv |
| Table 5 E5|label=y_rug_any lgbm | n 61,840; prev 0.713; PR 0.973; lift 1.36; ROC 0.944; ECE 0.006 | all_runs.csv |
| Table 5 E5|label=y_rug_drain prior | n 61,840; prev 0.262; PR 0.262; lift 1.00; ROC 0.500; ECE 0.024 | all_runs.csv |
| Table 5 E5|label=y_rug_drain rule_rep | n 61,840; prev 0.262; PR 0.385; lift 1.47; ROC 0.684; ECE 0.033 | all_runs.csv |
| Table 5 E5|label=y_rug_drain lgbm | n 61,840; prev 0.262; PR 0.933; lift 3.56; ROC 0.962; ECE 0.006 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump prior | n 61,840; prev 0.452; PR 0.452; lift 1.00; ROC 0.500; ECE 0.004 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump rule_rep | n 61,840; prev 0.452; PR 0.645; lift 1.43; ROC 0.734; ECE 0.024 | all_runs.csv |
| Table 5 E5|label=y_rug_devdump lgbm | n 61,840; prev 0.452; PR 0.903; lift 2.00; ROC 0.933; ECE 0.010 | all_runs.csv |
| Table 5 E5|label=y_collapse90 prior | n 61,840; prev 0.464; PR 0.464; lift 1.00; ROC 0.500; ECE 0.006 | all_runs.csv |
| Table 5 E5|label=y_collapse90 rule_rep | n 61,840; prev 0.464; PR 0.590; lift 1.27; ROC 0.664; ECE 0.024 | all_runs.csv |
| Table 5 E5|label=y_collapse90 lgbm | n 61,840; prev 0.464; PR 0.942; lift 2.03; ROC 0.942; ECE 0.008 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_classic prior | n 41,706; prev 0.596; PR 0.596; lift 1.00; ROC 0.500; ECE 0.034 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_classic lgbm | n 41,706; prev 0.596; PR 0.939; lift 1.58; ROC 0.929; ECE 0.004 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_mayhem prior | n 20,134; prev 0.872; PR 0.872; lift 1.00; ROC 0.500; ECE 0.311 | all_runs.csv |
| Table 5 E5|regime=train_classic_test_mayhem lgbm | n 20,134; prev 0.872; PR 0.947; lift 1.09; ROC 0.735; ECE 0.075 | all_runs.csv |
| Table 5 E5|regime=train_mayhem_test_mayhem prior | n 20,134; prev 0.872; PR 0.872; lift 1.00; ROC 0.500; ECE 0.018 | all_runs.csv |
| Table 5 E5|regime=train_mayhem_test_mayhem lgbm | n 20,134; prev 0.872; PR 0.965; lift 1.11; ROC 0.819; ECE 0.023 | all_runs.csv |
| Table 5 E5|filter=exclude_silence3s lgbm | n 61,574; prev 0.686; PR 0.953; lift 1.39; ROC 0.920; ECE 0.006 | all_runs.csv |
| Table 5 E5|filter=exclude_multihop_seam lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.008 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators prior | n 12,823; prev 0.588; PR 0.588; lift 1.00; ROC 0.500; ECE 0.075 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators rule_rep | n 12,823; prev 0.588; PR 0.588; lift 1.00; ROC 0.500; ECE 0.113 | all_runs.csv |
| Table 5 E5|subgroup=first_time_creators lgbm | n 12,823; prev 0.588; PR 0.868; lift 1.48; ROC 0.861; ECE 0.011 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators prior | n 49,017; prev 0.711; PR 0.711; lift 1.00; ROC 0.500; ECE 0.048 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators rule_rep | n 49,017; prev 0.711; PR 0.932; lift 1.31; ROC 0.884; ECE 0.041 | all_runs.csv |
| Table 5 E5|subgroup=repeat_creators lgbm | n 49,017; prev 0.711; PR 0.962; lift 1.35; ROC 0.929; ECE 0.007 | all_runs.csv |
| Table 5 E5|seed=20261030 lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.006 | all_runs.csv |
| Table 5 E5|seed=20261031 lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.006 | all_runs.csv |
| Table 5 E5|seed=20261032 lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.006 | all_runs.csv |
| Table 5 E5|seed=20261033 lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.007 | all_runs.csv |
| Table 5 E5|seed=20261034 lgbm | n 61,840; prev 0.686; PR 0.953; lift 1.39; ROC 0.919; ECE 0.007 | all_runs.csv |
| Table 5 E5|train_legacy_harness_sample->test_complete lgbm | n 61,840; prev 0.686; PR 0.945; lift 1.38; ROC 0.908; ECE 0.019 | all_runs.csv |
| Table 5 five seeds | PR 0.9528 ± 0.0001; ROC 0.9189 ± 0.0001; ECE 0.0066 ± 0.0005 | all_runs.csv |
| 5.8 top-3 P1_random_mint | f10_rep_rug 0.040; dev_buy_sol 0.030; f10_rep_n 0.019 | E6_permutation_importance.csv |
| 5.8 top-3 P4_time_unseen_creator | dev_buy_sol 0.047; f10_rep_rug 0.044; f10_dev_share 0.025 | E6_permutation_importance.csv |
| 5.8 Kendall tau | 0.74 | E6_summary.json |
