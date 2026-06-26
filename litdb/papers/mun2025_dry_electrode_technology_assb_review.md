<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. REVIEW paper. -->
# 차세대 ASSB를 위한 건식전극(dry electrode) 기술 — 무용매 제조(dry-mixing·PTFE 섬유화·calendering·co-rolling) 종합 리뷰 — Mun (Advanced Materials 2025)

> slug `mun2025_dry_electrode_technology_assb_review` · DOI `10.1002/adma.202506123` · type `review (exp/process; no DEM/MPM/FEM)` · PDF `Mun_2025_AdvMater_DryElectrodeTechnology_ASSB_Review.pdf` (21 p, main only) · digested `2026-06-26` · status ✅ · Open Access CC BY-NC (© 2025 The Authors, Adv. Mater. / Wiley-VCH)

---

## 1. 한 줄 요약
**ASSB(전고체전지)용 *건식전극(dry electrode) 제조기술*을 재료과학+공정 관점에서 종합한 리뷰** — 슬러리(wet) 캐스팅이 갖는 (i) 용매 건조 에너지/CO₂, (ii) NMP/비극성 용매 독성, (iii) 황화물 SE-용매 부반응(LiF·PO₄³⁻·SO₄²⁻ 생성), (iv) **바인더 마이그레이션 → 두께방향 조성·porosity 구배·계면 박리**를 모두 회피하는 **무용매(solvent-free) 대안**으로서 *dry-mixing → PTFE 전단-섬유화(fibrillation) → free-standing film → calendering/co-rolling/lamination* 공정을 정리한다. **이 논문 자체는 시뮬레이션·신규 실험 데이터가 없다**(리뷰 — 모든 수치는 1차 문헌 인용; Table 1/2가 그 모음). 우리에게 가치는 **frame[5] *positioning* 문서**: 건식전극의 핵심 난제가 모두 *미세구조*(균질분산·PTFE 섬유망·porosity·계면접촉·입자파쇄·dispersion·segregation)이고, 리뷰가 그것을 "실험으로 풀어야 할 과제"로 남긴다 → 우리 **DEM(패킹·CBD·접촉망 σ)+MPM(소성 morphology·void-fill)**이 바로 그 미세구조를 *예측*하는 도구로 자리매김. 정량 앵커로는 **wet vs dry SSE porosity 22.0 → 10.2 %**(Fig 4f, ★건식이 더 치밀), **PTFE 0.1–1 wt% 저바인더**(우리 1 wt%와 정합), **co-rolling/calendering = 우리 압밀 공정의 산업 버전**, **PTFE 상전이 19 ℃·E_SE 모듈러스 표(LPSCl계 Li₅PS₅류 18–25 GPa)**가 우리 E_eff·CBD·압밀과 직접 매핑된다.

> ⚠ **이 리뷰의 *원전(provenance)* 주의:** Mun et al.은 리뷰어다. Table 1/2·Fig 1–7의 *수치*는 전부 *인용된 1차 논문*(Ryu, Hong, Park, Kim, Elango, Suh, Yan, Lee, Yoon …)에서 옴 → 이 digest는 각 수치에 *원전 ref 번호*를 병기한다. "Mun이 말했다"가 아니라 "Mun이 *인용한* 1차 문헌이 측정했다". 절대값 전이 시 *원전*을 cite할 것.

---

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM/도전제/바인더) | 연구유형 |
|---|---|---|---|---|
| **Junyoung Mun**(SKKU/SIEST + Sungkyunkwan Adv. Mater.), **Taeseup Song**(Hanyang, Energy/Battery Eng.), **Min-Sik Park**(Kyung Hee, Adv. Mater. Eng.), **Jung Ho Kim**\*(교신, ISEM, **University of Wollongong**, jhk@uow.edu.au) | **Adv. Mater. 2025, 37, 2506123** (Received 2025-03-31, Revised 2025-05-21, Published online 2025-06-03) | 10.1002/adma.202506123 | **리뷰** — 대표 SE = **Li₆PS₅Cl (LPSCl)·Li₁₀GeP₂S₁₂ (LGPS)** 황화물; CAM = **NCM(LiNiₓCoᵧMnᵤO₂)·LFP·NCA**; 도전제 = **VGCF / MWNT / Super-P / CF / holey graphene / PANI / hard carbon**; 바인더 = **PTFE(주)·PVDF·pitch·SBR·TPA·CNBR·이오노머·binder-free** | **REVIEW** (재료과학+공정; **시뮬레이션 없음, 신규 실험 없음** — Table 1/2 = 인용 데이터 집계). J.M.·T.S.·M.-S.P. equal contribution. |

핵심 범위(논문 구성):
- **§1 Introduction** — LIB→ASSB 동기(안전·에너지밀도), wet 공정의 4대 난제(건조에너지·CO₂, 용매독성, SE-용매 부반응, 바인더 마이그레이션).
- **§2 Dry Coating Process for ASSBs** — (2.1) wet vs dry 미세구조, (2.2) 바인더·방법(PTFE 섬유화·Maxwell/extrusion roll-to-roll·electrostatic spray·fusion bonding·대안 바인더), (2.3) 고에너지밀도 ASSB(core-shell·thick electrode·PTFE 섬유화 제어).
- **§3 Cathode Fabrication** — (3.1) roll-pressing 건식양극(DPCE), (3.2) 대안 바인더(pitch)·binder-free, (3.3) 첨가제(LiPO₂F₂·NaCl 템플릿) thick 양극.
- **§4 Anode Fabrication** — (4.1) graphite/Si 건식음극, (4.2) PVP 표면개질로 PTFE 분해 억제, (4.3) PANI/hard-carbon 급속충전.
- **§5 Auxiliary Components** — (5.1) SE 막(separator), (5.2) 집전체, (5.3) 도전제.
- **§6 Perspective** — 5대 난제(바인더 재료·mixing·coating·thick electrode·scale-up); dispersion·segregation·pressure-free 운용.

---

