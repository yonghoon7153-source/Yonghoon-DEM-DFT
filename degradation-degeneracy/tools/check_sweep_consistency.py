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


def compare_pair(sweep: pd.DataFrame, main: pd.DataFrame,
                 sweep_obj: str, main_obj: str, tol: float = 0.02) -> dict:
    """정의가 같은 두 목적함수를 공통 cond_id에서 맞대본다."""
    a = sweep[sweep["objective"] == sweep_obj]
    b = main[main["objective"] == main_obj]
    if a.empty or b.empty:
        return {"sweep_objective": sweep_obj, "main_objective": main_obj,
                "n_common": 0, "_오류": "한쪽에 해당 목적함수 행이 없다"}

    common = sorted(set(a["cond_id"]) & set(b["cond_id"]))
    a = _score(a[a["cond_id"].isin(common)], tol)
    b = _score(b[b["cond_id"].isin(common)], tol)

    # J는 같은 목적함수 값이므로 조건별로 직접 뺄 수 있다
    ja = a.set_index("cond_id")["J"]
    jb = b.set_index("cond_id")["J"].reindex(ja.index)
    ok = ja.notna() & jb.notna()
    worse = float(((ja[ok] > jb[ok] * (1 + _J_REL_TOL))).mean()) if ok.any() else float("nan")
    better = float(((jb[ok] > ja[ok] * (1 + _J_REL_TOL))).mean()) if ok.any() else float("nan")

    out = {"sweep_objective": sweep_obj, "main_objective": main_obj,
           "n_common": len(common),
           "sweep": _stats(a), "main": _stats(b),
           "sweep_J_worse_frac": worse, "sweep_J_better_frac": better}

    # 판정 — J가 계통적으로 나쁘면 optimizer 문제이지 목적함수 문제가 아니다
    d = out["sweep"].get("degenerate_frac_corrected", np.nan) \
        - out["main"].get("degenerate_frac_corrected", np.nan)
    out["degenerate_frac_corrected_diff"] = float(d)
    if np.isfinite(worse) and worse > 0.5:
        out["판정"] = ("sweep이 같은 목적함수를 **더 나쁘게** 풀었다 "
                       f"({worse:.0%}의 조건에서 J가 더 큼) — 이 sweep의 차이는 "
                       "가중치가 아니라 optimizer 설정에서 온다. 최적 w로 인용 금지.")
    elif np.isfinite(d) and abs(d) > 0.05:
        out["판정"] = ("J는 비슷한데 판정 비율이 5%p 넘게 다르다 — 표본(층화 468조건)이 "
                       "본 실행과 달라서일 수 있다. 결론 인용 전에 표본을 맞춰 볼 것.")
    else:
        out["판정"] = "일치 — sweep과 본 실행이 같은 답을 낸다."
    return out


def run_check(sweep_dir, main_dir, pairs=DEFAULT_PAIRS, tol: float = 0.02) -> dict:
    sweep = pd.read_parquet(Path(sweep_dir) / "fits.parquet")
    main = pd.read_parquet(Path(main_dir) / "fits.parquet")
    res = {"sweep_dir": str(sweep_dir), "main_dir": str(main_dir),
           "pairs": [compare_pair(sweep, main, s, m, tol) for s, m in pairs]}
    res["일치"] = all(p.get("판정", "").startswith("일치") for p in res["pairs"])
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
        if p["n_common"] == 0:
            print(f"\n{p['sweep_objective']} vs {p['main_objective']}: {p['_오류']}")
            continue
        print(f"\n■ {p['sweep_objective']}  vs  {p['main_objective']}"
              f"   (공통 {p['n_common']}조건)")
        print(f"  {'':22s} {'sweep':>12s} {'본 실행':>12s}")
        for k in ("J_median", "mean_abs_err_pp", "degenerate_frac",
                  "degenerate_frac_corrected"):
            if k in p["sweep"]:
                print(f"  {k:22s} {p['sweep'][k]:12.4f} {p['main'][k]:12.4f}")
        print(f"  sweep의 J가 더 큰 조건 비율 : {p['sweep_J_worse_frac']:.1%}")
        print(f"  sweep의 J가 더 작은 조건 비율: {p['sweep_J_better_frac']:.1%}")
        print(f"  → {p['판정']}")

    print(f"\n전체 일치: {res['일치']}")
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=2),
                                encoding="utf-8")
        print(f"저장: {a.json}")


if __name__ == "__main__":
    main()
