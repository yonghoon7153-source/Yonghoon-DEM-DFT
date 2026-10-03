"""Replay small CPU review probes only. Run in an extracted copy; evidence logs update."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

root = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--deps', type=Path, help='Optional NumPy/SciPy package directory')
ap.add_argument('--full', action='store_true', help='Include actual producer and rule-J mutations')
a = ap.parse_args()
env = os.environ.copy()
env['PYTHONUTF8'] = '1'
env['PYTHONDONTWRITEBYTECODE'] = '1'
parts = [str(root/'source/scripts')]
if a.deps:
    parts.insert(0, str(a.deps.resolve()))
if env.get('PYTHONPATH'):
    parts.append(env['PYTHONPATH'])
env['PYTHONPATH'] = os.pathsep.join(parts)
jobs = ['evidence_root/probe_units_identifiability.py',
        'evidence_gates/run_reproductions.py',
        'evidence_consumers/probe_consumers.py',
        'evidence_area/probe_area_contract.py']
if a.full:
    jobs += ['evidence_gates/probe_payload_mutation.py', 'evidence_gates/run_extra.py']
for job in jobs:
    print('REPLAY', job, flush=True)
    p = subprocess.run([sys.executable, str(root/job)], cwd=root, env=env)
    if p.returncode:
        raise SystemExit(p.returncode)
meta = json.loads((root/'evidence_gates/reproduction_metadata.json').read_text(encoding='utf-8'))
assert all(x['exit']==0 for x in meta['runs'].values()), meta['runs']
comparison = json.loads((root/'evidence_gates/reproduction_comparison.json').read_text(encoding='utf-8'))
assert all(not x['missing_from_supplement'] for x in comparison.values()), comparison
if a.full:
    for name in ['summary.json']:
        m = json.loads((root/'evidence_gates/payload_mutation'/name).read_text(encoding='utf-8'))
        assert all(v['exit']==0 for v in m.values() if isinstance(v,dict) and 'exit' in v), m
    m=json.loads((root/'evidence_gates/extra_metadata.json').read_text(encoding='utf-8'))
    assert all(x['exit']==0 for x in m.values()), m
print('REPLAY COMPLETE. Mutation PASS reproduces missing gates; it is NOT a release approval.')
