#!/usr/bin/env python
"""collect_dataset.py — flatten all cascade outputs into a single CSV
suitable for downstream ML training.

Long-term project goal: train an in-house ML predictor that, given a
candidate composition (compound + site combination + concentration),
predicts ΔE_form / B0 / E_young / BVSE_mobility / Li-Li disorder etc.
without running the full UMA+anneal+EOS+elastic chain.

This script is the dataset-collection step. Run once after the cascade
finishes; output dataset.csv is ready for sklearn / xgboost / GNN
training.

Columns (~30 features):

  Structural   composition_Li, composition_P, composition_S, ...,
               n_atoms, volume, lattice_a, lattice_alpha, ...
  Dopant       dopant_class, cation_site, anion_site, x_compound,
               charge_compensation_type
  MLIP-Tier1   ΔE/atom, ΔV/V0
  MLIP-Tier2   li_li_disorder_std, dopant_blocking_fraction,
               lattice_angle_dev_deg
  BVSE         bvs_li_mean, bvs_li_std, migration_volume_fraction
  Post-anneal  ΔE_anneal_meV, post_anneal_E/atom
  EOS          B0_GPa, V0_per_atom, BM3_R²
  Elastic      B_hill, G_hill, E_young, pugh, nu

Usage:
  python3 tools/doping/collect_dataset.py \\
      --cascade_dir runs/tier_2026_05_16/ \\
      --out runs/tier_2026_05_16/dataset.csv
"""
import argparse
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


FEATURE_COLUMNS = [
    'name', 'dopant', 'cation_site', 'anion_site', 'concentration',
    'charge_compensation', 'n_fu_actual',
    # Composition columns added dynamically
    # Tier-1
    'screen_de_per_atom', 'screen_dV_over_V0', 'screen_converged',
    # Tier-2
    'tier2_li_li_disorder_std', 'tier2_li_li_disorder_mean',
    'tier2_dopant_blocking_fraction', 'tier2_lattice_angle_dev_deg',
    'tier2_lattice_aspect_ratio',
    # BVSE
    'bvs_li_mean', 'bvs_li_std', 'bvs_li_proxy_score',
    'migration_volume_fraction', 'li_mobility_score',
    # Anneal
    'anneal_delta_E_meV', 'anneal_E_post_per_atom', 'anneal_dV_pct',
    'anneal_converged',
    # EOS (with fit quality)
    'eos_B0_GPa', 'eos_V0_per_atom', 'eos_Bp', 'eos_r2',
    'eos_fit_quality_ok', 'eos_fit_quality_reason',
    # Elastic
    'elastic_B_hill_GPa', 'elastic_G_hill_GPa', 'elastic_E_young_GPa',
    'elastic_pugh_GoverB', 'elastic_poisson_nu',
    # DT-2 Stage 10 — Li ionic conductivity (paper-essential target)
    'sigma_300K_S_cm_NE', 'sigma_md_Ea_eV', 'sigma_md_D_300K_cm2s',
    'sigma_md_fit_R2', 'sigma_md_n_T_points',
    # DT-2 Stage 11 — NCM cathode adhesion (ranking-only; absolute strain-contaminated)
    'wad_J_m2_mean', 'wad_J_m2_std', 'wad_n_seeds', 'wad_n_lbfgs_ok',
    'wad_ncm_nx', 'wad_area_mismatch_pct',
    # DT-3 quality flags — Layer 2 학습 시 row filter
    'sigma_md_sanity_warnings_count', 'wad_lbfgs_ok_fraction',
    'wad_area_mismatch_severity',     # 'ok' / 'moderate' / 'contaminated'
    # Rerank (post-anneal ΔE)
    'rerank_de_pre_anneal', 'rerank_de_post_anneal',
    'rerank_delta_E_anneal_meV',
    # Combined
    'combined_score', 'rank_combined',
]


