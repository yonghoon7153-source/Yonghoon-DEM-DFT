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
  python3 cage_jump_descriptors.py --li_sites traj.xyz [more.xyz ...] [--every N] [--tau 0.10 0.15]
  python3 cage_jump_descriptors.py --selftest

--li_sites (2026-10-14, quick look for the 24g/48h question — EXPLORATORY, not a reported quantity):
  every Li gets the barycentric coordinates of the tetrahedron of its 4 nearest anions (S incl. PS4 S, Cl, Br, I,
  O, F, Se, N). lambda_min ~ 0 -> Li sits on a face (24g-like, the shared face of a 48h doublet);
  lambda_min ~ 0.2-0.3 -> Li sits inside the tetrahedron (48h-like); < 0 -> outside its 4-anion tetrahedron.
  Works on one frame (a relaxed structure) or a multi-frame extended-xyz trajectory (every N-th frame).
  Minimum images are found by searching the 27 neighbouring images after rounding — plain rounding of fractional
  coordinates is NOT a minimum image in skewed cells such as our 60-degree modelc cell (the selftest proves it).

What --li_sites does NOT do:
  * it is not site-analysis (no site list from the ideal structure, no residence times, no hop events). The formal
    24g/48h analysis is decided to use site-analysis >= 1.10 with a pinned version (user 2026-10-14);
  * the tau thresholds are arbitrary — report the lambda_min distribution, not one fraction;
  * at 600 K thermal motion smears lambda (a Li passing a face is counted as 24g-like for those frames);
  * frames between saved snapshots are invisible; it does not use velocities or time ordering.
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


ANIONS = {"S", "Cl", "Br", "I", "O", "F", "Se", "N"}
_SHIFTS = np.array([[i, j, k] for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)], float)


def iter_extxyz(path, every=1):
    """Yield (symbols, positions, lattice) for every `every`-th frame of an extended-xyz file (one frame is fine)."""
    with open(path) as fh:
        k = 0
        while True:
            head = fh.readline()
            if not head:
                return
            if not head.strip():
                continue
            n = int(head.split()[0])
            com = fh.readline()
            m = re.search(r'Lattice="([^"]+)"', com)
            if not m:
                raise SystemExit(f"⛔ {path}: frame {k} has no Lattice= — cannot apply periodic images")
            rows = [fh.readline().split() for _ in range(n)]
            if k % every == 0:
                L = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
                yield (np.array([r[0] for r in rows]), np.array([[float(x) for x in r[1:4]] for r in rows]), L)
            k += 1


def mic_vectors(frac_d, L):
    """Minimum-image Cartesian vectors for fractional differences (..., 3): round, then search the 27 neighbours.
    Plain rounding alone is not a minimum image in a skewed cell (60-degree rhombohedral modelc)."""
    f = frac_d - np.round(frac_d)
    cand = (f[..., None, :] + _SHIFTS) @ L                       # (..., 27, 3)
    k = np.argmin(np.einsum('...ij,...ij->...i', cand, cand), axis=-1)
    return np.take_along_axis(cand, k[..., None, None], axis=-2)[..., 0, :]


def li_face_lambda(sym, pos, L, anions=ANIONS):
    """Per-Li minimum barycentric coordinate in the tetrahedron of its 4 nearest anions (NaN if degenerate)."""
    Li = np.where(sym == "Li")[0]
    An = np.where(np.isin(sym, list(anions)))[0]
    if len(Li) == 0 or len(An) < 4:
        raise ValueError(f"need Li and >= 4 anions (Li {len(Li)} · anions {len(An)})")
    Linv = np.linalg.inv(L)
    v = mic_vectors((pos[An] @ Linv)[None, :, :] - (pos[Li] @ Linv)[:, None, :], L)   # (nLi, nAn, 3) Li -> anion
    d2 = np.einsum('ijk,ijk->ij', v, v)
    nn = np.argsort(d2, axis=1)[:, :4]
    V = np.take_along_axis(v, nn[:, :, None], axis=1)                                 # (nLi, 4, 3)
    A = np.concatenate([np.transpose(V, (0, 2, 1)), np.ones((len(Li), 1, 4))], axis=1)  # (nLi, 4, 4)
    b = np.zeros((len(Li), 4)); b[:, 3] = 1.0
    lam = np.full((len(Li), 4), np.nan)
    ok = np.abs(np.linalg.det(A)) > 1e-6
    if ok.any():
        lam[ok] = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
    out = np.full(len(Li), np.nan)
    out[ok] = lam[ok].min(axis=1)
    return out


