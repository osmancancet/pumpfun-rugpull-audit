"""Figures and manuscript tables from results/*.csv (run after s02_experiments.py)."""
import json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C

R = C.RESULTS; F = C.FIGURES; F.mkdir(parents=True, exist_ok=True)
runs = pd.read_csv(R / "all_runs.csv")
summ = json.load(open(R / "E6_summary.json")); best = summ["best_model"]
plt.rcParams.update({"font.size": 8, "figure.dpi": 300, "savefig.dpi": 600, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                     "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "axes.grid": True, "grid.color": "#e4e3df", "grid.linewidth": 0.5, "axes.axisbelow": True,
                     "legend.frameon": False})
# Two categorical slots (validated: CVD dE >= 8 on the adjacent pair) + marker shape as secondary encoding
COL = {"vendorrep": "#2a78d6", "causalrep": "#eb6834"}
MRK = {"vendorrep": "o", "causalrep": "s"}
LAB = {"vendorrep": "published reputation", "causalrep": "causal reputation"}
INK2 = "#52514e"

def save(fig, name):
    fig.savefig(F / f"{name}.png", bbox_inches="tight"); fig.savefig(F / f"{name}.pdf", bbox_inches="tight"); plt.close(fig)

# Fig 2: protocol inflation. Point = estimate, bar = 95% creator-clustered bootstrap CI.
# P1/P2: one split. P3/P4: five forward folds (small, light) plus the hold-out fold (large).
e1 = runs[runs.tag.str.startswith("E1")].copy()
e1["protocol"] = e1.tag.str.split("|").str[1]; e1["reps"] = e1.tag.str.split("|").str[2]
g = e1[e1.model == best].groupby(["protocol", "reps"]).agg(pr=("pr_auc", "mean"), pr_sd=("pr_auc", "std"),
                                                          roc=("roc_auc", "mean"), roc_sd=("roc_auc", "std")).reset_index()
order = ["P1_random_mint", "P2_creator_grouped", "P3_time_forward", "P4_time_unseen_creator"]
prev = e1[e1.model == best].groupby("protocol").prevalence.mean().reindex(order)
ci = pd.read_csv(R / "E1_protocol_CIs.csv")
ci["protocol"] = ci.tag.str.split("|").str[1]; ci["reps"] = ci.tag.str.split("|").str[2]
ci["fold"] = ci.tag.str.extract(r"fold(\d+)$")[0].astype(float)
last = ci.fold.max()
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
for ax, metric, lab in [(axes[0], "pr_auc", "PR-AUC"), (axes[1], "roc_auc", "ROC-AUC")]:
    for k, rp in enumerate(["vendorrep", "causalrep"]):
        for i, pr in enumerate(order):
            sub = ci[(ci.metric == metric) & (ci.reps == rp) & (ci.protocol == pr)]
            x0 = i + (k - 0.5) * 0.32
            main = sub if sub.fold.isna().all() else sub[sub.fold == last]
            other = sub[sub.fold.notna() & (sub.fold != last)]
            for j, (_, r) in enumerate(other.iterrows()):
                ax.plot(x0 - 0.06 + 0.03 * j, r.value, MRK[rp], ms=2.5, color=COL[rp], alpha=0.45, mec="none")
            if main.empty:
                continue
            r = main.iloc[0]
            ax.errorbar(x0 + 0.07 if len(other) else x0, r.value, yerr=[[r.value - r.ci_lo], [r.ci_hi - r.value]],
                        fmt=MRK[rp], ms=4.5, color=COL[rp], mec="white", mew=0.6, elinewidth=1.2, capsize=0,
                        label=LAB[rp] if i == 0 else None)
    ax.set_xticks(range(4), [f"P1 random\nprev. {prev.iloc[0]:.2f}", f"P2 creator\nprev. {prev.iloc[1]:.2f}",
                             f"P3 time\nprev. {prev.iloc[2]:.2f}", f"P4 unseen\nprev. {prev.iloc[3]:.2f}"])
    ax.tick_params(axis="x", length=0); ax.grid(axis="x", visible=False)
    ax.set_ylabel(lab); ax.set_xlim(-0.6, 3.6)
axes[0].legend(loc="lower left", fontsize=7, handletextpad=0.3)
fig.tight_layout(); save(fig, "fig2_protocol_inflation")

# Fig 3: reliability diagram (raw scores) with the number of hold-out launches per bin
rel = pd.read_csv(R / f"E3_reliability_{best}.csv")
fig, (ax, axh) = plt.subplots(2, 1, figsize=(3.4, 3.8), sharex=True, gridspec_kw={"height_ratios": [3, 1], "hspace": 0.08})
ax.plot([0, 1], [0, 1], color=INK2, lw=0.8, ls=(0, (3, 2)))
ax.plot(rel.mean_p, rel.frac_pos, "-o", color=COL["causalrep"], lw=1.5, ms=4, mec="white", mew=0.6)
ax.text(0.02, 0.93, "dashed diagonal = perfect calibration", color=INK2, fontsize=7)
ax.set_ylabel("Observed rug rate (300 s)"); ax.set_ylim(-0.02, 1.02)
axh.bar(rel.mean_p, rel.n / 1000, width=0.07, color="#b9b8b2", edgecolor="none")
axh.set_ylabel("launches\n(thousands)", fontsize=7); axh.set_xlabel("Predicted probability"); axh.set_xlim(-0.02, 1.02)
save(fig, "fig3_reliability")

