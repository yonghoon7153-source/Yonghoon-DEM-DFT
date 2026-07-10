#!/usr/bin/env python3
"""phaseB_v7c_dft_binding.py — SDCP v7c | Phase-B DFT+U cross-check of the
LiNiO2(104) binding energy on the Phase-A (UMA) geometries.

Phase-A (UMA) gave doped_sulfonate_down_r0 = -0.935 vs neutral -0.893 eV
(Delta 0.04) — too close to trust, because UMA has no charge/spin knob and
sees only the radical *geometry*. Phase-B re-scores the SAME geometries with
DFT+U (the arbiter). We emit 5 single-point SCF inputs:

  slab            E_slab  (the shared reference)
  complex_doped   E(slab + doped radical, champion orientation)
  complex_neutral E(slab + neutral molecule, same orientation)
  mol_doped       E_mol(doped)   gas ref, doublet
  mol_neutral     E_mol(neutral) gas ref, singlet

  E_bind(tag) = E(complex_tag) - E_slab - E_mol(tag)     [negative = binding]
  Verdict = sign & size of  E_bind(doped) - E_bind(neutral).

Settings are cloned VERBATIM from reference_dft_v2/scf_u62.in — the converged
LiNiO2(104) recipe — with ONE deliberate change (u62c plan): the FSM line
`tot_magnetization = 0.0` is DROPPED for the slab/complexes so the adsorbed
radical's spin is free to find its own ground state; only the Ni AFM guess
(starting_magnetization +/-0.3) is kept. The Ni1/Ni2 sublattice split is
inherited from scf_u62.in by nearest-position matching (both are the same
96-atom (104) slab; relaxation drift << Ni-Ni spacing, so the map is 1:1).

Single-point (calculation='scf'): the cross-check isolates the electronic/U
effect at fixed UMA geometry — apples-to-apples with Phase-A.

Usage (on KISTI, where scf_u62.in + phaseA xyz live):
  conda activate uma   # only for ASE io; no GPU needed
  python3 phaseB_v7c_dft_binding.py \
      --ref_scf     /data/work/runs/sdcp_linio2_binding/reference_dft_v2/scf_u62.in \
      --slab        /data/work/runs/sdcp_linio2_binding/reference/slab_relaxed.xyz \
      --complex_doped   /data/work/runs/sdcp_linio2_binding/phaseA_v7c/complex_doped_sulfonate_down_r0.xyz \
      --complex_neutral /data/work/runs/sdcp_linio2_binding/phaseA_v7c/complex_neutral_sulfonate_down_r0.xyz \
      --mol_doped   /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_doped.xyz \
      --mol_neutral /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz \
      --pseudo_dir  /data/work/pseudo \
      --out         /data/work/runs/sdcp_linio2_binding/phaseB_v7c
Writes <out>/{slab,complex_doped,complex_neutral,mol_doped,mol_neutral}/scf.in
plus <out>/README_harvest.txt (E_bind formula + a grep-the-energies snippet).
"""
import argparse
import json
import os
import re
import numpy as np
from ase.io import read
from scipy.optimize import linear_sum_assignment

# ---- cloned from scf_u62.in (reference_dft_v2) ------------------------------
ECUTWFC = 60.0
ECUTRHO = 480.0
DEGAUSS = 0.03            # smearing = 'mv'
CONV_THR = 1.0e-6
MIX_BETA = 0.03          # local-TF, ndim 20 — the slow/safe recipe that converged
MIX_NDIM = 20
U_NI = 6.2               # HUBBARD ortho-atomic, Ni1-3d / Ni2-3d
AFM_MAG = 0.3            # starting_magnetization Ni1 +0.3 / Ni2 -0.3
KPTS_SLAB = "2 2 1 0 0 0"
MOL_VACUUM = 12.0        # A vacuum around gas-phase molecule box

