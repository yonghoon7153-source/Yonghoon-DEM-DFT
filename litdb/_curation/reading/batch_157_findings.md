# batch 157 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-24 · 후보 표 N-118 · 새 카드)

대상: `khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer` — D. V. Khakhar, J. J. McCarthy, J. F. Gilchrist, J. M. Ottino, "Chaotic mixing of granular materials in two-dimensional tumbling mixers", *Chaos* **9** (1999) 195–205 · DOI 10.1063/1.166390.
비점착 유리구를 반 채운 준 2D 회전 용기에서 '강체 회전 바닥 + 표면 얇은 흐름층 (단순 전단 · 포물선 두께)' 연속체 기구학 모형을 세우고 (반 바퀴에 바닥 전체가 층을 지난다 → 층 중간 유량 Q0 = ωL²/2 · 평균 속도 u = ωL²/(2δ0) · 층 상사 δ0/L = k), 원형 = 정상 흐름 (나쁜 섞임) · 타원 · 정사각 = 반 바퀴 주기의 혼돈 이류임을 보이며, 충돌 확산 (Savage f ≈ 0.025) 을 더한 모형이 정사각 실험 IS 를 맞춤 없이 따라가고, Pe = 20k³(L/d)² 로 크기 키우기를 논한다.
쪽 = 인쇄 p.195–205 (PDF p.2–12 · PDF p.1 = AIP 표지) · 그림 14 (전부 임베디드 래스터) · 표 0 · 번호 식 22 · SI 없음 · 계산 (DEM · FEM · MPM) 없음 · 고른 의도 대조 = **일부** (k = δ0/L 의 정의 · 측정 출처 = 채움 / '0.03' = 원문 인쇄값 아님 — 그림 4 두 직선 기울기 0.0243 · 0.0357 의 평균 / 3D 드럼 진술 없음 → 그대로 쓰지 않는다 / 제1 저자 = Khakhar).
인용 서지 (질문 k · l 용): D. V. Khakhar, J. J. McCarthy, J. F. Gilchrist, J. M. Ottino, *Chaos* **9** (1999) 195–205.
⚠ 글자 층은 그리스 문자 · 기호를 라틴으로 뱉는다 (δ→d · ω→v · '='→'5' · '−'→'2' 등) — 인용문 · 식 · 숫자는 전부 400 dpi 렌더 (크롭 = 번호 식 22 + 문장 안 식 5 + 근거 문단 20) 에서 옮겼다.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질 · 압밀 · 기공 없음 — 비점착 유리구 혼합).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압력 · 탈압 없음).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (기계 물성 0 — 확산 계수의 Savage 앞 인자 f(ν) ≈ 0.025 (ν 0.55 · 반발 계수 ≈ 0.9 · p.200) 는 항복 · 경도가 아니다).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (압축 · 하중 분담 없음 — 같은 유리구 한 종).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (접촉 법칙 없음 — 입자 계산은 회전 원통 계산 [30–32] (p.197) · Savage 의 전단 흐름 입자 동역학 [34] (p.200) 인용뿐).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음 · 연속체 기구학 모형은 운동량 방정식을 풀지 않는다 — *"Prediction of the time-varying flow … would require the (numerical) solution of the mass and momentum balance equations"* p.197 · 카드 §4-1).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] khakhar1999_… | (흐름 밖: 믹서) 3D 회전 원통 (구르기 영역) 의 가로 흐름을 **'축 흐름 없음' 가정으로 2D 정상 흐름** 으로 본다 — *"The flow of similar particles in a rotating cylinder operating in the rolling regime is two dimensional (2D) and steady"* · *"Axial mixing occurs due to diffusion alone, since there is no axial flow"* (p.196) · 앞 · 뒤 판 마찰 · 3D 측정 · 축 확산 크기 없음 · 실험 = 준 2D 6 mm (*"~8 particle diameters"* p.198 · 0.8 mm 면 7.5 · 그림 4 의 2.0 mm 면 3.0 입경 [카드 산술]) → 그림 4 의 흐름층 k (Nase δ/R_t 0.03 의 원 자료) 를 3D 드럼으로 옮기는 근거는 원문에 없다 · 카드 판정 = 그대로 쓰지 않는다 (우리 드럼 Fr 0.0827 = 그림 4 의 133–517 배 · 질량 보존 (식 7) + 중력 미끄럼 상한 ≈0.5 m/s 로 k ≳ 0.1 [카드 추론 · 동적 각 가정]) | 카드 §0-1 · §3-9 · §4-4 (iii) · p.196 · p.198 · 그림 4 | [인쇄] · [카드 산술] · [카드 추론] | 압밀 2D→3D 경고가 아니라 흐름층 기구학의 차원 가정 · 비점착 유리구

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] khakhar1999_… | **가압 · 탈압과 닿는 한계 없음** — 원문이 스스로 미룬 것은 믹서 쪽: 분리 (*"beyond the scope of this paper"* p.200) · 비대칭 용기 (*"would perhaps produce more widespread chaotic advection"* p.204) · 얇은 층 흐름 연구 (*"more studies focusing on the special aspects of granular flows (e.g., flow in thin layers) and their implications for chaotic advection are needed"* p.204) · 운동량 효과 (*"Momentum effects are neglected in the model"* 그림 14 캡션 p.204) | 카드 §3-8 · §4-4 · §11 | [인쇄] | 압밀 계산과 무관 — 믹서 판독에만

