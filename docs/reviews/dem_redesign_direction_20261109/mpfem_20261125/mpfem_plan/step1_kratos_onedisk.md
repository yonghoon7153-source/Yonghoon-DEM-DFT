# MPFEM 1 단계 — Kratos 설치 + 원판 하나 누르기 (설계 · 개발 자료)

2026-11-25 · [DEM 우선 (수영)] · **개발 자료 · 설계 문서 · 설치 0 · 계산 0 · 리포 쓰기 0** · 실행 = 본 세션 (J26 push 뒤)

- 1저자 11-25 결정: 순서 ① 이 단계 → ② 2D 49 원판 (결과 전 등록) → ③ 3D 작은 조각.  상용 프로그램 없음.  Kratos 먼저, 안 되면 MOOSE (공부 메모 `docs/reviews/dem_redesign_direction_20261109/study_mpfem_kratos_20261125.md` §5 Q1 · Q2 = '권고대로').
- 이 단계의 답은 **개발 자료**다.  판정 문장 · 논문 숫자에 쓰지 않는다.  값을 MPM 에 맞추지 않는다 (메모 3.2 §3-2 규칙 4 · frame [4]).

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 설치 명령 (판 · 해시 고정) · 시험 기하 · 메시 둘 · 팔 · 경계 · 접촉 · 출력 · 손 검산 통과 기준 · 갈림 (MOOSE 로 가는 조건) · 시간 어림 · 입력 초안 (`step1_inputs/`) | 설치 · 실행 · 결과 · 49 원판 (2 단계) · 3D (3 단계) · 문헌 식의 원문 확인 (2D 원기둥 Hertz 로그 꼴 = 카드 없음) |

표지: **[바퀴 판독]** = PyPI 바퀴 (10.4.4) 를 내려받아 안의 Python 원문 · 형식 stub 을 읽음 (설치 · 실행 0 · 내려받은 것은 지움) · **[바이너리 문자열]** = 바퀴 안 `.so` 의 문자열에 그 이름이 있음 (등록 · 동작 증명 아님) · **[카드]** = litdb 정본 카드 · **[리포]** = 리포 문서 · 코드 · **[우리 산술]** · **[우리 유도]** · **[추정]** · **[미확인]**.

---

## 0. 한눈에

1. 묻는 것: Kratos 가 우리 문제를 푸는가.  무른 탄소성 원판 · 큰 변형 · 평면 변형 · 강체 판 접촉이다.  원판 하나로 가른다.
2. 설계 전 발견: **2D 평면 변형 + 유한 변형 J2 법칙이 10.4.4 바퀴에 없다** [바이너리 문자열].  유한 변형 J2 는 3D 와 평면 응력에만 있다.  ⇒ 주 경로 = **3D 한 층 + 모든 절점 u_z = 0** (운동학상 평면 변형과 같다).  2D 는 작은 변형 J2 만 있다 → 작은 변형 구간 교차 검산에만 쓴다.
3. J2 법칙은 `KratosConstitutiveLawsApplication` 에 있다 [바이너리 문자열].  주어진 꾸러미 목록에 없었다 → 넣는다 (+8.3 MB).
4. gmsh 4.15.2 는 PyPI 에 있다.  그러나 `libgmsh.so` 가 `libGLU.so.1` 을 요구하고 이 컨테이너에 그것이 없다 [readelf · ldconfig].  ⇒ 메시는 numpy 메셔 (같은 O-격자) 가 기본이다.  gmsh 경로도 같은 스크립트에 있다.
5. 통과 기준은 손으로 검산되는 항등식이다: 판 힘 균형 · 평균 응력 정리 · 작은 변형 탄성 기울기 · 부피 ↔ 압력 · 재료점 시험 (첫 항복 0.46111 MPa · 평탄 0.46188 MPa).
6. 시간 [추정]: 설치 5–10 분 · 계산 1–1.5 시간 · 사람 반나절–하루.

---

## 1. 설계 전에 본 것 — 바퀴 판독 (설치 · 실행 0)

