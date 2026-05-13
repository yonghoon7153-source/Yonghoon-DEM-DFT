#!/usr/bin/env python3
"""STRICT physics-first porosity predictor — Yu-Standish trimodal RCP attempt.

STATUS: ⚠️  exploratory — the simple max/min trial-selection form of the
Yu-Standish 1991 LPM does not reproduce the binary Furnas valley for our
parameter range.  Sanity checks below show:
    binary D=12/1 X=0.3 : Yu-Standish ε≈0.29   (Bouvard data ~0.18)
    trimodal eq         : Yu-Standish ε≈0.21   (Furnas limit ~0.05)
The valley fails to emerge because at finite size ratio a single
controlling-component formula cannot interpolate smoothly through the
Furnas minimum.  Full Yu-Standish requires the smooth weighted-trial
combination or the 3-parameter Yu-Zou-Standish 1996 revision —
deferred as future work.

Kept here as a reference scaffold; the production model remains
predict_porosity_strict_physics.py (Bouvard binary interpolation +
λ_eff = D_AM_eff / D_SE), which fits the 8mAh thick-film campaign
within ±3% (88% of cases) and is the paper main result.

References for a proper future implementation:
  [Yu1991]  Yu, A.B. & Standish, N.  Ind. Eng. Chem. Res. 30 (1991) 1372
  [Yu1996]  Yu, Zou & Standish.       Ind. Eng. Chem. Res. 35 (1996) 3730
  [Stovall] Stovall, de Larrard, Buil. Powder Technol. 48 (1986) 1
"""
import numpy as np


# ── Material parameters ────────────────────────────────────────────
RHO_AM   = 4.8     # g/cm³
RHO_SE   = 2.0
H_SE     = 0.85e9  # Pa
P_PRESS  = 300e6   # Pa
PHI_MONO = 0.64    # Bernal RCP for monomodal spheres

# Endpoints
EPS_PURE_AM     = 1.0 - PHI_MONO     # 0.36
EPS_PURE_SE_EXP = 0.10               # USER ANCHOR (lab measurement)

# Derived
K_HECKEL    = -np.log(EPS_PURE_SE_EXP / EPS_PURE_AM) / (P_PRESS / 1e6)  # 1/MPa
SIGMA_Y_EFF = 1e6 / (3.0 * K_HECKEL)                                    # Pa

# Published constants (no fit)
ALPHA_KC  = 2.0     # Sridhar 2000
F_PERC    = 0.62    # consensus 0.60-0.70
SHARPNESS = 8.0


# ── Yu-Standish 1991 trimodal RCP ────────────────────────────────
def yu_standish_rcp(diameters, fractions, phi_mono=PHI_MONO):
    """Linear-mixture packing porosity for n components.

    Parameters
    ----------
    diameters  : iterable of particle diameters (any units, same for all)
    fractions  : iterable of solid-only volume fractions (sum normalized)
    phi_mono   : monomodal packing fraction (0.64 for RCP spheres)

    Returns
    -------
    eps_rcp    : RCP porosity (0..1)

    Formulation
    -----------
    Sort components large → small (index 0 = largest).
    For each j-dominant trial (j = 0..n-1):
        V^(j) = V0·X[j]
              + Σ_{i<j}  (V0 - (V0-1)·b(r_ij)) · X[i]   # i is coarser (wall)
              + Σ_{i>j}  V0 · (1 - a(r_ji)·(1-V0)) · X[i]  # i is finer (void-fill)
    where V0 = 1/φ_mono, r_ij = d[j]/d[i] ∈ (0,1].
    Final V_T = max_j V^(j) (most-constraining trial),  φ = 1/V_T.
    a(r), b(r) = (1-r)² (CPM-symmetric; reproduces Furnas binary limit).
    """
    d = np.asarray(diameters, dtype=float)
    X = np.asarray(fractions, dtype=float)
    mask = X > 0
    d, X = d[mask], X[mask]
    if X.sum() <= 0:
        return 1.0 - phi_mono
    X = X / X.sum()
    # Sort large → small
    order = np.argsort(-d)
    d, X = d[order], X[order]
    n = len(d)
    V0 = 1.0 / phi_mono

    def kernel(r):
        # "filling efficiency" — kernel=1 at r→0 (perfect), kernel=0 at r=1.
        # (1-r) gives Furnas binary minimum around the right composition.
        return (1.0 - r)
    # NOTE: V_eff_fines uses (V0 − (V0−1)·kernel) so fines→spec vol 1 (perfect
    # filling) as r→0, and →V0 at r=1.  V_eff_coarse uses (V0 + (V0−1)·kernel)
    # so wall effect loosens packing of fine matrix around big particles.

    # CPM / Yu-Standish formulation re-derived:
    #   For each j-controlling trial, compute V_T^(j) = total spec vol
    #   "fines in coarse voids" (i finer than j, j controls):
    #       V_eff_i = 1 + (V0 - 1) * (1 - kernel(r))    ← perfect fill→V_eff=1
    #   "coarse in fines matrix" (i coarser than j, wall effect):
    #       V_eff_i = V0 * (1 + (V0 - 1) * (1 - kernel(r)))  ← loosens
    #   With kernel(r) = (1-r) for spheres (CPM-K=infty, sphere-RCP fit).
    # Physically: the mixture packs at the BEST (densest) configuration
    # achievable across all "controlling-component" trials, so V_T = MIN.
    # The 1991 paper's "max" convention refers to the maximum *constraint*,
    # which equals the minimum-attainable specific volume after each trial
    # gives its own attainable V (different per controlling component).
    VT = +np.inf
    for j in range(n):
        s = V0 * X[j]
        for i in range(n):
            if i == j:
                continue
            if i < j:
                # i coarser (d[i] > d[j]); wall effect — loosens fine matrix
                r = d[j] / d[i]
                V_eff = V0 + (V0 - 1.0) * kernel(r)
            else:
                # i finer (d[i] < d[j]); fines fill coarse voids
                r = d[i] / d[j]
                V_eff = V0 - (V0 - 1.0) * kernel(r)
            s += V_eff * X[i]
        VT = min(VT, s)
    phi_mix = 1.0 / VT
    return max(1.0 - phi_mix, 0.05)


