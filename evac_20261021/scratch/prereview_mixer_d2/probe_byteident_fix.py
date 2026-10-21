#!/usr/bin/env python3
"""Probe A — default-off path byte identity: pre-D2 generator (e432ec015) vs HEAD (a76f59d0d = cb5a6a445 file).

Library level: for every static arm x a matrix of plan/deck options, deck() text of the two modules must be byte-identical;
ced_matrix() equal; deck_meta() equal except generator_sha256 (stiffened / dt-factor decks).
CLI level: run both generators as subprocesses with identical argv into separate dirs; compare every output file's bytes
(deck_meta.json compared as JSON minus generator_sha256), stdout (out-dir prefix normalised), rc.

usage: python3 -I probe_byteident.py  (writes probe_byteident.json next to this file)
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'gen')
# recheck 10-21: OLD NEW OUTJSON from argv (default preD2 vs FIX)
OLD_F = os.path.join(GEN, sys.argv[1] if len(sys.argv) > 1 else 'mmd_preD2.py')
NEW_F = os.path.join(GEN, sys.argv[2] if len(sys.argv) > 2 else 'mmd_FIX.py')
OUT_JSON = os.path.join(HERE, sys.argv[3] if len(sys.argv) > 3 else 'probe_byteident_fix_preD2.json')


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


OLD = load(OLD_F, 'mmd_old')
NEW = load(NEW_F, 'mmd_new')
res = dict(lib=[], cli=[], summary={})


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def lib_case(label, plan_kw, deck_kw, arms, phases=None, meta=False):
    out = []
    for M in (OLD, NEW):
        if phases is not None:
            M.set_phases(phases)
    try:
        pO = OLD.plan(**plan_kw)
        pN = NEW.plan(**plan_kw)
        for arm in arms:
            rec = dict(case=label, arm=arm)
            try:
                rpm = deck_kw.get('rpm') or OLD.resolve_rpm(pO['R'])
                kw = {k: v for k, v in deck_kw.items() if k != 'rpm'}
                tO = OLD.deck(pO, rpm, kw.pop('revolutions', 2), arm=arm, **kw)
            except SystemExit as e:
                tO = f'SystemExit:{e}'
            try:
                rpmN = deck_kw.get('rpm') or NEW.resolve_rpm(pN['R'])
                kw = {k: v for k, v in deck_kw.items() if k != 'rpm'}
                tN = NEW.deck(pN, rpmN, kw.pop('revolutions', 2), arm=arm, **kw)
            except SystemExit as e:
                tN = f'SystemExit:{e}'
            rec['old_sha'] = sha(tO)
            rec['new_sha'] = sha(tN)
            rec['deck_identical'] = (tO == tN)
            rec['old_refused'] = tO.startswith('SystemExit:')
            try:
                rec['ced_identical'] = OLD.ced_matrix(arm, pO['d']) == NEW.ced_matrix(arm, pN['d'])
            except SystemExit:
                rec['ced_identical'] = 'refused'
            if meta and not rec['old_refused']:
                kw = {k: v for k, v in deck_kw.items() if k not in ('rpm', 'revolutions', 'layered', 'n_baffles', 'baffle_h')}
                mO = OLD.deck_meta(pO, rpm, deck_kw.get('revolutions', 2), kw.get('seed', 32452843), arm, tO,
                                   argv=['x'], hold_bo_pairwise=kw.get('hold_bo_pairwise', False),
                                   dt_factor=kw.get('dt_factor', 1.0), dump_full_precision=kw.get('dump_full_precision', False))
                mN = NEW.deck_meta(pN, rpmN, deck_kw.get('revolutions', 2), kw.get('seed', 32452843), arm, tN,
                                   argv=['x'], hold_bo_pairwise=kw.get('hold_bo_pairwise', False),
                                   dt_factor=kw.get('dt_factor', 1.0), dump_full_precision=kw.get('dump_full_precision', False))
                gO, gN = mO.pop('generator_sha256'), mN.pop('generator_sha256')
                rec['meta_identical_minus_gensha'] = json.dumps(mO, sort_keys=True) == json.dumps(mN, sort_keys=True)
                rec['meta_keys_old_minus_new'] = sorted(set(mO) - set(mN))
                rec['meta_keys_new_minus_old'] = sorted(set(mN) - set(mO))
            out.append(rec)
    finally:
        for M in (OLD, NEW):
            M.set_phases(('AM_P', 'AM_S', 'SE'))
    res['lib'].extend(out)
    return out


ARMS = sorted(OLD.ARMS)
COH = [a for a in ARMS if OLD.ARMS[a].get('bond', 0) > 0]
# 1 golden-style (plan(8000), rpm 60, 2 revs)
lib_case('plan8000_rpm60_rev2', dict(n_total=8000), dict(rpm=60, revolutions=2, seed=32452843), ARMS)
# 2 campaign plan 100k CGF 151.4 soft, rpm from Fr, 2 revs
lib_case('p100k_cgf151.4_soft', dict(n_total=100000, cgf=151.4), dict(revolutions=2, seed=32452843), ARMS)
# 3 layered override on all arms (layered=True) and False
lib_case('p100k_layeredTrue', dict(n_total=100000, cgf=151.4), dict(revolutions=2, seed=32452843, layered=True), ARMS)
lib_case('p100k_layeredFalse', dict(n_total=100000, cgf=151.4), dict(revolutions=2, seed=32452843, layered=False), ARMS)
# 4 stiffened x14/x20/x28/x40 + hold
for F in (14.0, 20.0, 28.0, 40.0):
    lib_case(f'p100k_stiff{F:g}_hold', dict(n_total=100000, cgf=151.4, stiffen_se=F),
             dict(revolutions=2, seed=32452843, hold_bo_pairwise=True), ARMS, meta=True)
# 5 stiffened without hold (refusal for cohesive arms; E0/L0 allowed)
lib_case('p100k_stiff20_nohold', dict(n_total=100000, cgf=151.4, stiffen_se=20.0),
         dict(revolutions=2, seed=32452843, hold_bo_pairwise=False), ARMS)
# 6 dt factor
lib_case('p100k_dthalf', dict(n_total=100000, cgf=151.4), dict(revolutions=2, seed=32452843, dt_factor=0.5), ARMS, meta=True)
lib_case('p100k_stiff20_dthalf', dict(n_total=100000, cgf=151.4, stiffen_se=20.0),
         dict(revolutions=2, seed=32452843, hold_bo_pairwise=True, dt_factor=0.5), ARMS, meta=True)
# 7 full precision dump
lib_case('p100k_stiff20_fullprec', dict(n_total=100000, cgf=151.4, stiffen_se=20.0),
         dict(revolutions=2, seed=32452843, hold_bo_pairwise=True, dump_full_precision=True), ARMS, meta=True)
# 8 baffles
lib_case('p100k_baffles3', dict(n_total=100000, cgf=151.4), dict(revolutions=2, seed=32452843, n_baffles=3, baffle_h=0.12), ARMS)
# 9 revolutions 0 (reference), other seeds, other CGF
lib_case('p100k_rev0_seed49979687', dict(n_total=100000, cgf=151.4), dict(revolutions=0, seed=49979687), ARMS)
lib_case('p30k_cgf200', dict(n_total=30000, cgf=200.0), dict(revolutions=5, seed=67867967), ARMS)
lib_case('p300k_cgf100', dict(n_total=300000, cgf=100.0), dict(revolutions=1, seed=32452843), ARMS)
# 10 five phases (fibres)
lib_case('5phase_plan8000', dict(n_total=8000), dict(rpm=60, revolutions=2, seed=32452843), ARMS,
         phases=('AM_P', 'AM_S', 'SE', 'VGCF', 'PTFE'))
lib_case('2phase_AMP_SE_plan8000', dict(n_total=8000), dict(rpm=60, revolutions=2, seed=32452843), ARMS,
         phases=('AM_P', 'SE'))

# ---- CLI level ---------------------------------------------------------------------------------------------------
CLI = [
    ('default', []),
    ('LC_campaign', ['--arm', 'LC', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '2', '--seed', '32452843']),
    ('LC_ref20', ['--arm', 'LC', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '2', '--seed', '32452843',
                  '--stiffen-se', '20', '--hold-bo-pairwise']),
    ('E0_ref20_rev0', ['--arm', 'E0', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '0', '--seed', '32452843',
                       '--stiffen-se', '20', '--hold-bo-pairwise']),
    ('LH_ref20_dthalf', ['--arm', 'LH', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '2', '--seed', '32452843',
                         '--stiffen-se', '20', '--hold-bo-pairwise', '--dt-factor', '0.5']),
    ('LU637_ref20_fullprec', ['--arm', 'LU637', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '2', '--seed', '32452843',
                              '--stiffen-se', '20', '--hold-bo-pairwise', '--dump-full-precision']),
    ('all_arms_8000_cgf151.4', ['--all-arms', '--n-total', '8000', '--cgf', '151.4', '--revolutions', '1']),
    ('all_arms_100k_ref20', ['--all-arms', '--n-total', '100000', '--cgf', '151.4', '--revolutions', '2',
                             '--stiffen-se', '20', '--hold-bo-pairwise']),
    ('all_arms_cgf200_refuse_LU637', ['--all-arms', '--n-total', '8000', '--revolutions', '1']),
    ('LA_baffles2', ['--arm', 'LA', '--baffles', '2', '--n-total', '8000']),
    ('E1_rpm60_offband', ['--arm', 'E1', '--rpm', '60', '--allow-off-band', '--n-total', '8000']),
    ('LC_stiff20_nohold_refuse', ['--arm', 'LC', '--n-total', '100000', '--cgf', '151.4', '--stiffen-se', '20']),
    ('composite_seed_refuse', ['--arm', 'LC', '--n-total', '8000', '--seed', '32452844']),
    ('no_out_print_only', None),   # special: no --out
]


def run_cli(gen, args, out):
    argv = [sys.executable, '-I', gen] + (['--out', out] if out else []) + args
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    return subprocess.run(argv, capture_output=True, text=True, env=env)


def tree(d):
    files = {}
    for root, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(root, f)
            files[os.path.relpath(p, d)] = open(p, 'rb').read()
    return files


with tempfile.TemporaryDirectory(dir=HERE) as td:
    for label, args in CLI:
        rec = dict(case=label)
        if args is None:
            a = run_cli(OLD_F, ['--arm', 'LC', '--n-total', '100000', '--cgf', '151.4', '--stiffen-se', '20', '--hold-bo-pairwise'], None)
            b = run_cli(NEW_F, ['--arm', 'LC', '--n-total', '100000', '--cgf', '151.4', '--stiffen-se', '20', '--hold-bo-pairwise'], None)
            rec.update(rc_old=a.returncode, rc_new=b.returncode, stdout_identical=a.stdout == b.stdout)
            res['cli'].append(rec)
            continue
        oa, ob = os.path.join(td, label, 'old'), os.path.join(td, label, 'new')
        a = run_cli(OLD_F, args, oa)
        b = run_cli(NEW_F, args, ob)
        rec.update(rc_old=a.returncode, rc_new=b.returncode)
        rec['stdout_identical'] = a.stdout.replace(oa, '<OUT>') == b.stdout.replace(ob, '<OUT>')
        if not rec['stdout_identical']:
            la = a.stdout.replace(oa, '<OUT>').splitlines()
            lb = b.stdout.replace(ob, '<OUT>').splitlines()
            rec['stdout_first_diff'] = [(x, y) for x, y in zip(la, lb) if x != y][:3]
        ta, tb = (tree(oa) if os.path.isdir(oa) else {}), (tree(ob) if os.path.isdir(ob) else {})
        rec['files_old'] = sorted(ta)
        rec['files_same_set'] = sorted(ta) == sorted(tb)
        diffs = []
        for f in sorted(set(ta) | set(tb)):
            if f not in ta or f not in tb:
                diffs.append(f + ' (missing on one side)')
                continue
            if f.endswith('deck_meta.json'):
                ja, jb = json.loads(ta[f]), json.loads(tb[f])
                ja.pop('generator_sha256'), jb.pop('generator_sha256')
                ja['argv'] = [x.replace(oa, '<OUT>') for x in ja['argv']]
                jb['argv'] = [x.replace(ob, '<OUT>') for x in jb['argv']]
                if json.dumps(ja, sort_keys=True) != json.dumps(jb, sort_keys=True):
                    diffs.append(f + ' (json differs beyond generator_sha256)')
            elif ta[f] != tb[f]:
                diffs.append(f)
        rec['file_diffs'] = diffs
        rec['n_files'] = len(ta)
        res['cli'].append(rec)

lib_bad = [r for r in res['lib'] if not (r['deck_identical'] and r['ced_identical'] in (True, 'refused')
                                        and r.get('meta_identical_minus_gensha', True))]
cli_bad = [r for r in res['cli'] if not (r['rc_old'] == r['rc_new'] and r['stdout_identical']
                                        and r.get('files_same_set', True) and not r.get('file_diffs'))]
res['summary'] = dict(lib_cases=len(res['lib']), lib_identical=len(res['lib']) - len(lib_bad),
                      lib_refused_both=sum(1 for r in res['lib'] if r['old_refused']),
                      cli_cases=len(res['cli']), cli_identical=len(res['cli']) - len(cli_bad),
                      cli_both_rc0=sum(1 for r in res['cli'] if r['rc_old'] == 0 and r['rc_new'] == 0),
                      cli_rc=[(r['case'], r['rc_old'], r['rc_new'], r.get('n_files')) for r in res['cli']],
                      cli_files_compared=sum(r.get('n_files', 0) for r in res['cli']),
                      lib_bad=lib_bad[:10], cli_bad=cli_bad[:10])
res['files'] = dict(old=OLD_F, new=NEW_F)
json.dump(res, open(OUT_JSON, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(res['summary'], ensure_ascii=False, indent=1)[:4000])
