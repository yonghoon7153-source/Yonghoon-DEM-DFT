#!/usr/bin/env python3
"""Audit whether the AM_P / AM_S labeling in the corpus actually follows
the implicit size convention (AM_P = larger mode, AM_S = smaller mode).

`_ps_fraction` parses the user-provided `ps_ratio` string ("10:0", "0:10",
"7:3", …) — it does NOT check actual particle sizes.  If our form relies
on g010 (a sigmoid in p) to encode "small-particle fraction" disorder,
that interpretation only holds if r_AM_S < r_AM_P **in every case** (or
at least systematically).  This script verifies that empirically:

  • r_AM_S, r_AM_P distributions across the corpus
  • cases where r_AM_S ≥ r_AM_P  (convention violation)
  • monomodal cases (only one of r_AM_S/r_AM_P present) and what size they have
  • whether the corpus IS consistent enough to treat g010 as a small-AM
    fraction proxy

Run from the repo root:  python3 scripts/audit_ps_label_convention.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def load():
    rows = []
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = json.load(open(mp))
            except Exception: continue
            def _g(*keys):
                for k in keys:
                    v = d.get(k)
                    if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                        return v*1000.0 if v < 0.01 else float(v)
                return None
            ras = _g('_input_r_AM_S_um', '_input_r_AM_S', 'r_AM_S_um', 'r_AM_S')
            rap = _g('_input_r_AM_P_um', '_input_r_AM_P', 'r_AM_P_um', 'r_AM_P')
            ps  = d.get('ps_ratio') or ''
            rse = _g('_input_r_SE_um', '_input_r_SE', 'r_SE_um', 'r_SE')
            cid = mp.parent.name
            name = cid
            for meta_p in (Path('webapp/uploads') / cid / 'meta.json', mp.parent / 'meta.json'):
                if meta_p.exists():
                    try:
                        name = json.load(open(meta_p)).get('name') or cid
                        break
                    except Exception: pass
            rows.append({'name': name, 'ps': ps, 'r_AM_S': ras, 'r_AM_P': rap, 'r_SE': rse})
    return rows


def main():
    rows = load()
    n = len(rows)
    print(f"Loaded {n} cases from corpus\n")

    # 1) Label parsing distribution
    ps_counts = {}
    for r in rows: ps_counts[r['ps']] = ps_counts.get(r['ps'], 0) + 1
    print("=" * 70)
    print("PS-ratio labels in corpus:")
    for ps, c in sorted(ps_counts.items(), key=lambda x: -x[1]):
        print(f"   {ps or '(empty)':>12s} : {c:4d}")
    print()

    # 2) r_AM_S vs r_AM_P distributions
    rs_vals = [r['r_AM_S'] for r in rows if r['r_AM_S'] is not None]
    rp_vals = [r['r_AM_P'] for r in rows if r['r_AM_P'] is not None]
    print("=" * 70)
    print("AM particle sizes (µm) across the corpus:")
    print(f"   r_AM_S available in {len(rs_vals)}/{n} cases   "
          f"range [{min(rs_vals):.3f}, {max(rs_vals):.3f}]   "
          f"median {np.median(rs_vals):.3f}")
    print(f"   r_AM_P available in {len(rp_vals)}/{n} cases   "
          f"range [{min(rp_vals):.3f}, {max(rp_vals):.3f}]   "
          f"median {np.median(rp_vals):.3f}")
    # value distributions
    from collections import Counter
    print(f"\n   r_AM_S value distribution: ", end='')
    for v, c in sorted(Counter(round(x, 3) for x in rs_vals).items()):
        print(f"{v}µm×{c}", end='  ')
    print(f"\n   r_AM_P value distribution: ", end='')
    for v, c in sorted(Counter(round(x, 3) for x in rp_vals).items()):
        print(f"{v}µm×{c}", end='  ')
    print()
    print()

    # 3) Convention violation check
    both = [r for r in rows if r['r_AM_S'] and r['r_AM_P']]
    violations = [r for r in both if r['r_AM_S'] >= r['r_AM_P']]
    print("=" * 70)
    print(f"Convention check (AM_S < AM_P)?   bimodal cases: {len(both)}/{n}")
    print(f"   CONVENTION VIOLATIONS (r_AM_S ≥ r_AM_P) : {len(violations)}")
    for r in violations[:10]:
        print(f"     • {r['name'][:30]:30s}   r_AM_S={r['r_AM_S']:.3f}   "
              f"r_AM_P={r['r_AM_P']:.3f}   ps={r['ps']}")
    if len(violations) == 0:
        print(f"   ✓ no violations — AM_S is strictly smaller than AM_P in all bimodal cases")
    print()

    # 4) Monomodal cases — does the LABEL match the size?
    print("=" * 70)
    print("Monomodal cases (only one of AM_S / AM_P present):")
    mono_S = [r for r in rows if r['r_AM_S'] and not r['r_AM_P']]
    mono_P = [r for r in rows if r['r_AM_P'] and not r['r_AM_S']]
    print(f"   AM_S-only (labeled 0:10):  {len(mono_S)} cases   "
          f"r_AM_S range [{min(r['r_AM_S'] for r in mono_S):.3f}, "
          f"{max(r['r_AM_S'] for r in mono_S):.3f}]" if mono_S else
          f"   AM_S-only (labeled 0:10):  0 cases")
    print(f"   AM_P-only (labeled 10:0):  {len(mono_P)} cases   "
          f"r_AM_P range [{min(r['r_AM_P'] for r in mono_P):.3f}, "
          f"{max(r['r_AM_P'] for r in mono_P):.3f}]" if mono_P else
          f"   AM_P-only (labeled 10:0):  0 cases")
    # Check: is there overlap?  e.g. a 1.0µm monomodal labeled AM_S in one
    # case but AM_P in another?
    s_sizes = set(round(r['r_AM_S'], 2) for r in mono_S)
    p_sizes = set(round(r['r_AM_P'], 2) for r in mono_P)
    overlap = s_sizes & p_sizes
    if overlap:
        print(f"\n   ⚠ SIZE OVERLAP between AM_S-only and AM_P-only labels: "
              f"{sorted(overlap)} µm")
        print(f"     → the SAME particle size appears with BOTH labels in different cases.")
        print(f"     → label is NOT pure size-derived; this is the user's monomodal concern.")
    else:
        s_max = max(s_sizes) if s_sizes else 0
        p_min = min(p_sizes) if p_sizes else 0
        print(f"\n   ✓ no size overlap.  AM_S monomodal max = {s_max} µm, "
              f"AM_P monomodal min = {p_min} µm")
        if s_max < p_min:
            cutoff = (s_max + p_min) / 2
            print(f"   → corpus IS consistent with an implicit size cutoff at "
                  f"≈{cutoff:.2f} µm.")
            print(f"     (anything below ≈{cutoff:.2f} µm gets AM_S label, "
                  f"anything above gets AM_P)")
    print()

    # 5) Final verdict
    print("=" * 70)
    print("INTERPRETATION:")
    if not violations and not overlap:
        print("  ✓ Corpus follows the AM_P > AM_S size convention strictly.")
        print("    The g010 sigmoid in p IS effectively a sigmoid in 'fraction of")
        print("    small AM particles' for this corpus.  The form is reproducible")
        print("    for FUTURE data IF users follow the same size-based labeling.")
        print("    Recommend: enforce by checking r_AM_S < r_AM_P at data load.")
    else:
        print("  ⚠ Corpus has convention violations — the g010 interpretation as")
        print("    'small-AM fraction' is then a CORPUS-AVERAGE statement, not a")
        print("    strict per-case rule.  For the form to be reproducible, future")
        print("    data must use a consistent labeling (e.g. AM_S always = smaller).")


if __name__ == "__main__":
    main()
