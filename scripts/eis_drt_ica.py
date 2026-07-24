#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3-1 — 물리-기반 EIS + DRT + ICA(dQ/dV) + CV  (STEP4 확장, sulfide ASSB 반쪽셀).

frame[4]: 우리 STEP3/STEP4 물리에서 **등가회로 각 소자를 유도**해 EIS Z(ω)를 산출 → 실험 EIS
(eis_fit.py 가 CNLS 로 R0-p(R1,CPE1)-Wo1 피팅)와 **같은 회로**라 직접 대조 = frame[4] 교차검증.

회로 (eis_fit 정합):  Z(ω) = R0 + R_ct/(1 + jω·R_ct·C_dl) + Z_Wo(ω)
  · R0   = 직렬/옴 = L/σ_ion + L/σ_e + R_int      ← STEP3 σ-삼중 + 집전체 앵커
  · R_ct = 전하전달 = RT/(F·i0·(α_a+α_c)·a_spec)  ← STEP4 BV 선형화 (i0·반응면)
  · C_dl = 이중층 = c_dl_int · a_spec              ← ★앵커(실험 EIS CPE 또는 문헌 µF/cm²; §F1)
  · Z_Wo = 확산 = R_w·coth(√(jωτ))/√(jωτ), τ=r_p²/D_s  ← STEP4 구형 고체확산(Warburg 공짜)

★정직(§F1): C_dl 은 STEP4 방전솔브가 명시적으로 범위 밖(시간상수 ~ms ≪ dt)이라 EIS 전용으로
여기서 추가 — **크기는 앵커 필요**(실험 EIS 의 CPE1_Q 또는 sulfide|NMC 문헌 ~1-10 µF/cm²).  R_w 은
구형-Warburg DC 저항의 물리 추정(dU/dx·r/(F·c_max·D·a) O(1) 인자 = ASSUMED-FORM) — 실험 Wo1_R 로
교체 가능.  **모양(주파수 위치)은 우리 물리(τ=r²/D, ω_ct=1/R_ct C_dl)가 결정 = 예측력.**

