# REIL C5 요청문 v2 — 부록 (v2 사전 검토 C5V2-N1 · 문구 3 정정) · 2026-10-06 · 실행 0

> v2 (`REIL_C5_PILOT_APPROVAL_REQUEST_v2_20261006.md` · 커밋 `457db0b44` · 검토가 본 바이트 sha256 `3ee657da…`) 는 고치지 않는다. 이 부록이 아래 자리를 **대신한다**.
> 회신: `reviews/prereview_reil_v2_c5_request_v2_20261006/` (판정 "주요 정정 수용 · 환경 확인 호출의 범위 충돌 1 건 정정 필요"). 범위는 넓히지 않는다.

## A1. 환경 확인 = 계산 없는 식별 (C5V2-N1 P1 · v2 §4-2 · §5 "환경" 행 · §6-1 · §11 대체)

- **사실 (회신 · 우리 재확인):** `reil_c6_profile.py check` (`:237–246`) 는 `emit` (`:222–234`) 을 불러 **합성 최적화 1 회** (`cobyqa_options` `:149–181`) 와 **Sobol 배열 생성** (A0 · A1 / A2 · unit ·
  옛 `seed=` 대조 — `sobol` `:185–219`) 을 다시 한다. 시험에서 `emit` 을 가짜로 바꾼 사실은 실제 명령에 해당하지 않는다. v2 의 "venv 에서 `check` 만" 과 원판 회신의 `check` 권고는 이 점에서 넓었다.
- **대체 규칙 — 구현 단계와 측정 단계 모두 full `check` 를 부르지 않는다.** `reil_c5_pilot.py` 안에 **계산 없는 환경 식별** `env_identity()` 를 둔다:
  1. 실제 interpreter: `os.path.realpath(sys.executable)` · `sys.prefix` · `sys.version` — 지정 venv (`…/scratchpad/reil_p0/venv`) 가 아니면 중지.
  2. 설치 배포판: `reil_c6_profile.lock_text()` (설치 파일을 RECORD 와 해시 대조 — 읽기 · 해시만) 의 바이트 == 봉인 `reil_c6_rebuild_20261006/REIL_C6.lock.txt`.
  3. 프로필: `reil_c6_profile.profile()` (판 · 플랫폼 · 빌드 메타데이터 — 읽기만) 의 `_dump` 바이트 == 봉인 `PROFILE.json`.
  4. COBYQA: 봉인 `COBYQA_OPTIONS.json` 의 `options` == 파일럿이 넘길 옵션 표 · `implementation_files_sha256` 의 각 파일을 **지금 설치본에서 다시 해시**해 같음 (합성 최적화 호출 없음).
  5. 봉인 MANIFEST 의 파일별 sha 와 봉인 파일 바이트 일치 (봉인 자체의 무결성 — **이것만으로 현재 환경을 검증했다고 쓰지 않는다**; 1–4 가 현재 환경 대조).
- **측정 단계 (§10 (2) 승인 뒤):** `env_identity()` → 그 다음 **A0 seed 0 · 1 배열만** 같은 venv 에서 `qmc.Sobol(4, scramble=True, rng=seed)` 로 다시 만들어 봉인 `sobol_A0_their_box_seed{0,1}.npy` 와
  바이트 대조 (v2 §4-1 그대로). A1 / A2 · unit 배열 · 옛 `seed=` 대조 · 합성 최적화는 하지 않는다.
- **기록:** full C6 `check` = `NOT_RUN` · 좁은 식별을 "C6 전체 기능 PASS" 로 쓰지 않는다. full `check` 를 쓰려면 그 안의 합성 최적화 · 배열 · 임시 파일 · 횟수 · 예산을 **별도 환경 자기검사**로 승인받는다.
- 허용 파일은 v2 §5 의 두 파일 그대로 (`env_identity()` 는 `scripts/reil_c5_pilot.py` 안 · 시험은 `tests/test_reil_c5_pilot.py` 에서 가짜 설치 · 봉인으로 — RED 먼저).

## A2. 실행 상태 문구 (v2 §3 표 대체)

