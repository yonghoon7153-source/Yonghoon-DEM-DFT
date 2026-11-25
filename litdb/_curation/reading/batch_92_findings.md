# 배치 92 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-1)

카드 = `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` (원문 = 출판본 10 쪽 · SI 안내 없음 · 그림 크롭 45 장 = 도구 9 (다시 자름 4 — Fig 2 · 7 · 8 · 표 1) +
손 크롭 36 (패널 15 · 식 2 · 근거 문단 19) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 146 행).
서지 (k · l 인용용) = Ohashi A., Kodama M., Sun X. (머리글 'Sun Xueying'), Hori S., Suzuki K., Kanno R., Hirai S.,
*Stress distribution in the composite electrodes of sulfide all-solid-state lithium-ion batteries*, J. Power Sources 470 (2020) 228437,
DOI 10.1016/j.jpowsour.2020.228437.
⚠ 재료 = **Li₁₀GeP₂S₁₂ (LGPS)** + **ZrO₂ (활물질 대리 · E 200 GPa)** — LPSCl · NCM 아님 · 계산 = 선형 탄성 복셀 FEM + 응력 → 국소 σ 복셀 전도 (DEM · MPM · 압밀 계산 없음).  쪽 = PDF 쪽 p.1–10 (= 인쇄 쪽).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] ohashi2020_stress_distribution_composite_electrode_sulfide_assb | **기공 곡선 없음** — 순수 SE 는 σ(P) 만: LGPS 0.0205 (0.63 MPa) · 0.428 (8.4 · 꺾임) · 0.765 (50) · **1.168 (100)** · 1.40 mS/cm (128.6 MPa · 곡선 끝) — 0.6 → 8.4 MPa ×21 급경사 · 10–125 MPa 거의 직선 (0.0080 mS/cm/MPa) | 카드 §3-2 · 그림 5 | [판독] · [카드 산술] | LGPS · 가압 가지만 · 누른 채 · 진밀도 · 기공률 · 온도 없음 · 맞춤 식 [미확인]
- [a] ohashi2020_… | 그림 5 삽도 (순수 SE 두 두께 2.7 · 0.8 mm) 저항으로 지름 1 mm 단면을 넣어 낸 σ ≈0.62 mS/cm (99 MPa) ↔ 본 곡선 1.17 — 1.9 배 어긋남 · 단위 길이 저항 21.1 ↔ 22.1 kΩ/mm (99 MPa) | 카드 §3-2 | [판독 · 카드 산술] | 순수 SE 시료 단면 · 본 곡선 출처 [미확인] — 절대 σ 인용 때 이 어긋남을 같이 적는다

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] ohashi2020_… | **없음** — 복합체 · 순수 SE 모두 가압 (100 MPa · σ(P) 가압 가지) 만 · 탈압 측정 · 계산 0 | 카드 §0 · §4-4 (iv) | [미확인] | —

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] ohashi2020_… | 항복 · 경도 · 크리프 **없음** · 영률만 (표 1): LGPS **21.7 GPa** (*"first-principle calculation [23]"* = Deng 2016 · 참밀도 최대) · **0.3 GPa** (*"obtained experimentally for a compressed powder by considering total strain and applied stress"* = 압분체 할선 · 최소 · 시험 조건 · 인용 없음) · ν 0.37 · ZrO₂ 200.0 GPa · ν 0.30 (출처 없음) | 카드 §3-6 · 표 1 · p.3 | [인쇄] | 일축 항복 환산 없음 · 0.3 GPa = 같은 그룹 kodama2020 의 분말 할선 (25–250 MPa) 과 같은 꼴의 양 [다른 카드]
- [c] ohashi2020_… | CL-90 대조: NCM 경도 · NCM 영률 (140 GPa) · LPSCl 영률 (24 GPa) 은 **이 논문에 없다** — 'NMC' 3 회 모두 '고영률 활물질의 예' 문장 · 참고문헌의 'Wang' = [23] 2 저자 · [26] Z.Q. Wang 2014 (LGPS DFT · Int. J. Electrochem. Sci.) | 카드 §0-1 ② · §3-6 | [인쇄 · 전수 낱말 검색] | CL-90 인용의 정체를 이 논문으로 메울 수 없다 (같은 권일 뿐)

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] ohashi2020_… | ★ SE 평균 최소 주응력 (MPS) **87.7 · 66.0 · 60.9 · 48.9 MPa** (ZrO₂ 19 · 42 · 55 · 67 vol% · 인가 100 MPa · E_SE 21.7 · E_ZrO₂ 200 GPa) · 본문 42 vol% *"average and mode … approximately 66 and 69 MPa"* · 67 vol% *"approximately 50 MPa"* | 카드 §3-3 · 그림 6b · p.6 | [판독] · [인쇄] | 선형 탄성 · 결합 연속체 · 빈틈 0 · ZrO₂ 대리 · 100 MPa 한 점 · E_SE 0.3 GPa 계산의 응력은 그림 없음
- [d] ohashi2020_… | 평균 응력 정리 (f⟨σzz⟩_hard + (1 − f)⟨σzz⟩_SE = 100 MPa · MPS ≥ σzz) 로 ZrO₂ 축하중 몫 **≥ 0.29 · 0.62 · 0.73 · 0.84** · Voigt 0.68 · 0.87 · 0.92 · 0.95 · Reuss = f 사이 · 42 vol% 분포: SE 봉우리 61.6 · 평균 68.4 · ZrO₂ 봉우리 127.9 · 평균 153.0 MPa · 비 (평균) 2.24–2.32 ↔ 영률 비 9.2 | 카드 §3-3 | [카드 산술 · 판독] | 하한 (σzz ≤ MPS) · 우리 DEM 상별 virial (300 MPa 0.794 · φ_AM ≈0.62) 과 숫자만 가깝다 (≈0.79 보간) — 같은 양 아님 · 교차검증으로 쓰지 않음
- [d] ohashi2020_… | 저자 해석: *"zirconia acts as a stress support, decreasing the stress propagating through the SSE. As the volume fraction of zirconia increases, the rigidity of the stress support increases"* (p.9) · NCM 으로의 확장 = 외삽 문장 (*"active materials with high Young's modulus such as LCO, NMC, Si"* p.6) · ZrO₂ ≈ AM 영률 근거 [18] = LCO 한 편 | 카드 §0-1 · §3-3 | [인쇄] | NCM 계산 · 측정 없음 · 재밍 · 힘 사슬 · 접촉 진술 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- [e] ohashi2020_… | **없음** — 점접촉 · DEM 을 쓰지 않는다 · 대안 = 접촉 법칙 없는 **결합 연속체** (복셀 FEM · 맞춘 값 0 · 불확도 = E_SE 두 극단 21.7 ↔ 0.3 GPa → 막대 ×1.3–11.6) | 카드 §4-2 · §3-4 | [인쇄] · [카드 산술] | 접촉 · 미끄럼 · 분리 없음 (복셀 절점 공유 = 결합 [카드 추론])

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

