# MPFEM 1 단계 — MOOSE 입력 블록 (원판 하나 · 2D 평면 변형 · 판 접촉) (2026-11-25 · 개발 자료)

[DEM 우선 (수영)] · **개발 자료 · 판정 미사용 · 결과 0 건** · 만든 곳 = 서브 세션 조수 (1저자 11-25 *"권고대로"* · 11-26 *"권고대로해"*) · 바탕 = `../README.md` 의 결정 줄 (Kratos 탈락 · MOOSE 주 경로 · 다음 = 이 블록).
⚠ **MOOSE 입력 (`step1_disk.i`) 은 한 번도 돌지 않았다** — 이 컨테이너에 MOOSE 가 없다.  1저자 WSL 의 첫 스모크 전까지 **미검증**이다.  이 컨테이너에서 확인한 것은 메시 · 검사기 · 블록 · 실행기 (가짜 MOOSE) 뿐이다.

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 1 단계 설계 (`../mpfem_plan/step1_kratos_onedisk.md` A3-J2 팔) 를 MOOSE 로 옮긴 입력 · 메시 · 검사기 (C · P1 · P2 · P4 · P6 보고) · WSL 붙여넣기 블록 · 이 컨테이너에서 가능한 시험 | MOOSE 실행 · 결과 · 판정 · 나머지 팔 (A3-E · B2 · 동적 리허설 · P3 · P5 · P7 · P8) · 2 단계 (우리 σy → MOOSE von Mises 환산 규칙 = 2 단계 등록 때) |

## 무엇

지름 0.1 m 원판 하나를 강체 판 두 장이 위 · 아래에서 마찰 없이 누른다.  2D 평면 변형 · 유한 변형 J2 (완전 소성) · 메시 m13 · m26.  판은 걸음마다 각각 2.5 × 10⁻⁵ m 씩 다가오고 407 걸음 (지름 변형 0.20 + 판 틈 2 개) 이다.  검사는 결과 전에 고정된 항등식 넷 (C · P1 · P2 · P4) 이다 — 숫자 · 허용폭은 Kratos 설계 그대로다.

## 파일

| 파일 | 하는 일 |
|---|---|
| `step1_disk.i` | MOOSE 입력 (주 경로 · 접촉 = node-face kinematic) |
| `make_disk_msh.py` | 메시 m13 · m26 → Gmsh MSH 2.2 ASCII + `.mesh.json` (표준 라이브러리 · 설계 메셔의 2D 이식 · 절점 비트 같음 = 시험) |
| `check_step1.py` | 검사기 (표준 라이브러리) — C · P1 · P2 · P4 판정 + P6 보고 → 화면 + JSON |
| `run_step1.sh` | WSL 실행기 — 메시 → 스모크 (m13 · 12 걸음) → m13 → m26 → 검사 → 작은 묶음 |
| `build_block.py` | 위 넷으로 `moose_step1_block.txt` 생성 (md5 관문) |
| `moose_step1_block.txt` | **1저자가 붙여넣는 블록** (`../moose_wsl/moose_wsl_block.txt` 와 같은 꼴) |
| `tests/` | 이 컨테이너 시험 (`test_check_step1.py` · `test_mesh_port.py` · `test_block.py` · `mutate_check.py` · 시험용 가짜 `fake_moose.py` · `synthetic.py`) |

## Kratos 설계 → MOOSE (옮긴 것 · 바꾼 것)

