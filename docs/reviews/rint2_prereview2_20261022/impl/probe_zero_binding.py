# -*- coding: utf-8 -*-
"""탐침 B3 (2 회차 · PRE-impl-07 재확인 + B 증서 결합 옆 자리) — 증서 ↔ 런 결합 (`run_contract.cert_binding_problem`).
① 실제 침대 A 의 영값 증서 (R_j = ∞ 바닥) + A 의 매니페스트 = 받음  ② 지문만 다른 침대 B 의 것 (다른 런 증서) = 거부?
③ 양의 해 증서 (R_j 200) · 같은 σ 다른 계획 (R_j 201 의 plan_rows) = 거부?  ④ 증서 결합 칸 하나 결손 = 거부?  ⑤ 결합 판 다름 = 거부?
⑥ 단락 증서 (천장) 의 결합 — 다른 침대 지문 = 거부?"""
import contextlib
import copy
import io
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403
import run_contract as RC

CX_N = (8, 3, 14)
CX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 10.5)], [(2.1, 1.5, 10.5), (2.1, 1.5, 1.2), (6.5, 1.5, 1.2), (6.5, 1.5, 13.5)]]
P = rows(CX)
sid, _ = bed(P, CX_N)
reg = registry(sid, P)
S3.CONV_CERT = True
S3.CG_RTOL = 1e-12


def run(rj, **kw):
    pl = plan(reg, rj, **kw)
    with contextlib.redirect_stdout(io.StringIO()):
        r = S3.solve_sigma_z(sid, sig_e(), H, z_top_um=float(CX_N[2]), z_bot_um=0.0, cjunc=pl)
    man = {'ca_ext': {'cjunc': {'evidence': {'fp': {'sid': reg['fp']['sid'], 'registry': reg['fp']['registry'],
                                                     'plan_rows': pl['fp_rows']}}}}}
    return r, pl, man


out = {}
r0, p0, m0 = run(math.inf, allow_rj_limits=True)
c0 = dict(r0['conv_cert'])
out['1_own_zero_cert'] = RC.conv_cert_problem(c0, 0.0, m0)
out['2_foreign_bed_zero_cert'] = RC.conv_cert_problem(dict(c0, fp_sid='0123456789abcdef' * 2), 0.0, m0)
r2, p2, m2 = run(200.0)
c2 = dict(r2['conv_cert'])
out['3a_own_positive_cert'] = RC.conv_cert_problem(c2, r2['sigma_eff'], m2)
_r3, p3, _m3 = run(201.0)
out['3b_same_sigma_other_plan_rows'] = RC.conv_cert_problem(c2, r2['sigma_eff'], dict(m2, ca_ext={'cjunc': {'evidence': {'fp': dict(
    m2['ca_ext']['cjunc']['evidence']['fp'], plan_rows=p3['fp_rows'])}}}))
c4 = dict(c2)
c4.pop('fp_cjunc_rows')
out['4_missing_bind_field'] = RC.conv_cert_problem(c4, r2['sigma_eff'], m2)
out['5_other_bind_version'] = RC.conv_cert_problem(dict(c2, bind_version='cert-bind-v0'), r2['sigma_eff'], m2)
m6 = copy.deepcopy(m2)
m6['ca_ext']['cjunc']['evidence']['fp'].pop('registry')
out['6_manifest_missing_registry_fp'] = RC.conv_cert_problem(c2, r2['sigma_eff'], m6)
out['7_no_manifest'] = RC.conv_cert_problem(c2, r2['sigma_eff'], None) if True else None
for k, v in out.items():
    print(k, '→', v)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_zero_binding.json'), out)
