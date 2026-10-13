# REIL C4-0b1 한정 보완 (C4-0B1-N1–N3 · 승인 경계 A1) 승인 요청 · 2026-10-13

> 근거: C4-0b1 결과 검토 회신 (상태 문서 §48 · `reviews/review_reil_c4_0b1_result_20261013/`). 회신 원문: "다음에는 N1–N3 한정 보완·합성 검증
> 범위와 승인 경계 정리를 제안해 주세요." · "생산 변경 파일·추가 합성 사례·횟수·예산을 제시해 사용자 승인을 먼저 받고, 실패 기록을 유지한다."
> 이 문서는 승인 요청이다. 승인 전에는 저장소의 코드 · 시험을 바꾸거나 돌리지 않는다 (§1 의 두 파일은 `docs/` 의 고정본이고 pytest 가 모으지 않는다).

## 1. 먼저 고정한 것 (승인 전 · 실행 0)

| 대상 | 파일 | sha256 |
|---|---|---|
| 대조 (시험 15 항목) | `docs/REIL_C4_0B1_FIX_CONTROLS_DRAFT_20261013.py.txt` | `7133c550628c819c2eadca1d2e4e468ce9373d0907ccd9dc098a4c471f4e1297` |
| 변경부 (패치) | `docs/REIL_C4_0B1_FIX_PATCH_DRAFT_20261013.diff` | `5d2b887c16d0315bea96e90995c3b45c207b05025a38ef162525c3323148387d` |
| 패치 전 (지금) | `scripts/reil_c4_h.py` · `tests/test_reil_c4_0b1.py` | `676b0847…85ad` · `6afd6d98…7434` |
| 패치 뒤 기대 | `scripts/reil_c4_h.py` · `tests/test_reil_c4_0b1.py` | `7d49f132ec2133b1c2ae380140ba61ba10ef97a183ce304800e4fa15d23c3c0d` · `1040e531aa4a6696bb1f37ac1075f23db361ff99d0d3f7b6008afb590c346b2c` |

확인은 정적인 것만 했다: scratch 사본에 패치를 적용한 결과의 parse · 이름 검사 (symtable) · 모듈 속성 대조 · `git apply --check` 통과 · 적용
결과 = 위 기대 sha. 저장소의 코드 · 시험은 그대로다.

## 2. 생산 변경 파일 — `scripts/reil_c4_h.py` 하나

- **N1 · 구조 중지의 부분 기록 (`_partial` · `run_phase_a` · `_run_phase_a`)**
  - 실행 하나가 모으는 것 (행 · 평가 계수 · 경고 목록) 을 작업 단위 누적기에 걸어 두고, **모든 구조 중지 경로**가 그것을 partial 로 보낸다:
    최적화 중 구조 오류 · 모르는 옵션 경고 · 미분류 termination (N2) · 재평가 구조 오류 · 라벨 구조 오류 · 우리 코드의 예외 (wrapper).
  - partial = 그때까지의 행 (task · x0 · 반환점이 있으면 x · status · message · termination 등) + `n_eval` · `n_nonfinite` + `warnings` 원문 +
    `stop_error` (중지시킨 오류 원문). 아직 생기지 않은 값은 넣지 않는다 (0 · 성공값으로 채우지 않음).
  - 모르는 옵션 경고 경로는 계수 · 경고를 행에 적은 **뒤**에 중지한다 (지금은 적기 전에 partial 없이 중지).
- **N2 · 미분류 termination 은 전체 중지 (`termination` · `_run_phase_a`)**
  - `termination` = C5 `termination_of` 그대로: 성공 → `converged` · MAX_EVAL / MAX_ITER → `budget` · 그 밖 → `unclassified`.
  - `unclassified` 이면 재평가 · 증인으로 넘어가지 않고 `UnclassifiedTermination` 구조 중지 — partial 에 원 status · message · 반환점 · 계수.
  - `solver_error` 는 최적화 중 지역 예외 (반환점 없음) 에만 남는다. enum 별 다른 분류는 제안하지 않는다 (회신: 고정 환경 대응표를 먼저 승인).
  - 참고: COBYQA 는 `np.linalg.LinAlgError` 를 스스로 잡아 `LINALG_ERROR` status 로 돌려준다 (`scipy/_lib/cobyqa/main.py` 567 · 636 행) —
    목적 함수 쪽 LinAlgError 도 이 경로면 이제 전체 중지다.
