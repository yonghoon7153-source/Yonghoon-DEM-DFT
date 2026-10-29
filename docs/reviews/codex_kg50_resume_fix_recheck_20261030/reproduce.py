"""Reproduce CPU review evidence in a NEW directory. No Bash/DEM/network calls.

Exit 0 means the review observations (including false acceptances) reproduced;
it is NOT a production-tool GO. Reads the sealed repo and copies it to --out.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def sealed_files(base):
    entries = {}
    for line in (base / 'PIN.txt').read_text(encoding='utf-8').splitlines():
        m = re.fullmatch(r'([0-9a-f]{64})\s+(.+)', line.strip())
        if not m:
            continue
        name = m[2].replace('\\', '/')
        if not name.startswith('repo/'):
            name = 'repo/' + name
        p = (base / name).resolve()
        if not p.is_relative_to((base / 'repo').resolve()):
            raise RuntimeError('PIN path outside repo: ' + name)
        if not p.is_file() or digest(p) != m[1]:
            raise RuntimeError('Source hash mismatch: ' + name)
        entries[name] = m[1]
    if len(entries) != 282:
        raise RuntimeError(f'Expected 282 source files, got {len(entries)}')
    return entries

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, help='New, nonexistent evidence directory')
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    if out.exists():
        raise RuntimeError('Refusing existing output directory: ' + str(out))
    original = sealed_files(BASE)
    out.mkdir(parents=True)
    shutil.copytree(BASE / 'repo', out / 'repo')
    shutil.copyfile(BASE / 'PIN.txt', out / 'PIN.txt')
    jobs = [('program', 'probe_program.py'), ('launch', 'probe_launch.py'),
            ('q5', 'probe_q5.py'), ('q5', 'finish_evidence.py')]
    for area, filename in jobs:
        target = out / 'independent' / area / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BASE / 'independent' / area / filename, target)
    receipt = {'python': sys.version, 'platform': sys.platform,
               'source_file_count': len(original),
               'scope': 'CPU review reproduction only; no Bash, MPI, LIGGGHTS, SLURM or network',
               'runs': []}
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    for area, filename in jobs:
        script = out / 'independent' / area / filename
        start = time.monotonic()
        command = [sys.executable, '-I', '-X', 'utf8', '-B', str(script)]
        run = subprocess.run(command, cwd=str(out), env=env,
                             capture_output=True, text=True, encoding='utf-8', timeout=180)
        log = script.with_suffix('.execution.txt')
        log.write_text('STDOUT\n' + run.stdout + '\nSTDERR\n' + run.stderr,
                       encoding='utf-8', newline='\n')
        receipt['runs'].append({'script': script.relative_to(out).as_posix(),
            'argv': command, 'rc': run.returncode,
            'seconds': round(time.monotonic()-start, 3)})
        if run.returncode:
            (out/'run_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
            raise RuntimeError('Probe failed; inspect ' + str(log))
    p = json.loads((out/'independent/program/results.json').read_text(encoding='utf-8'))
    cases = {x['name']:x for x in p['cases']}
    assert len(cases) == 43
    for name in ['d2_drop_intermediate_variable_definition', 'd2_runtime_dependent_eager_variable']:
        assert all(cases[name][k] == 0 for k in ['static_rc','cut_rc','trial_rc'])
    assert cases['d2_received_baseline']['static_rc'] == 0
    assert cases['archived_after_settling_baseline']['static_rc'] == 0
    assert cases['archived_compress_r075']['static_rc'] == 1
    launch = json.loads((out/'independent/launch/results.json').read_text(encoding='utf-8'))['runner_suffix_false_green']
    assert not launch['checked_deck_problems']
    assert len(launch['actual_main_if_checked_problems']) == 1
    assert all(launch['runner_gate_predicates'].values())
    assert launch['actual_trial_identical_to_checked_trial'] and launch['manifest_matches']
    assert not launch['actual_main_covered_by_manifest']
    assert not launch['new_main_submission_observed']
    q = json.loads((out/'independent/q5/results.json').read_text(encoding='utf-8'))
    assert len(q['cases']) == 11 and all(not x['verify'] for x in q['cases'].values())
    assert len(q['mutations']) == 5 and all(x['allowlist_problems'] for x in q['mutations'].values())
    assert len(q['independent_registration_body']) == 8
    assert all(x['equal'] for x in q['independent_registration_body'].values())
    assert q['extra_echo_provenance']['accepted']
    assert q['d2']['current_producer_cut']['byte_equal_to_received_trial']
    assert sealed_files(out) == original == sealed_files(BASE)
    receipt['observations_reproduced'] = True
    receipt['source_files_unchanged'] = True
    receipt['production_go'] = False
    receipt['observations'] = {'program_inputs':43, 'q5_generated_branches':11,
        'q5_independent_bodies_equal':8, 'w2_mutations_rejected':5,
        'new_findings':['KG50RF-01','KG50RF-02','KG50RF-03']}
    (out/'run_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
