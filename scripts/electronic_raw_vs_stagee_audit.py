#!/usr/bin/env python3
"""Find all cases where raw Hertz σ_e differs significantly from Stage E σ_e.

Triggered by input_1mAh_5 user inspection:
  raw σ_e = 51.89 mS/cm (network solver Hertz)
  Stage E = 9.014 mS/cm (after Trevisanello / AM-crystallinity)
  → 5.8× reduction

These cases are the ones where displaying raw on the dashboard misleads
because the form actually fits to Stage E (the physically realistic
composite σ_e).  After the _load_electronic_sigma fix, all plots show
Stage E — this script audits how big the cosmetic change is and which
cases would have looked very different before/after.

Run on WSL:
    python3 scripts/electronic_raw_vs_stagee_audit.py
"""
from __future__ import annotations
import json
from pathlib import Path


def main():
    rows = []
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            meta_p = mp.parent / 'meta.json'
            nm = mp.parent.name
            if meta_p.exists():
                try:
                    nm = json.load(open(meta_p)).get('name', nm) or nm
                except Exception:
                    pass
            raw = d.get('electronic_sigma_full_mScm')
            stE = d.get('electronic_sigma_full_mScm_stage_e')
            phys = d.get('electronic_sigma_full_mScm_physics')
            src = d.get('stage_e_source') or {}
            if not (isinstance(raw, (int, float)) and raw and raw > 0):
                continue
            if not (isinstance(stE, (int, float)) and stE and stE > 0):
                continue
            ratio = raw / stE
            rows.append({
                'name': nm,
                'raw': float(raw),
                'stE': float(stE),
                'phys': float(phys) if isinstance(phys, (int, float)) and phys > 0 else None,
                'ratio': float(ratio),
                'src_e': src.get('sigma_e', '?'),
                'src_e_phys': src.get('sigma_e_physics', '?'),
                'phi_am': d.get('phi_am'),
                'am_am_cn': d.get('am_am_cn'),
                'am_am_area': d.get('am_am_mean_area'),
            })

    # Dedup by (name, raw, stE) — same case in multiple folders
    seen = set()
    unique = []
    for r in rows:
        k = (r['name'], round(r['raw'], 3), round(r['stE'], 3))
        if k in seen: continue
        seen.add(k); unique.append(r)
    rows = unique

    print("=" * 100)
    print(" σ_electronic — raw Hertz vs Stage E target audit")
    print("=" * 100)
    print(f"  Total cases with both raw>0 AND Stage E>0 : {len(rows)}")
    print()

    # Histogram of ratio
    bins = [(1, 1.5, '~ same'),
            (1.5, 2.0, '1.5-2×'),
            (2.0, 3.0, '2-3×'),
            (3.0, 5.0, '3-5×'),
            (5.0, 10.0, '5-10×  ★'),
            (10.0, 100.0, '>10×  ★★')]
    print(f"  raw/Stage E ratio distribution:")
    for lo, hi, label in bins:
        cnt = sum(1 for r in rows if lo <= r['ratio'] < hi)
        bar = '█' * cnt
        print(f"    {label:>14s}  ({lo:.1f}-{hi:.1f}):  n={cnt:>3d}  {bar}")
    print()

    # Largest ratios — these are the user's "그런 케이스" candidates
    big = sorted([r for r in rows if r['ratio'] >= 2.0],
                 key=lambda r: -r['ratio'])
    print("─" * 100)
    print(f" Cases with raw / Stage E >= 2× (={len(big)} cases)")
    print(" These are where dashboard previously showed misleadingly-high raw σ_e.")
    print(" After _load_electronic_sigma fix → plot now shows Stage E (the form's target).")
    print("─" * 100)
    print(f"  {'name':32s}  {'raw':>8s}  {'stE':>8s}  {'phys':>8s}  {'ratio':>6s}  "
          f"{'src_e':>22s}  φ_AM  CN_AM  A_AM-AM")
    print(f"  {'-'*32}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*22}  ----  -----  -------")
    for r in big:
        phys_s = f"{r['phys']:8.3f}" if r['phys'] else "    -   "
        phi_s = f"{r['phi_am']:.3f}" if isinstance(r['phi_am'], (int, float)) else "  -  "
        cn_s = f"{r['am_am_cn']:.2f}" if isinstance(r['am_am_cn'], (int, float)) else "  -  "
        ar_s = f"{r['am_am_area']:.2f}" if isinstance(r['am_am_area'], (int, float)) else "  -  "
        print(f"  {r['name'][:32]:32s}  {r['raw']:8.3f}  {r['stE']:8.3f}  {phys_s}  "
              f"{r['ratio']:6.2f}  {r['src_e']:>22s}  {phi_s}  {cn_s}  {ar_s}")
    print()

    # Largest absolute raw values (potential physics-pathway bugs)
    big_raw = sorted(rows, key=lambda r: -r['raw'])[:15]
    print("─" * 100)
    print(" Top-15 largest raw σ_e values (any source)")
    print(" These would have dominated old bar-plot scale.")
    print("─" * 100)
    print(f"  {'name':32s}  {'raw':>8s}  {'stE':>8s}  {'ratio':>6s}")
    for r in big_raw:
        print(f"  {r['name'][:32]:32s}  {r['raw']:8.3f}  {r['stE']:8.3f}  {r['ratio']:6.2f}")
    print()

    # Summary
    print("=" * 100)
    print(" SUMMARY")
    print("=" * 100)
    n_severe = sum(1 for r in rows if r['ratio'] >= 5.0)
    n_moderate = sum(1 for r in rows if 2.0 <= r['ratio'] < 5.0)
    n_mild = sum(1 for r in rows if 1.5 <= r['ratio'] < 2.0)
    print(f"  Severe   (raw/stE ≥ 5×): {n_severe:>3d} cases — display was very misleading")
    print(f"  Moderate (2-5×)        : {n_moderate:>3d} cases — noticeable difference")
    print(f"  Mild     (1.5-2×)      : {n_mild:>3d} cases — minor difference")
    print(f"  All other (~1×)         : {len(rows) - n_severe - n_moderate - n_mild:>3d} cases — no real change")
    print()
    print(f"  After fix: all plots show Stage E σ_e (the form's actual target).")
    print(f"  Bar / line plot scales should now match the parity / outlier plots.")


if __name__ == '__main__':
    main()
