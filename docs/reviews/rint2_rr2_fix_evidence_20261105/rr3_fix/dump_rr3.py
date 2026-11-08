"""RR3 검사 (RR3A–E · RR3P · 고정물 바꾼 CT06 · PC12C) 의 판정 (ok · 자르지 않은 bad · 행) 을 JSON 으로 — python3 dump_rr3.py <scripts 폴더> <out.json> [검사,…]."""
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

scripts, out = sys.argv[1], sys.argv[2]
cids = sys.argv[3].split(',') if len(sys.argv) > 3 else ['RR3A', 'RR3B', 'RR3C', 'RR3D', 'RR3E', 'RR3P', 'CT06', 'PC12C']
sys.path.insert(0, scripts)
import rint_r_chain as RR          # noqa: E402
import test_rint_r_chain as T      # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='rr3_dump_')
try:
    T.fixtures()
    res = {}
    for cid, _title, fn in T.CHECKS:
        if cid in cids:
            try:
                ok, why = fn()
            except Exception as e:                        # noqa: BLE001
                ok, why = False, f'{type(e).__name__}: {e}'
            res[cid] = {'ok': bool(ok), 'why': why}
    res['_chain_sha256'] = hashlib.sha256(pathlib.Path(RR.__file__).read_bytes()).hexdigest()
    res['_test_sha256'] = hashlib.sha256(pathlib.Path(T.__file__).read_bytes()).hexdigest()
    pathlib.Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1, default=repr, sort_keys=True), encoding='utf-8')
    for k, v in sorted(res.items()):
        if k.startswith('_'):
            continue
        w = v['why']
        print(k, 'PASS' if v['ok'] else 'FAIL', (w.get('n'), w.get('n_bad'), sorted(w.get('bad', {}))) if isinstance(w, dict) and 'n' in w else
              ('' if v['ok'] else str(w)[:300]))
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
