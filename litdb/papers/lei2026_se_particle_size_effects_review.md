<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = schlautmann2023_se_particle_size_composite_transport.md (같은 크기 묶음).  이 논문은 **리뷰**다 — 새 자료가 없고, 모든 수치는 다른 논문에서 옮긴 값이다.
     그래서 카드의 초점은 (i) SE 입도 효과의 기전 · 절충 지도 (ii) 입도 제어 합성 경로와 그 부작용 (iii) 복합양극에서 입도 → 물성 관계 (iv) 리뷰 자체의 인용 · 수치 결함 이다.
     쪽 표기: "p.N" = 인쇄 쪽 "Page N of 34" (= PDF N 쪽).
     값 표지: [리뷰] = 리뷰가 자기 서술로 적은 값 · [2차 · ref N] = 리뷰가 ref N 의 결과로 옮긴 값 (원 논문은 우리가 열지 않음 → 인용 전 원문 확인 필수) ·
     [판독] = 그림에서 읽은 값 (TREND 전용) · [우리 산술] · [추정] · [미확인] = 리뷰 34 쪽 전수에 없음.
     원문 전수: 본문 1–26 쪽 텍스트 층 전부 정독 · 참고문헌 210 개 중 본문 절에서 쓴 것만 대조 (번호 · 서지) · 의심 문장 (단위 빠짐 · 같은 값 반복) 은 렌더 이미지로 원문 확인.
     그림 크롭 9 장 = Fig. 1–6 + Table 1–3 (Table 3 은 쪽이 가로로 돌아 있어 시계 방향 90° 회전) — 전부 열람. -->
# 고체전해질 (SE) **입도 효과** 리뷰 — 입도 제어 합성 경로 (고상 · 액상 · 비전통) · 입자 단위 물성 (이온전도 · 화학 안정성 · 기계 물성 · 충진 밀도 · 계면 적합성) · 복합양극 (단층) · 다층 설계의 **절충**: 작은 SE = 접촉 · 충진 · 기계 강도 ↑ 이지만 부반응 · 응집 · 입계 ↑, 큰 SE = 이온전도 ↑ 이지만 치밀화 · 퍼콜레이션 ↓ — Lei · Peng · Wei · Cheng · Xie (HUST · Electrochem. Energy Rev. 2026)

> slug `lei2026_se_particle_size_effects_review` · DOI `10.1007/s41918-026-00288-x` · type `review (secondary compilation — no new data · 210 refs · sulfide/oxide/halide SEs: size-control synthesis routes · size-dependent intrinsic properties · composite-cathode (monolayer) and multilayer applications · outlook; no DEM/MPM, no new simulation)` · PDF `23704322-3._Review_of_Particle_Size_Effects_of_Solid_Electrolytes_in_All-Solid-State_Batteries.pdf` (34 쪽) · digested `2026-10-30` · status ✅
> topic: size_effect (SE 입도 효과)
> 묶음 역할: **표준 그림 · 절충 점검표 (리뷰)**
>
> **저자 · 소속 (p.1)**: **Tianyu Lei**¹'² · **Linfeng Peng**¹'² (공동 1저자) · Chaochao Wei³ · Shijie Cheng¹'² · **Jia Xie**¹'²\* (¹ Huazhong Univ. of Science and Technology, State Key Laboratory of Advanced Electromagnetic Technology · ² HUST School of Electrical and Electronic Engineering · ³ Lingnan Univ., School of Interdisciplinary Studies, Hong Kong) · 교신 xiejia@hust.edu.cn · *Electrochem. Energy Rev.* **(2026) 9:16** (34 쪽) · 접수 2025-09-21 · 수정 2025-12-16 · 승인 2026-03-17 · © Shanghai University and Periodicals Agency of Shanghai University 2026 · 연구비 NSFC 52425706 (China National Funds for Distinguished Young Scientists) · 이해충돌 없음 [인쇄 p.1 · p.26].
> **정본 litdb 이웃 (링크만)**: [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md) (리뷰 ref [190] · Fig. 5h–i) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref [188] · Fig. 5a–b · g) · [`faka2026_particle_size_consolidation_strain_lpscl`](faka2026_particle_size_consolidation_strain_lpscl.md) (같은 1저자 V. Faka 의 다른 논문 — 리뷰 ref [133] 은 Faka 2024 JACS 압력 유도 전위) · [`schneider2023_particle_size_pressure_transport`](schneider2023_particle_size_pressure_transport.md) (ref [134]) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (ref [177]) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (ref [45]) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (ref [43]).

---

## 0. 결론 먼저 — 우리 질문 (50 kg 4차년도 SE 입도 보고 p1–p7) 에 대한 답

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 이 리뷰가 정리한 "SE 입도 효과" 의 골격** | 작은 SE: 비표면적 · 충진 밀도 · 기계 강도 ↑ → 낮은 tortuosity · 밀착 · 이온/전자 경로 ↑ (고-로딩 양극에 유리) / 그러나 **응집 · 부반응 (높은 화학 반응성) · 입계 밀도 ↑ (σ ↓)**.  큰 SE: 이온전도 · 가공성 ↑ / 그러나 치밀화 · CAM · 탄소와의 퍼콜레이션 망 형성 ↓.  "다중 스케일 접촉이 만드는 불균질 계면 + 3D 퍼콜레이션 망이 ASSB 성능을 정한다" | [리뷰 p.1–2 초록 · 서론] · `Fig. 4e` 레이더 |
| **Q2 입도 제어 경로 (합성)** | 고상 (고에너지 볼밀 · 보조 소결 · 체가름) · 액상 (저에너지 습식 밀링 LWM · 공침 CDC · 용매 극성 재결정) · 비전통 (제트밀 · 원료 전처리 · 동결건조 · 기계적 합금 · 고온 충격 HTS) — **입도를 줄이는 공정이 거의 늘 σ 를 깎거나 불순물 · 응집을 남긴다** (예: 제트밀 LPSCl 2.0 → 0.23 mS cm⁻¹ [2차 · ref 72]) | §3-1 · `Table 1` · `Fig. 2` |
| **Q3 복합양극에서 입도 → 물성** | λ = D_CAM/D_SE 가 클수록 (SE 가 작을수록) 고-로딩에서 CAM 이용률 ↑ (Shi) · 작은 SE → 기공 ↓ · 피복 ↑ (Lee 2025 Joule: SE 1.4 vs 4.9 µm → 피복 94.8 vs 83.1 %) · 작은 SE → 두께 방향 SOC 기울기 ↓ (Jeong 2024) · "빠르기만이 아닌 **균형** 수송" (Schlautmann) · 크고 작은 SE 혼합 (Wang 2024 · Peng 2023) | §3-6 · `Fig. 5` · `Table 3` [2차] |
| **Q4 리뷰의 신뢰도** | **그림 출처 · 수치에 결함이 여럿** — Fig. 3a · 5i · 6a 캡션 출처가 본문 · 그림 내용과 안 맞고, 단위 빠진 범위 (*"0.1 to 0.1 mm"* · *"10 to 10 µm"*) · 같은 값 반복 (Padarti · Peng 7.02) · 축 오기 (Fig. 5g) 등.  ⇒ **수치는 원 논문에서 다시 확인한 뒤에만** 인용 | §9 |
| **Q5 우리에게** | ① **p1 · p7 점검표** — 문헌의 표준 그림 (PSD · SEM · 순수 SE σ(d) · 기공 · 피복 · tortuosity · 이용률 · 용량) 과 절충 축 (레이더) 을 한 장으로 준다 ② **p5** — 입도를 줄인 SE 의 σ 하락은 **공정 (비정질화 · 불순물 · 손상) 과 교란**된다고 리뷰 자신이 적는다 (*"cannot be attributed solely to the decrease in particle size"*) → 우리 손익분기선의 σ 비 (2.217) 를 *"입계 증가 때문"* 으로 쓰지 않는 근거 ③ 우리 DEM 은 레이더의 **구조 절반** (충진 · 접촉 · 퍼콜레이션 · tortuosity) 만 담고 **재료 절반** (σ(d) · 화학 안정성 · 응집 · 파괴) 은 입력 · 범위 밖 ④ **다음에 정본 카드로 만들 원 논문**: Jeong 2024 (SE 입도 × 두께 방향 SOC · EDXRD) · Lee 2025 Joule (SE 입도 → 피복 · 탈착) · Dixit 2021 (SE 패킹 · A_SE/A_AM) | §8 · §10 |

⇒ **한 문장**: SE 입도 효과를 **합성 → 입자 물성 → 복합양극 → 다층** 순으로 묶은 2026 년 리뷰 — 우리에게 쓸모는 **절충 지도와 표준 그림 점검표**이고, 개별 수치는 2 차 인용이라 (그리고 리뷰의 인용 결함이 있어) **원 논문 카드를 거쳐서만** 쓴다.

---

## 1. 한 줄 요약
SE 입도는 이온전도 (입계 · 비정질화) · 화학 안정성 (깁스–톰슨 표면 에너지 · 비표면적) · 기계 물성 (홀–페치 경도 · 파괴인성 · 크기 의존 파쇄) · 충진 밀도 (작은 입자의 재배열 · 소결 활성) · 계면 적합성 (접촉 면적 · 곡률 · 응력) 을 동시에 바꾼다.  리뷰는 이 절충을 레이더 (`Fig. 4e`) 로 요약하고, 복합양극에서는 λ = D_CAM/D_SE · SE 분율 · PSD · 피복을 tortuosity 를 줄이는 핵심 매개변수로 정리한다 (`Table 3`).  결론은 *"작은 입자 = 접촉 밀도 · 이온 퍼콜레이션 ↑ 이지만 응집 · 입계 저항 위험, 큰 입자 = 응력 열화 완화 · 이온전도 효율 ↓"* — 이중 (bimodal) 분포 · 층별 입도 · 다중물리 모델 · in situ 진단을 앞으로의 방향으로 든다.

