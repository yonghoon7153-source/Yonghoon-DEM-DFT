#!/usr/bin/env python3
"""se_material — the single source of truth for the solid-electrolyte (LPSCl) material
constants **on the PRODUCTION transport path**, and for their TEMPERATURE convention.

★ SCOPE — read this before trusting the phrase "single source of truth" ★
─────────────────────────────────────────────────────────────────────────
TRUE for the production σ path, and ONLY that path:
    network_conductivity.py · step3_sigma.py · voxel_conductivity.py ·
    mpm_webapp_payload.py · generate_comparison_plots.SE_SG (the LOOCV-0.975 σ_ionic
    scaling law) · webapp/predictor_engine.py · webapp/app.py · webapp templates
    (via the `sigma_grain()` Jinja global)

NOT YET TRUE repo-wide.  ~10 offline analysis / one-shot fitting scripts still carry a
bare 3.0 (physics_surface_contact_fit.py, triage_cases.py, verify_case.py,
build_tau_regime_db.py, export_comsol_2d.py, fit_constrained.py,
screening_ionic_thin_focus.py, analyze_network_results.py, the v-series fit scripts, and
some plot-local SIGMA_BULK constants inside generate_comparison_plots.py).  The current
inventory lives in docs/temp_pressure_capability.md §9-2.

⇒ CONSEQUENCE: push a temperature-enabled run's output through one of those scripts and
σ_grain silently reverts to 25 °C, so τ / σ_brug come out wrong.  Read temperature-swept
results on the production path only.  This header used to claim repo-wide truth flatly;
it is scoped now because the overclaim is itself the kind of silent-wrongness this module
exists to prevent (2026-07-28).

Why this module exists
──────────────────────
σ_grain = 3.0 mS/cm was duplicated as a bare literal across ≳12 files.  None of them
carried a temperature, and none of them referenced each other — so "add T-dependence"
could not be a one-line edit anywhere.  See docs/temp_pressure_capability.md §3-4 / T1-b.

★ CONVENTION (FIXED — do not use any other form) ★
────────────────────────────────────────────────
    σ(T)·T = σ₀ · exp(−Eₐ / (k_B·T))            [Kraft 2017, eq 5]

    ⇒  σ(T) / σ(T_ref) = (T_ref / T) · exp[ −(Eₐ/k_B) · (1/T − 1/T_ref) ]

The competing "σ form" (no 1/T prefactor, σ = σ₀·exp(−Eₐ/k_BT)) gives a 30→60 °C
multiplier that differs by ~10 % (×4.11 vs ×3.74 at Eₐ=0.41, T_ref=30 °C).  Because
that difference is the same order as the Eₐ-band spread we care about, the convention
MUST be pinned.  This module implements ONLY the σ·T (Kraft) form.

★ T_ref = 25 °C is OUR CONVENTION DECISION, NOT AN ANCHOR ★
───────────────────────────────────────────────────────────
σ_grain = 3.0 mS/cm comes from Cronau 2021/2022 (Li6PS5Cl single-crystal), whose data
are ALL room-temperature-single-point with NO Arrhenius analysis — i.e. "what °C is
3.0 mS/cm?" is genuinely UNDEFINED in the source.  We therefore DECLARE T_ref = 25 °C
and re-state 3.0 mS/cm as the prefactor under that convention.  The supporting (not
proving) datum is Minnmann 2021 (LPSCl bulk 1.6 mS/cm @ 25 °C, 380 MPa fabrication) —
one of the rare cards that states temperature AND pressure together.  If a future card
pins Cronau's actual measurement temperature, T_REF_C changes and every σ moves with it.

★ Eₐ IS A BAND — SINGLE-VALUE USE IS FORBIDDEN ★
────────────────────────────────────────────────
    0.29 eV  Ma 2024                     (low edge)
    0.41 eV  Reisacher 2023  ← DEFAULT   STATED, 375 MPa cold-pressed = our 300 MPa regime
    0.46 eV  Kraft 2017                  (high edge)
The band is 1.8× wide in Eₐ, which is ×2.47 vs ×4.44 at 30→60 °C.  ANY temperature
conclusion drawn from this module must be reported as a BAND (run all three), never as
a single number.  `EA_ION_EV_BAND` exists so callers can sweep it mechanically.

★ WHERE the T-dependence physically lives (deliberate approximation) ★
kim2025 shows the σ_ion temperature dependence is mostly the GRAIN-BOUNDARY share
(R_i,gb 25.6→3.1 vs R_i,bulk 9.3→6.0 Ω·cm², 30→60 °C), so the "correct" home is the
Cronau(r_SE) GB factor, not the grain prefactor.  But σ_grain × Cronau(r_SE) is a
PRODUCT, so a single global scalar gives an identical result wherever it is multiplied
in.  We therefore multiply the prefactor (simple) and defer r_SE-dependent Eₐ to T2-b.

★ DEFAULT = OFF ★
`T_C=None` ⇒ the functions return the bare 25 °C literals, bitwise.  Nothing in the
pipeline changes unless a caller explicitly passes a temperature.

Selftest:  python3 scripts/se_material.py --selftest
"""

