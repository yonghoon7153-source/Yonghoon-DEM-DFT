"""House figure style for the whole campaign — import at the top of every figure script.

    from tools.figures.house_style import INK, MUT, ELEM, GAPBAND, GAPLINE, apply_axes
    (or: import sys; sys.path.append(<repo>); ...)

Conventions locked 2026-07 (LPSOCl/b2o3 standard-DOS figure family):
- English labels only (user's viewer breaks on Korean).
- Element palette validated (lime<->sienna needs direct labels for CVD).
- Every data figure also exports an Origin-ready CSV into db/properties/.
"""

INK = "#1f2937"   # main line / text
MUT = "#6b7280"   # muted text / ticks

# element palette (validated 2026-07)
ELEM = {
    "Li": "#0d9488",  # teal
    "P":  "#7c3aed",  # violet
    "S":  "#c05621",  # sienna
    "Cl": "#65a30d",  # lime  (use direct labels next to lines: lime vs sienna CVD)
    "O":  "#be123c",  # crimson (dopant O -> bold lw ~2.6)
    "B":  "#0284c7",  # sky    (dopant B -> bold)
    "N":  "#2563eb",  # blue
}

# system colors for cross-system comparisons
SYS = {"modelc": "#6b7280", "lpsocl": "#be123c", "b2o3": "#0284c7", "comp1": "#9ca3af"}

# 계 표시명 — **한 가지로 통일** (2026-08-06 결정, 미뤄두던 항목을 닫음).
#   그림마다 LPSOCl / LPSOCl1.6 / "LPSOCl (Li27P5S21OCl8)" 로 갈려 있었다.
#   db/properties (hops_per_ion.csv, bv_path_segments_lpsocl.csv …)가 이미 `LPSOCl1.6` 이므로
#   **데이터 쪽에 맞춘다** — 그래야 CSV 열 이름과 그림 범례가 같은 말을 한다.
#   규칙: 계를 **비교**하는 그림은 아래 DISP 를 그대로 쓴다 (LPSCl1.6 / B2O3@LPSCl1.6 / …).
#         한 계만 다루면서 **조성식 자체가 요점**인 그림(ELF·COHP)은 DISP_LONG 을 쓴다.
DISP = {"modelc": "LPSCl1.6", "lpsocl": "LPSOCl1.6",
        "b2o3": "B2O3@LPSCl1.6", "comp1": "comp1"}
DISP_LONG = {"modelc": "LPSCl1.6 (Li$_{27}$P$_5$S$_{22}$Cl$_8$)",
             "lpsocl": "LPSOCl1.6 (Li$_{27}$P$_5$S$_{21}$OCl$_8$)",
             "b2o3": "B$_2$O$_3$@LPSCl1.6", "comp1": "comp1 (Li$_6$PS$_5$Cl)"}

GAPBAND = "#fef9c3"   # band-gap span fill
GAPLINE = "#2563eb"   # VBM/CBM dashed verticals (ls="--")
GAPTEXT = "#92400e"   # gap label text


def apply_axes(ax, xlabel=None, ylabel=None, title=None, fontsize=12):
    """Standard axis dressing: no top/right spines, muted ticks, INK labels."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize, color=INK)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize, color=INK)
    if title:
        ax.set_title(title, fontsize=fontsize + 0.5, color=INK)
    return ax


def gap_band(ax, vbm=0.0, cbm=None, gap=None, label=True, y=None, fontsize=12):
    """Eigenvalue band-gap band + dashed VBM/CBM lines on an E-E_VBM axis."""
    hi = cbm if cbm is not None else (vbm + gap)
    ax.axvspan(vbm, hi, color=GAPBAND, zorder=0)
    ax.axvline(vbm, color=GAPLINE, ls="--", lw=1.3)
    ax.axvline(hi, color=GAPLINE, ls="--", lw=1.3)
    if label:
        yy = y if y is not None else ax.get_ylim()[1] * 0.8
        ax.text((vbm + hi) / 2, yy, f"gap {hi - vbm:.3f} eV", ha="center",
                fontsize=fontsize, color=GAPTEXT, fontweight="bold")
    return ax
