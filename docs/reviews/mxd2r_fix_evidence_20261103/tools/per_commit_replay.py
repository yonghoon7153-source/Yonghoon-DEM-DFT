"""Per-commit replay of the D2 consumer regression (MXD2R-01 · 02 · 03 evidence).

Each <root>/<commit>/scripts/ is the `git archive <commit> scripts` tree of one commit.  This runs
that commit's own `scripts/test_mixer_d2_consumers.py` (python3 -I -X utf8 -B) and records, per test
method, ok / number of FAIL subtests / ERROR — so the before (tests-first commit) and after (each fix
commit) states are read from the same test file without editing it.

Usage: python3 -I per_commit_replay.py <root> <out.json> <commit> [<commit> ...]
"""
import hashlib
import json
import os
import re
import subprocess
import sys


def summarize(text):
    methods = {}
    for m in re.finditer(r'^(test_\w+) \(__main__\.D2Consumers\.\1\)', text, re.M):
        methods.setdefault(m.group(1), dict(fail_subtests=0, error=0))
    for m in re.finditer(r'^(FAIL|ERROR): (test_\w+) ', text, re.M):
        row = methods.setdefault(m.group(2), dict(fail_subtests=0, error=0))
        row['fail_subtests' if m.group(1) == 'FAIL' else 'error'] += 1
    for row in methods.values():
        row['status'] = 'ok' if not row['fail_subtests'] and not row['error'] else 'FAILED'
    ran = re.search(r'^Ran (\d+) tests? in', text, re.M)
    tail = re.search(r'^(OK|FAILED \([^)]*\))\s*$', text, re.M)
    return dict(ran=int(ran.group(1)) if ran else None, result=tail.group(1) if tail else None,
                methods=dict(sorted(methods.items())))


def main(root, out, *commits):
    report = dict(tool='per_commit_replay.py', python=sys.version.split()[0], commits={})
    for commit in commits:
        test = os.path.join(root, commit, 'scripts', 'test_mixer_d2_consumers.py')
        proc = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', test], capture_output=True)
        text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        with open(os.path.join(os.path.dirname(out), f'replay_{commit}.log'), 'w', encoding='utf-8') as f:
            f.write(text.replace(root, '<replay>'))
        files = {}
        for name in ('mixer_deck_readback.py', 'mixer_deck_diff.py', 'mixer_smoke_blind.py', 'test_mixer_d2_consumers.py'):
            with open(os.path.join(root, commit, 'scripts', name), 'rb') as f:
                files[name] = hashlib.sha256(f.read()).hexdigest()
        report['commits'][commit] = dict(rc=proc.returncode, files_sha256=files, **summarize(text))
        print(commit, 'rc', proc.returncode, report['commits'][commit]['result'])
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
