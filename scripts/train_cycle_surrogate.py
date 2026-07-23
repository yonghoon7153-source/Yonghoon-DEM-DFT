#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3-2 WSL 학습 파이프라인 — corpus → CycleSurrogate(GPR+RF) 학습·저장.

사용자 비전: "방대한 데이터로 ML 관계성".  ml_cycle_surrogate 의 CycleSurrogate 를 **실제 corpus**로
학습 = MLIP식 파이프라인 surrogate.  ★클라우드는 sklearn 부재 → 이 스크립트는 **WSL 실행용**:
  pip install scikit-learn joblib
  python scripts/train_cycle_surrogate.py --results webapp/results --out models/cycle_surrogate
클라우드에선 feature 조립·행렬빌드·리포트 로직만 mock corpus 로 검증(selftest); fit/save 는 import-guard.

frame[5]: 입력 = 물리-유도 feature(σ-triad·τ·coverage·CN·percolation·focus) → 남이 못 가진 "why".
§F1: 결측 nan(날조금지) · 타깃 provenance(model vs PENDING-exp) 는 ml_cycle_surrogate.TARGETS 준수.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ml_cycle_surrogate import (CycleSurrogate, DESIGN_KNOBS, PHYS_FEATURES, CYCLE_DIM, TARGETS,
                                 assemble_features)


# ── 케이스 metrics → 설계 knob + 타깃 ──────────────────────────────────────
def design_from_metrics(m):
    """merged metrics(+_ip=input_params) → 설계 knob dict.  ★리뷰 HIGH 수정: 설계는 input_params.json
    에 있고(별 파일) 키가 r_SE/r_AM_P/r_AM_S(sim-unit→µm ×2/scale)·am_se_ratio/ps_ratio(비율문자열)
    라 predictor_engine.py:165-192 규약을 따라 읽는다.  §F1: 못 읽으면 미포함(→nan), phi 폴백."""
    ip = m.get('_ip', {}) or {}
    scale = float(ip.get('scale', 1000) or 1000)
    d = {}
    for knob, rkey in (('d_se_um', 'r_SE'), ('d_am_p_um', 'r_AM_P'), ('d_am_s_um', 'r_AM_S')):
        r = ip.get(rkey, 0)
        if r and scale > 0:
            v = float(r) / scale * 1e6 * 2                    # 반지름(sim) → 지름(µm)
            if v > 0:
                d[knob] = v
    am = str(ip.get('am_se_ratio', ''))                       # '80:20' → am_pct 80
    if ':' in am:
        try:
            d['am_pct'] = float(am.split(':')[0])
        except ValueError:
            pass
    if 'am_pct' not in d:                                     # 폴백: phi_am/phi_se (predictor_engine 미러)
        pa, psx = m.get('phi_am', 0), m.get('phi_se', 0)
        if pa and psx and (pa + psx) > 0:
            d['am_pct'] = 100.0 * pa / (pa + psx)
    ps = str(m.get('ps_ratio', ip.get('ps_ratio', '')))      # '7:3' → ps_frac 0.7
    if ':' in ps:
        try:
            _p, _s = ps.split(':')[:2]
            _p, _s = float(_p), float(_s)
            if _p + _s > 0:
                d['ps_frac'] = _p / (_p + _s)
        except ValueError:
            pass
    for knob, keys in (('loading_mAh', ('loading', 'loading_mAh')), ('press_MPa', ('press_MPa', 'pressure')),
                       ('temp_K', ('temp_K', 'temperature')), ('vgcf_wt', ('vgcf_wt',)),
                       ('superp_wt', ('superp_wt',)), ('sdcp_wt', ('sdcp_wt',)), ('ptfe_wt', ('ptfe_wt',))):
        v = next((ip.get(k) for k in keys if ip.get(k) is not None), None)
        if v is not None:
            try:
                d[knob] = float(v)
            except (TypeError, ValueError):
                pass
    return d