## 2. 메타 / 범위 / 구성

| 저자 | 저널 / 년 | DOI | 범위 | 유형 |
|---|---|---|---|---|
| Lei · Peng (공동 1) · Wei · Cheng · Xie\* (HUST · Lingnan) | *Electrochem. Energy Rev.* **9**:16 (2026) · 34 쪽 · 참고문헌 **210** | 10.1007/s41918-026-00288-x | 황화물 (아지로다이트 · LGPS · Li₇P₃S₁₁ · LPS) · 산화물 (LLZO · LLZTO · LATP) · 할라이드 (Li₃InCl₆) SE | 리뷰 (새 자료 · 새 계산 없음) |

- **구성** (절 번호 = 원문): 1 서론 (`Fig. 1` 세 실패 모드) → 2 입도 제어 전략 (2.1 고상 · 2.2 액상 · 2.3 비전통 · `Fig. 2` · `Table 1`) → 3 입도가 SE 물성에 주는 영향 (3.1 이온전도 · 3.2 화학 안정성 · 3.3 기계 물성 · 3.4 충진 밀도 · 3.5 계면 적합성 · `Fig. 3` · `Fig. 4` · `Table 2`) → 4 ASSB 응용 (4.1 단층 = 복합양극 · 4.2 다층: 4.2.1 모사 · 기하 모델 · 4.2.2 덴드라이트 억제 이종구조 · 4.2.3 다크기 혼합 양극 · 4.2.4 층별 입도 분포 · `Fig. 5` · `Fig. 6` · `Table 3`) → 5 전망 (4 항) → 6 결론.
- **세 실패 모드와 입도 대응** (`Fig. 1`, p.2–3): (a) 고-로딩 양극의 높은 tortuosity → 이온 수송 동역학 제한 (불균형 SE/CAM 크기비 → 끊긴 퍼콜레이션 · 길고 굽은 Li⁺ 경로 → 작은 SE 일부 섞기) · (b) 국부 응력 아래 입자 파편화 → 고체–고체 접촉 손실 (입도 미세화 → 기공 ↓ · 응력 집중 ↓ · 입계 미끄럼이 부피 변형 흡수) · (c) 계면 결함으로 Li 금속 침투 (작은 SE → 공극 · 결함 ↓ · 고른 전류) [리뷰].

## 3. 핵심 수치 ★ (전부 2 차 인용 — 원 논문 확인 전 인용 금지)

### 3-1. 입도 제어 경로와 부작용 (§2 · `Table 1` · `Fig. 2`)
| 경로 | 예 (재료 · 조건 → 결과) | 부작용 · 한계 | 표지 · 쪽 |
|---|---|---|---|
| 고에너지 볼밀 (HDM) | LLZO 10 µm → 200 nm (6 h) [84] · Li₅.₅PS₄.₅Cl₁.₅ 50 → 1 µm (500 rpm 5 h) [85] · Li₃PS₄ 입도가 매체 지름 5/7/10 mm 에 6.9/7.1/11.2 µm · 회전 600/800/1000 rpm 에 6.2/11.2/16.5 µm (응집) · 1200 rpm 4.9 µm 최소 · [PS₄]³⁻ 90 % 전환 = 1200 rpm 3 h vs 600–1000 rpm ≥ 20 h [79] · 1 kg 배치 고속 건식 혼합 18,000 rpm 3 min [86, 87] | 넓은 분포 (밀링 후 황화물 D50 1.2 µm · D90 5 µm) · 격자 손상 (LLZO 입방 → 정방, σ −20 %) · 매체 · 용기 오염 (WC · ZrO₂) · 건식 밀링 = 습식보다 큰 SE · 넓은 분포 → 이온 tortuosity ↑ [78] | [2차 · p.4] |
| 보조 소결 | Al-LLZO 1230 °C 최대 결정립 24 (2 h) · 36 (4 h) · 84 µm (8 h) [93] · LLZTO 1 °C min⁻¹ 승온에서 치밀 [리뷰] · 탄소 첨가로 LLZO 결정립 7.87 → 5.88 (흑연) · 3.98 µm (아세틸렌 블랙), Li₂CO₃ 분해 780 → 720 °C [94] | 거친 분말 = 고온 · 밀도 ↓ · 빠른 승온 = 기공 ↑ · 불균일 성장 | [2차 · p.4–5] |
| 체가름 | 400 mesh ≈ 38 µm · D90/D10 < 3 · LGPS 20/10 µm 나일론 망: 원료 D50 4.3 µm (PI 0.51) · Class A 2.8 (0.43) · Class B 5.9 µm (0.51) [80] | 단단한 SE (LLZO) 는 모서리 파편 · 비표면 ↑ · 점성 재료는 망을 막음 | [2차 · p.5–6] |
| 저에너지 습식 밀링 (LWM) | Li₅.₃PS₄.₃ClBr₀.₇ 헵탄 4.0 mL + 디부틸에터 0.8 mL → D95 **1.25 µm** vs HDM 3.17 µm · 복합양극 (AM:SE 8:2) 공극 **13.5 vs 22.7 %** [78] · Li₆PS₅Cl p-자일렌 7 mL · 200 rpm 2 h → (1.8 ± 1.1) µm vs HDM 600 rpm (2.42 ± 2.81) µm [리뷰, 인용 번호 없음] · Li₇P₃S₁₁ 합성 > 20 → < 5 h (ACN · DME) [97] | 용매 오염 · 이상 입자 성장 (IPA 습식 → H-LLZO ≈10⁻⁶ S cm⁻¹ · 건조 42 h · 진동 충진 0.7 g cm⁻³ · 소결 후 100–200 µm 이상 성장 [104]) · 비용 | [2차 · p.6] |
| 공침 (CDC) | NAP–THF 에서 Li₆PS₅X (X = Cl, Br, I) · Li₃PS₄ · Li₃SbS₄ · Li₄SiS₄ [96] · Li₂S 나노결정 20 → 6 nm (전구체 0.4 → 1.6 mol L⁻¹, PI 4 → 2) [107] · Li₂S 228 ± 72 / 177 ± 49 / 546 ± 74 nm (S 0.075 / 0.150 / 0.300 mol L⁻¹) [102] | 과포화 최적점 존재 | [2차 · p.6–7] |
| 용매 극성 재결정 | Li₆PS₅Cl 7.91 µm → 입구 지름 · 교반으로 3.56 / 2.19 / 0.88 µm · 아지로다이트 상 94.1 → 96.2 % · σ **1.27 · 1.45 · 1.54 vs 원료 1.81 mS cm⁻¹** [96] · Li₃InCl₆: 양성자성 (H₂O 15 nm · 2.72 · EtOH 20 nm · 3.07 mS cm⁻¹) vs 비양성자성 (ACN 82 nm · 3.67 · THF 92 nm · 4.03 mS cm⁻¹) — 결정자 · 미세변형 · 응집 [108] | 비양성자성 = 응집 ↑ | [2차 · p.7] |
| 제트밀 | Li₆PS₅Cl 40 µm → D50 **1.9 µm** (볼밀은 14.7 µm) · σ **2.0 × 10⁻³ → 2.3 × 10⁻⁴ S cm⁻¹** (결정성 ↓ · 입계 부피 ↑) · 150 / 200 °C 저온 열처리 → 2.3 × 10⁻⁵ · 4.1 × 10⁻⁶ (Li₂S · LiCl · Li₄P₂S₆ 2.38 × 10⁻⁷ 생성, 표면 S 손실) · 450 °C → 2.2 × 10⁻³ 회복하나 응집 · 결정립 성장 [72] | 표면 손상 · S 손실 | [2차 · p.8] |
| 원료 전처리 | Li₂S 8 µm → < 2 µm (WBM, 프로피온산 에틸 800 rpm 1 h) · (0.34 ± 0.11) µm (용해–석출 + 500 °C 3 h) → Li₃PS₄ 1.32 µm (판상) → 93 nm (구형) — **Li₂S 크기와 선형 관계** (Ohsaki 2021) [74] | 기전 불명 · 절차 비일관 | [2차 · p.8] |
| 동결건조 | Li₃InCl₆ 80 % 가 < 200 nm (수화법 61.43 % < 400 nm · 볼밀 50.01 % < 400 nm) · NCM90 ASSB 20 C (9.98 mA cm⁻²) 30,000 사이클 > 70 % · CAM 95 % 로딩 49 C 충전 [73] | 용해도 · 화학 불활성 조건 엄격 | [2차 · p.8] |
| 기계적 합금 · HTS | 1200 rpm 초고속 → 11.7 mS cm⁻¹ [110] · HTS (250 °C s⁻¹) Li₆PS₅Cl **40.4 nm · 4.2 mS cm⁻¹** vs 통상 59.4 nm · 3.7 · 소성 30 s vs 10 h · 0.002 vs 0.033 kWh g⁻¹ [112] | 장비 요구 엄격 | [2차 · p.8–9] |

