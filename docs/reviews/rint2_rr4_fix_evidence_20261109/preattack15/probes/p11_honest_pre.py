# -*- coding: utf-8 -*-
"""P11 — 정직 꼴: 사슬 가운데 결과 전 멈춘 재실행 (시도 2 = 원천 1 에서 재실행 · 복사 전에 멈춤 · payload 없음 = 결과 전 · `adoption` 이 건너뜀) → 시도 3 = 다시
   원천 1 (그 시점 유효 사슬 끝 = 1) 에서 재실행 (대조 같음 뒤 L03 런 전 TIME_LIMIT).  기대 = 세 자리 자격 True · 통과 (from 1 = effective 1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def H8(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    f2 = T.rr4_att(base / 'attempt_2', 2, 1)
    s2 = T.rr4_put(f2, {'status': 'STOPPED', 'stop': {'code': 'RESUME_NOT_ALLOWED', 'run': h.N1, 'reason': None}, 'runs': [],
                        'resume': {'from': 1, 'copied': [], 'rerun': None, 'compared': [], 'determinism': None}})
    a3 = T.rr4_resume(a1[0], base / 'attempt_3', 3, 1, 'source-ceiling')
    return [a1, (f2, s2), a3]


o = h.three('H8_pre_in_chain', H8)
o['accepted_all_three'] = h.accepted(o)
sm = H8('H8_shape')
o['attempt2_fields'] = RR.result_fields(sm[1][0], sm[1][1])
o['adoption'] = RR.adoption(T.rr4_state(sm), 'ladder:P0')
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p11_honest_pre.json', o)
print('accepted', o['accepted_all_three'], o['writer'], o['places'], o['cli'], '| a2', o['attempt2_fields'], '| adoption', {k: o['adoption'][k] for k in ('chain', 'effective', 'problems')})
