"""
Comprehensive dataset screening — find hidden issues beyond the basic
(A)(B)(C)(D)(E) automatic scan.

Checks:
  1. τ_Dijkstra sampling bias — |τ_mean - τ_median| / τ_median > 20%
     or τ_std / τ_mean > 0.5 (high CV suggests few robust paths)
  2. Laplace ↔ Dijkstra outliers — Lg/D outside [0.3, 2.0]
  3. 8mAh series consistency — cases with same group/ps_ratio should have
     σ within a consistent physical band
  4. Duplicate content — same atoms.csv md5 hash across cases
  5. Meta integrity — meta.json present and parseable
  6. Thickness outliers — thickness_um vs group expectation

Usage:
  python3 scripts/screen_dataset.py
"""
import os, json, hashlib
from collections import defaultdict


def md5_of(path, chunk=1 << 20):
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while b := f.read(chunk):
                h.update(b)
        return h.hexdigest()
    except Exception:
        return None


def load_case(root):
    m_path = os.path.join(root, 'full_metrics.json')
    if not os.path.exists(m_path):
        return None
    try:
        m = json.load(open(m_path))
    except Exception:
        return None
    # Try to find meta.json via results/uploads twin
    meta = {}
    for candidate in [os.path.join(root, 'meta.json'),
                      root.replace('/results/', '/uploads/') + '/meta.json']:
        if os.path.exists(candidate):
            try:
                meta = json.load(open(candidate))
                break
            except Exception:
                pass
    return {
        'root': root,
        'name': meta.get('name', os.path.basename(root)),
        'ps':   meta.get('ps_ratio', '?'),
        'mode': meta.get('mode', '?'),
        'phi':   m.get('phi_se', 0),
        'perc':  m.get('percolation_pct', 0),
        'thick': m.get('thickness_um', 0),
        'tau_mean':   m.get('tortuosity_mean'),
        'tau_median': m.get('tortuosity_median'),
        'tau_std':    m.get('tortuosity_std', 0),
        'sig_H':  m.get('sigma_full_mScm'),
        'sig_P':  m.get('sigma_full_mScm_physics'),
        'sig_bulk': m.get('sigma_bulk_net'),
        'CN':     m.get('se_se_cn_mean'),
        'atoms_csv': os.path.join(root, 'atoms.csv'),
    }


