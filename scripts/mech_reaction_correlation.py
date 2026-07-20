#!/usr/bin/env python3
"""Mechanical (SE plastic strain / AM contact-coverage) ↔ reaction spatial
correlation for a STEP4 MPM payload.

The STEP4 reaction current j_rxn lives on the AM particles; the SE plastic
strain field lives in `se_strain_points` (x,y,z,Σdg).  This module bins both
through-thickness (z) and reports:
  • z-profile: j_rxn(z), coverage(z), SE-plastic-strain(z)
  • Pearson correlation  j_rxn–coverage  and  j_rxn–strain
  • per-particle  j_rxn vs coverage

★ OBSERVATIONAL ONLY.  The model has NO stress→reaction coupling: j_rxn is
transport-driven (ion access), strain is compaction-driven.  A spatial
correlation is co-location, not causation — the causal chemo-mechanical
coupling (A10) is a separate track.  j_rxn–coverage IS meaningful, because
coverage = the AM|SE Butler–Volmer reaction interface area.

Public API (used by the webapp route + CLI):
  compute(payload, n_bins=14) -> dict
  render_figure(payload, n_bins=14) -> matplotlib.figure.Figure
  to_csv_rows(payload, n_bins=14) -> list[list]

CLI:  python3 scripts/mech_reaction_correlation.py <payload.json> [--bins 14]
"""
from __future__ import annotations
import argparse
import json
import math
import sys


def _pearson(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pts)
    if n < 3:
        return None
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    mx = sx / n; my = sy / n
    cov = sum((p[0]-mx)*(p[1]-my) for p in pts)
    vx = sum((p[0]-mx)**2 for p in pts); vy = sum((p[1]-my)**2 for p in pts)
    if vx <= 0 or vy <= 0:
        return None
    return cov / math.sqrt(vx*vy)


def _partial_corr(y, x, ctrl):
    """Pearson(y, x) controlling for `ctrl` — correlation of the residuals after
    regressing each of y and x linearly on ctrl.  Isolates a genuine x↔y link
    from a shared dependence on ctrl (here ctrl = z, the separator distance)."""
    trip = [(a, b, c) for a, b, c in zip(y, x, ctrl)
            if a is not None and b is not None and c is not None]
    n = len(trip)
    if n < 4:
        return None
    ys = [t[0] for t in trip]; xs = [t[1] for t in trip]; cs = [t[2] for t in trip]

    def _resid(v):
        mc = sum(cs) / n; mv = sum(v) / n
        vc = sum((ci - mc) ** 2 for ci in cs)
        if vc <= 0:
            return None
        sl = sum((ci - mc) * (vi - mv) for ci, vi in zip(cs, v)) / vc
        return [vi - (mv + sl * (ci - mc)) for vi, ci in zip(v, cs)]

    ry = _resid(ys); rx = _resid(xs)
    if ry is None or rx is None:
        return None
    return _pearson(ry, rx)


def _within_slice_corr(y, x, z, n_bins, zmin, zmax):
    """Mean of the per-z-bin Pearson(x, y) — correlation that survives INSIDE a
    fixed depth, i.e. not explained by the shared z-gradient."""
    if zmax <= zmin:
        return None
    bins = [[] for _ in range(n_bins)]
    for a, b, zz in zip(y, x, z):
        if a is None or b is None:
            continue
        k = int((zz - zmin) / (zmax - zmin) * n_bins)
        k = min(max(k, 0), n_bins - 1)
        bins[k].append((b, a))
    rs = []
    for bb in bins:
        if len(bb) > 5:
            r = _pearson([p[0] for p in bb], [p[1] for p in bb])
            if r is not None:
                rs.append(r)
    return (sum(rs) / len(rs)) if rs else None