## 3. 핵심 물성 (수치)  ★
> ⚠ 리뷰 — 아래는 전부 **Mun et al.이 인용한 1차 문헌의 *stated* 값**(Table 1/2 또는 본문). 이 리뷰가 *측정*한 게 아니다. digitized 아님(표/본문 명시값). **원전 ref 번호 병기.** 우리 모델 앵커로 쓸 가치가 큰 것 ★.

### 3a. ★ porosity / 두께 / loading (건식 vs 습식, 우리 압밀 직접 대응)
| 물성 | 값 | 조건 (P, 조성) | 원전(ref) | 비고 |
|---|---|---|---|---|
| **★ SSE porosity (wet vs dry)** | **22.0 %(wet) → 10.2 %(dry)** | SE 막, dry-shearing vs slurry | Fig 4f, ref [59] | ★★ **건식이 절반 이하로 더 치밀** — 우리 "dry-press = 저-porosity"의 핵심 정성 앵커 (단 절대수치는 막-제조, 우리 RVE 압밀과 다른 축) |
| **binderless 양극 porosity** | **40 %** | NaCl-template, SPS, ~1 mm thick LFP/LTO | Fig 5f, ref [71] | NaCl 누출 후 균일 기공(전해질 침투용 = *good* porosity, ASSB 양극은 *반대* 목표) |
| dry 양극 최대 두께 | **~300 µm**(dry) vs **~150 µm**(wet) | NCM622+pitch/PVDF | Fig 5c, ref [67] | ★ 건식이 두께 2× (inactive 비율↓) |
| dry 음극 두께(PVP) | **112 → 98 µm**(densify) | graphite+PTFE+PVP @~10 mAh cm⁻² | Fig 6c, ref [75] | PVP가 PTFE 분해 억제 → 치밀화 |
| **PTFE 바인더 함량** | **0.1–1 wt%**(저바인더) | dry 양극(Hippauf) | Fig 3b, ref [33] | ★★ **우리 1 wt%와 정합** — 건식은 섬유망 덕에 저바인더로 구조 형성 |
| 최저 PTFE(SSE 막) | **0.1 wt%** | dry SE 막 | ref [33] | 섬유화로 0.1 wt%까지 가능 |
| Yoon dry SE 막 | **PTFE 0.5 wt%, 두께 ≈13.5 µm** | high-Mw PTFE | Fig 4h, ref [66] | 고분자량 PTFE = 큰 변형·섬유화 |

### 3b. ★ 재료 물성 (E_SE 모듈러스 표 — 우리 E_eff·압밀에 직접)
| 물성 | 값 | 조건 | 원전(ref) | 비고 |
|---|---|---|---|---|
| **★ Young's modulus (Fig 3e)** | **Li₅La₃Zr₂O₁₂(LLZO) sintered 92 GPa · Li₂O-SiO₂ glass 70–80 · SiO₂ glass 75 · Li₂O-P₂O₅ glass 50 · Li₂S-P₂S₅ glass 18–25 · polymer 1–6** | 다양 재료 | Fig 3e, ref [40] | ★★ **우리 E_SE real-bulk 22–24 ⊂ "Li₂S-P₂S₅ 18–25 GPa"** (= Sakuda 24 ∩ Bazzoun 22.1) — *황화물은 저-모듈러스라 상온 calendering 가능*의 근거; 산화물(LLZO 92)은 고온소결 필요 |
| **★ PTFE 상전이 온도** | **19 °C 와 30 °C** | 결정상 triclinic→hexagonal | 본문 §2.2, ref [42–46] | ★ **>19 °C서 storage modulus 급감 → 전단으로 섬유화** (PVDF·CMC엔 없음) = 우리 CBD 섬유화의 온도 트리거 |
| PTFE 초기 입자 | (Lee2025서 <300 nm; 본 리뷰 명시 안 함) | — | — | n/a(이 리뷰엔 PTFE 입경 수치 없음 → Lee2025 사용) |

### 3c. ★ 전기화학 성능 (Table 1 = ASSB+LIB 양극; Table 2 = 음극/추가) — 인용 데이터 집계
> Table 1: 다양 cell의 조성·두께·loading·용량·유지율. **ASSB는 단 1행**(Fig 5e, Kim et al. ref [69]). 나머지는 LIB(건식 vs 습식 비교 맥락).

| cell(원전) | AM:CA:binder (wt%) | SE/전해질 | 두께(µm) | loading(mg cm⁻²) | areal cap(mAh cm⁻²) | 가역용량(mAh g⁻¹) | 유지율 | 에너지밀도(Wh kg⁻¹ / Wh L⁻¹) |
|---|---|---|---|---|---|---|---|---|
| **★ ASSB(Fig5e, ref[69])** | **NCM811 85 : Super-P 10 : PTFE 1** + **LiPO₂F₂ 1 첨가** | **LPSCl 13 wt%** | **156.8** | **57.5** | **10.0** | **208.86** | **96.5 % @100 cyc** | – |
| NCM712 DPCE(Fig5a,[51]) | 80 NCM712 : 15 MWNT : 5 PVDF | LE(1M LiPF₆) | 573 | 100 | 17.6 | 176 | 67.0 % @400 | 360 / 701 |
| LFP(Fig5b,[43]) | 97 LFP : 1 Super-P : 2 PTFE | LE | 175 | 52 | 7.8 | 154.6 | 65.5 % @300 | 185 / 470 |
| NCM622(Fig5c,[67]) | 90 NCM622 : 7 Super-P : 3 pitch | LE+첨가제 | 305.1 | 75.1 | 10.9 | 170.5 | 85.5 % @15 | – |
| LFP+hG(Fig5d,[68]) | 50 LFP : 50 holey graphene(binderless) | LE | 340 | 11.6 | 0.9 | >160 | 87.5 % @200 | – |
| LFP+NaCl(Fig5f,[71]) | 50 LFP : 40 NaCl-template | LE | 1000 | 114.3 | 20 | 178 | 84 % @70 | – |

