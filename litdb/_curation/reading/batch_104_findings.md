# batch 104 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `meyer2017_calendering_compaction_resistance_line_load_exponential_model` — C. Meyer, H. Bockholt, W. Haselrieder, A. Kwade, "Characterization of the calendering process for compaction of electrodes for lithium-ion batteries", Journal of Materials Processing Tech. 249 (2017) 172–178, doi:10.1016/j.jmatprotec.2017.05.031 (본문 7 쪽 · SI 없음 · 카드 = `litdb/papers/meyer2017_calendering_compaction_resistance_line_load_exponential_model.md`).
리튬이온 전극 둘 (NCM 양극 · 흑연 음극 · 액체 전해질) 을 파일럿 캘린더로 누르며 선하중 (N/mm) 과 압연 뒤 코팅 밀도 · 기공률을 잰 공정 논문이다.  고체전해질이 없고, 하중이 압력으로 환산돼 있지 않고, 값이 전부 압연 뒤 (하중을 뺀 뒤) 것이며 입자 계산이 없다 — 아래 '없음' 은 그 때문이다.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질이 없는 리튬이온 코팅 · 압력 축 없음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 되돌아옴을 재지 않았다.  원문은 *"Leaving the gap the coating undergoes an elastic relaxation"* 한 문장뿐이고, 밀도 · 기공률은 모두 롤을 지난 전극 (하중 0) 에서 다이얼 게이지 두께 (분해능 1 µm) + 질량으로 구한다 — 하중 아래 간극 · 밀도 · 회복 크기 · 압연 뒤 측정까지의 시간이 없다 | 카드 §0 ⑨ · §4-4 (iv) · 논문 p.172 · p.174 | 인쇄 · 미확인 | 액체 리튬이온 압연 전극 · 회복 숫자 없음 (같은 그룹의 순간 회복 = `diener2022_roll_gap_springback_calendering`)
- [b] meyer2017_calendering_compaction_resistance_line_load_exponential_model | (인용으로만) 일축 가압에서는 유지 시간이 길수록 기공률이 뚜렷이 작다 — *"longer hold times during uniaxial compaction lead to a significant smaller porosity"* (Manev 외 1995 를 인용) | 카드 §3-7 · 논문 p.172 | 인쇄 (인용 근거) | 이 논문의 측정이 아니다 · 값 없음

