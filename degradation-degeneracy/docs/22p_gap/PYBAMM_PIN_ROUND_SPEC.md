# PyBaMM 환경 고정 라운드 — 고정 표 (C lock + B 역사 프로필 · 기록 대조)

> 2026-10-04 · **코드 변경 전** · 사용자 승인 "권고대로 너가 순서대로 해줘 같이 쳐내가자" (원문 · 해석은 원장 §135). 범위 초안
> `PYBAMM_PIN_ROUND_SCOPE_20261004.md` (커밋 `666524050`) 의 §3 초안을 여기서 확정한다. 기준 = 이 표가 든 커밋 (RUN_SCOPE 는
> `26c11d6fc` 이후 불변 · source_digest `803e2b7781cbc9cd`). **실행 GO 아님.** 설치 · 버전 변경 · 재생산 · 버전 비교 계산 없음.
> 틀은 사전 검토 회신 기록 `PYBAMM_PIN_PREREVIEW_REPLY_20261003.md` (C 현재 검증 · B 역사 정본 · D 새 생산 guard) 그대로다.

## §1 결정 (원장 §135)

| # | 결정 | 이 표에서 |
|---|---|---|
| D1 | 라운드 착수 | 이 커밋이 첫 커밋 (코드 전) |
| D2 | 범위 = **C + B** · D 는 새 생산 계획이 생길 때 별도 라운드 | §3–§6 · D 는 §11 |
| D3 | C 의 쓰임 = **기록 대조** (fail-closed 아님) | §4-4 · §5 |
| D4 | C 의 자리 = **새 lock 파일** · `requirements.txt` 하한 유지 | §3 · §7 |
| D5 | `requirements.txt` 주석 "검증 완료 조합" 을 같은 라운드에서 정정 | §7 |
| D6 | 정본 재생성 · 새 세대 생산 · 26.7.1 ↔ 26.8 비교 = 범위 밖 · 각각 별도 결정 | §11 |

## §2 파일 상한 (이 밖이 필요하면 멈추고 그 차이만 승인 요청)

| 파일 | RUN_SCOPE | 변경 |
|---|---|---|
| `requirements-validation-C.lock.txt` (새) | **안** (glob `requirements*.txt`) | C lock (§3) |
| `tools/env_profile.py` (새) | **안** | 측정 · lock 해석 · 대조 · lock 출력 · CLI (§4) |
| `requirements.txt` | **안** | 주석만 (§7) — 요구 줄 12 개 바이트 불변 |
| `scripts/smoke_e2e.sh` | **안** | 기록 단계 하나 (§5-1) |
| `docs/22p_gap/make_receipt.py` | 밖 | stamp 에 대조 결과 · `_stamp()` helper (§5-2) |
| `docs/22p_gap/env_profile_B_v4.yaml` (새) | 밖 | B 프로필 기록 (§6) |
| `tests/test_gate90_env_profile.py` (새) | 밖 | e01–e12 (§8) |
| `docs/22p_gap/mutation_replay.py` | 밖 | `-g90` 등록 + EXPECT (§9) |

불변: `src/` 전부 (`env_fingerprint` · `validate_provenance` · `src/grid.py` · `src/runner.py` · `src/fitting.py`) · `run.sh` · `configs/` ·
`requirements-gpu.txt` · `tools/` 의 다른 파일 · `tests/conftest.py`. 계산 경로 · solver 생성 · worker 서명 대조는 이 라운드에서 건드리지 않는다
(그 자리는 D — §11).

## §3 C lock — `requirements-validation-C.lock.txt`

### 3-1. 문법 (닫혀 있다 — 그 밖의 줄은 형식 오류 → 대조 결과 `UNMEASURED`)

| 줄 | 꼴 | 규칙 |
|---|---|---|
| 빈 줄 · 자유 주석 | 빈 줄 · `# …` (`#@` 로 시작하지 않는 주석) | 무시 |
| 지시 | `#@ <key> <JSON 문자열>` | key ∈ {`profile` `python` `implementation` `system` `machine` `libc`} · 각각 **정확히 한 번** · 값은 `json.loads` 가 `str` 을 내야 한다 (빈 문자열 · 공백 포함 값을 모호하지 않게) · `profile` 은 `"C"` |
| 배포판 | `<name>==<version>  # record-sha256 <R>` | name = PEP 503 정규형 (`[a-z0-9]+(-[a-z0-9]+)*`) · version = 공백 · `#` 없는 비지 않은 문자열 · R = 소문자 hex64 또는 `none` (RECORD 없음) · **이름 순 엄격 오름차순** (중복 없음) |
| 가려진 항목 | `#@ shadowed <name>==<version> record-sha256 <R>` | 경로 순서로 이미 본 이름의 뒤 항목 (다른 디렉터리에 가려진 것 · 같은 디렉터리의 중복 메타데이터 포함) · (name, version, R) 순 비감소 |

