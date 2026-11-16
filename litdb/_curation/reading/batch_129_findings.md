# batch 129 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-80)

대상: `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` — A. Sakuda · A. Hayashi · T. Ohtomo · S. Hama · M. Tatsumisago\*, "All-solid-state lithium secondary batteries using LiCoO2 particles with pulsed laser deposition coatings of Li2S–P2S5 solid electrolytes", *J. Power Sources* **196** (2011) 6735–6741 · DOI 10.1016/j.jpowsour.2010.10.103 (온라인 2010-11-09 · PDF 문서 정보의 '(2010)' 은 온라인 연도 · 인쇄 권호 연도 2011 · SI 없음).
LiNbO₃ 선코팅 LiCoO₂ (D-10 · ca. 10 µm) 위에 80Li₂S·20P₂S₅ 를 PLD 로 입혀 (진동 유동화 · 상온 · Ar 5 Pa · 10–120 min) SE 입자 없이 / SE 입자 10 wt% 를 더해 360 MPa In 반쪽 셀을 만들고, 막 양 · 막 열처리 (200 °C) · SE 입자 양에 따른 용량 · EIS 계면 저항 · 압분 단면 (FIB HAADF-STEM/EDX · 450 사이클 뒤) 을 본 실험 논문 — DEM · MPM · 계산 없음 · 기공 · 밀도 · 압력 곡선 · 탈압 없음.
쪽 = 인쇄 쪽 p.6735–6741 (PDF 쪽 = 인쇄 − 6734) · 판독 원자료 = `litdb/figures/sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode/digitized.csv` (2,292 행 · 벡터 경로) · 고른 의도 대조 = **일부** (카드 §0-1 — PLD SE 코팅은 채움 · 코어–쉘 선행은 구조로 채움 (낱말 없음 · 첫 보고는 [28] · 2 차 입자 뭉침) · DOE 수준은 Xs 0.1 / 0.3 · 360 MPa 만 (180 MPa · 체결 토크 없음)).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 의 기공 · 밀도 · 압력 의존이 없다.
- [a] sakuda2011_pld_sulfide_se_… | (참고 · 곡선 아님) 분리막 = 80Li₂S·20P₂S₅ 유리-세라믹 80 mg · φ 10 mm · 360 MPa → 101.9 mg/cm² | 카드 §3-3 · p.6737 (`txt_p6737_cell_90_10_bilayer_360mpa.png`) | [카드 산술] (인쇄 질량 · 지름) | 두께 · 진밀도 미인쇄 → 기공 계산 불가 · LPSCl 아님 · 랩 표준 (10–13 % · 1.64 g/cm³) 옆에 놓을 숫자 없음

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 하중 해제 · 되돌아옴 측정 없음 (셀은 스테인리스 봉으로 누른 펠릿 · 운전 적층압 [미확인]).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 막 · SE · LiCoO₂ 의 기계 물성 값 없음.  정성 문장만 (냉간 가압으로 막이 *"connected"*) — 질문 l 에 옮김.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] sakuda2011_pld_sulfide_se_… | (정성) SE 가 PLD 막 ≈1 wt% 뿐인 LiCoO₂ 압분체 (360 MPa · 450 사이클 뒤 단면) 에서 *"the LiCoO2 particles were closely packed in the composite electrode"* · 각진 입자가 면을 맞대고 막이 틈을 차지 · *"Some voids at the interfaces"* | 카드 §3-9 · §7-4 · p.6738 · 그림 3 (`fig_3.png` · `txt_p6738_tem_closely_packed_cold_pressing_voids.png`) | 인쇄 (원문 문장) + [판독 · 영상] | 하중 · 응력 · 배위수 · 기공 측정 없음 · 'AM 이 하중을 받았다' 는 [카드 추론] · 2D 단면 한 장 · LiCoO₂ ≠ NCM

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).  해상도에 쓸 기하만 있다 — 막 두께 / 입자 지름 ≈0.5–0.7 % (질문 m ①).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산이 없고 영상은 2D (분말 SEM · FIB 단면 TEM) 뿐 · 3D 재구성 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 압력 한 값 (360 MPa) · 기공 · 밀도 · 두께 미인쇄.
- [i] sakuda2011_pld_sulfide_se_… | (참고 · 기공 아님) 작업 전극 10 mg · φ 10 mm → 12.73 mg/cm² · 조성 = 코팅 LiCoO₂ 만 (SE 막 ≈1–3 wt%) · 90 : 10 · 이전 보고 70 : 30 · 서론 *"approximately 20–30 wt.% [27]"* | 카드 §3-3 · §0-1 · p.6736–6737 | [카드 산술] (부하) · 인쇄 (조성) | 기공 계산 불가 · 압력 의존 없음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] sakuda2011_pld_sulfide_se_… | 막만 있는 전극은 *"the capacities of these all-solid-state cells remained smaller than the 95 mAh g⁻¹ typical of … 70 wt.% LiNbO3-coated LiCoO2 … and 30 wt.% SE particles"* | 카드 §3-6 · p.6739 (`txt_p6739_reference_70_30_95mah.png`) | 인쇄 | 원인 (막 양 · 막 σ · 뭉침) 을 가르지 않음
- [j] sakuda2011_pld_sulfide_se_… | 압분 단면의 *"Some voids at the interfaces between LiCoO2 particles"* — *"This could be reduced using LiCoO2 with larger amounts of SE coating"* (120 min 막 = 40 min 의 3 배 · 예상만 · 그 단면 없음) | 카드 §3-9 · p.6738 | 인쇄 (예상 문장) | 가압 접촉의 불완전성 · 공극 양 측정 없음
- [j] sakuda2011_pld_sulfide_se_… | 이전 판 [28] 은 *"limited to 30 mAh g⁻¹, and this low cell capacity required improvement"* | 카드 §3-4 · p.6736 (`txt_p6736_se_20_30wt_prior_pld_30mah.png`) | 인쇄 | —

