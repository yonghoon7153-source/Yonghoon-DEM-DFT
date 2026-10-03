<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md.
     τ 묶음 형식 기준 = tjaden2018_tortuosity_review_calculation_approaches.md · landesfeind2016_tortuosity_eis_electrodes_separators.md · taufactor_tortuosity_factor_tomography_tool.md.
     쪽 표기 = 학술지 인쇄 쪽 (본문 PDF n 쪽 = 인쇄 362+n 쪽 · p.363–370).  SI 는 "SI p.n" (SI PDF 쪽 = SI 인쇄 번호 1–5).
     식·표·그림 번호 = 원문 번호.  수식·표·그림 쪽은 원문 PDF 를 그림으로 렌더해 대조했다 (텍스트 추출은 τ→t, ε→1 로 깨진다).
     값 표지: stated = 본문·캡션·표 원문 / 판독 = 그림에서 읽은 근사 (TREND 전용, 정밀값으로 쓰지 않음) / 우리 산술 = 원문 숫자로 이 카드가 계산 (식 명시) / [미확인] = 원문에 없음. -->
# 복합 양극의 잔류 공극(void)이 SE 이온 수송 tortuosity 를 키운다 — 전자차단 대칭셀 EIS τ_cond 1.6 · FIB-SEM 재구성 random-walk τ_diff 1.74 · void 를 SE 로 채우면 1.27 — Hlushkou (J. Power Sources 2018)

> slug `hlushkou2018_void_space_ion_transport_assb_cathode` · DOI `10.1016/j.jpowsour.2018.06.041` · type `mixed (exp: Li/SE/복합양극/SE/Li 전자차단 대칭셀 EIS Warburg-short · sim: FIB-SEM 3상 재구성 + random-walk 입자추적 확산 (복셀 연속체, 접촉 저항 항 없음) — ASSB 복합양극 tortuosity factor)` · PDF `6. The influence of void space on ion transport in a composite cathode for all-solid-state batteries.pdf` · digested `2026-10-03` · status ✅
>
> SI = `6. Sup) The influence of void space on ion transport in a composite cathode for all-solid-state batteries.pdf` (5 쪽 — 표지 · 영상 복원 6 단계 · void/LCO 분할 절차 · 유한크기 분석 · Fig. S1 · 참고문헌 5).  본문 8 쪽 + SI 5 쪽 **전부 읽었다**.
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 두 τ 는 **둘 다 제곱 없는 tortuosity factor = 우리 tau2** 다.
> ① **τ_cond = (σ_ion,electrolyte / σ_ion,composite)·ε** (Eq. 3, p.364) — 이름 *"ionic conductivity-based tortuosity"* ("factor" 낱말 없음).
> 실험 = **직류 관통 (flow-through) 이온 저항** R_ion (전자는 SE 층이 막는다) · σ_comp = d/(R_ion·A) 전체 단면 (Eq. 1) · **σ₀ = 순수 LPSI 펠릿 0.7 mS/cm @25 °C** (276 MPa 30 min, p.365).
> ② **τ_diff = D_ion,electrolyte / D_ion,eff** (Eq. 9, p.368) — *"diffusive tortuosity"*.  FIB-SEM 재구성 SE 상 안의 random walk 장시간 확산계수 (상 내부 평균) — **접촉 저항 항 없는 복셀 연속체** · **기준 = 벌크 SE 확산계수 (연속 매질 — 펠릿 아님; SE 는 비정질이라 '결정립' 이 없다)** · MSD/6 = **등방 평균** (관통 z 아님).
> ③ **τ_B = ε^−0.5** (p.369, Bruggeman) = Landesfeind α = 0.5 관례 = 우리 φ^−½.  **√ 값 (우리 tau) 과 기하 τ_geo 는 이 논문에 없다.**
>
> ★ **닫는 것 (§8-0 "전고체 복합 양극 τ 의 두 번째 절대 앵커 후보")** — 답: **조건부 한 점 · 재료계가 다르다** (Li₂S–P₂S₅–LiI 유리 + LiNbO₃ 코팅 LCO ~5 µm · 한 조성 φ_SE 0.537–0.62 · ε 장부 미기재).
> 결정 4 뒤 **판정선 앵커로는 약하다** (LPSCl 앵커 = Minnmann 유지) — 대신 **방법·기전 기준점**으로 값이 있다: (a) 접촉 저항 없는 복셀 연속체 τ 와 펠릿 기준 EIS τ 를 **같은 논문에서** 비교한 ASSB 선례 (결정 11),
> (b) **void 13.2 vol% (수지 포함)** 가 τ 를 1.27 → 1.74 (×1.37) 로 올린 반면 Bruggeman 은 1.22 → 1.34 만 예측 — 공극의 **자리 (형태)** 가 부피보다 크게 작용한다.

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (식·쪽) |
|---|---|---|
| 이 논문의 τ 는 τ² 계열 (tortuosity factor) 인가, √ 인가, 기하인가? | **tortuosity factor (= 우리 tau2)**.  τ_cond 는 ε·σ₀/σ_eff, τ_diff 는 D₀/D_eff(상 내부) — 두 식이 같은 양임을 Eq. 9 가 직접 적는다 | Eq. 3 (p.364) · Eq. 9 (p.368) |
| τ_cond 의 σ₀ 는? | **순수 LPSI 펠릿** 0.7 mS/cm @25 °C (6 mm, 276 MPa 30 min, 양면 Au 전극) — 펠릿 자신의 입자 접촉·잔류 기공을 품은 값 | p.365 |
| τ_diff 의 기준은? | D_ion,electrolyte = **벌크 SE 확산계수** (분할된 SE 상 = 연속 매질, 입계·접촉 없음).  τ_diff 는 그 값과 무관한 순수 기하-수송 인자 | Eq. 9–11 (p.368) |
| 측정값 | **τ_cond = 1.6 ± 0.1** (R_ion 97 ± 2 Ω, d 208 ± 5 µm) | p.366 · Fig. 2 |
| 시뮬값 (공극 포함 실제 구조) | **τ_diff = 1.74** (D_eff/D₀ ≈ 0.574, φ_SE 0.537, void+수지 13.2 %) | p.368 · Fig. 7 |
| 시뮬값 (void → SE 가상 치환) | **τ_diff = 1.27** (D_eff/D₀ 0.786, φ_SE 0.669) — D_eff **+37 %** | p.369 · Fig. 6B · Fig. 7 |
| Bruggeman (τ_B = ε^−0.5) | 1.22 (ε 0.669) ≈ 가상 구조 1.27 / **1.34** (ε 0.537, 원문 값 — 우리 검산 1.365) ≪ 1.6–1.74 | p.369 |
| 공극 효과의 기전 | 공극이 SE 상을 **잘게 끊어** 가늘고 굽은 경로를 많이 만든다 — CLD 평균 폭 μ: interparticle 9.4 → SE 5.2 µm, k_SE 1.54 (불균질) | p.369 · Table 3 (p.367) |
| 두 τ 의 "근접" (1.74 vs 1.6) 은 깨끗한가? | **아니다.**  시료가 다르고 (FIB 시료만 에폭시 수지), ε 장부가 다르며 (시뮬 0.537 ↔ EIS 의 ε 값 원문 없음 — 우리 역산은 공칭 0.62 쪽), 기준 상태 (벌크 연속체 D ↔ 펠릿 σ) 와 방향 (등방 ↔ 관통) 이 다르다.  **f = σ_eff/σ₀ 로 보면 복셀 쪽이 EIS 보다 ≈ 20–24 % 낮다 (우리 산술)** | §3-F · §8-0 |
| 우리 양 매핑 | τ_cond ↔ `tau2_ion_<mode>` 의 실험 짝 (관통 · 접촉 포함, σ₀ = 펠릿) · τ_diff ↔ STEP3 복셀 CF 계열 (`vox_cf`, 등방) · τ_B ↔ φ^−½ | § τ 정의 대조 |

---

## 1. 한 줄 요약
Li₂S–P₂S₅–LiI 유리 SE (LPSI) 와 LiNbO₃ 코팅 LiCoO₂ (~5 µm) 로 만든 **전고체 복합 양극 하나** (LCO:SE = 59:41 wt% = 38:62 vol%) 의 이온 수송 tortuosity 를 **두 독립 경로**로 구했다 —
① **Li / LPSI / 복합양극 / LPSI / Li 대칭셀 EIS**: 저주파에서 전자가 SE 층에 막혀 복합체 안 Li⁺ 가 SE 상으로만 관통하므로, Warburg-short 적합으로 **직류 이온 저항 R_ion** 을 얻고 **τ_cond = 1.6 ± 0.1** (Eq. 1·3);
② **FIB-SEM 재구성** (35.6 × 35.6 × 100 nm³, 55.9 × 38.9 × 58.1 µm³, LCO · SE · void 3상) 위에서 **random-walk 입자추적** (10⁷ 추적자, SE–LCO · SE–void 면 다중거부 경계) 으로 **τ_diff = 1.74**.
둘이 가깝다고 보고하고 (차이 = FIB 시료에만 넣은 안정화 수지 탓으로 귀속), **void 를 SE 로 채운 가상 구조**에서 τ_diff 가 **1.27** 로 떨어지며 Bruggeman (1.22) 과 맞는 반면, 실제 구조에서는 Bruggeman (1.34) 이 크게 과소평가함을 보인다.
결론: 공극은 SE 부피분율만 줄이는 것이 아니라 **SE 상의 형태를 가늘고 굽은 통로로 바꾼다** → 부피분율만으로 수송을 예측할 수 없고, **ASSB 전극 제조에서 잔류 공극량에 주의**해야 하며 SE 분율이 더 낮은 (고에너지) 전극에서는 문제가 더 커질 것이라 추정한다 (p.369).

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Dzmitry Hlushkou**, Arved E. Reising, Nico Kaiser, Stefan Spannenberger (Philipps-Universität **Marburg**, 화학과) · Sabine Schlabach (KIT 응용재료연구소 · Karlsruhe Nano Micro Facility) · Yuki Kato (Toyota Motor Europe, Advanced Technology 1 Division) · Bernhard Roling · **Ulrich Tallarek** (교신, Marburg) | **J. Power Sources 396 (2018) 363–370** | **10.1016/j.jpowsour.2018.06.041** | SE = **비정질 0.67 (0.75 Li₂S – 0.25 P₂S₅) – 0.33 LiI ("LPSI")** · AM = **LiCoO₂** (Toda, 평균 ~5 µm, LiNbO₃ ~12 nm 코팅) · 탄소·바인더 **없음** | **mixed** — 실험 (EIS 대칭셀) + 3D 물리 재구성 (FIB-SEM) + 공극 규모 확산 시뮬 (random walk) |

