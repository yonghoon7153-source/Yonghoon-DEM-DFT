#!/usr/bin/env python3
"""SVX (RCA-06 bed): old guard record vs new diagnostic / counterfactual with the production modules of a given scripts dir."""
import importlib.util
import sys

sys.path.insert(0, sys.argv[1])
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

spec = importlib.util.spec_from_file_location('tcj_current', sys.argv[2])
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
T.S3, T.CJ = S3, CJ
P = T.cat_rows(T.rows(T.SVX), T.rows(T.SVX_SDCP, phase=5, kind=0, fid0=700))
sid, _ = T.bed(P, T.SVX_N)
reg = T.registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
kw = {}
try:
    pl = T.plan(reg, T.SVX_RJ, sv_counterfactual={'threshold': None})
except TypeError:
    pl = T.plan(reg, T.SVX_RJ)
r = T.solve(sid, T.sig_e(), T.SVX_N, pl)
cj = r.get('cjunc') or {}
print('I', repr(T.I_of(r, T.SVX_N)), 'sv_dominant', cj.get('sv_dominant'), 'sv_local', cj.get('sv_local_dissipation'),
      'cf', {k: cj.get('sv_counterfactual', {}).get(k) for k in ('status', 'sv_counterfactual_ratio', 'G_cut_code')} if cj.get('sv_counterfactual') else None,
      'sv_face_abs_current_over_I', cj.get('sv_face_abs_current_over_I'))
