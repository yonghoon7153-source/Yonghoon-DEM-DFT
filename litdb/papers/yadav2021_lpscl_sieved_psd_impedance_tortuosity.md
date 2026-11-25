# 체 분급한 Li₆PS₅Cl (Ampcera 0.5–150 µm → <20 · 20–50 · 50–150 µm) 의 입도 등급이 순수 SE 이온 전도 · 복합양극 유효 이온 전도 · 전도도 기반 tortuosity · Li 금속 반쪽셀에 미치는 영향 — 임피던스 연구 — Yadav · Davoisne · Morcrette (교신) (2021 International Workshop on Impedance Spectroscopy (IWIS), IEEE, pp. 40–43)

> slug `yadav2021_lpscl_sieved_psd_impedance_tortuosity` · DOI `10.1109/IWIS54661.2021.9711800` · type `experiment (체 분급 LPSCl · SS 차단전극 EIS · Li|SE|복합양극|SE|Li 대칭셀 EIS (Warburg short) · Li 금속 반쪽셀 · SEM · 시뮬레이션 없음)` · PDF `efa42c8a-4._Impact_of_sulfide-based_solid_electrolyte_particle_size_distribution_on_the_electrochemistry_of_ASSB_via_impedance_study.pdf` (학회 논문 4 쪽 · SI 없음 · IEEE Xplore 판) · digested `2026-10-30` · status ✅
> topic: size_effect (SE 입도 효과)
> elements: Li, P, S, Cl, Ni, Co, Mn, O, C
> methods: sieving, EIS (ion-blocking pellet · electron-blocking symmetric cell), SEM cross-section, galvanostatic cycling
> HAL `hal-03696977` — 조정자 지시 · 문헌 지도 §4 링크 기준 (이 PDF 는 IEEE Xplore 판이라 HAL 번호가 인쇄돼 있지 않다)

<!-- 실독 기록 (2026-10-30)
     4 쪽 전부 200 dpi 렌더 + 내장 래스터 원본 (pdfimages) 로 읽고 pdftotext 로 인용문 대조.  그림 1–5 · 표 1 은 전부 래스터
     (그림 3 · 4 의 아래 표도 그림 안 래스터) → 표 값은 그림 안 글자를 읽었다 (흐림 없음 · "~" 표지까지 그대로).
     그림 5 전압 곡선 · 그림 3 · 4 Nyquist 는 눈 판독 (±5 mAh/g · ±20 Ω 급) → litdb/figures/<slug>/digitized.csv.
     표지: [인쇄] = 본문 · 그림 안 표 · 식 · [판독] = 그림에서 읽은 값 · [우리 산술] · [미확인] · [가정].
     쪽 = 학회 논문집 쪽 40–43 (PDF 1–4 쪽).  PDF 머리 = "Authorized licensed use limited to: Hanyang University. Downloaded on
     October 30,2026" (IEEE Xplore 판).
     크롭 6 장 = 그림 1–5 + 표 1 (캡션 뺀 영역) · 전부 열어 확인.
     중복 확인: 정본 litdb/papers/ 전수 (454 장) 에 DOI · "9711800" · "IWIS" · "hal-03696977" · 제목 낱말 grep → 카드 없음.
     저자 이름은 PDF 에 "성 이름" 순 ("Yadav Neelam Ghanshyam" · "Davoisne Carine" · "Morcrette Mathieu*") — 전자우편
     neelam.yadav@ · carine.davoisne@ · mathieu.morcrette@ 로 성 = Yadav · Davoisne · Morcrette 판단. -->

## 0. 이 digest 를 읽는 법 — 우리 질문과 원문 판정

**계기 (2026-10-30)**: 50kg 4차년도 보고의 문헌 지도 (`docs/50kg/report_y4/lit_se_size_map_20261030.md`) §6 순위 4 — *"LPSCl 에서 큰 PSD 가 이긴 반례 (p5 · p7)"*.

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 "큰 SE 가 이긴 반례" 맞나** | **맞다 (방향)** — 큰 등급 (50–150 µm) 이 순수 SE σ (**0.396 → 1.46 mS/cm, 3.7 배**) · 복합양극 σ (**2.16 × 10⁻⁵ → 1.12 × 10⁻⁴ S/cm, 5.2 배**) · τ (**2.48 → 1.98**) · 셀 (compC 사이클 ↔ compA **첫 충전 중 단락**) 에서 앞선다.  ⚠ 크기 척도가 우리 (0.7–3 µm) 보다 1–2 자릿수 크고 · CAM 입도 미기재 · 셀 한 개씩 · compA 실패는 단락 | 그림 3 · 4 · 표 1 · 그림 5 |
| **Q2 밀링 없는 σ(d) (p5)** | 체 분급이라 **밀링 손상 교란은 없다** — 대신 **치밀도와 교란**: 3 t 펠릿 compacity **83.2 → 84.4 → 89.2 %**.  ★ 그림 3 판독상 크기 차는 **고주파 끝이 아니라 큰 호 (입자 간 · 입계)** 에서 난다 (<20 µm 고주파 끝 ≈ 405 Ω·cm 로 오히려 낮음) | 그림 3 표 · [판독] |
| **Q3 구조 (f) vs 물성 (σ₀) 분리 (p5 형식)** | ★ 복합체 σ 이득 C/A **5.19 배 = 펠릿 σ_SE 3.69 배 × 구조 f 1.41 배** · B/A **2.91 = 3.01 × 0.97** [우리 산술] → **로그 기준 이득의 ≈ 79 % 가 펠릿 σ 차**, 구조 몫은 50–150 µm 등급에서만 나타난다 | 그림 3 · 4 표 |
| **Q4 tortuosity 수치 (p4)** | 그들 τ_cond = √(ε·σ_SE/σ_cc) = 우리 *tau* · τ² = **6.15 · 5.95 · 3.92** (우리 *수송 tortuosity* 쪽).  ⚠ 식 (4) 로 역산한 ε = **0.336 · 0.315 · 0.301** — 치밀도가 오르는데 SE 부피분율이 내려간다 (반대 방향) → **한 규칙으로 재현 불가** · 우리 규약 (φ = 고체 분율 × compacity, 밀도 가정) 으로는 **4.9 · 5.5 · 4.0** (A < B 순서 뒤집힘) | 표 1 · §3f |
| **Q5 단분산 가정 — 지지 / 반론?** | **해당 없음 (방향 반례 칸에만)** — 넓은 체 등급 (특히 <20 µm 는 0.5 µm 미분 포함) 을 비교했지 폭을 바꾸지 않았고, 크기가 ≥ 20 µm 급 · 탄소 5 wt% 포함 · NMC111.  우리 D 축 (0.7–3 µm · λ 2–8.57) 의 검정이 아니다 | §7c |