## k — DEM 의 한계
- [k] sakuda2011_pld_sulfide_se_… (Sakuda · Hayashi · Ohtomo · Hama · Tatsumisago 2011, J. Power Sources 196, 6735–6741) | **말 없음** — DEM · 시뮬레이션이 없다.  DEM 의 '단단한 구 · SE 를 구로 둠' 과 맞닿는 실험 사실만 있다: ① 실제 LiCoO₂ 는 각진 입자이고 압분 뒤 *"closely packed"* (면 맞댐 · 그림 2 · 3) ② SE 가 막 (≈1–3 wt%) 으로만 있어도 이온 경로가 이어져 용량이 0 → 15 · 35 · 65 mAh/g (그림 4 · p.6739 *"an SE coating on LiNbO3-coated LiCoO2 enabled the formation of a lithium-ion conducting path to the LiCoO2 particles"*) — SE 를 구로만 두는 모델은 이 양을 '흩어진 구' 로밖에 못 나타낸다 [카드 추론] | 카드 §4-4 · §7-3 · p.6737–6739 | 인쇄 + [카드 추론] | DEM 한계의 직접 진술로 쓰지 않는다 (논문은 DEM 을 말하지 않음) · LiCoO₂ · 80Li₂S·20P₂S₅

## l — 소성변형이 왜 어려운가 · 우회 · 비용
- [l] sakuda2011_pld_sulfide_se_… (Sakuda · Hayashi · Ohtomo · Hama · Tatsumisago 2011, J. Power Sources 196, 6735–6741) | 소성 계산의 어려움 · 우회 · 비용에 대한 말 없음 (계산 없음).  소성의 **실험 결과** 문장만: *"The all-solid-state cell was prepared by cold pressing. As a result of this pressing, the LiCoO2 particles packed closely in the composite electrode layer and the SE coating deposited on the LiCoO2 particles was connected to form the all-solid-state cell. As a result, a favorable SE region was formed in the interfacial space between the LiCoO2 particles."* | 카드 §3-9 · §4-4 · p.6738 (`txt_p6738_tem_closely_packed_cold_pressing_voids.png`) | 인쇄 (원문 문장) | 막의 변형량 · 기계 물성 · 압력 의존 없음 · 같은 SE 의 상온 가압 소결은 정본 `sakuda2013_sulfide_mechanical_property` 쪽 (그 카드 표지)

