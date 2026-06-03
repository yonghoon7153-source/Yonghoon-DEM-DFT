#!/usr/bin/env python3
"""Per-site bond environment for argyrodite Li-PS-X.

Splits bonds by anion site type:
  - 4a-Cl: octahedral Cl[Li6] cage center (Z=6, large V_poly)
  - 4d-Cl: tetrahedral Cl[Li4] anti-site at S-position (Z=4, small V_poly)
  - 4d-S : free S²⁻ at 4d site (no P neighbor)
  - PS4-S: S in PS4 tetrahedra (has P neighbor at ≈ 2.07 Å)

Then reports:
  - Li-Li
  - Li-Cl(4a)  vs  Li-Cl(4d)
  - Li-S(PS4)  vs  Li-S(4d)
  - Cl-Cl  (when present)
  - per-Cl-site bond statistics (each Cl indexed individually with Z, V_poly, mean d)

Usage:
    python3 per_site_bond_analysis.py --cif V0_init.cif --out V0_per_site.json
"""
import argparse, json
import numpy as np
from ase.io import read
from ase.neighborlist import neighbor_list


# argyrodite-standard cutoffs (Å)
CUTOFFS = {
    ("P", "S"):   2.3,
    ("Li", "S"):  3.2,
    ("Li", "Cl"): 3.4,
    ("Li", "Li"): 3.6,
    ("S", "S"):   4.0,
    ("Cl", "Cl"): 4.6,
    ("P", "Cl"):  4.5,
}


def pair_cut(a, b):
    """Symmetric lookup — try both orderings."""
    return CUTOFFS.get((a, b), CUTOFFS.get((b, a), 0.0))


def neighbors_within(i_idx, j_idx, d, sym, idx, target=None, cut=None):
    sel = (i_idx == idx)
    out = []
    for j, dij in zip(j_idx[sel], d[sel]):
        if target is not None and sym[j] != target:
            continue
        if cut is not None and dij > cut:
            continue
        out.append((j, dij))
    return out


def classify_anion_sites(atoms, sym, i_idx, j_idx, d):
    """Tag each Cl as '4a' (Z=6) or '4d' (Z=4), and each S as 'PS4' or '4d'."""
    tags = {}
    for i, s in enumerate(sym):
        if s == "Cl":
            nbrs_li = neighbors_within(i_idx, j_idx, d, sym, i,
                                        target="Li", cut=pair_cut("Li", "Cl"))
            z_li = len(nbrs_li)
            if z_li >= 5:
                tags[i] = ("Cl", "4a")
            else:
                tags[i] = ("Cl", "4d")
        elif s == "S":
            nbrs_p = neighbors_within(i_idx, j_idx, d, sym, i,
                                       target="P", cut=pair_cut("P", "S"))
            tags[i] = ("S", "PS4" if nbrs_p else "4d")
    return tags


def dedup_bonds(triples):
    """neighbor_list returns each bond twice (i→j and j→i). Halve the list."""
    seen = set()
    out = []
    for i, j, dij in triples:
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        out.append((i, j, dij))
    return out


