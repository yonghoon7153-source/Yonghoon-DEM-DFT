"""compare_objectives.py — 목적함수 4종 비교 (Phase 6). ★ 최종 산출물

같은 격자·같은 정답에 대해 pocv / pocv_dvdq / pocv_dvdq_dqdv / dqdv_only 를
적용했을 때 degeneracy가 얼마나 줄어드는지를 표 하나로 만든다.
"dQ/dV를 넣으면 X% → Y%로 준다"의 X와 Y가 여기서 나온다.

리뷰 규칙이 표의 형태를 결정한다
──────────────────────────────
F1  복원가능군(α_true≥1)에서만 센다. 복원불가군을 섞으면 모든 목적함수가
    똑같이 나빠 보여 정작 비교하려는 차이가 묻힌다. 제외 비율은 따로 명시.
F5  방법 바이어스를 뺀 보정 판정을 **같은 표에** 나란히 둔다. 둘 중
    유리한 쪽만 고르는 일이 없도록.
F10 노이즈 수준별로 쪼갠 표를 함께 낸다. dQ/dV의 이점은 노이즈에서
    희석되므로 노이즈 0 결과만 보면 과대평가된다.
F4  restart 기반 지표(불일치율)는 여기 넣지 않는다. 조건마다 restart 수가
    달라 목적함수 간 비교가 성립하지 않는다.
F14 저LLI·고LAM_PE 코너 공백을 각주로 붙인다.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# run.sh 없이 직접 실행해도 src/tools를 찾도록 (PYTHONPATH 미설정 대비)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

log = logging.getLogger(__name__)

# 34p 순서 — 항이 하나씩 쌓이는 순서로 보여야 개선 효과가 읽힌다
OBJ_ORDER = ["pocv", "pocv_dvdq", "pocv_dvdq_dqdv", "dqdv_only"]
OBJ_LABEL = {
    "pocv": "pOCV only",
    "pocv_dvdq": "pOCV + dV/dQ  (33p 기존)",
    "pocv_dvdq_dqdv": "pOCV + dV/dQ + dQ/dV  (34p 개선)",
    "dqdv_only": "dQ/dV only",
}
EXP_22P = {"lam_pe": 0.13, "lam_ne": 0.13, "lli": 0.17}


def _order(objs) -> list:
    known = [o for o in OBJ_ORDER if o in set(objs)]
    return known + sorted(set(objs) - set(known))


# ---------------------------------------------------------------- 표

def comparison_table(df: pd.DataFrame, by_noise: bool = False,
                     recoverable_only: bool = True) -> pd.DataFrame:
    """목적함수별 핵심 지표. F1에 따라 기본은 복원가능군만.

    ★ F29 — `recoverable_only=False`로 전체군도 반드시 같이 낸다. 실측에서
      결론의 **방향이 모집단에 따라 뒤집힌다**:
        복원가능군  33p 61.9% < 34p 63.3%   (33p가 낫다)
        전체 격자   33p 74.1% > 34p 71.9%   (34p가 낫다)
      복원불가군은 grid 기준에서 정답이 표현 불가능한 조건이므로 제외에 근거가
      있지만, 그 제외가 결론을 만든다면 제외 사실 자체를 결론과 같은 무게로
      적어야 한다.
    """
    rec = df[df["recoverable"]] if (recoverable_only and "recoverable" in df.columns) else df
    keys = ["objective"] + (["noise"] if by_noise and "noise" in rec.columns else [])
    rows = []
    for key, g in rec.groupby(keys):
        o = key[0] if isinstance(key, tuple) else key
        row = {"objective": o}
        if isinstance(key, tuple) and len(key) > 1:
            row["noise"] = key[1]
        row.update({
            "n": int(len(g)),
            "degenerate_frac": float(g["degenerate"].mean()),
            "degenerate_frac_corrected": float(g["degenerate_corrected"].mean())
            if "degenerate_corrected" in g.columns else np.nan,
            "mean_abs_err": float(g["abs_err_max"].mean()),
            "mean_abs_err_lam_pe": float(g["err_lam_pe"].abs().mean()),
            "mean_abs_err_lam_ne": float(g["err_lam_ne"].abs().mean()),
            "mean_abs_err_lli": float(g["err_lli"].abs().mean()),
            "pe_ne_antisym_frac": float(g["pe_ne_antisym"].mean()),
            "alpha_wall_frac": float(g["alpha_wall_any"].mean())
            if "alpha_wall_any" in g.columns else np.nan,
        })
        rows.append(row)
    out = pd.DataFrame(rows)
    out["_ord"] = out["objective"].map({o: i for i, o in enumerate(_order(out["objective"]))})
    sort_by = ["_ord"] + (["noise"] if "noise" in out.columns else [])
    return out.sort_values(sort_by).drop(columns="_ord").reset_index(drop=True)


def to_markdown(tbl: pd.DataFrame) -> str:
    """04_PROMPTS.md Phase 6이 요구한 형태의 마크다운 표."""
    has_noise = "noise" in tbl.columns
    head = ("| objective |" + (" noise |" if has_noise else "")
            # ★ 15차 발견 6 — 이 열은 일반 MAE 가 아니라 **행별 세 mode 중 최대
            #   절대오차의 평균**이다 (src/scoring.py). 라벨이 계산과 달라
            #   일반 MAE 로 오인·인용됐다.
            + " n | degeneracy | (바이어스 보정) | 평균 max-mode \\|err\\| | raw 반대부호 |")
    sep = "|---|" + ("---|" if has_noise else "") + "---|---|---|---|---|"
    lines = [head, sep]
    for _, r in tbl.iterrows():
        label = OBJ_LABEL.get(r["objective"], r["objective"])
        cells = [label]
        if has_noise:
            cells.append(f"{r['noise']:g}")
        corr = ("—" if pd.isna(r["degenerate_frac_corrected"])
                else f"{100 * r['degenerate_frac_corrected']:.0f}%")
        cells += [f"{r['n']:d}", f"{100 * r['degenerate_frac']:.0f}%", corr,
                  f"{100 * r['mean_abs_err']:.1f}%p",
                  f"{100 * r['pe_ne_antisym_frac']:.0f}%"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- 격차 경계 규약

#: ★ 17차 발견 1 — 참 격차는 설계 격자(0.02 step)에서 뺄셈으로 나오므로
#: nominal 2%p 가 `0.01999999999999999` 로 표현된다. raw float 에 `< 0.02` 를
#: 그대로 적용하면 **수학적으로 2%p 인 조건이 "2%p 미만" 군에 들어간다**.
#: v4 실측: recoverable·noise=0·pocv_dvdq 에서 raw 98 vs nominal 66 (32조건 편입),
#: 그 중 12조건이 분자에도 들어가 사건률 비가 90.00 → 89.09 로 움직였다.
#: 격자 step 0.02 에 비해 표현 오차는 1e-16 규모이므로 1e-9 로 흡수한다.
GAP_ATOL = 1e-9


def gap_lt(x, thresh: float):
    """`x < thresh` — **경계값은 '미만'이 아니다** (nominal thresh 는 제외)."""
    return np.asarray(x, dtype=float) < (thresh - GAP_ATOL)


def gap_ge(x, thresh: float):
    """`x >= thresh` — **경계값은 '이상'이다** (nominal thresh 는 포함)."""
    return np.asarray(x, dtype=float) >= (thresh - GAP_ATOL)


def gap_is_zero(x):
    """참 격차가 정확히 0 인가 (F34 exact-zero 군)."""
    return np.abs(np.asarray(x, dtype=float)) <= GAP_ATOL


# ---------------------------------------------------------------- 22p 판정

def _near_22p(df: pd.DataFrame, objective: str, noise: float, radius: float):
    """22p 근방 표본 선택 — `verdict_22p` 와 구성 helper 가 **같은 표본**을 봐야 한다.

    거리는 `EXP_22P` 중심에서 (lam_pe, lam_ne, lli) fractional coordinate 의
    **unscaled Euclidean distance** 다. radius 안에 점이 없으면 radius **밖**의
    최근접 1점으로 대체하는데(★ 18차 발견 9), 그때 renderer 가 "radius 안의
    조건" 이라고 쓰면 거짓이므로 대체 여부를 함께 돌려준다.
    """
    sub = df[df["objective"] == objective]
    if "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if sub.empty:
        return None, None, False
    d = np.sqrt(sum((sub[k] - v) ** 2 for k, v in EXP_22P.items()))
    near = sub[d <= radius]
    fallback = bool(near.empty)
    if fallback:                         # 격자에 정확히 없으면 최근접 1점
        near = sub.loc[[d.idxmin()]]
    return near, d, fallback


def p22_truth_composition(df: pd.DataFrame, objective: str = "pocv_dvdq",
                          noise: float = 0.0, radius: float = 0.021) -> dict:
    """22p 근방 표본의 **참값 구성** — 보고서 렌더 전용 파생값.

    ★ 16차 발견 4 (17차 사전). 보고서가 "절반은 PE=NE, wide-gap 은 하나도
    없다" 를 문자열 상수로 박아 두면 반경·step·noise 를 바꾸는 순간
    provenance 통과 배지를 단 채 거짓을 말한다. 구성은 데이터에서 나와야 한다.

    ★ 그런데 이 값을 `verdict_22p` 의 반환에 넣으면 안 된다 — 그러면 봉인된
    `objective_comparison.yaml` 의 key 집합과 재계산본이 달라져 F87 이 정당하게
    stale 을 올리고(실제로 v4 재생성에서 인용 금지 배너가 떴다), 8시간 재실행
    없이는 되돌릴 수 없다. 렌더 시점에 fits 정본에서 따로 뽑는다.
    """
    near, _, fallback = _near_22p(df, objective, noise, radius)
    if near is None:
        return {}
    # ★ 17차 발견 9 — exact-equal 정의를 gap 경계 규약과 공유하고, 표본 크기를
    #   함께 실어 renderer 가 verdict 와 **같은 표본**인지 대조할 수 있게 한다.
    return {"n_near_composition": int(len(near)),
            "p22_radius_fallback": fallback,
            "n_near_exact_equal": int(gap_is_zero(near["pe_ne_gap_true"]).sum()),
            "max_true_pe_ne_gap": float(near["pe_ne_gap_true"].max())}


def verdict_22p(df: pd.DataFrame, objective: str = "pocv_dvdq",
                noise: float = 0.0, radius: float = 0.021) -> dict:
    """22p 실험 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방의 복원 성적.

    ★ 이 프로젝트의 질문에 직접 답하는 함수다.
    격자 간격이 0.02이므로 반경 0.021이면 인접 격자점까지 포함한다.
    """
    near, d, fallback = _near_22p(df, objective, noise, radius)
    if near is None:
        return {"error": f"조건 없음 (objective={objective}, noise={noise})"}

    rec = bool(near["recoverable"].all()) if "recoverable" in near.columns else True
    out = {
        "objective": objective, "noise": noise,
        # ★ 17차 발견 9 — radius 는 결론을 정의하는 **selection protocol** 이다.
        #   기록하지 않으면 renderer 가 기본값을 다시 써서 다른 표본의 n_near 와
        #   구성 문장이 한 문단에 섞인다.
        "radius": float(radius),
        # ★ 18차 발견 9 — radius 밖 최근접 1점으로 대체됐는지 (protocol 사실)
        "radius_fallback": bool(fallback),
        "n_near": int(len(near)),
        "nearest_distance": float(d.min()),
        "recoverable": rec,
        "degenerate_frac": float(near["degenerate"].mean()),
        "mean_abs_err": float(near["abs_err_max"].mean()),
        "mean_err_lam_pe": float(near["err_lam_pe"].mean()),
        "mean_err_lam_ne": float(near["err_lam_ne"].mean()),
        "mean_err_lli": float(near["err_lli"].mean()),
        "pe_ne_antisym_frac": float(near["pe_ne_antisym"].mean()),
        "recovered_pe_ne_gap": float(near["pe_ne_gap_recovered"].mean()),
        "true_pe_ne_gap": float(near["pe_ne_gap_true"].mean()),
    }
    if "degenerate_corrected" in near.columns:
        out["degenerate_frac_corrected"] = float(near["degenerate_corrected"].mean())
    return out


# ---------------------------------------------------------------- 격차 붕괴

def gap_sensitivity(df: pd.DataFrame, objective: str, noise: float | None = 0.0,
                    gap_grid=(0.02, 0.04, 0.06, 0.08),
                    tol_grid=(0.01, 0.02, 0.03, 0.04, 0.05),
                    recoverable_only: bool = True) -> list[dict]:
    """★ F28 — 우도비·붕괴율의 임계 2차원 민감도.

    단일 (gap_thresh, tol) 조합의 값은 인용할 수 없다는 것이 리뷰의 결론이었다.
    사건률 비는 특정 임계 조합에서만 치솟는 성질이 있어, 이웃 칸에서 한 자릿수인
    값을 대표값으로 인용하면 사후선택이 된다. 그래서 표 전체를 같이 낸다 —
    한 칸만 떼어 쓰지 못하게 하는 것이 목적이다.

    ★ 18차 발견 11 — 여기 있던 경험 수치는 **경계 규약 수정(17차 발견 1) 이전**
    값이라 지웠다. 현행 값은 보고서와 `objective_comparison.yaml` 에서 읽을 것.
    docstring 에 실측을 고정하면 그 자체가 stale 인용원이 된다.
    """
    sub = df[df["objective"] == objective]
    if noise is not None and "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if recoverable_only and "recoverable" in sub.columns:
        sub = sub[sub["recoverable"]]
    if sub.empty:
        return []
    gt, gr = sub["pe_ne_gap_true"], sub["pe_ne_gap_recovered"]
    rows = []
    for g in gap_grid:
        for t in tol_grid:
            if g <= t:
                continue        # "뚜렷이 다름"이 "같음"보다 좁으면 정의가 무너진다
            wide = pd.Series(gap_ge(gt, g), index=gt.index)
            # ★ F34 — "참값이 같다"의 정의를 두 가지로 나눠 둘 다 낸다.
            #   `< tol`은 tol을 바꿀 때 분모 자체가 같이 움직여, 임계 민감도를
            #   보려는 표에서 두 효과가 섞인다. exact-zero는 tol과 무관하게 고정된
            #   격자점 집합이라 임계 효과만 분리해서 볼 수 있다.
            for same_def, same in (
                    ("lt_tol", pd.Series(gap_lt(gt, t), index=gt.index)),
                    ("exact_zero", pd.Series(gap_is_zero(gt), index=gt.index))):
                if not same.any() or not wide.any():
                    continue
                n_same_hat = int(gap_lt(gr[same], t).sum())
                n_wide_hat = int(gap_lt(gr[wide], t).sum())
                p_same = n_same_hat / int(same.sum())
                p_diff = n_wide_hat / int(wide.sum())
                rows.append({
                    "gap_thresh": float(g), "tol": float(t),
                    "same_def": same_def,
                    "n_same": int(same.sum()), "n_wide": int(wide.sum()),
                    # 분자도 싣는다 — 비율만 보면 표본 1~2개짜리 칸을 못 가린다
                    "n_same_called_same": n_same_hat,
                    "n_wide_called_same": n_wide_hat,
                    "p_same_given_same": p_same, "p_same_given_wide": p_diff,
                    "likelihood_ratio": float(p_same / p_diff) if p_diff > 0
                    else float("inf"),
                })
    return rows


def gap_analysis(df: pd.DataFrame, objective: str, noise: float | None = 0.0,
                 gap_thresh: float = 0.06, tol: float = 0.02,
                 recoverable_only: bool = True) -> dict:
    """★ 22p 질문에 가장 직접적으로 답하는 지표.

    22p 근방 격자점은 참 격차가 작아서(v4 실측: PE=NE 4/8, |ΔLAM|>0 4/8, 최대
    2%p), 거기서 복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은
    **반대 방향**이다.

      격차 붕괴(gap collapse)
        참값이 뚜렷이 다른데(|ΔLAM|_true ≥ gap_thresh)
        복원값은 같다고(|ΔLAM|_hat < tol) 말하는 비율.
        이 비율이 높으면 → 실측에서 LAM_PE ≈ LAM_NE가 나와도 **정보가 없다**.
        22p 결과를 물리로 읽을 근거가 사라진다.

      거짓 분리(false split)
        참값은 같은데(|ΔLAM|_true < tol) 복원값은 다르다고 말하는 비율.
        반대 방향 실패로, 격차 지표 자체의 신뢰도를 깎는다.

      shrinkage = mean(|ΔLAM|_hat / |ΔLAM|_true)
        1이면 격차를 그대로 복원, 0에 가까우면 전부 뭉갠다.

    gap_thresh 기본 0.06 = fine 격자 3칸. 참값 격차가 판정 기준(2%p)의
    3배는 돼야 "뚜렷이 다르다"고 말할 수 있다.
    """
    sub = df[df["objective"] == objective]
    if noise is not None and "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if recoverable_only and "recoverable" in sub.columns:
        sub = sub[sub["recoverable"]]
    if sub.empty:
        return {"error": f"조건 없음 (objective={objective}, noise={noise})"}

    gt, gr = sub["pe_ne_gap_true"], sub["pe_ne_gap_recovered"]
    wide, same = sub[gap_ge(gt, gap_thresh)], sub[gap_lt(gt, tol)]

    out = {
        "objective": objective, "noise": noise,
        "gap_thresh": gap_thresh, "tol": tol,
        "population": "recoverable" if recoverable_only else "all",
        "n_wide_gap_true": int(len(wide)),
        # ★ F28: 이 군은 "참 격차가 정확히 0"이 아니라 "< tol"이다. 옛 이름
        #   n_zero_gap_true는 조건을 잘못 말해서 바꿨다.
        "n_small_gap_true": int(len(same)),
        "n_exact_zero_gap_true": int(gap_is_zero(gt).sum()),
    }
    if len(wide):
        w_gr = wide["pe_ne_gap_recovered"]
        gap_err = (w_gr - wide["pe_ne_gap_true"]).abs()
        # ★ 18차 발견 1 — `collapse_measurable` 을 **삭제**했다.
        #
        #   옛 지표는 `|recovered − true|` 의 p99 를 모든 행에 공통인
        #   `gap_thresh − tol` 과 비교했다. 붕괴에는 (a) `true − recovered > 0`
        #   **방향**과 (b) 행마다 다른 필요 감소량 `true − tol` 이 필요한데 둘 다
        #   버린다. 반례: true 0.10 → recovered 0.20 은 붕괴와 정반대 방향인데
        #   절대오차 0.10 으로 "관측 가능" 판정을 받았다. 게다가 같은 결과에서
        #   뽑은 오차분포로 그 결과의 낮은 사건률을 방어하므로 순환 논리였다.
        #
        #   대체: **부호 있는 행별 여유**만 기술통계로 낸다. 판정하지 않는다.
        #     margin = tol − recovered_gap   (양수면 이미 붕괴, 음수면 그만큼 부족)
        required = float(gap_thresh - tol)
        margin = tol - w_gr
        out.update({
            # ★ 참값이 다른데 같다고 말하는 비율
            "gap_collapse_frac": float(gap_lt(w_gr, tol).mean()),
            "mean_true_gap_wide": float(wide["pe_ne_gap_true"].mean()),
            "min_true_gap_wide": float(wide["pe_ne_gap_true"].min()),
            "mean_recovered_gap_wide": float(w_gr.mean()),
            "shrinkage": float((w_gr / wide["pe_ne_gap_true"]).mean()),
            "collapse_requires_gap_err": required,
            "gap_err_median": float(gap_err.median()),
            "gap_err_p99": float(gap_err.quantile(0.99)),
            # 부호 있는 행별 여유 — 기술통계 전용 (판정 아님)
            "collapse_margin_median": float(margin.median()),
            "collapse_margin_max": float(margin.max()),
            # 복원 격차가 참 격차보다 **줄어든** 행 수 (붕괴 방향)
            "n_wide_gap_toward_collapse":
                int((wide["pe_ne_gap_true"] - w_gr > 0).sum()),
        })
    if len(same):
        out["false_split_frac"] = float(
            gap_ge(same["pe_ne_gap_recovered"], tol).mean())

    # ★ 22p 질문의 답을 우도비로 (리뷰 지적).
    #   관측 "두 전극이 같다"가 어느 가설을 더 지지하는가.
    #     P(같다고 답 | 참값 같음)      = 1 − false_split
    #     P(같다고 답 | 참값 크게 다름) = gap_collapse
    if "false_split_frac" in out and out.get("gap_collapse_frac") is not None:
        p_same = 1.0 - out["false_split_frac"]
        p_diff = out["gap_collapse_frac"]
        out["likelihood_ratio_equal"] = (
            float(p_same / p_diff) if p_diff > 0 else float("inf"))

        # ★ F28 — 이 값 하나만으로는 아무것도 주장할 수 없다. 임계를 흔들어
        #   얼마나 움직이는지를 **같은 dict 안에** 넣어, 떼어 인용하지 못하게 한다.
        sens = [r for r in gap_sensitivity(df, objective, noise,
                                           recoverable_only=recoverable_only)
                if r["same_def"] == "lt_tol"]     # gap_analysis와 같은 정의
        finite = [r["likelihood_ratio"] for r in sens
                  if np.isfinite(r["likelihood_ratio"])]
        n_inf = sum(1 for r in sens if not np.isfinite(r["likelihood_ratio"]))
        if finite:
            out["lr_sensitivity_min"] = float(min(finite))
            out["lr_sensitivity_max"] = float(max(finite))
            out["lr_sensitivity_median"] = float(np.median(finite))
            # ★ F34 — ∞를 조용히 빼면 변동폭이 좁아 보인다. 개수를 같이 낸다.
            out["lr_sensitivity_n_infinite"] = int(n_inf)
            # ★ 18차 발견 8 — 위 범위는 `lt_tol` 패널에서만 나온 값이다.
            #   보고서는 exact-zero 패널도 함께 싣고 그쪽 최대값이 다르다.
            #   한 범위를 전체 민감도 범위처럼 쓰지 못하게 따로 기록한다.
            _ez = [r["likelihood_ratio"]
                   for r in gap_sensitivity(df, objective, noise,
                                            recoverable_only=recoverable_only)
                   if r["same_def"] == "exact_zero"
                   and np.isfinite(r["likelihood_ratio"])]
            if _ez:
                out["lr_sensitivity_max_exact_zero"] = float(max(_ez))
            # ★ F34 — "local"은 **이웃 임계 한 칸**과 비교해야 한다. 전체 중앙값과
            #   비교하면 global outlier 판정이지 local spike 판정이 아니다.
            look = {(round(r["gap_thresh"], 6), round(r["tol"], 6)): r for r in sens}
            gs = sorted({round(r["gap_thresh"], 6) for r in sens})
            ts = sorted({round(r["tol"], 6) for r in sens})
            gi, ti = (gs.index(round(gap_thresh, 6)) if round(gap_thresh, 6) in gs else None,
                      ts.index(round(tol, 6)) if round(tol, 6) in ts else None)
            neigh = []
            if gi is not None and ti is not None:
                for dg in (-1, 0, 1):
                    for dt in (-1, 0, 1):
                        if dg == 0 and dt == 0:
                            continue
                        a, b = gi + dg, ti + dt
                        if 0 <= a < len(gs) and 0 <= b < len(ts):
                            r = look.get((gs[a], ts[b]))
                            if r and np.isfinite(r["likelihood_ratio"]):
                                neigh.append(r["likelihood_ratio"])
            if neigh:
                out["lr_neighbour_median"] = float(np.median(neigh))
                out["lr_neighbour_n"] = len(neigh)
                out["lr_is_local_spike"] = bool(
                    out["likelihood_ratio_equal"] > 3.0 * np.median(neigh))
        out["_주의"] = (
            "★ 이 우도비를 단독으로 인용하지 말 것. (1) posterior가 아니라 사건 "
            "우도비다 — '참값이 같을 확률'로 바꾸려면 사전확률과 2~6%p 중간 구간의 "
            "주변분포가 필요하다. (2) gap_thresh·tol 선택에 크게 의존한다 "
            f"(임계 격자 위 범위 {out.get('lr_sensitivity_min', float('nan')):.1f}"
            f"~{out.get('lr_sensitivity_max', float('nan')):.1f}, "
            f"중앙값 {out.get('lr_sensitivity_median', float('nan')):.1f}). "
            f"(3) 복원가능군(population={out['population']})으로 조건화한 값이라, "
            "실제 셀이 그 부분집단에 속한다는 독립 근거가 없으면 적용할 수 없다. "
            "gap_sensitivity 표 전체와 함께 볼 것.")
    return out


def plot_gap(df: pd.DataFrame, out_path, objective: str, noise: float = 0.0,
             tol: float = 0.02):
    """참 격차 vs 복원 격차 산점도. 대각선에서 아래로 눌리면 격차 붕괴."""
    sub = df[df["objective"] == objective]
    if "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    rec = sub[sub["recoverable"]] if "recoverable" in sub.columns else sub
    unrec = sub[~sub["recoverable"]] if "recoverable" in sub.columns else sub.iloc[:0]

    fig, ax = plt.subplots(figsize=(4.4, 4.2), constrained_layout=True)
    if len(unrec):
        ax.scatter(unrec["pe_ne_gap_true"], unrec["pe_ne_gap_recovered"],
                   s=10, c="0.8", marker="x", label="unrecoverable")
    ax.scatter(rec["pe_ne_gap_true"], rec["pe_ne_gap_recovered"],
               s=12, c="tab:blue", alpha=0.55, label="recoverable")
    lim = float(max(sub["pe_ne_gap_true"].max(), sub["pe_ne_gap_recovered"].max())) * 1.05
    ax.plot([0, lim], [0, lim], "k--", lw=1, label="perfect recovery")
    ax.axhspan(0, tol, color="tab:red", alpha=0.12)
    ax.text(lim * 0.98, tol * 0.5, "reported as equal", ha="right", va="center",
            fontsize=8, color="tab:red")
    ax.set_xlabel(r"true  $|LAM_{PE}-LAM_{NE}|$")
    ax.set_ylabel(r"recovered  $|LAM_{PE}-LAM_{NE}|$")
    ax.set_title(f"Electrode gap recovery — {objective}, noise={noise:g}", fontsize=10)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- 그림

def plot_panel(df: pd.DataFrame, out_path, noise: float = 0.0,
               value: str = "abs_err_max", tol: float = 0.02):
    """같은 지도를 목적함수 4종에 대해 나란히. 색 스케일 공유가 핵심."""
    from tools.plot_map import EXP_22P as MARK

    sub = df[df["noise"] == noise] if "noise" in df.columns else df
    objs = _order(sub["objective"].unique())
    lli_vals = sorted(sub["lli"].unique())
    # LLI는 22p에 가장 가까운 한 면만 (4×11 패널은 못 읽는다)
    lli = min(lli_vals, key=lambda v: abs(v - MARK["lli"]))
    g0 = sub[sub["lli"] == lli]
    pe_vals, ne_vals = sorted(g0["lam_pe"].unique()), sorted(g0["lam_ne"].unique())
    vmax = float(np.nanpercentile(sub[value], 98))

    fig, axes = plt.subplots(1, len(objs), figsize=(3.0 * len(objs) + 1.6, 3.5),
                             sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    im = None
    for ax, o in zip(axes, objs):
        g = g0[g0["objective"] == o]
        grid = np.full((len(ne_vals), len(pe_vals)), np.nan)
        unrec = np.zeros_like(grid, dtype=bool)
        for _, r in g.iterrows():
            i, j = ne_vals.index(r["lam_ne"]), pe_vals.index(r["lam_pe"])
            grid[i, j] = r[value]
            if "recoverable" in r and not r["recoverable"]:
                unrec[i, j] = True
        cmap = plt.get_cmap("RdYlGn_r").with_extremes(bad="0.85")
        im = ax.pcolormesh(pe_vals, ne_vals, np.ma.masked_invalid(grid),
                           cmap=cmap, vmin=0, vmax=vmax, shading="nearest")
        if unrec.any():
            ax.contourf(pe_vals, ne_vals, unrec.astype(float), levels=[0.5, 1.5],
                        colors="none", hatches=["///"], alpha=0)
        frac = g["degenerate"].mean() if len(g) else np.nan
        ax.set_title(f"{o}\ndegenerate {100 * frac:.0f}%", fontsize=9)
        ax.set_xlabel(r"LAM$_{PE}$")
        ax.plot(MARK["lam_pe"], MARK["lam_ne"], "*", ms=16, mfc="cyan",
                mec="k", mew=1.1, zorder=5)
    axes[0].set_ylabel(r"LAM$_{NE}$")
    cb = fig.colorbar(im, ax=axes, shrink=0.85)
    cb.set_label(value)
    fig.suptitle(f"Objective comparison — LLI = {lli:g}, noise = {noise:g}"
                 "    [star = 22p experiment · hatched = unrecoverable]",
                 y=1.06, fontsize=10)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_weight_curve(summary: pd.DataFrame, out_path,
                      metric: str = "degenerate_frac_corrected"):
    """w_dqdv sweep 곡선 — "튜닝 아니냐"에 대한 시각적 근거."""
    col = metric if metric in summary.columns else "degenerate_frac"
    fig, ax = plt.subplots(figsize=(5.2, 3.4), constrained_layout=True)
    for n, g in summary.groupby("noise"):
        g = g.sort_values("w_dqdv")
        ax.plot(g["w_dqdv"], 100 * g[col], "o-", ms=4, label=f"noise = {n:g} V")
    ax.axvline(1.0, color="0.6", ls=":", lw=1)
    ax.text(1.02, ax.get_ylim()[1], " default w=1", va="top", fontsize=8, color="0.4")
    ax.set_xlabel(r"$w_{dQ/dV}$")
    ax.set_ylabel(f"{col}  [%]")
    ax.set_title("dQ/dV weight sweep", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- 실행

# ------------------------------------------------- 파생 분석 provenance (18차 발견 6)

#: 파생 분석 산출물 스키마 버전. 파생 정의·규약이 바뀌면 올린다.
#: ★ raw 계산 provenance(`manifest.yaml`)와 **분리**한다 — 거기에 덧붙이면
#: 후대 분석 코드를 원래 계산에 거짓 귀속하게 된다 (18차 발견 6).
ANALYSIS_SCHEMA_VERSION = 1

#: 22p 표본 선택 protocol — 결론을 정의하므로 spec 에 박는다 (18차 발견 9)
P22_METRIC = "unscaled_euclidean_fractional_coordinates"
P22_EMPTY_RADIUS_POLICY = "nearest_fallback"


def analysis_parameters(df: pd.DataFrame, tol: float = 0.02,
                        gap_thresh: float = 0.06, noise: float = 0.0,
                        p22_radius: float = 0.021) -> dict:
    """이 파생 산출물을 정의하는 **모든** 자유 파라미터."""
    from src.io import _sha256_lines
    conds = sorted(set(df["cond_id"].astype(str))) if "cond_id" in df.columns else []
    return {
        "tol": float(tol),
        "gap_thresh": float(gap_thresh),
        "gap_atol": float(GAP_ATOL),
        "population": "recoverable(alpha_true >= 1 - atol) / all 두 벌 모두 기록",
        "noise": float(noise),
        "noise_unit": "sigma[V] of independent Gaussian voltage noise",
        "p22_center": [float(EXP_22P["lam_pe"]), float(EXP_22P["lam_ne"]),
                       float(EXP_22P["lli"])],
        "p22_radius": float(p22_radius),
        "p22_metric": P22_METRIC,
        "p22_empty_radius_policy": P22_EMPTY_RADIUS_POLICY,
        "selected_condition_ids_sha256": _sha256_lines(conds),
    }


def analysis_spec_id(params: dict) -> str:
    """파라미터 집합의 canonical digest — 같은 spec 인지 한 값으로 대조한다."""
    import hashlib
    import json
    return hashlib.sha256(
        json.dumps(params, sort_keys=True, default=str).encode()).hexdigest()


def _generator_identity() -> dict:
    """★ 18차 발견 6 — **파생 분석을 만든 코드** 좌표 (raw 계산 좌표와 분리)."""
    from src.io import env_fingerprint, git_info, source_digest
    gi = git_info()
    return {
        "git_commit": gi.get("git_commit", ""),
        "source_digest": source_digest(),
        "git_dirty": bool(gi.get("git_dirty")),
        "env": env_fingerprint(),
    }


def write_analysis_manifest(out_dir, in_dir, params: dict,
                            derived: "list[str]") -> dict:
    """`analysis_manifest.yaml` — raw 입력 · 생성 코드 · 파라미터 · 출력 digest."""
    import yaml

    from src.io import env_fingerprint, file_digest, git_info, source_digest
    out_dir, in_dir = Path(out_dir), Path(in_dir)

    def _fd(p):
        p = Path(p)
        return file_digest(p, full=True) if p.is_file() else None

    man = {
        "analysis_schema_version": ANALYSIS_SCHEMA_VERSION,
        "analysis_spec_id": analysis_spec_id(params),
        "raw_inputs": {
            "fits_sha256": _fd(in_dir / "fits.parquet"),
            "curves_sha256": _fd(in_dir / "curves.parquet"),
            "run_manifest_sha256": _fd(in_dir / "manifest.yaml"),
        },
        "generator": _generator_identity(),
        "parameters": params,
        "derived_outputs": {n: _fd(out_dir / n) for n in derived},
    }
    (out_dir / "analysis_manifest.yaml").write_text(
        yaml.safe_dump(man, allow_unicode=True, sort_keys=False,
                       default_flow_style=False), encoding="utf-8")
    return man


def verify_derived_freshness(run_dir, tol: float = 0.02) -> dict:
    """★ 18차 발견 6 — 보관 전 **의미 동치** 게이트.

    `payload_sha256.yaml` 은 stale bytes 도 충실히 해시한다. 바이트 보존은 파생
    파일이 봉인 fits 에서 재계산한 최신 의미를 담는지 증명하지 못한다. 여기서
    직접 재계산해 숫자를 대조한다.
    """
    import math

    import yaml
    run_dir = Path(run_dir)
    saved_p = run_dir / "objective_comparison.yaml"
    fits_p = run_dir / "fits.parquet"
    if not saved_p.is_file():
        return {"ok": False, "fail": ["objective_comparison.yaml 없음"]}
    if not fits_p.is_file():
        return {"ok": False, "fail": ["fits.parquet 없음 — 재계산 불가"]}

    from tools.compare_cases import _scored
    saved = yaml.safe_load(saved_p.read_text(encoding="utf-8")) or {}
    now = run_compare(run_dir, write=False, df=_scored(fits_p, tol), tol=tol)

    fail = []

    def walk(a, b, path=""):
        if isinstance(a, dict):
            for k, v in a.items():
                if isinstance(k, str) and k.startswith("_"):
                    continue           # 주석·self-description 은 대조 대상 아님
                if not isinstance(b, dict) or k not in b:
                    fail.append(f"{path}.{k}: 재계산본에 없다")
                    continue
                walk(v, b[k], f"{path}.{k}")
        elif isinstance(a, (list, tuple)):
            if not isinstance(b, (list, tuple)) or len(a) != len(b):
                fail.append(f"{path}: 길이 불일치")
                return
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f"{path}[{i}]")
        elif isinstance(a, bool):
            if bool(b) != a:
                fail.append(f"{path}: {a} ≠ {b}")
        elif isinstance(a, (int, float)):
            if not isinstance(b, (int, float)) or isinstance(b, bool) \
                    or not math.isclose(float(a), float(b),
                                        rel_tol=1e-9, abs_tol=1e-12):
                fail.append(f"{path}: {a} ≠ {b}")

    walk(saved, now)
    # self-description 이 실제 fits 를 가리키는가
    anchor = (saved.get("_analysis") or {}).get("fits_sha256")
    if anchor:
        from src.io import file_digest
        if anchor != file_digest(fits_p, full=True):
            fail.append("_analysis.fits_sha256: 이 fits 가 아니다")
    return {"ok": not fail, "fail": fail[:20]}


def run_compare(in_dir, out_dir=None, tol: float = 0.02,
                write: bool = True, df: "pd.DataFrame | None" = None) -> dict:
    """★ F69 — `write=False` / `df=` 는 **재검증용**이다.

    보고서 생성 시점에 저장된 `objective_comparison.yaml` 의 숫자를 다시 계산해
    대조하려면, 파일을 덮어쓰지 않고 같은 계산을 돌릴 수 있어야 한다. 그리고
    `df` 를 직접 주면 `degeneracy_map.parquet` 이 아니라 **정본 fits 에서 다시
    채점한 결과**로 대조할 수 있다 — map 자체가 변조된 경우까지 잡는다.
    """
    import yaml

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    if df is None:
        map_path = in_dir / "degeneracy_map.parquet"
        if not map_path.exists():
            raise SystemExit(f"{map_path} 없음 — 먼저 ./run.sh --mode score --in {in_dir}")
        df = pd.read_parquet(map_path)

    tbl = comparison_table(df)
    tbl_noise = comparison_table(df, by_noise=True)
    if write:
        tbl.to_csv(out_dir / "objective_comparison.csv", index=False)
        tbl_noise.to_csv(out_dir / "objective_comparison_by_noise.csv", index=False)

    objs = _order(df["objective"].unique())
    verdicts = {o: verdict_22p(df, o) for o in objs}
    gaps = {o: gap_analysis(df, o, tol=tol) for o in objs}
    # ★ F28/F29 — 복원가능군 조건화가 결론을 만들지 않았는지 보이려면 전체군을
    #   같이 내야 한다. 실측에서 결론 2의 방향이 모집단에 따라 뒤집혔다
    #   (복원가능군 33p 61.9 < 34p 63.3, 전체 격자 33p 74.1 > 34p 71.9).
    gaps_all = {o: gap_analysis(df, o, tol=tol, recoverable_only=False) for o in objs}
    sens = {o: gap_sensitivity(df, o) for o in objs}
    tbl_all = comparison_table(df, recoverable_only=False)
    if write:
        tbl_all.to_csv(out_dir / "objective_comparison_all_conditions.csv", index=False)

    figs = {}
    for o in objs:
        try:
            figs[f"gap_{o}"] = str(plot_gap(
                df, out_dir / "figures" / f"gap_recovery_{o}.png", o, tol=tol))
        except Exception as e:  # noqa: BLE001
            log.warning("격차 그림 실패 (%s): %s", o, e)
    for noise in (sorted(df["noise"].unique()) if "noise" in df.columns else [None]):
        try:
            figs[f"noise_{noise:g}"] = str(plot_panel(
                df, out_dir / "figures" / f"objective_panel_noise{noise:g}.png",
                noise, tol=tol))
        except Exception as e:  # noqa: BLE001
            log.warning("패널 그림 실패 (noise=%s): %s", noise, e)

    ws = in_dir / "wsweep" / "weight_sweep_summary.csv"
    if ws.exists():
        try:
            figs["weight_curve"] = str(plot_weight_curve(
                pd.read_csv(ws), out_dir / "figures" / "weight_sweep.png"))
        except Exception as e:  # noqa: BLE001
            log.warning("가중치 곡선 실패: %s", e)

    result = {"table": tbl.to_dict("records"),
              "table_all_conditions": tbl_all.to_dict("records"),
              "table_by_noise": tbl_noise.to_dict("records"),
              "verdict_22p": verdicts, "gap_analysis": gaps,
              "gap_analysis_all_conditions": gaps_all,
              "gap_sensitivity": sens, "figures": figs,
              "unrecoverable_frac": float(1 - df["recoverable"].mean())
              if "recoverable" in df.columns else 0.0}
    # ★ F29 — 모집단 선택이 결론의 방향을 바꾸는지 스스로 판정해 기록한다.
    try:
        a = tbl.set_index("objective")["degenerate_frac"]
        b = tbl_all.set_index("objective")["degenerate_frac"]
        d_rec = float(a["pocv_dvdq_dqdv"] - a["pocv_dvdq"])
        d_all = float(b["pocv_dvdq_dqdv"] - b["pocv_dvdq"])
        result["population_sensitivity"] = {
            "dqdv_minus_base_recoverable": d_rec,
            "dqdv_minus_base_all": d_all,
            "direction_flips": bool(d_rec * d_all < 0),
            "_주의": ("복원가능군과 전체 격자에서 33p·34p의 우열이 뒤집힌다. "
                     "결론 2를 인용할 때 어느 모집단인지 반드시 함께 쓸 것."
                     if d_rec * d_all < 0 else
                     "두 모집단에서 방향이 같다."),
        }
    except KeyError:
        pass
    if write:
        # ★ 18차 발견 6 — 이 파일을 **직접 읽는** 소비자가 오류의 시작점이었다.
        #   어느 fits 에서 어느 규약으로 나왔는지 파일 자체가 말해야 한다.
        #   key 가 `_` 로 시작하므로 F87 key 집합 대조에서는 제외된다.
        from src.io import file_digest as _fd0
        _params = analysis_parameters(df, tol=tol)
        _fits_p = in_dir / "fits.parquet"
        result["_analysis"] = {
            "schema_version": ANALYSIS_SCHEMA_VERSION,
            "analysis_spec_id": analysis_spec_id(_params),
            "fits_sha256": (_fd0(_fits_p, full=True)
                            if _fits_p.is_file() else None),
            "_주의": ("이 파일의 숫자는 위 fits 에서 이 spec 으로 계산됐다. "
                     "spec 이나 fits 가 다르면 인용하지 말 것."),
        }
        (out_dir / "objective_comparison.yaml").write_text(
            yaml.safe_dump(result, allow_unicode=True, sort_keys=False,
                           default_flow_style=False),
            encoding="utf-8")
        write_analysis_manifest(out_dir, in_dir, _params,
                                ["objective_comparison.yaml",
                                 "degeneracy_summary.yaml"])
        print(to_markdown(tbl))
    return result


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="목적함수 4종 비교 (Phase 6)")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run_compare(args.in_dir, args.out, args.tol)


if __name__ == "__main__":
    main()
