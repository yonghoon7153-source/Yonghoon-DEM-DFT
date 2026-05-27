#!/usr/bin/env python3
"""
Generate comparison plots from multiple DEM analysis cases.

Usage:
    python generate_comparison_plots.py \
        -i case1/full_metrics.json case2/full_metrics.json \
        -n "post_real_7" "post_real_8" \
        -o ./figures \
        -p porosity am_se_interface se_se_tradeoff se_se_total \
           percolation_tortuosity ionic_active coverage four_panel
"""

import argparse
import csv
import itertools
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _register_cjk_fallback():
    """Register a Korean-capable font so Hangul in titles/labels renders instead
    of tofu boxes.  Searches Linux, WSL-mounted Windows, and macOS locations and
    sets it as the PRIMARY sans-serif (Korean fonts carry Latin glyphs too, so
    the look stays clean and Hangul is guaranteed regardless of mpl fallback)."""
    from matplotlib import font_manager as _fm
    import os as _os, glob as _glob
    candidates = [
        '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf',
        '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
        '/mnt/c/Windows/Fonts/malgun.ttf',     # WSL → Windows Malgun Gothic
        '/mnt/c/Windows/Fonts/malgunbd.ttf',
        '/mnt/c/Windows/Fonts/gulim.ttc',
        '/mnt/c/Windows/Fonts/batang.ttc',
        'C:/Windows/Fonts/malgun.ttf',
        '/Library/Fonts/AppleGothic.ttf',
        '/System/Library/Fonts/AppleSDGothicNeo.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    ]
    for pat in ('/usr/share/fonts/**/*Nanum*.ttf',
                '/usr/share/fonts/**/NotoSansCJK*',
                '/usr/share/fonts/**/NotoSansKR*'):
        candidates += sorted(_glob.glob(pat, recursive=True))
    for path in candidates:
        if path and _os.path.exists(path):
            try:
                _fm.fontManager.addfont(path)
                name = _fm.FontProperties(fname=path).get_name()
                sl = [f for f in matplotlib.rcParams['font.sans-serif'] if f != name]
                matplotlib.rcParams['font.sans-serif'] = [name] + sl
                matplotlib.rcParams['font.family'] = 'sans-serif'
                matplotlib.rcParams['axes.unicode_minus'] = False
                return name
            except Exception:
                continue
    return None


_register_cjk_fallback()

try:                       # grade-axis values (Q/ASR/τ_Laplace/…) for param compare
    import grade_engine as _grade_engine
except Exception:
    _grade_engine = None


# ─── Color palette ────────────────────────────────────────────────────────────
BLUE = "#4472C4"
RED = "#C00000"
GREEN = "#548235"
LIGHT_GREEN = "#A9D18E"
BLACK = "#333333"
GRAY = "#888888"

DPI = 150
FIG_SINGLE = (7, 4.5)
FIG_FOUR = (14, 10)
GROUP_COLORS = ['#6c8cff', '#ff6b6b', '#51cf66', '#ffd43b', '#cc5de8', '#ff922b']


# ─── Helpers ──────────────────────────────────────────────────────────────────

_GROUP_INFO = None  # Set by main()
_Y_MAX_SIGMA = None  # Override y-axis max (mS/cm) for multiscale σ plots; set by main()
_GLOBAL_RGB = None  # (b, ln_k) from global fit across all plot groups
_GLOBAL_C_ION = None  # Fitted C for ionic scaling law (from global/ionic_scaling_fit)
_GLOBAL_FORMX_R2 = None  # (r2, loocv) from FORM X fit
_GLOBAL_IONIC_SIGMOID = None  # (C_thick, C_thin, tau_c, k) for sigmoid C(τ)
_GLOBAL_IONIC_POLY3 = None  # (a0, a1, a2, a3) for poly3 part of v9 BLEND
_GLOBAL_PS_SIGMOID = None   # v19: (k_pf, pc_pf, beta1, beta2, w_pf_mean, pf_t_mean)
_ALL_DATA = None  # all_data for _apply_style auto-detect
_REAL_NAMES = None  # saved case names (args.names), aligned with _ALL_DATA
_FOCUS_CASES = set()  # subset of saved names to show in the "1-1" focus parity
_FOCUS_LABEL = ""     # group name(s) of fully-selected groups, shown on the 1-1 plot
_FIT_CORPUS = []      # full-corpus metrics dicts for global (n=all) fit stats

# Generic parameter-comparison selections (set by main() from CLI args).
_PARAM_X = None       # X-axis metric key (scatter)
_PARAM_Y = None       # Y-axis metric key (scatter)
_PARAM_LIST = None    # list of metric keys (bar / correlation)
_PARAM_NORM = False   # normalize each param to its max (bar)

# Disk cache of the fitted v29 + v32 params. Webapp spawns a separate
# subprocess per plot set, so module globals do not survive across
# calls. Writing the fitted values here lets plot_multiscale_sigma (run
# in a different subprocess) reuse the same v29 that the parity plot
# produced. Keyed by the sorted list of case names so a different case
# selection invalidates stale entries automatically.
import hashlib as _hashlib, tempfile as _tempfile
_V29_CACHE_PATH = os.path.join(_tempfile.gettempdir(), 'dem_v29_v32_cache.json')


def _cases_fingerprint(names):
    """Stable hash of the sorted case-name tuple."""
    return _hashlib.md5(
        ','.join(sorted(str(n) for n in names)).encode('utf-8')
    ).hexdigest()


def _write_v29_cache(names, sigmoid, poly3, ps_sigmoid, v32_gammas=None):
    import json as _json
    name_list = sorted(str(n) for n in names)
    payload = {
        'fingerprint': _cases_fingerprint(names),
        'case_names': name_list,
        'sigmoid':  list(sigmoid),
        'poly3':    list(poly3),
        'ps_sigmoid': list(ps_sigmoid),
        'v32_gammas': dict(v32_gammas) if v32_gammas else None,
    }
    try:
        with open(_V29_CACHE_PATH, 'w') as f:
            _json.dump(payload, f)
        print(f"  [v29 cache] wrote {_V29_CACHE_PATH}  fp={payload['fingerprint'][:8]}  n={len(name_list)}")
    except Exception as e:
        print(f"  [v29 cache] write failed: {e}")


def _load_v29_cache(names):
    """Return (sigmoid, poly3, ps_sigmoid, v32_gammas) if cache covers current
    case list (exact match OR current names are a subset of cached names),
    else None. Subset match handles the webapp's multi-POST flow where the
    parity plot fits on ALL groups and each per-group POST requests only
    its own subset — they should still use the common fitted params."""
    import json as _json
    if not os.path.exists(_V29_CACHE_PATH):
        return None
    try:
        p = _json.load(open(_V29_CACHE_PATH))
    except Exception:
        return None
    cached_names = set(p.get('case_names', []))
    cur = set(str(n) for n in names)
    exact = p.get('fingerprint') == _cases_fingerprint(names)
    subset = bool(cached_names) and cur.issubset(cached_names)
    if not (exact or subset):
        print(f"  [v29 cache] miss (cur={len(cur)} cases, cached={len(cached_names)}; "
              f"not a subset)")
        return None
    tag = 'exact' if exact else f'subset {len(cur)}⊆{len(cached_names)}'
    print(f"  [v29 cache] hit [{tag}]  fp={p.get('fingerprint','?')[:8]}")
    return (tuple(p.get('sigmoid', [])),
            tuple(p.get('poly3', [])),
            tuple(p.get('ps_sigmoid', [])),
            p.get('v32_gammas'))

def _apply_style(ax, ylabel, names, data_list=None):
    """Apply common academic style with group separators.
    Auto-detect monomodal: if all P:S are same, use AM:SE as x-axis."""
    n = len(names)
    ax.set_xticks(range(n))

    # Check if all names (P:S) are the same → monomodal, use AM:SE instead
    x_labels = list(names)
    x_title = "P:S Configuration"
    if data_list is None:
        data_list = _ALL_DATA
    unique_names = set(names)
    if len(unique_names) == 1 and data_list is not None:
        # All P:S same → show AM:SE ratio instead
        am_se_labels = []
        for d in data_list:
            am_se = _get(d, 'am_se_ratio', '')
            if not am_se:
                phi_am = _get(d, 'phi_am', 0)
                phi_se = _get(d, 'phi_se', 0)
                if phi_am > 0 and phi_se > 0:
                    # Mass ratio (density-weighted): NCM=4800, LPSCl=2000 kg/m³
                    am_mass = phi_am * 4800
                    se_mass = phi_se * 2000
                    am_pct = round(am_mass / (am_mass + se_mass) * 100)  # nearest 1%
                    am_se = f"{am_pct:.0f}:{100-am_pct:.0f}"
            am_se_labels.append(str(am_se) if am_se else '?')
        if any(l != '?' for l in am_se_labels):
            x_labels = am_se_labels
            x_title = f"AM:SE Ratio (P:S={names[0]})"

    # Adaptive x-axis label sizing
    if n <= 8:
        ax.set_xticklabels(x_labels, fontsize=10)
    elif n <= 15:
        ax.set_xticklabels(x_labels, fontsize=8, rotation=45, ha='right')
    else:
        ax.set_xticklabels(x_labels, fontsize=7, rotation=45, ha='right')

    ax.set_xlabel(x_title, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.4, color="#CCCCCC", alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis='both', labelsize=9 if n <= 8 else 7)

    # Bottom margin for rotated labels
    if n > 8:
        ax.figure.subplots_adjust(bottom=0.18)

    # Add group separators and break lines at boundaries
    if _GROUP_INFO:
        sizes, gnames = _GROUP_INFO
        n_total = sum(sizes)
        # Break existing lines at group boundaries
        boundaries = []
        pos = 0
        for sz in sizes[:-1]:
            pos += sz
            boundaries.append(pos - 0.5)
        # Draw separators and labels
        pos = 0
        for gi, sz in enumerate(sizes):
            if gi > 0:
                ax.axvline(pos - 0.5, color='#888888', linestyle='--', linewidth=1, alpha=0.6)
            mid = pos + sz / 2 - 0.5
            # Staggered group labels: odd groups lower
            if n > 8:
                label_y = -0.26 if gi % 2 == 0 else -0.36
            else:
                label_y = -0.18
            label_fs = 7 if n > 15 else 8 if n > 8 else 9
            ax.text(mid, label_y, gnames[gi], ha='center', va='top',
                    transform=ax.get_xaxis_transform(),
                    fontsize=label_fs, fontweight='bold', color=GROUP_COLORS[gi % len(GROUP_COLORS)],
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=GROUP_COLORS[gi % len(GROUP_COLORS)], alpha=0.8))
            pos += sz


def _marker_size(n):
    """Adaptive marker size based on case count."""
    if n <= 8: return 10
    if n <= 15: return 7
    return 5

def _line_width(n):
    """Adaptive line width based on case count."""
    if n <= 8: return 2.5
    if n <= 15: return 2.0
    return 1.5

def _group_break_data(xs, ys):
    """Insert NaN at group boundaries so matplotlib breaks the line."""
    if not _GROUP_INFO:
        return xs, ys
    sizes = _GROUP_INFO[0]
    new_x, new_y = [], []
    pos = 0
    for gi, sz in enumerate(sizes):
        if gi > 0:
            new_x.append(float('nan'))
            new_y.append(float('nan'))
        for i in range(pos, pos + sz):
            if i < len(xs):
                new_x.append(xs[i] if not isinstance(xs, np.ndarray) else float(xs[i]))
                new_y.append(ys[i] if not isinstance(ys, np.ndarray) else float(ys[i]))
        pos += sz
    return new_x, new_y


def _break_lines_at_groups(fig):
    """Insert NaN at group boundaries for all lines in all axes."""
    if not _GROUP_INFO:
        return
    sizes = _GROUP_INFO[0]
    n_total = sum(sizes)
    for ax in fig.get_axes():
        for line in ax.get_lines():
            xd = line.get_xdata()
            yd = line.get_ydata()
            # Only process data lines (not grid, axvline, etc.)
            if len(xd) != n_total or not line.get_marker() or line.get_marker() == 'None':
                continue
            if True:
                new_x, new_y = [], []
                idx = 0
                for gi, sz in enumerate(sizes):
                    if gi > 0:
                        new_x.append(float('nan'))
                        new_y.append(float('nan'))
                    for j in range(sz):
                        if idx < len(xd):
                            new_x.append(float(xd[idx]))
                            new_y.append(float(yd[idx]))
                            idx += 1
                line.set_xdata(new_x)
                line.set_ydata(new_y)


def _save(fig, outdir, fname):
    _break_lines_at_groups(fig)
    fig.tight_layout(pad=1.5)
    fig.subplots_adjust(right=0.85, bottom=0.22 if _GROUP_INFO else 0.15)
    path = os.path.join(outdir, fname)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor='white', pad_inches=0.2)
    plt.close(fig)
    return path


def _focus_parity(outdir, file_base, sig_act, sig_pred, kept_names,
                  xlabel, ylabel, title):
    """"1-1" view: if _FOCUS_CASES is set, render <file_base>_focus.png with the
    SAME fit (1:1 + ±20% band + axis limits derived from the full set), but only
    the selected sample points.  The global fit is reused unchanged — this only
    filters which points are drawn.  Returns the path or None."""
    if not _FOCUS_CASES:
        return None
    sig_act = np.asarray(sig_act, float); sig_pred = np.asarray(sig_pred, float)
    foc = np.array([(nm in _FOCUS_CASES) for nm in kept_names])
    if not foc.any():
        print(f"  [SKIP] {file_base}_focus: none of the selected samples are in this fit")
        return None
    lim = [min(sig_act.min(), sig_pred.min())*0.8,
           max(sig_act.max(), sig_pred.max())*1.2]
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.plot(lim, lim, '--', color=GRAY, label='1:1')
    ax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                    color=GREEN, alpha=0.12, label='±20%')
    ax.scatter(sig_act[foc], sig_pred[foc], s=75, c=ORANGE,
               edgecolors='black', zorder=4, label='선택 샘플')
    for i in np.where(foc)[0]:
        ax.annotate(str(kept_names[i]), (sig_act[i], sig_pred[i]), fontsize=6,
                    color='#333333', xytext=(4, 3), textcoords='offset points')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if _FOCUS_LABEL:
        title = title + "\n그룹: " + _FOCUS_LABEL
    ax.set_title(title, fontsize=8)
    ax.legend(fontsize=8, loc='upper left'); ax.grid(True, alpha=0.25, which='both')
    return _save(fig, outdir, file_base + "_focus.png")