DRT: Z 의 Tikhonov 역변환 → γ(τ) 분포 (R_ct/C_dl/Warburg/GB 시상수 분리, 모델-자유).
ICA: 방전 V(t)/Q(t) → dQ/dV (OCP 상전이 피크).  CV: OCP + BV 동역학 → I(V) 스윕.
"""
from __future__ import annotations

import numpy as np

F = 96485.33212        # C/mol
R_GAS = 8.314462618    # J/mol/K


# ─────────────────────── 회로 소자 ───────────────────────
def warburg_open(freqs_hz, R_w, tau_s):
    """유한-공간(반사경계=삽입입자) Warburg 'Wo':  Z = R_w·coth(√(jωτ))/√(jωτ).
    고주파 → 45° Warburg(R_w/√); 저주파 → 용량성(입자 blocking).  eis_fit 'Wo1' 과 동일 형."""
    w = 2.0 * np.pi * np.asarray(freqs_hz, float)
    s = np.sqrt(1j * w * float(tau_s))
    s = np.where(np.abs(s) < 1e-9, 1e-9 + 0j, s)               # ω→0 특이 회피
    return float(R_w) * (1.0 / np.tanh(s)) / s                 # coth(s)/s — np.tanh 는 |s|→∞ 안정(→1)


def randles_eis(freqs_hz, R0, R_ct, C_dl, R_w, tau_w, R_int_arc=0.0, C_int=0.0):
    """Z(ω) = R0 + [R_int‖C_int 계면 arc] + R_ct/(1+jω R_ct C_dl) + Z_Wo.
    eis_fit R0-p(R1,CPE1)-Wo1 (CPE→이상 C) 정합 — 실험의 R1 arc = 집전체/계면 R_int.
    R_int_arc>0 & C_int>0 이면 계면 arc 로, C_int=0 이면 직렬(레거시).  단위: R Ω·cm², C F/cm²."""
    w = 2.0 * np.pi * np.asarray(freqs_hz, float)
    Z = float(R0) + float(R_ct) / (1.0 + 1j * w * float(R_ct) * float(C_dl)) \
        + warburg_open(freqs_hz, R_w, tau_w)
    if R_int_arc > 0.0:
        Z = Z + (float(R_int_arc) / (1.0 + 1j * w * float(R_int_arc) * float(C_int))
                 if C_int > 0.0 else float(R_int_arc))
    return Z


def physics_eis(freqs_hz, *, sigma_e_S_cm, sigma_ion_S_cm, thickness_um, r_int_ohm_cm2=0.0,
                i0_A_m2=2.0, a_spec=None, spec_area_cm2_cm3=None, porosity=None,
                am_vol_frac=None, coverage_frac=0.5,
                d_s_m2_s=3e-14, r_p_um=3.0, c_dl_uF_cm2=10.0, c_dl_areal_uF_cm2=None, dudx_V=None,
                c_max_mol_m3=63104.0, alpha_a=0.5, alpha_c=0.5, temp_k=298.15, r_w_ohm_cm2=None,
                r_int_mode='arc', c_int_uF_cm2=None):
    """우리 물리 파라미터 → EIS Z(ω) + 소자 dict.  각 소자 provenance 반환.
    a_spec = 반응면적/기하면적 [cm²/cm²].  없으면 spec_area_cm2_cm3·thickness 로 추정(구형 3φ/r)."""
    L_cm = float(thickness_um) * 1e-4
    T = float(temp_k)
    # R0 = HF 실축 절편(전자 벌크 + 집전체) + 전극 이온수송(분산 TL의 DC극한 R_ion/3).  ★리뷰#1: 전극
    #   L/σ_ion 을 전량 HF 직렬에 넣으면 실험 HF 절편(eis_fit R0=직렬/분리막/접촉)과 프레임 어긋나고 3×
    #   과대 → 다공전극 균일반응 TL DC극한 R_ion/3 만 직렬 기여(중간주파 45° feature 의 DC 한계).
    R_ion = L_cm / max(float(sigma_ion_S_cm), 1e-30)           # 전극 이온수송 전저항 (분산)
    R_e = L_cm / max(float(sigma_e_S_cm), 1e-30)
    # ★R_int 배치 (2026-07-24 물리정정): 실험(eis_fit)의 R_int 는 중간주파 **arc**(R1‖CPE1)지 HF 직렬
    #   절편이 아님 — 집전체/계면 접촉은 자기 이중층을 가진 계면.  직렬 배치는 "큰 오프셋+작은 arc"
    #   (실측은 "작은 오프셋~10 + 큰 arc~50")로 Nyquist 모양이 실험과 어긋났음.  기본 = arc 모드
    #   (r_int_mode='series' 레거시 유지).  DC 총저항은 두 모드 동일 (배치만 이동).
    R_int = max(float(r_int_ohm_cm2), 0.0)
    arc_int = (str(r_int_mode) == 'arc') and (R_int > 0.0)
    if arc_int:
        # 실험(eis_fit) R1‖CPE1 arc = 이 계면 arc (R1~24-79Ω 大 = 우리 R_int, ≠ 작은 BV R_ct).
        # → 🔬실험앵커의 Brug C_dl(c_dl_areal)이 이 C_int(계면 arc)를 앵커 (BV C_dl 아님).
        _cint = c_int_uF_cm2 if c_int_uF_cm2 is not None else c_dl_areal_uF_cm2
        C_int = (float(_cint) if _cint is not None else 100.0) * 1e-6   # F/cm²geo
        cint_src = (f'실험앵커 eis_fit CPE→Brug ≈{float(_cint):.0f} µF/cm²geo (계면 arc)' if _cint is not None
                    else 'ASSUMED 100 µF/cm²geo — 🔬실험앵커(CPE→Brug)로 교체 권장 §F1')
    else:
        C_int, cint_src = 0.0, ('직렬(레거시) — arc 권장' if R_int > 0 else 'R_int=0')
    R0_hf = R_e + (0.0 if arc_int else R_int)                 # HF 실축 절편 (arc 모드: 전자 벌크만)
    R_ion_tl_dc = R_ion / 3.0                                 # TL DC극한 (Newman 다공전극 균일반응)
    R0 = R0_hf + R_ion_tl_dc
    # a_spec (반응 계면 면적비): 직접 주거나, 비표면적×두께, 또는 구형 3·φ_AM·coverage/r 근사
    if a_spec is None:
        if spec_area_cm2_cm3 is not None:
            a_spec = float(spec_area_cm2_cm3) * L_cm
        else:                                                  # ★리뷰#3: φ_AM·coverage·3/r·L (φ_AM≠전고체,
            #   반응은 SE-덮인 AM 면만 = coverage) — 옛 (1−ε)전고체는 반응면 2-4× 과대→R_ct 과소.
            phi_solid = (1.0 - (float(porosity) / 100.0 if porosity and porosity > 1 else (porosity or 0.15)))
            phi_am = float(am_vol_frac) if am_vol_frac is not None else 0.75 * phi_solid  # AM≈75%고체(기본)
            a_spec = phi_am * float(coverage_frac) * (3.0 / (float(r_p_um) * 1e-4)) * L_cm
    a_spec = max(float(a_spec), 1e-6)
    # R_ct = RT/(F·i0·(αa+αc)·a_spec).  i0 A/m² → A/cm² (×1e-4)
    i0_cm2 = float(i0_A_m2) * 1e-4
    R_ct = R_GAS * T / (F * i0_cm2 * (float(alpha_a) + float(alpha_c)) * a_spec)
    # C_dl = 이중층.  기본 = c_dl_int(µF/cm²_계면) × 반응면적비 a_spec → F/cm²geo.
    #   ★실험앵커(c_dl_areal_uF_cm2)를 주면 총 이중층(µF/cm²_기하)을 직접 사용 = eis_fit CPE→Brug
    #   실측값(이미 총량이라 a_spec 곱 안 함); intrinsic 은 역산해 표시.  §F1: depressed arc(α낮음)라
    #   실측 C_dl 은 자릿수-앵커(셀간 40-80× 분산) — arc 주파수 f_ct 의 자릿수만 고정, 정밀앵커 아님.
    if (c_dl_areal_uF_cm2 is not None) and not arc_int:        # 직렬모드서만 실험앵커→BV C_dl (arc 모드는 C_int로 감)
        C_dl = float(c_dl_areal_uF_cm2) * 1e-6                  # F/cm²geo 직접 (실험 총 이중층)
        c_dl_int_eff = C_dl / a_spec * 1e6                      # 역산 intrinsic µF/cm²계면 (표시용)
        cdl_src = (f'실험앵커 eis_fit CPE→Brug ≈{float(c_dl_areal_uF_cm2):.0f} µF/cm²geo '
                   '(⚠α낮은 depressed arc → 자릿수 앵커, 정밀X)')
    else:
        C_dl = float(c_dl_uF_cm2) * 1e-6 * a_spec              # BV 이중층 (문헌 1-10 µF/cm²계면 × a_spec)
        c_dl_int_eff = float(c_dl_uF_cm2)
        cdl_src = ('BV arc — 문헌 µF/cm²계면 (실험앵커는 계면 arc C_int로; BV는 작은 sub-arc)' if arc_int
                   else '★앵커 µF/cm² (실험 EIS CPE 또는 sulfide|NMC 문헌 1-10) — §F1')
    # Warburg: τ = r²/D (구형 확산시간).  R_w = 물리추정 |dU/dx|·r/(F·c_max·D·a) 또는 입력
    r_m = float(r_p_um) * 1e-6
    tau_w = r_m ** 2 / max(float(d_s_m2_s), 1e-30)
    if r_w_ohm_cm2 is not None:
        R_w = float(r_w_ohm_cm2)
        rw_src = 'input (실험 Wo1_R 권장)'
    else:
        dudx = abs(float(dudx_V)) if dudx_V is not None else 0.5   # V/Δx (OCP 국소기울기; 기본 대략)
        # DC 구형-Warburg 저항 추정: |dU/dx|·r/(F·c_max·D·a_spec) — O(1) 인자 미정 = ASSUMED-FORM
        R_w = dudx * r_m / (F * float(c_max_mol_m3) * float(d_s_m2_s) * a_spec) * 1e4  # →Ω·cm² 스케일
        rw_src = 'ASSUMED-FORM (dU/dx·r/(F·c_max·D·a); O(1) 인자 미정 → 실험 Wo1_R 로 교체 권장)'
    Z = randles_eis(freqs_hz, R0, R_ct, C_dl, R_w, tau_w, R_int_arc=(R_int if arc_int else 0.0), C_int=C_int)
    f_int = (1.0 / (2 * np.pi * R_int * C_int)) if (arc_int and C_int > 0) else None
    elems = {'R0_ohm_cm2': R0, 'R0_hf_ohm_cm2': R0_hf, 'R_ion_tl_dc': R_ion_tl_dc, 'R_ion_full': R_ion,
             'R_e': R_e, 'R_int': R_int, 'R_int_mode': ('arc' if arc_int else 'series'),
             'C_int_uF_cm2': (C_int * 1e6 if arc_int else None), 'f_int_Hz': f_int,
             'R_dc_total_ohm_cm2': R0 + R_ct + R_w + (R_int if arc_int else 0.0),
             'R_ct_ohm_cm2': R_ct, 'C_dl_F_cm2': C_dl, 'C_dl_uF_cm2_int': c_dl_int_eff,
             'C_dl_uF_cm2_areal': C_dl * 1e6,
             'R_w_ohm_cm2': R_w, 'tau_w_s': tau_w, 'a_spec': a_spec, 'coverage_frac': float(coverage_frac),
             'f_ct_Hz': 1.0 / (2 * np.pi * R_ct * C_dl),
             'provenance': {'R0_hf': 'STEP3 σ_e (+직렬모드 R_int) — HF 절편, frame[4] 정합',
                            'R_ion_tl': 'STEP3 σ_ion 전극수송 TL DC극한 R_ion/3 (분산 feature)',
                            'R_int': ('집전체/계면 arc R‖C_int — 실험 R1(중간주파 arc) 정합; C_int=' + cint_src
                                      if arc_int else '직렬 절편 배치 (레거시); ' + cint_src),
                            'R_ct': '⚠STEP4 BV lin — i0 의존(i0 정량부재, 스윕전용 §F1)',
                            'C_dl': cdl_src,
                            'R_w': rw_src + '; ⚠D_s 도 미측정(스윕)',
                            'tau_w': 'r²/D_s (STEP4 구형확산) — ⚠D_s 미앵커',
                            'note': '★framing: 미세구조-emergent 는 주로 R0_hf(σ-triad); arc 주파수 f_ct 는 '
                                    'i0·c_dl(둘 다 미앵커)가 결정, Warburg 위치는 D_s(미측정) — "위치=예측력"은 '
                                    'σ-triad 한정, 동역학 위치는 앵커 대기(§F1).'}}
    return Z, elems


# ─────────────── 랩 EC-Lab PEIS 주파수 그리드 (full/sym cell .mps 설정) ───────────────
def lab_freq_grid(f_hi_hz=7.0e6, f_lo_hz=1.0e-2, per_decade=10):
    """랩 BioLogic VSP-300 PEIS 설정 그리드 (full_cell.mps·symmetric_cell.mps 2025):
    fi=7 MHz → ff=10 mHz, 10 pts/decade (로그), Va=5 mV(소신호 선형 — 우리 모델과 정합), E=0 vs OCV.
    → 실측과 **같은 주파수축** = frame[4] Nyquist/DRT 직접 겹침."""
    n = int(round((np.log10(f_hi_hz) - np.log10(f_lo_hz)) * per_decade)) + 1
    return np.logspace(np.log10(f_hi_hz), np.log10(f_lo_hz), max(n, 8))


# ─────────────── DRT 피크 → 물리 프로세스 배정 (hover 툴팁용) ───────────────
def assign_drt_peak(tau_s, elems=None):
    """DRT 피크 τ → 물리 프로세스 배정.  모델 소자(f_ct·τ_w·f_int)와 먼저 매칭(같은 물리서 유도 →
    정확), 실패 시 τ-band 휴리스틱.  반환 {process, label, detail} — 피크 위 hover 박스 내용."""
    tau_s = float(tau_s)
    if not (tau_s > 0):
        return {'process': 'na', 'label': '—', 'detail': ''}
    f = 1.0 / (2.0 * np.pi * tau_s)
    lt = np.log10(tau_s)
    if elems:
        f_ct = elems.get('f_ct_Hz'); tau_w = elems.get('tau_w_s'); f_int = elems.get('f_int_Hz')
        if f_ct and f_ct > 0 and abs(lt - np.log10(1.0 / (2 * np.pi * f_ct))) < 0.55:
            return {'process': 'charge_transfer', 'label': '전하전달 R_ct (CAM|SE 계면)',
                    'detail': (f'BV 반응 + 이중층 C_dl.  f_ct≈{f_ct:.0f} Hz = 1/2πR_ct·C_dl.  '
                               '충·방전 계면 kinetics — σ_e/σ_ion 개선엔 둔감(i0·반응면적이 지배).  '
                               '사이클 열화 시 접촉손실→R_ct↑ = 이 피크 성장·저주파 이동.')}
        if f_int and f_int > 0 and abs(lt - np.log10(1.0 / (2 * np.pi * f_int))) < 0.55:
            return {'process': 'interface', 'label': '집전체|전극 계면 R_int',
                    'detail': (f'집전체 접촉/계면 arc.  f_int≈{f_int:.0f} Hz.  '
                               'aged(SBE/DBE 집전체)→R_int↑ = 열화 지문 (pristine 대비 접촉저항 증가).')}
        if tau_w and tau_w > 0 and abs(lt - np.log10(tau_w)) < 0.7:
            return {'process': 'diffusion', 'label': '고체확산 Warburg (AM 입자내 Li⁺)',
                    'detail': (f'AM 입자 반경방향 Li⁺ 확산.  τ_w=r²/D_s≈{tau_w:.0f} s.  ⚠D_s 미측정(스윕).  '
                               '방전 상전이/스테이징(OCP 평탄부)이 이 저주파 대역에 겹침 — ICA(dQ/dV)가 상전이를 분리.')}
    # τ-band 휴리스틱 (모델 매칭 실패)
    if tau_s < 1e-4:
        return {'process': 'hf', 'label': '고주파 (접촉·입계)',
                'detail': f'f≈{f:.1e} Hz — 입자접촉·입계(grain boundary)·잔류 인덕턴스 대역 (모델 R0 근방).'}
    if tau_s < 1e-1:
        return {'process': 'charge_transfer', 'label': '전하전달 대역',
                'detail': f'f≈{f:.0f} Hz — 계면 전하전달(R_ct∥C_dl) 유력.'}
    if tau_s < 3.0:
        return {'process': 'film', 'label': '계면필름·느린반응',
                'detail': f'f≈{f * 1000:.0f} mHz — 계면상(interphase)/필름 또는 느린 전하전달.'}
    return {'process': 'diffusion', 'label': '저주파 확산·상전이',
            'detail': f'f≈{f * 1000:.1f} mHz — 고체확산(Warburg) 또는 방전 상전이(스테이징).'}


# ─────────────────────── DRT (Tikhonov 역변환) ───────────────────────
def drt(freqs_hz, Z, tau_min=None, tau_max=None, n_tau=80, lam=1e-3, subtract_R0=True):
    """Z(ω) → γ(τ) 분포 (모델-자유 시상수 분리).  Z(ω)=R0+∫γ(τ)/(1+jωτ)dlnτ.
    Tikhonov(2차 미분 평활) + 비음수(NNLS).  반환 (tau_grid, gamma, R0_fit, Z_recon)."""
    from scipy.optimize import nnls
    w = 2.0 * np.pi * np.asarray(freqs_hz, float)
    Zc = np.asarray(Z, complex)
    R0 = float(np.real(Zc)[np.argmax(w)]) if subtract_R0 else 0.0   # 고주파 실수 = R0
    tmin = tau_min if tau_min else 1.0 / (10 * w.max())
    tmax = tau_max if tau_max else 10.0 / w.min()
    tau = np.logspace(np.log10(tmin), np.log10(tmax), int(n_tau))
    # 커널 A: Z_k = R0 + Σ_j γ_j /(1+jω_k τ_j)  → 실·허수 스택
    K = 1.0 / (1.0 + 1j * np.outer(w, tau))                    # [n_f, n_tau]
    A = np.vstack([K.real, K.imag])                           # [2 n_f, n_tau]
    b = np.concatenate([Zc.real - R0, Zc.imag])
    # Tikhonov 2차-미분 정규화 → 확대행렬 [A; √λ·D2] x ≈ [b; 0]
    D2 = (np.diag(np.ones(n_tau)) * -2 + np.diag(np.ones(n_tau - 1), 1) + np.diag(np.ones(n_tau - 1), -1))
    Aa = np.vstack([A, np.sqrt(float(lam)) * D2])
    bb = np.concatenate([b, np.zeros(n_tau)])
    gamma, _ = nnls(Aa, bb, maxiter=5000)                     # γ≥0 (물리적 분포)
    Z_recon = R0 + K @ gamma
    return tau, gamma, R0, Z_recon


def drt_peaks(tau, gamma, rel_height=0.05):
    """γ(τ) 피크 → (τ_peak, R_peak=∫γ dlnτ over basin) 리스트 (프로세스 분리 진단).
    ★리뷰#2: 프로세스 저항 = 피크 basin 전체의 ∫γ dlnτ (단일 빈 height×Δlnτ 아님 — R_ct ~8× 과소보고).
    basin = 인접 극소(minima) 사이 구간 (watershed)."""
    from scipy.signal import find_peaks
    g = np.asarray(gamma, float)
    ln_t = np.log(np.asarray(tau, float))
    dln = np.gradient(ln_t)
    if g.max() <= 0:
        return []
    idx, _ = find_peaks(g, height=rel_height * g.max())
    if len(idx) == 0:
        return []
    # 피크 사이 극소 = basin 경계 (양끝은 배열 끝).  각 피크 basin 에서 γ·dlnτ 적분.
    mins, _ = find_peaks(-g)
    bounds = np.concatenate([[0], mins, [len(g) - 1]])
    out = []
    for i in idx:
        lo = bounds[bounds <= i].max() if (bounds <= i).any() else 0
        hi = bounds[bounds >= i].min() if (bounds >= i).any() else len(g) - 1
        R = float(np.sum(g[lo:hi + 1] * dln[lo:hi + 1]))     # basin 적분 = 프로세스 저항
        out.append({'tau_s': float(tau[i]), 'f_Hz': float(1.0 / (2 * np.pi * tau[i])),
                    'R_ohm_cm2': R, 'gamma_peak': float(g[i]), 'basin': [int(lo), int(hi)]})
    return out


# ─────────────────────── ICA (dQ/dV) ───────────────────────
def ica_dqdv(V, Q, n_grid=400, smooth_V=0.005):
    """방전(또는 충전) V, Q → dQ/dV(V).  균일 V 격자 재보간 + 미분.  OCP 상전이 = 피크.
    V,Q 단조 구간 가정(방전=V↓·Q↑).  반환 (V_grid, dQdV, peaks)."""
    V = np.asarray(V, float); Q = np.asarray(Q, float)
    o = np.argsort(V)                                          # V 오름차순
    Vs, Qs = V[o], Q[o]
    keep = np.concatenate([[True], np.diff(Vs) > 1e-9])        # 중복 V 제거(보간 안정)
    Vs, Qs = Vs[keep], Qs[keep]
    if len(Vs) < 4:
        return np.array([]), np.array([]), []
    Vg = np.linspace(Vs.min() + smooth_V, Vs.max() - smooth_V, int(n_grid))
    Qg = np.interp(Vg, Vs, Qs)
    from scipy.signal import savgol_filter, find_peaks
    # ★리뷰#9: Savitzky-Golay 평활 = 미분 전 노이즈 억제 (안 하면 수치 wiggle 이 중복피크로 오검출).
    w = min(max(5, (int(n_grid) // 30) | 1), len(Qg) if len(Qg) % 2 else len(Qg) - 1)
    if w > 3:
        Qg = savgol_filter(Qg, w, 3)
    dQdV = np.gradient(Qg, Vg)
    a = np.abs(dQdV)
    idx, _ = (find_peaks(a, height=0.1 * a.max(), prominence=0.05 * a.max())
              if a.max() > 0 else (np.array([], int), None))
    peaks = [{'V': float(Vg[i]), 'dQdV': float(dQdV[i])} for i in idx]
    return Vg, dQdV, peaks


# ─────────────────────── CV (OCP + BV 동역학) ───────────────────────
def cv_curve(ocp_x, ocp_U, x0, x100, c_rate_equiv=None, scan_rate_mV_s=0.1, v_lo=3.0, v_hi=4.3,
             R_ct_ohm_cm2=5.0, cap_mAh_cm2=3.0, n=400):
    """CV(준평형 열역학 dQ/dV 스윕): 전압 v_lo↔v_hi 삼각 스윕, 각 V 에서 준평형 x(OCP 역함수) →
    I = (dQ/dV)·scan_rate·방향.  피크 = OCP 상전이.  ★리뷰#8: 동역학/옴 보정(−(V−U)/R_ct)은 미포함
    (R_ct_ohm_cm2 인자는 예약, 미사용) — 완전 동역학 CV 는 step4_dyn --cv-hold.  반환 (V, I_mA_cm2, x)."""
    ocp_x = np.asarray(ocp_x, float); ocp_U = np.asarray(ocp_U, float)
    ox = np.argsort(ocp_x); Xs, Us = ocp_x[ox], ocp_U[ox]     # x 오름차순 → OCP 기울기 dU/dx
    dUdx = np.gradient(Us, Xs)
    dUdx = np.where(np.abs(dUdx) < 1e-4, np.sign(dUdx + 1e-30) * 1e-4, dUdx)   # 평탄부 clip(dx/dV 폭주 방지)
    oU = np.argsort(Us); Us2, Xs2, dUdx2 = Us[oU], Xs[oU], dUdx[oU]            # U 단조(역보간용)
    keep = np.concatenate([[True], np.diff(Us2) > 1e-9]); Us2, Xs2, dUdx2 = Us2[keep], Xs2[keep], dUdx2[keep]
    nh = int(n) // 2                                          # 삼각파 스윕(up→down) + 방향 부호
    Vsweep = np.concatenate([np.linspace(v_lo, v_hi, nh), np.linspace(v_hi, v_lo, int(n) - nh)])
    direction = np.concatenate([np.ones(nh), -np.ones(int(n) - nh)])
    x_of_V = np.interp(Vsweep, Us2, Xs2)                      # V → 준평형 stoich (OCP 역함수)
    dxdV = 1.0 / np.interp(Vsweep, Us2, dUdx2)                # dx/dV = 1/(dU/dx)|_x(V)
    dQdx = float(cap_mAh_cm2) / (float(x100) - float(x0) + 1e-12)    # mAh/cm² per Δx
    sr = float(scan_rate_mV_s) * 1e-3                         # V/s
    I_cap = 3600.0 * dQdx * dxdV * sr * direction             # mAh/(cm²·s)→mA/cm² (×3600); 방향=스윕부호
    return Vsweep, I_cap, x_of_V


# ─────────────── 사이클-N EIS/DRT 궤적 (열화 기전 진단, D5) ───────────────
def rint_growth_mult(cycles, r0, rc, ntot, shape='sqrt', jump=0.5):
    """rint_cycle_traj r_of_n 형(양끝-고정 assumed-form) → 성장곱수 R_int(N)/R_int(0) (≥1).
    r0=pristine·rc=cycled(@N_total) 측정 끝점, shape∈{sqrt,linear}, jump=즉시-점프 분율.
    §F1: 끝점 측정, 사이 곡선 assumed-form (rint_cycle_traj.r_of_n 과 동일 법 → 일관)."""
    import math as _m
    r0 = max(float(r0), 1e-9); rc = float(rc); ntot = max(int(ntot), 1)
    out = []
    for n in cycles:
        if n <= 0:
            out.append(1.0); continue
        d = rc - r0
        g = _m.sqrt(n / ntot) if shape == 'sqrt' else (n / ntot)
        r = r0 + float(jump) * d + (1.0 - float(jump)) * d * g
        out.append(max(r / r0, 1.0))
    return out


def cycle_eis_trajectory(freqs_hz, base_elems, cycles, growth_mult,
                         rct_share=0.7, r0_share=0.2, rw_share=0.1):
    """사이클-N EIS/DRT 궤적 (열화 기전 진단, D5).  base(N=0) physics_eis 소자 dict + 사이클별 성장곱수
    growth_mult(=R_int(N)/R_int(0)≥1) → 각 N 의 Z(ω)+DRT.  총 성장 ΔR_dc(N)=(mult−1)·R_dc0 를
    arc(R_ct)/직렬(R0)/Warburg(R_w) 로 분배(★ASSUMED partition §F1; 기본 0.7/0.2/0.1 = 황화물 CAM|SE
    접촉손실 지배 = R_ct arc 주성장, Kang&Shin/Yun).  C_dl·τ_w 는 고정(성장=크기만; D_s 저하로 τ_w
    이동은 별도).  DRT 로 어느 시상수(R_ct arc vs 확산 vs 접촉)가 자라는지 = 기전 지문.
    반환 list[{N, mult, R0/R_ct/R_w/R_dc, f_ct, Z(복소 array), tau, gamma, peaks}]."""
    R0_0 = float(base_elems['R0_ohm_cm2']); Rct_0 = float(base_elems['R_ct_ohm_cm2'])
    Rw_0 = float(base_elems['R_w_ohm_cm2']); Cdl = float(base_elems['C_dl_F_cm2'])
    tau_w = float(base_elems['tau_w_s'])
    arc_mode = base_elems.get('R_int_mode') == 'arc'          # ★arc: 계면 성장이 R_int arc 로 (실측 접촉손실 지점)
    Rint_0 = float(base_elems.get('R_int', 0.0))
    C_int = float(base_elems.get('C_int_uF_cm2') or 0.0) * 1e-6    # 계면 arc 용량 (고정)
    R_e = float(base_elems.get('R_e', 0.0))                        # σ 전자직렬 = 비열화 floor
    # 열화-가능 base: 반응 arc(R_ct)+확산(R_w)+계면(arc면 R_int, 직렬이면 R0−R_e 근사 계면몫).
    #   σ-수송(R_e+R_ion/3)은 미세구조 고정 → 비열화 floor (성장서 제외).
    R_face0 = Rint_0 if arc_mode else max(R0_0 - R_e, 0.0)
    R_dc0 = max(Rct_0 + Rw_0 + R_face0, 1e-9)                     # fold 기준 (열화-가능 스케일)
    R0_floor = R0_0 if arc_mode else R_e                          # arc: R0 통째 floor; 직렬: R_e 만
    s = float(rct_share) + float(r0_share) + float(rw_share)
    _a, _b, _c = ((float(rct_share) / s, float(r0_share) / s, float(rw_share) / s)
                  if s > 0 else (1.0, 0.0, 0.0))
    # ★arc 모드: 지배 성장분(rct_share=0.7)은 **계면 arc R_int**(황화물 접촉손실 지점)로, r0_share 는 BV R_ct 로.
    #   직렬 모드: 원래대로 R_ct=rct_share, 계면(R0-몫)=r0_share.  (dominant share 를 물리 지배 arc 에 배정)
    face_s, rct_s, rw_s = (_a, _b, _c) if arc_mode else (_b, _a, _c)
    out = []
    for n, mult in zip(cycles, growth_mult):
        dR = max(float(mult) - 1.0, 0.0) * R_dc0              # 총 성장분 (mult≥1 → dR≥0)
        Rct_n, Rw_n = Rct_0 + rct_s * dR, Rw_0 + rw_s * dR
        Rface_n = R_face0 + face_s * dR                       # 계면(arc R_int 또는 직렬 R0-몫) 성장
        if arc_mode:
            R0_n, Rint_n = R0_floor, Rface_n
            Z = randles_eis(freqs_hz, R0_n, Rct_n, Cdl, Rw_n, tau_w, R_int_arc=Rint_n, C_int=C_int)
        else:
            R0_n, Rint_n = R0_floor + Rface_n, 0.0           # 직렬: 성장을 R0 에 합산
            Z = randles_eis(freqs_hz, R0_n, Rct_n, Cdl, Rw_n, tau_w)
        tau, g, _R0f, _Zr = drt(freqs_hz, Z)
        R_dc_n = R0_n + Rct_n + Rw_n + (Rint_n if arc_mode else 0.0)
        out.append({'N': int(n), 'mult': float(mult),
                    'R0_ohm_cm2': R0_n, 'R_ct_ohm_cm2': Rct_n, 'R_w_ohm_cm2': Rw_n,
                    'R_int_ohm_cm2': Rint_n, 'R_dc_ohm_cm2': R_dc_n,
                    'f_ct_Hz': 1.0 / (2 * np.pi * Rct_n * Cdl),
                    'Z': Z, 'tau': tau, 'gamma': g, 'peaks': drt_peaks(tau, g),
                    'shares': {'R_ct': rct_s, 'R_face': face_s, 'R_w': rw_s}})
    return out


# ─────────────── 발표/논문용 그림 (matplotlib, svg+png — 랩 figure format) ───────────────
_PAPER_BLUE_LO = (0.663, 0.784, 0.898)     # 연한 파랑 (series 시작 — 랩 예시 SOC-legend 스타일)
_PAPER_BLUE_HI = (0.086, 0.208, 0.365)     # 진한 남색 (series 끝)


def _paper_ax(ax):
    """랩/논문 figure format: 사방 box frame + 안쪽 tick(상·우 포함) + 작은 폰트."""
    for s in ax.spines.values():
        s.set_linewidth(0.8)
    ax.tick_params(direction='in', which='both', top=True, right=True, labelsize=8, length=3.5, width=0.8)
    ax.tick_params(which='minor', length=2.0, width=0.6)


def _paper_blue(i, n):
    """단일-색군 파랑 gradient (연함→진남색) — 랩 예시 DRT SOC-series 재현."""
    t = i / (n - 1) if n > 1 else 1.0
    return tuple(_PAPER_BLUE_LO[k] + (_PAPER_BLUE_HI[k] - _PAPER_BLUE_LO[k]) * t for k in range(3))


_LBL_ZRE = r"$Z'$ ($\Omega$ cm$^2$)"
_LBL_ZIM = r"$-Z''$ ($\Omega$ cm$^2$)"
_LBL_DRT_Y = r"$\gamma(\ln\tau)$ ($\Omega$ cm$^2$)"
_LBL_DRT_X = r"$\tau$ (s)"


def save_eis_figures(out_prefix, freqs, Z, elems, tau=None, gamma=None, peaks=None,
                     traj=None, fmt=('png', 'svg')):
    """발표/논문용 EIS 그림 — 랩 figure format 재현 (2026-07-24 사용자 예시): 흰 배경 · 사방 box frame ·
    안쪽 tick · **open-circle Nyquist**(Pristine/N=### 주석) · **단일-색군 blue-gradient DRT**(SOC-legend
    스타일) · mathtext 라벨 γ(lnτ)/τ/Z′/−Z″ (Ω cm²) — 한글 없음 = 폰트 tofu 無.  base = Nyquist+DRT
    2-패널; traj(사이클) 있으면 오버레이+R(N) 성장 3-패널 추가.  svg+png 동시(CSV 는 CLI 별도) = 랩 규약."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    saved = []
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.1))
    zre, zim = np.real(Z), -np.imag(Z)
    ax1.plot(zre, zim, 'o', ms=3.8, mfc='white', mec='#1f4e8c', mew=0.9)      # open circles (랩 예시 Nyquist)
    ax1.set_aspect('equal', adjustable='datalim')             # ★equal aspect (Nyquist 표준: arc=진짜 반원)
    ax1.set_xlabel(_LBL_ZRE, fontsize=9)
    ax1.set_ylabel(_LBL_ZIM, fontsize=9)
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    r0v = elems.get('R0_ohm_cm2')
    if r0v is not None:
        ax1.annotate(r'$R_0$', (r0v, 0), textcoords='offset points', xytext=(2, 5), fontsize=8, color='#666666')
    _paper_ax(ax1)
    if tau is not None and gamma is not None:
        ax2.plot(tau, gamma, '-', color=_paper_blue(1, 1), lw=1.2)
        ax2.set_xscale('log')
        ax2.set_xlabel(_LBL_DRT_X, fontsize=9)
        ax2.set_ylabel(_LBL_DRT_Y, fontsize=9)
        ax2.set_xlim(float(np.min(tau)), float(np.max(tau)))
        ax2.set_ylim(bottom=0)
    _paper_ax(ax2)
    fig.tight_layout()
    for f in fmt:
        fn = f'{out_prefix}_eis.{f}'; fig.savefig(fn, dpi=200, facecolor='white'); saved.append(fn)
    plt.close(fig)
    if traj:
        n = len(traj)
        fig2, (bx1, bx2, bx3) = plt.subplots(1, 3, figsize=(10.8, 3.2))
        for i, tr in enumerate(traj):
            c = _paper_blue(i, n)
            lab = 'Pristine' if tr['N'] == 0 else f"N = {tr['N']}"
            bx1.plot(np.real(tr['Z']), -np.imag(tr['Z']), 'o', ms=3.0, mfc='white', mec=c, mew=0.8)
            bx2.plot(tr['tau'], tr['gamma'], '-', color=c, lw=1.15, label=lab)
        # Nyquist = 텍스트 주석 (랩 예시 2: Pristine/500th Cycle 을 arc 정점 옆에), DRT = legend (예시 1)
        for i in sorted({0, n - 1}):
            tr = traj[i]
            zr_i, zi_i = np.real(tr['Z']), -np.imag(tr['Z'])
            k = int(np.argmax(zi_i))
            bx1.annotate('Pristine' if tr['N'] == 0 else f"N = {tr['N']}",
                         (zr_i[k], zi_i[k]), textcoords='offset points', xytext=(0, 7),
                         ha='center', fontsize=7.5, color=_paper_blue(i, n))
        bx1.set_aspect('equal', adjustable='datalim')         # ★equal aspect
        bx1.set_xlabel(_LBL_ZRE, fontsize=9); bx1.set_ylabel(_LBL_ZIM, fontsize=9)
        _zi_max = max(float(np.max(-np.imag(tr['Z']))) for tr in traj)
        bx1.set_xlim(left=0); bx1.set_ylim(0, _zi_max * 1.18)     # 주석(N=…) 머리공간

        bx2.set_xscale('log')
        bx2.set_xlabel(_LBL_DRT_X, fontsize=9); bx2.set_ylabel(_LBL_DRT_Y, fontsize=9)
        bx2.set_xlim(float(np.min(traj[0]['tau'])), float(np.max(traj[0]['tau'])))
        bx2.set_ylim(bottom=0)
        bx2.legend(fontsize=7, frameon=False, handlelength=1.2, labelspacing=0.3, loc='upper left')
        ns = [tr['N'] for tr in traj]
        for key, mk, c, lab in (('R_ct_ohm_cm2', 'o', '#c0392b', r'$R_{ct}$ (arc)'),
                                ('R0_ohm_cm2', 's', '#1f4e8c', r'$R_0$ (series)'),
                                ('R_w_ohm_cm2', '^', '#e08b3d', r'$R_W$ (diffusion)'),
                                ('R_dc_ohm_cm2', 'D', '#333333', r'$R_{DC}$ (total)')):
            bx3.plot(ns, [tr[key] for tr in traj], '-' + mk, color=c, lw=1.1, ms=4, mfc='white', mew=0.9, label=lab)
        bx3.set_xlabel('Cycle number', fontsize=9)
        bx3.set_ylabel(r'$R$ ($\Omega$ cm$^2$)', fontsize=9)
        bx3.legend(fontsize=7, frameon=False, loc='center right')
        bx3.text(0.97, 0.03, 'assumed-form partition', transform=bx3.transAxes,   # §F1 정직 라벨
                 ha='right', fontsize=6.5, color='#888888')
        for bx in (bx1, bx2, bx3):
            _paper_ax(bx)
        fig2.tight_layout()
        for f in fmt:
            fn = f'{out_prefix}_cycle.{f}'; fig2.savefig(fn, dpi=200, facecolor='white'); saved.append(fn)
        plt.close(fig2)
    return saved


