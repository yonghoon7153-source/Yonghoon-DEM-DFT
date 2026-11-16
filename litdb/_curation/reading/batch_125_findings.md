# batch 125 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 밖 · 1저자 직접 요청)

대상: `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` — J. Kang · T. Y. Lee (공동 1 저자) · J. Park · H. R. Shin · D. S. Kim · J. Lee · H.-G. Jung\* · J.-H. Choi\* · J.-W. Lee\*, "Stress-Regulated Li Plating in Hybrid Ag–Carbon/Carbon Nanofiber Anodes for Durable All-Solid-State Batteries", *Adv. Energy Mater.* 2026, 0:e71816 (권 · 쪽 0 = 조판 전) · DOI 10.1002/aenm.71816 · [우리 그룹].
NCM811 ‖ Li₆PS₅Cl ‖ (Li · Ag–C · Ag–C + 다공 CNF) 셀에서 operando 하중 셀로 스택 압력 요동을 재고, 2D 선형 탄성 FE (경계 변위 처방) 와 2D phase-field (Li = Coble 크리프 점도 유체) 로 해석한 음극 쪽 논문 — DEM · MPM · 양극 압밀 계산 없음.
쪽 = PDF 쪽 (본문 p.1–18 · SI p.1–42) · 판독 원자료 = `litdb/figures/kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode/digitized.csv` (55 행 · 방법은 note 열) · 고른 의도 = 메인 세션 추정 의도 (1저자 말 아님 · 카드 §0-1).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 는 분리막 0.15 g 펠릿 (성형압 · 두께 · 기공 미기재) 으로만 쓰였다.  카드 §0-1 ⑤ 의 "0.69 mm" 는 랩 표준 진밀도 1.64 g/cm³ · 기공 0 을 대입한 [카드 산술] 이지 문헌 값이 아니다.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] kang2026_stress_… | 다공 CNF 층 (SE 아님 · ≈35 µm 시편 · Pyrograf-III CNF : SBR = 2 : 1): 5 MPa 누름 → 두께 33.15 → 32.92 µm · 뺀 뒤 회복 35.11 → 34.65 µm (5 회) — 누름 변형 ≈5.6 % · 5 회 동안 회복 두께 −1.3 % | 카드 §3-5 · SI 그림 S12 (`fig_S12.png`) | [판독] (막대 윗변 · digitized.csv SI Fig. S12 10 행) + [카드 산술] | 하중 방향 1 축 · 옆 구속 · 누른 시간 미기재 · 섬유 망 (SE 아님)
- [b] kang2026_stress_… | 같은 층 5 MPa 4 h 유지: 압력 지도 P_avg 4.75 → 4.71 → 4.72 → 4.72 MPa (−0.6 %) — *"stable load transmission without pronounced time-dependent collapse"* | 카드 §3-5 · SI 그림 S11 · 본문 p.6 (`txt_p6_cnf_compression.png`) | 인쇄 (그림 글자) | 압력 이완만 · 두께 크리프 미측정
- [b] kang2026_stress_… | 셀 안 CNF 층: 제작 18.5 → 첫 충전 21.0 (+13.5 %) → 방전 뒤 18.7 µm (*"nearly recovers its initial morphology"*) · 셀 ΔP 는 충전에 오르고 방전에 내린다 (스택 20 MPa 위 1.1–2.4 MPa) | 카드 §3-2 · §3-5 · 그림 5a–b · SI 그림 S27 · 본문 p.8 · p.10 | 인쇄 (그림 글자) | 단면 SEM 이 압력 뺀 뒤인지 [미확인] · SE 의 회복량은 없다

