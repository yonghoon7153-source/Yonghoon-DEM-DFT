#!/usr/bin/env python3
"""esw_cascade_batch.py — grand-potential ESW (oxidation/reduction window) for
EVERY doped-argyrodite champion in the cascade. Fast: needs only composition +
MP hull (no DFT). Same method as tools/oxidation/esw_grand_potential.py
(Mo/Ong/Ceder get_element_profile), looped over the cascade champions.

Run on gabia/kserver116 (MP_API_KEY set, mp_api + pymatgen in env):
    python3 esw_cascade_batch.py \
        --csv /data/work/repo/db/properties/cascade_v23_all.csv \
        --out /data/work/repo/db/properties/oxidation_stability_cascade.json

Reads rank_combined==1 rows, builds Composition from composition_* columns,
runs the grand-potential Li-evolution profile, and records per champion:
  reduction_limit_V, oxidation_limit_V, ocv_self_decomposition_V + onset rxns.
Caches the MP hull per chemsys so dopants sharing a chemsys pull once.
"""
import argparse, csv, json, os, math
from collections import defaultdict

def fnum(s):
    try: return float(s)
    except: return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="/data/work/repo/db/properties/cascade_v23_all.csv")
    ap.add_argument("--out", default="/data/work/repo/db/properties/oxidation_stability_cascade.json")
    ap.add_argument("--rank", default="1", help="rank_combined value to keep (champion)")
    a = ap.parse_args()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key: raise SystemExit("Set MP_API_KEY (run on gabia).")
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    from mp_api.client import MPRester
    Li = Element("Li")

    # ---- gather champion compositions ----
    champs = []
    for r in csv.DictReader(open(a.csv)):
        if r.get("rank_combined") != a.rank: continue
        comp = {}
        for k, v in r.items():
            if k.startswith("composition_") and v not in ("", None):
                n = fnum(v)
                if n and n > 0: comp[k.split("composition_")[1]] = n
        if not comp: continue
        champs.append((r.get("_dir", r.get("name", "?")), r.get("dopant", "?"), comp))
    print(f"{len(champs)} champions with composition")

    # ---- group by chemsys, pull each hull once ----
    by_sys = defaultdict(list)
    for name, dop, comp in champs:
        by_sys[tuple(sorted(comp))].append((name, dop, comp))

    results = {}
    for sys_els, items in by_sys.items():
        els = list(sys_els)
        try:
            with MPRester(key) as mpr:
                entries = mpr.get_entries_in_chemsys(els,
                    additional_criteria={"thermo_types": ["GGA_GGA+U"]})
            pd = PhaseDiagram(entries)
            muref = pd.el_refs[Li].energy_per_atom
        except Exception as e:
            for name, dop, comp in items:
                results[name] = {"dopant": dop, "error": f"hull: {str(e)[:120]}"}
            print(f"  [{'-'.join(els)}] hull FAIL: {str(e)[:80]}")
            continue
        print(f"  [{'-'.join(els)}] {len(entries)} entries -> {len(items)} champ")
        for name, dop, comp in items:
            try:
                c = Composition(comp)
                prof = pd.get_element_profile(Li, c)
                steps = [{"V": round(muref - float(p["chempot"]), 3),
                          "evo": round(float(p["evolution"]), 4),
                          "rxn": str(p["reaction"])} for p in prof]
                pos = [s for s in steps if s["evo"] > 1e-6]
                neg = [s for s in steps if s["evo"] < -1e-6]
                neu = [s for s in steps if abs(s["evo"]) <= 1e-6]
                red = max((s["V"] for s in pos), default=None)
                ox = min((s["V"] for s in neg), default=None)
                ocv = min((s["V"] for s in neu), default=None)
                def rxn_at(v): return min(steps, key=lambda s: abs(s["V"]-v))["rxn"] if v is not None else None
                results[name] = {"dopant": dop, "elements": els,
                    "reduction_limit_V": red, "oxidation_limit_V": ox,
                    "ocv_self_decomposition_V": ocv,
                    "oxidation_onset_rxn": rxn_at(ox), "ocv_rxn": rxn_at(ocv),
                    "window_V": (round(ox-red,3) if (ox is not None and red is not None) else None),
                    "n_breakpoints": len(steps)}
            except Exception as e:
                results[name] = {"dopant": dop, "error": str(e)[:120]}

    json.dump({"method": "grand-potential ESW (get_element_profile, MP GGA_GGA+U); per cascade champion",
               "source_csv": a.csv, "results": results}, open(a.out, "w"), indent=2)
    print(f"\n-> {a.out}")
    # compact summary (paste-friendly)
    print(f"\n{'champion':18s} {'ox_V':>6s} {'red_V':>6s} {'ocv_V':>6s} {'win_V':>6s}")
    for name in sorted(results):
        d = results[name]
        if "error" in d: print(f"{name:18s} ERROR {d['error'][:50]}"); continue
        print(f"{name:18s} {str(d['oxidation_limit_V']):>6s} {str(d['reduction_limit_V']):>6s} "
              f"{str(d['ocv_self_decomposition_V']):>6s} {str(d['window_V']):>6s}")

if __name__ == "__main__":
    main()
