#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""정확 union · 질량 보존 두께 · φ · physics v2 후보 표지 — 웹앱 ③ (1저자 비준 09-30 밤 · J20-l).

  python3 webapp/test_closed_param_exact_union.py      # 종료코드 0 = PASS

  [X] dem_analysis_core.calc_porosity_union_exact — 상자 [0,Lx)×[0,Ly)×[0,판) 무작위 점 (x · y 주기 · 벽 밖 부피 제외 ·
      세 입자 이상 겹침까지 정확) = LHS 인계 porosity_union_exact_pct 와 같은 계산 (lhs_union_webapp.coverage).
      해석해가 있는 작은 배치로 4σ 안: 겹친 두 구 · 바닥을 뚫은 구 · 주기 경계를 넘는 구 · 세 구 겹침 (쌍 렌즈가 틀리는 곳)
  [A] 분석기 CLI (웹앱과 같은 analyze_contacts_bimodal.py) 가 full_metrics.json 에 정확 union · 통계 오차 · 상태 ·
      질량 보존 두께 = 판 간격 × (1 − ε_sphere)/(1 − ε_exact) · φ_i 질량 보존 = (1 − ε_exact) × 부피 몫 (J20-e (라)) 을 싣는다
  [W] 웹앱: 케이스 화면 · 망 요약 행 · 그룹 표 열 · 그룹 그림 · 보고서 · 툴팁이 같은 이름 · 한정어로 보인다
  [V] physics v2 = 후보 · 미검증 (LHSC-10): 케이스 화면에 표지와 함께 · 예측기 자동 타깃 · 등급 축에서 제외