def safe_get(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
        if d is None:
            return default
    return d


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--cascade_dir', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()

    cd = Path(args.cascade_dir)

    # Load each stage's records
    def load(rel, key):
        path = cd / rel
        if not path.exists():
            return {}
        d = json.loads(path.read_text())
        records = d.get(key, [])
        if isinstance(records, list):
            return {r.get('name'): r for r in records if r.get('name')}
        return {}

    # v4.5.14: cascade Stage 04/05 swap (anneal first, then BVSE on post-anneal).
    # Pre-v4.5 path layout kept as fallback.
    screen = load('02_screen/uma_results.json', 'results')
    winners = load('03_winners/winners.json', 'winners')
    anneal = load('04_anneal/anneal_results.json', 'results') or \
             load('05_anneal/anneal_results.json', 'results')  # legacy
    bvse = load('05_bvse/bvs_report.json', 'records') or \
           load('04_bvse/bvs_report.json', 'records')         # legacy
    rerank = load('06_rerank/post_anneal_ranking.json',
                  'ranked_by_post_anneal')
    postproc = load('06_postproc/postproc_summary.json', 'records')  # legacy
    eos = load('07_eos/postproc_summary.json', 'records')
    elastic = load('08_elastic/postproc_summary.json', 'records')

    # DT-2 fix: Stage 10 σ_Li MD + Stage 11 NCM Wad — were missing entirely.
    # Stage 10 records use 'name' (winner ID); Stage 11 has separate baselines
    # vs winners lists. We merge winners into the by-name dict; baselines use
    # 'label' key not 'name', so collected separately.
    sigma_md = load('10_md_sigma/sigma_md_summary.json', 'records')
    cathode_winners = load('11_cathode_interface/cathode_interface_summary.json',
                            'winners')

    # Stage 11 baselines (comp1/2/3/4/5/modelC) — label-keyed, not name-keyed.
    cathode_baselines = {}
    cb_path = cd / '11_cathode_interface/cathode_interface_summary.json'
    if cb_path.exists():
        cb_data = json.loads(cb_path.read_text())
        for b in cb_data.get('baselines', []):
            label = b.get('label')
            if label:
                cathode_baselines[label] = b

    # Final ranking (already aggregated)
    final_path = cd / 'FINAL_RANKING.json'
    final_rows = []
    if final_path.exists():
        final_rows = json.loads(final_path.read_text()).get('rows', [])
    final_by_name = {r.get('name'): (i, r) for i, r in enumerate(final_rows, 1)}

    # Union of all names (Stage 10/11 names added — DT-2 fix)
    all_names = (set(screen) | set(winners) | set(bvse) | set(anneal) |
                 set(eos) | set(elastic) | set(postproc) |
                 set(sigma_md) | set(cathode_winners) | set(rerank))
    print(f"Joining {len(all_names)} unique structures")

    # Discover composition keys (Li, P, S, Cl, Nd, Al, ...)
    composition_elements = set()
    for r in screen.values():
        comp = safe_get(r, 'uma_relaxed', 'composition') or {}
        composition_elements.update(comp.keys())
    composition_cols = sorted(f"composition_{el}" for el in composition_elements)

    rows = []
    for name in sorted(all_names):
        s = screen.get(name, {})
        w = winners.get(name, {})
        b = bvse.get(name, {})
        a = anneal.get(name, {})
        e = eos.get(name, postproc.get(name, {}))
        ela = elastic.get(name, postproc.get(name, {}))
        sig = sigma_md.get(name, {})           # DT-2: Stage 10 σ_Li
        cat = cathode_winners.get(name, {})    # DT-2: Stage 11 Wad
        rr = rerank.get(name, {})              # rerank (post-anneal ΔE)
        rank_pair = final_by_name.get(name, (None, {}))

        s_uma = s.get('uma_relaxed', {})
        s_tier2 = s_uma.get('tier2', {})
        sig_arr = sig.get('arrhenius', {}) if isinstance(sig, dict) else {}

        # DT-3: derive quality flags
        sw = sig.get('sanity_warnings', []) if isinstance(sig, dict) else []
        n_sw = len(sw) if isinstance(sw, list) else 0
        n_seeds = cat.get('n_seeds') if cat else None
        n_ok = cat.get('n_lbfgs_ok') if cat else None
        lbfgs_frac = (n_ok / n_seeds) if (n_seeds and n_seeds > 0) else None
        amm = cat.get('area_mismatch_pct') if cat else None
        if amm is None:
            amm_sev = None
        elif amm > 10:
            amm_sev = 'contaminated'
        elif amm > 5:
            amm_sev = 'moderate'
        else:
            amm_sev = 'ok'

        row = {
            'name': name,
            'dopant': s.get('dopant') or w.get('dopant'),
            'cation_site': s.get('site') or w.get('site'),
            'anion_site': s.get('anion_site_label') or w.get('anion_site_label'),
            'concentration': s.get('concentration') or w.get('concentration'),
            'charge_compensation': s.get('charge_compensation') or w.get('charge_compensation'),
            'n_fu_actual': s.get('n_fu_actual'),

            'screen_de_per_atom': s_uma.get('de_per_atom_vs_baseline'),
            'screen_dV_over_V0': s.get('dV_over_V0'),
            'screen_converged': s.get('converged'),

            'tier2_li_li_disorder_std': s_tier2.get('li_li_disorder_std'),
            'tier2_li_li_disorder_mean': s_tier2.get('li_li_disorder_mean'),
            'tier2_dopant_blocking_fraction': s_tier2.get('dopant_blocking_fraction'),
            'tier2_lattice_angle_dev_deg': s_tier2.get('lattice_angle_dev_deg'),
            'tier2_lattice_aspect_ratio': s_tier2.get('lattice_aspect_ratio'),

            'bvs_li_mean': b.get('bvs_li_mean'),
            'bvs_li_std': b.get('bvs_li_std'),
            'bvs_li_proxy_score': b.get('bvs_li_proxy_score'),
            'migration_volume_fraction': b.get('migration_volume_fraction'),
            'li_mobility_score': b.get('li_mobility_score'),

            'anneal_delta_E_meV': a.get('delta_E_anneal_meV_per_atom'),
            'anneal_E_post_per_atom': (a.get('E_post_relax', 0) / a.get('n_atoms', 1)
                                       if a.get('n_atoms') else None),
            'anneal_dV_pct': ((a.get('volume_post', 0) - a.get('volume_pre', 1))
                              / a.get('volume_pre', 1) * 100
                              if a.get('volume_pre') else None),
            'anneal_converged': a.get('converged'),

            'eos_B0_GPa': safe_get(e, 'eos', 'B0_GPa'),
            'eos_V0_per_atom': safe_get(e, 'eos', 'V0_per_atom'),
            'eos_Bp': safe_get(e, 'eos', 'Bp'),
            'eos_r2': safe_get(e, 'eos', 'r2'),
            'eos_fit_quality_ok': safe_get(e, 'eos', 'fit_quality_ok'),
            'eos_fit_quality_reason': safe_get(e, 'eos', 'fit_quality_reason'),

            'elastic_B_hill_GPa': safe_get(ela, 'elastic', 'B_hill_GPa'),
            'elastic_G_hill_GPa': safe_get(ela, 'elastic', 'G_hill_GPa'),
            'elastic_E_young_GPa': safe_get(ela, 'elastic', 'E_young_GPa'),
            'elastic_pugh_GoverB': safe_get(ela, 'elastic', 'pugh_ratio_GoverB'),
            'elastic_poisson_nu': safe_get(ela, 'elastic', 'poisson_nu'),

            # DT-2 Stage 10: σ_Li (paper-essential target)
            'sigma_300K_S_cm_NE': sig_arr.get('sigma_300K_S_cm_NE'),
            'sigma_md_Ea_eV': sig_arr.get('Ea_eV'),
            'sigma_md_D_300K_cm2s': sig_arr.get('D_300K_cm2s'),
            'sigma_md_fit_R2': sig_arr.get('fit_R2'),
            'sigma_md_n_T_points': sig_arr.get('n_T_points_used'),

            # DT-2 Stage 11: NCM Wad (ranking only — absolute strain-contaminated)
            'wad_J_m2_mean': cat.get('Wad_mean_J_m2'),
            'wad_J_m2_std': cat.get('Wad_std_J_m2'),
            'wad_n_seeds': n_seeds,
            'wad_n_lbfgs_ok': n_ok,
            'wad_ncm_nx': cat.get('ncm_nx'),
            'wad_area_mismatch_pct': amm,

            # DT-3 quality flags for Layer 2 row filter
            'sigma_md_sanity_warnings_count': n_sw,
            'wad_lbfgs_ok_fraction': lbfgs_frac,
            'wad_area_mismatch_severity': amm_sev,

            # Rerank (post-anneal ΔE)
            'rerank_de_pre_anneal': rr.get('de_pre_anneal'),
            'rerank_de_post_anneal': rr.get('de_post_anneal'),
            'rerank_delta_E_anneal_meV': rr.get('delta_E_anneal_meV_per_atom'),

            'combined_score': rank_pair[1].get('score_combined'),
            'rank_combined': rank_pair[0],
        }
        # composition counts
        comp = s_uma.get('composition') or {}
        for el in composition_elements:
            row[f'composition_{el}'] = comp.get(el, 0)
        rows.append(row)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    headers = FEATURE_COLUMNS + composition_cols
    with out.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    # Also dump JSON manifest with provenance
    (out.with_suffix('.json')).write_text(json.dumps({
        'provenance': get_provenance(),
        'n_rows': len(rows),
        'columns': headers,
        'cascade_dir': str(cd),
    }, indent=2, default=str))
    print(f"✓ {len(rows)} rows × {len(headers)} cols → {out}")
    print(f"  Provenance manifest → {out.with_suffix('.json')}")
    print(f"\nNext: train predictor with this dataset, e.g.:")
    print(f"  python3 tools/doping/train_predictor.py --csv {out}")


if __name__ == '__main__':
    main()
