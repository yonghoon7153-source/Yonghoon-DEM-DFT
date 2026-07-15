# Voxel σ solver ↔ DEM network solver — frame[4] cross-validation (AMS_S1)

Stage-2 image-based voxel FV conductivity (`scripts/voxel_conductivity.py`) vs the production
DEM Kirchhoff/Holm network solver, on **input_1mAh_8_AMS_S1** (P:S 0:10, AM:SE 85:15, 378 AM_S
@2.5µm + 19971 SE @0.5µm, 300 MPa).  This is the controlling record for what the voxel σ tool
does and does NOT capture — do not lose to compaction.

## The headline result — voxel electronic reproduces DEM σ_full; voxel ionic reproduces only σ_contact-free (the UPPER BOUND, NOT production σ_ionic)

| channel | voxel σ (this tool) | DEM dashboard | reproduces |
|---|---|---|---|
| **electronic** | 2.67→4.03→5.19 (128/192/256), geometric extrap **11.76** | σ_full = **11.75** mS/cm | ✓ σ_full |
| **ionic** | 0.299/0.250 (192/256, `--porosity 0.174`) → **0.250** | σ_contact-free = σ_full·5.8 = 0.0436·5.8 = **0.253** mS/cm | ⚠ only σ_contact-free (= upper bound), NOT σ_ionic |

⚠ The ionic row is NOT "the voxel reproduces DEM ionic transport".  The voxel matches the **contact-free
upper bound** (0.25), while the **production σ_ionic = DEM 0.0436** (constriction-limited) — see line "Production
σ_ionic = DEM …" below; the voxel value is ~5.7× too high and is NOT a usable σ_ionic.
- The DEM dashboard reports **σ_contact-free / σ_full = 5.8×** (this is `R_brug_over_full` = σ_cf/σ_full) for the
  ionic channel (σ_ionic Hertz 0.0436, Physics 0.031 mS/cm).  (Separately, the per-edge mean **constriction-
  resistance fraction = 77.5 %**; these are TWO DIFFERENT decompositions — a 5.8× σ_cf/σ_full ratio ⇒ ~83 % of
  the SERIES resistance is constriction, while 77.5 % is the per-edge average.  Do not read 5.8× and 77.5 % as
  the same measurement.)
- voxel_ionic / DEM_σ_full = 0.250 / 0.0436 = **5.7×** → independently reproduces the dashboard's 5.8×
  σ_contact-free/σ_full factor.  The voxel lands on σ_contact-free almost exactly — confirming it captures the
  GEOMETRY but NOT the sub-voxel SE constriction.

## Why electronic matches σ_full but ionic matches σ_contact-free — CONTACT SIZE

The voxel fills each phase into cells and connects them face-to-face (harmonic-mean face
conductance).  It therefore captures the constriction of a contact **only if the contact neck is
resolvable** at the voxel pitch; otherwise it over-connects (full face area, no constriction).

- **electronic = AM network** (rigid AM_S, r=2.5µm → large AM-AM overlap necks).  The neck is many
  voxels wide → **resolved** → the voxel's geometric constriction ≈ the real Holm constriction →
  voxel electronic converges to **σ_full (11.75)**.  (3-pt geometric extrapolation 2.67/4.03/5.19,
  increment ratio 0.85 → Σ → 11.76.)
- **ionic = SE network** (SE r=0.5µm → tiny point contacts, ⟨A_hop⟩=0.065 µm², bottleneck
  0.0025 µm²).  At n_vox=256 the electrode is 17.8µm/93 ≈ 0.19µm/cell and a 0.065µm² contact is
  ~1 cell across → **sub-voxel / unresolved** → the voxel connects SE cells full-face with NO
  constriction → voxel ionic = **σ_contact-free (0.25)**, i.e. 5.8× the real σ_full.
  Resolving the SE constriction would need n_vox ≫ 1000 (impractical).

## frame[5] consequence — DEM owns σ_ionic; the voxel is the continuum reference

σ_ionic is dominated by **granular SE point-contact constriction** (77.5 % of the ionic
resistance here) — a DISCRETE contact-network phenomenon.  The DEM Kirchhoff solver with Holm
constriction R = 1/(2σ·a) captures it natively; a continuum/voxel FV structurally cannot (it has
no sub-voxel contact area).  This is exactly the "DEM = TRANSPORT" division: the explicit contact
network owns the constriction-limited σ.

- **Production σ_ionic = DEM 0.0436 mS/cm (Hertz) / 0.031 (Stage-E Physics).**  NOT the voxel value.
- The voxel's value is the **contact-free continuum σ** (an upper bound); its only transport use is
  (a) the electronic cross-check (matches σ_full because AM contacts are resolvable), and (b)
  quantifying the constriction overhead as voxel_ionic/DEM_full (= 5.7× ≈ dashboard 5.8×).

