#!/usr/bin/env python3
"""Combo test: P3 (signed-pivot r0=0.8) × sharpened Cronau, with
single-layer-AM_P pathology diagnostic.

CONTEXT
-------
Individual tests (test_p3_linear_pivot.py) showed:
  • P3 r0=0.8           ΔLOOCV +0.0012 (BELOW noise SE 0.0016)
                        corner-RMSE 0.1274→0.1059, LCO-RMSE 0.4146→0.1185 (BIG)
                        helps D0.5 62:38 corner & D0.25 (different mechanism)
  • Cronau sharpened    ΔLOOCV +0.0017 (just ABOVE noise SE)
                        helps D0.25 (sub-µm Cronau drop-off)
                        plateaus (1, 0.85, 0.55, 0.25) vs current (1, 0.90, 0.65, 0.33)

The two fixes target DIFFERENT case families:
  • P3 (signed r_SE pivot) ⟶ D0.5, D1, D1.5 (the bidirectional r_SE bias)
  • Cronau-sharp           ⟶ D0.25, sub-0.5µm SE (steeper Cronau curve)
→ likely ADDITIVE.  This script measures the combo.

PORosity connection (user 2026-05-28):
  Porosity v4 model also has outliers, including:
    A1 = input_1mAh_100_15  (single-layer AM_P, D_P > 0.5·thickness)
    A2 = input_1mAh_100_10  (single-layer AM_P)
    B  = input_1mAh_5_AMP   (single-layer AM_P)   ← ALSO σ_ionic outlier (+24.5%)
  Hypothesis: 'isolated 10:0' σ_ionic outliers (1mAh_5_AMP, 1mAh_8_AMP,
  8mAh_8_AMP, 8mAh_real_10) share the same single-layer geometric
  pathology that breaks porosity's continuum assumption.  This script
  computes D_P / thickness ratio for every σ_ionic outlier case and
  flags the ones in single-layer regime.

TESTS
-----
  1. T1 reference                (P2 + current Cronau)
  2. P3 r0=0.8 + current Cronau  (already tested)
  3. P2 + sharp Cronau           (already tested)
  4. P3 r0=0.8 + sharp Cronau    ← THE COMBO (NEW)
  5. additional r0 scan with sharp Cronau (r0 ∈ {0.7, 0.8, 0.9, 1.0})

VERDICT
-------
  • combo ΔLOOCV vs T1 > additive sum of individual ΔLOOCVs (+0.0029)?
    → fully additive, ADOPT BOTH
  • combo ΔLOOCV > 0.0017 but < additive sum?
    → partial interference, ADOPT ONE (the better individual)
  • combo ΔLOOCV ≤ 0.0017?
    → fixes interfere, KEEP T1

Plus diagnostic table: D_P/T ratio per σ_ionic outlier (single-layer flag).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from nested_cv_sat import (load_corpus, base_log_sat, cronau_factor,
                           cblend_fit, cblend_pred, loocv_r2, _g_phys_smooth,
                           _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, PHIC_PROD, PHI_C0)
import generate_comparison_plots as gcp


# ───── Form variants ────────────────────────────────────────────────
def p2_feat(a, g):
    """T1 production P2 = g · (φ−0.195)² · (r_SE − 0.5)+."""
    phi = a[:, 0]; r = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    rs = np.where(np.isfinite(r) & (r > 0), r, 0.5)
    return g * pex**2 * np.maximum(rs - 0.5, 0.0)


def p3_feat(a, r0, g):
    """Signed pivot P3 = g · (φ−0.195)² · (r_SE − r0)."""
    phi = a[:, 0]; r = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    rs = np.where(np.isfinite(r) & (r > 0), r, r0)
    return g * pex**2 * (rs - r0)


def cronau_sharp(rse_um):
    """Sharpened Cronau: plateaus (1, 0.85, 0.55, 0.25) vs current (1, 0.90, 0.65, 0.33)."""
    r = np.asarray(rse_um, float)
    K = 50.0
    f = (0.25
         + 0.30 / (1.0 + np.exp(-K*(r - 0.10)))
         + 0.30 / (1.0 + np.exp(-K*(r - 0.30)))
         + 0.15 / (1.0 + np.exp(-K*(r - 0.50))))
    return np.where(np.isfinite(r) & (r > 0), f, 1.0)


def fi_log(a):
    return a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])


def eval_variant(a, logsf, taus, base, extras, label):
    """Return (LOOCV, corner-RMSE, in-sample pred_log, err_pct)."""
    lo = loocv_r2(base, logsf, taus, extras=extras)
    b = cblend_fit(base, logsf, taus, extras=extras)
    pred = cblend_pred(base, taus, b, extras=extras)
    err = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100.0
    corner = (a[:, 6] < 0.05) & (a[:, 0] > 0.30)
    crmse = float(np.sqrt(np.mean((pred[corner] - logsf[corner])**2)))
    return lo, crmse, pred, err, b


# ───── Per-case names (for outlier overlap with porosity) ──────────
def load_case_names(n_target):
    names, seen = [], set()
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
            cov = gcp._cov_frac(d, physics=False) or gcp._cov_frac(d, physics=True)
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
            seen.add(key); names.append((nm, mp))
            if len(names) == n_target:
                break
    return names


def single_layer_diag(name_paths):
    """Per case, compute D_P / electrode-thickness ratio → single-layer flag.
    D_P = 2 * r_AM_P (µm).  thickness from thickness_um or _input_thickness_um."""
    rows = []
    for nm, mp in name_paths:
        try:
            d = json.load(open(mp))
        except Exception:
            continue
        # r_AM_P
        r_amp = None
        for k in ('_input_r_AM_P_um', '_input_r_AM_P', 'r_AM_P_um', 'r_AM_P'):
            v = d.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                r_amp = v * 1000.0 if v < 0.01 else float(v)
                break
        # thickness
        T = None
        for k in ('thickness_um', '_input_thickness_um', 'thickness', '_input_thickness'):
            v = d.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                T = float(v) * 1000.0 if v < 0.1 else float(v)
                break
        ratio = (2.0 * r_amp / T) if (r_amp and T) else None
        rows.append((nm, r_amp, T, ratio))
    return rows


def main():
    print("=" * 78)
    print(" COMBO TEST: P3 (signed-pivot) × Cronau-sharp + single-layer diagnostic")
    print("=" * 78)
    a = load_corpus()
    n = len(a)
    print(f"Corpus n = {n}")
    if n < 8 or a.ndim < 2:
        print("[ABORT] need corpus of ≥8 cases (run on WSL).")
        return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    g_phys = _g_phys_smooth(a); fi = fi_log(a)
    cron_cur = np.log(cronau_factor(a[:, 8]))
    cron_sharp = np.log(cronau_sharp(a[:, 8]))
    base_sat = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F)
    base_cur = base_sat + cron_cur
    base_sharp = base_sat + cron_sharp

    corner = (a[:, 6] < 0.05) & (a[:, 0] > 0.30)
    n_corner = int(corner.sum())
    print(f"0:10·SE-rich corner cases: {n_corner} / {n}\n")

    # ───── Four-way comparison ─────
    print("─" * 78)
    print(" Four-way variant LOOCV + corner RMSE")
    print("─" * 78)
    p2 = p2_feat(a, g_phys); p3_08 = p3_feat(a, 0.8, g_phys)

    variants = [
        ("T1 (P2 + cur Cronau) [REF]",  base_cur,   [p2,    fi]),
        ("P3 r0=0.8 + cur Cronau",      base_cur,   [p3_08, fi]),
        ("P2        + sharp Cronau",    base_sharp, [p2,    fi]),
        ("P3 r0=0.8 + sharp Cronau",    base_sharp, [p3_08, fi]),
    ]
    results = []
    for lbl, b, e in variants:
        lo, crmse, _pred, _err, _b = eval_variant(a, logsf, taus, b, e, lbl)
        results.append((lbl, lo, crmse))

    lo_t1 = results[0][1]; crmse_t1 = results[0][2]
    print(f"  {'variant':40s}  {'LOOCV':>7s}  {'ΔLOOCV':>8s}   {'corner-RMSE':>11s}  {'ΔRMSE':>8s}")
    for lbl, lo, crmse in results:
        d_lo = lo - lo_t1
        d_rmse = crmse - crmse_t1
        print(f"  {lbl:40s}  {lo:7.4f}  {d_lo:+8.4f}   {crmse:11.4f}  {d_rmse:+8.4f}")
    print()

    # Additivity check
    d_p3 = results[1][1] - lo_t1
    d_sh = results[2][1] - lo_t1
    d_co = results[3][1] - lo_t1
    additive_pred = d_p3 + d_sh
    print(f"  Additivity check:")
    print(f"    Δ(P3 only)              = {d_p3:+.4f}")
    print(f"    Δ(Cronau-sharp only)    = {d_sh:+.4f}")
    print(f"    Δ(additive prediction)  = {additive_pred:+.4f}")
    print(f"    Δ(combo measured)       = {d_co:+.4f}")
    interference = d_co - additive_pred
    print(f"    interference            = {interference:+.4f}  "
          f"({'additive' if abs(interference) < 0.0005 else 'partial' if d_co > max(d_p3,d_sh) else 'destructive'})")
    print()

    # ───── r0 scan with sharp Cronau ─────
    print("─" * 78)
    print(" Fine r0 scan with sharp Cronau (find best combo pivot)")
    print("─" * 78)
    print(f"  {'r0':>4s}  {'LOOCV':>7s}  {'ΔvsT1':>8s}   {'corner-RMSE':>11s}")
    best_r0 = (0.8, results[3][1])  # default
    for r0 in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]:
        if r0 == 0.5:
            # at r0=0.5, P3 reduces to (signed) variant of P2's pivot
            p3_r = p3_feat(a, 0.5, g_phys)
        else:
            p3_r = p3_feat(a, r0, g_phys)
        lo, crmse, _, _, _ = eval_variant(a, logsf, taus, base_sharp, [p3_r, fi], "")
        marker = " ←" if lo > best_r0[1] else ""
        if lo > best_r0[1]:
            best_r0 = (r0, lo)
        print(f"  {r0:4.1f}  {lo:7.4f}  {lo-lo_t1:+8.4f}   {crmse:11.4f}{marker}")
    print()
    print(f"  Best combo pivot: r0={best_r0[0]:.1f}  LOOCV={best_r0[1]:.4f}  "
          f"Δ vs T1 = {best_r0[1]-lo_t1:+.4f}")
    print()

    # ───── Per-case error: T1 vs best combo ─────
    print("─" * 78)
    print(" Per-case |err%| change on |err|>15% outliers (T1 → best combo)")
    print("─" * 78)
    p3_b = p3_feat(a, best_r0[0], g_phys)
    _, _, pred_combo, err_combo, _ = eval_variant(a, logsf, taus, base_sharp, [p3_b, fi], "")
    _, _, pred_t1,    err_t1,    _ = eval_variant(a, logsf, taus, base_cur,   [p2,    fi], "")
    names = load_case_names(n)
    nm_list = [nm for nm, _ in names]
    outlier_idx = np.where(np.abs(err_t1) > 15)[0]
    print(f"  {'case':32s}  {'φ':>5s} {'r_SE':>5s} {'p':>5s}    "
          f"{'err T1':>7s}  {'err combo':>9s}  {'Δ':>7s}")
    for i in sorted(outlier_idx, key=lambda j: -abs(err_t1[j])):
        nm = nm_list[i] if i < len(nm_list) else f"(idx{i})"
        dlt = abs(err_combo[i]) - abs(err_t1[i])
        flag = " ↓" if dlt < -3 else (" ↑" if dlt > 3 else "  ")
        rse_s = f"{a[i,8]:5.2f}" if np.isfinite(a[i,8]) else "  —  "
        print(f"  {nm[:32]:32s}  {a[i,0]:5.3f} {rse_s} {a[i,6]:5.2f}    "
              f"{err_t1[i]:+7.1f}  {err_combo[i]:+9.1f}  {dlt:+7.1f}{flag}")
    print()

    # ───── Single-layer AM_P diagnostic ─────
    print("─" * 78)
    print(" Single-layer AM_P pathology diagnostic (D_P / thickness)")
    print(" (porosity v4 model labels D_P > 0.5·T as 'Group A' outliers)")
    print("─" * 78)
    sl_rows = single_layer_diag(names)
    n_known = sum(1 for _, ramp, T, _ in sl_rows if ramp and T)
    print(f"  thickness + r_AM_P data available for {n_known}/{n} cases")
    print()
    print(f"  {'case':32s}  {'r_AM_P':>7s}  {'T_um':>7s}  {'D_P/T':>7s}  "
          f"{'σ_ionic err%':>11s}  {'flag':>10s}")
    print("  " + "─" * 76)
    sl_flagged = []
    for i, ((nm, _), (_, ramp, T, ratio)) in enumerate(zip(names, sl_rows)):
        err = err_t1[i]
        if ratio is None:
            continue
        flag = " single-layer" if ratio > 0.5 else ""
        if ratio > 0.5 or abs(err) > 15:
            print(f"  {nm[:32]:32s}  {ramp:7.2f}  {T:7.1f}  {ratio:7.3f}  "
                  f"{err:+11.1f}  {flag:>10s}")
            if ratio > 0.5:
                sl_flagged.append((nm, ratio, err))
    print()

    if sl_flagged:
        print(f"  {len(sl_flagged)} cases flagged as single-layer-AM_P pathology:")
        mean_abs_err = np.mean([abs(e) for _, _, e in sl_flagged])
        print(f"    mean |σ_ionic err%| = {mean_abs_err:.1f}%  "
              f"(corpus avg ≈ {np.mean(np.abs(err_t1)):.1f}%)")
        if mean_abs_err > 1.5 * np.mean(np.abs(err_t1)):
            print(f"    → single-layer flag IS predictive of σ_ionic outliers.")
            print(f"    → recommend: document + EXCLUDE these from form-fit corpus, OR")
            print(f"      add geometric correction term (overfitting risk: only {len(sl_flagged)} cases).")
        else:
            print(f"    → single-layer flag is NOT a strong predictor of σ_ionic outliers here.")
    else:
        print("  No single-layer cases found (no D_P > 0.5·T in corpus).")
    print()

    # ───── VERDICT ─────
    print("=" * 78)
    print(" VERDICT")
    print("=" * 78)
    noise_se = 0.0016
    best_combo_delta = best_r0[1] - lo_t1
    print(f"  noise SE                : ±{noise_se:.4f}")
    print(f"  Best combo Δ vs T1      : {best_combo_delta:+.4f}  "
          f"({'above' if best_combo_delta > noise_se else 'below'} noise)")
    print(f"  P3 alone Δ              : {d_p3:+.4f}  ({'pass' if d_p3 > noise_se else 'fail'} noise)")
    print(f"  Cronau-sharp alone Δ    : {d_sh:+.4f}  ({'pass' if d_sh > noise_se else 'fail'} noise)")
    print()
    if best_combo_delta > 2 * noise_se:
        print(f"  → ADOPT COMBO: P3 r0={best_r0[0]:.1f} + sharpened Cronau "
              f"({best_combo_delta/noise_se:.1f}× noise).")
    elif best_combo_delta > noise_se:
        print(f"  → MARGINAL combo improvement; consider literature support for Cronau-sharp")
        print(f"    plateau values (1, 0.85, 0.55, 0.25) vs current (1, 0.90, 0.65, 0.33).")
    else:
        print(f"  → Combo doesn't clear noise bar; KEEP T1, focus on geometric")
        print(f"    pathology (single-layer AM_P) as separate documentation path.")


if __name__ == '__main__':
    main()