## k — DEM 의 한계
- [k] khakhar1999_… (D. V. Khakhar, J. J. McCarthy, J. F. Gilchrist, J. M. Ottino, *Chaos* 9, 195–205, 1999) | **말 없음 (DEM 을 쓰지 않음 · 입자 계산은 인용 [30–32] · [34] 뿐)** — 모형 스스로의 한계 문장만: 준정상 *"If we now assume that the layer geometry changes slowly with time compared to the dynamics of the flow, the flow in the layer is quasisteady and similar to that for a circular mixer with the same layer geometry"* (p.197) · *"for simplicity, we take the diffusivity to be a constant"* (p.200) · *"Momentum effects are neglected in the model"* (그림 14 캡션 · p.204) | 카드 §4-1 · §4-4 (i) | [인쇄] | DEM 한계의 근거로 인용 불가 — 연속체 영 모형의 가정 목록일 뿐

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] khakhar1999_… (같은 서지) | **논의 없음** (단단한 유리구 · 접촉 법칙 · 압축 · 소성 없음 · *"We note that there is no adjustable parameter in the model."* (p.202) 는 혼합 모형 (k 실측 + Savage f) 이야기) | 카드 §4-4 (ii) | — | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] khakhar1999_… | **흐름층 두께 k = δ0/L 를 가정하지 말고 덤프에서 잰다** — 경계 = *"the points at which an abrupt change in the direction of motion occurs"* (p.199) · δ0 = 층 중간 두께 · L = 자유 표면 반 길이 · 검산 = 층 중간 유량 Q0 = ωL²/2 (식 5 · p.197 · 원형이면 어느 채움이든 L = 반 길이로 같은 식 [카드 산술 · 식 2 적분]) · 이유 = Co ∝ k⁴ 라 같은 그림 4 안 값만으로 ×0.43 (0.0243) – ×28 (0.069) · 계산 기본값 0.1 이면 ×123 → 우리 B2-U SE–SE Co·λ² 0.040–11 [우리 산술 · λ² 미정] → Co 는 Nase 식 29 (δ · ⟨u⟩ 직접) 로 낸다 | 흐름 밖: Ⓒ 믹서 판독 (Co · 흐름층 측정 연산자); 결과 전 대조 항목 | 카드 §0-1 · §3-1 · §3-9 · §8 · p.197–199 · 그림 4 | [인쇄] · [판독] · [카드 산술] · [우리 산술] | 원문 k 측정 = Fr 1.6–6.2 × 10⁻⁴ · 반 채움 · 준 2D · 비점착
- [m] khakhar1999_… | **우리 39 각형 드럼은 이 틀에서 '원형' = 혼돈 이류 없음** — 반 길이 변동 1 − cos(π/39) = 0.32 % [카드 산술] · 원 = 유선이 닫힌 정상 흐름 · 둘레 선형 (24 바퀴 ≈ 9 ↔ 정사각 e 배 2.1 바퀴 · 타원 4.4 바퀴 [판독 · 카드 산술 · 그림 9]) · 섞임 = 층 안 충돌 확산 + 30 % 채움의 체류 시간 차 (기하 성분 · p.196 의 반 채움 반대 경우) → M(t) 를 확산형으로 읽는다 · 처음 상태 (층상 ↔ 좌우) 차는 큰 Pe (10⁴) 에서만 컸다 (20 바퀴 IS 원 0.448 ↔ 0.413 · 정사각 0.331 ↔ 0.398) · 작은 Pe (10²) 는 거의 같음 (0.297 ↔ 0.300 · 0.166 ↔ 0.171) [판독 · 그림 13] | 흐름 밖: Ⓒ 믹서 해석; 결과 전 대조 항목 | 카드 §3-5 · §3-7 · §3-9 · §9 항목 3 | [판독] · [카드 산술] · [카드 추론] | 2D 반 채움 계산 · 원문은 다각형 · 3D 를 다루지 않음
- [m] khakhar1999_… | **rpm 효과의 비점착 영 모형 = 회전당 불변** — 무차원 식 (10)–(13) 이 시간을 ω⁻¹ 로 재므로 같은 b̄ · k · D̄ 면 회전당 결과는 ω 와 무관 · ω 는 k(Fr) 와 D̄ = 0.025 d̄²/k² (식 20 · p.200) 를 거쳐서만 들어온다 [카드 산술] → 우리 rpm 팔은 같은 rpm 의 비점착 짝 (N0 꼴) + k 측정을 붙여 '점착 × rpm' 몫만 남긴다 | 흐름 밖: Ⓒ 믹서 rpm 축 (G3) | 카드 §3-2 · §0-2 G3 · §9 항목 4 | [인쇄] · [카드 산술] | 원문 혼합 시험은 rpm 을 바꾸지 않았다 · 실험 rpm [미확인]
- [m] khakhar1999_… | **거친 입자 (parcel) 는 Pe 를 바꾼다** — Pe = 20k³(L/d)² (식 22 · 실험 Pe ≈ 100 · p.202) · 우리 SE L/d 78.8 → k 0.03 · 0.05 · 0.1 에서 Pe 3.3 · 15.5 · 124 · CGF 151.4 는 같은 드럼에서 Pe 를 실제 입경 계의 ≈1/(2.3 × 10⁴) 로 낮춘다 [카드 산술 · 점착 무시] → 회전당 혼합 속도를 실제 입경으로 옮길 때 이 몫을 결과 전에 적는다 (G4 지도에 L/d 또는 Pe 축) | 흐름 밖: Ⓒ 믹서 척도 이전 (G4) | 카드 §3-7 · §3-9 · §9 항목 5 | [인쇄] · [카드 산술] · [우리 산술] | 비점착 · 상수 확산 · 2D 모형

