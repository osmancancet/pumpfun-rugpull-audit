"""Post hoc analyses requested in internal review round 6 (run after s02; earlier results are unchanged).

A  lead time of hold-out rugs, and ranking of rugs that leave at least 30 s / 60 s after the snapshot
B  launches with at least 1 SOL of peak reserves, and PR-AUC weighted by peak reserves (SOL at risk)
C  operating point fixed on the two validation days (model refit without them), applied to the test days
D  majority-class view on the P4 hold-out: PR-AUC of the non-rug class and false-safe rate at budgets
E  classic launches only: P1 versus P4, and H3 (learner minus best rule) on P4
F  matched population: P1 test launches split by whether their creator appears in P1 training
G  mayhem transfer with clustered intervals, and the pooled model on mayhem launches
H  drift slope of daily PR-AUC (frozen model), all launches and launches by creators unseen in its training
I  one-feature reserves rule for the DRAIN and collapse90 labels
J  published reputation versus causal/oracle on launches where the two reconstructions disagree
K  three-feature logistic scorecard baseline
Writes results/R6_*.csv and prints a summary. Uses the pre-specified models, seed and bootstrap size.
"""
import argparse
import numpy as np, pandas as pd
from scipy import stats
import config as C, common as U, models as M

ap = argparse.ArgumentParser(); ap.add_argument("--smoke", action="store_true"); args = ap.parse_args()
OUT = C.ROOT / ("results_smoke" if args.smoke else "results")
D = (pd.read_pickle(OUT / "analysis.pkl") if args.smoke else pd.read_parquet(C.DATA_PROC / "analysis.parquet"))
D = D.sort_values("t0").reset_index(drop=True)
DAYS = sorted(D.day.unique()); SEED = C.SEED; NB = 200 if args.smoke else C.N_BOOT; Y = C.PRIMARY_TARGET
BEST = M.available_models()[-1]; F = M.feature_set("causal"); F_nm = [c for c in F if c != "mayhem"]
RULES = ["c_rep_rug", "f10_rep_rug", "f10_dev_share", "f10_insider_share", "mayhem"]
folds = U.forward_folds(DAYS, C.TRAIN_DAYS, C.TEST_DAYS, C.GAP_DAYS) if not args.smoke else U.forward_folds(DAYS, 4, 2, 1)
trd, ted = folds[-1]
TR = D.day.isin(trd).to_numpy(); TE = D.day.isin(ted).to_numpy()
TEU = TE & ~D.creator.isin(set(D.loc[TR, "creator"])).to_numpy()
VALD = trd[-(C.VAL_DAYS if not args.smoke else 1):]
FIT = D.day.isin([d for d in trd if d not in VALD]).to_numpy(); VAL = D.day.isin(VALD).to_numpy()
CLS, MAY = (D.mayhem == 0).to_numpy(), (D.mayhem == 1).to_numpy()
rows = []

def fit(m, feats, tr, te, target=Y):
    cols = feats + [c for c in RULES if c not in feats] if (m.startswith("rule_") or m == "prior") else feats
    return M.fit_predict(m, D.loc[tr, cols], D.loc[tr, target].to_numpy(), D.loc[te, cols], SEED)

def put(block, what, n, **kw):
    rows.append(dict(block=block, what=what, n=int(n), **kw)); print(block, what, n, kw, flush=True)

def ci(y, s, g, metric=U.average_precision):
    if len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan
    return U.cluster_bootstrap_ci(y, s, g, metric, NB, SEED)

def pr_roc(block, what, mask_in_te, s_te, y_te, g_te):
    y, s, g = y_te[mask_in_te], s_te[mask_in_te], g_te[mask_in_te]
    pr = ci(y, s, g); roc = ci(y, s, g, U.roc_auc)
    put(block, what, len(y), prevalence=float(y.mean()), pr_auc=pr[0], pr_lo=pr[1], pr_hi=pr[2],
        roc_auc=roc[0], roc_lo=roc[1], roc_hi=roc[2])

# reference scores on the hold-out (same fit as E3)
s_te = fit(BEST, F, TR, TE); y_te = D.loc[TE, Y].to_numpy(); g_te = D.loc[TE, "creator"].to_numpy()
pr_roc("ref", "hold-out, all launches", np.ones(TE.sum(), bool), s_te, y_te, g_te)

# A lead time
lt = D.loc[TE, "lead_time_s"].to_numpy(); pos = y_te == 1
q = np.nanquantile(lt[pos], [0.1, 0.25, 0.5, 0.75, 0.9])
put("A", "lead time of hold-out rugs (s): q10,q25,median,q75,q90", pos.sum(),
    q10=q[0], q25=q[1], median=q[2], q75=q[3], q90=q[4],
    share_lt10=float(np.mean(lt[pos] < 10)), share_lt30=float(np.mean(lt[pos] < 30)), share_lt60=float(np.mean(lt[pos] < 60)))