def summarize(distances):
    if not distances:
        return {"n": 0, "mean": None, "std": None, "min": None, "max": None}
    arr = np.array(distances)
    return {
        "n": len(arr),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", required=True)
    ap.add_argument("--out", default="V0_per_site.json")
    args = ap.parse_args()

    atoms = read(args.cif)
    sym = atoms.get_chemical_symbols()
    print(f"natoms={len(atoms)}, V={atoms.get_volume():.4f} Å³, "
          f"formula={atoms.get_chemical_formula()}")

    i_idx, j_idx, d = neighbor_list("ijd", atoms, 4.6)

    # 1. Classify anion sites
    tags = classify_anion_sites(atoms, sym, i_idx, j_idx, d)
    cl_4a = [i for i, t in tags.items() if t == ("Cl", "4a")]
    cl_4d = [i for i, t in tags.items() if t == ("Cl", "4d")]
    s_ps4 = [i for i, t in tags.items() if t == ("S", "PS4")]
    s_4d  = [i for i, t in tags.items() if t == ("S", "4d")]
    print(f"\n=== Anion site assignment ===")
    print(f"  Cl 4a (Z≥5): {len(cl_4a)}   Cl 4d (Z<5): {len(cl_4d)}")
    print(f"  S in PS4   : {len(s_ps4)}   S free 4d  : {len(s_4d)}")

    # 2. Bond lists per pair type, with per-site split
    bonds = {
        "Li-Li":      [],
        "Li-Cl(4a)":  [],
        "Li-Cl(4d)":  [],
        "Li-S(PS4)":  [],
        "Li-S(4d)":   [],
        "P-S":        [],
        "S-S":        [],
        "Cl-Cl":      [],
        "Cl(4a)-Cl(4a)": [],
        "Cl(4a)-Cl(4d)": [],
        "Cl(4d)-Cl(4d)": [],
    }
    for i, j, dij in zip(i_idx, j_idx, d):
        a, b = sym[i], sym[j]
        cut = pair_cut(a, b)
        if cut == 0 or dij > cut:
            continue
        pair = tuple(sorted([a, b]))
        if pair == ("Li", "Li"):
            bonds["Li-Li"].append((i, j, dij))
        elif pair == ("Cl", "Li"):
            cl_idx = i if a == "Cl" else j
            sub = tags[cl_idx][1]
            bonds[f"Li-Cl({sub})"].append((i, j, dij))
        elif pair == ("Li", "S"):
            s_idx = i if a == "S" else j
            sub = tags[s_idx][1]
            bonds[f"Li-S({sub})"].append((i, j, dij))
        elif pair == ("P", "S"):
            bonds["P-S"].append((i, j, dij))
        elif pair == ("S", "S"):
            bonds["S-S"].append((i, j, dij))
        elif pair == ("Cl", "Cl"):
            bonds["Cl-Cl"].append((i, j, dij))
            ta, tb = tags[i][1], tags[j][1]
            ss = tuple(sorted([ta, tb]))
            key = f"Cl({ss[0]})-Cl({ss[1]})"
            if key in bonds:
                bonds[key].append((i, j, dij))

    # Dedup (neighbor_list double-counts)
    for k in bonds:
        bonds[k] = dedup_bonds(bonds[k])

    # 3. Summary stats per bond category
    print(f"\n=== Per-category bond statistics ===")
    stats = {}
    for k, triples in bonds.items():
        dlist = [t[2] for t in triples]
        s = summarize(dlist)
        stats[k] = s
        if s["n"] > 0:
            print(f"  {k:<18} n={s['n']:3d}  mean={s['mean']:.4f} ± "
                  f"{s['std']:.4f}  [{s['min']:.3f}, {s['max']:.3f}] Å")
        else:
            print(f"  {k:<18} n=0")

    # 4. Per-Cl-site details (each Cl atom individually)
    print(f"\n=== Per-Cl-atom detail ===")
    cl_detail = []
    for i in [k for k in range(len(atoms)) if sym[k] == "Cl"]:
        nbrs_li = neighbors_within(i_idx, j_idx, d, sym, i,
                                    target="Li", cut=pair_cut("Li", "Cl"))
        d_li = [n[1] for n in nbrs_li]
        z_li = len(d_li)
        d_mean = float(np.mean(d_li)) if d_li else None
        d_std = float(np.std(d_li)) if d_li else None
        rec = {
            "atom_idx": int(i),
            "site": tags[i][1],
            "Z_Li": z_li,
            "Li_Cl_mean_A": d_mean,
            "Li_Cl_std_A": d_std,
            "Li_Cl_min_A": float(min(d_li)) if d_li else None,
            "Li_Cl_max_A": float(max(d_li)) if d_li else None,
        }
        cl_detail.append(rec)
        print(f"  Cl[{i:3d}] site={tags[i][1]:>2}  Z(Li)={z_li}  "
              f"mean Li-Cl = {d_mean:.4f} Å"
              f" ± {d_std:.4f}" if d_std else "")

    # 5. Per-Li-atom: Li environment (counts and distances)
    print(f"\n=== Per-Li-atom environment (first 8) ===")
    li_detail = []
    for li_idx in [k for k in range(len(atoms)) if sym[k] == "Li"]:
        nS_ps4 = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="S",
                                                       cut=pair_cut("Li", "S"))
                      if tags[n][1] == "PS4")
        nS_4d  = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="S",
                                                       cut=pair_cut("Li", "S"))
                      if tags[n][1] == "4d")
        nCl_4a = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="Cl",
                                                       cut=pair_cut("Li", "Cl"))
                      if tags[n][1] == "4a")
        nCl_4d = sum(1 for n, dn in neighbors_within(i_idx, j_idx, d, sym,
                                                       li_idx, target="Cl",
                                                       cut=pair_cut("Li", "Cl"))
                      if tags[n][1] == "4d")
        env = f"S(PS4)_{nS_ps4}_S(4d)_{nS_4d}_Cl(4a)_{nCl_4a}_Cl(4d)_{nCl_4d}"
        li_detail.append({
            "atom_idx": int(li_idx), "env": env,
            "nS_PS4": nS_ps4, "nS_4d": nS_4d,
            "nCl_4a": nCl_4a, "nCl_4d": nCl_4d,
        })
    # Aggregate Li env types
    from collections import Counter
    env_counts = Counter(rec["env"] for rec in li_detail)
    print(f"  Li environment types ({len(env_counts)} unique):")
    for env, n in env_counts.most_common():
        print(f"    {env}: {n} Li sites")

    # 6. Dump JSON
    out = {
        "formula": atoms.get_chemical_formula(),
        "natoms": len(atoms),
        "volume_A3": float(atoms.get_volume()),
        "anion_sites": {
            "Cl_4a": len(cl_4a),
            "Cl_4d": len(cl_4d),
            "S_PS4": len(s_ps4),
            "S_4d":  len(s_4d),
            "Cl_4d_fraction": (
                len(cl_4d) / (len(cl_4a) + len(cl_4d))
                if (len(cl_4a) + len(cl_4d)) else 0.0),
        },
        "bond_stats": stats,
        "per_Cl_detail": cl_detail,
        "Li_environment_types": dict(env_counts),
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
