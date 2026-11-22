# batch 137 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-88)

대상: `ohsaki2021_liquid_phase_shaking_li3ps4_size_control_fine_li2s` — S. Ohsaki · T. Yano · A. Hatada · H. Nakamura · S. Watano\*, "Size control of sulfide-based solid electrolyte particles through liquid-phase synthesis", *Powder Technology* **387** (2021) 415–420 · DOI 10.1016/j.powtec.2021.04.050 (본문 6 쪽 + SI 3 쪽).
Li₃PS₄ (LPS) 를 프로피온산 에틸 속 액상 진탕법으로 만들 때 원료 Li₂S 를 습식 유성 볼밀 (중앙값 8 → 1.5 µm) 이나 에탄올 용해–석출 (0.34 µm) 로 먼저 작게 해 LPS 를 SEM 등가원 1382 nm (인용) → 227 → 93 nm 로 줄이고 360 MPa 펠릿 σ 1.1 · 1.5 × 10⁻⁴ S/cm 를 보고한 합성 실험 (계산 · 기공 · 압밀 없음).
쪽 = PDF 쪽 p.1–6 (인쇄 쪽 = 414 + n) · SI p.1–3 · 판독 원자료 = `litdb/figures/ohsaki2021_…/digitized.csv` (23 행 · 래스터 원본 픽셀) · 고른 의도 대조 = **채움 (한정 둘)** (카드 §0-1 — 서브 µm SE 크기 제어 · kawaguchi2023 LPS 합성 출처 = 채움 · '밀링 없이' = 일부 (원료 Li₂S 볼밀 경로 있음) · 재료 = Li₃PS₄).
인용 서지 (질문 k · l 용): Ohsaki, Yano, Hatada, Nakamura, Watano, Powder Technol. 387 (2021) 415–420.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 기공 · 밀도 · 두께 숫자가 원문에 없다 (전문 검색 'porosity' · 'thickness' 0 회 · 'density' 는 에너지 밀도 · '고밀도 충전' 표현뿐).
- [a] ohsaki2021_… | (참고 · 곡선 아님) 순수 Li₃PS₄ 펠릿을 **360 MPa** 로 만들어 임피던스만 잼 — 펠릿 질량 · 두께 · 밀도 · 측정 중 압력 [미확인] | 카드 §3-1 · p.3 (`txt_p2p3_characterization_impedance_360mpa.png`) | 인쇄 | LPSCl 아님 · 진밀도 없음 · 랩 표준 (10–13 % · 1.64) 옆에 둘 숫자 없음

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 · 되돌아옴 · 두께 측정 없음 (360 MPa 성형 뒤 상태 미기재).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 값 0 건 (정성 *"high deformability, softness, and ductility"* 한 줄은 질문 l 에 옮김).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (CAM · 복합체 없음).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).
- [f] ohsaki2021_… | (간접 · 해상도 규칙의 '지름' 정의) 판상 LPS 의 등가원 지름은 2D 투영 넓이로 정해져 짧은 축 (폭) 을 감추고 두께는 재지 않았다 — 원래 LPS ≈3 µm × 500 nm → 등가원 1382 nm · 볼밀 유래 길이 0.34 ± 0.11 µm · 폭 129 ± 61 nm → 등가원 227 ± 68 nm | 카드 §3-3 · §4-2 · §8 U1 · 표 1 · p.4–5 (`tab_1.png` · `txt_p4p5_original_milled_lps_sizes.png`) | 인쇄 · [카드 산술] (3 × 0.5 µm → √(4·1.5/π) = 1.382 µm 재현) | 지름당 셀 수 규칙에 넣을 지름 = 가장 얇은 치수 [카드 해석]

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 전이 진술 없음.
- [g] ohsaki2021_… | (참고) 크기 전부 SEM **2D 투영** 등가원 지름 (≥100 개 · 판상 = 다각형 넓이) · 3D 측정 없음 · 볼밀 Li₂S 는 레이저 회절 중앙값 (응집을 쟀을 가능성 저자 언급) | 카드 §3-1 · §4-2 · p.3 (`txt_p2p3_characterization_impedance_360mpa.png` · `txt_p3_milling_median_8_to_2um.png`) | 인쇄 | 2D 크기를 3D 구 지름으로 옮기는 환산 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (복합체 없음).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
가압 · 탈압과 직접 닿는 것 없음.  원문 한계 (참고):
- [j] ohsaki2021_… | *"It is noted that the details of the physicochemical reaction during LPS synthesis has not been elucidated yet"* — 그림 9 관계의 기전 미해명 | 카드 §0 ⑦ · §3-4 · p.5 (`txt_p5_fig9_linear_square_relation.png`) | 인쇄 | 합성 쪽 한계
- [j] ohsaki2021_… | LPS 입도 분포를 레이저 회절로 못 잼 (*"the chemical reaction for LPS particles proceeded in a solvent"*) · 볼밀 Li₂S 측정에 응집이 섞였을 가능성 · SEM *"slightly poor focus due to the difficulty of SEM observations of the sulfide solid electrolytes"* | 카드 §3-1 · §3-2 · §3-3 · p.3 · p.5 | 인쇄 | 크기 측정 자체의 한계 — 입경을 DEM 입력으로 옮길 때의 불확실도
- [j] ohsaki2021_… | (카드가 적은 원문 공백) σ 측정 온도 · 두께 · 밀도 · 측정 중 압력 · 회로 · Li₃PS₄ 진밀도 · BET · 반복 [미확인] · Nyquist 최저점 비 1.77 ↔ σ 비 1.36 불일치 [카드 산술] | 카드 §3-5 · §13 | 카드 서술 | 펠릿 σ 를 수송 계산의 입력이나 대조값으로 쓰기 전에 필요한 칸이 비어 있다

