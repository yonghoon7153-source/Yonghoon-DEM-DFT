# 3D MPM compaction — calibration & composite finding (2026-06-16)

Production 3D MPM = `scripts/mpm3d_compaction.py` (MLS-MPM, von Mises J2, GPU/Taichi).
The 3D companion to the 2D champion.  This file records the three fixes that made
the 3D servo behave, the pure-SE calibration to our Minnmann anchor, and the
composite result + its honest limit.  Anchors used here are OURS (Minnmann pure-SE
~10 % @ 300 MPa; our rigid 3D DEM composite 36–41 %; de Larrard geometric ~20 %).

## Production parameters (LOCKED)
| param | value | meaning |
|---|---|---|
| E_SE | 1.53 GPa | softened Young's (shear-softening proxy) |
| **ν_SE** | **0.49** | → **K_SE = 25.5 GPa ≈ real LPSC bulk (24)**; μ_SE = 0.51 GPa (soft shear) |
| σ_y (SE) | 0.30 GPa | von Mises yield (top of LPSC lit range 0.05–0.30) |
| E_AM / ν_AM | 140 / 0.30 | AM ~rigid (no yield) |
| target | 0.30 GPa | servo platen axial stress (= 300 MPa) |
| readout | wallP | platen reaction stress (default) |

These are the **defaults** in the script.  Pure-SE: `--material SE`.  Composite:
`--material mix --am-frac <vol AM of solid>`.

## The three fixes (the core of this session)
The first GPU runs over-compressed pure-SE to **0 % porosity** (the wall crushed the
bed before the stress reached target).  Three independent problems, three fixes:

**(1) wallP readout — the servo signal.**  The servo had been driven by the
volume-mean Cauchy σzz (`Σ −P[2,2]/J / n`).  That mean is **resolution-biased**: a
well-resolved soft SE dilutes it, so the platen keeps descending past target (the same
"512 blocker" the 2D matcher hit).  Direct evidence from a soft-bulk run: once dense,
**wallP = 1.08 GPa while the volume-mean σzz read only 0.09 (12× dilution)**.
NEW **wallP = Σ_{platen nodes} m·(v_trial − v_wall) / (dt·area)** = a boundary
force balance ≈ constitutive stress (GPa), resolution-invariant, and the TRUE
experimental BC (press AT the target).  Default servo signal; `--readout sigzz`
keeps the old one.  (Both printed every frame.)  NB at static settling wallP→0
(momentum reaction needs motion) → use the `porosity@target` readout below.

**(2) ν_SE stiff bulk — the over-crush fix.**  Root cause of the 0 %: the 18× E
softening (24→1.53) softened the **bulk** modulus too.  At ν=0.30, E=1.53 →
**K = 1.27 GPa**, so at 0.30 GPa the SE compresses ~20 % volumetrically (J→0.8) =
unphysical (real LPSC K ≈ 24 GPa, near-incompressible at 0.3 GPa).  Fix = raise the
SE Poisson ratio so the BULK is stiff while the SHEAR stays soft (= volume-preserving
granular flow).  GPU ν-sweep (pure-SE, σy=0.15, n_grid=256):

| ν_SE | K_SE | porosity@target |
|---|---|---|
| 0.45 | 5.1 GPa | **0.00 %** (still over-crushes) |
| 0.49 | 25.5 GPa | **6.32 %** ✓ (stops at physical porosity) |

⇒ K must be ~real (≈25) to stop the crush.  This is the **3D mirror of the 2D
CORRECTION 1** (`--nu-se`): only the SHEAR softening is the granular-rearrangement
proxy; softening the bulk was an unintended side effect.  Physical reading: SE bulk =
REAL (24 GPa), only the shear yields/rearranges.

**(3) servo arm-after-compaction guard — the composite fix.**  In the composite a big
rigid AM hitting the platen on first contact spikes wallP transiently, which tripped
the `p≥target` stop at frame ~13 while wallP was really ~0 → the servo armed
prematurely and crawled at the fine bidirectional step → **under-compacted (ended ~40 %,
never reached 0.30 GPa)**.  Guard (2D-proven): refuse to arm the stop until the bed has
actually compacted (**porosity ≤ por0 − 5 %p**), so the first-contact transient is
ignored and the fast descend continues to the real target.  Pure-SE is unaffected
(no big-AM transient; it compacts well past the guard before target).

