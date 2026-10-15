#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ T2 **개발** harness — T2-1′ `mms_linear_jump` (제조해 · 계면 막) · T2-4a `trace_jump_operator` (RRM ↔ CNC 막 연산자) (2026-10-13).

⛔ **개발 실행 — D12-V 봉인 전 · 검증 PASS 아님.**  이 harness 의 숫자 (사다리 · 관측 차수 · L1 ↔ 축별) 는 개발 산출이다 — 나중에 독립 검증
   결과로 재분류하지 않는다 (v3.1 §6-2 · Codex v3 판정 §4 · §8).  허용치 · 관측 위치 · 판별 기준 = D12-V (1저자 · 실행 전) · L1 ↔ 축별 = D11.
   시험 (scripts/test_rint_t2_dev.py) 이 PASS/FAIL 로 보는 것은 정확한 층 (제조해 · 정확 이산 · 면 함수 공유 · 연속 극한 산술) 뿐.
⛔ 생산 경로 아님 — 시험 전용 harness (생산 솔버 경로 밖) · 면 조립은 생산 `step3_sigma.interface_face_g` 를 **공유**한다 (v2 §4 · v3 §4-1 —
   따로 짜면 "같은 법칙" 을 검증하지 못한다) · 정답 (제조해) 은 그 함수로 다시 만들지 않는다.  웹앱 화면 없음.

T2-1′ (v2 §4 T2-1 · v3 §4-1 보강 · Codex `mms_sign_check`): 2D (z 한 층) FV · 계면 = 평면 (법선 θ · 원점에서 법선 방향 offset_um) · u = 법선 · v = 접선 ·
  φ1 = αu + βuv (σ1 · u < 0) · φ2 = (σ1α/σ2)u + (σ1β/σ2)uv + r′σ1α + r′σ1βv (σ2 · u ≥ 0) — u = 0 에서 flux 연속 · φ1 − φ2 = r′·J_n
  (J_n = −σ1 ∂φ1/∂u · r′ = 1e4·r_face [µm·cm/S] — r[Ω·cm²]·σ[S/cm] = cm → µm 는 ×1e4).  전 경계 Dirichlet (정확 φ) · 계단 계면의 막 면 법칙
  'L1' r_face·(|n_x| + |n_y|) · 'axis' r_face/|n_k| (D11 후보 둘).  변이: 막 삭제 · ×1e4 누락 · jump 부호 반전 (정답 쪽).
  ★ 경계 반 셀 (RIMP-01 · Codex 10-14 판정문 §2 · 1저자 Q1 (가)): 셀 중심과 경계면 중심이 계면의 **반대편**이면 그 반 셀에도 두 상과 막이 있다 →
    g_b = h² / (d_c/σ_c + d_f/σ_f + 1e4·r_face) (d_c + d_f = h/2 · 평면 교차 위치 = u 의 선형 보간 · r_face = 그 축 내부 막 면과 **같은 법칙** · 변이 포함).
    교차 아닌 경계 반 셀 = 옛 2σh 그대로.  `BOUNDARY_RULE` · 출력 `n_bc_cross` · `tie_count` (|u| < 1e−12 셀 수 — 배정은 부동소수 반올림에 걸린다).
    v1 산출 (`t2_dev.json` · 10-13) 은 이 반 셀을 bulk 로 바로 이었다 (결함 판) — v2 산출 = `t2_dev_v2.json`.
T2-4a (v3 §2-3 · Codex `support_smearing_continuum`): 평면 위 원판 a · support b · Δφ = 1 + βx (원판 중심 기준 · bulk 없음) ·
  RRM = Σ w_e Δφ_e² / Σ w_e (w = 면 ∩ 참 원판 · rint_rrm_reference.disc_rect_area) → 1 + β²a²/4 · CNC = support 면 (중심이 b 안) 평균 → 1 + β²b²/4.

  python3 scripts/rint_t2_dev.py --out docs/data/rint_t2_dev_20261013
