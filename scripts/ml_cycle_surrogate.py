#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3-2 — ML 사이클수명 + 파이프라인 surrogate (MLIP식 가속).

사용자 비전: 비싼 STEP4 충방전 + 사이클 sim 을 **물리-유도 feature** 로 예측 → GPU-시간 대신 초.
frame[5] payoff: 남들은 조성→성능 블랙박스.  우리는 조성 →(DEM/MPM/STEP3 가 계산한 σ·τ·percolation·
current-focus)→ 성능 = **"why" 가 있는 feature**.  그래서 남이 못 찾는 관계성을 찾음.

두 역할 (상보):
  (A) **surrogate** — 물리-feature → 타깃(R_int(N)·fade·σ-triad·EIS 소자) 빠른 예측 → 역설계·대규모 스윕.
      우리 파이프라인이 학습셋 생성+검증, surrogate 가 물량.  (파이프라인 정확도 상속 = MLIP 규약.)
  (B) **사이클수명** — R_int(N)·retention(N) 성장.  오픈소스 cycling 데이터로 **FORM/METHOD 앵커**
      (§F1: 절대크기는 sulfide-ASSB 앵커에만; liquid-cell 은 form/method 만 — 기전 다름).

★정직(§F1): 실제 GPR/RF 학습은 sklearn(WSL) — 클라우드 부재 → import-guard.  feature 조립·성장모델·
아키텍처는 pure numpy 로 여기서 완전 검증.  타깃 provenance(model vs experiment-anchored) 라벨 필수.
"""
from __future__ import annotations

import math

import numpy as np

# ── 3-층 feature 스키마 ──────────────────────────────────────────────────
DESIGN_KNOBS = ['am_pct', 'ps_frac', 'd_am_p_um', 'd_am_s_um', 'd_se_um', 'loading_mAh',
                'press_MPa', 'temp_K', 'vgcf_wt', 'superp_wt', 'sdcp_wt', 'ptfe_wt', 'coating_cei']
# ★ 차별점: DEM/MPM/STEP3 가 계산한 물리-유도 feature (남이 못 가진 "why" 축)
PHYS_FEATURES = ['porosity', 'sigma_e_eff', 'sigma_ion_eff', 'sigma_thermal', 'tau_se',
                 'coverage_AM_hertz', 'coverage_AM_tabor', 'cn_am_am', 'cn_se_se', 'f_perc',
                 'focus_e', 'focus_ion', 'holm_area_rel', 'fracture_index', 'contact_am_se']
CYCLE_DIM = ['cycle_N']
# 타깃 + provenance (model = 우리 파이프라인 산출 / exp = 실험 앵커 필요)
TARGETS = {
    'R_int_ohm_cm2': 'model+PENDING-exp (R_int(N): 접촉-기계 몫 model, 화학·절대 = sulfide exp 대기)',
    'retention_pct': 'PENDING-exp (현재 form-only: 오픈소스 FORM 만; sulfide 절대 fade 실험 미배선 §F1)',
    'sigma_e_eff': 'model (STEP3 Kirchhoff)', 'sigma_ion_eff': 'model (STEP3 Bazzoun-검증)',
    'R_ct_ohm_cm2': 'model (STEP4 BV) — ⚠i0 의존(미앵커, 스윕전용)', 'C_dl_uF_cm2': 'PENDING-exp (EIS CPE 앵커 대기)',
    'polarization_mV': 'model (STEP4)', 'porosity': 'model (DEM/MPM)',
}


# ── 사이클 열화 성장 모델 (ASSUMED-FORM; 계수는 학습/앵커) ───────────────────
def rint_growth(N, R0, a_sat, tau_N, b_sqrt=0.0):
    """R_int(N) = R0·[1 + a_sat·(1−exp(−N/τ_N)) + b_sqrt·√N].
    포화항(a_sat, τ_N: 초기 접촉손실·CEI 형성) + √N 항(b_sqrt: 확산-율속 지속성장).
    ★ASSUMED-FORM (Kang&Shin R_int(N) 관측형) — 계수는 우리 사이클런 + 실험 앵커로 학습.
    양끝 고정 규약(A11-②)과 정합: R(0)=R0."""
    N = np.asarray(N, float)
    return float(R0) * (1.0 + float(a_sat) * (1.0 - np.exp(-N / max(float(tau_N), 1e-9)))
                        + float(b_sqrt) * np.sqrt(np.maximum(N, 0.0)))


def retention(N, q_lin=0.0, q_sqrt=0.0, q_knee=0.0, n_knee=1e9):
    """용량유지율(%) = 100·[1 − q_lin·N − q_sqrt·√N − q_knee·max(0,N−n_knee)].
    선형(LLI 근사) + √N(SEI/확산) + knee(급락 개시).  ★shape = 오픈소스 cycling FORM 앵커,
    sulfide 절대율은 실험(§F1).  0..100 clip."""
    N = np.asarray(N, float)
    r = 100.0 * (1.0 - float(q_lin) * N - float(q_sqrt) * np.sqrt(np.maximum(N, 0.0))
                 - float(q_knee) * np.maximum(0.0, N - float(n_knee)))
    return np.clip(r, 0.0, 100.0)


def assemble_features(case, cycle_N=0, design=None):
    """케이스 metrics dict(+선택 design) → feature 벡터 + 이름 (pure numpy).
    없는 key 는 np.nan (surrogate 가 마스킹/impute) — 날조 0 (§F1: 결측을 0으로 채우지 않음)."""
    design = design or {}
    s3 = case.get('step3', case) if isinstance(case, dict) else {}
    fse = (s3.get('field_scale_e') or {}); fsi = (s3.get('field_scale_ion') or {})

    def g(*keys, src=case):
        for k in keys:
            v = (src or {}).get(k)
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    pass
        return np.nan
    feats, names = [], []
    for k in DESIGN_KNOBS:
        feats.append(float(design.get(k, np.nan))); names.append(k)
    phys = {
        'porosity': g('porosity_mpm_pct', 'porosity_settled_pct', 'porosity'),
        'sigma_e_eff': g('sigma_e_eff_S_cm', src=s3), 'sigma_ion_eff': g('sigma_ion_eff_S_cm', src=s3),
        'sigma_thermal': g('k_eff_W_mK', src=(s3.get('thermal') or {})),   # ★리뷰: step3['thermal'] 밑
        'tau_se': g('tau', src=(s3.get('pore') or {})),                    # step3['pore']['tau'] (존재 확인)
        'coverage_AM_hertz': g('coverage_AM_P_hertz_pct', 'coverage_AM_hertz_pct'),
        'coverage_AM_tabor': g('coverage_AM_P_tabor_pct', 'coverage_AM_tabor_pct'),
        'cn_am_am': g('am_am_cn', 'coordination_AM'), 'cn_se_se': g('se_se_cn'),
        'f_perc': g('f_perc_recommended', 'f_perc_x_AM'),
        'focus_e': float(fse.get('focus_top', np.nan)), 'focus_ion': float(fsi.get('focus_top', np.nan)),
        'holm_area_rel': g('area_AM_SE_total_physics', 'holm_area'),
        'fracture_index': g('fracture_index', 'fracture_index_force'),
        'contact_am_se': g('am_se_cn'),
    }
    for k in PHYS_FEATURES:
        feats.append(float(phys.get(k, np.nan))); names.append(k)
    feats.append(float(cycle_N)); names.append('cycle_N')
    return np.array(feats, float), names


# ── surrogate (sklearn = WSL; import-guard) ─────────────────────────────
class CycleSurrogate:
    """물리-feature(+cycle_N) → 타깃 surrogate.  GPR(불확실성) + RF(비선형) 앙상블(predictor_engine 규약).
    fit/predict 는 sklearn 필요(WSL).  구조·feature·성장모델은 클라우드 검증됨."""

    def __init__(self, targets=None):
        self.targets = targets or list(TARGETS)
        self.models = {}
        self.feat_names = None
        self._ready = False

    def _feat_idx_for_target(self, target, names):
        """★리뷰#5 leakage 가드 (2단 surrogate 설계→물리→타깃): 타깃이 물리-feature 면(σ_e 등)
        입력을 **설계 knob 만**으로(자기·타 물리 누출 차단; 파이프라인 1단=설계→물리 예측).  파생타깃
        (R_int·retention·R_ct 등)은 **자기 이름만 제외**한 물리+설계+cycle(2단=물리→성능)."""
        if target in PHYS_FEATURES:
            return [i for i, n in enumerate(names) if n in DESIGN_KNOBS]
        return [i for i, n in enumerate(names) if n != target]

    def fit(self, X, Y, feat_names=None):
        """X[n,d] 물리-feature, Y{target: y[n]}.  결측 impute + per-target 마스킹(누출가드) + 표준화 → GPR+RF."""
        try:
            from sklearn.gaussian_process import GaussianProcessRegressor
            from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            return {'status': 'sklearn 부재 (WSL 전용) — 학습 스킵.  pip install scikit-learn',
                    'ready': False}
        X = np.asarray(X, float)
        self.feat_names = feat_names or (DESIGN_KNOBS + PHYS_FEATURES + CYCLE_DIM)
        self._med = np.nanmedian(np.where(np.isfinite(X), X, np.nan), axis=0)
        self._med = np.where(np.isfinite(self._med), self._med, 0.0)
        Xi = np.where(np.isfinite(X), X, self._med)
        _allnan = ~np.isfinite(X).any(axis=0)                 # ★리뷰: 전-결측 feature 경고(median→0 무정보 숨김 방지)
        if _allnan.any():
            _bad = ([self.feat_names[i] for i in np.where(_allnan)[0]]
                    if self.feat_names else list(map(int, np.where(_allnan)[0])))
            print(f'  ⚠ 전-결측 feature {int(_allnan.sum())}개 → median=0 impute(무정보, 해당 타깃 퇴화 위험): {_bad[:10]}')
        for t in self.targets:
            if t not in Y:
                continue
            y = np.asarray(Y[t], float); m = np.isfinite(y)
            if m.sum() < 5:
                continue
            idx = self._feat_idx_for_target(t, self.feat_names)   # 누출가드: 타깃별 입력 feature 집합
            if not idx:
                continue
            scaler = StandardScaler().fit(Xi[m][:, idx])
            Xs = scaler.transform(Xi[m][:, idx])
            k = ConstantKernel(1.0) * RBF(length_scale=np.ones(len(idx))) + WhiteKernel(1e-3)
            gpr = GaussianProcessRegressor(kernel=k, n_restarts_optimizer=3, alpha=1e-6, normalize_y=True)
            rf = RandomForestRegressor(n_estimators=100, max_depth=6, min_samples_leaf=3, random_state=42)
            gpr.fit(Xs, y[m]); rf.fit(Xs, y[m])
            self.models[t] = (gpr, rf, scaler, idx)               # per-target: 모델+스케일러+feature idx
        self._ready = len(self.models) > 0
        return {'status': f'{len(self.models)} 타깃 학습 (per-target 누출가드)', 'ready': self._ready,
                'targets': list(self.models)}

    def predict(self, X):
        """X[n,d] → {target: (mean, std)}.  타깃별 feature 마스크 적용(누출가드) + GPR±std + RF."""
        if not self._ready:
            return {'error': 'not fitted (sklearn/WSL 학습 필요)'}
        Xi = np.where(np.isfinite(X), X, self._med)
        Xa = np.atleast_2d(Xi)
        out = {}
        for t, (gpr, rf, scaler, idx) in self.models.items():
            Xs = scaler.transform(Xa[:, idx])
            gm, gs = gpr.predict(Xs, return_std=True)
            rm = rf.predict(Xs)
            out[t] = {'mean': float(0.5 * (gm[0] + rm[0])), 'std': float(gs[0]),
                      'gpr': float(gm[0]), 'rf': float(rm[0]), 'provenance': TARGETS.get(t, '')}
        return out

    def predict_cycle_curve(self, X_base, n_max=100, n_pts=11):
        """설계(물리-feature) → R_int(N)·retention(N) 곡선.  cycle_N 축을 스윕해 surrogate 예측
        (또는 성장모델 계수를 surrogate 로 얻어 rint_growth/retention 평가).  체크포인트 N."""
        Ns = np.unique(np.round(np.linspace(0, n_max, n_pts))).astype(int)
        curve = {'N': Ns.tolist(), 'R_int': [], 'retention': []}
        ci = self.feat_names.index('cycle_N') if (self.feat_names and 'cycle_N' in self.feat_names) else -1
        for N in Ns:
            x = np.array(X_base, float).copy()
            if ci >= 0:
                x[ci] = N
            p = self.predict(x)
            curve['R_int'].append(p.get('R_int_ohm_cm2', {}).get('mean'))
            curve['retention'].append(p.get('retention_pct', {}).get('mean'))
        return curve


# ── self-test (mock; 클라우드) ───────────────────────────────────────────
def _selftest():
    fails = []
    # 1) 성장모델: R_int(N) 단조증가 + R(0)=R0
    N = np.arange(0, 101)
    R = rint_growth(N, R0=50.0, a_sat=0.8, tau_N=30.0, b_sqrt=0.01)
    if abs(R[0] - 50.0) > 1e-9:
        fails.append(f'rint_growth R(0)≠R0: {R[0]}')
    if not np.all(np.diff(R) >= -1e-9):
        fails.append('rint_growth 비단조')
    ret = retention(N, q_lin=0.001, q_sqrt=0.005)
    if not (ret[0] == 100.0 and ret[-1] < 100.0 and np.all(ret >= 0)):
        fails.append(f'retention 경계/단조 실패: {ret[0]},{ret[-1]}')
    # 2) feature 조립: 결측 nan(§F1 날조금지), 존재값 정확
    case = {'porosity_mpm_pct': 7.9, 'step3': {'sigma_e_eff_S_cm': 3.0, 'sigma_ion_eff_S_cm': 2e-4,
            'field_scale_e': {'focus_top': 67.6}, 'field_scale_ion': {'focus_top': 32.9}}}
    f, names = assemble_features(case, cycle_N=10, design={'am_pct': 82, 'sdcp_wt': 0.5})
    if len(f) != len(DESIGN_KNOBS) + len(PHYS_FEATURES) + 1:
        fails.append(f'feature 길이 {len(f)}')
    if not (f[names.index('cycle_N')] == 10 and f[names.index('am_pct')] == 82):
        fails.append('feature 값 매핑 오류')
    if not np.isnan(f[names.index('d_se_um')]):
        fails.append('결측이 nan 아님(§F1: 0으로 날조 금지)')
    if not (abs(f[names.index('sigma_e_eff')] - 3.0) < 1e-9 and abs(f[names.index('focus_e')] - 67.6) < 1e-9):
        fails.append('물리-feature 추출 오류')
    # 3) surrogate: sklearn 있으면 학습·예측, 없으면 graceful (import-guard 규약)
    rng = np.random.RandomState(0)
    Xtr = rng.rand(40, len(names)); Xtr[:, names.index('cycle_N')] = rng.randint(0, 100, 40)
    Ytr = {'R_int_ohm_cm2': 50 + 0.3 * Xtr[:, names.index('cycle_N')] + rng.randn(40),
           'sigma_e_eff': 2 + Xtr[:, names.index('sigma_e_eff')]}
    sur = CycleSurrogate(targets=['R_int_ohm_cm2', 'sigma_e_eff'])
    res = sur.fit(Xtr, Ytr, feat_names=names)
    if 'ready' not in res:
        fails.append('fit 반환 규약 위반')
    if res.get('ready'):                                     # sklearn 존재(WSL)
        pr = sur.predict(Xtr[0])
        if 'R_int_ohm_cm2' not in pr or 'mean' not in pr['R_int_ohm_cm2']:
            fails.append('predict 반환 구조 오류')
        cur = sur.predict_cycle_curve(Xtr[0], n_max=100, n_pts=6)
        if len(cur['N']) != 6 or any(v is None for v in cur['R_int']):
            fails.append('predict_cycle_curve 오류')
        print(f'  [WSL] surrogate 학습·예측·사이클곡선 OK ({res["status"]})')
    else:
        print(f'  [cloud] sklearn 부재 → import-guard graceful ✓ ({res["status"][:40]}…)')
    print('selftest OK' if not fails else 'selftest FAIL:\n  ' + '\n  '.join(fails))
    if not fails:
        print(f"  성장모델: R_int(0)=50→(100)={R[-1]:.1f}Ω·cm² · retention(100)={ret[-1]:.1f}%")
        print(f"  feature: {len(DESIGN_KNOBS)} 설계 + {len(PHYS_FEATURES)} 물리(★차별) + 1 cycle = {len(f)}")
    return 1 if fails else 0


if __name__ == '__main__':
    import sys
    raise SystemExit(_selftest() if (len(sys.argv) <= 1 or sys.argv[1] == '--selftest') else _selftest())