- **N3 · 재평가 예외는 REEVAL_ERROR (`witness` · `_run_phase_a`)**
  - `witness(..., reeval_error=False)`: SOLVER_ERROR → **REEVAL_ERROR** → NONFINITE → INFEASIBLE_RETURN 순. 반환점의 독립 재평가에서 지역 예외면
    `invalid:REEVAL_ERROR` · 정상 반환한 NaN 은 `invalid:NONFINITE` · 구조 오류는 전체 중지. 원 termination 은 덮어쓰지 않는다.
  - 이유별 집계 (`phase_a_summary`) 는 이유 문자열로 세므로 그대로 둘이 갈린다.
- **A1 · 건조는 읽기만 (`dryrun` · `check_h_arrays` · `_attach_from_files`)**
  - `dryrun` 에서 합성 표본을 뺀다 (`_synthetic_sample` · `_key` 삭제). PLAN.json 하나만 쓰고 `execution` 에 최적화 · 목적 호출 · util import ·
    Sobol 생성 0 을 적는다 (schema v2).
  - `check_h_arrays(..., regenerate=True)` 에 **바이트 대조** (`regenerate=False`) 를 더한다: 생성기를 부르지 않고 봉인 npy 바이트에서 블록 raw sha 를
    다시 계산해 INDEX 와 맞춘다 (+ MANIFEST 인증 · 파일 · P0 · 계획 · 표 · 규칙 기록 대조는 그대로). 건조는 이것을 쓴다.
    재생성 대조는 봉인 단계와 시험에만 남는다.
  - **이 바이트 대조 전환은 회신이 요구한 것이 아니라 내 제안이다** — 05 답변에서 "Sobol 재생성은 '읽음'만은 아니다" 라고 판단을 맡긴 부분 (§48).
    빼기로 하시면 대조 · 패치 고정본을 다시 만들어야 한다 (§8-2).
- **바꾸지 않는 것:** 봉인 배열 · label · 규칙 기록 · `seal_h_arrays` · 목적 · ρ · 문턱 · 공통 갱신 · e3a · monitor · c5 · 기존 증거
  (05 의 `SYNTHETIC_SAMPLE.json` 포함 — 범위 이탈 기록으로 그대로 둔다).

## 3. 기존 시험의 기대값 정정 — 패치 안 `tests/test_reil_c4_0b1.py` 두 곳

| 시험 | 지금 기대 (승인과 다름) | 고친 기대 |
|---|---|---|
| test_07 termination | LINALG_ERROR → `solver_error` | → `unclassified` (이름도 `…_or_unclassified`) |
| test_10 건조 | `SYNTHETIC_SAMPLE.json` 20 행 · 목적 넷 완료 | 그 파일 없음 · `execution` 0 회 (이름 `…_writes_only_the_plan` · 절 머리 주석) |

나머지 49 항목은 그대로다.

## 4. 대조 15 항목 — 지금 코드 (패치 전) 에서의 RED 예상

