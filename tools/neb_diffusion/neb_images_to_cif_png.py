#!/usr/bin/env python3
"""Split a multi-frame NEB path (extxyz or ASE .traj) into per-image CIF + PNG.

Each NEB image -> img{i}.cif (structure, openable in VESTA) and img{i}.png
(quick top + side view, energy in title if present).

Works two ways:
  * On gabia (where ASE + neb_path_final_dft.xyz live): uses ASE -> nicest output.
  * Anywhere with only numpy+matplotlib (e.g. this sandbox, if you paste the
    xyz): pure-numpy CIF writer + matplotlib scatter PNG fallback.

Usage:
  python3 neb_images_to_cif_png.py --in neb_path_final_dft.xyz --out_dir images_export
  python3 neb_images_to_cif_png.py --in neb.traj --out_dir images_export   # ASE only
"""
import argparse, os, re, sys
from pathlib import Path
import numpy as np

ELEM_COLORS = {  # CPK-ish, for the matplotlib fallback
    "Li": "#9b59b6", "N": "#3050f8", "C": "#404040", "O": "#ff0d0d",
    "P": "#ff8000", "S": "#ffff30", "Cl": "#1ff01f", "H": "#dddddd",
}
ELEM_SIZE = {"Li": 70, "N": 120, "C": 90, "O": 110, "P": 150, "S": 150, "Cl": 140}


# ---------- pure-numpy extxyz reader ----------
def read_extxyz(path):
    txt = open(path).read().splitlines()
    frames, i, L = [], 0, len(txt)
    while i < L:
        if not txt[i].strip():
            i += 1; continue
        n = int(txt[i].split()[0])
        comment = txt[i + 1]
        m = re.search(r'Lattice="([^"]+)"', comment)
        cell = (np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
                if m else None)
        em = re.search(r'energy=(-?[\d.eE+]+)', comment)
        energy = float(em.group(1)) if em else None
        sym, pos = [], []
        for ln in txt[i + 2:i + 2 + n]:
            t = ln.split()
            sym.append(t[0]); pos.append([float(t[1]), float(t[2]), float(t[3])])
        frames.append({"sym": sym, "pos": np.array(pos, float),
                       "cell": cell, "energy": energy})
        i += 2 + n
    return frames


# ---------- pure-numpy CIF writer ----------
def write_cif(frame, path, title="image"):
    cell, pos, sym = frame["cell"], frame["pos"], frame["sym"]
    if cell is None:
        sys.exit("ERROR: no Lattice in xyz comment -> cannot write CIF "
                 "(need a periodic cell). Use the extxyz from run_neb_qe.py.")
    a, b, c = (np.linalg.norm(cell[i]) for i in range(3))
    ang = lambda u, v: np.degrees(np.arccos(
        np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))
    alpha, beta, gamma = ang(cell[1], cell[2]), ang(cell[0], cell[2]), ang(cell[0], cell[1])
    frac = pos @ np.linalg.inv(cell)
    cnt = {}
    with open(path, "w") as f:
        f.write(f"data_{title}\n")
        f.write(f"_cell_length_a {a:.6f}\n_cell_length_b {b:.6f}\n_cell_length_c {c:.6f}\n")
        f.write(f"_cell_angle_alpha {alpha:.4f}\n_cell_angle_beta {beta:.4f}\n"
                f"_cell_angle_gamma {gamma:.4f}\n")
        f.write("_symmetry_space_group_name_H-M 'P 1'\n_symmetry_Int_Tables_number 1\n")
        f.write("loop_\n _atom_site_label\n _atom_site_type_symbol\n"
                " _atom_site_fract_x\n _atom_site_fract_y\n _atom_site_fract_z\n")
        for s, (fx, fy, fz) in zip(sym, frac):
            cnt[s] = cnt.get(s, 0) + 1
            f.write(f"{s}{cnt[s]} {s} {fx:.6f} {fy:.6f} {fz:.6f}\n")


# ---------- matplotlib fallback PNG (top + side) ----------
def render_png_mpl(frame, path, title):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pos, sym = frame["pos"], np.array(frame["sym"])
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    for ax, (h, v, lab) in zip(axs, [(0, 1, "top (x-y)"), (0, 2, "side (x-z)")]):
        for e in sorted(set(sym)):
            mk = sym == e
            ax.scatter(pos[mk, h], pos[mk, v], s=ELEM_SIZE.get(e, 100),
                       c=ELEM_COLORS.get(e, "#888"), edgecolors="k",
                       linewidths=0.3, label=e, alpha=0.9)
        ax.set_aspect("equal"); ax.set_title(lab, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    axs[1].legend(fontsize=7, loc="upper right", ncol=2)
    fig.suptitle(title, fontsize=11)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="neb_path_final_dft.xyz or neb.traj")
    ap.add_argument("--out_dir", default="images_export")
    ap.add_argument("--no_png", action="store_true", help="CIF only")
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    use_ase = False
    try:
        from ase.io import read, write  # noqa
        use_ase = True
    except Exception:
        if args.inp.endswith(".traj"):
            sys.exit("ERROR: .traj needs ASE (not installed). Give the extxyz instead.")

    if use_ase:
        from ase.io import read, write
        imgs = read(args.inp, index=":")
        try:
            E0 = imgs[0].get_potential_energy()
        except Exception:
            E0 = None
        for i, a in enumerate(imgs):
            write(str(out / f"img{i}.cif"), a)
            if not args.no_png:
                try:
                    e = a.get_potential_energy()
                    rel = f"  E_rel={ (e-E0)*1000:.0f} meV" if E0 is not None else ""
                except Exception:
                    rel = ""
                write(str(out / f"img{i}_top.png"), a, rotation="0x,0y,0z")
                write(str(out / f"img{i}_side.png"), a, rotation="-90x")
        print(f"[ASE] wrote {len(imgs)} images -> {out}/ (img*.cif + *_top/_side.png)")
    else:
        frames = read_extxyz(args.inp)
        E0 = frames[0]["energy"]
        for i, fr in enumerate(frames):
            write_cif(fr, out / f"img{i}.cif", title=f"img{i}")
            if not args.no_png:
                rel = (f"  E_rel={(fr['energy']-E0)*1000:.0f} meV"
                       if (fr["energy"] is not None and E0 is not None) else "")
                render_png_mpl(fr, out / f"img{i}.png", f"NEB image {i}{rel}")
        print(f"[numpy] wrote {len(frames)} images -> {out}/ (img*.cif"
              f"{'' if args.no_png else ' + img*.png'})")


if __name__ == "__main__":
    main()
