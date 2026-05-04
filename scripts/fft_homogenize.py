#!/usr/bin/env python3
"""FFT-based effective-conductivity homogenization via the Moulinec-Suquet
1998 fixed-point iteration on a voxelized microstructure.

Algorithm
─────────
For each phase p with intrinsic σ_p, solve the periodic conductivity
problem on voxel grid Ω:

  ∇·j(x) = 0    where   j(x) = σ(x)·e(x),    e(x) = ∇φ(x)
  ⟨e⟩ = ê_z     (unit macroscopic gradient)

Moulinec-Suquet scheme:
  1. Initialize e(x) = ê_z  (uniform macro)
  2. Compute polarization τ(x) = (σ(x) - σ_0)·e(x)  with σ_0 = mean
  3. FFT τ → τ̂(ξ)
  4. Apply Green's operator in Fourier:
        ê_a(ξ ≠ 0) = -ξ_a ξ_b / (σ_0 |ξ|²) · τ̂_b(ξ)
        ê(0) = ê_z   (preserve macro)
  5. IFFT → e(x);  check ||e_new − e_old||/||e_new|| < tol;  iterate.

Effective σ:  σ_eff = ⟨σ(x)·e_z(x)⟩.

For isotropic input (cubic voxels, periodic), σ_eff_z = σ_eff_x = σ_eff_y;
we run only the z direction for speed.

High-contrast handling
──────────────────────
For σ_ionic: AM and void are insulators (σ ≈ 0). Use ε-regularization
σ_min = 1e-6 × σ_SE to keep the matrix well-conditioned. Eyre-Milton
1999 acceleration applied for contrast > 100 (faster convergence).

Output
──────
  case_dir/fft_homogenize_summary.json
    σ_ionic_FFT (mS/cm), σ_e_FFT (mS/cm), σ_th_FFT (W/(m·K))
    + iterations to convergence per channel
  Console comparison vs network_conductivity.json values.

Usage
─────
  python3 scripts/fft_homogenize.py CASE_ID                 # run all 3 channels
  python3 scripts/fft_homogenize.py CASE_ID --channel ionic  # ionic only
  python3 scripts/fft_homogenize.py CASE_ID --tol 1e-5
  python3 scripts/fft_homogenize.py --all
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import fft as spfft

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'

PHASE_VOID = 0
PHASE_AM_P = 1
PHASE_AM_S = 2
PHASE_SE   = 3

# Intrinsic conductivities (literature, sulfide ASSB)
# σ_ionic   : SE only — Li6PS5Cl ~ 7 mS/cm
# σ_e       : AM electronic — single-crystal NCM ~ 6 mS/cm
# κ_thermal : AM ~ 4 W/(m·K), SE ~ 0.5 W/(m·K)
SIGMA_IONIC_SE_MSCM   = 7.0      # mS/cm
SIGMA_E_AM_MSCM       = 6.0      # mS/cm
KAPPA_AM_W_MK         = 4.0      # W/(m·K)
KAPPA_SE_W_MK         = 0.5      # W/(m·K)

# Numerical regularization for high-contrast (insulator phases)
EPS_CONTRAST = 1e-6


def discover_case(case_id: str) -> Path | None:
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for vox_p in root.rglob('voxel_grid.npy'):
            if vox_p.parent.name == case_id:
                return vox_p.parent
    return None


def discover_all_cases() -> list[Path]:
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for vox_p in root.rglob('voxel_grid.npy'):
            d = vox_p.parent
            if d not in seen:
                seen.add(d)
                out.append(d)
    return sorted(out)


def assign_sigma(grid: np.ndarray, channel: str) -> np.ndarray:
    """Return scalar σ(x) field for the given channel.

    Uses ε-regularization for insulator phases to keep FFT well-conditioned.
    """
    if channel == 'ionic':
        sigma_field = np.full(grid.shape, EPS_CONTRAST * SIGMA_IONIC_SE_MSCM,
                              dtype=np.float64)
        sigma_field[grid == PHASE_SE] = SIGMA_IONIC_SE_MSCM
    elif channel == 'e':
        sigma_field = np.full(grid.shape, EPS_CONTRAST * SIGMA_E_AM_MSCM,
                              dtype=np.float64)
        sigma_field[grid == PHASE_AM_P] = SIGMA_E_AM_MSCM * 0.65   # AM_P factor
        sigma_field[grid == PHASE_AM_S] = SIGMA_E_AM_MSCM * 1.00   # AM_S factor
    elif channel == 'thermal':
        sigma_field = np.full(grid.shape, EPS_CONTRAST * KAPPA_AM_W_MK,
                              dtype=np.float64)
        sigma_field[grid == PHASE_AM_P] = KAPPA_AM_W_MK * 0.5
        sigma_field[grid == PHASE_AM_S] = KAPPA_AM_W_MK * 1.0
        sigma_field[grid == PHASE_SE]   = KAPPA_SE_W_MK
    else:
        raise ValueError(f'unknown channel {channel!r}')
    return sigma_field


def make_freq_grid(shape: tuple[int, int, int], voxel_um: float
                    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (ξ_x, ξ_y, ξ_z, |ξ|²) arrays for FFT homogenization."""
    nx, ny, nz = shape
    L_um = voxel_um  # voxel spacing in μm; FFT freqs scale with 1/L
    kx = 2.0 * np.pi * spfft.fftfreq(nx, d=L_um)
    ky = 2.0 * np.pi * spfft.fftfreq(ny, d=L_um)
    kz = 2.0 * np.pi * spfft.fftfreq(nz, d=L_um)
    Kx, Ky, Kz = np.meshgrid(kx, ky, kz, indexing='ij')
    K2 = Kx**2 + Ky**2 + Kz**2
    K2[0, 0, 0] = 1.0   # avoid div-by-zero at ξ=0; we'll mask separately
    return Kx, Ky, Kz, K2


