#!/usr/bin/env python3
"""Stage D — Stage-wise (literature-informed) fracture-aware σ_e solver.

Replaces the binary R=∞ filter (Stage C, run_network_fracture_aware.py)
with **per-contact σ_factor scaling** based on Lawn 1998 fracture stages
and literature-reported electronic-conductivity loss per stage.

Stage-wise σ_factor (literature synthesis):

    Lawn stage     │  F/P_c range  │  σ_factor  │  reasoning
    ───────────────┼───────────────┼────────────┼──────────────────────────
    intact         │  < 1          │   1.00     │  no damage
    microcrack     │  1 ≤ . < 3    │   0.85     │  partial intergranular
                                                  (Trevisanello 2021,
                                                   Heenan 2020 NMC811)
    multicrack     │  3 ≤ . < 11   │   0.40     │  rock-salt phase forms,
                                                  ~60% σ_e loss
                                                  (Jiang 2021, Wang 2021)
    fragmentation  │  11 ≤ . < 32  │   0.10     │  mostly broken + rock-salt
                                                  (Min 2024)
    pulverization  │  ≥ 32         │   0.02     │  residual surface only
                                                  (binary literature limit)

Implementation: multiplies contact_area + delta of each AM-AM contact by
the stage σ_factor BEFORE running network_conductivity. This preserves
graph topology while scaling per-edge conductance. SE-SE and AM-SE
contacts are untouched (only AM-AM are subject to fracture).

Output keys merged into full_metrics.json:
  electronic_sigma_full_mScm_stagewise            ← primary new metric
  thermal_sigma_full_mScm_stagewise
  electronic_sigma_loss_pct_stagewise             = (1-fa/full)×100
  fracture_aware_method = 'stagewise (Lawn-Lit)'

For comparison, run_network_fracture_aware.py (Stage C) writes the
binary-filter equivalents (`*_fracture_aware`). Both can coexist.

Usage:
  python3 scripts/run_network_fracture_stagewise.py
  python3 scripts/run_network_fracture_stagewise.py --quiet
  python3 scripts/run_network_fracture_stagewise.py CID …
"""
from __future__ import annotations
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT     = Path(__file__).resolve().parent.parent
SCRIPTS  = ROOT / 'scripts'
WEBAPP   = ROOT / 'webapp'
NET_PY   = SCRIPTS / 'network_conductivity.py'

sys.path.insert(0, str(SCRIPTS))
from fracture_model import fracture_classify_force_sim  # noqa: E402

# Lawn force-multiplier band edges and literature-derived σ_factor.
STAGE_FACTORS: list[tuple[float, float, float, str]] = [
    # (lower, upper, factor, label)
    (-float('inf'),  1.0, 1.00, 'intact'),
    (1.0,            3.0, 0.85, 'microcrack'),
    (3.0,           11.0, 0.40, 'multicrack'),
    (11.0,          32.0, 0.10, 'fragmentation'),
    (32.0,  float('inf'), 0.02, 'pulverization'),
]


def _stage_factor(m: float) -> tuple[float, str]:
    """Return (σ_factor, stage_label) for a given Lawn force multiplier m=F/P_c."""
    for lo, hi, f, lbl in STAGE_FACTORS:
        if lo <= m < hi:
            return f, lbl
    return 1.0, 'intact'