⇒ **분류 한 줄**: *같은 LPSCl 원료를 체로 나눈 크기 등급 (<20 · 20–50 · 50–150 µm) 비교 — "큰 SE 가 순수 SE · 복합양극 이온 전도 · tortuosity · 셀에서 이긴다" 는 반례 쪽이며, 크기 척도가 우리보다 1–2 자릿수 크고 단일 시료 · 단락 셀 · 재현 안 되는 τ 로 정량 근거는 약하다 (방향 자료).*

---

## 1. 한 줄 요약

Ampcera Li₆PS₅Cl (0.5–150 µm) 를 체로 **<20 µm · 20–50 µm · 50–150 µm** 로 나누고, 각 등급으로 **NMC111 66.5 · SE 28.5 · C45 2.5 · VGCF 2.5 wt%** 복합양극 (compA · B · C) 을 만들었다.
순수 SE 펠릿 (3 t) 은 **큰 등급일수록 치밀하고 (compacity 83 → 89 %) σ 가 높다 (0.40 → 1.46 mS/cm)**.  Li|SE|복합양극|SE|Li 대칭셀 EIS (저주파 Warburg short 적합 · SEM 두께) 로 얻은 복합양극 유효 σ 도 **2.2 × 10⁻⁵ → 1.1 × 10⁻⁴ S/cm** 로 큰 SE 쪽이 높고, 전도도 기반 tortuosity τ 는 **2.48 · 2.44 · 1.98** — 큰 SE 가 가장 낮다.
50–150 µm 분리막 · Li 금속 반쪽셀에서 compC 는 C/50 표기 사이클을 돌았고 compA 는 첫 충전 중 **단락**했다.
저자 결론: *큰 SE 는 같은 압력에서 더 치밀 · 전도성 → "포화 압력" 이 낮고 (추론) · 복합양극 τ 를 낮춰 성능을 높인다 · 다만 입도를 키우는 효과에는 한계 (평탄) 가 있을 것.*

## 2. 메타 / 동기 / 질문

| 저자 | 학회/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Neelam Ghanshyam Yadav** · Carine Davoisne · **Mathieu Morcrette\*** (Laboratoire de Réactivité et Chimie des Solides (LRCS), CNRS UMR 7314, Université de Picardie Jules Verne, 33 rue Saint Leu, 80039 Amiens Cedex, France) · \* 교신 (mathieu.morcrette@u-picardie.fr) | **2021 International Workshop on Impedance Spectroscopy (IWIS)** · IEEE · pp. 40–43 · 978-1-6654-9472-4/21/$31.00 ©2021 IEEE · 학회 장소 · 날짜 [미확인] | 10.1109/IWIS54661.2021.9711800 | **Li₆PS₅Cl (Ampcera, 0.5–150 µm → 체 분급 3 등급)** · **NMC111** (입도 [미확인]) · 탄소 **C45 2.5 + VGCF 2.5 wt%** · 바인더 없음 [인쇄된 조성에 없음] | 실험만 (체 분급 · EIS · SEM · 정전류 사이클) |

- **키워드 (p.40)**: Sulfide based SE · All-solid-state batteries · Impedance spectroscopy · particle size · porosity · tortuosity · effective ionic conductive · pressure · charge transfer resistance · interfacial resistance etc.
- **동기 (p.40)**: 황화물 SE 는 냉간 성형 · 높은 σ 가 장점이지만 *"young's modulus reported up to 20 GPa"* [1 = Sakuda 2013] 인데도 균열이 잘 난다 [2] · 균열 · 전파는 **기공**과 엮이고 기공 (compacity) 은 *"morphology and size of individual particles and their distribution"* 에 좌우된다 [5] · 성능 제한 인자에 합의가 없다 (이온 전도 [12] ↔ CAM–SE 전하이동 [8]) → SE 입도 · 분포가 SE 분리막 σ · 복합양극 유효 σ · 사이클에 미치는 영향을 본다.
- **같은 원료**: *"To avoid changes in the source of ArgCl (argyrodite-Li6PS5Cl), we took an ArgCl from Ampcera which had particles ranging from 0.5-150µm and sieved it"* (p.40–41) — 합성 · 밀링 없이 **체 분급만**으로 크기를 나눴다.
- **감사의 글**: UPJV · 프랑스 교육부 (박사 과제) 지원 (p.43).  이해관계 서술 없음.

---

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · 조성 (그림 1 · p.40–41)

| 항목 | 값 | 표기 · 출처 |
|---|---|---|
| SE 원료 | Argyrodite Li₆PS₅Cl (*"ArgCl"*), **Ampcera**, **0.5–150 µm** | [인쇄] 그림 1 · p.41 |
| 체 분급 | **<20 µm → compA · 20–50 µm → compB · 50–150 µm → compC** | [인쇄] 그림 1 |
| 체 방법 (체 규격 · 분위기 · 시간) · 각 등급의 실측 PSD · SEM | [미확인] (등급 경계만) | — |
| 복합양극 조성 | **NMC111 66.5 % + SE 28.5 % + C45 2.5 % + VGCF 2.5 % (wt%)** | [인쇄] 그림 1 아래 줄 |
| 혼합 방법 · NMC111 입도 · 코팅 | [미확인] (그림 2.2 모식은 *"Secondary NMC particles"*) | — |
| 분리막 (전지) | **50–150 µm 등급 고정** (*"keeping the SE with large particles constant"*) | [인쇄] p.42 |
| SE 고체 기준 부피분율 | ≈ **0.48** (NMC 4.75 · LPSCl 1.87 · 탄소 1.8–2.1 g/cm³ 가정 → 0.476–0.482) | [우리 산술 · 가정] |

### 3b. 순수 SE 펠릿 — 그림 3 아래 표 (SS 차단전극 · 3 t · 30 MHz–1 Hz) ★

| SE 등급 | Compacity 3T\* (%) | σ_SE (S/cm) | 기공 (%) | 1/σ (Ω·cm) | 출처 |
|---|---|---|---|---|---|
| **<20 µm** | **~83.24** | **~3.96 × 10⁻⁴** | 16.8 | 2525 | [인쇄] · [우리 산술] |
| **20–50 µm** | **~84.39** | **~1.19 × 10⁻³** | 15.6 | 840 | |
| **50–150 µm** | **~89.21** | **~1.46 × 10⁻³** | 10.8 | 685 | |

