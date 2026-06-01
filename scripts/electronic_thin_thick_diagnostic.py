#!/usr/bin/env python3
"""σ_electronic Stage 16 — 박막(thin) vs 후막(thick) 분리 진단.

User insight (2026-06-01): 박막에서 form 이 안 맞는 mechanism 이 후막과
다르므로, T/d_AM ratio (또는 절대 thickness) 로 분리하는 게 shape
매칭에 도움될 것.

이 스크립트:
  1. 각 case 의 T, d_AM, T/d_AM 계산
  2. T/d_AM 으로 thin / mid / thick 3 bin 분리
  3. 각 bin 별 form-vs-target bias 평균 + spread 보고
  4. 잔차 ~ T/d Spearman 상관 (현재 form 의 T/d 의존성 충분한지)
  5. dual-branch (thin/thick separate fit) 시도 → 단일 fit 대비 LOOCV 개선 측정
  6. 박막 영역 의 missing physics 후보 (잔차-feature 상관)

verdict: dual-branch 가 |ΔLOOCV| > +0.01 이면 Stage 17 으로 진행 가치.

Run on WSL:
    python3 scripts/electronic_thin_thick_diagnostic.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from collections import defaultdict
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def main():
    import matplotlib
    matplotlib.use('Agg')
    import generate_comparison_plots as gcp
    from scipy.stats import spearmanr

    # ───── Walk corpus (archive first, skip nameless) ─────
    data_list, names = [], []
    seen = set()
    for base in ('webapp/archive', 'webapp/results'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            meta_p = mp.parent / 'meta.json'
            cid = mp.parent.name
            nm = cid
            if meta_p.exists():
                try:
                    mn = json.load(open(meta_p)).get('name', '') or ''
                    if mn: nm = mn
                except Exception: pass
            if nm == cid and not nm.startswith('input_'): continue
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except Exception: continue
            data_list.append(d); names.append(nm)

    # ───── Global Stage 16 fit ─────
    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None:
        print("[ABORT] corpus too small"); return
    fit_mask = ~arr['excluded']
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    coef = fit['coef']
    sig_act = arr['sig_act']
    sig_pred = np.exp(fit['pred_log'])
    err_pct = (sig_pred - sig_act) / sig_act * 100.0
    resid_log = arr['logsf'] - fit['pred_log']
    n = arr['n']
    nfit = fit['n_fit']

    # T/d_AM ratio
    T_a = arr['T']
    r_eff = arr['r_eff']
    d_AM = 2.0 * r_eff
    Td = T_a / d_AM

    print("=" * 100)
    print(f" σ_electronic Stage 16 — THIN vs THICK diagnostic  (n={n}, fit={nfit})")
    print("=" * 100)
    print(f"  Global fit: σ_S={float(np.exp(coef[0])):.2f}  σ_P={float(np.exp(coef[1])):.2f}  "
          f"β_T={coef[2]:+.3f}  β_AC={coef[7]:+.3f}")
    print(f"  R²={fit['r2']:.3f}  LOOCV={fit['loocv']:.3f}")
    print()
    print(f"  T/d_AM 분포:  min={Td.min():.1f}  median={np.median(Td):.1f}  "
          f"max={Td.max():.1f}  (T={T_a.min():.0f}~{T_a.max():.0f}μm, "
          f"d_AM={d_AM.min():.1f}~{d_AM.max():.1f}μm)")
    print()

    # ───── Bin by T/d_AM ─────
    # Boundaries: thin (T/d < 5), mid (5..15), thick (≥15)
    bins = [
        ('thin (T/d < 5)',     Td < 5),
        ('mid  (5 ≤ T/d < 15)', (Td >= 5) & (Td < 15)),
        ('thick (T/d ≥ 15)',   Td >= 15),
    ]
    print("─" * 100)
    print(" Per T/d_AM bin shape bias")
    print("─" * 100)
    print(f"  {'bin':22s}  {'n':>4s}  {'n_clean':>7s}  {'mean err%':>10s}  {'median':>8s}  "
          f"{'p25..p75':>16s}  {'max |err|':>9s}")
    for lab, mask in bins:
        n_total = int(mask.sum())
        if n_total == 0:
            print(f"  {lab:22s}  {0:>4d}  empty"); continue
        clean_mask = mask & (~arr['excluded'])
        n_clean = int(clean_mask.sum())
        if n_clean == 0:
            print(f"  {lab:22s}  {n_total:>4d}  {0:>7d}  all excluded"); continue
        errs = err_pct[clean_mask]
        m = float(np.mean(errs)); md = float(np.median(errs))
        p25 = float(np.percentile(errs, 25)); p75 = float(np.percentile(errs, 75))
        mx = float(np.max(np.abs(errs)))
        flag = ""
        if abs(m) > 15: flag = "  ★ SHAPE-MISS"
        elif abs(m) > 8: flag = "  ◆ moderate"
        print(f"  {lab:22s}  {n_total:>4d}  {n_clean:>7d}  {m:+10.1f}  {md:+8.1f}  "
              f"{p25:+6.1f}..{p75:+5.1f}  {mx:>9.1f}{flag}")
    print()

    # ───── Spearman ρ(resid, T/d) ─────
    clean = ~arr['excluded']
    rho_td, _ = spearmanr(Td[clean], resid_log[clean])
    rho_t, _ = spearmanr(T_a[clean], resid_log[clean])
    print("─" * 100)
    print(" 잔차 ~ thickness 시그널")
    print("─" * 100)
    print(f"  ρ(residual, T/d_AM) = {rho_td:+.3f}  (current form 의 (T/d)^β_T 가 충분히 보정?)")
    print(f"  ρ(residual, T_um)   = {rho_t:+.3f}  (절대 두께 신호)")
    if abs(rho_td) > 0.3:
        if rho_td < 0:
            direction = "form OVER-predicts thin (T/d 작을수록 form 너무 높음)"
        else:
            direction = "form UNDER-predicts thin (T/d 작을수록 form 너무 낮음)"
        print(f"  → {direction} → β_T 조정 또는 thin-only correction 필요")
    elif abs(rho_td) < 0.15:
        print(f"  → T/d 신호 거의 없음 — 현재 (T/d)^β_T 가 적절히 잡고 있음")
    print()

    # ───── Dual-branch (thin vs thick separate fit) ─────
    print("─" * 100)
    print(" Dual-branch fit test  (T/d split → 두 region 별도 fit)")
    print("─" * 100)
    cutoff = 8.0   # T/d < 8 = thin, ≥8 = thick (initial guess; can tune)
    thin_mask = Td < cutoff
    thick_mask = Td >= cutoff
    thin_clean = thin_mask & (~arr['excluded'])
    thick_clean = thick_mask & (~arr['excluded'])
    n_thin, n_thick = int(thin_clean.sum()), int(thick_clean.sum())
    print(f"  cutoff T/d = {cutoff}")
    print(f"  thin  (T/d<{cutoff}):  n={n_thin}")
    print(f"  thick (T/d≥{cutoff}):  n={n_thick}")

    if n_thin >= 8 and n_thick >= 8:
        # Fit each separately on full design matrix
        from numpy.linalg import lstsq
        X = arr['X']; y_resid = arr['y_resid']
        # Per-bin LOOCV
        def loo_r2(X_, y_):
            n_ = len(y_)
            coef_full, *_ = lstsq(X_, y_, rcond=None)
            ss = float(np.sum((y_ - y_.mean())**2))
            sse = 0.0
            for j in range(n_):
                m_ = np.ones(n_, bool); m_[j] = False
                c, *_ = lstsq(X_[m_], y_[m_], rcond=None)
                sse += (y_[j] - X_[j] @ c)**2
            return 1 - sse/ss if ss > 0 else 0.0
        # Global fit reference (audit-excluded removed)
        loo_global = float(fit['loocv'])
        loo_thin = loo_r2(X[thin_clean], y_resid[thin_clean])
        loo_thick = loo_r2(X[thick_clean], y_resid[thick_clean])
        # Effective combined LOOCV: weighted average of per-bin SSE
        # Approximate: n-weighted average of individual LOOCV
        loo_dual = (n_thin*loo_thin + n_thick*loo_thick) / (n_thin + n_thick)
        delta = loo_dual - loo_global
        print()
        print(f"  Global (single fit)    LOOCV = {loo_global:.4f}")
        print(f"  Dual (thin-only fit)   LOOCV = {loo_thin:.4f}  on n={n_thin}")
        print(f"  Dual (thick-only fit)  LOOCV = {loo_thick:.4f}  on n={n_thick}")
        print(f"  Dual combined (n-wt)   LOOCV = {loo_dual:.4f}")
        print(f"  Δ vs global            = {delta:+.4f}")
        if delta > 0.01:
            print(f"  → ★ ADOPT dual-branch — 통계 SE 안 + meaningful improvement")
        elif delta > 0.005:
            print(f"  → ◆ marginal — ROI 검토")
        else:
            print(f"  → form 단일 fit 이 충분 — dual-branch 가치 없음")
    else:
        print(f"  → 한 bin 이 너무 작음 (≥8 필요), dual-branch 진단 불가")
    print()

    # ───── Thin-region missing physics candidates ─────
    print("─" * 100)
    print(" Thin region (T/d<5) 의 잔차 ~ feature Spearman")
    print(" (박막에서 잔차 잘 설명하는 feature → thin-specific form term 후보)")
    print("─" * 100)
    thin_clean_idx = np.where(thin_clean)[0]
    if len(thin_clean_idx) >= 5:
        feat_keys = ['phi_am', 'phi_se', 'am_am_cn', 'am_am_mean_area',
                     'se_se_cn', 'coverage_AM_mean', 'coverage_AM_P_mean',
                     'coverage_AM_S_mean', 'thickness_um', 'r_AM_S', 'r_AM_P',
                     'bulk_resistance_fraction', 'contact_pressure_mean',
                     'stress_cv', 'tortuosity_recommended']
        rhos_thin = []
        for k in feat_keys:
            vals = []
            for ci in thin_clean_idx:
                idx_src = arr['keep_idx'][ci]
                v = data_list[idx_src].get(k)
                vals.append(float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else np.nan)
            vals = np.array(vals)
            mask_v = np.isfinite(vals)
            if mask_v.sum() < 5: continue
            r_, _ = spearmanr(vals[mask_v], resid_log[thin_clean_idx[mask_v]])
            if not np.isnan(r_):
                rhos_thin.append((k, float(r_)))
        rhos_thin.sort(key=lambda r: -abs(r[1]))
        for k, r_ in rhos_thin[:8]:
            flag = ""
            if abs(r_) > 0.5: flag = "  ★ STRONG"
            elif abs(r_) > 0.3: flag = "  ◆ moderate"
            print(f"  {k:25s}  ρ={r_:+.3f}{flag}")
    else:
        print(f"  thin region 너무 작음 (n={len(thin_clean_idx)})")
    print()

    print("=" * 100)
    print(" VERDICT")
    print("=" * 100)
    if abs(rho_td) > 0.3 and n_thin >= 8 and n_thick >= 8:
        print(f"  T/d 잔차 신호 {rho_td:+.2f} + dual-branch 분리 가치 있음")
        print(f"  → Stage 17 으로 진행 검토:")
        print(f"     - sigmoid blend: σ_e = w(T/d)·σ_thin + (1-w)·σ_thick")
        print(f"     - 또는 thin-only correction 항 추가: exp(β_thin·g_thin·X)")
        print(f"     - 위 thin-region feature 중 |ρ|>0.3 인 것을 새 항 후보로")
    else:
        print(f"  현재 (T/d)^β_T 가 thin/thick 가 거의 잡고 있음")
        print(f"  → 박막 mismatch 는 다른 원인 (1mAh family-wide bias 등 데이터 한계)")


if __name__ == '__main__':
    main()