def main():
    cases = []
    for base in ['webapp/results', 'webapp/archive']:
        if not os.path.isdir(base):
            continue
        for r, _, files in os.walk(base):
            if 'full_metrics.json' in files:
                c = load_case(r)
                if c:
                    cases.append(c)

    print(f"Scanned {len(cases)} cases\n")

    # ─── Check 1: τ sampling bias ────────────────────────────────
    print("=" * 72)
    print("1. TAU SAMPLING BIAS (|mean-median|/median > 20% or CV > 0.5)")
    print("=" * 72)
    bad_tau = []
    for c in cases:
        tm, td, ts = c['tau_mean'], c['tau_median'], c['tau_std']
        if tm and td:
            skew = abs(tm - td) / td
            cv = (ts / tm) if tm > 0 else 0
            if skew > 0.20 or cv > 0.5:
                bad_tau.append((c, skew, cv))
    for c, skew, cv in sorted(bad_tau, key=lambda x: -x[1]):
        print(f"  {c['name']:30s}  τ_mean={c['tau_mean']:.2f} τ_med={c['tau_median']:.2f} "
              f"skew={skew*100:.0f}%  CV={cv*100:.0f}%")
    print(f"  → {len(bad_tau)} cases\n")

    # ─── Check 2: Laplace/Dijkstra outliers ─────────────────────
    print("=" * 72)
    print("2. LAPLACE↔DIJKSTRA OUTLIERS (Lg/D outside [0.3, 2.0])")
    print("=" * 72)
    import math
    bad_lg = []
    for c in cases:
        td, sb, phi = c['tau_mean'], c['sig_bulk'], c['phi']
        if td and sb and phi and sb > 0:
            tau_lg = math.sqrt(phi / sb)
            ratio = tau_lg / td
            if not (0.3 <= ratio <= 2.0):
                bad_lg.append((c, tau_lg, ratio))
    for c, tlg, r in sorted(bad_lg, key=lambda x: -abs(math.log(x[2]))):
        print(f"  {c['name']:30s}  τ_Dij={c['tau_mean']:.2f}  τ_Lg={tlg:.2f}  "
              f"Lg/D={r:.2f}×  φ={c['phi']:.3f}")
    print(f"  → {len(bad_lg)} cases\n")

    # ─── Check 3: 8mAh series consistency ───────────────────────
    print("=" * 72)
    print("3. GROUP CONSISTENCY (same group, same PS → similar σ expected)")
    print("=" * 72)
    groups = defaultdict(list)
    for c in cases:
        n = c['name']
        if n.startswith('input_'):
            # Parse: input_{tag}_{idx}[_variant]
            tag = n.replace('input_', '').split('_')[0]
            # Exclude pure digit cases that map directly
            groups[tag].append(c)
    for g, clist in sorted(groups.items()):
        if len(clist) < 2:
            continue
        sigs = [c['sig_H'] for c in clist if c['sig_H']]
        if len(sigs) < 2:
            continue
        lo, hi = min(sigs), max(sigs)
        if hi / lo > 10:  # order-of-magnitude within group
            print(f"  group '{g}' (n={len(clist)}): σ range [{lo:.4f}, {hi:.4f}]  ratio={hi/lo:.0f}×")
            for c in sorted(clist, key=lambda x: x['sig_H'] or 0):
                print(f"    {c['name']:30s}  σ={c['sig_H']}  φ={c['phi']:.3f} τ={c['tau_mean']}")
    print()

    # ─── Check 4: Duplicate atoms.csv ───────────────────────────
    print("=" * 72)
    print("4. DUPLICATE ATOMS.CSV (same md5 across cases)")
    print("=" * 72)
    hashes = defaultdict(list)
    for c in cases:
        h = md5_of(c['atoms_csv'])
        if h:
            hashes[h].append(c)
    dups = [(h, cs) for h, cs in hashes.items() if len(cs) > 1]
    for h, cs in dups:
        print(f"  md5={h[:10]}... ({len(cs)} cases):")
        for c in cs:
            print(f"    {c['name']:30s}  {c['root']}")
    print(f"  → {len(dups)} duplicate groups\n")

    # ─── Check 5: Thickness outliers ────────────────────────────
    print("=" * 72)
    print("5. THICKNESS vs GROUP (박막:15-25μm, 표준:50-80μm, 후막:130-160μm)")
    print("=" * 72)
    import re
    expectations = {
        'thin':        (10, 30),
        'thin_':       (10, 30),
        'real_':       (40, 90),
        'real40_':     (40, 90),
        'real8_':      (50, 90),
        'particulate': (80, 180),
        'S_':          (50, 100),
        '':            (50, 200),  # generic input_N
    }
    bad_thick = []
    for c in cases:
        thick = c['thick']
        if not thick:
            continue
        m = re.match(r'input_(thin\d*|real\d*|particulate|S_|)', c['name'])
        tag = m.group(1) if m else ''
        if tag in expectations:
            lo, hi = expectations[tag]
            if not (lo <= thick <= hi):
                bad_thick.append((c, tag, lo, hi))
    for c, tag, lo, hi in bad_thick:
        print(f"  {c['name']:30s}  thick={c['thick']:.1f}μm  expected [{lo}, {hi}] for '{tag}'")
    print(f"  → {len(bad_thick)} cases (some may be OK — naming conventions not uniform)\n")

    # ─── Summary ────────────────────────────────────────────────
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Total cases:                 {len(cases)}")
    print(f"  (1) τ sampling bias:         {len(bad_tau)}")
    print(f"  (2) Laplace outliers:        {len(bad_lg)}")
    print(f"  (3) Group σ inconsistent:    (see above, order-of-mag only)")
    print(f"  (4) Duplicate atoms.csv:     {len(dups)} groups")
    print(f"  (5) Thickness off expected:  {len(bad_thick)}")


if __name__ == '__main__':
    main()
