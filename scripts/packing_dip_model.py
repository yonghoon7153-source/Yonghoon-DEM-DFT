#!/usr/bin/env python3
"""Resolution-FREE geometric packing dip  —  de Larrard linear packing model.

WHY THIS EXISTS (CLAUDE.md frame [3] Furnas dip):
  The MPM/DEM "porosity vs AM%" dip kept coming out resolution-dependent because
  it was read at a *common pressure*, and the MPM pressure read-out is itself
  resolution-biased (320 vs 512 differ ~55-72% at the SAME porosity).  The user's
  goal: "절대값이 안맞아도 괜찮아 — 트랜드 확인하는데 환경(해상도)이 변수가
  되면 안된다"  (absolutes may be off, but the TREND must not depend on the
  numerical environment).

  The cleanest possible way to remove resolution as a variable is to remove the
  grid ENTIRELY.  This script computes the porosity-vs-composition trend from
  pure packing GEOMETRY — continuous coordinates, no grid, no pressure read-out,
  no plasticity model.  If the dip appears HERE, it is a geometric-packing fact
  (frame [3]: "the dip is a GEOMETRIC packing effect, independent of plasticity
  model"), not a numerical artifact.

NOT A FORCED FIT (answers the user's "왜 문헌곡선 강제매칭이랑 가까워지냐"):
  The only inputs are (a) the real particle size ratio 12:4:1 (AMP:AMS:SE,
  CLAUDE.md frame) and (b) the single-species packing density beta (a measurable
  geometric constant — we SWEEP it to show the dip is robust, i.e. not tuned).
  Nothing is fit to any target curve.  We SELF-VALIDATE the model by checking it
  reproduces the PARAMETER-FREE Furnas ideal limit (infinite size separation ->
  porosity = product of component porosities, optimum coarse fraction =
  1/(1+eps0)).  Passing that proves the code is doing geometry, not matching.

MODEL: de Larrard / Yu-Standish Linear Packing Density Model.
  virtual packing density   gamma = min_i gamma_i
  gamma_i = beta_i / (1 - sum_{j coarser}[wall]*y_j - sum_{j finer}[loosening]*y_j)
    wall_ij      = 1 - beta_i + b_ij*beta_i*(1 - 1/beta_j),  b_ij = 1-(1-d_i/d_j)^1.50
    loosening_ij = 1 - a_ij*beta_i/beta_j,                   a_ij = sqrt(1-(1-d_j/d_i)^1.02)
  actual packing density via compaction index K (de Larrard):
    K = sum_i (y_i/beta_i) / (1/phi - 1/gamma_i)    -> solve for phi (bisection)
  (K -> inf recovers virtual gamma.  K~9 = vibrated+pressed, appropriate for a
   hundreds-of-MPa cold press.)

Run:  python3 scripts/packing_dip_model.py
Out:  table + ASCII trend + docs/data/packing_dip_model.csv  (+ optional PNG)
"""
import numpy as np
import os

# composition convention copied verbatim from scripts/mpm2d_composition.py
RHO_AM, RHO_SE = 4800.0, 2000.0          # wt% -> volume% densities
SIZES = dict(AMP=12.0, AMS=4.0, SE=1.0)  # real 12:4:1 ratio (CLAUDE.md frame)


# ---------------------------------------------------------------- core model --
def _per_class_gamma(d, b, y):
    """per-class virtual packing density gamma_i (classes already sorted L->S)."""
    n = len(d)
    gi = np.empty(n)
    for i in range(n):
        denom = 1.0
        for j in range(n):
            if j == i:
                continue
            if d[j] > d[i]:                                   # j coarser -> wall on fine i
                b_ij = 1.0 - (1.0 - d[i] / d[j]) ** 1.50
                denom -= (1.0 - b[i] + b_ij * b[i] * (1.0 - 1.0 / b[j])) * y[j]
            else:                                             # j finer -> loosens coarse i
                a_ij = np.sqrt(max(0.0, 1.0 - (1.0 - d[j] / d[i]) ** 1.02))
                denom -= (1.0 - a_ij * b[i] / b[j]) * y[j]
        gi[i] = b[i] / denom if denom > 1e-9 else 1e9
    return gi


def virtual_gamma(diams, betas, y):
    """virtual (K->inf, theoretical-max) packing density = min_i gamma_i."""
    d = np.asarray(diams, float); b = np.asarray(betas, float); y = np.asarray(y, float)
    o = np.argsort(-d)
    return float(_per_class_gamma(d[o], b[o], y[o]).min())