- 본문 (p.41): *"SE with a large particle size ranging from 50-150µm have the highest ionic conductivity (1.46 × 10⁻³ S·cm⁻¹), while the particles <20um have the lowest value (3.96 × 10⁻⁴ S·cm⁻¹)."* · *"a similar trend can be highlighted between the compacity and ionic conductivity in SE."*
- 비 (큰/작은) σ **3.69** · 20–50/<20 **3.01** [우리 산술].
- 성형: *"The pellets were pressed at 3T each"* (p.41) · 금형 지름 미기재 → 전지와 같은 ⌀10 mm 면 **≈ 375 MPa** [우리 산술 · 가정] (1 t ≈ 125 MPa).
- **compacity** = 정의 · 측정법 미기재 (프랑스어 *compacité* = 충전율 · 상대밀도로 읽음) · *"3T\*"* 의 별표 설명 없음 [미확인].
- ★ **그림 3 Nyquist (저항률 축 · 원 래스터 735 px 에서 눈금 0 · 500 · 1000 Ω·cm 로 보정한 판독)**: 50–150 µm 파랑 = ≈ 580 Ω·cm 에서 시작하는 작은 호가 ≈ 700 에서 차단 스파이크로 · 20–50 µm 초록 = ≈ 630 → ≈ 850–900 · <20 µm 빨강 = ≈ **405 Ω·cm 에서 시작해 큰 호로 그림 밖 (> 1 kΩ·cm)** [판독].  보고 σ 의 역수 (685 · 840 · 2525 Ω·cm) 는 **호 끝 (스파이크 시작)** 과 맞는다 → σ_SE = 펠릿 **전체** (호 포함) 저항으로 계산 — 그림 2.1 의 식 *σ_SE = d / (R_SE-Bulk·A)* 와 이름이 어긋난다 (§10-3).  ⇒ **작은 등급의 손해는 고주파 끝 (입자 내부) 이 아니라 호 (입자 간 접촉 · 입계) 에서 난다** [판독 · 해석 추정].

### 3c. 복합양극 — 그림 4 아래 표 (Li|SE|comp|SE|Li · 3T\*) ★

| Comp | Compacity 3T\* (%) | σ_cathode comp (S/cm) | 기공 (%) | f = σ_cc/σ_SE | 출처 |
|---|---|---|---|---|---|
| **compA** (<20 µm) | **~55.44** | **~2.16 × 10⁻⁵** | 44.6 | **0.0545** | [인쇄] · [우리 산술] |
| **compB** (20–50 µm) | **~60.95** | **~6.29 × 10⁻⁵** | 39.0 | **0.0529** | |
| **compC** (50–150 µm) | **~64.05** | **~1.12 × 10⁻⁴** | 36.0 | **0.0767** | |

- 비 C/A **5.19** = σ_SE 비 **3.69** × f 비 **1.41** · B/A **2.91** = **3.01** × **0.97** [우리 산술] ⇒ **A ↔ B 는 구조 (f) 가 같고 차이는 전부 펠릿 σ** · 구조 이득은 C 에서만 (+41 %).  C/A 이득의 **로그 몫 79 %** 가 펠릿 σ [우리 산술].
- 그림 4 Nyquist [판독]: 세 셀 모두 고주파 시작 ≈ 30 Ω (3e7 Hz 표지) · compA = 고주파 호 ≈ 30–255 Ω 뒤 **큰 저주파 호가 ≈ 595 Ω (1 Hz) 까지** · compB = ≈ 365 Ω 까지 · compC = 고주파 호 ≈ 30–200 Ω 뒤 작은 꼬리 ≈ 255 Ω.  주파수 표지 3e7 · 3e5 · 3e3 · 1 Hz.
- 두께 d = SEM 단면에서 (값 미기재) · 적합 매개변수 미기재 [미확인].

### 3d. 표 1 — 전도도 기반 tortuosity (p.42)

| σ_SE (S/cm) | σ_cathode comp (S/cm) | **τ** (인쇄) | τ² | 식 (4) 역산 ε = τ²·σ_cc/σ_SE | 출처 |
|---|---|---|---|---|---|
| ~3.96 × 10⁻⁴ | 2.16 × 10⁻⁵ | **2.48** | 6.15 | 0.336 | [인쇄] · [우리 산술] |
| ~1.19 × 10⁻³ | 6.29 × 10⁻⁵ | **2.44** | 5.95 | 0.315 | |
| 1.46 × 10⁻³ | 1.12 × 10⁻⁴ | **1.98** | 3.92 | 0.301 | |

- 본문 (p.42): *"The tortuosity values in the cathode composite, range from 1.9-2.5. The lowest value of tortuosity is exhibited by compC"* · 초록: *"1.9 being the lowest for large particles"* (표는 1.98).
- ⚠ 역산 ε 가 compacity 와 **반대로** 내려간다 (0.336 → 0.301 ↔ compacity 55 → 64 %).  ε 를 상수로 두면 τ 상대값은 1 : 1.016 : 0.843 (표 1 : 0.984 : 0.798) · ε ∝ compacity 면 1 : 1.065 : 0.906 — **어느 규칙으로도 표 1 이 재현되지 않는다** [우리 산술].
- **우리 규약 tau2 = φ_SE·σ₀/σ_eff** (φ_SE = 고체 분율 0.48 × compacity · σ₀ = 각 등급 펠릿 σ_SE) = **4.9 · 5.5 · 4.0** · tau = 2.2 · 2.35 · 2.0 [우리 산술 · 밀도 가정 — 탄소 1.8–2.1 에서 ±0.05] → **A 와 B 의 순서가 뒤집힌다**.

### 3e. 전지 (그림 5 · Li 금속 · 50–150 µm 분리막 · 토크 9.7 Nm) [판독]

| 셀 | 사이클 (그림 표기) | 충전 끝 | 방전 끝 (Q−Q0) | 방전 용량 | 비고 |
|---|---|---|---|---|---|
| **compA** | 1st cycle | ≈ 3.85 V · ≈ 80–85 mAh/g 에서 | — | — | **"Short circuit"** — 전압이 ≈ 1.3 V 로 떨어진 뒤 ≈ 0.75 V 로 ≈ 320 mAh/g 까지 |
| **compC** | 1st cycle_C/50 | 4.3 V · ≈ 152 mAh/g | ≈ 48 mAh/g (≈ 2.3 V) | **≈ 104 mAh/g** | 첫 쿨롱효율 ≈ 68 % [우리 산술] |
| **compC** | 165th cycle_C/50 | 4.3 V · ≈ 67 mAh/g | ≈ 9 mAh/g | **≈ 58 mAh/g** | 첫 방전의 ≈ 56 % [우리 산술] |

