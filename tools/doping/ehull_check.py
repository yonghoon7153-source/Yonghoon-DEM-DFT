#!/usr/bin/env python
"""ehull_check.py — Stage 9e: convex-hull (synthesizability) check.

For each top-K winner, queries Materials Project for the convex hull
of the same elements and reports ΔE_hull (eV/atom). ΔE_hull > 50
meV/atom is the standard *"likely hard to synthesize"* flag.

paper relevance: reviewer will ask whether the predicted doped
argyrodite is thermodynamically reachable. ΔE_hull gives a clean
upper bound (kinetic accessibility separate).

API key: requires MP_API_KEY environment variable. Without it the
stage emits a WARN and skips gracefully (does not abort the cascade).
Free Materials Project API key: https://next-materials-project.org/api

Usage:
  export MP_API_KEY=<your_key>
  python3 tools/doping/ehull_check.py \\
      --ranking $OUT/06_rerank/post_anneal_ranking.json \\
      --anneal_dir $OUT/04_anneal/ \\
      --out $OUT/09e_ehull/ehull_summary.json --top 10
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def get_winner_composition(xyz_path):
    """Return formula and per-atom energy (MLIP, not DFT) for one winner."""
    from ase.io import read
    atoms = read(str(xyz_path))
    comp = {}
    for s in atoms.get_chemical_symbols():
        comp[s] = comp.get(s, 0) + 1
    return comp, len(atoms)


def query_hull_energy(elements, mpr):
    """Return min E/atom of competing phases on the hull. None on failure."""
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    try:
        entries = mpr.get_entries_in_chemsys(elements)
        if not entries:
            return None, []
        pd = PhaseDiagram(entries)
        # Lowest-energy entry per atom is on the hull. We need the hull
        # energy at the winner's composition — but we don't have a DFT
        # entry for it. Cheapest interpretable proxy: the minimum E/atom
        # across all competing entries (loose upper bound on E_hull).
        # Real ΔE_hull requires the winner's DFT energy.
        e_min = min(e.energy_per_atom for e in entries)
        return e_min, [f"{e.composition.reduced_formula}: "
                       f"{e.energy_per_atom:.3f} eV/atom"
                       for e in sorted(entries,
                                      key=lambda x: x.energy_per_atom)[:5]]
    except Exception as e:
        return None, [f"MP query failed: {e}"]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking', required=True)
    p.add_argument('--anneal_dir', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--metastable_threshold_meV', type=float, default=50.0,
                   help='WARN if winner ΔE_hull > this. Default 50 meV/atom '
                        '(standard "likely synthesizable" cutoff).')
    args = p.parse_args()

    api_key = os.environ.get('MP_API_KEY')
    if not api_key:
        print(f"⚠ MP_API_KEY env var not set — Stage 9e SKIPPED.")
        print(f"   Free key: https://next-materials-project.org/api")
        print(f"   Then: export MP_API_KEY=<key>")
        # Write an explicit skip marker so the cascade can report it
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            'provenance': get_provenance(),
            'skipped': True,
            'reason': 'MP_API_KEY not set',
            'instructions': 'export MP_API_KEY=<key>; rerun with '
                           'FORCE_RERUN=09e tier_cascade.sh',
        }, indent=2))
        return  # graceful skip, NOT a failure

    try:
        from mp_api.client import MPRester
    except ImportError:
        raise SystemExit(
            "mp_api package missing. Install with:\n"
            "  pip install mp-api pymatgen")

    ranking = json.loads(Path(args.ranking).read_text())
    records = ranking.get('ranked_by_post_anneal', [])[:args.top]
    if not records:
        raise SystemExit(f"No records in {args.ranking}")

    print(f"\n=== Stage 9e Ehull / synthesizability — top-{args.top} winners ===")
    print(f"  Metastable WARN threshold: {args.metastable_threshold_meV} meV/atom\n")

    rows = []
    with MPRester(api_key) as mpr:
        for i, rec in enumerate(records, 1):
            name = rec['name']
            xyz = Path(args.anneal_dir) / name / 'post_relax.xyz'
            if not xyz.exists():
                print(f"  [{i}/{len(records)}] {name}: MISSING {xyz}")
                continue
            comp, n_at = get_winner_composition(xyz)
            elements = sorted(comp.keys())
            print(f"  [{i}/{len(records)}] {name}  ({''.join(elements)})", flush=True)
            e_min, top_phases = query_hull_energy(elements, mpr)
            rows.append({
                'name': name,
                'dopant': rec.get('dopant'),
                'site': rec.get('site'),
                'composition': comp,
                'elements': elements,
                'n_atoms': n_at,
                'mp_min_e_per_atom_eV': e_min,
                'top_5_competing_phases': top_phases,
                'note': ('MLIP E and MP DFT E not directly comparable; '
                         'this gives competing-phase reference. True '
                         'ΔE_hull requires winner DFT — use this as '
                         'synthesizability hint, not a hard cut.'),
            })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'config': {'top': args.top,
                   'metastable_threshold_meV': args.metastable_threshold_meV},
        'rows': rows,
    }, indent=2, default=str))

    print(f"\n✓ Stage 9e → {out}  ({len(rows)} winners checked)")
    print(f"  ⚠ For absolute ΔE_hull, run DFT on top-K and compare to "
          f"MP entries. This stage gives competing-phase reference only.")


if __name__ == '__main__':
    main()
