# -*- coding: utf-8 -*-
"""P7 — 요약 없는 재실행 시도 (정직 대조 같음 뒤 멈춤에서 요약 지움 = 사슬 부모 사망 꼴) 에 attempt.json 형 바꿈:
   resume_of True (원장 1) · resume_of 1.0 · machine 같음 + n 그대로 → ⓐ (`attempt_entry_diff` = `!=` 비교 · 1 == True == 1.0) 이 가르는가.
   대조: resume_of None (원장 1) = [ⓐ] 거부여야."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def mk(val):
    def f(tag):
        atts = T.rr4_two(tag, 'source-ceiling')
        f2 = atts[1][0]
        (Path(f2) / 'ladder_summary.json').unlink()
        T.rr4_att_set(f2, resume_of=val)
        return [atts[0], (f2, None)]
    return f


res = {}
for nm, val in (('resume_of_True', True), ('resume_of_1.0', 1.0), ('resume_of_None', None), ('resume_of_1_honest', 1)):
    o = h.three('P7_' + nm.replace('.', '_'), mk(val))
    o['accepted_all_three'] = h.accepted(o)
    res[nm] = o
# found_attempts_problem (판정 · 합치기) 도 같은 비교 함수
atts = mk(True)('P7_found')
st = T.rr4_state(atts)
res['found_attempts_problem_True'] = RR.found_attempts_problem(st, RR._attempt_folders([Path(atts[0][0]).parent]))
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p7_orphan_types.json', res)
for k, v in res.items():
    if isinstance(v, dict):
        print(k, 'ACCEPTED' if v['accepted_all_three'] else 'rejected', v['writer'], v['places'], v['cli'])
    else:
        print(k, v)
