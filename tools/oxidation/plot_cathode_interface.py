#!/usr/bin/env python3
"""plot_cathode_interface.py — SE/cathode oxidation-reactivity figure.

Reads the interface_reactivity_v2.py json (GrandPotential interfacial reactivity,
Richards/Ong 2016) and plots the most-exothermic SE/cathode reaction energy vs the
applied charge voltage, for each cathode, doped (solid) vs undoped (dashed). More
negative = more reactive interface = worse. The oxidation-side counterpart to
plot_anode_interface.py; together they give the both-sided interface module.

  python3 tools/oxidation/plot_cathode_interface.py \
      --json db/properties/cathode_interface_b2o3.json \
      --out docs/figures/oxidation/b2o3_cathode_interface.png
"""
import argparse, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CAT_COLORS = ["#c0392b", "#2c7fb8", "#27ae60", "#8e44ad", "#e67e22"]
DOPED, UNDOPED = "b2o3", "LPSCl1.6"
DOPED_LBL = "B₂O₃-doped"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="db/properties/cathode_interface_b2o3.json")
    ap.add_argument("--out", default="docs/figures/oxidation/b2o3_cathode_interface.png")
    A = ap.parse_args()
    d = json.loads(Path(A.json).read_text())
    res = d["results"]

    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    for ci, (cat, cd) in enumerate(res.items()):
        bv = cd.get("by_voltage", {})
        Vs = sorted(bv, key=float)
        x = [float(v) for v in Vs]
        col = CAT_COLORS[ci % len(CAT_COLORS)]
        y_d = [bv[v].get(DOPED) for v in Vs]
        y_u = [bv[v].get(UNDOPED) for v in Vs]
        if any(e is not None for e in y_d):
            ax.plot(x, [e if e is not None else np.nan for e in y_d], "-o", color=col,
                    lw=2, ms=5, label=f"{cat} · {DOPED_LBL}")
        if any(e is not None for e in y_u):
            ax.plot(x, [e if e is not None else np.nan for e in y_u], "--s", color=col,
                    lw=1.6, ms=4, mfc="white", label=f"{cat} · undoped")

    ax.axhline(0, color="black", lw=0.9, zorder=1)
    ax.set_xlabel("charge voltage V (vs Li/Li⁺)")
    ax.set_ylabel("most-exothermic SE/cathode reaction energy (eV/atom)")
    ax.set_title("Cathode oxidation-interface reactivity (open-Li, Richards/Ong 2016)\n"
                 "more negative = more reactive interface (worse); solid = doped, dashed = undoped",
                 fontsize=10.5)
    ax.invert_yaxis()                       # more-negative (more reactive) at top -> reactivity ramps UP with V
    ax.grid(ls=":", alpha=0.4)
    ax.legend(fontsize=8.5, framealpha=0.95, ncol=max(1, len(res) // 2))
    fig.tight_layout()
    Path(A.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(A.out, dpi=200)
    print(f"-> {A.out}")


if __name__ == "__main__":
    main()
