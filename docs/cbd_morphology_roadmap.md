# CBD / conductive-additive morphology roadmap (PTFE + carbon)

**Controlling status doc for the conductive-additive (VGCF / Super P / PTFE) morphology
work.  DO NOT lose this to context compaction — the user explicitly said "1,3은 잊으면
안돼!" (2026-06-24).**  Tools: `scripts/additives.py` (seeding), `scripts/mpm3d_compaction.py`
(`--add-recipe`, `--save-phase/--save-fibre/--save-fibre-dia`), `scripts/mpm_webapp_payload.py`
(`--phase/--fibre/--fibre-dia`), `webapp/static/js/viewer3d.js` (`buildCarbonOverlay`),
`scripts/mpm_input_from_case.py` (bakes the flags into run_mpm.sh).

## The physical picture (literature-grounded)

PTFE dry-electrode binder fibrillates by roll/shear DRAWING into a hierarchical, tangled
**fibril web** that NETS the carbon + active material → the **Carbon-Binder Domain (CBD)**.
Lit (Frontiers 2023 fenrg.2023.1336344; RSC EES 2025 d5ee03240g; Powder Tech 2024
S0032591024010957; Nat. Comm. Mater. 2025 s43246-025-01046-0; J. Power Sources 2025
S0378775325029842): primary fibrils few-µm Ø, 100s-µm long → branch into secondary →
finer fibrils down to 10s nm; web-like; over-shear → collapse to FILM; branch-like, does
NOT block pores.  **Length↔Ø inverse** = constant-volume drawing: A=V/L → d ∝ √(V/L)
(longer ⇒ thinner).  Initial PTFE particle SIZE has a distribution → V_i varies too.

