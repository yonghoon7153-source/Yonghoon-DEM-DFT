#!/usr/bin/env python3
"""k-point convergence scan for QE SCF — run BEFORE trusting any DFT property.

A too-sparse Monkhorst-Pack mesh silently corrupts geometry (residual forces),
band gap (DOS), and elastic constants. This script runs single-point SCF at a
series of k-meshes on a FIXED geometry and reports where total energy / pressure
/ force converge, so the production mesh is chosen by measurement, not guesswork.

It does NOT relax — it measures k-sensitivity at one geometry. The absolute
geometry may be imperfect; that does not affect the conclusion about which mesh
is needed (the ΔE(k) plateau is geometry-independent to good approximation).

Convergence metric: |ΔE/atom| between consecutive meshes < --conv_meV_atom.

Usage (on the container, QE in PATH):
    python3 kconv_scan.py \
        --template /path/to/scf_tight.in \
        --kgrids 2x2x2 3x3x3 4x4x4 5x5x5 6x6x6 \
        --pw "mpirun --bind-to none -np 1 pw.x" \
        --workdir kconv \
        --conv_meV_atom 1.0

The template must be a complete SCF input (CONTROL/SYSTEM/ELECTRONS + cards).
Its existing K_POINTS block is replaced for each grid. prefix/outdir are made
unique per grid so runs don't clobber each other.
"""
import argparse
import json
import re
import subprocess
import time
from pathlib import Path

RY_TO_EV = 13.605693122994
RY_BOHR_TO_EV_ANG = 25.71104309541616  # 1 Ry/bohr in eV/Angstrom


def replace_kpoints(text: str, kx: int, ky: int, kz: int) -> str:
    """Replace the K_POINTS automatic block (header + next line) with a new grid."""
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip().upper().startswith("K_POINTS"):
            out.append("K_POINTS automatic")
            out.append(f"  {kx} {ky} {kz}  0 0 0")
            i += 2  # skip old header + old grid line
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + "\n"


def set_namelist_value(text: str, key: str, value: str) -> str:
    """Set or insert `key = value` inside namelists (simple key replace)."""
    pat = re.compile(rf"^(\s*){re.escape(key)}\s*=.*$", re.MULTILINE)
    if pat.search(text):
        return pat.sub(rf"\g<1>{key} = {value}", text, count=1)
    # insert after &CONTROL
    return re.sub(r"(&CONTROL\s*\n)", rf"\1  {key} = {value}\n", text, count=1)


def count_atoms(text: str) -> int:
    m = re.search(r"^\s*nat\s*=\s*(\d+)", text, re.MULTILINE | re.IGNORECASE)
    return int(m.group(1)) if m else 0


