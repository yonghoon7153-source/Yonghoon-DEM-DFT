# batch_101 — 정독 근거 (후보 표 N-52 · 한 편)

카드: `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` — K. Taghikhani · W. Huber · P. J. Weddle · M. Asle Zaeem · J. R. Berger · R. J. Kee, "Modeling coupled electro-chemo-mechanical phenomena within all-solid-state battery composite cathodes", J. Mech. Phys. Solids 198 (2025) 106060, DOI 10.1016/j.jmps.2025.106060.
원문 PDF 19 쪽 (보충 자료 없음) 을 직접 읽고 쓴 카드에서 옮겼다.  표지는 카드의 것 그대로 ([인쇄] · [판독] · [카드 산술] · [카드 해석] · [다른 카드] · [미확인]).  형식: `- [글자] slug | 내용 | 위치 | 표지 | 한계`.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

이 배치에 없음 (순수 SE 시편 · 압밀 계산이 없다.  SE 밀도 · 진밀도는 원문에 쓰이지 않는다 — 카드 §8 "단계 0" 행).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법

이 배치에 없음 (탈압을 다루지 않는다 — 적층압은 운전 내내 일정 · 출발 무응력 · 카드 §4-4 (iv) · 원문 p.9).

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기와 견줄 환산

이 배치에 없음 (모든 상이 선형 탄성 — 항복 · 경도 · 크리프 값 없음.  있는 것은 파괴 쪽 입력뿐: LPSC G_c 2.785 · NMC G_c 2.5 · 계면 G_c 1.0 J m⁻² · ℓ₀ 1 × 10⁻⁷ m [인쇄 Table 1 p.10 · 카드 §3-2] — 항복 세기와 견줄 양이 아니다).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (40 MPa 를 걸지만 상별 응력 몫을 내지 않는다 · 입자는 처음부터 접합된 연속체 — 카드 §8 "R1" 행).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음 (접촉 법칙이 없다 — 카드 §4-3).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정

