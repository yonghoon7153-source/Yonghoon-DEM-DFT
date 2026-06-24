#!/usr/bin/env python3
"""Image-based effective conductivity on the MPM voxel grid — the FEM/continuum
cross-check for the DEM network (Kirchhoff/Holm) solver.

Take the MPM phase grid (each voxel = void / SE / AM / VGCF / SuperP …), assign a
per-voxel conductivity for the channel of interest, hold the TOP face at 1 V and
the BOTTOM at 0 V, and solve ∇·(σ∇φ)=0 (finite-volume, harmonic-mean face
conductances, insulating side walls).  σ_eff = I·L / (A·ΔV) — the homogenised
conductivity a blocking-electrode EIS / 4-probe would read.

Channels:
  ionic      : SE conducts (σ_SE), AM + carbon + void block  → σ_eff,ion
  electronic : AM + VGCF + SuperP conduct, SE + void block   → σ_eff,e
               (carbon σ ≫ AM → fibres BRIDGE dead AM: the 도전재 payoff, quantified)

This gives the MPM a TRANSPORT readout (it had only mechanics) → a SECOND,
independent σ to validate the DEM network solver (frame[4]); and it ingests the
VGCF/SuperP phases from additives.py natively.

  python3 scripts/voxel_conductivity.py            # self-test (slab / series / parallel)
"""
from __future__ import annotations
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import cg

PHASE_SIGMA = {  # per channel; void always 0.  ionic/electronic mS/cm, thermal W/m·K
    'ionic':      {'SE': 3.0, 'AM': 0.0, 'VGCF': 0.0, 'SuperP': 0.0, 'PTFE': 0.0},
    'electronic': {'SE': 0.0, 'AM': 50.0, 'VGCF': 5.0e5, 'SuperP': 1.0e5, 'PTFE': 0.0},
    'thermal':    {'SE': 0.7, 'AM': 4.0, 'VGCF': 20.0, 'SuperP': 5.0, 'PTFE': 0.25},  # all solid conducts
}
PHASE_CODE = {'void': 0, 'AM': 0 - 9, 'SE': 1, 'VGCF': 2, 'SuperP': 3, 'PTFE': 4}  # AM handled separately


def sigma_from_phase(phase, channel, code2name, sigma_map=None):
    """phase: int 3D array of phase codes; code2name: {code: 'SE'/'AM'/...}.
    Returns per-voxel σ (float 3D), 0 where insulating for this channel."""
    sig = (sigma_map or PHASE_SIGMA[channel])
    out = np.zeros(phase.shape, np.float64)
    for code, name in code2name.items():
        out[phase == code] = sig.get(name, 0.0)
    return out


