#!/usr/bin/env python3
"""Seed conductive additives (VGCF fibres, Super P / Super C carbon black, PTFE
binder) as EXTRA MPM material phases — counts derived from the electrode recipe,
never hard-coded.

Why this works cheaply where LIGGGHTS can't: the discrete DEM would need millions
of nano objects (Super P ~40 nm, VGCF Ø~0.15 µm) → impossible.  The MPM is a
grid/continuum whose cost is resolution-bound, and it already carries a PER-POINT
material (µ, λ, σ_y) — so an additive is just "more material points with different
constants", no kernel change.  Nano features stay sub-grid → they enter as a
HOMOGENISED phase (a fibre = a chain of points along its axis; carbon black = a
small blob), evenly distributed through the box (optionally avoiding the fixed AM).

Recipe → count chain (densities g/cm³, literature):
  AM(NMC811) 4.80 · SE(Li6PS5Cl) 1.64 · VGCF 2.00 · SuperP 1.90 · PTFE 2.20
  wt%  --(/ρ)-->  vol%  --(× solid_vol)-->  phase volume  --(/ vol-per-object)-->  N
VGCF Ø≈0.15 µm, L≈10 µm (aspect ≈67);  SuperP aggregate ≈0.2 µm.

  python3 scripts/additives.py            # demo: the two production recipes
"""
from __future__ import annotations
import argparse
import numpy as np

DENS = {'AM': 4.80, 'SE': 1.64, 'VGCF': 2.00, 'SuperP': 1.90, 'PTFE': 2.20}  # g/cm³
PHASE = {'SE': 1, 'AM': 0, 'VGCF': 2, 'SuperP': 3, 'PTFE': 4}                 # save-phase codes
# default geometry (µm)
VGCF_D, VGCF_L = 0.15, 10.0      # fibre diameter, length
SP_D, PTFE_D   = 0.20, 0.30      # carbon-black aggregate, PTFE domain (effective sphere)


def vol_fracs(wt: dict) -> dict:
    """wt% (any subset of AM/SE/VGCF/SuperP/PTFE) → volume fractions (sum 1)."""
    v = {k: wt[k] / DENS[k] for k in wt if wt.get(k, 0) > 0}
    tot = sum(v.values())
    return {k: vv / tot for k, vv in v.items()}


def recipe_counts(wt: dict, solid_vol_um3: float,
                  vgcf_d=VGCF_D, vgcf_l=VGCF_L, sp_d=SP_D, ptfe_d=PTFE_D) -> dict:
    """Number of VGCF fibres / SuperP / PTFE objects for a recipe + solid volume."""
    vf = vol_fracs(wt)
    out = {'vol_fracs': vf}
    v_fib = np.pi * (vgcf_d / 2) ** 2 * vgcf_l                      # µm³ per fibre
    v_sp = np.pi / 6 * sp_d ** 3
    v_pt = np.pi / 6 * ptfe_d ** 3
    for ph, vobj in (('VGCF', v_fib), ('SuperP', v_sp), ('PTFE', v_pt)):
        if vf.get(ph, 0) > 0:
            out[ph] = {'vol_um3': vf[ph] * solid_vol_um3,
                       'n': int(round(vf[ph] * solid_vol_um3 / vobj)),
                       'vol_per_obj_um3': vobj}
    return out


def seed_fibres(n, box_um, dx_um, rng, in_am=None, L=VGCF_L):
    """n random-oriented fibres (SEM-like: long thin rods threading the interstices),
    each a chain of points spaced ~dx along its axis.  Even distribution = uniform
    random centres.  Points falling in AM (in_am) are dropped (fibre bends around)."""
    (Lx, Ly, Lz) = box_um
    k = max(2, int(round(L / (0.7 * dx_um))))                      # points per fibre
    t = np.linspace(-L / 2, L / 2, k)
    pts = []
    for _ in range(n):
        c = np.array([rng.uniform(0, Lx), rng.uniform(0, Ly), rng.uniform(0, Lz)])
        d = rng.normal(size=3); d /= np.linalg.norm(d) + 1e-12     # isotropic direction
        line = c[None, :] + t[:, None] * d[None, :]
        line = line[(line[:, 0] >= 0) & (line[:, 0] < Lx) & (line[:, 1] >= 0)
                    & (line[:, 1] < Ly) & (line[:, 2] >= 0) & (line[:, 2] < Lz)]
        if in_am is not None and len(line):
            line = line[~np.array([in_am(p) for p in line])]
        if len(line):
            pts.append(line)
    return np.concatenate(pts, 0).astype(np.float32) if pts else np.zeros((0, 3), np.float32)


def seed_blobs(n, box_um, rng, in_am=None):
    """n carbon-black / PTFE points, uniform-random (even) through the box, non-AM."""
    (Lx, Ly, Lz) = box_um
    out, tries = [], 0
    while len(out) < n and tries < 50 * n + 100:
        p = np.array([rng.uniform(0, Lx), rng.uniform(0, Ly), rng.uniform(0, Lz)])
        tries += 1
        if in_am is None or not in_am(p):
            out.append(p)
    return np.array(out, np.float32) if out else np.zeros((0, 3), np.float32)


def parse_recipe(s: str) -> dict:
    """'AM:SE:VGCF:PTFE=80:18:1:1' or 'AM:SE:VGCF=72:27:1' → wt dict."""
    keys, vals = s.split('=')
    keys = keys.split(':'); vals = [float(v) for v in vals.split(':')]
    return dict(zip(keys, vals))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recipe', default='', help="e.g. AM:SE:VGCF:PTFE=80:18:1:1")
    ap.add_argument('--rve-um', default='50,50,33', help='box Lx,Ly,Lz µm')
    ap.add_argument('--porosity', type=float, default=0.13)
    ap.add_argument('--dx-um', type=float, default=0.13)
    a = ap.parse_args()
    Lx, Ly, Lz = (float(v) for v in a.rve_um.split(','))
    solid = Lx * Ly * Lz * (1 - a.porosity)
    recipes = [a.recipe] if a.recipe else ['AM:SE:VGCF=72:27:1', 'AM:SE:VGCF:PTFE=80:18:1:1']
    rng = np.random.default_rng(0)
    for r in recipes:
        wt = parse_recipe(r)
        c = recipe_counts(wt, solid)
        print(f'\n=== {r}   (RVE {Lx:g}×{Ly:g}×{Lz:g}µm, solid {solid:,.0f}µm³) ===')
        print('  vol%: ' + '  '.join(f'{k} {100*v:.1f}' for k, v in c['vol_fracs'].items()))
        for ph in ('VGCF', 'SuperP', 'PTFE'):
            if ph in c:
                print(f'  {ph:7s} {c[ph]["n"]:>8,} objects  (vol {c[ph]["vol_um3"]:.0f}µm³)')
        if 'VGCF' in c:
            fib = seed_fibres(c['VGCF']['n'], (Lx, Ly, Lz), a.dx_um, rng)
            print(f'  → VGCF seeded {len(fib):,} material points '
                  f'({len(fib)/max(c["VGCF"]["n"],1):.0f} pts/fibre)')


if __name__ == '__main__':
    main()
