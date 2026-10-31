"""All experiments (E1-E6). Writes CSVs to results/ (or results_smoke/ with --smoke).

E1 protocol inflation      E2 reputation look-ahead audit   E3 baselines + calibration + tests
E4 feature-group ablation  E5 robustness (labels, regimes, seams, filters, seeds)
E6 importance stability across protocols
"""
import argparse, json, os, time
import numpy as np, pandas as pd
import config as C
import common as U
import models as M

ap = argparse.ArgumentParser()
ap.add_argument("--smoke", action="store_true", help="run on the synthetic table from smoke_test.py")
ap.add_argument("--max-train", type=int, default=0, help="optional cap on training rows (0 = all)")
args = ap.parse_args()

OUT = C.ROOT / ("results_smoke" if args.smoke else "results"); OUT.mkdir(parents=True, exist_ok=True)
SEED = C.SEED
N_BOOT = 200 if args.smoke else C.N_BOOT

def read(name):
    p = C.DATA_PROC / name
    if args.smoke:
        return pd.read_pickle(C.ROOT / "results_smoke" / name.replace(".parquet", ".pkl"))
    return pd.read_parquet(p)

D = read("analysis.parquet").sort_values("t0").reset_index(drop=True)
DAYS = sorted(D.day.unique())
MODELS_ML = M.available_models()
BASELINES = ["prior", "rule_mayhem", "rule_dev", "rule_insider", "rule_rep"]
log_rows = []

def cap(idx, seed):
    if args.max_train and idx.sum() > args.max_train:
        rng = np.random.default_rng(seed); w = np.flatnonzero(idx)
        keep = rng.choice(w, args.max_train, replace=False); m = np.zeros(len(idx), bool); m[keep] = True
        return m
    return idx

def evaluate(tag, tr, te, feats, target=C.PRIMARY_TARGET, models=None, val=None, store=None, data=None):
    """Fit every model on tr, score te; threshold fixed on val (or on tr) at the test prevalence of tr."""
    data = D if data is None else data
    tr = cap(tr, SEED)
    Xtr, ytr = data.loc[tr, feats + _rule_cols(feats)], data.loc[tr, target].to_numpy()
    Xte, yte = data.loc[te, feats + _rule_cols(feats)], data.loc[te, target].to_numpy()
    res = {}
    for m in (models or BASELINES + MODELS_ML):
        t = time.time()
        cols = list(Xtr.columns) if m.startswith("rule_") or m == "prior" else feats
        s = M.fit_predict(m, Xtr[cols], ytr, Xte[cols], SEED)
        # operating point: flag the same share of test launches as the TRAINING prevalence
        # (label-free on the test side; documented as a transductive rate rule)
        thr = U.threshold_for_rate(s, ytr.mean())
        met = U.all_metrics(yte, s, thr)
        for b in C.ALERT_BUDGETS:
            met[f"prec@{int(b*100)}%"] = U.precision_at_budget(yte, s, b)
        met.update(tag=tag, model=m, n_train=int(tr.sum()), secs=round(time.time() - t, 1))
        log_rows.append(met); res[m] = s
        print(f"{time.strftime('%H:%M:%S')} {tag} {m} n_tr={int(tr.sum())} n_te={int(te.sum())} ap={met.get('pr_auc', float('nan')):.4f} {met['secs']}s", flush=True)
        if store is not None:
            store[(tag, m)] = s
    return res, yte

def _rule_cols(feats):
    need = ["c_rep_rug", "f10_rep_rug", "f10_dev_share", "f10_insider_share", "mayhem"] + \
           [f"e{e}_rep_rug" for e in C.REP_EMBARGO_SENS if f"e{e}_rep_rug" in D.columns]
    return [c for c in need if c not in feats]

def save():
    pd.DataFrame(log_rows).to_csv(OUT / "all_runs.csv", index=False)

# ========================================================================= E1 protocols
FEATS_V = M.feature_set("vendor"); FEATS_C = M.feature_set("causal")
preds = {}
tr, te = U.split_random_rows(len(D), 0.2, SEED)
for fs, F in [("vendorrep", FEATS_V), ("causalrep", FEATS_C)]:
    evaluate(f"E1|P1_random_mint|{fs}", tr, te, F, store=preds)
