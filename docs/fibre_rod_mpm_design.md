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

---

## RESULT (GPU, 2026-07-01) — buckling is DEM-territory, NOT MPM-scaffold

Ran `--fibre-rod` on input_6mAh_real_4 (VGCF 1 wt%, n_grid 256, scaffold, hold).  The rod compiled and
ran to completion on the GPU (no crash — the blind Taichi first cut works).  **But the fibres stayed
nearly straight, stiffness-independently:**

| --rod-stiff | fibre_straightness_mean | p10 (most-buckled decile) | buckled_frac (<0.9) |
|---|---|---|---|
| 0.6  | 0.997 | 0.999 | 0.7 % |
| 0.15 | 0.996 | 0.999 | 1.0 % |

Softening the bending stiffness **4×** changed nothing (0.997 → 0.996).  If the rod were too stiff to
buckle, 4× softer would have buckled markedly — it didn't.  ⇒ the limiter is **not** the rod
(stiffness/coupling hypothesis REFUTED); it is that **the fibres experience almost no axial compression**
in this framework.

**Why (frame[5]):** the scaffold bed compacts only ~2 %p (15.9 → 13.8 %) with the AM **frozen**, and that
densification is SE flowing into voids + the platen descending — the fibres are **advected (translated)**
by the smooth SE flow, not axially compressed along their length.  Real dramatic VGCF buckling comes from
**discrete particles pinching the fibre** as they rearrange — a **contact/DEM** phenomenon the continuum
SE (and the frozen AM) structurally cannot supply.  The rod is correct (numpy: compress → buckles at
Euler); the continuum MPM just never applies the compression.

