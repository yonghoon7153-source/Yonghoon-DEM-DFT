#!/usr/bin/env python3
"""plot_interface_window_integrated.py — ONE figure unifying the anode (Li metal,
Li-In) and cathode (oxidation) interface stability across the full electrochemical
window, on a single voltage axis.

Unifying metric: the min interphase BAND GAP (eV) of the limiting decomposition
product = electronic leakiness (< 2 eV -> electron-conducting -> non-passivating).
One question, answered from 0 V (Li metal anode) up to cathode charge voltage:
"is the interphase that forms here insulating (passivating) or leaky?"

Data (all real, b2o3):
  * anode reservoir contacts   <- db/properties/anode_interface_b2o3.json
        Li metal 0 V, Li-In 0.62 V (reduction interphase + min gap)
  * SE intrinsic decomposition <- db/properties/b2o3_esw.json (B-product voltages)
        + db/properties/b2o3_sei_gaps.json (product band gaps), toward the cathode.

The SE/SPECIFIC-cathode chemical reactivity (interface_reactivity_v2.py, vs
LiCoO2/NMC811) is a further refinement; this figure is the intrinsic landscape.

  python3 tools/oxidation/plot_interface_window_integrated.py
"""
import argparse, json, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LEAKY = 2.0
DBP = Path(__file__).resolve().parent.parent.parent / "db" / "properties"


def jload(name):
    return json.loads((DBP / name).read_text())


def limiting_from_anode(info):
    """(product, gap) that sets the min gap, parsed from leaky_products like 'LiB(0.0)'."""
    mn = info.get("min_product_gap_eV")
    for tok in info.get("leaky_products") or []:
        m = re.match(r"([A-Za-z0-9]+)\(([-0-9.]+)\)", tok)
        if m and abs(float(m.group(2)) - (mn if mn is not None else 1e9)) < 1e-6:
            return m.group(1), float(m.group(2))
    return ("?", mn if mn is not None else np.nan)


def resolve_gap(prodstr, gaps):
    """map an esw product label ('Li2B2S5 thioborate', 'BCl3/BPO4') to an MP gap."""
    for cand in re.split(r"[/ ]", prodstr):
        cand = cand.strip()
        if cand in gaps:
            return cand, gaps[cand]
    return prodstr.split()[0], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/figures/oxidation/b2o3_interface_window_integrated.png")
    A = ap.parse_args()
    an = jload("anode_interface_b2o3.json")["results"]
    esw = jload("b2o3_esw.json")
    gaps = jload("b2o3_sei_gaps.json")["sei_gaps_MP_eV"]

    # ---- b2o3 series: anode reservoir points + intrinsic decomposition toward cathode
    pts = []   # (V, gap, product, regime)
    for vk, info in sorted(an["b2o3"]["by_anode"].items(), key=lambda kv: float(kv[0])):
        prod, g = limiting_from_anode(info)
        pts.append((float(vk), g, prod, info.get("anode", "anode")))
    for vk, prodstr in esw["b2o3"].get("new_B_reactions", {}).items():
        V = float(vk.split("_")[0])
        prod, g = resolve_gap(prodstr, gaps)
        if g is not None:
            pts.append((V, g, prod, "intrinsic"))
    pts.sort(key=lambda p: p[0])
    Vb, Gb = [p[0] for p in pts], [p[1] for p in pts]

    # undoped anode points (contrast)
    und = [(float(vk), *limiting_from_anode(info))
           for vk, info in sorted(an["LPSCl1.6"]["by_anode"].items(), key=lambda kv: float(kv[0]))]

    fig, ax = plt.subplots(figsize=(10.0, 5.3))
    # passivation bands
    ax.axhspan(0, LEAKY, color="#e74c3c", alpha=0.07)
    ax.axhspan(LEAKY, 9, color="#27ae60", alpha=0.06)
    ax.axhline(LEAKY, ls="--", lw=1.1, color="#c0392b")
    ax.text(4.45, LEAKY + 0.06, "leaky < 2 eV (electron-conducting)", ha="right",
            va="bottom", fontsize=8.5, color="#c0392b")
    # intrinsic stable window shading
    rv, ov = esw["b2o3"]["reduction_V"], esw["b2o3"]["oxidation_V"]
    ax.axvspan(rv, ov, color="#7f8c8d", alpha=0.12)
    ax.text((rv + ov) / 2, 8.4, f"intrinsic ESW\n{rv:.2f}–{ov:.2f} V (0.31)", ha="center",
            va="top", fontsize=8, color="#34495e")

    # b2o3 connecting step + colored points
    ax.plot(Vb, Gb, "-", color="#999", lw=1.0, zorder=2)
    for V, g, prod, reg in pts:
        c = "#27ae60" if g >= LEAKY else "#c0392b"
        mk = "o" if reg != "intrinsic" else "D"
        ax.scatter([V], [g], s=85, color=c, edgecolor="black", lw=0.7, marker=mk, zorder=4)
        dy = 0.28 if g < 6 else -0.5
        ax.annotate(f"{prod}\n{g:.2f}", (V, g), textcoords="offset points",
                    xytext=(0, 10 if dy > 0 else -22), ha="center",
                    va="bottom" if dy > 0 else "top", fontsize=8.6,
                    fontweight="bold" if g < LEAKY else "normal", color=c)
    # undoped anode contrast (open markers)
    for V, prod, g in und:
        ax.scatter([V], [g], s=70, facecolor="white", edgecolor="#2c7fb8", lw=1.6,
                   marker="s", zorder=3)
    ax.scatter([], [], s=70, facecolor="white", edgecolor="#2c7fb8", lw=1.6, marker="s",
               label="undoped LPSCl1.6 (anode)")
    ax.scatter([], [], s=85, color="#888", edgecolor="black", marker="o", label="b2o3 anode reservoir (Li metal, Li-In)")
    ax.scatter([], [], s=85, color="#888", edgecolor="black", marker="D", label="b2o3 intrinsic decomposition (→ cathode)")

    # anode / cathode zone labels
    ax.annotate("ANODE\n(Li metal, Li-In)", (0.31, 7.4), ha="center", fontsize=9,
                color="#7b241c", fontweight="bold")
    ax.annotate("CATHODE charge →", (3.7, 6.0), ha="center", fontsize=9,
                color="#1a5276", fontweight="bold")

    ax.set_xlim(-0.15, 4.5); ax.set_ylim(-0.3, 9)
    ax.set_xlabel("V vs Li/Li⁺   (0 = Li metal anode  →  ~4.3 = charged cathode)")
    ax.set_ylabel("min interphase band gap (eV)  —  passivating ↑ / leaky ↓")
    ax.set_title("Integrated interface stability across the electrochemical window (B₂O₃-doped)\n"
                 "ANODE side = LIABILITY (LiB 0 @ Li metal → Li₃P 0.7 @ Li-In);  "
                 "CATHODE/oxidation side = PASSIVATED (wide-gap B/O)", fontsize=10.5)
    ax.legend(loc="center left", fontsize=8.3, framealpha=0.95)
    ax.grid(axis="y", ls=":", alpha=0.35)
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent.parent / A.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200)
    print(f"-> {A.out}")


if __name__ == "__main__":
    main()
