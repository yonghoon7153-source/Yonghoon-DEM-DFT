#!/usr/bin/env python3
"""B2O3 doping of LPSCl1.6 (modelC) — Stage 0: Ewald joint pre-rank.

UPGRADED protocol (kb/methodology/b2o3_doping_chemistry.md §5.7).

B2O3 -> bare B3+ at P (4b tetrahedral, -2 acceptor) + O2- at S (16e, isovalent).
Charge compensation: fill existing Li vacancies (LPSCl1.6 has ~0.6 vac/fu).

KEY POINT — what Ewald can / cannot rank:
  charged DOF (Ewald-RIGOROUS)   : B@P (+3 vs +5), halogen S2-/Cl- on free 4a/4d,
                                   Li-fill (+1 vs vacancy 0), acceptor-vacancy assoc.
  isovalent DOF (Ewald-BLIND)    : O@S (both -2) -> O placement decided by COVALENCY,
                                   handled here as chemistry MOTIFS (BO4 / distributed /
                                   free-S) emitted per top config for UMA/DFT to rank.

This avoids the two failure modes of the old sequential-greedy method:
  (1) Li-ordering noise (1162 meV) contaminating a "1 representative Li" ranking,
  (2) greedy cut discarding coupled minima (B-O / acceptor-vacancy coupling).

Pipeline:
  1. supercell -> oxidation states -> site pools
  2. Li-vacancy candidate sites (spglib symmetry-completion; void-finder fallback)
  3. precompute geometric Ewald kernel M once (positions fixed across configs)
  4. random-sample {B sites, halogen pattern, Li-fill sites}; score E = q^T M q
  5. exact config-key dedup -> keep top-N by Ewald
  6. per top-K: emit O motifs (bo4 / distributed / free_s) -> UMA-ready CIFs + ranked.csv

Deps: ase, numpy, scipy (always).  spglib optional (better Li candidates).
Usage:
  python3 b2o3_enumerate.py --base db/structures/modelc_V0_k663.xyz \
      --supercell 1 1 2 --n_B 2 --n_O 3 --n_samples 80000 --top 300 \
      --o_motif_top 20 --out b2o3_stage0
"""
import argparse, json, itertools, hashlib
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list

KE = 14.399645351950543  # e^2/(4*pi*eps0) in eV*Angstrom
OXI = {"Li": +1, "P": +5, "B": +3, "S": -2, "O": -2, "Cl": -1, "VAC": 0}


# ----------------------------------------------------------------------
# Ewald (neutral cell) — geometric kernel M s.t. E = q^T M q  (eV)
# ----------------------------------------------------------------------
def ewald_matrix(pos, cell, alpha=None, rcut=None, kcut=None):
    """Return N×N matrix M with E_ewald = sum_ij q_i q_j M_ij (neutral cell)."""
    pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    N = len(pos); V = abs(np.linalg.det(cell))
    if alpha is None:
        alpha = (N * np.pi**3 / V**2) ** (1.0 / 6.0)  # standard heuristic
    if rcut is None:
        rcut = 3.2 / alpha
    if kcut is None:
        kcut = 2.0 * alpha * 3.2
    recip = 2 * np.pi * np.linalg.inv(cell).T

    # --- real space ---
    nmax = np.ceil(rcut / np.array([np.linalg.norm(cell[i]) for i in range(3)])).astype(int)
    shifts = np.array(list(itertools.product(
        range(-nmax[0], nmax[0] + 1), range(-nmax[1], nmax[1] + 1),
        range(-nmax[2], nmax[2] + 1))))
    Lvecs = shifts @ cell
    M = np.zeros((N, N))
    from scipy.special import erfc
    dij = pos[:, None, :] - pos[None, :, :]              # N,N,3
    for L in Lvecs:
        r = np.linalg.norm(dij + L, axis=2)              # N,N
        zero = r < 1e-8
        r[zero] = 1.0
        contrib = erfc(alpha * r) / r
        contrib[zero] = 0.0
        M += 0.5 * contrib                                # 0.5: each pair counted twice over i,j
    # --- reciprocal ---
    kmax = np.ceil(kcut / np.array([np.linalg.norm(recip[i]) for i in range(3)])).astype(int)
    ks = np.array(list(itertools.product(
        range(-kmax[0], kmax[0] + 1), range(-kmax[1], kmax[1] + 1),
        range(-kmax[2], kmax[2] + 1))))
    ks = ks[np.any(ks != 0, axis=1)]
    G = ks @ recip
    G2 = np.einsum("ij,ij->i", G, G)
    keep = G2 < kcut**2
    G, G2 = G[keep], G2[keep]
    pref = (2 * np.pi / V) * np.exp(-G2 / (4 * alpha**2)) / G2
    phase = np.cos(dij @ G.T)                             # N,N,K
    M += 0.5 * np.einsum("k,ijk->ij", pref, phase)
    # --- self term (diagonal) ---
    M[np.diag_indices(N)] -= alpha / np.sqrt(np.pi)
    return KE * M


