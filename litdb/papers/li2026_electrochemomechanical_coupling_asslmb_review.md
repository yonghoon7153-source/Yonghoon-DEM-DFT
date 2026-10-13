<!-- digest 표준 양식 (standard depth — 1저자 우선순위 낮음 · 리뷰). ★ = 사용자가 특히 원한 항목. 형식 이웃 = stallard2022_cathode_mechanical_properties_review.md (리뷰 카드).
     쪽 표기 = 학술지 인쇄 쪽 "n of 68" (Batteries 2026, 12, 392 — PDF 쪽 = n).  SI 없음.
     값 표지: [인쇄] = 리뷰 본문 · 표 · 캡션에 적힌 값 (⚠ 대부분 인용 논문의 값을 리뷰가 옮긴 것 — 원 논문 미대조) · [판독] = 그림에서 읽은 값 ·
     [우리 대조] = 리뷰의 참고문헌 목록 · 정본 litdb 카드와 우리가 맞춰 본 결과 · [우리 산술] · [추정] · [미확인].
     본문 59 쪽 + 참고문헌 9 쪽 = 68 쪽 — 본문 전부 pdftotext 로 정독 · 표 4 개는 렌더로 대조 · 그림 13 장 · 표 4 장 = 크롭 17 장 접촉 시트로 열람. -->
# 전고체 리튬금속전지 (ASSLMB) 의 **전기-화학-기계 결합** 리뷰 — 응력의 출처 (양극 부피변화 · 복합양극 부조화 · Li 석출/박리 · 적층압 · 열) → 전기화학 영향 → 파괴 양식 → 측정법 → 완화 전략 → AI · ⚠ 표 3 의 Li₆PS₅Cl E = 4.7 GPa 는 **13 % 다공 펠릿값** · 표 3 인용 번호 전부 +7 어긋남 — Li · Li · Wang · Park · Fleischmann · Kato · **Cheng** (Batteries 2026)

