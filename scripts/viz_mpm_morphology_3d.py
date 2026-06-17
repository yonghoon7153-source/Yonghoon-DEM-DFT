#!/usr/bin/env python3
"""3D view of the MPM scaffold morphology: the fixed AM skeleton + the
plastically-conformed SE that flowed into the interstices, with an optional
corner cutaway so you can see INSIDE the bed.  This is the MPM's unique 3D
output — a rigid-sphere DEM cannot deform the SE, so the void-filling SE shape
only exists here.

Two engines:
  • mpl    — static PNG (AM = shaded spheres, SE = point cloud), multi-cut.
             Works with the base setup (matplotlib only).  matplotlib 3D has no
             true z-buffer, so heavy beds look busy — use --cut to thin it.
  • plotly — interactive HTML you spin in a browser (proper WebGL occlusion).
             Best for exploring; needs `pip install plotly`.

  # real plastic SE (run mpm3d_compaction --save-se se384.npy first):
  python3 scripts/viz_mpm_morphology_3d.py --se se384.npy \
      --scaffold docs/data/real14_am_scaffold.csv --cut quarter --out morph3d.png

  # interactive:
  python3 scripts/viz_mpm_morphology_3d.py --se se384.npy --engine plotly \
      --scaffold docs/data/real14_am_scaffold.csv --out morph3d.html

  # quick GEOMETRY proxy (no MPM run — cell-fills the interstices to --se-frac;
  # shows the packing, NOT the plastic flow):
  python3 scripts/viz_mpm_morphology_3d.py --se-proxy --se-frac 0.27 \
      --scaffold docs/data/real14_am_scaffold.csv --out morph3d_proxy.png
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                         # noqa: E402

# scaffold box geometry (must match mpm3d_compaction.py --am-scaffold)
SW = (0.04, 0.96); FLOOR = 0.05
WIDTH = SW[1] - SW[0]; SCL = WIDTH / 0.05               # box units per LIGGGHTS unit
UM_BOX = 1000.0 / SCL                                   # µm per box unit
COL = {1: '#2b2f3a', 2: '#9aa0ad', 3: '#f4d35e'}       # AM_P / AM_S / SE


def load_am(path):
    am = np.loadtxt(path, delimiter=',')
    t = am[:, 0].astype(int)
    c = np.column_stack([SW[0] + am[:, 1] * SCL,
                         SW[0] + am[:, 2] * SCL,
                         FLOOR + am[:, 3] * SCL])
    r = am[:, 4] * SCL
    return t, c, r


def proxy_se(c, r, se_frac, top, n, rng):
    """Cell-fill the interstitial (non-AM) cells to `se_frac` → SE cell-centre
    points (box units).  GEOMETRY proxy only — this is the un-compacted fill,
    not the plastically-flowed SE the MPM produces."""
    xs = np.linspace(SW[0], SW[1], n)
    zs = np.linspace(FLOOR, top, max(2, int(n * (top - FLOOR) / WIDTH)))
    X, Y, Z = np.meshgrid(xs, xs, zs, indexing='ij')
    pts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    is_am = np.zeros(len(pts), bool)
    for i in range(len(r)):                              # 457 spheres, vectorised
        is_am |= ((pts - c[i]) ** 2).sum(1) <= r[i] ** 2
    free = np.where(~is_am)[0]
    k = min(int(se_frac * len(pts)), len(free))
    return pts[rng.choice(free, size=k, replace=False)]


def _cut_keep(pts, cut, xmid, ymid):
    if cut == 'half':
        return pts[:, 1] >= ymid
    if cut == 'quarter':
        return (pts[:, 1] >= ymid) | (pts[:, 0] >= xmid)
    return np.ones(len(pts), bool)


def render_mpl(t, c, r, se, cut, se_sample, out, rng, se_slab=0.0):
    xmid = ymid = 0.5 * (SW[0] + SW[1])
    keep_se = _cut_keep(se, cut, xmid, ymid)
    se = se[keep_se]
    if se_slab > 0.0 and cut != 'none':
        # show SE only as a thin layer at the exposed cut face(s) → a clean
        # cross-section of the void-fill instead of a full-volume dust cloud
        near = (se[:, 1] <= ymid + se_slab)
        if cut == 'quarter':
            near |= (se[:, 0] <= xmid + se_slab)
        se = se[near]
    if len(se) > se_sample:
        se = se[rng.choice(len(se), se_sample, replace=False)]

    fig = plt.figure(figsize=(11, 10))
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 16); v = np.linspace(0, np.pi, 11)
    su = np.outer(np.cos(u), np.sin(v))
    sv = np.outer(np.sin(u), np.sin(v))
    sw = np.outer(np.ones_like(u), np.cos(v))

    def keep_pt(x, y):                                   # cut-plane mask (hide front)
        if cut == 'half':
            return y >= ymid
        if cut == 'quarter':
            return (y >= ymid) | (x >= xmid)
        return np.ones_like(x, bool)

    drawn = 0
    for i in range(len(r)):
        # skip spheres entirely in the removed region
        if cut == 'half' and c[i, 1] + r[i] < ymid:
            continue
        if cut == 'quarter' and (c[i, 1] + r[i] < ymid and c[i, 0] + r[i] < xmid):
            continue
        xs = c[i, 0] + r[i] * su; ys = c[i, 1] + r[i] * sv; zs = c[i, 2] + r[i] * sw
        hide = ~keep_pt(xs, ys)                          # slice the straddling spheres
        if hide.any():
            xs = xs.copy(); xs[hide] = np.nan
        ax.plot_surface(xs, ys, zs, color=COL[t[i]], linewidth=0, antialiased=False,
                        alpha=0.95 if t[i] == 1 else 0.85, shade=True,
                        rcount=11, ccount=16)
        drawn += 1
    ax.scatter(se[:, 0], se[:, 1], se[:, 2], s=3, c=COL[3], alpha=0.18,
               depthshade=True, linewidths=0)

    ax.set_box_aspect((1, 1, (max(c[:, 2] + r) - FLOOR) / WIDTH))
    ax.view_init(elev=16, azim=-70)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_title(f'MPM scaffold morphology (3D, cut={cut})\n'
                 f'AM_P dark · AM_S gray · SE yellow ({len(se):,} pts shown) · '
                 f'{drawn} AM spheres', fontsize=10)
    plt.tight_layout(); plt.savefig(out, dpi=140)
    print(f'saved {out}   (mpl, {drawn} AM spheres, {len(se):,} SE pts, cut={cut})')


def render_plotly(t, c, r, se, se_sample, out, rng):
    import plotly.graph_objects as go
    if len(se) > se_sample:
        se = se[rng.choice(len(se), se_sample, replace=False)]
    # AM as size-scaled markers per type (WebGL gives real depth occlusion)
    px_per_box = 620.0                                   # marker px ≈ radius·this
    data = []
    for ty, name in ((1, 'AM_P'), (2, 'AM_S')):
        m = t == ty
        if not m.any():
            continue
        data.append(go.Scatter3d(
            x=c[m, 0], y=c[m, 1], z=c[m, 2], mode='markers', name=name,
            marker=dict(size=np.clip(r[m] * px_per_box, 3, 46), color=COL[ty],
                        opacity=0.95, line=dict(width=0))))
    data.append(go.Scatter3d(
        x=se[:, 0], y=se[:, 1], z=se[:, 2], mode='markers', name='SE',
        marker=dict(size=1.6, color=COL[3], opacity=0.45)))
    fig = go.Figure(data=data)
    fig.update_layout(title='MPM scaffold morphology (interactive 3D) — '
                      'AM skeleton + plastic SE void-fill',
                      scene=dict(xaxis_title='x', yaxis_title='y',
                                 zaxis_title='z (compaction)',
                                 aspectmode='data'))
    fig.write_html(out)
    print(f'saved {out}   (plotly interactive, {len(se):,} SE pts)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scaffold', required=True, help='AM scaffold CSV (type,x,y,z,r)')
    ap.add_argument('--se', help='SE point cloud npy [n,3] box units (--save-se output)')
    ap.add_argument('--se-proxy', action='store_true',
                    help='no MPM run: cell-fill the interstices (geometry proxy)')
    ap.add_argument('--se-frac', type=float, default=0.27, help='proxy fill fraction')
    ap.add_argument('--proxy-n', type=int, default=90, help='proxy grid resolution')
    ap.add_argument('--engine', choices=['mpl', 'plotly'], default='mpl')
    ap.add_argument('--cut', choices=['none', 'half', 'quarter'], default='quarter',
                    help='corner cutaway to see inside (mpl only)')
    ap.add_argument('--se-sample', type=int, default=60000, help='max SE pts rendered')
    ap.add_argument('--se-slab', type=float, default=0.05,
                    help='mpl only: show SE only within this depth of the cut face '
                         '(box units; 0 = full volume dust). Declutters the view.')
    ap.add_argument('--out', default='mpm_morphology_3d.png')
    a = ap.parse_args()

    rng = np.random.default_rng(0)
    t, c, r = load_am(a.scaffold)
    top = float((c[:, 2] + r).max()) + 0.01
    if a.se_proxy or not a.se:
        se = proxy_se(c, r, a.se_frac, top, a.proxy_n, rng)
        print(f'proxy SE: {len(se):,} cell-fill pts (se_frac={a.se_frac}, '
              f'n={a.proxy_n}) — GEOMETRY only, not plastic flow')
    else:
        se = np.load(a.se).astype(np.float64)
        print(f'loaded {len(se):,} SE pts from {a.se}')

    if a.engine == 'plotly':
        render_plotly(t, c, r, se, a.se_sample, a.out, rng)
    else:
        render_mpl(t, c, r, se, a.cut, a.se_sample, a.out, rng, se_slab=a.se_slab)


if __name__ == '__main__':
    main()
