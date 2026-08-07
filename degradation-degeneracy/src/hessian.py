"""hessian.py — 목적함수의 곡률로 flat direction을 진단한다 (Phase 5).

★ 이것이 degeneracy의 **직접 증거**다.

최적점에서 J(p)의 2차 미분(4×4 Hessian)을 구하면, 고윳값이 작은 방향은
"그 방향으로 파라미터를 움직여도 J가 거의 안 변한다" = 데이터가 그 조합을
구분하지 못한다는 뜻이다.

특히 최소 고윳값의 고유벡터에서 **α_PE와 α_NE 성분이 같은 부호로 묶여 있으면**,
"PE와 NE를 함께 움직여도 곡선이 안 변한다" → 22p에서 LAM_PE ≈ LAM_NE가
나온 이유가 물리가 아니라 **수학**임을 가리킨다.

지표:
  eigvals              고윳값 4개 (오름차순)
  condition_number     최대/최소 — 클수록 심한 degeneracy
  flat_direction_score 최소/최대 — 0에 가까울수록 평평한 골짜기
  flat_vec_*           최소 고윳값의 고유벡터 성분 (a_pe, b_pe, a_ne, b_ne)
  pe_ne_coupled        |v_a_pe|·|v_a_ne| 가 둘 다 유의하고 부호가 같은가
"""

from __future__ import annotations

import logging

import numpy as np

log = logging.getLogger(__name__)

PARAM_NAMES = ("a_pe", "b_pe", "a_ne", "b_ne")


def numerical_hessian(objective, p, eps: float = 1e-4) -> np.ndarray:
    """중심차분 Hessian.

    eps 기본값이 큰 이유: reference 곡선 보간이 조각선형이라 너무 작은 스텝은
    한 조각 안에서만 움직여 2차 미분이 0으로 나온다 (fitting.py의 L-BFGS-B
    실패와 같은 원인). 여러 보간 구간을 가로지르는 크기를 쓴다.
    """
    p = np.asarray(p, float)
    n = len(p)
    H = np.zeros((n, n))
    f0 = float(objective(p))

    for i in range(n):
        for j in range(i, n):
            ei = np.zeros(n); ei[i] = eps
            ej = np.zeros(n); ej[j] = eps
            if i == j:
                fpp = float(objective(p + ei))
                fmm = float(objective(p - ei))
                H[i, i] = (fpp - 2 * f0 + fmm) / eps ** 2
            else:
                fpp = float(objective(p + ei + ej))
                fpm = float(objective(p + ei - ej))
                fmp = float(objective(p - ei + ej))
                fmm = float(objective(p - ei - ej))
                H[i, j] = H[j, i] = (fpp - fpm - fmp + fmm) / (4 * eps ** 2)
    return H


def eigen_analysis(H: np.ndarray, coupling_tol: float = 0.3) -> dict:
    """고윳값 분해 → degeneracy 지표."""
    H = 0.5 * (H + H.T)                      # 대칭화 (수치 오차 제거)
    w, V = np.linalg.eigh(H)                 # 오름차순
    order = np.argsort(w)
    w, V = w[order], V[:, order]

    w_min, w_max = float(w[0]), float(w[-1])
    v = V[:, 0]                              # 최소 고윳값의 고유벡터 = 평평한 방향
    # 부호 규약: 최대 성분이 양수가 되게 고정 (해석 일관성)
    if v[np.argmax(np.abs(v))] < 0:
        v = -v

    a_pe, a_ne = float(v[0]), float(v[2])
    coupled = bool(abs(a_pe) > coupling_tol and abs(a_ne) > coupling_tol
                   and a_pe * a_ne > 0)

    return {
        **{f"eigval_{i}": float(x) for i, x in enumerate(w)},
        "condition_number": float(w_max / w_min) if w_min > 0 else float("inf"),
        "flat_direction_score": float(w_min / w_max) if w_max > 0 else float("nan"),
        "min_eigval_positive": bool(w_min > 0),
        **{f"flat_vec_{k}": float(x) for k, x in zip(PARAM_NAMES, v)},
        # ★ α_PE·α_NE가 같은 부호로 묶여 있는가 = 22p 패턴의 수학적 근원
        "pe_ne_coupled": coupled,
    }


def analyze_condition(cfg_objectives: dict, curves_g, ref: dict, p_opt,
                      weights: dict, eps: float = 1e-4) -> dict:
    """한 조건의 Hessian 분석. curves_g는 그 조건의 곡선 DataFrame."""
    from src.fitting import (build_reference_interps, make_ref_interp,  # noqa: F401
                             reconstruct, window_shortfall)
    from src.objective import compute_features, default_scales, make_objective

    x = curves_g["x_norm"].to_numpy()
    v_target = curves_g[ref["v_col"]].to_numpy()
    grid_ref = {"x": ref["x"], "pe": ref["pe"], "ne": ref["ne"]}
    f_pe, f_ne = build_reference_interps(ref.get("mode", "grid"), grid_ref,
                                         ref.get("halfcell"))

    target = compute_features(x, v_target, cfg_objectives, with_peaks=True)
    ref_feat = compute_features(ref["x"], ref["full"], cfg_objectives)
    scales = default_scales(ref_feat)

    obs = np.isfinite(target.v)
    lo, hi = float(x[obs].min()), float(x[obs].max())
    J = make_objective(target, lambda p: (x, reconstruct(p, f_pe, f_ne, x)[2]),
                       weights, scales, cfg_objectives,
                       lambda p: window_shortfall(p, lo, hi))

    H = numerical_hessian(J, p_opt, eps)
    return {**eigen_analysis(H), "J_at_opt": float(J(p_opt))}