이 배치에 없음 (MPM 아님.  유한요소 phase-field 의 격자 규칙 · 수치 편향 추정은 m 절에 적었다).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 2D 에서는 균열 · 계면 분리가 면 밖으로 무한히 이어진 면이 되어 효과가 과장된다: *"The fracture effects are exaggerated in a 2D model because the cracks propagate infinitely in the out-of-plane direction."* — 무압 계산에서 실험에 없는 전압 계단 셋 (Q ≈103 · 122–124 · 128 mAh g⁻¹) 이 나온 것을 이렇게 설명 | 카드 §3-6 · §4-4 (iii) · §10 ② · 원문 p.12 · Fig. 9a | [인쇄] (계단 위치는 [판독 · 벡터 경로]) | 2D 평면 변형 phase-field (선형 탄성) 의 말 — 접촉 · 소성 계산이 아님.  3D 대조 계산은 없다 (과장의 크기는 재지 않았다)
- [g] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 모형이 세 전류 모두 용량을 과대 예측 (+4.7 / +7.0 / +13.7 %) 하는 원인의 첫째로 2D 를 든다: *"the quantitative discrepancies are likely due to model simplifications, including using a 2D model, the assumption of isotropic behavior in cathode particles, and neglecting factors such as randomly oriented primary-secondary morphology, inter-granular fracture, and formation of resistive cathode-electrolyte interphase (CEI) layer."* | 카드 §3-5 · 원문 p.11 · Fig. 7 | 문장 [인쇄] · 백분율 [판독] | 원인들이 분리되지 않았다 (2D 몫이 얼마인지 모른다)
- [g] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 2D 를 고른 이유 = 계산 자원: *"Although the model is fully capable of representing three-dimensional microstructures, the present paper reports results in a two-dimensional setting using a plane-strain assumption. Practical limitations for needed computational resources make full three-dimensional simulations impractical for parametric studies."* · 2D 에서도 ≈3.5 M 자유도 | 카드 §3-4 · §4-4 · 원문 p.9 · p.14 | [인쇄] | 요소 수 · 계산 시간 · 기계는 [미확인]
- [g] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 평면 변형 + 면 밖 화학 팽창 없음이 3D 입자의 응력 상태를 더 잘 나타낸다고 주장 (근거 = 같은 저자의 2024 논문): *"The two-dimensional mechanics are simplified from 3D by assuming a plane-strain condition with no chemical expansion in the out-of-plane direction. This simplification provides a more accurate representation of the state of stress in 3D particles (Taghikhani et al., 2024)."* | 카드 §4-1 끝 · 원문 p.9 | [인쇄] | 근거 논문 (Electrochim. Acta 479, 143790) 은 카드 없음 → n 절

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음 (DEM 을 쓰지 않는다.  출발 기하는 SEM 그림을 Adobe Illustrator 로 고쳐 im2mesh 로 격자를 만든 것 — 카드 §3-1 · §4-2 · 원문 p.6).

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (압력별 기공이 없다.  기공은 입력 기하의 한 값이다: Fig. 3 캡션 "≈15% porosity" = 손으로 고친 2D 그림의 면적 분율 · 래스터 색 분류 판독 12.5 % (윤곽선 빼고 다시 나누면 14.5 %) [판독] · 대조 구조 "no pores" — 카드 §3-1 · §3-6.  원문이 문헌 값으로 옮긴 "5% void volume fraction (Kodama et al., 2020)" (p.2) 는 정본 kodama2020 카드로는 뒷받침되지 않고 · "6% to 30% (Bielefeld et al., 2020)" (p.14) 는 정본 bielefeld2020 카드에 없는 문장이다 [다른 카드]).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 성형 뒤 잔류 응력을 넣지 않았다: *"The present model assumes the structure to be stress-free at the initial condition (x = 0.97). This assumption neglects the effect of residual stress developed during the fabrication process. These residual stress effects are the focus of ongoing studies."* | 카드 §3-10 ① · §10 ① · 원문 p.9 | [인쇄] | 2D · 선형 탄성 모형의 말 — 잔류 응력의 크기 · 영향은 계산하지 않았다
- [j] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 적층압을 바꿔도 결과가 거의 안 변한다는 고백: *"It is notable that the present model has limitations in evaluating the effects of changing external pressure. Modifying the pressure results in only slightly changes to the voltage profiles. To capture this effect, future models should include a larger region of interest or incorporate the fracture mechanism within the polycrystalline NMC particles."* — 판독으로도 0 MPa 150.7 · 5 MPa 185.6 · 40 MPa 185.7–186.5 mAh g⁻¹ (0.1 C 충전 끝) | 카드 §3-6 · 원문 p.13 · Fig. 10a · 13 | 문장 [인쇄] · 값 [판독 · 벡터 경로] | 운전 적층압 (성형압 아님) · 계면 G_c 1.0 J m⁻² · ℓ₀ 100 nm 가정 · 2D
- [j] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 길이 척도 (= 강도) 를 자료 없이 골랐다: *"In the absence of empirical data on strength of materials, the parameter selection relies on reasonable approximations aligned with available estimates in the literature"* · 결론: *"The predictions depend on fundamental materials properties, some of which are yet to be measured and validated."* | 카드 §3-4 · §3-10 ⑧ · 원문 p.9 · p.15 | [인쇄] | —
- [j] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | NMC 입자 안 (1 차 입자 사이) 파괴 · 방향성 · 사이클 피로 · CEI 를 넣지 않았다 | 카드 §3-10 ④ · ⑤ · ⑦ · 원문 p.10 · p.11 · p.14 | [인쇄] | 조건 R7 은 계면 쪽만 채운다

## k — DEM 의 한계 (논문이 직접 말한 문장 · 수치)

