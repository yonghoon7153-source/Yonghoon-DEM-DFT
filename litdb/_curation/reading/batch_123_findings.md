# batch 123 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 기존 카드 보강 · 68-1 번 파일)

대상: `zhang2026_xct_dem_cathode_calendering_peel_calibration` — Xiao Zhang · Tengteng Gao · Zhiqiang Xiao · Yanhuai Ding, "Investigation into Microstructural and Mechanical Evolution During Lithium-Ion Battery Cathode Calendering via X-ray Tomography-Based Discrete Element Method", *JOM* (2026) · DOI 10.1007/s11837-026-08748-x · 권 · 쪽 미인쇄 · 16 쪽 · SI 없음 (보강 전 카드 604 줄 · 2026-09-26 digest → 보강 뒤 764 줄).
Ebner 2013 싱크로트론 CT 의 미압연 NMC 양극에서 100 × 100 × 75 µm³ 를 잘라 입자를 등가 구로 바꾸고 (실측 PSD), NMC–NMC = 탄성 Hertz–Mindlin · CBD (2.2 µm 구) · 입자–Al = linear parallel bond 로 두고, 입자–Al bond 강도를 박리 피크 (0.0347 MPa) 에 맞춘 뒤 30 · 60 · 200 MPa 를 판으로 눌렀다 같은 속도로 빼는 DEM — 공극 · FSA · 배위수 · 집전체 매립 · 힘 사슬 · 응력 텐서 · 체적 에너지 밀도.  액체 LIB · SE 없음 · 소성 · 파괴 모델 없음.
쪽 = PDF 쪽 p.1–16 · 판독 원자료 = `litdb/figures/zhang2026_xct_dem_cathode_calendering_peel_calibration/digitized.csv` (55 행 · Fig 2d · 4b · 4c · 7 · 10 · 12 — 2026-11-16 재판독) · 보강 의도 = '이 논문의 참고문헌이 후보 표 (N-55 · N-66 · N-67 · N-68 · N-69) · wishlist 의 원 인용처 → 참고문헌 목록 원문 + 카드 2 차 서술 대조' → **일부 다름** (카드 §14: 2 차 서술 18 행 중 17 행 같음 · [30] (L222) 귀속 범위가 넓다 → 정정 표지).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 없음 (액체 LIB NMC111 + CBD 양극).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] zhang2026_xct_dem_cathode_calendering_peel_calibration (Zhang · Gao · Xiao · Ding, JOM 2026) | 같은 DEM 안 가압 → 제하: 30 MPa 하중 중 0.333 → 제하 뒤 0.411 (실험 0.412) · 60 MPa ≈0.280 → ≈0.370 · 200 MPa ≈0.152 → ≈0.319 · 200 MPa 런은 5 MPa 에서 아직 ≈0.236 (회복의 ≈절반이 5 MPa 아래) · 두께 회복 ER 11.3 · ≈11.3 · ≈16.4 % | p.7–8 · Fig 4b · 4c · 카드 §3.5 · §12 D2 · digitized.csv | [인쇄] 0.333 · 0.411 · 0.412 · [판독] 나머지 (2026-11-16 재판독 ±0.002) · [카드 산술] ER | 잰 방법 = 판을 같은 속도 (0.01 m s⁻¹) 로 올린 뒤 끝 공극 (*"moved upward in the opposite direction at the same velocity to simulate elastic recovery"* p.5 · 공극 정의식 · 겹침 관례 미기재) · 실험 쪽 되돌아옴 측정 없음 · 기전 = 탄성 Hertz + 취성 bond (소성 없음) · 액체 LIB

