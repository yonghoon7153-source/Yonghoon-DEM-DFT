#!/usr/bin/env python3
"""PRE-D3V2 탐침 03 — R01 검출 한계 Δμ_r,min = (w₁ + w₂)/|b₁/a₁ − b₂/a₂| (w_k = h_k/|a_k|) 가 R02 의 실제 받아들일 집합과 맞는가.

R01 보장 (v2 §4): "선형화 아래 |Δμ_r| > Δμ_r,min 이면 교집합이 빈다".
R02 집합 (v2 §3-7) 은 띠에 칸의 |ΔI| 를 더한다 ⇒ 선형 곡선에서 반폭 = h/a + (칸 폭) — w_k 보다 칸 하나 넓다.

[가정 예시] = C01 대조 그대로: T2 a 5 °/decade · b 200 °/단위 μ_r · 띠 3° · T1 (HR) a 0.05 /decade · b 0 · 띠 0.03.
참 Bo = 10 (x_t = 1) · 덱 μ_r 이 Δ 틀림 → DEM 곡선 I_k(x) = c + a_k·x + b_k·(μ_true + Δ) · 측정 m_k = c + a_k·x_t + b_k·μ_true.
T1 격자 = (가) 8 수준 (C01 의 가정) (나) v2 기본 배치의 탭 4 수준 (0.6718 · 6.718 · 67.18 · 637.3 — HR 은 탭 수준에서만).

재실행: python3 -I p03_r01_vs_r02.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
TOL = R2.TOL_MU_R
a2, b2, h2 = 5.0, 200.0, 3.0
a1, b1, h1 = 0.05, 0.0, 0.03
mu_true, xt = 0.075, 1.0
w2, w1 = h2 / a2, h1 / a1
dmin_formula = (w1 + w2) / abs(b1 / a1 - b2 / a2)


def run(t1_levels):
    out = []
    first_empty = None
    for i in range(0, 161):
        d = 0.0005 * i
        I2 = [40.0 + a2 * x + b2 * (mu_true + d) for x in X]
        m2 = 40.0 + a2 * xt + b2 * mu_true
        A2 = R2.accept(X, I2, [h2 / 2.0] * len(X), m2, 0.0, nu=None)
        X1 = [X[k] for k in t1_levels]
        I1 = [1.2 + a1 * x + b1 * (mu_true + d) for x in X1]
        m1 = 1.2 + a1 * xt + b1 * mu_true
        A1 = R2.accept(X1, I1, [h1 / 2.0] * len(X1), m1, 0.0, nu=None)
        C = c.intersect(A1['comps'], A2['comps']) if (A1['comps'] and A2['comps']) else []
        x1, x2 = xt - b1 / a1 * d, xt - b2 / a2 * d
        b = R2.b_check(x1, w1, x2, w2, (b1 / a1, b2 / a2), TOL)
        anc = R2.anchor(A1, A2)
        truth_in = bool(C) and c.inside(xt, C)
        if not C and first_empty is None:
            first_empty = d
        out.append(dict(dmu=round(d, 5), intersection=[(round(p, 3), round(q, 3)) for p, q in C],
                        b_check=b['status'], dmin=round(b['dmin'], 4), certifies=b['certifies_friction'],
                        anchor=anc['status'], anchor_Bo=(round(10 ** anc['x'], 3) if anc.get('x') is not None else None),
                        truth_in_intersection=truth_in))
    return out, first_empty


res = {}
for name, lv in (('T1_8levels', list(range(8))), ('T1_tap4levels', [1, 3, 5, 7])):
    rows, fe = run(lv)
    # 핵심 행: 식이 '빈다' 고 하는 Δ (> dmin_formula) 인데 실제 교집합이 비지 않은 것
    contra = [r for r in rows if r['dmu'] > dmin_formula and r['intersection']]
    wrong_cert = [r for r in rows if r['dmu'] > TOL and r['intersection'] and r['certifies']]
    # B 의 판정 (b_check · |x1−x2| ≤ w1+w2 모형) 과 실제 교집합이 다른 행
    res[name] = dict(dmin_formula=dmin_formula, actual_detection_limit=fe,
                     n_contradictions=len(contra), first_contradiction=(contra[0] if contra else None),
                     last_contradiction=(contra[-1] if contra else None),
                     rows_beyond_tol_certified_by_formula=len(wrong_cert),
                     sample=[r for r in rows if r['dmu'] in (0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.07)])
pcommon.dump('p03_r01_vs_r02.json', res)
for k, v in res.items():
    print(f'[{k}] 식 Δμ_r,min = {v["dmin_formula"]:.4f} · 실제 (R02 집합) 첫 빈 교집합 Δ = {v["actual_detection_limit"]} · 허용 {TOL}')
    for r in v['sample']:
        print(f"   Δμ_r {r['dmu']:.3f}: 교집합 {r['intersection']} · 참값 안? {r['truth_in_intersection']} · 앵커 {r['anchor']} {r['anchor_Bo']} · "
              f"B(식) {r['b_check']} (dmin {r['dmin']}) · 마찰 확인 주장 {r['certifies']}")
