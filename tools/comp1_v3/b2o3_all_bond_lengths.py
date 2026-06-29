#!/usr/bin/env python3
"""b2o3_all_bond_lengths.py — comprehensive bond-length statistics.

Pure-numpy (no pymatgen/ASE needed) nearest-neighbour distance statistics on
the B2O3-doped champion (db/structures/b2o3_relaxV0.cif). Reports EVERY relevant
atom-pair type (cation-anion bonds, anion-anion cage contacts) with
mean/std/min/max/n, plus per-environment breakdowns:
  - P tetrahedra classified by O count (PS4 / PS3O / PS2O2) -> P-S, P-O per type
  - S classified by bonding (free-S / B-S / P-S bridging)
  - Cl classified 4a (octahedral, Z>=5) vs 4d (anti-site, Z<5) -> Li-Cl per site

Exact triclinic minimum image (search lattice translations in -1..1).

    python3 tools/comp1_v3/b2o3_all_bond_lengths.py \
        --cif db/structures/b2o3_relaxV0.cif \
        --json db/properties/b2o3_bond_lengths_full.json
"""
import argparse, json, re, itertools
import numpy as np


def parse_cif(path):
    a = b = c = al = be = ga = None
    syms, fr = [], []
    in_loop = False
    cols = []
    for line in open(path):
        s = line.strip()
        if s.startswith("_cell_length_a"): a = float(s.split()[1])
        elif s.startswith("_cell_length_b"): b = float(s.split()[1])
        elif s.startswith("_cell_length_c"): c = float(s.split()[1])
        elif s.startswith("_cell_angle_alpha"): al = float(s.split()[1])
        elif s.startswith("_cell_angle_beta"): be = float(s.split()[1])
        elif s.startswith("_cell_angle_gamma"): ga = float(s.split()[1])
        elif s.startswith("_atom_site_"):
            in_loop = True; cols.append(s)
        elif in_loop and s and not s.startswith("_") and not s.startswith("loop_"):
            t = s.split()
            if len(t) >= 5:
                syms.append(t[1])
                fr.append([float(t[2]), float(t[3]), float(t[4])])
    return (a, b, c, al, be, ga), syms, np.array(fr)