- 접수 2018-02-27 · 수정본 2018-06-07 · 수리 2018-06-10 · 온라인 2018-06-16 (p.363).  © 2018 Elsevier (OA 표기 없음).
- 연구비: **Toyota Motor Corporation (Japan)** · Li 분말 Rockwood Lithium · 단층촬영 = KNMF 장기 사용자 과제 2017-019-020749 (p.369).
- 키워드: All-solid-state battery · Composite cathode · Ion transport · Tortuosity · Physical reconstruction · Random-walk method (p.363).
- 그룹 계보: Tallarek 그룹의 크로마토그래피 충전층·모놀리스 재구성/CLD/random-walk 도구 ([24–31], [36–37]) 를 ASSB 양극에 옮긴 것 — 방법의 검증 이력은 **이전 논문들**에 있다 (p.368 "confirmed by comparing … [36,37] … [38]").
- 정본 카드 대조: 이 논문을 인용하는 정본 카드 = `minnmann2021_jes_charge_transport_bottlenecks` ([43]) · `bielefeld2019_microstructural_modeling_composite_cathode` (ref 16) · `bielefeld2020_effective_ionic_conductivity_binder` (void 가정의 출처로).  이 논문 자신의 카드는 없었다 (파일 목록 + DOI 검색, 2026-10-03).

---

## 3. 핵심 수치

### 3-A. 재료 · 공정 (stated, 쪽)

| 항목 | 값 | 쪽 |
|---|---|---|
| SE 조성 | 비정질 0.67 (0.75 Li₂S – 0.25 P₂S₅) – 0.33 LiI (LPSI) — Li 금속과 안정한 전자절연 계면상 형성 [23] | p.365 |
| SE 전도도 (σ₀) | **σ₂₅°C = 0.7 mS/cm** ("overall ionic conductivity") | p.365 |
| SE 합성 | 유성 볼밀 Pulverisette 7 · ZrO₂ 20 ml 용기 · ZrO₂ 볼 10 mm × 10 개 · **700 rpm 약 8 h** (5 min 분쇄 · 20 min 휴지 · 99 회) | p.365 |
| σ₀ 측정 펠릿 | 6 mm · **276 MPa · 30 min · 실온** · 연마 스테인리스 압출 다이 · 두께 = 마이크로미터 · 양면 Au 스퍼터 · Alpha-AK, 1 MHz–0.1 Hz, 10 mV_rms, −120 ~ 160 °C (±1 °C) | p.365 |
| SE 밀도 | 2.2 g/cm³ | Table 1 (p.365) |
| SE 입경 · 펠릿 밀도 · E · σ_y | **[미확인]** (원문 없음) | — |
| LCO | Toda, 평균 **~5 µm**, LiNbO₃ **~12 nm** 코팅 (서론 일반론은 "~10 nm" [8]) · 밀도 5.1 g/cm³ | p.364–365 |
| 양극 조성 (Table 1) | LCO **59 wt% = 38 vol%** · SE **41 wt% = 62 vol%** (탄소·바인더 없음).  우리 검산 (59/5.1)/(59/5.1 + 41/2.2) = 0.383 ✓ | p.365 |
| 혼합 | Vortex 10 min → 자작 저에너지 볼 혼합기 (3 mm ZrO₂) 하룻밤 — LiNbO₃ 코팅을 깨지 않는 연한 혼합 (서론 p.364 의 동기) | p.364–365 |
| 음극 (전지 조립용, Table 2) | Li₄Ti₅O₁₂ / SE / Super C65 = 30 / 60 / 10 wt% = 21 / 66 / 13 vol% · 유성밀 150 rpm (5 min · 5 min 휴지 · 10 회) | p.365 |
| 셀 틀 | **코런덤 관 내경 9.8 mm** + 스테인리스 압출 다이 | p.365 |
| 대칭셀 제작 | ① LTO 음극 / LCO 양극 완전 전지 조립 → 부분 충전 (AM ≈ **Li₀.₇₁CoO₂**) ② 음극을 Dremel 로 갈아 제거 ③ 양면에 SE 층 → **4 t cm⁻² · 5 min** ④ 양면 Li 분말 → **1 t cm⁻²**.  (우리 환산, tonne-force 가정: 4 t cm⁻² ≈ **392 MPa**, 1 t cm⁻² ≈ 98 MPa) | p.365 |
| EIS | Autolab PGSTAT302N · OCP 정전위 · **500 kHz – 0.3 mHz** (본문) / **1 MHz – 0.3 mHz** (Fig. 2 캡션) · 10 mV_rms · RelaxIS 적합 | p.365 · p.366 |
| 두께 | 측정 후 에폭시 (Specifix 40) 매립 → 띠톱 절단 → 광학 현미경 (Leica DM 2700 M) 단면 → **d = 208 ± 5 µm** | p.365 · Fig. 2 (p.366) |
| FIB 시료 | 양극 혼합물 37.7 mg + **에폭시 수지** 기계 혼합 → 0.95 cm 펠릿, **4 t cm⁻² · 14 h** (수지 경화) · 한쪽에 스테인리스 프릿 (VICI JR-5FR6-5, 0.95 cm · 1.02 mm · 기공 0.5 µm) | p.365 |
| EIS 측정 온도 · 측정 중 적층압 · SE 층 두께 · 최초 전지 조립 압력 | **[미확인]** | — |

### 3-B. EIS → τ_cond (stated + 판독 + 우리 산술)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 고주파 | 2R_electrolyte + 반원 (셀 계면 임피던스 Z_interfaces 로 추정 — "most likely") | stated, p.365–366 |
| 저주파 | Warburg-short 거동 (Eq. 6) | stated, p.366 |
| **R_ion** | **97 ± 2 Ω** (Eq. 6 저주파 적합) | stated, p.366 |
| **τ_cond** | **1.6 ± 0.1** (Eq. 1 · 3) | stated, p.366 · p.369 |
| Nyquist 모양 | 첫 점 Z′ ≈ 365 Ω (−Z″ ≈ 4) → 최소 ≈ 375 Ω → 45° 상승 → 정점 Z′ ≈ 430 Ω (−Z″ 데이터 ≈ 29 · 적합 ≈ 32) → **마지막 측정점 ≈ 465 Ω (−Z″ ≈ 18)**, 적합선은 ≈ 471 Ω 까지 | 판독 (Fig. 2) — 저주파 실축 닫힘은 **측정이 아니라 적합 외삽**.  2R_el + 계면 (≈ 375 Ω) 이 R_ion 의 약 4 배 |
| A (전극 면적) | 원문 숫자 없음.  셀 틀 내경 9.8 mm 로 **가정** → A = π (0.49 cm)² = 0.754 cm² | 우리 가정 |
| σ_ion,composite | d/(R_ion·A) = 0.0208 cm / (97 Ω × 0.754 cm²) ≈ **0.284 mS/cm** | 우리 산술 (A 가정) |
| f = σ_comp/σ₀ · N_M = 1/f | ≈ **0.406** · ≈ **2.46** | 우리 산술 |
| τ_cond 재현 | ε = 0.62 (Table 1 공칭) → **1.53** (d·R 오차 전파 ± 0.05) · ε = 0.537 (재구성 SE) → 1.32 · 1.60 이 되려면 ε ≈ 0.65 (공칭보다 큼) 또는 σ₀ ≈ 0.73 mS/cm 또는 더 작은 A 가 필요 | 우리 산술 — **보고값 1.6 은 공칭 ε 0.62 쪽 (± 0.1 안) 이고 0.537 쪽은 아니다.  원문은 Eq. 3 에 넣은 ε · A · 측정 온도를 적지 않는다 → 정확 재현 불가 [미확인]** |

### 3-C. FIB-SEM 재구성 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| 장비 | FEI Strata 400 S 이중빔 (KNMF, KIT) | p.365 |
| 시료 준비 | 탄소 패드 + 은 페이스트 (ACHESON 1415) + Au 스퍼터 40 mA · 60 s · 보호 탄소층 ~1 µm (Ga⁺ 30 kV · 0.9 nA) · U 자 트렌치 (30 kV · 20 nA) | p.365 |
| 절편 · 촬영 | Slice&View · Ga⁺ 30 kV · 6.5 nA 로 x–y 면 절편 · SEM 5 kV · **590 장 · 2048 × 1768 px · 화소 35.6 nm · 절편 간격 100 nm** | p.366 |
| 복원 (SI) | ① 자기상관으로 영상 간 변위 보정 (Matlab R2014b) ② 그림자 강도 구배를 LCO·수지 대표점의 선형 맞춤으로 보정 (ImageJ) ③ 관심 영역으로 축소 ④ ① 반복 ⑤ Xlib stripes 필터 (감쇠 6) 로 세로 줄무늬 제거 ⑥ 8 bit 대비 확장 | SI p.2 |
| void 상 분할 (SI) | stripes 필터 (감쇠 3·6·12·24 반복) → **강도 < 65 인 복셀 = void/수지** → 변위 보정 → 수동 수정 (잔류 기공 너머로 비치는 배경 구조 등) → 3D 최대/최소 필터 평활 → y 축 척도 보정 (정사각 화소) | SI p.2 |
| LCO 상 분할 (SI) | stripes 필터 → 가우스 흐림 σ = 2 px → MorphoLibJ 형태학적 분할 (gradient radius 3 px · tolerance 8 · dam 끔) → 표지 영상 (문턱 + 최소 필터 반경 22 px, 수동 추가·삭제) → 표지가 든 영역 = LCO → 수동 붓 수정 → 3D 최대 (xy 2 px · z 1 절편) / 최소 (4 / 2) / 최대 (2 / 1) → y 축 척도 보정 | SI p.2–3 |
| SE 상 | **LCO 도 void 도 아닌 나머지 전부** (여집합) | p.366 · Fig. 4 캡션 (p.367) |
| void 상의 뜻 | ★ **"안정화 수지가 차지한 공간 + 잔류 공극" 을 합친 것** (분리 불가) | p.366 · Fig. 4C 캡션 (p.367) |
| 재구성 부피 | **55.9 × 38.9 × 58.1 µm³** · 복셀 **35.6 × 35.6 × 100.0 nm³** (비등방) | p.366 |
| 크기 감각 (우리 산술) | LCO 5 µm 기준 한 변 ≈ 7.8–11.6 개 입자 · LiNbO₃ 12 nm 는 화소 (35.6 nm) 보다 얇아 **미해상** | 우리 산술 |

### 3-D. CLD 형태 지표 — Table 3 (p.367, stated)

