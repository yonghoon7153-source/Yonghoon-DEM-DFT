<!-- 표준 양식 확장 (paper-level STANDALONE). ★ = 1저자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = lee2025_heckel_argyrodite_powder_densification_nanoindentation.md (같은 "1.64" 문제를 처음 짚은 카드).
     쪽 표기 = PDF 쪽 (PDF p.1 = IOP 내려받기 표지 · 논문 본문 = PDF p.2–11 · 인쇄 쪽 번호 없음 · e-location 100525).
     SI 는 받지 못했다 — 본문이 "Supplementary material for this article is available online" 이라 적고 Fig. S1–S7 을 부른다 → 그 내용은 전부 [미확인].
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (±15 % 감각 · 경향 전용) ·
     [우리 산술] = 이 논문 밖 값 (정본 카드 · CLAUDE.md) 과 엮은 계산 (식은 그 자리에) · [정본 카드] = 다른 litdb 정본 카드가 적은 값 ·
     [미확인] = 본문 전수에 없음 (SI 미입수라 "원문에 없다" 고 단정하지 않는다) · [추정] = 해석.
     원문 11 쪽 전부 렌더 이미지 (100 dpi) + pdftotext 로 읽었고, 인용문 · 표 칸은 300 dpi 크롭으로 다시 대조했다.
     PDF md5 923ed2014660ddb1a95d56d36a97700e (묶음 main.pdf = 업로드 78d3dc02 사본과 같음). 정본 대조 판 = f98988e6c. -->
# 상압 (스택압 0.20–0.28 MPa) Li/Li₆PS₅Cl/Li 대칭셀의 임계 전류 밀도 (CCD) — 셀 지그 · 전해질 두께 · Li 원천이라는 '숨은 변수' 와 galvanodynamic 분극 (Tafel 차용) 판정법: CCD 0.023–0.19 mA cm⁻² · 저항은 Li–SE interface 가 지배 · 펠릿 = NEI powder ≈100 mg · ⌀10 mm · 360 MPa 2 분 → 1.55–1.60 g cm⁻³ · ≈0.80–0.85 mm (원문 '결정학 밀도 1.64' 는 인용 문헌 Doux 2020 의 1.860 과 어긋남) — Tron · Orue · López-Aranguren · Beutl (J. Electrochem. Soc. 2023)

> slug `tron2023_lpscl_ccd_ambient_pressure` · DOI `10.1149/1945-7111/ad01e3` · type `experiment (Li/Li₆PS₅Cl/Li 대칭셀 · 단계 정전류 + galvanodynamic 분극 · PEIS impedance · ssNMR · SEM · peel tester 스택압 · NEI powder 펠릿 360 MPa · 시뮬레이션 없음)` · PDF `1.Critical_Current_Density_Measurements_of_Argyrodite_Li6PS5Cl_Solid_Electrolyte_at_Ambient_Pressure.pdf` · SI `미입수 (Fig. S1–S7 미확인)` · digested `2026-10-14` · status ✅
>
> **저자**: Artur Tron¹ · Ander Orue² · Pedro López-Aranguren² · **Alexander Beutl¹\*** — ¹ AIT Austrian Institute of Technology GmbH, Center for Low-Emission Transport, Battery Technologies (1210 Vienna, Austria) · ² CIC energiGUNE, Basque Research and Technology Alliance (BRTA), Vitoria-Gasteiz (Spain) · *J. Electrochem. Soc.* **2023**, *170*, 100525 (open access · CC BY 4.0) · 투고 2023-08-10 · 수정 2023-09-06 · 출판 **2023-10-20** · 연구비 EU H2020 875028 (SUBLIME) · Horizon Europe 101069686 (PULSELION) · ORCID Tron 0000-0002-6565-8247 · Beutl 0000-0002-7098-619X [인쇄 PDF p.2 · p.10 — 크롭 `txt_p2_title_abstract.png`].
> **이웃 카드 (링크만)**: [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) (이 논문 ref 22 = ref 40 — "1.64" 가 기대는 바로 그 문헌) · [`ohno2020_interlab_ionic_conductivity_argyrodite`](ohno2020_interlab_ionic_conductivity_argyrodite.md) (결정학 1.86 · 피크노미터 1.874 · 8 랩 펠릿 밀도) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (같은 "1.64" 를 이론밀도로 쓴 또 하나) · [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) (σ–스택압 — 이 논문에 없는 축).

---

## 0. 결론 먼저 — 우리 질문 다섯에 대한 답

**한 문장**: 이 논문은 NEI 상용 Li₆PS₅Cl 을 **≈100 mg · ⌀10 mm 다이 · 360 MPa 2 분**으로 눌러 **1.55–1.60 g cm⁻³ · ≈0.80–0.85 mm** 펠릿을 만들고 (우리 랩 펠릿과 같은 질량 · 지름), 그 위에 Li 를 붙여 **상압 (0.20–0.28 MPa) 의 CCD** 를 셀 지그 · 두께 · Li 원천별로 잰다.
"결정학 밀도 1.64 g cm⁻³" 는 **ref 22 (Doux 2020) 한 개에만 기대는데, 그 문헌 (정본 카드 기준) 은 이론밀도 1.860 · 펠릿 1.49–1.58 을 쓴다** — 1.64 는 결정학 값이 아니다 (Z = 4 · a ≈ 9.86 Å → 1.86 [우리 산술]).  σ_ion 은 재지 않았다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① SE 진밀도 1.64 의 출처 | 유일한 자리: *"Dense pellets with densities in the range of 1.6 to 1.55 g cm−3 could be thus obtained, in good agreement with literature values and the crystallographic density of 1.64 g cm3.²²"* → ref 22 = *"J.-M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. Wang, E. A. Wu, C. Jo, H. Yang, and Y. S. Meng, Adv, Energy Mater., 10, 1903253 (2020)."* (같은 논문이 ref 40 으로 한 번 더 — 연도만 2019).  **측정도 계산도 아니다** — 이 논문에 비중병 · 기체 · 격자상수 · XRD 가 하나도 없다.  라벨 = "crystallographic".  **인용한 Doux 2020 은 이론밀도 1.860 g cm⁻³ 로 상대밀도 80.3–84.9 % 를 낸다** (펠릿 실측 1.492–1.579) — 1.64 는 그 문헌의 어느 값과도 같지 않다.  결정학 계산: a 9.8591 Å (Ohno Table S1) → **1.860** · a 9.8614 Å (Kraft 중성자) → 1.859.  1.64 가 되려면 a = **10.28 Å** (Li₆PS₅I 의 10.14 Å 보다 크다).  **같은 상품명 NEI "fine" 의 진밀도 인쇄값 = 1.87** (Frankenberg 2025).  같은 그룹의 Beutl 2024 (묶음 이웃) 는 같은 1.64 에 **다른 인용** (Zhou 2019 · Tron 2023 Nanomaterials) 을 단다 | [인쇄] PDF p.3 · p.10 · p.11 · [정본 카드] doux2020 §6 + `docs/data/doux2020_stack_pressure.csv` (Table S2, table_stated) · ohno2020 §3.1 · kraft2017 · frankenberg2025 · [우리 산술] |
| ② 펠릿 제작 · 측정 조건 | NEI Corp. *"Commercially available fine Li6PS5Cl powder … used as received"* · **D50 [미확인]** · **≈100 mg** · **⌀10 mm** 경화강 다이 (Across International, W18Cr4V) · **≈50 MPa 수 초 → 360 MPa 2 분** · 온도 미기재 · 가열 언급 없음 (냉간으로 읽힘) · 두께 *"around 0.80 mm"* (p.4) · *"0.85–0.80 mm"* (p.6) · **두께를 잰 도구 · 상태 (다이 안 / 놓은 뒤 / 꺼낸 뒤) [미확인]** · 겉보기 밀도 1.55–1.60 g cm⁻³ (측정법 미기재) · **상대밀도 · 공극 = 저자 계산 없음** (1.64 와 "좋은 일치" 라는 말로 ≈95–98 % 치밀을 함의).  [우리 산술] 공극 = **1.64 기준 2.4–5.5 % · 1.86 기준 14.0–16.7 %** (두께로 다시 계산하면 3.0–8.7 % / 14.4–19.5 %) — §3-3 | [인쇄] PDF p.3 · p.4 · p.6 · [우리 산술] |
| ③ σ_ion ↔ 압력 · 온도 | **σ_ion 값 없음** (EIS 는 단락 확인 · "Rct" 대조용으로만) · **온도 미기재** · **hot press 없음** · **압력 무관 주장 없음** — 결론은 반대: *"A higher pressure will yield enhanced CCD values, mainly due to the decrease of Rct."* · 작동압 = 스택압 실측 **Swagelok 0.20 · CR2032 0.24 · ECC-Std 0.28 MPa** + 10 MPa 압력셀 (단계 정전류만) · 성형압은 360 MPa 한 점 | [인쇄] PDF p.3 · p.7–8 · p.10 |
| ④ 측정 재현성 | **n 미기재 · 표준편차 · 오차막대 없음 · round robin 없음** (반복이 보이는 것은 스택압 하중–변위 n = 3 뿐, Fig 4b).  흩어짐의 크기: 같은 CR2032 · Li chip 세 셀 "Rct" **327–478 (1.46 배)** · 지그 간 **269–653 (2.4 배, 스택압은 0.20–0.28 MPa 로 비슷)** · Swagelok 스프링 느슨 **1988 vs 269 (7.4 배)**.  셀 = CR2032 (X2lab SS316, 물결 스프링) · ECC-Std (EL-CELL) · Swagelok S4R ½ inch · 10 MPa 압력셀 (ref 38) · 전극 = **Li 금속 (비차단)** — 차단 전극 없음 · PEIS **1 MHz–0.1 Hz · 50 mV** · 정상상태 판정 없음 (1 h 고정 계단) · 벌크/계면 분리 안 함 (기울기 전체를 "Rct" 라 부르고 단위는 Ω 로 적었지만 숫자는 Ω·cm² — §3-9) | [인쇄] PDF p.3 · p.6–8 · Table I–IV · [판독] · [우리 산술] |
| ⑤ 우리 DEM/MPM | **순수 SE 한 점** (360 MPa · 2 분 유지 · 상태 미상) — 세대 2 표적 (300 MPa + 이완 · ε_union 10–13 % · 1.64 기준) 에 대면: 같은 1.64 로 계산하면 이 펠릿은 **2–9 %** 로 표적보다 치밀 · 1.86 으로 둘 다 옮겨도 (펠릿 14–20 % ↔ 표적 20.6–23.3 %) **여전히 ≈1–9 %p 치밀** — 밀도 차로는 이 펠릿 1.50–1.60 ↔ 표적 1.43–1.48 g cm⁻³ (압력 360 ↔ 300 MPa 차이 포함).  밀도 기준 선택 자체가 공극을 **≈11 %p** 옮긴다 (표적 폭 3 %p 의 ≈4 배).  실험 공극은 질량 보존 연산자 (DEM ε_sphere 쪽 · D9) 다.  **다압력 Heckel 없음** | [우리 산술] · §7-2 |

