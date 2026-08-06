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


# ---------------------------------------------------------------- multi-start 진단

def multistart_diagnostics(df: pd.DataFrame, j_tol: float = 1e-3,
                           p_tol: float = 1e-2, skip_first: bool = False) -> pd.DataFrame:
    """★ restarts_json에서 **해석 가능한** multi-start 지표를 다시 만든다 (F21).

    fitting이 기록하던 두 지표는 그대로 쓰면 오독한다.

      n_restarts_agree  adaptive 조기 종료 때문에, restart를 5까지 간 조건은
                        "앞 두 번이 안 맞아서 계속 간" 조건이다. 따라서
                        `agree >= n_restarts`는 **정의상 거짓**이다 (실측 0.0).
                        측정이 아니라 동어반복이다.
      p_spread          최적 J에 근접한 해들 사이의 퍼짐이라, 값이 0이면
                        "해가 일치"가 아니라 **"최적 J에 도달한 게 하나뿐"** 이다.
                        오히려 서로 다른 국소최소가 있다는 신호에 가깝다.

    그래서 원본 (p, J) 목록에서 두 축을 분리해 다시 센다.

      n_near_J       최적 J의 j_tol 이내에 든 restart 수
      p_spread_all   **모든** restart의 최적해 대비 최대 거리
      p_spread_near  n_near_J 안에서의 최대 거리

    그리고 조건을 셋으로 나눈다 — 세 경우의 처방이 다르다.

      unique_min   n_near_J == 전체, p_spread_near 작음
                   → 해가 유일. 문제 없음
      flat_valley  n_near_J >= 2, p_spread_near 큼
                   → **같은 J에 서로 다른 해.** 이것이 degeneracy의 직접 증거다.
                     데이터가 그 조합을 구분하지 못한다는 뜻
      multimodal   n_near_J == 1, p_spread_all 큼
                   → J가 다른 국소최소가 여럿. 데이터는 구분하지만
                     최적화가 어렵다 = 초기값 문제 (F20의 dQ/dV가 이 경우)

    ★ skip_first — warm start 보정 (F21b, 필수).
      F20 이후 dQ/dV 목적함수는 restart 0에만 좋은 초기값이 들어가고 1~4는
      무작위다. 그러면 최적 J에 닿는 restart가 **정의상 하나뿐**이 되어
      항상 multimodal로 분류되고, flat_valley는 관측 자체가 불가능해진다.
      warm start를 받은 목적함수와 안 받은 목적함수를 그대로 비교하면
      "dQ/dV가 flat valley를 없앴다"는 잘못된 결론이 나온다.
      skip_first=True면 restart 0을 빼고 **무작위 restart끼리만** 비교한다.
    """
    import json as _json

    if "restarts_json" not in df.columns:
        log.warning("restarts_json 열이 없음 — multi-start 진단 생략")
        return pd.DataFrame()

    rows = []
    for _, r in df.iterrows():
        try:
            rs = _json.loads(r["restarts_json"])
        except (TypeError, ValueError):
            continue
        if not rs:
            continue
        ps = np.array([p for p, _ in rs], float)
        js = np.array([j for _, j in rs], float)
        ok = np.isfinite(js)
        if not ok.any():
            continue
        ps, js = ps[ok], js[ok]
        if skip_first:
            ps, js = ps[1:], js[1:]      # restart 0 = warm start 지점
            if len(js) < 2:
                continue
        i_best = int(np.argmin(js))
        p_best, j_best = ps[i_best], js[i_best]

        near = np.abs(js - j_best) <= j_tol * max(1.0, abs(j_best))
        d_all = np.max(np.abs(ps - p_best), axis=1)
        spread_all = float(d_all.max())
        spread_near = float(d_all[near].max())
        n_near = int(near.sum())

        if n_near >= 2 and spread_near > p_tol:
            kind = "flat_valley"
        elif n_near == 1 and spread_all > p_tol:
            kind = "multimodal"
        else:
            kind = "unique_min"

        rows.append({
            "cond_id": r["cond_id"], "objective": r["objective"],
            **{k: r[k] for k in ("lli", "lam_pe", "lam_ne", "noise")
               if k in df.columns},
            "n_restarts_total": int(len(js)), "n_near_J": n_near,
            "p_spread_all": spread_all, "p_spread_near": spread_near,
            "J_best": float(j_best), "J_worst": float(js.max()),
            "multistart_kind": kind,
        })
    return pd.DataFrame(rows)


