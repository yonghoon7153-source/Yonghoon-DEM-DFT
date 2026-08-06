"""diagnose_objective.py — 목적함수가 나쁜가, 최적화가 실패한 건가.

fine 격자 결과에서 dQ/dV를 넣은 목적함수가 오히려 나빠졌다(62% → 87%).
결론을 내기 전에 원인을 갈라야 한다. 가능성은 셋이고, 서로 처방이 다르다.

  (A) 최적화 실패    목적함수의 최소는 정답 근처인데 최적화가 못 찾음
                     → restart·초기값 문제. 목적함수는 무죄
  (B) 목적함수 오류  목적함수의 최소가 정답이 아닌 곳에 있음
                     → dQ/dV 항 자체가 잘못된 곳을 가리킴
  (C) 해상도 부족    곡선 점수가 모자라 dQ/dV가 이산화 잡음
                     → (B)로 보이지만 처방은 곡선 재생성

가르는 방법 — **교차 평가**:
  pocv_dvdq가 찾은 해 p_A를 dQ/dV 목적함수로 평가한 J_dqdv(p_A)와,
  dQ/dV 목적함수가 찾은 해 p_B의 J_dqdv(p_B)를 비교한다.

    J_dqdv(p_B) < J_dqdv(p_A)  이고  p_A가 정답에 더 가깝다
        → **목적함수가 틀린 곳을 더 좋아한다** = (B) 또는 (C). 최적화는 무죄
    J_dqdv(p_B) > J_dqdv(p_A)
        → 최적화가 더 나쁜 점에 멈춘 것 = (A)

(C)는 해상도 보고로 따로 판별한다. dQ/dV 격자점 수와 피크 폭(점 단위)이
핵심이다. 피크가 몇 점 안 되면 그 피크는 물리가 아니라 격자다.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# run.sh 없이 직접 실행해도 src를 찾도록 (PYTHONPATH 미설정 대비)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

log = logging.getLogger(__name__)

PARAM_NAMES = ("a_pe", "b_pe", "a_ne", "b_ne")


def resolution_report(curves: pd.DataFrame, obj_cfg: dict) -> dict:
    """곡선·dQ/dV 해상도. 피크가 몇 점으로 표현되는지가 핵심."""
    from src.objective import compute_features

    n_per_cond = curves.groupby("cond_id").size()
    g = curves[curves["cond_id"] == curves["cond_id"].iloc[0]].sort_values("x_norm")
    v_col = "v_full_noisy" if "v_full_noisy" in g.columns else "v_full"
    f = compute_features(g["x_norm"].to_numpy(), g[v_col].to_numpy(),
                         obj_cfg, with_peaks=True)

    d = obj_cfg.get("dqdv", {})
    win = int(d.get("window", 21))
    n_grid = int(np.isfinite(f.dqdv).sum())

    # ★ 피크 폭을 **실측**한다. 설정값(peak_halfwidth)을 되읽으면 순환 논증이다.
    from scipy.signal import find_peaks, peak_widths

    y = np.nan_to_num(np.abs(f.dqdv))
    peaks, _ = find_peaks(y, prominence=float(d.get("peak_prominence", 0.05)))
    widths_pts = peak_widths(y, peaks, rel_height=0.5)[0] if len(peaks) else np.array([])

    vg = np.asarray(f.v_grid, float)
    dv_per_pt = float((vg.max() - vg.min()) / max(1, len(vg) - 1))

    med_w = float(np.median(widths_pts)) if len(widths_pts) else float("nan")
    verdict = "판정 불가 (피크 미검출)"
    if len(widths_pts):
        if med_w < win:
            verdict = (f"★ 해상도 부족 — 피크 FWHM 중앙값 {med_w:.1f}점 < savgol 창 {win}점. "
                       f"스무딩이 피크를 통째로 뭉갠다. dQ/dV 항은 물리가 아니라 "
                       f"이산화·필터 아티팩트를 맞추게 된다.")
        elif med_w < 3 * win:
            verdict = (f"경계 — 피크 FWHM {med_w:.1f}점이 savgol 창 {win}점의 "
                       f"{med_w / win:.1f}배. 곡선 점수를 늘리는 편이 안전하다.")
        else:
            verdict = f"해상도 충분 — 피크 FWHM {med_w:.1f}점 ≫ savgol 창 {win}점."

    return {
        "points_per_condition": {
            "min": int(n_per_cond.min()), "median": int(n_per_cond.median()),
            "max": int(n_per_cond.max()),
        },
        "dqdv_grid_points": n_grid,
        "dqdv_peaks_found": int(len(peaks)),
        "peak_fwhm_points_median": med_w,
        "peak_fwhm_mV_median": med_w * dv_per_pt * 1000 if len(widths_pts) else None,
        "mV_per_grid_point": dv_per_pt * 1000,
        "savgol_window": win,
        "savgol_window_frac_of_grid": win / max(1, n_grid),
        "_판정": verdict,
    }


def _build_objective(cfg, g, ref, weights):
    """한 조건의 J(p). hessian.analyze_condition과 같은 구성."""
    from src.fitting import build_reference_interps, reconstruct, window_shortfall
    from src.objective import compute_features, default_scales, make_objective

    x = g["x_norm"].to_numpy()
    v_target = g[ref["v_col"]].to_numpy()
    f_pe, f_ne = build_reference_interps(ref.get("mode", "grid"),
                                         {"x": ref["x"], "pe": ref["pe"], "ne": ref["ne"]},
                                         ref.get("halfcell"))
    target = compute_features(x, v_target, cfg, with_peaks=True)
    scales = default_scales(compute_features(ref["x"], ref["full"], cfg))
    obs = np.isfinite(target.v)
    lo, hi = float(x[obs].min()), float(x[obs].max())
    return make_objective(target, lambda p: (x, reconstruct(p, f_pe, f_ne, x)[2]),
                          weights, scales, cfg, lambda p: window_shortfall(p, lo, hi))


def cross_evaluate(in_dir: Path, obj_cfg: dict, base: str, test: str,
                   n_sample: int, seed: int) -> dict:
    """★ 핵심 진단 — test 목적함수가 base의 해를 어떻게 평가하는가."""
    from src.fitting import extract_reference

    curves = pd.read_parquet(in_dir / "curves.parquet")
    fits = pd.read_parquet(in_dir / "fits.parquet")

    ref_rows = extract_reference(curves)
    ref = {"x": ref_rows["x_norm"].to_numpy(), "pe": ref_rows["v_pe"].to_numpy(),
           "ne": ref_rows["v_ne"].to_numpy(), "full": ref_rows["v_full"].to_numpy(),
           "v_col": "v_full_noisy" if "v_full_noisy" in curves.columns else "v_full",
           "mode": str(fits["reference"].iloc[0]) if "reference" in fits else "grid"}
    if ref["mode"] == "halfcell":
        from src.config import load_config
        from src.halfcell import get_halfcell_reference
        ref["halfcell"] = get_halfcell_reference(load_config("configs/base.yaml")).as_dict()

    A = fits[fits["objective"] == base].set_index("cond_id")
    B = fits[fits["objective"] == test].set_index("cond_id")
    common = sorted(set(A.index) & set(B.index))
    if not common:
        raise SystemExit(f"{base}/{test} 공통 조건 없음")

    rng = np.random.default_rng(seed)
    if len(common) > n_sample:
        common = [common[i] for i in rng.choice(len(common), n_sample, replace=False)]

    w_test = obj_cfg["objectives"][test]
    by_cond = {k: g.sort_values("x_norm") for k, g in curves.groupby("cond_id")}

    rows = []
    for cid in common:
        g = by_cond.get(cid)
        if g is None:
            continue
        try:
            J = _build_objective(obj_cfg, g, ref, w_test)
            pA = np.array([float(A.loc[cid, k]) for k in PARAM_NAMES])
            pB = np.array([float(B.loc[cid, k]) for k in PARAM_NAMES])
            jA, jB = float(J(pA)), float(J(pB))
        except Exception as e:  # noqa: BLE001
            log.debug("%s 실패: %s", cid, e)
            continue

        def err(row):
            return max(abs(float(row[f"{m}_hat"]) - float(row[m]))
                       for m in ("lli", "lam_pe", "lam_ne"))

        rows.append({"cond_id": cid, "J_test_at_base": jA, "J_test_at_own": jB,
                     "err_base": err(A.loc[cid]), "err_test": err(B.loc[cid])})

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("교차 평가 표본이 비었음")

    prefers_own = df["J_test_at_own"] < df["J_test_at_base"]
    base_more_accurate = df["err_base"] < df["err_test"]
    smoking_gun = prefers_own & base_more_accurate

    if base == test:
        verdict = "base == test — 배관 확인용. 해석 대상 아님"
    elif smoking_gun.mean() > 0.5:
        verdict = ("(B/C) 목적함수가 틀린 곳을 더 좋아한다 — 최적화 문제가 아니다. "
                   "해상도 보고를 함께 볼 것")
    elif prefers_own.mean() < 0.5:
        verdict = ("(A) test 목적함수가 자기 해보다 base 해를 더 좋아한다 = "
                   "최적화가 최소를 못 찾았다. 목적함수는 무죄")
    else:
        verdict = ("혼재 — test는 자기 해를 선호하지만 정확도 우위가 뚜렷하지 않다. "
                   "노이즈 수준별로 다시 볼 것")

    return {
        "base": base, "test": test, "n": int(len(df)),
        "test_prefers_own_solution_frac": float(prefers_own.mean()),
        "base_solution_more_accurate_frac": float(base_more_accurate.mean()),
        # ★ 둘 다 참인 비율 = "더 낮은 J인데 정답에서 더 멀다"
        "objective_misleading_frac": float(smoking_gun.mean()),
        "median_err_base": float(df["err_base"].median()),
        "median_err_test": float(df["err_test"].median()),
        "median_J_test_at_base": float(df["J_test_at_base"].median()),
        "median_J_test_at_own": float(df["J_test_at_own"].median()),
        "_판정": verdict,
    }


def reference_self_check(in_dir: Path, obj_cfg: dict) -> dict:
    """★ 가장 깨끗한 시험 — 무열화 조건에서 각 목적함수가 정답을 내는가.

    이 조건은 타깃 곡선이 곧 reference 곡선이므로 정답이 자명하다:
    p = (α_PE, β_PE, α_NE, β_NE) = (1, 0, 1, 0), 그리고 J = 0.

    그래서 **J(정답)과 J(찾은 해)를 직접 비교**할 수 있다. 이게 원인을 가른다.

        J(정답) ≤ J(찾은 해)  →  목적함수의 최소는 정답인데 최적화가 못 찾았다 (A)
        J(정답) >  J(찾은 해)  →  목적함수가 정답보다 다른 점을 더 좋아한다 (B/C)
                                  = 그 목적함수는 무열화 셀조차 무열화라고 못 한다
    """
    from src.fitting import extract_reference

    fits = pd.read_parquet(in_dir / "fits.parquet")
    curves = pd.read_parquet(in_dir / "curves.parquet")
    m = (fits["lli"] == 0) & (fits["lam_pe"] == 0) & (fits["lam_ne"] == 0)
    if "noise" in fits.columns:
        m &= fits["noise"] == 0
    ref_fits = fits[m]
    if ref_fits.empty:
        return {"_주의": "무열화·무노이즈 조건이 fits에 없음"}

    cid = str(ref_fits["cond_id"].iloc[0])
    g = curves[curves["cond_id"] == cid].sort_values("x_norm")
    ref_rows = extract_reference(curves)
    ref = {"x": ref_rows["x_norm"].to_numpy(), "pe": ref_rows["v_pe"].to_numpy(),
           "ne": ref_rows["v_ne"].to_numpy(), "full": ref_rows["v_full"].to_numpy(),
           "v_col": "v_full_noisy" if "v_full_noisy" in curves.columns else "v_full",
           "mode": str(fits["reference"].iloc[0]) if "reference" in fits else "grid"}
    if ref["mode"] == "halfcell":
        from src.config import load_config
        from src.halfcell import get_halfcell_reference
        ref["halfcell"] = get_halfcell_reference(load_config("configs/base.yaml")).as_dict()

    # ★ p=(1,0,1,0)이 정답인 것은 grid 기준일 때뿐이다. halfcell 기준은 전 범위
    #   테이블이라 무열화 셀도 α≠1, β≠0 이므로 이 시험을 적용하면 오탐이 난다.
    if ref["mode"] != "grid":
        return {"_주의": (f"reference={ref['mode']} 에서는 p=(1,0,1,0)이 정답이 아니다 "
                         f"(전 범위 테이블 기준이라 무열화 셀도 α≠1). "
                         f"이 시험은 --reference grid 결과에만 적용한다."),
                **{str(r["objective"]): {
                    "lam_pe_hat": float(r["lam_pe_hat"]),
                    "lam_ne_hat": float(r["lam_ne_hat"]),
                    "lli_hat": float(r["lli_hat"]), "J_at_found": float(r["J"]),
                } for _, r in ref_fits.iterrows()}}

    p_truth = np.array([1.0, 0.0, 1.0, 0.0])
    out = {}
    for _, r in ref_fits.iterrows():
        name = str(r["objective"])
        d = {"lam_pe_hat": float(r["lam_pe_hat"]), "lam_ne_hat": float(r["lam_ne_hat"]),
             "lli_hat": float(r["lli_hat"]), "J_at_found": float(r["J"]),
             "a_pe": float(r["a_pe"]), "a_ne": float(r["a_ne"])}
        try:
            J = _build_objective(obj_cfg, g, ref, obj_cfg["objectives"][name])
            j_truth = float(J(p_truth))
            d["J_at_truth"] = j_truth
            d["_판정"] = ("(A) 최적화 실패 — 목적함수의 최소는 정답 쪽인데 못 찾았다"
                         if j_truth <= d["J_at_found"] + 1e-12 else
                         "★ (B/C) 목적함수가 정답보다 다른 점을 더 좋아한다 — "
                         "무열화 셀을 무열화라고 못 한다")
        except Exception as e:  # noqa: BLE001
            d["_판정"] = f"J 재구성 실패: {e}"
        out[name] = d
    out["_기준"] = {"cond_id": cid, "p_truth": p_truth.tolist(),
                   "_설명": "정답 p=(1,0,1,0), J=0 이어야 정상"}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="목적함수 진단 (Phase 6)")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--base", default="pocv_dvdq", help="잘 나온 목적함수")
    ap.add_argument("--test", default="pocv_dvdq_dqdv", help="나빠진 목적함수")
    ap.add_argument("--n-sample", type=int, default=120)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--config", default="configs/objectives.yaml")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    from src.config import load_config

    in_dir = Path(args.in_dir)
    obj_cfg = load_config(args.config)

    out = {
        "resolution": resolution_report(
            pd.read_parquet(in_dir / "curves.parquet"), obj_cfg),
        "reference_self_check": reference_self_check(in_dir, obj_cfg),
        "cross_evaluation": cross_evaluate(in_dir, obj_cfg, args.base, args.test,
                                           args.n_sample, args.seed),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
