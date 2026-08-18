"""analyze_22p_gap.py — 22p 동작점에서 두 전극을 가를 수 있는가.

★ 이 저장소의 원래 질문에 **직접** 답하는 분석이다.

v4 본 격자는 `0.0:0.20:0.02` 라 값이 전부 짝수 백분위여서 22p 조건
(LAM_PE ≈ LAM_NE ≈ 0.13, LLI ≈ 0.17) 이 격자에 없었다. `verdict_22p` 가
반경 0.021 로 잡은 8점은 그 조건을 둘러싼 corner 이고 참 격차가 0 또는 2%p
뿐이라 wide-gap 이 하나도 없었다 — "참 격차가 큰데도 같다고 답하는가" 를
그 표본으로는 물을 수 없다 (v4 결론 3 의 한계).

`configs/grid_22p.yaml` 은 22p 를 격자에 정확히 넣고 평균 LAM 을 0.13 에
고정한 채 |ΔLAM| 을 0 → 12%p 로 쓴다. 이 도구는 그 스윕을 읽어

  · 참 격차별 **붕괴율** (복원 격차 < tol) 과 shrinkage
  · 22p 동작점(LLI 0.17 · 평균 LAM 0.13 · noise 0) 만의 값
  · 평균·LLI·noise 를 넓혀 n 을 키운 값

을 나란히 낸다. **둘을 함께 봐야 한다** — 좁히면 n 이 작고, 넓히면 동작점이
아니다.

    python tools/analyze_22p_gap.py --in results/fit_22p_v1
    python tools/analyze_22p_gap.py --in results/fit_22p_v1 --plot out.png
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

log = logging.getLogger(__name__)

#: 22p 동작점
P22 = {"lli": 0.17, "lam_mean": 0.13}


def _fmt_pp(x) -> str:
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) \
        else f"{100 * float(x):.1f}%p"


def gap_table(df: pd.DataFrame, tol: float = 0.02) -> pd.DataFrame:
    """참 격차 구간별 복원 성적.

    붕괴 = 참 격차가 있는데 복원 격차 < tol → "두 전극이 같다" 고 답한 것.
    """
    from tools.compare_objectives import gap_is_zero, gap_lt

    g = df.copy()
    g["gap_true"] = (g["lam_pe"] - g["lam_ne"]).abs()
    g["gap_hat"] = g["pe_ne_gap_recovered"]
    # ★ bin 폭은 **0.01(1%p)** 이다. 0.02 로 묶으면 촘촘한 격자(0.01 step)의
    #   홀수 격차가 이웃 짝수 bin 으로 넘어가 표가 거짓이 된다 (3%p → 4%p).
    #   0.02 step 격자에서는 결과가 같으므로 손해가 없다. 표현 오차는
    #   반올림으로 흡수한다.
    g["gap_bin"] = (g["gap_true"] / 0.01).round().astype(int)       # %p 단위

    rows = []
    for b, sub in g.groupby("gap_bin", sort=True):
        collapsed = gap_lt(sub["gap_hat"], tol)
        rows.append({
            "참 격차": f"{b}%p",
            "n": int(len(sub)),
            "붕괴(복원<2%p)": f"{int(collapsed.sum())}/{len(sub)}"
                              f" ({100 * collapsed.mean():.1f}%)",
            "복원 격차 중앙값": _fmt_pp(sub["gap_hat"].median()),
            "shrinkage": ("—" if b == 0 else
                          f"{float((sub['gap_hat'] / sub['gap_true']).median()):.2f}"),
        })
    return pd.DataFrame(rows)


def run(in_dir, objective: str = "pocv_dvdq", tol: float = 0.02,
        plot: str | None = None) -> dict:
    from tools.compare_cases import _scored

    in_dir = Path(in_dir)
    df = _scored(in_dir / "fits.parquet", tol)
    df = df[df["objective"] == objective]
    if df.empty:
        raise SystemExit(f"목적함수 {objective} 행이 없습니다")

    df = df.copy()
    df["lam_mean"] = (df["lam_pe"] + df["lam_ne"]) / 2
    df["gap_true"] = (df["lam_pe"] - df["lam_ne"]).abs()

    rec = df[df["recoverable"]] if "recoverable" in df.columns else df

    # ── ① 22p 동작점만 (LLI 0.17 · 평균 LAM 0.13 · noise 0) ─────────────
    tight = rec[(rec["lli"].sub(P22["lli"]).abs() < 1e-9)
                & (rec["lam_mean"].sub(P22["lam_mean"]).abs() < 1e-9)
                & (rec["noise"] == 0)]

    # ── ①' 동작점 **근방** — 좁히면 n 이 작고 넓히면 동작점이 아니다.
    #      그 사이를 메우는 중간 층 (★ 첫 실행에서 ① 이 n=5 였다).
    near = rec[(rec["lli"].sub(P22["lli"]).abs() <= 0.021)
               & (rec["lam_mean"].sub(P22["lam_mean"]).abs() <= 0.021)
               & (rec["noise"] == 0)]

    # ── ② 넓힌 표본 — LLI 전부 · 평균 전체 · noise 0 ──────────────────────
    wide = rec[rec["noise"] == 0]

    out = {
        "objective": objective, "tol": tol,
        "n_rows_total": int(len(df)),
        "n_recoverable": int(len(rec)),
        "tight": {"n": int(len(tight)),
                  "정의": "LLI=0.17 · 평균 LAM=0.13 · noise=0 · 복원가능군"},
        "near": {"n": int(len(near)),
                 "정의": "|LLI−0.17|≤2%p · |평균 LAM−0.13|≤2%p · noise=0 · 복원가능군"},
        "wide": {"n": int(len(wide)),
                 "정의": "noise=0 · 복원가능군 (평균·LLI 전부)"},
    }

    print("=" * 74)
    print(f" 22p 동작점에서 두 전극을 가를 수 있는가  (objective={objective})")
    print("=" * 74)
    print(f"\n전체 {len(df)}행 중 복원가능군 {len(rec)}행 "
          f"({100 * len(rec) / len(df):.0f}%)\n")

    print("① 22p 동작점만 — LLI 0.17 · 평균 LAM 0.13 · noise 0")
    print(f"   (평균을 고정했으므로 '격차 때문인지 총 열화량 때문인지' 가 안 섞인다)\n")
    if len(tight):
        t1 = gap_table(tight, tol)
        print(t1.to_string(index=False))
        out["tight"]["table"] = t1.to_dict("records")
    else:
        print("   조건 없음 — 격자에 그 동작점이 없다")
    print(f"\n   ⚠ n={len(tight)} 로 작다. 아래 넓힌 표본과 **함께** 볼 것.\n")

    print("①' 동작점 근방 — |LLI−17%| ≤ 2%p · |평균 LAM−13%| ≤ 2%p · noise 0")
    print("   (① 과 ② 사이 — 동작점을 크게 벗어나지 않으면서 n 을 키운다)\n")
    if len(near):
        tn = gap_table(near, tol)
        print(tn.to_string(index=False))
        out["near"]["table"] = tn.to_dict("records")
    else:
        print("   조건 없음")
    print()

    print("② 넓힌 표본 — noise 0 · 복원가능군 (평균 LAM·LLI 전부)")
    print("   (n 은 크지만 22p 동작점이 아닌 조건이 섞인다)\n")
    t2 = gap_table(wide, tol)
    print(t2.to_string(index=False))
    out["wide"]["table"] = t2.to_dict("records")

    # ── ③ 22p 조건 자체 ────────────────────────────────────────────────
    exact = df[(df["lli"].sub(0.17).abs() < 1e-9)
               & (df["lam_pe"].sub(0.13).abs() < 1e-9)
               & (df["lam_ne"].sub(0.13).abs() < 1e-9)]
    print(f"\n③ 22p 조건 그 자체 (0.13, 0.13, 0.17) — n={len(exact)}")
    for _, r in exact.iterrows():
        print(f"   noise={r['noise']:<6g} 복원 LAM_PE={r['lam_pe_hat']:.4f} "
              f"LAM_NE={r['lam_ne_hat']:.4f} LLI={r['lli_hat']:.4f} "
              f"| 복원 격차 {_fmt_pp(r['pe_ne_gap_recovered'])}"
              f" | recoverable={bool(r.get('recoverable', True))}")
    out["exact_22p"] = exact[["noise", "lam_pe_hat", "lam_ne_hat", "lli_hat",
                              "pe_ne_gap_recovered"]].to_dict("records")

    # ── ④ 누적 사건률 — 인용 가능한 한 줄이 표에서 바로 나오게 ───────────
    from tools.compare_objectives import gap_lt as _lt
    print("\n④ 누적 — '참 격차가 이만큼 이상인데 같다고 답한' 비율")
    for label, sub in (("동작점 근방(①')", near), ("넓힌 표본(②)", wide)):
        if not len(sub):
            continue
        g = sub.copy()
        g["gap_true"] = (g["lam_pe"] - g["lam_ne"]).abs()
        line = []
        for thr in (0.04, 0.06, 0.08):
            s2 = g[g["gap_true"] >= thr - 1e-9]
            if not len(s2):
                line.append(f"≥{100*thr:.0f}%p: n=0")
                continue
            k = int(_lt(s2["pe_ne_gap_recovered"], tol).sum())
            line.append(f"≥{100*thr:.0f}%p: {k}/{len(s2)} ({100*k/len(s2):.1f}%)")
            out.setdefault("cumulative", {}).setdefault(label, {})[
                f">={100*thr:.0f}pp"] = {"k": k, "n": int(len(s2))}
        print(f"   {label:<16s} " + "  ·  ".join(line))
    print("   ⚠ 동일가중 합성격자의 **조건부 사건률**이다 — 실제 셀 posterior 가 아니다.")

    if plot:
        _plot(wide, tight, plot, objective, tol)
        print(f"\n그림: {plot}")
    print()
    return out


def _plot(wide: pd.DataFrame, tight: pd.DataFrame, path: str,
          objective: str, tol: float) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    hi = max(0.14, float(wide["gap_true"].max()) * 1.05)

    ax.axhspan(0, tol, color="#dc2626", alpha=.07)
    ax.axhline(tol, color="#dc2626", lw=1, ls=":")
    ax.text(0.004, tol * 1.06, f'judged "same"  (< {100*tol:.0f}%p)',
            fontsize=8.5, color="#dc2626")
    ax.plot([0, hi], [0, hi], color="#059669", lw=1.6, ls="--",
            label="perfect recovery")

    ax.scatter(wide["gap_true"] * 100, wide["gap_hat"] * 100 if "gap_hat" in wide
               else wide["pe_ne_gap_recovered"] * 100,
               s=16, c="#9aa5b1", alpha=.55, label="all (noise 0, recoverable)")
    if len(tight):
        ax.scatter(tight["gap_true"] * 100,
                   tight["pe_ne_gap_recovered"] * 100,
                   s=95, marker="D", facecolors="none", edgecolors="#2563eb",
                   linewidths=2, label="22p operating point\n(LLI 17%, mean LAM 13%)")
    ax.set(xlabel="TRUE gap  |LAM_PE − LAM_NE|  [%p]",
           ylabel="RECOVERED gap  [%p]",
           title=f"Can the fit tell the electrodes apart?  ({objective})")
    ax.legend(fontsize=8.5, loc="upper left")
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="22p 동작점 격차 복원력 분석")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--objective", default="pocv_dvdq")
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--plot", default=None)
    ap.add_argument("--log-level", default="WARNING")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run(args.in_dir, args.objective, args.tol, args.plot)


if __name__ == "__main__":
    main()
