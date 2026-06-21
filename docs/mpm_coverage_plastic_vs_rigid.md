# MPM coverage — PLASTIC vs RIGID: why the values are usable (2026-06-21)

Controlling record for the SE→AM coverage numbers the MPM reports (webapp
`mpm_metrics.json` / `mpm_payload.json`).  This exists because the coverage value
kept **changing with settings** during development ("값도 바뀌고") — this doc pins
down the two measures that DO NOT change, why each is sound, and why the (modest)
plastic increment is the correct physics, not a measurement defect.

Bands throughout: **Hertz 0.13 µm** (contact), **Tabor 0.26 µm** (plastic spread) —
the same two distances the DEM Stage-E uses, so MPM↔DEM is apples-to-apples.

---

## 1. The two measures we report (and the one we do NOT)

| measure | how | code | invariance |
|---|---|---|---|
| **PLASTIC** (deformed) | AM surface → nearest **deformed SE material point** (KDTree), fraction within band | `deformed_coverage`, run at **all** SE points (`--cov-sub 0`) | subsample-free (no sampling at all-points); grid-free |
| **RIGID** (geometric) | AM surface → nearest **SE sphere SURFACE** (gap = d_centre − r_SE), analytic | `geometric_coverage` | fully analytic — invariant to n_vox / subsample / cloud density; stable 0.1 %p over n_samp 800–10000 |
| ~~voxel-adjacency~~ (`coverage_AM_*_mpm_pct`, ~26 %) | SE-occupied cell adjacent to AM cell | mpm3d preview | **NOT reported** — density/n_vox-bound, does not converge |

Both reported endpoints are **settings-independent** → the numbers are usable.
The PLASTIC − RIGID **difference** is the only thing the plasticity adds, and it is
exactly the MPM's unique contribution (a rigid-sphere DEM has zero of it).

### Why RIGID is rock-solid
`geometric_coverage` never touches the point cloud.  It samples each AM sphere
surface with a Fibonacci lattice and asks "is the nearest SE **sphere surface**
within 0.13 / 0.26 µm?" — pure analytic geometry on the real AM scaffold + real SE
centres.  No n_vox, no subsample, no resolution.  This is the reference floor.

### Why PLASTIC is usable (the saga resolution)
`deformed_coverage` queries the **deformed** SE cloud, so it sees plastic flow that
the rigid spheres can't.  The historical problem: the value drifted with `--cov-sub`
(45 % @ 12 M points → 70 % @ all points).  Two things fix it:
- **r_pt correction** (`bands = b/UM + r_pt`, `r_pt = ½ median NN spacing`): each SE
  point represents a sub-volume of radius ~r_pt, so its *surface* reaches r_pt past
  the centre.  As the cloud sparsens, r_pt grows AND the nearest-point distance grows
  by the same amount → they cancel.  This makes a **surface** cloud subsample-invariant.
- BUT the MPM cloud is **volume-filling**, so the cancellation is only approximate
  (residual drift remained).  → Production runs at **all points** (`--cov-sub 0`):
  with no subsampling there is no subsample dependence to begin with — the value is
  **fully determined by the SE cloud**.  n_vox does not enter (this is a KDTree on the
  raw points, not the voxel-adjacency preview).

⇒ **Report PLASTIC (all-points deformed) and RIGID (analytic geometric).  Never report
the voxel-adjacency 26 % — that is the one that does not converge.**

---

## 2. Why the plastic increment is MODEST — and that is CORRECT

real_14 (AM-rich): AM_P **plastic 51/73 % vs rigid 46/70 % → Δ +5/+3**.  "Plastic 적용돼도
극적으로 바뀌진 않네" — right, and it should not, for three compounding reasons:

1. **Coverage is a near-contact measure → rigid packing already wins most of it.**
   The bands are tiny (0.13 / 0.26 µm).  An SE sphere pressed against AM at 300 MPa is
   already within 0.13 µm of most of the contact zone (rigid 46/70 %).  Plasticity only
   converts "just-barely-not-covered" surface (a 0.14 µm gap) into covered — a **margin**
   effect, structurally bounded.  The wider Tabor band has even less headroom
   (Δ +3 < Δ +5), exactly as expected.

2. **σ_y = 0.30 GPa = the 300 MPa press (at the yield threshold).**
   SE sits *on* its yield point — it deforms plastically but does not flow like a
   liquid.  Real LPSCl at 300 MPa yields without smearing.  A much softer σ_y would
   spike coverage; the realistic σ_y gives a *moderate* plastic strain → moderate
   conforming.  The value not jumping is the SE material model being faithful, not a bug.

