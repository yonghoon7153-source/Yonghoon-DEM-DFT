---
title: "Planar Li deposition and dissolution enable practical anode-free pouch cells"
aliases: ["Planar Li deposition and dissolution enable practical"]
authors: ["Lei Liu", "Yuxuan Xiang", "Xingyu Lu", "Jianhui Wang"]
journal: "Nature"
year: 2026
doi: "10.1038/s41586-026-10402-0"
url: "https://www.nature.com/articles/s41586-026-10402-0"
if: 48.5
tier: "A"
relevance: 0.55
status: digested
keywords: ["anode-less assb"]
tags: ["paper/anode-free", "tier/A", "topic/planar-deposition", "topic/SEI", "system/liquid-electrolyte", "journal/Nature"]
source: bootstrap
date_added: 2026-09-03
analyzed_at: 2026-09-03
evidence_level: fulltext
ra_id: "doi:10.1038/s41586-026-10402-0"
---

# Planar Li deposition and dissolution enable practical anode-free pouch cells

**Lei Liu, Yuxuan Xiang, Xingyu Lu, Jianhui Wang** — *Nature* (2026) · IF 48.5 · Tier A · 관련도 0.55
DOI: [10.1038/s41586-026-10402-0](https://doi.org/10.1038/s41586-026-10402-0)
키워드: [[anode-less assb]]

> [!abstract] 한 줄 요약
> Liu et al.(Westlake Univ.)은 LiDFOB/NDFA 기반 'crossover-coupled' 전해질로 8 nm 두께의 균질한 B–F 고분자계 SEI를 만들어 Cu‖NCM811 anode-free 파우치셀(5.6 mAh cm⁻², 2.7 Ah)에서 Li의 2차원 평면 석출·용해를 구현했고 508 Wh kg⁻¹·100 % DOD 100 사이클(80 % 유지)을 보고했다.

## 선정 이유
Nature(IF 48.5)라 IF 순위 최상위지만, 액체 전해질 anode-free 논문이라 내 키워드 'anode-less assb'와는 시스템이 다르다. 그래도 '평면 석출을 만드는 계면 조건(SEI 균질성·기계적 유연성)'은 전고체 anode-free에서도 같은 설계 변수이므로, 배경·논리 인용용 Tier A로 유지하되 관련도는 0.55로 낮춰 잡는다.

## 핵심 내용
- SEI의 micro-heterogeneity와 기계적 취약성이 Li 석출·용해 불균일의 근원이라는 진단에서 출발해, 전해질 설계로 SEI 자체를 균질화했다.
- 1.6 M LiDFOB in NDFA 전해질에서 라디칼 종이 음극(3.9 V)에서 양극(4.2 V)보다 먼저 생성되는 위치 의존 계면 반응이 일어나, B–F 기반 고분자가 풍부한 'self-adaptive mesh-film' SEI(두께 8 nm, sub-nm 균질도)가 형성됐다.
- Cu‖NCM811 anode-free 파우치셀에서 5.6 mAh cm⁻², 2.7 Ah, 508 Wh kg⁻¹(1,668 Wh L⁻¹); 100 % DOD 100 사이클, 80 % DOD 250 사이클에서 80 % 용량 유지.
- 출력 2,650 W kg⁻¹(96 Wh kg⁻¹ 기준), 작동 온도 −40~100 °C.
- cryo-FIB-SEM/cryo-TEM, in situ EPR, 고체/액체 NMR로 SEI 구조와 라디칼 형성을 추적했다 — 계산(DFT/MD)은 사용하지 않았다.

## 방법
- **시스템**: Cu 집전체 ‖ NCM811, 액체 전해질 1.6 M LiDFOB/NDFA (interlayer·host 없음)
- **기법**: 전해질 설계(crossover-coupled) + cryo-FIB-SEM, cryo-TEM, SEM-EDS, AFM, XPS, Raman, ss/liquid NMR, in situ EPR, 질량분석, 3D 재구성
- **파라미터**: 5.6 mAh cm⁻², 2.7 Ah 파우치, 100 % DOD / 80 % DOD, SEI 8 nm, −40~100 °C
- **검증**: 파우치셀 사이클링 + 다중 분광/현미경 상관; 시뮬레이션 없음

> [!tip] 내 연구와의 연결
> **DEM** — -
> **DFT/MLIP** — SEI 형성 메커니즘(라디칼 선행 생성)은 DFT/AIMD로 검증 가능한 주제라, 내 SEI 형성 에너지(Nd₂O₃ 도핑 LPSCl) 프레임을 액체계 대비 '고체 계면에서는 어떤 상이 먼저 생기는가'로 확장하는 아이디어를 준다.
> **Anode-free** — 전고체 anode-free에서는 SEI 대신 SE/집전체 계면과 압력이 평면 석출을 결정한다. 이 논문의 '계면의 기계적 유연성 + 빠른 Li⁺ 수송 = 평면 석출' 논리는 황화물 SE 계면 설계(interlayer 연성, 접촉 균일성)에 그대로 옮길 수 있는 설계 원칙이다.

### 비교할 수치
- 면적 용량 5.6 mAh cm⁻² (액체 anode-free) vs 황화물 anode-free 보고값(보통 1~3 mAh cm⁻², 압력 수 MPa~수십 MPa) — 리뷰 작성 시 대비표
- SEI 두께 8 nm vs 황화물 SE/집전체 interlayer 두께(Ag–C 수 µm, 액체금속 나노드롭 등)

## 논문 작성에 쓸 곳
- **Introduction**: 'anode-free 셀의 수명은 계면의 균질성과 기계적 안정성이 좌우한다'는 일반 명제의 최신 근거로 인용(액체계지만 Nature급 데이터).
- **Methods**: 
- **Discussion**: 전고체 anode-free에서 평면 석출을 유도하려면 액체계의 SEI 역할을 SE/집전체 계면과 stack pressure가 대신해야 함을 대비시키며, 내 DEM 접촉 균일성 지표를 '평면 석출 조건'으로 해석하는 문단에 사용.

> [!quote] 인용 문장 초안
> Even in liquid-electrolyte anode-free cells, planar Li deposition and dissolution are governed by the homogeneity and mechanical compliance of the interphase [ref], a design principle that translates to the solid-electrolyte/current-collector interface in anode-free all-solid-state batteries.

> [!warning] 비판 포인트 / 세미나 질문
> - 액체 전해질 시스템이라 ASSB의 핵심 변수(stack pressure, SE 크리프, 계면 공극)가 아예 없다 — 내 키워드에 잡힌 것은 'anode-free' 용어 때문이며 ASSB 데이터로 인용하면 안 된다.
> - 100 % DOD 100 사이클, 80 % 유지라는 수치는 anode-free 기준으로는 좋지만 상용 수명(수백~천 사이클)과는 거리가 있다.
> - 세미나 질문: 'SEI가 8 nm로 얇고 균질하다는 것이 사이클 동안 유지되는가(후반 사이클 cryo-TEM 데이터)?'

## Follow-up
- [ ] 황화물 anode-free 논문(예: Ag–C interlayer, Li₂S–Ag, hydride interlayer)들과 면적 용량·압력·사이클 비교표 만들기
- [ ] 리뷰/세미나용으로 '액체 vs 고체 anode-free 설계 변수 대응표' 노트 작성

## 원문 초록
> Anode-free lithium metal batteries (AFLMBs), which are manufactured without anode active material, offer great potential for high-energy-density, low-cost energy storage. However, AFLMBs face a long-standing challenge of short lifespan because of the harsh conditions of lacking excess Li resource and an anode host. This issue is associated with uneven Li deposition and dissolution, rooted in the micro-heterogeneity and mechanical fragility of solid electrolyte interphase (SEI). (이하 원문 초록은 nature.com 참조 — 첫 단락만 확보)

---
*related:* [[anode-less assb]] · *digest:* [[2026-09-04]]
