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
    """metrics dict → 설계 knob dict (없는 값은 미포함 → assemble_features 가 nan).  §F1: 날조 없음."""
    inp = m.get('input', m.get('params', {})) or {}
    g = lambda *ks: next((inp.get(k) for k in ks if inp.get(k) is not None), None)
    d = {}
    for key, src in (('am_pct', ('am_pct', 'am_wt_pct')), ('ps_frac', ('ps_frac', 'ps_ratio')),
                     ('d_am_p_um', ('d_am_p', 'r_am_p')), ('d_am_s_um', ('d_am_s', 'r_am_s')),
                     ('d_se_um', ('d_se', 'r_se')), ('loading_mAh', ('loading', 'loading_mAh')),
                     ('press_MPa', ('press_MPa', 'pressure')), ('temp_K', ('temp_K', 'temperature')),
                     ('vgcf_wt', ('vgcf_wt',)), ('superp_wt', ('superp_wt',)),
                     ('sdcp_wt', ('sdcp_wt',)), ('ptfe_wt', ('ptfe_wt',))):
        v = g(*src)
        if v is not None:
            try:
                d[key] = float(v)
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


def load_corpus_from_results(results_folder):
    """results/<case>/{mpm_metrics.json|full_metrics.json} 전부 → cases list.  없는 폴더 스킵."""
    cases = []
    if not os.path.isdir(results_folder):
        return cases
    for case in sorted(os.listdir(results_folder)):
        cd = os.path.join(results_folder, case)
        if not os.path.isdir(cd):
            continue
        for mf in ('mpm_metrics.json', 'full_metrics.json'):
            mp = os.path.join(cd, mf)
            if os.path.exists(mp):
                try:
                    cases.append(json.loads(open(mp).read()))
                except Exception:
                    pass
                break
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
           'note': 'GPR+RF per-target(누출가드).  물리타깃=설계knob·파생타깃=물리feature.'}
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
    # mock corpus: 30 케이스 metrics (설계 + step3 σ + 일부 R_int)
    cases = []
    for i in range(30):
        am = 70 + 20 * rng.rand()
        cases.append({'input': {'am_pct': am, 'ps_frac': rng.rand(), 'd_se': 1 + 2 * rng.rand(),
                                'loading': 2 + 6 * rng.rand()},
                      'porosity_mpm_pct': 6 + 6 * rng.rand(), 'cycle_N': int(rng.randint(0, 100)),
                      'step3': {'sigma_e_eff_S_cm': 1 + 3 * rng.rand(),
                                'sigma_ion_eff_S_cm': 1e-4 + 2e-4 * rng.rand(),
                                'field_scale_e': {'focus_top': 50 + 50 * rng.rand()},
                                'field_scale_ion': {'focus_top': 20 + 30 * rng.rand()}},
                      **({'R_int_ohm_cm2': 40 + 30 * rng.rand()} if i % 2 == 0 else {})})
    # 1) 설계·타깃 추출
    d = design_from_metrics(cases[0])
    if 'am_pct' not in d or 'ps_frac' not in d:
        fails.append(f'design 추출 실패: {list(d)}')
    tg = targets_from_metrics(cases[0])
    if 'sigma_e_eff' not in tg or 'porosity' not in tg:
        fails.append(f'target 추출 실패: {list(tg)}')
    # 2) 행렬 빌드: X 모양, Y 키, 결측 nan(§F1)
    X, Y, names = build_matrix(cases)
    if X.shape != (30, len(DESIGN_KNOBS) + len(PHYS_FEATURES) + 1):
        fails.append(f'X 모양 {X.shape}')
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