| 설계 항목 (step1 문서) | Kratos (A3-J2) | MOOSE (이 폴더) | 메모 |
|---|---|---|---|
| 기하 | D 0.1 m · 판 틈 0.0017272 D · 판 2 D × 0.1 D | 같음 | `make_disk_msh.py` |
| 메시 m13 · m26 | O-격자 ns·nr 8·2 / 16·4 · α 0.6 · 반지름 exact | 같은 절점 (비트 같음) · 같은 사각형 · 같은 경계 선분 | 시험 `t_same_ogrid_as_design_mesher` |
| 차원 | 3D 한 층 + u_z = 0 (10.4.4 에 2D 유한 변형 평면 변형 J2 가 없어서) | 2D 평면 변형 (변위 둘 → F_zz = 1) | 1저자 11-25 결정 "2D 평면 변형" |
| 요소 | `TotalLagrangianQ1P0MixedElement3D8N` (잠김 방지) | QUAD4 + `volumetric_locking_correction = true` (평균 팽창 = Q1P0 꼴) | MOOSE 는 2D 에서도 F 전체를 세제곱근으로 고친다 → 요소 안 면 밖 변형률이 조금 생긴다 [소스 판독] |
| 재료 | 유한 변형 J2 von Mises · E 10 MPa · ν 0.45 · σy 0.4 MPa · 경화 0 | `ComputeFiniteStrain` + `IsotropicPlasticityStressUpdate` (hardening 0) + `ComputeMultipleInelasticStress` · 같은 수 | 회전 시험 (`../moose_wsl/rot_test.i`) 과 같은 객체 |
| 판 | 탄성 10 GPa · 모든 절점 변위 지정 | 같음 (nodeset 22 · 32 전부 Dirichlet) | 판 요소의 커널 · 재료는 범위 검사 (kernel coverage) 용 |
| 하중 | 판마다 걸음당 Δu/2 = 2.5 × 10⁻⁵ m · 407 걸음 | `FunctionDirichletBC` ∓2.5 × 10⁻⁵ t · dt 1 · end 407 | |
| 강체 모드 | x = 0 줄 u_x = 0 · y = 0 줄 u_y = 0 | 같음 (nodeset 41 · 42) | |
| **접촉** | **mortar ALM · 마찰 없음** (종 = 원판 · 주 = 판) | **node-face kinematic · 마찰 없음** (secondary = 원판 위 · 아래 반쪽, primary = 판 면) | ★ **바꾼 곳** — 아래 Q1 |
| 수렴 | Newton · 상대 10⁻⁶ · 최대 30 회 · sparse_lu | PJFNK (Newton · 행렬 없는 정확한 방향 미분) · LU 전처리 · `nl_rel_tol 1e-6` · `nl_max_its 30` · 선 탐색 없음 | MOOSE 의 유한 변형 조립 Jacobian 이 근사라 PJFNK |
| 절대 허용 | 잔차 10⁻⁹ N (두께 0.005 m 판) | `nl_abs_tol 2e-7` N/m (두께당 같은 값) | 첫 6 걸음 (접촉 전 · 잔차 0) 에서만 쓰인다 |
| 걸음 | 고정 · 자동 자르기 없음 | `abort_on_solve_fail` · `dtmin = dt` | 못 풀면 그 자리에서 멈춘다 (C 실패) |
| 판 힘 | 판 절점 REACTION_Y 합 ÷ 두께 | 원판 경계 절점 (y > 0 / y < 0) 의 내력 (`save_in`) 합 | kinematic 은 원판 절점의 법선 내력을 그대로 판으로 넘긴다 → 같은 양 [소스 판독] |
| 판 사이 높이 h | h0 + u_top − u_bot | 같음 (판 면 절점 평균 변위) | |
| 평균 응력 ⟨σ⟩ | Σ (현재 요소 면적 × 적분점 평균 σ) ÷ 면적 | 요소 평균 σ (`RankTwoAux`, 기준 가중) 을 현재 메시에서 적분 ÷ 현재 면적 | 같은 추정자 · 정확한 적분점 합과의 차 = 요소 안 J 와 σ 의 공분산 (어림 ≲ 10⁻³) |
| A0 | 메시 다각형 면적 | 같음 (MOOSE 기준 면적과 10⁻⁹ 안 = 입력 무결성 검사) | |

## 검사 (결과 전 고정 · 숫자 그대로)

판독 행 = `|F_bot|` ≥ 최대 `|F_bot|` 의 1 % 인 걸음 (`../mpfem_plan/step1_inputs/run_onedisk.py` 와 같다).  힘은 두께당 (N/m).

