# 🚨🚨🚨 MUST READ — Digital Twin Platform North Star

> **새 session / 압축 후 첫 5분 안에 무조건 읽기**.
> 이 문서를 안 읽으면 Claude가 **반드시 Nd2O3 paper narrative로 drift함** —
> 그 drift는 본 프로젝트의 진짜 목적이 아니다.
>
> 마지막 갱신: 2026-05-18 (압축 후 drift 사건으로 작성)

---

## 1. 이 프로젝트가 진짜로 무엇인가

**Digital Twin Platform** for sulfide solid electrolyte dopant screening.
**3-layer ML 인프라**가 본체. Nd2O3, paper #2 mechanism narrative 등은
모두 이 platform의 **데이터 1개 점 + demonstration**일 뿐.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Active Learning + Inverse Design (Phase 3)        │
│  → Pareto multi-objective, composition-property maps        │
└─────────────────────────────────────────────────────────────┘
                            ↑ retrain
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: ML Surrogate (GBR → GNN/M3GNet/MACE)              │
│  → train_predictor.py, predict_new.py, chain_predict.py,    │
│    predict_best_site.py, collect_dataset.py                 │
│  → cold-start: 라벨만으로 ΔE/B0/E/σ 예측 (UMA 안 돎)        │
│  → 1000× faster than Layer 1                                │
└─────────────────────────────────────────────────────────────┘
                            ↑ training data
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: UMA-s-1p1 Cascade (18-stage, verified)            │
│  → tier_cascade.sh, 75+ DOPANT_DB, 5 doping types           │
│  → cascade가 dataset.csv 생성 (Stage 09b)                   │
│  → cascade가 predictor 학습 (Stage 09c)                     │
│  → paper #1 validation: R=+0.989                            │
└─────────────────────────────────────────────────────────────┘
                            ↑ occasional check
┌─────────────────────────────────────────────────────────────┐
│  Foundation: DFT (KISTI QE, paper-grade)                    │
│  → Top-K external validation (~10/year)                     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Nd2O3 cascade는 platform의 1개 demonstration

- 5월 16일 batch: Nd2O3 60 configs → 12 winners → 5 σ_Li winners
- 이건 **Layer 1 cascade의 한 번 작동 예시**
- Layer 2 학습에 dataset 1점만 줌 (model 학습 못 함, 최소 500+ 필요)
- 다음 step: **다른 compound batch 추가**해서 dataset 확장

## 3. Claude가 자주 drift하는 안티 패턴 (이러면 stop!)

다음 발언이 나오면 **즉시 이 문서로 돌아오세요**:

- ❌ *"Nd2O3 narrative 강화하자"* — Nd는 1개 datapoint. 다른 compound 더 돌려야
- ❌ *"왜 Nd인가 cherry-pick 해명"* — Layer 2 학습되면 자동 답변 됨
- ❌ *"Stage 11 v6 area mismatch fix 필수"* — Layer 2 v1엔 Wad target 안 써도 됨
- ❌ *"paper #2 mechanism deep dive"* — paper #1 mechanism (R=0.989) 이미 있음
- ❌ *"4f³ chemistry 강조"* — case study일 뿐
- ❌ *"option A/B/C cathode protocol 선택"* — Layer 1 한 stage detail
- ❌ *"새 doped slab builder 작성"* — 검증된 v30u_ensemble 쓰면 됨

올바른 frame:
- ✅ *"Layer 1 cascade를 N 종 compound에 돌려서 dataset.csv 키우자"*
- ✅ *"train_predictor.py 출력 CV R²가 충분히 높은가?"*
- ✅ *"predict_best_site.py로 새 compound (UMA 안 돌리고) 예측 정확성?"*
- ✅ *"chain_predict.py go/no-go gate logic 작동 검증"*
- ✅ *"Layer 2 model swap: GBR → ALIGNN/M3GNet 시점?"*

## 4. 검증된 자산 (재생성 금지)

### Layer 1 — Production code (tools/doping/)
8 rounds 외부 review + 5 rounds self-review 통과:

| File | 역할 | 상태 |
|------|------|------|
| `site_preference.py` | 75+ DOPANT_DB, multi-valence | ✅ verified |
| `substitute_compound.py` | Type A/B/B'/C/D doping | ✅ verified |
| `substitute_struct.py` | spread/cluster/chain methods | ✅ verified |
| `run_uma_screening.py` | UMA + Tier-1/2 metrics | ✅ verified |
| `run_anneal.py` | Langevin MD + relax | ✅ verified |
| `run_mlip_postproc.py` | EOS BM3 + finite-strain Cij | ✅ verified |
| `run_md_sigma.py` | σ_Li Arrhenius MD | ✅ verified (paper-grade σ_300K) |
| `bvse_proxy.py` | per-Li BVS + migration volume | ✅ verified (sign-corrected v4.5.11) |
| `combine_rankings.py` | multi-axis ranking | ✅ verified |
| `tier_cascade.sh` | 18-stage factory line | ✅ verified |
| `_provenance.py` | metadata stamp (21 scripts) | ✅ verified (v4.5.13 fully closed) |

### Layer 2 — Production code (tools/doping/, ML 측)

| File | 역할 | 상태 |
|------|------|------|
| `collect_dataset.py` | Layer 1 → CSV (~30 cols) | ✅ wired in Stage 09b |
| `train_predictor.py` | GBR per-target (5 targets) | ✅ wired in Stage 09c |
| `predict_new.py` | cold-start / with-structure inference | ⚠️ 정상 작동, but Nd2O3 60 데이터로만 학습됨 |
| `chain_predict.py` | Tier 1 → 2 gate logic | ⚠️ 동일 |
| `predict_best_site.py` | compound → site recommendation | ⚠️ 동일 |