# ---------------------------------------------------------------- CLI

def run_hessian(in_dir, out_dir=None, objective: str = "pocv_dvdq",
                n_sample: int | None = 200, seed: int = 0,
                objectives_config: str = "configs/objectives.yaml",
                eps: float = 1e-4) -> dict:
    """fits.parquet의 최적점에서 Hessian을 계산 (표본 추출 지원)."""
    from pathlib import Path

    import pandas as pd

    from src.config import load_config
    from src.fitting import extract_reference, PARAM_NAMES as FIT_PARAMS

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    obj_cfg = load_config(objectives_config)
    weights = obj_cfg["objectives"][objective]

    curves = pd.read_parquet(in_dir / "curves.parquet")
    fits = pd.read_parquet(in_dir / "fits.parquet")
    fits = fits[fits["objective"] == objective]
    if fits.empty:
        raise SystemExit(f"목적함수 {objective} 행이 없음")

    ref_rows = extract_reference(curves)
    v_col = "v_full_noisy" if "v_full_noisy" in curves.columns else "v_full"
    ref = {"x": ref_rows["x_norm"].to_numpy(), "pe": ref_rows["v_pe"].to_numpy(),
           "ne": ref_rows["v_ne"].to_numpy(), "full": ref_rows["v_full"].to_numpy(),
           "v_col": v_col, "mode": str(fits["reference"].iloc[0])
           if "reference" in fits.columns else "grid"}
    if ref["mode"] == "halfcell":
        from src.halfcell import get_halfcell_reference
        ref["halfcell"] = get_halfcell_reference(load_config("configs/base.yaml")).as_dict()

    if n_sample and len(fits) > n_sample:
        fits = fits.sample(n=n_sample, random_state=seed)
        log.info("표본 %d조건으로 Hessian 계산 (전체 %d)", n_sample, len(fits))

    rows = []
    by_cond = {k: g.sort_values("x_norm") for k, g in curves.groupby("cond_id")}
    for _, r in fits.iterrows():
        g = by_cond.get(r["cond_id"])
        if g is None:
            continue
        p_opt = [float(r[k]) for k in FIT_PARAMS]
        try:
            res = analyze_condition(obj_cfg, g, ref, p_opt, weights, eps)
        except Exception as e:  # noqa: BLE001
            log.debug("Hessian 실패 %s: %s", r["cond_id"], e)
            continue
        rows.append({"cond_id": r["cond_id"], "objective": objective, "eps": eps,
                     **{k: r[k] for k in ("lli", "lam_pe", "lam_ne", "noise")
                        if k in r},
                     **res})

    df = pd.DataFrame(rows)
    path = out_dir / f"hessian_{objective}.parquet"
    df.to_parquet(path, index=False)

    summary = {
        "objective": objective, "n": int(len(df)), "eps": eps,
        "median_condition_number": float(df["condition_number"].median()),
        "median_flat_score": float(df["flat_direction_score"].median()),
        "pe_ne_coupled_frac": float(df["pe_ne_coupled"].mean()),
        "min_eigval_positive_frac": float(df["min_eigval_positive"].mean()),
    }
    summary["_주의"] = (
        "★ 조건수는 eps에 강하게 의존한다 (실측: pocv_dvdq_dqdv에서 "
        "eps 1e-3/1e-4/1e-5 → 12.8/229/17381). 목적함수가 여러 스케일에서 "
        "울퉁불퉁하면 Hessian이 수렴하지 않으므로, **절대값을 인용하지 말고 "
        "같은 eps에서 목적함수끼리만 비교할 것.**")
    log.info("Hessian 요약: %s", summary)
    log.info("저장: %s", path)

    # ★ degeneracy_summary.yaml에도 올린다 — 결론에서 쓰려면 한 곳에 있어야 한다.
    #   "평평한 방향이 PE-NE 결합인가"는 22p 가설의 직접적인 검정이라 표에만 두면 묻힌다.
    ds = out_dir / "degeneracy_summary.yaml"
    if ds.exists():
        import yaml
        try:
            doc = yaml.safe_load(ds.read_text(encoding="utf-8")) or {}
            doc["hessian_pe_ne_coupled_frac"] = summary["pe_ne_coupled_frac"]
            doc["hessian_eps"] = eps
            ds.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                          encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            log.warning("degeneracy_summary.yaml 갱신 실패: %s", e)
    return summary


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Hessian / flat direction 분석")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--objective", default="pocv_dvdq")
    ap.add_argument("--n-sample", dest="n_sample", type=int, default=200)
    ap.add_argument("--eps", type=float, default=1e-4)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    s = run_hessian(args.in_dir, args.out, args.objective, args.n_sample, eps=args.eps)
    print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
