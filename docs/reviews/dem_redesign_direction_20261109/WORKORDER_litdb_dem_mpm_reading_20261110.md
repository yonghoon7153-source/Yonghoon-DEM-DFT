# 작업지시서: litdb 정본의 DEM · MPM 축 정독 (본 세션 · 2026-11-10)

1저자 11-10: "본 브랜치에서도 원래 litdb에 있는 DEM, MPM 섹션 정독도 같이 하라".
받는 곳은 본 세션 (stoic) 이고, 트랙은 [DEM 우선 (수영)] 입니다. 새 계산은 없습니다. 읽고 정리하는 일입니다.

## 0. 왜 하는가

- 방향 메모 3.1 판이 정본에 이미 있던 LPSCl 카드 셋 (lee2025 · miss2026 · thompson2026) 을 쓰지 않았습니다. 사전 공격 세 번도 놓쳤습니다 (원장 SELF-161).
- 새 논문을 더 먹이기 전에, 이미 가진 카드를 끝까지 읽어 계획에 쓸 것과 빠진 것을 가립니다.
- 결과는 메모 3.2 판에 들어갑니다. 3.2 는 Codex 판정 처분 (DRD-01–13) 과 같이 고칩니다.

## 1. 범위

정본은 가지 claude/friendly-meitner-lldvar 의 litdb 폴더입니다. 이 가지는 다른 세션이 계속 올립니다 (11-10 아침에도 올라옴). 그래서 먼저 fetch 하고 읽은 판의 sha 를 기록합니다.

| 층 | 무엇 | 읽는 깊이 |
|---|---|---|
| 1 | `litdb/INDEX_DEM.md` 의 절 "MPM · 연속체" 11 편과 "접촉역학 · 소성 (DEM 이론)" 51 편. 모두 62 편 | 카드 전문 |
| 2 | 같은 인덱스의 다른 절에서 가압 · 치밀화와 닿는 카드 (아래 목록) | 카드 전문 |
| 3 | `litdb/comparison_vs_ours_DEM.md` 의 A (압밀 · porosity) · C (역학 · morphology) · D (패킹) · E (교차검증 지점) · F (아직 못 하는 것) 절 | 전문 |
| 4 | 인덱스에 기대지 않는 확인. papers 폴더 목록을 직접 뽑아 낱말로 훑기 | 제목 줄과 머리 요약 |

층 2 목록 (11-10 인덱스 기준. 읽기 전에 인덱스 줄을 보고 더하거나 뺍니다)

- SE 입도 절 19 편 전부. 특히 lee2025_heckel_argyrodite_powder_densification_nanoindentation · faka2026_particle_size_consolidation_strain_lpscl · schneider2023_particle_size_pressure_transport · bazzoun2025_dem_parameter_sensitivity_assb_cathode · bazzoun2026_dem_fem_rnm_ionic · otani2025_dem_se_dispersion_aggregation_compression · minnmann2021_jes_charge_transport_bottlenecks · minnmann2024_microstructure_porosity_visualization
- 공정 절: so2021_dem_mold_pressure_assb_coldpress · benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem · demirtas2021_mpfem_hollow_sphere_die_compaction · diener2022_roll_gap_springback_calendering · larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity · sangros2019_dem_calendering_lib_electrode · sangros2020_lib_electrode_dem_mech_elec_ionic · ngandjong2021_dem_calendering_digital_twin · lyu2025_3d_dem_drying_calendering_lib · xu2023_realistic_am_shape_cgmd_calendering · zhang2026_xct_dem_cathode_calendering_peel_calibration
- 복합양극 절: miss2026_insitu_conductivity_porosity_pressure_compaction · miss2026_pressure_tortuosity_composite_cathode_coating · so2022_dem_compaction_coated_particles_assb · nisar2024_dem_effective_electrical_conductivity_sps
- 기타 절: doux2020_stack_pressure_assb · sakuda2013_sulfide_mechanical_property · lee2024_multiphysics_dem_fem_initial_pressure_assb · kakar1967_deformation_theory_hot_pressing · deysher2022_transport_mechanical_aspects_assb_review · kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review

