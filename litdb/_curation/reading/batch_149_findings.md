# batch 149 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · 후보 표 N-112 첫째 · 새 카드)

대상: `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` — Hongming Li · J. J. McCarthy\*, "Controlling Cohesive Particle Mixing and Segregation", *Phys. Rev. Lett.* 90 (18), 184301 (2003) · DOI 10.1103/PhysRevLett.90.184301.
액체 다리 (물 ≈1 vol%) 로 점착한 이원 유리 · 아크릴 구 (반지름 0.4–1.0 mm) 를 반 채운 준 2D 회전 드럼 (지름 ≈14 cm · 6–9 rpm) 에서 ≈30 바퀴 돌린 점근 상태를 사진으로 보고, 쌍별 입상 Bond 수 (식 1) 의 위계로 M 상 (점착이 분리를 줄임) · E 상 (점착이 분리를 키움) 을 예측한 실험 + 해석 논문 — 압밀 · 고체전해질 · 계산 모델 없음.
쪽 = PDF 쪽 p.1–4 (인쇄 184301-1 … -4) · SI 없음 · 고른 의도 대조 = **일부** (쌍별 Bo · 위계 · 상태도 · 실험 · 드럼 채움 / 'Bo 축' 없음 — 축 = 크기비 · 젖음비 · 밀도비 / 경계식 인쇄 없음 · 카드 유도 / 판정 = 사진 정성 · 카드 §0-1).
인용 서지 (질문 k · l 용): H. Li, J. J. McCarthy, *Phys. Rev. Lett.* 90, 184301 (2003), DOI 10.1103/PhysRevLett.90.184301.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 압밀 · 고체전해질 없음 (중력 아래 회전 드럼 혼합 · 유리 / 아크릴 구 · 카드 §0 · §3-4).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압력 · 탈압 없음 (카드 §4-3 ④).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 물성 값 0 (강체 mm 구 · 식 (1) 에 탄성 · 소성 항 없음 · 카드 §4-2).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 압축 · 하중 몫 없음.  가장 가까운 것은 크기 · 밀도가 다른 두 종의 점착 쌍 위계 (하중 아님): 같은 종 2–2 (큰 입자) 의 Bo 가 다른 쌍보다 크면 E 상 (카드 §3-2).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · 계산 없음.  점착력은 모세관 (액체 다리) 힘 한 값 2πγR_e cos θ (식 1 분자 · 다리 부피 · 간격 · 점성 · 탄성 항 없음 · 카드 §3-1).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 — MPM · 계산 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | **경고 · 증거 없음** — 실험 = *"half-filled, pseudo-two-dimensional tumbler mixers"* (지름 ≈14 cm · 깊이 2 cm) · *"qualitatively similar to an ideal case … an infinitely long chute"* · 이론 = 차원 없는 쌍별 힘 비 · 3D 드럼 · 축 방향 분리 · 2D → 3D 이전에 대한 말 없음 | 카드 §3-5 · §4-3 ③ · p.1 · `txt_p1_asymptotic_state_drum_14cm_half_filled_silane.png` | 인쇄 | 우리 3D DEM 드럼 (반지름 13.14 mm · Fr 0.0827) 과 차원 · 회전 세기 모두 다르다

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — 계산 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 전지 재료 · 압력 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | 원문 스스로 적은 한계 셋 — (i) *"While we cannot decouple diffusive mixing from segregation"* (p.1) (ii) *"our theory is not intended to address the macroscopic pattern of segregation"* — 점착 차이 → 표면 각이 시간에 따라 변해 거시 줄무늬 (그림 3c · [20]) (p.3) (iii) *"we expressly avoid rate-dependent phenomena which are complicated by both the cohesion and the bridging-liquid viscosity [17]"* · 운동학은 *"vital to a full description"* (p.3–4) | 카드 §3-8 · §11 · p.1 · p.3–4 | 인쇄 | 가압 · 탈압과 직접 닿지 않는다 — 압밀 DEM 의 **초기 배치 (혼합 상태)** 를 정하는 단계의 한계 (속도 · 시간 의존을 뺀 점근 이론)

