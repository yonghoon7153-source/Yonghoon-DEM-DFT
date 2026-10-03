<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     τ 묶음 형식 기준 = kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md · siroma2015_transmission_line_model_porous_electrode_impedance.md ·
     froboese2019_microstructure_ionic_conductivity_assb_electrode.md (같은 날 앞 묶음 카드).
     이 논문은 실험 논문이다 (EIS 시간 추적 · XPS · ToF-SIMS · SEM · 갈바노) — 시뮬레이션이 없고, τ 를 정의하지도 쓰지도 않는다.
     이 카드의 1차 목적 = park2020_digitaltwin_assb_foundational 의 SI Table S1 각주 b ("literature[18a-c]") 중 [18b] 를 원문으로 대조하는 것.
     쪽 표기: 본문 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 p.(22966 + n)  (PDF 1 = p.22967 … PDF 10 = p.22976).
     SI = 별도 PDF 10 쪽 ("20. Sup) Understanding the effects of chemical reactions … .pdf") — 인쇄 쪽 번호가 없다 → "SI p.n" = SI PDF 쪽.
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 값 (≈ · 추세 전용, 정밀 인용 불가) / 파생 = 카드 작성자 계산 (식 명시 · 원문에 없는 값). -->
# 황화물 ASSB 양극–전해질 계면의 "화학" 반응만 떼어 보기 — SOC 0 숙성 40 h 를 ee-연결 (이온 차단) TLM 으로 추적해 bulk · 입계 저항 분리 · Ni-rich NCM + argyrodite 1:1 v/v (295 MPa · 탄소 없음) · 베어 vs LiNbO₃ 코팅 · 입계 이온 저항 +389 Ω vs +21 Ω · 반응 산물 NiS · Li₂S · LiPₓClᵧ · LiCl · 접촉 손실 — Jung (J. Mater. Chem. A 2019)

> slug `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` · DOI `10.1039/c9ta08517c` · type `exp (EIS impedance 시간 추적 + ee-연결 TLM 적합 · XPS · ToF-SIMS · SEM · 갈바노 — 시뮬레이션 없음; 황화물 ASSB 양극 복합체의 SOC 0 계면 화학 숙성)` · PDF `20. Understanding the effects of chemical reactions at the cathode–electrolyte interface in sulfide based all-solid-state batteries.pdf` · digested `2026-10-03` · status ✅
>
> ★ **이 카드가 닫는 것 (원문 판정)** — Park 2020 디지털트윈 SI Table S1 각주 b 가 [18a–c] 로 인용한 두 값, NCM 전자 σ **8.5×10⁻⁴ S cm⁻¹** 와 LPSCl 이온 σ **−4.45×10⁻³·ε_s + 4.64×10⁻³ S cm⁻¹** 는
> **이 논문 ([18b]) 에 없다** (본문 10 쪽 · SI 10 쪽 전수, 렌더 + 텍스트 검색).  argyrodite · NCM 어느 쪽의 σ 값도, 부피분율 의존 식도 없고,
> 논문 전체에서 S cm⁻¹ 단위 수치는 **LiNbO₃ 10⁻¹¹ S cm⁻¹ (p.22970, ref 27 인용값) 하나**뿐이다.  보고되는 것은 **복합체 (1:1 v/v) TLM 적합 저항 (Ω)** 이다 (SI Table S1–S2).
> ⇒ [18a] (카드 기준) · [18b] (이 카드) · [18c] (Froboese 카드) **셋 다 해당 값 없음** → Park σ₀ 출처는 계속 `[미확인]` · Park 역산 tau2 = "추세 전용" 유지 (§8).
> τ 쪽: 이 논문은 τ 를 정의하지 않는다.  쓰인 TLM 식은 Siroma 2015 표 3 **T형 "open–open"** (단자 레일 = 전자 · 앞계수 Z_e²) 과 같은 꼴 = **관통형** 연결이다 (τ_e 계열 아님).
> 원 저항을 σ 로 바꾸면 복합체 **σ_eff 까지** (파생) 이고, σ₀ (순수 SE) · 기공률이 없어 f · tau2 는 n/a.
>
> 형제 카드: `siroma2015_transmission_line_model_porous_electrode_impedance` (= 이 논문 ref 23 · TLM 해의 원전) · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (= ref 25 · ASSB TLM τ) ·
> `xiao2019_cathode_coating_screening` (= ref 15 · LiNbO₃ 계면 DFT) · `zhu2015_esw_grand_potential_origin` (= ref 10) · `rao2011_argyrodite_se_studies_bvse` (= ref 17).
> 역링크: `park2020_digitaltwin_assb_foundational` (참고문헌 [18] b · Table S1 각주 b "literature[18a-c]") · `froboese2019_microstructure_ionic_conductivity_assb_electrode` §8 (f) ("[18b] 미대조" 기록 → 이 카드로 해소).

---

## 0. 결론 먼저 (질문 → 답 → 근거)

| 질문 | 답 | 근거 (쪽) |
|---|---|---|
| Park 2020 의 NCM σ 8.5×10⁻⁴ S cm⁻¹ 가 여기 있나 | **없다.**  NCM 의 전자 σ 값이 아예 없다 ("electronic pathway is mainly affected by NCM" 라는 정성 문장뿐) | 본문 p.22967–22976 · SI p.1–10 전수 |
| Park 의 LPSCl σ(ε_s) 직선식이 여기 있나 | **없다.**  유일한 식 = Methods 의 ee-연결 TLM 임피던스 식 (번호 없음).  측정 조성이 **1:1 v/v 하나**라 ε_s 직선 (계수 2 개) 을 만들 데이터도 없다 | p.22974 · p.22968–22969 |
| 이 논문이 주는 σ 는 고유인가 유효인가 | σ 를 **하나도 적지 않는다** (LiNbO₃ 인용값 제외).  SI 저항을 σ = T/(R·A) 로 바꾸면 전부 **복합체 유효값** (1:1 · 295 MPa · 25 °C · 계면 포함) — 파생 | SI Table S1–S2 (SI p.7–8) |
| 복합체 유효 이온 σ (파생) | t = 0: **0.080 (베어) · 0.101 (LiNbO₃) mS cm⁻¹** → 40.6 h: 0.033 (−59 %) · 0.092 (−9 %) | §3-4 |
| "반응 산물이 입계 이온 전도를 줄인다" 의 정량 | 40 h 뒤 증가 (stated, Fig 2j): 입계 이온 **389 Ω (베어) vs 21 Ω (LiNbO₃)** · 입계 전자 234 vs 99 · bulk 이온 41 vs 3.5 · bulk 전자 43 vs 3.3 Ω — SI 표 차로 소수점까지 재현 | p.22971 · Fig 2(j) · SI p.7–8 |
| 입계 몫 | t = 0 이온 저항의 **91 % (베어) · 93 % (LiNbO₃)** 가 입계 성분 (R_tot/R_bulk 11.0 · 13.8, 파생) — CPE α 0.41–0.54 의 **등가회로 분해비** | SI p.7–8 · §3-4 |
| 접촉 손실 | 40 h 뒤 베어만 균열 · 접촉 손실 (SEM Fig 1e–h) · 입계 C 감소 (C_i 2.45 → 0.62 ×10⁻⁷ F) · 무가압 in situ SEM 5 일 균열 (베어만 — 코팅 대조 없음) | p.22968 · p.22971 · SI p.4 |
| τ 정의 | **없다** ("tortuos" 0 건).  TLM = Siroma T형 open–open (관통형) — τ_e 계열 아님 | p.22974 ↔ siroma2015 카드 표 3 |
| σ₀ 기준 | **없다** — 순수 SE 펠릿 미측정 · SE σ 미보고 | 전수 |
| 결정 4 · 메모 v2 §3-4 | 권고 **불변**.  Park σ₀ = 인용 [18a–c] 어디에도 없는 모형 입력 → "추세 전용" 유지 + 한정어 보강 제안 | §8 |

## 1. 한 줄 요약
삼성 SAIT 그룹이 **Ni-rich NCM + argyrodite (Mitsui) 1:1 v/v, 탄소 없는 펠릿** (295 MPa · 2 min · 320 µm) 을 SUS 이온 차단 전극 사이에 끼우고 **SOC 0 에서 40.6 h 숙성**시키며 EIS 를 반복 측정해,
**ee-연결 전송선 모델 (TLM)** 로 이온 · 전자 경로 각각의 bulk · 입계 저항을 떼어 **전기화학 사이클 없는 화학 반응만의 효과**를 봤다.  베어 NCM 은 입계 이온 저항이 274 → 663 Ω (+389) 로 늘고 입계 용량이 줄었으며 (균열 · 접촉 손실 해석),
XPS · ToF-SIMS 로 **NiS · CoS · MnS · Li₂S · LiPₓClᵧ · LiCl** (사이클 뒤 보고되는 인산 · 아황산 · 황산 계와 다른 산물) 을 찾았다.  LiNbO₃ 코팅 (수 nm) 은 입계 이온 저항 증가를 21 Ω 으로 막았지만
전자 입계 저항을 키웠다 (t = 0 에서 296.7 vs 50.6 Ω).  5 일 숙성 셀의 첫 충전 용량은 베어 247 → 205 mAh g⁻¹ (83 %), 코팅 222 → 212 (95 %).
**σ 값 · 부피분율 식 · τ 는 보고하지 않는다** — 우리에게는 (i) Park σ₀ 출처 후보의 **부정 판정**, (ii) TLM 연결형 분류의 두 번째 T형 실측 사례, (iii) 복합체의 비-bulk (입계) 이온 항이 크고 **화학 숙성으로 시간에 따라 자란다**는 정성 자료다.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Sung-Kyun Jung**‡ᵃ, **Hyeokjo Gwon**‡ᵃ, Seok-Soo Lee ᵃ, Hyunseok Kim ᵃ, Jae Cheol Lee ᵇ, Jae Gwan Chung ᵇ, Seong Yong Park ᵇ, Yuichi Aihara ᶜ, **Dongmin Im**\*ᵃ (‡ 공동 1저자 · \* 교신) | **J. Mater. Chem. A 7 (2019) 22967–22976** | **10.1039/c9ta08517c** | SE **argyrodite** (Mitsui 제공 · 본문은 조성식 미기재, 그림 표지 Li₆PS₅Cl) · AM **Ni-rich NCM** (Ni:Co:Mn 미기재) · 코팅 **LiNbO₃** (수 nm) · EIS 펠릿은 탄소 · 바인더 없음 | **실험** (EIS · TLM 적합 · XPS · ToF-SIMS · SEM · TEM · XRD · 갈바노) — 시뮬레이션 없음 |

