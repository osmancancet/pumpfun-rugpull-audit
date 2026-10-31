"""Offline integrity check: compare every downloaded day file with the sha256 in the card."""
import hashlib, re
from pathlib import Path
import config as C
card = (C.DATA_RAW / "README.md") if (C.DATA_RAW / "README.md").exists() else next(C.DATA_RAW.rglob("README.md"))
card = card.read_text(encoding="utf-8")
rows = re.findall(r"(data/[\w/\-\.]+\.parquet)\S*\s*\|[^|]*\|[^|]*\|\s*([0-9a-f]{64})", card)
bad = missing = 0
for rel, sha in rows:
    f = C.DATA_RAW / rel
    if not f.exists():
        missing += 1; continue
    if hashlib.sha256(f.read_bytes()).hexdigest() != sha:
        bad += 1; print("MISMATCH", rel)
print(f"listed={len(rows)} missing={missing} mismatched={bad}")