def parse_scf_out(out_path: Path):
    """Extract total energy (Ry), pressure (kbar), total force (Ry/bohr),
    n_kpoints, and JOB DONE flag from a pw.x output."""
    txt = out_path.read_text(errors="ignore")
    res = {"job_done": "JOB DONE" in txt}
    m = re.findall(r"^!\s+total energy\s*=\s*([-\d.]+)\s*Ry", txt, re.MULTILINE)
    res["E_Ry"] = float(m[-1]) if m else None
    m = re.findall(r"P=\s*([-\d.]+)", txt)
    res["P_kbar"] = float(m[-1]) if m else None
    m = re.findall(r"Total force\s*=\s*([-\d.]+)", txt)
    res["total_force_Ry_bohr"] = float(m[-1]) if m else None
    m = re.search(r"number of k points=\s*(\d+)", txt)
    res["n_kpoints"] = int(m.group(1)) if m else None
    # anisotropy of stress (cubic should be isotropic): read 3x3 stress in kbar
    sm = re.search(r"total\s+stress.*?\n((?:\s*[-\d.]+.*\n){3})", txt)
    if sm:
        rows = []
        for ln in sm.group(1).strip().splitlines():
            nums = [float(x) for x in ln.split()]
            # each row: 3 Ry/bohr^3 then 3 kbar
            rows.append(nums[3:6] if len(nums) >= 6 else nums[:3])
        if len(rows) == 3:
            sxx, syy, szz = rows[0][0], rows[1][1], rows[2][2]
            shear = max(abs(rows[0][1]), abs(rows[0][2]), abs(rows[1][2]))
            res["stress_diag_kbar"] = [sxx, syy, szz]
            res["stress_anisotropy_kbar"] = max(sxx, syy, szz) - min(sxx, syy, szz)
            res["stress_max_shear_kbar"] = shear
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--kgrids", nargs="+", default=["2x2x2", "3x3x3", "4x4x4", "5x5x5", "6x6x6"])
    ap.add_argument("--pw", default="mpirun --bind-to none -np 1 pw.x")
    ap.add_argument("--workdir", default="kconv")
    ap.add_argument("--conv_meV_atom", type=float, default=1.0)
    ap.add_argument("--omp", type=int, default=8)
    ap.add_argument("--skip_existing", action="store_true",
                    help="reuse an existing converged .out instead of re-running")
    args = ap.parse_args()

    tmpl_text = Path(args.template).read_text()
    nat = count_atoms(tmpl_text)
    if nat == 0:
        raise SystemExit("could not read nat from template")
    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)
    print(f"template={args.template}  nat={nat}  workdir={wd}")

    import os
    env = dict(os.environ, OMP_NUM_THREADS=str(args.omp))

    results = []
    for kg in args.kgrids:
        kx, ky, kz = (int(x) for x in kg.lower().split("x"))
        tag = f"k{kx}{ky}{kz}"
        inp = wd / f"scf_{tag}.in"
        outp = wd / f"scf_{tag}.out"

        text = replace_kpoints(tmpl_text, kx, ky, kz)
        text = set_namelist_value(text, "prefix", f"'kconv_{tag}'")
        text = set_namelist_value(text, "outdir", f"'./tmp_{tag}/'")
        inp.write_text(text)

        if args.skip_existing and outp.exists() and "JOB DONE" in outp.read_text(errors="ignore"):
            print(f"[{tag}] reuse existing {outp}")
        else:
            print(f"[{tag}] running {kx}x{ky}x{kz} ...", flush=True)
            t0 = time.time()
            with open(outp, "w") as fo:
                subprocess.run(args.pw.split() + ["-inp", str(inp)],
                               stdout=fo, stderr=subprocess.STDOUT, env=env, check=False)
            print(f"[{tag}] done in {(time.time()-t0)/60:.1f} min", flush=True)

        r = parse_scf_out(outp)
        r.update({"kgrid": kg, "kx": kx, "ky": ky, "kz": kz, "tag": tag, "nat": nat})
        if r["E_Ry"] is not None:
            r["E_eV_per_atom"] = r["E_Ry"] * RY_TO_EV / nat
        if r.get("total_force_Ry_bohr") is not None:
            r["total_force_eV_ang"] = r["total_force_Ry_bohr"] * RY_BOHR_TO_EV_ANG
        results.append(r)

    # convergence table
    print("\n" + "=" * 92)
    header = ("kgrid", "nk", "E/atom(eV)", "dE/atom(meV)", "P(kbar)",
              "aniso(kbar)", "Ftot(eV/A)", "done")
    print(f"{header[0]:>8} {header[1]:>5} {header[2]:>13} {header[3]:>13} "
          f"{header[4]:>9} {header[5]:>11} {header[6]:>11} {header[7]:>5}")
    print("-" * 92)
    prev_E = None
    converged_grid = None
    for r in results:
        epa = r.get("E_eV_per_atom")
        dE = (abs(epa - prev_E) * 1000) if (epa is not None and prev_E is not None) else None
        if dE is not None and dE < args.conv_meV_atom and converged_grid is None:
            converged_grid = r["kgrid"]
        epa_s = "-" if epa is None else f"{epa:.5f}"
        dE_s = "" if dE is None else f"{dE:.2f}"
        P_val = r.get("P_kbar")
        P_s = "?" if P_val is None else f"{P_val:.2f}"
        an_val = r.get("stress_anisotropy_kbar")
        an_s = "?" if an_val is None else f"{an_val:.2f}"
        ftot = r.get("total_force_eV_ang")
        ftot_s = "" if ftot is None else f"{ftot:.3f}"
        nk_s = str(r.get("n_kpoints", "?"))
        print(f"{r['kgrid']:>8} {nk_s:>5} {epa_s:>13} {dE_s:>13} "
              f"{P_s:>9} {an_s:>11} {ftot_s:>11} {str(r['job_done']):>5}")
        prev_E = epa if epa is not None else prev_E
    print("=" * 92)
    print(f"Converged at: {converged_grid or 'NOT REACHED'} "
          f"(|dE/atom| < {args.conv_meV_atom} meV between consecutive meshes)")
    print("Note: stress anisotropy on a CUBIC cell should → 0; nonzero means the "
          "geometry broke symmetry (under-converged relax).")

    # plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ks = [r["kx"] for r in results]
        epa = [r.get("E_eV_per_atom") for r in results]
        P = [r.get("P_kbar") for r in results]
        aniso = [r.get("stress_anisotropy_kbar") for r in results]
        fig, ax = plt.subplots(1, 3, figsize=(15, 4))
        ax[0].plot(ks, epa, "o-"); ax[0].set_xlabel("k (per axis)")
        ax[0].set_ylabel("E/atom (eV)"); ax[0].set_title("Total energy convergence"); ax[0].grid(alpha=0.3)
        ax[1].plot(ks, P, "s-", color="C1"); ax[1].set_xlabel("k (per axis)")
        ax[1].set_ylabel("Pressure (kbar)"); ax[1].set_title("Pressure convergence"); ax[1].grid(alpha=0.3)
        ax[2].plot(ks, aniso, "^-", color="C3"); ax[2].set_xlabel("k (per axis)")
        ax[2].set_ylabel("stress anisotropy (kbar)")
        ax[2].set_title("Cubic-symmetry breaking (→0 = good)"); ax[2].grid(alpha=0.3)
        plt.tight_layout()
        png = wd / "kconv.png"
        plt.savefig(png, dpi=160, facecolor="white")
        print(f"  → {png}")
    except Exception as e:
        print(f"  (plot skipped: {e})")

    summary = {
        "template": args.template, "nat": nat,
        "conv_meV_atom": args.conv_meV_atom,
        "converged_grid": converged_grid,
        "results": results,
    }
    (wd / "kconv_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"  → {wd / 'kconv_summary.json'}")


if __name__ == "__main__":
    main()