- [f] ohashi2020_… | MPM 없음 · 복셀 FEM 해상도: 복셀 4 × 4 × 5 µm · ZrO₂ (< 150 µm) ≈30–37 복셀 · LGPS 입자 (< 40 µm) ≤ 8–10 복셀 → SE 입자 · 빈틈 안 풀림 (*"treated as void-free … voids smaller than voxel size could not be distinguished from the SSE"*) · ≈300 × 300 × 400 = 3.6 × 10⁷ 복셀 · 자유도 ≈1.09 × 10⁸ · 수렴 · 해상도 시험 0 · 수송 수렴 = *"current values through the composite in the z-direction were uniformly distributed"* | 카드 §4-2 · §4-3 · p.3–4 | [인쇄] · [카드 산술] | 수치 오차 추정 없음 · 요소 · 풀이기 · 시간 [미확인]

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] ohashi2020_… | 측정 · 계산 모두 3D (CT · 3D 복셀 FEM · 3D 전도) · 그림 8 은 3D 결과의 2D 단면 · 2D → 3D 진술 **없음** | 카드 §4-4 (iii) | [인쇄] | —

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

- [h] ohashi2020_… | DEM 아님 · **실측 CT → FE** 로 넘긴 선례: 100 MPa 누른 채 찍은 형상을 응력 없는 출발로 두고 **추가 100 MPa** 를 선형으로 건다 — *"the virtual pressurization with VOXELCON corresponded to applying an additional pressure of 100 MPa. Nevertheless, analytical results were approximately equal to the actual stress distribution … because the stress calculation relied on the assumption that no large-scale deformation occurred under linear stress analysis"* (p.3) | 카드 §4-2 | [인쇄] | 압밀 이력 · 잔류 응력을 버리는 가정 — 우리 DEM → MPM (눌린 상태를 넘기는) 때 같은 가정을 쓰면 적어 둘 것

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] ohashi2020_… | **없음** — 복합체 빈틈은 CT 에서 안 보여 고체로 셈 · 'volume fraction' = ZrO₂ 부피만 (*"The voids present in the SSE are not included in the volume fraction"* p.6) · 복합체 σ 실측값도 없음 (그림 7 = 계산 ÷ 실측) → Wiener 상한으로 실측 복합체 ÷ 순수 SE ≤ 0.47 · 0.33 · 0.096 · 0.079 | 카드 §3-4 | [카드 산술 · 상한] | 기공 대신 σ 비의 상한뿐

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] ohashi2020_… | *"This margin of error is attributed to the non-linearity of the stress–strain relationship of the SSE powder … Non-linear stress analysis is necessary to minimize the margin of error. In the current study, which uses linear stress analysis, it is impossible to determine whether the isotropic (Case 2) or anisotropic (Case 3) model is more accurate"* (p.9) | 카드 §4-4 (ii) · 크롭 `txt_p9_margin_error_nonlinear_linear_analysis.png` | [인쇄] | —
- [j] ohashi2020_… | *"Currently it is not possible to discuss which nanoscale features, such as void content, tortuosity, or particle contact area, is the dominant factor affecting ion transport in local regions"* (p.9) · *"We initially assume that the void ratio of the SSE is solely dependent on stress"* (p.6–7) | 카드 §0-1 · §4-3 | [인쇄] | AM–SE 접촉 감소 의도에 대한 '없음' 의 근거

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] ohashi2020_… (Ohashi et al. 2020, J. Power Sources 470, 228437) | **말 없음** — DEM 을 쓰지 않는다.  가까운 문장 (분말 일반): *"because the SSE is a powder, its Young's modulus may vary with pressure depending on the resultant non-linear stress–strain relationship [24–26]"* (p.3) | 카드 §4-4 (i) | [인쇄] | DEM 한계의 근거로 인용하지 않는다

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] ohashi2020_… (Ohashi et al. 2020, J. Power Sources 470, 228437) | 소성을 **넣지 않는다** — 선형 탄성 (Hooke · Galerkin) 한 번 · 우회 = SE 영률 두 극단 (참밀도 DFT 21.7 GPa ↔ 압분체 할선 0.3 GPa) 으로 오차 막대 (맞춘 값 0) · 이유 진술: *"Because the SSE in the composite electrode contained voids, it had a Young's modulus different from that of the true density state"* (p.3) · *"Non-linear stress analysis is necessary to minimize the margin of error"* (p.9) · 비용 = 3.6 × 10⁷ 복셀 GPU 선형 풀이 한 번 (시간 [미확인]) · 검증 = 그림 7 (막대 ×1.3–11.6 · 42–67 vol% 에서 1 을 포함) | 카드 §4-4 (ii) · §3-4 | [인쇄] · [카드 산술] | 판별력 약한 검증 (저자도 Case 2 ↔ 3 구분 불가)

