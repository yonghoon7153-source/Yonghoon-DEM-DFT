# -*- coding: utf-8 -*-
"""P14 — 예외: 공통 검증을 직접 부를 때 잡히지 않는 예외가 나는 요약 꼴 (runs = 정수 · stop = 글 · copied_from 큰 정수 · from 음수 · 이름 없는 복사 기록) 과
   그 꼴이 실제 쓰기 자리 (recover CLI) · 다음 재개 자리 (차례 · 사슬) 에 닿는가 (traceback 이면 rc 1 · 화면 Traceback)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def edits():
    return {
        'runs_int': lambda s: s.update(runs=5),
        'stop_str': lambda s: s.update(stop='x'),
        'copied_from_huge': lambda s: s['runs'][0].update(copied_from=10 ** 30),
        'from_negative': lambda s: s['resume'].update({'from': -1}),
        'copy_no_name': lambda s: s['runs'][0].pop('name'),
        'resume_list': lambda s: s.update(resume=[1, 2]),
    }


res = {}
for nm, fn in edits().items():
    row = {}
    atts = T.rr4_two(f'X_{nm}_d', 'source-ceiling')
    st = T.rr4_state(atts)
    s = json.loads(json.dumps(atts[1][1]))
    fn(s)
    try:
        row['direct'] = (RR.resume_provenance_problem(st, 2, atts[1][0], s) or '')[:120] or None
    except Exception as e:  # noqa: BLE001
        row['direct'] = f'EXC {type(e).__name__}: {e}'[:160]
    o = h.three(f'X_{nm}', lambda t, fn=fn: T.rr4_edit(T.rr4_two(t, 'source-ceiling'), fn))
    row['three'] = {'writer': o['writer'] if not isinstance(o['writer'], list) else o['writer'][0],
                    'places': o['places'] if not isinstance(o['places'], list) else o['places'][:3],
                    'cli': o['cli'] if not isinstance(o['cli'], list) else o['cli'][:3]}
    res[nm] = row
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p14_exceptions.json', res)
for k, v in res.items():
    print(k, '| direct:', v['direct'], '| three:', json.dumps(v['three'], ensure_ascii=False, default=str)[:400])
