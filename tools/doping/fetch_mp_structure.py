#!/usr/bin/env python
"""fetch_mp_structure.py — Download a structure from Materials Project.

Saves both CIF and POSCAR by default. Default target is mp-985592
(Li6PS5Cl cubic F-43m) — note this is the metastable polymorph (see
kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md). For an
accurate ground-state baseline, prefer 48HR or monoclinic Pm relaxed
POSCARs from Pustorino 2025 SI.

Usage:
  # Default: mp-985592 → data/lpscl_bulk.cif
  export MP_API_KEY="your_materials_project_api_key"
  python3 scripts/doping/fetch_mp_structure.py

  # Custom mp-id and output dir
  python3 scripts/doping/fetch_mp_structure.py \\
      --mp_id mp-985592 --out_dir data/ --basename lpscl_bulk

  # Pass API key explicitly
  python3 scripts/doping/fetch_mp_structure.py --api_key XXXX
"""
import argparse
import os
from pathlib import Path


def fetch_mp_structure(mp_id: str, api_key: str):
    """Fetch a pymatgen Structure from Materials Project."""
    try:
        from mp_api.client import MPRester
    except ImportError as e:
        raise ImportError(
            "mp_api not installed. On gabia: `pip install mp-api pymatgen ase`"
        ) from e
    with MPRester(api_key) as mpr:
        docs = mpr.materials.summary.search(material_ids=[mp_id])
        if not docs:
            raise ValueError(f"{mp_id} not found in Materials Project")
        return docs[0].structure


def fetch_mp_doc(mp_id: str, api_key: str) -> dict:
    """fetch_mp_structure plus provenance (2026-11-28 · b2o3_site_dft.py mp_fetch uses it).

    Returns {"structure", "material_id_returned", "formula_pretty", "db_version"}.
    MP is migrating ids — asking for mp-1211324 returned mp-aaacqxxk (CLAUDE.md 2026-09-21) —
    so the caller records both the asked and the returned id.
    Cannot: pick among polymorphs, look at energies, or work without network and a key
    (the key is read by the caller from the environment and never printed here).
    db_version is None when the client cannot report it (recorded as unknown, not guessed).
    """
    try:
        from mp_api.client import MPRester
    except ImportError as e:
        raise ImportError(
            "mp_api not installed. On gabia: /data/apps/miniforge3/envs/uma/bin/python"
        ) from e
    with MPRester(api_key) as mpr:
        docs = mpr.materials.summary.search(material_ids=[mp_id],
                                            fields=["material_id", "structure", "formula_pretty"])
        if not docs:
            raise ValueError(f"{mp_id} not found in Materials Project")
        try:
            ver = mpr.get_database_version()
        except Exception:
            ver = None
        d = docs[0]
        return {"structure": d.structure, "material_id_returned": str(d.material_id),
                "formula_pretty": str(d.formula_pretty), "db_version": None if ver is None else str(ver)}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--mp_id', default='mp-985592',
                       help='Materials Project ID (default: mp-985592 Li6PS5Cl)')
    parser.add_argument('--out_dir', default='data/',
                       help='Output directory (default: data/)')
    parser.add_argument('--basename', default='lpscl_bulk',
                       help='Output basename (default: lpscl_bulk → '
                            'lpscl_bulk.cif + lpscl_bulk.vasp)')
    parser.add_argument('--api_key', default=None,
                       help='MP API key (or set MP_API_KEY env var)')
    parser.add_argument('--formats', nargs='+', default=['cif', 'vasp'],
                       help='Output formats (cif, vasp, xyz)')
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get('MP_API_KEY')
    if not api_key:
        raise SystemExit(
            "MP API key required. Get one at https://next-gen.materialsproject.org/api\n"
            "  export MP_API_KEY='your_key'  # then re-run\n"
            "  or pass --api_key XXXX"
        )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {args.mp_id} from Materials Project...")
    struct = fetch_mp_structure(args.mp_id, api_key)
    print(f"  formula: {struct.composition.reduced_formula}")
    print(f"  space group: {struct.get_space_group_info()}")
    print(f"  {len(struct)} atoms, a={struct.lattice.a:.4f} Å, "
          f"V={struct.volume:.2f} Å³")

    for fmt in args.formats:
        path = out_dir / f"{args.basename}.{fmt}"
        struct.to(filename=str(path))
        print(f"  ✓ {path}")

    if args.mp_id == 'mp-985592':
        print("\n⚠ mp-985592 is the F-43m cubic polymorph — dynamically unstable")
        print("  (imaginary phonons at -146, -115 cm⁻¹; D'Amore 2022).")
        print("  For accurate elastic baselines, relax it first or use the")
        print("  48HR / monoclinic Pm POSCAR from Pustorino 2025 SI.")


if __name__ == '__main__':
    main()