## c — 항복 · 경도 · 크리프 값과 정의
- [c] zhang2026_xct_… | 원문에 항복 · 경도 · 크리프 값 없음 (Hertz 탄성 · 항복 캡 없음) · 카드가 다른 카드 (xu2017 NMC532 경도 8.6 GPa) 로 견준 Hertz 평균 면압 ≈0.75 H (평균 접촉 7.3 mN) · 최대 ≈1.1–2.4 H | 카드 §12 D7 | [카드 산술] | 다른 재료 (NMC532) 값 · 일축 항복 환산 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] zhang2026_xct_… | 하중 경로 = 초기 bond 망 지배 → 압력 ↑ NMC–NMC Hertz 접촉 수 ↑ · *"These force chains are primarily carried by NMC particles, and the contact forces between NMC particles are significantly greater than those transmitted through cohesive bonds."* (p.11) · 몫 숫자 없음 · RVE σ_zz ÷ 판 응력 1.013 · ≈1.11 · 0.993 · K 0.40 → 0.68 · Z (= 2·CN) 1.81 · 2.58 · 4.10 (30 · 60 MPa 에서 Z < 3) | p.11 · Fig 8 · 10 · 카드 §3.8 · §3.9 · §12 D3 · D4 | [인쇄] 문장 · σ · CN · [카드 산술] 비 · Z | 무른 상 = SE 가 아니라 bond 로 묶인 CBD · 상별 하중 몫 미보고

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] zhang2026_xct_… | 대안 없음 — NMC–NMC 탄성 Hertz–Mindlin (식 1–6) + linear parallel bond (식 7–21 · Potyondy–Cundall [26]) · 맞춘 값 4 (Ē* 0.3 GPa · σ̄ 3.6 × 10⁷ Pa · λ̄ 2 → '거시 기계 응답' (표적 미기재) · σ̄_Particle-Al 7.2 × 10⁴ Pa → 박리 피크) · 항복 캡이 없어 200 MPa 에서 면압이 NMC 경도를 넘는 접촉 (카드 D7) = 큰 변형 범위의 경고 수치 · 앞선 대안의 서술: Sonzogni [21] *"a novel contact law incorporating cohesive-plastic behavior of binder layers"* (p.2) | p.2 · p.3–4 · p.6–7 · 카드 §4.2–4.3 · §12 D7 | [인쇄] 식 · 값 · [카드 산술] 면압 | 파단 판정 문장 원문에 없음 (PFC 관례로 읽음 [추정]) · c̄ · κ̄* 미기재

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 3D 만 (Fig 2a · 2b 의 2D 단면은 설명용) · 2D → 3D 에 대한 말 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — 이 논문은 넘기지 않는다 (반대 방향: 실측 CT 입자 → DEM 출발 상태).  선행 서술 하나: Ngandjong [17] = *"…coupled it with coarse-grained molecular dynamics simulations of slurry drying and electrochemical finite-element models…"* (p.2) → 정본 `ngandjong2021_dem_calendering_digital_twin`.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — SE 없음.  (참고 · 다른 양: 액체 LIB NMC111 + CBD 전극의 DEM 제하 뒤 공극 0.432 · 0.411 · ≈0.371 · ≈0.319 @ 0 · 30 · 60 · 200 MPa · 실험 0.424 · 0.412 · 0.359 · 0.310 [판독 Fig 4c · 30 MPa 는 인쇄] — 랩 표준과 다른 문헌 값)

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] zhang2026_xct_… | 원문의 한계 문장: 구 근사 → 부피 손실 오차 (p.8) · 파괴 판정은 다음 연구 (p.13) · 200 MPa 는 손상을 보이려는 조건이지 권장 공정이 아님 (p.14) · 카드의 한계: 헤드라인 W_V 2002 Wh L⁻¹ 은 하중 중 값 (제하 뒤 구조면 ≈1,680 · −18 % · D1) · '매립 깊이' 0.937 µm 는 벽 겹침 (L7) · 보정 · 검증 미분리 (L4) · 단일 RVE · 시드 · 수렴 없음 (L10) · 박리 시편이 압연 전극인지 원문끼리 어긋남 (L164 · 2026-11-16) | p.8 · p.13 · p.14 · 카드 §10 · §12 D1 | [인쇄] 문장 · [카드 산술] D1 | 액체 LIB · 탄성 bond 계