**`Table 1` 전문 (p.9, 인쇄)**
| 방법 | 재료 | 입도 / µm | 분포 | σ / (mS cm⁻¹) | 환경 영향 | Ref. |
|---|---|---|---|---|---|---|
| 고에너지 건식 밀링 | LLZO | 0.2 | Wide | 0.26 | Friendly | [84] |
| 보조 소결 | LLZO | 600 | Wide | 0.57 | — | [84] |
| 체가름 | LGPS | 5.9 | Narrow | 9.21 | — | [80] |
| 저에너지 습식 밀링 | LPSClBr₀.₇ | 0.79 | Narrow | 1.09 | Unfriendly | [78] |
| 공침 | Li₆PS₅Cl (LPSC) | 5 | Narrow | 5.71 | — | [96] |
| 용매 교환 | LIC | 0.02 | Narrow | 3.07 | — | [108] |
| 제트밀 | LPSCl | 1.9 | Narrow | 0.23 | Friendly | [72] |
| 원료 전처리 | LPS | 0.093 | Narrow | 0.15 | Unfriendly | [74] |
| 동결건조 | LIC | < 0.2 | Narrow | \ | Unfriendly | [73] |
| 기계적 합금 | LPSClBr₀.₇ | 0.017–0.079 | \ | 11.7 | Friendly | [110] |
| 고온 충격 | Li₆PS₅Cl | 0.04 | \ | 4.2 | Friendly | [112] |
- ⚠ "입도" 열에 입자 크기와 **결정자 크기** (LIC 0.02 = Bonsu EtOH 결정자 20 nm · HTS 40.4 nm) 가 섞여 있다 · 공침 행 (LPSC 5 µm · 5.71) 은 본문 Ali [96] 서술 (0.88–3.56 µm · ≤ 1.81 mS cm⁻¹) 에 없는 값 [리뷰 대조 · §9].

### 3-2. 이온전도 ↔ 입도 (§3.1, p.10–12)
| 예 | 값 | 표지 |
|---|---|---|
| 황화물 입계 저항은 작고 σ 높음 | LGPS 10 · Li₅.₅PS₄.₅Cl₁.₅ 8.3 mS cm⁻¹ · 산화물은 입계 σ 가 체적의 1–10 % 까지 | [2차 · 28, 66 · 리뷰] |
| Yamada (LWM 250 min, 10 mm 볼) | σ **2.5 → 0.25 mS cm⁻¹** · 입도 20 → 1.0 µm · 원인 가설 = 부분 비정질화 · CAM/SE 크기비와 용량의 절충 (작은 SE = 접촉 ↑ 첫 방전 ↑ / 너무 작으면 입계 저항 ↑ → 상쇄) | [2차 · ref 80 · `Fig. 3a`] — ⚠ 재료명 · 출처 혼선 §9-1 |
| Peng (결정성 Li₅.₅PS₄.₅Cl₁.₅) | 습식 유리세라믹 대비 건식 볼밀 **7.02 × 10⁻³ vs 2.78 × 10⁻³ S cm⁻¹** · 리뷰: *"cannot be attributed solely to the decrease in particle size and the partial amorphization … impurities and material decomposition … may also contribute"* | [2차 · ref 85 · 리뷰 문장] |
| Sharafi (LLZO) | 80 µm 0.56 mS cm⁻¹ (상대밀도 99.4 %) vs 5 µm 0.46 (96.0 %) · 같은 밀도 99.4 % 에서 600 vs 80 µm 0.57 vs 0.56 (거의 같음) | [2차 · ref 84] |
| LLZO 밀도 (같은 문단 · 출처 번호 없음) | 상대밀도 79 → 94 % 에서 4.30 × 10⁻⁶ → 1.35 × 10⁻⁴ S cm⁻¹ · Padarti: 같은 밀도 79 % 인데 900 · 1000 °C 소성이 다른 σ (Li₂CO₃ 상 진화) — 두 값이 같은 수로 인쇄됨 (§9-5) | [2차 · ref 132] |
| Horii (Al-LLZO 저항망 + 전지 모델) | 입계 두께 7.5 nm 가정 · 결정립 0.1 nm–0.1 mm 계산 · 10 nm 아래 → 입계값 **9.6 × 10⁻⁷** · > 75 µm (비 > 10⁴) → 내부값 **7.7 × 10⁻⁴ S cm⁻¹** 접근 · 큰 변화 = 10 nm–10 µm (비 1–10³) · 0.1 C · 100 µm 에서 이론 에너지 **96 %** · 10.6 C 에서 0.739–0.825 · *"결정립은 입계 두께의 ≈10 배 이상"* | [2차 · ref 131 · `Fig. 3b–c`] (리뷰 본문은 단위가 빠짐 — §9-6) |
| Faka (Li₆PS₅Br) | 압력 유도 전위 · 내부 변형 ∝ 전위 밀도 · σ 0.4–1.0 mS cm⁻¹ (파이프 확산 유사 · 활성화 에너지 불변) | [2차 · ref 133] |
| Schneider (t-Li₇SiPS₈) | 체가름 < 50 vs > 50 µm: 작은 쪽 = 소성 변형 · 큰 쪽 = 취성 파쇄로 기공 채움 · 최종 밀도 수렴 · σ **4.1 vs 5.7 mS cm⁻¹** · 0.1 GPa 에서 체적형 σ · 0.01 GPa 는 입자 간 접촉 저항 지배 | [2차 · ref 134] (정본 카드 `schneider2023_particle_size_pressure_transport`) |

### 3-3. 화학 안정성 (§3.2, p.12–13)
- 깁스–톰슨 (식 1): ΔG_react = ΔG_bulk + (2γV_m/r)·ΔA — 작은 입자 = 표면 에너지 ↑ → 열역학 불안정 · 비표면적 ↑ · 곡률 유도 공공 ↑ → 반응 가속 [리뷰] (⚠ 리뷰는 r 을 *"particle diameter"* 라 적는다 — 깁스–톰슨의 r 은 반지름).
- LLZTO 분말 (용융 → 공기 제트밀 → 체): 0.40 µm (S_BET 5.62 m² g⁻¹) · 0.83 µm (2.73) · 4.93 µm (0.76) · 수화 반응 속도 상수 ∝ 비표면적 · 수화 = 탄산화의 선행 단계 [2차 · ref 51].
- Al-LLZO 반대 결과: 큰 입자 ASR **103 → 880 Ω cm²** (공기 24 h) vs 작은 입자 **38 → 64** · 원인 = 표면 Al · Li 분포 (큰 결정립은 액상 소결로 Al 이 입계에 분리) [2차 · ref 135 · `Fig. 3e`].
- 밀링 Li₆PS₅Cl: 비표면적 ↑ → 4.0 V 위 산화 안정성 ↓ · 환원 쪽은 더 안정 (치밀 미세구조) [2차 · ref 140 · `Fig. 3f`].

### 3-4. 기계 물성 (§3.3, p.13–14)
- LLZO (Sharafi): 경도 **(9.88 ± 0.49) → (6.86 ± 0.49) GPa** (평균 결정립 5 → 600 µm) · 홀–페치 H = H₀ + K_H d^(−1/2) (식 2) · 파괴인성 **(0.82 ± 0.07) → (0.60 ± 0.05) MPa m^½** (5 → 40 µm, ≥ 40 µm 에서 0.60 = 단결정값) · γ = K_IC²/2E (식 3) → **1.24 J m⁻²** (K_IC 0.60, E 150 GPa) [2차 · ref 84 · `Fig. 3g`].
- 파괴 응력 σ_c = K_IC (π d_c)^(−1/2) (식 4) — d_c = 기공 · 결정립 같은 임계 결함 크기 [리뷰].
- LGPS–Li 반응 (Zhao, in situ): **> 3 µm 분쇄 (pulverization) · 1–3 µm 균열만 · < 1 µm 균열 거의 없음** · 임계 파편화 크기 식 (5) (탄성 변형 에너지 µ_e = 0.375 eV nm⁻³ · α ≈ 15) → < 1 µm 에서는 탄성 에너지가 균열 진전에 모자람 [2차 · ref 62 · `Fig. 3h`] (서론 p.2 에도 같은 수치).
- 다결정 SE 의 덴드라이트 손상 모사 (Jiao): 평균 결정립 D_AS ≥ 0.4 µm = 입계 따라 "damage arms" · ≤ 0.1 µm = 솜털형 (flocculent) 손상 급증 · **최적 0.2 µm** (파괴 시간 최대 1.41 s) [2차 · ref 145] · LLZO (Xu): 2 µm 큰 결정립 = 계면 응력 집중 · 입계 균열 관통 · 0.2 µm = 고른 응력이나 선형 손상 확산 · 입계/결정립 인장강도 비 λ 에 따라 손상 단조 증가 또는 화산형 [리뷰, 인용 번호 없음].