Table 2(음극/추가, 모두 LIB):
- **graphite+PTFE**(Fig6a,[73]): 98 graphite : 2 PTFE, 41.25 mg cm⁻², 6 mAh cm⁻², 160 mAh g⁻¹, **88.2 % @300**.
- **Si+PTFE**(Fig6b,[43]): 73.7 Si : 26.3 C, 9.9 mAh cm⁻², ≈250, **83 % @150**.
- **graphite+PVP**(Fig6c,[75]): 96 graphite : 1 Super-P : 3 PTFE(0.5 PVP), 70.21 µm, 341.5, **86.3 % @200**.
- **Si(LDSC, magnetron)**(Fig6d,[74]): 175.7 mAh g⁻¹, **88.2 % @100**, ≈250 capacity.
- **PANI-graphite**(Fig6e,[77]): 80 graphite : 20 PANI(dual binder+conductor), 221.4, **78.2 % @100**.
- **★ Si+hard-carbon LiSH46(Fig6f, ASSB, [78])**: 95 Si : 5 PTFE(HC), ~6 mAh cm⁻², 2803.8 mAh g⁻¹, **61.5 % @5000 cyc @1C**.

### 3d. 시뮬레이션·압밀 정량 — **전부 n/a**
**Heckel / coordination Z / coverage% / σ_ionic(절대솔버값) / σ_electronic / σ_thermal / E_SE(우리식 fit) / σ_y / 접촉면적 / 압밀 porosity-vs-P 곡선**: **n/a** — 리뷰라 모델·솔버·정량 압밀 데이터 없음. porosity는 *막-제조 단면 segmentation 정성*(22.0/10.2 % 두 점, 40 %)뿐 → 우리 DEM 15.6 %/MPM 16.7 %와 *직접 비교 금지*(축이 다름; §10).

---

## 4. 시뮬레이션 방법 ★
- **code / version**: **없음** — 순수 리뷰. DEM·MPM·FEM·RNM·continuum 솔버 *일절 없음*.
- **DEM 접촉법칙 / 재료 파라미터(E,ν,μ,COR,σ_y)**: **n/a**(모델 없음). 단 **Fig 3e가 재료 *Young's modulus* 표를 제공**(위 §3b — 우리 E 입력에 유용한 *literature* 값).
- **bond/binder 모델**: 모델은 없으나 **PTFE 섬유화(fibrillation) 메커니즘을 개념·모식으로 제시** — 우리 CBD 시드 모델 물리와 1:1:
  - **전단력(shear force)**이 PTFE 입자에 가해지면 PTFE가 **늘어나 섬유상 네트워크(fibrous network)로 변형** → 저바인더로도 강건한 free-standing film(본문 §2.1 끝, §2.2; Fig 2a "Shear Force Effect", Fig 4f "Fiber-Type" vs wet "Film-Type").
  - **온도 트리거**: PTFE는 **19 °C에서 triclinic→hexagonal 상전이** → storage modulus 급감 → 상온 전단으로 섬유화(PVDF/CMC는 이 상전이 없어 섬유화 안 됨).
  - **분자량 의존**(Fig 4h, ref [66]): **high-Mw PTFE = 더 큰 변형·섬유화 → 더 robust SE 막**; low-Mw = "flimsy", intermediate = 부분적("incomplete SE dough").
  - **섬유화 제어 레버**(Fig 4g, ref [65]): **PTFE 비율↑ → 함량↑ / calendar loop↑ → 섬유화도↑ / fibrillation 온도·방향 → 균일도↑**. ★ = 우리 CBD 섬유망 morphology 입력 파라미터 후보.
- **MPM/continuum / 전달 솔버**: **n/a**. 전달은 *정성*("PTFE는 절연체 → Li⁺·전자 둘 다 저해"; "건식은 high coverage → fast Li⁺ diffusion"). **수치 σ 솔버 없음**.
- **입자 처리** ★ (DEM판 "무질서 처리"): 모델 없음. 단 리뷰가 강조하는 *실제 입자 거동*이 우리 모델 가정과 직결:
  - **(a) wet 공정 = 용매 건조 시 입자 *반발(repulsion)*·바인더 응집·도전제 응집 → AM 주변 void → SE coverage↓** (Fig 2a,b "Solvent-Drying Effect", Fig 3a) ↔ **dry 공정 = 전단으로 SE *변형·high coverage*** (Fig 2a "Shear Force Effect"). → 우리 *접촉/coverage* 모델이 잡는 바로 그 차이.
  - **(b) thick electrode 균열**: wet은 high-loading서 *crack at high loading*(건조 응력)·dry는 *crack-free*(Fig 2a). → 우리 압밀 균열/fracture와 같은 결(단 driver는 *건조 응력*, 우리는 *압밀 접촉응력*).
  - **(c) 황화물 SE는 *연성(ductile)*이라 calendering으로 변형** → 우리 MPM 소성 morphology의 전제(황화물 = 상온 소성). 단 리뷰는 *형상 모델*이 없으니 *개념*만.
- **도메인/RVE / servo / seeds / 압력범위**: **n/a**(공정 압력은 인용값으로만 — calendering/roll-press, SPS, hot-press; 절대 압력 sweep 없음. 단 인용 1차문헌의 binderless graphene 양극 두께-vs-압력은 우리 anchor: 아래 §5).
- **특이사항/공정 레버(우리 시뮬 입력에 시사점)**:
  - **3-step 건식공정**(Fig 3f): ① powder mixing → ② free-standing film(calendering) → ③ current-collector lamination. = 우리 압밀의 산업 공정 골격.
  - **2종 roll-to-roll**(Fig 3g): **Maxwell type**(fibrillize→calender) vs **extrusion type**(hot-press melt). 둘 다 PTFE 섬유화 기반.
  - **co-rolling/calendering = 우리 cold-press 압밀의 *연속(roll)* 버전** — 면내 전단 + 두께방향 압축. (cf Lee2025 co-rolling, Lyu2025 calendering DEM σ_zz>σ_xx 응력 이방성.)

