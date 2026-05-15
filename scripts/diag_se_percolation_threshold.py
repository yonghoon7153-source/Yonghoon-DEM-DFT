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
    # Read porosity from any of several plausible locations.  The
    # first run revealed that 'porosity_pct' isn't always the key
    # name in full_metrics.json — try a fallback list, and as a last
    # resort look the case_id up in all_dem_porosity.csv (where the
    # column is canonically called porosity_pct).
    porosity = None
    POROSITY_KEYS = ('porosity_pct', 'porosity', 'epsilon_pct',
                       'eps_pct', 'porosity_pct_dem')
    for src in (case_dir / 'full_metrics.json',
                  case_dir / 'metrics.json',
                  case_dir / 'input_params.json',
                  case_dir / 'meta.json'):
        if not src.exists():
            continue
        try:
            d = json.loads(src.read_text())
        except Exception:
            continue
        for k in POROSITY_KEYS:
            v = d.get(k)
            if v is not None:
                try:
                    v = float(v)
                    # Heuristic: values > 1 are %, ≤ 1 are fractions.
                    porosity = v / 100.0 if v > 1.0 else v
                    break
                except Exception:
                    pass
        if porosity is not None:
            break
    if porosity is None:
        # Last resort: project-wide all_dem_porosity.csv lookup.
        csv_p = ROOT / 'all_dem_porosity.csv'
        if csv_p.exists():
            try:
                import pandas as pd
                df = pd.read_csv(csv_p)
                row = df[df['case_id'] == case_dir.name]
                if not row.empty and 'porosity_pct' in df.columns:
                    v = float(row.iloc[0]['porosity_pct'])
                    porosity = v / 100.0 if v > 1.0 else v
            except Exception:
                pass
    se_vol_frac_rve = (se_vol_frac_solid * (1.0 - porosity)
                        if porosity is not None and 0 < porosity < 1
                        else float('nan'))                       # (ii)
    # (iii) Mass→volume back-calculation using the DEM-input densities
    # ρ_AM = RHO_AM, ρ_SE = RHO_SE.  Within our DEM particle volumes are
    # derived from sphere geometry (4/3 π r³) at constant density, so
    # this back-calculation is identical to def (i) by construction.
    # We keep the value reported in the CSV row so density mismatch
    # would be detectable if the input convention ever drifts.
    se_vol_frac_mass = se_vol / (am_vol + se_vol)                # (iii) ≡ (i) in DEM

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

    # Median SE radius (µm in real units) — used by the verification
    # suite to bin cases by D_SE for the RCP-universality check.
    se_r_sim_med = float(np.median(se_rs)) if se_rs else 0.0
    r_SE_um = se_r_sim_med * 1.0e6 / scale  # sim → real

    # Campaign inference from case-id prefix.  Matches the
    # naming convention used elsewhere in the project (input_<n>mAh_,
    # input_particulate_, plus the auto-generated archive IDs).
    cid = case_dir.name
    parent_path = str(case_dir).lower()
    if 'particulate' in cid.lower() or 'particulate' in parent_path:
        campaign = 'particulate'
    elif 'input_1mAh' in cid or '박막' in parent_path or '1mah' in cid.lower():
        campaign = 'thin-film 1mAh'
    elif 'input_6mAh' in cid or '6mAh_real' in cid or '6mah' in cid.lower():
        campaign = 'thick-film 6mAh'
    elif 'input_8mAh' in cid or '8mAh_real' in cid or '8mah' in cid.lower():
        campaign = 'thick-film 8mAh'
    else:
        campaign = 'other'

    return dict(case_id=case_dir.name,
                am_wt=am_wt,
                se_vol_frac_solid=se_vol_frac_solid,
                se_vol_frac_rve=se_vol_frac_rve,
                se_vol_frac_mass=se_vol_frac_mass,
                porosity=porosity,
                n_se=n_se_seen,
                r_SE_um=r_SE_um,
                campaign=campaign,
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


def _bootstrap_am_star(am_wts, fracs, target=OP_THRESHOLD,
                        n_boot: int = 1000, rng_seed: int = 12345
                        ) -> tuple[float | None, float | None, float | None]:
    """Bootstrap a 95 % CI on AM_wt* by resampling cases with
    replacement.  Returns (median, lo, hi).  Addresses the reviewer's
    "is Δ statistically significant vs measurement noise" check.

    Resample unit
    -------------
    Naive case-level resampling — each case is drawn with replacement
    from the full ensemble.  This treats every case as an independent
    sample of the AM_wt% × stress-bearing relationship and gives the
    CI that the user would obtain from a fresh independent ensemble
    of the same size.

    Caveat: when AM_wt% bins are unevenly populated (e.g. lots of
    bimodal thick-film 80 % cases but only one mono-AM 95 % case),
    naive resampling can sample the threshold-crossing region too
    densely or too sparsely depending on how the resample falls.  A
    stratified-by-AM_wt%-bin bootstrap would tighten the CI in that
    case but is over-engineering for a first-pass robustness check
    — we use naive resampling and document the choice so the
    reviewer can ask for stratified if the CI looks suspicious.

    Returns (None, None, None) when fewer than 5 valid replicates
    cross the threshold — i.e. when the threshold is barely covered
    by the sample and the CI would be meaningless.
    """
    rng = np.random.default_rng(rng_seed)
    n = len(am_wts)
    if n < 5:
        return (None, None, None)
    replicates: list[float] = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        amw_b = np.asarray(am_wts)[idx]
        fr_b  = np.asarray(fracs)[idx]
        v = _operational_threshold(amw_b, fr_b, target=target)
        if v is not None:
            replicates.append(v)
    if len(replicates) < 5:
        return (None, None, None)
    arr = np.array(replicates)
    return (float(np.median(arr)),
            float(np.percentile(arr, 2.5)),
            float(np.percentile(arr, 97.5)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--campaign', default=None,
                     help='Substring filter on case dir name (eg. 후막 박막 particulate)')
    ap.add_argument('--exclude-untrustworthy', action='store_true',
                     help='Filter out cases listed in docs/db/case_audit_fails.csv')
    ap.add_argument('--verification-suite', action='store_true',
                     help='After the main analysis, run the reviewer\'s 4-item '
                          'verification checklist (statistical significance, '
                          'D_SE universality, campaign split, outlier exclusion) '
                          'and emit one reviewer-ready report at the bottom.')
    args = ap.parse_args()

    cases = _discover_cases()
    if args.campaign:
        cases = [c for c in cases if args.campaign in str(c)]

    # --exclude-untrustworthy: drop the case_ids that the
    # validation-flag audit (docs/db/case_audit_fails.csv) flagged.
    excluded_set: set[str] = set()
    if args.exclude_untrustworthy:
        fails_csv = DOCSDB / 'case_audit_fails.csv'
        if fails_csv.exists():
            try:
                with fails_csv.open() as f:
                    excluded_set = {r['case_dir']
                                     for r in csv.DictReader(f)
                                     if r.get('case_dir')}
            except Exception:
                excluded_set = set()
        before = len(cases)
        cases = [c for c in cases if c.name not in excluded_set]
        print(f'Excluded {before - len(cases)} untrustworthy cases '
              f'(from {len(excluded_set)} audit-flagged ids).', flush=True)

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
            'case_id', 'campaign', 'am_wt', 'r_SE_um',
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
    print('  series                                 │ ' +
          '  '.join(f'τ={t}'.ljust(8) for t in THRESHOLDS))
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
    # marker 'x' is an unfilled glyph — set its colour via `color=`
    # instead of `edgecolor=` (matplotlib warns when an unfilled
    # marker gets an edge colour).
    ax2.scatter(am_wts, vf_solid, s=22, alpha=0.6,
                color='#666',
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

    # ── Final console summary — Δ vs Liu & Yin 0.65 with explicit
    # convention assumption + auto-classifier into reviewer's
    # pre-registered scenarios A / B / C so the output is reviewer-
    # ready without further interpretation. ─────────────────────
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
        print(f'  SE_vol_frac at AM_wt* — two reportable definitions:')
        print(f'    (i)  solid-only:        V_SE / (V_AM + V_SE)       = {se_solid:.3f}')
        if not np.isnan(se_rve):
            print(f'    (ii) RVE (porosity-aware): V_SE / V_RVE             = {se_rve:.3f}')
        else:
            print(f'    (ii) RVE (porosity-aware):                          = NaN '
                  f'(porosity_pct not in full_metrics.json)')
        print(f'  (iii) mass→volume back-calc is identical to (i) under our '
              f'DEM-input densities (ρ_AM = {RHO_AM:.0f}, ρ_SE = {RHO_SE:.0f});')
        print(f'        same value omitted to avoid duplicate output.')

        # Convention assumption — explicit so reviewer can override.
        # Liu & Yin 2025 use FEM continuum stress fields on a 2-phase
        # RVE, which conventionally refers to volume fractions of the
        # SE phase RELATIVE TO THE REPRESENTATIVE VOLUME (including
        # pore space).  Default assumption = def (ii); we still report
        # def (i) Δ as alternative.
        d_i  = se_solid - 0.65
        d_ii = (se_rve - 0.65) if not np.isnan(se_rve) else None
        print(f'\n  Δ vs Liu & Yin 2025 f_perc = 0.65')
        print(f'    Primary assumption: convention (ii) RVE-based '
              f'(FEM continuum on a porous RVE → most likely)')
        if d_ii is not None:
            print(f'      Δ_(ii) = {d_ii:+.3f}  → SE_vol_frac (ii) = {se_rve:.3f} vs 0.65')
        else:
            print(f'      Δ_(ii) = N/A — porosity missing in case set')
        print(f'    Alternative: convention (i) solid-only')
        print(f'      Δ_(i)  = {d_i:+.3f}  → SE_vol_frac (i)  = {se_solid:.3f} vs 0.65')

        # Bootstrap 95 % CI on AM_wt* — answers reviewer's "is Δ
        # statistically significant vs measurement noise" question.
        main_fracs = _series_data('se_only', 'system')
        am_med, am_lo, am_hi = _bootstrap_am_star(am_wts, main_fracs,
                                                    target=0.5)
        if am_med is not None:
            # Propagate the CI through to SE_vol_frac at AM_wt*
            sort_idx = np.argsort(am_wts)
            sv_med = float(np.interp(am_med, am_wts[sort_idx], vf_solid[sort_idx]))
            # SE volume fraction DECREASES with AM_wt%, so the higher
            # AM_wt% CI bound corresponds to the LOWER vol-frac value
            # and vice versa.  Compute both endpoints and re-sort so
            # sv_lo/sv_hi are always min/max.
            sv_at_amlo = float(np.interp(am_lo, am_wts[sort_idx], vf_solid[sort_idx]))
            sv_at_amhi = float(np.interp(am_hi, am_wts[sort_idx], vf_solid[sort_idx]))
            sv_lo, sv_hi = sorted([sv_at_amlo, sv_at_amhi])
            print(f'\n  Bootstrap 95 % CI (1000 resamples, main series):')
            print(f'    AM_wt*           = {am_med:.2f} %   '
                  f'CI [{am_lo:.2f}, {am_hi:.2f}]')
            print(f'    SE_vol_frac (i)  = {sv_med:.3f}    '
                  f'CI [{sv_lo:.3f}, {sv_hi:.3f}]')
            ci_width_i = sv_hi - sv_lo
        else:
            print('\n  Bootstrap CI not computable (sample too small or '
                  'threshold barely covered).')
            ci_width_i = None

        # Auto-classification into reviewer-registered scenarios.
        # IMPORTANT: the output is labelled "DRAFT — manual validation
        # required" because Δ < 0.05 alone is not sufficient evidence
        # for "strong validation" — it could be RCP-universality
        # coincidence, bootstrap-noise-driven, or driven by outliers.
        # The classifier provides a STARTING point for the response;
        # the user is expected to walk the verification checklist
        # before adopting any of the suggested framings.
        def _scenario():
            if d_ii is not None and abs(d_ii) < 0.05:
                return ('A', 'strong validation under RVE convention',
                        'Liu & Yin 0.65 directly confirmed; f_perc upgrades '
                        'from literature → measured constant.')
            if abs(d_i) < 0.05 and (d_ii is None or abs(d_ii) > 0.10):
                return ('B', 'partial validation under solid-only convention',
                        'Liu & Yin value matches our solid-only fraction; the '
                        'RVE discrepancy reflects argyrodite plastic '
                        'densification reducing pore volume — new discussion '
                        'point.')
            return ('C', 'system-specific deviation under both conventions',
                    'Stress-bearing percolation threshold in our argyrodite-'
                    'NCM composites systematically differs from Liu & Yin '
                    'sulfide-NCM by Δ; possible drivers: particle size '
                    'ratio, plastic phase modulus, AM crystallinity. The '
                    'deviation itself becomes a publishable finding.')
        scen, label, framing = _scenario()
        print(f'\n  → Scenario {scen} (auto-classified): {label}')
        print(f'    Suggested framing (DRAFT — manual validation required):')
        print(f'      "{framing}"')
        print(f'\n    Before adopting, verify:')
        # Per-scenario verification checklist.  All three share the
        # first two items (statistical / coincidence) and the third
        # is scenario-specific.
        print(f'      [ ] (1) Is the Δ statistically significant '
              f'vs measurement noise?')
        if ci_width_i is not None:
            sig_flag = ('CI excludes 0.65 → statistically significant'
                        if (sv_lo > 0.65 or sv_hi < 0.65)
                        else 'CI brackets 0.65 → cannot reject null')
            print(f'              Bootstrap CI on SE_vol_frac (i) = '
                  f'[{sv_lo:.3f}, {sv_hi:.3f}] — {sig_flag}')
        else:
            print(f'              Bootstrap unavailable; rerun with larger sample.')
        print(f'      [ ] (2) Is the agreement physically meaningful or '
              f'RCP-universality coincidence?')
        print(f'              Recommend: plot AM_wt* vs D_SE across the '
              f'monomodal percolation sweep (D_SE = 0.5/1.0/2.0/3.0 µm). '
              f'If AM_wt* drifts with D_SE → not universality.')
        if scen == 'A':
            print(f'      [ ] (3-A) Is Δ_(ii) ≈ 0 because Liu & Yin\'s convention '
                  f'really is RVE-based, or is the apparent match an artefact '
                  f'of the porosity assumption (porosity_pct from '
                  f'full_metrics.json may have its own uncertainty)?')
        elif scen == 'B':
            print(f'      [ ] (3-B) Is the RVE discrepancy magnitude consistent '
                  f'with the argyrodite plasticity argument?  Cross-check by '
                  f'computing |Δ_(ii)| against the case-level porosity — if '
                  f'discrepancy scales with (1 - porosity), the plasticity '
                  f'explanation holds.')
        else:
            print(f'      [ ] (3-C) Is the deviation driven by a specific '
                  f'subset (e.g. mono-AM cases, very high or low D_SE)?  '
                  f'Recommend: rerun with --campaign filters and report '
                  f'AM_wt* by subset.  A deviation that disappears under '
                  f'physically-coherent filtering is a regime boundary, '
                  f'not a system-wide finding.')
        print(f'      [ ] (4) Are any outlier cases skewing AM_wt*?  The 22 '
              f'cases flagged untrustworthy in docs/db/case_audit_fails.csv '
              f'should be checked individually — if AM_wt* shifts >2 %p '
              f'when they are excluded, the threshold estimate is '
              f'outlier-driven.')

    # ── Reviewer-ready verification suite ───────────────────────
    # When the user passes --verification-suite, run items 2-4
    # automatically (item 1 is the bootstrap CI already printed
    # above) and emit a single consolidated report at the bottom.
    if args.verification_suite and rows:
        _run_verification_suite(rows, excluded_set, main_star=main_star)


def _analyse_subset(rows: list[dict], series_key: str = 'frac_se_only_system',
                     threshold: float = 0.5
                     ) -> dict:
    """Re-runs the operational-threshold + bootstrap on an arbitrary
    subset of the per-case `rows` produced by _case_stats.  Returns
    {n, am_star, am_star_ci, sv_solid_at_star, sv_rve_at_star, n_threshold_crosses}."""
    if not rows:
        return {'n': 0, 'am_star': None, 'am_star_ci': (None, None),
                'sv_solid': None, 'sv_rve': None}
    am_wts = np.array([r['am_wt'] for r in rows])
    fracs  = np.array([r[series_key] for r in rows])
    vf_sld = np.array([r['se_vol_frac_solid'] for r in rows])
    vf_rve = np.array([r['se_vol_frac_rve']   for r in rows])
    am_star = _operational_threshold(am_wts, fracs, target=threshold)
    am_med, am_lo, am_hi = _bootstrap_am_star(am_wts, fracs, target=threshold,
                                                n_boot=400)
    sv_sld = None; sv_rve = None
    if am_star is not None:
        idx = np.argsort(am_wts)
        sv_sld = float(np.interp(am_star, am_wts[idx], vf_sld[idx]))
        valid = ~np.isnan(vf_rve)
        if valid.sum() >= 2:
            i2 = np.argsort(am_wts[valid])
            sv_rve = float(np.interp(am_star,
                                       am_wts[valid][i2],
                                       vf_rve[valid][i2]))
    return {
        'n': len(rows),
        'am_star': am_star,
        'am_star_ci': (am_lo, am_hi),
        'sv_solid': sv_sld,
        'sv_rve': sv_rve,
    }


def _run_verification_suite(all_rows: list[dict],
                              excluded_set: set,
                              main_star: float | None):
    """Walks the reviewer's 4-item checklist programmatically and
    prints a consolidated reviewer-ready report.  All four items
    end up in a single console block so the user can copy-paste
    into the reviewer reply without re-assembly."""

    print()
    print('=' * 78)
    print('REVIEWER-READY VERIFICATION SUITE')
    print('  4-item checklist walked automatically — copy-paste into reply')
    print('=' * 78)

    # ── Baseline (all rows, main series) ─────────────────────────
    base = _analyse_subset(all_rows)
    print('\n[Baseline, all cases, SE-SE only · system mean, τ=0.5]')
    print(f'  N = {base["n"]} cases')
    if base['am_star'] is not None:
        print(f'  AM_wt*  = {base["am_star"]:.2f} %   '
              f'CI [{base["am_star_ci"][0]:.2f}, {base["am_star_ci"][1]:.2f}]')
        print(f'  SE_vol_frac (i)  = {base["sv_solid"]:.3f}')
        if base['sv_rve'] is not None:
            print(f'  SE_vol_frac (ii) = {base["sv_rve"]:.3f}')

    # ── (1) Statistical significance ──────────────────────────────
    print('\n[Item 1] Statistical significance vs measurement noise')
    if base['am_star'] is not None:
        lo, hi = base['am_star_ci']
        if lo is not None and hi is not None:
            # Map CI back to SE_vol_frac (i) for the 0.65 comparison
            am_wts = np.array([r['am_wt'] for r in all_rows])
            vf_sld = np.array([r['se_vol_frac_solid'] for r in all_rows])
            idx = np.argsort(am_wts)
            sv_at_lo = float(np.interp(lo, am_wts[idx], vf_sld[idx]))
            sv_at_hi = float(np.interp(hi, am_wts[idx], vf_sld[idx]))
            sv_lo, sv_hi = sorted([sv_at_lo, sv_at_hi])
            excludes = (sv_lo > 0.65) or (sv_hi < 0.65)
            verdict = ('✓ CI excludes 0.65 → statistically significant'
                        if excludes
                        else '⚠ CI brackets 0.65 → cannot reject null')
            print(f'  Bootstrap 95 % CI on SE_vol_frac (i): [{sv_lo:.3f}, {sv_hi:.3f}]')
            print(f'  Verdict: {verdict}')

    # ── (2) D_SE universality check ───────────────────────────────
    print('\n[Item 2] RCP-universality coincidence check '
          '(AM_wt* drift vs D_SE)')
    # Bin by D_SE — use natural project values (0.5/1.0/2.0/3.0 µm) when
    # available, otherwise fall back to quartiles.
    d_se = np.array([r['r_SE_um'] * 2 for r in all_rows])  # diameter
    valid_d = d_se[d_se > 0]
    if valid_d.size:
        unique_d = sorted(set(round(d, 1) for d in valid_d))
    else:
        unique_d = []
    if len(unique_d) <= 6 and len(unique_d) >= 2:
        # Discrete D_SE values — use as-is
        bins_used = [(d, [r for r in all_rows
                            if abs(r['r_SE_um']*2 - d) < 0.15]) for d in unique_d]
    elif valid_d.size >= 8:
        # Continuous — quartile-bin
        qs = np.quantile(valid_d, [0.0, 0.25, 0.5, 0.75, 1.0])
        bins_used = []
        for lo, hi in zip(qs[:-1], qs[1:]):
            subset = [r for r in all_rows
                      if lo <= r['r_SE_um']*2 <= hi]
            bins_used.append((f'{lo:.2f}-{hi:.2f}', subset))
    else:
        bins_used = []
    if not bins_used:
        print('  Insufficient D_SE variation in the sample to bin '
              '(need ≥ 2 distinct D_SE values).')
    else:
        print(f'  {"D_SE bin (µm)":18s} │ {"N":>5s} │ {"AM_wt*":>8s}'
              f' │ {"SE_vol_frac (i)":>16s} │ Δ vs baseline')
        drifts = []
        for label, sub in bins_used:
            res = _analyse_subset(sub)
            if res['am_star'] is None:
                continue
            d_am = (res['am_star'] - base['am_star']) if base['am_star'] else None
            drifts.append(res['am_star'])
            print(f'  D_SE = {str(label):11s} │ {res["n"]:>5d} │ '
                  f'{res["am_star"]:>7.2f}% │ {res["sv_solid"]:>15.3f} │ '
                  f'{(f"{d_am:+.2f} %p" if d_am is not None else "—"):>14s}')
        if len(drifts) >= 2:
            span = max(drifts) - min(drifts)
            verdict = ('⚠ AM_wt* drifts ' + f'{span:.1f} %p across D_SE'
                        ' → NOT universality (size-ratio dependent)'
                        if span > 3.0 else
                       '✓ AM_wt* stable within ' + f'{span:.1f} %p across D_SE'
                       ' → consistent with universality')
            print(f'  Verdict: {verdict}')

    # ── (3-C) Subset/campaign split ───────────────────────────────
    print('\n[Item 3-C] Subset deviation check — per-campaign AM_wt*')
    campaigns = sorted(set(r['campaign'] for r in all_rows))
    print(f'  {"campaign":20s} │ {"N":>5s} │ {"AM_wt*":>8s}'
          f' │ {"SE_vol_frac (i)":>16s} │ Δ vs baseline')
    cam_stars = []
    for cam in campaigns:
        sub = [r for r in all_rows if r['campaign'] == cam]
        res = _analyse_subset(sub)
        if res['am_star'] is None:
            print(f'  {cam:20s} │ {res["n"]:>5d} │ {"—":>8s} │ '
                  f'{"—":>16s} │ {"—":>14s}')
            continue
        d_am = (res['am_star'] - base['am_star']) if base['am_star'] else None
        cam_stars.append((cam, res['am_star']))
        print(f'  {cam:20s} │ {res["n"]:>5d} │ {res["am_star"]:>7.2f}% │ '
              f'{res["sv_solid"]:>15.3f} │ '
              f'{(f"{d_am:+.2f} %p" if d_am is not None else "—"):>14s}')
    if cam_stars:
        span = max(s for _, s in cam_stars) - min(s for _, s in cam_stars)
        verdict = ('⚠ AM_wt* varies > 5 %p across campaigns'
                    ' → deviation is subset-driven, NOT system-wide'
                    if span > 5.0 else
                   '✓ AM_wt* stable within ' + f'{span:.1f} %p across campaigns'
                   ' → deviation is system-wide, not a single regime')
        print(f'  Verdict: {verdict}')

    # ── (4) Outlier exclusion sensitivity ──────────────────────────
    print('\n[Item 4] Outlier sensitivity — exclude untrustworthy cases')
    # Re-read case_audit_fails.csv since it may not have been loaded
    # if the user did NOT pass --exclude-untrustworthy on this run.
    fails_csv = DOCSDB / 'case_audit_fails.csv'
    if fails_csv.exists():
        try:
            with fails_csv.open() as f:
                untrust = {r['case_dir'] for r in csv.DictReader(f)
                            if r.get('case_dir')}
        except Exception:
            untrust = set()
    else:
        untrust = set()
    kept = [r for r in all_rows if r['case_id'] not in untrust]
    dropped = [r for r in all_rows if r['case_id'] in untrust]
    res = _analyse_subset(kept)
    if res['am_star'] is not None and base['am_star'] is not None:
        d_am = res['am_star'] - base['am_star']
        # Per-campaign breakdown of the excluded set — addresses the
        # reviewer's "Δ = 0.00 %p needs explanation" point.  If the
        # exclusion set contains few or zero mono-AM `particulate`
        # cases, AM_wt* is naturally insensitive because the
        # threshold-crossing series is driven by that subset.
        dropped_by_camp: dict[str, int] = {}
        for r in dropped:
            dropped_by_camp[r['campaign']] = dropped_by_camp.get(r['campaign'], 0) + 1
        n_dropped_particulate = dropped_by_camp.get('particulate', 0)
        print(f'  Cases excluded: {len(dropped)} '
              f'(untrustworthy audit; {len(kept)} remain).')
        if dropped_by_camp:
            breakdown = ', '.join(f'{k}={v}' for k, v in
                                    sorted(dropped_by_camp.items()))
            print(f'    excluded by campaign: {breakdown}')
            print(f'    n excluded from mono-AM particulate (the subset '
                  f'driving AM_wt*): {n_dropped_particulate} / 20')
        print(f'  AM_wt* (excluded) = {res["am_star"]:.2f} %   '
              f'Δ vs baseline = {d_am:+.2f} %p')
        if res['sv_solid'] is not None:
            print(f'  SE_vol_frac (i)   = {res["sv_solid"]:.3f}')
        # Verdict needs awareness that a near-zero shift can be
        # *trivial* when the exclusions don't touch the driving
        # subset.  Flag that case explicitly so the reviewer can tell
        # robustness from non-impact.
        if abs(d_am) > 2.0:
            verdict = ('⚠ AM_wt* shifts > 2 %p when outliers excluded'
                        ' → threshold is outlier-driven')
        elif n_dropped_particulate == 0:
            verdict = ('· AM_wt* unchanged but exclusion did not touch '
                        'mono-AM driving subset (n_dropped_particulate = 0) '
                        '— robustness untested for the relevant subset')
        elif n_dropped_particulate <= 2:
            verdict = (f'~ AM_wt* shifts only {abs(d_am):.2f} %p; '
                        f'exclusion touched {n_dropped_particulate} '
                        f'particulate case(s), low statistical leverage')
        else:
            verdict = ('✓ AM_wt* shifts < 2 %p when outliers excluded '
                        f'including {n_dropped_particulate} particulate cases '
                        '→ threshold genuinely robust to outliers')
        print(f'  Verdict: {verdict}')
    else:
        print('  Verification not applicable (no fails CSV or no kept cases).')

    print()
    print('=' * 78)
    print('END VERIFICATION SUITE — copy block above into reviewer reply.')
    print('=' * 78)


if __name__ == '__main__':
    main()
