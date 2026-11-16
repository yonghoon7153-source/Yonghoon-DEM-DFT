# batch 113 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-74 · 대피 세션)

대상: `german2014_coordination_number_powder_densification` — R. M. German, "Coordination number changes during powder densification", *Powder Technology* **253** (2014) 368–376 · DOI 10.1016/j.powtec.2013.12.006 (단독 저자 · SI 없음)
문헌 113 쌍 (최소 안정 · 무작위 느슨 / 조밀 충전 · 완전 치밀 · 다이 / 냉간 등압 (CIP) 압분 · 고상 / 액상 소결 · DEM · 모의) 의 **평균 배위수 ↔ 상대밀도 f** 를 모아 N_C = 2 + 11f² (식 9 · 표준오차 1.0) 와 선형 식 (10) 을 맞추고 앞선 식 9 개와 견줬다 (표 6 · 7) — 새 계산 · 실험 · 압력 축 · 부분 배위수 없음.
쪽 = 학술지 쪽 p.368–376 (PDF 쪽 = 학술지 쪽 − 367) · 원자료 = `litdb/figures/german2014_coordination_number_powder_densification/tables_1_5_transcribed.csv` (표 1–5 인쇄 115 행) · `digitized.csv` (52 행 · 그림 3 · 4 · 5 · 6) · 고른 의도 = '단계 5 · 7 — 압밀이 배위수를 바꾸는 크기: nadeem2023 §8-③ 의 근거 · 압축 중 접촉수 변화 해석' → 의도 대조 결과 **일부** (평균 Z 가 밀도로 바뀌는 크기 = 채움 · 부분 Z_ij · 혼합 지표 E_XY · 다분산 · 하중 아래 측정 = 없음).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 황화물 · SE · 압력 축이 없다 (밀도 축만).  랩 표준 (순수 SE 300 MPa 기공 10–13 % · 판정 없음) 을 f 로 옮긴 0.87–0.90 에서 이 논문이 주는 것은 기공이 아니라 그 밀도의 단분산 평균 Z 기대값뿐 (m 둘째 항목).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] german2014_coordination_number_powder_densification | 탈압 · 되돌아옴을 다루지 않는다 · 압분 자료 (청동 다이 [71] · CIP [118] · 소금 [134]) 는 금속조직 단면 · CT 라 **뺀 뒤** Z 뿐 — 회복량 · 누른 채 값 없음 | 카드 §4-3 ④ · §7-1 상태 행 · 표 4 | [카드 해석] | 각 자료의 압력 · 측정 상태 [미확인] (카드 §13 ⑤)

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 한 상의 평균 Z 만 (단단 + 무름 혼합 · 하중 몫 없음).  최소 안정 Z ≈3 은 *"The general sense is 3 to 3.5 contacts are required for gravitational stability"* (p.369) 의 중력 안정 기준이고 하중 몫 · 재밍의 정의가 아니다.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] german2014_coordination_number_powder_densification | 점접촉이 깨지는 쪽의 서술 (접촉 법칙 아님): *"During densification the point contacts between particles become flat-faced bonds with neighboring grains."* · *"The number of faces is the coordination number. As density increases, close neighbors form new contacts to increase coordination number with densification."* (p.368) · Z 가 f 0.9 → 1 에서 급상승 (식 (9) 10.9 → 13.0 · Arzt (11) 10.0 → 13.7) | 카드 §4-3 ① · §8 후보 C · `txt_p1_intro_faces_single_value` | [인쇄 · 카드 산술] | 접촉 법칙 · 범위 문턱 없음 · MDR · EEPA · Thornton–Ning · Storåkers 0 회 (본문 전수 검색)
- [e] german2014_… | '대안' 은 접촉력 법칙이 아니라 Z(f) 식들: 식 (9) 상수 2 개 (2 · 11) 를 113 쌍에 맞춤 (표준오차 1.0) · 식 (10) 2 개 (0.50–0.80 에서만) · 앞선 식 = 선형 (a, b) 4 쌍 · 프랙탈 (8.9f − 1) · RDF 수축 식 (4) + (5) (상수 7.3 · 15.5 + 출발 밀도 f₀) · 1/(1 − f^1/3) (상수 없음) · 14 − 10.4(1 − f)^0.4 · 2 exp 2.4f → 113 쌍 오차 1.0 (식 9) · 1.2 (식 7 · 10) · 2.2 (RDF · f > 0.63) · 17.1 (1/(1 − f^1/3)) · 4.7 (2 exp 2.4f) | 카드 §3-3 · §3-5 · 표 6 · 7 | [인쇄 · 카드 산술 (상수 개수)] | 앞선 식의 상수를 무엇에 맞췄는지는 원문에 없다 · 식 (9) 의 신뢰구간 · 과정별 잔차 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음.  관측량 쪽 근거만:
- [f] german2014_… | [카드 해석] 원문의 Z (닿은 이웃 수 · 완전 치밀 = 결정립 면 수) 는 입자 경계가 있어야 정의된다 → 한 속도장 MPM (후보 A) 에서는 이 관측량이 서지 않고, 입자별 속도장 (A′) · 입자별 FE (B) 에서만 외부 대조선 (±1 띠 · ≈14 상한) 이 된다 | 카드 §7-4 · §8 후보 A · A′ · B | [카드 해석] | 연속체 접촉 판정 (셀 겹침) ↔ '면' 의 대응 [미확인]
- [f] german2014_… | 오차 쪽 근거 = 측정 오차와 맞춤 산포뿐: *"In those reports where measurement error is estimated, typical values are ±0.03 on fractional density and ±1 on coordination number"* (p.372) · 식 (9) 표준오차 1.0 · U6 (조밀 충전 해상도 수렴) 의 관측량 후보 = Z(f) 평균 · 분포 폭 (그림 4: 구리 f 0.69 · 평균 7.0 [인쇄] · 표준편차 ≈1.39 [판독 + 카드 산술]) | 카드 §3-2 · §3-9 · §8 U0–U6 | [인쇄 · 판독 · 카드 산술] | 수치 해상도 규칙 · 수렴 시험 없음

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] german2014_… | 2D 단면 연결수 C_G → 3D 배위수: 식 (2) N_C = C_G / (c sin(ϕ/2)) · **c = 0.75** · ϕ = 이면각 (액상 소결 · [149–151]) — 표 5 (27 행) 가 이 환산 값 | 카드 §3-3 식 (2) · `eq_02_2d_connectivity_to_3d_dihedral` · `txt_p5_eq2_dihedral_c075` | [인쇄] | 이면각 · 미세구조에 걸린 환산 — 일반 분말 · 단면 접촉 계수에 그대로 쓰는 식 아님
- [g] german2014_… | 2D ↔ 3D 값 차: *"In two-dimensional random cross sections Aboav and Langdon [135] measured nearly 58,000 grains in sintered magnesia giving 5.85 sides. This is slightly larger than expected for a 14-sided tetrakaidecahedron"* (p.371) · Gurland *"The measured two-dimensional connectivity corresponds to a three-dimensional coordination of 2 to 3.3"* (p.369) · 그림 2 (2D 설명) 의 완전 치밀 = 육각형 6 이웃 | 카드 §4-3 ③ · §5 | [인쇄] | → 2D 단면 접촉 계수 (kawaguchi2018 카드 3.17 · 1.04 · 0.57) 를 3D Z 로 부르지 않는다 (카드 §7-1 · §9 ⑤)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — 넘김 · 결합 계산이 없다 (문헌 자료 모음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 · 압력 축이 없다 (금속 청동 구 압분 f 0.63–0.97 뿐 · 표 4).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] german2014_… | **하중 아래 측정 · 압력 축 · 탈압 없음** (밀도 축만) · [카드 해석] 원문 압분 Z = 뺀 뒤의 소성 금속 (면 접촉 유지) ↔ 탄성 DEM 은 빼면 접촉을 잃는다 (yano2023 카드: 누른 채 8.94–9.30 → 뺀 뒤 4.16–4.25) → 우리 '누른 채' DEM Z 와 원문 '뺀 뒤' 압분 Z 가 기전상 맞는 짝 · 뺀 뒤 DEM Z 를 원문과 견주면 접촉 유지 기전의 차가 섞인다 | 카드 §11 ⑧ · §7-1 상태 행 · §8 단계 6 | [카드 해석] | 압분 압력 · 측정 상태 [미확인]
- [j] german2014_… | **과정 섞인 평균** — 압분 청동 12 점 (다이 7 + CIP 5 · f 0.63–0.97) 에서 자료 − 식 (9) = 평균 −0.74 · RMS 1.05 · 식 (7) −0.13 · 0.36 · Arzt (11) (11 점) −0.38 · 0.48 → 냉간 압분 구간 (f 0.79–0.96) 에서 식 (9) 가 약 1 높다 | 카드 §3-7 · §11 ⑥ | [카드 산술] | 한 재료 · 한 그룹 · Arzt 는 같은 자료를 보며 만든 모형 (독립 검증 아님)
- [j] german2014_… | **부분 배위수 · 크기비 · 혼합 없음** — 크기 분포는 *"In experiments with mixed lead spheres (2× diameter difference) in different ratios (25 and 50 vol.%), the average coordination ranged from 13.0 to 13.8, indicating size distribution is not a significant factor [62]"* (p.371) 한 줄 (완전 치밀 · 크기비 2) | 카드 §3-8 · §11 ⑦ | [인쇄] | 12 : 4 : 1 · 상별 Z 로 옮기지 않는다
- [j] german2014_… | **등압 ↔ 일축** — 원문은 견주지 않는다 · 표 4 의 같은 청동 다이 [71] ↔ CIP [118] 가 같은 밀도 근처에서 0 … +0.3 차 (측정 오차 ±1 안) | 카드 §3-7 · §0 ⑥ | [인쇄 · 카드 산술] | 일축 ↔ 등압 효과를 이 논문에서 끌어낼 수 없다

