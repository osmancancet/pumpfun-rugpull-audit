"""Numpy/pandas-only utilities: metrics, statistical tests, splits, causal reputation.

Everything here is dependency-light on purpose so that it can be unit-tested
(smoke_test.py) without scikit-learn/scipy. Model code lives in models.py.
"""
from __future__ import annotations
import math, warnings
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------- metrics
def roc_auc(y, s):
    """ROC-AUC via the Mann-Whitney U statistic with midranks for ties."""
    y = np.asarray(y).astype(int); s = np.asarray(s, float)
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = _midrank(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))

def average_precision(y, s):
    """Average precision (step-wise PR-AUC), ties handled by grouping equal scores."""
    y = np.asarray(y).astype(int); s = np.asarray(s, float)
    P = y.sum()
    if P == 0:
        return float("nan")
    order = np.argsort(-s, kind="mergesort")
    y, s = y[order], s[order]
    distinct = np.r_[np.where(np.diff(s))[0], len(s) - 1]
    tp = np.cumsum(y)[distinct]; fp = (distinct + 1) - tp
    prec = tp / (tp + fp); rec = tp / P
    rec_prev = np.r_[0.0, rec[:-1]]
    return float(np.sum((rec - rec_prev) * prec))

def brier(y, p):
    y = np.asarray(y, float); p = np.asarray(p, float)
    return float(np.mean((p - y) ** 2))

def ece(y, p, n_bins=10):
    """Expected calibration error, equal-width bins (as in the dataset card's ECE)."""
    y = np.asarray(y, float); p = np.clip(np.asarray(p, float), 0, 1)
    bins = np.minimum((p * n_bins).astype(int), n_bins - 1)
    e = 0.0
    for b in range(n_bins):
        m = bins == b
        if m.any():
            e += m.mean() * abs(p[m].mean() - y[m].mean())
    return float(e)

def confusion(y, yhat):
    y = np.asarray(y).astype(int); yhat = np.asarray(yhat).astype(int)
    tp = int(((y == 1) & (yhat == 1)).sum()); tn = int(((y == 0) & (yhat == 0)).sum())
    fp = int(((y == 0) & (yhat == 1)).sum()); fn = int(((y == 1) & (yhat == 0)).sum())
    return tp, fp, tn, fn

def mcc(y, yhat):
    tp, fp, tn, fn = confusion(y, yhat)
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return float((tp * tn - fp * fn) / den) if den > 0 else 0.0

def precision_at_budget(y, s, budget):
    """Precision when flagging the top `budget` share of launches (alert-budget view)."""
    y = np.asarray(y).astype(int); s = np.asarray(s, float)
    k = max(1, int(round(budget * len(y))))
    thr = np.sort(s)[::-1][k - 1]
    above = s > thr; tie = s == thr
    # launches tied at the cut-off score enter in expectation (random tie-breaking), so the
    # value does not depend on row order (matters for the prior and binned one-feature rules)
    take = k - above.sum()
    return float((y[above].sum() + take * y[tie].mean()) / k)

def threshold_for_rate(s_val, rate):
    """Score threshold that flags `rate` of the validation launches (fixed before testing)."""
    return float(np.quantile(np.asarray(s_val, float), 1 - rate))

def all_metrics(y, s, thr=None):
    out = {"n": int(len(y)), "prevalence": float(np.mean(y)),
           "roc_auc": roc_auc(y, s), "pr_auc": average_precision(y, s),
           "brier": brier(y, s), "ece": ece(y, s)}
    out["pr_auc_lift"] = out["pr_auc"] / out["prevalence"] if out["prevalence"] > 0 else float("nan")
    if thr is not None:
        out["mcc"] = mcc(y, np.asarray(s) >= thr)
    return out

def _midrank(x):
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort"); xs = x[order]
    n = len(x); ranks = np.empty(n)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[j + 1] == xs[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1
        i = j + 1
    return ranks

# ----------------------------------------------------------------------------- tests
def _norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))

def delong_test(y, s1, s2):
    """Paired DeLong test for two correlated ROC-AUCs (DeLong et al., 1988).
    Returns (auc1, auc2, diff, se, z, two-sided p)."""
    y = np.asarray(y).astype(int)
    pos, neg = y == 1, y == 0
    m, n = pos.sum(), neg.sum()
    aucs, v10, v01 = [], [], []
    for s in (np.asarray(s1, float), np.asarray(s2, float)):
        tx, ty = _midrank(s[pos]), _midrank(s[neg])
        tz = _midrank(np.r_[s[pos], s[neg]])
        auc = (tz[:m].sum() - m * (m + 1) / 2) / (m * n)
        v10.append((tz[:m] - tx) / n)
        v01.append(1 - (tz[m:] - ty) / m)
        aucs.append(auc)
    s10 = np.cov(np.vstack(v10)); s01 = np.cov(np.vstack(v01))
    S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    diff = aucs[0] - aucs[1]
    se = math.sqrt(max(var, 1e-300))
    z = diff / se
    return float(aucs[0]), float(aucs[1]), float(diff), float(se), float(z), float(2 * _norm_sf(abs(z)))

