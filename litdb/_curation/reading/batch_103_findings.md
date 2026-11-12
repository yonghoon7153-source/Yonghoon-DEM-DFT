# batch 103 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `paulick2015_particle_contact_stiffness_two_particle_method` — M. Paulick, M. Morgeneyer, A. Kwade, "A new method for the determination of particle contact stiffness", Granular Matter 17 (2015) 83–93, doi:10.1007/s10035-014-0537-x (본문 11 쪽 · 보충 자료 없음 · 카드 = `litdb/papers/paulick2015_particle_contact_stiffness_two_particle_method.md`).
유리 구슬 (0.8 · 1.5 · 3.0 mm · 최대 80 N) 의 접촉 하나를 재는 실험 논문이다.  층 · 기공 · 계산이 없다 — 아래 '없음' 은 그 때문이다.  값은 유리의 것이라 옮기지 않고 방법만 옮긴다.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (유리 구슬 접촉 실험 · 기공 · 밀도 · 층 압축 없음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] paulick2015_particle_contact_stiffness_two_particle_method | 층이 아니라 **접촉 하나** 의 제하다.  80 N 에 닿자마자 같은 속도 (90 µm/min · 유지 없음) 로 0 N 까지 내리며 힘–변위를 기록.  변위의 63–78 % (한 알 · 두 알 배치) · 69–88 % (입자–입자 = 두 배치의 차) 가 돌아오고, F ≈ 0 잔류 = 한 알 6.9 / 8.7 / 14.4 µm · 입자–입자 5.5 / 2.0 / 6.1 µm (3.0 / 1.5 / 0.8 mm) · 가압 일의 17–35 % 소산 | 카드 §3-5 · §4-4 (iv) · 논문 Fig 6a–c · p.88 · p.90 | 판독 (원문에 인쇄 값 없음) · 일과 비율은 카드 산술 | 유리 + 강철 판 · 잔류가 유리의 것인지 판 압흔인지 가르지 않았다 · 원문은 *"remanent plastic deformation"* 의 정성 서술뿐 · 입자–입자 제하 곡선은 그리지 않았다
- [b] paulick2015_particle_contact_stiffness_two_particle_method | 80 N–0 N–80 N 5 회 (3.0 mm): 한 알은 2 번째부터 가압 곡선이 겹치고, 입자–입자는 4 번째에서 포화.  사이클 원점 (잔류 변위) 이 3.3 → 3.5 → 3.8 µm 로 사이클마다 0.2–0.3 µm 씩 는다 | 카드 §3-8 · 논문 Fig 9 · 10 · p.90–91 | 인쇄 (정성) · 판독 + 카드 산술 (값) | 한 크기 · 시편 하나 · 반복 시편은 10 회 평균과 변위가 15–21 % 다르다