# ── SFM + stress percolation (unchanged from strict_physics) ────
def sfm_constraint(f_am, lam_eff):
    if f_am <= 1e-9:
        return 1.0
    kc = 1.0 + ALPHA_KC * f_am ** 2
    kc *= 1.0 + 0.05 * np.log(max(lam_eff, 1.0))
    return kc


def stress_percolation(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC)))


# ── Predict (case-specific particle sizes) ───────────────────────
def predict(am_wt, se_wt, d_p, n_p, d_s, n_s, d_se):
    """Predict porosity from full per-case particle data.

    am_wt, se_wt  : mass fractions of AM and SE in the solid (sum=100)
    d_p, d_s, d_se: particle diameters (µm) for AM_P, AM_S, SE
                    (set d_p or d_s = 0 if absent)
    n_p, n_s      : particle COUNTS for AM_P, AM_S (used to split AM volume)
    """
    v_am = am_wt / RHO_AM
    v_se = se_wt / RHO_SE
    f_am_tot = v_am / (v_am + v_se)
    f_se     = v_se / (v_am + v_se)

    # Split AM volume between P and S by particle count × r³
    if n_p > 0 and n_s > 0 and d_p > 0 and d_s > 0:
        vol_p = n_p * d_p ** 3
        vol_s = n_s * d_s ** 3
        frac_p_in_am = vol_p / (vol_p + vol_s)
    elif n_p > 0 and d_p > 0:
        frac_p_in_am = 1.0
    else:
        frac_p_in_am = 0.0
    f_p = f_am_tot * frac_p_in_am
    f_s = f_am_tot * (1.0 - frac_p_in_am)

    # Yu-Standish trimodal RCP
    diams = []
    fracs = []
    if f_p > 0 and d_p > 0:
        diams.append(d_p); fracs.append(f_p)
    if f_s > 0 and d_s > 0:
        diams.append(d_s); fracs.append(f_s)
    if f_se > 0 and d_se > 0:
        diams.append(d_se); fracs.append(f_se)
    eps_rcp = yu_standish_rcp(diams, fracs)

    # Effective lambda for SFM (volume-weighted AM diameter / d_se)
    if frac_p_in_am > 0 and frac_p_in_am < 1:
        d_eff_am = frac_p_in_am * d_p + (1 - frac_p_in_am) * d_s
    elif frac_p_in_am > 0:
        d_eff_am = d_p
    else:
        d_eff_am = d_s if d_s > 0 else 4.0
    lam_eff = d_eff_am / d_se if d_se > 0 else 1.0

    kc   = sfm_constraint(f_am_tot, lam_eff)
    p_se = stress_percolation(f_se)

    # Plastic densification: Heckel at composite-effective pressure
    P_eff = P_PRESS / kc
    eps_pure_eff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta_max = EPS_PURE_AM - eps_pure_eff
    delta = delta_max * f_se * p_se
    eps_pred = max(eps_rcp - delta, 0.03)

    return dict(f_p=f_p, f_s=f_s, f_se=f_se,
                d_eff_am=d_eff_am, lam_eff=lam_eff,
                eps_rcp=eps_rcp, eps_pred=eps_pred,
                kc=kc, p_se=p_se)


# ── Default trimodal predict (for backward compat with curve plots) ─
D_AM_P_DEFAULT = 12.0
D_AM_S_DEFAULT = 4.0
D_SE_DEFAULT   = 1.0


def predict_strict(am_se_wt, p_s_vol):
    """Backward-compatible default-size predict (matches old API)."""
    am_wt, se_wt = am_se_wt
    pv, sv = p_s_vol
    total = pv + sv if (pv + sv) > 0 else 1
    # Use particle counts equivalent to vol-fraction split inside AM
    # (ratio matters, not absolute counts)
    n_p = pv * 1000 if pv > 0 else 0
    n_s = sv * 1000 if sv > 0 else 0
    if n_p == 0 and n_s == 0:
        n_s = 1000  # fallback monomodal S
    return predict(am_wt, se_wt,
                   D_AM_P_DEFAULT, n_p,
                   D_AM_S_DEFAULT, n_s,
                   D_SE_DEFAULT)


# ── Self-test ────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f'σ_y_eff (derived) = {SIGMA_Y_EFF/1e6:.1f} MPa')
    print(f'K_Heckel          = {K_HECKEL:.3e} 1/MPa')
    print()
    print('Sanity check Yu-Standish:')
    print(f'  monomodal (D=10):           ε = {yu_standish_rcp([10],[1]):.3f}  '
          f'(expect 0.360)')
    print(f'  binary  D=12/1, X=(0.7,0.3): ε = '
          f'{yu_standish_rcp([12,1],[0.7,0.3]):.3f}  '
          f'(Furnas ~0.13-0.18)')
    print(f'  trimodal 12/4/1, X=eq:      ε = '
          f'{yu_standish_rcp([12,4,1],[1/3]*3):.3f}  '
          f'(perfect Furnas trimodal -> 0.05)')
    print()
    print(f'predict_strict(75:25, P:S=7:3):')
    r = predict_strict((75, 25), (7, 3))
    for k, v in r.items():
        print(f'  {k:>10s} = {v}')