- [k] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode (Taghikhani, Huber, Weddle, Asle Zaeem, Berger, Kee, 2025, J. Mech. Phys. Solids 198, 106060) | **말 없음** — DEM 을 쓰지도 인용하지도 않는다 (낱말 *discrete · DEM* 0 회).  선행 방법으로 든 것은 응집 영역 · phase-field · 연속체 손상 · 유효 스프링 · 확장 유한요소 (*"cohesive zone modeling … phase-field fracture … continuum damage … effective springs … and extended-finite-elements … to predict electrode cracking"*) 와 P2D 뿐 | 카드 §4-4 (i) · 원문 p.2–3 (전수 검색) | [인쇄] (낱말 셈 = 카드 "원문 대조 기록") | DEM 한계의 reference 로는 쓸 수 없다

## l — 소성변형이 왜 어려운가 (논문의 설명 · 우회 · 맞춘 값 · 검증 · 비용)

- [l] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode (Taghikhani, Huber, Weddle, Asle Zaeem, Berger, Kee, 2025, J. Mech. Phys. Solids 198, 106060) | **이유를 설명하지 않고 소성을 뺐다.**  서론은 *"sulfide-based solid electrolytes (e.g., LPSC) are sufficiently malleable so as to maintain interfacial contact under external pressure"* (p.2) 라고 하면서 구성식은 선형 탄성 + 손상 (식 28 · 30) · 작은 변형 (식 12) 이다 (낱말 *plastic · yield · creep* 0 회).  우회 = 없음 (탄성 + 취성 phase-field 파괴 · LPSC E 22.1 GPa · ν 0.37 = DFT 값).  맞춘 값 = 0 개 (계면 G_c 1.0 J m⁻² · ℓ₀ 100 nm 는 가정값 · 검증 곡선과의 차 +4.7 / +7.0 / +13.7 % [판독] 는 그대로 둠).  검증 = Bielefeld 2022 에서 다시 실은 전압–용량 곡선 한 벌 (세 전류 · 40 MPa).  비용 = 2D 에서 2 차 삼각 요소 ≈3.5 M 자유도 · segregated solver · 3D 는 *"impractical for parametric studies"* (p.14) · 물성을 상수로 둔 이유도 *"to reduce the computational cost"* (p.10) — 입자 수 ≈125 (판독) · 계산 시간 [미확인] | 카드 §4-4 (ii) · §3-4 · §3-5 · 원문 p.2 · p.4 · p.7 · p.9 · p.10 · p.14 | 문장 · 식 [인쇄] · 백분율 · 입자 수 [판독] | 압밀 계산이 아니라 주어진 구조 위의 충방전 계산이다 — "소성이 어렵다" 는 문장의 reference 가 아니라 "최신 결합 모형도 SE 소성 · 성형 이력을 뺀다" 는 사례로만 쓴다.  제1 주응력 색 눈금 −200 … 800 MPa [판독 Fig. 8c] 는 탄성이라 남는 값이다

## m — 받아들일 통찰 (바로 가져다 쓸 것)

