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

---

# 📍 ROUND 2 UPDATE (2026-05-18 evening) — v4.5.15 deployed + in-vivo test

> 첫 round (위) 권장사항을 받아 **즉시 v4.5.15 commit + deploy + gabia 실측**.
> 결과: **Layer 2 학습 자체는 작동 확인**, but **새 bug 2건 + sample-size
> 한계 노출**. 이번 round 2에서는 (a) v4.5.15 fix 적용의 타당성 검증, (b) 새
> findings 처리 결정, (c) multi-compound batch 시작 전 마지막 점검.

## v4.5.15 deployed fixes (round 1 권장에 기반)

| ID | Description | Result |
|----|-------------|--------|
| DT-1 | `collect_dataset.py` stage path swap (04_bvse/05_anneal → 04_anneal/05_bvse) | ✅ anneal 12/61 non-null (was 0/61) |
| DT-2 | Stage 10 (σ_Li) + Stage 11 (Wad) 컬럼 통합 (19 new cols) | ✅ sigma_300K 5/61 non-null |
| DT-3 | Quality flags (sanity_warnings_count, lbfgs_ok_fraction, area_mismatch_severity, eos_fit_quality_ok) | ✅ all present |
| DT-4 | GroupKFold + LOCO CV alongside random | ✅ 3 schemes reporting |
| DT-5 | sigma_300K_S_cm_NE added to TARGETS | ✅ recognized |
| DT-6 | DummyRegressor baseline | ✅ R²≈0 baseline working |
| DT-7 | Stage 12 (collect+train) cascade reorder | ✅ post-Stage 10/11 |

**Commit**: `b9f2b19 v4.5.15` on `claude/unified-2026-05-15` branch.
**Total**: 3 files, +168 / −18 lines.

## In-vivo test result (gabia, Nd2O3 cascade)

### Layer 2 training works (cold_start mode, screen_de_per_atom target):

| Model | Random KFold R² | LOCO R² | n_folds (loco) |
|-------|-----------------|---------|----------------|
| **GBR**   | **+0.953 ± 0.012** | +0.137 ± 0.539 | 2 |
| **RF**    | +0.953 ± 0.012 | +0.137 ± 0.540 | 2 |
| **Dummy** | −0.059 ± 0.038 | −3.32 ± 2.89  | 2 |

**핵심 관찰**:
- ✅ GBR R²=+0.95 (random) vs Dummy R²=−0.06 → **non-trivial 학습 확인**
- ✅ LOCO collapse (0.14 vs random 0.95) → **multi-compound batch 필수성 정량 증명**
- ✅ Dummy LOCO R²=−3.32 → **Layer 2 (R²=0.14)도 dummy보다 훨씬 나음 (+3.5)**
- ⚠ LOCO n_folds=2 → dataset에 dopant=2종 (Nd2O3 + 1 잔여) — 진정한 cold-start 아님

→ Layer 2 학습 framework 자체는 paper-grade로 작동. 다만 **single-compound로는 한계 직접 노출**.

## Round 2 new findings (deployment 후 발견)

### NEW-A: BVSE Stage 05 produces **empty records list**

```bash
$ python3 -c "import json; d=json.load(open('05_bvse/bvs_report.json'));
                print('n_records:', len(d.get('records', [])))"
n_records: 0
```

- `STAGE_05.DONE` 마커는 있음 → BVSE ran without crash
- but `records: []` → silent fail
- 결과: bvs_li_mean / migration_volume_fraction 등 **0/61 non-null**
- Layer 2의 *"migration mobility"* target 학습 불가능

**가능한 원인** (reviewer 진단 요청):
- (a) `bvse_proxy.py`가 `xyz_dir` 인자 받았지만 글로빙 실패
- (b) Stage 05 input이 Stage 04 anneal output `post_relax.xyz` 인데 file 위치 다름
- (c) CR-3 fix (v4.5.11)가 BVSE를 post-anneal로 이동했는데 path layout 미스매치
- (d) bvse_proxy 내부 silent exception

