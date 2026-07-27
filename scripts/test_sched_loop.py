#!/usr/bin/env python3
"""Zive 스케줄 Loop 전개 회귀 테스트 — mpm_input_from_case.expand_sched.

  python3 scripts/test_sched_loop.py      # 종료코드 0=PASS

핵심 불변식 (하나라도 깨지면 산출물이 조용히 덮어써지거나 사이클이 어긋난다):
  ① 실행 순서 = 블록 반복 순서 (cyc1 전체 → cyc2 전체 → …)
  ② 출력명 키 (스텝 idx, cyc) 가 전역 유일  ← 2026-07-27 회귀 버그 지점
  ③ Loop 없는 스케줄은 기존 동작과 동일 (하위호환)
  ④ Loop 블록 안 수동 n 은 무시되고 경고
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpm_input_from_case import expand_sched                      # noqa: E402

C = {'k': 'c', 'r': 2, 'v': 4.3, 'i': 1, 'n': 1}
D = {'k': 'd', 'r': 2, 'v': 2.5, 'n': 1}
R = {'k': 'r', 't': 1, 'n': 1}


def _keys(flat):
    return [(i, c) for i, c, _ in flat]


def main():
    ok = True

    def chk(name, cond, got=''):
        nonlocal ok
        ok &= bool(cond)
        print(f'  {"OK  " if cond else "FAIL"} {name}{("  → " + str(got)) if got else ""}')

    # ① 기본 3사이클: [충, 휴, 방, Loop→1 ×3]
    f = expand_sched([C, R, D, {'k': 'l', 'to': 1, 'n': 3}], warn=None)
    chk('① 순서/사이클 (cyc1 전체 → cyc2 → cyc3)',
        _keys(f) == [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3)], _keys(f))

    # ② 출력명 유일성 — 수동 n 과 Loop 회차가 충돌하던 회귀 케이스
    seq = [dict(C, n=3), D, {'k': 'l', 'to': 1, 'n': 3}]
    f = expand_sched(seq, warn=None)
    names = [f'step4_sched{i:02d}n{c}' for i, c, st in f if st['k'] != 'r']
    chk('② 수동 n=3 + Loop×3 → 이름 충돌 없음', len(names) == len(set(names)), names)
    chk('②b 그 스텝의 cyc 가 1..3 (수동 n 무시)',
        sorted(c for i, c, _ in f if i == 0) == [1, 2, 3])

    # ③ 하위호환: Loop 없으면 수동 n 이 그대로 cyc
    f = expand_sched([dict(C, n=2), dict(D, n=5)], warn=None)
    chk('③ Loop 없음 = 수동 n 보존', _keys(f) == [(0, 2), (1, 5)], _keys(f))

    # ④ 부분 블록 Loop (뒤쪽 일부만 반복)
    f = expand_sched([C, D, {'k': 'l', 'to': 2, 'n': 3}], warn=None)
    chk('④ 부분블록 [2..2] ×3', _keys(f) == [(0, 1), (1, 1), (1, 2), (1, 3)], _keys(f))

    # ⑤ 연속 Loop 2개 (서로 겹치지 않는 블록)
    f = expand_sched([C, {'k': 'l', 'to': 1, 'n': 2}, D, {'k': 'l', 'to': 3, 'n': 3}], warn=None)
    chk('⑤ 독립 Loop 2개', _keys(f) == [(0, 1), (0, 2), (2, 1), (2, 2), (2, 3)], _keys(f))

    # ⑥ Rest 도 사이클과 함께 반복 (프로토콜 표시)
    f = expand_sched([C, R, {'k': 'l', 'to': 1, 'n': 2}], warn=None)
    chk('⑥ Rest 포함 반복', _keys(f) == [(0, 1), (1, 1), (0, 2), (1, 2)], _keys(f))

    # ⑦ n=2 (최소 Loop) / 큰 n 도 선형 증가
    f = expand_sched([C, {'k': 'l', 'to': 1, 'n': 2}], warn=None)
    chk('⑦ 최소 Loop n=2', _keys(f) == [(0, 1), (0, 2)], _keys(f))
    f = expand_sched([C, D, {'k': 'l', 'to': 1, 'n': 50}], warn=None)
    chk('⑦b n=50 → 100런, 전역 유일', len(f) == 100 and len(set(_keys(f))) == 100)

    # ⑧ 경고 발화 (수동 n 무시 알림)
    msgs = []
    expand_sched([dict(C, n=3), {'k': 'l', 'to': 1, 'n': 2}], warn=msgs.append)
    chk('⑧ 수동 n 무시 경고', any('무시' in m for m in msgs), msgs)

    print('SCHED-LOOP TEST ' + ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