| 상 | 부피분율 [%] | μ [µm] (평균 현 길이) | k [–] (균질도, k = μ²/σ²) |
|---|---|---|---|
| LCO | **33.1** | 3.3 | 3.64 |
| interparticle (= SE + void 합친 상) | **66.9** | 9.4 | 1.43 |
| void (수지 + 잔류 공극) | **13.2** | 1.3 | 2.48 |
| SE | **53.7** | 5.2 | 1.54 |

- LCO/SE 부피비 0.616 (재구성) ≈ 0.613 (공칭 혼합) — 절대 분율이 낮은 것은 void 상 때문 (p.366).  ⇒ void 를 빼고 정규화하면 33.1/86.8 = 38.1 % · 53.7/86.8 = 61.9 % (우리 산술) = Table 1 공칭과 같다 → **void+수지는 LCO·SE 비를 바꾸지 않은 "추가 부피"** 다.
- 비교 기준 (p.367): 상대 표준편차 15 % 인 구형 입자 → k ≈ **12** (LCO 3.64 = 불규칙 형상 · 넓은 크기 분포) · 크로마토그래피 모놀리스 기공 — 실리카 k 2.5–3.0 [24,29] · 고분자 1.2–1.6 [25,30] (성능이 이미 훨씬 나쁜 쪽).  **k_SE 1.54 = SE 통로가 매우 불균질**.
- 우리 산술 (검산 감각): 구의 평균 현 길이 = (2/3)·지름 → μ_LCO 3.3 µm ⇔ 지름 ≈ 4.95 µm = 공칭 ~5 µm 와 맞는다 (입자 접촉·비구형 무시한 근사).
- 유한크기 (SI p.3, Fig. S1): 하위 부피 한 변을 10 → 100 % 로 키우며 CLD 반복 — **LCO·SE·void 의 μ·k 는 한 변의 ~70 % 에서 점근값**, **interparticle 상의 μ 는 100 % 에서야 겨우 전역값에 접근** (원문 낱말 "only finally becomes large enough to approach").  판독 (Fig. S1): μ_interparticle ≈ 6.0 (20 %) → ≈ 8.7 (70 %) → ≈ 9.1 (80–90 %) → ≈ 9.4 (100 %) — 아직 오르는 중; μ_SE ≈ 4.0 (30 %) → ≈ 5.2 (≥ 70 %); μ_LCO ≈ 3.1–3.3 (≥ 30 %); μ_void ≈ 1.3 평탄.  ⇒ **void-free 가상 구조 (= interparticle 상) 의 τ 1.27 은 RVE 수렴이 가장 덜 된 상 위의 값**이다.

### 3-E. Random-walk 시뮬 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| 방법 | random-walk 입자추적 [34] — Fick 제2법칙 ↔ 추적자 확률미분방정식의 등가 (Eq. 10) | p.368 |
| 추적자 | **N = 10⁷**, SE 상 (Fig. 6A 적색) 에 무작위 초기 배치 | p.368 |
| 걸음 | 각 축 가우스 변위, 표준편차 (2 D₀ Δt)^½ · Δt = 평균 확산 변위가 **Δh/10 이하** (Δh = 35.6 nm) | p.368 |
| 경계 | SE–LCO · SE–void 면에 **다중거부 (multiple-rejection) 경계** [35] — 면을 넘는 변위는 SE 안에 들 때까지 다시 뽑는다 (= 무유속 · 절연) | p.368 |
| 출력 | D(t) = (1/6N) d/dt Σ [Δr_i(t)]² (Eq. 11) → **장시간 점근값 = D_ion,eff** (정상 확산) | p.368 |
| 검증 | 구 배열에서 이 방법의 D 를 해석해 [38] 와 비교 — **이전 논문 [36, 37] 에서** | p.368 |
| 시간 척도 | t_D = 2 D₀ t / d_LCO², d_LCO = 5 µm (t_D = 1 ≈ 벌크에서 d_LCO 를 확산하는 평균 시간) · Fig. 7 은 t_D ≈ 5.5 까지 | p.368 · Fig. 7 |
| **실제 구조 (LCO + SE + void)** | D(t)/D₀ → **≈ 0.574** ⇒ **τ_diff = 1.74** (우리 검산 1/0.574 = 1.742) | p.368 |
| **가상 구조 (void → SE)** | LCO 부피 (33.1 %) · 형상 그대로, void 를 전부 SE 로 → φ_SE 53.7 → **66.9 %** · D/D₀ → **0.786** ⇒ **τ_diff = 1.27** (1/0.786 = 1.272) | p.368–369 |
| 변화 | "SE 부피분율 13 % 증가" → D_eff **+37 %** (0.786/0.574 = 1.369 ✓) · τ_diff 1.74 → 1.27 | p.369 |
| Bruggeman τ_B = ε^−0.5 [39] | ε = 0.669 → **1.22** (≈ 가상 1.27) · ε = 0.537 → **1.34** (원문) ≪ 실험 1.6 ± 0.1 · 시뮬 1.74 | p.369 |
| 판독 (Fig. 7) | 가상 구조 곡선은 t_D ≈ 1 에서 평탄, 실제 구조 곡선은 t_D ≈ 2 이후에도 0.60 → 0.58 로 서서히 내려간다 · 확률 잡음 띠 ≈ ±0.01–0.02 | 판독 |

### 3-F. ★ 우리 산술 — f · N_M 으로 다시 본 표 (ε 장부에 덜 휘둘리는 비교)

| 경우 | φ_SE (ε) | tau2 (원문 τ) | f = φ/tau2 = σ_eff/σ₀ | N_M = 1/f | Bruggeman τ_B = φ^−½ (우리 검산) | tau2 / τ_B |
|---|---|---|---|---|---|---|
| EIS — σ_comp 역산 (A 가정) | — (f 는 ε 불요) | — | **0.406** | 2.46 | — | — |
| EIS — 보고 τ_cond, ε = 0.62 가정 | 0.62 | 1.6 ± 0.1 | **0.388** | 2.58 | 1.270 | 1.26 |
| 시뮬 — 실제 구조 (void+수지 13.2 %) | 0.537 | 1.74 | **0.308** | 3.24 | 1.365 (원문 1.34) | 1.27 (원문 기준 1.30) |
| 시뮬 — void → SE 가상 | 0.669 | 1.27 | **0.526** | 1.90 | 1.223 (원문 1.22) | 1.04 |

- ★ **τ 로는 9 % 근접 (1.74 vs 1.6), f 로는 복셀이 20–24 % 낮다** (0.308 vs 0.388–0.406).  차이의 원인은 두 τ 가 **다른 ε 로 정규화**됐기 때문이다 (시뮬 0.537 ↔ EIS 공칭 0.62 추정).  ⇒ 시료 간 ε 장부가 다르면 τ 비교가 f 비교보다 가까워 보인다.
- ★ EIS 의 f (0.39–0.41) 는 두 시뮬 구조 사이 (0.308 < f_EIS < 0.526) 에 든다 — 원문의 설명 ("FIB 시료에만 수지가 있어 SE 분율이 낮다") 과 **같은 방향**.  다만 EIS 시료의 실제 잔류 공극은 원문에 없다 [미확인].
- void 의 수송 대가 (가상 ↔ 실제, 같은 LCO 기하): f **×1.71** (0.526/0.308) · tau2 ×1.37.  ⚠ 가상 구조는 **SE:LCO 비도 바꾼다** (실제 1.62 → 가상 2.02) — "공극만 없앤 같은 전극" 이 아니다 (§10).
- Bruggeman 배수: void-free 가상 1.04 배 (구 근사가 맞음) ↔ 실제 구조 1.27–1.30 배 (공극 형태 효과).  ASSB 실측의 다른 배수와 비교: Minnmann 42 vol% 이온 2.8 배 · 61 vol% 65 배 (그 카드 §16-3) — Hlushkou 는 SE 가 많은 끝이라 배수가 작다.
- √ 관례 (우리 tau, 원문에 없음): √1.6 = 1.26 · √1.74 = 1.32 · √1.27 = 1.13.

---

## 4. ★ 방법 — 정독

### 4-1. 이론: R_ion 을 재서 τ_cond 로 (Eq. 1–6, p.364)
- **Eq. 1** `σ_ion,composite = d / (R_ion·A)` — d · A = 전극 두께 · 면적 (**전체 기하 단면**).
- **Eq. 2** `σ_ion,composite = ε·σ_ion,electrolyte` — "ideal case": 전해질 부피분율 ε 와 순수 전해질 상 전도도로만 정해지는 경우 (= 곧고 균일한 경로, 서론 p.364 "ions migrate along straight, uniform pathways").  ⇒ Wiener 평행 상한 = **τ = 1 기준**.
- **Eq. 3** `τ_cond = (σ_ion,electrolyte / σ_ion,composite)·ε` — 이상 거동에서 벗어난 정도 = "ionic conductivity-based tortuosity".  **제곱 없음.**
- **Eq. 4** `Z_overall = 2R_electrolyte + Z_composite + Z_interfaces` — 대칭셀 Li / 전해질 / 복합전극 / 전해질 / Li [22] 의 직렬 합.
- **Eq. 5** `Z_high frequencies = 2R_electrolyte + Z_interfaces` — 복합전극의 전자 저항 R_e− 가 R_ion · 2R_electrolyte 보다 훨씬 작으면 Z_composite 무시 (Fig. 1A: 고주파에서는 전자가 복합체를 단락).
- **Eq. 6** `Z_low frequencies = 2R_electrolyte + R_interfaces + [R_ion / (iωβ)^α]·tanh(iωβ)^α` (인쇄형 그대로 — 지수 α 의 자리는 tanh 바깥에 찍혀 있다) — 저주파에서는 **전자가 전해질 층에 막혀** (Fig. 1B) 복합체 안에 Li 농도 분포가 생기고 Warburg-short 형 임피던스가 된다.  β = 정상 농도 분포가 서는 시간상수, 이상적으로 α = 0.5.  ω → 0 극한에서 그 항 → R_ion (tanh x / x → 1) ⇒ **R_ion = 복합체를 관통하는 직류 이온 저항**.
- ⇒ 측정 사슬: Eq. 6 저주파 적합 → R_ion → Eq. 1 → σ_comp → Eq. 3 (+ σ₀ · ε) → τ_cond.
- 경계조건 성격: Li⁺ 가 한쪽 SE 층에서 들어와 반대쪽 SE 층으로 **관통** (flow-through) — Nguyen 의 conventional τ 계열 (카드 `nguyen2020_electrode_tortuosity_factor`) 이고 집전체 쪽에서 이온이 막히는 τ_e (차단 대칭셀) 계열이 **아니다**.
- AM 조건: 측정 시 LCO 는 부분 충전 (≈ Li₀.₇₁CoO₂) 상태 — 원문은 이유를 적지 않는다.  Eq. 5 의 R_e− ≪ R_ion 조건 (탄소 없는 양극의 전자 경로 = LCO 망) 을 맞추려는 것으로 읽힌다 (우리 해석, 원문 근거 없음).

