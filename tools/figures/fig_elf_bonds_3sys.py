#!/usr/bin/env python3
"""fig_elf_bonds_3sys.py — ELF 결합 서술자 3계 비교 (comp1 · modelc · lpsocl).

⚠ **읽어야 할 양은 ELF_central_min 이다.**
   ELF_midpoint 는 짧은 결합에서 상대 원자의 lone-pair 영역에 걸려 높게 읽힌다 —
   Li–O 가 중점 0.784(중간)인데 central_min 0.163(최저)인 것이 그 실증이다.
   문헌 관례도 bond-path 의 **최솟값**으로 공유/이온을 가른다(>0.7 공유 · <0.3 이온).
   그래서 두 값을 나란히 그리되 central_min 을 주패널로 둔다.

  python3 tools/figures/fig_elf_bonds_3sys.py
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT, ELEM, SYS, apply_axes            # noqa: E402

SRC = [(ROOT / "docs/figures/icohp/elf_bond_midpoint.csv", None),
       (ROOT / "db/properties/lpsocl_elf_bond_midpoint.csv", None)]
OUT = ROOT / "docs/figures/icohp/elf_bonds_3sys.png"
CSVOUT = ROOT / "db/properties/elf_bonds_3sys_origin.csv"

ORDER = ["P-S", "O-P", "Li-S", "Cl-Li", "Li-O"]     # 공유 → 이온 순
SYSORDER = ["comp1", "modelc", "lpsocl"]
LABEL = {"comp1": "comp1 (Li₆PS₅Cl)", "modelc": "modelc (LPSCl1.6)",
         "lpsocl": "lpsocl (+O)"}
# 공유/이온 판정선 (문헌 관례)
COV, ION = 0.70, 0.30


def load():
    rows = {}
    for f, _ in SRC:
        if not f.exists():
            continue
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            rows.setdefault(r["system"], {})[r["bond"]] = r
    return rows


def main():
    R = load()
    syss = [s for s in SYSORDER if s in R]
    bonds = [b for b in ORDER if any(b in R[s] for s in syss)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 4.8),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    x = np.arange(len(bonds)); w = 0.8 / max(1, len(syss))

    # (a) central_min — 주패널
    for j, s in enumerate(syss):
        v = [float(R[s][b]["ELF_central_min"]) if b in R[s] and R[s][b].get("ELF_central_min")
             else np.nan for b in bonds]
        ax1.bar(x + (j - (len(syss) - 1) / 2) * w, v, w, label=LABEL.get(s, s),
                color=SYS.get(s, MUT), edgecolor=INK, linewidth=0.5)
        for xi, vi in zip(x + (j - (len(syss) - 1) / 2) * w, v):
            if not np.isnan(vi):
                ax1.text(xi, vi + 0.02, f"{vi:.2f}", ha="center", fontsize=7.5, color=INK)
    ax1.axhline(COV, color="#0d9488", ls="--", lw=1.2)
    ax1.axhline(ION, color="#be123c", ls="--", lw=1.2)
    ax1.text(len(bonds) - 0.45, COV + 0.015, "covalent  > 0.70", fontsize=8.5,
             color="#0d9488", ha="right")
    ax1.text(len(bonds) - 0.45, ION - 0.055, "ionic  < 0.30", fontsize=8.5,
             color="#be123c", ha="right")
    ax1.set_xticks(x); ax1.set_xticklabels(bonds, fontsize=10)
    ax1.set_ylim(0, 1.05)
    apply_axes(ax1, ylabel="ELF central minimum (bond path)",
               title="(a) ELF central min — the discriminating quantity")
    ax1.legend(frameon=False, fontsize=8.5, loc="lower left")

    # (b) midpoint — 왜 이걸로 판정하면 안 되는지
    for j, s in enumerate(syss):
        v = [float(R[s][b]["ELF_midpoint"]) if b in R[s] else np.nan for b in bonds]
        ax2.bar(x + (j - (len(syss) - 1) / 2) * w, v, w, label=LABEL.get(s, s),
                color=SYS.get(s, MUT), edgecolor=INK, linewidth=0.5, alpha=0.75)
    ax2.set_xticks(x); ax2.set_xticklabels(bonds, fontsize=10)
    ax2.set_ylim(0, 1.05)
    apply_axes(ax2, ylabel="ELF at bond midpoint",
               title="(b) midpoint — compressed, do not rank with this")
    ax2.text(0.5, 0.06,
             "Li–O reads 0.78 here (middling) but 0.16 in (a):\n"
             "the midpoint of a short bond sits inside the O lone pair.",
             transform=ax2.transAxes, ha="center", fontsize=8.5, color=MUT,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=MUT, lw=0.7))

    fig.suptitle("ELF bond descriptors — host bonds unchanged by O doping; "
                 "Li–O is the most ionic bond in the lattice",
                 fontsize=11, color=MUT, y=1.0)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {OUT}")

    with open(CSVOUT, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# ELF bond descriptors, 3 systems — Origin-ready\n")
        f.write("# ⚠ ELF_central_min 이 판별력 있는 양. midpoint 는 짧은 결합에서 lone-pair 에 걸려 높다.\n")
        f.write("# 방법: QE pp.x plot_num=8 on NC ONCV scf. comp1/modelc 는 기존 산출, lpsocl 은 2026-07-29.\n")
        w_ = csv.writer(f)
        w_.writerow(["system", "bond", "n_bonds", "mean_dist_A", "ELF_midpoint",
                     "ELF_mid_std", "ELF_central_min"])
        for s in syss:
            for b in bonds:
                if b in R[s]:
                    r = R[s][b]
                    w_.writerow([s, b, r["n_bonds"], r["mean_dist_A"], r["ELF_midpoint"],
                                 r.get("ELF_mid_std", ""), r.get("ELF_central_min", "")])
    print(f"→ {CSVOUT}")
    for s in syss:
        for b in bonds:
            if b in R[s]:
                r = R[s][b]
                print(f"  {s:8s} {b:6s} mid {float(r['ELF_midpoint']):.3f} · "
                      f"cmin {float(r['ELF_central_min']):.3f}")


if __name__ == "__main__":
    main()
