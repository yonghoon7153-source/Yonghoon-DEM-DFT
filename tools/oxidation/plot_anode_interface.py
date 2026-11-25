#!/usr/bin/env python3
"""plot_anode_interface.py — anode reduction-interphase figure from the by_anode json.

Reads db/properties/anode_interface_b2o3.json (the open-Li get_element_profile
output) and plots the min interphase band gap per (electrolyte, anode), with the
leaky threshold (2 eV) and the gap-limiting phase annotated. Shows the Li-metal ->
Li-In mitigation directly: b2o3's metallic-LiB liability is bare-Li-metal-specific.

  python3 tools/oxidation/plot_anode_interface.py \
      --json db/properties/anode_interface_b2o3.json \
      --out docs/figures/oxidation/b2o3_anode_interface.png
"""
import argparse, json, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LEAKY_EV = 2.0
COLORS = {"b2o3": "#c0392b", "LPSCl1.6": "#2c7fb8"}      # doped red / undoped blue
LABELS = {"b2o3": "B₂O₃-doped", "LPSCl1.6": "undoped LPSCl1.6"}


def limiting_phase(info):
    """phase that sets the min gap, e.g. 'LiB(0.0)' -> 'LiB'."""
    leaky = info.get("leaky_products") or []
    mn = info.get("min_product_gap_eV")
    for tok in leaky:
        m = re.match(r"([A-Za-z0-9]+)\(([-0-9.]+)\)", tok)
        if m and abs(float(m.group(2)) - (mn if mn is not None else 1e9)) < 1e-6:
            return m.group(1)
    return (leaky[0].split("(")[0] if leaky else "—")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="db/properties/anode_interface_b2o3.json")
    ap.add_argument("--out", default="docs/figures/oxidation/b2o3_anode_interface.png")
    A = ap.parse_args()
    d = json.loads(Path(A.json).read_text())
    res = d["results"]

    # anode voltage keys present in the json, sorted (Li metal first)
    vkeys = sorted({v for r in res.values() for v in r.get("by_anode", {})}, key=float)
    anode_name = {}
    for r in res.values():
        for vk, info in r.get("by_anode", {}).items():
            anode_name[vk] = info.get("anode", f"{vk} V")
    xlab = [f"{anode_name[vk]}\n({float(vk):.2f} V)" for vk in vkeys]

    systems = [s for s in ("b2o3", "LPSCl1.6") if s in res] + \
              [s for s in res if s not in ("b2o3", "LPSCl1.6")]
    x = np.arange(len(vkeys)); w = 0.8 / max(1, len(systems))

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for si, sysid in enumerate(systems):
        ba = res[sysid].get("by_anode", {})
        gaps = [ba.get(vk, {}).get("min_product_gap_eV") for vk in vkeys]
        xs = x + (si - (len(systems) - 1) / 2) * w
        bars = ax.bar(xs, [g if g is not None else 0 for g in gaps], w,
                      color=COLORS.get(sysid, "#888"), label=LABELS.get(sysid, sysid),
                      edgecolor="black", linewidth=0.6, zorder=3)
        for xb, vk, g in zip(xs, vkeys, gaps):
            if g is None:
                continue
            ph = limiting_phase(ba.get(vk, {}))
            metal = (g < 0.05)
            ax.annotate(f"{ph}\n{g:.2f} eV", (xb, g), textcoords="offset points",
                        xytext=(0, 4), ha="center", va="bottom", fontsize=8.5,
                        fontweight="bold" if metal else "normal",
                        color="#7b241c" if metal else "black")

    ax.axhspan(0, LEAKY_EV, color="#e74c3c", alpha=0.07, zorder=0)
    ax.axhline(LEAKY_EV, ls="--", lw=1.2, color="#c0392b", zorder=2)
    ax.text(np.mean(x), LEAKY_EV + 0.05, "leaky < 2 eV (electron-conducting)",
            ha="center", va="bottom", fontsize=8.5, color="#c0392b")
    ax.set_xticks(x); ax.set_xticklabels(xlab)
    ax.set_ylabel("min interphase band gap (eV)")
    ax.set_title("Anode reduction-interphase passivation (open-Li, MP gaps)\n"
                 "metallic LiB is bare-Li-metal-specific; Li-In avoids it", fontsize=10.5)
    ax.set_ylim(0, max(2.4, ax.get_ylim()[1] + 0.3))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.grid(axis="y", ls=":", alpha=0.4, zorder=0)
    fig.tight_layout()
    Path(A.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(A.out, dpi=200)
    print(f"-> {A.out}")


if __name__ == "__main__":
    main()
