#!/usr/bin/env python3
"""
One-shot outlier summary report — designed for copy-paste into assistant.

Merges v29 fit results, physics-mode regime attribution, meta.json, and
input_params into a single per-outlier block that captures every signal
needed for diagnosis.

Outputs 3 formats:
  1. stdout (human-readable, terminal)
  2. docs/figures/physics_regime/outlier_summary.md   (markdown, for pasting)
  3. docs/figures/physics_regime/outlier_summary.csv  (spreadsheet)

Usage:
  python3 scripts/outlier_feed_report.py                # outliers only (|err|>20%)
  python3 scripts/outlier_feed_report.py --all          # every case
  python3 scripts/outlier_feed_report.py --threshold 15  # custom |err| cutoff
"""
from __future__ import annotations
import os, json, sys, argparse
from pathlib import Path
import pandas as pd

WEBAPP = Path('webapp')
OUT    = Path('docs/figures/physics_regime')


def load_meta(case_id: str) -> dict:
    for base in (WEBAPP / 'uploads', WEBAPP / 'results'):
        p = base / case_id / 'meta.json'
        if p.exists():
            try:
                return json.load(open(p))
            except Exception:
                pass
    return {}


def load_input_params(case_id: str) -> dict:
    for base in (WEBAPP / 'results', WEBAPP / 'archive'):
        p = base / case_id / 'input_params.json'
        if p.exists():
            try:
                return json.load(open(p))
            except Exception:
                pass
    return {}


def load_full_metrics(case_id: str) -> dict:
    for base in (WEBAPP / 'results', WEBAPP / 'archive'):
        p = base / case_id / 'full_metrics.json'
        if p.exists():
            try:
                return json.load(open(p))
            except Exception:
                pass
    return {}


def build_rows(threshold: float, include_all: bool):
    """Merge v29 fit CSV, regime CSV, and per-case metadata."""
    fit_csv = OUT / 'v29_fit_per_case.csv'
    if not fit_csv.exists():
        sys.exit(f'ERROR: {fit_csv} not found — run v29_outlier_vs_geom.py first')
    fit = pd.read_csv(fit_csv)

    if not include_all:
        fit = fit[fit['abs_err_pct'] > threshold].copy()
    fit = fit.sort_values('abs_err_pct', ascending=False)

    rows = []
    for _, r in fit.iterrows():
        cid = r['case_id']
        meta = load_meta(cid)
        ip   = load_input_params(cid)
        fm   = load_full_metrics(cid)

        rows.append({
            'case_id':        cid,
            'name':           r.get('name') or meta.get('name', cid),
            'mode':           meta.get('mode', '?'),
            'AM:SE':          ip.get('am_se_ratio', '?'),
            'P:S':            meta.get('ps_ratio', '') or '?',
            'scale':          meta.get('scale', '?'),
            'r_AM_P_um':      (ip.get('r_AM_P', 0) * 1000 if ip.get('r_AM_P') else None),
            'r_AM_S_um':      (ip.get('r_AM_S', 0) * 1000 if ip.get('r_AM_S') else None),
            'r_SE_um':        (ip.get('r_SE', 0) * 1000 if ip.get('r_SE') else None),
            'box_x_um':       (ip.get('box_x', 0) * 1000 if ip.get('box_x') else None),
            'box_y_um':       (ip.get('box_y', 0) * 1000 if ip.get('box_y') else None),
            'thickness_um':   round(fm.get('thickness_um', 0) or 0, 1),
            'porosity':       round(fm.get('porosity', 0) or 0, 1),
            'phi_SE':         round(fm.get('phi_se', 0) or 0, 3),
            'σ_actual_mScm':  round(fm.get('sigma_full_mScm', 0) or 0, 4),
            'σ_pred_v29':     round(r.get('sigma_predicted', 0) or 0, 4),
            'err_pct':        round(r.get('err_pct', 0) or 0, 1),
            'abs_err_pct':    round(r.get('abs_err_pct', 0) or 0, 1),
            'τ_Dij':          round(fm.get('tortuosity_mean', 0) or 0, 3),
            'τ_Lap_eff':      fm.get('tortuosity_lap_eff') or fm.get('tau_lap_eff'),
            'SE_SE_CN':       round(fm.get('se_se_cn', 0) or 0, 2),
            'perc_pct':       round(fm.get('percolation_pct', 0) or 0, 1),
            'Ionic_active_AM':round(fm.get('ionic_active_pct', 0) or 0, 1),
            'GB_density':     round(fm.get('gb_density_mean', 0) or 0, 3),
            'p50_dR':         round(r.get('p50_dr', 0) or 0, 3),
            'geom_pct':       round(r.get('geom', 0) or 0, 2),
            'tabor_pct':      round(r.get('tabor', 0) or 0, 1),
            'liggghts_lb_pct':round(r.get('liggghts_lb', 0) or 0, 1),
        })

    return rows


