#!/usr/bin/env python3
"""E_above_hull (convex-hull stability) for a doped argyrodite.

Two modes:
  --mode uma  (DEFAULT, self-consistent): UMA single-points OUR structure AND
      every MP competing phase in the chemsys, builds the PhaseDiagram from
      those UMA energies -> internally consistent E_above_hull. UMA(omat) is one
      method for everything, so the number is meaningful (no QE-vs-MP mixing).
  --mode mp   (fast, products only): builds the hull from MP energies and reports
      what OUR composition decomposes into + the hull energy at that composition.
      Does NOT give our structure's absolute E_above_hull (would need an
      MP-compatible energy for it), but the decomposition PRODUCTS are robust.

Needs: pymatgen, mp_api, MP_API_KEY env; for --mode uma also fairchem + a GPU.
Run on gabia (has the oxidation env + internet + UMA).

  MP_API_KEY=... python3 tools/doping/convex_hull_ehull.py \
      --cif db/structures/b2o3_relaxV0.cif --mode uma --device cuda \
      --out /data/work/runs/b2o3_ehull/ehull_uma.json
"""
import argparse, os, json
from pathlib import Path


def get_mp_entries(elements, key):
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        try:
            ents = mpr.get_entries_in_chemsys(elements, inc_structure=True)
        except TypeError:
            ents = mpr.get_entries_in_chemsys(elements)   # older client
    return ents


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", required=True)
    ap.add_argument("--elements", nargs="+",
                    default=["Li", "P", "S", "Cl", "B", "O"])
    ap.add_argument("--mode", choices=["uma", "mp"], default="uma")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--out", default="ehull_result.json")
    args = ap.parse_args()
    key = os.environ.get("MP_API_KEY")
    if not key:
        raise SystemExit("set MP_API_KEY env var")

    from pymatgen.core import Structure
    from pymatgen.entries.computed_entries import ComputedEntry
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    ours = Structure.from_file(args.cif)
    comp = ours.composition
    print(f"our composition: {comp.reduced_formula}  ({comp.formula})")
    mp_entries = get_mp_entries(args.elements, key)
    print(f"MP entries in {'-'.join(args.elements)}: {len(mp_entries)}")

    result = {"cif": args.cif, "composition": comp.formula,
              "reduced": comp.reduced_formula, "elements": args.elements,
              "mode": args.mode, "n_mp_entries": len(mp_entries)}

    if args.mode == "uma":
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        from pymatgen.io.ase import AseAtomsAdaptor
        pred = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
        calc = FAIRChemCalculator(pred, task_name="omat")
        ad = AseAtomsAdaptor()

        def uma_E(struct):
            at = ad.get_atoms(struct); at.calc = calc
            return float(at.get_potential_energy())

        entries, skipped = [], 0
        for e in mp_entries:
            st = getattr(e, "structure", None)
            if st is None:
                skipped += 1; continue
            try:
                entries.append(ComputedEntry(st.composition, uma_E(st)))
            except Exception:
                skipped += 1
        our_E = uma_E(ours)
        our_entry = ComputedEntry(comp, our_E)
        pd = PhaseDiagram(entries + [our_entry])
        eah = pd.get_e_above_hull(our_entry)            # eV/atom
        decomp = pd.get_decomposition(comp)
        result.update({
            "uma_model": args.uma_model,
            "n_uma_entries": len(entries), "skipped": skipped,
            "our_E_eV": our_E, "our_E_per_atom": our_E / len(ours),
            "E_above_hull_eV_per_atom": eah,
            "on_hull": bool(eah < 1e-3),
            "decomposition": {d.composition.reduced_formula: round(amt, 4)
                              for d, amt in decomp.items()},
            "note": "UMA(omat)-consistent hull: our structure + all MP phases "
                    "single-pointed with UMA. E_above_hull is internally "
                    "consistent (MLIP, not DFT-absolute).",
        })
        print(f"\nE_above_hull = {eah*1000:.1f} meV/atom  "
              f"({'ON HULL / stable' if eah < 1e-3 else 'metastable'})")
        print("decomposes into:", result["decomposition"])
    else:
        pd = PhaseDiagram(mp_entries)
        decomp = pd.get_decomposition(comp)
        hull_e = pd.get_hull_energy(comp)
        result.update({
            "hull_energy_eV": float(hull_e),
            "hull_energy_per_atom": float(hull_e) / comp.num_atoms,
            "decomposition_products": {d.composition.reduced_formula: round(amt, 4)
                                       for d, amt in decomp.items()},
            "note": "MP-energy hull. Products + hull energy at our composition. "
                    "Absolute E_above_hull of OUR structure needs an MP-compatible "
                    "energy (use --mode uma for a self-consistent number).",
        })
        print("\nMP-hull decomposition products at our composition:")
        print(result["decomposition_products"])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
