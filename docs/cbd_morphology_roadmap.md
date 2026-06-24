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

### ⏳ PENDING (batch 2 — add AFTER v2 confirms batch 1)
2. **branching (1차→2차→3차 hierarchy)** — primary fibril spawns thinner secondary/tertiary
   children from points along it (reduced V, shorter L) → tree topology + finer fibrils.
   Today the per-fibre Ø spread approximates the thickness RANGE but not the connected tree.
4. **directed particle→particle bridge** — today: nucleate on carbon then ISOTROPIC walk.
   Real binder bridges adjacent particles: bias the walk toward a NEIGHBouring attractor so
   the fibril CONNECTS two particles/carbon clusters (the actual binding action).

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
