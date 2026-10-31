"""Collect every number the manuscript cites into results/key_numbers.md (run after s04).

The manuscript is updated from this one file after each full run; values are never typed by hand.
Each line names the manuscript location and the results file the value comes from.
"""
import json
import numpy as np, pandas as pd
import config as C

R = C.RESULTS
runs = pd.read_csv(R / "all_runs.csv")
best = json.load(open(R / "E6_summary.json"))["best_model"]
out = []
def put(where, value, src):
    out.append((where, value, src))
f3 = lambda x: f"{x:.3f}"

# cohort and flow
flow = pd.read_csv(R / "flow.csv")
for _, r in flow.iterrows():
    put(f"Table 2: {r.step}", f"{int(r.rows):,}", "flow.csv")
t1 = pd.read_csv(R / "table1_descriptives.csv", index_col=0)
for m, nm in [(0, "classic"), (1, "mayhem")]:
    r = t1.loc[m]
    put(f"5.1 {nm}: launches / creators", f"{int(r.n):,} / {int(r.creators):,}", "table1_descriptives.csv")
    put(f"5.1 {nm}: rug300 / graduated / first launch", f"{r.rug300:.1%} / {r.grad:.3%} / {r.first_time:.1%}", "table1_descriptives.csv")
cc = pd.read_csv(R / "creator_concentration.csv", index_col=0).iloc[:, 0]
put("5.1 creators; top-1% share; max; median", f"{int(cc.creators):,}; {cc.share_launches_top1pct_creators:.1%}; {int(cc.max_launches_one_creator):,}; {cc.median_launches_per_creator:.0f}", "creator_concentration.csv")

# Table 3 (protocols)
e1 = runs[runs.tag.str.startswith("E1") & (runs.model == best)].copy()
e1["protocol"] = e1.tag.str.split("|").str[1]; e1["reps"] = e1.tag.str.split("|").str[2]
ci = pd.read_csv(R / "E1_protocol_CIs.csv")
folds = pd.read_csv(R / "folds.csv"); last = int(folds.fold.max())
for (p, rp), g in e1.groupby(["protocol", "reps"]):
    if len(g) == 1:
        c_pr = ci[(ci.tag == g.tag.iloc[0]) & (ci.metric == "pr_auc")].iloc[0]
        c_roc = ci[(ci.tag == g.tag.iloc[0]) & (ci.metric == "roc_auc")].iloc[0]
        put(f"Table 3 {p} {rp}", f"prev {f3(g.prevalence.iloc[0])}; PR {f3(c_pr.value)} [{f3(c_pr.ci_lo)}, {f3(c_pr.ci_hi)}]; "
            f"ROC {f3(c_roc.value)} [{f3(c_roc.ci_lo)}, {f3(c_roc.ci_hi)}]; ECE {f3(g.ece.iloc[0])}", "E1_protocol_CIs.csv, all_runs.csv")
    else:
        tag_last = g.tag[g.tag.str.endswith(f"fold{last}")].iloc[0]
        c_pr = ci[(ci.tag == tag_last) & (ci.metric == "pr_auc")].iloc[0]
        ups = ci[ci.tag.str.contains(f"{p}\\|{rp}\\|fold", regex=True) & (ci.metric == "pr_auc")].ci_hi
        put(f"Table 3 {p} {rp}", f"prev {f3(g.prevalence.mean())} ± {f3(g.prevalence.std())}; PR {f3(g.pr_auc.mean())} ± {f3(g.pr_auc.std())} "
            f"(hold-out {f3(c_pr.value)} [{f3(c_pr.ci_lo)}, {f3(c_pr.ci_hi)}]); ROC {f3(g.roc_auc.mean())} ± {f3(g.roc_auc.std())}; "
            f"ECE {f3(g.ece.mean())} ± {f3(g.ece.std())}; fold upper limits {f3(ups.min())}–{f3(ups.max())}", "all_runs.csv, E1_protocol_CIs.csv")

# reputation audit
ag = pd.read_csv(R / "E2_reputation_agreement.csv")
for _, r in ag.iterrows():
    put(f"5.3 agreement {r.reference}", f"n {int(r.n):,}; exact {r.exact_share:.1%}; MAE {r.mae:.3f}; r {r.pearson:.3f}", "E2_reputation_agreement.csv")
s1 = pd.read_csv(R / "S1_reputation_diff.csv")
for _, r in s1.iterrows():
    put(f"5.3 S1 {r.comparison}", f"{r.ap_diff:.4f} [{r.ci_lo:.4f}, {r.ci_hi:.4f}], p {r.boot_p:.3f}", "S1_reputation_diff.csv")
for tag in sorted(runs.tag[runs.tag.str.startswith(("E2|", "E2b|"))].unique()):
    for _, r in runs[runs.tag == tag].iterrows():
        put(f"Table 3b {tag} {r.model}", f"PR {f3(r.pr_auc)}; ROC {f3(r.roc_auc)}; ECE {f3(r.ece)}", "all_runs.csv")