def ewald_energy(M, q):
    return float(q @ M @ q)


# ----------------------------------------------------------------------
# site pools
# ----------------------------------------------------------------------
def site_pools(atoms):
    s = atoms.get_chemical_symbols()
    ii, jj = neighbor_list("ij", atoms, {("P", "S"): 2.4})
    ps4 = set()
    for a, b in zip(ii, jj):
        if s[a] == "S": ps4.add(a)
        if s[b] == "S": ps4.add(b)
    P = [i for i in range(len(atoms)) if s[i] == "P"]
    Cl = [i for i in range(len(atoms)) if s[i] == "Cl"]
    freeS = [i for i in range(len(atoms)) if s[i] == "S" and i not in ps4]
    ps4S = sorted(ps4)
    return dict(P=P, Cl=Cl, freeS=freeS, ps4S=ps4S,
                free_anion=sorted(freeS + Cl))  # 4a/4d pool


# ----------------------------------------------------------------------
# Li-vacancy candidate sites
# ----------------------------------------------------------------------
def li_vacancy_candidates(atoms, n_need, min_anion=2.3, max_anion=2.95,
                          min_cation=1.7, grid=0.4):
    """spglib symmetry-completion of the Li sublattice; void-finder fallback."""
    s = atoms.get_chemical_symbols()
    occ_Li = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] == "Li"]]
    cell = atoms.cell.array
    # --- try spglib symmetry completion ---
    try:
        import spglib
        num = atoms.get_atomic_numbers()
        spg = (cell, atoms.get_scaled_positions(), num)
        sym = spglib.get_symmetry(spg, symprec=0.3)
        if sym is not None:
            frac = atoms.get_scaled_positions()
            li_frac = frac[[i for i in range(len(atoms)) if s[i] == "Li"]]
            gen = []
            for R, t in zip(sym["rotations"], sym["translations"]):
                gen.append((li_frac @ R.T + t) % 1.0)
            gen = np.vstack(gen)
            # dedup
            uniq = []
            for f in gen:
                if not any(np.linalg.norm(((f - u + 0.5) % 1.0 - 0.5)) < 0.05 for u in uniq):
                    uniq.append(f)
            uniq = np.array(uniq)
            cart = uniq @ cell
            # vacancy = not near an occupied Li
            cand = [c for c in cart if min_dist(c, occ_Li, cell) > 0.6]
            cand = dedup_cart(cand, cell, 0.6)
            if len(cand) >= n_need:
                return np.array(cand), "spglib_symmetry"
    except Exception:
        pass
    # --- void-finder fallback (grid pockets with REAL Li coordination) ---
    # require Li-like environment: nearest anion in bond range AND >=3 anions
    # coordinating (within 3.25 A) -> rejects surface/over-large pockets that the
    # loose criterion over-generates.
    anion = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] in ("S", "Cl", "O")]]
    cation = atoms.get_positions()[[i for i in range(len(atoms)) if s[i] in ("Li", "P", "B")]]
    na = (np.linalg.norm(cell, axis=1) / grid).astype(int)
    gx = np.linspace(0, 1, na[0], endpoint=False)
    gy = np.linspace(0, 1, na[1], endpoint=False)
    gz = np.linspace(0, 1, na[2], endpoint=False)
    gf = np.array(np.meshgrid(gx, gy, gz)).reshape(3, -1).T
    gc = gf @ cell
    inv = np.linalg.inv(cell)
    keep, score = [], []
    for p in gc:
        da_all = anion_dists(p, anion, inv, cell)
        da = da_all.min()
        ncoord = int((da_all < 3.25).sum())
        if min_anion < da < max_anion and ncoord >= 3 and min_dist(p, cation, cell) > min_cation:
            keep.append(p); score.append(ncoord)
    # dedup keeping higher-coordination representative
    order = np.argsort(score)[::-1]
    cand = dedup_cart([keep[i] for i in order], cell, 1.2)
    cand = [c for c in cand if min_dist(c, occ_Li, cell) > 0.9]
    return np.array(cand), "void_finder"


