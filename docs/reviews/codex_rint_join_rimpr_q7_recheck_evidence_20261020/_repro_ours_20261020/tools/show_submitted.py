"""Summarize submitted_{new,old}.json rows: rc, seconds, PASS-line tail (read-only).

Usage: python3 -I show_submitted.py <submitted_*.json> [...]
"""
import json
import sys

for p in sys.argv[1:]:
    rows = json.load(open(p, encoding='utf-8'))
    print('==', p.rsplit('/', 1)[-1])
    for r in rows:
        cmd = r['command']
        name = ' '.join(c.rsplit('/', 1)[-1].rsplit('\\', 1)[-1] for c in cmd[4:])
        tail = [t for t in r['tail'] if t.strip()]
        print(f"  rc={r['rc']} {r['seconds']:7.1f}s  {name}")
        for t in tail[-3:]:
            print('       |', t[:160])
