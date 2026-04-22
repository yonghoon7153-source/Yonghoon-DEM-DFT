#!/usr/bin/env python3
"""
Coverage computed in BOTH Hertzian (LIGGGHTS contact_area) and Physics
(Tabor A = F_real/H with caps) modes for every AM particle.

Addresses two open questions:
  • H1: does plastic deformation change AM surface coverage?
        (dual-mode values per case → Δ% reported)
  • COMSOL input: per-AM A_AM_SE for electrochemically-active area
        (one CSV row per AM particle with both mode values)

Per case outputs:
  • full_metrics.json — adds coverage_AM_P_mean_physics,
                         coverage_AM_S_mean_physics,
                         coverage_AM_mean_physics (+ std)
  • coverage_per_am.csv — one row per AM particle:
        am_id, am_type, radius_um, surface_area_um2,
        A_AM_SE_hertzian_um2, A_AM_SE_physics_um2,
        coverage_hertzian_pct, coverage_physics_pct,
        delta_pct_physics_vs_hertzian

Usage:
  python3 scripts/coverage_physics_vs_hertzian.py <case_id>
  python3 scripts/coverage_physics_vs_hertzian.py --all
"""
from __future__ import annotations
import os, sys, json, argparse
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from plastic_coverage import film_area_from_overlap  # noqa: E402

WEBAPP = Path(__file__).parent.parent / 'webapp'


def find_case_dir(cid: str) -> Path | None:
    for base in ('results', 'archive'):
        p = WEBAPP / base / cid
        if p.exists() and (p / 'atoms.csv').exists() and (p / 'contacts.csv').exists():
            return p
    return None


def load_meta(cid: str) -> dict:
    for base in ('uploads', 'results'):
        m = WEBAPP / base / cid / 'meta.json'
        if m.exists():
            try:
                return json.load(open(m))
            except Exception:
                pass
    return {}


def parse_type_map(s: str) -> dict:
    tm = {}
    for pair in (s or '').split(','):
        if ':' in pair:
            k, v = pair.split(':', 1)
            try:
                tm[int(k.strip())] = v.strip()
            except ValueError:
                pass
    return tm