## k — DEM 의 한계
- [k] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy (H. Li · J. J. McCarthy, *Phys. Rev. Lett.* 90, 184301, 2003) | **말 없음** — DEM · simulation 을 쓰지 않는다 (원문 전수).  대신 *"we develop a particle-scale theory of mixing/segregation in cohesive systems"* (p.1) · *"a particle-level model is able to accurately predict previously unreported results on the mixing and segregation of wet granular materials"* (p.4) = 해석적 쌍별 힘 비 (계산 아님) | 카드 §4-3 ① · p.1 · p.4 · `txt_p1_intro_…` · `txt_p3_p4_asymptotic_only_rate_avoided_conclusion.png` | 인쇄 | DEM 한계 근거로 인용하지 않는다

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy (H. Li · J. J. McCarthy, *Phys. Rev. Lett.* 90, 184301, 2003) | **논의 없음** — 강체 mm 유리 · 아크릴 구 · 점착은 모세관 (액체 다리) 힘으로 탄성 · 소성과 무관한 식 (1) · 맞춘 값 0 · 계산 비용 해당 없음 | 카드 §4-3 ② · §3-1 | 인쇄 · 카드 해석 | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | **쌍별 Bo 위계로 혼합 상을 결과 전에 분류하는 규칙** — Bo_12 > {Bo_11, Bo_22} → M (다른 종에 붙음 · 섞임) · 같은 쌍 하나라도 크면 E (같은 종끼리 · 분리) · 크기 인자 R_e = 2R1R2/(R1+R2) (= 2R\*) · 무게 = 두 질량 중 작은 쪽 = 우리 논지 §2-1 쌍 Bond 수와 같은 꼴 → B2-U (Bo_SE–SE 21.2 · γ_AM/γ_SE 0.1 · 기하평균) = E 꼴 (SE–SE 21.2 > SE–AM_P 12.1) · B2-C = M 꼴 (SE–AM_P 38.2 > 21.2) · B1 = 여섯 쌍 모두 Bo < 1 [우리 산술] | 흐름 밖: Ⓒ 믹서 (결과 전 대조 항목 · 후보 D0 의 믹서 판독) — 왜: 판독 전에 상 분류를 적으면 결과가 위계를 따르는지 (교차 확인) · 어긋나는지 (충돌 · 거친 입자 효과 = 정보) 를 가를 수 있다 (카드 §3-2 · §7-3 · §9-1 · p.2)
- [m] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | **판가름 수의 결합 규칙 감도** — 같은 크기 인자 2/(1+r) 에서 혼합쌍 규칙만으로 'SE→AM 이 SE–SE 를 이기는' γ_A/γ_S 문턱 = 산술 r 0.111 · 기하평균 ((1+r)/2)² 0.309 (논지 0.31) · min (이 논문의 '큰 θ') (1+r)/2 0.556 (AM_P · AM_S 0.250 · 0.391 · 0.625) [우리 산술] — 이 논문은 min 을 근거 없이 (*"simply"*) 가정 | 흐름 밖: Ⓒ 믹서 · 논지 §2-8 판가름 측정 (같은 SE 탐침 AFM 으로 W_AS 직접) — 왜: 0.31 하나를 믿고 비코팅 팔을 설계하면 규칙 선택이 5 배 문턱 차로 숨는다 (카드 §7-2 · p.2)
- [m] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | **'점근 상태' 의 정의와 확인** — 처음 완전 분리 → ≈30 바퀴 뒤 *"time invariant and is assumed to represent the asymptotic state"* · 회전 · 점성 의존은 일부러 뺌 — 우리 B 계열 판독은 2 바퀴 | 흐름 밖: Ⓒ 믹서 · 단계 0 의 판정 전 확인 항목 — 왜: 점근 이론 (위계) 과 견주기 전에 Lacey M(t) · 군집 분율 (t) 의 평탄을 보이거나 '과도 상태' 로 적어야 한다 (카드 §3-5 · §9-3 · p.2)
- [m] li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy | **대조 실험의 꼴 = DEM 단위 시험** — 크기 · 밀도 같고 젖음만 다른 쌍 (그림 2c/d · 마름 섞임 → 젖음 분리) · 젖음 같고 크기만 다른 쌍 (그림 2a/b · 마름 크기 분리 → 젖음 섞임) | 흐름 밖: Ⓒ 믹서 DEM (SJKR + 기하평균 쌍 규칙 구현의 방향 시험 · U 목록 밖 제안) — 왜: 결합 규칙 (min · 기하평균 모두) 아래 같은 크기 · 밀도에서 γ 대비는 늘 E 이고 크기 대비 + Bo_12 우세는 M 이라 구현 결함을 정성으로 잡는다 (카드 §8 · §9-4 · p.2–3)