tr, te = U.split_group(D.creator, 0.2, SEED)
for fs, F in [("vendorrep", FEATS_V), ("causalrep", FEATS_C)]:
    evaluate(f"E1|P2_creator_grouped|{fs}", tr, te, F, store=preds)
# P3 forward folds; P4 = P3 restricted to test creators never seen in training
folds = U.forward_folds(DAYS, C.TRAIN_DAYS, C.TEST_DAYS, C.GAP_DAYS) if not args.smoke else U.forward_folds(DAYS, 4, 2, 1)
fold_scores = []
for k, (trd, ted) in enumerate(folds):
    tr = D.day.isin(trd).to_numpy().copy(); te = D.day.isin(ted).to_numpy().copy()
    seen = set(D.loc[tr, "creator"]); te_unseen = te & ~D.creator.isin(seen).to_numpy()
    for fs, F in [("vendorrep", FEATS_V), ("causalrep", FEATS_C)]:
        r, y = evaluate(f"E1|P3_time_forward|{fs}|fold{k}", tr, te, F, store=preds)
        r2, y2 = evaluate(f"E1|P4_time_unseen_creator|{fs}|fold{k}", tr, te_unseen, F, store=preds)
    fold_scores.append((k, trd[0], trd[-1], ted[0], ted[-1], int(te.sum()), int(te_unseen.sum())))
pd.DataFrame(fold_scores, columns=["fold", "train_from", "train_to", "test_from", "test_to", "n_test", "n_test_unseen"]).to_csv(OUT / "folds.csv", index=False)
save()

# main hold-out used for paired tests: last fold (train <= day t, gap, test last days)
trd, ted = folds[-1]
TR = D.day.isin(trd).to_numpy(); TE = D.day.isin(ted).to_numpy()
VAL_DAYS = trd[-C.VAL_DAYS:] if not args.smoke else trd[-1:]
FIT = D.day.isin(trd[:-len(VAL_DAYS)]).to_numpy(); VAL = D.day.isin(VAL_DAYS).to_numpy()

# ========================================================================= E2 reputation audit
au = []
m = D.f10_rep_rug.notna()
for ref in ["c_rep_rug", "o_rep_rug"]:
    mm = m & D[ref].notna()
    a, b = D.loc[mm, "f10_rep_rug"].to_numpy(), D.loc[mm, ref].to_numpy()
    au.append(dict(reference=ref, n=int(mm.sum()), mae=float(np.mean(np.abs(a - b))),
                   exact_share=float(np.mean(np.isclose(a, b, atol=1e-9))),
                   pearson=float(np.corrcoef(a, b)[0, 1]) if mm.sum() > 2 else np.nan))
mm = D.f10_rep_n.notna()
au.append(dict(reference="rep_n_vs_c_rep_n_res", n=int(mm.sum()),
               mae=float(np.mean(np.abs(D.loc[mm, "f10_rep_n"] - D.loc[mm, "c_rep_n_res"]))),
               exact_share=float(np.mean(D.loc[mm, "f10_rep_n"] == D.loc[mm, "c_rep_n_res"])), pearson=np.nan))
au.append(dict(reference="rep_n_vs_o_rep_n_res", n=int(mm.sum()),
               mae=float(np.mean(np.abs(D.loc[mm, "f10_rep_n"] - D.loc[mm, "o_rep_n_res"]))),
               exact_share=float(np.mean(D.loc[mm, "f10_rep_n"] == D.loc[mm, "o_rep_n_res"])), pearson=np.nan))
pd.DataFrame(au).to_csv(OUT / "E2_reputation_agreement.csv", index=False)
best = MODELS_ML[-1]
for rep in ["none", "causal", "vendor", "oracle"]:
    evaluate(f"E2|holdout|rep={rep}", TR, TE, M.feature_set(rep), models=[best, "logreg"], store=preds)
# E2b embargo sensitivity of the causal reputation (review round 2, R1.R2-1)
for e in C.REP_EMBARGO_SENS:
    if f"e{e}_rep_rug" in D.columns:
        evaluate(f"E2b|holdout|embargo={e}s", TR, TE, M.feature_set(f"causal_e{e}"), models=["rule_rep_e%d" % e, best])
save()