## k — DEM 의 한계 (원문 문장 · 인용 서지 = X. Zhang, T. Gao, Z. Xiao, Y. Ding, JOM (2026), DOI 10.1007/s11837-026-08748-x)
- [k] zhang2026_xct_… (Zhang et al., JOM 2026) | *"Slight discrepancies were observed during the later stages of calendering, which can be mainly attributed to the spherical particle approximation adopted in the DEM framework, introducing a certain degree of volumetric loss error."* — 자기 모델에 대해 적은 유일한 한계 문장 (크기 · 정의 없음 · 60 · 200 MPa 에서 DEM 이 +0.009–0.011 성기다 [판독]) | p.8 · 카드 §15 (i) | [인쇄] | 구 근사의 오차 크기를 재지 않았다
- [k] zhang2026_xct_… | *"Given the highly spherical morphology of the NMC particles, they were represented as equivalent spheres in the numerical modeling."* · CBD: *"If the real morphology was directly used in the DEM simulation, the computational cost would increase substantially."* | p.4 · 카드 §4.4 · §15 (i) | [인쇄] | 같은 논문 SEM (Fig 11c) 은 1 차 결정립이 뭉친 이차입자 · 비용 숫자 없음
- [k] zhang2026_xct_… | *"Since calendering is essentially a particle rearrangement process, particle-scale simulations are capable of revealing the underlying mechanisms of structural evolution and mechanical response…¹⁷"* — 형상 변화 · 소성을 계산 밖에 두는 전제 [카드 해석] | p.8 · 카드 §15 (i) | [인쇄] 문장 · [카드 해석] | ref 17 (Ngandjong) 에 기댄 전제
- [k] zhang2026_xct_… | 남의 DEM: *"most DEM studies still rely on virtual particle packing and lack validation based on realistic microstructural data, leading to uncertainties in parameter calibration and model reliability."* · 파괴는 모델 밖: *"subsequent studies can utilize the extracted stress information to evaluate the critical stress conditions for particle fracture…"* | p.2 · p.13 | [인쇄] | 말 없음: 믿을 수 있는 겹침 · 상대밀도 · 변형률 상한 · 접촉 독립 가정이 깨지는 밀도 · 보정값이 물성이 아니라는 고백

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = X. Zhang, T. Gao, Z. Xiao, Y. Ding, JOM (2026), DOI 10.1007/s11837-026-08748-x)
- [l] zhang2026_xct_… (Zhang et al., JOM 2026) | 소성 없음 — NMC–NMC 탄성 Hertz–Mindlin (항복 캡 없음) · CBD 선형 탄성 bond · 형상 고정 · 집전체 = 변형 안 하는 벽 · 그래도 본문은 '변형' 이라 쓴다: *"particles experience more extensive contact, deformation, and local rearrangement"* (p.10) · *"low deformation resistance of CBD"* (p.11) · *"more severe deformation of the current collector"* (p.10) — 모델의 변형 = 겹침 δ [카드 관찰] | p.10–11 · 식 1–21 · 카드 §4.4 · §15 (ii) | [인쇄] 문장 · [카드 관찰] | 소성을 넣기 어려운 이유의 설명 = 원문에 없음
- [l] zhang2026_xct_… | 우회 = 없음 · 대신 bond 세 값 (Ē* 0.3 GPa · σ̄ 3.6 × 10⁷ Pa · λ̄ 2) 을 *"the macroscopic mechanical responses predicted by the numerical model are in good agreement with experimental measurements"* 가 되게 맞추고 (표적 미기재) 입자–Al bond 1 값 (7.2 × 10⁴ Pa) 을 박리 피크에 맞춤 = 맞춘 값 4 · 검증 = 제하 뒤 공극 4 점 (Fig 4c · 30 MPa 0.411 ↔ 0.412) · 계산 비용 · 입자 수 · 시간 간격 = 원문에 없음 | p.6–8 · 카드 §4.6 · §10 L4 | [인쇄] | 보정 · 검증 미분리 · λ̄ 와 σ̄ 는 인장 항에서 서로 바뀐다 (식별성)