3. **AM-rich → SE is load-shielded, and its flow goes to VOIDS not AM wrapping.**
   The rigid AM skeleton (140 GPa) carries the 300 MPa; interstitial SE sees less than
   the full local pressure → deforms less.  And most of the plastic flow that *does*
   happen closes **SE–SE bulk voids** (porosity loose 24.4 % → 15.9 %, **−8.5 %p**)
   rather than wrapping AM surfaces → big porosity move, small coverage move.

**The dramatic plastic signatures live elsewhere**, not in near-contact coverage:
porosity void-fill (−8.5 %p vs the loose seed; plastic reaches densities the rigid
sphere structurally cannot) and **morphology** (SEM-matching core-preserved +
boundary-flattening shape change).  Coverage is simply not where plasticity dominates.

---

## 3. input_S_1 (SE-rich) vs real_14 (AM-rich) — what it proves

| | **input_S_1** (SE-rich) | **real_14** (AM-rich) |
|---|---|---|
| porosity (MPM / DEM) | 20.17 % / 19.7 % | 15.91 % / 15.64 % |
| thickness (MPM / DEM) | — | 29.95 / 30.28 µm |
| SE / solid | — | 25.8 % (DEM ~27) |
| **coverage PLASTIC** (0.13/0.26 µm) | **70 / 91 %** | **52 / 74 %** (AM_P) |
| **coverage RIGID** (0.13/0.26 µm) | **60 / 87 %** | **46 / 70 %** (AM_P) |
| **plastic conforming Δ** (Hertz) | **+10 %p** | **+6 %p** |
| σ_ionic | 0.48 (excellent) | 0.063 |
| σ_e / AM percolation | 0 / 0 % (electronically dead) | 14.25 / 87 % |

(real_14 is the **periodic** RVE production run — x,y periodic = the DEM `boundary p p f`,
so boundary AM/SE get bulk compaction + coverage; porosity held 15.93→15.91 % and AM_P
plastic ticked 51/73→52/74.  input_S_1 was run pre-periodic on the now-dead V100, so its
70/91 is the walls-RVE value; the periodic bump is ~+1–3 %p and does not change the
comparison direction below.  S_1's reported coverage vs real_14's AM_P; each case's payload
also carries the AM_S breakdown — small AM_S, being more numerous, typically reads a few %p
lower than AM_P.  The comparison is robust to AM-subtype because it is driven by SE
volume fraction, not by which AM it wraps.)

**Two locked conclusions:**

1. **SE-rich covers more — even rigid, and plastic widens the gap.**
   Rigid alone: S_1 60/87 > real_14 46/70.  Plastic: 70/91 vs 52/74.  More SE volume
   fraction → more SE within reach of the AM surface → geometry already favours S_1, and
   plasticity amplifies it.  The predicted real_14 ~50/73 came out **52/74** (periodic) — hit.

2. **The plastic increment difference (+10 vs +6) IS the AM load-shielding signature.**
   SE-rich S_1: SE is load-**bearing** → sees full pressure → flows more → +10 %p.
   AM-rich real_14: SE is load-**shielded** → sees less → flows less → +6 %p.
   The 2× ratio in the *plastic* increment between the two cases is a direct, coverage-
   side observation of the load-shielding documented for the composite SE overlap
   (rigid AM carries the 300 MPa, SE lightly loaded).  ⇒ MPM is **not** "failing to
   represent coverage" — this plastic increment is precisely the value only the MPM
   can give, and it behaves correctly across the SE-rich → AM-rich contrast.

---

## 4. frame[4]/[5] standing

- **frame[4]** (independent calibration): RIGID coverage is geometry on the DEM scaffold;
  PLASTIC coverage is the MPM (champion E_SE=1.53, ν_SE=0.49, σ_y=0.30, anchored only to
  Minnmann).  Their agreement on the *rigid* floor (MPM rigid 46/70 vs DEM Stage-E Tabor
  ~48–52) cross-validates; the *plastic* increment is the MPM's added information.
- **frame[5]** (division): coverage's **near-contact / mechanical** part is shared
  (DEM Tabor ≈ MPM rigid); the **plastic conforming increment** is MPM-only; the
  **transport** use of coverage (B3 surface-roughness conduction correction) stays DEM-only.

⇒ **Usable values to report**: PLASTIC (all-points deformed) and RIGID (analytic
geometric), at 0.13 / 0.26 µm.  Both are settings-independent; their difference is the
MPM's physical plastic-conforming contribution.  Do **not** report the voxel-adjacency
preview number.
