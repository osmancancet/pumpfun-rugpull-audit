"""Spot-check sampled mints against the public Solana RPC (no key): the oldest transaction's
block time vs t0 and its fee payer vs creator. Read-only; writes results/crosscheck_rpc.csv."""
import json, time, urllib.request, pandas as pd
RPC = "https://api.mainnet-beta.solana.com"
def rpc(method, params):
    for i in range(6):
        try:
            req = urllib.request.Request(RPC, json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
                                         {"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if "error" in r: raise RuntimeError(r["error"])
            return r["result"]
        except Exception as e:
            time.sleep(2 + 3 * i); err = e
    raise err
S = pd.read_csv("../results/crosscheck_sample.csv"); out = []
for _, r in S.iterrows():
    before, oldest, pages = None, None, 0
    while pages < 15:
        p = {"limit": 1000}; p.update({"before": before} if before else {})
        sig = rpc("getSignaturesForAddress", [r.mint, p]); pages += 1; time.sleep(0.5)
        if not sig: break
        oldest = sig[-1]; before = oldest["signature"]
        if len(sig) < 1000: break
    row = dict(mint=r.mint, pages=pages, complete=pages < 15)
    if oldest:
      try:
        tx = rpc("getTransaction", [oldest["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 1}]); time.sleep(0.5)
        payer = tx["transaction"]["message"]["accountKeys"][0]
        row.update(oldest_block_time=oldest["blockTime"], t0=r.t0, dt_s=oldest["blockTime"] - r.t0,
                   fee_payer=payer, creator=r.creator, creator_match=payer == r.creator, tx_err=oldest["err"] is not None)
      except Exception as e:
        row.update(oldest_block_time=oldest["blockTime"], t0=r.t0, dt_s=oldest["blockTime"] - r.t0, creator=r.creator, error=str(e)[:120])
    acc = rpc("getAccountInfo", [r.mint, {"encoding": "jsonParsed"}]); time.sleep(0.5)
    info = (acc or {}).get("value") or {}
    pi = info.get("data", {}).get("parsed", {}).get("info", {}) if isinstance(info.get("data"), dict) else {}
    row.update(owner_program=info.get("owner"), decimals=pi.get("decimals"), supply=pi.get("supply"), mint_authority=pi.get("mintAuthority"))
    print(row, flush=True); out.append(row)
pd.DataFrame(out).to_csv("../results/crosscheck_rpc.csv", index=False)
