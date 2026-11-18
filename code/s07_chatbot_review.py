"""Post hoc analyses for review round 10 (run after s02 and s06; earlier results are unchanged).

L  matched comparison stratified by resolved creator history (c_rep_n_res bins 0, 1-2, 3-9, 10+):
   P1 test seen/unseen and P3 hold-out seen/unseen (= P4), PR-AUC, ROC-AUC, prevalence, n per bin
M  full-stream deployment view: the reference model is trained on the actionable training rows, as in E3,
   and scores every hold-out launch, including those that rug within MIN_LEAD_S of the snapshot.
   Outcome = any rug within the 300 s horizon. Reports PR-AUC/ROC, ECE, the rug rate among the lowest-scored
   1/5/10% (safe list), the share of fast rugs among the top 1/5/10% and the share of fast rugs caught there.
N  P4 with "unseen" computed from the full training window (fast-rug launches included), actionable rows
O  launches with at least 1 SOL of peak reserves on the P4 hold-out, and the learner minus the best rule there
P  look-ahead audit restricted to launches whose published history count equals the causal one
   (removes history truncation as an explanation), with the number of creators behind it
Writes results/R7_chatbot_review.csv and prints a summary. Uses the pre-specified models, seed and bootstrap size.
"""
import argparse
import numpy as np, pandas as pd
import config as C, common as U, models as M

ap = argparse.ArgumentParser(); ap.add_argument("--smoke", action="store_true"); args = ap.parse_args()
OUT = C.ROOT / ("results_smoke" if args.smoke else "results")
D = (pd.read_pickle(OUT / "analysis.pkl") if args.smoke else pd.read_parquet(C.DATA_PROC / "analysis.parquet"))
D = D.sort_values("t0").reset_index(drop=True)
DAYS = sorted(D.day.unique()); SEED = C.SEED; NB = 200 if args.smoke else C.N_BOOT; Y = C.PRIMARY_TARGET
BEST = M.available_models()[-1]; F = M.feature_set("causal")
RULES = ["c_rep_rug", "f10_rep_rug", "f10_dev_share", "f10_insider_share", "mayhem"]
folds = U.forward_folds(DAYS, C.TRAIN_DAYS, C.TEST_DAYS, C.GAP_DAYS) if not args.smoke else U.forward_folds(DAYS, 4, 2, 1)
trd, ted = folds[-1]
TR = D.day.isin(trd).to_numpy(); TE = D.day.isin(ted).to_numpy()
TEU = TE & ~D.creator.isin(set(D.loc[TR, "creator"])).to_numpy()
rows = []

def fit(m, feats, Dtr, Dte, target=Y):
    cols = feats + [c for c in RULES if c not in feats] if (m.startswith("rule_") or m == "prior") else feats
    return M.fit_predict(m, Dtr[cols], Dtr[target].to_numpy(), Dte[cols], SEED)

def put(block, what, n, **kw):
    rows.append(dict(block=block, what=what, n=int(n), **kw)); print(block, what, n, kw, flush=True)

def ci(y, s, g, metric=U.average_precision):
    if len(y) < 20 or len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan
    return U.cluster_bootstrap_ci(y, s, g, metric, NB, SEED)

def pr_roc(block, what, msk, s, y, g, **extra):
    y, s, g = y[msk], s[msk], g[msk]
    pr = ci(y, s, g); roc = ci(y, s, g, U.roc_auc)
    put(block, what, len(y), prevalence=float(y.mean()) if len(y) else np.nan, pr_auc=pr[0], pr_lo=pr[1], pr_hi=pr[2],
        roc_auc=roc[0], roc_lo=roc[1], roc_hi=roc[2], **extra)

BINS = [(0, 0, "0"), (1, 2, "1-2"), (3, 9, "3-9"), (10, np.inf, "10+")]
def hbin(v):
    v = np.nan_to_num(np.asarray(v, float))
    return [(lab, (v >= lo) & (v <= hi)) for lo, hi, lab in BINS]

# reference fits (identical to s06)
s_te = fit(BEST, F, D[TR], D[TE]); y_te = D.loc[TE, Y].to_numpy(); g_te = D.loc[TE, "creator"].to_numpy()
pr_roc("ref", "hold-out, all launches (actionable target)", np.ones(TE.sum(), bool), s_te, y_te, g_te)

# L history-stratified matched comparison
tr1, te1 = U.split_random_rows(len(D), 0.2, SEED)
s1 = fit(BEST, F, D[tr1], D[te1]); y1 = D.loc[te1, Y].to_numpy(); g1 = D.loc[te1, "creator"].to_numpy()
seen1 = D.loc[te1, "creator"].isin(set(D.loc[tr1, "creator"])).to_numpy()
seen3 = D.loc[TE, "creator"].isin(set(D.loc[TR, "creator"])).to_numpy()
for nm, s, y, g, seen, h in [("P1 test", s1, y1, g1, seen1, D.loc[te1, "c_rep_n_res"]),
                             ("P3 hold-out", s_te, y_te, g_te, seen3, D.loc[TE, "c_rep_n_res"])]:
    for lab, b in hbin(h):
        pr_roc("L", f"{nm}, history {lab}, creator seen", b & seen, s, y, g, history_bin=lab, seen=1)
        pr_roc("L", f"{nm}, history {lab}, creator unseen", b & ~seen, s, y, g, history_bin=lab, seen=0)

# full-stream cohort: same build, no MIN_LEAD_S exclusion
import s01_build_dataset as B
lead_min = C.MIN_LEAD_S
raw = (pd.read_pickle(OUT / "syn_raw.pkl") if args.smoke
       else pd.concat([B.load("launches_legacy"), B.load("launches")], ignore_index=True))
