# Dry-Electrode Composite Pipeline — Microstructure → Multiphysics → Degradation

Controlling roadmap for the conductive-additive + grid-multiphysics + chemo-mechanical
degradation extension.  Built on the DEM↔MPM complementary frame (CLAUDE.md): DEM owns
discrete packing/contacts/fracture, MPM owns plastic morphology/stress; here we ADD a
grid field-solver (transport), conductive additives, and SOC-breathing degradation.
Each model stays calibrated to experiment independently (frame [4]); agreement =
cross-validation, disagreement = a quantified model limit.

```
 DEM (LIGGGHTS)            MPM grid (mpm3d_compaction)         grid multiphysics
 ─────────────            ───────────────────────────         ─────────────────
 AM+SE packing            SE plastic morphology (void-fill)   voxel_conductivity.py
 contacts / Auerbach  ─▶  + ADDITIVES (VGCF/SuperP/PTFE)  ─▶  σ_ionic / σ_e / σ_thermal
 force chains             stress / plastic-strain field       (0V/1V field solve, ∇·σ∇φ=0)
        │                          │                                   │
        └────────── SOC breathing (eigenstrain) ───────────────────────┘
                    → stress → Auerbach fracture → contact/σ loss → DEGRADATION ↺
```

WHY this is possible where LIGGGHTS isn't: the DEM cost scales with **particle count**
(nano carbon = millions of objects → impossible); the grid cost is **resolution-bound**,
and the MPM already carries a **per-point material (µ, λ, σ_y)** — so an additive is just
"more material points with different constants", no kernel change.  Nano features stay
sub-grid → they enter HOMOGENISED (a fibre = a chain of points; carbon black = a blob).

---

## Modules

| file | role | status |
|------|------|--------|
| `scripts/additives.py` | recipe wt% → VGCF/SuperP/PTFE counts (flexible) + seeding (fibres = point-chains, SuperP = blobs) | ✅ done, tested |
| `scripts/voxel_conductivity.py` | image-based effective σ on the MPM voxel grid (FEM cross-check for the DEM network); ionic/electronic/thermal | ✅ done, self-test exact |
| `scripts/mpm3d_compaction.py` | **+ `--add-recipe`** : seed additives as extra phases after SE | ⏳ Stage 1 |
| (Stage-E σ-map builder) | per-voxel σ with Cronau/Trevisanello/Wang/fracture → apples-to-apples vs network solver | ⏳ Stage 2 |
| (SOC breathing) | AM eigenstrain(SOC) → cyclic stress → Auerbach fracture → σ loss | ⏳ Stage 3 |

---

## Physical parameters (literature; tunable)

| material | ρ (g/cm³) | size | mechanics (MPM) | σ_ionic | σ_e (mS/cm) | κ (W/m·K) |
|----------|-----------|------|-----------------|---------|-------------|-----------|
| AM (NMC811) | 4.80 | 6 / 2 µm | E 140 GPa, ~rigid | block | 50 | 4.0 |
| SE (LPSCl)  | 1.64 | 0.5 µm   | E 1.53 GPa softened, σ_y 0.30, ν 0.49 | σ_grain·Cronau(r_SE) | block | 0.7 |
| **VGCF**    | 2.00 | Ø0.15 × L10 µm (AR≈67) | **medium stiff + high yield** (keeps fibre shape, bends along AM) | block | 5·10⁵ | 20 |
| **Super P** | 1.90 | ~0.2 µm aggregate (sphere) | soft filler | block | 1·10⁵ | 5 |
| **PTFE**    | 2.20 | Ø~1 × L~50 µm fibril (hot-roll 85°C; branch to 10s nm) | **soft binder FIBRE** | block | 0 | 0.25 |