def actual_phi(diams, betas, y, K=9.0):
    """de Larrard actual packing density for finite compaction index K."""
    d = np.asarray(diams, float); b = np.asarray(betas, float); y = np.asarray(y, float)
    o = np.argsort(-d); d, b, y = d[o], b[o], y[o]
    ys = y / y.sum()
    gi = _per_class_gamma(d, b, y)
    gmin = gi.min()

    def Kof(phi):
        s = 0.0
        for i in range(len(d)):
            if ys[i] <= 0:
                continue
            den = (1.0 / phi - 1.0 / gi[i])
            if den <= 1e-12:
                return np.inf
            s += (ys[i] / b[i]) / den
        return s

    lo, hi = 1e-4, gmin * (1.0 - 1e-9)
    for _ in range(200):                      # K(phi) is monotone increasing in phi
        mid = 0.5 * (lo + hi)
        if Kof(mid) > K:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------- composition --
def vol_fracs(am_wt, ps=(7, 3)):
    """AM weight% -> volume fractions of {AMP, AMS, SE} (sum=1), P:S split."""
    w = am_wt / 100.0
    if w <= 0:
        vam = 0.0
    elif w >= 1:
        vam = 1.0
    else:
        a = w / RHO_AM; bb = (1.0 - w) / RHO_SE; vam = a / (a + bb)
    p, s = ps
    fp, fs = p / (p + s), s / (p + s)
    return {'AMP': fp * vam, 'AMS': fs * vam, 'SE': 1.0 - vam}


def porosity_curve(am_grid, beta, K, ps=(7, 3), sizes=SIZES):
    out = []
    for am in am_grid:
        f = vol_fracs(am, ps)
        diams = [sizes['AMP'], sizes['AMS'], sizes['SE']]
        y = [f['AMP'], f['AMS'], f['SE']]
        betas = [beta, beta, beta]
        nz = [k for k in range(3) if y[k] > 1e-12]
        if len(nz) == 0:
            out.append(np.nan); continue
        d2 = [diams[k] for k in nz]; y2 = [y[k] for k in nz]; b2 = [betas[k] for k in nz]
        phi = actual_phi(d2, b2, y2, K=K)
        out.append((1.0 - phi) * 100.0)
    return np.array(out)


# ----------------------------------------------------------------- self test --
def self_validate():
    """Prove the code does GEOMETRY: virtual gamma must hit the Furnas ideal
    limit (1-eps0^2 at coarse fraction 1/(1+eps0)) for a huge size ratio."""
    print("=" * 74)
    print("SELF-VALIDATION  (NOT a fit — checks the parameter-free Furnas ideal)")
    print("=" * 74)
    ok_all = True
    for beta in (0.84, 0.74, 0.64):
        eps0 = 1.0 - beta
        ys = np.linspace(0.001, 0.999, 999)
        g = np.array([virtual_gamma([1e4, 1.0], [beta, beta], [yy, 1 - yy]) for yy in ys])
        i = int(np.nanargmax(g))
        phi_pred, y1_pred = g[i], ys[i]
        phi_ideal, y1_ideal = 1 - eps0 ** 2, 1.0 / (1.0 + eps0)
        ok = abs(phi_pred - phi_ideal) < 0.01 and abs(y1_pred - y1_ideal) < 0.03
        ok_all &= ok
        print(f"  beta={beta:.2f} (eps0={eps0:.2f}):  virtual phi_max={phi_pred:.4f} "
              f"(ideal {phi_ideal:.4f}) @ coarse y1={y1_pred:.3f} (ideal {y1_ideal:.3f})"
              f"   [{'PASS' if ok else 'FAIL'}]")
    print(f"  --> de Larrard reproduces the parameter-free Furnas ideal limit: "
          f"{'PASS' if ok_all else 'FAIL'}\n")
    return ok_all