"""
import json
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def sv(r):
    return 4.0 / 3.0 * math.pi * r ** 3


def lens(r1, r2, d):
    dl = r1 + r2 - d
    return math.pi * dl ** 2 / (12 * d) * (d ** 2 + 2 * d * (r1 + r2) - 3 * (r1 - r2) ** 2)


def cap(r, h):
    return math.pi * h * h * (3 * r - h) / 3.0


def within(res, want_void_pct, name, k=4.0):
    got, se = res.get('porosity_union_exact_pct'), res.get('porosity_union_exact_se_pct')
    ok = got is not None and se is not None and abs(got - want_void_pct) <= k * se + 1e-9
    return chk(name, ok, f'got {got} ± {se} · want {want_void_pct:.5f}')


def section_x():
    print('[X] calc_porosity_union_exact — 해석해 대조')
    import dem_analysis_core as C
    f = getattr(C, 'calc_porosity_union_exact', None)
    if not chk('X0 dem_analysis_core.calc_porosity_union_exact 가 있다', callable(f)):
        return
    L, H, N = 0.01, 0.01, 1_000_000
    vb = L * L * H
    a = {1: dict(x=0.004, y=0.005, z=0.005, radius=0.0015, type=1),
         2: dict(x=0.006, y=0.005, z=0.005, radius=0.0015, type=1)}
    want = 100 * (1 - (2 * sv(0.0015) - lens(0.0015, 0.0015, 0.002)) / vb)
    r = f(a, H, L, None, mc_n=N, seed=11)
    within(r, want, 'X1 겹친 두 구 (상자 안) — union = 두 구 − 렌즈')
    chk('X2 상태 OK · 점 수 · 시드 기록', r.get('union_exact_status') == 'OK' and r.get('union_exact_mc_n') == N
        and r.get('union_exact_mc_seed') == 11, repr({k: r.get(k) for k in ('union_exact_status', 'union_exact_mc_n', 'union_exact_mc_seed')}))
    b = {1: dict(x=0.005, y=0.005, z=0.0005, radius=0.0015, type=1)}
    want_b = 100 * (1 - (sv(0.0015) - cap(0.0015, 0.001)) / vb)
    within(f(b, H, L, None, mc_n=N, seed=12), want_b, 'X3 바닥을 뚫은 구 — 바닥 아래 부피는 고체가 아니다 (벽 밖 제외)')
    c = {1: dict(x=0.0095, y=0.005, z=0.005, radius=0.0015, type=1)}
    within(f(c, H, L, None, mc_n=N, seed=13), 100 * (1 - sv(0.0015) / vb), 'X4 x 경계를 넘는 구 — 주기라 온전한 구')
    t = {1: dict(x=0.005, y=0.005, z=0.005, radius=0.0015, type=1),
         2: dict(x=0.005, y=0.005, z=0.005, radius=0.0015, type=1),
         3: dict(x=0.005, y=0.005, z=0.005, radius=0.0015, type=1)}
    within(f(t, H, L, None, mc_n=N, seed=14), 100 * (1 - sv(0.0015) / vb),
           'X5 같은 자리 세 구 — union = 한 구 (쌍 렌즈 합은 여기서 틀린다)')
    r2 = f(a, H, L, None, mc_n=N, seed=11)
    chk('X6 같은 시드 → 같은 값 (재현)', r2.get('porosity_union_exact_pct') == r.get('porosity_union_exact_pct'))
    rr = f(a, H, 0.01, 0.008, mc_n=N, seed=15)
    within(rr, 100 * (1 - (2 * sv(0.0015) - lens(0.0015, 0.0015, 0.002)) / (0.01 * 0.008 * H)),
           'X7 비정사각 상자 (x 0.010 · y 0.008) — V_box = x · y · 판')
    off = f(a, H, L, None, mc_n=0)
    chk('X8 mc_n 0 → 계산 안 함 · 값 없음 · 상태 off', off.get('porosity_union_exact_pct') is None
        and off.get('union_exact_status') == 'off', repr(off))
    poly = {i: dict(x=0.0003 * i % L, y=0.005, z=0.005, radius=0.0001 + 1e-6 * i, type=1) for i in range(1, 40)}
    rp = f(poly, H, L, None, mc_n=10_000, seed=16)
    chk('X9 반경 종류가 너무 많으면 예외 없이 건너뜀 (값 없음 · 사유)', rp.get('porosity_union_exact_pct') is None
        and str(rp.get('union_exact_status', '')).startswith('skipped'), repr(rp.get('union_exact_status')))


def section_a():
    print('[A] 분석기 CLI → full_metrics.json')
    import test_closed_param_values as TV
    os.environ['DEM_UNION_MC_N'] = '400000'
    tmp = tempfile.mkdtemp(prefix='exact_union_')
    bed = TV.make_bed(os.path.join(tmp, 'A'))
    pr, m = TV.run_bed(bed)
    if not chk('A0 analyze_contacts_bimodal rc 0', pr.returncode == 0 and bool(m), (pr.stderr or '')[-500:]):
        return
    eu, se = m.get('porosity_union_exact_pct'), m.get('porosity_union_exact_se_pct')
    chk('A1 porosity_union_exact_pct · _se_pct · 상태 OK · 점 수', isinstance(eu, float) and isinstance(se, float)
        and m.get('union_exact_status') == 'OK' and m.get('union_exact_mc_n') == 400000,
        repr({k: m.get(k) for k in ('porosity_union_exact_pct', 'porosity_union_exact_se_pct', 'union_exact_status', 'union_exact_mc_n')}))
    if not isinstance(eu, float):
        return
    th, es = m.get('thickness_um'), m.get('porosity')
    want_th = th * (1 - es / 100) / (1 - eu / 100)
    chk('A2 질량 보존 두께 = 판 간격 × (1 − ε_sphere)/(1 − ε_exact)',
        abs(m.get('thickness_mass_conserving_um', float('nan')) - want_th) < 1e-9 * max(1, want_th),
        f"{m.get('thickness_mass_conserving_um')} vs {want_th}")
    ps, pa, sos = m.get('phi_se_mass_conserving'), m.get('phi_am_mass_conserving'), m.get('se_of_solid_vol')
    chk('A3 φ 질량 보존 = (1 − ε_exact) × 부피 몫 · 닫힘 φ_SE + φ_AM + ε_exact = 1',
        None not in (ps, pa, sos) and abs(ps - (1 - eu / 100) * sos) < 1e-12 and abs(ps + pa + eu / 100 - 1) < 1e-12,
        repr((ps, pa, sos)))
    want_sos = bed['phi_se'] / (bed['phi_se'] + bed['phi_am'])
    chk('A4 SE/고체 부피 몫 = 손계산', sos is not None and abs(sos - want_sos) < 1e-12, f'{sos} vs {want_sos}')
    chk('A5 쌍 렌즈 union ≠ 정확 union 을 구분해 둘 다 싣는다', m.get('porosity_union') is not None
        and m.get('porosity_union') != eu)
    chk('A6 숫자는 숫자 (문자열 아님)', not any(isinstance(m.get(k), str) for k in (
        'porosity_union_exact_pct', 'porosity_union_exact_se_pct', 'thickness_mass_conserving_um',
        'phi_se_mass_conserving', 'phi_am_mass_conserving', 'union_exact_mc_n')))


def section_w():
    print('[W] 웹앱 표시 — 같은 이름 · 한정어')
    import app as A
    keys = {k[2]: k[0] for k in A.GROUP_DISPLAY_KEYS}
    for key in ('porosity_union_exact_pct', 'thickness_mass_conserving_um', 'phi_se_mass_conserving', 'phi_am_mass_conserving'):
        chk(f'W1 그룹 표 열 {key}', key in keys)
    lab = keys.get('porosity_union_exact_pct')
    chk('W2 정확 union · 질량 보존 두께 = 낮을수록 좋음', lab in A.GROUP_LOWER_BETTER
        and keys.get('thickness_mass_conserving_um') in A.GROUP_LOWER_BETTER)
    tables = {'network_summary': {'columns': ['a', 'b', 'c', 'd'],
                                  'data': [['── 구조 ──', '', '', ''], ['Porosity ε_sphere (%)', '10.0', '10.0', '0%']]}}
    A.inject_dual_porosity_rows(tables, {'porosity_union': 12.0, 'overlap_fraction_pct': 2.0,
                                         'porosity_union_exact_pct': 12.6, 'porosity_union_exact_se_pct': 0.014,
                                         'thickness_mass_conserving_um': 31.2,
                                         'phi_se_mass_conserving': 0.3, 'phi_am_mass_conserving': 0.574})
    labels = [r[0] for r in tables['network_summary']['data']]
    chk('W3 망 요약에 정확 union 행 (몬테카를로 · 인계 규약)', any('exact' in l and 'Monte Carlo' in l for l in labels), repr(labels))
    chk('W4 망 요약에 질량 보존 두께 · φ 행', any('mass-conserving' in l and 'Thickness' in l for l in labels)
        and any('mass-conserving' in l and 'φ_SE' in l for l in labels), repr(labels))
    sh = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    chk('W5 케이스 화면 배지가 정확 union 값을 그린다', re.search(r'metrics\.porosity_union_exact_pct is not none', sh) is not None)
    gh = open(os.path.join(HERE, 'templates', 'group.html'), encoding='utf-8').read()
    chk('W6 그룹 그림 체크박스 porosity_union_exact_pct', 'value="porosity_union_exact_pct"' in gh)
    chk('W7 그룹 표 툴팁 (정확 union · 질량 보존)', "'Porosity (union exact)'" in gh and '질량 보존' in gh)
    import generate_comparison_plots as G
    chk('W8 그림 목록 porosity_union_exact_pct', 'porosity_union_exact_pct' in G.PLOT_REGISTRY)
    asrc = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    chk('W9 MD 보고서 · 쉬운 설명에 porosity_union_exact_pct', asrc.count('porosity_union_exact_pct') >= 4)


def section_v():
    print('[V] physics v2 = 후보 · 미검증 — 표지 · ML · 등급 제외')
    import app as A
    tables = {'network_summary': {'columns': ['a', 'b', 'c', 'd'],
                                  'data': [['── 구조 ──', '', '', ''], ['Porosity ε_sphere (%)', '10.0', '10.0', '0%']]}}
    inj = getattr(A, 'inject_physics_v2_rows', None)
    if chk('V1 inject_physics_v2_rows 가 있다', callable(inj)):
        inj(tables, {'coverage_AM_mean_physics_v2': 41.0, 'coverage_AM_P_mean_physics_v2': 38.0,
                     'coverage_status_physics_v2': 'ok'})
        labels = [r[0] for r in tables['network_summary']['data']]
        chk('V2 v2 행에 "후보 · 미검증" 표지', any('physics v2' in l and '후보 · 미검증' in l for l in labels), repr(labels))
        t2 = {'network_summary': {'columns': ['a'], 'data': [['Porosity ε_sphere (%)']]}}
        inj(t2, {'coverage_AM_mean_physics_v2': None})
        chk('V3 v2 값이 없으면 행을 만들지 않는다', len(t2['network_summary']['data']) == 1)
    import predictor_engine as P
    ok_fn = getattr(P, '_fm_auto_target_ok', None)
    if chk('V4 예측기 자동 타깃 판정 함수가 있다', callable(ok_fn)):
        chk('V5 *_physics_v2 는 자동 타깃이 아니다', not ok_fn('coverage_AM_mean_physics_v2', 41.0)
            and not ok_fn('h_film_sim_physics_v2', 1e-5))
        chk('V6 legacy physics · 정확 union 은 그대로 후보', ok_fn('coverage_AM_mean_physics', 41.0)
            and ok_fn('porosity_union_exact_pct', 12.0))
    import grade_engine as GE
    v2 = [a.get('label') for a in GE.AXES if str(a.get('key', '')).endswith('_physics_v2')
          or str(a.get('fallback_key', '')).endswith('_physics_v2')]
    chk('V7 등급 축에 physics v2 없음', not v2, repr(v2))


def main():
    for fn in (section_x, section_a, section_w, section_v):
        try:
            fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            _fail.append(f'{fn.__name__} 예외 {type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        sys.exit(1)


if __name__ == '__main__':
    main()