바이트: UTF-8 · LF (`.gitattributes` 의 `*.txt text eol=lf`) · 끝 줄바꿈. 줄 머리의 자유 주석은 `emit_lock` 이 쓰는 고정 문구다.

### 3-2. 내용 (생성 시점 이 검증 컨테이너의 실측 — 2026-10-04)

| 축 | 값 |
|---|---|
| 지시 | `python "3.11.15"` · `implementation "CPython"` · `system "Linux"` · `machine "x86_64"` · `libc "glibc 2.39"` |
| 유효 배포판 | **170** — `pip freeze` 167 + `pip` · `setuptools` · `wheel` (`pip freeze` 가 숨기는 셋). 대조는 `importlib.metadata` 의 전체 목록이다 |
| 가려진 항목 | **2** — `packaging 24.0` (`/usr/lib/python3/dist-packages` · `/usr/local/…` 의 26.3 에 가려짐) · `cryptography 41.0.7` (같은 디렉터리의 중복 메타데이터) · 둘 다 RECORD 없음 |
| RECORD 없는 유효 배포판 | **22** (Debian 시스템 배포판 — `pyyaml` · `pip` · `setuptools` · `wheel` · `cryptography` 등) — 파일 대조 불가 · 결과의 `unverifiable` 에 이름으로 |
| 핵심 배포판 | pybamm 26.8.0.0 · pybammsolvers 0.9.1 · casadi 3.7.2 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.5 · joblib 1.6.0 · pyarrow 25.0.1 · matplotlib 3.11.2 · pyyaml 6.0.1 |

생성: 프로젝트 root 에서 `python -m tools.env_profile --emit-lock` 의 출력 그대로. 정규형: `emit_lock(parse_lock(text)) == text` (고정점).

### 3-3. 선언하지 않는 것

C 는 정본 (v4) 생산 환경이 아니다 · C 로 만든 수치가 B 의 수치와 같다는 주장이 아니다 · **설치 처방이 아니다** (리눅스 시스템 배포판을 담는다 —
`pip install -r` 용으로 만들지 않았다) · 다른 기계 (사용자 Windows · 생산 서버) 에 강제하지 않는다.

## §4 대조 — `tools/env_profile.py`

### 4-1. 측정 — 그 프로세스의 `sys.path` 순서 그대로

| 축 | 측정 |
|---|---|
| 해석기 · 플랫폼 | `platform.python_version()` · `python_implementation()` · `system()` · `machine()` · `" ".join(platform.libc_ver()).strip()` |
| 배포판 | `sys.path` 의 각 항목에 `importlib.metadata.distributions(path=[항목])` — 정규 이름의 첫 항목 = 유효 · 뒤 항목 = 가려진 것. version = 메타데이터 그대로. record = RECORD 텍스트 (`read_text("RECORD")`) 의 UTF-8 sha256 · 없으면 `none`. 이름 없는 배포판은 측정 실패 |
| 파일 | RECORD 가 있는 **유효** 배포판의 해시 있는 항목 전부를 다시 해시해 RECORD 와 대조 — 다름 · 없음 (`FileNotFoundError`) = 불일치 · 해시 없는 항목은 수만 (`files_unhashed`) · 그 밖의 읽기 오류 · 모르는 해시 알고리즘 = 측정 실패. 설치 뒤 파일 변경의 감지 범위는 RECORD 가 덮는 만큼이다 (사전 검토 P2) |
| origin | `KEY_MODULES` = `env_fingerprint()` 의 module 축 10 (`numpy` `scipy` `pandas` `joblib` `pyarrow` `pybamm` `matplotlib` `yaml` `pybammsolvers` `casadi`) 마다 `importlib.machinery.PathFinder.find_spec(m, sys.path)` 의 origin 파일이 (i) RECORD 가 있는 유효 배포판 **하나**의 파일 목록에 있으면 확인 (주인 이름을 남긴다) · (ii) 아니고 RECORD 없는 유효 배포판의 디렉터리 안이면 확인 불가 (`unverifiable`) · (iii) 그 밖 (못 찾음 · 파일 아님 · 어느 배포판에도 없음 · 주인 둘 이상) 은 불일치 — 사전 검토 Q5 "설치 식별과 실제 origin" |