def compute(payload, n_bins=14):
    """Return the z-profiles + correlations from a STEP4 MPM payload dict."""
    parts = payload.get('particles') or []
    strain_pts = payload.get('se_strain_points') or []
    case = payload.get('case') or ''

    # per-particle arrays
    pz  = [float(p.get('z', 0.0)) for p in parts]
    pjr = [float(p.get('jrxn', 0.0)) for p in parts if p.get('jrxn') is not None]
    have_jrxn = len(pjr) == len(parts) and len(parts) > 0
    pjr = [float(p.get('jrxn')) if p.get('jrxn') is not None else None for p in parts]
    pcov = [float(p.get('coverage')) if p.get('coverage') is not None else None
            for p in parts]

    zs = [z for z in pz]
    # strain point z + value  (list rows: [x,y,z,strain])
    sz = [float(r[2]) for r in strain_pts if len(r) >= 4]
    sst = [float(r[3]) for r in strain_pts if len(r) >= 4]

    zmin = min(zs) if zs else 0.0
    zmax = max(zs) if zs else 1.0
    if zmax <= zmin:
        zmax = zmin + 1.0
    edges = [zmin + (zmax-zmin)*i/n_bins for i in range(n_bins+1)]
    zc = [0.5*(edges[i]+edges[i+1]) for i in range(n_bins)]

    def _bin(zv, vv):
        acc = [[] for _ in range(n_bins)]
        for z, v in zip(zv, vv):
            if v is None:
                continue
            k = int((z - zmin) / (zmax - zmin) * n_bins)
            if k >= n_bins:
                k = n_bins - 1
            if k < 0:
                k = 0
            acc[k].append(v)
        return [ (sum(a)/len(a) if a else None) for a in acc ]

    jr_z  = _bin(pz, pjr) if have_jrxn else [None]*n_bins
    cov_z = _bin(pz, pcov)
    st_z  = _bin(sz, sst) if sz else [None]*n_bins

    return {
        'case': case, 'n_bins': n_bins, 'z_um': zc,
        'jrxn_z': jr_z, 'coverage_z': cov_z, 'strain_z': st_z,
        'have_jrxn': have_jrxn, 'have_strain': bool(sz),
        # z-profile Pearson — BOTH curves are monotonic in z so these are
        # inflated by the shared z-gradient (z-confound); report but caveat.
        'corr_jrxn_coverage': _pearson(jr_z, cov_z),
        'corr_jrxn_strain':   _pearson(jr_z, st_z),
        'corr_particle_jrxn_coverage': _pearson(list(pjr), list(pcov)),
        # ── honesty layer: is the coverage link REAL or just the z-gradient? ──
        'corr_jrxn_z': _pearson(list(pjr), list(pz)),            # reaction is z-driven (ion-limited)
        'corr_jrxn_coverage_partial_z': _partial_corr(pjr, pcov, pz),   # z-controlled → genuine link
        'corr_jrxn_coverage_within_slice': _within_slice_corr(pjr, pcov, pz, n_bins, zmin, zmax),
        '_pp': {'z': pz, 'jrxn': pjr, 'coverage': pcov},
    }


def to_csv_rows(payload, n_bins=14):
    d = compute(payload, n_bins)
    rows = [['z_um', 'jrxn_mean', 'coverage_mean_pct', 'se_plastic_strain_mean']]
    for i in range(d['n_bins']):
        rows.append([
            f"{d['z_um'][i]:.1f}",
            '' if d['jrxn_z'][i] is None else f"{d['jrxn_z'][i]:.4f}",
            '' if d['coverage_z'][i] is None else f"{d['coverage_z'][i]:.1f}",
            '' if d['strain_z'][i] is None else f"{d['strain_z'][i]:.4f}",
        ])
    return rows