# ========================================================================= E3 baselines, calibration, tests
r, yte = evaluate("E3|holdout|causalrep", TR, TE, FEATS_C, store=preds)
grp = D.loc[TE, "creator"].to_numpy()
PREV_TR = float(D.loc[TR, C.PRIMARY_TARGET].mean())
tests = []
ref = best
for other in [m for m in BASELINES + MODELS_ML if m != ref]:
    a1, a2, dif, se, z, p = U.delong_test(yte, r[ref], r[other])
    d_ap, lo, hi, p_ap = U.cluster_bootstrap(yte, r[ref], r[other], grp, U.average_precision, N_BOOT, SEED)
    # operating point from the TRAINING prevalence (no test labels used; review R1.3)
    thr_a = U.threshold_for_rate(r[ref], PREV_TR); thr_b = U.threshold_for_rate(r[other], PREV_TR)
    b, c, p_mc = U.mcnemar_test(yte, r[ref] >= thr_a, r[other] >= thr_b)
    tests.append(dict(ref=ref, other=other, auc_ref=a1, auc_other=a2, auc_diff=dif, delong_p=p,
                      ap_diff=d_ap, ap_ci_lo=lo, ap_ci_hi=hi, ap_boot_p=p_ap, mcnemar_b=b, mcnemar_c=c, mcnemar_p=p_mc))
T = pd.DataFrame(tests)
# protocol contrasts on the same model: P1 vs P4 inflation (bootstrap CI of the PR-AUC per protocol)
ci = []
for key, s in preds.items():
    tag, mname = key
    if mname != ref or not tag.startswith("E1"):
        continue
    parts = tag.split("|")
    if parts[1] == "P1_random_mint":
        _, te_ = U.split_random_rows(len(D), 0.2, SEED)
    elif parts[1] == "P2_creator_grouped":
        _, te_ = U.split_group(D.creator, 0.2, SEED)
    else:
        k = int(parts[-1].replace("fold", "")); trd_, ted_ = folds[k]
        te_ = D.day.isin(ted_).to_numpy().copy()
        if parts[1] == "P4_time_unseen_creator":
            te_ &= ~D.creator.isin(set(D.loc[D.day.isin(trd_), "creator"])).to_numpy()
    y_ = D.loc[te_, C.PRIMARY_TARGET].to_numpy(); g_ = D.loc[te_, "creator"].to_numpy()
    if len(np.unique(y_)) < 2:
        continue
    for nm, f in [("pr_auc", U.average_precision), ("roc_auc", U.roc_auc)]:
        pt, lo, hi = U.cluster_bootstrap_ci(y_, s, g_, f, N_BOOT, SEED)
        ci.append(dict(tag=tag, model=mname, metric=nm, value=pt, ci_lo=lo, ci_hi=hi))
pd.DataFrame(ci).to_csv(OUT / "E1_protocol_CIs.csv", index=False)

# calibration: raw vs isotonic/Platt fitted on validation days (never on test)
cal = []
Xf, yf = D.loc[FIT, FEATS_C], D.loc[FIT, C.PRIMARY_TARGET].to_numpy()
Xv, yv = D.loc[VAL, FEATS_C], D.loc[VAL, C.PRIMARY_TARGET].to_numpy()
Xt = D.loc[TE, FEATS_C]
for mname in MODELS_ML:
    sv = M.fit_predict(mname, Xf, yf, Xv, SEED); st = M.fit_predict(mname, Xf, yf, Xt, SEED)
    variants = {"raw": st}
    try:
        from sklearn.isotonic import IsotonicRegression
        from sklearn.linear_model import LogisticRegression
        variants["isotonic"] = IsotonicRegression(out_of_bounds="clip").fit(sv, yv).predict(st)
        lg = LogisticRegression().fit(np.log(np.clip(sv, 1e-6, 1-1e-6) / (1 - np.clip(sv, 1e-6, 1-1e-6)))[:, None], yv)
        variants["platt"] = lg.predict_proba(np.log(np.clip(st, 1e-6, 1-1e-6) / (1 - np.clip(st, 1e-6, 1-1e-6)))[:, None])[:, 1]
    except ImportError:
        pass
    for vn, s in variants.items():
        cal.append(dict(model=mname, calibration=vn, brier=U.brier(yte, s), ece=U.ece(yte, s), pr_auc=U.average_precision(yte, s)))
        if vn == "raw":
            p = np.clip(s, 0, 1); bins = np.minimum((p * 10).astype(int), 9)
            rel = pd.DataFrame({"bin": bins, "p": p, "y": yte}).groupby("bin").agg(mean_p=("p", "mean"), frac_pos=("y", "mean"), n=("y", "size"))
            rel.assign(model=mname).to_csv(OUT / f"E3_reliability_{mname}.csv")