측정 프로세스의 `sys.path` 와 계산 진입점 (`python -m src.*` · cwd = 프로젝트 root) 이 같도록 CLI 는 `python -m tools.env_profile` 로 부른다.
저장소 안 경로 (프로젝트 root · `tools/` · `docs/22p_gap/`) 에 배포판 메타데이터 · 핵심 module 이 없음은 e06 이 확인한다 (경로 첫 항목의 차이가
결과를 바꾸지 않는다는 근거).

### 4-2. 결과 — 닫힌 dict (`compare_lock()` 은 예외를 내지 않는다)

| 키 | 값 |
|---|---|
| `profile` | `"C"` |
| `lock_path` | 저장소 안이면 프로젝트 root 기준 POSIX 상대경로 · 밖이면 절대경로 |
| `lock_sha256` | lock 바이트의 hex64 · 읽지 못하면 `None` |
| `status` | `MATCH` (불일치 0) · `MISMATCH` (불일치 ≥ 1) · `UNMEASURED` (lock 을 읽지 못함 · 형식 오류 · 측정 예외) |
| `reason` | `UNMEASURED` 면 비지 않은 문자열 (형식 오류는 줄 번호를 담는다) · 그 밖은 `""` |
| `mismatches` | `{"axis","subject","locked","measured"}` 목록 · (axis, subject) 순 · axis ∈ {`python` `implementation` `system` `machine` `libc` `dist_missing` `dist_extra` `dist_version` `dist_record` `shadowed` `file` `origin`} · `UNMEASURED` 면 **`None`** |
| `unverifiable` | `{"dists_without_record": [이름…], "origins": [module…]}` · `UNMEASURED` 면 `None` |
| `counts` | `dists_locked` `dists_measured` `shadowed_locked` `shadowed_measured` `files_verified` `files_unhashed` `origins_verified` (정수) · `UNMEASURED` 면 `None` |

`MATCH` 는 `unverifiable` 의 일치를 주장하지 않는다 (따로 이름으로 적는다). 측정하지 않은 칸은 `None` 이다 — 빈 목록 · 빈 dict 로 쓰면
"불일치 없음" 으로 읽힌다 (61차 P1-3 의 교훈).

### 4-3. CLI

`python -m tools.env_profile [--lock PATH] [--json] [--emit-lock]` — 기본 lock 은 도구 위치 기준 프로젝트 root 의 `requirements-validation-C.lock.txt`.
요약 줄 (상태 · lock sha256 앞 16 · 수) + 불일치 줄 (`✗ axis subject locked=… measured=…`) + 확인 불가 줄. `--json` 은 결과 dict (키 정렬).
**rc 0 — 세 상태 모두** (기록 전용 · D3) · 사용법 오류 rc 2 · `--emit-lock` 은 측정 실패면 rc 1 (부분 lock 을 내지 않는다).

### 4-4. fail-closed 아님의 경계

`MISMATCH` · `UNMEASURED` 는 pytest · smoke · `run.sh` · 영수증 생성 어느 것도 막지 않는다. 다만 도구 자체가 잡히지 않은 예외로 죽으면
smoke 의 실패로 센다 (§5-1 — 기록이 만들어지지 않은 것은 기록 대조가 아니다). `UNMEASURED` 를 `MATCH` 로 적지 않는다.

## §5 기록 자리

| # | 자리 | 규칙 |
|---|---|---|
| 5-1 | `scripts/smoke_e2e.sh` | `bad()` 정의 뒤 · 단계 0 전에 `step "환경 프로필 C 대조 (기록 전용 · 원장 §135)"` 와 `"$PY" -m tools.env_profile \|\| bad "환경 프로필 C 대조 도구 실패"` 한 번. 상태는 로그에만 — 판정 축이 아니다 |
| 5-2 | 검증 영수증 stamp (`docs/22p_gap/make_receipt.py`) | `stamp.environment_profile_C` = `compare_lock()` 결과 dict 그대로. stamp 는 core 밖이라 재생성 대조 · `core_sha256` · `tools/preserve.py::read_verification_receipt` (최상위 키 집합만 본다) 불변. stamp 는 새 helper `_stamp()` 가 만든다 (시험 진입점) |
| 5-3 | 게이트 증거 | smoke 로그 (5-1) · 두 영수증의 stamp (5-2) · clean 커밋의 `python -m tools.env_profile --json` 원문 한 개 |