| 시험 | 대상 | 종류 | RED 예상 |
|---|---|---|---|
| n1_a 실제 fork · COBYQA · 목적 NaN · NaN · MemoryError → 부모에 평가 3 · 비유한 2 · 중지 오류 · 작업 중단 | N1 | 음성 (회신 반례) | 실패 — partial 이 (3, 없음) · `stop_error` 없음 |
| n1_b 모르는 옵션 → 구조 중지 · partial 에 계수 · 경고 원문 | N1 | 음성 | 실패 — partial 없음 |
| n1_c 반환 · 재평가 뒤 우리 코드 예외 → partial 에 계수 · x · termination | N1 | 음성 | 실패 — partial 이 task_id · unit · run_id 뿐 |
| n1_d n1_a 와 같은 fork 경로 · 오류 없음 → 완료 · 전역 중지 없음 | N1 | 양성 | 통과 |
| n2_a 성공 → converged · 예산 → budget · LINALG · INFEASIBLE · 999 · 성공 아닌 0 → unclassified | N2 | 음성 | 실패 — LINALG_ERROR 가 `solver_error` |
| n2_b status 999 반환 → 구조 중지 · partial 에 원 status · message · 재평가 0 | N2 | 음성 | 실패 — `DID NOT RAISE` |
| n2_c ×2 성공 · 예산 반환 → 재평가 · 유효 증인까지 | N2 | 양성 | 통과 ×2 |
| n2_d 실제 fork · status 999 → 전역 중지 · 작업 중단 · partial status 999 | N2 | 음성 | 실패 — `global_stop None` (지금은 완료) |
| n3_a 재평가 중 util 지역 예외 → `invalid:REEVAL_ERROR` · termination 유지 · 집계 분리 | N3 | 음성 | 실패 — `invalid:NONFINITE` |
| n3_b 재평가가 NaN 을 정상 반환 → `invalid:NONFINITE` | N3 | 양성 | 통과 |
| n3_c 재평가 MemoryError → 구조 중지 · partial 에 termination · x · 평가 수 | N3 | 특성 고정 | 통과 (이미 구현된 분기) |
| a1_a Sobol 생성 · minimize · util 로드를 막고 건조 → PLAN.json 하나 · `execution` 0 회 · mode bytes | A1 | 음성 | 실패 — 건조가 봉인 재생성 대조에서 `qmc.Sobol` 을 부름 (AssertionError) |
| a1_b npy 한 값과 그 MANIFEST 항목을 함께 바꿈 → 바이트 대조가 INDEX raw sha 로 거부 | A1 | 음성 | 실패 — `TypeError` (`regenerate` 인자 없음 · 구현 전) |
| a1_c 손대지 않은 봉인 → 생성기를 막아도 바이트 대조 통과 | A1 | 양성 | 실패 — `TypeError` (구현 전) |

- 기대: **10 실패 · 5 통과**. 실패는 행동 반례 8 (n1_a · n1_b · n1_c · n2_a · n2_b · n2_d · n3_a · a1_a) + 인터페이스 부재 2 (a1_b · a1_c).
- 실제 fork 작업자를 쓰는 것: n1_a · n1_d · n2_d (감시 모듈 `supervise` · 작업자 1). 가짜 minimize 는 `monkeypatch` 로 부모에서 바꾸고 fork 가 물려받는다.

## 5. 추가 합성 사례 · 횟수 (회신 요구)

| 실행 | RED (새 15 만) | GREEN (기존 51 + 새 15) |
|---|---|---|
| 실제 COBYQA · **가짜 목적** (건조 옵션 maxfev 50) | 3 실행 — n1_a (fork · 3 평가에서 중지) · n1_b · n1_d (fork) | 8 실행 — 위 3 + 기존 test_08 의 5 (그중 1 은 첫 평가에서 지역 오류) |
| 가짜 minimize (최적화기 없음 · 목적 0–3 호출) | 8 — n1_c · n2_b · n2_c ×2 · n2_d (fork) · n3_a · n3_b · n3_c | 8 (같음) |
| 보존 util 사본 (합성 곡선 · 최적화 없음) | 0 | 기존 test_06 의 평가 몇 회 (v_full · jv_jd · J_V^s) — 이번에 바뀌지 않음 |
| 보존 util 사본 + COBYQA (합성 표본) | 0 | **0** — test_10 의 합성 표본 20 실행이 A1 로 없어진다 (지난 GREEN 보다 20 실행 적음) |
| Sobol 생성 (봉인 함수 · 시험 안) | a1_a 전체 봉인 1 · a1_b · a1_c 부분 봉인 2 | 위 + 기존 test_05 · test_10 의 봉인 · 재생성 대조 |
| REIL 자료 · xlsx · pkl · 노트북 | 0 | 0 |

- 시험 밖 (단계로서) 의 합성 실행은 없다. 건조 재실행도 없다.

## 6. 실행 순서와 배정 (승인하면)

1. 착수 전에 `.gitattributes` 에 `evidence/reil_c4_0b1_fix_20261013/** -text` 를 넣고 커밋한다.
2. 착수 기록 (t0 · HEAD · uptime) 을 쓴다. 증거 폴더가 이미 있으면 중지한다.
3. **identity 1 회 (60 s)** — C4-0b1 과 같은 대조 스크립트 · 같은 인자 (새 봉인 경로 · 전체 MANIFEST sha). 맞지 않으면 시작하지 않는다.
4. 대조 고정본을 `tests/test_reil_c4_0b1_fix.py` 로 복사하고 sha 를 대조한다 (`7133c550…`).
5. **RED 1 회 (600 s)** — 새 시험 파일만, 지금 코드로 돈다. §4 의 예상 (10 실패 · 5 통과 · 실패 종류) 과 다르거나 무관한 하네스 실패가 나면
   원문을 보존하고 멈춘다.
