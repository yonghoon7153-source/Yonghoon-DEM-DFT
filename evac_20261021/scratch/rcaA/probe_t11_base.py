#!/usr/bin/env python3
"""T1-11 (A / A_FAR) ports and terminal current with the production modules of a given scripts dir.
argv: <production scripts dir> <current test file path>"""
import importlib.util
import sys

sys.path.insert(0, sys.argv[1])
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

spec = importlib.util.spec_from_file_location('tcj_current', sys.argv[2])
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
T.S3, T.CJ = S3, CJ
for nm, A in (('A', T.T4_A), ('A_FAR', T.T4_A_FAR)):
    P = T.rows([A, T.T4_B])
    sid, _ = T.bed(P, T.T4_N)
    reg = T.registry(sid, P)
    r = T.solve(sid, T.sig_e(), T.T4_N, T.plan(reg, 1e3))
    print(nm, 'port_i', T._pcells(reg, 0, 'i'), 'port_j', T._pcells(reg, 0, 'j'), 'I', repr(T.I_of(r, T.T4_N)))
