#!/usr/bin/env python3
"""recheck 10-21 (③) — do the new readback / diff D2 guards falsely refuse VALID generator decks?

Library path of the fixed tools at W (9412f384a): generator gm_arm → deck() text → readback d2_check · compare('GM'/'E') and
diff_decks(…, 'GM'/'E').  Grid over generation × stiffness × ρ (incl. non-round 9-digit values) × Bo (incl. rounding-edge
mantissas 1.000005 · 9.999995 …) × NCM surface states.  Records any false problem and, per check, the worst |deviation| / tolerance.
usage: python3 -I -B probe_falsereject.py <W>   (writes probe_falsereject.json)
"""
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
sys.path.insert(0, os.path.join(W, 'scripts'))


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


gen = load('make_mixer_deck', os.path.join(W, 'scripts', 'make_mixer_deck.py'))
rb = load('mixer_deck_readback', os.path.join(W, 'scripts', 'mixer_deck_readback.py'))
dd = load('mixer_deck_diff', os.path.join(W, 'scripts', 'mixer_deck_diff.py'))
TOL = rb.TOL
RHOS = [0.01, 0.0137, 0.03, 0.1, 0.123456789, 0.3, 0.31, 0.5, 0.70710678, 1.41421356, 3.14159265, 10.0, 31.6227766]
BOS = [1e-3, 0.0123456789, 0.21244, 0.5, 0.987654321, 1.000005, 1.0000049, 1.0000051, 9.999995, 9.9999951, 3.33333333, 123.456789,
       637.32]
if os.environ.get('FR_QUICK'):
    RHOS, BOS = RHOS[4:6], BOS[2:4]
res = dict(n_decks=0, n_refused=0, refused=[], false_problems=[], worst={}, gm_pairs=0, gm_false=[], e_pairs=0, e_false=[], worst_gm=0.0)
W_ = res['worst']


def upd(k, v, info):
    if v is not None and math.isfinite(v) and v > W_.get(k, (0.0, None))[0]:
        W_[k] = (v, info)


def dev_rows(R, D, info):
    tab = R['decl']['table'] if R['decl'] else {}
    for r_ in R['rows']:
        if 'expect' in r_:
            upd('law', abs(r_['F0_ratio'] / r_['expect'] - 1.0) / TOL['gm_law_rel'], info + ' ' + r_['pair'])
            h = tab.get(r_['pair'])
            if h:
                for col, key in (('ratio', 'F0_ratio'), ('F0', 'F0'), ('R_star', 'R_star'), ('E_star', 'E_star')):
                    hv = rb._dec(h[col])
                    if hv:
                        upd('hdr_' + col, abs(hv / r_[key] - 1.0) / TOL['gm_hdr_rel'], info + ' ' + r_['pair'])
                hv = rb._dec(h['ovl'])
                if hv is not None:
                    upd('hdr_ovl', abs(hv - r_['overlap'] * 100.0) / (TOL['gm_ovl_abs'] + TOL['gm_ovl_rel'] * r_['overlap'] * 100.0),
                        info + ' ' + r_['pair'])
            upd('ovl_vs_ceiling', r_['overlap'] / 0.01, info + ' ' + r_['pair'])
    if R.get('bo_read') is not None and R['decl']:
        upd('bo', abs(R['bo_read'] / R['decl']['bo_se'] - 1.0) / TOL['gm_bo_rel'], info)
    dc = R['decl']
    if dc:
        if dc['wall_rule'] == rb.D2_WALL_NCM:
            upd('q2_gw', abs(dc['gamma_wall'] / (rb.GM_WALL * dc['rho']) - 1.0) / TOL['gm_q2_rel'], info)
        else:
            upd('q2_rho_world', abs(dc['rho'] / (dc['gamma_wall'] / rb.GM_WALL) - 1.0) / TOL['gm_q2_rel'], info)