| 기호 | 식 | 허용 | MOOSE 출력 (CSV 열) |
|---|---|---|---|
| C | 모든 걸음 수렴 (종료 코드 0 · 로그에 실패 줄 없음 · 걸음 dt, 2dt, … 빈틈 없음) ∧ 끝 시간 도달 | 필수 | `time` · `nl_its` · `rc.txt` · `run.log` |
| P1 | \|\|F_top\| − \|F_bot\|\| / max | 10⁻³ | `F_top_y` · `F_bot_y` |
| P2 | \|⟨σ_yy⟩ + \|F_bot\| h / A\| ÷ (\|F_bot\| h / A) · \|⟨σ_xx⟩\| / \|⟨σ_yy⟩\| | 각 10⁻² | `int_syy` · `int_sxx` · `area` · `u_top` · `u_bot` |
| P4 | \|(A/A0 − 1) − ⟨σ_xx + σ_yy + σ_zz⟩ / (3K)\| · K = E / (3(1 − 2ν)) = 33.33 MPa | 10⁻³ | `area` · `int_szz` (+ 위) |
| P6 | m13 ↔ m26 σ_b(u) = \|F_bot\| / D · 규칙 U6c-06 꼴 (공통 구간 · 합집합 표본 · 최대 차 ÷ 고운 쪽 최대) | **보고만** | 위 |

보고만 (판정 아님): 최대 σ_b · 끝 접근량 · 판 x 힘 비 · y = 0 줄 반력 비 · Newton 반복 수 · 최대 von Mises / σy.

## 1저자 WSL 에서

1. `moose_step1_block.txt` **전체**를 WSL 터미널에 붙여넣는다 (11-25 회전 시험 블록과 같은 방법).  파일이 WSL 에 있으면 `bash moose_step1_block.txt` 도 같다.
2. 블록이 하는 일 (네트워크 0): 파일 넷을 `~/moose_step1/` 에 쓴다 → **md5 관문** (한 글자라도 다르면 `⛔ … 아무것도 안 함`) → `bash run_step1.sh`: `conda activate moose` → 새 폴더 `~/moose_step1/run_<날짜>_none_XXXX` → 메시 둘 → **스모크** (m13 · 12 걸음 · 첫 접촉 = 7 걸음; 거부 · 실패면 오류 줄과 로그 끝 40 줄을 보이고 멈춘다) → m13 407 걸음 → m26 407 걸음 → 검사 → 묶음.
3. 돌려보낼 것: **화면 전체** + `<run 폴더>/result_small.tgz` (CSV · 로그 · JSON · 입력 해시 · `.e` 와 `.msh` 뺌).  볼 그림이 필요하면 `m13/out.e` · `m26/out.e` (ParaView).
4. 시간 [추정]: 2D 작은 메시라 m13 · m26 각각 수 분 [미측정].  시간 상한 = 스모크 15 분 · 본 런 각 4 시간 (넘으면 종료 코드 124 → C 실패).

### 고침 순서 (결과 전 고정 · 설계 K-3 을 옮김 · 손으로만 · 한 번에 하나 · 자동 재실행 0)

| 순서 | 무엇 | 명령 |
|---|---|---|
| ① | 걸음 반 (dt 0.5 · 814 걸음 · 같은 판 속도) | `FIX=dt_half bash ~/moose_step1/run_step1.sh` |
| ② | 접촉 꼴 바꾸기 (예: mortar) | 세션이 새 입력을 만든다 (스위치 아님) |
| ③ | 잠김 방지 끔 (보통 QUAD4) | `FIX=no_vlc bash ~/moose_step1/run_step1.sh` |
| ④ | 그래도 안 되면 | 1저자에게 보고 (다음 도구 결정) |

각 실행은 새 폴더를 만들고 `run_info.txt` 에 `fix=` 를 남긴다.  어느 고침을 왜 했는지는 그 폴더 옆에 한 줄씩 적는다 (설계 §5 와 같다).

## 시험 (이 컨테이너 · MOOSE 없이 · 시험 먼저)