### NEW-B: `train_predictor.py` mask 너무 strict (with_structure mode)

```python
# train_predictor.py:170 (현재)
for f in feats_numeric:
    if f in df.columns:
        mask &= df[f].notna()    # ← bvs_li_mean이 0/61 → mask all False
```

`with_structure` mode가 BVSE 컬럼 non-null 요구 → NEW-A로 인해 0 usable.

`cold_start` mode (BVSE features 안 봄)에선:
- screen_de_per_atom: 60/61 usable ✓
- 다른 target들은 sample 적어서 skip (threshold=20)

**해결책 옵션** (reviewer 진단 요청):
- (b1) `cold_start` default로 변경 (sklearn 권장: less strict masking)
- (b2) Optional feature 패턴 — NaN imputer 도입
- (b3) BVSE feature를 STRUCTURAL → CHEAP_FEATURES_OPTIONAL로 분리

### NEW-C: Sample-size threshold issue

`train_predictor.py:149`:
```python
if len(d) < 20:
    print(f"  ✗ skip {tgt} (only {len(d)} usable rows)")
```

`sigma_300K_S_cm_NE`: 5 usable rows (Nd2O3 5 winners) → skip.

paper에 "preliminary indicator" 결과 보고하려면 threshold 완화 필요.

**Reviewer 권장 threshold?**
- 너무 낮으면 (n<5) CV unstable
- 너무 높으면 (n≥20) winner stage data 학습 불가

## Round 2 specific questions for reviewer

### Q-R2-1: NEW-A — BVSE empty records 원인 진단 + fix path?

가능한 fix:
- (a1) `bvse_proxy.py` exception handling 강화 + non-fatal logging
- (a2) `tier_cascade.sh` Stage 05 input path 명시 (현재: `04_anneal/*/post_relax.xyz`)
- (a3) BVSE를 optional stage로 격하, mobility target은 σ_300K MD로 대체
- 권장: ?

### Q-R2-2: NEW-B — mask logic 권장?

- (b1) `cold_start` default + BVSE features는 *"if available"* optional 처리
- (b2) sklearn SimpleImputer (mean/median) 통합
- (b3) feature group 분리 — required vs optional
- 권장: ?

### Q-R2-3: NEW-C — small sample threshold 권장?

- 현재 `len(d) < 20` → 5 sample sigma_300K skip
- 권장 새 threshold: ?
- multi-compound batch 후 sample 충분해지면 자동 해결되지만, paper "preliminary indicator" 보고 위해 단기 완화 가능?

### Q-R2-4: Round 1 권장 그대로 진행해도 OK인가?

Round 1 권장사항:
- **D**: N ≥ 500 datapoint
- **E**: 9 oxide + (CaO/ZnO/TiO2)
- **F**: 3 CV scheme reporting (구현 완료)
- **G**: GBR 유지 + dummy baseline (구현 완료, R²=−0.06 정확히 작동)

v4.5.15 결과 (R²=0.95 random, LOCO=0.14) 보고 round 1 권장값 조정 필요한가?

특히:
- **N ≥ 500** — Nd2O3 single 60 사례에서 random R²=0.95 이미 나왔는데 multi-compound 후 N=500에서 어떤 R² 기대?
- **9 oxide list** — Round 1 권장대로 그대로 진행 OK?
- **추가 compound 카테고리** (fluoride, chloride) Round 2에서 추가하라 권장?

### Q-R2-5: Multi-compound batch 시작 시점

지금 즉시 시작 vs NEW-A/B/C fix 후 시작?

- **Option α**: NEW-A (BVSE) 먼저 fix → batch → BVSE features 학습 포함
- **Option β**: 즉시 batch (BVSE NaN으로 두고) → batch 후 NEW-A fix
- **Option γ**: NEW-A는 별도 stage로 격하 (BVSE 없이 Layer 2 작동) → batch

**시간 여유 있음** (사용자 명시), but 가장 efficient path?

### Q-R2-6: Round 2 reviewer one-line ask