⛔ **한정어 (떼지 말 것)**: ① **SI 미입수** — Fig. S1 (셀 사진) · S2 (단계 정전류 전체) · S3 · S7 (PEIS) · S4 (ssNMR) · S5 (장기 사이클) · S6 (두 방법 비교) 은 본문 서술로만 안다 ② **Doux 2020 원문 PDF 는 이 작업에서 직접 열지 않았다** — "1.860 · 1.492–1.579" 는 정본 카드 `doux2020_stack_pressure_assb` §6 과 리포 `docs/data/doux2020_stack_pressure.csv` (Table S2, `table_stated`) 근거 · 정본 카드 · CSV 어디에도 1.64 는 없다 ③ 펠릿 밀도 측정법 · 두께 측정 상태 · 꺼낸 뒤 지름 미기재 ④ 한 압력 (360 MPa) · NEI 분말 (입경 미상) · 우리 300 MPa 와 다르다 ⑤ 이 논문의 주제는 **Li 금속 음극 계면의 CCD** 다 — 복합 양극 수송 · σ_e 는 다루지 않는다.

---

## 1. 한 줄 요약
황화물 SE 의 CCD 가 문헌마다 >1 mA cm⁻² 부터 제각각인 이유를 **측정 조건 (높은 스택압 · 고온 · 비표준 셀)** 에서 찾고, LPSCl 을 모델로 **상압에 가까운 상용 셀 (스택압 0.20–0.28 MPa)** 에서 단계 정전류 (time-control · charge-control) 와 **galvanodynamic 분극** (전류를 선형으로 올리며 전압을 보는 Tafel 차용법) 을 비교했다.
결과: LPSCl 의 CCD 는 **0.05–0.2 mA cm⁻²** 수준 (문헌 0.3–2.15 mA cm⁻² 는 높은 압력의 산물) · galvanodynamic 법이 **같은 실험 하나로 CCD · "Rct" · 겉보기 j0** 를 함께 줘 더 낫다 · 셀 지그 (조립 때의 압착 포함) · Li 표면 피막이 CCD 를 크게 흔들고, 단계 정전류에서는 **두꺼운 펠릿이 CCD 를 부풀린다** (덴드라이트가 갈 길이 멀어 단락이 늦다).  펠릿은 360 MPa 냉간 압착 ≈0.80–0.85 mm — 이 펠릿의 밀도 문장이 우리 "1.64" 질문의 출처다.
저자 결론 (PDF p.10): *"Regarding the applicability of Li6PS5Cl for battery application under ambient conditions it could be found that the high interfacial resistance is the main bottleneck for application. Usually, this issue is resolved in literature by application of high pressures during cycling … This approach seems to be less feasible at larger scale"* → 연성 계면층 (refs 11 · 44) 을 대안으로 제시.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| A. Tron · A. Orue · P. López-Aranguren · **A. Beutl\*** (AIT Vienna · CIC energiGUNE) | J. Electrochem. Soc. 170 (2023) 100525 · CC BY 4.0 | 10.1149/1945-7111/ad01e3 | **NEI Corp. 상용 "fine" Li₆PS₅Cl (그대로)** · Li chip (MTI ⌀15.6 × 0.25 mm) · Li foil (Goodfellow 38.1 mm 폭 × 0.20 mm) · Li on Cu (China Energy Lithium, Li 0.04 mm) | 실험 — Li 대칭셀 CCD (단계 정전류 · galvanodynamic) · PEIS · ssNMR · SEM · 스택압 (peel tester) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 펠릿 · 셀 (PDF p.3 · p.6 · p.8)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE 분말 | *"Commercially available fine Li6PS5Cl powder was purchased from NEI Corp. and used as received."* — 입경 · PSD · 로트 **[미확인]** (같은 상품명의 다른 카드: `frankenberg2025_…` 측정 x50 **17 ± 2 µm** · 진밀도 **1.87** [정본 카드] · 묶음 이웃 `beutl2024_…` *"∼1 µm particle size"* [정본 반입 전] — 1 차 입자 ↔ 응집체 차이로 보이나 [추정]) | [인쇄] PDF p.3 |
| 펠릿 질량 · 다이 | *"around 100 mg of the Li6PS5Cl powder was used and placed in a 10 mm hardened steel die set (Across International, W18Cr4V hardened carbon tool steel)"* | [인쇄] PDF p.3 |
| 성형 | *"Around 50 MPa were applied for a couple of seconds and then the pressure was increased to 360 MPa for 2 min."* — 온도 · 분위기 · 하중 속도 · 제하 방식 **[미확인]** | [인쇄] PDF p.3 |
| 펠릿 밀도 | *"Dense pellets with densities in the range of 1.6 to 1.55 g cm−3"* — 측정법 (질량/부피? 몇 개?) **[미확인]** · 상한 "1.6" 은 두 자리 | [인쇄] PDF p.3 |
| 기준 밀도 | *"… in good agreement with literature values and the crystallographic density of 1.64 g cm3.²²"* (단위 "cm3" 의 음수 지수 빠짐 = 원문 그대로) | [인쇄] PDF p.3 · §3-2 |
| 두께 | *"the electrolyte layer which is rather thick at around 0.80 mm"* (p.4) · *"electrolyte and electrode thicknesses, which were in the range of 0.85–0.80 mm and 0.15–0.10 mm respectively"* (p.6) · 두께 시리즈 0.85 · 0.42 · 0.20 mm (Table III, p.8) — **얇은 펠릿 만든 법 (질량) · 두께 측정 도구 · 상태 [미확인]** | [인쇄] PDF p.4 · p.6 · p.8 |
| Li 전극 | 칩 · 포일 = 메스로 표면 긁고 파우치 필름 (Dai Nippon D-EL408PH(3)S-250) 사이에 유리 원통으로 밀어 평탄화 → **⌀8 mm** 펀칭 · Li on Cu = 받은 그대로 | [인쇄] PDF p.3 |
| 셀 | CR2032 (X2lab, SS316 · 물결 스프링 1.5 × 1.4 mm · SS316 스페이서 ⌀15.5 × 0.5 mm) · ECC-Std (EL-CELL, 제조사 부품) · Swagelok (S4R, ½ inch, 플런저에 Li 직접 · 스프링 최대 압축) · 압력셀 10 MPa (ref 38) | [인쇄] PDF p.3 · p.7 |
| 전류 밀도 면적 | *"Only the geometric surface area of the electrodes was used"* → Li ⌀8 mm = **0.5 cm²** (p.7 의 압력 환산도 0.5 cm²) | [인쇄] PDF p.6 · p.7 |

