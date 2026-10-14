#!/usr/bin/env python3
"""Run the unloading-kit self-tests and checks; save full logs + rc per command.

    python3 run_suite.py <kit_dir> <out_dir> [name ...]
"""
import json
import os
import platform
import subprocess
import sys
import time

CMDS = [
    ('ul_lib_selftest', ['ul_lib.py', '--selftest']),
    ('ul_s3_selftest', ['ul_s3.py', '--selftest']),
    ('ul_observers_selftest', ['ul_observers.py', '--selftest']),
    ('ul_gates_selftest', ['ul_gates.py', '--selftest']),
    ('ul_reader_selftest', ['ul_reader.py', '--selftest']),
    ('seal_kit_selftest', ['seal_kit.py', '--selftest']),
    ('seal_kit_check', ['seal_kit.py', '--check']),
    ('make_unload_decks_selftest', ['make_unload_decks.py', '--selftest']),
    ('make_unload_decks_check', ['make_unload_decks.py', '--check']),
    ('history_make_history_decks_selftest', ['history_test/make_history_decks.py', '--selftest']),
    ('history_make_history_decks_check', ['history_test/make_history_decks.py', '--check']),
    ('history_read_history_selftest', ['history_test/read_history.py', '--selftest']),
    ('ul_runner_test_selftest', ['ul_runner_test.py', '--selftest']),
]


def main():
    kit, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    want = set(sys.argv[3:])
    os.makedirs(out, exist_ok=True)
    def sh(p):
        import hashlib
        return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None
    git = lambda *a: subprocess.run(['git', '-C', kit] + list(a), capture_output=True, text=True).stdout.strip()  # noqa: E731
    summ = {'python': sys.version.split()[0], 'platform': platform.platform(),
            'bash': subprocess.run(['bash', '--version'], capture_output=True, text=True).stdout.splitlines()[0],
            'kit': os.path.relpath(kit, git('rev-parse', '--show-toplevel') or kit), 'git_head': git('rev-parse', 'HEAD'),
            'git_dirty_paths': git('status', '--porcelain', '--', '.').splitlines(),
            'kit_SHA256SUMS_sha256': sh(os.path.join(kit, 'SHA256SUMS')),
            'history_SHA256SUMS_sha256': sh(os.path.join(kit, 'history_test', 'SHA256SUMS')),
            'README_sha256': sh(os.path.join(kit, 'README.md')), 'results': []}
    for name, args in CMDS:
        if want and name not in want:
            continue
        t0 = time.time()
        p = subprocess.run([sys.executable, '-I', os.path.join(kit, args[0])] + args[1:], cwd=kit, capture_output=True, text=True,
                           timeout=3600)
        dt = time.time() - t0
        txt = (f'$ python3 -I {args[0]} {" ".join(args[1:])}\n# cwd = kit folder · rc = {p.returncode} · {dt:.1f} s\n'
               f'# ── stdout ──\n{p.stdout}# ── stderr ──\n{p.stderr}# ── rc = {p.returncode} ──\n')
        with open(os.path.join(out, f'{name}.log'), 'w', encoding='utf-8') as f:
            f.write(txt)
        lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
        n_ok = sum(1 for ln in lines if ln.lstrip().startswith('✓'))
        n_bad = sum(1 for ln in lines if ln.lstrip().startswith('✗'))
        last = lines[-1] if lines else ''
        summ['results'].append({'name': name, 'cmd': ['python3', '-I'] + args, 'rc': p.returncode, 'seconds': round(dt, 1),
                                'n_check_lines_ok': n_ok, 'n_check_lines_fail': n_bad, 'last_line': last})
        print(f'{name:40s} rc={p.returncode} ok={n_ok} fail={n_bad} {dt:6.1f}s  {last[:90]}', flush=True)
    with open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summ, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main()