for L in (30, 60):
    keep = ~pos | (lt >= L)          # drop rugs that leave within L s of the snapshot; non-rugs kept
    pr_roc("A", f"rugs leaving >= {L} s after the snapshot vs non-rugs", keep, s_te, y_te, g_te)

# B non-trivial launches and SOL-weighted PR-AUC
pk = D.loc[TE, "peak_rs"].to_numpy(float)
for thr in (1.0, 5.0):
    pr_roc("B", f"peak reserves >= {thr:g} SOL", pk >= thr, s_te, y_te, g_te)
w = np.clip(np.nan_to_num(pk), 0, None)
srt = U._Sorted(y_te, s_te); prior_w = float((w * y_te).sum() / w.sum())
put("B", "PR-AUC weighted by peak reserves (SOL)", len(y_te), weighted_pr_auc=U._w_ap(srt, w[srt.order]), weighted_prevalence=prior_w)

# C operating point fixed on validation days
s_val = fit(BEST, F, FIT, VAL); s_tv = fit(BEST, F, FIT, TE)
prev_fit = float(D.loc[FIT, Y].mean()); grad = D.loc[TE, "y_grad"].to_numpy() == 1
for name, rate in [("training-prevalence share", prev_fit), ("budget 10%", 0.10), ("budget 5%", 0.05), ("budget 1%", 0.01)]:
    thr = U.threshold_for_rate(s_val, rate); flag = s_tv >= thr
    tp = int((flag & (y_te == 1)).sum())
    put("C", f"threshold from validation days, {name}", len(y_te), flag_rate_val=rate, flag_rate_test=float(flag.mean()),
        precision=tp / max(flag.sum(), 1), recall=tp / max((y_te == 1).sum(), 1), mcc=U.mcc(y_te, flag.astype(int)),
        false_safe_rate=float(y_te[~flag].mean()) if (~flag).any() else np.nan,
        graduated_flagged=float(flag[grad].mean()) if grad.any() else np.nan, n_graduated=int(grad.sum()))

# D majority-class view on the P4 hold-out
yu = D.loc[TEU, Y].to_numpy(); gu = D.loc[TEU, "creator"].to_numpy()
for m in [BEST, "rule_insider", "rule_rep", "prior"]:
    su = fit(m, F, TR, TEU)
    nr = ci(1 - yu, 1 - su, gu)
    out = dict(nonrug_prevalence=float(1 - yu.mean()), nonrug_pr_auc=nr[0], nonrug_lo=nr[1], nonrug_hi=nr[2])
    for b in C.ALERT_BUDGETS:   # false-safe rate: share of rugs among the b lowest-scored launches (tie-aware)
        out[f"false_safe@{int(b*100)}%"] = 1 - U.precision_at_budget(1 - yu, 1 - su, b)
    put("D", f"P4 hold-out, {m}", len(yu), **out)

# E classic launches only
tr1, te1 = U.split_random_rows(len(D), 0.2, SEED)
for nm, a, b in [("P1 random mint, classic", tr1 & CLS, te1 & CLS), ("P4 hold-out, classic", TR & CLS, TEU & CLS)]:
    s = fit(BEST, F_nm, a, b); y = D.loc[b, Y].to_numpy(); g = D.loc[b, "creator"].to_numpy()
    pr_roc("E", nm, np.ones(b.sum(), bool), s, y, g)
    if nm.startswith("P4"):
        for r in ["rule_insider", "rule_dev", "rule_rep"]:
            d, lo, hi, p = U.cluster_bootstrap(y, s, fit(r, F_nm, a, b), g, U.average_precision, NB, SEED)
            put("E", f"P4 classic, {BEST} minus {r}", len(y), ap_diff=d, ci_lo=lo, ci_hi=hi, boot_p=p)
for nm, msk in [("P1 test", te1), ("P3 hold-out", TE), ("P4 hold-out", TEU)]:
    put("E", f"mayhem share, {nm}", msk.sum(), mayhem_share=float(D.loc[msk, "mayhem"].mean()))

# F matched population inside P1
s1 = fit(BEST, F, tr1, te1); y1 = D.loc[te1, Y].to_numpy(); g1 = D.loc[te1, "creator"].to_numpy()
seen1 = D.loc[te1, "creator"].isin(set(D.loc[tr1, "creator"])).to_numpy()
pr_roc("F", "P1 test, creator seen in P1 training", seen1, s1, y1, g1)
pr_roc("F", "P1 test, creator unseen in P1 training", ~seen1, s1, y1, g1)
seen3 = ~D.loc[TE, "creator"].isin(set(D.loc[TR, "creator"])).to_numpy()
pr_roc("F", "P3 hold-out, creator seen in training", ~seen3, s_te, y_te, g_te)
pr_roc("F", "P3 hold-out, creator unseen in training (= P4)", seen3, s_te, y_te, g_te)

