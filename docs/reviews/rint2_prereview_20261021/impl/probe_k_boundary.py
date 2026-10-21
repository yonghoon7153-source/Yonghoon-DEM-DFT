# -*- coding: utf-8 -*-
"""탐침 A3 (RCA-05 옆 자리) — 분산판 v0 의 간선 수 k = ceil(L_c/L_par) 경계에서 σ 가 연속인가.
깊은 교차 (d0 = 0) 를 직교에서 아주 조금 기울이면 L_c/L_par = 1/sin θ 가 1 + 1e-9 를 넘는다 → k 1 → 2.
총 접합 G (배율) 는 1/sin θ 로 연속 (차이 ~1e-8) — 그런데 간선 자리 (포트) 가 옮겨지면 σ 가 뛴다.
A = 아래 판에서 세로 (x 3.5) z 0.5 → 5.5 (막다른 위끝) · B = 교차점 C 를 지나는 기운 선 → 오른쪽 끝에서 위 판까지 세로."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (9, 3, 10)
out = {}


def run(theta_deg, Cz, rj=1e3):
    th = math.radians(theta_deg)
    C = np.array([3.5, 1.5, Cz])
    u = np.array([math.sin(th), 0.0, math.cos(th)])    # θ = 90 → B 가로 (x)
    b0 = C - 3.0 * u
    b1 = C + 3.0 * u
    A = [(3.5, 1.5, 0.5), (3.5, 1.5, 5.5)]
    B = [tuple(b0), tuple(b1), (b1[0], 1.5, 9.5)]
    P = rows([A, B], step=0.25)
    sid, _ = bed(P, N)
    reg = registry(sid, P)
    inst = reg['instances']; sub = reg['subedges']; pos = reg['positions']
    pl = plan(reg, rj)
    r = solve(sid, sig_e(), N, pl)
    ports = [(tuple(int(v) for v in pos['ijk'][a]), tuple(int(v) for v in pos['ijk'][b])) for a, b in zip(sub['port_i'], sub['port_j'])]
    return {'theta': theta_deg, 'Cz': Cz, 'sid_sha': hash(sid.tobytes()), 'n_inst': int(len(inst['fi'])),
            'Lc_over_Lpar': float(inst['Lc'][0] / LPAR) if len(inst['fi']) else None,
            'k': int(inst['nsub'][0]) if len(inst['fi']) else None, 'mult': float(inst['mult'][0]) if len(inst['fi']) else None,
            'ports': ports, 'g': [float(x) for x in pl['g_code']], 'I': I_of(r, N), 'reason': r.get('reason')}


for Cz in (3.5, 3.0, 3.25):
    rows_ = [run(t, Cz) for t in (90.0, 89.9999, 89.999, 89.99, 89.9)]
    base = rows_[0]
    for x in rows_:
        x['I_rel_to_90deg'] = (x['I'] - base['I']) / base['I']
        x['same_sid_as_90deg'] = x['sid_sha'] == base['sid_sha']
        print(Cz, {k: x[k] for k in ('theta', 'k', 'Lc_over_Lpar', 'ports', 'I', 'I_rel_to_90deg', 'same_sid_as_90deg')})
    out[f'Cz_{Cz}'] = rows_
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_k_boundary.json'), out)