def targets_from_metrics(m):
    """metrics dict → 타깃 dict (있는 것만; 없으면 미포함=학습서 마스크).  σ-triad 는 STEP3 상시,
    R_int/retention 은 사이클런 있을 때만."""
    s3 = m.get('step3', m) or {}
    out = {}
    for t, keys, src in (('sigma_e_eff', ('sigma_e_eff_S_cm',), s3),
                         ('sigma_ion_eff', ('sigma_ion_eff_S_cm',), s3),
                         ('porosity', ('porosity_mpm_pct', 'porosity_settled_pct', 'porosity'), m),
                         ('R_int_ohm_cm2', ('R_int_ohm_cm2', 'r_int_ohm_cm2'), m),
                         ('retention_pct', ('retention_pct',), m),
                         ('polarization_mV', ('polarization_mV', 'eta_total_mV'), m)):
        v = next((src.get(k) for k in keys if src.get(k) is not None), None)
        if v is not None:
            try:
                out[t] = float(v)
            except (TypeError, ValueError):
                pass
    return out


def build_matrix(cases):
    """cases = [metrics_dict, …] → (X[n,d], Y{target:[n]}, feat_names).  cycle_N 은 metrics 에 있으면
    사용, 없으면 0(pristine).  §F1: 결측 nan."""
    feat_names = DESIGN_KNOBS + PHYS_FEATURES + CYCLE_DIM
    X, Yrows = [], []
    for m in cases:
        N = float(m.get('cycle_N', 0) or 0)
        f, names = assemble_features(m, cycle_N=N, design=design_from_metrics(m))
        X.append(f); Yrows.append(targets_from_metrics(m))
    X = np.array(X, float)
    Y = {t: np.array([r.get(t, np.nan) for r in Yrows], float) for t in TARGETS}
    return X, Y, feat_names


def load_corpus_from_results(results_folder, gate=True):
    """results/<case>/{full_metrics.json + mpm_metrics.json + input_params.json} **병합** → cases.
    ★리뷰 HIGH/MED: DEM feature(full)·MPM/STEP3 feature(mpm)·설계(input_params)는 서로 다른 파일 →
    한 파일만 로드하면 절반이 결측.  3 병합.  + sentinel gating(σ=0 미해·porosity 과압축 제외;
    predictor_engine 미러) — 물리없는 0을 실측처럼 학습 방지(§F1)."""
    cases = []
    if not os.path.isdir(results_folder):
        return cases

    def _rd(p):
        try:
            with open(p) as f:
                return json.loads(f.read())
        except Exception:
            return None
    for case in sorted(os.listdir(results_folder)):
        cd = os.path.join(results_folder, case)
        if not os.path.isdir(cd):
            continue
        merged = {}
        for f in ('full_metrics.json', 'mpm_metrics.json'):   # full(DEM망) 먼저, mpm(STEP3) 오버레이
            d = _rd(os.path.join(cd, f))
            if d:
                merged.update(d)
        ip = _rd(os.path.join(cd, 'input_params.json'))
        if ip:
            merged['_ip'] = ip
        if not merged:
            continue
        if gate:                                              # sentinel 제외
            s3 = merged.get('step3', {}) or {}
            sig_e, sig_i = s3.get('sigma_e_eff_S_cm'), s3.get('sigma_ion_eff_S_cm')
            por = merged.get('porosity_mpm_pct') or merged.get('porosity')
            if (sig_e is not None and sig_e <= 0) or (sig_i is not None and sig_i <= 0):
                continue                                      # 네트워크 미해/비퍼콜 σ=0
            if por is not None and (por <= 0 or por > 40):
                continue                                      # 과압축(por≤0)·비물리 sentinel
        cases.append(merged)
    return cases