def make(gname, F, dtf, gam_p, gam_s, rho, bo, explicit=False):
    p = gen.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=gname)
    rpm = gen.resolve_rpm(p['R'])
    if explicit:
        a = gen.gm_arm({'AM_P': 1.0, 'AM_S': 1.0, 'SE': 1.0}, gamma_wall=gen.GM_WALL_HARE2026 * rho, bo_se=bo)
    else:
        a = gen.gm_arm({'AM_P': gam_p, 'AM_S': gam_s, 'SE': 1.0}, gamma_wall=gen.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
    nm = gen.register_arm('GMPROBE', a)
    try:
        return gen.deck(p, rpm, 2, arm=nm, hold_bo_pairwise=(F != 1.0), dt_factor=dtf)
    finally:
        gen.ARMS.pop(nm, None)


for gname in ('gen1', 'lab20261014'):
    for F, dtf in ((1.0, 1.0), (20.0, 1.0), (40.0, 0.5)):
        for rho in RHOS:
            for bo in BOS:
                decks = {}
                for st, pair in (('uu', (rho, rho)), ('cc', (1.0, 1.0)), ('cu', (1.0, rho)), ('uc', (rho, 1.0)), ('xx', None)):
                    gp, gs = pair or (1.0, 1.0)
                    info = f'{gname} F{F:g} dt{dtf:g} rho {rho:g} bo {bo:.9g} {st}'
                    try:
                        t = make(gname, F, dtf, gp, gs, rho, bo, explicit=(st == 'xx'))
                    except SystemExit as e:
                        res['n_refused'] += 1
                        if len(res['refused']) < 400:
                            res['refused'].append((info, str(e)[-90:]))
                        continue
                    res['n_decks'] += 1
                    D = rb.read_deck(t, info)
                    R = rb.d2_check(D)
                    if R['problems'] or not R['is_d2']:
                        res['false_problems'].append((info, R['problems'][:3]))
                    dev_rows(R, D, info)
                    decks[st] = (t, D)
                # same-ρ-world contrasts (GM) on both tools
                for a_, b_ in (('uu', 'cc'), ('cc', 'uu'), ('uu', 'cu'), ('uc', 'cc')):
                    if a_ in decks and b_ in decks:
                        res['gm_pairs'] += 1
                        A, B = rb.read_deck(decks[a_][0], a_), rb.read_deck(decks[b_][0], b_)
                        T = rb.compare('GM', A, B)
                        dfr = dd.diff_decks(decks[a_][0], decks[b_][0], 'GM')
                        if T['verdict'] != 'PASS' or dfr['verdict'] != 'PASS':
                            res['gm_false'].append((f'{gname} F{F:g} rho {rho:g} bo {bo:.9g} {a_}->{b_}', T['verdict'], T['failures'][:2],
                                                    dfr['verdict'], {k: dfr.get(k) for k in ('missing', 'outside', 'd2_rule', 'non_ced_diffs')
                                                                     if dfr.get(k)}))
                        for r_ in T['rows']:
                            if r_.get('expect_change') and r_.get('ratio'):
                                v = abs(r_['ratio'] / r_['expect'] - 1.0) / TOL['gm_mult_rel']
                                res['worst_gm'] = max(res['worst_gm'], v)
        print(gname, F, 'decks', res['n_decks'], 'refused', res['n_refused'], 'false', len(res['false_problems']), 'gm_pairs', res['gm_pairs'],
              'gm_false', len(res['gm_false']), flush=True)
# E pairs: soft → ×20 same arm (both generations, a few ρ / Bo)
for gname in ('gen1', 'lab20261014'):
    for rho in (0.1, 0.3, 3.14159265):
        for bo in (0.21244, 0.987654321, 9.999995):
            try:
                ts = make(gname, 1.0, 1.0, rho, rho, rho, bo)
                tr = make(gname, 20.0, 1.0, rho, rho, rho, bo)
            except SystemExit:
                continue
            res['e_pairs'] += 1
            T = rb.compare('E', rb.read_deck(ts, 's'), rb.read_deck(tr, 'r'))
            dfr = dd.diff_decks(ts, tr, 'E')
            if T['verdict'] != 'PASS' or dfr['verdict'] != 'PASS':
                res['e_false'].append((f'{gname} rho {rho:g} bo {bo:g}', T['verdict'], T['failures'][:2], dfr['verdict'], dfr.get('d2_rule')))
res['worst'] = {k: [round(v[0], 4), v[1]] for k, v in W_.items()}
json.dump(res, open(os.path.join(HERE, 'probe_falsereject.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ('n_decks', 'n_refused', 'gm_pairs', 'e_pairs', 'worst_gm')}, ensure_ascii=False))
print('false_problems', len(res['false_problems']), res['false_problems'][:3])
print('gm_false', len(res['gm_false']), res['gm_false'][:3])
print('e_false', len(res['e_false']), res['e_false'][:3])
print('worst (|dev|/tol)', json.dumps(res['worst'], ensure_ascii=False)[:1500])
