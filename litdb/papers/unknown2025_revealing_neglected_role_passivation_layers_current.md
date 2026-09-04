<!-- 🌱 research-agent 가 만든 **뼈대**다.  실물(PDF·SI)을 읽고 채워야 digest 가 된다.
     깊이 기준 = litdb/papers/_TEMPLATE.md · 실제 사례 = bazzoun2026_dem_fem_rnm_ionic.md.
     ⛔ `⏳ 문서 대기` 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->
# Revealing the Neglected Role of Passivation Layers of Current Collectors for Solid-State Anode-Free Batteries — ⏳ 문서 대기 (Advanced Materials 2025)

> slug `unknown2025_revealing_neglected_role_passivation_layers_current` · DOI `10.1002/adma.202513090` · type `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)`
> · PDF `⏳ 미확보` · digested `2026-09-03` · status `🌱 skeleton (문서 대기)`
> · evidence_level `snippet`
> · IF `26.8` · tier `A` · relevance `0.6`

## 0. 왜 이 카드가 열렸나 (research-agent 판정)
Advanced Materials(IF 26.8)이고 제목이 내 키워드 'anode-less assb'의 핵심 변수(집전체 계면)를 정면으로 다룬다. 2025년 9월 논문이라 1년 가까이 됐지만 전고체 anode-free 계면 설계의 기준 문헌이 될 가능성이 커서 포함한다. 단, 샌드박스에서 출판사 페이지 접근이 막혀 초록조차 확보하지 못했으므로 관련도는 보수적으로 0.6으로 두고 로컬 재분석을 요청한다.

## 1. 한 줄 요약
Advanced Materials(2025-09-07 온라인)에 실린 Western University·FZ Jülich·Univ. Twente 공동 논문으로, 전고체 anode-free 전지에서 그동안 간과된 집전체 표면 passivation layer의 역할을 다룬다 — 제목·서지 정보만 확보된 상태라 내용 요약은 전문 확보 후 보강해야 한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성·계 | 연구유형 |
|---|---|---|---|---|
| ⏳ 문서 대기 | Advanced Materials 2025 | 10.1002/adma.202513090 | ⏳ 문서 대기 | ⏳ 문서 대기 |

## 3. 핵심 물성 (수치) ★ 실물 필요
> ⛔ 초록만으로 채우지 말 것.  단위·조건 없는 값은 우리 db 와 **같은 표에 놓을 수 없다**.
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| ⏳ 문서 대기 |  |  |  |

## 4. 방법 ★ 실물 필요
- **code / version**: ⏳ 문서 대기
- **축 A(DEM/MPM/복셀)**: 접촉모델·강성·마찰·압축압력·입경분포·셀·복셀 크기 —
- **축 B(DFT/MLIP)**: functional·vdW·pseudo/PAW·k-points·ecut·supercell·U·MLIP 학습셋 —
- **축 C(실험)**: 셀 구성·면적용량·온도·율·EIS 조건·등가회로 —
- **무질서·상태 선택 규칙**(있으면):
- **특이사항**:

## 5. Figure set ★ 실물 필요
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| ⏳ 문서 대기 |  |  |

## 6. Post-processing ★ 실물 필요
- **무엇**: (NEB / BVSE / COHP / TauFactor / Kirchhoff / Heckel / CNLS fit …)
- **도구**:
- **수치화·플롯 방식**:

## 7. 우리 대비 ★ 실물 필요 — 이 카드의 값어치는 여기서 나온다
- **어느 축인가**: (A: DEM/MPM/복셀 · B: DFT/MLIP · C: 실험 EIS · none)
- **우리 확보값과의 일치/충돌**: → `db/properties/canonical_registry.json`(축 B) ·
  `docs/db/section7_10case_sweep.csv`(축 A) 와 대조
- **인용 포인트**: (축 A = `main.tex` 절 이름 / 축 B = `kb/` 카드 또는 `db/properties/` 항목)
- **비판 포인트**: (보고량 정의가 있는가 · 상태 선택 규칙이 있는가 · 수렴을 보였는가 ·
  DEM↔MPM 을 서로 보정했는가[frame[4] 위반] · DOS-threshold 갭 · 단일시드 σ 비)

## 8. research-agent 초록 판정 (실물 판독으로 대체될 것)
- 확보된 정보: 제목, 저널(Advanced Materials), 온라인 게재일 2025-09-07, DOI 10.1002/adma.202513090, 기관(Western University, Flex-N-Gate, FZ Jülich, Univ. Twente), 저자 10명(명단 미확보).
- 제목이 시사하는 주제: 집전체(예: Cu, SUS, Al)의 native passivation layer(산화막 등)가 전고체 anode-free 셀의 Li 석출·계면 저항·수명에 미치는 영향.

## 9. 남은 일
- [ ] PDF·SI 확보 → §3–§7 채우기
- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로
- [ ] `INDEX.md`(argyrodite SE 축) 또는 `INDEX_DEM.md`(DEM 축)에 **손으로** 등재
