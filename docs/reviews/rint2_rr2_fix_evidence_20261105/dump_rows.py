"""Rint ② 회차 ② 고침 (11-05) 증거 — 사슬 시험 (`scripts/test_rint_r_chain.py`) 의 검사 몇 개를 그 시험의 틀 그대로 (고정물 · 임시 폴더) 돌려
검사마다 (통과 bool, 사유 객체) 를 자르지 않고 JSON 으로 남긴다 (시험 화면은 사유를 600 자에서 자른다).  시험 · 사슬 코드는 바꾸지 않는다.

  python3 dump_rows.py <작업 트리> <출력.json> <검사 이름 쉼표>
"""
import json
import shutil
import sys
import tempfile
import time
import traceback
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
IDS = [x for x in sys.argv[3].split(',') if x]
sys.path.insert(0, str(TREE / 'scripts'))
import test_rint_r_chain as T                                   # noqa: E402
import rint_r_chain as RR                                       # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='rint_rr2_dump_')
res = {'tree': str(TREE), 'chain_sha256': __import__('hashlib').sha256((TREE / 'scripts' / 'rint_r_chain.py').read_bytes()).hexdigest(),
       'test_sha256': __import__('hashlib').sha256((TREE / 'scripts' / 'test_rint_r_chain.py').read_bytes()).hexdigest(), 'checks': {}}
t0 = time.time()
try:
    T.fixtures()
    for cid, title, fn in T.CHECKS:
        if cid not in IDS:
            continue
        try:
            ok, why = fn()
        except Exception as e:                                  # noqa: BLE001
            ok, why = False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:200]}'
        res['checks'][cid] = {'pass': bool(ok), 'why': why}
        print(f'  {"PASS" if ok else "FAIL"}  {cid}')
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
res['seconds'] = round(time.time() - t0, 1)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True, default=repr) + '\n', encoding='utf-8')
print(f'→ {OUT} ({res["seconds"]} s)')
