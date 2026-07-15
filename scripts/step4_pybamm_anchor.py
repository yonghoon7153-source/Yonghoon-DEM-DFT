#!/usr/bin/env python3
"""STEP4-v2 pybamm 앵커 (frame[4] — 독립 균질 참조와 대조, cross-fit 금지).

두 모드 (pybamm 설치 환경에서 실행 — V100/WSL; cloud 컨테이너엔 없음):

1) --export-params OUTDIR
   pybamm 내장 Chen2020(NMC811) 파라미터에서 §F1-깨끗한 앵커 파일 생성:
     · ocp_nmc811_chen2020.csv  — U_ocp(x) 테이블 (x = 양극 stoichiometry)
     · params_nmc811_chen2020.json — c_max, stoich 창(x0=충전끝/x100=방전끝), provenance
   → step4_dyn.py --ocp-csv/--params-json 입력.  (수치를 우리가 손으로 적지 않고
   pybamm 배포본에서 기계적으로 추출 = 날조 0, provenance 명시.)

2) --compare OUT.npz --sigma-e-S-cm .. --sigma-ion-S-cm .. --eps .. --thickness-um ..
   [--r-um 3.0 --d-s 3e-14 --i0 2.0 --c-rate ..]
   균질 half-cell DFN 트윈: 우리 STEP3 유효값(σ_e_eff/σ_ion_eff/ε/두께)과 동일
   OCP/D_s/i0/대표입경을 pybamm DFN(working electrode = positive)에 넣고 V(t) 대조.
   프로토콜(설계 §4): 균일-구조 극한에서 voxel-v2 ≈ pybamm 수 % = 솔버 검증;
   실제 침대와의 편차 = 미세구조 효과의 정량 (부가가치).
   ⚠ 매칭 규약: Bruggeman 지수 0 (유효값 직접 주입), t⁺=1·D_e 大 (SSB 단일이온 —
   농도분극 무력화), 분리막 얇게(1µm)+고전도, Li-금속 교환전류 大 (anode 분극 제거).
   compare는 EXPERIMENTAL — 첫 스모크에서 파라미터 이름/버전 차이를 다듬을 것.
"""
import argparse
import json
import os

import numpy as np


def _eval_ocp(pv, key, sto):
    """pybamm 파라미터의 OCP 항목을 numpy로 평가 (함수/보간 양쪽 방어)."""
    import pybamm
    f = pv[key]
    try:
        out = f(sto)
        if hasattr(out, 'evaluate'):
            raise TypeError
        return np.asarray(out, float)
    except Exception:
        vals = []
        for s in np.atleast_1d(sto):
            expr = f(pybamm.Scalar(float(s)))
            vals.append(float(expr.evaluate() if hasattr(expr, 'evaluate') else expr))
        return np.asarray(vals, float)


def export_params(outdir):
    import pybamm
    pv = pybamm.ParameterValues('Chen2020')
    c_max = float(pv['Maximum concentration in positive electrode [mol.m-3]'])
    x = np.linspace(0.005, 0.995, 199)
    U = _eval_ocp(pv, 'Positive electrode OCP [V]', x)
    # stoich 창: pybamm 유틸(버전별 위치 방어) → 실패 시 initial-concentration 기반 폴백
    x0 = x100 = None
    how = ''
    try:
        from pybamm.models.full_battery_models.lithium_ion.electrode_soh import (
            get_min_max_stoichiometries)
        mm = get_min_max_stoichiometries(pv)                 # (x_0, x_100, y_100, y_0) 버전차 유의
        vals = [float(v) for v in np.ravel(mm)]
        ys = sorted(v for v in vals if 0 < v < 1)[-2:] if len(vals) >= 4 else vals
        x100_, x0_ = min(ys), max(ys)                        # 양극: 충전끝=저리튬(min), 방전끝=고리튬(max)
        x0, x100 = x100_, x0_                                # x0(우리 규약)=충전 시작=저리튬
        how = 'pybamm get_min_max_stoichiometries'
    except Exception as e:
        ci = float(pv['Initial concentration in positive electrode [mol.m-3]'])
        x0, x100 = ci / c_max, 0.9                           # 폴백: 초기(≈충전상태) + 보수적 상한
        how = f'FALLBACK initial-concentration ({type(e).__name__}) — compare 전 수동확인 요망'
    os.makedirs(outdir, exist_ok=True)
    csvp = os.path.join(outdir, 'ocp_nmc811_chen2020.csv')
    with open(csvp, 'w') as fh:
        fh.write('x_stoich,U_V\n')
        for xi, ui in zip(x, U):
            fh.write(f'{xi:.5f},{ui:.6f}\n')
    prov = {
        'c_max_mol_m3': c_max,
        'x_at_charged': float(x0), 'x_at_discharged': float(x100),
        'stoich_window_source': how,
        'provenance': f'pybamm {getattr(__import__("pybamm"), "__version__", "?")} '
                      'ParameterValues("Chen2020") — Chen et al. 2020 (LG M50, NMC811) '
                      'positive electrode OCP + c_max; §F1: 기계 추출(수기 수치 0)',
    }
    jp = os.path.join(outdir, 'params_nmc811_chen2020.json')
    json.dump(prov, open(jp, 'w'), indent=1, ensure_ascii=False)
    print(f'exported:\n  {csvp}  (n={len(x)}, U {U.min():.3f}–{U.max():.3f} V)\n  {jp}')
    print(json.dumps(prov, indent=1, ensure_ascii=False))


