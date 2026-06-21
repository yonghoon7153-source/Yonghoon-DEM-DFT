#!/usr/bin/env python3
"""interface_reactivity_v2.py — VOLTAGE-RESOLVED electrolyte/cathode interface
reactivity (Richards/Ong 2016, Chem. Mater. 28, 266), the accurate upgrade of
interface_reactivity.py.

Why this is more accurate than v1
---------------------------------
v1 computed the SE/cathode mutual reaction at OCV (closed system). But the real
degradation happens during CHARGE, where the cathode is delithiated and the
local environment is strongly oxidizing (low mu_Li / high voltage). This tool
opens the system to a Li reservoir (GrandPotentialInterfacialReactivity) and
evaluates the most-exothermic SE/cathode reaction AS A FUNCTION OF the applied
voltage V (vs Li/Li+), via mu_Li = mu_Li(Li metal) - V. At high V the cathode
delithiates automatically, so we capture the charged-state reactivity.

  reaction energy more negative  ==  more reactive interface  ==  worse.

Outputs reaction_energy(V) for each electrolyte x cathode, and the comp1-vs-
modelc difference at each voltage (where they may diverge even though OCV is
identical).

Run on gabia/kserver116-27 (MP_API_KEY set, MP reachable, pymatgen+mp_api):
  python3 interface_reactivity_v2.py \
    --electrolytes "Li6PS5Cl:LPSCl" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
    --cathodes LiCoO2 LiNiO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
    --voltages 2.5 3.0 3.5 4.0 4.3 \
    --out interface_reactivity_v2.json
"""
import argparse, json, os
from pathlib import Path


def get_entries(elements):
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    print(f"[mp_api] {len(entries)} entries in {'-'.join(sorted(elements))}")
    return entries


def li_metal_mu(entries):
    from pymatgen.core import Composition
    es = [e.energy_per_atom for e in entries
          if e.composition.reduced_formula == "Li"]
    return min(es)  # Li metal reference (eV/atom)


def min_rxn_grand(c1, c2, gpd, pd):
    from pymatgen.analysis.interface_reactions import GrandPotentialInterfacialReactivity
    gir = GrandPotentialInterfacialReactivity(
        c1, c2, gpd, pd_non_grand=pd,
        include_no_mixing_energy=True, use_hull_energy=True)
    min_e, min_rxn = 1e9, None
    for k in gir.get_kinks():
        e = float(k[2])
        if e < min_e:
            min_e, min_rxn = e, str(k[3])
    return min_e, min_rxn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+", required=True,
                    help='comp:label, e.g. "Li6PS5Cl:LPSCl"')
    ap.add_argument("--cathodes", nargs="+", default=["LiCoO2", "LiNiO2"],
                    help='comp[:label] cathodes')
    ap.add_argument("--voltages", nargs="+", type=float,
                    default=[2.5, 3.0, 3.5, 4.0, 4.3])
    ap.add_argument("--out", default="interface_reactivity_v2.json")
    a = ap.parse_args()

    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

    elems = set()
    for s in a.electrolytes + a.cathodes:
        elems |= set(Composition(s.split(":")[0]).elements)
    elems.add(Element("Li"))
    elements = sorted(e.symbol for e in elems)
    print("chemsys =", elements)
    entries = get_entries(elements)
    pd = PhaseDiagram(entries)
    mu0 = li_metal_mu(entries)
    print(f"mu_Li(metal) = {mu0:.4f} eV/atom")

    results = {}
    for cat in a.cathodes:
        cstr, _, clab = cat.partition(":"); clab = clab or cstr
        cc = Composition(cstr)
        results[clab] = {"composition": cstr, "by_voltage": {}}
        print(f"\n######## cathode {clab} ({cstr}) ########")
        for V in a.voltages:
            mu = mu0 - V
            gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu})
            row = {}
            for spec in a.electrolytes:
                estr, _, elab = spec.partition(":"); elab = elab or estr
                try:
                    e, rxn = min_rxn_grand(Composition(estr), cc, gpd, pd)
                    row[elab] = round(e, 5)
                    print(f"  V={V:.2f}  {elab:9s}: {e:.4f} eV/atom")
                except Exception as ex:
                    row[elab] = None
                    print(f"  V={V:.2f}  {elab}: ERR {type(ex).__name__}: {ex}")
            results[clab]["by_voltage"][f"{V:.2f}"] = row

    Path(a.out).write_text(json.dumps({
        "method": "GrandPotentialInterfacialReactivity (Richards/Ong 2016), "
                  "open to Li reservoir; mu_Li = mu_Li(metal) - V; "
                  "use_hull_energy=True; MP GGA_GGA+U. More negative = more "
                  "reactive interface at that voltage.",
        "mu_Li_metal_eV": round(mu0, 4),
        "voltages_V": a.voltages,
        "results": results,
    }, indent=2))
    print(f"\n→ {a.out}")


if __name__ == "__main__":
    main()