---

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 건식공정 5대 이점 모식: Cost↓·CO₂↓·Non-Toxic·Stable Interface·High Energy Density | 우리 *동기* 슬라이드용 — 왜 dry-process가 중요한가 |
| **2a** | ★ **dry(crack-free) vs slurry(crack at high loading) 공정 + 두께 비교** | 우리 thick-electrode·압밀 균열 맥락 (단 우리는 압밀 균열, 여기선 건조 균열) |
| **2b** | ★ **단면 미세구조 모식: dry = AM/SE/VGCF/PTFE 균일 / wet = 응집 도전제·wet binder·*Void*(빨강 점선)** | ★ **우리 CBD·packing·void 모델이 그리는 바로 그 미세구조** — dry는 균일분산, wet은 void·응집 |
| **3a** | ★ **wet(Solvent-Drying: binder coating·aggregation·point contact·low utilization) vs dry(Shear Force: limited binder coating·deformed SE·*high coverage*·high utilization)** | ★★ **우리 coverage/utilization(dead-AM/dead-SE) 모델의 정성 그림** — dry가 coverage·utilization↑ |
| **3b** | dry 양극 제조(NCM,C,SE + **0.1–1 wt% binder** → mixing → shearing → sheet) | ★ **저바인더(0.1–1 wt%)** = 우리 PTFE 1 wt% 정합 |
| **3c** | 황화물 SE-용매 부반응 4단계: initial→residual solvent→changed surface→**resistive particulate side-phase** | wet 공정의 SE 표면 열화(우리 안 다루는 *화학* 축) |
| **3d** | 코팅·도핑이 SE-용매 부반응 억제(pristine core-shell, atmospheric/chemical stability) | 표면개질 맥락(backlog A4 carbon coating과 다른 *화학* 코팅) |
| **★ 3e** | ★★ **Young's modulus 표: LLZO 92 / Li₂O-SiO₂ 70–80 / SiO₂ 75 / Li₂O-P₂O₅ 50 / Li₂S-P₂S₅ 18–25 / polymer 1–6 GPa** | ★★★ **우리 E_SE real-bulk 22–24 ⊂ Li₂S-P₂S₅ 18–25**; 황화물 저-모듈러스 = 상온 calendering 근거; 산화물 고-모듈러스 = 고온소결 필요(우리가 황화물만 다루는 이유) |
| **3f** | dry 3-step: powder mixing → free-standing film → CC lamination | 우리 압밀 공정 골격 |
| **3g** | ★ **roll-to-roll 2종: Maxwell(fibrillize→calender) / extrusion(hot-press melt)** | ★ co-rolling/calendering = 우리 압밀의 연속 버전 |
| **3h** | electrostatic spray(hot roller, gap control) — Hot Rolled 단면 | 또 다른 dry 방법(우리 범위 밖) |
| **3i** | fusion bonding(pre-mix→cast→thermocompression) | dry 막 융합 |
| **3j,k** | 이오노머(Li⁺-conducting binder) / binder-free 시스템 | 바인더 대안(PTFE 절연 회피) |
| **4a** | high-energy ASSB cell 설계(thick cathode + ultrathin SE + Li/anode-free) | 우리 layered-composite(Phase 5) 맥락 |
| **4b** | ★ **에너지밀도 증가 전략 바그래프**(baseline→thin SE ~30 µm→thick dry→100 % Si→Li metal→anode-free) | thin SE·thick electrode가 에너지밀도 핵심 |
| **4c** | ★ **PTFE 입경(L vs S) 제어 → Passable vs Blocked Li⁺ Path** (SC-NCA+LPSCl) | ★ **PTFE가 Li⁺ 경로 *차단*** = 우리 voxel σ-블로킹·Lee2025 PTFE 페널티와 同 |
| **★ 4d** | ★★ **Conventional Dry Cathode(poor ionic contact·disrupted Li⁺·nonuniform current) → Functionalized(enhanced contact·connected Li⁺·uniform current)** — PTFE 개질로 계면 엔지니어링 | ★★ **우리 coverage·접촉망·current-distribution 모델이 정량화할 정성 그림** |
| **4e** | ★ **core-shell NCM@SE 구조**(mechanofusion): NCM core + SE shell → intimate contact·without void·uniform distribution | ★ 우리 *coverage*(SE가 AM 감쌈)의 이상적 한계 — core-shell = coverage 100 % 목표 |
| **★ 4f** | ★★ **wet vs dry binder(Film-Type vs Fiber-Type SEM) + wet vs dry SSE(porosity 22.0 % vs 10.2 %)** | ★★★ **건식 SSE porosity 10.2 % < wet 22.0 % 직접 SEM 정량** + **fiber-type 섬유망 = 우리 CBD 검증** |
| **4g** | ★ **PTFE 섬유화 제어**: PTFE ratio↑→함량↑ / calendar loop↑→섬유화도↑ / 온도·방향→균일도↑ | ★ 우리 CBD 섬유망 입력 파라미터 후보 |
| **4h** | ★ **PTFE 분자량별 섬유화**(low-Mw flimsy / intermediate incomplete / high-Mw robust entangled) | ★ 우리 CBD draw·섬유화 강성의 분자량(=강성/길이) 의존 |
| **5a** | DPCE(dry press-coated, MWNT) 제조·구조 모식 | LIB roll-press 양극(우리 범위 밖이나 공정 참고) |
| **5b** | LFP dry 양극(PTFE 섬유화→calendering→lamination) | 저바인더 PTFE 양극 |
| **5c** | ★ **wet(4-step, ~150 µm max) vs pitch-binder dry(2-step, ~300 µm max)** 공정 비교 | ★ 건식 두께 2× (thick electrode) |
| **5d** | slurry(binder) vs **dry pressing(binderless, air escaping)** — holey graphene | binderless 압밀(공기 배출 = 우리 void-fill 다른 버전) |
| **★ 5e** | ★★ **thick dry 양극 + 첨가제 LiPO₂F₂/NaCl**: "Not effective densification by void(particle crack)" vs "Effective densification by **bimodal structure → suppression of particle crack → interfacial reinforcement by decomposition of additive**" | ★★★ **bimodal 구조가 치밀화+입자균열 억제** = 우리 Furnas dip(bimodal packing) + AM_P 균열 억제와 *직접* 정합 |
| **5f** | NaCl-template binderless 양극: grinded→SPS sinter→NaCl leach → **40 % porosity** 균일기공 | 템플릿 기공(전해질 침투용 *good* porosity — ASSB 양극 목표와 반대) |
| **6a** | graphite dry 음극(pre-mix→fibrillation→lamination) + 3D-XRM porosity(top/bottom) + volume-fraction(dry 균일 vs wet 구배) | ★ **dry = 두께방향 균일분산 / wet = 구배**(우리 layered·dispersion 모델) |
| **6b–f** | Si/PANI/hard-carbon 음극(magnetron sputter·표면개질·급속충전) | 우리 범위 밖(음극 화학) |
| **★ 7** | ★ **Perspective 모식: 5대 난제**(Binder 재료·Mixing·Coating·Thick Electrode·Scale-up) | ★★ **우리 시뮬이 메우는 *과제 목록*** — 균질분산·섬유화·두께·정밀 두께/loading 모두 *미세구조* 문제 |