### 3-2. ★★ "결정학 밀도 1.64" 의 추적 — 문장 → 인용 번호 → 참고문헌 → 그 문헌의 값
1. **문장 (유일한 자리)** — PDF p.3 왼쪽, Experimental › *Materials and cell assembly* 둘째 문단 끝 (크롭 `txt_p3_materials_pellet.png`): *"Dense pellets with densities in the range of 1.6 to 1.55 g cm−3 could be thus obtained, in good agreement with literature values and the crystallographic density of 1.64 g cm3.²²"* — 이 논문 어디에도 1.64 의 다른 근거 · 상대밀도 · 공극률 계산이 없다 (본문 전수 · 텍스트 검색).
2. **인용 번호 → 원문 그대로** — ref 22 (PDF p.10, 크롭 `txt_p10_ref22.png`): *"J.-M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. Wang, E. A. Wu, C. Jo, H. Yang, and Y. S. Meng, Adv, Energy Mater., 10, 1903253 (2020)."* · 같은 논문이 ref 40 (PDF p.11, 크롭 `txt_p11_ref40.png`) 으로 한 번 더: *"… Adv. Energy Mater., 10, 1903253 (2019)."* — ref 40 은 *"thick lithium foils are used for application in pressure cells using sulfide-based electrolytes"* (PDF p.9) 의 근거로 쓰였다.  [정본 카드] 그 논문 = `doux2020_stack_pressure_assb` (DOI 10.1002/aenm.201903253 · 온라인 2019-11-25 · 권호 2020) — 연도 둘 다 통용.
3. **측정인가 계산인가** — 둘 다 아니다.  이 논문에는 비중병 (기체 종류) · 아르키메데스 · XRD · 격자상수 · Z · 몰질량이 없다.  "crystallographic" 은 **라벨뿐**이고 근거는 ref 22 하나.
4. **ref 22 가 실제로 쓰는 값** [정본 카드 · 리포 CSV, 원문 PDF 미대조]: Doux 2020 Table S2 — NEI LPSCl · 200 mg · ⌀13 mm · 370 MPa 펠릿 넷: 두께 1.01 / 0.96 / 1.01 / 0.99 mm → 실측 **1.492 / 1.579 / 1.494 / 1.524 g cm⁻³** → 상대밀도 **80.3 / 84.9 / 80.3 / 83.0 % (평균 82.1 %) — 이론밀도 1.860 g cm⁻³ 기준** · 본문 *"A porosity of 18% within the electrolyte provides connecting pathways"* (`doux2020` 카드 §6 · CSV 섹션 (C)).  ⇒ **1.64 는 ref 22 의 이론밀도 (1.860) 도, 펠릿 실측 (1.49–1.58) 도 아니다.**  "literature values 와 좋은 일치" 는 펠릿 밀도 (1.55–1.60 ↔ 1.49–1.58) 에 대해서만 선다.
5. **결정학 계산 대조** [우리 산술 · 이 논문엔 격자상수가 없어 정본 카드 값으로]: ρ_X = Z·M / (N_A·a³) · Z = 4 · M = 268.37 g mol⁻¹

| a (Å) · 출처 | ρ_X (g cm⁻³) |
|---|---|
| 9.85910(10) · `ohno2020` Table S1 (그 표 자신이 이론밀도 **1.86** 을 적는다) | **1.860** |
| 9.8614(1) · `kraft2017` 중성자 | 1.859 |
| 9.8598(4) · `adeli2019` XRD (x = 0) | 1.860 |
| 9.898(7) · `kraft2017` X-ray PDF | 1.838 |
| **1.64 가 되려면** | **a = 10.28 Å (+4.3 %)** — `ohno2020` 의 Li₆PS₅I (10.142 Å) 보다 크다 → Li₆PS₅Cl 결정으로 불가능 |

   - 실측 골격 밀도: `ohno2020` 랩 D 피크노미터 **1.874 g cm⁻³** (Table S6) ≈ 결정학 1.86 [정본 카드].
   - ★ **같은 상품명 (NEI "fine" Li₆PS₅Cl — 이 논문이 쓴 분말) 의 진밀도 인쇄값 1.87 g cm⁻³**: `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` [정본 카드 — 원문 p.4 · p.12 인쇄 · 측정법은 카드에 없음] · 그 논문의 혼합 밀도 검산 (NCM 4.75 · LPSCl 1.87 → 70:30 wt = 50:50 vol · ρ₀ 3.249 ✓) 이 1.87 로 맞는다 — 로트는 다를 수 있다.
   - **겉보기 밀도가 1.64 를 넘는 Li₆PS₅Cl 펠릿이 이미 있다** — `ohno2020` 랩 C **1.77** (370 MPa) · G **1.70** (441 MPa) · D **1.655** (720 MPa) [정본 카드 §3.3].  펠릿 겉보기 밀도는 골격 밀도의 아래 한계이므로 [우리 산술], **그 분말들에서 1.64 는 진밀도일 수 없다** (다른 분말 · 다른 로트라는 한정어는 남는다).
