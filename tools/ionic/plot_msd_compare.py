#!/usr/bin/env python3
"""Combine multiple msd_origin LiMSD_vs_t.csv into one Origin CSV + a qualitative
MSD-vs-t preview PNG (NO slope/D annotation — curves only).

Usage:
  python3 plot_msd_compare.py \
      comp1=msd_origin/comp1/comp1_LiMSD_vs_t.csv \
      modelc=msd_origin/modelc/modelc_LiMSD_vs_t.csv \
      --out_csv msd_compare.csv --out_png msd_compare.png
"""
import argparse, csv, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

REDS = ["#fca5a5", "#ef4444", "#991b1b"]   # 600/800/1000 light->dark
BLUES = ["#93c5fd", "#3b82f6", "#1e3a8a"]
CMAP = {"comp1": REDS, "modelc": BLUES}


def read_csv(path):
    rows = list(csv.reader(open(path)))
    hdr = rows[0]
    data = np.array([[float(x) if x not in ("", None) else np.nan for x in r]
                     for r in rows[1:] if any(c.strip() for c in r)])
    return hdr, data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+", help="label=path.csv (LiMSD_vs_t)")
    ap.add_argument("--out_csv", default="msd_compare.csv")
    ap.add_argument("--out_png", default="msd_compare.png")
    args = ap.parse_args()

    series = []
    for item in args.pairs:
        if "=" not in item:
            sys.exit(f"bad pair (need label=path): {item}")
        lab, path = item.split("=", 1)
        series.append((lab, *read_csv(path)))

    nmin = min(s[2].shape[0] for s in series)
    t = series[0][2][:nmin, 0]
    cols, names = [t], ["t_ps"]

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for lab, hdr, data in series:
        shades = CMAP.get(lab.lower(), None)
        for j in range(1, data.shape[1]):
            y = data[:nmin, j]
            Tlab = hdr[j].replace("MSD_", "").replace("_A2", "")
            cols.append(y); names.append(f"{lab}_{Tlab}")
            ti = {"600K": 0, "800K": 1, "1000K": 2}.get(Tlab, j - 1)
            c = shades[ti] if shades and ti < len(shades) else None
            ax.plot(t, y, lw=1.6, color=c, label=f"{lab} {Tlab}")

    np.savetxt(args.out_csv, np.c_[cols].T, delimiter=",",
               header=",".join(names), comments="")
    ax.set_xlabel("Time (ps)", fontsize=12)
    ax.set_ylabel("Li MSD (Å²)", fontsize=12)
    ax.set_title("Li MSD vs t — comp1 (LPSCl) vs modelc (LPSCl$_{1.6}$)\n"
                 "qualitative (slope/D in the Arrhenius table, not here)", fontsize=11)
    ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(args.out_png, dpi=200)
    print(f"-> {args.out_csv}  ({len(names)-1} series)")
    print(f"-> {args.out_png}")


if __name__ == "__main__":
    main()