- 전압 창 · 율 · 온도 · 사이클 프로토콜 [미확인] — 165 사이클을 전부 C/50 으로 돌리면 ≈ 16,500 h (≈ 1.9 년) [우리 산술] → 중간 율이 따로 있었을 것 [추정].
- compB 셀 · 반복 셀 없음.

### 3f. 우리 산술 정리

| 양 | 값 | 식 / 입력 |
|---|---|---|
| 3 t · 1 t 압력 (⌀10 mm) | **374.6 · 124.9 MPa** | 질량 × 9.80665 / (π · 0.5² cm²) |
| 펠릿 σ 비 (큰/작은) | 3.69 | 1.46 / 0.396 mS/cm |
| 복합체 σ 비 C/A | 5.19 = 3.69 × 1.41 | σ_SE 비 × f 비 |
| 복합체 σ 비 B/A | 2.91 = 3.01 × 0.97 | |
| SE 고체 부피분율 | 0.476–0.482 | NMC 4.75 · LPSCl 1.87 (정본 schlautmann2023 Table S1 · faka2026 Table S5) · 탄소 1.8–2.1 (가정) |
| 우리 규약 tau2 (A · B · C) | 4.9 · 5.5 · 4.0 | φ_SE / f |
| 그들 τ² (A · B · C) | 6.15 · 5.95 · 3.92 | 표 1 τ 제곱 |
| 순수 SE 기공 (A · B · C 등급) | 16.8 · 15.6 · 10.8 % | 100 − compacity |
| 복합체 기공 | 44.6 · 39.0 · 36.0 % | 100 − compacity |

---

## 4. 재료 & 방법 ★

### 4a. 체 분급 (§II-A, p.40–41)
- 같은 Ampcera 원료 (0.5–150 µm) → 체로 3 등급.  임피던스가 *"the morphology and size of the particles, the pores and porosity"* 에 민감하므로 원료를 바꾸지 않으려고 체 분급을 택했다 (p.40–41).
- 체 규격 · 분위기 (글러브박스 여부) · 등급별 수율 · 등급 안 PSD [미확인].

### 4b. 순수 SE 이온 전도 (그림 2.1 · §II-B · p.41)
- **이온 차단 (SS | SE | SS)** · 그림 2.1 식: **R_Total = R₀ + R_SE-Bulk + R_SE-GB** · **σ_SE = d / (R_SE-Bulk · A)**.
- *"The pellets were pressed at 3T each"* · EIS **30 MHz–1 Hz** (모든 측정 공통, p.41) · 펠릿 질량 · 두께 · 지름 · 온도 [미확인].

### 4c. 복합양극 유효 이온 전도 (그림 2.2 · §II-B · §III · p.41–42)
- **대칭셀 Li | SE | 복합양극 | SE | Li** (그림 4 범례 *"Li-SE-compX-SE-Li"*) — SE 층이 전자를 막는다.
- 식 (1): **R_Total = R₀ + 2R_SE + R_interfaces + R_cathode.comp**.
- *"At low frequencies, the electrons in the cathode composite are blocked by the SE layers and Li concentrations are formed in the composite, which gives effective ionic resistance in cathode composite. Hence the R_cathode.comp, can be fitted with Warburg short-type impedance."* (p.42)
- **두께 d = SEM 단면 영상** → **σ_cathode comp = d / (R_cathode.comp · A)** (그림 2.2).
- 성형 *"fixed at 3T\*, to be comparable with the pressure used to fabricate the battery"* (p.41).
- 적합 회로 전체 · 매개변수 · d 값 [미확인].

### 4d. tortuosity 정의 (p.42)
- 식 (2) 이상 (굴곡 없음): **σ_cathode.comp = σ_SE · ∈** (∈ = SE 부피분율).
- 식 (3) *"In simple terms"*: **τ = actual path travelled / minimum physical distance between two points** (기하 정의).
- 식 (4) (번호 칸 *"()"* 로 인쇄): **τ²_cond = (σ_SE / σ_cathode.comp) · ∈** — 그림 2 의 화살표 상자도 같은 식 (*"∈ = Volume fraction of SE"*).  인용 [10] = Hlushkou 2018.
- ⇒ 식 (3) (기하) 와 식 (4) (전도도) 를 같은 τ 로 부른다 — 우리 규약으로는 식 (4) 의 τ²_cond = *수송 tortuosity (tau2)* · τ_cond = *tau* · 식 (3) = *τ_geo* (§13).
- ∈ 값 · 산출 방식 (기공 포함 여부) [미확인] — 역산값 §3d.

### 4e. 전지 조립 (§II-C, p.41)
- SE 분말 **80 mg** (50–150 µm 등급) → **⌀10 mm PMMA 틀**에서 **1 t · ≈ 1 min** → 복합양극 **10 mg** 넣고 **3 t · ≈ 3 min** 동시 성형 → **Li 포일 0.75 mm** 손 압착 → 토크 렌치 **9.7 Nm** 로 *"constant stack pressure"* (압력 환산값 [미확인]).

### 4f. 입자 처리 (우리 "무질서 처리" 칸)
- **시뮬레이션 없음.**  입자는 실물 (각진 · 판상 LPSCl — 그림 5 분리막 SEM) · 크기 등급은 체 경계로만 정의.
- 우리 쪽 대응: 단분산 구 (D50 하나) — 이 논문의 등급은 **폭이 넓은 분포** (특히 <20 µm 는 0.5–20 µm) 라 우리 대리 입도와 같은 종류의 변수가 아니다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 그림 1 — 분급 · 조성 모식
- 검은 상자 *"Argyrodite (Ampcera)(0.5-150µm)"* → 빨강 <20 µm (compA) · 초록 20–50 µm (compB) · 파랑 50–150 µm (compC).  아래 줄 = 조성 (NMC111 66.5 · SE 28.5 · C45 2.5 · VGCF 2.5 wt%).

### 5.2 그림 2 — 측정 셀 · 식
- 2.1: SS 사이 노란 SE 펠릿 · Li⁺ 화살표 (차단) · R_Total 식 · σ_SE 식.
- 2.2: Li 사이 *"Cathode comp"* — 노란 SE · 검은 C · 파란 *"Secondary NMC particles"* · R_Total 식 · σ_cathode comp 식.
- 아래 상자: τ²_cond = (σ_SE/σ_cathode.comp)·∈ · *"∈ = Volume fraction of SE"*.

### 5.3 그림 3 — 순수 SE EIS (저항률 축 Ω·cm)
- §3b 표 · 판독.  큰 등급일수록 **호가 작고 스파이크가 일찍** 선다 = 입자 간 저항이 작다 [판독 해석].

