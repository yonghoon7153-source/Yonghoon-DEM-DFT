#!/usr/bin/env python3
"""
Per-contact Physics-mode cap attribution.

For the case(s) given, iterate every contact, run the full plastic_coverage
physics-mode decision, and record WHICH of the four candidates wins A_plastic:

  elastic_lb   — A_elastic  (pure Hertz point contact)
  liggghts_lb  — A_liggghts (LIGGGHTS-reported contact area)
  tabor        — A = F_real / H  (plastic Tabor)
  volume       — V_overlap / h_film_min  (volume-conservation cap)
  geom         — 2π R_min²  (hemisphere lateral cap)

Outputs:
  • stdout: regime table + δ/R* quantiles
  • <out>/<case>_regime_hist.png   — stacked bar (regime fraction)
  • <out>/<case>_dR_hist.png       — δ/R* histogram coloured by winning cap
  • <out>/<case>_regime.csv        — per-contact wins

Usage:
  python3 scripts/physics_regime_histogram.py <case_id> [<case_id>...]
  python3 scripts/physics_regime_histogram.py 260418_165023_2f531c 260421_212503_cb59a9
"""
from __future__ import annotations
import os, sys, json, argparse
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from plastic_coverage import (
    E_STAR_AM_SE_REAL, H_REAL_SE, H_FILM_MIN,
    DR_YIELD_ONSET, DR_FULLY_PLASTIC,
)


CAP_LABELS = ['elastic_lb', 'liggghts_lb', 'tabor', 'volume', 'geom']
CAP_COLORS = {
    'elastic_lb':  '#60a5fa',   # blue   — under-plastic fallback
    'liggghts_lb': '#34d399',   # green  — DEM-native
    'tabor':       '#fbbf24',   # amber  — plastic Tabor active
    'volume':      '#fb923c',   # orange — volume conservation
    'geom':        '#ef4444',   # red    — hemisphere (extreme)
}


def classify_contacts(atoms_csv: str, contacts_csv: str) -> pd.DataFrame:
    """Return DataFrame with per-contact δ, R*, the 4 candidate areas, winner."""
    atoms = pd.read_csv(atoms_csv)
    id_r = dict(zip(atoms['id'].astype(int), atoms['radius'].astype(float)))

    cdf = pd.read_csv(contacts_csv, low_memory=False)
    needed = {'id1', 'id2', 'delta', 'contact_area'}
    if not needed.issubset(cdf.columns):
        raise KeyError(f"Missing columns in {contacts_csv}: want {needed}, got {set(cdf.columns)}")

    r1 = cdf['id1'].astype(int).map(id_r).astype(float)
    r2 = cdf['id2'].astype(int).map(id_r).astype(float)
    delta = cdf['delta'].astype(float)
    ligg  = cdf['contact_area'].astype(float)

    R_star = (r1 * r2) / (r1 + r2)
    R_min  = np.minimum(r1, r2)
    dr     = np.where(R_star > 0, delta / R_star, 0.0)

    elastic = np.pi * R_star * delta
    F_real  = (4.0/3.0) * E_STAR_AM_SE_REAL * np.sqrt(R_star) * np.power(delta, 1.5)
    A_tabor = F_real / H_REAL_SE
    V_over  = (np.pi/6.0) * (delta**2) * (3.0*R_star - delta)
    A_vol   = V_over / H_FILM_MIN
    A_geom  = 2.0 * np.pi * (R_min ** 2)

    # min of physics caps
    A_cap = np.minimum(A_tabor, np.minimum(A_vol, A_geom))
    dem_lb = np.maximum(elastic, ligg.fillna(0.0))
    A_final = np.maximum(dem_lb, A_cap)

    # Attribution — which candidate produced A_final?
    eps = 1e-30
    winners = np.empty(len(cdf), dtype=object)
    # elastic-only branch (dr < DR_YIELD_ONSET): always elastic
    is_elastic_regime = dr < DR_YIELD_ONSET
    winners[is_elastic_regime] = 'elastic_lb'
    # non-elastic: who wins?
    mask = ~is_elastic_regime
    for lbl, arr in [('elastic_lb', elastic), ('liggghts_lb', ligg.fillna(0.0)),
                     ('tabor', A_tabor), ('volume', A_vol), ('geom', A_geom)]:
        close = np.isclose(A_final, arr, rtol=1e-6, atol=eps)
        assign = mask & close & (winners == None)
        winners[assign] = lbl
    # leftover (shouldn't happen) → tabor default
    winners[winners == None] = 'tabor'

    return pd.DataFrame({
        'id1': cdf['id1'].astype(int),
        'id2': cdf['id2'].astype(int),
        'delta': delta, 'R_star': R_star, 'dr': dr,
        'elastic_area_um2': elastic * 1e12,    # m² → μm² (assumes sim units = m)
        'liggghts_area_um2': ligg * 1e12,
        'A_tabor_um2': A_tabor * 1e12,
        'A_volume_um2': A_vol * 1e12,
        'A_geom_um2': A_geom * 1e12,
        'A_final_um2': A_final * 1e12,
        'regime': winners,
    })


