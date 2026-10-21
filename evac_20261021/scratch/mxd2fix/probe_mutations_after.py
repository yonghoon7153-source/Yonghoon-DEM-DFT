#!/usr/bin/env python3
"""Mutation probe on the FIXED generator (scratch) — the review's 24 mutations (M10 · M11 · M12 · M13 · M24 re-anchored to the
new code with the same intent) + 8 extra mutations on the new guards (M25–M32).  Each = one exact-substring replacement (must occur
exactly once) in a copy of scripts/make_mixer_deck.py placed in mut_after/<name>/ next to additives.py · make_mixer_baffles.py.
A control copy (no mutation) runs first; KILLED = selftest has >= 1 FAIL that the control does not have (or rc != 0 with a clean control).
usage: python3 -I -B probe_mutations_after.py <repo_worktree> <out_json>"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO, OUTJ = sys.argv[1], sys.argv[2]
SRC = open(os.path.join(REPO, 'scripts', 'make_mixer_deck.py'), encoding='utf-8').read()
MUT = [
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
    #  re-anchored (same intent as the review's mutation · the guarded line was rewritten in this fix)
    ('M10_wallncm_ignores_rho', "    return GM_WALL_HARE2026 * _gm_num(rho_uncoated, 'ρ_비코팅 NCM = γ_NCM/γ_SE', GM_GAMMA_RANGE)",
     "    _gm_num(rho_uncoated, 'x', GM_GAMMA_RANGE)\n    return GM_WALL_HARE2026"),
    ('M11_gmnum_allow_zero', '    if not (lo <= v <= hi):', '    if not (0.0 <= v <= hi):'),
    ('M12_gmnum_allow_nan_inf', "    if not math.isfinite(v):\n        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 유한하지 않다 (NaN · ∞)')\n"
                                "    lo, hi = rng\n    if not (lo <= v <= hi):",
     '    lo, hi = rng\n    if v < lo or v > hi:'),
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
    ('M24_meta_wall_rule_dropped',
     "        meta['adhesion_rule'].update(wall_rule=a_['wall_rule'], surface=dict(a_['surface']), layered=bool(a_.get('layered')))",
     '        pass'),
    #  extra — the guards this fix added (do the new tests fail for the right reason?)
    ('M25_q2_ncm_membership_off', '        off = {t: g[t] for t in ncm if g[t] not in (1.0, rho)}', '        off = {}'),
    ('M26_explicit_coated_only_off', '        off = {t: g[t] for t in ncm if g[t] != 1.0}', '        off = {}'),
    ('M27_arm_name_match_not_fullmatch', 'not _ARM_NAME_RE.fullmatch(name)', "not re.match(r'^[A-Za-z][A-Za-z0-9_]{0,31}$', name)"),
    ('M28_desc_control_chars_allowed', "    bad = sorted({c for c in s if unicodedata.category(c)[0] == 'C'})", '    bad = []'),
    ('M29_ascii_decimal_is_float', '    if t is None or not _ASCII_DEC_RE.fullmatch(t):', '    if t is None:'),
    ('M30_meta_schema_stays_v1', '        meta[\'schema\'] = MIXER_DECK_META_SCHEMA_V2', '        pass'),
    ('M31_registered_old_text', "        meta['registered'] = (MIXER_D2_REGISTERED", "        meta['registered'] = (meta['registered']"),
    ('M32_ced_post_assert_off', '            if not (math.isfinite(M[i][j]) and M[i][j] >= sys.float_info.min):', '            if False:'),
]


def run(d):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, 'make_mixer_deck.py'), '--selftest'],
                       capture_output=True, text=True, timeout=900)
    fails = [l.strip()[6:].strip()[:110] for l in p.stdout.splitlines() if l.startswith('  FAIL')]
    tail = [l for l in p.stdout.splitlines() if 'selftest:' in l]
    return p.returncode, fails, (tail[-1] if tail else (p.stderr.strip().splitlines() or [''])[-1])


root = os.path.join(HERE, 'mut_after')
shutil.rmtree(root, ignore_errors=True)
os.makedirs(root)


def place(name, text):
    d = os.path.join(root, name)
    os.makedirs(d)
    open(os.path.join(d, 'make_mixer_deck.py'), 'w', encoding='utf-8').write(text)
    for f in ('additives.py', 'make_mixer_baffles.py'):
        shutil.copy(os.path.join(REPO, 'scripts', f), os.path.join(d, f))
    return d


rc0, f0, s0 = run(place('CONTROL', SRC))
print(f'CONTROL rc={rc0} {s0} control_fails={f0}')
base = set(f0)
res = [dict(mutation='CONTROL', rc=rc0, n_fail=len(f0), fails=f0, summary=s0)]
for name, old, new in MUT:
    n = SRC.count(old)
    rec = dict(mutation=name, occurrences=n)
    if n != 1:
        rec['status'] = 'NOT_APPLIED'
        res.append(rec)
        print(f'{name}: NOT APPLIED (occurrences {n})')
        continue
    rc, fails, summ = run(place(name, SRC.replace(old, new)))
    extra = [x for x in fails if x not in base]
    rec.update(rc=rc, n_fail=len(fails), fails=fails, new_fails=extra, summary=summ,
               status='KILLED' if (extra or (rc != 0 and rc0 == 0)) else 'SURVIVED')
    res.append(rec)
    print(f"{name:34s} {rec['status']:9s} rc={rc} nfail={len(fails)} {summ[:44]} | {'; '.join(x[:46] for x in extra[:4])}")
json.dump(res, open(OUTJ, 'w'), ensure_ascii=False, indent=1)
shutil.rmtree(root, ignore_errors=True)
