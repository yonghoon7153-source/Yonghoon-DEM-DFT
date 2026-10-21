#!/usr/bin/env python3
"""Probe mutant M16 in memory (no file change): contact point / ports for PCP and PCP-FAR under 'argmin first pair'."""
import importlib.util
import sys
import types

import numpy as np

SCR = sys.argv[1]
sys.path.insert(0, SCR)
src = open(SCR + '/carbon_junction.py', encoding='utf-8').read()
old = "        b = bnd[np.lexsort((j[bnd], i[bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]]\n"
assert src.count(old) == 1
mut = types.ModuleType('carbon_junction')
mut.__file__ = SCR + '/carbon_junction.py'
exec(compile(src.replace(old, "        b = mem[np.argmin(d[mem])]\n"), mut.__file__, 'exec'), mut.__dict__)
sys.modules['carbon_junction'] = mut
import test_carbon_junction as T  # noqa: E402
import step3_sigma as S3  # noqa: E402

T.S3, T.CJ = S3, mut
for nm, polys in (('PCP', T.PCP), ('PCP-FAR', [T.PCP_AFAR, T.PCP[1]])):
    P = T.rows_exact(polys)
    sid, _ = T.bed(P, T.PCP_N)
    reg = T.registry(sid, P)
    I = reg['instances']
    print(nm, 'Ci', I['Ci'].tolist(), 'Cj', I['Cj'].tolist(), 'ports', T._pcells(reg, 0, 'i'), T._pcells(reg, 0, 'j'),
          'piece_i', I['piece_i'].tolist(), 'fi', I['fi'].tolist())