층 4 낱말: compaction · densif · heckel · yield · hardness · nanoindent · creep · springback · unload · relax · relative density · porosity 와 pressure · mpm · mpfem · contact dynamics · multi-contact · plastic.
인덱스가 셋이라 (INDEX · INDEX_DEM · 동결 스냅샷) 인덱스만 보면 빠집니다. 파일 목록을 직접 봅니다.

## 2. 읽는 방법

- 인덱스 한 줄이 아니라 카드 파일을 읽습니다. 정본 가지에서 그대로 꺼내 읽고, stoic 의 동결 스냅샷은 쓰지 않습니다.
- 카드가 길어서 가벼운 에이전트에 8–10 편씩 나눠 맡깁니다. 게이트가 도는 동안은 동시에 둘까지입니다.
- 에이전트에는 아래 추출 양식과 정독 질문만 줍니다. 메모의 결론은 주지 않습니다 (결론을 주면 그대로 확인해 옵니다).
- 본 세션이 표본 10 % 이상을 카드 원문과 직접 대조합니다. 메모 3.2 에 들어갈 숫자는 전부 본 세션이 카드에서 다시 읽습니다.
- 숫자와 서지는 카드에 적힌 것만 씁니다. 카드의 표지 ([카드 판독] · [카드 산술] · [미확인]) 는 그대로 옮깁니다. 검색 요약이나 기억으로 채우지 않습니다.
- 정본은 읽기만 합니다. 카드의 오류를 찾으면 고치지 말고 적어서 1저자에게 보고합니다.

추출 양식 (카드 하나에 한 줄)

| 칸 | 내용 |
|---|---|
| slug · 서지 | 카드에 적힌 그대로 |
| 방법 | DEM · MPM · FEM · 입자별 FE · 실험 · 리뷰 |
| 재료 · 차원 | 재료 이름 · 2D 인지 3D 인지 |
| 조건 | 압력 범위 · 누른 채인지 뺀 뒤인지 · 온도 |
| 준 것 | 무엇을 쟀거나 계산했나. 값은 쪽 · 그림 번호와 표지까지 |
| 계획의 자리 | 단계 0–7 · 후보 A · A′ · B · C · C′ · 단위 시험 U0–U6 · 결과 전 대조 항목 가운데 어디 |
| 한계 | 재료 · 차원 · 정의가 우리와 다른 점 |
| 메모 3.1 | 이미 썼나 (예 · 아니오) |
| 3.2 제안 | 넣을 문장이나 대조 항목 한 줄. 없으면 없음 |

정독 질문 (질문마다 근거 카드 slug 를 답니다. 카드가 없으면 "카드 없음" 이라고 적습니다)

| # | 질문 | 닿는 곳 |
|---|---|---|
| a | 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선이 있는 카드. 진밀도 값 · 질량 기준인지 · 누른 채인지 뺀 뒤인지 | 단계 4 대조 · DRD-03 |
| b | 압력을 뺄 때 되돌아오는 양과 잰 방법 | 단계 6 · U3 · U4 |
| c | 항복 · 경도 · 크리프 값과 정의. 우리 항복 세기와 견줄 환산이 되는가 | 항복 세기 대조 · SELF-160 |
| d | 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍 | 조건 R1 · DRD-11 |
| e | 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 (multi-contact · MDR · EEPA · Thornton-Ning · Storåkers). 대안마다 맞춘 값이 몇 개인가 | 후보 C · C′ · DRD-10 |
| f | MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 (지름당 셀 수). 수치 오차를 어떻게 추정했나 | 후보 A · A′ · DRD-01 |
| g | 2D 결과를 3D 로 옮길 때의 경고나 증거 | DRD-02 |
| h | DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점 (PyCompact · Demirtas · Lim 2025) | 주간보고 지적 1 |
| i | 복합 양극의 압력별 기공 | 단계 5 외부 기준 |
| j | comparison 문서 F 절의 "아직 못 하는 것" 가운데 이 재설계가 닫는 것과 그대로 남는 것 | 메모 3.2 범위 문장 |

