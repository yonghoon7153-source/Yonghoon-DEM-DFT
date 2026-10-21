#!/usr/bin/env python3
"""PRE-D3V2 탐침 06 — F1 (실측 재현 안 됨) 문턱 = '봉인 곡선의 이웃 차 |ΔI| 중앙값의 ½' (v2 §3-7 · R17 · Qv2-13).

R02 를 만든 바로 그 꼴 (jarray2019 꼴 계단 · C02) 에서 |ΔI| 는 계단 칸 하나만 크고 나머지는 ≈ 0 ⇒ 중앙값 ≈ 0 ⇒ 문턱 ≈ 0
⇒ 날 평균들의 SD 가 0 이 아니면 (어떤 실측이든) F1 '그 시험 탈락'.  측정이 계단 칸 (곡선이 가장 민감한 곳) 에 있어도.
대조: 문턱이 측정 근처의 국소 기울기를 보지 않는다 — 완만 직선 (5 °/decade) 이면 문턱 1.25°.

재실행: python3 -I p06_f1_threshold.py
"""
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
s = 0.1 / (2.0 * math.log(9.0))
res = {}
for name, fx in (('계단 (jarray 꼴 · 35 → 48.9 · 폭 0.1 decade · 셋째 칸)',
                  lambda x: 35.0 + 13.9 / (1.0 + math.exp(-(x - 0.5 * (X[2] + X[3])) / s))),
                 ('완만 직선 40 + 5x', lambda x: 40.0 + 5.0 * x),
                 ('바닥 · 전이 · 고원 (넓은 시그모이드 · 폭 1 decade)',
                  lambda x: 35.0 + 13.9 / (1.0 + math.exp(-(x - 1.3) / (1.0 / (2 * math.log(9.0))))))):
    for refine in (False, True):
        xs = R2.refine(list(X), fx, 2.0 * 1.5) if refine else list(X)
        I = [fx(x) for x in xs]
        dI = [abs(b - a) for a, b in zip(I, I[1:])]
        thr = 0.5 * statistics.median(dI)
        res[f'{name} · 세분 {refine}'] = dict(levels=len(xs), dI=[round(v, 4) for v in dI], F1_threshold_deg=thr)
pcommon.dump('p06_f1_threshold.json', res)
for k, v in res.items():
    print(f'{k}: 수준 {v["levels"]} · F1 문턱 (날 평균 SD 상한) = {v["F1_threshold_deg"]:.4g}°')
print('참고: geldart2006 카드 — 동적 AOR 5 회 SD 0.3–2.0° (같은 날 반복)')
