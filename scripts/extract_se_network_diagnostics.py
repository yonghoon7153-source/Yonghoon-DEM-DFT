#!/usr/bin/env python3
"""Phase C — Batch SE network diagnostics + paper-quality figure.

For every case in webapp/results/ + webapp/archive/:
  1. Load atoms.csv + contacts.csv
  2. Run compute_se_network_diagnostics() (Phase A5+A6 code path)
  3. Extract composition (AM:SE, P:S, scale, φ_SE)
  4. Aggregate per-case stats:
       - n_percolating, n_cut, n_bn
       - bn_min, bn_median areas (μm²)
       - dead-end cluster counts
       - cut_fraction (n_cut / n_percolating)

Writes:
  docs/data/se_diagnostics_82.csv         — full per-case table
  docs/figures/percolation_risk_scaling.png  — 4-panel paper figure

Usage:
  python3 scripts/extract_se_network_diagnostics.py
  python3 scripts/extract_se_network_diagnostics.py --csv-only
  python3 scripts/extract_se_network_diagnostics.py --no-plot
"""
from __future__ import annotations
import argparse, csv, json, math, os, sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
SCRIPTS = ROOT / 'scripts'
DATA_DIR = ROOT / 'docs' / 'data'
FIG_DIR  = ROOT / 'docs' / 'figures'
sys.path.insert(0, str(SCRIPTS))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from viewer3d_data import compute_se_network_diagnostics

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


_TS_PAT = __import__('re').compile(r'^\d{6}_\d{6}_[0-9a-f]{6,}$')

def _is_timestamp_name(name: str) -> bool:
    """True for archive timestamp IDs like 260421_213656_78ec86."""
    return bool(_TS_PAT.match(name))


def discover_cases() -> list[Path]:
    """Walk both results/ and archive/, dedup by (atoms.csv size,
    contacts.csv size).  Prefer NAMED case_ids (input_*, etc.) over
    timestamp-style IDs when both exist for the same analysis.
    """
    # Pass 1: collect every candidate dir
    cands = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if not ((d / 'contacts.csv').exists() and
                    ((d / 'input_params.json').exists() or
                     (d / 'meta.json').exists())):
                continue
            try:
                size = atoms_p.stat().st_size
                ct_size = (d / 'contacts.csv').stat().st_size
            except OSError:
                continue
            cands.append((d, size, ct_size))

    # Pass 2: dedup by (atoms size, contacts size); within a key, prefer
    # non-timestamp names (i.e., human-readable input_* over hex IDs).
    by_key: dict[tuple, Path] = {}
    for d, asize, csize in cands:
        key = (asize, csize)
        if key not in by_key:
            by_key[key] = d
        else:
            cur = by_key[key]
            cur_is_ts = _is_timestamp_name(cur.name)
            new_is_ts = _is_timestamp_name(d.name)
            if cur_is_ts and not new_is_ts:
                by_key[key] = d   # named wins over timestamp
    return sorted(by_key.values())


def load_case(case_dir: Path):
    """Returns (atoms_by_id, type_map, scale, meta)."""
    meta = {}
    for fname in ('input_params.json', 'meta.json'):
        p = case_dir / fname
        if p.exists():
            try:
                meta = json.loads(p.read_text())
                break
            except Exception:
                pass
    scale = float(meta.get('scale') or 1000.0)
    # type_map: prefer "1:AM_P,2:AM_S,3:SE" string format
    type_map = {}
    tm = meta.get('type_map')
    if isinstance(tm, str):
        for tok in tm.split(','):
            if ':' in tok:
                k, v = tok.split(':', 1)
                try:
                    type_map[int(k.strip())] = v.strip()
                except Exception:
                    pass
    elif isinstance(tm, dict):
        for k, v in tm.items():
            try:
                type_map[int(k)] = str(v)
            except Exception:
                pass
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

    atoms = {}
    with (case_dir / 'atoms.csv').open() as f:
        for r in csv.DictReader(f):
            try:
                aid = int(r['id'])
            except Exception:
                continue
            atoms[aid] = {
                'type':   int(r.get('type', 0) or 0),
                'radius': float(r.get('radius', 0) or 0),
                'x':      float(r.get('x', 0) or 0),
                'y':      float(r.get('y', 0) or 0),
                'z':      float(r.get('z', 0) or 0),
            }
    return atoms, type_map, scale, meta