def mcnemar_test(y, yhat1, yhat2):
    """Exact-binomial McNemar test on discordant correct/incorrect decisions."""
    y = np.asarray(y).astype(int)
    c1 = np.asarray(yhat1).astype(int) == y; c2 = np.asarray(yhat2).astype(int) == y
    b = int((c1 & ~c2).sum()); c = int((~c1 & c2).sum()); n = b + c
    if n == 0:
        return b, c, 1.0
    k = min(b, c)
    # two-sided exact p = 2 * P(X <= k), X ~ Bin(n, 0.5); log-space for large n
    logp = [_log_binom_pmf(i, n) for i in range(k + 1)]
    mx = max(logp)
    p = 2 * math.exp(mx) * sum(math.exp(v - mx) for v in logp)
    return b, c, float(min(1.0, p))

def _log_binom_pmf(i, n):
    return math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2)

def benjamini_hochberg(pvals):
    p = np.asarray(pvals, float); m = len(p)
    order = np.argsort(p); ranked = p[order] * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(m); out[order] = np.minimum(q, 1)
    return out

def cluster_bootstrap(y, s_a, s_b, clusters, metric, n_boot, seed):
    """Paired cluster bootstrap of metric(s_a) - metric(s_b), resampling clusters
    (creators) with replacement. Returns point diff, percentile 95% CI, two-sided p."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y); s_a = np.asarray(s_a); s_b = np.asarray(s_b)
    codes, uniq = pd.factorize(np.asarray(clusters))
    idx_by = pd.Series(np.arange(len(y))).groupby(codes).apply(np.array).to_list()
    G = len(idx_by)
    point = metric(y, s_a) - (metric(y, s_b) if s_b is not None else 0)
    diffs = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.integers(0, G, G)
        ii = np.concatenate([idx_by[g] for g in pick])
        diffs[b] = metric(y[ii], s_a[ii]) - metric(y[ii], s_b[ii])
    lo, hi = np.nanpercentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return float(point), float(lo), float(hi), float(min(1.0, p))

def cluster_bootstrap_ci(y, s, clusters, metric, n_boot, seed):
    rng = np.random.default_rng(seed)
    y = np.asarray(y); s = np.asarray(s)
    codes, _ = pd.factorize(np.asarray(clusters))
    idx_by = pd.Series(np.arange(len(y))).groupby(codes).apply(np.array).to_list()
    G = len(idx_by); vals = np.empty(n_boot)
    for b in range(n_boot):
        ii = np.concatenate([idx_by[g] for g in rng.integers(0, G, G)])
        vals[b] = metric(y[ii], s[ii])
    return float(metric(y, s)), *map(float, np.nanpercentile(vals, [2.5, 97.5]))

def friedman_statistic(scores):
    """Friedman chi-square for a (blocks x methods) matrix of scores (higher = better).
    p-value via chi-square survival (Wilson-Hilferty approximation, no scipy)."""
    X = np.asarray(scores, float); N, k = X.shape
    R = np.vstack([_midrank(-row) for row in X])
    Rj = R.mean(0)
    chi2 = 12 * N / (k * (k + 1)) * np.sum((Rj - (k + 1) / 2) ** 2)
    df = k - 1
    z = ((chi2 / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return float(chi2), int(df), float(_norm_sf(z)), Rj

# ----------------------------------------------------------------------------- splits
def split_random_rows(n, test_frac, seed):
    rng = np.random.default_rng(seed); perm = rng.permutation(n)
    k = int(round(n * test_frac)); test = np.zeros(n, bool); test[perm[:k]] = True
    return ~test, test

def split_group(groups, test_frac, seed):
    """Group-disjoint split: every creator is in train OR test, never both."""
    codes, uniq = pd.factorize(np.asarray(groups))
    rng = np.random.default_rng(seed)
    test_groups = rng.random(len(uniq)) < test_frac
    test = test_groups[codes]
    return ~test, test

def split_temporal(day, train_days, test_days, gap_days=0):
    """Train on the given list of days, purge `gap_days`, test on `test_days` (lists of day labels)."""
    day = np.asarray(day)
    return np.isin(day, train_days), np.isin(day, test_days)

def forward_folds(days_sorted, train_len, test_len, gap, expanding=False):
    """Forward-chaining folds over sorted day labels: yields (train_days, test_days)."""
    D = list(days_sorted); folds = []
    start = 0; t0 = train_len
    while t0 + gap + test_len <= len(D):
        tr = D[0 if expanding else t0 - train_len: t0]
        te = D[t0 + gap: t0 + gap + test_len]
        folds.append((tr, te)); t0 += test_len
    return folds

# ----------------------------------------------------------------------------- reputation
def causal_reputation(df, embargo_s, creator="creator", t0="t0", rugged="rugged",
                      graduated="graduated", rug_dt="rug_dt_s", grad_dt="migrate_dt_s", oracle=False, strict=True):
    """Creator track record that uses ONLY outcomes knowable before each launch.

    A previous launch j of the same creator counts as resolved for launch i iff its
    outcome time is strictly < t0_i, where outcome time = t0_j + rug_dt_j if rugged, else
    t0_j + embargo_s (conservative stand-in for path closure). Unresolved launches never count.
    With oracle=True every earlier launch counts from its own launch time with the label it will have
    (look-ahead reference, used only to audit published reputation fields). Under strict=True the oracle
    uses the same "within the embargo" labels as the causal version, so the two differ only in timing.
    strict=True (default): every launch resolves at t0_j + min(rug_dt_j, embargo_s) and is credited
    with "rugged within the embargo" / "graduated by its resolution time". A launch that rugs only after
    the embargo therefore counts as not rugged from t0_j + embargo_s on, exactly like a launch that
    never rugs, so whether a launch is in the denominator never depends on its future. strict=False
    reproduces the first full run (late rugs stayed unresolved until t0_j + rug_dt_j; graduation used
    the final label at t0_j + embargo_s).
    Returns c_rep_n (earlier launches), c_rep_n_res (resolved), c_rep_rug, c_rep_grad (NaN if none).
    Vectorised event sweep: O(n log n).
    """
    cr = pd.factorize(df[creator])[0]
    t = df[t0].to_numpy(float)
    known = df[rugged].notna().to_numpy()
    rug = df[rugged].fillna(0).to_numpy(float)
    grad = df[graduated].fillna(0).to_numpy(float)
    rdt = np.clip(df[rug_dt].to_numpy(float), 0, None)          # a negative lag never resolves before the launch
    if strict:
        # labels known by the embargo: "rugged within E" and "graduated by the resolution time"
        early = (rug == 1) & (np.nan_to_num(rdt, nan=np.inf) <= embargo_s)
        dt_res = np.where(early, np.nan_to_num(rdt, nan=embargo_s), embargo_s)
        rug = early.astype(float)
        if grad_dt in df.columns:
            gdt = np.clip(df[grad_dt].to_numpy(float), 0, None)
            if np.any((grad == 1) & np.isnan(gdt)):
                warnings.warn(f"{int(((grad == 1) & np.isnan(gdt)).sum())} graduated launches lack {grad_dt}; counted as not graduated")
            grad = ((grad == 1) & (np.nan_to_num(gdt, nan=np.inf) <= dt_res)).astype(float)
        else:
            warnings.warn(f"column {grad_dt} missing: graduation share uses the final label (not causal)")
    if oracle:
        t_out = t.copy()                                   # same labels as the causal version, credited at launch time
    elif strict:
        t_out = t + dt_res
    else:
        t_out = np.where(rug == 1, t + np.nan_to_num(rdt, nan=embargo_s), t + embargo_s)
    t_out = np.where(known, t_out, np.inf)
    n = len(t)
    # events (resolutions) and queries (launches); at equal time the query sorts first => strict "<"
    ev_c = np.r_[cr, cr]; ev_t = np.r_[t, t_out]
    kind = np.r_[np.zeros(n), np.ones(n)]            # 0 = query, 1 = resolution event
    w_n = np.r_[np.zeros(n), np.isfinite(t_out).astype(float)]
    w_r = np.r_[np.zeros(n), np.where(np.isfinite(t_out), rug, 0)]
    w_g = np.r_[np.zeros(n), np.where(np.isfinite(t_out), grad, 0)]
    order = np.lexsort((kind, ev_t, ev_c))
    c_sorted = ev_c[order]
    def gcum(w):
        cs = np.cumsum(w[order])
        start = np.r_[0, np.flatnonzero(np.diff(c_sorted)) + 1]
        offs = np.repeat(np.r_[0, cs[start[1:] - 1]] if len(start) > 1 else np.array([0.0]),
                         np.diff(np.r_[start, len(c_sorted)]))
        return cs - offs
    cn, crg, cgr = gcum(w_n), gcum(w_r), gcum(w_g)
    qmask = kind[order] == 0; qidx = order[qmask]
    k = np.empty(n); k[qidx] = cn[qmask]
    rr = np.empty(n); rr[qidx] = crg[qmask]
    gg = np.empty(n); gg[qidx] = cgr[qmask]
    # number of earlier launches by launch time (strict)
    o2 = np.lexsort((t, cr)); prev = np.empty(n)
    cs = np.r_[0, np.flatnonzero(np.diff(cr[o2])) + 1]
    pos = np.arange(n) - np.repeat(cs, np.diff(np.r_[cs, n]))
    # ties in t0 within a creator: count only strictly earlier launches
    ts_ = t[o2]; cc_ = cr[o2]
    first_of_tie = np.r_[True, (np.diff(ts_) != 0) | (np.diff(cc_) != 0)]
    tie_start = np.maximum.accumulate(np.where(first_of_tie, np.arange(n), 0))
    prev[o2] = pos - (np.arange(n) - tie_start)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = pd.DataFrame({"c_rep_n": prev, "c_rep_n_res": k,
                            "c_rep_rug": np.where(k > 0, rr / np.maximum(k, 1), np.nan),
                            "c_rep_grad": np.where(k > 0, gg / np.maximum(k, 1), np.nan)}, index=df.index)
    return out

# ----------------------------------------------------------------------------- fast cluster bootstrap
# Resampling G clusters with replacement is equivalent to giving every row the weight
# "number of times its cluster was drawn" (multinomial counts). With the score order fixed once,
# weighted AP and ROC-AUC are O(n) per replicate. Point estimates are unchanged.
class _Sorted:
    def __init__(self, y, s):
        s = np.asarray(s, float); self.order = np.argsort(-s, kind="mergesort")
        ss = s[self.order]; self.y = np.asarray(y)[self.order].astype(float)
        self.last = np.r_[np.where(np.diff(ss))[0], len(ss) - 1]       # last index of each tie group
        self.gid = np.repeat(np.arange(len(self.last)), np.diff(np.r_[-1, self.last]))

def _w_ap(S, w):
    wp = w * S.y; P = wp.sum()
    if P <= 0: return np.nan
    tp = np.cumsum(wp)[S.last]; tot = np.cumsum(w)[S.last]
    prec = np.divide(tp, tot, out=np.zeros_like(tp), where=tot > 0); rec = tp / P
    return float(np.sum((rec - np.r_[0.0, rec[:-1]]) * prec))

def _w_auc(S, w):
    wp = np.bincount(S.gid, w * S.y, len(S.last)); wn = np.bincount(S.gid, w * (1 - S.y), len(S.last))
    P, N = wp.sum(), wn.sum()
    if P <= 0 or N <= 0: return np.nan
    neg_below = N - np.cumsum(wn)                    # negatives with strictly lower score (descending order)
    return float(np.sum(wp * (neg_below + 0.5 * wn)) / (P * N))

def _fast_metric(metric):
    return {average_precision: _w_ap, roc_auc: _w_auc}.get(metric)

def _cluster_weights(clusters, n_boot, seed):
    rng = np.random.default_rng(seed)
    codes, _ = pd.factorize(np.asarray(clusters)); G = codes.max() + 1
    for _ in range(n_boot):
        cnt = rng.multinomial(G, np.full(G, 1.0 / G)) if G < 2000 else np.bincount(rng.integers(0, G, G), minlength=G)
        yield cnt[codes].astype(float)

_slow_cluster_bootstrap, _slow_cluster_bootstrap_ci = cluster_bootstrap, cluster_bootstrap_ci

def cluster_bootstrap(y, s_a, s_b, clusters, metric, n_boot, seed):
    f = _fast_metric(metric)
    if f is None:
        return _slow_cluster_bootstrap(y, s_a, s_b, clusters, metric, n_boot, seed)
    A, B = _Sorted(y, s_a), _Sorted(y, s_b)
    point = metric(y, s_a) - metric(y, s_b)
    diffs = np.array([f(A, w[A.order]) - f(B, w[B.order]) for w in _cluster_weights(clusters, n_boot, seed)])
    lo, hi = np.nanpercentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return float(point), float(lo), float(hi), float(min(1.0, p))

def cluster_bootstrap_ci(y, s, clusters, metric, n_boot, seed):
    f = _fast_metric(metric)
    if f is None:
        return _slow_cluster_bootstrap_ci(y, s, clusters, metric, n_boot, seed)
    A = _Sorted(y, s)
    vals = np.array([f(A, w[A.order]) for w in _cluster_weights(clusters, n_boot, seed)])
    return float(metric(y, s)), *map(float, np.nanpercentile(vals, [2.5, 97.5]))
