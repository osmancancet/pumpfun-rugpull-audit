"""Offline integrity check: compare every downloaded day file of the two subsets used here with the sha256 in the card."""
import hashlib, re
import config as C
card = (C.DATA_RAW / "README.md") if (C.DATA_RAW / "README.md").exists() else next(C.DATA_RAW.rglob("README.md"))
card = card.read_text(encoding="utf-8")
# card rows: | subset | data/<subset>/<day>.parquet (optional note) | rows | bytes | sha256 |
rows = re.findall(r"\|\s*(launches(?:_legacy)?)\s*\|\s*(data/[\w/\-\.]+\.parquet)[^|]*\|[^|]*\|[^|]*\|\s*([0-9a-f]{64})", card)
bad = missing = 0
for _, rel, sha in rows:
    f = C.DATA_RAW / rel
    if not f.exists():
        missing += 1; continue
    if hashlib.sha256(f.read_bytes()).hexdigest() != sha:
        bad += 1; print("MISMATCH", rel)
print(f"listed={len(rows)} missing={missing} mismatched={bad}")
if missing or bad:
    raise SystemExit("day files missing or changed; see README step 2")
