#!/usr/bin/env python3
"""recheck 10-21 — the FIXED tools (worktree W = 9412f384a) on decks from the FIXED generator (gen/mmd_FIX.py).

Stages (each well under 60 s; run one at a time):
  decks  — generate Q2-valid D2 decks + old-arm decks (CLI) into decks/recheck/<name>/
  rb     — scripts/mixer_deck_readback.py --table <K> A B --json  (original MXD2-01 (a)(b) counterexamples + same-class pairs)
  df     — scripts/mixer_deck_diff.py A B --allow <K> [--expect-deck]  (two-deck mode)
  mut    — mutant generators (M04 · M05 · M16 · M06 · N15 · N25) → their decks → readback / diff (are they caught downstream?)
  runs   — --runs mode with D2 cell names (d2_cli_args) incl. meta absent / meta Bo tamper / deck tamper
  edge   — CLI numeric tokens of other options · rho near 1 · name grammar vs generator range
Results accumulate in probe_recheck_tools.json (one key per stage).
usage: python3 -I -B probe_recheck_tools.py <W> <stage>
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
STAGE = sys.argv[2]
GEN = os.path.join(HERE, 'gen', 'mmd_FIX.py')
RB = os.path.join(W, 'scripts', 'mixer_deck_readback.py')
DF = os.path.join(W, 'scripts', 'mixer_deck_diff.py')
OUT = os.path.join(HERE, 'decks', 'recheck')
JS = os.path.join(HERE, 'probe_recheck_tools.json')
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']
LAB, G1 = ['--dens-gen', 'lab20261014'], ['--dens-gen', 'gen1']
R20, R40, DTH = ['--stiffen-se', '20', '--hold-bo-pairwise'], ['--stiffen-se', '40', '--hold-bo-pairwise'], ['--dt-factor', '0.5']


def gm(p, s, rho='0.3', bo='0.5', wall=None):
    w = ['--gm-gamma-wall', wall] if wall else ['--gm-wall-ncm', rho]
    return ['--gm-gamma', f'AM_P={p},AM_S={s}'] + w + ['--gm-bo-se', bo]


DECKS = {
    'GMuu_soft_lab': gm('0.3', '0.3') + LAB,
    'GMuu_ref20_lab': gm('0.3', '0.3') + LAB + R20,
    'GMcc_ref20_lab': gm('1', '1') + LAB + R20,
    'GMcu_ref20_lab': gm('1', '0.3') + LAB + R20,
    'GMuc_ref20_lab': gm('0.3', '1') + LAB + R20,
    'GMcc_exp_ref20_lab': gm('1', '1', wall='0.00768') + LAB + R20,
    'GMuu_ref20_gen1': gm('0.3', '0.3') + G1 + R20,
    'GMcc_ref20_gen1': gm('1', '1') + G1 + R20,
    'GMuu_ref20_lab_bo04': gm('0.3', '0.3', bo='0.4') + LAB + R20,
    'GMcc_ref20_lab_rho05': gm('1', '1', rho='0.5') + LAB + R20,
    'GMuu_ref20_lab_dthalf': gm('0.3', '0.3') + LAB + R20 + DTH,
    'GMuu_ref40_lab': gm('0.3', '0.3') + LAB + R40,
    'GMuu_ref20_lab_bo5': gm('0.3', '0.3', bo='5') + LAB + R20,
    'GMuu_ref20_lab_rho1p00001': gm('1.00001', '1.00001', rho='1.00001') + LAB + R20,
    'GMcc_ref20_lab_rho1p00001': gm('1', '1', rho='1.00001') + LAB + R20,
    'GMuu_ref20_lab_rho1p0001': gm('1.0001', '1.0001', rho='1.0001') + LAB + R20,
    'GMcc_ref20_lab_rho1p0001': gm('1', '1', rho='1.0001') + LAB + R20,
    'GMuu_ref20_lab_odd': gm('0.123456789', '0.123456789', rho='0.123456789', bo='0.987654321') + LAB + R20,
    'GMcc_ref20_lab_odd': gm('1', '1', rho='0.123456789', bo='0.987654321') + LAB + R20,
    'LC_soft_lab': ['--arm', 'LC'] + LAB,
    'LC_ref20_lab': ['--arm', 'LC'] + LAB + R20,
    'LH_ref20_lab': ['--arm', 'LH'] + LAB + R20,
    'LC_soft_gen1': ['--arm', 'LC'],
    'LC_ref20_gen1': ['--arm', 'LC'] + R20,
}
P = lambda n: os.path.join(OUT, n, 'in.mixer')        # noqa: E731


def load_js():
    return json.load(open(JS, encoding='utf-8')) if os.path.exists(JS) else {}


def save(key, val):
    J = load_js()
    J[key] = val
    json.dump(J, open(JS, 'w'), ensure_ascii=False, indent=1)


def run(argv):
    p = subprocess.run([sys.executable, '-I', '-B'] + argv, capture_output=True, text=True, env=ENV)
    return p.returncode, (p.stdout + p.stderr)


def rb(kind, a, b, tag=None, pa=None, pb=None):
    js = os.path.join(OUT, f'rb_{tag or (kind + "_" + a + "__" + b)}.json')
    rc, txt = run([RB, '--table', kind, pa or P(a), pb or P(b), '--json', js])
    fails = []
    try:
        J = json.load(open(js, encoding='utf-8'))
        for T in J.get('tables', []):
            fails += T.get('failures', [])
    except Exception as e:                                  # noqa: BLE001
        fails = [f'(no json: {e}) {txt.strip().splitlines()[-1:] if txt.strip() else ""}']
    return dict(kind=kind, old=a, new=b, rc=rc, n_fail=len(fails), fails=[f[:230] for f in fails[:6]])


def df(allow, a, b, extra=(), pa=None, pb=None):
    rc, txt = run([DF, pa or P(a), pb or P(b), '--allow', allow] + list(extra))
    lines = [l for l in txt.strip().splitlines() if '⛔' in l or 'PASS' in l or 'FAIL' in l][:6]
    return dict(allow=allow, old=a, new=b, extra=list(extra), rc=rc, lines=[l[:230] for l in lines])


if STAGE == 'decks':
    res = {}
    for name, args in DECKS.items():
        d = os.path.join(OUT, name)
        if os.path.isdir(d):
            shutil.rmtree(d)
        rc, txt = run([GEN, '--out', d] + BASE + args)
        res[name] = dict(rc=rc, tail=txt.strip().splitlines()[-1:] if rc else [])
        print(name, rc, res[name]['tail'])
    save('decks', res)

elif STAGE == 'rb':
    Q = [('E', 'GMuu_soft_lab', 'GMuu_ref20_lab'), ('E', 'LC_soft_lab', 'LC_ref20_lab'), ('E', 'LC_soft_gen1', 'LC_ref20_gen1'),
         ('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMcu_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMuc_ref20_lab'),
         ('GM', 'GMcu_ref20_lab', 'GMcc_ref20_lab'), ('GM', 'GMcc_ref20_lab', 'GMuu_ref20_lab'), ('GM', 'GMuu_ref20_gen1', 'GMcc_ref20_gen1'),
         ('GM', 'GMuu_ref20_lab', 'GMcc_exp_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab_rho05'),
         ('GM', 'GMuu_ref20_lab', 'GMuu_ref20_lab_bo04'), ('GM', 'GMuu_ref20_lab', 'GMcc_ref20_gen1'), ('GM', 'GMuu_ref20_lab', 'GMuu_ref20_lab'),
         ('GM', 'GMuu_soft_lab', 'GMcc_ref20_lab'),
         ('GM', 'GMuu_ref20_lab_rho1p00001', 'GMcc_ref20_lab_rho1p00001'), ('GM', 'GMuu_ref20_lab_rho1p0001', 'GMcc_ref20_lab_rho1p0001'),
         ('GM', 'GMuu_ref20_lab_odd', 'GMcc_ref20_lab_odd'),
         ('DT', 'GMuu_ref20_lab', 'GMuu_ref20_lab_dthalf'), ('E', 'GMuu_ref20_lab', 'GMuu_ref40_lab'), ('E', 'GMuu_soft_lab', 'GMcc_ref20_lab'),
         ('E', 'LC_soft_lab', 'GMuu_ref20_lab'), ('B', 'LC_ref20_lab', 'LH_ref20_lab'), ('U', 'GMuu_ref20_lab', 'GMuu_ref20_lab_bo5'),
         ('B', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('U', 'GMuu_ref20_lab', 'GMcc_ref20_lab')]
    res = [rb(*q) for q in Q]
    for r_ in res:
        print('rb', r_['kind'], r_['old'], '->', r_['new'], 'rc', r_['rc'], 'nfail', r_['n_fail'], '|', (r_['fails'] or ['PASS'])[0][:170])
    save('rb', res)

elif STAGE == 'df':
    Q = [('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMcu_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMuc_ref20_lab'),
         ('GM', 'GMcc_ref20_lab', 'GMuu_ref20_lab'), ('GM', 'GMuu_ref20_gen1', 'GMcc_ref20_gen1'),
         ('A', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('B', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('U', 'GMuu_ref20_lab', 'GMcc_ref20_lab'),
         ('E', 'GMuu_ref20_lab', 'GMcc_ref20_lab'), ('EB', 'GMuu_ref20_lab', 'GMcc_ref20_lab'),
         ('E', 'GMuu_soft_lab', 'GMuu_ref20_lab'), ('E', 'LC_soft_lab', 'LC_ref20_lab'), ('E', 'LC_soft_lab', 'GMuu_ref20_lab'),
         ('GM', 'GMuu_ref20_lab', 'GMcc_exp_ref20_lab'), ('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab_rho05'),
         ('GM', 'GMuu_ref20_lab', 'GMuu_ref20_lab_bo04'), ('GM', 'LC_ref20_lab', 'LH_ref20_lab'), ('B', 'LC_ref20_lab', 'LH_ref20_lab'),
         ('GM', 'GMuu_ref20_lab_rho1p00001', 'GMcc_ref20_lab_rho1p00001'), ('GM', 'GMuu_ref20_lab_rho1p0001', 'GMcc_ref20_lab_rho1p0001'),
         ('GM', 'GMuu_ref20_lab_odd', 'GMcc_ref20_lab_odd'), ('U', 'GMuu_ref20_lab', 'GMuu_ref20_lab_bo5'),
         ('E', 'GMuu_ref20_lab', 'GMuu_ref40_lab')]
    res = [df(*q) for q in Q]
    res.append(df('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab', ['--expect-deck', P('GMcc_ref20_lab')]))
    res.append(df('GM', 'GMuu_ref20_lab', 'GMcc_ref20_lab', ['--expect-deck', P('GMcu_ref20_lab')]))
    for r_ in res:
        print('df', r_['allow'], r_['old'], '->', r_['new'], r_['extra'][1:] and os.path.basename(os.path.dirname(r_['extra'][1])), 'rc',
              r_['rc'], '|', ' / '.join(r_['lines'])[:240])
    save('df', res)

elif STAGE == 'mut':
    SRC = open(GEN, encoding='utf-8').read()
    MUTS = {
        'M04': ("nu_se, (DENS if dens is None else dens)[mat_se], E=E['SE'])", "nu_se, DENS[mat_se], E=E['SE'])"),
        'M05': ("M_soft = ced_matrix(arm, p['d'], dens=_dens_of(p))", "M_soft = ced_matrix(arm, p['d'])"),
        'M16': ("gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],", "gamma_wall=a_['gamma_wall'], bo_se=BO_BASE,"),
        'M06': ('            ov = pair_overlap(M[i][j], ti, tj, d, E)',
                '            if ti != tj and tj != WALL:\n                continue\n            ov = pair_overlap(M[i][j], ti, tj, d, E)'),
        'N15': ("""+ f"{a['rho_uncoated_ncm']:g} = {a['gamma_wall']:g} — 같은 ρ 세계의 코팅 팔도 같은 벽")""",
                """+ f"{1.0:g} = {a['gamma_wall']:g} — 같은 ρ 세계의 코팅 팔도 같은 벽")"""),
        'M15': ('{f / fss:>11.6g}', '{f:>11.6g}'),
        'M18': ('def gm_arm(gamma, gamma_wall=None, bo_se=None, layered=True,', 'def gm_arm(gamma, gamma_wall=None, bo_se=None, layered=False,'),
        'M13': ('        if gw != gm_wall_from_ncm(rho):', '        if False:'),
    }
    mroot = os.path.join(HERE, 'mutx')
    res = {}
    for nm, (o, n) in MUTS.items():
        assert SRC.count(o) == 1, nm
        d = os.path.join(mroot, nm)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'make_mixer_deck.py'), 'w', encoding='utf-8').write(SRC.replace(o, n))
        for f in ('additives.py', 'make_mixer_baffles.py'):
            shutil.copy(os.path.join(W, 'scripts', f), os.path.join(d, f))
        g = os.path.join(d, 'make_mixer_deck.py')
        args_s = gm('0.3', '0.3') + LAB
        if nm == 'M06':
            args_s = gm('10', '10', rho='10', bo='800') + LAB
        if nm == 'M13':
            args_s = ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB   # (CLI always passes gm_wall_from_ncm(ρ))
        rec = {}
        for tag, extra in (('soft', []), ('ref20', R20)):
            dd = os.path.join(mroot, nm + '_decks', tag)
            if os.path.isdir(dd):
                shutil.rmtree(dd)
            rc, txt = run([g, '--out', dd] + BASE + args_s + extra)
            rec[tag + '_rc'] = rc
            rec[tag + '_tail'] = txt.strip().splitlines()[-1:] if rc else []
        if rec['soft_rc'] == 0 and rec['ref20_rc'] == 0:
            a_, b_ = os.path.join(mroot, nm + '_decks', 'soft', 'in.mixer'), os.path.join(mroot, nm + '_decks', 'ref20', 'in.mixer')
            rec['rb_E'] = rb('E', nm + '_soft', nm + '_ref20', tag='mut_' + nm, pa=a_, pb=b_)
            rec['df_E'] = df('E', nm + '_soft', nm + '_ref20', pa=a_, pb=b_)
            if nm in ('M04', 'M05', 'M16', 'N15', 'M15', 'M18'):
                # also the same-world uncoated → coated (fixed generator cc ref20) — GM table / --allow GM
                rec['rb_GM_vs_fixed_cc'] = rb('GM', nm + '_ref20', 'GMcc_ref20_lab', tag='mutGM_' + nm, pa=b_, pb=P('GMcc_ref20_lab'))
                rec['df_GM_vs_fixed_cc'] = df('GM', nm + '_ref20', 'GMcc_ref20_lab', pa=b_, pb=P('GMcc_ref20_lab'))
        res[nm] = rec
        print(nm, {k: (v if not isinstance(v, dict) else (v.get('rc'), (v.get('fails') or v.get('lines') or ['PASS'])[0][:150])) for k, v in rec.items()})
    save('mut', res)

elif STAGE == 'runs':
    spec = importlib.util.spec_from_file_location('mdd', DF)
    sys.path.insert(0, os.path.join(W, 'scripts'))
    mdd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mdd)
    R = os.path.join(OUT, 'runs')
    if os.path.isdir(R):
        shutil.rmtree(R)
    names = {'uu': 'GMuu_rho0p3_bo0p5_lab20261014_ref_r2_s32452843', 'cc': 'GMcc_rho0p3_bo0p5_lab20261014_ref_r2_s32452843',
             'uu_nometa': 'GMuu_rho0p3_bo0p5_lab20261014_soft_r2_s32452843'}
    res = {}
    for k, nm in names.items():
        a = mdd.d2_cli_args(nm)
        rc, txt = run([GEN, '--out', os.path.join(R, nm)] + a)
        res['gen_' + k] = dict(rc=rc, args=a)
    os.remove(os.path.join(R, names['uu_nometa'], 'deck_meta.json'))
    res['cell_problems_uu'] = mdd.cell_deck_problems(os.path.join(R, names['uu']), names['uu'])[0]
    res['cell_problems_nometa'] = mdd.cell_deck_problems(os.path.join(R, names['uu_nometa']), names['uu_nometa'])[0]
    tag = lambda n: n[:n.rindex('_s')]                       # noqa: E731
    rc, txt = run([DF, '--runs', R, '--ref-arm', tag(names['uu']), '--arm', tag(names['cc']), '--allow', 'GM', '--expect-seeds', '32452843'])
    res['runs_GM'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-4:]])
    # meta deck_file tamper + bo tamper (M16-like) on a copy
    mp = os.path.join(R, names['cc'], 'deck_meta.json')
    mj = json.load(open(mp, encoding='utf-8'))
    json.dump(dict(mj, deck_file='other.mixer'), open(mp, 'w'), ensure_ascii=False)
    res['cell_problems_cc_deckfile_tamper'] = mdd.cell_deck_problems(os.path.join(R, names['cc']), names['cc'])[0]
    rc, txt = run([RB, '--table', 'GM', os.path.join(R, names['uu'], 'in.mixer'), os.path.join(R, names['cc'], 'in.mixer')])
    res['rb_GM_cc_deckfile_tamper'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-3:]])
    json.dump(dict(mj, deck_file='other.mixer', adhesion_rule=dict(mj['adhesion_rule'], bo_se=0.21244)), open(mp, 'w'), ensure_ascii=False)
    rc, txt = run([RB, '--table', 'GM', os.path.join(R, names['uu'], 'in.mixer'), os.path.join(R, names['cc'], 'in.mixer')])
    res['rb_GM_cc_deckfile_and_bo_tamper'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-3:]])
    res['cell_problems_cc_deckfile_and_bo_tamper'] = mdd.cell_deck_problems(os.path.join(R, names['cc']), names['cc'])[0]
    json.dump(dict(mj, adhesion_rule=dict(mj['adhesion_rule'], bo_se=0.21244)), open(mp, 'w'), ensure_ascii=False)
    rc, txt = run([RB, '--table', 'GM', os.path.join(R, names['uu'], 'in.mixer'), os.path.join(R, names['cc'], 'in.mixer')])
    res['rb_GM_cc_bo_tamper'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-3:]])
    rc, txt = run([DF, os.path.join(R, names['uu'], 'in.mixer'), os.path.join(R, names['cc'], 'in.mixer'), '--allow', 'GM'])
    res['df2deck_GM_cc_bo_tamper'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-3:]])
    os.remove(mp)
    rc, txt = run([RB, '--table', 'GM', os.path.join(R, names['uu'], 'in.mixer'), os.path.join(R, names['cc'], 'in.mixer')])
    res['rb_GM_cc_meta_removed'] = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-3:]])
    for k, v in res.items():
        print(k, json.dumps(v, ensure_ascii=False)[:300])
    save('runs', res)

elif STAGE == 'edge':
    res = {}
    E = os.path.join(OUT, 'edge')
    cases = {
        'stiffen_2_0': ['--arm', 'LC', '--stiffen-se', '2_0', '--hold-bo-pairwise'],
        'stiffen_fullwidth20': ['--arm', 'LC', '--stiffen-se', '２０', '--hold-bo-pairwise'],
        'stiffen_nan': ['--arm', 'LC', '--stiffen-se', 'nan', '--hold-bo-pairwise'],
        'stiffen_inf': ['--arm', 'LC', '--stiffen-se', 'inf', '--hold-bo-pairwise'],
        'dt_0_5': ['--arm', 'LC', '--dt-factor', '0_5'],
        'dt_nan': ['--arm', 'LC', '--dt-factor', 'nan'],
        'cgf_15_1.4': ['--arm', 'LC', '--cgf', '15_1.4'],
        'gm_stiffen_2_0': gm('0.3', '0.3') + LAB + ['--stiffen-se', '2_0', '--hold-bo-pairwise'],
        'gm_stiffen_nan': gm('0.3', '0.3') + LAB + ['--stiffen-se', 'nan', '--hold-bo-pairwise'],
        'gm_dt_fullwidth': gm('0.3', '0.3') + LAB + ['--dt-factor', '０.５'],
        'gm_nbsp_value': ['--gm-gamma', 'AM_P= 0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_emsp_value': ['--gm-gamma', 'AM_P=0.3 ,AM_S=0.3', '--gm-wall-ncm', ' 0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_se_explicit_1e0': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3,SE=1e0', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_se_1p0000001': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3,SE=1.0000001', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_rho_4e-5': gm('4e-5', '4e-5', rho='4e-5') + LAB,
        'gm_rho_3e-5': gm('3e-5', '3e-5', rho='3e-5') + LAB,
        'gm_rho_1e-6_coated': gm('1', '1', rho='1e-6') + LAB,
        'gm_bo_1e-6': gm('1', '1', rho='1', bo='1e-6') + LAB,
        'gm_bo_1.00001e4': gm('1', '1', rho='1', bo='1.00001e4') + LAB,
        'gm_gamma_1e6_bo_small': gm('1e6', '1e6', rho='1e6', bo='1e-6') + LAB,
        'gm_gamma_1.000001e6': gm('1.000001e6', '1.000001e6', rho='1.000001e6', bo='1e-6') + LAB,
        'gm_bo_dot5': gm('0.3', '0.3', bo='.5') + LAB,
        'gm_bo_5dot': gm('0.3', '0.3', bo='5.') + LAB,
        'gm_rho_upperE': gm('3E-1', '3E-1', rho='3E-1') + LAB,
        'gm_rho_plus_sign': gm('0.3', '0.3', rho='+0.3') + LAB,
        'gm_key_lower': ['--gm-gamma', 'am_p=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_key_dup': ['--gm-gamma', 'AM_P=0.3,AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
        'gm_trailing_comma': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3,', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5'] + LAB,
    }
    for k, a in cases.items():
        d = os.path.join(E, k)
        if os.path.isdir(d):
            shutil.rmtree(d)
        rc, txt = run([GEN, '--out', d] + BASE + a)
        info = dict(rc=rc, tail=[l[:200] for l in txt.strip().splitlines()[-1:]])
        mp = os.path.join(d, 'deck_meta.json')
        if rc == 0 and os.path.exists(mp):
            m_ = json.load(open(mp, encoding='utf-8'))
            info.update(stiffen=m_.get('stiffen_se'), dt_factor=m_.get('dt_factor'), cgf=m_.get('cgf'),
                        gamma=(m_.get('adhesion_rule') or {}).get('gamma'), rho=(m_.get('adhesion_rule') or {}).get('rho_uncoated_ncm'),
                        bo=(m_.get('adhesion_rule') or {}).get('bo_se'))
        elif rc == 0:
            info['note'] = 'no deck_meta (default/old-arm deck)'
        res[k] = info
        print(k, json.dumps(info, ensure_ascii=False)[:260])
    # name grammar vs generator range (diff tool)
    spec = importlib.util.spec_from_file_location('mdd', DF)
    sys.path.insert(0, os.path.join(W, 'scripts'))
    mdd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mdd)
    gram = {}
    for nm in ('GMuu_rho0p00001_bo0p5_lab20261014_ref_r2_s32452843', 'GMuu_rho0p00004_bo0p5_lab20261014_ref_r2_s32452843',
               'GMcc_rho1000000_bo0p000001_lab20261014_ref_r2_s32452843', 'GMuu_rho0p3_bo10000_lab20261014_ref_r2_s32452843',
               'GMuu_rho1p00001_bo0p5_lab20261014_ref_r2_s32452843', 'GMuu_rho0p3_bo0p5_gen1_ref2_dthalf_r8_s15485863'):
        try:
            c_ = mdd.parse_cell(nm)
            parse = 'ok'
        except ValueError as e:
            parse = f'ValueError {e}'[:160]
            c_ = None
        try:
            t_ = mdd.cell_expected_deck(nm) if c_ else None
            exp = 'ok' if t_ else None
        except SystemExit as e:
            exp = f'SystemExit {str(e)[:150]}'
        except Exception as e:                              # noqa: BLE001
            exp = f'{type(e).__name__} {str(e)[:150]}'
        gram[nm] = dict(parse=parse, expected_deck=exp)
        print(nm, gram[nm])
    res['grammar'] = gram
    save('edge', res)
