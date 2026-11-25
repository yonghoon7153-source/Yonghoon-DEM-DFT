#!/usr/bin/env python3
"""LPSOCl (O-doped LPSCl1.6) at V0 — standard-style DOS/PDOS figures.
Data: db/properties/lpsocl_dos_smooth.csv (sigma 0.15 eV effective) + lpsocl_pdos_element_smooth.csv (sigma 0.15 eV effective).
2026-09-07: the TOTAL DOS was still at base sigma 0.05 while the PDOS had been re-smoothed to 0.15 on 2026-08-04 —
the panels did not match. Both are now 0.15. Originals kept as *_sigma005.csv.
Gap 2.2309 eV = VBM/CBM eigenvalues 2.3870/4.6179, fixed-occ nscf (03b, k882).
Same figure family as b2o3/fig_b2o3_dos.py. Outputs 2 PNGs into cwd.
"""
import csv
from pathlib import Path
DB = str(Path(__file__).resolve().parents[4] / "db" / "properties") + "/"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUT = "#1f2937", "#6b7280"
GAP = 2.2309
COL = {"Li": "#0d9488", "P": "#7c3aed", "S": "#c05621", "Cl": "#65a30d", "O": "#be123c"}


def _rows(path):
    """`#` 주석줄과 BOM 을 건너뛰고 DictReader 로 넘긴다.

    ⛔ 2026-09-07 — 종전엔 `csv.DictReader(f)` 를 그냥 썼다. lpsocl 총 DOS 파일에
      우연히 주석이 **없어서** 돌아갔을 뿐이고, 같은 가족의 `lpscl16_dos_smooth.csv`
      는 원래 `#` 헤더가 있어 **이 도구로 읽으면 KeyError 로 죽는다.**
      스무딩 이력을 헤더에 적자마자 바로 터졌다 — 주석은 예외가 아니라 관례다.
    """
    with open(path, encoding="utf-8-sig") as f:
        lines = [ln for ln in f if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))

E, D = [], []
for r in _rows(DB + "lpsocl_dos_smooth.csv"):
    E.append(float(r["E_minus_VBM"])); D.append(float(r["total_DOS"]))

# ── 1) total DOS ──
fig, ax = plt.subplots(figsize=(8.6, 5.4))
fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
ax.fill_between(E, D, color="#e5e7eb", alpha=0.8)
ax.plot(E, D, color=INK, lw=1.8)
ax.axvspan(0, GAP, color="#fef9c3", zorder=0)
ax.axvline(0, color="#2563eb", ls="--", lw=1.4)
ax.axvline(GAP, color="#2563eb", ls="--", lw=1.4)
ax.text(GAP/2, 88, "gap 2.231 eV", ha="center", fontsize=12, color="#92400e", fontweight="bold")
ax.text(GAP/2, 79, "(VBM/CBM eigenvalues,\nfixed-occ nscf)", ha="center", fontsize=8.5, color="#92400e")
ax.text(GAP/2, 8, "tails inside gap =\nGaussian smoothing\n($\\sigma$ = 0.15 eV) only", ha="center",
        fontsize=7.5, color=MUT, style="italic")
ax.set_xlim(-8, 8); ax.set_ylim(0, 125)
ax.set_xlabel("E $-$ E$_{VBM}$ (eV)", fontsize=12, color=INK)
ax.set_ylabel("DOS (states/eV)", fontsize=12, color=INK)
ax.set_title("LPSOCl (O-doped LPSCl$_{1.6}$) — total DOS (PBE, tetrahedra, V$_0$)", fontsize=12.5, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT)
fig.savefig("lpsocl_dos_total.png", dpi=300)
plt.close(fig)

# ── 2) element PDOS ──
cols = {el: [] for el in COL}
E2 = []
for r in _rows(DB + "lpsocl_pdos_element_smooth.csv"):
    E2.append(float(r["E_minus_VBM"]))
    for el in COL: cols[el].append(float(r[el]))
fig, ax = plt.subplots(figsize=(8.6, 5.4))
fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
ax.axvspan(0, GAP, color="#fef9c3", zorder=0)
ax.axvline(0, color="#2563eb", ls="--", lw=1.2)
ax.axvline(GAP, color="#2563eb", ls="--", lw=1.2)
for el in ("Li", "P", "S", "Cl"):
    ax.plot(E2, cols[el], color=COL[el], lw=1.7)
ax.plot(E2, cols["O"], color=COL["O"], lw=2.6, zorder=5)
lab = {"S": (-0.75, 54), "Cl": (-3.05, 36), "Li": (6.05, 22), "P": (-4.25, 16.5), "O": (-5.25, 6.3)}
for el, (x, y) in lab.items():
    ax.text(x, y, el, color=COL[el], fontsize=12, fontweight="bold", ha="center")
ax.annotate("O 2p buried deep below VBM\n(P–O bonding band) — no O at band edges",
            xy=(-5.15, 3.9), xytext=(-7.7, 30), fontsize=9.5, color=COL["O"],
            arrowprops=dict(arrowstyle="-|>", color=COL["O"], lw=1.2))
ax.text(GAP/2, 51, "gap 2.231 eV", ha="center", fontsize=10.5, color="#92400e", fontweight="bold")
ax.set_xlim(-8, 8); ax.set_ylim(0, 58)
ax.set_xlabel("E $-$ E$_{VBM}$ (eV)", fontsize=12, color=INK)
ax.set_ylabel("PDOS (states/eV)", fontsize=12, color=INK)
ax.set_title("LPSOCl — element-resolved PDOS (PBE, V$_0$)", fontsize=12.5, color=INK)
ax.legend(handles=[plt.Line2D([], [], color=COL[e], lw=2.2, label=e) for e in ("Li","P","S","Cl","O")],
          loc="upper right", frameon=False, fontsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT)
fig.savefig("lpsocl_pdos_elements.png", dpi=300)
print("saved 2 figures")