# ─────────────────────── self-test ───────────────────────
def _selftest():
    fails = []
    freqs = np.logspace(5, -2, 60)                            # 100 kHz → 10 mHz
    # 1) Randles: 알려진 소자 → Nyquist 형상 (HF 실수=R0, arc, Warburg 꼬리)
    Z = randles_eis(freqs, R0=20.0, R_ct=40.0, C_dl=2e-5, R_w=30.0, tau_w=100.0)
    hf, lf = Z[np.argmax(freqs)], Z[np.argmin(freqs)]
    if not (abs(hf.real - 20.0) < 2.0 and abs(hf.imag) < 5.0):
        fails.append(f'HF 실수 R0≈20 실패: {hf:.2f}')
    if not (lf.real > 40.0 and lf.imag < -5.0):               # LF: Warburg 용량성 꼬리
        fails.append(f'LF Warburg 꼬리 실패: {lf:.2f}')
    # 2) physics_eis: 소자가 물리 파라미터로 유도되고 f_ct = 1/(2π R_ct C_dl)
    Zp, el = physics_eis(freqs, sigma_e_S_cm=2.0, sigma_ion_S_cm=2e-4, thickness_um=72.0,
                         r_int_ohm_cm2=50.0, i0_A_m2=2.0, porosity=8.0, r_p_um=3.0, d_s_m2_s=3e-14)
    if not (el['R0_ohm_cm2'] > el['R_e']):                    # R0 = R_e + R_ion/3 (arc 모드: R_int 은 별도 arc)
        fails.append('R0 이 R_e 보다 커야(이온 TL 추가)')
    if not (el.get('R_int_mode') == 'arc' and el.get('f_int_Hz') and el['f_int_Hz'] > 0):
        fails.append(f"R_int arc 모드/f_int 실패: mode={el.get('R_int_mode')} f_int={el.get('f_int_Hz')}")
    if not (el['tau_w_s'] > 0 and abs(el['tau_w_s'] - (3e-6) ** 2 / 3e-14) / el['tau_w_s'] < 1e-6):
        fails.append(f"τ_w=r²/D 불일치: {el['tau_w_s']:.3g}")
    if not (el['f_ct_Hz'] > 0):
        fails.append('f_ct 양수 아님')
    # 3) DRT: Randles(단일 arc) 역변환 → arc 시상수 τ=R_ct·C_dl 부근 피크 회복
    tau, g, R0f, Zr = drt(freqs, Z, n_tau=70, lam=1e-2)
    recon_err = np.linalg.norm(Zr - Z) / np.linalg.norm(Z)
    if recon_err > 0.15:
        fails.append(f'DRT 재구성 오차 큼: {recon_err:.3f}')
    pk = drt_peaks(tau, g)
    tau_ct = 40.0 * 2e-5                                      # R_ct·C_dl = 8e-4 s
    if not any(0.2 * tau_ct < p['tau_s'] < 5 * tau_ct for p in pk):
        _pts = ', '.join('%.1e' % p['tau_s'] for p in pk)
        fails.append(f'DRT 가 arc τ≈{tau_ct:.1e}s 피크 못 찾음: {_pts}')
    # 4) ICA: 2-스텝 합성 방전 Q(V) (V=3.5·3.9서 용량 계단) → dQ/dV 2 뚜렷 피크.  SG평활이 노이즈
    #   더블릿 억제하되 진짜 2피크는 보존해야 함(리뷰#9).
    Vt = np.linspace(3.0, 4.2, 300)
    Qt = 1.5 * (1.0 / (1 + np.exp((Vt - 3.5) / 0.03)) + 1.0 / (1 + np.exp((Vt - 3.9) / 0.03)))
    Qt = Qt + 0.002 * np.sin(Vt * 400)                       # 미세 노이즈 (평활 검증용)
    Vg, dq, pk2 = ica_dqdv(Vt, Qt)
    if not (len(pk2) == 2):                                  # 정확히 2 (노이즈 더블릿 없이)
        fails.append(f'ICA 2-스텝 피크 ≠2: {len(pk2)} @ V={[round(p["V"],2) for p in pk2]}')
    # 5) CV: OCP 스윕 → 유한 I, 상전이서 피크
    xoc = np.linspace(0.05, 0.95, 200)
    Uoc = 4.2 - 0.6 * xoc - 0.1 * np.tanh((xoc - 0.5) * 10)   # 단조감소 OCP (역보간 가능)
    Vc, Ic, xc = cv_curve(xoc, Uoc, 0.05, 0.95, scan_rate_mV_s=0.1)
    if not (len(Vc) and np.isfinite(Ic).all() and np.abs(Ic).max() > 0):
        fails.append('CV I(V) 유한/비영 실패')
    # 6) 사이클-N EIS 궤적 (D5): R_int 2× 성장(30→60 @1000) → R_dc 2×, R_ct 단조증가, arc 성장
    cyc = [0, 100, 500, 1000]
    mult = rint_growth_mult(cyc, r0=30.0, rc=60.0, ntot=1000)          # 2.0 at N_total
    traj = cycle_eis_trajectory(freqs, el, cyc, mult)
    if not (len(traj) == 4 and abs(traj[0]['mult'] - 1.0) < 1e-9 and traj[-1]['mult'] > 1.5):
        fails.append(f'cycle EIS mult 실패: {[round(t["mult"], 2) for t in traj]}')
    rct_seq = [t['R_ct_ohm_cm2'] for t in traj]
    if not all(rct_seq[i] <= rct_seq[i + 1] + 1e-9 for i in range(len(rct_seq) - 1)):
        fails.append(f'R_ct(N) 단조증가 실패: {[round(r, 2) for r in rct_seq]}')
    # 성장 총량 보존: ΔR_dc(N_total) == (mult−1)·R_dc0_degradable.
    #   arc 모드 degradable = R_ct + R_w + R_int(계면 arc); σ-floor(R0)은 비열화.
    R_deg0 = traj[0]['R_ct_ohm_cm2'] + traj[0]['R_w_ohm_cm2'] + traj[0]['R_int_ohm_cm2']
    added = traj[-1]['R_dc_ohm_cm2'] - traj[0]['R_dc_ohm_cm2']
    if not (abs(added - (traj[-1]['mult'] - 1.0) * R_deg0) < 1e-6):
        fails.append(f"성장 총량 보존 실패: Δ={added:.3f} vs (mult−1)·R_deg0={((traj[-1]['mult'] - 1.0) * R_deg0):.3f}")
    # arc 모드: 계면 R_int 이 단조 성장(접촉손실 지점)
    ri_seq = [t['R_int_ohm_cm2'] for t in traj]
    if not all(ri_seq[i] <= ri_seq[i + 1] + 1e-9 for i in range(len(ri_seq) - 1)):
        fails.append(f"R_int(N) 단조증가 실패: {[round(r, 1) for r in ri_seq]}")
    print('selftest OK' if not fails else 'selftest FAIL:\n  ' + '\n  '.join(fails))
    if not fails:
        print(f"  Randles: R0={hf.real:.1f} arc+Warburg → LF {lf.real:.1f}{lf.imag:+.1f}j Ω·cm²")
        print(f"  physics_eis: R0={el['R0_ohm_cm2']:.1f}(hf{el['R0_hf_ohm_cm2']:.1f}+ionTL{el['R_ion_tl_dc']:.1f}) "
              f"R_ct={el['R_ct_ohm_cm2']:.1f} C_dl={el['C_dl_F_cm2']*1e6:.1f}µF/cm² f_ct={el['f_ct_Hz']:.1f}Hz "
              f"R_w={el['R_w_ohm_cm2']:.2g} τ_w={el['tau_w_s']:.2g}s")
        print(f"  DRT: {len(pk)} 피크 (recon {recon_err*100:.1f}%), arc τ_ct≈{tau_ct:.1e}s")
        print(f"  ICA: {len(pk2)} 상전이 피크 @ V={[round(p['V'],2) for p in pk2]}")
        print(f"  CV: {len(Vc)}pt |I|max={np.abs(Ic).max():.3g} mA/cm²")
    return 1 if fails else 0


