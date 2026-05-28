#!/usr/bin/env python3
"""Diagnose what explains the 0:10 / 62:38 σ_ionic residual (after SAT-blend).

62:38 is the SE-RICH end of the 0:10 group (≈38% SE → high σ), NOT near the
percolation threshold — so GB / threshold rounding are irrelevant there.  The
open question is why σ swings ~3× across SE size at fixed composition
(D0.25≈0.23 vs D1≈0.67).  This ranks EVERY numeric full-metrics field by its
correlation with the SAT-blend log-residual, computed three ways:

    • whole corpus
    • 0:10 subset (pure AM_S)
    • 0:10 + SE-rich subset (φ above the 0:10 median → the 62:38-type cases)

so a feature that explains the spread WITHIN 0:10 shows up even if it is
diluted globally.  Fields whose name implies they are derived from σ
(circular) are flagged with (*).

Run from the repo root:  python3 scripts/resid_diag_62_38.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp          # noqa: E402
from nested_cv_sat import base_log_sat, cblend_fit, cblend_pred, PHI_C0  # noqa: E402

# φc_P*, φc_S*, δ* frozen at the production SAT-blend values
PHICP, PHICS, DELTA = 0.200, 0.195, 0.040
# name fragments that imply a σ-derived (circular) quantity → flag, don't trust
_CIRC = ('sigma', 'sigma_', 'conductiv', 'cond_', 'σ', 'kappa', 'resist',
         'conductance', 'brug', 'tortuosity_laplace', 'tau_laplace')


def _is_circular(k):
    kl = k.lower()
    return any(c in kl for c in _CIRC)


def load():
    rows, feats = [], []
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
            rows.append((phi, cn, cov, fp, tau, float(sig), p))
            feats.append({k: float(v) for k, v in d.items()
                          if isinstance(v, (int, float)) and not isinstance(v, bool)
                          and np.isfinite(v)})
    return np.array(rows, float), feats


def _rank(resid, feats, idx, label):
    keys = set()
    for i in idx:
        keys |= set(feats[i].keys())
    out = []
    for k in keys:
        v = np.array([feats[i].get(k, np.nan) for i in idx])
        m = np.isfinite(v) & np.isfinite(resid[idx])
        if m.sum() >= max(5, int(0.5*len(idx))) and np.std(v[m]) > 1e-12:
            r = float(np.corrcoef(v[m], resid[idx][m])[0, 1])
            out.append((k, r, int(m.sum())))
    out.sort(key=lambda t: -abs(t[1]))
    print(f"\n── {label}  (n={len(idx)}) — top residual correlations ──")
    for k, r, nn in out[:15]:
        flag = ' (*circular?)' if _is_circular(k) else ''
        print(f"   {r:+.3f}  [{nn:2d}]  {k}{flag}")


def main():
    a, feats = load()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    base = base_log_sat(a, PHICP, PHICS, DELTA)
    bv5, bp3 = cblend_fit(base, logsf, taus)
    resid = logsf - cblend_pred(base, taus, bv5, bp3)   # SAT-blend log-residual

    p = a[:, 6]; phi = a[:, 0]
    all_idx = np.arange(n)
    s010 = np.where(p < 0.05)[0]                          # pure AM_S (0:10)
    if len(s010):
        med = np.median(phi[s010])
        s010_rich = s010[phi[s010] >= med]               # SE-rich 0:10 (62:38-type)
    else:
        s010_rich = s010
    print(f"corpus n={n} | 0:10 n={len(s010)} | 0:10 SE-rich n={len(s010_rich)} "
          f"| SAT-blend resid std={resid.std():.3f}")
    _rank(resid, feats, all_idx, "WHOLE corpus")
    if len(s010) >= 6:
        _rank(resid, feats, s010, "0:10 subset (pure AM_S)")
    if len(s010_rich) >= 6:
        _rank(resid, feats, s010_rich, "0:10 SE-rich (62:38-type)")
    print("\n(*circular?) = name implies σ-derived; use only geometric features as predictors.")


if __name__ == "__main__":
    main()
