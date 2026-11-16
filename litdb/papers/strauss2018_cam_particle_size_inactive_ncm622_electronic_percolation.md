<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 3 순위 · N-77 · 정독 126) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음 카드들과 같은 꼴.
     원문 = 출판본 Letter (ACS Energy Lett. 2018, 3, 992−996 · PDF 5 쪽) + Supporting Information (PDF 8 쪽 = S-1 표지 + S-2 … S-8).
     쪽 표기 = 본문은 "p.n" = PDF 쪽 n (학술지 쪽 = 991 + n · p.1 = 992 … p.5 = 996) · SI 는 "SI p.n" = SI PDF 쪽 n (= 인쇄 S-n · SI p.1 = 표지).
     크롭 파일 이름의 pN · SIpN 과 figures.json 의 page 는 그 PDF 의 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 75 행 —
     본문 그림은 300 dpi 래스터 (xref 99 · 125 · 126 · 127) 를 그대로 꺼내 눈금 위치 · 색 분리 · 성분 중심으로 읽었고, SI 그림은 300 dpi 쪽 렌더에서 읽었다) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 ·
     [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 5 쪽 + SI 8 쪽 전수에 없음.
     원문 13 쪽은 글자 층 추출 + 그림 전부 열람으로 읽었다.  DEM · 입자 계산 · 압밀 시뮬레이션 · 모델은 없다 — 실험 Letter. -->
# NCM622 2차 입자 크기 (d50 4.0 / 8.3 / 15.6 µm) 가 탄소 없는 β-Li₃PS₄ 복합 양극 (7 : 3 wt) 의 용량을 가른다 — 첫 충전 162 / 95 / 84 mAh g⁻¹ · ex situ XRD 비활성 CAM 2 / 27 / 31 % · DC 분극 전자 부분 전도도 ≈10⁻³ → ≈10⁻⁶ S cm⁻¹ (이온 ≈10⁻⁶ · 크기 무관) = AM 망의 전자 percolation (같은 분말의 액체 LIB 는 크기 차 없음) — Strauss · Bartsch · de Biasi · Kim · Janek · Hartmann · Brezesinski (ACS Energy Lett. 2018)

> slug `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` · DOI `10.1021/acsenergylett.8b00275` · type `experiment (carbon-free NCM622 : β-Li₃PS₄ = 7 : 3 wt powder composite · CAM d50 4.0 / 8.3 / 15.6 µm · 정전류 C/10 · C/30 · C/50 · ex situ XRD 두 상 Rietveld 비활성 CAM + operando XRD 액체 셀 격자 보정 · DC 분극 이온 / 전자 부분 값 (55 MPa 누른 채) · AM–AM electronic contact 부족 · 단면 SEM/EDX · 액체 LIB 대조 — DEM · 모델 · 기공 측정 없음)` · PDF `b10f8cff-77._Impact_of_cathode_material_particle_size_on_the_capacity_of_bulk-type_all-solid-state_batteries.pdf` · SI `b0965bf7-77._Sup_Impact_of_cathode_material_particle_size_on_the_capacity_of_bulk-type_all-solid-state_batteries.pdf` · digested `2026-11-16` · status ✅
>
> **원제**: *Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries* (p.1)
> **저자**: **Florian Strauss\*** ᵃ · Timo Bartsch ᵃ · Lea de Biasi ᵃ · A-Young Kim ᵃ · Jürgen Janek ᵃ˒ᵇ · Pascal Hartmann ᵃ˒ᶜ · **Torsten Brezesinski\*** ᵃ — ᵃ Battery and Electrochemistry Laboratory (BELLA), Institute of Nanotechnology, Karlsruhe Institute of Technology (KIT) · ᵇ Institute of Physical Chemistry, Justus-Liebig-University Giessen · ᶜ BASF SE, Ludwigshafen — \* 교신 (Strauss · Brezesinski) · *ACS Energy Lett.* **2018**, **3**, **992–996** (Letter · 호 4 = 쪽 옆 내려받기 주소 "…/article-pdf/3/4/992/…" — 인용 줄에는 호가 인쇄되지 않음) · 접수 2018-02-16 · 승인 · 출판 2018-03-21 · 연구비 = BASF International Network for Batteries and Electrochemistry (T. Bartsch = BMBF ARTEMYS) · 이해상충 없음.
> **이웃 카드 (링크만)**: 가리킨 카드 [`hippauf2019_dry_film_ptfe_sulfide_cathode_sheet`](hippauf2019_dry_film_ptfe_sulfide_cathode_sheet.md) (ref 24 · L276) · [`kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`](kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md) (ref 10 · L282) · [`schmitt2026_chemomech_stability_dry_cathode_separator_sheets`](schmitt2026_chemomech_stability_dry_cathode_separator_sheets.md) (ref 16 · L405 · 같은 KIT BELLA 그룹 · 교신 Brezesinski · Strauss) · [`lei2026_se_particle_size_effects_review`](lei2026_se_particle_size_effects_review.md) (ref [184] · L122 · L207 · L242 · L244 · L279) / 이 논문을 인용한 다른 정본 카드: [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (ref 13) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref [13]) · [`minnmann2022_designing_cathodes_solidstate`](minnmann2022_designing_cathodes_solidstate.md) (ref 36) · [`cronau2022_wet_milling_particle_size_ionic_conductivity`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) ([21]) · [`famprikis2019_fundamentals_inorganic_sse`](famprikis2019_fundamentals_inorganic_sse.md) (76).
> **판독 원자료**: `litdb/figures/strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation/digitized.csv` (75 행 — 그림 4 표지 6 · 그림 1d · 1e · 2a–c 곡선 끝점 · 그림 3b 십자 6 · SI 그림 S2 봉우리 8 · S4 부피 12 · S6 전류 13 · S3 축 점검 · S7 눈금 · 두께) · 그림 크롭 **43 장** (도구 12 중 다시 자름 3 + 손 크롭 31 = 그래픽 초록 1 · 패널 14 · 식 2 · 근거 문단 14) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 코팅 없는 NCM622 (BASF) 의 **다결정 2차 입자 크기만** 바꾼 세 분말 (d50 **4.0 · 8.3 · 15.6 µm** · NCM-L 은 NCM-M 을 20 µm 체로 쳐서 위에 남은 것) 을 β-Li₃PS₄ 와 **7 : 3 wt (탄소 없음)** 로 볼밀 혼합해 375 MPa 로 성형한 반쪽 셀 (In 음극 · 55 MPa · 25 °C) 에서 — 첫 충전 (C/10) 이 **162 → 95 → 84 mAh g⁻¹** 로 떨어지고 (p.2), 충전된 복합체의 ex situ XRD 003 봉우리가 둘로 갈라져 **충전 안 된 (비활성) CAM 이 2 → 27 → 31 %** (p.3 · SI 표 S1) 이며, 같은 조성의 DC 분극 (55 MPa 누른 채) 으로 잰 **전자 부분 전도도가 ≈10⁻³ → ≈10⁻⁶ S cm⁻¹ (3 자릿수)** 떨어지는 동안 **이온 부분 전도도는 ≈10⁻⁶ S cm⁻¹ 로 크기와 무관**하다 (p.3–4 · 그림 4).  저자 결론: 큰 입자 복합체에서는 *"not all of the particles are electronically connected"* — 비활성 CAM 은 **전자 접촉 부족** 탓이고, 작은 입자 (≪10 µm) 는 거의 다 충전되며 그때 남는 한계는 **느린 이온 수송**이다 (p.4).  같은 분말의 액체 LIB (탄소 4 wt %) 는 크기 차가 *"negligible"* 이다 (p.2) — 크기 효과는 **고체 복합체 (탄소 없음) 의 망 연결**에서 온다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ CAM 입경 설계 (우리 PC/SC) | NCM622 (60 % Ni) **다결정 2차 입자** 세 크기: L d50 **15.6** / d90 26.1 · M **8.3** / 13.0 · S **4.0** / 4.8 µm (측정법 [미확인]) · 셋 다 구형 2차 입자 덩이 (SEM 그림 1a–c) — **단결정 (SC) 은 없다**.  S · M = BASF 공급 · L = M 을 20 µm 체로 친 위쪽 (같은 합성 · 크기만 다름) | [인쇄] p.2 · SI p.2 · 그림 1a–c |
| ② ★ SE · 조성 | β-Li₃PS₄ (THF 습식 · 140 °C ≥12 h 진공) · 맨 SE σ **"approximately 0.2 mS/cm"** (측정 조건 [미확인]) · **SE 입경 [미확인]** (본문 · SI 어디에도 없음) · 복합 = β-Li₃PS₄ : NCM622 **3/7 w/w** · 행성 밀 140 rpm 30 min (10 mm ZrO₂ 볼 10 개 · 70 mL · 1 g) · **탄소 · 결합제 없음** · 고체 중 AM 부피 ≈0.48 [카드 산술 · 진밀도 가정 — §3-1] | [인쇄] p.2 · p.3 · SI p.2 |
| ③ ★ 성형압 · 측정압 | 반쪽 셀: β-Li₃PS₄ 60 mg 를 ≈125 MPa (≈400 µm) → 복합 10–12 mg (≈90 µm · 1.9 mAh cm⁻²) 를 **375 MPa** → In 박 (100 µm · Ø 8 mm) 125 MPa → 운전 **55 MPa** · 25 °C / DC 분극: 전자 = 복합 ≈100 mg **375 MPa 2 min** (SS 플런저 사이) · 이온 = 복합 250 MPa + 유리 250 MPa + In/Li 원판 → 전체 375 MPa 2 min · 측정 중 **55 MPa** / **본문에는 압력 숫자가 하나도 없다** (전부 SI) | [인쇄] SI p.2–3 |
| ④ ★ 전기화학 (C/10 첫 사이클) | 첫 충전 **162 (S) · 95 (M) · 84 (L) mAh g⁻¹** · 첫 CE **70 · 55 · 50 %** · 분극 LIB 대비 **+100–200 mV** · C/30: S *"approximately 190"* · M 120 · L 100 · C/50 L 100 → **110** — [판독] 그림 1e 방전 끝 S 109.8 · M 55.7 · L 42.3 → CE 0.68 · **0.59** · 0.51 (M 은 본문 55 % 와 다르다 · §3-6) | [인쇄] p.2 · [판독] 그림 1e · 2 |
| ⑤ ★ 비활성 CAM | ex situ XRD (충전 3.8 V vs In/InLi 뒤 · 펠릿 그대로 · Si 내부 표준) 003 봉우리 두 상 Rietveld → 비활성 **2 (S) · 27 (M) · 31 % (L)** (각 ±1 · SI 표 S1) · 활성 쪽 평균 x(Li) **0.46 · 0.56 · 0.53** (operando 액체 셀 a · c 보정곡선 · ±0.02) · 비활성 상 격자 = 처음 분말과 같음 · 이 SOC × 활성 분율로 **90 · 92 · 153 mAh g⁻¹** (L · M · S) 가 전기화학과 *"close"* · 오차: 상 분율 **−3 % (L · M) · −11 % (S · XRD 검출 한계)** | [인쇄] p.3 · SI p.4 · SI p.7 |
| ⑥ ★ 부분 전도도 (그림 4) | 이온 [판독] **1.29 × 10⁻⁶ (S) · 6.7 × 10⁻⁷ (M) · 8.8 × 10⁻⁷ (L)** S cm⁻¹ (본문 *"around 10⁻⁶"* · 맨 β-Li₃PS₄ 보다 *"roughly 2 orders"* 낮다) · 전자 [판독] **8.8 × 10⁻⁴ · 3.8 × 10⁻⁵ · 1.4 × 10⁻⁶** (본문 *"about 10⁻³ … to 10⁻⁶"*) → S→L **2.8 자릿수** · σ_e/σ_ion = **680 · 57 · 1.6** [카드 산술] · 방법: 300 mV 정전위 · 정상 영역 선형 맞춤 전류 · R = U/I · σ 식 (인쇄는 σ = (R×A)/l — 차원이 저항률 · §3-4) | [인쇄] p.3–4 · SI p.3 · [판독] 그림 4 |
| ⑦ 화학–역학 · 접촉 잃음 | **측정 없음** — 낮은 CE 를 *"most likely associated with different chemo-mechanical effects … the volume contraction during charging leads to a reduced electrical contact between the CAM particles and the SE"* (인용 [9, 18]) + 코팅 없는 NCM 의 SE 산화 분해 층으로 설명 (p.2) · 같은 시료의 충전 뒤 단위 격자 부피 **−1.68 (S) · −1.34 (M) · −1.32 % (L)** · a −1.6 … −1.8 % · c +1.8 … +2.0 % [카드 산술 · SI 표 S1] | [인쇄] p.2 · SI p.7 |
| ⑧ DEM · 소성 · 2D/3D · 탈압 (네 질문) | DEM · 모델 **없음** · 소성 · 변형 낱말 0 회 · *"favorable mechanical properties of this class of SE materials allow good processability … even when cold pressed"* (p.1 · 한 문장) · percolation 문장 *"composites made of small particles offer many more contact points between them than those consisting of relatively large (spherical) particles"* (p.4 · 인용 [26] SOFC) · 탈압 · 되돌아옴 **없음** | [인쇄] p.1 · p.4 |
| ⑨ 저자 한계 | CE 차이 *"not yet fully understood"* · 건식 분말 혼합의 성분 분리 가능 (*"might be also affected by the particle size"* — SEM/EDX 로 *"do not reveal major inhomogeneities"*) · XRD 해석에 부반응 용량 미포함 · NCM-S 비활성 분율은 XRD 검출 한계 근처 | [인쇄] p.2 · p.4 · SI p.4 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **NCM622 (코팅 없음) + β-Li₃PS₄ (습식)** — 우리 NCM811 + Li₆PS₅Cl 이 아니다 · SE 입경 [미확인] ② 크기는 **다결정 2차 입자 d50** (측정법 [미확인]) — 단결정 ↔ 다결정 비교가 아니다 ③ 전도도 = **DC 분극 · 375 MPa 성형 뒤 55 MPa 누른 채 · 실온 · 첫 충전 전 (SOC 0) 복합체** — 충전 상태의 σ_e 는 재지 않았다 ④ 비활성 분율 = **첫 충전 뒤 한 번 · ex situ · 두 상 Rietveld** (전자 고립과 이온 고립을 가르지 않는다 · 그 원인 판정은 따로 잰 SOC 0 의 σ_e 로 한 것) ⑤ 기공 · 밀도 · 두께 실측 **없음** — 원문 대략값 (≈90 µm · 1.9 mAh cm⁻² · 10–12 mg) 끼리 서로 잘 맞지 않는다 (§3-1).
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방향** (같은 무게비 · 탄소 없음 · 크기만 바꾸면 작은 CAM 이 AM 전자 망을 잇는다 — 전자 σ ≈2.8 자릿수 · 비활성 CAM 2 → 31 %) 과 **측정 · 보고 꼴** (전자 고립 CAM 을 XRD 로 세는 법 · DC 분극 두 배치 · 같은 분말을 체로 갈라 크기만 바꾸는 설계) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-77 의 '왜' 칸)

