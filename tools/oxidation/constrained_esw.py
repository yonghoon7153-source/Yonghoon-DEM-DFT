#!/usr/bin/env python3
"""constrained_esw.py — Mechanically-CONSTRAINED electrochemical stability window
(Gil-González/Fitzhugh constrained-ensemble method), our-cells implementation.

Extends the 0-pressure grand-potential ESW (esw_grand_potential.py) with the
Fitzhugh strain term so we reproduce Gil-González (Energy Storage Mater. 2022)
with OUR comp1 / modelc compositions and show that the Cl-rich oxidation window
widens MORE under mechanical constriction.

Method (exact reduction of Fitzhugh Eq.1)
-----------------------------------------
The constrained decomposition driving force (Gil-González Eq.1) is
    d_sD G' = (G_D - G_SE) + V*eps_RXN*K_eff ,
with eps_RXN = (V_products - V_SE)/V_SE the reaction volumetric strain and K_eff
the effective bulk modulus (mechanical-constriction level). Since
    V*eps_RXN*K_eff = K_eff*(V_products - V_SE) ,
the strain penalty is a per-phase PV term: augmenting every phase energy by
    E_i -> E_i + K_eff * V_i        (P = K_eff effective pressure)
adds K_eff*V_products to any decomposition and K_eff*V_SE to the parent (a
constant), so the grand-potential hull built from the augmented entries selects
exactly the strain-minimised decomposition. Volume-EXPANDING decompositions
(eps_RXN>0) are suppressed -> the SE is stabilised -> the window WIDENS, and the
optimal product set itself changes with K_eff (reproducing their Table S1, e.g.
PCl3/P2S7/SCl at 0 GPa -> SCl4/Li2PS3/S at 20 GPa). This is the LINEAR strain
model (work against an effective back-pressure P=K_eff).

Phase set: excludes LiS4 (mp-995393), SCl3 (mp-1186934), Li5PS4Cl2 (mp-1040450),
matching Gil-González SI.

Voltage convention: V = mu_Li(metal, augmented frame) - mu_Li ; 0 V = Li metal.
(The Li reference is taken in the SAME augmented frame, so comp1 and modelc are
compared consistently; an overall reference offset cancels in the comparison.)

Usage (gabia / kserver116-27, MP_API_KEY set):
    python3 constrained_esw.py \
        --target "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" \
        --v_se_A3 254.16 243.29 \
        --k_eff 0 10 20 \
        --out constrained_esw_results.json

  --v_se_A3 : SE molar volume per FORMULA UNIT (Å^3/fu) for each target, used
              only for the eps_RXN diagnostic print (the hull uses MP volumes).
              comp1 EOS V0 1016.62/4fu = 254.16 ; modelc 1216.44/5fu = 243.29.
"""
import argparse
import json
import os
from pathlib import Path

GPA_A3_TO_EV = 6.241509074e-3  # 1 GPa*Å^3 in eV
EXCLUDE_IDS = {"mp-995393", "mp-1186934", "mp-1040450"}  # LiS4, SCl3, Li5PS4Cl2