## n — 논문 에이전트 후보
- [n] J. J. McCarthy, D.V. Khakhar, and J. M. Ottino, Powder Technol. 109, 72 (2000). (원문 참고 [18] · 서지 일부만 — 목록에 제목 없음) | g · m — 젖은 입자 드럼 혼합: 이 논문이 *"cohesion plays a minimal role, but may increase mixing rates slightly"* 의 근거로 든 앞선 실험 (표면층 확산 혼합 · 우리 믹서 시간 축) (카드 §3-5 · §12) | litdb 확인: papers/ 617 목록 · '109, 72' · 'Powder Technol. 109' grep 0 · mccarthy* 카드 없음 (nase2001 의 Khakhar = 다른 논문 Gilchrist 1999)
- [n] K. M. Hill, D.V. Khakhar, J. F. Gilchrist, J. J. McCarthy, and J. M. Ottino, Proc. Natl. Acad. Sci. U.S.A. 96, 11701 (1999). (원문 참고 [20] · 서지 일부만) | j · m — 그림 3c 의 거시 분리 줄무늬 (*"previously reported only for more complex container geometries"*) 의 선례 — 우리 Lacey 칸 판독이 줄무늬 · 비반경 무늬에 어떻게 반응하는지 (카드 §3-8 · §12) | litdb 확인: '11701' · 'K.M. Hill' grep 0 (이 카드뿐)
- [n] A. Samadani and A. Kudrolli, Phys. Rev. Lett. 85, 5102 (2000). (원문 참고 [17] · 서지 일부만) | j · m — 젖은 쏟은 더미에서 사이 액체 점성이 표면장력보다 중요할 수 있다는 앞선 결과 (이 논문이 뺀 속도 의존 · G3 rpm 축의 빈칸) (카드 §3-8 · §12) | litdb 확인: 'Samadani' · 'Kudrolli' grep 0 · '5102' = schmitt2026 의 무관한 수
- [n] J. C. Williams, Powder Technol. 15, 245 (1976). (원문 참고 [4] · 서지 일부만) | m — '점착이 분리를 줄인다 · 기원 불명' 이라는 앞선 이해의 출처 (이 논문의 새로움 주장 · G1 판정의 배경) (카드 §12) | litdb 확인: '15, 245' grep 0 · wishlist 의 'Williams' = Williamson 1990 (다른 논문)
- [n] C. Thornton, K. K. Yin, and M. J. Adams, J. Phys. D 29, 424 (1996). (원문 참고 [11] · 서지 일부만 — 제목 · 내용 [미확인]) | m — 서론 [8–15] (사이 액체 점착 연구) 의 하나 · 같은 Thornton 계의 점착 입자 계산 여부 확인용 (카드 §12) | litdb 확인: 'J. Phys. D 29' grep 0 · `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` = 다른 논문 (1991)