## m — 받아들일 통찰
- [m] sakuda2011_pld_sulfide_se_… | ① **해상도 규칙 = 껍질 두께**: 막 50–70 nm / 입자 ca. 10 µm → t/d ≈0.5–0.7 % · 막에 칸 2 개면 지름당 286–400 칸 · 3D 입자 하나에 2.3–6.4 × 10⁷ 칸 · 우리 MPM real_14 격자 (dx 141 nm · CLAUDE.md) 로는 막 = 0.35–0.50 칸 → 코팅 활물질의 껍질은 격자로 풀지 말고 **접촉 단위 성질** (AM–AM 접점의 SE 막 전도 · 계면 저항 항) 로 넣는다 · 자리 = 단계 1 · U1 · 후보 A′-0 · A · A′ · 흐름 밖: 믹서 Ⓒ | 카드 §3-2 · §7-3 · §8 · p.6737 | [카드 산술] (인쇄 두께 · 지름) | 50–70 nm 는 이전 보고 [28] 의 TEM 값 · 20–40 min 은 입자 뭉침
- [m] sakuda2011_pld_sulfide_se_… | ② **결과 전 대조 (정성)**: SE 막 ≈1–3 wt% (매끈한 구 기하 3–13 vol% of LiCoO₂ [카드 산술]) 만으로 이온 경로가 이어진다 (용량 15–65 mAh/g · 비코팅 0) · 막 (20 min) + SE 입자 10 wt% = SE 입자 30 wt% 혼합 (95 mAh/g) → 우리 DEM σ_ion (SE = 구) 은 막을 '흩어진 구' 로 두어 경로 없음 쪽으로 간다 · σ_ionic 폼 문턱 φc 0.195–0.200 은 막에 적용되지 않는다 [카드 추론] · 자리 = 결과 전 대조 항목 · 후보 D0 · 단계 7 · 흐름 밖: 믹서 Ⓒ | 카드 §0 · §3-4 · §3-7 · §7-3 · p.6739–6740 | 인쇄 + [카드 산술 · 추론] | LiCoO₂ · 80Li₂S·20P₂S₅ · 360 MPa · 셀 하나씩
- [m] sakuda2011_pld_sulfide_se_… | ③ **보고 규약 (분모 · 인쇄 ↔ 그림)**: 같은 셀이 활물질 기준 95 ↔ 복합체 기준 86 mAh/g · 보통 70 : 30 은 95 ↔ 67 · 막-전극은 두 분모가 같다 (65 · 69 ≈ 67 [카드 산술]) — '코팅 이득' 크기가 분모에 걸린다 · 그림 8 방전 끝 16.4 · 58.1 · 91.9 [판독] ↔ 본문 20 · 60 · 95 (2–3.6 mAh/g 차) → 인용할 때 분모 · 인쇄값 · 판독값을 함께 적는다 · 자리 = 단계 0 · 흐름 밖: 문헌 인용 규약 | 카드 §3-4 · §3-7 · §11 · p.6739–6740 | 인쇄 + [판독 · 벡터] + [카드 산술] | 원문은 어긋남을 설명하지 않음
- [m] sakuda2011_pld_sulfide_se_… | ④ **Rint ② 방향 대조**: SE 입자 10 wt% 의 비코팅 LiCoO₂ 계면 저항 ca. 850 Ω ↔ 30 wt% ca. 300 Ω (2.83 배 · 면적 저항 667.6 ↔ 235.6 Ω·cm² [카드 산술]) — 저자 해석 = LiCoO₂–SE 접촉 면적 · LiNbO₃ ≈60 · SE 막 ≈30 Ω [판독] → '계면 저항 ∝ 1/접촉 면적' 의 방향 기준 (맞춤 표적 아님 — 다른 논문 셀끼리 · 등가 회로 없음 · 축 눈금 다름) · 자리 = 흐름 밖: Rint ② · 단계 7 | 카드 §3-8 · p.6740 (`txt_p6740_eis_850_vs_300_ohm_contact_area.png` · `fig_7.png`) | 인쇄 + [판독] + [카드 산술] | 면적은 재지 않았다