def discover_case_dirs() -> list[Path]:
    """Recursively find case dirs under results/ and archive/ at any depth.
    Fixes a depth-1-only iteration bug that silently skipped categorized
    archive cases (webapp/archive/category/case_id/)."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for atoms_p in root.rglob('atoms.csv'):
            case_dir = atoms_p.parent
            if ((case_dir / 'contacts.csv').exists()
                    and (case_dir / 'full_metrics.json').exists()
                    and case_dir not in seen):
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try: return json.load(open(path))
            except Exception: pass
    return {}


def scale_contacts(atoms_df: pd.DataFrame, contacts_df: pd.DataFrame,
                    type_map: dict, scale: float = 1000.0
                    ) -> tuple[pd.DataFrame, dict]:
    """Apply stage-wise σ_factor to AM-AM contact_area + delta.

    Returns (modified_contacts, stage_counts).
    """
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in lbl}
    id_to_type   = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['type'].astype(int)))
    id_to_radius = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['radius'].astype(float)))

    out = contacts_df.copy()
    has_ca = 'contact_area' in out.columns
    has_delta = 'delta' in out.columns
    factors = []
    stage_counts = {lbl: 0 for *_, lbl in STAGE_FACTORS}
    n_am_am = 0

    for _, c in contacts_df.iterrows():
        i1 = int(c['id1']); i2 = int(c['id2'])
        t1 = id_to_type.get(i1); t2 = id_to_type.get(i2)
        if t1 is None or t2 is None:
            factors.append(1.0); continue
        is_am_am = (t1 in am_types and t2 in am_types)
        if not is_am_am:
            factors.append(1.0); continue
        n_am_am += 1
        # F/P_c
        r1 = id_to_radius.get(i1, 0.0); r2 = id_to_radius.get(i2, 0.0)
        r_min = min(r1, r2)
        fn = float(c.get('fn', 0) or 0)
        if fn <= 0:
            fn = math.sqrt((c.get('fn_x', 0) or 0) ** 2
                            + (c.get('fn_y', 0) or 0) ** 2
                            + (c.get('fn_z', 0) or 0) ** 2)
        if r_min <= 0 or fn <= 0:
            factors.append(1.0); stage_counts['intact'] += 1; continue
        pair_label = '-'.join(sorted([type_map.get(t1, ''),
                                       type_map.get(t2, '')]))
        _stage, _pc, m = fracture_classify_force_sim(
            fn, r_min, contact_type=pair_label, scale=scale)
        f, lbl = _stage_factor(m)
        factors.append(f)
        stage_counts[lbl] += 1

    factors_arr = pd.Series(factors, index=out.index)
    if has_ca:
        out['contact_area'] = out['contact_area'].astype(float) * factors_arr
    if has_delta:
        out['delta'] = out['delta'].astype(float) * factors_arr
    stage_counts['__total_am_am'] = n_am_am
    return out, stage_counts


def parse_type_map(s: str) -> dict:
    out = {}
    for tok in (s or '').split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try: out[int(k.strip())] = v.strip()
            except Exception: pass
    return out


def run_one(case_dir: Path) -> tuple[str, bool, str]:
    meta = _read_meta(case_dir)
    type_map = parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    scale = float(meta.get('scale', 1000))

    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)
    scaled_df, stage_counts = scale_contacts(
        atoms_df, contacts_df, type_map, scale=scale)
    n_total_am_am = stage_counts['__total_am_am']
    if n_total_am_am == 0:
        return (case_dir.name, False, 'no AM-AM contacts')

    with tempfile.TemporaryDirectory(prefix='nfsw_') as tmpd:
        tmp = Path(tmpd)
        shutil.copy2(case_dir / 'atoms.csv', tmp / 'atoms.csv')
        scaled_df.to_csv(tmp / 'contacts.csv', index=False)
        # CRITICAL: copy input_params.json so network_conductivity reads
        # correct box_x, box_y (otherwise defaults to 0.05×0.05).
        for aux in ('input_params.json', 'meta.json'):
            src = case_dir / aux
            if src.exists():
                shutil.copy2(src, tmp / aux)

        type_map_str = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
        cmd = [sys.executable, str(NET_PY),
               str(tmp / 'atoms.csv'), str(tmp / 'contacts.csv'),
               '-o', str(tmp), '-t', type_map_str, '-s', str(int(scale)),
               '--contact-mode', 'both']
        try:
            cp = subprocess.run(cmd, check=False, capture_output=True,
                                  text=True, timeout=1800)
        except Exception as e:
            return (case_dir.name, False, f'EXC: {e}')
        if cp.returncode != 0:
            err = (cp.stderr or '').strip().splitlines()
            return (case_dir.name, False,
                    err[-1][:120] if err else f'returncode={cp.returncode}')

        net_json_p = tmp / 'network_conductivity.json'
        if not net_json_p.exists():
            return (case_dir.name, False, 'no network_conductivity.json')
        with open(net_json_p) as f:
            net_sw = json.load(f)

    fm_path = case_dir / 'full_metrics.json'
    try:
        with open(fm_path) as f:
            fm = json.load(f)
    except Exception as e:
        return (case_dir.name, False, f'fm read failed: {e}')

    sigma_full_sw = net_sw.get('sigma_full_mScm')
    sigma_e_sw    = net_sw.get('electronic_sigma_full_mScm')
    sigma_th_sw   = net_sw.get('thermal_sigma_full_mScm')

    fm['sigma_full_mScm_stagewise']            = sigma_full_sw
    fm['electronic_sigma_full_mScm_stagewise'] = sigma_e_sw
    fm['thermal_sigma_full_mScm_stagewise']    = sigma_th_sw
    fm['fracture_aware_method']                = 'stagewise (Lawn-Lit)'
    fm['stagewise_stage_counts']               = {k: int(v)
                                                    for k, v in stage_counts.items()}

    sigma_e_full = fm.get('electronic_sigma_full_mScm')
    if sigma_e_full and sigma_e_full > 0 and sigma_e_sw is not None:
        loss = (1.0 - sigma_e_sw / sigma_e_full) * 100
        fm['electronic_sigma_loss_pct_stagewise'] = round(loss, 2)
    sigma_th_full = fm.get('thermal_sigma_full_mScm')
    if sigma_th_full and sigma_th_full > 0 and sigma_th_sw is not None:
        loss_th = (1.0 - sigma_th_sw / sigma_th_full) * 100
        fm['thermal_sigma_loss_pct_stagewise'] = round(loss_th, 2)

    with open(fm_path, 'w') as f:
        json.dump(fm, f, indent=2, default=str)

    if sigma_e_full and sigma_e_sw is not None:
        loss_pct = fm.get('electronic_sigma_loss_pct_stagewise', '?')
        ic = stage_counts.get('intact', 0)
        mc = stage_counts.get('microcrack', 0)
        mu = stage_counts.get('multicrack', 0)
        fr = stage_counts.get('fragmentation', 0)
        pu = stage_counts.get('pulverization', 0)
        msg = (f'σ_e: {sigma_e_full:.3f} → {sigma_e_sw:.3f} (loss {loss_pct}%)  '
               f'[i:{ic} mc:{mc} mu:{mu} fr:{fr} pu:{pu}]')
    elif sigma_e_full:
        msg = f'σ_e: {sigma_e_full:.3f} → 0 (disconnected)'
    else:
        msg = f'[stages i:{stage_counts.get("intact", 0)} ...]'
    return (case_dir.name, True, msg)


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    ap.add_argument('--quiet', action='store_true', help='One line per case')
    args = ap.parse_args()

    all_cases = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in all_cases if d.name in wanted]
    else:
        cases = all_cases
    if not cases:
        ap.error('No cases found.')

    print(f'Stagewise fracture-aware solver on {len(cases)} cases  '
          f'(σ_factors: 1.00/0.85/0.40/0.10/0.02 by Lawn stage) …',
          flush=True)
    n_ok = n_fail = 0
    for i, d in enumerate(cases, 1):
        try:
            cid, ok, msg = run_one(d)
        except Exception as e:
            cid, ok, msg = (d.name, False, f'EXC: {type(e).__name__}: {e}')
        tag = '✓' if ok else '✗'
        if not args.quiet or not ok:
            print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:130]}',
                  flush=True)
        if ok: n_ok += 1
        else:  n_fail += 1
    print(f'\nDone — {n_ok} ok, {n_fail} failed.', flush=True)
    if n_fail: sys.exit(1)


if __name__ == '__main__':
    main()
