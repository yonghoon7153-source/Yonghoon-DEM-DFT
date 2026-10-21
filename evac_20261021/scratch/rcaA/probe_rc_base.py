#!/usr/bin/env python3
"""RCA-03 loop chain (RC fixture of the current test file) solved with the production modules of a given scripts dir.
argv: <production scripts dir> <current test file path>"""
import importlib.util
import sys

sys.path.insert(0, sys.argv[1])
import step3_sigma as S3  # noqa: E402  (production modules from argv[1], cached before the test module loads)
import carbon_junction as CJ  # noqa: E402
import fibre_segment_raster  # noqa: E402,F401

spec = importlib.util.spec_from_file_location('tcj_current', sys.argv[2])
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
T.S3, T.CJ = S3, CJ
P, sid = T._rc_bed()
reg = T._rc_reg(sid, P, 5.0)
r = T.solve(sid, T.sig_e(), T.RC_N, T.plan(reg, 1e3), vox=T.RC_H)
seq = T.seq_cells_v(T.RC_LOOP, T.RC_H, T.RC_STEP)
print('I', repr(T.I_of(r, T.RC_N, vox=T.RC_H)), 'chain_ref', repr(T.chain_ref(len(seq), g_ax=T.RC_GAX, g_pl=T.RC_GPL)), 'CJ', CJ.__file__)
