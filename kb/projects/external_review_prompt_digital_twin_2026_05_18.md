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

## What we expect from review — explicit **recommendation** required

리뷰어가 **각 항목에 대해 구체적 권장사항을 제시**해주세요. 모호한 "should
consider X" 말고 **actionable decision** 형태로:

### 1. 즉시 결정 사항 (Layer 1 fixes — 코드 수정 전 결정)

리뷰어 권장 형식: **"Fix now"** / **"Defer to Phase 2"** / **"Skip entirely"**

- **A. Stage 07/08 sanity_warnings 추가** (B0 5-80 GPa, E 5-200 GPa)
  - 권장 action: ?
  - 권장 threshold: ?

- **B. Stage 11 v6 area mismatch (현재 234-325% strain)**
  - (b1) `run_cathode_interface.py` patch — SE supercell expansion
  - (b2) v30u_ensemble verified slab builder import (paper #1 호환)
  - (b3) Defer — Layer 2 v1에서 Wad target 제외
  - 권장: ?

- **C. `collect_dataset.py` quality flag 통합** (lbfgs_ok, area_mismatch_pct, fit_quality_ok)
  - 권장 action: ?
  - Layer 2 학습 시 처리 (drop / weight / flag-only)?

### 2. Layer 2 demonstration 최소 요건

리뷰어 권장 형식: **수치 + 근거**

- **D. Minimum dataset size for paper-grade Layer 2 GBR**
  - 권장 N (compound × site × seed): ?
  - 근거: ?

- **E. Compound batch composition** — 어느 compound 우선?
  - 우리 후보: Li2O, MgO, Al2O3, Y2O3, La2O3, Nd2O3, Sm2O3, SiO2, ZrO2 (9 oxide)
  - 권장 추가/제외: ?
  - 다른 카테고리 (fluoride, chloride, bromide) 포함 여부: ?

- **F. CV scheme** (random k-fold vs GroupKFold by dopant)
  - 권장: ?
  - 우리 use case ("known dopant 새 site" vs "new dopant cold-start") 별 권장 다른가?

### 3. 모델 아키텍처

리뷰어 권장 형식: **현재 GBR 유지 권장 / GNN 전환 권장**

- **G. Layer 2 v1 모델**: GBR (현재) 그대로 권장? 또는 다른 sklearn 모델?
  - 권장: ?
  - 근거 (interpretability vs accuracy vs deployment): ?

- **H. GNN 전환 시점**
  - 권장 dataset 크기 임계점: ?
  - 권장 GNN: ALIGNN / M3GNet / MACE / SchNet / 기타?

### 4. Demonstration paper 구조

리뷰어 권장 형식: **paper 구조 outline**

- **I. Paper 핵심 contribution**
  - (i1) Methodology + tool paper (JOSS, JCIM 등)
  - (i2) Application paper (Chem Mater, J Mater Chem A 등)
  - (i3) Mechanism + screening hybrid
  - 권장: ?

- **J. Minimum demonstration**
  - "이 정도면 paper 작성 시작 OK" 임계점 정량 권장: ?
    - N compounds: ?
    - Layer 2 CV R²: ?
    - Cold-start accuracy: ?

### 5. Phase 2 transition path

리뷰어 권장 형식: **순서가 있는 step list**

- **K. Active learning loop 구축 순서**
  - 1단계: ?
  - 2단계: ?
  - 3단계: ?

- **L. 다음 압축/재개 시 잃지 말아야 할 핵심**
  - 권장: 추가로 anchor 문서에 박아둘 항목?

## Reviewer가 명시적으로 답해주길 바라는 한 문장

> *"이 프로젝트가 Digital Twin paper로 publish 가능한 최단 path는 무엇인가?
> 우리가 지금까지 한 작업 중 직접 paper 기여하는 것은? 버려야 할 것은?
> 그리고 아직 안 했지만 필수로 해야 할 작업은?"*

답변은 우선순위와 근거 함께 제시 부탁드립니다.

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
