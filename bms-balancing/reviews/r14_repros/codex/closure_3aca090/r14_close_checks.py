"""Read-only R14 closure checks of stored scientific metadata, not fitting."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
target = args.target.resolve()
def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=target, text=True).strip()
head = git('rev-parse', 'HEAD')
assert head == '3aca0906dcf0e8690ab534f0bef3abf6a02cdb9a'
assert git('status', '--porcelain') == ''
args.output.mkdir(parents=True, exist_ok=False)
checks = {
    'current_schema': ['--new', 'out', '--schema-only'],
    'legacy_schema': ['--new', 'out/archive/legacy_r6_u14', '--schema-only'],
    'new_vs_legacy': ['--new', 'out', '--old', 'out/archive/legacy_r6_u14'],
}
result = {'target_head': head, 'target_tree': git('rev-parse', 'HEAD^{tree}'), 'checks': {}}
for name, argv in checks.items():
    command = [sys.executable, '-B', 'scripts/check_u14.py', *argv]
    cp = subprocess.run(command, cwd=target, capture_output=True, timeout=180)
    for stream, data in [('stdout', cp.stdout), ('stderr', cp.stderr)]:
        (args.output/f'{name}.{stream}.txt').write_bytes(data)
    promotion = next((json.loads(line[10:]) for line in cp.stdout.decode('utf-8').splitlines()
                      if line.startswith('PROMOTION ')), None)
    result['checks'][name] = {'command': command, 'child_exit_code': cp.returncode,
        'promotion': promotion, 'stdout_sha256': hashlib.sha256(cp.stdout).hexdigest(),
        'stderr_sha256': hashlib.sha256(cp.stderr).hexdigest()}
    print(json.dumps({'case': name, 'rc': cp.returncode, 'promotion': promotion}), flush=True)
result['target_status_after'] = git('status', '--porcelain')
assert result['target_status_after'] == ''
(args.output/'results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