"""
import argparse
import copy
import datetime
import json
import math
import os
import platform
import subprocess
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import step3_sigma as S3            # noqa: E402  면 함수 공유 (읽기만)
import rint_rrm_reference as RRM    # noqa: E402  원판 ∩ 직사각형 정확 면적 (시험 전용 모듈)

DEV_LABEL = ('개발 실행 — D12-V 봉인 전 · 검증 PASS 아님 (v3.1 §6-2 · 개발 결과를 나중에 독립 검증으로 재분류하지 않는다 · '
             '허용치 · 관측 위치 · L1 ↔ 축별 (D11) = 1저자)')
#: 경계 반 셀 규칙 (RIMP-01) — 교차 반 셀 = 거리 가중 직렬 + 같은 법칙의 r_face (판정문 §2 의 교차 연결 꼴) · 교차 아님 = 2σh.
BOUNDARY_RULE = 'crossing_half_cell_series_v1'
TIE_TOL_UM = 1e-12                                     # tie 셀 = 셀 중심이 계면 위 (|u| < 이것) — 기록만 (배정 규칙은 u ≥ 0 → 영역 2)


# ═════════════════════════ T2-4a ═════════════════════════
def trace_energy_factor(R, beta):
    """연속 극한: 반경 R 원판 위 균일 가중 · Δφ = 1 + βx (원판 중심 기준) → ⟨Δφ²⟩ = 1 + β²R²/4."""
    return 1.0 + beta * beta * R * R / 4.0


def trace_jump_operator(a, b, beta, h, center=(0.0, 0.0)):
    """한 h 의 이산 막 연산자 — 면 = 원점 기준 h 격자의 정사각형 · Δφ_e = 1 + β(x_e − c_x) (면 중심).
    RRM: 가중 w_e = 면 ∩ 참 원판 (반경 a) · CNC: support = 중심이 반경 b 안인 면 · 균일 가중."""
    cx, cy = float(center[0]), float(center[1])
    R = max(a, b) + 2.0 * h
    i0, i1 = int(math.floor((cx - R) / h)), int(math.ceil((cx + R) / h))
    j0, j1 = int(math.floor((cy - R) / h)), int(math.ceil((cy + R) / h))
    num = den = 0.0
    cnc = []
    n_rrm = 0
    for i in range(i0, i1 + 1):
        x0 = i * h
        xc = x0 + 0.5 * h
        dphi = 1.0 + beta * (xc - cx)
        for j in range(j0, j1 + 1):
            y0 = j * h
            yc = y0 + 0.5 * h
            w = RRM.disc_rect_area(cx, cy, a, x0, x0 + h, y0, y0 + h)
            if w > 0.0:
                num += w * dphi * dphi; den += w; n_rrm += 1
            if (xc - cx) ** 2 + (yc - cy) ** 2 <= b * b:
                cnc.append(dphi * dphi)
    return {'h_um': h, 'rrm': num / den, 'cnc': float(np.mean(cnc)) if cnc else None, 'n_faces_rrm': n_rrm, 'n_faces_cnc': len(cnc),
            'sum_w_over_pi_a2': den / (math.pi * a * a)}


def trace_ladder(a, b, beta, hs, center=(0.0, 0.0)):
    cont = {'rrm': trace_energy_factor(a, beta), 'cnc': trace_energy_factor(b, beta)}
    rows = []
    for h in hs:
        r = trace_jump_operator(a, b, beta, h, center)
        r['err_rrm'] = r['rrm'] - cont['rrm']; r['err_cnc'] = (r['cnc'] - cont['cnc']) if r['cnc'] is not None else None
        rows.append(r)
    order = []
    for p, q in zip(rows[:-1], rows[1:]):
        o = {}
        for k in ('err_rrm', 'err_cnc'):
            if p[k] and q[k] and p[k] != 0.0 and q[k] != 0.0:
                o[k] = math.log(abs(p[k]) / abs(q[k])) / math.log(p['h_um'] / q['h_um'])
        order.append(o)
    return {'label': DEV_LABEL, 'a_um': a, 'b_um': b, 'beta_per_um': beta, 'center_um': list(center), 'continuum': cont,
            'continuum_rel_diff': cont['cnc'] / cont['rrm'] - 1.0, 'rows': rows, 'observed_order': order}


# ═════════════════════════ T2-1′ ═════════════════════════
class Mms:
    """제조해 (v2 §4 T2-1 식 그대로) — 회전 좌표 u = n·x − offset · v = t·x (n = (cosθ, sinθ) · t = (−sinθ, cosθ)) · 길이 µm · σ S/cm.
    offset_um = 계면 평면의 법선 방향 이동 (0 = 원점을 지남 · 옛 배치 비트 같음) — Codex `ShiftMms` (u − offset) 와 같은 꼴."""

    def __init__(self, alpha, beta, s1, s2, r_face, theta_deg, offset_um=0.0):
        self.alpha, self.beta, self.s1, self.s2 = float(alpha), float(beta), float(s1), float(s2)
        self.r_face = float(r_face)
        self.rprime = S3.RINT_OHM_CM2_TO_UM_CM_PER_S * self.r_face           # 1e4 · r_face [µm·cm/S]
        th = math.radians(float(theta_deg))
        self.theta_deg = float(theta_deg)
        self.offset_um = float(offset_um)
        if not math.isfinite(self.offset_um):
            raise ValueError(f'offset_um 은 유한: {offset_um!r}')
        self.n = np.array([math.cos(th), math.sin(th)]); self.t = np.array([-math.sin(th), math.cos(th)])

    def with_r_face(self, r_face):
        """같은 배치 (θ · offset · subclass 의 uv) 의 r_face 만 바꾼 사본 — 변이 `jump_sign_flipped` 의 정답 쪽."""
        o = copy.copy(self)
        o.r_face = float(r_face)
        o.rprime = S3.RINT_OHM_CM2_TO_UM_CM_PER_S * o.r_face
        return o

    def uv(self, x, y):
        u = self.n[0] * x + self.n[1] * y
        if self.offset_um != 0.0:
            u = u - self.offset_um
        return u, self.t[0] * x + self.t[1] * y

    def phi1_uv(self, u, v):
        return self.alpha * u + self.beta * u * v

    def phi2_uv(self, u, v):
        k = self.s1 / self.s2
        return (k * self.alpha * u + k * self.beta * u * v + self.rprime * self.s1 * self.alpha + self.rprime * self.s1 * self.beta * v)

    def dphi1_du(self, u, v):
        return self.alpha + self.beta * v

    def dphi2_du(self, u, v):
        return self.s1 / self.s2 * (self.alpha + self.beta * v)

    def phi(self, x, y):
        u, v = self.uv(x, y)
        return np.where(u < 0.0, self.phi1_uv(u, v), self.phi2_uv(u, v))

    def is_harmonic(self):
        """두 영역 식이 회전 좌표의 쌍선형 (u · v · uv · 상수) 이라 ∂²/∂u² = ∂²/∂v² = 0 — 2 차 중심차분으로 확인 (다항식이라 반올림만)."""
        rng = np.random.default_rng(3)
        e = 1e-3
        for f in (self.phi1_uv, self.phi2_uv):
            for u, v in rng.uniform(-1, 1, (5, 2)):
                lap = (f(u + e, v) - 2 * f(u, v) + f(u - e, v) + f(u, v + e) - 2 * f(u, v) + f(u, v - e)) / (e * e)
                if abs(lap) > 1e-6:
                    return False
        return True


def _face_rface(M, axis, law):
    nk = abs(float(M.n[axis]))
    if law == 'L1':
        return M.r_face * (abs(float(M.n[0])) + abs(float(M.n[1])))
    if law == 'axis':
        return M.r_face / nk if nk > 1e-14 else 1e300
    raise ValueError(f'law 는 L1 | axis: {law!r}')


def mms_solve(M, n, L, law, mutant=None):
    """n × n 셀 (h = L/n · 상자 [−L/2, L/2]²) FV · 전 경계 Dirichlet (정답 φ) · 영역 = 셀 중심 u 부호 (u ≥ 0 → 영역 2) ·
    두 영역 사이 면 = 막 면 → 생산 `S3.interface_face_g(g0, σa, σb, r_face, h)` (r_face = 법칙) · 직접 풀이.
    경계 반 셀 (`BOUNDARY_RULE` · RIMP-01): 셀 중심 ↔ 경계면 중심이 같은 영역 = 2σh · 다른 영역 (계면이 반 셀을 가로지름) =
    h²/(d_c/σ_c + d_f/σ_f + 1e4·r_face) — d_c = (h/2)·|u_c|/(|u_c| + |u_f|) (u 는 선분 위 선형) · d_f = h/2 − d_c · r_face = 그 축 내부 막
    면과 같은 값 (법칙 · 변이 그대로).  정답 (제조해) 은 이 함수로 만들지 않는다 (ref.phi).
    mutant: 'film_deleted' (막 r 0) · 'unit_1e4_missing' (r_face × 1e−4 — cm → µm 환산 누락) · 'jump_sign_flipped' (정답 쪽 jump 부호 반전)."""
    if mutant not in (None, 'film_deleted', 'unit_1e4_missing', 'jump_sign_flipped'):
        raise ValueError(f'mutant: {mutant!r}')
    ref = M
    if mutant == 'jump_sign_flipped':
        ref = M.with_r_face(-M.r_face)
    h = float(L) / int(n)
    xc = -0.5 * L + (np.arange(n) + 0.5) * h
    X, Y = np.meshgrid(xc, xc, indexing='ij')
    U, _V = M.uv(X, Y)
    reg2 = U >= 0.0
    sig = np.where(reg2, M.s2, M.s1)
    idx = np.arange(n * n).reshape(n, n)
    rows, cols, vals = [], [], []
    diag = np.zeros(n * n); rhs = np.zeros(n * n)
    n_film = 0
    rf_ax = []                                             # 축마다 막 r_face (법칙 · 변이) — 내부 막 면 · 교차 경계 반 셀이 같은 값을 쓴다
    for axis in (0, 1):
        rf = _face_rface(M, axis, law)
        if mutant == 'film_deleted':
            rf = 0.0
        elif mutant == 'unit_1e4_missing':
            rf = rf * 1e-4
        rf_ax.append(rf)
    for axis in (0, 1):
        sa_ = [slice(None)] * 2; sb_ = [slice(None)] * 2
        sa_[axis] = slice(0, -1); sb_[axis] = slice(1, None)
        sa_, sb_ = tuple(sa_), tuple(sb_)
        s_a, s_b = sig[sa_].ravel(), sig[sb_].ravel()
        A, B = idx[sa_].ravel(), idx[sb_].ravel()
        g0 = 2.0 * s_a * s_b / (s_a + s_b) * h
        film = (reg2[sa_] != reg2[sb_]).ravel()
        rf = rf_ax[axis]
        g = g0.copy()
        if film.any():
            g[film] = S3.interface_face_g(g0[film], s_a[film], s_b[film], np.full(int(film.sum()), rf), h)
        n_film += int(film.sum())
        rows += [A, B]; cols += [B, A]; vals += [-g, -g]
        np.add.at(diag, A, g); np.add.at(diag, B, g)
    #  경계: 면 중심의 정답 φ · 반 셀 — 교차 아님 = 2σh · 교차 = 거리 가중 직렬 + 막 (RIMP-01)
    half = 0.5 * L
    n_cross = 0
    for (axis, ii, jj, fx, fy) in ((0, np.zeros(n, int), np.arange(n), -half + 0 * xc, xc), (0, np.full(n, n - 1), np.arange(n), half + 0 * xc, xc),
                                   (1, np.arange(n), np.zeros(n, int), xc, -half + 0 * xc), (1, np.arange(n), np.full(n, n - 1), xc, half + 0 * xc)):
        k = idx[ii, jj]
        s_c = sig[ii, jj]
        gb = 2.0 * s_c * h
        u_c = U[ii, jj]
        u_f, _vf = M.uv(fx, fy)
        cross = (u_f >= 0.0) != reg2[ii, jj]
        if cross.any():
            uc, uf = np.abs(u_c[cross]), np.abs(u_f[cross])
            d_c = 0.5 * h * uc / (uc + uf)
            d_f = 0.5 * h - d_c
            s_f = np.where(u_f[cross] >= 0.0, M.s2, M.s1)
            gb = gb.copy()
            gb[cross] = h * h / (d_c / s_c[cross] + d_f / s_f + S3.RINT_OHM_CM2_TO_UM_CM_PER_S * rf_ax[axis])
            n_cross += int(cross.sum())
        np.add.at(diag, k, gb)
        np.add.at(rhs, k, gb * ref.phi(fx, fy))
    Amat = sparse.coo_matrix((np.concatenate(vals + [diag]), (np.concatenate(rows + [np.arange(n * n)]),
                                                             np.concatenate(cols + [np.arange(n * n)]))), shape=(n * n, n * n)).tocsc()
    phi = spsolve(Amat, rhs).reshape(n, n)
    ex = ref.phi(X, Y)
    e = phi - ex
    return {'n': int(n), 'h_um': h, 'law': law, 'mutant': mutant, 'theta_deg': M.theta_deg, 'offset_um': M.offset_um,
            'n_film_faces': n_film, 'n_bc_cross': n_cross, 'tie_count': int((np.abs(U) < TIE_TOL_UM).sum()),
            'boundary_rule': BOUNDARY_RULE,
            'err_max': float(np.abs(e).max()), 'err_l2': float(np.sqrt(np.mean(e * e))), 'phi_exact': ex}


def mms_sign_check():
    """Codex `mms_sign_check` (docs/reviews/codex_rint_g2_design_review_evidence_20261006/evidence.json) — α 2 · β 3 · σ1 2 · σ2 5 · r 0.1 · v 0.4
    (무차원 — 이 식에서 r 는 r′ 자리).  normal_from_1_to_2 · J_n = −σ1 ∂φ1/∂u · φ1 − φ2 (u = 0) = r·J_n."""
    alpha, beta, s1, s2, r, v = 2., 3., 2., 5., .1, .4
    grad1 = alpha + beta * v
    grad2 = s1 / s2 * grad1
    phi1, phi2 = 0., r * s1 * grad1
    Jn = -s1 * grad1
    return {'normal_from_1_to_2': True, 'normal_flux_1': Jn, 'normal_flux_2': -s2 * grad2, 'phi1_minus_phi2': phi1 - phi2,
            'r_times_Jn': r * Jn}


def mms_ladder(cases, ns, laws, L=1.6, alpha=2.0, beta=3.0, s1=2.0, s2=5.0, r_face=1e-5, mutants=True):
    """cases = [(θ°, 계면 법선 이동 µm), …] — 행마다 tie 셀 수 · 경계 반 셀 교차 수를 같이 싣는다 (tie 배정 = 플랫폼 반올림 의존 표지)."""
    out = []
    for th, off in cases:
        M = Mms(alpha, beta, s1, s2, r_face, th, offset_um=off)
        for law in laws:
            rows = []
            for n in ns:
                r = mms_solve(M, n, L, law)
                r.pop('phi_exact')
                rows.append(r)
            order = [math.log(p['err_l2'] / q['err_l2']) / math.log(p['h_um'] / q['h_um'])
                     if p['err_l2'] > 0 and q['err_l2'] > 0 else None for p, q in zip(rows[:-1], rows[1:])]
            muts = {}
            if mutants:
                for mut in ('film_deleted', 'unit_1e4_missing', 'jump_sign_flipped'):
                    m = mms_solve(M, ns[-1], L, law, mutant=mut)
                    muts[mut] = {'err_l2': m['err_l2'], 'err_max': m['err_max'], 'ratio_to_correct_l2': m['err_l2'] / rows[-1]['err_l2']
                                 if rows[-1]['err_l2'] > 0 else None}
            out.append({'theta_deg': th, 'offset_um': off, 'law': law, 'rows': rows, 'observed_order_l2': order,
                        'mutants_at_finest': muts})
    return {'label': DEV_LABEL, 'boundary_rule': BOUNDARY_RULE,
            'params': {'L_um': L, 'alpha_V_per_um': alpha, 'beta_V_per_um2': beta, 's1_S_cm': s1, 's2_S_cm': s2,
                       'r_face_ohm_cm2': r_face, 'rprime_um_cm_per_S': 1e4 * r_face},
            'cases': out}


def _git(*args):
    try:
        return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                  # noqa: BLE001
        return None


#: v2 사다리 배치 — v1 의 넷 + 이동 45° (tie 0 · RIMP-01 회귀와 같은 배치).  v1 (10-13) = θ 넷 · 이동 없음 · 결함 경계.
LADDER_CASES = ((0.0, 0.0), (15.0, 0.0), (30.0, 0.0), (45.0, 0.0), (45.0, 0.001))
OUT_NAME = 't2_dev_v2.json'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    aa = math.sqrt(1.0 - 0.99 ** 2)                    # Codex 픽스처: R 1 µm 두 구 · δ 0.02 → a 0.14106735979665894 µm
    trace = trace_ladder(aa, 0.24, 4.0, [0.24 / 2 ** k for k in range(1, 8)], center=(0.013, 0.007))
    mms = mms_ladder(LADDER_CASES, (8, 16, 32, 64, 128), ('L1', 'axis'))
    import scipy as _sp
    doc = {'kind': 'rint_t2_dev', 'version': 'v2', 'label': DEV_LABEL, 'boundary_rule': BOUNDARY_RULE,
           'history': ('v1 = t2_dev.json (10-13 · 첫 사다리) — 경계 반 셀을 bulk 2σh 로 바로 이은 결함 판 (RIMP-01 · Codex 10-14 판정문 §2) · '
                       'v2 = 이 파일 (경계 교차 반 셀 = 거리 가중 직렬 + 같은 법칙의 r_face · 이동 45° 추가) — 둘 다 개발 산출'),
           'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
           'git_head': _git('rev-parse', 'HEAD'),
           'code_blobs': {f: _git('hash-object', f) for f in ('scripts/rint_t2_dev.py', 'scripts/step3_sigma.py', 'scripts/rint_rrm_reference.py')},
           'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': _sp.__version__},
           'mms_sign_check': mms_sign_check(), 't2_4a_trace_jump_operator': trace, 't2_1_mms_linear_jump': mms}
    with open(os.path.join(a.out, OUT_NAME), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
        fh.write('\n')
    print(DEV_LABEL)
    print('T2-4a 연속:', trace['continuum'], '· 가장 고운 h:', {k: trace['rows'][-1][k] for k in ('h_um', 'rrm', 'cnc')})
    for c in mms['cases']:
        errs = ['%.2e' % r_['err_l2'] for r_ in c['rows']]
        orders = [None if o is None else round(o, 2) for o in c['observed_order_l2']]
        ties = [r_['tie_count'] for r_ in c['rows']]
        print(f"T2-1′ θ {c['theta_deg']:>4} · 이동 {c['offset_um']:g} · {c['law']:<4} · L2 오차 {errs} · 차수 {orders} · tie {ties}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
