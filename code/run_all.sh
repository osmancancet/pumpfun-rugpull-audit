#!/usr/bin/env bash
# Full reproduction. Expects the data in data/raw/pumpfun-launches (see README step 2).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../results && python -m pip freeze > ../results/environment.txt   # exact package versions (review R3, round 2)
python --version >> ../results/environment.txt
python verify_data.py
python s01_build_dataset.py
python s02_experiments.py
python s03_figures_tables.py
python s04_supplementary.py   # post hoc analyses added in internal review round 3 (S1, S2)
python s05_key_numbers.py     # every number the manuscript cites -> results/key_numbers.md
python s06_review_r6.py 2>&1 | tee ../results/log_s06.txt   # post hoc analyses of Section 5.9 -> results/R6_review_analyses.csv
python s06_tables.py          # Tables 7 and 8 -> results/table7_review_r6.md