## How to run the voxel σ (settled recipe)

```
python3 scripts/voxel_conductivity.py --se se_carbon.npy --phase phase_carbon.npy \
  --scaffold am_carbon.csv --n-vox 256 --porosity <MPM void frac, e.g. 0.174>
```
- `--porosity` is REQUIRED for a stable ionic read: the SE MPM cloud is not space-filling, so the
  bare "≥1 point/cell" occupancy fragments and σ_ionic spuriously → 0 as n_vox rises.  Filling SE
  to its true fraction as the densest CONTIGUOUS region (target_porosity) is resolution-stable
  (ground-truth analytic free-space SE = 1.90 flat across 128/192/256; a dense point cloud with
  --porosity reproduces it).  n_vox ≥ 192 (128 under-resolves the SE necks).
- `--se-close` is opt-in (default off); --porosity alone already matches ground truth, closing
  slightly over-fills.
- ionic WITHOUT==WITH (gain 1.0×) by design — a single-structure σ-toggle cannot isolate the CBD
  ionic blocking (carbon blocks SE equally in both columns); use a structural no-CBD vs +CBD run.
- electronic high-contrast solve (carbon 1e5 vs AM 50) is kept fast/robust by a 200× contrast cap
  + Jacobi-preconditioned CG (per-channel envelope trim places the Dirichlet faces on the
  conducting phase's own z-extent so an AM-on-floor scaffold doesn't zero σ_ionic).

## Debugging history (all fixed inside the voxel tool, in order)

1. **σ_ionic = 0** — Dirichlet faces pinned to the box floor where the rigid AM rests (SE never
   touched the bottom face).  Fix: per-channel envelope trim.
2. **electronic CG stall** — carbon/AM 2000–10000× conductivity contrast → ill-conditioned.  Fix:
   200× contrast cap (a phase ≥200× its neighbour is already a perfect bridge, <0.2 % σ effect) +
   Jacobi preconditioner; CG rtol 1e-8→1e-6.
3. **σ_ionic disconnects at high n_vox** — SE point cloud not space-filling.  Fix: `--porosity`
   (densest-contiguous target_porosity fill).  Validated against an analytic ground truth.
4. **glitchy carbon→SE ionic toggle** (σ_without < σ_with, impossible 7.6×) — removed; ionic CBD
   blocking is a structural comparison, not a σ-toggle.

## AMS_S1 reference numbers (DEM dashboard)

porosity 21.1 % (ε_union 22.5), thickness 17.84µm, φ_SE 0.235, ⟨z_SE-SE⟩ 3.86, SE percolation
97 %, τ_Dijkstra 2.35, τ_Laplace,eff 4.01 (Hertz)/4.77 (Physics).  σ_ionic 0.0436/0.031,
σ_e 11.75/8.28, κ 5.315/4.560.  Bruggeman EMT σ_ionic 0.124 (R_brug 5.8× vs network).
MPM (n_grid 384, hold): porosity 17.86 %, thickness 16.89µm, SE 28.6 % of solid, cov_AM_S
plastic/rigid Tabor 70/64 %.

## ⚠ The `--se-id` contact-network mode (se_contact_network) — EXPERIMENTAL, currently OVER-COUNTS

`scripts/voxel_conductivity.py --se-id` builds an SE-PARTICLE network from the MPM `--save-se-id` (Voronoi-
tagged particle ids): voxelise SE per-particle, take the contact area between touching particles, Holm
constriction, Kirchhoff.  Intent: an independent, plastic-deformed-contact σ_ionic.  **Status: it over-counts
and is NOT a usable σ_ionic** — keep for diagnostics only.

- The space-filling Voronoi partition makes neighbouring particles share their FULL mutual facet, so the
  "contact area" = the Voronoi facet, NOT the small plastic contact disk.  Facet ≫ real neck → r_c too large
  → constriction too small → σ_ionic ≈ **0.88** on real_10-class cases, which is ABOVE even the contact-free
  fused-FV (0.25) and ~20× the DEM full (0.044).  The ordering 0.88 > 0.25 > 0.044 is the tell-tale: it
  under-resists MORE than the no-constriction limit.
- Even a corrected interpenetration/overlap-based contact area (DEM-style δ/R* plastic film) cannot rescue it:
  the SE neck (⟨A_hop⟩≈0.065 µm², bottleneck 0.0025) is SUB-VOXEL at any practical n_vox (cell ≈0.19 µm at
  256; recommended n_vox ≫ 1000), so the voxel contact area saturates at ~1 cell² ≫ the real neck.
- **frame[5] holds**: σ_ionic constriction belongs to the DEM contact network (Holm), period.  The voxel-
  contact variant is at best a coarse UPPER bound + a contact-area diagnostic — NOT an independent σ_ionic.
  (The code docstring + CLI print now carry this caveat; production σ_ionic stays the DEM value.)