| 항목 | 본 것 | 표지 |
|---|---|---|
| 꾸러미 · 판 | KratosMultiphysics · StructuralMechanics · ContactStructuralMechanics · Meshing · LinearSolvers · **ConstitutiveLaws** 모두 10.4.4 (2026-09-28) · BSD-4-Clause · Python ≥ 3.8 · manylinux_2_28 | PyPI JSON |
| 크기 | 바퀴 34.8 · 9.7 · 17.1 · 8.3 · 3.0 · 8.3 MB (합 81.2 MB) · 풀면 112.3 · 28.5 · 54.7 · 21.9 · 8.2 · 46.7 MB (합 ≈ 272 MB) | 바퀴 목록 [우리 산술] |
| 해시 | cp311 (이 컨테이너) · cp312 (WSL) 둘 다 `step1_inputs/requirements_kratos_10.4.4.txt` 에 | PyPI JSON · 내려받은 6 개 sha256 일치 |
| 시스템 의존 | Kratos `.so` 의 NEEDED = libc · libm · libstdc++ · libgomp · libz 등 기본뿐 · 이 컨테이너에 모두 있음 · glibc 2.39 ≥ 2.28 | readelf · ldconfig |
| 유한 변형 J2 | `FiniteStrainIsotropicPlasticity3DVonMisesVonMises` · `…PlaneStressVonMisesVonMises` 있음 · **`FiniteStrainIsotropicPlasticityPlaneStrain` 문자열 0 회** (법칙 · 구조 · 접촉 응용의 `.so` 여섯 개) | [바이너리 문자열] |
| 작은 변형 J2 | `SmallStrainJ2PlasticityPlaneStrain2DLaw` · `SmallStrainIsotropicPlasticityPlaneStrainVonMisesVonMises` · `SmallStrainJ2Plasticity3DLaw` 있음 | [바이너리 문자열] |
| 탄성 | `LinearElasticPlaneStrain2DLaw` · `LinearElastic3DLaw` · `HyperElastic3DLaw` · `HyperElasticPlaneStrain2DLaw` 있음 | [바이너리 문자열] · 꼴 (neo-Hookean 여부) [추정] |
| 요소 | `TotalLagrangianQ1P0MixedElement3D8N` (잠김 방지) · `UpdatedLagrangianElement3D8N` · `TotalLagrangianElement3D8N` · `SmallDisplacementBbarElement2D4N` · TL · UL 2D4N | [바이너리 문자열] |
| 접촉 조건 | mortar ALM · 벌점: 2D2N · 3D3N · 3D4N 만 (2 차 요소 면 없음) → 접촉하는 몸은 **선형 요소** | [바이너리 문자열] |
| 접촉 꼴 | `"contact_type"` = Frictionless · FrictionlessComponents · Frictional (Coulomb) · 그룹 `"0"`–`"9"` 열 개 · `"assume_master_slave"` = 종 (slave) 목록 | [바퀴 판독] `alm_contact_process.py` · `search_base_process.py` |
| 닿으면 붙임 | 접촉 `.so` 에서 Adhesion · ADHESION · Cohesive · Glued · GLUED · Tied · TIED 문자열 0 회 (MeshTying 은 10 회) · mesh tying 은 처음부터 묶는다 (`"database_step_update" : 999999999`) | [바이너리 문자열] · [바퀴 판독] `mesh_tying_process.py` |
| 풀이기 고름 | `solver_settings` 에 `contact_settings` 가 있으면 `contact_structural_mechanics_static_solver` 등으로 바뀐다 · 해석 단계 = `StructuralMechanicsAnalysis` | [바퀴 판독] `python_solvers_wrapper_structural.py` · `structural_mechanics_analysis.py` |
| 설정 키 | 고정 값 검사 (`RecursivelyValidateAndAssignDefaults`) — 모르는 키는 오류.  초안의 키는 이 기본값 목록에서만 골랐다 · `"line_search"` 는 낡은 키 → `"solving_strategy_settings"` | [바퀴 판독] `structural_mechanics_solver.py` · `auxiliary_methods_solvers.py` |
| 선형 풀이기 | `LinearSolversApplication` = sparse_lu · sparse_qr · sparse_cg · 밀집 꼴.  Pardiso · MKL 문자열 0 회 | [바이너리 문자열] |
| 명시 동역학 접촉 | `explicit_penalty_contact_process.py` · `contact_structural_mechanics_explicit_dynamic_solver.py` 있음 (3 단계 후보) | [바퀴 판독] 파일 이름 |
| 재료점 API | `KratosGlobals.HasConstitutiveLaw` · `ConstitutiveLawParameters.SetDeformationGradientF` · `CalculateMaterialResponseCauchy` · `FinalizeMaterialResponseCauchy` | [바퀴 판독] `kratos_globals.py` · stub |
| gmsh | 4.15.2 · 바퀴 40.0 MB · GPLv2+ · `libgmsh.so.4.15` NEEDED 에 `libGLU.so.1` · **이 컨테이너에 없음** (나머지 X11 계열은 있음) | PyPI JSON · readelf · ldconfig |