- [m] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 탈압 계산의 산출물로 "성형 뒤 잔류 응력 장 · 계면 상태" 를 적는다 — 이 계열의 최신 결합 모형이 무응력 출발로 비워 두고 "진행 중 연구" 라고 적은 입력이다 | 단계 6 | 원문 p.9 인용 (카드 §10 ①) · 카드 §7-2 · §9 ②
- [m] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 2D 벤치마크의 분리 · 균열 효과를 3D 크기로 읽지 않는다는 한정어 + 근거 문장 (2D 에서 분리는 면 밖 무한한 면 · 실험에 없는 전압 계단) | 단계 2 · 단계 3 | 원문 p.12 (카드 §10 ②) · Fig. 9a 판독 (카드 §3-6)
- [m] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 접촉 원장의 G_c 는 계보를 적는다: 이 논문 LPSC 2.785 J m⁻² 와 우리 원장의 Bucci 2.8 ± 1.8 은 같은 뿌리 (McGrogan 2017 의 Li₂S–P₂S₅ 유리 K²/E) 라 독립 앵커 둘이 아니고 · NMC–SE 계면 1.0 J m⁻² 는 무출처 가정인데 결과가 1 ↔ 2 J m⁻² 사이에서 갈린다 (무압 0.1 C 용량 150.7 ↔ 185.8 [판독]) | 후보 D0 (접촉 원장) · 조건 R2 | 카드 §3-2 · §3-6 · §7-3 · Table 1 p.10 · Fig. 12 · [다른 카드 mcgrogan2017 L72]
- [m] taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode | 수치 기법이 만든 편향을 손으로 풀리는 1D 문제로 잰다 (문턱 + 이력 장 풀이가 균열당 15/(8√2) = 1.326 G_c 를 소산 — 식 35–37) · 그리고 길이 척도를 고르는 것이 곧 강도를 고르는 것 (σ_c ∝ √(G_c·E / ℓ₀) [카드 산술]) · 한 방향 적층압은 압력 축과 나란한 계면을 누르지 못한다 (40 MPa 에서도 가로 균열 띠 [판독]) | 흐름 밖: 사이클 열화 모형 (phase-field 를 들일 때) · 적층압 ↔ 재접촉 대응 | 카드 §3-4 · §3-8 · §3-9 · 원문 p.7–8 · Fig. 8b · 14b

## n — 논문 에이전트 후보 (이 논문이 인용 · 정본에 카드 없음 · 서지는 이 논문 참고문헌 목록 그대로)

- [n] Bielefeld, A., Weber, D.A., Rueß, R., Glavas, V., Janek, J., 2022. Influence of lithium ion kinetics, particle morphology and voids on the electrochemical performance of composite cathodes for all-solid-state batteries. J. Electrochem. Soc. 169 (2), 020539. | 질문 i · m — 이 논문의 검증 곡선 · 농도 의존 D · i₀ · 개회로 전압 · 초기 x · 공극률 · 입자 크기의 원전 (실험 셀 조건과 0.5 C ↔ 5 C 표기 어긋남을 가를 수 있다 · 공극이 전기화학에 주는 영향) · 카드 §3-3 · §3-5 · §12 · jeong2024 카드 §12 도 "카드 없음" 으로 가리킴 | litdb 확인: papers/ 에 bielefeld2019 · bielefeld2020 뿐 · "020539" grep = 인용만 → 카드 없음
- [n] Taghikhani, K., Weddle, P.J., Hoffman, R.M., Berger, J.R., Kee, R.J., 2023. Electro-chemo-mechanical finite-element model of single-crystal and polycrystalline NMC cathode particles embedded in an argyrodite solid electrolyte. Electrochim. Acta 460, 142585. | 조건 R2 · R7 · 질문 m — 정본 lei2026 카드 L115 의 "계면 분리 최대 틈 9.3 / 16.0 / 13.8 nm (r_s 0.5 / 1.5 / 3.0 µm)" · 단결정 ↔ 다결정 비교의 원문일 가능성 (이 JMPS 논문에는 그 값이 없다 — 아래 카드 문제) · 카드 §0-1 · §12 | litdb 확인: papers/ 에 taghikhani* 는 이 카드뿐 · "142585" grep 0 건 → 카드 없음
- [n] Taghikhani, K., Singh, A., Weddle, P.J., Colclasure, A.M., Smith, K., Berger, J.R., Kee, R.J., 2024. Consequences of plane-strain and plane-stress assumptions in fully coupled chemo-mechanical Li-ion battery models. Electrochim. Acta 479, 143790. | 질문 g — 2D 가정 (평면 변형 ↔ 평면 응력) 이 3D 입자 응력과 얼마나 다른지를 직접 다룬 논문 (이 논문 p.9 가 근거로 인용) · NMC E 175.27 GPa · ν 0.2819 · β^iso 의 출처 · 카드 §3-2 · §4-1 · §12 | litdb 확인: "143790" grep 0 건 → 카드 없음
- [n] Conforto, G., Ruess, R., Schröder, D., Trevisanello, E., Fantin, R., Richter, F.H., Janek, J., 2021. Editors' choice—quantification of the impact of chemo-mechanical degradation on the performance and cycling stability of NCM-based cathodes in solid-state Li-ion batteries. J. Electrochem. Soc. 168 (7), 070546. | 조건 R7 · 질문 m — 화학–역학 열화가 성능 · 수명에 주는 몫을 실험으로 정량 (이 논문 결론이 "압력 범위 실험과 일치" 의 근거로 든 논문 — 본문 자료로는 뒷받침되지 않아 원문 확인 필요) · 카드 §3-11 ⑧ · §12 | litdb 확인: "conforto" · "070546" grep = 인용만 → 카드 없음
- [n] Zhang, F., Guo, Y., Zhang, L., Jia, P., Liu, X., Qiu, P., Zhang, H., Huang, J., 2023. A review of the effect of external pressure on all-solid-state batteries. Etransportation 15, 100220. | 질문 b · i · j — 성형압 ↔ 운전 적층압의 효과를 모은 리뷰 (이 논문 서론이 "제조 중 계면 균열 · 공극" 의 근거로 인용) · 카드 §12 | litdb 확인: papers/ 의 zhang2023 은 `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` (다른 논문) · "100220" grep 0 건 → 카드 없음

