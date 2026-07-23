#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3-3 — 오픈소스 cycling 데이터 인제스트 + §F1 provenance 게이트.

사용자 비전: "오픈소스로 cycling 데이터 엄청 많으니 참고해서 넣는다."  ★핵심 정직(§F1): 공개
cycling 데이터는 대부분 **liquid-cell Li-ion**(Severson/NASA/Stanford…)이지 sulfide ASSB 가 아님 —
열화 기전이 다름(sulfide=접촉손실/화학-역학, liquid=SEI/용해).  그래서:
  · **FORM/METHOD** (fade 곡선 모양·R_int 성장 법칙·DRT 분해 방법) = 전이 가능 (화학-무관 방법론).
  · **ABSOLUTE 크기** (사이클당 fade %·R_int Ω·cm²) = **matching chemistry(sulfide-ASSB)에만**.
liquid-cell 로 학습해 "sulfide 다"라고 하면 §F1 위반 → 이 모듈이 chemistry 태그로 **게이트**한다.

역할: (1) 공개 cycling CSV → 정본 스키마, (2) chemistry provenance 태그 + transferable 게이트,
(3) fade/R_int FORM 계수 적합(ml_cycle_surrogate 모델) — liquid 는 form-only 라벨, (4) 알려진 데이터셋
레지스트리(provenance 포함).  실제 데이터 다운로드는 WSL/사용자측(대용량); 여기선 프레임워크+검증.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from ml_cycle_surrogate import retention as _retention_model, rint_growth as _rint_model
except ImportError:                                            # 독립 실행 폴백
    def _retention_model(N, q_lin=0.0, q_sqrt=0.0, q_knee=0.0, n_knee=1e9):
        N = np.asarray(N, float)
        return np.clip(100.0 * (1 - q_lin * N - q_sqrt * np.sqrt(np.maximum(N, 0)) -
                                q_knee * np.maximum(0, N - n_knee)), 0, 100)

    def _rint_model(N, R0, a_sat, tau_N, b_sqrt=0.0):
        N = np.asarray(N, float)
        return R0 * (1 + a_sat * (1 - np.exp(-N / max(tau_N, 1e-9))) + b_sqrt * np.sqrt(np.maximum(N, 0)))


# ── 정본 스키마 ──────────────────────────────────────────────────────────
SCHEMA = ['cycle_N', 'discharge_capacity', 'coulombic_eff', 'R_int_ohm_cm2']   # R_int 선택
CHEMISTRIES = {                                                # provenance: 우리 sulfide-ASSB 와의 관계
    'sulfide_assb': {'transfer_absolute': True, 'note': '우리 화학 — 절대크기 앵커 가능'},
    'oxide_assb': {'transfer_absolute': False, 'note': 'ASSB 이나 산화물 SE — 기전 유사(접촉/화학) form 유용, 절대 별개'},
    'liquid_nmc': {'transfer_absolute': False, 'note': 'liquid Li-ion NMC — SEI/용해 기전 → FORM/METHOD 만'},
    'liquid_lfp': {'transfer_absolute': False, 'note': 'liquid LFP(Severson) — 대용량 통계·METHOD 만'},
    'unknown': {'transfer_absolute': False, 'note': '미상 → form-only(보수)'},
}


def provenance_gate(chemistry):
    """chemistry → transferable 게이트.  form/method 는 항상 True(방법론), absolute 는 sulfide 만."""
    c = CHEMISTRIES.get(chemistry, CHEMISTRIES['unknown'])
    return {'chemistry': chemistry, 'transfer_form': True, 'transfer_method': True,
            'transfer_absolute': bool(c['transfer_absolute']), 'note': c['note'],
            'F1_label': ('ABSOLUTE-OK (matching chemistry)' if c['transfer_absolute']
                         else 'FORM/METHOD-ONLY (다른 화학 — 절대크기 전이 금지, §F1)')}


