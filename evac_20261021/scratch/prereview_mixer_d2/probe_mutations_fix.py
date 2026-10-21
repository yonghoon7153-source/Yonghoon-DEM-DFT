#!/usr/bin/env python3
"""recheck 10-21 — mutation tests on the FIXED generator (gen/mmd_FIX.py = 9412f384a scripts/make_mixer_deck.py).

The first review's 24 mutations (anchors adapted where the fix moved/rewrote the line: M10 M11 M12 M13 M24) + new mutations on the
fix's own guards (N01–N26).  Each mutation = one exact-substring replacement (must occur exactly once) in a copy placed in
mutfix/<name>/make_mixer_deck.py next to copies of additives.py and make_mixer_baffles.py; `python3 -I -B … --selftest`;
KILLED = rc != 0 or >= 1 FAIL line.  Also records WHICH checks failed (to judge "fails for the right reason").
Control = unmutated copy (must PASS).
usage: python3 -I -B probe_mutations_fix.py <repo_worktree>   (writes probe_mutations_fix.json)
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
SRC = open(os.path.join(HERE, 'gen', 'mmd_FIX.py'), encoding='utf-8').read()
MUT = [
    # ── the first review's 24 (same intent; anchors adapted for the fixed code where needed) ──
    ('M01_arith_mean', 'f = f_ss * math.sqrt(g[ti] * g[tj]) * rs / rss', 'f = f_ss * (0.5 * (g[ti] + g[tj])) * rs / rss'),
    ('M02_drop_Rstar', 'f = f_ss * math.sqrt(g[ti] * g[tj]) * rs / rss', 'f = f_ss * math.sqrt(g[ti] * g[tj])'),
    ('M03_wall_Rstar_half', '    if tj == WALL:\n        return ri\n', '    if tj == WALL:\n        return ri / 2.0\n'),
    ('M04_F0SS_gen1_density', "nu_se, (DENS if dens is None else dens)[mat_se], E=E['SE'])", "nu_se, DENS[mat_se], E=E['SE'])"),
    ('M05_deck_ignores_dens', "M_soft = ced_matrix(arm, p['d'], dens=_dens_of(p))", "M_soft = ced_matrix(arm, p['d'])"),
    ('M06_ceiling_skip_mixed', '            ov = pair_overlap(M[i][j], ti, tj, d, E)',
     '            if ti != tj and tj != WALL:\n                continue\n            ov = pair_overlap(M[i][j], ti, tj, d, E)'),
    ('M07_stiff_D2_old_ceiling', "    if ARMS[arm].get('rule') == 'geomean':          # D2 팔 = 모든 쌍 천장 (옛 팔은 대각 · 벽 검사 그대로)",
     "    if False:"),
    ('M08_wall_gamma_ignored', "    g[WALL] = a['gamma_wall']\n", "    g[WALL] = 1.0\n"),
    ('M09_no_ceiling_soft', "    _assert_ceiling_pairwise(a.get('desc', 'D2'), M, d, E)\n", "    pass\n"),
    ('M10_wallncm_ignores_rho', "    return GM_WALL_HARE2026 * _gm_num(rho_uncoated, 'ρ_비코팅 NCM = γ_NCM/γ_SE', GM_GAMMA_RANGE)",
     "    _gm_num(rho_uncoated, 'x', GM_GAMMA_RANGE)\n    return GM_WALL_HARE2026"),
    ('M11_gmnum_allow_zero_neg', "    if not (lo <= v <= hi):\n        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 지원 범위",
     "    if not (v <= hi):\n        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 지원 범위"),
    ('M12_gmnum_finite_check_off', "    if not math.isfinite(v):\n        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 유한하지 않다",
     "    if False:\n        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 유한하지 않다"),
    ('M13_rho_check_removed', '        if gw != gm_wall_from_ncm(rho):', '        if False:'),
    ('M14_cli_both_wall_allowed', '        if a.gm_gamma_wall is not None and a.gm_wall_ncm is not None:', '        if False:'),
    ('M15_header_F0_not_ratio', '{f / fss:>11.6g}', '{f:>11.6g}'),
    ('M16_meta_bo_const', "gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],", "gamma_wall=a_['gamma_wall'], bo_se=BO_BASE,"),
    ('M17_meta_gamma_wall_const', "gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],", "gamma_wall=GM_WALL_HARE2026, bo_se=a_['bo_se'],"),
    ('M18_gm_uniform_insertion', 'def gm_arm(gamma, gamma_wall=None, bo_se=None, layered=True,',
     'def gm_arm(gamma, gamma_wall=None, bo_se=None, layered=False,'),
    ('M19_overlap_max_radius', '    rmin = min(d[t] / 2.0 for t in (ti, tj) if t != WALL)', '    rmin = max(d[t] / 2.0 for t in (ti, tj) if t != WALL)'),
    ('M20_require_dens_off', "    if ARMS[arm].get('rule') == 'geomean' and p.get('dens_gen') is None:", '    if False:'),
    ('M21_ced_exponent', '(f * es ** 2 / (4.5 * math.pi ** 3 * rs ** 2)) ** (1.0 / 3.0)', '(f * es ** 2 / (4.5 * math.pi ** 3 * rs ** 2)) ** 0.34'),
    ('M22_F0SS_radius_diam', "ced_ss = ced_for_bond(a['bo_se'], d['SE'] / 2.0,", "ced_ss = ced_for_bond(a['bo_se'], d['SE'],"),
    ('M23_gm_lab_header_off', "    _dens_hdr = _dens_header(p)                        # 밀도 세대를 명시한 덱만 (미지정 = '' → 바이트 그대로)",
     "    _dens_hdr = ''"),
    ('M24_meta_wall_rule_dropped', "        meta['adhesion_rule'].update(wall_rule=a_['wall_rule'], surface=",
     "        meta['adhesion_rule'].update(surface="),
    # ── new: the fix's own guards ──
    ('N01_q2_ncm_off_removed', '        off = {t: g[t] for t in ncm if g[t] not in (1.0, rho)}', '        off = {}'),
    ('N02_explicit_coated_only_removed', '        off = {t: g[t] for t in ncm if g[t] != 1.0}', '        off = {}'),
    ('N03_rho_world_unscaled', 'wall_rule, rho_world = GM_WALL_RULE_EXPLICIT, gw / GM_WALL_HARE2026',
     'wall_rule, rho_world = GM_WALL_RULE_EXPLICIT, gw'),
    ('N04_surface_inverted', "surface={t: ('coated' if g[t] == 1.0 else 'uncoated') for t in ncm})",
     "surface={t: ('uncoated' if g[t] == 1.0 else 'coated') for t in ncm})"),
    ('N05_arm_name_match', '    if not isinstance(name, str) or not _ARM_NAME_RE.fullmatch(name):',
     '    if not isinstance(name, str) or not _ARM_NAME_RE.match(name):'),
    ('N06_desc_control_chars_ok', "    bad = sorted({c for c in s if unicodedata.category(c)[0] == 'C'})", '    bad = []'),
    ('N07_ascii_regex_bypass', '    if t is None or not _ASCII_DEC_RE.fullmatch(t):', '    if t is None:'),
    ('N08_ced_postcond_off', '            if not (math.isfinite(M[i][j]) and M[i][j] >= sys.float_info.min):', '            if False:'),
    ('N09_fss_postcond_off', '    if not (math.isfinite(f_ss) and f_ss >= sys.float_info.min):', '    if False:'),
    ('N10_gamma_range_wide', 'GM_GAMMA_RANGE = (1e-6, 1e6)', 'GM_GAMMA_RANGE = (1e-300, 1e300)'),
    ('N11_bo_range_wide', 'GM_BO_RANGE = (1e-6, 1e4)', 'GM_BO_RANGE = (1e-320, 1e300)'),
    ('N12_schema_v1', "        meta['schema'] = MIXER_DECK_META_SCHEMA_V2", "        meta['schema'] = 'mixer_deck_meta/1'"),
    ('N13_registered_old_text', "        meta['registered'] = (MIXER_D2_REGISTERED",
     "        meta['registered'] = ('docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 (강성 축)'"),
    ('N14_meta_rho_const', "            meta['adhesion_rule']['rho_uncoated_ncm'] = a_['rho_uncoated_ncm']",
     "            meta['adhesion_rule']['rho_uncoated_ncm'] = 1.0"),
    ('N15_header_rho_const', """+ f"{a['rho_uncoated_ncm']:g} = {a['gamma_wall']:g} — 같은 ρ 세계의 코팅 팔도 같은 벽")""",
     """+ f"{1.0:g} = {a['gamma_wall']:g} — 같은 ρ 세계의 코팅 팔도 같은 벽")"""),
    ('N16_header_surface_inverted', """f"{t} {'코팅' if surf[t] == 'coated' else '비코팅'}" for t in surf)""",
     """f"{t} {'비코팅' if surf[t] == 'coated' else '코팅'}" for t in surf)"""),
    ('N17_cli_rho_not_passed', "register_arm('GM', gm_arm(_g, gamma_wall=gm_wall_from_ncm(a.gm_wall_ncm), bo_se=a.gm_bo_se, rho_uncoated_ncm=a.gm_wall_ncm))",
     "register_arm('GM', gm_arm(_g, gamma_wall=gm_wall_from_ncm(a.gm_wall_ncm), bo_se=a.gm_bo_se))"),
    ('N18_cli_gamma_float', "            _g[_k] = ascii_decimal(_v, f'--gm-gamma {_k}')", "            _g[_k] = float(_v)"),
    ('N19_cli_bo_float', "ap.add_argument('--gm-bo-se', type=_ascii_float_arg", "ap.add_argument('--gm-bo-se', type=float"),
    ('N20_cli_wallncm_float', "ap.add_argument('--gm-wall-ncm', type=_ascii_float_arg", "ap.add_argument('--gm-wall-ncm', type=float"),
    ('N21_cli_gammawall_float', "ap.add_argument('--gm-gamma-wall', type=_ascii_float_arg", "ap.add_argument('--gm-gamma-wall', type=float"),
    ('N22_ceiling_loosened', '            if not math.isfinite(ov) or ov > OVL_CEILING * (1 + 1e-9):',
     '            if not math.isfinite(ov) or ov > OVL_CEILING * 1.5:'),
    ('N23_wall_comment_old_for_d2', "                 if _a_now.get('rule') == 'geomean' else", "                 if False else"),
    ('N24_registered_no_stiff_text', "if (float(p.get('stiffen_se', 1.0)) != 1.0 or float(dt_factor) != 1.0) else ''))",
     "if False else ''))"),
    ('N25_header_layered_from_arm', "    lay = bool(a.get('layered')) if layered is None else bool(layered)", "    lay = bool(a.get('layered'))"),
    ('N26_meta_layered_true', "layered=bool(a_.get('layered')))", "layered=True)"),
]
res = []
mroot = os.path.join(HERE, 'mutfix')
os.makedirs(mroot, exist_ok=True)


def run_one(name, text):
    d = os.path.join(mroot, name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'make_mixer_deck.py'), 'w', encoding='utf-8').write(text)
    for f in ('additives.py', 'make_mixer_baffles.py'):
        shutil.copy(os.path.join(REPO, 'scripts', f), os.path.join(d, f))
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, 'make_mixer_deck.py'), '--selftest'],
                       capture_output=True, text=True, env=dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1'),
                       timeout=900)
    fails = [l.strip()[6:].strip()[:110] for l in p.stdout.splitlines() if l.startswith('  FAIL')]
    tail = [l for l in p.stdout.splitlines() if 'selftest:' in l]
    return dict(rc=p.returncode, n_fail=len(fails), fails=fails,
                summary=tail[-1] if tail else (p.stderr.strip().splitlines() or [''])[-1][:200])


ctl = run_one('CONTROL', SRC)
ctl['mutation'] = 'CONTROL'
ctl['status'] = 'CLEAN' if (ctl['rc'] == 0 and not ctl['n_fail']) else 'DIRTY'
res.append(ctl)
print(f"CONTROL rc={ctl['rc']} nfail={ctl['n_fail']} {ctl['summary'][:70]}")
for name, old, new in MUT:
    n = SRC.count(old)
    rec = dict(mutation=name, occurrences=n)
    if n != 1:
        rec['status'] = 'NOT_APPLIED'
        res.append(rec)
        print(f'{name}: NOT APPLIED (occurrences {n})')
        continue
    rec.update(run_one(name, SRC.replace(old, new)))
    rec['status'] = 'KILLED' if (rec['rc'] != 0 or rec['n_fail']) else 'SURVIVED'
    res.append(rec)
    print(f"{name:34s} {rec['status']:9s} rc={rec['rc']} nfail={rec['n_fail']} {rec['summary'][:50]} | "
          f"{'; '.join(x[:44] for x in rec['fails'][:3])}")
json.dump(res, open(os.path.join(HERE, 'probe_mutations_fix.json'), 'w'), ensure_ascii=False, indent=1)
summ = {}
for r in res:
    summ[r['status']] = summ.get(r['status'], 0) + 1
print('SUMMARY', summ)