## m — 받아들일 통찰

- [m] ohashi2020_… | **방법 · 결과 전 대조**: 'SE 평균 축응력 ÷ 인가압 vs 단단한 상 분율' 네 점 (0.88 · 0.66 · 0.61 · 0.49 · 선형 탄성 · E 대비 9.2) 을 AM 이 하중을 지는 MPM 의 탄성 기준선으로 — 자리 = 단계 5 · 후보 A · A′ · B · 조건 R1 · 결과 전 대조 항목 · 근거 그림 6b · p.6 | 카드 §7-3 · §8 | [판독] | 같은 양 · 표지 (탄성 · 결합 · 빈틈 0) 필수
- [m] ohashi2020_… | **검증 규칙**: 상별 평균 응력 출력은 평균 응력 정리 (f⟨σ⟩_hard + (1 − f)⟨σ⟩_soft = P) 로 먼저 거른다 — 그들 그림 6a 는 평균으로는 맞고 (104 MPa · MPS ≥ σzz) 넓이 비 (0.69) 는 42 vol% 와 안 맞았다 (= 그림 정규화가 부피가 아님) — 자리 = 단계 0 · 단계 5 · 근거 카드 §3-3 · §3-7 | 카드 §3-3 | [카드 산술] | —
- [m] ohashi2020_… | **함정**: 기하만 넣은 복셀 σ (Case 1 = 우리 STEP3 꼴 · CONTACT_FREE) 가 단단한 상 19–67 vol% 에서 실측을 1.72–4.71 배 넘는다 (순수 SE 1.07 보다 큼) → STEP3 σ_ion 을 실험 옆에 둘 때 'AM 분율 클수록 상한 과대 ↑' 한정어 — 자리 = 단계 7 · 흐름 밖: STEP3 · 근거 그림 7 · p.6 | 카드 §7-4 | [판독] | 배수 전이 금지
- [m] ohashi2020_… | **관측량 해석**: σ(P) 저압 급경사 (0.6 → 8.4 MPa ×21) 때문에 복합체 σ 는 SE 평균 응력이 아니라 저응력 꼬리 · 좁은 목이 정한다 (Case 1 → 2 ×0.43 ↔ 평균 66 MPa 만이면 ×0.76) — 자리 = 단계 7 · 흐름 밖: Rint ② (SE–SE 협착) · 근거 그림 5 · 7 · 8 · p.9 | 카드 §3-5 | [카드 산술 · 카드 추론] | 응력장 → σ 변환 때 평균만 넘기지 않는다

