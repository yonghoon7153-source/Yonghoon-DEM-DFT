#!/usr/bin/env python3
"""Challenge resident R40 against isolated source mutations; never certify mutants."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
repo, out = args.repo.resolve(), args.out.resolve()
out.mkdir(parents=True)
relative = Path('docs/data/ps45_unload_20261009/ul_reader.py')
source = (repo / relative).read_text()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
mutations = [
    ('omit_raw_marker_rejection', "if marker != 'RESUME' and marker.strip() == 'RESUME':",
     "if False and marker != 'RESUME' and marker.strip() == 'RESUME':"),
    ('normalize_event_line_separators', "open(event_path, encoding='utf-8', errors='replace').read().split('\\n')",
     "open(event_path, encoding='utf-8', errors='replace').read().splitlines()"),
    ('ignore_marker_error_for_auth', '([], []) if pr or marker_pr else _resume_auth(d, events)',
     '([], []) if pr else _resume_auth(d, events)'),
    ('omit_manifest_separator_rejection', "if any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):",
     "if False and any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):"),
    ('select_manifest_key_before_separator_check', "if any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):",
     "if ln.strip().startswith('resume_from=') and any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):"),
]
child = '''
import sys,json
sys.path.insert(0,sys.argv[1]);import ul_reader as u
rows=[]
def check(name,cond,detail=''):
    ok=bool(cond() if callable(cond) else cond);rows.append({'case':name,'pass':ok})
u._resume_marker_tests(check,u.ul_lib.load_params())
print(json.dumps({'cases':rows,'passed':sum(r['pass'] for r in rows),'failed':[r['case'] for r in rows if not r['pass']]},ensure_ascii=False))
'''
reports = []
for name, old, new in mutations:
    assert source.count(old) == 1, name
    case = out / name
    working = case / 'repo'
    shutil.copytree(repo, working, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    changed = source.replace(old, new, 1)
    (working / relative).write_text(changed)
    temp = case / 'tmp'
    temp.mkdir()
    command = [sys.executable, '-I', '-c', child, str((working / relative).parent)]
    run = subprocess.run(command, capture_output=True, text=True, timeout=300,
                         env=dict(os.environ, TMPDIR=str(temp)))
    (case / 'stdout.json').write_text(run.stdout)
    (case / 'stderr.log').write_text(run.stderr)
    result = json.loads(run.stdout) if run.returncode == 0 else {}
    reports.append({'mutation': name, 'original_reader_sha256': sha(source.encode()),
                    'mutated_reader_sha256': sha(changed.encode()), 'probe_rc': run.returncode,
                    'case_count': len(result.get('cases', [])), 'failed_cases': result.get('failed'),
                    'detected': run.returncode == 0 and bool(result.get('failed'))})
    print(json.dumps(reports[-1], ensure_ascii=False), flush=True)
(out / 'report.json').write_text(json.dumps({'scope': 'Deliberately modified scratch sources, not approved consumers',
    'results': reports, 'all_detected': all(r['detected'] for r in reports)}, ensure_ascii=False, indent=2) + '\n')
raise SystemExit(0 if all(r['detected'] for r in reports) else 1)