### 4-2. 공극 규모 시뮬: τ_diff (Eq. 8–11, p.367–368)
- **Eq. 8** `σ_ion = (z q_e)² N_V D / (k_B T H_R)` — 이온전도도 ↔ 이동 이온 확산계수의 선형 관계 (Nernst–Einstein + Haven 비 H_R [33]).
- **Eq. 9** `τ_cond = (σ_el/σ_comp)·ε = (D_el/D_comp)·ε = D_el/D_eff = τ_diff` — D_comp = 복합체를 **유사균질 매질**로 본 전체 확산계수, **D_eff = 전해질 상 안의 유효 확산계수** (상 내부 평균).  ⇒ D_comp = ε·D_eff.
  - 성립 전제 (원문 (i)–(iii)): 부피·표면 반응 없음 · 전해질–AM 계면 흡착 없음 · **AM 이 이온을 통과시키지 않음**.  (실험 쪽 Li₀.₇₁CoO₂ 가 직류에서 Li⁺ 를 얼마나 나르는지는 원문이 다루지 않는다 [미확인].)
  - 암묵 전제 (우리 지적): Eq. 8 의 N_V · H_R 이 벌크와 복합체 SE 에서 같아야 Eq. 9 의 첫 등호가 선다.
- **Eq. 10** `r(t + Δt) = r(t) + α·√(6 D Δt)` — α = 방향 무작위 · 길이 가우스 (평균 0 · 분산 1) 벡터.  구현은 각 축 표준편차 (2 D_el Δt)^½ 의 가우스 변위.
- **Eq. 11** `D(t) = (1/6N)·d/dt Σᵢ [Δrᵢ(t)]²` — 3 축 합 ÷ 6 = **등방 평균** (확산 텐서의 대각 평균).  축별 D (관통 방향 따로) 는 보고하지 않는다.
- 추적자는 **SE 상 전체**에 놓는다 → 고립 SE 주머니의 추적자도 평균에 들어가 장시간 기여 0 이 된다 = ε 에 **전 SE** 를 쓰는 관례 (우리 φ_SE 와 같은 "전체 상" 장부).
- Tjaden 리뷰의 분류로는 **voxel flux 계열의 random walk** (그 카드 D13 — `tjaden2018_tortuosity_review_calculation_approaches`).  장시간 D 는 무유속 내부면을 가진 정상 확산 (Laplace) 해의 유효 확산계수와 같은 양이다 — 방향만 등방.
- **원문에 없는 것 [미확인]**: 재구성 외곽 (도메인 경계) 의 경계조건 (주기 / 반사) · 실행 시간 길이와 점근값을 읽은 시간창 · τ_diff 의 오차 막대 · 실현 수 · 축별 이방성 · SE–SE 입자 경계 처리 (분할하지 않았으므로 해당 없음).

### 4-3. void → SE 가상 치환 (p.368–369, Fig. 6)
- LCO 상의 부피분율 (33.1 %) 과 기하는 **그대로**, void 복셀을 전부 SE 로 바꿈 → φ_SE 0.537 → 0.669 → τ_diff 1.74 → 1.27.
- 해석 (p.369): 가상 구조의 interparticle 공간은 **구 충전의 입자 사이 공간과 비슷**해 (LCO 가 불규칙해도 구와 닮음, Fig. 5 · 6B) Bruggeman 이 맞는다.  실제 구조는 공극이 SE 통로를 잘게 나눠 (Fig. 6A) Bruggeman 이 **크게 과소평가**한다 — "a relatively small additional volume fraction of voids (13%) … already suffices to create a substantial number of fine and highly tortuous paths".  CLD 가 뒷받침: μ_interparticle 9.4 µm (가상) → μ_SE 5.2 µm (실제).
- 결론 문장 (p.369): 정확한 형태–수송 관계에는 **형태 정보 전체가 필요하고 부피분율만으로는 안 된다**.

### 4-4. CLD (Eq. 7, p.366) — 형태 기술자
- 재구성 안 무작위 씨앗점에서 **26 방향 (각도 등간격)** 으로 상 경계 (또는 재구성 경계) 까지 벡터를 쏘고, 마주 보는 두 벡터를 합쳐 현 하나.  한쪽이라도 재구성 경계에 닿으면 버림.  상마다 **10⁶ 현**.
- 히스토그램을 **k-Gamma 함수** `f(l) = (k^k/Γ(k))·(l^(k−1)/μ^k)·exp(−k·l/μ)` 로 Levenberg–Marquardt 적합 [28] → μ (평균 특징 크기) · k = μ²/σ² (균질도, 클수록 균질).  상관된 무질서를 가진 복합재의 CLD 를 기술한다고 보고됨 [27].
- 기하 가정이 필요 없다는 것이 장점 (p.366).  유한크기 분석 (SI p.3) 으로 RVE 대표성 확인 (§3-D).

### 4-5. ★ 입자 처리 (DEM 양식 항목)
- **DEM · MPM · 접촉 모형 없음.**  미세구조 = 실제 압축 시료의 FIB-SEM 영상 (실제 형상 · 실제 크기 분포).  LCO 는 불규칙 (k_LCO 3.64 ≪ 구 ~12).
- SE 상 = **연속 여집합** — SE 입자 경계·입계를 분할하지 않는다 ⇒ **접촉 저항 · 협착 저항 항이 구조적으로 0** (SE 복셀끼리는 같은 D 로 이어짐).  절연면은 SE–LCO · SE–void 뿐.
- void 상 = 절연상 (수지 + 잔류 공극).  화소보다 가는 틈 (≲ 35.6 nm, z 는 ≲ 100 nm) 은 SE 로 합쳐진다.
- 소성: 유리 SE 의 실제 소성 변형은 **시료가 이미 겪은 결과**로 영상에 들어 있을 뿐, 모형화하지 않는다 (진짜 형상 소성을 계산한 것도, 접촉 소성을 계산한 것도 아님).

### 4-6. 기법 미니 용어집
| 용어 | 뜻 (이 논문 문맥) |
|---|---|
| τ_cond | ionic conductivity-based tortuosity = ε·σ₀/σ_eff (Eq. 3) — 우리 tau2 |
| τ_diff | diffusive tortuosity = D₀/D_eff (Eq. 9) — 상 내부 장시간 확산계수 기준, 우리 tau2 |
| 전자차단 대칭셀 | Li / SE / 복합양극 / SE / Li — SE 층이 전자를 막아 저주파·직류에서 복합체를 지나는 전류가 Li⁺ 뿐 |
| Warburg-short | 유한 길이 확산 임피던스 R·tanh((iωβ)^α)/(iωβ)^α — 직류 극한 = R |
| Haven 비 H_R | 추적자 확산계수 ↔ 전도도 확산계수의 비 (Eq. 8) |
| random-walk 입자추적 | 추적자의 가우스 걸음으로 확산 방정식을 푸는 몬테카를로 — 장시간 MSD 기울기 = 유효 확산계수 |
| 다중거부 경계 | 금지 상으로 넘어가는 걸음을 SE 안에 들 때까지 다시 뽑는 무유속 경계 (Szymczak–Ladd [35]) |
| CLD · μ · k | 현 길이 분포 · 평균 현 길이 (특징 폭) · 균질도 μ²/σ² |
| interparticle 상 | SE + void 를 한 상으로 합친 것 (= LCO 의 여집합) |
| 유사균질 매질 | 복합체를 하나의 균질 매질로 본 관점 — D_comp = ε·D_eff |
| Bruggeman τ_B | ε^−0.5 (구형 입자, 이 논문 관례) — 우리 φ^−½ |

---

## 5. Figure set ★ (크롭 = 메인이 순서대로; 아래는 권고)

| 그림 (쪽) | 내용 | 우리가 쓸 점 | 크롭 권고 |
|---|---|---|---|
| Graphical abstract (p.363) | 청 = AM · 적 = SE · 흑 = void 단면 위에 "paths blocked by voids" (점선, 직선 경로가 공극에 막힘) · "open ionic path" (실선, 우회) | 기전 한 장 요약 — 발표용 개념도 | 선택 |
| Fig. 1 (p.364) | 대칭셀 전하 흐름: (A) 고주파 — 전자가 복합체를 단락 (B) 저주파 — 전자 차단, Li⁺ 가 복합체를 관통 | τ_cond 가 **관통형 (flow-through)** 임을 보이는 그림 — τ_e 와 구분할 때 근거 | ✅ |
| Fig. 2 (p.366) | 대칭셀 Nyquist (데이터 + Eq. 6 적합) + 광학 단면 (SE 층 I / 복합양극 II / SE 층 I), d = 208 ± 5 µm | R_ion 97 Ω 의 출처 · 저주파 닫힘이 **적합 외삽**임 (판독) | ✅ |
| Fig. 3 (p.366) | FIB 트렌치 시료 (축 x · y · z, 척도 40 µm) | 좌표계 — 누름 방향과 재구성 축의 관계는 원문에 없음 [미확인] | 낮음 |
| Fig. 4 (p.367) | 한 절편의 재구성 단계: (A) 복원 영상 (B) LCO (백) (C) **void = 수지 + 잔류 공극** (백) (D) 3상 합성 (청 LCO · 적 SE · 흑 void), 척도 15 µm | ★ "void" 가 수지를 포함한다는 시각 증거 · SE = 여집합 | ✅ |
| Fig. 5 (p.367) | 재구성 부피의 LCO 상 3D (55.9 × 38.9 × 58.1 µm) | RVE 크기 감각 | 낮음 |
| Fig. 6 (p.368) | (A) 실제 절편 — SE 적 / LCO + void 흑, φ_SE 53.7 % (B) 같은 절편, void → SE, φ_SE 66.9 %, 척도 15 µm | ★ 공극이 SE 통로를 잘게 끊는 모습 — 우리 STEP3 "void → SE" 수치 실험의 그림 원형 | ✅ |
| Fig. 7 (p.368) | D(t)/D₀ vs t_D (= 2D₀t/d_LCO², d_LCO 5 µm): 흑 = LCO + SE + void → 0.574 (τ 1.74) · 적 = LCO + SE → 0.786 (τ 1.27), 점선 = 점근값 | ★ 핵심 정량 그림 — 두 tau2 의 출처 | ✅ |
| Table 1 · 2 (p.365) | 양극 · 음극 조성 (ρ · wt% · vol%) | φ_SE 공칭 0.62 의 출처 | Table 1 선택 |
| Table 3 (p.367) | 3상 + interparticle 부피분율 · μ · k | ★ φ_SE 0.537 · void 13.2 % · μ_SE 5.2 µm 의 출처 | ✅ |
| SI Fig. S1 (SI p.4) | (위) 현 생성 모식 (LCO 청 벡터 · interparticle 녹 벡터, 경계에 닿은 현 버림) (아래) 하위 부피 크기별 μ · k (LCO · SE · void · interparticle) | ★ interparticle μ 가 100 % 에서도 오르는 중 — 가상 구조 τ 1.27 의 RVE 한정어 | ✅ |

