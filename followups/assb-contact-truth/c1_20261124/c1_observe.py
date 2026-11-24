"""C1 관측 연산자 (설계서 `followups/assb-contact-truth/DESIGN_v1.md` §4-2 · §4-3) — 진단 전용 · 인용 금지.

F1 펄스 맞춤 · 정합 필터 z · GITT 비 · 첫 충전 상한 · 참 θ 몫 · C1b 관측 O1–O4 · 잡음 (사본 `src/curves.py:add_noise`).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

BANDS = {"O1": (3.83, 4.69), "O2": (0.86, 0.96), "O3": (-0.227, -0.167), "O4": (-0.057, -0.027)}   # §5-3 (미리 고정)


# --------------------------------------------------------------------------------------------
# F1 — V(t) = V₀ − I·[R0 + R_p·(1 − e^{−t/τ}) + k·√t]  (변수 사영: τ 만 비선형)
# --------------------------------------------------------------------------------------------
_NAN_FIT = {"R0": np.nan, "Rp": np.nan, "tau": np.nan, "k": np.nan, "C": np.nan, "Rp_over_k": np.nan,
            "se_R0": np.nan, "se_Rp": np.nan, "se_tau": np.nan, "se_k": np.nan, "rss": np.nan, "n": 0,
            "resolved": False}


def _design(t, tau):
    return np.column_stack([np.ones_like(t), -np.expm1(-t / tau), np.sqrt(t)])


def _rss_tau(s, t, y):
    X = _design(t, np.exp(s))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    return float(r @ r)


def fit_f1(t, v, *, I: float, V0: float, dt: float, n_min: int = 5) -> dict:
    """창 안 표본 (t > 0 — 계단 뒤 시간) 의 F1 맞춤. 표본 < n_min → 전부 NaN. τ̂ < 2Δt → τ · C NaN (미해상)."""
    t = np.asarray(t, float)
    v = np.asarray(v, float)
    if t.size < n_min or I == 0:
        return dict(_NAN_FIT, n=int(t.size))
    y = (V0 - v) / I
    s_lo = np.log(0.1 * min(dt, t[0]))
    s_hi = np.log(100.0 * t[-1])
    grid = np.linspace(s_lo, s_hi, 241)
    vals = np.array([_rss_tau(s, t, y) for s in grid])
    i = int(np.argmin(vals))
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, grid.size - 1)]
    if b > a:
        res = minimize_scalar(_rss_tau, bounds=(a, b), args=(t, y), method="bounded",
                              options={"xatol": 1e-13, "maxiter": 500})
        s_best = float(res.x) if res.fun <= vals[i] else float(grid[i])
    else:
        s_best = float(grid[i])
    tau = float(np.exp(s_best))
    X = _design(t, tau)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    R0, Rp, k = (float(b_) for b_ in beta)
    r = y - X @ beta
    rss = float(r @ r)
    n = t.size
    # 표준오차 (4 매개 Jacobian · s² = RSS/(n−4)) — y 공간 (전압 ÷ I) 그대로
    J = np.column_stack([np.ones_like(t), -np.expm1(-t / tau), -Rp * (t / tau ** 2) * np.exp(-t / tau), np.sqrt(t)])
    s2 = rss / max(n - 4, 1)
    try:
        cov = s2 * np.linalg.inv(J.T @ J)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(4, np.nan)
    out = {"R0": R0, "Rp": Rp, "tau": tau, "k": k, "C": tau / Rp if Rp != 0 else np.nan,
           "Rp_over_k": Rp / k if k != 0 else np.nan, "se_R0": float(se[0]), "se_Rp": float(se[1]),
           "se_tau": float(se[2]), "se_k": float(se[3]), "rss": rss, "n": int(n), "resolved": True}
    if tau < 2.0 * dt:
        out.update({"tau": np.nan, "C": np.nan, "resolved": False})
    return out


# --------------------------------------------------------------------------------------------
# 정합 필터 z (§4-2) — 상대 팔 가족을 log f 세 점 이차 보간으로 이어 프로파일
# --------------------------------------------------------------------------------------------
def _project_out(vecs, i_t):
    nrm = float(i_t @ i_t)
    if nrm == 0.0:
        return vecs
    return [x - i_t * (float(x @ i_t) / nrm) for x in vecs]


def _pieces(s_nodes):
    """오름차순 노드 → (구간 [lo, hi], 가장 가까운 세 노드의 지표) 목록."""
    n = s_nodes.size
    br = np.unique(np.concatenate([s_nodes, 0.5 * (s_nodes[1:] + s_nodes[:-1])]))
    out = []
    for lo, hi in zip(br[:-1], br[1:]):
        mid = 0.5 * (lo + hi)
        order = np.lexsort((np.arange(n), np.abs(s_nodes - mid)))
        out.append((lo, hi, np.sort(order[:3])))
    return out


def z_profile(target, family, logf, *, i_t, sigma: float, dR0: str) -> float:
    """min over (f′ ∈ [min f, max f], ΔR0) ‖target − V_K(f′) + I·ΔR0‖₂ / σ. dR0 ∈ {"none", "free"}."""
    target = np.asarray(target, float)
    family = np.atleast_2d(np.asarray(family, float))
    logf = np.atleast_1d(np.asarray(logf, float))
    i_t = np.asarray(i_t, float)
    if dR0 not in ("none", "free"):
        raise ValueError(dR0)
    order = np.argsort(logf)
    s_nodes, fam = logf[order], family[order]
    nf = s_nodes.size
    if nf == 1:
        r = target - fam[0]
        if dR0 == "free":
            r = _project_out([r], i_t)[0]
        return float(np.sqrt(r @ r)) / sigma
    best = np.inf
    pieces = _pieces(s_nodes) if nf >= 3 else [(s_nodes[0], s_nodes[1], np.array([0, 1]))]
    for lo, hi, idx in pieces:
        ss = s_nodes[idx]
        V = fam[idx]
        # V(s) = c0 + c1 s + c2 s²  (Lagrange → 거듭제곱 계수)
        if idx.size == 3:
            M = np.vander(ss, 3, increasing=True)
        else:
            M = np.vander(ss, 2, increasing=True)
        coef = np.linalg.solve(M, V)                     # 행 = 거듭제곱 계수 벡터
        a = target - coef[0]
        b = coef[1]
        c = coef[2] if idx.size == 3 else np.zeros_like(a)
        if dR0 == "free":
            a, b, c = _project_out([a, b, c], i_t)
        aa, ab, ac, bb, bc, cc = a @ a, a @ b, a @ c, b @ b, b @ c, c @ c

        def q(s):
            return aa - 2 * s * ab + s * s * (bb - 2 * ac) + 2 * s ** 3 * bc + s ** 4 * cc

        # d/ds: -2ab + 2s(bb-2ac) + 6 s² bc + 4 s³ cc = 0
        cand = [lo, hi]
        roots = np.roots([4 * cc, 6 * bc, 2 * (bb - 2 * ac), -2 * ab]) if (cc != 0 or bc != 0) else \
            ([ab / (bb - 2 * ac)] if (bb - 2 * ac) != 0 else [])
        for rt in np.atleast_1d(roots):
            if abs(np.imag(rt)) < 1e-12 and lo <= np.real(rt) <= hi:
                cand.append(float(np.real(rt)))
        for s in cand:
            val = q(s)
            if val < best:
                best = val
    return float(np.sqrt(max(best, 0.0))) / sigma


def z_cell(famA, famK, logf, *, idx: int, i_t, sigma: float, dR0: str) -> float:
    """대칭 판: A(f) 를 K 가족으로 · K(f) 를 A 가족으로 맞춘 것 중 작은 쪽."""
    zAK = z_profile(famA[idx], famK, logf, i_t=i_t, sigma=sigma, dR0=dR0)
    zKA = z_profile(famK[idx], famA, logf, i_t=i_t, sigma=sigma, dR0=dR0)
    return min(zAK, zKA)


# --------------------------------------------------------------------------------------------
# GITT 비 (§4-2 O2) · R6 기록
# --------------------------------------------------------------------------------------------
def gitt_ratio(*, t_pulse, v_pulse, t_rest, v_rest, v_pre) -> dict:
    t_pulse = np.asarray(t_pulse, float)
    t_rest = np.asarray(t_rest, float)
    i1 = int(np.argmin(np.abs(t_pulse - 1.0)))            # 펄스 시작 뒤 첫 표본 (t = 1 s)
    dE_t = float(v_pulse[-1] - v_pulse[i1])
    dE_s = float(v_rest[-1] - v_pre)
    i10 = int(np.argmin(np.abs(t_rest - 600.0)))
    return {"dE_t": dE_t, "dE_s": dE_s, "ratio": dE_s / dE_t if dE_t != 0 else np.nan,
            "dE_s_10min": float(v_rest[i10] - v_pre)}


def coverage_ratio(r_var: dict, r_ref: dict) -> float:
    return r_var["ratio"] / r_ref["ratio"]


# --------------------------------------------------------------------------------------------
# 첫 충전 상한 (O5) · 참 θ 몫 · C1b 관측
# --------------------------------------------------------------------------------------------
def first_charge_bound(*, Qch_ref, Qch_var, Qdis_ref, Qdis_var) -> float:
    """θ 몫 상한 = Q_dis,기준 × (ΔQ_ch/Q_ch) / ΔQ_dis (65호 digest 식 · 정식 줄 (저))."""
    return Qdis_ref * ((Qch_ref - Qch_var) / Qch_ref) / (Qdis_ref - Qdis_var)


def true_theta_share(*, Qdis_theta1, Qdis_theta, Qdis_ref) -> float:
    """(같은 p · f_σ 의 θ=1 − θ<1 첫 방전 차) ÷ (기준 대비 첫 방전 결손)."""
    return (Qdis_theta1 - Qdis_theta) / (Qdis_ref - Qdis_theta)


def c1b_observables(ref: dict, var: dict) -> dict:
    return {"O1": var["Rp"] / ref["Rp"], "O2": var["gitt_ratio"] / ref["gitt_ratio"],
            "O3": var["Qdis"] / ref["Qdis"] - 1.0, "O4": var["Qch"] / ref["Qch"] - 1.0}


def in_bands(o: dict) -> bool:
    return bool(all(BANDS[k][0] <= o[k] <= BANDS[k][1] for k in BANDS))


# --------------------------------------------------------------------------------------------
# 관측 표본 · 잡음
# --------------------------------------------------------------------------------------------
def observe_indices(t_rel, dt_obs: float, truth_dt=(1e-4, 1e-2), dense: float = 0.5):
    """계단 뒤 상대 시간 t_rel 에서 Δt 관측 표본 지표. truth 간격보다 촘촘한 관측은 truth 점 그대로 (§4-2)."""
    t_rel = np.asarray(t_rel, float)
    k = np.round(t_rel / dt_obs, 6)
    on_grid = np.abs(k - np.round(k)) < 1e-6
    if dt_obs < truth_dt[1]:
        # 촘촘 구간 (< dense) 은 Δt 배수만 · 성긴 구간은 truth 점 전부
        coarse = t_rel >= dense - 1e-12
        return np.where(on_grid | coarse)[0]
    return np.where(on_grid)[0]


def noisy(v, sigma: float, seed: int):
    from src.curves import add_noise   # 사본 (읽기 재사용 — 새로 짜지 않는다 · §4-3)
    return add_noise(np.asarray(v, float), sigma, seed)
