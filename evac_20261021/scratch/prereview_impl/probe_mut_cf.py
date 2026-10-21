# -*- coding: utf-8 -*-
"""탐침 D2 — MUT-RCA 의 '반사실이 SV 면을 안 끊음' 변이는 지금 서명 (certify= 키워드) 이 안 맞아 TypeError 로 '잡힌다' (옳은 이유 아님).
서명을 맞춘 같은 변이로 RCA06 의 SVX 꼴 비 검사 (`sv_ok` 와 같은 식) 가 옳은 이유로 실패하는지 본다."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

SVX_N = (5, 3, 22)
SVX = [[(1.5, 1.5, 0.5), (1.5, 1.5, 20.5)], [(2.1, 1.5, 1.5), (3.5, 1.5, 1.5), (3.5, 1.5, 21.5)]]
SVX_SDCP = [[(2.5, 1.5, 20.5)]]
RJ = 2.0e4
P = cat_rows(rows(SVX), rows(SVX_SDCP, phase=5, kind=0, fid0=700))
sid, _ = bed(P, SVX_N)
reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)


def ratio():
    r = solve(sid, sig_e(), SVX_N, plan(reg, RJ, sv_counterfactual={'threshold': None}))
    return ((r.get('cjunc') or {}).get('sv_counterfactual') or {}).get('sv_counterfactual_ratio')


base = ratio()
real = CJ.CjuncAssembler.sv_counterfactual


def cf_nodrop_fixed(self, solve_, I_full, request, certify=None):   # 같은 변이 · 서명만 지금 판에 맞춤
    orig = self._assemble
    self._assemble = lambda *a, **k: orig(*a, **dict(k, drop_cat=None))
    try:
        return real(self, solve_, I_full, request, certify=certify)
    finally:
        del self._assemble


def cf_nodrop_old(self, solve_, I_full, request):                   # 시험에 있는 변이 그대로 (옛 서명)
    return real(self, solve_, I_full, request)


out = {'base_ratio': base}
for tag, fn in (('mutant_fixed_signature', cf_nodrop_fixed), ('mutant_test_as_written', cf_nodrop_old)):
    CJ.CjuncAssembler.sv_counterfactual = fn
    try:
        try:
            out[tag] = {'ratio': ratio(), 'exception': None}
        except Exception as e:                                      # noqa: BLE001
            out[tag] = {'ratio': None, 'exception': f'{type(e).__name__}: {e}'}
    finally:
        CJ.CjuncAssembler.sv_counterfactual = real
print(out)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_mut_cf.json'), out)