## c — 항복 · 경도 · 크리프 값과 정의
- [c] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 항복 · 경도 · 크리프 값 없음 ('harder' 는 수치 없는 서술).  압밀 저항을 재는 수는 식 (4) 의 **γ_C "compaction resistance" (N/mm)** — NCM 양극 292 ± 9 / 309 ± 45 · 흑연 음극 126 ± 26 / 144 ± 24 N/mm (2 / 5 m/min).  선하중 단위라 일축 항복 세기와 견줄 환산이 원문에 없다 (Heckel 은 *"reminds of"* 한 문단 · Heckel 좌표 · K · P_y 없음).  카드 산술: 식 (4) 는 Heckel 의 한계 밀도를 자유 매개변수로 푼 꼴 (γ_C ↔ 1/K) | 카드 §3-4 · §3-10 · 논문 p.175 · 표 2 | 인쇄 · 카드 산술 | N/mm · 액체 리튬이온 코팅 · 압연 뒤 값 — 우리 Heckel P_y (MPa · 순수 SE) 와 나란히 못 놓는다

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 하중 몫 · 응력 숫자 없음.  전극 단위의 정성 대비만: 단단한 구형 NCM (12 µm · 86 wt%) 코팅의 γ_C 가 무른 판상 흑연 (20.9 µm · 85 wt%) 코팅의 2.1–2.3 배 · 같은 기하 기공률 0.30 에 드는 선하중 633 ↔ 202 N/mm (3.1 배 · 카드 산술).  저자 이유 = NCM 이 단단해 입자 재배열 · 마찰에 큰 힘이 든다 (*"assumed but not clearly reduced"*) + NCM 구의 조밀한 충전이 입자 간 마찰을 키운다 (*"possibly"*) + 음극은 쉽게 눌리는 큰 기공 몫이 크다 (코팅 부피의 40.3 ↔ 25.8 %) | 카드 §3-4 · §3-6 · §4-4 (ii) · 논문 p.175–176 | 인쇄 · 카드 산술 | 두 전극은 조성 · 입자 모양 · 크기 · 부하 · 바인더가 함께 달라 저자 스스로 *"no direct comparison … is possible"* · 단단한 입자 + 무른 입자의 혼합이 아니라 전극 둘의 비교

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙을 다루지 않는다 · 입자 계산 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (두께 평균 측정 + 수은 압입 + 2D 단면 영상 4 장 (정량 없음) · 전이에 대한 말 없음 — 카드 §4-4 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] meyer2017_calendering_compaction_resistance_line_load_exponential_model | AM + SE 복합이 아니다 (NCM + 도전 탄소 + 흑연 첨가제 + 바인더 · 액체 전해질용).  압력 대신 **선하중별 · 압연 뒤** 기공률만 있다 — NCM 양극 (5 m/min) 0 · 58 · 118 · 375 · 1065 N/mm ↔ 기하 0.570 · 0.518 · 0.457 · 0.358 · 0.260 / 수은 압입 0.491 · 0.465 · 0.401 · 0.255 · 0.183 · 맞춤식 ε_ph = 0.26 + (0.57 − 0.26)·exp(−q_L/309 N/mm) · ε_Hg = 0.16 + (0.52 − 0.16)·exp(−q_L/340 N/mm) | 카드 §3-3 · §3-4 · §3-5 · 논문 Fig 6 · Fig 8 (범례) | 판독 (점) · 인쇄 (맞춤식) | 고체전해질 없음 · 선하중을 압력으로 바꾼 값이 원문에 없다 · 뺀 뒤 값 · 기하 기공률의 분모 = 가스 피크노미터 혼합물 밀도 4.3 g/cm³

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 원문이 적은 한계: 끝점 (최대 밀도 · 최소 기공률) 을 식의 외삽으로 정했다 — *"to find an alternative way of determinating the end point of compaction (maximal density or minimal porosity) instead of extrapolation of this equation, would be a complementary approach"* · 두 전극은 *"no direct comparison … is possible"* · 경도 · 마찰 설명은 *"assumed but not clearly reduced"* · 앞으로 = 재료 · 조성 · 질량 부하 · 롤 온도 · 압연이 전극 기계 물성에 주는 영향 | 카드 §0 ⑪ · 논문 p.173 · p.175 · p.178 | 인쇄 | 공정 식의 한계이고 입자 계산의 한계 진술은 아니다
- [j] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 카드가 적은 한계: 선하중 → 압력 환산 없음 · 압연 뒤 값 · 곡선마다 5 점에 3 수 (자유도 2) · 끝점이 맞춤 범위에 따라 변함 (음극 1.74 → 1.80 g/cm³ · γ_C 144 → 161) · '닫힌 기공' 설명의 약점 셋 · 인쇄 어긋남 14 건 (표 1 의 '코팅 두께' = 집전체 포함 값 등) | 카드 §3-4 · §3-5 · §3-11 · §11 | 카드 산술 · 카드 추론 | —

## k — DEM 의 한계
- [k] meyer2017_calendering_compaction_resistance_line_load_exponential_model (Meyer 외, J. Mater. Process. Technol. 249 (2017) 172–178) | **말 없음** — 이 논문은 DEM 을 쓰지도 언급하지도 않는다 ('DEM' · 'FEM' · 'simulation' · 'discrete' 0 회 · 인용한 계산은 유효 전도의 저항망 모델 둘뿐) | 카드 §4-4 (i) · 원문 대조 기록 | 인쇄 (전수 검색) | —

## l — 소성변형이 왜 어려운가
- [l] meyer2017_calendering_compaction_resistance_line_load_exponential_model (Meyer 외, J. Mater. Process. Technol. 249 (2017) 172–178) | 원문은 입자 소성을 계산에 넣기 어려운 이유를 논하지 않는다 (말 없음 · 'plasticity' 는 intro 의 인용 한 번).  택한 길 = **입자를 풀지 않는 현상 식**: 선하중 ↔ 압연 뒤 밀도에 ρ_C = ρ_C,max − (ρ_C,max − ρ_C,0)·exp(−q_L/γ_C) 를 맞춘다 — 맞춘 값 = 곡선마다 2 개 (본문: ρ_C,max · γ_C) 또는 3 개 (표 2 의 ρ_C,0 에도 표준오차 · 카드의 재맞춤이 3 수 가중 맞춤으로 표 2 를 재현) · 무엇에 = 파일럿 캘린더 실측 5 점 (음극 연장 12 점) · 검증 = 좁은 범위 (≤ 181 N/mm) 식이 331 N/mm 까지는 ±0.013 g/cm³ 로 맞고 그 위에서는 0.03–0.04 g/cm³ 낮게 예측 (카드 산술) · 비용 = 계산 없음 | 카드 §3-4 · §4-3 · 논문 p.175 · 표 2 · Fig 8 | 인쇄 · 카드 산술 | 식은 유도가 아니라 맞춤이고 재료 물성 (경도 · 마찰) 과의 연결은 가정 · N/mm · 액체 리튬이온 코팅

