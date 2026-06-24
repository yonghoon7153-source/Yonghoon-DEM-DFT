#!/usr/bin/env python3
"""GPU-free validation of the Stage-1 conductive-additive seeding path.

Runs the SAME recipe→counts→fibre/blob-seed→AM-avoid→phase/cohesion logic that
``mpm3d_compaction.py --add-recipe`` executes, but on a real DEM scaffold
(AM + SE CSV, box units) with no Taichi/GPU — so we can eyeball "did the VGCF /
PTFE get placed sensibly (threading the interstices, bending around the AM,
right counts, right stickiness)" BEFORE paying for the full GPU compaction.

  python3 scripts/validate_additive_seeding.py \
      --am docs/data/real14_am_scaffold.csv --se docs/data/real14_se_scaffold.csv \
      --recipe "AM:SE:VGCF:PTFE=80:18:1:1" --out docs/figures/additive_seed_check.png
"""
from __future__ import annotations
import argparse
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import additives as ad  # noqa: E402

# per-additive (E GPa, ν, σ_y GPa, code, is_fibre, L_µm, cohesion GPa) — mirrors
# mpm3d_compaction.ADD + the per-point coh map {VGCF/SuperP 0, PTFE 0.10}
ADD = {
    'VGCF':   (10.0, 0.30, 2.00, 2, True,  ad.VGCF_L, 0.0),
    'SuperP': (0.50, 0.30, 0.10, 3, False, 0.0,       0.0),
    'PTFE':   (0.30, 0.30, 0.05, 4, True,  ad.PTFE_L, 0.10),
}
SE_COH = 0.02   # SE cold-weld/vdW, auto-on in the additive regime (mpm3d line 137-138)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--am', required=True)
    ap.add_argument('--se', required=True)
    ap.add_argument('--recipe', default='AM:SE:VGCF:PTFE=80:18:1:1')
    ap.add_argument('--um-per-box', type=float, default=1000.0, help='µm per box unit (50µm = 0.05)')
    ap.add_argument('--dx-um', type=float, default=50.0 / 384, help='grid spacing µm (n_grid=384 over 50µm)')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--l-cv', type=float, default=0.4, help='fibre length variation (CV); 0=monodisperse')
    ap.add_argument('--slab-frac', type=float, default=0.10, help='half-thickness of the shown z-slab (frac of bed)')
    ap.add_argument('--out', default='docs/figures/additive_seed_check.png')
    ap.add_argument('--save-npy', default='', help='prefix to dump se.npy/phase.npy for viz_additives')
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    am = np.loadtxt(a.am, delimiter=',')
    se = np.loadtxt(a.se, delimiter=',')
    U = a.um_per_box
    am_xyz = am[:, 1:4] * U
    am_r = am[:, 4] * U
    se_xyz = se[:, 1:4] * U
    se_r = float(np.median(se[:, 4])) * U

    # box in µm = lateral [0,50] × z[min,max]; solid = SE spheres + AM spheres
    lo = np.array([0.0, 0.0, se_xyz[:, 2].min()])
    hi = np.array([am_xyz[:, 0].max(), am_xyz[:, 1].max(), max(am_xyz[:, 2].max(), se_xyz[:, 2].max())])
    box = tuple((hi - lo).tolist())
    am_vol = float((4 / 3 * np.pi * am_r ** 3).sum())
    se_vol = float(len(se) * 4 / 3 * np.pi * se_r ** 3)
    solid_um3 = am_vol + se_vol

    wt = ad.parse_recipe(a.recipe)
    add_wt = ad.additive_wt(wt)                              # additive wt% of the 100% total (AM:SE ignored)
    cnt = ad.recipe_counts_real(add_wt, am_vol, se_vol)      # additive = wt% of the REAL scaffold mass
    print(f'=== {a.recipe} ===')
    print(f'  box {box[0]:.1f}×{box[1]:.1f}×{box[2]:.1f}µm   solid {solid_um3:,.0f}µm³ '
          f'(AM {am_vol:,.0f} + SE {se_vol:,.0f})')
    print(f'  realised electrode (from scaffold): AM {cnt["am_wt_pct"]} / SE {cnt["se_wt_pct"]} wt% + '
          + '  '.join(f'{k} {add_wt[k]}wt%' for k in add_wt))

    # AM-avoidance: nearest-AM test (exact for non-overlapping spheres).  cKDTree
    # nearest centre, reject if within that centre's radius.  Same effect as the
    # rasterised pin_np mask in mpm3d_compaction, but exact (no voxel rounding).
    try:
        from scipy.spatial import cKDTree
        tree = cKDTree(am_xyz - lo)

        def reject_in_am(P):
            d, idx = tree.query(P, k=1)
            return d <= am_r[idx]
    except Exception:                                            # pragma: no cover
        def reject_in_am(P):
            out = np.zeros(len(P), bool)
            for i, p in enumerate(P):
                dd = am_xyz - lo - p
                out[i] = bool((np.einsum('ij,ij->i', dd, dd) <= am_r ** 2).any())
            return out

    # SE base points = real SE centres (1 pt/sphere here — the GPU path voxel-fills,
    # but for the seeding geometry check the centres suffice)
    pts_all = [se_xyz - lo]
    phase_all = [np.full(len(se), ad.PHASE['SE'], np.int8)]
    coh_all = [np.full(len(se), SE_COH, np.float32)]

    for nm, (E, nu, sy, code, is_fib, L_um, coh) in ADD.items():
        if nm not in cnt:
            continue
        nobj = cnt[nm]['n']
        lens = None
        if is_fib:
            raw, lens = ad.seed_fibres(nobj, box, a.dx_um, rng, L=L_um, L_cv=a.l_cv,
                                       return_lengths=True)             # no in_am → seed all, then filter
        else:
            raw = ad.seed_blobs(nobj, box, rng)
        if len(raw) == 0:
            continue
        in_am = reject_in_am(raw)
        kept = raw[~in_am]
        rej = int(in_am.sum())
        pts_all.append(kept)
        phase_all.append(np.full(len(kept), code, np.int8))
        coh_all.append(np.full(len(kept), coh, np.float32))
        lspread = (f'  L {lens.min():.0f}/{lens.mean():.0f}/{lens.max():.0f}µm (min/mean/max, '
                   f'AR {lens.mean() / (ad.VGCF_D if nm == "VGCF" else ad.PTFE_D):.0f})') if lens is not None else ''
        print(f'  {nm:7s} {nobj:>6,} objects → {len(raw):,} pts, {rej:,} in-AM dropped '
              f'({100 * rej / max(len(raw), 1):.1f}%) → {len(kept):,} kept  '
              f'(E={E} σ_y={sy} coh={coh}, phase {code}){lspread}')

    pts = np.concatenate(pts_all).astype(np.float32)
    phase = np.concatenate(phase_all)
    coh = np.concatenate(coh_all)
    print(f'  TOTAL {len(pts):,} material points  | phase counts: '
          + '  '.join(f'{nm}={int((phase == c).sum()):,}'
                      for nm, c in (('SE', 1), ('VGCF', 2), ('SuperP', 3), ('PTFE', 4)) if (phase == c).any()))
    print(f'  cohesion: SE={SE_COH} '
          + '  '.join(f'{nm}={ADD[nm][6]}' for nm in ('VGCF', 'SuperP', 'PTFE') if (phase == ADD[nm][3]).any())
          + '  → PTFE binder is %g× the SE stickiness' % (ADD['PTFE'][6] / SE_COH if (phase == 4).any() else 0))

    if a.save_npy:
        np.save(a.save_npy + '_se.npy', pts)
        np.save(a.save_npy + '_phase.npy', phase)
        print(f'  saved {a.save_npy}_se.npy / _phase.npy')

    _render(a.out, am_xyz - lo, am_r, pts, phase, box, a.slab_frac)