## 카드 문제
- `jarray2019_cohesion_driven_mixing_segregation_drum` **L322** (참고문헌 표 ref 14 · 20 의 '왜' 칸) — *"점착 혼합 상태도 (Bo 축)"* : 이 PRL (ref 14) 의 상태도 축은 **R1/R2 × cos θ1/cos θ2 (판 = ρ1/ρ2)** 이고 Bo 는 세 쌍의 **위계 (순서)** 로 상을 정하는 데만 쓰였다 (원문 p.2 *"in the parameter space of size ratio (R1/R2), density ratio (ρ1/ρ2), and wetting angle ratio … differing hierarchies of Bo_g,i-j are observed"* · 그림 1 · 4a) → 'Bo 축' 은 PRL 에 맞지 않는다 (PRE 2005 = ref 20 쪽은 이번에 확인하지 않음 [미확인]).  같은 문구가 후보 표 S8 N-112 '왜' 칸에도 있다 (후보 표 — 카드 아님).  서지 (*"Li, H. & McCarthy, J. Phys. Rev. Lett. 90, 184301 (2003)"*) · *"점착으로 분리 조절"* · *"McCarthy = Nase 2001 의 교신"* 은 원문과 같다 (이니셜 'J.' 는 Jarray 목록 꼴).  고치지 않았다.
- 그 밖: 정본에서 이 논문을 인용한 카드는 jarray2019 하나 (papers/ 617 목록 + '184301' · 'PhysRevLett.90' · 'McCarthy' · 'Hongming' grep).

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **반례** (섞임 ↔ 분리) · **일부** (덮임 ↔ 뭉침) | 근거: 젖음비 cos θ1/cos θ2 (= 점착 대비) 가 상태도 축 (그림 1) · p.2 *"When Bo_g1-2 > {Bo_g1-1, Bo_g2-2}, or the materials are adhesive, we expect that segregation will be limited at equilibrium. However, when either the Bo_g1-1 > Bo_g1-2 or Bo_g2-2 > Bo_g1-2, we expect that cohesion will not mitigate segregation, but instead will lead to more segregation than would be achieved in the dry case."* · p.3 *"our theory predicts that cohesion will lead to a novel mechanism of segregation if the particles differ in wetting characteristics"* · 그림 2–4 시험 (사진 정성) · '덮임 (adhesive) ↔ 뭉침 (cohesive)' 은 p.2 *"which conditions favor adhesive versus cohesive behavior"* 말뿐 · 덮임 관측 없음 | 좁힐 문장: "점착 대비로 섞임 ↔ 분리를 예측 · 시험한 선례 = Li & McCarthy 2003 (액체 다리 · mm 구 · 준 2D 드럼)" 을 먼저 적고, 우리 몫을 **건식 표면 에너지 결합 규칙 · µm 전극 3 상 (크기비 1/9 · 1/4 · 밀도비 0.42) · DEM 의 덮임 관측 (AM–SE 접촉 · SE 군집 · Lacey M)** 으로.
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **반례** (정성 · 접촉각) | 근거: p.3 *"wetting angles of θ ≈ 20° (hydrophilic) and θ ≈ 60° (hydrophobic), as measured by direct inspection of magnified images of roughly microliter sized droplets on actual particle surfaces"* · 예측이 실험을 이끈 순서 p.3 *"Fig. 1 predicts the formation of an E phase (points 2d on Fig. 1). … We therefore take identical, roughened 0.4 mm (radius) particles …"* · 한정: 힘 · 표면 에너지 측정 없음 · γ 값 없음 · 혼합쌍 min 가정 · 상 (M / E) 만 · 사진 판정 · 사전 등록 없음 | 좁힐 문장: "따로 잰 점착 입력 (접촉각) → 혼합 상 예측은 선례가 있다" → 우리 몫 = **같은 SE 탐침 AFM 힘 비 (또는 IGC γ) 로 W_AS 를 결합 규칙 없이 직접 재고 쌍별 Bo 로 DEM 정량 관측을 결과 전에 등록**.
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **없음** | 근거: p.1 *"we restrict our study to rotation rates that are sufficiently small (typically 6–9 rpm) such that the forces of interest include only the cohesive interaction (F_C) and the particle's weight (F_W), i.e., shearing forces are negligible"* · p.3 *"we expressly avoid rate-dependent phenomena"* · 드럼 벽은 *"treated with a hydrophobic silane to reduce adhesion to the surfaces"* (p.1) | 좁힐 필요 없음 (이 논문 기준) · ⚠ 위계 이론 = 느린 회전 극한 (Fr 0.0028–0.0063 [카드 산술] ↔ 우리 0.0827) — 다음 대조 = 같은 그룹 전단 판 (후보 표 N-151 · Li & McCarthy 2006) · Chaudhuri 2006 (N-150).
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **일부** | 근거: 상태도 = 재료 × 재료 (크기비 × 젖음비 · 밀도비 판) 뿐 · 공정 축 (회전 · 충전) 없음 · 같은 틀을 유리–유리 → 아크릴–유리 쌍 (밀도비 0.56 · 그림 4 · p.3) 에 적용 · p.2 *"This tool allows calculation of the scale-independent particle cohesion force in pseudostatic systems."* | 좁힐 문장: "Bo 위계 상태도 (재료 축) 는 선례가 있다" → 우리 몫 = **회전 세기 (Fr · 충돌 수 Co) 를 더한 공정 × 재료 지도 + 건식 µm 3 상으로의 이전**.
