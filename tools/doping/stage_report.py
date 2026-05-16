#!/usr/bin/env python
"""stage_report.py — generate per-stage human-readable markdown reports.

User wants to inspect each stage's output as it finishes, discuss with
me critically + look up more literature. So after every stage in
tier_cascade, this tool reads that stage's JSON and produces
STAGE_NN_REPORT.md with: summary stats, distributions, top entries,
known-issue flags, suggested follow-ups.

Usage (called by tier_cascade.sh automatically):
  python3 tools/doping/stage_report.py --stage 02 --cascade_dir runs/tier_2026_05_16/
"""
import argparse
import json
import statistics
from pathlib import Path
from collections import Counter, defaultdict
import sys

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def histogram(values, n_bins=10, label='value'):
    """Return ASCII histogram as multi-line string."""
    if not values:
        return "(no data)"
    vmin, vmax = min(values), max(values)
    if vmin == vmax:
        return f"all values = {vmin:.4g} ({len(values)} records)"
    bins = [0] * n_bins
    width = (vmax - vmin) / n_bins
    for v in values:
        idx = min(int((v - vmin) / width), n_bins - 1)
        bins[idx] += 1
    max_count = max(bins)
    lines = []
    for i, c in enumerate(bins):
        bin_lo = vmin + i * width
        bar = '█' * int(40 * c / max_count) if max_count > 0 else ''
        lines.append(f"  {bin_lo:+9.3g}: {bar} {c}")
    return '\n'.join(lines)


def stats_block(values, label):
    if not values:
        return f"- {label}: no data\n"
    if len(values) == 1:
        return f"- {label}: single value = {values[0]:.4g}\n"
    return (f"- {label}: n={len(values)}, "
            f"mean={statistics.mean(values):+.4g}, "
            f"std={statistics.stdev(values):.4g}, "
            f"min={min(values):+.4g}, max={max(values):+.4g}\n")


def report_00_preflight(cd: Path) -> str:
    path = cd / '00_preflight' / 'preflight_report.json'
    if not path.exists():
        return "# Stage 00 — preflight\n\n(no report file)\n"
    d = json.loads(path.read_text())
    s = d.get('summary', {})
    md = [
        "# Stage 00 — Preflight (sanity checks)",
        "",
        f"**{s.get('pass', '?')}/{s.get('total', '?')} checks passed**",
        "",
    ]
    for key in ('tools_present', 'disk_space', 'uma_load', 'baseline_relax'):
        entry = d.get(key, {})
        ok = '✓' if entry.get('ok') else '✗'
        md.append(f"- [{ok}] **{key}**: {entry.get('detail', '?')}")
    if 'baseline_relax' in d:
        br = d['baseline_relax'].get('detail', {})
        if isinstance(br, dict):
            md.append("")
            md.append("## Baseline relax details")
            md.append(f"- E/atom: {br.get('e_per_atom_eV', '?')} eV")
            md.append(f"- |ΔV/V0|: {br.get('dV_rel', 0)*100:.2f}%")
            md.append(f"- PS4 integrity (per P): {br.get('p_s_neighbors_per_P', '?')}")
            md.append(f"- relax steps: {br.get('converged_n_steps', '?')}")
            if br.get('issues'):
                md.append("- ⚠ issues:")
                for iss in br['issues']:
                    md.append(f"  - {iss}")
    return '\n'.join(md) + '\n'


def report_01_substitute(cd: Path) -> str:
    path = cd / '01_structures' / 'structures_summary.json'
    if not path.exists():
        return "# Stage 01 — substitute\n\n(no summary)\n"
    d = json.loads(path.read_text())
    structs = d.get('structures', [])
    by_dop = Counter(s.get('dopant', '?') for s in structs)
    by_csite = Counter(s.get('cation_site_used', s.get('site', '?')) for s in structs)
    by_asite = Counter(s.get('anion_site_used', s.get('anion_site_label', '?'))
                      for s in structs)
    md = [
        "# Stage 01 — Compound substitution batch",
        "",
        f"**{len(structs)} structures generated**",
        "",
        f"## By compound (top 20)",
    ]
    for k, v in by_dop.most_common(20):
        md.append(f"  - {k:25s} {v}")
    md.append("")
    md.append("## By cation site")
    for k, v in by_csite.most_common():
        md.append(f"  - {k:15s} {v}")
    md.append("")
    md.append("## By anion site")
    for k, v in by_asite.most_common():
        md.append(f"  - {k:15s} {v}")
    return '\n'.join(md) + '\n'