### 5.4 그림 4 — 복합양극 대칭셀 EIS
- §3c 표 · 판독.  compA 의 **큰 저주파 호 (≈ 255 → 595 Ω)** 가 R_cathode.comp 쪽 신호로 보인다 [판독 해석 — 저자는 호 배정을 그림에 표시하지 않음].

### 5.5 표 1 — tortuosity
- §3d.  저자 해석 (p.42): *"Higher τ means, higher transport issues, and consequently higher ohmic losses. The lower cutoff voltage is then reached faster and one would then observe a lower capacity while lower τ can decrease the electrolyte resistance, which reduces ohmic drop and is also good for capacity enhancement."*

### 5.6 그림 5 — 전지 · SEM
- 위: 복합양극 단면 SEM (compA · compC) + 분리막 (50–150 µm) SEM (두 패널 같은 영상으로 보임 [판독]) + Li.  compA 는 회색 작은 SE 사이에 흰 NMC 덩어리가 고르게 · **compC 는 큰 회색 SE 영역과 흰 NMC 덩어리 · 어두운 균열선이 보인다** [판독] — 저자는 균열을 논하지 않는다.  눈금 50 µm.
- 아래: compA 첫 충전 중 단락 · compC 1st / 165th (§3e).
- 저자 (p.42): *"comp C with the large particle in the composite outperforms comp A with small particles. One of the plausible explanation for this behaviour could be the differences in tortuosity in the cathode composite since other parameters such as SE separator, Li metal anode, cell assembly, cell configuration, cycling conditions and stack pressure of 9.7 Nm, etc are constant."*

### 5.7 결론 (§IV, p.42–43, 인쇄 요지)
1. *"the effective ionic conductivity even in the bulk of SE, varies with the particle size of SE. Larger SE particles exhibit higher ionic conductivity than smaller ones."*
2. *"The size of SE impacts the saturation pressure Hence for large SE particles, a higher effective ionic conductivity is reached even with a lower fabrication pressure"* — 복합양극은 AM 보호 때문에 압력을 무한정 못 올리므로 중요.
3. *"Large SE particles can also provide good effective ionic conductivity in the cathode composite, by lowering the tortuosity and improving the solid-state battery performances"*.
4. *"we agree that there should be a limit to increasing the SE particle size, beyond which the impact on increasing ionic conductivity reaches a plateau."*

---

## 6. 우선 질문 — 원문 대조

### Q1. "포화 압력이 낮다" 는 측정인가?
- **아니다.** 압력 계열 측정이 없다 — 3 t 한 점의 compacity · σ 에서 *"it could be deduced that the saturation pressure … will be lower"* (p.41) 라고 **추론**했다.  초록의 *"Consequently, the saturation pressure … is lower for large particle size"* 는 측정 결과처럼 읽히지만 근거는 단일 압력이다.

### Q2. 큰 등급의 σ 이득은 입자 내부인가 입자 간인가?
- 그림 3 판독으로는 **입자 간 (호) 쪽** — <20 µm 의 고주파 끝 (≈ 405 Ω·cm) 은 오히려 큰 등급 (≈ 580 · 630) 보다 낮고, 큰 호가 전체 저항을 키운다 [판독 · 고주파 한계 30 MHz 라 입자 내부 호가 다 보이는지는 미확인].
- 이 해석이 맞다면 펠릿 σ(d) 차이는 **같은 입도 축에서 접촉 수 · 접촉 저항 차**이고, 우리 접촉망 (Holm 협착) 이 따로 계산하는 양과 겹친다 (§7c · §11-②).

### Q3. 복합체 이득은 구조인가 물성인가?
- §3c: **A → B 는 f 가 같다 (0.0545 ↔ 0.0529)** — 복합체 σ 2.9 배 차는 펠릿 σ 3.0 배 차가 그대로 넘어온 것.  **B → C 에서만 f 가 1.45 배** (0.0529 → 0.0767).  ⇒ *"큰 SE 가 복합체 tortuosity 를 낮춘다"* 는 C 등급에서만 성립하고, 그것도 compacity (61.0 → 64.1 %) 증가와 함께다.

### Q4. 셀 비교는 tortuosity 를 시험했나?
- **아니다.** compA 는 **첫 충전 중 단락** (≈ 80–85 mAh/g) — 분리막 (두 셀 공통 50–150 µm) 을 지나는 Li 침투 같은 **분리막 · 음극 쪽 실패**로 보이며 [추정], 옴 손실로 하한 전압에 일찍 닿는 τ 효과의 모양이 아니다.  셀 한 개씩 · compB 없음 · 반복 없음.

---

## 7. 우리 DEM+MPM 대비 ★ (우리 쪽 근거 = `docs/50kg/report_y4/storyline_draft1.md` · 문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` · CLAUDE.md)

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 (50kg 4차년도) | 같음 / 다름 · 이유 |
|---|---|---|---|
| SE | Li₆PS₅Cl (Ampcera) 체 분급 3 등급 (<20 · 20–50 · 50–150 µm) | LPSCl D50 0.7 · 1 · 2 · 3 µm 단분산 대리 | **크기 척도 1–2 자릿수 다름** · 등급 = 넓은 분포 |
| CAM | NMC111 · 입도 [미확인] | NCM D6 µm 단일 | λ 계산 불가 · 그림 5 판독상 compB · C 는 SE ≳ CAM (λ < 1) 쪽일 가능성 [추정] — 우리 λ 2–8.57 밖 |
| 조성 | NMC 66.5 · SE 28.5 · 탄소 5 wt% | AM 85 wt% · SE 15 wt% · 탄소 없음 | SE · 탄소 몫이 다르다 |
| 압력 | 3 t (⌀10 mm 면 ≈ 375 MPa [가정]) · 셀 토크 9.7 Nm | 목표 300 MPa · 판 고정 이완 (끝 D2 279.8 · D3 291.4 MPa) | 단일 압력끼리 |
| 기공 | 순수 SE 10.8–16.8 % · **복합체 36–45 %** | 판 고정 D2 16.74 · D3 18.96 % (storyline §3) | 그들 복합체 기공이 매우 크다 (측정법 미상) → 수치 비교 금지 |
| 순수 SE σ(d) | 0.40 → 1.46 mS/cm (작은 → 큰 등급 · 체 분급) | σ₀ = 입력 (공통 σ₀ 의 f(d) 가 p5 의 틀) | p5 손익분기선의 *물성 쪽* 자료 (밀링 없는 사례) |
| 수송 지표 | τ_cond (√), τ² 6.15 · 5.95 · 3.92 (ε 불명) | f · tau2 (φ = 전극 부피 기준) | 우리 규약 재계산 4.9 · 5.5 · 4.0 [밀도 가정] |
| 기하 τ | 식 (3) 정의만 · 계산 없음 | 최단 경로 / 두께 | 비교 불가 |
| 시뮬레이션 | 없음 | DEM + 접촉망 | — |
| 전지 | compC 사이클 · compA 단락 | 없음 | — |

