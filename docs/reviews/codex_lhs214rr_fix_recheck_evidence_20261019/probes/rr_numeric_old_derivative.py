"""Execute the prior independent numeric probe with explicit read/write rerouting.

Prior probe and prior fixtures remain unchanged. Replacement manifest is saved.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent/'lhs214r_fix_recheck_20261017'
probe = OLD/'probes/numeric_adversarial.py'
raw = probe.read_bytes()
code = raw.decode('utf8')
replacements = {
    "prior = json.loads((ROOT/'evidence/numeric_probes.json').read_text(encoding='utf8'))":
    f"prior = json.loads(Path({str(OLD/'evidence/numeric_probes.json')!r}).read_text(encoding='utf8'))",
    "'pin':'60ba39e224aff48a030dccfe750342f3bf9db61f'":
    "'pin':'77d8fd44545c33cd10ab18fc250c7ad3023833ea'",
    "ROOT/'evidence/numeric_adversarial.json'": "ROOT/'evidence/rr_numeric_legacy.json'",
}
for old, new in replacements.items():
    assert code.count(old) == 1, old
    code = code.replace(old, new)
(ROOT/'evidence/rr_numeric_legacy_derivative_manifest.json').write_text(json.dumps({
    'original': str(probe), 'sha256': hashlib.sha256(raw).hexdigest(),
    'derivative_sha256': hashlib.sha256(code.encode('utf8')).hexdigest(),
    'replacements': replacements, 'execution_file': str(__file__),
}, ensure_ascii=False, indent=2), encoding='utf8')
exec(compile(code, str(__file__), 'exec'), {'__name__':'__main__', '__file__':str(__file__)})