### 3-5. 충진 밀도 · 압력 (§3.4, p.14–18 · `Fig. 4a–b` · `Table 2`)
- LLZTO 소결: D1.2 (1.2 µm) 열린 기공 < 1 % · D532.2 (532.2 µm) > 30 % · D1.2 를 섞어도 늘 줄지 않음 — D2.2 혼합만 D1.2 수준 · D4.1 · D9.5 혼합은 D1.2 분율과 함께 줄었다 늘어남 · 소결 활성 차로 미세 입자가 응집 · 이동 → 고리형 기공 · 표면 에너지 식 (6)–(7) E_r = 3E₀/(ρr) [2차 · ref 156 · `Fig. 4a`].
- 열간 압축 Li₃InCl₆ 250 °C: σ 4 배 (**4.4 × 10⁻³ S cm⁻¹**) · 상대밀도 80.3 → 93.67 % [2차 · ref 150].
- LPS 상대밀도 ≈95 % 넘으면 덴드라이트 완화 (89.2 % = 이어진 큰 기공 · 99.9 % = 고립 기공, 실패가 계면 Li 고갈로 바뀜) [2차 · ref 154].
- **LPSCl (Lin)**: 보통 3–5 µm vs 미세 ≈1 µm · 성형 100 · 300 · 500 MPa → 미세@500 MPa = 고른 기공 · tortuosity **1.05–1.13** · 보통@100 MPa = 이질 기공 · **1.17–1.30** · CCD 100 MPa 0.3–0.4 → 500 MPa > 1 mA cm⁻² · 절대 기공도와 무관 (보통@500 ≈ 미세@300) · 원인 = 기공 · 입계 연결성 + 국부 전류밀도 ("hot spot") [2차 · ref 157 · `Fig. 4b`] → `Fig. 4b` 판독: 미세 6.1 · 7.6 · 9.6 % → CCD ≈1.30 · 1.23 · 0.40 · 보통 13.9 · 15.4 · 17.9 % → ≈1.27 · 1.00 · 0.33 mA cm⁻² [판독].
- Li₅.₃PS₄.₃ClBr₀.₇ 나노 응집체 450 °C 열처리 → 한 변 2 µm 입방 · 상대밀도 80.2 → 89.5 % [2차 · p.17].
- 기공 배열 모사 (Dixit LLZO): HCP τ ≈ 1.209 · BCC 1.20–1.45 · FCC 1.59–1.89 · 평행육면체 τ = 1 (축 방향) [2차 · ref 158].
- **`Table 2` (p.17, 인쇄)**: 제조 압력 — SE 층: 낮은 압력 = 작은 입자 *"Good contact"* / 큰 입자 *"Poor contact"* · 높은 압력 = 작은 입자 *"Rearrangement"* / 큰 입자 *"Particle fragmentation"* → 역할 = 고체–고체 접촉 ↑ · 충진 밀도 ↑.  운전 압력 — 기계 안정 유지: 작은 = 응력 분산 · 공극 회피 / 큰 = 심한 응력 집중 (균열 · 탈착) → 입자 접촉 유지 · 구조 보존 · 덴드라이트 억제: 작은 = 물리 장벽 (높은 기계 모듈러스) → 음극 구멍 채움 · 침투 억제.
- 복합양극 압력 (리뷰 서술, p.17): 적절한 제조 압력 = 작은 입자 성분을 굳혀 연속 저기공 경로 · 지나치거나 모자란 압력 = SE 망을 끊는다 (예: AM 이 SE 상으로 파고듦) → tortuosity ↑.

### 3-6. 계면 적합성 (§3.5, p.18–19)
- 전고체 Li–S (Fan): 나노 Li₂S 9.4 nm · 나노 Li₃PS₄ 44 nm 조합 = 초기 계면 저항 **26.9 Ω** (vs 51.4 · 48.3) · 증가폭 **72.3** (vs 147.1 · 570.5 Ω) · 마이크로 Li₂S–나노 LPS = 첫 1,138 mAh g⁻¹ 이나 이용률 23.3 % [2차 · ref 165].
- AN-Li₆PS₅Br (결정자 74 nm) vs AN-BM (22 nm): 체적 · 입계 Li 이동도 거의 같음 · 작은 쪽이 용량 유지 ↑ (Li₂S 와 접촉 면적) [2차 · ref 164].
- NMC 단결정 · 다결정 2D FEM (Taghikhani): 계면 분리 최대 틈 **9.3 nm (r_s 0.5 µm) · 16.0 (1.5) · 13.8 (3.0)** — 비단조 · 큰 입자 = 변형 "스프링" 이 결합 ↑ 이지만 응력 ↑ · NMC811 내부 응력 = 화학 팽창 · 큰 입자에서 큼 [2차 · ref 166 · `Fig. 4c`].
- Li|Li₆PS₅Cl: 큰 결정립 (LG) = 뾰족한 형상에서 전류 집중 → 덴드라이트 · 작은 결정립 (SG) = 고른 전류 · 입계 tortuosity 가 Li 진전을 늦춤 [2차 · ref 61, 167 · `Fig. 4d`].
- **`Fig. 4e` 레이더 (p.15)**: 이온전도 · 화학 안정성 = **큰 입자 우세** · 충진 밀도 · 계면 적합성 · 기계 물성 = **작은 입자 우세** [리뷰 · 판독].

### 3-7. 복합양극 (단층) — 이 카드의 핵심 (§4.1, p.18–21 · `Fig. 5` · `Table 3`)
| 연구 (ref) | 계 · 변수 | 리뷰가 옮긴 결과 | 표지 |
|---|---|---|---|
| Strauss [184] | NCM622 + β-Li₃PS₄ · **CAM** NCM-S (D50 4.0 · D90 4.8 µm) vs NCM-L (15.6 · 26.1 µm) | 첫 충전 162 → 84 mAh g⁻¹ · 첫 CE 70 → 50 % · 전기화학 비활성 CAM 2 → 31 % · 이온 σ 무관 · 전자 σ 10⁻³ → 10⁻⁶ S cm⁻¹ | [2차] |
| Jiang [185] | CAM 3.0–11.3 µm × SE 질량분율 40–90 % | CAM 질량분율 = 2.49 × 입도 + 41.3 (선형) · 6.2 µm 에서 CAM 분율 +50 % → 평균 σ_e +4 자릿수 · σ_ion −1 자릿수 · 최적 60 wt% CAM (6.2 µm) | [2차] |
| **Shi [188]** | λ = D_CAM/D_SE · θ_CAM = V_activeCAM/V_CAM · f_CAM = 0.95 M_CAM/(M_CAM + M_SE) | f_CAM < 70 wt% 이면 θ = 1 · > 75 wt% 에서 급락 (f_CAM 90 % 에서 θ = 0.1) · f_CAM 70 % 에서 λ 4 → 0.5 이면 θ 1.0 → 0.2 · *"liquid-cell-level 부피 로딩 (≈50 vol%) = 큰 CAM ≈12 µm + 작은 SE ≈1.5 µm"* · `Fig. 5a–b` (70 wt% CAM + 3 µm SE) · `d–e` (80 wt% + 5 µm SE) | [2차] · 정본 `shi2019_…` |
| Shen [189] | 할라이드계 · 양극 · 전해질 < 500 nm | 85 wt% 로딩 0.1 C **175 mAh g⁻¹** vs 큰 입자 (30 · 5 µm) **38 · 62** | [2차] |
| **Schlautmann [190]** | Li₆PS₅Cl 4 · 11 · 20 · 40 µm | 결정성 같음 · 작은 SE 가 고르게 분포 → 연속 이온 경로 · 이온 σ 에 더 큰 영향 · σ_ion/σ_el → 1 (균형) 일 때 용량 ↑ (`Fig. 5h–i`) | [2차] · 정본 `schlautmann2023_…` |
| Park (리뷰 본문은 *"Yoon Chung et al."*) [172] | LATP-SS D50 1.521 µm (0.6276 m² g⁻¹) vs LATP-CP 0.423 µm (5.3687 m² g⁻¹) | σ 1.0 × 10⁻⁴ vs 0.45 × 10⁻⁴ S cm⁻¹ · 작은 쪽 첫 CE **84 vs 70 %** · 100 사이클 유지 **65 vs 50 %** | [2차] |
| **Jeong [191]** | LPSC-S (< 1 µm) vs LPSC-L (3–5 µm) · 싱크로트론 X 선 단층 + **EDXRD** + 중간 규모 모델 | 0.1 C SOC 진화: 작은 SE = 분리막 → 집전체로 이온 퍼콜레이션 효율적 · 기울기 작음 · 큰 SE = **심한 기울기 → 집전체 쪽 미활용** (`Fig. 5c · f`) · 작은 SE = 기공 부피분율 ↓ · AM 이용률 ↑ · 큰 SE = 낮은 압력에서 불균일 부피 변화 · 변위 ↑ → 국부 응력 | [2차] — 정본 카드 없음 |
| **Lee [192]** (Joule 2025) | SE **1.4 vs 4.9 µm** → CAM–SE 피복 | 높은 피복 **94.8 %** (고름) vs 낮은 **83.1 %** (국부 응집) · 사이클 뒤 **78.8 vs 57.2 %** · 국부 저피복 → 불균일 반응 · Li⁺ 농도 기울기 · 비동기 변형 → 자기촉매 탈착 | [2차] — 정본 카드 없음 |
| Liu TGH [193] | **CAM** 크기 기울기 (15–20 · 8–15 · < 8 µm 세 층, 각 ≈35 µm) · 20 mg cm⁻² · ≈100 µm | 100 사이클 뒤 TGH **116 mAh g⁻¹** · 일반 전극 20 사이클 뒤 40 · 작은 입자 전극 100 사이클 뒤 28 | [2차] (⚠ SE 입도 아님 · 도전재 · 바인더 슬러리 전극) |
- **`Table 3` (p.22, 인쇄 · 4 열 머리가 3 열과 같은 글자로 반복 — §9)**: SE 입도 D_SE — *"작게: ① 더 고른 채움 → 연속 이온 망 ② CAM 과 접촉 면적 ↑ ③ 국부 병목 ↓ → 미시 수송 저항 ↓"* / 방향 *"줄이되 지나치면 응집"* · CAM 입도 — *"크게: 같은 부피분율에서 입자 수 ↓ → 더 연속된 공간"* / *"고-로딩에서 적절히 키움"* · λ — *"높은 λ = tortuosity ↓ · 낮은 λ = 끊긴 이온 통로 · 이용률 급락"* / *"로딩에 맞춰 · 고-로딩일수록 큰 λ"* · SE 질량 · 부피분율 — *"임계 퍼콜레이션 문턱 아래면 크기 제어와 무관하게 망이 끊겨 tortuosity 무한"* / *"문턱 위 · D_SE · D_CAM 과 함께 최적화해 이온 · 전자 σ 균형"* · PSD · 공간 균일성 — *"좁은 PSD = 더 치밀하고 고른 충진"* / *"고른 분포 추구"* · 피복 · 계면 미세구조 — *"높고 고른 피복 = 고른 Li⁺ 흐름 · 국부 응력 완화 · 탈착 지연"* / *"작고 고르게 분산된 SE 로 피복 ↑"*.

