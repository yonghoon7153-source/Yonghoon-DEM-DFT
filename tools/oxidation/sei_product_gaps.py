#!/usr/bin/env python3
"""sei_product_gaps.py — band gaps of the SEI / decomposition product phases.

After esw_grand_potential.py gives the decomposition reactions for the
Nd2O3-doped composition, this looks up the MP band gap of each product phase
(lowest-energy entry per formula) to test the claim that the doped-cell
interphase is ELECTRONICALLY INSULATING (wide-gap) -> blocks e- leakage even
though the BULK gap narrowed.

Run on gabia/kserver116 where MP_API_KEY is set + MP reachable:
    python3 sei_product_gaps.py --formulas Li3PO4 Li4P2O7 NdPO4 Nd2O3 Nd2S3 \
        NdCl3 Li2S LiCl Li3P Li3PS4 Li2O S --out sei_product_gaps.json

NOTE (consistency with kb/physics/260318 PBE+U-4f note):
  MP gaps are PBE/PBE+U. For Nd-bearing phases (NdPO4, Nd2O3, Nd2S3, NdCl3)
  the 4f mis-placement => MP gap is a LOWER BOUND (real gap larger; e.g. exp
  Nd2O3 ~4.7, NdCl3 ~5 eV). Nd-FREE phases (Li3PO4 ~ exp 8, Li2S, LiCl) are
  reliable. The script flags Nd-bearing rows accordingly.
"""
import argparse, json, os
from pathlib import Path

DEFAULT = ["Li3PO4", "Li4P2O7", "NdPO4", "Nd2O3", "Nd2S3", "NdCl3",
           "Li2S", "LiCl", "Li3P", "Li3PS4", "Li2O", "S"]
# rough experimental gaps for the key wide-gap insulators (sanity anchor, eV)
EXP_ANCHOR = {"Li3PO4": "~8 (exp)", "Li2O": "~7.99 (exp)", "LiCl": "~9.4 (exp)",
              "Nd2O3": "~4.7 (exp)", "NdCl3": "~5 (exp)", "NdPO4": "wide (monazite)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formulas", nargs="+", default=DEFAULT)
    ap.add_argument("--out", default="sei_product_gaps.json")
    args = ap.parse_args()

    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("Set MP_API_KEY (run on gabia/kserver116).")
    from mp_api.client import MPRester

    rows = {}
    with MPRester(key) as mpr:
        for f in args.formulas:
            try:
                docs = mpr.materials.summary.search(
                    formula=f,
                    fields=["material_id", "formula_pretty",
                            "energy_above_hull", "band_gap", "is_stable"])
                if not docs:
                    rows[f] = {"error": "no MP entry"}
                    continue
                # pick the ground state (lowest e_above_hull)
                d = min(docs, key=lambda x: (x.energy_above_hull or 9e9))
                has_nd = "Nd" in f
                rows[f] = {
                    "material_id": str(d.material_id),
                    "formula": d.formula_pretty,
                    "band_gap_MP_eV": round(float(d.band_gap), 3),
                    "e_above_hull": round(float(d.energy_above_hull or 0), 4),
                    "is_stable": bool(d.is_stable),
                    "Nd_bearing_gap_is_LOWER_BOUND": has_nd,
                    "exp_anchor": EXP_ANCHOR.get(f, ""),
                }
                tag = "  (Nd: LOWER BOUND)" if has_nd else ""
                print(f"  {f:10s}  {d.formula_pretty:12s}  "
                      f"gap_MP={float(d.band_gap):5.2f} eV  "
                      f"E_hull={float(d.energy_above_hull or 0):.3f}{tag}")
            except Exception as e:
                rows[f] = {"error": str(e)[:160]}
                print(f"  {f:10s}  [error] {str(e)[:80]}")

    Path(args.out).write_text(json.dumps({
        "note": "MP PBE/PBE+U band gaps of decomposition/SEI product phases. "
                "Nd-bearing gaps are lower bounds (4f mis-placement). "
                "Wide gaps => electronically insulating interphase.",
        "gaps": rows,
    }, indent=2))
    print(f"\n-> {args.out}")


if __name__ == "__main__":
    main()
