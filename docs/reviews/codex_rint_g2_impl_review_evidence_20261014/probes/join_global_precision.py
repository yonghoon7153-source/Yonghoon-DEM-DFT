from pathlib import Path
import gzip
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source/scripts'))
import rint_iface_join as J

D = ROOT / 'source/docs/data'
SC = D / 'real14_am_scaffold.csv'
AT = D / 'real14_reference_20260928/atom_2060000.liggghts.gz'
CT = D / 'real14_reference_20260928/contact_2060000.liggghts.gz'
TMP = ROOT / 'tmp/join_global_precision'
TMP.mkdir(parents=True, exist_ok=True)
result = {}
for name, p, header, col in [('atom', AT, 'ITEM: ATOMS', 2), ('contact', CT, 'ITEM: ENTRIES', 0)]:
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        lines = f.read().splitlines()
    i = next(i for i, line in enumerate(lines) if line.startswith(header)) + 1
    tokens = lines[i].split()
    before = tokens[col]
    assert 'e' not in before and '.' in before
    tokens[col] = before + '0000000000'
    lines[i] = ' '.join(tokens)
    out = TMP / (name + '.dump')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    j = J.am_iface_join(SC, out if name == 'atom' else AT, out if name == 'contact' else CT,
                        type_map={1:'AM_P', 2:'AM_S', 3:'SE'})
    result[name] = {'before': before, 'after': tokens[col], 'equal_numeric_values': float(before) == float(tokens[col]),
                    'status': j['status'], 'rejections': j['rejections'], 'g_geo':j['g_geo'], 'g_frame':j['g_frame']}
    print(name, j['status'], [(r['code'],r['n']) for r in j['rejections']], flush=True)
p = ROOT / 'evidence/join_global_precision.json'
p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(p)