def anion_dists(p, pts, inv, cell):
    d = p[None, :] - pts
    f = (d @ inv + 0.5) % 1.0 - 0.5
    return np.linalg.norm(f @ cell, axis=1)


def min_dist(p, pts, cell):
    if len(pts) == 0:
        return 1e9
    d = p[None, :] - pts
    inv = np.linalg.inv(cell)
    f = (d @ inv + 0.5) % 1.0 - 0.5
    return float(np.linalg.norm(f @ cell, axis=1).min())


def dedup_cart(pts, cell, tol):
    out = []
    for p in pts:
        if not any(min_dist(p, np.array([u]), cell) < tol for u in out):
            out.append(p)
    return out


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--supercell", nargs=3, type=int, default=[1, 1, 2])
    ap.add_argument("--n_B", type=int, default=2)
    ap.add_argument("--n_O", type=int, default=3)
    ap.add_argument("--n_samples", type=int, default=80000)
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--o_motif_top", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="b2o3_stage0")
    A = ap.parse_args()
    rng = np.random.default_rng(A.seed)
    out = Path(A.out); (out / "cif").mkdir(parents=True, exist_ok=True)

    base = read(A.base) * tuple(A.supercell)
    pools = site_pools(base)
    n_Li_fill = 2 * A.n_B                     # P5+ -> B3+ = -2 each
    n_freeS = len(pools["freeS"])             # keep same free-S count (halogen reshuffle)
    print(f"supercell {A.supercell}  nat {len(base)}  pools: P {len(pools['P'])} "
          f"free_anion {len(pools['free_anion'])} (freeS {n_freeS}) ps4S {len(pools['ps4S'])}")
    print(f"doping: {A.n_B} B@P, {A.n_O} O@S, +{n_Li_fill} Li (charge comp)")

    licand, src = li_vacancy_candidates(base, n_Li_fill)
    print(f"Li-vacancy candidates: {len(licand)} ({src})")
    if len(licand) < n_Li_fill:
        raise SystemExit(f"need >= {n_Li_fill} Li candidates, got {len(licand)} — "
                         f"pass an ideal Li template or loosen void params")

    # --- master position list: framework + Li-occupied + Li-candidate ---
    s0 = base.get_chemical_symbols()
    fw_idx = [i for i in range(len(base)) if s0[i] != "Li"]   # P/S/Cl positions (fixed)
    li_occ_idx = [i for i in range(len(base)) if s0[i] == "Li"]
    pos = np.vstack([base.get_positions()[fw_idx],
                     base.get_positions()[li_occ_idx],
                     licand])
    cell = base.cell.array
    # index maps into master list
    fw_of = {old: k for k, old in enumerate(fw_idx)}
    nfw = len(fw_idx); nliocc = len(li_occ_idx)
    licand_master = list(range(nfw + nliocc, nfw + nliocc + len(licand)))
    liocc_master = list(range(nfw, nfw + nliocc))

    print("precomputing Ewald kernel ...", flush=True)
    M = ewald_matrix(pos, cell)

    # base charge vector (no doping): framework species + occupied Li(+1) + candidates(0)
    q0 = np.zeros(len(pos))
    for old in fw_idx:
        q0[fw_of[old]] = OXI[s0[old]]
    for m in liocc_master:
        q0[m] = OXI["Li"]
    # candidates start as vacancy (0)
    P_master = [fw_of[i] for i in pools["P"]]
    freeanion_master = [fw_of[i] for i in pools["free_anion"]]
    # halogen counts to preserve: n_freeS S(-2), rest Cl(-1)
    n_free = len(freeanion_master)

    # Deterministic: enumerate B (C(nP,n_B)) × halogen (C(n_free, n_freeS));
    # for each, place n_Li_fill Li GREEDILY at the lowest-marginal-energy candidate
    # sites (acceptor-vacancy association + Li-Li repulsion captured exactly).
    Mdiag = np.diag(M)
    cand_arr = np.array(licand_master)
    B_combos = list(itertools.combinations(range(len(P_master)), A.n_B))
    H_combos = list(itertools.combinations(range(n_free), n_freeS))
    n_total = len(B_combos) * len(H_combos)
    print(f"enumerating {len(B_combos)} B × {len(H_combos)} halogen = {n_total} base "
          f"configs, greedy-Li each ...", flush=True)
    if A.n_samples and n_total > A.n_samples:
        # subsample halogen patterns if the product is too large (keeps all B)
        keep = max(1, A.n_samples // len(B_combos))
        idx = rng.choice(len(H_combos), min(keep, len(H_combos)), replace=False)
        H_combos = [H_combos[i] for i in idx]
        print(f"  halogen subsampled to {len(H_combos)} (n_samples cap {A.n_samples})")

    seen = {}
    done = 0
    for bsel in B_combos:
        for Hsel in H_combos:
            q = q0.copy()
            for b in bsel:
                q[P_master[b]] = OXI["B"]
            Hset = set(Hsel)
            for k, m in enumerate(freeanion_master):
                q[m] = OXI["S"] if k in Hset else OXI["Cl"]
            # greedy Li fill
            placed = []
            for _ in range(n_Li_fill):
                marg = Mdiag[cand_arr] + 2.0 * (M[cand_arr] @ q)   # ΔE to add +1 at cand
                for p in placed:
                    marg[p] = np.inf
                c = int(np.argmin(marg))
                q[cand_arr[c]] = OXI["Li"]
                placed.append(c)
            key = (tuple(sorted(int(P_master[b]) for b in bsel)),
                   tuple(sorted(int(freeanion_master[k]) for k in Hsel)),
                   tuple(sorted(int(cand_arr[p]) for p in placed)))
            if key not in seen:
                seen[key] = ewald_energy(M, q)
            done += 1
            if done % 20000 == 0:
                print(f"  {done}/{n_total} ...", flush=True)

    ranked = sorted(seen.items(), key=lambda kv: kv[1])
    print(f"unique configs {len(ranked)}; lowest Ewald {ranked[0][1]:.3f} eV, "
          f"highest {ranked[-1][1]:.3f} eV, span {ranked[-1][1]-ranked[0][1]:.3f} eV")

    # --- write top-N (B/halogen/Li only; S not yet O) + O motifs for top-K ---
    rows = []
    for rank, (key, E) in enumerate(ranked[:A.top]):
        bpos, sfree, lifill = key
        st = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                          bpos, sfree, lifill, pools, o_sites=None)
        name = f"cfg{rank:04d}_E{E:.3f}"
        write(out / "cif" / f"{name}.cif", st)
        rows.append(dict(rank=rank, ewald_eV=round(E, 4), name=name,
                         B_sites=list(bpos), n_Li_fill=len(lifill)))
        # O motifs for the very top configs (UMA-ready full B2O3 structures)
        if rank < A.o_motif_top:
            for motif in ("bo4", "distributed", "free_s"):
                o_sites = pick_o_sites(base, bpos, pools, A.n_O, motif, rng, fw_idx)
                if o_sites is None:
                    continue
                st_o = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                                    bpos, sfree, lifill, pools, o_sites=o_sites)
                write(out / "cif" / f"{name}_O-{motif}.cif", st_o)

    json.dump(rows, open(out / "stage0_ranked.json", "w"), indent=2)
    with open(out / "stage0_ranked.csv", "w") as f:
        f.write("rank,ewald_eV,name,n_B,n_Li_fill\n")
        for r in rows:
            f.write(f"{r['rank']},{r['ewald_eV']},{r['name']},{len(r['B_sites'])},{r['n_Li_fill']}\n")
    print(f"\nwrote top {len(rows)} -> {out}/cif/  (+ O motifs for top {A.o_motif_top})")
    print(f"ranked: {out}/stage0_ranked.csv|json")
    print("NEXT: Stage 1 = UMA relax these (esp. the *_O-{bo4,distributed,free_s}.cif "
          "variants decide O placement by covalency).")


