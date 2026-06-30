# Additive recipe → MPM-input (zip) physics audit — 2026-06-30

The 첨가제 적용 panel generates a zip whose job is to build the MPM input **as
physically faithfully as possible** (it IS the GPU run's input = source of truth).
Audited the whole chain; one real bug found (SE density) + fixed.

## Chain
```
wt% (UI) → recipe_counts_real (mass-conserving) → counts per additive
        → seed_fibres / seed_carbon_black (literature morphology)
        → MPM points carrying recipe VOLUME + phase code + (PTFE) A3 cohesion
```

## ✅ Audited correct
- **Mass-conserving counts** (`recipe_counts_real`): `M_tot = M_solid/(1−Σwt/100)`,
  `V_a = (wt_a/100)·M_tot/ρ_a`, `n = V_a/v_obj`. Verified V_a matches to the µm³.
- **Literature geometry**: VGCF Ø0.15 × L10 µm (aspect 67, Showa VGCF-H); Super P
  Ø0.2 µm aggregate (40 nm primaries); PTFE Ø0.25 × L40 µm fibril (aspect 160).
- **MPM phase moduli** (`ADD` dict): VGCF E=10/σ_y=2.0 (stiff carbon), Super P
  E=0.5/σ_y=0.1 (soft black), PTFE E=0.3/σ_y=0.05 (soft binder — A3 binder_cap +
  pressure-regime propping applied for PTFE).
- **Volume conservation**: per-point `add_pvs = vol_um3/n_pts`, weight `_w` mean-1
  → Σ pvs = the recipe's vol_um3 (in box units). So the additive occupies its REAL
  recipe volume in the MPM grid → **porosity changes by the true additive volume**
  (the user's "porosity가 첨가물 따라 변동"). VGCF/Super P/PTFE all seed solid volume
  → all reduce porosity (volume-fill), structurally, in the GPU run.

## 🔧 Fixed: SE density inconsistency
The codebase carried **three** Li6PS5Cl densities — `porosity_physics_regression`
2.00 (project convention), `grade_engine:978` 2.00, `additives.py` **1.64**,
`grade_engine:1217` **1.85**. The zip's additive counts used 1.64 → out of band.
**Fixed `additives.py` SE 1.64 → 2.00** (= project convention; real crystallographic
≈ 1.85–1.88, so 2.0 is the project's slightly-high standard, kept for consistency
with the CLOSED porosity model). Effect: additive counts +2.3 %, SE wt% label
10.5 → 12.5 %p for the test recipe.
⚠ Remaining flag: `grade_engine.py:1217` still uses 1.85 (a separate composite-
density metric) — left as-is to avoid shifting that metric; the user should decide
whether to standardize it to 2.00 too.

## Verdict
After the SE-density fix the zip is physically faithful: mass-conserving counts,
literature morphology, real recipe volume in the grid, A3 binder physics for PTFE.
The GPU MPM run on this input gives structure-true porosity/morphology; the carbon
σ_e-network and SE-occupancy σ_ion are the NEXT step (network solver must read the
additive phases — see the model-improvement loop).
