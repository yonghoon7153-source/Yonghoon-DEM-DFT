#!/usr/bin/env python3
"""recheck 10-21 — the first review's 9 D2 decks: old HEAD generator (a76f59d0d, gen/mmd_HEAD.py) vs fixed (9412f384a, gen/mmd_FIX.py).

Per case: rc both · refusal text (fixed) · non-comment logical command tokens identical? · comment lines added/removed ·
deck_meta key diff (minus generator_sha256 · argv · deck_sha256 · deck_bytes) · my independent readback (probe_d2_readback.analyse)
on the fixed deck.  Extra Q2-valid cases (cu · uc · coated-world explicit · rho 10 Bo 300 · rho 1e-6 / 1e6 edges) on the fixed generator.
usage: python3 -I -B probe_regen9.py   (writes probe_regen9.json)
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, 'gen', 'mmd_HEAD.py')
NEW = os.path.join(HERE, 'gen', 'mmd_FIX.py')
spec = importlib.util.spec_from_file_location('pdr', os.path.join(HERE, 'probe_d2_readback.py'))
pdr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pdr)
BASE = pdr.BASE
EXTRA = [
    ('cu_r03_ncm_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5', '--dens-gen', 'lab20261014'],
     {'AM_P': 1, 'AM_S': .3, 'SE': 1}, 0.0256 * 0.3, 0.5),
    ('uc_r03_ncm_lab_ref20', ['--gm-gamma', 'AM_P=0.3,AM_S=1', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5', '--dens-gen', 'lab20261014',
                              '--stiffen-se', '20', '--hold-bo-pairwise'], {'AM_P': .3, 'AM_S': 1, 'SE': 1}, 0.0256 * 0.3, 0.5),
    ('uu_r03_ncm_gen1_ref40_dthalf', ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5', '--dens-gen', 'gen1',
                                      '--stiffen-se', '40', '--hold-bo-pairwise', '--dt-factor', '0.5'],
     {'AM_P': .3, 'AM_S': .3, 'SE': 1}, 0.0256 * 0.3, 0.5),
    ('cc_explicit_w00768_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.00768', '--gm-bo-se', '0.5', '--dens-gen', 'lab20261014'],
     {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.00768, 0.5),
    ('uu_r10_ncm_lab_bo300', ['--gm-gamma', 'AM_P=10,AM_S=10', '--gm-wall-ncm', '10', '--gm-bo-se', '300', '--dens-gen', 'lab20261014'],
     {'AM_P': 10, 'AM_S': 10, 'SE': 1}, 0.256, 300.0),
    ('uu_r1e-6_ncm_lab', ['--gm-gamma', 'AM_P=1e-6,AM_S=1e-6', '--gm-wall-ncm', '1e-6', '--gm-bo-se', '0.5', '--dens-gen', 'lab20261014'],
     {'AM_P': 1e-6, 'AM_S': 1e-6, 'SE': 1}, 0.0256e-6, 0.5),
    ('uu_r1e6_ncm_lab_bo1e-6', ['--gm-gamma', 'AM_P=1e6,AM_S=1e6', '--gm-wall-ncm', '1e6', '--gm-bo-se', '1e-6', '--dens-gen', 'lab20261014'],
     {'AM_P': 1e6, 'AM_S': 1e6, 'SE': 1}, 0.0256e6, 1e-6),
    ('cc_r1_ncm_lab_bo1e4', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-wall-ncm', '1', '--gm-bo-se', '1e4', '--dens-gen', 'lab20261014'],
     {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256, 1e4),
    ('uu_r03_ncm_lab_bo1010', ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '1010', '--dens-gen', 'lab20261014'],
     {'AM_P': .3, 'AM_S': .3, 'SE': 1}, 0.0256 * 0.3, 1010.0),
]


def gen(g, out, args):
    p = subprocess.run([sys.executable, '-I', '-B', g, '--out', out] + BASE + args, capture_output=True, text=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS='1'))
    dk = os.path.join(out, 'in.mixer')
    mp = os.path.join(out, 'deck_meta.json')
    return (p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] if p.returncode else [],
            open(dk, encoding='utf-8').read() if os.path.exists(dk) else None,
            json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else None)


def comments(t):
    return [l for l in t.split('\n') if l.lstrip().startswith('#')]


VOL = ('generator_sha256', 'argv', 'deck_sha256', 'deck_bytes')


def meta_diff(a, b):
    ka, kb = set(a) - set(VOL), set(b) - set(VOL)
    out = dict(only_old=sorted(ka - kb), only_new=sorted(kb - ka), changed=[])
    for k in sorted(ka & kb):
        if a[k] != b[k]:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                sub = sorted(x for x in set(a[k]) | set(b[k]) if a[k].get(x) != b[k].get(x))
                out['changed'].append(f'{k}.{{{",".join(sub)}}}')
            else:
                out['changed'].append(k)
    return out


res = dict(regen=[], extra=[])
with tempfile.TemporaryDirectory(dir=HERE) as td:
    for label, args, gamma, gw, bo in pdr.CASES:
        ro = gen(OLD, os.path.join(td, 'o_' + label), args)
        rn = gen(NEW, os.path.join(td, 'n_' + label), args)
        rec = dict(case=label, rc_old=ro[0], rc_new=rn[0], refuse_new=rn[1])
        if ro[2] is not None and rn[2] is not None:
            lo, ln_ = pdr.logical(ro[2]), pdr.logical(rn[2])
            rec['noncomment_tokens_identical'] = lo == ln_
            co, cn = comments(ro[2]), comments(rn[2])
            rec['comment_removed'] = [c for c in co if c not in cn][:12]
            rec['comment_added'] = [c for c in cn if c not in co][:12]
            rec['meta_diff'] = meta_diff(ro[3], rn[3])
            rec['pairs_table_identical'] = ro[3].get('pairs') == rn[3].get('pairs')
            rec['readback_new'] = {k: v for k, v in pdr.analyse(rn[2], rn[3], gamma, gw, bo).items() if k != 'rows'}
        res['regen'].append(rec)
        print(f"{label:34s} old rc {ro[0]} · new rc {rn[0]} {rn[1]}  tok_same={rec.get('noncomment_tokens_identical')} "
              f"pairs_same={rec.get('pairs_table_identical')} meta={rec.get('meta_diff')}")
    for label, args, gamma, gw, bo in EXTRA:
        rn = gen(NEW, os.path.join(td, 'x_' + label), args)
        rec = dict(case=label, rc_new=rn[0], refuse_new=rn[1])
        if rn[2] is not None:
            a_ = pdr.analyse(rn[2], rn[3], gamma, gw, bo)
            rec['readback_new'] = {k: v for k, v in a_.items() if k != 'rows'}
            rec['rows'] = [(r_['pair'], r_.get('rel'), r_.get('delta0_over_rmin')) for r_ in a_['rows']]
            rec['meta_adhesion_rule'] = rn[3].get('adhesion_rule')
            rec['meta_schema'] = rn[3].get('schema')
            rec['meta_registered'] = rn[3].get('registered')
            rec['header_wall_lines'] = [l for l in rn[2].split('\n') if '벽' in l and l.startswith('#')][:6]
        res['extra'].append(rec)
        rb = rec.get('readback_new') or {}
        print(f"{label:34s} new rc {rn[0]} {rn[1]} maxrelF0={rb.get('max_rel_F0')} BoRel={rb.get('bo_se_rel')} "
              f"d0max={rb.get('worst_delta0_over_rmin')} hdr={rb.get('header_rows')}:{rb.get('header_vs_mine_max_rel')}")
json.dump(res, open(os.path.join(HERE, 'probe_regen9.json'), 'w'), ensure_ascii=False, indent=1)