128 행은 각각 **지역 실행 상태 4 개** 중 정확히 하나다 — `NOT_STARTED` · `STARTED_INTERRUPTED` · `RETURNED_REEVAL_INTERRUPTED` · `COMPLETED`. `RECORD_INCOMPLETE` 는 행 상태가 아니라
**파일럿 전체 기록 상태** (최종 기록 실패) 이며 따로 적는다.

## A3. 무자료 한정 시험의 텍스트 입력 (v2 §5 "무자료 한정 시험 집합" 행 보충)

| 시험 파일 | 읽는 저장소 텍스트 입력 (식별) | 성격 |
|---|---|---|
| `tests/test_reil_p0.py` | `reviews/prereview_pybamm_reil_20261003/external/NOTEBOOK_SOURCE_EXCERPTS.json` (sha256 `95cca5f35aaaf72757812068251d72064b464cff6ef3f523c756f33d27d243a9`) · `…/external/util_LFP.py.txt` (sha256 `bdf78273d50f40ce3154d01a3ef8d36f0f5ea5ec1b04539584809d7b19b46f9c`) · `evidence/reil_p0_20261006/P0_RESULT.json` 은 읽지 않음 | 보존된 **검토 묶음 텍스트** (노트북 셀 원문 발췌 · util 사본) — 원 노트북 실행 · REIL xlsx · pkl 아님. util 사본은 `spec_from_file_location` 으로 로드 (최상위 import · 함수 정의만 · 상태 §22-2 의 AST 제한 유지) |
| `tests/test_reil_c6_profile.py` | 없음 (합성 RECORD 표 · `tmp_path`) | 측정 함수 넷을 가짜로 바꾼다 |
| `tests/test_reil_c5_pilot.py` (새) | `P0_RESULT.json` (셀 규칙 재계산) · 봉인 `COBYQA_OPTIONS.json` · util 사본 (위 sha) — 실행 전 식별 기록 | 합성 입력 · 가짜 설치 · 봉인 |

## A4. 구현 단계 한도의 정의 (v2 §5 "구현 단계 전체" 행 보충)

- **3,600 s 는 명령 실행 시간의 합**이다 (전체 벽시계가 아님). 합에 넣는 것: RED · GREEN · 무자료 한정 시험 · 건조 실행 · `env_identity()` 단독 실행 · 보존 명령 (`git` · 해시) 의 각 소요.
- 명령별 timeout: pytest 실행마다 **600 s** (RED 도 같음 — 넘으면 그 실행은 `timeout` 으로 기록하고 GREEN 횟수에 넣는다) · 건조 실행 **300 s** · `env_identity()` **120 s**.
- pytest 실행 경로: cwd `bms-balancing/` · `…/scratchpad/reil_p0/venv/bin/python -m pytest -p no:cacheprovider <파일>` · `PYTHONPATH=…/scratchpad/reil_p0/pytest_t` (venv 밖 · 이미 있는 것만 — 없으면
  설치하지 않고 중지) · `MPLBACKEND=Agg` · `MPLCONFIGDIR=<스크래치>`.
- 증거 폴더 `evidence/reil_c5_impl_20261006/` — 시작 때 있으면 **중지** (덮기 · 새 이름 없음).

## A5. 채택 문구 (v2 §10 (1) 대체)

> REIL C5 비용 파일럿의 구현을 v2 문서 (`bms-balancing/docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_20261006.md`) §5 와 부록 (`…_v2_ADDENDUM_20261006.md`) A1–A4 의 범위와 한도로
> 승인합니다. 두 파일 · RED 1 회 · GREEN 최대 3 회 · 무자료 한정 시험 집합 1 회 · 합성 건조 실행 1 회 (maxfev 50 · 작업자 2 · 300 s) · 계산 없는 환경 식별만 하고, full C6 check ·
> REIL 자료 · 정식 Sobol · 환경 재구축 · 비용 측정 · bms 전체 시험은 하지 말고 멈추세요.

v2 §10 (2) 측정 승인 문구는 "환경 확인" 을 A1 의 측정 단계 규칙으로 읽는다 (측정 승인 때 다시 확인).
