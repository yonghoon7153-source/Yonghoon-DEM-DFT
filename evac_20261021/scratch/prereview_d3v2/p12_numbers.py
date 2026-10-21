#!/usr/bin/env python3
"""PRE-D3V2 탐침 12 — v2 문서의 숫자 86 (V2_DOC_NUMBERS) ↔ 문서 본문 ↔ 독립 계산 (생성기 원시 함수 + 이 탐침의 식).

(1) 표의 각 문자열이 v2 문서 본문에 실제로 있는가 (C12 는 문서를 읽지 않는다 — 표 ↔ 계산만 비교)
(2) 독립 계산 — 스크립트의 computed_numbers 를 쓰지 않고 생성기 plan() · rpm_for_fr · 덱 경로 (gm_arm · ced_matrix_geomean ·
    _assert_ceiling_pairwise · pair_overlap) 를 직접 부르고 v_stick · 비 · 압력 · 질량은 이 탐침의 식으로
(3) 실제 생성기 덱 경로의 천장 — D2 팔 (ρ 1 · 0.3 · 벽 0.0256·ρ) 에서 SystemExit 가 나는 SE–SE Bo (이분법)
(4) T2 한 런 길이 — 설계 = 1.6 s 상수 · 생성기 run_steps (정착 = settle_time(2R) + 2 바퀴) 와 비교

재실행: python3 -I p12_numbers.py
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
m = c.m
doc = open(os.path.join(pcommon.REPO, 'docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261021.md'), encoding='utf-8').read()
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def doc_forms(s):
    if 'e' in s:
        mant, ex = s.split('e')
        return [f'{mant}×10{ex.lstrip("+").translate(SUP)}']
    return [s]


# (1) 표 ↔ 문서
missing, ctx = [], {}
for k, v in c.V2_DOC_NUMBERS.items():
    forms = doc_forms(v)
    hits = []
    for fm in forms:
        for mt in re.finditer(r'(?<![0-9.])' + re.escape(fm) + r'(?![0-9])', doc):
            hits.append(doc[max(0, mt.start() - 50):mt.end() + 30].replace('\n', ' '))
    if not hits:
        missing.append((k, v))
    ctx[k] = hits[:2]

# (2) 독립 계산
LAB = 'lab20261014'
p = m.plan(100000, cgf=151.4, dens_gen=LAB)
p20 = m.plan(100000, cgf=151.4, dens_gen=LAB, stiffen_se=20.0)
g = 9.81
R, L = p['R'], p['L']
rpm = 60.0 / (2 * math.pi) * math.sqrt(m.FR_ANCHOR * g / R)
wR = 2 * math.pi * rpm / 60.0 * R * 1e3
dse = p['d']['SE']
vpar = math.pi / 6 * dse ** 3
vdrum = math.pi * R ** 2 * L
nu = m.PHASE_MECH['SE'][0]
rho = {'SE': 1.64, 'AM': 4.85}


def vstick(bo, E):
    """SJKR + Hertz 고립 접촉 (점착 지배): B = 2πR*·CED · A = (4/3)E*√R* · δ₀ = (B/A)² · 분리 일 W = Bδ₀²/10 (∫ (Bδ − Aδ^1.5) dδ, 0..δ₀) ·
    붙음 = 되튐 에너지 e²(KE + W) < W ⇒ v < √(2W(1 − e²)/(e²·m*)) · m* = m/2."""
    r = dse / 2.0
    ced = m.ced_for_bond(bo, r, nu, rho['SE'], E=E)
    rs = r / 2.0
    es = E / (2.0 * (1.0 - nu ** 2))
    B, A = 2 * math.pi * rs * ced, (4.0 / 3.0) * es * math.sqrt(rs)
    d0 = (B / A) ** 2
    W = B * d0 ** 2 / 10.0
    ms = (4.0 / 3.0) * math.pi * r ** 3 * rho['SE'] * 1000.0 / 2.0
    e = m.COR
    return math.sqrt(2 * W * (1 - e * e) / (e * e * ms)) * 1e3


ESE, ESE20 = p['E']['SE'], p20['E']['SE']


def ov(bo, E):
    return m.overlap_for_ced(m.ced_for_bond(bo, dse / 2.0, nu, rho['SE'], E=E), dse / 2.0, nu, E=E) * 100.0


# (3) 실제 덱 경로 천장 — gm_arm + ced_matrix_geomean (soft E_PHASE · 모든 쌍 · 벽 포함)
def gm_ok(bo, rho_unc, cgf=151.4):
    pp = m.plan(100000, cgf=cgf, dens_gen=LAB)
    a = m.gm_arm({'AM_P': rho_unc, 'AM_S': rho_unc, 'SE': 1.0}, gamma_wall=m.gm_wall_from_ncm(rho_unc), bo_se=bo,
                 rho_uncoated_ncm=rho_unc)
    try:
        M = m.ced_matrix_geomean(a, pp['d'], dens=pp['dens'])
    except SystemExit as e:
        return False, str(e)
    return True, M


def gm_ceiling(rho_unc, cgf=151.4):
    lo, hi = 1.0, 1e5
    msg = None
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        ok, r = gm_ok(mid, rho_unc, cgf)
        if ok:
            lo = mid
        else:
            hi, msg = mid, r
    return lo, msg


ceil_rho1, msg1 = gm_ceiling(1.0)
ceil_rho03, msg03 = gm_ceiling(0.3)
ceil200, msg200 = gm_ceiling(1.0, cgf=200.0)

# (4) T2 런 길이 — 생성기 run_steps (×20 계획 · 2 바퀴)
st = m.run_steps(p20, rpm, 2.0)
sim_s = (2 * st['steps_fill'] + st['steps_run']) * p20['dt']
steps_per_s = 1.0 / p20['dt']
t2_days = [sim_s * steps_per_s / th / 86400.0 for th in (70.0, 63.0)]

# 독립 비 · 압력 · 질량
ratio_amp = (m.D_REAL_UM['AM_P'] / m.D_REAL_UM['SE']) ** 2 * rho['AM'] / rho['SE']
ratio_ams = (m.D_REAL_UM['AM_S'] / m.D_REAL_UM['SE']) ** 2 * rho['AM'] / rho['SE']
wt = {'AM_P': 80 * 0.7, 'AM_S': 80 * 0.3, 'SE': 18.0}
rho_mix = sum(wt.values()) / (wt['AM_P'] / 4.85 + wt['AM_S'] / 4.85 + wt['SE'] / 1.64)
lo_t, hi_t = 0.0, 2 * math.pi
for _ in range(100):
    th = 0.5 * (lo_t + hi_t)
    if (th - math.sin(th)) / (2 * math.pi) > 0.30:
        hi_t = th
    else:
        lo_t = th
depth = 1 - math.cos(lo_t / 2)
indep = {
    'drum_D_mm': 2 * R * 1e3, 'drum_L_mm': L * 1e3, 'rpm': rpm, 'wR_mm_s': wR, 'n_per_fill': vdrum * 0.6 / vpar,
    'dt_x20': p20['dt'], 'ceiling_soft (실제 덱 경로 · ρ 1)': ceil_rho1, 'ceiling (ρ 0.3)': ceil_rho03, 'ceiling_cgf200 (ρ 1)': ceil200,
    'ov_637_soft': ov(637.32, ESE), 'ov_850_soft': ov(849.76, ESE), 'ov_637_x20': ov(637.32, ESE20),
    'vstick_0212_x20': vstick(0.21244, ESE20), 'vstick_212_x20': vstick(212.44, ESE20), 'vstick_637_x20': vstick(637.32, ESE20),
    'vstick_ceil_x20': vstick(ceil_rho1, ESE20), 'vstick_0212_soft': vstick(0.21244, ESE), 'vstick_21_x20': vstick(21.244, ESE20),
    'vstick_637_g (÷268)': vstick(637.32 / 268.0, ESE20),
    'se_vol_pct': p['phi']['SE'] * 100, 'se_num_pct': p['n']['SE'] / sum(p['n'].values()) * 100,
    'd_over_amp': 2 * R / p['d']['AM_P'], 'd_over_se': 2 * R / dse,
    'bo_aa_ratio_amp': ratio_amp, 'bo_aa_ratio_ams': ratio_ams, 'rho_mix': rho_mix, 'depth_over_R': depth,
    't5_pa': 0.6 * rho_mix * 1000 * g * depth * R, 't2_cell_cm3': vdrum * 1e6,
    'T2 모사 시간 s (생성기 run_steps · 정착 포함)': sim_s, 'T2 정착 s': 2 * st['steps_fill'] * p20['dt'],
    'T2 한 런 일 (생성기 · 70–63 step/s)': t2_days,
}
ref = c.computed_numbers(LAB)
res = dict(table_missing_in_doc=missing, table_size=len(c.V2_DOC_NUMBERS), contexts=ctx, independent=indep,
           script_values={k: ref[k] for k in ('drum_D_mm', 'rpm', 'ceiling_soft', 'ov_637_soft', 'vstick_637_x20', 'vstick_ceil_x20',
                                                  't5_pa', 't2_run_d_lo', 't2_run_d_hi', 'ceiling_cgf200')},
           ceiling_messages=dict(rho1=msg1, rho03=msg03, cgf200=msg200))
pcommon.dump('p12_numbers.json', res)
print(f'(1) 표 {len(c.V2_DOC_NUMBERS)} 개 중 문서 본문에 그 표기가 없는 것 {len(missing)}: {missing}')
print('(2)(3)(4) 독립 계산:')
for k, v in indep.items():
    print(f'    {k:40s} {v}')
print('    스크립트 값 (대조):', {k: round(v, 6) for k, v in res['script_values'].items()})
print('    천장 거부 메시지 (ρ 1):', msg1)
print('    천장 거부 메시지 (ρ 0.3):', msg03)