## 3. 산출물

폴더는 docs/reviews/dem_redesign_direction_20261109/litdb_reading_20261110 로 합니다 (새 폴더).

- README.md: 읽은 정본 sha · 카드 수 · 누가 무엇을 읽었나 · 표본 대조 결과
- reading_table.tsv: 카드 하나에 한 줄 (위 양식)
- findings.md: 질문 a–j 의 답. 근거 slug · 값 · 한계
- gaps.md: 카드에 없어서 더 먹여야 하는 것. 11-10 대화의 먹일 문헌 표 (A1–A6 · B1–B6 · C1–C2) 와 합칩니다
- 메모 3.2 에는 대조 항목 등록 · 참고문헌 · 문장 고침만 넣습니다

문서에 새 경로를 백틱으로 적으면 참조 검사에 걸립니다. 파일을 만든 뒤에 적거나 허용목록에 한 줄 넣습니다.

## 4. 순서

1. 복귀 절차를 먼저 끝냅니다 (stoic fast-forward · 인계 문서의 첫 일).
2. 정본을 fetch 하고 sha 를 적습니다. 파일 목록에서 읽을 목록을 확정합니다 (층 1 은 62 편 · 층 2 는 위 목록).
3. 에이전트 정독과 본 세션 표본 대조를 합니다.
4. 산출물을 씁니다. 커밋 하나, 게이트, push 순서입니다.
5. 1저자가 새 PDF 를 주면 논문 에이전트로 정본에 카드를 만든 뒤 같은 표에 줄을 더합니다.
6. 메모 3.2 를 씁니다 (판정 처분 문서의 순서 + 이 정독 결과). 사전 공격 뒤 Codex 짧은 재확인으로 갑니다.

Rint ② 가 1 순위입니다. 이 일은 Rint 일정을 늦추지 않는 범위에서 합니다.

## 5. 하지 않는 것

- 새 시뮬레이션을 돌리지 않습니다.
- 기준 (순수 SE 10–13 % · 진밀도 1.64) · 손잡이 (항복 세기 하나) · 갈림 표를 정독 결과만으로 바꾸지 않습니다. 어긋나는 카드를 찾으면 먼저 1저자에게 보고합니다.
- 2D 숫자를 3D 로 옮기지 않습니다.
- 다른 재료의 값을 LPSCl 값처럼 쓰지 않습니다.
- DEM 과 MPM 을 서로 맞추는 데 문헌 값을 쓰지 않습니다.
- stoic 의 litdb 폴더 (동결 스냅샷) 에 쓰지 않습니다.

## 6. 끝 기준

- 층 1 의 62 편이 모두 표에 있습니다. 층 2 목록도 모두 있습니다.
- 질문 a–j 마다 답이 있습니다 (근거 slug 또는 "카드 없음").
- 표본 대조에서 어긋난 줄이 없습니다. 있으면 고치고 표본을 늘립니다.
- 메모 3.2 의 문헌 숫자가 모두 카드 slug 와 쪽 · 그림 번호를 답니다.

## 7. 1저자가 정할 것

| # | 질문 | 권고 |
|---|---|---|
| Q1 | 정독 범위를 62 편 + 관련 카드 약 40 편으로 할까요, DEM · MPM 축 251 편 전부로 할까요 | 62 편 + 관련 카드. 나머지는 층 4 로 훑어 빠진 것만 더합니다 |
| Q2 | SE 축 인덱스 (INDEX) 의 기계 물성 카드도 같이 읽을까요 | 예. 층 4 낱말에 걸린 것만 |
| Q3 | 정독을 메모 3.2 앞에 둘까요 | 예. 3.2 를 두 번 고치지 않기 위해서입니다 |

## 부록. 1저자가 찾아서 줄 문헌 (11-10 대화의 표)