의도 원문: *"입도 설계 — CAM 입경 효과 (우리 PC/SC) · SE 4 µm · NCM 5 µm 입경 효과 (hippauf2019 p.2 인용) · 같은 그룹 (schmitt2026) · lei2026 은 원 논문 카드 없음으로 적음"* (가리킨 카드 = hippauf2019 L276 · kawaguchi2023 L282 · schmitt2026 L405 · lei2026 L279)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "입도 설계 — CAM 입경 효과" | **채움** | 세 크기 d50 4.0 · 8.3 · 15.6 µm (p.2) → 첫 충전 162 · 95 · 84 mAh g⁻¹ (C/10 · 55 MPa · 25 °C · p.2) · 비활성 CAM 2 · 27 · 31 % (p.3) · 전자 σ ≈10⁻³ → 10⁻⁶ S cm⁻¹ (55 MPa 누른 채 · p.4) — 조성 7 : 3 wt · 탄소 없음 · 375 MPa 성형 (SI p.2–3) |
| "(우리 PC/SC)" | **일부** | **PC 크기 효과만** — 세 분말 모두 다결정 2차 입자 (초록 *"secondary particle size"* · SEM 그림 1a–c 의 구형 덩이) · **단결정 (SC) 시료 없음** · NCM-S 는 '작은 PC' 이지 SC 가 아니다 → 우리 모델의 "작은 AM = 단결정" 라벨 (AM_S) 을 이 논문으로 뒷받침하지 못한다.  또 크기 효과의 기전을 저자는 **입자 안 입계가 아니라 망의 접점 수** (percolation) 로 설명한다 (p.4) |
| "SE 4 µm" | **없음** | 원문 (본문 5 쪽 + SI 8 쪽) 에 **SE (β-Li₃PS₄) 입경이 없다** — 합성 (SI p.2) · XRD (그림 S1) 만 · SEM 없음.  **4.0 µm 는 NCM-S 의 d50** (p.2) |
| "NCM 5 µm 입경 효과" | **일부 (값 표기)** | NCM-S **d50 4.0 · d90 4.8 µm** (p.2) · 초록 · 서론 *"approximately 20 to 5 μm"* (p.1) · 결론 *"≪10 μm"* (p.4) — '5 µm' 은 범위의 끝 · d90 에 가깝다 |
| "(hippauf2019 p.2 인용)" | **대조 불가 (Hippauf 원문 없음)** | Hippauf 본문 p.2 의 그 문장은 이 트리에 PDF 가 없어 보지 못했다 · Strauss 원문 기준으로는 'SE 4 µm' 값이 없다 → 아래 2 차 인용 표 |
| "같은 그룹 (schmitt2026)" | **채움** | 교신 **Strauss · Brezesinski** (KIT BELLA) — schmitt2026 카드의 교신과 같다 · Janek 공저 · BASF 공저 (여기 Hartmann · 그쪽 Kondrakov) |
| "lei2026 은 원 논문 카드 없음으로 적음" | **채움 (해소)** | 이 카드로 원 논문 카드가 생겼다 · lei2026 L122 의 2 차 인용 값은 원문과 **모두 같다** (아래 표) |

**가리킨 카드 · 같은 논문을 인용한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `hippauf2019_…` L276 (ref 24) | 서지 *"F. Strauss, T. Bartsch, L de Biasi, A.-Y. Kim, J. Janek, P. Hartmann, et al., … ACS Energy Lett. 3 (4) (2018) 992–996"* · 메모 *"SE 4 µm · NCM 5 µm 입경 효과 (본문 p.2 인용)"* | 서지 ✓ (호 4 = 내려받기 주소) · **SE 입경은 원문에 없다** · 4.0 µm = NCM-S d50 · d90 4.8 µm | **일부** — 'SE 4 µm' 은 이 원문 값이 아니다 (Hippauf 원문의 그 문장은 미대조) |
| `kawaguchi2023_…` L282 (ref 10) | 서지 *"F. Strauss, T. Bartsch, L. De Biasi, A.Y. Kim, J. Janek, P. Hartmann, T. Brezesinski, … ACS Energy Lett. 3 (2018) 992–996"* · 메모 *"CAM 입경 효과 (우리 PC/SC)"* | 서지 ✓ (원문 'Lea de Biasi' · 'A-Young Kim' — 표기만) · **PC 크기 효과만 · SC 없음** | **일부** — 'PC/SC' 중 SC 쪽은 없다 |
| `schmitt2026_…` L405 (ref 16) | *"F. Strauss, et al., … ACS Energy Lett. 3 (2018) 992–996. — 카드 없음 — 같은 그룹 · CAM 입경 효과 (hippauf2019 카드 §11 에도 같은 행)"* | ✓ (hippauf2019 의 그 행은 §11 참고문헌 표 L276) | **채움** |
| `lei2026_…` L122 ([184]) | *"NCM622 + β-Li₃PS₄ · CAM NCM-S (D50 4.0 · D90 4.8 µm) vs NCM-L (15.6 · 26.1 µm) · 첫 충전 162 → 84 mAh g⁻¹ · 첫 CE 70 → 50 % · 전기화학 비활성 CAM 2 → 31 % · 이온 σ 무관 · 전자 σ 10⁻³ → 10⁻⁶ S cm⁻¹"* | 모두 ✓ (p.2–4) | **채움** |
| `lei2026_…` L207 · L242 | *"Strauss 비활성 CAM 2 → 31 % (CAM 크기)"* · *"SE 입도가 아닌 예가 SE 절에 — Strauss … 는 CAM 입도"* | ✓ | **채움** (리뷰의 분류 지적이 원문과 맞다) |
| `lei2026_…` L244 · L279 | *"카드를 만든 뒤 쓴다"* · *"Strauss 2018 → hippauf2019 · kawaguchi2023 (인용만)"* | 이제 카드 있음 | **채움 (해소)** |
| `bielefeld2019_…` L89 · L110 · L114 | *"carbon-free NCM-622 + LPS 에서 AM 입경↑(최대 20µm) → 전자전도 급락"* · *"ex situ XRD 의 inactive NCM-622 고분율"* · *"Strauss packing 밀도·porosity 미지"* · *"AM=5µm 채택 (… Strauss 현실값)"* | ✓ ('최대 20 µm' = 초록 *"approximately 20 to 5 μm"* · d50 최대 15.6) · 기공 · 밀도 미보고 ✓ | **채움** |
| `shi2019_…` L292 · L571 | *"도전제 없으면 CAM 자체 가 전자 percolation 가능"* · 정정 *"탄소 없이 CAM 이 전자를 날라야 하면 작은 CAM 이 유리 (ref [13] Strauss)"* | ✓ (p.1 · p.4) | **채움** |
| `minnmann2022_…` L88 | *"CAM 2차입자 최적 지름 3–5 µm (refs 36,37 = Strauss 2018 + Bielefeld 2019 인용)"* | 이 원문은 **최적을 말하지 않는다** — 가장 작은 시료 (d50 4.0) 가 셋 중 가장 좋았을 뿐 · 4 µm 아래는 재지 않았다 | **일부** — Minnmann 원문의 설계 문장 (카드는 그 원문을 옮긴 것으로 보인다 · Minnmann 원문 미대조) |
| `cronau2022_…` L89 ([21]) | *"p.1 (CAM < 5 µm 전형)"* | d90 4.8 µm 는 NCM-S 하나 · '전형' 은 이 원문 주장이 아니다 | **일부** (Cronau 원문의 인용 범위) |
| `famprikis2019_…` L394 (76) | *"Strauss et al., ACS Energy Lett. 3, 992 (2018) — cathode particle size ↔ capacity"* | ✓ | **채움** |

