#!/usr/bin/env python3
"""Export EVERY metric of EVERY case to one wide master CSV — for interaction /
regression analysis (not just porosity).

Reads, per case dir under the webapp results/ (+ archive/) tree:
  • meta.json          — readable name, mode, P:S ratio, scale
  • input_params.json  — design knobs (AM:SE wt%, radii, pressure, …) if present
  • full_metrics.json  — the full network/structure metric set (the dashboard source)
  • mpm_payload.json / mpm_metrics.json — MPM porosity/coverage/thickness (mpm_* cols)

Every scalar (int/float/str/bool) becomes a column; nested dicts are flattened to
dot-keys up to depth 2 (so validation_flags.* / stage_e_source.* are captured);
lists are skipped (kept tractable).  The header is the UNION of all keys seen, so
the CSV adapts to whatever the solver wrote — no hard-coded key list to drift.

Paths honor the SAME env as the webapp (WEBAPP_RESULTS_FOLDER / _ARCHIVE_FOLDER,
loaded from webapp/.env) so a worktree runner whose data lives in a shared dir is
found with no symlink.

  python3 scripts/export_master_csv.py [--out docs/data/case_master.csv] [--archive]
  # then analyse: pandas.read_csv(...).corr(), seaborn.pairplot, statsmodels OLS w/ interactions
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'

# Mirror app.py / run_network_full_corrections.py: load .env then honor env paths.
_envf = WEBAPP / '.env'
if _envf.exists():
    for _l in _envf.read_text().splitlines():
        _l = _l.strip()
        if _l and not _l.startswith('#') and '=' in _l:
            _k, _v = _l.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())
RESULTS_DIR = Path(os.environ.get('WEBAPP_RESULTS_FOLDER') or (WEBAPP / 'results'))
ARCHIVE_DIR = Path(os.environ.get('WEBAPP_ARCHIVE_FOLDER') or (WEBAPP / 'archive'))
UPLOADS_DIR = Path(os.environ.get('WEBAPP_UPLOAD_FOLDER') or (WEBAPP / 'uploads'))


def _load(path: Path) -> dict:
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception:
        return {}


def _flatten(d, prefix='', out=None, depth=0, maxdepth=2):
    """Flatten scalars + nested dicts (to maxdepth) into dot-keyed columns.
    Lists are skipped — they're not regression features and bloat the CSV."""
    if out is None:
        out = {}
    if not isinstance(d, dict):
        return out
    for k, v in d.items():
        key = f'{prefix}{k}'
        if isinstance(v, bool) or isinstance(v, (int, float, str)) or v is None:
            out[key] = v
        elif isinstance(v, dict) and depth < maxdepth:
            _flatten(v, key + '.', out, depth + 1, maxdepth)
        # lists / deep dicts: skip
    return out


def discover_cases(include_archive: bool) -> list[Path]:
    roots = [RESULTS_DIR] + ([ARCHIVE_DIR] if include_archive else [])
    seen, out = set(), []
    for root in roots:
        if not root.exists():
            continue
        for fm in root.rglob('full_metrics.json'):
            cd = fm.parent
            if cd not in seen:
                seen.add(cd)
                out.append(cd)
    return sorted(out)


def row_for(case_dir: Path) -> dict:
    row: dict = {'case': case_dir.name}
    # meta (also try the parallel uploads/<cid>/meta.json the solver uses)
    meta = _load(case_dir / 'meta.json') or _load(UPLOADS_DIR / case_dir.name / 'meta.json')
    row['name'] = meta.get('name', case_dir.name)
    for k in ('mode', 'ps_ratio', 'scale', 'created'):
        if k in meta:
            row[f'meta.{k}'] = meta[k]
    # derive AM_P fraction p_frac from "P:S = a:b" style ps_ratio if present
    m = re.search(r'(\d+)\s*:\s*(\d+)', str(meta.get('ps_ratio', '')))
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        if a + b > 0:
            row['p_frac'] = round(a / (a + b), 4)
    # design knobs
    _flatten(_load(case_dir / 'input_params.json'), 'inp.', row)
    # full metric set (the bulk)
    _flatten(_load(case_dir / 'full_metrics.json'), '', row)
    # MPM — merge the standalone sim metrics (mpm_metrics.json, raw 26 fields) with
    # the webapp payload's authoritative table dict (mpm_payload.json -> mpm_metrics),
    # payload winning on overlap.  Captures porosity/thickness/coverage/SE-frac/strain.
    mpm_raw = _load(case_dir / 'mpm_metrics.json')
    payload = _load(case_dir / 'mpm_payload.json')
    pm = payload.get('mpm_metrics') if isinstance(payload.get('mpm_metrics'), dict) else {}
    _flatten({**mpm_raw, **pm}, 'mpm.', row)
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='docs/data/case_master.csv')
    ap.add_argument('--archive', action='store_true',
                    help='also include webapp/archive cases (default: results only)')
    a = ap.parse_args()

    cases = discover_cases(a.archive)
    if not cases:
        raise SystemExit(f'no full_metrics.json under {RESULTS_DIR}'
                         + (f' or {ARCHIVE_DIR}' if a.archive else '')
                         + ' — set WEBAPP_RESULTS_FOLDER (.env) to your data dir')
    rows = [row_for(c) for c in cases]

    # union of all keys → stable header (id cols first, then sorted rest)
    head = ['case', 'name', 'p_frac']
    rest = sorted({k for r in rows for k in r} - set(head))
    cols = head + rest

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f'wrote {out}  ({len(rows)} cases × {len(cols)} columns)')
    print(f'  results dir: {RESULTS_DIR}')
    print(f'  sample columns: {", ".join(cols[:12])} …')


if __name__ == '__main__':
    main()