### 3-8. 다층 · 혼합 크기 (§4.2, p.21–25 · `Fig. 6`)
- **SE 패킹 기하 모델 (Dixit [194])**: 10 µm AM 둘레 SE 패킹 · 좁은 분포 = 더 연결된 패킹 · A_SE/A_AM = **1.58 (D_SE 3 µm) · 3.70 (2 µm) · 4.25 (1.5 µm)** · 최고 충진 밀도 = **D_AM/D_SE ≈ 3–4** (예 1.5 / 0.5 µm) · 크기 분산 S_SE ≤ 0.3 µm 에서 밀도 ↑ (분산 ↑ → 기공 ↑) · D_SE 0.5 · D_AM 1.5 µm 패킹의 전위 · 전류 모사 = hot/cold spot 없음 · 단 전자 전도체 · 삼상 경계 미포함 [2차 · p.21–23] (⚠ `Fig. 6a` 캡션은 ref [166] 로 표기 — §9-3).
- LLZO 이종구조 (Cheng [138]): SG 20–40 µm vs LG 100–200 µm · 입계 표면 피복 **32.2 vs 16.5 %** · ±46 µA cm⁻² 에서 SG · SG/LG/SG 안정 · LG · LG/SG/LG 는 20 · 15 h 안 단락 [2차] ↔ Sharafi [84]: 결정립 ≈5 → ≈600 µm 에서 **CCD 0.3 → 0.6 mA cm⁻²** (반대 경향 — 높은 스택압 ≫ 10 MPa 등 시험 조건 차이로 해석) [2차 · p.24].
- **혼합 크기 양극 (Wang [60])**: 작은 LPSCl₁.₅ **20 %** (300 nm–4 µm) + 큰 **10 %** (≈20 µm) (p.24 서술 · ⚠ 서론 p.2 는 *"20% large and 10% small … by weights"* 로 **거꾸로** 적음 — §9-14) · 13–40 mA cm⁻² (5–10 C) 에서 > 3 mAh cm⁻² 안정 · 작은 입자 = 조밀한 퍼콜레이션 이온망 · 큰 입자 = 장거리 경로 · tortuosity ↓ (가설) · Si–Cl (Si 20 µm : 서브 µm SE = 80 : 20) + 흑연 중간층 음극 [2차 · p.24–25] → `Fig. 6e` 판독 (25 °C · 18 mg cm⁻²): 4 C 에서 혼합 촉매전해질 vs Si-Cl ≈156 · 혼합 vs Si-G ≈117 · 큰 촉매전해질 ≈75 · **작은 촉매전해질 ≈54 mAh g⁻¹** (작은 SE 만으로는 율속이 가장 나쁨) [판독].
- **층별 입도 (Peng [85])**: Li₅.₅PS₄.₅Cl₁.₅ L-SE (60 µm, 고상 소결) · S-SE (1 µm, 볼밀) 을 양극 혼합물 / 전해질층에 넣어 L/L · S/L · L/S · S/S 네 구성 · S/L (양극 = 작은 SE · 전해질층 = 큰 SE) 이 25 · −20 °C 에서 최고 · 60 °C 에서는 S/S [2차 · p.25] → `Fig. 6i` 판독: 2.0 C 에서 S/L ≈105 · S/S ≈95 · L/L ≈73 · L/S ≈55 mAh g⁻¹ [판독].

### 3-9. 전망 (§5, p.25–26) · 결론 (§6)
(1) 확장 가능 · 저손상 · 친환경 입도 제어 (좁은 분포 · 기울기 분포 · 미세균열 · 상 균일 · 용매 잔류 · 불순물) · (2) 다중장 결합 최적 구성 (초고 로딩 검증 · 응력 소산과 이온 수송 동시 · *"current simulations predominantly focus on single-physics effects … while neglecting parallel experimental validation under coupled multifield conditions"* → 통합 다중물리 틀 필요) · (3) 다중 스케일 복합 SE (이중 분포 · 거친 결정립 = 덴드라이트 경로 tortuosity ↑ · 미세 결정립 = 침투 구동력 상쇄) · (4) in situ 입자 진화 감시 (EC-AFM · operando X 선 단층 · 응력 자료 기계학습 · ⁷Li NMR 추적).  결론: *"Smaller particles improve contact density and ionic percolation but are associated with increased risks of agglomeration and grain boundary resistance, whereas larger particles mitigate stress-induced degradation but reduce ion conduction efficiency"* [리뷰 p.26].

## 4. 방법 (리뷰 방법) · 입자 처리 · frame[5]
- **문헌 선정 · 검색 기준 · 정량 메타분석 없음** [미확인] — 서술형 리뷰.  수치는 각 절에서 원 논문 값을 옮김 · 그림 6 장은 전부 재사용 (permission) · 표 3 개는 리뷰 작성.
- **입자 처리 ★**: 리뷰가 다룬 모델은 (i) 저항망 + 전지 모델 (Horii · 결정립 · 입계) (ii) 2D FEM 전기화학–기계 (Taghikhani · Jiao · Xu) (iii) 패킹 기하 + 전위 모사 (Dixit · Shi) — **DEM 접촉망 · 소성 형상 변화 · 실 PSD 패킹** 을 명시적으로 다룬 절은 없다 (*"discrete element"* 낱말 0 회) [리뷰 전수 검색].  4.2.1 머리 문장: *"In most simulations in the literature, the particle size values were defined, and the wide range of particle sizes and stacking morphologies formed during actual preparation processes were neglected"* [리뷰 p.21] — 단분산 대리 입도의 한계를 리뷰도 짚는다.
- frame[5]: 리뷰는 **재료 (σ(d) · 화학 · 기계 파괴)** 와 **구조 (충진 · 접촉 · 퍼콜레이션)** 를 한 표 (레이더) 에 섞는다 — 우리 분업으로 나누면 구조 축 = DEM (접촉망 수송 · 패킹) · 형상 소성 = MPM · 재료 축 = 실측 입력 / 범위 밖.

### 4-1. 기법 · 용어 미니사전
- **λ = D_CAM/D_SE** (Shi) — CAM 대 SE 지름 비.  고-로딩일수록 큰 λ 가 필요.  우리 50 kg: NCM D6 / SE 0.7–3 µm → λ = **8.57 · 6 · 3 · 2**.
- **θ_CAM** — 이온 퍼콜레이션 망에 닿은 CAM 부피 / 전체 CAM 부피 (Shi 의 "cathode utilization").  ⚠ 우리 보고에서는 *"활성 AM"* 낱말을 쓰지 않는다 (`KG50B-01`) — *"SE 관통망과 경로가 있는 AM"* 으로.
- **피복 (coverage)** — CAM 표면 중 SE 와 닿은 비율.
- **PI (polydispersity index)** — 입도 분포 폭 지표 (정의는 원 논문마다 다름).
- **LWM / HDM** — 저에너지 습식 밀링 / 고에너지 건식 밀링.
- **CDC (cascade dissolution coprecipitation)** — 용해 → 연쇄 반응 → 증발 석출 3 단계 액상 합성.
- **HTS (high-temperature shock)** — 탄소천 줄 가열로 초급속 (250 °C s⁻¹) 소성.
- **CCD (critical current density)** — 단락 없이 견디는 최대 전류밀도.
- **홀–페치 · 깁스–톰슨** — 결정립 미세화 → 경도 ↑ (d^−½) · 작은 입자 → 표면 에너지 기여 ↑ (1/r).
- **tortuosity (리뷰 용법)** — 리뷰는 경로 길이 τ · 기하 τ (Lin 1.05–1.30 · Dixit 1.2–1.9) 와 수송 tortuosity factor (τ²) 를 **구분하지 않는다** → 우리 규약 (τ_geo ↔ tau2) 으로 옮길 때 원 논문 정의 확인 필수.

## 5. 결과 (리뷰의 논지 흐름)
1. **서론 (p.1–3)** — 크기는 SE 의 체적 · 계면 물성과 3D 이온/전자 퍼콜레이션 망을 함께 정한다 · 나노 vs 마이크로의 상보적 절충 · 세 실패 모드 (`Fig. 1`) · 예: Wang 의 이중 분포 (서론 표기 = 큰 20 % + 작은 10 % Li₅.₅PS₄.₅Cl₁.₅ 질량 · 4.2.3 절은 반대로 적음 — §9-14) 로 13–40 mA cm⁻² (5–10 C) · > 3 mAh cm⁻² · Singh: 큰 결정립 Li₆PS₅Cl 이 낮은 하중에도 입계 · 입내 파괴 · Zhao: LGPS > 3 µm 분쇄 / 1–3 µm 균열 / < 1 µm 무손상 [2차].
2. **합성 (§2)** — 고상 = 단순 · 저가 · 고 σ 이나 불순물 · 불균일 분포 · 에너지 소비 · 액상 = 정밀 화학량 · 입도 제어 · 저온 · 단시간이나 독성 · 가연 용매 · 후처리 · 비용 · 비전통 = 원료 · 장비 요건 엄격 (§3-1 표).
3. **입자 물성 (§3)** — σ: 너무 작으면 입계 밀도 ↑ = 주 장벽 · 너무 크면 입자 간 틈 → 전극 접촉 ↓ (최적 결정립 크기 존재) · 화학: 작을수록 반응성 ↑ (단, LLZO 는 반대 결과도) · 기계: 작을수록 응력 분산 · 파괴인성 ↑ 이나 입계 강도가 모자라면 솜털형 손상 · 충진: 작을수록 재배열 · 기공 제거 ↑ (단 크기 차가 너무 크면 상 분리 · 고리 기공) · 계면: 작을수록 접촉 ↑ · 곡률 효과로 분리 ↑ 일 수도 (Taghikhani 비단조).
4. **복합양극 (§4.1)** — *"the trade-off between tortuosity (favored by larger particles) and active surface area (enhanced by smaller particles) dictates the overall ionic conductivity"* [리뷰 p.21] · 좁은 PSD 와 미세구조 균일성이 핵심 전략.
5. **다층 (§4.2)** — 층마다 다른 입도 (양극 = 작은 SE · 전해질층 = 큰 SE) · 혼합 크기 촉매전해질 · 이종구조 결정립 — 시험 조건 (스택압 · 온도) 에 따라 결론이 뒤집히는 사례 (Cheng ↔ Sharafi · Peng 의 60 °C).