6. **1.64 는 어디서 왔나** — **[미확인]**.  관찰 (사실): 같은 1.64 를 LPSCl 밀도로 쓴 문헌이 정본에 여럿 있다 — `lee2025_heckel_…` (SI p.3 *"theoretical densities … calculated to be 1.64"*) · `kim2023_mechanofusion_…` (SI p.12) · `lee2026_lpscl_coating_thickness_ncm811` (SI) · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` (Table 2) · `bazzoun2026_dem_fem_rnm_ionic` (Table 1 ρ_SE) · `oh2026_bimodal_composite_cathode` (SSE 1.64 g/cc).
   ★ **같은 AIT 그룹 안에서도 인용이 바뀐다**: 이 논문 (2023-10) = ref 22 (Doux 2020) 하나 ↔ 같은 묶음의 이웃 카드 `beutl2024_round_robin_coin_cell_sulfide_assb` (Tron 공저 · 정본 반입 전 · 그 카드 §3-3 기준) = 같은 *"crystallographic density … 1.64"* 를 [37] Zhou … Nazar, *ACS Energy Lett* 2019, 4, 265 와 [10] Tron … Beutl, *Nanomaterials* 2023, 13, 327 에 붙인다.  **같은 수 · 같은 라벨 · 다른 출처** — 측정 · 계산 근거가 따라다니지 않는 관례값이라는 정황 [추정].  1.64 는 결정학 값이 아니라 **냉간 압착 펠릿 겉보기 밀도 범위 (Ohno 8 랩 1.47–1.77 · Doux 1.49–1.58 · 이 논문 1.55–1.60) 안의 값**이다 — 어떤 펠릿 값이 "이론밀도" 로 옮겨졌을 가능성 = [추정].  원출처 추적의 다음 단계: Doux 2020 원문 (본문 + SI) 에서 "1.64" 직접 검색 · 분말 공급사 자료.

⛔ 인용 금지 (이 카드 판단 · 원장 등재 전): 이 논문 PDF p.3 의 *"crystallographic density of 1.64 g cm3"* 를 Li₆PS₅Cl 결정학 · 진밀도의 근거로 쓰지 않는다 — 인용한 ref 22 가 그 값을 뒷받침하지 않고 결정학 계산은 1.86 이다.

### 3-3. ★ 펠릿 밀도 · 두께 · 공극 — 두 기준 [우리 산술]
식: A = π(0.5 cm)² = 0.7854 cm² · t = m / (ρ·A) · ε = 1 − ρ/ρ_s (질량 보존 연산자 — DEM ε_sphere 와 같은 쪽).

| 경우 | ρ (g cm⁻³) | ε · ρ_s = 1.64 | ε · ρ_s = 1.86 | ε · ρ_s = 1.874 (피크노미터) | 100 mg · ⌀10 mm 두께 |
|---|---|---|---|---|---|
| 인쇄 상한 "1.6" | 1.600 | **2.4 %** | **14.0 %** | 14.6 % | 0.796 mm |
| 인쇄 하한 1.55 | 1.550 | **5.5 %** | **16.7 %** | 17.3 % | 0.821 mm |
| 두께 0.80 mm (p.4) · 100 mg 로 역산 | 1.592 | 3.0 % | 14.4 % | 15.1 % | — |
| 두께 0.85 mm (p.6 상한) · 100 mg 로 역산 | 1.498 | 8.7 % | 19.5 % | 20.1 % | — |
| 질량 ±5 mg 감도 (0.80 mm) | 1.512–1.671 | −1.9–7.8 % | 10.2–18.7 % | — | — |
| 경계 (ρ = ρ_s) | 1.64 / 1.86 | 0 | 0 | — | **0.776 / 0.685 mm** |

- 두 기준 차 = ρ·(1/1.64 − 1/1.86) = **11.2–11.5 %p** (ρ 1.55–1.60).
- 인쇄 밀도 (1.55–1.60) 와 인쇄 두께 (0.80–0.85 mm) 는 질량 "around 100 mg" 아래서 대체로 맞는다 — 0.85 mm 펠릿이 1.55 이려면 질량 ≈103.5 mg.
- **우리 랩 규칙 (`docs/density_generations_20261014.md` §7) 에 대면**: 100.0 mg · ⌀10.00 mm 의 경계 두께 0.776 mm 보다 이 논문 펠릿 (0.80–0.85 mm) 이 두껍다 → ρ ≤ 1.64 → **이 논문 펠릿으로는 1.64 · 1.86 을 가르지 못한다** (그 문서의 "같은 조건 문헌 펠릿 두께 0.80–0.82 mm [검색 요약 · PDF 확인 전]" 확인: PDF 인쇄는 *"around 0.80 mm"* · *"0.85–0.80 mm"* — "0.82" 는 인쇄돼 있지 않고 1.55 g cm⁻³ · 100 mg 의 [우리 산술] 두께 0.821 mm 와 같은 값이다).
- 같은 압력대의 문헌 펠릿 [정본 카드]: Doux (**같은 NEI 분말**) 370 MPa · ⌀13 · 200 mg → 1.492–1.579 (1.86 기준 15.1–19.8 % · 1.64 기준 3.7–9.0 %) · `ohno2020` 랩 B (**다른 분말** — Giessen 합성 · 375 MPa · **⌀10 · 100 mg · 0.795 mm** · 1.60 g cm⁻³ · 결정학 기준 86 %) — 이 논문 (360 MPa · ⌀10 · ≈100 mg · ≈0.80 mm · 1.55–1.60) 과 **거의 같은 펠릿**이 다른 랩 · 다른 분말에서 나왔다.

### 3-4. CCD — 단계 정전류 (Fig 1 · PDF p.3–4)
- 계단: 0.01 · 0.02 · 0.05 · 0.10 · 0.20 · 0.50 · 1.00 · 2.00 mA cm⁻² · 계단마다 한 사이클 (plate/strip) · 사이클 뒤 PEIS (1 MHz–0.1 Hz · 50 mV) [인쇄 p.3].
- **(a) time-control 1 h · 1 사이클**: ≤0.05 안정 · 0.10 에서 계단 안 전압 상승 (단락 아님) · 0.20 급상승 (단락 아님) · **0.50 에서 단락** — 0 V 까지 안 떨어지는 **soft short** · PEIS 급락 (Fig. S3) · ssNMR ⁷Li **≈263 ppm** Li 금속 신호 (Fig. S4) [인쇄 p.3].
- **(b) 3 사이클 · (c) 5 사이클**: 단락 **0.20** [인쇄 p.3].  **(d) charge-control 1 mAh**: 단락 **0.10** [인쇄 p.3].  [판독] Fig 1d 시간축: 0.01 mA cm⁻² 계단이 0–200 h (100 h + 100 h) → "1 mAh" 는 **1 mAh cm⁻²** (면적당).
- time-control 0.10 mA cm⁻² 은 계단당 0.10 mAh (cm⁻²) 뿐 → 덴드라이트가 ≈0.80 mm 를 다 건너기 전에 전류가 뒤집힌다 · 0.10 mA cm⁻² 1 h 장기 사이클은 **11 사이클 뒤 단락** (Fig. S5) → charge-control 과 비슷한 총 전하 = Bai 2016 의 **Sand 용량** 개념과 맞는다 [인쇄 p.4].
- 저자 결론: *"charge-control measurements using reasonably high charge values (⩾1 mAh), seem to yield the most relevant results. A low CCD value which lies in the range of 0.05–0.10 mA cm−2 could be determined for Li6PS5Cl."* [인쇄 p.4].  단계법은 병목 정보를 안 준다 → galvanodynamic 도입.

### 3-5. CCD — galvanodynamic 분극 (Fig 2 · Table I · PDF p.4–6)
- 방법: 0.01 → 2 mA cm⁻² 선형 증가 · 기본 **0.20 µA cm⁻² s⁻¹** · 앞뒤 PEIS [인쇄 p.3].  [우리 산술] 전 구간이면 9,950 s (2.76 h).
- 해석 틀 (Fig 2a): 저전류 **linear** (Butler–Volmer 선형화, Eq 1 i = −i₀fη · Eq 2 R_ct = RT/(F i₀)) → **Sand** (표면 Li⁺ 가 시간이 지나며 고갈) → **Tafel** (표면 고갈 · 농도 구배 · 불안정 도금).  **CCD = 선형 구간의 끝 (Sand 구간의 시작)** · "Rct" = 저전류 직선 기울기 · **겉보기 j0** = 고전류 log i–η 직선의 x 절편 (Fig 2d) [인쇄 p.5–6].
- **Table I (CR2032 · Li chip)** [인쇄 p.6]:

| 훑기 속도 (µA cm⁻² s⁻¹) | j0 (mA cm⁻²) | "Rct" (원문 단위 Ω — §3-9) | CCD (mA cm⁻²) |
|---|---|---|---|
| 2.00 | 0.30 | 478 | 0.094 |
| 0.20 | 0.18 | 327 | 0.096 |
| 0.02 | 0.13 | 408 | 0.075 |

- 저자: "Rct" 차이는 훑기 속도가 아니라 **접촉 차이** — *"Slight deviations of the electrolyte and electrode thicknesses, which were in the range of 0.85–0.80 mm and 0.15–0.10 mm respectively could be the reason … Due to the static configuration of the CR2032 cell, small deviations in the sample sizes result in different internal pressures, which cannot be compensated."* [인쇄 p.6].
- j0 는 훑기 속도에 따라 커진다 (이중층 충전) — 저자는 *"directly proportional"* 이라 썼지만 [우리 산술] log–log 기울기 **0.18** (속도 100 배 → j0 2.3 배) · 느린 훑기는 전하가 많아 (*"around 4.00 mAh, 0.40 mAh, and 0.04 mAh"*) 도금 Li 면적이 커진다 → 0.20 µA cm⁻² s⁻¹ 채택 [인쇄 p.6].  ⚠ [우리 산술] 전 구간 적분은 27.8 / 2.78 / 0.278 mAh cm⁻² (× 0.5 cm² = 14.0 / 1.40 / 0.14 mAh) — 인쇄값과 안 맞고 (10 배씩이라는 비만 맞음) 계산 근거 미기재.
- CCD 0.075–0.096 ≈ 단계법 (Fig. S6) · 단락 여부는 CCD 지표로 부적절, 과전압 증가가 더 믿을 만하다 · 문헌 0.3–2.15 mA cm⁻² (ref 14) 는 높은 압력 · 스택압 <5 MPa 에서 stripping 공극 증가 (ref 31) [인쇄 p.6].

### 3-6. 셀 지그 · 스택압 (Fig 3 · 4 · Table II · PDF p.6–8)
- **Table II** [인쇄 p.7]:

| 셀 | j0 (mA cm⁻²) | "Rct" | CCD (mA cm⁻²) |
|---|---|---|---|
| ECC-Std | 0.16 | 653 | 0.062 |
| CR2032 | 0.18 | 327 | 0.096 |
| Swagelok (tight) | 0.38 | 269 | 0.115 |
| Swagelok (loose) | 0.042 | 1988 | 0.035 |

- 단계법 (Fig 3a): Swagelok 이 전 계단 최저 과전압 · 0.20 까지 안정 · 0.50 급상승 · 1.00 단락 · ECC-Std 는 0.10 부터 과전압 급증인데 **단락은 1.00 에서야** (PEIS Fig. S7) → 정의 (단락 vs 기울기) 에 따라 CCD 가 크게 달라진다 · **10 MPa 압력셀**: 과전압 감소 · 0.20 까지 안정 [인쇄 p.7].
- 장기 사이클 0.10 mA cm⁻² 1 h: **CR2032 22 h 뒤 단락 · Swagelok 100 h 넘게 지속** (Fig. S5) [인쇄 p.7].
- **스택압 (peel tester · 닫는 데 드는 하중)** [인쇄 p.7–8 · 크롭 `txt_p7_stack_pressure.png` · `txt_p8_stack_pressure.png`]:

| 셀 | 스프링 상수 (N mm⁻¹) | "stack pressure" (힘, N) | 압력 (MPa, 0.5 cm²) | 측정 방식 |
|---|---|---|---|---|
| Swagelok | 2.0 | 10 | **0.20** | 스프링 완전 압축 = 조립 상태 |
| ECC-Std | 2.2 | 14 | **0.28** | 시료 대신 1.9 mm 스페이서 |
| CR2032 | **43.1** | 12 | **0.24** | 시료 대신 1.9 mm 스페이서 |

   - 반복 n = 3 (Fig 4b 범례 #1–#3) · *"The rather similar stack pressures of 0.20–0.28 MPa inside the different cell setups cannot explain the differences obtained in the CCD measurements."* → 후보: Swagelok 조립 때 **손으로 세게 압착한 뒤 너트를 조인다** = 그때의 고압이 접촉을 만든다 (미검증) [인쇄 p.8].
   - [우리 산술] 압력 검산 10 N / 0.5 cm² = 0.20 MPa ✓ (펠릿 전 면적 0.785 cm² 로 나누면 0.13 · 0.18 · 0.15 MPa).  **두께 0.1 mm 당 힘 변화**: CR2032 **4.3 N (12 N 의 36 %)** · Swagelok 0.20 N (2 %) · ECC-Std 0.22 N (1.6 %) — **고정 간극 + 단단한 스프링 (CR2032) 은 시료 두께에 민감하다.**
   - [우리 산술 · 추정] 1.9 mm 대역 ↔ 실제 적층 (스페이서 0.5 × 2 + Li 0.10–0.15 × 2 + SE 0.80–0.85) = 2.00–2.15 mm → CR2032 실제 힘은 선형이면 **16–23 N (0.33–0.46 MPa)** 일 수 있다 — 인쇄 0.24 MPa 는 대역 시료 값.

### 3-7. 전해질 두께 (Fig 5 · Table III · PDF p.8–9)
| 두께 (mm) | j0 (mA cm⁻²) | "Rct" | CCD (mA cm⁻²) |
|---|---|---|---|
| 0.85 | 0.18 | 327 | 0.096 |
| 0.42 | 0.19 | 341 | 0.127 |
| 0.20 | 0.20 | 261 | 0.117 |
- CR2032 · 줄어든 두께는 **스틸 스페이서 추가**로 보정 (*"To enable comparable pressure in all cells"*) — 추가한 스페이서 두께 · 개수 · 얇은 펠릿의 질량 **[미확인]** [인쇄 p.8].  (Table III 캡션은 *"for different cell setups"* — 캡션 복사 오기.)
- 단계법: 0.85 mm 는 벌크 저항 때문에 과전압 큼 · 0.20 에서 급상승 · **0.5 에서 단락** · 0.42 · 0.20 mm 는 **0.20 에서 단락** (0.42 는 계단 뒤 절반) → *"for step chronopotentiometry a rather thin electrolyte layer should be used in order to avoid an overestimation of the stability"* · galvanodynamic 은 두께 무관 [인쇄 p.8–9].
- [우리 산술] j0 증가 0.18 → 0.20 (+11 %) 인데 두께는 4.25 배 — 저자가 인용한 *"limiting current … inversely proportional to the distance"* (ref 24) 의 1/L 과 맞지 않는다 · 본문 *"highest for the thin one (0.20 mm)"* ↔ 표 최대는 0.42 mm (0.127).
- [우리 산술 · 추정] 스페이서가 0.5 mm 단위라면: 0.42 mm + 1 장 → 적층 +0.07 mm → CR2032 +3 N (+25 %) · 0.20 mm + 1 장 → −0.15 mm (−6.5 N, −54 %) 또는 + 2 장 → +0.35 mm (+15 N, +126 %) — **43 N mm⁻¹ 스프링에서 "같은 압력" 은 보장되지 않는다.**

### 3-8. Li 원천 (Fig 6 · 7 · Table IV · PDF p.8–10)
| Li 원천 | 겉보기 j0 (mA cm⁻²) | "Rct" | CCD (mA cm⁻²) |
|---|---|---|---|
| Li chip (세척) | 0.18 | 327 | 0.096 |
| Li foil (세척) | 0.21 | 323 | 0.154 |
| Li on Cu (그대로) | 0.31 | 305 | 0.194 |
| Li chip (받은 그대로) | 0.07 | 2073 | 0.023 |
- SEM (Fig 6, ZEISS Supra 40 · 3 kV · 20 µm 막대): 세척 전 칩 · 포일 · Li on Cu 에 불순물 · 세척 후 (d, e) 감소 · Cu 집전체는 거칠다 (f, 1 µm 막대) [인쇄 p.9].
- 단계법 (Fig 7a): 모두 ≤0.05 안정 · 0.10 에서는 Li on Cu 만 안정 · 0.2 에서 모두 상승 · Li foil 단락 [인쇄 p.9].
- 해석: 세척 안 한 표면의 피막이 표면 확산을 바꿔 고전류 기울기 ↑ · Li on Cu 의 높은 CCD 는 불순물이 전극 면적을 키워 실효 전류 밀도를 낮춘 효과일 수 있다 · 받은 그대로의 칩 = 높은 "Rct" · 매우 낮은 CCD · j0 [인쇄 p.10].
- 원문 불일치: 본문 *"similar Rct of 324 Ω, 305 Ω, and 323 Ω, for the Li chip, Li foil, and Li on Cu"* ↔ Table IV 327 / 323 / 305 (순서 · 값 어긋남) [인쇄 p.10 · p.8].

### 3-9. ★ "Rct [Ω]" 의 정체 — 단위 · 벌크 몫 · Eq 2 정합 [판독 · 우리 산술]
1. **단위**: 그림의 가로축은 전류 밀도 I (mA cm⁻²) 다.  점선 (선형 적합) 기울기 dE/dI 를 읽으면 [판독] Fig 2c ≈460 · ≈333 · ≈420 (표 478 · 327 · 408) · Fig 3b CR2032 ≈330 · Swagelok tight ≈290 · ECC-Std ≈575–660 · loose ≈1800 (표 327 · 269 · 653 · 1988) · Fig 5b ≈330 · ≈265 (표 327–341 · 261) — **V·cm²/A = Ω·cm² 로 읽은 값이 표의 숫자와 같다.**  Ω 였다면 ÷ 0.5 cm² 로 **표의 ≈2 배** (327 → ≈650 Ω) 가 나와야 한다 ⇒ 표의 "Rct [Ω]" 는 **면적 비저항 (Ω·cm²) 으로 읽어야 한다** (단위 표기 오기로 판단).  교차 확인 [판독]: 단계 정전류 Fig 1a 의 0.01 · 0.02 · 0.05 mA cm⁻² 계단 전압 ≈0.005 · 0.009 · 0.021 V → **≈420–500 Ω·cm²** — galvanodynamic 기울기와 같은 자릿수라, 가로축이 (라벨대로) 전류가 아니라 **전류 밀도**임도 확인된다 (가로축이 mA 였다면 두 방법이 2 배 어긋난다).
2. **이름**: 저전류 기울기 = 벌크 (SE 두께) + 두 Li|SE 계면 (전하이동 + 접촉 · 협착) 의 합이다 — 저자는 전체를 "charge transfer resistance" 라 부른다.  [우리 산술] 벌크 몫 = L/σ = 0.080–0.085 cm ÷ 2.0–2.5 mS cm⁻¹ (같은 NEI LPSCl 펠릿 σ, [정본 카드] `doux2020` §2.1) = **32–43 Ω·cm² ≈ 10–13 %** → 0.2 MPa 대 셀의 저항은 **계면이 ≈85–90 % 지배**.
3. **Eq 2 정합**: 대칭셀이면 저전류 기울기 ≥ 2RT/(F·j0) (계면 둘).  [우리 산술 · 25 °C 가정 — 원문 온도 미기재] Rct·j0 = 52–145 mV = **2RT/F (51.4 mV) 의 1.0–2.8 배** (기본 조건 CR2032 0.20 µA: 58.9 mV = 1.15 배 · 0.20 mm 펠릿 52.2 mV = 1.02 배 · 받은 그대로 칩 145 mV = 2.8 배).  ⇒ 기본 조건에서는 대체로 맞지만, "겉보기 j0" (고전류 가지의 x 절편) 는 훑기 속도 · 피막에 따라 움직이는 **개시 · 한계 전류 표지**에 가깝다 [추정].
4. **두께 시리즈로 벌크를 갈랐나** — 못 갈랐다.  0.85 → 0.20 mm 의 벌크 변화 예상 ≈26–33 Ω·cm² [우리 산술] < 같은 조건 셀 사이 흩어짐 (Table I 327–478, ≈150) — n = 1 이면 묻힌다 (실측 327 · 341 · 261 비단조).

### 3-10. 없는 것 (본문 전수 — SI 미입수)
σ_ion · σ_e 값 · 측정 온도 · hot press · 격자상수 · XRD · 분말 입경 · 펠릿 밀도 측정법 · 두께 측정 상태 · 반복 수 · 표준편차 · round robin · 다압력 성형 · 스택압 아래 펠릿 두께 변화.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
NEI "fine" Li₆PS₅Cl (그대로) → ≈100 mg → ⌀10 mm 경화강 다이 → ≈50 MPa 수 초 → **360 MPa 2 분** → 펠릿 (1.55–1.60 g cm⁻³ · ≈0.80–0.85 mm) → 양면 Li ⌀8 mm (칩 · 포일 = 긁고 밀어 평탄화 · Li on Cu = 그대로) → 셀 (CR2032 물결 스프링 / ECC-Std / Swagelok 스프링 최대 / 10 MPa 압력셀) → ① 단계 정전류 (time-control 1 h × 1 · 3 · 5 사이클 / charge-control 1 mAh cm⁻²) + 사이클마다 PEIS (1 MHz–0.1 Hz · 50 mV) 또는 ② galvanodynamic 0.01 → 2 mA cm⁻² (0.20 µA cm⁻² s⁻¹ 기본 · 2.00 · 0.02 비교) + 앞뒤 PEIS → 단락 판정 (전압 급락 · PEIS 급락) · CCD (선형 끝) · "Rct" (기울기) · 겉보기 j0 (Tafel 절편) → 사후: 펠릿 표면 긁고 분쇄 → ssNMR (원문 표기 *"WB 500 MhZ Bruker Advance III"* · 2.5 mm 프로브 · MAS 20 kHz · ⁷Li 단일 펄스 · 반복 지연 30 s) · Li 표면 SEM (Ar 글러브박스 준비 · 밀폐 용기 운반) → 스택압: peel tester 하중–변위 (선형 구간 = 스프링 상수 · 급증 개시 = 하중).
- 안 한 것: σ_ion · 온도 제어/기록 · 밀도 측정법 기록 · 반복 통계 · 벌크/계면 분리 · 스택압 아래 셀 안 하중 실측 (대역 스페이서로 대신).

### 4-2. 입자 처리
- 실험 — 시뮬레이션 없음.  SE 는 냉간 압착 분말 펠릿 (입자 형상 · 크기 정보 없음).  관심은 SE 미세구조가 아니라 **Li 금속–SE 계면** (접촉 · 피막 · 덴드라이트 · stripping 공극).
- 우리 모델과의 관계: Li 금속 (항복 ≈0.8 MPa, `doux2020` 카드) 의 크리프 · 공극은 우리 DEM (강체 구) · MPM (SE J2) 어느 쪽에도 없는 물리다 → 이 논문의 CCD 결과는 모델로 옮기지 않는다.  옮길 수 있는 것은 **펠릿 밀도 한 점**과 **측정 관행**뿐.

### 4-3. 기법 미니 용어집
- **CCD (critical current density)**: 전해질이 무너지기 (덴드라이트 단락 · 급격한 분극) 전까지 버티는 최대 전류 밀도.
- **단계 정전류 (step chronopotentiometry)**: 전류를 계단으로 올리며 plate/strip 반복 — **time-control** (계단마다 같은 시간) vs **charge-control** (같은 전하, 예: 1 mAh cm⁻²).
- **galvanodynamic 분극 (programmed current chronopotentiometry)**: 전류를 일정 속도로 올리며 전압을 보는 법 — 저전류 선형 (BV 선형화) · Sand · Tafel 세 구간.
- **Sand 시간 · Sand 용량 (Bai 2016)**: 정전류에서 전극 표면 이온 농도가 0 이 되는 시간 · 그때까지의 전하 — 그 뒤 불안정 (덴드라이트) 도금.
- **겉보기 j0**: 기하 면적으로 나눈 교환 전류 밀도 — 도금 Li 거칠기 · 면적 변화 미반영.
- **soft short**: 단락인데 전압이 0 V 까지 안 떨어짐 (가는 Li 필라멘트 · 부분 접촉).
- **PEIS**: 정전위 임피던스 — 여기서는 단락 확인 (임피던스 급락) 용.
- **peel tester 로 스택압**: 셀을 닫는 데 드는 하중–변위 곡선 → 선형 구간 기울기 = 스프링 상수 · 급증 개시 하중 = 스택 힘.

---

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 단계 정전류 (a) time-control 1 h · (b) 3 사이클 · (c) 5 사이클 · (d) charge-control 1 mAh — 단락 0.50 / 0.20 / 0.20 / 0.10 mA cm⁻² | 같은 셀이라도 **프로토콜이 CCD 를 5 배 바꾼다** — 측정 규약을 값과 함께 적어야 한다는 증거 |
| 2 | (a) 선형 · Sand · Tafel 구간 모식 + 표면 피복 θ · (b) 훑기 속도 셋 · (c) 선형 구간 확대 + 직선 적합 · (d) Tafel (E vs log I) 절편 = 겉보기 j0 | ★ 기울기 = "Rct" 는 **Ω·cm²** (§3-9) · 판정법 설계 참고 |
| 3 | 셀 지그별 (a) 단계 정전류 (ECC-Std · Swagelok · CR2032 · 10 MPa 압력셀) · (b) galvanodynamic (CR2032 · ECC-Std · Swagelok tight · loose) | ★ 지그 · 조립이 저항을 2.4–7.4 배 바꾼다 — 우리 DC 분극 측정의 지그 · 압력 기록 근거 |
| 4 | peel tester 하중–변위 (a) 전 범위 (b) 0–1 mm 확대 — Swagelok · ECC-Std · CR2032 각 3 회 | 셀 안 스택압 실측법 · CR2032 스프링이 20 배 단단 |
| 5 | 두께 0.85 · 0.42 · 0.20 mm (a) 단계 정전류 (b) galvanodynamic | 두께 시리즈 n = 1 로는 벌크 항이 셀 산포에 묻힌다 (§3-9) |
| 6 | Li 원천 SEM — (a–c) 세척 전 칩 · 포일 · Li on Cu · (d, e) 세척 후 · (f) Cu 집전체 | 표면 피막 · 불순물 |
| 7 | Li 원천별 (a) 단계 정전류 (b) galvanodynamic (+ 받은 그대로의 칩) | 피막이 저항을 ≈6 배 키운다 |
| Tab 1 (Table I) | 훑기 속도별 j0 · "Rct" · CCD | 같은 셀형 3 셀 흩어짐 1.46 배 |
| Tab 2 (Table II) | 셀 지그별 j0 · "Rct" · CCD | 지그 효과 |
| Tab 3 (Table III) | 두께별 j0 · "Rct" · CCD (캡션은 "cell setups" 오기) | 두께 효과 |
| Tab 4 (Table IV) | Li 원천별 겉보기 j0 · "Rct" · CCD | 표면 효과 |

근거 크롭 (text, 같은 폴더): `txt_p2_title_abstract.png` (서지) · `txt_p3_materials_pellet.png` (★ 1.64 문장) · `txt_p10_ref22.png` · `txt_p11_ref40.png` (★ 인용 원문) · `txt_p4_thickness_0p80.png` · `txt_p6_rct_thickness.png` (두께) · `txt_p7_stack_pressure.png` · `txt_p8_stack_pressure.png` (스택압).  크롭 19 장 (그림 7 · 표 4 · 글 8) · 300 dpi · 전부 육안 확인.

## 6. Post-processing ★
- **무엇을 (저자)**: 저전류 직선 적합 → 기울기 "Rct" · 직선에서 처음 벗어나는 점 → CCD · 고전류 log i–η 직선의 x 절편 → 겉보기 j0 · PEIS 급락 → 단락 · ssNMR 263 ppm → Li 금속 확인 · 하중–변위 선형 적합 → 스프링 상수 · 급증 개시 → 스택 하중 → ÷ 0.5 cm² → MPa.
- **도구**: 전기화학 측정기 기종 · 적합 소프트웨어 · peel tester 기종 [미확인].
- **이 카드의 후처리**: 300 dpi 크롭 19 장 · 점선 기울기 판독 (단위 검사) · 두 밀도 기준 공극 표 · 결정학 밀도 재계산 · Rct·j0 ↔ 2RT/F · 스프링 감도 · 훑기 전하 검산 (§3).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 시료 | 순수 SE (NEI LPSCl) 펠릿 + Li 금속 양면 | 복합 양극 (NCM + LPSCl) · 순수 SE 침대 (E_SE 보정용) | 순수 SE 펠릿 밀도만 대조 가능 · CCD 는 우리 모델 밖 |
| 성형 | ≈100 mg · ⌀10 mm · **360 MPa 2 분** | DEM · MPM **300 MPa** (세대 2 = 서보 정적 300 MPa → 이완 → 판 제거 → 언로딩, `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` D2) | 압력 60 MPa 차 · 유지 시간 · 측정 상태가 다르다 |
| SE 진밀도 | 1.64 ("crystallographic", ref 22 — 뒷받침 안 됨) | 세대 2 = **1.64** (랩 표준, D10 · `docs/density_generations_20261014.md` · "실제 진밀도 미확인" 한정어) · 세대 1 = 2.0 | **같은 1.64 · 같은 미확인 지위** — 이 논문은 1.64 의 독립 근거가 못 된다 (§3-2) |
| 공극 (순수 SE) | 저자 계산 없음 → [우리 산술] 1.64 기준 2.4–8.7 % · 1.86 기준 14.0–19.5 % (360 MPa) | 세대 2 표적 ε_union **10–13 %** (300 MPa + 이완, D6 · D9) | §7-2 |
| 작동압 | 0.20–0.28 MPa (상용 셀) · 10 MPa (압력셀) | 모델은 제조압만 (작동압 축 없음) | Doux 와 함께 읽기 (§7-5) |
| 수송 | σ 없음 · 계면 "Rct" (Ω·cm²) | 접촉망 σ_ion · σ_e · κ (Holm 협착) · 복셀 STEP3 | 직접 비교 없음 |

### 7-2. ★ 세대 2 순수 SE 보정 표적 (300 MPa + 이완 · ε_union 10–13 % · 1.64) 에 주는 점
- **이 논문이 주는 점 하나**: 360 MPa · 2 분 · NEI 순수 LPSCl · ≈100 mg · ⌀10 mm → ρ 1.55–1.60 (인쇄) / 1.50–1.59 (두께로 역산) g cm⁻³ · 측정 상태 [미확인] (다이에서 꺼낸 뒤로 보이나 근거 없음 — [추정]).
- **연산자**: 실험 공극 = 질량 ÷ 기하 부피 ÷ ρ_s = **ε_sphere (질량 보존) 쪽** (D9 의 *"랩 펠릿 … 은 ε_sphere 로 대조"*) — DEM 의 ε_union 표적과 같은 연산자가 아니다 (순수 SE 침대는 겹침 때문에 ε_union > ε_sphere).
- **표적 밴드를 밀도로 바꾸면** [우리 산술]: ε(1.64) 10–13 % ⇔ ρ **1.427–1.476** g cm⁻³ ⇔ ε(1.86) **20.6–23.3 %** ⇔ 100 mg · ⌀10 mm 두께 **0.863–0.892 mm**.

| 비교 (ρ_s 기준) | 이 논문 360 MPa | 표적 (300 MPa) | 판단 |
|---|---|---|---|
| 1.64 | 2.4–5.5 % (인쇄 밀도) · 3.0–8.7 % (두께 역산) | 10–13 % | 이 논문 펠릿이 **≈1–11 %p 더 치밀** — 압력 차 (360 vs 300) 로 메울 수 있나는 아래 |
| 1.86 | 14.0–16.7 % · 14.4–19.5 % | 표적 밴드를 1.86 으로 옮기면 20.6–23.3 % | 이 논문이 **≈1–9 %p 더 치밀** (밀도 차는 기준과 무관 — 1.50–1.60 ↔ 1.43–1.48 g cm⁻³) |

- **압력 다리 (거친 어림 · [추정])**: Heckel 단계 II 기울기 K = 32.3 ×10⁻⁴ MPa⁻¹ (`lee2025_heckel_…` 상용 Li₆PS₅Cl · 다이 안 · 다른 분말) 를 빌리면 ε(300)/ε(360) = exp(60K) = 1.21 → 이 논문 펠릿의 300 MPa 등가 ρ ≈ **1.48–1.54** → ε(1.64) ≈ **5.8–9.5 %** · ε(1.86) ≈ 17.0–20.2 %.  ⇒ **1.64 기준으로 읽으면 표적 10–13 % 는 문헌 펠릿보다 약간 성기다 (표적이 ρ 1.43–1.48 을 요구)** — 단, 다이 안 기울기를 다이 밖 값에 쓴 어림 · 다른 분말 · 상태 미상이라 **숫자 판정에 쓰지 않는다**.
- **제일 큰 손잡이는 밀도 기준이다**: 같은 펠릿이 1.64 ↔ 1.86 으로 **≈11 %p** 옮겨진다 — 표적 폭 (3 %p) 의 ≈4 배.  표적이 "1.64 로 계산한 랩 펠릿 값" 이라면 진밀도가 1.86 일 때 그 펠릿의 실제 공극은 ≈21–23 % 다 (위 표).
- **같은 밀도 선택이 복합체 조성도 바꾼다** [우리 산술]: NCM 4.85 기준 AM:SE = 81.6 : 18.4 wt 의 SE 부피 몫 = **40.0 % (SE 1.64) ↔ 37.0 % (SE 1.86)** (80 : 18 wt 면 39.95 ↔ 36.97 %) — 세대 2 덱의 SE 개수 (`dem_protocol_gen2_plan_draft_20261014.md` §3-2 의 ×1.22) 도 기준에 따라 달라진다.
- **다압력 Heckel**: 없음 (성형은 360 MPa 한 점 · 50 MPa 예압은 수 초 · 밀도 미측정).

### 7-3. ★ 1.64 ↔ 1.86 — 결정 전에 알아야 할 것
1. **결정학 값은 1.86** (Z = 4 · a 9.859–9.861 Å, 정본 세 카드) · 실측 피크노미터 **1.874** (`ohno2020` 랩 D) · **이 논문과 같은 상품명 NEI "fine" 의 진밀도 인쇄값 1.87** (`frankenberg2025_…`).  1.64 는 결정학으로 불가능 (a 10.28 Å 필요).
2. **1.64 를 "진밀도" 로 쓰는 문헌은 많지만 근거가 붙은 것을 정본에서 못 찾았다** — 이 논문은 ref 22 를 붙였으나 그 문헌은 1.860 이다 (§3-2).  `lee2025_heckel_…` 는 "calculated" 라고만 썼다.
3. **랩 펠릿 가늠 규칙** (`docs/density_generations_20261014.md` §7 — 결과 전 규칙): 겉보기 ρ > 1.64 (불확도 넘어) 이면 그 로트에서 1.64 는 진밀도일 수 없다 · ρ ≤ 1.64 이면 못 가른다.  이 논문 (ρ ≤ 1.60) 은 **못 가르는 쪽**이다.  반면 `ohno2020` 랩 C (1.77) · G (1.70) · D (1.655) 는 **1.64 를 넘는다** — 다른 분말이지만 "Li₆PS₅Cl 진밀도 ≥ 1.77" 의 문헌 하한 [정본 카드 · 우리 산술].
4. 1저자 랩이 그 규칙을 쓸 때 이 논문이 경계를 알려준다: **100 mg · ⌀10 mm 에서 0.776 mm 보다 얇아야** 1.64 를 넘는다 — 360 MPa 의 이 논문 · `ohno2020` 랩 B (375 MPa) 는 0.795–0.85 mm 라 넘지 못했다.  더 높은 성형압 (랩 D 720 MPa → 1.655) 이나 더 치밀한 분말에서만 가를 가능성이 있다 [우리 산술 · 추정].

### 7-4. ★ DC 분극 σ_e 비 2.77 (SBE 4.47 · DBE 12.4 mS cm⁻¹, CLAUDE.md 10-12 kgy 앵커) — 이 논문이 주는 측정 관행
- 이 논문은 σ_e · 차단 전극 · 복합 양극을 다루지 않는다 — **직접 답은 없다**.  옮길 수 있는 것 (Li|SE|Li · 0.2 MPa 대):
  - 같은 셀형 · 같은 조건 3 셀의 총 저항 흩어짐 **1.46 배** · 지그만 바꿔 **2.4 배** (스택압이 비슷해도) · 스프링 느슨 **7.4 배** · 표면 피막 **6.3 배** (2073/327) [인쇄 Table I–IV · 우리 산술].
  - 그 저항의 **≈85–90 % 가 계면** (§3-9) — 이 경우 지그 · 압력 · 표면이 결과를 지배한다.
  - **두께 시리즈 n = 1 은 벌크를 못 가른다** (예상 벌크 변화 ≈30 Ω·cm² < 셀 산포 ≈150) — 반례로 쓸 수 있다.
  - 고정 간극 셀은 시료 두께 0.1 mm 가 힘을 36 % 바꾼다 (CR2032).
- 우리 2.77 에 대한 함의 [우리 산술 · 조건부]: 접촉 ASR R_c 가 두 시료에 같다면 겉보기 비 = (L/σ_SBE + R_c)/(L/σ_DBE + R_c) — **접촉은 비를 1 쪽으로 누른다** (그 경우 2.77 은 참 비의 아래 한계).  규모 감각 (두께 L 미확인 — 100 µm 가정): 벌크 ASR 2.24 (SBE) · 0.81 (DBE) Ω·cm² — R_c 가 ≈1 Ω·cm² 자릿수면 비가 크게 줄어든다.  접촉이 서로 다르면 어느 쪽으로든 움직인다.
- **권고 (우리 판단)**: "다시 재야 하나" 는 측정 조건 기록 (n · 지그 · 하중 · 두께 · 두께 시리즈 여부) 을 먼저 본다 — 기록이 없으면 2.77 에 불확도를 붙일 수 없다 (CLAUDE.md 10-12 *"측정 조건 미확인"* 과 같은 결론).  재측정이면: 같은 지그 · 하중계로 하중 기록 · 두께 2 점 이상 × 각 n ≥ 3 (기울기로 벌크 σ_e) · 두 시료를 같은 날 같은 절차로.

### 7-5. 작동압 (스택압) ↔ 제조압 — Doux 와 함께 읽기
- Doux 2020 (정본 카드): 25 MPa 압착 뒤 **5 MPa 가 최적** · ≥25 MPa 는 Li 가 18 % 연결 공극으로 크리프 → 단락 · 계면 임피던스 1 MPa >500 Ω → 25 MPa 32 Ω (포화).  이 논문: **0.20–0.28 MPa 는 접촉 부족** (Rct 지배 · CCD ≈0.1) · 10 MPa 에서 개선 · <5 MPa 에서 stripping 공극 증가 (ref 31).  ⇒ 두 논문이 합쳐 **작동압 창 (≈5–10 MPa)** 의 양쪽 끝을 준다 — 너무 낮으면 접촉 · 공극, 너무 높으면 크리프 단락.
- 우리 모델: 펠릿 압밀 (제조압 360–370 MPa) 은 작동압 (≤10 MPa) 에서 더 진행되지 않는다 (`doux2020` 카드 §8 의 해석) — 우리 300 MPa 압밀 ↔ 작동압 축 분리 규약과 맞다.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 순수 SE 펠릿 밀도 한 점 (frame[5] "Both: macroscopic porosity" 축의 외부 대조점 후보) · 상용 셀 스택압 실측 · 계면 저항 지배의 크기.
- **없는 것**: 수송 σ (DEM 쪽) · 형상 소성 · 공극 흐름 (MPM 쪽) · 다압력 · 미세구조.  ⇒ **DEM · MPM 어느 반쪽도 이 논문이 검증하지 않는다** — 이 카드의 값은 실험 측 기준 (밀도 · 측정 관행) 으로만 쓴다.  frame[4]: 이 한 점으로 E_SE 를 다시 맞추지 않는다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **1.64 는 출처가 끊긴 값이다** — 이 논문의 "crystallographic 1.64" 는 인용 문헌 (1.860) 과 맞지 않고 결정학으로 불가능하다.  세대 2 의 "SE 진밀도 1.64 (랩 표준)" 은 **값이 아니라 관례**로 표지를 유지하고, 결정 (D4 · D10 의 "실제 진밀도 미확인") 은 1.86 (결정학) · 1.874 (피크노미터, Ohno 랩 D) · 1.87 (NEI "fine" 인쇄값, Frankenberg 2025) 과 나란히 적어 둘 것.
2. **표적 밴드의 의미는 밀도 기준이 정한다** — 같은 펠릿이 1.64 ↔ 1.86 으로 ≈11 %p 옮겨진다.  ε_union 10–13 % 를 실험과 맞출 때 기준 밀도를 표적 문서에 같이 봉인해야 한다 (규율 ⑥).
3. **랩 펠릿 기록 칸** (`docs/density_generations_20261014.md` §7 과 같은 목록): 질량 0.1 mg · 두께 여러 점 · 꺼낸 뒤 지름 · 두께를 잰 상태 · 성형압 · 유지 시간 — 이 논문이 **빠뜨린 칸이 바로 그것들**이라 문헌 대조가 막힌다.
4. **DC 분극 σ_e (SBE/DBE)**: 지그 · 하중 · 두께 시리즈 × n 을 기록 — 계면 몫이 크면 비가 눌린다 (§7-4).
5. CCD 수치 자체는 우리 모델에 쓰지 않는다 (Li 금속 음극 · 모델 밖).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Cold-pressing ≈100 mg of commercial Li₆PS₅Cl (NEI) in a 10-mm die at 360 MPa for 2 min gave pellets of 1.55–1.60 g cm⁻³ and ≈0.80–0.85 mm thickness (Tron et al., *J. Electrochem. Soc.* 2023), i.e. 83–86 % of the crystallographic density of ≈1.86 g cm⁻³ (Z = 4, a ≈ 9.86 Å; our arithmetic)."
- "In Li|Li₆PS₅Cl|Li cells at 0.20–0.28 MPa stack pressure, the low-current resistance varied 2.4-fold between commercial cell setups and 7.4-fold between a tight and a loose Swagelok spring, with galvanodynamic critical current densities of 0.035–0.115 mA cm⁻² across these setups (Tron et al. 2023)."
- 국문: *"상용 Li₆PS₅Cl 100 mg 을 ⌀10 mm 다이에서 360 MPa 로 2 분 누른 펠릿은 1.55–1.60 g cm⁻³ (≈0.80–0.85 mm) 이다 (Tron 2023) — 결정학 밀도 1.86 기준 공극 14–17 % [우리 산술].  원문이 적은 '결정학 밀도 1.64' 는 그 인용 문헌의 값 (1.860) 이 아니다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **"crystallographic density of 1.64"** — 인용 근거 (ref 22) 와 불일치 · 결정학적으로 불가능 (§3-2).  펠릿이 "Dense" 하다는 함의 (≈95–98 %) 도 같이 무너진다 — 1.86 기준 83–86 %.
2. **단위 · 표기 오기**: "Rct [Ω]" = Ω·cm² 숫자 (§3-9) · "1 mAh" = 1 mAh cm⁻² · "1.64 g cm3" (음수 지수 빠짐) · *">1 mS cm−2"* (전도도 단위 cm⁻¹ 여야) · Table I 머리 *"sweep rate [µA cm−2 s]"* (s⁻¹) · *"sweep rates of 0.20 µA cm−2"* (s⁻¹ 빠짐) · 힘 (N) 을 "stack pressure" 로 부름 · *"1.6 to 1.55"* (범위 역순).
3. **본문 ↔ 표 불일치**: CR2032 "Rct" 본문 478 ↔ Table II 327 · Swagelok 본문 334 ↔ 표 269 · Li 원천 본문 324 / 305 / 323 ↔ Table IV 327 / 323 / 305 · Table III 캡션 "cell setups" · *"highest for the thin one (0.20 mm)"* ↔ 표 최대 0.42 mm.
4. **"j0 directly proportional to the sweep rate"** — log–log 기울기 0.18 (비례 아님) · 훑기 전하 *"4.00 / 0.40 / 0.04 mAh"* 는 프로토콜로 재현 안 됨 (§3-5).
5. **"Rct" = 벌크 + 두 계면** · Eq 2 를 단일 전극 꼴로 대칭셀에 적용 · 겉보기 j0 는 개시 · 한계 전류 표지에 가깝다 [추정] (§3-9).
6. **n = 1 · 오차 없음** — Table I 의 세 셀은 훑기 속도와 셀이 같이 바뀌어 교란 · 두께 시리즈의 "같은 압력" 은 43 N mm⁻¹ 스프링 · 스페이서 단위로 보장되지 않는다 [우리 산술 · 추정].
7. **스택압 실측 = 1.9 mm 대역 스페이서** (실제 적층 2.00–2.15 mm) — CR2032 는 실제 힘이 더 클 수 있다 [추정].
8. **측정 온도 미기재 · EIS 진폭 50 mV** (계면 비선형 구간일 수 있는 큰 진폭 — [추정]) · SI 미입수 (EIS 스펙트럼 · ssNMR · 장기 사이클 미확인).
9. **참고문헌 목록 결함**: ref 22 · 40 = 같은 논문 (연도 2020 · 2019) · ref 41 저자 목록에 *"A. C. S. Appl, Energy Mater."* 가 저자처럼 섞임 · ref 22 의 *"Adv, Energy Mater."* 쉼표.
10. **전이 한계**: Li 금속 계면 CCD ↔ 우리 복합 양극 수송 (다른 계) · 단일 성형압 360 MPa ↔ 우리 300 MPa · NEI 분말 (입경 미상) ↔ 랩 분말 · 펠릿 밀도 측정법 · 상태 미상.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 22 (= 40) | J.-M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. Wang, E. A. Wu, C. Jo, H. Yang, and Y. S. Meng, Adv, Energy Mater., 10, 1903253 (2020) | 정본 카드 있음 (`doux2020_stack_pressure_assb`) — **원문 PDF 에서 "1.64" 직접 검색 · Table S2 대조** (이 카드의 남은 확인) |
| 14 | S.-Y. Ham et al., Energy Stor. Mater., 55, 455 (2023) | 압력 아래 LPSCl CCD 0.3–2.15 mA cm⁻² 의 출처 |
| 24 | P. Bai, J. Li, F. R. Brushett, and M. Z. Bazant, Energy Environ. Sci., 9, 3221 (2016) | Sand 용량 · 한계 전류 ∝ 1/L |
| 31 | H. Yan, K. Tantratian, K. Ellwood, E. T. Harrison, M. Nichols, Y. Cui, and L. Chen, Adv. Energy Mater., 12, 2102283 (2022) | 스택압 <5 MPa 에서 stripping 공극 · j0 와 안정성 |
| 37 | S. Randau et al., Nat. Energy, 5, 259 (2020) | 본문이 "비상용 (자작) 측정 셋업" 문제의 근거로 인용 (PDF p.7) |
| 38 | M. Batzer, K. Voges, W. Wang, P. Michalowski, and A. Kwade, Materials Today Communications, 30, 103189 (2022) | 이 논문의 10 MPa 실험 압력셀 원전 (PDF p.7) |
| 15 | Y. Lu, C.-Z. Zhao, H. Yuan, X.-B. Cheng, J.-Q. Huang, and Q. Zhang, Adv. Funct. Mater., 31, 2009925 (2021) | CCD 측정의 두 주 변수 (계단 시간 · 계단당 사이클 수) 의 근거 (PDF p.2–3) |
| 19 | D. K. Singh, A. Henss, B. Mogwitz, A. Gautam, J. Horn, T. Krauskopf, S. Burkhardt, J. Sann, F. H. Richter, and J. Janek, Cell Reports Physical Science, 3, 101043 (2022) | "수십–수백 MPa · 고온" CCD 측정 사례로 인용 (PDF p.2) |
| 43 | J. Kasemchainan, S. Zekoll, D. S. Jolly, Z. Ning, G. O. Hartley, J. Marrow, and P. G. Bruce, Nat. Mater., 18, 1105 (2019) | 계면 문제를 사이클 중 고압으로 푸는 문헌 사례로 인용 (refs 19 · 42 · 43, PDF p.10) |
| 44 | J.-S. Kim et al., Nat. Commun., 14, 782 (2023) | 연성 계면층 계열 접근으로 CCD 를 높인 사례로 인용 (refs 11 · 44, PDF p.10) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-14)
- PDF 11 쪽 (IOP 표지 1 + 본문 10) 전부 100 dpi 렌더로 읽고 `pdftotext` 로 인용문 대조 · 인용문 · 표 칸은 300 dpi 크롭 19 장으로 다시 확인 (전부 육안).  인쇄 쪽 번호가 없어 PDF 쪽으로 적었다.
- 서지 (제목 · 저자 넷 · 소속 · JES 170 100525 · DOI 10.1149/1945-7111/ad01e3 · 투고 · 수정 · 출판일 · CC BY 4.0) = PDF p.2 인쇄 + PDF 메타데이터 Subject 줄 (*"Journal of The Electrochemical Society, 170(2023) 100525. doi:10.1149/1945-7111/ad01e3"*) 일치.
- "1.64" 텍스트 검색 = PDF p.3 한 곳뿐 · ref 22 (p.10) · ref 40 (p.11) 원문 크롭.
- Doux 2020 쪽 값은 정본 카드 `doux2020_stack_pressure_assb` (f98988e6c) §2.1 · §6 + 리포 `docs/data/doux2020_stack_pressure.csv` (C 절, `table_stated`) — Doux 원문 PDF 는 이 작업에서 열지 않았다.  결정학 · 피크노미터 · 랩별 펠릿 값은 정본 `ohno2020_interlab_…` §3.1 · §3.3 · `kraft2017_…` · `adeli2019_…` 카드.
- "Rct" 단위 판단 = Fig 2c · 3b · 5b · 7b 점선 기울기 판독 (±15 %) + Fig 1a 계단 전압 — 표 숫자와 Ω·cm² 로 일치 · Ω 해석 (×≈2) 은 배제.
- 교차 카드 (읽기만): `frankenberg2025_…` (NEI "fine" 진밀도 1.87 · x50 17 µm — 정본) · 같은 묶음 `beutl2024_…` §3-3 (같은 1.64 에 다른 인용 [37] · [10] — 정본 반입 전 스테이지 카드 · 그 카드의 "라벨 + 인용 번호를 함께 준 첫 논문" 문장은 이 논문 (2023-10) 이 더 이르다).
- 정본 litdb 중복 확인: `git ls-tree` papers/ 438 편 전수 + DOI (`ad01e3`) · 저자 (`Beutl` · `Artur Tron`) · 제목 낱말 grep (f98988e6c) — 없음.  같은 묶음에 같은 AIT 그룹 (Beutl) 의 round robin 카드가 따로 만들어지는 중 (아래).

## 🔗 관련 카드
- 1.64 · 진밀도 계보: `doux2020_stack_pressure_assb` (ref 22 — 1.860) · `ohno2020_interlab_ionic_conductivity_argyrodite` (1.86 · 1.874 · 8 랩 펠릿) · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` (NEI "fine" 진밀도 1.87 · x50 17 µm) · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` (TD 1.64 "calculated") · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` · `adeli2019_halide_substitution_boosting_argyrodite` (격자상수) · 1.64 사용처 `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `bazzoun2026_dem_fem_rnm_ionic` · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` · `lee2026_lpscl_coating_thickness_ncm811` · `oh2026_bimodal_composite_cathode`.
- 압력 · 펠릿 · σ: `cronau2021_stack_pressure_ionic_conductivity` · `miss2026_insitu_conductivity_porosity_pressure_compaction` (결정밀도 1.87 기준 · 회복) · `miss2026_pressure_tortuosity_composite_cathode_coating`.
- Li 금속 계면 · CCD: `hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd` · `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`.
- 같은 묶음 (10-14b · 정본 반입 전 · 내용 미대조): `beutl2024_round_robin_coin_cell_sulfide_assb` (같은 AIT Beutl — 실험실 간 흩어짐) · `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` (hot press · 압력 무관 σ — 이 논문에 없는 축).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
