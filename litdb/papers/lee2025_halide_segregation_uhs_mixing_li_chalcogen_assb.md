<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = zuo2022_chlorination_cathode_interface.md.
     ⚠ 본문(main text) PDF 없음 — 보충자료(SM) 2개 PDF(67 쪽) + Movie S1·S2 만으로 썼다. 본문 그림 1–4 의 내용·수치는 본 적 없다.
     트랙 = li2s (Li₂S 복합양극 계면상) · ⛔ 이 트랙의 1저자는 외부 1저자다 — 여기 '우리 대비' 해석은 전부 잠정이다. -->
# 초고속(2000 rpm) 원심혼합이 아지로다이트에서 할라이드를 빼내 칼코겐 양극 계면에 LiX 나노상을 만든다 — S/Se/SeS₂/Te 전고체 전지 — Lee … Amine, Xu (Science 2025) [보충자료 기준]

> slug `lee2025_halide_segregation_uhs_mixing_li_chalcogen_assb` · DOI `10.1126/science.adt1882` · type `exp (SEM-EDS · cryo-(S)TEM-EDS/EELS · HRTEM · in situ 가열 TEM · 방사광 XRD/PDF · in situ 가열 SXRD · XPS · Raman · S/Se K-edge XANES · in situ µ-CT · 스택압 모니터링 · EIS · CV; 원자계산 0)` · PDF `litdb/inbox/Sup) Lee2025 Science … part1 adt1882_sm.pdf` (SM p.1–30) + `… part2 adt1882_sm.pdf` (SM p.31–67) + `lee2025_adt1882_movie_s1.mp4` · `…_movie_s2.mp4` · ⛔ **본문 PDF 없음** · digested `2026-10-06` · status ✅ (SM 기준)
> elements: Li, P, S, Cl, Br, I, Se, Te, Ge, C
> methods: XPS, Raman
>
> ⭐ **중요 논문 (사용자 강조 2026-10-06)** — 실험 쪽 Li₂S 복합양극에서 이 논문 방식(Thinky 초고속 혼합)을 따라 한 조건이 지금까지 가장 높은 practical 용량을 냈다 (주간보고 2026-10-05). ⚠ 단 그 최고 조건은 **SE 를 Thinky 단계에 넣지 않았다** — 논문의 핵심 주장(할라이드 편석)은 SE 가 고에너지 혼합 안에 있어야 성립한다(§5.6 · §9). 그 차이가 이 카드의 제일 중요한 읽기다.
>
> **저자**: Jieun Lee … Khalil Amine\*, Gui-Liang Xu\* (교신 amine@anl.gov · xug@anl.gov; SM 표지 기준 · 전체 저자 목록·소속은 본문에만 있어 **미확인** — SM 의 시설 언급: NSLS-II 28-ID-1/28-ID-2/8-BM/8-ID, APS 20-BM-B, ALS 8.3.2). *Science* **388**, 724 (2025).
>
> 🔗 **관련 digest**: `cronk2026_lis_cathode_interphase_chemistry` (**[Cronk26]** · Li₂S+LPSCl 1-step 볼밀 500 rpm 1 h = 실험 쪽이 따라 했다가 거의 안 돈 경로 ① · Cl 행방 미보고) · `cronk2026_lis_positive_electrode_geometry_fem` (같은 논문 기하/FEM 축) · `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` (**[Wu26LiSRev]** — 이 논문을 ref 101 · *경쟁 가설 T1: 할라이드 편석 LiX-rich 계면상* 으로 표시) · `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` (**[Wang25MIEC]** — 유리 LPS 3상 계면) · `cronau2022_wet_milling_particle_size_ionic_conductivity` (밀링 손상 σ 곡선) · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` (4d Cl 점유 ≈62 %).
>
> 🎤 **관련 발표**: 없음 — `litdb/talks/*.md` 의 "논문 에이전트 인입 대기열" 에 이 논문 행 없음 (2026-10-06 grep: 대기열 파일 1개 `lee2026_skku_mlip_materials_design.md`, 해당 행 0).

---

## 0. 이 digest 를 읽는 법

1. **본문이 없다.** 이 카드는 보충자료(SM) 67 쪽과 동영상 2편만 읽고 썼다. 본문 그림 1–4(저자의 핵심 그림 — 성능 곡선 · 편석 EDS/EELS 대표 그림 · HRTEM)는 **본 적 없다**. SM 이 본문을 가리키는 곳(예: *"Fig. 2D 의 박스"*, *"Fig. 3A"*)은 그 사실만 적는다. 본문 핵심 성능은 [Wu26LiSRev] `Table 1` ref 101 행의 2차 인용만 있다 → §3a 에 **'2차 인용 · 기준(S/복합) 미확인'** 라벨로만 싣는다.
2. **이 논문의 주장 사슬**(SM 에서 재구성): ① 2000 rpm 원심혼합(UHS)의 *국소 가열 + 전단* → ② 아지로다이트(LPSCl 등)가 기계화학적으로 부분 분해 → ③ **나노 LiX(LiCl/LiBr)가 칼코겐(S/Se) 입자 표면에 편석** → ④ 계면 Li⁺ 수송·접촉 유지 → ⑤ 이용률 ≈100–115 %, 450 사이클(2차 인용). 각 고리의 근거와 빈틈을 §5 에서 하나씩 판정한다.
3. **우리 쪽 쓸모 순서**: (1) 혼합 프로토콜 전부(§4) → (2) 편석의 정체와 증거(§5.2–5.5) → (3) SE 용량 기여 정량(§5.10) → (4) 일반화·조건(§5.11) → (5) 계산(없음, §8) → (6) 빈틈(§10). 그리고 **실험 쪽 최고 조건과의 프로토콜 차이**(§9) 가 사용자에게 가장 직접적인 절이다.
4. **트랙 규율**: li2s 트랙은 **외부 1저자**가 규칙·판정을 준다. 아래 '우리 대비' 와 '제안' 은 전부 **잠정 해석**이고 결정이 아니다. 우리 소셀 유리 결과의 숫자는 이 카드에 옮기지 않는다(마감 카드의 허용 서술만 · §7).

## 1. 한 줄 요약

할로겐 아지로다이트(LPSCl 등)를 원소 칼코겐(S·Se·SeS₂·Te)·도전재(KB+C45)와 **함께** THINKY AR-100 에 넣고 **2000 rpm · 총 5 h(30 분 혼합/30 분 휴지)** 로 섞으면, SE 가 부분 분해해 **Cl(또는 Br)-풍부·P-결핍 영역이 칼코겐 입자 표면에 생기고** HRTEM 에서 **LiCl 격자줄무늬(≈2.91 Å)** 가 Se 와 탄소 사이에 보인다 → 4 mg cm⁻² 실온에서 S 이용률 ≈100–115 % · 저압(18 MPa)에서도 작동한다는 주장. ⚠ 그러나 같은 처리에서 **LPSCl 자체의 σ 는 0.44 → 0.01 mS cm⁻¹ 로 44배 떨어지고**(`Fig. S36`), "편석이 성능을 지배한다" 를 가르는 대조(외부 LiCl 첨가 · 할로겐 없는 SE 셀 성능)는 SM 에 없다.

## 2. 메타

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| Jieun Lee … K. Amine\*, G.-L. Xu\* (전체 목록 본문 · 미확인) | *Science* 388, 724 (2025) | 10.1126/science.adt1882 | 양극: S(·Se·SeS₂·Te) : SE : KB : C45 = **22.75 : 50 : 12.25 : 15** wt% (기본) · 고S **S : LPSCl : KB = 32.5 : 50 : 17.5** · SE 대조 LPSCl : KB : C45 = 50 : 25 : 25 · SE = Li₆PS₅Cl / Li₆PS₅Br / Li₆PS₅Cl₀.₅Br₀.₅ / Li₆PS₅Cl₀.₉I₀.₁ / SS7(할로겐 없는 아지로다이트) / LGPS | exp (원자계산 0) |

- **재료 출처(SM p.2)**: S(~100 mesh)·Se(99.99 %)·Te(99.8 %, ~200 mesh)·SeS₂(98 %) Sigma-Aldrich · LPSCl/LPSBr/LPSClBr/LPSClI(D50 ≈10 µm)·**SS7(D50 ≈5 µm, "halogen-free argyrodite as illustrated by MSE Supply")** — MSE Supply · LGPS(D50 ≈5 µm) NEI · KB EC-600JD(≈65 nm)·C45(≈90 nm) TIMCAL · Li 박(MTI)·In 박(99.99 %).
- ⚠ **SS7 의 조성은 SM 에 없다** — 공급사 제품명뿐이다. '할로겐 없는 아지로다이트' 가 Li₇PS₆ 계열인지 다른 것인지 **미확인**.

## 3. 핵심 수치 총정리 (전부 문헌 소환값 · 조건 병기)

### 3a. 셀 성능 — SM 에서 직접 읽은 것 + 2차 인용

| 항목 | 값 | 조건 | 출처 / 표기 |
|---|---|---|---|
| 최고 S 이용률 | **115 %** (= 1927 mAh g_S⁻¹) | 4 mg_S cm⁻², 0.67 mA cm⁻², 25 °C, 70 MPa, Li-In | `Fig. S2` 캡션 · `Table S1` · `Table S6` (stated; 본문 Fig. 3A 를 가리킴) |
| 장기 사이클 | **450 사이클 80 %** · 100 사이클 100 % · "고면적용량 6 mAh cm⁻²" | ≥4 mg_S cm⁻² | `Table S1` · `Fig. S2` 캡션 (stated) |
| 그림 속 "This work" 별 | ≈ **5 mAh cm⁻² @ 450 사이클** · ≈ **630 Wh kg⁻¹** @ 4 mg_S cm⁻² | 투영 셀 에너지밀도(LPSCl 막 30 µm 가정) | `Fig. S2B`·`Fig. S2A` figure-read ≈ — ⚠ 캡션의 "6 mAh cm⁻²" 와 별 위치(≈5)가 다르다 |
| 2차 인용 (본문 성능) | **1273 mAh g⁻¹ · 1.4 mA cm⁻² · 4 mg cm⁻² · 450 사이클 · 25 °C** · 조성 S/LPSCl/KB/C45 22.75:50:12.25:15 | — | **2차 인용 · 기준(S/복합) 미확인** — [Wu26LiSRev] `Table 1` ref 101 행. ✎ 4 mg × 1273 = 5.1 mAh cm⁻² → `Fig. S2B` 별(≈5)과 맞는다 (우리 산수) |
| 저압 | 36 MPa: 1 회 ≈1580 · 15 회 ≈1800 mAh g⁻¹ · 18 MPa: 1 회 ≈1600 · 2 회 ≈1340 · 10 회 ≈1260 mAh g⁻¹ · 캡션 "~1340 mAh g⁻¹ at 18 MPa" | 4 mg cm⁻², 0.67 mA cm⁻², **Li 금속 대극**(1.0–3.0 V vs Li) | `Fig. S40A,C,D` figure-read ≈ · 캡션 stated |
| 이용률 vs 스택압 (자기 셀) | 70 MPa ≈116 % · 36 MPa ≈94 % · 18 MPa ≈80 % | 같은 4 mg cm⁻² | `Fig. S40B` 별 figure-read ≈ |
| Li 금속 음극 | 1 회 방전 ≈1760 mAh g⁻¹ · **100 사이클 후 2.45 mAh cm⁻²** (초기 ≈3.0) | 1.7 mg_S cm⁻², C/10 (0.28 mA cm⁻²), 1.0–3.0 V vs Li · 스택압 미기재 (Li 금속 셀은 3/2/1 N·m = 54/36/18 MPa 중 하나 — Methods) | `Fig. S38` (2.45 stated · 나머지 figure-read ≈) |
| 고S 조성 (S 32.5 % · **KB 만**) | ≈5.7 → 6.2(≈25 회) → 5.85 mAh cm⁻² (50 회) | 4 mg_S cm⁻², 0.67 mA cm⁻², RT | `Fig. S39` figure-read ≈ · ✎ 5.85 / 4 ≈ 1460 mAh g_S⁻¹ |
| 400 rpm 5 h (대조) | 1 회 ≈1.07 mAh cm⁻² → 2 회 ≈0.2 → 100 회 ≈0.08 | 4 mg cm⁻², 0.67 mA cm⁻² | `Fig. S32` figure-read ≈ |
| 1500 rpm 5 h | 1 회 ≈1700 → 2 회 ≈1100 → 25 회 ≈1040 mAh g⁻¹ | 4 mg cm⁻², 0.67 mA cm⁻² | `Fig. S34B,C` figure-read ≈ |
| SE 선밀링(2000 rpm 5 h) + 400 rpm 5 h 혼합 | **1 회 ≈27 mAh g⁻¹** · 이후 ≈5 → ≈1 mAh g⁻¹ (1000 회) | 4 mg cm⁻², 0.67 mA cm⁻² | `Fig. S33E,F` figure-read ≈ |
| 1 h UHS + 열처리 3 h | 100 °C: 1 회 ≈1210 → 2 회 ≈640 → 50 회 ≈520 · 115 °C: ≈1350 → 730 → 650 · 145 °C: ≈1350 → 960 → 800 mAh g⁻¹ | 4 mg cm⁻², 0.67 mA cm⁻² | `Fig. S43` figure-read ≈ |

### 3b. 칼코겐 일반화 · SE 용량 기여 (`Table S6`, stated — 5 h UHS)

| | S | Se | Te |
|---|---|---|---|
| 이론 비용량 (mAh g⁻¹) | 1675 | 675 | 420 |
| 최고 달성 비용량 | 1927 | 974 | 861 |
| "정의된 칼코겐 이용률" | **115 %** | **144 %** | **205 %** |
| **SE 의 용량 기여** | **15 %** | **44 %** | **105 %** |
| 100 사이클 유지율 @0.1C | 99 % | 112 % | 107 % |

- 표 제목: *"with assumption of full utilization of chalcogen active materials"* — 즉 **SE 기여 = 이용률 − 100 %** 라는 **잔차**다. 독립 측정이 아니다(§5.10).
- 면적용량(`Fig. S41`, figure-read ≈): Se 1 회 ≈3.1 → 20 회 ≈3.85 mAh cm⁻² · SeS₂ ≈4.4 → 20 회 ≈5.2 → 100 회 ≈3.9 · Te ≈2.9 → 20/50 회 ≈3.45. 속도: Se 0.27 → 1.35 mA cm⁻² 에서 ≈4.75 → 3.85 · SeS₂ 0.54 → 2.7 에서 ≈4.7 → 3.3 · Te 0.17 → 0.85 에서 ≈4.1 → 3.35 mAh cm⁻². ⚠ Se·SeS₂·Te 의 칼코겐 로딩은 SM 에 없다(본문).

### 3c. SE 자체 — 처리에 따른 이온전도도 · 구조

| 항목 | 값 | 조건 | 출처 |
|---|---|---|---|
| LPSCl σ (공급 그대로) | **0.44 mS cm⁻¹** | 500 MPa 펠릿, SS 블로킹, 100 kHz–100 mHz, 25 °C, Z-view | `Fig. S36A` · `Fig. S42` stated |
| LPSCl σ — 2000 rpm 1 / 5 / 10 h 처리 후 | **0.11 / 0.01 / 0.002 mS cm⁻¹** | 같은 측정 | `Fig. S36A` stated — ⇒ 5 h 에 **44배**, 10 h 에 **220배** ↓ (우리 산수) |
| 다른 SE σ (공급 그대로) | LPSBr 0.94 · LPSClBr 1.04 · **LPSClI 2.3** · **SS7 0.21** · LGPS 0.56 mS cm⁻¹ | 같은 측정 | `Fig. S42` stated(막대 숫자) |
| 겉보기 D_Li 비 (Randles–Ševčík 기울기) | 2000 rpm 1 h **2.1** · 5 h **8.4** · 10 h **6.1** · 400 rpm 5 h **0.6** mA mV⁻¹ᐟ² s¹ᐟ² ⇒ 5 h / 400 rpm = **196 배** (기울기 비의 제곱) | CV 0.1/0.2/0.3/0.5 mV s⁻¹, 0.38–2.38 V vs Li-In | `Fig. S36B` stated · 그림 기울기 실독으로 네 값 모두 확인 ✓ |
| LPSCl 격자상수 a (Rietveld, GSAS-II) | 9.85082 (원료) → 9.85016 (1 h) → **9.84649 (5 h)** → 9.85195 Å (400 rpm 5 h) | λ = 0.1665 Å, NSLS-II 28-ID-2 | `Table S2`–`Table S5` stated · `Fig. S19B` ✓ |
| LPSCl 결정자 크기 | 0.766 → 0.245 → **0.123** → 0.41 | 같은 정련 | `Table S2`–`S5` 의 단위 표기는 **"mm"** 이지만 `Fig. S19B` 축은 **µm** → µm 로 읽는다 (표 오기) |
| Cl 자리 점유 | **4a 0.385 / 4d 0.615 — 네 표 모두 동일** · S 4a 0.615 / 4d 0.385 · Li 48h 0.5 | 같은 정련 | `Table S2`–`S5` — ⚠ **점유를 정련하지 않고 고정한 것으로 보인다**(§5.4) |
| Li U_iso (Å²) | 0.064 → 0.109 → **0.132** → 0.034 | 같은 정련 | `Table S2`–`S5` |

### 3d. 편석 정량 지표 (SM 에 있는 것 전부)

| 지표 | 값 | 출처 |
|---|---|---|
| Cl:P (STEM-EDS, Se/LPSCl/C 5 h, 6 영역) | **2.5 · 2.4 · 2.3 · 1.7 · 1.5 · 1.5** (LPSCl 화학량론 1) | `Fig. S26` 패널 숫자 stated |
| SEM-EDS 합 스펙트럼 wt% — SE 선밀링 + 400 rpm | S 77.5 · Cl 11.9 · P 10.5 → 캡션 *"Cl/P ≈ 1, no segregation"* | `Fig. S33C` 삽입 |
| SEM-EDS 합 스펙트럼 wt% — 1500 rpm 5 h | S 79.3 · Cl 11.7 · P 9.0 → 캡션 *"Cl/P slightly increased to 1.3"* | `Fig. S34A` 삽입 |
| ✎ 위 두 값의 **원자비** 환산 (우리 산수) | 선밀링 + 400 rpm **0.99** · 1500 rpm **1.14** (화학량론 1) — 캡션의 1.3 은 **무게비**(11.7/9.0) 이고, 무게비의 화학량론 기준은 1 이 아니라 **1.145**(35.45/30.97) 다 | §10-⑦ |
| EELS S-L₂,₃ 문턱 | 그림 라벨: site #11(저대비 · "S⁰ + Cl-rich") **167.8 eV** · #10 **165.6** · #9 **166.5 eV** — 캡션 문장은 *"166.6 eV for sulfides vs 168.6 eV for elemental sulfur"* | `Fig. S11C` (그림 라벨과 캡션 숫자가 다르다) |
| LiCl 격자줄무늬 | **≈2.91 Å** (LiCl (111) d = 2.97 Å 와 2 % 차 — 우리 산수, a(LiCl)=5.13 Å 가정) · Se ≈3.78 / 3.02 Å, FFT 각 66.4° · 탄소 ≈3.39 Å | `Fig. S30` |

## 4. 혼합 프로토콜 — 원문 그대로 + 빠진 것 ★ (우리 쓸모 1순위)

**원문(SM p.2)**: *"All the composite cathodes in this work were prepared using an AR-100 planetary centrifugal mixer (THINKY Inc.). The composite cathodes were prepared as a mixture of cathode active material powder, solid-state electrolyte, KB, and C45 with a weight ratio of 22.75:50:12.25:15 unless specified. The cathode mixture and ZrO₂ balls were placed in a container with a 1:5 weight ratio and mixed at 400, 1500 or 2000 rpm for 1, 5, or 10 h. Each mixing process involved alternating 30-min mixing followed by a 30-min rest period, which was repeated until the desired total mixing time was achieved."*

| 변수 | 이 논문 | 비고 |
|---|---|---|
| 장비 | **THINKY AR-100 planetary centrifugal mixer** (볼밀 아님 — 자전·공전 원심 혼합기에 볼을 넣은 것) | `Fig. S3`·`Fig. S40B` 의 가로축 "Mixing speed (rpm)" 에 남의 **유성 볼밀 rpm** 과 같은 축으로 놓는다 — 장비가 달라 rpm 이 같은 에너지가 아니다(§10-⑨) |
| 투입 | **활물질 + SE + KB + C45 를 한 번에** (문장 그대로 "a mixture of …") | 순서·단계 투입 언급 없음 ⇒ **동시 투입**으로 읽는다 |
| 볼 : 분말 | **ZrO₂ 볼 : 혼합물 = 5 : 1 (무게)** — 원문 *"mixture and ZrO₂ balls … 1:5"* | 볼 지름·개수·용기 부피·배치 질량 **미기재** |
| 속도 | 400 · 1500 · 2000 rpm | 2000 rpm 이 "UHS" |
| 시간 | 총 혼합 1 · 5 · 10 h (**최적 5 h**) | 30 분 혼합 + 30 분 휴지 반복 ⇒ 5 h 혼합 = 30 분 × 10 회 ≈ 벽시계 10 h (우리 산수) |
| 온도 | **용기 온도 측정 없음** | "국소 가열(heat striking)" 의 크기는 어디에도 수치가 없다(§5.5) |
| 분위기 | Ar 글러브박스 안에서 전부 | — |
| 조성 (기본) | **22.75 : 50 : 12.25 : 15** (S : SE : KB : C45) | 탄소 합 27.25 wt% · ✎ 4 mg_S cm⁻² 이면 복합양극 17.6 mg cm⁻² · SE 8.8 mg cm⁻² (우리 산수 — `Fig. S44` 의 SE 로딩 8.8 과 일치) |
| 조성 (고S) | **S : LPSCl : KB = 32.5 : 50 : 17.5** · **KB 단독** · 2000 rpm 5 h | `Fig. S39` 에서 ≈6 mAh cm⁻² (figure-read) — ⚠ `Fig. S18` 이 "단일 탄소면 편석이 적다" 고 한 것과 같은 논문 안에서 긴장(§10-⑥) |
| SE 대조 (용량 기여용) | LPSCl : KB : C45 = 50 : 25 : 25 · 2000 rpm 5 h | `Fig. S44` |
| 탄소 이중 사용 근거 | *"Carbon not only served as grinding materials but also worked as milling media"* · 볼밀 '엄지 규칙'(ref 67 Burmeister & Kwade) — KB(≈65 nm)+C45(≈90 nm) 두 입도가 밀링 효율을 올린다 | `Fig. S18` 캡션 — 기전 근거는 EDS 정성 지도뿐 |
| 셀 조립 | SE 100 MPa 성형 → 양극 분말 얹고 **500 MPa** → Li : In = 1 : 2 (원자비) 적층 → 전체 **350 MPa** → 케이스 4 N·m 체결 = **≈70 MPa** 스택압 | 0.38–2.38 V vs Li-In (Landt CT3002AU) · Li 금속 셀은 1.0–3.0 V vs Li · 3/2/1 N·m = 54/36/18 MPa |
| 측정 온도 | **25 °C 전부** | `Table S1` 의 비교군은 30–100 °C |

**'heat striking · shear fracturing' 기전 주장의 근거 그림** — `Fig. S1`·`Fig. S12`(도식) · `Fig. S13`·`Fig. S14`(in situ 가열 SXRD) · `Fig. S15`(145 °C 3 h 가열 EDS) · `Fig. S16`·`Fig. S17`·Movie S1·S2(in situ 가열 TEM) · `Fig. S43`(1 h UHS + 열처리 셀). **'shear' 쪽 근거**는 `Fig. S33`(SE 선밀링 대조) · `Fig. S34`(1500 rpm) 두 개다. 둘 다 §5.5–5.6 에서 판정한다.

## 5. 결과 — 절별 상세 (그림 실독 포함)

### 5.1 왜 이 문제인가 (`Fig. S2`·`Fig. S3`·`Table S1`)
- `Fig. S2A`: 문헌 ASSLSB 셀들을 S 로딩–투영 에너지밀도 평면에 놓고(LPSCl 막 30 µm 파우치 가정) 이용률 등고선 40/60/80/100 % 를 그렸다. "This work" 별은 4 mg cm⁻² 에서 ≈630 Wh kg⁻¹ (figure-read ≈) 로 문헌 최고(ref 22, ≈575)보다 위.
- `Fig. S2B`: 면적용량–사이클 수명. 저로딩 장수명 / 고로딩 단수명의 반비례 무리 위에 별(≈5 mAh cm⁻² · 450 회).
- `Fig. S3`: 혼합 속도–이용률. 문헌 점은 전부 **0–600 rpm**, 우리 별만 2000 rpm. 캡션 스스로 *"sulfur utilization reported in studies utilizing sulfide solid electrolytes may include extra capacity contributed by the redox reactions of the sulfides themselves"* 라고 단서를 단다 — 그런데 그 단서를 자기 115 % 에도 적용해야 한다(§5.10).
- `Table S1`: 촉매(ref 12, 60 °C, ~55 %) · 도핑(ref 1, SI, 100 °C, ~60 %) · 벌크 할라이드 첨가(ref 13, 60 °C, ~60 %) · 표면코팅(ref 17, 60 °C, 70 %) · 습식혼합(ref 24, 30 °C, 76 %) · **이 연구(raw S, 2000 rpm, 5 h, 25 °C, 115 %, 100 %@100 · 80 %@450)**. "Polysulfide risk" 칸(High/Low/Very low)은 **정성 판정이고 근거 측정이 없다**.

### 5.2 편석 — SEM-EDS 마이크로 척도 (`Fig. S4`–`Fig. S6`·`Fig. S18`·`Fig. S23`–`Fig. S25`·`Fig. S35`) ★
- **2000 rpm 5 h (`Fig. S4`, 실독)**: 가운데 ≈10 µm 구형 "S/LPSCl/C" 2차 입자(SEM 라벨)에서 **P 는 약하고 Cl 은 강하다**. 왼쪽 아래의 남은 LPSCl 입자는 **P 가 강하고 Cl 은 상대적으로 어둡다**. 즉 Cl 이 SE 입자에서 S/C 응집체 쪽으로 옮겨 간 모양이다. ⚠ 원래 LPSCl 입자가 **그대로 남아 있다** — 전량 반응이 아니다.
- **1 h (`Fig. S5`, 실독)**: P 와 Cl 지도가 대체로 겹치되 Cl 이 S 영역 쪽으로 더 퍼진 정도 — 5 h 보다 약하다.
- **400 rpm 5 h (`Fig. S6`, 실독)**: **P 와 Cl 이 같은 입자에 함께 밝다**(아래 왼쪽·오른쪽 위 LPSCl 입자) — 편석 없음. 캡션: *"no clear segregation of P, S and Cl … inhomogeneous distribution of Cl over S particles"*.
- **단일 탄소 (`Fig. S18C,D`, 실독)**: KB 만 · C45 만 — 구형 2차 입자는 생기지만 P·Cl 지도가 같은 모양으로 겹친다 → 캡션 *"single carbon additive shows significantly less halide segregation"*. ⚠ 셀 성능은 SM 에 없다(이 비교는 EDS 정성뿐).
- **10 h (`Fig. S35A`, 실독)**: Cl·P·S 가 거의 같은 입자 모양 — 캡션은 '편석 적음' 을 셀 압력 해석에서 말한다(`Fig. S37` 캡션). `Fig. S35B`: 10 h 에서 LPSCl 피크가 크게 약해짐(비정질화) · 5 h 는 피크 유지(약화) · 원료 양극의 S 피크는 5 h 후 사라짐.
- **Se/SeS₂/Te (`Fig. S23`–`Fig. S24`, 실독)**: 2000 rpm 에서 Cl 이 Se 영역 위에 넓게 깔린다 · 400 rpm 은 Se 가 거의 안 보일 만큼 흩어지고(작은 덩어리) Cl 은 P 와 겹친다. Te(`Fig. S24B`)는 Te·S·P·Cl 이 모두 같은 구형 입자 위 — **Te 에서 Cl 이 P 와 갈라진 모습은 이 그림에서 뚜렷하지 않다** (판독).
- **다른 할로겐 SE (`Fig. S25`, 실독)**: LPSBr · LPSClBr · LPSClI 2000 rpm 5 h. 캡션 *"both halogens were successfully dispersed within the sulfur matrix"*. ⚠ I 지도(`Fig. S25C`)는 **신호가 거의 바탕 수준의 점묘**(LPSClI 의 I 는 0.1) — 편석 판정 불가.

### 5.3 편석 — 나노 척도 cryo-STEM-EDS · EELS · HRTEM (`Fig. S11`·`Fig. S26`–`Fig. S31`) ★
- **cryo 규율(`Fig. S7`–`Fig. S10`, 캡션만 읽음 · 그림 미실독)**: RT-TEM 은 LPSCl 이 전자선에 부풀고 줄고 구멍이 남(3.87 e⁻ Å⁻² s⁻¹, 107.5 s) · cryo(−178 °C) 에서는 같은 선량에 변화 없음 · 0.05 e⁻ Å⁻² s⁻¹ 저선량 · 공기 3 분 노출에 O 신호 급증 → Ar 전송 홀더. **방법 쪽 모범**이다.
- **EELS (`Fig. S11`, 실독)**: S/LPSCl/C 5 h 의 HAADF 저대비 가장자리(#7·#11)와 고대비 내부(#8–#10). #11 의 S-L₂,₃ 문턱이 더 높고(167.8 eV 라벨) **200 eV 위 Cl-L₂,₃ 구조**가 보임 → 라벨 *"S⁰ + Cl-rich"*; #9·#10 은 낮은 문턱(166.5/165.6) · Cl 구조 약함 → *"Sⁿ⁻ + Cl-deficient"*. ⚠ 캡션은 #7–#11 다섯 곳을 말하지만 **그림에는 #9·#10·#11 셋만** 있다.
- **Cl-L 에지 (`Fig. S28`, 실독)**: Se/LPSCl/C 5 h 의 영역 i–v + KCl 기준. i–iii 은 ≈200 eV 문턱 뒤 뚜렷한 구조, iv 약함, **v 는 평탄(Cl 없음)**. 영역 위치는 **본문 그림 2D 의 박스** — 본 적 없음.
- **Cl:P (`Fig. S26`, 실독)**: 여섯 영역 모두 Cl 이 Se 입자 둘레(청록)를 싸고 Se(적)는 안쪽 — **Cl:P 2.5/2.4/2.3/1.7/1.5/1.5**. ⇒ 이 논문에서 편석의 **가장 직접적인 정량 근거**다. ⚠ EDS 정량 방식(Cliff–Lorimer k-인자 · 두께 보정)은 미기재, 영역 선택 기준도 미기재.
- **EDS 스펙트럼 (`Fig. S29`, 실독)**: Se/LPSBr/C 에서 **Br-Lα(1.48 keV) "rich"** 가 Se-Lα(1.38 keV) 어깨에 붙어 있다 — 두 선이 0.1 keV 차라 **겹침 분리가 판정의 전부**다. Se/LPSCl/C 는 Cl-Kα(2.62) 가 S-Kα(2.31) 와 비슷한 높이 · P-Kα(2.01) 는 아주 작음("P deficient"). S/LPSCl/C 는 S 가 크고 Cl 이 그 절반쯤.
- **HRTEM (`Fig. S27`·`Fig. S30`·`Fig. S31`, 실독)**: Se 입자 표면에 탄소 격자줄무늬(`Fig. S27C`) · 줄무늬 ≈2.91 Å 영역 "LiCl" (`Fig. S30A`) · `Fig. S31A,D` 에서 **"Carbon | LiCl | Se"** 및 **"Se | LiCl | Se"** 의 띠 모양 경계(점선)를 그었다 — 띠 두께 figure-read ≈ 10–15 nm. ⚠ "LiCl" 동정은 **d 값 하나 + FFT** 다. 2.91 Å 는 LiCl(111) 2.97 Å 와 2 % 차인데, **LPSCl·Li₂S·Se 의 다른 면간거리도 2.9–3.0 Å 대에 있을 수 있다**(이 논문은 대안 동정을 배제하는 절차를 적지 않았다). MATLAB 모델 + HRTEM 시뮬레이션(200 kV, Cs 0.5 mm, 두께 ≈4 nm, Δf 40 nm)은 Methods 에 있으나 그 비교 그림은 SM 에 없다(본문 추정).

### 5.4 편석 — 벌크 구조 (XRD 리트벨트 · PDF · Raman · XPS) (`Fig. S19`–`Fig. S22`·`Table S2`–`Table S5`)
- **SXRD (`Fig. S19A`, 실독)**: 400 rpm·2000 rpm 1 h·5 h 모두 **S 피크가 사라졌다**(400 rpm 도). LPSCl 피크는 남고 5 h 에서 넓어짐. **LiCl 피크는 어느 복합체에도 보이지 않는다** — 저자는 "nanosized" 라 XRD 무음이라고 본다.
- **리트벨트 (`Table S2`–`Table S5`)**: a 변화는 5 h 에서 **−0.0043 Å (−0.044 %)** — 작다. 결정자 0.77 → 0.12 µm. 🔴 **Cl 점유 4a 0.385 / 4d 0.615 가 네 표에서 소수 셋째 자리까지 같다** — 정련에서 고정한 값으로 보인다. ⇒ **"Cl 이 LPSCl 격자를 빠져나갔다" 는 리트벨트로 보여지지 않았다.** (원료의 4d Cl ≈62 % 는 [Kraft] 의 ≈62 % 와 같은 값이다.)
- **PDF (`Fig. S19C`, 실독)**: S₈ 고리의 4.5 Å 상관이 모든 복합체에서 사라짐 → S 비정질화. LPSCl 의 2.0/3.35/4.1 Å 는 유지. 캡션 *"no significant differences were observed between different composite sulfur cathodes"* — **PDF 는 400 rpm 과 2000 rpm 을 구분하지 못했다.**
- **Raman (`Fig. S19D`, 실독)**: S₈ 473/219/152 cm⁻¹ 가 복합체에서 사라짐. ⚠ 그림의 5 h 복합체 스펙트럼에는 **LPSCl 425 cm⁻¹ 가 아주 약한 둔덕**이고 대신 **≈242 cm⁻¹ (figure-read ≈) 날카로운 피크** 하나가 있다 — 캡션은 *"those belonging to LPSCl were still maintained"* 라 하고 242 cm⁻¹ 피크는 **언급·동정이 없다**(§10-⑧).
- **XPS (`Fig. S21`, 실독)**: Cl 2p 는 처리 전후 같음 — 캡션 스스로 *"its state in LPSCl and LiCl was identical"* ⇒ **XPS Cl 2p 는 LiCl 을 가르지 못한다**. Li 1s 는 2000 rpm 5 h 에서 고결합에너지 쪽으로 이동했다는데 그림상 이동은 **≈0.1–0.2 eV (figure-read ≈)** 로 C 1s 285.0 eV 보정 오차와 같은 크기다. S 2p 는 S⁰ 성분이 400 rpm → 1 h → 5 h 로 크게 줄어 **5 h 에서 표면 신호가 LPSCl 성분으로 덮인다** — SE 유래 물질이 S 를 덮는다는 그림과는 맞는다. P 2p(`Fig. S22`)는 원료와 같음 → Li₃P 등 환원 P 없음.

### 5.5 '국소 가열' 기전의 근거 (`Fig. S13`–`Fig. S17`·`Fig. S43`·Movie S1·S2)
- **in situ 가열 SXRD, S+LPSCl+C 손혼합 (`Fig. S13`, 실독)**: 30 → 400 °C (10 °C min⁻¹, λ 0.1824 Å). 저자: S 결정 피크가 ≈100 °C 에서 사라지고 **결정 LiCl 은 ≈200 °C 에서 나타나기 시작**. 그림: LiCl (111)·(200) 화살표 위치(2θ ≈3.5° · ≈4.0°)의 줄무늬는 **대략 300 °C 위에서 눈에 띈다** (figure-read ≈ — 200 °C 시작은 그림에서 확인 못 했다).
- **in situ 가열 SXRD, LPSCl+C 만 (`Fig. S14`, 실독)**: 40 → 500 °C. **LPSCl (311)·(222) 피크가 사라지는 구간과 LiCl (111)·(200) 이 서는 구간이 같다** — 대략 300 °C 위 (figure-read ≈). ⇒ 저자: *"LiCl can be thermally produced from Li₆PS₅Cl and carbon even without the presence of elemental sulfur"*. 이 그림이 실제로 보여 주는 것은 **"LPSCl 이 열분해될 때 LiCl 이 생긴다"** 이고, 그 온도는 수백 °C 다.
- **145 °C 3 h 가열 (`Fig. S15`, 실독)**: 손혼합 S/LPSCl/C 를 가열하면 EDS 점 스펙트럼에서 Cl 이 P·S 대비 커짐(#2 vs #1). ⚠ **점 하나씩**의 비교다 · 정규화 기준 미기재.
- **in situ 가열 TEM (`Fig. S16`·`Fig. S17`·Movie S1·S2, 실독)**: 시료는 **2000 rpm 0.5 h 로 이미 섞은** Se/LPSCl/KB/C45. 레이저(1 mW, **온도 미측정**)로 LPSCl/C 영역의 대비가 밝아지는(분해?) 모습 · 열전 가열 20 → 220 °C(100 °C min⁻¹)에서 168.6 °C 근처 노출 Se 가 사라지고(증발/이동) 혼합 영역이 어두워짐. `Fig. S17G`: Se 영역 회색값 ≈122 → 74, LPSCl/C 영역 ≈45 → 132 (figure-read ≈). ⚠ **화학 동정(EDS·회절)이 가열 중에 없다** — 대비 변화만으로 "LPSCl 분해 → 편석" 을 말한다. 고진공에서 Se 증발이 같이 일어난다(저자도 인정).
- **열처리 셀 (`Fig. S43`)**: 1 h UHS 시료를 100/115/145 °C 에서 3 h → 높을수록 유지율 좋음(§3a). 🔴 **S 의 녹는점은 ≈115 °C** 다 — 115·145 °C 처리는 Li–S 분야의 표준 **용융확산(melt-diffusion)** 과 같은 조작이다. 편석과 S 용융 재분포를 가르지 못한다(§10-③).
- ⇒ **판정 (잠정)**: "heat striking" 이 **용기 안에서 몇 °C 를 만드는지 측정이 없다.** in situ 가열 실험들은 *가열하면 LPSCl 이 분해해 LiCl 이 생길 수 있다* 를 보여 주지만, 그 문턱(수백 °C, figure-read)을 Thinky 혼합이 국소적으로라도 넘는다는 증거는 SM 에 없다.

### 5.6 '편석이 지배한다' 의 대조 — 입도 vs 편석 (`Fig. S33`·`Fig. S34`·`Fig. S36`) ★★
- **SE 선밀링 대조 (`Fig. S33`, 실독)**: LPSCl 만 2000 rpm 5 h 따로 밀링(SEM 에서 입자 작아짐 · 표면 주름) → S·C 와 **400 rpm 5 h** 로 혼합 → Cl/P ≈1(편석 없음) → **1 회 방전 ≈27 mAh g⁻¹**(figure-read ≈). 저자 결론: *"the halide segregation dominated the boosted cell performance, rather than the reduced particle size of solid electrolyte."*
- 🔴 **그러나 이 대조는 두 변수를 동시에 바꿨다**: ① 편석 없음 ② **SE σ 가 이미 0.01 mS cm⁻¹ 로 떨어진 SE**(`Fig. S36A`, 5 h 처리 = 44배 ↓) ③ S–C–SE 를 400 rpm 으로만 섞음. 저자도 캡션에 *"due to lack of halide segregation at the interface **and dramatic decreased bulk ionic conductivity**"* 라고 둘을 같이 적었다. ⇒ 이 셀이 안 도는 것은 **'SE 를 혼자 갈면 망가진다'** 로도 완전히 설명된다. '편석이 지배' 를 세우려면 *같은 SE σ · 같은 접촉 · 편석만 다른* 셀이 필요한데 SM 에 없다.
- **1500 rpm (`Fig. S34`)**: Cl/P(원자비 1.14 · §3d) 로 편석이 약한데도 **25 회 ≈1040 mAh g⁻¹** — 400 rpm(≈0.1 mAh cm⁻² ≈ 25 mAh g⁻¹)과는 **40 배 차**, 2000 rpm 5 h(≈1500 대)와는 1.5 배 차. ⇒ 성능 이득의 **대부분이 이미 1500 rpm 에서 오는데 그때 편석 지표는 거의 화학량론**이다(우리 읽기 · §10-②).
- **D_Li 196 배 (`Fig. S36B`)**: 2000 rpm 5 h 와 400 rpm 5 h 의 Randles–Ševčík 기울기 비의 제곱. 전환형 복합양극의 CV 피크 전류에 반무한 확산식을 적용한 **겉보기 값**이고 면적·농도 항이 같다는 가정이 들어간다. 그림 기울기 네 개는 본문 숫자와 맞는다 ✓.
- **10 h 는 왜 나쁜가 (`Fig. S35`·`Fig. S37`)**: LPSCl 이 더 비정질화(σ 0.002 mS cm⁻¹) · 저자는 "편석이 적어서" 라고도 쓴다. 두 해석이 같은 그림에 공존한다.

### 5.7 스택압 · 부피 (`Fig. S37`·`Fig. S50`)
- **in situ 압력 (`Fig. S37`, 실독)**: 초기 70 MPa. 1 회 방전 ΔP **−3.1 (1 h) · −4.3 (5 h) · −5.25 (10 h) MPa**, 충전 후 남은 ΔP **−1.45 · ≈−0.05 · −2.45 MPa** (figure-read ≈). 누적 면적용량 축: 1 h 방전 끝 ≈4.65 · 5 h ≈6.2 · 10 h ≈6.1 mAh cm⁻² (figure-read ≈). 저자 스스로 *"the overall stack pressure change would be predominantly influenced by the Li-In anode"* — 양극 기여를 따로 떼지 않았다. ⚠ 각 전압에서 5 분 휴지 → 전압 스파이크·압력 둔덕.
- **in situ µ-CT (`Fig. S50`, 실독)**: 양극 두께 ≈60 µm 가 OCV · 1 회 방전 · 1 회 충전에서 "거의 그대로". 눈금 20 µm · **복셀 크기·두께 측정법 미기재** · 단면 1 장씩. ⚠ 그림 패널 라벨 "C" 가 떠 있고 C 패널이 따로 없다(라벨 오류로 보임).

### 5.8 반응 경로 — XPS · XANES (`Fig. S44`–`Fig. S49`)
- **S 2p 방전/충전 (`Fig. S45`, 실독)**: 방전 1.18 → 0.78 → 0.38 V 에서 S⁰(163.3 eV) 소멸 · Li₂S(160.3 eV) 성장, 충전 1.68 → 1.98 → 2.38 V 에서 역전. 캡션 *"Peaks corresponding to LPSCl remained unchanged throughout cycling"*.
- **P 2p (`Fig. S46`)**: 0.38–2.38 V(vs Li-In) 전 구간에서 P 2p 변화 없음 → 저자: 편석이 SE 의 가역 redox 를 돕는다. Zeier 그룹(ref 39)이 0.8 V vs Li-In 이상 하한을 권했는데 그보다 깊이 내려가도 환원 P 가 없다는 주장. ⚠ XPS 는 표면 수 nm 다.
- **S K-edge 10 h (`Fig. S47`, 실독)**: 방전 상태에서도 LPSCl 전연(≈2471 eV) 특징이 남고 Li₂S(≈2473 eV) 와 섞임 — 10 h 시료만 SM 에 있다(5 h 는 본문 추정).
- **Se K-edge (`Fig. S48`·`Fig. S49`, 실독)**: in situ — OCV 의 Se 백색선(≈12659.5 eV) 이 방전 1.0 V 에서 Li₂Se(≈12665) 로 연속 이동, 충전 3.0 V 에서 복귀. ex situ — 5 h 가 가장 가역, **400 rpm 방전은 거의 안 움직임**(≈1 eV) → 이용률 차이의 분광 근거.

### 5.9 다른 SE (`Fig. S25`·`Fig. S42`) — 할로겐 없는 대조에서 효과가 사라지나?
- SM 에 있는 것: SE 6종의 σ(`Fig. S42`) · LPSBr/LPSClBr/LPSClI 복합체 EDS(`Fig. S25`). **SS7 · LGPS 복합체의 셀 성능·EDS 는 SM 에 없다** → 본문에 있을 것으로 추정(본 적 없음).
- ⇒ **"할로겐 없는 SE 에서 효과가 사라진다" 는 SM 만으로는 확인 불가.** 이게 이 논문의 가장 중요한 대조인데 우리가 못 봤다. 본문 확보 1순위(§8 끝 · §15).
- ⚠ 확인되더라도 SS7(0.21 mS cm⁻¹)·LGPS(0.56) 는 LPSCl(0.44)·LPSClI(2.3)와 σ·기계물성·분해 경로가 다르다 — '할로겐 유무' 만 바꾼 대조가 아니다.

### 5.10 SE 의 용량 기여 정량 (`Table S6`·`Fig. S44`) ★
- **방법 ①(`Table S6`)**: 최고 달성 비용량 ÷ 칼코겐 이론값 − 1 ⇒ S 15 % · Se 44 % · **Te 105 %**. *"with assumption of full utilization of chalcogen"* — 칼코겐이 100 % 쓰였다고 **가정**한 **하한형 잔차**다(칼코겐 이용률이 100 % 미만이면 SE 기여는 그보다 크다).
- **방법 ②(`Fig. S44`, 실독)**: LPSCl : KB : C45 = 50 : 25 : 25 (S 없음) · **SE 로딩 8.8 mg cm⁻²**(= S 셀의 SE 로딩과 같음, §4) · 0.67 mA cm⁻² · 같은 창. CV 에서 ≈1.9 V 산화 · ≈1.3 V 환원 피크가 사이클마다 커짐. 면적용량 1 회 ≈1.37 → 5 회 ≈1.2 → 100 회 ≈0.88 mAh cm⁻² (figure-read ≈). S 2p: 방전 0.38 V 에서 **Li₂S 성분 뚜렷**, 충전 2.38 V 에서 소량 S⁰.
- ✎ **두 방법을 나란히 (우리 산수 · 정의가 다름)**: SE 단독 셀 ≈1.2 mAh cm⁻² ÷ S 셀 ≈6 mAh cm⁻²(1500 mAh g⁻¹ × 4 mg) ≈ **20 %** — `Table S6` 의 15 % 보다 크다. ⚠ SE 단독 셀은 탄소가 50 wt% 라 SE–탄소 접촉이 훨씬 많고, S 셀 안에서는 SE 와 S 가 Li 를 다툰다 → 둘 다 정확한 분리가 아니다. **Cronk26 처럼 dQ/dV 로 전위 영역을 갈라 SE 몫을 떼는 분석은 이 논문에 없다.**
- ⇒ **Li₂S/S 양극에서 SE redox 가 겉보기 용량에 얼마나 섞이나**: S 계에서 **최소 15 %(가정 하 잔차) · 대조 셀 비로 ≈20 %(우리 산수)**, Se 44 %, Te 에서는 **칼코겐 몫보다 SE 몫이 더 크다**. 이 논문의 "115 % 이용률" 은 **S 의 성능이 아니라 S + SE 의 합**이다 — 저자도 표로 인정했다.

### 5.11 일반화 · 조건 요약
- **칼코겐**: S · Se · SeS₂ · Te 네 가지 모두 2000 rpm 5 h 에서 작동(§3b). Se 는 Li₂Se 단일 단계 전환을 in situ XANES 로 확인.
- **SE**: Cl · Br · Cl/Br · Cl/I 아지로다이트 EDS 편석(정성). SS7·LGPS 결과는 본문.
- **로딩**: 기본 4 mg_S cm⁻² · Li 금속 셀 1.7 mg_S cm⁻² · 고S 조성도 4 mg_S cm⁻².
- **전류**: 0.67 mA cm⁻² (= 0.1C, 1C = 1675 mA g⁻¹ 기준 — 우리 산수 ✓) · 2차 인용 450 사이클은 1.4 mA cm⁻²(≈0.21C).
- **온도**: 25 °C. **스택압**: 70 (기본) · 54 (Li 금속) · 36 · 18 MPa. **음극**: Li-In(1:2 원자비, 0.38–2.38 V) 기본 · Li 금속(1.0–3.0 V).

## 6. 메커니즘 종합 (저자 서사 vs 근거의 사정거리)

| 고리 | 저자 문장 | 근거 | 우리 판정 (잠정) |
|---|---|---|---|
| ① UHS = 국소 고온 + 전단 | *"localized heating striking and shearing fracturing force"* (`Fig. S1`) | **온도 측정 0** · 도식 2장 | 🔴 미측정 |
| ② LPSCl 부분 분해 | *"decomposition of LPSCl"* (`Fig. S17` 캡션) | SE σ 0.44 → 0.01 (`Fig. S36A`) · 결정자 ↓ · 10 h 비정질화 | 🟡 **기계적 손상은 확실**, 화학 분해 생성물은 ③ 에서만 |
| ③ 나노 LiCl/LiBr 생성·편석 | *"segregation of nanosized lithium halides"* | STEM-EDS Cl:P 1.5–2.5 · Cl-L EELS · HRTEM 2.91 Å · SEM-EDS 지도 | 🟡 **Cl-풍부 · P-결핍 영역은 강한 근거**. 그 상이 **LiCl 결정**이라는 동정은 d 값 하나 + FFT · XRD 무음 · XPS 무력 · 리트벨트 점유 고정 |
| ④ 칼코겐 표면에 침착 | *"deposition onto the interface with chalcogen cathode particles"* | `Fig. S26`·`Fig. S31` (Se 둘레 Cl) | 🟢 Se 에서는 그림이 일관 · S 는 cryo 한 장(`Fig. S11`) |
| ⑤ 계면 수송 ↑ → 이용률·수명 | *"substantially improves effective ionic transport"* | D_Li 196 배(겉보기) · 압력 회복 · CT 두께 | 🔴 **편석만의 기여는 분리 안 됨** — SE 선밀링 대조는 σ 손상과 교락, 1500 rpm 은 편석 약한데 성능 대부분 확보, 열처리는 S 용융과 교락 |

## 7. 우리 대비 (li2s 트랙 · 잠정 — 외부 1저자 판단 전)

> ⛔ 이 절은 우리 쪽 숫자를 새로 옮기지 않는다. 우리 기록은 경로만 적고, 소셀 유리 결과는 **마감 카드의 허용 서술 범위 안에서만** 말한다. 소셀 유리의 Li 수송 계수·Ea 는 보고하지 않는다.

| 항목 | 이 논문 | 우리 (li2s 트랙) | 같음 / 다름 / 왜 |
|---|---|---|---|
| 활물질 | **원소 S**(·Se·Te) — 녹는점 낮고(S ≈115 °C) 무르며 혼합 중 비정질화·이동 | **Li₂S** — 녹는점 ≈938 °C, 단단한 이온결정 | 🔴 **다르다**. 논문 기전 고리 (2) *"the low melting points of chalcogen cathodes facilitate their migration"* (`Fig. S17` 캡션) 는 Li₂S 에 **옮겨지지 않는다** |
| 계면상 모델 | **Cl 이 LiCl(LiX) 로 갈라져 칼코겐 표면에 편석** — 화학적으로 불균일 | 소셀 유리 a-Li₄PS₄Cl (= a-Li₃PS₄·LiCl **균질** · Cl 이 유리망 안에 고르게) — `db/properties/lpscl_smallcell_glass_md_v2_closed_2026_10_05.json` · `lpscl_li2s_interphase_prereg_2026_09_11.json` | 🟠 **가정이 정면으로 다르다** — 우리 모델은 '편석 0' 끝점이고 이 논문은 '편석된' 끝점을 관측했다고 주장한다(S 계에서) |
| 할로겐 없는 대조 | SS7 · LGPS (결과는 본문 · 미확인) | **대조 계 a-Li₃PS₄** (B) — `lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json` (ratified · 결과 전) | 🟢 **설계 의도가 맞물린다**. 다만 우리 B 는 'Cl 이 계에서 빠진 매트릭스' 이고, 논문이 말하는 상태는 'Cl 이 **LiCl 로 따로 서 있는** 매트릭스' 다 — B 는 그 절반(매트릭스 쪽)만 답한다 |
| 평형 생성물 | LPSCl 열분해 시 LiCl 생성 (`Fig. S14`) | 0층(post-hoc): Li₂S–LPSCl 조성선의 분해 산물 = {Li₃PS₄, LiCl, Li₂S} — `lpscl_li2s_hull_layer0_2026_09_11.json` §6 · 준안정 층위 반응식(LiCl 생성)은 **산술 힌트**(같은 파일 §7 · 마감 `lpscl_li2s_layer1_closed_2026_09_15.json` 허용 서술 "0층") | 🟢 **방향은 같다** (LPSCl 이 무너지면 LiCl 이 나온다). ⚠ 우리 것은 0 K 결정 평형 + 판정 아닌 산술, 논문은 수백 °C 가열 실측 — 층위가 다르다 |
| 공정 | Thinky 2000 rpm 5 h · S+SE+C 동시 | 우리 계산은 공정을 모사하지 않는다 (prereg §1c) | — |
| 무질서 | 원료 LPSCl 4d Cl 0.615 (고정값으로 보임) | comp1 은 질서 배열 52 원자 셀 (4a/4d 섞임 표현 안 함 — prereg §1b) | 비교 대상 아님 (같은 칸에 놓지 않는다) |
| 계산 | **0** | UMA MLIP-MD 소셀 유리 (상대차만 인용) | 비교할 계산값 없음 |

**허용 서술 범위 안에서 우리가 말할 수 있는 것 (마감 카드 그대로)** — v2 마감의 허용 문장: *"600 K 에서는 재현됐으나 (N₆₀₀ ≥ 3/5), 550 K 는 800 ps 로도 과반이 게이트를 통과하지 못했다 … 이 프로토콜에서 게이트를 안정적으로 통과하는 온도는 600 K 이며, 550 K 는 문턱 부근이다."* — 이 문장 외의 수송 서술은 하지 않는다. 대조 계 카드는 `'LiCl 이 Li 수송을 빠르게/느리게 한다' 를 600 K·이 셀 밖으로 넓히지 않는다 · 기구(왜)를 말하지 않는다` 를 이미 금지로 박았다 — **이 논문의 '편석 LiX 가 수송을 돕는다' 를 우리 대조 계 결과의 해석에 끌어오지 않는다.**

**잠정 읽기 (외부 1저자에게 보낼 질문 후보)**
1. 이 논문은 **S** 계다. Li₂S 계에서 같은 편석이 생기는지는 이 논문이 답하지 않는다. 다만 `Fig. S14`(S 없이 LPSCl+C 만으로 LiCl)는 *칼코겐 종류와 무관하게 LPSCl 이 열·기계적으로 무너지면 Cl 이 LiCl 로 나올 수 있다* 를 시사한다 → 우리 '균질 Cl 유리' 모델은 **두 끝점 중 하나**로 명시하는 것이 정직하다.
2. 대조 계 카드(A 균질 a-Li₄PS₄Cl vs B a-Li₃PS₄)는 "Cl 이 유리망 안에 있을 때 vs 없을 때" 를 묻는다. 이 논문이 제기하는 세 번째 상태 "Cl 이 **LiCl 나노상으로 따로**" 는 **새 카드가 필요한 질문**이고, 120 원자 셀로는 LiCl 나노상 + 매트릭스 계면을 담기 어렵다 (셀 크기 질문 — 보고량 카드 먼저).
3. [Cronk26] 의 Li₂S+LPSCl 볼밀은 *"LPSCl → LPS-like"* 를 말하고 Cl 행방을 보고하지 않았다. 이 논문은 S 계에서 Cl 행방을 'LiCl 편석' 으로 답한다. 두 논문을 합치면 *밀링 계면상 = LPS-like 매트릭스 + (편석 또는 용해된) Cl* 이라는 2-변수 그림이 되고, 우리 A/B 대조는 그중 '용해 vs 부재' 축을 잰다.

## 8. DFT/계산 방법 ★

- **계산 0.** SM 전체(67 쪽)에 DFT · AIMD · MD · MLIP · NEB · hull 계산이 없다. 유일한 계산은 **HRTEM 이미지 시뮬레이션**(MATLAB 결정 모델 LiCl [110] · Se [212] · 200 kV · Cc 1 mm · Cs 0.5 mm · 두께 ≈4 nm · Δf 40 nm)과 **투영 셀 에너지밀도 계산**(`Fig. S2A`, LPSCl 막 30 µm 파우치 가정 · 식 미기재)이다.
- **홉 수 검산**: 이 논문에 Ea·장벽 값이 **없다** → 해당 없음.
- **관측창 규칙**: 짧은 MD 의 '반응 없음' 서술 **없음** → 해당 없음. (in situ TEM 의 '변화 없음'(`Fig. S9C`, cryo 107.5 s)은 MD 가 아니라 실측이다.)
- **흡착 배위수 규칙**: 결합에너지 값 **없음** → 해당 없음.
- 본문에 계산이 있는지는 **미확인**(SM 의 Methods 목록에 계산 절이 없으므로 없을 가능성이 높다).

## 9. 실험 쪽 최고 조건과의 프로토콜 차이 ★★ (주간보고 2026-10-05 · 작성자 표기 없음 · 슬라이드에서 읽은 값 = figure-read ≈)

| 변수 | 이 논문 (2000 rpm 5 h 기본) | 이 논문 고S 변형 | 실험 쪽 ③ (최고 · ≈400–430 mAh g⁻¹ 가역 @60 °C, figure-read ≈) | 실험 쪽 ② (≈150–200 @60 °C) | 실험 쪽 ① (≈15 @45 °C) |
|---|---|---|---|---|---|
| 활물질 | **원소 S** | 원소 S | **Li₂S** | Li₂S | Li₂S |
| 조성 (활물질 : SE : 탄소) | 22.75 : 50 : 27.25 | **32.5 : 50 : 17.5** | **30 : 50 : 20** | 30 : 50 : 20 | 30 : 50 : 20 |
| 탄소 | **KB + C45** | **KB 만** | **KB 만** | (슬라이드 미표기) | Super P (손혼합) |
| 고에너지 단계에 들어간 것 | **S + SE + KB + C45 동시** | S + SE + KB 동시 | **Li₂S + KB 만** — LPSCl 은 그 뒤 **손·vortex** | Li₂S + LPSCl + C 동시 | Li₂S + LPSCl |
| 장비 | THINKY AR-100 + ZrO₂ 볼 | 같음 | Thinky (모델 슬라이드 표기 확인 필요) | **유성 볼밀** 500 rpm | 유성 볼밀 500 rpm (Cronk 방식) |
| 속도 · 시간 | 2000 rpm · **총 5 h** (30 분 × 10) | 2000 rpm · 5 h | 2000 rpm · **1 h** (30 분 × 2) | 500 rpm · 1 h | 500 rpm · 1 h |
| 볼 : 분말 | **5 : 1** | 5 : 1 | **5 : 1** · 배치 1 g | (미표기) | 30 : 1 |
| 로딩 | 4 mg_S cm⁻² | 4 mg_S cm⁻² | 1.5 mg cm⁻² (무엇 기준인지 슬라이드 확인 필요) | 같음 | 같음 |
| 온도 · 율 | **25 °C** · 0.1C | 25 °C · 0.1C | **60 °C** · 0.05C 형성 → 0.2C | 60 °C | 45 °C |
| 음극 · 스택 | Li-In · 70 MPa | 같음 | SUS\|양극\|SE\|LiIn\|SUS (압력 미표기) | 같음 | 같음 |

**읽기 (잠정)**
1. **실험 쪽 ③ 은 논문의 '할라이드 편석' 단계를 하지 않았다.** 논문 자신의 대조 `Fig. S33` 은 *SE 를 따로 처리하고 저에너지로 섞으면 Cl/P ≈1 = 편석 없음* 을 보였다. ③ 은 LPSCl 이 고에너지 단계에 아예 없으므로, 논문 논리로는 **편석이 생길 수 없는** 경로다.
2. 그러면 ③ 의 이득은 무엇에서 왔나 — **논문 SM 이 지지하는 후보 둘**:
   - (a) **SE 를 망가뜨리지 않았다.** `Fig. S36A`: 2000 rpm 처리만으로 LPSCl σ 가 1 h 에 4배, 5 h 에 44배 떨어진다. ②(SE 동시 볼밀)·과거 Thinky 반복 조건이 SE 를 같이 갈았다면 SE σ 손상을 같이 샀을 것이다. ③ 은 SE 를 손·vortex 로만 넣어 **원료 σ 를 지켰다**. (실험 쪽 ① 은 Cronk 방식으로 Li₂S+LPSCl 을 볼밀한 경우라 이것과 같은 방향의 손상이 있었을 수 있다 — [Cronk26] 에서도 LPSCl 단독 10 h 밀링 σ 가 크게 떨어졌다.)
   - (b) **활물질–탄소 접촉 · 활물질 분쇄.** `Fig. S27`(탄소 격자줄무늬가 Se 표면에) · `Fig. S18` 캡션(*"carbon … worked as milling media"*) · `Fig. S12` 도식(*"shear forces … reduce the particle size of chalcogen cathodes"*). Li₂S 는 전자 절연체라 **Li₂S–KB 의 나노 접촉**이 전환 반응의 전자 경로를 만든다. ③ 은 바로 그 단계(Li₂S + KB 고에너지 혼합)만 했다.
   - ⚠ 논문은 (a)·(b) 를 '편석' 과 **분리하지 않았다**(§5.6). 그래서 ③ 의 성공이 논문의 편석 가설을 지지하지도 반증하지도 않는다. 오히려 ③ 은 논문에 **없던 대조** — '편석 없이 활물질–탄소만 고에너지' — 의 Li₂S 판이다.
3. **조성은 논문의 고S 변형(32.5 : 50 : 17.5 · KB 만)에 가장 가깝다.** 그 변형은 `Fig. S39` 에서 ≈6 mAh cm⁻² 를 냈다(figure-read). 즉 *KB 단독이 편석을 줄인다*(`Fig. S18`)는 EDS 관찰에도 불구하고 **KB 단독 조성으로도 성능이 났다** — 실험 쪽이 KB 만 쓴 것이 논문 기준으로 결정적 결함은 아니다.
4. **SE 용량 기여**: 실험 쪽은 LPSCl 이 50 wt% 다. 논문 `Fig. S44`·`Table S6` 이 보여 주듯 SE 는 같은 창에서 용량을 낸다. ③ 의 400–430 mAh g⁻¹ 중 얼마가 Li₂S 몫인지는 **SE 단독 대조 셀 없이 모른다**(§15 실험 제안 1).
5. **시간 차이**: 과거 Thinky 2000 rpm **10 회 반복 = 30 분 × 10 = 논문의 5 h 와 같은 혼합 시간**이다(우리 산수 · 반복 1 회 = 30 분이라는 가정). 그 조건이 ≈30–120 mAh g⁻¹ 에 그쳤다면, **그때 LPSCl 이 같이 들어갔는지**가 결정적 질문이다 — 들어갔다면 논문의 Li₂S 판 재현이 실패한 기록이고, 안 들어갔다면 Li₂S+KB 의 과혼합(1 h 보다 나쁨)을 뜻한다. 주간보고만으로는 갈리지 않는다.
6. **온도**: 논문 25 °C · 실험 60 °C. 60 °C 에서 SE 분해·SE redox 기여가 커질 수 있다 — 같은 온도 비교가 아니다.

## 10. 주의 · 한계 (over-claim 방지)

① **본문 미확보** — 본문 그림 1–4 의 대표 EDS/EELS·성능·SS7/LGPS 대조를 못 봤다. 아래 비판 중 일부는 본문에서 풀릴 수 있다.
② **편석 ↔ 성능 상관은 정성** — 1500 rpm 에서 Cl/P(원자비) 1.14 로 거의 화학량론인데 성능은 400 rpm 대비 40 배 · 2000 rpm 의 2/3. "편석이 지배" 보다 "혼합 에너지가 지배" 가 SM 자료와 더 잘 맞는다 (우리 읽기).
③ **열처리 대조(`Fig. S43`)의 교락** — 115·145 °C 는 S 녹는점(≈115 °C) 이상이라 용융확산과 구분 불가.
④ **SE 선밀링 대조(`Fig. S33`)의 교락** — SE σ 44 배 손상과 편석 부재가 겹침(저자도 둘 다 적음).
⑤ **'heat striking' 미측정** — 용기 온도·국소 온도 측정 0. in situ 가열의 LiCl 문턱은 수백 °C (figure-read).
⑥ **같은 논문 안의 긴장** — `Fig. S18`(KB 단독 → 편석 적음) vs `Fig. S39`(KB 단독 고S 조성 → ≈6 mAh cm⁻²).
⑦ **Cl/P 비 기준 혼동** — `Fig. S34` 의 "1.3" 은 wt% 비(11.7/9.0)이고 원자비로는 1.14; `Fig. S33` 의 "≈1" 은 wt% 로 1.13 · 원자비 0.99. 무게비의 화학량론 기준은 1.145 다. `Fig. S26` 의 Cl:P 1.5–2.5 가 무게비인지 원자비인지 **미기재** — 무게비라면 원자비로 1.3–2.2 (우리 산수).
⑧ **Raman 미동정 피크** — `Fig. S19D` 5 h 복합체의 ≈242 cm⁻¹ 피크 · LPSCl 425 cm⁻¹ 의 거의 소멸이 캡션 서술("LPSCl 유지")과 어긋난다 (figure-read).
⑨ **rpm 비교의 단위 문제** — `Fig. S3`·`Fig. S40B` 가 유성 볼밀 rpm 과 원심 혼합기 rpm 을 한 축에 놓는다. 투입 에너지(볼 질량·궤도 반경·가속도)가 다르다.
⑩ **이용률 115 % 는 S 성능이 아니다** — `Table S6` 정의상 SE 몫 포함. Te 는 205 %(SE 105 %).
⑪ **리트벨트 점유 고정** — Cl 이탈을 회절로 보이지 않았다. a 변화 −0.044 % 는 크기·변형·비화학량론 어느 것으로도 설명 가능.
⑫ **HRTEM LiCl 동정** — d 하나(2.91 Å, LiCl(111) 대비 2 % 차) + FFT. 대안 상 배제 절차 미기재.
⑬ **in situ TEM 은 대비만** — 가열 중 화학 동정 없음 · 고진공 Se 증발 · 레이저 온도 미측정. Movie S1 의 00:40 ↔ 04:30 프레임은 눈으로 보기에 대비 변화가 미미하다 (판독).
⑭ **스택압 해석** — Li-In 음극이 압력 변화를 지배한다고 저자 스스로 씀 → 양극 부피 거동 결론은 약함.
⑮ **SS7 조성 미기재** — "할로겐 없는 아지로다이트" 의 정체가 공급사 이름뿐.
⑯ **EELS 수치 불일치** — `Fig. S11` 그림 라벨(167.8/165.6/166.5 eV)과 캡션(168.6/166.6 eV).
⑰ **`Fig. S2` 캡션 "6 mAh cm⁻² · 450 cycles" ↔ 별 위치 ≈5 mAh cm⁻²** (figure-read).

## 11. Figure set ★ (본 그림 / 안 본 그림은 §16)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| S1 | 도식: 저속 혼합(공극·접촉 상실) vs UHS(편석 → 수송·이용률·안정성). 용기 그림에 볼이 없다 | 개념도로만 — 근거 아님 |
| S2 | 문헌 비교: S 로딩–투영 에너지밀도(이용률 등고선) · 면적용량–사이클 수명. 별 ≈630 Wh kg⁻¹ · ≈5 mAh cm⁻² @450 (figure-read) | 실험 쪽 셀을 같은 평면에 찍을 틀 |
| S3 | 혼합 속도–S 이용률 문헌 지도. 문헌은 0–600 rpm, 별만 2000 rpm | ⚠ 장비가 다른 rpm 을 한 축에 둔 반면교사 |
| S4 | 2000 rpm 5 h SEM-EDS: S/C 응집체에 Cl 강·P 약 · 옆 LPSCl 입자는 P 강 | 실험 쪽 Cl/P 지도 판독 기준 그림 |
| S5 | 2000 rpm 1 h SEM-EDS: 편석 약함 | 시간 의존 |
| S6 | 400 rpm 5 h SEM-EDS: P·Cl 동위치 = 편석 없음 | 음성 대조 모양 |
| S7 | cryo-TEM 셋업 · RT 전자선 손상 · 공기 3 분 O 증가 (캡션만 읽음) | cryo 규율 체크리스트 |
| S8 | 저선량 노출시간–SNR (캡션만) | — |
| S9 | RT vs cryo 시간계열 손상 (캡션만) | — |
| S10 | cryo HRTEM · SAED [111] · (220) 3.57 Å (캡션만) | — |
| S11 | S/LPSCl/C 5 h EELS: 저대비 가장자리 "S⁰ + Cl-rich" · 내부 "Sⁿ⁻ + Cl-deficient" | 나노 편석 S 계 유일 근거 · 라벨/캡션 수치 불일치 |
| S12 | 도식: ZrO₂ 볼 사이 전단 + 마찰열 → LiX | 기전 주장의 원문 도식 |
| S13 | in situ 가열 SXRD S+LPSCl+C 손혼합 30–400 °C: S 비정질화, LiCl 출현 | LiCl 문턱 온도 — 그림상 ≈300 °C 위 (figure-read) |
| S14 | in situ 가열 SXRD LPSCl+C 40–500 °C: LPSCl 피크 소멸과 LiCl (111)/(200) 출현이 동시 | **LiCl = LPSCl 열분해 산물** 의 실측 — 우리 0층 산물 목록과 같은 방향 |
| S15 | 손혼합 vs 145 °C 3 h: EDS 점 스펙트럼 Cl 증가 | 점 하나 비교 — 약한 근거 |
| S16 | 레이저 1 mW in situ TEM (Se/LPSCl/C 0.5 h): LPSCl/C 대비 변화 · Se 영역 공극 | Movie S1 정지 판 · 온도 미측정 |
| S17 | 열전 가열 20–220 °C in situ TEM · 회색값 정량 (Se ≈122 → 74 · LPSCl/C ≈45 → 132) | Movie S2 정지 판 · 화학 동정 없음 |
| S18 | KB · C45 SEM · 단일 탄소 복합체 EDS: 편석 적음 | 실험 쪽 KB 단독 판단 시 `Fig. S39` 와 같이 볼 것 |
| S19 | SXRD(LiCl 피크 없음) · 격자상수/결정자 · PDF(S₈ 4.5 Å 소멸) · Raman(≈242 cm⁻¹ 미동정) | 리트벨트 수치의 그림판 |
| S20 | 원료 LPSCl · S 의 XPS (미실독) | — |
| S21 | 처리별 Cl 2p(불변) · Li 1s(≈0.1–0.2 eV 이동) · S 2p(S⁰ 감소) | XPS 로 LiCl 동정 불가의 근거 |
| S22 | P 2p 원료 vs UHS 5 h — 불변 | 환원 P 없음 |
| S23 | Se 복합체 2000 vs 400 rpm SEM-EDS | 칼코겐 일반화 |
| S24 | SeS₂ · Te 복합체 SEM-EDS | Te 는 편석 판독 애매 |
| S25 | LPSBr · LPSClBr · LPSClI 복합체 SEM-EDS | I 신호 바탕 수준 |
| S26 | Se/LPSCl/C 5 h STEM-EDS 6 영역 · Cl:P 2.5–1.5 | **편석 정량 핵심** — 실험 쪽이 따라 잴 지표 |
| S27 | Se 입자 TEM · EDS · 표면 탄소 격자줄무늬 | 활물질–탄소 나노 접촉 근거 (§9 읽기 2b) |
| S28 | Cl-L₂,₃ EELS 영역 i–v + KCl (본문 그림 2D 박스) | 위치 그림은 본문 |
| S29 | HAADF-EDS Se/LPSCl/C · S/Se + LPSCl/LPSBr EDS 스펙트럼 | Br-Lα / Se-Lα 겹침 주의 |
| S30 | HRTEM: LiCl 2.91 Å · Se 3.78/3.02 Å · 탄소 3.39 Å | LiCl 동정의 전부 |
| S31 | HRTEM 계면: Carbon\|LiCl\|Se · Se\|LiCl\|Se (띠 ≈10–15 nm, figure-read) | 편석층 두께 규모 |
| S32 | 400 rpm 5 h 셀: ≈1.07 → 0.08 mAh cm⁻² | 음성 대조 셀 |
| S33 | SE 선밀링 + 400 rpm: 편석 없음 · 1 회 ≈27 mAh g⁻¹ | ⚠ σ 손상과 교락된 대조 — **실험 쪽 ③ 과 정반대 배치**(SE 를 갈고 활물질은 약하게) |
| S34 | 1500 rpm 5 h: Cl/P "1.3"(wt) · 25 회 ≈1040 mAh g⁻¹ | 편석 약해도 성능 대부분 |
| S35 | 10 h SEM-EDS · SXRD (LPSCl 비정질화) | 과혼합 |
| S36 | LPSCl σ 0.44 → 0.11 → 0.01 → 0.002 mS cm⁻¹ · Randles–Ševčík 기울기 | **실험 쪽이 SE 를 고에너지 단계에서 뺀 이유의 정량 근거** |
| S37 | in situ 스택압: 방전 −3.1/−4.3/−5.25 · 충전 후 −1.45/≈0/−2.45 MPa | 압력 회복 지표 |
| S38 | Li 금속 대극 1.7 mg cm⁻² · 100 회 후 2.45 mAh cm⁻² | 음극 조건 차이 |
| S39 | 고S 32.5 : 50 : 17.5 (KB 만) · ≈6 mAh cm⁻² 50 회 | **실험 쪽 조성에 가장 가까운 논문 조건** |
| S40 | 36 · 18 MPa 전압곡선 · 이용률–rpm–압력 지도 | 저압 데이터 |
| S41 | Se · SeS₂ · Te 전압곡선 · 속도 | 일반화 |
| S42 | SE 6종 σ: LPSCl 0.44 · LPSBr 0.94 · LPSClBr 1.04 · LPSClI 2.3 · SS7 0.21 · LGPS 0.56 mS cm⁻¹ | SE 원료 σ 기준 |
| S43 | 1 h UHS + 100/115/145 °C 열처리 셀 | ⚠ S 용융과 교락 |
| S44 | LPSCl/C (S 없음) CV · 사이클(≈1.2 mAh cm⁻² @ SE 8.8 mg cm⁻²) · S 2p | **SE 용량 기여 대조 셀의 원형** — 실험 제안 1 |
| S45 | S 2p 방전/충전 전개 | 반응 경로 |
| S46 | P 2p 방전/충전 — 불변 | 0.38 V 까지 환원 P 없음 (표면) |
| S47 | S K-edge 10 h 방전/충전 | — |
| S48 | in situ Se K-edge 방전/충전 | Se → Li₂Se 단일 단계 |
| S49 | ex situ Se K-edge 시간·속도 비교 | 400 rpm 방전 거의 안 움직임 |
| S50 | in situ µ-CT 셋업 · 양극 ≈60 µm 두께 불변 | 복셀 미기재 |
| Table S1 | 전략별 비교 (촉매·도핑·벌크 할라이드·코팅·습식·이 연구) | 문헌 지형 — 온도 열이 있다 |
| Table S2 | 원료 LPSCl 리트벨트 (a 9.85082 Å) | 점유 고정 확인용 |
| Table S3 | 2000 rpm 1 h LPSCl 리트벨트 | — |
| Table S4 | 2000 rpm 5 h LPSCl 리트벨트 (a 9.84649 Å) | — |
| Table S5 | 400 rpm 5 h LPSCl 리트벨트 | — |
| Table S6 | 칼코겐 이용률 · SE 용량 기여 (S 15 % · Se 44 % · Te 105 %) | **SE 기여 정량 정본(가정 하 잔차)** |

**동영상 (`figures/<slug>/movie_S*.png`)**: Movie S1 (레이저 가열, 20× 재생, 15.8 s) — `movie_S1_t04.png`(오버레이 00:40) · `movie_S1_t15.png`(04:30): 마름모꼴 Se/LPSCl/C 덩어리 + 주변 입상 LPSCl/C. 두 프레임 사이 변화는 눈으로 보기에 미미하다. Movie S2 (열전 가열 20 → 220 °C, 15× 재생, 16.0 s) — `movie_S2_t04.png`(00:30) · `movie_S2_t15.png`(03:22.5): **왼쪽 위 노출 Se 입자가 사라지고 껍데기 윤곽만 남음** · 가운데 Se/LPSCl/C 입자는 더 어둡고 고르게 · 온도 표시는 프레임에 없다. 둘 다 **대비 변화 영상**이고 화학 정보는 없다.

## 12. Post-processing / 도구 (논문)
- **Rietveld**: GSAS-II (방사광 XRD). 결정자 크기·a·U_iso 보고, 점유는 고정으로 보임.
- **PDF**: NSLS-II 28-ID-1 (처리 소프트웨어 미기재).
- **EELS**: power-law 배경 제거 + Fourier-ratio 다중산란 제거.
- **in situ TEM**: DigitalMicrograph Drift Removal(서브픽셀) · 프레임 차분(`Fig. S17E,F`) · 회색값 0–255 정량(`Fig. S17G`).
- **HRTEM 시뮬레이션**: MATLAB 자작 스크립트 (LiCl [110] · Se [212]).
- **XPS**: C 1s 285.0 eV 보정 · Shirley 배경 · 공기차단 이송.
- **XANES**: Athena.
- **µ-CT**: ImageJ.
- **EIS**: Z-view 등가회로, σ = L/(R_b·A).
- **D_Li**: Randles–Ševčík (I_p ∝ v¹ᐟ²) 기울기 비.

## 13. 적용 인사이트 — 다음 실험·계산 제안 (우선순위 · 잠정)

**실험 쪽 (실험 1저자 판단 · 우리는 제안만)**
1. **SE 단독 대조 셀** — LPSCl + KB 를 ③ 과 **같은 혼합 경로**(손·vortex)·같은 SE 면적 로딩·같은 창·60 °C 로 돌려 SE 몫을 뺀다 (`Fig. S44` 방법). 50 wt% LPSCl 이면 이것 없이는 Li₂S 이용률을 말할 수 없다.
2. **'SE 를 고에너지 단계에 넣느냐' 단일 변수 분할** — Li₂S+KB Thinky 1 h 고정 뒤 (a) LPSCl 손혼합(현재 ③) (b) LPSCl 도 Thinky 에 같이 1 h (c) LPSCl 만 Thinky 1 h 후 손혼합. 각 단계 뒤 **LPSCl σ(EIS)** 와 **SEM-EDS Cl:P(원자비로 환산해서)** 를 같이 잰다 (`Fig. S36A`·`Fig. S26` 방법). 논문의 핵심 주장이 Li₂S 계에서 성립하는지 가르는 최소 실험이다.
3. **과거 Thinky 10·15 회 반복 조건의 투입물 확인** — LPSCl 이 같이 들어갔는지 기록으로 확인(§9 읽기 5). 들어갔다면 그것이 이 논문의 Li₂S 재현 실패 기록이다.
4. **KB vs KB+C45** — 논문은 이중 탄소를 '밀링 매체' 로 정당화했지만(`Fig. S18`) 자기 고S 조성은 KB 만이다(`Fig. S39`). ③ 에 C45 추가 한 조건이면 갈린다.
5. **25 °C 측정 한 점** — 논문과 같은 온도에서 ③ 을 재면 비교가 처음 성립한다.

**계산 쪽 (li2s 트랙 · 외부 1저자 회신 필요 · ⛔ 전부 보고량 카드 먼저)**
1. **이미 비준된 대조 계 카드(a-Li₃PS₄ B)를 그대로 진행** — 이 논문은 그 카드의 동기를 강화하지만 카드의 보고량·허용 문구를 바꾸지 않는다. 결과 해석에 이 논문의 '편석 LiX 가 수송을 돕는다' 를 끌어오지 않는다 (§7).
2. **세 번째 상태 'Cl 이 LiCl 나노상으로 분리' 를 물을지** — 질문 후보: *같은 조성에서 Cl 이 유리망에 녹아 있을 때(A) vs LiCl 로 분리됐을 때(A′), 매트릭스의 Li 이동성이 다른가.* ⚠ 120 원자 셀로 LiCl 나노상 + 계면을 담을 수 있는지(셀 크기) · '분리 상태' 를 어떻게 만들지(admissible state 선언) 가 카드 §3 에서 먼저 막힌다 — **보고량 카드 없이는 던지지 않는다**.
3. **값싼 열역학 링크 (계산 0 · 기존 원장 재읽기)** — 0층 분해 산물 목록 {Li₃PS₄, LiCl, Li₂S} 과 이 논문 `Fig. S14`(LPSCl 열분해 → LiCl)의 대응을 외부 1저자에게 **관측 접점 후보**로 보고. 판정 아닌 산술(0층 post-hoc) 지위를 그대로 달고.

## 14. 인용 가능 문장 (deck/paper 용, 방어 가능한 형태)
- "Ultrahigh-speed (2000 rpm) centrifugal mixing of elemental chalcogens with halide argyrodites produced Cl-rich, P-deficient regions at chalcogen surfaces (STEM-EDS Cl:P 1.5–2.5) and lattice fringes assigned to LiCl (Lee et al., Science 2025, SM Figs. S26, S30)."
- "The same processing reduced the ionic conductivity of Li₆PS₅Cl from 0.44 to 0.01 mS cm⁻¹ after 5 h (SM Fig. S36A)."
- "In that work the apparent sulfur utilization of 115 % includes a solid-electrolyte redox contribution estimated as 15 % under the assumption of full sulfur utilization (SM Table S6)."
- ⛔ 쓰지 않는다: "Halide segregation is the origin of the high utilization" (SM 에서 분리 안 됨) · "LiCl forms at the interface during Li₂S cathode mixing" (S 계 결과).

## 15. 미니 용어집
- **UHS mixing**: ultrahigh-speed mixing — 여기서는 THINKY 원심 혼합기 2000 rpm + ZrO₂ 볼.
- **planetary centrifugal mixer**: 용기가 자전하면서 공전하는 혼합기. 유성 볼밀과 비슷한 운동이지만 용기·볼·가속도가 달라 rpm 이 같은 에너지가 아니다.
- **halide segregation (할라이드 편석)**: 균일하던 할로겐이 한쪽(여기서는 칼코겐 표면)으로 모여 별도 상(LiX)을 이루는 현상.
- **EELS L₂,₃ edge**: 2p 내각 전자를 들뜨게 하는 손실 문턱. S ≈165 eV · Cl ≈200 eV. 문턱 위치가 산화상태에 따라 움직인다.
- **Randles–Ševčík**: CV 피크 전류 I_p ∝ n³ᐟ² A C D¹ᐟ² v¹ᐟ². 같은 셀 형식이면 기울기² 비가 겉보기 D 비.
- **Rietveld 점유 고정**: 자리 점유를 정련 변수로 풀지 않고 넣어 둔 값으로 묶는 것 — 그러면 점유 변화(여기서는 Cl 이탈)를 볼 수 없다.
- **melt-diffusion**: S 를 녹는점(≈115 °C) 위로 가열해 탄소 기공에 스며들게 하는 표준 S/C 복합 공정.
- **figure-read ≈**: 그림에서 눈으로 읽은 값(본문 명시값 아님).

## 16. 본 그림 / 안 본 그림 (2026-10-06)
- **본 쪽 · 텍스트**: SM 67 쪽 **전부** pdftotext 로 읽었다 (part1 p.1–30 · part2 p.31–67, 참고문헌 68 건 포함).
- **Read 로 본 그림 (크롭 56 장 = 그림 50 + 표 6 중 그림 45 장 + 표 2 장 · 동영상 프레임 4 장)**: `Fig. S1`–`Fig. S6` · `Fig. S11`–`Fig. S19` · `Fig. S21`–`Fig. S50` · `Table S1` · `Table S6` · Movie S1 2 프레임 · Movie S2 2 프레임.
- **안 본 그림**: `Fig. S7`·`Fig. S8`·`Fig. S9`·`Fig. S10` (cryo-TEM 방법론 — 캡션만) · `Fig. S20` (원료 XPS 기준 — 캡션만) · `Table S2`–`Table S5` (이미지는 안 봤고 pdftotext 숫자로 읽음 — 표는 텍스트가 더 정확).
- **크롭 방법**: `tools/litdb/extract_figures.py` 자동 49 장 · `Fig. S16`(캡션 번호 뒤 마침표 누락으로 앵커 실패) 과 `Table S1`–`Table S6`(캡션이 표 **아래**라 '백지' 로 버려짐)은 **손으로 잘라** `figures.json` 에 `manual_crop` 사유를 달았다. 동영상 프레임은 ffmpeg (`figures.json` 의 `movies`).
- **본문 그림 1–4: 본 적 없음.**

## 17. 한 줄 결론
이 논문은 *"할로겐 아지로다이트를 칼코겐·탄소와 함께 2000 rpm 으로 오래 섞으면 Cl-풍부 상이 칼코겐 표면에 생긴다"* 를 나노 분광으로 꽤 설득력 있게 보였지만, **그 상이 성능의 원인이라는 것은 SM 안에서 SE 손상·혼합 에너지·S 용융과 분리되지 않았다.** 실험 쪽의 최고 조건(Li₂S+KB 만 Thinky · SE 는 나중에 손혼합)은 이 논문의 편석 단계를 **건너뛴** 경로이며, SM 이 지지하는 그 이득의 후보는 *SE 손상 회피*와 *활물질–탄소 나노 접촉*이다 — SE 단독 대조 셀과 'SE 를 Thinky 에 넣느냐' 단일 변수 분할이 다음 실험이다.
