# -*- coding: utf-8 -*-
"""P6 — 원천 폴더 링크 (결과 줄 · 원장을 다 만든 뒤 원천 attempt_1 을 같은 내용 사본에 대한 심볼릭 링크로 바꿈) → 세 자리 (쓰기 직접 · 차례 · 사슬 · 실제 recover CLI).
   기대 = [원천] 거부 (`resume_source_locate` 링크 아님) · 예외 없이."""
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def to_link(f1):
    f1 = Path(f1)
    real = f1.parent.parent / (f1.parent.name + '_real_attempt_1')
    shutil.copytree(f1, real, symlinks=True)
    shutil.rmtree(f1)
    os.symlink(str(real), str(f1))


out = {}
# 쓰기 (직접)
atts = T.rr4_two('P6_w', 'source-ceiling')
st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in T.rr4_lines(atts, last_result=False)).encode('utf-8'))
to_link(atts[0][0])
try:
    line, why = RR.attempt_result(2, atts[1][0], atts[1][1], 'recover', st)
    out['writer'] = [line['resume_ok'], T.rr4_tag(why)]
except Exception as e:  # noqa: BLE001
    out['writer'] = f'exc {type(e).__name__}: {e}'[:300]
# 차례 · 사슬
atts = T.rr4_two('P6_p', 'source-ceiling')
st = T.rr4_state(atts)
to_link(atts[0][0])
nx = T.rr4_next(st)
for nm, fn in (('order', lambda: RR.attempt_order_problem(st, nx, T.RR4_PLAN)),
               ('chain', lambda: RR.resume_chain_problem(st, nx, 3, Path(atts[-1][0]).parent))):
    try:
        o = fn()
        out[nm] = [o[0], T.rr4_tag(o[1]), o[1][:200]] if o else None
    except Exception as e:  # noqa: BLE001
        out[nm] = f'exc {type(e).__name__}: {e}'[:300]
# 실제 recover CLI (원장 줄 = rr4_cli 와 같은 손 줄 · recover 전에 링크)
atts = T.rr4_two('P6_c', 'source-ceiling')
d, _rc, _so = T.led_new('PA15_P6_c')
head = T.led_lines(d)[0]
c0 = T.git_(d, 'rev-parse', 'HEAD')
for f, _s in atts:
    T.rr4_att_set(f, ledger_commit=c0)
for x in T.rr4_lines(atts, head_plan=head['plan_sha256'], last_result=False)[1:]:
    T.led_hand(d, x)
to_link(atts[0][0])
rc, so = T.call(['--stage', 'recover', '--out', str(atts[1][0]), '--ledger', str(d)])
r = T.led_result(d, 2) or {}
out['cli'] = [rc, r.get('resume_ok'), T.rr4_tag(T.git_(d, 'log', '-1', '--format=%B'))]
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p6_src_link.json', out)
print(json.dumps(out, ensure_ascii=False, indent=1))
