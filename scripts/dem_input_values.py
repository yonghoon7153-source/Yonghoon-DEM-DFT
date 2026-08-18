#!/usr/bin/env python3
"""LHS 설계 CSV → **LIGGGHTS 덱 입력값 표** (사용자 엑셀 시트와 같은 계산).

사용자 시트(`input_real_1_t~5`)의 계산 셀 **19개를 전수 검산해 전부 일치**함을 확인하고
(`--verify-sheet`), 그 계산을 설계 100+ 행에 그대로 적용한다.

★ 시트 규약 (검산 완료):
    RVE 면적      = (rve_µm × 1e-4)²  cm²
    활물질 로딩    = 목표 면용량 / 활물질 비용량 × 1000   mg/cm²
    질량비        = am : (100−am) 정규화
    실제 질량 AM  = 로딩 × 1e-3 × 면적                      g
    실제 필요 부피 = m_AM/ρ_AM + m_SE/ρ_SE                  cm³
    높이(상별)     = (m/ρ)/면적 × 1e4                        µm   ← **고체만 (ε = 0)**
    Sim 변환      = 길이 ×1000 · 영률 ×0.001 · 압력 ×0.001
    생성 구역     = Sim 필요부피 / (Sim_RVE² × Sim_설정높이)

★ 시트가 비워 둔 칸을 채운다: 목표 두께 · plate 높이 · **입자수 P/S/SE**.

⚠⚠ **가장 위험한 칸은 `생성 구역`이다.**  그 값은 `Sim_설정 높이`로 나눈 것인데, 덱의
   `region reg_mix block ... z_lo z_hi` 와 **반드시 같아야** 한다.  업로드된 `input_real_1`
   은 `0.005 → 0.30` (높이 0.295) 인데 시트는 0.5 를 쓴다 — 그대로 두면 실현 부피분율이
   **1.69배** 어긋나고, 그러면 로딩(=면용량)이 틀린다.  `--h-set` 로 덱 값을 넣을 것.

  python3 scripts/dem_input_values.py --verify-sheet
  python3 scripts/dem_input_values.py --design docs/data/lhs_design_20260818.csv \\
      --out docs/data/dem_input_values_20260818.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import sys

#  ── 재료 상수 (사용자 시트 = 정본) ────────────────────────────────────────────
CAP_MAH_G = 200.0                     # NCM811 활물질 비용량 (⚠ 실제 용량은 180~200)
RHO_AM, RHO_SE = 4.8, 2.0             # g/cm³ (진밀도)
E_AM_PA, E_SE_PA = 1.40e11, 2.40e10
NU_AM, NU_SE = 0.25, 0.30
SC_R, SC_E = 1000.0, 0.001            # scale factor — 길이 ×1000 · 영률/압력 ×0.001
PRESS_MPA = 300.0
EPS_ASSUMED = 0.183                   # ★ 시트 물리(16.04 µm/mAh, ε=0)와 코퍼스 회귀
#   (19.64 µm/mAh)를 맞추면 함축 ε = 0.183 이 나온다.  두 경로가 독립인데 일치한다.
H_SET_M_DEFAULT = 0.5                 # Sim 설정 높이 — ⚠ 덱의 reg_mix z-span 과 같아야 한다
VOLFRAC_TARGET = 0.25                 # 시트의 8 mAh 케이스가 0.257 → 그 정도를 목표로 역산


def sheet(am_pct, load_target, rve_um, d_p, d_s, d_se, ps,
          eps=EPS_ASSUMED, h_set=H_SET_M_DEFAULT):
    """한 행의 덱 입력값 전부.  d_* 는 **직경 µm**, ps 는 AM 중 대립 몫."""
    o = {}
    o['rve_area_cm2'] = (rve_um * 1e-4) ** 2
    o['am_loading_mg_cm2'] = load_target / CAP_MAH_G * 1000.0
    o['w_am'] = am_pct / 100.0
    o['w_se'] = 1.0 - o['w_am']
    o['m_am_g'] = o['am_loading_mg_cm2'] * 1e-3 * o['rve_area_cm2']
    o['m_se_g'] = o['m_am_g'] * o['w_se'] / o['w_am']
    o['m_total_g'] = o['m_am_g'] + o['m_se_g']
    v_am, v_se = o['m_am_g'] / RHO_AM, o['m_se_g'] / RHO_SE
    o['v_needed_cm3'] = v_am + v_se
    o['h_am_um'] = v_am / o['rve_area_cm2'] * 1e4          # 고체만
    o['h_se_um'] = v_se / o['rve_area_cm2'] * 1e4
    o['h_solid_um'] = o['h_am_um'] + o['h_se_um']          # ε = 0 두께
    o['thickness_target_um'] = o['h_solid_um'] / (1.0 - eps)
    #  ── Sim 단 ────────────────────────────────────────────────────────────
    o['sim_rve_m'] = rve_um * 1e-6 * SC_R
    o['sim_v_needed_m3'] = o['v_needed_cm3'] * 1e-6 * SC_R ** 3
    o['sim_h_set_m'] = h_set
    o['insert_volfrac'] = o['sim_v_needed_m3'] / (o['sim_rve_m'] ** 2 * h_set)
    o['sim_E_am_Pa'], o['sim_E_se_Pa'] = E_AM_PA * SC_E, E_SE_PA * SC_E
    o['sim_press_MPa'] = PRESS_MPA * SC_E
    for nm, d in (('p', d_p), ('s', d_s), ('se', d_se)):
        o[f'sim_radius_{nm}_m'] = (float('nan') if d is None or d != d
                                   else d / 2.0 * 1e-6 * SC_R)
    #  ★ 권장 설정높이 — 생성 구역이 목표 부피분율이 되게 역산.  면용량 2 mAh 는 시트의
    #    8 mAh 대비 필요 부피가 1/4 이라, 시트의 0.5 m 를 그대로 쓰면 분율이 **6 %** 로 떨어져
    #    입자가 0.5 m 를 낙하해야 한다 = settling 이 불필요하게 길어진다.
    o['h_set_recommended_m'] = o['sim_v_needed_m3'] / (o['sim_rve_m'] ** 2 * VOLFRAC_TARGET)
    o['sim_thickness_target_m'] = o['thickness_target_um'] * 1e-6 * SC_R
    o['sim_plate_z_m'] = o['sim_thickness_target_m']       # 바닥 벽이 z=0
    #  ── ★ 입자수 (시트가 비워 둔 칸) ──────────────────────────────────────
    def n_of(d, vol_cm3):
        if d is None or d != d or d <= 0:
            return float('nan')
        return vol_cm3 / ((math.pi / 6.0) * (d * 1e-4) ** 3)
    o['n_am_p'] = n_of(d_p, v_am * ps)
    o['n_am_s'] = n_of(d_s, v_am * (1.0 - ps))
    o['n_se'] = n_of(d_se, v_se)
    o['n_total'] = sum(v for v in (o['n_am_p'], o['n_am_s'], o['n_se']) if v == v)
    return o


_SHEET_EXPECT = [   # (라벨, 시트값, 키)  — 사용자 시트 input_real_1 (8 mAh, am 81.6…)
    ('RVE 면적 (cm²)', 2.50e-05, 'rve_area_cm2'),
    ('활물질 로딩 (mg/cm²)', 40.0, 'am_loading_mg_cm2'),
    ('질량비 AM', 0.816327, 'w_am'),
    ('질량비 SE', 0.183673, 'w_se'),
    ('실제 질량 AM (g)', 1.00e-06, 'm_am_g'),
    ('실제 질량 SE (g)', 2.25e-07, 'm_se_g'),
    ('전체 혼합물 질량 (g)', 1.23e-06, 'm_total_g'),
    ('실제 필요 부피 (cm³)', 3.21e-07, 'v_needed_cm3'),
    ('높이 AM (µm)', 83.0, 'h_am_um'),
    ('높이 SE (µm)', 45.0, 'h_se_um'),
    ('Sim_RVE (m)', 0.05, 'sim_rve_m'),
    ('Sim_실제 필요 부피 (m³)', 3.2e-04, 'sim_v_needed_m3'),
    ('생성 구역', 0.257, 'insert_volfrac'),
    ('Sim_영률 AM (Pa)', 1.4e8, 'sim_E_am_Pa'),
    ('Sim_영률 SE (Pa)', 2.4e7, 'sim_E_se_Pa'),
    ('Sim_압력 (MPa)', 0.30, 'sim_press_MPa'),
    ('Sim_radius_P (m)', 6.00e-3, 'sim_radius_p_m'),
    ('Sim_radius_S (m)', 2.00e-3, 'sim_radius_s_m'),
    ('Sim_radius_SE (m)', 5.00e-4, 'sim_radius_se_m'),
]


def verify_sheet(tol=6e-3):
    """사용자 엑셀의 계산 셀을 전수 재계산해 대조 (시트 반올림 폭 안)."""
    o = sheet(am_pct=100 * 80 / 98, load_target=8.0, rve_um=50.0,
              d_p=12.0, d_s=4.0, d_se=1.0, ps=1.0)
    ok, bad = 0, []
    print('사용자 시트 계산 셀 검산 (input_real_1, 8 mAh/cm²)')
    for lbl, want, key in _SHEET_EXPECT:
        got = o[key]
        good = abs(got - want) / max(abs(want), 1e-30) < tol
        (ok := ok + 1) if good else bad.append(lbl)
        print(f"  {'✓' if good else '✗'} {lbl:26s} 시트 {want:<11.6g} 계산 {got:<11.6g}"
              + ('' if good else f'  ← {100 * (got / want - 1):+.2f} %'))
    print(f'\n검산 {ok}/{len(_SHEET_EXPECT)} 일치' + (f'   불일치: {bad}' if bad else ''))
    print(f"\n시트가 비워 둔 칸 (계산하면):")
    print(f"  고체만 높이 (ε=0)   {o['h_solid_um']:.1f} µm")
    print(f"  목표 두께 (ε={EPS_ASSUMED})  {o['thickness_target_um']:.1f} µm"
          f"  → plate 높이 {o['sim_plate_z_m']:.4f} m")
    print(f"  입자수  AM {o['n_am_p']:,.0f} · SE {o['n_se']:,.0f} "
          f"(합 {o['n_total']:,.0f})")
    print(f"\n★ ε = {EPS_ASSUMED} 의 근거: 시트 물리는 {o['h_solid_um'] / 8.0:.2f} µm/mAh (ε=0)이고 "
          f"코퍼스 291건 회귀는 19.64 µm/mAh — 두 **독립** 경로를 맞추면 ε 가 나온다.")
    return 1 if bad else 0


def _f(r, k):
    v = r.get(k, '')
    return float(v) if v not in ('', None) else float('nan')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--design', default='')
    ap.add_argument('--out', default='')
    ap.add_argument('--load', type=float, default=None,
                    help='목표 면용량 mAh/cm² (기본 = 설계 CSV 의 loading_mAh_cm2)')
    ap.add_argument('--eps', type=float, default=EPS_ASSUMED)
    ap.add_argument('--h-set', type=float, default=H_SET_M_DEFAULT,
                    help='⚠ 덱의 reg_mix z-span 과 **같아야** 한다 (생성 구역이 그것으로 나뉜다)')
    ap.add_argument('--verify-sheet', action='store_true')
    a = ap.parse_args()
    if a.verify_sheet or not a.design:
        raise SystemExit(verify_sheet())

    rows = list(csv.DictReader(open(a.design, encoding='utf-8')))
    out = []
    for r in rows:
        load = a.load if a.load is not None else _f(r, 'loading_mAh_cm2')
        o = sheet(_f(r, 'am_pct'), load, _f(r, 'rve_um'),
                  _f(r, 'd_am_p_um'), _f(r, 'd_am_s_um'), _f(r, 'd_se_um'),
                  _f(r, 'ps_frac'), eps=a.eps, h_set=a.h_set)
        out.append({'case_id': r['case_id'], 'block': r['block'],
                    'am_pct': _f(r, 'am_pct'), 'ps_frac': _f(r, 'ps_frac'),
                    'd_am_p_um': r['d_am_p_um'], 'd_am_s_um': r['d_am_s_um'],
                    'd_se_um': r['d_se_um'], 'loading_mAh_cm2': load, **o})
    cols = list(out[0])
    if a.out:
        with open(a.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, cols)
            w.writeheader()
            for o in out:
                w.writerow({c: ('' if (isinstance(o[c], float) and o[c] != o[c])
                                else (f'{o[c]:.6g}' if isinstance(o[c], float) else o[c]))
                            for c in cols})
        print(f'→ {a.out}   ({len(out)} 행 · {len(cols)} 열)')

    import numpy as np
    nt = np.array([o['n_total'] for o in out])
    vf = np.array([o['insert_volfrac'] for o in out])
    th = np.array([o['thickness_target_um'] for o in out])
    print(f"\n{len(out)} 행 요약 (면용량 {out[0]['loading_mAh_cm2']:g} mAh/cm² · "
          f"ε {a.eps} · Sim 설정높이 {a.h_set} m)")
    print(f"  목표 두께      {th.min():>8.1f} – {th.max():>8.1f} µm  (중앙 {np.median(th):.1f})")
    print(f"  생성 구역      {vf.min():>8.4f} – {vf.max():>8.4f}     (중앙 {np.median(vf):.4f})")
    print(f"  전체 입자수    {nt.min():>8,.0f} – {nt.max():>8,.0f}    (중앙 {np.median(nt):,.0f} · "
          f"합 {nt.sum():,.0f})")
    hr = np.array([o['h_set_recommended_m'] for o in out])
    print(f"  ★ 권장 설정높이 {hr.min():.3f} – {hr.max():.3f} m (중앙 {np.median(hr):.3f}) — "
          f"생성 구역을 {VOLFRAC_TARGET} 로 맞춘 값.  현재 {a.h_set} m 를 쓰면 분율이 "
          f"{np.median(vf):.3f} 라 입자가 그 높이를 낙하한다 = settling 이 길어진다")
    hi = [o for o in out if o['insert_volfrac'] > 0.5]
    if hi:
        print(f"  ⚠ 생성 구역 > 0.5 인 행 {len(hi)}개 — `insert/pack` 이 못 채울 수 있다.  "
              f"`--h-set` 를 키우고 덱의 reg_mix 도 같이 키울 것")
    print("  ⚠⚠ `생성 구역` 은 **덱의 `region reg_mix` z-span** 으로 나눈 값이다.  "
          "둘이 다르면 실현 로딩(=면용량)이 그 비만큼 틀린다 — 업로드된 input_real_1 은 "
          "0.005→0.30 (높이 0.295) 인데 시트 기본은 0.5 다.")
    sys.stdout.flush()