def ingest_csv(path, col_map=None, chemistry='unknown', source='', cap_nominal=None):
    """cycling CSV → 정본 dict.  col_map: {정본키: CSV열명}.  없으면 헤더 자동추정.
    retention(%)=capacity/nominal·100 (nominal 없으면 1사이클 기준).  provenance 동봉."""
    import csv as _csv
    rows = list(_csv.DictReader(open(path, newline='')))
    if not rows:
        return {'error': f'빈 CSV: {path}'}
    hdr = rows[0].keys()
    cm = col_map or {}
    # 자동 추정 (없는 키만)
    def _guess(cands):
        for h in hdr:
            if any(k in h.lower() for k in cands):
                return h
        return None
    cm.setdefault('cycle_N', _guess(['cycle', 'cyc', 'n']))
    cm.setdefault('discharge_capacity', _guess(['discharge', 'q_dis', 'capacity', 'cap']))
    cm.setdefault('coulombic_eff', _guess(['coulombic', 'ce', 'efficien']))
    cm.setdefault('R_int_ohm_cm2', _guess(['r_int', 'resist', 'rint', 'ohm']))

    def _col(key):
        h = cm.get(key)
        if not h or h not in hdr:
            return None
        out = []
        for r in rows:
            try:
                out.append(float(r[h]))
            except (TypeError, ValueError):
                out.append(np.nan)
        return np.array(out, float)
    N = _col('cycle_N'); Q = _col('discharge_capacity')
    if N is None or Q is None:
        return {'error': f'cycle/capacity 열 못 찾음 (헤더: {list(hdr)}) — col_map 지정 필요'}
    nom = float(cap_nominal) if cap_nominal else (float(Q[np.isfinite(Q)][0]) if np.isfinite(Q).any() else 1.0)
    ret = 100.0 * Q / max(nom, 1e-12)
    return {'source': source, 'n_cycles': int(np.nanmax(N)) if np.isfinite(N).any() else 0,
            'cycle_N': N, 'discharge_capacity': Q, 'retention_pct': ret,
            'coulombic_eff': _col('coulombic_eff'), 'R_int_ohm_cm2': _col('R_int_ohm_cm2'),
            'cap_nominal': nom, 'provenance': provenance_gate(chemistry)}


# ── FORM 적합 (계수 = 오픈소스서 학습; 게이트로 라벨) ───────────────────────
def fit_fade_form(N, retention, chemistry='unknown', with_knee=False):
    """(N, retention%) → retention 성장모델 계수(q_lin,q_sqrt[,q_knee,n_knee]).
    ★게이트: 절대 전이 불가 화학이면 'form_only'=True (계수 모양만 채택, 절대 fade율은 sulfide 실험)."""
    from scipy.optimize import curve_fit
    N = np.asarray(N, float); r = np.asarray(retention, float)
    m = np.isfinite(N) & np.isfinite(r)
    if m.sum() < 4:
        return {'error': 'fade 적합 점 부족(<4)'}
    N, r = N[m], r[m]
    try:
        if with_knee:
            p0 = [1e-3, 1e-3, 1e-3, 0.5 * N.max()]
            f = lambda n, ql, qs, qk, nk: _retention_model(n, ql, qs, qk, nk)
            popt, _ = curve_fit(f, N, r, p0=p0, maxfev=20000,
                                bounds=([0, 0, 0, 0], [1, 1, 1, N.max()]))
            keys = ['q_lin', 'q_sqrt', 'q_knee', 'n_knee']
        else:
            f = lambda n, ql, qs: _retention_model(n, ql, qs)
            popt, _ = curve_fit(f, N, r, p0=[1e-3, 1e-3], maxfev=20000, bounds=([0, 0], [1, 1]))
            keys = ['q_lin', 'q_sqrt']
    except Exception as e:
        return {'error': f'curve_fit 실패: {type(e).__name__}'}
    pred = _retention_model(N, *popt)
    r2 = 1 - np.sum((r - pred) ** 2) / max(np.sum((r - r.mean()) ** 2), 1e-12)
    g = provenance_gate(chemistry)
    return {'coeffs': dict(zip(keys, [float(x) for x in popt])), 'r2': float(r2),
            'form_only': not g['transfer_absolute'], 'provenance': g,
            'F1': ('FORM 채택 (모양만; 절대 fade율은 sulfide 실험 앵커)' if not g['transfer_absolute']
                   else 'ABSOLUTE 채택 가능 (sulfide-ASSB)')}


