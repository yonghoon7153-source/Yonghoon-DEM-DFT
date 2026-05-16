#!/usr/bin/env python
"""combine_rankings.py — chain all pipeline outputs into one unified
multi-axis ranking. The factory line's "final assembly".

Each stage in the cascade contributes one ranking axis:

  Stage 02 (UMA screen):          ΔE/atom vs baseline, ΔV/V₀
  Stage 02 (Tier-2):              Li-Li disorder std, dopant blocking,
                                  lattice angle deviation
  Stage 04 (BVSE):                Li migration volume %, BVS std,
                                  Li mobility proxy score
  Stage 05 (anneal):              ΔE_anneal, post-anneal ΔE/atom
  Stage 07 (EOS):                 B0, V0, fit R²
  Stage 08 (elastic):             B, G, E_young, Pugh G/B, Poisson ν

Outputs unified record per structure with ALL metrics joined by name +
several composite rankings:

  rank_by_stability        — lowest post-anneal ΔE/atom
  rank_by_modulus          — highest E_young
  rank_by_mobility         — highest BVSE proxy score
  rank_combined_paper      — weighted blend (stability + modulus + mobility)

Usage:
  python3 tools/doping/combine_rankings.py \\
      --cascade_dir runs/tier_2026_05_16/ \\
      --out runs/tier_2026_05_16/FINAL_RANKING.json
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# NEW-6 fix: stage path fallback list. v1 cascade: 04=bvse, 05=anneal.
# v2 cascade: 04=anneal, 05=bvse. We try v2 path first, then v1.
STAGE_FILE_CANDIDATES = {
    'screening': [('02_screen/uma_results.json',       'results')],
    'winners':   [('03_winners/winners.json',          'winners')],
    'anneal':    [('04_anneal/anneal_results.json',    'results'),
                  ('05_anneal/anneal_results.json',    'results')],
    'bvse':      [('05_bvse/bvs_report.json',          'records'),
                  ('04_bvse/bvs_report.json',          'records')],
    'rerank':    [('06_rerank/post_anneal_ranking.json',
                                                  'ranked_by_post_anneal')],
    'eos':       [('07_eos/postproc_summary.json',     'records')],
    'elastic':   [('08_elastic/postproc_summary.json', 'records')],
}


def normalize(values, invert=False):
    arr = np.array([v if v is not None else np.nan for v in values],
                   dtype=float)
    if np.all(np.isnan(arr)):
        return [0.5] * len(values)
    lo = np.nanmin(arr); hi = np.nanmax(arr)
    if hi - lo < 1e-12:
        return [0.5] * len(values)
    norm = (arr - lo) / (hi - lo)
    if invert:
        norm = 1 - norm
    return [float(x) if not np.isnan(x) else 0.0 for x in norm]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--cascade_dir', required=True,
                  help='tier_cascade output directory')
    p.add_argument('--out', required=True)
    p.add_argument('--w_stab', type=float, default=0.4,
                  help='Weight: stability (post-anneal ΔE)')
    p.add_argument('--w_mod', type=float, default=0.3,
                  help='Weight: modulus (E_young)')
    p.add_argument('--w_mob', type=float, default=0.3,
                  help='Weight: Li mobility (BVSE proxy)')
    args = p.parse_args()

    cd = Path(args.cascade_dir)
    recs: dict[str, dict] = {}

    # Pass 1: union all records keyed by 'name'. Try each candidate path
    # and use the first that exists (handles v1↔v2 cascade layouts).
    for stage_name, candidates in STAGE_FILE_CANDIDATES.items():
        chosen = None
        for rel_path, key in candidates:
            p = cd / rel_path
            if p.exists():
                chosen = (p, key)
                break
        if chosen is None:
            print(f"  ✗ {stage_name}: no path found "
                  f"(tried {[c[0] for c in candidates]})")
            continue
        path, key = chosen
        d = json.loads(path.read_text())
        records = d.get(key, [])
        if not isinstance(records, list):
            records = []
        for r in records:
            name = r.get('name', None)
            if not name:
                continue
            if name not in recs:
                recs[name] = {'name': name}
            recs[name][f'_{stage_name}'] = r
        print(f"  ✓ {stage_name}: {len(records)} records (from {path.name})")
    print(f"\nJoined: {len(recs)} unique structures")

    # Pass 2: extract per-structure metrics
    rows = []
    for name, blob in recs.items():
        row = {'name': name}
        # ΔE/atom (post-anneal preferred, fallback to screen)
        scr = blob.get('_screening', {}).get('uma_relaxed', {})
        ann = blob.get('_anneal', {})
        if 'E_post_relax' in ann and 'n_atoms' in ann:
            base_E = blob.get('_screening', {}).get('baseline_e_per_atom', None)
            if base_E:
                row['de_per_atom_post_anneal'] = ann['E_post_relax'] / ann['n_atoms'] - base_E
            row['delta_E_anneal_meV'] = ann.get('delta_E_anneal_meV_per_atom', None)
        row['de_per_atom_screen'] = scr.get('de_per_atom_vs_baseline', None)
        row['dV_over_V0'] = blob.get('_screening', {}).get('dV_over_V0', None)
        # Tier-2
        t2 = scr.get('tier2', {})
        row['li_li_disorder_std'] = t2.get('li_li_disorder_std', None)
        row['dopant_blocking_frac'] = t2.get('dopant_blocking_fraction', None)
        # BVSE
        bv = blob.get('_bvse', {})
        row['migration_volume_pct'] = (bv.get('migration_volume_fraction', None) * 100
                                       if bv.get('migration_volume_fraction') is not None
                                       else None)
        row['bvs_li_proxy'] = bv.get('bvs_li_proxy_score', None)
        row['li_mobility_score'] = bv.get('li_mobility_score', None)
        # EOS
        eos = blob.get('_eos', {}).get('eos', {})
        row['B0_GPa'] = eos.get('B0_GPa', None)
        row['V0_per_atom'] = eos.get('V0_per_atom', None)
        # Elastic
        ela = blob.get('_elastic', {}).get('elastic', {})
        row['E_young_GPa'] = ela.get('E_young_GPa', None)
        row['B_hill_GPa'] = ela.get('B_hill_GPa', None)
        row['G_hill_GPa'] = ela.get('G_hill_GPa', None)
        row['pugh_ratio'] = ela.get('pugh_ratio_GoverB', None)
        row['poisson_nu'] = ela.get('poisson_nu', None)
        rows.append(row)

    # Composite axis scores (min-max normalized)
    de_axis = [r.get('de_per_atom_post_anneal') or r.get('de_per_atom_screen') for r in rows]
    de_norm = normalize(de_axis, invert=True)  # lower ΔE = higher score
    mod_norm = normalize([r.get('E_young_GPa') for r in rows], invert=False)
    mob_norm = normalize([r.get('li_mobility_score') for r in rows], invert=False)

    for r, ds, ms, mb in zip(rows, de_norm, mod_norm, mob_norm):
        r['score_stability'] = ds
        r['score_modulus'] = ms
        r['score_mobility'] = mb
        r['score_combined'] = (args.w_stab * ds
                              + args.w_mod * ms
                              + args.w_mob * mb)

    # Sort by combined
    rows.sort(key=lambda r: -r['score_combined'])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'weights': {'stability': args.w_stab, 'modulus': args.w_mod,
                    'mobility': args.w_mob},
        'n_structures': len(rows),
        'rows': rows,
    }, indent=2, default=str))

    # Top-20 table
    print(f"\n{'='*110}")
    print(f"  TOP-20 — combined paper score (stab×{args.w_stab} + mod×{args.w_mod} + mob×{args.w_mob})")
    print(f"{'='*110}")
    print(f"{'Rank':<5}{'Name':<40}{'ΔE/at':>8}{'V_mig%':>8}{'B0':>8}{'E_y':>8}{'Pugh':>7}"
          f"{'comb':>8}")
    for i, r in enumerate(rows[:20], 1):
        de = r.get('de_per_atom_post_anneal') or r.get('de_per_atom_screen') or 0
        vmig = r.get('migration_volume_pct') or 0
        b0 = r.get('B0_GPa') or 0
        ey = r.get('E_young_GPa') or 0
        pg = r.get('pugh_ratio') or 0
        print(f"{i:<5}{r['name'][:38]:<40}"
              f"{de:>+7.3f} {vmig:>6.2f}% {b0:>7.1f} {ey:>7.1f} "
              f"{pg:>6.3f} {r['score_combined']:>7.3f}")
    print(f"\n✓ {len(rows)} structures → {out}")


if __name__ == '__main__':
    main()
