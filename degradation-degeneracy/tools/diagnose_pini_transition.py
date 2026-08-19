"""왜 격자마다 왜곡 민감도 문턱이 다른가 — Case 1 좌표 원점을 본다.

★ 13차 게이트에서 열린 질문. 같은 왜곡(PE +2 mV)이 dense 격자에서는 상전이를
  일으키고(거짓 분리 6.2% → 96.3%) seed_101 격자에서는 아무 일도 안 했다
  (6.7% → 6.7%). 코드·캐시는 동일했고, dense 를 다른 코드로 재실행해 결과가
  완전히 같음을 확인해 코드 변경도 배제했다.

  남은 축은 `p_ini` — half-cell 기준(Case 1)의 좌표 원점이다. 이것은 격자마다
  **pristine 조건**(lli=lam_pe=lam_ne=0, noise=0)을 자체 fitting 해서 만든다.
  그 곡선은 두 격자에서 물리적으로 같다. 그런데 값이 달랐다:

      dense    [1.5333, -0.4307, 1.0312, -0.0279]
      seed_101 [1.5128, -0.4215, 1.0629, -0.0597]

  multistart 난수 seed 가 `sha1(cond_id)` 에서 나오고 cond_id 에는 noise_seed 가
  들어가므로, **같은 곡선이 격자마다 다른 국소해로 수렴**할 수 있다. 즉 조건
  하나의 최적화 요동이 격자 전체의 좌표계를 정하고, 그 좌표계가 왜곡 하에서
  반대칭 골짜기로 떨어지는지를 좌우한다 — 이것이 검증할 가설이다.

이 도구는 그 가설을 **데이터로** 놓는다. 여러 fit 다리의 원점과 결과를 한 표로
모으고, 원점 차이와 붕괴율 차이가 같이 움직이는지 보여준다. 인과를 증명하지는
않는다 (그러려면 원점을 바꿔 끼워 돌려야 한다) — 상관을 보여주고 다음 실험을
겨냥하게 한다.

사용:
    python tools/diagnose_pini_transition.py --legs results/fit_22p_dense_hc \\
        results/fit_dense_pe2mv results/fit_22p_seed_101_hc results/fit_seed101_pe2mv
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PARAM_NAMES = ("a_pe", "b_pe", "a_ne", "b_ne")


def leg_facts(run_dir: str | Path, objective: str) -> dict:
    """한 fit 다리에서 원점·왜곡·결과 요약을 뽑는다."""
    import pandas as pd
    import yaml

    d = Path(run_dir)
    man = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8")) or {}
    spec = man.get("run_spec") or {}
    recipe = spec.get("halfcell_recipe") or {}

    f = pd.read_parquet(d / "fits.parquet")
    f = f[f["objective"] == objective]
    if f.empty:
        raise SystemExit(f"{d}: objective={objective} 행이 없습니다 "
                         f"(있는 것: {sorted(set(pd.read_parquet(d / 'fits.parquet')['objective']))})")

    p_ini = (spec.get("p_ini") or {}).get(objective)
    return {
        "dir": str(d),
        "source_digest": spec.get("source_digest"),
        "p_ini": [round(float(x), 4) for x in p_ini] if p_ini else None,
        # ★ 원점을 만든 조건. 옛 artifact 에는 없다 (13차에 봉인을 추가했다).
        "p_ini_cond": spec.get("p_ini_cond"),
        "offset_pe_mv": float(recipe.get("pe_offset_mv") or 0.0),
        "offset_ne_mv": float(recipe.get("ne_offset_mv") or 0.0),
        "stretch_pe": float(recipe.get("pe_stretch") or 1.0),
        "stretch_ne": float(recipe.get("ne_stretch") or 1.0),
        "n_cond": int(f["cond_id"].nunique()),
        "frame": f,
    }


def gap_stats(f, tol: float) -> dict:
    """참 격차 0 칸의 거짓 분리와 전체 격차 bias (동작점 근방)."""
    import numpy as np

    g = f[(f["noise"] == 0)].copy()
    g["true_gap"] = (g["lam_pe"] - g["lam_ne"]).abs()
    g["rec_gap"] = (g["lam_pe_hat"] - g["lam_ne_hat"]).abs()
    near = g[(g["lli"] - 0.17).abs().le(0.02)
             & (((g["lam_pe"] + g["lam_ne"]) / 2) - 0.13).abs().le(0.02)]
    zero = near[near["true_gap"] <= 1e-9]
    signed = ((near["lam_pe_hat"] - near["lam_pe"])
              - (near["lam_ne_hat"] - near["lam_ne"]))
    return {
        "n_near": int(len(near)),
        "n_gap0": int(len(zero)),
        "false_split": int((zero["rec_gap"] >= tol).sum()),
        "gap_bias_pp": round(100 * float(signed.mean()), 2) if len(near) else None,
        "median_rec_gap0_pp": (round(100 * float(zero["rec_gap"].median()), 2)
                               if len(zero) else None),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--legs", nargs="+", required=True, help="fit 디렉터리들")
    ap.add_argument("--objective", default="pocv_dvdq_dqdv")
    ap.add_argument("--tol", type=float, default=0.02, help="판정선 (기본 2%p)")
    ap.add_argument("--json", default=None, help="요약을 JSON 으로도 저장")
    args = ap.parse_args()

    rows = []
    for leg in args.legs:
        d = leg_facts(leg, args.objective)
        d.update(gap_stats(d.pop("frame"), args.tol))
        rows.append(d)

    print("=" * 78)
    print(f" Case 1 좌표 원점 vs 왜곡 민감도  (objective={args.objective}, "
          f"판정선 {100*args.tol:.0f}%p)")
    print("=" * 78)
    print("\n★ 묻는 것: 원점(p_ini)이 다른 다리끼리 붕괴율도 다른가.")
    print("  원점은 pristine 조건(lli=lam=0, noise=0) 자체 fitting 으로 만드는데,")
    print("  multistart 난수가 cond_id 에 묶여 있어 **같은 곡선도 격자마다 다른")
    print("  국소해**로 갈 수 있다. 그 원점이 왜곡 하에서 반대칭 골짜기로")
    print("  떨어지는지를 좌우한다는 것이 검증 대상 가설이다.\n")

    for r in rows:
        wob = []
        if r["offset_pe_mv"]:
            wob.append(f"PE {r['offset_pe_mv']:+g} mV")
        if r["offset_ne_mv"]:
            wob.append(f"NE {r['offset_ne_mv']:+g} mV")
        if r["stretch_pe"] != 1.0:
            wob.append(f"PE stretch {r['stretch_pe']:g}")
        if r["stretch_ne"] != 1.0:
            wob.append(f"NE stretch {r['stretch_ne']:g}")
        fs = (f"{r['false_split']}/{r['n_gap0']} "
              f"({100*r['false_split']/r['n_gap0']:.1f}%)" if r["n_gap0"] else "—")
        print(f"── {Path(r['dir']).name}")
        print(f"   왜곡      : {' · '.join(wob) if wob else '없음 (대조)'}")
        print(f"   p_ini     : {r['p_ini']}")
        print(f"   원점 조건 : {r['p_ini_cond'] or '(미봉인 — 13차 이전 artifact)'}")
        print(f"   digest    : {r['source_digest']}")
        print(f"   거짓 분리 : {fs}   ①' 격차 bias {r['gap_bias_pp']}%p   "
              f"참0 복원격차 중앙값 {r['median_rec_gap0_pp']}%p")
        print()

    # 원점이 같은 다리끼리 묶어 본다 — 같은 좌표계에서 왜곡만 다른 비교가
    # 되어야 "왜곡 때문" 이라고 말할 수 있다.
    by_ini: dict = {}
    for r in rows:
        by_ini.setdefault(str(r["p_ini"]), []).append(r)
    print("── 원점별 묶음 (같은 좌표계 안에서만 왜곡 효과를 읽을 수 있다)")
    for ini, group in by_ini.items():
        names = ", ".join(Path(g["dir"]).name for g in group)
        print(f"   {ini}\n     → {names}")
    if len(by_ini) > 1:
        print("\n   ⚠ 원점이 여러 개다. 다른 원점끼리의 붕괴율 차이는 왜곡 효과와")
        print("     좌표계 효과가 **섞여** 있다 — 그대로 문턱으로 인용하지 말 것.")

    if args.json:
        Path(args.json).write_text(
            json.dumps([{k: v for k, v in r.items()} for r in rows],
                       ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n요약 저장: {args.json}")


if __name__ == "__main__":
    main()
