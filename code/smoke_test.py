"""SMOKE TEST ON SYNTHETIC DATA ONLY.

Checks the numpy implementations against brute-force definitions and runs the whole
pipeline end-to-end on a synthetic table. NOTHING produced here is a research result;
outputs go to results_smoke/ and must never be reported in the manuscript.
"""
import itertools, subprocess, sys
import numpy as np, pandas as pd
import config as C
import common as U

rng = np.random.default_rng(0)
ok = lambda c, msg: print(("PASS " if c else "FAIL ") + msg) or c
results = []

# ---------------------------------------------------------------- metric unit tests
y = rng.integers(0, 2, 400); s = np.round(rng.random(400) + 0.3 * y, 2)  # ties on purpose
pairs = [(i, j) for i in np.flatnonzero(y == 1) for j in np.flatnonzero(y == 0)]
brute = np.mean([1.0 if s[i] > s[j] else 0.5 if s[i] == s[j] else 0.0 for i, j in pairs])
results.append(ok(abs(U.roc_auc(y, s) - brute) < 1e-12, f"roc_auc == brute force ({brute:.4f})"))
# AP brute: mean over positives of precision at the score of that positive (ties grouped)
ap_b = np.mean([((s >= s[i]) & (y == 1)).sum() / (s >= s[i]).sum() for i in np.flatnonzero(y == 1)])
results.append(ok(abs(U.average_precision(y, s) - ap_b) < 1e-12, f"average_precision == brute force ({ap_b:.4f})"))
results.append(ok(U.mcc([1, 1, 0, 0], [1, 1, 0, 0]) == 1.0 and U.mcc([1, 0], [0, 1]) == -1.0, "mcc extremes"))
results.append(ok(U.ece(np.r_[np.ones(50), np.zeros(50)], np.full(100, 0.5)) < 1e-12, "ece of constant 0.5 on balanced = 0"))
a1, a2, d, se, z, p = U.delong_test(y, s, s)
results.append(ok(abs(d) < 1e-12, "delong: identical scores give zero difference"))
s2 = s + rng.normal(0, 0.3, len(s))
_, _, d, se, _, p = U.delong_test(y, s, s2)
boot = []
for b in range(300):
    ii = rng.integers(0, len(y), len(y)); boot.append(U.roc_auc(y[ii], s[ii]) - U.roc_auc(y[ii], s2[ii]))
results.append(ok(0.7 < se / np.std(boot) < 1.3, f"delong SE ~ bootstrap SE ({se:.4f} vs {np.std(boot):.4f})"))
q = U.benjamini_hochberg([0.01, 0.04, 0.03, 0.005])
results.append(ok(np.allclose(q, [0.02, 0.04, 0.04, 0.02]), f"BH q-values {np.round(q,3)}"))
b_, c_, pm = U.mcnemar_test([1]*10, [1]*10, [0]*10)
results.append(ok(b_ == 10 and c_ == 0 and pm < 0.01, f"mcnemar exact p={pm:.4f}"))

