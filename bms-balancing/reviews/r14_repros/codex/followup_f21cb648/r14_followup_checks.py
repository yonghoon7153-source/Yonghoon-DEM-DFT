"""R14 follow-up: ordinary metadata/CLI checks only, no fitting or replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED = 'f21cb6480fc27857c7aac67e823cae62b1443830'
parser = argparse.ArgumentParser()
parser.add_argument('--target', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
target = args.target.resolve()
args.output.mkdir(parents=True, exist_ok=False)
def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=target, text=True).strip()
assert git('rev-parse', 'HEAD') == EXPECTED
assert git('status', '--porcelain') == ''
checks = {
    'current_schema': ['scripts/check_u14.py', '--new', 'out', '--schema-only'],
    'legacy_schema': ['scripts/check_u14.py', '--new', 'out/archive/legacy_r6_u14', '--schema-only'],
    'new_vs_legacy': ['scripts/check_u14.py', '--new', 'out', '--old', 'out/archive/legacy_r6_u14'],
    'new_vs_current_head': ['scripts/check_u14.py', '--new', 'out', '--old-rev', 'HEAD'],
    'new_vs_prepromotion': ['scripts/check_u14.py', '--new', 'out', '--old-rev', '42314198e0beee59834d394cdba2757183503b59'],
}
result = {'target_head': EXPECTED, 'target_tree': git('rev-parse', 'HEAD^{tree}'), 'checks': {}}
for name, argv in checks.items():
    command = [sys.executable, '-B', *argv]
    cp = subprocess.run(command, cwd=target, capture_output=True, timeout=180)
    stdout = cp.stdout.decode('utf-8', errors='replace')
    for stream, data in [('stdout', cp.stdout), ('stderr', cp.stderr)]:
        (args.output / f'{name}.{stream}.txt').write_bytes(data)
    promotion = next((json.loads(line.removeprefix('PROMOTION '))
                      for line in stdout.splitlines() if line.startswith('PROMOTION ')), None)
    result['checks'][name] = {'command': command, 'child_exit_code': cp.returncode,
                             'promotion': promotion,
                             'stdout_sha256': hashlib.sha256(cp.stdout).hexdigest(),
                             'stderr_sha256': hashlib.sha256(cp.stderr).hexdigest()}
    print(json.dumps({'case': name, 'rc': cp.returncode, 'promotion': promotion}), flush=True)
result['target_status_after'] = git('status', '--porcelain')
assert result['target_status_after'] == ''
(args.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
