#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ T2 **개발** harness — T2-1′ `mms_linear_jump` (제조해 · 계면 막) · T2-4a `trace_jump_operator` (RRM ↔ CNC 막 연산자) (2026-10-13).

⛔ **개발 실행 — D12-V 봉인 전 · 검증 PASS 아님.**  이 harness 의 숫자 (사다리 · 관측 차수 · L1 ↔ 축별) 는 개발 산출이다 — 나중에 독립 검증
   결과로 재분류하지 않는다 (v3.1 §6-2 · Codex v3 판정 §4 · §8).  허용치 · 관측 위치 · 판별 기준 = D12-V (1저자 · 실행 전) · L1 ↔ 축별 = D11.
   시험 (scripts/test_rint_t2_dev.py) 이 PASS/FAIL 로 보는 것은 정확한 층 (제조해 · 정확 이산 · 면 함수 공유 · 연속 극한 산술) 뿐.
⛔ 생산 경로 아님 — 시험 전용 harness (생산 솔버 경로 밖) · 면 조립은 생산 `step3_sigma.interface_face_g` 를 **공유**한다 (v2 §4 · v3 §4-1 —
   따로 짜면 "같은 법칙" 을 검증하지 못한다) · 정답 (제조해) 은 그 함수로 다시 만들지 않는다.  웹앱 화면 없음.

T2-1′ (v2 §4 T2-1 · v3 §4-1 보강 · Codex `mms_sign_check`): 2D (z 한 층) FV · 계면 = 원점을 지나는 평면 (법선 θ) · u = 법선 · v = 접선 ·
  φ1 = αu + βuv (σ1 · u < 0) · φ2 = (σ1α/σ2)u + (σ1β/σ2)uv + r′σ1α + r′σ1βv (σ2 · u ≥ 0) — u = 0 에서 flux 연속 · φ1 − φ2 = r′·J_n
  (J_n = −σ1 ∂φ1/∂u · r′ = 1e4·r_face [µm·cm/S] — r[Ω·cm²]·σ[S/cm] = cm → µm 는 ×1e4).  전 경계 Dirichlet (정확 φ) · 계단 계면의 막 면 법칙
  'L1' r_face·(|n_x| + |n_y|) · 'axis' r_face/|n_k| (D11 후보 둘).  변이: 막 삭제 · ×1e4 누락 · jump 부호 반전 (정답 쪽).
T2-4a (v3 §2-3 · Codex `support_smearing_continuum`): 평면 위 원판 a · support b · Δφ = 1 + βx (원판 중심 기준 · bulk 없음) ·
  RRM = Σ w_e Δφ_e² / Σ w_e (w = 면 ∩ 참 원판 · rint_rrm_reference.disc_rect_area) → 1 + β²a²/4 · CNC = support 면 (중심이 b 안) 평균 → 1 + β²b²/4.

  python3 scripts/rint_t2_dev.py --out docs/data/rint_t2_dev_20261013
