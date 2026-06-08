#!/usr/bin/env python3
"""esw_grand_potential.py — REAL electrochemical stability window (ESW)
via the grand-potential phase-diagram method (Ong 2008; Mo/Ong/Ceder 2012,
Chem. Mater. 24, 15; Zhu/He/Mo 2015, JMCA).

This is the genuine ESW — NOT the qualitative "competing-phase energy span"
hint from tools/doping/esw_check.py. The Li reservoir is opened (grand
canonical) and the composition's Li-grand-potential decomposition is tracked
as the applied potential (= μ_Li) is scanned, using pymatgen's standard
`PhaseDiagram.get_element_profile`.

Why get_element_profile (and not "place compound at hull energy + scan")
-----------------------------------------------------------------------
For these argyrodite electrolytes the ordered phase is itself slightly
metastable (~tens of meV/atom above hull) and, more importantly, a
non-stoichiometric composition (modelc Li5.4PS4.4Cl1.6) has NO MP entry and
no MP-scale total energy of its own. get_element_profile needs only the
*composition* and the MP convex hull: it returns, as the Li chemical
potential is swept, the sequence of equilibrium decomposition reactions and
the critical μ_Li at which they switch. That makes comp1 (in MP) and modelc
(not in MP) directly comparable on the same footing.

Voltage convention
------------------
V (vs Li/Li+) = μ_Li(metal) − μ_Li ,  with e = 1, energies in eV.
V = 0  → μ_Li = Li-metal reference (most reducing).
High V → low μ_Li (most oxidizing).

  • Reduction (cathodic) limit = lowest V above which NO further Li is taken
    up (below it the composition is reduced — Li3P / Li2S / Li metal form).
  • Oxidation (anodic) limit  = highest V below which NO Li is released
    (above it the composition is oxidized — S / P2S5 / Cl2 form).
  • ESW width = anodic − cathodic.

Usage (run where MP_API_KEY is set, e.g. gabia/kserver116-27):
    python3 esw_grand_potential.py \
        --target "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --out esw_lpscl_results.json
"""
import argparse
import json
import os
from pathlib import Path


def get_chemsys_entries(elements):
    """MP2020-corrected entries for the chemsys, pinned to the classic
    GGA/GGA+U mixed hull (avoids R2SCAN mixing noise; matches the Mo/Ong
    literature numbers)."""
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    chemsys = "-".join(sorted(elements))
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements,
            additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    print(f"[mp_api] {len(entries)} entries in {chemsys} (GGA_GGA+U hull)")
    return entries


def rxn_to_str(reaction):
    try:
        return str(reaction)
    except Exception:
        return repr(reaction)