def print_stdout(rows, threshold: float, include_all: bool):
    label = 'ALL cases' if include_all else f'OUTLIERS (|err| > {threshold}%)'
    print(f'\n=== {label} — {len(rows)} cases ===\n')
    for r in rows:
        err_sign = '📈 overshoot' if r['err_pct'] > 0 else '📉 undershoot'
        print(f"  [{r['abs_err_pct']:5.1f}%] {err_sign}  {r['name']}  ({r['case_id']})")
        print(f"    mode={r['mode']}  AM:SE={r['AM:SE']}  P:S={r['P:S']}  "
              f"scale={r['scale']}")
        print(f"    particles  r_AM_P={r['r_AM_P_um']}μm  r_AM_S={r['r_AM_S_um']}μm  "
              f"r_SE={r['r_SE_um']}μm")
        print(f"    geometry   box={r['box_x_um']}×{r['box_y_um']}μm  "
              f"thick={r['thickness_um']}μm  porosity={r['porosity']}%  "
              f"φ_SE={r['phi_SE']}")
        print(f"    σ          actual={r['σ_actual_mScm']}  pred={r['σ_pred_v29']}  "
              f"err={r['err_pct']:+.1f}%")
        print(f"    path       τ_Dij={r['τ_Dij']}  τ_Lap_eff={r['τ_Lap_eff']}  "
              f"CN_SE_SE={r['SE_SE_CN']}  perc={r['perc_pct']}%")
        print(f"    regime     p50_δ/R={r['p50_dR']}  geom={r['geom_pct']}%  "
              f"tabor={r['tabor_pct']}%  liggghts_lb={r['liggghts_lb_pct']}%")
        print()


def write_markdown(rows, out_path: Path, threshold: float, include_all: bool):
    label = 'All cases' if include_all else f'Outliers (|err| > {threshold}%)'
    lines = [f'# v29 FORM X — {label}', '',
             f'Total: **{len(rows)} cases**, sorted by |err| descending.', '']
    for r in rows:
        direction = 'OVERSHOOT' if r['err_pct'] > 0 else 'UNDERSHOOT'
        lines.append(f"## `{r['name']}`  —  |err|={r['abs_err_pct']:.1f}%  {direction}")
        lines.append('')
        lines.append(f'- **case_id**: `{r["case_id"]}`')
        lines.append(f'- **mode**: `{r["mode"]}`, **AM:SE** = {r["AM:SE"]}, '
                     f'**P:S** = {r["P:S"]}, **scale** = {r["scale"]}')
        lines.append(f'- **Particles**: r_AM_P = {r["r_AM_P_um"]} μm, '
                     f'r_AM_S = {r["r_AM_S_um"]} μm, r_SE = {r["r_SE_um"]} μm')
        lines.append(f'- **Geometry**: box {r["box_x_um"]}×{r["box_y_um"]} μm, '
                     f'thickness = {r["thickness_um"]} μm, '
                     f'porosity = {r["porosity"]}%, φ_SE = {r["phi_SE"]}')
        lines.append(f'- **σ_actual** = {r["σ_actual_mScm"]} mS/cm, '
                     f'**σ_pred_v29** = {r["σ_pred_v29"]} mS/cm, '
                     f'**err** = {r["err_pct"]:+.1f}%')
        lines.append(f'- **Path**: τ_Dij = {r["τ_Dij"]}, τ_Lap_eff = {r["τ_Lap_eff"]}, '
                     f'SE-SE CN = {r["SE_SE_CN"]}, percolation = {r["perc_pct"]}%, '
                     f'ionic-active AM = {r["Ionic_active_AM"]}%')
        lines.append(f'- **Regime**: p50 δ/R* = {r["p50_dR"]}, '
                     f'geom cap = {r["geom_pct"]}%, tabor = {r["tabor_pct"]}%, '
                     f'liggghts_lb = {r["liggghts_lb_pct"]}%')
        lines.append(f'- **GB density** = {r["GB_density"]} hops/μm')
        lines.append('')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(lines))
    print(f'→ {out_path}')


def write_csv(rows, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f'→ {out_path}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--threshold', type=float, default=20.0,
                    help='|err%%| cutoff (default 20)')
    ap.add_argument('--all', action='store_true',
                    help='Include every case, not just outliers')
    args = ap.parse_args()

    rows = build_rows(args.threshold, args.all)
    if not rows:
        print('No cases match criteria.')
        return

    print_stdout(rows, args.threshold, args.all)

    suffix = 'all' if args.all else f'outliers_{int(args.threshold)}pct'
    write_markdown(rows, OUT / f'outlier_summary_{suffix}.md',
                   args.threshold, args.all)
    write_csv(rows, OUT / f'outlier_summary_{suffix}.csv')


if __name__ == '__main__':
    main()
