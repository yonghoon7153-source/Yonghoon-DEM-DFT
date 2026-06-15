#!/usr/bin/env python3
"""300 K Nernst-Einstein ionic conductivity from the paper-grade Arrhenius fits.

We have D(T) from MLIP-MD (UMA-s-1p1) at 600/800/1000 K and the Arrhenius fit
ln D = ln D0 - Ea/(kB T). This extrapolates D to 300 K and converts to an ionic
conductivity via the Nernst-Einstein (Einstein) relation, Haven ratio H_R = 1:

    sigma_NE = n_Li * z^2 * e^2 * D / (kB * T)        (z = +1 for Li)

n_Li = (# Li in MD cell) / (cell volume). This is the SAME convention used to
produce the stored modelc value (~14 mS/cm), so the two compositions are
directly comparable. Absolute sigma carries MLIP overshoot (~3-5x) and the
H_R=1 inflation (~2x); the RATIO and Ea are the robust quantities.
"""
import numpy as np

# physical constants
kB_eV = 8.617333262e-5      # eV/K
kB_J = 1.380649e-23         # J/K
e = 1.602176634e-19         # C

# --- paper-grade fits (db/properties/li_transport.json) + actual MD cells ---
systems = {
    "LPSCl  (Li6PS5Cl, comp1 4fu natural)": dict(
        Ea=0.2532, D0=4.110e-4,      # arrhenius_fit PAPER_GRADE
        n_Li=24, V_A3=1016.62,       # comp1_v3_4fu_natural MD cell
        D600_ref=3.086e-6),
    "LPSCl1.6 (Li5.4PS4.4Cl1.6, modelc 5fu)": dict(
        Ea=0.2234, D0=5.745e-4,      # CSV fit slope/intercept (reproduces stored 1.014e-7)
        n_Li=27, V_A3=1216.2,        # 5 f.u. cell (n_Li=2.22e22 cm^-3 -> V=1216 A^3)
        D600_ref=7.90e-6),
}

print("=" * 74)
print(" 300 K extrapolation + Nernst-Einstein sigma (H_R = 1, z = +1)")
print("=" * 74)
out = {}
for name, s in systems.items():
    # number density of Li (carriers) in cm^-3
    n = s["n_Li"] / (s["V_A3"] * 1e-24)        # A^3 -> cm^3
    # D extrapolated to 300 K
    D300 = s["D0"] * np.exp(-s["Ea"] / (kB_eV * 300.0))
    # check: reproduce D(600 K) from the fit
    D600 = s["D0"] * np.exp(-s["Ea"] / (kB_eV * 600.0))
    # Nernst-Einstein conductivity (S/cm) at 300 K
    sigma = n * e**2 * D300 / (kB_J * 300.0)
    out[name] = dict(n=n, D300=D300, sigma_mScm=sigma * 1e3)
    print(f"\n  {name}")
    print(f"    n_Li         = {n:.3e} cm^-3   ({s['n_Li']} Li / {s['V_A3']:.1f} A^3)")
    print(f"    fit          : Ea = {s['Ea']:.4f} eV,  D0 = {s['D0']:.3e} cm^2/s")
    print(f"    D(600K) fit  = {D600:.3e} cm^2/s   (ref MD {s['D600_ref']:.2e})")
    print(f"    D(300K) extrap = {D300:.3e} cm^2/s")
    print(f"    sigma_NE(300K) = {sigma*1e3:.2f} mS/cm   ({sigma:.3e} S/cm)")

names = list(out)
r_sig = out[names[1]]["sigma_mScm"] / out[names[0]]["sigma_mScm"]
r_D = out[names[1]]["D300"] / out[names[0]]["D300"]
print("\n" + "-" * 74)
print(f"  RATIO LPSCl1.6 / LPSCl  @300K :  sigma {r_sig:.2f}x   (D {r_D:.2f}x)")
print(f"  (at 600 K the D ratio is {7.90e-6/3.086e-6:.2f}x — gap widens at low T because Ea differs)")
print("-" * 74)
print("\n  experiment (RT): LPSCl ~1-3.2 mS/cm ; LPSCl1.6/Cl-rich ~7-9.9 mS/cm")
print("  NE is right order, ~1.5-2x high: MLIP D-overshoot (~2-5x) + bulk-vs-pellet resistance.")
print("  Haven H_R=1 is the TRACER->charge assumption; real H_R<1 => true intrinsic sigma = sigma_NE/H_R")
print("  is even HIGHER (opposite sign), so H_R does NOT cause the overshoot. Robust: Ea + ratio.")
