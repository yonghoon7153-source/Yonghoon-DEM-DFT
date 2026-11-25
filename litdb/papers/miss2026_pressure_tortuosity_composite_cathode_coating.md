<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md (같은 Roling 그룹 · 같은 1저자 · 같은 해).
     쪽 표기 = 논문 쪽 "n of 11" (ChemElectroChem e70274 은 쪽 번호 대신 "n of 11").  SI 는 "SI p.n" (SI PDF 3 쪽).
     값 표지: [인쇄] = 본문 · SI · 그림 범례에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv — 래스터 원본에서
     눈금 보정 + 표지 무게중심) · [재계산] = 판독값을 원문 식에 다시 넣은 값 · [우리 산술] = 이 논문 밖 우리 값과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음.
     원문 14 쪽 (본문 11 + SI 3) 은 렌더 이미지로 전부 읽었다.  그림은 전부 래스터 (벡터 아님) — 판독은 원 래스터 해상도에서 했다. -->
# 압밀 중 (in situ) 잰 복합 양극의 전자 · 이온 tortuosity — NMC622 단결정 / 다결정 × LiNbO₃ 코팅 유무 × CAM 부피분율 (0.3–0.7) · 0.67Li₃PS₄–0.33LiI 유리 SE · 8.8 → 663 MPa 단조 가압: τ_eon 은 압력으로 한 자릿수 떨어지고 τ_ion (같은 압력 순수 SE 펠릿 기준) 은 거의 평평 · 막자사발 혼합이 미세구조를 정한다 — Miß · Müller · Schäfer · Versok · Seus · Mereacre · Binder · Roling (ChemElectroChem 2026)

