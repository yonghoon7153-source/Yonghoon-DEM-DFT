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


# ── 점수 지도용 컬러맵 (2026-08-18) ──────────────────────────────────────────
#  RdYlGn 을 대체한다. 세 가지 이유:
#   ① 채도가 너무 높아 슬라이드에서 촌스럽고, 인쇄하면 초록이 뭉갠다.
#   ② 적록색맹이 양 끝을 못 가른다 — 이 그림은 **양 끝이 곧 메시지**다.
#   ③ 양 끝이 house 색과 무관했다. crimson(#be123c)·teal(#0d9488) 로 맞춘다.
#  ⚠ 낮은 쪽은 **빨강을 유지**한다 — 대본이 "late transition metals sit together
#    in red" 라고 말한다. 색을 바꾸면 대본이 깨진다.
#  ⚠ 2026-08-18 2판 — 1저자 요청으로 **전체를 한 단계 연하게**. 채도를 낮추니
#    모든 칸에서 INK 가 읽혀 흰 글씨가 사라졌다(on_fill 이 알아서 처리한다).
#    낮은 쪽은 여전히 붉게 읽혀야 하므로 색상(hue)은 유지하고 명도만 올렸다.
_SCORE_STOPS = [
    (0.00, "#cf5c72"),   # soft crimson — 낮은 점수 (여전히 '빨간 블록')
    (0.28, "#eeab92"),   # pale terracotta
    (0.50, "#f4ead8"),   # pale sand (중립)
    (0.72, "#9bcbc3"),
    (1.00, "#63b3a9"),   # soft teal — 높은 점수
]


def score_cmap():
    """낮음(crimson) → 중립(sand) → 높음(teal) 발산형 컬러맵."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(
        "bml_score", [(p, c) for p, c in _SCORE_STOPS])


def on_fill(rgba):
    """그 배경 위에 **읽히는** 글자색. 밝으면 INK, 어두우면 흰색.

    ⚠ 2026-08-18 실측 — 앞 판은 칸 색과 무관하게 늘 INK 를 썼다. 그래서 진한
      칸(Sc·Cr·Cu·Gd)의 원소 기호와 점수가 슬라이드에서 안 읽혔다. 밝기 문턱을
      눈대중으로 잡으면 경계에서 또 틀리므로 상대휘도(WCAG)로 계산한다.
      문턱 0.179 는 임의값이 아니라 **흰 글씨와 검은 글씨의 대비가 같아지는 점**이다:
      (L+0.05)² = 1.05×0.05  →  L = 0.179.
    """
    r, g, b = rgba[0], rgba[1], rgba[2]

    def _lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    lum = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
    return "#f8fafc" if lum < 0.179 else INK
