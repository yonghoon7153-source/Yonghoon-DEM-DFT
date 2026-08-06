"""plot_map.py — degeneracy 지도 (Phase 5).

x=LAM_PE, y=LAM_NE, 색=abs_err_max, LLI별 facet.
**22p 실험 조건(LAM_PE≈13%, LAM_NE≈13%, LLI≈17%)을 마커로 찍어**
"우리 실험 조건이 degeneracy 영역 안에 있는가"에 그림으로 답한다.

리뷰 규칙 반영:
  F1  복원불가군(α_true<1)은 회색 해치로 구분 — 정답이 원리적으로 못 나오는 영역
  F14 저LLI+고LAM_PE 코너가 격자에 없다는 사실을 그림에 명시
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# 22p 실험 조건 (세미나 슬라이드)
EXP_22P = {"lam_pe": 0.13, "lam_ne": 0.13, "lli": 0.17}


def plot_degeneracy_map(df: pd.DataFrame, out_path, objective: str = "pocv_dvdq",
                        noise: float | None = 0.0, value: str = "abs_err_max",
                        tol: float = 0.02):
    sub = df[df["objective"] == objective]
    if noise is not None and "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if sub.empty:
        raise SystemExit(f"조건에 맞는 행 없음 (objective={objective}, noise={noise})")

    lli_vals = sorted(sub["lli"].unique())
    pe_vals = sorted(sub["lam_pe"].unique())
    ne_vals = sorted(sub["lam_ne"].unique())

    # 서버 기본 폰트에 한글 글리프가 없어 그림 내 텍스트는 영문 고정
    nearest_lli = min(lli_vals, key=lambda v: abs(v - EXP_22P["lli"]))

    fig, axes = plt.subplots(1, len(lli_vals),
                             figsize=(2.6 * len(lli_vals) + 2, 3.4),
                             sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    vmax = float(np.nanpercentile(sub[value], 98))

    for ax, lli in zip(axes, lli_vals):
        g = sub[sub["lli"] == lli]
        grid = np.full((len(ne_vals), len(pe_vals)), np.nan)
        unrec = np.zeros_like(grid, dtype=bool)
        for _, r in g.iterrows():
            i, j = ne_vals.index(r["lam_ne"]), pe_vals.index(r["lam_pe"])
            grid[i, j] = r[value]
            if "recoverable" in r and not r["recoverable"]:
                unrec[i, j] = True

        cmap = plt.get_cmap("RdYlGn_r").with_extremes(bad="0.85")
        im = ax.pcolormesh(pe_vals, ne_vals, np.ma.masked_invalid(grid),
                           cmap=cmap, vmin=0, vmax=vmax, shading="nearest")
        # F1: 원리적 복원불가 영역을 해치로 (정답이 못 나오는 곳)
        if unrec.any():
            ax.contourf(pe_vals, ne_vals, unrec.astype(float), levels=[0.5, 1.5],
                        colors="none", hatches=["///"], alpha=0)
        # degeneracy 경계선
        try:
            ax.contour(pe_vals, ne_vals, np.nan_to_num(grid), levels=[tol],
                       colors="k", linewidths=1.2, linestyles="--")
        except Exception:  # noqa: BLE001
            pass
        # 22p 실험 조건 — LLI가 가장 가까운 패널 하나에만 (연산자 우선순위 함정 회피)
        if lli == nearest_lli:
            ax.plot(EXP_22P["lam_pe"], EXP_22P["lam_ne"], "*", ms=18,
                    mfc="cyan", mec="k", mew=1.2, label="22p experiment", zorder=5)
            ax.legend(fontsize=7, loc="upper left")
        ax.set_title(f"LLI = {lli:g}", fontsize=10)
        ax.set_xlabel(r"LAM$_{PE}$")
    axes[0].set_ylabel(r"LAM$_{NE}$")
    cb = fig.colorbar(im, ax=axes, shrink=0.85)
    cb.set_label(f"{value}   (dashed = {tol:g} threshold)")
    fig.suptitle(f"Degeneracy map — {objective}"
                 + (f", noise={noise:g}" if noise is not None else "")
                 + "   [gray = not in grid · hatched = unrecoverable by construction]",
                 y=1.08, fontsize=10)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="degeneracy 지도")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--objective", default="pocv_dvdq")
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--value", default="abs_err_max")
    ap.add_argument("--tol", type=float, default=0.02)
    args = ap.parse_args()

    d = Path(args.in_dir)
    df = pd.read_parquet(d / "degeneracy_map.parquet")
    out = Path(args.out) if args.out else d / "figures" / f"degeneracy_{args.objective}.png"
    print(plot_degeneracy_map(df, out, args.objective, args.noise, args.value, args.tol))


if __name__ == "__main__":
    main()