# ---------------------------------------------------------------- causal reputation vs brute force
n = 600
toy = pd.DataFrame({"creator": rng.integers(0, 40, n), "t0": np.sort(rng.integers(0, 20000, n)).astype(float)})
toy["rugged"] = np.where(rng.random(n) < 0.1, np.nan, (rng.random(n) < 0.6).astype(float))
toy["graduated"] = (rng.random(n) < 0.05).astype(float)
toy["rug_dt_s"] = np.where(toy.rugged == 1, rng.integers(1, 8000, n), np.nan)      # some rugs after the embargo
toy["migrate_dt_s"] = np.where(toy.graduated == 1, rng.integers(60, 8000, n), np.nan)
E = 3600
rep = U.causal_reputation(toy, E); orc = U.causal_reputation(toy, E, oracle=True)
leg = U.causal_reputation(toy, E, strict=False)
bad = bad_o = bad_l = 0
for i, r in toy.iterrows():
    prev = toy[(toy.creator == r.creator) & (toy.t0 < r.t0)]
    known = prev.rugged.notna().to_numpy()
    early = ((prev.rugged == 1) & (prev.rug_dt_s <= E)).to_numpy()
    # strict: resolve at min(rug time, E) with the "within E" labels
    tout = np.where(early, prev.t0 + prev.rug_dt_s, prev.t0 + E)
    m_ = known & (tout < r.t0)
    exp_rug = early[m_].mean() if m_.any() else np.nan
    dres = np.where(early, prev.rug_dt_s, E)
    g_ = ((prev.graduated == 1) & (prev.migrate_dt_s <= dres)).to_numpy()
    exp_grad = g_[m_].mean() if m_.any() else np.nan
    got = rep.loc[i]
    same = lambda a, b: np.isclose(a, b) or (np.isnan(a) and np.isnan(b))
    if got.c_rep_n != len(prev) or got.c_rep_n_res != m_.sum() or not same(got.c_rep_rug, exp_rug) or not same(got.c_rep_grad, exp_grad):
        bad += 1
    # legacy (first full run): late rugs stay unresolved until their rug time
    tl = np.where(prev.rugged == 1, prev.t0 + prev.rug_dt_s, prev.t0 + E)
    res = prev[known & (tl < r.t0)]
    if leg.loc[i, "c_rep_n_res"] != len(res) or not same(leg.loc[i, "c_rep_rug"], res.rugged.mean() if len(res) else np.nan):
        bad_l += 1
    eo = early[known].mean() if known.any() else np.nan     # oracle: same "within E" label, credited at launch
    if not same(orc.loc[i, "c_rep_rug"], eo):
        bad_o += 1
results.append(ok(bad == 0, f"causal_reputation (strict) == brute force on {n} launches (mismatches={bad})"))
results.append(ok(bad_l == 0, f"causal_reputation (strict=False, first run) == brute force (mismatches={bad_l})"))
results.append(ok(bad_o == 0, f"oracle reputation == brute force (mismatches={bad_o})"))
yb = np.r_[np.ones(30), np.zeros(70)]; sb = np.full(100, 0.5)
results.append(ok(abs(U.precision_at_budget(yb, sb, 0.05) - 0.3) < 1e-12, "precision_at_budget is tie-aware (constant score -> prevalence)"))
results.append(ok(((rep.c_rep_n_res <= rep.c_rep_n)).all(), "resolved history never exceeds launch history"))

# ---------------------------------------------------------------- splits
g = rng.integers(0, 300, 5000)
tr, te = U.split_group(g, 0.2, 1)
results.append(ok(len(set(g[tr]) & set(g[te])) == 0, "creator-grouped split is creator-disjoint"))
days = [f"d{i:02d}" for i in range(26)]
folds = U.forward_folds(days, 14, 2, 1)
results.append(ok(all(max(a) < min(b) and days.index(min(b)) - days.index(max(a)) == 2 for a, b in folds),
                  f"forward folds strictly ordered with 1-day purge ({len(folds)} folds)"))