VGCF + Super P are SEPARATE conductive additives — the recipe picks which goes in.
PTFE morphology: dry-process hot-roll fibrillation → long thin threads spanning tens of
NMC ([RSC D5EE03240G](https://pubs.rsc.org/en/content/articlehtml/2025/ee/d5ee03240g),
[Front. Energy 2023.1336344](https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1336344/full)).

### Production recipes
- standard: `AM:SE:VGCF = 72:27:1` wt%  → vol% 46.9 : 51.5 : 1.6  → 6,354 VGCF fibres (real_9 RVE)
- dry thick-film: `AM:SE:VGCF:PTFE = 80:18:1:1` wt% → vol% 58.3:38.4:1.7:1.6 → 7,102 VGCF + 194 PTFE fibrils

---

## Stage 1 — Carbon wiring (MPM morphology)   ⏳ IN PROGRESS
**Goal:** seed VGCF/SuperP/PTFE into the MPM as extra phases → see where the additives sit
after compaction (fibres threading the SE/voids, bending around AM — like the SEM).

**How:** after the SE seed builds `xs / mus / las / ylds / pvs`, if `--add-recipe` given,
call `additives.recipe_counts` (solid = AM_vol + SE) → seed fibre/blob points (box units,
avoiding `am_mask`) → append with per-additive (µ,λ,σ_y):
- VGCF  : E≈10 GPa, ν 0.3, σ_y≈2 GPa (high → no yield → fibre keeps shape, elastic bend)
- SuperP: E≈0.5 GPa soft, low σ_y (compliant void filler)
- PTFE  : E≈0.3 GPa soft binder fibre
Track a numpy `phase` (1 SE / 2 VGCF / 3 SuperP / 4 PTFE; 0 AM = scaffold mask) for output
(the kernel uses only µ/λ/σ_y → no P2G/G2P change).  Extend `--save-phase`.

**Run (planned):**
```
python3 scripts/mpm3d_compaction.py --am-scaffold am.csv --se-dump se.csv --periodic \
  --add-recipe "AM:SE:VGCF:PTFE=80:18:1:1" --save-phase phase.npy --save-se se.npy ...
```

---

## Stage 2 — Stage-E σ-map (transport consistency)   ⏳
**Goal:** the voxel field-solve must use the SAME literature-corrected σ as the DEM network
solver (Cronau/Trevisanello/Wang + fracture), so FEM↔network is apples-to-apples.

**How:** build a per-voxel σ map (voxel_conductivity already accepts a σ array):
- SE voxels: σ_grain × **Cronau(r_SE)** (sub-µm amorphization)
- AM voxels: **AM_P (poly) vs AM_S (single-crystal) Trevisanello** for σ_e; **Wang** for κ
- fractured regions: **Lawn stage σ-loss** (map DEM Auerbach per-contact → voxels)
Needs aux data: phase grid (have), AM_P/AM_S labels, fracture field.

---

## Stage 3 — SOC breathing → degradation   ⏳
**Goal:** CC/CV charge + CC discharge volume changes (NMC ~2-6 vol% vs SOC) → cyclic stress
→ fracture → contact/σ loss → cycle-life degradation.  No one has done this from microstructure.

**How (staged):**
1. single breathing step: AM eigenstrain ε_chem(SOC) (NMC SOC-volume literature curve), AM
   elastic+eigenstrain (still no plastic flow — consistent with rigid-but-breathing) → MPM
   stress field → where it exceeds the Auerbach/Lawn criterion (hotspots).
2. few cycles: contact-area + σ drift.
3. full cycle-life: needs a surrogate (1000 cycles × MPM solve infeasible).

**Coupling (the degradation loop):** MPM breathing-stress → DEM Auerbach fracture criterion
→ crack → contact/σ loss (voxel solve) → next cycle.  One-way first; two-way (crack → re-solve)
is the real loop.

---

## Stage 1b — webapp additive 3D viewer + save-list   ⏳ (after the additive run produces a payload)
Depends on the additive payload carrying phase (no phase data → nothing to colour), so build
AFTER Stage 1 GPU run succeeds and the payload format is set.  Three pieces, one go:
1. **payload phase** : `mpm_webapp_payload.py --phase phase.npy` → carry per-point/per-tri phase
   code (1 SE · 2 VGCF · 3 SuperP · 4 PTFE) into `mpm_payload.json`.
2. **viewer colour** : `single.html` 3D viewer renders by phase (SE grey · VGCF black fibre ·
   SuperP dot · PTFE orange) — extend the existing SE/AM viewer.
3. **button + save-list** : a "도전재 3D" button (active only when an additive payload is present)
   opens that viewer; BELOW it an **accumulating saved-payload list** (one row per recipe —
   VGCF 72:27:1, VGCF:PTFE 80:18:1:1, …) to save / re-select / compare, like the case-list/archive.

---

## Cross-validation targets (frame [4])
- σ_eff(FEM voxel)  vs  σ_ionic(DEM network/Kirchhoff)  — validates Holm/Stage-E (cf. Bazzoun RNM↔FEM)
- σ_e with carbon   vs  the "도전재 권장 / dead-AM" warning — turns the flag into a quantitative optimum
- breathing fracture vs  the press-only Auerbach fracture — adds the chemo-mechanical stress source