---

## 6. Post-processing ★
- **EIS 적합**: RelaxIS 로 Eq. 6 (Warburg-short + 직렬 R) 을 저주파 데이터에 적합 → R_ion ± 오차 (97 ± 2 Ω).  고주파 반원은 Z_interfaces 로 귀속 (추정).  두께는 측정 **후** 에폭시 매립 단면의 광학 측정 (평균 ± 편차).
- **영상**: Matlab (자기상관 변위 보정) · ImageJ (강도 구배 선형 보정 · Xlib stripes 필터 · 3D 최대/최소 필터 · 척도 보정) · MorphoLibJ v1.2.0 (형태학적 분할) · **수동 수정 단계가 여러 번** (void 배경 구조 · LCO 표지 · LCO 영역 붓 수정).
- **CLD**: 자작 코드 — 26 방향 · 10⁶ 현/상 · k-Gamma LM 적합 · 하위 부피 10–100 % 유한크기 분석.
- **확산 시뮬**: 자작 random walk — 10⁷ 추적자 · 다중거부 경계 · MSD → D(t) → 장시간 점근값 (Fig. 7 의 점선) → τ_diff.  점근값을 고른 방법 (창 · 맞춤) 은 원문에 없다.
- **보고 방식**: τ 는 소수 둘째 자리 (1.74 · 1.27) / EIS 는 ± 0.1.  Bruggeman 은 같은 ε 로 나란히.  f · N_M · √ 값은 보고하지 않는다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⚠ `our_dem_baseline.md` 는 현재 **자리표시 문서 (값 0)** 다.  아래 우리 쪽 숫자는 메인 리포 판단 메모 v2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`, 이하 "메모 v2") 와 CLAUDE.md 에서 가져왔고, 출처를 칸마다 적는다.
> **frame [5]**: 이 논문은 **실제 미세구조 위의 수송 절반**만 가진다 (형상은 영상, 역학·압밀 물리 없음 — 공극이 **왜 · 어떻게** 생기고 어떻게 없애는지는 다루지 않는다).  우리 쪽에서 같은 자리는 **STEP3 복셀 FV** (MPM 격자 위 σ, CL-81 의 CONTACT_FREE 가지) 이고, 공극을 메우는 소성 유동은 **MPM** 이 가진다.  접촉망 (DEM) 의 Holm 협착은 이 논문에 없다.
> **frame [4]**: 이 논문 수치로 우리 DEM · MPM 을 맞추지 않는다 (다른 SE 화학 · 한 점).  가져오는 것은 ① 정의 · 정규화 ② 공극 효과의 크기와 기전 ③ 복셀 ↔ EIS 비교의 방법 교훈.

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| SE | **비정질 LPSI 유리** (Li₂S–P₂S₅–LiI), σ₀ 0.7 mS/cm 펠릿 | **LPSCl 아지로다이트**, σ₀ 3.0 mS/cm (펠릿, 원장 CL-91) | **다름** — 화학 · 결정성 · 변형성 (E · σ_y 원문 없음) 이 다르다.  할라이드 ≠ LPSCl 과 같은 부류의 재료 이전 한계 |
| AM | LiNbO₃ 코팅 LCO ~5 µm, 불규칙 (k 3.64) | NCM811 구 (DEM 강체 + 연화 E) | **다름** — 형상 효과는 우리 구 DEM 에 없다 |
| 조성 | LCO 38 / SE 62 vol% 공칭 · 재구성 33.1 / 53.7 / void 13.2 | 메모 v2 의 Minnmann 대조 띠 φ_SE 0.248–0.613 (§3-3) · SE 가장 많은 침대 φ_SE 0.689–0.696 (§3-2) | 한 점 — **SE 많은 끝** |
| 공극 | void **13.2 % (수지 포함)** · EIS 시료의 잔류 공극 [미확인] | 같은 φ_SE 띠 (0.536 · 0.613) 의 우리 침대 ε_sphere 중앙 6.1 · 4.7 % (메모 v2 §3-3, "과압축 영역") | **다름** — 같은 φ_SE 에서 공극 자리에 우리는 AM 이 더 있다 (메모 v2 §3-3) |
| 압력 | 대칭셀 4 t cm⁻² 5 min (우리 환산 ≈ 392 MPa) · FIB 시료 4 t cm⁻² 14 h (수지) · σ₀ 펠릿 276 MPa | 생산 300 MPa | 같은 자릿수.  측정 중 적층압 · 스프링백 [미확인] |
| 입경비 | SE 입경 **[미확인]** (μ_SE 5.2 µm 는 통로 폭이지 입경 아님) | r_SE/r_AM 중앙 ≈ 0.13 (메모 v2 §3-3) | **배치 불가** — 메모 v2 결론 ④ 의 입경비 축에 올릴 수 없다 |
| 미세구조 원천 | FIB-SEM 실측 | DEM 구 충전 / MPM 스캐폴드 | 우리는 영상 대신 접촉 기하 |
| 수송 계산 | 복셀 random walk — **연속체 · 접촉 저항 0** | ① 접촉망 Kirchhoff (FULL = 원기둥 R_bulk + Holm R_c = 1/(2σa) · CF = R_c 0) ② STEP3 복셀 FV (조화평균, Holm 항 0 — CL-81) | τ_diff ↔ **STEP3 (②) 와 같은 물리 범주**.  접촉망 (①) 과는 이산화가 다르다 |
| 방향 | τ_diff 등방 (MSD/6) · τ_cond 관통 | z 관통 (Dirichlet 두 판) | τ_cond 만 같은 경계 |
| σ₀ 기준 | τ_cond = 펠릿 σ 기준 (τ ∝ σ₀) · τ_diff = 벌크 연속체 D 기준 (σ₀ 무관) | 우리 tau2 는 σ₀ 가 **약분** (메모 v2 §3-1) — 다만 간선 σ₀ = 펠릿값 위에 Holm 을 직렬로 더한 **모델 T** | 기준 상태 정렬 (결정 4) 전에는 값 비교 금지 |
| 연속체 T ≥ 1 | 1.27 · 1.74 (둘 다 ≥ 1 — Wiener 평행 상한 σ_eff ≤ φσ₀ 준수) | 접촉망 CF 가지는 26/157 이 T < 1 (메모 v2 §3-6, 원기둥 bulk 과전도) | ★ **연속체 복셀은 Wiener 를 지킨다** — CF 를 "모델 내부 기준선" 으로 부르는 결정 11 과 같은 방향 |
| Bruggeman 배수 | void-free 1.04 · 실제 1.27–1.30 | 우리 T_H / φ^−½ 중앙 3.40 (IQR 2.54–6.71) (메모 v2 §3-5, 1세대 협착식 포함) | 우리 배수는 접촉망 협착 + 입경비 + 기준 상태가 섞인 양 — 직접 비교하지 않는다 |
| 같은 φ_SE 띠의 우리 값 (숫자만 · 판정 없음) | τ_cond 1.6 (φ 0.62 공칭) · τ_diff 1.74 (φ 0.537) | T_H 중앙 2.65 (φ 0.613 띠, n 6) · 2.73 (φ 0.536 띠, n 2) — 둘 다 "과압축 영역" 표지 (메모 v2 §3-3) | 날 비 ≈ 1.5–1.7.  메모 v2 의 기준 상태 정렬 추정 (× 0.5–0.7, §3-2) 이 **같은 크기**라 정렬 뒤 부호가 정해지지 않는다 → **결정 4 전에 "일치 · 정합 · 검증" 낱말 금지** |
| 같은 φ_SE 의 다른 실험 | — | Minnmann 25 vol% NCM: τ² 2.40 @ φ_SE 0.613 (LPSCl, 펠릿 1.6 기준, 기공 보정 φ) | Hlushkou (1.6–1.74) 가 ≈ 0.67–0.73 배 — 재료계 · ε 장부 (Minnmann 은 기공 14 % 보정, Hlushkou EIS 는 미기재) · σ₀ 가 다 다르다.  **두 ASSB 실험의 SE 많은 끝 산포 ×1.4–1.5** (숫자만) |

- ★ **판정 요약**: 이 논문은 우리 **STEP3 복셀 σ 의 문헌 선례** (같은 물리: 연속 SE 상 · 절연 내포물 · 접촉 저항 0) 이지 접촉망 T 의 선례가 아니다.  절대 τ 앵커로는 재료계 · 한 점 · ε 장부 때문에 약하고, **공극 효과의 크기 (f ×1.71, tau2 ×1.37)** 와 **"τ 근접 ≠ f 근접"** 교훈이 우리에게 가장 값지다.
- 강체구 바닥 (~20 %) 과의 관계: 압축된 유리 SE 복합체가 void+수지 13.2 % 로 강체구 바닥 아래에 있다 — 실제 소성 치밀화의 방향과 맞다 (frame [1]/[2]).  ⚠ 수지를 포함한 값이라 잔류 기공의 상한도 하한도 아니다.

---

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 (메인 리포 CLAUDE.md ★★ τ 명명 규약, 1저자 비준 2026-10-03): **f** = σ_eff/σ₀ (`f_ion_<mode>`) · **tau2** = φ·σ₀/σ_eff = φ/f (`tau2_ion_<mode>`, 'tortuosity factor' 는 이것에만) · **tau** = √tau2 (`tau_ion_<mode>`, 웹앱 τ_Lap,eff) · **τ_geo** = 최단 경로/두께 (`tau_geo_SE_dij`, 수송 τ 아님) · **τ_e** = electrode tortuosity factor (우리에 없음).  키에 방법 · 이산화 · 가지 (flux/geo · net/vox · full/cf).

| 원문 기호 | 원문 정의 (식 · 쪽) | 원문 이름 | 정규화 — 어느 부피 · 어느 단면 · 어느 σ₀ · 방향 | 우리 양 | 키 · 환산 · 비고 |
|---|---|---|---|---|---|
| **σ_ion,composite** | `d/(R_ion·A)` (Eq. 1, p.364) | ionic conductivity of a composite electrode | 전체 기하 단면 A · 전체 두께 d · 관통 | σ_eff | f = σ_comp/σ₀ (원문은 f 를 이름 짓지 않는다) |
| **τ_cond** | `(σ_ion,electrolyte/σ_ion,composite)·ε` (Eq. 3, p.364) | **ionic conductivity-based tortuosity** ("factor" 없음) | ε = 전해질 부피분율 (EIS 에 넣은 값 원문 없음 — 역산상 공칭 0.62 쪽, §3-B) · 전체 단면 · **σ₀ = 순수 LPSI 펠릿 0.7 mS/cm @25 °C (276 MPa · 30 min)** · 관통 · 직류 | ★ **tau2** (실험 · 관통 · 접촉 포함) | `tau2_ion_<mode>` 의 **실험 짝**.  ⚠ σ₀ = 펠릿이라 펠릿 수준 접촉·기공은 σ₀ 에 흡수 — "펠릿 대비" tau2 (Minnmann τ² 와 같은 기준 부류) |
| (Eq. 2 이상 경우) | `σ_comp = ε·σ_el` (p.364) | ideal case | — | tau2 = 1 (Wiener 평행 상한) | "곧고 균일한 경로" (p.364) |
| **D_ion,composite** | Eq. 9 (p.368) | 유사균질 매질로 본 전체 확산계수 | 전체 부피 | f·D₀ | f = D_comp/D_el |
| **D_ion,eff** | Eq. 9 · Eq. 11 장시간 점근 (p.368) | effective diffusion coefficient in the electrolyte phase | **상 내부 평균** (SE 추적자만) · 등방 | D₀/tau2 | 우리 출력에 같은 이름의 열 없음 |
| **τ_diff** | `D_ion,electrolyte/D_ion,eff` (Eq. 9, p.368) | **diffusive tortuosity** | ε 불요 (MSD 에서 직접) · **기준 = 벌크 SE D (연속 매질, 펠릿 아님)** · **등방 (MSD/6)** · 연속체 · 접촉 저항 0 | ★ **tau2** (복셀 · CF 계열) | 우리 짝 = STEP3 Track-B `tau_full` (메모 v2 T15, 꼬리표 `vox_cf`) → 새 규약 꼴 `tau2_flux_ion_vox_cf`.  ⚠ 우리 것은 z 관통, 이것은 등방 |
| **τ_B** | `ε^−0.5` (p.369, [39]) | Bruggeman relation (spherical particles) — ε = 확산에 쓸 수 있는 (interparticle) 부피분율 | — | tau2_B = φ^−½ | 우리 `sigma_bruggeman` = φ^1.5 (f) 와 같은 관계.  Landesfeind α = 0.5 관례 · Tjaden/COMSOL 은 f 의 지수 1.5 |
| **ε** | Eq. 2–3 · Table 3 | volume fraction of the electrolyte | EIS: 값 미기재 · 시뮬: 0.537 (void+수지 제외) · 가상 0.669 | φ_SE | 우리 φ_SE = 전 SE 구 부피 합 ÷ 전극 부피 (질량 보존 계열, 기공 제외) — 같은 "전 SE" 장부 |
| **σ_ion,electrolyte** | p.365 | ionic conductivity of the pure electrolyte phase | **펠릿 측정값** | σ₀ | 우리 3.0 (펠릿, CL-91) 은 tau2 에서 약분 (메모 v2 §3-1) — 원문 τ_cond 는 σ₀ 에 **정비례** (비대칭) |
| **D_ion,electrolyte** | Eq. 9–10 | diffusion coefficient in bulk electrolyte | 벌크 연속체 (시뮬 입력, 값 불요) | σ₀ (STEP3 단일 σ) | 시뮬 τ 는 이 값과 무관 |
| (원문에 없음) √τ | — | — | — | **tau** = √tau2 | 우리 산술: √1.6 = 1.26 · √1.74 = 1.32 · √1.27 = 1.13 — **원문 값 아님** |
| (원문에 없음) 기하 τ | — (CLD μ 는 현 길이 = 폭 지표이지 경로 길이가 아니다) | — | — | τ_geo | **대응 없음** — 메모 v2 §2 의 "[G] ASSB SE 상 기하 τ 값 없음" 그대로 |
| (원문에 없음) τ_e | — | — | — | τ_e | **대응 없음** — EIS 는 관통형 (Fig. 1B), 집전체 차단형이 아니다 |
| (원문에 없음) N_M | — | — | — | 1/f | 우리 산술: EIS ≈ 2.46–2.58 · 시뮬 3.24 (실제) / 1.90 (가상) |

- **판정**
  1. **τ_cond = τ_diff = tortuosity factor = 우리 tau2.**  원문 낱말은 "tortuosity" 이지만 우리 규칙 ("tortuosity factor 는 tau2 에만") 에 따라 tortuosity factor 로 부른다.  √ (tau) 로 옮겨 적을 때는 반드시 "우리 산술" 표지.
  2. **두 τ 의 기준 상태가 다르다** — τ_cond 는 **펠릿 σ** 대비 (펠릿 자신의 입자 접촉 · 잔류 기공 효과가 기준에 들어감), τ_diff 는 **연속 SE 상** 대비.  원문은 둘을 기준 정렬 없이 비교한다 → 메모 v2 결정 4 가 우리 쪽에 요구하는 정렬 문제가 **이 논문 안에도** 있다.  펠릿의 기공률 · 밀도는 원문에 없다 [미확인] — 방향만 확실: 벌크 연속체 기준으로 바꾸면 실험 τ_cond 는 **더 커진다**.
  3. **ε 장부가 다르다** — τ_diff 는 ε 없이 정해지고, τ_cond 는 ε 에 비례하는데 그 값이 원문에 없다.  §3-F 처럼 **f (또는 N_M) 로 비교**하는 것이 안전하다 (Landesfeind 카드 §3-3 ⑥ 의 "N_M 비교가 ε 정의에 덜 휘둘린다" 와 같은 교훈).
  4. **방향**: τ_cond 관통 = 우리 z · τ_diff 등방 — 압축 전극의 이방성은 원문이 재지 않았다 [미확인].
  5. **접촉 저항**: τ_cond 는 복합체 안의 펠릿 초과분 (SE–SE 접촉 · 협착 · 계면) 을 **전부 포함**, τ_diff 는 **하나도 포함하지 않는다**.  ⇒ τ_cond ↔ 우리 `tau2_ion_<mode>` (FULL, 접촉망) 의 실험 짝 · τ_diff ↔ STEP3 `vox_cf` 의 문헌 짝.
  6. **COMSOL 로 넘길 때**: 이 논문 값은 이미 tau2 꼴이라 COMSOL τ_F 칸에 **그대로** 들어가는 양이다 — √ 를 취하지 않는다 (근거 강도는 메모 v2 §1: Transport of Concentrated Species Eq 6-6 = 확정 · 배터리 인터페이스 = "강하게 시사", GUI 캡처로 닫을 항목).  σ₀ 칸은 이 논문의 0.7 (펠릿) 과 짝이어야 σ_eff 를 재현한다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

### 8-0. ★ 닫는 것: **전고체 복합 양극 τ 의 두 번째 절대 앵커 후보**

| 물음 | 답 (쪽) |
|---|---|
| 재구성 | **FIB-SEM** (FEI Strata 400 S, KNMF) — 590 절편 · 화소 35.6 nm · 절편 100 nm · 재구성 55.9 × 38.9 × 58.1 µm³ · 3상 (LCO · SE · void) — SE = 여집합, **void = 수지 + 잔류 공극** (p.366, SI p.2–3).  FIB 시료는 **에폭시 수지와 섞어 4 t cm⁻² · 14 h** 로 누른 별도 펠릿 (p.365) — EIS 시료와 **다른 시료** |
| 시뮬레이션 방법 | **random-walk 입자추적** (10⁷ 추적자 · Δt: 평균 변위 ≤ 35.6/10 nm · 다중거부 무유속 경계) — **SE 상 하나에서만**, SE–LCO · SE–void 면 절연, **접촉 저항 항 없음** · 장시간 MSD/6 → D_eff (등방).  도메인 외곽 경계조건 [미확인].  Laplace 직접 풀이가 아니지만 장시간 극한에서 같은 유효 확산계수 (Tjaden 분류 voxel flux) (p.368) |
| τ 정의 · 기호 · 정규화 | τ_cond = ε·σ₀/σ_eff (Eq. 3) · τ_diff = D₀/D_eff (Eq. 9) — **둘 다 제곱 없는 tortuosity factor = tau2**.  σ_eff = 전체 단면 · ε = 전해질 부피분율 · σ₀ = **순수 펠릿 0.7 mS/cm** (EIS) / 벌크 연속체 D (시뮬) (p.364–365, p.368) |
| 보고값 | **φ_SE 공칭 0.62 (LCO 38 vol%) — τ_cond 1.6 ± 0.1** (EIS, R_ion 97 ± 2 Ω, d 208 ± 5 µm) · **φ_SE 0.537 + void 13.2 % — τ_diff 1.74** (D_eff/D₀ 0.574) · **void → SE 가상 φ_SE 0.669 — τ_diff 1.27** (0.786) · Bruggeman 1.34 / 1.22.  유효 확산/전도: 원문 보고 = D_eff/D₀ 두 값뿐 · σ_eff 는 원문에 숫자 없음 (우리 역산 ≈ 0.284 mS/cm, A 가정) (p.366–369) |
| 잔류 공극 효과 — 크기 | 같은 LCO 기하에서 void+수지 13.2 vol% 가 **D_eff −27 % (0.786 → 0.574) · tau2 ×1.37 (1.27 → 1.74) · f ×0.59 (0.526 → 0.308, 우리 산술)**.  Bruggeman 은 같은 부피 변화에 tau2 ×1.10 (1.22 → 1.34) 만 예측 (p.369) |
| 잔류 공극 효과 — 기전 | 공극이 **SE 상을 잘게 끊어 가늘고 굽은 통로를 많이 만든다** — 부피 손실보다 **형태 변화**가 크다 · CLD μ 9.4 → 5.2 µm · k_SE 1.54 (불균질) · Fig. 6A ↔ 6B (p.369).  SE 분율이 더 낮은 전극에서 더 나빠질 것이라는 추정 (p.369, 검증 없음) |
| **결정 4 뒤 두 번째 절대 대조 자리로?** | **조건부 — 판정선 앵커로는 쓰지 않기를 권한다.**  ① 재료계: 유리 LPSI (σ₀ 0.7) + 코팅 LCO ↔ 우리 LPSCl (3.0) + NCM 구 — 화학 · 변형성이 다르다.  ② 한 조성 · 한 압력 · 반복 없음 (± 는 적합 오차).  ③ φ_SE 0.54–0.62 = 우리 코퍼스가 "과압축 영역" 으로 표지한 SE 많은 띠 (메모 v2 §3-3) — 우리 침대의 공극 (4.7–6.1 %) 이 Hlushkou (13.2 %, 수지 포함) 와 다르다.  ④ σ₀ = 펠릿 (276 MPa) — Minnmann 과 같은 "펠릿 기준" 부류라 결정 4 의 T_pure,ours 정렬이 똑같이 필요.  ⑤ **입경비 [미확인]** (SE 입경 없음) → 메모 v2 결론 ④ 의 축에 놓을 수 없다.  ⑥ EIS 의 ε 미기재 → tau2 가 ±7 % (ε 0.537–0.62) 흔들린다 — f 로 비교해야 한다.  ⇒ **판정선 = LPSCl 앵커 (Minnmann) 만**, Hlushkou = "같은 φ_SE 의 다른 화학에서 tau2 가 얼마인가" 를 보여주는 **참고 점 · 방법 기준점** |
| **결정 11 (복셀 Laplace 선례 — 접촉 저항 항 유무)** | **접촉 저항 항 없음 — 확정** (SE = 연속 여집합, 절연면은 SE–LCO · SE–void 뿐).  ★ 결과: 복셀 τ_diff 1.74 가 펠릿 기준 EIS τ_cond 1.6 보다 **높다** (τ 로 +9 %, f 로 복셀 σ 가 20–24 % 낮음) — **이 한 사례에서 "접촉 저항 0 복셀 = σ 상한" 이 경험적으로 서지 않았다**.  원인 후보가 겹쳐 분리 불가: FIB 시료의 수지 (복셀 τ↑) · 펠릿 기준 (EIS τ↓) · ε 장부 차 · 등방 ↔ 관통.  ⇒ CL-81 의 "엄밀한 상한이라 부르지 않는다" 한정어를 **지지하는 외부 사례 (n = 1)**.  연속체 복셀 T 는 1.27 · 1.74 로 **T ≥ 1** (Wiener 준수) — 접촉망 CF 가지의 T < 1 (26/157) 이 원기둥 bulk 성질이라는 메모 v2 §3-6 판정과 같은 방향 |

### 8-1. 인사이트
- ① ★ **STEP3 "void → SE" 수치 실험** (같은 프레임에서 공극 복셀을 SE 로 바꿔 tau2 · f 비교) 은 그대로 따라 할 수 있다 — 이 논문 값 (f ×1.71, tau2 ×1.37 @ φ_SE 0.54 → 0.67) 이 비교 기준.  우리 쪽 의미는 **"소성 유동이 공극을 메우면 수송이 얼마나 오르나" 의 상한**이다 (frame [5]: MPM 이 가진 void-fill).  ⚠ 이 논문의 치환은 SE 부피를 **더한다** (SE:LCO 1.62 → 2.02) — MPM 의 부피 보존 소성 유동 (SE 부피 일정, 두께 감소) 과 다르다 → 우리는 (a) 치환판과 (b) 같은 SE 부피의 MPM 압밀 전후 프레임판을 **둘 다** 계산해야 비교가 선다.
- ② ★ **앵커 비교는 tau2 와 f 를 같이** — 이 논문의 "τ 9 % 근접" 이 f 로는 20–24 % 차였다 (ε 0.537 ↔ 공칭 0.62).  우리 φ_SE (구 부피 합) ↔ Minnmann (기공 보정 φ) ↔ Hlushkou (EIS ε 미기재) 처럼 ε 장부가 셋으로 갈리므로, 결정 4 의 판정선은 **f (σ_eff/σ₀) 로도 등록**하고 앵커마다 ε 장부를 표에 적는다.
- ③ **Bruggeman 은 "공극 없는 SE 연속 기지 + 구 닮은 AM" 에서만 맞았다** (1.04 배).  우리 접촉망은 SE 가 점접촉 입자상이라 이 전제부터 다르다 — 우리 T 의 Bruggeman 배수 (중앙 3.40, 메모 v2 §3-5) 를 이 논문 1.04–1.30 과 같은 줄에 놓지 않는다.
- ④ **CLD (μ, k) 를 우리 복셀 프레임에 계산** 하면 MPM 의 통로 폭 지표 d_h = V_free/S_AM (CLAUDE.md d_h 절) 과 대조할 수 있는 형태 기술자가 하나 더 생긴다 — Hlushkou 의 μ_SE 5.2 µm · k_SE 1.54 가 문헌 기준점.  (계산법: 26 방향 · 경계 현 버림 · k-Gamma 적합 · 유한크기 곡선.)
- ⑤ **복셀 해상도 감각**: 화소 35.6 nm 로 μ_void 1.3 µm (≈ 36 화소) · μ_SE 5.2 µm 를 풀었다 — 우리 MPM 의 d_h/dx ≳ 3.5 규칙 (CLAUDE.md) 보다 훨씬 고운 해상도에서 얻은 값이다.  반대로 z 는 100 nm 라 그 방향의 얇은 공극은 빠졌을 수 있다.
- ⑥ **EIS 쪽 방법 교훈**: 저주파 Warburg-short 의 실축 닫힘을 측정하지 못하고 적합으로 외삽했다 (Fig. 2 판독).  우리가 ASSB EIS 값을 앵커로 쓸 때 "R_ion 이 측정 창 안에서 닫혔는가" 를 확인 항목에 넣는다 (Landesfeind 카드의 TLM-C 과대 교훈과 같은 부류).

---

## 9. 인용 가능 문장 (deck/paper용)
- "For a LiCoO₂ / Li₂S–P₂S₅–LiI glass composite cathode (38:62 vol%), Hlushkou et al. (J. Power Sources 396, 363, 2018) obtained an ionic-conductivity-based tortuosity τ_cond = ε·σ₀/σ_eff = 1.6 ± 0.1 from an electron-blocking symmetric-cell impedance measurement and a diffusive tortuosity τ_diff = D₀/D_eff = 1.74 from random-walk simulations in a FIB-SEM reconstruction; both are tortuosity factors in the τ² convention (no square root taken)."
- "Replacing the 13.2 vol% void phase (stabilizing resin plus residual voids) of the reconstruction with solid electrolyte reduced the simulated tortuosity factor from 1.74 to 1.27, whereas the Bruggeman relation predicts only 1.34 → 1.22 for the same change in volume fraction — residual voids act mainly by fragmenting the electrolyte phase into fine, tortuous channels (Hlushkou et al., 2018)."
- "Because the simulated and measured tortuosities in that study were normalized with different electrolyte volume fractions, a 9 % agreement in τ corresponds to a ≈ 20 % difference in σ_eff/σ₀ (our arithmetic from the reported values); we therefore compare effective-conductivity ratios alongside tortuosity factors."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료계가 다르다** — 비정질 Li₂S–P₂S₅–LiI 유리 (σ₀ 0.7) + LiNbO₃ 코팅 LCO.  LPSCl/NCM 수치로 **전이 불가**, 쓰는 것은 정의 · 기전 크기 · 방법 교훈.
- ⚠ **한 조성 · 한 압력 · 한 재구성 · 한 EIS 셀** — 반복 · 실현 오차 없음 (± 0.1 · ± 2 Ω 은 적합/측정 오차).  τ_diff 에는 오차 막대가 없다.
- ⚠ **"void" = 수지 + 잔류 공극** (p.366) — 13.2 % 는 수지 없는 압축 복합체의 잔류 기공률이 **아니다**.  저자 스스로 τ_diff–τ_cond 차를 수지 탓으로 본다 (p.368 · p.369).
- ⚠ **두 τ 는 다른 시료** (FIB = 수지 섞어 14 h 압축 / EIS = 수지 없이 5 min 압축 + 충전 이력) · **다른 기준 상태** (벌크 연속체 D / 펠릿 σ) · **다른 방향** (등방 / 관통) · **다른 ε 장부** (0.537 / 미기재) — "근접" 은 깨끗한 교차검증이 아니다 (§3-F · § τ 정의 대조).
- ⚠ **가상 void-free 구조는 SE:LCO 비를 바꾼다** (1.62 → 2.02; φ_SE 0.669 > 공칭 0.62) — "같은 전극에서 공극만 없앤 것" 이 아니라 "공극을 SE 로 채운 것" 이다.  또 그 구조 = interparticle 상인데 그 상의 μ 는 RVE 에서 완전히 수렴하지 않았다 (SI Fig. S1).
- ⚠ EIS 의 ε · A · 측정 온도 · 측정 적층압 미기재 → τ_cond 정확 재현 불가 (우리 역산 1.53 @ ε 0.62).  SE 입경 · 펠릿 밀도 · E · σ_y 없음.
- ⚠ 도메인 외곽 경계조건 · 점근값을 읽은 시간창 · 축별 이방성 미기재 (random walk).
- ⚠ 저주파 Warburg 닫힘은 적합 외삽 (Fig. 2 판독).
- ⚠ 원문 내부 불일치 · 산술 (인용 전에 볼 것):
  1. EIS 주파수 범위: 본문 **500 kHz** – 0.3 mHz (p.365) ↔ Fig. 2 캡션 **1 MHz** – 0.3 mHz (p.366).  (σ₀ 펠릿 측정은 1 MHz – 0.1 Hz, p.365 — 별개.)
  2. Bruggeman: 원문 τ_B = **1.34** @ ε 0.537 (p.369) ↔ 우리 검산 0.537^−0.5 = **1.365** (1.34 는 ε ≈ 0.557 에 해당).  결론 (실험·시뮬보다 낮다) 은 불변.
  3. "(66.9% LCO, 33.1% SE)" (p.369) — **뒤바뀜** (Table 3 · Fig. 6 은 LCO 33.1 % · SE/interparticle 66.9 %).
  4. "relative increase by 13% in SE volume fraction" · "reduction (13%)" (p.369) — 실제는 **절대 13.2 %p** (53.7 → 66.9); 상대 증가는 +24.6 % (우리 산술).
  5. LiNbO₃ 두께: 서론 일반론 "∼10 nm" [8] (p.364) ↔ 이 시료 "∼12 nm" (p.365) — 모순은 아니다 (일반론 ↔ 실측).
- ⚠ **메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`):
  - **§8-1 #6** "기공 13–17 % 비교 문헌 (p.9)" — Hlushkou 의 유일한 공극 수치는 **13.2 vol% (수지 + 잔류 공극, FIB 시료)** 다 (이 논문 p.366 · Fig. 4C 캡션 p.367 · Table 3 p.367).  Minnmann 이 그 값을 기공률 비교 문헌으로 쓴 것을 옮길 때 **"수지 포함" 한정어**를 붙여야 한다.
  - **§8-1 #6** "미세구조 기반 ASSB τ 의 두 번째 절대 앵커 후보 (내용 [미확인])" — 내용 확인됨: **비 LPSCl (Li₂S–P₂S₅–LiI 유리 + LCO) · 한 조성** · EIS τ_cond 1.6 ± 0.1 (p.366) + 복셀 τ_diff 1.74 / 1.27 (p.368–369) → 지위를 **"조건부 참고 점 · 방법 기준점"** 으로 낮출 것을 제안 (§8-0).
  - §2 "[G] ASSB SE 상 기하 τ: 값 없음" — **그대로** (이 논문도 기하 τ 없음; τ_diff 는 flux 계열).  §1 대조표에 열을 더한다면: Hlushkou τ_cond "ionic conductivity-based tortuosity" · τ_diff "diffusive tortuosity" = T 행, τ_B = ε^−0.5 = Bruggeman 행.
