"""P8-03 (real path) — reverify report for a stored results JSON whose value changed JSON type (number <-> boolean).
Fake-runner verdict (s_verdict_main) -> edit verdict_results.json (first boolean -> 1, or first int 0/1 -> false/true) -> --reverify --out
-> report fields.  Restores the file afterwards.

  python3 -I probe_p803b_reverify_type.py <tree>
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_common import setup  # noqa: E402

RR, T = setup(sys.argv[1])
v = T.s_verdict_main()
resp = v['out'] / 'verdict_results.json'
pubp = v['out'] / 'verdict.json'
res0, pub0 = resp.read_bytes(), pubp.read_bytes()
r = json.loads(res0.decode('utf-8'))
hit = []


def flip(o, path=()):
    """first bool -> int (True -> 1 · False -> 0) in document order."""
    if hit:
        return o
    if isinstance(o, dict):
        return {k: flip(x, path + (k,)) for k, x in o.items()}
    if isinstance(o, list):
        return [flip(x, path + (i,)) for i, x in enumerate(o)]
    if isinstance(o, bool):
        hit.append(path)
        return int(o)
    return o


r2 = flip(r)
print('flipped path:', hit)
try:
    resp.write_bytes(RR.canon_bytes(r2))
    rc, so = T.rv_call(v['out'], out=Path(T.TD) / 'runs' / 'P803b_rep')
    rep = T.u_json(Path(T.TD) / 'runs' / 'P803b_rep' / 'reverify_report.json')
    pubp.write_bytes(pub0.replace(b'"sentence_allowed": false', b'"sentence_allowed": 0').replace(b'"sentence_allowed": true', b'"sentence_allowed": 1'))
    resp.write_bytes(res0)
    rc2, so2 = T.rv_call(v['out'], out=Path(T.TD) / 'runs' / 'P803b_rep2')
    rep2 = T.u_json(Path(T.TD) / 'runs' / 'P803b_rep2' / 'reverify_report.json')
finally:
    resp.write_bytes(res0)
    pubp.write_bytes(pub0)
keys = ('result', 'grade_differ', 'public_keys_differ', 'results_differ', 'results_keys_differ', 'results_bytes', 'public_bytes')
print('results JSON bool->int :', rc, json.dumps({k: (rep or {}).get(k) for k in keys}, ensure_ascii=False))
print('verdict JSON sentence_allowed bool->int :', rc2, json.dumps({k: (rep2 or {}).get(k) for k in keys}, ensure_ascii=False))
print('verdict sentence_allowed was:', json.loads(pub0.decode()).get('sentence_allowed'))
