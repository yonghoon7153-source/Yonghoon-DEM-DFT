#!/usr/bin/env python3
"""PRE-D3V2 탐침 09 — 참조 구현 RulesV2.validation (R09 의 '실행 가능한 명세') 의 두 자리.

(가) 판별력 없음인데 status = '통과' — R09 '주장하는 것' = *"'검증 통과' 는 판별력 있을 때만"* · §3-7 *"판별력이 없으면
     '검증 아님 (보고만)'"*.  C09 는 discriminating 플래그만 보고 status 를 안 본다.
(나) 구간 안에 격자 수준이 없으면 (세분 뒤 구간 폭 중앙 0.241 decade < 격자 0.5 — C02 출력) 예측 집합이 비어 StopIteration.
(다) 두 시드가 한 수준에서 갈리면 (이진: 한 시드 흐름 · 한 시드 멈춤) 판정표가 없다 — validation 은 수준당 예측 하나만 받는다.

재실행: python3 -I p09_r09_reference.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
S, F = '멈춤', '흐름'
out = {}
r = R2.validation([F] + [S] * 7, 3, 5, S)
out['가_no_discrimination'] = r
try:
    r2 = R2.validation([F] * 4 + [S] * 4, 4, 3, S)           # 구간 안 수준 0 (i_lo > i_hi)
    out['나_empty_inner'] = r2
except Exception as e:                                         # noqa: BLE001
    out['나_empty_inner'] = f'{type(e).__name__}: {e}'
pcommon.dump('p09_r09_reference.json', out)
for k, v in out.items():
    print(k, '→', v)