## c — 항복 · 경도 · 크리프 값과 정의
- [c] kang2026_stress_… | Li 크리프 = Coble 꼴 B = D δ V_m / (R T d_p³) (식 17) · ε̇ = B σ_eq (식 18) · 점도 μ = 1/(3B) (식 19–20 · χ_map = 3 = 일축 → 전단) — D_interlayer 3.15 × 10⁻¹⁰ · D_host 3.15 × 10⁻¹¹ m² s⁻¹ · δ 5 × 10⁻¹⁰ m · d_p 50 / 200 nm (가정) → μ_host 0.34 × 10⁸ · μ_interlayer 0.54 × 10⁵ Pa s | 카드 §3-4 · 본문 p.15 · 표 S3 · SI 그림 S24 · `eq_17`–`eq_20` | 인쇄 + [카드 산술 재현 = 인쇄값과 같음] | Li (음극) 의 값 · 항복 문턱 없음 (뉴턴 유체) · SE · AM 항복 · 경도 없음
- [c] kang2026_stress_… | LPSCl 탄성 입력 E 22.1 GPa · ν 0.33 (K 21.7 · G 8.31 GPa [카드 산술]) — Ref. S1 (Pustorino 2025) 로 인용했으나 정본 그 카드 표 3 에 22.1 없음 (48H 29.0 · ν 0.33) | 카드 §3-3 · §3-7 ⑧ · 표 S1 (`tab_S1.png`) | 인쇄 + [다른 카드] | 항복 · 일축 항복 환산 없음 · 출처 불일치

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 양극 압밀 계산 · 하중 분담 측정 없음 (FE 는 LPSCl 한 상).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — DEM · 접촉 법칙 없음 (본문 · SI 에 DEM · discrete element 낱말 0 회).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] kang2026_stress_… | MPM 없음.  해상도 쪽 숫자만: phase-field 계면 두께 매개변수 20 nm (기공 크기 사례 10 nm) ↔ 기공 50 · 200 nm (계면 두께 ÷ 기공 ≤ 0.4) · 고체 벽 = 젖은 벽 + Navier 미끄럼 200 nm · FE 80 × 50 Q4 (요소 1.5 × 2 µm) — 격자 수렴 시험 · 수치 오차 추정 없음 · phase-field 격자 · 풀이기 · 도구 미기재 | 카드 §3-3 · §3-4 · 본문 p.14–16 (`txt_p16_phasefield_bc.png` · `txt_p14_fe_methods.png`) | 인쇄 | 유체 2 상 경계 조건 (고체 접촉 아님) · 수렴 근거 없음

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] kang2026_stress_… | 두 모델 다 2D (FE 평면 변형 · phase-field 곧은 기공) — 2D → 3D 전이에 대한 말 없음 · ⚠ 그림 6 · S21 은 2 µm × 28 µm 영역을 가로 · 세로 비율이 다르게 그렸다 (카드 판독) | 카드 §3-4 · §4-4 ③ · 그림 6 · SI 그림 S21 | 인쇄 + [판독] | 경고 · 증거 모두 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — DEM 없음 · FE 와 phase-field 는 서로도 이어지지 않는다 (카드 §4-2).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 양극 NCM : LPSCl : Super P = 72 : 27 : 1 · 450 MPa 공압착 · 기공 · 두께 미측정.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] kang2026_stress_… | FE 저자 한계: *"Although the model does not explicitly account for Li creep, interfacial separation, or fracture, it provides a comparative framework for evaluating the increasing mechanical burden associated with larger plated-Li inventories."* | 카드 §3-3 · 본문 p.4 (`txt_p4_fe_results_limits.png`) | 인쇄 | 분리 (R2) · 파괴 없이 선형 탄성
- [j] kang2026_stress_… | 스택 압력의 지위: *"the 20 MPa condition should be regarded as the selected operating condition required for stable cycling of the present powder-assembled mold-cell configuration, rather than as an intrinsic pressure requirement of the Ag–C/CNF architecture"* · 크리프 한계 (식 S9) 가 σ_stack 에 비례 → 1 · 2 MPa 파우치에서 호스트 한계 0.022 · 0.044 mA cm⁻² [카드 산술] | 카드 §3-4 · §3-6 · 본문 p.10–11 (`txt_p10_pouch_20mpa_condition.png` · `txt_p11_creep_flux_stack_pressure.png`) | 인쇄 + [카드 산술] | 몰드 셀 결과를 저압 파우치로 옮기지 말라는 저자 경고
- [j] kang2026_stress_… | 카드가 본 한계: ΔP = 상대값 · 틀 강성 · 온도 보정 · 절대 압력 곡선 없음 · 양극 수축이 섞인 합 · phase-field 는 CNF 의 실제 팽창 (18.5 → 21.0 µm) 을 계산하지 않는다 (고정 벽) · FE 첨두 σ_yy 의 용량 의존이 진술된 선형 모델로 재현되지 않음 | 카드 §0 한정어 · §3-3 ② · §11 | [카드 해석] · [카드 산술] | 압력 경계 · 탈압 계산의 검증 표적이 못 됨