def train_and_save(X, Y, feat_names, out_dir):
    """CycleSurrogate.fit → joblib 저장 + 리포트 JSON.  sklearn/joblib 부재(클라우드) → graceful."""
    sur = CycleSurrogate()
    res = sur.fit(X, Y, feat_names=feat_names)
    if not res.get('ready'):
        return {'status': res.get('status'), 'saved': False,
                'hint': 'WSL 에서 pip install scikit-learn joblib 후 재실행'}
    try:
        import joblib
    except ImportError:
        return {'status': '학습 OK 이나 joblib 부재 → 저장 스킵', 'saved': False, 'targets': res['targets']}
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump({'surrogate': sur, 'feat_names': feat_names, 'targets': res['targets'],
                 'n_samples': int(X.shape[0])}, os.path.join(out_dir, 'cycle_surrogate.joblib'))
    # per-타깃 학습 표본 수 리포트 (CV R² 는 fit 내부 확장 여지 — 현재 표본수/provenance)
    rep = {'n_samples': int(X.shape[0]), 'n_features': int(X.shape[1]),
           'targets': {t: {'n': int(np.isfinite(Y[t]).sum()), 'provenance': TARGETS.get(t, '')}
                       for t in res['targets']},
           'note': 'GPR+RF per-target(누출가드: 물리타깃=설계knob·파생타깃=물리feature).  ⚠cycle_N 축은 '
                   'corpus 에 사이클런(cycle_N 있는 metrics)이 있어야 학습됨 — 없으면 uniform 0 → R_int(N)/'
                   'retention(N)은 ASSUMED-FORM(rint_growth/retention) 계수로만(surrogate 미학습).  fit 로그의 '
                   '⚠전-결측 경고 확인(설계 미결측 = input_params.json 있어야).'}
    json.dump(rep, open(os.path.join(out_dir, 'train_report.json'), 'w'), indent=2, ensure_ascii=False)
    return {'status': f"{len(res['targets'])} 타깃 학습·저장", 'saved': True,
            'out': out_dir, 'report': rep}


def run(results_folder, out_dir):
    cases = load_corpus_from_results(results_folder)
    if len(cases) < 5:
        return {'error': f'corpus 부족({len(cases)}<5) — {results_folder} 확인 (WSL 실 corpus 필요)'}
    X, Y, names = build_matrix(cases)
    return {'corpus': len(cases), **train_and_save(X, Y, names, out_dir)}