# ----------------------------------------------------------------- reporting --
def ascii_trend(am, por, width=52):
    lo, hi = np.nanmin(por), np.nanmax(por)
    span = max(hi - lo, 1e-6)
    di = int(np.nanargmin(por))
    print(f"  {'AM wt%':>6} {'poros%':>7}  {'(min='+format(lo,'.1f')+'  max='+format(hi,'.1f')+')':<22}")
    for k, (a, p) in enumerate(zip(am, por)):
        n = int(round((p - lo) / span * width))
        bar = '#' * n
        mark = '  <== DIP' if k == di else ''
        print(f"  {a:6.0f} {p:7.2f}  |{bar:<{width}}|{mark}")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--ps', default='7:3', help='AM_P:AM_S split, e.g. 7:3, 5:5, 3:7')
    a = ap.parse_args()
    p, s = (int(z) for z in a.ps.split(':'))
    ps = (p, s); tag = f"ps{p}{s}"

    passed = self_validate()

    am = np.arange(0, 101, 5.0)
    K = 9.0                                   # vibrated+pressed (hundreds of MPa)
    print("=" * 74)
    print(f"POROSITY vs AM wt%   (P:S = {p}:{s}, sizes 12:4:1, de Larrard K={K:.0f})")
    print("  grid-free / resolution-free by construction — no MPM grid involved")
    print("=" * 74)

    rows = [('AM_wt%',)]
    curves = {}
    for beta in (0.88, 0.86, 0.84, 0.80, 0.74, 0.64):
        por = porosity_curve(am, beta, K, ps=ps)
        curves[beta] = por
        di = int(np.nanargmin(por))
        end = 0.5 * (por[0] + por[-1])
        depth = end - por[di]
        print(f"\n  beta={beta:.2f}  (2D-RCP~0.84, 3D-RCP~0.64):  "
              f"DIP at AM={am[di]:.0f}wt%  poros_min={por[di]:.2f}%  "
              f"(endpoints avg {end:.2f}% -> dip depth {depth:.2f}%p)")

    print("\n  ---- ASCII trend at beta=0.84 (2D RCP, closest to the MPM) ----")
    ascii_trend(am, curves[0.84])

    print("\n  ---- ASCII trend at beta=0.64 (3D RCP, textbook McGeary scale) ----")
    ascii_trend(am, curves[0.64])

    # CSV — tagged per P:S; also keep the plain name for the 7:3 default (compat)
    os.makedirs('docs/data', exist_ok=True)
    betas = sorted(curves.keys())
    hdr = 'AM_wt%,' + ','.join(f'poros_beta{b:.2f}' for b in betas)
    lines = [hdr]
    for i, a in enumerate(am):
        lines.append(f"{a:.0f}," + ','.join(f"{curves[b][i]:.3f}" for b in betas))
    out_paths = [f'docs/data/packing_dip_model_{tag}.csv']
    if ps == (7, 3):
        out_paths.append('docs/data/packing_dip_model.csv')
    for op in out_paths:
        with open(op, 'w') as fh:
            fh.write('\n'.join(lines) + '\n')
    print(f"\n  saved {', '.join(out_paths)}")

    # optional plot (works on WSL/uma where matplotlib exists)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7.4, 5.0))
        for b in (0.88, 0.84, 0.74, 0.64):
            ax.plot(am, curves[b], '-o', ms=4, lw=1.8, label=f'beta={b:.2f}')
        ax.set_xlabel('AM weight fraction (%)')
        ax.set_ylabel('porosity (%)')
        ax.set_title('Resolution-FREE geometric packing dip (de Larrard)\n'
                     f'sizes 12:4:1, P:S={p}:{s}, K=9 — no grid, no pressure read-out',
                     fontsize=10)
        ax.legend(fontsize=8); ax.grid(alpha=0.3)
        plt.tight_layout()
        os.makedirs('docs/figures', exist_ok=True)
        plt.savefig(f'docs/figures/packing_dip_model_{tag}.png', dpi=130)
        print(f"  saved docs/figures/packing_dip_model_{tag}.png")
    except Exception as e:
        print(f"  (plot skipped — no matplotlib here: {e})")

    print("\n" + "=" * 74)
    print("INTERPRETATION (frame [3]-compliant; report to user, do not solo-decide):")
    print("  * This curve has NO resolution parameter — it cannot move with grid")
    print("    size.  It is the geometric trend the MPM rigid-jamming sweep should")
    print("    CONVERGE to as n_grid increases.")
    print("  * If a dip is present here, the dip is geometric-packing physics")
    print("    (frame [3]); if it is shallow/absent at 12:4:1, that quantifies how")
    print("    weak the geometric dip is at THIS size ratio (AMS/AMP ratio is only 3).")
    print("=" * 74)


if __name__ == '__main__':
    main()
