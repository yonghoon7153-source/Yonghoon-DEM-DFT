# batch 116 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode` — K. Hayashi, T. Mori, K. Fukuda, H. Ito, Y. Manabe, "Application of Warm Isostatic Pressing to Densification of All Solid-State Composite Cathode Electrodes in All Solid-State Lithium-Ion Batteries", J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173 (Vol. 72 Supplement), doi:10.2497/jjspm.16C-SIS6-03 (본문 7 쪽 · 보충 자료 · 표 · 식 없음 · 카드 = `litdb/papers/hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode.md` · 후보 표 N-64).
LiNbO₃ 코팅 NCM111 + Li₆PS₅Cl + 아세틸렌 블랙 + 바인더를 슬러리로 Al 박에 발라 말린 양극 시트 (74 : 23 : 3 wt% · ≈170 µm) 를 **600 MPa 한 압력**으로 등방 가압 (WIP) 하며 온도 (상온 · 100 · 150 · 190 °C) 와 유지 시간 (1 · 30 · 60 s) 만 바꾼 실험 논문이다.  구조 값은 전부 **압력을 뺀 뒤** 싱크로트론 CT (화소 0.65 µm) 의 "void ratio" (= 기공 + 탄소 복셀 분율) 와 두께.  계산 (DEM · MPM · FEM) · 압력 축 · 단축 가압 대조 · 순수 SE · 질량 / 진밀도 기공 · 탈압이 없다 — 아래 '없음' 은 그 때문이다.  **방향과 측정 꼴은 옮길 수 있고 값은 옮길 수 없다.**

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (순수 SE 의 기공 · 밀도 측정 없음 — 분리막 펠릿은 *"formed by uniaxial press at 600 MPa"* · 두께 600 µm 한 줄뿐 · 밀도 미기재 · 카드 §3-9).  참고로만: 서론의 2 차 인용 *"the relative density of 75Li2S-25P2S5 exceeded 90% when compressed at pressures over 350 MPa"* (p.1 · ref 10 = Sakuda 2013) 은 정본 `sakuda2013_sulfide_mechanical_property` 의 [인쇄] 값과 같다 (카드 §12) — 이 논문의 측정이 아니다.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (모든 구조 값이 감압 뒤 한 상태 — CT 시료는 ⌀0.8 mm 유리 모세관 속 · 가압 중 값이 없어 되돌아온 양을 알 수 없다 · 감압 속도 미기재 · 카드 §4-4 (4)).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 물성 값 **없음** (항복 · 경도 · 크리프 · 온도 의존 탄성 — 저자: *"the mechanical properties of the SE should be clarified, which will be an extension of the present work"*).  시간 의존의 간접 관측만: 600 MPa · 100 °C 에서 유지 1 → 30 → 60 s 에 보이는 기공 0.087 → 0.036 → 0.029 (두께는 94.5 · 99.0 · 97.5 µm 로 그대로) | 카드 §3-5 · 논문 p.5 · Fig. 8 | [판독 · 벡터] · 인용문 [인쇄] | 시료 하나씩 · 승압 시간 미기재 · 전체 기공의 감소인지 기공 크기의 재분배인지 미정 · 일축 항복 세기와 견줄 환산 없음
- [c] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 온도 의존 (600 MPa · 60 s): 보이는 기공 0.057 (상온) → 0.042 (100 °C) → 0.039 (150 °C) · 두께 103.0 → 97.5 → 94.7 µm · 저자 해석 *"a softening of the SE, resulting in increased fluidity and enhanced movement of particles during WIP"* | 카드 §3-4 · §3-8 · 논문 p.3 · p.5 · Fig. 3 | [판독 · 벡터] · 해석문 [인쇄] | 추론 (물성 측정 없음) · 3 점 · 190 °C 는 사진뿐

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 하중 몫 수치 **없음** — 정성 서술: *"This indicates that densification was interrupted due to contact with each AM particle."* · *"many voids remained in the SE because the contact of the AM particles resulted in releasing applied pressure in the surroundings"* (600 MPa · 100 °C · 1 s 시료) | 카드 §0 ⑨ · §3-5 · 논문 p.5 | [인쇄] (저자 추론 · 응력 측정 아님) | 등방 가압 · 바인더 시트 · AM ≈50 vol% [카드 산술] · 근거는 "두께가 1 s 에 끝남 + 1 s 의 AM 배치가 60 s 와 비슷" 뿐
- [d] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 가압 전후 AM 기둥 (범주 그림의 AM 면적 분율 × 두께) = 50.4 (가압 전) · 46.7 · 52.2 · 51.2 · 47.0 µm → 49.5 ± 2.5 µm 로 보존 · 기공 + 탄소는 SE 영역 안에 남는다 (본문 *"The reduction of voids primarily occurred in the SE region"*) | 카드 §3-6 · 논문 p.2 · Fig. 2 · 9 | [판독] + [카드 산술] | 조건마다 표시 단면 한 장 · 면적비 = 부피비 가정

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙 · 입자 계산 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  영상 해상도 참고: 유효 화소 0.65 µm · SE 입자 "수 µm" (지름당 화소 ≈3–8 [카드 산술]) — 이 해상도에서 가압 전 SE 알갱이 사이 기공은 "SE 갈래" 에 묻힌다 (카드 §3-6).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 원문의 말은 없음.  판독 증거: 표시된 2D 범주 단면의 검정 (기공 + 탄소) 면적 분율 0.197 · 0.063 · 0.086 · 0.048 · 0.041 이 3D 복셀 값 0.191 · 0.057 · 0.087 · 0.042 · 0.039 와 ±0.006 안에서 같다 (다섯 시료) | 카드 §3-6 · Fig. 2 · 9 ↔ Fig. 3 · 8 | [판독] | 같은 CT 자료의 단면 ↔ 부피 (영상 내부 일관성) — 2D 계산을 3D 로 옮기는 근거는 아니다

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (계산 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | **압력별 값은 없다** (600 MPa 하나 — *"the process pressure was set at 600 MPa"* · *"WIP was conducted at 600 MPa for all experiments"*).  있는 것 = 등방 600 MPa · 감압 뒤의 온도별 값: void ratio (기공 + 탄소 복셀 분율 · 화소 0.65 µm) 가압 전 0.191 → 상온 0.057 → 100 °C 0.042 → 150 °C 0.039 · 두께 169.3 → 102.97 → 97.46 → 94.74 µm | 카드 §0 조건별 표 · §3-4 · 논문 p.2 · p.3 · Fig. 3 · 8 | void ratio · 두께 표지 [판독 · 벡터] · 본문 "≈170 → ≈104 → 94 µm" · "around 0.04" [인쇄] | 진밀도 · 질량 기준 아님 · 탄소 포함 · 시료 하나씩 · NCM111 + LPSCl 74 : 23 : 3 wt% 슬러리 시트 · 등방
- [i] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 유지 시간별 (600 MPa · 100 °C): 1 s 0.087 · 94.5 µm → 30 s 0.036 · 99.0 µm → 60 s 0.029 · 97.5 µm | 카드 §3-5 · 논문 p.5 · Fig. 8 | [판독 · 벡터] · "95 µm" [인쇄] | 같은 조건 (100 °C · 60 s) 값이 Fig. 3 에서는 0.042 — 재현 폭 ≥ ±0.007
- [i] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 이 void ratio 는 전체 기공이 아니다: (1 − void)·t = 137.0 (가압 전) → 97.1 · 86.3 · 95.4 · 93.4 · 91.1 µm 로 보존되지 않고, 두께 감소 (−39.2 … −44.2 %) 가 요구하는 가압 전 기공은 ≥ 0.39–0.44 (CT 는 0.19) | 카드 §3-6 | [카드 산술] (가정: 면적 · 고체 보존) | 원문 값 아님 — 연산자 경고용

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 원문이 적은 한계: (1) WIP 의 치밀화 기전과 공정 압력 · 온도의 영향은 *"still an open question"* (p.1) (2) *"Voids and carbon-related materials were not distinguished"* (p.2) · 0.04 는 *"within the resolution of the CT measurements"* (p.3) (3) 두께는 *"within the variation of sample preparation"* 만큼 흔들린다 (p.5) (4) *"the mechanical properties of the SE should be clarified"* (p.5) | 카드 §3-10 | [인쇄] | —
- [j] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 카드가 적은 한계: 압력 축 · 단축 대조 · 가압 중 상태 · 탈압 · 질량 / 진밀도 · 로딩 · 입경 수치 · 응력 · 물성 · 수송 지표 없음 · 시료 하나씩 (같은 조건 0.042 ↔ 0.029) · 190 °C 는 사진뿐 · 고온의 화학 변화 미확인 · EIS 맞춤값 미인쇄 · "두 단계" 의 둘째 단계가 전체 기공 감소인지 미정 | 카드 §11 · §13 | [카드 해석] · [미확인] | —

## k — DEM 의 한계
- [k] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode (Hayashi 외, J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173) | **말 없음** — DEM 을 쓰지 않는 실험 논문이고 DEM · simulation · model 낱말이 본문에 없다 | 카드 §4-4 (1) | — | —
- [k] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode (Hayashi 외, J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173) | 구가 변하지 않는 DEM 이 담지 못하는 것의 **실측 사진** (모델에 대한 말은 아님): 상온 600 MPa 등방 뒤에는 *"most AM and SE particles remained isolated, with boundaries between adjacent AM similarly observed"* 인데 190 °C 에서는 *"the SE particles coalesced to form large particles without boundaries"* · 그리고 두께가 그대로인 채 보이는 기공이 유지 시간과 함께 준다 (0.087 → 0.029 · 1 → 60 s) | 카드 §3-5 · §3-8 · 논문 p.5 · Fig. 6 · 8 | 인용문 [인쇄] · 값 [판독] | cryo-FIB 단면 SEM 한 시야씩 · 정량 없음 · 등방 · 승온

## l — 소성변형이 왜 어려운가
- [l] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode (Hayashi 외, J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173) | **말 없음** — 계산이 없어 소성을 넣기 어려운 이유 · 우회 · 맞춘 값 · 비용에 대한 논의가 없다.  관측과 저자 해석만: 치밀화가 (i) 순간 단계 (AM 접촉에서 멈춤) 와 (ii) 등방압 아래 서서히 진행되는 단계로 나뉘고 (*"suggesting a two-step process"*), 온도를 올리면 SE 가 물러져 (*"a softening of the SE, resulting in increased fluidity"*) 입자가 더 움직인다 — 확인에는 SE 의 기계 물성이 필요하다고 스스로 적는다 | 카드 §3-5 · §3-8 · §4-4 (2) · 논문 p.5 | [인쇄] | 시간 · 온도 의존 유동은 속도 무관 소성 (우리 MPM) · 탄성-이력 접촉 (우리 DEM) 에 없는 축 [카드 해석]

## m — 받아들일 통찰
- [m] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 무엇을: **영상 기공은 '무엇을 한 갈래로 셌는지' 와 '기둥 보존' 을 같이 본다** — 이 논문의 void ratio 는 기공 + 탄소 갈래 (바닥 0.04 ≈ 탄소 + 바인더의 부피 몫 0.05 [카드 산술]) 이고, AM 기둥 (분율 × 두께) 은 49.5 ± 2.5 µm 로 보존되는데 (1 − void)·t 는 137 → 86–97 µm 로 준다 → 가압 전 CT 0.19 ↔ 두께 하한 ≥ 0.39–0.44 | 우리 쪽 어디에: 단계 0 (연산자 표에 '탄소 포함 여부 · 기둥 보존 검사' 칸) ; 결과 전 대조 항목 ; 흐름 밖: MPM 복셀 · STEP3 pore 지표를 CT 와 견줄 때 탄소 상을 기공과 합쳐 다시 세기 | 왜: 카드 §3-3 · §3-6 (Fig. 2 · 3 · 8 판독 + 산술)
- [m] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 무엇을: **복합 압밀 결과의 자체 검사 꼴 — 세 갈래 (AM / SE / 기공) 단면 + AM 기둥 보존 + '남은 기공이 어느 상 옆에 있나'** : 이 논문에서 변형은 두께 방향뿐이고 (봉지 속 유체 압력인데도) 기공은 SE 영역에 남는다 → 시트 + 등방압 ≈ 일축 변형 + 균일 수직 압력 경계 [카드 해석] | 우리 쪽 어디에: 단계 5 ; 단계 7 ; 후보 A′-0 ; 조건 R1 | 왜: 카드 §3-6 · §8 (Fig. 2 · 9 판독 · p.2 본문)
- [m] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 무엇을: **함정 — "유지 시간이 길면 기공이 준다" 를 두께 없이 믿지 않는다**: 1 → 60 s 에 보이는 기공은 5.9 %p 줄었는데 두께는 94.5 → 99.0 → 97.5 µm 로 줄지 않았다 (줄었다면 ≈5.5 µm [카드 산술]) → 시료 산포이거나 큰 기공이 해상도 아래로 나뉜 것 · 그리고 같은 조건의 값이 두 그림에서 0.042 ↔ 0.029 | 우리 쪽 어디에: 단계 5 · 조건 R6 의 한정어 (우리 DEM · MPM 에 시간 · 온도 축 없음 — 재현 표적으로 삼지 않는다) ; 흐름 밖: 실험 원측정을 받을 때 두께 + 질량 + 진밀도 + 압력 상태를 같이 | 왜: 카드 §3-5 · §7-3 (Fig. 3 · 8 벡터 판독)
- [m] hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode | 무엇을: **EIS 호가 줄 때 '면적이 는 것' 인지 가리는 법 — 봉우리 주파수 (시간 상수) 가 그대로인지 본다**: 호 폭 ≈123 → 75 → 64 Ω 인데 위상 봉우리는 세 시료 모두 1.3–1.5 × 10⁴ Hz → R·C ≈ (2.4–2.9) × 10⁻⁵ s 로 일정 = 닿은 면적이 는 꼴 | 우리 쪽 어디에: 흐름 밖: Rint ② (계면 저항 ↔ 접촉 면적) · 단계 7 | 왜: 카드 §3-9 (Fig. 5 판독 + 산술 · 원문은 맞춤값을 인쇄하지 않았고 호의 귀속은 ref 16 인용 하나)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Y.-G. LEE, S. FUJIKI, C. JUNG, N. SUZUKI, N. YAHIRO, R. OMODA, D.-S. KO, T. SHIRATSUCHI, T. SUGIMOTO, S. RYU, L. H. KU, T. WATANABE, Y. PARK, Y. AIHARA, D. IM, I. T. HAN: Nat. Energy, 5 (2020) 299–308. | i · b · 단계 5 — WIP 를 쓴 ASSB 의 원전 (이 논문 서론: *"over 900 Whl-1 by using WIP … improved the contact properties"* · `minnmann2021_jes_charge_transport_bottlenecks` 는 "WIP 로 한 자릿수 기공" 으로 2 차 인용) — WIP 조건 · 기공 값의 원문 확인 ([13] · 카드 §12) | litdb 확인: ls 'lee2020' 없음 · grep '299–308' · 'Nat. Energy 5' = 인용만 (cronau2022 · minnmann2021 · 이 카드) → 카드 없음
- [n] K. HAYASHI, T. MORI, K. FUKUDA: SPring-8/SACLA Research Reports, 10 (2022) 471–477 (in Japanese). | i · 단계 0 — 같은 저자들의 앞선 CT 보고 — 이 논문에 없는 분석 조건 (분석 부피 · 문턱 · 두께 재는 법) 과 다른 압력 조건이 있을 수 있다 ([14] · 카드 §12 · §13 의 [미확인] 6 · 7 · 11 을 메울 후보) | litdb 확인: ls 'hayashi' = 이 카드뿐 · grep 'SPring-8/SACLA Research Reports' = 이 카드뿐 → 카드 없음
- [n] Y. MORINO: Electrochem. 90 (2022) 027001 (4 pages). | 흐름 밖 (Rint ② · EIS 해석) — 이 논문이 고주파 호를 "전하이동" 에 귀속한 유일한 근거 ([16] · 카드 §3-9 · §11-6) | litdb 확인: ls 'morino' 없음 · grep '027001' = 이 카드뿐 → 카드 없음
- [n] B. D. L. CAMPÉON, H. B. RAJENDRA, N. YABUUCHI: ChemSusChem, 17 (2024) e202301054 (12 pages). | i · 후보 A′-0 — HIP · CIP 가 ASSB 부품 치밀화에 쓸 만하다는 근거로 인용 — 등방 가압의 압력 · 밀도 자료 가능 ([11] · 카드 §12) | litdb 확인: ls 'campeon' 없음 · grep 'e202301054' = 이 카드뿐 → 카드 없음
- (참고 · 후보로 세지 않음) [15] W. CHOI 외, ACS Appl. Mat. Interfaces 16 (2024) 26066–26078 = 정본 `interfacial_impedance_formulation_assb_cathode` · [10] Sakuda 2013 = `sakuda2013_sulfide_mechanical_property` · [9] Froboese 2019 = `froboese2019_microstructure_ionic_conductivity_assb_electrode` · [6] Deiseroth 2008 · [4] Kamaya 2011 — 카드 있음.  [12] M. DIXIT 외, ACS Energy Lett. 7 (2022) 3936–3946 = 정본 `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` (같은 날 후보 N-63 으로 들어옴 — 이 작업의 push 직전 원격 끝에서 확인해 후보에서 뺐다 · 그 카드의 답: 같은 압력의 단축 ↔ 등방 대조 값 없음 · 황화물 SE 등방 밀도 자료 0 건).
- push 직전 다시 본 결과 (정본 `litdb/papers/` 534 장): 위 네 후보 (lee2020 · hayashi2022 · morino2022 · campeon2024) 의 카드는 여전히 없다.  Lee 2020 은 `dixit2022_…` 카드 §12 에도 "없음" 후보로 올라 있다 (그 카드의 [69] · LPSCl 계 파우치 셀 WIP 490 MPa) — 두 정독이 같은 문헌을 가리킨다.

## 카드 문제
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L439 — 서지 (저자 다섯 · 제목 · 권 72 · 2025 · S1167–S1173 · DOI) 와 한 줄 요약 *"WIP 복합 양극 치밀화 (계면 · 전하이동 저항 감소의 선행)"* 은 원문과 **같다** → 내용 문제 없음.  두 가지만 적는다: (i) 그 줄의 학술지 이름 *"粉体および粉末冶金"* 은 이 PDF 에 인쇄되어 있지 않다 (원문 인쇄 = *"J. Jpn. Soc. Powder Powder Metallurgy"* · 쪽 아래 *"Journal of the Japan Society of Powder and Powder Metallurgy" Vol. 72 Supplement*) — benhadjali 원문 목록의 표기를 옮긴 것으로 보이고 오류는 아니다 (ii) 그 줄의 *"카드 없음"* 은 이 카드가 생겨 낡았다 (그 카드는 고치지 않았고 "🔗 관련 카드" 에 한 줄만 더했다).
- 후보 표 N-64 의 '왜' 칸 *"압력별 기공 값이 있는지는 [미확인]"* → 원문 확인 결과 **없음** (압력 600 MPa 하나 · 온도 · 유지 시간 축만 · 단축 가압 대조도 없음).  *"단계 5 (결과 전 대조 후보)"* 는 **일부** 만 채운다 (등방 · 600 MPa · 바인더 시트 · 영상 갈래 분율이라 방향 항목으로만).  후보 표는 고치지 않았다 (메인 세션 소관).
- 도구 메모 (카드 문제 아님 · 보고용): `tools/litdb/extract_figures.py --slug … --clean` 을 돌리면 `litdb/figures/_sources.json` 을 전부 다시 써서 **다른 카드** (`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`) 의 PDF 이름 줄이 바뀐다 (그 카드 figures.json 의 sources 글자와 커밋된 `_sources.json` 이 다르다) — 이번에는 그 줄을 되돌리고 이 카드 항목 7 줄만 손으로 넣었다 (README 2 절).  이 학술지 조판에서는 도구가 그림 9 장 가운데 2 장만 뽑는다 (그림이 캡션까지 빈 줄로 이어진 긴 글 블록 안에 있어 '영역 없음' · '그래픽 없음') — 7 장을 손으로 잘랐다.