## k — DEM 의 한계
(인용 서지 = Kang, J., Lee, T. Y., Park, J., Shin, H. R., Kim, D. S., Lee, J., Jung, H.-G., Choi, J.-H., Lee, J.-W. (2026). Stress-Regulated Li Plating in Hybrid Ag–Carbon/Carbon Nanofiber Anodes for Durable All-Solid-State Batteries. Adv. Energy Mater. 0, e71816. doi:10.1002/aenm.71816)
- [k] kang2026_stress_… (Kang · Lee 외 2026 · Adv. Energy Mater.) | **말 없음** — DEM 을 쓰지도 언급하지도 않는다 (본문 18 쪽 + SI 42 쪽 낱말 셈 0) | 카드 §4-4 ① | — | DEM 한계의 인용처로 쓸 수 없다

## l — 소성변형이 왜 어려운가
(인용 서지 = k 와 같음)
- [l] kang2026_stress_… (Kang · Lee 외 2026 · Adv. Energy Mater.) | Li 의 소성 · 크리프 · 셀 순응을 FE 에 넣지 않고 효과 인자 하나로 대체: *"only a fraction of the deposition-induced deformation is transferred to the SE because deformation can be partially relaxed through Li plasticity and creep, occupation of interfacial free volume, and compliance of the surrounding cell stack"* (p.4) · *"Uniform Li growth was assumed to be accommodated primarily by Li plastic flow, creep, and compliance of the cell stack and therefore was not imposed directly on the elastic LPSCl domain"* (p.15) · *"Since β is an effective model parameter rather than a directly measured material property, its influence was evaluated over a range of values (Figure S6)."* (p.4) — β = 0.003 하나 · 맞춘 대상 없음 · 0–0.005 민감도 (결론 = "용량이 크면 응력이 크다" 가 모든 β > 0 에서 유지) | 카드 §3-3 · §4-4 ② · 본문 p.4 · p.14–15 (`txt_p4_fe_model_beta.png` · `txt_p15_fe_bc_traction.png`) · SI 그림 S6 | 인쇄 | 계산 비용 [미확인] · SE 쪽 소성 없음 (SE 는 선형 탄성)
- [l] kang2026_stress_… (같은 서지) | 소성 유동을 점성 유동으로 바꾼 우회: *"Li was treated as a highly viscous Newtonian phase whose local viscosity was derived from a pore-scale Coble-type diffusion-creep relation"* (p.15) — 탄성 · 항복 · 경화 · 되돌아옴 없음 · 맞춘 값 0 (가정 4 = 기공 50 · 200 nm · 접촉각 75° · 간극 80 nm) · 검증 = SOC 10 / 50 / 75 % 단면과 정성 대조 (*"broadly consistent with the phase-field prediction that host filling approaches completion near SOC = 58%"*, p.9) | 카드 §3-4 · `txt_p8_phasefield_setup.png` · `txt_p9_soc_resolved.png` · 표 S3 | 인쇄 | 2D · 고정 벽 · 도구 · 격자 미기재

