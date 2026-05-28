#!/usr/bin/env python3
"""σ_electronic data audit — find the cause of the impossible 6-orders-of-mag
σ_e range observed in electronic_nested_cv.py (0.17 ~ 1,119,859 mS/cm).

For each case in the corpus, print:
  • raw  σ_e  = electronic_sigma_full_mScm
  • phys σ_e  = electronic_sigma_full_mScm_physics
  • stE  σ_e  = electronic_sigma_full_mScm_stage_e
  • stEP σ_e  = electronic_sigma_full_mScm_stage_e_physics
  • phi_am, p_amp (composition)
  • r_AM_P, r_AM_S (particle sizes)

Sort by descending picked-target σ.  Look for:
  • Top cases with σ > 100 mS/cm  ← impossible for NCM composite
  • Stage E ≫ physics ratio        ← Trevisanello correction blowing up
  • Single-crystal vs polycrystal AM_P → different σ_AM literature
  • Discrepancy direction          ← which transformation introduces the bug

Run on WSL:
    python3 scripts/electronic_audit.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp


def _meta_name(cid, mp_parent):
    for meta_p in (Path('webapp/uploads') / cid / 'meta.json',
                   mp_parent / 'meta.json'):
        if meta_p.exists():
            try:
                return json.load(open(meta_p)).get('name') or cid
            except Exception:
                pass
    return cid


def main():
    rows = []
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
            cid = mp.parent.name
            nm = _meta_name(cid, mp.parent)
            sigs = {
                'raw':  d.get('electronic_sigma_full_mScm'),
                'phys': d.get('electronic_sigma_full_mScm_physics'),
                'stE':  d.get('electronic_sigma_full_mScm_stage_e'),
                'stEP': d.get('electronic_sigma_full_mScm_stage_e_physics'),
            }
            phi_am = d.get('phi_am')
            p_amp = gcp._ps_fraction(d)
            ras, rap = gcp._r_am_sizes(d)
            T = d.get('thickness_um')
            cn_am = d.get('am_am_cn')

            # pick target like electronic_nested_cv.py
            target = None; target_key = None
            for k in ('stEP', 'stE', 'phys', 'raw'):
                v = sigs[k]
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                    target = v; target_key = k; break

            key = (round(phi_am or 0, 4), round(cn_am or 0, 3),
                   round(float(target or 0), 5))
            if key in seen:
                continue
            seen.add(key)

            rows.append({'name': nm, 'cid': cid, 'sigs': sigs,
                         'target': target, 'target_key': target_key,
                         'phi_am': phi_am, 'p_amp': p_amp,
                         'r_AM_S': ras, 'r_AM_P': rap, 'T': T,
                         'cn_am': cn_am})

    valid = [r for r in rows if r['target'] is not None]
    n = len(valid)
    print(f"=" * 100)
    print(f" σ_e AUDIT — n={n} cases with a valid σ_e target")
    print(f"=" * 100)
    targets = np.array([r['target'] for r in valid])
    print(f"  target σ_e range : {targets.min():.4f} ~ {targets.max():.1f} mS/cm")
    print(f"  median            : {np.median(targets):.4f}  geomean: {np.exp(np.mean(np.log(targets))):.4f}")
    print()

    # bands
    bands = [(0, 0.01), (0.01, 0.1), (0.1, 1), (1, 10),
             (10, 100), (100, 1000), (1000, 1e4), (1e4, 1e8)]
    print("  Distribution by magnitude band:")
    for lo, hi in bands:
        cnt = int(((targets >= lo) & (targets < hi)).sum())
        marker = "  ⚠ IMPOSSIBLE for NCM composite" if lo >= 100 else (
                 "  ← typical range" if lo == 1 else "")
        print(f"     [{lo:>7.2f}, {hi:>7.0f})  n={cnt:>3d}{marker}")
    print()

    # Top 15 highest σ_e — these are the suspects
    sorted_rows = sorted(valid, key=lambda r: -r['target'])
    print("=" * 100)
    print(" TOP 15 highest-σ_e cases (suspect — check raw vs corrected values)")
    print("=" * 100)
    print(f"  {'#':>3s} {'case':30s} {'tgt_key':>6s}  "
          f"{'raw':>10s}  {'phys':>10s}  {'stE':>10s}  {'stEP':>10s}  "
          f"{'φ_AM':>5s}  {'P:S':>4s}  {'r_AM_P':>6s}  {'r_AM_S':>6s}")
    print("  " + "─" * 96)
    for i, r in enumerate(sorted_rows[:15], 1):
        s = r['sigs']
        ps_lab = (f"{int(round(r['p_amp']*10))}:{10-int(round(r['p_amp']*10))}"
                  if r['p_amp'] is not None else "-")
        def fmt(v):
            return f"{v:>10.3f}" if isinstance(v, (int, float)) else "       —  "
        print(f"  {i:>3d} {r['name'][:30]:30s} {r['target_key']:>6s}  "
              f"{fmt(s['raw'])}  {fmt(s['phys'])}  {fmt(s['stE'])}  {fmt(s['stEP'])}  "
              f"{(r['phi_am'] or 0):5.3f}  {ps_lab:>4s}  "
              f"{(r['r_AM_P'] or 0):6.2f}  {(r['r_AM_S'] or 0):6.2f}")
    print()

    # Bottom 5 lowest σ_e — sanity check on low end
    print("=" * 100)
    print(" BOTTOM 5 lowest-σ_e cases (sanity check)")
    print("=" * 100)
    print(f"  {'#':>3s} {'case':30s} {'tgt_key':>6s}  "
          f"{'raw':>10s}  {'phys':>10s}  {'stE':>10s}  {'stEP':>10s}  "
          f"{'φ_AM':>5s}  {'P:S':>4s}")
    print("  " + "─" * 96)
    for i, r in enumerate(sorted_rows[-5:], 1):
        s = r['sigs']
        ps_lab = (f"{int(round(r['p_amp']*10))}:{10-int(round(r['p_amp']*10))}"
                  if r['p_amp'] is not None else "-")
        def fmt(v):
            return f"{v:>10.3f}" if isinstance(v, (int, float)) else "       —  "
        print(f"  {i:>3d} {r['name'][:30]:30s} {r['target_key']:>6s}  "
              f"{fmt(s['raw'])}  {fmt(s['phys'])}  {fmt(s['stE'])}  {fmt(s['stEP'])}  "
              f"{(r['phi_am'] or 0):5.3f}  {ps_lab:>4s}")
    print()

    # Per-key ratio analysis: stE/phys ratio (Stage E correction factor)
    print("=" * 100)
    print(" Stage E / physics RATIO distribution (how much Trevisanello shifts σ_e)")
    print("=" * 100)
    ratios = []
    for r in valid:
        s = r['sigs']
        a = s.get('stE') or s.get('stEP')
        b = s.get('phys') or s.get('raw')
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b > 0:
            ratios.append((a / b, r['name'], a, b))
    if ratios:
        rats = np.array([r[0] for r in ratios])
        print(f"  n with both Stage E and physics available: {len(ratios)}")
        print(f"  ratio range : {rats.min():.4f} ~ {rats.max():.1f}×")
        print(f"  median ratio: {np.median(rats):.4f}  (literature Trevisanello: typically 0.1~0.5)")
        print(f"  cases with ratio > 10 (likely BUG):")
        ratios.sort(key=lambda t: -t[0])
        for ratio, nm, a, b in ratios[:10]:
            if ratio > 10:
                print(f"     {nm[:30]:30s}  stE={a:>10.2f}  phys={b:>10.2f}  ratio={ratio:>8.2f}×")
    print()

    # P:S composition breakdown of top-σ_e suspects
    print("=" * 100)
    print(" P:S composition of top-15 suspects (is AM_P single-crystal correction over-applied?)")
    print("=" * 100)
    from collections import Counter
    top15_ps = Counter()
    for r in sorted_rows[:15]:
        ps_lab = (f"{int(round(r['p_amp']*10))}:{10-int(round(r['p_amp']*10))}"
                  if r['p_amp'] is not None else "-")
        top15_ps[ps_lab] += 1
    for ps, cnt in sorted(top15_ps.items(), key=lambda t: -t[1]):
        print(f"     {ps:>5s} : {cnt} cases")

    print()
    print("=" * 100)
    print(" DIAGNOSIS HINTS")
    print("=" * 100)
    print(" If top suspects are P:S=10:0 (AM_P-only) AND stE / phys ratio ≫ 1:")
    print("   → Trevisanello AM_P single-crystal correction is being applied as")
    print("     a MULTIPLIER (σ_AM_P_single ≈ 10⁴-10⁵ × poly NCM).  Check the")
    print("     Stage E pipeline for AM_P branch.")
    print(" If σ_e > 100 mS/cm appears across all P:S → general units bug")
    print("   (S/cm vs mS/cm somewhere in the pipeline).")
    print(" If only a few extreme outliers → those specific cases need fixing.")


if __name__ == '__main__':
    main()
