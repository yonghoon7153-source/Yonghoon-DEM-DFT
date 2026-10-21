#!/usr/bin/env python3
"""Key-by-key comparison of two JSON documents (Codex vs ours).

Leaf classes: exact (same type+value) · rel<=1e-12 (both finite numbers) · DIFF (with both values).
Strings that look like filesystem paths are classed 'path' (environment, not a verdict value).
Usage: compare_json.py codex.json ours.json out_report.json [--label NAME] [--ignore-key k ...]
"""
import json, math, re, sys

args = sys.argv[1:]
codex_p, ours_p, out_p = args[0], args[1], args[2]
label = codex_p
ignore = set()
i = 3
while i < len(args):
    if args[i] == '--label':
        label = args[i + 1]; i += 2
    elif args[i] == '--ignore-key':
        ignore.add(args[i + 1]); i += 2
    else:
        raise SystemExit('bad arg ' + args[i])


def load(p):
    with open(p, 'rb') as f:
        b = f.read()
    return json.loads(b.decode('utf-8-sig'))


A, B = load(codex_p), load(ours_p)
stats = {'exact': 0, 'rel_le_1e-12': 0, 'path': 0, 'diff': 0, 'missing_in_ours': 0, 'extra_in_ours': 0, 'type_diff': 0}
rows = []
PATHLIKE = re.compile(r'([A-Za-z]:\\|/tmp/|/home/|\\Users\\|/Users/|Documents\\Codex|scratchpad)')


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def walk(a, b, path):
    last = path.rsplit('.', 1)[-1] if '.' in path else path
    if last in ignore:
        return
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k not in b:
                stats['missing_in_ours'] += 1; rows.append({'key': f'{path}.{k}', 'class': 'missing_in_ours', 'codex': _s(a[k])})
            else:
                walk(a[k], b[k], f'{path}.{k}')
        for k in b:
            if k not in a:
                stats['extra_in_ours'] += 1; rows.append({'key': f'{path}.{k}', 'class': 'extra_in_ours', 'ours': _s(b[k])})
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            rows.append({'key': path, 'class': 'list_len_diff', 'codex_len': len(a), 'ours_len': len(b)})
            stats['diff'] += 1
        for j, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f'{path}[{j}]')
        return
    if num(a) and num(b):
        if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
            stats['exact'] += 1; return
        if a == b and type(a) == type(b):
            stats['exact'] += 1; return
        if a == b:   # int vs float same value
            stats['exact'] += 1; return
        if math.isfinite(a) and math.isfinite(b):
            d = abs(a - b) / max(abs(a), abs(b))
            if d <= 1e-12:
                stats['rel_le_1e-12'] += 1; rows.append({'key': path, 'class': 'rel_le_1e-12', 'codex': a, 'ours': b, 'rel': d}); return
            stats['diff'] += 1; rows.append({'key': path, 'class': 'DIFF', 'codex': a, 'ours': b, 'rel': d}); return
        stats['diff'] += 1; rows.append({'key': path, 'class': 'DIFF', 'codex': a, 'ours': b}); return
    if type(a) != type(b):
        if isinstance(a, str) and isinstance(b, str):
            pass
        else:
            stats['type_diff'] += 1; rows.append({'key': path, 'class': 'type_diff', 'codex': _s(a), 'ours': _s(b)}); return
    if a == b:
        stats['exact'] += 1; return
    if isinstance(a, str) and isinstance(b, str) and (PATHLIKE.search(a) or PATHLIKE.search(b)
                                                      or a.replace('\\', '/') == b.replace('\\', '/')):
        stats['path'] += 1; rows.append({'key': path, 'class': 'path', 'codex': a[:300], 'ours': b[:300]}); return
    stats['diff'] += 1; rows.append({'key': path, 'class': 'DIFF', 'codex': _s(a), 'ours': _s(b)})


def _s(x):
    s = json.dumps(x, ensure_ascii=False)
    return s if len(s) <= 400 else s[:400] + f'...[{len(s)} chars]'


walk(A, B, '$')
rep = {'label': label, 'codex': codex_p, 'ours': ours_p, 'stats': stats, 'rows': rows}
with open(out_p, 'w', encoding='utf-8') as f:
    json.dump(rep, f, ensure_ascii=False, indent=1)
print(label, json.dumps(stats, ensure_ascii=False))
for r in rows:
    if r['class'] not in ('path',):
        print('  ', json.dumps(r, ensure_ascii=False)[:600])
