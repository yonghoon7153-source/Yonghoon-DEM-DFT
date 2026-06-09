#!/usr/bin/env python3
"""constrained_esw.py — Mechanically-CONSTRAINED electrochemical stability window
(Gil-González/Fitzhugh constrained-ensemble method), our-cells implementation.

Reproduces the composition dependence of Gil-González (Energy Storage Mater. 2022)
for OUR comp1 / modelc by computing the REACTION VOLUMETRIC STRAIN of the
decomposition explicitly and applying the Fitzhugh strain term as a leading-order
shift of the window edges.

Why strain-explicit (not augmented-hull)
----------------------------------------
get_element_profile gives edge voltages set by PHASE stability, which are
composition-INDEPENDENT (comp1 and modelc share the same Li-P-S-Cl decomposition
phases -> identical edges). Gil-González's Cl-rich-widens-more result instead
comes from the composition-dependent REACTION STRAIN. Here we:
  1. Get the K_eff=0 oxidation-onset and reduction-onset reactions per
     composition (clean MP hull, LiS4/SCl3/Li5PS4Cl2 excluded).
  2. Compute the reaction volume change DeltaV = V_products(solids) - V_SE from
     MP molar volumes (released/consumed Li goes to/from the anode reservoir and
     does NOT count in the constrained solid volume).
  3. Apply Fitzhugh Eq.1 at the onset: the decomposition driving force
     d_sD G' = dG_chem + K_eff*DeltaV ; near the K_eff=0 onset dG_chem grows
     ~ -n_e*(phi - phi0)*e, so the edge shifts by
        anodic : phi_ox(K)  = phi_ox0  + K_eff*DeltaV_ox  / n_e_ox
        cathodic: phi_red(K) = phi_red0 - K_eff*DeltaV_red / n_e_red
     (units: GPa*Å^3 -> eV via 6.242e-3; per electron -> Volts.) A volume-
     EXPANDING decomposition (DeltaV>0) is suppressed -> the window WIDENS, and
     a composition whose decomposition expands MORE per electron widens MORE.

Usage (gabia, MP_API_KEY set):
    python3 constrained_esw.py \
        --target "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --v_se_A3 254.16 243.29 \
        --k_eff 0 10 20 \
        --out constrained_esw_results.json
  --v_se_A3 : SE molar volume per FORMULA UNIT (Å^3): comp1 1016.62/4=254.16,
              modelc 1216.44/5=243.29.
"""
import argparse
import json
import os
from pathlib import Path

GPA_A3_TO_EV = 6.241509074e-3
EXCLUDE_FORMULAS = {"LiS4", "SCl3", "Li5PS4Cl2"}  # Gil-González SI exclusions


def get_entries(elements):
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    kept, dropped = [], []
    for e in entries:
        if e.composition.reduced_formula in EXCLUDE_FORMULAS:
            dropped.append(e.composition.reduced_formula); continue
        kept.append(e)
    print(f"[mp_api] {len(entries)} entries; dropped {sorted(set(dropped))}; "
          f"kept {len(kept)}")
    return kept


def vol_per_atom_table(entries):
    """reduced_formula -> volume per atom (Å^3) from the lowest-energy entry."""
    best = {}
    vpa = {}
    for e in entries:
        rf = e.composition.reduced_formula
        epa = e.energy_per_atom
        if rf not in best or epa < best[rf]:
            best[rf] = epa
            try:
                vpa[rf] = float(e.structure.volume) / e.composition.num_atoms
            except Exception:
                pass
    return vpa


