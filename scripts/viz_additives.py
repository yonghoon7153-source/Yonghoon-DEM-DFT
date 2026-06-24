#!/usr/bin/env python3
"""Visualise the Stage-1 additive morphology: a top-down (x–y) slab of the MPM
output coloured by phase — AM skeleton + SE + VGCF fibres + Super P + PTFE — to
eyeball "where the carbon sits" vs the SEM.

Real run:  --se se_dump.npy --phase phase.npy [--am am_scaffold.csv] [--lateral-box B]
Preview :  --demo   (synthesise a few AM + VGCF fibres + Super P, render the look)

  python3 scripts/viz_additives.py --demo --out docs/figures/additives_preview.png
"""
import argparse
import numpy as np

COL = {1: ('#bdbdbd', 'SE', 1), 2: ('#111111', 'VGCF', 6), 3: ('#777777', 'Super P', 8),
       4: ('#e08214', 'PTFE', 4)}   # phase → (colour, label, marker size)


def _demo(rng, box=50.0):
    """AM_P(6µm)+AM_S(2µm) skeleton + VGCF fibres threading the gaps + Super P dots."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import additives as ad
    am = []                                                  # (x,y,z,r)
    for r, k in ((6.0, 9), (2.0, 40)):
        for _ in range(k):
            am.append((rng.uniform(r, box - r), rng.uniform(r, box - r),
                       rng.uniform(r, box - r), r))
    am = np.array(am)

    def in_am(p):                                            # reject points inside an AM sphere
        d = am[:, :3] - p
        return bool((np.einsum('ij,ij->i', d, d) <= am[:, 3] ** 2).any())
    fib = ad.seed_fibres(70, (box, box, box), 0.3, rng, L=10.0, in_am=in_am)
    sp = ad.seed_blobs(300, (box, box, box), rng, in_am=in_am)
    return am, fib, sp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--se', default=''); ap.add_argument('--phase', default='')
    ap.add_argument('--am', default=''); ap.add_argument('--lateral-box', type=float, default=50.0)
    ap.add_argument('--demo', action='store_true')
    ap.add_argument('--slab', default='0.45,0.55', help='z-slab fraction to show (clarity)')
    ap.add_argument('--out', default='docs/figures/additives_preview.png')
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(8, 8))

    if a.demo:
        am, fib, sp = _demo(rng)
        box = 50.0
        for x, y, z, r in am:
            ax.add_patch(Circle((x, y), r, fc='#5a6b7a', ec='#33414d', alpha=0.85, zorder=1))
        ax.scatter(sp[:, 0], sp[:, 1], s=8, c='#777777', alpha=0.6, zorder=2, label='Super P')
        ax.scatter(fib[:, 0], fib[:, 1], s=5, c='#111111', zorder=3, label='VGCF')
        ax.set_title('Stage-1 additive morphology — PREVIEW (synthetic)\n'
                     'AM skeleton + VGCF fibres threading interstices + Super P', fontsize=11)
    else:
        se = np.load(a.se); ph = np.load(a.phase)
        box = a.lateral_box
        # the MPM se.npy is in box units [0,1] lateral; map to µm if a lateral-box given
        sx, sy, sz = se[:, 0], se[:, 1], se[:, 2]
        zlo, zhi = (float(v) for v in a.slab.split(','))
        m = (sz >= sz.min() + zlo * (sz.max() - sz.min())) & (sz <= sz.min() + zhi * (sz.max() - sz.min()))
        um = box / (sx.max() - sx.min() + 1e-9)
        if a.am:
            amr = np.loadtxt(a.am, delimiter=',')
            for row in amr:
                ax.add_patch(Circle((row[1] * 1e6 if row[1] < 1 else row[1], row[2] * 1e6 if row[2] < 1 else row[2]),
                                    row[4] * 1e6 if row[4] < 1 else row[4], fc='#5a6b7a', ec='none', alpha=0.5, zorder=1))
        for code, (c, lab, ms) in COL.items():
            sel = m & (ph == code)
            if sel.any():
                ax.scatter((sx[sel] - sx.min()) * um, (sy[sel] - sy.min()) * um, s=ms, c=c,
                           alpha=0.7, label=f'{lab} ({int(sel.sum())})', zorder=COL[code][2])
        ax.set_title(f'Stage-1 additive morphology — {a.se}\nz-slab {a.slab} (top-down x–y)', fontsize=10)

    ax.set_xlim(0, box); ax.set_ylim(0, box); ax.set_aspect('equal')
    ax.set_xlabel('x (µm)'); ax.set_ylabel('y (µm)'); ax.legend(loc='upper right', fontsize=9)
    import os
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    fig.tight_layout(); fig.savefig(a.out, dpi=130)
    print(f'saved {a.out}')


if __name__ == '__main__':
    main()
