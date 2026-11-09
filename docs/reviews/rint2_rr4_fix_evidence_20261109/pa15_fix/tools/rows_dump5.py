# -*- coding: utf-8 -*-
"""고침 C (사전 공격 15 처분) — 상주 시험 행 값 내보내기: 사슬 = argv[1] 의 scripts/rint_r_chain.py · 시험 = argv[2] 의 scripts/test_rint_r_chain.py (기본 = 같은 트리)
→ argv[3] (JSON) 에 RR5A–F (+ RR4D) 의 행마다 값 · 기대 · 같음.  사슬 · 시험 판을 갈라 "고친 시험 × 바탕 사슬" (시험 먼저) 을 잰다."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

chain_tree = Path(sys.argv[1]).resolve()
test_tree = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 and sys.argv[2] != '-' else chain_tree
out = Path(sys.argv[3]) if len(sys.argv) > 3 else None
sys.path.insert(0, str(test_tree / 'scripts'))
spec = importlib.util.spec_from_file_location('rint_r_chain', str(chain_tree / 'scripts' / 'rint_r_chain.py'))
RR = importlib.util.module_from_spec(spec)
sys.modules['rint_r_chain'] = RR
spec.loader.exec_module(RR)
import test_rint_r_chain as T  # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='rr5_rows_')
with contextlib.redirect_stdout(io.StringIO()):
    T.fixtures()
res = {'chain': str(chain_tree / 'scripts' / 'rint_r_chain.py'), 'test': str(test_tree / 'scripts' / 'test_rint_r_chain.py'), 'checks': {}}
for cid, title, fn in T.CHECKS:
    if not (cid.startswith('RR5') or cid == 'RR4D'):
        continue
    try:
        ok, info = fn()
    except Exception as e:                                    # noqa: BLE001
        ok, info = False, f'exc {type(e).__name__}: {e}'
    res['checks'][cid] = {'ok': ok, 'info': info}
    if isinstance(info, dict) and 'got' in info:
        print(cid, 'PASS' if ok else 'FAIL', 'n', info['n'], 'bad', info['bad_names'])
        for k, v in info['got'].items():
            print('   ', k, json.dumps(v, ensure_ascii=False, default=str)[:220])
    else:
        print(cid, 'PASS' if ok else 'FAIL', json.dumps(info, ensure_ascii=False, default=str)[:600])
if out:
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