def report_02_screen(cd: Path) -> str:
    path = cd / '02_screen' / 'uma_results.json'
    if not path.exists():
        return "# Stage 02 — UMA screen\n\n(no results)\n"
    d = json.loads(path.read_text())
    results = d.get('results', [])
    if not results:
        return "# Stage 02 — UMA screen\n\n(empty results)\n"

    n_conv = sum(1 for r in results if r.get('converged'))
    n_outlier = sum(1 for r in results
                   if r.get('uma_relaxed', {}).get('outlier_flag'))
    des = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in results
           if 'uma_relaxed' in r]
    dvs = [r.get('dV_over_V0', 0) * 100 for r in results
           if r.get('dV_over_V0') is not None]
    md = [
        "# Stage 02 — UMA screening (Tier 1+2)",
        "",
        f"- **{len(results)} structures**, {n_conv} converged ({n_conv/len(results)*100:.0f}%)",
        f"- {n_outlier} flagged as outlier (|ΔV|>30% or |ΔE|>5 eV/atom)",
        "",
        stats_block(des, 'ΔE/atom vs baseline (eV)'),
        stats_block(dvs, 'ΔV/V₀ (%)'),
        "",
        "## ΔE/atom distribution (ascending)",
        '```',
        histogram(des),
        '```',
        "",
        "## ΔV/V₀ distribution (%)",
        '```',
        histogram(dvs),
        '```',
        "",
        "## Top 10 most stable (lowest ΔE/atom)",
    ]
    sorted_r = sorted([r for r in results if 'uma_relaxed' in r],
                     key=lambda r: r['uma_relaxed']['de_per_atom_vs_baseline'])
    for i, r in enumerate(sorted_r[:10], 1):
        u = r['uma_relaxed']
        md.append(f"  {i:>2}. {r.get('name', '?')[:40]:<40} "
                 f"ΔE={u['de_per_atom_vs_baseline']:+.4f} "
                 f"ΔV={r.get('dV_over_V0', 0)*100:+.2f}%")
    return '\n'.join(md) + '\n'


def report_03_winners(cd: Path) -> str:
    path = cd / '03_winners' / 'winners.json'
    if not path.exists():
        return "# Stage 03 — winners\n\n(no winners.json)\n"
    d = json.loads(path.read_text())
    w = d.get('winners', [])
    md = [
        "# Stage 03 — Per-group winners",
        "",
        f"- **{len(w)} groups**, one winner per (compound, cation_site, anion_site)",
        f"- Top-1 of each group passed forward to anneal + post-processing",
        "",
        "## Top 20 winners (by metric)",
    ]
    for i, ww in enumerate(w[:20], 1):
        grp = '/'.join(str(v) for v in ww.get('group_key', {}).values())
        md.append(f"  {i:>2}. {grp[:50]:<50} "
                 f"min={ww.get('group_metric_min', 0):+.4f} "
                 f"spread={ww.get('group_metric_spread', 0):+.4f} "
                 f"(n={ww.get('n_in_group', 0)})")
    return '\n'.join(md) + '\n'


def report_bvse(cd: Path) -> str:
    """BVSE report — path varies by cascade version (v1: 04_bvse, v2: 05_bvse)."""
    for sub in ('04_bvse', '05_bvse'):
        path = cd / sub / 'bvs_report.json'
        if path.exists():
            break
    else:
        return "# BVSE\n\n(no report)\n"
    if not path.exists():
        return "# Stage 04 — BVSE\n\n(no report)\n"
    d = json.loads(path.read_text())
    recs = d.get('records', [])
    bvs_mean = [r['bvs_li_mean'] for r in recs if 'bvs_li_mean' in r]
    mig = [r.get('migration_volume_fraction', 0) * 100 for r in recs
           if 'migration_volume_fraction' in r]
    md = [
        "# Stage 04 — BVSE Li mobility proxy",
        "",
        f"- **{len(recs)} structures**",
        stats_block(bvs_mean, '⟨BVS⟩ per Li'),
        stats_block(mig, 'Migration accessible volume (%)'),
        "",
        "## BVS distribution",
        '```',
        histogram(bvs_mean, label='BVS'),
        '```',
        "",
        "## Migration volume distribution (%)",
        '```',
        histogram(mig, label='%'),
        '```',
        "",
        "## Top 20 by Li mobility score",
    ]
    ok = [r for r in recs if 'li_mobility_score' in r]
    ok.sort(key=lambda r: -r['li_mobility_score'])
    for i, r in enumerate(ok[:20], 1):
        md.append(f"  {i:>2}. {r['name'][:40]:<40} "
                 f"⟨BVS⟩={r['bvs_li_mean']:.3f} σ={r['bvs_li_std']:.3f} "
                 f"V_mig={r['migration_volume_fraction']*100:.1f}% "
                 f"score={r['li_mobility_score']:.3f}")
    return '\n'.join(md) + '\n'


