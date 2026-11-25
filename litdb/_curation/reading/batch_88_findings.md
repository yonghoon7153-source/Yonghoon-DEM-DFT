# batch 88 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-13)

대상: `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` — J. Hærvig, U. Kleinhans, C. Wieland, H. Spliethoff, A.L. Jensen, K. Sørensen, T.J. Condra, "On the adhesive JKR contact and rolling models for reduced particle stiffness discrete element simulations", *Powder Technology* 319 (2017) 472–482 · DOI 10.1016/j.powtec.2017.07.006 (후보 표 N-48 · 가리킨 카드 = `alizadeh2018_dem_adhesion_calibration_segregation_heap` L265).
접착 DEM 의 강성 연화 규칙 (해석 유도 · 부록 A) + 단일 충돌 수치 (두 입자 정면 · 입자–벽 비스듬 · 외력) + Dahneke PSL–석영 반발 실험 대조 · 침대 · 압밀 · 소성 없음.
쪽 = 학술지 p.472–482 (PDF p.1–11) · 판독 원자료 = `litdb/figures/haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem/digitized.csv` (806 행 · 그림 3 · 4 · 6 · 7 · 8 · 11 · 12 · 13 · 벡터 좌표).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE · 압력 · 기공 0 — 단일 충돌).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압밀 · 탈압 0 — 충돌 되튐 (반발 계수) · 떼는 힘만: 아래 j).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 원문 값 없음 (탄성 접촉 · 항복 0) · 카드 산술만: Thornton–Ning 꼴로 넓히면 항복 속도 V_y ∝ (p_y⁵/E\*⁴)^{1/2} 를 연화 뒤에도 지키려면 p_y ∝ E\*^{4/5} | 카드 §8 후보 C · C′ 행 (V_y 식 = `thorntonning1998_…` 식 10) | [카드 산술 · 이 논문 밖] | 일축 항복 세기와의 환산 없음 · 이 논문의 주장 아님

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (단일 충돌 · 하중 분담 0).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 큰 변형 범위는 말 없음 · 대신 **연화한 점접촉 법칙이 바뀌는 범위**: 국소 부피 분율이 closed-pack 에 가까운 다입자 충돌에서 E_mod/E < 10⁻³ 이면 접착 거동이 *"might be changed slightly"* ([8, 9] 인용 · 수치 없음) · 응집체 충돌은 연화가 일정 이상이면 다르게 거동 ([8, 9]) | 카드 §0 ③ · §4-2 (i) (d)(e) · 논문 p.7 · p.9 | [인쇄] | 근거 = 인용만 · 대안 모델 (MDR · EEPA · Thornton–Ning · 다접촉) 비교 없음 · 맞춘 값 = 검증의 E · γ · e 셋 (Krijt 2013 맞춤)
- [e] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 같은 꼴 안의 함정: 단순 JKR (그리고 SJKR) 은 닿을 때 · 뗄 때 같은 힘 경로라 접착 이력 고리 넓이 0 → 붙음은 감쇠 e 가 정한다 (e → 1 이면 0.05 · 0.5 · 2 m/s 에서 e_eff 0.977 · 0.999 · 1.000 — 늘 되튐) | 카드 §3-7 | [카드 재계산] | 접착 꼴 한정 (JKR 원식의 음의 겹침 끊김과 다른 기전)

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 0).  (수치 쪽 하나만: 붙음 경계 이분법 수렴 \|δ_n/r_p\| = 10⁻⁷ · 시간 간격 지침 Δt_col/δt ≈ 50 (Silbert [30] 인용) — 카드 §3-5 · §3-6 · DEM 단일 충돌의 것.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 진술 없음 — 식은 3D 벡터 꼴 (n · 토크 · 각속도) 이지만 계산은 두 입자 / 입자–벽 단일 충돌 (정면 = 사실상 1D) | 카드 §4-2 (iii) | 표지 없음 (카드 서술) | 침대 차원 증거 아님

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 탈압 · 판 분리 쪽: 에너지 규칙 (식 24) 이면 떼는 힘 ∝ (E_mod/E)^{2/5} — 우리 압축 배수 (÷17.78) 면 0.316 · 믹서 soft SE (E_mod/E ≈ 4.5 × 10⁻⁴) 면 0.046 → '연화 모델의 떼는 힘이 실물보다 작다' 는 한정어 | 카드 §8 단계 6 · §7-3 | [카드 산술] | 단순 JKR · 단일 접촉 — 침대 탈압 자료 아님
- [j] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 압축 DEM (hooke/hysteresis · 선형 스프링) 에는 지수 2/5 가 그대로 옮겨지지 않는다 — 선형 꼴의 불변량을 따로 세워야 함 · 우리 덱의 adhesion 강성을 18 배 연화와 함께 어떻게 정했는지 [미확인] | 카드 §7-4 · [미확인] 목록 | [카드 추론] · [미확인] | 리포 덱을 보지 않은 카드

## k — DEM 의 한계
- [k] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem (Hærvig et al. 2017 · Powder Technol. 319, 472–482) | 연화 DEM 의 한계 문장: *"the mechanistic models in DEM combined with high particle stiffness for most common materials require time step sizes in the order of nanoseconds, which makes DEM simulations impractical for more complex applications"* (초록) · *"care should be taken when introducing reduced particle stiffness to make sure that the critical force FC = 3πRγmod still remains significantly higher than typical external forces trying to separate the particles"* (p.9) · *"for collisions involving many particles with a local volume fraction approaching the closed-pack solution, the adhesive behaviour might be changed slightly if the particle stiffness is reduced too much, Emod/E < 10−3 [8,9]"* (p.9) | 카드 §4-2 (i) · §0 ③ | [인쇄] | 단단한 구 · 점접촉 · 접촉 독립 · 형상 고정의 한계는 말 없음
- [k] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem (Hærvig et al. 2017 · Powder Technol. 319, 472–482) | 연화만 하면 결과가 바뀐다: *"If the surface energy density γ is left unchanged, the result is a more adhesive collision as the kinetic energy lost upon collision is increased significantly"* (p.4) · *"decreasing the particle stiffness does, in most cases, result in a different effective coefficient of restitution"* (p.7 · 그림 7) · γ 그대로 E/10 이면 분리 에너지 × 4.642 (= 10^{2/3}) | 카드 §3-2 · §3-4 | [인쇄] · [카드 산술] | 단순 JKR · 단일 충돌
- [k] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem (Hærvig et al. 2017 · Powder Technol. 319, 472–482) | 보정값 ≠ 물성 쪽 (간접): 연화 모델의 γ_mod 는 고른 E_mod 에 묶인 값 (식 24) · 검증값은 맞춤 — *"the fitted values suggested by Krijt et al. [28] are used when comparing to experiments"* (p.5) · e 0.86 *"fitted to experimental data at high velocities"* (그림 6 캡션) · 연화의 동기 = 계산 시간 — *"A widely used approach to decrease computational costs is to decrease the particle stiffness"* (p.1) | 카드 §0-1 · §3-3 | [인쇄] · [카드 추론] | 원문은 '보정값은 물성이 아니다' 를 직접 쓰지 않는다

## l — 소성변형이 왜 어려운가
- [l] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem (Hærvig et al. 2017 · Powder Technol. 319, 472–482) | **말 없음** — 접촉은 탄성 (Hertz + 단순 JKR) + 점성 감쇠 · 소산은 반발 계수 e 하나 (맞춤값 0.86) · 원문의 'particle deformation' 은 접착에 기여하는 **탄성** 접촉 변형 (Tabor) 의 뜻: *"When the particle diameter is large (typically dp > 10 µm), particle deformation cannot be neglected when describing the adhesive force"* (p.2) · 우회 · 맞춘 값 · 비용 = 해당 없음 (소성 문제를 다루지 않는 단일 충돌 논문) | 카드 §4-2 (ii) · §0-1 l 행 | [인쇄] | 소성 · 형상 · 이력 · 회복 0

## m — 받아들일 통찰
- [m] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 무엇: **강성을 바꿀 때 '지킨 불변량' 칸** — 떼는 힘 (F₀ · Bo) 과 분리 에너지 (응집수 · 붙는 속도) 는 JKR 에서 (E_mod/E)^{2/5} 만큼 갈리고 (우리 믹서 soft SE 배수에서 떼는 힘 기준 22 배) 지수는 접촉 꼴마다 다르다 (단순 JKR 2/5 · SJKR 4/5 [카드 산술] · 선형 [미확인]) · 어디: 후보 D0; 단계 0 (등록 칸); 흐름 밖: 믹서 SE ref ×20 · ×40 덱 · 왜: 식 24 · A.11 (p.4 · p.10) · 카드 §7-3 SJKR 유도 (W_sep = (81/80)π⁵R\*³CED⁵/E\*⁴)
- [m] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 무엇: **U5 단일 충돌 회귀 시험** — 같은 입자쌍을 E 배수 셋 (1 · 0.1 · 0.01) 으로 충돌시켜 v_final 같음 · 시간축 X^{2/5} (PSL–석영 5 m/s 표적: v_final −3.593 · v_max 5.615 m/s · t(v = 0) 0.008855 µs [판독]) — 연화 규칙 · 감쇠 꼴 (식 11 의 √ 누락까지 가려냄) · 접착 구현을 한 번에 · 어디: U5; U0 (γ → 0 이면 e_eff = e) · 왜: 그림 8 · 13 · 카드 재계산 넷째 자리 일치 (§3-3 · §3-6)
- [m] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 무엇: **붙음 경계의 무차원 꼴** — 경계가 λ/Ad^{5/2} (∝ (운동 에너지 ÷ 분리 에너지)^{3/2}) 한 변수로 접힌다 (그림 7 네 곡선 ±0.7 % · 그림 11 기울기 2.5000–2.5003) → 접착 충돌 결과를 KE/W_sep 로 보고하고 다른 Ad 자료를 한 곡선으로 점검 · 어디: 결과 전 대조 항목; 흐름 밖: 믹서 붙는 속도 산술 · 왜: 식 25 · 카드 §3-4 · §3-5
- [m] haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem | 무엇: **함정 — 단순 JKR · SJKR 의 붙음은 감쇠가 정한다** (이력 고리 0 · e → 1 이면 늘 되튐) → SE–SE 붙는 속도 산술 (dev-u 18.7 · 46.6 mm/s — CLAUDE.md) 에 e · 감쇠 꼴을 같이 적는다 · 어디: 후보 D0; 흐름 밖: 믹서 SE–SE 점착 · 왜: 카드 §3-7 재계산

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Y. Gu, A. Ozel, S. Sundaresan, A modified cohesion model for CFD-DEM simulations of fluidization, Powder Technol. 296 (2016) 17–28. http://dx.doi.org/10.1016/j.powtec.2015.09.037 (원문 참고문헌 [8] 그대로) | k · e · m — 식 24 와 같은 기준 (vdW 판) · E_mod/E < 10⁻³ 조밀 충전 경고와 응집체 거동 변화의 근거 (카드 §0 ③ · §4-2 (i) · §12) | litdb 확인: papers/ ls 에 'gu20…' 없음 · DOI grep 0 · 'Ozel' 은 다른 카드의 연구비 문구뿐 → 카드 없음
- [n] T. Kobayashi, T. Tanaka, N. Shimada, T. Kawaguchi, DEM-CFD analysis of fluidization behavior of Geldart Group A particles using a dynamic adhesion force model, Powder Technol. 248 (2013) 143–152. http://dx.doi.org/10.1016/j.powtec.2013.02.028 ([9] 그대로) | k · m — 힘 축척 규칙 F_ad,mod/F_ad = √(k_mod/k) (힘 보존 계열의 다른 판) · 응집체 경고 (카드 §12) | ls 'kobayashi' 없음 · DOI grep 0 → 카드 없음
- [n] S. Krijt, G. Güttler, D. Heißelmann, C. Dominik, A.G.G.M. Tielens, Energy dissipation in head-on collisions of spheres, J. Phys. D Appl. Phys. 46 (2013) 435303. http://dx.doi.org/10.1088/0022-3727/46/43/435303 ([28] 그대로) | k · l — 검증 맞춤값 (E · γ · e) 의 출처 · 맞춤 절차 → '보정값 ≠ 물성' 의 직접 근거 후보 (카드 §3-3 · [미확인] 목록) | ls 'krijt' 없음 · DOI grep 0 → 카드 없음
- [n] K.L. Johnson, J.A. Greenwood, An adhesion map for the contact of elastic spheres, J. Colloid Interface Sci. 192 (1997) 326–333. http://dx.doi.org/10.1006/jcis.1997.4984 ([10] 그대로) | e — JKR · DMT · Maugis 영역 지도 (Tabor λ_T) — 우리 SE–SE 접착이 어느 영역인지 (카드 §3-1 · §12) | DOI grep 0 · 'adhesion map' grep 0 → 카드 없음
- [n] E.J.R. Parteli, J. Schmidt, C. Brümel, K.-E. Wirth, W. Peukert, T. Pöschel, Attractive particle interaction forces and packing density of fine glass powders, Nat. Sci. Rep. 4 (2014) 1–7. http://dx.doi.org/10.1038/srep06227 ([13] 그대로) | e · m — 단순 JKR 의 출처 · 접착이 충전 밀도를 바꾸는 크기 (카드 §3-1 · §12) | ls 'parteli' 없음 · DOI grep 0 · `hare2026_dem_pept_dry_mixing_nmc622_eirich` 이 [80] 으로 인용만 → 카드 없음

## 카드 문제
- 없음 — 가리킨 카드 `alizadeh2018_dem_adhesion_calibration_segregation_heap` 의 2 차 인용 (L49 *"강성 연화 JKR 해석 = Hærvig 2017 (Powder Technol. 319, 472 — ref 2, '같은 함수 꼴')"* · L236 *"JKR 에서 떼는 힘은 E 와 무관하지만 분리 일은 E\*^{−2/3} … (그들 E 1/6.4 연화면 ×0.48)"* · L265 서지) 는 원문 (식 24 · A.11 · p.4 · 첫 쪽) 과 같다 (6.4^{−2/5} = 0.476 [카드 산술]).
- (참고 · 문제 아님) 이 논문 γ 는 면 하나의 표면 에너지 (F_C = 3πRγ ⇒ JKR 접착 일 W = 2γ) — 지수와 무관.  `johnson1971_jkr_surface_energy_contact_elastic_solids` §7-1 ② 의 *"F₀ 보존 규칙 = W 보존"* 의 W 는 접착 일 (표면 성질) — 새 카드의 분리 에너지 W_sep (이 논문 식 23) 와 다른 양이라 두 카드는 어긋나지 않는다.
- (원문 자체의 인쇄 어긋남 — 카드 문제 아님 · 새 카드 §11) 식 11 의 √ 누락 (카드 재계산으로 판별) · (A.10) 둘째 항 2 배 · 그림 4 캡션의 선 모양 열쇠 반대 · Ad 정의 둘 (캡션 ↔ 본문 2/3 배) · 그림 7 ↔ 8 기준 λ 4 배 · F_yield 식의 /R 누락 · §5.2 가 예고한 입자 층 위 증착 없음.
