from pathlib import Path
import json, os, shutil, subprocess, sys

import argparse
parser = argparse.ArgumentParser(description="Independent source-loader and contract completeness regression checks")
parser.add_argument('--source', type=Path, required=True, help='Root containing the frozen fixture script and evidence JSON')
parser.add_argument('--repo', type=Path, required=True, help='Read-only Git source repository')
parser.add_argument('--output', type=Path, required=True, help='New scratch output directory')
args = parser.parse_args()
BASE, SRC = args.output.resolve(), args.source.resolve()
BASE.mkdir(parents=True)
(BASE / 'tmp').mkdir()
EVID = Path('docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024')
PYTHON = sys.executable
ENV = dict(os.environ, TMPDIR=str(BASE / 'tmp'))
observations = []

def run_case(name, mutate=None, extra_env=None, expected_rc=2, expected_status=None):
    dest = BASE / 'cases' / name
    for rel in (Path('scripts/test_dem_gen2_t12_consumer_contract.py'), EVID/'source-manifest.json', EVID/'p1-consumer-contract.json'):
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SRC / rel, target)
    if mutate:
        mutate(dest)
    env = dict(ENV, **(extra_env or {}))
    result = subprocess.run([PYTHON, '-I', str(dest / 'scripts/test_dem_gen2_t12_consumer_contract.py'),
                             '--repo', str(args.repo.resolve())], env=env, capture_output=True, text=True)
    status = None
    if result.stdout:
        try:
            receipt = json.loads(result.stdout)
            status = receipt['status']
        except ValueError:
            pass
    out = {'case': name, 'returncode': result.returncode, 'status': status,
           'expected_rc': expected_rc, 'expected_status': expected_status,
           'pass': result.returncode == expected_rc and (expected_status is None or status == expected_status),
           'stderr': result.stderr.strip()}
    observations.append(out)

def update(dest, filename, change):
    path = dest / EVID / filename
    obj = json.loads(path.read_text())
    change(obj)
    path.write_text(json.dumps(obj))

run_case('wrong-pin', lambda d: update(d, 'source-manifest.json', lambda m: m.update(consumer_pin='8347d32ea678c0174bd77d4c79cfbd7b0591e4a3')))
run_case('wrong-prefix', lambda d: update(d, 'source-manifest.json', lambda m: m.update(source_prefix='other/')))
run_case('missing-source', lambda d: update(d, 'source-manifest.json', lambda m: m['files_sha256'].pop('ul_s3.py')))
run_case('wrong-hash', lambda d: update(d, 'source-manifest.json', lambda m: m['files_sha256'].update({'ul_reader.py': '0'*64})))
empty = BASE / 'empty-object-database'
empty.mkdir()
run_case('missing-git-objects', extra_env={'GIT_OBJECT_DIRECTORY': str(empty), 'GIT_ALTERNATE_OBJECT_DIRECTORIES': ''})
run_case('empty-excerpts', lambda d: update(d, 'p1-consumer-contract.json', lambda m: m.update(params={}, bed_parameters={})), expected_rc=1, expected_status='FAIL')
run_case('missing-bed', lambda d: update(d, 'p1-consumer-contract.json', lambda m: m['bed_parameters'].pop('ps_0_10_r45')), expected_rc=1, expected_status='FAIL')
run_case('missing-h0', lambda d: update(d, 'p1-consumer-contract.json', lambda m: m['bed_parameters']['ps_7_3_r45'].pop('h0')), expected_rc=1, expected_status='FAIL')
(BASE / 'report.json').write_text(json.dumps(observations, indent=2)+'\n')
print(json.dumps(observations, indent=2))

raise SystemExit(0 if all(x['pass'] for x in observations) else 1)