def _render(out, am_xyz, am_r, pts, phase, box, slab_frac=0.10):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    # z-slab in the middle for clarity
    zc = box[2] * 0.5
    zlo, zhi = zc - box[2] * slab_frac, zc + box[2] * slab_frac
    fig, ax = plt.subplots(figsize=(8.4, 8))
    for (x, y, z), r in zip(am_xyz, am_r):
        if zlo - r <= z <= zhi + r:
            ax.add_patch(Circle((x, y), r, fc='#5a6b7a', ec='#33414d', alpha=0.55, zorder=1))
    m = (pts[:, 2] >= zlo) & (pts[:, 2] <= zhi)
    COL = {1: ('#cfcfcf', 'SE', 2, 1.5), 2: ('#111111', 'VGCF', 5, 4),
           3: ('#777777', 'Super P', 7, 3), 4: ('#e08214', 'PTFE', 6, 5)}
    for code, (c, lab, ms, zo) in COL.items():
        sel = m & (phase == code)
        if sel.any():
            ax.scatter(pts[sel, 0], pts[sel, 1], s=ms, c=c, alpha=0.75,
                       label=f'{lab} ({int((phase == code).sum()):,} total)', zorder=zo, linewidths=0)
    ax.set_xlim(0, box[0]); ax.set_ylim(0, box[1]); ax.set_aspect('equal')
    ax.set_xlabel('x (µm)'); ax.set_ylabel('y (µm)')
    ax.set_title('Stage-1 additive seeding check (GPU-free) — real DEM scaffold\n'
                 f'z-slab {zlo:.1f}–{zhi:.1f}µm · AM skeleton + carbon threading interstices', fontsize=10)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    fig.tight_layout(); fig.savefig(out, dpi=135)
    print(f'  saved {out}')


if __name__ == '__main__':
    main()