def analyze(pd, comp, mu_Li_ref, label, comp_str):
    """Run get_element_profile and extract the ESW for one composition."""
    from pymatgen.core import Element
    Li = Element("Li")

    # evolution profile of the OPEN element Li for this composition.
    # Returns list of {'chempot','evolution','reaction','energy'} sorted by
    # DECREASING chempot (i.e. increasing voltage).
    profile = pd.get_element_profile(Li, comp)

    n_Li_nominal = comp[Li]  # moles of Li in the nominal composition

    steps = []
    for p in profile:
        mu = float(p["chempot"])
        steps.append({
            "mu_Li_eV": round(mu, 4),
            "V_vs_Li": round(mu_Li_ref - mu, 3),
            "evolution_Li": round(float(p["evolution"]), 4),
            "reaction": rxn_to_str(p["reaction"]),
            "energy_per_atom": round(float(p["energy"]), 5),
        })

    # The "as-synthesized" composition is stable where its equilibrium Li
    # content equals the nominal Li content (evolution == n_Li_nominal).
    # That plateau's μ_Li bounds are the ESW edges.
    tol = 1e-4
    plateau = [s for s in steps
               if abs(s["evolution_Li"] - n_Li_nominal) < tol]
    window = None
    if plateau:
        v_lo = min(s["V_vs_Li"] for s in plateau)
        v_hi = max(s["V_vs_Li"] for s in plateau)
        window = (v_lo, v_hi)

    # Fallback / robust read: the highest-V step before Li starts LEAVING
    # (oxidation onset) and the lowest-V step before Li starts being ADDED
    # (reduction onset), read straight off the monotone evolution curve.
    # steps are sorted decreasing mu => increasing V.
    s_byV = sorted(steps, key=lambda s: s["V_vs_Li"])
    ox_limit = red_limit = None
    for i, s in enumerate(s_byV):
        if abs(s["evolution_Li"] - n_Li_nominal) < tol:
            red_limit = s["V_vs_Li"] if red_limit is None else red_limit
            ox_limit = s["V_vs_Li"]
    # decomposition products immediately past each limit
    def products_at(volt_target):
        # nearest step at or beyond the limit
        best = min(steps, key=lambda s: abs(s["V_vs_Li"] - volt_target))
        return best["reaction"]

    print(f"\n=== {label}  {comp_str}  ===")
    print(f"  nominal Li content n_Li = {float(n_Li_nominal):.3f}")
    if window:
        print(f"  ESW (composition stable plateau): "
              f"{window[0]:.2f} – {window[1]:.2f} V vs Li  "
              f"(width {window[1]-window[0]:.2f} V)")
        print(f"  ↓ reduction (cathodic) limit {window[0]:.2f} V  "
              f"→ below: {products_at(window[0]-0.01)}")
        print(f"  ↑ oxidation (anodic)   limit {window[1]:.2f} V  "
              f"→ above: {products_at(window[1]+0.01)}")
    else:
        print("  [warn] no Li-content plateau == nominal; dumping full profile")
    print(f"  full profile ({len(steps)} breakpoints):")
    for s in steps:
        print(f"    V={s['V_vs_Li']:>5.2f}  Li={s['evolution_Li']:>6.3f}  "
              f"{s['reaction']}")

    return {
        "composition": comp_str,
        "label": label,
        "n_Li_nominal": float(n_Li_nominal),
        "mu_Li_ref_eV": round(mu_Li_ref, 4),
        "esw_cathodic_V": round(window[0], 3) if window else None,
        "esw_anodic_V": round(window[1], 3) if window else None,
        "esw_width_V": round(window[1] - window[0], 3) if window else None,
        "profile": steps,
    }


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", nargs="+", required=True,
                    help='comp:label, e.g. "Li6PS5Cl:comp1" '
                         '"Li5.4P1S4.4Cl1.6:modelc"')
    ap.add_argument("--elements", nargs="+", default=["Li", "P", "S", "Cl"])
    ap.add_argument("--out", default="esw_grand_potential_results.json")
    args = ap.parse_args()

    from pymatgen.core import Element, Composition
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    entries = get_chemsys_entries(args.elements)
    pd = PhaseDiagram(entries)
    Li = Element("Li")
    mu_Li_ref = pd.el_refs[Li].energy_per_atom
    print(f"μ_Li(metal) reference = {mu_Li_ref:.4f} eV/atom")

    results = {}
    for spec in args.target:
        comp_str, _, label = spec.partition(":")
        label = label or comp_str
        comp = Composition(comp_str)
        try:
            results[label] = analyze(pd, comp, mu_Li_ref, label, comp_str)
        except Exception as e:
            print(f"  [error] {label}: {type(e).__name__}: {e}")
            results[label] = {"composition": comp_str, "error": str(e)}

    Path(args.out).write_text(json.dumps({
        "method": "grand-potential ESW via PhaseDiagram.get_element_profile "
                  "(Mo/Ong/Ceder 2012); MP GGA_GGA+U corrected hull; Li opened.",
        "elements": args.elements,
        "mu_Li_ref_eV": round(mu_Li_ref, 4),
        "voltage_convention": "V = mu_Li(metal) - mu_Li; 0 V = Li metal",
        "results": results,
    }, indent=2))
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
