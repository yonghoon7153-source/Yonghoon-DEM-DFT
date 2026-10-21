#!/usr/bin/env python3
"""PRE-D3V2 탐침 05 — R09 (검증 판별력) 를 연속 관측량 (T2 다른 두 속도 · T3 흐름 시간) 에 쓰면 판정이 나오는가.

v2 §3-7 R09: 예측 = 구간 안 수준 전부 (두 끝 · 중심) · 판별력 = 구간 안 예측과 바로 밖 이웃 수준의 예측이 갈릴 때만
            (이진 = 판정표 · 연속 = 차 > 띠) · 구간 안에서 예측이 갈리면 '불확정' · 판별력 없으면 '검증 아님'.
원장 MXD3-09 처리 계획: "구간 두 끝 + 중심 예측 · 이웃 밖 수준과 갈릴 때만 '판별력 있는 검증'".

손 계산 (선형 검증 응답 I_v = c + a_v·x · 띠 h_v):  구간 폭 W (R02 · 선형 보정 곡선이면 W ≥ 2 칸 = 1 decade) ·
바로 밖 이웃 = 구간 끝에서 ≤ 1 칸 (0.5 decade).  '불확정 아님' ⟺ a_v·W ≤ h_v · '판별력' ⟺ a_v·d_out > h_v (d_out ≤ 0.5)
⇒ 둘 다 ⟺ W < d_out — 불가능 (W ≥ 1 > 0.5).  [읽기 B · 두 끝 · 중심]
읽기 A (참조 구현 · 구간 안 격자 수준) 도 구간 안 수준이 둘 이상이면 같은 모순 (안 수준 간격 = 밖 이웃 간격 = 칸 폭).

재실행: python3 -I p05_r09_continuous.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
U, A_C = 1.5, 5.0                         # [가정 예시] = C02 대조 (보정 곡선 40 + 5x · 띠 3°)


def classify(preds_in, pred_out, hv):
    """연속 판정: 구간 안 예측 퍼짐 > 띠 = 불확정 · 밖 이웃이 가까운 안 예측과 > 띠 = 판별력."""
    if max(preds_in) - min(preds_in) > hv:
        return '불확정'
    if any(abs(po - pi) > hv for po, pi in pred_out):
        return '판별력 있음'
    return '판별력 없음'


out = {}
for hv in (3.0, 1.0):
    for av in (0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 40.0):
        cnt = {'A': {}, 'B': {}}
        for j in range(201):
            xt = X[1] + (X[6] - X[1]) * j / 200.0
            I = [40.0 + A_C * x for x in X]
            comps = R2.accept(X, I, [U] * len(X), 40.0 + A_C * xt, 0.0, nu=None)['comps']
            if len(comps) != 1:
                continue
            lo, hi = comps[0]
            g = lambda x: 10.0 + av * x                      # noqa: E731 — 선형 검증 응답
            inner = [k for k, x in enumerate(X) if lo - 1e-12 <= x <= hi + 1e-12]
            below = [k for k, x in enumerate(X) if x < lo - 1e-12]
            above = [k for k, x in enumerate(X) if x > hi + 1e-12]
            # 읽기 A — 구간 안 격자 수준 · 밖 이웃 = 가장 가까운 밖 격자 수준 (참조 구현 validation() 의 i_lo − 1 · i_hi + 1)
            if inner:
                pin = [g(X[k]) for k in inner]
                pout = ([(g(X[below[-1]]), g(X[inner[0]]))] if below else []) + ([(g(X[above[0]]), g(X[inner[-1]]))] if above else [])
                ra = classify(pin, pout, hv)
            else:
                ra = '안 수준 0 (정의 없음)'
            cnt['A'][ra] = cnt['A'].get(ra, 0) + 1
            # 읽기 B — 두 끝 · 중심 (새 Bo 수준) · 밖 이웃 = 구간 바로 밖 격자 수준
            pin = [g(lo), g(0.5 * (lo + hi)), g(hi)]
            pout = ([(g(X[below[-1]]), g(lo))] if below else []) + ([(g(X[above[0]]), g(hi))] if above else [])
            rb = classify(pin, pout, hv)
            cnt['B'][rb] = cnt['B'].get(rb, 0) + 1
        out[f'hv{hv}_av{av}'] = cnt

# 판별력이 나는 꼴 — 구간 안은 평평 · 구간 끝과 밖 이웃 사이에서 띠보다 크게 뛰는 계단 (손으로 만든 예)
xt = 1.0
I = [40.0 + A_C * x for x in X]
lo, hi = R2.accept(X, I, [U] * len(X), 40.0 + A_C * xt, 0.0, nu=None)['comps'][0]
above = [x for x in X if x > hi + 1e-12][0]
xs_step = 0.5 * (hi + above)
step = lambda x: 10.0 if x < xs_step else 20.0          # noqa: E731
pin = [step(lo), step(0.5 * (lo + hi)), step(hi)]
step_res = classify(pin, [(step(above), step(hi))], 3.0)
out['step_example'] = dict(interval=(lo, hi), next_level_above=above, step_at=xs_step, result=step_res)
pcommon.dump('p05_r09_continuous.json', out)
for k, v in out.items():
    print(k, v)