import math

# ── LPSCl (Li6PS5Cl) argyrodite grain-interior ionic conductivity ──────────────
# Cronau 2021/2022 single-crystal σ_grain.  NOT the pellet value (pellet includes GB
# + porosity; e.g. Bazzoun 2026 pellet 1.02 mS/cm).  Declared at T_REF_C (see header).
SIGMA_GRAIN_MS_CM_25C = 3.0        # mS/cm
SIGMA_GRAIN_S_CM_25C = 3.0e-3      # S/cm  (same number, the unit the solvers use)

# ── Temperature convention ────────────────────────────────────────────────────
T_REF_C = 25.0                     # ★ OUR CONVENTION (not an anchor) — see header
K_B_EV_PER_K = 8.617333262e-5      # eV/K (CODATA 2018)
ABS_ZERO_C = -273.15

# ── Ionic activation energy band (eV) — NEVER cite a single value ─────────────
EA_ION_EV_DEFAULT = 0.41           # Reisacher 2023, STATED, 375 MPa cold-press
EA_ION_EV_BAND = {
    'ma2024':        0.29,         # low edge
    'reisacher2023': 0.41,         # DEFAULT — pressure regime matches ours
    'kraft2017':     0.46,         # high edge (Eₐ itself is figure-read)
}
EA_ION_EV_MIN = 0.29
EA_ION_EV_MAX = 0.46

# ── σ_e (electronic) temperature policy ───────────────────────────────────────
# Reisacher 2023 qualitative finding: in the OHMIC regime the electronic response is
# T-INDEPENDENT (CM-4: 33.50 Ω @25 °C vs 43.89 Ω @65 °C — uncorrelated; CM-3 even has
# the opposite sign).  There is NO quantitative σ_e(T) anchor (§F1).  The pipeline
# solvers (network_conductivity / step3_sigma) already leave σ_e T-independent, so
# "no Arrhenius on σ_e" is BOTH the literature-consistent AND the solver-consistent
# choice.  This constant exists so the (previously divergent) predictor surrogate can
# name the same policy instead of inventing an Eₐ.
SIGMA_E_T_DEPENDENCE = 'NOT_MODELLED'   # literature-consistent (Reisacher, qualitative)

_CONVENTION = 'sigma*T = sigma0*exp(-Ea/(kB*T))  [Kraft 2017 eq 5]'


def c_to_k(t_c):
    """°C → K."""
    return float(t_c) - ABS_ZERO_C


