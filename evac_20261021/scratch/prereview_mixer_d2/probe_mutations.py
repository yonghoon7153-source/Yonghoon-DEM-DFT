#!/usr/bin/env python3
"""Probe E — mutation tests on the HEAD generator's D2 / density code: does --selftest fail for the RIGHT reason?

Each mutation = one exact-substring replacement (must occur exactly once) in a copy of gen/mmd_HEAD.py, placed in
mut/<name>/make_mixer_deck.py next to copies of additives.py and make_mixer_baffles.py (DG1 reads additives.py, the CLI
loads the baffle helper).  Runs `python3 -I -B make_mixer_deck.py --selftest` (one at a time, nice 19) and records the
FAIL lines.  KILLED = >=1 check failed; SURVIVED = selftest still all-PASS.
usage: python3 -I -B probe_mutations.py <repo_worktree>
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
SRC = open(os.path.join(HERE, 'gen', 'mmd_HEAD.py'), encoding='utf-8').read()
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
    ('M10_wallncm_ignores_rho', "    return GM_WALL_HARE2026 * _gm_num(rho_uncoated, 'ρ_비코팅 NCM = γ_NCM/γ_SE')",
     "    _gm_num(rho_uncoated, 'x')\n    return GM_WALL_HARE2026"),
    ('M11_gmnum_allow_zero', '    if not (math.isfinite(v) and v > 0.0):\n        raise SystemExit(f\'⛔ D2 결합 규칙: {what}',
     '    if not (math.isfinite(v) and v >= 0.0):\n        raise SystemExit(f\'⛔ D2 결합 규칙: {what}'),
    ('M12_gmnum_allow_nan_inf', '    if not (math.isfinite(v) and v > 0.0):\n        raise SystemExit(f\'⛔ D2 결합 규칙: {what}',
     '    if not (v > 0.0 or math.isnan(v)):\n        raise SystemExit(f\'⛔ D2 결합 규칙: {what}'),
    ('M13_rho_check_removed', '        if gw != gm_wall_from_ncm(rho_uncoated_ncm):', '        if False:'),
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
    ('M24_meta_wall_rule_dropped', "        if a_.get('wall_rule'):\n            meta['adhesion_rule'].update(",
     "        if False:\n            meta['adhesion_rule'].update("),
]
res = []
mroot = os.path.join(HERE, 'mut')
os.makedirs(mroot, exist_ok=True)
for name, old, new in MUT:
    n = SRC.count(old)
    rec = dict(mutation=name, occurrences=n)
    if n != 1:
        rec['status'] = 'NOT_APPLIED'
        res.append(rec)
        print(f'{name}: NOT APPLIED (occurrences {n})')
        continue
    d = os.path.join(mroot, name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'make_mixer_deck.py'), 'w', encoding='utf-8').write(SRC.replace(old, new))
    for f in ('additives.py', 'make_mixer_baffles.py'):
        shutil.copy(os.path.join(REPO, 'scripts', f), os.path.join(d, f))
    p = subprocess.run(['nice', '-n', '19', sys.executable, '-I', '-B', os.path.join(d, 'make_mixer_deck.py'), '--selftest'],
                       capture_output=True, text=True, env=dict(os.environ, OPENBLAS_NUM_THREADS='1'), timeout=600)
    fails = [l.strip()[6:].strip()[:90] for l in p.stdout.splitlines() if l.startswith('  FAIL')]
    tail = [l for l in p.stdout.splitlines() if 'selftest:' in l]
    rec.update(rc=p.returncode, n_fail=len(fails), fails=fails, summary=tail[-1] if tail else (p.stderr.strip().splitlines() or [''])[-1],
               status='KILLED' if (p.returncode != 0 or fails) else 'SURVIVED')
    res.append(rec)
    print(f"{name:28s} {rec['status']:9s} rc={p.returncode} nfail={len(fails)} {rec['summary'][:60]} | {'; '.join(x[:40] for x in fails[:4])}")
json.dump(res, open(os.path.join(HERE, 'probe_mutations.json'), 'w'), ensure_ascii=False, indent=1)
