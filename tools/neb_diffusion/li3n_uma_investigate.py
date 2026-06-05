#!/usr/bin/env python3
"""Li3N(001) Li-adatom — systematic UMA investigation (why is UMA 0.054 ≪ paper 0.133?).

Diagnostic logic
----------------
UMA-oc20 reproduces LiC6 (0.241 vs DFT 0.287, 0.84x) but gives Li3N 0.054 vs paper
0.133 (0.41x). UMA is therefore NOT generically broken for surface adatoms -> the
Li3N gap is most likely a SETUP issue (termination / adsorption site / path def).
This script isolates the cause, step by step, all with UMA-oc20.

  sites : place adatom at on-N / bridge / hollow / top-Li, relax (top layers free),
          report ABSOLUTE binding energy (vs isolated Li and vs clean slab) + the
          adatom's final height (did it stay ON the surface or incorporate?).
          -> compare binding to paper's -3.44 eV; find the TRUE minimum site.
  neb   : CI-NEB between two chosen site minima (default on-N -> adjacent on-N,
          the paper's path), barrier = max(E)-E(start). Same protocol as LiC6.
  sweep : repeat `sites`+`neb` over {termination, n_layers, supercell, task} to see
          which knob moves the barrier toward 0.133.

Reuses slab builders from li3n_mlneb_gpaw.py. Deps: ase, fairchem. Runs in minutes.

Examples (on a node with fairchem + GPU):
  python3 li3n_uma_investigate.py sites --task oc20 --supercell 3 3 --layers 6
  python3 li3n_uma_investigate.py neb   --task oc20 --supercell 3 3 --layers 6 \
          --start on_N --end on_N_adj --images 7
  python3 li3n_uma_investigate.py sweep --task oc20
"""
import argparse, json, itertools
from pathlib import Path
import numpy as np
from ase import Atom, Atoms
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.mep import NEB
from li3n_mlneb_gpaw import build_li3n_001, freeze_bottom, top_N_sites, make_calc


def slab_and_calc(A):
    slab = build_li3n_001(nlayers=A.layers, supercell=(A.supercell[0], A.supercell[1], 1),
                          terminate=A.term)
    fixed = freeze_bottom(slab, relax_top_layers=A.relax_top, nlayers=A.layers)
    # diagnostic: is the top plane N-exposed (paper) or pure-Li?
    z = slab.positions[:, 2]; sym = np.array(slab.get_chemical_symbols())
    ztop = z.max(); top_has_N = bool(((np.abs(z - ztop) < 1.0) & (sym == "N")).any())
    zntop = z[sym == "N"].max()
    print(f"[slab] term={A.term}: top plane {'N-EXPOSED' if top_has_N or abs(zntop-ztop)<0.4 else 'pure-Li (N buried %.2f A)'%(ztop-zntop)}"
          f" | {len(slab)} atoms, topN z={zntop:.2f}, ztop={ztop:.2f}")
    calc = make_calc("uma", A.task, A.device)
    return slab, fixed, calc


def candidate_sites(slab, h=1.9):
    """Return dict name->xyz for adatom candidate adsorption positions."""
    Ntop = top_N_sites(slab)
    P = slab.positions[Ntop]
    z = P[:, 2].max()
    # nearest-neighbour N pair (for bridge + adjacent on-N)
    p0 = P[0]
    d = np.linalg.norm(P[:, :2] - p0[:2], axis=1); d[d < 1e-3] = 1e9
    j = int(np.argmin(d)); p1 = P[j]
    # the two N completing triangles on either side of the p0-p1 edge ->
    # gives two ADJACENT hollow sites (share that edge) = a hollow->hollow hop,
    # which is UMA's true MEP (UMA minimum is the hollow, not on-N).
    ds = np.linalg.norm(P[:, :2] - p0[:2], axis=1) + np.linalg.norm(P[:, :2] - p1[:2], axis=1)
    ds[np.linalg.norm(P[:, :2] - p0[:2], axis=1) < 1e-3] = 1e9
    ds[np.linalg.norm(P[:, :2] - p1[:2], axis=1) < 1e-3] = 1e9
    near = np.argsort(ds)
    pa, pb = P[near[0]], P[near[1]]
    cen = lambda *ps: [np.mean([q[0] for q in ps]), np.mean([q[1] for q in ps]), z + h * 0.9]
    sites = {
        "on_N":       [p0[0], p0[1], z + h],
        "on_N_adj":   [p1[0], p1[1], z + h],
        "bridge":     [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, z + h * 0.9],
        "hollow":     cen(p0, p1, pa),
        "hollow_adj": cen(p0, p1, pb),
    }
    return sites