서지의 권호는 정본 카드에 인쇄된 것이고 제목은 검색으로 확인한 것입니다. B 줄은 원문을 받기 전이라 확정이 아닙니다. 카드를 만들 때 원문으로 다시 확인합니다.

| # | 논문 | 쓰는 곳 |
|---|---|---|
| A1 | Cárdenas-Barrantes, Cantor, Barés, Renouf, Azéma, Three-dimensional compaction of soft granular packings, Soft Matter 18 (2022) 312–321, doi:10.1039/D1SM01241J | 입자별 유한요소 방식의 3D 비용 · 입자 수 (1 순위) |
| A2 | Cantor, Cárdenas-Barrantes, Preechawuttipong, Renouf, Azéma, Compaction Model for Highly Deformable Particle Assemblies, Phys. Rev. Lett. 124, 208003 (2020), doi:10.1103/PhysRevLett.124.208003 | 압밀 법칙의 원전 |
| A3 | Cárdenas-Barrantes, Cantor, Barés, Renouf, Azéma, Micromechanical description of the compaction of soft pentagon assemblies, Phys. Rev. E 103, 062902 (2021), doi:10.1103/PhysRevE.103.062902 | 입자 모양 · 마찰과 재배열 |
| A4 | Barés, Cárdenas-Barrantes, Cantor, Azéma, Renouf, Highly strained mixtures of bidimensional soft and rigid grains: an experimental approach from the local scale, EPJ Web Conf. 249, 05004 (2021), doi:10.1051/epjconf/202124905004 | 2022 실험판 장치의 앞 판 |
| A5 | Vu, Barés, Soft-grain compression: Beyond the jamming point, Phys. Rev. E 100, 042907 (2019) | 접촉 판정 방법 · 소성 입자 실험 |
| A6 | Phys. Rev. E 106, L022901 의 Supplemental Material | 2022 실험판 카드의 미확인 칸 |
| B1 | Hu, Fang, Ge, Qu, Zhu, Pradhana, Jiang, A Moving Least Squares Material Point Method with Displacement Discontinuity and Two-Way Rigid Body Coupling, ACM Trans. Graph. 37(4) (2018), doi:10.1145/3197517.3201293 | 우리 코드 계보의 원전 · 강체 결합 |
| B2 | Homel, Herbold, Field-gradient partitioning for fracture and frictional contact in the material point method, Int. J. Numer. Methods Eng., doi:10.1002/nme.5317 | 속도장을 입자 수만큼 늘리지 않는 접촉 |
| B3 | Nairn, Bardenhagen, Smith, Generalized contact and improved frictional heating in the material point method, Comput. Part. Mech. 5(3) (2018) 285–296, doi:10.1007/s40571-017-0168-1 | 마찰 · 점착 법칙 |
| B4 | Papakyriakou 외, Mechanical behavior of inorganic lithium-conducting solid electrolytes, J. Power Sources 516 (2021) 230672, doi:10.1016/j.jpowsour.2021.230672 | LPSCl 나노압입 · 크리프 |
| B5 | Var, Barthel, Maiza, Sicsic, Bregiroux 외, The mechanical properties of solid sulfur electrolytes: a local approach for a multiscale design, J. Power Sources 668 (2026) 239292, doi:10.1016/j.jpowsour.2026.239292 | LPSCl 입자 압입과 압력별 펠릿 |
| B6 | Doerrer 외, High Energy Density Single-Crystal NMC/Li6PS5Cl Cathodes for All-Solid-State Lithium-Metal Batteries, ACS Appl. Mater. Interfaces 13 (2021) 37809–37815, doi:10.1021/acsami.1c07952 | 복합 양극 밀도. 압력별 표가 있는지는 원문 확인 |
| C1 | 랩 자료: NCM + LPSCl 복합 펠릿의 압력별 원측정 (질량 · 면적 · 두께 · 압력 · 조성 · 누른 채인지 뺀 뒤인지) | 복합 단계의 외부 기준 |
| C2 | 랩 자료: 순수 SE 10–13 % 의 원측정이 있으면 같은 항목 | 기준값의 측정 상태 확인 |
