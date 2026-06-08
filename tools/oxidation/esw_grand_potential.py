#!/usr/bin/env python3
"""esw_grand_potential.py — REAL electrochemical stability window (ESW)
via the grand-potential phase-diagram method (Ong 2008; Mo/Ong/Ceder 2012,
Chem. Mater. 24, 15; Zhu/He/Mo 2015, JMCA).

This is the genuine ESW — NOT the qualitative "competing-phase energy span"
hint produced by tools/doping/esw_check.py. Here the Li reservoir is opened
(grand canonical, chemical potential μ_Li scanned) and the compound's
grand-potential decomposition energy is evaluated at every applied potential.

Method
------
1. Pull every Materials-Project entry in the Li-P-S-Cl quaternary
   (already MP2020-corrected: sulfide/halide anion corrections applied).
2. Build the closed PhaseDiagram → reference μ_Li(metal) = E(Li bcc)/atom,
   and the convex-hull energy E_hull(x) at the TARGET composition x.
3. For an applied potential φ (V vs Li/Li+):
        μ_Li(φ) = μ_Li(metal) − e·φ          (e = 1, energies in eV)
   Build the GrandPotentialPhaseDiagram at μ_Li(φ) and evaluate the target's
   grand-potential energy-above-hull e_above_hull^Φ.
4. The compound is electrochemically stable where e_above_hull^Φ ≤ tol.
   • Cathodic limit (reduction, low φ)  = lower edge of that window.
   • Anodic   limit (oxidation, high φ) = upper edge.
   At each edge the equilibrium decomposition products are reported.

Energy convention for the target
--------------------------------
By default the target is placed at the MP convex-hull energy of its
composition (energy_mode='hull') — i.e. treated as an ideal, marginally
stable line phase. This gives the INTRINSIC thermodynamic window of the
composition on a footing consistent with MP, and lets a non-MP /
non-stoichiometric composition (modelc Li5.4PS4.4Cl1.6) be compared
apples-to-apples with an MP phase (comp1 Li6PS5Cl). Pass energy_mode='mp'
to instead use the real MP entry energy of an existing phase (shows whether
the phase is itself stable/metastable; only valid if the exact phase is in MP).

Usage (run on a machine with MP_API_KEY set, e.g. gabia/kserver116-27):
    python3 esw_grand_potential.py \
        --target "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --phi_max 5.0 --dphi 0.01 --tol 1e-3 \
        --out esw_lpscl_results.json
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np


def get_chemsys_entries(elements):
    """Return MP2020-corrected ComputedEntries for the chemsys. Tries the
    modern mp_api client first, falls back to legacy pymatgen MPRester."""
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    chemsys = "-".join(sorted(elements))
    try:
        from mp_api.client import MPRester
        with MPRester(key) as mpr:
            entries = mpr.get_entries_in_chemsys(elements)
        print(f"[mp_api] {len(entries)} entries in {chemsys}")
        return entries
    except Exception as e:
        print(f"[mp_api] failed ({type(e).__name__}: {e}); trying legacy MPRester")
        from pymatgen.ext.matproj import MPRester as LegacyMPRester
        with LegacyMPRester(key) as mpr:
            entries = mpr.get_entries_in_chemsys(elements)
        print(f"[legacy] {len(entries)} entries in {chemsys}")
        return entries


def scan_window(entries, comp, e_target, mu_Li_ref, phi_grid, tol):
    """Scan applied potential; return per-φ grand e_above_hull and window."""
    from pymatgen.core import Element, Composition
    from pymatgen.analysis.phase_diagram import (
        GrandPotentialPhaseDiagram, GrandPotPDEntry, PDEntry)

    Li = Element("Li")
    target = PDEntry(comp, e_target)  # total energy (eV) at this composition
    n_atoms = comp.num_atoms

    rows = []
    for phi in phi_grid:
        mu_Li = mu_Li_ref - phi  # eV; e=1
        try:
            gpd = GrandPotentialPhaseDiagram(entries, {Li: mu_Li})
            g_target = GrandPotPDEntry(target, {Li: mu_Li})
            _, ehull = gpd.get_decomp_and_e_above_hull(g_target,
                                                       allow_negative=True)
        except Exception:
            ehull = float("nan")
        rows.append((float(phi), float(ehull)))

    # contiguous stable window: e_above_hull <= tol
    stable_phi = [p for p, e in rows if np.isfinite(e) and e <= tol]
    window = None
    if stable_phi:
        window = (min(stable_phi), max(stable_phi))
    return rows, window, target


def decomp_at(entries, comp, mu_Li, target):
    """Equilibrium grand-potential decomposition products at a given μ_Li."""
    from pymatgen.core import Element
    from pymatgen.analysis.phase_diagram import (
        GrandPotentialPhaseDiagram, GrandPotPDEntry)
    Li = Element("Li")
    gpd = GrandPotentialPhaseDiagram(entries, {Li: mu_Li})
    g_target = GrandPotPDEntry(target, {Li: mu_Li})
    decomp, _ = gpd.get_decomp_and_e_above_hull(g_target, allow_negative=True)
    out = {}
    for e, amt in decomp.items():
        f = e.original_entry.composition.reduced_formula \
            if hasattr(e, "original_entry") else e.composition.reduced_formula
        out[f] = out.get(f, 0.0) + float(amt)
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", nargs="+", required=True,
                    help='comp:label, e.g. "Li6PS5Cl:comp1" '
                         '"Li5.4P1S4.4Cl1.6:modelc"')
    ap.add_argument("--elements", nargs="+", default=["Li", "P", "S", "Cl"])
    ap.add_argument("--phi_max", type=float, default=5.0,
                    help="max applied potential V vs Li to scan")
    ap.add_argument("--dphi", type=float, default=0.01)
    ap.add_argument("--tol", type=float, default=1e-3,
                    help="grand e_above_hull tolerance (eV/atom) for 'stable'")
    ap.add_argument("--energy_mode", choices=["hull", "mp"], default="hull",
                    help="hull = place target at MP convex-hull energy of its "
                         "composition (default, composition-only, consistent "
                         "across MP & non-MP); mp = use real MP entry energy "
                         "(only if exact phase in MP)")
    ap.add_argument("--out", default="esw_grand_potential_results.json")
    args = ap.parse_args()

    from pymatgen.core import Element, Composition
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    entries = get_chemsys_entries(args.elements)
    pd = PhaseDiagram(entries)
    Li = Element("Li")
    mu_Li_ref = min(e.energy_per_atom for e in entries
                    if e.composition.reduced_formula == "Li")
    print(f"μ_Li(metal) reference = {mu_Li_ref:.4f} eV/atom")

    # map reduced_formula -> lowest-energy MP entry (for energy_mode='mp')
    best_mp = {}
    for e in entries:
        rf = e.composition.reduced_formula
        if rf not in best_mp or e.energy_per_atom < best_mp[rf].energy_per_atom:
            best_mp[rf] = e

    phi_grid = np.arange(0.0, args.phi_max + 1e-9, args.dphi)
    results = {}

    for spec in args.target:
        comp_str, _, label = spec.partition(":")
        label = label or comp_str
        comp = Composition(comp_str)
        rf = comp.reduced_formula

        if args.energy_mode == "mp" and rf in best_mp:
            mp_e = best_mp[rf]
            # scale energy to the given composition's atom count
            e_target = mp_e.energy_per_atom * comp.num_atoms
            e_hull = pd.get_hull_energy(comp)
            e_above_hull_0 = (e_target - e_hull) / comp.num_atoms
            esrc = f"MP entry {getattr(mp_e,'entry_id','?')} " \
                   f"(e_above_hull={e_above_hull_0:.4f} eV/atom)"
        else:
            e_target = pd.get_hull_energy(comp)
            e_above_hull_0 = 0.0
            esrc = "MP convex-hull energy of composition (ideal line phase)"

        print(f"\n=== {label}  {comp_str}  ({rf}) ===")
        print(f"  energy source: {esrc}")

        rows, window, target = scan_window(
            entries, comp, e_target, mu_Li_ref, phi_grid, args.tol)

        edges = {}
        if window:
            cath, anod = window
            print(f"  STABLE window: {cath:.2f} – {anod:.2f} V vs Li  "
                  f"(width {anod - cath:.2f} V)")
            # decomposition just OUTSIDE each edge
            d_phi = args.dphi
            cath_red = decomp_at(entries, comp, mu_Li_ref - (cath - d_phi),
                                 target) if cath - d_phi >= 0 else {}
            anod_ox = decomp_at(entries, comp, mu_Li_ref - (anod + d_phi),
                                target)
            print(f"  ↓ cathodic (reduction) limit {cath:.2f} V → {cath_red}")
            print(f"  ↑ anodic   (oxidation) limit {anod:.2f} V → {anod_ox}")
            edges = {
                "cathodic_limit_V": round(cath, 3),
                "anodic_limit_V": round(anod, 3),
                "window_width_V": round(anod - cath, 3),
                "reduction_products": cath_red,
                "oxidation_products": anod_ox,
            }
        else:
            print("  no stable window found in scan range")

        results[label] = {
            "composition": comp_str,
            "reduced_formula": rf,
            "energy_mode": args.energy_mode,
            "energy_source": esrc,
            "e_above_hull_0V_eV_per_atom": round(e_above_hull_0, 5),
            "mu_Li_ref_eV": round(mu_Li_ref, 4),
            **edges,
            "profile_phi_ehull": [[round(p, 3), round(e, 5)]
                                  for p, e in rows],
        }

    Path(args.out).write_text(json.dumps({
        "method": "grand-potential ESW (Mo/Ong/Ceder 2012); MP2020-corrected "
                  "MP entries; Li reservoir opened, μ_Li scanned.",
        "elements": args.elements,
        "phi_max_V": args.phi_max,
        "dphi_V": args.dphi,
        "tol_eV_per_atom": args.tol,
        "mu_Li_ref_eV": round(mu_Li_ref, 4),
        "results": results,
    }, indent=2))
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
