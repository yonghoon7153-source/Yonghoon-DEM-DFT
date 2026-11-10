"""Reproduce bounded review arithmetic only; never execute a research model.

Run from any location: python -I -X utf8 -B reproduce_review.py
Requires numpy and scipy. No network, project imports, Git, Taichi or host access.
Writes only this evidence directory's generated probe JSON and reproduction logs.
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PKG = ROOT / 'package'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def same(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-11)
    return a == b

def main():
    declared = {}
    for line in (PKG / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        h, name = line.split(None, 1)
        assert name not in declared
        path = (PKG / name).resolve()
        assert path.is_relative_to(PKG.resolve())
        assert sha(path.read_bytes()) == h, name
        declared[name] = h
    actual = {p.relative_to(PKG).as_posix() for p in PKG.rglob('*') if p.is_file()}
    assert actual == set(declared) | {'SHA256SUMS'}
    comparisons = json.loads((ROOT / 'remote_blob_comparison.json').read_text(encoding='utf-8'))
    for row in comparisons:
        b = (PKG / row['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        assert blob == row['local'] == row['remote']['sha'], row['path']
    assert len(comparisons) == 46
    logs = ROOT / 'reproduction'
    logs.mkdir(exist_ok=True)
    cases = [
        ('branches_review/independent_enumeration.py', 'branches_review/independent_results.json'),
        ('physics_review/counterexamples.py', 'physics_review/counterexamples.json'),
        ('code_arithmetic_review/reproduce.py', 'code_arithmetic_review/results.json'),
    ]
    results = []
    for script, generated in cases:
        saved = ROOT / 'expected' / generated
        expected = json.loads(saved.read_text(encoding='utf-8'))
        p = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(ROOT / script)],
                           cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        stem = Path(script).parent.name
        (logs / (stem + '.stdout.txt')).write_bytes(p.stdout)
        (logs / (stem + '.stderr.txt')).write_bytes(p.stderr)
        assert p.returncode == 0, (script, p.returncode, p.stderr.decode('utf-8', 'replace'))
        observed = json.loads((ROOT / generated).read_text(encoding='utf-8'))
        matched = same(expected, observed)
        assert matched, ('probe output differs', script)
        results.append({'script': script, 'returncode': p.returncode,
                        'expected_json_matches': matched,
                        'generated_sha256': sha((ROOT / generated).read_bytes())})
    import numpy
    import scipy
    summary = {'status': 'PASS', 'input_files': len(actual), 'input_hash_rows': len(declared),
               'pinned_source_blobs': len(comparisons), 'checks': results,
               'python': sys.version, 'platform': platform.platform(),
               'numpy': numpy.__version__, 'scipy': scipy.__version__,
               'numeric_compare_rtol': 1e-10, 'numeric_compare_atol': 1e-11,
               'research_model_runs': 0, 'remote_host_access': False,
               'scope': 'input bytes, saved Git blob metadata, bounded independent arithmetic only'}
    (logs / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
