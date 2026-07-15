#!/usr/bin/env python3
"""STEP4-v2 — 갈바노스타틱 시간 전개: 비선형 Butler-Volmer + 입자별 구형확산 (voxel-DFN, SSB).

설계: docs/step4_v2_design.md.  v1(step3_sigma.solve_reaction_current, 저율 선형·균일 SOC
스냅샷)의 동역학판.  같은 rasterized 복셀 격자 위 두 망(전자: AM+carbon+SDCP / 이온: SE+SDCP)을
AM|ion BV 면에서 결합하고, 시간을 굴린다.

물리 (황화물 SSB 특화 — 근사가 아니라 물리인 것 2개):
  · SE = 단일이온 전도체(t⁺≈1) → 전해질 농도분극 없음 → 이온망은 시종 옴익.
  · 전위 준정적(전기장 이완 ≪ 확산) → 각 시점 (φ_e, φ_i) 정상상태를 Newton으로 푼다.
  · 입자 내부: x(ρ,t) 구형 1D Fick — FV Crank–Nicolson, 입자별 tridiagonal(벡터화 Thomas).
  · 대칭 BV(α=0.5): I_face = 2·i0(x_s)·A_face·sinh(β·η),  η = φ_e − φ_i − U_ocp(x_s),
    β = F/(2RT).  I_face 부호: e-망 → i-망(= 탈리튬/충전) 양수.
  · 갈바노스타틱: 집전체(bottom) = 전자망 supernode B (외부로 I_app 인출: b[B] = −I_app),
    분리막(top) = 이온망 접지(φ=0, Li counter 기준) → V_cell = φ_B 가 미지수로 자연히 나옴.
    평형(I=0)에서 φ_B = U(x̄) = OCV 재현이 부호 규약의 셀프체크.

단위: 내부 SI (m, s, A, V, mol).  σ 테이블 입력은 S/cm(STEP3 규약) → ×100 [S/m].

§F1 앵커 입력(날조 금지 — 기본값 없이 파일로만):
  · U_ocp(x)·c_max·stoich 창(x0, x100): --ocp-csv + --params-json
    (scripts/step4_pybamm_anchor.py --export-params 가 pybamm Chen2020에서 생성, provenance 포함)
  · D_s: --d-s (기본 3e-14 m²/s = Kang&Shin 2025 FEM 값 인용, 문헌범위 1e-14–1e-13)
  · i0: --i0 (기본 2 A/m² = v1 훅 유지, ⚠F1 스윕 대상)
  셀프테스트는 합성 선형 OCP(TEST-ONLY 라벨)만 사용 — 실측/문헌 수치 아님.

한계(정직, 설계 §6): half-cell(anode 과전압 없음) · 열/열화/부피변화 없음 · 입자 표면 SOC는
입자당 1D(면별 국소 SOC 없음 — 입자간 불균일이 해상 대상) · 코팅 부분피복은 전면적 flux로 균질화.
"""
import argparse
import json
import sys

import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import cg

F_CONST = 96485.33212        # C/mol
R_GAS = 8.314462618          # J/mol/K
T_K = 298.15
BETA = F_CONST / (2.0 * R_GAS * T_K)   # 1/V — 대칭 BV sinh 인자
GPU = False                  # --gpu 로 켬; CuPy 실패 시 CPU 폴백 (step3_sigma 패턴)


# ---------------------------------------------------------------- CG (warm start)
def _cg(L, b, x0=None, rtol=1e-9):
    """Jacobi-CG, GPU(CuPy) 우선/CPU 폴백 — step3_sigma._solve_cg 패턴 + x0 warm start."""
    diag = L.diagonal()
    if GPU:
        try:
            import cupy as cp
            import cupyx.scipy.sparse as cxs
            from cupyx.scipy.sparse.linalg import cg as cg_gpu
            Lg = cxs.csr_matrix(L.astype(np.float64))
            bg = cp.asarray(b, np.float64)
            Mg = cxs.diags(1.0 / cp.asarray(diag))
            x0g = cp.asarray(x0, np.float64) if x0 is not None else None
            try:
                xg, info = cg_gpu(Lg, bg, x0=x0g, tol=rtol, maxiter=50000, M=Mg)
            except TypeError:
                xg, info = cg_gpu(Lg, bg, x0=x0g, rtol=rtol, atol=0.0, maxiter=50000, M=Mg)
            return cp.asnumpy(xg), int(info)
        except Exception as e:
            print(f'    step4 GPU solve unavailable ({type(e).__name__}: {e}) → CPU', flush=True)
    M = sparse.diags(1.0 / diag)
    try:
        return cg(L, b, x0=x0, rtol=rtol, maxiter=50000, M=M)
    except TypeError:
        return cg(L, b, x0=x0, tol=rtol, maxiter=50000, M=M)