6. 패치를 적용한다 (`git apply` · 고정본 sha `5d2b887c…`). 결과 sha 가 §1 의 기대값과 다르면 멈춘다.
7. **GREEN 1 회 (600 s)** — 기존 시험 파일 (51) + 새 시험 파일 (15), `-rP` 를 붙인다. 기대는 66 통과다. 예상 밖 실패는 원문을 보존하고 멈춘다
   (자동 수정 · 재시험 없음).
8. 끝 기록 · 비밀값 검사 · 커밋 · push · 결과 기록 (§49) · 검토 발송문을 쓰고 멈춘다.

- **배정:** identity 60 + RED 600 + GREEN 600 = 계산 1,260 s · 전체 작업 2 h · 자동 재시험 0 (C4-0a 보완과 같다).
- **단계 실행기:** C4-0b1 의 것에서 증거 경로 · scratch 폴더 · env 두 이름 (`REIL_C4_0B1_FIX_EVIDENCE` · `REIL_C4_0B1_FIX_STEP`) 만 바꾼다.
  사본은 증거 폴더에 넣는다.

## 7. 위험 · 밝힐 것

1. **기존 시험의 실제 COBYQA 5 실행 · 새 n1_b · n1_d:** 패치 뒤에는 성공 · 예산 밖 status 가 나오면 전체 중지다. 그런 status 가 나오면 GREEN 이
   예상 밖 실패로 멈춘다 (원문 보존). 지금까지의 관측: C5 파일럿 128 실행 (실자료 · 본 옵션) 이 모두 `converged` (status 0) · 05 합성 표본의 반환
   18 실행이 모두 converged / budget · 기존 test_08_a_run_records 는 converged / budget 을 단언해 통과했다. 나머지 기존 실행의 termination 은
   기록되지 않았다.
2. a1_b · a1_c 의 RED 실패는 인터페이스 부재 (`TypeError`) 다 — 행동 반례가 아니다.
3. partial 의 `stop_error` 는 구조 이벤트의 info 와 같은 내용이다. 상태 행 (`structural_partial`) 에도 중지 오류가 남게 하려고 겹쳐 싣는다.
4. RED / GREEN 은 C4-0 전체로 각 4 회가 된다 (0a · 0a 보완 · 0b1 · 0b1 보완). 0b2 까지 가면 각 5 회다.
5. 회신의 조건 "ρ 는 두 단일 목적 Phase A 완료 뒤 · 공통 갱신은 등록 탐색 종료 뒤 1 회" 는 실제 연결부의 몫이다 — 이 보완에 넣지 않는다 (0b2 · C4-A).

## 8. 하지 않는 것

- 기존 51 기록 · `02_red` / `03_green` / `05_dryrun` 증거 (SYNTHETIC_SAMPLE.json 포함) · 배열 · 환경 봉인을 덮어쓰거나 지우지 않는다.
- 건조 재실행 · 배열 재봉인 · full C6 check · 전체 bms-balancing suite · 환경 재구축 · 설치를 하지 않는다.
- C4-0b2 · C4-E / A / B · 자료 개봉 · 맞춤 · COMSOL 은 범위 밖이다.

## 9. 정하실 것

1. **위 범위 그대로 승인할지.**
2. **A1 의 바이트 대조 전환** (건조에서 Sobol 재생성을 뺌) 을 넣을지 — **권장: 넣는다.** 건조 정의 "계획 · seed · 봉인만 읽음" 을 문자 그대로
   지키고, 05 에서 판정이 남은 부분 (§48) 을 닫는다. 빼면 대조 · 패치를 다시 고정해 다시 요청한다.
3. GREEN 에 기존 51 을 같이 돌릴지 — **권장: 같이 돈다.** 바뀌는 함수가 모두 기존 시험 경로이고, 두 기대값을 고친다.
4. 건조를 다시 돌릴지 — **권장: 돌리지 않는다.** a1_a 가 함수 수준에서 덮는다. 다음 건조는 0b2 의 몫이다.