def plot_case(df: pd.DataFrame, case_name: str, out_dir: str):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    os.makedirs(out_dir, exist_ok=True)

    # 1) Stacked-bar regime fraction
    counts = df['regime'].value_counts()
    total = counts.sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    bottom = 0.0
    for lbl in CAP_LABELS:
        frac = counts.get(lbl, 0) / total * 100
        if frac > 0:
            ax.bar(case_name, frac, bottom=bottom,
                   color=CAP_COLORS[lbl], label=f'{lbl} ({frac:.1f}%)',
                   edgecolor='white', linewidth=0.5)
            bottom += frac
    ax.set_ylabel('Contact fraction (%)')
    ax.set_title(f'Physics-mode cap attribution — {case_name}\n'
                 f'Total contacts: {total:,}')
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    plt.tight_layout()
    p = os.path.join(out_dir, f'{case_name}_regime_hist.png')
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f'  → {p}')

    # 2) δ/R* histogram colored by winning cap
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bins = np.linspace(0, min(0.5, df['dr'].quantile(0.99) * 1.1), 60)
    bot = np.zeros(len(bins) - 1)
    for lbl in CAP_LABELS:
        vals = df.loc[df['regime'] == lbl, 'dr'].values
        if len(vals) == 0:
            continue
        h, _ = np.histogram(vals, bins=bins)
        ax.bar(bins[:-1], h, width=np.diff(bins), bottom=bot,
               color=CAP_COLORS[lbl], label=lbl, align='edge',
               edgecolor='none')
        bot += h
    ax.axvline(DR_YIELD_ONSET,   color='k', lw=0.6, ls='--',
               label=f'yield onset ({DR_YIELD_ONSET:.3f})')
    ax.axvline(DR_FULLY_PLASTIC, color='k', lw=0.6, ls=':',
               label=f'fully plastic ({DR_FULLY_PLASTIC:.3f})')
    ax.set_xlabel(r'$\delta / R^*$ (normalized overlap)')
    ax.set_ylabel('contacts')
    ax.set_yscale('log')
    ax.set_title(f'δ/R* distribution — {case_name}')
    ax.legend(loc='upper right', fontsize=7, framealpha=0.9)
    plt.tight_layout()
    p = os.path.join(out_dir, f'{case_name}_dR_hist.png')
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f'  → {p}')


def find_case_dir(case_id: str) -> str | None:
    for base in ('webapp/results', 'webapp/archive'):
        p = os.path.join(base, case_id)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'atoms.csv')) \
           and os.path.exists(os.path.join(p, 'contacts.csv')):
            return p
    return None


def get_case_name(case_id: str, case_dir: str) -> str:
    # Try meta.json name; fall back to case_id
    for base in ('webapp/uploads', 'webapp/results'):
        m = os.path.join(base, case_id, 'meta.json')
        if os.path.exists(m):
            try:
                return json.load(open(m)).get('name', case_id)
            except Exception:
                pass
    m = os.path.join(case_dir, 'meta.json')
    if os.path.exists(m):
        try:
            return json.load(open(m)).get('name', case_id)
        except Exception:
            pass
    return case_id


def discover_cases() -> list[str]:
    """Every case_id under webapp/results with both atoms.csv and contacts.csv."""
    out = []
    base = 'webapp/results'
    if not os.path.isdir(base):
        return out
    for cid in sorted(os.listdir(base)):
        d = os.path.join(base, cid)
        if os.path.isdir(d) \
           and os.path.exists(os.path.join(d, 'atoms.csv')) \
           and os.path.exists(os.path.join(d, 'contacts.csv')):
            out.append(cid)
    return out


