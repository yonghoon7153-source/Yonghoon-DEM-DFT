#!/usr/bin/env python3
"""(나) Homogenized cap-plasticity compaction curve — pure-physics Heckel reference.

The companion to the resolved-grain mpm2d_PS_pressure.py.  That script keeps the
Furnas dip but over-densifies (pure-J2 is isochoric → no plastic *volume* change,
so it flows to 0 porosity).  This script instead models a HOMOGENIZED porous REV
with a Drucker-Prager-CAP constitutive law:

  * REAL elastic modulus (E = 24 GPa, LPSCl single-crystal) — NO 18x softening
  * plastic VOLUMETRIC compaction (the physics J2 is missing)
  * density hardening whose cap pressure DIVERGES at a jamming porosity phi_min
    → physical residual porosity (continuum proxy for geometric jamming)

Closed form (above cap onset p_c0):
    phi(P) = phi_min + (phi0 - phi_min) * (p_c0 / P)**(1/b)
  p_c0 is auto-solved so the curve passes EXACTLY through the experimental anchor
  (Doux 2020: 300 MPa -> ~10%).  b and phi_min are the shape knobs to fit the
  rest of the Doux curve (5-15% over 250-400 MPa).

NOTE: 0D / homogenized → no grain sizes → NO Furnas dip (that needs the resolved-
grain script).  This is the clean multi-pressure Heckel reference only, calibrated
to EXPERIMENT independently of DEM (frame #4 compliant — no DEM cross-fit).
"""
import numpy as np

# ---- material (REAL, un-softened) -------------------------------------------
E, NU = 24.0, 0.30                 # GPa  (LPSCl bulk single-crystal)
K = E / (3 * (1 - 2 * NU))         # bulk modulus

# ---- cap-plasticity shape knobs (calibrate to Doux 2020) --------------------
PHI0     = 0.50                    # initial loose porosity (pre-press)
PHI_MIN  = 0.03                    # jamming residual porosity (RCP-like limit)
B_HARD   = 2.5                     # density-hardening exponent (curve steepness)

# ---- experimental anchor (locks p_c0) ---------------------------------------
P_ANCHOR_GPa   = 0.30             # Doux 2020 calibration pressure
PHI_ANCHOR     = 0.10             # ~10% porosity at 300 MPa


def solve_pc0(b=B_HARD, phi_min=PHI_MIN, phi0=PHI0):
    """p_c0 such that phi(P_ANCHOR)=PHI_ANCHOR exactly (anchor-locked)."""
    frac = (PHI_ANCHOR - phi_min) / (phi0 - phi_min)
    return P_ANCHOR_GPa * frac ** b


def porosity(P_GPa, b=B_HARD, phi_min=PHI_MIN, phi0=PHI0):
    P = np.atleast_1d(np.asarray(P_GPa, float))
    pc0 = solve_pc0(b, phi_min, phi0)
    phi = np.empty_like(P)
    elastic = 1 - (1 - phi0) * np.exp(P / K)                    # stiff → tiny
    plastic = phi_min + (phi0 - phi_min) * (pc0 / np.maximum(P, 1e-12)) ** (1.0 / b)
    m = P > pc0
    phi[m] = plastic[m]
    phi[~m] = elastic[~m]
    return phi, pc0


def heckel(P_MPa, phi):
    """Heckel fit ln(1/(1-D)) = K*P + A → P_y = 1/K, sigma_y_eff = P_y/3."""
    D = 1 - np.asarray(phi)
    y = np.log(1.0 / (1.0 - D))
    Kf, Af = np.polyfit(np.asarray(P_MPa, float), y, 1)
    yhat = Kf * np.asarray(P_MPa) + Af
    ss = np.sum((y - y.mean()) ** 2)
    r2 = 1 - np.sum((y - yhat) ** 2) / ss if ss > 0 else float('nan')
    return 1.0 / Kf, (1.0 / Kf) / 3.0, r2


def main():
    Pt = np.array([100, 200, 300, 400, 500, 600], float)        # MPa
    phi, pc0 = porosity(Pt / 1000.0)
    print(f"REAL E={E} GPa, K={K:.1f} GPa  |  phi0={PHI0}  phi_min={PHI_MIN}  "
          f"b={B_HARD}  p_c0={pc0*1000:.1f} MPa (anchor-locked @300→10%)")
    print("  porosity vs pressure:")
    for p, f in zip(Pt, phi):
        print(f"    {int(p):4d} MPa  ->  {f*100:5.1f} %")
    Py, sy, r2 = heckel(Pt, phi)
    print(f"  Heckel: P_y={Py:.0f} MPa  sigma_y_eff={sy:.0f} MPa  R2={r2:.4f}")
    print("  Doux 2020 exp ref: 300→~10%, 250-400 MPa → 5-15%  (independent anchor)")

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        Pf = np.linspace(50, 700, 200)
        pf, _ = porosity(Pf / 1000.0)
        fig, ax = plt.subplots(figsize=(5.2, 4))
        ax.plot(Pf, pf * 100, '-', color='#2e8b57', lw=2, label='cap model (real E=24)')
        ax.scatter(Pt, phi * 100, s=30, color='#2e8b57', zorder=5)
        ax.axhspan(5, 15, xmin=0, xmax=1, color='gray', alpha=0.15,
                   label='Doux 2020 (250-400 MPa)')
        ax.scatter([300], [10], s=120, marker='*', color='crimson',
                   zorder=6, label='anchor 300→10%')
        ax.set_xlabel('pressure (MPa)'); ax.set_ylabel('porosity (%)')
        ax.set_title('Homogenized cap-plasticity Heckel (real E)'); ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
        plt.tight_layout(); plt.savefig('cap_compaction_heckel.png', dpi=120)
        print("  saved cap_compaction_heckel.png")
    except Exception as e:
        print(f"  (plot skipped: {e})")


if __name__ == '__main__':
    main()