def arrhenius_sigma_factor(T_C, ea_ev=None, T_ref_C=None):
    """σ(T)/σ(T_ref) under the σ·T (Kraft 2017 eq 5) convention.

    Returns EXACTLY 1.0 when T_C is None (feature off) or T_C == T_ref
    (1/T − 1/T_ref is exactly 0.0 and T_ref/T is exactly 1.0 in IEEE-754).
    """
    if T_C is None:
        return 1.0
    ea = EA_ION_EV_DEFAULT if ea_ev is None else float(ea_ev)
    t_ref = T_REF_C if T_ref_C is None else float(T_ref_C)
    T = c_to_k(T_C)
    Tr = c_to_k(t_ref)
    if T <= 0.0 or Tr <= 0.0:
        raise ValueError(f'temperature must be above absolute zero (got {T_C} °C / ref {t_ref} °C)')
    return (Tr / T) * math.exp(-(ea / K_B_EV_PER_K) * (1.0 / T - 1.0 / Tr))


def sigma_grain_mS_cm(T_C=None, ea_ev=None, T_ref_C=None):
    """LPSCl grain σ_ion in mS/cm.

    T_C is None  → returns the bare literal 3.0 (bitwise identical to the historical
                   hard-coded value; T_dependence = NOT_MODELLED).
    T_C given    → 3.0 × arrhenius_sigma_factor(T_C, ea_ev)  (T_dependence = ARRHENIUS).
    """
    if T_C is None:
        return SIGMA_GRAIN_MS_CM_25C
    return SIGMA_GRAIN_MS_CM_25C * arrhenius_sigma_factor(T_C, ea_ev, T_ref_C)


def sigma_grain_S_cm(T_C=None, ea_ev=None, T_ref_C=None):
    """LPSCl grain σ_ion in S/cm (the unit the Kirchhoff / voxel solvers take).

    T_C is None → returns the bare literal 3.0e-3, bitwise.
    """
    if T_C is None:
        return SIGMA_GRAIN_S_CM_25C
    return SIGMA_GRAIN_S_CM_25C * arrhenius_sigma_factor(T_C, ea_ev, T_ref_C)


def scale_sigma_ion(sigma_at_ref, T_C=None, ea_ev=None, T_ref_C=None):
    """Apply the Arrhenius factor to an ARBITRARY caller-supplied σ_ion that is
    declared to be a T_ref value (e.g. a --sigma-ion-se override).  T_C None → the
    input is returned unchanged (identity, bitwise)."""
    if T_C is None:
        return sigma_at_ref
    return sigma_at_ref * arrhenius_sigma_factor(T_C, ea_ev, T_ref_C)


def provenance(T_C=None, ea_ev=None, T_ref_C=None, sigma_e_modelled=False):
    """Provenance block to stamp into every σ-emitting JSON / npz meta.

    Downstream MUST be able to answer "what temperature convention produced this σ?"
    without reading the code.  Keys are stable; add, never rename.
    """
    t_ref = T_REF_C if T_ref_C is None else float(T_ref_C)
    on = T_C is not None
    return {
        'T_C': (None if not on else float(T_C)),
        'T_ref_C': t_ref,
        'Ea_ion_eV': (None if not on else (EA_ION_EV_DEFAULT if ea_ev is None else float(ea_ev))),
        'T_dependence': ('ARRHENIUS' if on else 'NOT_MODELLED'),
        'sigma_ion_T_factor': (1.0 if not on else arrhenius_sigma_factor(T_C, ea_ev, t_ref)),
        'sigma_e_T_dependence': ('ARRHENIUS' if sigma_e_modelled else SIGMA_E_T_DEPENDENCE),
        'convention': _CONVENTION,
        'Ea_band_eV': dict(EA_ION_EV_BAND),
        'trust': (
            'T_ref=25 °C is OUR CONVENTION, not an anchor — Cronau σ_grain=3.0 mS/cm is a '
            'single RT point with no Arrhenius (docs/temp_pressure_capability.md T1-b). '
            'Ea is a BAND 0.29-0.46 eV (1.8x wide = x2.47..x4.44 at 30->60 °C); single-value '
            'reporting is forbidden — sweep EA_ION_EV_BAND. '
            + ('T_dependence=NOT_MODELLED: sigma is the 25 °C value; a run at any other cell '
               'temperature UNDER-states sigma_ion (and over-states the ionic ohmic drop).'
               if not on else
               'sigma_ion only: i0 / D_s / OCP dU/dT / SE hardness carry NO Arrhenius (no anchor, '
               'F1) — a T-swept run is NOT a full-physics temperature sweep.')
        ),
    }


