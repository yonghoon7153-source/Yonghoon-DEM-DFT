# kgy 실행 환경 (Python 3.8) 에서 R 경로 코드가 멈춘다 — 재현 · 수정 증거 (Rint ② · 2026-10-24 · `SELF-132` · `SELF-133`)

## 무엇이 있었나

- 1저자 10-24 kgy 출력: `~/dem-ca1-fe1be` (핀 `fe1be7960` · 깨끗함) 의 `scripts/test_ca_s0_census.py` → `FAIL: E1 | E11 | R | R8 | A` · S0 단계 1 출력 폴더
  `~/sdcp/ca1_s0_sbe_20261023` 에는 `payload_capture_kit_SBE_vgcf100.log` (1,168 B · 10-23 23:56) 하나만 남았다 (그 폴더는 실패 시도 기록 · 보존).
- kgy `~/dem-venv` = **Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1** (1저자 10-24 출력 · 기록 `docs/data/phase_a_6mah/README.md` 의 "py 3.8" 과 같음).
  개발 · 게이트 · Codex 탐침은 Python 3.11 · numpy 2.4.6 · scipy 1.17.1 에서만 돌았다.
- 같은 부류 세 번째: 08-16 (`check_method_discipline.py` 의 py3.8 주석 — 게이트가 원격 3.8 에서 막힘) · 08-25 (`pellet_rve_sigma.py` 주석 *"dict-union `|` 금지 — kgy dem-venv 는 Python 3.8"*).  막는 검사가 없었다.

## 재현 환경 (이 컨테이너)

- `uv python install 3.8` → CPython **3.8.20** (uv 관리 판 · kgy 는 3.8.10) · 그 인터프리터에 직접 (venv 없이) numpy **1.24.4** · scipy **1.10.1** (kgy 와 같은 판) ·
  scikit-image 0.21.0 · matplotlib < 3.8 · threadpoolctl · plotly · pyamg < 5.2.
- ⚠ venv 를 쓰면 `test_ca_ext_runner` · `test_rint_r_chain_e2e` 의 가짜 `python3` 심이 `os.path.realpath(sys.executable)` 로 venv 밖 기본 인터프리터 (패키지 없음) 를 집어
  numpy 가 없다고 멈춘다 — 재현 첫 판 둘이 이것 · git 이력 없는 사본 (`git archive`) 의 가짜 실패를 섞었다 (기록하지 않음).  kgy `~/dem-venv` 도 venv 라 그 두 시험은 kgy 에서
  같은 꼴로 멈췄을 것이다 (추정) → 수정 ④.
- 트리 = 리포를 `git clone --shared` 한 사본 (git 이력 · docs 있음) · 실행 = `tools/py38_runall.sh` (`PY38_BIN` = 그 인터프리터의 bin · BLAS 스레드 1 · nice 19).

## 결과

| 묶음 | 고치기 전 (`9a72d65c6` · `logs/unpatched/`) | 고친 뒤 (`9a72d65c6` + `tools/apply_py38_fix.py` · `logs/patched/`) |
|---|---|---|
| `run_contract --selftest` | 124/124 | 124/124 |
| `step3_sigma --selftest-rint` | PASS | PASS |
| `test_ptfe_face_alpha` | rc 1 · `dict \|` TypeError | 242 PASS · 0 FAIL |
| `test_carbon_junction` | rc 1 · `math.nextafter` 없음 13 | 440/440 (QD6x 는 이 판 뒤에 더함 → 커밋본 441) |
| `test_ca_ext_b6` | rc 1 · `dict \|` · `math.nextafter` | 454 PASS · 0 FAIL |
| `test_ca_ext_runner` | rc 1 · payload 가 `ptfe_face_alpha.capsule_summary` 에서 멈춤 | 128 PASS · 0 FAIL |
| `test_rint_r_chain` | 186/240 · `math.nextafter` 없음 8 | 240/240 |
| `test_rint_r_chain_e2e` | rc 1 · 러너 rc 1 (payload 멈춤) | 16 PASS · 0 FAIL |
| `test_step3_target_cert` (빠른 판) | rc 1 · `dict \|` · `math.nextafter` | 260/260 |
| `test_step3_conv_cert` | 26/27 · **K4** | 26/27 · **K4** (남음 — 아래) |
| `test_ca_s0_census` | 94 PASS · 5 FAIL (`E1 \| E11 \| R \| R8 \| A` = kgy 와 같음 · 전부 `dict \|` TypeError) | **152 PASS · 0 FAIL** |

