#!/usr/bin/env python3
"""SDCP mixing-morphology PREVIEW — ball-mill / thinky / hand-mix side by side.

Seeds the SDCP particles on the real14 DEM scaffold with the SAME code path the GPU
run uses (additives.seed_sdcp + ADDITIVE_PROCESS rows + recipe_counts_real), so what
this shows IS what mpm3d_compaction starts from — no divergence risk by construction.
NO compaction happens here (CPU, numpy-only): this is the SEEDED state, which is
exactly where the mixing physics lives:
  ball-mill / Thinky (high shear): the dry process MILLS the as-made powder →
      0.2-0.5 µm SINGLES (manuscript Fig S3), surface_frac=0.5 AM-anchored
      (sulfonate + ordered-mixing decoration) + rest dispersed in-pore.
  hand-mix (low shear): NO milling energy → the AS-MADE ~3 µm agglomerates
      (manuscript Fig S2) survive; ALL SDCP seeds as ~3 µm clusters
      (n_agg = 0.64·(3/0.3)³ ≈ 640 primaries each), 0.3 anchored (draped caps
      on NCM — weaker decoration: adhesion/weight fades ~×100 at 3 µm guest size).

Usage:
  python3 scripts/preview_sdcp_mixing.py [--wt 1.0] [--seed 0]
      [--out docs/figures/sdcp_mixing_preview.png]
Prints per-mixing stats (objects, points, realised AM-anchored share, SDCP→AM
nearest-surface distance quartiles) and writes a 2×3 panel figure.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import additives as ad                                         # noqa: E402

try:
    from scipy.spatial import cKDTree
except ImportError:                                            # pragma: no cover
    sys.exit('scipy required (pip install scipy)')

ROOT = Path(__file__).resolve().parents[1]
AM_CSV = ROOT / 'docs/data/real14_am_scaffold.csv'
SE_CSV = ROOT / 'docs/data/real14_se_scaffold.csv'
MIXINGS = ('ballmill', 'thinky', 'handmix')


def load_scaffold():
    """real14 scaffold CSVs (LIGGGHTS box units ×1000 → µm) → (AM C,R,type), SE C."""
    am = np.loadtxt(AM_CSV, delimiter=',', comments='#')
    se = np.loadtxt(SE_CSV, delimiter=',', comments='#')
    am_t = am[:, 0].astype(int)
    am_c = am[:, 1:4] * 1000.0
    am_r = am[:, 4] * 1000.0
    se_c = se[:, 1:4] * 1000.0
    se_r = float(se[0, 4]) * 1000.0
    return am_c, am_r, am_t, se_c, se_r


def main():
    pa = argparse.ArgumentParser()
    pa.add_argument('--wt', type=float, default=1.0, help='SDCP wt%% of the electrode (default 1.0)')
    pa.add_argument('--seed', type=int, default=0)
    pa.add_argument('--out', default=str(ROOT / 'docs/figures/sdcp_mixing_preview.png'))
    args = pa.parse_args()

    am_c, am_r, am_t, se_c, se_r = load_scaffold()
    box = (50.0, 50.0, float((am_c[:, 2] + am_r).max()))       # LIGGGHTS cell: lateral 0..50 µm PERIODIC
    #   (CSV header) — seed strictly inside it; out-of-cell anchored pts DROP (fibre convention, same as
    #   the mpm3d run: no wall curtains, volume re-pinned by add_pvs downstream).  z = bed top.

    # recipe → particle count, EXACTLY as mpm3d does it (scaffold masses, not a hardcoded ratio)
    am_um3 = float((4.0 / 3.0 * np.pi * am_r ** 3).sum())
    se_um3 = float(len(se_c) * 4.0 / 3.0 * np.pi * se_r ** 3)
    cnt = ad.recipe_counts_real({'SDCP': args.wt}, am_um3, se_um3)
    n = cnt['SDCP']['n']
    print(f"scaffold: AM {len(am_c)} spheres ({am_um3:,.0f} µm³) + SE {len(se_c)} × Ø{2*se_r:.1f}µm "
          f"({se_um3:,.0f} µm³); box {box[0]:.0f}×{box[1]:.0f}×{box[2]:.1f} µm")
    print(f"SDCP {args.wt} wt% → {cnt['SDCP']['vol_um3']:,.0f} µm³ = {cnt['SDCP']['vol_pct_of_solid']} vol% "
          f"of solid → n = {n:,} primaries (Ø {ad.SDCP_D} µm)")

    # EXACT in_am / surface distance: one KDTree per radius CLASS (real14: r=6 AM_P, r=2 AM_S).
    # A point inside any class-r sphere is < r from its NEAREST same-class centre (k=1 exact) —
    # avoids the k-nearest-by-centre false negatives a mixed-radius single tree has.
    classes = [(float(r), cKDTree(am_c[am_r == r])) for r in np.unique(am_r)]

    def in_am(q):
        q = np.asarray(q, np.float64)
        return any(t.query(q)[0] < r for r, t in classes)

    def dist_surf(P):
        """min over classes of (dist to nearest same-class centre − r); negative = inside."""
        return np.min(np.column_stack([t.query(np.asarray(P, np.float64))[0] - r
                                       for r, t in classes]), axis=1)

    results = {}
    for mix in MIXINGS:
        row = ad.additive_process('SDCP', mix)
        rng = np.random.default_rng(args.seed)                 # same seed → comparable panels
        pts, ids, info = ad.seed_sdcp(n, box, 0.13, rng, am=(am_c, am_r), in_am=in_am,
                                      surface_frac=float(row.get('surface_frac', 0.5)),
                                      clump=int(row.get('clump', 1)),
                                      agg_d=float(row.get('agg_d', 0.0)), d=ad.SDCP_D,
                                      return_ids=True, return_info=True)
        dsurf = dist_surf(pts)                                 # SDCP → nearest AM SURFACE (µm), exact
        near = float(np.mean(dsurf < ad.SDCP_D))               # near-AM(<1 particle Ø) — includes INCIDENTAL
        q25, q50, q75 = np.percentile(dsurf, (25, 50, 75))     #   proximity of bulk pts, ≠ the seeded split
        results[mix] = dict(pts=pts, ids=ids, dsurf=dsurf, row=row, near=near, info=info)
        print(f"[{mix:8s}] {row.get('morph', '')}\n"
              f"           → {len(pts):,} pts / {len(np.unique(ids)):,} objects | seeded anchored share "
              f"{100*info['realized_anchor_frac']:.1f}% (nominal sf={info['surface_frac_nominal']}) | "
              f"near-AM(<{ad.SDCP_D}µm incl. incidental) {100*near:.1f}% | d_surf q25/50/75 = "
              f"{q25:.2f}/{q50:.2f}/{q75:.2f} µm | survival {100*info['survival']:.1f}%"
              + (f" | agg Ø{row['agg_d']}µm × {info.get('n_agg_design', 0)} primaries "
                 f"(pack {info.get('agg_pack_assumed', 0)} ASSUMED §F1)"
                 if row.get('agg_d', 0) > 0 else ""))

    # ── figure: row 1 = full x-z slice, row 2 = zoom on the biggest AM_P in the slab ──
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    y0, half = box[1] / 2.0, 0.8                               # slab |y−y0| < 0.8 µm
    fig, axes = plt.subplots(2, 3, figsize=(16.5, 10.5), dpi=150)
    big = np.argmax(np.where(np.abs(am_c[:, 1] - y0) < am_r * 0.7, am_r, 0))
    zx, zz, zw = am_c[big, 0], am_c[big, 2], 8.0               # zoom window centre + half-width
    ttl = {'ballmill': 'ball-mill — milled 0.2-0.5µm singles (S3)',
           'thinky': 'thinky — milled singles (S3, ≡ball-mill)',
           'handmix': 'hand-mix — as-made ~3µm agglomerates (S2)'}
    for col, mix in enumerate(MIXINGS):
        pts = results[mix]['pts']
        sl = np.abs(pts[:, 1] - y0) < half
        se_sl = np.abs(se_c[:, 1] - y0) < half
        for r_i, (ax, w) in enumerate(((axes[0, col], None), (axes[1, col], zw))):
            for c, r, t in zip(am_c, am_r, am_t):
                dy = abs(c[1] - y0)
                if dy < r:
                    rs = np.sqrt(r * r - dy * dy)
                    ax.add_patch(Circle((c[0], c[2]), rs,                     # AM_P darker, AM_S lighter
                                        facecolor=('#c9c9c9' if t == 1 else '#e2e2e2'),
                                        edgecolor='#8a8a8a', lw=0.6, zorder=1))
            ax.scatter(se_c[se_sl, 0], se_c[se_sl, 2], s=2.5, c='#9ecae1', alpha=0.35,
                       lw=0, zorder=2, label='SE (Ø1µm)')
            ax.scatter(pts[sl, 0], pts[sl, 2], s=(2.2 if w is None else 6.5), c='crimson',
                       lw=0, zorder=3, label='SDCP')
            if w is None:
                ax.set_xlim(0, box[0]); ax.set_ylim(0, box[2])
                ax.set_title(ttl[mix], fontsize=11)
                st = results[mix]
                ax.text(0.02, 0.98, f"{len(pts):,} pts / {len(np.unique(st['ids'])):,} obj\n"
                                    f"seeded anchored {100*st['info']['realized_anchor_frac']:.0f}% "
                                    f"(sf={st['row']['surface_frac']})",
                        transform=ax.transAxes, va='top', fontsize=8.5,
                        bbox=dict(fc='white', alpha=0.8, ec='none'))
            else:
                ax.set_xlim(zx - w, zx + w); ax.set_ylim(max(zz - w, 0), zz + w)
                ax.set_title(f'zoom {2*w:.0f}µm @ AM_P', fontsize=9)
            ax.set_aspect('equal'); ax.set_xlabel('x (µm)', fontsize=8)
            if col == 0:
                ax.set_ylabel('z (µm)', fontsize=8)
            ax.tick_params(labelsize=7)
    axes[0, 0].legend(loc='lower left', fontsize=7, framealpha=0.85)
    fig.suptitle(f'SDCP {args.wt} wt% seeding on real14 scaffold — mixing morphology '
                 f'(x-z slab |y−{y0:.0f}µm|<{half}µm; SEEDED state = MPM run input; seed {args.seed})',
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print(f"figure → {out}")


if __name__ == '__main__':
    main()