## m — 받아들일 통찰
- [m] zhang2026_xct_… | 무엇을: 공극 연산자 · 보고에 **'하중 중 / 제하 뒤' 상태 칸**을 결과 전에 둔다 — 같은 DEM 안에서 200 MPa 0.152 ↔ 0.319 · 헤드라인 W_V 2002 Wh L⁻¹ 은 하중 중 값 (제하 뒤 ≈1,680) | 단계 0; 단계 6; 결과 전 대조 항목 | 근거 p.7–8 · Fig 4b · 4c · 12 · 카드 §12 D1
- [m] zhang2026_xct_… | 무엇을: **RVE 응력 (식 24 · Christoffersen [39]) 의 σ_zz ÷ 판 응력**을 침대마다 상주 점검으로 (그들 1.013 · ≈1.11 · 0.993) + 측압계수 K (0.40 → 0.68) 를 기술자로 | 단계 5; 후보 D0 | 근거 p.12–13 · Fig 10 · 카드 §12 D3 (같은 꼴로 실패한 예 = du2025 0.095 · 다른 카드)
- [m] zhang2026_xct_… | 무엇을: **문헌 귀속은 위첨자 위치로 읽는다** — '큰 입자 = 접촉 · 힘 많음 → 파쇄 취약' 은 이 논문 자신의 DEM 서술이고 ref 30 은 'X-CT 에서 보였다' 문장 끝에만 붙는다 → R7 근거로는 크기 정규화 실측 (wheatcroft2023 · 카드 D7b) 을 쓴다 | 조건 R7; 흐름 밖: 문헌 인용 검증 | 근거 p.12 · 카드 §14 · L222 정정
- [m] zhang2026_xct_… | 무엇을: 판 · 벽 분리를 계산할 때 **입자–벽 점착**을 둔다 — 없으면 제하 때 코팅이 들뜬다 (Giménez [19] 비판 · p.6) · 점착 강도 1 값을 박리 피크에 맞춘 절차 (0.0349 ↔ 0.0347 MPa) — 단 피크 ≠ 에너지 (시간축 무차원) | 후보 A′-0; U4; 단계 6 | 근거 p.6 · Fig 3b · 카드 §8 ③

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] M. Lippke, T. Ohnimus, F. Frankenberg, C. Schilde, and A. Kwade, Powder Technol. 444, 119984 (2024). (원문 참고 [32] · 인쇄 그대로) | b · j · 후보 A′-0 · 단계 6 — 입자–집전체 응집을 넣어 캘린더링 DEM 의 코팅 들뜸을 막은 선례 (Zhang p.6: *"not quantitatively calibrated"*) · 탈압 때 벽 점착 모델의 원전 · 카드 L105 · §14 | papers/ ls lippke* = `lippke2023_dem_drying_structure_formation_lib` (Energy Technol. 2023 · 다른 논문) 뿐 · '119984' grep 0 건 · wishlist · 후보 표 없음 → 카드 없음
- [n] D.O. Potyondy and P.A. Cundall, Int. J. Rock Mech. Min. Sci. 41, 1329 (2004). (원문 참고 [26] · 인쇄 그대로) | e · l · 후보 C′ — linear parallel bond (식 7–21) 의 원전 · 이 논문 · ge2022 · lyu2025 · xu2023 의 결합 모델 · 파단 판정 · λ̄ 의 원 정의 (카드 L294 '[추정]' 을 닫을 자료) | papers/ ls potyondy* 없음 · 'Potyondy' grep = 인용만 (ge2022 · he2026 · lyu2025 · lyu2026 · morrissey2013 등) · wishlist 없음 → 카드 없음
- [n] J. Christoffersen, M.M. Mehrabadi, and S. Nemat-Nasser, J. Appl. Mech. 48, 339 (1981). (원문 참고 [39] · 인쇄 그대로) | d · m · 단계 5 — RVE 평균 응력 σ = (1/V) Σ F ⊗ L (식 24) 의 원전 · 우리 DEM Love–Weber 응력 · 상별 virial 하중 몫의 정의 근거 | papers/ ls christoffersen* 없음 · 'Christoffersen' grep = du2025 · ge2022 · zhang2026_xct · zunker2024r · zunker2025 (인용만) · wishlist 없음 → 카드 없음
- [n] I. Srivastava, D.S. Bolintineanu, J.B. Lechman, and S.A. Roberts, ACS Appl. Mater. Interfaces 12, 34919 (2020). (원문 참고 [28] · 인쇄 그대로) | e · m · 흐름 밖 (믹서 Ⓒ · 점착 축) — CBD = PVDF : CB 50 : 50 가정의 출처 · 점착이 전극 메소구조 · 수송을 바꾸는 계산 | papers/ ls srivastava* 없음 · '34919' grep = ge2022 (인용) · wishlist 없음 (batch_119 n 에도 있음) → 카드 없음
- [n] N. Iqbal, I.U. Haq, and S. Lee, Int. J. Mech. Sci. 216, 107034 (2022). (원문 참고 [38] · 인쇄 그대로) | 조건 R7 · j — Zhang p.12 가 *"particle fracture behavior … becomes one of the key factors determining the critical state of charge at which mechanical failure of the electrode occurs"* 의 근거로 든 것 (원문 내용 미확인) | papers/ ls iqbal* 없음 · '107034' grep 0 건 · wishlist 의 Iqbal (Effects of Diffusion-Induced Nonlinear Local Volume Change …) 은 다른 논문 → 카드 없음
- (세지 않음 · 이미 정본 카드 · 후보 표 · wishlist) [21] Sonzogni 2024 = 정본 `sonzogni2024_dem_rotating_roll_calendering_binder_coated_nmc811` (N-68 · 2026-11-16) · [14] Ge 2023 CEJ (wishlist L326) · [15] Lu 2020 Nat. Commun. (L74) · [12] J. Zhang 2024 Appl. Energy (L241) · [37] J. Zhang 2022 Powder Technol. (L232) · [34] Song 2023 Appl. Energy (L107 · L238) · [31] Sangrós Giménez 2018 Adv. Powder Technol. (L328).

