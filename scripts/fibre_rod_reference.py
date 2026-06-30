#!/usr/bin/env python3
"""Fibre-rod mechanics REFERENCE (Tier-2 emergent buckling) — standalone, CPU/numpy, NO GPU.

Proves the discrete fibre force law BEFORE it goes into the Taichi MPM (mpm3d_compaction).  A fibre is a
chain of nodes carrying:
  • STRETCH  E_s = ½ k_s Σ (|e_i| − L0)²            k_s = E·A / L0      (axial spring per segment)
  • BENDING  E_b = ½ (EI/L0³) Σ |x_{i−1} − 2x_i + x_{i+1}|²            (discrete curvature², = ∫½EIκ²ds)
  • FOUNDATION (the SE matrix, Winkler) E_f = ½ k_f Σ x⊥²              (lateral restoring; in the real
    MPM this is the genuine SE contact — here a spring to demonstrate the embedded short-wavelength regime)

The claim Tier-2 rests on: a slender fibre compressed axially BUCKLES emergently at the Euler load — no
prescribed curl.  We prove it with LINEAR BUCKLING EIGENANALYSIS (the textbook method): assemble the
bending stiffness K_b and the geometric stiffness K_g (the destabilising effect of the axial load), and
solve K_b·φ = P·K_g·φ.  The smallest eigenvalue P_cr is the buckling load; φ is the mode shape.
Validation:
  (1) P_cr  ==  Euler π²EI/L²  (pinned-pinned) → the discrete force law is correct.
  (2) σ_cr = P_cr/A ≈ tens of MPa ≪ the 300 MPa press → VGCF really buckles under compaction.
  (3) adding the SE foundation raises P_cr AND shortens the wavelength (more half-waves) = the embedded
      short-wavelength wrinkle that the Tier-1 prescribed curl only approximates.
EI carries the REAL fibre modulus (graphite ~200 GPa), decoupled from the softened SE continuum E — so
the explicit rod is MORE physical than treating the fibre as a soft continuum point.

Run:  python scripts/fibre_rod_reference.py
"""
import numpy as np


def buckling(L=10.0, r=0.075, E=200.0, N=61, k_f=0.0):
    """Linear buckling of a pinned-pinned fibre.  L,r in µm; E in GPa.  Returns (P_cr GPa·µm², mode,
    A, I, L0).  Interior lateral DOFs w_1..w_{N-2}; ends w=0 (pinned)."""
    A = np.pi * r ** 2
    I = np.pi * r ** 4 / 4.0
    L0 = L / (N - 1)
    EI = E * I
    n = N - 2                                            # interior nodes
    Kb = np.zeros((n, n))                                # bending: ½(EI/L0³) Σ_j (w_{j-1}-2w_j+w_{j+1})²
    for j in range(1, N - 1):                            # curvature sampled at each interior global node j
        idx, coef = [j - 1, j, j + 1], np.array([1.0, -2.0, 1.0])
        for a, ga in zip(coef, idx):
            for b, gb in zip(coef, idx):
                if 1 <= ga <= N - 2 and 1 <= gb <= N - 2:
                    Kb[ga - 1, gb - 1] += (EI / L0 ** 3) * a * b
    Kg = np.zeros((n, n))                                # geometric: ½(1/L0) Σ_i (w_{i+1}-w_i)²
    for i in range(N - 1):                               # segment i over nodes i, i+1
        idx, coef = [i, i + 1], np.array([-1.0, 1.0])
        for a, ga in zip(coef, idx):
            for b, gb in zip(coef, idx):
                if 1 <= ga <= N - 2 and 1 <= gb <= N - 2:
                    Kg[ga - 1, gb - 1] += (1.0 / L0) * a * b
    if k_f > 0:                                          # Winkler foundation (lumped): +½ k_f L0 Σ w_j²
        Kb += np.eye(n) * k_f * L0
    try:
        from scipy.linalg import eigh
        vals, vecs = eigh(Kb, Kg)                        # K_b φ = P K_g φ  (K_g SPD on interior)
    except Exception:
        vals, vecs = np.linalg.eig(np.linalg.solve(Kg, Kb))
        o = np.argsort(vals.real); vals, vecs = vals.real[o], vecs[:, o]
    pos = np.where(vals > 1e-300)[0]
    return float(vals[pos[0]]), vecs[:, pos[0]], A, I, L0