> ★ **SAME-SYSTEM EXPERIMENTAL VALIDATION — Lee 2025, Nat. Commun. 16, 4200** (UCSD+LGES; digest
> `litdb/papers/lee2025_corolling_dryprocess_lpscl_ptfe.md`).  EXACTLY our materials: **LPSCl + NCM811/82 +
> VGCF + PTFE (<300 nm)**.  Their **Fig 3h,i + Supplementary Fig 17/18** show by SEM a **"fibrillated
> binder–VGCF network"** bridging the SSE–electrode interface, and the Fig 3i / SI Fig 18a schematics draw it
> as **tangled squiggly curved fibrils netting the VGCF** — i.e. our (1) curl(worm-like) + (4) nucleate-on-carbon
> picture, literally.  SI Fig 18a gives a 5-step fibrillation mechanism (contact → shear particle-movement +
> binder stress → binder **stretched & fibrillated across interface** → new contacts → repeat每 reduction step) =
> our shear-DRAW seeding (3, d∝√(V/L)).  PTFE initial particle <300 nm = our V_i seed-size distribution (2,vol_cv).
> CAVEAT: their fibrillation is the *film-roll-shear fabrication* step, which our RVE does not reproduce — use as
> CONCEPT/morphology validation, not a claim our sim runs that shear.  Also Lee 2025 SI Fig 5: PTFE 0.5→5 wt%
> collapses σ_e 34→0.011 + σ_i 0.069→0.007 mS/cm → the **binder insulation/contact-blocking penalty** (Stage-2
> σ_e correction; today's CBD only ADDS σ_e via the carbon web, no binder penalty).

## The 5-physics PTFE model — status

### ✅ DONE (batch 1, commit e2c9371, 2026-06-24) — verify with run real11_VGCF_PTFE_v2
1. **curl (tangled web)** — PTFE path = persistent random walk (worm-like, curl=0.4);
   VGCF stays straight (curl=0, a real graphite fibre is stiff).  `seed_fibres(curl=…)`.
2. **vol_cv (initial node-volume spread)** — V_i lognormal (vol_cv=0.6): real PTFE
   particle/agglomerate size distribution.  `seed_fibres(vol_cv=…)`.
3. **vol_conserve (drawing d∝√(V_i/L_i))** — each fibril conserves its OWN V_i while drawn
   to L_i → two independent spreads (V_i × L_i) ⇒ diverse fibres (thick short stub … thin
   long strand).  Per-point volume weight ∝ V_i/L_i, ×add_pvs preserves recipe volume.
4. **nucleate on carbon (CBD co-location)** — nucleate_frac=0.6 of PTFE fibrils START on an
   already-seeded VGCF/SuperP point → binder web nets the carbon instead of floating in
   void.  `seed_fibres(nucleate=carbon_pts, nucleate_frac=…)`; carbon seeded BEFORE PTFE
   (ADD dict order VGCF→SuperP→PTFE).
5. **thickness viz** — per-point Ø ∝ √weight saved (`--save-fibre-dia`), per-fibre median
   `d` carried to payload (`--fibre-dia`), viewer renders thickness as BRIGHTNESS (thick
   solid, thin faint; WebGL line width is unreliable).

### ✅ DONE (batch 2, 2026-06-24) — re-run VGCF+PTFE to view (with --void-max for the pore view)
2. **branching (1차→2차 hierarchy)** — `seed_fibres(branch_frac=0.5, branch_n=2, branch_vol=0.3,
   branch_len=0.5)`: a primary spawns ≤2 thinner secondary fibrils from points along it (child V =
   branch_vol·V_parent, L = branch_len·L_parent → child d ∝ √(V/L) smaller).  Children are separate
   fibre ids (own `d`).  Smoke test: 300 primaries → ~500 fibres (+200 children), weight mean 1
   (recipe volume preserved by the normalisation), per-fibre Ø spread widens at the thin end.
4. **directed particle→particle bridge** — `seed_fibres(bridge_frac=0.5, bridge_drift=0.15)`: a fibril
   nucleated on one carbon point picks a NEARBY 2nd carbon (within ~1 fibre length) and STEERS its
   walk toward it (drift term in `_grow`), so it CONNECTS two carbon clusters instead of wandering —
   the binding action Lee 2025 SEM shows (binder fibrils fibrillated ACROSS the interface).
   PTFE ADD-dict in mpm3d_compaction.py now (curl0.4, vol_cv0.6, nuc0.6, branch0.5, bridge0.5).

### 🚩 DEFERRED — different category, NOT "just forgot" (the user's ①③ — KEEP)
1. **internal nano-porosity (CBD dual-porosity, 50-70% dense)** — CBD nano-pores 10-100 nm
   are SUB-GRID at dx≈0.19 µm (n_grid 266 / 50 µm box) → cannot be seeded as explicit pores
   on this grid.  Belongs to **Stage 2** (CBD as a homogenised porous phase → effective σ
   with internal tortuosity/porosity via Bruggeman on the CBD sub-scale), OR a **synthetic
   CBD-envelope** architecture (define a CBD domain larger than the solid, fill ~60%).
   Decision (envelope vs Stage-2 effective-σ) is OPEN — revisit at Stage 2.
3. **over-fibrillation → film** — high-shear FAILURE regime (web collapses to a film if
   shear > PTFE tensile strength).  Not the normal morphology → add as an optional
   `--film` toggle later, do NOT bake into the default web.

## Recipe / convention (unchanged)
additive = wt% of the 100% electrode; AM:SE from the REAL scaffold (recipe AM:SE ignored).
"AM:SE:VGCF:PTFE=80:18:1:1" → VGCF 1 + PTFE 1 wt% (AM:SE fill 98%).  per-point pvs =
recipe_vol_share so additive occupies its real volume regardless of point count.

## Why carbon helps (target cases)
VGCF/SuperP boost **σ_electronic** (dead-AM: low/ poorly-connected or FRACTURED AM electronic
network — e.g. the 92:8 8mAh cases where AM_P pulverises 37-40 % and σ_e Physics hits the
Bruggeman fallback).  They do NOT fix **σ_ionic** (dead-SE: thin/fragmented SE network — the
0:10 and 92:8 ionic-bottleneck cases).  PTFE is the binder (mechanical + CBD), not a conductor.

## Stage 2 (the real payoff, pending)
Voxel σ solver on the seeded morphology → quantify "도전재 넣으니 dead-AM 살아나 σ_e ↑".
This is where CBD nano-porosity (#1) enters as the CBD phase's effective transport property.

## ★ SuperP + PTFE CBD — VALIDATED, code UNCHANGED (2026-06-24)
Real dry process the user described: ① **Thinky/planetary mix** → SuperP already coats/disperses on the
AM (carbon black), then ② **hot-roll** → PTFE fibrillates into the binder web.  This maps EXACTLY onto the
existing code with NO change — the ADD-dict order seeds SuperP (cblack, mixing=thinky → surface_frac 0.70
coats AM) BEFORE PTFE, and PTFE's `nucleate=carbon_seed` already collects phase codes (2,3) = VGCF AND
**SuperP**, so the PTFE binder nucleates on + bridges the SuperP.
- Smoke test with REAL recipe counts (AM:SE:SuperP:PTFE=80:18:1:1, recipe_counts_real): SuperP n≈133 k
  aggregates (dense), PTFE n≈246 fibres.  SuperP coats AM 65 %; **PTFE within 0.5/1.0 µm of SuperP =
  26 / 79 %** → binder genuinely nets the carbon = a real CBD.  (An earlier 6 % was a smoke-test artifact
  of too-few SuperP; the recipe volume-balance fixes it — SuperP is dense, PTFE threads through it.)
- RUN (dedicated *_carbon filenames so webapp plain-runs can't clobber se_dump; --mixing thinky; n_vox 192):
  `--add-recipe "AM:SE:SuperP:PTFE=80:18:1:1" --mixing thinky`.  Viewer: SuperP = magenta chains (phase 3,
  additive_fibres), PTFE = amber web (phase 4).  All-three (VGCF+SuperP+PTFE) also works — just add VGCF to
  the recipe.
- OPEN: tune PTFE↔SuperP binding if the real run looks too dispersed (higher nucleate_frac / shorter PTFE for
  the localized SuperP); confirm on the real GPU run.

## ★ Voxel CBD electronic FV — SuperP vs VGCF bridging quantified (real_10, 2026-06-25) ★

The transport payoff of the CBD morphology work: run the Stage-2 voxel FV (`scripts/voxel_conductivity.py`)
on the +CBD MPM dumps and read the electronic WITHOUT→WITH-CBD gain = how much the carbon network bridges
dead AM.  Case **input_8mAh_real_10** (P:S 10:0, 226 AM_P @6µm + 142,212 SE @0.5µm, DEM σ_e = 8.64 mS/cm,
i.e. a GOOD AM network).  Two `--add-recipe`s, same 80:18:1:1 wt%, n_grid 266 MPM → n_vox 256 voxel FV, `--gpu`:

| additive | WITHOUT (AM-only) | WITH CBD | **gain** | morphology | voxel carbon cells |
|---|---|---|---|---|---|
| **SuperP** | 6.464 | **8.564** | **1.3×** | 1.4 M small aggregates (distributed) | 721 k |
| **VGCF**   | 6.464 | **7.073** | **1.1×** | 31,789 long fibres (concentrated)   | 669 k |

- **Consistency ✓**: WITHOUT-CBD = 6.464 for BOTH (identical to 4283 CG iters) — same fixed AM scaffold ⇒
  same AM-only σ_e; the FV solve is deterministic + exact.  (voxel 6.46 < DEM 8.64 = the known electronic
  neck under-resolution at n_vox 256, converges up with res; the GAIN is the resolution-robust quantity.)
- **SuperP (1.3×) > VGCF (1.1×) — and it is NOT the σ value**: the 200× contrast cap clamps SuperP (1e5) and
  VGCF (5e5) to the SAME ~1e4 mS/cm, so the difference is PURE MORPHOLOGY.  SuperP's many distributed
  aggregates contact MORE dead-AM gaps than VGCF's fewer, longer fibres — for real_10's already-good AM
  network where carbon only mops up the few isolated AM, "many contacts" beats "long reach".
- ⚠ **VGCF is likely UNDER-counted**: VGCF fibres are sub-µm thin → at n_vox 256 (cell ≈0.5 µm) they
  voxelise to 1-cell threads (669 k < 721 k cells) that can break → its long-range bridging is
  under-resolved.  A fair SuperP-vs-VGCF verdict needs higher n_vox or fibre-aware voxelisation.
- **Real-physics reading**: for a POOR AM network (many dead AM) VGCF's long fibres should WIN (long
  bridges span gaps SuperP can't); real_10's AM is good, so SuperP's contact density edges it.  Next:
  repeat on an AM-poor case to confirm the VGCF crossover + bump VGCF resolution.
- Pipeline (gabia GPU): `mpm3d_compaction.py --se-dump … --add-recipe "AM:SE:{SuperP|VGCF}:PTFE=80:18:1:1"
  --save-se se_carbon{,_vgcf}.npy --save-phase phase_carbon{,_vgcf}.npy --save-se-id se_id{,_vgcf}.npy`
  then `nohup voxel_conductivity.py --se … --phase … --scaffold am_carbon.csv --n-vox 256 --porosity 0.165
  --channel electronic --gpu > {superp,vgcf}_fv.log 2>&1 &`.  σ_e thick-electrode (708 z-cells, 26 M nodes)
  ≈ 9–10 min/run on an A6000 with --gpu + bincount assembly + residual-% progress.