def temperature_argparse(ap):
    """Attach the standard `--temp-c` / `--ea-ion-ev` pair to an argparse parser.
    Defaults are None / None so an unset run is bitwise unchanged."""
    ap.add_argument('--temp-c', type=float, default=None,
                    help='operating temperature in °C.  DEFAULT None = sigma stays at the '
                         f'{T_REF_C:.0f} °C convention value (bitwise-unchanged legacy behaviour).  '
                         'When set, sigma_ion is scaled by the Kraft-2017 sigma*T Arrhenius law '
                         f'(T_ref={T_REF_C:.0f} °C).  sigma_e/kappa/i0/D_s stay T-independent '
                         '(no anchor, F1) — this is NOT a full-physics temperature sweep.')
    ap.add_argument('--ea-ion-ev', type=float, default=None,
                    help=f'ionic activation energy in eV (default {EA_ION_EV_DEFAULT} = Reisacher 2023, '
                         'STATED, 375 MPa cold-press).  ★ SINGLE-VALUE USE IS FORBIDDEN — the band is '
                         '0.29 (Ma 2024) / 0.41 / 0.46 (Kraft 2017); always report the sweep.')
    return ap


def warn_band(T_C=None, ea_ev=None, printer=print):
    """One-line stderr/stdout notice so a T-swept run can never look like a full sweep."""
    if T_C is None:
        return
    ea = EA_ION_EV_DEFAULT if ea_ev is None else float(ea_ev)
    f = arrhenius_sigma_factor(T_C, ea)
    lo = arrhenius_sigma_factor(T_C, EA_ION_EV_MIN)
    hi = arrhenius_sigma_factor(T_C, EA_ION_EV_MAX)
    printer(f'  [T] sigma_ion x{f:.3f} @ {T_C:.1f} °C  (Ea={ea:.2f} eV, T_ref={T_REF_C:.0f} °C, '
            f'sigma*T Kraft2017)   Ea-band x{lo:.3f}..x{hi:.3f} — REPORT THE BAND')
    printer('  [T] ⚠ sigma_ion ONLY.  i0 / D_s / OCP dU/dT / SE hardness carry no Arrhenius '
            '(no anchor, F1) → not a full-physics temperature sweep.')


