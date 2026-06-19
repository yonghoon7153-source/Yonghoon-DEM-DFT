#!/usr/bin/env python3
"""Argyrodite Li-cage jump GEOMETRIC descriptors (NEB-free), Taklu/Nano Energy 2021 style.

Instead of explicit NEB barriers, characterise Li+ transport by the geometry that
controls the doublet / intra-cage / inter-cage jumps:
  - free anion (cage centre) inventory + S/Cl site disorder
  - intra-cage 48h-48h Li-Li distance (shorter -> easier intra-cage / doublet hop)
  - inter-cage 48h-48h Li-Li distance (the long-range, rate-limiting window)
  - Li per cage (carrier distribution)

These are PROXIES (correlative), to be presented with the quantitative AIMD Ea
(comp1 0.253 eV, modelc 0.223 eV), not as barriers.

numpy-only (no ase/pymatgen). Reads extended-xyz (Lattice="..." in comment line),
full MIC for triclinic cells.

Usage:
  python3 cage_jump_descriptors.py LABEL=path.xyz [LABEL2=path2.xyz ...] [--out out.csv]
"""
import numpy as np, sys, re, json

PS_BOND = 2.30     # P-S bond cutoff (PS4 ~2.04-2.11 -> free S clearly > 2.3)
CAGE_R  = 3.30     # Li within this of a cage centre = that cage's Li
INTRA_MAX = 3.80   # Li-Li shorter than this within a cage = doublet/intra candidate


def read_extxyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0].split()[0])
    m = re.search(r'Lattice="([^"]+)"', lines[1])
    L = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
    sym, pos = [], []
    for ln in lines[2:2 + n]:
        p = ln.split()
        sym.append(p[0]); pos.append([float(p[1]), float(p[2]), float(p[3])])
    return np.array(sym), np.array(pos, float), L


def mic(pi, pj, L, Linv):
    """min-image distance matrix between cart sets pi(M,3), pj(N,3)."""
    d = (pi @ Linv)[:, None, :] - (pj @ Linv)[None, :, :]
    d -= np.round(d)
    return np.linalg.norm(d @ L, axis=2)


def analyze(label, path):
    sym, pos, L = read_extxyz(path)
    Linv = np.linalg.inv(L)
    idx = {e: np.where(sym == e)[0] for e in set(sym)}
    P, S, Cl, Li = (idx.get(e, np.array([], int)) for e in ("P", "S", "Cl", "Li"))

    # --- PS4 sulfurs vs free S ---
    bonded = set()
    if len(P) and len(S):
        dPS = mic(pos[P], pos[S], L, Linv)
        for i in range(len(P)):
            for j in np.where(dPS[i] < PS_BOND)[0]:
                bonded.add(int(S[j]))
    freeS = np.array([s for s in S if s not in bonded], int)

    centers = np.concatenate([freeS, Cl]) if len(Cl) or len(freeS) else np.array([], int)
    ctype = np.array(["S"] * len(freeS) + ["Cl"] * len(Cl))

    # --- assign Li -> nearest cage centre ---
    dLiC = mic(pos[Li], pos[centers], L, Linv)
    assign = np.argmin(dLiC, axis=1)
    li_cage_d = dLiC[np.arange(len(Li)), assign]

    # --- Li-Li distances, split intra/inter cage ---
    dLiLi = mic(pos[Li], pos[Li], L, Linv)
    np.fill_diagonal(dLiLi, np.inf)
    intra, inter = [], []
    for a in range(len(Li)):
        for b in range(a + 1, len(Li)):
            (intra if assign[a] == assign[b] else inter).append(dLiLi[a, b])
    intra, inter = np.array(intra), np.array(inter)

    # per-cage shortest intra Li-Li (doublet), per Li shortest inter (window)
    cage_short_intra = []
    for c in range(len(centers)):
        members = np.where(assign == c)[0]
        if len(members) >= 2:
            sub = dLiLi[np.ix_(members, members)]
            cage_short_intra.append(sub[sub < np.inf].min())
    cage_short_intra = np.array(cage_short_intra)
    # shortest inter-cage Li-Li per Li (window crossing)
    win = []
    for a in range(len(Li)):
        others = np.where(assign != assign[a])[0]
        if len(others):
            win.append(dLiLi[a, others].min())
    win = np.array(win)

    nS = int((ctype == "S").sum()); nCl = int((ctype == "Cl").sum())
    # Li delocalization: how many Li sit in S-centred vs Cl-centred cages
    li_center_type = ctype[assign]
    li_in_S = int((li_center_type == "S").sum())
    li_in_Cl = int((li_center_type == "Cl").sum())
    occ = np.bincount(assign, minlength=len(centers))
    occ_cages = int((occ >= 1).sum())
    res = {
        "label": label,
        "n_atoms": len(sym),
        "formula": "".join(f"{e}{len(idx.get(e,[]))}" for e in ["Li", "P", "S", "Cl"]),
        "n_PS4": len(P),
        "free_anion_centers": int(len(centers)),
        "centers_S": nS, "centers_Cl": nCl,
        "cage_center_Cl_fraction": round(nCl / max(1, len(centers)), 3),
        # Li delocalization (anion-disorder signature)
        "Li_in_S_cages": li_in_S,
        "Li_in_Cl_cages": li_in_Cl,
        "Li_frac_on_Cl_sites": round(li_in_Cl / max(1, len(Li)), 3),
        "occupied_cages": occ_cages,
        "Li_per_occ_cage": [int(x) for x in occ if x >= 1],
        # intra-cage (doublet / 48h-48h within cage)
        "intra_doublet_min_A": round(float(cage_short_intra.min()), 3) if len(cage_short_intra) else None,
        "Li_NN_median_A": round(float(np.median([dLiLi[a][dLiLi[a] < np.inf].min() for a in range(len(Li))])), 3),
        # inter-cage (window / 48h-48h across cages)
        "inter_window_min_A": round(float(win.min()), 3) if len(win) else None,
        "inter_window_mean_A": round(float(win.mean()), 3) if len(win) else None,
    }
    return res


def main():
    args = [a for a in sys.argv[1:] if "=" in a and not a.startswith("--")]
    out = None
    for a in sys.argv[1:]:
        if a.startswith("--out"):
            out = a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1]
    rows = []
    for a in args:
        label, path = a.split("=", 1)
        rows.append(analyze(label, path))

    keys = list(rows[0].keys())
    w = max(len(k) for k in keys)
    print(f"{'descriptor':<{w}} | " + " | ".join(f"{r['label']:>14}" for r in rows))
    print("-" * (w + 3 + 17 * len(rows)))
    for k in keys:
        if k == "label":
            continue
        print(f"{k:<{w}} | " + " | ".join(f"{str(r[k]):>14}" for r in rows))

    if out:
        import csv
        with open(out, "w", newline="") as f:
            wr = csv.writer(f); wr.writerow(keys)
            for r in rows: wr.writerow([r[k] for k in keys])
        print(f"\n-> {out}")


if __name__ == "__main__":
    main()