## n — 논문 에이전트 후보
- [n] D. V. Khakhar, J. J. McCarthy, T. Shinbrot, and J. M. Ottino, "Transverse flow and mixing of granular materials in a rotating cylinder," Phys. Fluids 9, 31–43 (1997). (원문 참고 [10]) | ★ g · m — 흐름층 연속체 모형의 원전 (포물선 두께 *"Computations and experimental results indicate that the layer thickness may be approximated as δ = δ0[1 − (x/L)²]"* [10] p.197 · 식 20 확산 검증 [10, 24] p.200) · **원형 원통의 δ0 · 속도 측정** 이 있으면 Nase δ/R_t 0.03 의 다른 출처 후보 (카드 §12 · [미확인]) — 우리 드럼 흐름층 어림 | litdb 확인: papers/ 에 카드 없음 (`ls` · `git grep` 'Khakhar' = chaudhuri2006 · figueroa2009 · li2003 · li2005 · nase2001 인용뿐 · 'Transverse flow' = chaudhuri2006 ref [7]) · wishlist 없음
- [n] H. Henein, J. K. Brimacombe, and A. P. Watkinson, "Experimental study of transverse bed motion in rotary kilns," Metall. Trans. B 14, 191–197 (1983). (원문 참고 [14]) | m — 회전 영역 (무너짐 · 구르기) 구분의 출처 (p.195–196 *"avalanching regime … 14"* · *"rolling regime 14"*) → 우리 드럼 (Fr 0.0827 · 30 % 채움) 이 구르기 영역인지 (흐름층 모형을 쓸 수 있는 전제) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Henein' = ebner2013 의 다른 저자 목록뿐 · 'rotary kiln' 0) · wishlist 없음
- [n] S. B. Savage, Disorder, in Disorder and Granular Media, edited by D. Bideau and A. Hansen (Elsevier Science, Amsterdam, 1993), pp. 255–285. (원문 참고 [34] · 서지 일부만 — 장 제목은 원문 목록에 'Disorder' 만) | m — 충돌 확산 D = f(ν)d²·dv_x/dy · f ≈ 0.025 (ν 0.55 · e ≈ 0.9) 의 출처 (식 19–20 · p.200) → 우리 상별 확산 어림 (AM_P ↔ SE (1.3626/0.1514)² ≈ 81 배 · 카드 §8) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Savage' = walton1993 의 다른 Savage 인용뿐 · 'Disorder and Granular' 0) · wishlist 없음
- [n] P. V. Danckwerts, "The definition and measurement of some characteristics of mixtures," Appl. Sci. Res., Sect. A 3, 279–296 (1952). (원문 참고 [35]) | m — IS (intensity of segregation) 정의의 원전 (p.200 · [35] · [36]) — 이 논문 IS 는 정규화 안 한 σ 인데 *"normalized standard deviation"* 이라 부름 (카드 §3-10 ⑥) → IS ↔ Lacey M 환산 규칙을 원 정의로 닫기 | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Danckwerts' = chandratilleke2012 · chaudhuri2006 · lacey1954 인용뿐) · wishlist 없음
- [n] G. Metcalfe, T. Shinbrot, J. J. McCarthy, and J. M. Ottino, "Avalanche mixing of granular materials," Nature (London) 374, 39–41 (1995). (원문 참고 [8]) | m — 제목대로 무너짐 (avalanche) 영역의 혼합 = 낮은 rpm 쪽 영 모형 후보 (원문은 [8–13] 묶음으로만 인용 · p.195 · 쐐기 · '반 채움이면 느림' 문장은 원문이 [7] 로 인용 · p.196) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Metcalfe' = nase2001 · stewart2001 인용뿐 · 'Avalanche mixing' 0) · wishlist 없음
- (후보 수 밖 메모) 참고 [24] Khakhar · McCarthy · Ottino, Phys. Fluids 9, 3600–3614 (1997) = wishlist batch_151 (figueroa2009 의 n) 에 이미 있음 · 참고 [33] Elperin · Vikhansky, Europhys. Lett. 43, 17–22 (1998) = *"a slightly more detailed model"* (u 의 x 의존 · p.197) — 다섯 밖.