# Fig 4: frozen-model daily metrics as small multiples (one scale per panel, no dual axis)
dr = pd.read_csv(R / "E3_daily_drift_frozen_model.csv"); dd = pd.to_datetime(dr.day)
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.4), sharex=True)
axs[0].plot(dd, dr.pr_auc, "-o", color=COL["vendorrep"], lw=1.5, ms=3, mec="white", mew=0.5)
axs[0].plot(dd, dr.roc_auc, "-s", color=COL["causalrep"], lw=1.5, ms=3, mec="white", mew=0.5)
axs[0].text(dd.iloc[-1], dr.pr_auc.iloc[-1] + 0.004, "PR-AUC", ha="right", va="bottom", fontsize=7, color="#0b0b0b")
axs[0].text(dd.iloc[-1], dr.roc_auc.iloc[-1] - 0.004, "ROC-AUC", ha="right", va="top", fontsize=7, color="#0b0b0b")
lo_ = min(dr.pr_auc.min(), dr.roc_auc.min()); hi_ = max(dr.pr_auc.max(), dr.roc_auc.max())
axs[0].set_ylim(lo_ - 0.02, min(1, hi_ + 0.015)); axs[0].set_title("(a) ranking", loc="left", fontsize=8)
axs[1].plot(dd, dr.ece, "-o", color="#0b0b0b", lw=1.2, ms=3, mec="white", mew=0.5)
axs[1].set_ylim(0, dr.ece.max() * 1.5); axs[1].set_title("(b) ECE", loc="left", fontsize=8)
axs[2].plot(dd, dr.prevalence, "-o", color="#0b0b0b", lw=1.2, ms=3, mec="white", mew=0.5)
axs[2].set_ylim(dr.prevalence.min() - 0.05, dr.prevalence.max() + 0.03); axs[2].set_title("(c) rug prevalence (300 s)", loc="left", fontsize=8)
import matplotlib.dates as mdates
for ax in axs:
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    for _, r in dr[dr.multihop_seam == 1].iterrows():
        ax.axvspan(pd.to_datetime(r.day), pd.to_datetime(r.day) + pd.Timedelta(days=1), color="#b9b8b2", alpha=0.3)
fig.tight_layout(); save(fig, "fig4_daily_drift")

# Fig 5: permutation importance, P1 -> P4 dumbbell per feature (published reputation features)
NICE = {"f10_dev_share": "creator share at snapshot", "f10_insider_share": "insider share", "f10_bundle_wallets": "bundle wallets",
        "f10_rs": "real SOL reserves", "f10_n_buys": "number of buys", "f10_age": "snapshot age", "dev_buy_sol": "developer buy (SOL)",
        "dev_share": "creator share after first buy", "mayhem": "mayhem flag", "f10_rep_n": "published launch count",
        "f10_rep_rug": "published rug share", "f10_rep_grad": "published graduation share",
        "f10_rep_rug_missing": "no published history"}
I = pd.read_csv(R / "E6_permutation_importance.csv", index_col=0)
I = I.sort_values(I.columns[1])
fig, ax = plt.subplots(figsize=(4.6, 3.6))
y = np.arange(len(I))
ax.hlines(y, I.iloc[:, 0], I.iloc[:, 1], color="#b9b8b2", lw=1.5)
ax.plot(I.iloc[:, 0], y, "o", color=COL["vendorrep"], ms=5, mec="white", mew=0.6, label="P1 random mint")
ax.plot(I.iloc[:, 1], y, "s", color=COL["causalrep"], ms=5, mec="white", mew=0.6, label="P4 time-forward, unseen creators")
ax.axvline(0, color=INK2, lw=0.6)
ax.set_yticks(y, [NICE.get(c, c) for c in I.index]); ax.grid(axis="y", visible=False)
ax.set_xlabel("PR-AUC drop when the feature is permuted"); ax.legend(loc="lower right", fontsize=7)
fig.tight_layout(); save(fig, "fig5_importance_shift")

# Tables (markdown, pasted into the manuscript)
def md(df, path):
    open(R / path, "w").write(df.to_markdown(index=False, floatfmt=".3f"))
md(pd.read_csv(R / "flow.csv"), "table_flow.md")
md(g, "table2_protocols.md")
md(runs[runs.tag == "E3|holdout|causalrep"][["model", "pr_auc", "pr_auc_lift", "roc_auc", "mcc", "brier", "ece", "prec@1%", "prec@5%"]], "table3_models.md")
md(pd.read_csv(R / "E3_E4_paired_tests.csv"), "table4_tests.md")
md(runs[runs.tag.str.startswith(("E2|", "E2b|"))][["tag", "model", "pr_auc", "roc_auc", "ece"]], "table5_reputation.md")
md(pd.read_csv(R / "E2_reputation_agreement.csv"), "table5b_rep_agreement.md")
md(runs[runs.tag.str.startswith("E5|")][["tag", "model", "n", "prevalence", "pr_auc", "pr_auc_lift", "roc_auc", "ece"]], "table6_robustness.md")
print("figures ->", F, "| tables ->", R)
