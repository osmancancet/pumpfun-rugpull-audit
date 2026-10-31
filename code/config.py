"""Single source of truth for paths, seeds and protocol constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # /workspace/makale
DATA_RAW = ROOT / "data" / "raw" / "pumpfun-launches"
DATA_PROC = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

HF_REPO = "loopholetape/pumpfun-launches"            # CC BY 4.0
HF_REVISION = "022649eb0504005be0ae34833d224341777355be"                                 # set to a commit hash to freeze the release used in the paper

SEED = 20261030                                       # global seed; every stochastic step derives from it
N_BOOT = 2000                                         # bootstrap replicates for CIs
ALPHA = 0.05

# Decision time: a prediction is issued at the first snapshot under 10 s (f10_*); the
# primary target is a rug within 300 s of launch that happens AFTER that snapshot.
PRIMARY_TARGET = "y_rug300"
HORIZON_S = 300

# Data-quality filters (dataset card, Known issues KI-01..KI-18)
MAX_CREATE_LAG_S = 1.0      # above 1 s the f10 snapshot is not the true early state
MAX_SILENCE_3S = 0.0        # strict: no capture silence in the first 3 s (sensitivity: relax)
SEAM_MULTIHOP = ("2026-10-08T16:20:00Z", "2026-10-09T16:51:21Z")   # KI-18
SEAM_LEGS = "2026-10-06T03:46:40Z"                                  # legs/fee sweeps
SEAM_DECODER = "2026-09-27T00:18:34Z"                               # KI-02

# Embargo used when a creator's earlier launch counts as "resolved" for the causal reputation
# (path closure needs >= 10 min quiet for migrated curves and 1 h for curves under 1 SOL).
REP_EMBARGO_S = 3600
REP_EMBARGO_SENS = (600, 86400)   # sensitivity of the causal reputation to the embargo (E2b)
REP_STRICT = True                 # resolve every launch at min(rug time, embargo); False = first full run (see common.causal_reputation)

# Temporal protocol: days 2026-09-27..2026-10-22 (26 UTC days)
TRAIN_DAYS = 14            # expanding/rolling window length for forward folds
VAL_DAYS = 2
TEST_DAYS = 2
GAP_DAYS = 1               # purge gap between train/val and test (outcomes settle up to ~1 h; 1 day is conservative)

ALERT_BUDGETS = (0.01, 0.05, 0.10)    # share of launches an analyst/wallet could flag