def report_anneal(cd: Path) -> str:
    """Anneal report — path varies (v1: 05_anneal, v2: 04_anneal)."""
    for sub in ('04_anneal', '05_anneal'):
        path = cd / sub / 'anneal_results.json'
        if path.exists():
            break
    else:
        return "# Anneal\n\n(no report)\n"
    if not path.exists():
        return "# Stage 05 — anneal\n\n(no results)\n"
    d = json.loads(path.read_text())
    rs = d.get('results', [])
    des = [r['delta_E_anneal_meV_per_atom'] for r in rs
           if 'delta_E_anneal_meV_per_atom' in r]
    md = [
        "# Stage 05 — Light anneal (300K, 20ps)",
        "",
        f"- **{len(rs)} winners annealed**",
        stats_block(des, 'ΔE_anneal (meV/atom)'),
        "",
        "## ΔE_anneal distribution",
        "(negative = anneal found deeper basin; positive = local min escape)",
        '```',
        histogram(des, label='meV'),
        '```',
        "",
        "## Most-stabilized after anneal (lowest ΔE_anneal)",
    ]
    sorted_r = sorted([r for r in rs if 'delta_E_anneal_meV_per_atom' in r],
                     key=lambda r: r['delta_E_anneal_meV_per_atom'])
    for i, r in enumerate(sorted_r[:10], 1):
        md.append(f"  {i:>2}. {r['name'][:40]:<40} "
                 f"ΔE_anneal={r['delta_E_anneal_meV_per_atom']:+.1f} meV/atom")
    return '\n'.join(md) + '\n'


def report_07_eos(cd: Path) -> str:
    path = cd / '07_eos' / 'postproc_summary.json'
    if not path.exists():
        return "# Stage 07 — EOS\n\n(no summary)\n"
    d = json.loads(path.read_text())
    rs = d.get('records', [])
    b0s = [r['eos']['B0_GPa'] for r in rs
           if 'eos' in r and 'B0_GPa' in r['eos']]
    r2s = [r['eos']['r2'] for r in rs if 'eos' in r and 'r2' in r['eos']]
    md = [
        "# Stage 07 — MLIP EOS (B0, V0 via 3rd-order Birch-Murnaghan)",
        "",
        f"- **{len(rs)} EOS fits attempted**",
        stats_block(b0s, 'B₀ (GPa)'),
        stats_block(r2s, 'BM3 fit R²'),
        "",
        "## B₀ distribution (GPa)",
        '```',
        histogram(b0s),
        '```',
        "",
        "## Highest B₀ (most rigid)",
    ]
    sorted_r = sorted([r for r in rs if 'eos' in r and 'B0_GPa' in r['eos']],
                     key=lambda r: -r['eos']['B0_GPa'])
    for i, r in enumerate(sorted_r[:10], 1):
        md.append(f"  {i:>2}. {r['name'][:40]:<40} "
                 f"B₀={r['eos']['B0_GPa']:.2f} GPa "
                 f"R²={r['eos']['r2']:.4f}")
    return '\n'.join(md) + '\n'