## n — 논문 에이전트 후보

- [n] E.J. Cheng, N.J. Taylor, J. Wolfenstine, J. Sakamoto, Elastic properties of lithium cobalt oxide (LiCoO2), J. Asian Ceram. Soc. 5 (2017) 113–117, https://doi.org/10.1016/j.jascer.2017.03.001. | c · d — 'ZrO₂ 영률 ≈ 활물질 (LCO · Si · NMC)' 의 유일한 근거 [18] · LCO E (koerver2018 L187 이 191.0 GPa 로 옮김) — 카드 §3-6 · §12 | litdb 확인: ls cheng2017* 없음 · "jascer" grep = koerver2018 · sharma2023 · stallard2022 인용만 · wishlist · S8 에 'jascer' · 'Asian Ceram' 없음 → 카드 없음
- [n] Z.Q. Wang, M.S. Wu, G. Liu, X.L. Lei, B. Xu, C.Y. Ouyang, Elastic properties of new solid state electrolyte material Li10GeP2S12: a study from first-principles calculations, Int. J. electrochem. Sci. 9 (2014) 562–568. | c — LGPS 탄성 DFT · 비선형 응력–변형 근거 [24–26] 의 하나 · CL-90 'Wang' 대조 (2014 · 다른 학술지 — 이 줄로 CL-90 을 잇지 않는다) — 카드 §0-1 · §12 | litdb 확인: ls wang2014* 없음 · "562–568" grep 0 (이 서지) · deng2016 카드 L38 이 'Wang 2014' 를 선행 DFT 로 언급만 → 카드 없음
- [n] A. Kato, M. Nose, M. Yamamoto, A. Sakuda, A. Hayashi, M. Tatsumisago, Mechanical properties of sulfide glasses in all-solid-state batteries, J. Ceram. Soc. Jpn. 126 (2018) 719–727, https://doi.org/10.2109/jcersj2.18022. | c — 황화물 분말 · 유리의 비선형 응력–변형 · 기계 물성 [24–26] — 카드 §4-4 · §12 | litdb 확인: ls kato2018* = kato2018_thick_electrode_assb_cycle_tortuosity (다른 논문 · J. Phys. Chem. Lett.) · "jcersj2.18022" grep 0 · 제목 낱말 "Mechanical properties of sulfide glasses" grep = var2026 인용만 → 카드 없음
- [n] Y. Nagano, Y. Ikeda, H. Kawamoto, N. Takano, Image-based modeling by 3-D CT for homogenization stress analysis - application to porous ceramics -, 52, 2004, https://doi.org/10.11396/jjsndi.53.701, 701-701. (서지 일부만 — 원문 목록에 학술지 이름 없음) | f · h — VOXELCON [22] · CT 영상 기반 균질화 응력 해석의 방법 원전 (복셀 FEM 의 결합 가정 · 해상도) — 카드 §4-2 · §12 | litdb 확인: ls nagano* 없음 · "jjsndi" grep 0 · "Nagano" grep = 다른 논문의 다른 줄 → 카드 없음
- [n] G. Bucci, T. Swamy, S. Bishop, B.W. Sheldon, Y.-M. Chiang, W.C. Carter, The effect of stress on battery-electrode capacity, J. Electrochem. Soc. 164 (2017) A645, https://doi.org/10.1149/2.0371704jes. | d · j — 활물질 응력 ↔ 용량 (서론 [15] · SE 가 AM 경계를 구속해 사이클 응력) — 카드 §12 | litdb 확인: ls bucci2017* = bucci2017_chemomech_failure_assb_cycling_czm (J. Mater. Chem. A · 다른 논문) · "2.0371704jes" grep 0 → 카드 없음