def compute_case(cid: str, case_dir: Path, type_map: dict, scale: float = 1000.0,
                 write_csv: bool = True, update_metrics: bool = True,
                 verbose: bool = False) -> dict:
    """Compute per-AM coverage in Hertzian and Physics modes, return summary dict."""
    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)

    # Index radii and types by id
    id_to_r = dict(zip(atoms_df['id'].astype(int), atoms_df['radius'].astype(float)))
    id_to_t = dict(zip(atoms_df['id'].astype(int), atoms_df['type'].astype(int)))

    am_types = [k for k, v in type_map.items() if 'AM' in v]
    se_types = [k for k, v in type_map.items() if v == 'SE']

    # Per-AM surface area (sim units, m²)
    am_surf = {}
    for aid, r in id_to_r.items():
        if id_to_t.get(aid) in am_types:
            am_surf[aid] = 4.0 * np.pi * r * r

    # Scan ALL contacts: compute both A_hertzian and A_physics per AM particle
    # AND global sums (AM-SE total, SE-SE total, AM-AM total).
    am_se_hertz = defaultdict(float)   # per-AM AM-SE Hertzian area (sim m²)
    am_se_phys  = defaultdict(float)   # per-AM AM-SE Physics area (sim m²)
    am_am_hertz = defaultdict(float)   # per-AM AM-AM area (for free-surface deduction)

    # Per-AM-type buckets for totals (used by UI rows "AM-SE Total" etc.)
    total_am_se_h = 0.0
    total_am_se_p = 0.0
    total_se_se_h = 0.0
    total_se_se_p = 0.0
    total_am_am_h = 0.0
    total_am_am_p = 0.0

    for _, c in contacts_df.iterrows():
        i1, i2 = int(c['id1']), int(c['id2'])
        if i1 not in id_to_t or i2 not in id_to_t:
            continue
        t1, t2 = id_to_t[i1], id_to_t[i2]
        r1 = id_to_r[i1]; r2 = id_to_r[i2]
        delta_sim = float(c.get('delta', 0) or 0)
        A_ligg_sim = float(c.get('contact_area', 0) or 0)
        R_star = (r1 * r2) / (r1 + r2) if (r1 + r2) > 0 else 0
        R_min = min(r1, r2)
        A_phys_sim = A_ligg_sim
        if delta_sim > 0 and R_star > 0 and R_min > 0:
            try:
                A_p, _regime = film_area_from_overlap(
                    delta_sim, R_star, R_min=R_min,
                    ligg_area=A_ligg_sim, mode='physics')
                A_phys_sim = A_p
            except Exception:
                pass

        # Bucket by contact-type pair
        am1 = t1 in am_types;  am2 = t2 in am_types
        se1 = t1 in se_types;  se2 = t2 in se_types

        if (am1 and se2) or (am2 and se1):
            total_am_se_h += A_ligg_sim
            total_am_se_p += A_phys_sim
            if am1:
                am_se_hertz[i1] += A_ligg_sim
                am_se_phys[i1]  += A_phys_sim
            else:
                am_se_hertz[i2] += A_ligg_sim
                am_se_phys[i2]  += A_phys_sim
        elif se1 and se2:
            total_se_se_h += A_ligg_sim
            total_se_se_p += A_phys_sim
        elif am1 and am2:
            total_am_am_h += A_ligg_sim
            total_am_am_p += A_phys_sim
            am_am_hertz[i1] += A_ligg_sim
            am_am_hertz[i2] += A_ligg_sim

    # Per-AM coverage (% of non-AM-occluded surface) + per-AM CSV
    # Convert to μm²: multiply by scale² (if sim units are m and scale=1000)
    area_conv = scale * scale  # sim m² → μm²
    rows = []
    covs_by_type = defaultdict(lambda: {'hertz': [], 'phys': []})
    for aid, r_sim in id_to_r.items():
        t = id_to_t.get(aid)
        if t not in am_types:
            continue
        lbl = type_map.get(t, f'T{t}')
        surf = am_surf.get(aid, 0.0)
        am_am = am_am_hertz.get(aid, 0.0)
        free = max(surf - am_am, 0.0)
        A_h = am_se_hertz.get(aid, 0.0)
        A_p = am_se_phys.get(aid, 0.0)
        cov_h = min(A_h / free * 100, 100.0) if free > 0 else 0.0
        cov_p = min(A_p / free * 100, 100.0) if free > 0 else 0.0
        covs_by_type[lbl]['hertz'].append(cov_h)
        covs_by_type[lbl]['phys'].append(cov_p)
        rows.append({
            'am_id': aid,
            'am_type': lbl,
            'radius_um': round(r_sim * scale, 3),
            'surface_area_um2':       round(surf * area_conv, 3),
            'A_AM_SE_hertzian_um2':   round(A_h * area_conv, 4),
            'A_AM_SE_physics_um2':    round(A_p * area_conv, 4),
            'coverage_hertzian_pct':  round(cov_h, 3),
            'coverage_physics_pct':   round(cov_p, 3),
            'delta_pct_physics_vs_hertzian': round(
                ((cov_p - cov_h) / cov_h * 100) if cov_h > 0 else 0, 2),
        })

    # Summary
    summary = {}
    for lbl, arrs in covs_by_type.items():
        if not arrs['hertz']:
            continue
        h = np.array(arrs['hertz'])
        p = np.array(arrs['phys'])
        summary[lbl] = {
            'n':              int(len(h)),
            'hertzian_mean':  float(np.mean(h)),
            'hertzian_std':   float(np.std(h)),
            'physics_mean':   float(np.mean(p)),
            'physics_std':    float(np.std(p)),
            'delta_mean_pct': float((np.mean(p) - np.mean(h)) / np.mean(h) * 100)
                                if np.mean(h) > 0 else 0.0,
        }

    # Write per-AM CSV
    if write_csv and rows:
        df_out = pd.DataFrame(rows)
        csv_path = case_dir / 'coverage_per_am.csv'
        df_out.to_csv(csv_path, index=False)
        if verbose:
            print(f'  → {csv_path}  ({len(df_out)} AM particles)')

    # Update full_metrics.json
    if update_metrics:
        fm_path = case_dir / 'full_metrics.json'
        if fm_path.exists():
            try:
                m = json.load(open(fm_path))
                for lbl, s in summary.items():
                    base = f'coverage_{lbl}'
                    m[f'{base}_mean_physics']    = round(s['physics_mean'], 3)
                    m[f'{base}_std_physics']     = round(s['physics_std'], 3)
                    m[f'{base}_delta_pct_physics'] = round(s['delta_mean_pct'], 2)
                # Aggregate total-AM coverage ("coverage_AM_mean_physics")
                all_h = [v for arrs in covs_by_type.values() for v in arrs['hertz']]
                all_p = [v for arrs in covs_by_type.values() for v in arrs['phys']]
                if all_h:
                    m['coverage_AM_mean_physics'] = round(float(np.mean(all_p)), 3)
                    m['coverage_AM_delta_pct_physics'] = round(
                        float((np.mean(all_p) - np.mean(all_h)) /
                              max(np.mean(all_h), 1e-9) * 100), 2)
                # Global area totals (Physics mode) — feeds UI rows
                #   "AM-SE Total(μm²)" and "SE-SE Total(μm²)".
                # Keys match the existing Hertzian keys + _physics suffix.
                m['area_AM전체_SE_total_physics'] = round(total_am_se_p * area_conv, 2)
                m['area_SE_SE_total_physics']    = round(total_se_se_p * area_conv, 2)
                m['area_AM전체_AM_total_physics'] = round(total_am_am_p * area_conv, 2)
                # Δ% (reference): only meaningful if Hertzian total > 0
                if total_am_se_h > 0:
                    m['area_AM전체_SE_total_delta_pct_physics'] = round(
                        (total_am_se_p - total_am_se_h) / total_am_se_h * 100, 2)
                if total_se_se_h > 0:
                    m['area_SE_SE_total_delta_pct_physics'] = round(
                        (total_se_se_p - total_se_se_h) / total_se_se_h * 100, 2)
                with open(fm_path, 'w') as f:
                    json.dump(m, f, indent=2, default=str)
                if verbose:
                    print(f'  → {fm_path}  (updated physics keys)')
                    print(f'    AM-SE total: H={total_am_se_h*area_conv:,.1f}  '
                          f'P={total_am_se_p*area_conv:,.1f}  '
                          f'Δ={(total_am_se_p/total_am_se_h-1)*100 if total_am_se_h else 0:+.1f}%')
                    print(f'    SE-SE total: H={total_se_se_h*area_conv:,.1f}  '
                          f'P={total_se_se_p*area_conv:,.1f}  '
                          f'Δ={(total_se_se_p/total_se_se_h-1)*100 if total_se_se_h else 0:+.1f}%')
            except Exception as e:
                print(f'  [warn] failed to update full_metrics.json: {e}')

    return summary


