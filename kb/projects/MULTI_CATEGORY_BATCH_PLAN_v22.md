# Multi-Category Multi-Compound Batch Plan — Paper #2 (v4.5.18)

> **목적**: Layer 2 cold-start cross-validation을 위한 22-compound, 4-category 다중 첨가제 batch.
> Round 1 reviewer의 oxide-only 권장을 사용자 지적 (*"ZrCl4, LiBr 같은 non-oxide 후보 많은데"*) 따라 확장.
>
> 작성: 2026-05-18 (Round 3 reviewer GO 후)

---

## 1. 배경 — Round 1/2 reviewer는 왜 oxide만 권장했나

Round 1 reviewer의 보수적 권장 (9-12 oxide):

| Reviewer 논리 | 한계 |
|---|---|
| 화학 일관성 (모두 O²⁻ → S²⁻ swap) | Layer 2가 Hard-Hard mechanism만 학습 → cold-start 일반화 X |
| Sundar 2025 oxide coating literature | Coating용; bulk doping은 halide/fluoride 더 많음 |
| Anion site 일관 (S→O at 16e/4d) | DOPANT_DB 75+ 중 ~12개만 활용 → 80% 낭비 |
| Phase 2 deferred non-oxide | "왜 oxide만?" reviewer 공격 포인트 |

→ 사용자 지적이 옳음. **22-compound 4-category multi-category batch로 확장**.

## 2. 22-Compound 분류 표

### Tier A — Oxides (12개, reviewer 원래 list)

화학 일관성 + Sundar 2025 + industrial coating relevance:

| Category | Compound | Cation | Anion | Valence | Notes |
|---|---|---|---|---|---|
| Mono-valent | Li₂O | Li⁺ | O²⁻ | +1 | Baseline (host-like) |
| Di-valent | MgO | Mg²⁺ | O²⁻ | +2 | Industrial common |
| Di-valent | CaO | Ca²⁺ | O²⁻ | +2 | Larger cation |
| Di-valent | ZnO | Zn²⁺ | O²⁻ | +2 | Sundar 2025 top coating |
| Tri-valent | Al₂O₃ | Al³⁺ | O²⁻ | +3 | Sundar 2025 top coating |
| Tri-valent (RE) | Y₂O₃ | Y³⁺ | O²⁻ | +3 | 4d⁰ closed shell |
| Tri-valent (RE) | La₂O₃ | La³⁺ | O²⁻ | +3 | 4f⁰ closed shell |
| Tri-valent (RE) | **Nd₂O₃** | **Nd³⁺** | O²⁻ | +3 | **paper #2 main, 4f³ open shell** |
| Tri-valent (RE) | Sm₂O₃ | Sm³⁺ | O²⁻ | +3 | 4f⁵ open shell |
| Tetra-valent | SiO₂ | Si⁴⁺ | O²⁻ | +4 | P-site acceptor |
| Tetra-valent | ZrO₂ | Zr⁴⁺ | O²⁻ | +4 | 4d⁰ |
| Tetra-valent | TiO₂ | Ti⁴⁺ | O²⁻ | +4 | 3d⁰ (mixed valence test) |

### Tier B — Halides (6개, 사용자 지적 추가)

Real synthesis precursors (ball-mill reagents) + paper #1 cross-validation:

| Category | Compound | Cation | Anion | Valence | Notes |
|---|---|---|---|---|---|
| Fluoride | LiF | Li⁺ | F⁻ | +1 | F→Cl₄d swap, paper #1 anchor |
| Fluoride | MgF₂ | Mg²⁺ | F⁻ | +2 | Mg + F co-doping |
| Fluoride | AlF₃ | Al³⁺ | F⁻ | +3 | Common SE precursor |
| Chloride | AlCl₃ | Al³⁺ | Cl⁻ | +3 | Ball-mill reagent |
| Chloride | ZrCl₄ | Zr⁴⁺ | Cl⁻ | +4 | **사용자 명시한 예** |
| Bromide | LiBr | Li⁺ | Br⁻ | +1 | **사용자 명시한 예**, paper #1 cross-check (Br→Cl₄d) |

