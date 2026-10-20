"""Classify structure_results.json cases (read-only).

Usage: python3 -I structure_summary.py <structure_results.json>
"""
import json
import sys
from collections import Counter

d = json.load(open(sys.argv[1], encoding='utf-8'), parse_constant=float)
res = d['results']
st = Counter(r['status'] for r in res)
exc = Counter(r.get('exception') for r in res if r['status'] == 'EXCEPTION')
up = [r['case'] for r in res if r.get('unexpected_pass')]
ur = [r['case'] for r in res if r.get('unexpected_reject')]
pos = [r['case'] for r in res if r['status'] == 'PASS' and not r.get('unexpected_pass')]
guard = Counter(r.get('quantitative_guard') for r in res)
print('n', len(res), 'status', dict(st), 'exceptions', dict(exc))
print('expected positives (PASS, not unexpected)', len(pos))
print('unexpected_pass (header false-PASS)', len(up), up)
print('unexpected_reject', len(ur), ur)
print('quantitative_guard', dict(guard))
for r in res:
    if r['case'] in ('real14', 'case15'):
        g = r['g_geo']
        print(r['case'], r['status'], {k: g.get(k) for k in ('n_scaffold', 'n_dump_am', 'n_matched')},
              'entrance' in r and r['entrance'] and {k: r['entrance'].get(k) for k in ('n_rows_physical',) if k in r['entrance']})
prior_pass = [r['case'] for r in res if r.get('unexpected_pass') and r.get('prior', {}).get('status') == 'PASS']
print('header false-PASS also PASS on prior pin:', len(prior_pass))
