"""Read-only numeric review runner; saves independent evidence outside source.

The prior probe is reused by source transformation in memory: ROOT changes to this
review, provenance pin/base changes, and its previous-base omitted-fields filter
is removed because this comparison base already contains those fields. All tested
numeric probes remain unchanged. The exact original and derived hashes are saved.
"""
from pathlib import Path
import base64
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
SOURCE = ROOT / 'source'
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['TMP'] = os.environ['TEMP'] = str(ROOT / 'tmp')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
DEPS = [str(WORK / 'lhs_coverage_review_20260930/deps'), str(WORK / 'gen2_network_reverify3_20261007/deps')]
os.environ['PYTHONPATH'] = os.pathsep.join([str(SOURCE/'scripts'), str(SOURCE/'webapp'), *DEPS])
ORIGINAL_SHA256 = 'c77e316e6a1b1555f9f9135912c9bd397d2213d03b1628f4bcf6166a62f7493d'

def read_original(prefer_bundle=False):
    original = WORK/'lhs214_fix_reverify_20261015/probes/l214_numeric.py'
    bundled = ROOT/'probes/numeric_l214_original.py.b64'
    if original.is_file() and not prefer_bundle:
        raw_bytes, origin = original.read_bytes(), str(original)
    else:
        raw_bytes = base64.b64decode(''.join(bundled.read_text(encoding='ascii').split()), validate=True)
        origin = str(bundled)
    digest = hashlib.sha256(raw_bytes).hexdigest()
    assert digest == ORIGINAL_SHA256, f'Prior probe byte integrity mismatch: {origin}: {digest}'
    # Match Path.read_text's universal-newline behavior used by the first run.
    raw = raw_bytes.decode('utf8').replace('\r\n', '\n').replace('\r', '\n')
    return original, origin, raw

def verify_bundle():
    original, origin, raw = read_original(prefer_bundle=True)
    compile(raw, str(original), 'exec')
    result = dict(bundle=origin, decoded_sha256=ORIGINAL_SHA256, syntax_valid=True,
                  sibling_present=original.is_file(), fallback_load_verified=True)
    if original.is_file():
        result['sibling_text_identical'] = read_original()[2] == raw
        assert result['sibling_text_identical']
    (ROOT/'evidence/numeric_bundle_verification.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps(result))

def tests():
    results = []
    for name in ('test_l214r01_certificate', 'test_l214r05_published_certificate', 'test_l214r06_same_class', 'test_l214r09_same_class'):
        command = [sys.executable, '-X', 'utf8', '-B', f'scripts/{name}.py']
        proc = subprocess.run(command, cwd=SOURCE, env=os.environ, text=True, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = ROOT / f'evidence/numeric_{name}.log'
        log.write_text(proc.stdout, encoding='utf8')
        result = dict(command=command, cwd=str(SOURCE), returncode=proc.returncode, log=str(log), tail=proc.stdout.splitlines()[-6:])
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    (ROOT/'evidence/numeric_selftests.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')

def old_probe():
    original, origin, raw = read_original()
    changes = [
        ('ROOT = Path(__file__).resolve().parents[1]', f'ROOT = Path({str(ROOT)!r})'),
        ('filtered = {k: v for k, v in new.items() if k not in omitted}', 'filtered = new'),
        ('9e3ef54ca228111360bfe5f6d9dad4ebe26d54af', '60ba39e224aff48a030dccfe750342f3bf9db61f'),
        ('0c557e72aaffdf6cfd033c0667c643de4501c5b1', '6cb2569569ec74b7f5a96e0ef19494e872da5272')]
    derived = raw
    for before, after in changes:
        assert before in derived
        derived = derived.replace(before, after)
    (ROOT/'evidence/numeric_probe_adapter.json').write_text(json.dumps(dict(original=str(original), loaded_from=origin, original_sha256=ORIGINAL_SHA256, derived_sha256=hashlib.sha256(derived.encode()).hexdigest(), replacements=changes), indent=2), encoding='utf8')
    ns = dict(__file__=str(original), __name__='numeric_previous_adapter')
    exec(compile(derived, str(original), 'exec'), ns)
    ns['main']()

if __name__ == '__main__':
    if '--verify-bundle' in sys.argv:
        verify_bundle()
    elif '--tests' in sys.argv:
        tests()
    else:
        old_probe()
