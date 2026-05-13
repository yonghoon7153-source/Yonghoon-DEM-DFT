#!/usr/bin/env python3
"""Diagnostic: fracture rate per particle type and per contact-pair type.

Resolves the visual question 'why does AM_S look more cracked than AM_P
in the 3D viewer when poly should fracture more?' by quantifying:

  (1) per-contact damage rate by pair type (AM_P-AM_P, AM_P-AM_S, AM_S-AM_S)
      — should show AM_P-AM_P MOST damaged (low K_IC, modest R)
  (2) per-particle damage rate by single type (AM_P vs AM_S)
      — aggregation: a particle is 'damaged' if any of its AM-AM
      contacts is damaged.  This is what the 3D viewer shows.

Usage:
    python3 scripts/diag_brittle_per_type.py <case_dir>
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from fracture_model import fracture_classify_force_sim, k_ic_for_pair, K_IC_AM_S, K_IC_AM_P


def fnum(x, d=0.0):
    try: return float(x)
    except: return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    args = ap.parse_args()
    case_dir = Path(args.case_dir)

    meta = json.loads((case_dir / 'meta.json').read_text())
    scale = float(meta.get('scale', 1000.0))
    type_map = {}
    for tok in str(meta.get('type_map', '')).split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            type_map[int(k.strip())] = v.strip()

    # Load atoms
    atoms = {}
    for r in csv.DictReader((case_dir / 'atoms.csv').open()):
        aid = int(r['id'])
        atoms[aid] = dict(
            type=type_map.get(int(r.get('type', 0)), '?'),
            r=fnum(r.get('radius') or r.get('r')),
        )

    # Per-particle aggregate
    particle_worst = defaultdict(lambda: 0)  # id → worst m
    pair_stats = defaultdict(lambda: {'n': 0, 'damaged': 0})

    for r in csv.DictReader((case_dir / 'contacts.csv').open()):
        try:
            i1 = int(r['id1']); i2 = int(r['id2'])
        except: continue
        if i1 not in atoms or i2 not in atoms: continue
        a1 = atoms[i1]; a2 = atoms[i2]
        if 'AM' not in a1['type'] or 'AM' not in a2['type']: continue
        fn = fnum(r.get('fn'))
        if not fn:
            fn = math.sqrt(fnum(r.get('fn_x'))**2 +
                           fnum(r.get('fn_y'))**2 +
                           fnum(r.get('fn_z'))**2)
        ct = '-'.join(sorted([a1['type'], a2['type']]))
        r_min = min(a1['r'], a2['r'])
        stage, _, m = fracture_classify_force_sim(
            fn, r_min, contact_type=ct, scale=scale)
        pair_stats[ct]['n'] += 1
        if stage != 'intact':
            pair_stats[ct]['damaged'] += 1
        if m > particle_worst[i1]: particle_worst[i1] = m
        if m > particle_worst[i2]: particle_worst[i2] = m

    print('=' * 70)
    print(f'Case: {case_dir.name}')
    print(f'K_IC: AM_S = {K_IC_AM_S/1e6:.2f} MPa·m^0.5  (single-crystal, tough)')
    print(f'      AM_P = {K_IC_AM_P/1e6:.2f} MPa·m^0.5  (polycryst, brittle)')
    print('=' * 70)

    # (1) per-pair-type contact damage
    print('\n(1) Per-contact damage rate by pair type:')
    print(f'{"pair":>12s} {"contacts":>10s} {"damaged":>10s} {"%":>7s}')
    print('-' * 50)
    for pair in sorted(pair_stats):
        s = pair_stats[pair]
        pct = 100 * s['damaged'] / max(s['n'], 1)
        print(f'{pair:>12s} {s["n"]:>10d} {s["damaged"]:>10d} {pct:>6.1f}%')

    # (2) per-particle damage (3D viewer aggregation)
    am_p_total = sum(1 for a in atoms.values() if a['type'] == 'AM_P')
    am_s_total = sum(1 for a in atoms.values() if a['type'] == 'AM_S')
    am_p_dmg = sum(1 for i, m in particle_worst.items()
                   if m >= 1 and atoms[i]['type'] == 'AM_P')
    am_s_dmg = sum(1 for i, m in particle_worst.items()
                   if m >= 1 and atoms[i]['type'] == 'AM_S')

    print('\n(2) Per-particle damage (viewer aggregation):')
    print(f'{"type":>8s} {"total":>10s} {"damaged":>10s} {"%":>7s}')
    print('-' * 45)
    print(f'{"AM_P":>8s} {am_p_total:>10d} {am_p_dmg:>10d} '
          f'{100*am_p_dmg/max(am_p_total,1):>6.1f}%')
    print(f'{"AM_S":>8s} {am_s_total:>10d} {am_s_dmg:>10d} '
          f'{100*am_s_dmg/max(am_s_total,1):>6.1f}%')

    print('\nInterpretation:')
    print('  (1) tells you at the contact level which TYPE OF CONTACT')
    print('      cracks most — AM_P-AM_P should dominate (low K_IC).')
    print('  (2) tells you at the particle level which TYPE OF PARTICLE')
    print('      shows colour in the 3D viewer.  Many small AM_S particles')
    print('      can each pick up a "damaged" flag from AM_P-AM_S contacts.')
    print('      Compare fractions, not absolute counts, to see the')
    print('      "polycryst more brittle" expectation.')


if __name__ == '__main__':
    main()
