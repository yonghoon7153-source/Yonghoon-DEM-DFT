#!/usr/bin/env python3
"""Fit elastic constants from 12 finite-difference strain SCFs.

Each pair of ±h strain SCFs gives one diagonal Voigt elastic constant via:
    C_ii_normal = (E(+h) + E(-h) - 2 E0) / (V0 * h^2)        [i = 1,2,3]
    C_ii_shear  = (E(+h) + E(-h) - 2 E0) / (V0 * (2h)^2)     [i = 4,5,6 — γ = 2 ε_tensor]

For cubic symmetry (LPSCl argyrodite F-43m), there are 3 independent
constants (C11, C12, C44). Diagonal Voigt entries are averaged:
    C11 = mean(C11, C22, C33)
    C44 = mean(C44, C55, C66)
C12 is recovered using the BM-EOS bulk modulus K:
    K  = (C11 + 2 C12) / 3   →   C12 = (3 K − C11) / 2

VRH (Voigt–Reuss–Hill) averaging then yields B, G; from these:
    E = 9 B G / (3 B + G)
    ν = (3 B − 2 G) / (2 (3 B + G))

Usage:
    python3 fit_elastic_cij.py \\
        --workdir /home/.../elastic_static \\
        --v0_ry   -1262.91500 \\
        --v0_A3   XXX.X \\
        --strain  0.005 \\
        --bulk_GPa  YY.Y \\
        --symmetry cubic
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np


# Conversion factors
RY_TO_EV  = 13.605693122994
RY_PER_BOHR3_TO_GPA = 14710.50498  # 1 Ry/Bohr^3 → GPa
EV_PER_A3_TO_GPA = 160.21766208    # 1 eV/Å^3 → GPa


def parse_total_energy_ry(path: Path) -> float:
    """Parse last '!    total energy = ... Ry' line from QE pw.x output."""
    txt = path.read_text()
    matches = re.findall(r"!.*total energy\s+=\s+(-?\d+\.\d+)\s+Ry", txt)
    if not matches:
        raise ValueError(f"{path}: no total energy line found")
    return float(matches[-1])


def parse_volume_A3(path: Path) -> float:
    """Parse the equilibrium cell volume (Å³) from QE output (relax or scf)."""
    txt = path.read_text()
    m = re.findall(r"unit-cell volume\s+=\s+([\d.]+)\s+\(a\.u\.\)\^3", txt)
    if m:
        bohr3 = float(m[-1])
        return bohr3 * (0.5291772) ** 3
    raise ValueError(f"{path}: no unit-cell volume line found")


def voigt_constants_from_pairs(work: Path, E0_eV: float, V0_A3: float, h: float):
    """Return dict of 6 diagonal Voigt Cij (GPa)."""
    labels = ["11", "22", "33", "23", "13", "12"]
    results = {}
    for i, lbl in enumerate(labels, start=1):
        f_p = work / f"strain_{lbl}_p.out"
        f_m = work / f"strain_{lbl}_m.out"
        if not (f_p.exists() and f_m.exists()):
            print(f"  [skip] strain_{lbl}: missing pair")
            results[f"C{i}{i}"] = None
            continue
        Ep = parse_total_energy_ry(f_p) * RY_TO_EV
        Em = parse_total_energy_ry(f_m) * RY_TO_EV
        d2E = Ep + Em - 2.0 * E0_eV  # eV
        is_shear = (i >= 4)
        denom_strain = (2.0 * h) ** 2 if is_shear else h ** 2  # engineering for shear
        Cii_eV_per_A3 = d2E / (V0_A3 * denom_strain)
        Cii_GPa = Cii_eV_per_A3 * EV_PER_A3_TO_GPA
        results[f"C{i}{i}"] = Cii_GPa
        kind = "shear" if is_shear else "normal"
        print(f"  C{i}{i}  ({kind}, strain {lbl})   "
              f"ΔE = {d2E*1000:+.2f} meV   "
              f"C{i}{i} = {Cii_GPa:.2f} GPa")
    return results


def cubic_vrh(C11: float, C12: float, C44: float):
    """Voigt-Reuss-Hill averaging for cubic Cij (in GPa).
    Returns dict with B_V, B_R, B_VRH, G_V, G_R, G_VRH, E, nu, A (anisotropy).
    """
    # Voigt
    B_V = (C11 + 2.0 * C12) / 3.0
    G_V = (C11 - C12 + 3.0 * C44) / 5.0
    # Reuss
    B_R = (C11 + 2.0 * C12) / 3.0  # same as Voigt for cubic
    diff = C11 - C12
    G_R = 5.0 * diff * C44 / (4.0 * C44 + 3.0 * diff) if (diff > 0 and C44 > 0) else float("nan")
    # Hill
    B = (B_V + B_R) / 2.0
    G = (G_V + G_R) / 2.0
    # Engineering moduli
    E = 9.0 * B * G / (3.0 * B + G)
    nu = (3.0 * B - 2.0 * G) / (2.0 * (3.0 * B + G))
    # Zener anisotropy
    A = 2.0 * C44 / diff if diff > 0 else float("nan")
    return dict(B_V=B_V, B_R=B_R, B_VRH=B, G_V=G_V, G_R=G_R, G_VRH=G,
                E=E, nu=nu, A_zener=A)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True,
                    help="dir containing strain_{11,22,33,23,13,12}_{p,m}.out")
    ap.add_argument("--v0_ry", type=float, default=None,
                    help="equilibrium V0 total energy in Ry (from V0_relax.out)")
    ap.add_argument("--v0_out", default=None,
                    help="path to V0_relax.out (parses both E and volume)")
    ap.add_argument("--v0_A3", type=float, default=None,
                    help="equilibrium V0 cell volume in Å³ "
                         "(if not provided via --v0_out)")
    ap.add_argument("--strain", type=float, default=0.005,
                    help="strain magnitude h used in the SCFs (default 0.005)")
    ap.add_argument("--bulk_GPa", type=float, default=None,
                    help="bulk modulus K from BM EOS (GPa) — needed for "
                         "cubic C12 recovery")
    ap.add_argument("--symmetry", choices=["cubic", "diagonal_only"],
                    default="cubic")
    ap.add_argument("--out", default=None,
                    help="JSON summary path (default: <workdir>/elastic_results.json)")
    args = ap.parse_args()

    work = Path(args.workdir)
    if not work.exists():
        raise SystemExit(f"workdir not found: {work}")

    # Resolve V0 reference
    if args.v0_out:
        v0_path = Path(args.v0_out)
        E0_Ry = parse_total_energy_ry(v0_path)
        V0_A3 = parse_volume_A3(v0_path)
        print(f"V0 reference (from {v0_path}):")
        print(f"  E0 = {E0_Ry:.6f} Ry  = {E0_Ry*RY_TO_EV:.4f} eV")
        print(f"  V0 = {V0_A3:.4f} Å³")
    else:
        if args.v0_ry is None or args.v0_A3 is None:
            raise SystemExit("Must provide --v0_out OR (--v0_ry AND --v0_A3)")
        E0_Ry = args.v0_ry
        V0_A3 = args.v0_A3
        print(f"V0 reference (manual):")
        print(f"  E0 = {E0_Ry:.6f} Ry  = {E0_Ry*RY_TO_EV:.4f} eV")
        print(f"  V0 = {V0_A3:.4f} Å³")

    E0_eV = E0_Ry * RY_TO_EV
    h = args.strain
    print(f"\nStrain magnitude h = {h}")
    print(f"Reading strain SCF pairs from {work}\n")

    # 6 diagonal Voigt constants
    Cij_diag = voigt_constants_from_pairs(work, E0_eV, V0_A3, h)

    # Symmetrize per symmetry choice
    summary = {
        "v0_reference": {"E0_Ry": E0_Ry, "E0_eV": E0_eV, "V0_A3": V0_A3},
        "strain_step": h,
        "voigt_diagonal_GPa": Cij_diag,
    }

    if args.symmetry == "cubic":
        # Sanity check + average
        c_normal = [Cij_diag[k] for k in ("C11", "C22", "C33") if Cij_diag[k] is not None]
        c_shear  = [Cij_diag[k] for k in ("C44", "C55", "C66") if Cij_diag[k] is not None]
        if not c_normal or not c_shear:
            raise SystemExit("Missing normal- or shear-strain pairs for cubic averaging")

        C11_avg = float(np.mean(c_normal))
        C44_avg = float(np.mean(c_shear))
        C11_std = float(np.std(c_normal))
        C44_std = float(np.std(c_shear))
        print(f"\nCubic symmetry averaging:")
        print(f"  C11 ≈ {C11_avg:.2f} ± {C11_std:.2f} GPa  "
              f"(from C11/C22/C33 = {[f'{x:.1f}' for x in c_normal]})")
        print(f"  C44 ≈ {C44_avg:.2f} ± {C44_std:.2f} GPa  "
              f"(from C44/C55/C66 = {[f'{x:.1f}' for x in c_shear]})")

        # C12 from bulk modulus
        if args.bulk_GPa is None:
            print("\n[warn] --bulk_GPa not provided — cannot recover C12 / "
                  "compute VRH moduli. Provide BM-EOS K to complete.")
            summary["cubic"] = {
                "C11_avg_GPa": C11_avg, "C44_avg_GPa": C44_avg,
                "C12_GPa": None,
                "VRH": None,
            }
        else:
            K = args.bulk_GPa
            C12 = (3.0 * K - C11_avg) / 2.0
            print(f"\n  C12 = (3 K − C11) / 2 = (3 × {K:.2f} − {C11_avg:.2f}) / 2 = "
                  f"{C12:.2f} GPa  (BM-EOS K = {K} GPa)")
            vrh = cubic_vrh(C11_avg, C12, C44_avg)
            print(f"\nVRH-averaged engineering moduli (cubic):")
            print(f"  Bulk modulus    B_VRH = {vrh['B_VRH']:.2f} GPa")
            print(f"  Shear modulus   G_VRH = {vrh['G_VRH']:.2f} GPa")
            print(f"  Young's modulus E      = {vrh['E']:.2f} GPa")
            print(f"  Poisson ratio   ν      = {vrh['nu']:.4f}")
            print(f"  Zener anisotropy A     = {vrh['A_zener']:.3f}  (1 = isotropic)")
            summary["cubic"] = {
                "C11_avg_GPa": C11_avg,
                "C11_std_GPa": C11_std,
                "C44_avg_GPa": C44_avg,
                "C44_std_GPa": C44_std,
                "C12_GPa": C12,
                "VRH": vrh,
            }
    else:
        summary["note"] = "diagonal_only mode — VRH/E/nu not computed; provide --symmetry cubic + --bulk_GPa for full output"

    out = Path(args.out) if args.out else work / "elastic_results.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
