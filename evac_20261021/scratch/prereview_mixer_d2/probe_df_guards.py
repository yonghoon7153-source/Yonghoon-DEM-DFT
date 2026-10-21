#!/usr/bin/env python3
"""recheck 10-21 — fixed deck diff GM guards fire on single edits?  (rule-unchanged element changed · changed element with wrong
multiplier · wall-wall nonzero · asymmetric CED)  usage: python3 -I -B probe_df_guards.py <W>"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
sys.path.insert(0, os.path.join(W, 'scripts'))
s = importlib.util.spec_from_file_location('mixer_deck_diff', os.path.join(W, 'scripts', 'mixer_deck_diff.py'))
dd = importlib.util.module_from_spec(s)
sys.modules['mixer_deck_diff'] = dd
s.loader.exec_module(dd)
R = os.path.join(HERE, 'decks', 'recheck')
U = open(os.path.join(R, 'GMuu_ref20_lab', 'in.mixer'), encoding='utf-8').read()
C = open(os.path.join(R, 'GMcc_ref20_lab', 'in.mixer'), encoding='utf-8').read()


def ced_block(t):
    m = re.search(r'(?m)^fix mC .*\n((?:    .*\n){4})', t)
    return m


def set_ced(t, i, j, newtok, sym=True):
    m = ced_block(t)
    lines = m.group(1).split('\n')[:4]
    rows = [ln.rstrip().rstrip('&').split() for ln in lines]
    rows[i][j] = newtok
    if sym:
        rows[j][i] = newtok
    new = ''.join('    ' + ' '.join(r) + (' &' if k < 3 else '') + '\n' for k, r in enumerate(rows))
    return t[:m.start(1)] + new + t[m.end(1):]


def get_ced(t, i, j):
    m = ced_block(t)
    return float(m.group(1).split('\n')[i].rstrip().rstrip('&').split()[j])


cases = {
    'control uu->cc': (U, C, None),
    'SE-SE (rule-unchanged) x1.01 in cc': (U, set_ced(C, 2, 2, f'{get_ced(C, 2, 2) * 1.01:g}'), 'outside'),
    'SE-WALL (rule-unchanged) x1.001 in cc': (U, set_ced(C, 2, 3, f'{get_ced(C, 2, 3) * 1.001:g}'), 'outside'),
    'AM_S-SE (changed) x1.0001 extra in cc': (U, set_ced(C, 1, 2, f'{get_ced(C, 1, 2) * 1.0001:g}'), 'd2_rule'),
    'WALL-WALL nonzero in cc': (U, set_ced(C, 3, 3, '1'), 'd2_rule'),
    'asymmetric AM_P-AM_S in cc': (U, set_ced(C, 0, 1, f'{get_ced(C, 0, 1) * 1.01:g}', sym=False), 'non_ced_diffs'),
}
res = {}
for k, (a, b, key) in cases.items():
    r = dd.diff_decks(a, b, 'GM')
    res[k] = dict(verdict=r['verdict'], outside=r.get('outside'), missing=r.get('missing'), d2_rule=[x[:140] for x in (r.get('d2_rule') or [])][:3],
                  non_ced=[x[:120] for x in (r.get('non_ced_diffs') or [])][:2])
    print(k, '->', r['verdict'], '| outside', r.get('outside'), '| d2', (r.get('d2_rule') or [''])[0][:110], '| nonced', (r.get('non_ced_diffs') or [''])[0][:80])
json.dump(res, open(os.path.join(HERE, 'probe_df_guards.json'), 'w'), ensure_ascii=False, indent=1)
