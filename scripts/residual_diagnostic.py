#!/usr/bin/env python3
"""Residual diagnostic for v32 scaling law.

Scans every case in webapp/archive, computes v32 prediction vs Network-solver
σ_ionic, and correlates the residual (signed %err) against a bank of
candidate features — composition, size, thin-film, packing, v32's own
four features, and name-derived regime flags.

Output:
  1. Residual table, sorted by |err|%
  2. Feature correlations (Pearson) ranked by |corr|
  3. Sub-group breakdown (1mAh vs 6mAh vs 8mAh, thin vs bulk, 80:20 vs rest)
  4. Verdict: is the 1mAh_80:20 P-rich cluster a distinct regime?

Usage:
  python3 scripts/residual_diagnostic.py
"""
from __future__ import annotations
import os, sys, json, math
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

# Reuse v32 prediction machinery from generate_comparison_plots
from generate_comparison_plots import (  # noqa: E402
    _formx_v29_predict, _formx_v29_params, _formx_v32_predict,
    _v32_features_for_case, _ps_fraction,
)

ARCHIVE = Path(__file__).parent.parent / 'webapp' / 'archive'


def parse_ps(s):
    """'7:3' → 0.7 (P fraction). '' → None."""
    if not s or ':' not in str(s):
        return None
    try:
        p, ss = str(s).split(':')
        p, ss = float(p), float(ss)
        return p / (p + ss) if (p + ss) > 0 else None
    except Exception:
        return None


def parse_amse(s):
    """'80:20' → 0.2 (SE fraction)."""
    if not s or ':' not in str(s):
        return None
    try:
        am, se = str(s).split(':')
        am, se = float(am), float(se)
        return se / (am + se) if (am + se) > 0 else None
    except Exception:
        return None


def name_flags(name):
    n = (name or '').lower()
    return {
        'is_1mAh':    '1mah' in n,
        'is_6mAh':    '6mah' in n,
        'is_8mAh':    '8mah' in n,
        'is_thin':    'thin' in n or '1mah' in n,
        'is_particulate': 'particulate' in n,
        'is_real':    'real' in n,
        'is_S_seed':  ('_s1' in n or '_s2' in n or '_s3' in n),
    }


def load_all_cases():
    cases = []
    for meta_path in ARCHIVE.rglob('meta.json'):
        d = meta_path.parent
        fm = d / 'full_metrics.json'
        if not fm.exists():
            continue
        try:
            meta = json.load(open(meta_path))
            m = json.load(open(fm))
        except Exception:
            continue
        m['_source_path'] = str(fm)
        cases.append({
            'case_id':     d.name,
            'name':        meta.get('name', d.name),
            'meta':        meta,
            'metrics':     m,
        })
    return cases


def predict_v32(data, debug=False):
    """Full v32 pipeline: v29 base × v32 exp correction."""
    cfg = _formx_v29_params()
    phi_se    = data.get('phi_se', 0) or 0
    cn        = data.get('se_se_cn', 0) or 0
    tau       = data.get('tortuosity_mean', 0) or 0
    # coverage lookup — try multiple historical key names
    cov = 0
    for k in ('am_se_coverage_elastic_pct', 'coverage_AM_mean',
              'coverage_AM', 'am_se_coverage_pct'):
        v = data.get(k)
        if v is not None and v > 0:
            cov = v
            break
    perc_raw  = data.get('percolation_pct', 0) or 0
    f_perc    = perc_raw / 100.0 if perc_raw > 1 else perc_raw
    ps_frac   = _ps_fraction(data) or 0.7
    gb_dens   = data.get('gb_density_mean', 0) or 0
    if debug:
        print(f'    phi_se={phi_se}  cn={cn}  tau={tau}  cov={cov}  '
              f'f_perc={f_perc}  p_frac={ps_frac}  gb={gb_dens}')
    try:
        v29 = _formx_v29_predict(phi_se, cn, tau, cov, f_perc, ps_frac, gb_dens,
                                 params=cfg)
    except Exception as e:
        if debug: print(f'    v29 raised: {e}')
        return None
    if v29 <= 0 or not np.isfinite(v29):
        if debug: print(f'    v29 returned {v29} (non-positive)')
        return None
    v32 = _formx_v32_predict(v29, data)
    return v32


