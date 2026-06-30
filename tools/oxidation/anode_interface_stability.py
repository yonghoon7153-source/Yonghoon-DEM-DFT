#!/usr/bin/env python3
"""anode_interface_stability.py — is the SE stable against a Li-METAL anode?

The decisive calc flagged by external review (b2o3 report card #1). Uses the
CLOSED pymatgen InterfacialReactivity (Richards/Ong 2016, Wenzel/Janek anode
picture): the most-exothermic mutual reaction between the SE and Li metal along
the SE-Li tie-line. Li metal = 0 V (the anode); a closed binary, so NO open Li
reservoir (that breaks for a pure-Li partner -- use esw_grand_potential.py for
voltage-resolved windows). Reports the reaction ENERGY (more negative = more
reactive = LESS stable vs Li) and its PRODUCTS, and flags electronically-leaky
products by MP band gap -> confirms/refutes the predicted BP/Li3P leaky reduction
front and compares b2o3 vs undoped LPSCl1.6.

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
    from pymatgen.analysis.interface_reactions import InterfacialReactivity
    from mp_api.client import MPRester

    elems = set()
    for s in a.electrolytes:
        elems |= set(Composition(s.split(":")[0]).elements)
    elems.add(Element("Li"))
    chemsys = sorted(e.symbol for e in elems)
    print("chemsys =", chemsys)
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(chemsys)
        gaps = {}
        for d in mpr.materials.summary.search(chemsys=chemsys,
                fields=["formula_pretty", "band_gap", "energy_above_hull"]):
            f = d.formula_pretty
            if f not in gaps or (d.energy_above_hull or 9) < gaps[f][1]:
                gaps[f] = (round(float(d.band_gap), 2), float(d.energy_above_hull or 0))

    pd = PhaseDiagram(entries)
    Li = Composition("Li")
    mu0 = min(e.energy_per_atom for e in entries if e.composition.reduced_formula == "Li")
    print(f"mu_Li(metal) = {mu0:.4f} eV/atom\n")

    def product_gaps(rxn):
        out = {}
        for tok in re.findall(r"[A-Z][A-Za-z0-9.()]*", rxn or ""):
            try:
                rf = Composition(tok).reduced_formula
            except Exception:
                continue
            if rf in gaps and rf != "Li":
                out[rf] = gaps[rf][0]
        return out

    results = {}
    for spec in a.electrolytes:
        estr, _, elab = spec.partition(":"); elab = elab or estr
        ir = InterfacialReactivity(Composition(estr), Li, pd, use_hull_energy=True)
        me, rxn, kinks = 1e9, None, []
        for k in ir.get_kinks():
            idx, x, e, rk = k[0], k[1], k[2], k[3]
            kinks.append({"x_Li": round(float(x), 3),
                          "energy_eV_atom": round(float(e), 4), "reaction": str(rk)})
            if float(e) < me:
                me, rxn = float(e), str(rk)
        pg = product_gaps(rxn)
        leaky = sorted(f"{p}({g})" for p, g in pg.items() if g < LEAKY_EV)
        results[elab] = {
            "composition": estr,
            "max_rxn_energy_eV_atom": round(me, 4),   # most-exothermic = anode driving force
            "reaction": rxn, "product_gaps_eV": pg, "leaky_products": leaky,
            "min_product_gap_eV": (min(pg.values()) if pg else None),
            "all_kinks": kinks}
        print(f"######## {elab} ({estr}) vs Li metal ########")
        print(f"  max reaction energy = {me:.4f} eV/atom  (more negative = less stable vs Li)")
        print(f"  reaction = {rxn}")
        print(f"  product gaps = {pg}")
        print(f"  LEAKY products (<{LEAKY_EV} eV) = {leaky or 'none'}\n")

    Path(a.out).write_text(json.dumps({
        "method": "closed pymatgen InterfacialReactivity (Richards/Ong 2016) SE vs Li metal (anode, 0 V); "
                  "max (most-negative) mutual reaction energy = anode driving force. leaky_products = interphase "
                  f"phases with MP gap < {LEAKY_EV} eV (electron-conducting -> non-passivating). MP GGA/GGA+U.",
        "mu_Li_metal_eV": round(mu0, 4), "leaky_threshold_eV": LEAKY_EV,
        "results": results}, indent=2))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
