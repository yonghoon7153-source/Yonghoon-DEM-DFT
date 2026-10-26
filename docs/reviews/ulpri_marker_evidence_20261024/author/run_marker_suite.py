#!/usr/bin/env python3
"""Run the existing 13 kit commands on explicit source, preserving raw receipts."""
from pathlib import Path
import argparse
import ast
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
repo, out = args.repo.resolve(), args.out.resolve()
out.mkdir(parents=True)
kit = repo / 'docs/data/ps45_unload_20261009'
driver = repo / 'docs/reviews/ulpr_resume_integer_evidence_20261024/author/run_suite.py'
tree = ast.parse(driver.read_text())
commands = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'CMDS' for t in node.targets))
assert len(commands) == 13
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
def identity():
    return {str(p.relative_to(kit)): sha(p) for p in sorted(kit.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
before = identity()
temp = out / 'tmp'
temp.mkdir()
env = dict(os.environ, TMPDIR=str(temp), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
receipt = {'schema': 'ulpri_kit_direct_suite_v1', 'source_kind': 'frozen scratch working files',
           'base_consumer': '01c1aaf5be8acdf7d1716f34cc86fc77d8e27362',
           'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'python': sys.version, 'command_list_source_sha256': sha(driver), 'source_sha256': before,
           'new_physical_runs': 0, 'shared_gate_included': False, 'status': 'RUNNING', 'results': []}
def save():
    (out / 'summary.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
save()
for name, command_args in commands:
    command = [sys.executable, '-I', str(kit / command_args[0]), *command_args[1:]]
    start = time.monotonic()
    run = subprocess.run(command, cwd=kit, env=env, capture_output=True, text=True, timeout=3600)
    log = out / (name + '.log')
    log.write_text(run.stdout + '\n--- stderr ---\n' + run.stderr)
    lines = run.stdout.splitlines()
    row = {'name': name, 'command': command, 'exit_code': run.returncode,
           'seconds': round(time.monotonic() - start, 3), 'log': log.name, 'log_sha256': sha(log),
           'pass_lines': sum(line.lstrip().startswith('✓') for line in lines),
           'fail_lines': sum(line.lstrip().startswith('✗') for line in lines)}
    receipt['results'].append(row)
    save()
    print(json.dumps(row), flush=True)
receipt['source_unchanged'] = before == identity()
receipt['finished_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt['status'] = 'PASS' if receipt['source_unchanged'] and all(r['exit_code'] == 0 and r['fail_lines'] == 0 for r in receipt['results']) else 'FAIL'
save()
raise SystemExit(0 if receipt['status'] == 'PASS' else 1)