def relax_adatom(slab, fixed, calc, xyz, fmax=0.02, steps=300, tag="x", logdir="."):
    at = slab.copy()
    at += Atom("Li", position=xyz)
    at.set_constraint(FixAtoms(indices=fixed))     # adatom (last) free
    at.calc = calc
    BFGS(at, logfile=f"{logdir}/relax_{tag}.log").run(fmax=fmax, steps=steps)
    return at


def isolated_Li_energy(calc):
    a = Atoms("Li", positions=[[0, 0, 0]], cell=[20, 20, 20], pbc=True)
    a.calc = calc
    return a.get_potential_energy()


def cmd_sites(A):
    slab, fixed, calc = slab_and_calc(A)
    e_slab = (slab.copy(), slab)[1]; sc = slab.copy(); sc.calc = calc
    E_slab = sc.get_potential_energy()
    E_Li = isolated_Li_energy(calc)
    z_surf = slab.positions[top_N_sites(slab), 2].max()
    print(f"[sites] task={A.task} cell={A.supercell} layers={A.layers} "
          f"| E_slab={E_slab:.3f}  E_Li(iso)={E_Li:.3f}  z_surf(N)={z_surf:.2f}")
    sites = candidate_sites(slab)
    rows = {}
    for name, xyz in sites.items():
        at = relax_adatom(slab, fixed, calc, xyz, tag=name)
        E = at.get_potential_energy()
        zad = at.positions[-1, 2]
        Eb = E - E_slab - E_Li
        incon = "INCORPORATED" if zad < z_surf - 0.3 else "surface"
        rows[name] = dict(E=float(E), E_bind=float(Eb), z_adatom=float(zad), state=incon)
        print(f"  {name:9s}: E_bind={Eb:+.3f} eV  z_ad={zad:5.2f} ({incon})")
    emin = min(rows, key=lambda k: rows[k]["E_bind"])
    print(f"  --> lowest site (UMA): {emin}  E_bind={rows[emin]['E_bind']:+.3f} eV "
          f"(paper on-N |(002): -3.44 eV)")
    json.dump({"settings": vars(A), "E_slab": E_slab, "E_Li_iso": E_Li, "sites": rows},
              open(f"{A.out}_sites.json", "w"), indent=1)
    print(f"  wrote {A.out}_sites.json")
    return rows


def cmd_neb(A):
    slab, fixed, calc = slab_and_calc(A)
    sites = candidate_sites(slab)
    ini = relax_adatom(slab, fixed, calc, sites[A.start], tag="ini")
    fin = relax_adatom(slab, fixed, calc, sites[A.end],   tag="fin")
    images = [ini] + [ini.copy() for _ in range(A.images - 2)] + [fin]
    for im in images:
        im.set_constraint(FixAtoms(indices=fixed)); im.calc = make_calc("uma", A.task, A.device)
    neb = NEB(images, climb=False, k=0.1)
    neb.interpolate("idpp")
    BFGS(neb, logfile=f"{A.out}_neb.log").run(fmax=0.1, steps=200)   # warm-up
    neb.climb = True
    BFGS(neb, logfile=f"{A.out}_neb.log").run(fmax=A.fmax, steps=400)  # CI
    E = np.array([im.get_potential_energy() for im in images]); E -= E[0]
    barrier = float(E.max())
    print(f"\n=== Li3N(001) {A.start}->{A.end} UMA-{A.task} CI-NEB ({A.images} img) ===")
    print("  rel-E (eV):", [round(float(x), 4) for x in E])
    print(f"  BARRIER = {barrier:.4f} eV   (paper 0.133)")
    from ase.io import write
    write(f"{A.out}_neb.traj", images)
    json.dump({"settings": vars(A), "rel_E": [float(x) for x in E], "barrier": barrier},
              open(f"{A.out}_neb.json", "w"), indent=1)
    print(f"  wrote {A.out}_neb.json , {A.out}_neb.traj")
    return barrier