### 7b. 문헌 지도 (`lit_se_size_map_20261030`) 에서의 자리 — 보고서 쪽별

| 쪽 | 이 논문이 주는 것 | 쓸 때의 한정어 |
|---|---|---|
| **p2** 공간 점유 · 압밀 | 큰 SE 등급 → **순수 SE 펠릿 · 복합체 둘 다 치밀** (89 vs 83 % · 64 vs 55 %) — 순수 SE 방향은 faka2026 (작을수록 덜 치밀) 과 같고, **복합체 방향은 schlautmann2023 (작을수록 치밀) 과 반대** | 크기 ≥ 20 µm 급 · 복합체 기공 36–45 % (측정법 미상) · λ 미상 |
| **p4** 이온 망 | τ² (= 수송 tortuosity 쪽) 3.9–6.2 · 우리 규약 재계산 4.0–5.5 — 지도 T7 칸 수치 하나 더 | ε 규칙 재현 불가 (§3d) |
| **p5** 구조 vs 물성 | ★ **밀링 없는 σ(d)** — 체 분급 펠릿 σ 비 **3.69** (50–150 ↔ <20 µm) · 복합체 이득의 분해 **5.19 = 3.69 (펠릿) × 1.41 (구조 f)** = p5 손익분기선과 **같은 형식의 실측 분해** — 이 사례에선 펠릿 σ 가 이득의 대부분 (로그 79 %) | 펠릿 σ 차가 입자 간 호에서 나면 (§6 Q2) 우리 f(d) 와 곱할 때 **이중계상** 위험 (§11-②) |
| **p7** 관측 경향 · 다음 | *"문헌 방향 (카드)"* 열의 **반례**: *"큰 SE 등급 (20–150 µm) 이 순수 SE σ · 복합체 σ · τ · 셀에서 이김 (Yadav 2021 · 체 분급 · 크기 척도 다름 · 단락 셀)"* — 지도 §2 의 *"단서 · 반례"* 목록에 추가 | 우리 D 범위 (0.7–3 µm) 의 방향을 검정하지 않음 |
| p1 · p3 · p6 | 직접 기여 없음 | — |

### 7c. 단분산 가정 — 지지인가 반론인가
- **해당 없음.**  이 논문의 변수는 *체 등급* (위치 이동 + 폭 다름) 이지 *같은 D50 에서 폭* 이 아니다.  등급 크기는 ≥ 20 µm 급 (compA 만 0.5–20 µm 의 넓은 미분 포함) 이라 우리 0.7–3 µm 대리 입도와 겹치지 않는다.
- 쓸 수 있는 것은 **방향 반례** 하나: *"SE 가 CAM 보다 클 수도 있는 큰 크기 영역에서는 큰 SE 가 이길 수 있다."*  지도 §0-4 의 *"실험 다수는 SE ≳ CAM 영역"* 과 같은 줄에 놓인다.
- 다만 **§6 Q2 의 관찰** (작은 등급 펠릿의 손해 = 입자 간 호) 은 우리 모델 해석에 직접 쓸모가 있다 — 단분산이든 아니든 우리 접촉망은 **입자 간 접촉 저항을 이미 계산**하므로, 펠릿 σ(d) 를 입력 σ₀ 로 바꿔 끼우는 시나리오 (p5) 에서 같은 기전을 두 번 세지 않는지 확인해야 한다.

### 7d. frame [4] / [5]
- **frame [5]**: 순수 실험 — 수송 (EIS) · 충전 (compacity) 만 있고 구조 해석 (접촉 · 경로 · 형상) 이 없다.  우리 DEM (접촉망 · 협착) · MPM (형상 소성) 이 줄 수 있는 칸 = *"큰 SE 가 왜 복합체 f 를 올리는가 (C 등급에서만)"* 의 기전.
- **frame [4]**: 모델이 없으니 교차검증 대상이 아니라 **실험 앵커 후보** — 그러나 크기 척도 · 조성 (탄소 5 wt%) · 단일 시료 때문에 우리 침대의 직접 앵커로는 쓰지 않는다.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 체 분급 모식 (<20 · 20–50 · 50–150 µm → compA · B · C) + 조성 줄 (NMC111 66.5 · SE 28.5 · C45 2.5 · VGCF 2.5 wt%) | 시료 정의 |
| 2 | (2.1) SS\|SE\|SS 차단 셀 · R_Total = R₀ + R_SE-Bulk + R_SE-GB · σ_SE = d/(R_SE-Bulk·A) (2.2) Li\|SE\|comp\|SE\|Li · R_Total = R₀ + 2R_SE + R_interfaces + R_cathode.comp · σ = d/(R·A) + τ²_cond 식 | ★ 복합체 이온 σ 측정 셀 설계 (전자 차단 SE 층) |
| 3 | 순수 SE Nyquist (저항률 Ω·cm, <20 · 20–50 · 50–150 µm) + 표 (compacity 83.24 · 84.39 · 89.21 · σ 3.96 × 10⁻⁴ · 1.19 × 10⁻³ · 1.46 × 10⁻³ S/cm) | ★ 밀링 없는 σ(d) · 손해 = 입자 간 호 (판독) |
| 4 | 복합양극 대칭셀 Nyquist (3e7 · 3e5 · 3e3 · 1 Hz 표지) + 표 (compacity 55.44 · 60.95 · 64.05 · σ 2.16 × 10⁻⁵ · 6.29 × 10⁻⁵ · 1.12 × 10⁻⁴ S/cm) | ★ 복합체 σ = 펠릿 σ × 구조 f 분해 (§3c) |
| 5 | 전지 모식 + SEM (compA · compC 단면 · 50–150 µm 분리막) + 전압 곡선 (compA 단락 · compC 1st / 165th C/50) | 셀 비교의 한계 (단락) · compC 균열선 |
| 표 1 | σ_SE · σ_cathode comp · τ (2.48 · 2.44 · 1.98) | τ² = 수송 tortuosity 쪽 · ε 재현 불가 |

