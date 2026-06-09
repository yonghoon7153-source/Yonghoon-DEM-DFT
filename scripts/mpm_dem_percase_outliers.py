#!/usr/bin/env python3
"""Per-case DEM ↔ champion-MPM porosity comparison + outliers (named).

For each webapp case, predict porosity from the validated champion composition
curve (scripts/mpm2d_composition.py, plastic & rigid SE) evaluated at the case's
own SE-fraction-of-solid, and flag cases OUTSIDE the [plastic, rigid] bracket:
  • DEM < plastic  → denser than the single-size plastic MPM = a packing/Furnas
    well-packed corner (the size diversity the champion slice can't span).
  • DEM > rigid    → more porous than the rigid bound = under-compacted /
    anomalous (often the broken-sim or extreme-AM_P cases).

No MPM run needed — uses the baked champion curve.  Reads webapp full_metrics
for names + phi_am/phi_se/P:S/porosity.

Run:  python3 scripts/mpm_dem_percase_outliers.py [--results webapp/results] [--plot]
Out:  prints the ranked outlier table; --plot → docs/figures/mpm_dem_percase_parity.png
"""
import argparse
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RHO_AM, RHO_SE = 4.8, 2.0
CHAMP_AM = list(range(0, 101, 10))
CHAMP_PLASTIC = [6.5, 7.2, 8.2, 8.9, 10.0, 11.2, 11.4, 13.5, 16.4, 20.2, 28.2]
CHAMP_RIGID = [8.1, 9.1, 11.5, 12.7, 15.4, 17.0, 17.5, 18.4, 21.2, 24.0, 28.7]


def champ_se_of_solid(am_wt):
    w = am_wt / 100.0
    if w <= 0: return 100.0
    if w >= 1: return 0.0
    a = w / RHO_AM; b = (1 - w) / RHO_SE
    return 100.0 * (1 - a / (a + b))


def ps_ratio(d):
    v = d.get('ps_ratio') or (d.get('meta') or {}).get('ps_ratio')
    if v and ':' in str(v):
        try:
            p, s = (float(z) for z in str(v).split(':')); return p, s
        except Exception:
            pass
    fp = d.get('ps_frac_AM_P')
    if fp is None:
        fp = (d.get('meta') or {}).get('ps_frac_AM_P')
    if fp is not None:
        return fp * 10, 10 - fp * 10
    return 7, 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default=os.path.join(HERE, '..', 'webapp', 'results'))
    ap.add_argument('--plot', action='store_true')
    a = ap.parse_args()

    cx = np.array([champ_se_of_solid(am) for am in CHAMP_AM])
    o = np.argsort(cx); cx = cx[o]
    cp = np.array(CHAMP_PLASTIC)[o]; cr = np.array(CHAMP_RIGID)[o]

    rows = []
    for f in glob.glob(os.path.join(a.results, '*', 'full_metrics.json')):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        pa = d.get('phi_am'); ps = d.get('phi_se'); po = d.get('porosity')
        if None in (pa, ps, po) or pa + ps <= 0:
            continue
        nm = (d.get('meta') or {}).get('name') or d.get('name') or os.path.basename(os.path.dirname(f))
        p, s = ps_ratio(d); tot = p + s
        amp = pa * p / tot * 100; ams = pa * s / tot * 100; se = ps * 100
        se_solid = 100.0 * se / (amp + ams + se)
        pp = float(np.interp(se_solid, cx, cp)); pr = float(np.interp(se_solid, cx, cr))
        lo, hi = min(pp, pr), max(pp, pr)
        resid = (po - lo) if po < lo else ((po - hi) if po > hi else 0.0)
        rows.append((resid, nm, po, pp, pr, se_solid, amp, ams, se))

    rows.sort(key=lambda r: r[0])
    n = len(rows); inb = sum(1 for r in rows if r[0] == 0)
    if n == 0:
        print(f"No cases found under {a.results} (full_metrics.json with "
              f"phi_am/phi_se/porosity).\nRun this on the machine that has "
              f"webapp/results/ (the WSL box), or pass --results <path>.")
        return
    print(f"per-case DEM vs champion [plastic,rigid] band — n={n}, "
          f"in band {inb} ({100*inb/max(n,1):.0f}%)\n")
    hdr = f"  {'resid':>6s} {'DEM':>5s} {'plas':>5s} {'rig':>5s} {'SE/sol':>6s}  {'AMP/AMS/SE':>11s}  case"
    print("== DENSER than plastic (packing/Furnas well-packed) — top 12 ==")
    print(hdr)
    for r in rows[:12]:
        print(f"  {r[0]:6.1f} {r[2]:5.1f} {r[3]:5.1f} {r[4]:5.1f} {r[5]:6.0f}  "
              f"{r[6]:3.0f}/{r[7]:3.0f}/{r[8]:3.0f}  {r[1]}")
    print("\n== MORE POROUS than rigid (under-compacted / anomaly) — top 12 ==")
    print(hdr)
    for r in [x for x in rows[::-1] if x[0] > 0][:12]:
        print(f"  {r[0]:6.1f} {r[2]:5.1f} {r[3]:5.1f} {r[4]:5.1f} {r[5]:6.0f}  "
              f"{r[6]:3.0f}/{r[7]:3.0f}/{r[8]:3.0f}  {r[1]}")

    if a.plot:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        po = np.array([r[2] for r in rows]); pp = np.array([r[3] for r in rows])
        resid = np.array([r[0] for r in rows])
        fig, ax = plt.subplots(figsize=(6.4, 6.0))
        lo = min(po.min(), pp.min()) - 2; hi = max(po.max(), pp.max()) + 2
        ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1 (DEM = plastic-MPM)')
        c = np.where(resid == 0, '#2453b8', np.where(resid < 0, '#2e8b57', '#c0392b'))
        ax.scatter(pp, po, s=22, c=c, alpha=0.8)
        ax.set_xlabel('champion plastic-MPM predicted porosity (%)')
        ax.set_ylabel('DEM porosity (%)')
        ax.set_title('Per-case DEM vs champion plastic MPM\n'
                     'blue=in band · green=denser (Furnas) · red=more porous (anomaly)',
                     fontsize=10)
        ax.set_aspect('equal'); ax.grid(alpha=0.3); ax.legend(fontsize=8)
        out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_percase_parity.png')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        plt.tight_layout(); plt.savefig(out, dpi=140); print(f"\nsaved {out}")


if __name__ == '__main__':
    main()
