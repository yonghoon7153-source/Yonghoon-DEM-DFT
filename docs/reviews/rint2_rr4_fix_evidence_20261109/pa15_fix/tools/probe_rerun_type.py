# -*- coding: utf-8 -*-
"""고침 C 자기 점검 — ⑤ (`resume_rerun_problem`) 의 다시 대조가 요약 resume.rerun 이름을 `run_dirs` 에 넘긴다 (옛 = 기록 outdir 글).  rerun · 첫 새 런 이름이 글이
아닌 꼴 (정수 · 목록 · null) · 요청 칸 없는 기록 · 요청 칸 있는 기록 → `result_fields` · `stop_cause` 가 사유로 끝나나 (traceback 없음) 를 잰다.
쓰임: python3 probe_rerun_type.py <코드 트리>"""
import contextlib
import copy
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'scripts'))
spec = importlib.util.spec_from_file_location('rint_r_chain', str(tree / 'scripts' / 'rint_r_chain.py'))
RR = importlib.util.module_from_spec(spec)
sys.modules['rint_r_chain'] = RR
spec.loader.exec_module(RR)
import test_rint_r_chain as T  # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='rr5_type_')
with contextlib.redirect_stdout(io.StringIO()):
    T.fixtures()

out = {}
for nm, val, drop_arms in (('control', 'L02_ceiling', False), ('int5', 5, False), ('int5_noarms', 5, True), ('list', ['L02_ceiling'], True), ('none', None, True),
                           ('float', 2.0, True), ('str_other', 'L02_ceilingQ', True)):
    atts = T.rr4_two(f'T_{nm}', 'source-ceiling')
    f, s = atts[-1]
    s = copy.deepcopy(s)
    s['runs'][1]['name'] = val
    s['resume']['rerun'] = val
    if drop_arms:
        s['runs'][1].pop('arms', None)
    T.rr4_put(f, s)
    try:
        r = RR.result_fields(f, s)
        out[nm] = ['ok', r['resume_ok'], r['side'], RR.stop_cause(s, f), RR.stop_record_problem(s, f)]
    except Exception as e:                                    # noqa: BLE001
        out[nm] = ['exc', f'{type(e).__name__}: {e}'[:200]]
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
