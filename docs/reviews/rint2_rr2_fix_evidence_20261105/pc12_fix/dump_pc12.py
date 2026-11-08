"""PC12A–E 다섯 검사의 판정 (ok · 전체 bad 사전 · n) 을 자르지 않고 JSON 으로 — python3 dump_pc12.py <scripts 폴더> <out.json>."""
import json
import pathlib
import shutil
import sys
import tempfile

scripts, out = sys.argv[1], sys.argv[2]
cids = sys.argv[3].split(',') if len(sys.argv) > 3 else None
sys.path.insert(0, scripts)
import rint_r_chain as RR          # noqa: E402
import test_rint_r_chain as T      # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pc12_dump_')
try:
    T.fixtures()
    res = {}
    for cid, _title, fn in T.CHECKS:
        if cid.startswith('PC12') and cid != 'PC12' and (cids is None or cid in cids):
            try:
                ok, why = fn()
            except Exception as e:                        # noqa: BLE001
                ok, why = False, f'{type(e).__name__}: {e}'
            res[cid] = {'ok': bool(ok), 'why': why}
    res['_chain_sha256'] = __import__('hashlib').sha256(pathlib.Path(RR.__file__).read_bytes()).hexdigest()
    pathlib.Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1, default=repr, sort_keys=True), encoding='utf-8')
    for k, v in res.items():
        if k.startswith('_'):
            continue
        w = v['why']
        print(k, 'PASS' if v['ok'] else 'FAIL', (w.get('n'), w.get('n_bad'), sorted(w.get('bad', {}))) if isinstance(w, dict) else w)
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
