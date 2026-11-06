"""Bounded implementation-side rerun; no simulator. Usage: python -I -B FILE OUT_DIR.

Run from the repository root. OUT_DIR must not exist. Mutations use a temporary
copy of scripts, never tracked implementation files. Historical evidence stays put.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path.cwd().resolve()
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=False)
OLD = Path('docs/reviews/mxd2r_fix_evidence_20261103')
CASE_ROOT = Path('docs/reviews/codex_mixer_d2_review_20261027')
CORE = ['scripts/' + n + '.py' for n in (
    'mixer_deck_readback', 'mixer_deck_diff', 'mixer_smoke_blind', 'test_mixer_d2_consumers')]
env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR='/tmp')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_dependencies(paths):
    seen, todo = set(), list(map(Path, paths))
    while todo:
        path = todo.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names = [n.name for n in node.names] if isinstance(node, ast.Import) else (
                [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            for name in names:
                dep = Path('scripts') / (name.split('.')[0] + '.py')
                if dep.is_file() and dep not in seen:
                    todo.append(dep)
    return sorted(map(str, seen))


tools = [OLD / 'mxd2r04/tools/preattack_probe_v3.py',
         OLD / 'mxd2r04/tools/positive_extra.py',
         OLD / 'mxd2r04/tools/mutation_check_v4.py',
         OLD / 'mxd2r04/tools/mutation_check_v3.py', OLD / 'tools/mutation_check.py',
         OLD / 'tools/preattack_outside_scope.py',
         CASE_ROOT / '_repro_ours_20261030/tools/run_d2_cli_cases.py']
sources = local_dependencies(CORE) + list(map(str, tools))
before = {p: sha(p) for p in sources}
report = dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
              head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              thread_environment={k: env[k] for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS',
                                                    'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')},
              sources_sha256=before, commands=[])


def run(name, args):
    cmd = [sys.executable, '-I', '-X', 'utf8', '-B', *map(str, args)]
    start = time.monotonic()
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, timeout=300)
    raw = proc.stdout + proc.stderr
    (OUT / (name + '.log')).write_bytes(raw)
    report['commands'].append(dict(name=name, argv=cmd, rc=proc.returncode,
                                   elapsed_seconds=round(time.monotonic()-start, 3),
                                   log=name + '.log', log_sha256=hashlib.sha256(raw).hexdigest()))
    print(name, 'rc', proc.returncode, flush=True)


run('d2_consumers', ['scripts/test_mixer_d2_consumers.py'])
for key in ('readback', 'diff', 'smoke'):
    script = {'readback': CORE[0], 'diff': CORE[1], 'smoke': CORE[2]}[key]
    run(key + '_selftest', [script, '--selftest'])
run('external_cli_cases', [tools[-1], ROOT / 'scripts', ROOT / CASE_ROOT / 'd2/evidence/cases',
                           'current', OUT / 'external_cli_cases'])
run('preattack_probe_v3', [tools[0], ROOT / 'scripts', OUT / 'preattack_probe_v3.json'])
run('outside_scope', [tools[-2], ROOT / 'scripts', OUT / 'outside_scope.json'])
run('positive_extra', [tools[1], ROOT / 'scripts'])
with tempfile.TemporaryDirectory(prefix='mxd2r-recheck-', dir='/tmp') as tmp:
    scripts = Path(tmp) / 'scripts'
    shutil.copytree(ROOT / 'scripts', scripts, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    scratch_before = {p: sha(scripts / Path(p).name) for p in CORE}
    run('mutation_subset', [tools[2], scripts, OUT / 'mutation_subset.json',
                            'M01 ', 'M06 ', 'M16 ', 'M21 ', 'M31 ', 'M55 '])
    report['scratch_core_restored'] = scratch_before == {p: sha(scripts / Path(p).name) for p in CORE}
report['sources_unchanged'] = before == {p: sha(p) for p in sources}
(OUT / 'run_summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
assert report['sources_unchanged'] and report['scratch_core_restored']
assert all(row['rc'] == 0 for row in report['commands']), 'Inspect retained command logs'