# ---------------------------------------------------------------- 구형확산 (FV + CN)
class RadialDiffusion:
    """입자별 구형 1D Fick, 정규화 반경 ρ=r/R ∈ [0,1], FV 셸 Nr개, Crank–Nicolson.

    FV 유도 (셸 k, 경계 ρ_k = k/Nr, 중심값 x_k):
      Ṽ_k · dx_k/dt = (D/R²)·[ρ²_{k+1}(x_{k+1}−x_k) − ρ²_k(x_k−x_{k−1})]/Δρ + δ_{k,Nr−1}·J/(c_max·R)
      (Ṽ_k = (ρ_{k+1}³−ρ_k³)/3 — 단위구 셸부피/4π; 표면 면적항 ρ²=1)
    질량보존: Σ Ṽ_k Δx_k = Δt·J/(c_max·R) 가 CN에서 기계정밀도로 성립(FV 보존형) — selftest 1.
    x_surf = x_{Nr−1} + (∂x/∂ρ)|₁·Δρ/2,  (∂x/∂ρ)|₁ = J·R/(D·c_max)  (flux BC ghost 외삽)."""

    def __init__(self, n_p, nr, r_p_m, d_s, c_max, x_init):
        self.n_p, self.nr = int(n_p), int(nr)
        self.R = np.asarray(r_p_m, np.float64)              # [n_p] m
        self.D = float(d_s)
        self.c_max = float(c_max)
        rho = np.arange(nr + 1) / nr                        # 셸 경계
        self.d_rho = 1.0 / nr
        self.Vk = (rho[1:] ** 3 - rho[:-1] ** 3) / 3.0      # [nr]
        self.A_lo = rho[:-1] ** 2                           # 셸 하부 경계면 ρ² [nr] (k=0 → 0)
        self.A_hi = rho[1:] ** 2                            # 셸 상부 경계면 ρ²
        self.x = np.full((self.n_p, nr), float(x_init))
        self.J = np.zeros(self.n_p)                         # 표면 몰유속 [mol/m²/s], 리튬화 +

    def surf_x(self):
        grad = self.J * self.R / (self.D * self.c_max)      # (∂x/∂ρ)|₁
        return np.clip(self.x[:, -1] + 0.5 * self.d_rho * grad, 1e-6, 1.0 - 1e-6)

    def mean_x(self):
        return (self.x * self.Vk).sum(1) / self.Vk.sum()

    def step(self, dt):
        """CN 한 스텝 (J 고정).  벡터화 Thomas (n_p 동시).
        이산화: Ṽ_k dx_k/dt = (D/R²)[A_hi(x_{k+1}−x_k) − A_lo(x_k−x_{k−1})]/Δρ + src
        → x_{k±1} 결합계수 = (D·dt/R²)·A/(Ṽ_k·Δρ)  [Δρ 1회 — 검증: √t selftest]"""
        lam = self.D * dt / (self.R ** 2)                   # [n_p]
        aL = self.A_lo / (self.Vk * self.d_rho)             # [nr]
        aH = self.A_hi / (self.Vk * self.d_rho)
        # M·x 연산자 (행 k: +aL·x_{k-1} −(aL+aH)·x_k +aH·x_{k+1}; 표면 aH항 제외=무유속,
        # 유속은 소스 s로).  CN: (I − λ/2·M)x⁺ = (I + λ/2·M)x + dt·s
        lo = np.outer(lam, aL)                              # [n_p, nr] (k=0 열은 0)
        hi = np.outer(lam, aH)
        hi[:, -1] = 0.0                                     # 표면 경계: 확산항 없음(소스로)
        dg = lo + hi
        s = np.zeros_like(self.x)
        s[:, -1] = self.J / (self.c_max * self.R) / self.Vk[-1]
        rhs = self.x + 0.5 * (lo * np.roll(self.x, 1, 1) - dg * self.x + hi * np.roll(self.x, -1, 1))
        rhs[:, 0] -= 0.5 * lo[:, 0] * self.x[:, -1]         # roll 오염 제거 (k=0: lo=0이라 0이지만 명시)
        rhs[:, -1] -= 0.5 * hi[:, -1] * self.x[:, 0]
        rhs += dt * s
        # Thomas: A = I + (λ/2)(대각 dg, 부대각 −lo/−hi)
        a = -0.5 * lo                                       # sub (k-1 결합)
        c = -0.5 * hi                                       # super
        d = 1.0 + 0.5 * dg
        cp_ = np.zeros_like(c); dp = np.zeros_like(rhs)
        cp_[:, 0] = c[:, 0] / d[:, 0]
        dp[:, 0] = rhs[:, 0] / d[:, 0]
        for k in range(1, self.nr):
            den = d[:, k] - a[:, k] * cp_[:, k - 1]
            cp_[:, k] = c[:, k] / den
            dp[:, k] = (rhs[:, k] - a[:, k] * dp[:, k - 1]) / den
        xn = np.empty_like(self.x)
        xn[:, -1] = dp[:, -1]
        for k in range(self.nr - 2, -1, -1):
            xn[:, k] = dp[:, k] - cp_[:, k] * xn[:, k + 1]
        self.x = xn


# ---------------------------------------------------------------- OCP / i0
class OCP:
    def __init__(self, x_tab, u_tab, c_max, x0, x100, provenance='', test_only=False):
        o = np.argsort(x_tab)
        self.x_tab = np.asarray(x_tab, np.float64)[o]
        self.u_tab = np.asarray(u_tab, np.float64)[o]
        self.c_max, self.x0, self.x100 = float(c_max), float(x0), float(x100)
        self.provenance, self.test_only = provenance, bool(test_only)

    def U(self, x):
        return np.interp(x, self.x_tab, self.u_tab)

    @staticmethod
    def load(ocp_csv, params_json):
        tab = np.loadtxt(ocp_csv, delimiter=',', skiprows=1)
        p = json.load(open(params_json))
        return OCP(tab[:, 0], tab[:, 1], p['c_max_mol_m3'], p['x_at_charged'],
                   p['x_at_discharged'], p.get('provenance', ''))

    @staticmethod
    def synthetic_test():
        """TEST-ONLY 합성 선형 OCP — 문헌수치 아님 (selftest 전용, §F1)."""
        x = np.linspace(0.0, 1.0, 21)
        return OCP(x, 4.2 - 1.0 * x, c_max=50000.0, x0=0.25, x100=0.85,
                   provenance='SYNTHETIC-TEST-ONLY', test_only=True)


