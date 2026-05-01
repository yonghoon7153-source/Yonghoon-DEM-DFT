#!/usr/bin/env python3
"""Stage C: Fracture-aware network conductivity solver.

For each case, builds a filtered contacts.csv with multicrack+ AM-AM
contacts excluded (force-based, F/P_c >= 3) and re-runs network_
conductivity to produce σ_e^fracture-aware. Compared against the
unfiltered σ_e^full this quantifies the AM-fracture sensitivity of
the electronic and thermal channels — the missing piece of paper
Section 4 / 5 (which only addressed σ_ionic).

Filter convention
─────────────────
Force-based (Hooke-correct, model-agnostic; see paper Section 2):
  F/P_c >= 3   →  multicrack+ → contact treated as 'broken' (R = ∞)
  F/P_c <  3   →  intact / single microcrack → contact retained

Choice rationale
────────────────
The multicrack threshold (Lawn 1998 second multiplier) is the natural
"contact significantly compromised" line. Single microcracks
(F/P_c in [1, 3]) do not yet meaningfully degrade contact conductance.
Force-based picked over δ-based per Section 6 (paper) because force
is internally consistent with the LIGGGHTS hooke contact model and
matches Auerbach's original force-based criterion.

What the solver produces
────────────────────────
σ_ionic       — UNCHANGED (SE-SE only, AM-AM not in graph) [sanity check]
σ_electronic  — DROPS by the fracture-loss factor (AM-AM only)
σ_thermal     — partially drops (AM-AM share only)

Output keys merged into full_metrics.json:
  sigma_full_mScm_fracture_aware
  electronic_sigma_full_mScm_fracture_aware     ← primary new metric
  thermal_sigma_full_mScm_fracture_aware
  electronic_sigma_loss_pct                     = (1 - filtered/full) × 100
  n_am_am_contacts_excluded
  n_am_am_contacts_total
  fracture_aware_threshold                       = 'multicrack (F/Pc >= 3)'

Usage:
  python3 scripts/run_network_fracture_aware.py            # all cases
  python3 scripts/run_network_fracture_aware.py --quiet    # one line/case
  python3 scripts/run_network_fracture_aware.py CID …      # specific cases
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
from fracture_model import fracture_classify_force_sim, k_ic_for_pair  # noqa: E402

# Lawn force multiplier threshold for "broken" contact classification.
# F/P_c >= 3 → multicrack+ (multiple cone/radial cracks, contact compromised).
THRESHOLD_MULTIPLIER = 3.0


def discover_case_dirs() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for d in sorted(root.iterdir()):
            if (d.is_dir()
                    and (d / 'atoms.csv').exists()
                    and (d / 'contacts.csv').exists()
                    and (d / 'full_metrics.json').exists()):
                out.append(d)
    return out


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try: return json.load(open(path))
            except Exception: pass
    return {}


def filter_contacts(atoms_df: pd.DataFrame, contacts_df: pd.DataFrame,
                     type_map: dict, scale: float = 1000.0
                     ) -> tuple[pd.DataFrame, int, int]:
    """Return (filtered_contacts, n_excluded, n_total_am_am).

    Removes AM-AM contacts whose F/P_c >= 3.0 (multicrack+ regime).
    SE-SE and AM-SE contacts unaffected.
    """
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in lbl}
    id_to_type   = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['type'].astype(int)))
    id_to_radius = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['radius'].astype(float)))

    keep_mask = []
    n_total_am_am = 0
    n_excluded = 0

    for _, c in contacts_df.iterrows():
        i1 = int(c['id1']); i2 = int(c['id2'])
        t1 = id_to_type.get(i1); t2 = id_to_type.get(i2)
        if t1 is None or t2 is None:
            keep_mask.append(True); continue
        is_am_am = (t1 in am_types and t2 in am_types)
        if not is_am_am:
            keep_mask.append(True); continue
        n_total_am_am += 1
        # Compute F/P_c
        r1 = id_to_radius.get(i1, 0.0); r2 = id_to_radius.get(i2, 0.0)
        r_min = min(r1, r2)
        fn = float(c.get('fn', 0) or 0)
        if fn <= 0:
            fn = math.sqrt((c.get('fn_x', 0) or 0) ** 2
                            + (c.get('fn_y', 0) or 0) ** 2
                            + (c.get('fn_z', 0) or 0) ** 2)
        if r_min <= 0 or fn <= 0:
            keep_mask.append(True); continue
        pair_label = '-'.join(sorted([type_map.get(t1, ''),
                                       type_map.get(t2, '')]))
        _stage, _pc, m = fracture_classify_force_sim(
            fn, r_min, contact_type=pair_label, scale=scale)
        if m >= THRESHOLD_MULTIPLIER:
            keep_mask.append(False)
            n_excluded += 1
        else:
            keep_mask.append(True)

    return contacts_df[pd.Series(keep_mask, index=contacts_df.index)], \
           n_excluded, n_total_am_am


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

    # Load contacts + filter
    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)
    n_orig = len(contacts_df)
    filtered_df, n_excl, n_total_am_am = filter_contacts(
        atoms_df, contacts_df, type_map, scale=scale)
    if n_total_am_am == 0:
        return (case_dir.name, False, 'no AM-AM contacts')

    # Write filtered contacts to a tmp dir + run network_conductivity there
    with tempfile.TemporaryDirectory(prefix='nfa_') as tmpd:
        tmp = Path(tmpd)
        # Need atoms.csv + filtered contacts.csv co-located
        shutil.copy2(case_dir / 'atoms.csv', tmp / 'atoms.csv')
        filtered_df.to_csv(tmp / 'contacts.csv', index=False)
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
            return (case_dir.name, False, 'no network_conductivity.json output')
        with open(net_json_p) as f:
            net_filt = json.load(f)

    # Merge fracture-aware σ values into full_metrics.json
    fm_path = case_dir / 'full_metrics.json'
    try:
        with open(fm_path) as f:
            fm = json.load(f)
    except Exception as e:
        return (case_dir.name, False, f'fm read failed: {e}')

    # Pull the new σ values
    sigma_full_filt = net_filt.get('sigma_full_mScm')
    sigma_e_filt    = net_filt.get('electronic_sigma_full_mScm')
    sigma_th_filt   = net_filt.get('thermal_sigma_full_mScm')

    fm['sigma_full_mScm_fracture_aware']            = sigma_full_filt
    fm['electronic_sigma_full_mScm_fracture_aware'] = sigma_e_filt
    fm['thermal_sigma_full_mScm_fracture_aware']    = sigma_th_filt
    fm['n_am_am_contacts_excluded']    = int(n_excl)
    fm['n_am_am_contacts_total']       = int(n_total_am_am)
    fm['fracture_aware_threshold']     = f'F/P_c >= {THRESHOLD_MULTIPLIER:.0f} (multicrack+)'
    fm['fracture_aware_excluded_pct']  = round(
        100.0 * n_excl / max(n_total_am_am, 1), 2)

    # Loss pct: how much σ_e dropped due to filtering
    sigma_e_full = fm.get('electronic_sigma_full_mScm')
    if sigma_e_full and sigma_e_full > 0 and sigma_e_filt is not None:
        loss = (1.0 - sigma_e_filt / sigma_e_full) * 100
        fm['electronic_sigma_loss_pct'] = round(loss, 2)
    sigma_th_full = fm.get('thermal_sigma_full_mScm')
    if sigma_th_full and sigma_th_full > 0 and sigma_th_filt is not None:
        loss_th = (1.0 - sigma_th_filt / sigma_th_full) * 100
        fm['thermal_sigma_loss_pct'] = round(loss_th, 2)

    with open(fm_path, 'w') as f:
        json.dump(fm, f, indent=2, default=str)

    if sigma_e_full and sigma_e_filt is not None:
        loss_pct = fm.get("electronic_sigma_loss_pct", "?")
        msg = (f'σ_e: {sigma_e_full:.3f} → {sigma_e_filt:.3f} mS/cm  '
               f'(loss {loss_pct}%)  '
               f'[{n_excl}/{n_total_am_am} AM-AM excluded]')
    elif sigma_e_full:
        fm['electronic_sigma_full_mScm_fracture_aware'] = 0.0
        fm['electronic_sigma_loss_pct'] = 100.0
        with open(fm_path, 'w') as f:
            json.dump(fm, f, indent=2, default=str)
        msg = (f'σ_e: {sigma_e_full:.3f} → 0 (network disconnected)  '
               f'[{n_excl}/{n_total_am_am} AM-AM excluded]')
    else:
        msg = f'[{n_excl}/{n_total_am_am} AM-AM excluded]'
    return (case_dir.name, True, msg)


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids (default: all)')
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

    print(f'Fracture-aware network solver on {len(cases)} cases '
          f'(threshold F/P_c >= {THRESHOLD_MULTIPLIER}, force-based) …',
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