def effective_sigma(sigma, axis=2, dx=1.0, tol=1e-8, return_field=False):
    """Finite-volume solve of div(σ ∇φ)=0 with φ=1 on the high-`axis` face, φ=0 on
    the low face, no-flux side walls.  σ: 3D float (0 = insulator).  Returns σ_eff
    in the SAME units as σ (geometry cancels)."""
    sigma = np.moveaxis(sigma, axis, 2)            # solve along z
    # Trim leading/trailing z-slices that hold NO conducting cell so the Dirichlet faces sit on
    # the conducting phase's OWN envelope.  Without this, an interstitial phase that never reaches
    # the box floor/ceiling — e.g. SE packed under a rigid AM scaffold that rests on the floor —
    # reads σ_eff=0 even though it percolates internally (its cells touch the top face but not the
    # bottom k=0 face, which the AM occupies).  Internal all-insulator gaps are NOT trimmed, so a
    # genuinely disconnected phase still yields σ_eff=0.  L in σ_eff=I·L/A becomes the conducting
    # span → the slab's true conductivity, undiluted by headspace.
    zmask = (sigma > 0).any(axis=(0, 1))
    if not zmask.any():
        return (0.0, None) if return_field else 0.0
    z0 = int(np.argmax(zmask)); z1 = int(len(zmask) - np.argmax(zmask[::-1]))
    sigma = sigma[:, :, z0:z1]
    nx, ny, nz = sigma.shape
    cond = sigma > 0
    N = int(cond.sum())
    if N == 0:
        return (0.0, None) if return_field else 0.0
    gid = -np.ones(sigma.shape, np.int64)
    gid[cond] = np.arange(N)
    s = sigma
    diag = np.zeros(N)
    rows, cols, data = [], [], []

    def harm(a, c):                                 # harmonic-mean face conductance (vectorised)
        out = np.zeros(a.shape)
        m = (a > 0) & (c > 0)
        out[m] = 2.0 * a[m] * c[m] / (a[m] + c[m])
        return out

    # internal edges along each axis (x,y side walls are no-flux ⇒ just the interior pairs)
    for ax in (0, 1, 2):
        sa = [slice(None)] * 3; sa[ax] = slice(0, sigma.shape[ax] - 1)
        sb = [slice(None)] * 3; sb[ax] = slice(1, sigma.shape[ax])
        ga = gid[tuple(sa)].ravel(); gb = gid[tuple(sb)].ravel()
        g = harm(s[tuple(sa)], s[tuple(sb)]).ravel()
        m = (ga >= 0) & (gb >= 0) & (g > 0)
        ga, gb, g = ga[m], gb[m], g[m]
        rows += [ga, gb]; cols += [gb, ga]; data += [-g, -g]
        np.add.at(diag, ga, g); np.add.at(diag, gb, g)

    # z Dirichlet faces (½-cell ⇒ g=2σ): bottom k=0 → φ=0, top k=nz-1 → φ=1
    b = np.zeros(N)
    g0 = gid[:, :, 0].ravel(); s0 = s[:, :, 0].ravel(); m0 = g0 >= 0
    np.add.at(diag, g0[m0], 2.0 * s0[m0])
    g1 = gid[:, :, nz - 1].ravel(); s1 = s[:, :, nz - 1].ravel(); m1 = g1 >= 0
    np.add.at(diag, g1[m1], 2.0 * s1[m1]); b[g1[m1]] += 2.0 * s1[m1]

    rows.append(np.arange(N)); cols.append(np.arange(N)); data.append(np.where(diag > 0, diag, 1.0))
    A = csr_matrix((np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    phi, _ = cg(A, b, rtol=tol, maxiter=20000)

    I = float((2.0 * s0[m0] * phi[g0[m0]]).sum())  # current through the bottom Dirichlet face
    sigma_eff = I * nz / (nx * ny * 1.0)           # σ_eff = I·L/(A·ΔV), ΔV=1, L=nz, A=nx·ny
    if return_field:
        f = np.zeros(sigma.shape); f[cond] = phi
        return sigma_eff, f
    return sigma_eff


def _selftest():
    print('=== voxel effective-conductivity self-test ===')
    n = 24
    # 1) homogeneous slab σ=3 → σ_eff = 3
    hom = np.full((n, n, n), 3.0)
    print(f'  homogeneous σ=3.0           → σ_eff = {effective_sigma(hom):.4f}  (expect 3.000)')
    # 2) two layers in SERIES along z (σ1=2 bottom half, σ2=6 top) → harmonic mean = 3
    ser = np.empty((n, n, n)); ser[:, :, :n // 2] = 2.0; ser[:, :, n // 2:] = 6.0
    print(f'  series 2|6 (⊥ current)      → σ_eff = {effective_sigma(ser):.4f}  (expect 3.000 harmonic)')
    # 3) two columns in PARALLEL (σ1=2, σ2=6 split in x) → arithmetic mean = 4
    par = np.empty((n, n, n)); par[:n // 2] = 2.0; par[n // 2:] = 6.0
    print(f'  parallel 2|6 (∥ current)    → σ_eff = {effective_sigma(par):.4f}  (expect 4.000 arithmetic)')
    # 4) insulating slab blocking the path → σ_eff = 0 (no percolation)
    blk = np.full((n, n, n), 3.0); blk[:, :, n // 2] = 0.0
    print(f'  blocked layer (no percol.)  → σ_eff = {effective_sigma(blk):.4f}  (expect 0.000)')


# ── real-data path: voxelise the MPM phase cloud (+ AM scaffold) and run all channels ──
def _vc():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viz_mpm_continuum.py')
    spec = importlib.util.spec_from_file_location('viz_mpm_continuum', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def voxelize_phase(se_pts, phase, scaffold, n_vox, top=None):
    """Per-phase presence grids on the vc grid: AM from the scaffold spheres, SE/VGCF/SuperP/PTFE
    from the MPM point cloud (phase 1/2/3/4).  Returns ({name: bool grid}, h)."""
    vc = _vc()
    t, c, r = vc.load_am(scaffold)                         # AM spheres (box units)
    se1 = se_pts[phase == 1]                               # true SE points → SE occupancy
    if top is None:
        top = float(se_pts[:, 2].max()) + 0.01
    am_p, am_s, se_mask, h = vc.voxelize(se1, t, c, r, n_vox, top, 1, False)
    nx, ny, nz = se_mask.shape
    SW0, FLOOR = vc.SW[0], vc.FLOOR
    pres = {'AM': am_p | am_s, 'SE': se_mask}
    for code, name in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE')):
        g = np.zeros((nx, ny, nz), bool)
        m = phase == code
        if m.any():
            p = se_pts[m]
            ix = np.clip(((p[:, 0] - SW0) / h).astype(np.int64), 0, nx - 1)
            iy = np.clip(((p[:, 1] - SW0) / h).astype(np.int64), 0, ny - 1)
            iz = np.clip(((p[:, 2] - FLOOR) / h).astype(np.int64), 0, nz - 1)
            g[ix, iy, iz] = True
        pres[name] = g
    return pres, h


def sigma_grid(pres, channel, drop_carbon=False):
    """Per-cell σ = MAX σ over the phases present (a sub-grid carbon thread makes its cells
    conduct; for ionic the SE wins; void = 0).  drop_carbon → carbon insulating (WITHOUT-CBD)."""
    sig = dict(PHASE_SIGMA[channel])
    if drop_carbon:
        sig['VGCF'] = 0.0; sig['SuperP'] = 0.0
    out = np.zeros(next(iter(pres.values())).shape, np.float64)
    for name, g in pres.items():
        s = sig.get(name, 0.0)
        if s > 0:
            np.maximum(out, np.where(g, s, 0.0), out=out)
    return out


def _main():
    import argparse
    ap = argparse.ArgumentParser(description='Stage-2 voxel σ on the MPM phase grid (σ_e/σ_i/κ, ±CBD)')
    ap.add_argument('--se', required=True, help='se_carbon.npy — all MPM points (box units)')
    ap.add_argument('--phase', required=True, help='phase_carbon.npy — per-point phase (1 SE/2 VGCF/3 SuperP/4 PTFE)')
    ap.add_argument('--scaffold', required=True, help='am_scaffold.csv — AM spheres')
    ap.add_argument('--n-vox', type=int, default=128)
    ap.add_argument('--channel', default='all', choices=['ionic', 'electronic', 'thermal', 'all'])
    a = ap.parse_args()
    pts = np.load(a.se).astype(np.float64); phase = np.load(a.phase)
    if len(pts) != len(phase):
        raise SystemExit(f'se {len(pts)} != phase {len(phase)} — mismatched run (se_dump overwritten?)')
    u, cc = np.unique(phase, return_counts=True)
    print('phase counts:', {int(p): int(n) for p, n in zip(u, cc)})
    pres, h = voxelize_phase(pts, phase, a.scaffold, a.n_vox)
    print('grid', next(iter(pres.values())).shape, ' cells/phase:', {k: int(v.sum()) for k, v in pres.items()})
    chans = ['electronic', 'ionic', 'thermal'] if a.channel == 'all' else [a.channel]
    units = {'electronic': 'mS/cm', 'ionic': 'mS/cm', 'thermal': 'W/m·K'}
    print(f'\n  {"channel":<11}{"WITHOUT CBD":>14}{"WITH CBD":>14}{"gain":>9}')
    for ch in chans:
        s_wout = effective_sigma(sigma_grid(pres, ch, drop_carbon=True))
        s_with = effective_sigma(sigma_grid(pres, ch, drop_carbon=False))
        gain = f'{s_with / s_wout:>6.1f}x' if s_wout > 1e-9 else '  None→'   # σ_e=None revived
        print(f'  {ch:<11}{s_wout:>13.4g} {s_with:>13.4g}  {gain:>8}  ({units[ch]})')
    print('\n  electronic: carbon (VGCF/SuperP) BRIDGES dead AM → σ_e None→finite is the CBD payoff.')
    print('  ionic: carbon does NOT help; PTFE blocking shows as lower σ_i (Lee 2025 penalty).')


if __name__ == '__main__':
    import sys
    (_main() if '--se' in sys.argv else _selftest())
