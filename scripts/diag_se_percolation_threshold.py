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
                              z_top: float, z_bot: float,
                              cutoff_mode: str = 'system',
                              ) -> tuple[float, int, int]:
    """Returns (fraction, n_total_SE, n_spanning_SE_volume_units).

    Implements Radjai 1996 strong-network filter (|F_n| > mean) and
    then tests top↔bottom connectivity of SE particles through the
    strong sub-network.  When bridge_through_AM=True, strong AM-SE
    contacts are also included as edges so an SE cluster can span
    through AM particles.

    cutoff_mode:
      'system'        — Radjai 1996 original: mean of ALL contact
                        |F_n|.  Reviewer-preferred default because
                        it doesn't go circular at high AM_wt%
                        (where SE contacts become rare and their
                        own mean would drop, artificially keeping
                        the strong-network ratio inflated).
      'se_involving' — mean of only SE-involving contacts.  Kept
                        as a robustness alternative; the AM-AM
                        force tail can dominate the system mean
                        at extreme AM_wt% so this asks "are SE
                        contacts strong relative to other SE
                        contacts".

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

    if cutoff_mode == 'system':
        # Radjai 1996 original — mean of ALL contact normal forces.
        all_fn = [fn for (_, _, fn, _) in contacts]
        if not all_fn:
            return 0.0, n_total_se, 0
        f_mean = float(np.mean(all_fn))
    else:
        # SE-involving subset — alternative robustness check.
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

    # ── AM weight fraction ────────────────────────────────────────
    am_vol = sum((4.0/3.0)*math.pi*(a['r']**3)
                 for a in atoms.values() if 'AM' in (a.get('type') or ''))
    se_vol = sum((4.0/3.0)*math.pi*(a['r']**3)
                 for a in atoms.values() if a.get('type') == 'SE')
    if (am_vol + se_vol) <= 0:
        return None
    am_mass = am_vol * RHO_AM
    se_mass = se_vol * RHO_SE
    am_wt = 100.0 * am_mass / (am_mass + se_mass)

    # ── Three SE volume-fraction definitions ─────────────────────
    # (i)  V_SE / V_total_particles  — solid-only fraction (Bouvard /
    #      Liu & Yin's likely "SE phase fraction" convention)
    # (ii) V_SE / V_RVE              — bulk fraction including pore
    #      space.  Common in compaction literature and FEM continuum
    #      stress maps.
    # (iii) V_SE / (V_SE + V_AM)     — mass→volume back-calc.
    #      Mathematically identical to (i) in DEM where particle
    #      volume is the only solid contribution; reported separately
    #      so reviewer can sanity-check the equivalence.
    se_vol_frac_solid = se_vol / (am_vol + se_vol)             # (i)
    # Try to read porosity from full_metrics.json or input_params.json
    # for definition (ii).  Fall back to NaN when unavailable so the
    # reviewer can tell which value is interpolated vs measured.
    porosity = None
    fm_path = case_dir / 'full_metrics.json'
    if fm_path.exists():
        try:
            fm = json.loads(fm_path.read_text())
            porosity = fm.get('porosity_pct')
            if porosity is not None:
                porosity = float(porosity) / 100.0
        except Exception:
            porosity = None
    se_vol_frac_rve = (se_vol_frac_solid * (1.0 - porosity)
                        if porosity is not None and 0 < porosity < 1
                        else float('nan'))                       # (ii)
    se_vol_frac_mass = se_mass / ((am_mass / RHO_AM + se_mass / RHO_SE) *
                                    ((RHO_AM + RHO_SE) / 2)) if False else \
                       se_vol / (am_vol + se_vol)                # (iii) = (i)

    # ── Top / bottom strip for spanning-cluster test ─────────────
    se_rs = [a['r'] for a in atoms.values() if a.get('type') == 'SE']
    margin = float(np.median(se_rs)) if se_rs else 0.0
    z_vals = [a['z'] for a in atoms.values() if a.get('type') == 'SE']
    if not z_vals:
        return None
    z_top = max(z_vals) - margin
    z_bot = min(z_vals) + margin

    # ── Four stress-bearing fractions: 2 cutoffs × 2 bridge modes ─
    measurements = {}
    n_se_seen = 0
    for cutoff in ('system', 'se_involving'):
        for bridge in (False, True):
            frac, n_se, _ = _stress_bearing_fraction(
                atoms, contacts,
                bridge_through_AM=bridge, z_top=z_top, z_bot=z_bot,
                cutoff_mode=cutoff)
            n_se_seen = n_se
            key = f'frac_{"bridge" if bridge else "se_only"}_{cutoff}'
            measurements[key] = frac

    return dict(case_id=case_dir.name,
                am_wt=am_wt,
                se_vol_frac_solid=se_vol_frac_solid,
                se_vol_frac_rve=se_vol_frac_rve,
                se_vol_frac_mass=se_vol_frac_mass,
                porosity=porosity,
                n_se=n_se_seen,
                **measurements)


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
        if not s:
            print(f'  ✗ {d.name} — skipped')
    if not rows:
        print('No usable cases.', flush=True); sys.exit(1)
    print(f'Done — {len(rows)} cases analysed.', flush=True)

    DOCSDB.mkdir(parents=True, exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    csv_p = DOCSDB / 'se_percolation_results.csv'
    with csv_p.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'case_id', 'am_wt',
            'se_vol_frac_solid', 'se_vol_frac_rve', 'se_vol_frac_mass',
            'porosity', 'n_se',
            'frac_se_only_system', 'frac_bridge_system',
            'frac_se_only_se_involving', 'frac_bridge_se_involving'])
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f'  ✓ {csv_p}')

    am_wts = np.array([r['am_wt'] for r in rows])
    vf_solid = np.array([r['se_vol_frac_solid'] for r in rows])
    vf_rve   = np.array([r['se_vol_frac_rve']   for r in rows])

    # ── Reviewer-driven sensitivity table ──────────────────────────
    # Two cutoff modes × two bridge modes × three thresholds.
    # Defaults: cutoff='system' (Radjai 1996 original — reviewer-
    # preferred to avoid circular logic at high AM_wt%), threshold
    # 0.5 (the operational anchor), bridge=False (main measurement —
    # bridging is reported as upper-bound sanity check).
    THRESHOLDS = [0.3, 0.5, 0.7]
    SERIES = [
        ('se_only', 'system',       'SE-SE only · system mean (main)'),
        ('bridge',  'system',       'SE-SE + bridge · system mean'),
        ('se_only', 'se_involving', 'SE-SE only · SE-involved mean'),
        ('bridge',  'se_involving', 'SE-SE + bridge · SE-involved mean'),
    ]

    def _series_data(bridge_or_only: str, cutoff: str):
        key = f'frac_{bridge_or_only}_{cutoff}'
        return np.array([r[key] for r in rows])

    # ── Sensitivity table ─────────────────────────────────────────
    print('\n── Operational AM_wt* sensitivity '
          f'(crossing thresholds {THRESHOLDS}) ──')
    print('  series                                 │ '
          ' '.join(f'τ={t}'.ljust(10) for t in THRESHOLDS))
    sens_table = {}
    for bridge_or_only, cutoff, label in SERIES:
        fracs = _series_data(bridge_or_only, cutoff)
        row_vals = []
        for t in THRESHOLDS:
            am_star = _operational_threshold(am_wts, fracs, target=t)
            row_vals.append(am_star)
        sens_table[(bridge_or_only, cutoff)] = row_vals
        cells = ['—' if v is None else f'{v:.1f}%' for v in row_vals]
        print(f'  {label:38s} │ ' + ' '.join(c.ljust(10) for c in cells))

    # ── Main figure ───────────────────────────────────────────────
    fig, ax1 = plt.subplots(figsize=(11, 6.8))
    ax2 = ax1.twinx()

    # Markers / colours per series
    style = {
        ('se_only', 'system'):       ('#1f77b4', 'o', 'SE-SE only · system mean'),
        ('bridge',  'system'):       ('#d62728', 'D', 'SE-SE + bridge · system mean'),
        ('se_only', 'se_involving'): ('#1f77b4', 'o', None),    # robustness
        ('bridge',  'se_involving'): ('#d62728', 'D', None),    # robustness
    }
    for bridge_or_only, cutoff, _ in SERIES:
        col, mk, label = style[(bridge_or_only, cutoff)]
        fracs = _series_data(bridge_or_only, cutoff)
        is_alt = (cutoff == 'se_involving')
        ax1.scatter(am_wts, fracs, s=44 if not is_alt else 22,
                    alpha=0.85 if not is_alt else 0.35,
                    facecolor=col if not is_alt else 'none',
                    edgecolor='black' if not is_alt else col,
                    marker=mk, linewidth=0.5 if not is_alt else 0.8,
                    label=label)

    # SE volume fraction (definition (i), solid-only — the most direct
    # match for Liu & Yin's "SE phase fraction").  Definition (ii) is
    # an alternative right axis but we keep one for legibility — both
    # values are in the CSV.
    ax2.scatter(am_wts, vf_solid, s=22, alpha=0.6,
                facecolor='none', edgecolor='#666',
                marker='x', label='SE vol fraction (def i: solid-only)')

    # Threshold lines + Liu & Yin anchor
    ax1.axhline(0.5, color='#555', ls='--', lw=0.9,
                label='operational threshold τ = 0.5')
    for tau in (0.3, 0.7):
        ax1.axhline(tau, color='#999', ls=':', lw=0.6)
    ax2.axhline(0.65, color='purple', ls=':', lw=1.0,
                label='Liu & Yin 2025 f_perc = 0.65')

    # Mark main-series AM_wt* at τ=0.5
    main_star = sens_table[('se_only', 'system')][1]
    if main_star is not None:
        idx = np.argsort(am_wts)
        se_at_star = float(np.interp(main_star, am_wts[idx], vf_solid[idx]))
        ax1.axvline(main_star, color='#1f77b4', ls=':', lw=1)
        ax1.text(main_star + 0.4, 0.88,
                  f'AM_wt* (main) = {main_star:.1f} %\n'
                  f'SE vol_frac (i) at AM_wt* = {se_at_star:.2f}',
                  fontsize=9, color='#1f77b4')

    ax1.set_xlabel('AM weight fraction (%)', fontsize=11)
    ax1.set_ylabel('Stress-bearing SE / total SE (volume ratio)',
                   fontsize=11, color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax2.set_ylabel('SE volume fraction (composition, def i)',
                   fontsize=11, color='#666')
    ax2.tick_params(axis='y', labelcolor='#666')
    ax1.set_ylim(-0.05, 1.05); ax2.set_ylim(0, 1)
    ax1.grid(alpha=0.3)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    leg = ax1.legend([h for h, l in zip(h1, l1) if l] +
                      [h for h, l in zip(h2, l2) if l],
                      [l for l in l1 if l] + [l for l in l2 if l],
                      fontsize=9, loc='lower left', framealpha=0.95)
    fig.text(0.5, -0.02,
              'Faded markers = SE-involved mean cutoff (robustness check, '
              'see Radjai 1996 vs SE-restricted alternative). '
              'Dotted horizontals at τ = 0.3, 0.7 show threshold-sensitivity '
              'envelope reported in console.',
              ha='center', va='top', fontsize=9, color='#666')

    ax1.set_title('SE stress-bearing percolation — direct measurement '
                  'vs Liu & Yin 2025 f_perc',
                  fontsize=12, fontweight='bold')
    plt.tight_layout()
    out = FIGDIR / 'se_percolation_threshold.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    print(f'  ✓ {out}')

    # ── Final console summary — three SE_vol_frac definitions at
    # the main-series AM_wt* so reviewer can pick the convention that
    # matches Liu & Yin's continuum-FEM definition ────────────────
    print('\n── Reviewer summary at main series (SE-SE only · system mean, τ = 0.5) ──')
    if main_star is None:
        print('  AM_wt* not crossed in this sample range — extend AM_wt% range.')
    else:
        idx = np.argsort(am_wts)
        se_solid = float(np.interp(main_star, am_wts[idx], vf_solid[idx]))
        # def (ii) only valid where porosity was available
        valid_rve = ~np.isnan(vf_rve)
        if valid_rve.sum() >= 2:
            sorted_idx_rve = np.argsort(am_wts[valid_rve])
            se_rve = float(np.interp(
                main_star,
                am_wts[valid_rve][sorted_idx_rve],
                vf_rve[valid_rve][sorted_idx_rve]))
        else:
            se_rve = float('nan')
        print(f'  AM_wt* (operational, τ = 0.5)   = {main_star:.2f} %')
        print(f'  SE_vol_frac at AM_wt*           — three definitions:')
        print(f'    (i)   V_SE / V_total_particles (solid-only)        = {se_solid:.3f}')
        print(f'    (ii)  V_SE / V_RVE (including porosity)            = '
              f'{("%.3f" % se_rve) if not np.isnan(se_rve) else "NaN (porosity missing)"}')
        print(f'    (iii) V_SE / (V_SE + V_AM) mass→volume back-calc   = {se_solid:.3f} (same as (i) in DEM)')
        print(f'  Liu & Yin 2025 f_perc           = 0.65 (convention: '
              f'most likely def (i) solid-only or (ii) RVE — confirm in their §)')
        print(f'  Δ vs literature: def (i)  = {se_solid - 0.65:+.3f}, '
              f'def (ii) = '
              f'{("%+.3f" % (se_rve - 0.65)) if not np.isnan(se_rve) else "NaN"}')


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
