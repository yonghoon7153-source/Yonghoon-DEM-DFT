# -*- coding: utf-8 -*-
"""탐침 2-③″ (보호 띠 칼날) — 사슬의 실제 `Ladder` 에 RCA-01 회로 (S = 1.597 + 0.0363/(r + 0.1) mS/cm · r = R/10^4.75 · origin 무관) 를
가짜 fetch 로 넣고 판독 보장 오차 e 를 칼날 d/(1 − d) 양쪽으로.  등록 R 4판 §3-2b ⑧: e ≤ 칼날 → hi 끝 = 후보 (비 599.03) · e > 칼날 →
바깥 이웃 1e7 (비 1,000).  lo 쪽은 같은 규칙 · lo 끝 = 바깥 이웃 10,000 (후보 확인 실패) 그대로여야."""
import json
import math
import os
import sys
REPO = os.environ.get('PRE_REPO')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as R   # noqa: E402


def S(Rj):
    if Rj == 'inf':
        return 1.597e-3
    x = float(Rj)
    if x == 0.0:
        return (1.597 + 0.0363 / 0.1) * 1e-3
    r = x / 10 ** 4.75
    return (1.597 + 0.0363 / (r + 0.1)) * 1e-3


def run(e):
    def fetch(role, key, arms):
        n = arms if isinstance(arms, int) else len(arms)
        return [{'sigma': S(key), 'err_rel': float(e), 'state': 'positive'} for _ in range(n)]
    lad = R.Ladder(fetch, max_points=40, ratio_max=R.PLAN_NO_CAP)
    lad.run()
    st = lad.st
    return {'R_j0': st['R_j0'], 'R_j_lo': st['R_j_lo'], 'R_j_hi': st['R_j_hi'], 'ratio': st['R_ratio'], 'n_runs': st['n_runs'],
            'hi_source': st['ends']['hi']['source'], 'lo_source': st['ends']['lo']['source']}


# 칼날 — hi 후보 판독이 T⁻ 아래 상대 거리 d (사슬의 같은 후보로 다시 계산)
base = run(0.0)
cand = float(base['R_j_hi'])
Tm = R.TARGET_SBE_MS * 1e-3 * (1 - R.CONFIRM_TOL)
d = 1.0 - S(repr(cand)) / Tm
knife = d / (1 - d)
out = {'e0': base, 'd': d, 'knife': knife}
for tag, e in (('knife*(1-1e-6)', knife * (1 - 1e-6)), ('knife*(1+1e-6)', knife * (1 + 1e-6)), ('3.7e-5', 3.7e-5), ('3.8e-5', 3.8e-5),
               ('1e-4', 1e-4)):
    out[tag] = run(e)
for k, v in out.items():
    print(k, v)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_band_knife.json'), 'w'), ensure_ascii=False, indent=1)