> slug `li2026_electrochemomechanical_coupling_asslmb_review` · DOI `10.3390/batteries12100392` · type `review (전기-화학-기계 결합 · 전고체 Li 금속전지 · 측정 + 연속체/해석/위상장 모델 정리 — DEM 언급 없음)` · PDF `31._Electro-Chemo-Mechanical_Coupling_in_All-Solid-State_Lithium_Metal_Batteries_From_Stress_Generation_to_Failure_Mitigation.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: Qichanghao Li (Tohoku AIMR · IMR) · Ying Li (AIMR) · Zihao Wang (Tohoku 파괴신뢰성연구소) · **Kyu-Young Park** (POSTECH 신소재) · **Simon Fleischmann** (KIT HIU Ulm) · Hidemi Kato (Tohoku IMR) · **Eric Jianfeng Cheng\*** (Tohoku AIMR · ericonium@tohoku.ac.jp) · *Batteries* **2026**, 12 (10), 392 (MDPI · Review · 68 쪽) · 접수 2026-08-18 · 승인 09-18 · 출판 **2026-10-03** · 편집 Chunwen Sun · **CC BY** · 연구비 JST SICORP (JPMJSC25E2) · GIMRT · TUMUG · *"No new data were created or analyzed"* [인쇄 p.59].
> **정본 litdb 이웃 (이 리뷰가 인용하고 카드가 이미 있는 것 — 링크만)**: [`oh2026_bimodal_composite_cathode`](oh2026_bimodal_composite_cathode.md) (= ref [184]) · [`bucci2018_mechanical_instability_interface_delamination`](bucci2018_mechanical_instability_interface_delamination.md) (= [128]) · [`song2025_porous_argyrodite_modulus_fracture_toughness`](song2025_porous_argyrodite_modulus_fracture_toughness.md) (= [74]) · [`minnmann2024_microstructure_porosity_visualization`](minnmann2024_microstructure_porosity_visualization.md) (= [172]) · [`trevisanello2021_sc_pc_ncm_cracking_diffusion`](trevisanello2021_sc_pc_ncm_cracking_diffusion.md) (= [44]) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (= [72]) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (= [69]).

---

## 0. 결론 먼저 — 우리에게 쓸모 (정직하게: 중간 이하)
- 이 리뷰는 **Li 금속 음극 쪽 (석출 · 박리 · 덴드라이트 · 적층압) 이 절반 이상**이고, 복합양극 쪽은 문헌 요약 수준이다.  **새 자료 없음** (저자 명시).  DEM · 퍼콜레이션은 **한 번도 나오지 않는다** — 모델 쪽은 연속체 (2D Farzanian) · 1D 해석 (Bucci) · 응집 파괴 (Rezaei) · 위상장 (Yuan) · FE+ML (Wu) 뿐 [우리 대조 — 본문 검색].
- 우리에게 쓸모 있는 것 세 가지:
  1. **복합양극 기계 문헌 지도** (§4.1 · §6.1.2) — Koerver 2017 · Shi 2020 · Bucci 2018 · Rezaei · Yuan · Park 2025 (NCM811:LPSC 70:30 / 80:20 / 85:15) · Jeong 2024 (SE 입경 → 공극 11 vs 16 vol %) · **Oh 2026 (큰 PC + 작은 SC 바이모달, 7:3 최적)** 를 한 곳에 묶었다.
  2. **SC vs PC (ASSB)** 의 요약 한 줄 (Conforto 2021): SC 100 사이클 ≈91 % · 사이클 뒤 Li 확산 경로 중앙값 PC 3–4 배 ↔ SC < 2 배 [인쇄 p.13].
  3. ⚠ **물성 표의 함정 사례** — 표 3 의 Li₆PS₅Cl 행 (E 4.7 GPa · G 1.7 · ν 0.37 · H 0.9 · K_Ic 0.17) 은 정본 `song2025_porous_argyrodite_modulus_fracture_toughness` 카드의 **13 % 다공 펠릿 벌크값**과 같다 (그 카드: 나노압입 28 GPa · DFT ≈22 GPa 와 다른 양).  다른 행 (LLZO 150 · LGPS 37.2 GPa 등) 과 측정 부류를 표시하지 않고 한 표에 섞었고, **표 3 의 인용 번호는 모든 행이 +7 어긋나 있다** (§10-1).  ⇒ 이 표의 E_SE 를 우리 입력으로 옮기면 안 된다.

## 1. 한 줄 요약
ASSLMB 에서 고체 전해질의 강성이 전극 부피변화를 풀어 주지 못해 응력으로 바뀌고 (양극 부피변화 · 복합양극 상 간 기계 부조화 · Li 석출/박리 · 적층압 · 열팽창 차), 그 응력이 다시 수송 · 반응 · 접촉을 바꾸는 **양방향 결합**을 결정 → 입자 → 전극 → 계면 → 셀 축척으로 정리하고, 측정법 (표 4, 19 기법) · 완화 전략 (코팅 · 순응 복합양극 · 바이모달 · 결정 방향 · 적층압 · 계면층 · 자가치유) · AI 폐루프 설계를 묶은 총설.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Q. Li, Y. Li, Z. Wang, K.-Y. Park, S. Fleischmann, H. Kato, **E. J. Cheng\*** (Tohoku · POSTECH · KIT) | Batteries 12 (2026) 392 · MDPI · CC BY | 10.3390/batteries12100392 | 산화물 · 황화물 · 할라이드 SE 전반 + 층상 · 스피넬 · 올리빈 양극 + Li 금속 · Si 음극 | 리뷰 (참고문헌 218 편 · 새 자료 없음) |

---

## 3. 핵심 수치 (리뷰가 옮긴 값 — 원 논문 미대조, [인쇄] = 리뷰에 적힌 값)

### 3-1. 표 2 — 양극의 충전 부피변화 [인쇄 p.4]
| 양극 | 구조 | 상전이 | 충전 부피변화 | 지배 응력 원인 | 기계 열화 | 리뷰 ref |
|---|---|---|---|---|---|---|
| LCO | 층상 | H1-H2-H3 | +2 % | CoO₂ 층 수축 | 균열 | [27,28] |
| NCM111 | 층상 | H1-M-H2-H3 | −3.4 % | 중간 이방 변형 | 균열 | [29,30] |
| **NCM811** | 층상 | 강한 H2-H3 | **−6 %** | c 축 수축 | **입계 파괴** | [31,32] |
| LNO | 층상 | 강한 H2-H3 | −9 % (비단조) | Ni–O 수축 | 붕괴/균열 | [33,34] |
| LMO | 스피넬 | 입방/정방 | −1.5 % | Mn³⁺ 왜곡 | 파괴 · Mn 용출 | [35,36] |
| o-LNMO | 스피넬 | 2 상/고용 | −3 % | 고전압 변형 | 계면 열화 | [37,38] |
| LFP | 올리빈 | LFP/FP | −6.8 % | 정합 응력 | 상경계 응력 | [39,40] |
- ⚠ 같은 리뷰 본문 (Kondrakov [30], 3.0–4.3 V vs Li): **NCM811 단위포 부피변화 최대 5.1 % · NCM111 1.2 %** · NCM811 c 14.467 → 14.030 Å [인쇄 p.5] — 표 2 (−6 % · −3.4 %) 와 숫자가 다르다 (출처 · 전압창 미표기).

### 3-2. 표 3 — 무기 SE 의 실온 σ · 기계 물성 [인쇄 p.8]
| SE | 구조 | σ_RT (S cm⁻¹) | E (GPa) | G (GPa) | ν | H (GPa) | K_Ic (MPa m^½) | 인쇄 ref → [우리 대조] 실제 해당 |
|---|---|---|---|---|---|---|---|---|
| Li₇La₃Zr₂O₁₂ | 가넷 | 3 × 10⁻⁴ | 150 | 60 | 0.26 | 6.3 | 1.25 | [66–68] |
| Li₆.₄La₃Zr₁.₄Ta₀.₆O₁₂ | 가넷 | 4.5 × 10⁻⁴ | 159 | 63 | 0.26 | 11.3 | 1.51 | [69] |
| Li₀.₃₅La₀.₅₇TiO₃ | 페로브스카이트 | 1 × 10⁻³ | 200 | 80 | 0.26 | 9.2 | 1 | [70–72] |
| Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃ | NASICON | 1.8 × 10⁻⁴ | 131 | 53 | 0.24 | 11 | 1.4 | [73] |
| Li₁.₅Al₀.₅Ge₁.₅(PO₄)₃ | NASICON | 5.0 × 10⁻⁴ | 141 | 56 | 0.25 | 10.6 | 0.52 | [74] |
| 75Li₂S–25P₂S₅ | 유리 | 2.8 × 10⁻⁴ | 18 | 7.1 | 0.30 | 1.9 | 0.23 | [75–77] → 실제 [68–70] (Hayashi 2001 · Sakuda 2013 · McGrogan 2017) |
| Li₇P₃S₁₁ | 유리-세라믹 | 1.7 × 10⁻² | 21.9 | 8.1 | 0.35 | – | – | [78,79] → [71,72] (Seino 2014 · Deng 2016) |
| **Li₆PS₅Cl** | 아지로다이트 | **1.1 × 10⁻³** | **4.7** | **1.7** | **0.37** | **0.9** | **0.17** | **[80–82] → [73–75] (Yu 2016 · Song 2025 · Wang 2024)** |
| Li₁₀GeP₂S₁₂ | LGPS | 1.2 × 10⁻² | 37.2 | 14.4 | 0.30 | 0.5 | 0.34 | [83–86] → [76–79] |
| Li₃YCl₆ | 층상 할라이드 | 5.1 × 10⁻⁴ | 38 | 15 | 0.27 | 1.7 | – | [87–89] → [80–82] (Asano 2018 · **Andrews 2017 — 섬광체 액체 형광, 무관** · Liu 2024) |
| Li₃InCl₆ | 왜곡 암염 | 2 × 10⁻³ | 10.5 | 3.8 | 0.39 | – | – | [90,91] → [83,84] (Li 2019 · Ren 2022) |
- [우리 대조]: 참고문헌 목록 쪽 (p.62–63) 의 번호를 렌더로 확인 — 인쇄 번호의 문헌 (예: [80] Asano 할라이드 · [81] 섬광체 액체 · [82] Liu 할라이드 · [90] 접촉역학 · [91] 압력 계면) 은 그 행의 물질과 맞지 않고, **7 을 빼면 모든 확인 행이 그 물질의 문헌이 된다**.  ⇒ 표 3 의 인용은 **일괄 +7 오프셋** (위 6 개 행은 확인 · 위 5 개 산화물 행은 미확인).
- [우리 대조] **Li₆PS₅Cl 행 = 정본 `song2025_porous_argyrodite_modulus_fracture_toughness` 의 값** (E 4.7 ± 1.1 GPa · K_Ic 0.17 ± 0.03 · ν 0.37 가정 — 그 논문은 **기공 13 % · 360 MPa 냉간 · ⌀≈1 µm 입자 펠릿의 mm 시편 벌크값**, 같은 논문의 나노압입 28 GPa · 0.69).  리뷰는 다공 · 측정 부류를 표시하지 않았다.

### 3-3. 복합양극 기계 (§2.2 · §4.1 · §5.1 · §6.1.2)
- 복합양극 SE 함량 *"approximately 20–50 wt%"* [인쇄 p.7].
- Farzanian [50] (2D 연속체): **E < 20 GPa** 인 황화물은 양극 부피변화를 수용해 결함 억제 · LLZO (E ≈150 GPa) 는 손상 큼 · 양극 > 50 vol % 면 전극 팽창 > 5 % · 공극 > 1 % [인쇄 p.8].
- Park [51] (ACS Nano 2025, NCM811 : LPSC = 70:30 / 80:20 / 85:15): 80:20 · 85:15 열화 심함 · 미세구조 기반 모의에서 방전 중 NCM 부피변화 ≈10 % · 85:15 가 70:30 보다 > 2 GPa 응력 영역이 훨씬 넓음 · 3D XANES: NCM 많을수록 방전 끝 리튬화 덜 되고 불균일 [인쇄 p.8–9 · p.36].
- Koerver [119] (NCM811 / β-Li₃PS₄): 첫 쿨롱효율 70.5 % · 사이클당 1–2 % 손실 · 50 사이클 뒤 81 mAh g⁻¹ · 첫 충전 중 계면 저항 +≈140 *"Ω·cm−2"* (⚠ 단위 오기 — Ω·cm²) · 충전 뒤 입자 둘레 구형 틈 [인쇄 p.21].
- Shi [118] (JMCA 2020): 129 → 102 mAh g⁻¹ (26 사이클) → 30–40 사이클 급락 → < 20 · 접촉 손실 부피 2.87 → 10.4 vol % (입자 한쪽에 몰림) · 50 사이클 뒤 **300 MPa 재가압으로 ≈80 mAh g⁻¹ 회복** [인쇄 p.23].
- Bucci [128]: 반경 변형 ≈2.5 % (부피 ≈7.5 %) 면 대부분 조합에서 계면 박리 개시 · 무른 SE 면 부피 ≈25 % 까지 · 반경 50–500 nm 입자는 균열 안정화 [인쇄 p.23] — 정본 `bucci2018_mechanical_instability_interface_delamination` 카드 §3.1 과 일치 [우리 대조].
- Yuan [130] (3D, LLZO): 최대 박리 틈 ≈23.4 nm · 무른 SE 는 지연시킬 뿐 [인쇄 p.24].
- Zheng [109] (Sci. Adv. 2025, TXM): 사이클 뒤 NCM811 균열 = 입자 부피의 ≈5.36 % · LNO 코팅 0.058 % · LNO@NMC811 133 → 116 mAh g⁻¹ (200 사이클) vs 비코팅 110 → 6 [인쇄 p.37 · p.44].
- Jeong [173] (AEM 2024, XCT): 작은 LPSC 양극 공극 ≈11 vol % ↔ 큰 LPSC 16 vol % · 임계압 ≈400 MPa 위에서 두 전극 응답 비슷 (공극 붕괴) · 0.1C 유지율 94.26 % vs 47.33 % [인쇄 p.36].
- Minnmann [172] (JES 2024, 플라스마 FIB-SEM): SE 입경 ↓ → 공극 ↓ · 이온 tortuosity ↓ · 유효 이온전도도 ↑ [인쇄 p.34].
- **Oh [184] (ACS Energy Lett. 2026)**: 큰 다결정 NCWA (LiNi₀.₈₈Co₀.₁₀W₀.₀₁Al₀.₀₁O₂) + 작은 단결정 NCM + LPSC · 단봉 대비 **공극 35–58 % 낮음** · 큰 PC : 작은 SC **= 7:3 최적** (0.5C 최고 · 2–3C 양호) · 200 사이클 **87.8 %** [인쇄 p.46] — 정본 `oh2026_bimodal_composite_cathode` 카드와 일치 (2D 공극 16.80 → 7.55 → 17.96 · 87.80 %) [우리 대조].
- Conforto [108] (JES 2021): ASSB 에서 SC-NCM 100 사이클 ≈91 % · 사이클 뒤 Li 확산 경로 중앙값 **PC 3–4 배 ↑ ↔ SC < 2 배** [인쇄 p.13].
- Moradi [185] (Nat. Commun. 2025): 003-LCO 충전 +≈40 kPa (압축) ↔ 110-LCO −≈30 kPa (인장) · 음응력 NMC622 복합양극 셀 **1 MPa** 적층압 · 5 mAh cm⁻² · 1.25 mA cm⁻² · 200 사이클 > 99 % [인쇄 p.46–47].

### 3-4. 음극 · 적층압 · 열 (요약만)
- Zhang [52] (임베디드 변형 센서): 초기 적층압 200 → 3500 kPa 면 초기 변형 증가 단계 ≈50 % 단축 · 정상 단계 평균 변형 −47.4 % · 전류 0.1 → 0.2 mA cm⁻² 면 정상 단계 변형 ≈4 배 [인쇄 p.10].
- Zhang [56]: Li 크리프가 0.005 mA cm⁻² 위에서는 석출 속도를 못 따라감 [인쇄 p.11] · Vishnugopi [142]: 석출 10 mA cm⁻² 에 ≈10 MPa · 박리 5 mA cm⁻² 에 ≈12 MPa 필요 [인쇄 p.31].
- 열응력 식 (1): **σ_th = E·Δα·ΔT / (1 − ν)** [인쇄 p.12].
- AI 다목적 설계 식 (11–12): min [R_int, ΔG_rxn, σ_max, D_damage] s.t. σ_ion ≥ σ_min · σ_e ≤ σ_e,max · K_Ic ≥ K_Ic,min [인쇄 p.56] · 비정질 LiF 코팅 (LCO/LPSC) 은 ≈1 nm 넘으면 Li 수송 방해 (ML-MD, ref [214]) [인쇄 p.57].

### 3-5. 표 4 — 측정 기법 19 종 비교 [인쇄 p.33]
광학 · SEM · FIB-SEM · 싱크로트론 XCT · TXM · XANES 영상 · **중성자 영상/단층** (Li 민감도 ✓ · 응력 ✗ · 공간해상도 10–100 µm) · 중성자 회절 · 싱크로트론 XRD · Raman · DIC · 광섬유 브래그 격자 · 압력 센서 · AFM · 나노압입 · cryo-TEM 등 — 공간해상도 · operando 가능 · Li 민감도 · 응력 민감도 · 장단점 표.

---

## 4. ★ 방법 · 입자 처리 (리뷰가 다룬 모델 계열)
- 실험 정리 + 모델 계열 소개: 2D 연속체 (Farzanian) · 1D 방사대칭 해석 + 응집 파괴 (Bucci) · 열역학 일관 응집 파괴 (Rezaei — SE 구속에서 반경 균열 + 원주 균열 + 입계 전단 = 혼합 모드) · 3D 전기-화학-기계 결합 (Yuan, 위상장) · FE 데이터 + 물리정보 SE-UNet (Wu) · 결정립 수준 화학역학 (Liu [120]).
- **입자 처리**: 모두 연속체 (입자 = 연속 영역 · 접촉망 없음) 이거나 단일 입자 단위셀.  **DEM (접촉망 · 재배열 · 패킹) 은 리뷰 범위 밖** — frame[5] 의 DEM 쪽 반쪽이 통째로 비어 있다.
- 용어: **ASSLMB** (전고체 리튬금속전지) · **R_int** (계면 저항) · **CTE** (열팽창계수) · **K_Ic** (모드 I 파괴인성) · **MEIS / MV** (기계-전기화학 임피던스 · 기계-전압전류법 — 전기 + 기계 신호 동시 획득) · **TXM** (투과 X 선 현미경).

## 5. Figure set
| Fig / Table | 내용 | 우리 활용 |
|---|---|---|
| 1 | 음극/양극 결합 · 계면 파괴 개념도 | 개념 |
| 2 | 응력의 출처 — (a–c) 양극 격자 · 균열 (d, e) **복합양극 응력 (Farzanian · Park, 로딩 의존)** (f, g) Li 석출/박리 (h–k) 적층압 · 접촉역학 · Li 크리프 | (d, e) 가 우리 MPM/DEM 복합양극 응력 지도와 같은 그림 언어 |
| 3 | 응력 → 전기화학 — (a–c) **SC vs PC 확산 경로 (Conforto)** · 균열-반응 불균일 (Zheng) (d–g) Li 결함 응력 · 공극 (h, i) 외부 하중 (j, k) 계면 진화 단계 | (b) SC/PC 사이클 뒤 확산 경로 비교 |
| 4 | **복합양극 파괴** — (a, b) Koerver 틈 (c, d) 셀 휨 · 모서리 균열 (e) Shi 접촉 손실 3D (f, g) Bucci 박리 지도 (h, i) 구속 하 혼합모드 균열 (j–l) Yuan 3D 박리 | ★ 우리 A10 접촉 원장 (CZM) · Auerbach 파괴 축의 문헌 지도 |
| 5 | 덴드라이트 · SE 관통 | 음극 축 (우리 범위 밖) |
| 6 | 계면 열화 — (a) Si/LPSC 복합 음극의 3D SE 망 (b–d) 접촉 손실 · 협착 반원 (e) SEI 응력 | (c) 접촉 손실 = 저주파 협착 반원 — 우리 Holm 협착과 같은 물리 |
| 7 | 측정법 개관 | — |
| 8 | 3D 측정 — (a) Minnmann FIB-SEM (b) Jeong XCT (SE 입경) (c) Park 3D XANES (로딩) (d) Zheng TXM | (a, b) SE 입경 → 공극 · tortuosity (우리 SE 크기 축) |
| 9 · 10 | Li 석출 · 관통 operando · 응력 operando (적층압 · 광섬유 · DIC) | 음극 / 셀 축 |
| 11 | 양극 완화 — (a) LNO 코팅 · Li₃BO₃ (b) PVDF–PAN (c) **Oh 바이모달 (큰 PC + 작은 SC)** (d) LCO 결정 방향 (Moradi) | ★ (c) = 우리 PC:SC 축의 실험 대응 (정본 `oh2026_bimodal_composite_cathode` 카드) |
| 12 | 계면 공학 — LLZO 표면 · 일시 액상 치밀화 · 열구배 · 계면층 | — |
| 13 | 자가치유 · 순응 기판 · 유연 셀 | — |
| Table 1 | 응력 출처 5 종 × 기전 · 지배 축척 · 결과 | 분류 틀 |
| Table 2 | 양극 7 종 부피변화 | NCM811 −6 % (본문 5.1 % 와 상충) |
| Table 3 | SE 11 종 σ · E · G · ν · H · K_Ic | ⚠ LPSCl = 다공 펠릿값 · 인용 +7 오프셋 |
| Table 4 | 측정 기법 19 종 비교 | 중성자 영상 = Li 민감 · 10–100 µm (짝 카드 kim2026 과 연결) |

## 6. Post-processing
- 리뷰 — 자체 후처리 없음.  우리 후처리 = 표 3 인용 번호 대조 (렌더) · LPSCl 행 ↔ 정본 `song2025_porous_argyrodite_modulus_fracture_toughness` 대조 · Bucci · Oh 요약 ↔ 정본 카드 대조 · 본문 검색 (DEM · 퍼콜레이션 0 회).

---

## 7. 우리 DEM+MPM 대비 (관련도: 중간 이하 — 정직하게)
| 항목 | 이 리뷰 | 우리 | 판정 |
|---|---|---|---|
| E_SE (LPSCl) | 표 3: **4.7 GPa** (다공 13 % 펠릿 · 출처 표기 없이) | 실재 bulk 22–24 GPa (우리 DFT E_VRH 22.06) · DEM E_eff 1.35 · MPM 1.53 GPa (연화 대리값 — CLAUDE.md frame[2]) | ⛔ 이 표의 4.7 을 입력으로 쓰지 않는다 — **측정 부류가 다르다** (다공 mm 벌크 ↔ 결정 · DFT) |
| 복합양극 SE 함량 | 20–50 wt% | ps45 18.4 wt% (하한 아래쪽) | 우리 침대는 SE 가 적은 쪽 끝 |
| 바이모달 PC:SC | Oh 2026 요약 — 7:3 최적 · 공극 35–58 % ↓ | ps45 다섯 조성 · 7:3 에서 σ_ion 최대 (Hertz 0.0893 mS cm⁻¹) — 단 *"7:3 최적" 은 시드 산포 안이라 확정 못 함* (`docs/data/ps45_r45_network_g2_20261007/README.md`) | 방향 같음 · 우리 쪽 한정어 유지 |
| 접촉 손실 · 박리 | Bucci 2.5 % 반경 · Shi 2.87 → 10.4 vol % · 재가압 회복 | A10 접촉 원장 (`cycle_contact_ledger.py` — Bucci CZM 판정, CLAUDE.md 2026-07-22) · DEM 제하 팔 없음 | Shi 의 "재가압 회복" = 접촉 손실이 가역 기계 몫이라는 실험 — 우리 제하/재가압 팔의 표적 후보 |
| SC vs PC | Conforto: 확산 경로 PC 3–4 배 ↑ ↔ SC < 2 배 | `docs/ncm_sc_poly_electrochem_anchors.md` §1 (ASSB 에서 SC > PC · Jung 2023 5C SC 74.0 % vs PC 41.6 %) | 같은 방향 (2 차 요약 하나 추가) |
| 접촉 손실의 임피던스 | 저주파 협착 반원 (Eckhardt) | DEM 망의 Holm 협착 (접촉당) | 같은 물리 · 다른 척도 (Li/SE 평면 계면 ↔ 입자 접촉망) |
| 모델 계열 | 연속체 · 해석 · 위상장 · FE+ML | DEM (접촉망) + MPM (형상 소성) | 리뷰에 **DEM 없음** → frame[5] DEM 쪽 공백 = 우리 위치 |

- frame[5]: 이 리뷰가 정리한 모델은 전부 **MPM/연속체 쪽 (기계 · 형상)** 이고, **접촉망 수송 (DEM)** 은 다루지 않는다 — 우리 DEM+MPM 분업을 설명할 때 *"문헌의 전기-화학-기계 모델은 연속체 쪽에 몰려 있다"* 는 근거로 쓸 수 있다 (리뷰 범위 한정 — 분야 전체 주장 아님) [우리 해석].

## 8. 적용 인사이트
1. **물성 표를 옮길 때 측정 부류부터** — E_SE 를 문헌 표에서 가져오면 다공 펠릿 (4.7) · 나노압입 (28) · DFT (22) 가 같은 이름으로 섞인다.  우리 입력 감사 (CLAUDE.md 규율 ⑥ — 원문 확인한 정본 카드에서만) 의 반례 사례로 기록.
2. **재가압 회복 (Shi 2020)** — 접촉 손실의 가역 몫을 재는 실험 설계 표적 (우리 DEM 에는 제하 · 재가압 팔이 없다).
3. **Oh 2026 · Jeong 2024 · Minnmann 2024 · Park 2025** 를 묶은 지도 — PC:SC · SE 입경 · NCM:SE 비 세 축을 한 번에 보는 문헌 목록 (원 논문 카드 필요: Jeong 2024 · Park 2025 · Conforto 2021 · Shi 2020 · Zheng 2025 는 정본 카드 **없음**).

## 9. 인용 가능 문장
- "A 2026 review of electro-chemo-mechanical coupling in all-solid-state Li-metal batteries summarizes composite-cathode failure as contact loss, particle cracking and interfacial debonding driven by cathode volume change under solid-electrolyte constraint (Li et al., *Batteries* 2026, 12, 392)."
- ⚠ 그 리뷰의 Li₆PS₅Cl E = 4.7 GPa 는 인용하지 않는다 (다공 펠릿값 · 원 논문 = Song 2025 를 직접 인용).

## 10. 주의/한계
1. **표 3 인용 번호 +7 오프셋** (확인 6 행) · ref [81] (섬광체 액체 형광, PCCP 2017) 은 주제와 무관한 문헌 — 표 3 수치를 인용할 때는 **원 논문을 직접** 찾아야 한다.
2. **LPSCl E 4.7 GPa = 13 % 다공 펠릿 벌크값** — 부류 표시 없이 다른 SE 의 치밀/DFT 값과 섞임.
3. **표 2 ↔ 본문 불일치** (NCM811 −6 % ↔ 5.1 % · NCM111 −3.4 % ↔ 1.2 %).
4. 단위 오기 *"140 Ω·cm−2"* (p.21).
5. 리뷰 — 숫자는 전부 2 차 인용 (원 논문 미대조 — 위 [우리 대조] 표지가 붙은 것만 확인) · 그림은 대부분 재수록.
6. Li 금속 음극 중심 — 복합양극 · 수송망 (퍼콜레이션 · tortuosity) 은 가볍게만.

## 11. 참고문헌 — 우리가 더 볼 것 (리뷰 목록 서지 그대로)
| 번호 | 서지 | 왜 |
|---|---|---|
| 51 · 86 | Park, S.H.; … Hatzell, K.B. Chemo-Mechanical Behavior and Stability of High-Loading Cathodes in Solid-State Batteries. ACS Nano 2025, 19, 22262–22269 | ★ NCM811:LPSC 70:30–85:15 · 3D XANES · 미세구조 응력 — 우리 AM:SE 축 (정본 카드 없음) |
| 173 | Jeong, M.; … Operando Investigation on the Role of Densification and Chemo-Mechanics on Solid-State Cathodes. Adv. Energy Mater. 2024, 14, 2304544 | ★ SE 입경 → 공극 11 vs 16 vol % · 임계압 ≈400 MPa (정본 카드 없음) |
| 108 | Conforto, G.; … Janek, J. … Chemo-Mechanical Degradation … NCM-Based Cathodes in Solid-State Li-Ion Batteries. J. Electrochem. Soc. 2021, 168, 070546 | SC vs PC 확산 경로 (정본 카드 없음) |
| 118 | Shi, T.; … Ceder, G. Characterization of Mechanical Degradation in an All-Solid-State Battery Cathode. J. Mater. Chem. A 2020, 8, 17399–17404 | 접촉 손실 vol % · 300 MPa 재가압 회복 (정본 카드 없음) |
| 109 | Zheng, X.; … Unravelling Electro-Chemo-Mechanical Interplay in Layered Oxide Cathode Degradation in Solid-State Batteries. Sci. Adv. 2025, 11, eady7189 | TXM 균열 부피 · LNO 코팅 |
| 50 · 85 | Farzanian, S.; … Tu, Q.H. Mechanical Investigations of Composite Cathode Degradation in All-Solid-State Batteries. ACS Appl. Energy Mater. 2023, 6, 9615–9623 | E < 20 GPa 수용 · 로딩 > 50 vol % |
| 185 | Moradi, S.; Zahiri, B.; Braun, P.V. Cathode Chemomechanics Controls Li Metal Solid-State Battery Performance under Low Stack Pressures. Nat. Commun. 2025, 16, 9266 | 결정 방향으로 양극 응력 부호 제어 |
| 184 | Oh, H.; … Lee, Y.M.; et al. Bimodal Composite Cathodes Advancing the Chemo-Mechanical Integrity and Kinetics for All-Solid-State Batteries. ACS Energy Lett. 2026, 11, 2103–2114 | 정본 카드 있음 (`oh2026_bimodal_composite_cathode`) |

## 원문 대조 기록 (2026-10-13)
- 본문 59 쪽 pdftotext 정독 (참고문헌 9 쪽은 필요한 번호만) · 표 1–4 렌더 대조 · 참고문헌 p.62–63 번호를 PyMuPDF 단어 좌표로 확인 (표 3 오프셋 판정 근거).
- 크롭 17 장 (그림 13 = 임베드 래스터/띠 합집합 bbox · 표 4 = 제목 ~ 괘선/Note) · 캡션 = 텍스트 층 (다음 쪽으로 이어진 Fig. 3 · 4 · 12 는 이어 붙임).
- 정본 litdb 전수 검색 (papers/ 목록 + 제목 · 저자 · DOI grep): 같은 리뷰 카드 없음.

## 🔗 관련 카드
`oh2026_bimodal_composite_cathode` · `bucci2018_mechanical_instability_interface_delamination` · `bucci2017_chemomech_failure_assb_cycling_czm` · `song2025_porous_argyrodite_modulus_fracture_toughness` · `stallard2022_cathode_mechanical_properties_review` · `minnmann2024_microstructure_porosity_visualization` · `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `hu2024_amorphous_lif_coating_lco_lpscl_interface` · `kim2026_operando_neutron_thick_nmc811_interior_hotspot` (중성자 영상).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