Also added `porosity@target` (porosity at the frame the target stress is FIRST
reached) so an overshooting/oscillating servo cannot corrupt the reported value.

## Pure-SE calibration → Minnmann ✓
With ν=0.49 (K=25.5), σ_y sweep (n_grid=256, GPU, settled porosity):

| σ_y (GPa) | porosity | |
|---|---|---|
| 0.15 | ~5.6 % | |
| 0.20 | ~6.7 % | |
| 0.25 | ~9.0 % | |
| **0.30** | **~10.0 %** | ✓ **= Minnmann 300→10 %** |

⇒ **E=1.53, ν=0.49, σ_y=0.30 → pure-SE 10 % @ 0.30 GPa.**  σ_y=0.30 is the top of the
LPSC single-crystal yield range (physical).  3D needs a stiffer shear than the 2D
champion (σ_y=0.15) because the extra flow direction densifies more — a geometric
2D↔3D difference, not a model change.  Bonus consistency: at ν=0.49, **wallP ≈
volume-mean σzz** (uniform internal stress when incompressible) → the readout question
closes (the 12× divergence only happened with the soft bulk).

## Composite — plastic densifies below rigid DEM; absolute is packing-limited
n_grid=256, ν=0.49, σ_y=0.30, default sizes r_am/r_se = 0.045/0.018 (**2.5:1**),
settled porosity:

| am_frac (= vol% AM of solid) | MPM porosity | our rigid 3D DEM |
|---|---|---|
| 0.5 | **27.6 %** | 36–41 % |
| 0.6 | **33.2 %** | 36–41 % |

- **Trend ✓**: 0.5 (27.6) < 0.6 (33.2) — more SSE → denser (correct composition direction).
- **Plastic < rigid DEM** (27.6 vs 36) — plastic flow void-fills ~8–10 %p that the rigid
  sphere cannot.  This **quantifies** the DEM↔MPM gap: the plastic continuum reaches a
  density the rigid-sphere DEM structurally can't.
- **BUT the absolute is still high** and is dominated by the **size ratio**, not the
  plasticity.  At 2.5:1 the small SE cannot reach into the large-AM interstices; the
  real powder is 12:4:1 (much smaller SE → far better geometric void-filling).  At
  n_grid=256 the real ratio is unresolvable (SE would be <1 cell), so the run is a
  *poor-packing* lower bound.

**Honest frame [5] conclusion:** composite absolute porosity = **geometric packing
(real size ratio; de Larrard / DEM domain) × plastic flow (MPM domain)**.  The MPM has
the plastic flow but not the real-size packing (resolution-capped); de Larrard/DEM has
the packing but (rigid) no plastic flow.  Neither alone hits the dense composite —
both halves are needed.  → for composite ABSOLUTE porosity use real-size packing;
the MPM owns the *plastic densification increment* and the *composition trend*.

## Do / don't
- DO use the locked defaults (1.53 / 0.49 / 0.30) for pure-SE — Minnmann-matched.
- DO read `porosity@target` and `porosity(settled)`; ignore the static-settling wallP→0.
- DON'T lower ν_SE below ~0.49 — K drops, the bed over-crushes to 0 % (proven at 0.45).
- DON'T chase the composite ABSOLUTE with this size ratio — it is packing-limited, not a
  plasticity limit; needs the real 12:4:1 ratio at higher n_grid (GPU-heavy) and even
  then the absolute is owned by de Larrard/DEM, not the resolved-grain MPM.
- The MPM's deliverables here: pure-SE Minnmann anchor + the plastic-vs-rigid
  densification increment + the composition trend (50<60).  Transport σ stays with DEM.

## Tooling (scripts/mpm3d_compaction.py)
`--readout {wallP,sigzz}`, `--nu-se`, `--sigma-y`, `--am-frac`, `--n-grid`,
two-tier RSA build, MLS-MPM J2 return map, servo (descend + arm-guard + fine
bidirectional), wallP reaction accumulator, `porosity@target` capture.
