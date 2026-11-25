# 디지털 트윈 + ML Screening 프로젝트 로드맵

> **프로젝트 전체 그림**과 단계별 milestone, KPI, 자원 계획.
> 안용훈 PhD candidate 주도, 2026-05-15 기준.

---

## 🎯 비전

**"황화물 SE / 코팅 / 양극 시스템의 자율 디지털 트윈"**:

원자 수준 시뮬레이션 (UMA + ML surrogate) + 실험 데이터 + 문헌 자동화 →
새로운 코팅 소재를 1년 내 발견 + 검증 가능한 플랫폼 구축.

**최종 deliverable**: 학계/산업체가 사용할 수 있는 **open platform**
(우리 lab 운영 + 외부 partnership).

---

## 📊 단계별 KPI

### Phase 0 — Foundation 검증 (완료, 2026-05-14)
- [x] UMA로 paper W_ad 5/5 strict rank 재현 (R=+0.989)
- [x] 3대 표면 driver 식별 (Cl-O, S-O, Li-O)
- [x] 메커니즘 정량 검증 (vacancy 2.6×, bulk Cl R=+0.97)
- [x] Robustness 확인 (α, cutoff, slab)
- [x] Mechanism MD + defense 완성
- [x] 검증된 scripts 7개 (`scripts/adhesion/`)

### Phase 1 — POC: 100 도핑 후보 (3-6개월)

**목표**: LPSCl 기반 cation/anion 단일 도핑 100 후보 UMA screening.

**Deliverables**:
- [ ] atomate2 setup + UMA integration
- [ ] `scripts/doping/site_preference.py` — site 자동 선택
- [ ] `scripts/doping/run_single_dopant.py` — 100 후보 자동 실행
- [ ] `scripts/descriptors/compute_tier1.py` — Tier-1 descriptor 자동 계산
- [ ] DB: 100 후보 × 15 descriptor 결과
- [ ] Top-10 후보 mechanism MD 작성

**KPI**:
- 100 후보 screening 완료 (UMA 기준 1주일)
- Top-10에 paper 검증 5개 모두 포함 (sanity check)
- 추가 신규 5개 후보 식별 + 정량 평가

**자원**: GPU 1대 (gabia), Claude (디지털 어시스턴트), 본인 시간 30% (병행).

### Phase 2 — Scale-up + ML Surrogate (6-12개월)

**목표**: 10,000 후보 screening + active learning.

**Deliverables**:
- [ ] MACE 또는 Allegro surrogate model 학습 (Layer 1 데이터 활용)
- [ ] Surrogate 성능 검증 (R > 0.9 vs UMA)
- [ ] BoTorch active learning loop
- [ ] Co-doping (cation + anion) enumeration
- [ ] SQS for mixed compositions
- [ ] 10,000 후보 screening (Surrogate)
- [ ] Top-100 UMA 정밀 검증

**KPI**:
- Surrogate inference 1000× faster than UMA
- Active learning이 random search 대비 5× efficient
- Top-100에 paper-aligned + novel candidates 포함

**자원**: GPU 2-4대, atomate2 cluster setup, 본인 시간 50%.

### Phase 3 — Production + 실험 Partnership (12-24개월)

**목표**: Pareto 다목적 최적 후보 → 실험 합성 → 검증.

**Deliverables**:
- [ ] Inverse design (generative model: VAE 또는 GFlowNet)
- [ ] DFT validation (atomate2-VASP, HSE06)
- [ ] Pareto front (W_ad + σ + 비용 + 안정성)
- [ ] 실험 partner와 top-5 합성
- [ ] Literature auto-DB 통합 (PaperQA 등)
- [ ] Web UI (Streamlit, 외부 접근)

**KPI**:
- DFT-UMA-experiment 3-way agreement R > 0.9
- 합성된 top-5 중 ≥1개가 paper 베스트 (comp3=316 aJ) 능가
- Platform 외부 사용자 ≥10명 (학계)

**자원**: 합성 실험 (외부 partner), 본인 + 후배 1명.

### Phase 4 — Open Platform (24-36개월)

**목표**: 학계/산업 공개. 논문 + open source release.

**Deliverables**:
- [ ] Top-tier paper (Nature Energy / Joule / Adv. Mater.)
- [ ] Github open release (atomate2 module 형태)
- [ ] Web platform (Materials Project처럼)
- [ ] Tutorial + workshop

**KPI**:
- 논문 published
- Github star ≥100
- 외부 lab adoption ≥3

---

## 🏗️ Architecture (재정리)

