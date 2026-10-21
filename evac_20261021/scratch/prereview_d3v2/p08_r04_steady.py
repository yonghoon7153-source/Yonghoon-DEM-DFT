#!/usr/bin/env python3
"""PRE-D3V2 탐침 08 — R04 정상 상태 = '두 측정 창의 블록 평균 차 ≤ 2 × 블록 표준오차' (v2 §3-2 · §3-3) 는 차이 검정이다.

손 계산: 블록 SD σ_b · 창마다 블록 n 개 · 표류 δ.  SE = σ_b·√(2/n) ⇒ '정상' ⟺ |δ + 잡음| ≤ 2σ_b√(2/n).
  · 시끄러운 런 (σ_b 4° · n 4) — 2SE = 5.66° ⇒ 보정 띠 (3°) 와 같은 크기의 표류 3° 도 대체로 '정상'.
  · 조용한 긴 런 (σ_b 0.3° · n 40) — 2SE = 0.134° ⇒ 무시할 표류 0.3° 도 거의 늘 '비정상'.
  ⇒ 결과가 잡음이 클수록 통과 (부재의 증거를 정상의 증거로 읽음) · 비정상일 때의 처리 (제외? 연장? TECH?) 가 설계에 없다.
참조 구현 RulesV2.steady 를 그대로 쓴다 (블록 독립 정규 · [가정 예시]).

재실행: python3 -I p08_r04_steady.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
rng = random.Random(8)
rows = []
for sig, n, drift in ((4.0, 4, 3.0), (4.0, 4, 0.0), (1.5, 4, 3.0), (0.5, 4, 3.0), (0.3, 40, 0.3), (0.3, 40, 0.0), (0.3, 40, 0.15)):
    acc = 0
    T = 20000
    for _ in range(T):
        w1 = [40.0 + rng.gauss(0, sig) for _ in range(n)]
        w2 = [40.0 + drift + rng.gauss(0, sig) for _ in range(n)]
        acc += bool(R2.steady(w1, w2, None))
    rows.append(dict(block_sd=sig, blocks_per_window=n, drift_deg=drift, P_steady=acc / T))
pcommon.dump('p08_r04_steady.json', rows)
for r in rows:
    print(f"블록 SD {r['block_sd']}° · 창마다 {r['blocks_per_window']} 블록 · 표류 {r['drift_deg']}° → '정상' 판정 확률 {r['P_steady']:.3f}")
