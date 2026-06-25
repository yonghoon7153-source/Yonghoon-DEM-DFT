#!/usr/bin/env python3
"""Randomly thin an AM scaffold CSV → a controlled AM-POOR network for the CBD
electronic-bridging crossover probe (SuperP vs VGCF).

The CBD electronic gain on a GOOD AM network (input_8mAh_real_10) favours SuperP
(many distributed contacts mop up the few isolated AM).  Literature (P11/P12) says
1D VGCF wins in the AM-POOR / percolation-limited regime (long fibres bridge gaps
0D carbon can't reach).  To test that crossover with ONLY ONE variable changed —
AM-network density — we keep the SAME SE + carbon MPM dump and just DECIMATE the AM
scaffold, opening dead gaps for the carbon to bridge.

Usage:
  python3 scripts/decimate_scaffold.py am_carbon.csv am_carbon_p30.csv --keep 0.30 --seed 0

Format (matches viz_mpm_continuum.load_am): comma-delimited, no header,
columns = [type(1=AM_P,2=AM_S), x, y, z, r]  (box units).  Same decimated file
must be used for BOTH SuperP and VGCF voxel runs (same seed → identical AM-poor
geometry → fair morphology comparison).
"""
import argparse
import numpy as np


def main():
    ap = argparse.ArgumentParser(description='Randomly thin an AM scaffold CSV (AM-poor crossover probe).')
    ap.add_argument('src', help='input am_scaffold.csv ([type,x,y,z,r], no header)')
    ap.add_argument('dst', help='output decimated csv')
    ap.add_argument('--keep', type=float, required=True, help='fraction of AM particles to KEEP (0<f<=1)')
    ap.add_argument('--seed', type=int, default=0, help='RNG seed — use the SAME seed for SuperP & VGCF')
    a = ap.parse_args()
    if not (0.0 < a.keep <= 1.0):
        raise SystemExit('--keep must be in (0, 1]')

    am = np.atleast_2d(np.loadtxt(a.src, delimiter=','))
    n = len(am)
    t = am[:, 0].astype(int)
    n_keep = max(1, int(round(n * a.keep)))
    rng = np.random.default_rng(a.seed)
    idx = np.sort(rng.choice(n, size=n_keep, replace=False))
    kept = am[idx]

    np.savetxt(a.dst, kept, delimiter=',', fmt=['%d', '%.8g', '%.8g', '%.8g', '%.8g'])

    def _split(types):
        p = int((types == 1).sum()); return p, len(types) - p
    p0, s0 = _split(t)
    p1, s1 = _split(kept[:, 0].astype(int))
    print(f'  {a.src} → {a.dst}  (seed {a.seed})')
    print(f'  kept {n_keep}/{n} AM ({100*n_keep/n:.0f}%)   AM_P {p0}→{p1}   AM_S {s0}→{s1}')


if __name__ == '__main__':
    main()