⇒ 위 이름은 문자열로만 봤다.  실제 등록 · 동작은 K-1 탐침 (§5) 이 먼저 확인한다.

---

## 2. 설치 (본 세션 · J26 push 뒤)

```bash
KV="<리포 밖 새 폴더>"                       # 예: 스크래치 아래 · 리포 · worktree 안 금지
python3 -m venv "$KV"
"$KV/bin/python" -m pip install --no-deps --require-hashes --no-cache-dir \
    -r step1_inputs/requirements_kratos_10.4.4.txt
"$KV/bin/python" -I -c "import KratosMultiphysics as KM; print(KM.Kernel.Version())"
du -sh "$KV"; df -h "$KV"
```

- 받는 양: Kratos 81.2 MB + numpy 16.9 MB ≈ 98 MB.  설치 뒤 ≈ 0.33 GB [추정: Kratos 풀린 크기 272 MB + numpy 40–60 MB].  `--no-cache-dir` 로 받은 사본을 남기지 않는다.  이 컨테이너 남은 자리 약 2.4 GB 안이다.
- WSL (Python 3.12.3) 도 같은 파일이다.  cp312 해시가 들어 있다.
- gmsh 는 선택이다 (`requirements_gmsh_optional.txt`).  이 컨테이너에서 쓰려면 `libglu1-mesa` 시스템 꾸러미가 필요하다 → **시스템 변경 = 1저자 결정**.  1–2 단계는 numpy 메셔로 충분하다.
- numpy 2.4.6 과 Kratos 10.4.4 의 짝은 PyPI 의존 표기 (`numpy>=1.20`) 만 봤다 [추정: 맞음].

---

## 3. 시험 설계

### 3-1. 기하 (= 등록 ① G1)

| 항목 | 값 | 근거 |
|---|---|---|
| 원판 | 지름 D = 0.1 m · R = 0.05 m · 가운데 (0, 0) | 리포 코드 단위 (D = 0.1 모형 길이) 를 m 로 읽음 · `scripts/suyoung_u6_first_dev.py` |
| 판 틈 | g_p = 0.0017272 D = 1.727 × 10⁻⁴ m (위 · 아래 각각) | 등록 ① §2 (침대 7 × 7 의 판 틈과 같다) |
| 판 | 너비 2 D · 두께 0.1 D · 강체 (판의 모든 절점 변위 지정 · 판 재료는 결과에 안 든다) | 설계 선택 |
| 끝 접근량 | u_end = 0.20 D + 2 g_p = 0.020345 m (원판 지름 변형 0.20) | 등록 ① §2 |
| 3D 한 층 | 두께 t_z = 0.005 m · 한 층 · 모든 절점 u_z = 0 · 앞뒤 면은 자유 (접촉 없음) | 이 문서 §0-2 |

### 3-2. 메시 (O-격자 · `make_disk_mesh.py`)

| 이름 | ns · nr | 원판 요소 | 절점 (한 층) | 경계 선분 | 면적 등가 지름당 | 경계 선분 / D | 다각형 면적 비 | 처짐 / D |
|---|---|---|---|---|---|---|---|---|
| **m13** | 8 · 2 | 128 | 145 | 32 | 12.8 | 0.0982 | 0.99359 | 0.00241 |
| **m26** (2 배) | 16 · 4 | 512 | 545 | 64 | 25.5 | 0.0491 | 0.99839 | 0.00060 |
| m52 (예비 · 2 단계용) | 32 · 8 | 2048 | 2113 | 128 | 51.1 | 0.0245 | 0.99960 | 0.00015 |

