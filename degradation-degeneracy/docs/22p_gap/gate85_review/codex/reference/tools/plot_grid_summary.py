"""plot_grid_summary.py — grid 결과 요약 지도 (용량 heatmap).

Phase 5의 degeneracy 지도(plot_map.py) 이전 단계로, grid 곡선 데이터의 sanity check용:
x=LAM_PE, y=LAM_NE, color=Q[mAh], facet=LLI. 불능(infeasible) 셀은 회색 표시.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def plot_grid_summary(run_dir: str | Path, out_path: str | Path | None = None) -> Path:
    run_dir = Path(run_dir)
    df = pd.read_parquet(run_dir / "curves.parquet")
    q = df.groupby(["lli", "lam_pe", "lam_ne"], as_index=False).q_mah.first()

    lli_vals = sorted(q["lli"].unique())
    pe_vals = sorted(df["lam_pe"].unique())
    ne_vals = sorted(df["lam_ne"].unique())

    fig, axes = plt.subplots(1, len(lli_vals), figsize=(3.2 * len(lli_vals), 3.6),
                             sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    vmin, vmax = q.q_mah.min(), q.q_mah.max()

    for ax, lli in zip(axes, lli_vals):
        sub = q[q["lli"] == lli]
        grid = np.full((len(ne_vals), len(pe_vals)), np.nan)
        for _, r in sub.iterrows():
            grid[ne_vals.index(r["lam_ne"]), pe_vals.index(r["lam_pe"])] = r["q_mah"]
        masked = np.ma.masked_invalid(grid)
        cmap = plt.get_cmap("viridis").copy()
        cmap.set_bad("lightgray")   # infeasible 셀
        im = ax.pcolormesh(pe_vals, ne_vals, masked, cmap=cmap, vmin=vmin, vmax=vmax,
                           shading="nearest")
        ax.set_title(f"LLI = {lli:g}")
        ax.set_xlabel(r"LAM$_{PE}$")
    axes[0].set_ylabel(r"LAM$_{NE}$")
    fig.colorbar(im, ax=axes, label="Q [mAh]", shrink=0.85)
    # 서버 기본 폰트에 한글 글리프가 없어 그림 내 텍스트는 영문 고정
    fig.suptitle("Coarse grid — discharge capacity map (gray = PE-limited infeasible)",
                 y=1.06)

    out = Path(out_path) if out_path else run_dir / "figures" / "grid_capacity_map.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    print(plot_grid_summary(args.in_dir, args.out))
