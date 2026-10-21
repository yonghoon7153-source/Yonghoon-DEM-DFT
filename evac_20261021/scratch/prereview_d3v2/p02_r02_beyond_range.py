#!/usr/bin/env python3
"""PRE-D3V2 탐침 02 — R02 받아들일 집합이 '곡선 값 범위 밖' 측정을 받아들이는가 (F10 · F3′ · F5 가 죽는가).

v2 §3-7 R02:  칸 [x_k, x_k+1] 에서 |L(x) − m| ≤ √[(t_exp·u_exp)² + (t_ν·u_칸)²] + |I_k+1 − I_k| 인 부분의 합집합.
v2 §3-7 F10:  "측정이 그 시험 곡선 값 범위 밖 — 끝 방향을 적고 F3′ 로".

손 계산: 가파른 칸 (I_k = 35 · I_k+1 = 48.9 · 띠 h = 3) 은 m ∈ [35 − 3 − 13.9, 48.9 + 3 + 13.9] = [18.1, 65.8] 이면
칸의 일부를 받는다.  그런데 칸 안 단조 곡선 (R02 보장의 전제) 은 [35, 48.9] 밖 값을 못 낸다 ⇒ 정답 (단조 포락) = [32, 51.9] 밖이면 빈 칸.
⇒ m = 60 (곡선 최대 48.9 보다 11.1° 위) · m = 20 (곡선 최소 35 보다 15° 아래) 에서 v2 는 '앵커' · 정답은 F10.

재실행:  python3 -I p02_r02_beyond_range.py   (REPO 환경변수 = 검토 작업 트리 · 기본 = 이 에이전트 작업 트리)
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X                                   # 설계 격자 8 수준 log10 Bo
U = 1.5                                   # [가정 예시] C02 와 같은 u (ν None → 배수 2 → 띠 3°)
D_ANG = 13.9
s = 0.1 / (2.0 * math.log(9.0))           # C02 와 같은 전이 폭 (10–90 % 0.1 decade)
xstar = 0.5 * (X[2] + X[3])               # 셋째 칸 한가운데


def f(x):
    return 35.0 + D_ANG / (1.0 + math.exp(-(x - xstar) / s))


I = [f(x) for x in X]
u = [U] * len(X)
rows = []
for mm in (60.0, 55.0, 51.0, 20.0, 25.0, 31.0, 42.0):
    A = R2.accept(X, I, u, mm, 0.0, nu=None)
    comps = A['comps']
    env = pcommon.monotone_envelope_accept(X, I, 2.0 * U, mm)
    f3 = R2.f3(X, I, f, mm, 2.0 * U, 1015.4)
    rows.append(dict(m=mm, curve_min=min(I), curve_max=max(I),
                     v2_comps=[(round(a, 4), round(b, 4)) for a, b in comps],
                     v2_comps_Bo=[(round(10 ** a, 3), round(10 ** b, 3)) for a, b in comps],
                     v2_status=('비지 않음 (앵커 후보)' if comps else f'빈 집합 → F10 ({A["side"]})'),
                     monotone_envelope=[(round(a, 4), round(b, 4)) for a, b in env],
                     correct_status=('비지 않음' if env else 'F10 (곡선 값 범위 밖)'),
                     ref_f3_direct=f3['status']))

# 받아들이는 m 의 범위 (v2 · 정답) — 가파른 칸 하나만 보는 손 계산과 같은지
grid_m = [10.0 + 0.01 * i for i in range(6001)]
acc_v2 = [mm for mm in grid_m if R2.accept(X, I, u, mm, 0.0, nu=None)['comps']]
acc_env = [mm for mm in grid_m if pcommon.monotone_envelope_accept(X, I, 2.0 * U, mm)]

# 두 시험 — T1 (HR) 은 넓게 받는다 · T2 측정이 곡선 최대보다 위 → v2 = 앵커 · 정답 = F10 (T2)
T1 = dict(comps=[(X[0], X[-1])], side=None)
A2 = R2.accept(X, I, u, 60.0, 0.0, nu=None)
anc = R2.anchor(T1, A2)
res = dict(
    curve_levels_Bo=[round(10 ** x, 4) for x in X], curve_I=[round(v, 4) for v in I], band_stat=2.0 * U,
    rows=rows,
    accepted_m_range_v2=(min(acc_v2), max(acc_v2)), accepted_m_range_correct=(min(acc_env), max(acc_env)),
    hand_v2=(35.0 - 2 * U - D_ANG, 35.0 + D_ANG + 2 * U + D_ANG),
    two_test_v2_anchor=dict(status=anc['status'], Bo=(10 ** anc['x'] if anc.get('x') is not None else None)),
)
pcommon.dump('p02_r02_beyond_range.json', res)
for r in rows:
    print(f"m {r['m']:5.1f} (곡선 {r['curve_min']:.1f}–{r['curve_max']:.1f}) → v2 {r['v2_status']} {r['v2_comps_Bo']} | 정답 {r['correct_status']} | 참조 f3 {r['ref_f3_direct']}")
print('v2 가 받는 m 범위', res['accepted_m_range_v2'], ' 손 계산', res['hand_v2'], ' 정답 (단조 포락)', res['accepted_m_range_correct'])
print('두 시험 (T1 넓음 · T2 m 60) → v2', res['two_test_v2_anchor'])