## k — DEM 의 한계 (원문 문장 · 인용 서지 = R. M. German 2014, Powder Technology 253, 368–376)
- [k] german2014_coordination_number_powder_densification (R. M. German 2014 · Powder Technol. 253, 368–376) | *"Simulations fail to shed light on the problem, in part since they have uncertain effects such as particle sliding, work hardening, and in sintering grain growth during densification [160]."* (p.373) — 모의 일반 (DEM 이름은 없음) · 근거 [160] = B. Henrich, A. Wonisch, T. Kraft, M. Moseler, H. Riedel, Acta Mater. 55 (2007) 753–762 | 카드 §4-3 ① · `txt_p6_simulations_fail_sliding_hardening` | [인쇄] | 수치 상한 · 밀도 문턱 없음
- [k] german2014_… (German 2014) | *"A computer simulation based on the particle free volume distribution linked coordination number to fractional density, giving of 0.55 with 4.2 contacts (random loose) and 0.63 with 6.0 contacts (random dense) [101]. These density and coordination predictions seem low compared to experiment."* (p.370) — 실험 합의 0.58 / 6.2 · 0.63 / 6.7 대비 · 대상 [101] = C. Song, P. Wang, H.A. Makse, Nature 453 (2008) 629–632 | 카드 §4-3 ① · `txt_p3_free_volume_simulation_low` | [인쇄] | DEM 이 아니라 자유 부피 분포 모의 (원문 표기)
- [k] german2014_… (German 2014) | 점접촉 · 형상 불변 가정의 끝 (DEM 을 겨냥한 문장은 아님): *"During densification the point contacts between particles become flat-faced bonds with neighboring grains."* (p.368) · 완전 치밀 = 다면체 면 13.9 (그림 1 · 표 3) | 카드 §4-3 ① · §0 ⑨ | [인쇄] | —
- [k] german2014_… (German 2014) | 반대 쪽 수치 — 표 1–4 의 DEM 13 행이 식 (9) ±1 안 (평균 +0.05 · RMS 0.46) · 원문은 DEM 값을 실험과 따로 판정하지 않는다 → 평균 Z(f) 는 DEM 이 실험 띠 안에서 내는 관측량 | 카드 §3-2 · §4-3 ① | [카드 산술] | 그 DEM 들의 접촉 법칙 · 판정 · 입자 수 [미확인] (카드 §13 ④)

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = R. M. German 2014, Powder Technology 253, 368–376)
- [l] german2014_… (German 2014) | 이유: 미끄럼 · 가공경화 · (소결) 결정립 성장의 *"uncertain effects"* (p.373 · k 첫 항목) · 결정립 모양 모형의 부족 — *"Unfortunately, in modeling sintering behavior this assumption of 14 sides is extended to fractional densities as low as 0.80. In this density range the measured grain coordination is only 8.0, corresponding to octahedral grain shapes according to recent tomography data [25]. Better grain shape models are needed during densification."* (p.371) | 카드 §4-3 ② · `txt_p4_14_sides_vs_8_at_080` | [인쇄] | 소결 맥락 · 냉간 압분의 입자 소성 계산은 논하지 않는다 · 본문 8.0 ↔ 표 4 의 같은 출처 [25] f 0.80 행 8.5 (카드 §3-10 ⑧)
- [l] german2014_… (German 2014) | 택한 우회 = Z(f) 경험식 하나: *"providing a simple but accurate relation for embedding in powder consolidation calculations"* (초록) · 맞춘 값 2 개 (2 · 11) · 맞춘 대상 = 113 쌍 전부 (실험 + 모의 + 합의값 · 같은 가중 · TableCurve 2D 5.01) · 검증 = 표준오차 1.0 *"which is the about the same as the experimental error"* (p.373 · 인쇄 그대로) 뿐 (독립 · 교차 검증 · 과정별 잔차 없음) · 비용 = 해석식 | 카드 §4-1 · §3-4 · `txt_p6_eq9_113_reports_fit` | [인쇄] | 계수 신뢰구간 [미확인]
- [l] german2014_… (German 2014) | 기하 우회의 값: RDF 수축 모형 (식 4 · 5) = *"(without particle sliding or rearrangement)"* (p.373) · 상수 2 개 (7.3 · 15.5 = Arzt 1982 의 Z₀ · C) + 출발 밀도 f₀ → 113 쌍 오차 2.2 (f > 0.63) ↔ 식 (9) 1.0 | 카드 §3-3 · §3-5 · `txt_p6_rdf_shrinkage_no_rearrangement` | [인쇄 · 카드 산술] | 표 6 의 f 1.00 = 18.4 는 인쇄 식으로 9.5 (원문 안 어긋남 · 카드 §3-10 ①)