# Table 4 and tests
h = runs[runs.tag == "E3|holdout|causalrep"]
for _, r in h.iterrows():
    put(f"Table 4 {r.model}", f"PR {f3(r.pr_auc)}; lift {f3(r.pr_auc_lift)}; ROC {f3(r.roc_auc)}; MCC {f3(r.mcc)}; Brier {f3(r.brier)}; "
        f"ECE {f3(r.ece)}; P@1% {f3(r['prec@1%'])}; P@5% {f3(r['prec@5%'])}; P@10% {f3(r['prec@10%'])}", "all_runs.csv")
T = pd.read_csv(R / "E3_E4_paired_tests.csv")
for _, r in T.iterrows():
    q = "<0.001" if r.bh_q < 0.001 else f"{r.bh_q:.3f}"
    put(f"Table 4 / 5.6 Δ {r.ref} vs {r.other}", f"{f3(r.ap_diff)} [{f3(r.ap_ci_lo)}, {f3(r.ap_ci_hi)}], BH q {q}", "E3_E4_paired_tests.csv")
s2 = pd.read_csv(R / "S2_P4_holdout_tests.csv")
for _, r in s2.iterrows():
    put(f"5.4 S2 lgbm vs {r.other} (P4 hold-out n {int(r.n):,}, prev {f3(r.prevalence)})",
        f"{f3(r.ap_ref)} vs {f3(r.ap_other)}; Δ {f3(r.ap_diff)} [{f3(r.ci_lo)}, {f3(r.ci_hi)}]; q {r.bh_q:.3g}", "S2_P4_holdout_tests.csv")
fr = pd.read_csv(R / "E3_friedman_P4.csv")
put("5.4 Friedman", f"chi2 {fr.chi2.iloc[0]:.1f}, df {int(fr.df.iloc[0])}, p {fr.p.iloc[0]:.2g}; ranks " +
    ", ".join(f"{m} {k:.1f}" for m, k in fr.sort_values("mean_rank")[["model", "mean_rank"]].values), "E3_friedman_P4.csv")

# calibration and drift
cal = pd.read_csv(R / "E3_calibration.csv")
for _, r in cal.iterrows():
    put(f"5.5 calibration {r.model} {r.calibration}", f"ECE {r.ece:.4f}; Brier {r.brier:.4f}; PR {f3(r.pr_auc)}", "E3_calibration.csv")
dr = pd.read_csv(R / "E3_daily_drift_frozen_model.csv")
put("5.5 drift ranges", f"n {dr.n.min():,}–{dr.n.max():,}; PR {f3(dr.pr_auc.min())}–{f3(dr.pr_auc.max())}; ROC {f3(dr.roc_auc.min())}–{f3(dr.roc_auc.max())}; "
    f"ECE {f3(dr.ece.min())}–{f3(dr.ece.max())}; prev {f3(dr.prevalence.min())}–{f3(dr.prevalence.max())}", "E3_daily_drift_frozen_model.csv")

# robustness
for tag in runs.tag[runs.tag.str.startswith("E5|")].unique():
    for _, r in runs[runs.tag == tag].iterrows():
        put(f"Table 5 {tag} {r.model}", f"n {int(r.n):,}; prev {f3(r.prevalence)}; PR {f3(r.pr_auc)}; lift {r.pr_auc_lift:.2f}; ROC {f3(r.roc_auc)}; ECE {f3(r.ece)}", "all_runs.csv")
sd = runs[runs.tag.str.startswith("E5|seed=")]
put("Table 5 five seeds", f"PR {sd.pr_auc.mean():.4f} ± {sd.pr_auc.std():.4f}; ROC {sd.roc_auc.mean():.4f} ± {sd.roc_auc.std():.4f}; ECE {sd.ece.mean():.4f} ± {sd.ece.std():.4f}", "all_runs.csv")

# importance
I = pd.read_csv(R / "E6_permutation_importance.csv", index_col=0)
for c in I.columns:
    top = I[c].sort_values(ascending=False).head(3)
    put(f"5.8 top-3 {c}", "; ".join(f"{k} {v:.3f}" for k, v in top.items()), "E6_permutation_importance.csv")
put("5.8 Kendall tau", f"{json.load(open(R / 'E6_summary.json'))['kendall_tau_P1_vs_P4']:.2f}", "E6_summary.json")

with open(R / "key_numbers.md", "w", encoding="utf-8") as fh:
    fh.write("| Manuscript location | Value | Source |\n|---|---|---|\n")
    for w, v, s in out:
        fh.write(f"| {w} | {v} | {s} |\n")
print(f"{len(out)} entries -> {R / 'key_numbers.md'}")