def fit_rint_form(N, rint, chemistry='unknown'):
    """(N, R_int) → rint_growth 계수(R0,a_sat,tau_N,b_sqrt).  게이트 동일."""
    from scipy.optimize import curve_fit
    N = np.asarray(N, float); R = np.asarray(rint, float)
    m = np.isfinite(N) & np.isfinite(R)
    if m.sum() < 4:
        return {'error': 'R_int 적합 점 부족(<4)'}
    N, R = N[m], R[m]
    try:
        p0 = [float(R[np.argmin(N)]), 0.5, max(0.3 * N.max(), 1.0), 1e-3]
        popt, _ = curve_fit(_rint_model, N, R, p0=p0, maxfev=20000,
                            bounds=([1e-6, 0, 1e-3, 0], [np.inf, 20, np.inf, 1]))
    except Exception as e:
        return {'error': f'curve_fit 실패: {type(e).__name__}'}
    pred = _rint_model(N, *popt)
    r2 = 1 - np.sum((R - pred) ** 2) / max(np.sum((R - R.mean()) ** 2), 1e-12)
    g = provenance_gate(chemistry)
    return {'coeffs': dict(zip(['R0', 'a_sat', 'tau_N', 'b_sqrt'], [float(x) for x in popt])),
            'r2': float(r2), 'form_only': not g['transfer_absolute'], 'provenance': g}


# ── 알려진 공개 데이터셋 레지스트리 (provenance 포함) ────────────────────────
DATASET_REGISTRY = [
    {'name': 'Severson-MIT-Toyota 2019', 'chemistry': 'liquid_lfp', 'n_cells': 124,
     'use': 'METHOD (early-cycle→life 예측 방법론), 대용량 통계 검증 — ★절대 fade는 LFP-liquid, sulfide 전이 금지',
     'url': 'data.matr.io (CC-BY)'},
    {'name': 'NASA Ames PCoE (Randle/Battery)', 'chemistry': 'liquid_nmc', 'n_cells': 34,
     'use': 'R_int(N) 성장 FORM (임피던스 사이클링) — 방법·모양, 절대는 NMC-liquid',
     'url': 'nasa.gov/PCoE'},
    {'name': 'Stanford-SLAC (Attia 2020 CLO)', 'chemistry': 'liquid_lfp', 'n_cells': 224,
     'use': 'closed-loop 최적화 METHOD (BO 사이클수명) = 우리 v3 설계루프 원형', 'url': 'data.matr.io'},
    {'name': 'Oxford Battery Degradation', 'chemistry': 'liquid_nmc', 'n_cells': 8,
     'use': 'degradation-mode(LLI/LAM) 분해 METHOD (ICA/dV) — dQ/dV 방법 앵커', 'url': 'ora.ox.ac.uk'},
    {'name': '★ sulfide-ASSB cycling (Kang&Shin·Conforto·Choi 등)', 'chemistry': 'sulfide_assb', 'n_cells': None,
     'use': '★유일한 ABSOLUTE 앵커 — R_int(N)·fade 절대크기.  희소 → WSL PDF digitize(#5)',
     'url': '문헌 (rint_eis_anchors.csv 참조)'},
]


def registry_summary():
    lines = ['공개 cycling 데이터셋 레지스트리 (provenance):']
    for d in DATASET_REGISTRY:
        g = provenance_gate(d['chemistry'])
        lines.append(f"  · {d['name']} [{d['chemistry']}] — {g['F1_label'][:22]} — {d['use'][:60]}")
    return '\n'.join(lines)