## 카드 문제

- `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` L363 (ref 24 행): 둘째 문장 *"strain caused by the pressure reduces the contact between the AM and SE"* 을 ref 24 의 근거로 적었는데 Sakka 원문은 refs **18 · 24** 를 함께 단다 — L365 (ref 18 행) 과 같이 읽으면 원문 그대로이고, Ohashi 원문에 그 내용이 없다는 것은 **Sakka 원문의 인용 범위 문제** (카드 문제 아님 · 고치지 않음 · 관련 카드 줄 한 줄로 이음).
- `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` L363: *"A. Ohashi … 228437 … 정본 카드 없음"* — 11-17 부터 카드가 있다 · 줄은 그대로 두고 관련 카드 절에 한 줄 보탬.
- `heck2026_densification_sulfide_se_binder_scalable` L305: 저자 표기 'S. Xueying' (머리글 'Sun Xueying') = Heck 원문 그대로 (카드 문제 아님) · 그 줄의 'CL-90 … [미확인]' 에는 이 카드 §0-1 ② 가 답 (세 값 없음) — 관련 카드 절에 한 줄 보탬.
- (원문 문제 · 이 카드 §3-7 에 기록) 그림 6a 넓이 비 0.69 ↔ 42 vol% · 본문 '최빈 69 MPa' ↔ 그림 봉우리 61–63 MPa · 그림 5 삽도 σ ≈0.6 ↔ 본 곡선 1.17 mS/cm · 41 ↔ 42 vol% · 계면 이름 섞임 (LGPS/Li · LGPS/SE · Li/SE) · 참고문헌 [7] · [22] 학술지 이름 빠짐.