## m — 받아들일 통찰
- [m] kang2026_stress_… | **측정 안 되는 손잡이의 보고 꼴**: 값 하나 (β 0.003) + 범위 훑기 (0–0.005) + "결론이 범위 전체에서 유지되는가" 를 한 그림으로 → 우리 E_eff 18 배 연화 · MPM σ_y 보고에 같은 꼴 | 자리: 단계 0 · 후보 D0 | 근거: 본문 p.4 · SI 그림 S6 · 카드 §9 ②
- [m] kang2026_stress_… | **같이 움직이는 둘째 변수를 고정한 대조**: 적재를 올리면 전류도 오르는 교란을 0.98 mA cm⁻² 고정 셀로 갈랐다 → 우리 비교 (조성 · 입경 · 압력) 등록에 "같이 움직이는 변수" 칸 | 자리: 단계 0 | 근거: 본문 p.3 (`txt_p3_same_current_control.png`) · SI 그림 S5 · 카드 §9 ③
- [m] kang2026_stress_… | **표 → 닫힌 꼴 → 그림 값 재현 사슬**: 표 S3 값만으로 Coble 점도 · 모세관 압력 · SOC 58 % · 호스트 크리프 한계 0.437 mA cm⁻² (σ_stack 20 MPa 대입 ↔ S26 고원 ≈0.44) 가 재현됐다 → 우리 2D 단위 시험도 입력 표에서 닫힌 꼴 값을 먼저 재현하고 그림 값과 대조 | 자리: 단계 2 · U0 | 근거: 카드 §3-4 [카드 산술]
- [m] kang2026_stress_… | **볼트 틀에서는 압력이 출력**: 스택 20 MPa · Ø 13 mm 에서 반대쪽 판 치밀 Li 1 µm 당 ΔP ≈0.1 MPa (= 0.48–0.51 MPa per mAh cm⁻² · 이 틀 한정) → 언로딩 · 스택 단계에서 판 경계조건 (하중 고정 ↔ 간극 고정) 을 등록할 때 `zhang2026_anode_free_…` (0–4 MPa · ΔP/P 11–13 %) 와 나란한 실측 사례 | 자리: 흐름 밖: 스택 압력 경계조건 · 단계 6 · 조건 R4 | 근거: 본문 p.2 · 그림 1a · 카드 §3-2 · §7-2 [카드 산술]

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 (`git ls-tree` · 원격 끝 2026-11-16) + `git grep` (DOI · 권쪽 · 제1 저자 성 · 제목 낱말) — 아래 다섯 모두 자기 카드 없음 (`dixit2022_isostatic_…` · `lin2025_submicron_…` · `park2025_high_loading_…` 는 같은 성 · 다른 논문).
- [n] M. Dixit, N. Muralidharan, A. Parejiya, et al., "Differences in the Interfacial Mechanical Properties of Thiophosphate and Argyrodite Solid Electrolytes and Their Composites," ACS Applied Materials & Interfaces 14 (2022): 44292–44302, https://doi.org/10.1021/acsami.2c10589 . (원문 참고문헌 그대로 · ref 33) | c — argyrodite · thiophosphate 계면 역학 물성 (이 논문 FE 경계 처방의 인용 [31–33]) · 카드 §12 | '44292' · 'acsami.2c10589' grep = 카드 없음
- [n] C. Lin, H. Ruan, and M. Wang, "Comprehensive Study of Li Deposition and Solid Electrolyte Cracking by Integrating Simulation and Experimental Data," Advanced Science 12 (2025): 2501434, https://doi.org/10.1002/advs.202501434 . (원문 참고문헌 그대로 · ref 47) | l · c — Li 를 크리프 점도 유체로 다루는 phase-field 의 인용처 [21, 47, 48] + SE 균열 · 카드 §12 | '2501434' · 'Ruan' grep = 카드 없음
- [n] S. H. Park, K. G. Naik, Z. Li, et al., "Pressure Heterogeneity and Material Utilization in Thin-Film Solid-State Cathodes," ACS Energy Letters 11 (2026): 5086–5094, https://doi.org/10.1021/acsenergylett.6c01154 . (원문 참고문헌 그대로 · ref 31) | d · j — 불균일 경계 변위 FE 의 인용처 · 박막 양극의 압력 불균일 · 카드 §12 | 'acsenergylett.6c01154' · '5086' grep = 카드 없음
- [n] C. Fang, B. Lu, G. Pawar, et al., "Pressure-Tailored Lithium Deposition And Dissolution In Lithium Metal Batteries," Nature Energy 6 (2021): 987–994, https://doi.org/10.1038/s41560-021-00917-3 . (원문 참고문헌 그대로 · ref 59) | b · j — 스택 압력 ↔ 석출 Li 밀도 (이 논문 석출 밀도 인자 0.6–0.9 의 인용처) · 카드 §12 | '00917-3' · 'Pressure-Tailored' grep = 카드 없음
- [n] S. H. Park, K. G. Naik, B. S. Vishnugopi, P. P. Mukherjee, K. B. Hatzell, Adv. Energy Mater. 2025, 15, 2405129. (SI 참고문헌 [S3] 그대로 · 제목 미인쇄 = 서지 일부만) | f · c — phase-field 의 D_interlayer · D_host · 전자 전도도 1000 S m⁻¹ 출처 · 카드 §12 | '2405129' grep = 카드 없음 (`zhang2026_anode_free_…` L308 이 출처 후보로 언급만)

## 카드 문제
없음 — 가리킨 카드 없음 (후보 표 밖).
참고 (카드 문제 아님 · 고치지 않음): 이 논문 표 S1 의 *"Young's modulus 22.1 GPa · Ref. S1"* (= Pustorino 2025 *Chem. Mater.* 37, 313) 이 정본 `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` 표 3 (L72–L80 · E 27.8 / 29.0 / 21.7 / 29.9 / 37.9 GPa) 과 맞지 않는다 — 22.1 은 `comparison_vs_ours.md` [Deng16] 행 (L115 · E 22.1 · ν 0.37) 과 같은 숫자 · 논문 쪽 인용 문제로 읽힘 (Pustorino 원문 PDF 대조 전).