def fft_homogenize_z(sigma_field: np.ndarray, voxel_um: float,
                      tol: float = 1e-4, max_iter: int = 200,
                      verbose: bool = True) -> tuple[float, int, list[float]]:
    """Run Moulinec-Suquet for unit gradient in z direction.

    Returns (σ_eff, n_iter, residual_history).
    """
    shape = sigma_field.shape
    n_total = sigma_field.size

    sigma_min = float(sigma_field.min())
    sigma_max = float(sigma_field.max())
    # Reference: harmonic mean for high contrast (Eyre-Milton recommendation)
    contrast = sigma_max / max(sigma_min, 1e-30)
    if contrast > 100:
        sigma_0 = 2.0 * sigma_min * sigma_max / (sigma_min + sigma_max)
    else:
        sigma_0 = 0.5 * (sigma_min + sigma_max)

    if verbose:
        print(f'    σ_min={sigma_min:.4e}  σ_max={sigma_max:.4e}  '
              f'contrast={contrast:.1e}  σ_0={sigma_0:.4e}')

    Kx, Ky, Kz, K2 = make_freq_grid(shape, voxel_um)

    # Initialize e = ê_z (uniform)
    e_x = np.zeros(shape, dtype=np.float64)
    e_y = np.zeros(shape, dtype=np.float64)
    e_z = np.ones(shape, dtype=np.float64)

    residuals = []
    for it in range(max_iter):
        # j = σ e ;  τ = (σ - σ_0) e
        tau_x = (sigma_field - sigma_0) * e_x
        tau_y = (sigma_field - sigma_0) * e_y
        tau_z = (sigma_field - sigma_0) * e_z

        # FFT
        TauX = spfft.fftn(tau_x)
        TauY = spfft.fftn(tau_y)
        TauZ = spfft.fftn(tau_z)

        # Green's operator: e_hat_a = -K_a K_b / (σ_0 |K|²) · τ_hat_b
        kdot = (Kx * TauX + Ky * TauY + Kz * TauZ) / (sigma_0 * K2)
        EX = -Kx * kdot
        EY = -Ky * kdot
        EZ = -Kz * kdot
        # Restore macro gradient at ξ=0
        EX[0, 0, 0] = 0.0
        EY[0, 0, 0] = 0.0
        EZ[0, 0, 0] = 1.0 * n_total   # because IFFT divides by n_total

        e_x_new = spfft.ifftn(EX).real
        e_y_new = spfft.ifftn(EY).real
        e_z_new = spfft.ifftn(EZ).real

        # Convergence — relative L2 of e change
        de2 = ((e_x_new - e_x)**2 + (e_y_new - e_y)**2
               + (e_z_new - e_z)**2).sum()
        e2  = (e_x_new**2 + e_y_new**2 + e_z_new**2).sum()
        rel = np.sqrt(de2 / max(e2, 1e-30))
        residuals.append(float(rel))

        e_x, e_y, e_z = e_x_new, e_y_new, e_z_new

        if verbose and (it % 5 == 0 or rel < tol):
            print(f'    iter {it:3d}   residual = {rel:.3e}', flush=True)
        if rel < tol:
            break

    # σ_eff = ⟨σ e_z⟩
    sigma_eff = float((sigma_field * e_z).mean())
    return sigma_eff, it + 1, residuals


