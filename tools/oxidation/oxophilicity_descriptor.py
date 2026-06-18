#!/usr/bin/env python3
"""oxophilicity_descriptor.py — Is Nd a SPECIAL O-getter, or just an O-carrier?

The physical question (O-only / Nd-only is non-physical; Nd2O3 is the real
co-dopant). The meaningful comparison is: among oxide co-dopants that ALL
deliver O, does the Nd(3+) cation do something the others don't?

This MP descriptor ranks cations by OXOPHILICITY = how much M prefers bonding
O over S (the driving force that pulls O into a sulfide and holds it):

    oxophilicity(M) = Ef_per_anion(best M-sulfide) - Ef_per_anion(best M-oxide)
                      [eV/anion]   (>0 => prefers O; bigger => stronger getter)

It is a SCREEN, not proof: the rigorous number is the DFT O-incorporation
energy in the modelc host (see oxophilicity_dft_campaign.md). But if Nd ranks
far above plain O-carriers (Li/Mg/Al), that quantitatively supports "Nd is a
strong O-getter" with a one-shot MP query (no doped-cell DFT).

Run where MP reachable (kserver116 / gabia):
    python3 oxophilicity_descriptor.py --out oxophilicity.json
"""
import argparse, json, os
from collections import defaultdict

# realistic oxide co-dopant cations to compare against Nd
CATIONS = ["Nd", "La", "Ce", "Y", "Sm", "Gd",   # rare-earth / trivalent (Nd family)
           "Sc", "In", "Ga", "Al",              # other trivalent
           "Mg", "Ca", "Zn",                    # divalent O-carriers
           "Li", "Na",                          # monovalent (pure-O reference: Li2O)
           "Zr", "Ti", "Ta", "Nb"]              # high-valent (coating oxides)

def anion_count(comp, anion):
    return comp.get_el_amt_dict().get(anion, 0.0)

def best_per_anion(entries, pd, anion):
    """min formation energy per anion over all M-anion binaries (no Li/other)."""
    from pymatgen.core import Composition
    best = None
    for e in entries:
        comp = e.composition
        els = set(str(el) for el in comp.elements)
        # binary M-anion only
        n_an = anion_count(comp, anion)
        if n_an <= 0:
            continue
        ef = pd.get_form_energy_per_atom(e)         # eV/atom (hull-referenced)
        ef_per_anion = ef * comp.num_atoms / n_an
        if best is None or ef_per_anion < best[0]:
            best = (ef_per_anion, e.composition.reduced_formula, round(ef, 4))
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="oxophilicity.json")
    args = ap.parse_args()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("set MP_API_KEY (run on kserver116/gabia)")
    from mp_api.client import MPRester
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    rows = {}
    with MPRester(key) as mpr:
        for M in CATIONS:
            try:
                ox = mpr.get_entries_in_chemsys([M, "O"],
                        additional_criteria={"thermo_types": ["GGA_GGA+U"]})
                su = mpr.get_entries_in_chemsys([M, "S"],
                        additional_criteria={"thermo_types": ["GGA_GGA+U"]})
                pd_ox = PhaseDiagram(ox); pd_su = PhaseDiagram(su)
                bo = best_per_anion(ox, pd_ox, "O")
                bs = best_per_anion(su, pd_su, "S")
                if not bo or not bs:
                    rows[M] = {"note": "missing oxide or sulfide"}; continue
                oxoph = bs[0] - bo[0]   # eV/anion, >0 prefers O
                rows[M] = {"oxophilicity_eV_per_anion": round(oxoph, 3),
                           "best_oxide": bo[1], "Ef_O_per_anion": round(bo[0], 3),
                           "best_sulfide": bs[1], "Ef_S_per_anion": round(bs[0], 3)}
                print(f"{M:3s}  oxophilicity={oxoph:6.3f}  ox={bo[1]:12s}({bo[0]:.2f})  "
                      f"su={bs[1]:12s}({bs[0]:.2f})")
            except Exception as e:
                rows[M] = {"error": str(e)[:80]}; print(f"{M}: ERR {e}")

    ranked = sorted([(v.get("oxophilicity_eV_per_anion", -99), m)
                     for m, v in rows.items()], reverse=True)
    out = {"descriptor": "oxophilicity = Ef/anion(sulfide) - Ef/anion(oxide); >0 prefers O",
           "method": "MP GGA_GGA+U hull, pymatgen PhaseDiagram.get_form_energy_per_atom",
           "ranking_most_to_least_oxophilic": [m for _, m in ranked if _ > -99],
           "Nd_rank": [i for i, (_, m) in enumerate(ranked) if m == "Nd"],
           "data": rows,
           "interpretation": "If Nd ranks ABOVE plain O-carriers (Li/Mg/Al/Zn), the Nd3+ "
               "cation has a genuine extra O-affinity (getter) -> supports a Nd-specific role "
               "in stabilizing O in the sulfide. If Nd ~ Li/Mg, Nd is just an O-carrier. "
               "La/Ce/Y comparison isolates rare-earth vs Nd-4f specificity."}
    json.dump(out, open(args.out, "w"), indent=1)
    print(f"\nwrote {args.out}\nNd rank (0=most oxophilic): {out['Nd_rank']}")

if __name__ == "__main__":
    main()