> *"v4.5.15 deployment 결과 + 새 findings (BVSE empty, mask strict, threshold) 보고
> Layer 2 production-ready로 인정 가능한가, 아니면 multi-compound batch 시작
> 전 추가 fix 필요한 critical 항목 있는가?"*

## v4.5.15 Files attached for Round 2

- **commit b9f2b19**: v4.5.15 patch diff (3 files)
- `tools/doping/collect_dataset.py` (updated)
- `tools/doping/train_predictor.py` (updated)
- `tools/doping/tier_cascade.sh` (Stage 12 added)
- gabia 실측 결과:
  - `runs/.../dataset_v3.csv` (60 cols × 61 rows)
  - `runs/.../predictor_v3_cold/training_summary.json` (R²=0.953 GBR vs −0.06 dummy)
- New findings 진단 결과:
  - BVSE n_records: 0
  - train_predictor `--mode with_structure` → 0 trained
  - train_predictor `--mode cold_start` → 1 trained (screen_de_per_atom)

---

# 📍 ROUND 3 UPDATE (2026-05-18 late) — v4.5.17 NEW-D fix

> v4.5.16 deployed (NEW-A bvse_proxy hard-exclude + NEW-B mask + NEW-C
> threshold). Gabia sanity test on Stage 05 alone revealed **NEW-D**:
> same `post_relax.xyz` name collision pattern that round 9 fixed in
> combine_rankings.py (CR-A v4.5.8) was missed in `bvse_proxy.py` and
> `run_mlip_postproc.py`. Without fix, multi-compound batch loses 80%
> of Stage 05/07/08 records to dict-key collision.

## v4.5.17 deployed fix (NEW-D)

| File | Change | Impact |
|------|--------|--------|
| `bvse_proxy.py` | `winner_name()` helper; replace 4 uses of `.stem` | BVSE records 0 dupes in dict |
| `run_mlip_postproc.py` | same helper; replace 5 uses of `.stem` | EOS/elastic records keyed by parent dir |

Test result (v4.5.16 in-vivo, NEW-D bug):
- Stage 05 BVSE: 12 records computed
- collect_dataset: only **1/61 row** with `bvs_li_mean` non-null (11 overwritten)

Test result (v4.5.17 expected after gabia rerun):
- Stage 05 BVSE: 12 records computed, **12 unique names** preserved
- collect_dataset: **12/61 row** with `bvs_li_mean` non-null

**Commit**: `a00fbf1` v4.5.17 on `claude/unified-2026-05-15`.

## Round 3 question for reviewer

### Q-R3-1: NEW-D fix 적절한가?

`winner_name(xyz_path)` helper — `stem in ('post_relax', 'post_md')`이면
`parent.name` 반환:
```python
def winner_name(xyz_path):
    p = Path(xyz_path)
    if p.stem in ('post_relax', 'post_md'):
        return p.parent.name
    return p.stem
```

- 적용 위치: 9 places (bvse 4 + postproc 5)
- 동일 패턴이 combine_rankings.py (v4.5.8 CR-A)에 이미 적용됨 — 일관성
- 권장 audit: 다른 cascade script에도 같은 패턴 잔재 있는지? (run_anneal,
  run_md_sigma, run_cathode_interface, rank_anneal, generate_dft_inputs 등)

### Q-R3-2: Multi-compound batch GO 인증?

지금 v4.5.17 + Round 3 reviewer 인증 후 즉시 시작 가능?
- ✅ DT-1~DT-7 (v4.5.15)
- ✅ NEW-A/B/C (v4.5.16)
- ✅ NEW-D (v4.5.17)
- 추가 audit 필요한 hole 있는가?

### Q-R3-3: One-line ask (Round 3)

> *"v4.5.17 post NEW-D fix로 multi-compound batch GO 가능한가, 아니면
> 추가 라운드 4가 필요한가?"*

## v4.5.17 files attached

- `tools/doping/bvse_proxy.py` (winner_name + 4 usages)
- `tools/doping/run_mlip_postproc.py` (winner_name + 5 usages)
- commit `a00fbf1` full diff