def report_08_elastic(cd: Path) -> str:
    path = cd / '08_elastic' / 'postproc_summary.json'
    if not path.exists():
        return "# Stage 08 — elastic\n\n(no summary)\n"
    d = json.loads(path.read_text())
    rs = d.get('records', [])
    eys = [r['elastic']['E_young_GPa'] for r in rs
           if 'elastic' in r and r['elastic'].get('E_young_GPa')]
    pus = [r['elastic']['pugh_ratio_GoverB'] for r in rs
           if 'elastic' in r and r['elastic'].get('pugh_ratio_GoverB')]
    md = [
        "# Stage 08 — MLIP elastic constants (finite strain)",
        "",
        f"- **{len(rs)} elastic calcs**",
        stats_block(eys, 'E_young (GPa)'),
        stats_block(pus, 'Pugh G/B (>0.57 brittle, <0.57 ductile)'),
        "",
        "## E_young distribution (GPa)",
        '```',
        histogram(eys),
        '```',
        "",
        "## Top 10 by Young's modulus",
    ]
    sorted_r = sorted([r for r in rs
                      if 'elastic' in r and r['elastic'].get('E_young_GPa')],
                     key=lambda r: -r['elastic']['E_young_GPa'])
    for i, r in enumerate(sorted_r[:10], 1):
        e = r['elastic']
        md.append(f"  {i:>2}. {r['name'][:40]:<40} "
                 f"E={e['E_young_GPa']:.1f} GPa "
                 f"B_h={e.get('B_hill_GPa', 0):.1f} G_h={e.get('G_hill_GPa', 0):.1f} "
                 f"ν={e.get('poisson_nu', 0):.3f} Pugh={e.get('pugh_ratio_GoverB', 0):.3f}")
    return '\n'.join(md) + '\n'


def report_09_final(cd: Path) -> str:
    path = cd / 'FINAL_RANKING.json'
    if not path.exists():
        return "# Stage 09 — final\n\n(FINAL_RANKING.json missing)\n"
    d = json.loads(path.read_text())
    rows = d.get('rows', [])
    weights = d.get('weights', {})
    md = [
        "# Stage 09 — FINAL ranking (combined multi-axis score)",
        "",
        f"- **{len(rows)} structures ranked**",
        f"- Weights: stability={weights.get('stability', 0):.2f}, "
        f"modulus={weights.get('modulus', 0):.2f}, "
        f"mobility={weights.get('mobility', 0):.2f}",
        "",
        "## Top 20 paper candidates",
    ]
    for i, r in enumerate(rows[:20], 1):
        md.append(f"  {i:>2}. {r['name'][:38]:<38} "
                 f"ΔE={r.get('de_per_atom_post_anneal') or r.get('de_per_atom_screen', 0):+.4f} "
                 f"V_mig={r.get('migration_volume_pct', 0):.1f}% "
                 f"B0={r.get('B0_GPa') or 0:.1f} GPa "
                 f"E={r.get('E_young_GPa') or 0:.1f} GPa "
                 f"comb={r.get('score_combined', 0):.3f}")
    md.extend([
        "",
        "## Next steps suggested:",
        "1. Top-10 candidates → DFT spot-check via tools/doping/generate_dft_inputs.py",
        "2. Compare top dopant identities against literature (Pham 2021, Sundar 2025, etc.)",
        "3. Train predictor for future cold-start screening: train_predictor.py",
        "4. Critical literature search per top candidate (positive/negative control).",
    ])
    return '\n'.join(md) + '\n'


REPORT_HANDLERS = {
    '00': report_00_preflight,
    '01': report_01_substitute,
    '02': report_02_screen,
    '03': report_03_winners,
    # v2 cascade: 04=anneal, 05=bvse; v1 was swapped. handlers auto-detect path.
    '04': report_anneal,
    '05': report_bvse,
    '07': report_07_eos,
    '08': report_08_elastic,
    '09': report_09_final,
}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--cascade_dir', required=True)
    p.add_argument('--stage', default='all',
                  help="Stage ID (00, 01, ..., 09) or 'all' to write every "
                       "available report.")
    args = p.parse_args()

    cd = Path(args.cascade_dir)
    cd.mkdir(parents=True, exist_ok=True)

    stages = ([args.stage] if args.stage != 'all'
              else sorted(REPORT_HANDLERS.keys()))
    for s in stages:
        if s not in REPORT_HANDLERS:
            print(f"  no handler for stage {s}")
            continue
        md = REPORT_HANDLERS[s](cd)
        report_path = cd / f'STAGE_{s}_REPORT.md'
        report_path.write_text(md)
        print(f"  ✓ stage {s} → {report_path}")


if __name__ == '__main__':
    main()