| 시험 | 고치기 전 | 뒤 | 무엇을 보나 |
|---|---|---|---|
| `tests/test_check_step1.py` | 0 / 26 | 26 / 26 | 검사마다 통과 · 실패 경우 (허용 바로 아래 · 위 · 1 % 경계 포함 · NaN · 열 빠짐 · 접촉 없음 · 종료 코드 · 로그 · 걸음 빈틈 · dt 0.5 · P6 값) |
| `tests/test_mesh_port.py` | 0 / 4 | 4 / 4 | 설계 메셔 (`../mpfem_plan/step1_inputs/make_disk_mesh.py --dim 2`, numpy) 와 절점 비트 같음 · 사각형 · 경계 · SymX/SymY · 통계 · 태그 · 변이 면 소속 · 반시계 |
| `tests/test_block.py` | 0 / 10 → 추가 2 (0 / 2) | 12 / 12 | 왕복 (풀어낸 파일 = 원본 바이트) · 글자 하나 바꾸면 관문 닫힘 (입력 · 검사기 · md5 줄) · 스모크 거부 → 멈춤 · 발산 → C 실패 · FIX 수동 · conda 없음 → STOP · 네트워크 · 개인 문자열 없음 · 붙여넣기 위험 문자 없음 |
| `tests/mutate_check.py` (검사기 규칙 하나씩 깨기 · 사본에서) | — | 10 / 10 잡힘 | 1 % 경계 · P1 허용 · 로그 · 빈틈 · P2 부호 · P2 x · P4 · 종료 코드 · A0 무결성 · NOT_COMPUTED |
| 대화형 붙여넣기 (가상 터미널의 bash 5.2 에 블록을 글자로 입력) | — | 파일 넷 바이트 같음 · 관문 통과 | |

- 시험 도중 고친 것 (시험 쪽 결함): 접촉 없음 자료에 2 차 힘 항이 남아 있었다 · `run_*` 글롭이 `run_step1.sh` 도 잡았다 (블록 시험 도우미 · 거부 시험이 엉뚱한 이유로 통과 → 고침).
- 고친 것 (산출물): 대화형 bash 는 `!` 뒤 글자를 기록 확장한다.  bash 5.2 는 heredoc 본문에는 하지 않았지만 (대조 시험) 판마다 다를 수 있어, 첫 줄 `#!` 를 지우고 빌더가 `!` 위험 · TAB 을 거부한다.
- 다시 돌리기: `python3 tests/test_check_step1.py` · `python3 tests/test_mesh_port.py` · `python3 tests/test_block.py` · `python3 tests/mutate_check.py` (블록이 낡으면 `t_committed_block_is_current` 실패 → `python3 build_block.py`).  게이트 (`scripts/check_all.sh`) 에는 아직 안 묶였다 (폴더 밖 파일이라 손대지 않음).

## 확인 못 한 것 — 기댄 MOOSE 기능과 확신

근거 = 공개 MOOSE · libMesh 소스 (11-25 master 판독) 와 MOOSE 자체 시험 입력.  WSL 의 conda 판은 더 오래됐을 수 있다 [미확인].

