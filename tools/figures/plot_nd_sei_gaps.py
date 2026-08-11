#!/usr/bin/env python3
"""plot_nd_sei_gaps.py — SEI/decomposition product band gaps (Materials Project)
for the Nd2O3-doped LPSCl1.6 story, framed around the O EFFECT:
O makes wide-gap insulating passivators (Li3PO4, Li2O) vs the conductive
leak products (Li3P, Li2S, polysulfide) that form without O.
⚠ 2026-08-11 — Nd 7종 값을 **하드코딩에서 db/properties/nd_gap_reference_mp.json 으로** 옮겼다.
   하드코딩본은 준안정 '예측만' 다형체를 물고 있었다:
     NdPO$_4$  5.55 = mp-1103387 (제논타임형, hull +0.018, theoretical) → **5.679 = mp-3584 (모나자이트)**
     Nd$_2$S$_3$ 1.79 = mp-32586 (I-42d, hull +0.020, theoretical)      → **0.760 = mp-438 (Pnma)**
   Nd 는 모나자이트·α-사방정이 관측 바닥상이다. 값이 어디서 왔는지 그림에 material_id 로 박는다.
   ⚠ Nd$_2$S$_3$ 가 1.79 → 0.76 으로 내려가면 '한계(2–4 eV)'가 아니라 **전도성 누설(<2 eV)** 구간이다.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__) or ".", "..", ".."))
REF = os.path.join(ROOT, "db", "properties", "nd_gap_reference_mp.json")

# Nd 미포함 상 — sei_product_gaps.py (MP) 유래. (label, gap_eV, contains_O)
NON_ND = [
    ("LiCl",         6.65, False),
    ("Li$_3$PO$_4$", 5.73, True),
    ("Li$_2$O",      5.24, True),
    ("Li$_2$S",      3.90, False),
    ("Li$_3$P",      0.70, False),
]
#: Nd 상의 표시 라벨과 O 포함 여부 (값·material_id 는 JSON 에서 읽는다)
ND_META = {
    "NdPO4":   ("NdPO$_4$",    True),
    "NdOCl":   ("NdOCl",       True),
    "NdCl3":   ("NdCl$_3$",    False),
    "LiNdO2":  ("LiNdO$_2$",   True),
    "Nd2O3":   ("Nd$_2$O$_3$", True),
    "Nd2S3":   ("Nd$_2$S$_3$", False),
    "NdS":     ("NdS",         False),
}

if not os.path.isfile(REF):
    sys.exit(f"⛔ {REF} 이 없다 — **판정 아님**. gabia 에서 회수해 등재할 것.\n"
             "   (하드코딩으로 되돌리지 말 것: 그 값들이 준안정 예측 다형체를 물고 있었다)")
ref = json.load(open(REF, encoding="utf-8"))["phases"]

# (label, gap_eV, contains_O, is_nd, mp_id)
DATA = [(lb, g, o, False, None) for lb, g, o in NON_ND]
for key, (lb, has_o) in ND_META.items():
    if key not in ref:
        sys.exit(f"⛔ {key} 가 {os.path.basename(REF)} 에 없다 — 그림을 반쪽으로 그리지 않는다")
    p = ref[key]
    DATA.append((lb, round(float(p["band_gap_eV"]), 3), has_o, True, p["material_id"]))
DATA.sort(key=lambda r: r[1])  # ascending -> conductive at bottom

print("Nd 상 출처 (그림에 박히는 값):")
for lb, g, _o, is_nd, mid in DATA:
    if is_nd:
        p = next(v for v in ref.values() if v["material_id"] == mid)
        print(f"   {lb:14s} {g:6.3f} eV  {mid:12s} {p['spacegroup']:8s} "
              f"hull {p['e_above_hull']:.4f}{'  ⚠예측만' if p.get('theoretical') else ''}")

labels = [d[0] for d in DATA]
gaps   = [d[1] for d in DATA]

def color(g):
    if g >= 4.0:  return "#3a9e54"   # insulator -> passivation (green)
    if g >= 2.0:  return "#e0a13a"   # marginal (amber)
    return "#c0392b"                 # conductive leak (red)

cols = [color(g) for g in gaps]

fig, ax = plt.subplots(figsize=(8.6, 5.4))
y = range(len(labels))
bars = ax.barh(list(y), gaps, color=cols, edgecolor="black", lw=0.6, zorder=3)

# O-derived -> blue outline + (O) tag · Nd 상은 material_id 를 같이 박는다
for i, d in enumerate(DATA):
    if d[2]:
        bars[i].set_edgecolor("#1f4fb0"); bars[i].set_linewidth(2.2)
    tag = "  *" if d[3] else ""        # Nd lower-bound marker
    ax.text(d[1] + 0.08, i, f"{d[1]:.2f}{tag}", va="center", ha="left",
            fontsize=8.5, fontweight="bold" if d[2] else "normal")
    if d[4]:                           # 값의 출처를 그림에서 바로 읽을 수 있게
        ax.text(0.12, i, d[4], va="center", ha="left", fontsize=6.4,
                color="white", zorder=4)

ax.set_yticks(list(y)); ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("band gap (eV, Materials Project)", fontsize=11)
ax.set_xlim(0, 7.6)
ax.axvline(2.0, ls="--", lw=1, color="0.4")
ax.text(2.0, len(labels)-0.3, "  conductive-leak threshold (~2 eV)",
        color="0.35", fontsize=8, va="top")
ax.set_title("SEI / decomposition-product band gaps — the O effect\n"
             "O makes wide-gap passivators (Li$_3$PO$_4$ 5.73, Li$_2$O 5.24); "
             "without O → conductive leak (Li$_3$P, Li$_2$S)",
             fontsize=10.5, fontweight="bold")

legend = [
    Patch(fc="#3a9e54", ec="black", label="insulator ≥4 eV → passivation"),
    Patch(fc="#e0a13a", ec="black", label="marginal 2–4 eV"),
    Patch(fc="#c0392b", ec="black", label="conductive <2 eV → e⁻ leak"),
    Patch(fc="white",  ec="#1f4fb0", lw=2.2, label="O-derived phase"),
]
ax.legend(handles=legend, loc="lower right", fontsize=8.5, framealpha=0.95)
ax.text(0.99, 0.02, "* Nd-containing = MP lower bound (4f) · mp-id shown in bar\n"
                    "source: db/properties/nd_gap_reference_mp.json (observed ground states)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="0.5")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)

import os
out = os.path.join(os.path.dirname(__file__) or ".", "../../docs/figures/nd_sei/sei_product_gaps_O")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
fig.tight_layout()
fig.savefig(out + ".png", dpi=300, bbox_inches="tight")
fig.savefig(out + ".pdf", bbox_inches="tight")
print("saved:", os.path.abspath(out) + ".png / .pdf")