> slug `miss2026_pressure_tortuosity_composite_cathode_coating` · DOI `10.1002/celc.70274` · type `experiment (in situ 가압 셀 CompreDrive · 이온 차단 WC 전극 EIS · 복합 양극 powder 펠릿 · SEM/EDX · 시뮬레이션 없음)` · PDF `2. Pressure-Dependent Electronic and Ionic Tortuosities During Fabrication of Composite Cathodes for All-Solid-State Batteries Influence of Active Material Particle Morphology, Volume Fraction, and Coating.pdf` · SI `2. Sup) Pressure-Dependent Electronic and Ionic Tortuosities During Fabrication of Composite Cathodes for All-Solid-State Batteries Influence of Active Material Particle Morphology, Volume Fraction, and Coating.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: Vanessa Miß · Greta Müller · Sophie Schäfer · Evelyn Versok · Stefan Seus (Univ. Marburg, mar.quest) · Valeriu Mereacre · Joachim R. Binder (KIT IAM-ESS) · **Bernhard Roling\*** (Marburg) · *ChemElectroChem* **2026**, 13, e70274 (Research Article, 본문 11 쪽 + SI 3 쪽) · 접수 2026-02-16 · 수정 06-08 · 승인 06-26 · **CC-BY** · 연구비 DFG RO 1213/20-1 · RO 1213/14-2 (p.10).
> **같은 그룹 · 같은 1저자 카드 (링크만 — 내용 베끼지 않음)**: [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) (ACS AMI 2026 — 단일상 SE · CAM 의 가압 중 두께 · 공극 · 제거 회복.  **이 카드와 다른 논문**: 저쪽 = 공극 · 두께 · 스프링백, 이쪽 = 복합체 tortuosity · 공극 자료 없음) · [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (본문 ref 13) · [`so2021_dem_mold_pressure_assb_coldpress`](so2021_dem_mold_pressure_assb_coldpress.md) (본문 ref 17) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (본문 ref 11).
> **판독 원자료**: `litdb/figures/miss2026_pressure_tortuosity_composite_cathode_coating/digitized.csv` (176 행 — Fig 1 · 4 · 5 · 6 · 8).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이 논문은 **하중을 한 번도 빼지 않는 첫 압밀** (8.8 → 663 MPa 계단 증가) 동안 이온 차단 전극 임피던스 한 장에서 **전자 σ (저주파) · 병렬 σ (중간 주파수)** 를 떼어 내
**τ_eon · τ_ion 을 압력의 함수로** 준다.  τ 의 정의는 우리 규약의 **tau2 (수송 tortuosity = tortuosity factor)** 와 같은 꼴이지만, **σ₀ = 같은 압력에서 잰 순수 SE 펠릿 σ** · **φ = 공극을 뺀 명목 부피분율 (1 − ε_CAM)** 이라
우리 tau2 (σ₀ 고정 3.0 → 보고 1.5 mS/cm · φ_SE 구 부피 기준) 와 **기준 상태가 다르다** — 숫자를 나란히 놓지 않는다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① DEM 언로딩 시험 (ρ_c · 판 속도 0.01 mm/s) 의 실험 표적 | **없다** — 단조 가압만 (Fig S2 계단, 제거 없음).  결론 끝 문단이 "제작 압력 제거 · 작동 적층압 적용 중 과정은 **더 가역적일 것으로 기대되며** 앞으로 자세히 보겠다" 고 적는다 | [인쇄] p.11 · SI p.2 |
| ② CL-94 (순수 SE 300 MPa 공극) | **없다** — 공극 · 밀도 · 두께-압력 자료 0 건.  SE 도 LPSCl 이 아니라 **비정질 0.67Li₃PS₄–0.33LiI** | 본문 · SI 전수 |
| ③ V2 (순수 SE 앵커의 상태 · 측정량 · 불확도) | 순수 SE 펠릿 σ_ion(p) 곡선 한 개 (Fig 1) — **σ 는 있으나 공극이 없어** V2 의 측정량 (ε) 이 아니다 | [인쇄] p.3 · [판독] |
| ④ Heckel (DEM 순수 SE P_y 138 MPa) | **없다** (두께 · 밀도 미보고) | — |
| ⑤ τ 규약 (tau2 · τ_geo) | 원문 τ_eon · τ_ion = **tortuosity factor (tau2 꼴)**: R = τ/(σ₀·φ) · d/A (p.2) · σ_comp = σ₀·φ/τ (Eq 4–5, p.4).  σ₀ = **같은 압력의 순수 상 펠릿 σ** (SE: Fig 1 · CAM: 같은 그룹 앞 논문 ref 22) — 펠릿 ≡ 1 규약의 **압력별 갱신판** | [인쇄] p.2 · p.4 · p.8 |
| ⑥ τ_eon 의 압력 의존 | ε_CAM 0.5 · 44 → 663 MPa 에서 **"typically … by one order of magnitude"** · 판독: pc 무코팅 ≈1000 (70–97 MPa) → 51 · sc 무코팅 98 (43 MPa) → 9.0 · pc 코팅 27 (97) → 11 · sc 코팅 55 (243) → 22 | [인쇄] p.8 · [판독] Fig 8a |
| ⑦ τ_ion 의 압력 의존 | **약하다** (*"The pressure dependence of τion is weak"*) — pc 무코팅 ≈3.4 → 2.6 · sc 무코팅 ≈14 → 8.6 · pc 코팅 10 → 5.9 · sc 코팅 24 → 12.6 | [인쇄] p.8 · [판독] Fig 8b |
| ⑧ PC ↔ SC (우리 ps45 축) | **형상 · 혼합이 지배**: sc 는 뭉쳐 (AM–AM) τ_eon 낮고 τ_ion 높음 · pc 는 막자사발 혼합 중 **갈라지고 SE 로 거의 균일하게 덮여** τ_ion 낮고 τ_eon 높음 — 우리 ps45 의 "SC 많을수록 σ_ion ↓" 와 **방향은 같고 설명은 다르다** (§7-3) | [인쇄] p.8–10 · Fig 9–12 |

⛔ **한정어 (떼지 말 것)**: ① SE = 비정질 **Li₃PS₄–LiI 유리** (볼밀 8 h) ≠ 우리 Li₆PS₅Cl ② CAM = NMC622 (상용 MSE) ≠ 우리 NCM (PC r 4.5 · SC r 2.0 µm) ③ **도전재 · 결합재 없음** ④ τ 의 σ₀ 가 **압력마다 바뀐다** (같은 압력 순수 펠릿) — 우리 tau2 와 기준 상태 다름 ⑤ φ 는 공극 무시 ⑥ 공극 · 두께-압력 · 반복 시료 수 · 오차 막대의 뜻 [미확인] ⑦ ε_CAM = 0.5 라 적힌 τ 와 달리 50:50 시료는 그림 축에서 **ε_CAM ≈ 0.52–0.53** 자리에 찍혀 있다 [판독] (§10-3).

---

## 1. 한 줄 요약
이온 차단 WC 피스톤 사이에서 복합 양극 분말을 **처음 압밀하는 동안** (8.8 → 663 MPa) 임피던스를 찍어, 세 저항 R₁ · R₁+R₂ · R₁+R₂+R₃ (모두 두께에 비례 = 벌크) 을
**고주파 σ_hf (국부 운동, ε_CAM 에 선형) · 중간 주파수 σ_if (= 전자 + 이온 병렬) · 저주파 σ_lf (= 전자, 이온 차단)** 로 해석하고 (p.3–6), 그로부터 τ_eon · τ_ion 을 계산했다.
결과: **전자 tortuosity 는 압력으로 한 자릿수 떨어지고 (CAM–CAM 접촉 개선), 이온 tortuosity 는 같은 압력의 순수 SE 펠릿 기준으로 거의 평평** (SE 압밀이 순수 펠릿과 비슷하게 진행).
CAM 형상 · 코팅이 미세구조를 바꾼다 — **sc-NMC622 는 응집** (전자 빠름 · 이온 느림), **pc-NMC622 는 막자사발에서 갈라지며 SE 로 덮임** (이온 빠름 · 전자 느림), LiNbO₃ 코팅은 그 정도를 바꾼다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| V. Miß, G. Müller, S. Schäfer, E. Versok, S. Seus (Marburg) · V. Mereacre, J. R. Binder (KIT) · **B. Roling\*** | ChemElectroChem 13 (2026) e70274 · CC-BY | 10.1002/celc.70274 | SE = **비정질 0.67Li₃PS₄ + 0.33LiI** (자체 볼밀 합성) · CAM = **LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NMC622)** 상용 (MSE Supplies) **sc / pc × 무코팅 / LiNbO₃ 0.5 wt% 코팅** — 복합체 CAM:SE 부피비 70:30 · 50:50 · 30:70 (무코팅) · 60:40 · 50:50 · 40:60 (코팅) | 실험 — in situ 압력별 EIS (이온 차단) + SEM/EDX (분말 · 혼합분말 · FIB 단면).  **시뮬레이션 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 시료 · 셀 (p.2 · SI)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE 합성 | Li₂S (99.9 %) · P₂S₅ · LiI (99.999 %) 화학량론 · 행성 볼밀 Pulverisette 7 · ZrO₂ 20 mL 용기 · ⌀10 mm 볼 10 개 · **≈8 h (99 회 × 5 분 밀링 + 15 분 휴지) · 700 rpm** → 마노 유발 분쇄 · 2 g 배치 | [인쇄] p.2 |
| SE 상 | XRD = **비정질** (Fig S1, Li₄PS₄I 기준과 대조 — 날카로운 반사 없음, 넓은 혹 ≈21° · 28°) | [인쇄] p.2 · SI p.2 · 혹 위치 [판독] |
| CAM | NMC622 sc · pc 무코팅 상용 (MSE Supplies, Tucson) · 일부를 **LiNbO₃ 0.5 wt%** 로 코팅 (H₂O₂ 활성화 "chemically activated coating" — sol–gel 보다 치밀 · 두께 균일, refs 18–19) · **350 °C 열처리 → 비정질 코팅** | [인쇄] p.2 |
| 입경 | **[미확인]** (본문 · SI 수치 없음).  SEM (Fig 9 · S4) 판독: pc = 구형 2차입자 ≈8–10 µm · sc = 1차입자 ≈1.5–4 µm, 무코팅 sc 는 큰 응집 · SE 는 혼합분말에서 ≈10–20 µm 덩어리 (Fig 10) | [판독 — 축척 막대 기준 대략] |
| 복합체 혼합 | **마노 유발 15 분** (부피비로 칭량) | [인쇄] p.2 |
| 시료 질량 | 40 mg · 80 mg (두 두께) | [인쇄] p.2 |
| 압력 셀 | **CompreDrive** (rhd instruments) **능동 힘 제어** · 밀폐 시료 셀 CompreCell · **WC 피스톤 = 전극** (이온 차단) · 셀 지름 [미확인] | [인쇄] p.2 |
| 압력 계단 (Fig S2) | 8.8 MPa 시작 → 8.8 MPa 간격 97 MPa 까지 → 24.25 간격 194 → 49 간격 292 → 97 간격 584 → 663 MPa.  **판독상 49 MPa 간격이 389 MPa 까지 이어진다** (340 · 389 점 존재) — 본문 문장과 1 단계 어긋남 | [인쇄] p.2 · [판독] Fig 1 · 8 · S2 |
| 유지 · 하중 속도 | 각 계단 "plateau" 에서 측정 (SI Fig S2 캡션) — 유지 시간 · 속도 [미확인] | [인쇄] SI p.2 |
| EIS | NEISYS (Novocontrol) · **1 MHz – 0.1 Hz · 10 mV_rms · 25 °C** · RelaxIS 적합 · 등가회로 L–R₁–(R₂‖CPE₁)–(R₃‖CPE₂) (Fig 2a 삽입) | [인쇄] p.2–3 · 회로 [판독] |
| 순수 SE 펠릿 | 같은 계단 · 같은 셀 | [인쇄] p.2 |

### 3-2. ★ 순수 SE (0.67Li₃PS₄–0.33LiI) 펠릿 σ_ion(p) — Fig 1 (p.3)
본문: *"σ_ion^SE increases from about 10⁻⁴ S cm⁻¹ at low pressures to about 10⁻³ S cm⁻¹ at high pressures. At high pressures, the ionic conductivity becomes virtually independent of the pressure."* [인쇄] p.3 · 195 MPa 값 **0.73 mS cm⁻¹** [인쇄] p.7.

| p (MPa) | 8.8 | 52 | 97 | 145 | 194 | 243 | 292 | 389 | 486 | 584 | 663 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| σ (mS/cm) [판독] | 0.098 | 0.33 | 0.49 | 0.63 | **0.73** | 0.81 | 0.86 | 0.93 | 0.98 | 1.00 | 1.00 |

- 판독 194 MPa 0.731 = 인쇄 0.73 (195 MPa) — 판독 보정 확인.  86 % 의 증가가 ≲300 MPa 에서 끝나고 486 → 663 MPa 는 +1.6 % (평탄) [판독].
- ⚠ 두께 (σ = d/(R·A) 의 d) 가 **가압 중 값인지** [미확인] — 같은 그룹 AMI 논문 (`miss2026_insitu_…` 카드) 이 다이 밖 두께를 쓰면 저압 −22 % · 고압 +6.5 % 편향을 보였다 (다른 SE).

### 3-3. 두께 비례 = 세 저항이 전부 벌크 (Fig 2 · Fig S3)
- pc 무코팅 50:50 · 486 MPa · **128 · 246 µm** 두 시료 (Fig 2a) [인쇄] p.3 · 캡션 p.4.  Fig 2b: log R_i vs log d 의 점 **넷** (log d ≈ 2.05 · 2.11 · 2.39 · 2.40 → d ≈ 112 · 129 · 245 · 251 µm [판독]) 이 기울기 1 선에 놓인다 → *"All resistances are proportional to the thickness of the cathode. This implies that all resistances are bulk resistances."* [인쇄] p.3.
- sc 무코팅 50:50 · 486 MPa (Fig S3): d ≈ 124 · 141 · 210 · 295 µm [판독] — 같은 결론 (R₁ 은 기울기 1 선에서 ±0.1 decade 안팎 흩어짐 [판독]).
- ⇒ 전극–시료 계면 (WC | 복합체) 저항이 세 반원에 섞이지 않았다는 근거 — **우리 접촉망 σ (계면 저항 없는 벌크 망) 와 같은 양을 잰다는 전제의 실험 확인** (이 셀 · 이 압력 한정).

### 3-4. ★ 세 σ 의 해석 (Eq 1–6 · p.3–6)
- 정의 (Eq 1–3): σ_hf = d/(A·R₁) · σ_if = d/(A·(R₁+R₂)) · σ_lf = d/(A·(R₁+R₂+R₃)).
- **σ_lf = σ_eon^composite = σ_eon^CAM · ε_CAM / τ_eon** (Eq 4) — 이온 차단이라 저주파는 전자만.
- **σ_if = σ_par = σ_eon^comp + σ_ion^comp = σ_eon^CAM·ε_CAM/τ_eon + σ_ion^SE·(1 − ε_CAM)/τ_ion** (Eq 5) — 혼합전도체 (MIEC) 의 "병렬 전도도" (Jamnik–Maier, refs 20–21).
- **σ_hf = σ_eon^CAM·ε_CAM + σ_ion^SE·(1 − ε_CAM)** (Eq 6) — 고주파에서는 국부 운동이라 tortuosity · 협착 영향 무시 → ε_CAM 에 **선형** (Fig 4 · 7b).
- 근거 패턴 (Fig 7 모식 ↔ Fig 4–6 자료): σ_lf(ε) 는 기울기 + · 곡률 + · σ_if(ε) 는 곡률 + 이고 기울기는 전자 / 이온 중 큰 쪽이 정한다 (극소 ≈0.5 가능) · σ_hf 는 직선.
- **결론 문장**: *"Electronic and ionic tortuosities can be obtained from the values of σlf and σif, except in cases with σlf ≈ σif."* [인쇄] p.10 — 전자 σ 가 이온 σ 보다 훨씬 크면 (σ_lf ≈ σ_if) 이온 몫이 두 큰 수의 차로만 남아 정해지지 않는다.

### 3-5. ★ 조성 축 판독 (Fig 4–6 · ε_CAM 세 점) — S/cm → 표는 mS/cm [판독]
| 시료 · 압력 | σ_hf (Fig 4) | σ_if (Fig 5) | σ_lf = σ_eon^comp (Fig 6) |
|---|---|---|---|
| pc 무코팅 · 98 MPa (ε 0.3 / 0.52 / 0.7) | 0.65 / 1.28 / 1.95 | 0.133 / **0.075** / 0.168 (극소) | 미결정 / ≈0 / 0.157 |
| pc 무코팅 · 486 | 1.56 / 4.86 / 6.24 | 0.38 / 0.40 / 1.56 | ≈0 / 0.22 / **1.52** |
| sc 무코팅 · 98 | 0.81 / 1.33 / 1.30 | 0.140 / 0.089 / 0.42 | 0.004 / 0.072 / 0.42 |
| sc 무코팅 · 486 | 2.68 / 5.29 / 6.58 | 0.43 / 1.23 / 2.68 | 0.067 / 1.17 / **2.68** |
| pc 코팅 · 98 (ε 0.4 / 0.53 / 0.6) | 0.60 / 1.03 / 1.22 | 0.062 / 0.029 / 0.020 (음의 기울기) | 0.0005 / 0.0043 / 0.0099 |
| pc 코팅 · 486 | 1.74 / 2.52 / 2.57 | 0.171 / 0.216 / 0.33 | 0.030 / 0.139 / 0.28 |
| sc 코팅 · **195** | 0.93 / 0.98 / 1.04 (기울기 ≈0) | 0.105 / 0.021 / 0.039 | 미결정 / 0.0071 / 0.033 |
| sc 코팅 · 486 | 1.80 / 2.54 / 2.92 | 0.190 / 0.106 / 0.169 | 0.023 / 0.073 / 0.160 |

- Fig 6 캡션: *"In two cases at low εCAM, σlf could not be determined, since the maximum of the low-frequency semicircle was located outside the frequency range"* [인쇄] p.7 (pc 무코팅 98 MPa ε 0.3 · sc 코팅 195 MPa ε 0.4 [판독]).
- 본문 해석 사례 (p.4–6): ① sc · pc 무코팅 98 MPa = 낮은 ε 에서 이온 지배 (음의 기울기) · 높은 ε 에서 전자 지배 → 486 MPa 에서 전자가 전 범위 지배 ② pc 코팅 = 98 MPa 이온 지배 · 486 MPa 전자 지배 → *"the coating lowers the electronic conductivity"* ③ sc 코팅 = 두 압력 모두 낮은 ε 이온 · 높은 ε 전자 → *"the electronic conductivity of sc-NMC622 is lowered more strongly by the coating than … pc-NMC622"*.
- σ_hf 기울기 ≈0 인 유일한 경우 = sc 코팅 195 MPa → 그 압력의 코팅 sc 전자 σ **≈0.96 mS cm⁻¹** (ref 22) 가 SE 0.73 과 비슷해서 (Eq 6 의 기울기 = σ_CAM − σ_SE) [인쇄] p.7.
- [우리 산술 — 판독 3 점 직선] Eq 6 의 절편 (ε → 0) 은 σ_SE 여야 하는데: sc 코팅 195 MPa **0.72** (σ_SE 0.73 ✓) · sc 무코팅 98 MPa 0.50 (0.49 ✓) 이지만 pc 무코팅 486 MPa **−1.8** (σ_SE 0.98 ✗) · pc 코팅 98 MPa −0.64 (0.49 ✗) — **Eq 6 은 선형성 · 기울기 부호까지만 맞고 절편은 시료마다 어긋난다** (원문은 "strong indication for a linear relation" 까지만 주장).

### 3-6. ★★ τ_eon · τ_ion vs p (ε_CAM = 0.5 · Fig 8 · p.8) [판독]
| p (MPa) | pc 무코팅 τ_eon / τ_ion | sc 무코팅 τ_eon / τ_ion | pc 코팅 τ_eon / τ_ion | sc 코팅 τ_eon / τ_ion |
|---|---|---|---|---|
| 43–61 | — / — | **98 → 52** / ≈13–14 | — / — | — / — |
| 70–97 | **≈800–1200** (큰 오차막대) / ≈3.4 | 44 → 38 / ≈14 | **27** / **10.1** | — / — |
| 123 | 448 / 3.3 | 26 / 13.7 | 20 / 9.1 | — / — |
| 194 | 202 / 3.0 | (pc 코팅과 겹침 ≈17) / 11.6 | 17 / 7.7 | — / — |
| 243 | 133 / 3.0 | (겹침) / 10.7 | (겹침 ≈13–14) / 7.4 | **55** / **24** |
| 291 | 103 / 2.9 | (겹침 ≈12–13) / 10.4 | ≈12–13 / 7.2 | 43 / 22 |
| 486 | 60 / 2.7 | 9.5 / 8.6 | 11.4 / 6.1 | 25.5 / 14.3 |
| 663 | **51** / **2.6** | **9.0** / **8.6** | **11.3** / **5.9** | **22** / **12.6** |

- 본문: *"Increasing the pressure from 44 MPa to 663 MPa at εCAM = 0.5 leads typically to a drop of τeon by one order of magnitude."* [인쇄] p.8.  판독 배수: pc 무코팅 ≈20× (70 → 663) · sc 무코팅 ≈11× (43 → 663) · pc 코팅 ≈2.4× (97 → 663) · sc 코팅 ≈2.5× (243 → 663).
- *"Remarkably, the LiNbO3 coating leads to an increase of the electronic tortuosity in the case of sc-NMC622 and to a drop of the electronic tortuosity in the case of pc-NMC622."* [인쇄] p.8.
- τ_ion: *"The pressure dependence of τion is weak suggesting that the compaction of the solid electrolyte in the composite pellets with increasing pressure is similar to the compaction in the pure solid electrolyte pellets."* · *"The pc-NMC622-based composite cathodes exhibit lower τion values than the sc-NMC622-based composite cathodes."* [인쇄] p.8–9.
- 곡선 시작 압력이 다른 이유 = 낮은 압력에서 σ_lf · σ_if 결정 불가 (반원 극대가 주파수 창 밖 · σ_lf ≈ σ_if) — 원문은 이유를 곡선별로 적지 않았다 [판독 + 추정].
- **[재계산] 내적 일관성 확인**: 판독한 Fig 5 · 6 (ε_CAM 0.52 자리 점) 과 Fig 1 의 σ_SE(486 MPa) 0.98 을 Eq 5 에 φ = 0.5 로 넣으면 τ_ion(486) = pc 무코팅 **2.66** (Fig 8b 2.70) · sc 무코팅 8.2 (8.6) · pc 코팅 6.4 (6.1) · sc 코팅 14.9 (14.3) — ±5 % 안 (σ_if − σ_lf 차이의 판독 오차 크기).  98 MPa 도 pc 무코팅 3.3 (3.4) · sc 무코팅 14.4 (≈14) · pc 코팅 10.2 (10.1).  ⇒ **τ 는 ε_CAM = 0.5 (명목) 로 계산됐다** — 0.52 를 넣으면 4 % 낮아진다.
- [우리 산술] Eq 4 를 거꾸로 풀면 τ_eon(486) 에 들어간 순수 CAM σ_eon^CAM (ref 22 의 값 — 이 논문에 수치 없음) ≈ pc 무코팅 **26** · sc 무코팅 22 · pc 코팅 3.2 · sc 코팅 3.7 mS/cm (판독 σ_lf × τ / 0.5).  같은 그룹 AMI 논문의 pc-NMC622 단일상 σ_e (in situ, 400 MPa ≈15.9 mS/cm [판독], `miss2026_insitu_…` §3-5) 와 같은 자릿수 · 다른 압력 · 다른 두께 규약.

### 3-7. ★ 미세구조 — 형상 · 코팅 · 막자사발 혼합 (Fig 9–12 · p.8–10)
- **sc-NMC622 무코팅**: 분말이 **강하게 응집** (Fig 9) · 혼합분말에서도 응집 유지 (Fig 10 Ni EDX) → *"the agglomeration of uncoated sc-NMC622 particles in the composite and the resulting good electronic contacts lead to a low electronic tortuosity"* · SE 는 큰 입자로 그 사이에 남아 이온 경로를 막음 → 높은 τ_ion (p.8–10).
- **sc-NMC622 코팅**: 응집 경향 **낮음** → 전자 접촉 적음 → τ_eon 높음 (p.8).
- **pc-NMC622 무코팅**: 응집 경향 낮음 · **막자사발 혼합이 입자를 갈라지게 하고 대부분의 입자를 SE 로 거의 균일하게 덮는다** (Fig 10 · 11 · 12) → *"This SE coating of the previously uncoated particles together with the cracking of pc-NMC622 particles diminishes the electronic transport strongly, implying a high electronic tortuosity"* · 같은 SE 피복이 이온 경로를 이어 τ_ion 낮음 (p.8–9).  저자 표현 *"dry coating"* — 용액 SE 코팅 (ref 23) 은 SE σ 를 낮추지만 이 건식 피복은 그렇지 않다고 적는다 (p.9).
- **pc-NMC622 코팅**: 역시 갈라지지만 SE 로 **부분적으로만** 덮임 → 전자 수송이 덜 깎임 → τ_eon 이 무코팅 pc 보다 **낮다** (*"paradox observation at first sight"*) · τ_ion 은 무코팅 pc 보다 높음 (p.8 · p.10).
- Fig 11 (663 MPa 뒤 FIB 단면, 판독): pc 무코팅 2차입자 내부 **방사 · 그물 균열** · SE (보라) 가 CAM (초록) 사이를 채움 · sc 1차입자 ≈1–3 µm 가 무리 지어 접촉 · 일부 공동 (검정).
- 결론 (p.10): sc 와 pc 의 응집 · SE 상호작용 차이는 *"most likely related to the surface properties of the NMC particles, e.g., to different surface chemistries or to different degrees of crystallinity at the surface"* — TEM · XPS 후속 필요.  **표면 에너지 · 화학 측정은 없다.**

### 3-8. 인용된 선행 수치 (서지 그대로 — 원문 확인 안 함)
- Park et al. (ref 16, Appl. Sci. 2022): 전자 차단 셀 τ_ion **20–75 @40 MPa → 5–15 @660 MPa** [인쇄] p.2 — 정본 카드 없음 [미확인 원문].
- So et al. (ref 17 = 정본 `so2021_dem_mold_pressure_assb_coldpress`): DEM 에서 같은 하락 경향 (정성) [인쇄] p.2.
- *"To the best of our knowledge, a study on the pressure dependence of the electron transport tortuosity τeon has not yet been published."* [인쇄] p.2.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
분말 (40 · 80 mg) → CompreCell (WC 피스톤 = 이온 차단 전극) → CompreDrive 능동 힘 제어 계단 가압 (Fig S2) → 계단마다 EIS (25 °C) → 등가회로 L–R₁–(R₂‖CPE₁)–(R₃‖CPE₂) 적합 → R₁ · R₁+R₂ · R₁+R₂+R₃ → 두께로 σ_hf · σ_if · σ_lf (Eq 1–3) → Eq 4 로 τ_eon (σ_CAM 은 ref 22) → Eq 5 로 τ_ion (σ_SE 는 Fig 1) → SEM/EDX (분말 · 혼합분말 · 663 MPa 뒤 FIB 단면).
- 두께 d 의 출처 (in situ 변위 vs 꺼낸 뒤) [미확인] · 시료 지름 A [미확인] · 반복 수 · 오차막대 정의 [미확인] (Fig 4–6 · 8 에 오차막대 있음).

### 4-2. τ 정의 ↔ 우리 τ 명명 규약
- 원문 (p.2): R_eon = (τ_eon / (σ_eon^CAM · ε_CAM)) · d/A · R_ion = (τ_ion / (σ_ion^SE · ε_SE)) · d/A — 즉 σ_eff = σ₀ · φ / τ.
- ⇒ **원문 τ = 우리 tau2 (수송 tortuosity · tortuosity factor)** 꼴 (√ 아님).  다른 것은 기준 상태:

| 항목 | 이 논문 | 우리 tau2 (CLAUDE.md τ 블록) |
|---|---|---|
| σ₀ | **같은 압력의 순수 상 펠릿 σ** (SE Fig 1 · CAM ref 22) | σ_grain 3.0 (봉인 상수) · 보고 기준 1.5 mS/cm (1저자 10-12) — 압력 무관 |
| φ | 명목 부피분율 (1 − ε_CAM) — **공극 무시** | φ_SE = SE 구 부피 합 / 전극 부피 (공극 포함 상자 기준) |
| 담는 것 | 순수 펠릿에도 있는 SE–SE 접촉 저항은 **약분된다** — 복합체만의 초과분 | SE–SE 접촉 협착 포함 (ps45 Hertz tau2 의 73–75 % 가 SE–SE 협착, 10-13) |
- 환산 규칙 (값 없이 식만): tau2_우리꼴 = τ_원문 × (σ₀_우리 / σ_펠릿(p)) × (φ_우리 / φ_명목).  ⚠ 이 SE (LPS–LiI 유리) 의 σ₀_우리 (결정립 / 치밀 고유 σ) 는 원문에 없다 → **숫자 환산 불가**.
- litdb J 절 "기준 상태 장부" 에 한 줄 추가 후보: **펠릿 ≡ 1 · 압력별 갱신 (같은 압력의 순수 펠릿)** — Minnmann · Kaiser · Kato 의 고정 펠릿 ≡ 1 과 또 다르다.

### 4-3. ★ 입자 처리 (실험 — 시뮬레이션 없음)
- 실제 입자: SE = 볼밀 비정질 유리 조각 (변형 쉬움 — 원문 서술 없음) · CAM = pc 구형 2차입자 (1차입자 응집) / sc 단결정 다면체.
- **혼합 단계가 미세구조를 정한다** — 막자사발 15 분이 pc 를 **갈라지게** 하고 SE 를 표면에 **바른다** (건식 피복).  압밀 전 상태가 이미 "구 + 구" 가 아니다.
- 우리 DEM 과의 대응: 강체 구 (PC r 4.5 · SC r 2.0 µm) · 혼합 단계 없음 (LIGGGHTS insert/pack) · PC 균열은 압축 중 Auerbach 판정만 · SE 피복 = 접촉 기하일 뿐 — **이 논문이 지배 인자로 지목한 응집 · 혼합 중 파쇄 · 건식 피복 셋 다 우리 침대 생성에 없다**.

### 4-4. 기법 미니 용어집
- **이온 차단 (ion-blocking) 전극**: WC 피스톤은 전자만 통과 → 저주파 극한 = 전자 저항만 (σ_lf).
- **병렬 전도도 σ_par** (Jamnik–Maier MIEC): 중간 주파수에서 이온 · 전자 두 레일이 함께 흐르는 값 = σ_eon + σ_ion.
- **σ_hf (고주파 국부 전도도)**: 캐리어 이동 거리가 짧아 tortuosity · 협착이 안 보이는 값 (원문 해석) — ε 에 선형.
- **pc / sc**: 다결정 2차입자 / 단결정.  **LiNbO₃ 코팅**: 계면 안정 코팅 (여기서는 0.5 wt% · 비정질 · 전자 절연성).
- **tortuosity factor (tau2)** = φσ₀/σ_eff — 우리 보고 이름 "수송 tortuosity".

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 순수 0.67Li₃PS₄–0.33LiI 펠릿 σ_ion vs p (로그 · 22 점 · 8.8 → 663 MPa) — 0.1 → 1.0 mS/cm, ≥ ~490 MPa 평탄 | 유리 SE 의 압력 포화 모양 (σ₀ 를 압력별로 바꾸는 이 논문 τ 의 분모) |
| 2 | (a) pc 무코팅 50:50 · 486 MPa · 128 · 246 µm Nyquist + 등가회로 (b) log R vs log d — 기울기 1 | ★ 세 저항이 벌크 (두께 비례) = 계면 저항 불포함의 확인 절차 |
| 3 | 30:70 (207 µm) vs 70:30 (225 µm) Nyquist @486 MPa — CAM 적으면 저주파 반원 지배 (−Z″ ≈5000 Ω cm²) · 많으면 고주파 반원 지배 (≈15 Ω cm²) | 조성에 따른 전자 / 이온 반원 교대 |
| 4 | σ_hf vs ε_CAM — 4 CAM × 2 압력, 선형 적합 | Eq 6 (국부 전도도) 의 선형성 · 절편은 일부 시료에서 σ_SE 와 다름 (§3-5) |
| 5 | σ_if vs ε_CAM — 기울기 + / − / 극소 | 병렬 전도도 해석 |
| 6 | σ_lf (= 복합체 전자 σ) vs ε_CAM — 기울기 + · 곡률 + | ★ CAM–CAM 전자 퍼콜레이션의 압력 · 형상 의존 (우리 σ_e 채널 대조) |
| 7 | (a) σ_lf · σ_ion^comp · σ_if 모식 (b) σ_hf 모식 | 해석 틀 |
| 8 | ★★ (a) τ_eon (b) τ_ion vs p · ε_CAM 0.5 · 4 CAM (로그 10⁰–10⁴) | 우리 tau2 와 규약 대조 (§4-2) · 전자 τ 압력 의존 = 한 자릿수 |
| 9 | 순수 NMC622 4 종 SEM (50 µm 막대) — sc 무코팅 큰 응집 | 입경 · 응집 정성 |
| 10 | 막자사발 혼합분말 SEM/EDX (S 보라 · Ni 초록) — pc 무코팅이 SE 로 덮임 · sc 사이 큰 SE | ★ 혼합 상태 = 미세구조 지배 인자 (이종기술 논지 P3 방향의 정성 사례) |
| 11 | 663 MPa 뒤 FIB 단면 EDX — pc 2차입자 내부 균열 · sc 무리 | 압밀 뒤 PC 균열 · SE 채움 |
| 12 | 모식: pc 무코팅 = 균일 SE 피복 · pc 코팅 = 부분 피복 · sc = 응집 + 큰 SE | 논지 그림 언어 |
| S1 | SE XRD (비정질) vs Li₄PS₄I 기준 | 상 확인 |
| S2 | 압력 계단 (단조 증가 · 제거 없음) — ⚠ 자동 크롭이 백지로 빼서 손 크롭 | ★ 언로딩 자료 없음의 근거 |
| S3 | sc 무코팅 50:50 · 486 MPa log R vs log d (4 두께) | 벌크 확인 반복 |
| S4 | 4 종 NMC622 고배율 SEM (10 µm 막대) | 1차 · 2차입자 크기 판독 |

## 6. Post-processing ★
- **무엇을**: 등가회로 적합 (RelaxIS) → 세 저항 → 세 σ (in situ 두께 여부 [미확인]) → σ(ε_CAM) 의 모양 (기울기 · 곡률) 으로 각 σ 의 물리적 뜻 판정 (Fig 7 모식) → Eq 4 · 5 로 τ_eon · τ_ion (ε_CAM 0.5) → SEM/EDX 정성 해석.
- **도구**: RelaxIS · Zeiss Crossbeam 550 (5 kV · 100 pA · EDX 5 kV · 1–2 nA · Oxford Ultim Max) · 불활성 이송 셔틀.
- **안 한 것**: 공극 · 밀도 · 두께-압력 곡선 · Heckel · 하중 제거 · 반복 시료 통계 · 표면 에너지 · 입경 분포 · 모델.
- **우리 후처리 (이 카드)**: Fig 1 · 4 · 5 · 6 · 8 판독 (176 행) · Eq 5 재계산으로 τ_ion 재현 (±5 %) · Eq 4 역산 σ_CAM · Eq 6 절편 점검.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 측정 상태 | 단조 가압 중 (계단 plateau) · 제거 없음 | DEM = 300 MPa 판 정지 + 판 고정 이완 · 언로딩 시험 (ρ_c, P_meas 1 MPa) = 등록 · 실행 전 (`docs/reviews/dem_unloading_ps45_prereg_20261009.md`) | 이 논문은 "가압 중" 쪽 자료만 — 언로딩 표적 0 |
| SE | 비정질 Li₃PS₄–LiI 유리 · σ 펠릿 1.0 mS/cm @≥490 MPa [판독] | Li₆PS₅Cl · σ₀ 3.0 (봉인) / 보고 1.5 mS/cm | 재료 다름 — 절대값 전이 금지 |
| CAM | NMC622 sc · pc · LiNbO₃ 유무 · 도전재 없음 | NCM PC r 4.5 + SC r 2.0 µm 구 · (Phase A 등은 VGCF 포함) | 형상 · 응집 · 혼합 손상이 우리 침대에 없음 |
| 전자 채널 | τ_eon (pc 무코팅) ≈1000 → 51 · sc 무코팅 98 → 9 (압력 ↑) [판독] | DEM σ_e = 접촉망 (AM–AM 접촉 · Hertz/Physics 면적) | ★ 방향 같음 (압력 ↑ → AM–AM 접촉 ↑) · 크기는 형상 · 응집이 지배 — 구 크기만으로는 안 나옴 |
| 이온 채널 τ | 2.6–24 (펠릿 σ(p) 기준 · φ 명목) [판독] | ps45 Hertz tau2 7.24–5.03 (σ₀ 고정 · 73–75 % 가 SE–SE 협착 · 협착 뺀 같은 망 1.25–1.79) — CLAUDE.md 10-13 | ⛔ **규약 다름** (§4-2) — 나란히 놓지 않는다 |
| PC ↔ SC | sc → τ_ion ↑ (응집한 sc 사이에 큰 SE 덩어리) · pc → τ_ion ↓ (갈라진 pc 를 SE 가 덮어 경로를 잇는다) | ps45 (PC r 4.5 · SC r 2.0 µm): SC 많을수록 σ_ion ↓ (0:10 → 7:3 FULL 1.52 배) · 분해 = 활물질 표면적 2.25 배 → SE 가 AM 표면을 덮는 데 쓰여 SE 1 개당 SE–SE 접촉 4.41 ↔ 5.57 (CF 망 1.47–1.49 배 = 경향의 대부분) — `docs/data/ps45_r45_network_g2_20261007/README.md` "P:S 경향 분해" | **방향은 같다** (SC 쪽 이온 불리) · **설명이 다르다**: 실험 = 응집 · 큰 SE (sc) vs 피복이 경로 (pc) / 모델 = AM 표면 피복이 SE–SE 접촉을 빼앗음 — §7-3 |
| 측정 연산자 | 차단 전극 EIS 한 장에서 σ_e · σ_ion 분리 (Eq 4–5) | 망 Kirchhoff (각 채널 따로) | 우리는 채널을 직접 푼다 — 그들의 "σ_lf ≈ σ_if 면 이온 미결정" 한계 없음 |

### 7-2. 언로딩 시험 (ρ_c) — 무엇을 주나
- **자료 0** — Fig S2 = 단조 계단 · 결론의 마지막 문단이 제작 압력 제거 과정을 *"expected to be more reversible in nature"* 로 **기대만** 적는다 (p.11).  ⇒ ρ_c 의 실험 표적 · 기전 근거로 쓰지 않는다.
- 간접 재료: 663 MPa 뒤 단면에 pc 2차입자 **내부 균열** (Fig 11) — 언로딩 중 회복에 PC 내부 공극 · 균열이 섞일 수 있다는 정성 근거 (우리 DEM AM = 꽉 찬 구 · 회복 = 접촉 겹침 회복만).  같은 그룹 AMI 논문의 pc-NMC622 단일상 회복 (300 MPa 다이 안 7.9 %) 과 함께 볼 것.

### 7-3. ★ PC/SC · 혼합 상태 ↔ 우리 모델 · 이종기술 논지
- 이 논문의 **지배 인자 = 혼합 단계** (응집 · 파쇄 · 건식 피복) — 우리 파이프라인에는 혼합이 없다 (믹서 캠페인은 별도 개발 트랙).  ⇒ **우리 ps45 의 SC/PC 효과는 "같은 혼합 상태 (무작위 삽입) 에서 크기만 다를 때" 의 효과**로 한정해 말한다.
- 이종기술 논지 (`docs/hetero_thesis.md` 비준 블록) P3 *"혼합 상태의 차이가 압축 뒤 SE 경로 (연결 · coverage · σ_ion) 차이로 이어진다"* 와 **방향이 같은 정성 실험 사례** — 단 ① SE 가 다르고 (유리) ② 코팅은 LiNbO₃ (SE 선코팅 아님) ③ 피복은 막자사발에서 저절로 생겼고 ④ 원인 (표면 화학 · 결정성) 은 저자도 미측정.  ⛔ "코팅 효과 크기" · "표면 에너지 차이" 근거로 쓰지 않는다 (논지 "하지 않는 말").
- 같은 방향 · 다른 설명 [우리 해석]: SC 쪽이 이온에 불리한 것은 실험 (τ_ion sc 8.6–14 ↔ pc 2.6–3.4, ε_CAM 0.5) 과 우리 ps45 (SC 많을수록 σ_ion ↓) 가 같다.  그러나
  실험은 **SE 가 CAM 을 덮은 것이 τ_ion 을 낮췄다** (피복층 = 이온 경로) 고 읽고, 우리 분해는 **SE 가 AM 표면을 덮는 데 쓰여 SE–SE 접촉이 줄어든 것**을 SC 쪽 하락의 주인으로 읽는다 (피복 = SE 의 낭비).
  같은 현상 (AM 표면의 SE) 이 수송에 주는 부호는 **피복층이 이어져 관통 경로가 되는가 (실험 pc) · 섬으로 끊기는가 (모델의 구 접촉)** 에 걸린다 — 강체 구 DEM 은 얇은 연속 피복을 못 만들므로 앞쪽 경로를 원리상 담지 못한다.
  판별 후보 = 우리 망에서 AM–SE 접촉에 걸린 SE 가 관통 성분에 속하는 비율 (새 계산 · 1저자 결정).

### 7-4. 전자 채널 — 우리 σ_e 와
- 압력 ↑ → τ_eon 한 자릿수 ↓ (CAM–CAM 접촉 개선) 은 우리 접촉망 σ_e 의 정성 방향과 같다.  크기 (pc 20× · sc 11×) 는 응집 · 균열 · 코팅이 정한다 — 강체 구 DEM 의 Hertz/Physics 면적으로는 응집 (사전 AM–AM 접촉) 을 못 만든다.
- 우리 σ_e 앵커 (kgy DC 분극 SBE 4.47 · DBE 12.4 mS/cm, CLAUDE.md 10-12) 는 **VGCF 포함** 전극 — 이 논문 (도전재 없음, 복합체 σ_eon 0.0005–2.7 mS/cm [판독]) 과 같은 양이 아니다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 수송 반쪽 (복합체 σ_eon · σ_ion · τ 의 압력 · 형상 의존) — 실험.
- **없는 것**: 기계 반쪽 (공극 · 두께 · 하중 분담 · 회복) · 접촉 수 · 3D 미세구조 정량 · 모델.  ⇒ DEM 수송 쪽의 **경향 대조점** (압력 · 형상) 만 준다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **τ 기준 상태 장부에 새 꼴 하나**: "펠릿 ≡ 1, 압력별 갱신" — 우리 tau2 와 비교하기 전에 σ₀ · φ 를 맞춘다 (§4-2).  litdb J 절 · 메인 τ 판단 메모 결정 4 (순수 SE 망 런 관문) 의 사례로.
2. **τ_ion 이 압력에 거의 평평한 것은 정규화의 산물**일 수 있다 — 분모 (순수 SE 펠릿 σ) 가 같은 압력에서 같이 오르기 때문.  우리 고정 σ₀ tau2 는 압력에 따라 더 크게 움직일 것 (SE–SE 협착 포함) — 문헌 "τ_ion 압력 둔감" 을 우리 모델 검증에 쓰려면 같은 정규화로 다시 계산해야 한다.
3. **혼합 상태 한정어**: 우리 PC/SC 효과 문장에 "같은 (무작위) 혼합 상태에서의 크기 효과" 를 붙인다 — 실험의 sc/pc 차이는 응집 · 파쇄 · 피복이 지배 (Fig 10–12).
4. **EIS 측정 연산자 메모**: 이온 차단 전극 한 장에서 σ_lf (전자) · σ_if (병렬) — 우리 σ_e 실험 앵커 논의 때 DC 분극 외의 대안 측정법 (σ_lf ≈ σ_if 면 이온 미결정 한계 포함).
5. **PC 내부 균열 정성 근거** (Fig 11) — 언로딩 회복 · Auerbach 판정 토론의 배경.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Pressure-dependent impedance measurements during the first compaction of NMC622/Li₃PS₄–LiI composites (Miß et al., *ChemElectroChem* 2026) show that the electronic tortuosity drops by about one order of magnitude between ~44 and 663 MPa, while the ionic tortuosity — referenced to a pure-SE pellet at the same pressure — changes only weakly."
- "In that work the tortuosity is defined as a tortuosity factor (σ_eff = σ₀·φ/τ) with σ₀ taken from the pure-phase pellet at the same pressure, i.e. a different reference state from ours."
- 국문: *"단결정 NMC 는 응집해 전자 tortuosity 가 낮고 이온 tortuosity 가 높으며, 다결정 NMC 는 막자사발 혼합 중 갈라지고 SE 로 덮여 반대가 된다 (Miß 2026, SEM/EDX 정성) — 혼합 상태가 압축 뒤 수송을 정하는 실험 사례."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **SE · CAM 이 우리 것과 다르다** — 비정질 Li₃PS₄–LiI · NMC622 · 도전재 없음.
2. **τ 기준 상태** (§4-2) — 압력별 펠릿 σ₀ · 명목 φ.  우리 tau2 와 숫자 비교 금지.
3. **ε_CAM 표기 불일치**: Fig 8 은 ε_CAM = 0.5 · Fig 4–6 의 50:50 점은 축에서 ≈0.52–0.53 [판독] — 저자 설명 없음 (실측 밀도 보정값일 가능성 = 추정).  τ 재계산은 0.5 로 맞는다 (§3-6).
4. **두께 · 면적 · 반복 · 오차막대 정의 [미확인]** — σ 의 d 가 가압 중 두께인지 밝히지 않는다 (같은 그룹 AMI 논문은 그 차이가 −22 … +6.5 % 라고 보였다).
5. **σ_CAM(p) 의 출처는 ref 22 (앞 논문) — 이 논문에 수치 없음** → τ_eon 은 그 논문 값에 기댄다.  역산값 (§3-6) 은 우리 산술.
6. **Eq 6 절편** (§3-5) — 일부 시료에서 σ_SE 와 다르다 → σ_hf 해석은 정성 근거까지만.
7. **압력 계단 본문 ↔ 그림** — 49 MPa 간격이 389 MPa 까지 (본문은 292 까지) [판독].
8. **SC/PC 차이의 원인 (표면 화학 · 결정성) 은 가설** — 측정 없음 (p.10).
9. **"이온 τ 압력 둔감"** 은 정규화 효과와 분리되지 않았다 (§8-2).
10. **전이 한계**: 막자사발 혼합 · 40–80 mg 펠릿 ≈110–300 µm · 단조 가압 · 25 °C — 건식 후막 공정 · 언로딩 · 작동 적층압 상태로 옮기지 않는다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 11 | B. Tjaden, D. J. L. Brett, and P. R. Shearing, *Int. Mater. Rev.* 63 (2018): 47–67 | 정본 카드 있음 — τ 정의 |
| 12 | C. König, V. Miß, L. Janin, and B. Roling, *ACS Appl. Energy Mater.* 6 (2023): 9356–9362 (SE 습식 밀링으로 τ_ion 완화) | 같은 그룹 τ_ion 규약 · SE 입경 효과 |
| 13 | P. Minnmann, … J. Janek, *J. Electrochem. Soc.* 168 (2021): 040537 | 정본 카드 있음 — tau2 펠릿 ≡ 1 규약 |
| 14 | M. Kroll, M. Duchardt, … *J. Power Sources* 505 (2021): 230064 | 시트형 · 양극 형상 |
| 15 | T. Shi, Q. Tu, Y. Tian, … *Adv. Energy Mater.* 10 (2020): 1902881 | 입경 최적화 (고부하) |
| 16 | S.-Y. Park, J. Jeong, and H.-C. Shin, *Appl. Sci.* 12 (2022): 12692 | τ_ion 20–75 → 5–15 (40 → 660 MPa) 의 원전 — 미 digest |
| 17 | M. So, G. Inoue, … *J. Power Sources* 508 (2021): 230344 | 정본 카드 있음 — DEM 압밀 τ |
| 19 | J. Haust, Y. Guo, J. Belz, … *Adv. Mater. Interfaces* 12 (2025): e00590 | LiNbO₃ 코팅 구조 |
| 20–21 | J. Jamnik, J. Maier (and S. Pejovnik), *J. Electrochem. Soc.* 146 (1999): 4183 · *Electrochim. Acta* 44 (1999): 4139 | MIEC 병렬 전도도 · 망 모델 (Eq 5 의 근거) |
| 22 | V. Miß, S. Seus, A. Marx, et al., *ACS Mater. Lett.* 7 (2025): 2262–2269 | ★ σ_eon^CAM(p) 원 자료 (형상 · 코팅 · 열처리) — τ_eon 분모 |
| 23 | K. H. Park, D. Y. Oh, … *Adv. Mater.* 28 (2016): 1874–1883 | 용액 SE 코팅 (σ 저하) 대조 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 11 쪽 · SI 3 쪽 전부 렌더 이미지로 읽고 `pdftotext` 로 인용문 대조 · DOI `10.1002/celc.70274` = 매 쪽 바닥 인쇄.
- 그림은 전부 래스터 (PyMuPDF 로 확인) — 판독은 원 래스터 (최대 2920×4097) 에서 눈금 위치 자동 탐지 + 색 표지 무게중심 (침식으로 선 · 오차막대 제거).  Fig 1 의 194 MPa 판독 0.731 mS/cm = 인쇄 0.73 (195 MPa) 로 보정 확인.
- τ_ion (486 · 98 MPa) 을 Fig 5 · 6 판독 + Eq 5 로 다시 계산해 Fig 8b 와 ±5 % 안 일치 (§3-6).
- 그림 크롭 16 장 = 본문 Figure 1–12 · SI Figure S1–S4 (표 없음) · **2 장 손 크롭** (fig_9 왼쪽 빈 여백 95 pt 제거 · fig_S2 = 자동 추출이 "거의 백지" 로 빼서 래스터 경계 + 2 pt 로 손 크롭) — `figures.json` 의 `recrop` · `manual_crop`.
- 정본 litdb 중복 확인: DOI · 제목 낱말 papers/ 전수 grep — 없음 (같은 1저자 AMI 2026 논문은 다른 논문).

## 🔗 관련 카드
- 같은 그룹: `miss2026_insitu_conductivity_porosity_pressure_compaction` · `cronau2021_stack_pressure_ionic_conductivity` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `hlushkou2018_void_space_ion_transport_assb_cathode`.
- τ 규약: `tjaden2018_tortuosity_review_calculation_approaches` · `minnmann2021_jes_charge_transport_bottlenecks` · `landesfeind2016_tortuosity_eis_electrodes_separators` · `nguyen2020_electrode_tortuosity_factor` · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`.
- 압밀 · DEM: `so2021_dem_mold_pressure_assb_coldpress` · `so2022_dem_compaction_coated_particles_assb` · `trevisanello2021_sc_pc_ncm_cracking_diffusion`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
