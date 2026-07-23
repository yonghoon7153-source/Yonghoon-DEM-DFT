#!/usr/bin/env python3
"""Visualise the MPM scaffold SE morphology from a 2D (x-z) slab of the compacted
composite.  Two panels:
  • FULL  — a phase raster (AM skeleton / SE / void) overview, SE-AM contact in red.
  • ZOOM  — the SE rendered as its actual MATERIAL POINTS (a scatter), so you see the
            real plastic SE *shape* (deformed grains), not a filled blob.  Give
            --se-dump (the seed-centre CSV) to colour each SE point by its grain →
            the individual SE grains separate visually (like the 2D-champion morphology).
            AM is drawn as faint outlines only (—hide-am to drop it entirely).

The MPM SE actually deforms/flows around the rigid real AM (the DEM cannot), so this
slab IS the SE plastic morphology — the MPM's unique output.

  python3 scripts/viz_mpm_morphology.py --se se_dump.npy --scaffold am_scaffold.csv \
      --zoom-w 10 --se-dump se_scaffold.csv --out morph_zoom.png
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                       # noqa: E402
import matplotlib.patches as mpatches                 # noqa: E402
from matplotlib.colors import ListedColormap, BoundaryNorm  # noqa: E402

# scaffold box geometry (must match mpm3d_compaction.py --am-scaffold)
SW = (0.04, 0.96); FLOOR = 0.05
WIDTH = SW[1] - SW[0]; SCL = WIDTH / 0.05              # box units per LIGGGHTS unit
UM_BOX = 1000.0 / SCL                                  # µm per box unit

# phase colours: void / AM_P / AM_S / SE / SE-AM contact
COLORS = ['#ffffff', '#2b2f3a', '#9aa0ad', '#f4d35e', '#ef4444']
_NORM = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], len(COLORS))
_CMAP = ListedColormap(COLORS)


def build_lab(x0, x1, z0, z1, nx, sx, sz, am_t, am_c, am_r, y, se_min_count, denoise, contact_um):
    """Phase label raster (0 void / 1 AM_P / 2 AM_S / 3 SE / 4 SE-AM contact) for the
    overview panel.  contact_um = SE within this µm of AM → red (the contact band)."""
    nz = max(2, int(round(nx * (z1 - z0) / (x1 - x0))))
    X, Z = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(z0, z1, nz))
    lab = np.zeros((nz, nx), np.int8)
    inw = (sx >= x0) & (sx < x1) & (sz >= z0) & (sz < z1)
    se_mask = np.zeros((nz, nx), bool)
    if inw.any():
        ix = np.clip(((sx[inw] - x0) / (x1 - x0) * (nx - 1)).astype(int), 0, nx - 1)
        iz = np.clip(((sz[inw] - z0) / (z1 - z0) * (nz - 1)).astype(int), 0, nz - 1)
        cnt = np.zeros((nz, nx), np.int32); np.add.at(cnt, (iz, ix), 1)
        se_mask = cnt >= se_min_count
    if denoise > 0:
        from scipy import ndimage as ndi
        se_mask = ndi.binary_closing(se_mask, iterations=denoise)
        se_mask = ndi.binary_opening(se_mask, iterations=denoise)
    lab[se_mask] = 3
    am_mask = np.zeros((nz, nx), bool)
    for i in range(len(am_r)):
        cx, cy, cz = am_c[i]; rr = am_r[i]; d = y - cy
        if abs(d) >= rr:
            continue
        reff = np.sqrt(rr * rr - d * d)
        msk = (X - cx) ** 2 + (Z - cz) ** 2 <= reff * reff
        lab[msk] = am_t[i]; am_mask |= msk
    if contact_um > 0:
        um_per_px = (x1 - x0) * UM_BOX / nx
        it = max(1, int(round(contact_um / max(um_per_px, 1e-9))))
        try:
            from scipy import ndimage as ndi
            lab[(lab == 3) & ndi.binary_dilation(am_mask, iterations=it)] = 4
        except Exception:
            pass
    return lab


def densest_center(sx, sz, x0, x1, z0, z1, w_box, weights=None):
    """Box-unit centre of the densest w_box window — weighted by `weights` if given (e.g.
    plastic strain → centre on the HIGH-STRAIN region; else by SE point density)."""
    if not len(sx) or (weights is not None and float(np.nansum(weights)) <= 0):
        weights = None
    if not len(sx):
        return (x0 + x1) / 2, (z0 + z1) / 2
    H, xe, ze = np.histogram2d(sx, sz, bins=40, range=[[x0, x1], [z0, z1]], weights=weights)
    try:
        from scipy import ndimage as ndi
        kx = max(1, int(round(w_box / ((x1 - x0) / 40))))
        H = ndi.uniform_filter(H, size=kx, mode='constant')
    except Exception:
        pass
    i, j = np.unravel_index(int(np.argmax(H)), H.shape)
    return 0.5 * (xe[i] + xe[i + 1]), 0.5 * (ze[j] + ze[j + 1])


def scatter_phase(ax, px, pz, strain, ph, vmax, ptsize, am_color='#9aa0ad'):
    """Composite scatter: AM points (ph==0) grey, SE points (ph==1) strain-coloured (afmhot)."""
    am = ph == 0; se = ph == 1
    if am.any():
        ax.scatter(px[am], pz[am], c=am_color, s=ptsize, edgecolors='none')
    sc = None
    if se.any():
        sc = ax.scatter(px[se], pz[se], c=strain[se], s=ptsize, cmap='afmhot',
                        vmin=0.0, vmax=vmax, edgecolors='none')
    return sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--se', required=True, help='SE point cloud npy ([n,3], box units) from --save-se')
    ap.add_argument('--scaffold', default='', help='AM scaffold CSV (type,x,y,z,r LIGGGHTS units); '
                    'omit for an SE-only loose→dense demo (no AM)')
    ap.add_argument('--y', type=float, default=0.5, help='slab centre (box units, 0.04..0.96)')
    ap.add_argument('--slab', type=float, default=0.0, help='slab half-thickness (box units; 0=auto≈1.5 r_se)')
    ap.add_argument('--nx', type=int, default=220, help='full-panel raster columns')
    ap.add_argument('--se-min-count', type=int, default=1, help='full panel: pixel is SE if ≥N points')
    ap.add_argument('--denoise', type=int, default=0, help='full panel: close+open iters on SE mask (scipy)')
    ap.add_argument('--contact-um', type=float, default=0.26, help='full panel: SE within this µm of AM → red')
    ap.add_argument('--zoom-w', type=float, default=10.0,
                    help='zoom window width (µm) — the SE-shape scatter panel; smaller = more zoom (0=full only)')
    ap.add_argument('--zoom-at', default='', help='zoom centre "cx,cz" µm (default: densest SE)')
    ap.add_argument('--se-dump', default='', help='seed-centre CSV (se_scaffold.csv) → colour SE points by grain')
    ap.add_argument('--dg', default='', help='accumulated plastic strain npy (mpm3d --save-dg) → colour the SE '
                    'points by Σdg (afmhot, like the champion morphology); takes priority over grain colour')
    ap.add_argument('--eps', default='', help='accumulated TOTAL strain npy (mpm3d --save-eps) — deformation vs the '
                    'seed sphere (incl elastic); PREFERRED over --dg (use for the loose→dense demo)')
    ap.add_argument('--dg-vmax', type=float, default=0.0,
                    help='fix the Σdg colour max (0=auto: 98th pct of non-zero strain) — tune contrast')
    ap.add_argument('--hide-am', action='store_true', help='do not draw AM in the zoom (SE shape only)')
    ap.add_argument('--pt-size', type=float, default=6.0, help='zoom scatter point size')
    ap.add_argument('--phase', default='', help='per-point phase npy (mpm3d --save-phase, 1=SE/0=AM) → composite '
                    'view: AM points grey, SE points strain-coloured (for --material mix runs)')
    ap.add_argument('--out', default='mpm_morphology.png')
    a = ap.parse_args()

    se = np.load(a.se).astype(np.float64)                       # [n,3] box units
    if a.scaffold:
        am = np.loadtxt(a.scaffold, delimiter=',')
        am_t = am[:, 0].astype(int)
        am_c = np.column_stack([SW[0] + am[:, 1] * SCL, SW[0] + am[:, 2] * SCL, FLOOR + am[:, 3] * SCL])
        am_r = am[:, 4] * SCL
    else:                                                       # SE-only loose→dense demo (no AM)
        am_t = np.zeros(0, int); am_c = np.zeros((0, 3)); am_r = np.zeros(0)
    r_se = 0.0005 * SCL
    half = a.slab if a.slab > 0 else 1.5 * r_se
    z_top = (float((am_c[:, 2] + am_r).max()) if len(am_r) else float(se[:, 2].max())) + 0.01
    x0, x1, z0, z1 = SW[0], SW[1], FLOOR, z_top

    m = np.abs(se[:, 1] - a.y) < half
    slab = se[m]; sx, sz = slab[:, 0], slab[:, 2]
    strain_npy = a.eps or a.dg                                  # TOTAL (vs seed) preferred over PLASTIC
    field_label = 'total strain ε (vs seed)' if a.eps else 'plastic strain Σdg'
    dg_slab = np.load(strain_npy).astype(np.float64)[m] if strain_npy else None
    phase_slab = np.load(a.phase).astype(np.int8)[m] if a.phase else None  # 1=SE, 0=AM (composite)
    dg_vmax = 1.0
    if dg_slab is not None:
        pos = dg_slab[dg_slab > 0]
        dg_vmax = a.dg_vmax if a.dg_vmax > 0 else (float(np.percentile(pos, 98)) if len(pos) else 1.0)
        print(f'  {field_label}: mean {dg_slab.mean():.4f}  max {dg_slab.max():.3f}  '
              f'>0 in {100.0*(dg_slab>0).mean():.1f}% of slab pts  → colour vmax={dg_vmax:.3f}')

    lab = build_lab(x0, x1, z0, z1, a.nx, sx, sz, am_t, am_c, am_r, a.y,
                    a.se_min_count, a.denoise, a.contact_um)
    por = 100.0 * (lab == 0).mean(); se_f = 100.0 * ((lab == 3) | (lab == 4)).mean()
    am_f = 100.0 * ((lab == 1) | (lab == 2)).mean(); ct_f = 100.0 * (lab == 4).mean()
    ext_full = [0, (x1 - x0) * UM_BOX, 0, (z1 - z0) * UM_BOX]

    if a.zoom_w <= 0:
        fig, ax = plt.subplots(figsize=(9, 9 * (z1 - z0) / (x1 - x0) + 0.6))
        ax.imshow(lab, origin='lower', cmap=_CMAP, norm=_NORM, interpolation='nearest',
                  extent=ext_full, aspect='equal')
        ax.set_xlabel('x (µm)'); ax.set_ylabel('z (µm, compaction ↓)')
        ax.set_title(f'MPM SE plastic morphology — x-z slice @ y={a.y:.2f}\n'
                     f'AM {am_f:.0f}% · SE {se_f:.0f}% · void {por:.0f}% · contact {ct_f:.1f}% (red)', fontsize=10)
        plt.tight_layout(); plt.savefig(a.out, dpi=150)
        print(f'saved {a.out}   AM {am_f:.1f}% / SE {se_f:.1f}% / void {por:.1f}% / contact {ct_f:.1f}%')
        return

    # ── zoom window (box units) ──────────────────────────────────────────────
    hw = (a.zoom_w / UM_BOX) / 2.0
    if a.zoom_at:
        cxu, czu = [float(v) for v in a.zoom_at.split(',')]
        cx_b, cz_b = x0 + cxu / UM_BOX, z0 + czu / UM_BOX
    else:
        cx_b, cz_b = densest_center(sx, sz, x0, x1, z0, z1, 2 * hw, weights=dg_slab)
    zx0, zx1, zz0, zz1 = cx_b - hw, cx_b + hw, cz_b - hw, cz_b + hw
    if zx0 < x0: zx0, zx1 = x0, x0 + 2 * hw           # noqa: E701
    if zx1 > x1: zx0, zx1 = x1 - 2 * hw, x1
    if zz0 < z0: zz0, zz1 = z0, z0 + 2 * hw
    if zz1 > z1: zz0, zz1 = z1 - 2 * hw, z1
    zx0, zz0 = max(zx0, x0), max(zz0, z0)

    win = (sx >= zx0) & (sx < zx1) & (sz >= zz0) & (sz < zz1)
    Pw = slab[win]                                              # SE material points in the zoom
    xu = (Pw[:, 0] - zx0) * UM_BOX; zu = (Pw[:, 2] - zz0) * UM_BOX

    # colour priority: plastic strain Σdg (--dg, the continuous field — like the champion
    # image, smooth dark-core→bright-rim) > grain (--se-dump, blocky on the gridded points)
    # > flat SE.  (the gridded look of grain-colour is the voxel-seeded SE lattice.)
    dgw, pc = None, COLORS[3]
    if dg_slab is not None and len(Pw):
        dgw = dg_slab[win]
    elif a.se_dump and len(Pw):
        from scipy.spatial import cKDTree
        sd = np.loadtxt(a.se_dump, delimiter=',')
        seeds = np.column_stack([SW[0] + sd[:, 1] * SCL, SW[0] + sd[:, 2] * SCL, FLOOR + sd[:, 3] * SCL])
        gid = cKDTree(seeds).query(Pw)[1]
        pc = plt.cm.hsv((gid * 0.6180339887) % 1.0)            # golden-ratio hue → adjacent grains differ

    fig, (axf, axz) = plt.subplots(1, 2, figsize=(16, 7.6))
    if phase_slab is not None and dg_slab is not None:          # composite: full panel = AM grey + SE strain scatter
        #   ★그레인 색 모드(--se-dump, strain 없음)에선 dg_slab=None → full 패널은 phase 래스터로 폴백(아래 else)
        nfull = min(150000, len(slab))
        fi = (np.random.default_rng(1).choice(len(slab), nfull, replace=False)
              if len(slab) > nfull else np.arange(len(slab)))
        axf.set_facecolor('white')
        scatter_phase(axf, (sx[fi] - x0) * UM_BOX, (sz[fi] - z0) * UM_BOX,
                      dg_slab[fi], phase_slab[fi], dg_vmax, max(0.5, a.pt_size * 0.25))
        axf.set_xlim(0, (x1 - x0) * UM_BOX); axf.set_ylim(0, (z1 - z0) * UM_BOX); axf.set_aspect('equal')
    else:
        axf.imshow(lab, origin='lower', cmap=_CMAP, norm=_NORM, interpolation='nearest',
                   extent=ext_full, aspect='equal')
    axf.add_patch(mpatches.Rectangle(((zx0 - x0) * UM_BOX, (zz0 - z0) * UM_BOX),
                  (zx1 - zx0) * UM_BOX, (zz1 - zz0) * UM_BOX, fill=False, ec='#06b6d4', lw=2))
    axf.set_xlabel('x (µm)'); axf.set_ylabel('z (µm, compaction ↓)')
    axf.set_title(f'full — AM {am_f:.0f}% · SE {se_f:.0f}% · void {por:.0f}% · contact {ct_f:.1f}% (red)', fontsize=10)

    axz.set_facecolor('white')
    if phase_slab is not None and dgw is not None:             # composite: AM grey + SE strain
        sc = scatter_phase(axz, xu, zu, dgw, phase_slab[win], dg_vmax, a.pt_size)
        if sc is not None:
            fig.colorbar(sc, ax=axz, fraction=0.046, pad=0.04, label=field_label)
        ctag = f'AM grey + SE {field_label}'
    else:
        if not a.hide_am:                                      # faint AM outlines (context only)
            for i in range(len(am_r)):
                cx, cy, cz = am_c[i]; rr = am_r[i]; d = a.y - cy
                if abs(d) >= rr:
                    continue
                reff = np.sqrt(rr * rr - d * d)
                axz.add_patch(plt.Circle(((cx - zx0) * UM_BOX, (cz - zz0) * UM_BOX), reff * UM_BOX,
                              fill=False, ec='#c7ccd6', lw=1.0, ls='--'))
        if dgw is not None:
            sc = axz.scatter(xu, zu, c=dgw, s=a.pt_size, cmap='afmhot', vmin=0.0, vmax=dg_vmax, edgecolors='none')
            fig.colorbar(sc, ax=axz, fraction=0.046, pad=0.04, label=field_label)
            ctag = f'{field_label} (vmax {dg_vmax:.3f})'
        else:
            axz.scatter(xu, zu, c=pc, s=a.pt_size, edgecolors='none')
            ctag = 'grain-coloured' if a.se_dump else 'SE points'
    axz.set_xlim(0, (zx1 - zx0) * UM_BOX); axz.set_ylim(0, (zz1 - zz0) * UM_BOX)
    axz.set_aspect('equal'); axz.set_xlabel('x (µm)'); axz.set_ylabel('z (µm, compaction ↓)')
    axz.set_title(f'zoom ({a.zoom_w:.0f} µm) — SE material points ({ctag}) · {len(Pw):,} pts', fontsize=10)
    fig.suptitle(f'MPM SE plastic morphology — x-z slab @ y={a.y:.2f}', fontsize=11)

    plt.tight_layout(); plt.savefig(a.out, dpi=150)
    print(f'saved {a.out}   zoom {a.zoom_w:.0f}µm @ ({(cx_b-x0)*UM_BOX:.1f},{(cz_b-z0)*UM_BOX:.1f})µm · '
          f'{len(Pw):,} SE pts · AM {am_f:.1f}%/SE {se_f:.1f}%/void {por:.1f}%')


if __name__ == '__main__':
    main()