## 6. Figure set ★ (크롭 9 장 = `figures/lei2026_se_particle_size_effects_review/`)
| Fig | 내용 | 원 출처 (캡션 표기) | 우리 활용 |
|---|---|---|---|
| 1 | *"Partical Size Effects of SEs in ASSBs"* — (a) 높은 tortuosity → 빠른 Li⁺ (b) 접촉 · 기계 실패 → 응력 분산 (c) 공극 → 치밀 계면 · 이상 구성 (작은 · 큰 SE + CAM 원통) | 리뷰 작성 | 개념도 (p1 서론 그림의 문헌판) |
| 2 | 입도 제어 경로: (a) HDM → 높은 tortuosity (b) 탄소 보조 LLZO 소결 (c) LGPS 체가름 (d) LWM → 낮은 tortuosity (e) 공침 Li₃PS₄–Li₂S–LiX (f) 용매 교환 재결정 (g) 제트밀 40 → 2 µm + < 250 °C 후열처리 = S 결핍 (h) Li₂S 전처리 → 원래 · 서브 µm · 나노 LPS (i) 동결건조 | [78] · [94] · [80] · [78] · [95] · [96] · [72] · [74] · [73] | ★ p1 *"입도를 줄이는 경로 = 재료 상태도 바꾼다"* 의 그림 근거 |
| 3 | (a) 밀링 시간 vs 용량 · λ · Li⁺ σ (b) 결정립 크기 vs σ · 확산계수 (10⁻¹⁰–10⁻⁴ m) (c) 결정립 × C-rate 의 이론 에너지 분율 (d) 입도 ↔ 열화 동역학 모식 (e) 큰 · 작은 결정립 ASR (초기 · 공기 24 h) (f) Pristine · Milled · LiTFSI@LPSC CV (g) LLZO 결정립 vs 파괴인성 (h) LGPS 입도 vs 분쇄 · 균열 · 무파괴 | (a) [126] ⚠ · (b, c) [131] · (d) [51] · (e) [135] · (f) [140] · (g) [84] · (h) [62] | ★ p5 — `3a` = *"작을수록 σ ↓ · 용량은 최적점"* 의 대표 그림 (출처 혼선 §9-1) · `3h` = 크기 의존 파쇄 (음극 쪽 반응) |
| 4 | (a) LLZTO D1.2 혼합 분율 × (D90−D10) vs 열린 기공 (b) LPSCl 미세 · 보통 기공도 vs CCD (c) NMC 입자 r_s 0.5 · 1.5 · 3.0 µm 의 Li 농도 · von Mises (d) Li|SG-LPSC · LG-LPSC 전류밀도 (e) **작은 vs 큰 입자 레이더** | (a) [156] · (b) [157] · (c) [166] · (d) [61] · (e) 리뷰 | ★ `4e` = p7 절충 축 요약 · `4b` = 압력 × 입도 (순수 SE 층) |
| 5 | (a, b) 작은 SE 복합 미세구조 · SE 망 (d, e) 큰 SE (c, f) 두께 0–60 µm × 시간 SOC 지도 — 작은 SE 고름 · 큰 SE 기울기 (g) CAM 로딩 × λ 의 θ_CAM (h) 용량 vs σ_ion/σ_el (C/20 · 1 C) (i) S/M/L/XL 50 사이클 (0.214 mA cm⁻²) (j) TGH 전극 단면 (k) TGH vs 일반 전극 100 사이클 | (a, b) [188] · (c–f) [191] · (g, h) [190] ⚠ · (i–k) [193] ⚠ | ★★ p6 (두께 방향 SOC × SE 입도 = Jeong) · p4 (θ · λ) · p7 |
| 6 | (a) 크기 섞인 SE 패킹의 전위 · 전류 모사 (b, c) LLZO SG/LG/SG · LG/SG/LG 이종구조 · 전압 (d–f) 작은 + 큰 LPSCl 혼합 촉매전해질 · C-rate · 온도 (g, h) L/S · S/L 단면 SEM · EDS (i) L/L · S/L · L/S · S/S 율속 | (a) [166] ⚠ · (b, c) [138] · (d–f) [60] · (g–i) [85] | p7 *"다음 = 혼합 · 층별 입도"* 후보 |
| 표 1 | 입도 제어 방법 비교 (11 행) | 리뷰 | §3-1 |
| 표 2 | 압력 × 크기 효과 요약 | 리뷰 | §3-5 · p2 |
| 표 3 ★ | tortuosity 를 줄이는 입도 매개변수 (6 행) | 리뷰 | ★ p4 · p7 점검표 |

## 7. Post-processing (리뷰)
- 새 후처리 없음 — 그림 재사용 · 표 정리.  수치 메타분석 · 단위 통일 · 조건 (압력 · 온도 · 조성) 정규화 **없음** → 서로 다른 조건의 값이 한 문단에 나란히 놓인다 (예: `Table 1` σ 열은 측정 압력 · 온도 미기재).
- **우리 후처리 (이 카드)**: 의심 문장을 렌더로 원문 확인 (단위 빠짐 · 같은 값 반복) · 그림 캡션 출처 ↔ 본문 인용 ↔ 그림 내용 대조 · `Fig. 4b` · `5h` · `6e` · `6i` 판독 · 우리 크기비 λ 계산 · σ 하락 비 모음 (§8-3).

---

## 8. 우리 DEM+MPM 대비 ★ (우리 값의 출처 = `docs/50kg/report_y4/storyline_draft1.md` · `docs/50kg/report_y4/lit_se_size_map_20261030.md`)

### 8-1. 레이더 (`Fig. 4e`) 를 우리 모델 칸으로 나누면
| 리뷰 축 | 리뷰의 크기 방향 | 우리 DEM + 망 (50 kg) | 판정 |
|---|---|---|---|
| 충진 밀도 | 작을수록 ↑ (소결 · 재배열) | 판 고정 공극 D2 **16.74** · D3 **18.96 %** (두 점 · 시드 1) · D0.7 · D1 = 계산 중 | ✓ **계산 가능** — 단 순수 SE 압밀은 *작을수록 덜 치밀* 한 반례가 있다 (faka2026 · 지도 §2) → 리뷰 일반화는 소결 산화물 예가 중심 |
| 계면 적합성 (접촉 · 피복) | 작을수록 ↑ | p3 = AM 구면 기하 캡 합집합 · AM 마다 접촉 수 × 면적 (계산 전) | ✓ 계산 가능 (기하 면적 ≠ 전도 면적 한정어) |
| 퍼콜레이션 · tortuosity | 작을수록 낮은 tortuosity (λ ↑) | p4 = 기하 ↔ 수송 tortuosity 짝 · 협착 몫 (계산 전) | ✓ 계산 가능 — 리뷰 τ 용법은 정의 미구분 |
| 이온전도 (재료) | 클수록 ↑ (입계 · 비정질화) | σ₀ = **입력** (네 입도 공통) · p5 손익분기선 (실측 펠릿 σ 비 5.1/2.3 = 2.217) | ✗ 모델 밖 — 실측 입력으로만 |
| 화학 안정성 | 클수록 ↑ | 없음 | ✗ 범위 밖 |
| 기계 물성 (파괴 · 인성) | 작을수록 ↑ | 강체구 · SE 유효 E 1.35 GPa · 파괴 없음 (Auerbach 진단은 별도) · p6 = 입자 응력 (Love–Weber) | △ 응력 분포까지 (파괴 아님) |
| 응집 (본문 · 초록) | 작을수록 위험 | 단분산 · 응집 없음 | ✗ — otani2025 (응집수 N 1 → 307) 처럼 **이득 상한 쪽** 으로 읽을 것 |
⇒ 우리 4 개 침대는 레이더의 **구조 절반**을 계산한다 · **재료 절반은 입력 또는 범위 밖** — p7 표의 *"계산 / 모형 한계"* 상태 칸에 그대로 옮길 수 있다 [추정 · 권고].

### 8-2. 50 kg 문헌 지도 (`lit_se_size_map_20261030.md` §6 순위 3 *"표준 그림 점검 · 응집 · 부반응 절충 · p1 · p5 · p7"*) 의 점검표 — 지도 §2 의 T1–T15 와 이 리뷰
| T | 표준 그림 · 지표 | 리뷰가 보인 예 | 우리 | 쪽 |
|---|---|---|---|---|
| T1 | PSD · SEM | 체가름 PI · LWM D95 · 제트밀 D50 · `Fig. 2` | ✗ 단분산 입력 — *"D50 하나"* 한계를 리뷰 4.2.1 도 짚음 | p1 |
| T2 | 순수 SE σ vs 입도 | Yamada 2.5 → 0.25 · 제트밀 2.0 → 0.23 · Peng 7.02 → 2.78 · 재결정 1.81 → 1.27–1.54 mS cm⁻¹ · 큰 쪽이 높음 (Schneider 5.7 vs 4.1) · HTS 는 작은 쪽이 높음 (4.2 vs 3.7) | ✗ σ₀ 입력 | p5 |
| T3 | 복합체 기공 · 밀도 | LWM 13.5 vs HDM 22.7 % · Jeong 기공 부피 ↓ | ✓ | p2 |
| T5 | 계면 · 피복 | Lee 94.8 vs 83.1 % · Dixit A_SE/A_AM 1.58 → 4.25 | ✓ (기하) | p3 |
| T6 · T7 | 유효 이온 σ · tortuosity | `Table 3` · LWM *"lower ion transport tortuosity"* · Lin τ 1.05–1.30 | ✓ | p4 |
| T9 | 이용률 · 고립 AM | Shi θ_CAM · Strauss 비활성 CAM 2 → 31 % (CAM 크기) | ✓ 연결성만 (`KG50B-01` 낱말) | p4 |
| T10 | 용량 · 율 | 대부분 예 | ✗ | p7 |
| T11 | λ 축 | Shi `Fig. 5g` · Dixit 3–4 | ✓ (λ 8.57–2) | p1 |
| T12 | 압력 × 입도 | `Table 2` · Lin 100–500 MPa (순수 SE 층) | △ 가압 가지 | p2 |
| T13 | 전류 지도 | Dixit 패킹 모사 · Singh Li 계면 | ✓ | p4 |
| T14 | 공정 손상 (XRD · 결정자) | 제트밀 결정성 ↓ · 재결정 상 분율 · Bonsu 미세변형 | ✗ | p5 |
| T15 | 응력 · 균열 | Zhao · Jiao · Taghikhani · Sharafi | △ 가압 상태 응력 | p6 |
| (새) | **두께 방향 SOC × SE 입도** | **Jeong 2024 (`Fig. 5c · f`)** — 지도 §3 p6 의 *"12 편 중 두께 방향 분포 낸 논문 없음"* 을 메울 원 논문 | ✗ 반응 미계산 | **p6** |

