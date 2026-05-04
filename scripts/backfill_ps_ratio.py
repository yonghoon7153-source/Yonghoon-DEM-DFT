#!/usr/bin/env python3
"""Backfill `ps_ratio` (AM_P:AM_S mass/volume ratio) into per-case meta.json
by computing AM_P volume fraction directly from atoms.csv + type_map.

Why this exists
───────────────
The `ps_ratio` form field on upload was inconsistently filled, so 80/80
cases lack it in their meta.json. This blocks Section 7 analysis:

  - Pearson(AM_P_volume_fraction → σ_e_loss) regression: n=0
  - 2D pivot (P:S band × r_SE band): all cases collapse into single band

Volume fractions are deterministic from the existing data: each atom's
volume ∝ r³, and the type_map labels which particles are AM_P vs AM_S.
So we compute it from the source of truth (atoms.csv) instead of asking
the user to remember historical synthesis ratios.

Output
──────
Writes into each case's meta.json (creates if absent):
  ps_ratio       : 'P:S' string label like '7:3', '5:5', '3:7', '10:0', '0:10'
  ps_frac_AM_P   : float — AM_P volume / (AM_P + AM_S) volume
  ps_source      : 'computed_from_atoms.csv'  (audit trail)

If meta.json already has a ps_ratio set by the upload form, it is
preserved unless --force is given.

Usage:
  python3 scripts/backfill_ps_ratio.py
  python3 scripts/backfill_ps_ratio.py --force   # overwrite existing
  python3 scripts/backfill_ps_ratio.py --quiet
  python3 scripts/backfill_ps_ratio.py CID …
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'


def discover_case_dirs() -> list[Path]:
    """Recursively find case dirs at any depth under results/ or archive/."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            case_dir = atoms_p.parent
            if case_dir not in seen:
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    """Try the canonical meta.json locations in order."""
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def _meta_path(case_dir: Path) -> Path:
    """Return the meta.json path to write to (prefers in-case-dir copy)."""
    p1 = case_dir / 'meta.json'
    p2 = WEBAPP / 'uploads' / case_dir.name / 'meta.json'
    if p1.exists():
        return p1
    if p2.exists():
        return p2
    return p1


def _parse_type_map(s: str) -> dict:
    out = {}
    for tok in (s or '').split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                out[int(k.strip())] = v.strip()
            except Exception:
                pass
    return out


def _vol_frac_AM_P(atoms_df: pd.DataFrame, type_map: dict) -> float | None:
    """Return AM_P volume fraction in [0, 1] (or None if no AM particles).

    Volume ∝ r³ per particle. We use volume rather than count because
    secondary AM_P (5–12 μm) is much larger than AM_S (1–3 μm) and the
    paper's P:S labels (7:3, 5:5 …) are conventional volume/mass ratios,
    not number ratios.
    """
    am_p_types = {tid for tid, lbl in type_map.items() if lbl == 'AM_P'}
    am_s_types = {tid for tid, lbl in type_map.items() if lbl == 'AM_S'}
    if not am_p_types and not am_s_types:
        return None  # bimodal-only case with no AM, skip
    if 'type' not in atoms_df.columns or 'radius' not in atoms_df.columns:
        return None

    r3 = atoms_df['radius'].astype(float) ** 3
    v_p = float(r3[atoms_df['type'].isin(am_p_types)].sum()) if am_p_types else 0.0
    v_s = float(r3[atoms_df['type'].isin(am_s_types)].sum()) if am_s_types else 0.0
    total = v_p + v_s
    if total <= 0:
        return None
    return v_p / total


def _ps_label(frac_p: float) -> str:
    """Snap continuous AM_P fraction to nearest canonical P:S label.

    Uses 1-decimal rounding (10 % buckets) since human-readable labels are
    customary in the paper:
      0:10, 1:9, 2:8, …, 9:1, 10:0
    """
    p10 = round(frac_p * 10)
    s10 = 10 - p10
    return f'{p10}:{s10}'


def backfill_one(case_dir: Path, force: bool = False) -> tuple[str, str, str]:
    """Return (case_id, status, message). status ∈ {'updated','skipped','no-am','error'}."""
    meta_p = _meta_path(case_dir)
    meta = _read_meta(case_dir)

    existing = (meta.get('ps_ratio') or '').strip()
    if existing and not force:
        return (case_dir.name, 'skipped',
                f'has ps_ratio={existing!r} (use --force to overwrite)')

    type_map = _parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

    try:
        atoms = pd.read_csv(case_dir / 'atoms.csv', usecols=['type', 'radius'])
    except Exception as e:
        return (case_dir.name, 'error', f'atoms.csv read failed: {e}')

    frac_p = _vol_frac_AM_P(atoms, type_map)
    if frac_p is None:
        return (case_dir.name, 'no-am',
                'no AM_P/AM_S split (single-AM type or bimodal-SE-only)')

    label = _ps_label(frac_p)
    meta['ps_ratio']     = label
    meta['ps_frac_AM_P'] = round(frac_p, 4)
    meta['ps_source']    = 'computed_from_atoms.csv'

    meta_p.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_p, 'w') as f:
        json.dump(meta, f, indent=2, default=str, ensure_ascii=False)

    return (case_dir.name, 'updated',
            f'ps_ratio={label}  (AM_P frac={frac_p:.3f} from {len(atoms)} atoms)')


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    ap.add_argument('--force', action='store_true',
                    help='Overwrite existing ps_ratio (default: keep)')
    ap.add_argument('--quiet', action='store_true',
                    help='Only print final summary line')
    args = ap.parse_args()

    all_cases = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in all_cases if d.name in wanted]
    else:
        cases = all_cases
    if not cases:
        ap.error('No cases found.')

    if not args.quiet:
        print(f'P:S ratio backfill on {len(cases)} cases  '
              f'(force={args.force}) …', flush=True)

    n_upd = n_skip = n_none = n_err = 0
    label_counts: dict[str, int] = {}
    for i, d in enumerate(cases, 1):
        cid, status, msg = backfill_one(d, force=args.force)
        if status == 'updated':
            n_upd += 1; tag = '✓'
            # extract label for histogram
            label = msg.split('=', 1)[1].split(' ', 1)[0]
            label_counts[label] = label_counts.get(label, 0) + 1
        elif status == 'skipped': n_skip += 1; tag = '·'
        elif status == 'no-am':   n_none += 1; tag = '∅'
        else:                     n_err += 1; tag = '✗'
        if not args.quiet:
            print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:120]}',
                  flush=True)

    print(f'\nDone — {n_upd} updated, {n_skip} kept, '
          f'{n_none} no-AM-split, {n_err} errors.', flush=True)
    if label_counts:
        print('  P:S distribution:')
        for lbl in sorted(label_counts.keys(),
                           key=lambda s: int(s.split(':')[0])):
            print(f'    {lbl:>5s} : {label_counts[lbl]:3d}')


if __name__ == '__main__':
    main()
