#!/usr/bin/env python3
"""aggregate_interface_campaign.py — mean +/- std over seeds of the interface-decomp
metrics, per system. Reads interface_decomp_<sys>_s<seed>.csv (written by
analyze_interface_decomp.py) and reports the seed-averaged initial->final change +
error bars, so the b2o3-vs-undoped decomposition contrast gets a real uncertainty.

  python3 tools/oxidation/aggregate_interface_campaign.py db/properties "2 3 4" \
    --out db/properties/interface_campaign_summary.csv
"""
import argparse
import csv
import glob
import os
import re
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dbdir")
    ap.add_argument("seeds", nargs="?", default="2 3 4")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    files = glob.glob(os.path.join(a.dbdir, "interface_decomp_*_s*.csv"))
    sysd = {}
    for f in files:
        m = re.search(r"interface_decomp_(.+)_s(\d+)\.csv", os.path.basename(f))
        if m:
            sysd.setdefault(m.group(1), []).append(f)

    rows_out = []
    for sysn, fs in sorted(sysd.items()):
        agg = {}
        for f in fs:
            d = np.genfromtxt(f, delimiter=",", names=True)
            i0, iN = d[0], d[-1]
            for col in d.dtype.names:
                if col in ("frame", "t_ps"):
                    continue
                agg.setdefault(col + "_init", []).append(float(i0[col]))
                agg.setdefault(col + "_final", []).append(float(iN[col]))
            ps0 = float(i0["P_S"])
            agg.setdefault("PS_loss_pct", []).append((ps0 - float(iN["P_S"])) / ps0 * 100 if ps0 else 0.0)

        print(f"\n=== {sysn}  (n={len(fs)} seeds) ===")
        print(f"  PS_loss%          : {np.mean(agg['PS_loss_pct']):5.0f} +/- {np.std(agg['PS_loss_pct']):.0f}")
        print(f"  P-Li final (Li3P) : {np.mean(agg['P_Li_final']):5.2f} +/- {np.std(agg['P_Li_final']):.2f}")
        print(f"  S-Li final (Li2S) : {np.mean(agg['S_Li_final']):5.2f} +/- {np.std(agg['S_Li_final']):.2f}")
        print(f"  Li penetrated     : {np.mean(agg['Li_penetrated_final']):5.0f} +/- {np.std(agg['Li_penetrated_final']):.0f}")
        if "B_Li_final" in agg:
            print(f"  B-Li final (LiB)  : {np.mean(agg['B_Li_final']):5.2f} +/- {np.std(agg['B_Li_final']):.2f}")

        summ = {"system": sysn, "n_seeds": len(fs)}
        for k, v in agg.items():
            summ[k + "_mean"] = round(np.mean(v), 4)
            summ[k + "_std"] = round(np.std(v), 4)
        rows_out.append(summ)

    if a.out and rows_out:
        keys = ["system", "n_seeds"] + sorted(set().union(*[set(r) - {"system", "n_seeds"} for r in rows_out]))
        with open(a.out, "w", newline="") as fo:
            w = csv.DictWriter(fo, fieldnames=keys)
            w.writeheader()
            for r in rows_out:
                w.writerow(r)
        print(f"\n-> {a.out}")


if __name__ == "__main__":
    main()