## §6 B 프로필 — `docs/22p_gap/env_profile_B_v4.yaml` (기록 전용 · RUN_SCOPE 밖 · 어떤 코드도 읽지 않는다)

| 키 | 내용 |
|---|---|
| `profile` · `kind` | `B` · `HISTORICAL_PRODUCER_RECORD_ONLY` |
| `sources` | 네 producer manifest — `artifacts/grid_curves_v4/curves_manifest.yaml` (3,713 B · `a6e5ab9c…`) · `artifacts/grid_fit_v4/manifest.yaml` (6,576 B · `228664b1…`) · `artifacts/halfcell_fit_v4/manifest.yaml` (7,711 B · `3fa4106a…`) · `artifacts/paired_fixed5_v4/manifest.yaml` (6,310 B · `7a14333e…`) — 각각 경로 · 바이트 수 · sha256 (64 자) · env 가 든 키 경로 전부 (`env` · `grid_run_spec.env` · `run_spec.env` · `start_provenance.env`) |
| `env` | 일곱 자리에 같은 13 키 그대로 — python 3.10.12 · platform `Linux-5.15.0-130-generic-x86_64-with-glibc2.35` · machine x86_64 · numpy 2.2.6 · scipy 1.15.3 · pandas 2.3.3 · joblib 1.5.3 · pyarrow 25.0.1 · pybamm 26.7.1.0 · matplotlib 3.10.9 · yaml 6.0.3 · pybammsolvers 0.9.0 · casadi 3.7.2 |
| `solver` | `grid_curves_v4` 의 `solver` (`IDAKLUSolver`) 와 `grid_run_spec.effective_solver` (effective_class `IDAKLUSolver` · requested `type idaklu` · `rtol 1e-6` · `atol 1e-6` · `fallback casadi` · `casadi_mode safe`) · 세 fit 의 `run_spec.producer.solver` (`IDAKLUSolver`) — 원문 그대로 · 출처 경로와 함께 |
| `not_recorded` | 전이 의존성 · 배포 파일 해시 (RECORD) · 로컬 패치 · native 라이브러리 (SUNDIALS · BLAS · OpenMP) · Python 빌드 · smoothing backend 축 (지문에 그 축이 생기기 전 기록) |
| `not_claimed` | B 를 다시 설치하면 정본이 같게 나온다 · B = C · 26.7.1 ↔ 26.8 동등 |
| `use` | 정본 재생성을 시도할 때의 기준 — 재생성 동등성을 주장하려면 그때 사전 고정 비교가 따로 필요 (사전 검토 Q2) · 이번 범위 아님 (D6) |

## §7 `requirements.txt` 주석 정정 (D5 · 요구 줄은 바이트 불변)

`# ── 핵심 ──` 아래 세 줄 (`# 검증 완료 조합 (2026-08-05, docs/ENV_REPORT.md):` · `#   pybamm 26.7.1.0 / numpy 2.4.6 / scipy 1.17.1 / pandas
3.0.5 / Python 3.11` · `#   IDAKLU OK, composite DFN OK, 1 solve ≈ 2 s`) 을 다음으로 바꾼다 — 옛 문구는 "옛 주석" 으로 인용해 남긴다:

```
# ★ 90차 (원장 §135 · D5) — 이 파일은 **하한만** 둔다. 생산 환경 선언이 아니다.
#   · v4 정본 producer 환경 기록 = 프로필 B — docs/22p_gap/env_profile_B_v4.yaml (기록 전용)
#   · 현재 검증 환경의 정확 고정 = 프로필 C — requirements-validation-C.lock.txt (기록 대조 전용 · 막지 않는다)
#   옛 주석 "검증 완료 조합 (2026-08-05, docs/ENV_REPORT.md): pybamm 26.7.1.0 / numpy 2.4.6 /
#   scipy 1.17.1 / pandas 3.0.5 / Python 3.11 · IDAKLU OK, composite DFN OK, 1 solve ≈ 2 s" 는
#   scaffold 커밋 61bce598d 때 scripts/verify_env.py 진단의 기록이다 — v4 정본 producer 기록
#   (Python 3.10.12 · numpy 2.2.6 · scipy 1.15.3 · pandas 2.3.3 · pybamm 26.7.1.0) 과 다르고,
#   인용한 docs/ENV_REPORT.md 는 .gitignore 된 로컬 출력이라 저장소에 없다.
```