## m — 받아들일 통찰
- [m] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 무엇을: 압밀 곡선을 요약할 식을 결과 전에 고른다 — Heckel 직선 (한계 = 진밀도 · 2 수) 인가 한계를 푼 지수 포화 (3 수) 인가.  한계가 있는 자료는 Heckel 좌표에서 휜다 (이 논문 자료에서 국소 1/K 가 574 → 5629 N/mm · 219 → 1656 N/mm 로 7.6–9.8 배 변함).  어디에: 후보 M0 ; 단계 0 | 카드 §3-10 · §9-1 · 논문 식 (4) · 표 2 | 인쇄 + 카드 산술 | 선하중 축 자료에서 본 꼴이고 우리 순수 SE 4 압력 자료가 휘는지는 따로 봐야 한다
- [m] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 무엇을: 끝점 (최소 기공률 · 최대 밀도) 은 외삽이라 맞춤 범위를 값 옆에 적는다 — 같은 음극을 ≤ 181 N/mm 로 맞추면 1.74 g/cm³ · γ_C 144, 728 N/mm 까지면 1.80 · 161, 실측 1.77 이 좁은 범위 끝점을 넘는다 · 저자도 외삽 아닌 방법이 필요하다고 적는다.  어디에: 후보 M0 (맞춤 범위 · 가중 · 점 수 · 자유도 병기) | 카드 §3-4 · 논문 표 2 · Fig 8 캡션 · p.178 | 인쇄 + 카드 산술 | —
- [m] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 무엇을: 기공률 값에 연산자 · 분모 밀도 · 측정 창을 붙인다 — 같은 NCM 양극이 기하 (질량 · 두께 · 피크노미터 4.3 g/cm³) 57.0 → 26.0 % ↔ 수은 압입 (8 nm–10 µm) 49.1 → 18.3 % · 차 5.3–10.3 %p 이고, 분모 밀도 (피크노미터 4.3 ↔ 성분 합산 ≈3.9) 만으로도 같은 크기가 움직인다 → 복합 양극 실측과 견줄 때 NCM 밀도 (결정 ↔ 입자 겉보기) 칸을 둔다 · '코팅 두께' 가 집전체 포함 값으로 인쇄된 실례 (표 1) 도 있다.  어디에: 단계 0 | 카드 §3-1 · §3-5 · 논문 Fig 6 · 표 1 · p.176 | 판독 · 카드 산술 | 액체 리튬이온 코팅 · '닫힌 기공' 의 직접 정량은 원문에 없다
- [m] meyer2017_calendering_compaction_resistance_line_load_exponential_model | 무엇을: 압연 문헌의 선하중 (롤 힘 ÷ 코팅 폭 · N/mm) 은 접촉 길이 가정 없이 MPa 로 옮기지 않는다 — 이 논문은 환산을 주지 않는다 · 카드 어림 (접촉 길이 √(R·Δh)) 은 평균 ≈7–220 MPa · 체류 30–155 ms 의 자릿수 감각일 뿐이다.  어디에: 흐름 밖: 압연 (롤) 문헌을 일축 300 MPa 계산 옆에 놓을 때의 읽는 법 | 카드 §3-9 · 논문 p.174 | 인쇄 (정의) · 카드 추정 (압력) | 카드 추정은 원문 값이 아니다 (인용 금지)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Heckel, R.W., 1961. Density-pressure relationships in powder compaction. Transa. Metall. Soc. AIME 221, 671–675. | c · m — Heckel 식의 원전 (이 논문 식 (4) 가 닮았다고 한 식 · 우리 Heckel 트랙의 뿌리 · K · P_y 의 정의와 항복 세기 환산이 원문에 어떻게 적혀 있는지) · 카드 §3-10 · §12 | litdb 확인: ls 'heckel' = `lee2025_heckel_argyrodite_powder_densification_nanoindentation` 뿐 (다른 논문) · '221, 671' · 'Density-pressure relationships' grep 0 건 → 카드 없음 (`lee2025_heckel_*` · `faka2026_*` 카드는 같은 권의 1001–1008 쪽을 인용 — 같은 해의 다른 논문인지 [미확인])
- [n] Manev, V., Naidenov, I., Puresheva, B., Pistoia, G., 1995. Effect of electrode porosity on the performance of natural Brazilian graphite electrodes. J. Power Sources 57 (1–2), 133–136. | b · m — 일축 가압에서 유지 시간이 길수록 기공률이 작다는 주장의 원 자료 (가압 유지 시간 효과 · 카드 §3-7 · 논문 p.172) | litdb 확인: ls 'manev' 없음 · 'Manev' grep = `matthews2024_ptfe_nanofibril_network` 본문 언급 하나 → 카드 없음
- [n] Antartis, D., Dillon, S., Chasiotis, I., 2015. Effect of porosity on electrochemical and mechanical properties of composite Li-ion anodes. J. Compos. Mater. 49 (15), 1849–1862. | c · i 근처 — 일축 열간 가압의 **압력** ↔ 음극 기공 · 기계 물성 (이 논문에 없는 압력 축 · 논문 p.173 은 "식으로 잇지 않았다" 고만 적는다 · 카드 §12) | litdb 확인: ls 'antartis' 없음 · grep 0 건 → 카드 없음
- [n] Schilcher, C., Meyer, C., Kwade, A., 2016. Structural and electrochemical properties of calendered LMO cathodes. Energy Technol. 4, 1–8. | k · 조건 R7 — 압연 밀도 ↔ 활물질 입자 파쇄 (LMO) (논문 p.173 · 카드 §4-4 (ii) · §12) | litdb 확인: ls 'schilcher' 없음 · grep 0 건 → 카드 없음
- [n] Ott, J., Völker, B., Gan, Y., McMeeking, R.M., Kamlah, M., 2013. A micromechanical model for effective conductivity in granular electrode structures. Acta Mech. Sin. 29 (5), 682–698. | m · 흐름 밖 (접촉망 수송) — 입자 구조의 저항망 유효 전도 모델 (일축 압축 · 활물질 팽창의 영향 포함 · 논문 p.173 · 카드 §12) | litdb 확인: ls 'ott' 없음 · 'Kamlah' · 제목 grep 0 건 → 카드 없음
- (참고 · 후보로 세지 않음) Völker, B., McMeeking, R.M., 2012. J. Power Sources 215, 199–215 (위 모델의 원형) · Froboese 외, Mater. Charact. (accepted · 권 · 쪽 원문에 없음 = 서지 일부만 — 이 논문의 수은 압입 절차) = 정본에 카드 없음 (`froboese2019_microstructure_ionic_conductivity_assb_electrode` 는 다른 논문) · 뒤 논문 Meyer 2018 (J. Energy Storage 18, 371–379) = 후보 표 N-61 (차례 대기).