---

## 6. Post-processing ★
- **무엇**: 리뷰라 *자체* 후처리 없음. **인용 1차 문헌이 쓴 기법을 *정리***:
  - **3D-XRM(X-ray microscopy) + 단면 SEM**으로 **porosity·두께방향 입자/기공 분포**(dry 균일 vs wet 구배) — Fig 6a(ref [73]).
  - **단면 SEM threshold segmentation**으로 **wet vs dry SSE porosity 22.0/10.2 %**(Fig 4f, ref [59]).
  - **DMA**(PTFE storage modulus vs 온도)·상전이(19 °C) — Fig 4h 등.
  - **tortuosity 측정**(x/y/z, SPS 양극서 *higher tortuosity → Li⁺ 저해*) — §3.3 Elango(ref [71]).
  - **EIS/전기화학**(rate·cycle)로 wet vs dry 성능 비교(Table 1/2).
- **도구**: 인용문헌 의존(ImageJ류 segmentation·Amira류 CT·DMA·EIS) — *이 리뷰는 도구를 안 씀*.
- **수치화·플롯·기록**: 본 리뷰의 정량은 **Table 1(양극+LIB)·Table 2(음극)** 두 집계표 + Fig 3e(모듈러스)·Fig 4f(porosity)·Fig 4g/4h(섬유화 정성). σ는 *정성 논증*(절대 σ 솔버 없음).

---

## 우리 DEM+MPM 대비 (comparison vs ours)
> A. 사용자 요구 — 건식공정 미세구조(섬유화 PTFE CBD망·무용매 패킹) vs 우리 DEM(packing·CBD)+MPM(소성 morphology); co-rolling/calendering = 우리 압밀. → `our_dem_baseline.md`

| 항목 | 이 리뷰 (Mun 2025, 인용 종합) | 우리 (DEM+MPM) | 차이 / 이유 (frame[4]/[5]) |
|---|---|---|---|
| 성격 | **리뷰**(no model/exp) — 과제·landscape 정리 | DEM(전달)+MPM(역학) *예측* 시뮬 | **frame[5] positioning** — 리뷰가 남긴 *미세구조 과제*를 우리가 예측. 경쟁 아님. |
| 공정 | **dry-mixing·PTFE 섬유화·calendering·co-rolling**(무용매) | **cold-press 압밀**(300 MPa RVE) | ★ **co-rolling/calendering = 우리 압밀의 *연속(roll)* 버전** — 우리는 두께방향 압축 RVE; 리뷰는 그 산업 공정 |
| 미세구조 | dry = 균일분산·high coverage·low void / wet = 응집·void·구배(Fig 2b,3a) | DEM packing+CBD+접촉망; coverage(Tabor/Hertz); porosity | ★ **우리 coverage·utilization·void 모델이 리뷰의 정성 "dry=high coverage" 그림을 *정량화*** |
| **CBD/바인더** | **PTFE 전단-섬유화**(19 °C 상전이·고-Mw robust·calendar loop↑→섬유화↑); **PTFE는 절연 → Li⁺·전자 *차단*** | 우리 CBD: curl·vol-conserve·nucleate-on-carbon 시드(`docs/cbd_morphology_roadmap.md`); voxel σ-블로킹 | ★ **리뷰 = 우리 CBD 섬유망 모델의 *literature positioning*** + **PTFE σ-페널티(차단)의 정성 근거**(정량은 Lee2025/Bielefeld2020) |
| porosity | **dry SSE 10.2 % vs wet 22.0 %**(Fig 4f, 막-제조 segmentation) | DEM 15.6 % / MPM 16.7 % @300(Minnmann 10 %) | ⚠ **축이 다름**(그들=막 단면 정성 2점, 우리=RVE 압밀) → *직접 비교 금지*; "dry가 더 치밀"이라는 *방향*만 정합 |
| E_SE | **Li₂S-P₂S₅ glass 18–25 GPa**(Fig 3e) | real-bulk 22–24; E_eff 1.35(DEM)/1.53(MPM) 연화 | ★ **우리 24 ⊂ 18–25**(=Sakuda 24·Bazzoun 22.1 *3중 확인*); E_eff는 그 연화 프록시 |
| bimodal | ★ **"bimodal structure → 치밀화 + 입자균열 억제"**(Fig 5e, LiPO₂F₂ 첨가) | DEM/de Larrard **Furnas dip @ AM 70–85 wt%**; AM_P 균열 | ★ **bimodal 치밀화 = 우리 dip; "균열 억제"는 우리 AM_P 파괴와 결 정합**(단 리뷰는 *정성*) |
| thick electrode | dry ~300 µm(crack-free) vs wet ~150(crack) | 우리 RVE(~30 µm real_14) — *thin*만 | ⚠ 우리는 *thick* 막을 안 다룸 — frame[5] *gap*(우리는 RVE 미세구조, thick-film 균열은 미보유) |
| 전달 솔버 | **없음**(정성 "PTFE 차단·high coverage→fast Li⁺") | Kirchhoff/Holm + Stage-E + 삼중항 σ_i/σ_e/σ_thermal | ★ **우리 강점** — 명시적 접촉망 σ·삼중항(리뷰엔 절대 σ 없음) |
| morphology/변형장 | 정성(섬유화·variation) | MPM 진짜 소성 형상변화·void-fill·Σdg | ★ **우리 강점**(MPM 정량 변형장) |
| fracture | 정성(thick crack·입자균열 억제) | DEM AM_P 37–40% cracked·Auerbach·fracture-Holm | ★ **우리 강점**(정량 균열) |
| 음극/화학 | graphite/Si·PANI·SEI·표면개질(상세) | **우리 안 다룸** | ⚠ 우리는 *양극 미세구조*만 — 음극·SEI·화학은 리뷰가 더 넓음 |