## k — DEM 의 한계 (서지: Ohsaki, Yano, Hatada, Nakamura, Watano, Powder Technol. 387 (2021) 415–420)
- [k] ohsaki2021_… (Ohsaki 2021 · Powder Technol.) | **말 없음** — 계산 · 모사를 하지 않고 DEM 을 인용하지도 않는다 (본문 · SI 에 DEM · discrete · simulation 0 회) | 카드 §4-4 (i) | — | DEM 한계 진술 0

## l — 소성변형이 왜 어려운가 · 우회 (서지: Ohsaki, Yano, Hatada, Nakamura, Watano, Powder Technol. 387 (2021) 415–420)
- [l] ohsaki2021_… (Ohsaki 2021 · Powder Technol.) | **논의 없음** — 정성 한 줄만: *"In addition, sulfide SEs have unique mechanical properties such as high deformability, softness, and ductility."* (p.1 · 수치 · 인용 없음) | 카드 §4-3 · §4-4 (ii) · `txt_p1_mechanics_dense_packing.png` | 인쇄 | 황화물 일반 서술 · Li₃PS₄ 값 없음 · 우회 · 비용 없음

## m — 받아들일 통찰
- [m] ohsaki2021_… | **입경의 정의 칸을 등록 의무로** — 한 논문에 크기 정의 넷 (레이저 회절 중앙값 · SEM 2D 등가원 평균 · DLS 강도 봉우리 166.6 nm · Z-평균 6393 nm) 이 섞이고 그림 9 가로축 값이 이름 ((Li₂S 크기)²) 이 아니라 (π/4)·d² 다 (다섯 점 ≤ 2 px) → 문헌 입경을 결과 전 대조나 DEM 구 지름 · 격자 해상도로 옮길 때 '측정 · 통계 · 2D/3D · 응집 · 모양' 을 칸으로 둔다 | 자리: 단계 0 · U1 · 후보 D0 | 왜: 카드 §3-4 · §4-2 · §7-4 · 그림 9 (`fig_9.png` · digitized.csv fig9) [판독 · 카드 산술]
- [m] ohsaki2021_… | **사면체 틈 규칙을 크기비 탐색의 기준선으로** — '5 µm 구 조밀 충전 → 틈 ≈1.1 µm' = 사면체 틈 내접구 0.2247·D (팔면체 0.4142·D) [카드 산술] → 우리 12 : 4 : 1 의 SE/AM_S 0.25 는 사면체 한계 바로 위 · AM_P 사면체 틈 (2.70 µm) 에는 들어감 [우리 산술 · 단분산 조밀 가정] — Furnas dip 크기비를 바꿀 때 0.2247 · 0.4142 를 그린다 | 자리: 흐름 밖: 입도 설계 (D0 침대 크기비 · Furnas dip) | 왜: 카드 §7-3 · p.1 (`txt_p1_void_1p1um_fill_smaller.png`) [인쇄 · 카드 산술]
- [m] ohsaki2021_… | **σ ↔ 입경 반례 한 점 기록 (판정 아님)** — 같은 측정 안의 서브 µm Li₃PS₄ 짝 93 ↔ 227 nm → σ 1.5 ↔ 1.1 × 10⁻⁴ S/cm (비 1.36) ↔ 우리 Cronau(r) (출처 없는 가정 · SELF-51) 비 0.351/0.542 = 0.65 [우리 산술] — 방향 반대 · 재료 · 상태 (분말 1 차 입자 · 응집 · 밀도 미보고) 가 달라 폼을 바꾸는 근거는 아님 | 자리: 흐름 밖: σ_ionic 폼 (Cronau(r_SE)) | 왜: 카드 §7-2 · 표 1 (`tab_1.png` · `txt_p5_table1_sigma_1e-4.png`) [인쇄 · 우리 산술]
- [m] ohsaki2021_… | **리뷰를 거친 값은 원 카드에서 다시 (함정)** — 리뷰 카드 (lei2026) 가 이 논문을 '1.32 µm' (원문 1382 nm) · 'Li₂S 크기와 선형' (원문 = 크기의 제곱과 선형) · 분포 'Narrow' (원문에 판정 없음 · PdI 1.000) 로 옮겼다 → 입도 문헌 지도의 값은 원 카드 대조 뒤에 쓴다 | 자리: 흐름 밖: 문헌 대조 규약 (단계 0) | 왜: 카드 §0-1 2 차 인용 표 [인쇄]

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] N.H.H. Phuc, K. Morikawa, T. Mitsuhiro, H. Muto, A. Matsuda, Synthesis of plate-like Li3PS4 solid electrolyte via liquid-phase shaking for all-solid-state lithium batteries, Ionics 23 (2017) 2061–2067. (ref [24]) | m · R6 — 원래 판상 LPS (≈3 µm × 500 nm) 와 LS 절차의 원전 · 표 1 '원래' 행의 치수 출처 · `kawaguchi2023_…` 도 [30] 으로 인용 — 카드 §12 | papers/ 목록 (phuc* 없음) · 'Ionics 23 (2017) 2061' grep = `kawaguchi2023_…` 가 인용만 → 카드 없음
- [n] S. Choi, S. Lee, J. Park, W.T. Nichols, D. Shin, Facile synthesis of Li2S-P2S5 glass-ceramics electrolyte with micron range particles for all-solid-state batteries via a low-temperature solution technique (LTST), Appl. Surf. Sci. 444 (2018) 10–14. (ref [26]) | m (σ ↔ 입경 대조의 기준값) — 표 1 원래 LPS σ 2.0 × 10⁻⁴ 의 출처 · 그림 2 의 LS 인용도 [26] (본문은 [24]) — 측정 조건을 봐야 '작아져도 σ 유지' 를 판정할 수 있다 — 카드 §3-7 · §12 | papers/ 목록 (choi2018 = 다른 논문 (FIB-SEM)) · 'Appl. Surf. Sci. 444' grep = 0 → 카드 없음
- [n] N.H.H. Phuc, K. Morikawa, M. Totani, H. Muto, A. Matsuda, Chemical synthesis of Li3PS4 precursor suspension by liquid-phase shaking, Solid State Ionics 285 (2016) 2–5. (ref [29]) | m (σ ↔ 입경 · 공정) — DMC 용매 LS 로 100–500 nm LPS 인데 σ 6.4 × 10⁻⁶ S cm⁻¹ (p.1 인용) — 서브 µm 에서 σ 가 낮은 반대 사례 · Cronau(r) 가정 대조의 두 번째 점 후보 — 카드 §3-5 · §12 | papers/ 목록 (phuc* 없음) · '285 (2016) 2' grep = 0 → 카드 없음