- 면적 등가 지름당 = √(요소 수 / (π/4)) [우리 산술].  같은 잣대로 Zhou 2019 = 132 요소 = 13.0 · Huang 2017 = 1200 요소 = 39 · Li 2022 (3D) = 1014 요소 = 12.5 [카드: `zhou2019_mpfem_2d_copper_powder_die_compaction_release` §3-1 · `huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction` §3-1 · `li2022_mpfem_3d_soft_hard_composite_compaction_vibration_unloading` §3-1].  m13 은 Zhou 와 요소 수 자릿수가 같다 (128 ↔ 132 · 절점 145 ↔ 169).
- 안쪽 정사각 반변 = 0.6 R (`--alpha 0.6`).  경계에서 둘레 · 반지름 요소 길이가 비슷하다 (m13 0.098 D · 0.1 D).  정사각 모서리 앞 요소는 얇다 (m13 반지름 0.038 D) [우리 산술].
- 반지름: 1 단계 = `exact` (경계 절점이 원 위 · θ 90° · 270° 에 절점 → 위 · 아래 첫 접촉 점이 정확).  다각형 면적 부족 0.64 % (m13) · 0.16 % (m26) 는 P2 · P4 가 실제 FE 면적을 쓰므로 판정에 안 든다.  2 단계는 `area` (Φ_m 이 ΣA₀ 와 맞게).
- ⚠ 판 틈 0.00173 D 는 m13 처짐 0.00241 D 보다 작다.  접촉 폭이 자라는 모양은 다각형 꼴이다 → 첫 힘 변위는 메시마다 다를 수 있다.  보고만 한다.

### 3-3. 팔 (재료 · 요소)

| 팔 | 차원 · 요소 | 법칙 (재료 파일) | 끝 | 쓰임 |
|---|---|---|---|---|
| **A3-J2** (주) | 3D 한 층 · `TotalLagrangianQ1P0MixedElement3D8N` (안 되면 `UpdatedLagrangianElement3D8N` · 잠김 표지) | `FiniteStrainIsotropicPlasticity3DVonMisesVonMises` · 완전 소성 (`StructuralMaterials_A3_J2.json`) | u_end (ε 0.20) | 주 결과 · P1 · P2 · P4 |
| A3-E | 같음 | `HyperElastic3DLaw` (`StructuralMaterials_A3_elastic.json`) | u_end | 큰 변형 탄성 보고 (P7) |
| B2-J2 | 2D · `SmallDisplacementBbarElement2D4N` | `SmallStrainJ2PlasticityPlaneStrain2DLaw` (`StructuralMaterials_B2_J2.json`) | ε 0.02 (47 걸음) | 작은 변형 교차 검산: A3-J2 와 ε ≤ 0.01 에서 같은가 (보고) |
| B2-E | 같음 | `LinearElasticPlaneStrain2DLaw` (`StructuralMaterials_B2_elastic.json`) | ε 0.02 | **P3** (정확 항등식) |
| A3-J2-dyn (리허설) | A3 와 같음 · Bossak 암시 동역학 | A3-J2 | u_end · V0 와 V0/4 | 2 단계 풀이기 시험 (P8 · 보고) |

- 재료: E 10 MPa · ν 0.45 · σ_y 0.4 MPa (단축) · 경화 0 [리포: `docs/reviews/suyoung_u6_first_development_20261118/README.md`] · ρ 1000 kg/m³ [카드: `nezamabadi2022_mpm_cd_plastic_particle_compaction` §3.1 · MPM 은 ρ = 1 무차원 → 같은 무차원 수].  판 = 탄성 E 10 GPa (모든 절점 구속이라 결과 무관).
- 유한 변형 J2 변수 `YIELD_STRESS` (+ `_TENSION` · `_COMPRESSION` 같은 값) · `HARDENING_CURVE` 3 (= 완전 소성으로 읽음 [추정 · 기억 · 원문 미열람]) · `FRACTURE_ENERGY` 1e10 (완전 소성이면 안 쓰일 것 [추정]).  작은 변형 J2 변수 `ISOTROPIC_HARDENING_MODULUS` 0 · `EXPONENTIAL_SATURATION_YIELD_STRESS` = σ_y · `HARDENING_EXPONENT` 1 [추정].  K-2 의 `Check()` 오류 문구로 고친다.
- ⚠ **재료식 꼴이 MPM 과 다르다.**  MPM 2D = fixed-corotated 응력 + 면내 두 로그 주변형률의 편차로 하는 반환 [리포 코드 판독: `scripts/dem_suyoung_sf2d_dev.py` `stress()` · `plastic_project()`].  Kratos = 3D von Mises (σ_zz 포함) · 탄성 꼴 · 반환 꼴 [미확인].
  - 단축 평면 변형 (σ_xx = 0) 첫 항복: Kratos J2 0.46111 MPa ↔ MPM 2D 0.46188 MPa → 0.17 % [우리 산술 · 작은 탄성 변형].
  - 면내 평균 압력 m 이 있으면 J2 의 항복 편차가 √(1 − (1−2ν)² m²/σ_y²) 배로 준다: m = σ_y 에서 0.5 % · m = 3σ_y (1.2 MPa) 에서 4.6 % [우리 산술 · 탄성 σ_zz = ν(σ_xx+σ_yy) 가정 · 소성 흐름이 자라면 0 쪽].
  - 그래서 49 원판의 FE ↔ MPM 차이에서 재료식 몫을 떼려면 이 단계의 원판 하나 대조 (등록 ① G1 의 MPM 판이 나오면 나란히) 가 먼저다.