def plot_dataset_summary(summary_df, out_dir, sort_by='p50_dr'):
    """Dataset-wide stacked-bar — one bar per case, sorted by median δ/R*."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    df = summary_df.copy()
    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=True).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(max(10, len(df) * 0.18), 9),
                                    sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    x = np.arange(len(df))
    bottom = np.zeros(len(df))
    for lbl in CAP_LABELS:
        if lbl not in df.columns:
            continue
        y = df[lbl].values
        ax1.bar(x, y, bottom=bottom, color=CAP_COLORS[lbl],
                edgecolor='white', linewidth=0.3, label=lbl, width=0.9)
        bottom += y
    ax1.set_ylabel('Contacts in each cap (%)')
    ax1.set_ylim(0, 100)
    ax1.set_title(f'Physics-mode cap attribution across {len(df)} cases '
                  f'(sorted by median δ/R*)')
    ax1.legend(loc='lower right', fontsize=8, framealpha=0.95, ncol=5)
    ax1.grid(axis='y', alpha=0.2)

    # Lower panel: median/p90/max δ/R* per case
    ax2.plot(x, df['p50_dr'], color='#2563eb', marker='o', ms=3, label='p50 δ/R*')
    ax2.plot(x, df['p90_dr'], color='#d97706', marker='s', ms=3, label='p90 δ/R*')
    ax2.plot(x, df['max_dr'], color='#dc2626', marker='^', ms=3, label='max δ/R*')
    ax2.axhline(DR_YIELD_ONSET,   color='k', ls='--', lw=0.6, label=f'yield onset ({DR_YIELD_ONSET:.3f})')
    ax2.axhline(DR_FULLY_PLASTIC, color='k', ls=':',  lw=0.6, label=f'fully plastic ({DR_FULLY_PLASTIC:.3f})')
    ax2.set_ylabel('δ/R*')
    ax2.set_yscale('log')
    ax2.legend(loc='upper left', fontsize=7, framealpha=0.95, ncol=3)
    ax2.grid(axis='y', alpha=0.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df['name'], rotation=90, fontsize=6)
    ax2.set_xlabel('case (sorted by median δ/R*)')

    plt.tight_layout()
    p = os.path.join(out_dir, 'dataset_regime_summary.png')
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f'\n→ {p}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*',
                    help='case_id(s) to analyse (omit with --all)')
    ap.add_argument('--all', action='store_true',
                    help='Process every case under webapp/results/ with CSVs')
    ap.add_argument('--no-per-case-plots', action='store_true',
                    help='Skip per-case PNG generation (--all is fast-mode by default)')
    ap.add_argument('-o', '--out', default='docs/figures/physics_regime',
                    help='output directory for PNGs + CSV')
    args = ap.parse_args()

    cases = list(args.cases)
    if args.all:
        cases = discover_cases()
        if not args.cases and not args.no_per_case_plots:
            # fast default for dataset-wide run
            args.no_per_case_plots = True
    if not cases:
        ap.error('No cases given. Pass case_id(s) or use --all.')

    os.makedirs(args.out, exist_ok=True)
    summary_rows = []

    for cid in cases:
        cdir = find_case_dir(cid)
        if not cdir:
            print(f'[SKIP] {cid} — no atoms.csv/contacts.csv found')
            continue
        name = get_case_name(cid, cdir)
        atoms_csv = os.path.join(cdir, 'atoms.csv')
        contacts_csv = os.path.join(cdir, 'contacts.csv')

        df = classify_contacts(atoms_csv, contacts_csv)
        n = len(df)
        vc = df['regime'].value_counts()
        row = {
            'case_id': cid,
            'name': name,
            'n_contacts': n,
            'p50_dr': float(df['dr'].quantile(0.5)),
            'p90_dr': float(df['dr'].quantile(0.9)),
            'p99_dr': float(df['dr'].quantile(0.99)),
            'max_dr': float(df['dr'].max()),
        }
        for lbl in CAP_LABELS:
            row[lbl] = float(vc.get(lbl, 0)) / max(n, 1) * 100
        summary_rows.append(row)

        print(f'  {name:32s}  n={n:>7,}  '
              f'p50={row["p50_dr"]:.3f}  '
              f'tabor={row["tabor"]:4.1f}%  '
              f'geom={row["geom"]:4.1f}%  '
              f'liggghts_lb={row["liggghts_lb"]:4.1f}%')

        # per-case CSV always (small)
        csv_path = os.path.join(args.out, f'{name}_regime.csv')
        df.to_csv(csv_path, index=False)
        if not args.no_per_case_plots:
            plot_case(df, name, args.out)

    if summary_rows:
        import pandas as pd
        sdf = pd.DataFrame(summary_rows)
        summary_csv = os.path.join(args.out, 'dataset_summary.csv')
        sdf.to_csv(summary_csv, index=False)
        print(f'\n→ {summary_csv}  ({len(sdf)} cases)')
        if len(sdf) >= 2:
            plot_dataset_summary(sdf, args.out)


if __name__ == '__main__':
    main()
