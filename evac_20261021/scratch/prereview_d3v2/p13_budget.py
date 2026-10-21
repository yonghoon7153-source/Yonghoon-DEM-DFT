#!/usr/bin/env python3
"""PRE-D3V2 탐침 13 — v2 §3-6 규모 · 일정 [추정] 이 v2 규칙에서 나온 수와 맞는가.

(a) R02 세분 상한 — '이웃 |ΔI| > κ·2·u_ref 인 칸에 중점 · 최대 2 회 · 세분 수준 = 그 칸 양 끝 중 B 가 있는 시험이면 A · B'
    ⇒ 미리 셀 수 있다 (상한).  설계 = "+ 세분 (가파른 칸만 · 미리 셀 수 없음)".
(b) T2 런 길이 — 설계 = 1.6 s 상수 · 생성기 run_steps = 정착 settle_time(2R) + 2 바퀴.
(c) 충진 f_cal (⬜ 0.11 – 0.30) — N = f × 8.27×10⁵ · 설계 합계 = 10 만 parcel 기준만.
(d) 합 — 설계 13.4–33.9 일 ↔ (b) · (c) · (a) 를 넣은 범위.
[추정] 처리량 ∝ 1/N (parcel 수 비례) · 3 슬롯 · 설계와 같은 T1 · T3 [추정] 값.

재실행: python3 -I p13_budget.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
m = c.m
ref = c.computed_numbers('lab20261014')
# (a) 세분 상한 — T2 B 수준 = X1 X3 X5 X7 → 모든 칸에 B 끝 → 새 수준마다 A·B
t2_cells, t2_runs = 7, 0
cells = t2_cells
for rnd in range(2):
    t2_runs += 2 * cells          # 칸마다 중점 하나 × (A · B)
    cells *= 2
t1_cells, t1_runs = 3, 0          # 탭 4 수준 (전부 A · B)
cells = t1_cells
for rnd in range(2):
    t1_runs += 2 * cells
    cells *= 2
# (b) T2 런 길이
p20 = m.plan(100000, cgf=151.4, dens_gen='lab20261014', stiffen_se=20.0)
rpm = m.rpm_for_fr(m.FR_ANCHOR, p20['R'])
st = m.run_steps(p20, rpm, 2.0)
sim = (2 * st['steps_fill'] + st['steps_run']) * p20['dt']
steps_per_s = 1.0 / p20['dt']
t2_gen = [sim * steps_per_s / th / 86400.0 for th in (70.0, 63.0)]
t2_doc = [ref['t2_run_d_lo'], ref['t2_run_d_hi']]
t1s = (ref['t1_short_lo'], ref['t1_short_hi'])
t1t = (ref['t1_tap_lo'], ref['t1_tap_hi'])
t1p = (ref['t1_pour_lo'], ref['t1_pour_hi'])
c2r = (ref['c2_run_lo'], ref['c2_run_hi'])


def total(t2, nscale=1.0):
    t2 = [v * nscale for v in t2]
    c0 = ((9 * t2[0] + 6 * t1s[0]) / 3, (9 * t2[1] + 6 * t1s[1]) / 3)
    c1 = ((12 * t2[0] + 8 * t1t[0] + 4 * t1p[0]) / 3, (12 * t2[1] + 8 * t1t[1] + 4 * t1p[1]) / 3)
    c2 = ((7 * c2r[0] + 6 * t2[0]) / 3, (11 * c2r[1] + 10 * t2[1]) / 3)
    return dict(c0=c0, c1=c1, c2=c2, sum=(c0[0] + c1[0] + c2[0], c0[1] + c1[1] + c2[1]))


n_f = {f: f * ref['n_per_fill'] for f in (0.11, 0.30)}
res = dict(
    refine_upper_runs=dict(T2=t2_runs, T1_tap=t1_runs, total=t2_runs + t1_runs,
                           days=((t2_runs * t2_gen[0] + t1_runs * t1t[0]) / 3, (t2_runs * t2_gen[1] + t1_runs * t1t[1]) / 3)),
    t2_sim_s_generator=sim, t2_settle_s=2 * st['steps_fill'] * p20['dt'], t2_rot_s=st['steps_run'] * p20['dt'],
    t2_run_days_doc=t2_doc, t2_run_days_generator=t2_gen,
    N_at_f=n_f,
    totals_doc_basis=total(t2_doc), totals_generator_t2=total(t2_gen),
    totals_generator_t2_f030=total(t2_gen, n_f[0.30] / 1e5), totals_generator_t2_f011=total(t2_gen, n_f[0.11] / 1e5),
)
pcommon.dump('p13_budget.json', res)
print('(a) R02 세분 상한 (2 회 · A·B):', res['refine_upper_runs'])
print(f'(b) T2 모사 시간 — 생성기 {sim:.3f} s (정착 {res["t2_settle_s"]:.3f} + 회전 {res["t2_rot_s"]:.3f}) ↔ 설계 1.6 s · 런 일 생성기 {t2_gen} ↔ 설계 {t2_doc}')
print('(c) N(f):', {k: round(v) for k, v in n_f.items()})
for k in ('totals_doc_basis', 'totals_generator_t2', 'totals_generator_t2_f011', 'totals_generator_t2_f030'):
    print(f'(d) {k}:', {kk: tuple(round(x, 1) for x in vv) for kk, vv in res[k].items()})