- 시간 (고친 뒤 · 차례로 · 이 컨테이너): 합 ≈ 380 s (`logs/patched/summary.txt`).
- S0 의 멈춘 줄 = `ptfe_face_alpha.py` `capsule_summary` (traceback: `ca_s0_census.alpha_census` → `fa.capsule_summary`) — payload 가로채기는 끝나고 α 분포 계산에서 멈춘다.

## 고친 것 (`tools/apply_py38_fix.py` 가 사본에 한 것과 같은 바꿈 · 커밋본은 + QD6x)

| # | 자리 | 3.8 에서 | 고침 |
|---|---|---|---|
| ① | `scripts/ptfe_face_alpha.py` `capsule_summary` | `dict \| dict` → TypeError (S0 α 분포 · face_alpha payload 블록) | `{**{…}, 'dia_classes': …, 'volume_basis': …}` — 같은 dict (키 순서 같음) |
| ② | `scripts/ca_ext_svcf.py` `_div_dir` 의 방향 반올림 | `math.nextafter` (3.9+) → AttributeError (SV 증서 구간 · R 사슬 · `run_contract` 기록 검사) | `_nextafter` — `math.nextafter` 가 있으면 그것 (3.9+ 비트 같음) · 없으면 IEEE 754 비트 한 칸 (C99 규칙) |
| ③ | 시험 4 파일 (`test_carbon_junction` · `test_ca_ext_b6` · `test_step3_target_cert` · `test_rint_r_chain`) | `math.nextafter` 13 곳 (4 · 2 · 1 · 6) · `dict \|` 5 곳 | 시험 기대값은 numpy `np.nextafter` (모듈과 독립) · 사슬 시험은 3.8 이면 SV 모듈의 같은 함수 · `{**a, **b}` |
| ④ | 시험 심 2 곳 (`test_ca_ext_runner` · `test_rint_r_chain_e2e`) | `realpath(sys.executable)` = venv 밖 | `abspath` |

- 3.11 의 계산은 바뀌지 않는다 (① ③ = 같은 dict · ② = 3.9+ 는 `math.nextafter` 를 그대로 부른다).
- `_nextafter` 의 3.8 가지 대조: `math.nextafter` 를 떼고 160만 쌍 (경계 + 무작위 비트 패턴) 비교 = 차이 0 (`logs/check_nextafter.out` · 부호 있는 0 · NaN 포함) ·
  상주 시험 `test_carbon_junction` **QD6x** (3.9+ 에서도 `math.nextafter` 를 잠시 떼고 3.8 가지를 np.nextafter 와 비트 대조 · 32,112 쌍 · 고치기 전 모듈 = AttributeError 로 FAIL).
- 정적 훑기 (`tools/scan.py` · R 경로 import 닫힘 31 모듈 · 휴리스틱): 고치기 전 `logs/scan_rpath_before_fix.out` · 고친 뒤 `logs/scan_rpath_after_fix.out` —
  고친 뒤 남는 줄 = `np.nextafter` (numpy) · QD6x 의 `math.nextafter` 떼기 · 되돌리기 · `cg(rtol=)` 의 TypeError 폴백 (전부 의도 · 거짓 양성).  변수끼리의 `dict |` 는 이 훑기가 못 본다 → 정본 = 위 3.8 실행.

## 남는 것 — K4 (`SELF-133` · 다음 단계)

- `scripts/step3_sigma.py` `_solve_cg` 의 CPU 폴백은 scipy < 1.12 에서 `cg(..., tol=…)` (legacy) 로 내려간다.  정확한 해 (spsolve) 를 초기값으로 rtol 1e-14 이어 풀면
  scipy 1.10.1 = 30,000 회 미수렴 (info 30000) · 상대 잔차 2.7e-14 → **1.1e-10** (나빠짐 · `atol=0` 을 줘도 같음) · scipy 1.17.1 = 바로 수렴 (info 0 · 최대 차 2.4e-14)
  (`tools/k4probe.py` → `logs/k4probe_py38.out` · `logs/k4probe_py311.out`).
- 영향: kgy R 은 GPU 필수 (`EXPECT_BACKEND=gpu` · CPU 폴백 거부) · S0 는 풀이 없음 → 지금 돌릴 것과 무관.  kgy 판 시험에서는 K4 가 실패한다.
- 처분 = 1저자 10-24 Q2 (가): 오래된 scipy 의 CPU 폴백을 scipy ≥ 1.12 와 같은 CG 로 맞춘다 (시험 먼저) + 게이트에 kgy 판 (3.8 · numpy 1.24.4 · scipy 1.10.1) R 경로 시험 단계.
  gabia 판이 다르면 낮은 쪽에 맞춘다 (gabia 판 = 1저자 확인 대기).

## 폴더