## c — 항복 · 경도 · 크리프 값과 정의
- [c] paulick2015_particle_contact_stiffness_two_particle_method | 접촉 항복압 (*"micro yield pressure"*) σ_Yield ≈ p_max = (3/2)·F_Y/(π R\* δ_Y) (식 9) — 힘 ↔ 변위^1.5 그림에서 Hertz 직선을 떠나는 점으로 읽는다.  인쇄: 6.3 N · 2.52 µm → 796 MPa | 카드 §3-7 · 논문 p.92 · Fig 11a | 인쇄 · 카드 산술 (같은 수를 식 9 에 넣으면 표 2 의 입자–입자 R\* 0.75 × 10⁻³ m 에서 1,592 MPa · 796 은 R\* 1.5 × 10⁻³ m 일 때) | 유리 (또는 유리–강철) 접촉 · 일축 항복 세기가 아니고 일축 환산도 없다 · 인쇄된 항복점이 판독한 입자–입자 곡선 위에 없다 · 경도 · 크리프 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (재료 하나 · 접촉 하나).  가까운 것: 판 (강철 E 200 GPa) 이 탄성이면 Hertz 만으로도 한 알 압축이 입자–입자 접촉보다 1.20 배 더 눌린다 (카드 §3-6 [카드 산술]).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] paulick2015_particle_contact_stiffness_two_particle_method | 큰 변형이 아니라 **아주 작은 겹침에서의 Hertz 이탈** 이다.  원문: 입자–입자는 약 1.5 N · 한 알은 약 5 N 부터 비탄성 (3.0 mm).  판독: 겹침이 지름의 0.05–0.08 % (1.6–2.5 µm) 에서 Hertz 직선과 갈리고, 80 N (지름의 0.68 · 1.11 · 2.45 %) 에서 입자–입자 변위 ÷ Hertz = 1.27 / 0.83 / 0.79 (3.0 / 1.5 / 0.8 mm) | 카드 §3-5 · §3-7 · 논문 p.92 · Fig 11a · Fig 6 | 인쇄 (힘) · 판독 + 카드 산술 (나머지) | 유리 · 물성은 공급사 값 · 크기에 따라 방향이 갈려 원인 (판 · 장치 · 소성 · 물성 · 쌓임) 을 가르지 못한다 · 대안 접촉 법칙 제시 없음 · 맞춘 값 0 개

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (계산 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (3D 실물 실험 · 차원 전이에 대한 말 없음 — 카드 §4-4 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] paulick2015_particle_contact_stiffness_two_particle_method | 원문이 적은 한계: 재료 하나 (*"only one material type was studied"*) · Hertz 곡선은 공급사 물성으로 계산해 *"should … not be taken as a correct but as an appropriate solution"* · 3 mm 한 알 강성의 굴곡은 *"An explanation of this behaviour is not found"* · 2 차 다항식은 0 N 근처에서 *"imprecise"* · 낮은 힘 범위는 향후 과제 | 카드 §0 한정어 · §3-6 · §3-7 · 논문 p.83 · p.89 · p.92 | 인쇄 | 접촉 측정의 한계 진술이고 층 가압 · 탈압 계산에 대한 말은 아니다
- [j] paulick2015_particle_contact_stiffness_two_particle_method | 카드가 적은 한계: 변위 측정 사양 · 장치 컴플라이언스 · 빈 판 시험 없음 · 입자–입자 곡선에 오차 막대 없음 (뺄셈이 산포를 2.8–3.6 배 키움) · 강성을 접선으로 정의하고 할선을 그림 · 원통 안지름 여유 20 · 37.5 % (본문은 7 %) · 잔류 변위가 어느 쪽 소성인지 미구분 | 카드 §11 · §3-3 · §3-4 · §3-9 | 카드 관찰 · 카드 산술 · 미확인 | —

## k — DEM 의 한계
- [k] paulick2015_particle_contact_stiffness_two_particle_method (Paulick · Morgeneyer · Kwade, Granular Matter 17 (2015) 83–93) | 강성 입력값의 지위에 대한 문장 셋.  ① *"In DEM simulation the contact stiffness does not only describe the contact between particles, but it is also a crucial parameter influencing the time step of the simulation. Therefore, the particle contact stiffness is often reduced in order to reduce the simulation time [39]. On the other hand different investigations have shown that a reduced contact stiffness, or reduced Young's modulus, can influence the simulation result in an undesirable manner"* (p.85 · 근거로 든 것 = 유동층 · 전단 · 구속 압축 · 골재 회복 거동의 선행 연구 [40–43]) ② *"The particle contact stiffness is therefore neither a particle property nor corresponds to a bulk property; it is the result of a superposition of surface roughness and particle stiffness."* (p.84) ③ *"However, until now single particle stiffnesses were measured and used as simulation parameters."* (p.86) | 카드 §4-4 (i) · §10 | 인쇄 | 단단한 구 · 점접촉 · 접촉 독립 가정 · 믿을 수 있는 겹침 상한 · 조밀 영역에 대해서는 **말 없음**.  ① 은 계산 속도 때문에 낮추는 관행에 대한 말이라, 층 기공률에 맞춘 연화 (우리 E_eff) 와 목적이 다르다

## l — 소성변형이 왜 어려운가
- [l] paulick2015_particle_contact_stiffness_two_particle_method (Paulick · Morgeneyer · Kwade, Granular Matter 17 (2015) 83–93) | 원문은 입자 계산에 소성을 넣기 어려운 이유를 논하지 않는다 (**말 없음** · 실험 논문).  대신 접촉 수준의 사실을 준다: 저자가 구형이라 Hertz 이론을 적용할 수 있다고 고른 유리 구슬 (p.85) 도 수 N 에서 Hertz 직선을 떠나고 (*"As long as the WPW- and PP-force-displacement curves correspond to the straight line, the particle contact is elastic, otherwise they show non-elastic behaviour [32]."* · p.92), 첫 접촉에서 *"the material started to flow during the first contact and stays remanent plastically deformed during the following contacts"* (p.91) → 첫 가압 ↔ 재가압의 끝 강성이 1.15 배 (한 알) · 1.26 배 (입자–입자) 다르다.  택한 우회 = 접촉 모델을 세우지 않고 힘에 따라 변하는 강성을 직접 잰다 · 맞춘 물리 값 0 개 (기술용 2 차 다항식 계수 3 개 × 곡선) · 비용 = 배치 2 × 크기 3 × 10 회 + 반복 시험 · 가압 한 번 19–39 s | 카드 §4-4 (ii) · §3-8 · 논문 p.91–92 · Fig 9 · 10 · 11 | 인쇄 (문장) · 판독 + 카드 산술 (비 · 시간) | 유리 · 접촉 하나 · 겹침 ≤ 지름의 2.5 % · 이웃 접촉 없음 · 강성은 사이클 원점 기준 할선이라 '경화' 의 상당 부분이 잔류 변위가 원점에서 빠진 것 (카드 관찰)

## m — 받아들일 통찰
- [m] paulick2015_particle_contact_stiffness_two_particle_method | 무엇을: 한 알 · 두 알 짝 검사 — 판이 강체 · 무마찰이면 같은 두 입자를 쌓아 누른 변위는 한 알 변위의 정확히 2 배 (같은 힘 · 첫 가압 · 대칭이라 재료 법칙과 무관) → 해석해가 없는 소성 입자에도 서는 일관성 검사이고 차이가 곧 접촉 처리 · 해상도의 오차 눈금.  어디에: U1 ; U5 ; 단계 2 ; 후보 A′-0 (판 접촉 회귀 시험) | 카드 §4-2 · §8 · §9-1 · 논문 식 (6)–(8) · Fig 3 | 카드 산술 (원문 직렬 스프링 식에 벽 강성 무한대를 넣은 극한 — 원문 문장이 아니다) | 접촉끼리 간섭이 없고 두 입자가 같을 때
- [m] paulick2015_particle_contact_stiffness_two_particle_method | 무엇을: 접촉 강성을 적는 규약 — 접선 dF/dδ 인지 할선 F/δ 인지 (Hertz 에서 1.5 배) · 몇 번째 가압인지 (첫 ↔ 재가압 1.15–1.26 배) · 정규화에 쓴 R\* 와 E\* 의 인수 2 규약.  이 논문은 접선으로 정의하고 실험값은 할선으로 그려, 3.0 mm 입자–입자 강성 ÷ Hertz 가 그림 그대로는 0.53 (3.96 ÷ 7.49) · 같은 정의로는 0.79 (할선) · 0.97 (접선) 이다.  어디에: 결과 전 대조 항목 ; 조건 R5 ; 후보 D0 · 후보 C′ 의 접촉 값을 문헌과 견줄 때 | 카드 §3-4 · §3-6 · 논문 식 (5) · p.92 · Fig 8 · 11b | 인쇄 (정의) · 판독 + 카드 산술 (그림 값의 정체) | 다항식 계수는 그림에서 복원한 것 (±수 %)
- [m] paulick2015_particle_contact_stiffness_two_particle_method | 무엇을: '단일 입자 압축' 문헌 값을 재료 · 접촉 값으로 쓰기 전 점검 셋 — 판 · 장치 몫 (유리에서 한 알 변위가 Hertz 의 1.30–1.49 배 · 초과 8.3–9.5 µm 가 크기와 무관) · 변위 0 점 규약 (접촉 검출 문턱) · 판 재질 (탄성 판이면 Hertz 만으로 1.20 배).  어디에: 단계 4 (SE 재료 값의 외부 근거를 고를 때) ; U1 의 실험 대조 | 카드 §3-5 · §3-6 · §3-9 · §9-3 · 논문 Fig 6 · p.88 | 판독 + 카드 산술 · 카드 추론 (초과분 = 하중 경로 컴플라이언스 후보) | 원문은 장치 컴플라이언스를 주지 않는다
- [m] paulick2015_particle_contact_stiffness_two_particle_method | 무엇을: 접촉 항복압을 실험에서 읽는 절차와 함정 — 힘 ↔ 변위^1.5 에서 Hertz 직선을 떠나는 점 → 식 (9).  함정 = R\* 선택에 2 배 (796 ↔ 1,592 MPa) · 판 접촉이 먼저 항복할 수 있음 (80 N 의 Hertz 최대 접촉압이 유리–강철 2.6–6.4 GPa) · 원점 근처에서는 맞춤 다항식이 이탈점을 만든다 (곡선이 직선을 따르다 벗어나는 것이 아니라 가로지른다).  어디에: 후보 C′ (항복 캡 값의 실험 근거를 읽을 때) | 카드 §3-7 · 논문 p.92 · 식 (9) · Fig 11a | 인쇄 · 판독 + 카드 산술 | 유리 값 · 우리 재료의 항복압은 주지 않는다

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Antonyuk, S., Heinrich, S., Tomas, J., Deen, N.G., Van Buijtenen, M.S., Kuipers, J.A.M.: Energy absorption during compression and impact of dry elastic-plastic spherical granules. Granul. Matter. 12(1), 15–47 (2010). doi:10.1007/s10035-009-0161-3 | b · c · m — 탄소성 과립의 압축 + 충돌에서의 에너지 흡수 (ref 46).  이 논문에 없는 충돌 쪽 (U5) 과 누르고 떼기 (U3) 의 관측량 · 입경 ↔ 강성 관계의 원 논의 (카드 §3-6 · §12) | litdb 확인: ls 'antonyuk' 없음 · DOI 's10035-009-0161-3' · 제목 grep = 이 카드의 참고문헌 줄뿐 · wishlist · 후보 표 0 건
- [n] Russell, A., Müller, P., Tomas, J.: Multiple compression of moist spherical elastic-plastic zeolite 4A granules. Chem. Eng. Technol. 36(7), 1240–1248 (2013). doi:10.1002/ceat.201300109 | b · c · e — 탄소성 입자의 반복 압축 · Hertz 이탈 힘 (ref 38 · 이 논문이 *"below a force of 10 N"* 으로 인용 · 카드 §3-7) | litdb 확인: ls 'russell' 없음 · DOI 'ceat.201300109' · 제목 grep = 이 카드뿐 · wishlist · 후보 표 0 건
- [n] Paul, J., Romeis, S., Tomas, J., Peukert, W.: A review of models for single particle compression and their application to silica microspheres. Adv. Powder Technol. 25(1), 136–153 (2014). doi:10.1016/j.apt.2013.09.009 | c · e · m — 단일 입자 압축을 푸는 모델 리뷰 (µm 실리카 구) — U1 의 해석 대조 식 후보 (ref 37 · 카드 §12) | litdb 확인: ls 'paul2014' 없음 · DOI 'apt.2013.09.009' · 제목 grep = 이 카드뿐 · wishlist · 후보 표 0 건
- [n] Romeis, S., Paul, J., Ziener, M., Peukert, W.: A novel apparatus for in situ compression of submicron structures and particles in a high resolution SEM. Rev. Sci. Instrum. 83(9) (2012). doi:10.1063/1.4749256 | m — 우리 입자 규모 (µm 아래) 의 단일 입자 압축 장치 (ref 36) — 이 논문의 두 배치 뺄셈을 우리 규모로 옮길 때의 장치 쪽 (카드 §8 흐름 밖) | litdb 확인: ls 'romeis' 없음 · DOI '1.4749256' · 제목 grep = 이 카드뿐 · wishlist · 후보 표 0 건
- [n] Samimi, A., Hassanpour, A., Ghadiri, M.: Single and bulk compressions of soft granules: experimental study and DEM evaluation. Chem. Eng. Sci. 60(14), 3993–4004 (2005). doi:10.1016/j.ces.2005.02.036 | d · l · m — 무른 과립의 한 알 압축 ↔ 층 압축 ↔ DEM (ref 34) — 이 논문이 문제 삼은 '한 알 강성을 입력으로 쓰는' 방식의 직접 시험 (카드 §4-4 (i) · §12) | litdb 확인: ls 'samimi' 없음 · DOI 'ces.2005.02.036' · 제목 grep = 이 카드뿐 · wishlist · 후보 표 0 건
- (참고 · 후보로 세지 않음) ref 18 Cole · Peters (2007) Granul. Matter 9(5), 309–321 = 입자 쌍 접촉 실험 (`coetzee2017_dem_calibration_review` L641 이 Cole 외 [216,217] 의 입자 접촉 실측을 옮겨 둠 — 같은 논문인지는 그 카드에 서지가 없어 미확인 · 카드 없음) · ref 40 Moreno-Atanasio 외 (2007) = 후보 표 N-49 에 이미 있음 · ref 28 Thornton · Ning (1998) = 정본 카드 있음.

## 카드 문제
- `coetzee2017_dem_calibration_review` L648 — "시험기·압반의 강성/변형을 배제하고 두 구 사이 접촉강성만 측정하는 방법": 원문 (요약 p.83 · p.86–87) 과 같다 · 숫자 인용 없음 · 문제 없음.  보탤 한정 = 배제는 '같은 힘에서 변위를 뺀다' 는 가정 위의 것이고 원문은 장치 변형량을 따로 재거나 검증하지 않았다 (그 카드는 고치지 않았다).
- `paulick2015_elastic_particle_properties_dem_review` L1072 — "미digest, WISHLIST 후보" 는 이 카드로 해소돼 낡은 표기가 됐다.  그 줄은 고치지 않았고 카드 끝에 '🔗 관련 카드' 한 줄만 더했다.
- 후보 표 N-54 의 '왜' 칸 — 방법 서술은 맞다.  다만 (a) U5 의 '충돌' 은 이 논문에 없다 (준정적 한 쌍) (b) 변위 측정 사양이 없다 (c) 값은 유리라 대조 값이 되지 못한다 (카드 §0-1 · §8).  후보 표는 고치지 않았다 (메인 세션 소관).
- 원문 자체의 어긋남 17 건 (식 8 의 인쇄 꼴 · 강성 정의 · 796 MPa 의 R\* · 단위 · 원통 치수 등) 은 카드 §3-10 에 표로 두었다 — 카드 문제가 아니라 원문 쪽이다.
