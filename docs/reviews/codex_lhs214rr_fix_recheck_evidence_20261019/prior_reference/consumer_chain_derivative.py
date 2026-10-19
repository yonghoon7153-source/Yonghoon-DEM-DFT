"""Documented path-only derivative of the 2026-10-15 consumer probe.

The original probe is read with __file__ rebound to this review folder so source
and outputs select the 2026-10-17 pinned snapshot. One exact path assignment is
changed from evidence/consumers_temp to review/tmp, as requested for this review.
If the previous review folder is absent, the bundled base64 original is decoded
in memory. Both inputs must have the pinned original SHA256 before compilation.
--verify-bundle validates and compiles only; it does not run any probe or write.
External dependency search paths and temporary directory are environmental only.
The original old fixture limits and real-source provision adapter still apply.
No source snapshot or verdict expressions are edited.
"""
from pathlib import Path
import base64
import hashlib
import json
import os
import sys

REVIEW = Path(__file__).resolve().parents[1]
WORKSPACE = REVIEW.parent
ORIGINAL = WORKSPACE / 'lhs214_fix_reverify_20261015/probes/l214_consumers.py'
BUNDLED = Path(__file__).with_name('l214_consumers_20261015.py.b64')
ORIGINAL_SHA256 = '804de03d58902862f74006afaf1e24dfed97a42a254d02b86a4cc98797de243a'


def original_payload(bundle_only=False):
    if not bundle_only and ORIGINAL.is_file():
        payload, origin = ORIGINAL.read_bytes(), ORIGINAL
    else:
        encoded = BUNDLED.read_bytes().strip()
        payload, origin = base64.b64decode(encoded, validate=True), BUNDLED
    actual = hashlib.sha256(payload).hexdigest()
    if actual != ORIGINAL_SHA256:
        raise ValueError(f'Original consumer probe SHA256 mismatch: {origin}: {actual}')
    return payload, origin


verify_only = '--verify-bundle' in sys.argv
payload, origin = original_payload(bundle_only=verify_only)
code = payload.decode('utf-8')
old_tmp = "SCRATCH = EVIDENCE / 'consumers_temp'"
assert code.count(old_tmp) == 1
code = code.replace(old_tmp, "SCRATCH = REVIEW / 'tmp'")
compiled = compile(code, str(origin), 'exec')
if verify_only:
    print(json.dumps(dict(source=str(origin), bytes=len(payload), sha256=ORIGINAL_SHA256,
                          derivative_syntax='ok', probe_executed=False), indent=2))
    raise SystemExit(0)

deps = [WORKSPACE / 'lhs_coverage_review_20260930/deps', WORKSPACE / 'gen2_network_reverify3_20261007/deps']
sys.path[:0] = [str(p) for p in deps]
os.environ['PYTHONPATH'] = os.pathsep.join(map(str, deps))
os.environ['TMP'] = os.environ['TEMP'] = str(REVIEW / 'tmp')
print('Original consumer probe sha256:', hashlib.sha256(payload).hexdigest(), flush=True)
scope = {'__file__': str(Path(__file__).resolve()), '__name__': '__main__'}
exec(compiled, scope)
