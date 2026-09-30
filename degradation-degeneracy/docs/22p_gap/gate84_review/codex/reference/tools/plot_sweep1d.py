"""plot_sweep1d.py — 32p와 동일한 2×3 subplot 재현 (headless, Agg).

패널 순서(원본 subplot 배치): Reference / LLI / LAM_ne_li / LAM_ne_de / LAM_pe_li / LAM_pe_de
각 패널: 정규화 용량 축, PE·NE 곡선(값별 색), full cell(최소·최대 값만 회색점선/검정파선).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as ticker  # noqa: E402
import pandas as pd  # noqa: E402

# 원본 ltype 색 순서
_COLORS = ["k", "r", "b", "g", "m", "c", "y"]

_PANELS = [
    ("reference", "Reference"),
    ("lli", "LLI"),
    ("lam_ne_li", r"LAM$_{ne,li}$"),
    ("lam_ne_de", r"LAM$_{ne,de}$"),
    ("lam_pe_li", r"LAM$_{pe,li}$"),
    ("lam_pe_de", r"LAM$_{pe,de}$"),
]


def plot_sweep1d(df: pd.DataFrame, out_path: str | Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 곡선은 Q_ref로 정규화돼 있으므로, 자기 용량(q_mah/q_ref)을 넘는 구간은
    # 보간 fill 값(평평한 꼬리)이다. 원본 32p처럼 유효 구간만 그린다.
    ref_q = float(df.loc[df["mode"] == "reference", "q_mah"].iloc[0])

    for ax, (mode, title) in zip(axes.flat, _PANELS):
        sub = df[df["mode"] == mode]
        values = sorted(sub["value"].unique())
        for i, v in enumerate(values):
            g = sub[sub["value"] == v]
            valid = g["x_norm"] <= float(g["q_mah"].iloc[0]) / ref_q + 1e-9
            g = g[valid]
            c = _COLORS[i % len(_COLORS)]
            ax.plot(g["x_norm"], g["v_ne"], c + "-", lw=1.0,
                    label=f"{title}={v:g}" if mode != "reference" else "NE (ref.)")
            ax.plot(g["x_norm"], g["v_pe"], c + "-", lw=1.0)
            if i == 0:
                ax.plot(g["x_norm"], g["v_full"], color="gray", linestyle=":",
                        lw=1.5, label=f"Full cell ({v:g})")
            if len(values) > 1 and i == len(values) - 1:
                ax.plot(g["x_norm"], g["v_full"], "k--", lw=1.5,
                        label=f"Full cell ({v:g})")
        ax.set_xlabel("Normalized Capacity")
        ax.set_ylabel("Potential [V]")
        ax.set_title(title)
        ax.legend(fontsize=7)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True,
                    help="sweep1d curves.parquet 또는 그 디렉터리")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    p = Path(args.in_path)
    if p.is_dir():
        p = p / "curves.parquet"
    df = pd.read_parquet(p)
    out = Path(args.out) if args.out else p.parent / "figures" / "32p_reproduction.png"
    print(plot_sweep1d(df, out))


if __name__ == "__main__":
    main()
