#!/usr/bin/env python3
"""Li+ probability-density isosurface from an AIMD trajectory -> Gaussian .cube (VESTA).

Reproduces the "(f1/f2/f3) Cl1/Cl1.5/Cl2" type figure: time-average the mobile-ion
positions over the AIMD trajectory onto a 3D grid -> the Li probability density.
Rendered in VESTA as an isosurface over the framework, it shows the Li diffusion
network (Cl-rich -> more connected/3D -> higher sigma).

Output .cube contains the FRAMEWORK atoms (everything except --species, at their
trajectory-averaged positions) + the Li density as volumetric data. Open in VESTA;
the Li cloud is the isosurface, the framework gives context.

numpy-only; reads multi-frame extended-xyz (aimd_mlip traj.xyz). Periodic Gaussian
smoothing via FFT (no scipy needed).

Usage:
  python3 li_density_cube.py --traj T600/traj.xyz --out comp1_T600_Li.cube \
      --skip 100 --spacing 0.2 --sigma_A 0.4
  (--skip drops equilibration frames; VESTA isosurface level ~0.3-0.6 of max)
"""
import numpy as np, re, argparse

BOHR = 1.8897259886  # Å -> Bohr
Z = {"H":1,"Li":3,"B":5,"C":6,"N":7,"O":8,"F":9,"Na":11,"Mg":12,"Al":13,"Si":14,
     "P":15,"S":16,"Cl":17,"K":19,"Ca":20,"Sc":21,"Ti":22,"V":23,"Cr":24,"Mn":25,
     "Fe":26,"Co":27,"Ni":28,"Cu":29,"Zn":30,"Ga":31,"Ge":32,"As":33,"Br":35,
     "Y":39,"Zr":40,"Nb":41,"Mo":42,"Ag":47,"Sn":50,"Sb":51,"I":53,"Ba":56,
     "La":57,"Nd":60,"Sm":62,"Gd":64,"Hf":72,"Ta":73,"W":74}


def read_traj(path):
    txt = open(path).read().splitlines()
    pos, cells, sym, i, L = [], [], None, 0, len(txt)
    while i < L:
        if not txt[i].strip():
            i += 1; continue
        n = int(txt[i].split()[0])
        m = re.search(r'Lattice="([^"]+)"', txt[i + 1])
        cell = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
        s, p = [], []
        for ln in txt[i + 2:i + 2 + n]:
            t = ln.split()
            s.append(t[0]); p.append([float(t[1]), float(t[2]), float(t[3])])
        if sym is None:
            sym = np.array(s)
        pos.append(p); cells.append(cell); i += 2 + n
    return sym, np.array(pos, float), np.array(cells, float)


def smooth_periodic(rho, sig_vox):
    F = np.fft.fftn(rho)
    for ax, nn in enumerate(rho.shape):
        k = np.fft.fftfreq(nn)
        g = np.exp(-2 * np.pi**2 * sig_vox[ax]**2 * k**2)
        sh = [1, 1, 1]; sh[ax] = nn
        F = F * g.reshape(sh)
    return np.real(np.fft.ifftn(F))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traj", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--species", default="Li")
    ap.add_argument("--spacing", type=float, default=0.2, help="grid spacing (Å)")
    ap.add_argument("--sigma_A", type=float, default=0.4, help="Gaussian smoothing (Å)")
    ap.add_argument("--skip", type=int, default=0, help="skip first N frames (equilib)")
    args = ap.parse_args()

    sym, pos, cells = read_traj(args.traj)
    if args.skip:
        pos = pos[args.skip:]
    cell = cells[0]; cinv = np.linalg.inv(cell)
    mob = np.where(sym == args.species)[0]
    fw = np.where(sym != args.species)[0]
    if len(mob) == 0:
        raise SystemExit(f"no {args.species} atoms in {args.traj}")

    lens = np.linalg.norm(cell, axis=1)
    n = np.maximum(8, np.round(lens / args.spacing).astype(int))

    rho = np.zeros(tuple(n))
    for t in range(len(pos)):
        frac = (pos[t][mob] @ cinv) % 1.0
        idx = (np.floor(frac * n).astype(int)) % n
        np.add.at(rho, (idx[:, 0], idx[:, 1], idx[:, 2]), 1.0)
    rho /= len(pos)
    rho = smooth_periodic(rho, args.sigma_A / (lens / n))

    avg = pos.mean(0)
    with open(args.out, "w") as f:
        f.write("Li+ probability density from AIMD (VESTA isosurface)\n")
        f.write(f"{args.species} density | {len(pos)} frames | spacing {args.spacing} A | sigma {args.sigma_A} A\n")
        f.write(f"{len(fw):5d} 0.000000 0.000000 0.000000\n")
        for ax in range(3):
            v = cell[ax] / n[ax] * BOHR
            f.write(f"{int(n[ax]):5d} {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for a in fw:
            zz = Z.get(sym[a], 0); r = avg[a] * BOHR
            f.write(f"{zz:5d} {float(zz):.6f} {r[0]:.6f} {r[1]:.6f} {r[2]:.6f}\n")
        flat = rho.flatten()  # C-order -> last axis fastest (cube convention)
        for i in range(0, len(flat), 6):
            f.write(" ".join(f"{x:.5e}" for x in flat[i:i + 6]) + "\n")

    print(f"-> {args.out}")
    print(f"   grid {tuple(int(x) for x in n)}  framework atoms {len(fw)}  "
          f"{len(mob)} {args.species}  frames {len(pos)}")
    print(f"   rho max {rho.max():.4f}  mean {rho.mean():.5f}  "
          f"-> VESTA isosurface level ~{0.4*rho.max():.3f} (try 0.3-0.6x max)")


if __name__ == "__main__":
    main()