### 3-4. 경계 · 접촉 · 풀이

| 항목 | 정적 대칭 (A3-J2 · A3-E · B2-*) | 동적 리허설 (A3-J2-dyn) |
|---|---|---|
| 판 운동 | 두 판이 걸음마다 Δu/2 씩 가운데로 · Δu = 0.0005 D = 5 × 10⁻⁵ m · 407 걸음 (B2 = 47 걸음) | 아래판 고정 · 위판 V0 = 0.034 c_S = 1.997 m/s · Δt 2.5 × 10⁻⁵ s (걸음당 5 × 10⁻⁵ m) · 408 걸음 · V0/4 = Δt 10⁻⁴ s · 408 걸음 |
| 강체 모드 | x = 0 줄 절점 u_x = 0 · y = 0 줄 u_y = 0 (대칭 해일 때만 같은 답) | 구속 없음 (질량이 막는다) |
| 3D | 모든 절점 u_z = 0 | 같음 |
| 접촉 | mortar ALM · 마찰 없음 · 그룹 "0" = `DiskSurface` (종) + `PlateSurfaces` (주) · `in_radius_with_obb` · search_factor 3.5 | 같음 |
| 수렴 | `contact_residual_criterion` · 상대 10⁻⁶ · 최대 30 회 · `sparse_lu` | 같음 · Bossak α_m −0.3 (기본값) |

- 파속 (ρ 1000): c_S = 58.72 m/s · c_P = 194.76 m/s · V0/c_P = 0.01025 = 등록 ① §2 와 같다 [우리 산술].  NZ22 집합체 판 속도 2 m/s (V/c_S 0.034) 와도 같다 [카드].
- 정적 = 준정적 극한 (관성 0).  MPM 은 명시 동역학 V0 다.  그래서 동적 리허설을 같이 둔다.

### 3-5. 출력 (`run_onedisk.py`)

- `trace.csv` (걸음마다): 수렴 · 뉴턴 횟수 · 판 변위 · 접근량 · 판 사이 높이 h · 위 · 아래 판 힘 (두께당) · σ_b = |아래 힘| / D (등록 ① 판독) · 원판 면적 · 평균 Cauchy 응력 (xx · yy · zz · xy) · 경계 적분 평균 변형률 (xx · yy · xy) · 활성 종 절점 수.
- `summary.json`: 입력 sha256 (변수 · 메시 · 재료 · 드라이버) · 판 · 시간 · §4 검산값과 통과 여부.
- VTK: 20 걸음마다 변위 · 반력 · 적분점 Cauchy 응력.

---

## 4. 통과 기준 — 결과 전 · 손 검산

