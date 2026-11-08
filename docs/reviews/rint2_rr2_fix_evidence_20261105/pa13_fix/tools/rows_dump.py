"""PA13A–D 행 표 전부 (시험 모듈을 라이브러리로 · 결과 = JSON) — 고치기 전 · 뒤 증거 (시험 출력은 600 자에서 자른다)."""
import json
import os
import sys
import tempfile

SCRIPTS = os.environ['PA13_SCRIPTS']
sys.path.insert(0, SCRIPTS)
import rint_r_chain as RR          # noqa: E402
import test_rint_r_chain as T      # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa13rows_')
T.fixtures()
out = {}
for cid, _title, fn in T.CHECKS:
    if not cid.startswith('PA13'):
        continue
    try:
        ok, why = fn()
    except Exception as e:                                  # noqa: BLE001
        ok, why = False, f'{type(e).__name__}: {e}'
    out[cid] = {'pass': bool(ok), 'detail': why}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