---

## 적용가능성 (applicability to our model)
> B. 사용자 요구 — 어떤 dry-process feature가 우리 CBD 모델(backlog A3 섬유화-PTFE bond, `--coh`)·압밀 protocol(co-rolling vs cold-press)·앵커(porosity·loading·압력)에 들어가나. 스크립트 매핑.

- **① ★ PTFE 섬유화 메커니즘 → 우리 CBD 섬유망 모델의 *literature positioning* (backlog A3, frame[5] 근거):**
  Fig 2a/3a("Shear Force Effect → deformed SE·fibrillation·high coverage")·Fig 4f("Fiber-Type" SEM)·Fig 4g(섬유화 제어 레버)·Fig 4h(분자량별 섬유화)는 우리 `docs/cbd_morphology_roadmap.md`의 **curl(worm-like) + nucleate-on-carbon + shear-draw** 그림과 정성 일치 → 우리 CBD 시드 모델이 *literature-grounded*(Lee2025 SEM이 *실측 검증*이면, 이 리뷰는 *공정 메커니즘 종합*). **흡수 후보**: (a) **섬유화도 = f(calendar loop, PTFE 분자량/강성, 온도)** 를 CBD 시드 파라미터(섬유 길이/강성/curl)로 매핑; (b) **저바인더 0.1–1 wt%**(우리 1 wt% 정합) — 섬유망이라 소량으로 구조 형성 → 우리 CBD volume fraction 입력 정당화. ⚠ 막-제조 *전단* 공정은 우리 압밀 RVE가 *재현 안 함* → *개념/positioning*으로만(over-claim 금지).
  - **스크립트**: CBD 섬유망 생성 시드(roadmap batch1); `network_conductivity.py`의 CBD voxel σ-블로킹(SuperP/VGCF 차등); `--coh`(SE cold-weld+vdW adhesion, mpm3d_compaction.py) = PTFE *결착력*의 MPM 대응(단 PTFE는 *섬유*, --coh는 *등방 점착* → 형태 다름).

- **② ★ PTFE σ-페널티(차단) → 우리 σ_e/σ_ionic 보정 (backlog B 검증, Lee2025와 합류):**
  Fig 4c("PTFE-L blocks Li⁺ path")·Fig 4d("disrupted Li⁺ pathway")·§2.1("polymeric binders inherently act as insulators, reducing both Li⁺ and e⁻ conductivities")·§6("PTFE undergoes irreversible reactions·low ionic conductivity")는 **PTFE가 두 전도도를 *차단*** 한다는 정성 근거 → **이 리뷰는 *정성*, 정량 곡선은 Lee2025**(0.5→5 wt%서 σ_e 34→0.011·σ_i 0.069→0.007, `docs/data/lee2025_transport_anchors.csv`)·Bielefeld2020(바인더 active-interface −82 %). ⇒ 우리 σ_e/σ_ionic 폼이 도전제 *기여*만 반영하고 바인더 *차단* 페널티가 없는 문제 → **이 리뷰가 그 페널티의 *정성 mechanism* 출처**(왜 막는가: 절연 + Li⁺/전자 경로 물리 차단). 절대 보정은 Lee2025 곡선으로.
  - **스크립트**: `generate_comparison_plots.py` σ_e Stage 22.5 / σ_ionic T1 — 바인더 wt% 항(비단조) 추가 시 *mechanism*은 본 리뷰, *수치*는 Lee2025.

- **③ ★ bimodal 치밀화 + 입자균열 억제 → 우리 Furnas dip + AM_P 파괴 (frame[3]/[5] 정합):**
  Fig 5e("Effective densification by **bimodal structure → suppression of particle crack**")는 우리 DEM/de Larrard **Furnas dip(AM 70–85 wt%)** + AM_P 균열 작업과 직접 정합 — bimodal이 (i) packing 치밀화(우리 dip), (ii) 큰 입자 균열 억제(우리 AM_P fracture·Lee2025 PC-NCM 균열·Kang2025 큰입자 균열). ⇒ **우리 dip+fracture 모델이 리뷰의 정성 주장을 *정량화***(dip 깊이·위치, 균열 분율). 단 리뷰 첨가제(LiPO₂F₂ *분해*에 의한 interfacial reinforcement)는 우리가 안 다루는 *화학* 축.
  - **스크립트**: `mpm2d_jamming.py`/de Larrard 기하(dip); DEM fracture(Auerbach)·`f_intact`.

- **④ E_SE 모듈러스 표 → 우리 E 입력 재확인 (frame[2]):**
  Fig 3e "Li₂S-P₂S₅ 18–25 GPa" → 우리 real-bulk 22–24가 *문헌 범위 내*(Sakuda 24·Bazzoun 22.1 3중 확인) → E_eff 1.35/1.53는 그 연화 프록시. ★ **산화물(LLZO 92)과 대비**: 황화물 저-모듈러스라 *상온 calendering* 가능 = 우리가 황화물(LPSCl)만 다루고 산화물 고온소결을 안 다루는 *경계 근거*.
  - **스크립트**: `our_dem_baseline.md` E_SE 행 + MPM `--e-se` 입력.

