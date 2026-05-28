#!/usr/bin/env python3
"""Deep per-case investigation of the remaining 10 |err|>20% outliers
after C4 adoption.  Goal: identify what's TRULY different about each
outlier (which metric is anomalous), then test candidate corrections.

Two sections:
  PART 1 — PER-CASE ANOMALY DIAGNOSTIC
    For each outlier, find the top 5 numeric metrics with |z|>1.5
    across the corpus.  Also show the closest non-outlier (same
    composition, similar φ) for comparison.

  PART 2 — CANDIDATE TERM TESTS
    Each new term joint with C4's (P2, Δcov).  Reports:
    • LOOCV gain over C4
    • per-outlier err shift (intent: which outlier gets fixed?)
    • Leave-corner-out sign-consistency check

  Candidate terms:
    X.   damping for extreme r_SE/r_AM_P ratio
         (addresses 10:0 r_SE=0.5 high-variance pattern, 4-5 cases)
    Z.   CN<3 marginal-percolation soft turn-off (addresses 6mAh_real_6)
    W.   log(path_hop_area_mean) — Holm constriction explicit
    V.   log(bulk_resistance_fraction) — captures τ_Laplace/τ_Dijkstra ratio
    U.   am_am_cn (AM-AM contact count) — packing geometry of pure AM
    T.   stress_cv — particle stress non-uniformity

Run from the repo root:  python3 scripts/deep_outlier_investigation.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa
from nested_cv_sat import (load_corpus, base_log_sat, cblend_fit, cblend_pred,
                           cronau_factor, production_extras,
                           _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, PHI_C0)


def _load_names_and_metrics(a):
    """Re-walk corpus aligned with `a`, return (names, list_of_full_metrics)."""
    names, metrics, seen = [], [], set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=True) or gcp._cov_frac(d, physics=False)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            names.append(nm)
            metrics.append(d)
    return names, metrics


def _is_circular(k):
    """Flag σ-derived metrics that would be circular features."""
    kl = k.lower()
    return any(c in kl for c in ('sigma', 'conduct', 'σ', 'kappa', 'resist',
                                   'brug', 'tortuosity_laplace', 'tau_laplace'))


def _all_numeric_metrics(metrics):
    """Build a corpus-wide table of numeric metric values."""
    keys = set()
    for d in metrics:
        keys |= {k for k, v in d.items()
                 if isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v)}
    table = {}
    for k in keys:
        vals = np.array([d.get(k, np.nan) for d in metrics], float)
        if np.isfinite(vals).sum() < 0.5 * len(metrics):
            continue  # too many missing
        v_ok = vals[np.isfinite(vals)]
        if np.std(v_ok) < 1e-12:
            continue  # constant metric
        table[k] = (vals, float(np.nanmean(vals)), float(np.nanstd(vals)))
    return table


def _z_anomalies(metrics_dict, table, top_k=5, threshold=1.5):
    """Top-k metric|z|-scores above threshold for one case."""
    rows = []
    for k, (vals_all, mean, std) in table.items():
        v = metrics_dict.get(k)
        if v is None or not isinstance(v, (int, float)) or not np.isfinite(v):
            continue
        z = (float(v) - mean) / std
        if abs(z) >= threshold:
            rows.append((abs(z), k, float(v), z))
    rows.sort(reverse=True)
    return rows[:top_k]


# ── Candidate correction features ─────────────────────────────────────────
def feat_size_ratio_damp(a, metrics):
    """X: r_SE / r_AM_eff size ratio (centered).  Hypothesis: extreme ratios
    (very small SE relative to AM) correlate with form variance at 10:0."""
    rse = a[:, 8]
    ram = a[:, 13]  # composition-weighted r_AM
    rse_med = float(np.nanmedian(rse[np.isfinite(rse)]))
    ram_med = float(np.nanmedian(ram[np.isfinite(ram)]))
    rse_safe = np.where(np.isfinite(rse) & (rse > 0), rse, rse_med)
    ram_safe = np.where(np.isfinite(ram) & (ram > 0), ram, ram_med)
    ratio = rse_safe / ram_safe
    med = float(np.nanmedian(ratio))
    return ratio - med


def feat_cn_low_damp(a, metrics):
    """Z: CN<3 marginal-percolation soft turn-off.  σ(K·(3 − CN)) gives ~1
    for CN<3 (active) and ~0 for CN>3 (inactive).  Addresses 6mAh_real_6."""
    cn = a[:, 1]
    return 1.0 / (1.0 + np.exp(-3.0 * (3.0 - cn)))  # smooth indicator


def feat_path_hop_area(a, metrics):
    """W: log(path_hop_area_mean_physics) — Holm constriction term, explicitly."""
    vals = np.array([d.get('path_hop_area_mean_physics') or d.get('path_hop_area_mean')
                     for d in metrics], float)
    med = float(np.nanmedian(vals[np.isfinite(vals) & (vals > 0)]))
    safe = np.where(np.isfinite(vals) & (vals > 0), vals, med)
    return np.log(safe / med)


def feat_bulk_resistance_log(a, metrics):
    """V: log(bulk_resistance_fraction_physics).  σ-derived → flagged circular,
    but informationally captures τ_Laplace/τ_Dijkstra gap.  Include cautiously."""
    vals = np.array([d.get('bulk_resistance_fraction_physics') or d.get('bulk_resistance_fraction')
                     for d in metrics], float)
    med = float(np.nanmedian(vals[np.isfinite(vals) & (vals > 0)]))
    safe = np.where(np.isfinite(vals) & (vals > 0), vals, med)
    return np.log(safe / med)


def feat_am_am_cn(a, metrics):
    """U: log(am_am_cn_mean) — AM-AM coordination count (packing geometry)."""
    vals = np.array([d.get('am_am_cn_mean') or 0.0 for d in metrics], float)
    med = float(np.nanmedian(vals[vals > 0])) if (vals > 0).any() else 1.0
    safe = np.where(vals > 0, vals, med)
    return np.log(safe / med)


def feat_stress_cv(a, metrics):
    """T: log(stress_cv) — particle stress non-uniformity (mechanical heterogeneity)."""
    vals = np.array([d.get('stress_cv') or np.nan for d in metrics], float)
    med = float(np.nanmedian(vals[np.isfinite(vals) & (vals > 0)]))
    safe = np.where(np.isfinite(vals) & (vals > 0), vals, med)
    return np.log(safe / med)


# ── FRACTURE candidates (added 2026-05-28 after Part 1 found fracture is
# the dominant anomaly in 6+ outliers; form's cov^½ implicitly assumes
# all contacts are intact, but fracture renders many dysfunctional) ──

def feat_fracture_index(a, metrics):
    """F1: fracture_index (severe / total).  Centered.  Expected β < 0:
    high fracture should REDUCE σ but form ignores it → form over-predicts."""
    vals = np.array([d.get('fracture_index') or 0.0 for d in metrics], float)
    med = float(np.nanmedian(vals[np.isfinite(vals)]))
    return np.where(np.isfinite(vals), vals - med, 0.0)


def feat_intact_pct_log(a, metrics):
    """F2: log(intact_fraction) where intact = 1 − (frag + pulv).
    Expected β > 0: more intact ⇒ higher σ.  Form uses cov without
    fracture correction; this term directly models the broken-contact loss."""
    intact = []
    for d in metrics:
        frag = d.get('frac_fragmentation_pct') or 0.0
        pulv = d.get('frac_pulverization_pct') or 0.0
        intact_pct = max(100.0 - frag - pulv, 1.0)
        intact.append(intact_pct / 100.0)
    return np.log(np.array(intact))


def feat_ionic_active_log(a, metrics):
    """F3: log(ionic_active_pct / 100).  Directly captures fracture-induced
    connectivity loss.  Expected β > 0: low active% ⇒ low σ.  6mAh_real_6
    showed z=-8.3 here (96% vs corpus 100%) — the clearest single signal."""
    vals = np.array([d.get('ionic_active_pct') or 100.0 for d in metrics], float)
    safe = np.where(vals > 0, vals / 100.0, 0.5)
    return np.log(safe)


def feat_fracture_aware_excl_log(a, metrics):
    """F4: log(1 − fracture_aware_excluded_pct/100).  Fraction of contacts
    NOT excluded by fracture awareness.  Captures dysfunctional contacts
    differently from frac_pct (uses the fracture-aware solver's own
    bookkeeping).  1mAh_5_AMP had 82% excluded (z=+2.9)."""
    vals = np.array([d.get('fracture_aware_excluded_pct') or 0.0 for d in metrics], float)
    intact = np.maximum(100.0 - vals, 1.0) / 100.0
    return np.log(intact)


# ── CONNECTIVITY / VULNERABILITY candidates (2026-05-28, NEW after C5
# adoption left 6mAh_real_6 +35% — its TOP anomaly was ionic_active_pct
# z=-8.3, which f_intact (= fracture-excluded) DOESN'T capture) ──

def feat_ionic_active_pct_log(a, metrics):
    """G1: log(ionic_active_pct/100).  Fraction of AM particles touching
    the SE percolating cluster.  DIFFERENT from f_intact — captures
    CONNECTIVITY loss not fracture exclusion.  6mAh_real_6 had z=-8.3
    (only 96% AM active vs corpus 100%).  Expected β > 0: low active% ⇒
    fewer AM-SE conduction pathways ⇒ lower σ."""
    vals = np.array([(d.get('ionic_active_pct') or 100.0) / 100.0 for d in metrics], float)
    safe = np.clip(vals, 0.5, 1.0)
    return np.log(safe)


def feat_am_vulnerable_log(a, metrics):
    """G2: log(1 + am_vulnerable_pct/100).  AM particles with insufficient
    SE coverage (vulnerable to performance loss).  6mAh_real_6 had
    am_vulnerable_pct=2% z=+5.9.  Expected β < 0: more vulnerable AM ⇒
    network performance degraded."""
    vals = np.array([(d.get('am_vulnerable_pct') or 0.0) / 100.0 for d in metrics], float)
    return np.log(1.0 + vals)  # always finite & ≥ 0


def feat_top_reachable_log(a, metrics):
    """G3: log(top_reachable_pct/100).  Fraction of AM reachable from the
    top current collector.  6mAh_real_6 had 87% z=-5.9 (vs ~100% typical).
    Expected β > 0: fewer reachable ⇒ broken current path ⇒ lower σ."""
    vals = np.array([(d.get('top_reachable_pct') or 100.0) / 100.0 for d in metrics], float)
    safe = np.clip(vals, 0.5, 1.0)
    return np.log(safe)


def feat_smooth_f_small(a, metrics):
    """S1: smooth size-based label-free gate g_phys.  Replaces g_010
    (sigmoid in p_AM_P composition) with σ(K·(f_small_smooth − 0.5))
    where f_small_smooth = (1−p)·σ(5·(3.5 − r_AM_S)) + p·σ(5·(3.5 − r_AM_P)).
    For input_S_2 (r_AM_S = 4 µm, near-AM_P size) the smooth gate would
    treat the case as 'borderline' instead of 'pure small-AM' → P2 might
    fire less aggressively, fixing the +24% over-prediction.

    Returns the DIFFERENCE between smooth-g_phys and current g_010 to test
    the swap impact (centered, since constant shift absorbed by C_blend a)."""
    p_arr = a[:, 6]
    # current g_010 (label-based)
    g_010_now = 1.0 / (1.0 + np.exp(10.0 * (p_arr - 0.5)))
    # smooth f_small (size-based, label-free)
    n_m = len(metrics)
    ras = np.array([(d.get('_input_r_AM_S_um') or d.get('r_AM_S') or 2.5) for d in metrics], float)
    rap = np.array([(d.get('_input_r_AM_P_um') or d.get('r_AM_P') or 5.5) for d in metrics], float)
    # if either missing, use median as fallback
    ras = np.where(ras > 0, ras, 2.5)
    rap = np.where(rap > 0, rap, 5.5)
    sig_S = 1.0 / (1.0 + np.exp(-5.0 * (3.5 - ras)))   # small-AM weight
    sig_P = 1.0 / (1.0 + np.exp(-5.0 * (3.5 - rap)))   # ≈0 if r_AM_P big
    f_small = (1.0 - p_arr) * sig_S + p_arr * sig_P
    g_phys_smooth = 1.0 / (1.0 + np.exp(-10.0 * (f_small - 0.5)))
    diff = g_phys_smooth - g_010_now  # diff captures the "swap shift"
    return diff - np.mean(diff)  # center


def _loocv_aug(base, logsf, taus, extras):
    """LOOCV with C_blend + multiple extras (joint OLS per fold)."""
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    X_cols = [np.ones(n), lt, lt**2] + list(extras)
    X = np.column_stack(X_cols)
    betas_acc = []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], logsf[m] - base[m], rcond=None)
        pi = base[i] + X[i] @ coef
        sse += (logsf[i] - pi)**2
        betas_acc.append(coef)
    betas_acc = np.array(betas_acc)
    return 1 - sse/ss, betas_acc.mean(axis=0)


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    names, metrics = _load_names_and_metrics(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]

    # Production C4 (gated P2 + Δcov)
    cf = cronau_factor(a[:, 8])
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)
    extras_c4, _med = production_extras(a)
    lo_c4, b_c4 = _loocv_aug(base, logsf, taus, extras_c4)
    # single-shot pred for current err
    n_e = len(extras_c4)
    lt_all = np.log(taus)
    X_full = np.column_stack([np.ones(n), lt_all, lt_all**2] + extras_c4)
    coef_ss, *_ = np.linalg.lstsq(X_full, logsf - base, rcond=None)
    pred_c4 = base + X_full @ coef_ss
    err_c4 = (np.exp(pred_c4) - np.exp(logsf)) / np.exp(logsf) * 100.0
    out_idx = np.where(np.abs(err_c4) > 20.0)[0]
    out_idx = out_idx[np.argsort(-np.abs(err_c4[out_idx]))]

    print("=" * 90)
    print(f"DEEP OUTLIER INVESTIGATION   n={n}   C4 LOOCV={lo_c4:.4f}")
    print(f"   {len(out_idx)} cases with |err|>20%   ({(np.abs(err_c4)>30).sum()} >30%)")
    print("=" * 90)

    # ===== PART 1 — Per-case anomaly diagnostic =====
    print("\n" + "█" * 90)
    print("PART 1 — Per-case anomaly diagnostic (top 5 metrics with |z|>1.5)")
    print("█" * 90)
    table = _all_numeric_metrics(metrics)
    print(f"  Built corpus stats for {len(table)} numeric metrics.\n")
    for k_rank, i in enumerate(out_idx):
        nm = names[i]; err = err_c4[i]; phi = a[i, 0]; cn = a[i, 1]; rse = a[i, 8]; p = a[i, 6]
        sa = float(np.exp(logsf[i])); sp = float(np.exp(pred_c4[i]))
        print(f"\n  [{k_rank+1}] {nm}   err={err:+.1f}%   σ_act={sa:.3f}  σ_pred={sp:.3f}")
        print(f"      design: φ={phi:.3f}  CN={cn:.1f}  r_SE={rse:.2f}µm  p_AM_P={p:.2f}")
        anomalies = _z_anomalies(metrics[i], table, top_k=8, threshold=1.5)
        for absz, key, v, z in anomalies:
            flag = " (*circ?)" if _is_circular(key) else ""
            print(f"        |z|={absz:4.1f}  z={z:+5.1f}  {key[:50]:50s}={v:.4f}{flag}")

    # ===== PART 2 — Candidate term tests =====
    print("\n" + "█" * 90)
    print("PART 2 — Candidate term tests   (joint with C4: [P2_gated, Δcov] + new)")
    print("█" * 90)
    print(f"  C4 reference: LOOCV={lo_c4:.4f}   "
          f"|err|>20%={len(out_idx)}   |err|>30%={(np.abs(err_c4)>30).sum()}")

    candidates = [
        ('X — r_SE/r_AM ratio damping',          feat_size_ratio_damp),
        ('Z — CN<3 soft turn-off',               feat_cn_low_damp),
        ('W — log(path_hop_area_physics)',       feat_path_hop_area),
        ('V — log(bulk_resistance_fraction)',    feat_bulk_resistance_log),
        ('U — log(am_am_cn_mean)',               feat_am_am_cn),
        ('T — log(stress_cv)',                   feat_stress_cv),
        # FRACTURE candidates (NEW — Part 1 revealed fracture is dominant anomaly)
        ('F1 — fracture_index (centered)',       feat_fracture_index),
        ('F2 — log(intact_fraction) [non-frac]', feat_intact_pct_log),
        ('F3 — log(ionic_active_pct/100)',       feat_ionic_active_log),
        ('F4 — log(1 − fracture_aware_excluded)', feat_fracture_aware_excl_log),
        # CONNECTIVITY / VULNERABILITY (after C5 left 6mAh_real_6 unfixed)
        ('G1 — log(ionic_active_pct/100)',       feat_ionic_active_pct_log),
        ('G2 — log(1 + am_vulnerable_pct/100)',  feat_am_vulnerable_log),
        ('G3 — log(top_reachable_pct/100)',      feat_top_reachable_log),
        # SMOOTH SIZE-BASED gating (for input_S_2 r_AM_S=4µm anomaly)
        ('S1 — smooth f_small (size-based g)',   feat_smooth_f_small),
    ]
    se_loocv = 0.0016  # ~noise SE

    print(f"\n  {'candidate':38s} {'LOOCV':>7s} {'Δ':>7s} {'β_new':>9s}   target outlier changes")
    print("  " + "-" * 88)
    for tag, featfn in candidates:
        new_feat = featfn(a, metrics)
        if not np.all(np.isfinite(new_feat)):
            print(f"  {tag:38s}  [skip: non-finite values]")
            continue
        if np.std(new_feat) < 1e-12:
            print(f"  {tag:38s}  [skip: constant feature]")
            continue
        new_extras = extras_c4 + [new_feat]
        lo_new, b_new = _loocv_aug(base, logsf, taus, new_extras)
        # single-shot for per-case err
        X_new = np.column_stack([np.ones(n), lt_all, lt_all**2] + new_extras)
        coef_new, *_ = np.linalg.lstsq(X_new, logsf - base, rcond=None)
        pred_new = base + X_new @ coef_new
        err_new = (np.exp(pred_new) - np.exp(logsf)) / np.exp(logsf) * 100.0
        d_lo = lo_new - lo_c4
        b_new_term = float(coef_new[-1])
        # Show how the worst 3 outliers changed
        top3 = out_idx[:3]
        change_str = ', '.join(f"{names[i][-12:]}:{err_c4[i]:+.0f}→{err_new[i]:+.0f}%" for i in top3)
        flag = "★" if d_lo > se_loocv else (" " if abs(d_lo) < se_loocv else "⚠")
        print(f"  {tag:38s} {lo_new:7.4f} {d_lo:+7.4f} {b_new_term:+9.4f}   {change_str}  {flag}")
        # Also show how MANY outliers move into ±20%
        n_out_new = int((np.abs(err_new) > 20).sum())
        n_30_new = int((np.abs(err_new) > 30).sum())
        print(f"      → |err|>20% = {n_out_new} (Δ {n_out_new - len(out_idx):+d})   "
              f"|err|>30% = {n_30_new} (Δ {n_30_new - (np.abs(err_c4)>30).sum():+d})")
        # Per-outlier err change summary
        improved = [i for i in out_idx if abs(err_new[i]) < abs(err_c4[i]) - 2.0]
        worsened = [i for i in out_idx if abs(err_new[i]) > abs(err_c4[i]) + 2.0]
        print(f"      improved ≥2pp: {len(improved)}/{len(out_idx)}   "
              f"worsened ≥2pp: {len(worsened)}/{len(out_idx)}")

    # ===== PART 3 — INTEGRATED FRACTURE-AWARE COV TESTS =====
    # User direction: "수식을 합리적으로 넣어봐" — put the equation in
    # reasonably.  Instead of bolt-on β·log(f_intact), MODIFY the existing
    # cov^½ Holm term to use effective cov = cov · f_intact.  This is
    # PHYSICALLY MOTIVATED (Holm: g ∝ √A_contact; broken contacts contribute
    # zero area) and has NO new fit parameter (β is frozen at 0.5 by Holm).
    # In log space: add 0.5·log(f_intact) to base.  Effectively replaces
    # cov^½ with (cov·f_intact)^½ throughout the form.
    print("\n" + "█" * 90)
    print("PART 3 — INTEGRATED fracture-aware cov  (cov → cov · f_intact, frozen β=0.5)")
    print("█" * 90)
    print(f"  C4 reference: LOOCV={lo_c4:.4f}   |err|>20%={len(out_idx)}   |err|>30%={(np.abs(err_c4)>30).sum()}")

    def _f_intact_options(metrics):
        """3 candidate f_intact definitions (intact fraction of contacts)."""
        n_m = len(metrics)
        opts = {}
        # FI1: 1 - fracture_index (frag+pulv / total contacts)
        vals = np.array([d.get('fracture_index') or 0.0 for d in metrics], float)
        opts['FI1: 1 − fracture_index'] = np.clip(1.0 - vals, 0.05, 1.0)
        # FI2: ionic_active_pct / 100
        vals = np.array([(d.get('ionic_active_pct') or 100.0) / 100.0 for d in metrics], float)
        opts['FI2: ionic_active_pct/100'] = np.clip(vals, 0.05, 1.0)
        # FI3: 1 - fracture_aware_excluded_pct/100
        vals = np.array([1.0 - (d.get('fracture_aware_excluded_pct') or 0.0) / 100.0
                         for d in metrics], float)
        opts['FI3: 1 − fracture_aware_excluded/100'] = np.clip(vals, 0.05, 1.0)
        return opts

    f_opts = _f_intact_options(metrics)
    print(f"\n  {'integrated form':40s} {'LOOCV':>7s} {'Δ':>7s}   target outlier changes")
    print("  " + "-" * 88)
    for tag, f_int in f_opts.items():
        # Modified base: add 0.5·log(f_intact) — equivalent to using cov·f_intact in Holm
        base_mod = base + 0.5 * np.log(f_int)
        # Fit C4 with this modified base (same extras: P2_gated + Δcov)
        lo_mod, _ = _loocv_aug(base_mod, logsf, taus, extras_c4)
        # Single-shot pred for per-case shift
        X_full = np.column_stack([np.ones(n), lt_all, lt_all**2] + extras_c4)
        coef_mod, *_ = np.linalg.lstsq(X_full, logsf - base_mod, rcond=None)
        pred_mod = base_mod + X_full @ coef_mod
        err_mod = (np.exp(pred_mod) - np.exp(logsf)) / np.exp(logsf) * 100.0
        d_lo = lo_mod - lo_c4
        flag = "★" if d_lo > se_loocv else (" " if abs(d_lo) < se_loocv else "⚠")
        top3 = out_idx[:3]
        change_str = ', '.join(f"{names[i][-15:]}:{err_c4[i]:+.0f}→{err_mod[i]:+.0f}%" for i in top3)
        print(f"  {tag:40s} {lo_mod:7.4f} {d_lo:+7.4f}   {change_str}  {flag}")
        n_out_new = int((np.abs(err_mod) > 20).sum())
        n_30_new = int((np.abs(err_mod) > 30).sum())
        improved = [i for i in out_idx if abs(err_mod[i]) < abs(err_c4[i]) - 2.0]
        worsened = [i for i in out_idx if abs(err_mod[i]) > abs(err_c4[i]) + 2.0]
        print(f"      → |err|>20% = {n_out_new} (Δ {n_out_new - len(out_idx):+d})   "
              f"|err|>30% = {n_30_new} (Δ {n_30_new - (np.abs(err_c4)>30).sum():+d})")
        print(f"      improved ≥2pp: {len(improved)}/{len(out_idx)}   "
              f"worsened ≥2pp: {len(worsened)}/{len(out_idx)}")
        # Per-outlier err change for ALL 10 outliers (detail)
        print(f"      per-outlier shifts:")
        for i in out_idx:
            shift = err_mod[i] - err_c4[i]
            marker = "↓" if abs(err_mod[i]) < abs(err_c4[i]) else ("↑" if abs(err_mod[i]) > abs(err_c4[i]) else "·")
            print(f"        {names[i][:30]:30s}  {err_c4[i]:+6.1f}% → {err_mod[i]:+6.1f}%  ({shift:+5.1f}pp)  {marker}")

    print("\n" + "=" * 90)
    print("Interpretation guide:")
    print("  • ★ candidate: LOOCV beats C4 by > noise SE — worth testing leave-corner-out")
    print("  • improved≥2pp count high = candidate captures multiple outliers")
    print("  • β_new sign / magnitude indicates direction of correction")
    print("  • PART 3 ★ = INTEGRATED form supported by Holm physics (β frozen 0.5)")
    print("            adopt by modifying _sat_baselog: cov → cov · f_intact")


if __name__ == "__main__":
    main()