# ── self-test (mock corpus; 클라우드) ────────────────────────────────────
def _selftest():
    fails = []
    rng = np.random.RandomState(0)
    # mock corpus: 30 케이스 — ★실제 스키마(input_params 별파일 + step3 중첩 + DEM top-level) 재현
    #   (리뷰 HIGH 회귀: 옛 selftest 는 코드에 맞춘 {'input':…} mock 이라 스키마 불일치를 못 잡았음).
    cases = []
    for i in range(30):
        am = 70 + int(20 * rng.rand())
        p = 3 + int(5 * rng.rand())
        cases.append({
            # r_* = LIGGGHTS box 단위(scale=1000): d_µm = r/scale·1e6·2 = r·2000 → r~5e-4..3e-3
            '_ip': {'scale': 1000, 'r_SE': 5e-4 + 5e-4 * rng.rand(), 'r_AM_P': 2e-3 + 2e-3 * rng.rand(),
                    'r_AM_S': 8e-4 + 8e-4 * rng.rand(), 'am_se_ratio': f'{am}:{100 - am}',
                    'loading': 2 + 6 * rng.rand(), 'vgcf_wt': rng.rand()},
            'ps_ratio': f'{p}:{10 - p}', 'phi_am': 0.5, 'phi_se': 0.15,
            'porosity_mpm_pct': 6 + 6 * rng.rand(), 'cycle_N': int(rng.randint(0, 100)),
            'am_am_cn': 3 + rng.rand(), 'se_se_cn': 4 + rng.rand(), 'f_perc_recommended': 0.5 + 0.4 * rng.rand(),
            'am_se_cn': 5 + rng.rand(), 'area_AM_SE_total_physics': 100 + 50 * rng.rand(),
            'fracture_index': 0.1 * rng.rand(), 'coverage_AM_P_hertz_pct': 40 + 20 * rng.rand(),
            'coverage_AM_P_tabor_pct': 50 + 20 * rng.rand(),
            'step3': {'sigma_e_eff_S_cm': 1 + 3 * rng.rand(), 'sigma_ion_eff_S_cm': 1e-4 + 2e-4 * rng.rand(),
                      'thermal': {'k_eff_W_mK': 1 + rng.rand()}, 'pore': {'tau': 1.5 + rng.rand()},
                      'field_scale_e': {'focus_top': 50 + 50 * rng.rand()},
                      'field_scale_ion': {'focus_top': 20 + 30 * rng.rand()}},
            **({'R_int_ohm_cm2': 40 + 30 * rng.rand()} if i % 2 == 0 else {})})
    # 1) 설계·타깃 추출 — ★설계가 input_params(별파일)서 읽혀 유한이어야 (HIGH 회귀)
    d = design_from_metrics(cases[0])
    for k in ('am_pct', 'ps_frac', 'd_se_um', 'loading_mAh'):
        if k not in d or not np.isfinite(d[k]):
            fails.append(f'design 추출 실패({k}): {d}')
    if not (0.8 < d.get('d_se_um', 0) < 2.2):                 # r_SE 5e-4..1e-3 → d 1-2µm (단위변환 검증)
        fails.append(f"d_se_um 단위변환 오류: {d.get('d_se_um')}")
    tg = targets_from_metrics(cases[0])
    if 'sigma_e_eff' not in tg or 'porosity' not in tg:
        fails.append(f'target 추출 실패: {list(tg)}')
    # 2) 행렬: X 모양, 설계+물리 feature 유한(퇴화 방지), 결측 nan(§F1)
    X, Y, names = build_matrix(cases)
    if X.shape != (30, len(DESIGN_KNOBS) + len(PHYS_FEATURES) + 1):
        fails.append(f'X 모양 {X.shape}')
    _fin = np.isfinite(X).all(axis=0)                        # 전-케이스 유한한 열
    for key in ('am_pct', 'ps_frac', 'sigma_e_eff', 'sigma_thermal', 'tau_se', 'cn_am_am', 'f_perc'):
        if not _fin[names.index(key)]:
            fails.append(f'feature 전-결측(스키마 미스): {key}')
    if not (np.isfinite(Y['sigma_e_eff']).sum() == 30 and np.isfinite(Y['R_int_ohm_cm2']).sum() == 15):
        fails.append(f"Y 마스크 오류 σ_e={np.isfinite(Y['sigma_e_eff']).sum()} "
                     f"R_int={np.isfinite(Y['R_int_ohm_cm2']).sum()}")
    if not np.isnan(Y['retention_pct']).all():                # 없는 타깃 = 전부 nan (날조 없음)
        fails.append('없는 타깃이 nan 아님(§F1)')
    # 3) train_and_save: sklearn 부재면 graceful(saved False + hint), 있으면 저장
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = train_and_save(X, Y, names, td)
        if 'saved' not in r:
            fails.append('train_and_save 반환 규약 위반')
        if r.get('saved'):
            if not os.path.exists(os.path.join(td, 'cycle_surrogate.joblib')):
                fails.append('joblib 저장 안 됨')
            print(f'  [WSL] 학습·저장 OK: {r["status"]}')
        else:
            print(f'  [cloud] sklearn/joblib 부재 → graceful ✓ ({r["status"][:44]}…)')
    print('selftest OK' if not fails else 'selftest FAIL:\n  ' + '\n  '.join(fails))
    if not fails:
        print(f"  corpus 30 → X{X.shape} · 타깃 표본: σ_e {int(np.isfinite(Y['sigma_e_eff']).sum())} · "
              f"R_int {int(np.isfinite(Y['R_int_ohm_cm2']).sum())} · retention {int(np.isfinite(Y['retention_pct']).sum())}(미배선)")
    return 1 if fails else 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description='v3-2 WSL 학습: corpus → CycleSurrogate 저장')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--results', default='webapp/results', help='corpus 루트 (results/<case>/*metrics.json)')
    ap.add_argument('--out', default='models/cycle_surrogate', help='모델 저장 폴더')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    r = run(a.results, a.out)
    print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
    return 0 if not r.get('error') else 1


if __name__ == '__main__':
    raise SystemExit(main() if len(sys.argv) > 1 else _selftest())
