#!/usr/bin/env python3
"""PRE-D3V2 탐침 07 — 봉우리 곡선 (가운데 최대 · v2 가 C03 에서 예상한 grey1969 꼴 비단조) 위로 측정이 나가면 F10 → F3′ 가 무엇을 하나.

v2 §3-7: F10 "측정이 그 시험 곡선 값 범위 밖 — 끝 방향을 적고 F3′ 로" · F3′ 은 위 끝 / 아래 끝 확장만 정한다.
봉우리 위 측정은 어느 끝 너머도 아니다 (덱이 그 값을 어떤 Bo 에서도 못 낸다) — 분류 칸이 없다.
참조 구현은 같은 입력에 서로 다른 답을 낸다: side_of (F10 끝 방향) · f3 (F3′) · accept (R02).

재실행: python3 -I p07_f3_peaked.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
band = 3.0
cases = {
    '봉우리 (35 45 55 50 40 38 36 35)': [35, 45, 55, 50, 40, 38, 36, 35],
    '감소 곡선 (60 … 39)': [60, 57, 54, 51, 48, 45, 42, 39],
}
out = {}
for name, I in cases.items():
    I = [float(v) for v in I]
    for mm in (70.0, 60.0, 30.0, 64.0, 34.0):
        A = R2.accept(X, I, [band / 2.0] * len(X), mm, 0.0, nu=None)
        side = c.side_of(X, I, mm)
        f3 = R2.f3(X, I, lambda x: I[0], mm, band, 1015.4)
        env = pcommon.monotone_envelope_accept(X, I, band, mm)
        # 설계 문장대로: F10 → 끝 방향 (side) → F3′ 그 끝 칸 평평? (아래 끝 = I[1]−I[0] · 위 끝 = I[-1]−I[-2])
        if A['comps']:
            design = '앵커 후보 (R02 집합 비지 않음)'
        else:
            if side == 'low_bo':
                design = '아래 끝 평평 → 마찰 바닥' if abs(I[1] - I[0]) <= band else '아래로 한 단계 확장 (0.0672) → 그래도 끝 = 표현 범위 밖 (아래)'
            else:
                design = '위 끝 평평 → 위 포화 (F4)' if abs(I[-1] - I[-2]) <= band else '위로 확장 (964.7)'
        out[f'{name} · m {mm}'] = dict(R02_comps=A['comps'], side_of=side, ref_f3=f3['status'], design_path=design,
                                      correct_monotone_envelope=env,
                                      note=('측정 > 곡선 최대 + 띠 — 어느 끝 너머도 아님' if mm > max(I) + band and I.index(max(I)) not in (0, len(I) - 1) else ''))
pcommon.dump('p07_f3_peaked.json', out)
for k, v in out.items():
    print(f"{k}: R02 {'비지 않음' if v['R02_comps'] else '빔'} · F10 끝 방향 {v['side_of']} · 설계 문장 경로 = {v['design_path']} · 참조 f3 = {v['ref_f3']} · 정답(단조 포락) {'빔' if not v['correct_monotone_envelope'] else v['correct_monotone_envelope']} {v['note']}")