- `tools/` — `py38_runall.sh` (11 묶음 실행 · `PY38_BIN`) · `apply_py38_fix.py` (사본에 한 바꿈) · `apply_stepB.py` (Step B 바꿈) · `check_nextafter.py` · `k4probe.py` · `scan.py`.
- `logs/unpatched/` · `logs/patched/` — 묶음별 전체 출력 + `summary.txt` · `logs/check_nextafter.out` · `logs/k4probe_py38.out` · `logs/k4probe_py311.out` · `logs/scan_rpath_*.out`.

## Step B — K4 고침 + 게이트 kgy 판 단계 (1저자 10-24 Q2 (가) · `SELF-133`)

- **K4 고침** — `scripts/step3_sigma.py`: 모듈 이름 `cg` = scipy ≥ 1.12 이면 scipy 의 `cg` 그대로 · 옛 판이면 `_cg_v112` (scipy 1.17.1 의 `cg` 반복을 옮긴 것 · 실수 계) · `_solve_cg` 의 옛 `except TypeError → cg(tol=…)` (legacy 정지) 를 뺐다.
  - 이름 하나로 바꿔 끼우므로 감싸기 (`step3_conv_cert._cg_count` · 시험 K3 의 spy) 가 두 판 모두에서 그대로 걸린다.
  - 3.11 (scipy 1.17.1) 에서는 `cg` 가 같은 scipy 함수라 계산이 바뀌지 않는다.
- **시험 먼저** — `test_step3_conv_cert.py` 에 `t_k4b_v112` (K4b · K4c · K4d):
  - 고치기 전 (모듈 = `89fc47011`) = `AttributeError: … no attribute '_cg_v112'` → 27/28 (`logs/stepB/conv_cert_tests_only_py311.out`).
  - 고친 뒤 3.11 = 30/30 — K4b = `_cg_v112` 와 scipy 1.17.1 `cg` 가 네 계 (초기값 없음 · 정확한 해 · 무작위 · maxiter 소진) 에서 해 바이트 · info · callback 수까지 같음.
  - 고친 뒤 3.8 (scipy 1.10.1) = 29/29 — K4 통과 · K4b 는 비교 대상 (`cg(rtol=)`) 이 없어 건너뜀 표시 (세지 않음 · 3.11 게이트가 본다) · K4c (옛 판 길로 K4 수렴) · K4d (판에 맞는 `cg`).
- **시험 기반 모듈에 같은 cg (3.8 에서만 뜻)** — 옛 커밋의 `step3_sigma` 를 불러 "끈 경로 비트 같음" 을 보는 세 시험 (`test_carbon_junction` C0 · `test_step3_conv_cert` K1 기반 · `test_step3_target_cert` T12 · T23 기반) 은
  scipy < 1.12 에서 기반 모듈이 legacy `cg(tol=…)` 를 써서 첫 3.8 실행에서 C0 · T23a · T23b 가 갈렸다 (σ · 잔차 · 불균형) → 기반 모듈에도 지금 판의 `cg` (= `_cg_v112`) 를 넣어 코드 경로만 비교한다.
  3.11 에서는 조건 (`S3.cg is S3._cg_v112`) 이 거짓이라 아무것도 바꾸지 않는다.
- **게이트 단계** — `scripts/check_kgy_py38.sh` (11 묶음 · 인터프리터 = `$KGY_PY38` 또는 `uv python find 3.8` · 판이 (3.8 · numpy 1.24.4 · scipy 1.10.1) 이 아니거나 없으면 실패 — 건너뛰지 않는다) ·
  설치 = `scripts/setup_kgy_py38.sh` (컨테이너 재시작 뒤 한 번 · uv · 네트워크) · `scripts/check_all.sh` 에 한 줄.
  - 사본 실행 (Step B + 같은 cg) = 11 묶음 통과 (`logs/stepB/kgy_step/`) — S0 152 · 접합 441 · 사슬 240 · 끝-끝 16 · 목표 증서 260 · 수렴 증서 29 · b6 454 · 러너 128 · S1 242 · 계약 124 · rint 자체시험.
  - 시간 ≈ 6–7 분 (차례로 · BLAS 스레드 1).
- ⚠ 재현 판 = uv CPython 3.8.20 (kgy = 3.8.10) · 나머지 패키지 (scikit-image 0.21.0 · matplotlib 3.7.5 · threadpoolctl 3.5.0 · plotly 7.1.0 · pyamg 5.1.0) 는 kgy 의 판 확인 전 (1저자 `pip freeze` 대기).
- `step4_dyn` 의 같은 꼴 폴백 (`cg(rtol=)` → `cg(tol=)`) 은 R 경로 밖 (`--no-step4`) 이라 그대로 둔다.