def compare(a):
    import pybamm
    d = np.load(a.compare, allow_pickle=False)
    meta = json.loads(str(d['params_json']))
    pv = pybamm.ParameterValues('Chen2020')
    c_max = meta['c_max']
    i0_ref = float(meta['i0'])

    def j0(c_e, c_s_surf, c_s_max, T):
        x = c_s_surf / c_s_max
        return i0_ref * pybamm.sqrt(pybamm.maximum(4 * x * (1 - x), 1e-4))

    L = a.thickness_um * 1e-6
    upd = {
        'Positive electrode thickness [m]': L,
        'Positive electrode porosity': a.eps,
        'Positive electrode active material volume fraction': a.am_frac,
        'Positive particle radius [m]': a.r_um * 1e-6,
        'Positive particle diffusivity [m2.s-1]': float(meta['d_s']),
        'Positive electrode conductivity [S.m-1]': a.sigma_e_s_cm * 100.0,
        'Positive electrode Bruggeman coefficient (electrode)': 0.0,
        'Positive electrode Bruggeman coefficient (electrolyte)': 0.0,
        'Separator Bruggeman coefficient (electrolyte)': 0.0,
        'Separator porosity': 1.0,
        'Separator thickness [m]': 1e-6,
        'Electrolyte conductivity [S.m-1]': a.sigma_ion_s_cm * 100.0,
        'Electrolyte diffusivity [m2.s-1]': 1e-8,            # 농도분극 무력화 (t⁺=1 SSB)
        'Cation transference number': 0.9999,
        'Positive electrode exchange-current density [A.m-2]': j0,
        'Maximum concentration in positive electrode [mol.m-3]': c_max,
        'Initial concentration in positive electrode [mol.m-3]': meta['x0'] * c_max,
        'Nominal cell capacity [A.h]': 1.0,
    }
    for k, v in upd.items():
        try:
            pv.update({k: v}, check_already_exists=False)
        except Exception as e:
            print(f'  ⚠ param {k}: {type(e).__name__} {e}')
    model = pybamm.lithium_ion.DFN(options={'working electrode': 'positive'})
    # C-rate → 면적전류: 우리 npz의 I_1C를 그대로 쓰지 않고 pybamm 자체 용량 정의와 정합시키기
    # 위해 전류밀도[A/m²]로 직접 구동: i = C·F·c_max·Δx·(1−ε)·am_frac·L/3600
    i_area = (meta['c_rate'] * 96485.33212 * c_max * abs(meta['x100'] - meta['x0'])
              * a.am_frac * L / 3600.0)
    pv.update({'Current function [A]': i_area * a.area_cm2 * 1e-4}, check_already_exists=False)
    pv.update({'Electrode width [m]': np.sqrt(a.area_cm2) * 1e-2,
               'Electrode height [m]': np.sqrt(a.area_cm2) * 1e-2}, check_already_exists=False)
    sim = pybamm.Simulation(model, parameter_values=pv)
    sol = sim.solve([0, 3600.0 / max(meta['c_rate'], 1e-3) * 1.2])
    t_pb = sol['Time [s]'].entries
    V_pb = sol['Voltage [V]'].entries
    t_us, V_us = d['t'], d['V']
    Vi = np.interp(t_us, t_pb, V_pb)
    rms = float(np.sqrt(np.mean((Vi - V_us) ** 2)))
    print(f'pybamm twin: steps {len(t_pb)}, V {V_pb[0]:.3f}→{V_pb[-1]:.3f}')
    print(f'voxel-v2   : steps {len(t_us)}, V {V_us[0]:.3f}→{V_us[-1]:.3f}')
    print(f'ΔV RMS (공통 t-구간 보간): {rms * 1e3:.1f} mV')
    np.savez_compressed(a.out, t_pb=t_pb, V_pb=V_pb, t_us=t_us, V_us=V_us, rms_V=rms)
    print(f'saved {a.out}')


def main():
    ap = argparse.ArgumentParser(description='STEP4-v2 pybamm anchor (export/compare)')
    ap.add_argument('--export-params', metavar='OUTDIR')
    ap.add_argument('--compare', metavar='STEP4_OUT_NPZ')
    ap.add_argument('--sigma-e-S-cm', type=float, dest='sigma_e_s_cm')
    ap.add_argument('--sigma-ion-S-cm', type=float, dest='sigma_ion_s_cm')
    ap.add_argument('--eps', type=float, help='porosity (0-1)')
    ap.add_argument('--am-frac', type=float, default=0.5, help='AM 부피분율 (전극 기준)')
    ap.add_argument('--thickness-um', type=float)
    ap.add_argument('--r-um', type=float, default=3.0, help='대표 입경 반경 µm')
    ap.add_argument('--area-cm2', type=float, default=1.0)
    ap.add_argument('--out', default='step4_pybamm_compare.npz')
    a = ap.parse_args()
    if a.export_params:
        export_params(a.export_params)
    elif a.compare:
        need = [a.sigma_e_s_cm, a.sigma_ion_s_cm, a.eps, a.thickness_um]
        if any(v is None for v in need):
            ap.error('--compare needs --sigma-e-S-cm --sigma-ion-S-cm --eps --thickness-um')
        compare(a)
    else:
        ap.error('choose --export-params or --compare')


if __name__ == '__main__':
    main()
