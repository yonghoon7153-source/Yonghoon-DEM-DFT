#!/usr/bin/env python3
"""anode_interface_stability.py — SE reduction interphase vs anode RESERVOIRS.

External-review #1 calc, generalized to multiple practical anodes. Uses the
open-Li reduction profile (pymatgen PhaseDiagram.get_element_profile(Li, SE),
same machinery as esw_grand_potential) and reads the equilibrium decomposition
at each anode's Li chemical potential (V vs Li/Li+):
    Li metal = 0 V (most reducing) ; Li-In = ~0.62 V ; Li-Al = ~0.30 V .
Reports the interphase products + their MP band gaps + leaky flag at each anode,
so a milder alloy anode (Li-In) can be compared to bare Li metal. Compares the
doped SE vs the undoped reference.

Run on gabia/kserver116 (MP_API_KEY set, pymatgen + mp_api):
  python3 tools/oxidation/anode_interface_stability.py \
    --electrolytes "Li58P8S41Cl16B2O3:b2o3" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
    --anode_voltages 0.0 0.62 \
    --out db/properties/anode_interface_b2o3.json
"""
import argparse, json, os, re
from pathlib import Path

LEAKY_EV = 2.0
ANODE_NAMES = {0.0: "Li-metal", 0.62: "Li-In", 0.30: "Li-Al", 0.85: "Li-Sn"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolytes", nargs="+", required=True, help='comp:label')
    ap.add_argument("--anode_voltages", nargs="+", type=float, default=[0.0, 0.62],
                    help="anode reservoir V vs Li/Li+ (0=Li metal, 0.62=Li-In, 0.30=Li-Al)")
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
    mu_ref = pd.el_refs[Li].energy_per_atom
    print(f"mu_Li(metal) = {mu_ref:.4f} eV/atom  (V = mu_ref - mu_Li; 0 V = Li metal)\n")

    def rhs_formulas(rxn):
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

    # pass 1: profile + the decomposition step nearest each anode voltage
    raw, allprod = {}, set()
    for spec in a.electrolytes:
        estr, _, elab = spec.partition(":"); elab = elab or estr
        profile = pd.get_element_profile(Li, Composition(estr))
        steps = sorted(({"V_vs_Li": round(mu_ref - float(p["chempot"]), 3),
                         "reaction": str(p["reaction"])} for p in profile),
                       key=lambda s: s["V_vs_Li"])
        per_anode = {}
        for Va in a.anode_voltages:
            st = min(steps, key=lambda s: abs(s["V_vs_Li"] - Va))  # nearest-V regime
            prods = rhs_formulas(st["reaction"])
            allprod |= prods
            per_anode[f"{Va:.2f}"] = {"anode": ANODE_NAMES.get(Va, f"{Va}V"),
                                      "step_V": st["V_vs_Li"], "reaction": st["reaction"],
                                      "products": sorted(prods)}
        raw[elab] = (estr, per_anode, steps)

    # pass 2: MP band gaps for the actual product formulas (targeted)
    gaps = {}
    with MPRester(key) as mpr:
        for d in mpr.materials.summary.search(formula=sorted(allprod),
                fields=["formula_pretty", "band_gap", "energy_above_hull"]):
            f = d.formula_pretty
            if f not in gaps or (d.energy_above_hull or 9) < gaps[f][1]:
                gaps[f] = (round(float(d.band_gap), 2), float(d.energy_above_hull or 0))

    results = {}
    for elab, (estr, per_anode, steps) in raw.items():
        results[elab] = {"composition": estr, "by_anode": {}, "full_profile": steps}
        print(f"######## {elab} ({estr}) ########")
        for vkey, info in per_anode.items():
            pg = {p: gaps[p][0] for p in info["products"] if p in gaps}
            leaky = sorted(f"{p}({g})" for p, g in pg.items() if g < LEAKY_EV)
            mn = min(pg.values()) if pg else None
            results[elab]["by_anode"][vkey] = {
                "anode": info["anode"], "V_vs_Li": info["step_V"], "reaction": info["reaction"],
                "product_gaps_eV": pg, "leaky_products": leaky, "min_product_gap_eV": mn}
            print(f"  {info['anode']:9s} (V≈{vkey}): min gap {mn} | leaky {leaky or 'none'}")
            print(f"      {info['reaction']}")
        print()

    Path(a.out).write_text(json.dumps({
        "method": "open-Li get_element_profile(Li, SE); decomposition at each anode reservoir V (Li metal 0 V, "
                  f"Li-In ~0.62 V, ...). leaky = MP gap < {LEAKY_EV} eV (electron-conducting interphase). MP GGA/GGA+U.",
        "mu_Li_metal_eV": round(mu_ref, 4), "leaky_threshold_eV": LEAKY_EV,
        "anode_voltages": a.anode_voltages, "results": results}, indent=2))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
