# REIL C4-0a 한정 보완 (C4-0A-N1–N4) 승인 요청 · 2026-10-13

> 근거: C4-0a 결과 검토 회신 (상태 문서 §42 · `reviews/review_reil_c4_0a_result_20261013/`). 회신 원문: "네 항목의 변경부와 같은 분기의
> 양성·음성 대조를 먼저 고정해 사용자에게 **별도 한정 보완·검증 승인**을 요청해 주세요."
> 이 문서는 승인 요청이다. 승인 전에는 저장소의 코드 · 시험을 바꾸거나 돌리지 않는다 (아래 §1 의 두 파일은 `docs/` 의 고정본이고 pytest 가 모으지 않는다).

## 1. 먼저 고정한 것 (승인 전 · 실행 0)

| 대상 | 파일 | sha256 |
|---|---|---|
| 대조 (시험 14) | `docs/REIL_C4_0A_FIX_CONTROLS_DRAFT_20261013.py.txt` | `b2137e1119049f4f2b87c096fbb77a3de26304ea355adac98da85d796728004c` |
| 변경부 (패치) | `docs/REIL_C4_0A_FIX_PATCH_DRAFT_20261013.diff` | `a3f527a4957f70c4bb3f0b4473b7d12c33e695a43f5e1afd00e68d4a18037874` |
| 패치 전 (지금) | `scripts/reil_c4_e3a.py` · `scripts/reil_c4_monitor.py` · 기존 시험 `tests/test_reil_c4_0a.py` | `14751a75…5bb0` · `0c6ed54f…e892` · `6b2635d4…7e17` |
| 패치 뒤 기대 | `scripts/reil_c4_e3a.py` · `scripts/reil_c4_monitor.py` | `33b855378fb76634eb314f8cfb0428151ce1ec8b9045bc8447d8e17354a41ac3` · `0644510032e986aad2f67c824ebab70d8da699bb5a60680330377353200a60a9` |

확인은 정적인 것만 했다: 두 패치 결과본과 대조 파일의 parse · 이름 검사 (symtable) · `git apply --check` 통과. 저장소 코드는 그대로다.

## 2. 고칠 것 (패치 요지)

- **N1 · `check_arrays(arrays_dir, *, seal, manifest_sha256)`**
  - 수용된 봉인 (C6) 의 MANIFEST 바이트를 명시 sha256 으로 인증한다.
  - 넷의 npy sha 를 그 항목에 **직접** 대조한다. 그 뒤 로컬 MANIFEST · ARRAYS.json 의 자기 일치를 따로 본다.
  - `dryrun` 은 이미 받은 `seal` 을 넘긴다. 결과에 `c6_direct_match` 가 붙는다. CLI 인자는 바뀌지 않는다.
- **N2 · `final_record`**
  - 마지막 쓰기 · 재읽기 · 해시 · 용량 조회 **뒤** snapshot 하나로 시간 한도를 판정하고, 그 값을 그대로 반환한다.
  - 넘으면 `RECORD_INCOMPLETE` 다. 파일 · 해시 · 바이트 수는 보존한다.
  - 시간 · 크기 위반은 둘 다 `problems` 와 `limit_violations` 에 남긴다.
- **N3 · `Watch.stale(now)` + `supervise`**
  - `Watch.stale(now)` 는 확인만 한다 — `last_valid` · `samples` 를 바꾸지 않는다.
  - `supervise` 가 RSS 조회 뒤 · 디스크 조회 뒤 · 정상 종료 직전에 두 감시기의 freshness 를 본다.
  - 기존 이유 (마감 재검사 등) 가 먼저다 — 기존 시험의 판정 문구는 그대로다.
- **N4 · 구조 오류의 `partial`**
  - `worker_loop` 의 구조 오류 이벤트에 `partial` (JSON 형) 을 싣는다.
  - `_states` 는 그 작업 행에 `structural_partial` 을 붙인다. 상태는 `STARTED_INTERRUPTED` 그대로다 — 완료 행으로 바꾸지 않는다.
- **바꾸지 않는 것:** `run_e3a_call` · `classify` · 배열 봉인 · C5 코드 · 기존 시험 파일 · 기존 증거.

## 3. 대조 14 — 지금 코드 (패치 전) 에서의 RED 예상

| 시험 | 대상 | 종류 | RED 예상 |
|---|---|---|---|
| n1_a 배열 + 로컬 두 기록을 함께 바꿈 → dryrun 거부 · 쓰기 0 | N1 | 음성 | 실패 — `DID NOT RAISE` (지금은 계획을 쓴다) |
| n1_b 명시 sha 와 다른 C6 MANIFEST → 거부 | N1 | 음성 | 실패 — `TypeError` (`seal` 인자 없음 · 구현 전) |
| n1_c 손대지 않은 봉인 → 넷 모두 C6 직접 일치 | N1 | 양성 | 실패 — `TypeError` (구현 전) |
| n2_a 마지막 쓰기 뒤 snapshot 61 s > 60 s → 미완 · 해시 보존 · 그 값 반환 | N2 | 음성 | 실패 — 지금은 `COMPLETE` |
| n2_b 쓰기 뒤 용량 조회 지연 → 미완 | N2 | 음성 | 실패 — 지금은 `COMPLETE` |
| n2_c 한도 안 → COMPLETE · 반환 snapshot = 판정값 | N2 | 양성 | 통과 |
| n2_d 시간 · 크기 둘 다 초과 → 둘 다 기록 | N2 | 음성 | 실패 — `limit_violations` 없음 |
| n3_a 마지막 디스크 조회 6 s 뒤 정상 종료 → RSS 공백 6 s > 5 s 로 중단 | N3 | 음성 | 실패 — 지금은 `global_stop None` |
| n3_b 마지막 디스크 조회 1 s → 정상 종료 | N3 | 양성 | 통과 |
| n3_c `Watch.stale` 은 유효 시각 · 표본을 바꾸지 않는다 | N3 | 음성 | 실패 — `AttributeError` (구현 전) |
| n4_a `worker_loop` 가 partial 을 보낸다 | N4 | 음성 | 실패 — 지금은 info 만 |
| n4_b 실제 fork 작업자 · E3a 셋째 평가 MemoryError → partial (3 · 1 · 2 · 1) 이 부모에 · 작업은 중단 | N4 | 음성 | 실패 — partial 없음 |
| n4_c 우리 wrapper 안 오류 → 구조 (회신이 명시 요청) | — | 특성 고정 | 통과 (이미 구현된 분기) |
| out 합성 NSGA2 의 분기 · 평가 수 · 예외 요약을 파일로 | — | 기록용 | 통과 (기능 변경 없음) |