요구 줄 12 개 (`pybamm[all]>=24.5` … `pytest-json-report>=1.5` — 줄 끝 주석 포함) 는 바이트 그대로다.

## §8 시험 — RED 먼저 · 새 파일 `tests/test_gate90_env_profile.py` · node `e01`–`e12`

`tools.env_profile` · `make_receipt` 의 import 는 각 시험 **안에서** 한다 (수집 오류가 아니라 node 별 실패로 RED 를 본다). 합성 환경은 `tmp_path`
의 가짜 site 디렉터리 (`*.dist-info` 의 METADATA · RECORD · 파일 — 해시는 실제로 계산) 이고, 측정 경로는 함수 인자로 준다.

| node | 내용 | RED 기대 |
|---|---|---|
| e01 | 커밋된 lock: 형식 · 정규형 고정점 · §3-2 의 지시 값 · 유효 170 · 가려진 2 · 핵심 배포판 버전 · record 칸 형식 | 실패 (파일 없음) |
| e02 | 합성 왕복: `KEY_MODULES` 열 개 + RECORD 없는 배포판 하나 + 가려진 항목 하나 → `emit_lock` → `compare` = `MATCH` · 수 · `unverifiable` 이름 | 실패 (모듈 없음) |
| e03 [사례] | 축마다 정확히 그 축만: lock 쪽 교란 — `python` `implementation` `system` `machine` `libc` · `dist_missing` (lock 에 줄 추가) · `dist_extra` (줄 삭제) · `dist_version` · `dist_record` · `shadowed` / 환경 쪽 교란 — `file_hash` (설치 파일 수정) · `file_missing` (설치 파일 삭제) · `origin_stray` (경로 앞쪽의 RECORD 밖 사본) · `env_upgrade` (배포판 재설치 · 새 버전 → `dist_version` + `dist_record` 정확히 둘) → `MISMATCH` · 축 집합 일치 | 실패 |
| e04 [사례] | 형식 오류 → `UNMEASURED`: 모르는 지시 · 지시 중복 · 지시 누락 · JSON 아닌 값 · 정렬 어긋남 · 배포판 중복 · record 칸 형식 · 정규형 아닌 이름 · 모르는 줄 · UTF-8 아님 · 파일 없음 — `reason` (줄 번호) · `mismatches` / `unverifiable` / `counts` = `None` · 파일 없음이면 `lock_sha256` = `None` | 실패 |
| e05 [사례] | 측정 예외 → `UNMEASURED` (`MATCH` 아님): 이름 없는 배포판 · 모르는 해시 알고리즘 · 배포판 열거 자체의 예외 | 실패 |
| e06 | 실제 환경 · 커밋된 lock: 닫힌 키 · 상태 ∈ {`MATCH`, `MISMATCH`} · `lock_sha256` = 파일 sha256 · `dists_locked` 170 · 저장소 안 경로에 배포판 메타데이터 · 핵심 module 없음 | 실패 |
| e07 | `KEY_MODULES` = `src.io.env_fingerprint()` 의 module 축 (python · platform · machine · smoothing_backend 를 뺀 키 — 배포판 이름 `pybammsolvers` · `casadi` 포함) | 실패 |
| e08 | CLI (분리 프로세스): 어긋난 lock → rc 0 · `MISMATCH` · 축 줄 / 형식 오류 → rc 0 · `UNMEASURED` / `--json` → 닫힌 dict / `--emit-lock` → 정규형 lock · rc 0 | 실패 |
| e09 | smoke 정적: `-m tools.env_profile` 호출 정확히 하나 · `\|\| bad` (`\|\| true` 아님) · `bad()` 정의 뒤 · 단계 0 전 | 실패 (호출 없음) |
| e10 | `make_receipt._stamp()` 에 `environment_profile_C` = 닫힌 결과 dict · 상태 typed · `build()` 가 `_stamp()` 를 쓴다 · `VERIFICATION_RECEIPT_KEYS` 불변 | 실패 (`_stamp` 없음) |
| e11 | B 프로필 = 네 manifest: 경로 · 바이트 수 · sha256 · env 키 경로 **전수** (manifest 를 걸어 찾은 집합과 같다) · 일곱 env 가 `env` 와 같다 · solver 기록 · 한계 문구 | 실패 (파일 없음) |
| e12 | `requirements.txt`: 요구 줄 12 개 바이트 그대로 · "검증 완료 조합" 은 "옛 주석" 인용 안에만 · B · C 경로가 있고 파일이 존재 · "하한만" | 실패 (정정 전) |

