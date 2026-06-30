# Tier-2: emergent fibre buckling in the MPM (sub-grid rod) — design

**Goal.** Make conductive fibres (VGCF, PTFE) **actually buckle/bend because of the press forces**
during the existing MPM compaction — emergent, not the Tier-1 prescribed `curl=f(P)`.  This is the
"가장 현실적" version the user asked for.

**Status.** Force-law CORE **verified** (CPU/numpy, `scripts/fibre_rod_reference.py`).  Taichi
integration into `mpm3d_compaction.py` = the remaining build (`--fibre-rod`, opt-in).

---

## 0. Why MPM is the right home (not DEM)

- The MPM **already applies the press** (servo/hold platen, `substep()` lines 702–704).  A rod model
  just rides the existing pressurised flow.
- **DEM (LIGGGHTS) cannot apply pressure** in this workflow → would need a separate LAMMPS bonded-
  particle + platen sim (user-confirmed).  So although bonded-discrete mechanics is a DEM idiom
  (frame[5]), the **pressurised** version is most practical as an MPM-embedded rod.
- Bonus physics: the rod carries the **real fibre modulus** (graphite VGCF E≈200 GPa) for bending,
  **decoupled** from the softened SE continuum E (1.53) — so the explicit rod is *more* physical than
  treating the fibre as a soft continuum point.

## 1. Why not just refine the grid (the obvious route — infeasible)

A continuum MPM gets bending from the **grid** velocity gradient, but bending stiffness ∝ thickness³ and
VGCF Ø=150 nm is **sub-grid**.  To resolve even ~3 cells across the fibre in a ~100 µm box needs
dx≈50 nm → n_grid≈2000³ ≈ **8×10⁹ cells** — impossible.  ⇒ the bending stiffness must be carried by an
**explicit sub-grid rod on the fibre points**, not by grid resolution.

## 2. The model (VERIFIED force law)

Fibre = chain of nodes (the existing fibre points, contiguous per `fibre_np` id, in walk order):
- **Stretch**  `E_s = ½ k_s Σ (|e_i|−L0)²`,  `k_s = E·A/L0`  (near-inextensible axial spring).
- **Bending**  `E_b = ½ (EI/L0³) Σ |x_{i−1}−2x_i+x_{i+1}|²`  (discrete curvature² = ∫½EIκ²ds),
  `I = πr⁴/4`, real fibre **E** (VGCF ~200, PTFE ~0.5 GPa).
- **Foundation** = the **real SE** (no extra spring needed): the fibre points are already MPM material
  points, so the SE pushes them through the grid (P2G/G2P) — that IS the Winkler foundation.

**Verification** (`scripts/fibre_rod_reference.py`, linear buckling eigenanalysis `K_b φ = P·K_g φ`,
plot `docs/figures/fibre_rod_buckling.png`):

| check | result |
|---|---|
| discrete `P_cr` vs Euler `π²EI/L²` | ratio **0.9998** (E=200 and E=10) → force law correct |
| `σ_cr = P_cr/A` (VGCF L=10µm, r=0.075µm) | **27.8 MPa** (real E=200) / **1.4 MPa** (model E=10) ≪ 300 MPa press → **buckles** |
| SE foundation (Winkler `k_f`) | k_f 0→1, 0.5→10, 8→21 half-waves; λ 20→2→1 µm = `2π(EI/k_f)^¼` (theory) → **embedded short-λ wrinkle** = what Tier-1 `curl` only approximated |

⇒ emergent buckling is **physically real**; porting the stretch+bending force to the MPM fibre points
gives it for free under the existing press.

## 3. MPM coupling (concrete integration points in `substep()`)

The fibre's SE interaction + press already arrive as `v[p]` from G2P (line 722).  Insert the fibre's
**own** stretch+bending response between advection steps:

1. **Connectivity** (one-time): build `fib_prev[p]`, `fib_next[p]` Taichi fields (−1 at fibre ends) from
   `fibre_np` (points are contiguous per fibre, walk order) + rest length `L0_p`, rest curvature κ0_p.
2. **Stability = XPBD, not explicit forces.**  `k_s=EA/L0` is *very* stiff → explicit velocity kicks blow
   up at the MPM dt (the numpy relaxation overflowed for exactly this reason; eigenanalysis sidesteps it,
   but the GPU time-stepper can't).  Use **XPBD** (position-based): after advection (line 736), run K
   constraint-projection iterations along each fibre — (a) edge-length (inextensibility), (b) bending
   (curvature→κ0) — then set `v[p] = (x_new−x_old)/dt`.  XPBD is **unconditionally stable** and decouples
   the stiff rod from the MPM dt (standard for hair/rod in MPM, e.g. Cosserat/DER-PBD).
3. **Order per substep**: P2G (669) → grid-op incl. press (691) → G2P `v,C,F` + plastic + advect (710–736)
   → **XPBD rod solve on fibre points** (new) → write back `v[p]`.  AM stays frozen (scaffold), SE
   continuum unchanged.  Only fibre points get the extra rod constraints.

## 4. Per-additive (the σ_y asymmetry decides priority)

- **VGCF** (σ_y=2.0 GPa ≫ 0.3 press → stays elastic, never yields): the continuum gives it **zero**
  emergent deformation → the rod is the **only** way it buckles.  **Top priority.**
- **PTFE** (σ_y=0.05 < press): already yields/flows in the MPM (partly emergent) + A3 cohesion.  Rod adds
  fibril **draw/alignment** + bond — refinement.  (Bending E≈0.5 GPa, soft.)
- **SuperP** (σ_y=0.1 < press): already plastically compacts.  "Rod" = bonded **aggregate** with
  *breakable* bonds (structure fragmentation) — a different model; lower priority.

## 5. Rollout & validation (opt-in, doesn't disturb production)

- Flag `--fibre-rod` (default OFF → Tier-1 prescribed `curl=f(P)` stays the default until validated).
  When ON, **seed fibres ~straight** (`curl→0`) and let the rod buckle them emergently.
- GPU validation ladder (user's machine):
  1. **unit**: one fibre, axial compression, no SE → buckles at Euler `σ_cr` (mirror the numpy proof in
     Taichi; ratio≈1).
  2. **embedded**: VGCF-in-SE real run → fibres wrinkle at **short** wavelength (foundation), **porosity
     unchanged** (volume conserved, like Tier-1), morphology vs SEM.
  3. **STEP-3 payoff**: feed the buckled fibre geometry to the σ_e network (percolation/τ) → validate
     against **measured σ_e**.  ← the real reason to build it (not eyeballing).
- CFL note: XPBD removes the stretch-stiffness dt limit; expect ~K=5–20 constraint iters/substep, a
  modest per-step cost on the fibre points only (≪ the SE point count).

## 6. Sequence

Tier-1 (`curl=f(P)`, DONE) keeps STEP-1 porosity moving now.  Build `--fibre-rod` (XPBD) → unit-test on
GPU → enable for STEP-3 σ_e.  Tracked in `digest_model_application_backlog.md` §F2.