- ⚠ **다른 정본 카드에 주는 주의 (이 카드에서 고치지 않음 — 메인 판단)**: `bielefeld2020_effective_ionic_conductivity_binder` 의 "void φ 15 % (Hlushkou 2018류)" · "Hlushkou 13.2 %류로 추정" 과 `minnmann2021_jes_charge_transport_bottlenecks` 의 [43] "기공 13–17 % 비교 문헌" — 13.2 % 가 **수지 포함 void 상**이라는 한정어가 빠져 있다.
- ⚠ 이 카드의 "우리" 숫자 (T_H 띠 값 · 26/157 · Bruggeman 배수 · ε_sphere 띠) 는 **메모 v2 의 유도값**이지 이 논문 내용이 아니다.  `our_dem_baseline.md` 는 값이 없는 자리표시 문서다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄 · 카드 유무 = 정본 `litdb/papers/` 파일 목록 대조)

| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 | 카드 |
|---|---|---|---|
| [21] | Y. Kato, S. Shiotani, K. Morita, K. Suzuki, M. Hirayama, R. Kanno, All-solid-state batteries with thick electrode configurations, J. Phys. Chem. Lett. 9 (2018) 607–613. | 같은 계열 (Toyota) ASSB 후막 전극의 tortuosity — Bielefeld 2020 카드가 "void 를 빼고 τ² 를 계산" 했다고 적은 출처 (그 카드 기준) → 이 논문 τ_cond 의 ε 장부와 같은 관례인지 확인 | 없음 |
| [19] | Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota, T. Ioroi, AC impedance analysis of ionic and electronic conductivities in electrode mixture layers for an all-solid-state lithium-ion battery, J. Power Sources 316 (2016) 215–223. | ASSB 복합층 이온·전자 전도 분리 EIS — Minnmann TLM 의 선행과 같은 축 | 없음 |
| [20] | T. Asano, S. Yubuchi, A. Sakuda, A. Hayashi, M. Tatsumisago, Electronic and ionic conductivities of LiNi1/3Mn1/3Co1/3O2-Li3PS4 positive composite electrodes for all-solid-state lithium batteries, J. Electrochem. Soc. 164 (2017) A3960–A3963. | 황화물 복합양극 조성 스윕 — 메모 v2 §8-2 의 "같은 실험 축 두 번째 점" | 없음 |
| [22] | I.V. Thorat, D.E. Stephenson, N.A. Zacharias, K. Zaghib, J.N. Harb, D.R. Wheeler, Quantifying tortuosity in porous Li-ion battery materials, J. Power Sources 188 (2009) 592–600. | 이 논문 대칭셀 법의 인용원 · eRDM (관통형) 원조 | 없음 |
| [36] | H. Liasneuski, D. Hlushkou, S. Khirevich, A. Höltzel, U. Tallarek, S. Torquato, Impact of microstructure on the effective diffusivity in random packings of hard spheres, J. Appl. Phys. 116 (2014) 034904. | ★ 무작위 강체구 충전의 유효 확산 (같은 random walk) — 우리 DEM 구 충전 위 복셀/연속체 tau2 의 직접 기준점 후보 · 방법 검증 이력 | 없음 |
| [35] | P. Szymczak, A.J.C. Ladd, Boundary conditions for stochastic solutions of the convection-diffusion equation, Phys. Rev. E 68 (2003) 036704. | 다중거부 경계의 정확도 — 복셀 random walk 를 우리가 재현할 때 | 없음 |
| [34] | J. Salles, J.-F. Thovert, L. Delannay, L. Prevors, J.-L. Auriault, P.M. Adler, Taylor dispersion in porous media. Determination of the dispersion tensor, Phys. Fluids A 5 (1993) 2348–2376. | random-walk 입자추적 원전 | 없음 |
| [38] | M.H. Blees, J.C. Leyte, The effective translational self-diffusion coefficient of small molecules in colloidal crystals of spherical particles, J. Colloid Interface Sci. 166 (1994) 118–127. | 검증에 쓴 해석해 (구 배열) | 없음 |
| [27] | T. Müllner, K.K. Unger, U. Tallarek, Characterization of microscopic disorder in reconstructed porous materials and assessment of mass transport-relevant structural descriptors, New J. Chem. 40 (2016) 3993–4015. | CLD · k-Gamma 형태 기술자의 정의 — §8-1 ④ 를 우리 복셀에 옮길 때 | 없음 |
| [16] | T. Hutzenlaub, A. Asthana, J. Becker, D.R. Wheeler, R. Zengerle, S. Thiele, FIB/SEM-based calculation of tortuosity in a porous LiCoO2 cathode for a Li-ion battery, Electrochem. Commun. 27 (2013) 77–80. | 같은 LCO 의 FIB-SEM tortuosity (액체 LIB 기공상) — 영상 τ vs 실험 τ 선례 | 없음 (`landesfeind2016_…` 참고문헌에 등장) |
| [18] | G. Inoue, M. Kawase, Numerical and experimental evaluation of the relationship between porous electrode structure and effective conductivity of ions and electrons in lithium-ion batteries, J. Power Sources 342 (2017) 476–488. | 수치 ↔ 실험 유효 이온·전자 전도 비교 (액체 LIB) | 없음 |
| [14] | M. Ebner, D.-W. Chung, R.E. García, V. Wood, Tortuosity anisotropy in lithium-ion battery electrodes, Adv. Energy Mater. 4 (2014) 13011278. | 이방성 — 이 논문 τ_diff 가 등방 평균이라는 한계의 크기 감각 (인쇄된 논문번호 그대로) | 없음 |
| [32] | M.B. Clennell, Tortuosity: a guide through the maze, in: M.A. Lowell, P.K. Harvey (Eds.), Developments in Petrophysics, Geological Society, London, Special Publications, vol. 122, 1997, pp. 299–344. | Eq. 9 의 전도 ↔ 확산 등가 · τ vs τ² 관례 논의 원전 | 없음 |
| [13] | J. Landesfeind, J. Hattendorff, A. Ehrl, W.A. Wall, H.A. Gasteiger, Tortuosity determination of battery electrodes and separators by impedance spectroscopy, J. Electrochem. Soc. 163 (2016) A1373–A1387. | 액체 LIB EIS τ 정의 정본 | ✅ `landesfeind2016_tortuosity_eis_electrodes_separators` |
| [39] | D.A.G. Bruggeman, Berechnung verschiedener physikalischer Konstanten von heterogenen Substanzen. I. Dielektrizitätskonstanten und Leitfähigkeiten der Mischkörper aus isotropen Substanzen, Ann. Phys. 24 (1935) 636–664. | τ_B = ε^−0.5 의 원전 | 없음 |