⇒ **의도 대조 결과: 일부** — CAM (다결정 2차 입자) 입경 효과 · 같은 그룹 · lei2026 의 '카드 없음' 은 **채움**; '우리 PC/SC' 는 PC 쪽만 (SC 없음 · 기전도 망 연결); **'SE 4 µm' 은 없음** (SE 입경 미보고 · 4.0 µm = NCM-S d50); 'NCM 5 µm' 은 d50 4.0 · d90 4.8 · 범위 끝 '≈5 µm' 로 **일부**.

---

## 1. 한 줄 요약
같은 화학 (NCM622 · BASF) 의 다결정 2차 입자를 세 크기로 (S · M = 공급 그대로 · L = M 을 20 µm 체로) 준비해 **탄소 없는** β-Li₃PS₄ 복합 양극 (7 : 3 wt) 으로 만들고, **액체 LIB 에서는 크기 차가 없는데 고체 셀에서는 첫 충전이 162 → 84 mAh g⁻¹ 로 반 토막** 나는 것을 보인 뒤, 그 원인을 **느린 반응 (저율로 일부 회복) 과 충전되지 않는 입자 (저율로도 회복 안 됨)** 로 나눈다.
충전된 복합체의 ex situ XRD 가 '충전된 NCM' 과 '처음 그대로인 NCM' 두 상을 동시에 보여 주고 (비활성 2 / 27 / 31 %), DC 분극이 그 이유를 **전자 경로** 로 가리킨다 (전자 σ 3 자릿수 ↓ · 이온 σ 그대로).
저자 결론: 탄소 없는 복합체에서는 *"size (and surface) tailored cathode active materials"* 가 필요하고, 작은 CAM 은 전자 망 문제를 풀지만 그때는 **이온 수송이 병목**이다 (p.4).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| F. Strauss\* · T. Bartsch · L. de Biasi · A-Y. Kim · J. Janek · P. Hartmann · T. Brezesinski\* (KIT BELLA · JLU Giessen · BASF SE) | ACS Energy Lett. 3 (4), 992–996 (2018) · Letter | 10.1021/acsenergylett.8b00275 | **β-Li₃PS₄** (습식 · 입경 [미확인]) + **NCM622** (코팅 없음 · d50 4.0 / 8.3 / 15.6 µm) · 탄소 없음 · In 음극 | 실험 (정전류 · ex situ / operando XRD Rietveld · DC 분극 · SEM/EDX · 액체 LIB 대조) |