- 기대: **10 실패 · 4 통과**, 실패 종류도 표 그대로다.
- n3_a · n3_b 는 대본 multiprocessing 문맥 (실제 프로세스 0) 과 주입 시계로 돈다 — 검토 회신 M2 가 제안한 "대본 시계 · 디스크 콜백 · 끝 이벤트".
  `multiprocessing.get_context` 를 시험 동안만 `monkeypatch` 로 바꾸므로 생산 코드에 주입점을 더하지 않는다.
- n4_b 만 실제 fork 작업자를 쓴다 ("worker 경계를 통과한 partial 기록").

## 4. 실행 순서와 배정 (승인하면)

1. 착수 전에 `.gitattributes` 에 `evidence/reil_c4_0a_fix_20261013/** -text` 를 넣고 커밋한다.
2. 착수 기록 (t0 · HEAD · uptime) 을 쓴다. 증거 폴더가 이미 있으면 중지한다.
3. **identity 1 회 (60 s)** — C4-0a 와 같은 대조 스크립트 · 같은 인자 (새 봉인 경로 · 전체 MANIFEST sha). 맞지 않으면 시작하지 않는다
   (§38 · §39 의 환경 조건 → 별도 승인).
4. 대조 고정본을 `tests/test_reil_c4_0a_fix.py` 로 복사하고 sha 를 대조한다 (`b2137e11…`).
5. **RED 1 회 (600 s)** — 새 시험 파일만, 지금 코드로 돈다. §3 의 예상 (10 실패 · 4 통과 · 실패 종류) 과 다르면 원문을 보존하고 멈춘다.
6. 패치를 적용한다 (`git apply` · 고정본 sha `a3f527a4…`). 결과 sha 가 §1 의 기대값과 다르면 멈춘다.
7. **GREEN 1 회 (600 s)** — 기존 시험 파일 (26) + 새 시험 파일 (14), `-rP` 를 붙인다. 기대는 40 통과다. 예상 밖 실패는 원문을 보존하고 멈춘다
   (자동 수정 · 재시험 없음).
8. 끝 기록 · 비밀값 검사 · 커밋 · push · 결과 기록 (§43) · 검토 발송문을 쓰고 멈춘다.

- **배정:** identity 60 + RED 600 + GREEN 600 = 계산 1,260 s · 전체 작업 2 h · 자동 재시험 0.
- **단계 실행기:** C4-0a 의 것과 같은 방식 (cwd `bms-balancing/` · 비밀 형태 env 제거 · BLAS 1 스레드 · `MPLBACKEND=Agg` · scratch
  `MPLCONFIGDIR` / `TMPDIR` · meta · stdout · stderr · porcelain 시작 / 끝 · 덮어쓰기 거부). 증거 폴더만 새 폴더이고, `out` 시험이 쓸
  `REIL_C4_FIX_EVIDENCE` · `REIL_C4_FIX_STEP` 두 env 를 더한다. 실행기 사본은 증거 폴더에 넣는다.
- **합성 NSGA2 호출 수:** `out` 시험이 RED · GREEN 에서 각 1 회 (`02_red.nsga2_synthetic_outcome.json` · `03_green.…`), 기존 test_07 이 GREEN
  에서 1 회 (`-rP` 로 출력이 로그에 남는다) — 모두 3 회다. 각 ≤ 5,000 평가 · 합성 곡선 · 자료 0 이고, 결과가 같은지도 보게 된다.

## 5. 하지 않는 것

- 기존 26 기록 · 02_red / 03_green 증거 · 환경 봉인 · 배열을 덮어쓰지 않는다.
- 전체 bms-balancing suite · 환경 재구축 · full C6 check · 배열 재봉인 · 건조 재실행을 하지 않는다.
- C4-0b · C4-E / A / B · 자료 개봉 · 맞춤 · 설치 · COMSOL 은 범위 밖이다.

## 6. 정하실 것

1. **위 범위 그대로 승인할지.**
2. GREEN 에 기존 26 을 회귀로 같이 돌릴지 — **권장: 같이 돈다.** 바뀌는 네 함수가 모두 기존 시험이 지나는 경로다 (`check_arrays` ← test_09
   의 dryrun · `final_record` · `supervise` · `worker_loop`).
3. 건조를 다시 돌릴지 — **권장: 돌리지 않는다.** N1 의 dryrun 경로는 n1_a 와 기존 test_09 가 함수 수준에서 덮고, 배열 · 계획은 이미 수용됐다.