- 소속 (p.22967): ᵃ Next Generation Battery Lab, Material Research Center, Samsung Advanced Institute of Technology (SAIT), Samsung Electronics (수원) · ᵇ SAIT, Samsung Electronics · ᶜ Samsung R&D Institute Japan (Minoh, Osaka).
- 접수 2019-08-05 · 승인 2019-09-22 · 출판 2019-09-23 (p.22967).  © The Royal Society of Chemistry 2019 — 오픈 액세스 표기 없음 (머리의 "Licence and permissions" 링크만).
- 이해상충: *"There are no conflicts to declare"* (p.22975).  사사 절 없음.  ESI 있음 (그림 S1–S6 · 표 S1–S2 · 참고문헌 — 본문 목록 33 개와 같은 목록).
- 참고문헌 33 개 (p.22975–22976).  우리 축과 닿는 것: [19] Asano 2017 (NCM–Li₃PS₄ 복합 전극 전자 · 이온 전도도 — 이번 묶음 #23) · [22] Siroma 2016 · [23] Siroma 2015 · [24] Jamnik & Maier 1999 · [25] Kaiser 2018 · [28] Irvine 1990 (§11).

## 3. 핵심 수치 ★ (전부 원문 쪽 · 표지 병기)

### 3-1. 재료 · 공정 · 측정 조건

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | *"A sulfide-based argyrodite electrolyte provided by Mitsui"* — 조성식은 본문에 없다.  그림 3(a)(b) · SI 그림 S6 의 기준선 표지 = **Li₆PS₅Cl** | stated · p.22974 · p.22971 · SI p.6 |
| SE 의 σ | **보고 없음** (서론 · 본문의 "high ionic conductivity" 정성 표현뿐) | 전수 |
| AM | *"a Ni-rich NCM cathode material"* — Ni:Co:Mn · 입경 · 출처 미기재.  XRD = 층상 (003)…(201)/(116) (SI 그림 S1a).  SI 그림 S2 캡션 *"LiNbO₃-coated secondary and single particle of NCM"* — 2차 입자 · 단입자가 둘 다 나온다 (비율 미기재) | stated · p.22968 · p.22974 · SI p.1–2 |
| AM 입경 | **보고 없음**.  SI 그림 S4 (눈금 10 µm) 의 둥근 2차 입자 ≈ 5–7 µm | 판독 · 추세 전용 · SI p.4 |
| AM 의 σ | **보고 없음** | 전수 |
| 코팅 | LiNbO₃ — Li 금속 + 니오븀 에톡사이드를 IPA 에 녹여 NCM 투입 · 전구체 **0.75 mol%** · 회전증발 · **300 °C 1 h 공기 소성** · *"uniformly coated with several nanometers of LiNbO₃"* (TEM S1b 눈금 50 nm · EDS S2) | stated · p.22968 · p.22974 · SI p.1–2 |
| LiNbO₃ 전자 σ | **10⁻¹¹ S cm⁻¹** (ref 27 Benaissa 1992 — 논문 유일의 σ 수치) | stated (인용값) · p.22970 |
| EIS 펠릿 조성 | 양극 : 전해질 = **1 : 1 부피비 (중량비 7 : 2)** · 탄소 나노섬유 없음 | stated · p.22968 · p.22974 |
| 성형 | **295 MPa · 2 min** → 두께 **320 µm** (적합 입력 T = 0.0318 cm) | stated · p.22974 · SI p.7–8 |
| 측정 셀 | 두 **SUS 판** (이온 차단 집전체) 사이 · Teflon 셀 몸통 · *"We applied constant pressure on the pellet"* (그림 1a "P = const.") — **압력값 미기재** | stated · p.22968 · p.22974 |
| 전극 면적 | A = **1.327 cm²** (SI 표) = π(0.65 cm)² — ⌀13 mm (갈바노 셀 몸통 지름과 같음) | stated + 파생 · SI p.7 · p.22974 |
| EIS | Solartron 1470E 정전위기 + 1455 FRA · PEIS · **1 MHz – 10 mHz** · 진폭 **10 mV** · **25 °C** · *"every 1.5 h"* (SI 표 시점 = 0 · 1.4 · 5.6 · 12.6 · 19.6 · 26.6 · 33.6 · 40.6 h = 1.4 h 의 배수) | stated · p.22974 · p.22969 · SI p.7–8 |
| 기공률 · 펠릿 질량 · 재료 밀도 | **모두 보고 없음** → 기공률 계산 불가 | 전수 |
| 1:1 v/v ↔ 7:2 w/w | 두 표기가 같으려면 **ρ_NCM/ρ_SE = 3.5** (파생).  다른 정본 카드 밀도를 넣으면 7:2 w/w = SE **41.5 vol%** (Minnmann: NCM622 4.65 · LPSCl 1.87 g cm⁻³) · **38.0 vol%** (Park 2020: NCM 4.44 · LPSCl 2.07) — 고체 기준 · 이 논문 재료의 밀도는 미기재 | 파생 (§10) |
| 갈바노 셀 | 양극 = AM **9 mg** + argyrodite **5.25 mg** + 탄소 나노섬유 **0.75 mg** (= 60 : 35 : 5 wt%, 파생) 막자 혼합 · 분리막 SE **150 mg** · 양극 **15 mg** · 상대극 **Li–In** · ⌀13 mm Teflon · **295 MPa 2 min** · 뚜껑 **4 N·m 토크**로 정압 (MPa 환산 없음) · 숙성 셀 = 캡 체결 직후 글러브박스 **25 °C 5 일** | stated · p.22974 |
| 갈바노 조건 | 25 °C · 2.5–4.25 V *"versus the reduction potential of Li"* (Li–In ↔ Li 환산 미기술) · 형성 16 / 7 mA g⁻¹ (충 / 방) · 사이클 **50 / 80 mA g⁻¹** · TOSCAT-3100 | stated · p.22974 |

### 3-2. SI Table S1–S2 — TLM 적합 매개변수 전수 (stated, SI p.7–8)

베어 NCM + SE (Table S1):

| 시간 (h) | 0 | 1.4 | 5.6 | 12.6 | 19.6 | 26.6 | 33.6 | 40.6 |
|---|---|---|---|---|---|---|---|---|
| R_e (Ω) | 21.69 | 27.86 | 35.78 | 44.89 | 51.62 | 56.62 | 61.10 | 64.72 |
| R_e,gb (Ω) | 50.64 | 61.35 | 84.09 | 122.69 | 162.59 | 204.12 | 244.93 | 284.47 |
| Q_e (F cm⁻¹ s^(α−1)) | 9.24E-7 | 6.06E-7 | 4.67E-7 | 3.70E-7 | 3.22E-7 | 2.98E-7 | 2.80E-7 | 2.68E-7 |
| α_e | 0.520 | 0.542 | 0.540 | 0.531 | 0.521 | 0.511 | 0.503 | 0.496 |
| C_e (F) | 1.22E-7 | 1.07E-7 | 8.27E-8 | 6.05E-8 | 4.79E-8 | 4.06E-8 | 3.60E-8 | 3.25E-8 |
| R_i (Ω) | 27.51 | 34.49 | 43.46 | 52.35 | 58.36 | 62.51 | 66.07 | 68.92 |
| R_i,gb (Ω) | 273.99 | 273.53 | 339.07 | 415.81 | 488.02 | 555.46 | 613.79 | 663.25 |
| Q_i (F cm⁻¹ s^(α−1)) | 6.21E-7 | 4.29E-7 | 3.45E-7 | 2.96E-7 | 2.73E-7 | 2.65E-7 | 2.59E-7 | 2.55E-7 |
| α_i | 0.515 | 0.537 | 0.534 | 0.525 | 0.516 | 0.506 | 0.498 | 0.491 |
| C_i (F) | 2.45E-7 | 1.82E-7 | 1.38E-7 | 1.06E-7 | 8.75E-8 | 7.72E-8 | 6.88E-8 | 6.21E-8 |
| Q_cpe (F cm⁻¹ s^(α−1)) | 0.03965 | 0.05099 | 0.03804 | 0.02984 | 0.02527 | 0.0222 | 0.02006 | 0.0184 |
| α_cpe | 0.769 | 0.682 | 0.696 | 0.700 | 0.700 | 0.698 | 0.696 | 0.694 |
| L (H cm²) | 3.73E-6 | 4.04E-6 | 4.60E-6 | 5.27E-6 | 5.82E-6 | 6.34E-6 | 6.84E-6 | 7.27E-6 |

LiNbO₃ 코팅 NCM + SE (Table S2):

| 시간 (h) | 0 | 1.4 | 5.6 | 12.6 | 19.6 | 26.6 | 33.6 | 40.6 |
|---|---|---|---|---|---|---|---|---|
| R_e (Ω) | 21.29 | 19.15 | 20.98 | 22.72 | 23.12 | 23.84 | 24.42 | 24.60 |
| R_e,gb (Ω) | 296.70 | 304.88 | 323.03 | 343.84 | 360.41 | 373.29 | 385.19 | 395.99 |
| Q_e (F cm⁻¹ s^(α−1)) | 1.06E-06 | 1.29E-06 | 1.25E-06 | 1.20E-06 | 1.20E-06 | 1.19E-06 | 1.17E-06 | 1.17E-06 |
| α_e | 0.440 | 0.419 | 0.420 | 0.422 | 0.421 | 0.421 | 0.421 | 0.420 |
| C_e (F) | 1.78E-7 | 1.80E-7 | 1.86E-7 | 1.92E-7 | 2.01E-7 | 2.06E-7 | 2.06E-7 | 2.10E-7 |
| R_i (Ω) | 17.10 | 20.34 | 20.55 | 20.40 | 20.55 | 20.26 | 20.18 | 20.55 |
| R_i,gb (Ω) | 219.22 | 218.66 | 226.99 | 233.04 | 234.09 | 236.77 | 239.09 | 239.92 |
| Q_i (F cm⁻¹ s^(α−1)) | 1.32E-06 | 1.19E-06 | 1.25E-06 | 1.31E-06 | 1.31E-06 | 1.36E-06 | 1.37E-06 | 1.36E-06 |
| α_i | 0.424 | 0.434 | 0.427 | 0.420 | 0.418 | 0.414 | 0.412 | 0.412 |
| C_i (F) | 1.37E-7 | 1.37E-7 | 1.36E-7 | 1.32E-7 | 1.27E-7 | **1.28E-8** (인쇄 그대로 — 그림 2i 점은 ≈ 1.28×10⁻⁷, 오식) | 1.25E-7 | 1.24E-7 |
| Q_cpe (F cm⁻¹ s^(α−1)) | 0.02937 | 0.03063 | 0.03099 | 0.03160 | 0.03265 | 0.03329 | 0.03384 | 0.03448 |
| α_cpe | 0.805 | 0.796 | 0.799 | 0.800 | 0.796 | 0.795 | 0.793 | 0.790 |
| L (H cm²) | 6.90E-06 | 6.77E-06 | 6.89E-06 | 6.99E-06 | 7.06E-06 | 7.11E-06 | 7.17E-06 | 7.16E-06 |

- 두 표 모두 T (cm) = **0.0318** · A (cm²) = **1.327** 고정.  표의 R_e · R_i 는 본문 기호 R_e,bulk · R_i,bulk (그림 2a) 와 같은 양.
- "L (H cm²)" 은 **본문 어디에도 정의가 없다** — 본문 식의 L (두께, cm) 과 같은 글자이고, 베어에서는 시간에 따라 ≈ 2 배 (3.73 → 7.27 ×10⁻⁶) 변한다 (정체 미상 · §10).

### 3-3. 그림 2 의 인쇄값 (stated, p.22970)

| 패널 | 인쇄값 |
|---|---|
| (b) 이온 적합 (베어, t = 0) | R_e + R_e,gb = **72.3 ± 0.027 Ω** · R_i = **27.51 ± 0.223 Ω** · R_i,gb = **273.99 ± 2.13 Ω** · reduced χ² = **7.25E-3** |
| (c) 전자 적합 (베어, t = 0) | R_e,bulk = **21.69 ± 0.148 Ω** · R_e,gb = **50.65 ± 0.145 Ω** · R_i,bulk + R_i,gb = **324.83 ± 2.24 Ω** · reduced χ² = **7.18E-3** |
| (b)(c) 스펙트럼 | Z_re ≈ 29 → ≈ 72.5 Ω 의 두 호 (−Z_im 최대 ≈ 8 Ω @ ≈ 42 Ω · 둘째 호 ≈ 4.3 Ω @ ≈ 66 Ω) — 판독 |
| (d) k_e,bulk | 베어 **6.69 Ω h⁻⁰·⁵** · LiNbO₃ **0.87 Ω h⁻⁰·⁵** |
| (e) k_e,gb | LiNbO₃ **16.58 Ω h⁻⁰·⁵** (직선) · 베어 **5.66 Ω h⁻¹** (√t 에 포물선 · 단위 Ω/h) |
| (f) k_i,bulk | 베어 **6.74 Ω h⁻⁰·⁵** · LiNbO₃ **0.38 Ω h⁻⁰·⁵** |
| (g) k_i,gb | 베어 **8.23 Ω h⁻¹** (포물선) · LiNbO₃ **3.56 Ω h⁻⁰·⁵** (직선) |
| (h)(i) C_e · C_i | 베어는 둘 다 감소 (C_e 1.22→0.325 · C_i 2.45→0.621 ×10⁻⁷ F) · LiNbO₃ 는 거의 일정 (C_e 1.78→2.10 · C_i 1.37→1.24 ×10⁻⁷ F) — SI 표와 같은 값 |
| (j) 40 h 증가 (Ω) | 베어: bulk 전자 **43** · 입계 전자 **234** · bulk 이온 **41** · 입계 이온 **389** / LiNbO₃: **3.3** · **99** · **3.5** · **21** |

- 본문 p.22971: *"chemical reaction with the bare NCM electrode has the greatest effect on the increases in the ionic and electronic grain boundary resistances (389 and 234 Ω, respectively)"* · LiNbO₃ 는 입계 이온 21 Ω, 총 증가는 주로 입계 전자 (99 Ω).
- 본문 p.22971: *"Capacitance values are in the range from 10⁻⁸ to 10⁻⁷ F, indicating the response from the grain boundaries"* [28].
- 본문 p.22968: 초기 총 임피던스 *"(∼100 Ω)"* (베어) · *"(∼300 Ω)"* (LiNbO₃) — 어림값.  SI 의 R_e + R_e,gb = 72.3 · 318.0 Ω, 그림 1(c) 0 h 스펙트럼 ≈ 25 → ≈ 74 Ω (판독).

### 3-4. 파생 — 복합체 유효 σ (원문에 없는 값 · σ = T/(R·A), T 0.0318 cm, A 1.327 cm², l/A = 0.0240 cm⁻¹)

| 시간 (h) | 베어 σ_i,eff (mS cm⁻¹) | 베어 입계 몫 (이온) | 베어 σ_e,eff | LiNbO₃ σ_i,eff | LiNbO₃ 입계 몫 (이온) | LiNbO₃ σ_e,eff |
|---|---|---|---|---|---|---|
| 0 | **0.0795** | 90.9 % | **0.331** | **0.101** | 92.8 % | **0.0754** |
| 1.4 | 0.0778 | 88.8 % | 0.269 | 0.100 | 91.5 % | 0.0740 |
| 5.6 | 0.0626 | 88.6 % | 0.200 | 0.0968 | 91.7 % | 0.0697 |
| 12.6 | 0.0512 | 88.8 % | 0.143 | 0.0946 | 92.0 % | 0.0654 |
| 19.6 | 0.0439 | 89.3 % | 0.112 | 0.0941 | 91.9 % | 0.0625 |
| 26.6 | 0.0388 | 89.9 % | 0.0919 | 0.0932 | 92.1 % | 0.0603 |
| 33.6 | 0.0352 | 90.3 % | 0.0783 | 0.0924 | 92.2 % | 0.0585 |
| 40.6 | **0.0327** | 90.6 % | **0.0686** | **0.0920** | 92.1 % | **0.0570** |

- σ_i,eff = T/(A·(R_i + R_i,gb)) — TLM 이온 레일의 직류 등가 저항 (bulk + 입계) 기준.  σ_e,eff = T/(A·(R_e + R_e,gb)) = 저주파 극한 (= 순수 전자 경로, §4-1).
- 40.6 h / 0 h: 베어 σ_i × **0.41** · σ_e × **0.21** / LiNbO₃ σ_i × **0.91** · σ_e × **0.76**.
- 입계 몫이 숙성 내내 ≈ 89–93 % 로 거의 일정 — 베어에서는 bulk 와 입계가 **함께** 자란다 (bulk 이온 +41 Ω · 입계 이온 +389 Ω, 비율 유지).
- bulk 만의 등가 (t = 0): σ_i 0.87 (베어) · 1.40 (LiNbO₃) mS cm⁻¹ · σ_e 1.10 · 1.13 mS cm⁻¹ — 같은 SE · 같은 조성인데 이온 bulk 가 1.6 배 갈린다 (§10).
- (주의) 이 σ 들은 **NCM 의 이온 전도도도 포함**한다 — 원문 p.22968: *"The transmission line of the ions reflects the total ionic conductivity of the composite, including the individual ionic conductivities of NCM and argyrodite."*

### 3-5. 화학 분석 (stated, p.22971–22972 · 그림 3 · SI 그림 S5–S6)

| 항목 | 값 |
|---|---|
| S 2p — 순수 argyrodite · LiNbO₃ 셀 (표면 · 식각 뒤) | **163.0 · 161.8 eV** — 순수 argyrodite 와 같다 (S5 차분도 미미) |
| S 2p — 베어 셀 표면 | 환원 상태 **162.4 · 161.2 · 160.9 eV** → **NiS · CoS · MnS · Li₂S** 가능성 [30, 31] · 식각 뒤는 argyrodite 와 비슷 |
| 사이클 뒤 문헌 산물 [14] | 아황산 **167 eV** · 황산 **169 eV** — 이 화학 숙성에서는 **안 나온다** |
| Cl 2p | argyrodite Cl 2p₃/₂ **199.0 eV** · 베어 표면만 추가 **≈ 198.5 eV (LiPₓClᵧ)** · **≈ 200.2 eV (LiCl)** [32] |
| P 2p (SI 그림 S6) | 코팅 셀도 표면에서 낮은 결합에너지 쪽 이동 · 베어는 표면 · 식각 모두 크게 이동 · 인산 · 아인산 같은 산소 포함 화합물은 안 보임 |
| 원문 해석 | P 계 산물 → **전자 입계 저항** 증가 · S · Cl 계 산물 → **이온 입계 저항** 증가 (정성 연결, p.22972) |
| 사이클 뒤 문헌 [13] 과 비교 | 사이클 뒤 = Mn₃(PO₄)₂ · Ni₃(PO₄)₂ · Li₃PO₄ · POₓ⁻ · SOₓ⁻ (2 ≤ x ≤ 3) / SOC 0 화학 숙성 = 금속 황화물 · Li₂S · LiPₓClᵧ · LiCl → *"electrochemical cycling promotes the participation of oxygen"* |
| ToF-SIMS CEI 두께 (NiO 포화까지 스퍼터 시간) | 베어: 신선 **12 s** → 숙성 **25 s** (≈ 2 배) · LiNbO₃: *"changed only slightly"* · 숙성 베어 층은 Cl⁻ · LiCl⁻ · LiCl₂⁻ 신호가 큼 → **염소 계 산물 주도** |

### 3-6. 전기화학 (stated, p.22972–22973 · 그림 4)

| 항목 | 베어 NCM | LiNbO₃ 코팅 NCM |
|---|---|---|
| 첫 충전 용량, 신선 (16 / 7 mA g⁻¹) | **247 mAh g⁻¹** | **222 mAh g⁻¹** |
| 첫 충전 용량, 숙성 (5 일 이상) | **205 (83 % 유지)** | **212 (5 % 감소)** |
| 전압 히스테리시스 ΔV, 신선 → 숙성 | **0.10 → 0.28 V** | **0.14 → 0.19 V** |
| 사이클 (50 / 80 mA g⁻¹) 첫 용량 감소 (숙성 효과) | **43 %** (그림 4b: ≈ 100 → ≈ 57 mAh g⁻¹, 판독) | **24 %** (≈ 108 → ≈ 83, 판독) |
| 50 사이클 유지율 | 신선 **59 %** · 숙성 **80 %** | **≈ 78 %** (숙성 무관) |
| 에너지 효율 (판독) | 신선 ≈ 85 → 74 % · 숙성 ≈ 80 → 77 % | ≈ 90 → 86 % |

- 원문 해석: 숙성 베어의 사이클 유지율이 더 좋은 것은 SOC 0 에서 계면이 안정한 형태로 바뀌어 화학 반응성을 잃었기 때문 (p.22973) · 코팅 셀의 초기 용량 감소는 전자 절연 코팅으로 커진 입계 전자 저항 탓 (p.22973).
- (주의) "83 %" (형성 전류) 와 "43 %" (사이클 전류) 는 **다른 전류의 첫 용량**이다 — 본문 p.22973 은 43 % 를 *"as described before"* 로 잇는다 (§10).

### 3-7. 내부 정합 검사 (파생)

| 검사 | 결과 |
|---|---|
| 그림 2(j) 증가 ↔ SI 표 차 | 389.26 · 233.83 · 41.41 · 43.03 (베어) · 20.70 · 99.29 · 3.45 · 3.31 (코팅) → 인쇄값과 **전부 일치** |
| 그림 2(b) ↔ 2(c) 이온 합 | (b) R_i + R_i,gb = **301.50 Ω** ↔ (c) R_i,bulk + R_i,gb = **324.83 Ω** → **7.7 % 어긋남** (두 단계 적합이 이온 쪽에서 서로 맞지 않는다).  전자 합은 72.34 ↔ 72.3 으로 맞는다 |
| 그림 2(c) ↔ SI 표 | R_e,gb 50.65 ↔ 50.64 (반올림) |
| k 값 재현 (SI 표 · 무가중 최소제곱) | 베어 R_e 직선 6.96 (인쇄 6.69) · R_i 6.69 (6.74) · R_e,gb 2 차 계수 5.77 (5.66 Ω/h) · R_i,gb 7.74 (8.23 Ω/h) / 코팅 R_e 0.75 (0.87) · R_i 0.33 (0.38) · R_e,gb 16.3 (16.58) · R_i,gb 3.65 (3.56) → 1–15 % 차.  가중 · 맞춤식 미기술 → 표에서 k 를 다시 내지 말 것 |
| 고주파 끝 ↔ bulk 병렬 | 두 bulk 의 병렬 R_i·R_e/(R_i + R_e) = **12.1 Ω** (베어 t = 0) 인데 측정 스펙트럼은 1 MHz 에서 Z_re ≈ 29 Ω (판독) → bulk 값은 **측정창 밖 외삽**을 포함한다 (CPE α ≈ 0.5 라 1 MHz 에서도 입계 CPE 가 단락되지 않음 — 우리 추론) |
| 저주파 끝 ↔ 전자 합 | 그림 2(b) 끝 ≈ 72.5 Ω (판독) = R_e + R_e,gb 72.3 → ee-연결 직류 극한 = 전자 경로뿐 (§4-1) 과 정합 |
| A ↔ 지름 | π(0.65 cm)² = 1.3273 cm² ↔ 표 1.327 (⌀13 mm) |

## 4. ★ 방법 — 저항을 떼어 내는 사슬

### 4-1. TLM 임피던스 식 (Methods, p.22974 · 렌더로 확인 · 번호 없음)

```
Z_e−e connection = (Z_i·Z_e/(Z_i + Z_e))·L
                 + [2·Z_e²·√Z_cpe / (Z_i + Z_e)^(3/2)] · [cosh(L·√((Z_i + Z_e)/Z_cpe)) − 1] / sinh(L·√((Z_i + Z_e)/Z_cpe))
```
- 원문 기호 정의: *"Z_i, Z_e, and Z_cpe are the ionic, electronic, and constant-phase element impedances [Ω cm], respectively, and L [cm] is the thickness of the composite pellet."*
- **Siroma 2015 대응**: 표 3 T형 **"open–open"** 행 Z = z_A z_C/(z_A + z_C)·L + 2 z_A² √z_B/(z_A + z_C)^(3/2)·(cosh β − 1)/sinh β 와 글자 그대로 같은 꼴 — **z_A = Z_e (단자 레일 = 전자) · z_C = Z_i (양 끝이 막힌 레일 = 이온) · z_B = Z_cpe** (siroma2015 카드 §표 3).  정본 J 절의 *"앞계수 z_el² 는 이온 차단 (SS) 셀 판"* 과 같은 판이다.
- **극한 (우리 유도 · Siroma 카드의 T형 극한과 같음)**:
  - ω → 0 (Z_cpe → ∞): (cosh β − 1)/sinh β → β/2 → Z → **L·Z_e** = 전자 경로 저항 전부.  원문 p.22969 *"the total impedance equals the summation of R_e,bulk and R_e,gb"* 와 같은 말.
  - ω → ∞ (Z_cpe → 0): Z → **L·Z_iZ_e/(Z_i + Z_e)** = 두 레일 **병렬** (이온이 두께 전체를 전자와 나란히 지나간다).
  - ⇒ 직류 극한에 이온 정보가 **없다**.  이온 저항은 고주파 쪽 두 레일의 결합 (병렬 항) 으로부터 **적합으로만** 얻는다 = 모형 의존.
- **단위 표기 오류**: 쌍곡선 인자 L·√((Z_i + Z_e)/Z_cpe) 가 무차원이려면 (Z_i + Z_e)/Z_cpe 가 cm⁻² 여야 한다 → Siroma 1D 관례대로 **Z_i · Z_e [Ω cm⁻¹] · Z_cpe [Ω cm]** 여야 하고, 원문의 "모두 [Ω cm]" 는 차원이 맞지 않는다 (§10).

### 4-2. 등가회로 · 적합 절차 (p.22968–22969 · p.22974 · 그림 2a)
- 회로 (그림 2a): 집전체 | (양극 + 전해질, 1:1 v/v) | 집전체.  **이온 레일** = R_i,bulk 직렬 (R_i,gb ∥ Q_i,gb) · **전자 레일** = R_e,bulk 직렬 (R_e,gb ∥ Q_e,gb) · 두 레일 사이 = Q_cpe (계면).  단자는 전자 레일 양 끝 ("electron").
- *"four resistive components and three capacitive components"* (p.22969).  각 레일 = *"a Randles circuit without a Warburg element"*.
- **제외한 것**: Warburg 임피던스 · 전하전달 저항 — *"the charge transfer resistance is expected to be large under the experimental conditions of 10 mV amplitude in the Au/NCM + SE composite/Au configuration"* [22] (p.22969 · 셀은 SUS 인데 문장은 Au — §10).
- **두 단계 적합**: ① 전자 레일을 저항 하나 (= 직류 극한값 R_e + R_e,gb) 로 두고 이온 레일의 R_i,bulk · R_i,gb 를 분리 (그림 2b) ② 이온 레일을 저항 하나로 두고 전자 레일의 R_e,bulk · R_e,gb 를 분리 (그림 2c) — *"obtained reasonable reduced chi-square values in both cases"* (p.22969 · p.22974).
- **조성 선택의 이유**: TLM 이 명확한 두 반원을 주려면 총 이온 · 전자 전도도의 비가 알맞아야 하고, 그 비는 부피분율로 조절된다 [19] → **1:1 에서 두 반원이 분명했다** (p.22968–22969).  저자 스스로 *"Our model does not perfectly describe the actual cell system requiring higher loading amount of cathode active materials"* (p.22969).
- 원문의 반원 배정: 두 반원 = *"ionic and electronic pathways at high and low frequencies"* (p.22968).
- 적합 소프트웨어 · 가중 · 반복 셀 수: **미기재**.

### 4-3. 속도 상수 분석 (p.22969–22970)
- 저항을 **√t** 에 대해 그려 직선이면 확산 지배 반응 (Li 금속 | SE 계면층 성장 [11, 26] 과 같은 거동) 으로 읽는다.  기울기 = 속도 상수 k (Ω h⁻⁰·⁵).
- 베어의 입계 저항 둘은 √t 에 **포물선** (단위 Ω h⁻¹) → *"cannot be explained by the simple model of thickness increase"* → 확산 지배 반응 + 반응 산물에 의한 물리적 접촉 손실의 복합으로 해석 (p.22970–22971).
- 코팅 셀은 입계 전자 저항 (16.58 Ω h⁻⁰·⁵) 외에는 k 가 *"negligibly low"* (p.22970).

### 4-4. 화학 분석 · 형상 분석 (p.22974–22975)
- 분해 · 이송 = 글러브박스, 신선 또는 숙성 뒤 **3 h 이내** 측정.
- XPS: Quantum 2000 (ULVAC-PHI) · 단색 Al Kα 1486.6 eV · 25 W · 15 kV · 스폿 100 µm · FAT 모드 · 기저압 < 1×10⁻⁹ Torr · 서베이 −2–1250 eV (0.8 eV 간격) · 정밀 C 1s · S 2p · Cl 2p · P 2p (통과에너지 29.35 eV · 0.125 eV) · 깊이 = Ar⁺ 1 kV 스퍼터 · C 1s 284.5 eV 보정.
- ToF-SIMS: nanoTOF TRIFT V (ULVAC-PHI) · 음이온 스펙트럼 · 30 keV Bi⁺ 1 pA · 펄스 20.0 ns (bunching < 1 ns) · 100 × 100 µm² 래스터 · 스퍼터 5 keV · 50 nA Ar⁺ (300 × 300 µm²) · 20.0 eV 전자총 전하 보상.  CEI 두께 = NiO 신호 포화까지의 스퍼터 시간 [13].
- TEM (HAADF · EDS): Titan cubed G2 60-300, 300 kV · XRD: D8 Discover, Cu Kα · UHR-SEM · EDS: SU-9000, 15 kV.
- in situ SEM (SI 그림 S4): *"without external pressure in vacuum state"* · 신선 vs 5 일 뒤 · 베어만.

### 4-5. 시뮬레이션 · 입자 처리
- **시뮬레이션 없음.**  입자 처리 (구 · 형상 · PSD · 소성) 항목은 해당 없음 — 입경 · PSD 미보고.
- TLM 의 레일 · CPE 는 **등가회로 매개변수**이지 측정 기하가 아니다 ("입계" 의 자리 — SE–SE · SE–NCM · NCM–NCM — 를 회로가 가르지 않는다).
- DEM 관점의 위치: 이 논문은 강체구도 연속체도 아닌 **실물**이고, 우리 모델과의 연결은 (i) 측정 연결형의 분류 (ii) 복합체 계면 항의 존재 · 시간 의존 (iii) 압밀 조건 (295 MPa) 뿐이다.

### 4-6. 기법 미니 용어집
- **TLM (전송선 모델)**: 다공 복합 전극을 이온 레일 + 전자 레일 + 둘 사이 계면 소자의 사다리 회로로 보는 모형.  연결형 (어느 레일의 어느 끝에 단자가 붙는가) 에 따라 해가 다르다 (Siroma 2015 Z · T · E · 범용형).
- **ee-연결 (electron–electron connection)**: 두 집전체가 전자만 통하고 이온은 막는 배치 (SUS | 복합체 | SUS) — Siroma T형 open–open, 단자 레일 = 전자.  직류 극한 = 전자 저항, 고주파 극한 = 두 레일 병렬.
- **CPE (constant phase element)**: Z ∝ 1/(Q·(iω)^α).  α = 1 이면 이상 축전기.  이 논문의 레일 CPE 는 α 0.41–0.54 로 이상 축전기와 거리가 멀다 (분포가 넓은 응답).
- **입계 (grain boundary, gb) 저항**: 이 논문에서는 각 레일의 (R_gb ∥ Q_gb) 호의 저항.  원문은 C 크기 (10⁻⁸–10⁻⁷ F) 로 입계라 배정 [28].
- **reduced χ²**: 적합 잔차 제곱합 ÷ 자유도 — 적합 품질 지표 (7.25E-3 · 7.18E-3).
- **SOC 0 화학 숙성**: 방전 (리튬화) 상태 양극을 전위 인가 없이 SE 와 접촉시켜 둔 시간 — 전기화학 사이클이 없는 순수 화학 반응.
- **CEI (cathode electrolyte interphase)**: 양극–전해질 사이에 생긴 반응층.  원문은 화학 숙성 산물이 사이클 중 CEI 형성에 기여한다고 본다 (p.22972).
- **ToF-SIMS 깊이 프로파일**: 스퍼터하며 2 차 이온을 세어 깊이별 조성을 보는 법 — 여기서는 NiO 포화까지의 시간으로 반응층 두께를 상대 비교.
- **LiNbO₃ 코팅**: 황화물 SE 와 산화물 양극 사이 반응 · 계면 저항을 줄이는 수 nm 산화물 층 [18].  전자 절연 (10⁻¹¹ S cm⁻¹ [27]).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** (p.22969) | (a) SUS \| 복합체 \| SUS 셀 모식 (P = const., 교류 ΔE) · (b) 신선 복합체 단면 SEM + EDS (O = NCM · S · Cl = SE) · (c)(d) 베어 · 코팅 셀의 시간별 Nyquist (세로 오프셋 쌓기) · (e)–(h) 40 h 전후 단면 SEM (베어 숙성 = 균열 · 접촉 손실 / 코팅 = 유지) | ee-연결 셀의 그림 증거 · 베어 스펙트럼이 시간에 따라 오른쪽으로 길어짐 (저항 증가) · 접촉 손실의 형상 증거 (정성) |
| **2** (p.22970) | (a) TLM 등가회로 · (b)(c) 두 단계 적합 + 인쇄값 · (d)–(g) bulk · 입계 저항 vs √t + k · (h)(i) 입계 C vs √t · (j) 40 h 증가 막대 | ★ 핵심 — 이온 입계 몫 · 화학 숙성의 크기 · 코팅 효과 (389 vs 21 Ω) · 두 단계 적합의 이온 합 불일치 (301.5 vs 324.8 Ω) |
| **3** (p.22971) | (a)(c) S 2p · (b)(d) Cl 2p XPS (표면 실선 · 식각 점선 · 순수 argyrodite = Li₆PS₅Cl 표지) + 피크 분해 (NiS · Li₂S · LiPₓClᵧ · LiCl) · (e)(f) ToF-SIMS 깊이 프로파일 (신선 / 숙성, 표면 영역 음영) | 반응 산물의 화학 정체 — 우리 모델 밖 (화학 없음).  SE 조성 표지 Li₆PS₅Cl 의 유일한 원문 자리 |
| **4** (p.22973) | (a) 첫 사이클 프로필 (신선 w/o rest · 숙성 w/ rest, ΔV 표지) · (b) 50 사이클 용량 · 에너지 효율 | 화학 숙성 → 용량 · 과전압 — 셀 수준 결과 (우리 정적 모델과 직접 대응 없음) |
| SI S1 (SI p.1) | XRD (베어 · 코팅 NCM) · TEM 코팅층 (눈금 50 nm) | 층상 구조 유지 · 코팅 두께 수 nm |
| SI S2 (SI p.2) | 코팅 NCM 2 차 입자 · 단입자의 HAADF + EDS (Ni · Co · Mn · O · Nb, 눈금 200 · 60 nm) | AM 이 2 차 입자 · 단입자 혼재 (비율 미기재) |
| SI S3 (SI p.3) | 1:1 복합체 펠릿 단면 SEM (눈금 막대 값 미표기) | 두께 · 균질도 정성 |
| SI S4 (SI p.4) | 무가압 진공 in situ SEM — 신선 vs 5 일 (노란 화살표 = 균열 · 미세구조 변화, 눈금 10 µm) | 화학 유발 균열 가설의 근거 — **코팅 대조 없음** (§10) |
| SI S5 (SI p.5) | XPS 차분 스펙트럼 (표면 − 순수 SE · 식각 − 표면) | 코팅 셀의 변화가 미미함을 정량적으로 보이는 보조 |
| SI S6 (SI p.6) | P 2p XPS + 차분 | P 계 산물 → 전자 입계 저항 해석의 근거 |
| SI Table S1–S2 (SI p.7–8) | 시간별 TLM 적합 매개변수 전수 (§3-2) | ★ 원자료 — σ_eff 파생의 유일한 원천 |

- 크롭 후보 (메인 순서대로 · 캡션 대조): **Fig. 2** > **SI Table S1** > **Fig. 1** > **SI Table S2** > **SI Fig. S4** > Fig. 4 > Fig. 3.

## 6. Post-processing ★
- **무엇**: EIS (1.5 h 간격) → ee-연결 TLM 두 단계 적합 → R_e,bulk · R_e,gb · R_i,bulk · R_i,gb · Q · α · C → √t 에 대한 직선 / 포물선 맞춤 → 속도 상수 k → 40 h 증가 막대 (그림 2j).
  XPS 피크 분해 (S 2p · Cl 2p 이중항) · 차분 스펙트럼 (S5) · ToF-SIMS 의 NiO 포화 시간 → 반응층 상대 두께.  갈바노: ΔV (히스테리시스) · 용량 유지율 · 에너지 효율.
- **도구**: Solartron 1470E + 1455 FRA · TOSCAT-3100 · ULVAC-PHI Quantum 2000 / nanoTOF TRIFT V · FEI Titan · Bruker D8 · Hitachi SU-9000.  적합 소프트웨어 미기재.
- **수치화 · 플롯**: 저항은 Ω (전극 전체) 로만 보고하고 σ 로 바꾸지 않는다 · C 는 F (기하 정규화 없음) · k 는 Ω h⁻⁰·⁵ 또는 Ω h⁻¹ (맞춤 꼴에 따라 단위가 다르다).
- **기공 · 밀도 회계 없음**: 조성은 "1:1 v/v (7:2 w/w)" 뿐 — 압분체 기공률을 세지 않는다.

### 6-bis. 절별 논증 흐름
1. **문제 (p.22967–22968)**: ASSB 계면 열화는 부피 변화 · 고전위 산화 · 조립 직후 화학 반응이 얽혀 있다.  Li 금속 쪽은 계면층 성장 속도까지 연구됐지만 [11], 양극 쪽은 사이클 뒤 화학 상태 [12, 13] 만 보였고, DFT 가 예측한 안정 계면 화합물 [14, 15] 은 사이클 뒤 산물과 다르다 → **정상 상태 (SOC 0) 화학 반응**을 따로 떼어 볼 필요.
2. **설계 (p.22968)**: 양극 + SE 만의 1:1 펠릿 · 정압 · 베어 vs LiNbO₃ 코팅 · 시간별 EIS.  초기 임피던스는 베어가 작지만 (∼100 vs ∼300 Ω) 더 빨리 커진다 · 40 h 뒤 SEM 에서 베어만 균열 · 접촉 손실.
3. **입계 화학 열화 (p.22968–22971)**: TLM 으로 bulk / 입계를 분리 → 베어는 모든 저항이 크게 늘고 특히 입계 둘이 √t 에 포물선 · 입계 C 감소 → 접촉 손실 · 균열 동반 해석 → 무가압 in situ SEM 으로 균열 생성 확인 (가압 해제 이완 [29] 을 배제하려는 시도).  코팅은 입계 이온 증가를 21 Ω 으로 억제, 총 증가는 입계 전자 (99 Ω) 가 주도.
4. **산물 (p.22971–22972)**: XPS · SIMS 로 NiS · CoS · MnS · Li₂S · LiPₓClᵧ · LiCl (베어 표면) — 사이클 뒤 산소 포함 산물과 다름 · 코팅 셀은 P 2p 만 변함 → P 계 = 전자 입계, S · Cl 계 = 이온 입계 (정성 연결).  SIMS 반응층 두께 2 배 (12 → 25 s), 염소 계 주도.
5. **전기화학 영향 (p.22972–22973)**: 숙성 → 베어 첫 충전 용량 −17 % · ΔV 0.10 → 0.28 V · 사이클 유지율은 오히려 개선 (계면이 반응성을 잃음) · 코팅은 손실이 작다.
6. **결론 (p.22973–22974)**: SOC 0 화학 반응만으로도 반응 산물 + 접촉 손실로 성능이 크게 나빠진다 · 입계에서 열화가 빠르고 특히 이온 전도를 막는다 · 코팅의 효과는 **이온 절연성 산물의 생성을 막는 것**.

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 = CLAUDE.md ★★ τ 명명 규약 (1저자 비준 10-03).  'tortuosity factor' 는 τ² (`tau2`) 에만 쓴다.
> **이 논문은 τ 를 정의 · 보고하지 않는다** (본문 · SI 전수, "tortuos" 0 건).  아래 표는 이 논문의 **측정량**이 우리 다섯 양 중 어디에 닿는지 (또는 안 닿는지) 를 적는다.

| 원문 기호 (쪽) | 원문 정의 | 원문 이름 | 정규화 (어느 부피 · 어느 단면 · 어느 σ₀) | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| τ | **없음** | — | — | — | 이 논문에서 tau2 · tau · τ_geo · τ_e 어느 것도 계산할 수 없다 (아래) |
| Z_i · Z_e · Z_cpe (p.22974) | TLM 레일 · 계면 임피던스 | ionic / electronic / constant-phase element impedances | 원문 단위 "[Ω cm]" (차원 오류 — 4-1) · 두께 L | — (등가회로 매개변수) | Siroma z_C · z_A · z_B 에 대응 |
| R_i,bulk + R_i,gb (SI 표 · 그림 2b) | 이온 레일의 직류 등가 저항 (적합) | bulk / grain-boundary resistance of ion | 전극 전체 (A 1.327 cm² · T 0.0318 cm) | **σ_eff 의 분모** — σ_i,eff = T/(A·(R_i + R_i,gb)) (파생) | 관통 꼴 (두 레일이 두께 전체에서 병렬, 4-1) — 단 직류 측정이 아니라 **고주파 결합의 적합값** |
| σ_i,eff / σ₀ | 계산 불가 | — | σ₀ 미보고 | **f** = n/a | — |
| φ·σ₀ / σ_i,eff | 계산 불가 | — | σ₀ · 기공률 미보고 · φ 는 명목 1:1 v/v (고체 기준) 뿐 | **tau2** = n/a | 감도만 (파생): tau2 = **6.3 · σ₀[mS cm⁻¹] · (φ_SE/0.5)** (베어 t = 0) · **4.9 ·** (코팅 t = 0) · 15.3 · (베어 40.6 h) · 5.4 · (코팅 40.6 h) — σ₀ 와 φ 에 정비례 |
| (R_i + R_i,gb)/R_i | 등가회로 분해비 | — | 같은 레일 | **우리 FULL/CF 와 다른 양** | 11.0 (베어) · 13.8 (코팅), t = 0, 파생 — 숫자를 맞대지 않는다 (§8) |
| R_e,bulk + R_e,gb (직류 극한 L·Z_e) | 전자 경로 저항 | bulk / grain-boundary resistance of electron | 전극 전체 · 탄소 없음 (NCM 경로) | 전자 σ_eff (파생) | σ_e,eff 0.331 (베어) · 0.0754 (코팅) mS cm⁻¹ (t = 0) · tau2_e 는 σ_NCM 미보고로 n/a |
| (√ 값) | 없음 | — | — | **tau** = n/a | — |
| (최단 경로) | 없음 | — | — | **τ_geo** = n/a | 기하 미보고 |
| (편측 접근 TLM) | 없음 | — | — | **τ_e** — 이 논문은 τ_e 계열이 **아니다** | 이 셀은 ee-연결 T형 (관통) — Kaiser Type-A (전극 \| SE \| 전극, 편측 접근) 와 다르다 |
| L (H cm², SI 표) · T (cm, SI 표) · α (CPE) · k (속도 상수) | — | — | — | **기호 충돌** | L 은 본문에선 두께 · SI 에선 정의 없는 H cm² 양 · T 는 SI 에서 두께 (우리 옛 "T" = tau2 · 온도와 충돌) · α 는 Bruggeman 지수 아님 · k 는 κ (열전도) 아님 |

**σ₀ 기준**: **없음** — 순수 SE (argyrodite) 펠릿을 재지 않았고 SE 의 σ 를 어떤 형태로도 적지 않는다.  논문에 있는 유일한 전도도 수치는 코팅 물질 LiNbO₃ 의 10⁻¹¹ S cm⁻¹ (인용값, p.22970) 이다.
우리 망 σ₀ 3.0 mS/cm (펠릿값, 원장 `CL-91`) 와 짝지을 대상이 이 논문에는 없다.

**환산 사슬 (한 줄로)**:
```
σ_i,eff  = T/(A·(R_i + R_i,gb))                 (파생 · 관통 꼴 · TLM 고주파 결합의 적합값)
f        = σ_i,eff/σ₀                            → n/a (σ₀ 없음)
tau2     = φ_SE·σ₀/σ_i,eff                       → n/a (σ₀ · 기공 없음) ; 감도 = 6.3·σ₀·(φ_SE/0.5)  (베어, t = 0)
φ_SE     ≤ 0.5 (명목 1:1 v/v 고체 기준 × (1 − p)) ; 7:2 w/w 와 다른 카드 밀도면 0.38–0.42 (고체 기준)
τ_e      → 해당 없음 (T형 · 관통 연결)
```

**판정**:
1. 이 논문은 **τ 문헌이 아니다** — tau2 · f 를 만들 수 있는 두 입력 (σ₀ · φ) 이 다 빠져 있다.  남는 것은 복합체 σ_eff (파생) 와 그 시간 변화다.
2. 연결형으로는 **T형 open–open (관통형)** 이다 — 이온 저항도 두께 전체 경로의 저항으로 정의된다 (편측 접근 τ_e 가 아니다).  같은 계열 사례 = Minnmann 식 [1] (정본 J 절).  "EIS-TLM" 이라는 낱말만으로 τ_e 로 분류하지 않는다 (결정 5 · 13 한정어와 정합).
3. 다만 이온 저항은 **직류가 아니라 고주파 결합에서 적합으로** 나온다 (직류 극한은 전자뿐) → 같은 관통 꼴이라도 Kaiser Type-B (직류 Li⁺ 전류) 보다 모형 의존이 크다.
4. 감도식 tau2 = 6.3·σ₀·(φ/0.5) 는 **σ₀ 선택만으로 3 배** 흔들린다 (다른 재료의 펠릿 σ₀ 1.02 · 1.6 · 3.0 mS cm⁻¹ 를 넣으면 6.4 · 10.1 · 18.9 — 이 논문의 tau2 가 아니라 감도 산술) → 결정 4 의 "같은 재료 · 같은 압밀의 σ₀ 짝" 요구를 숫자로 보여 준다.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (이 브랜치에서는 값 자리표시 상태 — 우리 수치는 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` · CLAUDE.md 의 값으로 적는다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 실험 — 수송 (복합체 EIS) + 화학 (XPS · SIMS) + 형상 (SEM) | DEM 접촉망 T (관통) · STEP3 복셀 σ (CONTACT_FREE 가지) · MPM 형상 | 이 논문은 **시간 · 화학** 축을 가진다 — 우리 두 모델 모두 없는 축 |
| frame[4] | 실험 — 원칙상 독립 보정 앵커 후보 | 각 모델을 실험에 따로 보정 | 이 값으로 우리 모델을 맞추지 않는다 (σ₀ · 기공 · 입경 · AM 조성 미상) |
| SE | argyrodite (Mitsui · 그림 표지 Li₆PS₅Cl) · σ₀ 미보고 | LPSCl · 망 σ₀ 3.0 mS/cm (펠릿값, `CL-91`) | 같은 계열 · σ₀ 짝 없음 |
| AM | Ni-rich NCM (조성 · 입경 미기재 · 2 차 입자 + 단입자) · 베어 vs LiNbO₃ 수 nm | NMC811 bimodal · 강체구 + 연화 E_eff · 망에 코팅 없음 | 코팅이 전자 입계 저항을 t = 0 에서 5.9 배 (296.7/50.6) 바꾼다 — 우리 전자망에 없는 항 |
| 탄소 | EIS 펠릿 **없음** | DEM 망 탄소 없음 | 같음 — 이 점만은 대조 조건이 맞는다 |
| 조성 | 1:1 v/v (고체 명목) = 7:2 w/w (밀도비 3.5 함의) | φ_SE 띠별 (메모 v2 §3-3: 0.613 · 0.536 · 0.444 · 0.330 · 0.248) | 이 논문은 한 점 · φ 축 위치가 0.38–0.50 사이에서 불확정 |
| 압밀 | 295 MPa · 2 min (냉간) | 300 MPa 계열 냉간 압밀 | 비슷 |
| 측정 상태 | 25 °C · 정압 (값 미기재) · SUS 이온 차단 · ee-TLM · 0–40.6 h | 정적 기하 (판 고정 완화) 의 망 · 시간 없음 | 우리 = **숙성 0 의 기하**에 해당 |
| 계면 항 | TLM 입계 = 이온 저항의 91–93 % (t = 0, 등가회로) · 시간에 따라 증가 (베어) | 접촉망: SE–SE Holm (FULL) vs CF · 복셀: 계면 항 0 (CL-81) · ① r_int 기구 OFF | **다른 양** — 비율로 맞대지 않는다 (§8) |
| 값 (판정 없이) | σ_i,eff 0.080 (베어) · 0.101 (코팅) mS cm⁻¹ @ 1:1 v/v · t = 0 (파생) | — (절대 σ_eff 끼리는 비교하지 않는다 — 메모 v2 §3-1) | 참고: Bazzoun 실험 0.101 mS cm⁻¹ @ CAM:SE 52:46 v/v · 400 MPa (stated, `bazzoun2026_…` 카드) 와 같은 자릿수 — 재료 · 압력 · 방법이 달라 **일치로 읽지 않는다** |
| 접촉 손실 | 화학 숙성 → 균열 · 접촉 손실 (SEM · C 감소 · 무가압 in situ SEM) | DEM 접촉은 압밀 직후 그대로 · Auerbach 파괴 = 역학 · A10 원장 = 사이클 수축 개구 | 화학 유발 접촉 손실은 우리 모델 밖 (축 F) |

- **방법 artifact 와 실제 차이의 구분**: 이 표의 어느 행도 "모델 오차 배수" 를 주지 않는다.  ① 실물 (형상 소성 · 화학) vs 강체구 DEM · 연속체 MPM ② 재료 (Mitsui argyrodite · 미지정 Ni-rich NCM) ③ 파생 σ (TLM 고주파 결합의 적합값) vs stated ④ 단일 조성 · 단일 압력 · 단일 온도 — 넷이 겹친다.
- **frame[5]** — 이 논문이 가진 반쪽 = 실험 수송 (복합체 저항의 bulk / 입계 분해 · 시간 변화) + 계면 화학.  없는 반쪽 = 미세구조 (입경 · 기공 · 상 분포) · 기계 (압밀 · springback) · σ₀.

## 8. 적용 인사이트 (내 연구에 어떻게) — 이 묶음이 닫으려는 것

### Park σ₀ 조성식의 출처

**답: 이 논문 ([18b]) 에 없다.**

| 물음 | 이 논문 | 판정 |
|---|---|---|
| 찾는 두 값 | Park 2020 SI Table S1 각주 b ("Parameters based on literature[18a-c]") — (i) NCM 전자 σ **8.5×10⁻⁴ S cm⁻¹** (ii) LPSCl 이온 σ = **−4.45×10⁻³·ε_s + 4.64×10⁻³ S cm⁻¹** (ε_s = AM 부피분율) | (park2020 카드 §4 · SI p.11 기록) |
| 확인 범위 | 본문 p.22967–22976 전 10 쪽 (그림 1–4 · 캡션 · Methods 식 · 참고문헌 33) + SI p.1–10 (그림 S1–S6 · 표 S1–S2 · 참고문헌) — 렌더 판독 + 텍스트 검색 ("S cm" · "conductiv" · "volume fraction" · "8.5" · "tortuos") | 전수 |
| 8.5 · 4.45 · 4.64 라는 수 | **어디에도 없다** | 없음 |
| σ 값 | 논문 전체의 S cm⁻¹ 수치 = **LiNbO₃ 10⁻¹¹ S cm⁻¹ 하나** (p.22970, [27] 인용).  argyrodite σ · NCM σ · 복합체 σ 모두 **미기재** | 없음 |
| 부피분율 의존 식 | **없다** — 유일한 식은 ee-연결 TLM 임피던스 식 (p.22974).  조성 의존은 정성 문장 하나: *"The ratio of the total ionic and electronic conductivities in the composite can be controlled by varying the volume fraction between NCM and argyrodite … resulting in the variation of capacitance and resistance"* (p.22968, [19]) | 없음 |
| 데이터로 만들 수 있나 | 측정 조성 = **1:1 v/v 하나** → 계수 2 개짜리 ε_s 직선의 데이터원이 될 수 없다 | 불가 |
| 역산 시도 (우리 산술) | 8.5×10⁻⁴ S cm⁻¹ 은 R = 28.19 Ω 에 해당 (σ = T/(R·A)).  가장 가까운 SI 값 = 베어 R_e (1.4 h) 27.86 Ω → 8.60×10⁻⁴ · 베어 R_i (0 h) 27.51 Ω → 8.71×10⁻⁴ | **재현 안 됨** — 둘 다 원문에 σ 로 적힌 적이 없고, 복합체 (NCM+SE 1:1) TLM 의 'bulk' 레일 성분 (전자 · 이온) 이며 NCM 고유값이 아니고, 시점이 임의다 = 우연의 근접 |
| 그 σ 는 고유인가 유효인가 | 이 논문이 줄 수 있는 σ 는 전부 **복합체 유효값** (1:1 · 295 MPa · 25 °C · 입계 · 계면 포함) 이다 | 만약 이런 값을 고유 σ₀ 로 썼다면 미세구조 벌점의 이중계상이겠지만 — 값 · 식이 원문에 없으므로 **이 경로는 성립하지 않는다** |
| 크기 대조 (우리 산술) | Park 식 = ε_s 0.5 에서 **2.42 mS cm⁻¹** (60–90 wt% 설계 ε_s 로 3.08 → 2.44, park2020 카드) ↔ 이 논문 복합체 유효 σ_i (1:1, t = 0) **0.080 · 0.101 mS cm⁻¹** | Park 식은 이 논문류 복합체 유효값보다 **24–30 배** 크다 → 복합체 유효값을 옮긴 것일 수 없다.  크기로는 펠릿 · 고유 수준 (우리 σ₀ 3.0 과 같은 자릿수).  조성 기울기 (ε_s 0.35 → 0.49 에서 −21 %) 의 근거는 여전히 미상 — 이중계상이 있더라도 그 기울기 몫 (≈ 20 %) 에 한정된다 (추론) |
| [18a–c] 종합 | 18a Wang 2018 — 8.5×10⁻⁴ 없음 · LPSCl 식 없음 (park2020 카드 §4 · `wang2018_…` 카드 기준, 원문 재대조는 그 카드 소관) · **18b 이 논문 — 없음 (원문 전수)** · 18c Froboese 2019 — 없음 (froboese 카드 원문 전수) | **각주 b 가 인용한 세 문헌 어디에도 두 값이 없다** |
| 남는 후보 | Table S2 각주 b 의 [16d] Li 2020 J. Energy Chem. 40, 39 (park2020 카드 — 미대조) · 각주 a *"Parameters set in cell design or by experiments"* (= 저자 자체 측정, 미공개) | `[미확인]` 유지 |
| 다음 대조 (추론) | 이 논문이 조성 의존 · 1:1 펠릿 설계의 근거로 인용한 ref 19 **Asano 2017** (NCM111–Li₃PS₄, 이번 묶음 #23 · 같은 묶음 카드 `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`) — 단 **Park 2020 은 Asano 를 인용하지 않는다** (park2020 카드 grep 0 건) · 그 카드에도 Park 식 · 8.5×10⁻⁴ 언급은 없다 (낱말 grep) | Park 식 출처로 잇는 근거는 없다 — 조성 의존 σ 실측의 형태 참고일 뿐 |

- **결정 4 (σ₀ 기준 상태)** — 이 논문은 σ₀ 를 줄 수 없다 (순수 펠릿 없음 · 단일 조성 · 복합체 유효값만).  대신 감도식 (§ τ 정의 대조 판정 4) 이 **σ₀ 를 다른 재료에서 빌리면 tau2 가 3 배 흔들린다**는 것을 숫자로 보인다 → "같은 재료 · 같은 압밀의 σ₀ 짝" 요구 강화.  권고 **불변**.
- **메모 v2 §3-4 (Park 역산 = "추세 전용")** — **유지**.  한정어 보강 제안: *"Park σ₀ 는 인용 문헌 [18a–c] 어디에도 없는 모형 입력 (출처 미상) — 크기는 펠릿 수준 (2.4–3.1 mS cm⁻¹)"*.  Park 식과 우리 3.0 이 60–80 wt% 에서 3.08–2.64 로 끼어 있어 σ₀ 판 차이는 ≤ ≈ 14 % (tau2 ∝ σ₀ → 3.0/3.08 · 3.0/2.84 · 3.0/2.64 = 0.97 · 1.06 · 1.14, 파생 · 메모 v2 §3-4 표 4.4 / 11 / 19 ↔ 4.3 / 11 / 21) — 역산의 큰 불확실성은 σ₀ 값보다 **출처 · 조성 기울기 · NBR · 입경비** 쪽에 있다.

### 이온 전도 측정 · "입계 이온 전도 감소" 의 정량 · 접촉 손실 — 우리 σ₀ (3.0 mS/cm 펠릿값) 와 복셀 계면 저항 트랙 (CL-81 ① r_int) 에 주는 의미

| 물음 | 이 논문 (쪽) |
|---|---|
| 시료 | 베어 또는 LiNbO₃ 코팅 Ni-rich NCM + argyrodite (Mitsui) **1:1 v/v**, 탄소 · 바인더 없음 (p.22974) |
| 성형 / 측정 압력 | 성형 **295 MPa · 2 min** → 320 µm · 측정 중 "constant pressure" (그림 1a) — **값 미기재** (p.22968 · p.22974) |
| 온도 | **25 °C** (p.22974) |
| 방법 | PEIS 1 MHz – 10 mHz · 10 mV · SUS \| 복합체 \| SUS (ee-연결 · 이온 차단) · TLM 두 단계 적합 · 1.5 h 간격 · 0–40.6 h (p.22969 · p.22974) |
| 순수 SE 펠릿 σ | **측정 · 보고 없음** |
| 복합체 유효 σ_i (파생) | 베어 0.0795 → 0.0327 mS cm⁻¹ (**−59 %**, 40.6 h) · 코팅 0.1014 → 0.0920 (**−9 %**) |
| 입계 이온 저항 | 베어 273.99 → 663.25 Ω (**+389 · ×2.42**) · 코팅 219.22 → 239.92 Ω (+21 · ×1.09) (SI · 그림 2j) |
| 입계 몫 (이온) | t = 0: 91 % (베어) · 93 % (코팅) — 숙성 중에도 89–93 % (파생) |
| 접촉 손실 증거 | ① 40 h 뒤 단면 SEM: 베어 = *"physical cracks and contact loss"*, 코팅 = 밀착 유지 (그림 1e–h, p.22968) ② 입계 C 감소 (C_i ×0.25 · C_e ×0.27, 베어) — 원문은 *"permittivity of the interface and interparticle distance"* 둘 다 가능하다고 적고 형상 변화 쪽으로 읽음 (p.22971) ③ 무가압 진공 in situ SEM 5 일: 베어에서 균열 생성 · 확대 (SI 그림 S4) — *"chemically induced physical degradation, which must be confirmed further"* (p.22971) |

**우리에게 주는 의미**
1. **σ₀ (3.0 mS/cm, 펠릿값)**: 이 논문은 σ₀ 를 주지도, 비교 기준이 되지도 않는다.  정성적으로만 — "펠릿 σ₀ 에 펠릿 수준 입계가 이미 들어 있다 (`CL-91`)" 는 우리 서술과 같은 맥락에서, 복합체를 등가회로로 나누면 **비-bulk (입계) 몫이 이온 저항의 ≈ 90 %** 다.  수치 이식은 하지 않는다.
2. **r_int (CL-81 ①)**:
   - (a) **크기 앵커가 아니다** — 접촉 면적 · 접촉 수 · 기하가 없어 r [Ω cm²] 로 바꿀 수 없다.
   - (b) **정성 지지** — 실물 복합체 (295 MPa 냉간 압밀 · t = 0) 에서 비-bulk 이온 항이 bulk 항의 ≈ 11–14 배 (등가회로 분해) — 계면 항이 0 인 연속체 · 복셀 σ (CONTACT_FREE 가지) 는 실물 저항의 큰 몫을 빠뜨릴 수 있다는 방향.
   - (c) **그 항은 시간 · 화학 의존**이다 — 무코팅 +389 Ω / 40.6 h (×2.4) vs 코팅 +21 Ω (×1.09).  ⇒ r_int 를 복합체 EIS 에 맞출 날이 오면 **코팅 · 숙성 시간 · 측정 시점**을 같은 칸에 적어야 한다.  우리 DEM · 복셀 기하는 **숙성 0** 에 해당한다.
   - (d) **이중계상 경고** — 복합체 EIS 의 입계 항을 r_int 로 옮기면 펠릿 σ₀ 안에 이미 있는 SE–SE 입계를 다시 센다.  이 논문에는 순수 펠릿 스펙트럼이 없어 그 몫을 빼 줄 수 없다 (CL-81 ① 6 단계 중 ④ "입력 σ 내부값 규약" 과 같은 문제).
   - (e) 이 논문의 "입계" 는 SE–SE · SE–NCM · NCM–NCM 을 가르지 않는다 — 원문은 이온 입계의 자리를 지정하지 않고, 전자 입계만 *"grain boundaries at the cathode–cathode or cathode–electrolyte interface"* 로 적는다 (p.22970).  NCM 자신의 이온 전도도 이온 레일에 섞인다 (p.22968).
3. **우리 FULL/CF 와 숫자를 맞대지 않는다** — (R_i + R_i,gb)/R_i = 11.0 · 13.8 은 CPE α 0.41–0.54 의 **등가회로 분해비**이고, 우리 FULL/CF 는 같은 접촉망 안의 **모델 내부 협착 비** (결정 11 의 이름) 다.  `SELF-24` · `L2-07` (kim2025 GB-only 3.75× ↔ 4.04 인용 금지) 과 같은 부류의 비교 금지.
4. **화학 유발 접촉 손실은 우리 모델 밖 (축 F)** — DEM 접촉은 압밀 직후 상태이고, Auerbach 파괴는 역학, A10 접촉 원장은 사이클 수축 개구다.  SOC 0 화학 반응이 접촉을 끊는 경로는 어디에도 없다.

### 결정별 인사이트 (메모 v2 §0-2 결정 번호)
- ① **결정 4 · 메모 §3-4** — 위 "Park σ₀ 조성식의 출처" 판정.  [18a–c] 소진 → Park σ₀ = 출처 미상 모형 입력 · 크기는 펠릿 수준 · "추세 전용" 유지.  권고 **불변** (한정어 보강만).
- ② **결정 11 (CF 지위) · CL-81 ①** — 실물 복합체의 비-bulk 이온 항이 크고 (≈ 90 %) 화학 숙성으로 자란다는 정성 자료.  CF 이름표 ("모델 내부 기준선") · FULL/CF ("모델 내부 협착 비") 결정과 충돌하지 않는다 — 오히려 "등가회로 입계 몫 ≠ 협착 비" 를 한정어로 더할 근거.  권고 **불변**.
- ③ **결정 13 (τ_e) · 결정 5 (COMSOL 표기)** — 두 번째 T형 실측 사례 (Minnmann 다음).  ee-연결 = 관통형 → τ_e 아님.  "tau2 에 EIS 를 붙일 때 연결형 병기" (앞 묶음 부록 결정 5 한정어) 의 예.  추가 한정어 제안: *"ee-연결 (이온 차단 집전체) TLM 의 이온 저항은 직류가 아니라 고주파 결합에서 적합으로 얻는다 — 관통 꼴이지만 모형 의존"*.  권고 **불변**.
- ④ **결정 14 (전자 · 열)** — 탄소 없는 NCM:SE 1:1 복합체의 전자 유효 σ (파생) 0.33 mS cm⁻¹ (베어) · 0.075 (코팅) · 코팅 수 nm 가 전자 입계 저항을 5.9 배 키우고 bulk 전자는 그대로 (21.69 ↔ 21.29 Ω) → AM–AM 전자 접촉항은 **표면층 (코팅 · 반응층)** 이 지배한다.  "GB 인자를 T 에 흡수" 할 때 표면 막도 흡수 대상임을 적을 것.  권고 **불변**.

## 9. 인용 가능 문장 (deck/paper용)
- "Jung et al. aged carbon-free NCM–argyrodite composite pellets (1:1 v/v, 295 MPa) at SOC 0 and separated the bulk and grain-boundary ionic and electronic resistances with an electron–electron (ion-blocking) transmission-line model; after about 40 h the ionic grain-boundary resistance increased by 389 Ω for bare NCM but only by 21 Ω for LiNbO₃-coated NCM (J. Mater. Chem. A 7 (2019) 22967, Fig. 2j)."
- "The paper reports no ionic conductivity of the solid electrolyte or of the composite, no electronic conductivity of NCM and no composition-dependent conductivity relation; the only conductivity value it gives is that of LiNbO₃ (10⁻¹¹ S cm⁻¹, cited from the literature)."
- "Converted with the reported pellet thickness (0.0318 cm) and area (1.327 cm²), the fitted ionic resistances correspond to composite effective ionic conductivities of about 0.08 (bare) and 0.10 mS cm⁻¹ (coated) at t = 0 — our arithmetic, not values stated in the paper."
- "The transmission-line expression used has the form of Siroma's T-type open–open solution with the electronic rail as the terminal rail; its low-frequency limit contains only the electronic resistance, so the ionic resistances follow from the high-frequency coupling of the two rails and are therefore model-dependent."

## 10. 주의/한계 (over-claim 방지)
- **σ 값 없음** — 이 카드 §3-4 의 σ 는 전부 파생 (σ = T/(R·A)) 이다.  원문 값처럼 인용하지 말 것.
- **재료 미상** — SE 조성식은 그림 표지 (Li₆PS₅Cl) 로만 · Mitsui 제품의 σ 미상 · NCM 은 "Ni-rich" (조성 · 입경 · 2 차 / 단입자 비율 미기재).
- **기공률 · 밀도 · 질량 미보고** — φ_SE 는 명목 1:1 v/v (고체 기준) 뿐.  게다가 "1:1 v/v (7:2 w/w)" 는 ρ_NCM/ρ_SE = 3.5 일 때만 같고, 다른 정본 카드 밀도로는 7:2 w/w = SE 38–42 vol% → φ_SE 가 0.38–0.50 사이에서 불확정 (파생).
- **단일 조성 · 단일 압력 · 단일 온도** (1:1 · 295 MPa · 25 °C) · 조건당 셀 수 · 반복 **미기재** · 그림 2(b)(c) 의 ± 는 적합 오차.
- **측정 압력 미기재** — "constant pressure" 뿐 (EIS 셀) · 갈바노 셀은 4 N·m 토크 (MPa 환산 없음).
- **등가회로 분해의 한계** — 레일 CPE α 0.41–0.54 (이상 축전기와 먼 분포 응답) · bulk 값은 측정창 (1 MHz) 밖 외삽을 포함 (§3-7) · 이온 저항은 고주파 결합에서만 정해진다 (직류 극한 = 전자뿐, §4-1) · "입계" 의 물리적 자리 (SE–SE / SE–NCM / NCM–NCM) 미지정 · 이온 레일에 NCM 이온 전도 포함.
- **두 단계 적합의 불일치** — 이온 합 301.50 Ω (그림 2b) ↔ 324.83 Ω (그림 2c), 7.7 % (p.22970).
- **같은 SE · 같은 조성인데 t = 0 값이 갈린다** — 이온 bulk 27.51 vs 17.10 Ω (×1.61) · 이온 입계 273.99 vs 219.22 Ω (×1.25) (베어 vs 코팅).  원문은 *"initial resistance values are quite similar regardless of the coating layer, except … electronic grain boundary"* (p.22970) — 셀 간 · 적합 간 산포의 감각으로만 쓸 것.
- **k 값** — 직선 (Ω h⁻⁰·⁵) 과 포물선 (Ω h⁻¹) 이 단위가 달라 "입계가 bulk 보다 빠르다" 는 비교는 정성이다 · 맞춤식 · 가중 미기술 · SI 표 무가중 재현은 1–15 % 차 (§3-7).
- **C 의 입계 배정** — 원문은 C 범위 (10⁻⁸–10⁻⁷ F) 를 [28] 의 입계 범위와 대조하지만 기하 정규화 (l/A = 0.0240 cm⁻¹, 파생) 를 했는지 적지 않는다 · C 를 Q 에서 계산한 식도 미기재.
- **접촉 손실 증거의 한계** — in situ SEM (S4) 은 **무가압 · 진공 · 베어만** (코팅 대조 없음) → 화학 유발 균열과 압력 해제 · 진공 효과를 가르지 못한다.  원문도 *"must be confirmed further"* (p.22971).  C 감소는 계면 유전율 변화로도 설명될 수 있다고 원문이 적는다.
- **사이클 결과의 비교 축** — "83 % 유지" (형성 16 / 7 mA g⁻¹, 그림 4a) 와 "43 % 감소 as described before" (사이클 50 / 80 mA g⁻¹, 그림 4b) 는 다른 전류의 값이다 (p.22972–22973).  "aged for more than 5 days" (p.22972) ↔ Methods "5 days" (p.22974).
- **원문 표기 · 내부 불일치 (그대로 두고 표지만)**: TLM 식 단위 "[Ω cm]" 차원 오류 (p.22974 — Z_i · Z_e 는 Ω cm⁻¹ 이어야 함) · 본문 식의 L (두께) ↔ SI 표의 "L (H cm²)" (정의 없음) · SI 의 두께 기호 T · 셀 구성 *"Au/NCM + SE composite/Au"* (p.22969, [22] 인용 문장 — 인용 문헌의 셀 구성을 빌린 서술로 읽히나 구분 없음) ↔ SUS 판 (p.22974 · 그림 1a) · *"every 1.5 h"* ↔ 표 시점 1.4 h 배수 · *"(∼100 Ω)"* ↔ 72.3 Ω (SI) · SI Table S2 C_i (26.6 h) "1.28E-8" ↔ 그림 2(i) ≈ 1.28×10⁻⁷ (오식) · *"Except for the electrode composite containing bare NCM, a strong linear correlation…"* (p.22970) 인데 베어의 bulk 저항 둘은 √t 에 직선 (그림 2d · f — 예외는 입계 둘뿐) · *"Even the electronic and ionic grain boundary resistances of bare NCM have a parabolic relationship"* (어색한 "Even") · 그림 2(c) R_e,gb 50.65 ↔ SI 50.64 · 갈바노 전압 *"versus the reduction potential of Li"* 인데 상대극은 Li–In (환산 미기술).
- **시뮬레이션 없음** — DEM · MPM 어느 쪽의 검증도 아니다 (frame[4]: 실험 쪽 앵커 후보일 뿐, 이 계에서는 연결 조건 미충족).

### 10-1. 메모 v2 정정 후보 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`)
- **없음** — 메모 v2 는 이 논문 (Jung 2019 = park [18b]) 을 §8-2 "낮음" 목록에만 올렸고 내용 주장을 하지 않는다.
- (보강 · 정정 아님) **§3-4 한정어** — *"Park 의 σ₀ 는 측정 펠릿이 아니라 조성 의존 모형 입력이다"* 에 *"인용 문헌 [18a–c] (Wang 2018 · Jung 2019 · Froboese 2019) 어디에도 그 값 · 식이 없다 — 출처 미상 (각주 a 의 자체 측정 또는 [16d] 미대조)"* 를 더할 것을 제안 (§8 · 이 카드 p.22967–22976 · SI p.1–10 전수).
- (보강) 앞 묶음 부록 결론 ⑥ *"Froboese 2019 · Park 2019 · Park 2020 CEJ 셋 다 아니다"* 에 **Jung 2019 ([18b])** 를 더할 수 있다 — [18a–c] 셋이 소진된다.  (부록의 셋 중 Park 2019 · Park 2020 CEJ 는 Table S2 각주의 [12] 이고 Table S1 각주의 [18] 이 아니다 — 두 각주를 한 줄에 묶을 때 구분 표기 권장.)

### 10-2. 이 논문을 인용하는 카드와의 대조 (그 카드는 고치지 않는다 — 메인 판단)
- `park2020_digitaltwin_assb_foundational` 참고문헌 표 (l.878): 서지 *"[18] b) S.-K. Jung, H. Gwon, S.-S. Lee, H. Kim, J. C. Lee, J. G. Chung, S. Y. Park, Y. Aihara, D. Im, J. Mater. Chem. A 2019, 7, 22967"* — 원문과 **일치** (저자 9 명 · 권 · 쪽).  그 행의 기대 (*"NCM 8.5×10⁻⁴ 와 ε_s 의존 LPSCl σ 식의 출처 확인"*) 는 **원문에 없음으로 판정** → 행의 "정본 카드" 칸을 이 슬러그로, 메모를 "출처 아님 (원문 전수)" 로 바꿀 후보.  같은 카드 §4 (l.330) 의 *"(18b · 18c 미대조 …)"* 도 둘 다 대조 완료 (둘 다 없음) 로 갱신 후보.
- `froboese2019_microstructure_ionic_conductivity_assb_electrode` §8 (f) · §10 정정 후보 2 의 *"[18b] Jung 2019 J. Mater. Chem. A 미대조"* → 대조 완료 (없음) 로 갱신 후보.
- (참고 · 이 카드 범위 밖) `bazzoun2026_dem_fem_rnm_ionic` 표의 "Cronau 단결정 3.0" 표기는 CLAUDE.md `CL-91` (펠릿값 · "단결정" 라벨 철회) 과 어긋난다 — 이 카드의 §7 비교에는 Bazzoun 의 stated σ_eff 만 썼다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로, p.22975–22976) | 왜 | 정본 카드 |
|---|---|---|
| 19 T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi and M. Tatsumisago, Electronic and ionic conductivities of LiNi1/3Mn1/3Co1/3O2-Li3PS4 positive composite electrodes for all-solid-state lithium batteries, J. Electrochem. Soc., 2017, 164, A3960–A3963. | 이 논문이 조성 (부피비) 의존 · 1:1 펠릿 설계의 근거로 인용 (p.22968 두 곳) — 조성별 복합체 전자 · 이온 σ 실측 (메모 v2 §8-2) | 같은 묶음 #23 → `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` (정본 워크트리에 작성됨 · 커밋 전) |
| 22 Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota and T. Ioroi, AC impedance analysis of ionic and electronic conductivities in electrode mixture layers for an all-solid-state lithium-ion battery, J. Power Sources, 2016, 316, 215–223. | ASSB 전극 혼합층의 이온 · 전자 TLM 분석 — 이 논문의 R_ct · Warburg 제외 근거와 "Au/…/Au" 문장의 출처 · Kaiser 카드도 같은 논문을 "없음" 으로 기록 | 없음 |
| 23 Z. Siroma, N. Fujiwara, S.-i Yamazaki, M. Asahi, T. Nagai and T. Ioroi, Mathematical solutions of comprehensive variations of a transmission-line model of the theoretical impedance of porous electrodes, Electrochim. Acta, 2015, 160, 313–322. | 이 논문 식 = 표 3 T형 open–open | ✅ `siroma2015_transmission_line_model_porous_electrode_impedance` |
| 24 J. Jamnik and J. Maier, Treatment of the impedance of mixed conductors equivalent circuit model and explicit approximate solutions, J. Electrochem. Soc., 1999, 146, 4183–4188. | 혼합 전도체 TLM 의 원전 (두 레일 + 계면) | 없음 (`pouraghajan2018_…` 에 언급) |
| 25 N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato and B. Roling, Ion transport limitations in all-solid-state lithium battery electrodes containing a sulfide-based electrolyte, J. Power Sources, 2018, 396, 175–181. | 이 논문이 TLM 모델 선택의 근거로 인용 (p.22968) — ASSB τ_eff 두 방법 | ✅ `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` |
| 28 J. T. Irvine, D. C. Sinclair and A. R. West, Electroceramics: characterization by impedance spectroscopy, Adv. Mater., 1990, 2, 132–138. | C 크기 → 입계 배정의 근거 (정규화 관례 확인 필요) | 없음 |
| 11 S. Wenzel, et al. Direct observation of the interfacial instability of the fast ionic conductor Li10GeP2S12 at the lithium metal anode, Chem. Mater., 2016, 28, 2400–2407. · 26 S. Wenzel, S. J. Sedlmaier, C. Dietrich, W. G. Zeier and J. Janek, Interfacial reactivity and interphase growth of argyrodite solid electrolytes at lithium metal electrodes, Solid State Ionics, 2018, 318, 102–112. | R ∝ √t 확산 지배 계면층 성장 모형의 출처 | 없음 |
| 13 F. Walther, et al. Visualization of the Interfacial Decomposition of Composite Cathodes in Argyrodite-Based All-Solid-State Batteries Using Time-of-Flight Secondary-Ion Mass Spectrometry, Chem. Mater., 2019, 31, 3745–3755. | 사이클 뒤 산물 · SIMS CEI 두께 방법 (NiO 포화) | 없음 |
| 12 R. Koerver, et al. Capacity fade in solid-state batteries: interphase formation and chemomechanical processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid electrolytes, Chem. Mater., 2017, 29, 5574–5582. · 29 R. Koerver, et al. Chemo-mechanical expansion of lithium electrode materials–on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci., 2018, 11, 2142–2158. | Ni-rich NCM 계면 · 화학–기계 열화 · 가압 해제 이완 (in situ SEM 의 동기) | 없음 |
| 14 J. Auvergniot, A. Cassel, J.-B. Ledeuil, V. Viallet, V. Seznec and R. Dedryvère, Interface stability of argyrodite Li6PS5Cl toward LiCoO2, LiNi1/3Co1/3Mn1/3O2, and LiMn2O4 in bulk all-solid-state batteries, Chem. Mater., 2017, 29, 3883–3890. · 33 J. Auvergniot, A. Cassel, D. Foix, V. Viallet, V. Seznec and R. Dedryvère, Redox activity of argyrodite Li6PS5Cl electrolyte in all-solid-state Li-ion battery: An XPS study, Solid State Ionics, 2017, 300, 78–85. | 사이클 뒤 XPS 산물 (아황산 · 황산) — 화학 숙성 산물과의 대조 축 | 없음 |
| 15 Y. Xiao, L. J. Miara, Y. Wang and G. Ceder, Computational Screening of Cathode Coatings for Solid-State Batteries, Joule, 2019, 3, 1252–1275. | LiNbO₃ 계면 안정성 DFT (p.22972) | ✅ `xiao2019_cathode_coating_screening` |
| 10 Y. Zhu, X. He and Y. Mo, Origin of outstanding stability in the lithium solid electrolyte materials: insights from thermodynamic analyses based on first-principles calculations, ACS Appl. Mater. Interfaces, 2015, 7, 23685–23693. | 황화물의 좁은 전기화학 창 | ✅ `zhu2015_esw_grand_potential_origin` |
| 17 R. P. Rao and S. Adams, Studies of lithium argyrodite solid electrolytes for all-solid-state batteries, Phys. Status Solidi A, 2011, 208, 1804–1807. | argyrodite 선택 근거 | ✅ `rao2011_argyrodite_se_studies_bvse` |
| 18 N. Ohta, et al. LiNbO3-coated LiCoO2 as cathode material for all solid-state lithium secondary batteries, Electrochem. Commun., 2007, 9, 1486–1490. · 27 K. Benaissa, P. Ashrit, G. Bader, F. E. Girouard and V.-V. Truong, Electrical and optical properties of LiNbO3, Thin Solid Films, 1992, 214, 219–222. | LiNbO₃ 코팅의 원조 · LiNbO₃ σ 10⁻¹¹ S cm⁻¹ 의 출처 | 없음 |