## n — 논문 에이전트 후보 (원문 참고문헌 목록 서지 그대로 · papers/ 목록 + grep 으로 카드 없음 확인)
- [n] [28] A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, Electrochem. Solid-State Lett. 13 (2010) A73–A75. | 의도 (코어–쉘 선행) · m ① — **PLD SE 코팅의 첫 보고** · 막 두께 50–70 nm 의 단면 TEM 원자료 · 40 min 셀 100 사이클 (카드 §0-1 · §3-2 · §12) | papers/ 에 sakuda2010 없음 (sakuda* = sakuda2013 하나) · 'A73' · 'Solid-State Lett. 13' grep 0 건
- [n] [29] A. Sakuda, A. Hayashi, S. Hama, M. Tatsumisago, J. Am. Ceram. Soc. 93 (2010) 765–768. | m ① · ② — PLD 80Li₂S·20P₂S₅ 막 σ 7.9 × 10⁻⁵ S/cm 와 200 °C 열처리 뒤 σ (껍질 전도 입력) (카드 §3-1 · §12) | papers/ 에 없음 · '765–768' · 'Ceram. Soc. 93' grep 0 건
- [n] [27] F. Mizuno, A. Hayashi, K. Tadanaga, M. Tatsumisago, J. Power Sources 146 (2005) 711–714. | i — 복합 전극 SE 20–30 wt% 필요의 출처 (조성 설계 · DOE 수준 Xs 0.3 의 뿌리) (카드 §0-1 · §12) | papers/ 에 mizuno 없음 · '711–714' grep = kawaguchi2018 이 인용만
- [n] [25] A. Sakuda, H. Kitaura, A. Hayashi, K. Tadanaga, M. Tatsumisago, J. Electrochem. Soc. 156 (2009) A27–A32. | m ④ — '이전 결과 ca. 300 Ω' (SE 30 wt%) 의 출처 셋 가운데 하나 · Li₂O–SiO₂ 코팅 (같은 출처 [24] ESL 11 (2008) A1–A3 · [26] J. Power Sources 189 (2009) 527–530) (카드 §3-8 · §12) | papers/ 에 없음 · '156 (2009) A27' grep = kawaguchi2023 이 인용만
- [n] [18] A. Sakuda, A. Hayashi, M. Tatsumisago, Chem. Mater. 22 (2010) 949–956. | m ④ · 흐름 밖 (계면) — LiCoO₂–Li₂S–P₂S₅ 계면 열화가 고저항의 원인이라는 저자 믿음의 출처 (p.6735) (카드 §12) | papers/ 에 없음 · '949–956' grep = kawaguchi2018 이 인용만

## 카드 문제
- `kawaguchi2017_dry_coating_parametric_na2so4_model_se` **L234**: *"정본 카드는 그 셀 양극을 "PLD 코팅 LiCoO₂ · 무탄소 (80:20)" 로 적는다"* — 지금 `sakuda2013_sulfide_mechanical_property` 카드는 **90 : 10** 이다 (그 카드 L82 *"양극 LiCoO₂ : SE 막 ≈ 90 : 10 … 이전 판 '양극 80:20' 오기 정정 2026-10-21"* · L248) → 낡은 교차 인용.  이 논문 (Kawaguchi 2017 의 [15]) 쪽에서 '10 wt%' 는 PLD 막 (≈1–3 wt%) 위에 **더 섞은 SE 입자** 의 몫이다 (p.6737 · p.6740).  고치지 않음.
- `kawaguchi2017_dry_coating_parametric_na2so4_model_se` **L114**: *"10 wt% 로 코팅한 것은 PLD (Sakuda, ref 16) 뿐"* — 이 논문 기준으로는 PLD 막이 ≈1–3 wt% 이고 10 wt% 는 SE 입자다 ('10 wt% 로 코팅' 과 다름).  그 문장의 귀속 (ref 16 = Sakuda 2013) 이 맞는지는 Kawaguchi 2017 원문 · Sakuda 2013 원문 대조 전 [미확인].  고치지 않음.
- `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` **L87 · L284**: *"수준 범위 = 기존 연구 [11,19] 의 조건"* · *"DOE 수준 범위의 근거"* — [19] (= 이 논문) 이 주는 것은 Xs 0.1 (90 : 10) · Xs 0.3 (이전 보고 70 : 30) · P 360 MPa 뿐 · **180 MPa · 체결 토크 0.5 / 2.5 N·m 는 이 논문에 없다** (원문 압력 = 360 · 240 (In 박) MPa · 셀 = 스테인리스 봉).  Kawaguchi 2023 원문 서술을 옮긴 줄이라 카드 오류는 아니나, 이 논문을 180 MPa · Ts 수준의 근거로 인용하면 안 된다.  고치지 않음.
- `nakamura2020_dry_coating_ncm_li3ps4_core_shell` **L338** · `kawaguchi2017_*` **L233** · `kawaguchi2018_dry_coating_model_se_particle_powtec` **L381**: 서지 · 'PLD SE 코팅' 서술 모두 원문과 같음 — 문제 없음 ('코어–쉘' 낱말은 원문에 없지만 구조 서술로는 맞다 · kawaguchi2018 의 *"lab-scale … scale-up is impractical"* 은 Kawaguchi 쪽 평가 · 이 논문에 규모 말 없음).
