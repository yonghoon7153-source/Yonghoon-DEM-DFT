#!/usr/bin/env python3
"""Audit how many σ_electronic cases used the 'Bruggeman fallback' instead
of a real network-solver result.

User found via dashboard inspection of 1mAh_100_2 / _3:
  • 1mAh_100_3: raw σ_e (Hertz)='—', physics='—', stE=68.232  (phantom)
  • 1mAh_100_2: raw σ_e (Hertz)='—', physics=61.83, stE=54.787
    plus a system flag: 'Bruggeman fallback fired — Physics: (σ_e)' ⚡

These reveal the network solver electronic pathway can fail (silent or
flagged), and the Stage E pipeline falls back to a Bruggeman-based
estimate × Trevisanello multiplier — producing phantom σ_e values that
don't reflect actual Kirchhoff network conductance.

This script walks the corpus and reports:
  • Total cases with full_metrics.json
  • Cases where raw electronic_sigma_full_mScm (Hertz) IS populated
  • Cases where it's missing (= solver didn't run on Hertz electronic)
  • Cases flagged with 'Bruggeman fallback' / 'Layer-6' / similar in
    channel-status fields
  • The intersection (silent-failure cases that current load_corpus
    would still pick up via Stage E)
  • Per-case listing with σ_e values across all 4 columns

Run on WSL:
    python3 scripts/electronic_fallback_audit.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def main():
    rows = []
    seen_paths = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            if str(mp) in seen_paths:
                continue
            seen_paths.add(str(mp))
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            cid = mp.parent.name
            nm = cid
            meta_p = mp.parent / 'meta.json'
            if meta_p.exists():
                try:
                    nm = json.load(open(meta_p)).get('name') or cid
                except Exception:
                    pass

            raw = d.get('electronic_sigma_full_mScm')
            phys = d.get('electronic_sigma_full_mScm_physics')
            stE = d.get('electronic_sigma_full_mScm_stage_e')
            stEP = d.get('electronic_sigma_full_mScm_stage_e_physics')

            # Look for fallback flag — check both stage_e_source dict
            # (structured) and any text field (legacy).
            fallback_hit = False
            src_fb = d.get('stage_e_source') or {}
            if (src_fb.get('sigma_e') == 'fallback_weighted_factor'
                or src_fb.get('sigma_e_physics') == 'fallback_weighted_factor'):
                fallback_hit = True
            if not fallback_hit:
                for k, v in d.items():
                    if isinstance(v, str):
                        if any(s in v.lower() for s in
                               ['bruggeman fallback', 'layer-6', 'fallback fired',
                                'bruggeman_fallback']):
                            fallback_hit = True
                            break

            def _num(v):
                return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None

            rows.append({
                'name': nm, 'cid': cid,
                'raw': _num(raw), 'phys': _num(phys),
                'stE': _num(stE), 'stEP': _num(stEP),
                'fallback': fallback_hit,
            })

    n_total = len(rows)
    n_with_raw = sum(1 for r in rows if r['raw'] is not None)
    n_missing_raw = sum(1 for r in rows if r['raw'] is None)
    n_with_stE = sum(1 for r in rows if r['stE'] is not None)
    n_phantom = sum(1 for r in rows if r['raw'] is None and r['stE'] is not None)
    n_flag = sum(1 for r in rows if r['fallback'])
    n_no_se = sum(1 for r in rows if r['stE'] is None and r['stEP'] is None
                  and r['raw'] is None and r['phys'] is None)

    print("=" * 78)
    print(" σ_electronic — corpus-wide Bruggeman-fallback audit")
    print("=" * 78)
    print(f"  Total full_metrics.json files scanned : {n_total:>4d}")
    print(f"  with raw electronic σ (Hertz) > 0     : {n_with_raw:>4d}")
    print(f"  WITHOUT raw σ (solver didn't run)     : {n_missing_raw:>4d}  ⚠")
    print(f"  with Stage E σ value populated        : {n_with_stE:>4d}")
    print(f"  PHANTOM: missing raw but has Stage E  : {n_phantom:>4d}  ★")
    print(f"  flagged 'Bruggeman fallback' in text  : {n_flag:>4d}")
    print(f"  no σ_e value at all (raw/phys/stE/stEP all empty): {n_no_se:>4d}")
    print()

    if n_phantom > 0:
        print("─" * 78)
        print(f" PHANTOM CASES: raw=missing but Stage E populated ({n_phantom} cases)")
        print(" These are precisely the buggy entries contaminating the σ_e fit.")
        print("─" * 78)
        print(f"  {'case':32s}  {'raw':>8s}  {'phys':>8s}  {'stE':>8s}  {'stEP':>8s}  fallback?")
        # Dedup by case name (multiple full_metrics.json files per case)
        seen_names = set()
        sorted_rows = sorted(rows, key=lambda r: r['name'])
        for r in sorted_rows:
            if r['raw'] is None and r['stE'] is not None:
                if r['name'] in seen_names:
                    continue
                seen_names.add(r['name'])
                def fmt(v):
                    return f"{v:>8.3f}" if v is not None else "      — "
                fb = "YES ⚡" if r['fallback'] else ""
                print(f"  {r['name'][:32]:32s}  {fmt(r['raw'])}  {fmt(r['phys'])}  "
                      f"{fmt(r['stE'])}  {fmt(r['stEP'])}  {fb}")
        print()

    if n_flag > 0 and n_flag != n_phantom:
        print("─" * 78)
        print(f" FALLBACK-FLAGGED but raw IS populated ({n_flag - n_phantom} cases)")
        print(" These have 'Bruggeman fallback' note BUT also have a raw solver value.")
        print(" Stage E may still be partially phantom — inspect individually.")
        print("─" * 78)
        seen2 = set()
        for r in sorted(rows, key=lambda r: r['name']):
            if r['fallback'] and r['raw'] is not None:
                if r['name'] in seen2: continue
                seen2.add(r['name'])
                def fmt(v):
                    return f"{v:>8.3f}" if v is not None else "      — "
                print(f"  {r['name'][:32]:32s}  raw={fmt(r['raw'])}  "
                      f"phys={fmt(r['phys'])}  stE={fmt(r['stE'])}  stEP={fmt(r['stEP'])}")
        print()

    # ───── Verdict ─────
    print("=" * 78)
    print(" VERDICT")
    print("=" * 78)
    pct_phantom = 100 * n_phantom / n_with_stE if n_with_stE > 0 else 0
    print(f"  Phantom rate: {pct_phantom:.1f}% of Stage-E-populated cases")
    print(f"  ({n_phantom}/{n_with_stE} cases had Stage E σ_e but no raw solver output)")
    print()
    print(f"  The raw-required filter in _stage_e_electronic() will now exclude")
    print(f"  ALL {n_phantom} phantom cases from the σ_e fit corpus.")
    print()
    print(f"  Next step (separate session): find why network_conductivity.py's")
    print(f"  electronic pathway failed/didn't run on those {n_phantom} cases.")
    print(f"  Common candidates:")
    print(f"    • AM-AM percolation guard (am_am_cn < threshold → skip electronic)")
    print(f"    • Thin-electrode guard (T < N × d_AM → can't form AM-AM network)")
    print(f"    • Silent-fail try/except in run_network_full_corrections.py")


if __name__ == '__main__':
    main()
