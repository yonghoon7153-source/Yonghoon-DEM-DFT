"""Replay stress probes after a minimal ZIP extraction, without packaged deps.

Required environment: Python 3.10+ with NumPy, pandas and NetworkX installed.
The original review machine may supply its pre-existing NetworkX dependency
cache through PYTHONPATH; it is never included in the ZIP.
"""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'tmp').mkdir(exist_ok=True)
(ROOT / 'evidence').mkdir(exist_ok=True)
files = [
    'probes/mv_stress_probe.py', 'probes/mv_stress_core_probe.py',
    'source/scripts/plane_load_share.py', 'source/scripts/dem_analysis_core.py',
    'source/scripts/analyze_contacts.py', 'source/scripts/metrics_json.py',
    'source/scripts/type_map_resolve.py',
    'source/docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json',
    'source/docs/data/ps45_plane_load_20261007/real14_validation/plane_load.json',
    'source/docs/data/ps73_damping_branch_20261007/snap_3100000_20261008/plane/plane_load.json',
    'source/docs/data/ps73_damping_branch_20261007/snap_moments_20261008/results_20261008/vm_moments.json',
]
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
cache = ROOT.parent / 'lhs_coverage_review_20260930/deps'
used_external_cache = importlib.util.find_spec('networkx') is None and cache.is_dir()
if used_external_cache:
    env['PYTHONPATH'] = str(cache) + (os.pathsep + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
report = {
    'scope': 'Replay of 11-file minimal ZIP; no dependency environments, empty tmp directory or prior evidence included.',
    'required_packages': ['numpy', 'pandas', 'networkx'],
    'external_review_cache_used_as_environment': used_external_cache,
    'files': files, 'replays': [],
}
versions = subprocess.run([sys.executable, '-B', '-c',
    'import json,sys,numpy,pandas,networkx; print(json.dumps(dict(python=sys.version,numpy=numpy.__version__,pandas=pandas.__version__,networkx=networkx.__version__)))'],
    env=env, capture_output=True, text=True, encoding='utf-8')
if versions.returncode:
    raise RuntimeError('Required environment packages unavailable: ' + versions.stderr)
report['runtime'] = json.loads(versions.stdout)
with tempfile.TemporaryDirectory(prefix='mv_stress_zip_', dir=ROOT / 'tmp') as work:
    work = Path(work).resolve()
    work.relative_to((ROOT / 'tmp').resolve())
    archive = work / 'minimal.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            assert (ROOT / rel).is_file(), rel
            z.write(ROOT / rel, rel)
    extracted = work / 'extracted'
    extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        for member in z.namelist():
            (extracted / member).resolve().relative_to(extracted.resolve())
        z.extractall(extracted)
    assert not (extracted.parent / 'lhs_coverage_review_20260930/deps').exists()
    for name, evidence in [('mv_stress_probe.py', 'mv_stress_arithmetic.json'),
                           ('mv_stress_core_probe.py', 'mv_stress_core_controls.json')]:
        completed = subprocess.run([sys.executable, '-B', str(extracted / 'probes' / name)],
            cwd=extracted, env=env, capture_output=True, text=True, encoding='utf-8')
        row = {'probe': name, 'exit_code': completed.returncode, 'stderr': completed.stderr}
        if completed.returncode == 0:
            actual = json.loads((extracted / 'evidence' / evidence).read_text(encoding='utf-8'))
            expected = json.loads((ROOT / 'evidence' / evidence).read_text(encoding='utf-8'))
            row['json_equal_to_recorded_evidence'] = actual == expected
        report['replays'].append(row)
        assert completed.returncode == 0, completed.stderr
        assert row['json_equal_to_recorded_evidence'], name
report['passed'] = True
(ROOT / 'evidence/mv_stress_portability.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