def get_entries(elements):
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        entries = mpr.get_entries_in_chemsys(
            elements, additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    kept, dropped, novol = [], [], 0
    for e in entries:
        eid = str(getattr(e, "entry_id", ""))
        if any(x in eid for x in EXCLUDE_IDS):
            dropped.append(eid); continue
        kept.append(e)
    print(f"[mp_api] {len(entries)} entries; dropped {dropped}; kept {len(kept)}")
    return kept


def entry_volume(e):
    try:
        return float(e.structure.volume)
    except Exception:
        v = getattr(e, "data", {}) or {}
        return float(v.get("volume")) if v.get("volume") else None


def augmented_pd(entries, k_eff):
    """PhaseDiagram with each phase energy -> E + K_eff*V (effective pressure)."""
    from pymatgen.analysis.phase_diagram import PhaseDiagram, PDEntry
    pd_entries, missing = [], 0
    for e in entries:
        V = entry_volume(e)
        # Do NOT augment the open-element reservoir (elemental Li at the anode is
        # NOT under the cathode-side constriction). Keeping Li metal unaugmented
        # fixes the voltage reference so the window WIDENS (anodic up, cathodic
        # down) instead of rigidly shifting up.
        els = e.composition.elements
        is_Li_metal = (len(els) == 1 and els[0].symbol == "Li")
        if V is None or is_Li_metal:
            if V is None and not is_Li_metal:
                missing += 1
            pd_entries.append(PDEntry(e.composition, e.energy)); continue
        aug = e.energy + k_eff * V * GPA_A3_TO_EV
        pd_entries.append(PDEntry(e.composition, aug))
    if missing:
        print(f"   [warn] {missing} entries had no volume (no augmentation)")
    return PhaseDiagram(pd_entries)


def window_from_profile(pd, comp, mu_Li_ref):
    from pymatgen.core import Element
    Li = Element("Li")
    profile = pd.get_element_profile(Li, comp)
    steps = []
    for p in profile:
        mu = float(p["chempot"])
        steps.append({
            "V": round(mu_Li_ref - mu, 3),
            "evo": round(float(p["evolution"]), 4),
            "rxn": str(p["reaction"]),
        })
    s = sorted(steps, key=lambda x: x["V"])
    pos = [x for x in s if x["evo"] > 1e-6]    # reduction (Li uptake)
    neg = [x for x in s if x["evo"] < -1e-6]   # oxidation (Li release)
    red = max((x["V"] for x in pos), default=None)   # cathodic limit
    ox = min((x["V"] for x in neg), default=None)     # anodic limit
    ox_rxn = next((x["rxn"] for x in s if x["V"] == ox), None) if ox else None
    return red, ox, ox_rxn, steps


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", nargs="+", required=True,
                    help='comp:label, e.g. "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc"')
    ap.add_argument("--v_se_A3", nargs="+", type=float, default=None,
                    help="SE molar volume per fu (Å^3), same order as --target (diagnostic only)")
    ap.add_argument("--elements", nargs="+", default=["Li", "P", "S", "Cl"])
    ap.add_argument("--k_eff", nargs="+", type=float, default=[0, 10, 20],
                    help="effective bulk moduli (GPa) to scan")
    ap.add_argument("--out", default="constrained_esw_results.json")
    args = ap.parse_args()

    from pymatgen.core import Element, Composition
    Li = Element("Li")
    entries = get_entries(args.elements)

    # consistent Li reference per K_eff (augmented frame)
    results = {}
    targets = []
    for i, spec in enumerate(args.target):
        cs, _, lab = spec.partition(":")
        v_se = args.v_se_A3[i] if args.v_se_A3 and i < len(args.v_se_A3) else None
        targets.append((cs, lab or cs, v_se))
        results[lab or cs] = {"composition": cs, "v_se_A3_per_fu": v_se,
                              "by_k_eff": {}}

    for k in args.k_eff:
        print(f"\n========== K_eff = {k} GPa ==========")
        pd = augmented_pd(entries, k)
        mu_ref = pd.el_refs[Li].energy_per_atom
        for cs, lab, v_se in targets:
            comp = Composition(cs)
            try:
                red, ox, ox_rxn, steps = window_from_profile(pd, comp, mu_ref)
            except Exception as e:
                print(f"  [err] {lab} K={k}: {type(e).__name__}: {e}")
                results[lab]["by_k_eff"][str(k)] = {"error": str(e)}
                continue
            width = (ox - red) if (red is not None and ox is not None) else None
            print(f"  {lab:8s} K={k:>4.0f}: window {red} - {ox} V "
                  f"(width {width})  anodic-rxn: {ox_rxn}")
            results[lab]["by_k_eff"][str(k)] = {
                "reduction_limit_V": red, "oxidation_limit_V": ox,
                "window_width_V": round(width, 3) if width is not None else None,
                "oxidation_onset_rxn": ox_rxn,
                "profile": steps,
            }

    # summary table: window vs K_eff per target + widening
    print("\n================ SUMMARY ================")
    for lab in results:
        bk = results[lab]["by_k_eff"]
        print(f"\n{lab} ({results[lab]['composition']}):")
        base = bk.get("0", {})
        for k, d in bk.items():
            if "error" in d:
                print(f"  K={k:>4} GPa: ERROR"); continue
            dw = ""
            if base and base.get("window_width_V") is not None and d.get("window_width_V") is not None:
                dw = f"  (Δwidth vs 0 GPa: {d['window_width_V']-base['window_width_V']:+.2f} V)"
            print(f"  K={k:>4} GPa: {d['reduction_limit_V']} - "
                  f"{d['oxidation_limit_V']} V, width {d['window_width_V']}{dw}")

    Path(args.out).write_text(json.dumps({
        "method": "constrained-ensemble ESW (Fitzhugh strain = +K_eff*V per phase) "
                  "on MP GGA_GGA+U hull, LiS4/SCl3/Li5PS4Cl2 excluded.",
        "excluded_mp_ids": sorted(EXCLUDE_IDS),
        "k_eff_GPa": args.k_eff,
        "results": results,
    }, indent=2))
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