def _get(data, key, default=0.0):
    v = data.get(key, default)
    if v is None:
        return default
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def _write_csv(outdir, fname, headers, names, *columns):
    """Write comparison CSV with case names and data columns."""
    import csv
    with open(os.path.join(outdir, fname), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Case'] + headers)
        for i, name in enumerate(names):
            row = [name] + [c[i] if i < len(c) else '' for c in columns]
            w.writerow(row)


def _resolve_am_se(d):
    """Standard: AM-SE → P:S에 맞게 AM_P-SE or AM_S-SE로 분배."""
    am_p = _get(d, "area_AM_P_SE_total")
    am_s = _get(d, "area_AM_S_SE_total")
    if am_p == 0 and am_s == 0:
        total = _get(d, "area_AM_SE_total") or _get(d, "area_AM전체_SE_total")
        ps = d.get("ps_ratio", "")
        if ps in ("P only", "10:0"):
            return total, 0
        else:
            return 0, total
    return am_p, am_s


def _resolve_coverage(d):
    """Standard: coverage_AM → P/S에 맞게 분배."""
    cov_p = _get(d, "coverage_AM_P_mean")
    cov_s = _get(d, "coverage_AM_S_mean")
    std_p = _get(d, "coverage_AM_P_std")
    std_s = _get(d, "coverage_AM_S_std")
    if cov_p == 0 and cov_s == 0:
        cov = _get(d, "coverage_AM_mean")
        std = _get(d, "coverage_AM_std")
        ps = d.get("ps_ratio", "")
        if ps in ("P only", "10:0"):
            return cov, std, 0, 0
        else:
            return 0, 0, cov, std
    return cov_p, std_p, cov_s, std_s


# ─── Individual plot functions ────────────────────────────────────────────────

def plot_porosity(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = list(range(len(names)))
    ys = [_get(d, "porosity") for d in all_data]
    ax.plot(xs, ys, marker="s", markersize=9, color=BLACK, linewidth=1.5,
            markerfacecolor=BLACK, markeredgecolor=BLACK, zorder=3)
    # y range with padding
    if ys:
        ymin, ymax = min(ys), max(ys)
        pad = max((ymax - ymin) * 0.15, 0.5)
        ax.set_ylim(ymin - pad, ymax + pad)
    _apply_style(ax, "Porosity (%)", names)
    ax.set_title("Porosity", fontsize=13, fontweight="bold", pad=10)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_am_se_interface(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = np.arange(len(names))
    width = 0.5

    resolved = [_resolve_am_se(d) for d in all_data]
    am_p = [r[0] for r in resolved]
    am_s = [r[1] for r in resolved]

    ax.bar(xs, am_p, width, label="AM_P-SE", color=GREEN, zorder=3)
    ax.bar(xs, am_s, width, bottom=am_p, label="AM_S-SE",
           color=LIGHT_GREEN, zorder=3)
    ax.legend(fontsize=10, frameon=False)

    _apply_style(ax, "Interface Area (μm²)", names)
    ax.set_title("AM-SE Interface Area", fontsize=13, fontweight="bold", pad=10)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_se_se_tradeoff(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)

    xs = np.arange(len(names))
    width = 0.5
    counts = [_get(d, "area_SE_SE_n") for d in all_data]
    means = [_get(d, "area_SE_SE_mean") for d in all_data]

    ax.bar(xs, counts, width, color=BLUE, alpha=0.75, zorder=3, label="Contact Count")
    _apply_style(ax, "SE-SE Contact Count", names)
    ax.set_title("SE-SE Contact: Count vs Mean Area", fontsize=13, fontweight="bold", pad=10)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.legend(loc="upper left", fontsize=9, frameon=False)

    ax2 = ax.twinx()
    ax2.plot(xs, means, marker="s", color=RED, linewidth=2, markersize=8,
             zorder=4, label="Mean Area")
    ax2.set_ylabel("Mean Contact Area (μm²)", fontsize=11, color=RED)
    ax2.tick_params(axis="y", labelcolor=RED, labelsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.legend(loc="upper right", fontsize=9, frameon=False)

    if standalone:
        return _save(fig, "", "")
    return ax


def plot_se_se_total(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = list(range(len(names)))
    ys = [_get(d, "area_SE_SE_total") for d in all_data]
    ax.plot(xs, ys, marker="s", color=GRAY, linewidth=1.5, markersize=8, zorder=3,
            markerfacecolor=GRAY, markeredgecolor=GRAY)

    if ys:
        idx_max = int(np.argmax(ys))
        ax.annotate(f"max: {ys[idx_max]:,.0f}",
                    xy=(idx_max, ys[idx_max]),
                    xytext=(15, 10), textcoords="offset points",
                    fontsize=10, ha="left", color=RED, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
        ymin, ymax = min(ys), max(ys)
        pad = max((ymax - ymin) * 0.15, 100)
        ax.set_ylim(ymin - pad, ymax + pad)

    _apply_style(ax, "SE-SE Total Contact Area (μm²)", names)
    ax.set_title("SE-SE Total Contact Area", fontsize=13, fontweight="bold", pad=10)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_percolation_tortuosity(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)

    xs = list(range(len(names)))
    perc = [_get(d, "percolation_pct") for d in all_data]
    top_reach = [_get(d, "top_reachable_pct") for d in all_data]
    tort = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean")) for d in all_data]

    ax.plot(xs, perc, marker="s", color=BLUE, linewidth=2, markersize=8,
            zorder=3, label="Percolation %")
    ax.plot(xs, top_reach, marker="D", color="#00B0F0", linewidth=1.5, markersize=7,
            linestyle="--", zorder=3, label="Top Reachable %")
    _apply_style(ax, "SE Connectivity (%)", names)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_title("Percolation / Top Reachable & Tortuosity", fontsize=13, fontweight="bold", pad=10)
    ax.legend(loc="center left", fontsize=8, frameon=False)

    ax2 = ax.twinx()
    ax2.plot(xs, tort, marker="^", color=RED, linewidth=2, markersize=9,
             zorder=4, label="Tortuosity")
    ax2.set_ylabel("Tortuosity", fontsize=11, color=RED)
    ax2.tick_params(axis="y", labelcolor=RED, labelsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.legend(loc="center right", fontsize=9, frameon=False)

    if standalone:
        return _save(fig, "", "")
    return ax


def plot_ionic_active(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = list(range(len(names)))
    ys = [_get(d, "ionic_active_pct") for d in all_data]

    # Fill per group to avoid cross-group shading
    if _GROUP_INFO and len(_GROUP_INFO[0]) > 1:
        sizes = _GROUP_INFO[0]
        pos = 0
        for gi, sz in enumerate(sizes):
            gx = xs[pos:pos+sz]
            gy = ys[pos:pos+sz]
            ax.plot(gx, gy, marker="o", color=GREEN, linewidth=2, markersize=9, zorder=3)
            ax.fill_between(gx, gy, 100, color=RED, alpha=0.12, label="Dead zone" if gi == 0 else None)
            ax.fill_between(gx, 0, gy, color=GREEN, alpha=0.12, label="Active zone" if gi == 0 else None)
            pos += sz
    else:
        ax.plot(xs, ys, marker="o", color=GREEN, linewidth=2, markersize=9, zorder=3)
        ax.fill_between(xs, ys, 100, color=RED, alpha=0.12, label="Dead zone")
        ax.fill_between(xs, 0, ys, color=GREEN, alpha=0.12, label="Active zone")
    if ys:
        ymin = max(min(ys) - 3, 0)
        ax.set_ylim(ymin, 101)
    _apply_style(ax, "Ionic Active AM (%)", names)
    ax.set_title("Ionic Active AM Fraction", fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=9, frameon=False, loc="lower left")
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_coverage(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)

    xs = np.arange(len(names))
    width = 0.3

    resolved = [_resolve_coverage(d) for d in all_data]
    mean_p = [r[0] for r in resolved]
    std_p = [r[1] for r in resolved]
    mean_s = [r[2] for r in resolved]
    std_s = [r[3] for r in resolved]

    # Only plot bars where values > 0
    has_p = any(v > 0 for v in mean_p)
    has_s = any(v > 0 for v in mean_s)

    if has_p:
        ax.bar(xs - width / 2, mean_p, width, yerr=std_p, capsize=4,
               color=GREEN, label="AM_P", zorder=3, error_kw=dict(lw=1.2))
    if has_s:
        ax.bar(xs + width / 2, mean_s, width, yerr=std_s, capsize=4,
               color=LIGHT_GREEN, label="AM_S", zorder=3, error_kw=dict(lw=1.2))

    _apply_style(ax, "Coverage (%)", names)
    ax.set_title("AM Coverage (P vs S)", fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=10, frameon=False)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_stress_cv(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = list(range(len(names)))
    ys = [_get(d, "stress_cv") for d in all_data]
    ax.plot(xs, ys, marker="s", markersize=9, color=BLACK, linewidth=1.5, zorder=3)
    if ys:
        ymin, ymax = min(ys), max(ys)
        pad = max((ymax - ymin) * 0.15, 1)
        ax.set_ylim(ymin - pad, ymax + pad)
    _apply_style(ax, "Von Mises CV (%)", names)
    ax.set_title("Stress Distribution Uniformity", fontsize=13, fontweight="bold", pad=10)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_stress_ratio(all_data, names, ax=None):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)
    xs = list(range(len(names)))

    type_keys = ['AM_P', 'AM_S', 'SE']
    colors = {'AM_P': RED, 'AM_S': '#FF8C00', 'SE': GREEN}
    markers = {'AM_P': 's', 'AM_S': 'o', 'SE': '^'}

    for tk in type_keys:
        ys = [_get(d, f"stress_ratio_{tk}") for d in all_data]
        if any(v > 0 for v in ys):
            ax.plot(xs, ys, marker=markers[tk], markersize=8, color=colors[tk],
                    linewidth=1.5, label=tk, zorder=3)

    ax.axhline(y=1.0, color=GRAY, linestyle='--', linewidth=1, alpha=0.5, label='mean')
    _apply_style(ax, "σ / σ_mean", names)
    ax.set_title("Stress Ratio by Type", fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=9, frameon=False)
    if standalone:
        return _save(fig, "", "")
    return ax


def plot_stress_z_layer(all_data, names, ax=None):
    """Z-layer별 stress CV profile (all cases overlaid)."""
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=FIG_SINGLE)

    colors_cycle = [BLUE, RED, GREEN, '#FF8C00', BLACK, '#9467BD']
    for i, d in enumerate(all_data):
        z_data = d.get('stress_z_layer_cv', [])
        if z_data:
            zs = [layer['z_mid_um'] for layer in z_data]
            cvs = [layer['cv'] for layer in z_data]
            c = colors_cycle[i % len(colors_cycle)]
            ax.plot(zs, cvs, marker='o', markersize=5, linewidth=1.5,
                    color=c, label=names[i], zorder=3)

    ax.set_xlabel("Z Position (μm)", fontsize=10)
    ax.set_ylabel("Von Mises CV (%)", fontsize=11)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.4, color="#CCCCCC", alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Stress Uniformity by Z-layer", fontsize=13, fontweight="bold", pad=10)
    ax.legend(fontsize=8, frameon=False)
    if standalone:
        return _save(fig, "", "")
    return ax


def _save_csv(outdir, fname, names, all_data, keys):
    """Save plot data as CSV for download."""
    import csv
    path = os.path.join(outdir, fname)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Case'] + [k for k, _ in keys])
        for i, name in enumerate(names):
            row = [name]
            for key, transform in keys:
                val = _get(all_data[i], key)
                if transform:
                    val = transform(all_data[i])
                row.append(val)
            writer.writerow(row)
    return fname


# ─── Four-panel composite ────────────────────────────────────────────────────

def plot_four_panel(all_data, names, outdir):
    fig, axes = plt.subplots(2, 2, figsize=FIG_FOUR)
    plot_porosity(all_data, names, ax=axes[0, 0])
    plot_am_se_interface(all_data, names, ax=axes[0, 1])
    plot_se_se_tradeoff(all_data, names, ax=axes[1, 0])
    plot_percolation_tortuosity(all_data, names, ax=axes[1, 1])

    for i, label in enumerate(['(a)', '(b)', '(c)', '(d)']):
        ax = axes.flat[i]
        ax.text(-0.12, 1.05, label, transform=ax.transAxes,
                fontsize=14, fontweight='bold', va='top')

    fig.suptitle("DEM Analysis Comparison", fontsize=16, fontweight="bold", y=1.01)
    return _save(fig, outdir, "four_panel.png")


def _generate_particle_info(all_data, ps_labels, case_names, outdir):
    """Generate particle info summary table(s) as PNG, split by group if available."""
    global _GROUP_INFO

    if _GROUP_INFO and len(_GROUP_INFO[0]) > 1:
        sizes, gnames = _GROUP_INFO
        n_groups = len(sizes)
        fig, axes = plt.subplots(n_groups, 1, figsize=(max(7, max(sizes)*1.5 + 2), 3 * n_groups))
        if n_groups == 1:
            axes = [axes]

        idx = 0
        for gi, (sz, gname) in enumerate(zip(sizes, gnames)):
            ax = axes[gi]
            ax.axis('off')
            ax.set_title(gname, fontsize=12, fontweight='bold', color=GROUP_COLORS[gi % len(GROUP_COLORS)], pad=10)

            group_data = all_data[idx:idx+sz]
            group_labels = ps_labels[idx:idx+sz]

            headers = ['P:S'] + group_labels
            rows_data = []
            for ptype in ['AM_P', 'AM_S', 'SE']:
                row = [f'{ptype} Count']
                for d in group_data:
                    val = d.get(f'n_{ptype}', '-')
                    row.append(str(int(val)) if val != '-' else '-')
                rows_data.append(row)
            for ptype in ['AM_P', 'AM_S', 'SE']:
                row = [f'{ptype} R (μm)']
                for d in group_data:
                    val = d.get(f'r_{ptype}', '-')
                    row.append(str(val) if val != '-' else '-')
                rows_data.append(row)

            table = ax.table(cellText=rows_data, colLabels=headers, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1, 1.4)
            for j in range(len(headers)):
                cell = table[0, j]
                cell.set_facecolor(GROUP_COLORS[gi % len(GROUP_COLORS)])
                cell.set_text_props(color='white', fontweight='bold')
            for i in range(len(rows_data)):
                for j in range(len(headers)):
                    cell = table[i+1, j]
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')

            idx += sz

        fig.tight_layout()
        fig.savefig(os.path.join(outdir, 'particle_info.png'), dpi=DPI,
                    bbox_inches='tight', facecolor='white', pad_inches=0.1)
        plt.close(fig)
    else:
        # Single group (original behavior)
        fig, ax = plt.subplots(figsize=(max(7, len(ps_labels)*1.5 + 2), 3))
        ax.axis('off')

        headers = ['P:S'] + ps_labels
        rows_data = []
        for ptype in ['AM_P', 'AM_S', 'SE']:
            row = [f'{ptype} Count']
            for d in all_data:
                val = d.get(f'n_{ptype}', '-')
                row.append(str(int(val)) if val != '-' else '-')
            rows_data.append(row)
        for ptype in ['AM_P', 'AM_S', 'SE']:
            row = [f'{ptype} R (μm)']
            for d in all_data:
                val = d.get(f'r_{ptype}', '-')
                row.append(str(val) if val != '-' else '-')
            rows_data.append(row)

        table = ax.table(cellText=rows_data, colLabels=headers, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.4)
        for j in range(len(headers)):
            cell = table[0, j]
            cell.set_facecolor('#4472C4')
            cell.set_text_props(color='white', fontweight='bold')
        for i in range(len(rows_data)):
            for j in range(len(headers)):
                cell = table[i+1, j]
                cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')

        fig.tight_layout()
        fig.savefig(os.path.join(outdir, 'particle_info.png'), dpi=DPI,
                    bbox_inches='tight', facecolor='white', pad_inches=0.1)
        plt.close(fig)


# ─── New Plots ─────────────────────────────────────────────────────────────────

ORANGE = "#ED7D31"
PURPLE = "#7030A0"


def plot_se_network(data_list, names, outdir):
    """SE-SE CN mean + SE Cluster count (dual Y axis)."""
    fig, ax1 = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))

    cn = [_get(d, "se_se_cn") for d in data_list]
    clusters = [_get(d, "n_components") for d in data_list]
    large_clusters = [_get(d, "n_large_components") for d in data_list]

    color1, color2 = BLUE, ORANGE
    ax1.plot(x, cn, 's-', color=color1, markersize=10, linewidth=2.5, label="SE-SE CN mean")
    _apply_style(ax1, "SE-SE CN mean", names)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    ax2.bar(x - 0.15, clusters, 0.3, color=color2, alpha=0.4, label="Total Clusters")
    ax2.bar(x + 0.15, large_clusters, 0.3, color=color2, alpha=0.85, label="Large (≥10)")
    ax2.set_ylabel("SE Cluster Count", fontsize=11, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper right')
    ax1.set_title("SE Network: CN & Clusters", fontsize=12, fontweight='bold')
    _write_csv(outdir, 'se_network.csv', ['SE-SE CN', 'Total Clusters', 'Large(≥10)'],
               names, cn, clusters, large_clusters)
    return _save(fig, outdir, "se_network.png")


def plot_contact_force(data_list, names, outdir):
    """Contact force distribution by type (grouped bar)."""
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    n = len(names)
    x = np.arange(n)
    types = ['AM_P-AM_P', 'AM_P-SE', 'SE-SE', 'AM_P-AM_S', 'AM_S-SE']
    colors = [RED, GREEN, BLUE, ORANGE, LIGHT_GREEN]

    # Find which types actually have data
    active = []
    for ct, color in zip(types, colors):
        key = f"fn_{ct.replace('-','_')}_mean"
        vals = [_get(d, key) for d in data_list]
        if any(v > 0 for v in vals):
            active.append((ct, key, color, vals))

    if not active:
        plt.close(fig)
        return None

    w = 0.8 / len(active)
    for i, (ct, key, color, vals) in enumerate(active):
        offset = (i - len(active)/2 + 0.5) * w
        bars = ax.bar(x + offset, vals, w, label=ct, color=color, alpha=0.85)

    _apply_style(ax, "Fn mean (μN)", names)
    ax.legend(fontsize=8, loc='upper right')
    ax.set_title("Contact Force by Type", fontsize=12, fontweight='bold')
    # CSV
    headers = [ct for ct, _, _, _ in active]
    cols = [vals for _, _, _, vals in active]
    _write_csv(outdir, 'contact_force.csv', [f'Fn {h} mean(μN)' for h in headers], names, *cols)
    return _save(fig, outdir, "contact_force.png")


def plot_contact_pressure(data_list, names, outdir):
    """Contact pressure mean & max (dual bar)."""
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    n = len(names)
    x = np.arange(n)
    w = 0.35

    means = [_get(d, "contact_pressure_mean") for d in data_list]
    maxes = [_get(d, "contact_pressure_max") for d in data_list]

    ax.bar(x - w/2, means, w, label="Mean", color=BLUE, alpha=0.85)
    ax.bar(x + w/2, maxes, w, label="Max", color=RED, alpha=0.85)

    _apply_style(ax, "Contact Pressure (MPa)", names)
    ax.legend(fontsize=9)
    ax.set_title("Contact Pressure", fontsize=12, fontweight='bold')
    _write_csv(outdir, 'contact_pressure.csv', ['CP mean(MPa)', 'CP max(MPa)'], names, means, maxes)
    return _save(fig, outdir, "contact_pressure.png")


def plot_am_vulnerability(data_list, names, outdir):
    """AM vulnerability + AM-SE CN (dual Y axis)."""
    fig, ax1 = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))

    vuln = [_get(d, "am_vulnerable_pct") for d in data_list]
    cn = [_get(d, "am_se_cn_mean") for d in data_list]

    color1, color2 = RED, BLUE
    ax1.bar(x, vuln, 0.5, color=color1, alpha=0.7, label="Vulnerable AM (%)")
    _apply_style(ax1, "Vulnerable AM (%)", names)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    ax2.plot(x, cn, 'o-', color=color2, markersize=8, linewidth=2, label="AM-SE CN")
    ax2.set_ylabel("AM-SE CN mean", fontsize=11, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper right')
    ax1.set_title("AM Vulnerability & SE Connectivity", fontsize=12, fontweight='bold')
    _write_csv(outdir, 'am_vulnerability.csv', ['Vulnerable(%)', 'AM-SE CN'], names, vuln, cn)
    return _save(fig, outdir, "am_vulnerability.png")


def plot_effective_conductivity(data_list, names, outdir):
    """Bruggeman effective ionic conductivity."""
    fig, ax1 = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))

    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    phi = [_get(d, "phi_se") for d in data_list]

    ax1.plot(x, sigma_brug, 's-', color=GREEN, markersize=10, linewidth=2.5, label="σ_brug/σ_grain")
    _apply_style(ax1, "σ_brug / σ_grain", names)
    ax1.tick_params(axis='y', labelcolor=GREEN)

    ax1b = ax1.twinx()
    ax1b.bar(x, phi, 0.4, color=BLUE, alpha=0.25, label="φ_SE")
    ax1b.set_ylabel("φ_SE", fontsize=10, color=BLUE)
    ax1b.set_ylim(0.2, max(phi) * 1.15 if phi else 0.4)
    ax1b.tick_params(axis='y', labelcolor=BLUE)
    ax1b.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper right')
    ax1.set_title("Bruggeman: σ_brug/σ_grain = φ_SE × f_perc / τ²", fontsize=12, fontweight='bold')

    _write_csv(outdir, 'effective_conductivity.csv',
               ['φ_SE', 'σ_brug/σ_grain'], names, phi, sigma_brug)
    return _save(fig, outdir, "effective_conductivity.png")


R_GB_MIN_R2 = 0.75  # minimum R² for R_gb fitting to be valid

def _fit_r_gb(data_list, names, use_global=True):
    """Fit GB correction: BLM+Constriction model R = C × (GB_d² × T)^α.
    log(R) = α × log(GB_d²×T) + ln(C)
    Returns alpha, ln_C, valid_idx, r_squared."""
    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    perc = [_get(d, "percolation_pct") / 100 for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    g_path = [_get(d, "path_conductance_mean") for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    thickness = [_get(d, "thickness_um", 0) for d in data_list]

    sigma_proxy = [g_path[i] * perc[i] / tau[i] if g_path[i] > 0 and tau[i] > 0 else 0
                   for i in range(len(data_list))]

    valid_idx = [i for i in range(len(data_list))
                 if sigma_proxy[i] > 0 and gb_dens[i] > 0 and sigma_brug[i] > 0 and thickness[i] > 0]

    if use_global and _GLOBAL_RGB is not None:
        return _GLOBAL_RGB[0], _GLOBAL_RGB[1], valid_idx, 1.0

    alpha = 1.87
    ln_C = -3.26
    r_squared = 0
    if len(valid_idx) >= 2:
        ratio = np.array([sigma_brug[i] / sigma_proxy[i] for i in valid_idx])
        # x = GB_d² × T (BLM + Constriction)
        x_vals = np.array([gb_dens[i]**2 * thickness[i] for i in valid_idx])
        log_y = np.log(ratio)
        log_x = np.log(x_vals)
        from scipy import stats as sp_stats
        slope, intercept, r_val, _, _ = sp_stats.linregress(log_x, log_y)
        alpha = slope
        ln_C = intercept
        r_squared = r_val ** 2
    return alpha, ln_C, valid_idx, r_squared


def plot_rgb_fitting(data_list, names, outdir):
    """BLM+Constriction fitting: log(R) vs log(GB_d²×T)."""
    alpha, ln_C, valid_idx, r_squared = _fit_r_gb(data_list, names)

    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    perc = [_get(d, "percolation_pct") / 100 for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    g_path = [_get(d, "path_conductance_mean") for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    thickness = [_get(d, "thickness_um", 100) for d in data_list]
    sigma_proxy = [g_path[i] * perc[i] / tau[i] if g_path[i] > 0 and tau[i] > 0 else 0
                   for i in range(len(data_list))]

    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    # x = log(GB_d² × T), y = log(R)
    x_pts = np.array([np.log(gb_dens[i]**2 * thickness[i]) for i in valid_idx])
    y_pts = np.array([np.log(sigma_brug[i] / sigma_proxy[i]) for i in valid_idx])

    # Group colors
    point_groups = [0] * len(valid_idx)
    group_boundaries = []
    if _GROUP_INFO:
        sizes, gnames = _GROUP_INFO
        pos = 0
        for sz in sizes:
            group_boundaries.append((pos, pos + sz))
            pos += sz
        for j, i in enumerate(valid_idx):
            for g_idx, (start, end) in enumerate(group_boundaries):
                if start <= i < end:
                    point_groups[j] = g_idx
                    break

    if _GROUP_INFO:
        for j in range(len(valid_idx)):
            gi = point_groups[j]
            ax.scatter(x_pts[j], y_pts[j], s=100, c=GROUP_COLORS[gi % len(GROUP_COLORS)],
                      zorder=5, edgecolors='white', linewidth=1.5)
    else:
        ax.scatter(x_pts, y_pts, s=100, c=BLUE, zorder=5, edgecolors='white', linewidth=1.5)

    # Labels
    try:
        from adjustText import adjust_text
        texts = []
        for j, i in enumerate(valid_idx):
            texts.append(ax.text(x_pts[j], y_pts[j], names[i], fontsize=8, color=BLACK, zorder=6))
        adjust_text(texts, x=list(x_pts), y=list(y_pts), ax=ax,
                   arrowprops=dict(arrowstyle='-', color='gray', lw=0.5),
                   force_text=(0.5, 0.5), expand=(1.3, 1.5))
    except ImportError:
        for j, i in enumerate(valid_idx):
            ax.annotate(names[i], (x_pts[j], y_pts[j]),
                       fontsize=8, ha='left', va='bottom', xytext=(5, 5),
                       textcoords='offset points', color=BLACK, zorder=6)

    # Group labels
    if _GROUP_INFO:
        for gi, (start, end) in enumerate(group_boundaries):
            group_js = [j for j, i in enumerate(valid_idx) if start <= i < end]
            if group_js:
                cx = np.mean([x_pts[j] for j in group_js])
                cy = min([y_pts[j] for j in group_js])
                ax.text(cx, cy - (max(y_pts) - min(y_pts)) * 0.08, gnames[gi],
                       ha='center', va='top',
                       fontsize=9, fontweight='bold', color=GROUP_COLORS[gi % len(GROUP_COLORS)],
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                                edgecolor=GROUP_COLORS[gi % len(GROUP_COLORS)], alpha=0.8))

    # Fit line
    x_line = np.linspace(min(x_pts) * 0.9, max(x_pts) * 1.1, 100)
    y_line = alpha * x_line + ln_C
    ax.plot(x_line, y_line, '-', color=RED, linewidth=2.5,
            label=f"y = {alpha:.2f}·x + {ln_C:.2f}")

    ax.set_xlabel("log(GB_d² × T)", fontsize=12)
    ax.set_ylabel("log(σ_brug / σ_proxy)", fontsize=12)
    title_suffix = " (global)" if _GLOBAL_RGB is not None else ""
    ax.set_title(f"BLM+Constriction Fitting{title_suffix}", fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.text(0.95, 0.05, f"α = {alpha:.2f}\nln(C) = {ln_C:.2f}\nR² = {r_squared:.4f}\nn = {len(x_pts)}",
            transform=ax.transAxes, fontsize=11, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8))
    y_margin = (max(y_pts) - min(y_pts)) * 0.15
    ax.set_ylim(min(y_pts) - y_margin, max(y_pts) + y_margin)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.4, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    _write_csv(outdir, 'rgb_fitting.csv',
               ['GB_d²×T', 'log(GB_d²×T)', 'log(σ_brug/σ_proxy)', 'σ_brug', 'σ_proxy', 'thickness_um'],
               [names[i] for i in valid_idx],
               [gb_dens[i]**2 * thickness[i] for i in valid_idx],
               list(x_pts), list(y_pts),
               [sigma_brug[i] for i in valid_idx],
               [sigma_proxy[i] for i in valid_idx],
               [thickness[i] for i in valid_idx])
    return _save(fig, outdir, "rgb_fitting.png")


def _load_network_sigma(data_list):
    """Load σ_full from network_conductivity.json for each case."""
    sigma_net = [0] * len(data_list)
    for i, d in enumerate(data_list):
        net_val = _get(d, "sigma_full_mScm", 0)
        if net_val > 0:
            sigma_net[i] = net_val
        else:
            src = _get(d, "_source_path", "")
            if src:
                net_path = os.path.join(os.path.dirname(src), "network_conductivity.json")
                if os.path.exists(net_path):
                    try:
                        with open(net_path) as _nf:
                            nd = json.load(_nf)
                        sigma_net[i] = nd.get("sigma_full_mScm", 0) or 0
                    except:
                        pass
    return sigma_net


def plot_gb_corrected(data_list, names, outdir):
    """Part I: Proxy-based GB-corrected σ_eff using BLM+Constriction."""
    alpha, ln_C, _, r2_check = _fit_r_gb(data_list, names)
    SIGMA_BULK = 3.0  # σ_grain (grain interior)
    C = np.exp(ln_C)

    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    thickness = [_get(d, "thickness_um", 100) for d in data_list]

    sigma_corr = []
    for i in range(len(data_list)):
        gb2t = gb_dens[i]**2 * thickness[i]
        if gb2t > 0:
            correction = C * gb2t**alpha
            sigma_corr.append(sigma_brug[i] / correction if correction > 0 else sigma_brug[i])
        else:
            sigma_corr.append(sigma_brug[i])
    sigma_abs = [s * SIGMA_BULK for s in sigma_corr]

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    ax.plot(x, sigma_corr, 's-', color=RED, markersize=ms, linewidth=lw, label="σ_brug/σ_grain")
    _apply_style(ax, "σ_brug / σ_grain (proxy)", names)
    ax.tick_params(axis='y', labelcolor=RED)

    ax2 = ax.twinx()
    ax2.plot(x, sigma_abs, 'D--', color=ORANGE, markersize=ms-2, linewidth=lw-0.5, label="σ_ionic (mS/cm)")
    ax2.set_ylabel("σ_ionic (mS/cm)", fontsize=11, color=ORANGE)
    ax2.tick_params(axis='y', labelcolor=ORANGE)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')
    gb_src = "global" if _GLOBAL_RGB is not None else "local"
    ax.set_title(f"Part I: Proxy σ_eff = σ_brug / C·(GB_d²·T)^α\nα={alpha:.2f}, R²={r2_check:.3f} [{gb_src}]",
                 fontsize=10, fontweight='bold')

    _write_csv(outdir, 'gb_corrected.csv',
               ['GB_d', 'T(μm)', 'GB_d²×T', 'σ_brug/σ_grain', 'σ_brug/σ_grain', 'σ_eff(mS/cm)'],
               names, gb_dens, thickness,
               [gb_dens[i]**2*thickness[i] for i in range(len(names))],
               sigma_brug, sigma_corr, sigma_abs)
    return _save(fig, outdir, "gb_corrected.png")


def plot_ionic_scaling_fit(data_list, names, outdir):
    """Ionic scaling law fit: σ_predicted vs σ_actual scatter (log-log).
    Uses same fitting approach as find_scaling_law.py model 4."""
    SIGMA_BULK = 3.0

    phi_se = [_get(d, "phi_se") for d in data_list]
    f_perc = [_get(d, "percolation_pct", 0) / 100 for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    g_path = [_get(d, "path_conductance_mean", 0) for d in data_list]
    cn = [_get(d, "se_se_cn", 0) for d in data_list]
    sigma_net = _load_network_sigma(data_list)

    # Same as find_scaling_law.py: σ_brug = 3.0 × φ_SE × f_perc / τ²
    valid_idx = []
    SIGMA_MIN = 0.0  # include all non-zero σ_net (was 0.01; relaxed to test fit on low-σ cases)
    for i in range(len(data_list)):
        if (phi_se[i] > 0 and f_perc[i] > 0 and tau[i] > 0 and
            g_path[i] > 0 and cn[i] > 0 and gb_dens[i] > 0 and sigma_net[i] > SIGMA_MIN):
            valid_idx.append(i)

    if len(valid_idx) < 3:
        return None

    s_actual = np.array([sigma_net[i] for i in valid_idx])
    log_sf = np.log(s_actual)

    # σ_brug in mS/cm (same as find_scaling_law.py)
    sigma_brug = np.array([SIGMA_BULK * phi_se[i] * f_perc[i] / tau[i]**2 for i in valid_idx])
    log_sb = np.log(sigma_brug)

    # Fit: log(σ_full) = log(σ_brug) + a*log(g_path*gb_d²) + b*log(cn) + c
    log_combo = np.array([np.log(g_path[i] * gb_dens[i]**2) for i in valid_idx])
    log_cn = np.array([np.log(cn[i]) for i in valid_idx])
    residual = log_sf - log_sb
    X = np.column_stack([log_combo, log_cn, np.ones(len(valid_idx))])
    b_fit, _, _, _ = np.linalg.lstsq(X, residual, rcond=None)
    a_combo, b_cn, ln_C = b_fit
    C_fit = np.exp(ln_C)

    # Predicted (using fixed champion exponents: 0.25, 2)
    # Also compute free-fit R² for comparison
    pred_free = log_sb + X @ b_fit
    ss_res_free = np.sum((log_sf - pred_free)**2)
    ss_tot = np.sum((log_sf - np.mean(log_sf))**2)
    r2_free = 1 - ss_res_free / ss_tot

    # Fixed exponents + fit C only
    log_rhs_fixed = log_sb + 0.25 * log_combo + 2 * log_cn
    ln_C_fixed = np.mean(log_sf - log_rhs_fixed)
    C_fixed = np.exp(ln_C_fixed)
    # Save v3 C (legacy, for reference only)
    global _GLOBAL_C_ION
    pred_fixed = ln_C_fixed + log_rhs_fixed
    ss_res_fixed = np.sum((log_sf - pred_fixed)**2)
    r2_fixed = 1 - ss_res_fixed / ss_tot

    # === v12-CLEAN v3 (production) — simple fractions + f_p³ ===
    # v12 fit: (α,β,γ,δ,φc) = (0.53, 1.48, 0.42, 2.90, 0.20)
    # Rounded cleanly: (1/2, 3/2, 2/5, 3, 0.20) — δ=3 (not 2!) matches 2.90.
    # σ = C_blend(τ) × σ_grain × √(φ-0.2) × CN^(3/2) × cov^(2/5) × f_p³
    PHI_C = 0.20  # data-native percolation threshold
    coverage = [(lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)([v for v in [_get(d,"coverage_AM_P_mean",0), _get(d,"coverage_AM_S_mean",0), _get(d,"coverage_AM_mean",0)] if v>0]) for d in data_list]

    phi_ex_arr = np.array([max(phi_se[i] - PHI_C, 1e-4) for i in valid_idx])
    cn_arr = np.array([cn[i] for i in valid_idx])
    tau_arr = np.array([tau[i] for i in valid_idx])
    cov_arr = np.array([coverage[i] for i in valid_idx])

    # FORM X v9 BLEND: (1-w)·v5_sigmoid(τ) + w·poly3(lnτ)
    # Blend sigmoid (k, τc) continuously optimized by LOOCV.
    # Smooth k → fewer outliers in transition band.
    TAU_C = 2.1; TAU_K = 5.0          # v5 C(τ) sigmoid (fixed)
    fp_arr = np.array([max(f_perc[i], 0.01) for i in valid_idx])
    log_tau_arr = np.log(tau_arr)
    # v12-clean v3: α=1/2, β=3/2, γ=2/5, δ=3, φc=0.20
    # + v22: κ·log(hop_area) correction for R_bulk cylindrical-approx bias
    hop_area_prod = np.array([max(_get(data_list[i], "path_hop_area_mean", 0), 1e-10) for i in valid_idx])
    log_hop_area = np.log(hop_area_prod)
    log_rhs_base_v12 = (np.log(SIGMA_BULK) + 0.50*np.log(phi_ex_arr) + 1.5*np.log(cn_arr)
                        + 0.40*np.log(cov_arr) + 3.0*np.log(fp_arr))
    # v17 addition: β·I(p_frac > 0.5) — captures particulate-majority offset
    # (v14b found ΔLOOCV=+0.00385 ⭐ for this term)
    def _pfrac_v12(d):
        ps = (d.get("ps_ratio", "") or "")
        if ps in ("P only", "10:0"): return 1.0
        if ps in ("S only", "0:10"): return 0.0
        if ":" in ps:
            try:
                p, s = ps.split(":"); p, s = float(p), float(s)
                return p / (p + s) if (p + s) > 0 else 0.5
            except Exception:
                return 0.5
        return 0.5
    pf_prod = np.array([_pfrac_v12(data_list[i]) for i in valid_idx])
    # v18: replace binary indicator with smooth sigmoid. (k_pf, pc_pf) jointly
    # optimized by LOOCV alongside (k_bl, τc_bl). Binary is k_pf→∞ limit.
    # log_rhs_base starts with pure v12-clean v3; β added via residual fit later
    log_rhs_base = log_rhs_base_v12.copy()
    w_sigmoid = 1.0 / (1.0 + np.exp(-TAU_K * (tau_arr - TAU_C)))

    def _fit_at(k_bl, tc_bl, k_pf=10.0, pc_pf=0.5, tau_c_win=2.0, sigma_tau_win=0.3):
        """v29 PRODUCTION: v25 Gaussian τ-bump + v29 sigmoid(log gb_dens).
        3-term residual correction: β_pf·w_pf + β_lin·p·w_win + β_gb·w_gb.
        v30 phase-split exploration (v30/v30.1/v30.2) found no signal above noise —
        reverted to v29 as final. See v30b/c/d/e/v31 diagnostic sweeps below for
        the exhaustive search record.
        Returns (r2, loocv, w20, b_v5, b_p3, w_bl, pred, β_pf, β_win, w_pf)."""
        w_bl = 1.0 / (1.0 + np.exp(-k_bl * (tau_arr - tc_bl)))
        w_pf = 1.0 / (1.0 + np.exp(-k_pf * (pf_prod - pc_pf)))
        # Gaussian bump × p_frac·(1-p_frac) — MIXED-regime selector
        w_win = np.exp(-0.5 * ((tau_arr - tau_c_win) / max(sigma_tau_win, 0.05))**2)
        X_v5_l = np.column_stack([np.ones(len(log_sf)), w_sigmoid])
        X_p3_l = np.column_stack([np.ones(len(log_sf)), log_tau_arr, log_tau_arr**2, log_tau_arr**3])

        b_v5_l = np.linalg.lstsq(X_v5_l, log_sf - log_rhs_base, rcond=None)[0]
        b_p3_l = np.linalg.lstsq(X_p3_l, log_sf - log_rhs_base, rcond=None)[0]
        pv_l = X_v5_l @ b_v5_l
        pp_l = X_p3_l @ b_p3_l
        pred_pre = (1 - w_bl) * pv_l + w_bl * pp_l + log_rhs_base

        # v30: v29 + I(τ>1.8)·log(cov_P/cov_S) — phase-split asymmetry for thin regime
        #   β_pf · w_pf                     — P:S global sigmoid
        #   β_lin · p·w_win                 — linear p × Gaussian τ-bump
        #   β_gb · w_gb                     — sigmoid(log gb_dens)
        #   β_ps · I(τ>1.8)·log(cov_P/cov_S) — NEW v30: thin AM_P:AM_S coverage asymmetry
        # Rationale: r=-0.378 (p<0.005) found via v30b/c/d sweeps. Physics: at P=7:3
        # primary AM dominates coverage → log(cov_P/cov_S)>0 → negative β corrects
        # over-prediction. At P=3:7 reverse. ΔLOOCV=+0.00045 (subnoise but consistent
        # across 3 refinements). Conservative integration: data has more to say with
        # more samples, but current sign & magnitude are physics-justified.
        pf_c = w_pf - w_pf.mean()
        lin_term = pf_prod * w_win
        lin_c = lin_term - lin_term.mean()
        gb_arr_prod = np.array([max(gb_dens[i], 1e-6) for i in valid_idx])
        gb_log = np.log(gb_arr_prod)
        gc_gb = float(np.median(gb_log))   # sigmoid center = median
        k_gb = 4.0                         # steepness (bounded transition)
        w_gb = 1.0 / (1.0 + np.exp(-k_gb * (gb_log - gc_gb)))
        mix_term = w_gb
        mix_c = w_gb - w_gb.mean()
        # v29: 3-term residual (β_pf, β_lin, β_gb) — v30 phase-split was explored
        # (v30/v30.1/v30.2) but LOOCV gain was below noise σ=0.0018 in all variants.
        X_corr = np.column_stack([pf_c, lin_c, mix_c])
        resid = log_sf - pred_pre
        bc = np.linalg.lstsq(X_corr, resid, rcond=None)[0]
        pred = pred_pre + X_corr @ bc
        beta_pf, beta_lin, beta_gb = float(bc[0]), float(bc[1]), float(bc[2])
        beta_mix = beta_gb
        beta_win = beta_lin

        r2 = 1 - np.sum((log_sf - pred)**2) / ss_tot
        n_loo = len(log_sf)
        sse_loo = 0.0
        for ii in range(n_loo):
            mk = np.ones(n_loo, bool); mk[ii] = False
            bv_ = np.linalg.lstsq(X_v5_l[mk], (log_sf - log_rhs_base)[mk], rcond=None)[0]
            bp_ = np.linalg.lstsq(X_p3_l[mk], (log_sf - log_rhs_base)[mk], rcond=None)[0]
            pv9 = (1 - w_bl) * (X_v5_l @ bv_) + w_bl * (X_p3_l @ bp_) + log_rhs_base
            pf_c_mk = w_pf[mk] - w_pf[mk].mean()
            lin_mk = lin_term[mk];  lin_c_mk = lin_mk - lin_mk.mean()
            wgb_mk = w_gb[mk];      wgb_c_mk = wgb_mk - wgb_mk.mean()
            Xc_mk = np.column_stack([pf_c_mk, lin_c_mk, wgb_c_mk])
            bc_mk = np.linalg.lstsq(Xc_mk, (log_sf - pv9)[mk], rcond=None)[0]
            pred_ii = pv9[ii] + bc_mk[0] * (w_pf[ii] - w_pf[mk].mean()) \
                              + bc_mk[1] * (lin_term[ii] - lin_mk.mean()) \
                              + bc_mk[2] * (w_gb[ii] - wgb_mk.mean())
            sse_loo += (log_sf[ii] - pred_ii)**2
        loocv = 1 - sse_loo / ss_tot
        s_act_l = np.exp(log_sf); s_prd_l = np.exp(pred)
        w20 = int(np.sum(np.abs(s_prd_l - s_act_l) / s_act_l < 0.20))
        # Stash β_mix on the function for caller print access
        _fit_at._beta_mix = beta_mix
        return r2, loocv, w20, b_v5_l, b_p3_l, w_bl, pred, beta_pf, beta_win, w_pf

    # v29: continuous 6D optimization — (k_bl, τc_bl, k_pf, pc_pf, τ_c_win, σ_τ_win)
    from scipy.optimize import minimize
    def _neg_loocv(p):
        k_, tc_, kp_, pc_, tcw_, stw_ = p
        if k_ <= 0.1 or k_ > 20 or tc_ < 1.2 or tc_ > 3.0: return 1e6
        if kp_ <= 0.1 or kp_ > 50 or pc_ < 0.1 or pc_ > 0.9: return 1e6
        if tcw_ < 1.2 or tcw_ > 3.0 or stw_ < 0.15 or stw_ > 1.0: return 1e6
        return -_fit_at(k_, tc_, kp_, pc_, tcw_, stw_)[1]
    res = minimize(_neg_loocv, x0=[5.0, 2.0, 10.0, 0.5, 2.0, 0.3], method='Nelder-Mead',
                   options={'xatol': 1e-3, 'fatol': 1e-5, 'maxiter': 600, 'adaptive': True})
    best_k, best_tc, best_kp, best_pc, best_tcw, best_stw = (float(res.x[0]), float(res.x[1]),
                                                              float(res.x[2]), float(res.x[3]),
                                                              float(res.x[4]), float(res.x[5]))
    # Coarse sweep for diagnostic visibility (k_pf/pc_pf fixed at sane defaults)
    k_sweep = [1.5, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0]
    print(f"\n[BLEND SWEEP] coarse k scan at τc=2.0 (k_pf=10, pc_pf=0.5 fixed)")
    print(f"  {'k':>5s}  {'R²':>6s}  {'LOOCV':>6s}  {'±20%':>5s}")
    for k in k_sweep:
        r2_k, lo_k, w20_k, *_ = _fit_at(k, 2.0, 10.0, 0.5, 2.0, 0.3)
        print(f"  {k:5.1f}  {r2_k:.4f}  {lo_k:.4f}  {w20_k:2d}/{len(log_sf):2d}")
    r2_formX, loocv_formX, w20_opt, b_v5, b_p3, w_blend, pred_formX, beta_pf_prod, beta_win_prod, w_pf_prod = \
        _fit_at(best_k, best_tc, best_kp, best_pc, best_tcw, best_stw)
    kappa_area = 0.0
    print(f"  → continuous optimum: k_bl={best_k:.2f}, τc_bl={best_tc:.3f}  |  "
          f"k_pf={best_kp:.2f}, pc_pf={best_pc:.3f}  |  "
          f"τ_c_win={best_tcw:.3f}, σ_τ_win={best_stw:.3f}")
    print(f"    R²={r2_formX:.4f}, LOOCV={loocv_formX:.4f}, ±20%={w20_opt}/{len(log_sf)}")
    _Ct_chk = float(np.exp(b_v5[0])); _Cn_chk = float(np.exp(b_v5[0] + b_v5[1]))
    print(f"    Ct={_Ct_chk:.4f} (thick asymptote)  Cn={_Cn_chk:.4f} (thin asymptote)  "
          f"Ct/Cn={_Ct_chk/_Cn_chk:.2f}")
    print(f"    poly3 coefs = [{b_p3[0]:+.3f}, {b_p3[1]:+.3f}, {b_p3[2]:+.3f}, {b_p3[3]:+.3f}]")
    print(f"    β_pf    = {beta_pf_prod:+.4f}  ← P:S sigmoid amplitude")
    print(f"    β_lin   = {beta_win_prod:+.4f}  ← v28: p_frac × Gaussian bump (linear)")
    print(f"    β_gb    = {float(getattr(_fit_at, '_beta_mix', 0.0)):+.4f}  ← v29: sigmoid(log gb_dens) correction (bounded)")
    TAU_C_BL = best_tc
    TAU_K_BL = best_k

    # ────────────────────────────────────────────────────────────────
    # Export fitted v29 params to module globals.
    # Downstream plots (plot_multiscale_sigma, etc.) read these via
    # _formx_v29_params() → _formx_v29_predict() so they use the SAME
    # Nelder-Mead-optimised v29 as the parity plot above. Without this
    # export, _formx_v29_params() silently falls back to hardcoded
    # defaults which diverge from the fit and produce apparent residuals
    # (the "1mAh_80:20 7:3 under-prediction" was exactly this artifact).
    # ────────────────────────────────────────────────────────────────
    global _GLOBAL_IONIC_SIGMOID, _GLOBAL_IONIC_POLY3, _GLOBAL_PS_SIGMOID
    # v5 sigmoid amplitude + blend params (TAU_C, TAU_K of v5 sigmoid are
    # fixed shape constants, not fit).
    _C_thick_fit = float(np.exp(b_v5[0]))
    _C_thin_fit  = float(np.exp(b_v5[0] + b_v5[1]))
    _GLOBAL_IONIC_SIGMOID = (_C_thick_fit, _C_thin_fit,
                             2.1, 5.0,             # v5 sigmoid τ_c, k (fixed)
                             best_k, best_tc)      # blend K_BL, TC_BL (fit)
    _GLOBAL_IONIC_POLY3 = tuple(float(x) for x in b_p3)

    # Recompute centering means so downstream predictions match fit output.
    _gb_vec = np.array([max(gb_dens[i], 1e-6) for i in valid_idx])
    _gb_log = np.log(_gb_vec)
    _gb_log_med = float(np.median(_gb_log))
    _w_pf_vec  = 1.0 / (1.0 + np.exp(-best_kp * (pf_prod - best_pc)))
    _w_win_vec = np.exp(-0.5 * ((tau_arr - best_tcw) / max(best_stw, 0.05))**2)
    _w_gb_vec  = 1.0 / (1.0 + np.exp(-4.0 * (_gb_log - _gb_log_med)))
    _beta_gb_fit = float(getattr(_fit_at, '_beta_mix', 0.0))
    _GLOBAL_PS_SIGMOID = (
        best_kp, best_pc,                                # K_PF, PC_PF
        beta_pf_prod, beta_win_prod, _beta_gb_fit,       # B_PF, B_LIN, B_GB
        float(_w_pf_vec.mean()),                         # WPF_MEAN
        float((pf_prod * _w_win_vec).mean()),            # LIN_MEAN
        _gb_log_med,                                     # GB_LOG_MEAN
        best_tcw, best_stw,                              # TAU_C_WIN, SIGMA_TAU_WIN
        float(_w_gb_vec.mean()),                         # W_GB_MEAN
    )
    print(f"  [v29 export] globals set: C_thick={_C_thick_fit:.4f}, C_thin={_C_thin_fit:.4f}, "
          f"K_BL={best_k:.2f}, TC_BL={best_tc:.2f}, K_PF={best_kp:.2f}, PC_PF={best_pc:.2f}")

    # === v12 DATA-NATIVE EXPONENT FIT (diagnostic only, does not replace v9) ===
    # Jointly optimize (α, β, γ, δ, φc, k_bl, τc) where:
    #   log σ = log(σ_grain) + α·log(φ-φc) + β·log(CN) + γ·log(cov) + δ·log(fp) + C_blend(τ)
    # v9 fixed (α,β,γ,δ,φc) = (0.75, 1.5, 0.25, 2.0, 0.185). We check if the data
    # prefers different values by LOOCV. If v12 LOOCV > v9 LOOCV, data disagrees
    # with Kirkpatrick/Bruggeman priors. If ≈ same, v9 priors are consistent.
    cn_np = np.array([cn[i] for i in valid_idx], dtype=float)
    cov_np = np.array([coverage[i] for i in valid_idx], dtype=float)
    fp_np = np.array([max(f_perc[i], 0.01) for i in valid_idx], dtype=float)
    phi_np = np.array([phi_se[i] for i in valid_idx], dtype=float)
    ln_sigma = log_sf
    ss_tot_local = ss_tot

    def _loocv_at(params):
        a, b, g, dl, pc, kb, tcb = params
        if pc < 0.05 or pc > 0.30: return 1e6
        if a < 0.1 or a > 3.0: return 1e6
        if b < 0.1 or b > 3.5: return 1e6
        if g < -1.5 or g > 2.5: return 1e6
        if dl < 0.1 or dl > 5.0: return 1e6
        if kb < 0.1 or kb > 20 or tcb < 1.2 or tcb > 3.0: return 1e6
        phi_ex_v = np.maximum(phi_np - pc, 1e-4)
        lrhs = (np.log(SIGMA_BULK) + a*np.log(phi_ex_v) + b*np.log(cn_np)
                + g*np.log(cov_np) + dl*np.log(fp_np))
        w_bl_v = 1.0 / (1.0 + np.exp(-kb * (tau_arr - tcb)))
        X_v = np.column_stack([np.ones(len(ln_sigma)), w_sigmoid])
        X_p = np.column_stack([np.ones(len(ln_sigma)), log_tau_arr,
                                log_tau_arr**2, log_tau_arr**3])
        sse = 0.0
        n_loo = len(ln_sigma)
        for ii in range(n_loo):
            mk = np.ones(n_loo, bool); mk[ii] = False
            bv_ = np.linalg.lstsq(X_v[mk], (ln_sigma - lrhs)[mk], rcond=None)[0]
            bp_ = np.linalg.lstsq(X_p[mk], (ln_sigma - lrhs)[mk], rcond=None)[0]
            p_ii = (1 - w_bl_v[ii]) * (X_v[ii] @ bv_) + w_bl_v[ii] * (X_p[ii] @ bp_) + lrhs[ii]
            sse += (ln_sigma[ii] - p_ii)**2
        return sse / ss_tot_local   # minimize

    # ── v29 FITTED predictions + v32 per-run γ refit ──────────────────
    # v29 is already-fitted (R² ≈ 0.983). v32 γ are OLS-refit against
    # residuals of FITTED predictions so they play well with any v29
    # parameter update. If regime-features unavailable (no
    # dataset_summary.csv), predictions fall back to v29 silently.
    s_pred_v29 = np.exp(pred_formX)
    global _V32_FITTED_GAMMAS
    _V32_FITTED_GAMMAS = None
    try:
        feat_order = list(_V32_GAMMAS.keys())
        X_rows, y_rows = [], []
        for j, i in enumerate(valid_idx):
            feats = _v32_features_for_case(data_list[i])
            if feats is None:
                continue
            σ_net_i = sigma_net[i]
            σ_v29_i = float(s_pred_v29[j])
            if σ_net_i <= 0 or σ_v29_i <= 0:
                continue
            X_rows.append([feats.get(k, 0.0) for k in feat_order])
            y_rows.append(np.log(σ_net_i) - np.log(σ_v29_i))
        if len(X_rows) >= len(feat_order) + 2:
            X_arr = np.array(X_rows)
            y_arr = np.array(y_rows)
            gammas, *_ = np.linalg.lstsq(X_arr, y_arr, rcond=None)
            _V32_FITTED_GAMMAS = dict(zip(feat_order, (float(g) for g in gammas)))
            print(f"  [v32 refit] n_cases_used={len(X_rows)} / {len(valid_idx)}")
            for k, g in _V32_FITTED_GAMMAS.items():
                print(f"    γ({k:13s}) = {g:+.4f}")
    except Exception as _e:
        print(f"  [v32 refit] skipped ({_e}); using hardcoded defaults")
        _V32_FITTED_GAMMAS = None

    # Cache write deferred to main() after the plot loop so we can key on
    # args.names (case IDs) rather than the P:S-ratio label list passed
    # here as `names`. P:S labels are not unique across cases (every 7:3
    # case collides), which made the subset-match lookup trivially true
    # in the wrong direction and trivially false in the right one.

    s_pred = np.array([
        _formx_v32_predict(s_pred_v29[j], data_list[i])
        for j, i in enumerate(valid_idx)
    ])
    r2 = r2_formX
    s_actual = np.array([sigma_net[i] for i in valid_idx])

    # --- Residual diagnostic: find |err|>20% outliers and dump feature signature ---
    # Build per-index group label (e.g. "SE 0.5μm (1mAh_85:15)") + case hint from data source path
    def _case_label(idx):
        grp = ""
        if _GROUP_INFO:
            sizes, gnames = _GROUP_INFO
            pos = 0
            for sz, gn in zip(sizes, gnames):
                if pos <= idx < pos + sz:
                    grp = gn
                    break
                pos += sz
        src = data_list[idx].get("_source_path", "") if idx < len(data_list) else ""
        case_id = os.path.basename(os.path.dirname(src)) if src else ""
        lbl = names[idx] if idx < len(names) else f"idx{idx}"
        return f"{grp} | {case_id} [{lbl}]" if grp or case_id else lbl

    rel_err = (s_pred - s_actual) / s_actual * 100           # log-space (multiplicative) err %
    abs_err = np.abs(rel_err)
    delta_sigma = s_pred - s_actual                           # linear-space absolute gap (mS/cm)
    abs_delta = np.abs(delta_sigma)
    n_total = len(valid_idx)
    rmse_lin = float(np.sqrt(np.mean(delta_sigma**2)))
    mae_lin = float(np.mean(abs_delta))
    print(f"\n[IONIC v9 BLEND DIAG] n={n_total}, R²={r2_formX:.4f}, LOOCV={loocv_formX:.4f}")
    print(f"  log-space : mean|err|={np.mean(abs_err):.1f}%   median|err|={np.median(abs_err):.1f}%")
    print(f"  linear-sp : MAE={mae_lin:.4f} mS/cm   RMSE={rmse_lin:.4f} mS/cm")
    # Tier counts — show both % and absolute
    tiers = [5, 10, 15, 20, 30]
    cnt = {t: int(np.sum(abs_err < t)) for t in tiers}
    print(f"  tiers(%): <5%:{cnt[5]}/{n_total}   <10%:{cnt[10]}/{n_total}   <15%:{cnt[15]}/{n_total}"
          f"   <20%:{cnt[20]}/{n_total}   <30%:{cnt[30]}/{n_total}")
    abs_thresholds_mScm = [0.005, 0.010, 0.020, 0.030, 0.050]
    acnt = {t: int(np.sum(abs_delta < t)) for t in abs_thresholds_mScm}
    print(f"  tiers(Δσ): <0.005:{acnt[0.005]}/{n_total}   <0.010:{acnt[0.010]}/{n_total}   "
          f"<0.020:{acnt[0.020]}/{n_total}   <0.030:{acnt[0.030]}/{n_total}   <0.050:{acnt[0.050]}/{n_total}")

    # ─── TABLE 1: sorted by relative error % (log-space view) ───
    hdr = (f"  {'#':>3s} {'case (group | id [P:S])':70s} "
           f"{'σ_act':>7s} {'σ_pred':>7s} {'Δσ':>8s} {'err%':>7s} "
           f"{'φ_SE':>5s} {'f_p':>5s} {'τ':>5s} {'CN':>5s} {'cov':>5s}")
    print(f"\n  ── sorted by |err%| (log-space; relative; physics-correct) ──")
    print(hdr); print("  " + "-" * (len(hdr)-2))
    pct_sorted = sorted(range(n_total), key=lambda j: -abs_err[j])
    shown = 0
    for rank, j in enumerate(pct_sorted, 1):
        if abs_err[j] <= 10.0:
            continue
        i = valid_idx[j]
        nm = _case_label(i)[:70]
        flag = "  ⚠" if abs_err[j] > 20 else ("  ·" if abs_err[j] > 15 else "")
        print(f"  {rank:3d} {nm:70s} {s_actual[j]:7.4f} {s_pred[j]:7.4f} "
              f"{delta_sigma[j]:+8.4f} {rel_err[j]:+6.1f}% "
              f"{phi_se[i]:5.3f} {f_perc[i]:5.3f} {tau[i]:5.2f} {cn[i]:5.2f} {cov_arr[j]:5.3f}{flag}")
        shown += 1
    print(f"  ({shown} cases with |err|>10%, remaining {n_total - shown} are within ±10%)")

    # ─── TABLE 2: sorted by absolute gap Δσ (linear-space; matches what plot shows) ───
    print(f"\n  ── sorted by |Δσ| mS/cm (linear-space; absolute; matches plot visual) ──")
    print(hdr); print("  " + "-" * (len(hdr)-2))
    abs_sorted = sorted(range(n_total), key=lambda j: -abs_delta[j])
    shown2 = 0
    # Threshold: top 15 OR |Δσ| > 0.015 (whichever larger) — matches plot visibility
    delta_thr = 0.015
    for rank, j in enumerate(abs_sorted, 1):
        if abs_delta[j] <= delta_thr and shown2 >= 15:
            break
        i = valid_idx[j]
        nm = _case_label(i)[:70]
        flag = "  ⚠" if abs_delta[j] > 0.030 else ("  ·" if abs_delta[j] > 0.020 else "")
        print(f"  {rank:3d} {nm:70s} {s_actual[j]:7.4f} {s_pred[j]:7.4f} "
              f"{delta_sigma[j]:+8.4f} {rel_err[j]:+6.1f}% "
              f"{phi_se[i]:5.3f} {f_perc[i]:5.3f} {tau[i]:5.2f} {cn[i]:5.2f} {cov_arr[j]:5.3f}{flag}")
        shown2 += 1
    print(f"  ({shown2} shown; threshold |Δσ|>{delta_thr} or top-15)")

    # ─── Sign-pattern breakdown: how many over vs under, by magnitude tier ───
    over_mask = delta_sigma > 0
    under_mask = delta_sigma < 0
    print(f"\n  ── sign bias: over (pred>act) vs under (pred<act) ──")
    print(f"  |Δσ|>0.010:  over {int(np.sum(over_mask & (abs_delta > 0.010))):>3d}    under {int(np.sum(under_mask & (abs_delta > 0.010))):>3d}")
    print(f"  |Δσ|>0.020:  over {int(np.sum(over_mask & (abs_delta > 0.020))):>3d}    under {int(np.sum(under_mask & (abs_delta > 0.020))):>3d}")
    print(f"  |Δσ|>0.030:  over {int(np.sum(over_mask & (abs_delta > 0.030))):>3d}    under {int(np.sum(under_mask & (abs_delta > 0.030))):>3d}")
    print(f"  mean(Δσ) = {float(np.mean(delta_sigma)):+.4f}  ← if far from 0, systematic bias")
    # Residual-vs-feature correlation (Pearson on log-residual)
    log_res = np.log(s_pred) - np.log(s_actual)
    gb_arr = np.array([gb_dens[i] for i in valid_idx])
    gp_arr = np.array([g_path[i] for i in valid_idx])

    # Parse P:S ratio → particulate fraction
    def _parse_ps(d):
        ps = d.get("ps_ratio", "") or ""
        if ps in ("P only", "10:0"): return 1.0
        if ps in ("S only", "0:10"): return 0.0
        if ":" in ps:
            try:
                p, s = ps.split(":")
                p, s = float(p), float(s)
                return p / (p + s) if (p + s) > 0 else 0.5
            except Exception:
                return 0.5
        return 0.5
    p_frac_arr = np.array([_parse_ps(data_list[i]) for i in valid_idx])

    # AM-side morphology (previously unused)
    am_se_cn = np.array([_get(data_list[i], "am_se_cn_mean", 0) for i in valid_idx], dtype=float)
    am_am_cn = np.array([_get(data_list[i], "am_am_cn", 0) for i in valid_idx], dtype=float)
    am_am_area = np.array([_get(data_list[i], "am_am_mean_area", 0) for i in valid_idx], dtype=float)
    cn_ratio = np.divide(cn_arr, np.maximum(am_se_cn, 0.1))

    # ── HETEROGENEITY (std/cv) — mean-field model misses this ──
    cn_std = np.array([_get(data_list[i], "se_se_cn_std", 0) for i in valid_idx], dtype=float)
    tau_std = np.array([_get(data_list[i], "tortuosity_std", 0) for i in valid_idx], dtype=float)
    # coefficient of variation (dimensionless)
    cn_cv = np.divide(cn_std, np.maximum(cn_arr, 0.1))
    tau_cv = np.divide(tau_std, np.maximum(tau_arr, 0.1))
    am_am_cn_std = np.array([_get(data_list[i], "am_am_cn_std", 0) for i in valid_idx], dtype=float)

    # ── MECHANICAL STRESS / FORCE ──
    stress_cv = np.array([_get(data_list[i], "stress_cv", 0) for i in valid_idx], dtype=float)
    stress_z = np.array([_get(data_list[i], "stress_z_layer_cv", 0) for i in valid_idx], dtype=float)

    # ── R_BULK CYLINDRICAL-APPROXIMATION PROXY ──
    # Network solver uses R_cyl ≈ ρ·d/(π·a²); true R_sph = ρ/(2a).
    # Ratio R_cyl/R_sph ∝ 1/sqrt(A) → small contact area = big σ_net bias.
    # path_hop_area_mean is the per-hop contact area along percolating paths.
    hop_area = np.array([_get(data_list[i], "path_hop_area_mean", 0) for i in valid_idx], dtype=float)
    se_se_area = np.array([_get(data_list[i], "area_SE_SE_mean", 0) for i in valid_idx], dtype=float)

    feats = {'log(phi_ex)': np.log(phi_ex_arr), 'log(CN)': np.log(cn_arr),
             'log(tau)': log_tau_arr, 'log(cov)': np.log(cov_arr),
             'log(fp)': np.log(fp_arr),
             'log(gb_dens)': np.log(np.maximum(gb_arr, 1e-10)),
             'log(g_path)': np.log(np.maximum(gp_arr, 1e-10)),
             'p_frac (P:S)': p_frac_arr,
             '(p_frac)²': p_frac_arr**2,
             # AM-side morphology
             'log(am_se_cn)':  np.log(np.maximum(am_se_cn, 0.1)),
             'log(am_am_cn)':  np.log(np.maximum(am_am_cn, 0.1)),
             'log(se_cn/am_se_cn)': np.log(np.maximum(cn_ratio, 1e-3)),
             # ── NEW HETEROGENEITY (std/CV) ──
             'CN_cv (std/mean)':    cn_cv,
             'τ_cv (std/mean)':     tau_cv,
             'log(CN_std)':         np.log(np.maximum(cn_std, 1e-3)),
             'log(τ_std)':          np.log(np.maximum(tau_std, 1e-3)),
             'log(am_am_cn_std)':   np.log(np.maximum(am_am_cn_std, 1e-3)),
             # ── NEW MECHANICAL ──
             'stress_cv':           stress_cv,
             'stress_z_layer_cv':   stress_z,
             # ── Saturation probe: near-percolation sensitivity ──
             'log(1-fp)':           np.log(np.maximum(1.0 - fp_arr, 1e-4)),
             # ── R_BULK CYLINDRICAL APPROXIMATION PROXY ──
             'log(hop_area)':       np.log(np.maximum(hop_area, 1e-10)),
             '1/sqrt(hop_area)':    1.0 / np.sqrt(np.maximum(hop_area, 1e-10)),
             'log(se_se_area)':     np.log(np.maximum(se_se_area, 1e-10))}
    print("  residual(log) correlations:")
    for nm, v in feats.items():
        c = np.corrcoef(log_res, v)[0, 1] if np.std(v) > 0 else 0.0
        flag = " ⚠" if abs(c) > 0.3 else ""
        print(f"    {nm:12s} r = {c:+.3f}{flag}")
    print()

    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    # Group colors
    point_groups = [0] * len(valid_idx)
    group_boundaries = []
    if _GROUP_INFO:
        sizes, gnames = _GROUP_INFO
        pos = 0
        for sz in sizes:
            group_boundaries.append((pos, pos + sz))
            pos += sz
        for j, i in enumerate(valid_idx):
            for g_idx, (start, end) in enumerate(group_boundaries):
                if start <= i < end:
                    point_groups[j] = g_idx
                    break

    # Mark |err|>20% cases with a subtle darker edge (no overlay)
    is_outlier = np.abs((s_pred - s_actual) / s_actual) > 0.20

    if _GROUP_INFO:
        for j in range(len(valid_idx)):
            gi = point_groups[j]
            edge = '#444' if is_outlier[j] else 'white'
            lw = 1.8 if is_outlier[j] else 1.5
            ax.scatter(s_actual[j], s_pred[j], s=100,
                      c=GROUP_COLORS[gi % len(GROUP_COLORS)],
                      zorder=5, edgecolors=edge, linewidth=lw)
    else:
        ax.scatter(s_actual, s_pred, s=100, c=BLUE, zorder=5,
                  edgecolors='white', linewidth=1.5)

    # 1:1 line
    all_vals = np.concatenate([s_pred, s_actual])
    vmin, vmax = all_vals[all_vals > 0].min() * 0.5, all_vals.max() * 2
    ax.plot([vmin, vmax], [vmin, vmax], 'k--', linewidth=1.5, alpha=0.5, label='1:1 line')

    # ±20% band
    ax.fill_between([vmin, vmax], [vmin*0.8, vmax*0.8], [vmin*1.2, vmax*1.2],
                    alpha=0.1, color='green', label='±20%')

    # Group legend (no per-point labels to avoid MemoryError with adjustText on 41+ points)
    if _GROUP_INFO:
        from matplotlib.patches import Patch
        legend_patches = []
        for gi, (start, end) in enumerate(group_boundaries):
            group_js = [j for j, i in enumerate(valid_idx) if start <= i < end]
            if group_js:
                color = GROUP_COLORS[gi % len(GROUP_COLORS)]
                legend_patches.append(Patch(facecolor=color, label=gnames[gi]))
        if legend_patches:
            ax.legend(handles=legend_patches + [
                plt.Line2D([0], [0], linestyle='--', color='black', label='1:1 line'),
            ], fontsize=7, loc='upper left', ncol=1)

    # R²
    log_pred = np.log(s_pred[s_pred > 0])
    log_actual = np.log(s_actual[s_actual > 0])
    if len(log_pred) > 2:
        ss_res = np.sum((log_pred - log_actual)**2)
        ss_tot = np.sum((log_actual - np.mean(log_actual))**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    else:
        r2 = 0

    # Error stats
    errors = np.abs(s_pred - s_actual) / s_actual * 100
    within_20 = np.sum(errors < 20)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("σ_actual (Network solver, mS/cm)", fontsize=11)
    ax.set_ylabel("σ_predicted (Scaling law, mS/cm)", fontsize=11)
    # Title reads the ACTUAL γ being applied (refitted per-run if OLS converged,
    # else hardcoded defaults). Previously the coefficients were baked into the
    # text as -0.75/+1.62/-1.99/+0.35, which misled readers after a refit.
    _g = _V32_FITTED_GAMMAS if _V32_FITTED_GAMMAS is not None else _V32_GAMMAS
    _refit_tag = 'refit' if _V32_FITTED_GAMMAS is not None else 'default'
    _title_formula = (f"σ_ion — v12-clean v3 (=v29/v32) × exp("
                      f"{_g['LIGG_LB_PCT']:+.2f}·LIGG_LB "
                      f"{_g['THIN_X_GEOM']:+.2f}·w_thin·GEOM "
                      f"{_g['P50_DR_DEV']:+.2f}·(p₅₀δR−0.2) "
                      f"{_g['PSD_RATIO']:+.2f}·r_SE/r_AM)  [γ:{_refit_tag}]")
    ax.set_title(f"{_title_formula}\n"
                 f"τ-blend(k={best_k:.0f},τc={best_tc:.2f})  P:S(k={best_kp:.0f},pc={best_pc:.2f},β={beta_pf_prod:+.3f})  κ_A={kappa_area:+.3f}  R²={r2:.3f} (v32-applied)  |  v29_base R²={r2_formX:.3f} LOOCV={loocv_formX:.3f}",
                 fontsize=8, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')

    txt = (f"R²={r2:.3f} (n={len(valid_idx)})\n"
           f"|err|={np.mean(errors):.0f}%, ≤20%: {within_20}/{len(errors)}")
    ax.text(0.95, 0.05, txt, transform=ax.transAxes, fontsize=9,
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    ax.set_xlim(vmin, vmax)
    ax.set_ylim(vmin, vmax)
    ax.set_aspect('equal')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    _write_csv(outdir, 'ionic_scaling_fit.csv',
               ['σ_actual(mS/cm)', 'σ_predicted(mS/cm)', 'error(%)'],
               [names[i] for i in valid_idx],
               list(s_actual), list(s_pred), list(errors))
    outpath = _save(fig, outdir, "ionic_scaling_fit.png")
    real_all = (_REAL_NAMES if (_REAL_NAMES and len(_REAL_NAMES) == len(data_list))
                else list(names))
    _focus_parity(outdir, "ionic_scaling_fit", s_actual, s_pred,
                  [real_all[i] for i in valid_idx],
                  'σ_actual (Network solver, mS/cm)',
                  'σ_predicted (Scaling law, mS/cm)',
                  "선택 샘플만 — Hertzian v12-clean v3 식·계수 전체 fit 그대로 "
                  "(n=%d, R²=%.3f)" % (len(valid_idx), r2))
    return outpath


def plot_network_sigma(data_list, names, outdir):
    """Part II: Network solver σ_full (ground truth)."""
    SIGMA_BULK = 3.0  # σ_grain (grain interior)
    sigma_net = _load_network_sigma(data_list)
    sigma_brug_abs = [_get(d, "sigma_ratio") * SIGMA_BULK for d in data_list]

    if not any(s > 0 for s in sigma_net):
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    ax.plot(x, sigma_net, 's-', color='#2ecc71', markersize=ms, linewidth=lw,
            label="σ_full (network)")
    ax.plot(x, sigma_brug_abs, 'o--', color=BLUE, markersize=ms-2, linewidth=lw-0.5,
            alpha=0.5, label="σ_brug (Bruggeman)")
    _apply_style(ax, "σ_ionic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("Part II: Network Solver σ_full vs Bruggeman σ_brug",
                 fontsize=10, fontweight='bold')

    # R_brug annotation
    r_brugs = [sigma_brug_abs[i]/sigma_net[i] if sigma_net[i] > 0 else 0 for i in range(len(names))]
    valid_r = [r for r in r_brugs if r > 0]
    if valid_r:
        ax.text(0.95, 0.95, f"R_brug = {min(valid_r):.1f}~{max(valid_r):.1f}×\n(Bruggeman overestimation)",
                transform=ax.transAxes, fontsize=9, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8))

    _write_csv(outdir, 'network_sigma.csv',
               ['σ_brug(mS/cm)', 'σ_full(mS/cm)', 'R_brug'],
               names, sigma_brug_abs, sigma_net, r_brugs)
    return _save(fig, outdir, "network_sigma.png")


# ============================================================================
# FORM X v29 — SINGLE SOURCE OF TRUTH PREDICTION
# ============================================================================
# Shared by plot_multiscale_sigma (and can be reused by predictor_engine etc).
# Reads hyperparameters from module globals set by plot_ionic_scaling_fit.
# Any future changes to the v29 formula should ONLY touch this function and
# the fit function's residual computation — they must stay in lock-step.

def _formx_v29_params():
    """Load all v29 hyperparameters from module globals with legacy fallbacks.
    Returns a dict; centralizes the global-unpacking logic."""
    # C(τ) v5 asymptote + τ-blend coefficients
    TAU_C, TAU_K = 2.1, 5.0
    K_BL, TC_BL = 20.0, 2.044
    C_thick, C_thin = 0.029, 0.017
    if _GLOBAL_IONIC_SIGMOID is not None:
        if len(_GLOBAL_IONIC_SIGMOID) >= 6:
            C_thick, C_thin, TAU_C, TAU_K, K_BL, TC_BL = _GLOBAL_IONIC_SIGMOID[:6]
        else:
            C_thick, C_thin, TAU_C, TAU_K = _GLOBAL_IONIC_SIGMOID[:4]
    elif _GLOBAL_C_ION is not None:
        C_thick = _GLOBAL_C_ION; C_thin = C_thick * 0.54
    # poly3 coefs for blend
    p3 = _GLOBAL_IONIC_POLY3 if _GLOBAL_IONIC_POLY3 is not None \
         else (-3.80, +2.38, -5.58, +2.81)
    # P:S sigmoid + τ-bump + gb_dens sigmoid (residual correction)
    K_PF, PC_PF, B_PF, B_LIN, B_GB = 50.0, 0.598, -0.10, -0.49, 0.043
    WPF_MEAN, LIN_MEAN, GB_LOG_MEAN = 0.5, 0.05, -5.0
    TAU_C_WIN, SIGMA_TAU_WIN = 2.0, 0.15
    W_GB_MEAN = 0.5
    # v30 phase-split params (β_ps · w_thin(τ) · log(cov_P/cov_S))
    B_PS = 0.0; TAU_C_PS = 1.8; K_PS = 10.0; PS_MEAN = 0.0
    if _GLOBAL_PS_SIGMOID is not None:
        n = len(_GLOBAL_PS_SIGMOID)
        if n == 15:
            (K_PF, PC_PF, B_PF, B_LIN, B_GB,
             WPF_MEAN, LIN_MEAN, GB_LOG_MEAN,
             TAU_C_WIN, SIGMA_TAU_WIN, W_GB_MEAN,
             B_PS, TAU_C_PS, K_PS, PS_MEAN) = _GLOBAL_PS_SIGMOID
        elif n == 11:
            (K_PF, PC_PF, B_PF, B_LIN, B_GB,
             WPF_MEAN, LIN_MEAN, GB_LOG_MEAN,
             TAU_C_WIN, SIGMA_TAU_WIN, W_GB_MEAN) = _GLOBAL_PS_SIGMOID
        elif n == 10:
            (K_PF, PC_PF, B_PF, B_LIN, B_GB,
             WPF_MEAN, LIN_MEAN, GB_LOG_MEAN,
             TAU_C_WIN, SIGMA_TAU_WIN) = _GLOBAL_PS_SIGMOID
    return dict(
        SIGMA_BULK=3.0, PHI_C=0.20,
        C_thick=C_thick, C_thin=C_thin, TAU_C=TAU_C, TAU_K=TAU_K,
        K_BL=K_BL, TC_BL=TC_BL, p3=p3,
        K_PF=K_PF, PC_PF=PC_PF, B_PF=B_PF, B_LIN=B_LIN, B_GB=B_GB,
        WPF_MEAN=WPF_MEAN, LIN_MEAN=LIN_MEAN, GB_LOG_MEAN=GB_LOG_MEAN,
        TAU_C_WIN=TAU_C_WIN, SIGMA_TAU_WIN=SIGMA_TAU_WIN, W_GB_MEAN=W_GB_MEAN,
        B_PS=B_PS, TAU_C_PS=TAU_C_PS, K_PS=K_PS, PS_MEAN=PS_MEAN,
    )


def _formx_v29_predict(phi_se, cn, tau, coverage, f_perc, p_frac, gb_dens,
                        area_p=0.0, area_s=0.0, params=None):
    """Single source of truth for v29 FORM X prediction.
    area_p / area_s kept in signature for backward compat; v29 FINAL doesn't use them.
    Returns σ (mS/cm); 0 if core inputs invalid."""
    if not (cn > 0 and tau > 0 and coverage > 0):
        return 0.0
    p = params if params is not None else _formx_v29_params()
    phi_ex = max(phi_se - p['PHI_C'], 1e-4)
    # C(τ): v5 sigmoid asymptote ⊕ poly3 blend
    w_v5 = 1.0 / (1.0 + np.exp(-p['TAU_K'] * (tau - p['TAU_C'])))
    w_bl = 1.0 / (1.0 + np.exp(-p['K_BL'] * (tau - p['TC_BL'])))
    ln_C_v5 = np.log(p['C_thick']) + (np.log(p['C_thin']) - np.log(p['C_thick'])) * w_v5
    lt = np.log(tau)
    ln_C_p3 = p['p3'][0] + p['p3'][1]*lt + p['p3'][2]*lt**2 + p['p3'][3]*lt**3
    ln_C = (1 - w_bl) * ln_C_v5 + w_bl * ln_C_p3
    # Base Kirkpatrick scaling (α=1/2, β=3/2, γ=2/5, δ=3, φc=0.20)
    s = (np.exp(ln_C) * p['SIGMA_BULK']
         * phi_ex**0.5 * cn**1.5 * coverage**0.4 * f_perc**3)
    # Residual correction: β_pf·w_pf + β_lin·p·w_win + β_gb·w_gb + β_ps·w_thin·log(cov_P/cov_S)
    w_pf = 1.0 / (1.0 + np.exp(-p['K_PF'] * (p_frac - p['PC_PF'])))
    w_win = np.exp(-0.5 * ((tau - p['TAU_C_WIN']) / max(p['SIGMA_TAU_WIN'], 0.05))**2)
    w_gb = 1.0 / (1.0 + np.exp(-4.0 * (np.log(max(gb_dens, 1e-6)) - p['GB_LOG_MEAN'])))
    # v29 FINAL: 3-term residual correction (no phase-split β_ps)
    ps_corr = (p['B_PF']  * (w_pf - p['WPF_MEAN'])
             + p['B_LIN'] * (p_frac * w_win - p['LIN_MEAN'])
             + p['B_GB']  * (w_gb - p['W_GB_MEAN']))
    return s * np.exp(ps_corr)


def _ps_fraction(d):
    """Parse P:S ratio string to fraction of P (carbon). Shared across plots."""
    ps = (d.get("ps_ratio", "") or "")
    if ps in ("P only", "10:0"): return 1.0
    if ps in ("S only", "0:10"): return 0.0
    if ":" in ps:
        try:
            p, s = ps.split(":"); p, s = float(p), float(s)
            return p / (p + s) if (p + s) > 0 else 0.5
        except Exception:
            return 0.5
    return 0.5


# ──────────────────────────────────────────────────────────────
# v32 correction (4-term, fit from Apr-2026 exhaustive refit)
# Applied as  σ_v32 = σ_v29 × exp(Σ γ_i · feature_i)
# ──────────────────────────────────────────────────────────────
_V32_GAMMAS = {
    'LIGG_LB_PCT': -0.750,  # DEM-native dominance (normalised /35)
    'THIN_X_GEOM': +1.619,  # thin × hemisphere cap (normalised /20)
    'P50_DR_DEV':  -1.992,  # median δ/R* deviation from 0.20
    'PSD_RATIO':   +0.348,  # r_SE / r_AM_avg
}
_V32_T_CHAR = 30.0  # μm, thin-regime characteristic length

# Set inside plot_ionic_scaling_fit after v29 Nelder-Mead converges, by
# refitting γ on residuals of the FITTED v29 predictions. When populated,
# _formx_v32_predict() uses these instead of the hardcoded defaults above,
# avoiding the double-correction that degraded R² 0.983 → 0.976 when the
# hardcoded (defaults-calibrated) γ were applied on top of v29 FITTED.
_V32_FITTED_GAMMAS = None


def _load_v32_regime_table():
    """Load dataset_summary.csv once (case_id → {p50_dr, geom_pct, liggghts_lb_pct}).
    Returns {} if missing — v32 then falls back to v29 silently."""
    import os
    p = os.path.join('docs', 'figures', 'physics_regime', 'dataset_summary.csv')
    if not os.path.exists(p):
        return {}
    try:
        import csv
        out = {}
        with open(p) as f:
            for row in csv.DictReader(f):
                out[row.get('case_id', '')] = {
                    'p50_dr':       float(row.get('p50_dr') or 0),
                    'geom_pct':     float(row.get('geom') or 0),
                    'liggghts_lb_pct': float(row.get('liggghts_lb') or 0),
                }
        return out
    except Exception:
        return {}


_V32_REGIME_TABLE = None  # lazy-loaded


def _v32_features_for_case(data):
    """Compute v32 correction features from a single full_metrics dict.
    Returns None if required fields missing (falls back to v29)."""
    global _V32_REGIME_TABLE
    if _V32_REGIME_TABLE is None:
        _V32_REGIME_TABLE = _load_v32_regime_table()

    import os, json
    src = data.get("_source_path", "") or ""
    # case_id = parent directory of full_metrics.json
    case_id = os.path.basename(os.path.dirname(src)) if src else ""

    # Thickness
    T = _get(data, "thickness_um", 0) or 0
    if T <= 0:
        return None
    w_thin = np.exp(-T / _V32_T_CHAR)

    # Regime-cap features (p50_dr, geom_pct, liggghts_lb_pct)
    reg = _V32_REGIME_TABLE.get(case_id, {})
    p50_dr      = reg.get('p50_dr', 0.20)       # assume plastic threshold as default
    geom_pct    = reg.get('geom_pct', 0)
    liggghts_lb = reg.get('liggghts_lb_pct', 0)

    # PSD ratio — load input_params.json (r_SE / r_AM_avg)
    r_SE_r = r_AM_avg = 0
    if src:
        ip_path = os.path.join(os.path.dirname(src), 'input_params.json')
        if os.path.exists(ip_path):
            try:
                ip = json.load(open(ip_path))
                r_SE_r = ip.get('r_SE', 0) or 0
                r_p = ip.get('r_AM_P')
                r_s = ip.get('r_AM_S')
                rvals = [v for v in (r_p, r_s) if v]
                r_AM_avg = (sum(rvals) / len(rvals)) if rvals else 0
            except Exception:
                pass
    psd_ratio = (r_SE_r / r_AM_avg) if r_AM_avg > 0 else 0.1

    return {
        'LIGG_LB_PCT': liggghts_lb / 35.0,
        'THIN_X_GEOM': w_thin * (geom_pct / 20.0),
        'P50_DR_DEV':  p50_dr - 0.20,
        'PSD_RATIO':   psd_ratio,
    }


def _formx_v32_predict(sigma_v29, data):
    """Apply v32 4-term correction to v29 prediction.
    If regime features missing, returns v29 unchanged (silent passthrough).

    Uses _V32_FITTED_GAMMAS when populated (per-run refit by
    plot_ionic_scaling_fit → avoids double-correction). Falls back to
    the hardcoded _V32_GAMMAS when run standalone without a prior fit."""
    if sigma_v29 <= 0:
        return sigma_v29
    feats = _v32_features_for_case(data)
    if feats is None:
        return sigma_v29
    gammas = _V32_FITTED_GAMMAS if _V32_FITTED_GAMMAS is not None else _V32_GAMMAS
    log_corr = sum(gammas[k] * feats.get(k, 0.0) for k in gammas)
    return sigma_v29 * np.exp(log_corr)


def plot_multiscale_sigma(data_list, names, outdir):
    """FORM X v29: delegates prediction to _formx_v29_predict (single source of
    truth with plot_ionic_scaling_fit). Reads fitted hyperparams from globals."""
    # Consistency warning: v29 globals are set by plot_ionic_scaling_fit. If
    # they are still None, we fall back to hardcoded v29 defaults, which no
    # longer match whatever γ the parity plot is showing.
    if _GLOBAL_IONIC_SIGMOID is None:
        print("  [multiscale] WARNING: v29 globals not set — include "
              "'ionic_scaling_fit' in the plot list for consistent rendering.")

    phi_se = [_get(d, "phi_se") for d in data_list]
    cn = [_get(d, "se_se_cn", 0) for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    coverage = [(lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)([v for v in [_get(d,"coverage_AM_P_mean",0), _get(d,"coverage_AM_S_mean",0), _get(d,"coverage_AM_mean",0)] if v>0]) for d in data_list]
    f_perc = [max(_get(d, "percolation_pct", 100) / 100, 0.01) for d in data_list]
    sigma_net = _load_network_sigma(data_list)

    # Compute predictions via shared helper (matches fit by construction)
    p = _formx_v29_params()
    sigma_v29_raw = [
        _formx_v29_predict(
            phi_se[i], cn[i], tau[i], coverage[i], f_perc[i],
            _ps_fraction(data_list[i]),
            _get(data_list[i], "gb_density_mean", 1e-6),
            area_p=_get(data_list[i], "area_AM_P_SE_mean", 0.0),
            area_s=_get(data_list[i], "area_AM_S_SE_mean", 0.0),
            params=p,
        )
        for i in range(len(data_list))
    ]
    # v32 correction applied on top of v29 — per-case features pulled from
    # dataset_summary.csv (physics-regime caps) + input_params (PSD ratio).
    # Cases without regime data fall back to v29 silently.
    #
    # If plot_ionic_scaling_fit has not populated _V32_FITTED_GAMMAS yet
    # (e.g. user requested multiscale without parity), do our own OLS
    # refit here so we don't apply stale hardcoded γ that were fit on a
    # different case population.
    global _V32_FITTED_GAMMAS
    if _V32_FITTED_GAMMAS is None:
        try:
            feat_order = list(_V32_GAMMAS.keys())
            X_rows, y_rows = [], []
            for i, d in enumerate(data_list):
                feats = _v32_features_for_case(d)
                if feats is None: continue
                σn = sigma_net[i]; σv = sigma_v29_raw[i]
                if σn <= 0 or σv <= 0: continue
                X_rows.append([feats.get(k, 0.0) for k in feat_order])
                y_rows.append(np.log(σn) - np.log(σv))
            if len(X_rows) >= len(feat_order) + 2:
                gammas, *_ = np.linalg.lstsq(np.array(X_rows), np.array(y_rows), rcond=None)
                _V32_FITTED_GAMMAS = dict(zip(feat_order, (float(g) for g in gammas)))
                print(f"  [multiscale→v32 refit] n={len(X_rows)}  "
                      + "  ".join(f"γ({k})={g:+.3f}" for k, g in _V32_FITTED_GAMMAS.items()))
        except Exception as _e:
            print(f"  [multiscale→v32 refit] skipped: {_e}")

    sigma_ms = [
        _formx_v32_predict(sigma_v29_raw[i], data_list[i])
        for i in range(len(data_list))
    ]

    has_net = any(s > 0 for s in sigma_net)

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    ax.plot(x, sigma_ms, 's-', color=RED, markersize=ms, linewidth=lw,
            label="v12-clean v3 (mS/cm)")
    # ±22% error band (DEM stochastic variability)
    _ms_arr = np.array(sigma_ms)
    _ms_lo = _ms_arr * 0.78; _ms_hi = _ms_arr * 1.22
    ax.fill_between(x, _ms_lo, _ms_hi, color=RED, alpha=0.10, label='±22% band')
    if has_net:
        ax.plot(x, sigma_net, 'D--', color='#2ecc71', markersize=ms-2, linewidth=lw-0.5,
                alpha=0.7, label="Network solver (mS/cm)")
        # Outlier mark: rel>20% OR |Δσ|>0.025 (catches BOTH log-space %
        # and linear-space absolute outliers — user asked for dual visibility)
        _net_arr = np.array(sigma_net, dtype=float)
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = np.where(_net_arr > 0, np.abs(_ms_arr - _net_arr) / _net_arr, 0.0)
        abs_gap = np.abs(_ms_arr - _net_arr)
        out_mask = (rel > 0.20) | (abs_gap > 0.025)
        if np.any(out_mask):
            y_top = max(np.nanmax(_ms_hi), np.nanmax(_net_arr)) * 1.03
            ax.scatter(x[out_mask], [y_top] * int(out_mask.sum()),
                       marker='*', s=40, color='#888', zorder=3, clip_on=False)

    _apply_style(ax, "σ_ionic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')
    # Dynamic title: show the γ actually used (refit or hardcoded default).
    _g2 = _V32_FITTED_GAMMAS if _V32_FITTED_GAMMAS is not None else _V32_GAMMAS
    _tag2 = 'refit' if _V32_FITTED_GAMMAS is not None else 'default'
    ax.set_title(
        f"σ_ion — v12-clean v3 (=v29/v32) × exp("
        f"{_g2['LIGG_LB_PCT']:+.2f}·LIGG_LB "
        f"{_g2['THIN_X_GEOM']:+.2f}·w_thin·GEOM "
        f"{_g2['P50_DR_DEV']:+.2f}·(p₅₀δR−0.2) "
        f"{_g2['PSD_RATIO']:+.2f}·r_SE/r_AM)  [γ:{_tag2}]",
        fontsize=8.5, fontweight='bold')

    # Unified y-axis: if user/webapp passed --y-max-sigma, use it for cross-run
    # visual comparison. Otherwise auto-scale to current data (tight view).
    if _Y_MAX_SIGMA is not None and _Y_MAX_SIGMA > 0:
        ax.set_ylim(0, _Y_MAX_SIGMA)
    else:
        # Auto-compute: 10% headroom above max of (FORM X + ±22%) and network
        _candidates = [float(np.nanmax(_ms_hi))] if len(_ms_hi) else []
        if has_net:
            _net_max = float(np.nanmax(np.array(sigma_net, dtype=float)))
            if np.isfinite(_net_max):
                _candidates.append(_net_max)
        if _candidates:
            ax.set_ylim(0, max(_candidates) * 1.10)

    _write_csv(outdir, 'multiscale_sigma.csv',
               ['φ_SE', 'CN', 'τ', 'coverage', 'σ_v32(mS/cm)', 'σ_v29(mS/cm)', 'σ_network(mS/cm)'],
               names, phi_se, cn, tau, coverage, sigma_ms, sigma_v29_raw, sigma_net)
    return _save(fig, outdir, "multiscale_sigma.png")


def plot_v3_fitting(data_list, names, outdir):
    """[Legacy] v3: σ_brug × C × (G_path × GB_d²)^(1/4) × CN²."""
    SIGMA_BULK = 3.0
    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    g_path = [_get(d, "path_conductance_mean", 0) for d in data_list]
    cn = [_get(d, "se_se_cn", 0) for d in data_list]
    sigma_net = _load_network_sigma(data_list)

    valid = [i for i in range(len(data_list))
             if g_path[i]>0 and cn[i]>0 and gb_dens[i]>0 and sigma_brug[i]>0 and sigma_net[i]>0.01]
    if len(valid) < 3:
        C_v3 = 0.073
    else:
        log_rhs = np.array([np.log(sigma_brug[i]*SIGMA_BULK) + 0.25*np.log(g_path[i]*gb_dens[i]**2) + 2*np.log(cn[i]) for i in valid])
        log_act = np.array([np.log(sigma_net[i]) for i in valid])
        C_v3 = np.exp(np.mean(log_act - log_rhs))

    sigma_v3 = []
    for i in range(len(data_list)):
        if g_path[i]>0 and cn[i]>0 and gb_dens[i]>0:
            sigma_v3.append(sigma_brug[i]*C_v3*(g_path[i]*gb_dens[i]**2)**0.25*cn[i]**2*SIGMA_BULK)
        else:
            sigma_v3.append(0)

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names)); lw = _line_width(len(names))
    ax.plot(x, sigma_v3, 's-', color=RED, markersize=ms, linewidth=lw, label="v3 (mS/cm)")
    if any(s>0 for s in sigma_net):
        ax.plot(x, sigma_net, 'D--', color='#2ecc71', markersize=ms-2, linewidth=lw-0.5, alpha=0.7, label="Network solver (mS/cm)")
    _apply_style(ax, "σ_ionic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title(f"[Legacy v3] σ_brug × {C_v3:.4f} × (G_path×GB_d²)^¼ × CN²", fontsize=9, fontweight='bold')
    return _save(fig, outdir, "v3_fitting.png")


def plot_formx_decomposition(data_list, names, outdir):
    """FORM X v4 factor decomposition: (φ-φc)^¾, CN^1.5, ⁴√cov, C(τ)."""
    PHI_C = 0.185; TAU_C = 2.1; TAU_K = 5.0
    phi_se = [_get(d, "phi_se") for d in data_list]
    cn = [_get(d, "se_se_cn", 0) for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    coverage = [(lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)([v for v in [_get(d,"coverage_AM_P_mean",0), _get(d,"coverage_AM_S_mean",0), _get(d,"coverage_AM_mean",0)] if v>0]) for d in data_list]

    n = len(data_list)
    log_phiex = np.array([0.75*np.log(max(phi_se[i]-PHI_C, 0.001)) for i in range(n)])
    log_cn = np.array([1.5*np.log(cn[i]) if cn[i]>0 else 0 for i in range(n)])
    log_cov = np.array([0.25*np.log(coverage[i]) if coverage[i]>0 else 0 for i in range(n)])
    if _GLOBAL_IONIC_SIGMOID:
        # v29: tuple grew to 6 (adds best_k, best_tc). Only first 4 used here.
        Ct, Cn, tc, k = _GLOBAL_IONIC_SIGMOID[:4]
    else:
        Ct, Cn, tc, k = 0.034, 0.019, TAU_C, TAU_K
    log_Csig = np.array([np.log(Ct) + (np.log(Cn)-np.log(Ct)) / (1+np.exp(-k*(tau[i]-tc))) for i in range(n)])

    # Ref: best case
    sigma_net = _load_network_sigma(data_list)
    ref = np.argmax(sigma_net) if any(s>0 for s in sigma_net) else 0

    factors = [
        ('(φ−φc)^¾', log_phiex, '#4472C4'),
        ('CN^1.5', log_cn, '#ED7D31'),
        ('⁴√cov', log_cov, '#A5A5A5'),
        ('C(τ)', log_Csig, '#FFC000'),
    ]

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(max(8, n*0.8), max(10, n*0.32)), gridspec_kw={'height_ratios': [3, 2]})

    # Top: stacked bar (relative to ref)
    x = np.arange(n)
    bottom_pos = np.zeros(n); bottom_neg = np.zeros(n)
    for label, vals, color in factors:
        delta = vals - vals[ref]
        pos = np.clip(delta, 0, None); neg = np.clip(delta, None, 0)
        ax.bar(x, pos, bottom=bottom_pos, color=color, label=label, width=0.7, edgecolor='white', linewidth=0.5)
        ax.bar(x, neg, bottom=bottom_neg, color=color, width=0.7, edgecolor='white', linewidth=0.5)
        bottom_pos += pos; bottom_neg += neg

    ax.axhline(0, color='gray', linewidth=0.5)
    _apply_style(ax, 'Δlog(factor) from ref', names, data_list)
    # Get x_labels from ax (after _apply_style monomodal detection)
    x_labels = [t.get_text() for t in ax.get_xticklabels()]
    if not any(x_labels) or all(t == '' for t in x_labels):
        x_labels = list(names)
    ax.set_title(f'FORM X Factor Decomposition (ref: {x_labels[ref] if ref < len(x_labels) else names[ref]})', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=4)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # Bottom: horizontal bar per case (dominant factor)
    for i in range(n):
        deltas = [(label, vals[i]-vals[ref]) for label, vals, _ in factors]
        deltas.sort(key=lambda x: abs(x[1]), reverse=True)
        dominant = deltas[0][0]
        colors = [c for l,_,c in factors if l==dominant][0]
        ax2.barh(i, deltas[0][1], color=colors, height=0.6, edgecolor='white', linewidth=0.5)
        ax2.text(deltas[0][1], i, f' {dominant}', va='center', fontsize=7)

    ax2.set_yticks(range(n))
    ax2.set_yticklabels([x_labels[i][:20] for i in range(n)], fontsize=7)
    ax2.set_xlabel('Dominant factor Δlog', fontsize=10)
    ax2.set_title('Dominant factor per case', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)

    fig.tight_layout()
    _write_csv(outdir, 'formx_decomposition.csv',
               ['(φ-φc)^¾', 'CN^1.5', '⁴√cov', 'C(τ)', 'dominant'],
               x_labels,
               list(log_phiex), list(log_cn), list(log_cov), list(log_Csig),
               [sorted([(l, v[i]-v[ref]) for l,v,_ in factors], key=lambda x:-abs(x[1]))[0][0] for i in range(n)])
    return _save(fig, outdir, "formx_decomposition.png")


def plot_ionic_decomp_physics(data_list, names, outdir):
    """PHYSICS fixed-form factor decomposition: each factor's Δlog
    contribution vs the reference (max-σ) case for
    σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³ (physics target)."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    n = len(data_list)
    phi = [_get(d, 'phi_se') for d in data_list]
    cn = [_get(d, 'se_se_cn', 0) for d in data_list]
    cov = [(_cov_frac(d, physics=True) or _cov_frac(d, physics=False)) for d in data_list]
    fp = [_get(d, 'percolation_pct', 0)/100.0 for d in data_list]
    tau = [_get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 1)) for d in data_list]
    log_phi = np.array([0.5*np.log(max(phi[i]-PHI_C, 1e-4)) if phi[i] > PHI_C else 0 for i in range(n)])
    log_cn = np.array([CN_EXP*np.log(cn[i]) if cn[i] > 0 else 0 for i in range(n)])
    log_cov = np.array([COV_EXP*np.log(cov[i]) if cov[i] and cov[i] > 0 else 0 for i in range(n)])
    log_fp = np.array([3.0*np.log(max(fp[i], 1e-3)) if fp[i] > 0 else 0 for i in range(n)])
    # C_blend(τ): fit on valid cases, contribution = pred − base
    idx = [i for i in range(n)
           if phi[i] > PHI_C and cn[i] > 0 and cov[i] and cov[i] > 0 and fp[i] > 0
           and tau[i] > 0 and _stage_e_sigma(data_list[i])]
    log_cb = np.zeros(n)
    if len(idx) >= 8:
        base = np.array([np.log(SG)+log_phi[i]+log_cn[i]+log_cov[i]+log_fp[i] for i in idx])
        logsf = np.array([np.log(_stage_e_sigma(data_list[i])) for i in idx])
        taus = np.array([tau[i] for i in idx])
        _r2, _lo, _Ct, _Cn, pred, _, _ = _cblend_fit_score(base, logsf, taus)
        for j, i in enumerate(idx):
            log_cb[i] = pred[j] - base[j]
    sig = [_stage_e_sigma(d) or 0 for d in data_list]
    ref = int(np.argmax(sig)) if any(s > 0 for s in sig) else 0
    factors = [
        ('(φ−0.19)^0.5', log_phi, '#4472C4'),
        ('CN²', log_cn, '#ED7D31'),
        ('cov^0.5', log_cov, '#A5A5A5'),
        ('f_p³', log_fp, '#70AD47'),
        ('C_blend(τ)', log_cb, '#FFC000'),
    ]
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(max(8, n*0.8), max(10, n*0.32)),
                                  gridspec_kw={'height_ratios': [3, 2]})
    x = np.arange(n); bpos = np.zeros(n); bneg = np.zeros(n)
    for label, vals, color in factors:
        delta = vals - vals[ref]
        pos = np.clip(delta, 0, None); neg = np.clip(delta, None, 0)
        ax.bar(x, pos, bottom=bpos, color=color, label=label, width=0.7,
               edgecolor='white', linewidth=0.5)
        ax.bar(x, neg, bottom=bneg, color=color, width=0.7, edgecolor='white', linewidth=0.5)
        bpos += pos; bneg += neg
    ax.axhline(0, color='gray', linewidth=0.5)
    _apply_style(ax, 'delta-log(factor) from ref', names, data_list)
    x_labels = [t.get_text() for t in ax.get_xticklabels()]
    if not any(x_labels):
        x_labels = list(names)
    ax.set_title('PHYSICS fixed-form factor decomposition (ref: %s)'
                 % (x_labels[ref] if ref < len(x_labels) else names[ref]),
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=5)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    for i in range(n):
        deltas = sorted([(l, v[i]-v[ref]) for l, v, _ in factors],
                        key=lambda t: -abs(t[1]))
        dom = deltas[0][0]; col = [c for l, _, c in factors if l == dom][0]
        ax2.barh(i, deltas[0][1], color=col, height=0.6, edgecolor='white', linewidth=0.5)
        ax2.text(deltas[0][1], i, f' {dom}', va='center', fontsize=7)
    ax2.set_yticks(range(n)); ax2.set_yticklabels([x_labels[i][:20] for i in range(n)], fontsize=7)
    ax2.set_xlabel('Dominant factor delta-log', fontsize=10)
    ax2.set_title('Dominant factor per case', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
    fig.tight_layout()
    _write_csv(outdir, 'ionic_decomp_physics.csv',
               ['(phi-0.19)^0.5', 'CN^2', 'cov^0.5', 'f_p^3', 'C_blend', 'dominant'],
               x_labels, list(log_phi), list(log_cn), list(log_cov), list(log_fp), list(log_cb),
               [sorted([(l, v[i]-v[ref]) for l, v, _ in factors], key=lambda t: -abs(t[1]))[0][0]
                for i in range(n)])
    return _save(fig, outdir, "ionic_decomp_physics.png")


def _load_electronic_sigma(data_list):
    """Load electronic σ_full from full_metrics or network_conductivity.json."""
    vals = [0.0] * len(data_list)
    for i, d in enumerate(data_list):
        v = _get(d, "electronic_sigma_full_mScm", 0)
        if v and v > 0:
            vals[i] = v
        else:
            src = _get(d, "_source_path", "")
            if src:
                net_path = os.path.join(os.path.dirname(src), "network_conductivity.json")
                if os.path.exists(net_path):
                    try:
                        with open(net_path) as _nf:
                            nd = json.load(_nf)
                        vals[i] = nd.get("electronic_sigma_full_mScm", 0) or 0
                    except:
                        pass
    return vals


def _load_thermal_sigma(data_list):
    """Load thermal σ_full from full_metrics or network_conductivity.json."""
    vals = [0.0] * len(data_list)
    for i, d in enumerate(data_list):
        v = _get(d, "thermal_sigma_full_mScm", 0)
        if v and v > 0:
            vals[i] = v
        else:
            src = _get(d, "_source_path", "")
            if src:
                net_path = os.path.join(os.path.dirname(src), "network_conductivity.json")
                if os.path.exists(net_path):
                    try:
                        with open(net_path) as _nf:
                            nd = json.load(_nf)
                        vals[i] = nd.get("thermal_sigma_full_mScm", 0) or 0
                    except:
                        pass
    return vals


def plot_electronic_sigma(data_list, names, outdir):
    """Electronic conductivity from AM-AM network."""
    sigma_el = _load_electronic_sigma(data_list)
    if not any(s > 0 for s in sigma_el):
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    # Use NaN to break line at σ=0 cases (prevents cross-group connection)
    y_line = np.array([s if s > 0 else np.nan for s in sigma_el])
    x_none = [x[i] for i in range(len(names)) if sigma_el[i] <= 0]

    ax.plot(x, y_line, 's-', color='#e74c3c', markersize=ms, linewidth=lw,
            label="σ_electronic (mS/cm)")
    if x_none:
        ax.plot(x_none, [0]*len(x_none), 'x', color='gray', markersize=ms+2,
                label="No AM percolation")

    _apply_style(ax, "σ_electronic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("Electronic Conductivity (AM-AM Network)\nσ_AM = 0.05 S/cm",
                 fontsize=10, fontweight='bold')

    # Annotation: range
    valid_vals = [s for s in sigma_el if s > 0]
    if valid_vals:
        ax.text(0.95, 0.95, f"Range: {min(valid_vals):.2f} ~ {max(valid_vals):.2f} mS/cm",
                transform=ax.transAxes, fontsize=9, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffeaea', alpha=0.8))

    _write_csv(outdir, 'electronic_sigma.csv',
               ['σ_electronic(mS/cm)'], names, sigma_el)
    return _save(fig, outdir, "electronic_sigma.png")


def plot_thermal_sigma(data_list, names, outdir):
    """Thermal conductivity from ALL-contact network."""
    sigma_th = _load_thermal_sigma(data_list)
    if not any(s > 0 for s in sigma_th):
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    ax.plot(x, sigma_th, 's-', color='#ff922b', markersize=ms, linewidth=lw,
            label="k_eff (mS/cm equiv.)")

    _apply_style(ax, "k_eff (thermal, mS/cm equiv.)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("Thermal Conductivity (ALL Contact Network)\nk_AM=4.0e-2, k_SE=0.7e-2 W/(cm·K)",
                 fontsize=10, fontweight='bold')

    valid_vals = [s for s in sigma_th if s > 0]
    if valid_vals:
        ax.text(0.95, 0.95, f"Range: {min(valid_vals):.2f} ~ {max(valid_vals):.2f}",
                transform=ax.transAxes, fontsize=9, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3e0', alpha=0.8))

    _write_csv(outdir, 'thermal_sigma.csv',
               ['k_eff(mS/cm)'], names, sigma_th)
    return _save(fig, outdir, "thermal_sigma.png")


def plot_electronic_scaling(data_list, names, outdir):
    """Electronic 2-regime scaling: thick (topology) + thin (contact mechanics)."""
    SIGMA_AM = 50.0
    phi_am = [_get(d, "phi_am") for d in data_list]
    cn_am = [_get(d, "am_am_cn") for d in data_list]
    thickness = [_get(d, "thickness_um") for d in data_list]
    d_am_list = [2.0 * max(_get(d, "r_AM_P", 0), _get(d, "r_AM_S", 0), _get(d, "r_AM", 0))
                 for d in data_list]
    tau = [max(_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)), 0.1) for d in data_list]
    cov_list = [(lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)(
        [v for v in [_get(d,"coverage_AM_P_mean",0), _get(d,"coverage_AM_S_mean",0),
                     _get(d,"coverage_AM_mean",0)] if v > 0]) for d in data_list]
    am_delta = [max(_get(d, "am_am_mean_delta", 0), 0.001) for d in data_list]
    am_area = [max(_get(d, "am_am_mean_area", 0), 0.01) for d in data_list]
    am_hop = [max(_get(d, "am_am_mean_hop", 0), 0.1) for d in data_list]
    am_gc = [max(_get(d, "am_path_conductance_mean", 0), 0.001) for d in data_list]
    porosity = [max(_get(d, "porosity", 10), 0.1) for d in data_list]
    phi_se = [max(_get(d, "phi_se", 0.2), 0.01) for d in data_list]
    el_perc = [max(_get(d, "electronic_percolating_fraction", 0), 0.01) for d in data_list]
    el_act = [max(_get(d, "electronic_active_fraction", 0), 0.01) for d in data_list]
    sigma_net = _load_electronic_sigma(data_list)

    # --- Fit C globally on ALL electronic data (thick/thin separate) ---
    # Use screening_electronic_sweep.load_all_electronic() for reliable dedup
    import importlib.util as _ilu
    _sweep_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screening_electronic_sweep.py')
    _spec = _ilu.spec_from_file_location("sweep", _sweep_path)
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _unique = _mod.load_all_electronic()

    # Fit C_thick and C_thin separately
    # Load mixing parameter for bimodal correction
    for r in _unique:
        _m2 = json.load(open(os.path.join(r['path'], 'full_metrics.json')))
        _nP = _m2.get('n_AM_P', 0); _nS = _m2.get('n_AM_S', 0)
        _rP = max(_m2.get('r_AM_P', 0), 0.1); _rS = max(_m2.get('r_AM_S', 0), 0.1)
        _vP = _nP * _rP**3; _vS = _nS * _rS**3; _vT = max(_vP + _vS, 0.001)
        r['fP_vol'] = _vP / _vT
        r['mix'] = 4 * r['fP_vol'] * (1 - r['fP_vol'])  # symmetric: 0=mono, 1=50:50

    # Load contact info + G_holm for each case
    for r in _unique:
        _m2 = json.load(open(os.path.join(r['path'], 'full_metrics.json')))
        _nP = _m2.get('n_AM_P', 0); _nS = _m2.get('n_AM_S', 0)
        _rP = max(_m2.get('r_AM_P', 0), 0.1); _rS = max(_m2.get('r_AM_S', 0), 0.1)
        _vP = _nP * _rP**3; _vS = _nS * _rS**3; _vT = max(_vP + _vS, 0.001)
        r['fP_vol'] = _vP / _vT
        # G_holm: Holm conductance-weighted CN
        _n_pp = _m2.get('area_AM_P_AM_P_n', 0) or 0
        _n_ps = _m2.get('area_AM_P_AM_S_n', 0) or 0
        _n_ss = _m2.get('area_AM_S_AM_S_n', 0) or 0
        _a_pp = _m2.get('area_AM_P_AM_P_mean', 0) or 0
        _a_ps = _m2.get('area_AM_P_AM_S_mean', 0) or 0
        _a_ss = _m2.get('area_AM_S_AM_S_mean', 0) or 0
        _nAM = max(_nP + _nS, 1)
        _th = _n_pp*np.sqrt(max(_a_pp,0.001)) + _n_ps*np.sqrt(max(_a_ps,0.001)) + _n_ss*np.sqrt(max(_a_ss,0.001))
        r['g_holm'] = max(_th / _nAM, 0.01) if _th > 0 else r['cn']
        r['g_total'] = _th if _th > 0 else r['cn'] * _nAM  # total Holm sum
        # A_min: smallest non-zero contact type area (bottleneck indicator)
        _areas = [a for a,n in [(_a_pp,_n_pp),(_a_ps,_n_ps),(_a_ss,_n_ss)] if n > 0 and a > 0]
        r['a_min'] = min(_areas) if _areas else 0.01

    C_thick = 1.0; C_thin = 1.0
    if len(_unique) >= 5:
        _s = np.array([r['sigma'] for r in _unique])
        _cn = np.array([r['cn'] for r in _unique])
        _ratio = np.array([r['ratio'] for r in _unique])
        _por = np.array([r['por'] for r in _unique])
        _delta = np.array([r['delta'] for r in _unique])
        _pa = np.array([r['phi_am'] for r in _unique])
        _gh = np.array([r.get('g_holm', r['cn']) for r in _unique])

        _tk = _ratio >= 8; _tn = _ratio < 8
        if _tk.sum() >= 3:
            # Thick: CN^1.5 × G_holm^0.25 × (φ-φc)² / por^0.35 × exp(-0.05×logCN×logG_h)
            _phi_ex_tk = np.clip(_pa[_tk] - 0.10, 0.001, None)
            _log_cn_tk = np.log(_cn[_tk]); _log_gh_tk = np.log(_gh[_tk])
            _log_phi_tk = np.log(_phi_ex_tk)
            _rhs_tk = SIGMA_AM * np.sqrt(_cn[_tk]) * np.sqrt(_gh[_tk]) * _phi_ex_tk**3 / _por[_tk]**0.25 * np.exp(-0.75*_log_cn_tk*_log_phi_tk - 0.25*_log_gh_tk**2)
            C_thick = float(np.exp(np.mean(np.log(_s[_tk]) - np.log(_rhs_tk))))
        if _tn.sum() >= 3:
            _delta_tn = _delta[_tn]
            _rhs_tn = SIGMA_AM * _cn[_tn] * _delta_tn**0.5 / _ratio[_tn]**0.5
            C_thin = float(np.exp(np.mean(np.log(_s[_tn]) - np.log(_rhs_tn))))

    # ── Global R² from ALL data (not just this comparison group) ──
    r2_global_tk = 0; r2_global_tn = 0; n_global_tk = 0; n_global_tn = 0
    if len(_unique) >= 5:
        _s_all = np.array([r['sigma'] for r in _unique])
        _ratio_all = np.array([r['ratio'] for r in _unique])
        # Thick global R²
        _tk_mask = _ratio_all >= 8
        if _tk_mask.sum() >= 3:
            _cn_g = np.log(np.array([r['cn'] for r in _unique])[_tk_mask])
            _pa_g = np.array([r['phi_am'] for r in _unique])[_tk_mask]
            _phi_ex_g = np.clip(_pa_g - 0.10, 0.001, None)
            _por_g = np.array([r['por'] for r in _unique])[_tk_mask]
            _gh_g = np.array([r.get('g_holm', r['cn']) for r in _unique])[_tk_mask]
            _log_phi_g = np.log(_phi_ex_g)
            _log_gh_g = np.log(_gh_g)
            _pred_tk = C_thick * SIGMA_AM * np.exp(_cn_g)**0.5 * _gh_g**0.5 * _phi_ex_g**3 / _por_g**0.25 * np.exp(-0.75*_cn_g*_log_phi_g - 0.25*_log_gh_g**2)
            _log_a = np.log(_s_all[_tk_mask]); _log_p = np.log(_pred_tk)
            _ss_res = np.sum((_log_a - _log_p)**2); _ss_tot = np.sum((_log_a - np.mean(_log_a))**2)
            r2_global_tk = 1 - _ss_res / _ss_tot if _ss_tot > 0 else 0
            n_global_tk = int(_tk_mask.sum())
        # Thin global R²
        _tn_mask = _ratio_all < 8
        _ep_all = np.array([r['ep'] for r in _unique])
        _tn_perc = _tn_mask & (_ep_all >= 0.50)
        if _tn_perc.sum() >= 3:
            _cn_tn = np.array([r['cn'] for r in _unique])[_tn_perc]
            _delta_tn = np.array([r['delta'] for r in _unique])[_tn_perc]
            _ratio_tn = _ratio_all[_tn_perc]
            _pred_tn = C_thin * SIGMA_AM * _cn_tn * _delta_tn**0.5 / _ratio_tn**0.5
            _log_a = np.log(_s_all[_tn_perc]); _log_p = np.log(_pred_tn)
            _ss_res = np.sum((_log_a - _log_p)**2); _ss_tot = np.sum((_log_a - np.mean(_log_a))**2)
            r2_global_tn = 1 - _ss_res / _ss_tot if _ss_tot > 0 else 0
            n_global_tn = int(_tn_perc.sum())

    # Compute per-case G_holm and A_min
    case_g_holm = []; case_g_total = []; case_a_min = []
    for d in data_list:
        _nP = _get(d, "n_AM_P", 0) or 0; _nS = _get(d, "n_AM_S", 0) or 0
        _n_pp = _get(d, "area_AM_P_AM_P_n", 0) or 0
        _n_ps = _get(d, "area_AM_P_AM_S_n", 0) or 0
        _n_ss = _get(d, "area_AM_S_AM_S_n", 0) or 0
        _a_pp = _get(d, "area_AM_P_AM_P_mean", 0) or 0
        _a_ps = _get(d, "area_AM_P_AM_S_mean", 0) or 0
        _a_ss = _get(d, "area_AM_S_AM_S_mean", 0) or 0
        _nAM = max(_nP + _nS, 1)
        _th = _n_pp*np.sqrt(max(_a_pp,0.001)) + _n_ps*np.sqrt(max(_a_ps,0.001)) + _n_ss*np.sqrt(max(_a_ss,0.001))
        case_g_holm.append(max(_th / _nAM, 0.01) if _th > 0 else cn_am[len(case_g_holm)] if len(case_g_holm) < len(cn_am) else 1.0)
        case_g_total.append(_th if _th > 0 else (cn_am[len(case_g_total)] * _nAM if len(case_g_total) < len(cn_am) else 1.0))
        _areas = [a for a,n in [(_a_pp,_n_pp),(_a_ps,_n_ps),(_a_ss,_n_ss)] if n > 0 and a > 0]
        case_a_min.append(min(_areas) if _areas else 0.01)

    # Compute predictions per case
    sigma_scaling = []
    for i in range(len(data_list)):
        if phi_am[i] > 0 and cn_am[i] > 0 and d_am_list[i] > 0 and thickness[i] > 0:
            ratio_i = thickness[i] / d_am_list[i]
            if ratio_i >= 8:
                # THICK: CN^1.5 × G_holm^0.25 × (φ-φc)² / por^0.35
                phi_ex_i = max(phi_am[i] - 0.10, 0.001)
                _gh_i = max(case_g_holm[i], 0.01)
                _log_cn_i = np.log(cn_am[i]); _log_gh_i = np.log(_gh_i); _log_phi_i = np.log(phi_ex_i)
                _correction = np.exp(-0.75*_log_cn_i*_log_phi_i - 0.25*_log_gh_i**2)
                s = C_thick * SIGMA_AM * np.sqrt(cn_am[i]) * np.sqrt(_gh_i) * phi_ex_i**3 / porosity[i]**0.25 * _correction
            else:
                # THIN: CN × δ^0.5 / √(T/d)
                if el_perc[i] >= 0.50:
                    s = C_thin * SIGMA_AM * cn_am[i] * am_delta[i]**0.5 / ratio_i**0.5
                else:
                    s = 0.0
            sigma_scaling.append(s)
        else:
            sigma_scaling.append(0.0)

    has_net = any(s > 0 for s in sigma_net)
    if not has_net and not any(s > 0 for s in sigma_scaling):
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    y_scaling = np.array([s if s > 0 else np.nan for s in sigma_scaling])
    y_net = np.array([s if s > 0 else np.nan for s in sigma_net]) if has_net else None

    ax.plot(x, y_scaling, 's-', color=RED, markersize=ms, linewidth=lw,
            label="Scaling law")
    # ±13% error band (DEM stochastic variability, 1σ from residual)
    _err_frac = 0.13
    y_lo = y_scaling * (1 - _err_frac)
    y_hi = y_scaling * (1 + _err_frac)
    ax.fill_between(x, y_lo, y_hi, color=RED, alpha=0.12, label='±13% band')
    if has_net and y_net is not None:
        ax.plot(x, y_net, 'D--', color='#2ecc71', markersize=ms-2, linewidth=lw-0.5,
                alpha=0.7, label="Network solver")

    _apply_style(ax, "σ_electronic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')

    # R² (log-space) — this group only (for display)
    valid_both = [i for i in range(len(names)) if sigma_net[i] > 0 and sigma_scaling[i] > 0]
    if len(valid_both) >= 3:
        sa = np.array([sigma_net[i] for i in valid_both])
        sp = np.array([sigma_scaling[i] for i in valid_both])
        errs = np.abs(sp - sa) / sa * 100
        w20 = np.sum(errs < 20)
    else:
        errs = np.array([0]); w20 = 0

    n_total = n_global_tk + n_global_tn
    ax.set_title(f"Electronic 2-Regime Scaling Law\n"
                 f"Thick R²={r2_global_tk:.3f}(n={n_global_tk}), Thin R²={r2_global_tn:.3f}(n={n_global_tn})",
                 fontsize=9, fontweight='bold')

    # Formula box with global R²
    txt = (f"Thick: G_h-primary + interactions R²={r2_global_tk:.3f}(n={n_global_tk})\n"
           f"Thin: CN×√δ/√(T/d) R²={r2_global_tn:.3f}(n={n_global_tn})\n"
           f"Group |err|={np.mean(errs):.0f}%, ≤20%: {w20}/{len(valid_both)}")
    ax.text(0.95, 0.95, txt, transform=ax.transAxes, fontsize=7, ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffeaea', alpha=0.8))

    _write_csv(outdir, 'electronic_scaling.csv',
               ['σ_scaling(mS/cm)', 'σ_network(mS/cm)'],
               names, sigma_scaling, sigma_net)
    return _save(fig, outdir, "electronic_scaling.png")


def plot_thermal_scaling(data_list, names, outdir):
    """Thermal scaling law: σ_th = 286 × σ_ion^(3/4) × φ_AM² / CN_SE."""
    C_th = 286.0

    sigma_ion = _load_network_sigma(data_list)
    phi_am = [_get(d, "phi_am") for d in data_list]
    cn_se = [_get(d, "se_se_cn") for d in data_list]

    sigma_scaling = []
    for i in range(len(data_list)):
        if sigma_ion[i] > 0 and phi_am[i] > 0 and cn_se[i] > 0:
            s = C_th * sigma_ion[i]**(3/4) * phi_am[i]**2 / cn_se[i]
            sigma_scaling.append(s)
        else:
            sigma_scaling.append(0.0)

    # Network solver for comparison
    sigma_net = _load_thermal_sigma(data_list)
    has_net = any(s > 0 for s in sigma_net)

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    # Use NaN to break line at σ=0 cases
    y_scaling = np.array([s if s > 0 else np.nan for s in sigma_scaling])
    y_net = np.array([s if s > 0 else np.nan for s in sigma_net]) if has_net else None

    ax.plot(x, y_scaling, 's-', color='#ff922b', markersize=ms, linewidth=lw,
            label="Scaling law (mS/cm)")
    if has_net and y_net is not None:
        ax.plot(x, y_net, 'D--', color='#2ecc71', markersize=ms-2, linewidth=lw-0.5,
                alpha=0.7, label="Network solver (mS/cm)")

    _apply_style(ax, "\u03c3_th (mS/cm equiv.)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("Thermal: \u03c3_th = 286 \u00d7 \u03c3_ion^(3/4) \u00d7 \u03c6_AM\u00b2 / CN_SE\n"
                 "R\u00b2=0.90, 1 free param",
                 fontsize=9, fontweight='bold')

    # Annotation box
    valid_scaling = [s for s in sigma_scaling if s > 0]
    if valid_scaling:
        txt = ("R\u00b2 = 0.90\n"
               "\u03c3_th = 286 \u00d7 \u03c3_ion^(3/4) \u00d7 \u03c6_AM\u00b2 / CN_SE")
        ax.text(0.95, 0.95, txt,
                transform=ax.transAxes, fontsize=8, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3e0', alpha=0.8))

    _write_csv(outdir, 'thermal_scaling.csv',
               ['\u03c3_ion(mS/cm)', 'phi_AM', 'CN_SE', '\u03c3_scaling(mS/cm)', '\u03c3_network(mS/cm)'],
               names, sigma_ion, phi_am, cn_se, sigma_scaling, sigma_net)
    return _save(fig, outdir, "thermal_scaling.png")


def plot_transport_tradeoff(data_list, names, outdir):
    """Ionic vs Electronic trade-off: dual Y-axis showing inverse relationship."""
    sigma_ionic = _load_network_sigma(data_list)
    sigma_el = _load_electronic_sigma(data_list)

    if not any(s > 0 for s in sigma_ionic) or not any(s > 0 for s in sigma_el):
        return None

    fig, ax1 = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    # Ionic on left Y
    color_ion = '#2ecc71'
    ax1.plot(x, sigma_ionic, 's-', color=color_ion, markersize=ms, linewidth=lw,
             label="σ_ionic")
    ax1.set_ylabel("σ_ionic (mS/cm)", color=color_ion, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color_ion)

    # Electronic on right Y
    ax2 = ax1.twinx()
    color_el = '#e74c3c'
    y_el = np.array([s if s > 0 else np.nan for s in sigma_el])
    no_el = [i for i in range(len(names)) if sigma_el[i] == 0]
    ax2.plot(x, y_el, 'D-', color=color_el, markersize=ms, linewidth=lw, label="σ_electronic")
    if no_el:
        ax2.plot([x[i] for i in no_el], [0]*len(no_el), 'x', color='gray', markersize=ms-2)
    ax2.set_ylabel("σ_electronic (mS/cm)", color=color_el, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color_el)

    _apply_style(ax1, "", names)
    ax1.set_title("Ionic vs Electronic Conductivity Trade-off\n(↑ AM → ↑ electronic, ↓ ionic)",
                  fontsize=10, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')

    _write_csv(outdir, 'transport_tradeoff.csv',
               ['σ_ionic(mS/cm)', 'σ_electronic(mS/cm)'],
               names, sigma_ionic, sigma_el)
    return _save(fig, outdir, "transport_tradeoff.png")


def plot_transport_normalized(data_list, names, outdir):
    """3-mode normalized comparison: ionic/electronic/thermal on same scale."""
    sigma_ionic = _load_network_sigma(data_list)
    sigma_el = _load_electronic_sigma(data_list)
    sigma_th = _load_thermal_sigma(data_list)

    has_ionic = any(s > 0 for s in sigma_ionic)
    has_el = any(s > 0 for s in sigma_el)
    has_th = any(s > 0 for s in sigma_th)

    if not has_ionic:
        return None

    # Normalize each to its own max
    def _norm(arr):
        mx = max(arr) if max(arr) > 0 else 1
        return [v / mx for v in arr]

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))
    w = 0.25

    if has_ionic:
        norm_ion = _norm(sigma_ionic)
        ax.bar(x - w, norm_ion, w, color='#2ecc71', alpha=0.8, label=f"Ionic (max={max(sigma_ionic):.2f})")
    if has_el:
        norm_el = _norm(sigma_el)
        ax.bar(x, norm_el, w, color='#e74c3c', alpha=0.8, label=f"Electronic (max={max(sigma_el):.2f})")
    if has_th:
        norm_th = _norm(sigma_th)
        ax.bar(x + w, norm_th, w, color='#ff922b', alpha=0.8, label=f"Thermal (max={max(sigma_th):.2f})")

    _apply_style(ax, "Normalized σ (ratio to max)", names)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_ylim(0, 1.15)
    ax.set_title("3-Mode Transport Comparison (Normalized)\nIonic (SE-SE) | Electronic (AM-AM) | Thermal (ALL)",
                 fontsize=10, fontweight='bold')

    _write_csv(outdir, 'transport_normalized.csv',
               ['ionic(mS/cm)', 'electronic(mS/cm)', 'thermal(mS/cm)'],
               names, sigma_ionic, sigma_el, sigma_th)
    return _save(fig, outdir, "transport_normalized.png")


def plot_transport_absolute(data_list, names, outdir):
    """3-mode absolute values on log scale."""
    sigma_ionic = _load_network_sigma(data_list)
    sigma_el = _load_electronic_sigma(data_list)
    sigma_th = _load_thermal_sigma(data_list)

    has_ionic = any(s > 0 for s in sigma_ionic)
    has_el = any(s > 0 for s in sigma_el)
    has_th = any(s > 0 for s in sigma_th)

    if not has_ionic:
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    if has_ionic:
        ax.plot(x, sigma_ionic, 's-', color='#2ecc71', markersize=ms, linewidth=lw,
                label="Ionic (SE-SE)")
    if has_el:
        y_el_abs = np.array([s if s > 0 else np.nan for s in sigma_el])
        ax.plot(x, y_el_abs, 'D-', color='#e74c3c', markersize=ms, linewidth=lw,
                label="Electronic (AM-AM)")
    if has_th:
        ax.plot(x, sigma_th, '^-', color='#ff922b', markersize=ms, linewidth=lw,
                label="Thermal (ALL)")

    ax.set_yscale('log')
    _apply_style(ax, "σ_ionic (mS/cm, log scale)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("3-Mode Transport: Absolute Values\nIonic ≪ Thermal < Electronic (typical)",
                 fontsize=10, fontweight='bold')

    # Minnmann reference line
    ax.axhline(0.17, color='gray', linestyle=':', linewidth=1, alpha=0.6)
    ax.text(len(names)-0.5, 0.17, "Minnmann 0.17", fontsize=7, color='gray', va='bottom', ha='right')

    _write_csv(outdir, 'transport_absolute.csv',
               ['ionic(mS/cm)', 'electronic(mS/cm)', 'thermal(mS/cm)'],
               names, sigma_ionic, sigma_el, sigma_th)
    return _save(fig, outdir, "transport_absolute.png")


def plot_r_brug_comparison(data_list, names, outdir):
    """R_brug for ionic vs electronic vs thermal — how much does Bruggeman overestimate?"""
    # Ionic R_brug
    r_ionic = []
    for d in data_list:
        v = _get(d, "R_brug_over_full", 0)
        r_ionic.append(v if v > 0 else 0)

    # Electronic R_brug
    r_el = []
    for i, d in enumerate(data_list):
        v = _get(d, "electronic_R_brug", 0)
        if v and v > 0:
            r_el.append(v)
        else:
            src = _get(d, "_source_path", "")
            if src:
                net_path = os.path.join(os.path.dirname(src), "network_conductivity.json")
                if os.path.exists(net_path):
                    try:
                        with open(net_path) as _nf:
                            nd = json.load(_nf)
                        r_el.append(nd.get("electronic_R_brug", 0) or 0)
                    except:
                        r_el.append(0)
                else:
                    r_el.append(0)
            else:
                r_el.append(0)

    # Thermal R_brug
    r_th = []
    for i, d in enumerate(data_list):
        v = _get(d, "thermal_R_brug", 0)
        if v and v > 0:
            r_th.append(v)
        else:
            src = _get(d, "_source_path", "")
            if src:
                net_path = os.path.join(os.path.dirname(src), "network_conductivity.json")
                if os.path.exists(net_path):
                    try:
                        with open(net_path) as _nf:
                            nd = json.load(_nf)
                        r_th.append(nd.get("thermal_R_brug", 0) or 0)
                    except:
                        r_th.append(0)
                else:
                    r_th.append(0)
            else:
                r_th.append(0)

    has_ionic = any(r > 0 for r in r_ionic)
    has_el = any(r > 0 for r in r_el)
    has_th = any(r > 0 for r in r_th)

    if not has_ionic:
        return None

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))
    w = 0.25

    if has_ionic:
        ax.bar(x - w, r_ionic, w, color='#2ecc71', alpha=0.8, label="Ionic R_brug")
    if has_el:
        ax.bar(x, r_el, w, color='#e74c3c', alpha=0.8, label="Electronic R_brug")
    if has_th:
        ax.bar(x + w, r_th, w, color='#ff922b', alpha=0.8, label="Thermal R_brug")

    ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(len(names)-0.5, 1.05, "Bruggeman = exact", fontsize=7, color='gray', ha='right')

    _apply_style(ax, "R_brug (σ_brug / σ_network)", names)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_title("Bruggeman Overestimation by Transport Mode\nR_brug > 1 = Bruggeman overestimates",
                 fontsize=10, fontweight='bold')

    _write_csv(outdir, 'r_brug_comparison.csv',
               ['R_ionic', 'R_electronic', 'R_thermal'],
               names, r_ionic, r_el, r_th)
    return _save(fig, outdir, "r_brug_comparison.png")


def plot_ion_path_quality(data_list, names, outdir):
    """Ion path quality: GB Density, Hop Area, Bottleneck, Conductance (2x2)."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    x = np.arange(len(names))

    # GB Density (lower is better)
    vals = [_get(d, "gb_density_mean") for d in data_list]
    axes[0,0].plot(x, vals, 's-', color=BLUE, markersize=8, linewidth=2)
    _apply_style(axes[0,0], "GB Density (hops/μm)", names)
    axes[0,0].set_title("Grain Boundary Density (GB_d)  ↓ better", fontsize=10, fontweight='bold')

    # Path Hop Area mean (higher is better)
    vals = [_get(d, "path_hop_area_mean") for d in data_list]
    axes[0,1].plot(x, vals, 's-', color=ORANGE, markersize=8, linewidth=2)
    _apply_style(axes[0,1], "Hop Area mean (μm²)", names)
    axes[0,1].set_title("Path Hop Area  (↑ better)", fontsize=10, fontweight='bold')

    # Bottleneck (higher is better)
    vals = [_get(d, "path_hop_area_min_mean") for d in data_list]
    axes[1,0].plot(x, vals, 's-', color=RED, markersize=8, linewidth=2)
    _apply_style(axes[1,0], "Bottleneck (μm²)", names)
    axes[1,0].set_title("Path Bottleneck  (↑ better)", fontsize=10, fontweight='bold')

    # Path Conductance (higher is better)
    vals = [_get(d, "path_conductance_mean") for d in data_list]
    axes[1,1].plot(x, vals, 's-', color=GREEN, markersize=8, linewidth=2)
    _apply_style(axes[1,1], "Conductance (μm²)", names)
    axes[1,1].set_title("Path Conductance (G_path)  (↑ better)", fontsize=10, fontweight='bold')

    gb = [_get(d, "gb_density_mean") for d in data_list]
    ha = [_get(d, "path_hop_area_mean") for d in data_list]
    bn = [_get(d, "path_hop_area_min_mean") for d in data_list]
    gc = [_get(d, "path_conductance_mean") for d in data_list]
    _write_csv(outdir, 'ion_path_quality.csv',
               ['GB Density(hops/μm)', 'Hop Area mean(μm²)', 'Bottleneck(μm²)', 'Conductance(μm²)'],
               names, gb, ha, bn, gc)

    _break_lines_at_groups(fig)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.suptitle("Ion Path Quality", fontsize=14, fontweight='bold', x=0.5, y=0.99, ha='center')
    path = os.path.join(outdir, "ion_path_quality.png")
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor='white', pad_inches=0.3)
    plt.close(fig)
    return path


# ─── Plot dispatch table ─────────────────────────────────────────────────────

PLOT_REGISTRY = {
    "porosity": {
        "func": plot_porosity,
        "file": "porosity.png",
        "title": "Porosity",
        "description": "AM_P 비율 증가에 따른 기공률 변화.\n7:3 부근에서 최저 (bimodal packing 효과).\nV\u2011shape 경향이면 최적 조성 존재.",
        "origin_tip": "Line+Symbol → X: P:S Configuration, Y: Porosity(%).\nSymbol: Square (size 10), Color: Black.\nLine: B-Spline, Width 1.5.\nY축 범위: 자동 ± 1%p 여유.",
    },
    "am_se_interface": {
        "func": plot_am_se_interface,
        "file": "am_se_interface.png",
        "title": "AM-SE Interface Area",
        "description": "AM_P\u2011SE와 AM_S\u2011SE 접촉 면적을\nStacked Bar로 비교.\nAM_P 비율 증가 → AM_P\u2011SE 증가, AM_S\u2011SE 감소.\n전체 AM\u2011SE Total은 S only에서 최대.",
        "origin_tip": "Stacked Bar → X: Configuration, Y: Interface Area (μm²).\nColumn1: AM_P-SE (Dark Green #548235).\nColumn2: AM_S-SE (Light Green #A9D18E).\nLegend 우상단.",
    },
    "se_se_tradeoff": {
        "func": plot_se_se_tradeoff,
        "file": "se_se_tradeoff.png",
        "title": "SE-SE Contact Trade-off",
        "description": "SE-SE 접촉 개수(bar)와 개별 접촉 평균 면적(line)의 trade-off.\n\nAM_P↑ → SE가 넓은 공간에 분산 → 접촉 수↑ + 개별 면적↓\n= 악수 약한 사람 10명 vs 악수 센 사람 3명",
        "origin_tip": "Double-Y Axis → Left: Bar (Contact Count, Blue #4472C4).\nRight: Line+Symbol (Mean Area μm², Red #C00000, Square).\nX: Configuration.",
    },
    "se_se_total": {
        "func": plot_se_se_total,
        "file": "se_se_total.png",
        "title": "SE-SE Total Contact Area",
        "description": "SE-SE 전체 접촉 면적 = N × Mean.\n7:3 부근에서 최대 → N 증가가 Mean 감소를 압도.\n10:0에서 감소 시작 → 과도한 AM_P는 SE 품질 저하.",
        "origin_tip": "Line+Symbol → X: Configuration, Y: Total Area (μm²).\nSymbol: Square (Gray), Line: Solid.\n최대값에 Annotation arrow (Red).",
    },
    "percolation_tortuosity": {
        "func": plot_percolation_tortuosity,
        "file": "percolation_tortuosity.png",
        "title": "Percolation & Tortuosity",
        "description": "이온 전도 경로 형성률(Percolation %)과 경로 꼬임(Tortuosity).\n\nPercolation↑ + Tortuosity↓ = 좋은 이온 경로.\nAM_P↑ → 둘 다 개선 (넓은 SE 공간).",
        "origin_tip": "Double-Y Axis → Left: Percolation % (Blue, Square).\nRight: Tortuosity (Red, Triangle).\n범례: 좌측/우측 분리.",
    },
    "ionic_active": {
        "func": plot_ionic_active,
        "file": "ionic_active.png",
        "title": "Ionic Active AM Fraction",
        "description": "Top(SE pellet)에서 이온이 도달 가능한 AM 비율.\n\n100% = 모든 AM이 이온 경로에 연결.\nDead zone(빨강) = SE 미연결 → 반응 불가 AM.",
        "origin_tip": "Line+Fill plot → X: Configuration, Y: Ionic Active (%).\nGreen fill: Active zone (0 ~ line).\nRed fill: Dead zone (line ~ 100).\nY축: 95~100 확대 권장.",
    },
    "coverage": {
        "func": plot_coverage,
        "file": "coverage.png",
        "title": "AM Coverage",
        "description": "AM 표면의 SE 피복률.\n= (SE 접촉 면적) / (AM 자유 표면적) × 100%\n\nAM_P가 클수록 SE 접촉 면적↑ → Coverage↑.\nError bar = 입자 간 편차(std).",
        "origin_tip": "Grouped Bar + Error Bar.\nAM_P: Green #548235, AM_S: Light Green #A9D18E.\nCap size 4, Line width 1.2.\nX: Configuration, Y: Coverage (%).",
    },
    "stress_cv": {
        "func": plot_stress_cv,
        "file": "stress_cv.png",
        "title": "Stress CV",
        "description": "Von Mises 응력 변동계수(CV).\n\nCV 낮을수록 전극 내 응력이 균일.\n유효영률 사용으로 절대값은 참고용, 상대 비교만 유효.",
        "origin_tip": "Line+Symbol → X: P:S, Y: VM CV (%).\nSymbol: Square, Black.\nCV < 100%면 양호.",
    },
    "stress_ratio": {
        "func": plot_stress_ratio,
        "file": "stress_ratio.png",
        "title": "Stress Ratio by Type",
        "description": "입자 유형별 응력 비율 (σ_type / σ_mean).\n\n> 1.0 = 평균보다 응력 집중\n< 1.0 = 평균보다 하중 적음\n\nSE > 1.0이면 SE에 응력 집중 → 소성변형 유발.",
        "origin_tip": "Multi-line → X: P:S, Y: σ/σ_mean.\nAM_P: Red, AM_S: Orange, SE: Green.\ny=1.0에 점선 (mean baseline).",
    },
    "se_network": {
        "func": plot_se_network,
        "file": "se_network.png",
        "title": "SE Network",
        "description": "SE-SE 배위수(CN)와 클러스터 수.\nCN = SE 입자 하나가 접촉하는 SE 이웃 수\nCN↑ = 조밀한 네트워크 (CN≥4: 안정적 3D percolation)\nCluster↓ = 분절 적음. Large(≥10) 클러스터만 이온 경로에 유의미.",
        "origin_tip": "Dual-Y → Left: Line (CN, Blue).\nRight: Bar (Clusters, Orange).",
    },
    "contact_force": {
        "func": plot_contact_force,
        "file": "contact_force.png",
        "title": "Contact Force",
        "description": "접촉 유형별(AM-AM, AM-SE, SE-SE) 법선력 평균.\nFn = √(fn_x² + fn_y² + fn_z²), 단위: μN\nF_real = F_sim / scale²\n대립자 간 접촉력이 가장 크며, P:S 변화에 따라 하중 분담 변화 관찰.",
        "origin_tip": "Grouped Bar → X: Configuration, Y: Fn mean (μN).\nAM-AM: Red, AM-SE: Green, SE-SE: Blue.",
    },
    "contact_pressure": {
        "func": plot_contact_pressure,
        "file": "contact_pressure.png",
        "title": "Contact Pressure",
        "description": "접촉 압력 P = Fn / A_contact (MPa).\n같은 힘이라도 면적이 작으면 압력↑.\nMax는 failure 시작점, Mean은 전체 경향.",
        "origin_tip": "Dual Bar → X: Configuration, Y: Pressure (MPa).\nMean: Blue, Max: Red.",
    },
    "am_vulnerability": {
        "func": plot_am_vulnerability,
        "file": "am_vulnerability.png",
        "title": "AM Vulnerability",
        "description": "Vulnerable = (SE 0개 + SE 1개 접촉 AM) / 전체 AM × 100\nAM-SE CN = AM당 SE 접촉 수 평균\nVulnerable↓ + CN↑ = 안정적 이온 공급.\nSE 1개 접촉 = single point of failure.",
        "origin_tip": "Dual-Y → Left: Bar (Vulnerable %, Red).\nRight: Line (AM-SE CN, Blue).",
    },
    "effective_conductivity": {
        "func": plot_effective_conductivity,
        "file": "effective_conductivity.png",
        "title": "σ_brug/σ_grain (Bruggeman Estimate)",
        "description": "σ_brug/σ_grain = φ_SE × f_perc / τ²  (σ_grain = 3.0 mS/cm)\n\n접촉 저항(constriction) 무시 → 실제 Network Solver 대비 3~10× 과대추정.\nNetwork Solver σ_ionic이 ground truth.",
        "origin_tip": "Line+Symbol (Green) + Bar (φ_SE, Blue).",
    },
    "rgb_fitting": {
        "func": plot_rgb_fitting,
        "file": "rgb_fitting.png",
        "title": "[Legacy] BLM+Constriction Fitting (Part I proxy)",
        "description": "⚠ Legacy: FORM X로 대체됨\nProxy: R = σ_brug/σ_proxy = C×(GB_d²×T)^α\nSingle\u2011path 근사 → R=15~1600 (실제 3~10)\nBruggeman exponent 분해: n_eff = n_geo(2.54) + n_contact(0.83) = 3.37",
        "origin_tip": "Scatter + Fit line (log\u2011log).",
        "hidden": True,
    },
    "gb_corrected": {
        "func": plot_gb_corrected,
        "file": "gb_corrected.png",
        "title": "[Legacy] Proxy σ_eff (Part I)",
        "description": "⚠ Legacy: FORM X로 대체됨\nProxy 기반 보정 (single\u2011path 근사)\n절대값 과장 → Network solver가 ground truth",
        "origin_tip": "Line (Red, ratio) + Dashed (Orange, mS/cm).",
        "hidden": True,
    },
    "network_sigma": {
        "func": plot_network_sigma,
        "file": "network_sigma.png",
        "title": "Ionic: Network Solver σ_full (Part II)",
        "description": "Kirchhoff resistor network (R_bulk + R_constriction)\n초록: σ_full (ground truth) | 파란: σ_brug (Bruggeman)\nR_brug = 3~10× | Constriction 69~81% 지배\nMinnmann(2021) 0.17 mS/cm과 same order\nσ_grain = 3.0 mS/cm (grain interior, not pellet)",
        "origin_tip": "Green: Network solver, Blue dashed: Bruggeman.",
    },
    "ionic_scaling_fit": {
        "func": plot_ionic_scaling_fit,
        "file": "ionic_scaling_fit.png",
        "title": "Ionic: FORM X Scaling Law (Predicted vs Actual)",
        "description": "FORM X v9 BLEND:\nσ = [(1-w)·C_v5(τ) + w·C_p3(τ)] × σ_grain × CN^1.5 × (φ-φc)^¾ × ⁴√cov × fp²\nw(τ) = σ(15·(τ-2.0))  # sharp transition\nC_v5(τ) = sigmoid(thick→thin) — captures moderate τ\nC_p3(τ) = cubic in lnτ — captures extreme thin (τ>3)\n\nφ_c=0.185, 6 params (2 v5 + 4 poly3)\nR²={formx_r2}, LOOCV={formx_loocv}",
        "origin_tip": "Scatter (log-log): X=actual (Network solver), Y=predicted (FORM X).\n1:1 line (black dashed), ±20% band (green).",
    },
    "multiscale_sigma": {
        "func": plot_multiscale_sigma,
        "file": "multiscale_sigma.png",
        "title": "Ionic: FORM X Scaling Law",
        "description": "FORM X v9 BLEND:\nσ = C_blend(τ) × σ_grain × CN^1.5 × (φ\u2011φc)^¾ × ⁴√cov × fp²\nv5 sigmoid (τ<2) + poly3(lnτ) (τ≥2), smooth blend at τ=2.0\nv5 handles moderate, poly3 handles extreme thin (τ>3)\nR²={formx_r2}, w20=51/55",
        "origin_tip": "Red: FORM X prediction.\nGreen dashed: Network solver (ground truth).",
    },
    "formx_decomposition": {
        "func": plot_formx_decomposition,
        "file": "formx_decomposition.png",
        "csv": "formx_decomposition.csv",
        "title": "FORM X Factor Decomposition",
        "description": "FORM X v9 각 항의 상대 기여도:\n(φ\u2011φc)^¾: percolation excess\nCN^1.5: network connectivity\n⁴√cov: AM\u2011SE 계면\nC_blend(τ): v5 + poly3 혼합 regime\nfp²: SE percolation fraction\nref: 최고 σ case 기준",
        "origin_tip": "Stacked bar (top): factor contributions.\nHorizontal bar (bottom): dominant factor per case.",
    },
}


def plot_sigma_decomposition(data_list, names, outdir):
    """Decompose σ_eff into Bruggeman + contact terms. Show which factor dominates."""
    SIGMA_BULK = 3.0  # σ_grain (grain interior)
    C_ms = 0.073  # default, used only for reference σ_ms (decomposition is relative, C cancels out)

    sigma_brug = [_get(d, "sigma_ratio") for d in data_list]
    gb_dens = [_get(d, "gb_density_mean") for d in data_list]
    g_path = [_get(d, "path_conductance_mean", 0) for d in data_list]
    cn = [_get(d, "se_se_cn", 0) for d in data_list]
    phi = [_get(d, "phi_se") for d in data_list]
    tau = [_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)) for d in data_list]
    f_perc = [_get(d, "percolation_pct") / 100 for d in data_list]

    n = len(data_list)
    # Decompose log(σ_brug) = log(σ_grain) + log(φ_SE) + log(f_perc) - 2log(τ) + log(C) + 0.25*log(G_path*GB_d²) + 2log(CN)
    log_phi = np.array([np.log(phi[i]) if phi[i] > 0 else 0 for i in range(n)])
    log_fperc = np.array([np.log(f_perc[i]) if f_perc[i] > 0 else 0 for i in range(n)])
    log_tau2 = np.array([-2 * np.log(tau[i]) if tau[i] > 0 else 0 for i in range(n)])
    log_gpath_gbd = np.array([0.25 * np.log(g_path[i] * gb_dens[i]**2) if g_path[i] > 0 and gb_dens[i] > 0 else 0 for i in range(n)])
    log_cn2 = np.array([2 * np.log(cn[i]) if cn[i] > 0 else 0 for i in range(n)])

    # Normalize: relative to best σ_eff case (show what limits performance)
    sigma_ms = []
    for i in range(n):
        if g_path[i] > 0 and cn[i] > 0 and gb_dens[i] > 0:
            sigma_ms.append(sigma_brug[i] * C_ms * (g_path[i] * gb_dens[i]**2)**0.25 * cn[i]**2 * SIGMA_BULK)
        else:
            sigma_ms.append(0)
    ref = int(np.argmax(sigma_ms))  # best σ_eff case
    d_phi = log_phi - log_phi[ref]
    d_tau = log_tau2 - log_tau2[ref]
    d_fperc = log_fperc - log_fperc[ref]
    d_gpath_gbd = log_gpath_gbd - log_gpath_gbd[ref]
    d_cn = log_cn2 - log_cn2[ref]

    fig, axes = plt.subplots(2, 1, figsize=(max(8, len(names)*0.7), 10), gridspec_kw={'height_ratios': [2, 1]})

    # Top: σ_eff with each factor's contribution as stacked
    ax = axes[0]
    x = np.arange(n)
    w = 0.6

    # Stacked bar: each factor's log contribution (relative to reference)
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    labels = ['φ_SE', 'τ²', 'f_perc', '(G_path×GB_d²)^¼', 'CN²']
    contributions = [d_phi, d_tau, d_fperc, d_gpath_gbd, d_cn]

    # Positive and negative stacking
    pos_bottom = np.zeros(n)
    neg_bottom = np.zeros(n)
    for j, (contrib, color, label) in enumerate(zip(contributions, colors, labels)):
        pos = np.maximum(contrib, 0)
        neg = np.minimum(contrib, 0)
        ax.bar(x, pos, w, bottom=pos_bottom, color=color, label=label, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax.bar(x, neg, w, bottom=neg_bottom, color=color, alpha=0.4, edgecolor='white', linewidth=0.5)
        pos_bottom += pos
        neg_bottom += neg

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('Δlog(σ_brug) from reference', fontsize=11)
    ax.set_title(f'[Legacy v3] σ_ionic Factor Decomposition (ref: {names[ref]})', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left', ncol=3)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Bottom: dominant factor for each case
    ax2 = axes[1]
    # Find which factor has largest |contribution| for each case
    all_contribs = np.array(contributions)  # (5, n)
    dominant_idx = np.argmax(np.abs(all_contribs), axis=0)

    for i in range(n):
        if i == ref:
            ax2.barh(i, 0, color='gray')
            continue
        vals = all_contribs[:, i]
        sorted_idx = np.argsort(np.abs(vals))[::-1]
        # Show top 3 contributors
        y_pos = i
        for rank, j in enumerate(sorted_idx[:3]):
            ax2.barh(y_pos, vals[j], height=0.25, left=0,
                    color=colors[j], alpha=0.9 - rank*0.25,
                    edgecolor='white', linewidth=0.5)

    ax2.set_yticks(range(n))
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlabel('Factor contribution (Δlog)', fontsize=10)
    ax2.set_title('Dominant factors per case', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l) for c, l in zip(colors, labels)]
    ax2.legend(handles=legend_elements, fontsize=7, loc='lower right', ncol=3)

    plt.tight_layout()
    _write_csv(outdir, 'sigma_decomposition.csv',
               ['φ_SE(Δlog)', 'τ²(Δlog)', 'f_perc(Δlog)', '(G_path×GB_d²)^¼(Δlog)', 'CN²(Δlog)'],
               names, list(d_phi), list(d_tau), list(d_fperc), list(d_gpath_gbd), list(d_cn))
    return _save(fig, outdir, "sigma_decomposition.png")


PLOT_REGISTRY["v3_fitting"] = {
    "func": plot_v3_fitting,
    "file": "v3_fitting.png",
    "title": "[Legacy] v3 Fitting (thick only)",
    "description": "⚠ Legacy: FORM X로 대체됨\nv3: σ_brug × C × (G_path × GB_d²)^(1/4) × CN²\nthick R²=0.96, thin R²=-1.0",
    "origin_tip": "Red: v3 prediction. Green dashed: Network solver.",
    "hidden": True,
}

PLOT_REGISTRY["sigma_decomposition"] = {
    "func": plot_sigma_decomposition,
    "file": "sigma_decomposition.png",
    "title": "[Legacy] v3 Factor Decomposition",
    "description": "⚠ Legacy (v3): FORM X로 대체됨\nσ_ion = σ_brug × C × (G_path × GB_d²)^(1/4) × CN²\nthick only (thin에서 실패)",
    "origin_tip": "Stacked bar (top) + Horizontal bar (bottom).",
    "hidden": True,
}


def plot_electronic_decomposition(data_list, names, outdir):
    """Decompose σ_el: Thick(CN^(2-0.3M) × (φ-φc)² / por^(0.4-0.15M)), Thin(CN × √δ / √(T/d))."""
    SIGMA_AM = 50.0

    phi_am = [_get(d, "phi_am") for d in data_list]
    cn_am = [max(_get(d, "am_am_cn"), 0.01) for d in data_list]
    thickness = [_get(d, "thickness_um") for d in data_list]
    d_am = [2.0 * max(_get(d, "r_AM_P", 0), _get(d, "r_AM_S", 0), _get(d, "r_AM", 0))
            for d in data_list]
    porosity = [max(_get(d, "porosity", 10), 0.1) for d in data_list]
    am_delta = [max(_get(d, "am_am_mean_delta", 0), 0.001) for d in data_list]

    n = len(data_list)
    ratios = [thickness[i] / d_am[i] if d_am[i] > 0 and thickness[i] > 0 else 0 for i in range(n)]

    # Thick factors: CN^(2-0.3M), (φ-φc)², por^-(0.4-0.15M)
    phi_ex = [max(phi_am[i] - 0.10, 0.001) for i in range(n)]
    # Use fP_vol for Ψ in decomposition
    case_psi = []
    for d in data_list:
        _nP2 = _get(d, "n_AM_P", 0) or 0; _nS2 = _get(d, "n_AM_S", 0) or 0
        _rP2 = max(_get(d, "r_AM_P", 0) or 0, 0.1); _rS2 = max(_get(d, "r_AM_S", 0) or 0, 0.1)
        _vP2 = _nP2 * _rP2**3; _vS2 = _nS2 * _rS2**3; _vT2 = max(_vP2 + _vS2, 0.001)
        case_psi.append(_vP2 / _vT2)
    log_phi = np.array([2.0 * np.log(phi_ex[i]) for i in range(n)])
    case_mix = [4*case_psi[i]*(1-case_psi[i]) for i in range(n)]
    log_cn2 = np.array([(2.0 - 0.3*case_mix[i]) * np.log(cn_am[i]) for i in range(n)])
    log_por = np.array([-(0.4 - 0.15*case_mix[i]) * np.log(porosity[i]) for i in range(n)])
    # Thin factors: CN, δ^0.5, (T/d)^-0.5
    log_cn1 = np.array([1.0 * np.log(cn_am[i]) for i in range(n)])
    log_delta = np.array([0.5 * np.log(am_delta[i]) for i in range(n)])
    log_ratio = np.array([-0.5 * np.log(max(ratios[i], 0.1)) for i in range(n)])

    # Determine thick/thin per case
    is_thick = [ratios[i] >= 8 for i in range(n)]

    # σ_el for reference selection (use max)
    sigma_el = []
    for i in range(n):
        if phi_am[i] > 0 and cn_am[i] > 0 and d_am[i] > 0 and thickness[i] > 0:
            if is_thick[i]:
                _psi_d = case_psi[i] if i < len(case_psi) else 0
                _mix_d = 4*_psi_d*(1-_psi_d) if i < len(case_psi) else 0
                sigma_el.append(max(phi_am[i]-0.10,0.001)**2 * cn_am[i]**(2-0.3*_mix_d) / porosity[i]**(0.4-0.15*_mix_d))
            else:
                sigma_el.append(cn_am[i] * am_delta[i]**0.5 / max(ratios[i], 0.1)**0.5)
        else:
            sigma_el.append(0)

    if not any(s > 0 for s in sigma_el):
        return None

    ref = int(np.argmax(sigma_el))

    # Build contributions based on regime
    colors_all = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6']
    labels_all = ['[Thick] (φ-φc)²', '[Thick] CN^(2-0.3M)', '[Thick] 1/por^(0.4-0.15M)', '[Thin] √δ', '[Thin] 1/√(T/d)']
    # Thin CN uses same slot [1] but different label
    label_cn_thin = '[Thin] CN'

    # Thick reference: highest σ among thick cases; Thin reference: highest σ among thin
    thick_idx = [i for i in range(n) if is_thick[i] and sigma_el[i] > 0]
    thin_idx = [i for i in range(n) if not is_thick[i] and sigma_el[i] > 0]
    ref_tk = thick_idx[np.argmax([sigma_el[i] for i in thick_idx])] if thick_idx else ref
    ref_tn = thin_idx[np.argmax([sigma_el[i] for i in thin_idx])] if thin_idx else ref

    contribs = np.zeros((5, n))
    for i in range(n):
        if is_thick[i]:
            contribs[0, i] = log_phi[i] - log_phi[ref_tk]
            contribs[1, i] = log_cn2[i] - log_cn2[ref_tk]
            contribs[2, i] = log_por[i] - log_por[ref_tk]
        else:
            contribs[1, i] = log_cn1[i] - log_cn1[ref_tn]
            contribs[3, i] = log_delta[i] - log_delta[ref_tn]
            contribs[4, i] = log_ratio[i] - log_ratio[ref_tn]

    fig, axes = plt.subplots(2, 1, figsize=(max(8, len(names)*0.7), 10), gridspec_kw={'height_ratios': [2, 1]})

    ax = axes[0]
    x = np.arange(n)
    w = 0.6

    has_thick = any(is_thick[i] for i in range(n))
    has_thin = any(not is_thick[i] for i in range(n))

    pos_bottom = np.zeros(n)
    neg_bottom = np.zeros(n)
    used_labels = set()
    for j in range(5):
        contrib = contribs[j]
        if np.all(np.abs(contrib) < 1e-6):
            continue
        pos = np.maximum(contrib, 0)
        neg = np.minimum(contrib, 0)
        lbl = labels_all[j]
        if j == 1 and has_thin and not has_thick:
            lbl = label_cn_thin
        ax.bar(x, pos, w, bottom=pos_bottom, color=colors_all[j], label=lbl, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax.bar(x, neg, w, bottom=neg_bottom, color=colors_all[j], alpha=0.4, edgecolor='white', linewidth=0.5)
        pos_bottom += pos
        neg_bottom += neg
        used_labels.add(j)

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('Δlog(σ_el) from reference', fontsize=11)
    regime_str = []
    if has_thick: regime_str.append(f"Thick ref: {names[ref_tk]}")
    if has_thin: regime_str.append(f"Thin ref: {names[ref_tn]}")
    ax.set_title(f'Electronic σ_el Factor Decomposition ({", ".join(regime_str)})', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left', ncol=3)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Bottom: dominant factor
    ax2 = axes[1]
    for i in range(n):
        if i == ref:
            ax2.barh(i, 0, color='gray')
            continue
        vals = contribs[:, i]
        sorted_idx = np.argsort(np.abs(vals))[::-1]
        for rank, j in enumerate(sorted_idx[:3]):
            if abs(vals[j]) < 0.01:
                continue
            ax2.barh(i, vals[j], height=0.25, left=0,
                    color=colors_all[j], alpha=0.9 - rank*0.25,
                    edgecolor='white', linewidth=0.5)

    ax2.set_yticks(range(n))
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlabel('Factor contribution (Δlog)', fontsize=10)
    ax2.set_title('Dominant factors per case', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors_all[j], label=labels_all[j] if not (j==1 and has_thin and not has_thick) else label_cn_thin) for j in sorted(used_labels)]
    ax2.legend(handles=legend_elements, fontsize=7, loc='lower right', ncol=min(len(legend_elements), 3))

    plt.tight_layout()
    _write_csv(outdir, 'electronic_decomposition.csv',
               ['φ^2.5(Δlog)', 'CN(Δlog)', '1/√por(Δlog)', '√δ(Δlog)', '1/√(T/d)(Δlog)'],
               names, *[list(contribs[j]) for j in range(5)])
    return _save(fig, outdir, "electronic_decomposition.png")


PLOT_REGISTRY["electronic_decomposition"] = {
    "func": plot_electronic_decomposition,
    "file": "electronic_decomposition.png",
    "title": "Electronic: Factor Decomposition",
    "description": "Thick: CN^(2-0.3M) × (φ-φc)² / por^(0.4-0.15M)\nΨ = V_large/(V_large+V_small), 0=mono\nThin: CN × √δ / √(T/d)\n\n(φ-φc)²: percolation (φc=0.10)\nΨ: bimodal large-AM fraction\n√δ: AM-AM penetration depth",
    "origin_tip": "Stacked bar (top) + Horizontal bar (bottom).",
}


def plot_thermal_decomposition(data_list, names, outdir):
    """Decompose σ_th into σ_ion^(3/4), φ_AM², CN_SE^(-1) factors."""
    C_th = 286.0

    sigma_ion = _load_network_sigma(data_list)
    phi_am = [_get(d, "phi_am") for d in data_list]
    cn_se = [_get(d, "se_se_cn") for d in data_list]

    n = len(data_list)

    # log contributions
    log_ion = np.array([0.75 * np.log(sigma_ion[i]) if sigma_ion[i] > 0 else 0 for i in range(n)])
    log_phi = np.array([2 * np.log(phi_am[i]) if phi_am[i] > 0 else 0 for i in range(n)])
    log_cn = np.array([-1 * np.log(cn_se[i]) if cn_se[i] > 0 else 0 for i in range(n)])

    # σ_th for reference selection
    sigma_th = []
    for i in range(n):
        if sigma_ion[i] > 0 and phi_am[i] > 0 and cn_se[i] > 0:
            sigma_th.append(C_th * sigma_ion[i]**(3/4) * phi_am[i]**2 / cn_se[i])
        else:
            sigma_th.append(0)

    if not any(s > 0 for s in sigma_th):
        return None

    ref = int(np.argmax(sigma_th))
    d_ion = log_ion - log_ion[ref]
    d_phi = log_phi - log_phi[ref]
    d_cn = log_cn - log_cn[ref]

    fig, axes = plt.subplots(2, 1, figsize=(max(8, len(names)*0.7), 10), gridspec_kw={'height_ratios': [2, 1]})

    ax = axes[0]
    x = np.arange(n)
    w = 0.6

    colors = ['#2ecc71', '#e74c3c', '#3498db']
    labels = ['σ_ion^(3/4)', 'φ_AM²', 'CN_SE⁻¹']
    contributions = [d_ion, d_phi, d_cn]

    pos_bottom = np.zeros(n)
    neg_bottom = np.zeros(n)
    for j, (contrib, color, label) in enumerate(zip(contributions, colors, labels)):
        pos = np.maximum(contrib, 0)
        neg = np.minimum(contrib, 0)
        ax.bar(x, pos, w, bottom=pos_bottom, color=color, label=label, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax.bar(x, neg, w, bottom=neg_bottom, color=color, alpha=0.4, edgecolor='white', linewidth=0.5)
        pos_bottom += pos
        neg_bottom += neg

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylabel('Δlog(σ_th) from reference', fontsize=11)
    ax.set_title(f'Thermal σ_th Factor Decomposition (ref: {names[ref]})', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=3)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Bottom: dominant factor
    ax2 = axes[1]
    all_contribs = np.array(contributions)
    for i in range(n):
        if i == ref:
            ax2.barh(i, 0, color='gray')
            continue
        vals = all_contribs[:, i]
        sorted_idx = np.argsort(np.abs(vals))[::-1]
        for rank, j in enumerate(sorted_idx[:3]):
            ax2.barh(i, vals[j], height=0.25, left=0,
                    color=colors[j], alpha=0.9 - rank*0.25,
                    edgecolor='white', linewidth=0.5)

    ax2.set_yticks(range(n))
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlabel('Factor contribution (Δlog)', fontsize=10)
    ax2.set_title('Dominant factors per case', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='gray', linewidth=0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l) for c, l in zip(colors, labels)]
    ax2.legend(handles=legend_elements, fontsize=8, loc='lower right', ncol=3)

    plt.tight_layout()
    _write_csv(outdir, 'thermal_decomposition.csv',
               ['σ_ion^3/4(Δlog)', 'φ_AM²(Δlog)', 'CN_SE⁻¹(Δlog)'],
               names, list(d_ion), list(d_phi), list(d_cn))
    return _save(fig, outdir, "thermal_decomposition.png")


PLOT_REGISTRY["thermal_decomposition"] = {
    "func": plot_thermal_decomposition,
    "file": "thermal_decomposition.png",
    "title": "Thermal: Factor Decomposition (R²=0.90)",
    "description": "σ_th = 286 × σ_ion^(3/4) × φ_AM² / CN_SE\nR²=0.90\n\nσ_ion^(3/4): SE backbone (ionic에서 계승)\nφ_AM²: AM thermal enhancement\nCN_SE⁻¹: SE 과밀집 페널티 (ionic과 부호 역전!)",
    "origin_tip": "Stacked bar (top) + Horizontal bar (bottom).",
}
def plot_electronic_active_am(data_list, names, outdir):
    """Electronic Active AM%: bottom-reachable AM fraction."""
    active = [_get(d, "electronic_active_fraction", 0) * 100 for d in data_list]
    perc = [_get(d, "electronic_percolating_fraction", 0) * 100 for d in data_list]
    phi_am = [_get(d, "phi_am", 0) for d in data_list]
    sigma_el = _load_electronic_sigma(data_list)

    has_data = any(a > 0 for a in active)
    if not has_data:
        # Fallback: estimate from phi_am (literature model)
        for i in range(len(data_list)):
            pa = phi_am[i]
            if pa >= 0.55:
                active[i] = 100.0
            elif pa >= 0.30:
                active[i] = 87 + (pa - 0.30) / 0.25 * 13
            elif pa > 0:
                active[i] = 50 + (pa - 0.18) / 0.12 * 37
        has_data = True

    fig, ax1 = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names))
    ms = _marker_size(len(names))
    lw = _line_width(len(names))

    # Bar: Electronic Active AM%
    colors = ['#2ecc71' if a >= 95 else '#f39c12' if a >= 80 else '#e74c3c' for a in active]
    ax1.bar(x, active, 0.6, color=colors, alpha=0.8, label='Electronic Active AM (%)')
    ax1.set_ylabel('Electronic Active AM (%)', fontsize=11)
    ax1.set_ylim(0, 105)
    ax1.axhline(95, color='#2ecc71', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.axhline(80, color='#f39c12', linestyle='--', linewidth=0.8, alpha=0.5)

    # Line: σ_electronic
    ax2 = ax1.twinx()
    y_el = np.array([s if s > 0 else np.nan for s in sigma_el])
    ax2.plot(x, y_el, 'D-', color='#9b59b6', markersize=ms, linewidth=lw, label='σ_electronic')
    ax2.set_ylabel('σ_electronic (mS/cm)', color='#9b59b6', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#9b59b6')

    _apply_style(ax1, '', names)
    ax1.set_title('Electronic Active AM & Dead AM Analysis\nGreen≥95%, Yellow≥80%, Red<80%',
                  fontsize=10, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, fontsize=8, loc='lower right')

    _write_csv(outdir, 'electronic_active_am.csv',
               ['Active_AM(%)', 'σ_electronic(mS/cm)', 'φ_AM'],
               names, active, sigma_el, phi_am)
    return _save(fig, outdir, 'electronic_active_am.png')


PLOT_REGISTRY["electronic_active_am"] = {
    "func": plot_electronic_active_am,
    "file": "electronic_active_am.png",
    "title": "Electronic Active AM (Dead AM Analysis)",
    "description": "Bottom(CC)-reachable AM = 전자가 도달하는 AM 비율.\n95%+: 녹색 (정상), 80~95%: 황색 (주의), <80%: 적색 (도전재 필요!)\nDead AM = CC에서 전자 경로 없는 AM → 비활성.\nφ_AM > 55%면 대부분 OK. φ_AM < 35%면 도전재 필수.",
    "origin_tip": "Bar (Active %, colored) + Line (σ_electronic, purple).",
}

PLOT_REGISTRY["ion_path_quality"] = {
        "func": plot_ion_path_quality,
        "file": "ion_path_quality.png",
        "title": "Ion Path Quality (G_path, GB_d)",

        "description": "이온 경로 품질 4종 (모두 percolating 경로들의 mean):\n\n• GB Density = mean(N_hops / L_z) (hops/μm)\n  → ↓ 좋음 (입계 적을수록 저항↓)\n• Path Hop Area = mean(각 hop의 접촉면적)\n  → ↑ 좋음\n• Bottleneck = mean(각 경로의 최소 접촉면적)\n  → ↑ 좋음\n• Path Conductance = mean(1/Σ(1/A_i)) (μm²)\n  → ↑ 좋음 (직렬 저항 모델의 유효 면적)\n\n왜 mean? 경로 안은 직렬, 경로끼리는 병렬.\nmean = 경로 품질, f_perc = 경로 수량 (역할 분리).\n30개 shortest path 샘플 (best/mean/worst 10개씩).\nConductance가 가장 종합적 지표.",
        "origin_tip": "2×2 Subplots → GB Density (Blue), Hop Area (Orange), Bottleneck (Red), Conductance (Green).",
}
PLOT_REGISTRY["electronic_sigma"] = {
    "func": plot_electronic_sigma,
    "file": "electronic_sigma.png",
    "title": "Electronic Conductivity",
    "description": "AM-AM 접촉 네트워크 기반 전자 전도도.\nσ_AM = 0.05 S/cm (NCM 활물질).\nAM percolation 없으면 σ=0 (도전재 필요).\n10:0(P only)에서 AM 부족 → percolation 실패 가능.",
    "origin_tip": "Line (Red) + X markers for no-percolation cases.",
}
PLOT_REGISTRY["thermal_sigma"] = {
    "func": plot_thermal_sigma,
    "file": "thermal_sigma.png",
    "title": "Thermal Conductivity",
    "description": "ALL 접촉 네트워크 기반 열전도도.\nk_AM=4.0e-2, k_SE=0.7e-2 W/(cm·K).\nAM-SE 접촉은 harmonic mean.\n양방향 전도 (source↔sink 모두).",
    "origin_tip": "Line (Orange).",
}
PLOT_REGISTRY["electronic_scaling"] = {
    "func": plot_electronic_scaling,
    "file": "electronic_scaling.png",
    "title": "Electronic: 2-Regime Scaling Law",
    "description": "Thick (T/d≥10): σ = C × σ_AM × φ² × CN² × √cov / √por\n  φ: AM vol fraction, CN: AM-AM coordination\n\nThin (T/d<10): σ = C × σ_AM × CN × √δ / √(T/d)\n  δ: AM-AM penetration depth, T/d: thickness ratio\n\nC: thick/thin 별도 global fit (parameter sweep 최적화)",
    "origin_tip": "Red: Scaling law, Green dashed: Network solver (ground truth).",
}
PLOT_REGISTRY["thermal_scaling"] = {
    "func": plot_thermal_scaling,
    "file": "thermal_scaling.png",
    "title": "Thermal Scaling Law",
    "description": "\u03c3_th = 286 \u00d7 \u03c3_ion^(3/4) \u00d7 \u03c6_AM\u00b2 / CN_SE\n\u03c3_ion: ionic network solver \uacb0\uacfc \uc0ac\uc6a9\nCN_SE\u207b\u00b9: SE clustering \u2192 AM \uace0\ub9bd penalty\nR\u00b2=0.90 (1 free param), LOOCV R\u00b2=0.86",
    "origin_tip": "Orange: Scaling law, Green dashed: Network solver.",
}
PLOT_REGISTRY["transport_tradeoff"] = {
    "func": plot_transport_tradeoff,
    "file": "transport_tradeoff.png",
    "title": "Ionic vs Electronic Trade-off",
    "description": "이온 전도(SE-SE)와 전자 전도(AM-AM)의 역관계.\nAM↑ → electronic↑, ionic↓.\n최적 조성 = 두 곡선의 교차점 근처.\n도전재(carbon) 추가 시 electronic 병목 완화 가능.",
    "origin_tip": "Dual Y-axis: Green (ionic, left), Red (electronic, right).",
}
PLOT_REGISTRY["transport_normalized"] = {
    "func": plot_transport_normalized,
    "file": "transport_normalized.png",
    "title": "3-Mode Transport (Normalized)",
    "description": "Ionic/Electronic/Thermal 정규화 비교.\n각 mode를 자체 최대값으로 나눔 (0~1).\n어떤 mode가 조성 변화에 가장 민감한지 비교.\nIonic이 보통 가장 민감 (AM 비율에 강하게 반응).",
    "origin_tip": "Grouped Bar: Green(ionic), Red(electronic), Orange(thermal).",
}
PLOT_REGISTRY["transport_absolute"] = {
    "func": plot_transport_absolute,
    "file": "transport_absolute.png",
    "title": "3-Mode Transport (Absolute, Log)",
    "description": "Ionic/Electronic/Thermal 절대값 비교 (log scale).\nIonic ≪ Thermal < Electronic (typical).\nMinnmann(2021) 0.17 mS/cm 참고선 포함.\n이온 전도가 항상 rate-limiting → ionic 최적화 우선.",
    "origin_tip": "Multi-line (log Y): Green(ionic), Red(electronic), Orange(thermal).",
}
PLOT_REGISTRY["r_brug_comparison"] = {
    "func": plot_r_brug_comparison,
    "file": "r_brug_comparison.png",
    "title": "R_brug by Transport Mode",
    "description": "각 transport mode별 Bruggeman 과대추정 배수.\nR_brug = σ_brug / σ_network.\nIonic R_brug=3~10× (constriction 지배).\nElectronic/Thermal은 R_brug 다를 수 있음.\nR_brug가 클수록 접촉 저항 기여가 큼.",
    "origin_tip": "Grouped Bar: Green(ionic), Red(electronic), Orange(thermal).",
}
PLOT_REGISTRY["stress_z_layer"] = {
    "func": plot_stress_z_layer,
    "file": "stress_z_layer.png",
    "title": "Stress Z-layer CV",
    "description": "전극 높이별 Von Mises CV 프로파일.",
    "origin_tip": "Multi-line → X: Z Position (μm), Y: VM CV (%).",
}


# ─── Generic parameter comparison (X-Y scatter / multi-bar / correlation) ─────

def _merged_params(d):
    """Flatten one case's comparable numeric params: every scalar in
    full_metrics.json plus derived SE-diagnostics from the sibling
    viewer_aux.json (3D-viewer values).  Returns {key: float}."""
    out = {}
    for k, v in d.items():
        if k.startswith('_'):
            continue
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            out[k] = float(v)
    src = d.get('_source_path')
    if src:
        aux_path = os.path.join(os.path.dirname(src), 'viewer_aux.json')
        if os.path.exists(aux_path):
            try:
                with open(aux_path) as f:
                    aux = json.load(f)
            except (OSError, ValueError):
                aux = {}
            for k, v in aux.items():
                if isinstance(v, bool):
                    continue
                if isinstance(v, (int, float)):
                    out[f'aux:{k}'] = float(v)
            # Derived SE-network diagnostics (same formulas grade_engine uses)
            np_ = aux.get('se_n_percolating')
            apts = aux.get('se_articulation_points')
            ncut = aux.get('se_n_articulation_points')
            if ncut is None and isinstance(apts, list):
                ncut = len(apts)
            nb = aux.get('se_n_bn_below_threshold')
            ne = aux.get('se_n_perc_edges')
            if np_ and ncut is not None:
                out['cut_fraction'] = ncut / np_
            if nb is not None and ne:
                out['bn_below_frac'] = nb / ne
            if aux.get('se_bn_median_norm') is not None:
                out['bn_median_norm'] = float(aux['se_bn_median_norm'])
    # Grade-engine derived metrics (Q, ASR, τ_Laplace, cycle-stable …) exposed
    # as 'grade:<label>' params — values the raw metrics don't carry directly.
    if src and _grade_engine is not None:
        cdir = os.path.dirname(src)
        ip = _load_json(os.path.join(cdir, 'input_params.json'))
        meta = _load_json(os.path.join(cdir, 'meta.json'))
        se_aux = None
        ax = _load_json(os.path.join(cdir, 'viewer_aux.json'))
        if ax:
            apts = ax.get('se_articulation_points')
            se_aux = {
                'n_percolating':        ax.get('se_n_percolating'),
                'n_articulation_points': (ax.get('se_n_articulation_points')
                                          if ax.get('se_n_articulation_points') is not None
                                          else (len(apts) if isinstance(apts, list) else None)),
                'n_bn_below_threshold': ax.get('se_n_bn_below_threshold'),
                'n_perc_edges':         ax.get('se_n_perc_edges'),
                'bn_median_norm':       ax.get('se_bn_median_norm'),
            }
        try:
            prepared = {**d, **_grade_engine.map_input_params(ip, meta)}
            for label, val in _grade_engine.axis_values(prepared, se_aux).items():
                out[f'grade:{label}'] = float(val)
        except Exception:
            pass
    return out


def _load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _param_label(key):
    """Display label for a metric key (strip aux: prefix, decorative stars)."""
    lbl = key[4:] + ' (3D)' if key.startswith('aux:') else key
    return lbl.replace('⭐', '').replace('★', '').replace('  ', ' ').strip()


def _case_colors(n):
    return [GROUP_COLORS[i % len(GROUP_COLORS)] for i in range(n)]


_STAGE_E_SIGMA_KEYS = ('sigma_full_mScm_stage_e_physics', 'sigma_full_mScm_physics',
                       'sigma_full_mScm_stage_e', 'sigma_full_mScm')


def _stage_e_sigma(d):
    """Best available Stage-E (or physics) σ_ionic for a case."""
    for k in _STAGE_E_SIGMA_KEYS:
        v = d.get(k)
        if v is not None and v > 0:
            return float(v)
    return None


def _cov_frac(d, physics=True):
    """Mean AM coverage as a fraction (mode-matched)."""
    keys = (['coverage_AM_mean_physics', 'coverage_AM_P_mean_physics',
             'coverage_AM_S_mean_physics'] if physics else
            ['coverage_AM_mean', 'coverage_AM_P_mean', 'coverage_AM_S_mean'])
    vs = [d.get(k) for k in keys]
    vs = [v for v in vs if v and v > 0]
    return (sum(vs) / len(vs) / 100.0) if vs else None


def plot_ionic_solver_vs_stage_e(data_list, names, outdir):
    """Per-case σ_ionic from the raw Hertzian network solver vs the Physics
    solver vs the Stage-E final value — shows how much the Tabor+volume
    contact model and the literature grain corrections shift σ_ionic away
    from the DEM-native Hertzian solve."""
    H, P, E, labs = [], [], [], []
    for d, nm in zip(data_list, names):
        h = d.get('sigma_full_mScm')
        p = d.get('sigma_full_mScm_physics')
        e = _stage_e_sigma(d)
        if not (h or p or e):
            continue
        H.append(h if h else np.nan)
        P.append(p if p else np.nan)
        E.append(e if e else np.nan)
        labs.append(nm)
    if not labs:
        print("  [SKIP] ionic_solver_vs_stage_e: no σ data")
        return None
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(labs)); w = 0.27
    ax.bar(x - w, H, w, label='Network solver (Hertzian)', color=BLUE)
    ax.bar(x,     P, w, label='Network solver (Physics)', color=GREEN)
    ax.bar(x + w, E, w, label='Stage E final', color=RED)
    # Δ% Physics vs Hertzian annotation
    for i in range(len(labs)):
        if H[i] and P[i] and not (np.isnan(H[i]) or np.isnan(P[i])) and H[i] > 0:
            d_pct = (P[i] - H[i]) / H[i] * 100
            ax.annotate(f'{d_pct:+.0f}%', (x[i], max(H[i], P[i])),
                        fontsize=6, ha='center', va='bottom', color=GRAY)
    ax.set_xticks(x); ax.set_xticklabels(labs, rotation=30, ha='right', fontsize=8)
    ax.set_ylabel('σ_ionic (mS/cm)')
    ax.set_title('σ_ionic: Network solver (Hertzian/Physics) vs Stage E', fontsize=10)
    # Honour the unified y-axis cap (y-max-sigma input) so panels share a scale
    if _Y_MAX_SIGMA and _Y_MAX_SIGMA > 0:
        ax.set_ylim(0, _Y_MAX_SIGMA)
    ax.legend(fontsize=8); ax.grid(True, axis='y', alpha=0.25)
    # Case-group separators + labels (same style as the per-config line plots)
    if _GROUP_INFO and len(_GROUP_INFO[0]) > 1:
        sizes, gnames = _GROUP_INFO
        pos = 0
        for gi, sz in enumerate(sizes):
            if gi > 0:
                ax.axvline(pos - 0.5, color='#888888', linestyle='--',
                           linewidth=1, alpha=0.6)
            mid = pos + sz / 2 - 0.5
            ax.text(mid, -0.30 if gi % 2 else -0.22, gnames[gi], ha='center',
                    va='top', transform=ax.get_xaxis_transform(), fontsize=7,
                    fontweight='bold', color=GROUP_COLORS[gi % len(GROUP_COLORS)],
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                              edgecolor=GROUP_COLORS[gi % len(GROUP_COLORS)], alpha=0.8))
            pos += sz
        fig.subplots_adjust(bottom=0.32)
    outpath = _save(fig, outdir, "ionic_solver_vs_stage_e.png")
    with open(os.path.join(outdir, "ionic_solver_vs_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['Case', 'Hertzian', 'Physics', 'Stage_E',
                     'Phys_vs_Hertz_%', 'StageE_vs_Phys_%'])
        for i, nm in enumerate(labs):
            dvh = ((P[i]-H[i])/H[i]*100) if (H[i] and not np.isnan(H[i])
                                             and not np.isnan(P[i]) and H[i] > 0) else ''
            dep = ((E[i]-P[i])/P[i]*100) if (P[i] and not np.isnan(P[i])
                                             and not np.isnan(E[i]) and P[i] > 0) else ''
            wr.writerow([nm,
                         '' if np.isnan(H[i]) else round(H[i], 4),
                         '' if np.isnan(P[i]) else round(P[i], 4),
                         '' if np.isnan(E[i]) else round(E[i], 4),
                         round(dvh, 1) if dvh != '' else '',
                         round(dep, 1) if dep != '' else ''])
    return outpath


def _cblend_fit_score(base_log, logsf, taus):
    """Fit C_blend(τ) (v5 asymptote ⊕ poly3-in-lnτ, fixed w_bl/w_v5) on the
    log-residual; return (r2, loocv, Ct, Cn, pred_log).  Shared by the
    Stage-E σ fit experiments."""
    KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    n = len(taus)
    resid = logsf - base_log
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    w_bl = 1.0/(1.0+np.exp(-KBL*(taus-CBL)))
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])
    bv5, *_ = np.linalg.lstsq(Xv5, resid, rcond=None)
    bp3, *_ = np.linalg.lstsq(Xp3, resid, rcond=None)
    pred = base_log + (1-w_bl)*(Xv5@bv5) + w_bl*(Xp3@bp3)
    ss = np.sum((logsf-logsf.mean())**2)
    r2 = 1 - np.sum((logsf-pred)**2)/ss if ss > 0 else 0.0
    sse = 0.0
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        b5, *_ = np.linalg.lstsq(Xv5[mk], resid[mk], rcond=None)
        b3, *_ = np.linalg.lstsq(Xp3[mk], resid[mk], rcond=None)
        cb = (1-w_bl[i])*(Xv5[i]@b5) + w_bl[i]*(Xp3[i]@b3)
        sse += (logsf[i]-(base_log[i]+cb))**2
    loocv = 1 - sse/ss if ss > 0 else 0.0
    return (r2, loocv, float(np.exp(bv5[0])), float(np.exp(bv5[0]+bv5[1])),
            pred, bv5, bp3)


def _se_size_proxy(d):
    """SE grain-size proxy in µm (larger ⇒ fewer grain boundaries in series
    ⇒ higher σ).  Prefer the direct SE radius (design input); fall back to
    the inverse GB density (more GB ⇒ smaller effective grains)."""
    for k in ('_input_r_SE_um', '_input_r_SE', 'r_SE_um', 'r_SE'):
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
            # sim units (<0.01) → µm via ×1000 (matches grade_engine).
            return v * 1000.0 if v < 0.01 else float(v)
    gb = d.get('gb_density_mean')
    if isinstance(gb, (int, float)) and not isinstance(gb, bool) and gb > 0:
        return 1.0 / gb
    return None


def _am_asym_proxy(d):
    """AM_P/AM_S asymmetry for mixed-AM cases.  Physics coverage asymmetry
    (cov_AM_P − cov_AM_S, fraction) is the #1 residual correlate; fall back
    to ln(r_AM_P/r_AM_S) when coverage is unavailable."""
    cp = d.get('coverage_AM_P_mean_physics'); cs = d.get('coverage_AM_S_mean_physics')
    if (isinstance(cp, (int, float)) and not isinstance(cp, bool) and
            isinstance(cs, (int, float)) and not isinstance(cs, bool)):
        return (cp - cs) / 100.0
    rp = d.get('_input_r_AM_P_um') or d.get('r_AM_P')
    rs = d.get('_input_r_AM_S_um') or d.get('r_AM_S')
    if (isinstance(rp, (int, float)) and isinstance(rs, (int, float))
            and rp > 0 and rs > 0):
        return float(np.log(rp / rs))
    return None


def _cblend_extra_score(base_log, logsf, taus, extra):
    """C_blend(τ) fit + extra multiplicative corrections exp(Σ β_j·extra_j)
    (β fit jointly on the post-C_blend residual via lstsq; each extra column
    centered per training set).  `extra` is an (n,k) array or None.  LOOCV
    refits C_blend AND β every fold so the extra DoF is honestly penalised.
    Returns (r2, loocv, betas:list, pred_log)."""
    KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    n = len(taus)
    extra = None if extra is None else np.asarray(extra, float).reshape(n, -1)
    k = 0 if extra is None else extra.shape[1]
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    w_bl = 1.0/(1.0+np.exp(-KBL*(taus-CBL)))
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])

    def _fit(mask):
        resid = logsf[mask] - base_log[mask]
        b5, *_ = np.linalg.lstsq(Xv5[mask], resid, rcond=None)
        b3, *_ = np.linalg.lstsq(Xp3[mask], resid, rcond=None)
        cb = (1-w_bl[mask])*(Xv5[mask]@b5) + w_bl[mask]*(Xp3[mask]@b3)
        if k == 0:
            return b5, b3, np.zeros(0), np.zeros(0)
        means = extra[mask].mean(axis=0)
        Ec = extra[mask] - means
        betas, *_ = np.linalg.lstsq(Ec, resid - cb, rcond=None)
        return b5, b3, betas, means

    b5, b3, betas, means = _fit(np.ones(n, bool))
    cb = (1-w_bl)*(Xv5@b5) + w_bl*(Xp3@b3)
    pred = base_log + cb + ((extra - means) @ betas if k else 0.0)
    ss = np.sum((logsf - logsf.mean())**2)
    r2 = 1 - np.sum((logsf - pred)**2)/ss if ss > 0 else 0.0
    sse = 0.0
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        b5i, b3i, bi, mi = _fit(mk)
        cbi = (1-w_bl[i])*(Xv5[i]@b5i) + w_bl[i]*(Xp3[i]@b3i)
        pi = base_log[i] + cbi + ((extra[i]-mi) @ bi if k else 0.0)
        sse += (logsf[i] - pi)**2
    loocv = 1 - sse/ss if ss > 0 else 0.0
    return r2, loocv, [float(b) for b in betas], pred


def plot_ionic_phic_scan_stage_e(data_list, names, outdir):
    """Fix CN² · (φ−φc)^0.5 · cov^0.5 · f_p³ (clean integer/half powers) +
    C_blend(τ), and scan the percolation threshold φc for the LOOCV-optimal
    value.  C_blend re-fits at EVERY φc so the τ prefactor tracks the new
    base form.  → 'CN² with a slightly tuned φc' best value + fit quality."""
    SG = 3.0; CN_EXP = 2.0; PHI_EXP = 0.5; COV_EXP = 0.5; FP_EXP = 3.0
    recs = []
    for d in data_list:
        sig = _stage_e_sigma(d); phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct')/100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if sig and sig > 0 and phi > 0 and cn > 0 and cov and cov > 0 and fp > 0 and tau > 0:
            recs.append((phi, cn, cov, fp, tau, sig))
    if len(recs) < 15:
        print(f"  [SKIP] ionic_phic_scan_stage_e: only {len(recs)} cases (<15)")
        return None

    def _fit_at(phic):
        rows = [r for r in recs if r[0] > phic + 1e-3]
        if len(rows) < 15:
            return None
        a = np.array(rows)
        base_log = (np.log(SG) + PHI_EXP*np.log(a[:, 0]-phic) + CN_EXP*np.log(a[:, 1])
                    + COV_EXP*np.log(a[:, 2]) + FP_EXP*np.log(a[:, 3]))
        r2, loo, Ct, Cn, _, bv5, bp3 = _cblend_fit_score(base_log, np.log(a[:, 5]), a[:, 4])
        return phic, r2, loo, len(rows), Ct, Cn, bv5, bp3

    grid = np.round(np.arange(0.10, 0.225, 0.005), 3)
    res = [r for r in (_fit_at(p) for p in grid) if r]
    if not res:
        print("  [SKIP] ionic_phic_scan_stage_e: no φc fit")
        return None
    M = np.array([(p, r2, lo, n) for (p, r2, lo, n, _, _, _, _) in res])
    best = max(res, key=lambda t: t[2])
    bphic, br2, bloo, bn, bCt, bCn, bbv5, bbp3 = best
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.plot(M[:, 0], M[:, 1], 's-', color=GRAY, ms=4, label='R² (train)')
    ax.plot(M[:, 0], M[:, 2], 'o-', color=BLUE, ms=5, label='LOOCV')
    ax.axvline(bphic, color=RED, ls='--', label=f'best φc={bphic:.3f}')
    ax.axvline(0.20, color='#aaaaaa', ls=':', label='v12 φc=0.20')
    ax.set_xlabel('φc (percolation threshold in φ−φc)'); ax.set_ylabel('R²')
    ax.set_title("CN²·(φ−φc)^0.5·cov^0.5·f_p³·C_blend(τ) — φc scan (Stage-E)\n"
                 "best φc=%.3f → R²=%.3f, LOOCV=%.3f  [Ct=%.4f, Cn=%.4f, n=%d]"
                 % (bphic, br2, bloo, bCt, bCn, bn), fontsize=8)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.25)
    outpath = _save(fig, outdir, "ionic_phic_scan_stage_e.png")
    with open(os.path.join(outdir, "ionic_phic_scan_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['phi_c', 'R2', 'LOOCV', 'n_used', 'Ct', 'Cn'])
        for (p, r2, lo, n, Ct, Cn, _v5, _p3) in res:
            wr.writerow([p, round(r2, 4), round(lo, 4), n, round(Ct, 5), round(Cn, 5)])
        wr.writerow([])
        wr.writerow(['# best (max LOOCV)', bphic, round(br2, 4), round(bloo, 4), bn,
                     round(bCt, 5), round(bCn, 5)])
        # FULL frozen C_blend spec at best φc — everything needed to hardcode
        wr.writerow([])
        wr.writerow(['# === FROZEN FORMULA (hardcode these) ==='])
        wr.writerow(['# σ = C_blend(τ)·σ_grain·(φ−%.3f)^0.5·CN^2·cov^0.5·f_p^3'
                     % bphic, 'σ_grain=3.0'])
        wr.writerow(['# C_blend(τ) = (1−w_bl)·exp(C_v5) + w_bl·exp(C_p3)'])
        wr.writerow(['C_v5 b0 (=lnCt)', round(float(bbv5[0]), 5),
                     'b1', round(float(bbv5[1]), 5)])
        wr.writerow(['C_p3 a0', round(float(bbp3[0]), 5), 'a1', round(float(bbp3[1]), 5),
                     'a2', round(float(bbp3[2]), 5), 'a3', round(float(bbp3[3]), 5)])
        wr.writerow(['w_v5 = σ(5·(τ−2.1))', 'w_bl = σ(20·(τ−1.92))', 'fixed'])
    return outpath


def plot_ionic_fit_stage_e(data_list, names, outdir):
    """FINAL fixed physics form for the Stage-E/Physics σ target:
    σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^(1/2)·f_p³.

    Exponents + φc are FIXED single values (chosen from the n=91 φc scan:
    CN² clean integer, φc=0.19 = robust n=91 peak that avoids the φc=0.20
    singularity).  Only the τ prefactor C_blend(τ) re-fits to the corpus.
    A free data-native exponent fit is kept in the CSV as a diagnostic."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    real_all = (_REAL_NAMES if (_REAL_NAMES and len(_REAL_NAMES) == len(data_list))
                else list(names))
    base_log, logsf, taus, free_rows, kept_names = [], [], [], [], []
    for idx, d in enumerate(data_list):
        sig = _stage_e_sigma(d)
        phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct') / 100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if not (sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0
                and fp > 0 and tau > 0):
            continue
        base_log.append(np.log(SG) + 0.5*np.log(phi-PHI_C) + CN_EXP*np.log(cn)
                        + COV_EXP*np.log(cov) + 3.0*np.log(fp))
        logsf.append(np.log(sig)); taus.append(tau)
        free_rows.append((np.log(phi-PHI_C), np.log(cn), np.log(cov),
                          np.log(fp), np.log(tau), np.log(sig/SG)))
        kept_names.append(real_all[idx])
    n = len(taus)
    if n < 8:
        print(f"  [SKIP] ionic_fit_stage_e: only {n} usable cases (<8)")
        return None
    base_log = np.array(base_log); logsf = np.array(logsf); taus = np.array(taus)
    resid = logsf - base_log
    w_v5 = 1.0 / (1.0 + np.exp(-KV5 * (taus - CV5)))
    lt = np.log(taus)
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])
    w_bl = 1.0 / (1.0 + np.exp(-KBL * (taus - CBL)))

    def _cblend_log(bv5, bp3, idx=slice(None)):
        return (1 - w_bl[idx]) * (Xv5[idx] @ bv5) + w_bl[idx] * (Xp3[idx] @ bp3)

    bv5, *_ = np.linalg.lstsq(Xv5, resid, rcond=None)
    bp3, *_ = np.linalg.lstsq(Xp3, resid, rcond=None)
    pred_log = base_log + _cblend_log(bv5, bp3)
    ss_tot = np.sum((logsf - logsf.mean())**2)
    r2 = 1 - np.sum((logsf - pred_log)**2) / ss_tot if ss_tot > 0 else 0.0
    sse = 0.0
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        bv5_i, *_ = np.linalg.lstsq(Xv5[mk], resid[mk], rcond=None)
        bp3_i, *_ = np.linalg.lstsq(Xp3[mk], resid[mk], rcond=None)
        cb_i = (1 - w_bl[i]) * (Xv5[i] @ bv5_i) + w_bl[i] * (Xp3[i] @ bp3_i)
        sse += (logsf[i] - (base_log[i] + cb_i))**2
    loocv = 1 - sse / ss_tot if ss_tot > 0 else 0.0
    Ct = float(np.exp(bv5[0])); Cn = float(np.exp(bv5[0] + bv5[1]))

    # Free data-native fit (diagnostic only — written to CSV)
    fa = np.array(free_rows)
    Xf = np.column_stack([fa[:, :5], np.ones(n)])
    fcoef, *_ = np.linalg.lstsq(Xf, fa[:, 5], rcond=None)

    sig_pred = np.exp(pred_log); sig_act = np.exp(logsf)
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.scatter(sig_act, sig_pred, s=55, c=BLUE, edgecolors='white', zorder=3)
    lim = [min(sig_act.min(), sig_pred.min()) * 0.8,
           max(sig_act.max(), sig_pred.max()) * 1.2]
    ax.plot(lim, lim, '--', color=GRAY, label='1:1')
    ax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                    color=GREEN, alpha=0.12, label='±20%')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('σ_actual (Stage E / Physics, mS/cm)')
    ax.set_ylabel('σ_predicted (fixed form, mS/cm)')
    ax.set_title("Stage-E σ_ionic — fixed physics form  (n=%d)\n"
                 "σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³"
                 "   [Ct=%.4f, Cn=%.4f]\nR²=%.3f, LOOCV=%.3f"
                 % (n, Ct, Cn, r2, loocv), fontsize=8)
    ax.legend(fontsize=8, loc='upper left'); ax.grid(True, alpha=0.25, which='both')
    outpath = _save(fig, outdir, "ionic_fit_stage_e.png")
    _focus_parity(outdir, "ionic_fit_stage_e", sig_act, sig_pred, kept_names,
                  'σ_actual (Stage E / Physics, mS/cm)',
                  'σ_predicted (fixed form, mS/cm)',
                  "선택 샘플만 — 식·계수는 전체 fit 그대로\n"
                  "σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³  "
                  "(fit: 전체 n=%d, R²=%.3f LOOCV=%.3f)" % (n, r2, loocv))
    with open(os.path.join(outdir, "ionic_fit_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['# physical v12 form refit to Stage-E target'])
        wr.writerow(['param', 'value'])
        wr.writerow(['C_thick (Ct)', round(Ct, 5)]); wr.writerow(['C_thin (Cn)', round(Cn, 5)])
        wr.writerow(['R2', round(r2, 4)]); wr.writerow(['LOOCV', round(loocv, 4)])
        wr.writerow([])
        wr.writerow(['# free data-native exponents (diagnostic — physical=0.5/1.5/0.4/3)'])
        for nm_, val in zip(['phi-0.2', 'CN', 'cov', 'f_p', 'tau', 'ln_C0'], fcoef):
            wr.writerow([nm_, round(float(val), 4)])
    return outpath


def _stage_e_base_arrays(corpus):
    """Build (base_log, logsf, taus) for the fixed Stage-E physics form over a
    list of metrics dicts (cases failing the validity filter are dropped)."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    bl, ls, ts = [], [], []
    for d in corpus:
        sig = _stage_e_sigma(d); phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct')/100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0 and fp > 0 and tau > 0:
            bl.append(np.log(SG) + 0.5*np.log(phi-PHI_C) + CN_EXP*np.log(cn)
                      + COV_EXP*np.log(cov) + 3.0*np.log(fp))
            ls.append(np.log(sig)); ts.append(tau)
    return np.array(bl), np.array(ls), np.array(ts)


def _stage_e_global_fit():
    """Fit C_blend on the FULL corpus (_FIT_CORPUS) → (r2, loocv, bv5, bp3, n).
    Returns None if no/insufficient corpus was supplied."""
    if not _FIT_CORPUS:
        return None
    bl, ls, ts = _stage_e_base_arrays(_FIT_CORPUS)
    if len(ts) < 8:
        return None
    r2, loo, _Ct, _Cn, _pred, bv5, bp3 = _cblend_fit_score(bl, ls, ts)
    return r2, loo, bv5, bp3, len(ts)


def _cblend_predict_log(base_log, taus, bv5, bp3):
    """Apply fixed-shape C_blend(τ) with given coefficients to predict log σ."""
    KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    base_log = np.asarray(base_log); taus = np.asarray(taus)
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    w_bl = 1.0/(1.0+np.exp(-KBL*(taus-CBL)))
    Xv5 = np.column_stack([np.ones(len(taus)), w_v5])
    Xp3 = np.column_stack([np.ones(len(taus)), lt, lt**2, lt**3])
    return base_log + (1-w_bl)*(Xv5@bv5) + w_bl*(Xp3@bp3)


def plot_ionic_perconfig_physics(data_list, names, outdir):
    """PHYSICS-mode per-config (P:S) line plot: the fixed physics formula
    σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³ vs the PHYSICS network
    solver σ.  C_blend + R²/LOOCV are taken from the GLOBAL (full-corpus) fit
    when a fit corpus is supplied, so every per-group panel reports the same
    n=all fit; otherwise it refits on the cases shown."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    netP = [None]*len(data_list)
    idx, base_log, logsf, taus = [], [], [], []
    for i, d in enumerate(data_list):
        sig = _stage_e_sigma(d)        # physics / Stage-E target
        netP[i] = sig if (sig and sig > 0) else None
        phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct')/100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0 and fp > 0 and tau > 0:
            idx.append(i)
            base_log.append(np.log(SG) + 0.5*np.log(phi-PHI_C) + CN_EXP*np.log(cn)
                            + COV_EXP*np.log(cov) + 3.0*np.log(fp))
            logsf.append(np.log(sig)); taus.append(tau)
    if len(idx) < 8:
        print(f"  [SKIP] ionic_perconfig_physics: only {len(idx)} usable cases (<8)")
        return None
    gfit = _stage_e_global_fit()
    if gfit:
        # GLOBAL fit (full corpus): same coeffs + R²/LOOCV on every panel.
        r2, loo, bv5, bp3, n_fit = gfit
        pred_log = _cblend_predict_log(np.array(base_log), np.array(taus), bv5, bp3)
    else:
        r2, loo, Ct, Cn, pred_log, _, _ = _cblend_fit_score(
            np.array(base_log), np.array(logsf), np.array(taus))
        n_fit = len(idx)
    pred = np.full(len(data_list), np.nan)
    for j, i in enumerate(idx):
        pred[i] = float(np.exp(pred_log[j]))
    net = np.array([n if (n and n > 0) else np.nan for n in netP])

    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names)); ms = _marker_size(len(names)); lw = _line_width(len(names))
    ax.plot(x, pred, 's-', color=RED, markersize=ms, linewidth=lw,
            label='fixed physics form (mS/cm)')
    ax.fill_between(x, pred*0.78, pred*1.22, color=RED, alpha=0.10, label='±22% band')
    ax.plot(x, net, 'D--', color='#2ecc71', markersize=max(ms-2, 3), linewidth=lw-0.5,
            alpha=0.75, label='Physics network solver (mS/cm)')
    _apply_style(ax, "σ_ionic (mS/cm)", names)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("σ_ionic PHYSICS per-config — fixed form vs Physics solver\n"
                 "σ = C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³   "
                 "전체 fit n=%d  R²=%.3f LOOCV=%.3f" % (n_fit, r2, loo),
                 fontsize=8.5, fontweight='bold')
    if _Y_MAX_SIGMA is not None and _Y_MAX_SIGMA > 0:
        ax.set_ylim(0, _Y_MAX_SIGMA)
    outpath = _save(fig, outdir, "ionic_perconfig_physics.png")
    _write_csv(outdir, "ionic_perconfig_physics.csv",
               ['sigma_pred(phys form)', 'sigma_physics_solver'],
               names,
               [None if np.isnan(pred[i]) else round(float(pred[i]), 4) for i in range(len(names))],
               [None if np.isnan(net[i]) else round(float(net[i]), 4) for i in range(len(names))])
    return outpath


def plot_ionic_formtest_stage_e(data_list, names, outdir):
    """Is a COMPLETELY DIFFERENT functional form worth it? Compare, on the
    SAME features {ln(φ−0.2), lnCN, lncov, lnf_p, lnτ}, the power-law
    (log-linear) vs a flexible degree-2 polynomial (squares + all pairwise
    interactions) — a sklearn-free stand-in for GPR/RF.  Judged by LOOCV:
      flexible ≫ power-law  → a better form exists (nonlinearity/interaction);
      flexible ≈ power-law  → noise/ data ceiling, NO new formula will help."""
    SG = 3.0; PHI_C = 0.20
    rows = []
    for d in data_list:
        sig = _stage_e_sigma(d)
        phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct') / 100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if not (sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0
                and fp > 0 and tau > 0):
            continue
        rows.append((np.log(phi-PHI_C), np.log(cn), np.log(cov),
                     np.log(fp), np.log(tau), np.log(sig)))
    n = len(rows)
    if n < 15:
        print(f"  [SKIP] ionic_formtest_stage_e: only {n} usable cases (<15)")
        return None
    A = np.array(rows); F = A[:, :5]; y = A[:, 5]
    ss_tot = np.sum((y - y.mean())**2)

    def _loocv_r2(X):
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        r2 = 1 - np.sum((y - X @ coef)**2) / ss_tot
        sse = 0.0
        for i in range(n):
            mk = np.ones(n, bool); mk[i] = False
            ci, *_ = np.linalg.lstsq(X[mk], y[mk], rcond=None)
            sse += (y[i] - X[i] @ ci)**2
        return r2, 1 - sse / ss_tot

    # A: power-law (log-linear)
    XA = np.column_stack([np.ones(n), F])
    r2A, looA = _loocv_r2(XA)
    # B: flexible degree-2 poly (linear + squares + pairwise interactions)
    cols = [np.ones(n)] + [F[:, j] for j in range(5)] \
        + [F[:, j]**2 for j in range(5)] \
        + [F[:, i]*F[:, j] for i, j in itertools.combinations(range(5), 2)]
    XB = np.column_stack(cols)
    r2B, looB = _loocv_r2(XB)

    gain = looB - looA
    verdict = ('새 형태 효과 有 (비선형/교호 신호)' if gain > 0.01
               else '노이즈 천장 — 새 식 효과 거의 없음')
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    labels = ['Power-law\n(log-linear, %d p)' % XA.shape[1],
              'Flexible poly-2\n(+sq +교호, %d p)' % XB.shape[1]]
    xpos = [0, 1]
    ax.bar([p-0.18 for p in xpos], [r2A, r2B], 0.36, label='R² (train)', color=GRAY)
    ax.bar([p+0.18 for p in xpos], [looA, looB], 0.36, label='LOOCV', color=BLUE)
    for p, (tr, lo) in zip(xpos, [(r2A, looA), (r2B, looB)]):
        ax.text(p-0.18, tr+0.005, f'{tr:.3f}', ha='center', fontsize=8)
        ax.text(p+0.18, lo+0.005, f'{lo:.3f}', ha='center', fontsize=8,
                color=BLUE, fontweight='bold')
    ax.set_xticks(xpos); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('R²'); ax.set_ylim(min(looA, looB)-0.05, 1.0)
    ax.set_title("새 함수형이 효과 있나? (Stage-E σ, n=%d)\n"
                 "ΔLOOCV(flex−power) = %+.3f → %s" % (n, gain, verdict),
                 fontsize=9)
    ax.legend(fontsize=8, loc='lower right'); ax.grid(True, axis='y', alpha=0.25)
    outpath = _save(fig, outdir, "ionic_formtest_stage_e.png")
    with open(os.path.join(outdir, "ionic_formtest_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['model', 'n_params', 'R2_train', 'LOOCV'])
        wr.writerow(['power-law (log-linear)', XA.shape[1], round(r2A, 4), round(looA, 4)])
        wr.writerow(['flexible poly-2', XB.shape[1], round(r2B, 4), round(looB, 4)])
        wr.writerow(['ΔLOOCV (flex - power)', '', '', round(gain, 4)])
        wr.writerow(['verdict', verdict])
    return outpath


def plot_ionic_refit_stage_e(data_list, names, outdir):
    """Test: refit ONLY the φ/CN/cov exponents (f_p=3 + C_blend(τ) kept) for
    the Stage-E/Physics target, LOOCV-validated, and compare to the fixed
    physical v12 exponents (0.5/1.5/0.4).  Since w_bl/w_v5 are fixed, C_blend
    is linear in its 6 basis terms → exponents + C_blend fit jointly by one
    least-squares.  Answers 'do the physics-target exponents differ, and does
    refitting them beat 0.939 under LOOCV (not just training R²)?'"""
    SG = 3.0; PHI_C = 0.20; KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    lp, lc, lcov, lfp, taus, logsf = [], [], [], [], [], []
    for d in data_list:
        sig = _stage_e_sigma(d)
        phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct') / 100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if not (sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0
                and fp > 0 and tau > 0):
            continue
        lp.append(np.log(phi-PHI_C)); lc.append(np.log(cn)); lcov.append(np.log(cov))
        lfp.append(np.log(fp)); taus.append(tau); logsf.append(np.log(sig))
    n = len(taus)
    if n < 10:
        print(f"  [SKIP] ionic_refit_stage_e: only {n} usable cases (<10)")
        return None
    lp = np.array(lp); lc = np.array(lc); lcov = np.array(lcov)
    lfp = np.array(lfp); taus = np.array(taus); logsf = np.array(logsf)
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    w_bl = 1.0/(1.0+np.exp(-KBL*(taus-CBL)))
    cblend = np.column_stack([(1-w_bl), (1-w_bl)*w_v5, w_bl,
                              w_bl*lt, w_bl*lt**2, w_bl*lt**3])
    ss_tot = np.sum((logsf - logsf.mean())**2)

    def _fit(X, offset):
        y = logsf - offset
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        pred = offset + X @ coef
        r2 = 1 - np.sum((logsf-pred)**2)/ss_tot
        sse = 0.0
        for i in range(n):
            mk = np.ones(n, bool); mk[i] = False
            ci, *_ = np.linalg.lstsq(X[mk], y[mk], rcond=None)
            sse += (logsf[i] - (offset[i] + X[i] @ ci))**2
        return coef, r2, 1 - sse/ss_tot, pred

    # Fixed physical v12 (exponents 0.5/1.5/0.4, f_p^3) — fit C_blend only
    off_fix = np.log(SG) + 0.5*lp + 1.5*lc + 0.4*lcov + 3.0*lfp
    _, r2_fix, loo_fix, _ = _fit(cblend, off_fix)
    # Free φ/CN/cov exponents (f_p^3 fixed) + C_blend
    Xfree = np.column_stack([lp, lc, lcov, cblend])
    off_free = np.log(SG) + 3.0*lfp
    cf, r2_free, loo_free, pred_free = _fit(Xfree, off_free)
    a, b, c = float(cf[0]), float(cf[1]), float(cf[2])
    # Standard errors of the exponents → only trust "확실하게 떨어지는" ones.
    # SE = sqrt(σ²·diag((XᵀX)⁻¹)); large SE/|coef| ⇒ poorly determined.
    yf = logsf - off_free
    resid_f = yf - Xfree @ cf
    dof = max(n - Xfree.shape[1], 1)
    sigma2 = float(resid_f @ resid_f) / dof
    try:
        cov = sigma2 * np.linalg.pinv(Xfree.T @ Xfree)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
        se_a, se_b, se_c = float(se[0]), float(se[1]), float(se[2])
    except Exception:
        se_a = se_b = se_c = float('nan')

    sig_act = np.exp(logsf); sig_pred = np.exp(pred_free)
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.scatter(sig_act, sig_pred, s=50, c=BLUE, edgecolors='white', zorder=3)
    lim = [min(sig_act.min(), sig_pred.min())*0.8, max(sig_act.max(), sig_pred.max())*1.2]
    ax.plot(lim, lim, '--', color=GRAY, label='1:1')
    ax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                    color=GREEN, alpha=0.12, label='±20%')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('σ_actual (Stage E / Physics, mS/cm)')
    ax.set_ylabel('σ_predicted (refit exponents)')
    gain = loo_free - loo_fix
    ax.set_title(
        "Stage-E σ — refit φ/CN/cov exponents  (n=%d)\n"
        "(φ−0.2)^(%.2f±%.2f) · CN^(%.2f±%.2f) · cov^(%.2f±%.2f) · f_p³ · C_blend(τ)   "
        "[v12: 0.50/1.50/0.40]\n"
        "refit: R²=%.3f LOOCV=%.3f   vs   fixed-v12: R²=%.3f LOOCV=%.3f   "
        "(ΔLOOCV=%+.3f %s)"
        % (n, a, se_a, b, se_b, c, se_c, r2_free, loo_free, r2_fix, loo_fix, gain,
           '개선' if gain > 0.002 else '미미/과적합'),
        fontsize=7.2)
    ax.legend(fontsize=8, loc='upper left'); ax.grid(True, alpha=0.25, which='both')
    outpath = _save(fig, outdir, "ionic_refit_stage_e.png")
    with open(os.path.join(outdir, "ionic_refit_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['model', 'phi_exp', 'CN_exp', 'cov_exp', 'fp_exp', 'R2', 'LOOCV'])
        wr.writerow(['fixed v12', 0.5, 1.5, 0.4, 3, round(r2_fix, 4), round(loo_fix, 4)])
        wr.writerow(['refit φ/CN/cov', round(a, 3), round(b, 3), round(c, 3), 3,
                     round(r2_free, 4), round(loo_free, 4)])
        wr.writerow(['  ± std error', round(se_a, 3), round(se_b, 3), round(se_c, 3),
                     '', '', ''])
        wr.writerow(['  well-determined?',
                     'Y' if se_a < abs(a)*0.5 else 'N',
                     'Y' if se_b < abs(b)*0.5 else 'N',
                     'Y' if se_c < abs(c)*0.5 else 'N', '(SE<50%·|exp|)', '', ''])
        wr.writerow(['ΔLOOCV', '', '', '', '', '', round(gain, 4)])
    return outpath


_OUTLIER_DIAG_FEATS = [
    ('phi_se', None), ('se_se_cn', None),
    ('tortuosity_recommended', 'tortuosity_mean'),
    ('gb_density_mean', None), ('path_hop_area_min_mean', None),
    ('se_se_cn_std', None), ('bulk_resistance_fraction', None),
    ('am_se_cn_mean', None), ('path_conductance_mean', None),
    ('path_hop_area_mean_physics', 'path_hop_area_mean'),
]


def plot_ionic_outliers_stage_e(data_list, names, outdir):
    """Outlier-focused diagnostic for the Stage-E σ fit: fits the FINAL fixed
    physics form (CN²·(φ−0.19)^0.5·cov^0.5·f_p³·C_blend(τ)), highlights the
    worst-fit cases, and reports which structural feature their log-residual
    correlates with most."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92
    # Saved case names (args.names) aligned with data_list; the `names` arg is
    # the P:S ratio used as a short label. Show the saved name + P:S in the table.
    real_all = (_REAL_NAMES if (_REAL_NAMES and len(_REAL_NAMES) == len(data_list))
                else list(names))
    base_log, logsf, taus, labs, real_labs, feat_rows = [], [], [], [], [], []
    for idx, (d, nm) in enumerate(zip(data_list, names)):
        sig = _stage_e_sigma(d)
        phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct') / 100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        if not (sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0
                and fp > 0 and tau > 0):
            continue
        base_log.append(np.log(SG) + 0.5*np.log(phi-PHI_C) + CN_EXP*np.log(cn)
                        + COV_EXP*np.log(cov) + 3.0*np.log(fp))
        logsf.append(np.log(sig)); taus.append(tau); labs.append(nm)
        real_labs.append(real_all[idx])
        fr = {}
        for key, fb in _OUTLIER_DIAG_FEATS:
            v = d.get(key)
            if v is None and fb:
                v = d.get(fb)
            fr[key] = float(v) if isinstance(v, (int, float)) else np.nan
        fr['cov_asym'] = ((d.get('coverage_AM_P_mean_physics') or 0)
                          - (d.get('coverage_AM_S_mean_physics') or 0))
        feat_rows.append(fr)
    n = len(taus)
    if n < 8:
        print(f"  [SKIP] ionic_outliers_stage_e: only {n} usable cases (<8)")
        return None
    base_log = np.array(base_log); logsf = np.array(logsf); taus = np.array(taus)
    resid0 = logsf - base_log
    w_v5 = 1.0 / (1.0 + np.exp(-KV5 * (taus - CV5)))
    lt = np.log(taus)
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])
    w_bl = 1.0 / (1.0 + np.exp(-KBL * (taus - CBL)))
    bv5, *_ = np.linalg.lstsq(Xv5, resid0, rcond=None)
    bp3, *_ = np.linalg.lstsq(Xp3, resid0, rcond=None)
    pred_log = base_log + (1 - w_bl) * (Xv5 @ bv5) + w_bl * (Xp3 @ bp3)
    resid = logsf - pred_log
    err_pct = (np.exp(pred_log) - np.exp(logsf)) / np.exp(logsf) * 100.0
    order = np.argsort(-np.abs(err_pct))

    feat_corr = []
    for key in [k for k, _ in _OUTLIER_DIAG_FEATS] + ['cov_asym']:
        vals = np.array([feat_rows[i].get(key, np.nan) for i in range(n)])
        m = np.isfinite(vals) & np.isfinite(resid)
        if m.sum() >= 8 and np.std(vals[m]) > 1e-12:
            feat_corr.append((key, float(np.corrcoef(vals[m], resid[m])[0, 1]),
                              int(m.sum())))
    feat_corr.sort(key=lambda t: -abs(t[1]))

    sig_act = np.exp(logsf); sig_pred = np.exp(pred_log)
    is_out = np.abs(err_pct) > 20.0
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.scatter(sig_act[~is_out], sig_pred[~is_out], s=45, c=BLUE,
               edgecolors='white', zorder=3, label='within ±20%')
    if is_out.any():
        ax.scatter(sig_act[is_out], sig_pred[is_out], s=70, c=RED,
                   edgecolors='black', zorder=4, label='outlier (>20%)')
    for i in order[:min(6, n)]:
        ax.annotate(f'{labs[i]} ({err_pct[i]:+.0f}%)', (sig_act[i], sig_pred[i]),
                    fontsize=6, color=RED if is_out[i] else GRAY,
                    xytext=(4, 3), textcoords='offset points')
    lim = [min(sig_act.min(), sig_pred.min())*0.8, max(sig_act.max(), sig_pred.max())*1.2]
    ax.plot(lim, lim, '--', color=GRAY)
    ax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                    color=GREEN, alpha=0.12)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('σ_actual (Stage E / Physics, mS/cm)')
    ax.set_ylabel('σ_predicted (v12 form)')
    top_corr = '  '.join(f'{k}:{r:+.2f}' for k, r, _ in feat_corr[:3])
    ax.set_title(f"Stage-E sigma fit outliers  (n={n}, {int(is_out.sum())} >20%)\n"
                 f"top residual-corr features -> {top_corr}", fontsize=8)
    ax.legend(fontsize=8, loc='upper left'); ax.grid(True, alpha=0.25, which='both')
    outpath = _save(fig, outdir, "ionic_outliers_stage_e.png")

    # "1-1" focus: classify outlier vs not ONLY among the selected samples
    # (residuals/fit from the full corpus; just the displayed subset changes).
    if _FOCUS_CASES:
        fmask = np.array([(rl in _FOCUS_CASES) for rl in real_labs])
        if fmask.any():
            ff, fax = plt.subplots(figsize=FIG_SINGLE)
            fi_out = fmask & is_out; fi_in = fmask & ~is_out
            fax.scatter(sig_act[fi_in], sig_pred[fi_in], s=55, c=BLUE,
                        edgecolors='white', zorder=3, label='within ±20%')
            if fi_out.any():
                fax.scatter(sig_act[fi_out], sig_pred[fi_out], s=80, c=RED,
                            edgecolors='black', zorder=4, label='outlier (>20%)')
            for i in np.where(fmask)[0]:
                fax.annotate(f'{real_labs[i]} ({err_pct[i]:+.0f}%)',
                             (sig_act[i], sig_pred[i]), fontsize=6,
                             color=RED if is_out[i] else GRAY,
                             xytext=(4, 3), textcoords='offset points')
            fax.plot(lim, lim, '--', color=GRAY)
            fax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                             color=GREEN, alpha=0.12)
            fax.set_xscale('log'); fax.set_yscale('log'); fax.set_xlim(lim); fax.set_ylim(lim)
            fax.set_xlabel('σ_actual (Stage E / Physics, mS/cm)')
            fax.set_ylabel('σ_predicted (v12 form)')
            fax.set_title("선택 샘플만 — outlier 판정(전체 fit 기준)  "
                          "(%d개 중 %d outlier)" % (int(fmask.sum()), int(fi_out.sum())),
                          fontsize=8)
            fax.legend(fontsize=8, loc='upper left'); fax.grid(True, alpha=0.25, which='both')
            _save(ff, outdir, "ionic_outliers_stage_e_focus.png")

    feat_keys = [k for k, _ in _OUTLIER_DIAG_FEATS] + ['cov_asym']
    # Feature medians/stds for per-case z-scores (reason inference)
    fmed, fstd = {}, {}
    for k in feat_keys:
        vv = np.array([feat_rows[i].get(k, np.nan) for i in range(n)])
        vv = vv[np.isfinite(vv)]
        if len(vv) >= 5:
            fmed[k] = float(np.median(vv)); fstd[k] = float(np.std(vv)) or 1.0

    def _ps_note(name):
        nm = (name or '').replace(' ', '')
        for ps in ('0:10', '10:0', '7:3', '3:7', '5:5', '8:2', '2:8'):
            if ps in nm:
                return ps
        return ''

    def _reason(i):
        parts = []
        ps = _ps_note(labs[i])
        if ps == '0:10':
            parts.append('순수 AM_S(0:10) — 임계 근처·packing 다름')
        elif ps == '10:0':
            parts.append('순수 AM_P(10:0)')
        elif ps:
            parts.append(f'P:S={ps}')
        parts.append('과대예측(σ_pred>실측)' if err_pct[i] > 0 else '과소예측(σ_pred<실측)')
        best, bz = None, 0.0
        for k in feat_keys:
            v = feat_rows[i].get(k, np.nan)
            if k in fmed and np.isfinite(v):
                z = (v - fmed[k]) / fstd[k]
                if abs(z) > abs(bz):
                    bz, best = z, k
        if best and abs(bz) > 1.2:
            parts.append(f'{best} {"높음" if bz > 0 else "낮음"} (z={bz:+.1f})')
        return ' · '.join(parts)

    outliers = [{'case': real_labs[i], 'ps': labs[i],
                 'err_pct': round(float(err_pct[i]), 1),
                 'sigma_act': round(float(sig_act[i]), 4),
                 'sigma_pred': round(float(sig_pred[i]), 4),
                 'direction': 'over' if err_pct[i] > 0 else 'under',
                 'reason': _reason(i)}
                for i in order if is_out[i]]
    import json as _json
    with open(os.path.join(outdir, "ionic_outliers_stage_e_data.json"), 'w',
              encoding='utf-8') as jf:
        _json.dump({'n': n, 'n_outliers': int(is_out.sum()),
                    'top_corr': [{'feature': k, 'r': round(r, 3)} for k, r, _ in feat_corr[:5]],
                    'outliers': outliers}, jf, ensure_ascii=False, indent=1)
    with open(os.path.join(outdir, "ionic_outliers_stage_e.csv"), 'w', newline='',
              encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['Case', 'P:S', 'sigma_act', 'sigma_pred', 'err_%', 'reason'] + feat_keys)
        for i in order:
            wr.writerow([real_labs[i], labs[i], round(sig_act[i], 4), round(sig_pred[i], 4),
                         round(err_pct[i], 1), _reason(i) if is_out[i] else '']
                        + [('' if not np.isfinite(feat_rows[i].get(k, np.nan))
                            else round(feat_rows[i][k], 4)) for k in feat_keys])
    return outpath


def plot_ionic_sizeterm_test(data_list, names, outdir):
    """TEST: can GATED multiplicative correction terms pull in the fit
    outliers without hurting global LOOCV?  4-way comparison of the fixed
    physics form with NO extra / +SE-size / +AM-asym / +BOTH:

      × exp(β_s · g_φ · [ln(size)−mean])         (SE grain size)
      × exp(β_a · g_mix · [asym−mean])            (AM_P/AM_S asymmetry)

    g_φ = σ(−K(φ−φ_gate)) turns the SE-size penalty ON near the percolation
    threshold (sparse SE → GB series resistance bites); g_mix is a Gaussian
    in the AM_P fraction p centered at 0.5 → ON for mixed-AM (7:3/3:7/5:5),
    OFF for pure 0:10 / 10:0.  size = r_SE else 1/gb_density; asym = physics
    coverage(AM_P−AM_S) else ln(r_AM_P/r_AM_S).  β fit by lstsq; LOOCV refits
    every fold (synthetic null ⇒ β≈0, flat LOOCV)."""
    SG = 3.0; PHI_C = 0.19; CN_EXP = 2.0; COV_EXP = 0.5
    PHI_GATE = 0.30; K_G = 12.0; P_MIX_W = 0.25
    base_log, logsf, taus, labs, phis, szlog, asym, pfr = [], [], [], [], [], [], [], []
    for d, nm in zip(data_list, names):
        sig = _stage_e_sigma(d); phi = _get(d, 'phi_se'); cn = _get(d, 'se_se_cn')
        cov = _cov_frac(d, physics=True) or _cov_frac(d, physics=False)
        fp = _get(d, 'percolation_pct')/100.0
        tau = _get(d, 'tortuosity_recommended', _get(d, 'tortuosity_mean', 0))
        sz = _se_size_proxy(d)
        if not (sig and sig > 0 and phi > PHI_C and cn > 0 and cov and cov > 0
                and fp > 0 and tau > 0 and sz and sz > 0):
            continue
        base_log.append(np.log(SG) + 0.5*np.log(phi-PHI_C) + CN_EXP*np.log(cn)
                        + COV_EXP*np.log(cov) + 3.0*np.log(fp))
        logsf.append(np.log(sig)); taus.append(tau); labs.append(nm)
        phis.append(phi); szlog.append(np.log(sz))
        av = _am_asym_proxy(d); asym.append(av if av is not None else 0.0)
        pfr.append(_ps_fraction(d))
    n = len(taus)
    if n < 12:
        print(f"  [SKIP] ionic_sizeterm_test: only {n} cases (<12) with a size proxy")
        return None
    base_log = np.array(base_log); logsf = np.array(logsf); taus = np.array(taus)
    phis = np.array(phis); szlog = np.array(szlog)
    asym = np.array(asym); pfr = np.array(pfr)
    g_phi = 1.0/(1.0+np.exp(K_G*(phis-PHI_GATE)))
    g_mix = np.exp(-0.5*((pfr-0.5)/P_MIX_W)**2)
    sfeat = g_phi*szlog            # SE-size feature (centered inside the fit)
    afeat = g_mix*asym             # AM-asymmetry feature

    # Near-threshold SATURATION base: round the percolation singularity so the
    # 62:38 / 0:10 cases (φ≈φc, where √(φ−φc) is hyper-sensitive) are tamed.
    # φ_eff = sqrt((φ−φc)² + δ²)  →  ≈ φ−φc far above φc, floors at δ near it.
    DELTA = 0.03
    phi_ex = np.maximum(phis - PHI_C, 1e-6)
    base_log_sat = base_log + 0.5*(np.log(np.sqrt(phi_ex**2 + DELTA**2)) - np.log(phi_ex))

    r2_n, lo_n, _, _, pred_n, _, _ = _cblend_fit_score(base_log, logsf, taus)
    r2_s, lo_s, b_s, pred_s = _cblend_extra_score(base_log, logsf, taus, sfeat)
    r2_a, lo_a, b_a, pred_a = _cblend_extra_score(base_log, logsf, taus, afeat)
    r2_b, lo_b, b_b, pred_b = _cblend_extra_score(
        base_log, logsf, taus, np.column_stack([sfeat, afeat]))
    r2_t, lo_t, _, _, pred_t, _, _ = _cblend_fit_score(base_log_sat, logsf, taus)
    r2_ta, lo_ta, b_ta, pred_ta = _cblend_extra_score(base_log_sat, logsf, taus, afeat)

    act = np.exp(logsf)
    def _out(pred):
        return np.abs((np.exp(pred)-act)/act*100.0) > 20.0
    panels = [('NO extra term', pred_n, r2_n, lo_n, ''),
              ('+ SE-size (g_phi)', pred_s, r2_s, lo_s, f'beta_s={b_s[0]:+.3f}'),
              ('+ AM-asym (g_mix)', pred_a, r2_a, lo_a, f'beta_a={b_a[0]:+.3f}'),
              ('+ BOTH (size+asym)', pred_b, r2_b, lo_b, f'beta_s={b_b[0]:+.3f} beta_a={b_b[1]:+.3f}'),
              ('SAT phic (rounded, d=%.2f)' % DELTA, pred_t, r2_t, lo_t, ''),
              ('SAT + AM-asym', pred_ta, r2_ta, lo_ta, f'beta_a={b_ta[0]:+.3f}')]

    def _is(nm, ps):
        return ps in (nm or '').replace(' ', '')
    m010 = np.array([_is(l, '0:10') for l in labs])
    mmix = np.array([(_is(l, '7:3') or _is(l, '3:7') or _is(l, '5:5')) for l in labs])

    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    for ax, (ttl, pred, r2, lo, btxt) in zip(axes.ravel(), panels):
        sp = np.exp(pred); out = _out(pred)
        base_m = ~m010 & ~mmix
        ax.scatter(act[base_m & ~out], sp[base_m & ~out], s=30, c=BLUE,
                   edgecolors='white', zorder=3, label='other')
        if (out & base_m).any():
            ax.scatter(act[out & base_m], sp[out & base_m], s=55, c=RED,
                       edgecolors='black', zorder=4, label='outlier(>20%)')
        if m010.any():
            ax.scatter(act[m010], sp[m010], s=64, marker='D', c=ORANGE,
                       edgecolors='black', zorder=5, label='0:10')
        if mmix.any():
            ax.scatter(act[mmix], sp[mmix], s=64, marker='s', c=PURPLE,
                       edgecolors='black', zorder=5, label='7:3/3:7/5:5')
        lim = [min(act.min(), sp.min())*0.8, max(act.max(), sp.max())*1.2]
        ax.plot(lim, lim, '--', color=GRAY)
        ax.fill_between(lim, [v*0.8 for v in lim], [v*1.2 for v in lim],
                        color=GREEN, alpha=0.12)
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_xlabel('σ_actual (Stage E / Physics, mS/cm)')
        ax.set_ylabel('σ_predicted (mS/cm)')
        n010 = int((out & m010).sum()); nmix = int((out & mmix).sum())
        ax.set_title(f"{ttl}\nR2={r2:.3f} LOOCV={lo:.3f}  out={int(out.sum())} "
                     f"(0:10 {n010}, mix {nmix})  {btxt}", fontsize=8)
        ax.grid(True, alpha=0.25, which='both'); ax.legend(fontsize=6.5, loc='upper left')
    fig.suptitle("Correction-term test (n=%d): size / AM-asym / rounded-phic SAT — catch 0:10(62:38)?\n"
                 "size=r_SE|1/gb_density  asym=cov(P-S)|ln(rP/rS)  g_phi=sig(-%g(phi-%g))  "
                 "g_mix=gauss(p;0.5,%g)  SAT: phi_eff=sqrt((phi-%.2f)^2+%.2f^2)"
                 % (n, K_G, PHI_GATE, P_MIX_W, PHI_C, DELTA), fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    outpath = _save(fig, outdir, "ionic_sizeterm_test.png")

    def _cnt(pred, mask):
        return int((_out(pred) & mask).sum())
    import json as _json
    with open(os.path.join(outdir, "ionic_sizeterm_test.json"), 'w',
              encoding='utf-8') as jf:
        _json.dump({'n': n,
                    'models': {
                        'none': {'r2': round(r2_n, 4), 'loocv': round(lo_n, 4),
                                 'n_out': int(_out(pred_n).sum()),
                                 'out_010': _cnt(pred_n, m010), 'out_mix': _cnt(pred_n, mmix)},
                        'size': {'r2': round(r2_s, 4), 'loocv': round(lo_s, 4),
                                 'beta_s': round(b_s[0], 4),
                                 'n_out': int(_out(pred_s).sum()),
                                 'out_010': _cnt(pred_s, m010), 'out_mix': _cnt(pred_s, mmix)},
                        'asym': {'r2': round(r2_a, 4), 'loocv': round(lo_a, 4),
                                 'beta_a': round(b_a[0], 4),
                                 'n_out': int(_out(pred_a).sum()),
                                 'out_010': _cnt(pred_a, m010), 'out_mix': _cnt(pred_a, mmix)},
                        'both': {'r2': round(r2_b, 4), 'loocv': round(lo_b, 4),
                                 'beta_s': round(b_b[0], 4), 'beta_a': round(b_b[1], 4),
                                 'n_out': int(_out(pred_b).sum()),
                                 'out_010': _cnt(pred_b, m010), 'out_mix': _cnt(pred_b, mmix)},
                        'sat': {'r2': round(r2_t, 4), 'loocv': round(lo_t, 4),
                                'n_out': int(_out(pred_t).sum()),
                                'out_010': _cnt(pred_t, m010), 'out_mix': _cnt(pred_t, mmix)},
                        'sat_asym': {'r2': round(r2_ta, 4), 'loocv': round(lo_ta, 4),
                                     'beta_a': round(b_ta[0], 4),
                                     'n_out': int(_out(pred_ta).sum()),
                                     'out_010': _cnt(pred_ta, m010), 'out_mix': _cnt(pred_ta, mmix)}},
                    'phi_gate': PHI_GATE, 'k_gate': K_G, 'p_mix_w': P_MIX_W, 'delta': DELTA},
                   jf, ensure_ascii=False, indent=1)
    return outpath


_FRAC_STAGES = [('intact', 'Intact', '#4caf50'),
                ('microcrack', 'Microcrack', '#a9d18e'),
                ('multicrack', 'Multi-crack', '#ffd43b'),
                ('fragmentation', 'Fragmentation', '#ff922b'),
                ('pulverization', 'Pulverization', '#e03131')]
_FRAC_PAIRS = ['AM_P-AM_P', 'AM_P-AM_S', 'AM_S-AM_S']


def plot_fracture_stages(data_list, names, outdir):
    """Stacked bar of the force-based fracture-stage distribution (intact →
    pulverization) per case — the Auerbach/Lawn compaction-time damage mix."""
    rows = []
    for d in data_list:
        others = sum(_get(d, f'frac_{s}_force_pct')
                     for s, _, _ in _FRAC_STAGES if s != 'intact')
        iv = d.get('frac_intact_force_pct')
        intact = float(iv) if iv is not None else max(0.0, 100.0 - others)
        rows.append([intact if s == 'intact' else _get(d, f'frac_{s}_force_pct')
                     for s, _, _ in _FRAC_STAGES])
    arr = np.array(rows, dtype=float)
    if arr.shape[0] == 0 or not np.any(arr[:, 1:] > 0):
        print("  [SKIP] fracture_stages: no AM-AM fracture data")
        return None
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names)); bottom = np.zeros(len(names))
    for i, (_s, lbl, col) in enumerate(_FRAC_STAGES):
        ax.bar(x, arr[:, i], bottom=bottom, color=col, label=lbl, width=0.62)
        bottom += arr[:, i]
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha='right', fontsize=8)
    ax.set_ylabel('contact fraction (%)'); ax.set_ylim(0, 100)
    ax.set_title('Fracture stage distribution (force-based)', fontsize=10)
    ax.legend(fontsize=7, ncol=5, loc='upper center', bbox_to_anchor=(0.5, -0.16))
    outpath = _save(fig, outdir, "fracture_stages.png")
    with open(os.path.join(outdir, "fracture_stages.csv"), 'w', newline='',
              encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Case'] + [lbl for _s, lbl, _c in _FRAC_STAGES])
        for nm, r in zip(names, rows):
            w.writerow([nm] + [round(v, 3) for v in r])
    return outpath


def plot_fracture_pairtype(data_list, names, outdir):
    """Grouped bar of severe % (fragmentation + pulverization, force-based) per
    AM-AM pair type — shows which contact type actually fails."""
    sev = {pt: [] for pt in _FRAC_PAIRS}
    present = []
    for pt in _FRAC_PAIRS:
        any_here = False
        for d in data_list:
            n = (d.get(f'n_total_force_{pt}') or d.get(f'n_total_{pt}') or 0)
            s = (_get(d, f'frac_fragmentation_force_{pt}_pct')
                 + _get(d, f'frac_pulverization_force_{pt}_pct'))
            sev[pt].append(s if n else 0.0)
            if n:
                any_here = True
        if any_here:
            present.append(pt)
    if not present:
        print("  [SKIP] fracture_pairtype: no pair-type fracture data")
        return None
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    x = np.arange(len(names)); nbar = len(present)
    bw = 0.8 / max(nbar, 1)
    pair_col = {'AM_P-AM_P': '#e03131', 'AM_P-AM_S': '#ffd43b', 'AM_S-AM_S': '#4caf50'}
    for j, pt in enumerate(present):
        ax.bar(x + j * bw - 0.4 + bw / 2, sev[pt], bw, label=pt,
               color=pair_col.get(pt, GRAY))
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha='right', fontsize=8)
    ax.set_ylabel('severe % (frag + pulv)')
    ax.set_title('Severe fracture by AM-AM pair type (force-based)', fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(True, axis='y', alpha=0.25)
    outpath = _save(fig, outdir, "fracture_pairtype.png")
    with open(os.path.join(outdir, "fracture_pairtype.csv"), 'w', newline='',
              encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Case'] + present)
        for i, nm in enumerate(names):
            w.writerow([nm] + [round(sev[pt][i], 3) for pt in present])
    return outpath


def plot_param_scatter(data_list, names, outdir):
    """X–Y scatter of any two metrics across the selected cases, with a
    least-squares trend line and Pearson r."""
    px, py = _PARAM_X, _PARAM_Y
    if not px or not py:
        print("  [SKIP] param_scatter: param-x/param-y not provided")
        return None
    xs, ys, labels = [], [], []
    for d, nm in zip(data_list, names):
        mp = _merged_params(d)
        x, y = mp.get(px), mp.get(py)
        if x is not None and y is not None:
            xs.append(x); ys.append(y); labels.append(nm)
    if len(xs) < 2:
        print(f"  [SKIP] param_scatter: <2 cases have both {px} & {py}")
        return None
    xs_a, ys_a = np.array(xs), np.array(ys)
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    cols = _case_colors(len(xs))
    ax.scatter(xs_a, ys_a, c=cols, s=70, edgecolors='white', linewidths=0.8, zorder=3)
    for x, y, nm in zip(xs, ys, labels):
        ax.annotate(nm, (x, y), fontsize=7, xytext=(4, 4),
                    textcoords='offset points', color=BLACK)
    title = f"{_param_label(py)}  vs  {_param_label(px)}"
    if len(xs) >= 3 and np.std(xs_a) > 0:
        b1, b0 = np.polyfit(xs_a, ys_a, 1)
        xr = np.linspace(xs_a.min(), xs_a.max(), 50)
        ax.plot(xr, b1 * xr + b0, '--', color=GRAY, lw=1.2, zorder=2)
        r = float(np.corrcoef(xs_a, ys_a)[0, 1])
        title += f"   (r = {r:+.2f}, n = {len(xs)})"
    ax.set_xlabel(_param_label(px)); ax.set_ylabel(_param_label(py))
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.25)
    outpath = _save(fig, outdir, "param_scatter.png")
    with open(os.path.join(outdir, "param_scatter.csv"), 'w', newline='',
              encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Case', _param_label(px), _param_label(py)])
        for x, y, nm in zip(xs, ys, labels):
            w.writerow([nm, round(x, 6), round(y, 6)])
    return outpath


def plot_param_bar(data_list, names, outdir):
    """Grouped bar of several metrics across cases.  When _PARAM_NORM, each
    metric is scaled to its max across cases so different units are
    comparable on one axis."""
    keys = _PARAM_LIST or []
    if not keys:
        print("  [SKIP] param_bar: no params provided")
        return None
    mps = [_merged_params(d) for d in data_list]
    keys = [k for k in keys if any(k in mp for mp in mps)]
    if not keys:
        print("  [SKIP] param_bar: none of the params present")
        return None
    ncase = len(data_list)
    fig_w = max(7, 1.1 * len(keys) * max(1, ncase * 0.35))
    fig, ax = plt.subplots(figsize=(min(fig_w, 18), 5))
    cols = _case_colors(ncase)
    group_w = 0.8
    bar_w = group_w / max(ncase, 1)
    xbase = np.arange(len(keys))
    for ci in range(ncase):
        vals = []
        for k in keys:
            v = mps[ci].get(k)
            if v is not None and _PARAM_NORM:
                col = [mp.get(k) for mp in mps if mp.get(k) is not None]
                mx = max((abs(c) for c in col), default=0) or 1.0
                v = v / mx
            vals.append(v if v is not None else 0.0)
        ax.bar(xbase + ci * bar_w - group_w / 2 + bar_w / 2, vals, bar_w,
               label=names[ci], color=cols[ci])
    ax.set_xticks(xbase)
    ax.set_xticklabels([_param_label(k) for k in keys], rotation=30, ha='right',
                       fontsize=8)
    ax.set_ylabel('normalized (value / max)' if _PARAM_NORM else 'value')
    ax.set_title('Parameter comparison' + (' (normalized)' if _PARAM_NORM else ''),
                 fontsize=10)
    ax.legend(fontsize=7, ncol=min(ncase, 4))
    ax.grid(True, axis='y', alpha=0.25)
    outpath = _save(fig, outdir, "param_bar.png")
    with open(os.path.join(outdir, "param_bar.csv"), 'w', newline='',
              encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Case'] + [_param_label(k) for k in keys])
        for ci in range(ncase):
            w.writerow([names[ci]] + [mps[ci].get(k, '') for k in keys])
    return outpath


def plot_param_corr(data_list, names, outdir):
    """Pearson correlation heatmap among the selected metrics over the case
    set (needs ≥3 cases and ≥2 metrics with variation)."""
    keys = _PARAM_LIST or []
    mps = [_merged_params(d) for d in data_list]
    # Keep keys present in every case (so correlation uses a full matrix)
    keys = [k for k in keys if all(k in mp for mp in mps)]
    if len(keys) < 2 or len(data_list) < 3:
        print(f"  [SKIP] param_corr: need ≥2 common params & ≥3 cases "
              f"(have {len(keys)} params, {len(data_list)} cases)")
        return None
    mat = np.array([[mp[k] for k in keys] for mp in mps], dtype=float)  # cases × params
    # Drop zero-variance columns (corr undefined)
    keep = [i for i in range(len(keys)) if np.std(mat[:, i]) > 1e-12]
    if len(keep) < 2:
        print("  [SKIP] param_corr: <2 params with variation")
        return None
    keys = [keys[i] for i in keep]
    mat = mat[:, keep]
    corr = np.corrcoef(mat, rowvar=False)
    n = len(keys)
    fig, ax = plt.subplots(figsize=(max(5, 0.7 * n + 2), max(4, 0.7 * n + 1.5)))
    im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels([_param_label(k) for k in keys], rotation=45, ha='right',
                       fontsize=7)
    ax.set_yticklabels([_param_label(k) for k in keys], fontsize=7)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{corr[i, j]:.2f}', ha='center', va='center',
                    fontsize=6,
                    color='white' if abs(corr[i, j]) > 0.6 else BLACK)
    ax.set_title(f'Parameter correlation matrix (Pearson r, n={len(data_list)})',
                 fontsize=10)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    outpath = _save(fig, outdir, "param_corr.png")
    return outpath


PLOT_REGISTRY["param_scatter"] = {
    "func": plot_param_scatter,
    "file": "param_scatter.png",
    "title": "파라미터 X–Y 산점도",
    "description": "선택한 두 파라미터를 케이스별 점으로 비교.\n추세선 + Pearson 상관계수 r 표시.\n분석요약·3D뷰어의 모든 수치 중 임의 2개 선택 가능.",
    "origin_tip": "Scatter → X: param-x, Y: param-y. 점에 케이스명 라벨, 점선 추세선.",
}
PLOT_REGISTRY["param_bar"] = {
    "func": plot_param_bar,
    "file": "param_bar.png",
    "title": "파라미터 다중 비교 (Bar)",
    "description": "선택한 여러 파라미터를 케이스별 grouped bar로 비교.\n정규화 옵션이면 각 파라미터를 자기 최댓값으로 나눠 단위가 달라도 한 축에서 비교.",
    "origin_tip": "Grouped Column → X: parameter, 색: case. 정규화 시 Y=÷max.",
}
PLOT_REGISTRY["param_corr"] = {
    "func": plot_param_corr,
    "file": "param_corr.png",
    "title": "파라미터 상관 Heatmap",
    "description": "선택한 파라미터들 사이의 Pearson 상관계수 행렬.\n어떤 지표가 함께 움직이는지(+1) / 반대로 움직이는지(−1) 한눈에.\n케이스 ≥3개, 변동 있는 파라미터 ≥2개 필요.",
    "origin_tip": "Heatmap (RdBu, −1~+1). 셀에 r 값 표기.",
}
PLOT_REGISTRY["ionic_solver_vs_stage_e"] = {
    "func": plot_ionic_solver_vs_stage_e,
    "file": "ionic_solver_vs_stage_e.png",
    "title": "σ_ionic: Network solver vs Stage E",
    "description": "케이스별 σ_ionic을 (1) Hertzian network solver, (2) Physics(Tabor+volume) solver, (3) Stage E final 셋으로 나란히 비교.\nHertzian→Physics 접촉모델 변화 + Stage E grain 보정이 σ를 얼마나 바꾸는지 한눈에.",
    "origin_tip": "Grouped Column → X: case, 3 bars (Hertzian/Physics/StageE).",
}
PLOT_REGISTRY["ionic_fit_stage_e"] = {
    "func": plot_ionic_fit_stage_e,
    "file": "ionic_fit_stage_e.png",
    "title": "σ_ionic → Stage E (물리식 재적합)",
    "description": "Stage-E(또는 Physics) σ_ionic을 타깃으로, 물리 고정식(√(φ−0.2)·CN^(3/2)·cov^(2/5)·f_p³)에 C_blend(τ)만 재적합 (parity + R²/LOOCV).\n지수는 물리값으로 고정(과적합 방지). 자유지수 진단치는 CSV에 함께 기록 — physics 타깃이 같은 지수를 원하는지 확인용.",
    "origin_tip": "Scatter parity (log-log) + 1:1 + ±20%. 제목에 물리식 + C_blend(Ct/Cn).",
}
PLOT_REGISTRY["ionic_decomp_physics"] = {
    "func": plot_ionic_decomp_physics,
    "file": "ionic_decomp_physics.png",
    "title": "σ_ionic PHYSICS factor decomposition",
    "description": "PHYSICS 고정식의 5개 factor 전부를 stack으로 분해: (φ−0.19)^0.5 · CN² · cov^0.5 · f_p³ · C_blend(τ). τ는 C_blend(τ)로 포함. 각 factor의 Δlog 기여를 ref(최고 σ) 대비 표시.",
    "origin_tip": "상단 stacked bar(factor별 Δlog), 하단 case별 dominant factor.",
}
PLOT_REGISTRY["ionic_perconfig_physics"] = {
    "func": plot_ionic_perconfig_physics,
    "file": "ionic_perconfig_physics.png",
    "title": "σ_ionic PHYSICS per-config (fixed form)",
    "description": "PHYSICS 모드 per-config 라인 plot: 고정 physics식 (C_blend(τ)·σ_grain·(φ−0.19)^0.5·CN²·cov^0.5·f_p³) vs PHYSICS 네트워크 솔버 σ, 그룹별 구분선.\nHertzian을 쓰는 multiscale 대신 physics 버전.",
    "origin_tip": "Line: 빨강=고정 physics식, 초록 점선=physics solver. 그룹 구분선.",
}
PLOT_REGISTRY["ionic_outliers_stage_e"] = {
    "func": plot_ionic_outliers_stage_e,
    "file": "ionic_outliers_stage_e.png",
    "title": "σ_ionic Stage E — outlier 진단",
    "description": "물리 v12 fit의 worst-fit 케이스(>±20%)를 빨강+이름으로 강조하고, 잔차와 가장 상관 높은 구조 feature를 표시 (= base 식이 놓친 물리 = 다음에 곱할 후보).\nCSV: |err| 내림차순 케이스별 feature + 잔차-feature 상관.",
    "origin_tip": "Parity(log-log), outlier 빨강 라벨. CSV로 outlier 원인 분석.",
}
PLOT_REGISTRY["ionic_sizeterm_test"] = {
    "func": plot_ionic_sizeterm_test,
    "file": "ionic_sizeterm_test.png",
    "title": "σ_ionic 게이트 보정항 TEST (SE-size · AM-asym · 둘다)",
    "description": "고정 물리식에 게이트 곱셈 보정항을 넣어 4-way(無 / +SE-입자크기 / +AM비대칭 / +둘다) parity로 비교.\n①SE-size × exp(β_s·g_φ·[ln(size)−mean]) — g_φ=σ(−12(φ−0.30))로 임계 근처(0:10·저-SE)에서만 ON, GB 직렬저항. ②AM-asym × exp(β_a·g_mix·[asym−mean]) — g_mix=가우시안(p;0.5)로 mixed-AM(7:3·3:7·5:5)에서만 ON, AM_P/AM_S 피복 비대칭. size=r_SE|1/gb_density, asym=physics cov(P−S)|ln(rP/rS).\n각 패널 제목에 R²·LOOCV·outlier 수(전체·0:10·mix)·β. LOOCV가 fold마다 β 재적합 → 과적합 정직 판정.",
    "origin_tip": "2×2 parity. 0:10=주황 다이아, 7:3/3:7/5:5=보라 사각. LOOCV 개선 + outlier 감소를 동시에 확인.",
}
PLOT_REGISTRY["fracture_stages"] = {
    "func": plot_fracture_stages,
    "file": "fracture_stages.png",
    "title": "취성 파괴 단계 분포 (Stacked)",
    "description": "케이스별 force-based 파괴 단계(intact→micro→multi→frag→pulv)를\nstacked bar로 비교. 압착 시점 손상 mix를 한눈에.\n(generic 산점도로는 못 보는 5단계 조성 비교)",
    "origin_tip": "Stacked Column → X: case, 5 stages 누적. 색: green→red.",
}
PLOT_REGISTRY["fracture_pairtype"] = {
    "func": plot_fracture_pairtype,
    "file": "fracture_pairtype.png",
    "title": "취성 파괴 — pair-type별 Severe%",
    "description": "AM_P-AM_P / AM_P-AM_S / AM_S-AM_S 별 severe%(frag+pulv) 비교.\n어떤 접촉 타입이 실제로 깨지는지 식별 (보통 AM_P-AM_P가 위험).",
    "origin_tip": "Grouped Column → X: case, 색: pair type.",
}


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputs", nargs="+", required=True)
    parser.add_argument("-n", "--names", nargs="+", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-p", "--plots", nargs="+",
                        default=list(PLOT_REGISTRY.keys()) + ["four_panel"])
    parser.add_argument("--group-sizes", default="")  # e.g. "3,5"
    parser.add_argument("--group-names", default="")  # e.g. "Case A,Case B"
    parser.add_argument("--global-rgb", default="")   # e.g. "5.21,0.20" (b,ln_k from global fit)
    parser.add_argument("--global-c-ion", default="")  # e.g. "0.0727" (C from ionic scaling fit)
    parser.add_argument("--y-max-sigma", type=float, default=None,
                        help="Fixed y-axis max (mS/cm) for multiscale σ plots; enables cross-run visual comparison")
    # Generic parameter-comparison selections
    parser.add_argument("--param-x", default="")   # scatter X metric key
    parser.add_argument("--param-y", default="")   # scatter Y metric key
    parser.add_argument("--param-list", default="")  # comma-separated keys (bar/corr)
    parser.add_argument("--param-norm", action="store_true")  # normalize bar to max
    parser.add_argument("--focus-cases", default="")  # \\t-separated saved names → "1-1" focus parity
    parser.add_argument("--focus-label", default="")  # group name(s) shown on the 1-1 plot
    parser.add_argument("--fit-corpus-inputs", nargs="*", default=[])  # full corpus for global fit stats
    args = parser.parse_args()

    global _PARAM_X, _PARAM_Y, _PARAM_LIST, _PARAM_NORM, _FOCUS_CASES, _FOCUS_LABEL, _FIT_CORPUS
    _PARAM_X = args.param_x or None
    _PARAM_Y = args.param_y or None
    _PARAM_LIST = [k for k in args.param_list.split(',') if k] or None
    _PARAM_NORM = bool(args.param_norm)
    _FOCUS_CASES = set(s for s in args.focus_cases.split('\t') if s)
    _FOCUS_LABEL = args.focus_label or ""
    _FIT_CORPUS = []
    for _p in (args.fit_corpus_inputs or []):
        try:
            with open(_p) as _f:
                _FIT_CORPUS.append(json.load(_f))
        except Exception:
            pass

    # Parse group info
    if args.group_sizes:
        args.group_sizes_list = [int(x) for x in args.group_sizes.split(',')]
        args.group_names_list = args.group_names.split(',') if args.group_names else [f"Case {chr(65+i)}" for i in range(len(args.group_sizes_list))]
    else:
        args.group_sizes_list = None
        args.group_names_list = None

    if len(args.inputs) != len(args.names):
        print(f"ERROR: inputs ({len(args.inputs)}) != names ({len(args.names)})")
        sys.exit(1)

    global _ALL_DATA, _REAL_NAMES
    all_data = []
    for path in args.inputs:
        with open(path, "r") as f:
            d = json.load(f)
        d["_source_path"] = path
        all_data.append(d)
    _ALL_DATA = all_data
    _REAL_NAMES = list(args.names)

    # Use P:S ratio as x-axis labels (fallback to case names)
    plot_names = []
    for i, d in enumerate(all_data):
        ps = d.get('ps_ratio', '')
        if ps:
            plot_names.append(ps)
        else:
            plot_names.append(args.names[i])

    os.makedirs(args.output, exist_ok=True)
    plot_info = {}

    # Try to pre-load fitted v29 + v32 params from disk cache. Webapp
    # invokes this script multiple times per render (one subprocess per
    # plot group / per plot subset), so module globals do not carry
    # across calls. The parity plot writes the cache; every subsequent
    # subprocess can now pick it up as long as the case list matches.
    global _V32_FITTED_GAMMAS, _GLOBAL_IONIC_SIGMOID, _GLOBAL_IONIC_POLY3, _GLOBAL_PS_SIGMOID
    _cached = _load_v29_cache(args.names)
    if _cached:
        _sig, _p3, _ps, _v32g = _cached
        if _sig: _GLOBAL_IONIC_SIGMOID = _sig
        if _p3:  _GLOBAL_IONIC_POLY3   = _p3
        if _ps:  _GLOBAL_PS_SIGMOID    = _ps
        if _v32g: _V32_FITTED_GAMMAS   = dict(_v32g)

    # Set global group info for _apply_style
    global _GROUP_INFO, _GLOBAL_RGB, _Y_MAX_SIGMA
    if args.group_sizes_list and len(args.group_sizes_list) > 1:
        _GROUP_INFO = (args.group_sizes_list, args.group_names_list)
    else:
        _GROUP_INFO = None
    _Y_MAX_SIGMA = args.y_max_sigma  # None = auto, else fixed (cross-run unified)

    # Set global R_gb if provided (from combined fit across all plot groups)
    if args.global_rgb:
        parts = args.global_rgb.split(',')
        if len(parts) >= 2:
            _GLOBAL_RGB = (float(parts[0]), float(parts[1]))
            print(f"  Using global R_gb: b={_GLOBAL_RGB[0]:.2f}, ln(k)={_GLOBAL_RGB[1]:.2f}")
    else:
        _GLOBAL_RGB = None

    # Set global C for ionic scaling if provided
    global _GLOBAL_C_ION
    if args.global_c_ion:
        _GLOBAL_C_ION = float(args.global_c_ion)
        print(f"  Using global C_ion: {_GLOBAL_C_ION:.6f}")
    else:
        _GLOBAL_C_ION = None

    # Generate particle info table as first plot
    if 'particle_info' in args.plots or True:  # always generate
        _generate_particle_info(all_data, plot_names, args.names, args.output)
        plot_info['particle_info'] = {
            'file': 'particle_info.png',
            'title': '입자 정보',
            'description': '각 케이스별 AM_P, AM_S, SE 입자수와 반지름.\nSE 크기가 같으면 비교 조건 동일.',
            'origin_tip': 'Table 형태로 Origin에서는 Worksheet에 직접 입력.',
        }

    # Generate CSV for each plot type
    csv_map = {
        'porosity': [('Case', None), ('Porosity(%)', lambda d: _get(d, 'porosity'))],
        'am_se_interface': [('Case', None),
            ('AM_P-SE(μm²)', lambda d: _resolve_am_se(d)[0]),
            ('AM_S-SE(μm²)', lambda d: _resolve_am_se(d)[1]),
            ('Total(μm²)', lambda d: _get(d, 'area_AM전체_SE_total') or sum(_resolve_am_se(d)))],
        'se_se_tradeoff': [('Case', None),
            ('SE-SE Count', lambda d: _get(d, 'area_SE_SE_n')),
            ('SE-SE Mean Area(μm²)', lambda d: _get(d, 'area_SE_SE_mean'))],
        'se_se_total': [('Case', None),
            ('SE-SE Total(μm²)', lambda d: _get(d, 'area_SE_SE_total'))],
        'percolation_tortuosity': [('Case', None),
            ('Percolation(%)', lambda d: _get(d, 'percolation_pct')),
            ('Tortuosity', lambda d: _get(d, 'tortuosity_mean'))],
        'ionic_active': [('Case', None),
            ('Ionic Active AM(%)', lambda d: _get(d, 'ionic_active_pct'))],
        'coverage': [('Case', None),
            ('Coverage AM_P(%)', lambda d: _resolve_coverage(d)[0]),
            ('Coverage AM_P std', lambda d: _resolve_coverage(d)[1]),
            ('Coverage AM_S(%)', lambda d: _resolve_coverage(d)[2]),
            ('Coverage AM_S std', lambda d: _resolve_coverage(d)[3])],
        'stress_cv': [('Case', None),
            ('Stress CV(%)', lambda d: _get(d, 'stress_cv'))],
        'stress_ratio': [('Case', None),
            ('σ_AM_P/σ_mean', lambda d: _get(d, 'stress_ratio_AM_P')),
            ('σ_AM_S/σ_mean', lambda d: _get(d, 'stress_ratio_AM_S')),
            ('σ_SE/σ_mean', lambda d: _get(d, 'stress_ratio_SE'))],
        'stress_z_layer': [('Case', None),
            ('Z_data', lambda d: str(d.get('stress_z_layer_cv', [])))],
    }

    import csv
    for pname, cols in csv_map.items():
        if pname in args.plots:
            csv_path = os.path.join(args.output, f"{pname}.csv")
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([c[0] for c in cols])
                for i, name in enumerate(plot_names):
                    row = []
                    for col_name, fn in cols:
                        if fn is None:
                            row.append(name)
                        else:
                            val = fn(all_data[i])
                            if isinstance(val, (int, float)):
                                row.append(round(val, 4))
                            else:
                                row.append(val)
                    writer.writerow(row)

    for plot_name in args.plots:
        if plot_name == "four_panel":
            outpath = plot_four_panel(all_data, plot_names, args.output)
            plot_info["four_panel"] = {
                "file": "four_panel.png",
                "title": "Four-Panel Composite",
                "description": "Porosity, AM-SE Interface, SE-SE Trade-off,\nPercolation/Tortuosity 4개 핵심 지표를 2×2 패널로 종합 비교.\n\n논문 Figure로 적합.",
                "origin_tip": "Graph > Merge Multiple Graphs.\n2×2 layout, 각 패널 개별 설정.\n전체 크기: 14×10 inch.",
            }
            print(f"  [OK] four_panel -> {outpath}")
            continue

        if plot_name not in PLOT_REGISTRY:
            print(f"  [SKIP] Unknown: {plot_name}")
            continue

        entry = PLOT_REGISTRY[plot_name]
        # min_groups check: skip if not enough case groups
        min_groups = entry.get("min_groups", 1)
        n_groups = len(_GROUP_INFO[0]) if _GROUP_INFO else 1
        if n_groups < min_groups:
            print(f"  [SKIP] {plot_name}: requires {min_groups}+ case groups (have {n_groups})")
            continue
        func = entry["func"]
        import inspect
        params = inspect.signature(func).parameters
        if 'outdir' in params:
            # Standalone plot (creates own fig, saves itself)
            outpath = func(all_data, plot_names, args.output)
            if outpath is None:
                # R² too low — generate "Bruggeman reference" note
                if plot_name in ('rgb_fitting', 'gb_corrected'):
                    _, _, _, r2_val = _fit_r_gb(all_data, plot_names, use_global=False)
                    plot_info[plot_name] = {
                        "file": "",
                        "csv": None,
                        "title": entry["title"] + " (skipped)",
                        "description": f"R²={r2_val:.4f} < {R_GB_MIN_R2}: fitting not reliable.\nBruggeman reference only.\nRVE size or data range insufficient.",
                        "origin_tip": "",
                    }
                continue
        else:
            fig, ax = plt.subplots(figsize=FIG_SINGLE)
            func(all_data, plot_names, ax=ax)
            outpath = _save(fig, args.output, entry["file"])

        # Check for CSV from csv_map (legacy) or standalone _write_csv
        csv_file = f"{plot_name}.csv" if plot_name in csv_map else None
        if csv_file is None:
            standalone_csv = os.path.join(args.output, f"{plot_name}.csv")
            if os.path.exists(standalone_csv):
                csv_file = f"{plot_name}.csv"
        # Dynamic description: replace {formx_r2}, {formx_loocv} with actual values
        desc = entry["description"]
        if _GLOBAL_FORMX_R2 is not None:
            r2_val, loocv_val = _GLOBAL_FORMX_R2
            desc = desc.replace("{formx_r2}", f"{r2_val:.3f}")
            desc = desc.replace("{formx_loocv}", f"{loocv_val:.3f}")
        elif '{formx_r2}' in desc:
            # Compute FORM X R² on the fly (same logic as plot_ionic_scaling_fit)
            try:
                PHI_C = 0.185; SGRAIN = 3.0
                _phi_se = np.array([_get(d, "phi_se", 0) for d in all_data])
                _cn_se = np.array([_get(d, "se_se_cn", 0) for d in all_data])
                _tau_se = np.array([max(_get(d, "tortuosity_recommended", _get(d, "tortuosity_mean", 1)), 0.1) for d in all_data])
                _cov_se = np.array([(lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)([v for v in [_get(d,"coverage_AM_P_mean",0),_get(d,"coverage_AM_S_mean",0),_get(d,"coverage_AM_mean",0)] if v>0]) for d in all_data])
                _snet = np.array(_load_network_sigma(all_data))
                _gb = np.array([_get(d, "gb_density_mean", 0) for d in all_data])
                _gp = np.array([_get(d, "path_conductance_mean", 0) for d in all_data])
                # Match ionic_scaling_fit filter: require gb_density and path_conductance
                _valid = (_phi_se > PHI_C+0.01) & (_cn_se > 0) & (_tau_se > 0) & (_cov_se > 0) & (_snet > 0.01) & (_gb > 0) & (_gp > 0)
                if _valid.sum() >= 5:
                    _phi_ex = np.clip(_phi_se[_valid] - PHI_C, 0.001, None)
                    _fp_se = np.clip(np.array([_get(d, "percolation_pct", 100) / 100 for d in all_data])[_valid], 0.01, 1.0)
                    _log_rhs = np.log(SGRAIN) + 0.75*np.log(_phi_ex) + 1.5*np.log(_cn_se[_valid]) + 0.25*np.log(_cov_se[_valid]) + 2.0*np.log(_fp_se)
                    _log_s = np.log(_snet[_valid])
                    _log_tau = np.log(_tau_se[_valid])
                    _w_sig = 1.0 / (1.0 + np.exp(-5.0 * (_tau_se[_valid] - 2.1)))
                    _w_bl = 1.0 / (1.0 + np.exp(-15.0 * (_tau_se[_valid] - 2.0)))
                    # v9 BLEND fit
                    _X_v5 = np.column_stack([np.ones(_valid.sum()), _w_sig])
                    _X_p3 = np.column_stack([np.ones(_valid.sum()), _log_tau, _log_tau**2, _log_tau**3])
                    _b_v5 = np.linalg.lstsq(_X_v5, _log_s - _log_rhs, rcond=None)[0]
                    _b_p3 = np.linalg.lstsq(_X_p3, _log_s - _log_rhs, rcond=None)[0]
                    _pred = (1-_w_bl)*(_X_v5@_b_v5) + _w_bl*(_X_p3@_b_p3) + _log_rhs
                    _ss_res = np.sum((_log_s - _pred)**2)
                    _ss_tot = np.sum((_log_s - np.mean(_log_s))**2)
                    _r2 = 1 - _ss_res / _ss_tot
                    desc = desc.replace("{formx_r2}", f"{_r2:.3f}")
                    desc = desc.replace("{formx_loocv}", f"~{_r2:.3f}")
                else:
                    desc = desc.replace("{formx_r2}", "N/A")
                    desc = desc.replace("{formx_loocv}", "N/A")
            except:
                desc = desc.replace("{formx_r2}", "N/A")
                desc = desc.replace("{formx_loocv}", "N/A")
        info_entry = {
            "file": entry["file"],
            "csv": csv_file,
            "title": entry["title"],
            "description": desc,
            "origin_tip": entry["origin_tip"],
        }
        # Add R_gb values to plot_info for downstream use
        if plot_name == 'rgb_fitting':
            r_gb, ln_k, _, _ = _fit_r_gb(all_data, plot_names, use_global=False)
            info_entry['b'] = round(r_gb, 4)
            info_entry['ln_k'] = round(ln_k, 4)
        if plot_name == 'ionic_scaling_fit' and _GLOBAL_C_ION is not None:
            info_entry['C_ion'] = round(_GLOBAL_C_ION, 6)
        plot_info[plot_name] = info_entry
        print(f"  [OK] {plot_name} -> {outpath}")
        # "1-1" focus view: register if the plot emitted a *_focus.png
        focus_file = f"{plot_name}_focus.png"
        if os.path.exists(os.path.join(args.output, focus_file)):
            plot_info[f"{plot_name}_focus"] = {
                "file": focus_file, "csv": None,
                "title": entry["title"] + " — 1-1 선택 샘플",
                "description": "항목1의 전체 fit(식·계수·1:1·±20% 동일)을 그대로 두고, "
                               "선택한 sample의 점만 표시. 재적합 없음.",
                "origin_tip": "동일 fit 위에 선택 케이스만 scatter.",
                "is_focus": True, "parent": plot_name,
            }
            print(f"  [OK] {plot_name}_focus -> {focus_file}")

    # Persist v29 + v32 fits to disk cache (keyed on args.names = case IDs,
    # which are unique — unlike the P:S-ratio label list passed into the
    # individual plot functions). Sibling subprocesses whose case list is a
    # subset of these IDs will pick up these params on startup.
    #
    # CRITICAL: only write when ionic_scaling_fit ran in this subprocess
    # (which implies Nelder-Mead on the FULL requested case set). Per-group
    # subprocesses would otherwise overwrite the parity cache with their
    # own narrow subset, so only the first group plot after parity would
    # hit — every subsequent group would miss because the cache would
    # contain just one group's IDs.
    wrote_parity = 'ionic_scaling_fit' in args.plots
    try:
        if (wrote_parity and _GLOBAL_IONIC_SIGMOID
                and _GLOBAL_IONIC_POLY3 and _GLOBAL_PS_SIGMOID):
            _write_v29_cache(args.names,
                             _GLOBAL_IONIC_SIGMOID,
                             _GLOBAL_IONIC_POLY3,
                             _GLOBAL_PS_SIGMOID,
                             _V32_FITTED_GAMMAS)
        elif not wrote_parity:
            print(f"  [v29 cache] skip write (ionic_scaling_fit not in "
                  f"this subprocess — preserves parity cache for siblings)")
    except Exception as _e:
        print(f"  [v29 cache] skipped: {_e}")

    info_path = os.path.join(args.output, "plot_info.json")
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(plot_info, f, indent=2, ensure_ascii=False)
    print(f"\nTotal: {len(plot_info)} plots")


if __name__ == "__main__":
    main()
