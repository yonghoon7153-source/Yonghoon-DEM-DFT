#!/usr/bin/env python3
"""anode_interface_stability.py — is the SE stable against a Li-METAL anode?

The decisive calc flagged by external review (b2o3 report card #1). Computes the
GrandPotentialInterfacialReactivity (Richards/Ong 2016) between the SE and Li
metal, opening the Li reservoir at mu_Li = mu_Li(metal) - V. V near 0 = direct
Li-metal contact (the anode). Reports, at each V, the most-exothermic interface
reaction ENERGY *and* its PRODUCTS (the existing interface_reactivity_v2.py saved
only the energy), and flags electronically-leaky products by cross-referencing
their MP band gaps. b2o3's ESW predicts a BP/Li3P reduction front -> this tells
us whether b2o3 is Li-metal-unstable (and how it compares to undoped LPSCl1.6).

Run on gabia/kserver116 (MP_API_KEY set, MP reachable):
  python3 tools/oxidation/anode_interface_stability.py \
    --electrolytes "Li58P8S41Cl16B2O3:b2o3" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
    --voltages 0.0 0.5 1.0 1.72 \
    --out db/properties/anode_interface_b2o3.json
"""
import argparse, json, os, re
from pathlib import Path

LEAKY_EV = 2.0   # MP gap below this = electronically leaky interphase (heuristic)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+", required=True, help='comp:label')
    ap.add_argument("--voltages", nargs="+", type=float, default=[0.0, 0.5, 1.0, 1.72])
    ap.add_argument("--out", default="anode_interface.json")
    a = ap.parse_args()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("Set MP_API_KEY (run on gabia/kserver116).")

    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram
    from pymatgen.analysis.interface_reactions import GrandPotentialInterfacialReactivity
    from mp_api.client import MPRester

    elems = set()
    for s in a.electrolytes:
        elems |= set(Composition(s.split(":")[0]).elements)
    elems.add(Element("Li"))
    chemsys = sorted(e.symbol for e in elems)
    print("chemsys =", chemsys)
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(chemsys)
        # MP band gaps of candidate product phases (lowest-e per formula)
        gaps = {}
        for d in mpr.materials.summary.search(chemsys=chemsys,
                fields=["formula_pretty", "band_gap", "energy_above_hull"]):
            f = d.formula_pretty
            if f not in gaps or (d.energy_above_hull or 9) < gaps[f][1]:
                gaps[f] = (round(float(d.band_gap), 2), float(d.energy_above_hull or 0))

    pd = PhaseDiagram(entries)
    mu0 = min(e.energy_per_atom for e in entries if e.composition.reduced_formula == "Li")
    Li = Composition("Li")
    print(f"mu_Li(metal) = {mu0:.4f} eV/atom\n")

    def product_gaps(rxn):
        # pull formula-like tokens from the reaction string, look up MP gaps
        out = {}
        for tok in re.findall(r"[A-Z][A-Za-z0-9.()]*", rxn or ""):
            try:
                rf = Composition(tok).reduced_formula
            except Exception:
                continue
            if rf in gaps:
                out[rf] = gaps[rf][0]
        return out

    results = {}
    for spec in a.electrolytes:
        estr, _, elab = spec.partition(":"); elab = elab or estr
        results[elab] = {"composition": estr, "by_voltage": {}}
        print(f"######## {elab} ({estr}) vs Li metal ########")
        for V in a.voltages:
            gpd = GrandPotentialPhaseDiagram(entries, {Element("Li"): mu0 - V})
            gir = GrandPotentialInterfacialReactivity(
                Composition(estr), Li, gpd, pd_non_grand=pd,
                include_no_mixing_energy=True, use_hull_energy=True)
            me, rxn = 1e9, None
            for k in gir.get_kinks():
                if float(k[2]) < me:
                    me, rxn = float(k[2]), str(k[3])
            pg = product_gaps(rxn)
            leaky = sorted([f"{p}({g})" for p, g in pg.items() if g < LEAKY_EV])
            results[elab]["by_voltage"][f"{V:.2f}"] = {
                "rxn_energy_eV_atom": round(me, 4), "reaction": rxn,
                "product_gaps_eV": pg, "leaky_products": leaky,
                "min_product_gap_eV": (min(pg.values()) if pg else None)}
            print(f"  V={V:.2f}: {me:.4f} eV/atom | leaky={leaky or 'none'} | {rxn}")
        print()

    Path(a.out).write_text(json.dumps({
        "method": "GrandPotentialInterfacialReactivity vs Li metal (anode), mu_Li=metal-V; MP GGA/GGA+U. "
                  "rxn_energy more negative = more reactive = LESS stable against Li metal. leaky_products = "
                  f"interface phases with MP gap < {LEAKY_EV} eV (electron-conducting interphase).",
        "mu_Li_metal_eV": round(mu0, 4), "leaky_threshold_eV": LEAKY_EV,
        "results": results}, indent=2))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
