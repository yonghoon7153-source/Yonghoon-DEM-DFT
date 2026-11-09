# -*- coding: utf-8 -*-
"""P15 — 다음 재개 허용 자리 (`attempt_order_problem` → `resume_chain_provenance_problem`) 는 요약 꼴 검사 없이 공통 검증을 부른다: 손으로 쓴 결과 줄 (resume_ok True ·
   요약 sha = 지금 폴더) + 요약 runs = 정수 → `--add --resume` 자리에서 Stop 이 아니라 TypeError 인가."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR
out = {}
for nm, fn in (('runs_int', lambda s: s.update(runs=5)), ('stop_str', lambda s: s.update(stop='x'))):
    atts = T.rr4_two(f'P15_{nm}', 'source-ceiling')
    lines = T.rr4_lines(atts)                                   # 결과 줄 2 = 정직 요약으로 셈 (resume_ok True)
    f2 = Path(atts[1][0])
    s = json.loads((f2 / 'ladder_summary.json').read_text(encoding='utf-8'))
    fn(s)
    (f2 / 'ladder_summary.json').write_bytes(RR.canon_bytes(s))
    r2 = [x for x in lines if x.get('kind') == 'result' and x['n'] == 2][0]
    r2['folder_sha256'] = RR.folder_digest(f2)                  # 손 고침 = 요약 sha 를 지금 폴더로
    st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in lines).encode('utf-8'))
    try:
        o = RR.attempt_order_problem(st, T.rr4_next(st), T.RR4_PLAN)
        out[nm] = ['returned', o[0] if o else None, (o[1][:160] if o else None)]
    except RR.Stop as e:
        out[nm] = ['Stop', e.code]
    except Exception as e:  # noqa: BLE001
        out[nm] = ['EXC', f'{type(e).__name__}: {e}'[:160]]
    try:
        c = RR.resume_chain_problem(st, T.rr4_next(st), 3, f2.parent)
        out[nm + '_chain'] = ['returned', c[0] if c else None]
    except Exception as e:  # noqa: BLE001
        out[nm + '_chain'] = ['EXC', f'{type(e).__name__}: {e}'[:160]]
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p15_order_crash.json', out)
print(json.dumps(out, ensure_ascii=False))
