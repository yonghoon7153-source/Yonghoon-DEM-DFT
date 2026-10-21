#!/usr/bin/env python3
"""PRE-D3V2 탐침 04 — v2 기본 시드 배치 (§3-3) 에서 T1 (HR) 곡선 = 탭 4 수준 (1 decade 칸) · R02 의 |ΔI| 항 · F2 (폭 > 2.5 decade = 식별 불가).

선형 HR 곡선 (기울기 a · 띠 h) 에서 R02 집합 폭 ≈ 2h/a + 2 × (칸 폭).  탭 4 수준이면 칸 폭 1 decade ⇒ 폭 ≥ 2 decade (h → 0 이어도).
F2 문턱 2.5 decade ⇒ 식별에 2h/a < 0.5 필요 (a > 4h /decade).  C01 대조의 T1 (a 0.05 · h 0.03) 은 2h/a = 1.2 ⇒ 폭 3.2 → 식별 불가.

재실행: python3 -I p04_t1_resolution.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
rows = []
for name, lv in (('8 수준 (C01 가정)', list(range(8))), ('탭 4 수준 (v2 기본 배치)', [1, 3, 5, 7])):
    X1 = [X[k] for k in lv]
    for a1, h1 in ((0.05, 0.03), (0.05, 0.01), (0.10, 0.03), (0.20, 0.03), (0.05, 0.0)):
        widths, f2, f3p = [], 0, 0
        for j in range(101):
            xt = X1[0] + (X1[-1] - X1[0]) * (0.15 + 0.7 * j / 100.0)     # 격자 안쪽 70 %
            I1 = [1.2 + a1 * x for x in X1]
            A = R2.accept(X1, I1, [h1 / 2.0] * len(X1), 1.2 + a1 * xt, 0.0, nu=None)
            comps = A['comps']
            w = sum(q - p for p, q in comps)
            lo_t = bool(comps) and abs(comps[0][0] - X1[0]) < 1e-12
            hi_t = bool(comps) and abs(comps[-1][1] - X1[-1]) < 1e-12
            widths.append(w)
            # v2 §3-7 원문: F2 = '격자 두 끝에 닿거나 폭 > 2.5 decade' · F3′ = '격자 끝에 닿거나 그 끝 너머' (한 끝)
            if (lo_t and hi_t) or w > 2.5:
                f2 += 1
            elif lo_t or hi_t:
                f3p += 1
        widths.sort()
        rows.append(dict(grid=name, a=a1, h=h1, two_h_over_a=(2 * h1 / a1 if a1 else None),
                         width_median=round(widths[50], 3), width_min=round(widths[0], 3),
                         F2_fraction=f2 / 101, F3prime_one_end_fraction=f3p / 101, identified_fraction=(101 - f2 - f3p) / 101))
pcommon.dump('p04_t1_resolution.json', rows)
for r in rows:
    print(f"{r['grid']:22s} a {r['a']:.2f}/decade · 띠 {r['h']:.2f} (2h/a {r['two_h_over_a']}) → R02 폭 중앙 {r['width_median']} · 최소 {r['width_min']} decade · "
          f"F2 (두 끝 · 폭 > 2.5) {r['F2_fraction']:.2f} · F3′ (한 끝) {r['F3prime_one_end_fraction']:.2f} · 식별 {r['identified_fraction']:.2f}")