# ---------------------------------------------------------------- end-to-end on synthetic launches
N = 30000; ncre = 6000
cre = rng.zipf(1.6, N) % ncre                                   # heavy-tailed: a few serial launchers
propensity = rng.beta(2, 1.3, ncre)                             # creator-level rug tendency
t0 = np.sort(rng.uniform(pd.Timestamp("2026-09-27", tz="UTC").timestamp(), pd.Timestamp("2026-10-23", tz="UTC").timestamp(), N))
mayhem = (rng.random(N) < 0.3).astype(int)
dev_share = np.clip(rng.beta(1, 8, N) + 0.1 * propensity[cre], 0, 1)
insider = np.clip(rng.beta(1, 6, N) + 0.05 * mayhem, 0, 1)
logit = -0.4 + 2.5 * (propensity[cre] - 0.6) + 3 * dev_share + 1.5 * insider + 1.2 * mayhem + rng.normal(0, 1, N)
rug = (rng.random(N) < 1 / (1 + np.exp(-logit))).astype(float)
rug[rng.random(N) < 0.05] = np.nan
rdt = np.where(rug == 1, rng.exponential(200, N) + 1, np.nan)
syn = pd.DataFrame({"mint": [f"m{i}" for i in range(N)], "creator": [f"c{c}" for c in cre], "t0": t0,
    "quote_asset": np.where(rng.random(N) < 0.97, "sol", "usdc"), "decoder_complete": 1, "mayhem": mayhem,
    "rugged": rug, "rug_dt_s": rdt, "graduated": (rng.random(N) < 0.03).astype(float),
    "migrate_dt_s": np.nan, "f10_dev_share": dev_share, "f10_insider_share": insider,
    "f10_bundle_wallets": rng.poisson(1 + 3 * insider), "f10_rs": rng.gamma(2, 1, N), "f10_n_buys": rng.poisson(3, N),
    "f10_age": rng.uniform(0, 9.9, N), "dev_buy_sol": rng.gamma(1, 1, N), "dev_share": dev_share,
    "create_lag_s": rng.exponential(0.3, N), "silence_3s": (rng.random(N) < 0.02).astype(int),
    "peak_rs": rng.gamma(2, 3, N), "terminal_rs": rng.gamma(1, 1, N),
    "rug_branch_inferred": np.where(rug == 1, np.where(rng.random(N) < 0.7, "dev_dump_or_recovered", "drain"), None),
    "features_basis": "tape_replay", "subset": np.where(t0 < pd.Timestamp("2026-09-30", tz="UTC").timestamp(), "launches_legacy", "launches")})
# synthetic "vendor" reputation = look-ahead version, to check that the audit detects it
o = U.causal_reputation(syn[syn.quote_asset == "sol"], 3600, oracle=True)
syn = syn.join(o.rename(columns={"c_rep_n_res": "f10_rep_n", "c_rep_rug": "f10_rep_rug", "c_rep_grad": "f10_rep_grad"})[["f10_rep_n", "f10_rep_rug", "f10_rep_grad"]])
import s01_build_dataset as B
d, lg, flow = B.build(syn)
out = C.ROOT / "results_smoke"; out.mkdir(exist_ok=True)
B.report(d, flow, out)
d.to_pickle(out / "analysis.pkl"); syn.to_pickle(out / "syn_raw.pkl")
r = subprocess.run([sys.executable, "s02_experiments.py", "--smoke"], capture_output=True, text=True)
print(r.stdout[-400:], r.stderr[-2000:])
results.append(ok(r.returncode == 0, "s02_experiments.py --smoke runs end-to-end"))
if r.returncode == 0:
    a = pd.read_csv(out / "E2_reputation_agreement.csv")
    results.append(ok(a.loc[a.reference == "o_rep_rug", "exact_share"].iloc[0] > a.loc[a.reference == "c_rep_rug", "exact_share"].iloc[0],
                      "audit flags a look-ahead reputation field (synthetic oracle) as closer to oracle than to causal"))
r7 = subprocess.run([sys.executable, "s07_chatbot_review.py", "--smoke"], capture_output=True, text=True)
print(r7.stdout[-400:], r7.stderr[-2000:])
results.append(ok(r7.returncode == 0, "s07_chatbot_review.py --smoke runs end-to-end"))
if r7.returncode == 0:
    r = pd.read_csv(out / "R7_chatbot_review.csv"); m = r[r.block == "M"].iloc[0]
    results.append(ok(m.n == m.actionable_n + m.fast_rug_n and m.check_actionable == m.actionable_n,
                      "full-stream cohort = actionable cohort + fast rugs"))
print(f"\n{sum(results)}/{len(results)} checks passed (synthetic data; not research results)")
sys.exit(0 if all(results) else 1)
