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


def compare(grid_fits: Path, halfcell_fits: Path, tol: float = 0.02,
            repo_root=None) -> dict:
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
    specs = {}
    for tag, fp in (("grid", Path(grid_fits)), ("halfcell", Path(halfcell_fits))):
        run_dir = fp.parent if fp.is_file() else fp
        scored_file = fp if fp.is_file() else run_dir / "fits.parquet"
        # F59: **실제로 채점한 파일**을 검증 대상으로 넘긴다
        # ★ 16차 발견 1 — 격리 root 를 관통시킨다
        v = validate_provenance(run_dir, repo_root=repo_root,
                                fits_path=scored_file)
        mp = run_dir / "manifest.yaml"
        man = (yaml.safe_load(mp.read_text(encoding="utf-8")) or {}) if mp.exists() else {}
        spec = man.get("run_spec") or {}
        specs[tag] = spec
        # ★ F69 — tag 는 **인자 순서**로 붙는다. 실제 역할을 확인하지 않으면
        #   grid artifact 두 개를 넣어도 "grid vs halfcell" 표가 나온다
        #   (리뷰 실측: reference = grid/grid 인데 provenance_ok=True, 배너 없음).
        #   이 비교의 결론 3 전체가 "기준 곡선이 다르다"는 전제 위에 있다.
        actual = str(spec.get("reference") or man.get("reference") or "?")
        role_ok = actual == tag
        prov[tag] = {"run_dir": str(run_dir), "scored_file": str(scored_file),
                     "ok": bool(v["ok"] and role_ok),
                     "fail": list(v["fail"]) + ([] if role_ok else ["reference_역할불일치"]),
                     "reference_실제": actual, "reference_기대": tag,
                     "fits_sha256": file_digest(scored_file),
                     "manifest_sha256": file_digest(run_dir / "manifest.yaml")}

    # ★ F69 — 같은 실험이어야 비교가 성립한다. 서로 다른 curves·목적함수 정의·
    #   조건 집합에서 나온 두 표를 나란히 놓으면 "기준 곡선 효과"가 아니라
    #   그냥 다른 두 실험이다.
    # ★ F78/8차 발견 7 — reference 와 **명시적으로 허용한** 좌표계 필드만 다를
    #   수 있다. 예전에는 curves·objectives·v_col·조건집합만 봐서, optimizer
    #   정책·warm start·순서·base config·inventory·환경이 달라도 "남는 차이는
    #   기준 곡선뿐"이라고 판정했다.
    MUST_MATCH = (("curves_sha", "입력 곡선"),
                  ("producer_sha", "곡선 producer"),
                  ("objectives", "목적함수 정의"),
                  ("objective_order", "목적함수 순서"),
                  ("v_col", "타깃 열"),
                  ("warm_start", "warm start"),
                  ("optimizer", "optimizer 정책"),
                  ("base_config_sha", "base config"),
                  ("inventory", "inventory 상수"),
                  # ★ F84/9차 발견 5 — objective **전처리** 설정. dQ/dV window 를
                  #   7 과 11 로 달리한 두 fit 이 각각 validator 를 통과하고 case
                  #   비교도 통과했다. 그러면 결론 3 의 차이가 기준 곡선이 아니라
                  #   전처리 차이일 수 있다.
                  ("obj_cfg", "objective 전처리 설정"),
                  ("source_digest", "코드 identity"),
                  ("env", "실행 환경"),
                  ("condition_ids_sha256", "조건 집합"))
    #: reference 에 따라 달라야 정상인 것 — 단 그 사실이 인과 문구를 제한한다
    ALLOWED_DIFF = ("bounds_preset", "bounds", "p_ini",
                    "halfcell_sha", "halfcell_meta_sha", "halfcell_cache",
                    "halfcell_recipe", "reference")
    shared, mismatch = {}, []
    for key, label in MUST_MATCH:
        a, b = specs["grid"].get(key), specs["halfcell"].get(key)
        shared[key] = {"grid": a, "halfcell": b, "일치": a == b}
        if a != b:
            mismatch.append(label)
    allowed_diff_seen = sorted(
        k for k in ALLOWED_DIFF
        if specs["grid"].get(k) != specs["halfcell"].get(k))

    # ① 공통 조건 ② grid 기준에서 복원가능한 조건만
    common = set(g["cond_id"]) & set(h["cond_id"])
    keep = set(g.loc[g["recoverable"], "cond_id"]) & common
    gg = g[g["cond_id"].isin(keep)]
    hh = h[h["cond_id"].isin(keep)]

    # ★ 10차 자체 리뷰 — '(바이어스 보정)' 열의 계수를 **비교 모집단 안에서**
    #   다시 추정한다. `_scored` 는 각 artifact 전체에서 보정하는데, halfcell
    #   쪽은 scoring 이 recoverable=True 로 고정하므로 grid-복원불가 조건
    #   (정본 격자의 ~절반)까지 bias 기저에 들어가 두 열이 서로 다른 모집단의
    #   보정을 받았다 (리뷰 실측: dqdv_only corrected 25% → 같은-모집단 0%,
    #   bias_err_lam_ne −1.79%p → +0.09%p). 모집단을 keep 으로 맞춘 뒤 계수를
    #   다시 추정해야 "남는 차이는 기준 곡선"이라는 결론 전제가 성립한다.
    from src.scoring import apply_bias_correction, clean_bias
    _corr_cols = (["resid_" + k for k in ("lli", "lam_pe", "lam_ne")]
                  + ["abs_resid_max", "degenerate_corrected"]
                  + [c for c in gg.columns if c.startswith("bias_err_")])
    gg = apply_bias_correction(gg.drop(columns=_corr_cols, errors="ignore"),
                               clean_bias(gg), tol)
    hh = apply_bias_correction(hh.drop(columns=_corr_cols, errors="ignore"),
                               clean_bias(hh), tol)

    def block(df: pd.DataFrame) -> dict:
        return {o: {
            "n": int(len(x)),
            "degenerate_frac": float(x["degenerate"].mean()),
            "degenerate_frac_corrected": float(x["degenerate_corrected"].mean()),
            "mean_abs_err": float(x["abs_err_max"].mean()),
            "pe_ne_antisym_frac": float(x["pe_ne_antisym"].mean()),
        } for o, x in df.groupby("objective")}

    provenance_ok = all(v["ok"] for v in prov.values()) and not mismatch
    return {
        "provenance": prov,
        "provenance_ok": provenance_ok,
        "공통_run_spec": shared,                  # F69
        "_주의_공통성": (
            "두 실행이 곡선·목적함수·optimizer 정책·환경까지 동일하다."
            if not mismatch else
            f"⚠ 인용 금지 — 두 실행이 다른 실험이다: {mismatch}. "
            "이 표의 차이를 '기준 곡선 효과'로 읽을 수 없다"),
        # ★ F78 — bounds preset 이 reference 별로 다른 것은 설계이지만, 그러면
        #   이 표의 차이는 "기준 곡선 효과"가 아니라 **기준 곡선 + 전용 bounds 를
        #   포함한 reference-specific pipeline 의 차이**다. 인과 문구를 그 수준
        #   으로 제한해야 한다 (리뷰: "최소한 '두 pipeline 차이'라고 써야 한다").
        "reference별_허용차이": allowed_diff_seen,
        "_인과범위": (
            "두 pipeline 은 reference 외에도 다음이 다르다: "
            f"{allowed_diff_seen}. 이 표는 '기준 곡선 단독 효과'가 아니라 "
            "**reference-specific fitting pipeline 의 차이**로 읽어야 한다."
            if allowed_diff_seen else
            "reference 외 모든 축이 동일하다 — 차이를 기준 곡선 효과로 읽을 수 있다."),
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
        # ★ 10차 자체 리뷰 — 보정 계수는 이 표의 **비교 모집단(keep) 안에서**
        #   다시 추정한다 (위 재보정 블록). 전체-모집단 보정을 그대로 쓰면
        #   halfcell 쪽 기저에 grid-복원불가 조건이 섞여 두 열이 비대칭이었다.
        "_주의_바이어스": (
            "'(바이어스 보정)' 열의 계수는 비교 모집단(공통 ∩ grid 복원가능)의 "
            "noise=0 행에서 다시 추정한 값이다 — 각 artifact 파일에 저장된 "
            "전체-모집단 보정과 다를 수 있다. halfcell 쪽 '복원가능'은 측정이 "
            "아니라 고정값이므로(아래 참조) 기저는 keep 으로만 제한된다."),
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
    # ★ 디렉터리를 줘도 받는다. 예전에는 그대로 write_text 해서
    #   `IsADirectoryError` 로 죽었고, e2e smoke 가 이걸 잡았다.
    out = Path(args.out) if args.out else fits(args.grid).parent
    if out.is_dir() or not out.suffix:
        out = out / "case_comparison.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(res, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")
    print(to_markdown(res))
    print(f"\n저장: {out}")


if __name__ == "__main__":
    main()
