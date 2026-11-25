# Yonghoon-DEM-DFT — 전고체전지(황화물 SE) 계산 캠페인 repo

BML Lab (한양대) · 안용훈. 아지로다이트 황화물 고체전해질의 도핑·계면·수송을
**DFT(QE) · MLIP-MD(UMA) · BVSE · DEM** 으로 계산하고, 그 값이 **인용해도 되는지**까지
원장으로 관리한다. 값보다 **판정과 금지**가 이 repo 의 본체다.

## 여기서 시작

| 묻는 것 | 정본 |
|---|---|
| **규율** — 무엇을 하면 안 되나 | **`CLAUDE.md`** ← 먼저 읽는다 (표준은 이 한 벌이다) |
| **지금 상태** | `kb/open_items.md` 의 ⏭ 절 · 기계 실측은 `kb/projects/restart_runbook_2026_09_07.md` |
| **판정** | `db/governance/decisions.json` (`active` 만 유효) |
| **값** | `db/properties/canonical_registry.json` |
| **금지** | `db/properties/citation_hazards.json` |
| **리뷰 왕복** | `kb/reviews/INDEX.md` (코드 체계는 `kb/CODES.md`) |

## 살아 있는 폴더

| 폴더 | 무엇 |
|---|---|
| `db/` | **수치 정본**(`properties/`·`structures/`)과 **판정 원장**(`governance/`). 숫자의 유일한 권위 |
| `kb/` | 사람이 읽는 해석 위키 — 규칙은 `kb/SCHEMA.md`, 색인 `kb/index.md`(생성물) |
| `litdb/` | 문헌 정본 — digest + `INDEX.md` + `comparison_vs_ours.md` + 크로핑 그림 |
| `tools/` | 계산·분석·그림 도구 (py·sh 수백 개 — **새로 짜기 전에 `grep -rl` 먼저**) |
| `webapp/` | 값·판정·금지를 사람이 보는 화면 (claim 결속 규율은 CLAUDE.md) |
| `runs/` | 실행 산출물 — **불변 원본, 수정 금지** |
| `research-agent/` | 논문 자동비서 (별도 지침: `research-agent/CLAUDE.md`) |

`docs/` `figures/` `factory/` `archive/` 는 산출물·보관소다.
작업 로그는 `TIMELOG.md` 가 아니라 **git log** 다 (TIMELOG 은 2026-06 이후 안 쓴다).

---

<details>
<summary><b>📦 2026-05 판 원문 (아카이브 — 지우지 않는다)</b></summary>

> ⚠ **아래는 2026-05-15 시점 문서다. 지금 사실과 다른 것이 많다** —
> 스스로를 "project bible" 이라 부르지만 `tools/` · `db/` · `litdb/` · `webapp/` · `runs/` 가
> 구조도에 하나도 없고, 대신 없는 경로(`scripts/descriptors/` · `data/final_combo/`)를 가리킨다.
> Phase 1–3 로드맵과 3-tier 아키텍처는 **당시 계획**으로 읽는다.
> ⚠ 여기 적힌 **R=+0.989** 는 20 시드 중 5 시드를 고른 판이다 —
> 100 시드 통계(`kb/results/adhesion_100seeds_analysis.md`)에서 일부 순위가 뒤집힌다.
> W_ad 는 `canonical_registry.json` 에도 `citation_hazards.json` 에도 **등록돼 있지 않다**.

# 📚 BML Argyrodite / Sulfide Coating Digital Twin Project — Bible

> **Last updated**: 2026-05-15
>
> 본 repo는 BML Lab (Hanyang University)의 **할로겐 치환 argyrodite 황화물
> SE / NCM 양극 접착 및 디지털 트윈 기반 머신러닝 소재 스크리닝 프로젝트**의
> 중앙 저장소. 안용훈 PhD candidate 주도.

---

## 🎯 프로젝트 전체 비전

전고체 배터리 복합양극에서 황화물 SE와 코팅 소재의 계면 안정성을 결정하는
원자 수준 메커니즘을 UMA MLIP로 정량 검증하고, 이를 기반으로 **자동화된
머신러닝 소재 스크리닝 디지털 트윈 플랫폼**을 구축한다.

**3-tier 시스템 아키텍처**:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: ACTIVE LEARNING + INVERSE DESIGN                  │
│  → Pareto multi-objective optimization                      │
│  → Composition-property maps                                │
│  → Top-N candidate suggestion to experiment partner         │
└─────────────────────────────────────────────────────────────┘
                            ↑ retrain
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: ML SURROGATE (GNN / GBT / SchNet / MACE)          │
│  → Trained on Layer 1 data                                  │
│  → 1000x faster inference than UMA                          │
│  → 10⁴~10⁵ candidate screening per day                       │
└─────────────────────────────────────────────────────────────┘
                            ↑ training data
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: UMA-s-1p1 (FAIRChem)                              │
│  → DFT 정확도, no SCF cost                                   │
│  → 100~1000 candidates/day                                  │
│  → ALREADY VALIDATED: R=+0.989 vs paper experiment          │
└─────────────────────────────────────────────────────────────┘
                            ↑ occasional check
┌─────────────────────────────────────────────────────────────┐
│  Foundation: DFT (VASP/QE, HSE06/PBE)                       │
│  → New chemistry validation                                  │
│  → 10/year                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Repository 구조