def _step3_params_from_metrics(m):
    """metrics dict(step3 최상위 또는 중첩) → physics_eis 입력 dict (σ-triad·두께·porosity·집전체).
    mpm_metrics.json 과 mpm_lab payload 의 mpm_metrics 둘 다 이 구조(step3 + thickness_mpm_um…)."""
    s3 = m.get('step3', m) or {}
    return {'sigma_e_S_cm': s3.get('sigma_e_eff_S_cm'), 'sigma_ion_S_cm': s3.get('sigma_ion_eff_S_cm'),
            'thickness_um': m.get('thickness_um') or m.get('thickness_mpm_um'),
            'porosity': m.get('porosity_mpm_pct') or m.get('porosity_settled_pct'),
            'r_int_ohm_cm2': (s3.get('collector_geometric') or {}).get('R_geom_ohm_cm2', 0.0)}


def _load_step3_params(metrics_json):
    """mpm_metrics.json(step3) 파일 → physics_eis 입력 dict."""
    import json
    return _step3_params_from_metrics(json.loads(open(metrics_json).read()))


def load_experimental_anchors(fits_dir=None):
    """실험 EIS(eis_fit) 피팅값 → physics_eis 앵커 dict (frame[4] — 문헌/ASSUMED-FORM 을 실측으로 교체).
    full-cell(R0-p(R1,CPE1)-Wo1) 로부터:
      · c_dl_areal_uF_cm2 = 셀별 CPE→Brug C_dl 의 GEOMETRIC MEAN (로그-분산 → 산술평균보다 대표적;
        ⚠ depressed arc α 낮아 셀간 40-80× 분산 → 자릿수 앵커, 정밀X)
      · r_w_ohm_cm2 = full-cell Wo1_R 의 MEDIAN (0=Warburg 미포착 셀 제외)
      · r_int_ohm_cm2 / r0_hf_ohm_cm2 = full-cell R1 / R_s 평균
    파일 없으면 None (클라우드/데이터 부재 시 graceful — 호출측이 문헌 기본값 유지)."""
    import csv
    import os
    import statistics as st
    if fits_dir is None:
        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fits_dir = os.path.join(_root, '이종기술', 'eis', 'fits')
    res = os.path.join(fits_dir, 'eis_fit_results.csv')
    if not os.path.isfile(res):
        return None
    cdl, rw, r1, rs = [], [], [], []
    try:
        for row in csv.DictReader(open(res)):
            if row.get('cell_type') != 'full':
                continue

            def _g(k):
                try:
                    return float(row.get(k, ''))
                except (TypeError, ValueError):
                    return None
            c, w, a1, s = _g('C_dl_uF_cm2'), _g('R_w_ohmcm2'), _g('R1_ohmcm2'), _g('R_s_ohmcm2')
            if c and c > 0:
                cdl.append(c)
            if w and w > 0:                                    # 0 = Warburg 미포착(1.3V 셀) 제외
                rw.append(w)
            if a1 and a1 > 0:
                r1.append(a1)
            if s and s > 0:
                rs.append(s)
    except Exception:
        return None
    if not cdl:
        return None
    geo = float(np.exp(np.mean(np.log(np.asarray(cdl, float)))))    # 기하평균 (로그-분산 대표값)
    return {
        'c_dl_areal_uF_cm2': round(geo, 1),
        'c_dl_range_uF_cm2': [round(min(cdl), 1), round(max(cdl), 1)],
        'r_w_ohm_cm2': (round(st.median(rw), 1) if rw else None),
        'r_int_ohm_cm2': (round(st.mean(r1), 1) if r1 else None),
        'r0_hf_ohm_cm2': (round(st.mean(rs), 1) if rs else None),
        'n_full': len(cdl),
        'provenance': {
            'C_dl': 'eis_fit CPE→Brug 기하평균 (⚠α낮은 depressed arc → 셀간 40-80× 분산 = 자릿수-앵커)',
            'R_w': 'eis_fit Wo1_R median (0=미포착 제외)',
            'R_int': 'eis_fit full-cell R1 평균 (SOC100)',
            'R0_hf': 'eis_fit full-cell R_s 평균 (HF 절편)',
            'note': 'frame[4] 실험앵커 — 실측 EIS 로 물리-EIS 소자 고정 (C_dl 자릿수·R_w 실측)'}}