- 정본 카드 유무 = `litdb/papers/` 파일 목록 + 낱말 grep 으로 확인 (2026-10-03).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- 본문 10 쪽 · SI 10 쪽 **전부** 렌더로 읽었다 (식 · 그림 1–4 · SI 그림 S1–S6 · 표 S1–S2).  그림 1(c) · 2(b)–(j) 는 확대 판독.
- SI 표의 차로 그림 2(j) 의 여덟 증가값을 소수점까지 재현 · A = π(0.65 cm)² = 1.3273 ↔ 표 1.327 · T 0.0318 cm ↔ 본문 320 µm.
- TLM 식을 Siroma 2015 표 3 T형 open–open (siroma2015 카드 전사) 과 항별 대조 → z_A = Z_e · z_C = Z_i · z_B = Z_cpe 로 일치 · 두 극한 (직류 L·Z_e · 고주파 병렬) 유도.
- 텍스트 검색 ("S cm" · "conductiv" · "volume fraction" · "volume ratio" · "8.5" · "tortuos" · "porosity" · "density"): S cm⁻¹ 수치는 LiNbO₃ 10⁻¹¹ 하나 · "tortuos" 0 건 · 기공률 0 건.
- 본문 · SI 어디에도 없는 것: SE · NCM · 복합체의 σ 값 · NCM 조성 · 입경 · PSD · 기공률 · 펠릿 질량 · 재료 밀도 · 측정 중 압력값 · 적합 소프트웨어 · 반복 수 · 순수 SE 펠릿 측정 · τ.

## 이 논문을 인용하는 corpus 카드
- `park2020_digitaltwin_assb_foundational` — [18] b (SI Table S1 각주 b "Parameters based on literature[18a-c]" · Table S2 각주 b "[12, 16d, 18]").  기대된 두 값은 이 논문에 없다 (§8).
- (언급) `froboese2019_microstructure_ionic_conductivity_assb_electrode` §8 (f) — "[18b] 미대조" 로 남겨 둔 항목.
- (메모) 메인 리포 `docs/reviews/tau_conventions_judgment_v2_20261003.md` §8-2 "낮음" 목록의 "Jung 2019 (park [18b])".

## Q&A 로그
- (아직 없음)
