"""Run one of our repo tests with temp / webapp / matplotlib folders redirected.

usage: python3 -I run_ours.py <repo_root> <out_prefix> <script_rel_or_abs> [args...]
Writes <out_prefix>.log (stdout + stderr) and <out_prefix>.json (rc, seconds,
command, environment, sha256 of the script before/after, tail).
Thread counts are fixed to 1 (same as the Codex wrapper). Runs with -B so no
__pycache__ is written into the repo.
"""
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def main():
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    script = Path(sys.argv[3])
    if not script.is_absolute():
        script = repo / script
    args = sys.argv[4:]
    tmp = out.parent.parent / 'tmp' / out.name
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS'):
        env[k] = '1'
    env['TMPDIR'] = env['TEMP'] = env['TMP'] = str(tmp)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['MPLCONFIGDIR'] = str(tmp / 'mpl')
    for k in ('UPLOAD', 'RESULTS', 'ARCHIVE', 'MPM_LAB', 'EIS'):
        env[f'WEBAPP_{k}_FOLDER'] = str(tmp / k.lower())
    before = hashlib.sha256(script.read_bytes()).hexdigest()
    cmd = [sys.executable, '-B', str(script), *args]
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=str(repo), env=env, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    secs = time.perf_counter() - t0
    after = hashlib.sha256(script.read_bytes()).hexdigest()
    out.with_suffix('.log').write_text(p.stdout + '\n--- STDERR ---\n' + p.stderr, encoding='utf-8')
    meta = dict(command=cmd, cwd=str(repo), returncode=p.returncode, seconds=round(secs, 2),
                python=sys.version.split()[0], platform=platform.platform(),
                script_sha256_before=before, script_sha256_after=after,
                unchanged=before == after,
                stdout_tail=p.stdout.splitlines()[-3:],
                environment={k: env[k] for k in env if k.startswith('WEBAPP_') or k in (
                    'TMPDIR', 'TEMP', 'TMP', 'MPLCONFIGDIR', 'OMP_NUM_THREADS',
                    'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')})
    out.with_suffix('.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(rc=p.returncode, seconds=meta['seconds'],
                          tail=meta['stdout_tail'][-1:] if meta['stdout_tail'] else []),
                     ensure_ascii=False))
    sys.exit(0)


if __name__ == '__main__':
    main()