# G mayhem transfer with intervals
ym = D.loc[TE & MAY, Y].to_numpy(); gm = D.loc[TE & MAY, "creator"].to_numpy()
for nm, a, feats in [("trained on classic", TR & CLS, F_nm), ("trained on mayhem", TR & MAY, F_nm), ("pooled (all training launches)", TR, F)]:
    s = fit(BEST, feats, a, TE & MAY)
    pr_roc("G", f"mayhem hold-out, {nm}", np.ones(len(ym), bool), s, ym, gm)
    put("G", f"mayhem hold-out ECE, {nm}", len(ym), ece=U.ece(ym, s))

# H drift slope of the frozen model
tr0 = D.day.isin(folds[0][0]).to_numpy(); s_all = fit(BEST, F, tr0, np.ones(len(D), bool))
unseen0 = ~D.creator.isin(set(D.loc[tr0, "creator"])).to_numpy()
for nm, base in [("all launches", np.ones(len(D), bool)), ("creators unseen in training", unseen0)]:
    dd = []
    for i, day in enumerate(DAYS):
        mm = (D.day == day).to_numpy() & ~tr0 & base
        if mm.sum() > 50 and D.loc[mm, Y].nunique() == 2:
            dd.append((i, U.average_precision(D.loc[mm, Y].to_numpy(), s_all[mm])))
    x, yv = np.array([a for a, _ in dd], float), np.array([b for _, b in dd])
    if len(x) < 3:
        put("H", f"daily PR-AUC slope per day, {nm}: fewer than 3 usable days", len(x)); continue
    X = np.c_[np.ones(len(x)), x]; beta, *_ = np.linalg.lstsq(X, yv, rcond=None)
    res = yv - X @ beta; s2 = res @ res / max(len(x) - 2, 1); se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    tq = stats.t.ppf(0.975, max(len(x) - 2, 1))
    put("H", f"daily PR-AUC slope per day, {nm}", len(x), slope=beta[1], slope_lo=beta[1] - tq * se, slope_hi=beta[1] + tq * se,
        pr_min=float(yv.min()), pr_max=float(yv.max()))

# I reserves rule for reserve-defined labels
for tgt in ["y_rug_drain", "y_collapse90"]:
    yt = D.loc[TE, tgt].to_numpy()
    s_rule = M._rule_scores(D.loc[TR, "f10_rs"].to_numpy(float), D.loc[TR, tgt].to_numpy(), D.loc[TE, "f10_rs"].to_numpy(float))
    s_l = fit(BEST, F, TR, TE, target=tgt)
    pr_roc("I", f"{tgt}, reserves rule (f10_rs)", np.ones(len(yt), bool), s_rule, yt, g_te)
    d, lo, hi, p = U.cluster_bootstrap(yt, s_l, s_rule, g_te, U.average_precision, NB, SEED)
    put("I", f"{tgt}, {BEST} minus reserves rule", len(yt), ap_diff=d, ci_lo=lo, ci_hi=hi, boot_p=p)

# J published reputation where causal and oracle disagree
m = D.f10_rep_rug.notna() & D.c_rep_rug.notna() & D.o_rep_rug.notna()
dis = m & ~np.isclose(D.c_rep_rug, D.o_rep_rug, atol=1e-9)
a, c, o = (D.loc[dis, k].to_numpy(float) for k in ["f10_rep_rug", "c_rep_rug", "o_rep_rug"])
put("J", "launches where causal and oracle rug shares differ", dis.sum(), share_all=float(dis.sum() / max(m.sum(), 1)),
    exact_causal=float(np.mean(np.isclose(a, c))), exact_oracle=float(np.mean(np.isclose(a, o))),
    mae_causal=float(np.mean(np.abs(a - c))), mae_oracle=float(np.mean(np.abs(a - o))),
    closer_to_causal=float(np.mean(np.abs(a - c) < np.abs(a - o))), closer_to_oracle=float(np.mean(np.abs(a - o) < np.abs(a - c))))

# K three-feature scorecard
SC = ["c_rep_rug", "c_rep_rug_missing", "f10_dev_share", "f10_insider_share"]
for nm, te_, y_, g_ in [("hold-out", TE, y_te, g_te), ("P4 hold-out", TEU, yu, gu)]:
    s_sc = fit("logreg", SC, TR, te_); s_b = s_te if nm == "hold-out" else fit(BEST, F, TR, TEU)
    pr_roc("K", f"scorecard (logistic, 3 features), {nm}", np.ones(len(y_), bool), s_sc, y_, g_)
    d, lo, hi, p = U.cluster_bootstrap(y_, s_b, s_sc, g_, U.average_precision, NB, SEED)
    put("K", f"{BEST} minus scorecard, {nm}", len(y_), ap_diff=d, ci_lo=lo, ci_hi=hi, boot_p=p)

pd.DataFrame(rows).to_csv(OUT / "R6_review_analyses.csv", index=False)
print(f"{len(rows)} rows -> {OUT / 'R6_review_analyses.csv'}")
