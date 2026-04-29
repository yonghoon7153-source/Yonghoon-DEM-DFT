#!/usr/bin/env python3
"""B2 + B4 diagnostic — AM-AM area dominance + AM-AM overlap variation.

Two diagnostics to settle whether B2 (AM-AM area subtraction) and B4
(AM deformation) are model-noise-level or critical:

  B2 diagnostic: For each case, compute per-AM
    • AM-AM contact area total
    • AM total surface = 4π R²
    • Ratio = AM-AM contact / total surface
  Aggregate across all 76+ cases. If most AMs show <5% AM-AM area,
  B2 is noise-level. If 10%+ AMs have >20% AM-AM area, B2 is critical.

  B4 diagnostic: For each AM-AM contact in the dataset
    • Hertzian overlap δ
    • Hertzian overlap ratio δ/R_min
  Distribution across cases. If max(δ/R) < 0.005, AM essentially rigid
  (plastic regime starts at ~0.0011 per Tabor). If significant fraction
  exceeds 0.005, AM deforming → B4 matters.
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from collections import defaultdict

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from fracture_model import (                                # noqa: E402
    fracture_classify_sim, fracture_classify_force_sim,
    ALL_STAGES, STAGE_RANK, worse,
)
warnings.filterwarnings('ignore')

WEBAPP = SCRIPTS.parent / 'webapp'

# Per-case `scale` (sim units → metres) is read from meta.json. Default
# matches existing pipeline (1 sim unit = 1 mm = 1000 m^-1).
DEFAULT_SCALE = 1000.0


def parse_type_map(s):
    out = {}
    for tok in s.split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try: out[int(k.strip())] = v.strip()
            except: pass
    return out


def find_case_dir(cid):
    for base in ('webapp/results', 'webapp/archive'):
        for p in Path(base).rglob(f'{cid}'):
            if p.is_dir() and (p / 'atoms.csv').exists():
                return p
    return None


def diagnose_one_case(case_dir, type_map, scale=DEFAULT_SCALE):
    """Return dict with per-AM stats for B2 + B4 + brittle fracture stage."""
    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)

    # AM types in this case
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in lbl}
    se_types = {tid for tid, lbl in type_map.items() if lbl == 'SE'}

    # Per-AM info — track *worst* fracture stage encountered per particle
    am_info = {}
    for _, row in atoms_df.iterrows():
        if int(row['type']) in am_types:
            r = float(row['radius'])
            am_info[int(row['id'])] = {
                'radius': r,
                'surface': 4 * np.pi * r ** 2,
                'am_am_area': 0.0,
                'am_se_area': 0.0,
                'am_am_overlap_max': 0.0,
                'am_am_overlap_count': 0,
                'type': type_map[int(row['type'])],
                'worst_stage': 'intact',
                'worst_mult':  0.0,
            }

    # ── Per-contact fracture-stage tally (Auerbach + Lawn) ─────────────
    # Two parallel classifications:
    #   δ-based  : uses LIGGGHTS overlap, Hertzian-equivalent (legacy)
    #   force-based : uses LIGGGHTS fn directly, model-agnostic (primary)
    am_am_overlaps = []
    stage_counts = {f'n_{s}_AM_AM': 0 for s in ALL_STAGES}
    stage_counts_force = {f'n_{s}_force_AM_AM': 0 for s in ALL_STAGES}
    pair_stage_counts = {pt: {s: 0 for s in ALL_STAGES}
                         for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S')}
    pair_stage_counts_force = {pt: {s: 0 for s in ALL_STAGES}
                                for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S')}
    # Per-pair-type R_min, P_c, F samples for paper Section 2 footnote
    pair_samples = {pt: {'R_min_sim': [], 'P_c_N': [], 'F_N': []}
                    for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S')}

    for _, c in contacts_df.iterrows():
        i1, i2 = int(c['id1']), int(c['id2'])
        if i1 not in am_info and i2 not in am_info: continue
        atype1 = atoms_df[atoms_df['id'] == i1].iloc[0] if (atoms_df['id'] == i1).any() else None
        atype2 = atoms_df[atoms_df['id'] == i2].iloc[0] if (atoms_df['id'] == i2).any() else None
        if atype1 is None or atype2 is None: continue
        t1, t2 = int(atype1['type']), int(atype2['type'])
        area = float(c.get('contact_area', 0) or 0)
        delta = float(c.get('delta', 0) or 0)

        if t1 in am_types and t2 in am_types:
            # AM-AM contact
            r1 = am_info[i1]['radius']; r2 = am_info[i2]['radius']
            r_min = min(r1, r2)
            am_info[i1]['am_am_area'] += area
            am_info[i2]['am_am_area'] += area
            if delta > 0 and r_min > 0:
                ratio = delta / r_min
                am_am_overlaps.append(ratio)
                am_info[i1]['am_am_overlap_count'] += 1
                am_info[i2]['am_am_overlap_count'] += 1
                am_info[i1]['am_am_overlap_max'] = max(
                    am_info[i1]['am_am_overlap_max'], ratio)
                am_info[i2]['am_am_overlap_max'] = max(
                    am_info[i2]['am_am_overlap_max'], ratio)

                # Brittle fracture stage classification — δ-based (legacy)
                pair_label = '-'.join(sorted([am_info[i1]['type'],
                                               am_info[i2]['type']]))
                stage, _dc, mult = fracture_classify_sim(
                    delta, r_min, contact_type=pair_label, scale=scale)
                stage_counts[f'n_{stage}_AM_AM'] += 1
                if pair_label in pair_stage_counts:
                    pair_stage_counts[pair_label][stage] += 1
                # Track per-particle worst stage (δ-based)
                for pid in (i1, i2):
                    if STAGE_RANK[stage] > STAGE_RANK[am_info[pid]['worst_stage']]:
                        am_info[pid]['worst_stage'] = stage
                        am_info[pid]['worst_mult']  = mult

                # ── Force-based classification (primary) ──
                # Read fn (normal force) — LIGGGHTS reports SI Newtons.
                fn = float(c.get('fn', 0) or 0)
                if fn <= 0:
                    fn = ((c.get('fn_x', 0) or 0) ** 2
                          + (c.get('fn_y', 0) or 0) ** 2
                          + (c.get('fn_z', 0) or 0) ** 2) ** 0.5
                if fn > 0:
                    stage_f, P_c_N, _mult_f = fracture_classify_force_sim(
                        fn, r_min, contact_type=pair_label, scale=scale)
                    stage_counts_force[f'n_{stage_f}_force_AM_AM'] += 1
                    if pair_label in pair_stage_counts_force:
                        pair_stage_counts_force[pair_label][stage_f] += 1
                    # Per-pair-type R_min, P_c, F samples (Section 2 footnote)
                    if pair_label in pair_samples:
                        pair_samples[pair_label]['R_min_sim'].append(r_min)
                        pair_samples[pair_label]['P_c_N'].append(P_c_N)
                        pair_samples[pair_label]['F_N'].append(fn)

        elif (t1 in am_types and t2 in se_types) or \
             (t2 in am_types and t1 in se_types):
            am_id = i1 if t1 in am_types else i2
            am_info[am_id]['am_se_area'] += area

    # Per-AM ratios
    ratios_AMP = []; ratios_AMS = []
    worst_mult_AMP = []; worst_mult_AMS = []
    for aid, info in am_info.items():
        if info['surface'] <= 0: continue
        r = info['am_am_area'] / info['surface']
        if info['type'] == 'AM_P':
            ratios_AMP.append(r)
            worst_mult_AMP.append(info['worst_mult'])
        elif info['type'] == 'AM_S':
            ratios_AMS.append(r)
            worst_mult_AMS.append(info['worst_mult'])

    n_total_amam = sum(stage_counts.values()) or 1
    n_total_amam_force = sum(stage_counts_force.values()) or 1
    out = {
        'n_AMP': len(ratios_AMP),
        'n_AMS': len(ratios_AMS),
        'AMP_amam_ratio_mean':   float(np.mean(ratios_AMP))   if ratios_AMP else None,
        'AMP_amam_ratio_median': float(np.median(ratios_AMP)) if ratios_AMP else None,
        'AMP_amam_ratio_max':    float(np.max(ratios_AMP))    if ratios_AMP else None,
        'AMS_amam_ratio_mean':   float(np.mean(ratios_AMS))   if ratios_AMS else None,
        'AMS_amam_ratio_median': float(np.median(ratios_AMS)) if ratios_AMS else None,
        'AMS_amam_ratio_max':    float(np.max(ratios_AMS))    if ratios_AMS else None,
        'am_am_overlap_n':       len(am_am_overlaps),
        'am_am_overlap_max':     float(np.max(am_am_overlaps))    if am_am_overlaps else 0.0,
        'am_am_overlap_median':  float(np.median(am_am_overlaps)) if am_am_overlaps else 0.0,
        'am_am_overlap_p95':     float(np.percentile(am_am_overlaps, 95))
                                  if am_am_overlaps else 0.0,
        # ── Brittle fracture stage counts (Auerbach + Lawn 1998) ──
        **stage_counts,
        'n_total_AM_AM':                 n_total_amam,
        'frac_microcrack_pct':           round(100.0 * stage_counts['n_microcrack_AM_AM']    / n_total_amam, 2),
        'frac_multicrack_pct':           round(100.0 * stage_counts['n_multicrack_AM_AM']    / n_total_amam, 2),
        'frac_fragmentation_pct':        round(100.0 * stage_counts['n_fragmentation_AM_AM'] / n_total_amam, 2),
        'frac_pulverization_pct':        round(100.0 * stage_counts['n_pulverization_AM_AM'] / n_total_amam, 2),
        # Severity index = (n_fragmentation + n_pulverization) / n_total
        'fracture_index':                round(
            (stage_counts['n_fragmentation_AM_AM'] +
             stage_counts['n_pulverization_AM_AM']) / n_total_amam, 4),
        # Per-AM worst-stage statistics
        'AMP_worst_mult_median':  float(np.median(worst_mult_AMP)) if worst_mult_AMP else None,
        'AMP_worst_mult_max':     float(np.max(worst_mult_AMP))    if worst_mult_AMP else None,
        'AMS_worst_mult_median':  float(np.median(worst_mult_AMS)) if worst_mult_AMS else None,
        'AMS_worst_mult_max':     float(np.max(worst_mult_AMS))    if worst_mult_AMS else None,
    }
    # Per-pair-type breakdown columns (δ-based)
    for pt, sc in pair_stage_counts.items():
        n_pair = sum(sc.values()) or 1
        for s, n in sc.items():
            out[f'n_{s}_{pt}']            = n
            out[f'frac_{s}_{pt}_pct']     = round(100.0 * n / n_pair, 2)
        out[f'n_total_{pt}'] = sum(sc.values())

    # ── Force-based aggregate columns ────────────────────────
    out.update(stage_counts_force)
    out['n_total_AM_AM_force'] = n_total_amam_force
    out['frac_microcrack_force_pct']    = round(100.0 * stage_counts_force['n_microcrack_force_AM_AM']    / n_total_amam_force, 2)
    out['frac_multicrack_force_pct']    = round(100.0 * stage_counts_force['n_multicrack_force_AM_AM']    / n_total_amam_force, 2)
    out['frac_fragmentation_force_pct'] = round(100.0 * stage_counts_force['n_fragmentation_force_AM_AM'] / n_total_amam_force, 2)
    out['frac_pulverization_force_pct'] = round(100.0 * stage_counts_force['n_pulverization_force_AM_AM'] / n_total_amam_force, 2)
    out['fracture_index_force'] = round(
        (stage_counts_force['n_fragmentation_force_AM_AM'] +
         stage_counts_force['n_pulverization_force_AM_AM']) / n_total_amam_force, 4)
    # Force-based per-pair-type breakdown
    for pt, sc in pair_stage_counts_force.items():
        n_pair = sum(sc.values()) or 1
        for s, n in sc.items():
            out[f'n_{s}_force_{pt}']        = n
            out[f'frac_{s}_force_{pt}_pct'] = round(100.0 * n / n_pair, 2)
        out[f'n_total_force_{pt}'] = sum(sc.values())

    # Per-pair-type R_min / P_c / F medians (paper Section 2 footnote)
    # All in SI: μm, mN.
    for pt, samples in pair_samples.items():
        if samples['R_min_sim']:
            r_um = float(np.median(samples['R_min_sim']) / scale * 1e6)
            out[f'R_min_um_median_{pt}']   = round(r_um, 3)
        if samples['P_c_N']:
            out[f'P_c_mN_median_{pt}']     = round(float(np.median(samples['P_c_N']) * 1e3), 4)
        if samples['F_N']:
            out[f'F_mN_median_{pt}']       = round(float(np.median(samples['F_N']) * 1e3), 4)
            if samples['P_c_N']:
                ratios = [f / p for f, p in zip(samples['F_N'], samples['P_c_N']) if p > 0]
                if ratios:
                    out[f'F_over_Pc_median_{pt}'] = round(float(np.median(ratios)), 3)
    return out


def main():
    paths = list(Path('webapp/results').glob('*/full_metrics.json')) + \
            list(Path('webapp/archive').rglob('*/full_metrics.json'))
    case_ids = list({p.parent.name for p in paths})
    print(f'Diagnosing B2+B4 across {len(case_ids)} cases...', flush=True)

    all_results = []
    n_processed = 0
    for cid in case_ids:
        case_dir = find_case_dir(cid)
        if case_dir is None: continue
        # type_map
        meta_p = case_dir / 'meta.json'
        if not meta_p.exists():
            up = WEBAPP / 'uploads' / cid / 'meta.json'
            meta_p = up if up.exists() else None
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
        scale = DEFAULT_SCALE
        if meta_p:
            try:
                m = json.load(open(meta_p))
                tm = parse_type_map(m.get('type_map', ''))
                if tm: type_map = tm
                scale = float(m.get('scale', DEFAULT_SCALE))
            except Exception: pass
        try:
            r = diagnose_one_case(case_dir, type_map, scale=scale)
            r['case_id'] = cid
            all_results.append(r)
            n_processed += 1
        except Exception as e:
            print(f'  {cid}: {e}', flush=True)
        if n_processed % 20 == 0 and n_processed > 0:
            print(f'  {n_processed}/{len(case_ids)} processed', flush=True)

    print(f'\n  successfully diagnosed: {len(all_results)} cases', flush=True)

    df = pd.DataFrame(all_results)

    # ── B2 summary ────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('B2 DIAGNOSTIC — AM-AM area / AM total surface ratio', flush=True)
    print('=' * 80, flush=True)
    print('\nAcross all cases, mean AM-AM area / total surface ratio:', flush=True)
    for col, label in [('AMP_amam_ratio_mean', 'AM_P (polycryst, large)'),
                        ('AMS_amam_ratio_mean', 'AM_S (single cryst, small)')]:
        v = df[col].dropna().values
        if len(v) == 0: continue
        print(f'  {label:30s}  median = {np.median(v):.3f}  '
              f'mean = {v.mean():.3f}  max = {v.max():.3f}', flush=True)

    print('\n  Verdict — B2 dominance:', flush=True)
    amp_mean = df['AMP_amam_ratio_mean'].dropna().mean()
    ams_mean = df['AMS_amam_ratio_mean'].dropna().mean()
    print(f'    AM_P mean ratio: {amp_mean:.3f}', flush=True)
    print(f'    AM_S mean ratio: {ams_mean:.3f}', flush=True)
    if amp_mean > 0.20 or ams_mean > 0.20:
        print('    🔴 AM-AM contact area > 20% of surface — B2 critical, '
              'need refined model.', flush=True)
    elif amp_mean > 0.10 or ams_mean > 0.10:
        print('    🟡 AM-AM area significant (10-20%) — B2 worth refining.',
              flush=True)
    else:
        print('    🟢 AM-AM area < 10% — B2 is noise-level, current '
              'subtraction acceptable.', flush=True)

    # ── B4 summary ────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('B4 DIAGNOSTIC — AM-AM overlap (δ/R) variation', flush=True)
    print('=' * 80, flush=True)
    print('\nAM-AM Hertzian overlap distribution (δ/R_min):', flush=True)
    print(f'  Plastic regime starts at ~0.0011 (Tabor yield)', flush=True)
    print(f'  Fully plastic: ~0.0078\n', flush=True)
    overlaps = df['am_am_overlap_median'].dropna().values
    overlaps_max = df['am_am_overlap_max'].dropna().values
    overlaps_p95 = df['am_am_overlap_p95'].dropna().values
    if len(overlaps) > 0:
        print(f'  per-case median overlap:  '
              f'{np.median(overlaps):.4f} (median across cases)', flush=True)
        print(f'  per-case max overlap:     '
              f'{np.median(overlaps_max):.4f} (median across cases)',
              flush=True)
        print(f'  per-case 95th-percentile: '
              f'{np.median(overlaps_p95):.4f} (median across cases)',
              flush=True)
        print(f'  GLOBAL maximum across all cases: '
              f'{overlaps_max.max():.4f}', flush=True)

        n_yielded = (df['am_am_overlap_max'] > 0.0011).sum()
        n_plastic = (df['am_am_overlap_max'] > 0.0078).sum()
        print(f'\n  Cases with at least one AM-AM contact in:', flush=True)
        print(f'    elastic-plastic transition (δ/R > 0.0011): '
              f'{n_yielded}/{len(df)}', flush=True)
        print(f'    fully plastic regime       (δ/R > 0.0078): '
              f'{n_plastic}/{len(df)}', flush=True)
        print(f'\n  Verdict — B4 (AM deformation):', flush=True)
        if n_plastic > len(df) * 0.3:
            print('    🔴 AM significantly deforming in many cases — '
                  'B4 critical, soft AM assumption wrong.', flush=True)
        elif n_yielded > len(df) * 0.5:
            print('    🟡 AM at yield onset frequently — B4 mild '
                  'consideration.', flush=True)
        else:
            print('    🟢 AM mostly elastic — B4 minor, current rigid-AM '
                  'assumption acceptable.', flush=True)

    # ── Brittle-fracture summary (Auerbach + Lawn 1998) ───────────────
    print('\n' + '=' * 80, flush=True)
    print('B4-REFRAME — Auerbach/Lawn brittle fracture stage distribution',
          flush=True)
    print('=' * 80, flush=True)
    print('\nReinterpret AM-AM δ/R as fracture-likelihood proxy '
          '(physically, NCM ceramic fractures rather than penetrating).',
          flush=True)
    print('Stages — intact / microcrack / multicrack / fragmentation / pulverization',
          flush=True)

    n_total_amam = df['n_total_AM_AM'].sum()
    if n_total_amam > 0:
        print(f'\n  Aggregate over all {len(df)} cases '
              f'({int(n_total_amam):,} AM-AM contacts):', flush=True)
        for s in ('intact', 'microcrack', 'multicrack',
                   'fragmentation', 'pulverization'):
            col = f'n_{s}_AM_AM'
            if col not in df.columns: continue
            tot = int(df[col].sum())
            pct = 100.0 * tot / max(n_total_amam, 1)
            print(f'    {s:14s}  {tot:>8,d}  ({pct:5.1f}%)', flush=True)

        idx = df['fracture_index'].dropna()
        if len(idx) > 0:
            print(f'\n  fracture_index = (n_fragmentation + n_pulverization) / n_total:',
                  flush=True)
            print(f'    median across cases:  {np.median(idx):.3f}', flush=True)
            print(f'    mean across cases:    {np.mean(idx):.3f}',   flush=True)
            print(f'    max across cases:     {np.max(idx):.3f}',    flush=True)

        # Per-pair-type breakdown headline
        print(f'\n  Severity (fragmentation+pulverization %) by pair type:',
              flush=True)
        for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
            col_frag = f'n_fragmentation_{pt}'
            col_pul  = f'n_pulverization_{pt}'
            col_tot  = f'n_total_{pt}'
            if col_tot not in df.columns: continue
            tot = df[col_tot].sum()
            if tot <= 0: continue
            sev_pct = 100.0 * (df[col_frag].sum() + df[col_pul].sum()) / tot
            print(f'    {pt:12s}  {sev_pct:5.1f}%  '
                  f'(of {int(tot):,} contacts)', flush=True)

        print(f'\n  Verdict — Brittle reframe (δ-based):', flush=True)
        median_idx = float(np.median(idx)) if len(idx) > 0 else 0
        if median_idx > 0.30:
            print('    🔴 Median fracture_index > 30% — DEM ensembles severely '
                  'over-overlap; reframe + paper caveat mandatory.',
                  flush=True)
        elif median_idx > 0.10:
            print('    🟡 Median fracture_index 10-30% — reframe recommended.',
                  flush=True)
        else:
            print('    🟢 Median fracture_index < 10% — minor caveat suffices.',
                  flush=True)

    # ── Force-based parallel summary ──
    n_total_force = df['n_total_AM_AM_force'].sum() if 'n_total_AM_AM_force' in df.columns else 0
    if n_total_force > 0:
        print('\n  ── Force-based classification (model-agnostic, primary) ──',
              flush=True)
        print(f'  Aggregate over all {len(df)} cases '
              f'({int(n_total_force):,} AM-AM contacts with fn>0):', flush=True)
        for s in ('intact', 'microcrack', 'multicrack',
                   'fragmentation', 'pulverization'):
            col = f'n_{s}_force_AM_AM'
            if col not in df.columns: continue
            tot = int(df[col].sum())
            pct = 100.0 * tot / max(n_total_force, 1)
            print(f'    {s:14s}  {tot:>8,d}  ({pct:5.1f}%)', flush=True)

        if 'fracture_index_force' in df.columns:
            idx_f = df['fracture_index_force'].dropna()
            if len(idx_f) > 0:
                print(f'\n  fracture_index_force '
                      f'(force-based severe fraction):', flush=True)
                print(f'    median: {np.median(idx_f):.3f}  '
                      f'mean: {np.mean(idx_f):.3f}  '
                      f'max: {np.max(idx_f):.3f}', flush=True)

        print(f'\n  Severity by pair type (force-based):', flush=True)
        for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
            col_frag = f'n_fragmentation_force_{pt}'
            col_pul  = f'n_pulverization_force_{pt}'
            col_tot  = f'n_total_force_{pt}'
            if col_tot not in df.columns: continue
            tot = df[col_tot].sum()
            if tot <= 0: continue
            sev_pct = 100.0 * (df[col_frag].sum() + df[col_pul].sum()) / tot
            print(f'    {pt:12s}  {sev_pct:5.1f}%  '
                  f'(of {int(tot):,} contacts)', flush=True)

    # ── Section 2 footnote — P_c statistics for paper draft ──
    print('\n' + '=' * 80, flush=True)
    print('SECTION-2 FOOTNOTE — per-pair-type P_c, R_min, F medians',
          flush=True)
    print('=' * 80, flush=True)
    print('\n  Pair          R_min (μm)   P_c (mN)    F (mN)      F/P_c',
          flush=True)
    print('  ' + '-' * 60, flush=True)
    for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
        r_col = f'R_min_um_median_{pt}'
        p_col = f'P_c_mN_median_{pt}'
        f_col = f'F_mN_median_{pt}'
        m_col = f'F_over_Pc_median_{pt}'
        if r_col not in df.columns: continue
        r_med = df[r_col].dropna()
        p_med = df[p_col].dropna() if p_col in df.columns else None
        f_med = df[f_col].dropna() if f_col in df.columns else None
        m_med = df[m_col].dropna() if m_col in df.columns else None
        if len(r_med) == 0: continue
        r_v = float(np.median(r_med))
        p_v = float(np.median(p_med)) if p_med is not None and len(p_med) > 0 else 0
        f_v = float(np.median(f_med)) if f_med is not None and len(f_med) > 0 else 0
        m_v = float(np.median(m_med)) if m_med is not None and len(m_med) > 0 else 0
        print(f'  {pt:12s}  {r_v:>10.2f}   {p_v:>8.3f}   {f_v:>8.3f}   {m_v:>6.2f}',
              flush=True)
    print('\n  → Use these medians to fill Section 2 footnote (TBD slots).',
          flush=True)

    # Save full results
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / 'b2_b4_diagnostic.csv', index=False)
    print(f'\n→ {out}/b2_b4_diagnostic.csv', flush=True)


if __name__ == '__main__':
    main()
