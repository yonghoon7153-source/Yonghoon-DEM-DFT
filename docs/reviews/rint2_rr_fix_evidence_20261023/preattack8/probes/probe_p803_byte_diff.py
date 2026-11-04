"""P8-03 / P8-04 — byte_diff_view (RINT2-E01) classification against its own docstring (unit, no runs).

  python3 -I probe_p803_byte_diff.py <tree>
"""
import json
import os
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'scripts'))
import rint_r_chain as RR  # noqa: E402

obj = {'a': {'c': 'x', 'd': [1, 2.5]}, 'b': 1, 'e': None, 'f': True}
new = RR.canon_bytes(obj)


def dumps(o, **kw):
    k = dict(ensure_ascii=False, indent=1, sort_keys=True)
    k.update(kw)
    return (json.dumps(o, **k) + '\n').encode('utf-8')


cases = {
    # JSON type change (number 1 -> true): docstring "value = 파싱한 값이 다름"
    'int_to_true': dumps(dict(obj, b=True)),
    # JSON type change (true -> 1)
    'true_to_int': dumps(dict(obj, f=1)),
    # JSON type change (true -> 1.0)
    'true_to_float': dumps(dict(obj, f=1.0)),
    # -0.0 (documented as format)
    'neg_zero': dumps(dict(obj, b=-0.0)),
    # value change AND missing final newline (E18i shape: json.dump without '\n')
    'value_and_no_nl': dumps(dict(obj, b=2))[:-1],
    # value change AND key order change AND CRLF
    'value_order_crlf': (json.dumps(dict(reversed(list(dict(obj, b=2).items()))), ensure_ascii=False, indent=1) + '\n').replace('\n', '\r\n').encode(),
    # duplicate key with a different first value (reader keeps the last)
    'dup_key_diff_first': new.replace(b'"b": 1,', b'"b": 999,\n "b": 1,'),
    # UTF-8 BOM in front of an otherwise identical file
    'bom': b'\xef\xbb\xbf' + new,
    # NaN where the canonical file has null
    'nan_for_null': new.replace(b'"e": null', b'"e": NaN'),
}
out = {}
for nm, old in cases.items():
    try:
        v = RR.byte_diff_view(old, new)
    except Exception as e:                       # noqa: BLE001
        v = f'EXC {type(e).__name__}: {e}'
    out[nm] = v

# results_differ / results_keys_differ / grade_differ semantics in reverify_report (same Python-equality)
r0 = json.loads(cases['int_to_true'].decode())
r1 = json.loads(new.decode())
out['_python_equality'] = {'r0 == r1 (true vs 1)': r0 == r1, 'results_keys_differ would be': sorted(k for k in set(r0) | set(r1) if r0.get(k) != r1.get(k))}

# deep nesting: does the report path crash (RecursionError not in the except list)?
deep = b'[' * 200000 + b']' * 200000
try:
    RR.byte_diff_view(deep, new)
    out['deep_nesting'] = 'no exception'
except Exception as e:                           # noqa: BLE001
    out['deep_nesting'] = f'EXC {type(e).__name__}'
print(json.dumps(out, ensure_ascii=False, indent=1))
