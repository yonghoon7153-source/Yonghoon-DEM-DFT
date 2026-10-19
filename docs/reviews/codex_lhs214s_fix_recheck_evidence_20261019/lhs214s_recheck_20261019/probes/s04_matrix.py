"""Replay unchanged 128-case rr_display_extended expectations at the two pins.

Adapter changes only source/output paths and captures every full response HTML.
"""
import hashlib
import json
from pathlib import Path
import sys

REVIEW = Path(__file__).resolve().parents[1]
original = REVIEW / 'source/docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/probes/rr_display_extended.py'
raw = original.read_text(encoding='utf-8')
replacements = [
    ("ROOT = REVIEW/'source' if TREE=='source' else REVIEW.parent/'lhs214r_fix_recheck_20261017/source'",
     "ROOT = REVIEW/'source' if TREE=='source' else REVIEW.parent/'lhs214rr_recheck_20261019/source'"),
    ('rr_display_extended_', 's04_matrix_'),
    ('if capture: (WORK/', 'if True: (WORK/'),
]
code = raw
for before, after in replacements:
    assert before in code, before
    code = code.replace(before, after)
(REVIEW / 'evidence' / ('s04_matrix_' + sys.argv[1] + '_adapter.json')).write_text(
    json.dumps(dict(original=str(original), sha256=hashlib.sha256(original.read_bytes()).hexdigest(), replacements=replacements), indent=2), encoding='utf-8')
exec(compile(code, str(original), 'exec'), globals())