## 카드 문제
- `nase2001_granular_bond_collision_number_wet_cohesion` (가리킨 카드 · 2 차 인용 대조 — 고치지 않음 · 🔗 관련 카드 한 줄만 더함):
  - **L205** (참고 42 서지) — 제목 · 학술지 · 권 · 쪽 · 연도 = 같음 · **저자 순서 다름** (카드 = *"J.F. Gilchrist, D.V. Khakhar, J.J. McCarthy, J.M. Ottino"* ↔ 원문 첫 쪽 · AIP 표지 · 머리글 = Khakhar · McCarthy · Gilchrist · Ottino) — Nase 원문 목록 자체가 그 순서인지는 [미확인] (Nase PDF 미열람) · *"δ/R_t ≈ 0.03 의 출처 — 카드 없음"* 은 이 카드로 낡음 · **'0.03' 은 원문 11 쪽 어디에도 인쇄 없음** (그림 4 두 직선 기울기 0.0243 · 0.0357 의 평균 0.0300 [판독]).
  - **L31** (표 ④ *"δ/R_t ≈ 0.03, Gilchrist 2D"*) — 수는 그림 4 기울기 평균과 맞지만 원문 인쇄값이 아님 · 'Gilchrist' 귀속 틀림 (제1 저자 Khakhar) · 조건 (Fr 1.6–6.2 × 10⁻⁴ · 반 채움 · 준 2D 6 mm · 유리구 0.8 · 2.0 mm · 비점착) 누락 (경미).
  - **L36** (한정어 ④ *"2D 드럼 실험값 차용"*) — '2D · 실험값' 맞음 · **'드럼' (원형) 인지 원문으로 확인 안 됨** (그림 4 = *"different mixers"* · 모양 · 크기 미기재 p.199) · 0.03 = 기울기 (절편 1.1–1.9 d 무시 → 점별 δ0/L 0.030–0.069).
  - **L99** (§3-6 우리 Co·λ² 산술 · δ/R_t = 0.03) — 같은 식이 k 에 따라 ×0.43 – ×123 (이 카드 §3-9) · 우리 드럼 Fr 0.083 은 측정 범위 밖 · 질량 보존상 k ≳ 0.1 [카드 추론] → 그 산술의 한정어 보강 필요 (값 자체는 그 카드 덱 (75.04 rpm) 기준으로 맞음 · B 덱 (76.68 rpm) 이면 ×0.958).
  - **L190** (§10 항목 7 *"Gilchrist 2D 드럼의 기하 상사 값 — 3D · 배플 · 다른 채움에서는 다를 수 있다"*) — 'geometrical similarity' = 원문 말 (p.198) ✓ · 경고 방향 ✓ · 범위 보탬: 같은 2D · 같은 반 채움 안에서도 δ0/L 이 L/d 에 따라 0.030–0.069 (절편) · 저자 귀속만 다름.