# PBE USPP/PAW pseudos (all confirmed present in /data/work/pseudo)
PSEUDOS = {
    'Li':  ('6.940',   'li_pbe_v1.4.uspp.F.UPF'),
    'Ni1': ('58.690',  'ni_pbe_v1.4.uspp.F.UPF'),
    'Ni2': ('58.690',  'ni_pbe_v1.4.uspp.F.UPF'),
    'O':   ('15.999',  'O.pbe-n-kjpaw_psl.0.1.UPF'),
    'C':   ('12.011',  'C.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'H':   ('1.008',   'H.pbe-rrkjus_psl.1.0.0.UPF'),
    'S':   ('32.065',  's_pbe_v1.4.uspp.F.UPF'),
}
SPECIES_ORDER = ['Li', 'Ni1', 'Ni2', 'O', 'C', 'H', 'S']


def parse_ref_ni(ref_scf):
    """Extract Ni1/Ni2 cartesian positions + labels from a QE input (AFM partition)."""
    with open(ref_scf) as f:
        lines = f.readlines()
    # cell
    cell = None
    for i, ln in enumerate(lines):
        if ln.strip().upper().startswith('CELL_PARAMETERS'):
            cell = np.array([[float(x) for x in lines[i + k].split()[:3]]
                             for k in (1, 2, 3)])
            break
    # atomic positions
    for i, ln in enumerate(lines):
        u = ln.strip().upper()
        if u.startswith('ATOMIC_POSITIONS'):
            crystal = 'CRYSTAL' in u
            j = i + 1
            pos, lab = [], []
            while j < len(lines):
                s = lines[j].split()
                if len(s) < 4 or not re.match(r'^[A-Za-z]', s[0]):
                    break
                sp = s[0]
                p = np.array([float(s[1]), float(s[2]), float(s[3])])
                if crystal:
                    if cell is None:
                        raise SystemExit("CRYSTAL positions but no CELL_PARAMETERS")
                    p = p @ cell
                if sp in ('Ni1', 'Ni2'):
                    pos.append(p)
                    lab.append(sp)
                j += 1
            if 'Ni1' not in lab or 'Ni2' not in lab:
                raise SystemExit("ref_scf has no Ni1/Ni2 labels — cannot inherit AFM split")
            return np.array(pos), lab, cell
    raise SystemExit("no ATOMIC_POSITIONS in ref_scf")


def _mic_min(P_ref, q, inv, cell):
    d = P_ref - q
    f = d @ inv; f -= np.round(f); d = f @ cell
    return np.sqrt((d ** 2).sum(axis=1)).min()


def best_translation(P_tgt, P_ref, cell, cutoff=0.6):
    """RANSAC rigid translation T (min-image) maximizing inliers of P_tgt+T vs
    P_ref. Two relaxations of the same (104) cell differ only by a cell-origin
    offset (no rotation: cell vectors identical), so a single T aligns them."""
    inv = np.linalg.inv(cell)
    best_T, best_in = np.zeros(3), -1
    for i in range(len(P_ref)):            # every ref anchor ...
        for j in range(len(P_tgt)):        # ... hypothesised == every target
            T = P_ref[i] - P_tgt[j]
            Q = P_tgt + T
            inl = sum(1 for q in Q if _mic_min(P_ref, q, inv, cell) < cutoff)
            if inl > best_in:
                best_in, best_T = inl, T
    return best_T, best_in


def split_ni(atoms, ni_ref, ref_lab, cell, align=True):
    """Per-atom labels; Ni -> Ni1/Ni2 by BIJECTIVE (Hungarian) match to ref (MIC),
    after a RANSAC translation alignment so a cell-origin offset between the two
    slabs does not scramble the (in-plane) AFM labels.

    Greedy nearest-match is not one-to-one and would orphan a Ni to a far ref;
    linear_sum_assignment guarantees a 1:1 map. Alignment removes the ~2.9 A
    offset first so the residual reflects true relaxation drift.
    """
    labels = list(atoms.get_chemical_symbols())
    ni_idx = [i for i, s in enumerate(labels) if s == 'Ni']
    inv = np.linalg.inv(cell)
    P = atoms.positions[ni_idx]
    if len(ni_idx) != len(ni_ref):
        print(f"  !! Ni count target {len(ni_idx)} != ref {len(ni_ref)} — greedy fallback")
        for a, idx in enumerate(ni_idx):
            labels[idx] = ref_lab[int(np.argmin([
                _mic_min(ni_ref[c:c + 1], P[a], inv, cell) for c in range(len(ni_ref))]))]
        return labels
    if align:
        T, inl = best_translation(P, ni_ref, cell)
        n = len(ni_ref)
        print(f"  RANSAC align: {inl}/{n} inliers @0.6A, T=[{T[0]:.2f} {T[1]:.2f} {T[2]:.2f}]")
        if inl >= 0.8 * n:
            P = P + T
        else:
            print(f"  !! weak alignment ({inl}/{n}) — a pure translation does not map the "
                  "slabs (rotation/reconstruction?); AFM labels UNRELIABLE, do not launch")
    # bijective Hungarian on (aligned) coordinates
    D = np.empty((len(ni_idx), len(ni_ref)))
    for a in range(len(ni_idx)):
        d = ni_ref - P[a]
        f = d @ inv; f -= np.round(f); d = f @ cell
        D[a] = np.sqrt((d ** 2).sum(axis=1))
    row, col = linear_sum_assignment(D)
    dists = D[row, col]
    for a, c in zip(row, col):
        labels[ni_idx[a]] = ref_lab[c]
    n1 = sum(1 for i in ni_idx if labels[i] == 'Ni1')
    print(f"  Ni assign (Hungarian post-align): max {dists.max():.2f} A, mean {dists.mean():.2f} A, "
          f">1A {(dists > 1.0).sum()}/{len(dists)}  -> Ni1 {n1}/Ni2 {len(ni_idx) - n1}")
    if dists.max() > 1.0:
        print("  !! residual >1.0 A after alignment — labels suspect, check the two slabs")
    return labels


def cluster_z(z, tol=0.8):
    """1D gap clustering along z -> band index per point (band 0 = lowest z)."""
    order = np.argsort(z)
    band = np.zeros(len(z), dtype=int)
    b = 0
    for k in range(1, len(order)):
        if z[order[k]] - z[order[k - 1]] > tol:
            b += 1
        band[order[k]] = b
    return band


def analyze_ref_layers(ni_ref, ref_lab, tol=0.8):
    """Report the ref AFM pattern along z. Returns (rows, band_lab, is_A_type).

    A-type (layer AFM): each z-band is a single spin and adjacent bands alternate
    -> reproducible from the target slab's OWN z-layering, immune to in-plane
    offset. Anything else (mixed labels within a z-band) = in-plane/G-type, which
    needs true position correspondence (not available when the slabs are offset).
    """
    z = ni_ref[:, 2]
    band = cluster_z(z, tol)
    lab = np.array(ref_lab)
    nb = int(band.max()) + 1
    rows, band_lab, pure = [], [], True
    for b in range(nb):
        m = band == b
        s = sorted(set(lab[m]))
        rows.append((b, float(z[m].mean()), int(m.sum()), "/".join(s)))
        band_lab.append(s[0] if len(s) == 1 else "?")
        if len(s) != 1:
            pure = False
    alt = pure and all(band_lab[b] != band_lab[b + 1] for b in range(nb - 1))
    return rows, band_lab, alt


def afm_layer_assign(atoms, ref_band_lab, tag, tol=0.8):
    """Assign Ni1/Ni2 by z-band alternation, phased to the ref's lowest band.
    Immune to in-plane shift AND rigid z-shift (band order preserved); the AFM
    energy is anyway invariant under global spin flip, so only the alternation
    matters. Prints the target's own band structure for a sanity cross-check."""
    labels = list(atoms.get_chemical_symbols())
    ni_idx = [i for i, s in enumerate(labels) if s == 'Ni']
    z = atoms.positions[ni_idx, 2]
    band = cluster_z(z, tol)
    lab0 = ref_band_lab[0]
    other = 'Ni2' if lab0 == 'Ni1' else 'Ni1'
    sizes = {}
    for a, idx in enumerate(ni_idx):
        labels[idx] = lab0 if band[a] % 2 == 0 else other
        sizes[int(band[a])] = sizes.get(int(band[a]), 0) + 1
    n1 = sum(1 for i in ni_idx if labels[i] == 'Ni1')
    nb = int(band.max()) + 1
    print(f"    [{tag}] z-layers: {nb} bands, sizes {[sizes[b] for b in range(nb)]} "
          f"-> Ni1 {n1}/Ni2 {len(ni_idx) - n1}")
    return labels


def afm_inplane_assign(atoms, tag, ztol=0.8):
    """In-plane AFM generated from the slab's OWN geometry, GUARANTEED net-zero
    (equal Ni1/Ni2). Ni are sorted by (z-band, x, y) and alternated GLOBALLY, so
    an even Ni count gives exactly 12/12 regardless of how the layers cluster
    (per-layer alternation would give a ferrimagnetic 13/11 seed on odd bands).
    It reproduces scf_u62's AFM TYPE (in-plane, net-zero) without needing any ref
    correspondence, so it is immune to the slabs being different structures.
    Applied identically to slab and both complexes (same atoms/order via index
    transfer) it cancels in the doped-neutral E_bind DIFFERENCE -- the Phase-B
    deliverable; the absolute E_bind then carries a common (cancelling) offset.
    """
    labels = list(atoms.get_chemical_symbols())
    ni_idx = [i for i, s in enumerate(labels) if s == 'Ni']
    pos = atoms.positions[ni_idx]
    band = cluster_z(pos[:, 2], ztol)
    nb = int(band.max()) + 1
    order = sorted(range(len(ni_idx)), key=lambda k: (
        int(band[k]), round(float(pos[k, 0]), 2), round(float(pos[k, 1]), 2)))
    for rank, k in enumerate(order):
        labels[ni_idx[k]] = 'Ni1' if rank % 2 == 0 else 'Ni2'
    n1 = sum(1 for i in ni_idx if labels[i] == 'Ni1')
    zc = [round(float(pos[band == b, 2].mean()), 2) for b in range(nb)]
    sizes = [int((band == b).sum()) for b in range(nb)]
    print(f"    [{tag}] in-plane AFM (global-alt): {nb} z-bands z={zc} sizes={sizes} "
          f"-> Ni1 {n1}/Ni2 {len(ni_idx) - n1}")
    if n1 != len(ni_idx) - n1:
        print(f"    !! net moment != 0 (odd Ni count?) — check the slab")
    return labels


def write_scf(path, atoms, labels, kind, kpts, pseudo_dir, prefix):
    """kind in {'slab','complex','molecule_doped','molecule_neutral'}."""
    has_ni = ('Ni1' in labels) or ('Ni2' in labels)
    doped_mol = (kind == 'molecule_doped')
    present = [sp for sp in SPECIES_ORDER if sp in labels]
    ntyp = len(present)
    nat = len(labels)

    sys_lines = [
        "    ibrav           = 0",
        f"    nat             = {nat}",
        f"    ntyp            = {ntyp}",
        f"    ecutwfc         = {ECUTWFC}",
        f"    ecutrho         = {ECUTRHO}",
        "    occupations     = 'smearing'",
        "    smearing        = 'mv'",
        f"    degauss         = {DEGAUSS}",
        "    nspin           = 2",
        "    nosym           = .true.",
    ]
    # spin setup
    if has_ni:                                   # slab / complex: AFM Ni guess + FSM
        sys_lines.append(f"    starting_magnetization(2) = +{AFM_MAG}   ! Ni1 up")
        sys_lines.append(f"    starting_magnetization(3) = -{AFM_MAG}   ! Ni2 down (AFM)")
        # FSM restored (2026-07-11): free-spin AFM+U sloshed (slab scf-iter 148 @ acc
        # 1.6 Ry); scf_u62's converged lineage used tot_magnetization. Slab/neutral
        # complex = 0.0 (AFM net-zero), doped complex = 1.0 (the radical electron).
        tm = 1.0 if kind == "complex_doped" else 0.0
        sys_lines.append(f"    tot_magnetization = {tm}")
    else:                                        # isolated molecule
        if doped_mol:
            sys_lines.append("    tot_magnetization = 1.0   ! [M-H] radical = doublet")
            sys_lines.append("    starting_magnetization(1) = 0.1")
        else:
            sys_lines.append("    tot_magnetization = 0.0   ! neutral molecule = singlet")
            sys_lines.append("    starting_magnetization(1) = 0.0")

    body = []
    body.append("&CONTROL")
    body.append("    calculation     = 'scf'")
    body.append(f"    prefix          = '{prefix}'")
    body.append("    outdir          = './tmp'")
    body.append(f"    pseudo_dir      = '{pseudo_dir}'")
    body.append("    tprnfor         = .true.")
    body.append("    tstress         = .false.")
    body.append("    disk_io         = 'low'")
    body.append("/")
    body.append("&SYSTEM")
    body.extend(sys_lines)
    body.append("/")
    body.append("&ELECTRONS")
    body.append(f"    conv_thr        = {CONV_THR}")
    body.append(f"    mixing_beta     = {MIX_BETA}")
    body.append("    mixing_mode     = 'local-TF'")
    body.append(f"    mixing_ndim     = {MIX_NDIM}")
    body.append("    electron_maxstep = 300")
    body.append("    diagonalization = 'david'")
    body.append("/")
    body.append("")
    body.append("ATOMIC_SPECIES")
    for sp in present:
        mass, pp = PSEUDOS[sp]
        body.append(f"  {sp:<3s} {mass:>8s}  {pp}")
    if has_ni:
        body.append("")
        body.append("HUBBARD ortho-atomic")
        body.append(f"U Ni1-3d {U_NI}")
        body.append(f"U Ni2-3d {U_NI}")
    body.append("")
    cell = atoms.cell.array
    body.append("CELL_PARAMETERS angstrom")
    for v in cell:
        body.append(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}")
    body.append("")
    body.append("ATOMIC_POSITIONS angstrom")
    for lab, p in zip(labels, atoms.positions):
        body.append(f"  {lab:<3s} {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}")
    body.append("")
    body.append("K_POINTS automatic" if kpts != "gamma" else "K_POINTS gamma")
    if kpts != "gamma":
        body.append(f"  {kpts}")
    body.append("")
    with open(path, "w") as f:
        f.write("\n".join(body))


def box_molecule(atoms):
    m = atoms.copy()
    ext = m.positions.max(axis=0) - m.positions.min(axis=0)
    L = ext + 2 * MOL_VACUUM
    m.set_cell(L)
    m.center()
    m.pbc = True
    return m


def afm_from_json(slab_atoms, afm_json):
    """Exact Ni1/Ni2 labels by index from extract_scf_slab.py's map. Use when the
    slab IS the scf_u62 geometry (slab_clean.xyz) -> no clustering/matching."""
    m = json.load(open(afm_json))
    labels = list(slab_atoms.get_chemical_symbols())
    if m["nat"] != len(labels):
        raise SystemExit(f"  !! afm_json nat {m['nat']} != slab nat {len(labels)} "
                         "-- slab is not the json's source geometry")
    for i in m["Ni1"]:
        labels[i] = 'Ni1'
    for i in m["Ni2"]:
        labels[i] = 'Ni2'
    bad = [i for i, s in enumerate(labels) if s == 'Ni']
    if bad:
        raise SystemExit(f"  !! {len(bad)} Ni not covered by afm_json indices")
    print(f"  AFM from json (exact, index-based): Ni1 {len(m['Ni1'])}/Ni2 {len(m['Ni2'])}")
    return labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref_scf", help="scf_u62.in (for --afm_mode match/layer/inplane diagnosis)")
    ap.add_argument("--afm_json", default=None,
                    help="exact Ni1/Ni2 index map from extract_scf_slab.py; when the slab is "
                         "scf_u62's own geometry this is the clean path (overrides afm_mode)")
    ap.add_argument("--slab", required=True)
    ap.add_argument("--complex_doped", required=True)
    ap.add_argument("--complex_neutral", required=True)
    ap.add_argument("--mol_doped", required=True)
    ap.add_argument("--mol_neutral", required=True)
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kpts", default=KPTS_SLAB, help="slab/complex k-grid")
    ap.add_argument("--afm_mode", default="auto",
                    choices=["auto", "layer", "inplane", "match"],
                    help="auto: layer if ref is A-type, else inplane. layer: z-band "
                         "alternation (A-type, offset-immune). inplane: 2up/2down per "
                         "z-layer from the slab's OWN geometry (in-plane AFM, needs no "
                         "ref correspondence). match: Hungarian on RANSAC-aligned ref.")
    ap.add_argument("--ztol", type=float, default=0.8, help="z-layer clustering gap (A)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    slab_atoms = read(a.slab)
    Nslab = len(slab_atoms)

    # ---- slab AFM computed ONCE, transferred to complexes by index (identical slab
    #      sublattice across slab/complex_doped/complex_neutral => clean cancellation) ----
    if a.afm_json:
        # exact index map (slab IS scf_u62's geometry): no ref parse / matching
        print("AFM source: exact index map (slab_afm.json) — clean DFT slab path")
        slab_labels = afm_from_json(slab_atoms, a.afm_json)
    else:
        if not a.ref_scf:
            raise SystemExit("provide --afm_json (clean DFT slab) or --ref_scf (diagnosis path)")
        ni_ref, ref_lab, cell = parse_ref_ni(a.ref_scf)
        print(f"ref AFM split: Ni1 x{ref_lab.count('Ni1')}  Ni2 x{ref_lab.count('Ni2')}", flush=True)
        rows, band_lab, is_A = analyze_ref_layers(ni_ref, ref_lab, a.ztol)
        print("  ref z-band diagnosis (band: <z> n label):")
        for b, zc, n, lb in rows:
            print(f"    band {b}: z={zc:5.2f}  n={n:2d}  {lb}")
        print(f"  ref pattern = {'A-type (z-layer AFM)' if is_A else 'NOT A-type (in-plane/G)'}")
        mode = a.afm_mode
        if mode == "auto":
            mode = "layer" if is_A else "inplane"
        if mode == "layer" and not is_A:
            raise SystemExit("  !! layer mode needs an A-type ref; this ref is in-plane.")
        print(f"  --> AFM assignment mode: {mode}", flush=True)
        if mode == "layer":
            slab_labels = afm_layer_assign(slab_atoms, band_lab, "slab", a.ztol)
        elif mode == "inplane":
            slab_labels = afm_inplane_assign(slab_atoms, "slab", a.ztol)
        else:
            slab_labels = split_ni(slab_atoms, ni_ref, ref_lab, slab_atoms.cell.array)
    slab_ni = {i: slab_labels[i] for i in range(Nslab) if slab_labels[i] in ('Ni1', 'Ni2')}

    jobs = [
        ("slab",            None,               "slab",             a.kpts,   "pb_slab"),
        ("complex_doped",   a.complex_doped,    "complex_doped",    a.kpts,   "pb_cxd"),
        ("complex_neutral", a.complex_neutral,  "complex_neutral",  a.kpts,   "pb_cxn"),
        ("mol_doped",       a.mol_doped,        "molecule_doped",   "gamma",  "pb_mold"),
        ("mol_neutral",     a.mol_neutral,      "molecule_neutral", "gamma",  "pb_moln"),
    ]
    for name, src, kind, kpts, prefix in jobs:
        if kind == "slab":
            atoms, labels = slab_atoms, slab_labels
        elif kind.startswith("complex"):
            atoms = read(src)
            base = list(atoms.get_chemical_symbols())
            mism = sum(1 for i in range(Nslab)
                       if base[i] != slab_atoms.get_chemical_symbols()[i])
            if mism:
                print(f"  !! {name}: {mism} of first {Nslab} atoms differ from the slab — "
                      "index transfer unsafe; check phaseA atom ordering")
            labels = base[:]
            for i in range(Nslab):
                if labels[i] == 'Ni':
                    labels[i] = slab_ni[i]        # inherit identical slab sublattice
        else:
            atoms = box_molecule(read(src))
            labels = list(atoms.get_chemical_symbols())
        d = os.path.join(a.out, name)
        os.makedirs(d, exist_ok=True)
        write_scf(os.path.join(d, "scf.in"), atoms, labels, kind, kpts,
                  a.pseudo_dir, prefix)
        nni = sum(1 for x in labels if x in ('Ni1', 'Ni2'))
        print(f"  {name:16s} nat={len(labels):3d}  Ni={nni:3d}  k={kpts}  -> {name}/scf.in",
              flush=True)

    with open(os.path.join(a.out, "README_harvest.txt"), "w") as f:
        f.write(
            "Phase-B DFT+U binding cross-check (single-point on UMA geometries)\n"
            "  E_bind(tag) = E(complex_tag) - E_slab - E_mol(tag)\n"
            "  VERDICT (robust)  = E_bind(doped) - E_bind(neutral)   (< 0 => doping strengthens)\n"
            "  The slab (and its in-plane-AFM microstate) enters both E_bind identically and\n"
            "  cancels in this difference, so the verdict does NOT depend on reproducing\n"
            "  scf_u62's exact AFM (the phaseA and scf_u62 slabs are different structures).\n"
            "  Absolute E_bind values carry a common, cancelling magnetic-state offset -- quote\n"
            "  the difference, not the absolutes.\n\n"
            "Run order (sequential; slab is the heaviest ~96+ atoms):\n"
            "  for j in slab complex_doped complex_neutral mol_doped mol_neutral; do\n"
            "    cd $j && mpirun -np <N> pw.x -in scf.in > scf.out 2>&1; cd ..\n"
            "  done\n\n"
            "Harvest:\n"
            "  for j in slab complex_doped complex_neutral mol_doped mol_neutral; do\n"
            "    printf '%-16s ' $j; grep '! *total energy' $j/scf.out | tail -1; done\n"
            "  # convert Ry->eV (x13.605693) then apply E_bind formula.\n"
        )
    print(f"\nwrote 5 inputs + README_harvest.txt under {a.out}", flush=True)


if __name__ == "__main__":
    main()