def load_contacts(case_dir: Path):
    out = []
    p = case_dir / 'contacts.csv'
    if not p.exists():
        return out
    with p.open() as f:
        for r in csv.DictReader(f):
            try:
                i1 = int(r['id1']); i2 = int(r['id2'])
            except Exception:
                continue
            area = float(r.get('contact_area', 0) or 0)
            delta = float(r.get('delta', 0) or 0)
            out.append({
                'id1': i1, 'id2': i2,
                'contact_area': area, 'delta': delta,
            })
    return out


def estimate_plate_z(atoms: dict) -> float:
    """Topmost z + radius among all particles (sim units)."""
    if not atoms:
        return 0.0
    return max(a['z'] + a['radius'] for a in atoms.values())


def load_composition(case_dir: Path, meta: dict):
    """Extract AM_wt fraction, P:S ratio, λ_eff, φ_SE.

    Falls back to all_dem_porosity.csv lookup if meta is incomplete."""
    am_wt = meta.get('am_wt')
    se_wt = meta.get('se_wt')
    p_vol = meta.get('p_vol') or 0
    s_vol = meta.get('s_vol') or 0
    r_AM_P = meta.get('r_AM_P_um') or 0
    r_AM_S = meta.get('r_AM_S_um') or 0
    r_SE   = meta.get('r_SE_um') or 0

    # Lookup in all_dem_porosity.csv (canonical source)
    porosity_csv = ROOT / 'all_dem_porosity.csv'
    if porosity_csv.exists():
        case_id = case_dir.name
        for r in csv.DictReader(porosity_csv.open()):
            if r.get('case_id', '').strip() == case_id:
                am_wt  = float(r.get('am_wt', am_wt or 0) or 0)
                se_wt  = float(r.get('se_wt', se_wt or 0) or 0)
                p_vol  = float(r.get('p_vol', 0) or 0)
                s_vol  = float(r.get('s_vol', 0) or 0)
                r_AM_P = float(r.get('r_AM_P_um', 0) or 0)
                r_AM_S = float(r.get('r_AM_S_um', 0) or 0)
                r_SE   = float(r.get('r_SE_um', 0) or 0)
                break

    # Effective r_AM (volume-weighted)
    if p_vol + s_vol > 0:
        r_eff = (p_vol*r_AM_P + s_vol*r_AM_S) / (p_vol + s_vol)
        f_AMP = p_vol / (p_vol + s_vol)
    elif r_AM_S > 0:
        r_eff = r_AM_S; f_AMP = 0.0
    else:
        r_eff = r_AM_P; f_AMP = 1.0
    lam_eff = (r_eff / r_SE) if r_SE > 0 else 0
    # Volume fraction (ρ_AM=4.8, ρ_SE=2.0 g/cm³)
    V_AM = (am_wt or 0) / 4.8
    V_SE = (se_wt or (100 - (am_wt or 0))) / 2.0
    phi_SE = V_SE / (V_AM + V_SE) if (V_AM + V_SE) > 0 else 0
    return {
        'am_wt':   am_wt or 0,
        'se_wt':   se_wt or (100 - (am_wt or 0)),
        'p_vol':   p_vol,
        's_vol':   s_vol,
        'f_AMP':   f_AMP,
        'r_AM_P':  r_AM_P,
        'r_AM_S':  r_AM_S,
        'r_SE':    r_SE,
        'lam_eff': lam_eff,
        'phi_SE':  phi_SE,
    }