def main(argv=None):
    import argparse
    import csv
    ap = argparse.ArgumentParser(description='v3-1 EIS/DRT/ICA/CV (물리-기반, sulfide ASSB)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--eis', action='store_true', help='EIS Nyquist + DRT 산출')
    ap.add_argument('--metrics', default='', help='mpm_metrics.json → σ-triad/두께/집전체 자동로드')
    ap.add_argument('--sigma-e', type=float, default=2.0); ap.add_argument('--sigma-ion', type=float, default=2e-4)
    ap.add_argument('--thickness-um', type=float, default=72.0); ap.add_argument('--r-int', type=float, default=0.0)
    ap.add_argument('--i0', type=float, default=2.0); ap.add_argument('--d-s', type=float, default=3e-14)
    ap.add_argument('--r-p-um', type=float, default=3.0); ap.add_argument('--porosity', type=float, default=8.0)
    ap.add_argument('--c-dl-uf', type=float, default=10.0, help='이중층 µF/cm² (★앵커: 실험 EIS CPE 또는 문헌 1-10)')
    ap.add_argument('--use-exp-anchors', action='store_true',
                    help='실험 EIS(eis_fit) 로 C_dl(CPE→Brug)·R_w(Wo1_R) 앵커 = frame[4] (데이터 있으면)')
    ap.add_argument('--cycle-traj', default='',
                    help='사이클-N EIS/DRT 궤적(D5): "r0,rc,ntot[,shape,jump]" R_int 끝점 (예 50,125,1000)')
    ap.add_argument('--cycle-ns', default='0,50,100,300,500,1000', help='궤적 N 목록(쉼표)')
    ap.add_argument('--cycle-shares', default='0.7,0.2,0.1', help='성장 분배 R_ct,R0,R_w (ASSUMED §F1)')
    ap.add_argument('--fig', action='store_true', help='발표/논문용 그림 저장 (matplotlib png+svg; Nyquist+DRT[+사이클])')
    ap.add_argument('--f-hi', type=float, default=1e5); ap.add_argument('--f-lo', type=float, default=1e-2)
    ap.add_argument('--ica', default='', help='방전곡선 CSV(V,Q 열) → dQ/dV')
    ap.add_argument('--out', default='eis_out')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.ica:
        import numpy as _np
        d = _np.genfromtxt(a.ica, delimiter=',', names=True)
        V = d[d.dtype.names[0]]; Q = d[d.dtype.names[1]]
        Vg, dq, pk = ica_dqdv(V, Q)
        with open(a.out + '_ica.csv', 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['V', 'dQdV']); w.writerows(zip(Vg, dq))
        print(f'ICA → {a.out}_ica.csv  ({len(pk)} 상전이 피크 @ V={[round(p["V"],3) for p in pk]})')
        return 0
    if a.eis or not (a.ica):
        kw = dict(sigma_e_S_cm=a.sigma_e, sigma_ion_S_cm=a.sigma_ion, thickness_um=a.thickness_um,
                  r_int_ohm_cm2=a.r_int, i0_A_m2=a.i0, d_s_m2_s=a.d_s, r_p_um=a.r_p_um,
                  porosity=a.porosity, c_dl_uF_cm2=a.c_dl_uf)
        if a.metrics:
            p = _load_step3_params(a.metrics)
            for k, v in p.items():
                if v is not None:
                    kw[k] = v
        if a.use_exp_anchors:                                 # frame[4] 실험앵커 (데이터 있으면)
            anc = load_experimental_anchors()
            if anc:
                kw['c_dl_areal_uF_cm2'] = anc['c_dl_areal_uF_cm2']
                if anc.get('r_w_ohm_cm2') is not None:
                    kw['r_w_ohm_cm2'] = anc['r_w_ohm_cm2']
                print(f'  실험앵커: C_dl≈{anc["c_dl_areal_uF_cm2"]} µF/cm²geo '
                      f'(범위 {anc["c_dl_range_uF_cm2"]}, n={anc["n_full"]}) · R_w={anc.get("r_w_ohm_cm2")} Ω·cm²')
            else:
                print('  ⚠ 실험앵커 파일 없음 (이종기술/eis/fits) — 문헌 기본값 유지')
        freqs = np.logspace(np.log10(a.f_hi), np.log10(a.f_lo), 70)
        Z, el = physics_eis(freqs, **kw)
        tau, g, R0f, Zr = drt(freqs, Z)
        with open(a.out + '_nyquist.csv', 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['f_Hz', 'Zre_ohm_cm2', 'Zim_ohm_cm2'])
            w.writerows([(fr, zr.real, zr.imag) for fr, zr in zip(freqs, Z)])
        with open(a.out + '_drt.csv', 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['tau_s', 'gamma']); w.writerows(zip(tau, g))
        print(f'EIS → {a.out}_nyquist.csv · DRT → {a.out}_drt.csv')
        print(f"  R0={el['R0_ohm_cm2']:.1f} R_ct={el['R_ct_ohm_cm2']:.2f} C_dl={el['C_dl_F_cm2']*1e6:.1f}µF/cm² "
              f"f_ct={el['f_ct_Hz']:.1f}Hz R_w={el['R_w_ohm_cm2']:.3g} τ_w={el['tau_w_s']:.3g}s")
        print(f"  C_dl int={el['C_dl_uF_cm2_int']:.2f}µF/cm²계면·총 {el['C_dl_uF_cm2_areal']:.0f}µF/cm²geo "
              f"({el['provenance']['C_dl']})")
        print(f"  R_w: {el['provenance']['R_w']}")
        for p in drt_peaks(tau, g):
            print(f"  DRT 피크: f={p['f_Hz']:.2g}Hz τ={p['tau_s']:.2g}s R≈{p['R_ohm_cm2']:.2f}Ω·cm²")
        traj = None
        if a.cycle_traj:                                       # 사이클-N EIS/DRT 궤적 (D5)
            _cp = [float(x) for x in a.cycle_traj.split(',')]
            r0c, rcc, ntot = _cp[0], _cp[1], int(_cp[2])
            shape = a.cycle_traj.split(',')[3] if len(_cp) > 3 else 'sqrt'
            jump = _cp[4] if len(_cp) > 4 else 0.5
            ns = [int(x) for x in a.cycle_ns.split(',')]
            sh = [float(x) for x in a.cycle_shares.split(',')]
            mult = rint_growth_mult(ns, r0c, rcc, ntot, shape, jump)
            traj = cycle_eis_trajectory(freqs, el, ns, mult, rct_share=sh[0], r0_share=sh[1], rw_share=sh[2])
            with open(a.out + '_cycle.csv', 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['N', 'mult', 'R0_ohm_cm2', 'R_int_ohm_cm2', 'R_ct_ohm_cm2',
                            'R_w_ohm_cm2', 'R_dc_ohm_cm2', 'f_ct_Hz'])
                for t in traj:
                    w.writerow([t['N'], round(t['mult'], 3), round(t['R0_ohm_cm2'], 2),
                                round(t.get('R_int_ohm_cm2', 0.0), 2),
                                round(t['R_ct_ohm_cm2'], 2), round(t['R_w_ohm_cm2'], 2),
                                round(t['R_dc_ohm_cm2'], 2), round(t['f_ct_Hz'], 2)])
            print(f'사이클-N EIS 궤적 → {a.out}_cycle.csv  (R_int {r0c}→{rcc}@N{ntot}, {shape} shape, '
                  f'분배 (계면/R_ct/R_w)={sh} ★ASSUMED §F1)')
            _ri0, _ri1 = traj[0].get('R_int_ohm_cm2', 0.0), traj[-1].get('R_int_ohm_cm2', 0.0)
            print(f"  N={traj[0]['N']}: R_int(계면)={_ri0:.1f} R_ct={traj[0]['R_ct_ohm_cm2']:.1f} → "
                  f"N={traj[-1]['N']}: R_int={_ri1:.1f}(×{_ri1/max(_ri0,1e-9):.1f}) R_ct={traj[-1]['R_ct_ohm_cm2']:.1f} "
                  f"— 계면 arc 지배 성장 = 접촉손실 지문 (Kang&Shin/Yun)")
        if a.fig:                                              # 발표/논문용 그림 (png+svg)
            saved = save_eis_figures(a.out, freqs, Z, el, tau, g, drt_peaks(tau, g), traj=traj)
            print('  그림 저장: ' + ', '.join(saved))
        return 0


if __name__ == '__main__':
    import sys
    raise SystemExit(main())
