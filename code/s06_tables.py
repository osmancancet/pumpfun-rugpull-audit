"""Markdown tables for the round-6 post hoc analyses, read from results/R6_review_analyses.csv."""
import pandas as pd, config as C
R = pd.read_csv(C.RESULTS / "R6_review_analyses.csv")
def row(what): return R[R.what == what].iloc[0]
f3 = lambda x: f"{x:.3f}"
T7 = [("Lead time: rugs ≥ 30 s after the snapshot vs all non-rugs", "rugs leaving >= 30 s after the snapshot vs non-rugs"),
      ("Lead time: rugs ≥ 60 s after the snapshot vs all non-rugs", "rugs leaving >= 60 s after the snapshot vs non-rugs"),
      ("Peak reserves ≥ 1 SOL", "peak reserves >= 1 SOL"), ("Peak reserves ≥ 5 SOL", "peak reserves >= 5 SOL"),
      ("P1 test, creator seen in P1 training", "P1 test, creator seen in P1 training"),
      ("P1 test, creator unseen in P1 training", "P1 test, creator unseen in P1 training"),
      ("P3 hold-out, creator seen in training", "P3 hold-out, creator seen in training"),
      ("P3 hold-out, creator unseen (= P4)", "P3 hold-out, creator unseen in training (= P4)"),
      ("Classic launches only, P1", "P1 random mint, classic"), ("Classic launches only, P4 hold-out", "P4 hold-out, classic"),
      ("Mayhem hold-out, trained on classic", "mayhem hold-out, trained on classic"),
      ("Mayhem hold-out, trained on mayhem", "mayhem hold-out, trained on mayhem"),
      ("Mayhem hold-out, pooled training", "mayhem hold-out, pooled (all training launches)"),
      ("DRAIN label, one-feature reserves rule", "y_rug_drain, reserves rule (f10_rs)"),
      ("collapse90 label, one-feature reserves rule", "y_collapse90, reserves rule (f10_rs)"),
      ("Logistic scorecard (reputation, creator and insider share), hold-out", "scorecard (logistic, 3 features), hold-out"),
      ("Logistic scorecard, P4 hold-out", "scorecard (logistic, 3 features), P4 hold-out")]
out = ["| Analysis | n (test) | Prevalence | PR-AUC [95% CI] | ROC-AUC [95% CI] |", "|---|---|---|---|---|"]
for lab, w in T7:
    r = row(w); out.append(f"| {lab} | {r.n:,} | {f3(r.prevalence)} | {f3(r.pr_auc)} [{f3(r.pr_lo)}, {f3(r.pr_hi)}] | {f3(r.roc_auc)} [{f3(r.roc_lo)}, {f3(r.roc_hi)}] |")
out += ["", "| Threshold set on the validation days | Share flagged (test) | Precision | Recall | MCC | Rugs among unflagged | Graduated tokens flagged |", "|---|---|---|---|---|---|---|"]
for lab in ["training-prevalence share", "budget 10%", "budget 5%", "budget 1%"]:
    r = row(f"threshold from validation days, {lab}")
    out.append(f"| {lab.replace('budget', 'Budget').replace('training', 'Training')} | {f3(r.flag_rate_test)} | {f3(r.precision)} | {f3(r.recall)} | {f3(r.mcc)} | {f3(r.false_safe_rate)} | {f3(r.graduated_flagged)} of {int(r.n_graduated)} |")
(C.RESULTS / "table7_review_r6.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