def analyze_case(case_dir: Path) -> dict | None:
    case_id = case_dir.name
    try:
        atoms, type_map, scale, meta = load_case(case_dir)
        contacts = load_contacts(case_dir)
        plate_z = estimate_plate_z(atoms)
        diag = compute_se_network_diagnostics(
            contacts, atoms, type_map, plate_z=plate_z, scale=scale)
    except Exception as e:
        print(f'  [{case_id}] SKIP — load/diag fail: {e}')
        return None
    comp = load_composition(case_dir, meta)
    bn = diag.get('bottleneck_edges') or []
    bn_areas = [b['area_um2'] for b in bn]
    bn_norms = [b.get('area_norm', 0) for b in bn]
    return {
        'case_id': case_id,
        'campaign': meta.get('campaign', '?'),
        **comp,
        'scale_factor': scale,
        'n_percolating': diag.get('n_percolating', 0),
        'n_cut':        len(diag.get('articulation_points') or []),
        'n_bn':         len(bn),
        # raw areas (μm²) — bn_area_min may vary across cases due to r_SE
        'bn_area_min':  round(min(bn_areas), 5) if bn_areas else None,
        'bn_area_p10':  round(float(np.percentile(bn_areas, 10)), 5) if bn_areas else None,
        'bn_area_p50':  round(float(np.percentile(bn_areas, 50)), 5) if bn_areas else None,
        # normalized A/r² — scale-invariant, cross-case comparable
        'bn_norm_min':  round(min(bn_norms), 5) if bn_norms else None,
        'bn_norm_p10':  round(float(np.percentile(bn_norms, 10)), 5) if bn_norms else None,
        'bn_norm_p50':  round(float(np.percentile(bn_norms, 50)), 5) if bn_norms else None,
        # reference: median A/r² across full percolating subgraph + threshold used
        'bn_median_norm':    diag.get('bn_median_norm', 0),
        'bn_threshold_norm': diag.get('bn_threshold_norm', 0),
        'n_dead_end_clusters': len(diag.get('dead_end_clusters') or []),
        'n_dead_end_top':      sum(1 for d in (diag.get('dead_end_clusters') or [])
                                     if d.get('type') == 'top_only'),
        'n_dead_end_bot':      sum(1 for d in (diag.get('dead_end_clusters') or [])
                                     if d.get('type') == 'bottom_only'),
        'cut_fraction':        round(len(diag.get('articulation_points') or [])
                                       / max(1, diag.get('n_percolating', 0)), 4),
    }


# ────────────────────────────────────────────────────────────────────────
def write_csv(rows: list[dict], out_path: Path):
    if not rows:
        print('No rows to write.'); return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with out_path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f'CSV → {out_path}  ({len(rows)} rows)')