def pick_o_sites(base, bpos, pools, n_O, motif, rng, fw_idx):
    """Choose n_O sulfur sites (in original-index space) for O substitution."""
    s = base.get_chemical_symbols()
    # B-tetrahedron corner S: PS4-S bonded to a B-substituted P
    bP_orig = [fw_idx[b] if False else None for b in bpos]  # placeholder
    # map master P index back to original atom index
    P_orig = pools["P"]
    fwinv = {fw_idx.index(i): i for i in fw_idx}  # not used; keep simple
    # bpos are master indices into framework; recover original P atom indices
    b_orig = [fw_idx[mb] for mb in bpos]
    from ase.neighborlist import neighbor_list
    ii, jj = neighbor_list("ij", base, {("P", "S"): 2.4})
    corner_of = {p: [] for p in b_orig}
    for a, b in zip(ii, jj):
        if a in corner_of and s[b] == "S": corner_of[a].append(b)
        if b in corner_of and s[a] == "S": corner_of[b].append(a)
    b_corners = sorted({c for v in corner_of.values() for c in v})
    if motif == "bo4":
        pool = b_corners
    elif motif == "free_s":
        pool = pools["freeS"]
    else:  # distributed: PS4-S not on B
        pool = [i for i in pools["ps4S"] if i not in set(b_corners)]
    if len(pool) < n_O:
        pool = pools["ps4S"]
    if len(pool) < n_O:
        return None
    return sorted(rng.choice(pool, n_O, replace=False).tolist())


def build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                 bpos, sfree, lifill, pools, o_sites):
    """Assemble ASE Atoms for a given config (bpos/sfree/lifill are master indices)."""
    from ase import Atoms
    s = list(base.get_chemical_symbols())
    new = base.copy()
    syms = list(new.get_chemical_symbols())
    # B@P
    for mb in bpos:
        syms[fw_idx[mb]] = "B"
    # halogen: set free-anion sites
    nfw = len(fw_idx)
    # sfree are master indices in framework space -> original
    sset = set(fw_idx[m] for m in sfree)
    for orig in pools["free_anion"]:
        syms[orig] = "S" if orig in sset else "Cl"
    # O@S
    if o_sites:
        for o in o_sites:
            syms[o] = "O"
    new.set_chemical_symbols(syms)
    # add filled Li
    li_master0 = nfw + len(li_occ_idx)
    from ase import Atom
    for ml in lifill:
        p = pos[ml]
        new.append(Atom("Li", position=p))
    return new


if __name__ == "__main__":
    main()
