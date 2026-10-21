"""Edit only the MXD3 block at the end of docs/reviews/findings.json (re-serialise that block in the file's style).

usage: python3 -I ledger_edit.py <repo_root> <mode>
  mode = evidence   : add the v2 rule-check script (with check id) to MXD3 items that have a check
  mode = v2notes    : append the v2 handling summary to each MXD3 note (from HANDLING below)
"""
import json
import sys

root, mode = sys.argv[1], sys.argv[2]
path = root + '/docs/reviews/findings.json'
txt = open(path, encoding='utf-8').read()
key = ',\n    {\n      "id": "MXD3-01",'
cut = txt.index(key)
assert txt.count(key) == 1
data = json.loads(txt)
F = data['findings']
i0 = next(i for i, f in enumerate(F) if f['id'] == 'MXD3-01')
mine = F[i0:]
assert [f['id'] for f in mine] == [f'MXD3-{n:02d}' for n in range(1, 22)], [f['id'] for f in mine]

EV2 = 'docs/reviews/mixer_d3_design_v2_evidence_20261021/d3_v2_rule_checks.py'
CHECKED = [n for n in range(1, 18) if n != 16]

HANDLING = {}   # filled for mode v2notes from the v2 design §0-2 table (n -> text)

if mode == 'evidence':
    for f in mine:
        n = int(f['id'][5:])
        if n in CHECKED:
            ev = f.setdefault('evidence_tests', [])
            tag = f'{EV2} (C{n:02d})'
            if tag not in ev:
                ev.append(tag)
elif mode == 'v2notes':
    import importlib.util
    spec = importlib.util.spec_from_file_location('h', sys.argv[3])
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    for f in mine:
        n = int(f['id'][5:])
        add = h.HANDLING[n]
        if add not in f['note']:
            f['note'] = f['note'] + '  ' + add
else:
    raise SystemExit('mode?')

block = ''.join(',\n' + '\n'.join('    ' + ln for ln in json.dumps(it, ensure_ascii=False, indent=2).split('\n'))
                for it in mine)
new = txt[:cut] + block + '\n  ]\n}\n'
after = json.loads(new)
assert after['findings'][:i0] == F[:i0]
open(path, 'w', encoding='utf-8').write(new)
print('ok', mode, len(mine))