## 카드 문제
- `he2026_dem_calendering_inhomogeneity_areal_density` L688 — "압연의 **Heckel 지수 기반 하중-변위 경험모델 + "compaction impedance"** 원전": 원문은 선하중 (N/mm) ↔ 압연 뒤 코팅 밀도 · 기공률의 지수 포화 식이고 (가로축에 변위 · 간극 없음 · 간극 값 미인쇄), 용어는 **"compaction resistance" γ_C** 다 ('impedance' 는 intro 의 *electrochemical impedance* 한 번뿐).  Heckel 은 *"The exponential relation reminds of the compaction equation of Heckel (1961)"* 한 문단 — 유도가 아니라 닮음.  같은 줄 "우리 Heckel 트랙의 직접 문헌 대응물" 도 축 (N/mm) · 재료 (액체 리튬이온 코팅) · 상태 (압연 뒤) · 한계 밀도 (자유) 가 달라 값의 짝은 못 된다.
- `he2026_dem_calendering_inhomogeneity_areal_density` L414 — "(intro 에서 Meyer 2017 의 "Heckel exponent" 를 인용만 한다)": 원문에 'Heckel exponent' 라는 표현이 없다 ('exponent' 로 시작하는 낱말 5 회는 전부 exponential(ly)).  이 낱말이 He 2026 원문의 표현인지 그 카드의 요약인지는 [미확인] (He 2026 PDF 는 이 작업에 없다).
- `heck2026_densification_sulfide_se_binder_scalable` L184 — "Meyer 지수식 … — Heckel 과 다른 식": 틀린 것은 아니다 (그 논문은 압력 P 로 바꿔 쓴다) · 다만 대수로는 Heckel 의 한계 밀도를 자유 매개변수로 푼 꼴이라는 점이 빠져 있다 (카드 §3-10 [카드 산술] · 고칠 문제는 아님).
- `diener2022_roll_gap_springback_calendering` L142 · `zhang2026_xct_dem_cathode_calendering_peel_calibration` L92 · `lu2020_insitu_nanoct_calendering_microstructural_evolution` L424 — 서지 · 식 · 요약이 원문과 같다 (문제 없음).
- 후보 표 N-55 의 '왜' 칸 ("Heckel 지수 기반 하중-변위 경험모델 + 'compaction impedance' 원전 · 단계 5") — 위 he2026 L688 을 그대로 옮긴 것이라 같은 차이가 있다.  후보 표는 고치지 않았다 (메인 세션 소관).
