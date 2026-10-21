# -*- coding: utf-8 -*-
"""탐침 B2 (극한 · 상태 증서) — CX (RCA05 시험 꼴 · 분산 간선 k = 5) 에서 R_j = ∞ (바닥) · R_j = 0 (천장) · 유한.
CONV_CERT 켬 (생산 증서 경로) · 직접해 대신 생산 CG (_solve_cg) — 증서 ⓐ–ⓓ 가 실제 해에 걸리게.
기대 (손 회로): 바닥 = A · B 가 접합으로만 이어짐 → σ 0 = VALID_ZERO_TOPOLOGY (조기 반환 · ok True) · 천장 = 다섯 포트 쌍 축약 회로 ·
단락 꼴 (축약 무리가 두 판에 닿음) = ELECTRODE_SHORT (게시 불가)."""
import contextlib
import io
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403
import run_contract as RC

CX_N = (8, 3, 14)
CX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 10.5)], [(2.1, 1.5, 10.5), (2.1, 1.5, 1.2), (6.5, 1.5, 1.2), (6.5, 1.5, 13.5)]]
out = {}


def cx_ref(rj, contract=False):
    from fibre_segment_raster import segment_cells  # noqa: F401
    seqA = seq_cells_pts(densify(CX[0]))
    seqB = seq_cells_pts(densify(CX[1]))
    nA = len(seqA)
    ia = {c: i for i, c in enumerate(seqA)}
    ib = {c: nA + i for i, c in enumerate(seqB)}
    E = [(i, i + 1, G_AX) for i in range(nA - 1)] + [(nA + i, nA + i + 1, G_AX) for i in range(len(seqB) - 1)]
    rep = list(range(nA + len(seqB)))
    for z in (1, 3, 5, 7, 9):
        a_, b_ = ia[(1, 1, z)], ib[(2, 1, z)]
        if contract:
            rep[b_] = a_
        else:
            E.append((a_, b_, 1e4 / rj))
    E = [(rep[a_], rep[b_], g) for a_, b_, g in E if rep[a_] != rep[b_]]
    return ref_I(nA + len(seqB), E, [(0, G_PL)], [(rep[nA + len(seqB) - 1], G_PL)])


P = rows(CX)
sid, _ = bed(P, CX_N)
reg = registry(sid, P)
S3.CONV_CERT = True
S3.CG_RTOL = 1e-12
for tag, rj, kw in (('finite_200', 200.0, {}), ('floor_inf', math.inf, {'allow_rj_limits': True}),
                    ('ceiling_0', 0.0, {'allow_rj_limits': True})):
    pl = plan(reg, rj, **kw)
    with contextlib.redirect_stdout(io.StringIO()):
        r = S3.solve_sigma_z(sid, sig_e(), H, z_top_um=float(CX_N[2]), z_bot_um=0.0, cjunc=pl)
    c = r.get('conv_cert') or {}
    want = (0.0 if math.isinf(rj) else cx_ref(rj if rj > 0 else 1.0, contract=(rj == 0.0)))
    I = I_of(r, CX_N)
    prob = RC.conv_cert_problem(c, r['sigma_eff'])
    out[tag] = {'I': I, 'I_hand': want, 'rel': (abs(I - want) / want if want else abs(I)), 'reason': r.get('reason'),
                'status': c.get('status'), 'ok': c.get('ok'), 'pass': [c.get('pass_a'), c.get('pass_b'), c.get('pass_c'), c.get('pass_d')],
                'err_bound_rel': c.get('target_err_bound_rel'), 'conv_cert_problem': prob,
                'record_R_j': (r.get('cjunc') or {}).get('R_j_ohm'), 'n_contract': (r.get('cjunc') or {}).get('n_contract'),
                'n_none_inf': (r.get('cjunc') or {}).get('n_none_inf'), 'quantitative': (r.get('cjunc') or {}).get('quantitative')}
    print(tag, out[tag])
# 단락 꼴 — F1 (교차 셀 접합 하나 · A 아래 판 · B 위 판) 천장 = 축약 무리가 두 판에 닿는가?  (A 가 위 판까지 닿게 늘린 꼴)
F1S = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(1.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
N1 = (6, 3, 8)
P1 = rows(F1S)
sid1, _ = bed(P1, N1)
reg1 = registry(sid1, P1)
with contextlib.redirect_stdout(io.StringIO()):
    r1 = S3.solve_sigma_z(sid1, sig_e(), H, z_top_um=float(N1[2]), z_bot_um=0.0, cjunc=plan(reg1, 0.0, allow_rj_limits=True))
c1 = r1.get('conv_cert') or {}
out['ceiling_F1S'] = {'I': I_of(r1, N1), 'reason': r1.get('reason'), 'status': c1.get('status'), 'ok': c1.get('ok'),
                      'conv_cert_problem': RC.conv_cert_problem(c1, r1['sigma_eff'])}
print('ceiling_F1S', out['ceiling_F1S'])
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_limits.json'), out)