def render_figure(payload, n_bins=14):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    d = compute(payload, n_bins)
    zc = d['z_um']
    jr, cov, st = d['jrxn_z'], d['coverage_z'], d['strain_z']
    pp = d['_pp']

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    a0 = ax[0]; a0b = a0.twinx()
    handles = []
    if d['have_jrxn']:
        handles += a0.plot([z for z, v in zip(zc, jr) if v is not None],
                           [v for v in jr if v is not None],
                           '-o', color='#d1495b', ms=4, lw=1.8,
                           label='reaction j_rxn(z)')
    handles += a0.plot([z for z, v in zip(zc, cov) if v is not None],
                       [v/100.0 for v in cov if v is not None],
                       '-s', color='#8a8f98', ms=3, lw=1.2, label='coverage(z)/100')
    if d['have_strain']:
        handles += a0b.plot([z for z, v in zip(zc, st) if v is not None],
                            [v for v in st if v is not None],
                            '-^', color='#2e6fdb', ms=4, lw=1.8,
                            label='SE plastic strain(z)')
    a0.set_xlabel('z (um)   [bottom = collector  ->  top = separator]')
    a0.set_ylabel('j_rxn (i / i-bar)  .  coverage/100')
    a0b.set_ylabel('SE plastic strain (sum dg)', color='#2e6fdb')
    def _f(v):
        return 'n/a' if v is None else f'{v:+.2f}'
    rjc = d['corr_jrxn_coverage']; rjs = d['corr_jrxn_strain']
    a0.set_title('z-profile: reaction vs mechanics (strain / contact)\n'
                 'j-coverage %s (raw, z-confounded)   j-strain %s (co-location, no coupling)'
                 % (_f(rjc), _f(rjs)))
    a0.legend(handles, [h.get_label() for h in handles], fontsize=8,
              loc='upper left', frameon=False)
    a0.grid(alpha=.25, lw=.5)

    # per-particle scatter j_rxn vs coverage, coloured by z
    xs = [c for c, j in zip(pp['coverage'], pp['jrxn']) if c is not None and j is not None]
    ys = [j for c, j in zip(pp['coverage'], pp['jrxn']) if c is not None and j is not None]
    cz = [z for z, c, j in zip(pp['z'], pp['coverage'], pp['jrxn'])
          if c is not None and j is not None]
    if xs and ys:
        sc = ax[1].scatter(xs, ys, c=cz, cmap='viridis', s=14, alpha=.7)
        cb = fig.colorbar(sc, ax=ax[1]); cb.set_label('z (um)')
        rpc = d['corr_particle_jrxn_coverage']
        ax[1].set_title('per-particle: reaction vs contact  (colour = z)\n'
                        'raw %s -> z-controlled %s (within-slice %s);  reaction~z %s'
                        % (_f(rpc), _f(d['corr_jrxn_coverage_partial_z']),
                           _f(d['corr_jrxn_coverage_within_slice']), _f(d['corr_jrxn_z'])))
    else:
        ax[1].text(0.5, 0.5, 'no per-particle j_rxn', ha='center', va='center',
                   transform=ax[1].transAxes)
    ax[1].set_xlabel('particle coverage (%)   [contact / mechanical proxy]')
    ax[1].set_ylabel('particle j_rxn  (i / i-bar)')
    ax[1].grid(alpha=.25, lw=.5)

    fig.suptitle('reaction <-> mechanics (stress/strain) spatial correlation  |  %s'
                 '   [OBSERVATIONAL - no stress->reaction coupling]'
                 % (d['case'] or 'payload'), fontweight='bold', fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, .93])
    return fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('payload')
    ap.add_argument('--bins', type=int, default=14)
    ap.add_argument('--out', default='mech_reaction.png')
    a = ap.parse_args()
    with open(a.payload) as f:
        payload = json.load(f)
    d = compute(payload, a.bins)
    print(f"case={d['case']}  have_jrxn={d['have_jrxn']}  have_strain={d['have_strain']}")
    print(f"corr j_rxn-coverage={d['corr_jrxn_coverage']}  "
          f"j_rxn-strain={d['corr_jrxn_strain']}  "
          f"per-particle={d['corr_particle_jrxn_coverage']}")
    fig = render_figure(payload, a.bins)
    fig.savefig(a.out, dpi=150)
    print(f"wrote {a.out}")


if __name__ == '__main__':
    main()
