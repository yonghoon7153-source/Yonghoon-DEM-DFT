#!/usr/bin/env python3
"""
Backfill warnings field on all already-persisted full_metrics.json files.

Why: analyze_contacts.py checked electronic_active_fraction BEFORE the
network solver ran, so the warning was never stored. The app-level fix
(_refresh_post_network_warnings in webapp/app.py) only applies to newly
analysed cases. This script replays the same warning logic over the 59
existing results to backfill.

Rules applied:
  • <10%  → critical  electronic_dead       (AM-AM percolation 없음)
  • <50%  → critical  electronic_low        (대량 dead AM)
  • <80%  → warning   electronic_marginal   (일부 dead AM)

Preserves:
  • any existing warnings (dedup by type)
  • disabled_warnings filter
  • warnings emitted by analyze_contacts.py for porosity/CN/tau/etc.

Usage:
  python3 scripts/refresh_warnings.py                     # all cases
  python3 scripts/refresh_warnings.py 260421_213656_78ec86  # selected
"""
from __future__ import annotations
import os, sys, json, glob


RESULTS = 'webapp/results'


def refresh_one(case_id: str) -> tuple[str, int]:
    fm_path = os.path.join(RESULTS, case_id, 'full_metrics.json')
    if not os.path.exists(fm_path):
        return 'no_full_metrics', 0
    try:
        with open(fm_path) as f:
            m = json.load(f)
    except Exception as e:
        return f'parse_error:{e}', 0

    existing = list(m.get('warnings') or [])
    known_types = {w.get('type') for w in existing if isinstance(w, dict)}
    disabled = set(m.get('disabled_warnings') or [])
    new_w = []

    el_active = m.get('electronic_active_fraction')
    if el_active is not None:
        pct = el_active * 100
        if pct < 10 and 'electronic_dead' not in known_types:
            new_w.append({
                'type': 'electronic_dead', 'severity': 'critical',
                'msg': f"Electronic Active AM={pct:.0f}% (<10%): 도전재 필수! AM-AM percolation 없음"})
        elif pct < 50 and 'electronic_low' not in known_types:
            new_w.append({
                'type': 'electronic_low', 'severity': 'critical',
                'msg': f"Electronic Active AM={pct:.0f}% (<50%): 대량 dead AM, 도전재 강력 권장"})
        elif pct < 80 and 'electronic_marginal' not in known_types:
            new_w.append({
                'type': 'electronic_marginal', 'severity': 'warning',
                'msg': f"Electronic Active AM={pct:.0f}% (<80%): 일부 dead AM, 도전재 권장"})

    merged = [w for w in (existing + new_w) if w.get('type') not in disabled]
    m['warnings'] = merged
    m['warning_count'] = len(merged)

    with open(fm_path, 'w') as f:
        json.dump(m, f, indent=2, default=str)

    return 'ok', len(new_w)


def main():
    if not os.path.isdir(RESULTS):
        print(f'ERROR: {RESULTS} not found (run from project root)')
        sys.exit(1)

    if len(sys.argv) > 1:
        case_ids = sys.argv[1:]
    else:
        case_ids = sorted(os.listdir(RESULTS))

    stats = {'ok': 0, 'no_full_metrics': 0}
    added_total = 0
    print(f'Refreshing warnings for {len(case_ids)} case(s)...\n')
    for cid in case_ids:
        status, added = refresh_one(cid)
        stats[status] = stats.get(status, 0) + 1
        added_total += added
        if added > 0:
            # Reload to show which warning was added
            fm = os.path.join(RESULTS, cid, 'full_metrics.json')
            try:
                wm = json.load(open(fm)).get('warnings', [])
                tags = ','.join(w.get('type', '?') for w in wm) or '—'
            except Exception:
                tags = '?'
            print(f'  [{status:16s}]  +{added}  {cid}  [{tags}]')

    print()
    print(f'Summary:')
    print(f'  Cases processed:  {stats.get("ok", 0)}')
    print(f'  No full_metrics:  {stats.get("no_full_metrics", 0)}')
    print(f'  New warnings:     {added_total}')


if __name__ == '__main__':
    main()