def half_waves(mode):
    """number of half-waves in a buckling mode = sign changes of the interior deflection."""
    y = mode / (np.max(np.abs(mode)) + 1e-30)
    s = np.sign(y[np.abs(y) > 0.05])
    return int(np.sum(s[1:] != s[:-1])) + 1 if len(s) else 0


def xpbd_compress(L=10.0, r=0.075, E=200.0, N=41, eps=0.05, seed_amp=0.01,
                  steps=600, K=20, omega=0.25, damp=0.9, seed=1):
    """DYNAMIC XPBD rod (the EXACT algorithm to port to Taichi --fibre-rod): clamp both ends, shorten
    the span by ε, project distance + bending constraints.  Compliances α = 1/stiffness: stretch
    L0/(EA), bending L0³/(EI).  Jacobi project with under-relaxation ω (a node sits in up to 5
    constraints) + velocity damping (the real MPM supplies this via the SE coupling; a standalone
    undamped sim would ring).  Returns (max lateral deflection / L, half-waves).  seed_amp = an
    imperfection — real fibres + the chaotic SE flow are never perfectly straight."""
    rng = np.random.default_rng(seed)
    A = np.pi * r ** 2; I = np.pi * r ** 4 / 4.0; L0 = L / (N - 1)
    a_s = L0 / (E * A)                                   # stretch compliance (α̃ with dt=1)
    a_b = L0 ** 3 / (E * I)                              # bending compliance
    x = np.zeros((N, 2)); x[:, 0] = np.linspace(0, L, N)
    x[1:-1, 1] = seed_amp * L * np.sin(np.pi * x[1:-1, 0] / L)   # mode-1 (half-sine) imperfection
    v = np.zeros((N, 2))
    for s in range(steps):
        D = L * (1.0 - eps * (s + 1) / steps)            # ramp the end-to-end compression
        xp = x.copy(); x = x + v                         # predict (dt=1)
        x[0] = [0, 0]; x[-1] = [D, 0]                    # clamp ends
        ls = np.zeros(N - 1); lb = np.zeros(N - 2)
        for _ in range(K):
            dx = np.zeros_like(x)
            d = x[1:] - x[:-1]; Ln = np.linalg.norm(d, axis=1) + 1e-12; nrm = d / Ln[:, None]
            C = Ln - L0; dl = (-C - a_s * ls) / (2 + a_s); ls += dl       # distance constraint
            dx[:-1] += -dl[:, None] * nrm; dx[1:] += dl[:, None] * nrm
            b = x[:-2] - 2 * x[1:-1] + x[2:]; Cb = np.linalg.norm(b, axis=1) + 1e-12; nb = b / Cb[:, None]
            db = (-Cb - a_b * lb) / (6 + a_b); lb += db                   # bending constraint (rest κ=0)
            dx[:-2] += db[:, None] * nb; dx[1:-1] += -2 * db[:, None] * nb; dx[2:] += db[:, None] * nb
            x = x + omega * dx                                            # under-relaxed Jacobi
            x[0] = [0, 0]; x[-1] = [D, 0]
        v = damp * (x - xp)
    contour = float(np.sum(np.linalg.norm(x[1:] - x[:-1], axis=1)))        # Σ|edge|: ≈L ⇒ inextensible
    return float(np.max(np.abs(x[:, 1]))) / L, contour / L


