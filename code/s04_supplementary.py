"""Post-hoc supplementary tests requested in review round 3 (run after s02).
S1: H2 interval - hold-out PR-AUC of LightGBM with published (vendor) or oracle reputation minus causal.
S2: H3 under P4 - last-fold unseen-creator test set, LightGBM vs each baseline (DeLong + clustered AP bootstrap, BH).
Writes results/S1_reputation_diff.csv and results/S2_P4_holdout_tests.csv."""
import numpy as np, pandas as pd
import config as C, common as U, models as M
D = pd.read_parquet(C.DATA_PROC / "analysis.parquet").sort_values("t0").reset_index(drop=True)
DAYS = sorted(D.day.unique()); SEED = C.SEED; NB = C.N_BOOT; Y = C.PRIMARY_TARGET
BEST = M.available_models()[-1]                       # pre-specified reference learner (as in s02)
folds = U.forward_folds(DAYS, C.TRAIN_DAYS, C.TEST_DAYS, C.GAP_DAYS)
trd, ted = folds[-1]
TR = D.day.isin(trd).to_numpy(); TE = D.day.isin(ted).to_numpy()
seen = set(D.loc[TR, "creator"]); TEU = TE & ~D.creator.isin(seen).to_numpy()
RULES = ["c_rep_rug", "f10_rep_rug", "f10_dev_share", "f10_insider_share", "mayhem"]
def fit(m, feats, te):
    cols = feats + [c for c in RULES if c not in feats] if (m.startswith("rule_") or m == "prior") else feats
    return M.fit_predict(m, D.loc[TR, cols], D.loc[TR, Y].to_numpy(), D.loc[te, cols], SEED)
# S1
yte = D.loc[TE, Y].to_numpy(); g = D.loc[TE, "creator"].to_numpy()
sc = {r: fit(BEST, M.feature_set(r), TE) for r in ["causal", "vendor", "oracle", "none"]}
rows = []
for r in ["vendor", "oracle", "none"]:
    d, lo, hi, p = U.cluster_bootstrap(yte, sc[r], sc["causal"], g, U.average_precision, NB, SEED)
    rows.append(dict(comparison=f"{BEST} rep={r} minus rep=causal", n=len(yte), ap_diff=d, ci_lo=lo, ci_hi=hi, boot_p=p))
pd.DataFrame(rows).to_csv(C.ROOT / "results/S1_reputation_diff.csv", index=False); print(pd.DataFrame(rows))
# S2
yu = D.loc[TEU, Y].to_numpy(); gu = D.loc[TEU, "creator"].to_numpy(); F = M.feature_set("causal")
s = {m: fit(m, F, TEU) for m in [BEST, "prior", "rule_mayhem", "rule_dev", "rule_insider", "rule_rep", "logreg"]}
rows = []
for o in [m for m in s if m != BEST]:
    a1, a2, dif, se, z, p = U.delong_test(yu, s[BEST], s[o])
    d, lo, hi, pb = U.cluster_bootstrap(yu, s[BEST], s[o], gu, U.average_precision, NB, SEED)
    rows.append(dict(ref=BEST, other=o, n=len(yu), prevalence=float(yu.mean()), ap_ref=U.average_precision(yu, s[BEST]),
                     ap_other=U.average_precision(yu, s[o]), ap_diff=d, ci_lo=lo, ci_hi=hi, boot_p=pb, auc_ref=a1, auc_other=a2, delong_p=p))
R = pd.DataFrame(rows); R["bh_q"] = U.benjamini_hochberg(R.boot_p.to_numpy())
R.to_csv(C.ROOT / "results/S2_P4_holdout_tests.csv", index=False); print(R.to_string())
