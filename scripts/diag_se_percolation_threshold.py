#!/usr/bin/env python3
"""SE stress-bearing percolation threshold — direct measurement.

Reviewer-driven check: does our literature-imported f_perc = 0.65
(Liu & Yin 2025) actually correspond to the percolation breakdown of
the *stress-bearing* SE backbone in our DEM data?

Reviewer notes that drove the algorithm:

  1. Definition ambiguity — Liu & Yin's 0.65 comes from a continuum
     FEM stress analysis; we operate on a discrete DEM contact
     network.  To avoid silently mapping different quantities, we
     compute the stress-bearing fraction under TWO definitions and
     report both:
        (a) SE-SE only — Radjai 1996 strong-network convention:
            keep contacts with |F_n| > mean(|F_n|), then test
            top↔bottom connectivity of SE particles through those
            strong SE-SE contacts.
        (b) SE-SE + AM-SE bridging — same strong filter but treat
            AM-SE contacts as "transit" edges that let an SE
            cluster span through an AM neighbour.  Captures the
            cases where the SE backbone winds around AM particles.

  2. Threshold finding in finite systems gives sigmoid, not step.
     We don't fit critical exponents.  Operational threshold:
       AM_wt% where stress_bearing_fraction first drops below 0.5.
     Defined explicitly so the operational meaning is unambiguous.

  3. Unit consistency for f_perc = 0.65 — Liu & Yin's quantity is
     a composition (SE volume fraction at percolation threshold),
     ours is a ratio (stress-bearing SE / total SE).  We plot both
     on twin y-axes so the "AM_wt% = X* → ratio crosses 0.5 → SE
     volume fraction at X* is Y" statement is unambiguous.

Outputs:
  docs/figures/se_percolation_threshold.png  — twin-axis figure
  docs/db/se_percolation_results.csv          — per-case raw table

Usage:
  python3 scripts/diag_se_percolation_threshold.py
  python3 scripts/diag_se_percolation_threshold.py --campaign 후막
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT    = Path(__file__).resolve().parent.parent
WEBAPP  = ROOT / 'webapp'
DOCSDB  = ROOT / 'docs' / 'db'
FIGDIR  = ROOT / 'docs' / 'figures'

# Reviewer-suggested operational threshold for the f_perc comparison
OP_THRESHOLD = 0.5

# Density ratio for converting AM:SE volume fraction → weight fraction
# (matches scripts/predict_porosity_strict_physics convention).
RHO_AM, RHO_SE = 4800.0, 2000.0


def _discover_cases() -> list[Path]:
    """Walk webapp/archive/ + webapp/results/ for case dirs that have
    atoms.csv + contacts.csv + meta.json or input_params.json."""
    seen, out = set(), []
    for base in ('archive', 'results'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if ((d / 'contacts.csv').exists() and
                    ((d / 'meta.json').exists() or
                     (d / 'input_params.json').exists())):
                if d not in seen:
                    seen.add(d)
                    out.append(d)
    return sorted(out)


def _load_atoms(case_dir: Path) -> tuple[dict, dict, float]:
    """Returns (atoms_by_id, type_map, scale)."""
    meta: dict = {}
    for fname in ('meta.json', 'input_params.json'):
        p = case_dir / fname
        if p.exists():
            try:
                meta = json.loads(p.read_text())
                break
            except Exception:
                pass
    scale = float(meta.get('scale', 1000.0))
    type_map = {}
    for tok in str(meta.get('type_map', '')).split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                type_map[int(k.strip())] = v.strip()
            except Exception:
                pass
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

    atoms = {}
    for r in csv.DictReader((case_dir / 'atoms.csv').open()):
        aid = int(r['id'])
        atoms[aid] = dict(
            id=aid,
            type=type_map.get(int(r.get('type', 0)), '?'),
            x=float(r.get('x', 0)), y=float(r.get('y', 0)),
            z=float(r.get('z', 0)),
            r=float(r.get('radius') or r.get('r') or 0),
        )
    return atoms, type_map, scale


def _load_contacts(case_dir: Path) -> list[tuple[int, int, float, float]]:
    """Returns list of (id1, id2, |F_n|, contact_area)."""
    out = []
    p = case_dir / 'contacts.csv'
    if not p.exists():
        return out
    for r in csv.DictReader(p.open()):
        try:
            i1 = int(r['id1']); i2 = int(r['id2'])
        except Exception:
            continue
        try:
            fn = float(r.get('fn') or 0)
            if not fn:
                fn = math.sqrt(float(r.get('fn_x') or 0) ** 2 +
                               float(r.get('fn_y') or 0) ** 2 +
                               float(r.get('fn_z') or 0) ** 2)
            area = float(r.get('contact_area') or 0)
        except Exception:
            continue
        if fn > 0:
            out.append((i1, i2, fn, area))
    return out


class _UnionFind:
    def __init__(self):
        self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def _stress_bearing_fraction(atoms: dict, contacts: list,
                              bridge_through_AM: bool,
                              z_top: float, z_bot: float
                              ) -> tuple[float, int, int]:
    """Returns (fraction, n_total_SE, n_spanning_SE_volume_units).

    Implements Radjai 1996 strong-network filter (|F_n| > mean) and
    then tests top↔bottom connectivity of SE particles through the
    strong sub-network.  When bridge_through_AM=True, strong AM-SE
    contacts are also included as edges so an SE cluster can span
    through AM particles.

    The "stress-bearing fraction" is reported by VOLUME of SE
    particles in the spanning component(s) divided by total SE
    volume — matches the way Liu & Yin 2025 frame the composition
    metric, while the underlying network test follows Radjai 1996
    discrete-contact convention.
    """
    se_ids = {aid for aid, a in atoms.items() if a.get('type') == 'SE'}
    n_total_se = len(se_ids)
    if not n_total_se or not contacts:
        return 0.0, 0, 0

    # Per-pair-type Radjai strong filter — Liu & Yin's 2-phase
    # threshold is about SE phase stress transmission, so we use
    # the mean |F_n| of contacts that involve at least one SE
    # particle as the cutoff (rather than the global mean which
    # would be dominated by AM-AM contacts at high AM_wt%).
    se_involved_fn = [fn for (i1, i2, fn, _) in contacts
                       if (atoms.get(i1, {}).get('type') == 'SE' or
                           atoms.get(i2, {}).get('type') == 'SE')]
    if not se_involved_fn:
        return 0.0, n_total_se, 0
    f_mean = float(np.mean(se_involved_fn))

    uf = _UnionFind()
    for (i1, i2, fn, _) in contacts:
        if fn <= f_mean:           # Radjai strong filter
            continue
        a1 = atoms.get(i1); a2 = atoms.get(i2)
        if a1 is None or a2 is None:
            continue
        t1, t2 = a1.get('type'), a2.get('type')
        is_se_se = (t1 == 'SE' and t2 == 'SE')
        is_am_se = ((t1 == 'SE' and 'AM' in (t2 or '')) or
                    ('AM' in (t1 or '') and t2 == 'SE'))
        if is_se_se or (bridge_through_AM and is_am_se):
            uf.union(i1, i2)

    # For each SE particle, classify its component as containing top,
    # bottom, both or neither.
    # We tag with the SE id of any "top" SE and any "bottom" SE in the
    # component; if both tags are present the component spans.
    top_root = {}
    bot_root = {}
    for aid in se_ids:
        z = atoms[aid]['z']
        root = uf.find(aid) if aid in uf.p else aid
        if z >= z_top:
            top_root[root] = True
        if z <= z_bot:
            bot_root[root] = True

    # Volume of SE particles whose component spans top↔bottom
    def _vol_se(aid):
        r = atoms[aid].get('r') or 0
        return (4.0/3.0) * math.pi * (r ** 3)
    total_vol = sum(_vol_se(aid) for aid in se_ids)
    if total_vol <= 0:
        return 0.0, n_total_se, 0
    span_vol = 0.0
    span_n   = 0
    for aid in se_ids:
        root = uf.find(aid) if aid in uf.p else aid
        if top_root.get(root) and bot_root.get(root):
            span_vol += _vol_se(aid)
            span_n   += 1
    return span_vol / total_vol, n_total_se, span_n


def _case_stats(case_dir: Path) -> dict | None:
    try:
        atoms, type_map, scale = _load_atoms(case_dir)
    except Exception:
        return None
    contacts = _load_contacts(case_dir)
    if not atoms or not contacts:
        return None

    # AM weight fraction (definitions identical to the porosity model)
    am_vol = sum((4.0/3.0)*math.pi*(a['r']**3)
                 for a in atoms.values() if 'AM' in (a.get('type') or ''))
    se_vol = sum((4.0/3.0)*math.pi*(a['r']**3)
                 for a in atoms.values() if a.get('type') == 'SE')
    if (am_vol + se_vol) <= 0:
        return None
    am_mass = am_vol * RHO_AM
    se_mass = se_vol * RHO_SE
    am_wt = 100.0 * am_mass / (am_mass + se_mass)
    se_vol_frac = se_vol / (am_vol + se_vol)

    # Top / bottom strip thickness — use the SE particle radius as
    # the natural margin so a single SE near the boundary counts.
    se_rs = [a['r'] for a in atoms.values() if a.get('type') == 'SE']
    margin = float(np.median(se_rs)) if se_rs else 0.0
    z_vals = [a['z'] for a in atoms.values() if a.get('type') == 'SE']
    if not z_vals:
        return None
    z_top = max(z_vals) - margin
    z_bot = min(z_vals) + margin

    frac_a, n_se, span_a = _stress_bearing_fraction(
        atoms, contacts, bridge_through_AM=False,
        z_top=z_top, z_bot=z_bot)
    frac_b, _,    span_b = _stress_bearing_fraction(
        atoms, contacts, bridge_through_AM=True,
        z_top=z_top, z_bot=z_bot)
    return dict(case_id=case_dir.name,
                am_wt=am_wt, se_vol_frac=se_vol_frac,
                n_se=n_se,
                frac_se_only=frac_a, span_n_se_only=span_a,
                frac_with_bridge=frac_b, span_n_with_bridge=span_b)


def _operational_threshold(am_wts, fracs, target=OP_THRESHOLD):
    """Find AM_wt% where `fracs` first drops below `target`, by
    monotonically-binned linear interpolation on the sorted-by-AM
    sequence."""
    pts = sorted(zip(am_wts, fracs))
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if y0 >= target and y1 < target:
            u = (target - y0) / (y1 - y0) if (y1 != y0) else 0
            return x0 + u * (x1 - x0)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--campaign', default=None,
                     help='Substring filter on case dir name (eg. 후막 박막 particulate)')
    args = ap.parse_args()

    cases = _discover_cases()
    if args.campaign:
        cases = [c for c in cases if args.campaign in str(c)]
    if not cases:
        print('No cases found.', flush=True); sys.exit(1)
    print(f'Processing {len(cases)} cases…', flush=True)

    rows = []
    for d in cases:
        s = _case_stats(d)
        if s: rows.append(s)
        tag = '·' if s else '✗'
        if not s:
            print(f'  {tag} {d.name} — skipped')
    if not rows:
        print('No usable cases.', flush=True); sys.exit(1)
    print(f'Done — {len(rows)} cases analysed.', flush=True)

    DOCSDB.mkdir(parents=True, exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    csv_p = DOCSDB / 'se_percolation_results.csv'
    with csv_p.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'case_id', 'am_wt', 'se_vol_frac', 'n_se',
            'frac_se_only', 'span_n_se_only',
            'frac_with_bridge', 'span_n_with_bridge'])
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f'  ✓ {csv_p}')

    # ── Plot ────────────────────────────────────────────────────
    am_wts   = np.array([r['am_wt']            for r in rows])
    fr_only  = np.array([r['frac_se_only']     for r in rows])
    fr_brdg  = np.array([r['frac_with_bridge'] for r in rows])
    se_vf    = np.array([r['se_vol_frac']      for r in rows])

    fig, ax1 = plt.subplots(figsize=(10, 6.5))
    ax2 = ax1.twinx()

    # Left axis — stress-bearing ratios (the directly measured quantity)
    ax1.scatter(am_wts, fr_only, s=42, alpha=0.75,
                 facecolor='#1f77b4', edgecolor='black', linewidth=0.4,
                 label='SE-SE only (Radjai strong)')
    ax1.scatter(am_wts, fr_brdg, s=42, alpha=0.75,
                 facecolor='#d62728', edgecolor='black', linewidth=0.4,
                 marker='D',
                 label='SE-SE + AM-SE bridge')
    # Right axis — SE volume fraction (the composition quantity used
    # by Liu & Yin's continuum-FEM literature value)
    ax2.scatter(am_wts, se_vf, s=22, alpha=0.6,
                 facecolor='none', edgecolor='#888',
                 marker='x', label='SE vol fraction (composition)')

    ax1.axhline(OP_THRESHOLD, color='#555', ls='--', lw=0.8,
                 label=f'operational threshold = {OP_THRESHOLD}')
    ax2.axhline(0.65, color='purple', ls=':', lw=0.9,
                 label='Liu & Yin 2025 f_perc = 0.65')

    # Operational threshold markers — AM_wt% where the SE-only ratio
    # crosses 0.5
    am_star_only = _operational_threshold(am_wts, fr_only)
    am_star_brdg = _operational_threshold(am_wts, fr_brdg)
    if am_star_only is not None:
        # SE vol fraction at that AM_wt%
        idx = np.argsort(am_wts)
        se_at_star = float(np.interp(am_star_only, am_wts[idx], se_vf[idx]))
        ax1.axvline(am_star_only, color='#1f77b4', ls=':', lw=1)
        ax1.text(am_star_only + 0.4, 0.85,
                  f'AM_wt* = {am_star_only:.1f}%\n'
                  f'SE vol_frac at AM_wt* = {se_at_star:.2f}',
                  fontsize=9, color='#1f77b4')

    ax1.set_xlabel('AM weight fraction (%)', fontsize=11)
    ax1.set_ylabel('Stress-bearing SE / total SE (volume ratio)',
                    fontsize=11, color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax2.set_ylabel('SE volume fraction (composition)',
                    fontsize=11, color='#666')
    ax2.tick_params(axis='y', labelcolor='#666')
    ax1.set_ylim(-0.05, 1.05); ax2.set_ylim(0, 1)
    ax1.grid(alpha=0.3)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=9, loc='lower left',
                 framealpha=0.95)

    ax1.set_title('SE stress-bearing percolation — direct measurement vs Liu & Yin 2025 f_perc',
                    fontsize=12, fontweight='bold')
    plt.tight_layout()
    out = FIGDIR / 'se_percolation_threshold.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    print(f'  ✓ {out}')

    # Console summary
    print('\n── Operational threshold (stress-bearing ratio drops below '
          f'{OP_THRESHOLD}) ──')
    if am_star_only is not None:
        idx = np.argsort(am_wts)
        se_at_star = float(np.interp(am_star_only, am_wts[idx], se_vf[idx]))
        print(f'  (a) SE-SE only         : AM_wt* = {am_star_only:.1f} %  '
              f'(SE vol_frac there = {se_at_star:.3f})')
    else:
        print('  (a) SE-SE only         : threshold not crossed in this sample')
    if am_star_brdg is not None:
        idx = np.argsort(am_wts)
        se_at_star_b = float(np.interp(am_star_brdg, am_wts[idx], se_vf[idx]))
        print(f'  (b) SE-SE + AM-SE bridge: AM_wt* = {am_star_brdg:.1f} %  '
              f'(SE vol_frac there = {se_at_star_b:.3f})')
    else:
        print('  (b) SE-SE + AM-SE bridge: threshold not crossed in this sample')
    print(f'\nCompare with Liu & Yin 2025 f_perc = 0.65 (SE volume fraction).')


if __name__ == '__main__':
    main()