### 8-3. p5 손익분기선과 리뷰의 σ 하락 사례 [우리 산술 — 리뷰 값의 2 차 인용]
| 사례 | 큰 / 작은 σ 비 | 입도 변화 | 공정 |
|---|---|---|---|
| Yamada [80] | 2.5 / 0.25 = **10** | 20 → 1.0 µm | LWM 250 min (비정질화 가설) |
| 제트밀 [72] | 2.0 / 0.23 = **8.7** | 40 µm → D50 1.9 µm | 제트밀 (결정성 ↓) |
| Peng [85] | 7.02 / 2.78 = **2.53** | 결정성 · 습식 vs 건식 | 건식 볼밀 |
| 재결정 [96] | 1.81 / (1.27–1.54) = **1.18–1.43** | 7.91 → 0.88–3.56 µm | 용매 재결정 |
| Schneider [134] | 5.7 / 4.1 = **1.39** | > 50 vs < 50 µm | 체가름 (공정 손상 없음) |
| HTS [112] | 3.7 / 4.2 = **0.88** (작은 쪽이 높음) | 59.4 vs 40.4 nm | 소성 방법 차 |
- 우리 덱의 펠릿 σ 비 **5.1 / 2.3 = 2.217** (3 µm vs 1 µm · 3 차년도 실측, storyline §2 5쪽) 은 이 범위 (0.88–10) 안 · 지도 §3 p5 의 다른 카드 범위 (1.25–2.9) 와도 맞물린다.  ⇒ σ 비는 **공정이 정한다** (같은 *"1 µm"* 라도 0.88–10 배) — 리뷰 자신의 문장 *"cannot be attributed solely to the decrease in particle size"* 가 p5 각주의 문헌 근거.

### 8-4. frame[4] / [5]
- frame[5]: 리뷰 = 재료 · 구조 · 전기화학을 한 서사로 묶은 **2 차 지도** · 우리 DEM 은 구조 → 오믹 수송 칸, MPM 은 형상 소성 칸.  리뷰 전망 (2) *"단일 물리 모사 · 결합 실험 검증 부족"* 은 우리 frame[4] (각 모델을 실험에 따로 맞추고 비교) 의 문제의식과 같다.
- frame[4]: 리뷰 값으로 모델을 맞추지 않는다 (2 차 · 조건 미정규화) — 원 논문 카드를 거친 값만 대조에 쓴다.

## 9. 비판 / 주의 / 한계 ★ (리뷰 자체의 결함 — 인용 전에 꼭 볼 것)
1. **`Fig. 3a` 출처 혼선** — 캡션 = ref [126] (Yadav & Wang, *"Formation of defects in garnet-type LLZO"*, J. Appl. Phys. 2025 — 내용 불일치 · 캡션의 *"© 2022 Wiley-VCH"* 와도 불일치) · 본문 = Yamada [80] 이고 그림을 *"(Fig. 2a)"* 로 잘못 가리킴 · 본문은 재료를 *"glass–ceramic Li₅.₅PS₄.₅Cl₁.₅"* 라 하나 ref [80] 제목은 *"LiCoO₂–Li₁₀GeP₂S₁₂ composite cathodes"* [리뷰 p.10 · p.11 · 참고문헌 대조].  ⇒ 2.5 → 0.25 mS cm⁻¹ 를 인용하려면 원 논문 확인 필수 [미확인].
2. **`Fig. 5i` 출처** — 캡션 *"(i–k) … Ref. [193]"* (Liu TGH) 이나 (i) 는 S/M/L/XL 4 계열 · 0.214 mA cm⁻² 50 사이클 = Schlautmann 의 그림 (정본 카드 §3c: C/10 = 0.214 mA cm⁻²) · 본문도 *"Fig. 5h, i"* 를 Schlautmann 으로 서술 [리뷰 대조 + 판독].
3. **`Fig. 6a` 출처** — 캡션 ref [166] (Taghikhani) · 본문 = Dixit [194] 의 패킹 모사 (그림 내용도 AM 둘레 SE 패킹 · 전위 · 전류) [리뷰 대조].
4. **본문 그림 번호 오류** — *"(Fig. 3e) [51]"* 는 캡션상 (d) 가 [51] · (e) 는 [135] · LLZTO 고리형 기공 *"(Fig. 5b–e)"* 는 복합양극 그림을 가리킴 (해당 그림 없음) [리뷰 p.12 · p.14].
5. **같은 값 반복** — Padarti: *"4.30 × 10⁻⁶ S cm⁻¹ for 900 °C vs. 4.30 × 10⁻⁶ S cm⁻¹ for 1000 °C"* 인데 *"distinct ionic conductivities"* · Peng: *"L-SE, 60 µm, 7.02 mS cm⁻¹, −25 °C … S-SE … 1 µm, 7.02 mS cm⁻¹, −25 °C"* (앞 절은 7.02 vs 2.78 · *"−25 °C"* 는 25 °C 로 보임) [리뷰 p.10 · p.25 — 렌더 확인].
6. **단위 빠짐** — Horii: *"grain size (from 0.1 to 0.1 mm)"* · *"from 10 to 10 μm"* (그림 축 = 10⁻¹⁰–10⁻⁴ m → 0.1 nm–0.1 mm · 10 nm–10 µm 로 읽힘) [리뷰 p.10 — 렌더 확인].
7. **저자 이름 · 정의** — ref [172] (Park, J.H. et al.) 를 본문은 *"Yoon Chung et al."* 로 · König [78] 의 *"lower ion transport tortuosity … (ε_SE = 0.237 for LWM)"* 는 부피분율을 tortuosity 처럼 적음 · 깁스–톰슨 식의 r 을 *"particle diameter"* 로 · `Table 3` 4 열 머리가 3 열과 같은 글자 [리뷰 p.6 · p.12 · p.20 · p.22].
8. **그림 축 오기** — `Fig. 5g` 세로축 눈금 *"60 · 70 · 80 · 80"* (맨 위 = 90 이어야 간격이 맞음) · 단위 *"(%)vol"* 인데 Shi 의 f_CAM 은 질량 기준 정의 · `Fig. 1` *"Partical"* · `Fig. 3h` *"Weather fractured"* · *"Partical size"* [판독].
9. **`Table 1` 혼합** — 입자 크기와 결정자 크기를 한 열에 · σ 측정 조건 (압력 · 온도) 없음 · 공침 행 (LPSC 5 µm · 5.71 mS cm⁻¹) 은 본문 서술에 없는 값.
10. **일반화의 반례가 빠짐** — *"smaller particles … higher packing densities"* 는 소결 산화물 · 고압 LPSCl 층 예 중심 · 냉간 압밀 순수 LPSCl 에서 작을수록 덜 치밀한 결과 (faka2026 카드) · 응집하면 이득이 준다는 DEM 결과 (otani2025 카드) 는 다루지 않음 [교차 카드].
11. **SE 입도가 아닌 예가 SE 절에** — Strauss · Jiang · Liu TGH 는 **CAM 입도** · TGH 는 도전재 · 바인더 슬러리 전극.
12. **tortuosity 정의 미구분** (§4-1) — 기하 τ · 수송 τ² 를 같은 낱말로.
13. **2 차 인용의 한계** — 이 카드의 모든 수치는 리뷰가 옮긴 값이다 · 우리 정본 카드가 있는 원 논문 (Schlautmann · Shi · Schneider · Faka · Minnmann · Bielefeld) 은 **그 카드 값**을 쓰고, 없는 것 (Jeong 2024 · Lee 2025 Joule · Dixit 2021 · Wang 2024 · Peng 2023 · König 2023 · Lin 2024 · Strauss 2018) 은 카드를 만든 뒤 쓴다 (정본 grep: 이들은 다른 카드의 참고문헌 줄에만 있음).  Calpa 2019 (ref [52]) 는 같은 묶음 (10-30 스테이징) 카드 `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` 가 있다.
14. **같은 연구의 조성이 두 곳에서 반대** — Wang [60] 혼합 촉매전해질: 서론 p.2 *"20% large and 10% small"* ↔ 4.2.3 절 p.24 *"20% small … and 10% large"* [리뷰 대조].