## m — 받아들일 통찰
- [m] german2014_… | 무엇을: **배위수를 결과 전 대조 항목으로 쓸 때 함께 등록할 칸 다섯** — 접촉 판정 (겹침 > 0 · 틈 문턱 · 면) · 차원 (3D / 2D 단면 + 환산식) · 상태 (누른 채 / 뺀 뒤) · 평균의 가중 (입자 수 · 상별) · 밀도 규약 (f = 1 − ε_sphere) · 우리 쪽 어디에: 단계 0; 결과 전 대조 항목 · 왜: 원문 자료가 이 칸들을 섞어 (접촉 · *"touching and close neighbors"* [37] · RDF [92] · 면 수 · 식 (2) 환산) 측정 오차 ±1 · 산포 1.0 이 됐다 (p.372 · 카드 §4-2 · §8 단계 0)
- [m] german2014_… | 무엇을: **순수 SE (단분산) DEM 압축 궤적의 평균 Z(f) 를 대조선 셋과 한 그림에** — 식 (9) ± 1.0 · 청동 다이 / CIP (표 4) · Arzt (11) · 랩 표준 f 0.87–0.90 의 기대 Z: 식 (9) 10.3–10.9 · 청동 9.0–9.2 · Arzt (11) 9.6–10.0 [카드 산술] (값 맞춤 금지 · frame[4]) · 우리 쪽 어디에: 단계 4; 후보 D0 (새 런 0 · 기존 압축 궤적) · 왜: σ_y 맞춤과 독립한 관측량 · 표 1–4 의 DEM 13 행이 ±1 안 · cardenasbarrantes2022 카드 (Hertz DEM 의 Z − Z₀ 가 입자 변형 계산과 같은 선) (카드 §8 단계 4 · 후보 D0 · §9 ②)
- [m] german2014_… | 무엇을: **압밀 · 믹싱 팔의 Z 보고에 기공을 공변량으로** — 평균 Z 는 상대밀도 1 %p 당 0.12–0.14 (f 0.55–0.64) · 0.19–0.20 (f 0.84–0.90) 움직인다 [카드 산술] · E_XY = n_XY ÷ n_XY^random (= N_contact f_X f_Y · 다른 종 쌍 × 2) 는 모든 접촉이 같은 배율로 늘면 상쇄되므로 팔 사이 판단 근거는 상별 Z_i 실측 [카드 해석] · 우리 쪽 어디에: 단계 5; 흐름 밖: 믹서 지표 (nadeem2023 §8-③) · 왜: 식 (9) 기울기 22f (카드 §3-6 · §0-1 · §9 ①)
- [m] german2014_… | 무엇을: **함정 둘** — (i) 그림 5 범례 · 표 5 의 'LPS' = liquid phase sintering (황화물 Li₂S–P₂S₅ 아님) (ii) 그림 6 의 '초기 배위수' = 녹체 밀도를 식 (9) 로 바꾼 값 (*"calculated using Eq. (9)"*) → Z 를 따로 잰 검증이 아니다 (순환) · 우리 쪽 어디에: 흐름 밖: 문헌 인용 · 보고 방식 · 왜: 카드 §3-9 · §3-10 ⑦ · §9 ③

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] H.F. Fischmeister, E. Arzt, Densification of powders by particle deformation, Powder Metall. 26 (1983) 82–88. (원문 목록 [118] 그대로) | 표 4 의 청동 CIP Z(f) (f 0.72–0.96 → 7.7–11.0) 의 원전 · arzt1982 카드 L453 의 [8] *"To be published"* (impingement · 가공경화 포함 냉간 압밀 완전 이론) 의 출판판 후보 [미확인] — e · j · 후보 M0 · 단계 4 대조선 (카드 §12 · §0-1 표) | litdb 확인: papers/ 에 fischmeister* 없음 · 제목 · '82–88' grep 0 · 'Fischmeister' grep = arzt1982 ([3] · [8]) · kakar1967 ('Fischmeister 1978' 언급) — 인용만
- [n] H.F. Fischmeister, E. Arzt, L.R. Olsson, Particle deformation and sliding during compaction of spherical powders: a study by quantitative metallography, Powder Metall. 21 (1978) 179–187. (원문 목록 [71] 그대로) | 냉간 다이 압분 청동의 Z(f) (f 0.63–0.97 → 7.3–11.8 · 완전 치밀 13.5) · 미끄럼 정량 (= arzt1982 카드 [3] · 그 카드의 '[8] 의 가장 가까운 대체') — e · j · k · 단계 4 대조선 (카드 §3-7 · §12) | litdb 확인: papers/ 에 fischmeister* 없음 · 제목 · '179–187' grep 0 · 'Fischmeister' grep = arzt1982 · kakar1967 (인용만)
- [n] A. Marmottant, L. Salvo, C.L. Martin, A. Mortensen, Coordination measurements in compacted NaCl irregular powders using X-ray microtomography, J. Eur. Ceram. Soc. 28 (2008) 2441–2449. (원문 목록 [134] 그대로) | 냉간 압분한 비구형 (소금) 분말의 CT 배위수 (표 3 완전 치밀 14.0) + 같은 출처의 DEM 행 (표 4 'Simulated by discrete element analysis [134]' f 0.63 → 6.8 · 0.76 → 9.1 · 0.89 → 10.8) — XCT ↔ DEM Z 대조법 (park2025 대조의 선례) · k · m · 단계 4 · 후보 D0 | litdb 확인: papers/ 에 marmottant* 없음 · 'Marmottant' · 'NaCl irregular' · 제목 grep 0
- [n] D. Bouvard, F.F. Lange, Relation between percolation and particle coordination in binary powder mixtures, Acta Metall. Mater. 39 (1991) 3083–3090. (원문 목록 [93] 그대로) | 이원 혼합의 부분 배위수 · 퍼콜레이션 — 이 논문이 못 주는 Z_ij 칸 (j · m 셋째 · 흐름 밖: 믹서 지표) · 이 논문 표 2 · 3 의 'Computer simulation [93]' 행 (f 0.57 → 6.0 · 1.00 → 15.0) 의 출처 | litdb 확인: papers/ 에 lange* 없음 · bouvard* = bouvard2000 (다른 논문) · 제목 grep 0 · 'Bouvard & Lange' 인용 = bouvard2000 · martinbouvard2003 · jarray2019 ('카드 없음' 으로 표기) — 인용만
- [n] A. Vagnon, J.P. Riviere, J.M. Missiaen, D. Bellet, M. Di Michiel, C. Josserond, D. Bouvard, 3D statistical analysis of a copper powder sintering observed in situ by synchrotron microtomography, Acta Mater. 56 (2008) 1084–1093. (원문 목록 [25] 그대로) | 구리 분말 소결 in situ 싱크로트론 CT 의 Z(f) (표 4 의 7 행 · f 0.72–0.87 → 7.8–8.9) · 본문 'f 0.80 에서 8.0 · 팔면체' (p.371) 의 근거 — l (14 면 가정의 잘못) · 단계 7 (접촉 면적 상한) | litdb 확인: papers/ 에 vagnon* 없음 · 'Vagnon' · '1084–1093' · 제목 grep 0