def main():
    cases = load_all_cases()
    print(f'Loaded {len(cases)} cases from {ARCHIVE}')

    rows = []
    skipped_no_sigma = 0
    skipped_v32_fail = 0
    for c in cases:
        m = c['metrics']
        sig_actual = m.get('sigma_full_mScm')
        if sig_actual is None or sig_actual <= 0:
            skipped_no_sigma += 1
            continue
        sig_v32 = predict_v32(m)
        if sig_v32 is None or sig_v32 <= 0:
            if skipped_v32_fail < 3:
                print(f'  [v32 fail debug] {c["name"]}:')
                predict_v32(m, debug=True)
            skipped_v32_fail += 1
            continue
        err_pct = (sig_actual - sig_v32) / sig_v32 * 100

        flags = name_flags(c['name'])
        feats = _v32_features_for_case(m) or {}
        row = {
            'name':        c['name'],
            'sigma_actual': sig_actual,
            'sigma_v32':    sig_v32,
            'err_pct':      err_pct,
            'abs_err_pct':  abs(err_pct),
            'ps_ratio':     m.get('ps_ratio'),
            'P_frac':       parse_ps(m.get('ps_ratio')),
            'am_se_ratio':  m.get('am_se_ratio'),
            'SE_frac':      parse_amse(m.get('am_se_ratio')),
            'thickness_um': m.get('thickness_um'),
            'porosity':     m.get('porosity'),
            'phi_se':       m.get('phi_se'),
            'se_se_cn':     m.get('se_se_cn'),
            'tortuosity':   m.get('tortuosity_mean'),
            'LIGG_LB_PCT':  feats.get('LIGG_LB_PCT'),
            'THIN_X_GEOM':  feats.get('THIN_X_GEOM'),
            'P50_DR_DEV':   feats.get('P50_DR_DEV'),
            'PSD_RATIO':    feats.get('PSD_RATIO'),
            **flags,
        }
        rows.append(row)

    if not rows:
        print(f'No cases with valid σ and v32 prediction. '
              f'(skipped_no_sigma={skipped_no_sigma}, skipped_v32_fail={skipped_v32_fail})')
        return
    print(f'  → {len(rows)} cases with valid prediction. '
          f'(skipped_no_sigma={skipped_no_sigma}, skipped_v32_fail={skipped_v32_fail})')

    rows.sort(key=lambda r: -r['abs_err_pct'])

    # ── 1. Top residuals ────────────────────────────────────────────────
    print(f'\n=== TOP |err|% (v32 residuals) ===')
    print(f'{"case":40s}  σ_act   σ_v32   err%   P:S    AM:SE  thick  ports')
    for r in rows[:20]:
        flags = []
        if r['is_1mAh']: flags.append('1mAh')
        if r['is_thin']: flags.append('THIN')
        if r['is_S_seed']: flags.append('SEED')
        print(f'{r["name"][:40]:40s}  '
              f'{r["sigma_actual"]:5.3f}  {r["sigma_v32"]:5.3f}  '
              f'{r["err_pct"]:+6.1f}  '
              f'{str(r.get("ps_ratio","-")):5s}  '
              f'{str(r.get("am_se_ratio","-")):6s}  '
              f'{(r["thickness_um"] or 0):5.1f}  '
              f'{",".join(flags)}')

    # ── 2. Feature correlations with err_pct ────────────────────────────
    print(f'\n=== FEATURE CORRELATIONS with signed err% ===')
    num_features = ['P_frac', 'SE_frac', 'thickness_um', 'porosity',
                    'phi_se', 'se_se_cn', 'tortuosity',
                    'LIGG_LB_PCT', 'THIN_X_GEOM', 'P50_DR_DEV', 'PSD_RATIO']
    errs = np.array([r['err_pct'] for r in rows])
    corrs = []
    for f in num_features:
        vals = [r.get(f) for r in rows]
        valid = [(v, e) for v, e in zip(vals, errs) if v is not None and np.isfinite(v)]
        if len(valid) < 3:
            continue
        xs, ys = zip(*valid)
        xs = np.array(xs, float); ys = np.array(ys, float)
        if np.std(xs) == 0:
            continue
        r = float(np.corrcoef(xs, ys)[0, 1])
        corrs.append((f, r, len(valid)))
    corrs.sort(key=lambda x: -abs(x[1]))
    for f, r, n in corrs:
        bar = '█' * int(abs(r) * 30)
        sign = '+' if r > 0 else '-'
        print(f'  {f:15s}  r={r:+.3f}  n={n:3d}  {sign} {bar}')

    # ── 3. Sub-group breakdown ──────────────────────────────────────────
    print(f'\n=== SUB-GROUP MEAN err% ===')
    groups = {
        '1mAh (thin)':      [r for r in rows if r['is_1mAh']],
        '6mAh':             [r for r in rows if r['is_6mAh']],
        '8mAh':             [r for r in rows if r['is_8mAh']],
        'particulate':      [r for r in rows if r['is_particulate']],
        '1mAh & 80:20':     [r for r in rows if r['is_1mAh'] and r.get('am_se_ratio') == '80:20'],
        '1mAh & P≥7:3':     [r for r in rows if r['is_1mAh'] and (r.get('P_frac') or 0) >= 0.7],
        '1mAh & 80:20 & P≥7:3': [r for r in rows if r['is_1mAh'] and r.get('am_se_ratio') == '80:20' and (r.get('P_frac') or 0) >= 0.7],
    }
    print(f'{"group":30s}  n   mean_err%   median   std')
    for gname, gl in groups.items():
        if not gl: continue
        errs_g = np.array([r['err_pct'] for r in gl])
        print(f'{gname:30s}  {len(gl):3d}  {errs_g.mean():+7.2f}    {np.median(errs_g):+6.2f}  {errs_g.std():5.2f}')

    # ── 4. Verdict ──────────────────────────────────────────────────────
    all_err = np.array([r['err_pct'] for r in rows])
    cluster = [r for r in rows if r['is_1mAh'] and r.get('am_se_ratio') == '80:20' and (r.get('P_frac') or 0) >= 0.7]
    print(f'\n=== VERDICT ===')
    print(f'  Global err%:            mean={all_err.mean():+.2f}  std={all_err.std():.2f}  |err|<20%: {np.sum(np.abs(all_err)<20)}/{len(all_err)}')
    if cluster:
        cl_err = np.array([r['err_pct'] for r in cluster])
        z = (cl_err.mean() - all_err.mean()) / (all_err.std() + 1e-9) * math.sqrt(len(cluster))
        print(f'  1mAh_80:20_P-rich:      mean={cl_err.mean():+.2f}  n={len(cluster)}  z-score={z:+.2f}σ vs global')
        if abs(z) > 2:
            print(f'  → CLUSTER is DISTINCT (|z|>2). v32 misses a regime-specific term here.')
        else:
            print(f'  → Cluster within normal scatter. No new term justified.')
    else:
        print(f'  No 1mAh_80:20_P-rich cases found (deleted?).')


if __name__ == '__main__':
    main()
