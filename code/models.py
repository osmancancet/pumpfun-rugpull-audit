"""Model zoo. scikit-learn/LightGBM are used when installed; a numpy logistic regression
and the rule baselines are always available (so the pipeline can be smoke-tested)."""
from __future__ import annotations
import numpy as np, pandas as pd
import config as C

BASE = ["f10_dev_share", "f10_insider_share", "f10_bundle_wallets", "f10_rs", "f10_n_buys",
        "f10_age", "dev_buy_sol", "dev_share", "mayhem"]
HOLDER = ["f10_dev_share", "f10_insider_share", "f10_bundle_wallets", "dev_share"]
FLOW = ["f10_rs", "f10_n_buys", "f10_age", "dev_buy_sol"]
REP = {"vendor": ["f10_rep_n", "f10_rep_rug", "f10_rep_grad", "f10_rep_rug_missing"],
       "causal": ["c_rep_n", "c_rep_n_res", "c_rep_rug", "c_rep_grad", "c_rep_rug_missing"],
       "oracle": ["o_rep_n", "o_rep_n_res", "o_rep_rug", "o_rep_grad", "o_rep_rug_missing"],   # same 5 columns as "causal"
       "none": []}
for _e in C.REP_EMBARGO_SENS:
    REP[f"causal_e{_e}"] = [f"e{_e}_rep_n", f"e{_e}_rep_n_res", f"e{_e}_rep_rug", f"e{_e}_rep_grad", f"e{_e}_rep_rug_missing"]

def feature_set(rep="causal", drop=()):
    cols = [c for c in BASE + REP[rep] if c not in set(drop)]
    return cols

# ------------------------------------------------------------------ preprocessing
class Prep:
    """Train-fitted median imputation + log1p of count-like columns + standardisation (for LR)."""
    LOG = {"f10_bundle_wallets", "f10_n_buys", "f10_rep_n", "c_rep_n", "c_rep_n_res", "o_rep_n", "o_rep_n_res",
           "dev_buy_sol", "f10_rs"} | {f"e{_e}_rep_{k}" for _e in C.REP_EMBARGO_SENS for k in ("n", "n_res")}
    def fit(self, X: pd.DataFrame):
        self.cols = list(X.columns)
        Z = self._log(X)
        self.med = Z.median(numeric_only=True).fillna(0)
        Z = Z.fillna(self.med)
        self.mu = Z.mean(); self.sd = Z.std().replace(0, 1).fillna(1)
        return self
    def _log(self, X):
        Z = X.astype(float).copy()
        for c in Z.columns:
            if c in self.LOG:
                Z[c] = np.log1p(Z[c].clip(lower=0))
        return Z
    def transform(self, X, scale=True):
        Z = self._log(X[self.cols]).fillna(self.med)
        return ((Z - self.mu) / self.sd).to_numpy() if scale else Z.to_numpy()

class NumpyLogit:
    """L2-penalised logistic regression by Newton/IRLS (fallback when sklearn is absent)."""
    def __init__(self, l2=1.0, iters=50):
        self.l2, self.iters = l2, iters
    def fit(self, X, y):
        X1 = np.c_[np.ones(len(X)), X]; w = np.zeros(X1.shape[1])
        R = np.eye(X1.shape[1]) * self.l2; R[0, 0] = 0
        for _ in range(self.iters):
            p = 1 / (1 + np.exp(-np.clip(X1 @ w, -30, 30)))
            g = X1.T @ (p - y) + R @ w
            H = (X1 * (p * (1 - p))[:, None]).T @ X1 + R
            step = np.linalg.solve(H + 1e-9 * np.eye(len(w)), g); w -= step
            if np.abs(step).max() < 1e-7:
                break
        self.w = w; return self
    def predict_proba(self, X):
        p = 1 / (1 + np.exp(-np.clip(np.c_[np.ones(len(X)), X] @ self.w, -30, 30)))
        return np.c_[1 - p, p]

# ------------------------------------------------------------------ registry
def make_model(name, seed):
    if name == "logreg":
        try:
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(C=1.0, max_iter=2000, random_state=seed), True
        except ImportError:
            return NumpyLogit(l2=1.0), True
    if name == "rf":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(n_estimators=300, min_samples_leaf=50, max_features="sqrt",
                                      n_jobs=-1, random_state=seed), False
    if name == "hgb":
        from sklearn.ensemble import HistGradientBoostingClassifier
        return HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=63,
                                              min_samples_leaf=200, l2_regularization=1.0,
                                              early_stopping=True, validation_fraction=0.1,
                                              random_state=seed), False
    if name == "lgbm":
        import lightgbm as lgb
        return lgb.LGBMClassifier(n_estimators=600, learning_rate=0.05, num_leaves=63,
                                  min_child_samples=200, subsample=0.8, subsample_freq=1,
                                  colsample_bytree=0.8, reg_lambda=1.0, random_state=seed,
                                  n_jobs=-1, verbose=-1), False
    raise KeyError(name)

def available_models():
    names = ["logreg"]
    try:
        import sklearn  # noqa
        names += ["rf", "hgb"]
    except ImportError:
        pass
    try:
        import lightgbm  # noqa
        names += ["lgbm"]
    except ImportError:
        pass
    return names

def fit_predict(name, Xtr, ytr, Xte, seed):
    """Returns test scores in [0,1]. Rules are fitted only on training data."""
    if name == "prior":
        return np.full(len(Xte), ytr.mean())
    if name.startswith("rule_"):
        col = {"rule_rep": "c_rep_rug", "rule_rep_vendor": "f10_rep_rug",
               "rule_dev": "f10_dev_share", "rule_insider": "f10_insider_share",
               "rule_mayhem": "mayhem", **{f"rule_rep_e{e}": f"e{e}_rep_rug" for e in C.REP_EMBARGO_SENS}}[name]
        return _rule_scores(Xtr[col].to_numpy(float), ytr, Xte[col].to_numpy(float))
    prep = Prep().fit(Xtr)
    model, scaled = make_model(name, seed)
    model.fit(prep.transform(Xtr, scale=scaled), ytr)
    return model.predict_proba(prep.transform(Xte, scale=scaled))[:, 1]

def _rule_scores(xtr, ytr, xte, n_bins=20):
    """One-feature rule turned into a calibrated score: quantile-bin the feature on the
    training data and return each bin's training rug rate (missing gets its own bin)."""
    finite = np.isfinite(xtr)
    edges = np.unique(np.nanquantile(xtr[finite], np.linspace(0, 1, n_bins + 1))) if finite.any() else np.array([0.0])
    uniq = np.unique(xtr[finite]) if finite.any() else np.array([0.0])
    discrete = len(uniq) <= n_bins            # binary/low-cardinality feature (e.g. mayhem): one bin per value
    def binize(x):
        if discrete:
            b = np.searchsorted(uniq, x, side="left"); b = np.where(np.isin(x, uniq), b, len(uniq))
        else:
            b = np.searchsorted(edges[1:-1], x, side="right") if len(edges) > 2 else np.zeros(len(x), int)
        return np.where(np.isfinite(x), b, -1)
    btr, bte = binize(xtr), binize(xte)
    prior = ytr.mean(); rate = {}
    for b in np.unique(btr):
        m = btr == b
        rate[b] = (ytr[m].sum() + prior * 10) / (m.sum() + 10)   # light shrinkage
    return np.array([rate.get(b, prior) for b in bte])