## 카드 문제
없음 (고칠 것 없음).  확인한 2 차 인용 — 같음 / 기록만:
- `nadeem2023_gnn_mixing_index` L57–60 · L494 — 서지 · 방향 같음 (빈칸 = 머리글자 R. M. · 끝 쪽 376 · DOI).  L250–256 의 *"size ratios"* 계산은 German [40] 몫이 아니지만 그 카드가 크기비를 Pinson [41] 에 두므로 문제 아님.
- 같은 카드 **L538–546 (§8-③)** — 제목 · *"점착 → porosity → Z 변화"* 방향은 원문과 같다 (p.369 · p.374).  그러나 *"Z_ij 가 팔마다 달라진다 ⇒ E_XY 가 움직인다"* 는 그 카드 자신의 추론이고 원문에는 Z_ij · E_XY 가 없다 · [카드 해석] E_XY 는 균일 배율 변화에 상쇄되므로 움직임은 상별 Z 의 비균일 변화에서만 생긴다 — 숫자를 German 에 귀속하지 않았으므로 카드 문제는 아니다 (기록만).
- `arzt1982_particle_coordination_densification_spheres` **L204** (Fig. 4 ● 압분 bronze [3] 판독 *"D ≈ 0.71 의 ≈ 7.8 → D ≈ 0.97 의 ≈ 11.8"*) — German 표 4 의 [71] (= 그 카드 [3]) 인쇄값 0.72 → 7.8 · 0.97 → 11.8 과 맞는다 (판독 확인).  L453 [8] *"To be published"* — German [118] (같은 두 저자 · Powder Metall. 26 (1983) 82–88) 이 후보 · 같은 논문인지 [미확인] (n).
- `martinbouvard2003_dem_composite_cold_compaction` L24 *"eq 18: Z=12D (Helle/Arzt)"* — German 표 6 모델 4 (12f) 와 같은 식 · German 은 출처 묶음 [19–23,118,137,157] 로만 적어 어느 논문 식인지 갈리지 않는다 (문제 아님).
- 후보 표 N-74 서지 *"공저자 미상 · 머리글자 없음"* — 단독 저자 · R. M. · 368–376 · DOI 10.1016/j.powtec.2013.12.006 (다른 점 없음 · 빈칸만 채움).
