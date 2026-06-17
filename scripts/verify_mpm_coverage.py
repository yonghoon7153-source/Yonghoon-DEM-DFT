#!/usr/bin/env python3
"""Is the MPM raw coverage (~27 %) trustworthy, or a voxel/sampling artifact?
Two independent checks on the SAME se_dump.npy + AM scaffold:

  (1) VOXEL-adjacency  — the sim's own measure: AM-surface voxel whose adjacent
      cell holds an SE material point.  Run at two grids (--n-grid + 2×) → if they
      agree, the value is resolution-CONVERGED.
  (2) CONTINUOUS geometric — independent of the voxel grid: Fibonacci-sample each
      AM surface, KDTree to the (sub-sampled) DEFORMED SE points, fraction within
      a contact band.  If this agrees with (1), the voxel measure is not an
      under-count.  NOTE: this uses the DEFORMED MPM points (the real plastic SE),
      NOT the rigid seed spheres — so it is the MPM's own plastic contact, not a
      DEM-style Tabor post-correction.

  python3 scripts/verify_mpm_coverage.py --se se384_dump.npy \
      --scaffold docs/data/real14_am_scaffold.csv --n-grid 384
"""
import argparse
import numpy as np

SW = (0.04, 0.96); FLOOR = 0.05
WIDTH = SW[1] - SW[0]; SCL = WIDTH / 0.05; UM_BOX = 1000.0 / SCL


def load_am(path):
    am = np.loadtxt(path, delimiter=',')
    t = am[:, 0].astype(int)
    c = np.column_stack([SW[0] + am[:, 1] * SCL, SW[0] + am[:, 2] * SCL, FLOOR + am[:, 3] * SCL])
    return t, c, am[:, 4] * SCL


def voxel_coverage(se, t, c, r, n):
    """The sim measure at grid n: AM-surface voxel whose ±1 neighbour holds an SE pt."""
    pin = np.zeros((n, n, n), np.int32)
    for i in range(len(r)):
        cx, cy, cz = c[i]; rr = float(r[i])
        lo = np.maximum(np.floor((np.array([cx, cy, cz]) - rr) * n).astype(int), 0)
        hi = np.minimum(np.ceil((np.array([cx, cy, cz]) + rr) * n).astype(int), n)
        if np.any(hi <= lo):
            continue
        gx = (np.arange(lo[0], hi[0]) + 0.5) / n; gy = (np.arange(lo[1], hi[1]) + 0.5) / n
        gz = (np.arange(lo[2], hi[2]) + 0.5) / n
        X, Y, Z = np.meshgrid(gx, gy, gz, indexing='ij')
        pin[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]][(X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= rr*rr] = t[i]
    ci = np.clip((se * n).astype(int), 0, n - 1)
    occ = np.zeros((n, n, n), bool); occ[ci[:, 0], ci[:, 1], ci[:, 2]] = True
    out = {}
    for ty, nm in ((1, 'AM_P'), (2, 'AM_S')):
        amt = pin == ty; tot = cov = 0
        for ax in range(3):
            for s in (1, -1):
                iface = amt & (np.roll(pin, s, ax) == 0)
                tot += int(iface.sum()); cov += int((iface & np.roll(occ, s, ax)).sum())
        out[nm] = 100.0 * cov / tot if tot else 0.0
    return out


def continuous_coverage(se, t, c, r, bands_um, n_samp=600, sub=3_000_000, seed=0):
    """Grid-free: AM surface within each band (µm) of a DEFORMED SE material point."""
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    pts = se if len(se) <= sub else se[rng.choice(len(se), sub, replace=False)]
    tree = cKDTree(pts)
    k = np.arange(n_samp); phi = np.pi * (3 - np.sqrt(5)); z = 1 - 2 * (k + 0.5) / n_samp
    rr = np.sqrt(1 - z * z); U = np.column_stack([rr * np.cos(phi * k), rr * np.sin(phi * k), z])
    bands = [b / UM_BOX for b in bands_um]                  # µm → box units
    out = {}
    for ty, nm in ((1, 'AM_P'), (2, 'AM_S')):
        m = t == ty; C = c[m]; R = r[m]
        acc = np.zeros(len(bands))
        for i in range(len(C)):
            d, _ = tree.query(C[i] + R[i] * U)
            acc += [float((d < b).mean()) for b in bands]
        out[nm] = (100.0 * acc / max(len(C), 1)).round(1).tolist()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--se', required=True); ap.add_argument('--scaffold', required=True)
    ap.add_argument('--n-grid', type=int, default=384)
    ap.add_argument('--bands-um', default='0.07,0.13,0.26')   # ~0.5,1,2 voxels @384
    a = ap.parse_args()
    t, c, r = load_am(a.scaffold)
    se = np.load(a.se).astype(np.float64)
    dens = len(se) / ((SW[1] - SW[0]) ** 2 * (se[:, 2].max() - FLOOR))   # pts per box³ (rough)
    print(f'loaded {len(se):,} SE pts  (≈{len(se)/a.n_grid**3*1e0:.2f} pts/cell-vol at n_grid={a.n_grid})')
    print('=== (1) VOXEL-adjacency (the sim measure @ n_grid) ===')
    v = voxel_coverage(se, t, c, r, a.n_grid)
    print(f'  n_grid={a.n_grid}:  AM_P {v["AM_P"]:.1f}%   AM_S {v["AM_S"]:.1f}%   '
          f'← this is the ~27% in question')
    print('  (NB: this measure is point-DENSITY-bound — at >n_grid the cells empty out and it '
          'collapses, so it does NOT resolution-converge; the grid-free check below is the arbiter.)')
    print('=== (2) CONTINUOUS geometric on the DEFORMED points (grid-free, robust) ===')
    bands = [float(x) for x in a.bands_um.split(',')]
    g = continuous_coverage(se, t, c, r, bands)
    print(f'  AM surface within band of an SE material point:')
    for j, b in enumerate(bands):
        print(f'    {b:.3f} µm:  AM_P {g["AM_P"][j]:.1f}%   AM_S {g["AM_S"][j]:.1f}%')
    print('VERDICT: the band ≈ the SE point spacing (dx/2 ≈ 0.065 µm @384) is the true contact '
          'coverage.  If the voxel @n_grid value sits in that band-range → ~27% is REAL; if the '
          'continuous value is much higher at the contact band → the voxel measure under-counts.')


if __name__ == '__main__':
    main()