**Verdict:** emergent fibre buckling is a **DEM/discrete** phenomenon, not a continuum-MPM one — confirmed
empirically by the stiffness-invariance test, a clean frame[5] boundary.  Practical consequence:
- **MPM** represents VGCF with the **Tier-1 prescribed curl** (as-grown waviness — avoids the ruler-
  straight artifact without forcing an unphysical buckle the framework can't drive).
- **Emergent buckling** belongs to a **DEM bonded-fibre + particle-pinching** model (needs pressurised
  DEM = LAMMPS; DEM/LIGGGHTS can't press) → parked as future work.
- `--fibre-rod` stays in the code (opt-in, verified to run) for a future framework that DOES supply fibre
  compression (mobile-AM MPM, or higher-strain protocols); it is not wrong, just un-driven here.

## SOLUTION (2026-07-01) — prescribed SEM-consistent buckle (`--fibre-buckle`)

Since the scaffold MPM can't compress the fibre to buckle it emergently, **prescribe the buckled shape a
real fibre would take** (Tier-1.5).  ⚠ **This is a SEM-consistent MORPHOLOGY KNOB, NOT a derived/validated
transport result** — see the "honest framing" caveats below (4-agent verification, 2026-07-01).
- **wavelength** λ = 2π(EI/E_SE)^¼ (Euler beam on a Winkler foundation): EI = 200 GPa·πr⁴/4 (real graphite),
  E_SE as the foundation modulus k_f → **λ ≈ 1.5 µm** (~6–7 *wavelengths* = **~13 half-waves** over a 10 µm
  fibre).  The ¼-power strongly suppresses the k_f uncertainty (k_f=E_SE omits a geometry factor ~1–3×, but
  λ moves only within ~1.0–1.6 µm).
- **amplitude** A = (λ/π)√ε_ax, with **ε_ax = `--buckle-strain`·cos²θ·(local AM fraction)**:
  - `cos²θ` (θ = fibre angle from press-z) → z-aligned fibres buckle most, in-plane ~straight.
  - **local AM fraction** (uniform_filter of the AM mask at ~fibre-length scale) → fibres in dense/pinched
    AM regions buckle more than those in open SE pores = the actual **particle-pinching driver** (verdict
    #3; the waviness is AM-POSITION-dependent, not spatially uniform).
  - `--buckle-strain 0.42` = the **fully-AM-confined** strain (a fibre pinched on all sides sees the macro
    bed strain).  The AM-fraction factor (~0.5 in interstices) reduces the EFFECTIVE mean to ~0.2 → mean
    straightness ~0.96–0.97, the SEM-consistent band — resolving the "0.42 is the macro not the fibre-axial
    strain" over-estimate *through the pinching mechanism* rather than an arbitrary lower number.

Validated — standalone (`seed_fibres`, AM-scaled) mean straightness 0.968 @ buckle_strain 0.42; **GPU
(input_6mAh_real_4, VGCF 1 wt%, AM-position-dependent): mean 0.9775, p10 0.94, 2 % bent** → a/λ ≈ 0.10,
the SEM band (0.10–0.20) lower edge.  AM-scaling raised the mean from the uniform 0.956 (open-pore fibres
straighten, buckling concentrates in dense-AM regions).  Raise `--buckle-strain` (→ ~0.55) to sit more
centrally in the band if a wavier mean is wanted.

### Honest framing (from the 4-agent verification — do NOT overclaim)
- **Formulas (λ, A) are real physics**: independently re-derived, self-consistent (straightness 0.930
  analytic / 0.943 MC / 0.945 code), quantitatively in the published CNT/CNF SEM a/λ band.
- **The absolute waviness is a KNOB, not "the physics"**: there is NO direct straightness/λ measurement of
  VGCF-H in a 300 MPa sulfide composite; the a/λ band is from *polymer* CNT/CNF (an upper bound for stiffer
  VGCF).  Real VGCF-H is stiff/straight; its in-electrode waviness is partly **as-grown manufacturing** +
  partly **discrete particle-pinching (DEM)**, not pure press-buckle.  So call it a *prescribed SEM-
  consistent morphology*, not a "physics-computed and validated buckle".
- **The shape is visualization/morphology, not transport, at production resolution**: amplitude A≈0.3 µm is
  **sub-voxel** (< 0.5 µm) and λ≈1.5 µm is ~3 cells → the buckled polyline rasterises to the same voxel
  thread as a straight fibre → **σ_e / tortuosity unchanged**.  Porosity/coverage unchanged (volume-
  conserving).  Do NOT cite a σ_e payoff unless a resolving grid (h≪0.3 µm) run shows one.
- VGCF only (PTFE stays a drawn web).  Recommended VGCF morphology in the MPM (supersedes the arbitrary
  Tier-1 curl=0.06) — as an honest SEM-consistent stand-in.

## COMPACTION-RESISTANCE (`--fibre-stiff`, 2026-07-02) — the DENSITY axis, not the SHAPE axis

Motivation (frame[4]): the verified volume-fill campaign makes porosity DROP ~linearly with additive
vol% (VGCF 2 wt% → −3.3 %p).  But the direct experimental anchor **Cho 2024** (same LPSCl SE + NCM811 +
VGCF 2 wt%, 433 MPa) shows porosity **FLAT-to-UP** (0.14→0.15, 0.18→0.19) with tortuosity rising — the
"conflicting roles" density penalty.  Real VGCF is a **compaction-RESISTING scaffold** (stiff graphite
E≈200 GPa, σ_y ≫ 0.3 GPa press → does not compress), NOT the passive void-filler the volume-fill assumes.
`--fibre-buckle`/`--vgcf-curl` are the SHAPE axis (volume-neutral, don't touch porosity); this is the
missing **stiffness/load** axis.

**Model (`--fibre-stiff`, mpm3d_compaction.py):** pin the VGCF-occupied grid cells rigid (v=0), unioned
into `am_mask` exactly like the frozen AM — the σ_y→∞, E→∞ limit of a stiff strut at 300 MPa (a 200 GPa
strut strains 0.15 % under 0.3 GPa ≈ rigid).  pin_np (AM coverage / AM_vol) is left untouched (VGCF gets a
separate tag 3); only the rigid-obstacle field changes.  The servo then reaches wallP=target at a HIGHER
wall_z where the load-bearing VGCF resists → larger height → porosity rises.  Percolation-gated by
construction: buried isolated VGCF doesn't reach the platen (no prop); only a floor→platen-bridging network
raises wall_z — physically the Cho/Reisacher percolation-onset behaviour.

**What it is / isn't (honest, mirrors the buckle framing):**
- It is the **UPPER bound** on the density penalty: fully rigid = no buckling relief.
- Crucially it still **cannot rearrange the frozen AM**.  The real prop-open has TWO halves: (a) the VGCF
  strut resists local compression (this lever captures it), and (b) the VGCF holds the whole AM skeleton
  apart so the AM settles LOOSER — that half lives in the DEM co-compaction (VGCF present when the AM
  jams) and the frozen-AM scaffold structurally cannot produce it (same frame[5] boundary as buckling).
- So `--fibre-stiff` tests **how much of the Cho density penalty the frozen-AM MPM scaffold can recover**
  from the strut-stiffness half alone.  If it flips porosity toward flat/up → the MPM captures the
  strut half; the residual vs Cho = the AM-rearrangement (DEM) half, quantified.  If it barely moves →
  the penalty is almost entirely AM-rearrangement → DEM co-compaction is the physical home (LIGGGHTS CAN
  pressurise — it is how the AM scaffold was made — so VGCF-as-stiff-clumps re-compaction is feasible).

**A/B test:** same VGCF wt% WITHOUT (volume-fill baseline) vs WITH `--fibre-stiff`, compare
`porosity_settled_pct` to the no-additive baseline (15.45 % MPM) and to Cho's direction.  ★ **Now
AUTO-baked for every VGCF recipe** in mpm_input_from_case.py (like `--fibre-buckle`) — VGCF as a
load-bearing strut IS the physical model, so the webapp/CLI zips always include it, no flag or sed
needed.  (`--fibre-stiff` CLI still force-enables it for a non-VGCF recipe.)  The pre-auto volume-fill
VGCF campaign numbers stay recorded for contrast.

### RESULT (GPU, input_6mAh_real_4 VGCF 4 wt%, n_grid 256, 2026-07-02) — direction ✓, mechanism ✓, magnitude modest → frame[5] confirmed

`--fibre-stiff` engaged cleanly: **2.39 M rigid load-bearing VGCF cells** = 8 vol% of solid, exactly
∝ the VGCF recipe volume (NOT over-connected by the binary_closing — 2.39 M / 8.3 M SE cells = 29 % =
VGCF/SE volume ratio 8/27.9 %).

| VGCF 4 wt% | porosity | thickness | SE plastic strain Σdg (mean) | total strain (mean) | cov AM_S |
|---|---|---|---|---|---|
| volume-fill (soft) | 8.63 % | 112.87 µm | (normal compaction) | — | 52.5 % |
| **+ --fibre-stiff** | **9.38 %** ↑ | 113.80 µm | **0.026 → 0.001** | 0.195 → 0.006 | 50.5 % |
| no-additive baseline | 15.45 % | — | — | — | — |

- **Direction ✓ (Cho):** porosity **8.63 → 9.38 % = +0.75 %p UP** — the conflicting-roles sign, opposite
  to the volume-fill drop.
- **Mechanism ✓ (the real value):** the SE plastic strain is **crushed** (Σdg 0.026 → 0.001; total strain
  0.195 → 0.006) — the rigid VGCF network **props the bed so the SE cannot plastically densify** → bed
  thickens (+0.9 µm) and SE conforms to the AM less (cov AM_S 52.5 → 50.5).  These are exactly the
  "conflicting roles" density-penalty signatures, emergent from the load-bearing physics.
- **Magnitude modest:** +0.75 %p recovers only **~11 %** of the 6.8 %p volume-fill error (would need ~+7 %p
  to reach the no-additive 15.45 % that Cho's flat-to-up implies).  Cause: the frozen AM already fixes
  `wall_z`; the VGCF sits in the interstitial void and only props the near-wall gap — it **cannot push the
  AM skeleton itself apart** (frozen).  That AM-rearrangement is the dominant half.

**Verdict (frame[5], mirrors the buckling stiffness-invariance test):** even the STRONGEST MPM lever
(fully-rigid VGCF = the σ_y→∞ upper bound) recovers only ~11 % of the porosity penalty → the penalty is a
**packing / AM-rearrangement phenomenon = DEM's domain**, empirically proven, not asserted.  The MPM
scaffold correctly owns the **direction + mechanism** (strut resistance → SE can't densify); the
**absolute magnitude** belongs to DEM co-compaction (VGCF present when the AM jams → looser skeleton).
Caveats: fully-rigid = stiffness upper bound; a mild first-contact wallP transient may inflate the stop
slightly (the scaffold disables the arm-guard) — both would only make the strut half SMALLER, reinforcing
the verdict.  Optional lower bracket: a softened-E elastic VGCF (vs fully-rigid) would sit below +0.75 %p.
⇒ `--fibre-stiff` is the physically-correct VGCF STIFFNESS model for the MPM (direction + mechanism +
morphology); report porosity as the frame[5] bracket [volume-fill 8.63 % … strut-corrected 9.38 %], with
the DEM packing half named as the remainder.  Production porosity-incl-additive stays with DEM (frame[5]).
