# External Review Prompt — Digital Twin Platform Readiness (2026-05-18)

> 외부 LLM (또는 다른 reviewer)에게 보낼 prompt 초안.
> 기존 review (8라운드)는 Stage 10/11 paper batch 직전 점검이었음.
> 이번은 **Digital Twin Platform 전체 readiness** + Layer 2 학습 path 검토.

---

## Context for reviewer

This project is a **3-layer ML platform for sulfide solid electrolyte (LPSCl
argyrodite) dopant screening**, NOT a single mechanism paper.

```
Layer 1 — UMA-s-1p1 cascade (18 stages, paper-validated R=0.989)
Layer 2 — ML surrogate (GBR, → GNN long-term)
Layer 3 — Active learning + inverse design (Phase 3)
```

8 rounds of external review have hardened Layer 1 (cascade) including
v4.5.13 closing all 21 cascade-script provenance holes. Tier_cascade.sh
already wires Stage 09b/09c for `collect_dataset.py` + `train_predictor.py`.

**Current status**:
- Layer 1: ✅ production-ready, paper-grade output
- Layer 2: ⚠️ wired but trained on only 1 compound (Nd2O3, 60 configs)
- Layer 3: ❌ not started (Phase 3)

## What we need reviewed

### A. Layer 2 training readiness (PRIMARY)

Is the dataset → training → inference flow paper-grade?

1. **`collect_dataset.py`** — does it capture all critical Layer 1 outputs?
   - ΔE/atom (binding), ΔV/V0, Tier-1/2 metrics, BVSE proxy
   - Post-anneal ΔE, EOS B0/V0/R², Elastic B/G/E/Pugh/ν
   - σ_Li from Stage 10 (Ea, σ_300K_NE)
   - Wad from Stage 11 (currently has area mismatch issue — separate)
   - **Quality flags**: `lbfgs_ok`, `area_mismatch_pct`, `fit_quality_ok`,
     `sanity_warnings`, `converged_post_anneal`
   - Are any of these missing from CSV columns?

2. **`train_predictor.py`** — GBR per-target. Sensible choice?
   - 5 targets: ΔE/atom, B0, E_young, Pugh, migration_volume_fraction
   - Categorical: dopant, cation_site, anion_site, charge_compensation
   - Numeric: Tier-2 metrics, BVSE std/mean, etc.
   - **Sample size requirement**: GBR 권장 최소? (currently we have 60 configs of Nd2O3 → way too small)
   - **CV scheme**: random k-fold — is dopant leakage acceptable for our use case?
     (Use case: predict NEW (site, conc) combos for ALREADY-seen dopants)
   - **Cold-start mode**: dopant-only features predict accuracy?
     (Use case: filter "obviously bad" before launching UMA)

3. **`predict_new.py` / `chain_predict.py` / `predict_best_site.py`** —
   inference correctness?
   - `predict_best_site.py` enumerate (cation_site × anion_site × concentration)
     for a NEW compound, score each
   - `chain_predict.py` Tier 1 stability gate → Tier 2 modulus/mobility
   - Are go/no-go thresholds (stability_threshold) sensible?

### B. Known Layer 1 issues — defer or fix?

1. **Stage 11 v6 area mismatch** (2026-05-18 발견):
   - `run_cathode_interface.py` stacks SE primitive cell with NCM nx×nx
   - Result: 234-325% in-plane strain for all baselines
   - Wad absolute values strain-contaminated (ranking still valid)
   - Paper #1 `필독/adhesion/v30u_ensemble/` has verified per-comp slab
     builders with strain<2% (R=0.989)
   - **Question**: For Layer 2 v1, defer Wad target until v30u port?

2. **Stage 07/08 sanity_warnings** (v4.5.13 deferred NEW-2):
   - Currently only `fit_quality_ok` flag (EOS R² gate)
   - Missing absolute range: B0 < 5 or > 80 GPa, E < 5 or > 200 GPa
   - **Question**: Should be added to dataset.csv as filter for Layer 2?

3. **Multi-compound batch not yet run** (Layer 2 data starvation):
   - 75+ compounds in DOPANT_DB
   - Only Nd2O3 cascade run → 60 datapoint
   - Layer 2 model can't generalize with n=60
   - **Question**: Minimum N (compound × site × seed) for paper-grade Layer 2?
     Recommend batch composition?

### C. Architecture decisions

1. **Layer 2 model choice**: GBR (current) vs ALIGNN/M3GNet/MACE-FT?
   - GBR: deterministic, fast retrain, interpretable, but needs hand-crafted features
   - GNN: end-to-end from structure, scales to large datasets
   - Crossover point in dataset size?

2. **Active learning loop** (Phase 2 next):
   - How to wire Layer 2 prediction → Layer 1 verification → retrain?
   - Uncertainty estimation in GBR (quantile regression?) or move to GNN?

3. **Multi-task vs single-task** for Layer 2:
   - Current: separate GBR per target
   - Multi-task GNN could exploit correlations (B0 vs E_young, σ vs mobility)

### D. Demonstration paper structure

If we wrote a Digital Twin methodology + demonstration paper now:

1. **Title候**: "Multi-tier ML platform for sulfide solid electrolyte dopant
   screening with paper-validated MLIP foundation"
2. **Sections**:
   - Layer 1 verification (paper #1 R=0.989 result)
   - Layer 2 architecture + training (multi-compound dataset)
   - Cold-start prediction validation (leave-one-out compound)
   - Case study: Nd2O3 doping site selectivity (4f³ chemistry)
3. **Reviewer question**: What's the minimum bar for Layer 2 demonstration?
   - 10 compounds? 20? 50?
   - 1 target (ΔE) only? Or all 5?
   - Compare to no-ML baseline (e.g., site_preference filter alone)?

### E. Honest gaps reviewer should catch

1. We've not yet validated UMA-s-1p1 sulfide bias (Wang 2025 npj Comp Mater
   warns of softening + Li diffusivity overestimation)
2. ML predictor data leakage: random k-fold leaks dopant across folds.
   GroupKFold by dopant is correct for cold-start use case.
3. Stage 11 v6 absolute Wad strain-contaminated (acknowledged).
4. Only Nd2O3 cascade run so far (data starvation).
5. modelC base hardcoded (Li5.4PS4.4Cl1.6) — other base argyrodites?

## What we expect from review

- Identify Layer 2 readiness gaps (data, features, model, validation scheme)
- Suggest minimum batch size for paper-grade Layer 2 demonstration
- Critique cold-start prediction methodology
- Flag any Layer 1 ↔ Layer 2 data flow holes in `collect_dataset.py`
- Recommend Phase 2 transition path (when to swap GBR → GNN)

## Files to attach

- `tools/doping/` full directory (28 scripts)
- `kb/projects/MUST_READ_digital_twin_north_star.md` (this session's anchor)
- `kb/projects/digital_twin_v2_roadmap.md` (existing roadmap)
- `README.md` (top-level vision)
- One example cascade output (current Nd2O3 run on gabia)

---

**One-line ask**:
> *"Is our Digital Twin platform's Layer 2 (ML surrogate) training pipeline
> production-ready, or are there blocking gaps before we should scale up
> the multi-compound batch?"*
