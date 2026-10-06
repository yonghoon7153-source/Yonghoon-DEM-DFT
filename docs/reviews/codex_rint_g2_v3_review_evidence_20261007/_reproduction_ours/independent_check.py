"""Independent check of the numbers PRINTED in the Codex Rint G2 v3 verdict (10-07).

Not a copy of the Codex probes: the inputs are the decimal literals printed in the
verdict text (§2 table, §3 code block, §5 table, §7-2), fed to our own code.
Only scripts/step3_sigma.py `rasterize` is imported from our checkout (for §3).

Usage: python3 -I -B independent_check.py <repo_root> <out.json>
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np


def eps_tie():
    eps = 1e-6                                     # µm²  (verdict §2)
    centres = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
    radii = [0.9999992499997188, 1.4142132972080272, 2.2360679774997900]   # verdict §2 table
    x = (0.0, 0.0, 0.0)                            # observation point
    p = [sum((xi - ci) ** 2 for xi, ci in zip(x, c)) - r * r for c, r in zip(centres, radii)]

    def pair(i, j):                                # v3 L78 read as a pairwise comparator
        if abs(p[i] - p[j]) <= eps:
            return min((i, j), key=lambda k: centres[k])
        return i if p[i] < p[j] else j

    fold = {}
    for perm in itertools.permutations(range(3)):
        w = perm[0]
        for k in perm[1:]:
            w = pair(w, k)
        fold["".join(map(str, perm))] = w
    setrule = {}
    for perm in itertools.permutations(range(3)):
        pmin = min(p[k] for k in perm)             # global minimum over the claimant SET
        band = [k for k in perm if p[k] <= pmin + eps]
        # complete canonical key = (centre, radius); row index never used
        setrule["".join(map(str, perm))] = min(band, key=lambda k: (centres[k], radii[k]))
    conc = [1.0, 1.0000002499999687]                # same centre, different radius (verdict §2)
    # power at any observation point x: |x-c|^2 - r^2 -> difference = r1^2 - r0^2 (x-independent)
    cwin = {}
    for perm in ([0, 1], [1, 0]):                   # centre-only key: the two keys are EQUAL
        cwin["".join(map(str, perm))] = min(perm, key=lambda k: (0.0, 0.0, 0.0))
    return {"power_um2": p,
            "pairwise": {"0_vs_1": pair(0, 1), "1_vs_2": pair(1, 2), "2_vs_0": pair(2, 0)},
            "sequential_fold_winner_by_input_order": fold,
            "set_rule_band": [k for k in range(3) if p[k] <= min(p) + eps],
            "set_rule_winner_by_input_order": setrule,
            "concentric_power_difference_um2": conc[1] ** 2 - conc[0] ** 2,
            "concentric_within_eps": (conc[1] ** 2 - conc[0] ** 2) <= eps,
            "concentric_centre_only_key_winner_by_input_order": cwin}


def raw_mask(repo):
    sys.path.insert(0, str(Path(repo) / "scripts"))
    import step3_sigma as s3
    c = np.array([[1.9748831001799223, 1.8791293045780670, 1.7896943576126298],    # verdict §3
                  [1.0611990064053260, 0.8549090548944595, 1.7364778658264648]])
    r = np.array([0.5348361452776790, 0.8437277367739292])
    t = np.array([2, 1])
    lo, hi, vox, bridge = np.zeros(3), np.full(3, 3.2), 0.1, 0.24
    q = np.array([15, 15, 15])
    out = {"orders": {}}
    grids = {}
    for perm in ([0, 1], [1, 0]):
        sid, _ = s3.rasterize(c[perm], r[perm], t[perm], None, None, lo, hi, vox, bridge_um=bridge)
        a, b = c[perm]
        ra, rb = r[perm]
        d = float(np.linalg.norm(a - b))           # same expression as step3_sigma.py L577–579
        mid = a + (b - a) * (ra + 0.5 * (d - ra - rb)) / max(d, 1e-12)
        g = (q + 0.5 - (mid - lo) / vox)
        key = "".join(map(str, perm))
        grids[key] = sid
        out["orders"][key] = {"bridge_centre_um": mid.tolist(),
                              "cell_15_15_15_dist2_over_h2": float(np.sum(g ** 2)),
                              "bridge_r2_over_h2": (bridge / vox) ** 2,
                              "sid_at_15_15_15": int(sid[15, 15, 15]),
                              "AM_mask_cells": int(np.isin(sid, [1, 2]).sum()),
                              "sid1_cells": int((sid == 1).sum()), "sid2_cells": int((sid == 2).sum())}
    diff = np.argwhere(np.isin(grids["01"], [1, 2]) != np.isin(grids["10"], [1, 2]))
    out["changed_AM_mask_cells"] = diff.tolist()
    out["changed_cell_centre_um"] = [((k + 0.5) * vox).tolist() for k in diff]
    return out


def beta_q():
    beta, f = -0.03125, (1.0 / 5.0) ** 3             # verdict §7 (a=1, L/a=5)
    k = (1 + 2 * beta * f) / (1 - beta * f)
    q_num = (k - 1) / f
    q_an = 3 * beta / (1 - beta * f)
    return {"beta": beta, "f": f, "keff_over_km": k, "q_num": q_num, "q_analytic": q_an,
            "q_num_minus_q_analytic": q_num - q_an,
            "beta_reconstructed_q_over_3_plus_qf": q_num / (3 + q_num * f),
            "wrong_pairing_beta_minus_q_analytic": beta - q_an}


def carbon():
    par = lambda a, b: 1.0 / (1.0 / a + 1.0 / b)
    c = 0.02
    return {"film2_par_carbon": par(2.0, c), "film1_par_carbon": par(1.0, c), "film0_carbon_only": c,
            "carbon_current_share_with_2ohm": (1 / c) / (1 / c + 1 / 2.0),
            "film_log_sensitivity_with_2ohm": (1 / 2.0) / (1 / c + 1 / 2.0)}


def main():
    repo, out = sys.argv[1], Path(sys.argv[2])
    res = {"inputs": "decimal literals printed in codex_review_rint_g2_v3_20261007.md §2 §3 §5 §7",
           "numpy": np.__version__, "python": sys.version.split()[0],
           "RINTV3_01_eps_tie": eps_tie(), "RINTV3_02_raw_mask": raw_mask(repo),
           "RINTV3_03_beta_q": beta_q(), "R4_carbon_bypass": carbon()}
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
