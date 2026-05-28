#!/usr/bin/env python3
"""Per-case factor decomposition for the σ_ionic outliers.

For every case with |err|>20% on the production form (SAT-blend × Cronau),
print which term in  log σ = log(σ_grain·Cronau) + 0.5·log(φ_eff) + CN²-term
                              + cov-term + f_p-term + C_blend(τ)
is unusual (|z|>1 across the corpus) and how much each term contributes.
This answers "which factor in the fit is pulling D1/D1.5 down?".

Run from the repo root:  python3 scripts/audit_outliers_factors.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp                                # noqa: E402
from nested_cv_sat import (base_log_sat, cblend_fit, cblend_pred,      # noqa: E402
                           cronau_factor, _direct_rse_um, PHI_C0,
                           PHICP_F, PHICS_F, DELTA_F, SG,
                           K_PS, P_C, _EXCLUDED_NAMES, _meta_name)


def load():
    rows, names = [], []
    seen = set()
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
            fp = gcp._get(d, 'percolation_pct')/100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            p = gcp._ps_fraction(d)
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            rse = _direct_rse_um(d) or np.nan
            cid = mp.parent.name
            nm = _meta_name(cid, mp.parent)
            if nm in _EXCLUDED_NAMES:
                continue
            rows.append((phi, cn, cov, fp, tau, float(sig), p, rse))
            names.append(nm)
    return np.array(rows, float), names


def main():
    a, names = load()
    n = len(a)
    if n < 10:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 7]))
    bv5, bp3 = cblend_fit(base, logsf, taus)
    pred = base + (cblend_pred(base, taus, bv5, bp3) - base)
    err_pct = (np.exp(pred) - np.exp(logsf))/np.exp(logsf)*100.0

    # Per-case TERM contributions (log space).
    phi, cn, cov, fp = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    p_frac, rse = a[:, 6], a[:, 7]
    g010 = 1.0/(1.0+np.exp(K_PS*(p_frac - P_C)))
    phic = (1.0-g010)*PHICP_F + g010*PHICS_F
    pex = phi - phic
    phi_eff = np.sqrt(pex**2 + (DELTA_F*g010)**2 + 1e-12)
    terms = {
        'σ_grain':   np.log(SG)*np.ones(n),
        'Cronau':    np.log(cronau_factor(rse)),
        '(φ_eff)^½': 0.5*np.log(phi_eff),
        'CN²':       2.0*np.log(cn),
        'cov^½':     0.5*np.log(cov),
        'f_p³':      3.0*np.log(fp),
        'C_blend':   cblend_pred(base, taus, bv5, bp3) - base,
    }
    # z-scores of each term across the corpus
    zs = {k: (v - v.mean())/(v.std() if v.std() > 1e-9 else 1.0) for k, v in terms.items()}

    # outliers (|err|>20%)
    is_out = np.abs(err_pct) > 20.0
    order = np.argsort(-np.abs(err_pct))
    out_idx = [i for i in order if is_out[i]]

    print(f"Corpus n={n} | outliers (|err|>20%): {len(out_idx)}")
    print(f"Production form LOOCV={1 - np.sum((logsf-pred)**2)/np.sum((logsf-logsf.mean())**2):.4f}")
    print(f"\n{'CASE':30s} {'err%':>6s}  {'log σ_act':>9s} {'log σ_pred':>10s}   "
          + ' '.join(f"{k:>9s}" for k in terms))
    print("-" * 130)
    for i in out_idx[:20]:
        line = (f"{names[i][:30]:30s} {err_pct[i]:+6.1f}  "
                f"{logsf[i]:+9.3f} {pred[i]:+10.3f}   ")
        for k in terms:
            v = terms[k][i]; z = zs[k][i]
            tag = '*' if abs(z) > 1.0 else ' '
            line += f"{v:+7.2f}{tag}({z:+.1f})  "
        # cut to fit
        print(line[:200])
    print("\nLegend: '*' = |z|>1 (this term is unusual for this case across the corpus).")
    print("→ For each outlier, look at the '*' columns to see WHICH term in the form")
    print("  is pulling its prediction away from the actual.")

    # Aggregate: which term most often outlier-tags in the SE-rich 0:10 (D1/D1.5)
    sub = [i for i in out_idx if p_frac[i] < 0.05 and phi[i] > 0.30]
    if sub:
        print(f"\nSE-rich 0:10 outliers (D1/D1.5-type, n={len(sub)}): "
              "term-by-term mean z & residual share")
        for k in terms:
            mz = float(np.mean([zs[k][i] for i in sub]))
            print(f"  {k:>10s}  mean z = {mz:+.2f}")

    # Name-family check — for each TOP-3 outlier, strip a trailing seed suffix
    # ('_S\d+', '_real_\d+', or trailing '_\d+') and list every corpus case
    # sharing that base.  If ONE seed is wildly off and siblings are fine → the
    # outlier is likely a per-seed simulation anomaly (candidate for removal).
    import re as _re
    def _family_base(nm):
        s = _re.sub(r'_S\d+$', '', nm)
        s = _re.sub(r'_real_\d+$', '_real', s)
        s = _re.sub(r'_\d+$', '', s)
        return s
    seen_bases = set()
    print("\n══ Name-family check (siblings of the top outliers) ══")
    for i_top in out_idx[:5]:
        base_nm = _family_base(names[i_top])
        if base_nm in seen_bases:
            continue
        seen_bases.add(base_nm)
        sibs = [j for j, nm in enumerate(names) if _family_base(nm) == base_nm]
        if len(sibs) < 2:
            continue
        sibs.sort(key=lambda j: names[j])
        print(f"\n  family '{base_nm}' — {len(sibs)} cases:")
        print(f"  {'name':30s}  {'σ_act':>7s}  {'σ_pred':>7s}  {'err%':>6s}  {'φ':>5s}  {'CN':>5s}  {'r_SE':>5s}")
        for j in sibs:
            sa, sp = float(np.exp(logsf[j])), float(np.exp(pred[j]))
            print(f"  {names[j][:30]:30s}  {sa:7.3f}  {sp:7.3f}  {err_pct[j]:+6.1f}  "
                  f"{a[j,0]:5.3f}  {a[j,1]:5.1f}  "
                  f"{a[j,7] if np.isfinite(a[j,7]) else float('nan'):5.2f}")
    print("\n→ If one variant is wildly off vs siblings (similar σ_act range, "
          "same φ/CN/r_SE) it's likely a per-seed simulation artifact.")


if __name__ == "__main__":
    main()