- **⑤ porosity/loading/두께 앵커 (압력-구분 컨텍스트로만):**
  - **dry SSE 10.2 % / wet 22.0 %**(Fig 4f) = "건식이 더 치밀"의 *정성 방향*(절대값은 막-제조, 우리 RVE와 *축 다름* → densCSV에 *porosity 칸 비우고* 컨텍스트로만).
  - **ASSB loading 57.5 mg cm⁻², 10 mAh cm⁻², NCM811 85:Super-P 10:PTFE 1 + LiPO₂F₂, LPSCl 13 wt%, 156.8 µm**(Table 1 Fig5e, ref[69]) = 우리 production(real_14 ~30 µm, 82:18) 대비 *thick·고-loading* 케이스 — 우리 입력 design point 확장 후보. ⚠ 첨가제 LiPO₂F₂ 있음.
  - **binderless graphene 음극 두께-vs-압력**(Fig 5d, ref[68]): 160 µm @500 MPa / 175 @200 / 340 @20 MPa(LIB) → 압력↑→두께↓(치밀화) = 우리 압밀 추세 정성 대응(단 LIB·graphene → 절대 전이 금지).
  - **스크립트**: `docs/data/densification_porosity_db.csv`(porosity 칸 비움, 컨텍스트만); webapp design-point 입력.

- **⑥ co-rolling/calendering protocol → 우리 압밀 protocol (servo/hold):**
  리뷰의 calendering(연속 압연)·co-rolling은 *변위/속도 제어*(roll gap) = 우리 MPM **hold**(변위정지) 결. Lee2025(fixed-gap vs const-pressure)·Lyu2025(calendering DEM, σ_zz>σ_xx 응력 이방성)와 합류 → **co-rolling = 면내 전단 + 두께 압축의 이방 응력장** → 우리 RVE는 *등방 압축*만 → frame[5] *gap*(전단-유발 섬유 정렬은 우리 미보유).
  - **스크립트**: `mpm3d_compaction.py --protocol hold`; (전단 정렬은 미보유 — 명시).

---

## frame[5] 위치 (review = positioning)
> C. 사용자 요구 — 리뷰이므로 우리 시뮬을 *건식전극 설계의 예측 미세구조 도구*로 자리매김. 우리가 모델하는 것/gap을 부드럽게.

이 리뷰는 *경쟁 모델이 아니라 landscape* 다 — 그래서 frame[4](교차검증) 대신 **frame[5] *division-of-labor positioning*** 으로 읽는 게 맞다.

- **리뷰가 "실험으로 풀어야 할 과제"로 남긴 것 = 전부 *미세구조* 문제**(Fig 7 Perspective 5대 난제):
  ① **Mixing**(균질분산·도전제 응집 억제·섬유화 프로토콜) ② **Coating**(정밀 두께/loading·기공/밀도 제어) ③ **Thick Electrode**(고-loading·micro-scale 이온/전자 수송) ④ **Binder 재료**(이온전도 바인더) ⑤ **Scale-up**(균일 분포·defect-free).
  → ①②③은 **우리 DEM+MPM이 *예측*하는 바로 그 미세구조 변수**: 분산/패킹(DEM packing·Furnas dip), 기공/밀도(porosity·Heckel), 접촉/coverage(Tabor·B3), 이온/전자/열 수송(Kirchhoff 삼중항), 소성 morphology/void-fill(MPM). ⑤ segregation도 우리 multi-size DEM이 잡는 packing 현상.

- **우리 시뮬의 positioning(부드럽게):**
  > "건식전극의 성패는 *미세구조*(균질분산·PTFE 섬유망·porosity·계면접촉·입자무결성)에 달렸고, 리뷰는 이를 실험적 과제로 정리한다. 우리 DEM+MPM은 이 미세구조를 *공정 입력(조성·압력·PSD·바인더)→예측*하는 도구 — DEM이 패킹·접촉망 수송·coverage·Furnas dip·균열을, MPM이 소성 morphology·void-fill·변형장을 담당해, 건식전극 설계의 *예측 스크리닝*을 제공한다."

- **우리가 *명확히* 모델하는 것**(리뷰 과제 ↔ 우리 능력):
  - 균질분산/패킹 → DEM multi-size packing, dispersion CV(backlog A5).
  - porosity/밀도/thick 치밀화 → DEM ε_sphere + Heckel; MPM 소성 void-fill.
  - 계면접촉/coverage(Fig 3a "high coverage"·Fig 4e core-shell) → Tabor/Hertz coverage + B3 roughness.
  - 이온/전자/열 수송 → Kirchhoff/Holm 삼중항(리뷰엔 *정성*만 → 우리 정량).
  - bimodal 치밀화 + 입자균열 억제(Fig 5e) → Furnas dip + AM_P fracture.
  - PTFE 섬유망 morphology → CBD 시드(roadmap) + σ-블로킹.

- **우리가 *아직 못 하는* gap(정직하게 — over-claim 방지):**
  - **막-제조 *전단* 공정**(co-rolling/calendering의 면내 전단 → PTFE 섬유 *정렬*) — 우리 RVE는 *등방 압축*만, 전단-유발 섬유 배향은 미보유.
  - **thick-film(~300 µm) 건조/제조 균열** — 우리는 RVE 미세구조(~30 µm), thick-film 스케일 균열·구배는 미보유.
  - **SE-용매 *화학* 부반응**(Fig 3c resistive side-phase)·**음극 SEI/화학**(graphite/Si/PANI) — 우리는 *양극 미세구조 물리*만(화학 축 미보유).
  - **PTFE *절대* σ-페널티** — 우리는 *정성 mechanism*(이 리뷰)은 있으나 *정량*은 외부(Lee2025/Bielefeld2020)에서 가져와 보정해야 함.
  - **co-rolling 두 막 동시 융합**(SSE+양극) — 우리는 단일 RVE.

---