| 기호 | 무엇 | 식 · 목표값 | 허용 (지위) | 근거 | 팔 |
|---|---|---|---|---|---|
| C | 모든 걸음 수렴 ∧ 끝 시간 도달 | — | 필수 | — | 전부 |
| P1 | 판 힘 균형 | \|F_top − F_bot\| / F ≤ | 10⁻³ (개발 정책값 · 수렴 허용 10⁻⁶ 에 여유) | 정적 평형 | 정적 팔 |
| P2 | 평균 응력 정리 | ⟨σ_yy⟩ = −F h / A · ⟨σ_xx⟩ = 0 | 각 10⁻² (개발 정책값) | 평형 · 관성 0 · 마찰 없는 판 (옆 견인력 0) 이면 재료 · 변형 크기와 무관하게 정확 [우리 유도 · 평균 응력 정리] | 정적 팔 |
| P3 | 작은 변형 탄성 | ⟨σ_yy⟩/⟨ε_yy⟩ = E/(1−ν²) = 12.539 MPa · ⟨ε_xx⟩/⟨ε_yy⟩ = −ν/(1−ν) = −0.8182 | 10⁻² · 2 × 10⁻² (개발 정책값) | 균일 선형 탄성체는 평균에서 정확히 Hooke 를 따른다 (평균 변형률 = 경계 적분) [우리 유도] · NZ22 단일 원판 탄성 기울기 ≈ 12.6 MPa ≈ 12.54 MPa 해석과 같은 꼴 [카드: `nezamabadi2022_mpm_cd_plastic_particle_compaction` §5.1 · 판독값] | B2-E |
| P4 | 부피 ↔ 압력 | \|ΔA/A₀ − ⟨tr σ⟩/(3K)\| ≤ · K = E/(3(1−2ν)) = 33.33 MPa | 10⁻³ (탄성 부피 변형 ≈ 1.5 % 의 7 % · 개발 정책값) | 소성 흐름은 비압축 · 부피는 탄성으로만 [우리 유도 · 작은 탄성 변형] | A3-J2 |
| P5 | 재료점 (`probe_kratos.py`) | 기울기 12.539 MPa · 첫 항복 \|σ_yy\| = σ_y/√(1−ν+ν²) = 0.46111 MPa · 평탄 2σ_y/√3 = 0.46188 MPa (ly 0.85 · 2D 는 ε_yy −0.15) · 30° 회전 객관성 | 기울기 0.5 % · 첫 항복 1 % (3D) / 0.5 % (2D) · 평탄 2 % (3D) / 0.5 % (2D) · 회전 차 ≤ 10⁻⁶ σ_y (개발 정책값) | [우리 산술] | 법칙 둘 |
| P6 | 메시 (보고) | m13 ↔ m26 의 σ_b(u) 차 = 등록 ① §4-1 식 (공통 구간 · 합집합 표본 · 분자 = 최대 차 · 분모 = 고운 쪽 최대) | 보고 (원판 하나라 판정 아님) | [리포] `docs/reviews/suyoung_u6c_force_rule_20261122/rule.json` | A3-J2 |
| P7 | 문헌 (보고) | NG17 직선 Hertz F = (π/4)E/(1−ν²)Rε (σ_b 기울기 4.924 MPa) 대비 비 · ε = 0.01 · 0.02 · 0.04 · NZ22 단일 원판 꺾임 ≈ 0.40–0.42 MPa @ ε ≈ 0.035–0.04 · 꺾인 뒤 기울기 ≈ 0.7 MPa (H0) | 보고 · 범주만 | [카드: `nguyen2017_mpm_bpm_deformable_particle_compaction` §4.3 — 직선 근사 · 교과서 로그 꼴은 카드 없음 [미확인]] · [카드: NZ22 §5.1 — 판독값 · σ · ε 정의 미기재] | A3-E · B2-E · A3-J2 |
| P8 | 리허설 (보고) | V0 ↔ V0/4 의 σ_b(u) 차 · 위 · 아래 힘 차 (관성) · 원판 중심 x 어긋남 | 보고 | — | A3-J2-dyn |

- P2 는 이 단계의 핵심 결속이다.  판 반력 (판독) 과 원판 안 응력 (해) 이 같은 숫자를 내야 한다.  접촉 힘 판독 · 응력 적분 · 면적 셈이 한 번에 묶인다.
- P3 는 B2-E 에서만 정확하다 (작은 변형 · 선형).  유한 변형 팔에는 쓰지 않는다.
- 모든 허용은 **개발 정책값**이다.  결과를 본 뒤 바꾸지 않는다.

---

## 5. 진행 순서 · 갈림 (결과 전 고정)