pd.DataFrame(cal).to_csv(OUT / "E3_calibration.csv", index=False)

# per-day drift of the best model trained once on the first window
drift = []
tr0 = D.day.isin(folds[0][0]).to_numpy()
s_all = M.fit_predict(best, D.loc[tr0, FEATS_C], D.loc[tr0, C.PRIMARY_TARGET].to_numpy(), D[FEATS_C], SEED)
for dday in DAYS:
    mm = (D.day == dday).to_numpy() & ~tr0
    if mm.sum() > 50 and D.loc[mm, C.PRIMARY_TARGET].nunique() == 2:
        y_ = D.loc[mm, C.PRIMARY_TARGET].to_numpy()
        drift.append(dict(day=dday, n=int(mm.sum()), prevalence=float(y_.mean()), pr_auc=U.average_precision(y_, s_all[mm]),
                          roc_auc=U.roc_auc(y_, s_all[mm]), ece=U.ece(y_, s_all[mm]), multihop_seam=int(D.loc[mm, "seam_multihop"].max())))
pd.DataFrame(drift).to_csv(OUT / "E3_daily_drift_frozen_model.csv", index=False)

# Friedman test of models across forward folds (P4, causal reputation)
R = pd.DataFrame(log_rows)
sub = R[R.tag.str.startswith("E1|P4_time_unseen_creator|causalrep")]
W = sub.pivot_table(index="tag", columns="model", values="pr_auc")
if len(W) >= 2:
    chi2, df_, p_f, ranks = U.friedman_statistic(W.to_numpy())
    pd.DataFrame({"model": W.columns, "mean_rank": ranks}).assign(chi2=chi2, df=df_, p=p_f).to_csv(OUT / "E3_friedman_P4.csv", index=False)

# ========================================================================= E4 ablation
groups = {"no_reputation": [c for c in FEATS_C if c.startswith("c_rep")], "no_holder_structure": M.HOLDER,
          "no_flow": M.FLOW, "no_mayhem_flag": ["mayhem"]}
for gname, drop in groups.items():
    F = [c for c in FEATS_C if c not in drop]
    r_ab, _ = evaluate(f"E4|holdout|{gname}", TR, TE, F, models=[best], store=preds)
    d_ap, lo, hi, p_ap = U.cluster_bootstrap(yte, r[best], r_ab[best], grp, U.average_precision, N_BOOT, SEED)
    T = pd.concat([T, pd.DataFrame([dict(ref=f"{best}|full", other=f"{best}|{gname}", ap_diff=d_ap, ap_ci_lo=lo, ap_ci_hi=hi, ap_boot_p=p_ap)])])
# BH within pre-specified families (review R1.2): primary = clustered-bootstrap PR-AUC test over
# all E3 pairwise and E4 ablation contrasts; DeLong and McNemar adjusted as separate secondary families.
T["bh_q"] = U.benjamini_hochberg(T["ap_boot_p"].fillna(1).to_numpy())
for col in ["delong_p", "mcnemar_p"]:
    ok_ = T[col].notna().to_numpy(); q = np.full(len(T), np.nan)
    if ok_.any():
        q[ok_] = U.benjamini_hochberg(T.loc[ok_, col].to_numpy())
    T[col.replace("_p", "_bh_q")] = q
T.to_csv(OUT / "E3_E4_paired_tests.csv", index=False)
save()

# ========================================================================= E5 robustness
for tgt in ["y_rug60", "y_rug3600", "y_rug_any", "y_rug_drain", "y_rug_devdump", "y_collapse90"]:
    if D.loc[TR, tgt].nunique() == 2 and D.loc[TE, tgt].nunique() == 2:
        evaluate(f"E5|label={tgt}", TR, TE, FEATS_C, target=tgt, models=["prior", "rule_rep", best])
