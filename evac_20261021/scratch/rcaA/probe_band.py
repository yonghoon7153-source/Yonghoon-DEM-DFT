#!/usr/bin/env python3
"""Probe: T1-11 geometry shifted by a non-dyadic origin offset -> contact point on the cell boundary up to rounding.
For each offset: d2 to the two tie candidates (cells (1,1,2) / (1,1,3)), and which one a strict argmin (no eps band) picks."""
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import test_carbon_junction as T  # noqa: E402
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

T.S3, T.CJ = S3, CJ
offs = [(0.0, 0.0, 0.0), (0.1, 0.1, 0.1), (0.3, 0.3, 0.3), (0.7, 0.7, 0.7), (0.1, 0.2, 0.3), (0.01, 0.02, 0.03),
        (1.1, 1.3, 1.7), (0.123, 0.456, 0.789), (0.2, 0.2, 0.2), (0.6, 0.6, 0.6), (0.9, 0.9, 0.9), (2.3, 2.3, 2.3)]
for o in offs:
    o = np.asarray(o, np.float64)
    shift = lambda poly: [tuple(np.asarray(p, np.float64) + o) for p in poly]  # noqa: E731
    for nm, A in (('A', T.T4_A), ('A_far', T.T4_A_FAR)):
        P = T.rows([shift(A), shift(T.T4_B)])
        sid, _ = T.bed(P, T.T4_N, lo=tuple(o))
        reg = T.registry(sid, P, lo=tuple(o))
        I = reg['instances']
        if len(I['fi']) != 1:
            print(o, nm, 'n_inst', len(I['fi']))
            continue
        pos = reg['positions']
        C = I['Ci'][0]
        lo = np.asarray(o)
        cells = [(1, 1, 2), (1, 1, 3)]
        d2 = [float(np.sum((lo + (np.asarray(c) + 0.5) * T.H - C) ** 2)) for c in cells]
        pi = int(I['port_i'][0])
        print(tuple(o), nm, 'C', C.tolist(), 'd2', d2, 'diff', d2[0] - d2[1], 'port', tuple(int(v) for v in pos['ijk'][pi]),
              'tie', bool(I['tie_i'][0]), 'strict pick', cells[int(np.argmin(d2))] if d2[0] != d2[1] else 'exact tie')