| 단계 | 하는 일 | 통과 | 실패면 |
|---|---|---|---|
| K-0 | 설치 (§2) | import 다섯 · `Kernel.Version()` | 오류 기록 → 1저자 |
| K-1 | `probe_kratos.py` — 법칙 · 요소 · 조건 이름 | `FiniteStrainIsotropicPlasticity3DVonMisesVonMises` 등록 ∧ 3D8N 요소 하나 이상 ∧ `SurfaceCondition3D4N` | 3D 유한 변형 J2 없음 → **MOOSE** (B2 만 돌려 2D 접촉을 보고) |
| K-2 | 재료점 P5 | P5a–d | 변수 고침 2 회 (Check 문구 · `HARDENING_CURVE` · 항복 변수 꼴) → 그래도 실패면 **MOOSE** |
| K-3 | 원판 하나 정적 · A3-J2 (m13 · m26) · A3-E · B2-J2 · B2-E | C · P1 · P2 · P4 (A3-J2 두 메시) · P3 (B2-E) | 고침 순서 고정: ① Δu 반 ② 벌점 접촉 (`PenaltyContactFrictionless` · `penalty_contact_process`) ③ 요소 UL 3D8N ④ 그래도 안 되면 **MOOSE** |
| K-4 | 동적 리허설 (보고) | C | 2 단계 풀이기를 정적 + 안정화로 다시 설계 (1저자) |

- **MOOSE 로 가는 조건 (사전 고정)**: A3-J2 가 ε 0.20 까지 C · P1 · P2 · P4 를 두 메시에서 통과하지 못하면.  1저자 Q2 의 "큰 변형 평면 변형 소성이 안 되면 MOOSE" 를 숫자로 적은 것이다.
- 통과하면 2 단계 등록 초안 (`step2_registration_draft.md`) 을 1저자에게 올린다.
- 자동 재실행 0.  고침은 위 순서대로만 · 고친 것은 `summary.json` 옆에 한 줄씩 적는다.

---

## 6. 시간 · 자리 어림 [추정]

| 단계 | 어림 | 근거 |
|---|---|---|
| K-0 설치 | 받기 ≈ 98 MB · 5–10 분 · 자리 ≈ 0.33 GB | §1 크기 [우리 산술] |
| K-1 · K-2 | 1 분 안 | 재료점 600 걸음 × 몇 번의 법칙 호출 |
| K-3 | 팔당 407 걸음 × 뉴턴 2–8 회 · 요소 128–512 → 1–10 분/팔 · 팔 5 개 (A3-J2 × 2 메시 · A3-E · B2 × 2) → 1 시간 안 | 미측정 |
| K-4 | 408 걸음 × 2 속도 (m13) → 30 분 안 | 미측정 |
| 사람 | 입력 고침 포함 반나절–하루 | — |

- 기계: 이 컨테이너 (코어 4 · 메모리 15 GB) 로 충분하다.  `OMP_NUM_THREADS=2`.
- 2 단계 시간은 K-4 의 걸음당 시간을 재어 다시 어림한다 (`step2_registration_draft.md` §9).

---

## 7. 한정 · 확인 못 한 것

- 법칙 · 요소 이름은 문자열로만 봤다.  등록 이름 ↔ 클래스 (예: `HyperElastic3DLaw` = neo-Hookean) 는 [추정].  K-1 이 확인한다.
- Q1P0 요소가 유한 변형 소성 법칙과 맞는지 [미확인].  안 되면 UL 3D8N 이고, 그 경우 ν 0.45 + 비압축 소성에서 **부피 잠김**이 생길 수 있다 → m13 ↔ m26 차가 크면 잠김 후보로 표지.
- 유한 변형 J2 의 탄성 꼴 · 응력 척도 (Kirchhoff · 로그 변형률 여부) [미확인].  P5 가 단축 경로 · 객관성까지만 본다.
- 접촉 법선: 메셔는 반시계 순서 (바깥 법선 (dy, −dx)) 로 쓴다.  Kratos 는 `NormalCheckProcess` 로 검사한다 [바퀴 판독 · 동작 미확인].  드라이버는 원판 중심 기준으로 법선을 다시 맞춘다.
- `REACTION` 부호 관례 [미확인] → 드라이버는 크기로 쓴다.  `INTEGRATION_WEIGHT` 를 요소가 주는지 [미확인] → 없으면 등분 가중 (평행사변형이 아닌 요소에서 작은 오차 [추정]).
- 3D 한 층 + u_z = 0 은 평면 변형과 운동학이 같다.  그러나 3D 면 대 면 mortar 적분은 2D 선분 대 선분과 다르다 → A3 ↔ B2 를 ε ≤ 0.01 에서 견준다 (보고).
- 2D 원기둥 Hertz 의 로그 꼴 · 탄소성 첫 항복 하중은 정본 카드가 없다 [미확인] → 판정에 안 쓴다 (등록 ① §4-3 과 같다).
- 내려받은 바퀴는 읽은 뒤 지웠다.  설치 때 다시 받는다 (해시 고정).