"""
import argparse
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
    """제조해 (v2 §4 T2-1 식 그대로) — 회전 좌표 u = n·x · v = t·x (n = (cosθ, sinθ) · t = (−sinθ, cosθ)) · 길이 µm · σ S/cm."""

    def __init__(self, alpha, beta, s1, s2, r_face, theta_deg):
        self.alpha, self.beta, self.s1, self.s2 = float(alpha), float(beta), float(s1), float(s2)
        self.r_face = float(r_face)
        self.rprime = S3.RINT_OHM_CM2_TO_UM_CM_PER_S * self.r_face           # 1e4 · r_face [µm·cm/S]
        th = math.radians(float(theta_deg))
        self.theta_deg = float(theta_deg)
        self.n = np.array([math.cos(th), math.sin(th)]); self.t = np.array([-math.sin(th), math.cos(th)])

    def uv(self, x, y):
        return self.n[0] * x + self.n[1] * y, self.t[0] * x + self.t[1] * y

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
    """n × n 셀 (h = L/n · 상자 [−L/2, L/2]²) FV · 전 경계 Dirichlet (정답 φ · 반셀 컨덕턴스 2σh) · 영역 = 셀 중심 u 부호 ·
    두 영역 사이 면 = 막 면 → 생산 `S3.interface_face_g(g0, σa, σb, r_face, h)` (r_face = 법칙) · 직접 풀이.
    mutant: 'film_deleted' (막 r 0) · 'unit_1e4_missing' (r_face × 1e−4 — cm → µm 환산 누락) · 'jump_sign_flipped' (정답 쪽 jump 부호 반전)."""
    if mutant not in (None, 'film_deleted', 'unit_1e4_missing', 'jump_sign_flipped'):
        raise ValueError(f'mutant: {mutant!r}')
    ref = M
    if mutant == 'jump_sign_flipped':
        ref = Mms(M.alpha, M.beta, M.s1, M.s2, -M.r_face, M.theta_deg)
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
    for axis in (0, 1):
        sa_ = [slice(None)] * 2; sb_ = [slice(None)] * 2
        sa_[axis] = slice(0, -1); sb_[axis] = slice(1, None)
        sa_, sb_ = tuple(sa_), tuple(sb_)
        s_a, s_b = sig[sa_].ravel(), sig[sb_].ravel()
        A, B = idx[sa_].ravel(), idx[sb_].ravel()
        g0 = 2.0 * s_a * s_b / (s_a + s_b) * h
        film = (reg2[sa_] != reg2[sb_]).ravel()
        rf = _face_rface(M, axis, law)
        if mutant == 'film_deleted':
            rf = 0.0
        elif mutant == 'unit_1e4_missing':
            rf = rf * 1e-4
        g = g0.copy()
        if film.any():
            g[film] = S3.interface_face_g(g0[film], s_a[film], s_b[film], np.full(int(film.sum()), rf), h)
        n_film += int(film.sum())
        rows += [A, B]; cols += [B, A]; vals += [-g, -g]
        np.add.at(diag, A, g); np.add.at(diag, B, g)
    #  경계: 면 중심의 정답 φ · 반셀 (2σh)
    half = 0.5 * L
    for (ii, jj, fx, fy) in ((np.zeros(n, int), np.arange(n), -half + 0 * xc, xc), (np.full(n, n - 1), np.arange(n), half + 0 * xc, xc),
                             (np.arange(n), np.zeros(n, int), xc, -half + 0 * xc), (np.arange(n), np.full(n, n - 1), xc, half + 0 * xc)):
        k = idx[ii, jj]
        gb = 2.0 * sig[ii, jj] * h
        np.add.at(diag, k, gb)
        np.add.at(rhs, k, gb * ref.phi(fx, fy))
    Amat = sparse.coo_matrix((np.concatenate(vals + [diag]), (np.concatenate(rows + [np.arange(n * n)]),
                                                             np.concatenate(cols + [np.arange(n * n)]))), shape=(n * n, n * n)).tocsc()
    phi = spsolve(Amat, rhs).reshape(n, n)
    ex = ref.phi(X, Y)
    e = phi - ex
    return {'n': int(n), 'h_um': h, 'law': law, 'mutant': mutant, 'theta_deg': M.theta_deg, 'n_film_faces': n_film,
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


def mms_ladder(thetas, ns, laws, L=1.6, alpha=2.0, beta=3.0, s1=2.0, s2=5.0, r_face=1e-5, mutants=True):
    out = []
    for th in thetas:
        M = Mms(alpha, beta, s1, s2, r_face, th)
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
            out.append({'theta_deg': th, 'law': law, 'rows': rows, 'observed_order_l2': order, 'mutants_at_finest': muts})
    return {'label': DEV_LABEL, 'params': {'L_um': L, 'alpha_V_per_um': alpha, 'beta_V_per_um2': beta, 's1_S_cm': s1, 's2_S_cm': s2,
                                           'r_face_ohm_cm2': r_face, 'rprime_um_cm_per_S': 1e4 * r_face},
            'cases': out}


def _git(*args):
    try:
        return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                  # noqa: BLE001
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    aa = math.sqrt(1.0 - 0.99 ** 2)                    # Codex 픽스처: R 1 µm 두 구 · δ 0.02 → a 0.14106735979665894 µm
    trace = trace_ladder(aa, 0.24, 4.0, [0.24 / 2 ** k for k in range(1, 8)], center=(0.013, 0.007))
    mms = mms_ladder((0.0, 15.0, 30.0, 45.0), (8, 16, 32, 64, 128), ('L1', 'axis'))
    import scipy as _sp
    doc = {'kind': 'rint_t2_dev', 'version': 'v1', 'label': DEV_LABEL,
           'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
           'git_head': _git('rev-parse', 'HEAD'),
           'code_blobs': {f: _git('hash-object', f) for f in ('scripts/rint_t2_dev.py', 'scripts/step3_sigma.py', 'scripts/rint_rrm_reference.py')},
           'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': _sp.__version__},
           'mms_sign_check': mms_sign_check(), 't2_4a_trace_jump_operator': trace, 't2_1_mms_linear_jump': mms}
    with open(os.path.join(a.out, 't2_dev.json'), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
        fh.write('\n')
    print(DEV_LABEL)
    print('T2-4a 연속:', trace['continuum'], '· 가장 고운 h:', {k: trace['rows'][-1][k] for k in ('h_um', 'rrm', 'cnc')})
    for c in mms['cases']:
        errs = ['%.2e' % r_['err_l2'] for r_ in c['rows']]
        orders = [None if o is None else round(o, 2) for o in c['observed_order_l2']]
        print(f"T2-1′ θ {c['theta_deg']:>4} · {c['law']:<4} · L2 오차 {errs} · 차수 {orders}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