## 카드 문제
1. **`zhang2026_xct_dem_cathode_calendering_peel_calibration` (이 카드 · 보강 대상 · 정정 표지로 고침)** — L33 '온라인 2026-09-21' 은 이 PDF 에 없다 (첫 쪽 = Received · accepted 뿐) · L222 ref 30 귀속 범위가 넓다 (원문은 X-CT 문장 끝에만 [30]) · L91 refs 4–6 이 붙은 문장이 다르다 · L394 우리 쪽 'Minnmann 순수 SE 10 % @300' 귀속 = CLAUDE.md `CL-94` 로 철회된 것 · `figures.json` f2 캡션에 본문 글이 섞여 있었다 (고침 · 옛 문자열 `caption_original_auto`).
2. **Zhang 원문 자체의 인용 문제 (카드 문제 아님 · 기록)** — 같은 문단의 자기 DEM 서술 ('접촉점이 많고 힘이 크다' · '작은 입자는 재배열 · 미끄럼으로 푼다') 끝에 X-CT 관찰 문장을 붙이고 거기에 ref 30 을 달아 근거처럼 읽힌다 · Stershic 원문에 그 서술이 없다는 것은 `stershic2015_*` 카드 · batch_120 기록.
3. **Zhang 원문 안의 어긋남 (기록 · 카드 §3.4 · §10 · 보강 표지)** — 박리 시편 *"as-prepared and fully dried"* ↔ 값은 *"calendering stress ∼ 200 MPa"* 전극 (p.6) · 박리값 0.17 ± 15 % ↔ 0.0347 ± 0.0032 MPa (p.6) · '200 MPa 이방성 개시' ↔ σ_xx/σ_yy 1.196 → 1.173 일정 (카드 D3) · 'deformation' 서술 ↔ 탄성 겹침 모델 · Fig 7 *'paticles'* · Fig 4b · 8 범례 없음 · 참고 [25] 'J. Appl. Mech. 20, 327 (2021)' · [24] 권 자리 '1882'.
4. **후보 표 N-55 '왜' 칸** (he2026 L688 에서 옮긴 *"Heckel 지수 기반 … compaction impedance"*) — 이 논문 p.1 의 [8] 서술은 *"an exponential relationship between compaction force and porosity reduction"* 뿐 · Heckel · impedance 낱말 없음 (batch_104 와 같은 지적 · 후보 표는 고치지 않음 · 메인 세션 소관).