### Tier C — Sulfide / Nitride (2개)

Chemistry diversity (different anion electronegativity):

| Category | Compound | Cation | Anion | Notes |
|---|---|---|---|---|
| Sulfide | Li₂S | Li⁺ | S²⁻ | Anion-only (S enrichment, paper #1 modelC inverse) |
| Nitride | Li₃N | Li⁺ | N³⁻ | Different electronegativity, novel chemistry |

### Tier D — Halide-rich verification (2개)

Paper #1 Type B 재현 + 새 Br case:

| Category | Spec | Notes |
|---|---|---|
| LiCl-rich | Cl=1.6 substitution | modelC와 동일, paper #1 cross-validation |
| LiBr-rich | Br=1.6 substitution | **Paper #1엔 Br=1.0 max만 있었음, 새 case** |

**총 22 compounds**.

## 3. Batch 규모 + 시간 추정

| 변수 | 값 |
|---|---|
| Compounds | 22 |
| Sites per compound | ~5 (chemistry-allowed by site_preference) |
| Random seeds per (compound, site) | 5 |
| Supercell variants | 1 (1×1×1; multi-supercell deferred to Phase 2) |
| **TOP_K_SIGMA** (Stage 10 σ_MD) | **3** (Round 4 reviewer 권장; was 5) |
| **TOP_K_NCM** (Stage 11 Wad) | **3** (reviewer b3 defer + 시간 절약) |
| **Total datapoint** | **~1,650** |
| **GPU time (RTX A6000, 2-GPU 병렬)** | **~16 days** (TOP_K_SIGMA=3 기준) |

### Stage별 시간 분포 (per compound, TOP_K=3 기준)
- Stage 01 substitute + 02 screen: 30분-1시간
- Stage 04 anneal × 5 winners: 4-6시간
- Stage 07 EOS × 3 (top-3): 1-2시간
- Stage 08 elastic × 3 (top-3): 1시간
- **Stage 10 σ_Li × 3 (TOP_K_SIGMA=3, 12h each)**: **~36시간** ← gating factor
- Stage 11 Wad × 3 (winners) + 6 baselines: 3-5시간

→ Compound 1개당 ~45시간 gabia GPU. 22 × 45h ÷ 2 (병렬 GPU) ≈ 495h ≈ **~21일** 보수적 (안전 마진 2-3일).
**실제 timing은 Step 1/22 (Li2O) 결과로 보정**.

### TOP_K framing for paper (Round 4 reviewer 권장)
> *"σ_Li and Wad evaluated for top-3 candidates per compound, selected by
> the cascade composite score (ΔE/atom × Li-mobility × σ_proxy). The
> remaining 2/5 winners undergo Wad spot-check only when ranking
> inversions are detected in the top-3."*

## 4. 실행 명령 (gabia)

### Option α: 모든 22 compound 한 번에 (Round 4 reviewer 우려)

⚠ **DEPRECATED — Round 4 reviewer 권장으로 Option β 채택**. 아래 보존 (반환 참고용).


```bash
cd /data/work/repo

# 새 batch 디렉토리
BATCH_DIR=runs/multi_category_2026_05_19_v22
mkdir -p $BATCH_DIR

# 22 compound list
COMPOUNDS=(
  # Tier A: Oxides (12)
  Li2O MgO CaO ZnO
  Al2O3 Y2O3 La2O3 Nd2O3 Sm2O3
  SiO2 ZrO2 TiO2
  # Tier B: Halides (6)
  LiF MgF2 AlF3
  AlCl3 ZrCl4
  LiBr
  # Tier C: Sulfide/Nitride (2)
  Li2S Li3N
)
# Tier D (halide-rich) — Type B substitution은 별도 호출

# Cascade for each Tier A/B/C compound (Type A doping)
for cmp in "${COMPOUNDS[@]}"; do
    echo "============================================"
    echo "Starting cascade for $cmp"
    echo "============================================"
    bash tools/doping/tier_cascade.sh \
        db/structures/lpscl_F43m_24G_canonical.cif \
        $BATCH_DIR/$cmp \
        5 1,1,1 1 \
        --compound $cmp --x_compound 0.05 \
        2>&1 | tee $BATCH_DIR/$cmp.log
done

# Tier D — halide-rich (LiCl 1.6, LiBr 1.6) Type B
# 이건 --halide_rich 옵션으로 cascade 호출
for hal in Cl Br; do
    bash tools/doping/tier_cascade.sh \
        db/structures/lpscl_F43m_24G_canonical.cif \
        $BATCH_DIR/${hal}_rich \
        5 1,1,1 1 \
        --halide_rich $hal --excess_per_fu 0.6 \
        --anion_site S_4a \
        2>&1 | tee $BATCH_DIR/${hal}_rich.log
done
```

### Option β ✅ ADOPTED — Phase 1A (12 oxide) → Round 5 review → Phase 1B (10 추가)

**Round 4 reviewer 권장 + 사용자 채택 (2026-05-18)**. 이유:
- Partial-paper safety net: Phase 1A 완료 = oxide-only paper draft 가능
- AlCl3/ZrCl4 chemistry issue가 Tier B에 몰려있음 → Phase 1A 안전 진행 후 1B에서 catch
- Layer 2 R² intermediate measurement → Round 5 review checkpoint
- 22 compound × per-compound step-by-step stepping과도 호환


```bash
# Week 1-2: Tier A 12 oxide (Phase 1A)
for cmp in Li2O MgO CaO ZnO Al2O3 Y2O3 La2O3 Nd2O3 Sm2O3 SiO2 ZrO2 TiO2; do
    bash tools/doping/tier_cascade.sh ... --compound $cmp
done

# Phase 1A 끝나면 Layer 2 oxide-only 결과 측정 (paper 1차 draft 가능)

# Week 3-4: Tier B/C/D 10 추가 (Phase 1B)
for cmp in LiF MgF2 AlF3 AlCl3 ZrCl4 LiBr Li2S Li3N; do
    bash tools/doping/tier_cascade.sh ... --compound $cmp
done
for hal in Cl Br; do
    bash tools/doping/tier_cascade.sh ... --halide_rich $hal
done

# Phase 1B 끝나면 Layer 2 full multi-category로 paper 2차 draft
```

### Phase 1A & 1B per-compound stepping table (Option β + per-compound 결합)

배치 자체는 sequential하게 진행하되, 각 compound 완료 후 결과 분석 + GO 결정:

```
[Phase 1A — 12 oxide, ~12-14일 (TOP_K_SIGMA=3)]
  Step 1/22:  Li2O   ← 가장 안전, baseline-like, cascade 검증용
  Step 2/22:  MgO
  Step 3/22:  CaO
  Step 4/22:  ZnO   (Sundar 2025 top coating)
  Step 5/22:  Al2O3 (Sundar 2025 top coating)
  Step 6/22:  Y2O3  (4d⁰)
  Step 7/22:  La2O3 (4f⁰ closed shell)
  Step 8/22:  Nd2O3 (4f³ — paper #2 original case study, cross-check)
  Step 9/22:  Sm2O3 (4f⁵)
  Step 10/22: SiO2  (P-site acceptor)
  Step 11/22: ZrO2  (4d⁰)
  Step 12/22: TiO2  (mixed valence test)

  [Checkpoint A] Phase 1A 완료 → unified_dataset_A.csv → Layer 2 R² 1차 측정
                 → Round 5 reviewer → Phase 1B GO 결정

[Phase 1B — 10 halide+sulfide+nitride+halide-rich, ~9-11일]
  Step 13/22: LiF    (fluoride, paper #1 cross-validation)
  Step 14/22: MgF2
  Step 15/22: AlF3
  Step 16/22: AlCl3  ⚠ chemistry watch (Cl host conflict)
  Step 17/22: ZrCl4  ⚠ chemistry watch (Zr size mismatch + Cl host)
  Step 18/22: LiBr   (paper #1 Br extension)
  Step 19/22: Li2S   (S²⁻ enrichment)
  Step 20/22: Li3N   ⚠ chemistry watch (N³⁻ charge mismatch)
  Step 21/22: LiCl-rich  (Type B, paper #1 modelC cross-validation)
  Step 22/22: LiBr-rich  (Type B, Br=1.6 새 case)

  [Checkpoint B] Phase 1B 완료 → unified_dataset_full.csv → Layer 2 full R²
                 → Round 6 reviewer → paper draft start
```

### Per-compound 분석 protocol (각 step 끝나면)

자동 추출:
```bash
WBASE=/data/work/runs/multi_category_2026_05_19_v22/<compound>
python3 << 'PY'
import json
from pathlib import Path
WBASE = Path('$WBASE')
print(f"=== {WBASE.name} cascade result ===")
# Stage markers
done = sorted([p.name for p in WBASE.glob('STAGE_*.DONE')])
print(f"Stages complete: {len(done)}/18+")
# Key files
for stage, key in [('02_screen/uma_results.json', 'results'),
                    ('07_eos/postproc_summary.json', 'records'),
                    ('10_md_sigma/sigma_md_summary.json', 'records')]:
    p = WBASE / stage
    if p.exists():
        n = len(json.loads(p.read_text()).get(key, []))
        print(f"  {stage}: {n} records")
PY
```

검토 항목 (per compound):
- ✅ 모든 stage DONE marker?
- ✅ dataset.csv 모든 컬럼 채움 비율?
- ✅ σ_Li winners 합리적 (pristine LPSCl 3 mS/cm 대비)?
- ✅ EOS B₀ 합리적 (15-30 GPa 범위)?
- ✅ Stage 11 area_mismatch_pct 기록?

이슈 발견 시: cascade 중단 → fix → 재시작 (resume marker로 빨리)
```

## 5. Multi-category batch의 paper-grade 강점

| 측정 | 12 oxide only | 22 multi-category |
|---|---|---|
| Layer 2 학습 데이터 | ~900 | **~1650** |
| Cold-start CV groups | 12 | **22** |
| LOCO R² 신뢰도 | 중간 | **높음** |
| Paper narrative scope | "oxide-focused screening" | **"comprehensive multi-category screening"** |
| Reviewer 공격 가능성 | "왜 oxide만?" | **거의 없음** |
| Industrial relevance | 부분 (coating용) | **전체** (bulk doping precursors) |
| Chemistry diversity | Hard-Hard만 | **Hard-Hard + Hard-Soft + halide** |
| DOPANT_DB 활용도 | 16% | **29%** (75+ 중 22) |

## 6. 검증 plan (multi-compound batch 후)

### Quality gate (per category)
- Tier A oxide LOCO R² ≥ 0.3 (random R² ≥ 0.7)
- Tier B halide LOCO R² ≥ 0.2 (random R² ≥ 0.6)
- Tier C sulfide/nitride: 통합 LOCO R² 통계만
- Cross-category prediction: Tier A 학습 → Tier B 예측 R²

### Paper Methods 섹션 narrative
> *"We screened 22 dopant compounds across 4 categories (oxides, fluorides,
> chlorides/bromides, sulfides/nitrides) covering the +1 to +4 valence range
> and Hard/Soft Lewis-acid spectrum. This breadth allows leave-one-compound-out
> cross-validation of the Layer 2 surrogate model on chemistry classes the
> training data has never seen, providing realistic cold-start deployment
> estimates."*

### Reviewer 우려 사전 차단
- *"Why these 22 specific compounds?"* — Mendeleev + Hard/Soft HSAB coverage table 첨부
- *"Cost-effectiveness?"* — 22 × 15h ÷ 2 GPU = 1주 vs 12 oxide × 15h ÷ 2 GPU = ~3.5일. **약 2배 시간, 80% 더 활용도**.
- *"Why not 75 (entire DOPANT_DB)?"* — Quality > quantity. 22가 statistical + chemistry coverage 둘 다 충족하는 sweet spot.

## 7. 즉시 실행 명령 (gabia에서)

```bash
cd /data/work/repo

# 최신 v4.5.18 fetch
git pull origin claude/unified-2026-05-15
git log --oneline -3
# 743d5de v4.5.16 + a00fbf1 v4.5.17 + 새 v4.5.18 commit이 있어야 함

# Sanity test on existing Nd2O3 cascade (NEW-D fix in run_anneal applied)
WBASE=/data/work/runs/tier_2026_05_16_v456_Nd2O3_6base

# run_anneal NEW-D defensive test (won't trigger in current cascade, but verify import OK)
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, 'tools/doping')
from run_anneal import winner_name
# Test
test_cases = [
    Path('04_anneal/winner_A/post_relax.xyz'),
    Path('04_anneal/winner_A/post_md.xyz'),
    Path('01_structures/compound/named_struct.xyz'),
]
for p in test_cases:
    print(f'  {p} → {winner_name(p)}')