새 node 이름이 등록부의 기존 `-k` 와 겹치지 않음을 KeywordMatcher 로 확인한다 (88 · 89차와 같은 절차). 기존 시험은 바꾸지 않는다 — 예상되는
기존 실패는 영수증 재생성 전의 validator identity 낡음 (89차 `03` 과 같은 종류) 뿐이고, 그 밖의 실패가 나면 멈추고 보고한다.

## §9 변이 (`-g90`)

| 이름 | 끄는 것 | 죽이는 node |
|---|---|---|
| `env-profile-compares-interpreter-and-platform-g90` | 해석기 · 플랫폼 다섯 축 비교 | e03 `python` … `libc` |
| `env-profile-reports-missing-dists-g90` | 빠진 배포판 보고 | e03 `dist_missing` |
| `env-profile-reports-extra-dists-g90` | 남는 배포판 보고 | e03 `dist_extra` |
| `env-profile-reports-version-drift-g90` | 버전 비교 | e03 `dist_version` · `env_upgrade` |
| `env-profile-reports-record-drift-g90` | RECORD digest 비교 | e03 `dist_record` |
| `env-profile-reports-shadowed-drift-g90` | 가려진 항목 비교 | e03 `shadowed` |
| `env-profile-verifies-installed-files-g90` | 설치 파일 재해시 대조 | e03 `file_hash` · `file_missing` |
| `env-profile-checks-module-origin-g90` | origin 판정 (주인 없음 → 통과) | e03 `origin_stray` |
| `env-profile-lock-grammar-is-closed-g90` | 모르는 줄을 건너뜀 | e04 `garbage` 류 |
| `env-profile-measurement-failure-is-unmeasured-g90` | 측정 예외 → 빈 결과 `MATCH` | e05 |
| `env-profile-cli-is-record-only-g90` | `MISMATCH` 에 rc 1 | e08 |
| `smoke-records-env-profile-g90` | smoke 기록 단계 제거 | e09 |
| `receipt-stamp-records-env-profile-g90` | stamp 필드 제거 | e10 |

증인은 `--emit-expect` 관측값으로 고정한다. 같은 치환 지점의 변이 둘을 독립 지점 둘로 세지 않는다 (89차 검토). 구현 모양 때문에 행을 합치거나
나눠야 하면 멈추고 그 차이를 보고한다.

## §10 영수증 · identity · 순서

RUN_SCOPE (lock · `tools/env_profile.py` · `requirements.txt` · `scripts/smoke_e2e.sh`) 가 바뀌므로 source_digest 가 움직이고, `make_receipt.py` 가
바뀌므로 영수증 core 의 `make_receipt_sha256` 도 움직인다 → 두 leg (`paired_fixed5_v4` · `grid_fit_v5`) 영수증 history 보존 뒤 clean 커밋에서
1 회 재생성 (stamp 에 `environment_profile_C`) · LEG_PRESERVATION 앵커 2×2 → 전체 pytest · strict smoke · 등록부 전체 변이 재생 (clean ·
start HEAD = end HEAD · dirty 0 · 동시 실행 없음) → GATE90 요청. 기존 정본 수용은 소급 취소하지 않는다 · 기존 artifacts 는 다시 만들지 않는다.

## §11 하지 않음

D guard (봉인 profile → 계획 · 생산 진입 · resume · worker 대조 · solver fallback 거부 — 새 truth 생산 계획이 생길 때 별도 라운드) · C 의
fail-closed · 설치 · 업그레이드 · 다운그레이드 · B 로 정본 재생성 · 새 세대 생산 · 26.7.1 ↔ 26.8 비교 계산 · `requirements.txt` 하한 변경 ·
`requirements-gpu.txt` · `src/` · `run.sh` · `tests/conftest.py` · 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class · 투영 게시.
REIL · COMSOL 작업은 게이트 차수 밖으로 따로 (이 라운드에 섞지 않는다).
