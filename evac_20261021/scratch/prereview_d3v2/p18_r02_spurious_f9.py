#!/usr/bin/env python3
"""PRE-D3V2 탐침 18 — R02 과포함의 둘째 결과: 단조 (가파름 · 평평 · 가파름) 곡선에서 받아들일 집합이 둘로 끊겨 R03 F9 '모호'.

손 계산 (8 수준 · 띠 h = 1 · m = 12.5 · I = 0 10 11 20 21 22 23 24):
  칸 0 (0→10): |L − 12.5| ≤ 1 + 10 → L ≥ 1.5 → [x0 + 0.075, x1] 를 받음 (단조면 이 칸은 ≤ 10 + 1 = 11 < 12.5 → 받을 수 없음)
  칸 1 (10→11): ≤ 1 + 1 → L ≥ 10.5 → [x1 + 0.25, x2]   (역시 칸 값 범위 [9, 12] 밖)
  칸 2 (11→20): ≤ 1 + 9 → 칸 전체 (정답)
  ⇒ v2 집합 = [x0+0.075, x1] ∪ [x1+0.25, x3] (두 성분) · 정답 (칸 값 범위 ± 띠) = [x2, x3] 한 성분.
  넓은 다른 시험과 겹치면 v2 = F9 '모호' (앵커 없음) · 정답 = 앵커.  다른 시험이 낮은 Bo 만 받으면 v2 = 가짜 앵커 · 정답 = F5.
재실행: python3 -I p18_r02_spurious_f9.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
I = [0.0, 10.0, 11.0, 20.0, 21.0, 22.0, 23.0, 24.0]
mm = 12.5
A = R2.accept(X, I, [0.5] * 8, mm, 0.0, nu=None)
env = pcommon.monotone_envelope_accept(X, I, 1.0, mm)
broad = dict(comps=[(X[0], X[-1])], side=None)
low = dict(comps=[(X[0], X[0] + 0.3)], side=None)
res = dict(v2_comps=A['comps'], correct_comps=env,
           with_broad_other=dict(v2=R2.anchor(broad, A)['status'], correct=R2.anchor(broad, dict(comps=env, side=None))['status']),
           with_low_other=dict(v2=R2.anchor(low, A), correct=R2.anchor(low, dict(comps=env, side=None))['status']))
pcommon.dump('p18_r02_spurious_f9.json', res)
for k, v in res.items():
    print(k, v)