def cmd_dft_sites(A):
    """Generate DFT (QE) relax inputs for adatom at on-N / hollow / bridge on a SMALL
    N-exposed slab. The DECISIVE arbiter of UMA's hollow vs DFT's on-N preference:
    DFT, not UMA, decides the route. Adatom xy-pinned (z+substrate free) so each
    lateral site's energy is read cleanly (on-N can't slide to hollow before measure).
    BFGS relax, NOT NEB -> hours, not days. Lowest final energy = DFT-preferred site."""
    from dft_drag import grab_card
    from ase import Atom
    sx, sy = A.supercell
    slab = build_li3n_001(nlayers=A.layers, supercell=(sx, sy, 1), terminate="N")
    fixed = set(freeze_bottom(slab, relax_top_layers=max(1, A.layers - 2), nlayers=A.layers))
    sites = candidate_sites(slab)
    tmpl = Path(A.template).read_text()
    species = grab_card(tmpl, "ATOMIC_SPECIES")
    ntyp = len(set(slab.get_chemical_symbols()))            # Li, N -> 2 (adatom is Li)
    cell = slab.cell.array
    kx = max(1, round(22.0 / (3.65 * sx))); ky = max(1, round(22.0 / (3.65 * sy)))
    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    cellstr = "CELL_PARAMETERS angstrom\n" + "\n".join(
        f"  {cell[i,0]:.10f} {cell[i,1]:.10f} {cell[i,2]:.10f}" for i in range(3))
    names = ["on_N", "hollow", "bridge"]
    print(f"[dft_sites] {len(slab)+1} atoms ({sx}x{sy}x{A.layers} N-exposed), "
          f"{len(fixed)} fixed, k={kx}x{ky}x1, adatom pin={A.pin}")
    for name in names:
        at = slab.copy(); at += Atom("Li", position=sites[name])
        syms = at.get_chemical_symbols(); pos = at.get_positions(); nat = len(at)
        plines = ["ATOMIC_POSITIONS angstrom"]
        for k in range(nat):
            if k == nat - 1:
                fl = "0 0 1" if A.pin == "xy" else "1 1 1"     # adatom xy-pin (z free) or free
            else:
                fl = "0 0 0" if k in fixed else "1 1 1"
            plines.append(f"  {syms[k]:3s} {pos[k,0]:.8f} {pos[k,1]:.8f} {pos[k,2]:.8f}  {fl}")
        ctrl = ("&CONTROL\n  calculation = 'relax'\n  prefix = 'li3n_dftsite_%s'\n"
                "  pseudo_dir = '/data/work/pseudo'\n  outdir = './tmp_%s/'\n"
                "  tprnfor = .true.\n  tstress = .false.\n  verbosity = 'low'\n  disk_io = 'low'\n"
                "  nstep = 100\n  forc_conv_thr = 1.0d-3\n  etot_conv_thr = 1.0d-5\n/\n" % (name, name))
        syst = ("&SYSTEM\n  ibrav=0\n  nat=%d\n  ntyp=%d\n  ecutwfc=60.0\n  ecutrho=480.0\n"
                "  occupations='smearing'\n  smearing='mv'\n  degauss=0.01\n  nosym=.true.\n/\n" % (nat, ntyp))
        elec = ("&ELECTRONS\n  conv_thr=1.0e-08\n  mixing_beta=0.3\n  electron_maxstep=300\n/\n")
        ions = ("&IONS\n  ion_dynamics='bfgs'\n  pot_extrapolation='none'\n  wfc_extrapolation='none'\n/\n")
        kpt = f"K_POINTS automatic\n  {kx} {ky} 1  0 0 0"
        inp = (ctrl + syst + elec + ions + "\n" + species + "\n\n" + kpt + "\n\n"
               + cellstr + "\n\n" + "\n".join(plines) + "\n")
        (out / f"{name}.in").write_text(inp)
        print(f"  wrote {name}.in")
    (out / "run_dft_sites.sh").write_text(_DFT_SITES_LAUNCHER)
    print(f"-> {out}/  : bash run_dft_sites.sh  (3 DFT relax, ranks E -> DFT-preferred site)")