## 9. Post-processing ★
- **순수 SE**: EIS (30 MHz–1 Hz) → 저항 (스파이크 시작 = 전체로 보임) → σ = d/(R·A) · compacity (방법 미기재).
- **복합체**: 대칭셀 EIS → 저주파 Warburg short 적합 → R_cathode.comp · SEM 단면 두께 d → σ = d/(R·A).
- **τ**: 식 (4) τ²_cond = (σ_SE/σ_cc)·∈ → τ (∈ 미기재).
- **전지**: 정전류 충방전 곡선 (Q−Q0 축) 두 장.
- **안 한 것**: 등급별 PSD · BET · SEM · 압력 계열 · 반복 · 오차 · 적합 매개변수 · 용량 표.
- **우리 후처리 (이 카드)**: 압력 환산 · σ 비 분해 (펠릿 × f) · 역산 ε · 우리 규약 tau2 · 그림 3 · 4 · 5 판독.

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **"포화 압력이 낮다" 는 추론** — 압력 계열 없음 (§6 Q1).  초록 문장은 측정처럼 읽힌다.
2. **크기 등급 = 다른 분포 + 다른 치밀도** — 크기 효과와 compacity (83 → 89 %) 가 함께 움직인다 · <20 µm 등급은 0.5 µm 미분까지 포함 · 등급별 표면적 · 수분 · 표면 불순물 (미분은 반응 면적이 크다) 미측정.
3. **σ_SE 의 저항 정의 불일치** — 그림 2.1 식은 R_SE-Bulk 만 쓰는데, 보고값의 역수는 그림 3 의 **호 끝 (전체)** 과 맞는다 [판독].  *"effective ionic conductivity even in the bulk of SE"* (결론) 도 실제로는 펠릿 전체 σ.
4. **표 1 τ 가 식 (4) 로 재현되지 않는다** — 역산 ε 0.336 → 0.301 (compacity 와 반대 방향) · 상수 · 비례 규칙 모두 불일치 (§3d).  τ 순서 A > B 는 우리 규약 (밀도 가정) 에선 뒤집힌다.
5. **식 (3) (기하) 와 식 (4) (전도도) 를 같은 τ 로 부름** — 우리 규약에서 식 (4) 는 수송 tortuosity (τ² 쪽), 식 (3) 은 기하 τ.  *"Tortuosity (depends on the porosity)"* 라 적어 기공 효과도 τ 에 섞는다.
6. **복합체 compacity 55–64 % (기공 36–45 %) 가 매우 낮다** — 같은 압력 급의 복합양극 문헌 (schlautmann2023 375 MPa 기공 14–24 %) 보다 두 배 · 측정법 (SEM 두께 + 질량?) 미기재 · 10 mg 층의 SEM 두께 오차 가능 [추정] → 절대값 인용 금지.
7. **셀 비교 무효** — compA 는 첫 충전 단락 (분리막 · Li 쪽 실패로 보임 [추정]) · 셀 한 개씩 · compB 없음 · 반복 없음.  *"outperforms … plausible explanation … tortuosity"* 는 근거 부족.
8. **사이클 프로토콜 미기재** — *"165th cycle_C/50"* 를 전부 C/50 로 돌리면 ≈ 1.9 년 [우리 산술] · 전압 창 · 온도 [미확인].
9. **CAM 입도 · 혼합법 · 탄소 분산 미기재** → λ = D_CAM/D_SE 를 알 수 없다 — 문헌 지도의 핵심 축 (λ) 위에 놓을 수 없다.
10. **그림 5 의 분리막 SEM 두 패널이 같은 영상**으로 보인다 (모식 용도) [판독] · compC 단면의 균열선은 논의되지 않음.
11. **학회 4 쪽 · SI 없음** — 체 분급 · 측정 · 적합 세부가 대부분 빠졌다.  수치 표에 *"~"* 표지 (근사) — 유효숫자 신뢰 불가.
12. **탄소 5 wt% 포함** — 우리 50kg 침대 (NCM + SE 두 상 · 탄소 없음) 와 다르고, 전자 경로는 문제가 아니다 (그들 σ_e 미측정).

## 11. 적용 인사이트
- ① **p7 반례 칸 문구 (제안)**: *"SE 가 CAM 보다 클 수 있는 수십 µm 영역에서는 체 분급한 큰 LPSCl 이 순수 SE σ (3.7 배) · 복합양극 σ (5.2 배) · 치밀도에서 앞선 보고가 있다 (Yadav 2021 · 단일 시료 · 단락 셀) — 우리 0.7–3 µm 범위의 방향을 검정하지 않는다."*
- ② ★ **p5 이중계상 경고**: 이 논문의 그림 3 은 작은 등급 펠릿의 σ 손해가 **입자 간 호 (접촉 · 입계)** 에서 난다고 시사한다 [판독].  p5 의 *"공통 σ₀ 의 f(d) × 실측 펠릿 σ(d)"* 시나리오에서, 펠릿 σ(d) 가 이미 **입도에 따른 접촉 저항**을 담고 있고 우리 f(d) 도 **접촉 협착**을 담으므로 둘을 곱하면 같은 기전을 두 번 셀 수 있다 — CLAUDE.md CL-81 · CL-91 의 *"펠릿값 σ₀ 와 명시 구조의 부분 이중계상"* 과 같은 부류.  storyline p5 가 이미 그 곱을 *"조건부 시나리오 (표로만)"* 로 묶어 둔 것과 맞는 근거 (⬜ 문구 반영 = 1저자).
- ③ **복합체 σ 분해의 실측 사례** — σ_cc 비 = σ_SE 비 × f 비 (5.19 = 3.69 × 1.41).  p5 의 손익분기 논리를 문헌 데이터로 한 번 돌려 볼 수 있는 표본 (그들은 큰 쪽이 물성 · 구조 둘 다 이김).
- ④ **측정 셀 설계 참고** — 복합체 이온 σ 를 Li\|SE\|comp\|SE\|Li 대칭셀 + 저주파 Warburg short 로 뽑는 방식 (전자 차단 = SE 층).  Minnmann 2021 · Schlautmann 2023 의 In/LiIn 대칭셀 TLM 과 같은 계열.
- ⑤ **분말 쪽 교훈** — 같은 원료를 체로 나누면 밀링 손상 교란은 없지만 미분 · 표면 · 치밀도 교란이 남는다.  우리 쪽 실측 분말 (3차년도 · 4차년도 SE) 의 σ(d) 를 해석할 때 *"밀링 손상 vs 입자 간 접촉"* 을 EIS 호 분리로 가를 수 있는지 확인할 가치가 있다 (실측 쪽 결정 = 1저자).

