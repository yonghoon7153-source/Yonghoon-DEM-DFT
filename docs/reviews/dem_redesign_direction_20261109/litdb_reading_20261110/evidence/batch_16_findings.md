# batch_16 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `duquesnoy2020_calendering_ml_mesostructure_generator` (510 줄) · `froboese2019_microstructure_ionic_conductivity_assb_electrode` (466) · `galvezaranda2024_time_dependent_dl_calendering_microstructure` (733) · `hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd` (476) · `hlushkou2018_void_space_ion_transport_assb_cathode` (391) · `holzer2013_constrictivity_effective_transport_porous_layers` (382) · `islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell` (138). 끝까지 못 읽은 카드 없음 (일곱 장 모두 한 – 다섯 번에 나눠 마지막 줄까지 읽음).

배치의 성격: 수송 · 미세구조 묶음이다. **실험 하나** (froboese2019 = 고분자 SE + 유리구 모델 전극의 기공 · 이온전도), **실험 + 복셀 계산 하나** (hlushkou2018 = LPSI 유리 + LCO 복합 양극의 EIS 와 FIB-SEM 재구성 위 확산), **실험 + 영상 분석 · 정의 하나** (holzer2013 = 액체 격막 · SOFC 양극의 협착 정의), **실험 회귀 + 확률 생성기 + ML 하나** (duquesnoy2020 = LIB 캘린더링), **DEM 궤적 위 딥러닝 하나** (galvezaranda2024 = LIB 압연 · 해제), **복셀 · FEM 전기화학 계산 둘** (hamann2026 = LLZO/Li 3D · islam2026 = LPSCl/Li 2D). **MPM 을 쓴 카드는 없고 DEM 은 galvezaranda2024 한 장** 인데, 그 논문에는 DEM 접촉 법칙 · 물성이 적혀 있지 않다 (ref [36] 상속). 순수 LPSCl 의 압력별 기공 곡선 · 항복 · 경도 · 하중 몫을 준 카드는 없다. 되돌아옴은 galvezaranda2024 한 장 (LIB · DEM · 값은 카드의 그림 판독) 뿐이다. 그래서 k (DEM 의 한계) 는 (1) DEM 논문이 적은 것, (2) 힘 없는 강체 구 생성기가 적은 것, (3) 실험이 말한 "강체 구 가정 밖의 것", (4) 카드의 풀이로 나눠 적었다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `판독` · `figure-read ≈` · `digitized` · `derived` · `derived(ours)` · `우리 산술` · `벡터 추출` · `[미확인]` · `TREND only`) · 없으면 "표지 없음". 카드가 "내 산출 · 내 분석 · 내 검증" 이라 적은 것은 카드 작성자의 것이라 여기서는 "카드 산출" 로 옮겼다. 따옴표 안 영어 문장은 카드가 옮겨 둔 원문. "카드 서술 · 카드의 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산" = 이 정독에서 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님). 카드가 "인용 금지" 표지를 붙인 값은 숫자를 옮기지 않고 줄 번호만 적었다 (froboese2019 의 인쇄 tortuosity 한 값 · hamann2026 의 CCD 값들 · holzer2013 의 Archie 지수 배정 · islam2026 의 입계 무영향 결과 · duquesnoy2020 이 가리킨 우리 쪽 격자 세 값). "랩 표준과 다른 문헌 값" = 순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ 과 다른 값이라는 표시 (기준은 그대로다).

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계` (k · l 은 slug 옆에 인용할 서지 · m 은 `무엇을 | 우리 쪽 어디에 | 근거 위치`)

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

압력별 곡선이 있는 카드 = **0**. 순수 SE 를 눌러 기공을 잰 카드 = **1** (froboese2019 — **고분자** SE · 732 MPa 한 점). 황화물 순수 SE 펠릿은 hlushkou2018 (LPSI 유리 · σ₀ 측정용) 에 나오지만 밀도 · 기공 값이 없다. LPSCl 의 진밀도를 적은 카드는 없다.

- [a] froboese2019_microstructure_ionic_conductivity_assb_electrode | 순수 고분자 SE (PEO : LiTFSI : SiO₂) 펠릿 · ⌀16 mm · 732 MPa 한 점: 기공 4.36 % · σ 6.19 × 10⁻⁴ S/cm @80 °C (같은 과립 · 같은 프레스 · 같은 어닐 · 코인셀 3 개) | §0 L29 · §3-2 L90 · §3-3 L127 · 논문 A321–A323 | stated | 황화물이 아님 (고분자 · 80 °C 72 h 어닐 뒤 80 °C 측정) — LPSCl 기준 (10–13 %) 과 견줄 수 없는 다른 재료의 값 · 압력 한 점 · 압분 온도 [미확인] · 카드도 "LPSCl 순수 SE 기공 앵커로 쓰지 않는다" (L370)
- [a] froboese2019_microstructure_ionic_conductivity_assb_electrode | 기준 밀도 · 질량 기준 · 상태: SE 이론 밀도 1.442 g/cm³ = 성분 진밀도 (PEO 1.24 · LiTFSI 2.16 · SiO₂ 2.0 g/cm³ · 가스 피크노미터) 의 질량분율 조화합 (Eq 4–7) · 기공률 ε = 1 − ρ_측정/ρ_이론 (Eq 11 · 질량 수지) · ρ_측정 = 질량 ÷ (두께 × 지름² × π/4) — 질량 소수 5 자리 · 세 점 두께 (Mitutoyo ID-C112AXB) | §3-1 L65–66 · L75 · §4-1 L188–193 · 논문 A319–A320 | stated (1.442 는 카드 재계산 1.4427 과 일치 · derived) | 누른 채인지 뺀 뒤인지 카드에 표기 없음 (게이지로 잰 펠릿 치수) · 1.442 는 고분자 SE 값 — 랩 표준 (LPSCl 1.64) 과 재료가 다른 문헌 값
- [a] hlushkou2018_void_space_ion_transport_assb_cathode | 순수 LPSI 유리 (Li₂S–P₂S₅–LiI) 펠릿 ⌀6 mm · 276 MPa · 30 min · 실온 — σ₀ 0.7 mS/cm @25 °C 측정용 · **펠릿 밀도 · 기공률 · SE 입경은 원문에 없음** | §0 L29 · §3-A L69–73 · 논문 p.365 | stated (조건 · σ₀) · [미확인] (밀도 · 기공) | 기공 값 0 건 · LPSCl 아님 · Table 1 의 SE 밀도 2.2 g/cm³ (L72 · stated) 는 LPSI 유리 값 — 랩 표준과 다른 (재료가 다른) 문헌 값
- [a] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 순수 LPSCl 층 (2D phase-field) 의 기공률 ~12 % · ~20 % 는 **초기 입자 수로 정한 입력** (압력 축 · 진밀도 없음). 기공 → SE 옴 저항 (고주파 절편) 22.0 (치밀) → 32.5 → 38.0 Ω·cm² | §3 L28–30 · §4-2 L60 | stated (기공 설정) · digitized (절편) | 2D · 계산 입력 — 눌러서 얻은 기공이 아님 · 랩 기준과 견줄 측정값 아님
- [a] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 순수 SE 기공 자료 없음 (소결 LLZO · 기공률은 기공 형성제 · 템플릿으로 정함). 지나가는 한 줄: LPSCl K_Ic 값의 출처 시료가 "다공 13 % 펠릿 · 거시 시험" (song2025 카드 인용) | §9 I-7 L344 | 표지 없음 (다른 카드 인용) | 압력 · 진밀도 · 상태 없음
- [a] duquesnoy2020 · galvezaranda2024 · holzer2013 | 해당 없음 (SE 없음 — LIB · 액체 격막) | — | — | —

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

되돌아온 양을 수로 준 카드 = **1** (galvezaranda2024 — DEM 계산 · 값은 카드의 그림 판독). 실측은 **없다**.

- [b] galvezaranda2024_time_dependent_dl_calendering_microstructure | DEM 압연 (평면 프레스 · 일정 속도) → 목표 CD 에서 프레스 해제 → 완화: CD 25 / 35 / 45 % 에서 되돌아옴 4.8 / 7.6 / 10.1 %p (최대 압축 CD 22.6 / 33.9 / 42.9 % → 완화 뒤 17.7 / 26.3 / 32.8 %) · 눌린 두께 대비 +6.3 / +11.5 / +17.7 % · 잰 방법 = Fig 5b · 6a · 6c 의 void 복셀 수를 판독해 두께 h = (722,000 − void)/(76 × 76) 복셀로 환산 (압축 최저 96.8 / 82.6 / 71.3 → 완화 102.8 / 92.1 / 84.0 복셀) | §3-D L143–157 · §4-1 L171–174 | derived(ours) · digitized — TREND only (읽기 오차 ≈ ± 0.7 %p) | **논문 본문에는 되돌아옴 숫자가 하나도 없음** (L32–34 · L81) · 액체계 LIB (NMC111 + CBD) · 압력 축 없음 (CD %) · DEM 물성 미기재 · 카드: "값은 전이 금지, 부호와 곡률만" (L448)
- [b] galvezaranda2024_time_dependent_dl_calendering_microstructure | 방향: 되돌아옴이 압축 깊이에 단조 증가 — 눌린 두께 대비 회복률 6 → 18 % ("세게 누를수록 더 많이 되튄다") | §3-D L155–157 · §7-3 L424 | derived(ours) | 세 점이 서로 다른 미세구조 (III · II · I) · 시드 · 오차막대 없음
- [b] galvezaranda2024_time_dependent_dl_calendering_microstructure | 같은 그룹 선행 (ngandjong2021 카드 2 판에서 옮김): 압입 언로딩 잔류 깊이 exp ≈ 0.84 · sim ≈ 0.75 d_max → 탄성 회복 16 % vs 25 % | §4-1 L191–193 | 표지 없음 (다른 카드 인용 · "≈") | 압입 회복이지 압연 되돌아옴이 아님 (카드 경고 L193) · LIB
- [b] galvezaranda2024_time_dependent_dl_calendering_microstructure | 지배 기전에 대한 카드 서술: LIB 에서는 되돌아옴을 CBD 점탄성이 지배 (hong2026 카드 인용) — 이 논문의 DEM 은 CBD 를 단일 라벨로 다뤄 그 기전이 모델에 없음 | §7-3 L424 · §10-⑩ L649–650 | 카드 서술 (다른 카드 인용) | ASSB (PTFE · SE) 로 값 전이 금지
- [b] hlushkou2018_void_space_ion_transport_assb_cathode | 재지 않음. 두께는 EIS 측정 뒤 에폭시 매립 단면의 광학 측정 (208 ± 5 µm) 한 상태뿐 · "측정 중 적층압 · 스프링백 [미확인]" | §3-A L81 · L83 · §7 L258 | stated (두께) · [미확인] | 하중 중 두께 없음
- [b] duquesnoy2020_calendering_ml_mesostructure_generator | 재지 않음. 닿는 사실: 제어량이 롤 gap 이고 캘린더 뒤 두께 → 기공률만 있음 — gap 1 µm (초기 두께 138–178 µm) 에서 캘린더 뒤 기공 22.8–25.6 % (실측 평균) · 22.4–25.7 % (다항식) | §3.1 L44 · §3.3 L69–72 · §12 L453 | stated (xlsx) · 카드 검증 표 | 카드는 gap ↔ 최종 두께의 차를 되돌아옴으로 풀이하지 않음 · LIB
- [b] froboese2019 · hamann2026 · holzer2013 · islam2026 | 이 카드들에 없음 | — | — | —

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

황화물 SE 의 항복 · 경도 · 크리프 값을 준 카드는 **없다**. 있는 것은 파괴 인성 (hamann2026 — LLZO · 인용된 LPSCl 값) 과 다른 카드에서 옮긴 탄성 입력뿐이다. **일축 항복 세기로의 환산은 어느 카드에도 없다.**

- [c] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 항복 · 경도 · 크리프 값 없음. 파괴 쪽만: LLZO K_IC 1.25 MPa·m^½ · 표면 결함 깊이 0.4–1.0 µm · γ 1.12 (Porz 식의 입력) → 결함 파괴 응력 σ₀ = K_IC/(γ√(πa)) = 996 MPa (0.4 µm) · 630 MPa (1.0 µm) | §3.1 L112 · §13 D2 L415 | stated (입력) · derived(ours) (응력) | LLZO (산화물) · 파괴 인성이지 항복이 아님
- [c] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | LPSCl 쪽 (다른 카드 인용): K_Ic 0.17 (song2025 · 다공 13 % 펠릿 · 거시 시험) — LLZO 의 약 1/7 · Fan 2026 초안 범위 0.2–0.4 | §7 L275 · §9 I-7 L344 · §13 D10 L448 | 표지 없음 (다른 카드 인용) | 이 카드에는 숫자만 (단위는 LLZO 값과 같은 줄에 놓여 있음) · 일축 항복 환산 없음
- [c] hlushkou2018_void_space_ion_transport_assb_cathode | SE (LPSI 유리) 의 E · σ_y · 입경 · 펠릿 밀도는 원문에 없음 | §3-A L73 · §10 L341 | [미확인] | —
- [c] galvezaranda2024_time_dependent_dl_calendering_microstructure | 이 논문에 DEM 물성 0 건 (E · ν · µ · COR · 접촉 법칙 전부 미기재). 카드가 옮긴 계보 카드 값 (ngandjong2021 · 같은 그룹 · 같은 조성): E_AM 200 GPa · E_CBD 2 GPa · ν_AM 0.3 / ν_CBD 0.5 · COR 0.15 · X_µ 0.001 | §4-1 L165–185 | 미기재 (이 논문) · 다른 카드 값 (출처 분리 경고 L184–185) | 탄성 입력뿐 · LIB · 이 논문 값이 아님
- [c] froboese2019_microstructure_ionic_conductivity_assb_electrode | 기계 물성 0 건 — 카드가 "famprikis2019 카드가 이 논문을 σ_y(SE) · K_Ic · µ 조달 대상으로 적었으나 이 논문에는 기계 물성이 하나도 없다" 는 정정 후보를 적음 | §10 L440 | 카드 서술 | —
- [c] duquesnoy2020 · holzer2013 · islam2026 | 이 카드들에 없음 | — | — | —

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫을 수로 준 카드는 **없다**. 닿는 것은 (1) 단단한 구 + 무른 기지를 한 압력으로 눌렀을 때 남는 기공 (froboese2019 — 실측), (2) 형상이 안 변하는 DEM 의 기공 바닥 (galvezaranda2024), (3) 힘 없는 배치 알고리즘의 막힘 (duquesnoy2020).

- [d] froboese2019_microstructure_ionic_conductivity_assb_electrode | 단단한 유리구 + 무른 고분자 SE 를 732 MPa 로 누른 뒤 남는 기공 (하중 몫 아님 · 결과만): 순수 SE 4.36 % → 유리구 60 vol% 에서 14.15 % (70–110 µm) · ≈ 16.3 % (40–70 µm) · 19.72 % (0–50 µm) · 굵은 두 입경은 30 vol% 까지 거의 일정한 뒤 지수적 증가 · 47.5 vol% 에서 ε ≈ 14.2 · 12.6 · 9.1 · 5.7 % (x50 2.96 · 35.65 · 60.68 · 92.5 µm) | §3-2 L90–110 · L115 · §3-3 L127 · 논문 A322–A323 · Fig 8 | stated (4.36 · 5.42 · 19.72) · 판독 ≈ (나머지 · TREND 전용) | 고분자 SE · 유리구 수십 µm · 단일 압력 · 하중을 누가 지는지는 재지 않음 · 60 % 굵은 두 입경의 본문 표기가 그림과 뒤바뀜 (카드 §3-6 c — 여기 값은 그림 배정)
- [d] froboese2019_microstructure_ionic_conductivity_assb_electrode | 한계 조성: 0–20 µm 유리구는 50 vol% 초과에서 기계적으로 불안정 (60 % 전극을 못 만듦) · 40–70 µm 는 > 60 vol% 불안정 · 측정 밀도는 50 vol% 까지 늘다가 줄어듦 · 원문 설명 = "기공 크기는 입경의 1/2–1/4" (ref 41) 이라 작은 틈을 SE 가 못 채움 | §3-1 L72 · §3-2 L113 · §3-3 L128 · §6-bis L288 | stated | 정성 · 하중 몫 아님
- [d] galvezaranda2024_time_dependent_dl_calendering_microstructure | DEM (AM 96 wt% · 형상 불변) 압연의 기공 바닥: CD 40 % 에서 ≈ 19–20 % 에 닿고 그 위에서는 ± 2 % 로 진동 (단조성 깨짐 · 미세구조 IV: 20.02 → 19.04 → 19.87 %) — 저자 해석 "전극이 기계적 압축 한계에 도달" (카드의 한국어 옮김) · 실험의 ≈ 20 % 하한 (2 차 NMC 입자 파쇄 · refs [15, 48, 49]) 과 정성 일치라고 적음 | §3-C L125–131 · L137–141 · §5-3 L294–295 | stated (표 값) · 저자 해석은 카드 옮김 | LIB · CD 축 (압력 없음) · 하중 몫 수치 없음 · 카드: "다른 기전이 우연히 같은 숫자. 그들의 20 % 는 AM 파쇄 한계, 우리 20 % 는 형상 소성 부재" (L421)
- [d] duquesnoy2020_calendering_ml_mesostructure_generator | 힘 없는 기하 한계: 강체 구 무작위 순차 배치가 낮은 기공률 · 높은 AM 분율에서 막힘 — SI: *"at low porosities and high AM content, stochastic algorithms can be stuck"* → 대책이 겹침 허용 (중심 거리 ≥ 0.7·(r_i + r_j)) | §4.1 L149–153 | stated (SI 인용문) · 코드 판독 (카드) | 역학 없음 (재밍이 아니라 배치 알고리즘의 막힘) · LIB
- [d] hamann2026 · hlushkou2018 · holzer2013 · islam2026 | 이 카드들에 없음 | — | — | —

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값의 수

**이 배치에 없음** — 접촉 법칙을 적은 카드가 없다. DEM 을 쓴 galvezaranda2024 도 접촉 법칙 "미기재" (L168) 이고, 계보 카드 (ngandjong2021) 의 "GH (Granular-Hertz) + SJKR" 이 한 줄 옮겨져 있을 뿐이다 (L182 · 깨지는 범위 · 맞춘 값의 수는 없음).

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

**MPM 을 쓴 카드가 없다** (접촉 · 다물체 · 강체 결합 정보 0). 아래는 복셀 · 격자 계산의 해상도 규칙과 수치 오차를 다룬 방식이다.

- [f] holzer2013_constrictivity_effective_transport_porous_layers | 영상 복셀 대비 특징 크기: 평균 입자 > 10 × 복셀 (c-PSD r50 157 nm ÷ 15 nm) · 좁은 목도 4–5 × 복셀 (MIP r50 66 nm) | §3-A L65 · §6 L220 · 논문 p.2940 | stated | FIB-SEM 영상 분석 (수송 · 역학 솔브 아님) · LSC 소결체 · 수렴 시험이 아니라 "여유" 서술
- [f] holzer2013_constrictivity_effective_transport_porous_layers | 대표 부피로 오차를 다룸: 두께를 75 nm 씩 1.5 µm 까지 · 그 뒤 1.25 µm 씩 7.6 µm 까지 늘려 반복 → 목 반지름 통계는 침투 깊이 ≈ 3 µm (= 최대 입자 반지름의 2–5 배) 위에서 평탄 · 거품 크기 통계는 > 6 µm 필요 · 6 방향 반복 ± 1 nm | §3-A L70–74 · §4-4 L155–156 · 논문 p.2943–2947 · p.2951 | stated | 기하 지표의 대표성 (힘 · 수송 계산 아님)
- [f] galvezaranda2024_time_dependent_dl_calendering_microstructure | DEM → 복셀 해상도: 0.4 µm = "가장 작은 입자의 거의 1/4" (최소 입자 지름 ≈ 1.6 µm 로 환산) · 상 경계 접촉면 오차 (최대 16.76 %) 의 해법으로 저자가 복셀 축소를 제시 · 프레임 수 · 격자 해상도는 "미탐색" | §3-B L97–99 · §5-3 L287–289 · §5-4 L305 | stated · derived(ours) (1.6 µm) | 수렴 시험 0 · 오차 추정 없음 (시드 · 오차막대 0 · L261–262)
- [f] duquesnoy2020_calendering_ml_mesostructure_generator | 구를 복셀로 찍을 때의 부피 손실 (슬라이스 반경을 내림 처리): 복셀 부피 ÷ 해석 부피 = 0.51 (R = 1.0 µm = 1 복셀) · 0.67 (R = 4.0 µm) · PSD 가중 0.694 · R = 1.25 에서 1.06 으로 비단조 → 분포의 모양이 왜곡 | §5(f) L330 | 카드 산출 (20 개 sub-voxel z-offset 평균) | 그 코드의 래스터 규칙에 한한 값 · 1 µm 단일 해상도 · 수렴 시험 없음 (L435)
- [f] duquesnoy2020_calendering_ml_mesostructure_generator | 채널 폭 대 격자: 논문 원자료 두 열로 d_h = ε/(S_V(1 − ε)) = 1.00–1.03 µm → d_h/dx ≈ 1.0 (n = 880) · 카드가 견준 우리 쪽 규칙 d_h/dx ≳ 3.5 의 근거 = MPM 응력 판독에서 격자를 2.25 배 조일 때 3.43 셀 +4.0 % ↔ 1.18 셀 +23.8 % | §5(d) L307–315 | 카드 산출 · 우리 쪽 규칙 인용 | 카드 자기비판: 3.5 는 MPM 응력 판독으로 맞춘 값이고 수송에서는 부호가 반대일 수 있어 "증명된 문턱이 아니라 자릿수 경고" (L315)
- [f] hlushkou2018_void_space_ion_transport_assb_cathode | 복셀 35.6 × 35.6 × 100 nm (비등방) · 무작위 걸음의 시간 간격 = 평균 변위 ≤ 복셀/10 · 추적자 10⁷ · 방법 검증 = 구 배열 해석해 [38] 대조 (이전 논문 [36, 37]) · 유한크기: 부분 부피 한 변을 10 → 100 % 로 키우며 반복 — LCO · SE · void 지표는 ~70 % 에서 점근 · SE + void 를 합친 상은 100 % 에서도 미수렴 | §3-C L111 · §3-D L126 · §3-E L133–137 | stated · 판독 (Fig S1) | 확산 계산 (역학 아님) · τ_diff 에 오차 막대 없음 · 도메인 외곽 경계조건 [미확인]
- [f] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 복셀 크기 · 격자 수 미기재 · 수렴 기준 = 전위 · 전극 면전류 상대 잔차 < 10⁻⁵ (식 S49 · S57) · 메모리는 겹치는 부분영역 분할로 GPU 에 올림 | §3.1 L110–111 · §4.4 L197–200 · §4.6 L210 | stated · [미확인] (복셀 크기) | 최대값 통계의 격자 수렴 근거 없음 (L365) · 전기화학 계산
- [f] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 2D 200 × 100 격자 · dx 3.75 µm · 입자 평균 반경 60 µm · "격자수렴 0 · 시드 0" | §4-2 L60 · §10 L118 | stated · 카드 서술 | 2D · FEM / phase-field

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

2D 계산을 3D 와 직접 견준 카드는 없다. 경고로 쓸 수 있는 것:

- [g] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 2D 한 장 · 실현 1 개 결과의 지위: "2D, 실현 1 개, 시드 0, 격자수렴 0 — 통계적 주장 불가" · "크기 전이 금지 (2D · 스케일 카툰)" · 3D 없음 | §4-2 L67 · §7 L99 · §10 L118 | 카드 서술 | 논문 자신의 2D ↔ 3D 비교는 없음
- [g] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 2D 에서 얇은 저항 상을 임계화하면 닫힌 망이 아니라 끊긴 선분이 되어 전류가 우회 — 넣은 저항 항의 효과가 사라짐 (연속 막이라면 직렬 ≈ 66 Ω·cm² 가 더해져야 한다는 카드 산술 ↔ 관측 변화는 거의 없음) | §6 L90 · §10 L120 | derived (카드 산술) · 카드 서술 | 그 "입계 영향 없음" 결과는 카드가 "인용 금지" 표지 (값은 옮기지 않음 · L33 · L76) · 2D · 격자 3.75 µm · 3D 에서 어떻게 되는지는 카드에 없음
- [g] holzer2013_constrictivity_effective_transport_porous_layers | 2D 면 통계의 대표성 부족: 출구면만 본 크기 분포는 6 방향 r50 이 53–94 nm 로 흩어짐 ↔ 전체 부피 통계는 6 방향 ± 1 nm · 입구면 6 방향 평균은 3D 분포와 가까움 (154 ↔ 157 nm) → 3D 부피 통계 권고 | §3-A L74–76 · §4-4 L156 · §5 L207–208 · 논문 p.2946–2948 | stated | 영상 기하 지표 (힘 · 수송 아님) · LSC
- [g] duquesnoy2020_calendering_ml_mesostructure_generator | 경계면 한 장의 2D 면적분율은 3D 연결성을 뜻하지 않음: 집전체 접촉 지표가 z = 1 슬라이스의 면적분율이라 "집전체 위에 떠 있는 고립된 CBD 섬 하나도 그대로 계수" — 연결성 검사 0 | §4.5 L236–241 | 카드 서술 (코드 판독) | 수송 지표 · LIB
- [g] galvezaranda2024 · hamann2026 · hlushkou2018 | 이 카드들에 없음 (모두 3D) | — | — | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

**역학 계산을 DEM 에서 FE · MPM 으로 넘긴 선례는 이 배치에 없다.** 가까운 것:

- [h] galvezaranda2024_time_dependent_dl_calendering_microstructure | DEM 입자 좌표 → 복셀 격자 (0.4 µm · 라벨 pore / CBD / AM / void) → GeoDict DiffuDict 유한체적 확산 (x · y 주기 · z 양끝 농도 고정) — **수송 계산용 넘김** (역학은 끝까지 DEM) · 넘기는 시점 = 프레임 (75 µs) 마다 복셀화 · 상류는 CGPD (슬러리 + 건조) → DEM 압연의 초기 구조 | §4-1 L176 · §4-2 L198–203 · §4-4 L250–253 | stated | LIB · 넘김의 함정: 복셀 라벨 기공률이 표의 기공률과 어긋나고 (프레임 0 에서 22.6 ↔ 31.09 % · 완화 뒤 2.7 ↔ 19.07 %) AM 복셀 수가 −22.3 % 까지 줄었다 되돌아옴 (L525–541 · digitized — TREND only)
- [h] duquesnoy2020_calendering_ml_mesostructure_generator | 선례 아님 (참고): 같은 그룹이 2020 확률 생성기 → 2023 에 CGMD 슬러리 → 건조 → DEM 압연 사슬 + GeoDict 로 교체 | §14 L478–489 | 카드 서술 (다른 카드 요약) | 역학 넘김 아님
- [h] hamann2026 · hlushkou2018 · islam2026 | DEM 없음 — 영상 (FIB-SEM) 또는 phase-field 미세구조 → 복셀 / FEM 수송 계산 | hamann §4.1 L178–182 · hlushkou §3-C L103–111 · islam §4 L41–60 | stated | 역학 계산 없음

## i. 복합 양극 (AM + SE) 의 압력별 기공

AM + SE 를 압력별로 잰 카드 = **0**. 한 압력의 점 (hlushkou2018 · froboese2019) 과 SE 없는 LIB 대조 (duquesnoy2020 · galvezaranda2024) 만 있다.

- [i] hlushkou2018_void_space_ion_transport_assb_cathode | LCO (≈ 5 µm) + LPSI 유리 복합 (38 : 62 vol% 공칭) · FIB 시료 (에폭시 수지와 섞어 4 t/cm² · 14 h): 재구성 부피분율 LCO 33.1 · SE 53.7 · void 상 13.2 % — void 상 = "안정화 수지가 차지한 공간 + 잔류 공극" (분리 불가) | §3-A L82 · §3-C L110 · §3-D L116–123 · 논문 p.365–367 · Table 3 | stated | 한 압력 (카드 환산 ≈ 392 MPa · tonne-force 가정) · 수지 포함이라 잔류 기공률이 아님 (상한도 하한도 아님 · L270) · EIS 시료 (수지 없음 · 5 min) 의 기공은 [미확인] · LPSI · LCO
- [i] froboese2019_microstructure_ionic_conductivity_assb_electrode | 모델 복합 (유리구 + 고분자 SE) @732 MPa 단일: 기공 ≈ 2.8 % (10 vol% · 0–20 µm) – 19.72 % (60 vol% · 0–50 µm) · 조성 · 입경 21 점 표 | §3-2 L88–110 | stated (19.72 등) + 판독 ≈ (TREND 전용) | 압력 축 없음 · NCM · 황화물 아님
- [i] duquesnoy2020_calendering_ml_mesostructure_generator | AM + SE 아님 (LIB 대조): NMC111 + CBD 전극의 캘린더 뒤 기공 22.1–36.4 % (초기 42.5–48.9 % · gap 1–100 µm) · 압력축은 교정식 P = 189·exp(−gap/(0.21·T)) 로 환산 (교정점 ≈ 6–175 MPa) · 생성기 쪽 곡선 (Fig 3): ε_init 48 % 에서 0.40 → 0.331 (AM 96 %) · 0.378 → 0.305 (AM 93 %) — "~100 MPa 이후 포화" | §3.1 L43–45 · §3.2 L52–54 · §6 L339 | stated (실측 범위 · 식) · figure-read ≈ TREND (곡선) | SE 없음 · 액체 전해질 · 압력은 gap 의 환산값 · Fig 3 의 ε_cal 은 측정이 아니라 다항식 목표값 (두께 100 µm 로 교정 범위 밖 외삽 · L75)
- [i] galvezaranda2024_time_dependent_dl_calendering_microstructure | AM + SE 아님 (LIB · DEM): CD 20 / 25 / 30 / 35 / 40 / 45 / 50 % 에서 기공 30.66 / 26.54 / 24.78 / 21.04 / 20.02 / 19.04 / 19.87 % (미세구조 IV) | §3-C L125–131 · SI Table S2 | stated | 압력 (MPa) 축 없음 · 계산값 (실험 아님) · SE 없음
- [i] hamann2026 · holzer2013 · islam2026 | 해당 없음 | — | — | —

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)

- [j] galvezaranda2024_time_dependent_dl_calendering_microstructure | 저자가 적은 한계 셋: (i) 상 사이 접촉면 오차 10–15 % (전체 기능 지표 < 5 % 와 대비) (ii) CD 20–50 % 밖의 외삽은 비물리적 거동을 낼 수 있음 (iii) 프레임 수 · 격자 해상도는 미탐색 · 그리고 "이 연구의 목표는 DEM 결과를 더 빠른 ML 로 재현하는 것" (기준선이 실험이 아니라 DEM) | §5-3 L297–299 · §5-4 L303–305 | stated (카드의 한국어 옮김) | LIB
- [j] galvezaranda2024_time_dependent_dl_calendering_microstructure | 카드가 적은 한계: 되돌아옴은 궤적의 육안 일치뿐 (숫자 0) · 압력 축 0 · DEM 물성 0 · 소성 형상 변화 0 · CBD 를 단일 라벨로 (점탄성 없음) · 데이터 · 코드 비공개 | §0 L32–40 · §4-5 L258–262 · §10-⑩ L643–650 | 카드 서술 | —
- [j] duquesnoy2020_calendering_ml_mesostructure_generator | 압밀 물리가 없다 (기공률이 입력 · 실험 다항식 밖으로 못 나감 — 다른 재료 · 압력 · 두께는 식을 다시 재야 함) · 압연 전 · 후 구조 사이에 연속성이 없음 (조건마다 새 상자를 처음부터 채움) · 생성 구조의 기공률 미측정 · 격자 수렴 시험 없음 | §4.1 L154–156 · §4.3 L212–218 · §11 L433–438 | 카드 서술 (코드 판독) · SI 인용문 (L153) | LIB
- [j] froboese2019_microstructure_ionic_conductivity_assb_electrode | 원문 결론: 구 충전은 0 % 기공에 못 가고 일축 압분으로는 0 % 불가 → 건식 과립 · 압출 · 코팅 같은 공정이 필요 · 카드: 단일 압력 · 단일 온도라 압력 의존을 말할 수 없음 | §6-bis L293 · §10 L424 | stated (카드 요약) · 카드 서술 | 고분자 SE
- [j] hlushkou2018_void_space_ion_transport_assb_cathode | 원문: 형태 – 수송 관계에는 형태 정보 전체가 필요하고 부피분율만으로는 안 됨 · 잔류 공극량에 주의 · SE 분율이 낮은 전극에서 더 나빠질 것 (추정 · 검증 없음) · 카드: 역학 · 압밀 물리 없음 — 공극이 왜 생기고 어떻게 없애는지는 다루지 않음 · 측정 중 적층압 · 되돌아옴 [미확인] | §1 L46 · §4-3 L189 · §7 L249 · L258 | stated (카드 요약) · 카드 서술 | LPSI · LCO
- [j] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 저자 §2.6: 계면 완전 정합 · Li 등전위 · 정상 상태의 이상화 — 실제는 보이드 (억제에 적층압 2–3 MPa 필요 [62] · 탈리 중 감소) · dead Li · 카드: 응력은 계산하지 않고 사후 문턱식 | §2.5 L87 · §4.5 L205–207 · §10.1 L351–353 | stated (카드 요약) | LLZO · Li 음극 — 가압 계산과는 "계면 접촉을 완전하다고 둔다" 는 가정에서만 닿음
- [j] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 역학 없음 (압력 · 응력 · 형상 소성 0) · 소결 모델에서 입자의 강체 병진 (어드벡션) 무시 · 실험 검증 0 | §4-2 L59 · L66 · §7 L104 · §10 L117 | stated · 카드 서술 | 2D
- [j] holzer2013_constrictivity_effective_transport_porous_layers | 가압 · 탈압과 닿는 한계 없음 (저자 한정어는 수송 분해식에 대한 것: *"the proposed parametric approach represents a heuristic solution and its validity has yet to be tested"*) | §4-3 L146 | stated (인용문) | —

## k. DEM 의 한계 (논문이 직접 말한 문장 · 수치)

**DEM 을 쓴 카드 = 1** (galvezaranda2024 — 물리는 ref [36] 상속). 그 논문은 DEM 의 한계 (믿을 수 있는 겹침 · 상대밀도 상한 · 접촉 독립 가정이 깨지는 밀도) 를 **직접 말하지 않는다**. 아래는 (1) DEM 논문에서 나온 것, (2) 힘 없는 강체 구 생성기가 적은 것, (3) 실험이 말한 "강체 구 가정 밖의 것", (4) 카드의 풀이다 — 인용할 때 넷을 구분한다.

- [k] galvezaranda2024_time_dependent_dl_calendering_microstructure (D. E. Galvez-Aranda, T. Le Dinh, U. Vijay, F. M. Zanotto, A. A. Franco, Adv. Energy Mater. 14, 2400376 (2024)) | (1) DEM 한계에 대한 직접 문장 = **말 없음** (접촉 법칙 · E · ν · µ · COR · 겹침 상한 전부 미기재). 가장 가까운 저자 서술: 기공률이 CD 40 % 에서 ≈ 19–20 % 바닥을 치고 그 위에서는 ± 2 % 진동 — "전극이 기계적 압축 한계에 도달" · 실험의 ≈ 20 % 하한은 "2 차 NMC 입자 파쇄 때문에 그 아래로 못 간다" (refs [15, 48, 49]) 와 정성 일치 | §3-C L137–141 · §4-1 L163–178 · §5-3 L294–295 | stated (표 값) · 저자 해석은 카드의 한국어 옮김 (원문 영어 문장은 카드에 없음) | LIB · CD 축 · 형상이 안 변하고 파쇄도 없는 DEM 이 같은 숫자에 닿은 것 — "다른 기전이 우연히 같은 숫자 … 같은 숫자를 같은 근거로 쓰지 말 것" 은 카드의 풀이 (L421)
- [k] galvezaranda2024_time_dependent_dl_calendering_microstructure (같은 서지) | (4) 깊이 누른 DEM 의 겹침 크기를 보여 주는 카드 판독: Fig 5b (미세구조 I · CD 45 %) 의 AM 복셀 수 4.40 → 3.42 × 10⁵ (−22.3 %) → 완화 뒤 3.95 (−10.2 %) — 고체 상의 복셀이 사라졌다 되돌아옴 = "복셀이 겹침 (union) 을 세고 있다는 서명" · 같은 시점의 pore 복셀 ≈ 0 | §10-② L525–532 | digitized — TREND only · 풀이는 카드 서술 | 논문은 이 불일치를 말하지 않음 · 겹침 탓이라는 것은 카드의 풀이 (다른 해상도 · void 처리 가능성도 열어 둠 · L537–539)
- [k] galvezaranda2024_time_dependent_dl_calendering_microstructure (같은 서지) | (1)(4) 검증의 지위: 이 논문의 실험 검증은 전부 ref [36] (Xu 2023 · J. Power Sources 554, 232294) 상속 — *"already validated by experiments … in electrode functional metrics such as tortuosity factor and porosity"* · 카드의 갱신: 기공률은 독립 검증 (실험 8 점) 이지만 τ 는 후처리 (dilation–erosion) 인자를 µ-XCT τ 값에 가장 가깝게 골라 모든 결과에 적용한 것 | §4-1 L177 · §12 L705–708 | stated (인용문) · 카드 서술 (xu2023 카드 인용) | 후처리 인자 (DEM 접촉 물성이 아님) · LIB
- [k] galvezaranda2024_time_dependent_dl_calendering_microstructure (같은 서지) | (1) 계산 비용: DEM ≈ 47 min / 프레임 (75 µs · 하드웨어 미기재) → 35 런 · 855 프레임 = 670 h (≈ 27.9 일 · 직렬) | §3-B L113–115 · §10-⑨ L631–632 | stated (47 min) · derived(ours) (합계) | 입자 수 미기재
- [k] duquesnoy2020_calendering_ml_mesostructure_generator (M. Duquesnoy, T. Lombardo, M. Chouchane, E. N. Primo, A. A. Franco, J. Power Sources 480 (2020) 229103) | (2) DEM 아님 (힘 없는 강체 구 무작위 배치) — 겹치지 않는 구로는 낮은 기공률에 못 간다는 것을 SI 가 스스로 적음: *"at low porosities and high AM content, stochastic algorithms can be stuck"* → 겹침 허용 (SI: *"if the radii intersection a is lower than 30 % of the smallest radius"* ↔ 코드: 침투 깊이 ≤ 0.3·(r_i + r_j) = 6.3 배 관대) · 겹친 부피는 한 번만 셈 (*"the overlapped AM fraction was considered only once"*) | §4.1 L149–153 · §11 L434 | stated (SI 인용문) · 코드 판독 (카드) | 겹침은 속도를 위해 허용한 것이고 물리적 소성이 아님 (카드 서술 L395) · 압력과 무관 · LIB
- [k] duquesnoy2020_calendering_ml_mesostructure_generator (같은 서지) | (4) 카드의 풀이: "강체 구, 소성 0 … 접촉법칙조차 없음" · 기공률이 입력이라 "~20 % 가 강체 구 바닥" 이라는 명제를 이 논문으로는 시험할 수 없음 ("반례도 증거도 아님") | §8.2 L395 · §8.3 L413 · §14 L494 | 카드 서술 | 논문 문장 아님
- [k] froboese2019_microstructure_ionic_conductivity_assb_electrode (L. Froboese, J. F. van der Sichel, T. Loellhoeffel, L. Helmers, A. Kwade, J. Electrochem. Soc. 166 (2) A318–A328 (2019)) | (3) DEM 안 씀 (실험) — DEM 에 대한 말 없음. 구 입자 모델이 놓치는 것으로 인용할 수 있는 실험 문장: *"the filling of pores with solid electrolyte gets more difficult with decreasing particle and pore sizes"* (A323) · 결론: 구 충전은 0 % 기공에 못 감 (입자는 비구형이어야) · 일축 압분으로는 0 % 불가 | §6-bis L293 · §7-2 L368 | stated (인용문 · 결론은 카드 요약) | 고분자 SE + 유리구 (황화물 아님) — 방향의 근거로만
- [k] froboese2019_microstructure_ionic_conductivity_assb_electrode (같은 서지) | (4) 카드의 풀이: 눌린 뒤 SE 는 연속 기지 — "'SE 입자' 라는 단위가 없다 — 우리 DEM 의 SE 구 · SE–SE 접촉 (Holm) 에 대응하는 구조가 없다" · DEM 기공은 구 충전의 기하 공극이라 "계면 미충전" 같은 공정 기공을 만들 기전이 없음 (같은 ε 라도 기공이 AM–SE 계면에 몰리면 SE 경로를 더 끊는다 — 제안 · 미검정) | §4-4 L227–228 · §7 L345 · §8 ④ L411 | 카드 서술 (Fig 5 단면 판독) | 논문 문장 아님 · SE 과립 크기 [미확인]
- [k] hlushkou2018_void_space_ion_transport_assb_cathode (D. Hlushkou, A. E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, U. Tallarek, J. Power Sources 396 (2018) 363–370) | (3) DEM 안 씀 (실험 + 복셀) — 말 없음. 구 충전 그림 밖의 것을 말한 문장: 공극이 없으면 SE 공간은 구 충전의 입자 사이 공간과 비슷해 Bruggeman 이 맞지만 (1.22 ↔ 1.27), 실제 구조에서는 *"a relatively small additional volume fraction of voids (13%) … already suffices to create a substantial number of fine and highly tortuous paths"* (p.369) — tortuosity factor 1.27 → 1.74 · 결론: 형태 정보 전체가 필요하고 부피분율만으로는 안 됨 | §3-E L139–142 · §4-3 L188–189 | stated (인용문 · 가운데 생략은 카드 그대로) | LPSI 유리 + LCO · void 13 % 는 수지 포함 · 수송에 대한 말 (가압 역학의 한계 문장이 아님)
- [k] hlushkou2018_void_space_ion_transport_assb_cathode (같은 서지) | (4) 카드의 풀이: 눌린 유리 SE 복합체가 void + 수지 13.2 % 로 "강체구 바닥 아래에 있다 — 실제 소성 치밀화의 방향과 맞다" (단 수지 포함이라 잔류 기공의 상한도 하한도 아님) · 접촉망은 SE 가 점접촉 입자상이라 "공극 없는 SE 연속 기지" 전제부터 다름 | §7 L270 · §8-1 ③ L323 | 카드 서술 | 논문 문장 아님
- [k] holzer2013_constrictivity_effective_transport_porous_layers (L. Holzer, D. Wiedenmann, B. Münch, L. Keller, M. Prestat, Ph. Gasser, I. Robertson, B. Grobéty, J. Mater. Sci. 48(7), 2934–2952 (2013)) | (3) DEM 안 씀 — 말 없음. 입자 사이 좁은 접촉 (목) 이 수송을 제한한다는 영상 쪽 문장: LSC 고체 입자상의 기하 협착 0.18 은 *"documents the morphological limitations for transport processes (e.g. electronic or ionic conductivity), which are caused by the narrow contacts between the LSC-particles"* (p.2944) | §3-A L67 | stated (인용문) | 소결 나노 입자 (LSC) · 그 상의 수송은 재지 않음 · 가압 역학 아님
- [k] holzer2013_constrictivity_effective_transport_porous_layers (같은 서지) | (4) 카드의 풀이 (접촉망 수송 쪽 한계): 접촉 저항을 끈 접촉망 가지는 입자 단면 원기둥을 잇는 꼴이라 부피가 보존되지 않아 tortuosity factor < 1 이 26/157 침대에서 나옴 → 원문 식의 정의역 (τ ≥ 1 · Eq. 2) 밖 = "모델 내부 기준선" | §0 L30 · §7 L237 · §8 (나) L299 | 카드 서술 (메모 v2 유도값 인용) | 우리 쪽 망에 대한 판단 · 논문 문장 아님
- [k] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd (T. R. Hamann, J. O'Neill, E. D. Wachsman, Adv. Funct. Mater. 2026, e78540) | DEM 안 씀 — 말 없음. 카드의 풀이: 소결 LLZO 는 "목이 이미 접합된 연속체" 라 접촉을 뭉뚱그릴 필요가 없는 드문 경우 — 냉간 압축 LPSCl 의 영률 연화와 접촉 저항 결손은 "이 논문으로 정당화되지 않는다" | §4.5 L204 · §7.1 L291 | 카드 서술 | 논문 문장 아님
- [k] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell (K. Islam, N. Katsube, Y. Ji, manuscript (2026) — 저널 미확정) | DEM 안 씀 — 말 없음. 카드 서술: "입자가 없다 — 전부 연속체 phase map … 강체구도, 접촉 소성도, 하중도 없다" | §4-2 L66 | 카드 서술 | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값

소성을 계산에 넣은 카드는 **없다**. 그래서 "왜 어려운가" 를 논문이 직접 설명한 문장은 실험 쪽 (froboese2019 · hlushkou2018) 에만 있고, 나머지는 소성을 넣지 않고 **돌아간 길** (실험 회귀식 · 형상 불변 DEM · 실물 영상 · 확산 소결) 의 값이다.

- [l] duquesnoy2020_calendering_ml_mesostructure_generator (M. Duquesnoy, T. Lombardo, M. Chouchane, E. N. Primo, A. A. Franco, J. Power Sources 480 (2020) 229103) | 우회 = 압밀을 풀지 않고 **실험 회귀식에 맡김**: ε_cal = f(AM% · ε_init · 두께 · gap) 6 항 다항식 · 맞춘 값 = 계수 6 개 · 맞춘 대상 = 캘린더 전극 54 개 (14 조건) · R² 0.97 · 검증 = 카드가 원자료 5 조건에서 재현 확인 (차 ≤ 0.4 %p · 내 검산) · 한계 = 식 밖으로 못 나감 (생성기가 두께 100 µm 를 넣어 교정 범위 138–180 µm 밖 → ε_cal 이 +10.3 %p 이동) · 비용 = 전극 8,800 개 생성 + 분석 ≈ 7 일 (i7-8700 · 32 GB) | §3.3 L57–75 · §4.3 L205–218 · §4.6 L256 | stated (계수 · R² · 비용) · 카드 검증 · 카드 분석 | LIB · 재료를 바꾸면 식을 다시 재야 함 (L156) · 강체 구의 겹침은 소성의 대리가 아니라 배치를 끝내기 위한 허용
- [l] galvezaranda2024_time_dependent_dl_calendering_microstructure (D. E. Galvez-Aranda, T. Le Dinh, U. Vijay, F. M. Zanotto, A. A. Franco, Adv. Energy Mater. 14, 2400376 (2024)) | 소성에 대한 설명 = **없음** ("이 논문에는 어떤 소성 서술도 없다" — 카드). 택한 길 = 형상이 안 변하는 DEM (CT 유래 비구형 입자 · 접촉 + 재배열) 에 해제 구간을 붙임 · 맞춘 값의 수 = 이 논문에 없음 (DEM 물성 0 건) · 검증 = ref [36] 상속 (기공률 실험 8 점 · τ 는 후처리 인자 맞춤) · 비용 DEM ≈ 47 min/프레임 → 대리모델 15 s/프레임 (학습 자료 580 프레임 = 454 h) | §4-1 L163–178 · §4-5 L257–262 · §10-⑨ L629–636 | stated · derived(ours) · 카드 서술 | LIB · 압력 축 없음 · 기공 바닥 ≈ 20 % (저자 해석 "기계적 압축 한계")
- [l] froboese2019_microstructure_ionic_conductivity_assb_electrode (L. Froboese, J. F. van der Sichel, T. Loellhoeffel, L. Helmers, A. Kwade, J. Electrochem. Soc. 166 (2) A318–A328 (2019)) | 왜 어려운가 (실험 쪽 관찰): 무른 SE 가 단단한 입자 사이 틈을 메우는 일이 틈이 작을수록 어려움 — *"the filling of pores with solid electrolyte gets more difficult with decreasing particle and pore sizes"* (A323) · "기공 크기는 입경의 1/2–1/4" (ref 41) · 결과: 같은 조성 · 같은 732 MPa 에서 유리구 x50 2.96 µm 는 기공 ≈ 14.2 % ↔ 92.5 µm 는 ≈ 5.7 % (47.5 vol%) | §3-2 L115 · §6-bis L288 · §7-2 L368 | stated (인용문) · 판독 ≈ (기공) | 고분자 SE (황화물 아님) · 시뮬레이션 없음 (우회도 없음) · 카드의 풀이: SE 는 "연성 고분자의 형상 흐름" 으로 틈을 채움 — 입자 모양이 변하는 계산 쪽의 기전 (L228 · 해석)
- [l] hlushkou2018_void_space_ion_transport_assb_cathode (D. Hlushkou, A. E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, U. Tallarek, J. Power Sources 396 (2018) 363–370) | 소성은 모형화하지 않음 — "유리 SE 의 실제 소성 변형은 시료가 이미 겪은 결과로 영상에 들어 있을 뿐" (카드). 우회 = 눌린 실물의 FIB-SEM 영상을 그대로 계산 격자로 (590 절편 · 수동 분할 수정 여러 번 · 계산 시간은 카드에 없음) · 공극을 SE 로 바꾼 가상 구조는 SE 부피를 더한 것 (SE : LCO 1.62 → 2.02) 이라 부피가 보존되는 유동과 다름 | §3-C L105–108 · §4-5 L197–200 · §8-1 ① L321 · §10 L340 | stated · 카드 서술 | LPSI · LCO · 한 시료
- [l] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd (T. R. Hamann, J. O'Neill, E. D. Wachsman, Adv. Funct. Mater. 2026, e78540) | 형상 · 응력 · 소성 0 — 기하는 정지 (소결 실구조) · Li 석출이 만드는 응력은 계산하지 않고 사후 문턱식 (Porz) 으로만 해석 | §4.5 L205 | 카드 서술 | LLZO · 가압 아님
- [l] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell (K. Islam, N. Katsube, Y. Ji, manuscript (2026) — 저널 미확정) | 형상을 바꾸는 것은 소성이 아니라 확산 소결 (phase-field · 표면 · 입계 확산) — 하중 · 압력 축 없음 · 강체 병진 무시 · 무차원 파라미터 9 개 (Table 1 · 무엇에 맞췄는지는 카드에 없음) · 검증 0 | §4-2 L59–66 | stated · 카드 서술 | 2D · 냉간 가압과 다른 기전
- [l] holzer2013_constrictivity_effective_transport_porous_layers | 이 카드에 없음 (역학 없음) | — | — | —

## m. 받아들일 통찰 (무엇을 | 우리 쪽 어디에 | 근거 위치)

- [m] duquesnoy2020_calendering_ml_mesostructure_generator | 보고하는 기공률은 만든 (누른) 구조에서 직접 센 값이어야 한다 — 이 생성기는 다항식의 목표값을 그대로 출력해 사전 충전 초과가 있어도 검출할 수단이 없음 | 단계 0 (기공 연산자 — 목표 · 입력값을 결과 칸에 적지 않기) · 단계 4 · 5 | §4.1-7 L154 · §11-4 L436 · §13-B L464
- [m] duquesnoy2020_calendering_ml_mesostructure_generator | 두께를 바꿀 때는 고체 부피 보존식 z = z₀(1 − ε_i)/(1 − ε_c) — 이 코드의 z = z₀(1 − (ε_i − ε_c)) 는 고체량이 +7.9 % (0.46 → 0.33) · +12.2 % (0.50 → 0.29) 어긋남 | 단계 0 (질량 보존 검사) · 단계 6 (두께 ↔ 기공 환산) | §3.3 L76 · §13-I L471
- [m] duquesnoy2020_calendering_ml_mesostructure_generator | 구를 격자에 찍을 때 부피 손실이 반지름에 비단조 (1 복셀 반지름 0.51 · 4 복셀 0.67 · 1.25 복셀 1.06) → 입도 분포의 모양이 달라짐 · 그래서 상 부피는 "찍은 뒤 센 값" 으로 맞춘다 (이 코드가 CBD 를 복셀 수로 강제해 부피 오차 0 으로 만든 방식) | U1 (입자 하나의 해상도) · 단계 5 (출발 구조의 상 부피) · 단계 7 | §5(a) L277–279 · §5(f) L330
- [m] duquesnoy2020_calendering_ml_mesostructure_generator | 함정 둘: tortuosity 값을 옮길 때 제곱 규약 확인 (공개 CSV = tortuosity factor · 논문 그림 = 그 제곱근) · 타깃이 다른 양의 대수 함수인지 먼저 검사 (active surface ≈ 100·ε/(1 − ε) · R² 0.9964 → 그 타깃의 ML R² 0.995 는 기공률을 다시 배운 것) | 단계 7 (수송 값 인용 규약) · 흐름 밖: ML 타깃 설계 · 문헌 값 대조 | §3.4 L93 · §7.3 L369–381
- [m] froboese2019_microstructure_ionic_conductivity_assb_electrode | 순수 SE 기준 상태의 장부를 결과 전에 정한다: σ₀ 를 같은 공정의 순수 펠릿으로 재고, 순수 펠릿의 tortuosity (= φ_pure) 를 1 로 두지 않고 계산 (0.956 · 기공 4.36 %) — 정규화 목표를 1 로 둘지 φ_pure 로 둘지 · 순수 상태의 기공을 SE 부피분율에 넣을지에 따라 값이 ≈ 12 % 달라짐 (카드 derived · 우리 순수 SE 침대 기공 ≈ 12 % 기준) | 단계 7 · 단계 0 (결과 전 판정 기준) · 결과 전 대조 항목 | §0 L29 · § τ 판정 2 L319 · §8 ① L408
- [m] froboese2019_microstructure_ionic_conductivity_assb_electrode | 입자 크기 효과를 볼 때는 같은 기공률 띠 안에서만 견준다 — 이 실험에서 같은 조성의 수송 순서는 입경이 아니라 공정 기공률 순서를 따름 (x50 3 µm 와 36 µm 가 거의 같은 값 9.2 · 8.7) | 단계 7 · 흐름 밖: 입도 설계 (입경비 효과의 판정) | §3-2 L115 · §8 ⑤ L412 · §10 L425
- [m] froboese2019_microstructure_ionic_conductivity_assb_electrode | 실험 대조 설계: 비활성 차단 입자 + 관통 측정 (가역 전극 양쪽) 은 우리 수송 tortuosity 와 정의가 같은 양을 바로 줌 (차단 전극 전송선 해석이 필요 없음) | 흐름 밖: 실험과의 대조 (LPSCl 판 대조 실험의 설계) · 결과 전 대조 항목 | § τ 판정 3 L320 · §8 ③ L410
- [m] froboese2019_microstructure_ionic_conductivity_assb_electrode | 함정 셋: (i) 시료별 값을 평균한 tortuosity 는 평균 σ 로 다시 계산한 값보다 14–29 % 큼 (역수의 평균 > 평균의 역수) → 평균 방식을 적기 (ii) 면적 모호성 (전극 원판 2.01 ↔ Li 박 1.131 cm²) 은 절대 σ 를 ≤ 1.78 배 흔들지만 무차원 비 (f · tortuosity) 에서는 약분 (iii) Bruggeman 지수 관례가 셋 (f 지수 1.5 · tortuosity factor 지수 0.5 · 제곱근 지수 0.25) | 단계 7 (보고 방식 · 실험 대조) | §3-6 (e)(f) L171–172 · § τ 판정 4 L321 · §8 ② L409
- [m] galvezaranda2024_time_dependent_dl_calendering_microstructure | 되돌아옴의 관측량 정의: 최대 압축 두께와 해제 · 완화 뒤 두께를 따로 적고, 차이 (%p) 와 눌린 두께 대비 회복률 (%) 두 가지로 보고 · 그림에는 압축 깊이와 되돌아옴 화살표를 함께 (Fig 1b 꼴) · 계산에는 "목표 도달 → 프레스 해제 → 완화" 구간을 명시 | 단계 6 (관측량 · 프로토콜) · 조건 R4 · 결과 전 대조 항목 | §3-D L145–157 · §4-1 L174 · §6 L315 · §8-1 L446–450
- [m] galvezaranda2024_time_dependent_dl_calendering_microstructure | 복셀로 넘길 때 기공률 규약을 기록 (구 부피 합 / union / 복셀 라벨) 하고 고체 상의 복셀 수가 보존되는지 본다 — 이 논문은 라벨 기공률이 표 값과 8.5 %p (프레임 0) · 16.4 %p (완화 뒤) 어긋나고 AM 복셀이 22 % 줄었다 되돌아옴 | 단계 0 (기공 연산자) · 단계 7 (누른 구조 → 수송 격자) | §7-2-③ L409–414 · §8-5 L464–466 · §10-② L520–541
- [m] galvezaranda2024_time_dependent_dl_calendering_microstructure | 판정 지표를 두 층으로: 벌크 지표 (기공률 · tortuosity) 는 3–5 % 로 맞아도 상 경계 지표 (접촉면적) 는 10–17 % 틀림 → 두 계산을 견줄 때 벌크 양과 계면 양을 따로 보고 · 그리고 공간 분산을 분모로 한 R² 는 두께만 맞혀도 높게 나옴 (void 라벨이 분산을 지배) · 선형 축이 큰 상대 오차를 가림 | 단계 3 (판정 지표 설계) · 단계 7 · 흐름 밖: 대리모델 평가 | §3-A L78–81 · §7-4 L434–436 · §10-① L509–518
- [m] galvezaranda2024_time_dependent_dl_calendering_microstructure | 자명한 기준선을 함께 싣는다: 완전 hold-out 전극에서 "같은 압축도의 다른 전극 평균" 이 기공률을 딥러닝과 같은 정확도로 맞힘 (4.01 ↔ 4.18 %) — 기공률은 사실상 압축도만의 함수라 모델을 가르는 힘이 약함 (확산 · tortuosity 에서는 30.32 ↔ 7.17 % · 13.79 ↔ 5.85 % 로 갈림) · 가속 배수는 (단계 배수 · 손익분기 · 남는 계산) 셋을 같이 | 단계 0 · 단계 3 (기공률만으로 접촉 표현을 가르지 않기) · 흐름 밖: 대리모델 · 계산 비용 보고 | §8-3 L455–458 · §8-4 L459–463 · §10-⑦ L591–619
- [m] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 계면 저항을 복셀 격자에 넣는 이산식: 상 경계 면의 컨덕턴스를 (반 복셀)/σ₁ + (반 복셀)/σ₂ + 면비저항 (Ω·cm²) 의 직렬로 — 얇은 상을 해상하지 않아도 격자와 무관한 계면 저항이 들어감 (SI S42 의 g_ij) | 단계 7 · 조건 R3 (입자 경계 면을 알아야 넣을 수 있음) · 흐름 밖: 계면 저항 | §4.3 L192–193 · §8.B-1 L315
- [m] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 슬라이스 평균 전류의 기준선: 그 높이의 평균 이온전류 ≈ f_ion(z)·J/φ(z) — 고체 분율이 바뀌는 층 경계에서 평균 전류가 분율 비만큼 뜀 (판독 1.33 / 1.6 / 2.35 ↔ 1.35 / 1.61 / 2.27) → 기준선으로 나눈 초과분만 협착 · 핫스팟 | 단계 7 (z 프로파일 보고) · 결과 전 대조 항목 (층상 구조의 경계 증폭 예측) | §3.2 L126–127 · §9 I-2 L334 · §8.B-3 L317
- [m] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 최대값 통계 대신 백분위: 모서리 (삼중선) 최대값은 격자를 조일수록 커질 수 있는 양 (계면 저항이 0 에 가까우면 특히) · 신뢰도는 길이 σ·(면비저항) 대 복셀 크기로 판단 (5 / 50 / 500 µm @1 / 10 / 100 Ω·cm²) · 이 논문은 복셀 크기가 없어 최대값 수렴을 확인할 수 없음 | 단계 7 (핫스팟 · 집중 지표 보고) · U6 (수렴을 볼 지표 고르기) | §6 L258 · §8.A-3 L310 · §9 I-4 L338
- [m] hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd | 검사 · 함정: 대표 부피는 부분 부피를 0.1 → 1.0 으로 키우며 지표의 평균 ± SD 가 평탄해지는지 (> 50 % 에서 안정) 로 봄 · 얇은 구조를 거울상으로 덧대 늘리지 않기 (대칭면 인공물) · 저항 분해는 소산전력으로 (ASR_k = P_k·A/I² · 폐계의 총 소산 = 성분 합) | 단계 5 · 7 (RVE 검사) · 흐름 밖: 충방전 계산의 저항 분해 | §3.2 L119 · §4.1 L182 · §6 L263–265 · §7.2 L297
- [m] hlushkou2018_void_space_ion_transport_assb_cathode | "공극 → SE 치환" 수치 실험과 그 한계: 같은 프레임에서 공극 복셀을 SE 로 바꾸면 수송이 얼마나 오르나 (문헌: f × 1.71 · tortuosity factor × 1.37 @ SE 0.54 → 0.67) — 단 치환은 SE 부피를 더하므로 (SE : AM 1.62 → 2.02) 부피 보존 압밀과 다름 → 치환판과 같은 SE 부피의 압밀 전 · 후 판을 둘 다 계산 | 단계 7 · 결과 전 대조 항목 (꼴) | §3-F L156 · §8-1 ① L321 · §10 L340
- [m] hlushkou2018_void_space_ion_transport_assb_cathode | 실험과 견줄 때 tortuosity factor 와 f = σ_eff/σ₀ 를 같이 적고 대조점마다 부피분율 장부를 표에: 이 논문의 "9 % 근접" (1.74 ↔ 1.6) 이 f 로는 20–24 % 차 (서로 다른 ε 로 정규화) | 단계 0 · 단계 7 (판정 기준을 f 로도 적기) · 결과 전 대조 항목 | §3-F L147–155 · §8-1 ② L322
- [m] hlushkou2018_void_space_ion_transport_assb_cathode | 형태 지표와 대표 부피: 현 길이 분포 (26 방향 · 상마다 10⁶ 현 · 경계에 닿은 현은 버림 · k-Gamma 적합 → 평균 폭 μ · 균질도 k = μ²/σ²) + 부분 부피 10 → 100 % 곡선 — 상마다 수렴 크기가 다름 (공극을 합친 상은 100 % 에서도 미수렴) · 기준점 μ_SE 5.2 µm · k_SE 1.54 | 단계 7 (SE 통로 폭 · 균질도 관측량) · 단계 5 (상자 크기 판정) | §3-D L116–126 · §4-4 L192–194 · §8-1 ④ L324
- [m] hlushkou2018_void_space_ion_transport_assb_cathode | 실험 값을 대조점으로 쓸 때의 함정: (i) 영상 시료의 "void" 가 안정화 수지를 포함 (13.2 % ≠ 잔류 기공률) (ii) 영상 시료와 전기 측정 시료가 다름 (수지 · 14 h ↔ 수지 없음 · 5 min) (iii) 저주파 호의 실축 닫힘이 측정이 아니라 적합 외삽 (iv) 기준 상태가 다름 (연속체 확산계수 ↔ 펠릿 σ) | 결과 전 대조 항목 (기공 · 수송 대조점의 확인 칸) · 단계 0 · 흐름 밖: 실험과의 대조 | §3-B L93 · §3-C L110 · §8-1 ⑥ L326 · §10 L338–339
- [m] holzer2013_constrictivity_effective_transport_porous_layers | 수송에서 되짚은 값 (ε·σ₀/σ_eff) 과 최단 경로 기하 굴곡도를 엄격히 구분하고 다른 이름 · 다른 축으로 보고 — 원문: *"must be strictly distinguished from the geometrical tortuosity (τ_geo)"* · 기하값 ≈ 1.6 평평 ↔ 수송값 최대 5.6 · 그 격차 = 협착 δ (σ_eff/σ₀ = ε·δ/τ_geo · 지수 모두 1) | 단계 7 (관측량 정의 · 보고) · 흐름 밖: 접촉망 수송의 이름 규약 | §0 L24–25 · §4-1 L120–121 · §4-6 L168 · § τ L274
- [m] holzer2013_constrictivity_effective_transport_porous_layers | 기하 협착 비는 수송 협착을 대신하지 못함: β = (r_min/r_max)² 를 δ 자리에 넣으면 8 점 중 6 점에서 저항을 13–36 % 과소 예측 → 접촉 반경 같은 기하 비로 수송 저항을 어림하지 말고 풀어서 얻은 값을 쓴다 · 기하 지표는 "기하" 표지를 달아 따로 | 단계 7 · 흐름 밖: 접촉망 수송 (협착 지표) · 계면 저항 | §3-B L96 · §4-6 L170–171 · §8 (가) L296 · (라) L308
- [m] holzer2013_constrictivity_effective_transport_porous_layers | 대표 부피 · 해상도 규칙: 목 크기 통계는 두께 > 2–5 × 최대 입자 반지름에서 안정 · 크기 분포는 그보다 큰 부피 (LSC > 6 µm) · 목은 4–5 복셀 · 입자는 > 10 복셀 · 방향 6 개 반복으로 재현성 확인 | 단계 5 · 7 (상자 크기) · U6 · U1 (특징당 복셀 수의 크기 감각) | §3-A L65 · L70 · §4-4 L155–156 · §8 (바) ⑥ L320
- [m] holzer2013_constrictivity_effective_transport_porous_layers | 기준 상태와 식 인용: 협착 분해는 "구조 없는 σ₀" (벌크 액체) 를 전제 — 펠릿 값을 σ₀ 로 쓰면 펠릿 안의 목 협착이 σ₀ 에 들어가 수송 쪽 협착과 겹쳐 셈 → 순수 SE 기준 계산을 먼저 · 식을 가져올 때는 인쇄형이 아니라 그림 수치로 검산된 꼴을 씀 (Eq. 8 은 역수로 · Eq. 9 는 부호가 바뀌어 인쇄됨) | 단계 7 (기준 상태 장부) · 흐름 밖: 문헌 식 인용 규약 | §7 L232 · §8 (바) ④ L318 · §10 L334 · L351–352
- [m] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 입자 경계 저항을 "해상된 얇은 상" 으로 넣으면 실패할 수 있음: 격자 (3.75 µm) 가 경계 두께 (nm) 를 못 풀고 임계화가 망을 끊어 저항 항을 넣고도 효과가 사라짐 (연속 막이면 ≈ 66 Ω·cm² 가 더해져야 함 · 카드 산술) → 입자 경계 면마다 면비저항으로 넣는다 | 단계 7 · 조건 R3 · 흐름 밖: 계면 저항 | §6 L90 · §8 ① L107 · §10 L119–120
- [m] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 검산법: 치밀 한 장에서 고주파 절편 = L/σ (21.9 ↔ 22.0 Ω·cm²) · 호 폭 = 2·RT/(F·i₀) (10.3 ↔ 9.2) 로 입력 표와 그림의 자기일관을 먼저 확인 | 단계 7 (수송 솔버의 해석값 검산) · 흐름 밖: 임피던스 계산 | §3 L29 · §6 L87
- [m] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 기공률만으로 수송을 판정하지 않기: 기공률이 0.20 → 0.22 로 거의 그대로 (오히려 늘었음) 인데 입자 사이 목이 자라면 저항이 −14 % · 기공 12 / 20 % 의 저항은 Bruggeman 보다 1.23 – 1.24 배 큼 (기공 형상) | 단계 0 · 단계 7 (판정 기준에 접촉 · 목 지표를 함께) · 결과 전 대조 항목 (방향) | §3 L30–31 · §5 Fig 3 L74
- [m] islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell | 기공이 전극 – SE 경계의 접촉 면적도 깎음: 호 폭 9.2 → 11.6 / 11.3 (+26 %) 을 접촉 분율 ≈ 0.79 / 0.81 로 읽을 수 있음 (카드 해석 · TREND 만) → 수송 계산에서 판 (집전 · 전극) 쪽 접촉 분율을 내부 저항과 따로 본다 | 단계 7 (경계면 접촉) · 흐름 밖: 계면 저항 · 전극 접촉 | §6 L89 · §8 ④ L110

## 카드 문제

(고치지 않고 적는다. "Minnmann 의 순수 SE 10 % @300 MPa" 를 우리 쪽 실험 앵커로 적은 카드 = **2 장** (duquesnoy2020 L401 · galvezaranda2024 L371 · L430). froboese2019 · hlushkou2018 · islam2026 에 나오는 Minnmann 은 복합 양극의 tortuosity 값이나 펠릿 σ 이고 순수 SE 기공 서술이 아니다. "인용 금지" 표지가 붙은 값이 있는 카드 = **5 장** — 숫자는 옮기지 않았다.)

**duquesnoy2020_calendering_ml_mesostructure_generator**

1. 우리 쪽 실험 앵커를 "pure-SE Minnmann 10 %@300 MPa, Cronau overlap, Bazzoun EIS" 로 적음 (L401) — 철회된 출처를 실험 근거로 쓴 서술.
2. 1 µm 껍질이 덮을 수 있는 AM 표면 비율이 자리마다 다름: 머리 요약 · 인용 문장 "~25–40 %" (L21 · L427) ↔ §5(c) "상한 23.9–65.8 % · 중앙값 39.0 %" (L302 · L504) · 같은 절의 "물리값의 1/3 이하" (L304) ↔ Q&A "1/3~1/7" (L504) ↔ "150 nm 면 6.7 배 · 50 nm 면 20 배" (L303).
3. "5 차원 다항식" (L17 · 인용 문장 "5-D polynomial" L426) ↔ 식의 입력은 넷 (AM% · ε_init · T · Gap) · 항은 여섯 (L60–62) — 무엇을 5 로 셌는지 카드에 없음.
4. 원문 (논문 · SI · 코드) 불일치를 카드가 적어 둠 (원문 문제): 본문 54 전극 ↔ SI 66 (L46) · SI Eq. S2 두께항 부호 오타 ↔ 코드 (L64) · SI 의 겹침 정의 (작은 반지름의 30 %) ↔ 코드 (반지름 합의 30 % · 6.3 배 관대 · L150) · Table S3 대칭성 오타 (L117) · 논문 "AM surface" ↔ 코드 AM ∪ CBD 표면 (L244) · 진입 스크립트의 반환값 이름 2 개 오류 (L235) · SI 그림 번호 "S2" 중복 (L442).
5. "인용 금지" 표지: 우리 쪽 격자 세 값 (원장 CL-41 · 숫자는 카드에 없음 · L400 · L444) · 같은 줄의 취소선 "보고값은 하한" 은 철회 표지 (CL-72).
6. 영문 원제가 카드에 없음 · SISSO 해석식 (L251–255) 은 "(…)" 생략이 든 기호 재현 (카드 스스로 "재구현 시 원 SI 확인 필수").
- 확인: 우리 쪽 값 (DEM E_eff 1.35 GPa · MPM E_eff 1.53 / σ_y 0.15 · L395) 은 한 곳뿐이라 카드 안 모순 없음.

**froboese2019_microstructure_ionic_conductivity_assb_electrode**

1. "인용 금지" 표지 값: 0–50 µm @60 vol% 의 인쇄 tortuosity (L100 · L126 · L168 · L428) — 카드 재계산 (≈ 80 · derived) 과 10 배 어긋남 (소수점 오기 의심 [미확인]). 저자의 "Eq 15 가 tortuosity 를 과대평가" 논증이 이 인쇄값 위에 서 있음.
2. 원문 내부 불일치를 카드 §3-6 이 적어 둠 (원문 문제): 60 vol% 굵은 두 입경의 기공률 입경 표기가 본문과 그림에서 뒤바뀜 (L169) · 본문 ρ_theo 1.93 @60 % ↔ Eq 8 로는 2.077 (L170) · 면적 A 2.01 cm² ↔ Li 박 1.131 cm² (절대 σ · R_if 에 ≤ 1.78 배 모호 · L171) · Fig 12 의 평균 방식 미기술 (L172) · "ε > 13 % 에서 ≈ 10⁻⁶" 느슨한 표현 (L173) · Fig A1 캡션 단위 · 분율 가짓수 "six ↔ five" (L174–175).
3. § τ 정의 대조 표의 N_M 값: "60 % 굵은 쪽 29–43" (L314) 은 1/f (f 0.035 · 0.023 · L105 · L110) 로는 맞지만, 같은 줄에 적힌 식 N_M = τ/φ_el 에 표의 τ (≈ 11.5 · 18.0) 와 φ_el (0.335 · 0.343) 을 넣으면 34–52 (내 검산) — §3-6 (f) 의 평균 방식 차이와 같은 뿌리로 보임.
4. 다른 카드 · 문서의 정정 후보를 카드가 적어 둠 (고치지 않음): famprikis2019 카드가 이 논문을 σ_y(SE) · K_Ic · µ 조달 대상에 넣었으나 기계 물성이 없음 (L440) · bielefeld2020 카드의 "Froboese 와 비슷" 은 Bruggeman 지수 관례 표지가 필요 (L442) · comparison 문서의 조달 추천에 "고분자 모델계" 한정어 누락 (L441).
5. [미확인] 으로 남은 것: 압분 온도 (L73) · SE 과립 크기 (L227) · 오차막대의 통계 정의 (L114) · 참고문헌 32 의 권 · 쪽 (L452) · 참고문헌 37 · 50 의 저널 표기 (L457 · L460).
- 확인: 우리 σ₀ 3.0 mS/cm 를 "LPSCl 펠릿값 입력, CL-91" 로 적음 (L304 · L342) · 순수 SE 침대 기공 ≈ 12 % (L408) 는 랩 기준 안 · Minnmann 은 τ² 와 복합 양극 "공통 14 %" 로만 나오고 (L319 · L363), 카드가 "LPSCl 순수 SE 기공 앵커로 쓰지 않는다 (CL-94 제안 맥락)" 고 적음 (L370).

**galvezaranda2024_time_dependent_dl_calendering_microstructure**

1. 우리 쪽 실험 앵커를 "Minnmann 10 %@300 MPa · Cronau overlap 11–12 % · Bazzoun EIS σ · Lee2025 σ_e" (L371) · "Minnmann · Cronau · Bazzoun · Lee2025" (L430) 로 적음 — 철회된 출처를 실험 근거로 쓴 서술. L420 은 출처 없이 "pure-SE 10 %@300 MPa" (값은 랩 기준 창의 아래 끝).
2. 계보 카드 (ngandjong2021) 의 압력축: "0–156 MPa" 로 정정했다고 적고 (L183 · L187–190 · L704) 도 두 곳에 "0–160 MPa" 가 남아 있음 (L422 · L718).
3. §10-② 의 "Table S2 의 micro-I @CD20 31.09 %" (L534) — 카드가 옮긴 §3-C 표 (시험 11 행 · L119–131) 에는 그 행이 없고 (미세구조 I 은 @45 만), 프레임 0 (압연 전) 의 라벨 기공률을 CD 20 % 값과 견줌.
4. 원문 내부 불일치를 카드 §10 이 적어 둠 (원문 문제): Table S2 미세구조 I @45 % 행의 확산도 · τ 가 DEM 과 DL 이 완전히 같음 (전사 오류 의심 · L133–135) · 본문 "오차 0.5–9.8 %" ↔ SI 13.76 · 14.71 % (L543–549) · "R² 항상 90 % 이상" ↔ Fig 6b ≈ 87.2 % (L551–553) · 데이터셋 개수 28 ↔ 35 · 검증 분할 80:20 ↔ 90:10 (L580–589) · Fig 7h ↔ Table S2 계열 뒤바뀜 (L621–626) · 추론 방식 (자기회귀인지 한 걸음 예측인지) 을 Fig 3 과 Fig 5c 가 다르게 말함 (L555–576 · 카드 판정 "미해결").
5. τ 범위를 "9.7 → 85.3 (CD 20 → 50 %)" 로 적음 (L426 · L671) — 표에서 9.74 는 미세구조 III @25 % 이고 (L123), CD 20 % (미세구조 IV) 는 10.63 (L125).
6. 영문 원제가 카드에 없음 · 하드웨어 · DEM 물성 미기재 (원문).
- 확인: 되돌아옴 값 (4.8 / 7.6 / 10.1 %p) 은 논문 값이 아니라 카드의 그림 판독 (TREND only) 이고, 머리 요약 (L34) · 표 (L81) · §3-D 에 derived(ours) 표지가 붙어 있음 (인용 문장 절에는 이 값이 없음) · 우리 쪽 값 (E_eff 1.35 GPa L427 · MPM champion E 1.53 / σ_y 0.15 L428 · 플래튼 관련 수치 L398–402) 은 카드 안에서 서로 다르지 않음.

**hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd**

1. "인용 금지" 표지 값: "0.4 µm (134.1 mV) 기준" 으로 적힌 CCD · 한계 저항 수치들 (L321 · 값이 놓인 자리 L13 · L156–161) — 카드 산술로는 인쇄 수치가 1.0 µm (84.8 mV) 문턱에서 재현됨 (문턱 라벨 ↔ 인쇄 수치 불일치 · L332 · L358). 원문 문제.
2. 원문의 캡션 – 그림 불일치: Fig 8 · Fig S9 캡션은 계면 저항 0 조건을 적지만 그림에 없음 · Fig S7 캡션 문장이 끊김 (L367) · 어느 재구성을 거울상으로 덧댔는지 미기재 (L366).
3. 우리 쪽 실 영률을 한 카드 안에서 다르게 적음: "실 E ≈ 22–24 GPa" (L275) ↔ "E_eff 연화 (24 → 1.35/1.53)" (L291).
4. [미확인] 으로 남은 것: 권 · 호 (L27) · 코드 공개 (L36) · 치밀층 조성 (L57) · 복셀 크기 · 격자 수 (L110) · 선형 솔버 (L198). 문턱 재현 (D2) 에 쓴 Li 몰부피 13.00 cm³/mol 은 논문에 인쇄되지 않은 카드 입력 (L112 · L415).
- 확인: 우리 σ_grain 3.0 mS/cm 를 "펠릿값 규약" 으로 적음 (L275) · Minnmann 서술 없음.

**hlushkou2018_void_space_ion_transport_assb_cathode**

1. 원문 내부 불일치 · 산술을 카드 §10 이 적어 둠 (원문 문제): EIS 주파수 범위 본문 500 kHz ↔ Fig 2 캡션 1 MHz (L345) · Bruggeman 1.34 @ε 0.537 ↔ 검산 1.365 (L346) · "(66.9% LCO, 33.1% SE)" 뒤바뀜 (L347) · "13 % 상대 증가" 는 실제로 절대 13.2 %p (상대 +24.6 % · L348).
2. void 13.2 % 가 "수지 + 잔류 공극" 이라는 한정어가 다른 카드에는 빠져 있다고 카드가 적어 둠 (고치지 않음): bielefeld2020 의 "void 15 % (Hlushkou 2018 류)" · minnmann2021 의 "기공 13–17 % 비교 문헌" · 메모 v2 §8-1 #6 (L351–354).
3. τ_cond 1.6 을 원문 숫자로 정확히 재현할 수 없음: Eq. 3 에 넣은 ε · 전극 면적 · 측정 온도가 원문에 없음 — 카드 역산은 면적을 셀 틀 내경 9.8 mm 로 **가정** 해 1.53 @ε 0.62 (L94–97 · L341).
4. 압력 환산 "4 t/cm² ≈ 392 MPa · 1 t/cm² ≈ 98 MPa" 는 카드의 환산 (tonne-force 가정 · L79) · 영문 원제는 PDF 파일명으로만 있음 (L8).
- 확인: 우리 σ₀ 3.0 을 "펠릿, 원장 CL-91" 로 적음 (L254 · L288) · "LPSCl 앵커 = Minnmann" (L19 · L317) 은 복합 양극의 tortuosity 대조점을 가리킴 (순수 SE 기공 아님).

**holzer2013_constrictivity_effective_transport_porous_layers**

1. "인용 금지 수준" 표지 값: Archie 지수의 재료 배정 (L62 · L108 · L335 · L355) — 카드의 벡터 추출 재맞춤으로는 두 재료가 뒤바뀐 꼴 · 원자료 [37] 미열람.
2. 원문 오식 · 불일치를 카드가 적어 둠 (L347–358 · 원문 문제): Eq. 5 인쇄형이 뜻과 반대 · "β is identical with τ" · "β = 1.77" (Eq. 6 의 β ≤ 1 · 그림 4 의 0.177 과 어긋남 · L72 · L350) · Eq. 8 이 Eq. 3 의 역수로 인쇄 · Eq. 9 의 부호 · 그림 16 범례 · 그림 11 계산값이 정확히 × 1.20 [원인 미확인] · 시료 W4 의 δ 가 그림 15 (0.792) 와 그림 12 로 계산한 값 (0.920) 에서 다름 (L93 · L104 · L356) · 기호 γ 이중 사용.
3. "c-PSD r50 / MIP r50 2.5 배 (157 / 66)" (L69) — 적힌 두 수로는 2.38 (내 검산) · 6 방향 값 64 nm (L74) 로는 2.45.
4. 값의 지위: §3-B 의 8 시료 표는 본문 명시값이 아니라 그림 벡터 추출 (≈ · L81–93 · L333) · §7 – §8 의 우리 쪽 수치는 메모 v2 의 유도값이고 이 카드에서 다시 계산하지 않음 (L336) · 전작 [37] 은 "(in press)" 서지만 있고 미열람 (L44 · L358).
- 확인: 우리 σ₀ 3.0 mS/cm 를 "펠릿값 (원장 CL-91)" 로 적음 (L232 · L252) · Minnmann 서술 없음.

**islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell**

1. "인용 금지" 표지: "GB minor" (입계 상을 넣어도 임피던스가 안 변한다는 결과 · L120 · 값이 놓인 자리 L33 · L76) — 카드 판정 "표현 규약의 결론" · 우리 랩 EIS (Kim 2025) 와 충돌 (L97).
2. 우리 σ_grain 3.0 을 "Cronau 단결정" 으로 적음 (L22 · L98 · L133) ↔ 같은 배치의 froboese2019 L304 · hamann2026 L275 · hlushkou2018 L254 · holzer2013 L232 는 "펠릿값 (CL-91)" — 카드 사이에서 우리 쪽 값의 지위가 다름.
3. "실 LPSCl 분말 (D50 ≈ 1.5 µm) 보다 40 배 큰 입자" (L28 · L119) — 반경 60 µm 를 지름 (D50) 1.5 µm 로 나눈 값 · 지름끼리면 80 배 (내 검산).
4. 서지 지위: 저널 · DOI 미확인 원고 (L3 · L6 — "게재본에서 수치가 바뀔 수 있다") · i₀ 의 출처가 "Exp" 로만 (L23 · L117) · Fig 9 캡션의 SEM 출처 "[10]" 은 "[16]" 의 오기 (L124).
- 확인: Minnmann 은 펠릿 σ "1.6 (Kim 2025/Minnmann)" 로만 나옴 (L98 · L133) — 순수 SE 기공 서술 없음.