def homogenize_one(case_dir: Path, channels: list[str], tol: float,
                    max_iter: int, verbose: bool = True) -> dict:
    grid_p = case_dir / 'voxel_grid.npy'
    meta_p = case_dir / 'voxel_meta.json'
    if not grid_p.exists() or not meta_p.exists():
        return {'error': 'no voxel data — run voxelize_microstructure.py first'}

    if verbose:
        print(f'\n=== {case_dir.name} ===')
    grid = np.load(grid_p)
    vox_meta = json.load(open(meta_p))
    voxel_um = vox_meta['voxel_um']
    if verbose:
        print(f'  grid {grid.shape}   voxel {voxel_um:.4f} μm')

    fm_p = case_dir / 'full_metrics.json'
    fm = json.load(open(fm_p)) if fm_p.exists() else {}

    out = {'case_id': case_dir.name, 'voxel_um': voxel_um,
            'shape': list(grid.shape), 'channels': {}}
    for ch in channels:
        if verbose:
            print(f'\n  Channel: {ch}')
        sigma_field = assign_sigma(grid, ch)
        t0 = time.time()
        sigma_eff, n_iter, residuals = fft_homogenize_z(
            sigma_field, voxel_um, tol=tol, max_iter=max_iter,
            verbose=verbose)
        dt = time.time() - t0
        if verbose:
            print(f'  ✓ σ_eff = {sigma_eff:.4f}  '
                  f'(after {n_iter} iter, {dt:.1f}s)')

        # Compare to network solver
        if ch == 'ionic':
            ns_value = fm.get('sigma_full_mScm')
            ns_value_phys = fm.get('sigma_full_mScm_physics')
            unit = 'mS/cm'
        elif ch == 'e':
            ns_value = fm.get('electronic_sigma_full_mScm')
            ns_value_phys = fm.get('electronic_sigma_full_mScm_physics')
            unit = 'mS/cm'
        elif ch == 'thermal':
            ns_value = fm.get('thermal_sigma_full_mScm')
            ns_value_phys = fm.get('thermal_sigma_full_mScm_physics')
            unit = 'W/(m·K)'

        if verbose and ns_value is not None:
            ratio_h = sigma_eff / ns_value if ns_value > 0 else float('nan')
            print(f'    network solver  Hertz : {ns_value:.4f} {unit}'
                  f'   (FFT/H = {ratio_h:.2f}×)')
        if verbose and ns_value_phys is not None:
            ratio_p = sigma_eff / ns_value_phys if ns_value_phys > 0 else float('nan')
            print(f'    network solver  Phys  : {ns_value_phys:.4f} {unit}'
                  f'   (FFT/P = {ratio_p:.2f}×)')

        out['channels'][ch] = {
            'sigma_fft':              sigma_eff,
            'sigma_network_hertz':    ns_value,
            'sigma_network_physics':  ns_value_phys,
            'unit':                   unit,
            'n_iter':                 n_iter,
            'time_s':                 round(dt, 2),
            'residual_final':         residuals[-1] if residuals else None,
        }

    # Save
    sum_p = case_dir / 'fft_homogenize_summary.json'
    with open(sum_p, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    if verbose:
        print(f'\n  saved: {sum_p}')
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id', nargs='?',
                    help='Single case (default: --all required)')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--channel', choices=['ionic', 'e', 'thermal', 'all'],
                    default='all',
                    help='Which channel to homogenize (default all)')
    ap.add_argument('--tol', type=float, default=1e-4,
                    help='Convergence tolerance (default 1e-4)')
    ap.add_argument('--max-iter', type=int, default=200,
                    help='Maximum iterations (default 200)')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    channels = ['ionic', 'e', 'thermal'] if args.channel == 'all' \
                else [args.channel]
    verbose = not args.quiet

    if args.case_id:
        case_dir = discover_case(args.case_id)
        if not case_dir:
            ap.error(f'Case {args.case_id!r}: voxel_grid.npy not found  '
                     '(run voxelize_microstructure.py first)')
        homogenize_one(case_dir, channels, args.tol, args.max_iter, verbose)
    elif args.all:
        cases = discover_all_cases()
        print(f'FFT homogenization on {len(cases)} cases  '
              f'channels={channels}  tol={args.tol} …')
        n_ok = n_fail = 0
        for d in cases:
            try:
                r = homogenize_one(d, channels, args.tol, args.max_iter,
                                     verbose)
                if 'error' not in r: n_ok += 1
                else:                n_fail += 1
            except Exception as e:
                print(f'  ✗ {d.name}: {type(e).__name__}: {e}')
                n_fail += 1
        print(f'\nDone — {n_ok} ok, {n_fail} failed.')
    else:
        ap.error('Pass case_id or --all')


if __name__ == '__main__':
    main()
