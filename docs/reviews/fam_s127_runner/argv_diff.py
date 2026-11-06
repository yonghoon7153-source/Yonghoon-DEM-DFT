#!/usr/bin/env python3
"""Token diff: argv the runner passed (recorded by the fake python) vs the RAW registration text.

Raw = s12-7 block with $COMMON/$COMMON7 expanded, NO amendment, `$PY` and `<OUT>` kept literal.
The runner's argv is normalised back to `$PY` / `<OUT>` so the only remaining differences are real.
usage: argv_diff.py PREREG SCENARIO_DIR
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expected_argv as E  # noqa: E402

prereg, sdir = sys.argv[1], sys.argv[2]
home = os.path.join(sdir, 'home')
py, out = os.path.join(home, 'fam-mpm310', 'bin', 'python'), os.path.join(home, 'fam_s127')
lines = open(prereg, encoding='utf-8').readlines()
E.amend = lambda t: list(t)                      # raw registration text: no amendment
raw, _, where = E.from_block(lines, '$PY', '<OUT>')
print('registration block lines %s (heading, ```bash, ```)' % (where,))
for arm in E.ARMS:
    got = open(os.path.join(sdir, 'fake', 'argv_' + arm), 'rb').read().split(b'\0')[:-1]
    got = [g.decode() for g in got]
    norm = ['$PY' if g == py else g.replace(out, '<OUT>') for g in got]
    reg = raw[arm]
    diffs = [(i, r, n) for i, (r, n) in enumerate(zip(reg, norm)) if r != n]
    same_len = len(reg) == len(norm)
    print('%-10s tokens reg=%d runner=%d  diffs=%s' % (arm, len(reg), len(norm),
          ', '.join('#%d %s→%s (after %s)' % (i, r, n, reg[i - 1]) for i, r, n in diffs) or 'none'))
    if not same_len:
        print('  LENGTH DIFFERS')
    print('  runner argv: ' + ' '.join(norm))