def process_one(cid: str, *, verbose: bool = False) -> dict | None:
    case_dir = find_case_dir(cid)
    if case_dir is None:
        print(f'  [skip] {cid}: no atoms.csv/contacts.csv')
        return None
    meta = load_meta(cid)
    type_map = parse_type_map(meta.get('type_map', ''))
    scale = meta.get('scale', 1000)
    if not type_map:
        print(f'  [skip] {cid}: no type_map in meta.json')
        return None
    name = meta.get('name', cid)
    if verbose:
        print(f'\n=== {name}  ({cid}) ===')
    return compute_case(cid, case_dir, type_map, scale=scale, verbose=verbose)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*', help='case_id(s) to process')
    ap.add_argument('--all', action='store_true',
                    help='Process every case in webapp/results and webapp/archive')
    args = ap.parse_args()

    cases: list[str] = []
    if args.all:
        for base in ('results', 'archive'):
            root = WEBAPP / base
            if root.exists():
                for d in sorted(root.iterdir()):
                    if d.is_dir() and (d / 'atoms.csv').exists() and (d / 'contacts.csv').exists():
                        cases.append(d.name)
    cases.extend(args.cases)
    cases = list(dict.fromkeys(cases))  # dedup, preserve order

    if not cases:
        ap.error('No cases selected. Pass case_id(s) or use --all.')

    print(f'Processing {len(cases)} case(s) ...')
    summary_rows = []
    for cid in cases:
        s = process_one(cid, verbose=True)
        if s is None:
            continue
        meta = load_meta(cid)
        nm = meta.get('name', cid)
        for lbl, v in s.items():
            print(f'  {nm:34s} {lbl:5s}  H={v["hertzian_mean"]:5.2f}%  '
                  f'P={v["physics_mean"]:5.2f}%  '
                  f'Δ={v["delta_mean_pct"]:+6.2f}%  n={v["n"]}')
            summary_rows.append({
                'case_id': cid, 'name': nm, 'am_type': lbl,
                'n_AM': v['n'],
                'cov_hertzian_pct': round(v['hertzian_mean'], 3),
                'cov_physics_pct':  round(v['physics_mean'], 3),
                'delta_pct':        round(v['delta_mean_pct'], 2),
            })

    if summary_rows:
        out_dir = Path('docs/figures/physics_regime')
        out_dir.mkdir(parents=True, exist_ok=True)
        out_csv = out_dir / 'coverage_hertz_vs_physics_summary.csv'
        pd.DataFrame(summary_rows).to_csv(out_csv, index=False)
        print(f'\n→ {out_csv}  ({len(summary_rows)} rows)')

        # Quick stats
        df = pd.DataFrame(summary_rows)
        print('\n=== Summary (Δ coverage % : physics vs hertzian) ===')
        for lbl, sub in df.groupby('am_type'):
            print(f'  {lbl:5s}  n_cases={len(sub):3d}  '
                  f'Δ median={sub["delta_pct"].median():+6.2f}%  '
                  f'mean={sub["delta_pct"].mean():+6.2f}%  '
                  f'max={sub["delta_pct"].abs().max():6.2f}%')

        # Verdict
        mean_all = df['delta_pct'].mean()
        print(f'\nVERDICT: Across all AM types and cases, '
              f'coverage in Physics mode differs from Hertzian by '
              f'mean Δ = {mean_all:+.2f}%.')


if __name__ == '__main__':
    main()
