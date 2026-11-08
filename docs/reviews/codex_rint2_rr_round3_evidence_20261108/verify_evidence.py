"""Verify this evidence package, without executing product code."""
import hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
bad=[]; n=0
for line in (root/'EVIDENCE_MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
    if not line: continue
    sha, rel=line.split('  ',1)
    p=(root/rel).resolve()
    if not p.is_relative_to(root.resolve()): raise SystemExit('unsafe manifest path')
    n+=1
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: bad.append(rel)
print({'checked':n,'mismatches':bad})
raise SystemExit(1 if bad else 0)
