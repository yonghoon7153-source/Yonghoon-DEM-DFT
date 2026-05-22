"""
extract_xy_fracture_heatmap.py — XY-projection severe% heatmap per case.

Per case 결과:
  • docs/figures/xy_heatmap/<case_id>.png  (matplotlib)
  • docs/data/xy_heatmap/<case_id>.json    (heatmap data, NxN grid)

Heatmap quantity:
  per (x,y) bin = (#severe contacts) / (#total contacts)  ×100
  where severe = fragmentation + pulverization (Lawn stages 3-4).

Contact's (x,y) = midpoint of two particles.

Bins: default 20×20 over the RVE box dimensions.

Usage:
  python3 scripts/extract_xy_fracture_heatmap.py [case_dir ...]
  python3 scripts/extract_xy_fracture_heatmap.py --all       # 모든 webapp case
  python3 scripts/extract_xy_fracture_heatmap.py --tier 6mAh  # 특정 tier
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

# Import the existing Lawn fracture classifier (single source of truth)
try:
    from viewer3d_data import aggregate_particle_metrics
except ImportError as e:
    print(f'Cannot import viewer3d_data: {e}', file=sys.stderr)
    sys.exit(1)


def case_xy_heatmap(case_dir: Path, n_bins: int = 20):
    """Compute XY severe% heatmap for one case.

    Returns:
        {
            'case_id': ...,
            'n_bins': N,
            'box_x_um': float, 'box_y_um': float,
            'bins_x': [...], 'bins_y': [...],   # bin edges (μm)
            'severe_count': [[...]], 'total_count': [[...]],
            'severe_pct': [[...]],
            'n_severe_contacts': int, 'n_total_contacts': int,
        }
    Or None if data missing.
    """
    case_id = case_dir.name
    results_dir = ROOT / 'webapp' / 'results' / case_id

    atoms_csv = results_dir / 'atoms.csv'
    contacts_csv = results_dir / 'contacts.csv'
    meta_file = case_dir / 'meta.json'
    ip_file = results_dir / 'input_params.json'
    fm_file = results_dir / 'full_metrics.json'

    if not (atoms_csv.exists() and contacts_csv.exists() and meta_file.exists()):
        return None

    meta = json.loads(meta_file.read_text())
    scale = meta.get('scale', 1000)
    type_map_str = meta.get('type_map', '1:AM,2:SE')
    type_map = {}
    for item in type_map_str.split(','):
        k, v = item.split(':')
        type_map[int(k)] = v.strip()

    ip = json.loads(ip_file.read_text()) if ip_file.exists() else {}
    box_x_um = (ip.get('box_x') or 0.05) * scale
    box_y_um = (ip.get('box_y') or 0.05) * scale
    if box_x_um <= 0 or box_y_um <= 0:
        return None

    # Atoms — map id → (x_um, y_um, type, r_um)
    df_a = pd.read_csv(atoms_csv)
    for col in df_a.columns:
        df_a[col] = pd.to_numeric(df_a[col], errors='coerce')
    atoms_by_id = {
        int(r['id']): {
            'type':   int(r['type']),
            'radius': float(r['radius']),
            'x':      float(r['x']),
            'y':      float(r['y']),
            'z':      float(r['z']),
        }
        for _, r in df_a.iterrows()
    }

    # Run aggregate to get brittle_pairs + counts
    contacts_df = pd.read_csv(contacts_csv, low_memory=False)
    n_total = len(contacts_df)
    if n_total > 5_000_000:
        return None  # too large

    def _stream(df):
        cols = list(df.columns)
        for tup in df.itertuples(index=False, name=None):
            yield dict(zip(cols, tup))

    agg = aggregate_particle_metrics(_stream(contacts_df), atoms_by_id,
                                      type_map, scale=scale)
    brittle_pairs = agg.get('brittle_pairs', [])

    # Bins (in μm)
    bins_x = np.linspace(0, box_x_um, n_bins + 1)
    bins_y = np.linspace(0, box_y_um, n_bins + 1)
    severe = np.zeros((n_bins, n_bins), dtype=int)
    total  = np.zeros((n_bins, n_bins), dtype=int)

    # Total = number of brittle_pairs (all damaged contacts)
    # Severe = subset where stage in {fragmentation, pulverization}
    n_severe = 0
    n_total_contacts = len(brittle_pairs)
    for bp in brittle_pairs:
        a1 = atoms_by_id.get(bp['id1'])
        a2 = atoms_by_id.get(bp['id2'])
        if not (a1 and a2):
            continue
        # Mid-point in μm (positions stored in sim units)
        mx = (a1['x'] + a2['x']) / 2 * scale
        my = (a1['y'] + a2['y']) / 2 * scale
        ix = int(np.clip(np.floor(mx / box_x_um * n_bins), 0, n_bins - 1))
        iy = int(np.clip(np.floor(my / box_y_um * n_bins), 0, n_bins - 1))
        total[iy, ix] += 1
        if bp.get('stage') in ('fragmentation', 'pulverization'):
            severe[iy, ix] += 1
            n_severe += 1

    # severe %: per-bin (severe/total)*100, NaN where total=0
    with np.errstate(divide='ignore', invalid='ignore'):
        severe_pct = np.where(total > 0, severe / total * 100, np.nan)

    return {
        'case_id': case_id, 'case_name': meta.get('name', case_id),
        'n_bins': n_bins,
        'box_x_um': round(box_x_um, 2), 'box_y_um': round(box_y_um, 2),
        'bins_x': bins_x.tolist(), 'bins_y': bins_y.tolist(),
        'severe_count': severe.tolist(),
        'total_count':  total.tolist(),
        'severe_pct':   [[None if np.isnan(v) else round(v, 1)
                          for v in row] for row in severe_pct],
        'n_severe_contacts': n_severe,
        'n_total_contacts':  n_total_contacts,
        'severe_frac_overall': round(100 * n_severe / max(n_total_contacts, 1), 2),
    }


def render_png(data: dict, out_path: Path):
    """Render the heatmap as a 2-panel PNG (severe% + total density)."""
    if not data:
        return False
    severe_pct = np.array([[np.nan if v is None else v for v in row]
                            for row in data['severe_pct']], dtype=float)
    total = np.array(data['total_count'])
    bins_x, bins_y = data['bins_x'], data['bins_y']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: severe%  (color = damage intensity)
    ax = axes[0]
    im = ax.imshow(severe_pct, origin='lower',
                    extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]],
                    cmap='hot_r', vmin=0, vmax=max(10, np.nanmax(severe_pct) if np.isfinite(np.nanmax(severe_pct)) else 10),
                    aspect='equal', interpolation='nearest')
    ax.set_title(f"Severe% (frag + pulv) per XY bin\n"
                 f"overall: {data['severe_frac_overall']}% ({data['n_severe_contacts']}/{data['n_total_contacts']})",
                 fontsize=10)
    ax.set_xlabel('x (μm)'); ax.set_ylabel('y (μm)')
    plt.colorbar(im, ax=ax, label='severe %', fraction=0.046, pad=0.04)

    # Right: total contact density (sanity check — uniform = OK)
    ax = axes[1]
    im = ax.imshow(total, origin='lower',
                    extent=[bins_x[0], bins_x[-1], bins_y[0], bins_y[-1]],
                    cmap='viridis', aspect='equal', interpolation='nearest')
    ax.set_title(f"Total damaged contact count per XY bin\n"
                 f"sum: {total.sum()}, max bin: {total.max()}",
                 fontsize=10)
    ax.set_xlabel('x (μm)'); ax.set_ylabel('y (μm)')
    plt.colorbar(im, ax=ax, label='count', fraction=0.046, pad=0.04)

    fig.suptitle(f"{data['case_name']} — XY fracture heatmap "
                  f"(RVE {data['box_x_um']:.0f}×{data['box_y_um']:.0f} μm, {data['n_bins']}×{data['n_bins']} bins)",
                  fontsize=11, y=1.02)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*',
                    help='case names (e.g. input_6mAh_real_4) or directories')
    ap.add_argument('--all', action='store_true',
                    help='process every case under webapp/uploads')
    ap.add_argument('--tier', help='filter by tier (1mAh, 6mAh, 8mAh, particulate, S)')
    ap.add_argument('--n-bins', type=int, default=20)
    ap.add_argument('--out-png', default='docs/figures/xy_heatmap')
    ap.add_argument('--out-json', default='docs/data/xy_heatmap')
    args = ap.parse_args()

    uploads = ROOT / 'webapp' / 'uploads'
    candidates = []
    if args.all or args.tier:
        # Walk uploads — case names extracted from meta.json
        for d in sorted(uploads.iterdir()):
            if not d.is_dir(): continue
            mf = d / 'meta.json'
            if not mf.exists(): continue
            try:
                name = json.loads(mf.read_text()).get('name', d.name)
            except Exception:
                continue
            if args.tier and args.tier not in name:
                continue
            candidates.append((name, d))
    elif args.cases:
        # Names or directories
        for cn in args.cases:
            p = Path(cn)
            if p.is_dir():
                candidates.append((p.name, p))
                continue
            # Look up name → directory via meta.json
            for d in uploads.iterdir():
                if not d.is_dir(): continue
                mf = d / 'meta.json'
                if not mf.exists(): continue
                try:
                    if json.loads(mf.read_text()).get('name') == cn:
                        candidates.append((cn, d))
                        break
                except Exception:
                    pass
    else:
        ap.print_help()
        return

    print(f'Processing {len(candidates)} case(s)...')
    out_png_dir  = ROOT / args.out_png
    out_json_dir = ROOT / args.out_json
    out_png_dir.mkdir(parents=True, exist_ok=True)
    out_json_dir.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    for name, d in candidates:
        try:
            data = case_xy_heatmap(d, n_bins=args.n_bins)
        except Exception as e:
            print(f'  [{name}] FAILED: {type(e).__name__}: {e}')
            continue
        if not data:
            print(f'  [{name}] skip (missing data or too large)')
            continue
        # Save JSON
        (out_json_dir / f'{name}.json').write_text(json.dumps(data, indent=2))
        # Render PNG
        ok = render_png(data, out_png_dir / f'{name}.png')
        if ok:
            n_ok += 1
            print(f'  [{name}] severe {data["severe_frac_overall"]}% '
                  f'(n_severe={data["n_severe_contacts"]} / {data["n_total_contacts"]})')

    print(f'\nDone — {n_ok}/{len(candidates)} cases rendered.')
    print(f'  PNGs  → {out_png_dir}')
    print(f'  JSONs → {out_json_dir}')


if __name__ == '__main__':
    main()
