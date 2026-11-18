# Leakage-aware evaluation of early rug-pull prediction on pump.fun (Solana)

Code accompanying the manuscript "Seen creators, settled labels: a leakage-aware audit of early
rug-pull prediction for Solana pump.fun memecoins" (O. C. Çetlenbik).

**Status (2026-11-18, fourth full run):** `results/` holds the run of record with the actionable primary target
(`config.MIN_LEAD_S = 60`: launches that rug less than 60 s after the snapshot are excluded from the analysis set but still
count in creator histories), on dataset revision 022649eb0504005be0ae34833d224341777355be (Python 3.9.6, macOS arm64;
package versions in `results/environment.txt`). The console output is in `results/log_run_of_record.txt` and
`results/log_s06.txt`, and the unit-test output in `results/log_smoke.txt`. `results_target0/` keeps the third full run
with the earlier full-stream target (rug within 300 s of launch, after the snapshot); the manuscript uses it only in
its Table 9. All 53 day files of the `launches` and `launches_legacy` subsets match the SHA-256 values in the dataset card.
Every number in the manuscript is copied from `results/key_numbers.md` (whose table labels follow the earlier table
numbering) or, for Section 5.9, from `results/R6_review_analyses.csv`. `smoke_test.py` (17/17 pass) checks the code on
**synthetic** data only; its outputs
(`results_smoke/`) are not research results.

On macOS, LightGBM needs OpenMP (`brew install libomp`). With huggingface_hub 1.x the download command is `hf download`
(see step 2); `verify_data.py` needs the dataset card `README.md` next to the day files.

## 1. Environment
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Data (public, CC BY 4.0, no account or token needed)
Dataset: loopholetape, *pump.fun launches with outcomes* (2026),
https://huggingface.co/datasets/loopholetape/pumpfun-launches

Put the files under `../data/raw/pumpfun-launches/`, keeping the repo layout
(`README.md`, `data/launches/*.parquet`, `data/launches_legacy/*.parquet`). For example:
```bash
REV=022649eb0504005be0ae34833d224341777355be
hf download loopholetape/pumpfun-launches --repo-type dataset --revision $REV \
  --include "data/launches/*" --include "data/launches_legacy/*" --local-dir ../data/raw/pumpfun-launches
hf download loopholetape/pumpfun-launches README.md KNOWN_ISSUES.md --repo-type dataset --revision $REV \
  --local-dir ../data/raw/pumpfun-launches
```
Write down the commit hash you downloaded and set `HF_REVISION` in `config.py` so the release is frozen.
Only the free, public parquet files are used. None of the vendor's paid API endpoints are used.
The free-text fields `name`, `symbol` and `uri` are dropped on load and never read.
They are attacker-controlled (KI-14).

## 3. Run
```bash
python smoke_test.py          # optional: unit tests + synthetic end-to-end run (about 10 s)
bash run_all.sh               # verify sha256 -> build table -> experiments -> figures/tables
```
Outputs: `../results/*.csv|md|json`, `../results/key_numbers.md` and `../figures/fig2..fig5*.png|pdf`.
Global seed `20261030` (`config.py`). The pipeline is deterministic given the data revision and
library versions.

## 4. What each script does
| script | purpose |
|---|---|
| `config.py` | paths, seed, horizons, seams, filters, fold sizes |
| `common.py` | numpy-only metrics (ROC-AUC, AP, MCC, Brier, ECE), DeLong, McNemar, BH, creator-cluster bootstrap, Friedman, splits, **causal creator reputation** (vectorised, embargoed) |
| `models.py` | prior, one-feature rule baselines, logistic regression, random forest, HistGradientBoosting, LightGBM |
| `s01_build_dataset.py` | filters per the dataset's known issues (KI-01/02/03/08/11/12/14), decision-time features, targets and label variants, seam flags, exclusion flow |
| `s02_experiments.py` | E1 protocol inflation (P1–P4); E2 reputation look-ahead audit; E3 baselines, paired tests, calibration, drift, Friedman; E4 ablation; E5 robustness (labels, mayhem, seams, silence, first-time vs repeat creators, seeds, legacy/sampled transfer); E6 importance stability |
| `s03_figures_tables.py` | figures 2–5 and markdown tables for the manuscript |
| `s05_key_numbers.py` | every number the manuscript cites, with its source file -> `results/key_numbers.md` |
| `s04_supplementary.py` | post hoc (round 3): S1 published/oracle/no reputation minus causal (paired clustered bootstrap); S2 LightGBM vs all scorers on the P4 hold-out with BH |
| `s06_review_r6.py` | post hoc (17 Nov 2026): lead time, peak-reserve subsets, validation-fixed thresholds, P4 majority class, classic-only runs, matched populations, mayhem intervals, drift slope, reserves rule, discordant-subset audit, scorecard -> `results/R6_review_analyses.csv` (log `results/log_s06.txt`) |
| `s06_tables.py` | Tables 7 and 8 of the manuscript -> `results/table7_review_r6.md` |
| `crosscheck_rpc.py` | read-only public-RPC check of creator, timing and mint metadata for 8 random launches |
| `verify_data.py` | offline sha256 check against the dataset card |

## 5. Filling the manuscript
Every `[SONUÇ BEKLENİYOR]` placeholder in the manuscript names the results file it comes from
(e.g. `results/table3_models.md`). Copy the values from there. Do not edit them by hand.

## Revisions after the internal (simulated) review
- BH is applied within pre-specified families: the primary family is the clustered-bootstrap PR-AUC tests (`bh_q`); DeLong (`delong_bh_q`) and McNemar (`mcnemar_bh_q`) are adjusted separately.
- The McNemar operating point uses the training prevalence (no test labels).
- LightGBM is the pre-specified reference learner (`best = MODELS_ML[-1]`), with histogram gradient boosting as the fallback.
- E2b embargo sensitivity: `config.REP_EMBARGO_SENS = (600, 86400)`.
- `run_all.sh` writes `results/environment.txt` (pip freeze and the Python version).
- Smoke test after the round 1–3 revisions: 15/15 PASS on synthetic data. These are not research results.

## Round 4 changes (independent audit, 2026-10-30)
- `common.causal_reputation(strict=True)` (`config.REP_STRICT`): every earlier launch resolves at t0 + min(rug time, embargo)
  and is credited with "rugged within the embargo" and "graduated by its resolution time". In the first run a launch that
  rugged after the embargo stayed out of the history until its rug time, so history membership depended on the future,
  and graduation used the final label. Negative lags are clipped; a missing migration-time column raises a warning.
  `strict=False` reproduces the first run.
- The oracle reputation uses the same labels, credited at launch time, so it differs from the causal one only in timing.
- `models.REP["oracle"]` now has the same five columns as `REP["causal"]` (it had four extra causal count columns).
- `precision_at_budget` is tie-aware (ties at the cut-off enter in expectation); before, the prevalence predictor and the
  binned rules depended on row order.
- The legacy transfer set uses the cohort filters (create lag, snapshot age, migration before the snapshot).
- Embargo sensitivity values are read from `config.REP_EMBARGO_SENS` everywhere; `s04` uses the same reference learner as `s02`.
- Figures 2–5 redrawn (interval plot, small multiples, dumbbell; PNG and PDF); `s05_key_numbers.py` added to `run_all.sh`.
- Smoke test: 17/17 PASS on synthetic data, including brute-force checks of the strict and first-run reputation and the
  tie-aware budget precision.