## 카드 문제
- `lei2026_se_particle_size_effects_review` **L58** (리뷰 ref [74] · [2차 · p.8]): *"→ Li₃PS₄ 1.32 µm (판상)"* ↔ 원문 **1382 nm** (= 1.38 µm · 표 1 · p.4 · [24] 치수 3 µm × 500 nm 에서 저자 계산) · *"Li₂S 크기와 선형 관계"* ↔ 원문 *"a linear relationship between the LPS particle size and the **square** of the Li2S particle size"* (p.5).  리뷰 원문 값인지 카드 전사인지는 이 카드로 못 가린다 (리뷰 PDF 대조 전) — 고치지 않았다.
- `lei2026_se_particle_size_effects_review` **L72** (리뷰 표 1 전사 · [인쇄 p.9]): *"원료 전처리 \| LPS \| 0.093 \| Narrow \| 0.15 \| Unfriendly \| [74]"* — 0.093 µm · 0.15 mS/cm 는 원문과 같다 · **'Narrow' (분포 폭) 와 'Unfriendly' (환경 영향) 는 원문에 없는 리뷰의 판정** (원문 SEM 93 ± 34 nm · DLS PdI 1.000 · Z-평균 6393 nm) — 카드 전사 문제 아님 · 리뷰 쪽 표지 후보.
- `yano2026_se_psd_width_ionic_tortuosity_dem` **L412** (ref 25): *"서브 µm SE 크기 제어 (밀링 없이)"* — 서지 ✓ · '밀링 없이' 는 SE 자체에만 맞다 (원료 Li₂S 를 습식 유성 볼밀하는 경로가 있고, 밀링 없는 경로는 용해–석출 하나) — 경미한 표현 한정.
- `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` L291 (ref 29) · L47 · L61 — 서지 · 역할 (그 논문 LPS 의 합성) · 몰비 (75 : 25 mol%) 원문과 같다 · 그 카드의 0.37 µm · 0.91 × 10⁻⁴ S/cm 는 그 논문 자체 측정 (이 논문 표 1 과 다른 시료) — 문제 아님.
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §3-7 에 적음): 그림 8 캡션 세 패널 ↔ 그림 두 패널 ↔ 본문 배정 · 그림 9 가로축 이름 (d²) ↔ 값 ((π/4)·d²) · 같은 숫자 0.34 ± 0.11 이 두 양 · 진탕 절차 인용 [24] (본문) ↔ [26] (그림 2 · 표 1 σ) · 오타 'AS impedance' · 'Cale–Cole' · 'diamter' · 'Rotaion'.
