"""fitting.py — α·β 최적화 (33p 이식) + 열화모드 환산 (21p).

정방향(모드→곡선)은 Phase 2의 modes.py, 역방향(곡선→모드)이 여기다.
`windowed_curve`는 원본 코드 그대로 재사용한다 (src/curves.py).

────────────────────────────────────────────────────────────────────────
정규화 규약 ★ (33p bound를 이해하는 열쇠)

곡선의 x축은 **각 셀 자기 용량**으로 정규화돼 있다 (extract_curves).
이때 half-cell 곡선 재구성은

    U_PE(x) = f_PE_ref( (x − β_PE)/α_PE )

이고, 전하 보존으로부터 (유도: docs/05_HANDOFF.md)

    α_PE = (1 − LAM_PE) / r,     r = Q_degraded / Q_reference

가 된다. 즉 **α는 열화율이 아니라 "전극 용량 / 셀 용량" 비**이며,
용량이 줄면(r<1) α는 1보다 커진다. 역환산은 21p 식 그대로:

    LAM_PE = 1 − α_PE·r
    LAM_NE = 1 − α_NE·r
    LLI    = 1 − r·[w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE)]   ← src/inventory.py 유도

⚠ α = 1.00 은 곧 LAM = 1 − r = **용량손실과 같음**을 뜻한다.
   33p의 lb = [1.00, …]는 이 지점을 하한으로 못 박으므로,
   최적화가 하한에 붙으면 자동으로 "LAM_PE ≈ LAM_NE ≈ 용량손실"이 나온다.
   22p의 결과 패턴과 정확히 일치 → bound active 여부를 반드시 검사한다.
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import minimize

from src.curves import windowed_curve

log = logging.getLogger(__name__)

PARAM_NAMES = ("a_pe", "b_pe", "a_ne", "b_ne")


# ---------------------------------------------------------------- 정방향

def make_ref_interp(x: np.ndarray, y: np.ndarray):
    """reference half-cell 곡선 보간자. 원본과 동일하게 범위 밖은 끝값 유지."""
    m = np.isfinite(x) & np.isfinite(y)
    return interp1d(x[m], y[m], bounds_error=False,
                    fill_value=(y[m][0], y[m][-1]))


def reconstruct(p, f_pe_ref, f_ne_ref, x: np.ndarray):
    """p = [α_PE, β_PE, α_NE, β_NE] → (PE, NE, full cell). 창 밖은 NaN."""
    a_pe, b_pe, a_ne, b_ne = p
    pe = windowed_curve(f_pe_ref, x, a_pe, b_pe)
    ne = windowed_curve(f_ne_ref, x, a_ne, b_ne)
    return pe, ne, pe - ne


def window_shortfall(p, x_min: float = 0.0, x_max: float = 1.0) -> float:
    """재구성 창이 관측 구간 [x_min, x_max]를 못 덮는 양 (연속량).

    전극의 창은 x ∈ [β, β+α]. 관측 구간을 벗어난 만큼을 더해서 돌려준다.
    목적함수 벌점이 이 값에 비례하면 landscape가 매끄러워져
    "창을 넓혀라"는 방향이 항상 살아 있다 (점 개수 세기는 계단형이라 갇힌다).
    """
    a_pe, b_pe, a_ne, b_ne = p
    total = 0.0
    for a, b in ((a_pe, b_pe), (a_ne, b_ne)):
        total += max(0.0, b - x_min) + max(0.0, x_max - (b + a))
    return total


# ---------------------------------------------------------------- 역환산

def to_degradation_modes(p, r: float = 1.0, convention: str = "derived",
                         w_pe: float | None = None, w_ne: float | None = None,
                         kappa: float | None = None) -> dict:
    """α·β → LAM_PE / LAM_NE / LLI.

    convention:
      "derived" — ★ 기본값. 전하 보존으로 유도한 식 (src/inventory.py 참조)
                    LLI = 1 − r·[w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE)]
                  w_pe·w_ne·kappa 가 필요하며, reference_inventory()로 구한다.
      "paper"   — 21p 식. 가중치(w_PE=1,w_NE=0,κ=1)도 다르고 β 항 부호도 반대다.
      "code"    — 원본 슬라이더 식 (r 미반영).

    합성 격자 95조건 평균 |오차|: derived 0.012 / paper 0.128 / code 0.200
    """
    a_pe, b_pe, a_ne, b_ne = p
    lam_pe = 1.0 - a_pe * r
    lam_ne = 1.0 - a_ne * r

    if convention == "derived":
        if w_pe is None or w_ne is None or kappa is None:
            raise ValueError("derived 규약에는 w_pe·w_ne·kappa가 필요합니다 "
                             "(src.inventory.reference_inventory 사용)")
        lli = 1.0 - r * (w_pe * a_pe + w_ne * a_ne + kappa * (b_ne - b_pe))
    elif convention == "paper":
        lli = 1.0 - (a_pe + b_pe - b_ne) * r
    elif convention == "code":
        lli = (1.0 - a_pe) + (b_pe - b_ne)
    else:
        raise ValueError(f"알 수 없는 convention: {convention}")
    return {"lam_pe": float(lam_pe), "lam_ne": float(lam_ne), "lli": float(lli)}


def to_modes_halfcell(p, p_ini, r: float) -> dict:
    """★ Case 1 — full-range half-cell OCV 기준에서의 역환산 (21p 식 원형).

    이 기준에서는 α·β가 논문과 같은 의미를 갖는다.
        α_PE = C_PE/C_full,  β_PE = −y0·α_PE
        α_NE = C_NE/C_full,  β_NE = (z0−1)·α_NE      (s = 1−z 로 방전방향 정렬)
    따라서 셀별 상수 없이 21p 식이 그대로 성립한다.

        LAM_PE = 1 − α_PE·r/α_PE,ini
        LAM_NE = 1 − α_NE·r/α_NE,ini
        LLI    = 1 − (α_NE + β_NE − β_PE)·r / (α_NE,ini + β_NE,ini − β_PE,ini)

    LLI의 전극 기준(NE)은 전하 보존에서 나온다: 완충 상태에서
    PE 보유 Li = −β_PE·C_full, NE 보유 Li = (α_NE+β_NE)·C_full 이므로
    총재고 = (α_NE + β_NE − β_PE)·C_full.
    비교용으로 21p 표기 그대로인 PE 기준도 함께 반환한다.
    """
    a_pe, b_pe, a_ne, b_ne = p
    a_pe0, b_pe0, a_ne0, b_ne0 = p_ini
    inv_ne = a_ne0 + b_ne0 - b_pe0
    inv_pe = a_pe0 + b_pe0 - b_ne0
    return {
        "lam_pe": float(1.0 - a_pe * r / a_pe0),
        "lam_ne": float(1.0 - a_ne * r / a_ne0),
        "lli": float(1.0 - (a_ne + b_ne - b_pe) * r / inv_ne) if inv_ne else float("nan"),
        "lli_pe_basis": float(1.0 - (a_pe + b_pe - b_ne) * r / inv_pe) if inv_pe else float("nan"),
    }


def modes_to_params(lam_pe: float, lam_ne: float, lli: float, r: float) -> np.ndarray:
    """역함수 — 참값에서 기대되는 α·β (테스트·진단용, "paper" 규약)."""
    a_pe = (1.0 - lam_pe) / r
    a_ne = (1.0 - lam_ne) / r
    # LLI = 1 − (a_pe + b_pe − b_ne)·r  →  b_pe − b_ne = (1−LLI)/r − a_pe
    d_beta = (1.0 - lli) / r - a_pe
    return np.array([a_pe, d_beta, a_ne, 0.0])


# ---------------------------------------------------------------- 최적화

@dataclass
class FitResult:
    p: np.ndarray
    J: float
    converged: bool
    n_eval: int
    bound_active: tuple                      # 파라미터별 bound 접촉 여부
    n_restarts: int = 1
    n_restarts_agree: int = 1                # 최적해와 사실상 같은 해에 도달한 수
    p_spread: float = 0.0                    # restart 간 해의 최대 퍼짐
    J_spread: float = 0.0
    restarts: list = field(default_factory=list)

    @property
    def any_bound_active(self) -> bool:
        return any(self.bound_active)


def _bound_active(p, lb, ub, tol: float = 1e-4) -> tuple:
    return tuple(bool(abs(v - l) < tol or abs(v - u) < tol)
                 for v, l, u in zip(p, lb, ub))


# dQ/dV 항이 들어가면 최소점이 바늘처럼 뾰족해진다 (실측: α를 0.001 흔들면
# J가 0 → 0.12). 기본 허용오차(xatol=1e-4)로는 그 바닥을 못 찍어서, 목적함수의
# 성질이 아니라 optimizer의 게으름이 결과로 보고돼 버린다. 그래서 조인다.
_NM_OPTIONS = {"xatol": 1e-7, "fatol": 1e-12, "maxiter": 4000, "maxfev": 4000}


def _minimize_until_stable(objective, x0, bounds, method: str,
                           max_rounds: int = 4, tol: float = 1e-12):
    """Nelder-Mead는 단순체가 찌그러지면 조기 종료한다. 해를 시작점으로 재시작해
    개선이 멈출 때까지 반복한다 (최적화 실패와 목적함수의 평평함을 구분하기 위함)."""
    opts = _NM_OPTIONS if method == "Nelder-Mead" else None
    best_x, best_f, ok, nfev = np.asarray(x0, float), np.inf, False, 0
    cur_x = best_x
    for _ in range(max_rounds):
        res = minimize(objective, cur_x, method=method, bounds=bounds, options=opts)
        nfev += int(res.nfev)
        if not np.isfinite(res.fun):
            break
        improved = best_f - float(res.fun)
        cur_x, ok = np.asarray(res.x, float), bool(res.success)
        # 리뷰 F16: best_x는 개선됐을 때만 갱신 — 반환 (p, J) 불일치 방지
        if float(res.fun) < best_f:
            best_f = float(res.fun)
            best_x = cur_x
        if improved < tol:
            break
    return best_x, best_f, ok, nfev


def fit(objective, init, lb, ub, n_restarts: int = 1, seed: int = 0,
        method: str = "Nelder-Mead", agree_tol: float = 1e-3,
        adaptive: bool = True, warm_init: bool = False) -> FitResult:
    """multi-start 최적화.

    ★ restart마다 다른 해에 수렴하면 그 자체가 degeneracy의 직접 증거다.
      (같은 데이터·같은 코드인데 답이 갈린다는 뜻)
      n_restarts_agree / p_spread 로 정량화한다.

    method 기본값이 Nelder-Mead인 이유: reference 곡선 보간이 조각선형이라
    L-BFGS-B의 수치 gradient가 무의미하다 (실측 α 오차 0.07 vs NM 0.00003).

    ★ warm_init — restart 0의 초기값이 앞 목적함수에서 물려받은 해인가 (F25).
      `restarts`를 J 오름차순으로 저장하므로 **순서만으로는 어느 것이 warm
      start였는지 알 수 없다.** 인덱스로 추정하던 사후 진단은 실제로는 warm이
      아니라 best restart를 버리고 있었다. 그래서 restart마다 출처를 같이
      적는다 — 나중에 지표를 바꿔도 원본에서 다시 셀 수 있어야 한다.
    """
    lb = np.asarray(lb, float)
    ub = np.asarray(ub, float)
    init = np.clip(np.asarray(init, float), lb, ub)
    bounds = list(zip(lb, ub))
    rng = np.random.default_rng(seed)

    results = []
    n_max = max(1, n_restarts)
    for k in range(n_max):
        x0 = init if k == 0 else rng.uniform(lb, ub)
        # ★ F31 — restart 0은 무작위가 아니다. warm start를 받았으면 "warm",
        #   아니면 공통 결정론적 초기값이라 "base_init"이다. 둘을 뭉치면
        #   "무작위 restart끼리만" 비교가 성립하지 않는다 — warm을 받은
        #   목적함수만 restart 0이 빠지고, 나머지는 base_init이 남는다.
        src = ("warm" if warm_init else "base_init") if k == 0 else "random"
        try:
            x, f, ok, nfev = _minimize_until_stable(objective, x0, bounds, method)
            results.append((x, f, ok, nfev, k, src))
        except Exception as e:  # noqa: BLE001
            log.debug("restart %d 실패: %s", k, e)
        # 적응적 multi-start: 앞의 두 번이 같은 해로 모이면 더 돌릴 이유가 없다.
        # 갈리는 조건(= degeneracy 후보)에서만 끝까지 돌려서 비용을 아낀다.
        if adaptive and k == 1 and len(results) == 2:
            (p0, j0, *_), (p1, j1, *_) = results
            if (abs(j0 - j1) <= agree_tol * max(1.0, abs(min(j0, j1)))
                    and np.max(np.abs(p0 - p1)) <= agree_tol * 10):
                break

    if not results:
        nan = np.full(4, np.nan)
        return FitResult(nan, float("nan"), False, 0, (False,) * 4, n_restarts, 0)

    # ★ J 오름차순 정렬 — 그래서 인덱스는 더 이상 restart 순서가 아니다.
    #   출처(restart index, warm 여부)는 튜플 안에 같이 실려 보존된다 (F25).
    results.sort(key=lambda t: t[1])
    p_best, J_best, ok, _, _, _ = results[0]      # (p, J, ok, nfev, i, source)
    nfev = sum(t[3] for t in results)     # 리뷰 F17: 전체 restart의 평가 수 합

    # 최적해와 J가 사실상 같은데 p가 다른 해 = 평평한 골짜기
    near = [p for p, J, *_ in results if abs(J - J_best) <= agree_tol * max(1.0, abs(J_best))]
    agree = sum(1 for p in near if np.max(np.abs(p - p_best)) <= agree_tol * 10)
    spread = float(np.max([np.max(np.abs(p - p_best)) for p in near])) if near else 0.0
    j_spread = float(max(J for _, J, *_ in results) - J_best)

    return FitResult(
        p=p_best, J=J_best, converged=ok, n_eval=nfev,
        bound_active=_bound_active(p_best, lb, ub),
        n_restarts=len(results), n_restarts_agree=agree,
        p_spread=spread, J_spread=j_spread,
        # F25/F31: (p, J)만 적으면 출처가 사라진다. dict로 바꿔 restart 인덱스와
        # 출처(warm / base_init / random)를 같이 남긴다.
        # 옛 형식 [(p, J), ...]도 읽는 쪽에서 받는다.
        restarts=[{"p": p.tolist(), "J": J, "i": k, "source": s,
                   "warm": s == "warm"}
                  for p, J, _, _, k, s in results],
    )


# ---------------------------------------------------------------- grid 구동

REF_KEY = ("lli", "lam_pe", "lam_ne")


def extract_reference(df):
    """grid 결과에서 reference 조건(모든 모드 0, 노이즈 0)의 곡선을 꺼낸다."""
    m = (df["lli"] == 0) & (df["lam_pe"] == 0) & (df["lam_ne"] == 0)
    if "noise" in df.columns:
        m &= df["noise"] == 0
    ref = df[m]
    if ref.empty:
        raise RuntimeError("reference 조건(lli=lam_pe=lam_ne=0, noise=0)이 결과에 없음")
    ref = ref[ref["cond_id"] == ref["cond_id"].iloc[0]].sort_values("x_norm")
    return ref


def build_reference_interps(mode: str, grid_ref: dict, hc=None):
    """fitting 기준 곡선. mode = "grid" (기준 셀 창) | "halfcell" (전 범위 반쪽셀)."""
    if mode == "grid":
        return (make_ref_interp(grid_ref["x"], grid_ref["pe"]),
                make_ref_interp(grid_ref["x"], grid_ref["ne"]))
    if mode == "halfcell":
        # PE: s ∝ y (방전 중 리튬화 → 증가) / NE: s ∝ 1−z (방전방향으로 정렬)
        # ★ windowed_curve가 s∈[0,1]을 가정하므로 **테이블 구간을 [0,1]로 정규화**한다.
        #   (정규화 없이 넣으면 확보 범위 밖이 전부 끝값으로 평평해져 fitting이 망가진다
        #    — 실측: LAM 오차 0.10 vs 정규화 후 개선)
        #   이때 α는 "테이블 구간 대비" 비율이 되지만, LAM은 ini로 정규화되므로
        #   구간 상수가 약분돼 식은 그대로 성립한다.
        y, u_pe = np.asarray(hc["y_pe"]), np.asarray(hc["u_pe"])
        z, u_ne = np.asarray(hc["z_ne"]), np.asarray(hc["u_ne"])
        s_pe = (y - y.min()) / (y.max() - y.min())
        s_ne = 1.0 - z
        s_ne = (s_ne - s_ne.min()) / (s_ne.max() - s_ne.min())
        order = np.argsort(s_ne)
        return (make_ref_interp(s_pe, u_pe), make_ref_interp(s_ne[order], u_ne[order]))
    raise ValueError(f"알 수 없는 reference 모드: {mode}")


def _fit_one(task: dict) -> list[dict]:
    """한 조건에 대해 목적함수 4종을 각각 fitting (워커에서 실행)."""
    from src.objective import compute_features, default_scales, make_objective

    x = np.asarray(task["x"])
    grid_ref = {"x": np.asarray(task["ref_x"]), "pe": np.asarray(task["ref_pe"]),
                "ne": np.asarray(task["ref_ne"])}
    ref_pe, ref_ne = build_reference_interps(task["reference"], grid_ref,
                                             task.get("halfcell"))
    obj_cfg = task["obj_cfg"]

    target = compute_features(x, np.asarray(task["v_target"]), obj_cfg, with_peaks=True)
    # 리뷰 F9: scale은 조건 불변이어야 J를 격자 전체에서 비교할 수 있다.
    # ref_feat를 타깃 격자(target.v_grid)로 계산하면 dqdv scale이 조건마다 미세하게
    # 달라지므로, reference **자기 격자**로 계산한다 (scale은 상수라 격자 불일치 무해).
    ref_feat = compute_features(np.asarray(task["ref_x"]), np.asarray(task["ref_full"]),
                                obj_cfg)
    scales = default_scales(ref_feat)

    def model_fn(p):
        _, _, full = reconstruct(p, ref_pe, ref_ne, x)
        return x, full

    obs = np.isfinite(target.v)
    x_lo, x_hi = float(x[obs].min()), float(x[obs].max())

    def shortfall(p):
        return window_shortfall(p, x_lo, x_hi)

    # ★ 계단식 초기값 (F20, 2026-08-06 실측).
    #
    #   dQ/dV 항이 들어간 목적함수는 **최소가 정답에 있는데도** 찾지 못한다.
    #   무열화 조건 실측: J(정답)=0 인데 최적화는 J=0.402에서 멈추고
    #   LAM_PE=-6.5%p 를 답했다. 300점 곡선의 dQ/dV는 뾰족한 이산 신호라
    #   α가 조금만 움직여도 피크가 격자 칸을 넘으며 J가 불연속으로 튄다
    #   → 전역최소의 유인역(basin)이 사실상 0폭.
    #
    #   그래서 **부드러운 항으로 먼저 풀고 그 해를 초기값으로 물려준다.**
    #   임의 튜닝이 아니라 표준적인 다단계 적합이며, dQ/dV의 역할도 원래
    #   "이미 가까운 해를 피크로 다듬는 것"이다.
    #
    #   순서는 objectives.yaml의 정의 순서(항이 하나씩 쌓이는 순서)를 따른다.
    def _has_dqdv(w):
        """이 목적함수가 warm start를 받아야 하는가.

        기본 규칙은 "dQ/dV 항이 있으면"이다. 다만 목적함수 집합에 따라 그 규칙이
        **불공정한 비교**를 만든다 — 가중치 sweep에서 w_dqdv=0 하나만 seed 제공자가
        되어 자기는 초기값을 못 받고 나머지는 다 받았다 (실측: w=0만 86%, 나머지
        22~33%. dQ/dV 효과가 아니라 초기값 차이였다).
        그래서 목적함수 정의에 `_warm`을 넣어 명시적으로 지정할 수 있게 한다.
        """
        v = w.get("_warm")
        if v is not None:
            return bool(v)
        return float(w.get("w_dqdv", 0.0)) != 0.0

    warm = bool(task.get("warm_start", True))
    seed_p = None                      # 부드러운 항으로 얻은 해

    rows = []
    for name, weights in task["objectives"].items():
        J = make_objective(target, model_fn, weights, scales, obj_cfg, shortfall)
        init = task["init"]
        if warm and _has_dqdv(weights) and seed_p is not None:
            init = seed_p
        warmed = init is not task["init"]
        res = fit(J, init, task["lb"], task["ub"],
                  n_restarts=task["n_restarts"], seed=task["seed"],
                  warm_init=warmed)
        if warm and not _has_dqdv(weights) and np.all(np.isfinite(res.p)):
            seed_p = list(map(float, res.p))    # 가장 최근의 매끄러운 해
        inv = task["inventory"]
        # F26: p_ini는 목적함수별 dict. 옛 형식(공통 리스트)도 그대로 받는다.
        _pi = task.get("p_ini")
        p_ini_obj = _pi.get(name) if isinstance(_pi, dict) else _pi
        if task["reference"] == "halfcell":
            hc = to_modes_halfcell(res.p, p_ini_obj, task["r"])
            main_modes = hc
            extra = {"lli_hat_pe_basis": hc["lli_pe_basis"]}
        else:
            main_modes = to_degradation_modes(res.p, task["r"], "derived",
                                              inv["w_pe"], inv["w_ne"], inv["kappa"])
            extra = {}
        paper = to_degradation_modes(res.p, task["r"], "paper")
        code = to_degradation_modes(res.p, task["r"], "code")
        p_ini = p_ini_obj or [float("nan")] * 4
        rows.append({
            **extra, "reference": task["reference"],
            **task["truth"],
            "cond_id": task["cond_id"], "objective": name,
            "q_mah": task["q_mah"], "r": task["r"],
            **dict(zip(PARAM_NAMES, res.p)),
            # 리뷰 F12: halfcell 재계산에 필요한 p_ini를 행에도 저장
            **{f"{k}_ini": float(v) for k, v in zip(PARAM_NAMES, p_ini)},
            "J": res.J, "converged": res.converged, "n_eval": res.n_eval,
            **{f"bound_active_{k}": v for k, v in zip(PARAM_NAMES, res.bound_active)},
            "any_bound_active": res.any_bound_active,
            # 리뷰 F1: grid 기준의 α=1 소프트 벽(창 부족 벌점이 만드는 파일업)은
            # box bound가 아니라 bound_active에 안 잡힌다 → 별도 플래그
            "alpha_wall_pe": bool(abs(res.p[0] - 1.0) < 1e-3),
            "alpha_wall_ne": bool(abs(res.p[2] - 1.0) < 1e-3),
            "n_restarts": res.n_restarts, "n_restarts_agree": res.n_restarts_agree,
            "p_spread": res.p_spread, "J_spread": res.J_spread,
            # 리뷰 F4: restart별 (p, J) 원본 — 사후에 노이즈 환산 임계로 재집계 가능
            "restarts_json": json.dumps(res.restarts),
            "lam_pe_hat": main_modes["lam_pe"], "lam_ne_hat": main_modes["lam_ne"],
            "lli_hat": main_modes["lli"],
            "lli_hat_21p": paper["lli"], "lli_hat_code": code["lli"],
            "bounds_preset": task["bounds_preset"],
            # F20: 이 목적함수가 매끄러운 해를 초기값으로 받았는가 (사후 감사용)
            "warm_started": bool(warm and _has_dqdv(weights) and init is not task["init"]),
        })
    return rows


def run_fit(in_dir, out_dir, obj_cfg: dict, objectives: dict, bounds: dict,
            bounds_preset: str, n_restarts: int, nproc: int,
            use_noisy: bool = True, limit: int | None = None,
            base_config: str | None = None, reference: str = "grid",
            resume: bool = False, subset: set | None = None,
            warm_start: bool = True) -> dict:
    """grid 결과 전체에 fitting 수행 → fits.parquet.

    subset: 이 cond_id 집합만 fitting (Phase 6 가중치 sweep의 층화 표본용).
            limit이 "앞 N개"인 것과 달리 격자 전체에 고르게 걸칠 수 있다.

    ★ 실행 잠금을 **함수 맨 앞에서** 잡는다 (리뷰 F19, 2026-08-06 실측 사고).

    이전에는 curves.parquet 로드 → 태스크 구성 → (halfcell이면) p_ini
    self-fitting 을 모두 마친 뒤에야 lock을 잡았다. 그 앞 구간이 무방비라
    두 번째 프로세스가 검사를 그냥 통과한다.

    실제 사고: PID 330053(04:17:13 시작)과 333299(04:38:48 시작)가 같은
    --out=results/grid_fine_v1 에 동시에 붙어 32워커씩 총 64개가 16물리코어를
    나눠 썼고(속도 반토막), 게다가 330053은 curves 재생성(04:37:56) **이전**의
    옛 프레임(Q=5720) 곡선을 메모리에 들고 있어 fit_chunks 에 틀린 결과를
    쌓고 있었다. 청크 병합은 mtime 최신 우선이므로 정상 결과를 덮어쓴다.
    """
    from pathlib import Path

    from src.io import acquire_run_lock, release_run_lock

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    acquire_run_lock(out_dir, ".fit.lock")
    try:
        return _run_fit_locked(in_dir, out_dir, obj_cfg, objectives, bounds,
                               bounds_preset, n_restarts, nproc, use_noisy,
                               limit, base_config, reference, resume, subset,
                               warm_start)
    finally:
        release_run_lock(out_dir, ".fit.lock")


def _run_fit_locked(in_dir, out_dir, obj_cfg: dict, objectives: dict, bounds: dict,
                    bounds_preset: str, n_restarts: int, nproc: int,
                    use_noisy: bool = True, limit: int | None = None,
                    base_config: str | None = None, reference: str = "grid",
                    resume: bool = False, subset: set | None = None,
                    warm_start: bool = True) -> dict:
    """run_fit 본체. 호출자가 이미 .fit.lock 을 보유한 상태여야 한다."""
    import os
    import time
    from pathlib import Path

    import pandas as pd
    from joblib import Parallel, delayed
    from tqdm import tqdm

    import yaml

    from src.io import (base_manifest, file_digest, git_info, source_digest,
                        write_manifest)

    in_dir, out_dir = Path(in_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ★ F51 — 시작 provenance를 **어떤 입력 로드·캐시 로드·self-fit 보다도 먼저**
    #   기록한다. 예전에는 run_sig 계산 뒤에 썼는데, halfcell 실행에서는 그보다
    #   앞에 curves 로드·inventory 계산·half-cell 캐시 로드·pristine p_ini fitting
    #   (모든 후속 fit 의 기준점을 정하는 실제 최적화)이 이미 끝나 있었다.
    # ★ 그리고 resume 마다 **덮어쓰지 않는다.** 덮어쓰면 최초 chunk 를 만든 시점의
    #   provenance 가 사라지고 마지막 시도만 "시작"으로 남는다.
    _attempts = out_dir / "attempts"
    _attempts.mkdir(exist_ok=True)
    _gi0 = git_info(Path(__file__).resolve().parent.parent)
    _src0 = source_digest()
    # 같은 초에 두 번 시작해도 겹치지 않게 기존 시도 수를 붙인다
    _n_prev = len(list(_attempts.glob("manifest_start_*.yaml")))
    attempt_id = f"{time.strftime('%Y%m%dT%H%M%S')}_{os.getpid()}_{_n_prev:03d}"
    start_prov = {
        "attempt_id": attempt_id,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "resume": bool(resume),
        "source_digest": _src0,
        **_gi0,
        "input_sha256": {str(x): file_digest(x) for x in
                         [in_dir / "curves.parquet",
                          base_config or "configs/base.yaml"] if x is not None},
        "_주의": ("실행 **시작** 시점 상태다 (입력 로드·self-fit 이전). "
                 "manifest.yaml 은 종료 시점이므로 둘이 다르면 실행 도중 코드나 "
                 "입력이 바뀐 것이다 (F42/F51). half-cell 캐시 digest 는 기준 곡선을 "
                 "고른 뒤 attempt 파일에 추가된다."),
    }
    (_attempts / f"manifest_start_{attempt_id}.yaml").write_text(
        yaml.safe_dump(start_prov, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    _first = out_dir / "manifest_start.yaml"
    if not _first.exists():          # 최초 시도만 대표로 남긴다 (덮어쓰지 않음)
        _first.write_text(
            yaml.safe_dump(start_prov, allow_unicode=True, sort_keys=False),
            encoding="utf-8")
    log.info("실행 시작 provenance: git %s dirty=%s src %s → %s",
             _gi0.get("git_commit_short"), _gi0.get("git_dirty"), _src0,
             _attempts / f"manifest_start_{attempt_id}.yaml")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(in_dir / "curves.parquet")

    ref = extract_reference(df)
    ref_x = ref["x_norm"].to_numpy()
    ref_pe, ref_ne = ref["v_pe"].to_numpy(), ref["v_ne"].to_numpy()
    ref_full = ref["v_full"].to_numpy()
    q_ref = float(ref["q_mah"].iloc[0])
    log.info("reference: Q=%.1f mAh, %d점", q_ref, len(ref_x))

    # LLI 환산 상수 (전하 보존 유도식) — 메인에서 1회 계산해 워커에 값만 전달
    from src.config import load_config as _load
    from src.inventory import reference_inventory
    base_cfg = _load(base_config or "configs/base.yaml")
    inv = reference_inventory(base_cfg, q_ref / 1000.0).as_dict()

    # ── Case 1: full-range half-cell OCV 기준 ──
    hc_dict, p_ini = None, None
    if reference == "halfcell":
        from src.halfcell import get_halfcell_reference, halfcell_cache_path
        hc = get_halfcell_reference(base_cfg)
        hc_used = halfcell_cache_path(base_cfg)     # F45: 실제로 쓴 캐시 하나
        # F51: 기준 곡선을 고른 직후, pristine self-fit **전에** attempt 파일 보강
        start_prov["input_sha256"][str(hc_used)] = file_digest(hc_used)
        start_prov["halfcell_cache"] = str(hc_used)
        (_attempts / f"manifest_start_{attempt_id}.yaml").write_text(
            yaml.safe_dump(start_prov, allow_unicode=True, sort_keys=False),
            encoding="utf-8")
        cov = hc.coverage()
        # 리뷰 F11: to_modes_halfcell의 LLI 식은 테이블이 화학량론 전 범위일 때만
        # 성립한다 (sim 테이블 y_min=0.251이면 오프셋 ≈2.2Ah로 LLI가 조용히 틀림).
        if cov["pe_min"] > 0.01 or cov["pe_max"] < 0.99 \
                or cov["ne_min"] > 0.01 or cov["ne_max"] < 0.99:
            raise RuntimeError(
                f"half-cell 테이블이 전 범위가 아님 ({cov}). "
                f"method='ocp' 캐시를 사용하세요 (python -m src.halfcell --method ocp)")
        hc_dict = hc.as_dict()
        log.info("half-cell 기준 범위: %s", cov)

    v_col = "v_full_noisy" if (use_noisy and "v_full_noisy" in df.columns) else "v_full"
    tasks = []
    for cond_id, g in df.groupby("cond_id", sort=False):
        g = g.sort_values("x_norm")
        q = float(g["q_mah"].iloc[0])
        truth = {k: float(g[k].iloc[0]) for k in ("lli", "lam_pe", "lam_ne")}
        truth.update({k: g[k].iloc[0] for k in ("lam_pe_type", "lam_ne_type", "noise")
                      if k in g.columns})
        tasks.append({
            "cond_id": cond_id, "x": g["x_norm"].to_numpy(),
            "v_target": g[v_col].to_numpy(), "q_mah": q, "r": q / q_ref,
            "truth": truth, "ref_x": ref_x, "ref_pe": ref_pe, "ref_ne": ref_ne,
            "ref_full": ref_full, "obj_cfg": obj_cfg, "objectives": objectives,
            "init": bounds["init"], "lb": bounds["lb"], "ub": bounds["ub"],
            "bounds_preset": bounds_preset, "n_restarts": n_restarts,
            "inventory": inv, "reference": reference, "halfcell": hc_dict,
            "p_ini": p_ini, "warm_start": warm_start,
            # hash()는 프로세스마다 소금이 달라 재현 불가 → sha1 기반 결정적 seed
            "seed": int(hashlib.sha1(cond_id.encode()).hexdigest()[:8], 16),
        })
    if subset is not None:
        sub = set(subset)
        missing = sub - {t["cond_id"] for t in tasks}
        if missing:
            log.warning("subset의 %d조건이 curves에 없음 (예: %s)",
                        len(missing), sorted(missing)[:3])
        tasks = [t for t in tasks if t["cond_id"] in sub]
        if not tasks:
            raise RuntimeError("subset과 겹치는 조건이 없음")
        log.info("subset 적용: %d조건", len(tasks))
    if limit:
        tasks = tasks[:limit]

    if reference == "halfcell":
        # ★ ini 정규화용: 기준 셀 자신을 먼저 fitting해 α_ini·β_ini를 얻는다.
        # 리뷰 F2: max(r)로 고르면 reference의 noise 변형 3개가 r=1.0 동률이라
        # 행 순서에 따라 노이즈 곡선에 self-fitting할 수 있고, --limit로 잘리면
        # 열화 조건이 뽑힌다 → truth로 명시 선택하고 clean 곡선을 강제한다.
        def _is_ref(t):
            tr = t["truth"]
            return (tr["lli"] == 0 and tr["lam_pe"] == 0 and tr["lam_ne"] == 0
                    and float(tr.get("noise", 0.0)) == 0.0)

        ref_candidates = [t for t in tasks if _is_ref(t)]
        if not ref_candidates:
            raise RuntimeError(
                "p_ini 기준 조건(lli=lam_pe=lam_ne=0, noise=0)이 태스크에 없음 "
                "(--limit로 잘렸을 수 있음)")
        # ★ p_ini는 목적함수마다 따로 구한다 (F26).
        #   한때 pocv_dvdq 하나로 fit해 모든 목적함수에 주입했는데, 목적함수마다
        #   pristine optimum이 다르므로 나머지는 남의 원점에서 좌표를 읽는 셈이
        #   된다. LAM_PE에 거의 일정한 offset이 생기고, 그게 degeneracy로 오독됐다.
        #   실측(공통 1,476조건): 34p가 99.1% → 10.0%, 평균|err| 3.94 → 1.43%p.
        #
        # ★★ 목적함수 전체를 **한 task로** 넘긴다 (F26b). 하나씩 따로 fit하면
        #   warm start 연쇄가 끊겨, 원점과 데이터 점이 서로 다른 optimizer
        #   프로토콜에서 측정된다. 그러면 F26이 지우려던 계통 오프셋이 그대로
        #   다시 생긴다. 실측: dqdv_only의 pristine이 단독 fit에서
        #   [1.5708, -0.4442, 1.0204, -0.0184], 연쇄 fit에서
        #   [1.4849, -0.4102, 1.0507, -0.0507]로 갈렸다 (본 fitting은 후자).
        #   비용도 4번 → 1번으로 준다.
        ref_id = ref_candidates[0]["cond_id"]
        ini_rows = _fit_one({**ref_candidates[0], "p_ini": [1.0, 0.0, 1.0, 0.0]})
        p_ini = {r["objective"]: [float(r[k]) for k in PARAM_NAMES] for r in ini_rows}
        for name, v in p_ini.items():
            log.info("α_ini·β_ini[%s] = %s (기준 조건 %s 자체 fitting, warm=%s)",
                     name, [round(x, 4) for x in v], ref_id,
                     bool(next(r["warm_started"] for r in ini_rows
                               if r["objective"] == name)))
        missing_ini = set(objectives) - set(p_ini)
        if missing_ini:
            raise RuntimeError(f"p_ini를 못 구한 목적함수: {sorted(missing_ini)}")
        for t in tasks:
            t["p_ini"] = p_ini

    from src.io import chunk_files, load_completed, mark_completed, merge_chunks, save_chunk

    # ── resume: 완료 조건 건너뛰기 ──
    # 리뷰 F18: 완료 파일명에 실행 서명을 넣는다. 안 그러면 다른 --objective로
    # resume했을 때 새 목적함수가 조용히 누락된다.
    #
    # ★ F32 — 서명에 **결과를 바꾸는 모든 설정**이 들어가야 한다. 예전에는
    #   목적함수 *이름*·reference·bounds preset·타깃 열·warm_start만 넣어서,
    #   같은 이름으로 가중치나 restart 수만 바꾸고 --resume하면 옛 청크가
    #   재사용됐다. 그러면 서로 다른 설정의 행이 섞인 결과가 새 manifest 아래
    #   생성되어, manifest 하나만 봐서는 검출할 수 없다.
    # ★ F36 — 경로 문자열이 아니라 **내용**을 넣는다. 같은 `configs/base.yaml`을
    #   수정해 inventory constants나 half-cell reference가 바뀌어도 서명이 그대로면
    #   resume이 옛 청크를 완료분으로 인정한다. obj_cfg도 두 섹션만 뽑지 말고
    #   resolved 전체를 넣는다 — 어느 키가 결과를 바꾸는지 미리 알 수 없다.
    # F45: glob 이 아니라 **실제로 쓴** 캐시 하나만
    hc_paths = [hc_used] if reference == "halfcell" else []
    _gi = git_info(Path(__file__).resolve().parent.parent)
    run_spec = {
        # ★ F49 — 코드 identity 를 서명에 넣는다. 없으면 코드만 바꾸고 resume 했을 때
        #   서로 다른 코드의 행이 같은 서명으로 섞이고 병합 검사를 통과한다.
        "sig_version": 3,
        "git_commit": _gi.get("git_commit"),
        "git_dirty": _gi.get("git_dirty"),
        "source_digest": source_digest(),
        "objectives": {k: objectives[k] for k in sorted(objectives)},   # 이름 + 가중치
        "reference": reference, "bounds_preset": bounds_preset,
        "bounds": bounds, "v_col": v_col, "warm_start": bool(warm_start),
        "n_restarts": n_restarts,
        "obj_cfg": obj_cfg,                      # resolved 전체
        "base_config": str(base_config),
        "base_config_sha": file_digest(base_config or "configs/base.yaml"),
        "inventory": inv,                        # base config에서 유도된 상수
        "curves_sha": file_digest(in_dir / "curves.parquet"),
        "halfcell_sha": {p.name: file_digest(p) for p in hc_paths},
    }
    run_sig = hashlib.sha1(
        json.dumps(run_spec, sort_keys=True, default=str).encode()).hexdigest()[:12]
    completed_name = f"fit_completed_{run_sig}.jsonl"

    done = load_completed(out_dir, completed_name) if resume else set()
    if resume and done:
        # 리뷰 F19b: "완료 표시는 있는데 청크에 행이 없는" 조건은 완료로 믿지 않는다.
        # 동시 실행 사고로 오염된 청크를 지우면 표시만 남아, resume이 그 조건을
        # 영원히 건너뛴다 (결과가 조용히 비는 가장 위험한 실패 모드).
        have: set[str] = set()
        for f in chunk_files(out_dir, "fit_chunks"):
            try:
                have |= set(pd.read_parquet(f, columns=["cond_id"])["cond_id"])
            except Exception:  # noqa: BLE001
                continue
        ghost = done - have
        if ghost:
            log.warning("완료 표시만 있고 결과 행이 없는 조건 %d개 → 완료 취소 후 재계산",
                        len(ghost))
            done &= have
    todo = [t for t in tasks if t["cond_id"] not in done]
    if resume and done:
        log.info("fit resume(sig=%s): %d개 완료 확인, %d개 남음",
                 run_sig, len(done), len(todo))

    # ★ 입력/출력 디렉터리를 반드시 찍는다. run.sh가 --out을 조용히 --in으로
    #   덮어써서 스모크 결과가 본 실행 디렉터리를 오염시킨 일이 있었다.
    log.info("fitting: %d조건 × %d목적함수 × %d restart (nproc=%d, warm_start=%s)\n"
             "         입력 %s\n         출력 %s",
             len(todo), len(objectives), n_restarts, nproc, warm_start,
             in_dir.resolve(), out_dir.resolve())
    t0 = time.perf_counter()
    n_done = 0
    with Parallel(n_jobs=nproc, backend="loky") as parallel:
        step = max(1, min(100, len(todo)))
        chunk_idx = 0
        for s in range(0, len(todo), step):
            chunk = todo[s:s + step]
            rows = []
            for rr in parallel(delayed(_fit_one)(t) for t in chunk):
                rows.extend(rr)
            # ★ F32 — 행마다 실행 서명을 박는다. 병합 단계에서 서로 다른 설정의
            #   청크가 섞였는지 검출할 수 있어야 한다 (manifest 하나만 보면 못 잡는다).
            for r in rows:
                r["run_sig"] = run_sig
            # ★ 청크 즉시 저장 — 5시간 실행이 죽어도 여기까지는 남는다
            save_chunk(pd.DataFrame(rows), out_dir, chunk_idx,
                       subdir="fit_chunks")
            chunk_idx += 1
            for t in chunk:
                mark_completed(out_dir, t["cond_id"], completed_name)
            n_done += len(chunk)
            el = time.perf_counter() - t0
            # tqdm은 파일 리다이렉트 시 버퍼링으로 안 보인다 → 로그로 진행률
            log.info("fit 진행: %d/%d (%.0f%%) — %.1f s/cond, 남은 예상 %.0f분",
                     n_done, len(todo), 100 * n_done / len(todo),
                     el / n_done, el / n_done * (len(todo) - n_done) / 60)
    elapsed = time.perf_counter() - t0

    # 이전 실행분(resume)까지 합쳐 병합. 같은 (cond_id, objective, ...)는 최신만.
    path = merge_chunks(out_dir, "fits.parquet", subdir="fit_chunks",
                        keys=("cond_id", "objective", "reference", "bounds_preset"))
    if path is None:      # 리뷰 F19: 전부 resume-완료면 청크가 없어도 죽지 않게
        path = out_dir / "fits.parquet"
        if not path.exists():
            raise RuntimeError("청크도 기존 fits.parquet도 없음 — 실행된 조건이 없습니다")
    fits = pd.read_parquet(path)

    # ★ F32 — 서로 다른 설정의 청크가 섞였으면 여기서 죽는다. 조용히 섞인 결과를
    #   새 manifest 아래 내보내는 것이 가장 위험하다 (읽는 쪽이 검출할 수 없다).
    # ★ F36 — 경고가 아니라 **실패**시킨다. 서명이 하나뿐이어도 현재 실행과
    #   다르면 옛 결과가 새 manifest 아래 통과한다. null 행도 dropna에 숨는다.
    if "run_sig" not in fits.columns:
        raise RuntimeError(
            f"{path}에 run_sig 열이 없습니다 — F32 이전 형식입니다. "
            f"{out_dir}/fit_chunks 를 비우고 처음부터 다시 돌리세요.")
    n_null = int(fits["run_sig"].isna().sum())
    sigs = sorted(str(s) for s in fits["run_sig"].dropna().unique())
    if n_null or len(sigs) != 1 or sigs[0] != run_sig:
        raise RuntimeError(
            f"실행 서명이 이번 실행과 일치하지 않습니다 "
            f"(서명 {sigs or '없음'}, 미기록 행 {n_null}, 이번 실행 {run_sig}). "
            f"다른 설정의 결과가 섞였거나 옛 형식입니다. "
            f"{out_dir}/fit_chunks 를 비우고 처음부터 다시 돌리세요 (F36).")

    # F30: config_hash를 비워 두면 어떤 목적함수 정의로 돌았는지 남지 않는다.
    #   실제 obj_cfg 내용을 해시해 박고, 입력 curves와 config 파일의 SHA도 남긴다.
    cfg_h = hashlib.sha1(json.dumps(obj_cfg, sort_keys=True, default=str)
                         .encode()).hexdigest()[:12]
    # halfcell 기준 캐시도 입력이다 — 이게 바뀌면 결과가 바뀐다 (F45: 실제 경로)
    hc_cache = list(hc_paths)
    write_manifest(out_dir, base_manifest(
        cfg_h, out_dir=out_dir,
        inputs=[in_dir / "curves.parquet", base_config, *hc_cache], extra={
        "run_type": "fit", "input": str(in_dir),
        "run_signature": run_sig, "run_spec": run_spec,
        # F42/F51: 시작 시점과 대조 (다르면 실행 도중 바뀐 것)
        "start_provenance": start_prov,
        "attempt_id": attempt_id,
        "attempts_dir": "attempts",
        "git_commit_changed_during_run": bool(
            start_prov.get("git_commit")
            != git_info(Path(__file__).resolve().parent.parent).get("git_commit")),
        "source_digest_changed_during_run": bool(_src0 != source_digest()),
        "objectives_resolved": obj_cfg.get("objectives"),
        "n_conditions": len(tasks), "objectives": list(objectives),
        "bounds_preset": bounds_preset, "bounds": bounds,
        "n_restarts": n_restarts, "target_column": v_col, "reference": reference,
        "p_ini": p_ini, "warm_start": warm_start,
        "q_ref_mah": q_ref, "lli_inventory_constants": inv, "elapsed_s": round(elapsed, 1),
        "fits_parquet": str(path),
    }))
    log.info("fitting 완료: %d행, %.1fs → %s", len(fits), elapsed, path)
    return {"n_rows": len(fits), "n_conditions": len(tasks),
            "elapsed_s": elapsed, "out": str(path)}


def main() -> None:
    import argparse
    import json
    import multiprocessing

    from src.config import load_config

    ap = argparse.ArgumentParser(description="alpha/beta fitting (33p·34p)")
    ap.add_argument("--in", dest="in_dir", required=True, help="grid 결과 디렉터리")
    ap.add_argument("--out", default=None, help="기본: --in 과 동일")
    ap.add_argument("--objectives-config", default="configs/objectives.yaml")
    ap.add_argument("--base-config", default="configs/base.yaml",
                    help="LLI 환산 상수(재고 분배) 계산용 물리 baseline")
    ap.add_argument("--objective", default=None,
                    help="콤마 목록. 기본: objectives.yaml 전체")
    ap.add_argument("--bounds", default="expanded", help="expanded | original_33p")
    ap.add_argument("--n-restarts", dest="n_restarts", type=int, default=None)
    ap.add_argument("--nproc", type=int, default=multiprocessing.cpu_count())
    ap.add_argument("--resume", action="store_true",
                    help="fit_completed.jsonl 기반 재개 (청크 단위 저장)")
    ap.add_argument("--reference", default="grid", choices=["grid", "halfcell"],
                    help="grid=기준 셀 창(유도식 환산) | halfcell=전 범위 반쪽셀(21p 식)")
    ap.add_argument("--clean", action="store_true", help="노이즈 없는 곡선으로 fitting")
    ap.add_argument("--limit", type=int, default=None, help="앞 N조건만 (스모크용)")
    ap.add_argument("--no-warm-start", dest="warm_start", action="store_false",
                    help="dQ/dV 목적함수에 매끄러운 해를 초기값으로 물려주지 않는다 "
                         "(F20 비교 실험용). 기본은 물려준다")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.objectives_config)

    objectives = dict(cfg["objectives"])
    if args.objective:
        want = [s.strip() for s in args.objective.split(",")]
        missing = [w for w in want if w not in objectives]
        if missing:
            raise SystemExit(f"objectives.yaml에 없는 목적함수: {missing}")
        objectives = {k: objectives[k] for k in want}

    fcfg = cfg["fitting"]
    presets = fcfg["bounds_presets"]
    if args.bounds not in presets:
        raise SystemExit(f"알 수 없는 bounds preset: {args.bounds} (가능: {list(presets)})")
    bounds = presets[args.bounds]

    summary = run_fit(
        in_dir=args.in_dir, out_dir=args.out or args.in_dir,
        obj_cfg=cfg, objectives=objectives, bounds=bounds,
        bounds_preset=args.bounds,
        n_restarts=args.n_restarts or int(fcfg.get("n_restarts", 5)),
        nproc=args.nproc, use_noisy=not args.clean, limit=args.limit,
        base_config=args.base_config, reference=args.reference,
        resume=args.resume, warm_start=args.warm_start,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
