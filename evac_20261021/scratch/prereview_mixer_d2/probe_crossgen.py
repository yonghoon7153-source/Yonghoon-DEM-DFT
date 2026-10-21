#!/usr/bin/env python3
"""Probe H — cross-generation false-accept check of scripts/mixer_deck_diff.py (HEAD, read only):
a gen1 deck vs a lab20261014 deck of the same arm must NOT pass any allowlist (density is not an allowed difference).
Uses decks written by probe_tools.py in decks/tools/.  usage: python3 -I -B probe_crossgen.py <repo_worktree>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
DF = os.path.join(REPO, 'scripts', 'mixer_deck_diff.py')
T = os.path.join(HERE, 'decks', 'tools')
env = dict(os.environ, OPENBLAS_NUM_THREADS='1')
R = []
for allow, a, b in (('E', 'LC_soft_gen1', 'LC_ref20_lab'), ('E', 'LC_soft_gen1', 'LC_soft_lab'), ('U', 'LC_soft_gen1', 'LC_soft_lab'),
                    ('B', 'LC_soft_gen1', 'LC_soft_lab'), ('E', 'GM1_soft_gen1', 'GM1_ref20_lab'), ('U', 'GM1_soft_gen1', 'GM1_soft_lab')):
    p = subprocess.run([sys.executable, '-I', '-B', DF, os.path.join(T, a, 'in.mixer'), os.path.join(T, b, 'in.mixer'), '--allow', allow],
                       capture_output=True, text=True, env=env)
    R.append(dict(allow=allow, old=a, new=b, rc=p.returncode, tail=(p.stdout + p.stderr).strip().splitlines()[-4:]))
    print(allow, a, '->', b, 'rc', p.returncode, '|', ' / '.join(x.strip()[:110] for x in R[-1]['tail']))
json.dump(R, open(os.path.join(HERE, 'probe_crossgen.json'), 'w'), ensure_ascii=False, indent=1)