```
Yonghoon-DEM-DFT/
├── README.md                    # ← 이 파일 (project bible)
├── TIMELOG.md                   # 시간순 작업 로그
│
├── kb/                          # Knowledge base (지식 베이스)
│   ├── papers/                  # 핵심 mechanism 문서
│   │   └── mechanism_anion_O_descriptor.md  # ★ 현재 paper용
│   ├── descriptors/             # 황화물 코팅 descriptor catalog
│   │   └── coating_descriptor_catalog.md    # ★ 필수 reference
│   ├── platforms/               # ML/automation 플랫폼 survey
│   │   ├── ml_automation_platforms.md       # ★ ML platforms
│   │   └── literature_db_tools.md           # ★ literature 자동화
│   ├── methodology/             # 방법론 문서
│   │   └── doping_substitution_algorithm.md # ★ LPSCl 도핑
│   ├── projects/                # 프로젝트 로드맵
│   │   └── digital_twin_roadmap.md          # ★ 큰 그림
│   └── literature_db/           # 자동화 literature DB (proposed)
│
├── scripts/
│   ├── adhesion/                # ★ 현재 검증된 adhesion 분석 (R=+0.989 결과)
│   ├── doping/                  # LPSCl 도핑/치환 알고리즘 (구현 예정)
│   ├── descriptors/             # descriptor 계산 (구현 예정)
│   └── automation/              # 자동화 파이프라인 (구현 예정)
│
├── data/
│   ├── final_combo/             # 현재 5-comp adhesion 데이터
│   └── doping_screening/        # screening 결과 (예정)
│
├── figures/                     # paper figures
│
└── archive/                     # 폐기/대체된 파일
    ├── deprecated_scripts/      # superseded scripts
    └── old_md/                  # outdated MD content
```

---

## ✅ 검증 완료된 기반 (Foundation)

### Paper-validated UMA pipeline (2026-05-14)

- **R=+0.989, ρ=+1.000** vs paper W_ad 실험 (5/5 strict rank)
- 메커니즘 정량 검증: Cl-O attractive (R=+0.975), S-O repulsive (R=−0.973),
  Li-O attractive (R=+0.771), Li-vacancy migration (Li₅.₄ 2.6× Li₆),
  bulk Cl Madelung (R=+0.97)
- Robustness: α ∈ [0.8, 1.5], Li-O cutoff [2.4, 3.6] Å, slab dataset robust
- 자세한 내용: [`kb/papers/mechanism_anion_O_descriptor.md`](kb/papers/mechanism_anion_O_descriptor.md)

### 검증된 scripts (재사용 가능)

`scripts/adhesion/`:
- `plot_R0988_TIGHT_FIT.py` — paper figure 생성
- `bond_density_36reg_FAST.py` — 36-reg averaged bond density (vectorized)
- `bond_density_LiO_cutoff_sweep.py` — cutoff sensitivity
- `run_li_migration_FINAL_combo.py` — vacancy migration test
- `alpha_sensitivity_FINAL.py` — α robustness
- `comprehensive_FINAL_analysis.py` — halogen depth + Cl regression
- `generate_stacked_deq_orthogonal.py` — d_eq stacked structure generator

---

## 🚀 다음 단계 (Phase 1-3)

### Phase 1 — POC: 100 doping 후보 UMA screening (3-6개월)
- LPSCl base + cation/anion site doping enumeration
- UMA로 W_ad + ionic conductivity 평가
- Descriptor catalog 확립

### Phase 2 — ML surrogate + active learning (6-12개월)
- Layer 1 데이터로 GNN/MACE 학습
- Active learning 루프 구축
- 10,000 후보 추론 + 정밀 검증

### Phase 3 — Inverse design + 실험 partnership (12-24개월)
- Pareto multi-objective optimization
- 실험 파트너와 top-10 candidate 검증
- Literature auto-DB 통합

---

## 📖 핵심 문서 빠른 링크

| 주제 | 문서 |
|------|------|
| 현재 paper 메커니즘 | [`kb/papers/mechanism_anion_O_descriptor.md`](kb/papers/mechanism_anion_O_descriptor.md) |
| Descriptor 카탈로그 | [`kb/descriptors/coating_descriptor_catalog.md`](kb/descriptors/coating_descriptor_catalog.md) |
| ML 자동화 플랫폼 survey | [`kb/platforms/ml_automation_platforms.md`](kb/platforms/ml_automation_platforms.md) |
| 문헌 자동 DB 도구 | [`kb/platforms/literature_db_tools.md`](kb/platforms/literature_db_tools.md) |
| LPSCl 도핑 알고리즘 | [`kb/methodology/doping_substitution_algorithm.md`](kb/methodology/doping_substitution_algorithm.md) |
| 디지털 트윈 로드맵 | [`kb/projects/digital_twin_roadmap.md`](kb/projects/digital_twin_roadmap.md) |

---

## 🛠️ Tech stack

**현재 사용 중**:
- UMA-s-1p1 (FAIRChem) — energy/force
- ase + pymatgen — structure manipulation
- numpy/scipy — analysis
- matplotlib — visualization

**도입 계획**:
- aiida — high-throughput workflow
- atomate2 — Materials Project automation
- matminer + dscribe — descriptor computation
- modnet/mace — surrogate ML
- skopt / optuna — Bayesian optimization
- Semantic Scholar API / OpenAlex — literature scraping
- bibtex / zotero API — citation management

---

## 👤 Contact

안용훈 (Yonghoon An)
- BML Lab, Hanyang University
- PhD Candidate
- Project lead

Co-developed with **Claude (Anthropic)** as the digital research assistant.

</details>
