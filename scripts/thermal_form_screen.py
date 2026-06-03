#!/usr/bin/env python3
"""σ_thermal form screening — comprehensive variant comparison.

Replaces the old 1-param σ_th = 286·σ_ion^(3/4)·φ²/CN with rigorous
literature-anchored multi-physics form, mirroring σ_ionic T1 and σ_e
Stage 22.5 methodology.

Tests multiple variants:
  • τ choice (ionic / electronic / geometric / harmonic / max)
  • Phase-mixing strategy (multiplicative geometric vs additive parallel)
  • LIVE param count (3 minimal → 8 full)
  • LOCKED endpoint values (Wang 2022 κ_S/κ_P, Ketter 2025 κ_SE)

Reports per-variant LOOCV / R² / median |err| / n/k.

Run:  python3 scripts/thermal_form_screen.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

# ── LOCKED literature constants ──────────────────────────────────────
KAPPA_S = 4.0     # W/(m·K)  NCM811 single-crystal      (Wang 2022 baseline)
KAPPA_P = 3.0     # W/(m·K)  NCM811 polycrystalline      (Wang 2022 + GB reduction)
KAPPA_SE = 0.7    # W/(m·K)  LPSCl                       (Ketter 2025)
WANG_R_REF = 2.0  # µm        Wang formula reference radius
WANG_BETA = 1.5   # Wang phonon-GB scattering exponent (mirrors NCM β=1.5)
CRONAU_R_REF = 1.0  # µm     Cronau sub-µm onset for SE
HOLM_EXP = 0.5    # Holm 1967 constriction


def wang(r_um, particle_type):
    """Wang 2022 + size-dependent phonon GB factor."""
    if particle_type == 'AM_P':
        return 1.0 / (1.0 + (max(r_um, 0.1) / WANG_R_REF) ** WANG_BETA)
    return 1.0  # AM_S single crystal, SE


def cronau_kappa(r_se_um):
    """SE size effect on κ — sub-µm amorphization (mirrors σ_ionic Cronau)."""
    if r_se_um >= 1.0: return 1.0
    if r_se_um >= 0.5: return 0.85
    if r_se_um >= 0.3: return 0.70
    if r_se_um >= 0.1: return 0.55
    return 0.40


# ── corpus loading ────────────────────────────────────────────────────
import generate_comparison_plots as gcp


def _ps_fraction(d):
    """AM_P mass fraction (= p in form)."""
    fn = getattr(gcp, '_ps_fraction', None)
    if fn: return fn(d)
    am_p = d.get('AM_P_mass_pct') or 0
    am_s = d.get('AM_S_mass_pct') or 0
    if am_p + am_s <= 0: return None
    return am_p / (am_p + am_s)


def _r_am_sizes(d):
    """r_AM_S, r_AM_P (µm)."""
    fn = getattr(gcp, '_r_am_sizes', None)
    if fn: return fn(d)
    return d.get('r_AM_S', 2.5), d.get('r_AM_P', 5.5)


def load_thermal_corpus():
    """Load all cases with valid thermal output + required structural metrics."""
    import glob
    rows = []
    skipped = {'no_kappa': 0, 'no_phi': 0, 'no_tau': 0, 'no_area': 0, 'other': 0}
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: skipped['other'] += 1; continue

        kappa = (d.get('thermal_sigma_full_mScm_stage_e') or
                 d.get('thermal_sigma_full_mScm') or 0)
        if not (kappa and kappa > 0):
            skipped['no_kappa'] += 1; continue

        phi_am = d.get('phi_am', 0) or 0
        phi_se = d.get('phi_se', 0) or 0
        if phi_am <= 0 or phi_se <= 0:
            skipped['no_phi'] += 1; continue

        tau_i = (d.get('tortuosity_recommended') or
                 d.get('tortuosity_mean') or 0)
        tau_e = (d.get('tortuosity_electronic_recommended') or
                 d.get('tortuosity_electronic_mean') or 0)
        if tau_i <= 0 or tau_e <= 0:
            skipped['no_tau'] += 1; continue

        A_am_am = d.get('am_am_mean_area', 0) or 0
        A_am_se_t = d.get('area_AM전체_SE_total', 0) or 0
        A_se_se_t = d.get('area_SE_SE_total', 0) or 0
        A_total = A_am_am + A_am_se_t + A_se_se_t
        if A_total <= 0:
            skipped['no_area'] += 1; continue

        p = _ps_fraction(d) or 0
        ras, rap = _r_am_sizes(d)
        ras = ras if (ras and np.isfinite(ras)) else 2.5
        rap = rap if (rap and np.isfinite(rap)) else 5.5
        rse = d.get('r_SE', 0.5) or 0.5
        T = d.get('thickness_um', 100) or 100
        d_AM = 2.0 * ((1-p)*ras + p*rap)

        f_severe = (d.get('frac_severe_force_pct') or 0) / 100
        f_intact = max(1.0 - f_severe, 0.05)

        rows.append({
            'name': nm, 'kappa': kappa,
            'p': p, 'phi_am': phi_am, 'phi_se': phi_se,
            'ras': ras, 'rap': rap, 'rse': rse,
            'A_total': A_total,
            'tau_i': tau_i, 'tau_e': tau_e,
            'T_d': T / max(d_AM, 1.0),
            'f_intact': f_intact,
        })
    return rows, skipped


# ── form variant builders ─────────────────────────────────────────────
def build_X_and_offset(rows, *,
                       tau_choice='geometric',
                       use_phase_mix=True,
                       use_holm=True,
                       use_size_locks=True,
                       extra_cols=('beta_T', 'beta_Fe', 'C_tau')):
    """Build X matrix and log_offset for a thermal form variant.

    LOCKED (in log_offset):
      - mix: (1-p)·log(κ_S) + p·log(κ_P)   (Wang endpoints)
      - WANG: (1-p)·log(WANG_S) + p·log(WANG_P)
      - κ_SE contribution (phase-weighted)
      - Cronau(r_SE) (if size_locks)
      - Holm √A_total (if use_holm)
      - Bruggeman 2-phase (if phase_mix)

    LIVE in X cols (extra_cols):
      - 'beta_T':  log(T/d_AM)
      - 'beta_Fe': log(f_intact)
      - 'C_tau':   constant + ln(τ) + ln²(τ)   (3 cols)
    """
    n = len(rows)
    log_off = np.zeros(n)
    cols = []
    col_labels = []

    for i, r in enumerate(rows):
        p = r['p']
        # AM material endpoints — Wang 2022 LOCKED
        log_mix_AM = ((1-p) * np.log(KAPPA_S * wang(r['ras'], 'AM_S')) +
                      p * np.log(KAPPA_P * wang(r['rap'], 'AM_P')))
        # SE contribution — Ketter LOCKED, weighted by phi_SE in solid
        phi_solid = r['phi_am'] + r['phi_se']
        if phi_solid <= 0: phi_solid = 0.7
        f_SE_solid = r['phi_se'] / phi_solid
        f_AM_solid = r['phi_am'] / phi_solid
        # Multiplicative phase mixing: κ ≈ κ_AM^f_AM · κ_SE^f_SE (geometric mean)
        log_kappa_SE = np.log(KAPPA_SE)
        if use_size_locks:
            log_kappa_SE += np.log(cronau_kappa(r['rse']))

        # Multi-phase term (LOCKED if use_phase_mix)
        if use_phase_mix:
            log_off[i] += f_AM_solid * log_mix_AM + f_SE_solid * log_kappa_SE
        else:
            # AM-only baseline
            log_off[i] += log_mix_AM

        # Bruggeman 2-phase (LOCKED exponent 4 for each, mirror σ_e for AM)
        if use_phase_mix:
            log_off[i] += 4.0 * np.log(max(r['phi_am'], 1e-3)) * f_AM_solid + \
                          1.0 * np.log(max(r['phi_se'], 1e-3)) * f_SE_solid

        # Holm √A_total
        if use_holm:
            log_off[i] += HOLM_EXP * np.log(max(r['A_total'], 1e-12))

    # Build X cols
    if 'beta_T' in extra_cols:
        cols.append([np.log(max(r['T_d'], 0.1)) for r in rows])
        col_labels.append('β_T·log(T/d_AM)')
    if 'beta_Fe' in extra_cols:
        cols.append([np.log(max(r['f_intact'], 0.05)) for r in rows])
        col_labels.append('β_Fe·log(f_intact)')
    if 'C_tau' in extra_cols:
        taus = []
        for r in rows:
            if tau_choice == 'ionic':       t = r['tau_i']
            elif tau_choice == 'electronic': t = r['tau_e']
            elif tau_choice == 'geometric': t = (r['tau_i'] * r['tau_e']) ** 0.5
            elif tau_choice == 'harmonic':  t = 2/(1/r['tau_i'] + 1/r['tau_e'])
            elif tau_choice == 'max':       t = max(r['tau_i'], r['tau_e'])
            else: t = r['tau_i']
            taus.append(max(t, 0.1))
        lt = np.log(taus)
        cols.append(np.ones(n).tolist())   # p_τ (constant)
        cols.append(lt.tolist())            # q_τ
        cols.append((lt**2).tolist())       # r_τ
        col_labels += ['p_τ', 'q_τ·lnτ', 'r_τ·ln²τ']

    if not cols:
        return np.zeros((n, 0)), log_off, []
    X = np.column_stack(cols)
    return X, log_off, col_labels


# ── fit + LOOCV ───────────────────────────────────────────────────────
def fit_loocv(rows, **variant_kwargs):
    """Fit and report LOOCV/R²/median|err| for one variant."""
    log_kappa = np.array([np.log(r['kappa']) for r in rows])
    X, log_off, col_labels = build_X_and_offset(rows, **variant_kwargs)
    n = len(rows)
    k = X.shape[1]

    if k == 0:
        # Pure LOCKED form (no LIVE params)
        pred_log = log_off
        sse_fit = float(np.sum((log_kappa - pred_log)**2))
        ss_tot = float(np.sum((log_kappa - log_kappa.mean())**2))
        r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
        return {'k': 0, 'r2': r2, 'loocv': r2, 'pred': np.exp(pred_log), 'coef': np.array([])}

    y_resid = log_kappa - log_off
    coef, *_ = lstsq(X, y_resid, rcond=None)
    pred_log = X @ coef + log_off
    err_pct = (np.exp(pred_log) - np.array([r['kappa'] for r in rows])) / \
               np.array([r['kappa'] for r in rows]) * 100
    sse_fit = float(np.sum((log_kappa - pred_log)**2))
    ss_tot = float(np.sum((log_kappa - log_kappa.mean())**2))
    r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0

    sse_loo = 0.0
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        try:
            c_loo, *_ = lstsq(X[m], y_resid[m], rcond=None)
            sse_loo += (y_resid[j] - X[j] @ c_loo)**2
        except: pass
    loocv = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    return {'k': k, 'r2': r2, 'loocv': loocv,
            'med_err': float(np.median(np.abs(err_pct))),
            'pred': np.exp(pred_log), 'coef': coef, 'col_labels': col_labels}


# ── main screen ───────────────────────────────────────────────────────
def main():
    rows, skipped = load_thermal_corpus()
    n = len(rows)
    print(f"\nLoaded {n} cases with valid thermal data.")
    print(f"Skipped: {skipped}\n")
    if n < 20:
        print(f"[ABORT] too few cases (n={n}<20)"); return

    # ─── BASELINE: old form σ_th = 286·σ_ion^(3/4)·φ²/CN ─────────────
    print("=" * 100)
    print("  BASELINE (old form): σ_th = 286·σ_ion^(3/4)·φ_AM²/CN_SE")
    print("=" * 100)
    # We don't easily have σ_ion in rows, so skip for now and rely on form variants.

    # ─── Screen variants ─────────────────────────────────────────────
    print()
    print("=" * 100)
    print(f"  σ_thermal form variants (n={n}, LOCKED κ_S={KAPPA_S} κ_P={KAPPA_P} κ_SE={KAPPA_SE})")
    print("=" * 100)
    print(f"  {'Variant':55s} {'k':>3s} {'n/k':>6s} {'R²':>7s} {'LOOCV':>7s} {'med|err|':>9s}")

    variants = [
        # Pure locked baselines (k=0 LIVE)
        ("V0a: Wang+Ketter mix only (no LIVE)",
         dict(tau_choice='ionic', use_phase_mix=True, use_holm=False,
              use_size_locks=False, extra_cols=())),
        ("V0b: +Holm √A_total (no LIVE)",
         dict(tau_choice='ionic', use_phase_mix=True, use_holm=True,
              use_size_locks=False, extra_cols=())),
        ("V0c: +Cronau(r_SE) +Holm (no LIVE)",
         dict(tau_choice='ionic', use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=())),

        # +C(τ) trio (3 LIVE)
        ("V1a: +C(τ_ionic)",
         dict(tau_choice='ionic',     use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('C_tau',))),
        ("V1b: +C(τ_electronic)",
         dict(tau_choice='electronic', use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('C_tau',))),
        ("V1c: +C(τ_geometric)",
         dict(tau_choice='geometric', use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('C_tau',))),
        ("V1d: +C(τ_harmonic)",
         dict(tau_choice='harmonic',  use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('C_tau',))),
        ("V1e: +C(τ_max)",
         dict(tau_choice='max',       use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('C_tau',))),

        # +β_T (best τ) (4 LIVE)
        ("V2: V1[best τ] + β_T",
         dict(tau_choice='geometric', use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('beta_T', 'C_tau'))),

        # +β_T +β_Fe (5 LIVE — likely production)
        ("V3: V2 + β_Fe",
         dict(tau_choice='geometric', use_phase_mix=True, use_holm=True,
              use_size_locks=True, extra_cols=('beta_T', 'beta_Fe', 'C_tau'))),

        # Ablation: drop Cronau lock
        ("V4: V3 - Cronau(r_SE)",
         dict(tau_choice='geometric', use_phase_mix=True, use_holm=True,
              use_size_locks=False, extra_cols=('beta_T', 'beta_Fe', 'C_tau'))),

        # Ablation: drop Holm
        ("V5: V3 - Holm √A",
         dict(tau_choice='geometric', use_phase_mix=True, use_holm=False,
              use_size_locks=True, extra_cols=('beta_T', 'beta_Fe', 'C_tau'))),

        # Ablation: drop phase-mix (AM-only baseline)
        ("V6: V3 - phase mix (AM-only)",
         dict(tau_choice='geometric', use_phase_mix=False, use_holm=True,
              use_size_locks=True, extra_cols=('beta_T', 'beta_Fe', 'C_tau'))),
    ]

    best_loo = -np.inf; best_label = None; best_result = None
    for label, kwargs in variants:
        res = fit_loocv(rows, **kwargs)
        n_over_k = n / max(res['k'], 1) if res['k'] > 0 else float('inf')
        med = res.get('med_err', float('nan'))
        marker = ' ★' if res['loocv'] > best_loo else ''
        if res['loocv'] > best_loo:
            best_loo = res['loocv']; best_label = label; best_result = (res, kwargs)
        print(f"  {label:55s} {res['k']:>3d} {n_over_k:>6.1f} "
              f"{res['r2']:>6.3f} {res['loocv']:>6.3f} {med:>8.1f}%{marker}")

    # ─── BEST variant detail ─────────────────────────────────────────
    print()
    print("=" * 100)
    print(f"  BEST: {best_label}")
    print("=" * 100)
    res, kwargs = best_result
    if 'col_labels' in res:
        for lbl, c in zip(res['col_labels'], res['coef']):
            print(f"    {lbl:25s}  coef = {c:+.4f}")
    print(f"  LOOCV {res['loocv']:.4f}  R² {res['r2']:.4f}  "
          f"med|err| {res.get('med_err', float('nan')):.1f}%  k={res['k']}  n/k={n/max(res['k'],1):.1f}")
    print()


if __name__ == '__main__':
    main()