- **1저자 메모 (후보 표) 와의 대조**: 저자 · 제목 · 학술지 · 권 3 · 쪽 992–996 · 2018 · DOI — **같다**.  표기만 다르다: 'L. De Biasi' ↔ 원문 **Lea de Biasi** · 'A.Y. Kim' ↔ **A-Young Kim**.  덧붙임: 호 4 (내려받기 주소) · Letter · 출판 2018-03-21.
- **글의 꼴**: Letter — 서론 → 재료 · 셀 → 첫 사이클 (그림 1) → 저율 (그림 2) → ex situ XRD + 보정 (그림 3) → 부분 전도도 (그림 4) → 결론.  번호 붙은 식 0 · 표 0 (본문) / SI: 재료 · 셀 · 측정 · Rietveld 세부 · 그림 S1–S7 · 표 S1 · 문장 안 식 둘 (R = U/I · σ).  **본문에는 압력 · 두께 · 질량이 없다** (전부 SI).
- 그룹 맥락: Strauss · Brezesinski · Janek (KIT BELLA / Giessen) — 같은 그룹 카드 `schmitt2026_…` · `minnmann2022_…` · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (Koerver 2018 EES — 이 논문의 [9] 는 Koerver 2017 Chem. Mater. 로 다른 논문) · `trevisanello2021_sc_pc_ncm_cracking_diffusion` (같은 그룹의 SC ↔ PC — 액체).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 조성 · 시편 (p.1–2 · SI p.2–3 · `txt_p1_carbon_free_cam_size_20_to_5um.png` · `txt_p2_sizes_d50_d90_protocol.png` · `txt_SIp2_materials_sieving_li3ps4_glass.png` · `txt_SIp2_cell_assembly_pressures_loading.png` · `fig_1abc.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CAM | Li₁₊ₓ(Ni₁₋ᵧ₋zCoᵧMn_z)₁₋ₓO₂ = **NCM622 (60 % Ni)** · **표면 코팅 없음** (*"pristine … without tailored surface coating"*) · 300 °C 밤새 진공 건조 | [인쇄] p.1 · SI p.2 |
| 세 크기 | **NCM-L d50 15.6 µm · d90 26.1** (단위 빠짐 — 원문 그대로) · **NCM-M 8.3 · 13.0 µm** · **NCM-S 4.0 · 4.8 µm** · 입도 측정법 [미확인] · 초록 *"approximately 20 to 5 μm"* | [인쇄] p.2 · p.1 |
| 크기 만든 법 | S · M = BASF 공급 · **L = M 을 20 µm 체로 쳐서 *"collecting the remaining fraction"*** — L · M 은 같은 합성 · 크기만 다르다 · ⚠ 체 눈 (20 µm) 위에 남은 쪽인데 d50 15.6 µm < 20 — 자름이 날카롭지 않다 (측정법 차이 가능 · [카드 해석]) | [인쇄] SI p.2 |
| 형상 (SEM 그림 1a–c) | 셋 다 **구형 2차 입자 덩이** (1차 결정립이 보이는 거친 표면) · L 에 큰 구 + 작은 위성 입자 · M 은 큰 구 + 작은 구 섞임 · S 는 ≈4 µm 덩이들 · 눈금 10 µm = 39 px (이 크롭) | [판독] 그림 1a–c |
| SE | **β-Li₃PS₄** — Li₂S 459.3 mg + P₂S₅ 740.6 mg · THF 35 mL ≥24 h 교반 · THF 세척 · 140 °C ≥12 h 동적 진공 (Liu 2013 [6]) · 순도 XRD (그림 S1 · Rwp 6.4 % · χ² 1.1 · Li₂S 불순물 상 분율 [미확인]) · 맨 SE σ **"approximately 0.2 mS/cm"** (p.3 · 측정 조건 [미확인]) · **SE 입경 · 형상 [미확인]** | [인쇄] SI p.2 · p.3 · 그림 S1 |
| 전자 차단 유리 | 1.5Li₂S·0.5P₂S₅·LiI 유리 (250 rpm 1 h + 450 rpm 15 h) · **1.3 mS/cm (375 MPa 냉간)** | [인쇄] SI p.2 |
| 복합 | **β-Li₃PS₄ : NCM622 = 3/7 w/w** (본문 *"milling a 7:3 weight mixture"* · *"This ratio was recently found to give the best performance"* [16, 17]) · 행성 밀 **140 rpm 30 min** · 10 mm ZrO₂ 볼 10 개 · 70 mL · 1 g · Ar · **탄소 · 결합제 없음** | [인쇄] p.2 · SI p.2 |
| 고체 중 AM 부피 | ≈**0.48** [카드 산술: (0.7/ρ_NCM)/(0.7/ρ_NCM + 0.3/ρ_SE) · ρ_NCM = **4.76 g cm⁻³** = 3 × 96.93 g mol⁻¹ / (N_A × 101.4 Å³) (Z = 3 · SI 표 S1 처음 분말 V 101.36–101.44 Å³ · 화학식량 = 명목 LiNi₀.₆Co₀.₂Mn₀.₂O₂) · ρ_SE = 1.85–1.90 가정 → 0.476–0.482] — **진밀도는 원문에 없다** | [카드 산술] |
| 같은 부피의 입자 수 | S 는 L 보다 (15.6/4.0)³ ≈ **59 배** · M 의 (8.3/4.0)³ ≈ 8.9 배 많다 [카드 산술 · 단분산 구 · d50 기준] | [카드 산술] |
| 반쪽 셀 | 셀 = 같은 그룹 장치 (SI [2] = Zhang 2017 JMCA) · 지름 [미확인] (In 원판 Ø 9 mm 가 들어간다) · β-Li₃PS₄ **60 mg ≈125 MPa → ≈400 µm** · 복합 **10–12 mg (≈90 µm · 1.9 mAh cm⁻²)** 를 **375 MPa** 로 붙임 · In 박 100 µm Ø 8 mm 를 **125 MPa** · 1 h 개회로 → C/10 (1C = 180 mA g⁻¹) · **3.8–2.3 V vs In/InLi (= 4.4–2.9 V vs Li⁺/Li)** · **55 MPa 유지** · 25 °C · MACCOR | [인쇄] p.2 · SI p.2 |
| ⚠ 대략값끼리 대조 | 면 용량 1.9 mAh cm⁻² ÷ 0.18 mAh mg⁻¹ ÷ 0.7 = 복합 15.1 mg cm⁻² · ÷ 0.0090 cm = 겉보기 밀도 **≈1.68 g cm⁻³** [카드 산술 · 가정: 로딩을 1C = 180 mAh g⁻¹ 로 셈 — 원문에 셈법 없음] = 이론 밀도 (≈3.23–3.28 g cm⁻³ · 위 가정) 의 **≈0.51–0.52** → 375 MPa 펠릿으로는 너무 낮다 · 또 분리막 60 mg ≈400 µm 를 지름 10 mm 에 넣으면 1.91 g cm⁻³ (β-Li₃PS₄ 진밀도 급 — 같은 꼴을 `koerver2018_…` 카드 L103 이 같은 그룹 셀에서 적었다 [다른 카드]) · 12 mm 면 반대로 면 용량이 1.1–1.3 mAh cm⁻² [카드 산술] ⇒ **원문 대략값 (≈90 µm · ≈400 µm · 10–12 mg · 1.9 mAh cm⁻²) 은 한 지름으로 서로 맞지 않는다 — 기공률 · 밀도를 이 숫자로 만들지 않는다** | [카드 산술] |
| ex situ XRD 셀 | 같은 꼴 · Specac 미니 펠릿 프레스로 **≈55 MPa** · C/10 → 3.8 V vs In/InLi (VMP3) · 첫 충전 뒤 *"disassembled without breaking the pellet apart"* · 복합 면을 위로 돔 셀 (Bruker) · Si 분말 내부 표준 | [인쇄] SI p.2 · SI p.4 |
| 액체 LIB 대조 | NCM 94 : Super C 4 : PVDF 2 wt% · NMP 슬러리 · Al 박 · 100 °C 24 h · **압연** · Ø 14 mm · 120 °C · CR2032 · GF/A · Li 600 µm · LP57 100 µL · 4.4–2.9 V vs Li · 같은 C/10 | [인쇄] SI p.3 |
| operando XRD 셀 | NCM-M/Li 파우치 (양극 20 × 40 mm² · Celgard 2500 · LP57 250 µL · 이슬점 < −50 °C 건조실) · Mo-Kα 회전 음극 · Pilatus 300K-W · 5–37° · *"every 75 s"* · C/10 · 4.4–2.9 V · TOPAS 5 | [인쇄] SI p.3–4 |

### 3-2. ★ 전기화학 — 첫 사이클 · 저율 · 액체 대조 (p.2 · 그림 1d · 1e · 2 · SI 그림 S2 · `fig_1d.png` · `fig_1e.png` · `fig_2a/2b/2c.png` · `fig_S2.png` · `txt_p2_first_cycle_162_84_ce_polarization.png` · `txt_p2_chemomech_contact_c30_c50.png`)
- **고체 셀 C/10 첫 사이클 [인쇄 p.2]**: 첫 충전 **162 (S) · 95 (M) · 84 (L) mAh g⁻¹** · 첫 CE **70 · 55 · 50 %** · 분극 *"increases by 100 to 200 mV with charge and discharge relative to LIB half-cells"*.
- **같은 그림 판독 [digitized.csv fig1e · 래스터 300 dpi · x 눈금 0–200 = 열 786.5–1308.5 px · y 눈금 3.6–2.4 V = 행 479.5–705 px]**: 충전 끝 (3.8 V) **S 161.1 · M 94.1 · L 83.0** · 방전 끝 (2.3 V) **S 109.8 · M 55.7 · L 42.3 mAh g⁻¹** → CE [카드 산술] **0.68 · 0.59 · 0.51** — S · L 은 본문과 맞고 **M 은 본문 55 % 보다 4 %p 높다** (그림 2b 의 C/10 실선 끝점도 94.0 / 55.5 로 같다 · 판독 오차 ±1 mAh g⁻¹ ≈ CE ±0.012).
- **액체 LIB C/10 [인쇄 p.2]**: *"specific charge capacity being around 200 mAh/g and approximately 10% capacity loss in the first cycle … negligible differences between the large, medium, and small NCM622"* · [판독 그림 1d] 충전 S 212.8 · M 210.0 · **L 234.4** · 방전 S 190.8 · M 188.4 · L 194.2 → CE 0.90 · 0.90 · **0.83** [카드 산술] — 방전은 셋이 같고, **L 의 충전만 ≈22 mAh g⁻¹ 크다** (원문 언급 없음).
- **저율 [인쇄 p.2]**: C/30 에서 NCM-S *"almost full charge capacity (approximately 190 mAh/g)"* · M **120** · L **100** · C/50 에서 L *"only marginally from 100 to 110"* → 저자: S 는 **느린 반응** (저율로 회복), M · L 은 *"poor kinetics is not the only issue"* (저율로도 회복 안 됨) → 일부 입자가 비활성.
  [판독 그림 2 · x 눈금 0–200 = 열 97.5–560.5 px]: C/30 충전 / 방전 **S 193.3 / 152.3 · M 118.1 / 80.6 · L 97.8 / 60.7** · C/50 **L 112.5 / 65.4** → CE 0.79 · 0.68 · 0.62 · 0.58 [카드 산술] (⚠ 그림 2c 의 두 점선은 범례로 갈리지 않는다 — 큰 쪽을 본문대로 C/50 으로 읽었다 [카드 해석]).
- **dQ/dU (그림 S2 · 판독 · V vs In/InLi · 액체 셀은 −0.6 V 로 옮겨 그림)**: 충전 봉우리 **S 3.22 · M 3.23 · L 3.31 V** ↔ 액체 NCM-M 3.10 V (+0.12 · +0.13 · +0.21 V) · 방전 봉우리 **S 3.01 · M 3.00 · L 2.93 V** ↔ 액체 3.12 V (−0.11 · −0.12 · −0.19 V) [카드 산술] — 본문 '100–200 mV' 와 같은 크기 · 크기가 클수록 분극이 크다.
- **저자 해석 (p.2)**: 낮은 CE 는 *"most likely associated with different chemo-mechanical effects during cycling operation (note that the volume contraction during charging leads to a reduced electrical contact between the CAM particles and the SE)"* [9, 18] + 코팅 없는 NCM 의 SE 산화 분해 → 절연 층 → 과전압 → 충전이 낮은 SOC 에서 끊긴다 [9].  **측정은 없다** (인용 기반 설명).

### 3-3. ★ ex situ XRD — 비활성 CAM · 격자 · SOC (p.2–3 · SI p.4 · 그림 3 · SI 그림 S3–S5 · SI 표 S1 · `fig_3a.png` · `fig_3b.png` · `tab_S1.png` · `fig_S5a/S5b.png` · `txt_p3_lattice_volume_inactive_2_27_31.png` · `txt_p3_capacity_90_92_153_ionic_1e6.png` · `txt_SIp4_rietveld_xli_053_056_046_error.png`)
- **방법 [인쇄 SI p.4]**: D8 ADVANCE (Cu-Kα · Ni 필터 · LynxEye) · 10–90° · 0.01° · 2.3 s 걸음 · 충전 뒤 펠릿을 그대로 · Si 내부 표준 (시료 높이 보정 · Si 영역 28.5 · 47 · 56 · 69.5 · 76.5 · 88° 제외) · FullProf · 배경 Chebyshev 24 · 고정 등방 변위 · **활성 · 비활성 두 NCM 상을 동시에 맞춤** · 자리 점유 = 명목.
- **두 상 판정 [인쇄 p.3]**: 003 봉우리가 갈라짐 = *"two NCM species with a different lithium content"* · 하나는 부분 탈리튬 (SOC > 0 · 활성) · 하나는 처음 그대로 (SOC = 0 · 비활성) — 액체 셀 operando 의 a · c (x(Li)) 곡선 (그림 3b) 과 대조.
- **SI 표 S1 [인쇄]** (a · c Å · V Å³ · 분율 % · z):

| 시료 | 상태 | a | c | V | 분율 | z |
|---|---|---|---|---|---|---|
| NCM-S | 충전 | 2.817(1) | 14.501(1) | 99.68(1) | **98(1)** | 0.2483(4) |
| | 비활성 | 2.869(1) | 14.227(4) | 101.43(5) | **2(1)** | 0.258(9) |
| | 처음 | 2.869(1) | 14.221(1) | 101.38(1) | | 0.2596(1) |
| NCM-M | 충전 | 2.823(1) | 14.486(1) | 100.00(1) | **73(1)** | 0.2471(4) |
| | 비활성 | 2.868(1) | 14.229(1) | 101.34(1) | **27(1)** | 0.2517(8) |
| | 처음 | 2.868(1) | 14.225(1) | 101.36(1) | | 0.2576(2) |
| NCM-L | 충전 | 2.823(1) | 14.509(1) | 100.10(1) | **69(1)** | 0.2473(5) |
| | 비활성 | 2.872(1) | 14.240(1) | 101.73(1) | **31(1)** | 0.2539(8) |
| | 처음 | 2.870(1) | 14.220(1) | 101.44(1) | | 0.2553(2) |

- **Rietveld 맞춤 질 (그림 S5 안 글자) [인쇄]**: 처음 분말 Rwp **2.1 · 2.0 · 1.6 %** (L · M · S) · χ² 1.4 · 1.4 · 1.7 / 충전 복합 Rwp **3.8 · 3.0 · 3.2 %** · χ² 1.5 · 1.6 · 1.5.
- **활성 상 x(Li) [인쇄 SI p.4]**: **0.53 (L) · 0.56 (M) · 0.46 (S)** (operando 비교 · a · c 평균 · *"about ±0.02"*) · [판독 그림 3b 십자] S: c 0.468 · a 0.443 · M: c 0.571 · a 0.552 · L: c 0.507 · a 0.542 → 평균 0.456 · 0.562 · 0.525 (인쇄와 같다).  ⚠ c 는 x(Li) ≈0.5 근처에서 최대라 (본문 p.3) 충전 시료의 c (14.49–14.51 Å) 가 거의 꼭지에 있다 — c 쪽 x 읽기가 둔하다 [카드 해석].
- **오차 [인쇄 SI p.4]**: 고정 Li 점유로 다시 맞추면 상 분율이 **−3 % (L · M) · −11 % (S)** 바뀐다 · S 가 큰 까닭 = *"the detection limit of inactive cathode active material by XRD"* · 부반응 (SE 분해) 용량은 해석에 없다.
- **SOC 로 낸 용량 [인쇄 p.3]**: *"capacities of 90, 92, and 153 mAh/g are obtained for NCM-L, NCM-M, and NCM-S"* — *"close to those obtained from the electrochemical data"* (84 · 95 · 162).  [카드 산술 · 이론 용량 276.5 mAh g⁻¹ = F/(3.6 × 96.93) · 1 Li · 원문에 식 · 이론 용량 없음]: 활성 분율 × (1 − x) × 276.5 = **L 89.7 · M 88.8 · S 146.3** (평균 x 판독값이면 90.7 · 88.5 · 147.5) — L 은 맞고 **M · S 는 인쇄값보다 ≈4 % 낮다** (x ±0.02 · 과리튬 Li₁₊ₓ 를 어떻게 셌는지 원문에 없음).
- **충전 뒤 격자 변화 [카드 산술 · 표 S1 충전 ↔ 처음]**: V **−1.68 (S) · −1.34 (M) · −1.32 % (L)** · a −1.81 · −1.57 · −1.64 % · c +1.97 · +1.83 · +2.03 % (이방성 — a 수축 · c 팽창) · 비활성 상 V 는 처음 분말과 +0.05 · −0.02 · **+0.29 % (L)**.
- **operando 보정곡선 (그림 3b · S4 · 액체 NCM-M/Li 파우치)**: a 는 x(Li) 와 거의 직선으로 줄고 c 는 x ≈0.5 까지 늘다 크게 준다 → 단위 격자 부피 감소 (p.3) · [판독 그림 S4] V **101.32 (x 1.0) → 99.87 (0.5) → 98.05 Å³ (≈0.31)** = −1.43 · **−3.2 %** [카드 산술].

### 3-4. ★ 부분 전도도 — 이온 · 전자 (p.3–4 · 그림 4 · SI p.3 · SI 그림 S6 · `fig_4.png` · `fig_S6a/S6b.png` · `txt_p3_capacity_90_92_153_ionic_1e6.png` · `txt_p4_electronic_3_orders_percolation_segregation.png` · `txt_SIp3_lib_pouch_dc_polarization.png` · `eq_S01_ohm_law_steady_state_current.png` · `eq_S02_conductivity_sigma_RA_over_l.png`)
- **측정 [인쇄 SI p.3]**: 반쪽 셀과 같은 장치 · **55 MPa 유지한 채** · 실온 ·
  - 전자 (이온 차단): 복합 ≈100 mg 를 **375 MPa 2 min** (SS 플런저 둘 사이) → 1 h 휴지 → **300 mV** 정전위 → 전류 응답.
  - 이온 (전자 차단): 복합 ≈100 mg **250 MPa** → 양쪽에 1.5Li₂S·0.5P₂S₅·LiI 유리 100 mg 씩 **250 MPa** → Ø 9 mm In · Ø 6 mm Li 원판 (Li 저장) → 전체 **375 MPa 2 min** → 6 h 휴지 → **300 mV**.
  - 저항: *"Ohm's law (R = U/I), where the current I was obtained by linear fitting of the steady state region"* · 전도도: *"σ = (R×A)/l (R, A, and l represent the resistance, area, and thickness)"* — ⚠ **인쇄된 식은 거꾸로다**: R·A/l 은 저항률 (Ω cm) 이고 전도도는 **σ = l/(R·A)** [카드 해석 · 차원] · 시편 두께 · 면적 · 유리 층 저항 빼기 [미확인].
- **그림 4 [인쇄 본문]**: 이온 *"not affected by the NCM622 particle size, being around 10⁻⁶ S/cm and thus roughly 2 orders of magnitude lower than for bare β-Li₃PS₄ (approximately 0.2 mS/cm)"* · 전자 *"decreases by 3 orders of magnitude from about 10⁻³ for NCM-S to 10⁻⁶ S/cm for NCM-L"*.
- **그림 4 판독 [digitized.csv fig4 · 래스터 xref 127 · 왼축 10⁻³ … 10⁻⁸ = 행 11.5 … 286.5 px (55.0 px/자릿수) · 오른축 10⁻³ … 10⁻⁶ = 행 27.0 … 294.5 px (89.2 px/자릿수) · 표지 중심 ±1 px = ±0.02 · ±0.01 자릿수]**:

| | NCM-S | NCM-M | NCM-L |
|---|---|---|---|
| σ_ion (채운 원 · 왼축) S cm⁻¹ | **1.29 × 10⁻⁶** | **6.7 × 10⁻⁷** | **8.8 × 10⁻⁷** |
| σ_e (빈 원 · 오른축) S cm⁻¹ | **8.8 × 10⁻⁴** | **3.8 × 10⁻⁵** | **1.4 × 10⁻⁶** |
| σ_e / σ_ion [카드 산술] | 680 | 57 | 1.6 |
| f_ion = σ_ion / 0.2 mS cm⁻¹ [카드 산술] | 0.0064 | 0.0034 | 0.0044 |

  ⚠ **두 축의 자릿수 간격이 다르다** (왼쪽 5 자릿수 · 오른쪽 ≈3.2 자릿수가 같은 높이) — 같은 높이의 표지끼리 견주면 틀린다 (그림의 화살표가 축을 가리킨다).  S→L 전자 σ 는 log₁₀(8.8 × 10⁻⁴ / 1.4 × 10⁻⁶) = **2.8 자릿수** (본문 '3').
- **이온 f 의 크기 [카드 산술 · 다른 카드]**: f ≈0.003–0.006 은 `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` 카드의 NMC111 + Li₃PS₄ 유리 (NMC 48–62 vol%) f **0.055–0.125** [다른 카드] 보다 **≈9–37 배 낮다** — SE (β-Li₃PS₄ 습식 ↔ 유리) · 혼합 (볼밀) · 기공 [미확인] · 맨 SE σ₀ 측정 조건 [미확인] 이 달라 원인을 가를 수 없다.  tau2 = φ_SE/f 의 **상한** (기공 0 · φ_SE ≤ 0.52) = 81 · 155 · 118 [카드 산술] — 숫자가 큰 만큼 '복합체 안 SE 망 + 측정 계면' 의 값으로만 읽는다.
- **그림 S6 (대표 곡선 · 어느 시료인지 [미확인])** [판독]: (a) 이온 차단 0.127 mA (0.02 h) → **0.1216 mA (2–2.5 h · 평탄)** → R ≈ **2.47 kΩ** · (b) 전자 차단 0.0255 (5 h) → 0.0118 (20 h) → **0.0048 mA (60 h · 아직 줄어듦)** → R ≈ **62.5 kΩ** [카드 산술 · 300 mV ÷ I] — (b) 는 60 h 에도 완전히 평탄하지 않다.
- **저자 결론 [인쇄 p.4]**: S 는 *"slow ionic transport through the electrode composite is the major issue"* · M · L 은 *"not all of the particles are electronically connected, which is why they cannot be addressed electrochemically. This is in agreement with percolation theory, predicting that composites made of small particles offer many more contact points between them than those consisting of relatively large (spherical) particles, thereby providing sufficient pathways for electron conduction"* [26] · 건식 분말 혼합의 성분 분리 가능성은 단면 SEM + S EDX (그림 S7) 로 *"do not reveal major inhomogeneities"* → σ_e 차이는 *"mainly result from the different average particle size"*.

### 3-5. 단면 SEM · EDX (SI 그림 S7 · `fig_S7abc.png` · `fig_S7def.png`)
- 충전 전 복합체 단면 (LEO-1530 · 10 keV) + S EDX (L a · d · M b · e · S c · f) · 눈금 20 µm (= 51 px 이 크롭 [판독]).
- 저자: *"do not reveal major inhomogeneities"* (p.4) — 정량 없음.
- [카드 해석 · 그림만 본 것]: (a) L 은 큰 구 둘레에 어두운 초승달 틈이 보이고 (b) M 은 위 · 아래 층 사이 틈 띠 · (c) S 는 고른 층에 가로 금 — **원문은 틈 · 금에 대해 말하지 않는다** (시편 준비 흔적인지 [미확인]).
- [판독 · 거칢] (c) 의 위 표면 ↔ 질감이 바뀌는 경계 ≈384 px ≈ **150 µm** — SI p.2 의 *"approx. 90 µm"* (10–12 mg 셀) 와 다르다 · 같은 종류 시편인지 · 경계가 복합 / 분리막인지 원문에 없다 → **두께 근거로 쓰지 않는다**.

### 3-6. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① CE 차이 원인 *"not yet fully understood"* (p.2) ② 건식 분말 혼합의 성분 분리 가능 (p.4) ③ XRD 해석에 부반응 용량 미포함 · NCM-S 비활성 분율은 검출 한계 근처 (SI p.4) ④ 그림 S6 은 *"Representative"* 곡선 (시료 [미확인]).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. **σ 식이 거꾸로** — SI p.3 *"σ = (R×A)/l"* = 저항률 · 전도도는 l/(R·A) (`eq_S02_conductivity_sigma_RA_over_l.png`).
2. **operando XRD 간격** — SI p.4 *"every 75 s"* ↔ 그림 S3 의 두 축 눈금이 **같은 높이에서 0/5/10/15/20 h = 0/100/200/300/400 번째 측정** → **180 s / 측정** [판독 · 눈금 행 513.5 · 414 · 315.5 · 217 · 119 px 가 양쪽에서 같다].
3. **NCM-M 첫 CE** — 본문 55 % ↔ 그림 1e (와 2b) 끝점 비 **0.59** [판독].
4. **SOC 용량** — 인쇄 92 (M) · 153 (S) ↔ 활성 분율 × (1 − x) × 이론 용량 88.8 · 146–148 [카드 산술 · 이론 용량 · 식은 원문에 없음] (x ±0.02 안이면 맞출 수 있다).
5. **액체 대조** — 본문 *"negligible differences"* · *"around 200 mAh/g"* ↔ 그림 1d 충전 L **234** · M 210 · S 213 [판독] (방전은 셋이 같다).
6. **대략값 대조** — ≈90 µm · 10–12 mg · 1.9 mAh cm⁻² · 분리막 60 mg ≈400 µm 가 한 셀 지름으로 서로 맞지 않는다 (§3-1 · 겉보기 밀도 ≈1.68 g cm⁻³) · 단면 SEM 은 ≈150 µm [판독 · 거칢].
7. **체 자름** — *"20 µm sieve … remaining fraction"* ↔ NCM-L d50 15.6 µm (< 20).
8. 표기: NCM-L *"d₉₀ = 26.1"* 단위 빠짐 · 그림 2c 의 두 점선 (C/30 · C/50) 범례 없음 · 그림 S2 캡션 *"the curve from on a liquid"* · 그림 4 두 축 자릿수 간격 다름 · 본문 전체에 압력 · 두께 · 질량 숫자 0 (전부 SI).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **시편 셋**: (가) 반쪽 셀 (복합 10–12 mg · 375 MPa · 55 MPa 운전) → 정전류 / (나) ex situ XRD 용 같은 셀 (≈55 MPa 에서 첫 충전 → 분해 → 펠릿 그대로 XRD) / (다) DC 분극 펠릿 (복합 ≈100 mg · 375 MPa 2 min · 이온 쪽은 유리 층 · 55 MPa 측정).  ⚠ **σ 는 SOC 0 (충전 전)** 에서, 비활성 분율은 **첫 충전 뒤** 에서 잰 것 — 두 결과를 이은 것은 저자의 해석.
- **비활성 CAM**: XRD 003 두 상 Rietveld → 상 분율 = 비활성 분율 · 활성 상 격자 → x(Li) (액체 셀 operando 보정).
- **SOC → 용량**: 활성 분율 × 활성 상 SOC → 질량 용량 (식 미인쇄).
- **부분 전도도**: 300 mV 정전위 정상 전류 → R = U/I → σ.
- **대조군**: 같은 세 분말의 액체 LIB (탄소 4 % · 압연) — 크기 효과가 고체 복합체에서만 나타나는지 보는 장치.

### 4-2. 입자 처리 ★
- 실험: AM = **구형 다결정 2차 입자** (SEM) · 크기 = d50 / d90 (측정법 [미확인]) · SE = 습식 β-Li₃PS₄ (입경 · 형상 [미확인]).
- 해석의 그림: 전자 경로 = **AM 입자끼리의 접점망** (탄소 없음) · *"small particles offer many more contact points … than … relatively large (spherical) particles"* (p.4) — DEM 접촉망이 세는 바로 그 양 (접점 수) 을 말로 쓴 것.  계산은 없다.
- DEM · 연속체 · 입자 형상 변화 · 소성 **다루지 않음**.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · SI 에 DEM · discrete · simulation 낱말 0 회).  관련 문장은 반대 방향 하나: percolation 이론으로 *"composites made of small particles offer many more contact points between them than those consisting of relatively large (spherical) particles"* (p.4 · [26] SOFC) — 접점 수로 전자 망을 설명 (DEM 접촉망과 같은 그림).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음** (plastic · elastic · deform 0 회).  역학 문장은 둘뿐: 황화물 SE 의 *"favorable mechanical properties … allow good processability as well as high conductivity, even when cold pressed"* (p.1 · [4–6]) · 충전 중 *"volume contraction … leads to a reduced electrical contact"* (p.2 · [9, 18] · 측정 아님).
3. **2D / 3D** — 계산 없음 · 2D → 3D 진술 없음 (SEM 단면은 2D 그림).
4. **압력을 뺄 때의 거동** — **다루지 않았다**: 모든 측정이 375 MPa 성형 뒤 **55 MPa 로 낮춘 상태** (부분 탈압 · 누른 채) 에서 이뤄졌고 그 사이 되돌아옴 · 두께 변화는 없다 · ex situ XRD 시편은 분해 (압력 0) 뒤 재었다.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 2차 입자 (secondary particle) | 작은 1차 결정립이 뭉친 다결정 구 — 이 논문의 '입경' 은 그 지름 (d50 · d90) |
| 비활성 CAM (inactive) | 첫 충전 뒤에도 처음 격자 그대로인 NCM 상 (SOC = 0) — XRD 두 상 분율로 센다 |
| 두 상 Rietveld | 같은 NCM 구조를 격자만 다른 두 상으로 동시에 맞춰 분율 · 격자를 얻음 |
| operando 보정곡선 | 액체 셀에서 충전하며 잰 a · c vs x(Li) — 고체 셀 충전 시료의 x(Li) 를 그 곡선에서 읽음 |
| DC 분극 (이온 / 전자 차단) | 한 종류 전하만 통하는 전극 사이에 정전위 → 정상 전류 → 그 종류의 부분 전도도 |
| 이온 차단 전극 | SS 플런저 — 전자만 통함 → 전자 σ |
| 전자 차단 전극 | Li 이온 전도 유리 (1.3 mS/cm) 층 + Li/In 저장 원판 — 이온만 통함 → 이온 σ |
| percolation | 도체 입자가 끊기지 않고 전극을 가로지르는 망을 이루는가 — 이 논문은 '접점 수' 로 설명 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **그래픽 초록** (`fig_toc_graphical_abstract.png`) | 복합 양극 블록 (검은 구 = CAM · 분리막 · 집전판) 에 X 선 · 검출기 — 숫자 없음 | 없음 (그림 안내만) |
| **Fig. 1** (`fig_1.png` · 패널 `fig_1abc` · `1d` · `1e`) | (a–c) SEM: L · M · S 분말 (눈금 10 µm) · (d) 액체 LIB 첫 사이클 · (e) 고체 셀 첫 사이클 (화살표 = 작을수록 용량 ↑) | ★ (e) 162 · 95 · 84 / 방전 110 · 56 · 42 [판독] · (d) 액체 대조 = 크기 차 없음 → '고체 복합체의 망 효과' 를 가르는 대조 설계 |
| **Fig. 2** (`fig_2.png` · `fig_2a/2b/2c`) | 각 크기의 C/10 (실선) · C/30 (점선) · L 만 C/50 | S 는 저율로 ≈193 (느린 반응) · L 은 C/50 에도 ≈113 (비활성) [판독] |
| **Fig. 3** (`fig_3.png` · `fig_3a` · `3b`) | (a) 충전 복합체 003 두 상 맞춤 (31 · 27 · 2 %) · (b) a · c vs x(Li) 보정곡선 + 십자 | ★ 전자 고립 AM 을 실측으로 세는 법 — 우리 망의 고립 AM 지표와 결과 전 대조 |
| **Fig. 4** (`fig_4.png`) | 이온 (채운 원 · 왼축) · 전자 (빈 원 · 오른축) 부분 전도도 × 세 크기 | ★ 탄소 없는 복합체 σ_e vs AM 크기 (2.8 자릿수) · σ_ion 크기 무관 [판독] |
| **SI Fig. S1** (`fig_S1.png`) | β-Li₃PS₄ Rietveld (Rwp 6.4 % · χ² 1.1 · Li₂S 불순물) | SE 순도만 |
| **SI Fig. S2** (`fig_S2.png`) | dQ/dU 첫 사이클 (세 크기 + 액체) | 분극 +0.12 … +0.21 V [판독] |
| **SI Fig. S3** (`fig_S3.png`) | 액체 파우치 operando XRD 등고선 + 전압 | 측정 간격 판독 함정 (75 s ↔ 축 180 s) |
| **SI Fig. S4** (`fig_S4.png`) | 단위 격자 부피 vs x(Li) (액체) | NCM622 부피 변화 −1.4 % (x 0.5) · −3.2 % (≈0.31) [판독] — 화학–역학 입력의 크기 감각 |
| **SI Fig. S5** (`fig_S5.png` · `fig_S5a` · `S5b`) | Rietveld: 처음 분말 · 충전 복합체 | 맞춤 질 (Rwp 1.6–3.8 %) |
| **SI Fig. S6** (`fig_S6.png` · `fig_S6a` · `S6b`) | DC 분극 대표 전류 (이온 차단 · 전자 차단) + 셀 그림 | 측정 배치 그림 · (b) 60 h 에도 덜 평탄 |
| **SI Fig. S7** (`fig_S7.png` · `fig_S7abc` · `S7def`) | 단면 SEM + S EDX (세 크기) | 성분 분리 없음 (저자) · 틈 · 금 (원문 언급 없음) |
| **SI Table S1** (`tab_S1.png`) | 충전 · 비활성 · 처음 상의 a · c · V · 분율 · z | ★ 비활성 2 · 27 · 31 % · 충전 V −1.3 … −1.7 % |
| 식 크롭 2 (`eq_S01` · `eq_S02`) · 근거 문단 14 (`txt_p*` · `txt_SIp*`) | R = U/I · σ = (R×A)/l (인쇄 그대로) · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **용량 · CE**: 첫 사이클 충 · 방전 끝 (질량 = CAM 기준 mAh g⁻¹_CAM).
- **분극**: dQ/dU 봉우리 위치를 액체 셀 (−0.6 V 옮김) 과 견줌.
- **비활성 분율**: FullProf 두 상 Rietveld 의 상 분율 (±1 %) · 고정 Li 점유 재맞춤으로 오차 (−3 · −11 %).
- **SOC**: 액체 셀 operando a · c (x) 곡선에서 a · c 각각으로 x 를 읽어 평균 (차이 = 그림 3b 띠).
- **전도도**: 300 mV 정상 영역 선형 맞춤 → R = U/I → σ (식 인쇄 오류 · 두께 · 면적 미인쇄).
- **판독 (이 카드)**: 본문 래스터를 그대로 꺼내 (300 dpi) 눈금 위치 · 색 분리 · 성분 중심 · 색 띠 끝점 — digitized.csv note 열에 방법 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 측정 상태 · 조성이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 탄소 없는 복합체 전자 σ vs AM 크기 | 7 : 3 wt NCM622 : β-Li₃PS₄ · d50 4.0 / 8.3 / 15.6 µm → **8.8 × 10⁻⁴ / 3.8 × 10⁻⁵ / 1.4 × 10⁻⁶ S cm⁻¹** [판독] (375 MPa → 55 MPa · SOC 0 · DC) | DEM 접촉망 σ_e = **AM–AM 접점망만 (탄소는 DEM 에 없다)** · ps45 다섯 조성 σ_e (PC 크기 인자 끔 · 공통 σ_AM 4.1 mS cm⁻¹) **0.375–0.467 mS cm⁻¹** [우리 · CLAUDE.md 10-13] · Stage 22.5 폼의 크기 항 = NCM(r) GB 계수 (Trevisanello) + √A_AM-AM + (T/d_AM)^β_T [우리] | **같은 '탄소 없는 AM 망' 꼴** — 이 논문은 우리 DEM σ_e 의 실험 쪽 짝이다 · NCM-S 0.88 mS cm⁻¹ 와 자릿수가 같다 (조건 · 재료 · 조성이 달라 값 대조 아님) · ★ **크기 의존의 기전이 다르다**: 이 논문 = 망 연결 (접점 수 · 고립 입자) · 우리 폼의 NCM(r) = 입자 안 입계 |
| 전자 고립 AM | 비활성 CAM **2 / 27 / 31 %** (첫 충전 뒤 · XRD) | 망 지표: 전자 활성 분율 · AM 고립 비율 (am_*_isolated) [우리] | **결과 전 대조 (방향)** — 같은 조성에서 AM 크기만 키우면 고립 AM ↑ 를 우리 망이 내는가 |
| 이온 σ (복합) | ≈1 × 10⁻⁶ S cm⁻¹ · 크기 무관 · f ≈0.003–0.006 (맨 SE 0.2 mS cm⁻¹ 기준) | ps45 Hertz σ_ion **0.0587–0.0893 mS cm⁻¹** (σ₀ 1.5 → f ≈0.04–0.06) · 수송 tortuosity 5.03–7.24 [우리 · CLAUDE.md 10-13] | f 가 **≈10 배 낮다** — SE (β-Li₃PS₄ ↔ LPSCl) · SE 입경 · 기공 [미확인] · 측정 계면 → 값 대조 불가 · 방향 (AM 크기 무관) 만 |
| AM 형상 | 구형 다결정 2차 입자 (SEM) | DEM 구 | **같은 가정이 이 계에선 그럴듯** — SE 형상은 [미확인] |
| 성형 · 상태 | 375 MPa 성형 → 55 MPa 측정 (부분 탈압 · 누른 채) | DEM 300 MPa 누른 채 / 판 고정 이완 [우리] | 상태가 다르다 — 우리 DEM 에 '55 MPa 로 낮춘 상태' 단계 없음 |
| CAM 부피 변화 (충전) | NCM622 V −1.32 … −1.68 % (x 0.46–0.56) · a −1.6 … −1.8 % · c +1.8 … +2.0 % [카드 산술] · 액체 S4 −3.2 % (x ≈0.31) [판독] | 사이클 접촉 원장 (A10 · Bucci CZM · AM 수축 → 접촉 개구) [우리 · CLAUDE.md] | 입력 크기 감각 (NCM622 · 이방) — 우리 NCM811 은 다른 값 |
| PC / SC | 세 크기 모두 **PC** | 모델 라벨: 작은 AM (AM_S) = 단결정 · σ_S 10 / σ_P 5 mS cm⁻¹ (코퍼스 끝점 · Trevisanello 는 방향만) [우리 · CLAUDE.md] | **이 논문은 그 라벨의 근거가 아니다** — 작은 PC 도 망 연결로 σ_e 가 크게 오른다 |

### 7-2. ★ 크기 → 전자 σ 의 부호 (우리 폼과의 긴장)
- 정본 `shi2019_…` 카드 L570 은 우리 Stage 22.5 폼을 *"σ_e ∝ φ_AM⁴·√A_AM-AM·NCM(r) — 큰 AM 은 AM-AM 접촉수·면적↑ → σ_e↑"* 로 적고, L571 이 그것을 Shi 의 반대 진술 (탄소 없으면 작은 CAM 유리 · ref [13] = 이 논문) 로 정정했다 [다른 카드].  이 논문은 그 정정의 **실측 원전**이다: 같은 7 : 3 wt · 탄소 없음 · 크기만 바꿨을 때 작은 쪽이 σ_e **≈2.8 자릿수 높다**.
- ⇒ 우리 σ_e 폼의 크기 항 부호는 **코퍼스 적합의 결과** (shi2019 카드 L571) 이고 이 실측과 견줘 본 적이 없다 — 우리 폼 · DEM 망에 같은 조건 (φ_AM ≈0.48 고체 기준 · AM 단분산 4 / 8 / 16 µm · SE 크기 고정) 을 넣어 **방향과 대략의 크기**를 결과 전 대조로 둔다 (§8 단계 7 · D0).  ⚠ 이 카드는 우리 폼의 순 크기 방향을 계산하지 않았다.
- [카드 해석 · 구 망 산술]: 끊김 없이 이어진 구 망에서 접촉 반지름이 입자 크기에 비례하면 (같은 변형률) 접점당 컨덕턴스 ∝ R · 단면당 접점 수 ∝ R⁻² · 길이당 접점 수 ∝ R⁻¹ → σ_eff 는 크기와 **무관**하다.  그러니 2.8 자릿수의 차이는 **연결성 (고립 입자 · 끊긴 경로) 에서만** 나올 수 있다 — 우리 DEM 이 φ_AM ≈0.5 근처에서 그 percolation 변화를 내는지가 판별 시험이다.

### 7-3. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **수송 쪽 (DEM 소관) 의 실험** — 접점망 연결 (전자 percolation) · 고립 AM · 부분 전도도.  압밀 · 소성 · 형상 (MPM 소관) 은 없다.
- 없는 반쪽: 기공 · 밀도 · 압력별 구조 · 탈압 · 입자 변형 · SE 입경 — 그래서 우리 DEM 과는 **방향 대조**만 된다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NCM622 (코팅 없음) + β-Li₃PS₄ — **랩 표준과 다른 문헌 계** · 기공 · 밀도 값 없음.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 — ① 원문의 **대략값 넷 (≈90 µm · 10–12 mg · 1.9 mAh cm⁻² · 60 mg ≈400 µm) 이 한 셀 지름으로 서로 맞지 않는다** (겉보기 밀도 ≈1.68 g cm⁻³ = 이론의 ≈0.5 [카드 산술]) → 결과 전 대조 항목에는 질량 · 면적 · 두께 · 성형압 · 측정압을 **실측값으로** 함께 등록해야 밀도 · 기공을 다시 만들 수 있다 ② **본문에 압력이 하나도 없다** (전부 SI) — 인용할 때 SI 까지 본다 | 기공 · 진밀도 · 압력별 값 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: 같은 AM 부피에서 d50 4.0 µm 는 15.6 µm 보다 입자 **≈59 배** [카드 산술] — AM 을 작게 하면 DEM 입자 수가 그만큼 는다 | 메모리 숫자 없음 |
| **단계 2 · 3** (2D MPM 코드 · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 — 맨 β-Li₃PS₄ σ ≈0.2 mS cm⁻¹ · 유리 1.3 mS cm⁻¹ (375 MPa) 뿐 · 기공 없음 | 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | 조성 (7 : 3 wt · 고체 중 AM ≈0.48 [카드 산술]) · 성형 375 MPa · AM 크기 세 단계 — 압밀 결과는 없음 | 기공 · AM 하중 몫 · 압력별 곡선 없음 |
| **단계 6** (탈압 · 되돌아옴) | 측정 상태가 **375 MPa → 55 MPa 로 낮춘 상태** 라는 사실 — 우리 탈압 계산이 '운전압 (수십 MPa) 으로 낮춘 상태' 의 망을 낼 때의 실험 쪽 조건 예 | 되돌아옴 · 두께 변화 · 탈압 전후 σ 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★★ **결과 전 대조 항목 셋**: ① 탄소 없는 복합 σ_e vs AM d50 (4.0 → 15.6 µm) **8.8 × 10⁻⁴ → 1.4 × 10⁻⁶ S cm⁻¹ (2.8 자릿수)** [판독] ② 전자 고립 (비활성) AM **2 → 27 → 31 %** [인쇄] ③ σ_ion **AM 크기 무관 ≈10⁻⁶** [판독] — 우리 DEM 접촉망 σ_e · 고립 AM 지표 · 이온 망이 같은 방향을 내는지 | σ_e 를 SOC 0 에서만 · 비활성은 첫 충전 뒤 한 번 · SE 크기 [미확인] · NCM622 · β-Li₃PS₄ |
| **후보 D0** (지금 DEM) | ★ **우리 DEM σ_e 의 실험 짝** (DEM 에는 탄소가 없다 = '탄소 없는 복합체') · AM 구 가정이 이 계 (구형 2차 입자) 에 맞는다 · 접점 수 → 전자 망이라는 해석 (p.4) 이 DEM 접촉망과 같은 그림 · §7-2 의 부호 시험 | DEM 연화 (E_eff 1.35) · 겹침이 접점 면적을 정하는 방식과 비교할 접점 면적 · 힘 자료 없음 |
| **후보 A′-0 · A · A′** (MPM 접촉 규칙 · 강체 AM · 입자별 속도장) | 없음 — 역학 자료 없음 | — |
| **후보 B · C · C′ · M0** | 없음 | — |
| **U0–U6** | 없음 | — |
| **R1–R7** | **R2** (미끄럼 · 분리): 충전 수축이 CAM–SE 전기 접촉을 줄인다는 인용 설명 (측정 아님) + 충전 V −1.3 … −1.7 % · a −1.6 … −1.8 % · c +1.8 … +2.0 % [카드 산술] · **R4** (탈압): 55 MPa 로 낮춘 상태의 측정 (회복 자료 없음) · **R7** (AM 파괴): 없음 (이방 격자 변화는 다결정 입계 응력의 입력 감각뿐 · 균열 관찰 없음) | R1 · R3 · R5 · R6 없음 |
| **결과 전 대조 항목** | 위 단계 7 의 셋 + ④ 액체 LIB 같은 분말 = 크기 차 없음 (방전 188–194 mAh g⁻¹ [판독]) → '크기 효과 = 고체 복합체 망' 의 대조 | 우리 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: NCM622 (코팅 없음) ↔ 우리 NCM811 · β-Li₃PS₄ (습식 · 입경 [미확인]) ↔ 우리 LPSCl · 7 : 3 wt (탄소 없음) ↔ 우리 코퍼스 핵심 (AM 70–85 wt% · 탄소는 STEP3 복셀에만) · 375 → 55 MPa ↔ 우리 300 MPa · 3D 실물 · 25 °C · SOC 0 의 σ.

## 9. 적용 인사이트 (행동)
1. **결과 전 대조 항목 등록 (단계 7 · D0)**: "탄소 없는 7 : 3 wt NCM622 : β-Li₃PS₄ 에서 AM d50 4.0 → 15.6 µm 로 σ_e 2.8 자릿수 ↓ · 비활성 AM 2 → 31 % · σ_ion 크기 무관 (Strauss 2018)" 을 **방향 항목**으로 — 값은 맞추는 데 쓰지 않는다.
2. **DEM 판별 시험 설계 (흐름 밖 → 단계 7)**: 우리 DEM 침대를 고체 중 AM ≈0.48 · AM 단분산 4 / 8 / 16 µm · SE 크기 고정 (이 논문은 SE 크기를 주지 않으므로 두 값으로 감싼다) 으로 만들어 σ_e 망 · 고립 AM 분율을 본다 — 이어진 구 망은 크기 무관이라 (§7-2) 차이가 나면 **연결성** 에서 온 것이다.
3. **우리 σ_e 폼의 크기 항 부호를 이 실측과 대조** — 그 전까지 이 논문을 우리 폼 (NCM(r) GB 계수 · AM_S = 단결정 라벨) 의 근거로 인용하지 않는다 (이 논문의 기전 = 망 연결 · 시료 = 모두 PC).
4. **DC 분극 보고 꼴 (흐름 밖: SBE · DBE σ_e 앵커)**: σ = l/(R·A) 로 적고 (원문 인쇄 식은 거꾸로), 성형압 · 측정압 · 휴지 시간 · 정상 영역 · 두께 · 면적 · 유리 층 저항을 함께 적는다 — 이 논문이 빠뜨린 칸이 곧 우리가 채워야 할 칸.
5. **크기만 바꾸는 시료 설계 (흐름 밖: 실험 협력)**: 같은 분말을 체로 갈라 (L = M 의 >20 µm) 화학을 고정한 채 크기만 바꾼다 — 다만 체 자름이 날카롭지 않았다 (d50 15.6 < 20).
6. **전자 고립 AM 을 XRD 로 세는 법 (흐름 밖)**: 충전 뒤 펠릿을 깨지 않고 두 상 Rietveld — 검출 한계 (2 % 근처 −11 % 오차) 와 '이온 고립과 전자 고립을 못 가름' 을 같이 적는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In carbon-free NCM622–β-Li₃PS₄ composite cathodes (7:3 wt), decreasing the NCM secondary-particle size (d50 15.6 → 4.0 µm) raised the first charge capacity from 84 to 162 mAh g⁻¹ at C/10, lowered the electrochemically inactive CAM fraction from 31 to 2 % (ex situ XRD), and increased the electronic partial conductivity by about three orders of magnitude (≈10⁻⁶ → ≈10⁻³ S cm⁻¹), while the ionic partial conductivity stayed ≈10⁻⁶ S cm⁻¹ (Strauss et al., *ACS Energy Lett.* 3 (2018) 992–996)."
- "The same three powders showed negligible size effects in liquid-electrolyte half-cells, indicating that the loss arises from electronic percolation through the CAM network of the solid composite (Strauss et al., 2018)."
- 국문 (한정어와 함께): *"탄소 없는 NCM622 : β-Li₃PS₄ (7 : 3 wt) 복합 양극에서 다결정 2차 입자를 15.6 → 4.0 µm 로 줄이면 전자 부분 전도도가 ≈3 자릿수 오르고 비활성 CAM 이 31 → 2 % 로 준다 (Strauss 2018 · 375 MPa 성형 · 55 MPa 측정 · SOC 0 의 DC 분극) — 단결정과의 비교가 아니고 SE 입경 · 기공은 보고되지 않았다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-6 의 ①–④.
**카드가 본 한계**
1. **SE 입경 · 기공 · 밀도 없음** — AM/SE 크기비를 모르므로 percolation 해석을 크기비로 옮길 수 없다.
2. **σ 는 충전 전 (SOC 0) 복합체** — 충전 상태의 σ_e (NCM 은 탈리튬하면 전자 σ 가 크게 오른다는 다른 카드 기록 · `asano2017_…` SOC 50 % σ_e ×26–45 [다른 카드]) 는 재지 않았다 → '비활성 = 전자 고립' 의 사슬은 SOC 0 의 망으로 잇는 해석이다.
3. **비활성 분율은 첫 충전 뒤 한 번 · ex situ · XRD 상 분율** — 이온 고립 · 전자 고립 · 반응 정지를 가르지 않는다 · S 는 검출 한계 근처.
4. **대략값끼리 안 맞음 · 본문 압력 0** — 밀도 · 기공을 만들지 않는다 (§3-1 · §3-6).
5. **원문 안 어긋남 여덟** (§3-6) — σ 식 · 75 s · M CE · SOC 용량 · 액체 L 충전 · 대략값 · 체 · 표기.
6. **기전 판정의 근거** = 부분 전도도 세 점 + 단면 SEM 정성 — 접점 수 · 연결성은 세지 않았다 (percolation 은 인용 [26] SOFC 이론).
7. **전이 한계**: NCM622 (코팅 없음) · β-Li₃PS₄ · 7 : 3 wt 탄소 없음 · 375 → 55 MPa · 25 °C · 셀 한 종류 · 반복 수 · 오차 막대 없음.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| (9) | Koerver, R.; Aygün, I.; Leichtweiß, T.; Dietrich, C.; Zhang, W.; Binder, J. O.; Hartmann, P.; Zeier, W. G.; Janek, J. Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes. Chem. Mater. 2017, 29, 5574−5582. | ★ '충전 수축 → CAM–SE 전기 접촉 감소' 의 인용처 (R2) — 카드 없음 (wishlist 에 이미 있음) |
| (18) | Zhang, W.; Schröder, D.; Arlt, T.; Manke, I.; Koerver, R.; Pinedo, R.; Weber, D. A.; Sann, J.; Zeier, W. G.; Janek, J. (Electro)chemical Expansion During Cycling: Monitoring the Pressure Changes in Operating Solid-State Lithium Batteries. J. Mater. Chem. A 2017, 5, 9929−9936. | 같은 인용처 · 이 논문 셀 장치의 출처 (SI [2]) — 카드 없음 (wishlist 에 이미 있음) |
| (16) | Zhang, W.; Weber, D. A.; Weigand, H.; Arlt, T.; Manke, I.; Schröder, D.; Koerver, R.; Leichtweiss, T.; Hartmann, P.; Zeier, W. G.; et al. Interfacial Processes and Influence of Composite Cathode Microstructure Controlling the Performance of All-Solid-State Lithium Batteries. ACS Appl. Mater. Interfaces 2017, 9, 17835−17845. | 7 : 3 wt 최적의 근거 · 같은 계 복합 미세구조 — 카드 없음 (lee2024 카드가 인용만) |
| (26) | Chen, D.; He, H.; Zhang, D.; Wang, H.; Ni, M. Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor. Energies 2013, 6, 1632−1656. | '작은 입자 = 접점 많음 → 전자 경로' 의 percolation 근거 — 카드 없음 |
| (20) | de Biasi, L.; Kondrakov, A. O.; Geßwein, H.; Brezesinski, T.; Hartmann, P.; Janek, J. Between Scylla and Charybdis: Balancing Among Structural Stability and Energy Density of Layered NCM Cathode Materials for Advanced Lithium-Ion Batteries. J. Phys. Chem. C 2017, 121, 26163−26171. | NCM 격자 · 부피 vs Li (화학–역학 입력) — 카드 없음 (koerver2018 · stallard2022 카드가 인용만) |
| (17) | Nam, Y. J.; Oh, D. Y.; Jung, S. H.; Jung, Y. S. Toward Practical All-Solid-State Lithium-Ion Batteries with High Energy Density and Safety: Comparative Study for Electrodes Fabricated by Dry- and Slurry-Mixing Processes. J. Power Sources 2018, 375, 93−101. | 7 : 3 wt 최적의 둘째 근거 · 건식 ↔ 습식 혼합 — 후보 표 N-78 |
| (21) · (22) | Kondrakov 2017 J. Phys. Chem. C 121, 24381 · 121, 3286 | 고 Ni NCM 격자 붕괴 · 이방 변형 · 기계 열화 (R7) |
| (6) | Liu, Z.; … Liang, C. Anomalous High Ionic Conductivity of Nanoporous β-Li₃PS₄. J. Am. Chem. Soc. 2013, 135, 975−978. | 이 논문 SE 의 합성 원전 — 카드 없음 |
| (8) | Kato 2016 Nat. Energy 1, 16030 | 정본 카드 있음 (`kato2016_high_power_assb_lsipscl_superionic`) |

## 13. [미확인] 목록 (본문 5 쪽 + SI 8 쪽 전수에 없음)
1. **SE (β-Li₃PS₄) 입경 · 형상** · Li₂S 불순물 분율 · 맨 SE σ (≈0.2 mS cm⁻¹) 의 측정 조건.
2. NCM 입도 측정법 (d50 · d90 · 부피 기준인지) · 단결정 / 다결정 1차 결정립 크기.
3. 진밀도 (NCM622 · β-Li₃PS₄) · 복합 기공 · 펠릿 두께 · 셀 지름 (반쪽 셀 · DC 분극).
4. DC 분극 시편의 두께 · 면적 · 유리 층 저항을 뺐는지 · 그림 S6 대표 곡선이 어느 시료인지.
5. 충전 상태 (SOC > 0) 의 σ_e · σ_ion.
6. SOC → 용량 계산식 · 이론 용량 · 과리튬 (Li₁₊ₓ) 처리.
7. 반복 셀 수 · 오차 막대.
8. 그림 2c 의 두 점선 중 어느 것이 C/30 · C/50 인지 (범례 없음).
9. operando XRD 간격 (75 s ↔ 그림 S3 축 180 s).
10. 단면 SEM 의 틈 · 금 · 층 두께 (≈150 µm 판독) 가 무엇인지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 본문 5 쪽 + SI 8 쪽을 글자 층 추출 + 그림 전부 열람으로 읽음.  서지 = 본문 첫 쪽 (제목 · 저자 7 명 · 소속 · 'Cite This: ACS Energy Lett. 2018, 3, 992−996' · 접수 · 승인 · 출판) · 쪽 바닥 DOI · 내려받기 주소 (권 3 · 호 4) · 감사 · 이해상충.  SI 첫 쪽 = 같은 제목 · 저자.  원문 낱말 셈: DEM (방법) · discrete · simulation · plastic · elastic · deform · unload · release = 0 · 'MPa' 는 본문 0 회 (SI 14 회).
- 그림 크롭 **43 장** = 도구 12 (Fig. 1–4 · SI Fig. S1–S7 · Table S1 — **다시 자름 3**: fig_1 쪽 폭 빈 곳 · fig_4 왼쪽 단 글자 조각 · tab_S1 아래 그림 S6 + 캡션 + 여백 세로 글줄) + 손 크롭 31 (그래픽 초록 1 · 패널 14 · 식 2 · 근거 문단 14).  본 뒤 다시 렌더 = fig_S6b (아래 끝) · txt_p3 하나 (다음 줄 글자 끝 흰색 가림).  캡션 글자 고침 4 (f1 본문 붙음 · f4 바닥글 · fS3 쪽 번호 · tS1 표 본문).  43 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop` · `caption_fix` · `note_manual`.
- 판독: digitized.csv 75 행 — 각 그림의 축 보정 · 색 분리 · 표지 판독 방법을 note 열에.  재현 확인: 그림 1e 충전 끝 161.1 · 94.1 · 83.0 ↔ 인쇄 162 · 95 · 84 · 그림 3b 십자 평균 0.456 · 0.562 · 0.525 ↔ SI 0.46 · 0.56 · 0.53 · 그림 3b 십자의 a · c ↔ 표 S1 (차 ≤0.001 Å) · 그림 S4 x 0.46 → 99.68 Å³ ↔ 표 S1 NCM-S 충전 99.68 · 그림 4 S→L 2.8 자릿수 ↔ 본문 '3 orders'.
- 2 차 인용 대조: 가리킨 카드 hippauf2019 (L276) · kawaguchi2023 (L282) · schmitt2026 (L405) · lei2026 (L122 · L207 · L242 · L244 · L279) + 인용 카드 bielefeld2019 · shi2019 · minnmann2022 · cronau2022 · famprikis2019 — 고치지 않았다 (카드 문제 = 정독 출력 batch_126 의 '카드 문제' 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (581 장 · strauss* 없음) + DOI (8b00275) · 제목 낱말 ('Impact of cathode material particle size') · 제1 저자 (Strauss) grep — 카드 없음 (인용만: 위 여덟 카드 · zuo2022 · stallard2022 의 Strauss 2020 은 다른 논문) (2026-11-16).

## 🔗 관련 카드
- 가리킨 카드 · 인용 카드: `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` · `lei2026_se_particle_size_effects_review` · `bielefeld2019_microstructural_modeling_composite_cathode` · `shi2019_high_am_loading_particle_size_assb` · `minnmann2022_designing_cathodes_solidstate` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `famprikis2019_fundamentals_inorganic_sse`.
- 복합 양극 부분 전도도 (DC 분극 · 이온 / 전자 차단): `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · `minnmann2021_jes_charge_transport_bottlenecks` · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` (NMC622 펠릿 σ).
- PC ↔ SC · CAM 크기: `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · `jung2023_single_crystal_ncm_morphology` · `kawaguchi2026_se_size_soc_dependent_cathode_resistance` · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`.
- 전자 percolation · 망: `chen2011_percolation_micromodel_composite_electrode` · `park2020_dimension_controlled_se_percolation_contact_area` · `kawaguchi2018_dry_coating_model_se_particle_powtec`.
- 화학–역학 (같은 그룹): `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
