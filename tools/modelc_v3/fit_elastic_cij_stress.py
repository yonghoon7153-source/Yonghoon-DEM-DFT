#!/usr/bin/env python3
"""Full Cij elastic tensor from 12 strain SCFs via stress-strain method.

Each strain SCF (with tstress=.true.) outputs a 6-component Voigt stress
tensor under the applied strain ε_k. By linear elasticity σ_i = Σ_j C_ij ε_j,
so one strain experiment yields ONE COLUMN of the Cij matrix:

    C_:k = ( σ(+h) − σ(−h) ) / (2 h)

12 SCFs (6 strain types × ±h) → full 6×6 Cij directly, including the
off-diagonal C12 / C13 / C23 that the energy-curvature method cannot
extract. No external bulk modulus needed.

The resulting Cij is then symmetrized (Cij = (Cij + Cji)/2), VRH-averaged,
and converted to engineering moduli (B, G, E, ν, Zener anisotropy A).

Usage:
    python3 fit_elastic_cij_stress.py \\
        --workdir /home/.../elastic_static \\
        --strain  0.005

QE stress convention parsed:
        total   stress  (Ry/bohr**3)            (kbar)     P=  ...
       σ_xx σ_xy σ_xz             σ_xx_kbar σ_xy_kbar σ_xz_kbar
       σ_yx σ_yy σ_yz             σ_yx_kbar σ_yy_kbar σ_yz_kbar
       σ_zx σ_zy σ_zz             σ_zx_kbar σ_zy_kbar σ_zz_kbar

Voigt:  σ1=σxx, σ2=σyy, σ3=σzz, σ4=σyz, σ5=σxz, σ6=σxy   (sign as printed)
Strain convention: tensor ε_ij applied with magnitude h; for shear
components (k=4,5,6) engineering γ_k = 2·ε_ij, so the denominator is 2·h
(NOT 4·h) when using tensor strain — see notes.
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np


KBAR_TO_GPA = 0.1
RY_TO_EV = 13.605693122994


def parse_stress_kbar(path: Path) -> np.ndarray:
    """Return 3×3 stress matrix (kbar) from the last printout of a QE pwo.

    QE output block:
        total   stress  (Ry/bohr**3)                   (kbar)     P= ...
        σ_xx σ_xy σ_xz             σ_xx σ_xy σ_xz
        σ_yx σ_yy σ_yz             σ_yx σ_yy σ_yz
        σ_zx σ_zy σ_zz             σ_zx σ_zy σ_zz
    """
    txt = path.read_text()
    # Find LAST occurrence
    matches = list(re.finditer(
        r"total\s+stress\s+\(Ry/bohr\*\*3\).*?P=\s*[-+\d.E]+\s*\n"
        r"\s*([-+\d.E\s]+)",
        txt, flags=re.IGNORECASE,
    ))
    if not matches:
        raise ValueError(f"{path}: no 'total stress' block found")
    block = matches[-1].group(1)
    # The 3 lines each have 6 numbers (Ry/bohr^3 × 3, kbar × 3)
    nums = []
    for line in block.strip().splitlines()[:3]:
        parts = line.split()
        nums.append([float(x) for x in parts])
    if not (len(nums) == 3 and all(len(r) == 6 for r in nums)):
        raise ValueError(f"{path}: unexpected stress block shape: {nums}")
    # kbar columns are indices 3,4,5 of each row
    kbar = np.array([[row[3], row[4], row[5]] for row in nums])
    return kbar


def stress_to_voigt(sigma_3x3: np.ndarray) -> np.ndarray:
    """3×3 stress → 6-vector Voigt:  (σxx, σyy, σzz, σyz, σxz, σxy)."""
    return np.array([
        sigma_3x3[0, 0], sigma_3x3[1, 1], sigma_3x3[2, 2],
        sigma_3x3[1, 2], sigma_3x3[0, 2], sigma_3x3[0, 1],
    ])


def vrh_averages(Cij_GPa: np.ndarray):
    """Voigt–Reuss–Hill from full 6×6 elastic matrix (GPa).

    Voigt: B = (C11+C22+C33 + 2(C12+C13+C23)) / 9
           G = (C11+C22+C33 − (C12+C13+C23) + 3(C44+C55+C66)) / 15
    Reuss: same formulas in compliance Sij = Cij^-1.
    Hill = (V + R) / 2.
    """
    C = Cij_GPa
    S = np.linalg.inv(C)
    # Voigt
    B_V = (C[0,0]+C[1,1]+C[2,2] + 2*(C[0,1]+C[0,2]+C[1,2])) / 9.0
    G_V = ((C[0,0]+C[1,1]+C[2,2]) - (C[0,1]+C[0,2]+C[1,2])
           + 3*(C[3,3]+C[4,4]+C[5,5])) / 15.0
    # Reuss
    B_R = 1.0 / (S[0,0]+S[1,1]+S[2,2] + 2*(S[0,1]+S[0,2]+S[1,2]))
    G_R = 15.0 / (4*(S[0,0]+S[1,1]+S[2,2]) - 4*(S[0,1]+S[0,2]+S[1,2])
                  + 3*(S[3,3]+S[4,4]+S[5,5]))
    # Hill
    B = (B_V + B_R) / 2.0
    G = (G_V + G_R) / 2.0
    # Engineering
    E = 9.0 * B * G / (3.0 * B + G)
    nu = (3.0 * B - 2.0 * G) / (2.0 * (3.0 * B + G))
    # Cubic Zener anisotropy (only meaningful if cubic)
    A_zener = 2.0 * C[3,3] / (C[0,0] - C[0,1]) if (C[0,0] - C[0,1]) > 0 else float("nan")
    return dict(B_V=B_V, B_R=B_R, B_VRH=B,
                G_V=G_V, G_R=G_R, G_VRH=G,
                E=E, nu=nu, A_zener=A_zener)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--strain", type=float, default=0.005,
                    help="strain magnitude h (tensor) applied in the SCFs")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no_symmetrize", action="store_true",
                    help="report raw Cij (no Cij ↔ Cji averaging)")
    ap.add_argument("--no_qe_sign_flip", action="store_true",
                    help="disable the QE stress sign convention flip. "
                         "QE prints σ_ij = -(1/V) ∂E/∂ε_ij so for stable "
                         "material with positive Cij, σ(+ε) < 0 → raw "
                         "(σ(+h)-σ(-h))/(2h) is NEGATIVE of Cij. Default: flip.")
    args = ap.parse_args()

    work = Path(args.workdir)
    if not work.exists():
        raise SystemExit(f"workdir not found: {work}")
    h = args.strain

    # Map: strain label "ij" → which Voigt column k (1..6) it represents
    # 11→1, 22→2, 33→3, 23→4 (shear), 13→5 (shear), 12→6 (shear)
    voigt_index_of = {"11": 0, "22": 1, "33": 2, "23": 3, "13": 4, "12": 5}

    Cij = np.full((6, 6), np.nan)

    print(f"Parsing 12 strain SCFs from {work}")
    print(f"strain magnitude h = {h} (tensor, ε_ij)\n")

    for lbl, k in voigt_index_of.items():
        f_p = work / f"strain_{lbl}_p.out"
        f_m = work / f"strain_{lbl}_m.out"
        if not (f_p.exists() and f_m.exists()):
            print(f"  [skip] strain_{lbl}: missing {f_p.name} or {f_m.name}")
            continue
        sigma_p_3x3 = parse_stress_kbar(f_p)
        sigma_m_3x3 = parse_stress_kbar(f_m)
        sigma_p = stress_to_voigt(sigma_p_3x3)
        sigma_m = stress_to_voigt(sigma_m_3x3)

        # For tensor strain applied as ε_ij = ±h, the corresponding Voigt
        # strain ε_k = h for k = 1,2,3 (normal) and γ_k = 2h for k = 4,5,6
        # (engineering shear). C_:k from σ-strain linear relation:
        is_shear = (k >= 3)
        strain_voigt = 2.0 * h if is_shear else h
        # ΔC_:k = (σ(+) - σ(-)) / (2 * applied_voigt_strain)
        col = (sigma_p - sigma_m) / (2.0 * strain_voigt)
        # QE stress convention σ_ij = -(1/V) ∂E/∂ε_ij ⇒ flip sign to get
        # physical Cij (positive for stable material). See db/properties/
        # elastic.json: "QE sign flip" is standard for finite-strain Cij.
        if not args.no_qe_sign_flip:
            col = -col
        # kbar → GPa
        col_GPa = col * KBAR_TO_GPA
        Cij[:, k] = col_GPa
        print(f"  C_:{k+1} (strain {lbl}, {'shear' if is_shear else 'normal'}): "
              f"{['{:+.2f}'.format(c) for c in col_GPa]} GPa")

    # Symmetrize unless told not to
    if not args.no_symmetrize:
        Cij = 0.5 * (Cij + Cij.T)
        print("\n[symmetrized] Cij ← (Cij + Cji) / 2\n")

    # Print full 6×6
    print("Full 6×6 elastic matrix Cij (GPa):")
    print("        " + "  ".join(f"j={j+1:>5}" for j in range(6)))
    for i in range(6):
        row = "  ".join(f"{Cij[i,j]:7.2f}" for j in range(6))
        print(f"  i={i+1:<3}  {row}")

    # Sanity: report cubic-symmetric quantities
    print()
    if not np.any(np.isnan([Cij[0,0], Cij[1,1], Cij[2,2]])):
        c_norm = [Cij[0,0], Cij[1,1], Cij[2,2]]
        print(f"  C11/C22/C33 = {c_norm[0]:.2f}, {c_norm[1]:.2f}, {c_norm[2]:.2f}  "
              f"→ avg {np.mean(c_norm):.2f}, σ {np.std(c_norm):.2f}")
    if not np.any(np.isnan([Cij[3,3], Cij[4,4], Cij[5,5]])):
        c_shear = [Cij[3,3], Cij[4,4], Cij[5,5]]
        print(f"  C44/C55/C66 = {c_shear[0]:.2f}, {c_shear[1]:.2f}, {c_shear[2]:.2f}  "
              f"→ avg {np.mean(c_shear):.2f}, σ {np.std(c_shear):.2f}")
    if not np.any(np.isnan([Cij[0,1], Cij[0,2], Cij[1,2]])):
        c_off = [Cij[0,1], Cij[0,2], Cij[1,2]]
        print(f"  C12/C13/C23 = {c_off[0]:.2f}, {c_off[1]:.2f}, {c_off[2]:.2f}  "
              f"→ avg {np.mean(c_off):.2f}, σ {np.std(c_off):.2f}")

    # VRH only meaningful if Cij is positive-definite
    eigs = np.linalg.eigvalsh(Cij)
    print(f"\n  eigenvalues of Cij: {[f'{e:.2f}' for e in eigs]} GPa  "
          f"(all > 0 ⇒ mechanically stable)")

    if np.any(np.isnan(Cij)):
        print("\n[warn] Some Cij entries are NaN — full VRH not computed.")
        vrh = None
    else:
        vrh = vrh_averages(Cij)
        print(f"\n=== VRH-averaged engineering moduli ===")
        print(f"  Bulk    Voigt {vrh['B_V']:7.2f}  Reuss {vrh['B_R']:7.2f}  VRH {vrh['B_VRH']:7.2f}  GPa")
        print(f"  Shear   Voigt {vrh['G_V']:7.2f}  Reuss {vrh['G_R']:7.2f}  VRH {vrh['G_VRH']:7.2f}  GPa")
        print(f"  Young's E       = {vrh['E']:.2f} GPa")
        print(f"  Poisson ν       = {vrh['nu']:.4f}")
        print(f"  Zener A         = {vrh['A_zener']:.3f}  (cubic only; 1 = isotropic)")

    out = Path(args.out) if args.out else work / "elastic_results_stress.json"
    summary = {
        "method": "stress-strain (full Cij, 12 SCFs)",
        "strain_step": h,
        "Cij_GPa": Cij.tolist(),
        "VRH": vrh,
    }
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