---

## 8. 입력 파일 (`step1_inputs/` · 실행 0 · 구문 검사만)

| 파일 | 하는 일 |
|---|---|
| `requirements_kratos_10.4.4.txt` | Kratos 6 꾸러미 + numpy · 판 · sha256 고정 (cp311 · cp312) |
| `requirements_gmsh_optional.txt` | gmsh 4.15.2 (선택 · libGLU 필요) |
| `make_disk_mesh.py` | G1 메시 (O-격자 원판 + 판 둘) → `.mdpa` + `.mesh.json` (2D · 3D 한 층 · numpy / gmsh) |
| `probe_kratos.py` | K-1 · K-2: import · 법칙 · 요소 · 조건 · 재료점 P5 → `probe_report.json` |
| `run_onedisk.py` | K-3 · K-4: 해석 + `trace.csv` + `summary.json` (C · P1–P4) |
| `ProjectParameters_A3_static.json` | 3D 한 층 · 정적 대칭 · ALM 마찰 없음 · 407 걸음 |
| `ProjectParameters_B2_static.json` | 2D · 정적 대칭 · 47 걸음 |
| `ProjectParameters_A3_dyn_V0.json` · `…_V0q.json` | 3D 한 층 · Bossak · 위판 V0 · V0/4 |
| `StructuralMaterials_{A3_J2, A3_elastic, B2_J2, B2_elastic}.json` | 원판 법칙 + 판 탄성 |

```bash
# 본 세션 · 리포 밖 작업 폴더에 step1_inputs 사본을 두고
PY="$KV/bin/python"; export OMP_NUM_THREADS=2
$PY -I probe_kratos.py --out probe_report.json                                   # K-1 · K-2
for m in "8 2 m13" "16 4 m26"; do set -- $m
  $PY -I make_disk_mesh.py --dim 3 --ns $1 --nr $2 --out disk_A3_$3
  $PY -I make_disk_mesh.py --dim 2 --ns $1 --nr $2 --out disk_B2_$3
  $PY -I run_onedisk.py --params ProjectParameters_A3_static.json --mdpa disk_A3_$3 \
      --materials StructuralMaterials_A3_J2.json --out run_A3J2_$3 --arm A3J2_$3
done
$PY -I run_onedisk.py --params ProjectParameters_A3_static.json --mdpa disk_A3_m13 \
    --materials StructuralMaterials_A3_elastic.json --out run_A3E_m13 --arm A3E_m13
for m in m13 m26; do
  $PY -I run_onedisk.py --params ProjectParameters_B2_static.json --mdpa disk_B2_$m \
      --materials StructuralMaterials_B2_elastic.json --out run_B2E_$m --arm B2E_$m --elastic-small-strain
done
$PY -I run_onedisk.py --params ProjectParameters_B2_static.json --mdpa disk_B2_m13 \
    --materials StructuralMaterials_B2_J2.json --out run_B2J2_m13 --arm B2J2_m13
for v in V0 V0q; do                                                              # K-4 (보고)
  $PY -I run_onedisk.py --params ProjectParameters_A3_dyn_$v.json --mdpa disk_A3_m13 \
      --materials StructuralMaterials_A3_J2.json --out run_A3J2dyn_${v}_m13 --arm A3J2dyn_${v}_m13
done
```

- UL 대체: `make_disk_mesh.py … --element-disk UpdatedLagrangianElement3D8N --out disk_A3UL_m13`.
- 결과 묶음 (본 세션): `probe_report.json` · 각 `run_*/summary.json` · `trace.csv` · 화면 기록 · sha256.  VTK 는 크기를 본 뒤 정한다.