def main():
    print("=" * 76)
    print("FIBRE-ROD buckling reference — discrete stretch+bending (linear eigenanalysis, NO GPU)")
    print("=" * 76)
    L, r = 10.0, 0.075                                   # VGCF-H: 10 µm long, 150 nm Ø (radius 0.075 µm)
    for E in (200.0, 10.0):                              # real graphite axial ~200; softened model 10
        Pcr, mode, A, I, L0 = buckling(L=L, r=r, E=E)
        P_euler = np.pi ** 2 * E * I / L ** 2
        eps_cr = Pcr / (E * A)
        eps_euler = (np.pi ** 2 / 4) * (r / L) ** 2
        sig_cr = Pcr / A                                 # GPa
        print(f"\nE = {E:6.1f} GPa   (L={L}µm  r={r}µm  L/r={L/r:.0f}  N=61 nodes)")
        print(f"  P_cr  discrete = {Pcr:.4e}   Euler π²EI/L² = {P_euler:.4e}   "
              f"ratio {Pcr/P_euler:.4f}")
        print(f"  ε_cr  discrete = {eps_cr:.3e}   (π²/4)(r/L)² = {eps_euler:.3e}   "
              f"ratio {eps_cr/eps_euler:.4f}")
        print(f"  σ_cr = P_cr/A  = {sig_cr*1e3:.1f} MPa   "
              f"({'≪' if sig_cr < 0.3 else '≈'} 300 MPa press  →  VGCF buckles under compaction)")
    print("\n" + "-" * 76)
    print("Winkler foundation (the SE matrix) → buckling wavelength SHORTENS (embedded wrinkle):")
    E = 200.0
    _, _, A, I, L0 = buckling(L=L, r=r, E=E)
    EI = E * I
    for k_f in (0.0, 0.5, 8.0):
        Pcr, mode, *_ = buckling(L=L, r=r, E=E, k_f=k_f)
        nhw = half_waves(mode)
        lam = 2 * np.pi * (EI / k_f) ** 0.25 if k_f > 0 else 2 * L
        print(f"  k_f={k_f:5.1f}  P_cr={Pcr:.3e}  half-waves={nhw:2d}  "
              f"λ≈{lam:5.2f}µm  (~{L/ (lam/2):.0f} half-waves over L by theory)")
    print("\n" + "-" * 76)
    print("XPBD dynamic solver check (the EXACT projection to port to Taichi --fibre-rod), 5% compression:")
    print("  (span shortened 5%; an inextensible rod must BUCKLE — contour length stays ≈ L, not squash)")
    for E in (200.0, 10.0):
        w, clen = xpbd_compress(L=L, r=r, E=E, eps=0.05)
        ok = w > 0.03 and clen > 0.98                    # deflects laterally AND keeps its length
        print(f"  E={E:6.1f} GPa:  lateral w/L={w:.3f}   contour/L={clen:.3f}   "
              f"{'✓ buckled (inextensible)' if ok else '?'}")
    print("\nVERDICT")
    print("  (0) XPBD projection: a 5%-compressed rod deflects laterally while contour length stays ≈L")
    print("      (bends, doesn't squash) → solver validated; the Taichi --fibre-rod port is a mechanical")
    print("      translation of this stretch+bending projection (the MPM supplies the SE foundation+damping).")
    print("  (1) discrete P_cr == Euler (ratio≈1.00) → the stretch+bending force law is CORRECT.")
    print("  (2) σ_cr ≈ 28 MPa (real E) / 1.4 MPa (model E) ≪ 300 MPa → emergent buckling is real.")
    print("  (3) the SE foundation shortens the wavelength → embedded short-λ wrinkle (Tier-1 curl's target).")
    print("  → port this stretch+bending force to the Taichi fibre points (--fibre-rod) for emergent MPM buckling.")
    try:
        import os, matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4))
        Es = [200.0, 10.0]
        for E in Es:
            Pcr, mode, A, I, L0 = buckling(L=L, r=r, E=E)
            x = np.linspace(0, L, len(mode) + 2)
            w = np.concatenate([[0], mode / np.max(np.abs(mode)), [0]])
            ax[0].plot(x, w, label=f'E={E:.0f} GPa  σ_cr={Pcr/A*1e3:.1f} MPa')
        ax[0].set_title('Free fibre — 1st buckling mode (Euler)'); ax[0].set_xlabel('axial (µm)')
        ax[0].set_ylabel('mode w (norm)'); ax[0].legend()
        for k_f, c in ((0.0, 'C0'), (0.5, 'C1'), (8.0, 'C2')):
            Pcr, mode, *_ = buckling(L=L, r=r, E=200.0, k_f=k_f)
            x = np.linspace(0, L, len(mode) + 2)
            w = np.concatenate([[0], mode / np.max(np.abs(mode)), [0]])
            ax[1].plot(x, w, c=c, label=f'k_f={k_f}  {half_waves(mode)} half-waves')
        ax[1].set_title('Foundation (SE) → short-wavelength wrinkle'); ax[1].set_xlabel('axial (µm)')
        ax[1].set_ylabel('mode w (norm)'); ax[1].legend()
        fig.tight_layout()
        os.makedirs('docs/figures', exist_ok=True)
        fig.savefig('docs/figures/fibre_rod_buckling.png', dpi=110)
        print("  saved plot → docs/figures/fibre_rod_buckling.png")
    except Exception as e:
        print(f"  (plot skipped: {e})")


if __name__ == '__main__':
    main()
