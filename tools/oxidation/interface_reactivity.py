#!/usr/bin/env python3
"""interface_reactivity.py — Electrolyte/cathode (and electrolyte/carbon)
mutual reaction energy via pymatgen InterfacialReactivity (Richards/Ong 2016,
Chem. Mater. 28, 266).

Purpose
-------
Our intrinsic bulk grand-potential ESW (esw_grand_potential.py) found comp1
(LPSCl) and modelc (LPSCl1.6) have an IDENTICAL oxidation onset (~2.1 V,
S2--limited) — yet experiment (Zuo et al., Angew 2023) shows the higher-Cl
phase is LESS stable in real cells, with WORSE cathode/carbon interface
decomposition. That penalty lives in the INTERFACE reaction (not the bulk
single-phase window). This tool computes the interface descriptor that should
reproduce the experimental trend: the maximum mutual reaction energy (most
exothermic, eV/atom) between the electrolyte and a contacting phase.

  more negative reaction energy  ==  more reactive interface  ==  less stable.

If modelc shows a MORE negative reaction energy with LiCoO2 / C than comp1, we
reproduce Zuo 2023 with our own calc — closing the intrinsic-bulk-vs-interface
gap quantitatively.

use_hull_energy=True places BOTH electrolyte compositions at the MP convex-hull
energy of their composition (consistent for comp1 in-MP and modelc non-MP),
the same footing as our ESW calc.

Usage (gabia/kserver116-27, MP_API_KEY set; CPU only):
    python3 interface_reactivity.py \
        --electrolytes "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --contacts LiCoO2 C \
        --out interface_reactivity_results.json
"""
import argparse
import json
import os
from pathlib import Path


def get_chemsys_entries(elements):
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    print(f"[mp_api] {len(entries)} entries in {'-'.join(sorted(elements))}")
    return entries


def reaction_descriptor(c1, c2, pd):
    """Return (min_energy_eV_per_atom, reaction_str, all_kinks)."""
    from pymatgen.analysis.interface_reactions import InterfacialReactivity
    ir = InterfacialReactivity(c1, c2, pd, use_hull_energy=True)
    kinks = ir.get_kinks()  # list of (index, x, energy, reaction, e_hull)
    rows = []
    min_e = 1e9
    min_rxn = None
    for k in kinks:
        # tuple layout: (index, x, react_energy_per_atom, Reaction, e_above_hull)
        idx, x, e, rxn = k[0], k[1], k[2], k[3]
        rows.append({"x_atomic_frac": round(float(x), 4),
                     "reaction_energy_eV_per_atom": round(float(e), 5),
                     "reaction": str(rxn)})
        if float(e) < min_e:
            min_e = float(e)
            min_rxn = str(rxn)
    return min_e, min_rxn, rows


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--electrolytes", nargs="+", required=True,
                    help='comp:label, e.g. "Li6PS5Cl:comp1" '
                         '"Li5.4P1S4.4Cl1.6:modelc"')
    ap.add_argument("--contacts", nargs="+", default=["LiCoO2", "C"],
                    help="contacting phases (cathode / carbon)")
    ap.add_argument("--out", default="interface_reactivity_results.json")
    args = ap.parse_args()

    from pymatgen.core import Composition
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    # union chemsys = electrolyte elements + all contact elements
    elems = set()
    for spec in args.electrolytes:
        elems |= set(Composition(spec.split(":")[0]).elements)
    for c in args.contacts:
        elems |= set(Composition(c).elements)
    elements = sorted(e.symbol for e in elems)
    print(f"chemsys = {elements}")

    entries = get_chemsys_entries(elements)
    pd = PhaseDiagram(entries)

    results = {}
    for contact in args.contacts:
        c_contact = Composition(contact)
        results[contact] = {}
        print(f"\n######## contact = {contact} ########")
        for spec in args.electrolytes:
            comp_str, _, label = spec.partition(":")
            label = label or comp_str
            c_el = Composition(comp_str)
            try:
                min_e, min_rxn, rows = reaction_descriptor(c_el, c_contact, pd)
                print(f"  {label:8s} vs {contact}: "
                      f"min ΔE_rxn = {min_e:.4f} eV/atom")
                print(f"      reaction: {min_rxn}")
                results[contact][label] = {
                    "electrolyte": comp_str,
                    "min_reaction_energy_eV_per_atom": round(min_e, 5),
                    "most_exothermic_reaction": min_rxn,
                    "all_kinks": rows,
                }
            except Exception as e:
                print(f"  {label} vs {contact}: ERROR {type(e).__name__}: {e}")
                results[contact][label] = {"error": str(e)}

    # comparison summary per contact
    summary = {}
    for contact, d in results.items():
        pair = {k: v.get("min_reaction_energy_eV_per_atom")
                for k, v in d.items() if "min_reaction_energy_eV_per_atom" in v}
        if len(pair) == 2:
            (la, ea), (lb, eb) = list(pair.items())
            more_reactive = la if ea < eb else lb
            summary[contact] = {
                "energies_eV_per_atom": pair,
                "more_reactive_interface": more_reactive,
                "delta_eV_per_atom": round(abs(ea - eb), 5),
            }

    Path(args.out).write_text(json.dumps({
        "method": "pymatgen InterfacialReactivity (Richards/Ong 2016), "
                  "use_hull_energy=True, MP GGA_GGA+U hull. Reaction energy "
                  "per atom; more negative = more reactive interface = less stable.",
        "chemsys": elements,
        "results": results,
        "comparison_summary": summary,
    }, indent=2))
    print(f"\n=== comparison summary ===")
    for contact, s in summary.items():
        print(f"  {contact}: {s['energies_eV_per_atom']} -> "
              f"MORE reactive: {s['more_reactive_interface']} "
              f"(Δ {s['delta_eV_per_atom']} eV/atom)")
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