| 기능 | 쓴 곳 | 확신 | 근거 |
|---|---|---|---|
| `FileMeshGenerator` 로 Gmsh MSH 2.2 읽기 (사각형 tag → block · 선 → sideset · 점 (type 15) → nodeset · 숫자 id) | 메시 | 높음 | libMesh `gmsh_io.C` · 경로에 `.e` 가 들어가면 Exodus 로 읽는다 → 실행기는 상대 경로 `disk.msh` 만 쓴다 |
| `StressDivergenceTensors` (`use_displaced_mesh`) · `ComputeFiniteStrain` · `IsotropicPlasticityStressUpdate` · `ComputeMultipleInelasticStress` | 운동 · 재료 | 높음 | 회전 시험에서 같은 객체가 돌았다 (3D) · 2D 변위 둘 = 평면 변형 |
| `volumetric_locking_correction` (GlobalParams) 2D | 잠김 방지 | 중-높음 | MOOSE 2D Hertz 시험이 같은 줄 · 2D 세제곱근 꼴 (위 표) |
| `[Contact]` 두 블록 · `formulation = kinematic` · 숫자 경계 · `penalty 1e8` | 접촉 | 높음 | `ContactAction.C` · `MechanicalContactConstraint.C` (법선 성분만 판으로 · 접선 줄은 원판 내력 그대로 · 수렴하면 침투 ≈ 잔차 ÷ penalty) |
| `save_in` + `NodalSum` | 판 힘 | 높음 | `save_in` = 변수 비례 조정 전 국소 잔차 (`Kernel.C` · `StressDivergenceTensors.C`) |
| `VolumePostprocessor` · `ElementIntegralVariablePostprocessor` (`use_displaced_mesh`) · `AverageNodalVariableValue` · `NumNonlinearIterations` · `ElementExtremeValue` | 면적 · 응력 · 변위 · 반복 | 높음 | framework 소스 |
| PJFNK + LU + `NONZERO` 이동 + `-mat_mffd_err 1e-5` · SMP full | 풀이기 | 높음 | MOOSE 2D 유한 변형 접촉 시험 (`mortar_tm/2d/frictionless_first/finite.i`, E = 10⁷) 과 같은 꼴 |
| `abort_on_solve_fail` · `dtmin` | C | 높음 | `TransientBase.C` |
| 407 걸음 끝까지 수렴하는가 (완전 소성 · 20 % 압축 · 접촉 넓어짐) | — | **모름** | 1 단계가 재는 것 |
| P4 가 10⁻³ 안인가 | — | 모름 [추정: 통과 쪽] | 탄성 부피 변형 ≈ 1–2 % 의 2 차 항 + MOOSE 잠김 방지 정의 (증분 F 평균의 det) 몫 — 실패하면 그 몫인지 먼저 본다 |

## 1저자가 정할 것

| # | 질문 | 권고 |
|---|---|---|
| Q1 | 접촉 꼴: 설계는 mortar ALM.  여기서는 node-face kinematic 을 주 경로로 했다 — 판이 평평한 강체 primary 라 판의 법선을 그대로 쓰고, 마찰 없는 판이 주는 힘은 정확히 수직이다.  MOOSE mortar 는 원판 쪽 절점 법선으로 힘을 주는데, 다각형 원판의 접촉 띠 끝에서 그 법선이 기울어 가짜 x 힘이 생기고 P2 의 ⟨σxx⟩ 검사에 잡힌다 [소스 판독 · 크기 미측정].  | kinematic 그대로 1 단계를 돌린다.  2 단계 (원판끼리 · 양쪽 다 곡면) 는 mortar 가 유력하니 그때 따로 시험한다 |
| Q2 | Exodus (`out.e`) 를 걸음마다 쓴다 (m13 + m26 ≈ 30 MB [추정]) | 둔다 (모양을 눈으로 볼 수 있다) · 돌려보내는 묶음에서는 뺀다 |
| Q3 | 스모크가 거부되면 | 화면을 그대로 세션에 보낸다 → 세션이 고친 새 블록 (자동 재시도 없음) |

## 한정

- 이 단계의 답은 개발 자료다.  판정 문장 · 논문 숫자에 쓰지 않는다.  FE 값에 MPM 을 맞추지 않는다 (frame [4] · 메모 3.2 §3-2 규칙 4).
- C · P1 · P2 · P4 는 도구 검사 (평형 · 평균 응력 정리 · 부피 ↔ 압력 항등식) 다.  원판의 물리가 실험과 맞는지는 보지 않는다.
- P6 은 원판 하나라 판정이 아니다 (설계 그대로).  P3 · P5 · P7 · P8 과 다른 팔은 이 블록에 없다.
- 반력은 판이 아니라 원판 쪽에서 읽는다 (kinematic 에서 같은 양 [소스 판독]).  ⟨σ⟩ 는 요소 평균 추정자라 정확한 적분과 아주 조금 다르다.