- `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` **L344** (경미 · 지시 목록 밖) — 같은 δ/R_t = 0.03 을 그들 드럼 (지름 9 cm · 50 % · Fr 0.008–0.09) 과 우리 드럼 (Fr 0.083 · 30 %) 에 함께 써서 '우리 B2 는 그들 K 120 보다 충돌 쪽' 이라는 상대 서열을 냈다 — 두 드럼의 k 가 같다는 가정에 기댄다 (그 카드는 이미 *"가정 많음 · 자릿수만"* 표지) · k⁴ 라 두 드럼의 k 비가 1.5 배만 달라도 서열 판단이 5 배 흔들린다 [카드 산술].
- 정본 밖 참고: 후보 표 N-118 서지 = 저자 순서만 원문과 다름 (Gilchrist 먼저 ↔ Khakhar 먼저) · 나머지 (Chaos 9 (1999) 195–205 · DOI 10.1063/1.166390 · 12 쪽) 같음.

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **없음** | 근거: *"We consider the mixing of similar, cohesionless granular materials"* (p.195) · *"we thus focus on mixtures of similar particles so that segregation does not occur"* (p.196) · 분리는 *"beyond the scope of this paper"* (p.200) · 끝 문단은 분리와 혼돈 이류의 동적 균형을 *"a wealth of unexplored possibilities"* 로 남김 (p.204) | 좁힐 필요 없음 · 가져올 것 = 비점착 같은 입자의 혼합 영 모형 (점착 팔을 이 기준선 위에서 읽는다)
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **없음** (점착 입력 0) | 근거: 다만 **비점착 혼합을 맞춤 값 없이 미리 낸 선례** — k (그림 4 실측) + Savage f(ν) ≈ 0.025 (문헌 [34]) → IS(t) 가 실험과 맞음 · *"We note that there is no adjustable parameter in the model."* (p.202) · 예측 등록 표지는 없다 | 좁힐 필요 없음 · 우리 G2 의 '입력을 따로 재고 맞춤 없이 미리 예측' 형식의 비점착판 원형으로 인용 가능
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **없음** | 근거: 혼합 시험에서 rpm 을 바꾸지 않음 · Fr 은 그림 4 (층 두께) 의 두 값뿐 · 무차원 식 (10)–(13) 이 시간을 ω⁻¹ 로 잼 · 최적 · 맞교환 · 벽 부착 말 없음 · *"In solids, more 'agitation'—tumbling in our case—does not imply better mixing"* (p.204 · 분리 맥락) | 좁힐 필요 없음 · 가져올 것 = 비점착 영 모형 '회전당 혼합은 rpm 과 무관 · rpm 은 k(Fr) · D̄ 를 거쳐서만' [카드 산술] → 우리 rpm 팔의 회전당 M 차이에서 k(Fr) 몫 (덤프로 잰) 을 빼고 남는 것만 점착 효과로 읽는다
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **없음** | 근거: 상태도 · 점착 축 0 · 옮겨 가는 규칙은 크기 (scale-up) 뿐 — *"the Péclet number increases, and therefore the effectiveness of the diffusion decreases with increasing system size"* (p.202) · *"in addition to the Péclet number, mixer shape significantly affects the rate of mixing"* (p.203) | 좁힐 필요 없음 · 가져올 것 = Pe = 20k³(L/d)² 로 크기 · 입경을 옮기는 틀 → 우리 G4 지도에 Pe (또는 L/d) 축을 같이 두어야 CGF parcel 결과를 실제 입경으로 옮길 수 있다 [카드 추론]