## 10. 적용 인사이트
1. **p1 서론 한 줄** — *"SE 를 작게 만드는 경로 (볼밀 · 습식 밀링 · 제트밀 · 재결정 · 액상 · HTS) 는 입도와 함께 결정성 · 불순물 · 응집 · 분포 폭을 바꾼다 (Lei 2026 리뷰) — 이 보고의 단분산 대리 입도는 그중 '크기' 만 떼어 본 비교다."*
2. **p5 각주** — 같은 *"작은 SE"* 라도 펠릿 σ 하락은 공정에 따라 0.88–10 배 (§8-3 · 2 차 인용) → 손익분기선 2.217 은 3 차년도 실측 한 쌍의 값이며 *"입계 증가"* 로 설명하지 않는다 (리뷰 문장 + ou2026 카드의 입계 몫이 작다는 계산과 같은 결).
3. **p7 표의 "문헌 방향" 열** — 레이더 다섯 축 (§8-1) 을 그대로 행으로 쓰고, 우리 칸은 *"구조 = 계산 · 재료 = 입력 / 범위 밖"* 으로 상태를 적는다.
4. **다음 정본 카드 후보 (우선순위)** — ① **Jeong 2024** (*Adv. Energy Mater.* 14, 2304544 · SE < 1 vs 3–5 µm × 두께 방향 SOC · EDXRD + 단층 + 모델) = p6 의 입도 쪽 원 논문 · stavola2023 과 짝 ② **Lee 2025 Joule** (9, 102046 · SE 1.4 vs 4.9 µm → 피복 94.8 vs 83.1 % · 탈착) = p3 ③ **Dixit 2021** (*Energy Storage Mater.* 40, 239 · A_SE/A_AM · λ 3–4) = p3 · p4 ④ **Wang 2024** (*Adv. Mater.* 36, 2309306 · 혼합 크기) · **Peng 2023** (*Energy Environ. Mater.* 6, e12308 · 층별) = p7 다음 단계 (서지는 리뷰 참고문헌 표기 그대로 · 원문 미확인).
5. **λ 위치** — 우리 λ 8.57 · 6 · 3 · 2 는 Dixit 의 최고 충진 λ ≈3–4 를 D2 (λ 3) 가 끼고 D3 (λ 2) 는 아래 · Shi 지도 (85 wt%) 에서는 모두 낮은 θ 영역 (지도 §1 shi2019 행) [우리 산술 · 2 차 대조].

## 11. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A 2026 review summarizes the particle-size effect of solid electrolytes as a trade-off: finer particles raise packing density, contact area and mechanical robustness but increase side reactions, agglomeration and grain-boundary density, whereas coarser particles retain higher ionic conductivity but hinder densification and percolation with cathode active materials (Lei et al., *Electrochem. Energy Rev.* 2026)."
- "The same review notes that the conductivity loss of milled argyrodite electrolytes cannot be attributed solely to the smaller particle size, because amorphization, impurities and decomposition introduced during milling contribute as well."
- 국문: *"SE 미립화는 충진 · 접촉 · 기계 강도를 올리지만 부반응 · 응집 · 입계를 늘리고, 미립화 공정 자체가 σ 를 깎을 수 있다 (Lei 2026 리뷰 · 수치는 원 논문 확인 후)."*

## 12. 참고문헌 — 우리가 더 볼 것 (리뷰 목록 서지 그대로 + 이유)
| 번호 | 서지 (리뷰 표기) | 왜 |
|---|---|---|
| 191 | Jeong, M.G., Naik, K.G., Zheng, Y.J., et al.: Operando investigation on the role of densification and chemo-mechanics on solid-state cathodes. Adv. Energy Mater. 14, 2304544 (2024) | ★★ SE 입도 × 두께 방향 SOC (p6) |
| 192 | Lee, D., Shim, Y., Choi, E., et al.: Alleviating kinetical delamination induced by localized cathode contact via electrochemomechanical modeling in all-solid-state batteries. Joule 9, 102046 (2025) | ★ 피복 ↔ 탈착 (p3) |
| 194 | Dixit, M.B., Parejiya, A., Muralidharan, N., et al.: Understanding implications of cathode architecture on energy density of solid-state batteries. Energy Storage Mater. 40, 239–249 (2021) | SE 패킹 · A_SE/A_AM · λ 3–4 |
| 60 | Wang, Y.C., Li, X.: Fast kinetics design for solid-state battery device. Adv. Mater. 36, 2309306 (2024) | 혼합 크기 촉매전해질 |
| 85 | Peng, L.F., Yu, C., Zhang, Z.Q., et al.: Tuning solid interfaces via varying electrolyte distributions enables high-performance solid-state batteries. Energy Environ. Mater. 6, e12308 (2023) | 층별 입도 · σ 2.78 vs 7.02 |
| 78 | König, C., Miß, V., Janin, L., et al.: Mitigating the ion transport tortuosity in composite cathodes of all-solid-state batteries by wet milling of the solid electrolyte particles. ACS Appl. Energy Mater. 6, 9356–9362 (2023) | LWM 공극 13.5 vs 22.7 % |
| 72 | Kim, Y.S., Jeon, S.H., Cho, W., et al.: Surficial sulfur loss of jet-milled Li6PS5Cl powder under mild-temperature heat treatment. ACS Appl. Energy Mater. 5, 15442–15451 (2022) | 제트밀 σ 손실 (p5) |
| 80 | Yamada, Y., Watanabe, K., Kim, H.S., et al.: Microstructure control of LiCoO2-Li10GeP2S12 composite cathodes by adjusting the particle size distribution for the enhancement of all-solid-state batteries. Batteries Supercaps 6, e202300261 (2023) | `Fig. 3a` 출처 확인 |
| 157 | Lin, L., Ayyaswamy, A., Zheng, Y.J., et al.: Nonintuitive role of solid electrolyte porosity on failure. ACS Energy Lett. 9, 2387–2393 (2024) | 입도 × 압력 × 기공 구조 |
| 52 | Calpa, M., Rosero-Navarro, N.C., Miura, A., et al.: Electrochemical performance of bulk-type all-solid-state batteries using small-sized Li7P3S11 solid electrolyte prepared by liquid phase as the ionic conductor in the composite cathode. Electrochim. Acta 296, 473–480 (2019) | 밀링 손상 없는 미립화 (지도 §6 순위 7) — 같은 묶음 카드 `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` |
| 47 | Rajagopal, R., Subramanian, Y., Ryu, K.S.: Improving the electrochemical performance of cathode composites using different sized solid electrolytes for all solid-state Lithium batteries. RSC Adv. 11, 32981–32987 (2021) | 지도 §4 웹 후보와 같은 논문 |
| 168 | Cheng, G.Z., Sun, H., Wang, H.R., et al.: Efficient ion percolating network for high-performance all-solid-state cathodes. Adv. Mater. 36, 2312927 (2024) | 이온 퍼콜레이션 망 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-30)
- 34 쪽 텍스트 층 (`pdftotext`) 전수 · 본문 1–26 쪽 정독 · 참고문헌은 본문에서 쓴 번호 (60 · 62 · 72–74 · 78–80 · 84–85 · 96 · 108 · 110 · 112 · 126 · 131 · 133–135 · 140 · 156–158 · 166 · 172 · 184–194 · 207–210) 를 대조.
- 렌더 확인: p.10 Horii 단위 빠짐 · p.25 Peng *"7.02 … −25 °C"* 반복 (텍스트 층 추출 오류가 아니라 원문 인쇄).
- 크롭 9 장 = 그림 6 (각 쪽 임베드 래스터 1 장 bbox) + 표 3 (캡션 ~ 표 끝 · `Table 3` 은 가로 쪽을 −90° 회전 · 쪽 아래 Springer 로고를 피해 다시 자름) · 200 dpi `pdftoppm` → PIL · 전부 열람.
- 정본 litdb 확인: 같은 DOI · 제목 카드 없음 (coordinator 사전 확인) · §12 · §9-13 의 원 논문들은 정본 `git grep` 에서 다른 카드의 참고문헌 줄에만 나옴 (Jeong 2024 → li2026 리뷰 카드 · Lee 2025 Joule → lee2026 PTFE 카드 · König 2023 → wolf2026 · Lin 2024 → thompson2026 · Strauss 2018 → hippauf2019 · kawaguchi2023 · Calpa 2019 → park2020).

## 🔗 관련 카드
- SE 입도 (복합양극): `schlautmann2023_se_particle_size_composite_transport` · `shi2019_high_am_loading_particle_size_assb` · `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2024_microstructure_porosity_visualization` · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `bazzoun2026_dem_fem_rnm_ionic` · `tailored_cathode_microstructure_low_pressure_assb` · `otani2025_dem_se_dispersion_aggregation_compression` · `park2020_dimension_controlled_se_percolation_contact_area` · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage`.
- SE 입도 (순수 SE · 공정): `faka2026_particle_size_consolidation_strain_lpscl` · `schneider2023_particle_size_pressure_transport` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `ou2026_microstructural_multiscale_fast_ion_transport`.
- tortuosity 정의: `bielefeld2019_microstructural_modeling_composite_cathode` · `bielefeld2020_effective_ionic_conductivity_binder` · `tjaden2018_tortuosity_review_calculation_approaches` · `landesfeind2016_tortuosity_eis_electrodes_separators`.
- 같은 주제 태그 (size_effect): `kawaguchi2026_se_size_soc_dependent_cathode_resistance` · `stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity`.
- 같은 묶음 (10-30 스테이징 · 다른 에이전트 · 제목만 확인): `yano2026_se_psd_width_ionic_tortuosity_dem` (LPSCl PSD 폭 × 이온 tortuosity · DEM — 지도 §6 순위 1 의 Ohsaki 그룹) · `lin2025_submicron_lpscl_cathode_li_kinetics` (서브 µm LPSCl 양극 — 순위 2) · `yadav2021_lpscl_sieved_psd_impedance_tortuosity` (체 분급 LPSCl 임피던스 — 순위 4) · `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` (리뷰 ref [52] — 순위 7) · `tron2023_rational_cathode_composite_optimization_lpscl` (순위 8).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