def i0_of_x(i0_ref, x_s):
    """i0(x) = i0_ref·√(4x(1−x)) — x=0.5에서 i0_ref로 정규화한 표준 (c_e 고정, 단일이온 SE)."""
    return i0_ref * np.sqrt(np.clip(4.0 * x_s * (1.0 - x_s), 1e-4, None))


# ---------------------------------------------------------------- 결합망 조립 (정적 1회)
class CellSystem:
    """v1(solve_reaction_current)과 같은 격자 규약: 6-이웃 face, plate band, anchored filter.
    정적(불변) 부분을 1회 조립해두고, Newton 반복에서는 BV 면 값만 갱신해 CSR 재조립."""

    def __init__(self, sid, sig_e_tab_S_cm, sig_i_tab_S_cm, pid, n_am, vox_um,
                 z_top_um=None, z_bot_um=0.0):
        vox_m = vox_um * 1e-6
        self.vox_m = vox_m
        sig_e = np.asarray(sig_e_tab_S_cm, np.float64)[sid] * 100.0   # S/m
        sig_i = np.asarray(sig_i_tab_S_cm, np.float64)[sid] * 100.0
        cond_e, cond_i = sig_e > 0, sig_i > 0
        nx, ny, nz = sid.shape
        zc = (np.arange(nz) + 0.5) * vox_um
        band = vox_um + 0.10
        z_b = float(z_bot_um)
        z_p = min(float(z_top_um) if z_top_um is not None else nz * vox_um, nz * vox_um)
        any_e = cond_e.any(2); k_first = np.argmax(cond_e, 2)
        bot_e = any_e & (zc[k_first] - z_b <= band)
        any_i = cond_i.any(2); k_last = nz - 1 - np.argmax(cond_i[:, :, ::-1], 2)
        top_i = any_i & (z_p - zc[k_last] <= band)
        if not bot_e.any() or not top_i.any():
            raise RuntimeError('no plate contact (bot_e/top_i empty)')
        uni = cond_e | cond_i
        lab, _ = ndimage.label(uni)
        ii, jj = np.where(bot_e); anch = set(lab[ii, jj, k_first[bot_e]].tolist())
        ii, jj = np.where(top_i); anch |= set(lab[ii, jj, k_last[top_i]].tolist())
        anch.discard(0)
        keep = np.isin(lab, list(anch))
        cond_e &= keep; cond_i &= keep
        self.n_e, self.n_i = int(cond_e.sum()), int(cond_i.sum())
        idx_e = -np.ones(sid.shape, np.int64); idx_e[cond_e] = np.arange(self.n_e)
        idx_i = -np.ones(sid.shape, np.int64); idx_i[cond_i] = np.arange(self.n_i)
        sig_e = np.where(cond_e, sig_e, 0.0); sig_i = np.where(cond_i, sig_i, 0.0)
        self.N = self.n_e + self.n_i + 1                    # +1 = 집전체 supernode B
        self.iB = self.N - 1
        rows, cols, vals = [], [], []
        diag0 = np.zeros(self.N)

        def _couple(idxN, sigN, off, sl_a, sl_b):
            A, B = idxN[sl_a], idxN[sl_b]
            sa, sb = sigN[sl_a], sigN[sl_b]
            m = (A >= 0) & (B >= 0)
            if not m.any():
                return
            g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox_m       # 조화평균 face-컨덕턴스 [S]
            a2, b2 = A[m] + off, B[m] + off
            rows.append(a2); cols.append(b2); vals.append(-g)
            rows.append(b2); cols.append(a2); vals.append(-g)
            np.add.at(diag0, a2, g); np.add.at(diag0, b2, g)

        SL = ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
              (np.s_[:, :, :-1], np.s_[:, :, 1:]))
        for sl_a, sl_b in SL:
            _couple(idx_e, sig_e, 0, sl_a, sl_b)
            _couple(idx_i, sig_i, self.n_e, sl_a, sl_b)
        # plates: bottom e-접점 ↔ supernode B (엣지), top i-접점 → 접지 (diag-only, v1 규약 g)
        ii, jj = np.where(bot_e); kk = k_first[bot_e]
        Ae = idx_e[ii, jj, kk]; m = Ae >= 0
        dist = np.maximum(np.abs(zc[kk[m]] - z_b), 0.5 * vox_um) * 1e-6
        gB = sig_e[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist
        aB = Ae[m]
        rows.append(aB); cols.append(np.full(len(aB), self.iB)); vals.append(-gB)
        rows.append(np.full(len(aB), self.iB)); cols.append(aB); vals.append(-gB)
        np.add.at(diag0, aB, gB); diag0[self.iB] += gB.sum()
        ii, jj = np.where(top_i); kk = k_last[top_i]
        Ai = idx_i[ii, jj, kk]; m = Ai >= 0
        dist = np.maximum(np.abs(z_p - zc[kk[m]]), 0.5 * vox_um) * 1e-6
        gT = sig_i[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist
        np.add.at(diag0, Ai[m] + self.n_e, gT)              # 접지(φ=0): diag-only
        # BV 면 목록 (값은 매 Newton 갱신)
        am_m = (sid == 1) | (sid == 2)
        ion_m = (sid == 5) | (sid == 6)
        fe, fi, fp = [], [], []
        for sl_a, sl_b in SL:
            for am_first in (True, False):
                slA, slB = (sl_a, sl_b) if am_first else (sl_b, sl_a)
                m = am_m[slA] & ion_m[slB]
                Ae2 = idx_e[slA]; Bi2 = idx_i[slB]
                m &= (Ae2 >= 0) & (Bi2 >= 0)
                if not m.any():
                    continue
                fe.append(Ae2[m]); fi.append(Bi2[m] + self.n_e); fp.append(pid[slA][m])
        if not fe:
            raise RuntimeError('no BV interface')
        self.f_e = np.concatenate(fe); self.f_i = np.concatenate(fi)
        self.f_pid = np.concatenate(fp)
        self.n_bv = len(self.f_e)
        self.A_face = vox_m * vox_m
        self.n_am = int(n_am)
        diag0[diag0 == 0.0] = 1.0                           # degree-0 가드 (v1 규약; CG x0 주의)
        self.rows0 = np.concatenate(rows + [np.arange(self.N)])
        self.cols0 = np.concatenate(cols + [np.arange(self.N)])
        self.vals0 = np.concatenate(vals + [diag0])
        self._static_nnz = len(self.vals0)
        self._diag0 = diag0

    # -- 비선형 잔차/야코비 (φ 전체 벡터; U_f, i0_f = 면별) --
    def _face_eta_I(self, phi, U_f, i0_f):
        eta = phi[self.f_e] - phi[self.f_i] - U_f
        arg = np.clip(BETA * eta, -40.0, 40.0)
        I_f = 2.0 * i0_f * self.A_face * np.sinh(arg)       # [A], e→i 양수(탈리튬)
        g_f = 2.0 * i0_f * self.A_face * BETA * np.cosh(arg)  # dI/dη [S] > 0
        return eta, I_f, g_f

    def residual(self, phi, U_f, i0_f, I_app):
        """F(φ) = L0·φ + BV(φ) − b;  b[B] = −I_app (방전: 외부로 인출)."""
        L0 = sparse.coo_matrix((self.vals0, (self.rows0, self.cols0)),
                               shape=(self.N, self.N)).tocsr()
        Fv = L0 @ phi
        _, I_f, _ = self._face_eta_I(phi, U_f, i0_f)
        np.add.at(Fv, self.f_e, I_f)
        np.add.at(Fv, self.f_i, -I_f)
        Fv[self.iB] += I_app                                # b[B]=−I_app 이항
        return Fv, I_f

    def newton(self, phi, U_f, i0_f, I_app, tol_rel=1e-8, max_it=25):
        """감쇠 Newton.  J = L0 + Σ_f g_f (e_a−e_b)(e_a−e_b)ᵀ — SPD → CG(warm).
        수렴 판정 = max(노드별 KCL 잔차 ∞-norm, e-망 집계잔차 |I_app−Σi_am|) / |I_app|
        — 집계 항이 없으면 노드별 1e-8이 큰 격자(n_e~1e6)에서 총전류 오차로 누적될 수 있음."""
        Fv, I_f = self.residual(phi, U_f, i0_f, I_app)
        scale = max(abs(I_app), 1e-12)

        def _err(F):
            return max(float(np.linalg.norm(F, np.inf)),
                       abs(float(F[:self.n_e].sum() + F[self.iB]))) / scale

        it = 0
        best, stall = np.inf, 0
        while it < max_it:
            r = _err(Fv)
            if r < tol_rel:
                break
            # float64 노이즈-바닥 정체 감지: 이미 잘 수렴한 상태(best<1e-3)에서 2연속 무개선일
            # 때만 종료 — 초기 비선형 감쇠 구간(r~1, 느린 하강)을 오판해 끊지 않도록 제한.
            if r >= 0.5 * best:
                stall += 1
                if stall >= 2 and best < 1e-3:
                    break
            else:
                stall = 0
            best = min(best, r)
            _, I_f, g_f = self._face_eta_I(phi, U_f, i0_f)
            diag_add = np.zeros(self.N)
            np.add.at(diag_add, self.f_e, g_f)
            np.add.at(diag_add, self.f_i, g_f)
            rows = np.concatenate([self.rows0, self.f_e, self.f_i, np.arange(self.N)])
            cols = np.concatenate([self.cols0, self.f_i, self.f_e, np.arange(self.N)])
            vals = np.concatenate([self.vals0, -g_f, -g_f, diag_add])
            J = sparse.coo_matrix((vals, (rows, cols)), shape=(self.N, self.N)).tocsr()
            dphi, info = _cg(J, -Fv, x0=None)
            step = 1.0
            for k in range(10):                             # 감쇠: ||F|| 감소 보장
                Fn, I_fn = self.residual(phi + step * dphi, U_f, i0_f, I_app)
                if (np.linalg.norm(Fn, np.inf)
                        <= np.linalg.norm(Fv, np.inf) * (1 - 0.25 * step)) or k == 9:
                    break                                    # k==9: 마지막 평가 스텝 그대로 적용
                step *= 0.5
            phi = phi + step * dphi
            Fv, I_f = Fn, I_fn
            it += 1
        return phi, I_f, _err(Fv), it

    def particle_current(self, I_f):
        """입자별 리튬화 전류 [A] (방전 +).  I_f 는 e→i(탈리튬) 양수 → 부호 반전 합산."""
        i_am = np.zeros(self.n_am)
        m = self.f_pid >= 0
        np.add.at(i_am, self.f_pid[m], -I_f[m])
        return i_am


# ---------------------------------------------------------------- 시간 루프
def simulate(sys_, ocp, r_p_m, d_s, i0_ref, c_rate, nr=20, v_min=3.0, v_max=4.5,
             dx_max=0.02, dt_init=1.0, dt_max=120.0, t_max=None, charge=False,
             verbose=True):
    """갈바노스타틱 방전(기본)/충전.  반환: dict of arrays (t, V, x_mean, …)."""
    n_am = sys_.n_am
    x_init = ocp.x0 if not charge else ocp.x100
    x_end = ocp.x100 if not charge else ocp.x0
    rad = RadialDiffusion(n_am, nr, r_p_m, d_s, ocp.c_max, x_init)
    V_p = 4.0 / 3.0 * np.pi * r_p_m ** 3                    # [m³] 물리 구부피 (용량 기준)
    cap_As = F_CONST * ocp.c_max * abs(ocp.x100 - ocp.x0) * V_p.sum()
    I_1C = cap_As / 3600.0
    I_app = c_rate * I_1C * (1.0 if not charge else -1.0)   # 방전 +(인출)
    # BV 면이 하나도 없는 입자 = dead (전류 0으로 자연 처리 — 미세구조 효과 그 자체)
    has_face = np.zeros(n_am, bool)
    has_face[np.unique(sys_.f_pid[sys_.f_pid >= 0])] = True
    if verbose:
        print(f'  step4-v2: n_am={n_am} (dead {int((~has_face).sum())}), BV faces {sys_.n_bv:,}, '
              f'dof {sys_.N:,}, I_1C={I_1C:.3e} A, I_app={I_app:.3e} A ({c_rate:g}C)', flush=True)
    phi = np.zeros(sys_.N)
    U0 = float(ocp.U(x_init))
    phi[:sys_.n_e] = U0; phi[sys_.iB] = U0                  # 초기추정 = 평형
    out = {k: [] for k in ('t', 'V', 'x_mean', 'x_surf_p05', 'x_surf_p50', 'x_surf_p95',
                           'eta_kin_mean', 'eta_diff_mean', 'newton_it', 'kcl_rel')}
    t, dt = 0.0, dt_init
    x_pid_prev = None
    while True:
        x_s = rad.surf_x()
        U_f = ocp.U(x_s)[np.clip(sys_.f_pid, 0, n_am - 1)]  # 면별 (입자 표면 SOC)
        i0_f = i0_of_x(i0_ref, x_s)[np.clip(sys_.f_pid, 0, n_am - 1)]
        phi, I_f, resid, n_it = sys_.newton(phi, U_f, i0_f, I_app)
        i_am = sys_.particle_current(I_f)                   # 리튬화 + [A]
        kcl = abs(i_am.sum() * (1.0) - I_app) / max(abs(I_app), 1e-30)
        V_cell = float(phi[sys_.iB])
        x_mean_p = rad.mean_x()
        eta_f = phi[sys_.f_e] - phi[sys_.f_i] - U_f
        w = np.abs(I_f) + 1e-30
        x_bar = float((x_mean_p * V_p).sum() / V_p.sum())
        out['t'].append(t); out['V'].append(V_cell)
        out['x_mean'].append(x_bar)
        out['x_surf_p05'].append(float(np.percentile(x_s[has_face], 5)))
        out['x_surf_p50'].append(float(np.percentile(x_s[has_face], 50)))
        out['x_surf_p95'].append(float(np.percentile(x_s[has_face], 95)))
        out['eta_kin_mean'].append(float((np.abs(eta_f) * w).sum() / w.sum()))
        out['eta_diff_mean'].append(float(np.mean(np.abs(ocp.U(x_s[has_face])
                                                         - ocp.U(x_mean_p[has_face])))))
        out['newton_it'].append(n_it); out['kcl_rel'].append(kcl)
        if verbose and (len(out['t']) % 10 == 1):
            print(f'    t={t:9.1f}s  V={V_cell:.4f}  x̄={x_bar:.4f}  '
                  f'ηkin={out["eta_kin_mean"][-1] * 1e3:.1f}mV  Newton {n_it}  KCL {kcl:.1e}', flush=True)
        # 종료: 전압창 / SOC 창 / 시간
        done_soc = (x_bar >= x_end - 1e-4) if not charge else (x_bar <= x_end + 1e-4)
        if V_cell < v_min or V_cell > v_max or done_soc or (t_max and t >= t_max):
            reason = ('V_cutoff' if (V_cell < v_min or V_cell > v_max) else
                      ('soc_end' if done_soc else 't_max'))
            if verbose:
                print(f'  step4-v2 END: {reason}  t={t:.0f}s  delivered '
                      f'{abs(x_bar - x_init) / abs(ocp.x100 - ocp.x0) * 100:.1f}% of 1C-capacity window', flush=True)
            break
        # 확산 전진 (면전류 → 표면 몰유속; J + = 리튬화)
        rad.J = i_am / (F_CONST * 4.0 * np.pi * rad.R ** 2)
        rad.step(dt)
        t += dt
        # adaptive Δt: 표면 SOC 스텝 제한
        dxs = np.max(np.abs(rad.J) * dt / (ocp.c_max * rad.R / 3.0) + 1e-30)
        dt = float(np.clip(dt * np.clip(dx_max / max(dxs, 1e-9), 0.5, 1.3), 0.2, dt_max))
    out = {k: np.asarray(v) for k, v in out.items()}
    out['x_final_per_particle'] = rad.mean_x()
    out['dead_particle'] = ~has_face
    out['I_app_A'] = I_app; out['I_1C_A'] = I_1C
    out['params'] = dict(c_rate=c_rate, d_s=d_s, i0=i0_ref, nr=nr, v_min=v_min,
                         c_max=ocp.c_max, x0=ocp.x0, x100=ocp.x100,
                         ocp_provenance=ocp.provenance, test_only=ocp.test_only)
    return out


# ---------------------------------------------------------------- selftests
def _selftest_radial():
    """구형확산 해석 체크 3종."""
    ok = True
    # 1) 질량보존 (기계정밀도): 일정 J 리튬화, Σ V_k Δx = Δt·J/(c_max·R)
    rad = RadialDiffusion(3, 25, np.array([2e-6, 5e-6, 1e-5]), 3e-14, 50000.0, 0.3)
    rad.J = np.array([1e-6, 2e-6, 0.5e-6])
    tot0 = (rad.x * rad.Vk).sum(1).copy()
    for _ in range(50):
        rad.step(2.0)
    got = (rad.x * rad.Vk).sum(1) - tot0
    exp = 50 * 2.0 * rad.J / (rad.c_max * rad.R)
    e1 = np.max(np.abs(got - exp) / exp)
    ok &= e1 < 1e-10
    print(f'radial mass conservation: max rel err {e1:.2e}  {"OK" if e1 < 1e-10 else "FAIL"}')
    # 2) 정상상태 무유속: J=0 → x 균일 유지 (초기 균일)
    rad = RadialDiffusion(1, 20, np.array([5e-6]), 3e-14, 50000.0, 0.5)
    for _ in range(100):
        rad.step(10.0)
    e2 = float(np.max(np.abs(rad.x - 0.5)))
    ok &= e2 < 1e-12
    print(f'radial equilibrium hold: max drift {e2:.2e}  {"OK" if e2 < 1e-12 else "FAIL"}')
    # 3) 단시간 √t 침투 (평면 극한): Δx_surf = 2J√(t/πD)/c_max, t ≪ R²/D
    R, D, cm = 10e-6, 1e-14, 50000.0
    rad = RadialDiffusion(1, 400, np.array([R]), D, cm, 0.3)
    rad.J = np.array([2e-6])
    dt, nstep = 0.05, 200                                   # t=10 s, √(Dt)=0.32µm ≪ R
    for _ in range(nstep):
        rad.step(dt)
    t = dt * nstep
    dx_num = float(rad.surf_x()[0] - 0.3)
    dx_ana = 2.0 * rad.J[0] * np.sqrt(t / (np.pi * D)) / cm
    e3 = abs(dx_num - dx_ana) / dx_ana
    ok &= e3 < 0.05                                          # 이산화 잔차 ~3% (계수버그는 수백%로 잡힘)
    print(f'radial √t (planar limit): num {dx_num:.4e} vs ana {dx_ana:.4e} '
          f'rel {e3:.3f}  {"OK" if e3 < 0.05 else "FAIL"}')
    return ok


def _build_sandwich(nxy=6, nz=12, vox_um=0.5):
    """v1 selftest와 같은 AM/SE 샌드위치 (입자 1개)."""
    sid = np.zeros((nxy, nxy, nz), np.int8)
    sid[:, :, :nz // 2] = 1
    sid[:, :, nz // 2:] = 6
    pid = np.where(sid == 1, 0, -1).astype(np.int32)
    return sid, pid, vox_um


def _selftest_cell():
    """결합해 체크: 평형 OCV 재현 / 저율 직렬-R / KCL / v1 분포 일치."""
    ok = True
    ocp = OCP.synthetic_test()
    # σ를 낮춰(1e-4 S/cm) 네트워크 저항과 BV 저항이 같은 자릿수가 되게 — 직렬-R 해석해가
    # 두 항 모두를 실제로 검증하도록 (고σ면 BV가 전부 지배해 네트워크 항 검증력이 없음)
    sid, pid, vox = _build_sandwich(nxy=6, nz=12, vox_um=5.0)
    se_cm, si_cm = 1e-4, 1e-4                                # S/cm
    sig_e = np.array([0., se_cm, 0., 0., 0., 0., 0.])
    sig_i = np.array([0., 0., 0., 0., 0., 0., si_cm])
    sysm = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=12 * vox, z_bot_um=0.0)
    # 1) I=0 → V=OCV(x0), η=0 (부호규약 셀프체크)
    x0 = ocp.x0
    i0_ref = 2.0
    U_f = np.full(sysm.n_bv, float(ocp.U(x0)))
    i0_f = np.full(sysm.n_bv, float(i0_of_x(i0_ref, x0)))
    phi = np.zeros(sysm.N)                                   # 평형 초기화 (simulate()와 동일 규약)
    phi[:sysm.n_e] = float(ocp.U(x0)); phi[sysm.iB] = float(ocp.U(x0))
    phi, I_f, r, it = sysm.newton(phi, U_f, i0_f, 0.0)
    e1 = abs(float(phi[sysm.iB]) - float(ocp.U(x0)))
    ok &= e1 < 1e-9
    print(f'cell equilibrium: V−OCV = {e1:.2e}  {"OK" if e1 < 1e-9 else "FAIL"}')
    # 2) 저율 직렬-R: V = OCV − I·R_series (선형화 BV g = 2·i0·A·β per face)
    I_small = 1e-10                                         # A — βη ≈ 0.03 선형 영역
    phi, I_f, r, it = sysm.newton(phi, U_f, i0_f, I_small)
    V = float(phi[sysm.iB])
    vox_m = vox * 1e-6
    nxy = sid.shape[0]; nzh = sid.shape[2] // 2
    se, si = se_cm * 100.0, si_cm * 100.0                   # S/m
    g_face = 2.0 * float(i0_of_x(i0_ref, x0)) * vox_m ** 2 * BETA
    R_col = (1.0 / (se * vox_m ** 2 / (0.5 * vox_m))                    # e-plate
             + (nzh - 1) / (se * vox_m)                                 # e-망 내부 (5칸)
             + (nzh - 1) / (si * vox_m)                                 # i-망 내부
             + 1.0 / (si * vox_m ** 2 / (0.5 * vox_m)))                 # i-plate
    R_ser = R_col / (nxy * nxy) + 1.0 / (g_face * nxy * nxy)            # 면병렬 + BV병렬
    V_exp = float(ocp.U(x0)) - I_small * R_ser
    e2 = abs(V - V_exp) / (I_small * R_ser)
    ok &= e2 < 1e-3
    print(f'cell low-rate series-R: ΔV num {float(ocp.U(x0)) - V:.3e} '
          f'vs ana {I_small * R_ser:.3e}  rel {e2:.2e}  {"OK" if e2 < 1e-3 else "FAIL"}')
    # 3) KCL: Σi_am = −I_f합 = I_app (방전 리튬화 규약)
    i_am = sysm.particle_current(I_f)
    e3 = abs(i_am.sum() - I_small) / I_small
    ok &= e3 < 1e-6
    print(f'cell KCL (galvanostatic): rel {e3:.2e}  {"OK" if e3 < 1e-6 else "FAIL"}')
    # 4) v1 분포 일치 (선형영역, 불균일 격자): 2입자 비대칭 → i_am 비율 v1 == v2
    from step3_sigma import solve_reaction_current
    sid2 = np.zeros((6, 6, 12), np.int8)
    sid2[:, :, 6:] = 6
    sid2[:3, :, :6] = 1                                      # 입자 0 (절반)
    sid2[3:, :, 2:6] = 2                                     # 입자 1 (얇게 — 비대칭)
    pid2 = np.full(sid2.shape, -1, np.int32)
    pid2[:3, :, :6] = 0; pid2[3:, :, 2:6] = 1
    sig_e2 = np.array([0., 1., 1., 0., 0., 0., 0.])
    sig_i2 = np.array([0., 0., 0., 0., 0., 0., 2.])
    gct_v1 = 2.0 * float(i0_of_x(i0_ref, x0)) * (0.5e-6) ** 2 * BETA   # [S] = v2 선형 g
    # v1은 code-units(σ[S/cm]·vox[µm])라 g 절대 스케일이 SI와 다름 — '분포' 비교는 g_ct/g_net
    # 비만 맞으면 됨.  g_code/g_SI = (σ_Scm·vox_um)/(100·σ_Scm·vox_um·1e-6) = 1e4 (vox 무관).
    g_v1 = gct_v1 * 1e4
    rv1 = solve_reaction_current(sid2, sig_e2, sig_i2, pid2, 2, 0.5, g_v1,
                                 z_top_um=6.0, z_bot_um=0.0)
    sys2 = CellSystem(sid2, sig_e2, sig_i2, pid2, 2, 0.5, z_top_um=6.0, z_bot_um=0.0)
    U2 = np.full(sys2.n_bv, float(ocp.U(x0)))
    i02 = np.full(sys2.n_bv, float(i0_of_x(i0_ref, x0)))
    phi2 = np.zeros(sys2.N)
    phi2[:sys2.n_e] = float(ocp.U(x0)); phi2[sys2.iB] = float(ocp.U(x0))
    phi2, I_f2, _, _ = sys2.newton(phi2, U2, i02, 1e-8)
    a2 = sys2.particle_current(I_f2)
    frac_v1 = rv1['i_am'] / rv1['i_am'].sum()
    frac_v2 = a2 / a2.sum()
    e4 = float(np.max(np.abs(frac_v1 - frac_v2)))
    ok &= e4 < 1e-4
    print(f'cell v1-regression (2-particle split): v1 {frac_v1.round(6)} vs v2 {frac_v2.round(6)} '
          f'Δmax {e4:.2e}  {"OK" if e4 < 1e-4 else "FAIL"}')
    return ok


def _selftest_discharge():
    """샌드위치 풀 방전 스모크: 용량 적산 일치 + V 단조 하강(저율) + 보존."""
    ok = True
    ocp = OCP.synthetic_test()
    sid, pid, vox = _build_sandwich(nxy=4, nz=8)
    sig_e = np.array([0., 1., 0., 0., 0., 0., 0.])
    sig_i = np.array([0., 0., 0., 0., 0., 0., 2.])
    sysm = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    # r_p=10µm: 용량(=I_app)을 키워 KCL 검증이 float64 잔차 노이즈 바닥(~1e-17 A) 위에서 놀게 함
    # (r=1µm이면 I_app~7e-13 A → 노이즈만으로 rel 1e-5가 나옴 — 솔버 한계 아님, 스케일 문제)
    r_p = np.array([10.0e-6])
    out = simulate(sysm, ocp, r_p, d_s=1e-13, i0_ref=5.0, c_rate=0.2, nr=15,
                   v_min=2.0, dx_max=0.05, dt_init=5.0, dt_max=600.0, verbose=False)
    # 용량 적산: Δx̄ = ∫I dt/(F·c_max·ΣV_p) — 시뮬 x̄ 전진과 일치해야
    dt_arr = np.diff(out['t'])
    q_As = (out['I_app_A'] * dt_arr).sum()
    dx_exp = q_As / (F_CONST * ocp.c_max * (4 / 3 * np.pi * r_p ** 3).sum())
    dx_got = out['x_mean'][-1] - out['x_mean'][0]
    e1 = abs(dx_got - dx_exp) / abs(dx_exp)
    ok &= e1 < 5e-3
    print(f'discharge coulomb count: Δx̄ {dx_got:.4f} vs ∫I {dx_exp:.4f}  rel {e1:.2e}  '
          f'{"OK" if e1 < 5e-3 else "FAIL"}')
    dV = np.diff(out['V'])
    mono = float((dV > 1e-6).mean())
    ok &= mono < 0.02
    print(f'discharge V monotone↓ (linear OCP): rising steps {mono * 100:.1f}%  '
          f'{"OK" if mono < 0.02 else "FAIL"}')
    okk = float(np.max(out['kcl_rel'])) < 1e-6
    ok &= okk
    print(f'discharge KCL all steps: max {np.max(out["kcl_rel"]):.1e}  {"OK" if okk else "FAIL"}')
    return ok


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description='STEP4-v2 galvanostatic voxel-DFN (SSB)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--grid', help='step4_grid.npz (mpm_webapp_payload --save-step4-grid)')
    ap.add_argument('--ocp-csv', help='U(x) 테이블 CSV (step4_pybamm_anchor --export-params)')
    ap.add_argument('--params-json', help='c_max/x0/x100/provenance JSON (같은 export)')
    ap.add_argument('--ocp-test', action='store_true',
                    help='합성 TEST-ONLY OCP (앵커 파일 없이 스모크; 결과에 test_only 라벨)')
    ap.add_argument('--c-rate', type=float, default=0.5)
    ap.add_argument('--charge', action='store_true', help='충전 방향 (기본 방전)')
    ap.add_argument('--d-s', type=float, default=3e-14,
                    help='D_s [m²/s] 기본 3e-14 (Kang&Shin 2025 FEM; 문헌 1e-14–1e-13)')
    ap.add_argument('--i0', type=float, default=2.0, help='i0_ref [A/m²] (v1 훅 유지, ⚠F1)')
    ap.add_argument('--nr', type=int, default=20)
    ap.add_argument('--v-min', type=float, default=3.0, help='방전 컷오프 [V vs Li] (운전 설정)')
    ap.add_argument('--v-max', type=float, default=4.5)
    ap.add_argument('--t-max', type=float, default=None)
    ap.add_argument('--gpu', action='store_true')
    ap.add_argument('--out', default='step4_dyn_out.npz')
    a = ap.parse_args()
    global GPU
    GPU = bool(a.gpu)
    if a.selftest:
        ok = _selftest_radial()
        ok &= _selftest_cell()
        ok &= _selftest_discharge()
        print('STEP4-V2 SELFTEST', 'PASS' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    if not a.grid:
        ap.error('--grid required (or --selftest)')
    g = np.load(a.grid, allow_pickle=False)
    sid = g['sid']; pid = g['pid']
    vox_um = float(g['vox_um']); z_top = float(g['z_top_um'])
    sig_e = g['sig_e_S_cm']; sig_i = g['sig_i_S_cm']
    r_um = g['am_r_um']
    if a.ocp_test:
        ocp = OCP.synthetic_test()
        print('⚠ TEST-ONLY synthetic OCP — 결과는 수치 스모크 전용 (§F1: 물리값 아님)', flush=True)
    else:
        if not (a.ocp_csv and a.params_json):
            ap.error('--ocp-csv/--params-json required (§F1 앵커; 임시 스모크는 --ocp-test)')
        ocp = OCP.load(a.ocp_csv, a.params_json)
        print(f'  OCP: {ocp.provenance}  c_max={ocp.c_max:g}  x0={ocp.x0}  x100={ocp.x100}', flush=True)
    sysm = CellSystem(sid, sig_e, sig_i, pid, len(r_um), vox_um, z_top_um=z_top, z_bot_um=0.0)
    out = simulate(sysm, ocp, r_um * 1e-6, a.d_s, a.i0, a.c_rate, nr=a.nr,
                   v_min=a.v_min, v_max=a.v_max, t_max=a.t_max, charge=a.charge)
    meta = out.pop('params')
    np.savez_compressed(a.out, **out, params_json=json.dumps(meta))
    print(f'saved {a.out}  (steps {len(out["t"])}, V {out["V"][0]:.3f}→{out["V"][-1]:.3f}, '
          f'x̄ {out["x_mean"][0]:.3f}→{out["x_mean"][-1]:.3f})')


if __name__ == '__main__':
    main()
