#!/usr/bin/env python3
"""Probe: two VGCF fibres sharing the exact same start point (V-shape), first-segment x components both > 0.
Collinear subdivision of one fibre changes the second point -> canonical path order may flip -> ports / matrix / sigma bits?"""
import io
import contextlib
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import test_carbon_junction as T  # noqa: E402
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402

T.S3, T.CJ = S3, CJ
N = (6, 3, 8)
A = [(1.25, 1.5, 0.5), (3.25, 1.5, 2.5), (3.25, 1.5, 7.5)]      # first direction (1, 0, 1)
B = [(1.25, 1.5, 0.5), (5.25, 1.5, 2.5), (5.25, 1.5, 7.5)]      # first direction (2, 0, 1)


def run(stepA, stepB, fids=(10, 20)):
    PA = T.rows([A], step=stepA, fids=[fids[0]])
    PB = T.rows([B], step=stepB, fids=[fids[1]])
    P = T.cat_rows(PA, PB)
    sid, _ = T.bed(P, N)
    reg = T.registry(sid, P)
    pl = T.plan(reg, 1e3)
    r = T.solve(sid, T.sig_e(), N, pl)
    order = [int(f) for f in reg['positions']['fid'][np.r_[0, np.flatnonzero(np.diff(reg['positions']['piece'])) + 1]]]
    return sid, reg, r, order


base = run(0.25, 0.25)
sub = run(0.25, 0.125)
print('sid same:', base[0].tobytes() == sub[0].tobytes())
print('piece fid order base', base[3], 'sub', sub[3])
print('n_inst', len(base[1]['instances']['fi']), len(sub[1]['instances']['fi']))
print('sys same:', T.sys_bytes(base[2]) == T.sys_bytes(sub[2]))
print('sigma', repr(base[2]['sigma_eff']), repr(sub[2]['sigma_eff']), np.float64(base[2]['sigma_eff']).tobytes() == np.float64(sub[2]['sigma_eff']).tobytes())
print('ports base', base[1]['instances']['port_i'], base[1]['instances']['port_j'], 'sub', sub[1]['instances']['port_i'], sub[1]['instances']['port_j'])