(다섯을 넘어 n 절에 싣지 않은 것 — 카드 §12 에만: Ruess 외 2020 J. Electrochem. Soc. 167 (10), 100532 · Lim 외 2017 Sci. Rep. 7, 39669.)

## 카드 문제

- `lei2026_se_particle_size_effects_review` L115 · L172 (관련 L144 · L162 · L174 · L213 · L234) + 후보 표 `S8_candidates.md` N-52 의 근거 칸: L115 의 *"NMC 단결정 · 다결정 2D FEM (Taghikhani): 계면 분리 최대 틈 9.3 nm (r_s 0.5 µm) · 16.0 (1.5) · 13.8 (3.0) … [2차 · ref 166 · Fig. 4c]"* 와 L172 의 *"NMC 입자 r_s 0.5 · 1.5 · 3.0 µm 의 Li 농도 · von Mises … [166]"* 는 **이 JMPS 2025 논문에 없다** (nm 단위 틈 · 입자 반지름 사다리 · 단결정 ↔ 다결정 비교 · von Mises 그림이 원문 19 쪽 전수에 없음).  리뷰의 ref 166 은 다른 Taghikhani 논문 (제목으로는 2023 Electrochim. Acta 460, 142585) 일 가능성이 크다 — lei2026 카드에 ref 166 의 서지가 적혀 있지 않아 확정하지 못했다.  후보 표가 그 줄들을 이 논문의 근거로 묶은 것이 귀속 문제다.  카드는 고치지 않았다.
- `liang2026_interface_bottleneck_solid_state_batteries` L246 (*"FEM phase-field fracture(복합양극 [97] Taghikhani et al., JMPS 198, 106060)"*) · `zhang2026_polymer_electrolyte_modeling_perspective` L124 (ref 162 서지 전문) = 원문과 같다 (문제 없음).
- 이 카드 (`taghikhani2025_…`) 안의 서로 다른 두 값은 전부 원문 자체의 어긋남이다 (카드 §3-11 의 16 건 — 0.5 C ↔ 5 C · 계면 G_c 0.2 ↔ 0.5 · x 0.97 ↔ 0.9729 · G_c 2.79 ↔ 2.785 · 사이클 규약 · 같은 조건의 끝 용량 183.8–186.4 등).
