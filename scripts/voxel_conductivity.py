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
    sigma = np.moveaxis(sigma, axis, 2)            # solve along z, restore later not needed
    nx, ny, nz = sigma.shape
    cond = sigma > 0
    idx = -np.ones(sigma.shape, np.int64)
    ids = np.argwhere(cond)
    idx[cond] = np.arange(len(ids))
    N = len(ids)
    if N == 0:
        return (0.0, None) if return_field else 0.0

    rows, cols, data = [], [], []
    b = np.zeros(N)
    s = sigma

    def gface(a, c):                                # harmonic-mean face conductance (dx cancels in σ_eff)
        return 2 * a * c / (a + c) if (a > 0 and c > 0) else 0.0

    for n, (i, j, k) in enumerate(ids):
        diag = 0.0
        for di, dj, dk in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            ii, jj, kk = i + di, j + dj, k + dk
            if dk == 0 and (ii < 0 or ii >= nx or jj < 0 or jj >= ny):
                continue                            # side walls: no-flux (Neumann)
            if kk < 0:                              # bottom face → φ=0 Dirichlet (½-cell ⇒ g=2σ)
                g = 2.0 * s[i, j, k];  diag += g;  continue
            if kk >= nz:                            # top face → φ=1 Dirichlet (½-cell ⇒ g=2σ)
                g = 2.0 * s[i, j, k];  diag += g;  b[n] += g * 1.0;  continue
            g = gface(s[i, j, k], s[ii, jj, kk])
            if g > 0:
                diag += g
                rows.append(n); cols.append(idx[ii, jj, kk]); data.append(-g)
        rows.append(n); cols.append(n); data.append(diag if diag > 0 else 1.0)
    A = csr_matrix((data, (rows, cols)), shape=(N, N))
    phi, _ = cg(A, b, rtol=tol, maxiter=20000)

    # current through the bottom Dirichlet face: I = Σ g·(φ_voxel − 0)
    I = 0.0
    for n, (i, j, k) in enumerate(ids):
        if k == 0:
            I += 2.0 * s[i, j, k] * phi[n]          # bottom Dirichlet face g=2σ (½-cell)
    sigma_eff = I * nz / (nx * ny * 1.0)            # σ_eff = I·L/(A·ΔV), ΔV=1, L=nz, A=nx·ny
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


if __name__ == '__main__':
    _selftest()
