#!/usr/bin/env python3
"""anode_interface_stability.py — what does the SE reduce to against a Li-METAL anode?

The decisive calc flagged by external review (b2o3 report card #1). Uses the SAME
grand-potential (open-Li) machinery as esw_grand_potential.py -- pymatgen
`PhaseDiagram.get_element_profile(Li, SE)` -- to get the Li-chempot decomposition
profile, and extracts the reaction at V ~ 0 (mu_Li = mu_Li(metal) = direct
Li-metal contact = the anode). That reaction's PRODUCTS are the reduction
interphase; their MP band gaps flag electronically-leaky (non-passivating) phases.
Compares b2o3 vs undoped LPSCl1.6 -> does doping worsen Li-metal stability?

(NOTE: a closed InterfacialReactivity(SE, Li) is wrong here -- the SE is not an MP
phase, so use_hull_energy projects it onto the hull and the SE/Li reaction reads
~0. The open-Li profile is the correct electrochemical-reduction picture.)

Run on gabia/kserver116 (MP_API_KEY set, pymatgen + mp_api):
  python3 tools/oxidation/anode_interface_stability.py \
    --electrolytes "Li58P8S41Cl16B2O3:b2o3" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
    --out db/properties/anode_interface_b2o3.json
"""
import argparse, json, os, re
from pathlib import Path

LEAKY_EV = 2.0   # MP gap below this = electronically leaky interphase (heuristic)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+", required=True, help='comp:label')
    ap.add_argument("--out", default="anode_interface.json")
    a = ap.parse_args()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("Set MP_API_KEY (run on gabia/kserver116).")

    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    from mp_api.client import MPRester

    elems = set()
    for s in a.electrolytes:
        elems |= set(Composition(s.split(":")[0]).elements)
    elems.add(Element("Li"))
    chemsys = sorted(e.symbol for e in elems)
    print("chemsys =", chemsys)
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(chemsys)

    pd = PhaseDiagram(entries)
    Li = Element("Li")
    mu_ref = pd.el_refs[Li].energy_per_atom   # mu_Li(metal); V = mu_ref - mu
    print(f"mu_Li(metal) = {mu_ref:.4f} eV/atom  (V = mu_ref - mu_Li; 0 V = Li metal)\n")

    def rhs_formulas(rxn):
        # RHS (products) of "A -> B + C + ..."; reduced formulas, drop Li metal
        rhs = (rxn or "").split("->")[-1]
        out = set()
        for tok in re.findall(r"[A-Z][A-Za-z0-9.()]*", rhs):
            try:
                rf = Composition(tok).reduced_formula
            except Exception:
                continue
            if rf != "Li":
                out.add(rf)
        return out

    # pass 1: reactions per SE
    raw = {}
    allprod = set()
    for spec in a.electrolytes:
        estr, _, elab = spec.partition(":"); elab = elab or estr
        profile = pd.get_element_profile(Li, Composition(estr))
        steps = sorted(({"V_vs_Li": round(mu_ref - float(p["chempot"]), 3),
                         "evolution_Li": round(float(p["evolution"]), 4),
                         "reaction": str(p["reaction"])} for p in profile),
                       key=lambda s: s["V_vs_Li"])
        anode = steps[0]            # lowest V = nearest Li metal (most reduced)
        prods = rhs_formulas(anode["reaction"])
        allprod |= prods
        raw[elab] = (estr, anode, steps, prods)

    # pass 2: MP band gaps for the ACTUAL product formulas (targeted -> no 100-cap bug)
    gaps = {}
    with MPRester(key) as mpr:
        for d in mpr.materials.summary.search(formula=sorted(allprod),
                fields=["formula_pretty", "band_gap", "energy_above_hull"]):
            f = d.formula_pretty
            if f not in gaps or (d.energy_above_hull or 9) < gaps[f][1]:
                gaps[f] = (round(float(d.band_gap), 2), float(d.energy_above_hull or 0))

    results = {}
    for elab, (estr, anode, steps, prods) in raw.items():
        pg = {p: gaps[p][0] for p in prods if p in gaps}
        leaky = sorted(f"{p}({g})" for p, g in pg.items() if g < LEAKY_EV)
        results[elab] = {
            "composition": estr,
            "anode_V_vs_Li": anode["V_vs_Li"],
            "anode_reduction_reaction": anode["reaction"],
            "product_gaps_eV": pg, "leaky_products": leaky,
            "min_product_gap_eV": (min(pg.values()) if pg else None),
            "full_profile": steps}
        print(f"######## {elab} ({estr}) vs Li metal ########")
        print(f"  anode (V≈{anode['V_vs_Li']}) reduction: {anode['reaction']}")
        print(f"  product gaps = {pg}")
        print(f"  LEAKY products (<{LEAKY_EV} eV) = {leaky or 'none'}  | min gap = {results[elab]['min_product_gap_eV']}\n")

    Path(a.out).write_text(json.dumps({
        "method": "pymatgen get_element_profile(Li, SE) (open-Li, same as esw_grand_potential); reaction at "
                  "V~0 (mu_Li=metal) = Li-metal reduction interphase. leaky_products = phases with MP gap < "
                  f"{LEAKY_EV} eV (electron-conducting -> non-passivating). MP GGA/GGA+U. Compare b2o3 vs LPSCl1.6.",
        "mu_Li_metal_eV": round(mu_ref, 4), "leaky_threshold_eV": LEAKY_EV,
        "results": results}, indent=2))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
