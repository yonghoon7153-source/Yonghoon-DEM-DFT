#!/usr/bin/env python3
"""Plot the 2D MPM porosity surface + the per-case 3D (DEM vs MPM scaffold) collection.

  3D cases : docs/data/case_3d_collection.csv  (built by parse_case_paste.py from button pastes)
  2D sweep : docs/data/mpm2d_ps_am_porosity.csv (optional, from mpm_dem_match --ps-am-grid)

Panels:
  (1) DEM vs MPM-3D porosity parity  — the frame[4] cross-validation (y=x, ±1.5 %p band)
  (2) porosity vs AM wt%             — DEM ● and MPM-3D ■ per case (coloured by P:S);
                                       2D-MPM trend line overlaid per matching P:S (if --2d given)

  python3 scripts/plot_2d_3d_porosity.py [--3d <csv>] [--2d <csv>] [--out <png>]
"""
import argparse
import csv
import os


def _read(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    for r in csv.DictReader(open(path)):
        if r.get('case', '').startswith('#') or (r.get('p_frac', '') or '').startswith('#'):
            continue
        out.append(r)
    return out


def _f(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--3d', dest='d3', default='docs/data/case_3d_collection.csv')
    ap.add_argument('--2d', dest='d2', default='docs/data/mpm2d_ps_am_porosity.csv')
    ap.add_argument('--out', default='docs/figures/porosity_2d_3d.png')
    a = ap.parse_args()

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    cases = _read(a.d3)
    if not cases:
        raise SystemExit(f'no 3D cases in {a.d3} — paste cases through parse_case_paste.py first')
    two = _read(a.d2)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(19, 5.2))

    # ── panel 1: DEM vs MPM-3D parity ──────────────────────────────────────────
    dem = np.array([_f(r, 'dem_porosity_pct') for r in cases], float)
    mpm = np.array([_f(r, 'mpm_porosity_pct') for r in cases], float)
    ok = ~(np.isnan(dem) | np.isnan(mpm))
    dem, mpm = dem[ok], mpm[ok]
    names = [r['case'].replace('input_', '') for r, k in zip(cases, ok) if k]
    lo = min(dem.min(), mpm.min()) - 2 if len(dem) else 0
    hi = max(dem.max(), mpm.max()) + 2 if len(dem) else 40
    ax1.plot([lo, hi], [lo, hi], 'k--', lw=1, label='y = x (DEM = MPM)')
    ax1.fill_between([lo, hi], [lo - 1.5, hi - 1.5], [lo + 1.5, hi + 1.5], color='0.85', alpha=0.6,
                     label='±1.5 %p (model-trust)')
    ax1.scatter(dem, mpm, s=55, c='#c0392b', zorder=3)
    for x, y, n in zip(dem, mpm, names):
        ax1.annotate(n, (x, y), fontsize=7, xytext=(4, 3), textcoords='offset points')
    if len(dem) >= 2:
        d = mpm - dem
        ax1.set_title(f'DEM vs MPM-3D porosity  (Δ̄={d.mean():+.2f} %p, |Δ|max={np.abs(d).max():.2f})')
    ax1.set_xlabel('DEM porosity (%)'); ax1.set_ylabel('MPM-3D scaffold porosity (%)')
    ax1.set_xlim(lo, hi); ax1.set_ylim(lo, hi); ax1.legend(fontsize=8); ax1.set_aspect('equal')

    # ── panel 2: porosity vs AM wt%, grouped by P:S ────────────────────────────
    pfracs = sorted({r['ps_label'] for r in cases if r.get('ps_label')})
    cmap = plt.cm.viridis
    for i, ps in enumerate(pfracs):
        col = cmap(i / max(len(pfracs) - 1, 1))
        sub = [r for r in cases if r.get('ps_label') == ps]
        am = np.array([_f(r, 'am_wt') for r in sub], float)
        order = np.argsort(am)
        am = am[order]
        dd = np.array([_f(r, 'dem_porosity_pct') for r in sub], float)[order]
        mm = np.array([_f(r, 'mpm_porosity_pct') for r in sub], float)[order]
        ax2.plot(am, dd, 'o-', color=col, label=f'DEM  P:S {ps}')
        ax2.plot(am, mm, 's--', color=col, mfc='none', label=f'MPM-3D  P:S {ps}')
        # 2D-MPM trend at this p_frac
        if two:
            pf = sub[0].get('p_frac')
            t = [(float(r['am_wt']), float(r['porosity_pct'])) for r in two
                 if r.get('p_frac') == pf and _f(r, 'porosity_pct') is not None]
            if len(t) >= 2:
                t.sort()
                ax2.plot([x for x, _ in t], [y for _, y in t], ':', color=col, alpha=0.6,
                         lw=2, label=f'2D-MPM  P:S {ps}')
    ax2.set_xlabel('AM wt%'); ax2.set_ylabel('porosity (%)')
    ax2.set_title(f'porosity vs composition  ({len(cases)} 3D cases)')
    ax2.legend(fontsize=7, ncol=1); ax2.grid(alpha=0.3)

    # ── panel 3: porosity vs P:S (Furnas dip), grouped by (mAh, AM wt%) ─────────
    groups = sorted({(r.get('mAh', ''), r.get('am_wt', '')) for r in cases})
    cmap3 = plt.cm.plasma
    for i, (mah, am) in enumerate(groups):
        sub = [r for r in cases if r.get('mAh') == mah and r.get('am_wt') == am]
        if len(sub) < 2:
            continue                                    # need ≥2 P:S to show a dip
        col = cmap3(i / max(len(groups) - 1, 1))
        p = np.array([_f(r, 'p_frac') for r in sub], float)
        order = np.argsort(p)
        p = p[order]
        dd = np.array([_f(r, 'dem_porosity_pct') for r in sub], float)[order]
        mm = np.array([_f(r, 'mpm_porosity_pct') for r in sub], float)[order]
        lab = f'{mah}mAh AM{am}'
        ax3.plot(p, dd, 'o-', color=col, label=f'DEM  {lab}')
        ax3.plot(p, mm, 's--', color=col, mfc='none', label=f'MPM-3D  {lab}')
        # mark the minimum (Furnas-optimal P:S)
        j = int(np.argmin(mm))
        ax3.annotate(f'dip\nP:S {sub[order[j]]["ps_label"]}', (p[j], mm[j]),
                     fontsize=7, ha='center', xytext=(0, -22), textcoords='offset points',
                     color=col, arrowprops=dict(arrowstyle='->', color=col, lw=0.8))
    ax3.set_xlabel('AM_P fraction  (P:S → 10:0 = 1.0)'); ax3.set_ylabel('porosity (%)')
    ax3.set_title('porosity vs P:S  (Furnas dip)')
    ax3.legend(fontsize=7); ax3.grid(alpha=0.3)

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    fig.tight_layout(); fig.savefig(a.out, dpi=130)
    print(f'saved {a.out}  ({len(cases)} 3D cases, 2D={"yes" if two else "no"})')


if __name__ == '__main__':
    main()
