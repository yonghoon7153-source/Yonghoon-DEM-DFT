#!/usr/bin/env python3
"""Pre-attack final — symlinked work root (ibb: <HOME> -> <LUSTRE_HOME>, evidence = RJ 323957 manifest
line 19 'verdict=<HOME>/…' ↔ 'run_dir=<LUSTRE_HOME>/…' = os.path.dirname(os.path.realpath(verdict))).
Shows: character equality of the RT2 log path against '<run>/RT1/rt.bin' holds for the runner-form run dir but fails
for the realpath-form run dir that grammar_prereq-style re-reads use (ul_reader.py 1509 · 1550).
Also: '${'-free read_restart line count when a generator header comment mentions read_restart.  Scratch only."""
import os
import sys
import tempfile

with tempfile.TemporaryDirectory(prefix='pfa_path_', dir=os.path.dirname(os.path.abspath(__file__))) as td:
    real = os.path.join(td, 'lustre', 'home', 'u')
    os.makedirs(os.path.join(real, 'hist', 'rtg_1', 'RT1'))
    os.makedirs(os.path.join(td, 'home'))
    os.symlink(real, os.path.join(td, 'home', 'u'))            # <HOME> -> <LUSTRE_HOME>
    run_runner_form = os.path.join(td, 'home', 'u', 'hist', 'rtg_1')   # what run_history.sh builds from $HOME
    ckpt = os.path.join(run_runner_form, 'RT1', 'rt.bin')       # -var ckpt · ckpt.txt · LIGGGHTS log echo
    open(ckpt, 'wb').write(b'x')
    verdict = os.path.join(run_runner_form, 'rt_grammar_verdict.json')
    rd = os.path.dirname(os.path.realpath(verdict))            # grammar_prereq form (ul_reader.py 1509)
    log_path = ckpt                                             # substituted read_restart line in RT2 log
    for label, run in (('first read (runner form)', run_runner_form), ('prereq re-read (realpath form)', rd)):
        exp = os.path.join(run, 'RT1', 'rt.bin')
        print(f'{label:34s} char-equal {log_path == exp!s:5s} · realpath-equal {os.path.realpath(log_path) == os.path.realpath(exp)}')

# header comment hazard: LIGGGHTS echoes every input line (comments included) to the log
log = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0 ...)',
       '# DEM 언로딩 키트 — ps_7_3_r45 · RT2 — RT1 의 rt.bin 을 read_restart 해 같은 경로 P (G2c′ D2)',
       'read_restart ${ckpt}', 'read_restart <HOME>/ps45/ps_7_3_r45/RJ/RT1/rt.bin']
sub = [l for l in log if 'read_restart' in l and '${' not in l]
cmd = [l for l in log if l.split()[:1] == ['read_restart'] and '${' not in l]
print('substring rule: lines =', len(sub), '(→ "둘 이상" SYNTAX_FAIL) · first-token rule: lines =', len(cmd))
sys.exit(0)
