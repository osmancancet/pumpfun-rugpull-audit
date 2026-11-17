"""Build the analysis table (one row per launch) with decision-time features and targets.

Decision time = the f10 snapshot (< 10 s after launch). Only information available at that
moment enters X. Exclusions are logged to results/flow.csv (CONSORT-style flow).
"""
import warnings
import glob
import numpy as np, pandas as pd
import config as C
from common import causal_reputation

def load(subset):
    files = sorted(glob.glob(str(C.DATA_RAW / "data" / subset / "*.parquet")))
    if not files:
        raise SystemExit(f"no files for {subset}; see README (data download step)")
    df = pd.concat((pd.read_parquet(f) for f in files), ignore_index=True)
    df["subset"] = subset
    return df

def main():
    C.DATA_PROC.mkdir(parents=True, exist_ok=True); C.RESULTS.mkdir(parents=True, exist_ok=True)
    cur, leg = load("launches"), load("launches_legacy")
    full = pd.concat([leg, cur], ignore_index=True)          # full history for creator reputation
    d, lg, flow = build(full)
    d.to_parquet(C.DATA_PROC / "analysis.parquet", index=False)
    lg.to_parquet(C.DATA_PROC / "legacy.parquet", index=False)
    report(d, flow, C.RESULTS)

def build(full):
    full = full.drop(columns=["name", "symbol", "uri"], errors="ignore")      # KI-14: creator text never used
    sol = full["quote_asset"].eq("sol")
    rep_c = causal_reputation(full[sol], C.REP_EMBARGO_S, strict=C.REP_STRICT)                # embargoed, causal
    rep_o = causal_reputation(full[sol], C.REP_EMBARGO_S, oracle=True)   # look-ahead reference (audit only)
    rep_o.columns = [c.replace("c_rep", "o_rep") for c in rep_o.columns]
    full = full.join(rep_c).join(rep_o)
    for e in C.REP_EMBARGO_SENS:                                         # E2b sensitivity
        r_e = causal_reputation(full[sol], e, strict=C.REP_STRICT)
        r_e.columns = [c.replace("c_rep", f"e{e}_rep") for c in r_e.columns]
        full = full.join(r_e)

    flow = []
    d = full[full.subset == "launches"].copy(); flow.append(("launches subset", len(d)))
    d = d[d.quote_asset.eq("sol")]; flow.append(("SOL-quoted (KI-03)", len(d)))
    d = d[d.decoder_complete.eq(1)]; flow.append(("decoder complete (KI-02)", len(d)))
    d = d[d.rugged.notna()]; flow.append(("outcome resolved (KI-08)", len(d)))
    d = d[d.f10_age.notna() & d.f10_dev_share.notna()]; flow.append(("has f10 snapshot (KI-01)", len(d)))
    d = d[d.create_lag_s.fillna(np.inf) <= C.MAX_CREATE_LAG_S]; flow.append(("create lag <= 1 s", len(d)))
    d = d[d.f10_age >= 0]; flow.append(("non-negative snapshot age (KI-11)", len(d)))
    already = d.rugged.eq(1) & (d.rug_dt_s <= d.f10_age)
    d = d[~already]; flow.append(("not rugged before the snapshot", len(d)))
    migrated = d.migrate_dt_s.notna() & (d.migrate_dt_s <= d.f10_age)
    d = d[~migrated]; flow.append(("not migrated before the snapshot", len(d)))
    soon = d.rugged.eq(1) & (d.rug_dt_s - d.f10_age < C.MIN_LEAD_S)
    d = d[~soon]; flow.append((f"no rug within {C.MIN_LEAD_S} s after the snapshot", len(d)))

    d["y_rug300"] = (d.rugged.eq(1) & (d.rug_dt_s <= C.HORIZON_S)).astype(int)
    d["y_rug120"] = (d.rugged.eq(1) & (d.rug_dt_s <= 120)).astype(int)
    d["y_rug3600"] = (d.rugged.eq(1) & (d.rug_dt_s <= 3600)).astype(int)
    d["y_rug_any"] = d.rugged.eq(1).astype(int)
    d["y_rug_drain"] = d.rug_branch_inferred.eq("drain").astype(int)
    d["y_rug_devdump"] = d.rug_branch_inferred.eq("dev_dump_or_recovered").astype(int)
    pk = d.peak_rs.clip(upper=85.1)                       # KI-12
    d["y_collapse90"] = ((pk >= 1) & (d.terminal_rs <= 0.10 * pk)).astype(int)
    d["y_grad"] = d.graduated.fillna(0).astype(int)
    d["lead_time_s"] = np.where(d.y_rug300 == 1, d.rug_dt_s - d.f10_age, np.nan)

    ts = pd.to_datetime(d.t0, unit="s", utc=True)
    d["day"] = ts.dt.strftime("%Y-%m-%d")
    d["seam_multihop"] = ts.between(pd.Timestamp(C.SEAM_MULTIHOP[0]), pd.Timestamp(C.SEAM_MULTIHOP[1])).astype(int)
    d["after_legs_seam"] = (ts >= pd.Timestamp(C.SEAM_LEGS)).astype(int)
    d["silence_flag"] = (d.silence_3s.fillna(0) > C.MAX_SILENCE_3S).astype(int)
    for c in ["f10_rep_rug", "f10_rep_grad", "c_rep_rug", "c_rep_grad", "o_rep_rug", "o_rep_grad"] + \
             [f"e{e}_rep_{k}" for e in C.REP_EMBARGO_SENS for k in ("rug", "grad")]:
        d[c + "_missing"] = d[c].isna().astype(int)
    d["first_time_creator"] = (d.c_rep_n == 0).astype(int)

    lg = full[(full.subset == "launches_legacy") & full.quote_asset.eq("sol") & full.rugged.notna()
              & full.f10_age.notna() & full.f10_dev_share.notna()].copy()
    # same filters as the cohort; create_lag_s is null on every harness_sample row (data card), so the lag
    # filter applies only where the lag was recorded
    lg = lg[(lg.create_lag_s.fillna(0) <= C.MAX_CREATE_LAG_S) & (lg.f10_age >= 0)]
    lg = lg[~(lg.rugged.eq(1) & (lg.rug_dt_s <= lg.f10_age))]
    lg = lg[~(lg.migrate_dt_s.notna() & (lg.migrate_dt_s <= lg.f10_age))]
    lg = lg[~(lg.rugged.eq(1) & (lg.rug_dt_s - lg.f10_age < C.MIN_LEAD_S))]
    lg["y_rug300"] = (lg.rugged.eq(1) & (lg.rug_dt_s <= C.HORIZON_S)).astype(int)
    lg["day"] = pd.to_datetime(lg.t0, unit="s", utc=True).dt.strftime("%Y-%m-%d")
    for c in ["f10_rep_rug", "f10_rep_grad", "c_rep_rug", "c_rep_grad"]:
        lg[c + "_missing"] = lg[c].isna().astype(int)
    if lg.empty:
        warnings.warn("legacy set is empty after the filters; the E5 legacy experiment will be skipped")
    return d, lg, flow

def report(d, flow, out):
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(flow, columns=["step", "rows"]).to_csv(out / "flow.csv", index=False)
    desc = d.groupby("mayhem").agg(n=("mint", "size"), creators=("creator", "nunique"),
                                   rug300=("y_rug300", "mean"), rug_any=("y_rug_any", "mean"),
                                   grad=("y_grad", "mean"), first_time=("first_time_creator", "mean"))
    desc.to_csv(out / "table1_descriptives.csv")
    cc = d.groupby("creator").size().sort_values(ascending=False)
    pd.Series({"creators": len(cc), "share_launches_top1pct_creators": cc.head(max(1, len(cc)//100)).sum() / len(d),
               "max_launches_one_creator": int(cc.max()), "median_launches_per_creator": float(cc.median())}
              ).to_csv(out / "creator_concentration.csv")
    print(pd.DataFrame(flow)); print(desc)

if __name__ == "__main__":
    main()
