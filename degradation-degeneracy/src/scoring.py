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

import itertools
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
    # ★ 행별로 판정한다 (F27). 예전에는 `(reference != "grid").any()`로 프레임
    #   전체를 봐서, grid 행과 halfcell 행을 붙여 넘기면 halfcell이 한 줄만
    #   있어도 grid 행까지 전부 복원가능으로 바뀌었다. 조용한 모집단 변경이라
    #   비교표의 분모가 소리 없이 늘어난다.
    is_grid = (out["reference"] == "grid") if "reference" in out.columns \
        else pd.Series(True, index=out.index)

    out["alpha_true_pe"] = np.where(is_grid, (1.0 - out["lam_pe"]) / out["r"], np.nan)
    out["alpha_true_ne"] = np.where(is_grid, (1.0 - out["lam_ne"]) / out["r"], np.nan)
    # halfcell 기준은 전 범위 테이블이라 이 벽이 없다 → True로 둔다.
    # ⚠ 이건 물리적 근거에 의한 **가정**이지 측정이 아니다. RESULTS.md가 이 사실을
    #   같이 싣는다. halfcell 쪽 복원불가율을 "0%로 측정됐다"고 인용하면 안 된다.
    out["recoverable"] = np.where(
        is_grid,
        (out["alpha_true_pe"] >= 1.0 - atol) & (out["alpha_true_ne"] >= 1.0 - atol),
        True)
    out["recoverable_measured"] = is_grid.to_numpy()

    # 실제로 벽에 붙었는지 (fitting.py가 기록한 플래그)
    for side in ("pe", "ne"):
        col = f"alpha_wall_{side}"
        if col not in out.columns:
            out[col] = ((out[f"a_{side}"] - 1.0).abs() < atol
                        if f"a_{side}" in out.columns
                        else pd.Series(False, index=out.index))
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

    ★ drop_warm — warm start 보정 (F21b, 필수).
      F20 이후 dQ/dV 목적함수는 restart 0에만 좋은 초기값이 들어가고 1~4는
      무작위다. 그러면 최적 J에 닿는 restart가 **정의상 하나뿐**이 되어
      항상 multimodal로 분류되고, flat_valley는 관측 자체가 불가능해진다.
      warm start를 받은 목적함수와 안 받은 목적함수를 그대로 비교하면
      "dQ/dV가 flat valley를 없앴다"는 잘못된 결론이 나온다.

    ★★ 옛 형식은 이 보정을 할 수 없다 (F25).
      `restarts_json`을 **J 오름차순으로 정렬해서** 저장하므로, 위치는 restart
      순서가 아니다. 그런데 예전 구현은 "첫 항목 = warm start"로 보고 그걸
      버렸다 — 실제로는 **best restart를 버리고 있었다.** 지금은 restart마다
      `{"i", "warm"}`을 같이 저장해 출처로 거른다. 출처가 없는 옛 산출물은
      복구가 불가능하므로 보정을 **생략하고 경고**한다 (조용히 틀린 값을 내는
      것보다 낫다).
    """
    import json as _json

    if "restarts_json" not in df.columns:
        log.warning("restarts_json 열이 없음 — multi-start 진단 생략")
        return pd.DataFrame()

    rows, n_legacy = [], 0
    for _, r in df.iterrows():
        try:
            rs = _json.loads(r["restarts_json"])
        except (TypeError, ValueError):
            continue
        if not rs:
            continue
        legacy = not isinstance(rs[0], dict) or "source" not in rs[0]
        if legacy:
            if isinstance(rs[0], dict):
                ps = np.array([d["p"] for d in rs], float)
                js = np.array([d["J"] for d in rs], float)
            else:
                ps = np.array([p for p, _ in rs], float)
                js = np.array([j for _, j in rs], float)
            source = np.array(["unknown"] * len(js), object)
        else:
            ps = np.array([d["p"] for d in rs], float)
            js = np.array([d["J"] for d in rs], float)
            source = np.array([d["source"] for d in rs], object)
            idx = np.array([int(d.get("i", -1)) for d in rs], int)
        if legacy:
            idx = np.full(len(js), -1, int)
        ok = np.isfinite(js)
        if not ok.any():
            continue
        ps, js, source, idx = ps[ok], js[ok], source[ok], idx[ok]
        n_dropped = 0
        if skip_first:
            if legacy:
                n_legacy += 1        # 출처를 모른다 → 아무것도 버리지 않는다
            else:
                # ★ F31 — "warm만 제거"로는 부족하다. restart 0은 warm이 아니어도
                #   공통 결정론적 초기값(base_init)이라 무작위가 아니다. warm을 받은
                #   목적함수만 restart 0이 빠지고 나머지는 base_init이 남으면,
                #   비교하는 restart 집합의 성격이 목적함수마다 달라진다.
                keep = source == "random"
                n_dropped = int((~keep).sum())
                ps, js, idx = ps[keep], js[keep], idx[keep]
                if len(js) < 2:
                    continue
        idx_kept = idx
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
            # F31: 실제로 몇 개를 버렸는지 기록한다. "형식이 새것이면 True"는
            # 보정이 실제로 일어났는지를 말해주지 않는다.
            "n_nonrandom_dropped": n_dropped,
            "random_only": bool(skip_first and not legacy),
            # ★ F44 — 개수만 맞추면 "같은 seed 를 비교했다"가 아니다. 최적화 예외로
            #   빠진 index 가 목적함수마다 다를 수 있으므로 **index 집합**을 남긴다.
            "restart_indices": ",".join(str(i) for i in sorted(idx_kept)),
        })
    if n_legacy:
        log.warning("multi-start: %d행이 옛 restarts 형식(출처 없음)이라 warm start "
                    "보정을 못 했습니다. 위치로 추정하면 warm이 아니라 best restart를 "
                    "버리게 되므로 보정을 생략했습니다 — 이 결과의 "
                    "multistart_random_only는 무효입니다 (F25). 재fit이 필요합니다.",
                    n_legacy)
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
                fits_name: str = "fits.parquet", allow_uncanonical: bool = False) -> dict:
    """★ F69 — 채점 대상은 **정본 fits.parquet 뿐**이다.

    예전에는 `--fits` 로 임의 parquet 을 받아 provenance 검사 없이
    `degeneracy_map.parquet` 을 만들었다. 그 map 에서 `objective_comparison.yaml`
    이 나오고 보고서가 그걸 그대로 읽으므로, **파일 인자 하나로 degeneracy 를
    94% → 0% 로 바꾸고도 인용 금지 배너가 뜨지 않았다.** (리뷰가 실제로 재현)

    `allow_uncanonical=True` 는 진단 전용이다. 이때는 산출물에 무효 표식을 박아
    하류가 인용하지 못하게 한다.
    """
    import json
    from pathlib import Path

    import yaml

    from src.io import fits_seal, validate_provenance

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    fits_path = in_dir / fits_name
    canonical = fits_path.resolve() == (in_dir / "fits.parquet").resolve()
    if not canonical and not allow_uncanonical:
        raise RuntimeError(
            f"채점 대상이 정본이 아닙니다: {fits_path}\n"
            f"  정본은 {in_dir / 'fits.parquet'} 하나뿐입니다. 임의 parquet 을 채점하면 "
            f"그 숫자가 비교표와 보고서까지 그대로 흘러가고, provenance 배너는 "
            f"정본만 보므로 검출되지 않습니다 (F69).\n"
            f"  진단 목적이면 allow_uncanonical=True / --allow-uncanonical 을 쓰세요 "
            f"(산출물에 무효 표식이 박힙니다).")

    # ★ F69 — 정본이라도 **봉인과 일치하는지** 본다. 채점은 fits 를 그대로 읽으므로,
    #   fitting 이후 파일이 바뀌었다면 채점 결과부터 이미 다른 숫자다.
    seal_state = "정상"
    if canonical:
        v = validate_provenance(in_dir, fits_path=fits_path)
        bad = [k for k in ("출력봉인_재계산", "조건집합_서명일치", "출력_완전성")
               if k in v["fail"]]
        if bad:
            seal_state = f"봉인 불일치: {bad}"
            log.warning("⚠ 채점 대상이 봉인과 어긋납니다 (%s) — 결과를 인용하지 마세요", bad)
        elif "출력봉인_기록" in v["fail"]:
            seal_state = "봉인 기록 없음 (F68 이전 산출물)"
            log.warning("⚠ fits_seal 기록이 없는 옛 산출물입니다 — 결과를 인용하지 마세요")
    else:
        seal_state = f"정본 아님 (진단 전용): {fits_name}"

    df = pd.read_parquet(fits_path)
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
    # ★ F69 — 채점 산출물이 **무엇을 채점했는지** 스스로 밝힌다. 하류(비교표·보고서)가
    #   이 표식을 보고 인용 여부를 판단할 수 있어야 한다.
    summary["_채점원본"] = {
        "fits": str(fits_path), "canonical": bool(canonical),
        "fits_sha256": fits_seal(fits_path)["file_sha256"],
        "봉인상태": seal_state,
        "인용가능": bool(canonical and seal_state == "정상"),
    }

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
            # ★ F25/F31: 옛 산출물은 restart 출처가 없어 보정 자체가 불가능하다.
            #   그 사실을 요약에 박아, 읽는 쪽이 무효인 줄 모르고 인용하지 못하게 한다.
            ok_random = bool(ms_r["random_only"].all()) if "random_only" in ms_r else False
            summary["multistart_random_only"]["random_only_적용"] = ok_random
            if "n_nonrandom_dropped" in ms_r:
                summary["multistart_random_only"]["평균_제외_restart수"] = \
                    float(ms_r["n_nonrandom_dropped"].mean())
            # ★ F40 — 평균 restart 수가 같아도 **조건 집합이 다르면** 비교가
            #   성립하지 않는다. adaptive 조기 종료 때문에 탈락하는 cond_id가
            #   목적함수마다 다르므로, 평균만 보면 완전히 다른 모집단을
            #   "비교가능"으로 판정한다. 공통 cond_id + 같은 restart 수인
            #   **paired subset**을 만들어 그것으로만 비교한다.
            if ok_random and {"objective", "cond_id"} <= set(ms_r.columns):
                blk = summary["multistart_random_only"]
                sets = {o: set(g["cond_id"]) for o, g in ms_r.groupby("objective")}
                blk["n_conditions_per_objective"] = {o: len(v) for o, v in sets.items()}
                # ★ F44 — restart **index 집합**까지 같아야 "같은 seed를 비교했다"가
                #   된다. 개수만 맞추면 33p가 {1,2}, 34p가 {1,3}이어도 통과한다.
                # ★ F44b — 전역 교집합은 결론 2가 요구하는 33p↔34p 비교를 과도하게
                #   줄인다. 제3·제4 목적함수에서만 빠진 조건도 함께 제외되기 때문이다.
                #   **목적함수 쌍마다** 따로 낸다.
                key = ms_r.set_index(["objective", "cond_id"])["restart_indices"]
                objs = sorted(sets)
                pairs = {}
                for a, b in itertools.combinations(objs, 2):
                    common = sets[a] & sets[b]
                    pr = {c for c in common if key[(a, c)] == key[(b, c)]}
                    ent = {"n_common": len(common), "n_paired": len(pr),
                           "비교가능": bool(len(pr) >= 30)}
                    if pr:
                        sub = ms_r[ms_r["cond_id"].isin(pr)
                                   & ms_r["objective"].isin([a, b])]
                        ent["summary"] = multistart_summary(sub)
                    pairs[f"{a}__vs__{b}"] = ent
                blk["pairwise"] = pairs
                # 전역(모든 목적함수 동시) — 참고용
                common_all = set.intersection(*sets.values()) if sets else set()
                paired = {c for c in common_all
                          if len({key[(o, c)] for o in objs}) == 1}
                blk["n_common_conditions"] = len(common_all)
                blk["n_paired_conditions"] = len(paired)
                blk["제외율_목적함수별"] = {
                    o: round(1 - len(paired) / len(v), 4) if v else None
                    for o, v in sets.items()}
                blk["비교가능"] = bool(len(paired) >= 30)
                blk["_주의_전역교집합"] = (
                    "`n_paired_conditions`·`비교가능`은 **모든 목적함수 동시** "
                    "교집합이라 33p↔34p 비교에는 과도하게 엄격하다. 두 목적함수를 "
                    "비교할 때는 `pairwise` 블록의 해당 항목을 쓸 것 (F44b).")
                # ★ F41 — paired subset은 **무작위 표본이 아니다.** adaptive 조기
                #   종료로 restart 2에서 멈춘 조건은 무작위 restart가 1개뿐이라
                #   탈락하므로, 남는 것은 **네 목적함수 모두가 끝까지 간 조건**
                #   = 모두에게 어려웠던 조건이다. 결과(최적화 난이도)로 선택된
                #   집합이라 격자 전체로 일반화할 수 없다.
                blk["_선택편향"] = (
                    f"paired subset은 무작위 표본이 아니다 — adaptive 조기 종료를 "
                    f"겪지 않은(=모든 목적함수가 끝까지 간) 조건만 남는다. "
                    f"목적함수별 제외율이 "
                    f"{min(blk['제외율_목적함수별'].values()):.0%}~"
                    f"{max(blk['제외율_목적함수별'].values()):.0%}로 크게 다르다는 것이 "
                    f"그 증거다. 여기서 잰 비율을 격자 전체로 일반화하지 말 것.")
                if paired:
                    ms_p = ms_r[ms_r["cond_id"].isin(paired)]
                    ms_p.to_parquet(out_dir / "multistart_paired.parquet", index=False)
                    blk["paired"] = multistart_summary(ms_p)
            summary["multistart_random_only"]["_주의"] = (
                "★ 목적함수 간 비교는 이 블록을 쓸 것 — source == 'random'인 restart만 "
                "남긴다. 위 multistart 블록은 warm start 지점과 공통 결정론적 초기값을 "
                "포함하므로, warm start를 받은 목적함수(w_dqdv≠0)가 인위적으로 "
                "multimodal 쪽으로 쏠린다. 단 `비교가능`이 false면 목적함수마다 남은 "
                "무작위 restart 수가 달라(adaptive 조기 종료) 검정력이 다르므로 "
                "그대로 비교하지 말 것 — `paired` 블록(공통 cond_id + 동일 restart 수)만 "
                "목적함수 간 비교에 쓸 수 있다."
                if ok_random else
                "⚠ 무효 — 이 fits.parquet은 restart 출처를 저장하지 않은 옛 형식이라 "
                "보정을 하지 못했습니다. restarts_json이 J 오름차순이라 위치로 "
                "추정하면 warm이 아니라 best restart를 버립니다. 이 블록을 인용하지 "
                "마세요 — 출처를 저장하는 현재 코드로 재fit해야 복구됩니다 (F25/F31).")
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
    ap.add_argument("--allow-uncanonical", action="store_true",
                    help="정본이 아닌 parquet 채점을 허용한다 (진단 전용 — "
                         "산출물에 무효 표식이 박히고 보고서가 인용을 막는다)")
    ap.add_argument("--tol", type=float, default=DEFAULT_TOL)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    s = run_scoring(args.in_dir, args.out, args.tol, args.fits,
                    allow_uncanonical=args.allow_uncanonical)
    print(json.dumps({k: v for k, v in s.items() if not k.startswith("_")},
                     ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
