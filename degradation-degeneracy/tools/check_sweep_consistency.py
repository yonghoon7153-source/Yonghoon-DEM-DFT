"""check_sweep_consistency.py — sweep과 본 실행이 같은 답을 내는지 확인.

가중치 sweep의 두 끝점은 본 실행의 목적함수와 **정의가 완전히 같다**.

    wdqdv_0.00 = {w_pocv 1, w_dvdq 1, w_dqdv 0} = pocv_dvdq        (33p 기존)
    wdqdv_1.00 = {w_pocv 1, w_dvdq 1, w_dqdv 1} = pocv_dvdq_dqdv   (34p 개선)

따라서 같은 cond_id에서 두 실행의 결과는 **일치해야 한다.** 어긋나면 그 차이는
목적함수가 아니라 optimizer 설정(restart 수, warm start, 조기 종료)에서 온 것이고,
그 상태의 sweep으로 "최적 가중치"를 고르면 **가중치가 아니라 optimizer 난이도를
고르게 된다.**

J는 같은 목적함수·같은 데이터의 값이므로 직접 비교할 수 있다. 낮은 쪽이 더 잘
푼 것이다 — 채점(degeneracy)을 거치지 않고도 optimizer 실패를 가려낼 수 있는
가장 깨끗한 지표라 이걸 먼저 본다.

사용:
    python -m tools.check_sweep_consistency --sweep results/grid_fine_v2/wsweep \
        --main results/grid_fine_v2
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.scoring import (add_error_columns, apply_bias_correction,
                         classify_recoverability, clean_bias)

log = logging.getLogger(__name__)

# sweep 목적함수 → 본 실행에서 정의가 동일한 목적함수
DEFAULT_PAIRS = (("wdqdv_0.00", "pocv_dvdq"),
                 ("wdqdv_1.00", "pocv_dvdq_dqdv"))

_J_REL_TOL = 0.01     # J가 1% 넘게 크면 "더 나쁘게 풀었다"로 센다


def _score(df: pd.DataFrame, tol: float) -> pd.DataFrame:
    """본 실행·sweep과 동일한 채점 파이프라인 (F1 → F5)."""
    s = classify_recoverability(add_error_columns(df, tol))
    return apply_bias_correction(s, clean_bias(s), tol)


def _stats(df: pd.DataFrame) -> dict:
    rec = df[df["recoverable"]] if "recoverable" in df.columns else df
    out = {"n": int(len(df)), "n_recoverable": int(len(rec)),
           "J_median": float(df["J"].median()),
           "mean_abs_err_pp": float(rec["abs_err_max"].mean() * 100)
           if len(rec) else float("nan"),
           "degenerate_frac": float(rec["degenerate"].mean()) if len(rec) else float("nan")}
    if "degenerate_corrected" in rec.columns and len(rec):
        out["degenerate_frac_corrected"] = float(rec["degenerate_corrected"].mean())
    return out


#: ★ 12차 발견 3 — 조건별 **수치 동일성** 허용오차. 두 끝점은 같은 곡선·같은
#: 목적함수·같은 seed·restart 구조를 쓰므로 통계적 유사가 아니라 같은 해가
#: 나와야 한다. 부동소수 재계산 오차만 허용한다.
_ATOL, _RTOL = 1e-9, 1e-6
#: 조건별로 대조하는 열 — 해(parameter)와 열화모드 추정치 전부
_EXACT_COLS = ("J", "a_pe", "b_pe", "a_ne", "b_ne",
               "lli_hat", "lam_pe_hat", "lam_ne_hat")


def _max_dev(a: pd.DataFrame, b: pd.DataFrame, col: str) -> dict:
    """조건별 |a-b| 의 최대·분위수와 대칭 tolerance 위반 수."""
    if col not in a.columns or col not in b.columns:
        return {"열없음": True}
    x = a.set_index("cond_id")[col].astype(float)
    y = b.set_index("cond_id")[col].astype(float).reindex(x.index)
    ok = x.notna() & y.notna()
    if not ok.any():
        return {"n": 0, "max_abs": float("nan"), "n_violate": 0}
    dev = (x[ok] - y[ok]).abs()
    tol = _ATOL + _RTOL * pd.concat([x[ok].abs(), y[ok].abs()], axis=1).max(axis=1)
    return {"n": int(ok.sum()), "max_abs": float(dev.max()),
            "p99_abs": float(dev.quantile(0.99)),
            "n_violate": int((dev > tol).sum()),
            "worst_cond": str(dev.idxmax()) if len(dev) else None}


def compare_pair(sweep: pd.DataFrame, main: pd.DataFrame,
                 sweep_obj: str, main_obj: str, tol: float = 0.02,
                 expected_conditions: int | None = None) -> dict:
    """정의가 같은 두 목적함수를 **조건별 수치**로 맞대본다 (12차 발견 3).

    예전에는 "J 가 더 나쁜 조건이 절반 이하" + "보정 degeneracy 차이 5%p 이하"
    면 일치로 봤다. 그러면 49% 의 조건에서 J 가 2배여도, 모든 lam_pe_hat 이
    10%p 어긋나도, 심지어 공통 조건이 0건이어도 "일치" 였다 (리뷰 실측).
    두 끝점은 같은 곡선·목적함수·seed·restart 구조를 쓰므로 **같은 해**가
    나와야 한다.
    """
    a = sweep[sweep["objective"] == sweep_obj]
    b = main[main["objective"] == main_obj]
    if a.empty or b.empty:
        return {"sweep_objective": sweep_obj, "main_objective": main_obj,
                "n_common": 0, "일치": False,
                "_오류": "한쪽에 해당 목적함수 행이 없다",
                "판정": "불일치 — 비교할 행이 없다"}

    sweep_ids, main_ids = set(a["cond_id"]), set(b["cond_id"])
    common = sorted(sweep_ids & main_ids)
    missing_in_main = sorted(sweep_ids - main_ids)
    out = {"sweep_objective": sweep_obj, "main_objective": main_obj,
           "n_sweep": len(sweep_ids), "n_main": len(main_ids),
           "n_common": len(common),
           "n_sweep_missing_in_main": len(missing_in_main),
           "missing_ids_예시": missing_in_main[:5],
           "expected_conditions": expected_conditions}
    reasons = []
    if not common:
        reasons.append("공통 조건 0건")
    if missing_in_main:
        reasons.append(f"sweep 조건 {len(missing_in_main)}건이 본 실행에 없다")
    if expected_conditions is not None and len(sweep_ids) != expected_conditions:
        reasons.append(f"sweep 조건 수 {len(sweep_ids)} ≠ 서명된 "
                       f"{expected_conditions}")

    if common:
        a = _score(a[a["cond_id"].isin(common)], tol)
        b = _score(b[b["cond_id"].isin(common)], tol)
        dev = {c: _max_dev(a, b, c) for c in _EXACT_COLS}
        out["조건별_차이"] = dev
        bad = [c for c, v in dev.items()
               if v.get("열없음") or v.get("n_violate", 1) > 0]
        if bad:
            reasons.append(f"조건별 수치가 다른 열: {bad}")
        # 설명 통계 (판정 기준 아님 — 12차 발견 3)
        out["_설명통계"] = {"sweep": _stats(a), "main": _stats(b)}

    out["일치"] = not reasons
    out["판정"] = ("일치 — 조건 집합과 조건별 해(J·parameter·모드)가 같다."
                   if not reasons else
                   "불일치 — " + "; ".join(reasons) +
                   ". 이 sweep 의 최적 w 를 인용하지 말 것.")
    return out


def run_check(sweep_dir, main_dir, pairs=DEFAULT_PAIRS, tol: float = 0.02) -> dict:
    import yaml

    sweep = pd.read_parquet(Path(sweep_dir) / "fits.parquet")
    main = pd.read_parquet(Path(main_dir) / "fits.parquet")
    # ★ 12차 발견 3 — 서명된 sweep 조건 수를 기준으로 coverage 를 본다
    expected = None
    mp = Path(sweep_dir) / "manifest.yaml"
    if mp.is_file():
        expected = ((yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
                     ).get("run_spec") or {}).get("n_conditions")
    res = {"sweep_dir": str(sweep_dir), "main_dir": str(main_dir),
           "tol_정책": {"atol": _ATOL, "rtol": _RTOL, "열": list(_EXACT_COLS)},
           "pairs": [compare_pair(sweep, main, s, m, tol, expected)
                     for s, m in pairs]}
    res["일치"] = bool(res["pairs"]) and all(p.get("일치") for p in res["pairs"])
    return res


def main() -> None:
    import json

    ap = argparse.ArgumentParser(description="sweep과 본 실행의 일치 확인")
    ap.add_argument("--sweep", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--json", default=None, help="결과를 이 경로에 저장")
    a = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    res = run_check(a.sweep, a.main, tol=a.tol)

    for p in res["pairs"]:
        print(f"\n■ {p['sweep_objective']}  vs  {p['main_objective']}"
              f"   (sweep {p.get('n_sweep', 0)} / 본 실행 {p.get('n_main', 0)} / "
              f"공통 {p['n_common']}조건)")
        if p.get("_오류"):
            print(f"  {p['_오류']}")
        for c, v in (p.get("조건별_차이") or {}).items():
            if v.get("열없음"):
                print(f"  {c:12s} 열이 없다")
            else:
                print(f"  {c:12s} max|Δ| {v['max_abs']:.3e}  "
                      f"위반 {v['n_violate']}/{v['n']}"
                      + (f"  (worst {v['worst_cond']})" if v["n_violate"] else ""))
        s = (p.get("_설명통계") or {}).get("sweep")
        m = (p.get("_설명통계") or {}).get("main")
        if s and m:
            print(f"  {'(설명 통계)':22s} {'sweep':>12s} {'본 실행':>12s}")
            for k in ("J_median", "mean_abs_err_pp", "degenerate_frac",
                      "degenerate_frac_corrected"):
                if k in s:
                    print(f"  {k:22s} {s[k]:12.4f} {m[k]:12.4f}")
        print(f"  → {p['판정']}")

    print(f"\n전체 일치: {res['일치']}")
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=2),
                                encoding="utf-8")
        print(f"저장: {a.json}")
    # ★ 11차 발견 5 — 불일치는 **nonzero** 로 끝나야 한다. 예전에는 판정을
    #   출력만 하고 0으로 끝나서, 이 도구를 파이프라인에 넣어도 아무것도 막지
    #   못했다 (보고서는 "이 도구가 확인한다"고 써 왔다).
    if not res["일치"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