→ Layer 2는 코드는 wire-up 됐지만 **dataset 부족**. 즉 *"코드 fix"* 보다
*"compound batch 추가 → dataset 키우기"* 가 우선.

### Paper #1 — Verified mechanism (필독/adhesion/v30u_ensemble/)
- R = +0.989, ρ = +1.000
- Cl-O R=+0.97, S-O R=-0.97, Li-O R=+0.77
- 4a/4d swap mechanism + Cl-Li-O bridge
- 36-registry ensemble, 36 lateral registries × 5 comp
- 새 slab builder 짜지 말고 이거 import해서 쓸 것

## 5. 알려진 문제와 처리 가이드

### Stage 11 v6 area mismatch (2026-05-18 발견)
- `run_cathode_interface.py`가 SE를 primitive로 stack → 234-325% strain
- v4.5.11 monitor만 추가 (fix 아님). 모든 baseline이 같은 contamination.
- **처리**: Layer 2 v1 학습에서 Wad target 빼고 진행. 나중에 v30u slab builder
  포팅으로 fix (옵션 C, deferred).

### KISTI charge sloshing (Job 726584/726844)
- Nd modelC DFT EOS, mixing_beta=0.05 + local-TF + maxstep=1000 도 부족
- iteration 130+ accuracy 1-11 Ry (target 1e-6) 진동
- **처리**: 별도 issue, Digital Twin core와 무관. UMA MLIP EOS (B0=20.0)으로
  paper #1에 인용 가능.

### Multi-compound batch 실행 중 (2026-05-20~) ✅
- **현재 ground truth = `tools/doping/master_batch_273.sh` (v4.5.20)**
- **91 compounds × 3 농도 (2/5/10%) = 273 cascades**
  - Phase 1A (37 oxides): +1~+6 valence 전범위 (Li2O Na2O Cu2O Ag2O / MgO ZnO CaO SrO BaO MnO CoO NiO / Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 Sm2O3 Gd2O3 Ga2O3 In2O3 Cr2O3 Fe2O3 B2O3 / SiO2 GeO2 SnO2 TiO2 ZrO2 HfO2 / V2O5 Nb2O5 Ta2O5 Sb2O5 / CrO3 MoO3 WO3)
  - Phase 1B (54): 불화물 10 + 염화물 19 + 브롬화물 5 + 요오드화물 4 + 질화물 5 + 황화물 11
  - 농도 3종 = concentration-aware Layer 2 feature (문헌 근거: Xiong2022 2%, Sundar2025 5%, Adeli2019 10%)
- **타임라인: ~193일 (6.4개월), 1 GPU sequential** — 스크립트 헤더에 명시된 의도된 규모
- gabia 진행 중 (2026-05-25 기준 ~7/273)
- ⚠️ **이 273이 최신 의도. 아래 v22(22-compound) plan doc은 superseded** (2026-05-18 구버전)

## 6. 다음 step (Priority order)

### Priority 1 — 273-batch 진행 + Layer 2 데이터 축적
- `master_batch_273.sh`가 알아서 resume/skip (5-trigger detection). 그냥 돌게 두면 됨.
- compound 완료마다 `dataset.csv` (45행 × 60물성) 생성 → 273개 pool이 Layer 2 학습셋
- **핵심: per-compound predictor(Stage 12b)는 deliverable 아님** (6-7점이라 R² 음수 정상). 273 pool → 단일 Layer 2 + LOCO가 산출물
- B2O3 포함 91개 모두 동등한 design-space 점. 특정 도펀트 "1등 증명"이 목적 아님

### Priority 2 — Layer 2 학습 정량 검증
- collect_dataset.py가 만든 CSV 컬럼 valid 확인
- train_predictor.py CV R² 정량 (target 별 ≥ 0.7 권장)
- predict_best_site.py로 leave-one-out compound prediction test

### Priority 3 — Paper #1 마무리 (paper-grade)
- 별도 paper, R=0.989 결과로 작성
- 본 Digital Twin paper와 분리해서 진행

### Priority 4 — Paper (Digital Twin 자체)
- Methodology + demonstration
- "Multi-tier ML platform for sulfide SE dopant screening"
- Layer 1 verification + Layer 2 cold-start accuracy + Case studies

## 7. CLAUDE.md / TIMELOG.md 와의 관계

- `CLAUDE.md` — 코드 생성 금지, inventory 먼저 보기 (절대 규칙)
- `CODE_INVENTORY.md` — 검증된 script 목록
- `README.md` — 프로젝트 비전 (이 문서와 일치)
- **이 문서** — 압축 후 Claude drift 방지용 north star

## 8. 의심스러우면 사용자께 묻기

다음 질문 패턴이 옳음:
- *"이 작업이 Layer 2 학습 데이터 확장에 기여하나요?"*
- *"이 코드 새로 짜는 거 아니라 검증된 도구 사용 맞나요?"*
- *"Nd2O3 narrative drift 중 아닌가요?"*
- *"paper #1 (R=0.989) vs Digital Twin paper 어느 쪽?"*

---

**마지막 한 줄**:
> Nd2O3는 1개 datapoint. Digital Twin Platform 구축이 본체.
> 코드 새로 짜지 말고 검증된 도구 사용. 사용자께 먼저 묻기.
