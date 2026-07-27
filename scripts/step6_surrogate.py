#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STEP6 — MLIP식 전기화학 surrogate v1 (STEP4 시간전개의 수요-측 가속).

MLIP 대응: 원자 국소환경 서술자→(에너지·힘)+위원회 불확실성→MD 전진, 외삽 감지 시 DFT 앵커.
우리: (SOC·표면 stoich·η·유효저항 서술자 ‖ 설계벡터)→(다음 스텝 Δstate)+위원회 밴드→시간 전개,
σ>gate 시 STEP4 실솔버 앵커 호출·transition 버퍼 축적·(v2)온라인 재학습.
파이프라인 정확도 상속 = MLIP 규약 (학습데이터 provenance='model'=STEP4 산출 → 전 출력 §F1 라벨).

솔버 치료(R1-R5)와 직교: R1/R2/R4/R5=공급-측(솔브 단가·조건수), STEP6=수요-측(비싼 스텝을 전개로
건너뛰고 앵커만 실솔브 + v2 warm-start 훅).  ★정직 한계: 앵커 호출 시 깊은 보정해 목표
(atol_cg≈2.7e-13~2.7e-14)가 Jacobi 자기바닥(~1.4e-12) 아래인 한 nnAMG의 정당한 필요는 잔존 —
STEP6은 호출 빈도만 줄이고 단가는 못 고침(단가=R1/R2/R4 몫).  "확률 높으면 진행"의 공식화:
deep_weak 조기종료 부분수렴 상태(resid 정직 보고)를 위원회 밴드가 덮으면 명시 로그와 함께 앵커
수용(이중 증거: 솔버 resid + surrogate 밴드) — 침묵 수용 금지 (v2, §8).

자산 재사용: ml_cycle_surrogate(스키마·nan=결측·import-guard·provenance) / ml_design_loop
(scalarize·sobol_doe) / eis_drt_ica(R0·R_ct·R_film 유효저항 = Q_*_W/I², frame[4] 회로 정합) /
cycling_data_ingest(provenance 게이트 → 여기선 provenance='model-surrogate').
스케일 분업: ml_cycle_surrogate=사이클-N 축(R_int(N)·retention) ‖ step6=사이클-내 시간축(V(t)).