## 8. 적용 인사이트 (내 연구에 어떻게)  ★
- ① **★ 리뷰 = 우리 DEM+MPM의 *동기/positioning* 1번 출처** — Fig 7(5대 난제)·Fig 1(5대 이점)·Fig 2b/3a(dry vs wet 미세구조)는 "왜 미세구조 예측이 필요한가"의 *권위 있는 리뷰 근거*. 우리 deck/paper Introduction에 *건식전극의 미세구조 난제 → 우리 예측 도구* 흐름으로 직접 인용.
- ② **★ PTFE 섬유화 메커니즘 = 우리 CBD 모델 *literature positioning*** (Lee2025 SEM 검증과 짝) — `docs/cbd_morphology_roadmap.md` batch1(curl·nucleate·shear-draw)이 *리뷰가 정리한 공정 메커니즘*과 정합 → 우리 CBD 시드가 임의 아님. 섬유화 레버(calendar loop·분자량·온도, Fig 4g/4h)를 CBD 시드 파라미터로 매핑.
- ③ **★ bimodal 치밀화+균열억제(Fig 5e) = 우리 Furnas dip + AM_P fracture 정합** → 우리 dip/fracture가 리뷰의 정성 주장을 *정량화*하는 차별점.
- ④ **★ E_SE 18–25 GPa(Fig 3e)** = 우리 real-bulk 22–24의 *3번째 문헌 확인*(Sakuda·Bazzoun과); 황화물 저-모듈러스 = 상온 calendering·우리 모델 적용범위 경계 근거.
- ⑤ **PTFE 저바인더 0.1–1 wt%** = 우리 PTFE 1 wt% 입력 정당화(섬유망이라 소량 충분).
- ⑥ **PTFE σ-차단(Fig 4c,d, §2.1)** = 우리 σ 폼 바인더-페널티의 *mechanism* 근거(정량은 Lee2025).

## 9. 인용 가능 문장 (deck/paper용)
- "A 2025 *Advanced Materials* review of dry-electrode technology for ASSBs (Mun et al.) frames the central manufacturing challenges — homogeneous dispersion, PTFE fibrillation, porosity/density control, interfacial contact, and particle integrity — as *microstructural* problems, which is precisely the regime our DEM+MPM predicts from process inputs (composition, pressure, PSD, binder)."
- "The review reports that dry-shearing produces a denser sulfide solid-electrolyte membrane than slurry casting (10.2 % vs 22.0 % porosity, Fig 4f, ref [59]) and enables low-binder (0.1–1 wt% PTFE) free-standing films via shear fibrillation — consistent with our 1 wt% PTFE CBD treatment and our dry-press low-porosity baseline."
- "Mun et al. place sulfide glasses (Li₂S-P₂S₅) at 18–25 GPa versus oxide LLZO at 92 GPa (Fig 3e), confirming our real-bulk E_SE ≈ 22–24 GPa and explaining why sulfides (LPSCl) — unlike oxides — densify by room-temperature calendering, the process our compaction model represents."
- "The review's 'bimodal structure → effective densification + suppression of particle crack' (Fig 5e) maps directly onto our Furnas-dip packing gain and our DEM treatment of polycrystalline-CAM fracture."

## 10. 주의/한계 (over-claim 방지)
- **리뷰 — 자체 시뮬레이션·신규 실험 *0***. DEM/MPM/FEM/RNM·정량 압밀 porosity·Heckel·coordination Z·coverage%·E_SE(우리식 fit)·σ_y·접촉면적·절대 σ 솔버값 **전부 n/a**. 모든 수치는 *인용 1차 문헌*의 stated 값(Table 1/2, Fig 3e/4f) → **절대값 전이 시 *원전 ref*를 cite**(Mun이 아니라 Ryu/Hong/Park/Kim/Lee … 가 측정).
- **porosity 22.0/10.2 %는 *막-제조 단면 segmentation*(SE separator)** 이지 *복합양극 압밀 porosity* 아님 → 우리 DEM 15.6 %/MPM 16.7 %와 **직접 비교 금지**(축이 다름; *방향*만 "dry가 더 치밀"). 40 %(NaCl-template)는 *전해질 침투용 good porosity*(ASSB 양극 목표와 반대).
- **Table 1 ASSB는 단 1행**(NCM811+LPSCl, ref[69]) 나머지는 **LIB**(액체전해질) — LIB는 porosity=good·이온전도체=공극으로 *위상 정반대* → LIB 수치를 우리 ASSB로 전이 금지(σ·porosity·loading 모두). ASSB 1행도 **LiPO₂F₂ 첨가제** 있음(우리 무첨가와 다름).
- **PTFE σ-페널티는 *정성 mechanism*만**(이 리뷰) — *정량 곡선*은 Lee2025/Bielefeld2020 소유. 이 리뷰로 절대 σ 보정 금지.
- **막-제조 *전단* 공정(co-rolling/calendering)** 은 우리 RVE가 *재현 안 함* — 섬유화·전단 정렬은 *개념/positioning*으로만, 우리 시뮬이 그 공정을 재현한다고 주장 금지.
- **음극·SEI·화학(graphite/Si/PANI/hard-carbon·표면개질·SE-용매 부반응)** 은 리뷰가 넓게 다루나 *우리 범위 밖*(양극 미세구조 물리만) — 이 부분은 digest/모델에서 *맥락*으로만.
- **E_SE 18–25 = *재료 고유 E*(glass)** → 우리 *real-bulk* 칸에만 매핑; *압밀-bed* E_eff(1.35/1.53)와 층위 다름(직접 동일시 금지). 또한 "Li₂S-P₂S₅ glass" ≠ LPSCl(아지로다이트) — *황화물 family* 범위로만(Bazzoun LPSCl 22.1이 LPSCl-특이 값).
- **frame[5] positioning**: 이 리뷰는 *과제 landscape* 를 줌; *모델 절반*(명시적 접촉망 σ 삼중항·MPM 변형장·Auerbach·Heckel·정량 dip)은 **우리가 추가**. 우리 시뮬을 *예측 도구*로 positioning 하되, 막-제조 전단·thick-film·화학 축은 *gap*으로 정직하게 명시.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