## 12. 🔗 이 논문을 쓰는 · 이웃하는 corpus 카드
- `minnmann2021_jes_charge_transport_bottlenecks` — 이 논문을 [43] 으로 인용 (ASSB tortuosity, PDF p.5 · 기공 13–17 % 비교, p.9).  두 논문 모두 **펠릿 σ₀ 기준 · 관통형** tortuosity factor — 같은 부류의 실험 tau2.
- `bielefeld2019_microstructural_modeling_composite_cathode` (ref 16 — "porosity 가 σ_eff,ion · tortuosity 에 큰 영향") · `bielefeld2020_effective_ionic_conductivity_binder` (void 15 % 가정의 근거로 인용 — §10 주의).
- 정의 묶음: `tjaden2018_tortuosity_review_calculation_approaches` (random walk = voxel flux, D13) · `landesfeind2016_tortuosity_eis_electrodes_separators` (τ = ε·N_M, 제곱 없음 — 같은 관례) · `nguyen2020_electrode_tortuosity_factor` (관통 τ ↔ τ_e — 이 논문은 관통 쪽) · `taufactor_tortuosity_factor_tomography_tool` (복셀 tortuosity factor — τ_diff 와 같은 양, 풀이법만 다름).
- `bazzoun2026_dem_fem_rnm_ionic` — LPSCl/NMC811 의 FEM 연속체 (접촉 저항 0) ↔ RNM (Holm) ↔ EIS — 이 논문의 "복셀 연속체 ↔ EIS" 와 같은 질문의 LPSCl 판.
- 같은 묶음 (2026-10-03, 같은 worktree 에서 동시 작성 중 — 이 카드에서 내용 미대조 · 링크 확정은 메인): `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (같은 Roling 그룹 · 같은 권 J. Power Sources 396 · Minnmann [25] — 임피던스 → ASSB 유효 이온전도도의 두 번째 실험 경로) · `ender2011_3d_reconstruction_composite_cathode` (복셀 재구성 + Laplace — 결정 11 의 또 다른 선례).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- 본문 8 쪽 (p.363–370) 전부 렌더 판독: Eq. 1–3 · 6 · 9 를 확대 렌더로 대조 (Eq. 3 τ_cond = (σ_el/σ_comp)·ε 제곱 없음 · Eq. 9 의 세 등호 · Eq. 6 인쇄형의 지수 자리) · Table 1 · 3 확대 대조 · Fig. 2 · Fig. 7 확대 판독.
- SI 5 쪽 전부 읽음 (복원 · 분할 절차 · 유한크기 · Fig. S1 판독 · 참고문헌).
- 우리 산술은 전부 원문 숫자로 다시 계산 (A 가정 하나 명시): σ_comp 0.284 mS/cm · f 0.406 · τ_cond 재현 1.53 (ε 0.62) · Bruggeman 1.365 @ 0.537 · f_sim 0.308 / 0.526 · 13.2 %p · 4 t cm⁻² ≈ 392 MPa.
- 중복 확인: 정본 `litdb/papers/` 파일 목록 (확인 시점 355 항목) 에 이 논문 카드 없음 · DOI `10.1016/j.jpowsour.2018.06.041` 검색 0 건 · 저자명 검색은 인용 카드 3 편 (minnmann2021 · bielefeld2019 · bielefeld2020) 만.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