## 12. 인용 가능 문장 (영문 초안)
- *"Sieving a single Li₆PS₅Cl batch (0.5–150 µm) into <20, 20–50 and 50–150 µm fractions gave pellet ionic conductivities of about 0.40, 1.19 and 1.46 mS cm⁻¹ at the same pressing load, together with increasing pellet compacity (≈83 → 89 %) [Yadav 2021]."*
- *"In NMC111-based composites with 28.5 wt% of these fractions (plus 5 wt% carbon), the effective ionic conductivity increased from 2.2 × 10⁻⁵ to 1.1 × 10⁻⁴ S cm⁻¹ from the finest to the coarsest fraction, and the conductivity-derived tortuosity decreased from 2.48 to 1.98 [Yadav 2021]."* (⚠ 단일 시료 · ε 미기재 — 각주)
- 국문: *"체 분급한 같은 LPSCl 에서 큰 등급이 순수 SE · 복합양극 이온 전도 모두 높았지만, 복합체 이득의 대부분은 펠릿 σ 차가 그대로 넘어온 것이고 구조 (f) 이득은 50–150 µm 등급에서만 보였다 (Yadav 2021 표값의 우리 산술)."*

## 13. 기법 용어 미니사전
- **체 분급 (sieving)**: 체 눈 크기로 분말을 등급으로 나누는 것 — 밀링 없이 크기를 바꾼다 · 각 등급은 여전히 분포를 가진다.
- **compacity (compacité)**: 충전율 = 상대밀도 (이 논문은 정의 미기재).
- **이온 차단 셀 (SS\|SE\|SS)**: 금속 전극이 Li⁺ 를 막아 저주파에 스파이크 — 그 앞 저항이 펠릿 이온 저항.
- **전자 차단 대칭셀 (Li\|SE\|comp\|SE\|Li)**: SE 층이 전자를 막고 Li 가 이온을 주고받는다 → 복합체의 이온 저항을 본다.
- **Warburg short (유한 길이 · 투과형)**: 유한 두께 층의 확산 · 전송선 응답을 나타내는 요소 — 저주파에서 실축 저항으로 닫힌다.
- **τ_cond (이 논문)**: √((σ_SE/σ_cc)·∈) = 우리 *tau* (√ 값) · 그 제곱 = 우리 *수송 tortuosity (tau2)* · 식 (3) 의 경로 길이 비 = 우리 *τ_geo* (기하).
- **포화 압력 (saturation pressure)**: 저자 정의 = 최고 이온 전도도에 닿는 압력 (이 논문은 측정 안 함).
- **C45 · VGCF**: 카본블랙 (Super C45 계열 이름) · 기상성장 탄소섬유 — 전자 도전재.

## 14. 참고문헌 — 원문 목록 (서지 그대로) · 정본 카드

| 번호 | 서지 (원문 목록) | 정본 카드 · 왜 |
|---|---|---|
| 1 | Sakuda, A., Hayashi, A. & Tatsumisago, M. Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery. Sci. Rep. 3, 2–6 (2013). | `sakuda2013_sulfide_mechanical_property` |
| 2 | Lewis, J. A. et al. Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography. Nat. Mater. c, (2021). | 카드 없음 (권호 인쇄 깨짐 "c") |
| 3 | Simon, F. J., Hanauer, M., Henss, A., Richter, F. H. & Janek, J. Properties of the Interphase Formed between Argyrodite-Type Li6PS5Cl and Polymer-Based PEO10:LiTFSI. ACS Appl. Mater. Interfaces 11, 42186–42196 (2019). | 카드 없음 |
| 4 | Luo, S. et al. A high energy and power all-solid-state lithium battery enabled by modified sulfide electrolyte film. J. Power Sources 485, 229325 (2021). | 카드 없음 (`luo2022_…` · `luo2026_…` 은 다른 논문) |
| 5 | Kodama, M. et al. High-pressure in situ X-ray computed tomography and numerical simulation of sulfide solid electrolyte. J. Power Sources 462, 228160 (2020). | 카드 없음 — 입도 · 치밀화 (faka2026 ref 12 와 같은 논문) |
| 6 | Bielefeld, A., Weber, D. A. & Janek, J. Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries. ACS Appl. Mater. Interfaces 12, 12821–12833 (2020). | `bielefeld2020_effective_ionic_conductivity_binder` |
| 7 | Shi, T. et al. High Active Material Loading in All-Solid-State Battery Electrode via Particle Size Optimization. Adv. Energy Mater. 10, (2020). | `shi2019_high_am_loading_particle_size_assb` |
| 8 | Kroll, M. et al. Sheet-type all-solid-state batteries with sulfidic electrolytes: Analysis of kinetic limitations based on a cathode morphology study. J. Power Sources 505, 230064 (2021). | 카드 없음 |
| 9 | Landesfeind, J., Hattendorff, J., Ehrl, A., Wall, W. A. & Gasteiger, H. A. Tortuosity Determination of Battery Electrodes and Separators by Impedance Spectroscopy. J. Electrochem. Soc. 163, A1373–A1387 (2016). | `landesfeind2016_tortuosity_eis_electrodes_separators` |
| 10 | Hlushkou, D. et al. The influence of void space on ion transport in a composite cathode for all-solid-state batteries. J. Power Sources 396, 363–370 (2018). | `hlushkou2018_void_space_ion_transport_assb_cathode` (τ 계산 인용처) |
| 11 | Thorat, I. V. et al. Quantifying tortuosity in porous Li-ion battery materials. J. Power Sources 188, 592–600 (2009). | `thorat2009_quantifying_tortuosity_porous_liion` |
| 12 | Schichtel, P. et al. On the impedance and phase transition of thin film all-solid-state batteries based on the Li4Ti5O12 system. J. Power Sources 360, 593–604 (2017). | 카드 없음 |

## 🔗 관련 카드
- 같은 축 · 반대 방향 짝: `schlautmann2023_se_particle_size_composite_transport` (복합체 작을수록 이득 · λ < 1) · `yano2026_se_psd_width_ionic_tortuosity_dem` (같은 날 digest · PSD 폭 · DEM).
- 순수 SE 입도 · 치밀화: `faka2026_particle_size_consolidation_strain_lpscl` (큰 PSD 가 더 치밀 · 같은 방향) · `schneider2023_particle_size_pressure_transport` · `cronau2022_wet_milling_particle_size_ionic_conductivity` (밀링 교란 쪽 대조).
- 복합체 이온 σ 측정 · tortuosity: `minnmann2021_jes_charge_transport_bottlenecks` · `landesfeind2016_tortuosity_eis_electrodes_separators` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `bielefeld2020_effective_ionic_conductivity_binder`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
