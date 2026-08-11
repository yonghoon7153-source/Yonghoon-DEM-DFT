"""weight_sweep.py — dQ/dV 가중치 최적화 (Phase 6).

목적: **"가중치를 결과가 좋게 나오도록 임의로 튜닝한 것 아니냐"** 는 질문에
숫자로 답한다. w_dqdv를 0~2로 훑어 degeneracy 비율이 최소가 되는 값을 찾고,
그 탐색 곡선 자체를 근거로 남긴다.

비용 설계
─────────
전체 격자(3,069조건)에 9가지 가중치를 다 돌리면 CPU로 감당이 안 된다.
그래서 **층화 표본**을 쓴다. 축마다 격자를 반으로 성기게(step 0.02 → 0.04)
잡아 (lli, lam_pe, lam_ne) 하위격자에 놓인 조건만 고른다. 무작위 표본이
아니라 격자 구조를 보존하므로, 코너·중앙이 빠지지 않는다.

  전체 11×11×11×noise3 = 3,993   →   표본 6×6×6×noise3 = 648 (guard 통과분만)

★ optimizer 설정을 본 실행과 다르게 두면 안 된다. 비용을 아끼거나 "공정하게"
하려고 건드렸다가 두 번 틀렸고, 두 번 다 **가중치가 아니라 최적화 난이도를
재는** 결과가 나왔다.

  F20c  restart 5 → 2 로 낮춤: 같은 목적함수·같은 조건에서 본 실행 17% vs
        sweep 92%. `pocv_dvdq`는 unique_min이 39%뿐이라 restart가 여러 번
        필요한 목적함수이고, 2번으로는 나쁜 국소최소에 자주 갇힌다.
  F20d  warm start를 끔("모두 같은 출발선"): w>0만 초기값을 잃어 dQ/dV 항을
        못 푼다. w=1의 J중앙값 0.406 vs 본 실행 0.326, 51.7%의 조건에서 더
        크고 평균|err| 6.17 vs 2.48%p. 최적 w가 0.5 → 0.0으로 뒤집혔다.

비용은 **층화 표본으로만** 아낀다. optimizer는 건드리지 않는다.

  468조건 × 9가중치 × 5restart ≈ 2.1만 최적화 ≈ 75분 (32워커 기준)

sweep의 양 끝점은 본 실행의 목적함수와 정의가 같으므로(w=0 ≡ pocv_dvdq,
w=1 ≡ pocv_dvdq_dqdv) **결과가 일치해야 한다.** `tools/check_sweep_consistency.py`
가 이걸 계산 없이 확인한다. 돌리고 나면 반드시 통과시킬 것.

리뷰 규칙
─────────
F10 dQ/dV 계열은 노이즈에서 피크 가중이 희석된다. 최적 w를 **노이즈 수준별로**
    따로 보고하고, 하나의 값으로 뭉개지 않는다.
F1  복원불가군(α_true<1)을 뺀 뒤에 비율을 센다. 안 그러면 모든 가중치가
    똑같이 나쁘게 보여 차이가 묻힌다.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

# w_dqdv 탐색 격자 (04_PROMPTS.md Phase 6: --w-dqdv 0:2:0.25)
DEFAULT_W_GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]


def obj_name(w: float) -> str:
    return f"wdqdv_{w:.2f}"


SEED_NAME = "_seed"      # w_grid에 0.0이 없을 때만 끼우는 숨은 seed 제공자


def build_weight_objectives(w_grid=DEFAULT_W_GRID, w_pocv: float = 1.0,
                            w_dvdq: float = 1.0) -> dict:
    """w_dqdv만 바꾼 목적함수 집합. pocv·dvdq 가중치는 34p 정의대로 1.0 고정.

    ★ warm start를 **본 실행과 똑같이** 켠 채로 돌린다 (F20d).

    한때 "모두 같은 출발선"이 공정하다고 보고 껐다가 틀렸다. sweep의 양 끝점은
    본 실행의 목적함수와 정의가 글자 그대로 같으므로(w=0 ≡ pocv_dvdq,
    w=1 ≡ pocv_dvdq_dqdv) **같은 답이 나와야** 하는데, 끄면 w=1만 어긋난다.

      tools/check_sweep_consistency.py 실측 (공통 468조건)
        w=0 : J중앙값 0.1440 = 0.1440,  degeneracy 58.23% = 58.23%   (일치)
        w=1 : J중앙값 0.4060 > 0.3261,  51.7%의 조건에서 sweep의 J가 더 큼
              평균|err| 6.17%p vs 2.48%p

    즉 warm start를 끈 sweep이 잰 것은 가중치의 가치가 아니라 **"dQ/dV 항은
    좋은 초기값 없이는 optimizer가 못 푼다"** 였다(F20에서 이미 확인한 현상).
    그 상태로 최적 w를 고르면 정보량이 아니라 최적화 난이도를 고르게 된다.

    공정의 기준은 "모두에게 똑같이"가 아니라 **"본 실행이 쓰는 설정 그대로"** 다.
    본 실행에서 `pocv_dvdq`는 seed 제공자라 warm start를 못 받고 dQ/dV 계열만
    받는데, sweep도 w=0이 seed 제공자가 되어 정확히 같은 구조가 된다.
    (w=0이 자기 해를 자기 초기값으로 받는 건 이득이 아니므로 비대칭이 아니다 —
     위 실측에서 w=0이 본 실행과 소수점까지 일치하는 것이 그 증거다.)

    w_grid에 0.0이 없으면 seed 제공자가 없으므로 숨은 `_seed`를 앞에 끼운다.
    """
    objs = {obj_name(w): {"w_pocv": w_pocv, "w_dvdq": w_dvdq, "w_dqdv": float(w)}
            for w in w_grid}
    if not any(float(w) == 0.0 for w in w_grid):
        # dict는 삽입 순서를 지키므로 맨 앞이 곧 seed 제공자가 된다
        return {SEED_NAME: {"w_pocv": w_pocv, "w_dvdq": w_dvdq, "w_dqdv": 0.0}} | objs
    return objs


# ---------------------------------------------------------------- 층화 표본

def stratified_subset(curves: pd.DataFrame, stride: int = 2,
                      axes=("lli", "lam_pe", "lam_ne")) -> list[str]:
    """축마다 격자값을 stride 간격으로 솎아낸 하위격자 위의 cond_id.

    무작위 추출을 쓰지 않는 이유: 격자 코너(저LLI·고LAM 등)가 빠지면
    바로 그 영역에서 가중치 효과가 갈리는데 그걸 못 본다.
    """
    keep_vals = {}
    for a in axes:
        vals = np.sort(curves[a].unique())
        keep_vals[a] = set(vals[::stride].tolist())
        # 축 끝값은 반드시 포함 (코너 보존)
        keep_vals[a].add(float(vals[-1]))

    m = pd.Series(True, index=curves.index)
    for a in axes:
        m &= curves[a].isin(keep_vals[a])
    sub = curves[m]
    ids = sorted(sub["cond_id"].unique())
    log.info("층화 표본: %d조건 (전체 %d, stride=%d, 축별 값 %s)",
             len(ids), curves["cond_id"].nunique(), stride,
             {a: len(v) for a, v in keep_vals.items()})
    return ids


# ---------------------------------------------------------------- 집계

def sweep_summary(scored: pd.DataFrame, tol: float = 0.02) -> pd.DataFrame:
    """가중치별 × 노이즈별 degeneracy 지표 (F1 복원가능군 한정, F10 노이즈 분리)."""
    from src.scoring import MODES

    df = scored[scored["recoverable"]] if "recoverable" in scored else scored
    df = df[df["objective"] != SEED_NAME]      # 숨은 seed는 비교 대상이 아니다
    rows = []
    group_cols = ["objective"] + (["noise"] if "noise" in df.columns else [])
    for key, g in df.groupby(group_cols):
        o = key[0] if isinstance(key, tuple) else key
        noise = key[1] if isinstance(key, tuple) and len(key) > 1 else np.nan
        rows.append({
            "objective": o,
            "w_dqdv": float(o.split("_")[-1]) if o.startswith("wdqdv_") else np.nan,
            "noise": noise,
            "n": int(len(g)),
            "degenerate_frac": float(g["degenerate"].mean()),
            "degenerate_frac_corrected": float(g["degenerate_corrected"].mean())
            if "degenerate_corrected" in g else np.nan,
            "mean_abs_err": float(g["abs_err_max"].mean()),
            "pe_ne_antisym_frac": float(g["pe_ne_antisym"].mean()),
            **{f"mean_abs_err_{k}": float(g[f"err_{k}"].abs().mean()) for k in MODES},
        })
    return pd.DataFrame(rows).sort_values(["noise", "w_dqdv"]).reset_index(drop=True)


def pick_optimum(summary: pd.DataFrame,
                 metric: str = "degenerate_frac_corrected") -> dict:
    """노이즈별 최적 w와, 전 노이즈 평균 기준 최적 w.

    ★ 노이즈별로 최적이 갈리면 하나로 못 정한다 — 그 사실 자체를 보고한다.
    실험 노이즈 수준을 모르는 채 한 값을 고르면 그게 곧 튜닝이다.
    """
    col = metric if metric in summary.columns else "degenerate_frac"
    per_noise = {}
    for n, g in summary.groupby("noise"):
        best = g.loc[g[col].idxmin()]
        per_noise[float(n)] = {"w_dqdv": float(best["w_dqdv"]),
                               col: float(best[col]),
                               "n": int(best["n"])}
    mean_by_w = summary.groupby("w_dqdv")[col].mean()
    w_star = float(mean_by_w.idxmin())
    ws = sorted(per_noise, key=lambda k: k)
    agree = len({per_noise[n]["w_dqdv"] for n in ws}) == 1
    return {
        "metric": col,
        "per_noise": per_noise,
        "w_star_mean_over_noise": w_star,
        "value_at_w_star": float(mean_by_w.min()),
        "value_at_w1": float(mean_by_w.get(1.0, np.nan)),
        "noise_levels_agree": agree,
        "_주의": ("노이즈 수준별 최적 w가 다르면 단일 값 채택은 근거가 약하다. "
                 "실험 노이즈 수준을 먼저 특정할 것." if not agree else
                 "모든 노이즈 수준에서 같은 w가 최적 — 단일 값 채택 근거 있음."),
    }


def write_optimized_config(out_path, opt: dict, w_pocv: float = 1.0,
                           w_dvdq: float = 1.0) -> None:
    """configs/objectives_optimized.yaml — 탐색 근거를 주석으로 함께 남긴다."""
    from pathlib import Path

    import yaml

    w = opt["w_star_mean_over_noise"]
    body = {
        "objectives": {
            "pocv_dvdq_dqdv_opt": {"w_pocv": w_pocv, "w_dvdq": w_dvdq,
                                   "w_dqdv": float(w)},
        },
        "_provenance": {
            "source": "src/weight_sweep.py — Phase 6 가중치 탐색",
            "metric": opt["metric"],
            "per_noise_optimum": opt["per_noise"],
            "value_at_w_star": opt["value_at_w_star"],
            "value_at_w1_default": opt["value_at_w1"],
            "noise_levels_agree": opt["noise_levels_agree"],
            "note": opt["_주의"],
        },
    }
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "# 자동 생성 — 직접 편집하지 말 것 (src/weight_sweep.py가 덮어씀)\n"
        "# w_dqdv는 임의 튜닝이 아니라 degeneracy 비율 최소화로 선택된 값이다.\n"
        "# 탐색 곡선은 results/.../weight_sweep_summary.csv 참조.\n"
        + yaml.safe_dump(body, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    log.info("저장: %s (w_dqdv=%.2f)", p, w)


# ---------------------------------------------------------------- 실행

def run_weight_sweep(in_dir, out_dir=None, w_grid=DEFAULT_W_GRID,
                     stride: int = 2, n_restarts: int = 5, nproc: int = 8,
                     bounds_preset: str = "expanded", reference: str = "grid",
                     tol: float = 0.02, resume: bool = False,
                     objectives_config: str = "configs/objectives.yaml",
                     base_config: str = "configs/base.yaml",
                     warm_start: bool = True, adaptive: bool = True,
                     method: str | None = None) -> dict:
    from pathlib import Path

    import yaml

    from src.config import load_config
    from src.fitting import run_fit
    from src.scoring import (add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias)

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir / "wsweep"
    out_dir.mkdir(parents=True, exist_ok=True)

    obj_cfg = load_config(objectives_config)
    bounds = obj_cfg["fitting"]["bounds_presets"][bounds_preset]
    # ★ F79/8차 발견 8 — config 의 method 를 실제로 읽는다 (본 실행과 같은 경로).
    #   예전에는 run_fit 기본값에 묵시적으로 의존했다 — "우연히 같을 뿐"이었다.
    method = method or str(obj_cfg.get("fitting", {}).get("method", "Nelder-Mead"))

    # ★ F79 — subset 을 정하는 read 도 봉인 대상이다. 예전에는 원본 curves 를
    #   읽어 subset 을 정한 **뒤에야** run_fit 의 seal/snapshot 이 시작돼, 그
    #   사이에 파일이 바뀌면 subset 과 계산이 다른 곡선에서 나왔다.
    #   여기서 digest 를 뜨고, run_fit 이 봉인한 값과 대조해 fail-closed 한다.
    from src.io import canonical_input_key, file_digest
    curves_path = in_dir / "curves.parquet"
    subset_curves_sha = file_digest(curves_path)
    curves = pd.read_parquet(curves_path,
                             columns=["cond_id", "lli", "lam_pe", "lam_ne"])
    subset = stratified_subset(curves.drop_duplicates("cond_id"), stride)
    if file_digest(curves_path) != subset_curves_sha:
        raise RuntimeError(
            "subset 계산 도중 curves.parquet 이 바뀌었습니다 (F79)")

    objectives = build_weight_objectives(w_grid)
    log.info("가중치 sweep: %d조건 × %d가중치 × %drestart",
             len(subset), len(objectives), n_restarts)

    # ★ warm_start는 본 실행과 같은 값이어야 한다 (F20d). 끄면 w>0만 optimizer
    #   실패에 빠져, sweep이 가중치가 아니라 최적화 난이도를 재게 된다.
    run_fit(in_dir, out_dir, obj_cfg, objectives, bounds, bounds_preset,
            n_restarts, nproc, use_noisy=True, base_config=base_config,
            reference=reference, resume=resume, subset=set(subset),
            warm_start=warm_start, adaptive=adaptive, method=method)

    # ★ F79 — run_fit 이 봉인한 곡선이 subset 을 정한 곡선과 같아야 한다
    man = yaml.safe_load((out_dir / "manifest.yaml").read_text(encoding="utf-8"))
    sealed_sha = (man.get("input_sha256") or {}).get(
        canonical_input_key(curves_path))
    if sealed_sha != subset_curves_sha:
        raise RuntimeError(
            f"subset 을 정한 곡선({subset_curves_sha})과 fitting 이 봉인한 "
            f"곡선({sealed_sha})이 다릅니다 — 그 사이에 파일이 바뀌었습니다 (F79)")

    fits = pd.read_parquet(out_dir / "fits.parquet")
    scored = classify_recoverability(add_error_columns(fits, tol))
    # 바이어스는 가중치별로 따로 잰다 — 가중치가 방법 바이어스 자체를 바꾸므로
    # 공통 바이어스를 빼면 비교가 왜곡된다 (F5)
    scored = apply_bias_correction(scored, clean_bias(scored), tol)

    summary = sweep_summary(scored, tol)
    summary.to_csv(out_dir / "weight_sweep_summary.csv", index=False)
    opt = pick_optimum(summary)

    # ★ optimizer 설정을 결과에 박아 둔다 (F20b/F20d). 이 sweep은 본 실행과
    #   설정이 같을 때만 인용할 수 있고, 그걸 읽는 쪽이 확인할 수 있어야 한다.
    used_seed = SEED_NAME in objectives
    warn = None
    if not warm_start:
        warn = ("warm start가 꺼진 채 실행됐다 — w>0만 초기값을 잃어 optimizer가 "
                "dQ/dV 항을 못 푼다. 실측으로 w=1의 J중앙값이 본 실행보다 크고"
                "(0.406 vs 0.326, 51.7%의 조건에서 더 큼) 평균|err|이 6.17 vs "
                "2.48%p였다. 이 결과의 최적 w를 인용하지 말 것 — 가중치가 아니라 "
                "최적화 난이도를 고른 값이다. tools/check_sweep_consistency.py로 "
                "본 실행과 대조할 수 있다.")
    elif n_restarts < 5:
        warn = (f"n_restarts={n_restarts}로 실행됐다 — pocv_dvdq는 unique_min이 "
                "39%뿐이라 restart가 부족하면 나쁜 국소최소에 갇힌다(F20c). "
                "최적 w를 인용하지 말 것.")
    # ★ F79 — tol 은 최적 w 를 바꾸는데 기록되지 않았고, sweep 산출물과 fits 를
    #   잇는 digest 도 없었다. 전부 박는다.
    (out_dir / "weight_sweep.yaml").write_text(
        yaml.safe_dump({"w_grid": list(map(float, w_grid)),
                        "n_conditions": len(subset), "stride": stride,
                        "n_restarts": n_restarts, "tol": float(tol),
                        "method": method, "adaptive": bool(adaptive),
                        "seed_objective_used": bool(used_seed),
                        "warm_start": bool(warm_start),
                        "subset_curves_sha": subset_curves_sha,
                        "fits_sha256": file_digest(out_dir / "fits.parquet",
                                                   full=True),
                        "optimum": opt}
                       | ({"_경고": warn} if warn else {}),
                       allow_unicode=True, sort_keys=False), encoding="utf-8")
    # ★ F79 — tracked config 를 실행이 덮어쓰면 worktree 가 dirty 가 되고,
    #   "최적 가중치 채택"이라는 결정이 검토 없이 저장소에 들어간다.
    #   run 디렉터리에 쓰고, configs/ 로의 승격은 사람이 커밋으로 한다.
    write_optimized_config(str(out_dir / "objectives_optimized.yaml"), opt)

    log.info("가중치별 요약:\n%s", summary.round(4).to_string(index=False))
    log.info("최적 w_dqdv = %.2f (노이즈 평균 %s %.4f, w=1.0일 때 %.4f)",
             opt["w_star_mean_over_noise"], opt["metric"],
             opt["value_at_w_star"], opt["value_at_w1"])
    return opt


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(description="dQ/dV 가중치 sweep (Phase 6)")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--w-grid", default=None,
                    help="쉼표 목록 또는 start:stop:step (기본 0:2:0.25)")
    ap.add_argument("--stride", type=int, default=2,
                    help="격자 솎기 간격 (2면 축당 11→6값)")
    ap.add_argument("--n-restarts", type=int, default=5)
    ap.add_argument("--nproc", type=int, default=8)
    ap.add_argument("--bounds", default="expanded")
    ap.add_argument("--reference", default="grid")
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--no-adaptive", dest="adaptive", action="store_false",
                    help="적응적 조기 종료를 끈다 (F66/F79 — 기록에 남는다)")
    ap.add_argument("--no-warm-start", dest="warm_start", action="store_false",
                    help="warm start를 끈다. 본 실행과 설정이 달라져 최적 w를 "
                         "인용할 수 없게 되므로 진단 목적으로만 쓸 것 (F20d)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    if args.w_grid:
        if ":" in args.w_grid:
            a, b, s = (float(x) for x in args.w_grid.split(":"))
            w_grid = list(np.round(np.arange(a, b + s / 2, s), 6))
        else:
            w_grid = [float(x) for x in args.w_grid.split(",")]
    else:
        w_grid = DEFAULT_W_GRID

    opt = run_weight_sweep(args.in_dir, args.out, w_grid, args.stride,
                           args.n_restarts, args.nproc, args.bounds,
                           args.reference, args.tol, args.resume,
                           warm_start=args.warm_start, adaptive=args.adaptive)
    print(json.dumps(opt, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