def onset_reactions(pd, comp, mu_Li_ref):
    """K_eff=0: return (red_limit_V, red_rxn, ox_limit_V, ox_rxn, full_steps)."""
    from pymatgen.core import Element
    Li = Element("Li")
    profile = pd.get_element_profile(Li, comp)
    steps = []
    for p in profile:
        steps.append({"V": round(mu_Li_ref - float(p["chempot"]), 3),
                      "evo": round(float(p["evolution"]), 4),
                      "rxn": p["reaction"]})
    s = sorted(steps, key=lambda x: x["V"])
    pos = [x for x in s if x["evo"] > 1e-6]   # reduction (Li uptake)
    neg = [x for x in s if x["evo"] < -1e-6]  # oxidation (Li release)
    red = max(pos, key=lambda x: x["V"]) if pos else None
    ox = min(neg, key=lambda x: x["V"]) if neg else None
    return red, ox, steps


def reaction_strain(rxn, vpa, v_se):
    """DeltaV = V_products(solids) - V_SE, n_e = |Li exchanged|. Returns
    (DeltaV_A3_per_fu, n_e, eps_RXN, product_str, missing[list])."""
    from pymatgen.core import Composition, Element
    Li = Composition("Li").reduced_formula
    vol_prod = 0.0
    n_Li = 0.0
    missing = []
    parts = []
    for c in rxn.products:
        coeff = abs(rxn.get_coeff(c))
        rf = c.reduced_formula
        if rf == "Li":
            n_Li += coeff * c.num_atoms
            continue
        vpa_i = vpa.get(rf)
        if vpa_i is None:
            missing.append(rf); continue
        v = coeff * c.num_atoms * vpa_i
        vol_prod += v
        parts.append(f"{coeff:.3g}{rf}({v:.1f})")
    # Li may instead be a REACTANT (reduction) -> count it as Li exchanged too
    for c in rxn.reactants:
        if c.reduced_formula == "Li":
            n_Li += abs(rxn.get_coeff(c)) * c.num_atoms
    dV = vol_prod - v_se
    eps = dV / v_se if v_se else None
    return dV, n_Li, eps, " + ".join(parts), missing