# ── 4-panel paper figure ──────────────────────────────────────────────
def make_figure(rows: list[dict], out_path: Path):
    if not rows:
        print('No data for figure.'); return
    R = [r for r in rows if r['n_percolating'] > 0]
    if not R:
        print('No percolating cases — figure skipped.'); return
    phi   = np.array([r['phi_SE']     for r in R])
    lam   = np.array([r['lam_eff']    for r in R])
    f_AM  = np.array([r['am_wt'] / 100 for r in R])
    n_cut = np.array([r['n_cut']      for r in R])
    cutf  = np.array([r['cut_fraction'] for r in R])
    bnmin = np.array([r['bn_area_min'] or np.nan for r in R])
    bnp50 = np.array([r['bn_area_p50'] or np.nan for r in R])
    # Normalized A/r² — scale-invariant
    bnnorm_min = np.array([r['bn_norm_min'] or np.nan for r in R])
    bnnorm_p50 = np.array([r['bn_norm_p50'] or np.nan for r in R])
    bn_med     = np.array([r['bn_median_norm'] or np.nan for r in R])
    camp  = [r['campaign'] for r in R]

    camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
                   '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
    camp_lab = {'particulate': 'particulate', '박막(1mAh)': 'thin 1mAh',
                '후막(6mAh)': 'thick 6mAh', '후막(8mAh)': 'thick 8mAh'}

    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.28,
                          left=0.07, right=0.985, top=0.93, bottom=0.07)

    def scatter(ax, x, y, ylog=False, xlog=False,
                 xlabel='', ylabel='', title=''):
        for c in sorted(set(camp)):
            idx = np.array([i for i, cc in enumerate(camp) if cc == c])
            if len(idx) == 0: continue
            ax.scatter(x[idx], y[idx], c=camp_colors.get(c, '#999'),
                        s=42, edgecolors='black', linewidths=0.5,
                        label=camp_lab.get(c, c))
        # Only set log scale when data has positive values (avoid matplotlib
        # warning on cases where x/y is all zero or NaN)
        if ylog and np.nanmax(y) > 0:
            ax.set_yscale('log')
        if xlog and np.nanmax(x) > 0:
            ax.set_xscale('log')
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        ax.set_title(title, loc='left')
        ax.grid(alpha=0.25)

    # (a) cut count vs φ_SE
    ax = fig.add_subplot(gs[0, 0])
    scatter(ax, phi, n_cut,
            xlabel=r'SE volume fraction  $\phi_{\mathrm{SE}}$',
            ylabel=r'$n_{\mathrm{cut}}$  (articulation points)',
            title=r'(a)  Cut-node count vs $\phi_{\mathrm{SE}}$')
    ax.legend(loc='best', fontsize=7.5)

    # (b) bn min normalized A/r² vs φ_SE — scale-invariant
    ax = fig.add_subplot(gs[0, 1])
    scatter(ax, phi, bnnorm_min, ylog=True,
            xlabel=r'SE volume fraction  $\phi_{\mathrm{SE}}$',
            ylabel=r'Narrowest  $A/r_{\min}^2$  (dimensionless)',
            title=r'(b)  Bottleneck min  $A/r^2$  vs $\phi_{\mathrm{SE}}$')
    # Reference line: median across all cases
    median_ref = float(np.nanmedian(bn_med)) if not np.all(np.isnan(bn_med)) else None
    if median_ref:
        ax.axhline(median_ref, color='gray', ls='--', lw=0.8,
                    label=f'corpus median A/r² ≈ {median_ref:.3f}')
        ax.axhline(median_ref * 0.10, color='red', ls=':', lw=0.8,
                    label='threshold (10% of median)')
        ax.legend(loc='best', fontsize=7)

    # (c) cut fraction vs λ_eff (skip log if no positive λ)
    ax = fig.add_subplot(gs[1, 0])
    scatter(ax, lam, cutf, xlog=True,
            xlabel=r'Size ratio  $\lambda_{\mathrm{eff}} = r_{\mathrm{AM,eff}}/r_{\mathrm{SE}}$',
            ylabel=r'$n_{\mathrm{cut}} / n_{\mathrm{percolating}}$',
            title=r'(c)  Cut fraction (network fragility) vs $\lambda_{\mathrm{eff}}$')
    if np.nanmax(lam) > 0:
        ax.set_xticks([2, 3, 5, 7, 10, 15, 20])
        ax.set_xticklabels(['2', '3', '5', '7', '10', '15', '20'])

    # (d) bn median A/r² vs AM weight fraction
    ax = fig.add_subplot(gs[1, 1])
    scatter(ax, f_AM*100, bnnorm_p50, ylog=True,
            xlabel='AM weight fraction (%)',
            ylabel=r'Bottleneck median  $A/r_{\min}^2$',
            title=r'(d)  Bottleneck median  $A/r^2$  vs AM weight fraction')

    fig.suptitle(
        'SE percolation-risk descriptors across 82-case DEM corpus  —  '
        'cut nodes (topology) + bottleneck areas (transport)',
        fontsize=12, fontweight='bold', y=0.985)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    print(f'Figure → {out_path}')


# ────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv-only', action='store_true',
                     help='Only write CSV, skip figure.')
    ap.add_argument('--no-plot', action='store_true',
                     help='Same as --csv-only.')
    ap.add_argument('--out-csv', default=str(DATA_DIR / 'se_diagnostics_82.csv'))
    ap.add_argument('--out-fig', default=str(FIG_DIR / 'percolation_risk_scaling.png'))
    args = ap.parse_args()

    cases = discover_cases()
    print(f'Found {len(cases)} candidate case dirs')

    rows = []
    for i, case_dir in enumerate(cases):
        result = analyze_case(case_dir)
        if result is None: continue
        rows.append(result)
        print(f'  [{i+1:>3}/{len(cases)}] {case_dir.name:35s}  '
              f'perc={result["n_percolating"]:>5d}  cut={result["n_cut"]:>4d}  '
              f'bn_min={result["bn_area_min"] if result["bn_area_min"] is not None else "-"}')

    # Summary diagnostics
    n_total = len(rows)
    n_perc  = sum(1 for r in rows if r['n_percolating'] > 0)
    n_with_comp = sum(1 for r in rows if r['lam_eff'] > 0)
    print(f'\nSummary:')
    print(f'  total cases:                 {n_total}')
    print(f'  with percolating SE (>0):    {n_perc}')
    print(f'  with composition (lam>0):    {n_with_comp}')
    print(f'  → figure uses intersection (both)')

    write_csv(rows, Path(args.out_csv))
    if not (args.csv_only or args.no_plot):
        make_figure(rows, Path(args.out_fig))


if __name__ == '__main__':
    main()