# label-rank agreement: does the model ranking survive a change of label?
# regimes
cls, may = (D.mayhem == 0).to_numpy(), (D.mayhem == 1).to_numpy()
F_nm = [c for c in FEATS_C if c != "mayhem"]
evaluate("E5|regime=train_classic_test_classic", TR & cls, TE & cls, F_nm, models=["prior", best])
evaluate("E5|regime=train_classic_test_mayhem", TR & cls, TE & may, F_nm, models=["prior", best])
evaluate("E5|regime=train_mayhem_test_mayhem", TR & may, TE & may, F_nm, models=["prior", best])
evaluate("E5|filter=exclude_silence3s", TR & (D.silence_flag == 0).to_numpy(), TE & (D.silence_flag == 0).to_numpy(), FEATS_C, models=[best])
evaluate("E5|filter=exclude_multihop_seam", TR & (D.seam_multihop == 0).to_numpy(), TE, FEATS_C, models=[best])
evaluate("E5|subgroup=first_time_creators", TR, TE & (D.first_time_creator == 1).to_numpy(), FEATS_C, models=["prior", "rule_rep", best])
evaluate("E5|subgroup=repeat_creators", TR, TE & (D.first_time_creator == 0).to_numpy(), FEATS_C, models=["prior", "rule_rep", best])
for sd in range(5):
    s = M.fit_predict(best, D.loc[TR, FEATS_C], D.loc[TR, C.PRIMARY_TARGET].to_numpy(), D.loc[TE, FEATS_C], SEED + sd)
    log_rows.append(dict(tag=f"E5|seed={SEED+sd}", model=best, **U.all_metrics(yte, s)))
# legacy (decoder seam + sampled features) -> complete: train on legacy, test on the hold-out
if not args.smoke and (C.DATA_PROC / "legacy.parquet").exists():
    L = pd.read_parquet(C.DATA_PROC / "legacy.parquet")
    L = L[L.f10_age >= 0]
    F_l = [c for c in FEATS_C if c in L.columns]
    for basis in ["harness_sample", "tape_replay"]:
        Lb = L[L.features_basis == basis]
        if len(Lb) > 1000 and Lb.y_rug300.nunique() == 2:
            s = M.fit_predict(best, Lb[F_l], Lb.y_rug300.to_numpy(), D.loc[TE, F_l], SEED)
            log_rows.append(dict(tag=f"E5|train_legacy_{basis}->test_complete", model=best, **U.all_metrics(yte, s)))
    lb = L.groupby("features_basis").agg(n=("mint", "size"), rug300=("y_rug300", "mean"))
    lb.to_csv(OUT / "E5_legacy_selection_bias.csv")
save()

# ========================================================================= E6 importance stability
def perm_importance(model_name, Xtr, ytr, Xte, yte, feats, seed, reps=3):
    rng = np.random.default_rng(seed)
    base = U.average_precision(yte, M.fit_predict(model_name, Xtr, ytr, Xte, seed))
    prep = M.Prep().fit(Xtr); mdl, scaled = M.make_model(model_name, seed)
    mdl.fit(prep.transform(Xtr, scale=scaled), ytr)
    out = {}
    for f in feats:
        drops = []
        for _ in range(reps):
            Xp = Xte.copy(); Xp[f] = rng.permutation(Xp[f].to_numpy())
            drops.append(base - U.average_precision(yte, mdl.predict_proba(prep.transform(Xp, scale=scaled))[:, 1]))
        out[f] = float(np.mean(drops))
    return out
imp = {}
tr1, te1 = U.split_random_rows(len(D), 0.2, SEED)
for nm, (a, b) in {"P1_random_mint": (tr1, te1), "P4_time_unseen_creator": (TR, TE & ~D.creator.isin(set(D.loc[TR, "creator"])).to_numpy())}.items():
    imp[nm] = perm_importance(best, D.loc[a, FEATS_V], D.loc[a, C.PRIMARY_TARGET].to_numpy(),
                              D.loc[b, FEATS_V], D.loc[b, C.PRIMARY_TARGET].to_numpy(), FEATS_V, SEED)
I = pd.DataFrame(imp); I.to_csv(OUT / "E6_permutation_importance.csv")
ra, rb = U._midrank(-I.iloc[:, 0].to_numpy()), U._midrank(-I.iloc[:, 1].to_numpy())
n = len(ra); conc = sum(np.sign(ra[i]-ra[j]) * np.sign(rb[i]-rb[j]) for i in range(n) for j in range(i+1, n))
json.dump({"kendall_tau_P1_vs_P4": conc / (n*(n-1)/2), "best_model": best, "models": MODELS_ML,
           "n_rows": int(len(D)), "days": DAYS}, open(OUT / "E6_summary.json", "w"), indent=1)
save()
print("done; results in", OUT)
