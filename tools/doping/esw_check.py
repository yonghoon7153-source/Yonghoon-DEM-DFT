#!/usr/bin/env python
"""esw_check.py — Stage 9f: electrochemical stability window (ESW).

Thermodynamic ESW upper / lower bound estimate for each top-K winner
against the most stable competing phases of the constituent elements.

Approach (cheap, screening-grade):
  1. For each element in winner composition, query MP for the most
     stable oxidized phase (higher oxidation state, e.g. P2O5, S → SO3)
     and most stable reduced phase (lower oxidation, e.g. Li2S → Li,
     Cl2 → LiCl).
  2. Estimate ESW = E_oxidation - E_reduction in eV vs Li/Li⁺ proxy.
  3. WARN if ESW is below typical SE window (3-5 V) — the doped
     argyrodite is then expected to react with Li anode or NCM
     cathode at operating voltage.

Limitations (printed at runtime):
  - Pure thermodynamic; kinetic barriers ignored.
  - Pseudobinary phase diagram approximation (Sundar 2025 style).
  - For paper-grade ESW: explicit interface DFT (Stage 11) preferred.

Usage:
  export MP_API_KEY=<key>
  python3 tools/doping/esw_check.py \\
      --ranking $OUT/06_rerank/post_anneal_ranking.json \\
      --anneal_dir $OUT/04_anneal/ \\
      --out $OUT/09f_esw/esw_summary.json --top 10
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking', required=True)
    p.add_argument('--anneal_dir', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--top', type=int, default=10)
    args = p.parse_args()

    api_key = os.environ.get('MP_API_KEY')
    if not api_key:
        print(f"⚠ MP_API_KEY not set — Stage 9f SKIPPED (graceful).")
        print(f"   Free key: https://next-materials-project.org/api")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            'provenance': get_provenance(),
            'skipped': True,
            'reason': 'MP_API_KEY not set',
        }, indent=2))
        return

    try:
        from mp_api.client import MPRester
    except ImportError:
        raise SystemExit("pip install mp-api pymatgen")

    from ase.io import read
    ranking = json.loads(Path(args.ranking).read_text())
    records = ranking.get('ranked_by_post_anneal', [])[:args.top]

    print(f"\n=== Stage 9f ESW thermodynamic bound — top-{args.top} ===")
    print(f"  ⚠ Thermodynamic only — kinetic stability separate.\n")

    rows = []
    with MPRester(api_key) as mpr:
        for i, rec in enumerate(records, 1):
            name = rec['name']
            xyz = Path(args.anneal_dir) / name / 'post_relax.xyz'
            if not xyz.exists():
                continue
            atoms = read(str(xyz))
            elements = sorted(set(atoms.get_chemical_symbols()))
            print(f"  [{i}/{len(records)}] {name}  ({''.join(elements)})", flush=True)

            try:
                entries = mpr.get_entries_in_chemsys(elements)
            except Exception as e:
                rows.append({'name': name, 'error': str(e)})
                continue

            if not entries:
                rows.append({'name': name, 'note': 'no MP entries'})
                continue

            # Cheap proxy: min E/atom across competing phases (lower bound
            # on reduction product stability) and max (oxidation).
            energies = [e.energy_per_atom for e in entries]
            e_lo = min(energies)
            e_hi = max(energies)
            # Pseudo-ESW window (eV/atom span across competing phases).
            # Real ESW vs Li/Li+ would need grand canonical phase
            # diagram (Mo et al. 2012); this is a coarse stability flag.
            esw_eV = float(e_hi - e_lo)

            rows.append({
                'name': name,
                'dopant': rec.get('dopant'),
                'elements': elements,
                'n_competing_phases': len(entries),
                'energy_span_eV_per_atom': esw_eV,
                'min_e_per_atom_eV': e_lo,
                'max_e_per_atom_eV': e_hi,
                'note': ('Coarse proxy: spans of competing-phase '
                         'energies. Not voltage-referenced; for real '
                         'ESW use grand canonical PD (Mo 2012).'),
            })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'config': {'top': args.top},
        'rows': rows,
    }, indent=2, default=str))
    print(f"\n✓ Stage 9f → {out}")


if __name__ == '__main__':
    main()