def li_sites_report(paths, every=1, taus=(0.10, 0.15)):
    """Pool lambda_min over Li and frames; print the distribution and the face-like fraction at each tau."""
    edges = [-np.inf, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, np.inf]
    names = ["<0", "0-.05", ".05-.10", ".10-.15", ".15-.20", ".20-.25", ">=.25"]
    rows = []
    for path in paths:
        lam, nf, nli = [], 0, None
        for sym, pos, L in iter_extxyz(path, every):
            x = li_face_lambda(sym, pos, L)
            lam.append(x); nf += 1; nli = len(x)
        lam = np.concatenate(lam)
        good = lam[np.isfinite(lam)]
        hist = np.histogram(good, bins=edges)[0] / max(1, len(good))
        rows.append((path, nf, nli, len(lam) - len(good), good, hist))
    for path, nf, nli, nbad, good, hist in rows:
        print(f"== {path}")
        print(f"   frames {nf} · Li {nli} · Li-frames {len(good)}" + (f" · degenerate {nbad}" if nbad else ""))
        print(f"   lambda_min p10 / p50 / p90 = {np.percentile(good, 10):.3f} / {np.percentile(good, 50):.3f} / "
              f"{np.percentile(good, 90):.3f}")
        print("   " + " · ".join(f"{t} {h:.3f}" for t, h in zip(names, hist)))
        print("   face-like (24g-like) fraction: " + " · ".join(f"tau {t:.2f} -> {np.mean(good < t):.3f}" for t in taus)
              + f" · outside (<0) {np.mean(good < 0):.3f}")
    return rows


def _selftest():
    ok = 0
    def chk(cond, what):
        nonlocal ok
        if not cond:
            raise SystemExit(f"selftest FAIL: {what}")
        ok += 1
    rng = np.random.default_rng(7)
    # 1. skewed cell (our 60-degree modelc cell): the 27-image search equals brute force, plain rounding does not
    Lm = np.array([[6.0683, 0.0, 3.5035], [2.0228, 5.7213, 3.5035], [0.0, 0.0, 35.0355]])
    fd = rng.uniform(-1, 1, size=(4000, 3))
    brute = np.min(np.linalg.norm((fd[:, None, :] - np.round(fd)[:, None, :]
                                   + np.array([[i, j, k] for i in range(-2, 3) for j in range(-2, 3)
                                               for k in range(-2, 3)])) @ Lm, axis=2), axis=1)
    ours = np.linalg.norm(mic_vectors(fd, Lm), axis=1)
    plain = np.linalg.norm((fd - np.round(fd)) @ Lm, axis=1)
    chk(np.allclose(ours, brute, atol=1e-9), "27-image minimum image equals brute force (125 images) in the 60-degree cell")
    chk(np.mean(plain > brute + 1e-6) > 0.05, "[negative] plain rounding is NOT a minimum image in this cell (>5 % of pairs too long)")
    # 2. a regular S tetrahedron + mirror apex (a 48h doublet): interior Li -> ~0.3, Li on the shared face -> ~0
    e = 4.0
    base = np.array([[0, 0, 0], [e, 0, 0], [e / 2, e * np.sqrt(3) / 2, 0]], float)
    c = base.mean(axis=0); h = e * np.sqrt(2 / 3)
    apex, mirror = c + [0, 0, h], c - [0, 0, h]
    Lc = np.eye(3) * 20.0
    def frame(li):
        return np.array(["S"] * 5 + ["Li"]), np.vstack([base, apex, mirror, li]) + 5.0
    s1, p1 = frame(c + [0, 0, 1.0])
    l_in = li_face_lambda(s1, p1, Lc)[0]
    chk(0.2 < l_in < 0.35, f"Li 1.0 A above the shared face is inside its tetrahedron (lambda_min {l_in:.3f})")
    s2, p2 = frame(c)
    chk(abs(li_face_lambda(s2, p2, Lc)[0]) < 1e-9, "Li on the shared face has lambda_min 0 (24g-like)")
    chk(li_face_lambda(s1, p1, Lc)[0] > 0.15 > li_face_lambda(s2, p2, Lc)[0], "[negative] the two Li are told apart at tau 0.15")
    # 3. invariance: translate + wrap in the skewed cell, and shuffle the atom order -> same lambda multiset
    sym = np.array(["S"] * 5 + ["Li"] * 2)
    pos = np.vstack([base, apex, mirror, c + [0, 0, 1.0], c]) + [3.0, 3.0, 10.0]
    lam0 = np.sort(li_face_lambda(sym, pos, Lm))
    shift = rng.uniform(0, 30, 3)
    f = (pos + shift) @ np.linalg.inv(Lm); f -= np.floor(f)
    perm = rng.permutation(len(sym))
    lam1 = np.sort(li_face_lambda(sym[perm], (f @ Lm)[perm], Lm))
    chk(np.allclose(lam0, lam1, atol=1e-9), "translate + wrap + shuffle leaves lambda_min unchanged (skewed cell)")
    # 4. no anions -> loud error, not a number
    try:
        li_face_lambda(np.array(["Li", "P", "P", "P", "P"]), np.zeros((5, 3)) + np.arange(5)[:, None], Lc)
        chk(False, "[negative] no anions must raise")
    except ValueError:
        ok += 1
    print(f"selftest PASS ({ok})")


def main():
    if "--selftest" in sys.argv:
        return _selftest()
    if "--li_sites" in sys.argv:
        import argparse
        ap = argparse.ArgumentParser(prog="cage_jump_descriptors.py --li_sites")
        ap.add_argument("--li_sites", nargs="+", required=True, metavar="XYZ")
        ap.add_argument("--every", type=int, default=1, help="use every N-th frame")
        ap.add_argument("--tau", type=float, nargs="+", default=[0.10, 0.15], help="face-like thresholds on lambda_min")
        a = ap.parse_args(sys.argv[1:])
        li_sites_report(a.li_sites, a.every, tuple(a.tau))
        return
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
