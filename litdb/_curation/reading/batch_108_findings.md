# batch 108 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `cottrino2013_insitu_xct_granulated_alumina_die_compaction` — S. Cottrino, Y. Jorand, E. Maire, J. Adrien, "Characterization by X-ray tomography of granulated alumina powder during in situ die compaction", Materials Characterization 81 (2013) 111–123, doi:10.1016/j.matchar.2013.04.004 (본문 13 쪽 · 보충 자료 없음 · 카드 = `litdb/papers/cottrino2013_insitu_xct_granulated_alumina_die_compaction.md` · 후보 표 N-62).
분무 건조한 나노 알루미나 과립 (전지 재료 아님) 을 흑연 금형 (안지름 3.5 mm) 안에서 7 → 113 MPa 로 누르며 단계마다 꺼내지 않고 실험실 X 선 단층 촬영 (복셀 2.5 µm) 으로 본 실험 논문이다.  계산 (DEM · FEM · MPM) · 황화물 · 복합 양극 · 탈압이 없다 — 아래 '없음' 은 그 때문이다.  **방법은 옮길 수 있고 값은 옮길 수 없다.**

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (황화물 아님 · 진밀도 · 질량 기준 기공률 · 압밀 곡선 미게재).  참고로만: 한 성분 알루미나 과립의 '2 µm 보다 큰 영상 기공' 압력 계열이 있다 (m 첫 항목 · 카드 §3-4) — 전체 기공률이 아니다.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (금형에서 꺼내지 않고 가압만 · 감압 단계 · 꺼낸 뒤 치수 · 유지 중 이완 기록 없음 — 카드 §0 ⑩ · §4-4 (iv)).  원문의 말은 예상 한 줄뿐: *"in uniaxial pressing, it is hardly conceivable. Indeed, due to die friction effects during ejection step, the green parts will be destroyed."* (p.123 · 바인더 없는 과립 · 측정 아님).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] cottrino2013_insitu_xct_granulated_alumina_die_compaction | **과립 (응집체) 항복 압력 Py** = 밀도–log(압력) 압밀 곡선의 첫 꺾임 (재배열 구간 → 과립 파쇄 · 소성 변형 구간): 바인더 있음 R.H. 5 **5 MPa** · R.H. 90 **1.8** · 바인더 없음 R.H. 5 **2.1** · R.H. 90 **1.5 MPa** — 재료의 항복 · 경도가 아니라 과립 강도의 척도 · 일축 항복 세기와의 환산 없음 | 카드 §3-3 · §7-3 · 논문 p.111–112 (정의) · p.117 · Table 2 | [인쇄] | 압밀 곡선 · 측정 장치 · 시료 크기 미게재 · Heckel 의 P_y (= 1/K) 와 다른 정의 (같은 표에 놓지 않는다) · 알루미나 과립
- [c] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 바인더 (PEO) 유리 전이 **40 °C @ R.H. 5 %** · **−19 °C @ R.H. 90 %** (DSC) → 건조 = 취성 파쇄 · 습윤 = 소성 변형으로 과립 거동이 갈린다 | 카드 §3-1 · §3-3 · 논문 p.112 · p.116 | [인쇄] | 과립 한 알 강도 · 경도 측정 없음 · 크리프 없음 (단계당 ≈30 분 스캔 동안의 하중 유지 방식 · 이완 [미확인])

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 혼합이 아니다 (한 종류 과립) — 하중 몫 · 재밍 값 없음.  닿는 정성 둘: ① 과립이 무를수록 (습도 · 바인더) 밀도 불균일이 커진다 — *"The pellet homogeneity increases with the granule stiffness"* (p.116) ② 크기 효과 인용 — *"smallest granules see the highest stresses and are thus easier to destroy [10]"* (p.119) · 끝까지 남는 것은 가장 큰 과립의 가운데 공동 | 카드 §3-3 · §3-7 | [인쇄] | 정성 · 응력 · 힘 측정 없음 · 단단한 + 무른 두 상의 분담이 아님

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙 · 입자 계산 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  영상 해상도 참고: 복셀 2.5 µm · 과립 지름당 20 (D50 50 µm) · 35.6 (89 µm) 복셀 [카드 산술 · §3-2] — 이 해상도에서도 17–19 MPa 의 파쇄는 *"difficult to observe due to insufficient resolution"* (p.116) · 기공은 2 µm 초과만 (복셀 하나의 등가 지름 3.1 µm [카드 산술]).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (촬영 · 분할 · 통계는 3D · 그림과 파쇄 양식 판단은 2D 단면 · 전이에 대한 말 없음 — 카드 §4-4 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (계산 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (전지 재료 아님 · 한 성분).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 원문이 적은 한계: (1) 밀도 지도는 회색값 미보정 — *"a density comparison sample-by-sample or pressure-by-pressure is not possible, since no calibration of the grey-level scale was made"* (p.113) (2) 빔 경화가 R.H. 90 시료에서 뚜렷 (p.113 · Fig 2) (3) 17–19 MPa 의 파쇄는 해상도 부족으로 관찰 곤란 (p.116) (4) 2 µm 아래 (수십 nm) 기공은 *"not detected in our measurement"* (p.122) (5) 가장 낮은 촬영 압력 8 MPa 가 Py 보다 높다 → *"a similar study should be performed at lower pressures"* (p.117) (6) 건조 두 배치의 처음 상태 재구성 실패 (p.120) (7) 금형이 작아 표준 탭 시험을 못 하고 손으로 다짐 (p.114) | 카드 §0 ⑪ · §11 | [인쇄] | —
- [j] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 카드가 적은 한계: 압밀 곡선 · 힘–변위 · 상대밀도 · 마찰 계수 · 탈압 · 반복 시료 없음 (DEM 검증 표적으로는 높이 · 보이는 기공 · 결함 통계 [전부 판독] 뿐) · 스캔 중 하중 유지 방식 미기재 · R.H. 90 지도의 '벽 쪽 치밀' 과 빔 경화가 분리되지 않음 [카드 비판] · Fig 9 ↔ Fig 10 의 '처음 상태' 가 다름 [판독] · Fig 7 · Fig 13 캡션의 패널 표기가 본문 · 축과 어긋남 | 카드 §3-6 · §3-7 · §3-10 · §11 | [판독] · [카드 비판] | —

## k — DEM 의 한계
- [k] cottrino2013_insitu_xct_granulated_alumina_die_compaction (Cottrino 외, Mater. Charact. 81 (2013) 111–123) | **말 없음** — DEM 을 쓰지 않는 실험 논문이고 DEM 의 한계를 논하지 않는다.  DEM 이 나오는 유일한 문장: *"General results indicate that a high hygrometry, increases the overall density of the compact but affects the internal density distribution in the sample [11]. This phenomenon has been reproduced with a discrete element modelling [1]. It was shown, in this last study that more severe density gradients were observed in humid samples."* (p.112 · [1] = Kong & Lannutti 2000 — 원 논문 미확인) | 카드 §4-4 (i) | [인쇄] | 한계 진술이 아니라 'DEM 이 경향을 재현했다' 는 인용
- [k] cottrino2013_insitu_xct_granulated_alumina_die_compaction (Cottrino 외, Mater. Charact. 81 (2013) 111–123) | 깨지지 않는 구 DEM 이 담지 못하는 단계의 **실측 근거** (모델에 대한 말은 아님): '입자' 가 다공성 응집체일 때 Py (1.5–5 MPa) 를 넘긴 8 MPa 에서 과립이 깨지거나 (바인더 없음 · 건조 바인더 = 취성) 눌리기 (습한 바인더 = 소성) 시작하고 — *"at 8 MPa granules have only began to deform or fracture"* (p.117) — 110 MPa 에는 속 빈 과립의 가운데 공동만 남는다 (가장 큰 결함 열 개 평균 54–86 µm · Table 3) · 27–28 → 110 MPa 구간 높이 감소 (10–17 %) 의 53–83 % 는 영상이 못 보는 과립 속 기공 몫 | 카드 §3-3 · §3-5 · §3-9 · 논문 p.116–119 · Fig 6 · 7 · 10 | [인쇄] + [판독] + [카드 산술] | 알루미나 과립 · 값 전이 불가 · DEM 과의 대조는 이 논문에 없다

## l — 소성변형이 왜 어려운가
- [l] cottrino2013_insitu_xct_granulated_alumina_die_compaction (Cottrino 외, Mater. Charact. 81 (2013) 111–123) | **말 없음** — 계산이 없어 소성을 넣기 어려운 이유 · 우회 · 맞춘 값 · 계산 비용에 대한 논의가 없다.  관측만: 같은 조성의 과립이 바인더의 유리 전이를 사이에 두고 취성 파쇄 ↔ 소성 변형으로 갈린다 — *"granules with a low Tg binder have a plastic behaviour and granules without binder or with a high Tg binder have a brittle behaviour. Thus, the fracture behaviour of the granules is related to the nature of the interparticle bounding inside each granule."* (p.116) · 습한 바인더 과립은 Py 뒤에도 자리를 바꾼다 — *"between 7 and 19 MPa, it is impossible to follow the evolution of the same granules. This is in opposition with the idea that reorganisation of granules occurs only in stage I"* (p.119) | 카드 §3-3 · §4-4 (ii) | [인쇄] | 과립 (응집체) 수준의 거동 — 입자 재료 (SE) 자체의 소성과 다른 층 · 실험 비용 = 단계당 스캔 ≈30 분 · 7–9 단계

## m — 받아들일 통찰
- [m] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 무엇을: **영상 · 복셀 기공률에는 '세는 기공의 최소 크기' 를 붙이고, 견주기 전에 기둥 (1 − ε)·H 보존을 본다** — 이 논문에서 2 µm 초과 기공은 30.2 → 12.8 → 6.4 → 2.75 → 0.67 % (7 → 13 → 19 → 27 → 110 MPa · 바인더 없음 R.H. 5) · 41.3 → 1.45 % (처음 → 112 MPa · 바인더 있음 R.H. 90) [판독] 인데 높이는 0.748 · 0.605 배로만 줄고 (1 − ε)·H 는 +4 … +20 % 늘었다 8–12 % 준다 [카드 산술] = 보이던 기공이 문턱 아래로 넘어간 것 · 인쇄된 충전 밀도 34.5 % 를 가정으로 얹으면 112 MPa 에서 전체 기공 ≈43 % 가운데 영상이 보는 것은 1.45 % [카드 산술 · 가정] | 우리 쪽 어디에: 단계 0 ; U6 ; 단계 7 (복셀 pore 지표를 실험 옆에 놓을 때) | 왜: 카드 §3-4 · §3-5 · §7-2 · 논문 p.122 의 *"not detected"* 문장
- [m] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 무엇을: **거시 곡선의 꺾임을 기전의 경계로 쓰지 않는다** — 압밀 곡선의 Py (1.5–5 MPa) 의 1.6–5.3 배 [카드 산술] 인 8 MPa 에서 과립은 막 깨지기 시작하고, 재배치는 Py 뒤 (7–19 MPa) 에도 일어난다 (저자 결론: Py 가 그 미시 과정의 '끝' 이라는 통념과 반대) → Heckel 단계 경계 · '판 응력이 처음 오르는 충전율' 로 기전을 말할 때는 구조 관측량 (접촉 · 형상 · 파쇄 수) 으로 따로 받친다 | 우리 쪽 어디에: 단계 4 ; 후보 M0 | 왜: 카드 §3-3 · §7-3 · 논문 p.117 · p.119 · p.123
- [m] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 무엇을: **불균일 · 결함의 관측량 정의** — 높이 여섯 구간 기공 분율 + 위 − 아래 차 (이 논문 최대 −11.4 %p @ 13 MPa → 27–28 MPa 부터 대체로 1 %p 안 [판독]) · 크기 등급별 기공 수 밀도 (50 µm 초과 · 20–50 µm) · 가장 큰 열 개의 평균 지름 · 함정 = 개수 분포는 이어진 큰 기공 하나를 0 으로 센다 (8 MPa 분포가 좁아 보이는 이유 · 부피 가중을 함께) | 우리 쪽 어디에: 단계 5 (실제 금형 펠릿 ↔ 옆 주기 RVE 를 견줄 때 이 차를 먼저 적는다) ; 후보 A′-0 ; 결과 전 대조 항목 (값이 아니라 정의) | 왜: 카드 §3-4 · §3-8 · §3-9 · 논문 p.119–122 · Fig 10 · 11 · 13 · Table 3
- [m] cottrino2013_insitu_xct_granulated_alumina_die_compaction | 무엇을: **X 선 CT 밀도 지도는 회색값 보정 + 빔 경화 점검 (반지름 방향 회색값 프로파일) 뒤에만 읽는다** — 저자 스스로 시료 · 압력 사이 비교 불가라 적었고, R.H. 90 시료는 가장자리 회색값이 축의 ≈1.25 배 [판독 · Fig 2] 인데 같은 시료의 지도에서 '벽 쪽이 더 치밀' 을 읽는다 (분리 안 됨 [카드 비판]); 높이 방향 기공 분율 (이진화한 기공을 셈) 은 이 인공물을 덜 탄다 [카드 추론] | 우리 쪽 어디에: 흐름 밖: 실험과의 대조 (CT 자료를 받을 때의 점검 항목) ; 단계 0 | 왜: 카드 §3-7 · 논문 p.113 · Fig 2 · 4

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Kong CM, Lannutti JJ. Localized densification during the compaction of alumina granules: the stage I–II transition. J Am Ceram Soc 2000;83(4):685–90. | c · k · 후보 M0 · 단계 4 — Py (단계 I–II 전이) 의 원 정의이자 이 논문이 *"reproduced with a discrete element modelling"* 이라 적은 문헌 ([1] · 0–3 MPa 의 치밀화 전선 · 카드 §4-4 (i) · §12) — 과립 압밀 DEM 의 한계 · 보정이 실제로 적혀 있는지 확인할 원문 | litdb 확인: ls 'kong' · 'lannutti' 없음 · grep 'Lannutti' · '685–90' = 이 카드뿐
- [n] Deis TA, Lannutti JJ. X-ray computed tomography for evaluation of density gradient formation during the compaction of spray-dried granules. J Am Ceram Soc 1998;81(5):1237–47. | m · 후보 A′-0 — 과립 압밀 밀도 구배 CT 의 선례 · 높이/지름 효과 · '균일성 ↔ 과립 강성' 의 근거 ([11] · 카드 §3-7 · §12) | litdb 확인: ls 'deis' = deiseroth2008 뿐 (다른 논문) · grep '1237–47' = 이 카드뿐
- [n] Busignies V, Leclerc B, Porion P, Evesque P, Couarraze G, Tchoreloffa P. Quantitative measurements of localized density variations in cylindrical tablets using X-ray microtomography. Eur J Pharm Biopharm 2006;64(1):38–50. | 단계 0 · m — 회색값을 밀도로 **보정한** 국소 밀도 지도 (40–200 MPa · 벽 · 펀치 근처 치밀 / 가운데 덜 치밀) — 이 논문이 하지 못한 보정의 방법 ([5] · 카드 §3-7 · §12) | litdb 확인: ls 'busignies' 없음 · grep 'Busignies' = 이 카드뿐
- [n] Kadiri MS, Michrafy A, Dodds JA. Pharmaceutical powders compaction: experimental and numerical analysis of the density distribution. Powder Technol 2005;157(1–3):176–82. | 후보 M0 · 후보 A′-0 — 금형 압밀 밀도 분포의 FEM (연속체) + 수은 기공계로 잰 높이별 기공 (이 논문 Fig 10 과 같은 꼴의 선례 · 벽 마찰 입력이 있을 원문) ([4] · 카드 §12) | litdb 확인: ls 'kadiri' 없음 · grep 'Kadiri' = 이 카드뿐
- [n] Buffiere J-Y, Maire E, Adrien J, Masse J-P, Boller E. In situ experiments with X ray tomography: an attractive tool for experimental mechanics. Exp Mech 2010;50:289–305. | j · b — 이 하중 틀 · 촬영기의 상세 (스캔 중 하중 유지 방식 · 응력 이완 = 이 카드의 [미확인] 을 메울 원문) ([13] · 카드 §3-2 · §12) | litdb 확인: ls 'buffiere' 없음 · grep 'Buffiere' = 이 카드뿐
- (참고 · 후보로 세지 않음) [2] Dimilia RA, Reed JS, Am Ceram Soc Bull 1983;62(4):484–8 (바인더 Tg ↔ 압밀 · 셋째 구간) · [12] Cottrino S, Jorand Y, Adrien J, Powder Technol 2013;237(3):586–93 (이 과립의 제조 · 가운데 공동 2 · 3 %) — 둘 다 정본 카드 없음 (카드 §12).

## 카드 문제
- `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` L426 — 서지 (*S. Cottrino, Y. Jorand, E. Maire, J. Adrien, … Mater. Charact. 81 (2013) 111–123*) 는 원문과 일치 · 2 차 인용 값 없음 → 내용 문제 없음.  다만 그 줄의 *"카드 없음"* 은 이 카드가 생겨 낡았다 (그 카드는 고치지 않았고 "🔗 관련 카드" 에 한 줄만 더했다).
- 후보 표 N-62 의 '왜' 칸 *"DEM 과립 압밀 검증 표적 후보"* — 원문에는 힘–변위 · 압밀 곡선 · 보정 밀도 · 마찰 계수 · 탈압이 없어 검증 표적으로는 **일부** 만 채운다 (높이 · 보이는 기공 · 결함 통계 = 전부 그림 판독).  후보 표는 고치지 않았다 (메인 세션 소관).
- 도구 문제 (카드 문제 아님 · 보고용): `tools/litdb/extract_figures.py --audit` 가 지금 정본에서 MemoryError 로 죽는다 — 번호 구멍 검사가 라벨의 숫자를 전부 이어 붙여 range 를 만드는데 `onoda1990_random_loose_packing_uniform_spheres_dilatancy_onset` 의 글 크롭 라벨 `p2728-dry-0p59-expansion-0p550` 이 27,280,590,550 이 된다 (그 밖에 lu2020 · meyer2017 · kollenda2024 도 10⁶ 이상).  이 카드의 라벨은 그림 번호 말고는 숫자를 넣지 않았다.  도구 · 남의 카드는 고치지 않았다.
