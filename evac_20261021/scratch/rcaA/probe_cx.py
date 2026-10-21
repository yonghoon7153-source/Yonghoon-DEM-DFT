#!/usr/bin/env python3
"""CX bed terminal current with the scripts dir given (current tree or base snapshot) — R_j 200 ohm (RCA05 test value)."""
import sys

sys.path.insert(0, sys.argv[1])
import test_carbon_junction as T  # noqa: E402
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

T.S3, T.CJ = S3, CJ
P = T.rows(T.CX) if hasattr(T, 'CX') else None
CXv = [[(1.5, 1.5, 0.5), (1.5, 1.5, 10.5)], [(2.1, 1.5, 10.5), (2.1, 1.5, 1.2), (6.5, 1.5, 1.2), (6.5, 1.5, 13.5)]]
N = (8, 3, 14)
P = T.rows(CXv)
sid, _ = T.bed(P, N)
reg = T.registry(sid, P)
r = T.solve(sid, T.sig_e(), N, T.plan(reg, 200.0))
print('I_code', repr(T.I_of(r, N)), 'n_inst', len(reg['instances']['fi']), 'Lc', reg['instances']['Lc'].tolist())