_DFT_SITES_LAUNCHER = r"""#!/bin/bash
set -e
cd "$(dirname "$(realpath "$0")")"
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:$PATH
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun
for f in on_N hollow bridge; do
  [ -f "$f.out" ] && grep -q "JOB DONE" "$f.out" && { echo "skip $f"; continue; }
  echo "=== $f ==="; $MPIRUN --bind-to none -np 1 $QE -inp "$f.in" > "$f.out" 2>&1 || echo "  nonzero"
done
echo; echo "=== DFT site preference (lower = preferred; UMA said hollow, paper/chem say on_N) ==="
python3 - <<'PY'
import re,glob
r=[]
for f in ("on_N","hollow","bridge"):
    try: t=open(f+".out").read()
    except FileNotFoundError: continue
    m=re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)",t)
    if m: r.append((f,float(m[-1])*13.605693))
if r:
    e0=min(e for _,e in r)
    for f,e in sorted(r,key=lambda x:x[1]): print(f"  {f:7s}  {e-e0:+.4f} eV (rel)")
    print(f"  -> DFT-preferred site: {min(r,key=lambda x:x[1])[0]}")
PY
"""


def cmd_sweep(A):
    print("[sweep] scanning termination/thickness/size knobs (on_N->on_N_adj barrier)")
    grid = dict(term=["N", "Li"], layers=[4, 6, 8], supercell=[(3, 3), (4, 4)])
    results = []
    for TM, L, S in itertools.product(grid["term"], grid["layers"], grid["supercell"]):
        A.term, A.layers, A.supercell = TM, L, S
        A.start, A.end = "on_N", "on_N_adj"
        A.out = f"sweep_{TM}_L{L}_S{S[0]}x{S[1]}_{A.task}"
        try:
            b = cmd_neb(A)
            results.append((TM, L, S, b))
        except Exception as e:
            print(f"  {TM} L{L} S{S}: FAIL {e}")
    print("\n[sweep] summary (term, layers, cell -> barrier eV; paper 0.133):")
    for TM, L, S, b in results:
        print(f"  term={TM} L{L} {S[0]}x{S[1]}: {b:.4f}")
    json.dump([dict(term=TM, layers=L, supercell=S, task=A.task, barrier=b)
               for TM, L, S, b in results], open("li3n_uma_sweep.json", "w"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("sites", "neb", "sweep", "dft_sites"):
        p = sub.add_parser(name)
        p.add_argument("--task", default="oc20", help="UMA task (oc20=surface; omat=bulk, avoid)")
        p.add_argument("--term", default="N", choices=["N", "Li"],
                       help="surface termination: N=Li2N N-exposed (paper); Li=pure-Li")
        p.add_argument("--device", default="cuda")
        p.add_argument("--layers", type=int, default=6)
        p.add_argument("--supercell", type=int, nargs=2, default=[3, 3])
        p.add_argument("--relax_top", type=int, default=5)
        p.add_argument("--out", default="li3n_uma")
        if name == "dft_sites":
            p.set_defaults(layers=5, supercell=[2, 2], out="li3n_dft_sites")
            p.add_argument("--template", required=True,
                           help="QE input with Li/N ATOMIC_SPECIES (e.g. li3n_dft_drag/drag_p0.in)")
            p.add_argument("--pin", default="xy", choices=["xy", "free"],
                           help="adatom: xy-pinned z-free (clean site energy) or fully free")
        if name == "neb":
            p.add_argument("--start", default="on_N",
                           choices=["on_N", "on_N_adj", "bridge", "hollow", "hollow_adj"])
            p.add_argument("--end", default="on_N_adj",
                           choices=["on_N", "on_N_adj", "bridge", "hollow", "hollow_adj"])
            p.add_argument("--images", type=int, default=7)
            p.add_argument("--fmax", type=float, default=0.05)
        if name == "sweep":
            p.add_argument("--images", type=int, default=7)
            p.add_argument("--fmax", type=float, default=0.05)
    A = ap.parse_args()
    {"sites": cmd_sites, "neb": cmd_neb, "sweep": cmd_sweep,
     "dft_sites": cmd_dft_sites}[A.cmd](A)


if __name__ == "__main__":
    main()
