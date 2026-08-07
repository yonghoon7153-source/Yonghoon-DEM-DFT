"""compare_cases.py — 기준 곡선 두 가지를 **같은 조건에서** 비교 (Phase 6).

    Case 1  전 범위 half-cell OCV (21p 논문 방식)   --reference halfcell
    Case 2  격자의 무열화 조건 곡선 (유도식 방식)     --reference grid

왜 별도 도구인가
────────────────
그냥 두 실행의 요약을 나란히 놓으면 **행 수가 다르다.** grid 기준은 참값
α=(1−LAM)/r < 1 인 조건을 복원불가로 빼기 때문에 3,069 → 1,476이 된다.
그 상태로 비교하면 "halfcell이 좋다"가 난이도 차이인지 기준 효과인지 모른다.

★ 그리고 halfcell의 "복원불가 0%"는 측정이 아니다.
  src/scoring.py 가 reference != "grid" 이면 recoverable=True 로 **고정**한다
  (전 범위 테이블이라 창이 부족할 일이 없다는 물리적 근거). 근거 있는 가정이지만
  실측이 아니므로 "0%"를 결과로 인용하면 안 된다.

그래서 여기서는:
  1. 두 실행의 **공통 cond_id**만 남기고
  2. grid 기준에서 **복원가능**으로 분류된 조건으로 한 번 더 좁혀서
  3. 같은 모집단에서 목적함수별로 비교한다.

이러면 남는 차이는 기준 곡선 효과뿐이다.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# run.sh 없이 직접 실행해도 src/tools를 찾도록
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd  # noqa: E402
import yaml  # noqa: E402

log = logging.getLogger(__name__)

CASE_LABEL = {"grid": "Case 2 (격자 무열화 곡선)", "halfcell": "Case 1 (전 범위 half-cell)"}


def _scored(fits_path: Path, tol: float) -> pd.DataFrame:
    from src.scoring import (add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias)

    df = classify_recoverability(add_error_columns(pd.read_parquet(fits_path), tol))
    return apply_bias_correction(df, clean_bias(df), tol)


def compare(grid_fits: Path, halfcell_fits: Path, tol: float = 0.02) -> dict:
    """★ F52 — 두 artifact **모두** provenance를 검증하고 digest를 봉인한다.

    이 표는 두 실행의 비교인데, `make_results.py` 의 배너는 주 입력 디렉터리
    하나만 검사한다. 그래서 검증된 grid + **검증 안 된 half-cell** 로 만든
    비교표가 녹색 배너 아래 실릴 수 있었다. 여기서 양쪽을 직접 확인하고
    결과 yaml 에 박아, 읽는 쪽이 전이적 입력까지 추적할 수 있게 한다.
    """
    from src.io import file_digest, validate_provenance

    g = _scored(grid_fits, tol)
    h = _scored(halfcell_fits, tol)
    prov = {}
    for tag, fp in (("grid", Path(grid_fits)), ("halfcell", Path(halfcell_fits))):
        run_dir = fp.parent if fp.is_file() else fp
        v = validate_provenance(run_dir)
        prov[tag] = {"run_dir": str(run_dir), "ok": v["ok"], "fail": v["fail"],
                     "fits_sha256": file_digest(
                         fp if fp.is_file() else run_dir / "fits.parquet"),
                     "manifest_sha256": file_digest(run_dir / "manifest.yaml")}

    # ① 공통 조건 ② grid 기준에서 복원가능한 조건만
    common = set(g["cond_id"]) & set(h["cond_id"])
    keep = set(g.loc[g["recoverable"], "cond_id"]) & common
    gg = g[g["cond_id"].isin(keep)]
    hh = h[h["cond_id"].isin(keep)]

    def block(df: pd.DataFrame) -> dict:
        return {o: {
            "n": int(len(x)),
            "degenerate_frac": float(x["degenerate"].mean()),
            "degenerate_frac_corrected": float(x["degenerate_corrected"].mean()),
            "mean_abs_err": float(x["abs_err_max"].mean()),
            "pe_ne_antisym_frac": float(x["pe_ne_antisym"].mean()),
        } for o, x in df.groupby("objective")}

    provenance_ok = all(v["ok"] for v in prov.values())
    return {
        "provenance": prov,
        "provenance_ok": provenance_ok,
        "_주의_provenance": (
            "두 artifact 모두 provenance 검증을 통과했다."
            if provenance_ok else
            "⚠ 인용 금지 — 비교에 쓰인 artifact 중 provenance 검증에 실패한 것이 "
            f"있다: { {k: v['fail'] for k, v in prov.items() if not v['ok']} }"),
        "n_conditions_total": int(g["cond_id"].nunique()),
        "n_conditions_common": len(common),
        "n_conditions_compared": len(keep),
        "_모집단": ("두 실행의 공통 조건 중, grid 기준에서 복원가능으로 분류된 것만. "
                  "행 수를 맞춰야 기준 효과와 난이도 차이가 섞이지 않는다."),
        "_주의_복원불가": ("halfcell의 복원불가 0%는 측정이 아니라 scoring.py가 "
                        "reference != 'grid' 일 때 recoverable=True로 고정한 값이다. "
                        "결과로 인용하지 말 것."),
        "grid": block(gg),
        "halfcell": block(hh),
    }


def to_markdown(res: dict) -> str:
    from tools.compare_objectives import OBJ_LABEL, OBJ_ORDER

    objs = [o for o in OBJ_ORDER if o in res["grid"] or o in res["halfcell"]]
    lines = [
        f"공통 {res['n_conditions_compared']}조건 "
        f"(전체 {res['n_conditions_total']} 중, grid 기준 복원가능군으로 맞춤)",
        "",
        "| objective | degeneracy | (바이어스 보정) | 평균 \\|err\\| |",
        "|---|---|---|---|",
    ]
    for o in objs:
        a, b = res["halfcell"].get(o), res["grid"].get(o)
        if not a or not b:
            continue
        lines.append(
            f"| {OBJ_LABEL.get(o, o)} | "
            f"{100 * a['degenerate_frac']:.0f}% / {100 * b['degenerate_frac']:.0f}% | "
            f"{100 * a['degenerate_frac_corrected']:.0f}% / "
            f"{100 * b['degenerate_frac_corrected']:.0f}% | "
            f"{100 * a['mean_abs_err']:.1f}%p / {100 * b['mean_abs_err']:.1f}%p |")
    lines += ["", "*(각 칸 = **Case 1 halfcell** / Case 2 grid)*"]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="기준 곡선 두 가지 비교 (Phase 6)")
    ap.add_argument("--grid", required=True, help="grid 기준 결과 디렉터리 또는 fits.parquet")
    ap.add_argument("--halfcell", required=True, help="halfcell 기준 쪽")
    ap.add_argument("--out", default=None, help="yaml 저장 위치 (기본 --grid 아래)")
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    def fits(p):
        p = Path(p)
        return p if p.suffix == ".parquet" else p / "fits.parquet"

    res = compare(fits(args.grid), fits(args.halfcell), args.tol)
    out = Path(args.out) if args.out else fits(args.grid).parent / "case_comparison.yaml"
    out.write_text(yaml.safe_dump(res, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")
    print(to_markdown(res))
    print(f"\n저장: {out}")


if __name__ == "__main__":
    main()