# ──────────────────────────────────────────────────────────────────────────────
def _selftest():
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    # 1. default OFF is bitwise identical to the historical literals
    chk('T=None → sigma_grain_mS_cm is bitwise 3.0',
        sigma_grain_mS_cm().hex() == (3.0).hex(), sigma_grain_mS_cm().hex())
    chk('T=None → sigma_grain_S_cm is bitwise 3.0e-3',
        sigma_grain_S_cm().hex() == (3.0e-3).hex(), sigma_grain_S_cm().hex())
    chk('T=None → factor is exactly 1.0', arrhenius_sigma_factor(None) == 1.0)
    chk('T=None → scale_sigma_ion is the identity',
        scale_sigma_ion(0.003).hex() == (0.003).hex())

    # 2. at T_ref the factor is exactly 1 and sigma is bitwise 3.0
    chk('T=25 °C → factor exactly 1.0', arrhenius_sigma_factor(25.0) == 1.0)
    chk('T=25 °C → sigma_grain_mS_cm bitwise 3.0',
        sigma_grain_mS_cm(25.0).hex() == (3.0).hex())

    # 3. multipliers match docs/temp_pressure_capability.md §6-A T1-b table
    #    (sigma*T form, T_ref = 25 °C, Ea = 0.41): 30 °C x1.28, 45 °C x2.56, 60 °C x4.79
    for t_c, want in ((30.0, 1.28), (45.0, 2.56), (60.0, 4.79)):
        got = arrhenius_sigma_factor(t_c)
        chk(f'T_ref=25, Ea=0.41 → {t_c:.0f} °C x{want}', abs(round(got, 2) - want) < 5e-3,
            f'got x{got:.4f}')
    #    cross-check the T_ref = 30 °C rows of the same table (0.41: 45 x2.00 / 60 x3.74;
    #    0.29: 45 x1.61 / 60 x2.47; 0.46: 45 x2.19 / 60 x4.44)
    for ea, t_c, want in ((0.41, 45.0, 2.00), (0.41, 60.0, 3.74),
                          (0.29, 45.0, 1.61), (0.29, 60.0, 2.47),
                          (0.46, 45.0, 2.19), (0.46, 60.0, 4.44)):
        got = arrhenius_sigma_factor(t_c, ea, T_ref_C=30.0)
        chk(f'T_ref=30, Ea={ea} → {t_c:.0f} °C x{want}', abs(round(got, 2) - want) < 5e-3,
            f'got x{got:.4f}')
    #    the FORBIDDEN sigma-form (no 1/T prefactor) must differ by ~10 % — proves the
    #    convention choice is load-bearing, not cosmetic
    sig_form_60 = math.exp(-(0.41 / K_B_EV_PER_K) * (1.0 / c_to_k(60.0) - 1.0 / c_to_k(30.0)))
    chk('sigma-form vs sigma*T differ ~10 % at 30→60 °C',
        abs(round(sig_form_60, 2) - 4.11) < 5e-3 and abs(sig_form_60 / 3.739 - 1.0) > 0.08,
        f'sigma-form x{sig_form_60:.3f} vs sigma*T x3.739')

    # 4. band is exposed and ordered
    chk('Ea band exposed 0.29/0.41/0.46',
        sorted(EA_ION_EV_BAND.values()) == [0.29, 0.41, 0.46])
    chk('band factors are monotone in Ea @60 °C',
        arrhenius_sigma_factor(60.0, 0.29) < arrhenius_sigma_factor(60.0, 0.41)
        < arrhenius_sigma_factor(60.0, 0.46))

    # 5. provenance contract
    p_off = provenance()
    chk('provenance OFF: T_C None, Ea None, NOT_MODELLED',
        p_off['T_C'] is None and p_off['Ea_ion_eV'] is None
        and p_off['T_dependence'] == 'NOT_MODELLED' and p_off['sigma_ion_T_factor'] == 1.0)
    p_on = provenance(60.0)
    chk('provenance ON: ARRHENIUS + T_ref 25 + Ea 0.41 + factor',
        p_on['T_dependence'] == 'ARRHENIUS' and p_on['T_ref_C'] == 25.0
        and p_on['Ea_ion_eV'] == 0.41 and abs(p_on['sigma_ion_T_factor'] - 4.785) < 1e-3)
    chk('provenance default sigma_e policy = NOT_MODELLED',
        p_off['sigma_e_T_dependence'] == 'NOT_MODELLED'
        and provenance(60.0, sigma_e_modelled=True)['sigma_e_T_dependence'] == 'ARRHENIUS')
    chk('provenance carries the convention string', 'Kraft 2017' in p_off['convention'])

    # 6. guards
    try:
        arrhenius_sigma_factor(-300.0)
        chk('below absolute zero raises', False)
    except ValueError:
        chk('below absolute zero raises', True)

    print('SE_MATERIAL SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    import argparse
    import sys
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true', help='run the convention/bitwise checks')
    ap.add_argument('--show', type=float, default=None, metavar='T_C',
                    help='print sigma_grain + the full Ea band at this temperature (°C)')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    if a.show is not None:
        print(f'T = {a.show:.1f} °C   (T_ref = {T_REF_C:.0f} °C, {_CONVENTION})')
        for nm, ea in sorted(EA_ION_EV_BAND.items(), key=lambda kv: kv[1]):
            print(f'  Ea={ea:.2f} eV [{nm:<14s}]  x{arrhenius_sigma_factor(a.show, ea):.3f}  '
                  f'→ sigma_grain {sigma_grain_mS_cm(a.show, ea):.3f} mS/cm')
        print('  ★ report the BAND, never a single value')
        sys.exit(0)
    ap.print_help()