C.MIN_LEAD_S = -1e12
DF, _, flow_full = B.build(raw); del raw
C.MIN_LEAD_S = lead_min
DF = DF.sort_values("t0").reset_index(drop=True)
DF["fast_rug"] = (DF.rugged.eq(1) & (DF.rug_dt_s - DF.f10_age < lead_min)).astype(int)
put("M", "full-stream cohort size; actionable cohort size", len(DF), actionable_n=len(D),
    fast_rug_n=int(DF.fast_rug.sum()), check_actionable=int((DF.fast_rug == 0).sum()))
FTR = DF.day.isin(trd).to_numpy(); FTE = DF.day.isin(ted).to_numpy()
sf = fit(BEST, F, D[TR], DF[FTE])                       # model of record, applied to every hold-out launch
yf = DF.loc[FTE, "y_rug300"].to_numpy(); gf = DF.loc[FTE, "creator"].to_numpy()
fast = DF.loc[FTE, "fast_rug"].to_numpy() == 1
unseen_full = ~DF.loc[FTE, "creator"].isin(set(DF.loc[FTR, "creator"])).to_numpy()
for nm, msk in [("full-stream hold-out", np.ones(len(yf), bool)), ("full-stream P4 hold-out", unseen_full)]:
    y, s = yf[msk], sf[msk]
    out = dict(ece=U.ece(y, s), mean_score=float(s.mean()), fast_share=float(fast[msk].mean()))
    for b in C.ALERT_BUDGETS:
        out[f"safe_rug_rate@{int(b*100)}%"] = 1 - U.precision_at_budget(1 - y, 1 - s, b)
        k = max(1, int(round(b * len(y)))); top = np.argsort(-s, kind="stable")[:k]
        out[f"fast_share_top@{int(b*100)}%"] = float(fast[msk][top].mean())
        out[f"fast_recall_top@{int(b*100)}%"] = float(fast[msk][top].sum() / max(fast[msk].sum(), 1))
        out[f"precision_top@{int(b*100)}%"] = U.precision_at_budget(y, s, b)
    pr_roc("M", nm, msk, sf, yf, gf, **out)
    pr_roc("M", f"{nm}, fast rugs vs non-rugs", msk & (fast | (yf == 0)), sf, yf, gf)

# N P4 with unseen defined on the full training window
full_tr_creators = set(DF.loc[FTR, "creator"])
TEU2 = TE & ~D.creator.isin(full_tr_creators).to_numpy()
put("N", "P4 overlap: actionable-defined vs full-window-defined unseen", TEU.sum(), n_full_defined=int(TEU2.sum()),
    n_both=int((TEU & TEU2).sum()))
pr_roc("N", "P4 hold-out, unseen relative to the full training window", TEU2[TE], s_te, y_te, g_te)

# O money at risk on P4
pk = D.loc[TE, "peak_rs"].to_numpy(float); u = ~seen3
pr_roc("O", "P4 hold-out, peak reserves >= 1 SOL", u & (pk >= 1), s_te, y_te, g_te)
m1 = TE.copy(); m1[TE] = u & (pk >= 1)
y_o = D.loc[m1, Y].to_numpy(); g_o = D.loc[m1, "creator"].to_numpy(); s_o = s_te[u & (pk >= 1)]
for r in ["rule_dev", "rule_rep", "rule_insider"]:
    if len(np.unique(y_o)) == 2:
        d_, lo, hi, p = U.cluster_bootstrap(y_o, s_o, fit(r, F, D[TR], D[m1]), g_o, U.average_precision, NB, SEED)
        put("O", f"P4 peak >= 1 SOL, {BEST} minus {r}", len(y_o), ap_diff=d_, ci_lo=lo, ci_hi=hi, boot_p=p)

# P look-ahead audit without history truncation
m = D.f10_rep_rug.notna() & D.c_rep_rug.notna() & D.o_rep_rug.notna() & D.f10_rep_n.notna()
same_n = m & (D.f10_rep_n == D.c_rep_n_res)
for nm, mm in [("all launches with all three fields", m), ("published count equals causal count", same_n)]:
    dis = mm & ~np.isclose(D.c_rep_rug, D.o_rep_rug, atol=1e-9)
    a, c, o = (D.loc[dis, k].to_numpy(float) for k in ["f10_rep_rug", "c_rep_rug", "o_rep_rug"])
    put("P", f"{nm}: discordant launches", dis.sum(), base_n=int(mm.sum()), creators=int(D.loc[dis, "creator"].nunique()),
        exact_all_causal=float(np.mean(np.isclose(D.loc[mm, "f10_rep_rug"], D.loc[mm, "c_rep_rug"]))),
        exact_all_oracle=float(np.mean(np.isclose(D.loc[mm, "f10_rep_rug"], D.loc[mm, "o_rep_rug"]))),
        exact_causal=float(np.mean(np.isclose(a, c))) if len(a) else np.nan,
        exact_oracle=float(np.mean(np.isclose(a, o))) if len(a) else np.nan,
        closer_to_causal=float(np.mean(np.abs(a - c) < np.abs(a - o))) if len(a) else np.nan)

pd.DataFrame(rows).to_csv(OUT / "R7_chatbot_review.csv", index=False)
pd.DataFrame(flow_full, columns=["step", "n"]).to_csv(OUT / "R7_flow_full_stream.csv", index=False)
print(f"{len(rows)} rows -> {OUT / 'R7_chatbot_review.csv'}")
