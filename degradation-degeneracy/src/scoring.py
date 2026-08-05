"""scoring.py — degeneracy 판정 (Phase 5).

정답을 아는 합성 데이터에서 fitting이 그 정답을 복원했는지 채점한다.

────────────────────────────────────────────────────────────────────────
적대적 리뷰가 강제한 규칙 (docs/06_REVIEW_DECISIONS.md §3) — 여기 다 반영돼 있다.

F1  grid 기준에서 참값 α<1인 조건은 **원리적으로 복원 불가**다.
    재구성 창이 reference 곡선 범위를 넘어서기 때문이며, 이 벽은 box bound가
    아니라 창 부족 벌점이 만드는 소프트 벽이라 `bound_active`에 안 잡힌다.
    → `recoverable=False`로 분리하고, 주 지표는 복원가능군에서만 센다.

F5  판정 기준(2%p)이 **방법 자체의 바이어스와 같은 크기**다.
    → 노이즈 0 조건에서 목적함수별 바이어스를 재고, 그것을 뺀 잔차로도 함께 판정한다.

F4  adaptive 조기 종료 때문에 조건마다 restart 수가 다르다.
    → multi-start 기반 지표는 `n_restarts`로 조건화해서만 보고한다.

F14 격자에 "저LLI + 고LAM_PE" 코너가 없다 (완방 프레임 guard의 산물).
    → 요약에 커버리지 공백을 명시해 결론이 과대 해석되지 않게 한다.
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

MODES = ("lli", "lam_pe", "lam_ne")
DEFAULT_TOL = 0.02          # 2%p — configs/objectives.yaml scoring.tolerance


# ---------------------------------------------------------------- 기본 채점

def score(truth: dict, recovered: dict, tol: float = DEFAULT_TOL) -> dict:
    """단일 조건 채점 (03_ARCHITECTURE.md 5절).

    pe_ne_antisym: PE와 NE 오차가 **반대 부호** — degeneracy의 특징적 지문.
    한쪽을 과대평가한 만큼 다른 쪽을 과소평가해 full-cell 곡선에서 상쇄된 것.
    """
    err = {k: float(recovered[k]) - float(truth[k]) for k in MODES}
    abs_err_max = max(abs(v) for v in err.values())
    return {
        **{f"err_{k}": v for k, v in err.items()},
        "abs_err_max": abs_err_max,
        "pe_ne_antisym": bool(err["lam_pe"] * err["lam_ne"] < 0),
        "pe_ne_gap_true": abs(float(truth["lam_pe"]) - float(truth["lam_ne"])),
        "pe_ne_gap_recovered": abs(float(recovered["lam_pe"])
                                   - float(recovered["lam_ne"])),
        "degenerate": bool(abs_err_max > tol),
    }


def add_error_columns(df: pd.DataFrame, tol: float = DEFAULT_TOL) -> pd.DataFrame:
    """fits.parquet(정답 열 포함) → 오차·판정 열 추가."""
    out = df.copy()
    for k in MODES:
        out[f"err_{k}"] = out[f"{k}_hat"] - out[k]
    err_cols = [f"err_{k}" for k in MODES]
    out["abs_err_max"] = out[err_cols].abs().max(axis=1)
    out["pe_ne_antisym"] = (out["err_lam_pe"] * out["err_lam_ne"]) < 0
    out["pe_ne_gap_true"] = (out["lam_pe"] - out["lam_ne"]).abs()
    out["pe_ne_gap_recovered"] = (out["lam_pe_hat"] - out["lam_ne_hat"]).abs()
    out["degenerate"] = out["abs_err_max"] > tol
    return out


# ---------------------------------------------------------------- F1 복원가능성

def classify_recoverability(df: pd.DataFrame, atol: float = 1e-3) -> pd.DataFrame:
    """★ F1 — 참값 α로 "원리적 복원 가능한가"를 분류한다.

    grid 기준에서 α_true = (1−LAM)/r 이고, α<1이면 재구성 창(폭 1/α > 1)이
    reference가 담고 있는 구간을 넘어선다. reference는 기준 셀이 실제로 지나간
    구간만 담으므로 그 바깥은 **정보가 없다** → 창 부족 벌점이 α를 1로 밀어올린다.

    이 벽은 box bound가 아니므로 `bound_active`가 False다. 그래서 별도 분류가 없으면
    "bound 문제 아님 → 진짜 물리"로 오판하게 된다.
    """
    out = df.copy()
    if "reference" in out.columns and (out["reference"] != "grid").any():
        # halfcell 기준은 전 범위 테이블이라 이 벽이 없다
        out["alpha_true_pe"] = np.nan
        out["alpha_true_ne"] = np.nan
        out["recoverable"] = True
        return out

    out["alpha_true_pe"] = (1.0 - out["lam_pe"]) / out["r"]
    out["alpha_true_ne"] = (1.0 - out["lam_ne"]) / out["r"]
    out["recoverable"] = (out["alpha_true_pe"] >= 1.0 - atol) & \
                         (out["alpha_true_ne"] >= 1.0 - atol)

    # 실제로 벽에 붙었는지 (fitting.py가 기록한 플래그)
    for side in ("pe", "ne"):
        col = f"alpha_wall_{side}"
        if col not in out.columns:
            out[col] = (out[f"a_{side}"] - 1.0).abs() < atol
    out["alpha_wall_any"] = out["alpha_wall_pe"] | out["alpha_wall_ne"]
    return out


# ---------------------------------------------------------------- F5 바이어스

def clean_bias(df: pd.DataFrame, group: tuple = ("objective",)) -> pd.DataFrame:
    """★ F5 — 노이즈 0·복원가능 조건의 평균 오차 = **방법 자체의 바이어스**.

    이걸 빼지 않으면 degenerate 판정이 상당 부분 방법 바이어스를 세게 된다.
    (F15 수정 전에는 이 바이어스가 ~1.6%p로 판정 기준 2%p와 맞먹었다)
    """
    m = df["noise"] == 0 if "noise" in df.columns else pd.Series(True, index=df.index)
    if "recoverable" in df.columns:
        m &= df["recoverable"]
    base = df[m]
    if base.empty:
        log.warning("clean 바이어스 기준 조건이 없음 — 보정 없이 진행")
        return pd.DataFrame()
    cols = [f"err_{k}" for k in MODES]
    return base.groupby(list(group))[cols].mean().rename(
        columns={c: f"bias_{c}" for c in cols}).reset_index()


def apply_bias_correction(df: pd.DataFrame, bias: pd.DataFrame,
                          tol: float = DEFAULT_TOL,
                          group: tuple = ("objective",)) -> pd.DataFrame:
    """바이어스를 뺀 잔차로 2차 판정 열을 추가 (원래 판정은 그대로 둔다)."""
    if bias.empty:
        out = df.copy()
        for k in MODES:
            out[f"resid_{k}"] = out[f"err_{k}"]
        out["abs_resid_max"] = out["abs_err_max"]
        out["degenerate_corrected"] = out["degenerate"]
        return out

    out = df.merge(bias, on=list(group), how="left")
    for k in MODES:
        out[f"resid_{k}"] = out[f"err_{k}"] - out[f"bias_err_{k}"].fillna(0.0)
    out["abs_resid_max"] = out[[f"resid_{k}" for k in MODES]].abs().max(axis=1)
    out["degenerate_corrected"] = out["abs_resid_max"] > tol
    return out


# ---------------------------------------------------------------- 요약

def summarize(df: pd.DataFrame, tol: float = DEFAULT_TOL) -> dict:
    """목적함수별 degeneracy 요약 + 리뷰 규칙에 따른 단서."""
    rec = df[df["recoverable"]] if "recoverable" in df.columns else df
    n_all, n_rec = len(df), len(rec)

    def _block(g: pd.DataFrame) -> dict:
        d = {
            "n": int(len(g)),
            "degenerate_frac": float(g["degenerate"].mean()),
            "mean_abs_err": float(g["abs_err_max"].mean()),
            "mean_abs_err_lam_pe": float(g["err_lam_pe"].abs().mean()),
            "mean_abs_err_lam_ne": float(g["err_lam_ne"].abs().mean()),
            "mean_abs_err_lli": float(g["err_lli"].abs().mean()),
            "pe_ne_antisym_frac": float(g["pe_ne_antisym"].mean()),
        }
        if "degenerate_corrected" in g.columns:
            d["degenerate_frac_corrected"] = float(g["degenerate_corrected"].mean())
        if "alpha_wall_any" in g.columns:
            d["alpha_wall_frac"] = float(g["alpha_wall_any"].mean())
        if "any_bound_active" in g.columns:
            d["bound_active_frac"] = float(g["any_bound_active"].mean())
        return d

    out = {
        "tolerance": tol,
        "n_rows_total": n_all,
        "n_rows_recoverable": n_rec,
        "unrecoverable_frac": float(1 - n_rec / n_all) if n_all else 0.0,
        "by_objective": {str(k): _block(g) for k, g in rec.groupby("objective")},
        "overall_recoverable": _block(rec) if n_rec else {},
    }

    # 노이즈별 (F10: dqdv 계열은 노이즈에서 피크 가중이 희석되므로 분리 보고 필수)
    if "noise" in rec.columns:
        out["by_objective_noise"] = {
            f"{o}|noise={n}": _block(g)
            for (o, n), g in rec.groupby(["objective", "noise"])
        }

    # F4: multi-start 지표는 restart 수로 조건화해야만 의미가 있다
    if "n_restarts" in rec.columns:
        out["restart_conditioned"] = {
            f"n_restarts={int(k)}": {
                "n": int(len(g)),
                "agree_frac": float((g["n_restarts_agree"] >= g["n_restarts"]).mean())
                if "n_restarts_agree" in g.columns else None,
                "median_p_spread": float(g["p_spread"].median())
                if "p_spread" in g.columns else None,
            }
            for k, g in rec.groupby("n_restarts")
        }
        out["_F4_주의"] = ("adaptive 조기 종료로 조건마다 검정력이 다르다. "
                          "restart 불일치율을 전체 평균으로 보고하지 말 것.")

    # F14: 격자 커버리지 공백
    if {"lli", "lam_pe"} <= set(df.columns):
        lo_lli = df[df["lli"] <= 0.02]
        out["coverage_gap"] = {
            "max_lam_pe_at_low_lli": float(lo_lli["lam_pe"].max()) if len(lo_lli) else None,
            "max_lam_pe_overall": float(df["lam_pe"].max()),
            "_주의": ("완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE 조건이 없다. "
                     "고LAM_PE 결론은 고LLI 동반 조건에서만 검증된 것."),
        }
    return out


# ---------------------------------------------------------------- CLI

def run_scoring(in_dir, out_dir=None, tol: float = DEFAULT_TOL,
                fits_name: str = "fits.parquet") -> dict:
    import json
    from pathlib import Path

    import yaml

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(in_dir / fits_name)
    log.info("채점 대상: %d행 (조건 %d, 목적함수 %s)", len(df),
             df["cond_id"].nunique(), sorted(df["objective"].unique()))

    df = add_error_columns(df, tol)
    df = classify_recoverability(df)
    bias = clean_bias(df)
    if not bias.empty:
        log.info("clean 바이어스 (노이즈0·복원가능 평균오차):\n%s",
                 bias.round(4).to_string(index=False))
    df = apply_bias_correction(df, bias, tol)

    path = out_dir / "degeneracy_map.parquet"
    df.to_parquet(path, index=False)

    summary = summarize(df, tol)
    (out_dir / "degeneracy_summary.yaml").write_text(
        yaml.safe_dump(summary, allow_unicode=True, sort_keys=False), encoding="utf-8")

    log.info("degeneracy 요약:\n%s", json.dumps(summary["by_objective"],
                                                ensure_ascii=False, indent=2))
    log.info("저장: %s", path)
    return summary


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(description="degeneracy 판정 (Phase 5)")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fits", default="fits.parquet", help="채점할 fits 파일명")
    ap.add_argument("--tol", type=float, default=DEFAULT_TOL)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    s = run_scoring(args.in_dir, args.out, args.tol, args.fits)
    print(json.dumps({k: v for k, v in s.items() if not k.startswith("_")},
                     ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
