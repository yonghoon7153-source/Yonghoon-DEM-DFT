# `factory/` — Physical-AI 자율 검증 파이프라인 (v1)

**목표 (확정)** 도핑/조성 입력 → 기존 DFT·MLIP 도구를 오케스트레이션 → **표준 "전기화학 report card"** 1개.
**범위** In-silico 전용(계산 + testable 예측) · **자율성** Human-in-loop 게이트 · **상태** v1 foundation 구축 중.

> 우리가 b2o3에서 **손으로** 해온 BVSE→MD(σ)→ESW→SEI→hull→elastic→DOS→charge→phonon→XPS 를 **표준화·자동화·이력추적**하는 층. "physical AI smart factory"의 토대.

---

## 1. 5-층 구조 (전체 비전 중 v1 위치)
| 층 | 내용 | 상태 |
|---|---|---|
| 데이터 | `db/`(구조·물성) + `kb/`(결과·방법론) | ✅ 보유 |
| 검증/측정 | `tools/`(BVSE·MD·ESW·SEI·hull·elastic·DOS·charge·phonon) = 계측기 | ✅ 보유 |
| 선별 | cascade (tier descriptor) | ✅ 보유 |
| **오케스트레이션 (v1)** | **조성→스테이지 자동실행→report card** (이 디렉터리) | ▶ 구축중 |
| Surrogate AI | DB로 물성 예측(능동학습) | ☐ v2 |

### 1.1 전체 흐름 (조성 → 구조 → 특성)
```
cascade           structure_discovery (Stage 0, DFT/MLIP)          report card
(조성 지명)  ──▶   enumerate → screen → anneal → MLIP-EOS      ──▶   transport·hull·ESW·
                  → DFT relax(basin check) → DFT-EOS → V0구조        mechanical·electronic·
                                                                     structure·phonon·anode
```
- **cascade**는 *조성*만 지명. **structure_discovery**(`registry/stages.yaml` + `kb/methodology/argyrodite_mechanical_pipeline.md`)가 그 조성을 **실제 V₀ 챔피언 구조**(`db/structures/<id>_relaxV0.cif`)로 만든다 — D'Amore 2022(polymorph)·Pustorino 2025(Li-ordering) 기반, basin cross-check 포함. **b2o3는 이 파이프라인을 거쳐 나옴**(`tools/doping/b2o3_enumerate→anneal→dft_eos`).
- 그 V₀ 구조가 **report card의 모든 섹션의 입력.** 즉 factory = **구조발견(upstream) → 특성화(report card)** 한 줄로 연결.
- **일반화 TODO**: b2o3 전용 스크립트(`b2o3_*.py`)를 임의 조성용(`enumerate_anion.py`·`run_li_anneal.py`·basin-RMSD 자동)으로 — 이게 factory가 신규 후보의 구조까지 자율 발견하는 핵심 build-out.

## 2. v1 구성요소
| 파일 | 역할 |
|---|---|
| `schema/report_card.schema.json` | **표준 산출물** — 전기화학 report card 스키마(계약) |
| `registry/stages.yaml` | **스테이지 카탈로그** — 각 물성 ↔ 도구·입출력·계산위치·비용·신뢰도·게이트 |
| `assemble_report_card.py` | **assembler** — 한 계의 `db/` 결과를 읽어 card(JSON+MD) 생성 |
| `cards/<id>_report_card.{json,md}` | 생성된 카드 (예: `b2o3`) |

## 3. report card 섹션 (표준 전기화학 산출물)
`transport`(σ300/273·Ea·BVSE) · `thermodynamic_stability`(e_hull·분해) · `electrochemical_window`(ESW·SEI gap) · `mechanical`(B/G/E/ν) · `electronic`(gap·N(E_F)) · `structure_chemistry`(배위·결합·산화상태) · `dynamical_stability`(허수모드) · `testable_predictions`(XPS/Raman/NMR) · `overall`(요약·flag·정직한계).

각 섹션은 **`status`(done/pending/n.a.) + `confidence`(A/B/C) + `method` + `source` + `caveats`** 를 항상 포함 → 과대주장 방지. **`source`는 스크립트가 실제로 읽는 파일만** 표기(자동화 허위귀속 금지; 수기 curation은 `curation:manual` 명시).

**confidence rubric** — A = DFT, 수렴, multi-witness 또는 실험검증 · B = single-config DFT/MLIP 또는 상대값 · C = fast proxy(스크리닝).

**roadmap descriptors (인정하되 미계산, status:n.a.)** — 신뢰 가능한 SE 카드가 아직 빚진 것: **anode-interface 안정성**(ESW 하한 1.72 V = Li 근처 환원, 헤드라인 리스크) · **임계전류밀도/dendrite(CCD)** · **grain-boundary 수송**(bulk σ ≠ total σ) · **공기/수분(H₂S) 안정성**(thioborate 민감) · **전자전도도**(self-discharge). 카드에 n.a.로 노출 → reviewer가 누락 아닌 "인지됨"으로 봄.

## 4. Human-in-loop 게이트 (자율성)
오케스트레이터(v1.1)는 스테이지 사이에 게이트:
1. **prep gate** — 구조 relax 확인 후 진행
2. **cost gate** — 비싼 스테이지(elastic·DFPT) 전 승인
3. **rank gate** — 최종 report card/추천 전 사람 검토
게이트 = 신뢰·논문급 검증 우선. 완전자율은 신뢰 쌓인 뒤.

## 5. 로드맵
- **v1.0 (지금)** schema + registry + assembler + b2o3 카드 (기존 DB로 작동 증명)
- **v1.1** 오케스트레이터(스테이지 dispatch + 캐시 + provenance + 게이트), KISTI/gabia 백엔드
- **v1.2** 신규 조성 end-to-end(구조생성→전체검증→카드)
- **v2** Surrogate AI(능동학습) — 사전선별로 비싼 계산 절감
- **품질** 외부리뷰 번들 + 백그라운드 code-review/science-audit 에이전트(CI식)

## 6. 정직한 경계 (외부 peer-review 반영)
- **현재 정체는 "provenance-discipline가 강제된 assembly + plan-only 스케줄러"** — 표준 도구(BVSE·MLIP-MD·ESW·hull·phonon·Bader)를 **오케스트레이션·표준화**하는 층이지, **새 물리·calibration·UQ·surrogate를 도입한 방법론적 기여는 아님**(그건 v2). README의 "autonomous/physical-AI" 표현은 **포부**이고 현 구현은 **사람이 명령을 실행하는 plan-only**임. 과대표현 금지.
- **계산 결과 + testable 예측**까지. 실제 CV/EIS/cycling = 물리 랩 루프(별도) 또는 실험데이터 surrogate.
- 절대 σ 등은 MLIP 한계 명시(card의 caveats). **Ea·상대비·정성결론이 robust 축.** 단 **현재 단일-trajectory라 error bar 없음** → multi-seed 필요(v2).
- **b2o3는 "SCREENED candidate"지 "validated champion" 아님.** 가장 결정적 위험인 **anode-interface 안정성(Li-metal 환원)이 미계산** — 그게 나오기 전엔 positive 추천 불가. (외부리뷰 #1)
- **UQ 부재**: A/B/C는 사람 판단이지 calibrated confidence 아님. provenance manifest도 입력 해시·MLIP/MP 버전 pin 없음(재현성 한계).

## 참고
- 첫 카드: `cards/b2o3_report_card.md` · 스키마: `schema/report_card.schema.json`
- 검증층 도구: `tools/` · 데이터: `db/` · 방법론: `kb/methodology/`
