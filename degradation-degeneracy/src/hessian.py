"""hessian.py — 목적함수의 곡률로 flat direction을 진단한다 (Phase 5).

★ 이 지표는 **결론 근거가 아니다** (F33 / 17차 발견 7). 참고 진단으로만 쓴다.

최적점에서 J(p)의 2차 미분(4×4 Hessian)을 구하면, 고윳값이 작은 방향은
"그 방향으로 파라미터를 움직여도 J가 거의 안 변한다" = 데이터가 그 조합을
구분하지 못한다는 뜻이다.

⚠ `pe_ne_coupled` 는 최소 고윳값 고유벡터에서 α_PE·α_NE 가 **같은 부호**인지를
센다. 그런데 22p 가설은 "한쪽 과대·다른쪽 과소" 이고 α = (1−LAM)/r 이므로
α 에서도 부호가 **반대**다 — 즉 이 지표가 묻는 질문이 가설과 다르다. 22p 의
직접 증거로 읽으면 안 된다. 게다가 목적함수가 보간·미분·peak 연산을 포함해
비매끄러워 절대 step `eps` 하나로 잰 수치 Hessian 이 수렴하지 않는다
(34p 조건수 중앙값이 eps 1e-3/1e-4/1e-5 에서 12.8/229/17381).

⚠ 이 모듈의 산출물은 fit provenance validator 의 **검증 범위 밖**이다 —
곡선·obj_cfg·v_col·reference·표본·eps 연결을 어느 검사도 보지 않는다
(A·A'·B·C 미수정).

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

def resolve_curves(in_dir, curves=None) -> "Path":
    """Hessian 이 읽을 곡선 파일을 정한다 (★ 18차 A).

    우선순위
      1. 명시된 `curves` (CLI `--curves`)
      2. `<in_dir>/curves.parquet`  — producer 와 fit 이 같은 디렉터리인 배치
      3. **봉인 스냅샷** `<in_dir>/_inputs/<digest12>_curves.parquet`
         — v4 의 실제 배치. 예전에는 여기서 `FileNotFoundError` 로 죽어,
           문서가 제시하던 Hessian 재현 명령이 애초에 돌지 않았다.

    셋 다 없으면 무엇이 없는지 말하고 멈춘다 (raw FileNotFoundError 금지).
    """
    from pathlib import Path
    in_dir = Path(in_dir)
    if curves is not None:
        c = Path(curves)
        if not c.is_file():
            raise SystemExit(f"지정한 곡선 파일이 없습니다: {c}")
        return c

    direct = in_dir / "curves.parquet"
    if direct.is_file():
        return direct

    snap = sorted((in_dir / "_inputs").glob("*_curves.parquet"))
    if len(snap) == 1:
        log.info("봉인 스냅샷 곡선 사용: %s", snap[0].name)
        return snap[0]
    if len(snap) > 1:
        raise SystemExit(
            f"봉인 스냅샷에 곡선이 여러 개입니다 ({[x.name for x in snap]}) — "
            f"--curves 로 지정하세요")

    raise SystemExit(
        f"곡선 파일을 찾지 못했습니다. 다음 중 하나가 필요합니다:\n"
        f"  - {direct}\n"
        f"  - {in_dir / '_inputs'}/<digest>_curves.parquet (봉인 스냅샷)\n"
        f"  - --curves <경로>")


def _sealed_halfcell_staging(in_dir) -> "Path | None":
    """봉인 스냅샷의 half-cell 캐시를 **정규 이름**으로 펼친 임시 캐시 디렉터리.

    ★ 18차 A' — 예전에는 live `configs/base.yaml` 과 live `.cache` 를 읽었다.
    봉인된 입력이 있는데도 실행 시점 파일을 보므로, 그 사이 바뀌면 다른 기준
    곡선으로 곡률을 잰다. 스냅샷 파일명은 `<digest12>_<원래이름>` 이라
    캐시 키 조회가 안 되므로 원래 이름으로 복사해 둔다.
    """
    import shutil
    import tempfile
    from pathlib import Path

    snap = Path(in_dir) / "_inputs"
    if not snap.is_dir():
        return None
    cached = [p for p in snap.glob("*_*.json")] + \
             [p for p in snap.glob("*_*.meta.yaml")]
    if not cached:
        return None
    staging = Path(tempfile.mkdtemp(prefix="hessian_sealed_hc_"))
    for p in cached:
        shutil.copy2(p, staging / p.name.split("_", 1)[1])
    return staging


def _sealed_base_config(in_dir) -> "Path | None":
    """봉인 스냅샷의 `base.yaml` (★ 18차 A')."""
    from pathlib import Path
    hits = sorted((Path(in_dir) / "_inputs").glob("*_base.yaml"))
    return hits[0] if len(hits) == 1 else None


def run_hessian(in_dir, out_dir=None, objective: str = "pocv_dvdq",
                n_sample: int | None = 200, seed: int = 0,
                objectives_config: str = "configs/objectives.yaml",
                eps: float = 1e-4, curves=None) -> dict:
    """fits.parquet의 최적점에서 Hessian을 계산 (표본 추출 지원)."""
    from pathlib import Path

    import pandas as pd

    from src.config import load_config
    from src.fitting import extract_reference, PARAM_NAMES as FIT_PARAMS

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    obj_cfg = load_config(objectives_config)
    weights = obj_cfg["objectives"][objective]

    # ★ 18차 A — 분리 배치에서는 봉인 스냅샷을 스스로 찾는다
    curves_path = resolve_curves(in_dir, curves)
    curves = pd.read_parquet(curves_path)
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
        # ★ 18차 A' — live config·live cache 대신 **봉인 입력**을 쓴다.
        from src.halfcell import get_halfcell_reference
        _cfg_path = _sealed_base_config(in_dir)
        _cache = _sealed_halfcell_staging(in_dir)
        if _cfg_path is None or _cache is None:
            log.warning("봉인된 half-cell 입력을 찾지 못해 live 파일을 씁니다 — "
                        "이 결과는 인용할 수 없습니다 (18차 A')")
        ref["halfcell"] = get_halfcell_reference(
            load_config(str(_cfg_path) if _cfg_path else "configs/base.yaml"),
            cache_dir=_cache).as_dict()

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
        "★ 조건수는 eps에 강하게 의존한다. 목적함수가 여러 스케일에서 울퉁불퉁하면 "
        "수치 Hessian 이 수렴하지 않는다 — **절대값도 목적함수 간 순서도 인용하지 "
        "말 것** (18차 발견 7: 순서가 eps 에 안정적이라는 근거는 확인되지 않았다).")
    log.info("Hessian 요약: %s", summary)
    log.info("저장: %s", path)

    # ★ 18차 B — 예전에는 `degeneracy_summary.yaml` 을 **덮어썼다.** 채점
    #   산출물을 곡률 진단이 변이시키므로 `score → hessian → report` 순서에서
    #   보고서가 stale 로 찍혔다. 자기 sidecar 에만 쓴다.
    import yaml
    side = out_dir / "hessian_summary.yaml"
    doc = {}
    if side.exists():
        try:
            doc = yaml.safe_load(side.read_text(encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            log.warning("hessian_summary.yaml 읽기 실패, 새로 씁니다: %s", e)
            doc = {}
    doc[objective] = {k: v for k, v in summary.items() if not k.startswith("_")}
    doc["_주의"] = (
        "★ 이 파일은 **인용 범위 밖**이다. fit provenance validator 는 Hessian 의 "
        "곡선·obj_cfg·v_col·reference·표본·eps 연결을 검증하지 않는다. "
        "조건수는 절대값도 목적함수 간 순서도 인용하지 말 것 — eps 를 바꾸면 값이 "
        "자릿수로 움직이고(18차 발견 7), 순서가 eps 에 안정적이라는 근거는 없다. "
        "곡선 출처: " + str(curves_path))
    side.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                    encoding="utf-8")
    log.info("저장: %s", side)
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
    # ★ 18차 A — 분리 배치에서 곡선을 명시할 수 있게 한다
    ap.add_argument("--curves", default=None,
                    help="곡선 parquet 경로 (생략 시 <in>/curves.parquet 또는 "
                         "봉인 _inputs 스냅샷에서 자동 해석)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    s = run_hessian(args.in_dir, args.out, args.objective, args.n_sample,
                    eps=args.eps, curves=args.curves)
    print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