def lattice_matrix(a, b, c, al, be, ga):
    al, be, ga = np.radians([al, be, ga])
    ax, ay, az = a, 0.0, 0.0
    bx, by, bz = b * np.cos(ga), b * np.sin(ga), 0.0
    cx = c * np.cos(be)
    cy = c * (np.cos(al) - np.cos(be) * np.cos(ga)) / np.sin(ga)
    cz = np.sqrt(max(c * c - cx * cx - cy * cy, 0.0))
    return np.array([[ax, ay, az], [bx, by, bz], [cx, cy, cz]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", default="db/structures/b2o3_relaxV0.cif")
    ap.add_argument("--json", default="db/properties/b2o3_bond_lengths_full.json")
    args = ap.parse_args()

    cell, syms, fr = parse_cif(args.cif)
    L = lattice_matrix(*cell)
    syms = np.array(syms)
    N = len(syms)
    cart = fr @ L

    # exact minimum-image distance matrix (search translations -1..1)
    trans = np.array(list(itertools.product([-1, 0, 1], repeat=3))) @ L  # (27,3)
    D = np.full((N, N), 1e9)
    for i in range(N):
        diff = cart - cart[i]                         # (N,3)
        # for each j, min over 27 images
        dd = diff[:, None, :] + trans[None, :, :]     # (N,27,3)
        D[i] = np.sqrt((dd ** 2).sum(-1)).min(1)
    np.fill_diagonal(D, 1e9)

    def pairs(e1, e2, lo, hi):
        m1 = syms == e1; m2 = syms == e2
        out = []
        idx1 = np.where(m1)[0]; idx2 = np.where(m2)[0]
        for i in idx1:
            for j in idx2:
                if e1 == e2 and j <= i:
                    continue
                d = D[i, j]
                if lo <= d <= hi:
                    out.append((i, j, d))
        return out

    def stat(lst):
        if not lst:
            return None
        d = np.array([x[2] for x in lst])
        return dict(mean=round(float(d.mean()), 3), std=round(float(d.std()), 3),
                    min=round(float(d.min()), 3), max=round(float(d.max()), 3),
                    n=len(d))

    # --- bond cutoffs (first coordination shell) ---
    cat_anion = {
        "P-S": ("P", "S", 1.8, 2.5),
        "P-O": ("P", "O", 1.3, 1.9),
        "B-S": ("B", "S", 1.5, 2.2),
        "B-O": ("B", "O", 1.2, 1.8),
        "Li-S": ("Li", "S", 1.9, 3.2),
        "Li-Cl": ("Li", "Cl", 2.0, 3.4),
        "Li-O": ("Li", "O", 1.6, 2.8),
    }
    anion_anion = {
        "S-S(cage)": ("S", "S", 3.0, 3.8),
        "S-Cl": ("S", "Cl", 3.0, 4.2),
        "Cl-Cl": ("Cl", "Cl", 3.5, 4.6),
    }
    framework = {
        "P-P": ("P", "P", 3.5, 5.5),
        "Li-Li": ("Li", "Li", 2.0, 3.2),
    }

    result = {"bonds_cation_anion": {}, "anion_anion": {}, "framework": {}}
    for k, (e1, e2, lo, hi) in cat_anion.items():
        result["bonds_cation_anion"][k] = stat(pairs(e1, e2, lo, hi))
    for k, (e1, e2, lo, hi) in anion_anion.items():
        result["anion_anion"][k] = stat(pairs(e1, e2, lo, hi))
    for k, (e1, e2, lo, hi) in framework.items():
        result["framework"][k] = stat(pairs(e1, e2, lo, hi))

    # --- per-P environment (PS4 / PS3O / PS2O2) ---
    Pidx = np.where(syms == "P")[0]
    Sidx = np.where(syms == "S")[0]
    Oidx = np.where(syms == "O")[0]
    p_env = {}
    for p in Pidx:
        nS = [(s, D[p, s]) for s in Sidx if D[p, s] <= 2.5]
        nO = [(o, D[p, o]) for o in Oidx if D[p, o] <= 1.9]
        key = f"PS{len(nS)}" + (f"O{len(nO)}" if nO else "")
        p_env.setdefault(key, {"P-S": [], "P-O": [], "count": 0})
        p_env[key]["count"] += 1
        p_env[key]["P-S"] += [d for _, d in nS]
        p_env[key]["P-O"] += [d for _, d in nO]
    p_env_out = {}
    for k, v in p_env.items():
        ps = np.array(v["P-S"]); po = np.array(v["P-O"])
        p_env_out[k] = {
            "n_P": v["count"] // 1 if False else len(np.unique([1])) and v["count"],
            "P-S_mean": round(float(ps.mean()), 3) if len(ps) else None,
            "P-O_mean": round(float(po.mean()), 3) if len(po) else None,
        }
    # fix n_P
    for k in p_env_out:
        p_env_out[k]["n_P"] = p_env[k]["count"]
    result["P_environments"] = p_env_out

    # --- S classification (free-S / B-S / P-S bridging) ---
    Bidx = np.where(syms == "B")[0]
    s_class = {"free-S": [], "B-S": [], "P-S(bridge)": []}
    for s in Sidx:
        boundB = any(D[s, b] <= 2.2 for b in Bidx)
        boundP = any(D[s, p] <= 2.5 for p in Pidx)
        if boundB:
            s_class["B-S"].append(s)
        elif boundP:
            s_class["P-S(bridge)"].append(s)
        else:
            s_class["free-S"].append(s)
    # Li-S distance per S class
    Liidx = np.where(syms == "Li")[0]
    s_class_out = {}
    for k, slist in s_class.items():
        lis = []
        for s in slist:
            lis += [D[li, s] for li in Liidx if D[li, s] <= 3.2]
        lis = np.array(lis)
        s_class_out[k] = {
            "n_S": len(slist),
            "Li-S_mean": round(float(lis.mean()), 3) if len(lis) else None,
            "Li-S_std": round(float(lis.std()), 3) if len(lis) else None,
            "n_LiS": len(lis),
        }
    result["S_classification"] = s_class_out

    # --- Cl 4a/4d (octahedral Z>=5 vs anti-site Z<5) + per-site Li-Cl ---
    Clidx = np.where(syms == "Cl")[0]
    cl4a, cl4d = [], []
    for cl in Clidx:
        Z = sum(1 for li in Liidx if D[cl, li] <= 3.4)
        (cl4a if Z >= 5 else cl4d).append(cl)
    def licl(clset):
        d = [D[li, cl] for cl in clset for li in Liidx if D[li, cl] <= 3.4]
        d = np.array(d)
        return (dict(mean=round(float(d.mean()), 3), std=round(float(d.std()), 3),
                     min=round(float(d.min()), 3), max=round(float(d.max()), 3),
                     n=len(d)) if len(d) else None)
    result["Cl_sites"] = {
        "n_4a": len(cl4a), "n_4d": len(cl4d),
        "Li-Cl_4a": licl(cl4a), "Li-Cl_4d": licl(cl4d),
        "Li-Cl_all": licl(list(Clidx)),
    }

    # --- print ---
    print("=== cation-anion bonds ===")
    for k, v in result["bonds_cation_anion"].items():
        if v: print(f"  {k:7s} {v['mean']:.3f} +/- {v['std']:.3f}  "
                     f"[{v['min']:.3f},{v['max']:.3f}]  n={v['n']}")
    print("=== anion-anion contacts ===")
    for k, v in result["anion_anion"].items():
        if v: print(f"  {k:11s} {v['mean']:.3f} +/- {v['std']:.3f}  n={v['n']}")
    print("=== framework ===")
    for k, v in result["framework"].items():
        if v: print(f"  {k:7s} {v['mean']:.3f} +/- {v['std']:.3f}  n={v['n']}")
    print("=== P environments ===")
    for k, v in result["P_environments"].items():
        print(f"  {k:7s} n_P={v['n_P']}  P-S={v['P-S_mean']}  P-O={v['P-O_mean']}")
    print("=== S classification ===")
    for k, v in result["S_classification"].items():
        print(f"  {k:13s} n_S={v['n_S']:2d}  Li-S={v['Li-S_mean']} +/-{v['Li-S_std']} (n={v['n_LiS']})")
    print("=== Cl sites ===")
    cs = result["Cl_sites"]
    print(f"  4a n={cs['n_4a']}  Li-Cl={cs['Li-Cl_4a']}")
    print(f"  4d n={cs['n_4d']}  Li-Cl={cs['Li-Cl_4d']}")

    import os
    os.makedirs("db/properties", exist_ok=True) if os.path.dirname(args.json) else None
    json.dump(result, open(args.json, "w"), indent=2)
    print(f"\n-> {args.json}")


if __name__ == "__main__":
    main()