def augmented_pd_relax(entries, k_eff):
    """Augmented PhaseDiagram for Fitzhugh re-min: E_i -> E_i + K_eff*V_i for every
    SOLID phase; Li metal kept UNAUGMENTED (open-element reservoir at the anode).
    Volume-expanding decompositions are penalised; optimal product set re-selected
    at each K_eff (reproduces Gil-González Table S1 product-set switching:
    PCl3/P2S7/SCl at 0 GPa -> SCl4/Li2PS3/S at 20 GPa)."""
    from pymatgen.analysis.phase_diagram import PhaseDiagram, PDEntry
    pd_entries = []
    for e in entries:
        els = e.composition.elements
        is_Li_metal = (len(els) == 1 and els[0].symbol == "Li")
        try:
            V = float(e.structure.volume)
        except Exception:
            V = None
        if V is None or is_Li_metal:
            pd_entries.append(PDEntry(e.composition, e.energy))
        else:
            pd_entries.append(PDEntry(e.composition, e.energy + k_eff * V * GPA_A3_TO_EV))
    return PhaseDiagram(pd_entries)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", nargs="+", required=True)
    ap.add_argument("--v_se_A3", nargs="+", type=float, required=True)
    ap.add_argument("--elements", nargs="+", default=["Li", "P", "S", "Cl"])
    ap.add_argument("--k_eff", nargs="+", type=float, default=[0, 10, 20])
    ap.add_argument("--mode", choices=["leading", "relax", "hybrid"], default="leading",
                    help="leading = leading-order edge shift (fast, K_eff=0 onset reused). "
                         "relax = full Fitzhugh re-min (augmented hull per K_eff; reports the "
                         "switched product set; absolute edge voltages come from breakpoints "
                         "which are composition-INVARIANT, so prefer hybrid for the comp1-vs-"
                         "modelc trend). "
                         "hybrid = use relax mode to DETECT product-set switching, then apply "
                         "leading-order phi += K_eff*DeltaV/n_e with the SWITCHED reaction's "
                         "DeltaV/n_e -- gives both the Gil-González product physics AND the "
                         "composition-resolved widening.")
    ap.add_argument("--out", default="constrained_esw_results.json")
    args = ap.parse_args()

    from pymatgen.core import Element, Composition
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    Li = Element("Li")

    entries = get_entries(args.elements)
    vpa = vol_per_atom_table(entries)
    pd = PhaseDiagram(entries)
    mu_ref = pd.el_refs[Li].energy_per_atom
    print(f"mu_Li(metal) = {mu_ref:.4f} eV/atom\n")

    results = {}
    for i, spec in enumerate(args.target):
        cs, _, lab = spec.partition(":")
        lab = lab or cs
        v_se = args.v_se_A3[i]
        comp = Composition(cs)
        red, ox, steps = onset_reactions(pd, comp, mu_ref)

        print(f"=== {lab}  ({cs})   V_SE = {v_se:.1f} Å^3/fu ===")
        ox_info = red_info = None
        if ox:
            dV, ne, eps, pstr, miss = reaction_strain(ox["rxn"], vpa, v_se)
            ox_info = {"phi0_V": ox["V"], "rxn": str(ox["rxn"]),
                       "DeltaV_A3": round(dV, 1), "n_e": round(ne, 3),
                       "eps_RXN": round(eps, 4) if eps is not None else None,
                       "products_vol": pstr, "missing_vol": miss}
            print(f"  OX  onset {ox['V']:.2f} V | n_e={ne:.2f} | "
                  f"DeltaV={dV:+.1f} Å^3 | eps_RXN={eps:+.3f} | {ox['rxn']}")
            if miss: print(f"      [warn] no MP volume for: {miss}")
        if red:
            dVr, ner, epsr, pstrr, missr = reaction_strain(red["rxn"], vpa, v_se)
            red_info = {"phi0_V": red["V"], "rxn": str(red["rxn"]),
                        "DeltaV_A3": round(dVr, 1), "n_e": round(ner, 3),
                        "eps_RXN": round(epsr, 4) if epsr is not None else None,
                        "products_vol": pstrr, "missing_vol": missr}
            print(f"  RED onset {red['V']:.2f} V | n_e={ner:.2f} | "
                  f"DeltaV={dVr:+.1f} Å^3 | eps_RXN={epsr:+.3f} | {red['rxn']}")

        # window vs K_eff: leading-order or full Fitzhugh re-min
        win = {}
        print(f"  window vs K_eff ({args.mode} mode):")
        for k in args.k_eff:
            phi_ox = phi_red = None
            ox_rxn_k = red_rxn_k = None
            if args.mode == "leading":
                if ox_info and ox_info["n_e"]:
                    phi_ox = ox_info["phi0_V"] + k * ox_info["DeltaV_A3"] * GPA_A3_TO_EV / ox_info["n_e"]
                    ox_rxn_k = ox_info["rxn"]
                if red_info and red_info["n_e"]:
                    phi_red = red_info["phi0_V"] - k * red_info["DeltaV_A3"] * GPA_A3_TO_EV / red_info["n_e"]
                    red_rxn_k = red_info["rxn"]
            else:  # relax or hybrid: rebuild augmented hull at each K_eff
                if k == 0:
                    pd_k, mu_k = pd, mu_ref
                else:
                    pd_k = augmented_pd_relax(entries, k)
                    mu_k = pd_k.el_refs[Li].energy_per_atom
                try:
                    red_k, ox_k, _ = onset_reactions(pd_k, comp, mu_k)
                except Exception as e:
                    print(f"    K={k:>4.0f} GPa: ERROR {type(e).__name__}: {e}")
                    win[str(k)] = {"error": str(e)}
                    continue
                if args.mode == "relax":
                    # raw breakpoint voltages (composition-INVARIANT, all same)
                    if ox_k:
                        phi_ox = ox_k["V"]; ox_rxn_k = str(ox_k["rxn"])
                    if red_k:
                        phi_red = red_k["V"]; red_rxn_k = str(red_k["rxn"])
                else:  # hybrid: leading-order shift using the SWITCHED rxn's DeltaV/n_e
                    if ox_k and ox_info:
                        dVx, nex, _, _, _ = reaction_strain(ox_k["rxn"], vpa, v_se)
                        if nex:
                            phi_ox = ox_info["phi0_V"] + k * dVx * GPA_A3_TO_EV / nex
                            ox_rxn_k = f"{str(ox_k['rxn'])} [DeltaV={dVx:+.1f} n_e={nex:.2f}]"
                    if red_k and red_info:
                        dVr, ner, _, _, _ = reaction_strain(red_k["rxn"], vpa, v_se)
                        if ner:
                            phi_red = red_info["phi0_V"] - k * dVr * GPA_A3_TO_EV / ner
                            red_rxn_k = f"{str(red_k['rxn'])} [DeltaV={dVr:+.1f} n_e={ner:.2f}]"
            width = (phi_ox - phi_red) if (phi_ox is not None and phi_red is not None) else None
            win[str(k)] = {"reduction_V": round(phi_red, 3) if phi_red is not None else None,
                           "oxidation_V": round(phi_ox, 3) if phi_ox is not None else None,
                           "width_V": round(width, 3) if width is not None else None,
                           "oxidation_rxn": ox_rxn_k,
                           "reduction_rxn": red_rxn_k}
            print(f"    K={k:>4.0f} GPa: {win[str(k)]['reduction_V']} - "
                  f"{win[str(k)]['oxidation_V']} V  (width {win[str(k)]['width_V']})")
            if args.mode in ("relax", "hybrid") and ox_rxn_k:
                base_rxn = ox_info["rxn"] if ox_info else None
                switched = (ox_rxn_k.split(" [")[0] != base_rxn) if base_rxn else False
                if switched:
                    print(f"      [re-min] anodic rxn switched to: {ox_rxn_k}")
        print()
        results[lab] = {"composition": cs, "v_se_A3_per_fu": v_se,
                        "oxidation_onset_K0": ox_info, "reduction_onset_K0": red_info,
                        "window_vs_k_eff": win}

    # comp1 vs modelc widening comparison
    labs = list(results)
    if len(labs) == 2:
        a, b = labs
        print("================ comp1 vs modelc ================")
        for lab in (a, b):
            ox = results[lab]["oxidation_onset"]
            if ox:
                print(f"  {lab}: oxidation eps_RXN = {ox['eps_RXN']:+.3f} "
                      f"(DeltaV {ox['DeltaV_A3']:+.1f} Å^3, n_e {ox['n_e']})")
        print("  -> larger eps_RXN / (DeltaV/n_e) widens MORE under constriction.")

    if args.mode == "leading":
        method_desc = ("strain-explicit constrained ESW (Fitzhugh leading-order "
                       "edge shift phi += K_eff*DeltaV/n_e using K_eff=0 onset rxn)")
    elif args.mode == "hybrid":
        method_desc = ("Fitzhugh hybrid: augmented hull per K_eff to DETECT product-set "
                       "switching, then leading-order shift with the SWITCHED rxn's "
                       "DeltaV/n_e -- gives both product physics and composition-resolved widening")
    else:
        method_desc = ("Fitzhugh full re-minimisation (augmented hull E_i += K_eff*V_i "
                       "for SOLID phases; Li metal unaugmented; raw breakpoint voltages -- "
                       "composition-INVARIANT, use only for product-set diagnostics)")
    Path(args.out).write_text(json.dumps({
        "method": method_desc + ". MP GGA_GGA+U hull; LiS4/SCl3/Li5PS4Cl2 excluded.",
        "mode": args.mode,
        "k_eff_GPa": args.k_eff, "results": results,
    }, indent=2))
    print(f"→ {args.out}")


if __name__ == "__main__":
    main()