# ── self-test ───────────────────────────────────────────────────────────
def _selftest():
    import tempfile
    import csv as _csv
    fails = []
    # 1) provenance 게이트: sulfide=절대OK, liquid=form-only
    if not provenance_gate('sulfide_assb')['transfer_absolute']:
        fails.append('sulfide 절대전이 True 여야')
    if provenance_gate('liquid_lfp')['transfer_absolute']:
        fails.append('liquid 절대전이 False 여야 (§F1)')
    if provenance_gate('무엇')['transfer_absolute']:
        fails.append('미상은 보수적 False 여야')
    # 2) 합성 cycling CSV 인제스트 (자동 헤더 추정)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'cyc.csv')
        Ntrue = np.arange(1, 201)
        Qtrue = 3.0 * _retention_model(Ntrue, q_lin=5e-4, q_sqrt=3e-3) / 100.0     # fade 곡선
        with open(p, 'w', newline='') as f:
            w = _csv.writer(f); w.writerow(['cycle', 'discharge_capacity_mAh', 'CE'])
            for n, q in zip(Ntrue, Qtrue):
                w.writerow([n, q, 0.999])
        d = ingest_csv(p, chemistry='liquid_lfp', source='synthetic', cap_nominal=3.0)
        if 'error' in d:
            fails.append(f"인제스트 실패: {d['error']}")
        elif not (d['n_cycles'] == 200 and abs(d['retention_pct'][0] - 100) < 1):
            fails.append(f"인제스트 값 오류: n={d.get('n_cycles')} ret0={d['retention_pct'][0]:.1f}")
        elif d['provenance']['transfer_absolute']:
            fails.append('liquid 인제스트가 절대전이 허용 (§F1 위반)')
        # 3) fade FORM 적합 → 계수 회복 + form_only 라벨
        if 'error' not in d:
            fit = fit_fade_form(d['cycle_N'], d['retention_pct'], chemistry='liquid_lfp')
            if 'error' in fit:
                fails.append(f"fade 적합 실패: {fit['error']}")
            elif not (fit['r2'] > 0.98 and fit['form_only']):
                fails.append(f"fade 적합 r2={fit.get('r2'):.3f} form_only={fit.get('form_only')}")
        # 4) R_int FORM 적합 (sulfide=절대OK)
        Rt = _rint_model(Ntrue, 50.0, 0.8, 40.0, 0.02)
        rf = fit_rint_form(Ntrue, Rt, chemistry='sulfide_assb')
        if 'error' in rf or rf['r2'] < 0.98 or rf['form_only']:
            fails.append(f"R_int 적합: {rf.get('error', rf.get('r2'))} form_only={rf.get('form_only')}")
    print('selftest OK' if not fails else 'selftest FAIL:\n  ' + '\n  '.join(fails))
    if not fails:
        print(f"  게이트: sulfide=절대OK · liquid=form-only(§F1) · 미상=보수")
        print(f"  인제스트: 200사이클 자동추정 · fade 적합 r2>0.98 form-only 라벨")
        print(registry_summary())
    return 1 if fails else 0


def main(argv=None):
    import argparse
    import json
    ap = argparse.ArgumentParser(description='v3-3 오픈소스 cycling 인제스트 + §F1 게이트')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--csv', default='', help='cycling CSV 인제스트')
    ap.add_argument('--chemistry', default='unknown', choices=list(CHEMISTRIES))
    ap.add_argument('--cap-nominal', type=float, default=None)
    ap.add_argument('--registry', action='store_true', help='알려진 데이터셋 레지스트리 출력')
    a = ap.parse_args(argv)
    if a.selftest or (not a.csv and not a.registry):
        return _selftest()
    if a.registry:
        print(registry_summary()); return 0
    d = ingest_csv(a.csv, chemistry=a.chemistry, cap_nominal=a.cap_nominal)
    if 'error' in d:
        print(d['error']); return 1
    print(f"인제스트: {d['n_cycles']} 사이클 · {d['provenance']['F1_label']}")
    ff = fit_fade_form(d['cycle_N'], d['retention_pct'], chemistry=a.chemistry, with_knee=True)
    print('fade FORM:', json.dumps(ff.get('coeffs', ff), ensure_ascii=False), f"(r2={ff.get('r2', 0):.3f})")
    if d.get('R_int_ohm_cm2') is not None and np.isfinite(d['R_int_ohm_cm2']).sum() >= 4:
        rf = fit_rint_form(d['cycle_N'], d['R_int_ohm_cm2'], chemistry=a.chemistry)
        print('R_int FORM:', json.dumps(rf.get('coeffs', rf), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
