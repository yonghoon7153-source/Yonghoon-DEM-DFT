# -*- coding: utf-8 -*-
"""탐침 B3 (RCA-13 옆 자리 · 증서 ↔ 결과 결합) — VALID_ZERO 증서는 σ 결합 (증서 σ 0 = 결과 σ 0) 이 아무것도 묶지 않는다.
조기 반환 증서의 격자 지문 (fp_sid · fp_sig) 은 hex 32 형식만 본다 → 다른 침대 (다른 sid) 의 영값 증서를 붙여도 받는가.
① 실제 침대 A (관통 없음 · R_j = ∞ 바닥) 의 증서 ② 그 증서를 지문만 다른 침대 B 의 것으로 바꾼 사본 · ③ 침대 B 의 매니페스트 지문과 대조할 칸이 있는가."""
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
P = rows(CX)
sid, _ = bed(P, CX_N)
reg = registry(sid, P)
S3.CONV_CERT = True
S3.CG_RTOL = 1e-12
with contextlib.redirect_stdout(io.StringIO()):
    r = S3.solve_sigma_z(sid, sig_e(), H, z_top_um=float(CX_N[2]), z_bot_um=0.0,
                         cjunc=plan(reg, math.inf, allow_rj_limits=True))
cert = dict(r['conv_cert'])
foreign = dict(cert, fp_sid='0123456789abcdef' * 2, fp_sig='fedcba9876543210' * 2)
s3_block = {'sigma_e_eff_S_cm': 0.0, 'manifest': {'ca_ext': {'cjunc': {'evidence': {'fp': {'sid': reg['fp']['sid']}}}}},
            'conv_cert': foreign}
out = {'own_cert_problem': RC.conv_cert_problem(cert, 0.0), 'foreign_cert_problem': RC.conv_cert_problem(foreign, 0.0),
       'next_gen_cert_ok_with_foreign': RC.next_gen_cert_ok(s3_block),
       'cert_fp_sid': cert['fp_sid'], 'registry_fp_sid': reg['fp']['sid'], 'same_function': cert['fp_sid'] == reg['fp']['sid']}
for k, v in out.items():
    print(k, v)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_zero_binding.json'), out)