```
┌─────────────────────────────────────────────────────────────┐
│                  USER INTERFACE                              │
│  (Streamlit / Jupyter / CLI / claude-code agents)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION (atomate2 + jobflow)             │
│  • Doping enumeration  • Descriptor computation             │
│  • UMA workflow        • DFT validation                     │
│  • DB management       • Active learning loop               │
└─────────────────────────────────────────────────────────────┘
        ↓                       ↓                    ↓
┌──────────────┐  ┌─────────────────────┐  ┌──────────────────┐
│ COMPUTE      │  │ ML / DESCRIPTORS    │  │ DATA / LITERATURE │
│ Layer (UMA,  │  │ Surrogate (MACE),   │  │ MongoDB, raw.json,│
│ MACE, DFT)   │  │ dscribe, matminer   │  │ OpenAlex DB       │
└──────────────┘  └─────────────────────┘  └──────────────────┘
        ↓                       ↓                    ↓
┌─────────────────────────────────────────────────────────────┐
│                     STORAGE / DB                             │
│  Local: data/, kb/literature_db/   Cloud: optional NOMAD     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧱 기술 stack 결정

| 컴포넌트 | 선택 | 이유 |
|---------|------|------|
| 워크플로우 | **atomate2** | MLIP 통합, modular, MP 호환 |
| MLIP Layer 1 | **UMA-s-1p1** | 본 연구 검증 R=+0.989 |
| MLIP Layer 2 | MACE-MP-0 (저장 학습) | Foundation + transfer learning |
| Descriptors | dscribe + matminer + custom | SOAP/MBTR + composition + 우리 검증 14-pair |
| ML Surrogate | MACE / scikit-learn ensemble | atomate2 통합 + interpretable baseline |
| Active learning | BoTorch + Ax | Multi-objective 강력 |
| DB | MongoDB (atomate2 default) | jobflow native |
| Literature | OpenAlex + Semantic Scholar + chroma | 무료 + 의미 검색 |
| AI 요약 | Claude API | 한국어 + 우리 맥락 |
| Version control | Git (이 repo) | 표준 |
| Visualization | matplotlib + plotly + ovito/vesta | publication + interactive |

---

## 📅 단계별 timeline (gantt-like)

```
Phase 0 (DONE)    ━━━━━━━━━━ 2026-05
Phase 1 (POC)               ━━━━━━━━━━━━━━━━━━━━━━ 2026-05 ~ 2026-11
Phase 2 (Scale)                      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2026-08 ~ 2027-05
Phase 3 (Exp)                                  ━━━━━━━━━━━━━━━━━━━━━━━━━━ 2026-12 ~ 2028-05
Phase 4 (Open)                                                 ━━━━━━━━━━━━━━━━━━━━━━ 2027-06 ~ 2029-05
```

---

## 💰 자원 계획

### 컴퓨팅
- **Phase 1**: GPU 1대 (현재 gabia, sufficient)
- **Phase 2**: GPU 2-4대 (cluster 추가 필요 or AWS spot)
- **Phase 3-4**: GPU 4-8대 + DFT 노드 (KSC/PLSI 신청)

### 인력
- **Phase 1**: 본인 only (Claude assistant 활용)
- **Phase 2**: 후배 1명 (descriptor / ML 학습 후 합류)
- **Phase 3**: 합성 partner (외부 lab — argyrodite 합성 경험 가진 그룹)
- **Phase 4**: 산업 partner (양산 검증)

### 예산
- atomate2 / UMA 무료
- Claude API ~$200/월 (literature 요약 + 코딩 보조)
- AWS GPU spot ~$500/월 (Phase 2 이상)
- 합성 실험 (Phase 3): partner와 협의

---

## 🎓 학습 / Skill development

### Self-learning (본인)
- [ ] atomate2 tutorial 완주 (1주)
- [ ] MACE / NequIP 개념 학습 (2주)
- [ ] Bayesian optimization 기초 (BoTorch tutorial, 1주)
- [ ] Active learning literature 리뷰 (2주)
- [ ] Materials genome project 개념

### 외부 도움
- atomate2 GitHub discussions
- Materials Project Workshop (annual)
- BML Lab 동료 / 교수님 conjsultation

---

## 🚦 리스크 + 완화

| 리스크 | 영향 | 완화 방안 |
|--------|------|----------|
| UMA가 새 chemistry에서 부정확 | 큼 | DFT spot check (Phase 1 마지막 5개) |
| atomate2 학습 곡선 | 중 | 후배 1명 합류 시 빨라짐 |
| MACE surrogate fitting 실패 | 중 | 대안: GBT, modnet |
| 합성 partner 부재 | 큼 | BML 내부 + 외부 lab 미리 접촉 |
| 학회 발표 / 논문 timeline 늦어짐 | 중 | Phase 1 결과로 conference paper 먼저 |
| Claude usage 비용 | 작 | $200/월 cap 설정 |

---

## 📈 성공 정의 (Vision)

**1년 후 (Phase 1 + Phase 2 일부 완료)**:
- 100+ 검증된 LPSCl 도핑 후보 DB
- Top-10에 paper 베스트 (316 aJ) 능가하는 novel 후보 ≥1개
- 학회 발표 (MRS / ECS) 1편

**3년 후 (Phase 4 완료)**:
- 학계/산업 공개 디지털 트윈 platform
- Top-tier 논문 published
- 산업 partner 1개 이상

**5년 후 (확장)**:
- 황화물 외 산화물/할라이드 SE로 확장
- Solid-state battery 전체 시스템 (anode + SE + cathode) 통합

---

## 🔗 핵심 reference 문서

- 현재 메커니즘: `kb/papers/mechanism_anion_O_descriptor.md`
- Descriptor 카탈로그: `kb/descriptors/coating_descriptor_catalog.md`
- ML 플랫폼: `kb/platforms/ml_automation_platforms.md`
- Literature 도구: `kb/platforms/literature_db_tools.md`
- 도핑 알고리즘: `kb/methodology/doping_substitution_algorithm.md`
- 작업 로그: `TIMELOG.md`

---

## 다음 action items (immediate)

1. [ ] atomate2 설치 + UMA workflow 테스트 (gabia에서)
2. [ ] `scripts/doping/` 첫 스크립트 작성 (site preference filter)
3. [ ] `scripts/automation/literature_harvest.py` 구현 (OpenAlex)
4. [ ] 100 후보 dopant list 작성 + cost/safety filter
5. [ ] BML 교수님과 Phase 1 plan 논의