selftest = 합성 RC-방전 ODE (TEST-ONLY §F1) — 진짜 동역학 생성→추출→학습→전파→밴드 정합→
OOD gate→앵커→랭킹까지 클라우드(numpy-only)에서 실제 PASS.
"""
from __future__ import annotations

import argparse
import glob as _glob
import hashlib
import json
import math
import os
import subprocess
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:                                                     # ml_design_loop 재사용 (§0 계약)
    from ml_design_loop import APP_OBJECTIVES, scalarize
except Exception:                                        # 단독 실행 폴백 (동일 수식 최소 복제)
    APP_OBJECTIVES = {}

    def scalarize(metrics, app='balanced', missing='penalize'):
        s = 0.0
        for key, sign, w in APP_OBJECTIVES.get(app, []):
            v = metrics.get(key)
            if v is None:
                if missing == 'nan':
                    return float('nan')
                v = 0.5 if missing == 'neutral' else (0.0 if sign > 0 else 1.0)
            s += w * sign * float(v)
        return float(s)

# ───────────────────────────── § 스키마/상수 ─────────────────────────────
F1_LABEL = ('SURROGATE/UNCALIBRATED — 전개값은 STEP4-모델 상속 예측; '
            '절대 신뢰는 앵커(실솔버) 상태만 (§F1)')
SCHEMA_VERSION = 'step6-v1'

# 설계특징 (params_json + npz + 선택적 STEP3 join; 결측=nan, 날조 금지 — ml_cycle_surrogate 규약)
DESIGN_FEATURES = [
    'c_rate', 'thickness_um',            # params / viz_z_um.max()
    'r_int_ohm_cm2', 'd_s_m2s',          # params (per-particle dict 는 log-mean)
    'i0_A_m2', 'asr_film', 'temp_k',     # params
    'areal_mAh_cm2', 'i_1c_A',           # params(area 필요) · npz I_1C_A
    'bv_face_per_cm2',                   # viz_I_face.shape[1]/면적 (면적 없으면 nan)
    'x0', 'x100', 'cv_hold',             # params (창·프로토콜)
    'sigma_e_eff', 'sigma_ion_eff',      # ★STEP3 join (mpm_payload.json; 없으면 nan)
    'log_tau_w',                         # eis_drt_ica: log(r_p²/D_s) (r_p join 없으면 nan)
]
# 상태벡터 s_t (전부 npz 시계열에서)
STATE_KEYS = ['x_mean', 'x_surf_p05', 'x_surf_p50', 'x_surf_p95',
              'eta_kin_V', 'eta_diff_V', 'v_terminal', 'i_norm',    # i_norm = |I|/I_1C
              'r0_eff', 'r_ct_eff', 'r_film_eff',                   # Q_*_W/I² (eis_drt_ica 정합)
              'phase_cc']                                            # 1=CC, 0=CV
# 물리-basis (state/design 에서만 계산 — 누수 없음; b_gap_relax/b_coul_step 은 확산-지연·쿨롱
# 구동항의 이산화 = 설계서 basis 의 물리-유도 확장 2항)
BASIS_KEYS = ['b_head_room', 'b_gap_surf_core', 'b_ir_scale', 'b_bv_asinh', 'b_log_dt',
              'b_gap_relax', 'b_coul_step']
# ★ 쿨롱계수 항은 학습 제외(정확 부기 — 전개에서 정확 적용; 추출기가 npz 항등식 자가검산)
DELTA_TARGETS_CC = ['d_v_terminal', 'd_x_surf_p05', 'd_x_surf_p50', 'd_x_surf_p95',
                    'd_eta_kin_V', 'd_eta_diff_V']
DELTA_TARGETS_CV = DELTA_TARGETS_CC + ['d_i_norm']                   # CV 는 전류가 상태
FEAT_NAMES = STATE_KEYS + DESIGN_FEATURES + BASIS_KEYS + ['dt_s']
_D2S = {'d_v_terminal': 'v_terminal', 'd_x_surf_p05': 'x_surf_p05', 'd_x_surf_p50': 'x_surf_p50',
        'd_x_surf_p95': 'x_surf_p95', 'd_eta_kin_V': 'eta_kin_V', 'd_eta_diff_V': 'eta_diff_V',
        'd_i_norm': 'i_norm'}
# 위원회 feature-subset 에서 항상 유지(퇴화 방지): 핵심 state + 물리 구동 basis 2항
_CORE_KEEP = ('x_surf_p50', 'i_norm', 'dt_s', 'b_gap_relax', 'b_coul_step')
_COUL_WARN_REL, _COUL_FAIL_REL = 1e-6, 1e-3              # 쿨롱 검산: 경고 / 런 제외 문턱
_SERIES_REQ = ('t', 'V_terminal', 'I', 'x_mean', 'x_surf_p05', 'x_surf_p50', 'x_surf_p95',
               'eta_kin_mean', 'eta_diff_mean', 'Q_ohm_e_W', 'Q_ohm_i_W', 'Q_ct_W', 'Q_film_W')
_SERIES_OPT = ('newton_resid', 'kcl_rel', 'energy_balance_rel', 'Q_rint_W', 'V')

# rank 용 앱-목적 (ml_design_loop.APP_OBJECTIVES 에 s6_ 네임스페이스로 등록 = scalarize 재사용;
# metric 은 [0,1] 정규화 전제, missing='penalize' 규약 그대로)
S6_OBJECTIVES = {
    's6_balanced':    [('delivered', +1, 0.5), ('v_mean', +1, 0.3), ('q_ohm_frac', -1, 0.2)],
    's6_fast_charge': [('delivered', +1, 0.5), ('v_mean', +1, 0.2), ('q_ohm_frac', -1, 0.3)],
    's6_explore':     [('anchor_need_frac', +1, 0.7), ('delivered', +1, 0.3)],
}
for _k, _v in S6_OBJECTIVES.items():
    APP_OBJECTIVES.setdefault(_k, _v)


def _f(v):
    """안전 float — 없음/비수치 = nan (§F1: 0 날조 금지)."""
    if v is None:
        return float('nan')
    if isinstance(v, dict):                              # per-particle {min,max} → log-mean
        try:
            return float(math.sqrt(float(v['min']) * float(v['max'])))
        except Exception:
            return float('nan')
    try:
        return float(v)
    except (TypeError, ValueError):
        return float('nan')


# ───────────────────────────── § (1) 추출기 ─────────────────────────────
def load_step4_npz(src):
    """step4 npz(경로) 또는 동형 dict(합성) → {시계열 arrays + params dict + 스칼라}.
    필수 시계열 누락은 'missing' 에 기록(호출측이 런 스킵) — 크래시 금지."""
    if isinstance(src, dict):
        d = dict(src)
        path = str(d.pop('_path', '<in-memory>'))
    else:
        path = str(src)
        with np.load(path, allow_pickle=True) as z:
            d = {k: z[k] for k in z.files}
    pj = d.get('params_json')
    if isinstance(pj, np.ndarray):
        pj = pj.item() if pj.ndim == 0 else None
    if isinstance(pj, bytes):
        pj = pj.decode()
    params = json.loads(pj) if isinstance(pj, str) else (pj if isinstance(pj, dict) else {})
    out = {'path': path, 'params': params or {}}
    for k in _SERIES_REQ + _SERIES_OPT:
        if k in d:
            out[k] = np.asarray(d[k], float).ravel()
    for k in ('viz_z_um',):
        if k in d:
            out[k] = np.asarray(d[k], float).ravel()
    if 'viz_I_face' in d:
        out['viz_I_face'] = np.asarray(d['viz_I_face'])
    for k in ('I_1C_A', 'q_frac_at_cutoff'):
        if k in d:
            out[k] = float(np.asarray(d[k]).ravel()[0])
    out['missing'] = [k for k in _SERIES_REQ if k not in out] + \
                     ([] if 'I_1C_A' in out else ['I_1C_A'])
    return out


def design_from_run(run, step3=None):
    """params_json + npz + 선택 STEP3 payload → 설계 dict (DESIGN_FEATURES 값; 결측=nan)."""
    p, s3 = run['params'], (step3 or {})
    d_s, i0 = _f(p.get('d_s')), _f(p.get('i0'))
    thick = float(np.max(run['viz_z_um'])) if 'viz_z_um' in run else _f(p.get('thickness_um'))
    area = _f(p.get('area_cm2'))                          # 실 step4 params 엔 없음 → nan 정직
    areal = _f(p.get('areal_mAh_cm2'))
    i1c = _f(run.get('I_1C_A'))
    if not np.isfinite(areal) and np.isfinite(area) and area > 0 and np.isfinite(i1c):
        areal = i1c / area * 1e3                          # A/cm² × 1h → mAh/cm²
    bv = float('nan')
    if 'viz_I_face' in run and np.isfinite(area) and area > 0:
        bv = float(run['viz_I_face'].shape[-1]) / area
    r_p = _f(s3.get('r_p_um', p.get('r_p_um')))
    ltw = float('nan')
    if np.isfinite(r_p) and r_p > 0 and np.isfinite(d_s) and d_s > 0:
        ltw = math.log((r_p * 1e-6) ** 2 / d_s)           # eis_drt_ica: τ_w = r_p²/D_s
    return {'c_rate': _f(p.get('c_rate')), 'thickness_um': thick,
            'r_int_ohm_cm2': _f(p.get('r_int_ohm_cm2')), 'd_s_m2s': d_s, 'i0_A_m2': i0,
            'asr_film': _f(p.get('asr_film')), 'temp_k': _f(p.get('temp_k')),
            'areal_mAh_cm2': areal, 'i_1c_A': i1c, 'bv_face_per_cm2': bv,
            'x0': _f(p.get('x0')), 'x100': _f(p.get('x100')),
            'cv_hold': float(bool(p.get('cv_hold', False))),
            'sigma_e_eff': _f(s3.get('sigma_e_eff_S_cm')),
            'sigma_ion_eff': _f(s3.get('sigma_ion_eff_S_cm')),
            'log_tau_w': ltw, 'r_p_um': r_p}


def _design_vec(design):
    """설계 dict → DESIGN_FEATURES 순서 벡터.  log_tau_w 없으면 r_p_um·d_s 로 계산 시도."""
    d = dict(design)
    if not np.isfinite(_f(d.get('log_tau_w'))):
        rp, ds = _f(d.get('r_p_um')), _f(d.get('d_s_m2s'))
        if np.isfinite(rp) and rp > 0 and np.isfinite(ds) and ds > 0:
            d['log_tau_w'] = math.log((rp * 1e-6) ** 2 / ds)
    return np.array([_f(d.get(k)) for k in DESIGN_FEATURES], float)


def _physics_basis(state, design, dt_s):
    """물리-유도 확장항 (★frame[5] payoff = "why" 있는 feature; 전부 state/design 계산 = 누수 0).
    b_gap_relax=(표면-코어 갭)·dt/τ_w (확산 완화 스텝) · b_coul_step=i·dt/3600·창 (쿨롱 구동 스텝)."""
    x100, x0 = _f(design.get('x100')), _f(design.get('x0'))
    i0 = _f(design.get('i0_A_m2'))
    ltw = _f(design.get('log_tau_w'))
    tau_w = math.exp(ltw) if np.isfinite(ltw) else float('nan')
    gap = state['x_surf_p50'] - state['x_mean']
    inorm = state['i_norm']
    return np.array([
        x100 - state['x_surf_p50'],                                        # b_head_room
        gap,                                                               # b_gap_surf_core
        inorm * state['r0_eff'],                                           # b_ir_scale
        math.asinh(inorm / i0) if (np.isfinite(i0) and i0 > 0) else float('nan'),  # b_bv_asinh
        math.log(max(dt_s, 1e-12)),                                        # b_log_dt
        gap * dt_s / tau_w if (np.isfinite(tau_w) and tau_w > 0) else float('nan'),  # b_gap_relax
        inorm * dt_s / 3600.0 * (x100 - x0),                               # b_coul_step
    ], float)


def _row(state, dvec, design, dt_s):
    """s_t ‖ design ‖ basis ‖ dt → X 행 (FEAT_NAMES 순서)."""
    sv = np.array([state[k] for k in STATE_KEYS], float)
    return np.concatenate([sv, dvec, _physics_basis(state, design, dt_s), [dt_s]])


def _run_states(run):
    """런 시계열 → [n, len(STATE_KEYS)] 상태행렬.  phase 추론: |I| ≥ 0.995·|I[0]| = CC
    (npz 에 phase 배열 없음 — CC 전류는 상수, CV 는 감쇠 = 정직 추론, 문서 명기)."""
    I = run['I']
    i1c = max(abs(float(run['I_1C_A'])), 1e-30)
    inorm = np.abs(I) / i1c
    I2 = np.maximum(I * I, 1e-30)
    cols = {'x_mean': run['x_mean'], 'x_surf_p05': run['x_surf_p05'],
            'x_surf_p50': run['x_surf_p50'], 'x_surf_p95': run['x_surf_p95'],
            'eta_kin_V': run['eta_kin_mean'], 'eta_diff_V': run['eta_diff_mean'],
            'v_terminal': run['V_terminal'], 'i_norm': inorm,
            'r0_eff': (run['Q_ohm_e_W'] + run['Q_ohm_i_W']) / I2,     # eis_drt_ica R0 정합
            'r_ct_eff': run['Q_ct_W'] / I2, 'r_film_eff': run['Q_film_W'] / I2,
            'phase_cc': (np.abs(I) >= 0.995 * abs(I[0])).astype(float)}
    return np.column_stack([cols[k] for k in STATE_KEYS])


def _resolve_step3(path, cli_map=None):
    """STEP3 join: ①CLI 'case=path' 맵(경로 부분일치) ②케이스 폴더 sibling mpm_payload.json.
    실패 시 {} (경고는 호출측 1줄; 날조 0)."""
    for key, jp in (cli_map or {}).items():
        if key in str(path):
            try:
                j = json.load(open(jp))
                return (j.get('step3') or j)
            except Exception:
                return {}
    sib = os.path.join(os.path.dirname(str(path)), 'mpm_payload.json')
    if os.path.isfile(sib):
        try:
            j = json.load(open(sib))
            return (j.get('step3') or j)
        except Exception:
            pass
    return {}


def extract_transitions(npz_paths, step3_map=None, quality_gate=True, verbose=True):
    """코퍼스(npz 경로 또는 동형 dict 리스트) → 전이쌍 데이터셋.
    · 스텝 k→k+1: dt=t[k+1]−t[k] 를 feature 로 (적응 dt 지원).
    · phase 경계 스텝(cc↔cv)의 전이쌍은 양쪽 모두 제외 (라벨 오염 방지).
    · quality_gate: newton_resid > 4·median 스텝 태그 → weight 0.25 (포함하되 정직 라벨 —
      부분수렴 데이터도 라벨과 함께 쓰는 게 STEP6 취지; ASSUMED 다운웨이트).
    · 쿨롱 검산: |Δx̄ − ±i·dt/3600·(x100−x0)| (fwd/사다리꼴 중 최소) 상대오차 >1e-6 경고,
      >1e-3 런 제외(excluded 목록 반환) — 추출기 자가검증."""
    Xc, Yc, Wc, Rc = [], [], [], []
    Xv, Yv, Wv, Rv = [], [], [], []
    bank_d, bank_s, runs, metas, qual, excluded = [], [], [], [], [], []
    iph = STATE_KEYS.index('phase_cc')
    iin = STATE_KEYS.index('i_norm')
    for src in npz_paths:
        run = load_step4_npz(src)
        path = run['path']
        if run['missing']:
            if verbose:
                print(f"  ⚠ {os.path.basename(path)}: 필수 키 누락 {run['missing'][:4]} → 스킵")
            excluded.append({'path': path, 'reason': f"missing:{run['missing'][:4]}"})
            continue
        s3 = _resolve_step3(path, step3_map) if not isinstance(src, dict) else \
            (step3_map or {}).get(path, {})
        dsn = design_from_run(run, s3)
        win = dsn['x100'] - dsn['x0']
        if not (np.isfinite(win) and abs(win) > 1e-9):
            excluded.append({'path': path, 'reason': 'x0/x100 없음(쿨롱창 불가)'})
            continue
        S = _run_states(run)
        t = run['t']
        n = S.shape[0]
        if n < 3:
            excluded.append({'path': path, 'reason': f'스텝 {n}<3'})
            continue
        dt = np.diff(t)
        # ── 쿨롱계수 항등식 검산 (★학습 안 하는 항의 자가검증)
        sgn = 1.0 if run['x_mean'][-1] >= run['x_mean'][0] else -1.0
        dx = np.diff(run['x_mean'])
        pf = sgn * S[:-1, iin] * dt / 3600.0 * abs(win)
        ptz = sgn * 0.5 * (S[:-1, iin] + S[1:, iin]) * dt / 3600.0 * abs(win)
        rel = np.minimum(np.abs(dx - pf), np.abs(dx - ptz)) / abs(win)
        crel = float(rel.max())
        if crel > _COUL_FAIL_REL:
            if verbose:
                print(f'  ⚠ {os.path.basename(path)}: 쿨롱 검산 실패 rel={crel:.2e} → 런 제외')
            excluded.append({'path': path, 'reason': f'coulomb rel {crel:.2e}'})
            continue
        if crel > _COUL_WARN_REL and verbose:
            print(f'  ⚠ {os.path.basename(path)}: 쿨롱 검산 rel={crel:.2e} (>{_COUL_WARN_REL:g})')
        # ── 품질 태그 (수렴품질 배지 규약)
        resid = run.get('newton_resid')
        w_step = np.ones(n - 1)
        if quality_gate and resid is not None and len(resid) == n:
            med = float(np.median(resid[resid > 0])) if (resid > 0).any() else 0.0
            if med > 0:
                w_step[resid[1:] > 4.0 * med] = 0.25      # 태그 = 다운웨이트 (ASSUMED)
        rid = len(runs)
        dvec = _design_vec(dsn)
        dV = np.diff(run['V_terminal'])
        dS = {tn: np.diff(S[:, STATE_KEYS.index(_D2S[tn])]) for tn in DELTA_TARGETS_CV}
        for k in range(n - 1):
            if S[k, iph] != S[k + 1, iph]:                # phase 경계 → 양쪽 모두 제외
                continue
            x = np.concatenate([S[k], dvec,
                                _physics_basis(dict(zip(STATE_KEYS, S[k])), dsn, dt[k]), [dt[k]]])
            if S[k, iph] >= 0.5:
                Xc.append(x)
                Yc.append([dV[k] if tn == 'd_v_terminal' else dS[tn][k] for tn in DELTA_TARGETS_CC])
                Wc.append(w_step[k]); Rc.append(rid)
            else:
                Xv.append(x)
                Yv.append([dV[k] if tn == 'd_v_terminal' else dS[tn][k] for tn in DELTA_TARGETS_CV])
                Wv.append(w_step[k]); Rv.append(rid)
        bank_d.append(dvec); bank_s.append(S[0])
        runs.append(path); metas.append(dsn)
        qual.append({'coul_rel_max': crel,
                     'resid_max': float(np.max(resid)) if resid is not None else float('nan'),
                     'ebal_max': float(np.max(run['energy_balance_rel']))
                     if 'energy_balance_rel' in run else float('nan'),
                     'kcl_max': float(np.max(run['kcl_rel'])) if 'kcl_rel' in run else float('nan')})
    def _a(v, dt=float):
        return np.asarray(v, dt) if v else np.zeros((0,), dt)
    return {'label': F1_LABEL, 'schema': SCHEMA_VERSION, 'feat_names': list(FEAT_NAMES),
            'tgt_cc': list(DELTA_TARGETS_CC), 'tgt_cv': list(DELTA_TARGETS_CV),
            'X_cc': np.asarray(Xc, float) if Xc else np.zeros((0, len(FEAT_NAMES))),
            'Y_cc': np.asarray(Yc, float) if Yc else np.zeros((0, len(DELTA_TARGETS_CC))),
            'w_cc': _a(Wc), 'run_cc': _a(Rc, int),
            'X_cv': np.asarray(Xv, float) if Xv else np.zeros((0, len(FEAT_NAMES))),
            'Y_cv': np.asarray(Yv, float) if Yv else np.zeros((0, len(DELTA_TARGETS_CV))),
            'w_cv': _a(Wv), 'run_cv': _a(Rv, int),
            'bank_design': np.asarray(bank_d, float) if bank_d else np.zeros((0, len(DESIGN_FEATURES))),
            'bank_state': np.asarray(bank_s, float) if bank_s else np.zeros((0, len(STATE_KEYS))),
            'runs': runs, 'meta': metas, 'quality': qual, 'excluded': excluded}


# ───────────────────────────── § (2) 위원회 ─────────────────────────────
class RidgeCommittee:
    """numpy-only 위원회: bootstrap(행 boot_frac) × random feature-subset(열 feat_frac) ridge.
    MLIP 앙상블 유사 — 평균=예측, 멤버 표준편차=인식적 불확실성 프록시(휴리스틱, ASSUMED 라벨).
    _CORE_KEEP 열(핵심 state + 물리 구동 basis)은 subset 에서 항상 유지(퇴화 방지)."""

    def __init__(self, n_members=24, lam=1e-3, feat_frac=0.7, boot_frac=0.8, seed=0):
        self.n_members, self.lam = int(n_members), float(lam)
        self.feat_frac, self.boot_frac, self.seed = float(feat_frac), float(boot_frac), int(seed)
        self.feat_names = self.tgt_names = None
        self.W = self.mask = self._mu = self._sd = self._med = self.sres = None
        self._ready = False

    def fit(self, X, Y, feat_names, tgt_names, sample_w=None, verbose=True):
        X, Y = np.atleast_2d(np.asarray(X, float)), np.atleast_2d(np.asarray(Y, float))
        self.feat_names, self.tgt_names = list(feat_names), list(tgt_names)
        with warnings.catch_warnings():                   # 전-결측 열 nanmedian 경고는 아래서 직접
            warnings.simplefilter('ignore', RuntimeWarning)
            med = np.nanmedian(np.where(np.isfinite(X), X, np.nan), axis=0)
        self._med = np.where(np.isfinite(med), med, 0.0)
        allnan = ~np.isfinite(X).any(axis=0)
        if allnan.any() and verbose:                      # ml_cycle_surrogate 전-결측 경고 규약
            bad = [self.feat_names[i] for i in np.where(allnan)[0]]
            print(f'  ⚠ 전-결측 feature {int(allnan.sum())}개 → median=0 impute(무정보): {bad[:8]}')
        Xi = np.where(np.isfinite(X), X, self._med)
        self._mu = Xi.mean(0)
        sd = Xi.std(0)
        self._sd = np.where(sd < 1e-12, 1.0, sd)
        Xs = (Xi - self._mu) / self._sd
        n, d = Xs.shape
        T = Y.shape[1]
        w = np.ones(n) if sample_w is None else np.asarray(sample_w, float)
        rng = np.random.default_rng(self.seed)
        core = [i for i, nm in enumerate(self.feat_names) if nm in _CORE_KEEP]
        rest = [i for i in range(d) if i not in core]
        self.W = np.zeros((self.n_members, d + 1, T))
        self.mask = np.zeros((self.n_members, d), bool)
        for m in range(self.n_members):
            rows = rng.integers(0, n, max(4, int(round(self.boot_frac * n))))
            keep = sorted(set(core) | set(
                rng.choice(rest, size=max(1, int(round(self.feat_frac * len(rest)))),
                           replace=False).tolist() if rest else []))
            self.mask[m, keep] = True
            A = np.concatenate([np.ones((len(rows), 1)), Xs[rows][:, keep]], axis=1)
            sw = np.sqrt(w[rows])[:, None]
            reg = self.lam * np.eye(A.shape[1])
            reg[0, 0] = 0.0                               # 절편은 무벌점
            Wm = np.linalg.solve((A * sw).T @ (A * sw) + reg, (A * sw).T @ (Y[rows] * sw))
            self.W[m, 0] = Wm[0]
            self.W[m, np.array(keep) + 1] = Wm[1:]
        self._ready = True
        mean = self.predict(X)[0]
        resid = Y - mean
        self.sres = np.sqrt(np.average(resid ** 2, axis=0, weights=w))   # aleatoric 프록시(ASSUMED)
        ss = np.maximum(((Y - Y.mean(0)) ** 2).sum(0), 1e-30)
        r2 = 1.0 - (resid ** 2).sum(0) / ss
        return {'ready': True, 'n': n, 'label': F1_LABEL,
                'train_r2': {t_: float(r) for t_, r in zip(self.tgt_names, r2)},
                'note': 'train R² 참고용 — 보고 지표는 loco_score(런 단위)만 (시계열 누수 규율)'}

    def predict(self, X):
        """X[n,d] → (mean[n,T], std[n,T], members[M,n,T])."""
        if not self._ready:
            raise RuntimeError('committee not fitted')
        X = np.atleast_2d(np.asarray(X, float))
        Xs = (np.where(np.isfinite(X), X, self._med) - self._mu) / self._sd
        A = np.concatenate([np.ones((len(Xs), 1)), Xs], axis=1)
        members = np.einsum('nf,mft->mnt', A, self.W)
        return members.mean(0), members.std(0), members

    def loco_score(self, X, Y, run_id, sample_w=None):
        """★leave-one-curve-out(런 단위) R² — 시계열 자기상관 누수 차단.
        random-split R² 는 보고 금지(낙관 편향; repo LOOCV 규율의 시계열판)."""
        X, Y = np.atleast_2d(np.asarray(X, float)), np.atleast_2d(np.asarray(Y, float))
        run_id = np.asarray(run_id)
        preds = np.full_like(Y, np.nan)
        for u in np.unique(run_id):
            m = run_id == u
            if m.all() or (~m).sum() < 10:
                continue
            c = type(self)(self.n_members, self.lam, self.feat_frac, self.boot_frac,
                           self.seed + 1000 + int(u))
            c.fit(X[~m], Y[~m], self.feat_names, self.tgt_names,
                  None if sample_w is None else np.asarray(sample_w)[~m], verbose=False)
            preds[m] = c.predict(X[m])[0]
        ok = np.isfinite(preds).all(axis=1)
        r2 = {}
        for j, tn in enumerate(self.tgt_names):
            yy, pp = Y[ok, j], preds[ok, j]
            r2[tn] = float(1.0 - ((yy - pp) ** 2).sum() / max(((yy - yy.mean()) ** 2).sum(), 1e-30))
        return {'per_target': r2, 'n_pooled': int(ok.sum()), 'n_runs': int(len(np.unique(run_id))),
                'label': F1_LABEL,
                'note': 'LOCO(런 단위) — random-split 보고 금지(시계열 자기상관 누수)'}

    # ── 저장/로드 (npz 팩; save_model 이 phase 별 2개를 한 npz 에) ──
    def to_arrays(self, prefix=''):
        meta = {'n_members': self.n_members, 'lam': self.lam, 'feat_frac': self.feat_frac,
                'boot_frac': self.boot_frac, 'seed': self.seed,
                'feat_names': self.feat_names, 'tgt_names': self.tgt_names}
        return {prefix + 'W': self.W, prefix + 'mask': self.mask, prefix + 'mu': self._mu,
                prefix + 'sd': self._sd, prefix + 'med': self._med, prefix + 'sres': self.sres,
                prefix + 'meta': np.array(json.dumps(meta))}

    @classmethod
    def from_arrays(cls, z, prefix=''):
        meta = json.loads(str(np.asarray(z[prefix + 'meta']).item()))
        c = cls(meta['n_members'], meta['lam'], meta['feat_frac'], meta['boot_frac'], meta['seed'])
        c.feat_names, c.tgt_names = meta['feat_names'], meta['tgt_names']
        c.W, c.mask = np.asarray(z[prefix + 'W']), np.asarray(z[prefix + 'mask'])
        c._mu, c._sd = np.asarray(z[prefix + 'mu']), np.asarray(z[prefix + 'sd'])
        c._med, c.sres = np.asarray(z[prefix + 'med']), np.asarray(z[prefix + 'sres'])
        c._ready = True
        return c


class SkCommittee(RidgeCommittee):
    """sklearn GBR(비선형) 위원회 업그레이드 — import-guard (WSL 전용, ml_cycle_surrogate 규약).
    클라우드(sklearn 부재)에선 fit 이 {'ready': False} 반환 (크래시 금지).
    predict 인터페이스 동일 → propagate/rank 는 모델 종류 무관."""

    def fit(self, X, Y, feat_names, tgt_names, sample_w=None, verbose=True):
        try:
            from sklearn.ensemble import GradientBoostingRegressor
        except ImportError:
            self._ready = False
            return {'ready': False, 'label': F1_LABEL,
                    'status': 'sklearn 부재 (WSL 전용) — RidgeCommittee(numpy) 폴백 사용'}
        X, Y = np.atleast_2d(np.asarray(X, float)), np.atleast_2d(np.asarray(Y, float))
        self.feat_names, self.tgt_names = list(feat_names), list(tgt_names)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            med = np.nanmedian(np.where(np.isfinite(X), X, np.nan), axis=0)
        self._med = np.where(np.isfinite(med), med, 0.0)
        Xi = np.where(np.isfinite(X), X, self._med)
        self._mu, sd = Xi.mean(0), Xi.std(0)
        self._sd = np.where(sd < 1e-12, 1.0, sd)
        Xs = (Xi - self._mu) / self._sd
        n = len(Xs)
        rng = np.random.default_rng(self.seed)
        w = np.ones(n) if sample_w is None else np.asarray(sample_w, float)
        self._sk = []                                     # [member][target] GBR
        for m in range(self.n_members):
            rows = rng.integers(0, n, max(4, int(round(self.boot_frac * n))))
            mods = []
            for j in range(Y.shape[1]):
                g = GradientBoostingRegressor(n_estimators=150, max_depth=3,
                                              subsample=0.9, random_state=self.seed + m)
                g.fit(Xs[rows], Y[rows, j], sample_weight=w[rows])
                mods.append(g)
            self._sk.append(mods)
        self._ready = True
        mean = self.predict(X)[0]
        self.sres = np.sqrt(np.average((Y - mean) ** 2, axis=0, weights=w))
        return {'ready': True, 'n': n, 'label': F1_LABEL, 'status': f'GBR 위원회 {self.n_members}멤버'}

    def predict(self, X):
        if not getattr(self, '_sk', None):
            return super().predict(X)
        X = np.atleast_2d(np.asarray(X, float))
        Xs = (np.where(np.isfinite(X), X, self._med) - self._mu) / self._sd
        members = np.stack([np.column_stack([g.predict(Xs) for g in mods]) for mods in self._sk])
        return members.mean(0), members.std(0), members

    def to_arrays(self, prefix=''):
        raise NotImplementedError('SkCommittee 저장은 v2 (WSL joblib) — v1 은 RidgeCommittee npz 만')


# ── 모델 팩 저장/로드 (phase 별 cc/cv + state0-bank 를 한 npz 에) ──
def save_model(path, com_cc, com_cv=None, bank_design=None, bank_state=None, extra_meta=None):
    arrs = com_cc.to_arrays('cc_')
    if com_cv is not None:
        arrs.update(com_cv.to_arrays('cv_'))
    if bank_design is not None:
        arrs['bank_design'] = np.asarray(bank_design, float)
        arrs['bank_state'] = np.asarray(bank_state, float)
    meta = {'label': F1_LABEL, 'schema': SCHEMA_VERSION, 'has_cv': com_cv is not None}
    meta.update(extra_meta or {})
    arrs['meta_json'] = np.array(json.dumps(meta, default=str))
    np.savez(path, **arrs)
    return path


def load_model(path):
    with np.load(path, allow_pickle=False) as z:
        meta = json.loads(str(np.asarray(z['meta_json']).item()))
        if meta.get('schema') != SCHEMA_VERSION:
            raise ValueError(f"모델 스키마 불일치: {meta.get('schema')} ≠ {SCHEMA_VERSION} — 재학습 필요")
        out = {'cc': RidgeCommittee.from_arrays(z, 'cc_'),
               'cv': RidgeCommittee.from_arrays(z, 'cv_') if meta.get('has_cv') else None,
               'meta': meta, 'label': F1_LABEL}
        for k in ('bank_design', 'bank_state'):
            out[k] = np.asarray(z[k]) if k in z.files else None
    return out


def train_from_corpus(npz_paths, step3_map=None, use_sklearn=False, seed=0, loco=True,
                      hyper=None, verbose=True):
    """코퍼스 → 추출 → phase 별 위원회 학습(+LOCO) → 모델 dict (save_model 로 저장 가능)."""
    data = extract_transitions(npz_paths, step3_map, verbose=verbose)
    if data['X_cc'].shape[0] < 30:
        raise ValueError(f"CC 전이쌍 {data['X_cc'].shape[0]} < 30 — 코퍼스 부족")
    cls = SkCommittee if use_sklearn else RidgeCommittee
    hyper = hyper or {}
    cc = cls(seed=seed, **hyper)
    res_cc = cc.fit(data['X_cc'], data['Y_cc'], data['feat_names'], data['tgt_cc'],
                    sample_w=data['w_cc'], verbose=verbose)
    if use_sklearn and not res_cc.get('ready'):
        if verbose:
            print(f"  {res_cc['status']}")
        cc = RidgeCommittee(seed=seed, **hyper)           # graceful 폴백 (numpy 기본 동작)
        res_cc = cc.fit(data['X_cc'], data['Y_cc'], data['feat_names'], data['tgt_cc'],
                        sample_w=data['w_cc'], verbose=verbose)
    cv = None
    res_cv = {'ready': False, 'note': 'CV 전이쌍 부족 — CC 전용 모델'}
    if data['X_cv'].shape[0] >= 30:
        cv = RidgeCommittee(seed=seed + 7, **hyper)
        res_cv = cv.fit(data['X_cv'], data['Y_cv'], data['feat_names'], data['tgt_cv'],
                        sample_w=data['w_cv'], verbose=verbose)
    loco_res = None
    if loco:
        loco_res = cc.loco_score(data['X_cc'], data['Y_cc'], data['run_cc'], data['w_cc'])
    md5s = []
    for p in data['runs']:
        try:
            md5s.append(hashlib.md5(open(p, 'rb').read()).hexdigest()[:12])
        except OSError:
            md5s.append('in-memory')
    meta = {'corpus': [str(p) for p in data['runs']], 'corpus_md5': md5s,
            'n_cc': int(data['X_cc'].shape[0]), 'n_cv': int(data['X_cv'].shape[0]),
            'excluded': data['excluded'], 'loco': (loco_res or {}).get('per_target'),
            'fit_cc': res_cc.get('train_r2'), 'fit_cv': res_cv.get('train_r2')}
    return {'cc': cc, 'cv': cv, 'meta': meta, 'label': F1_LABEL, 'data': data,
            'bank_design': data['bank_design'], 'bank_state': data['bank_state'],
            'loco': loco_res}


# ───────────────────────────── § (3) 전개 ─────────────────────────────
def _state0_from_bank(mdl, dvec):
    """state0 미지정 시: bank(코퍼스 각 런의 첫 스텝 state) → 설계공간 회귀/최근접 보간.
    n_runs≥8 이면 ridge 회귀(설계→state0; V0 의 IR-의존 등 흡수), 미만이면 최근접.
    라벨 'state0-보간' — OCP 없이 V(x_init) 못 만들기 때문 (§F1: 날조 대신 보간+라벨)."""
    D, S = mdl.get('bank_design'), mdl.get('bank_state')
    if D is None or len(D) == 0:
        raise ValueError('state0 없음 + bank 없음 — state0 명시 필요')
    if len(D) >= 8:
        reg = RidgeCommittee(n_members=8, lam=1e-2, feat_frac=1.0, boot_frac=0.9, seed=17)
        reg.fit(D, S, DESIGN_FEATURES, STATE_KEYS, verbose=False)
        s0 = reg.predict(dvec)[0][0]
        return dict(zip(STATE_KEYS, map(float, s0))), 'state0-보간(bank 회귀, UNCALIBRATED)'
    Dm = np.where(np.isfinite(D), D, np.nan)
    mu, sd = np.nanmean(Dm, 0), np.nanstd(Dm, 0)
    sd = np.where(~np.isfinite(sd) | (sd < 1e-12), 1.0, sd)
    z = (np.where(np.isfinite(D), D, mu) - mu) / sd
    q = (np.where(np.isfinite(dvec), dvec, mu) - mu) / sd
    i = int(np.argmin(((z - q) ** 2).sum(1)))
    return dict(zip(STATE_KEYS, map(float, S[i]))), f'state0-보간(bank 최근접 run={i})'


def propagate(model, design, state0=None, dt_s=30.0, t_max=None, c_rate=None, v_cut=3.0,
              cv_hold=False, i_cut_frac=0.05, sigma_gate_mv=5.0, anchor_fn=None,
              anchor_every=None, force=False, n_draw=128, seed=0, band_mode='member',
              max_steps=20000):
    """자기회귀 전개 (MLIP-MD 유사).  스텝: X=[s_t‖design‖basis‖dt] → 위원회 Δ → s_{t+1}=s_t+Δ,
    단 Δx̄ = 쿨롱계수 정확항(학습 안 함 — 질량보존 부기).
    · 밴드 3모드 (전부 UNCALIBRATED — 휴리스틱 라벨):
        'member'(기본) = √(std(멤버 누적 V경로)² + Σs_res²) — 멤버별 스텝-편향이 경로를 따라
          지속 누적되는 걸 그대로 반영(독립가정 없음; MLIP 위원회-궤적 스프레드) ★selftest 로
          RSS 과소를 실증하고 기본으로 채택 (설계서 대비 변경 — 문서 §밴드 기록);
        'rss' = √(Σ std_dv² + Σ s_res²) — 독립가정, 자기회귀 상관 시 과소(낙관 하한);
        'sum' = Σstd + √Σs_res² — 최보수 상한.
    · σ_gate: 스텝 std(d_v)>sigma_gate_mv[mV] →
        anchor_fn 有: state=anchor_fn(state,design) 실측 교체 + transition 버퍼 축적(v2 재학습 입력)
        anchor_fn 無: anchors[] 에 'ANCHOR-NEEDED' 마킹; force=False 면 전개 정지(기본 —
                      확신 없는 곡선 날조 금지), force=True 면 밴드 팽창 유지한 채 계속(스윕/정성).
    · 컷오프(확률적 진행): 멤버별 V-draw(멤버 누적경로 + aleatoric noise, n_draw개) →
      p_cut=P(V<v_cut).  p>0.5 종료; 0.1<p<0.9 = '불확실 종료창' [t_lo,t_hi] 보고.
    · anchor_every: N스텝마다 강제 앵커(드리프트 상한; v2 라이브 훅 기본).
    v1 은 방전 전용 (charge=True 는 v2 — NotImplementedError)."""
    mdl = load_model(model) if isinstance(model, str) else model
    cc, cvm = mdl['cc'], mdl.get('cv')
    design = dict(design)
    if design.get('charge'):
        raise NotImplementedError('충전 전개는 v2 (§8) — v1 은 방전만')
    if c_rate is not None:
        design['c_rate'] = float(c_rate)
    c_rate = _f(design.get('c_rate'))
    if not np.isfinite(c_rate):
        raise ValueError('c_rate 필요')
    x0w, x100w = _f(design.get('x0')), _f(design.get('x100'))
    if not (np.isfinite(x0w) and np.isfinite(x100w)):
        raise ValueError('design.x0/x100 필요 (쿨롱 정확항 — §F1: bank 로도 안 채움)')
    win = x100w - x0w
    dvec = _design_vec(design)
    st_src = 'given'
    if state0 is None:
        state0, st_src = _state0_from_bank(mdl, dvec)
    s = {k: float(state0.get(k, float('nan'))) for k in STATE_KEYS}
    if not np.isfinite(s['v_terminal']):
        raise ValueError('state0.v_terminal 필요')
    s['i_norm'], s['phase_cc'] = c_rate, 1.0
    rng = np.random.default_rng(seed)
    ti_cc = {t_: i for i, t_ in enumerate(cc.tgt_names)}
    ti_cv = {t_: i for i, t_ in enumerate(cvm.tgt_names)} if cvm is not None else None
    x_mean0 = s['x_mean']
    t = float(state0.get('t', 0.0))
    Mn = cc.n_members
    cumV_m = np.full(Mn, s['v_terminal'])
    var_v = alea2 = band_lin = 0.0
    curve = {k: [] for k in ('t', 'V', 'band_mV', 'x_mean', 'x_surf_p50', 'p_cut',
                             'i_norm', 'phase', 'delivered')}
    anchors, trans_new = [], []
    n_gate = step = 0
    t_lo = t_hi = None
    end = 't_max'
    p = 0.0

    def _rec():
        curve['t'].append(t); curve['V'].append(s['v_terminal'])
        if band_mode == 'rss':
            b = math.sqrt(var_v + alea2)
        elif band_mode == 'sum':
            b = band_lin + math.sqrt(alea2)
        else:                                             # 'member' (기본): 멤버 누적경로 스프레드
            b = math.sqrt(float(np.std(cumV_m)) ** 2 + alea2)
        curve['band_mV'].append(b * 1e3)
        curve['x_mean'].append(s['x_mean']); curve['x_surf_p50'].append(s['x_surf_p50'])
        curve['p_cut'].append(p); curve['i_norm'].append(s['i_norm'])
        curve['phase'].append('CC' if s['phase_cc'] >= 0.5 else 'CV')
        curve['delivered'].append(abs(s['x_mean'] - x_mean0) / abs(win))
    _rec()
    while True:
        if (t_max is not None and t >= t_max) or step >= max_steps:
            end = 't_max' if (t_max is not None and t >= t_max) else 'max_steps'
            break
        in_cc = s['phase_cc'] >= 0.5
        com, ti = (cc, ti_cc) if in_cc else (cvm, ti_cv)
        X = _row(s, dvec, design, dt_s)
        mean, std, mem = (a[0] if a.ndim == 2 else a[:, 0, :] for a in com.predict(X))
        sdv = float(std[ti['d_v_terminal']])
        gate = (sdv * 1e3 > sigma_gate_mv) or \
               (anchor_every is not None and step > 0 and step % int(anchor_every) == 0)
        if gate:
            n_gate += 1
            if anchor_fn is not None:
                s_prev = dict(s)
                sa = anchor_fn({**s, 't': t}, design)     # 실솔버(외부) 1-스텝 앵커
                trans_new.append({'t': t, 'x_row': [float(v) for v in X],
                                  'dstate_true': {k: float(_f(sa.get(k)) - s_prev[k])
                                                  for k in STATE_KEYS},
                                  'note': 'anchor-transition (전개상태 기점; v2 재학습 입력)'})
                for k in STATE_KEYS:
                    if k in sa and np.isfinite(_f(sa[k])):
                        s[k] = float(sa[k])
                var_v = alea2 = band_lin = 0.0            # 실측 교체 → 불확실성 리셋
                cumV_m[:] = s['v_terminal']
                if len(anchors) < 1000:
                    anchors.append({'t': t, 'std_mV': sdv * 1e3, 'mode': 'replaced'})
                X = _row(s, dvec, design, dt_s)           # 앵커 후 이번 스텝 재예측
                mean, std, mem = (a[0] if a.ndim == 2 else a[:, 0, :] for a in com.predict(X))
                sdv = float(std[ti['d_v_terminal']])
            else:
                if len(anchors) < 1000:
                    anchors.append({'t': t, 'std_mV': sdv * 1e3, 'mode': 'ANCHOR-NEEDED',
                                    'state': {k: float(s[k]) for k in STATE_KEYS}})
                if not force:
                    end = 'anchor_needed_stop'
                    break
        i_before = s['i_norm']                            # 쿨롱은 스텝 시작 전류 (fwd Euler)
        for j, tn in enumerate(com.tgt_names):
            sk = _D2S.get(tn)
            if sk:
                s[sk] += float(mean[j])
        s['x_mean'] += i_before * dt_s / 3600.0 * win     # ★쿨롱 정확항 (학습 안 함)
        if not in_cc:
            s['v_terminal'] = v_cut                       # CV 정의: V 고정 (d_v≈0 학습치 대신 핀)
        # 밴드/멤버 경로 누적
        var_v += sdv * sdv
        band_lin += sdv
        alea2 += float(com.sres[ti['d_v_terminal']]) ** 2
        cumV_m = cumV_m + mem[:, ti['d_v_terminal']]
        nd = max(1, int(n_draw) // Mn)
        draws = cumV_m[:, None] + math.sqrt(alea2) * rng.standard_normal((Mn, nd))
        p = float(np.mean(draws < v_cut))
        t += dt_s
        step += 1
        _rec()
        deliv = abs(s['x_mean'] - x_mean0) / abs(win)
        if in_cc:
            if p >= 0.1 and t_lo is None:
                t_lo = t
            if p >= 0.9 and t_hi is None:
                t_hi = t
            if p >= 0.5:
                if cv_hold and cvm is not None:
                    s['phase_cc'], s['v_terminal'] = 0.0, v_cut
                    cumV_m[:] = v_cut
                else:
                    end = 'V_cutoff(p>0.5)'
                    break
        elif abs(s['i_norm']) <= i_cut_frac:
            end = 'cv_i_cut'
            break
        if deliv >= 1.0:
            end = 'soc_window'
            break
    # 불확실 종료창 [t_lo, t_hi] → delivered (lo, hi)
    ta, da = np.asarray(curve['t']), np.asarray(curve['delivered'])
    d_end = float(da[-1])
    d_lo = float(np.interp(t_lo, ta, da)) if t_lo is not None else d_end
    d_hi = float(np.interp(t_hi, ta, da)) if t_hi is not None else d_end
    nsteps = max(step, 1)
    return {'label': F1_LABEL, 'schema': SCHEMA_VERSION, 'curve': curve, 'anchors': anchors,
            'n_gate': n_gate, 'anchor_need_frac': n_gate / nsteps, 'end_reason': end,
            'delivered_frac': (d_end, min(d_lo, d_hi), max(d_lo, d_hi)),
            'cutoff_window_s': (t_lo, t_hi), 'transitions_new': trans_new,
            'state0_source': st_src, 'state0_used': {k: float(state0.get(k, float('nan')))
                                                     for k in STATE_KEYS},
            'band_mode': band_mode + ' (위원회-휴리스틱 밴드 — UNCALIBRATED)'}


def make_anchor_fn_cli(cmd_template):
    """v1 앵커 어댑터(프로세스 경계, 느슨한 결합): 외부 실솔버 1-스텝 호출 커맨드 템플릿 → anchor_fn.
    규약: 템플릿의 {t},{v_terminal},{x_mean},… 는 state/design 값으로 format; 커맨드는 stdout
    마지막 JSON 줄에 갱신 state(STATE_KEYS 부분집합)를 출력.  v2 에서 step4_dyn on_step 라이브
    훅으로 대체 (§8)."""
    def fn(state, design):
        cmd = cmd_template.format(**{**design, **state})
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=24 * 3600)
        if r.returncode != 0:
            raise RuntimeError(f'anchor cmd 실패 rc={r.returncode}: {r.stderr[-300:]}')
        for line in reversed(r.stdout.strip().splitlines()):
            line = line.strip()
            if line.startswith('{'):
                upd = json.loads(line)
                return {**state, **upd}
        raise RuntimeError('anchor cmd stdout 에 JSON state 줄 없음 (규약: 마지막 줄 JSON)')
    return fn


# ───────────────────────────── § (4) 랭킹 ─────────────────────────────
def rank_candidates(model, designs, app='balanced', n_draw=256, metrics_norm=None,
                    seed=0, **prop_kw):
    """후보군 → 각자 propagate(force=True; 랭킹은 정성 허용) → per-후보 metric
    {delivered, v_mean, q_ohm_frac, anchor_need_frac} → scalarize(ml_design_loop 재사용,
    missing='penalize').  ★p_pick = Thompson식: 후보별 점수 draw(가우스 근사 — delivered/v_mean
    을 밴드·종료창 폭으로 샘플; ASSUMED) n_draw개 → argmax 빈도/n_draw = '이 후보가 최선일 확률'."""
    mdl = load_model(model) if isinstance(model, str) else model
    # s6_ 네임스페이스 우선 (ml_design_loop 의 σ-앱 'balanced' 등과 이름충돌 방지)
    app_key = f's6_{app}' if f's6_{app}' in APP_OBJECTIVES else \
        (app if app in APP_OBJECTIVES else 's6_balanced')
    rng = np.random.default_rng(seed)
    v_cut = float(prop_kw.get('v_cut', 3.0))
    rows = []
    for dsn in designs:
        res = propagate(mdl, dsn, force=True, seed=seed, **prop_kw)
        cur = res['curve']
        V, tt = np.asarray(cur['V']), np.asarray(cur['t'])
        v0 = float(V[0])
        _trapz = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz   # WSL numpy<2 호환 (repo 선례: pybamm_predictor)
        vmean = float(_trapz(V, tt) / max(tt[-1] - tt[0], 1e-9)) if len(V) > 1 else v0
        dmean, dlo, dhi = res['delivered_frac']
        st0 = res['state0_used']
        r0, rct, rf = st0.get('r0_eff'), st0.get('r_ct_eff'), st0.get('r_film_eff')
        q_ohm = None
        if all(np.isfinite(_f(v)) for v in (r0, rct, rf)) and (r0 + rct + rf) > 0:
            q_ohm = float(np.clip(r0 / (r0 + rct + rf), 0.0, 1.0))
        vspan = max(v0 - v_cut, 1e-9)
        met = {'delivered': float(np.clip(dmean, 0, 1)),
               'v_mean': float(np.clip((vmean - v_cut) / vspan, 0, 1)),
               'q_ohm_frac': q_ohm, 'anchor_need_frac': float(res['anchor_need_frac'])}
        if metrics_norm:
            met = metrics_norm(met, res)
        sd_del = max((dhi - dlo) / 2.0, 1e-6)             # 종료창 반폭 = delivered 불확실성 프록시
        sd_v = float(np.mean(cur['band_mV'])) * 1e-3 / vspan
        sc_mean = scalarize(met, app_key, missing='penalize')
        z1, z2 = rng.standard_normal(n_draw), rng.standard_normal(n_draw)
        draws = np.empty(n_draw)
        for i in range(n_draw):                           # Thompson draw (가우스 근사, ASSUMED)
            md = dict(met)
            md['delivered'] = float(np.clip(met['delivered'] + sd_del * z1[i], 0, 1))
            md['v_mean'] = float(np.clip(met['v_mean'] + sd_v * z2[i], 0, 1))
            draws[i] = scalarize(md, app_key, missing='penalize')
        rows.append({'design': dict(dsn), 'metrics': met, 'score_mean': float(sc_mean),
                     'score_std': float(draws.std()), '_draws': draws,
                     'anchor_need_frac': met['anchor_need_frac'],
                     'curve_summary': {'V0': v0, 'V_end': float(V[-1]),
                                       't_end_s': float(tt[-1]), 'delivered': dmean,
                                       'delivered_lo_hi': (dlo, dhi),
                                       'end_reason': res['end_reason'],
                                       'band_end_mV': float(cur['band_mV'][-1])},
                     'label': F1_LABEL})
    if rows:
        D = np.stack([r.pop('_draws') for r in rows])     # [n_cand, n_draw]
        win = np.argmax(D, axis=0)
        for i, r in enumerate(rows):
            r['p_pick'] = float(np.mean(win == i))
    rows.sort(key=lambda r: -r['score_mean'])
    return rows


def pick_next_anchor(ranked, budget=1):
    """능동학습 추천: p_pick 상위권(≥ max(0.1, 0.5·max_p)) 중 anchor_need_frac 최대 후보 =
    '실솔버 1런의 정보이득 최대 지점' (MLIP on-the-fly 의 DFT-호출 선택 대응).
    출력에 실행 커맨드 힌트(step4_dyn/킷 env) 동봉."""
    if not ranked:
        return []
    pmax = max(r.get('p_pick', 0.0) for r in ranked)
    pool = [r for r in ranked if r.get('p_pick', 0.0) >= max(0.1, 0.5 * pmax)] or ranked[:1]
    pool = sorted(pool, key=lambda r: -r.get('anchor_need_frac', 0.0))[:max(int(budget), 1)]
    out = []
    for r in pool:
        d = r['design']
        hint = ('python3 scripts/step4_dyn.py --c-rate {c} --r-int-ohm-cm2 {r} --d-s {ds} '
                '--i0 {i0} --ocp-csv <OCP> --params-json <PARAMS> --out <NPZ>  '
                '(킷 env: MPM_S4_RATE/MPM_S4_RINT/MPM_S4_DS/MPM_S4_I0 대응)').format(
            c=d.get('c_rate', '?'), r=d.get('r_int_ohm_cm2', '?'),
            ds=d.get('d_s_m2s', '?'), i0=d.get('i0_A_m2', '?'))
        out.append({'design': d, 'p_pick': r.get('p_pick'), 'score_mean': r.get('score_mean'),
                    'anchor_need_frac': r.get('anchor_need_frac'), 'cmd_hint': hint,
                    'label': F1_LABEL})
    return out


# ───────────────────────────── § (5) 검증 (합성 RC-방전 ODE) ─────────────────────────────
# TEST-ONLY (§F1: 물리값 아님) — 2-상태 모델: dsoc̄/dt=i/3600 (정확 쿨롱);
# dsoc_s/dt=(soc̄−soc_s)/τ + k_c·i/3600 (표면 지연, k_c=1.6 표면 선행);
# V = 4.2 − 0.9·soc_s − R·i·areal·1e-3 − 0.03·asinh(i/i0)  (옴 + BV꼴).
_SYN = {'U0': 4.2, 'slope': 0.9, 'bkin': 0.03, 'kc': 1.6, 'x0': 0.264, 'x100': 0.9084,
        'r_p_um': 2.0, 'area_cm2': 1.0, 'asr_film': 5.0, 'v_cut': 3.3}


def _synth_design(rng):
    tau = float(rng.uniform(80.0, 400.0))
    areal = float(rng.uniform(2.0, 4.5))
    return {'c_rate': float(rng.choice([0.5, 1.0, 1.5])),
            'r_int_ohm_cm2': float(rng.uniform(15.0, 55.0)),
            'areal_mAh_cm2': areal,
            'i0_A_m2': float(rng.uniform(0.5, 5.0)),
            'd_s_m2s': (_SYN['r_p_um'] * 1e-6) ** 2 / tau,      # τ_w=r²/D_s = τ (basis 정합)
            'x0': _SYN['x0'], 'x100': _SYN['x100'], 'r_p_um': _SYN['r_p_um'],
            'asr_film': _SYN['asr_film'], 'temp_k': 298.15,
            'area_cm2': _SYN['area_cm2'], 'thickness_um': 18.0 * areal}


def _syn_V(socs, i, dsn, rng=None, noise=0.0):
    v = (_SYN['U0'] - _SYN['slope'] * socs
         - dsn['r_int_ohm_cm2'] * i * dsn['areal_mAh_cm2'] * 1e-3
         - _SYN['bkin'] * math.asinh(i / dsn['i0_A_m2']))
    if noise > 0.0 and rng is not None:
        v += noise * rng.standard_normal()
    return v


def _synth_run(dsn, seed=0, noise=2e-4, dt_fix=None, cv_hold=False, v_cut=None, t_cap=3e4):
    """합성 ODE 를 실 npz 와 같은 필드명으로 dict 생성 (추출기 공유 — TEST-ONLY §F1)."""
    rng = np.random.default_rng(seed)
    v_cut = _SYN['v_cut'] if v_cut is None else v_cut
    tau = (_SYN['r_p_um'] * 1e-6) ** 2 / dsn['d_s_m2s']
    c, i0 = dsn['c_rate'], dsn['i0_A_m2']
    area = _SYN['area_cm2']
    i_1c = dsn['areal_mAh_cm2'] * 1e-3 * area             # A (1C 전류)
    win = _SYN['x100'] - _SYN['x0']
    R_abs, asr = dsn['r_int_ohm_cm2'] / area, _SYN['asr_film'] / area
    rows = {k: [] for k in ('t', 'V_terminal', 'I', 'x_mean', 'x_surf_p05', 'x_surf_p50',
                            'x_surf_p95', 'eta_kin_mean', 'eta_diff_mean', 'Q_ohm_e_W',
                            'Q_ohm_i_W', 'Q_ct_W', 'Q_film_W', 'newton_resid', 'kcl_rel',
                            'energy_balance_rel')}
    soc = socs = 0.0
    t, kdt, i, phase = 0.0, 0, c, 'cc'
    end = 't_cap'
    while t < t_cap:
        if phase == 'cv':                                 # V=v_cut 유지 전류 (이분법)
            lo, hi = 0.0, i
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if _syn_V(socs, mid, dsn) > v_cut:
                    lo = mid
                else:
                    hi = mid
            i = 0.5 * (lo + hi)
        V = _syn_V(socs, i, dsn, rng, noise)
        I_A = i * i_1c
        spread = 0.5 * (_SYN['kc'] - 1.0) * i * tau / 3600.0
        rows['t'].append(t); rows['V_terminal'].append(V); rows['I'].append(I_A)
        rows['x_mean'].append(_SYN['x0'] + win * soc)
        rows['x_surf_p50'].append(_SYN['x0'] + win * socs)
        rows['x_surf_p05'].append(_SYN['x0'] + win * (socs - spread))
        rows['x_surf_p95'].append(_SYN['x0'] + win * (socs + spread))
        rows['eta_kin_mean'].append(_SYN['bkin'] * math.asinh(i / i0))
        rows['eta_diff_mean'].append(_SYN['slope'] * (socs - soc))
        rows['Q_ohm_e_W'].append(I_A * I_A * 0.7 * R_abs)
        rows['Q_ohm_i_W'].append(I_A * I_A * 0.3 * R_abs)
        rows['Q_ct_W'].append(abs(I_A) * rows['eta_kin_mean'][-1])
        rows['Q_film_W'].append(I_A * I_A * asr)
        rows['newton_resid'].append(1e-10 * (1.0 + rng.random()))
        rows['kcl_rel'].append(1e-9); rows['energy_balance_rel'].append(1e-9)
        if phase == 'cc' and V <= v_cut:
            if cv_hold:
                phase = 'cv'
            else:
                end = 'V_cutoff'
                break
        if phase == 'cv' and i <= 0.08:
            end = 'cv_i_cut'
            break
        if soc >= 1.0:
            end = 'soc_window'
            break
        dt = float(dt_fix) if dt_fix else (20.0 + 15.0 * (kdt % 3))   # 적응 dt 흉내
        soc += i * dt / 3600.0                            # 정확 쿨롱 (fwd Euler)
        socs += dt * ((soc - socs) / tau + _SYN['kc'] * i / 3600.0)
        t += dt
        kdt += 1
    params = {'c_rate': c, 'd_s': dsn['d_s_m2s'], 'i0': i0, 'asr_film': _SYN['asr_film'],
              'temp_k': 298.15, 'r_int_ohm_cm2': dsn['r_int_ohm_cm2'], 'cv_hold': cv_hold,
              'x0': _SYN['x0'], 'x100': _SYN['x100'], 'area_cm2': area,
              'areal_mAh_cm2': dsn['areal_mAh_cm2'], 'r_p_um': _SYN['r_p_um'],
              'thickness_um': dsn.get('thickness_um', 18.0 * dsn['areal_mAh_cm2']),
              'end_reason': end, 'test_only': True}
    d = {k: np.asarray(v, float) for k, v in rows.items()}
    d.update({'I_1C_A': i_1c, 'q_frac_at_cutoff': soc, 'params_json': json.dumps(params),
              '_path': f'synthetic-{seed}'})
    return d


def _synth_state_at(dsn, t_target, cv_hold=False, v_cut=None):
    """진짜 ODE 를 0→t_target 정밀 재적분 (dt=1s, noise=0) → state dict = 모의 실솔버 앵커."""
    v_cut = _SYN['v_cut'] if v_cut is None else v_cut
    tau = (_SYN['r_p_um'] * 1e-6) ** 2 / dsn['d_s_m2s']
    soc = socs = 0.0
    i = dsn['c_rate']
    t = 0.0
    while t < t_target - 1e-9:
        dt = min(1.0, t_target - t)
        soc += i * dt / 3600.0
        socs += dt * ((soc - socs) / tau + _SYN['kc'] * i / 3600.0)
        t += dt
    win = _SYN['x100'] - _SYN['x0']
    spread = 0.5 * (_SYN['kc'] - 1.0) * i * tau / 3600.0
    area = _SYN['area_cm2']
    return {'x_mean': _SYN['x0'] + win * soc, 'x_surf_p50': _SYN['x0'] + win * socs,
            'x_surf_p05': _SYN['x0'] + win * (socs - spread),
            'x_surf_p95': _SYN['x0'] + win * (socs + spread),
            'eta_kin_V': _SYN['bkin'] * math.asinh(i / dsn['i0_A_m2']),
            'eta_diff_V': _SYN['slope'] * (socs - soc),
            'v_terminal': _syn_V(socs, i, dsn), 'i_norm': i,
            'r0_eff': dsn['r_int_ohm_cm2'] / area,
            'r_ct_eff': _SYN['bkin'] * math.asinh(i / dsn['i0_A_m2'])
            / max(i * dsn['areal_mAh_cm2'] * 1e-3 * area, 1e-30),
            'r_film_eff': _SYN['asr_film'] / area, 'phase_cc': 1.0}


def _synthetic_rc_corpus(n_case=24, seed=0, n_cv=6):
    """합성 코퍼스 (TEST-ONLY §F1) + step3 join 모의맵.  n_cv 개는 CCCV(방전 CV-hold)."""
    rng = np.random.default_rng(seed)
    runs, s3map = [], {}
    for k in range(n_case):
        dsn = _synth_design(rng)
        r = _synth_run(dsn, seed=100 + k, cv_hold=(k < n_cv))
        runs.append(r)
        s3map[f'synthetic-{100 + k}'] = {'sigma_e_eff_S_cm': float(rng.uniform(1, 4)),
                                         'sigma_ion_eff_S_cm': float(rng.uniform(1e-4, 4e-4)),
                                         'r_p_um': _SYN['r_p_um']}
    return runs, s3map


def _selftest():
    print(F1_LABEL)
    print('=== step6_surrogate selftest (합성 RC-방전 ODE — TEST-ONLY §F1) ===')
    fails = []
    rng = np.random.default_rng(3)

    # ① 추출기: 스키마·쿨롱 검산·phase 분리
    runs, s3map = _synthetic_rc_corpus(n_case=24, seed=0, n_cv=6)
    data = extract_transitions(runs, step3_map=s3map, verbose=False)
    ncc, ncv = data['X_cc'].shape[0], data['X_cv'].shape[0]
    if data['X_cc'].shape[1] != len(FEAT_NAMES) or ncc < 300:
        fails.append(f'① X_cc 스키마/규모 이상 {data["X_cc"].shape}')
    if ncv < 30 or data['Y_cv'].shape[1] != len(DELTA_TARGETS_CV):
        fails.append(f'① CV 전이쌍 이상 {data["X_cv"].shape}')
    if data['excluded']:
        fails.append(f'① 쿨롱/스키마 예기치 못한 제외 {data["excluded"][:2]}')
    tot_pairs = sum(len(load_step4_npz(r)['t']) - 1 for r in runs)
    n_cvruns = sum(1 for r in runs if json.loads(r['params_json'])['cv_hold']
                   and json.loads(r['params_json'])['end_reason'] == 'cv_i_cut')
    if ncc + ncv != tot_pairs - n_cvruns:                 # phase 경계쌍 = CCCV 런당 1개 제외
        fails.append(f'① phase 경계 제외 수 불일치 {ncc + ncv} ≠ {tot_pairs}−{n_cvruns}')
    if 'label' not in data:
        fails.append('① extract 반환에 F1 라벨 없음')
    print(f'① 추출기: CC {ncc} + CV {ncv} 전이쌍, phase 경계 {n_cvruns}쌍 제외, '
          f'쿨롱 검산 통과(제외 0)  {"OK" if not fails else "…"}')

    # ② 위원회 학습 + LOCO (런 단위 — random-split 은 보고 금지 확인용으로만 계산)
    mdl = train_from_corpus(runs, step3_map=s3map, seed=0, loco=True, verbose=True)
    loco = mdl['loco']['per_target']
    r2v = loco['d_v_terminal']
    if r2v < 0.9:
        fails.append(f'② LOCO R²(d_v)={r2v:.4f} < 0.9')
    idx = rng.permutation(ncc)                            # random-split (보고 금지 — 편향 데모)
    tr, te = idx[: int(0.8 * ncc)], idx[int(0.8 * ncc):]
    ctmp = RidgeCommittee(seed=5)
    ctmp.fit(data['X_cc'][tr], data['Y_cc'][tr], data['feat_names'], data['tgt_cc'], verbose=False)
    pr = ctmp.predict(data['X_cc'][te])[0][:, 0]
    yy = data['Y_cc'][te][:, 0]
    r2_rand = 1 - ((yy - pr) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()
    if not (r2_rand >= r2v - 0.05):                       # 통상 rand ≥ LOCO (낙관) — 계산만
        print(f'  (참고: random-split {r2_rand:.4f} < LOCO {r2v:.4f} — 이 코퍼스는 역전)')
    if 'note' not in mdl['loco'] or 'random-split' not in mdl['loco']['note']:
        fails.append('② LOCO 반환에 보고규율 note 없음')
    print(f"② 위원회: LOCO R²(d_v)={r2v:.4f} (>0.9), d_x_surf_p50={loco['d_x_surf_p50']:.4f} · "
          f'random-split={r2_rand:.4f}=계산만(보고 금지 규율)  OK')

    # ③ 전개: held-out 설계 전곡선 — 밴드(기본 'member')가 진실을 ≥68% 덮는지 (밴드 정합성)
    #    + 'rss' 독립가정의 과소커버 실증 (자기회귀 상관 — 설계서 ★ASSUMED 경고의 empirical 증거)
    ho = {'c_rate': 1.0, 'r_int_ohm_cm2': 40.0, 'areal_mAh_cm2': 3.0, 'i0_A_m2': 2.0,
          'd_s_m2s': (_SYN['r_p_um'] * 1e-6) ** 2 / 250.0, 'x0': _SYN['x0'], 'x100': _SYN['x100'],
          'r_p_um': _SYN['r_p_um'], 'asr_film': _SYN['asr_film'], 'temp_k': 298.15,
          'area_cm2': 1.0, 'thickness_um': 54.0}
    truth = load_step4_npz(_synth_run(ho, seed=999, noise=0.0, dt_fix=30.0))
    Sx = _run_states(truth)
    st0 = dict(zip(STATE_KEYS, map(float, Sx[0])))
    prop = propagate(mdl, ho, state0=st0, dt_s=30.0, v_cut=_SYN['v_cut'],
                     sigma_gate_mv=1e9, seed=1)
    prop_rss = propagate(mdl, ho, state0=st0, dt_s=30.0, v_cut=_SYN['v_cut'],
                         sigma_gate_mv=1e9, seed=1, band_mode='rss')
    nmin = min(len(prop['curve']['V']), len(truth['V_terminal']))
    dv = np.abs(np.asarray(prop['curve']['V'][:nmin]) - truth['V_terminal'][:nmin])
    band = np.asarray(prop['curve']['band_mV'][:nmin]) * 1e-3
    band_r = np.asarray(prop_rss['curve']['band_mV'][:nmin]) * 1e-3
    cov = float(np.mean(dv <= band + 1e-12))
    cov_r = float(np.mean(dv <= band_r + 1e-12))
    if cov < 0.68:
        fails.append(f'③ 밴드(member) 커버리지 {cov:.2f} < 0.68')
    dend_t = abs(truth['q_frac_at_cutoff'])
    dend_s = prop['delivered_frac'][0]
    print(f'③ 전개(held-out): {nmin}스텝, |V_err| 중앙 {np.median(dv) * 1e3:.2f} mV, '
          f'밴드 커버리지 member {cov * 100:.0f}% (≥68) vs rss {cov_r * 100:.0f}% '
          f'(독립가정 과소 실증) · delivered sur {dend_s:.3f} vs 진실 {dend_t:.3f} · '
          f'종료 {prop["end_reason"]}  OK')

    # ④ σ_gate: 학습범위 밖 설계(R×5 + τ×8) → std 팽창 → ANCHOR-NEEDED + force=False 정지
    s_in = float(np.max([a['std_mV'] for a in prop['anchors']])) if prop['anchors'] else 0.0
    # in-dist 스텝 std 최대값을 직접 측정 (gate=∞ 였으므로 anchors 비어있음 → 재측정)
    Xin = np.stack([_row(dict(zip(STATE_KEYS, Sx[k])), _design_vec(ho), ho, 30.0)
                    for k in range(min(40, len(Sx)))])
    s_in = float(np.max(mdl['cc'].predict(Xin)[1][:, 0]) * 1e3)
    ood = dict(ho)
    ood['r_int_ohm_cm2'] *= 5.0                           # 학습범위 밖 (R×5; +τ×8 다축)
    ood['d_s_m2s'] /= 8.0
    ood.pop('log_tau_w', None)
    prop_ood0 = propagate(mdl, ood, dt_s=30.0, v_cut=_SYN['v_cut'], sigma_gate_mv=1e9,
                          force=True, seed=2, t_max=1800.0)
    s_ood = float(np.max([0.0] + [a['std_mV'] for a in prop_ood0['anchors']]))
    Xo = _row({k: float(prop_ood0['state0_used'][k]) for k in STATE_KEYS},
              _design_vec(ood), ood, 30.0)
    s_ood = max(s_ood, float(mdl['cc'].predict(Xo)[1][0, 0] * 1e3))
    if not (s_ood > 2.0 * s_in):
        fails.append(f'④ OOD std 팽창 부족: in {s_in:.3f} → ood {s_ood:.3f} mV')
    gate = 0.5 * (s_in + s_ood)
    prop_ood = propagate(mdl, ood, dt_s=30.0, v_cut=_SYN['v_cut'], sigma_gate_mv=gate,
                         force=False, seed=2)
    if prop_ood['end_reason'] != 'anchor_needed_stop' or \
            not any(a['mode'] == 'ANCHOR-NEEDED' for a in prop_ood['anchors']):
        fails.append(f'④ gate 미발동/미정지: {prop_ood["end_reason"]}')
    print(f'④ σ_gate: std in-dist {s_in:.3f} → OOD {s_ood:.3f} mV ({s_ood / max(s_in, 1e-12):.1f}×) '
          f'→ gate {gate:.3f} mV 발동 · force=False 정지({prop_ood["end_reason"]})  OK')

    # ⑤ anchor_fn(합성 ODE=모의 실솔버) → 앵커 교체 후 오차 감소 + transitions_new 축적
    truth_ood = load_step4_npz(_synth_run(ood, seed=777, noise=0.0, dt_fix=30.0))
    st0o = dict(zip(STATE_KEYS, map(float, _run_states(truth_ood)[0])))
    t_end = float(truth_ood['t'][-1])

    def _anchor(state, design):
        return _synth_state_at(design, state['t'])
    pf = propagate(mdl, ood, state0=st0o, dt_s=30.0, v_cut=_SYN['v_cut'], sigma_gate_mv=gate,
                   force=True, seed=3, t_max=t_end)
    pa = propagate(mdl, ood, state0=st0o, dt_s=30.0, v_cut=_SYN['v_cut'], sigma_gate_mv=gate,
                   anchor_fn=_anchor, seed=3, t_max=t_end)
    def _verr(pp):
        nm = min(len(pp['curve']['V']), len(truth_ood['V_terminal']))
        return float(np.mean(np.abs(np.asarray(pp['curve']['V'][:nm])
                                    - truth_ood['V_terminal'][:nm])))
    ef, ea = _verr(pf), _verr(pa)
    if not (ea < ef):
        fails.append(f'⑤ 앵커 후 오차 미감소: force {ef * 1e3:.2f} vs anchor {ea * 1e3:.2f} mV')
    if not pa['transitions_new']:
        fails.append('⑤ transitions_new 버퍼 비어있음')
    # CLI 앵커 어댑터 규약 (마지막 줄 JSON) 스모크
    afn = make_anchor_fn_cli('python3 -c "import json;print(json.dumps({{\'v_terminal\':3.7}}))"')
    if abs(afn({'v_terminal': 3.5, 't': 0.0}, {})['v_terminal'] - 3.7) > 1e-12:
        fails.append('⑤ make_anchor_fn_cli JSON 규약 실패')
    print(f'⑤ 앵커: mean|V_err| force {ef * 1e3:.2f} → anchor {ea * 1e3:.2f} mV '
          f'({len(pa["anchors"])}회 교체, 버퍼 {len(pa["transitions_new"])}쌍) · CLI 어댑터 OK')

    # ⑥ rank: 저-R 후보 p_pick 최대 · Σp_pick≈1 · scalarize 방향
    cands = []
    for Rv in (20.0, 35.0, 50.0):
        c = dict(ho)
        c['r_int_ohm_cm2'] = Rv
        cands.append(c)
    ranked = rank_candidates(mdl, cands, app='balanced', n_draw=256, seed=4,
                             dt_s=30.0, v_cut=_SYN['v_cut'], sigma_gate_mv=1e9)
    psum = sum(r['p_pick'] for r in ranked)
    if abs(psum - 1.0) > 1e-9:
        fails.append(f'⑥ Σp_pick={psum} ≠ 1')
    if ranked[0]['design']['r_int_ohm_cm2'] != 20.0 or \
            ranked[0]['p_pick'] != max(r['p_pick'] for r in ranked):
        fails.append(f"⑥ 저-R 후보 미선두: {[r['design']['r_int_ohm_cm2'] for r in ranked]}")
    scs = [r['score_mean'] for r in sorted(ranked, key=lambda r: r['design']['r_int_ohm_cm2'])]
    if not (scs[0] > scs[1] > scs[2]):
        fails.append(f'⑥ scalarize 방향(저-R 우위) 위반 {scs}')
    picks = pick_next_anchor(ranked, budget=1)
    if not (picks and 'cmd_hint' in picks[0]):
        fails.append('⑥ pick_next_anchor 이상')
    print(f"⑥ rank: R=20/35/50 → score {ranked[0]['score_mean']:.3f}/"
          f"{ranked[1]['score_mean']:.3f}/{ranked[2]['score_mean']:.3f}, "
          f"p_pick={[round(r['p_pick'], 3) for r in ranked]} (Σ=1, 저-R 선두) · "
          f'next-anchor 추천 1건  OK')

    # ⑦ §F1 라벨 + save/load 왕복 bitwise
    for nm, obj in (('extract', data), ('propagate', prop), ('rank[0]', ranked[0]),
                    ('loco', mdl['loco']), ('pick[0]', picks[0])):
        if obj.get('label') != F1_LABEL:
            fails.append(f'⑦ {nm} 반환에 F1 라벨 없음')
    sp = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'step6_model_selftest.npz')
    save_model(sp, mdl['cc'], mdl['cv'], mdl['bank_design'], mdl['bank_state'],
               extra_meta=mdl['meta'])
    m2 = load_model(sp)
    for att in ('W', 'mask', '_mu', '_sd', '_med', 'sres'):
        if not np.array_equal(getattr(mdl['cc'], att), getattr(m2['cc'], att)):
            fails.append(f'⑦ save/load cc.{att} bitwise 불일치')
    if m2['cv'] is None or not np.array_equal(mdl['cv'].W, m2['cv'].W):
        fails.append('⑦ save/load cv 불일치')
    try:                                                  # 스키마 불일치 → 명시 에러 확인
        b = dict(np.load(sp, allow_pickle=False))
        b['meta_json'] = np.array(json.dumps({'schema': 'step6-v0', 'has_cv': False}))
        np.savez(sp + '.bad.npz', **b)
        load_model(sp + '.bad.npz')
        fails.append('⑦ 스키마 불일치 미검출')
    except ValueError:
        pass
    prop2 = propagate(m2, ho, state0=st0, dt_s=30.0, v_cut=_SYN['v_cut'],
                      sigma_gate_mv=1e9, seed=1)
    if prop2['curve']['V'] != prop['curve']['V']:
        fails.append('⑦ 로드 모델 전개 불일치')
    os.remove(sp); os.remove(sp + '.bad.npz')
    print('⑦ §F1 라벨 전 반환 확인 + save/load bitwise 왕복 + 스키마 가드 + 로드-전개 동일  OK')

    # ⑧ SkCommittee import-guard graceful (클라우드)
    sk = SkCommittee(seed=0)
    rsk = sk.fit(data['X_cc'][:50], data['Y_cc'][:50], data['feat_names'], data['tgt_cc'],
                 verbose=False)
    try:
        import sklearn  # noqa: F401
        wsl = True
    except ImportError:
        wsl = False
    if wsl:
        if not rsk.get('ready'):
            fails.append(f'⑧ WSL sklearn 존재인데 fit 실패 {rsk}')
        print('⑧ [WSL] SkCommittee GBR 학습 OK')
    else:
        if rsk.get('ready') is not False or 'status' not in rsk:
            fails.append(f'⑧ import-guard 반환 규약 위반 {rsk}')
        print(f"⑧ [cloud] sklearn 부재 → import-guard graceful ✓ ({rsk['status'][:34]}…)")

    print('selftest OK (8/8)' if not fails else 'selftest FAIL:\n  ' + '\n  '.join(fails))
    return 1 if fails else 0


# ───────────────────────────── § (6) CLI ─────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(
        description='STEP6 MLIP식 전기화학 surrogate — train/propagate/rank/selftest')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--train', metavar='GLOB', help="step4 npz glob (예 'results/*/step4_*.npz')")
    ap.add_argument('--step3-json', action='append', default=[], metavar='CASE=PATH',
                    help='STEP3 join: 케이스(경로 부분일치)=mpm_payload.json (반복 가능)')
    ap.add_argument('--out', help='모델 npz 출력 경로 (--train) / 결과 JSON (--propagate/--rank)')
    ap.add_argument('--sklearn', action='store_true', help='SkCommittee(GBR, WSL) 시도')
    ap.add_argument('--no-loco', action='store_true')
    ap.add_argument('--propagate', action='store_true')
    ap.add_argument('--model'); ap.add_argument('--design', help='설계 dict JSON 파일')
    ap.add_argument('--dt-s', type=float, default=30.0)
    ap.add_argument('--t-max', type=float)
    ap.add_argument('--v-cut', type=float, default=3.0)
    ap.add_argument('--cv-hold', action='store_true')
    ap.add_argument('--sigma-gate-mv', type=float, default=5.0)
    ap.add_argument('--anchor-cmd', help='실솔버 앵커 커맨드 템플릿 (마지막 줄 JSON state 규약)')
    ap.add_argument('--anchor-every', type=int)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--band-mode', choices=('member', 'rss', 'sum'), default='member',
                    help='밴드: member=멤버 누적경로 스프레드(기본) / rss=독립가정(과소) / sum=최보수')
    ap.add_argument('--rank', action='store_true')
    ap.add_argument('--candidates', help='설계 dict 리스트 JSON 파일')
    ap.add_argument('--app', default='balanced')
    ap.add_argument('--sobol', type=int, help='후보 Sobol 생성 개수 (--bounds 필요)')
    ap.add_argument('--bounds', help='{param:[lo,hi]} JSON (--sobol)')
    ap.add_argument('--n-draw', type=int, default=256)
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    print(F1_LABEL)                                       # 배너 첫 줄 규약
    if a.train:
        paths = sorted(_glob.glob(a.train))
        if not paths:
            ap.error(f'glob 매치 0: {a.train}')
        if not a.out:
            ap.error('--out MODEL.npz 필요')
        s3map = {}
        for kv in a.step3_json:
            k, _, v = kv.partition('=')
            s3map[k] = v
        mdl = train_from_corpus(paths, step3_map=s3map, use_sklearn=a.sklearn,
                                loco=not a.no_loco)
        save_model(a.out, mdl['cc'], mdl['cv'], mdl['bank_design'], mdl['bank_state'],
                   extra_meta=mdl['meta'])
        lc = (mdl['loco'] or {}).get('per_target', {})
        print(f"학습 완료: CC {mdl['meta']['n_cc']} / CV {mdl['meta']['n_cv']} 전이쌍, "
              f"제외 {len(mdl['meta']['excluded'])}런")
        if lc:
            print('  LOCO R² (런 단위 — random-split 보고 금지): '
                  + ', '.join(f'{k}={v:.3f}' for k, v in lc.items()))
        print(f'  저장: {a.out}')
        return 0
    if a.propagate:
        if not (a.model and a.design):
            ap.error('--model, --design 필요')
        design = json.load(open(a.design))
        anchor = make_anchor_fn_cli(a.anchor_cmd) if a.anchor_cmd else None
        res = propagate(a.model, design, dt_s=a.dt_s, t_max=a.t_max, v_cut=a.v_cut,
                        cv_hold=a.cv_hold, sigma_gate_mv=a.sigma_gate_mv, anchor_fn=anchor,
                        anchor_every=a.anchor_every, force=a.force, n_draw=a.n_draw,
                        band_mode=a.band_mode)
        d, lo, hi = res['delivered_frac']
        print(f"전개: {len(res['curve']['t'])}스텝 · 종료 {res['end_reason']} · "
              f"delivered {d * 100:.1f}% [{lo * 100:.1f}, {hi * 100:.1f}] · "
              f"gate 발동 {res['n_gate']}회 ({res['anchor_need_frac'] * 100:.0f}%) · "
              f"state0={res['state0_source']}")
        if res['end_reason'] == 'anchor_needed_stop':
            print('  ⚠ ANCHOR-NEEDED 정지 — 실솔버 앵커(--anchor-cmd) 또는 --force(정성 전용)')
        if a.out:
            json.dump(res, open(a.out, 'w'), default=float, ensure_ascii=False)
            print(f'  곡선 JSON: {a.out}')
        return 0
    if a.rank:
        if not a.model:
            ap.error('--model 필요')
        if a.candidates:
            cands = json.load(open(a.candidates))
        elif a.sobol and a.bounds:
            from ml_design_loop import sobol_doe          # 후보군 생성기 재사용
            bounds = {k: tuple(v) for k, v in json.load(open(a.bounds)).items()}
            cands = sobol_doe(bounds, a.sobol)
        else:
            ap.error('--candidates 또는 --sobol+--bounds 필요')
        ranked = rank_candidates(a.model, cands, app=a.app, n_draw=a.n_draw,
                                 dt_s=a.dt_s, v_cut=a.v_cut, sigma_gate_mv=a.sigma_gate_mv)
        for i, r in enumerate(ranked[:10]):
            print(f"#{i + 1} score {r['score_mean']:+.3f}±{r['score_std']:.3f} "
                  f"p_pick {r['p_pick']:.2f} anchor-need {r['anchor_need_frac'] * 100:.0f}% "
                  f"delivered {r['metrics']['delivered'] * 100:.0f}% — {r['design']}")
        for pk in pick_next_anchor(ranked, budget=1):
            print(f"next-anchor 추천: p_pick {pk['p_pick']:.2f} · {pk['cmd_hint']}")
        if a.out:
            json.dump(ranked, open(a.out, 'w'), default=float, ensure_ascii=False)
            print(f'  랭킹 JSON: {a.out}')
        return 0
    ap.print_help()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