def multistart_summary(ms: pd.DataFrame) -> dict:
    """목적함수별 요약. flat_valley 비율이 degeneracy의 직접 증거다."""
    if ms.empty:
        return {}
    out = {}
    for o, g in ms.groupby("objective"):
        counts = g["multistart_kind"].value_counts(normalize=True)
        out[str(o)] = {
            "n": int(len(g)),
            # ★ 같은 J에 서로 다른 해 = 데이터가 구분 못 함
            "flat_valley_frac": float(counts.get("flat_valley", 0.0)),
            # J가 다른 국소최소 여럿 = 최적화 난이도 (초기값으로 해결 가능)
            "multimodal_frac": float(counts.get("multimodal", 0.0)),
            "unique_min_frac": float(counts.get("unique_min", 0.0)),
            "median_p_spread_all": float(g["p_spread_all"].median()),
            "median_n_restarts": float(g["n_restarts_total"].median()),
        }
    out["_해석"] = ("flat_valley = degeneracy의 직접 증거 (같은 J, 다른 해). "
                   "multimodal = 최적화 난이도이지 degeneracy가 아니다 "
                   "— 초기값을 주면 사라진다 (F20).")
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

    # F4/F21: multi-start 지표는 restart 수로 조건화해야만 의미가 있고,
    # agree_frac은 조기 종료 때문에 n_restarts>2에서 정의상 0이 된다 (동어반복).
    # 해석 가능한 지표는 multistart_diagnostics()가 restarts_json에서 다시 만든다.
    if "n_restarts" in rec.columns:
        out["restart_conditioned"] = {
            f"n_restarts={int(k)}": {
                "n": int(len(g)),
                "agree_frac": float((g["n_restarts_agree"] >= g["n_restarts"]).mean())
                if "n_restarts_agree" in g.columns else None,
                "median_p_spread_nearJ": float(g["p_spread"].median())
                if "p_spread" in g.columns else None,
            }
            for k, g in rec.groupby("n_restarts")
        }
        out["_F4_주의"] = (
            "이 블록의 두 지표는 그대로 인용하지 말 것. "
            "(1) agree_frac: adaptive 조기 종료로 n_restarts>2인 조건은 "
            "'앞 두 번이 안 맞아서 계속 간' 조건이라 정의상 0이 된다 — 측정이 아니다. "
            "(2) p_spread_nearJ=0은 '해가 일치'가 아니라 '최적 J에 도달한 restart가 "
            "하나뿐'이라는 뜻이다. "
            "해석은 아래 multistart 블록(flat_valley / multimodal)을 볼 것.")

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

    # F21: restarts_json에서 해석 가능한 multi-start 지표를 다시 만든다.
    # (재계산 없이 저장된 원본 (p, J)만으로 가능)
    rec_df = df[df["recoverable"]] if "recoverable" in df else df
    ms = multistart_diagnostics(rec_df)
    if not ms.empty:
        ms.to_parquet(out_dir / "multistart.parquet", index=False)
        summary["multistart"] = multistart_summary(ms)
        # ★ F21b: warm start를 받은 목적함수는 restart 0만 좋은 초기값이라
        #   최적 J에 닿는 게 하나뿐이 된다 → 항상 multimodal로 찍힌다.
        #   목적함수 간 **공정 비교**는 무작위 restart끼리만 해야 한다.
        ms_r = multistart_diagnostics(rec_df, skip_first=True)
        if not ms_r.empty:
            ms_r.to_parquet(out_dir / "multistart_random_only.parquet", index=False)
            summary["multistart_random_only"] = multistart_summary(ms_r)
            summary["multistart_random_only"]["_주의"] = (
                "★ 목적함수 간 비교는 이 블록을 쓸 것. 위 multistart 블록은 "
                "warm start 지점(restart 0)을 포함하므로, warm start를 받은 "
                "목적함수(w_dqdv≠0)가 인위적으로 multimodal 쪽으로 쏠린다.")
        log.info("multi-start 진단: %s",
                 {k: v for k, v in summary["multistart"].items()
                  if not k.startswith("_")})
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