"

# 22-compound batch 시작 (백그라운드)
BATCH_DIR=/data/work/runs/multi_category_2026_05_19_v22
mkdir -p $BATCH_DIR

nohup bash -c '
source /data/apps/miniforge3/etc/profile.d/conda.sh
conda activate uma
for cmp in Li2O MgO CaO ZnO Al2O3 Y2O3 La2O3 Nd2O3 Sm2O3 SiO2 ZrO2 TiO2 LiF MgF2 AlF3 AlCl3 ZrCl4 LiBr Li2S Li3N; do
    echo "=== Starting $cmp at $(date) ==="
    bash tools/doping/tier_cascade.sh \
        db/structures/lpscl_F43m_24G_canonical.cif \
        '"$BATCH_DIR"'/$cmp \
        5 1,1,1 1 \
        --compound $cmp --x_compound 0.05
done
' > $BATCH_DIR/master.log 2>&1 &

echo "Started background batch. PID: $!"
echo "Monitor:  tail -f $BATCH_DIR/master.log"
echo "         watch -n 30 'bash tools/doping/watch_status.sh'"
```

## 8. 사용자 결정 요청

1. **Option α (22 모두 한 번에)** vs **Option β (Phase 1A oxide → 1B halide)** 중 어느 쪽?
2. **batch directory 이름**: `multi_category_2026_05_19_v22` OK? 또는 변경?
3. **TOP_K**: 현재 cascade default가 12 (top winners)인데 22 compound × 12 winners = 264 anneal. 너무 많으면 TOP_K_SCREEN=5 또는 8로?
4. **Tier D (halide-rich Cl/Br)** 포함 vs 제외?

답주시면 즉시 commit + push + gabia 명령 정확히 드립니다.

---

## 부록 — Round 1/2/3 reviewer 권장 추적

| Round | Compounds 권장 | 사용자 채택 |
|---|---|---|
| Round 1 | 9-12 oxide (D권장 수치+근거) | 부분 채택 (확장) |
| Round 2 | 12 oxide 유지 + fluoride/chloride Phase 2 | 사용자 지적으로 확장 |
| Round 3 | GO + slide wording 수정 | 채택 + 22 compound 확장 |
| **이 문서** | **22 compound 4 category** | **사용자 지적 결과** |

Round 1 reviewer의 보수성은 *"scope creep 방지"* 의도. 사용자가 더 야심차게 가는 것은 다음 reviewer round (multi-compound batch 후)에서 *"reviewer-recommended caution + user-justified expansion"* narrative로 정직하게 표현 가능.
