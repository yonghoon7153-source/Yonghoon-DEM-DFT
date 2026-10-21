# Codex 짧은 재확인 요청 — DEM 언로딩 키트 수정 재확인 반영 (ULKRF-01 · 02 · 03 · Q2 · Q3 · Q4) + 발송 전 사전 공격 리뷰 반영 (ULPR-01–04) (2026-10-15 · 갱신 10-21 · 결과 0 건 · 발송 = 1저자)

## 이번에 닫는 것 / 닫지 않는 것 (10-21 갱신판 — 먼저 읽는다)

**이번에 닫는 것** — 수정 재확인 판정 (코드 핀 `eaecfba2a` · HOLD) 의 잔여 P2 셋 · Q2–Q4 를 판정문 §4 · §7 최소 해결대로, 그리고 발송 전 사전 공격 리뷰 (독립 에이전트 · 리뷰 핀 `92e6cda4d` ·
판정문 반입 = `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/prereview_REVIEW.md`) 가 찾은 넷 (원장 `ULPR-01`–`04` · 1저자 10-21 Q1 · Q2 *"권고대로"*):
- `ULKRF-01` 같은 경계 RESUME 중복 · 상충 = 승인 없음 + 사유 (판정문 §4 · `one_auth_two_rollbacks` · `duplicate_event_only`).
- `ULKRF-02` 승인된 재시도의 단 끝이 옛 시도보다 짧음 · 같음 · 김 = 새 시도 시작 식별 (`resume_completed_hold_5_windows`) · 무승인 되돌아옴 = 미식별 그대로 ·
  **+ 다섯째 경우 = 새 시도가 그 단 줄을 다시 쓰기 전에 끝남 (TIMEOUT · GUARD · 이동 중 TIMEOUT) — `ULPR-01` (P2) 로 닫음**: 승인 경계 뒤 줄은 어느 시도가 썼는지 기록으로 증명될 때만 쓴다 (§1 · 등록 §14-12).
- `ULKRF-03` G2c 필수 열 결손 (양쪽 · 실제 restore CLI) = 예외 없이 사유 · RESTORED 아님 — 그 분류를 `ULPR-04` (P3) 로 등록 §14-10 대로 바꿈: 관측 결손 NOT_COMPUTED → **UNCONFIRMED** (옛 판 FAIL → VALUE_MISMATCH · 관문 영향 없음).
- `ULPR-02` (P3) — ULKRF-01 · Q3 가 더한 사유 줄 · 조건 여섯을 줄마다 지키는 시험 (각 줄을 지운 변이 = 그 시험이 그 이유로 실패 · §3-2).
- `ULPR-03` (P3) — G2 원자 비교 (`ul_gates._dump_tokens` · 복원 · 중력 팔) 도 관측 파싱 규칙: 같은 ID 두 줄 · 다른 TIMESTEP · 잘린 줄 · NaN = 관측 결손 · 빈 덤프 둘 = 비교 대상 없음 · 요청 step 결합 (같은 부류로 G2c 머리 step).
- Q2 영수증 범위 문구 · Q3 문법 사전 점검 원자료 재판독 · Q4 비차단 셋 · `ULKRR-01` 의 실행 부분 (실행 2 반입 · §7 Q7).

**이번에 닫지 않는 것** (그대로 열림 · 숨기지 않는다):
- 본 R · 10:0 연장 · U 의 GO (실행 · 결과 0 건).
- 정수 반올림 — 기록 CSV 의 k · w · step · n_windows 소수 토큰을 `int(round())` 로 읽는다 (판정문 §6 관찰) · Codex `resume_recheck.py` 의 `fractional_resume_event_k` · `fractional_confirmation_k` 는 고친 트리에서도
  기대 미충족 그대로 (§0 탐침 표) · `ULPR-01` 의 단 줄 ↔ 창 대조도 같은 반올림 값을 쓴다.
- 재판독은 그 폴더의 **지금** 원자료를 다시 읽는다 — 런 뒤 원자료가 바뀌지 않았다는 영수증 (원자료 sha256 기록) 은 없다 · 원래 자리 한정 · 판독기 판 한정 (`b1121b6b6` 이후).
- 실제 LIGGGHTS (MPI · SLURM) 재개 · Windows 는 돌리지 않았다 — `ULPR-01` 근거 = 합성 기록 + 덱 · 러너 소스 순서 · Windows R32 양성 = Codex 확인 요청 그대로.
- `ULPR-01` 의 보수 쪽 대가 (설계 · 결함 아님): 기록으로 시도를 가를 수 없는 경계 뒤 줄은 쓰지 않으므로, 새 시도 자신이 단 줄 → 단 끝 restart 사이에서 끊긴 드문 경우 그 시도의 마지막 단 줄도
  버린다 (주 값 = 미식별 · 낮은 하한 쪽으로만 · 시험 R37 '시도 미확정').
- 이번 수정 diff 자체의 독립 재리뷰 — 사전 공격 리뷰는 고치기 전 핀 (`92e6cda4d`) 대상 · 수정 뒤 확인 = 고친 쪽의 변이 시험 25 · 지킴 시험 · 사전 리뷰 탐침 · Codex 탐침 재실행 (§0 · §3-2).

> **한 줄 (10-15 첫 판)**: 수정 재확인 판정 (코드 핀 `eaecfba2a` · **HOLD**) 의 새 P2 셋 (`ULKRF-01` · `02` · `03`) 을 판정문 §4 · §7 의 최소 해결대로 고치고, Q2 범위를 판정문 권고 문구 그대로 적고,
> 문법 사전 점검이 그 런 폴더 원자료를 **승인된 판독기로 다시 읽게** 했다 (Q3) · 비차단 셋 (Q4) 도 같이 — 시험 먼저 · LIGGGHTS 없음.  각 반례가 고친 트리에서 거부되고
> 양성 대조가 그대로인지, Linux 전체 로그가 지원 환경 실행 기록을 채우는지 짧게 판정해 달라.  남은 실행 = ibb 문법 fixture 실행 2 (실제 바이너리 · 원 보고 묶음) → ✅ 10-15 PASS (§7).
> **한 줄 (10-21 갱신)**: 발송 전 사전 공격 리뷰가 찾은 넷 (`ULPR-01` P2 · `02`–`04` P3) 을 시험 먼저 고쳤다 — 판독기 · 관문 비교 · 봉인 규칙 글만 (덱 64 · 러너 · 표 · 이력 시험 폴더 ·
> 문법 판독기 `read_history.py` 바이트 그대로) · 실행 없음.  ULKRF 반례 · 양성 대조가 그대로인지와 함께 ULPR 넷이 닫혔는지 판정해 달라 (§1 · §5 Q8 · Q9).
> ✅ **1저자 10-15** — 수정 계획 dem_unloading_kit_fix_recheck_fix_plan_20261015.md Q1–Q4 = 권고대로 (*"권고대로 부탁해"*).
> ✅ **1저자 10-21** — 사전 공격 리뷰 Q1 (`ULPR-01` 을 고친 뒤 발송) · Q2 (G2c 열 결손 = 등록 §14-10 대로 UNCONFIRMED · `ULPR-04`) = 권고대로 (*"권고대로"*).
> **리뷰 핀 (10-21 갱신판)** = `28b66e116` — 이 갱신의 마지막 코드 커밋 (키트 `SHA256SUMS` sha256 `ecf406a6ca2b310f853d6e618e964b06ed11b8b43d3c747e5d87f20425b25de8`) ·
> **바로 뒤 커밋 = 문서 · 증거 · 이 요청서** (키트 코드 · 봉인 · 덱 · 이력 시험 폴더 바이트 = 핀과 같음 · 바뀐 것 = 키트 README · 등록 §14-12 · 이 요청서 · 증거 폴더) ·
> 10-15 첫 판 핀 = `92e6cda4d` (실행 2 반입판 · 키트 폴더 = `fcc0d6a75` 와 바이트 같음) · **기준** = `eaecfba2a` (판정문 코드 핀).
> 10-21 커밋 번호 = 이 갱신 가지를 본 가지에 그대로 (fast-forward) 붙인 번호 (`SELF-116` — 옮겨 심으면 번호가 바뀌므로 메인 세션이 고친다).

## 0. 대상 · 지위

- 판정문 codex_review_dem_unloading_kit_fix_recheck_20261015.md · 증거 codex_dem_unloading_kit_fix_recheck_evidence_20261015 (10-15 첫 판: 탐침 스크립트는 **실행하지 않았다** — `notes/` ·
  `evidence/*.json` · 탐침 글로 반례를 읽고 우리 시험으로 다시 만들었다).  **10-21**: 판정문 §7 탐침을 리뷰 핀 사본에서 그대로 돌렸다 — 결과와 고친 트리에서 '기대 어긋남' 으로 찍히는 줄의 이유 = 아래 탐침 재실행 안내.
- 사전 공격 리뷰 (10-21 · 고친 사람 설명 없이 diff · 코드만 본 독립 리뷰 · 리뷰 핀 `92e6cda4d`) — 보장 12 를 작은 반례로 깨 봄 → 결함 넷 (`ULPR-01` P2 · `02`–`04` P3 · 원장) + 요청서 문안 하나 (`PRE-UL-05` · 원장 밖).
  판정문 · 탐침 · 그 실행 결과 반입 = 증거 폴더 `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/` (`prereview_REVIEW.md` · `probe_resume_unfinished.py` · `probe_misc.py` · `probes/` · `probes_out/`).
- 커밋 (본 가지 · 순서): (10-15) 시험 먼저 `1c0b9fd65` → 수정 `22a347722` → 문서 · 증거 · 이 요청서 첫 판 `fcc0d6a75` → 참조 검사기 도달 기준 `4803b959c` (키트 밖) → 원장 `44a034534` →
  실행 2 반입 + §7 `92e6cda4d` (키트 무변경) / (10-21) 원장 `ULPR-01`–`04` 등재 `286a8d562` → 시험 먼저 `f1b911f76` → `ULPR-01` `55fff3eb1` → `ULPR-03` · `04` `2932b63bc` →
  지킴 시험 `c21b1a051` · `28b66e116` (= 리뷰 핀) → 문서 · 증거 · 이 요청서 갱신판 (바로 뒤 · 키트 코드 무변경).
- 바뀐 곳 (10-15) = 키트 `docs/data/ps45_unload_20261009/` — `ul_lib.py` · `ul_gates.py` · `ul_reader.py` · `run_unload.sh` (주석 한 줄 — EXT rc 2 범위) · `seal_kit.py` (규칙 글 · 증인 ·
  규칙 수 24 그대로) · `ul_runner_test.py` · README · `SHA256SUMS` · `active_rules.json` / 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §14-9 정정 줄 · §14-11 (결과 0 건).
- 바뀐 곳 (10-21) = 키트 `ul_reader.py` (sha256 `48e8f5f5…` → `969d6a87…`) · `ul_gates.py` (`74f4de3a…` → `14b59aff…`) · `seal_kit.py` (`299d1941…` → `36cec116…` · 규칙 글 · 증인 · 규칙 수 24 그대로) ·
  `active_rules.json` (`5dbf414d…` → `48d63476…`) · `SHA256SUMS` (`441f66d7…6c34` → `ecf406a6…` · 줄 다섯만) · README / 등록 §14-12 (결과 0 건).
- 10-21 에 바꾸지 않은 것: `ul_lib.py` · `ul_s3.py` · `ul_observers.py` · `ul_runner_test.py` · `make_unload_decks.py` · 러너 `run_unload.sh` · `run_unload_ibb.sbatch` · `unload_params.json` ·
  생산 덱 64 (`make_unload_decks.py --check`) · 이력 시험 폴더 전부 (`history_test/SHA256SUMS` sha256 `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d` 그대로 — 덱 아홉 · 판 STL · 표 ·
  생성기 · 판독기 `read_history.py` sha256 `70f741a9b8308fe33683de0f22872e2c44ce674dd6223cfce8c00e1a725b696c` (= `GRAMMAR_READER`) · 러너) · 물리 목표 · P_meas 1 MPa · 0.10 %p · S1–S4 · KE 계수 10 · S3 1e-3 ·
  판 법선력 부호 −1 · S0.  (10-15 · 10-21 둘 다 바꾸지 않은 것 = 표 · 덱 64 · 이력 시험 폴더 · 물리 목표 이하.)
- 실행 없음 (본 R · 10:0 연장 · U · H0–H5 · 문법 fixture 실제 바이너리 · LIGGGHTS · MPI · SLURM · Windows).  원장 `docs/reviews/findings.json` 은 이 수정 가지에서 고치지 않았다 (claimed_fixed = 메인 세션).

### 탐침 재실행 안내 (10-21 · `PRE-UL-05`) — 판정문 §7 탐침을 리뷰 핀 사본에서 그대로 돌린 결과

사본 = 판정문 증거 `probes/` · `support/` 바이트 그대로 + `source/` = 리뷰 핀 git archive (키트 · 이력 시험 반입 · ps73 묶음 · 원 덱 · `scripts/plane_load_share.py`) · `python3 -I -X utf8 -B` · BLAS 1 스레드 ·
Linux.  사전 리뷰 변형 둘 (증거 폴더 `probes/` — `grammar_provenance_kitreader.py` = 원 탐침에 두 줄 더함 · `receipt_ids_recheck_q4tolerant.py` = 줄 296 한 줄 바꿈) 은 아래 표에 따로 적는다.  고친 트리에서 rc 1 · 예외 · '기대 어긋남' 으로 찍히는 줄은 전부 아래 이유 — **회귀 아님**.

| 탐침 | 리뷰 핀 결과 | 회귀 아님 · 이유 |
|---|---|---|
| `resume_recheck.py` | rc 0 · 37 경우 중 35 기대대로 · 기대 어긋남 둘 = `fractional_resume_event_k` (RESUME 사건 k `1.4`) · `fractional_confirmation_k` (단 기록 k `3.4`) — 둘 다 정수로 반올림해 읽고 주 값 OK | 정수 반올림은 이번에 고치지 않았다 (판정문 §6 관찰 · 맨 위 '닫지 않는 것') · 나머지 35 = ULKRF-01 · 02 반례 거부 · 양성 그대로 (ULPR-01 의 경계 뒤 줄 규칙을 거친 뒤에도) · 사전 리뷰가 핀 `92e6cda4d` 에서 돌린 결과와 같은 둘 |
| `receipt_ids_recheck.py` (그대로) | rc 1 · 줄 296 `IndexError` (정밀도 블록 · 요약 JSON 없음) | 그 블록은 토큰 `1.0000000000000001` 의 덤프 행이 있다고 가정하는데, Q4 수정이 그 토큰 (float 가 정수 1 로 가리는 비정수 ID) 을 파서 문제로 거부해 행이 0 — Q4 가 의도대로 동작한 결과 |
| 같은 탐침 · 정밀도 블록만 빈 행 허용 (`receipt_ids_recheck_q4tolerant.py`) | rc 0 · 92 단언 · 기대 어긋남 하나 = `g2c_missing_column_actual_cli` — 실제 = rc 2 · stderr 없음 · `restore_verdict.json` 씀 (UNCONFIRMED) · 다음 UB 거부 (사유 "RESTORED 아님 (UNCONFIRMED)") · 기준 판 (`eaecfba2a`) 의 어긋남 둘 (`g2c_c_cpl7_missing` · `g2c_c_cpl8_missing`) = 기대대로 (복원 UNCONFIRMED · G2c NOT_COMPUTED · UB 거부) · 범위 관찰 다섯 그대로 | 그 단언의 기대가 옛 결함 꼴 (*"Defect scope: unhandled KeyError, not a false RESTORED certificate"*) 을 적은 것이라, 고친 트리의 rc 2 · 증서 UNCONFIRMED · UB 거부가 '어긋남' 으로 찍힌다 = ULKRF-03 + ULPR-04 수정 신호 (핀 `92e6cda4d` 에서는 같은 자리가 VALUE_MISMATCH) |
| `grammar_provenance.py` (그대로) | rc 1 · 17 경우 · 음성 11 거부 (기대대로) · 기대 어긋남 여섯 = 양성 `positive_actual_reader` 거부 + 원자료 변조 넷 · `different_reader_runner_seal` 거부 | 이 탐침의 합성 kit 사본에는 `SHA256SUMS` 만 있고 판독기 `read_history.py` · 표 `history_params.json` 이 없어, Q3 설계대로 *"kit 사본 … sha256 None ≠ 승인된 판독기 봉인 값 — 실행하지 않는다"* 로 양성까지 거부된다 (러너의 kit 사본에는 두 파일이 있다 — 아래 변형) |
| 같은 탐침 · kit 사본에 두 파일 (봉인 바이트) 을 넣은 판 (`grammar_provenance_kitreader.py`) | rc 1 · 양성 허용 · 음성 11 거부 · 기대 어긋남 다섯 = 원자료 변조 넷 (재판독 status FAIL · rc 2 → 거부) · `different_reader_runner_seal` (그 런 kit `SHA256SUMS` 의 판독기 줄 ≠ 봉인 값 → 거부) | 다섯의 기대 (`gate True`) 는 기준 판 결함 (판정 JSON 의 PASS 를 그대로 믿음) 을 적은 것이고 Q3 가 의도해서 뒤집었다 · 판독기 줄 대조 · 재판독 rc 대조 사유는 이번 `ULPR-02` 시험이 지킨다 |
| `grammar_types.py` · `history_actual.py` · `kit_byte_checks.py` | rc 0 · 문법 형 여섯 기대대로 (Windows git bash 확인 = 이 기계에 없음) · H0–H5 재판독 PASS · 판독 rc 0 · 생산 덱 64/64 바이트 같음 | `history_actual` 의 `equals_pinned` 거짓 = 그 런 (10-14 09:47 · 문법 fixture 전) 의 kit 사본 `SHA256SUMS` ↔ 지금 `history_test/SHA256SUMS` — 이력 시험 폴더는 그 뒤 문법 fixture 로 바뀌었다 (`18b798ecc` 이후) · 이번 갱신 무관 |
| `grammar_windows_r32.py` | rc 1 — Linux 라 CRLF 0 · 처음부터 허용 | Windows 줄바꿈 진단 탐침 — Windows 에서 R32 양성이 서는지 = 확인 부탁 그대로 (§5 Q5) |
| `source_audit.py` | 돌리지 않음 | GitHub API 조회 · 앞 회차 폴더 · 그 핀 원천 목록 대조용 (고친 트리 판정과 무관) |
| 사전 리뷰 `probe_resume_unfinished.py` (ULPR-01 반례) | rc 0 · 9 경우 기대대로 (A2 · A4 · A5 = 같은 꼴 fresh 와 같은 UNIDENTIFIED · B2 = fresh 와 같은 하한 0.225119763714296 % · A6 · 대조 그대로) | 핀 `92e6cda4d` = 넷 어긋남 (A2 · A4 · A5 = OK ρ 0.2026… · B2 = 하한 0.27014371645715524 %) → 0 = ULPR-01 수정 |
| 사전 리뷰 `probe_misc.py` | rc 0 · 16 경우 중 11 = 핀 `92e6cda4d` 와 같음 · 다섯 바뀜 = G2 같은 ID 두 줄 · 다른 TIMESTEP · 잘린 덧줄 (PASS → NOT_COMPUTED · ULPR-03) · G2c 양쪽 열 결손 (FAIL → NOT_COMPUTED · ULPR-04) · 중력 팔 출처 쌍 덤프 열 결손 (G2c FAIL → NOT_COMPUTED · 그 팔 복원 FAIL = TECH 그대로) | 바뀐 다섯 = 이번 수정 대상 그대로 · 나머지 (RESUME 토큰 · Q4 토큰 · Q3 kit 목록 · 양성) 무변경 |

- 화면 · JSON = 증거 폴더 `results/` (사전 리뷰 탐침 둘 · 변이 시험) · `results/codex_probes_pin/` (Codex 탐침 화면 + 요약
  `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/results/codex_probes_pin/summary.json`) · 사전 리뷰가 핀 `92e6cda4d` (와 ULPR-01 탐침은 기준 `eaecfba2a` 도) 에서 낸 결과 = `probes_out/`.

## 1. 결함 ↔ 수정 ↔ 시험

| 원장 | 판정문 최소 해결 | 수정 · 자리 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|
| `ULKRF-01` P2 | 승인 · 소비를 고유 경계와 연결 · 중복 · 상충 RESUME = 사유 있는 거부 · 사건 정리도 같은 규칙 · 정상 재개 양성 유지 | `ul_reader._resume_auth` → (승인, 문제): 러너 `resume_from` step 마다 RESUME 정확히 한 줄 · 둘 이상 (같은 k 중복 · 다른 k 상충) · 사건 ↔ 상태 파일 불일치 · `resume_from` 밖 RESUME = 승인 없음 + 사유 · `read_run` 사건 되감기 = 경계마다 한 번 · 버릴 사건 k > k_r · `_supersede` 소비 = 경계 값 (목록 번호 아님) · `resume_from` 없는 폴더 (UTc) = 승인 · 문제 없음 (부모 경계 규칙 그대로) | `ul_reader` R33 — `one_auth_two_rollbacks` (resume_from 한 줄 · 상태 파일 하나 · 같은 RESUME 두 줄 · 묶음 둘) · `duplicate_event_only` · 같은 step 다른 k = 3 실패 (주 값 OK · UVa 허용) → 3 거부 (사유 `ULKRF-01` · 승인 없음 · 남긴 줄 · 옛 사건 버리지 않음) · 대조 = 진짜 한 번 (승인 하나 · 남긴 줄 3) · `one_event_two_rollbacks` (거부) 그대로 · R28 · R10 · R23 (UTc) · M23 그대로 |
| `ULKRF-02` P2 | 승인된 시도 경계로 새 구간 식별 · 짧음 · 같음 · 김 + 무승인 중복 · 모든 중복 k 삭제 금지 | `_supersede(…, steps_csv)` — 새 시도 시작 = 승인 경계 뒤 먼저 오는 쪽: step 역행 (창 · 단 CSV) 또는 단 CSV 에서 k 가 k_r + 1 로 되돌아옴 (k ≤ 앞 줄 k) · 그 줄 = (k_r + 1 · step > s_r) · 버릴 줄 = s_r 뒤 (k > k_r) · 앞 줄 = (k_r, s_r) · 승인 없는 되돌아옴 = 문제 (미식별) | R34 — 생성 UT 덱 제어 흐름 (`make_unload_decks.deck_sim`) 으로 단 k 2 = 4 · 5 창 (P 0.0010 · 0.0009 · 0.0008 ×3 → S1 [0, 0, 0, 1, 1] · 정상 끝 = 다섯째 창) · 4 → 5 (Codex `resume_completed_hold_5_windows`) = 1 실패 (k [0, 1, 2, 2, 3, 4] 미식별) → 통과 (옛 창 넷 + 단 줄 버림 · 주 값 OK · UVa 허용) · 4 → 4 · 5 → 4 · 새 시도 단독 · 무승인 4 → 5 (= 미식별 그대로) 통과 그대로 |
| `ULKRF-03` P2 | `_contacts` 가 파서 `ok=False` 를 먼저 · g2c FAIL + why · 양쪽 파일 · 실제 restore CLI · 채우기 · 삭제 금지 | `ul_gates._contacts` — `d['ok']` 거짓이면 열을 읽기 전에 돌려준다 → `g2c_compare` 기존 FAIL + 사유 (열 이름 문제) → 복원 = VALUE_MISMATCH (RESTORED 아님 · `prepost` 거짓 · 기존 FAIL 경로) · **10-21 `ULPR-04`**: 그 분류를 관측 결손 NOT_COMPUTED → 복원 UNCONFIRMED 로 바꿈 (아래 행) | `ul_gates` C4 (시험 · 원 쪽 × `c_cpl[7]` · `[8]` = 4 `KeyError` → FAIL + 사유) · `ul_reader` R35 (복원 판정 4 · 다음 제출 UB 거부 · **실제 restore CLI** = rc 1 Traceback → rc 2 · `restore_verdict.json` RESTORED 아님 · G2c FAIL + 사유 · 덤프 바이트 그대로) = 9 실패 → 통과 (10-21: 같은 9 = 기대를 NOT_COMPUTED · UNCONFIRMED 로 고쳐 다시 시험 먼저) |
| `ULPR-01` P2 (10-21 사전 리뷰 PRE-UL-01 · 수정 전 판 `eaecfba2a` 에도 있음) | 승인된 이어 돌림의 새 시도가 단 k_r + 1 줄을 다시 쓰기 전에 끝나면 (TIMEOUT · GUARD · 이동 중 TIMEOUT) 옛 시도의 그 단 줄 · 창 · 사건이 남아 정상 관측으로 쓰인다 — 7:3 UT 주 값 OK ρ 0.2026… · UVa 허용 (같은 꼴 fresh = UNIDENTIFIED · 거부) · 교차 전 단 = 하한 0.225119763714296 → 0.27014371645715524 % (ULKRF-02 네 경우 밖의 다섯째) | `ul_reader._resume_tails` (후보 ① + ② 함께 — 판독기만): **승인 경계 뒤 줄은 어느 시도가 썼는지 기록으로 증명될 때만 쓴다** · 새 시도 증거 = 창 · 단 역행 · 경계 뒤 k ≥ k_r + 2 · RESUME 줄 뒤 사건 (step > s_r) · 요약 · 경계 뒤 단 끝 상태 파일 `state_unload_<s>` (s > s_r) — 없으면 경계 뒤 줄 (옛 시도 · 시도 미확정) 을 쓰지 않음 (②) · 있어도 단 k_r + 1 줄은 새 시도 증명 (그 단 끝 상태 파일 · RESUME 뒤 같은 (k, step) 단 끝 사건 · 남은 창과만 맞음) 일 때만 · 옛 시도 증명 (버린 옛 단 끝 사건 · 버린 옛 창과만 맞음) · 둘 다와 맞음 = 버림 (보수) · 둘 다 증명 · 경계 뒤 옛 사건인데 창 역행 없음 = 모순 (버리지 · 고르지 않고 미식별) · 남은 경계 뒤 단 줄 ↔ 그 단 창 기록 (w 1 … n_windows · 마지막 창 step · ①) · 팔 판정 JSON `resume_tails` (경계마다 새 시도 증거 · 버린 옛 사건 · 버린 줄 · 이유) · 덱 · 러너 · 봉인 덱 무변경 | `ul_reader` R37 19 (7:3 UT · 교차 전 단 · 분리 단 꼴) — 고치기 전 판 (시험 먼저 코드 + 지킴 시험) 12 실패 (A 넷 · B 셋 · 시도 미확정 · 모순 둘 · 손상 옛 기록 · 단 줄 ↔ 창) · 대조 · 양성 7 통과 → 19/19 · 사전 리뷰 탐침 9 경우 = 핀 `92e6cda4d` 넷 어긋남 → 0 · R28 · R33 · R34 · R10 양성 그대로 |
| `ULPR-02` P3 | ULKRF-01 · Q3 가 더한 사유 줄 · 조건 여섯 (`resume_from` 밖 RESUME · k / step 숫자 아님 · 사건 ↔ 상태 파일 불일치 · 되감기 k > k_r · kit `SHA256SUMS` 판독기 줄 대조 · 재판독 rc) 을 하나씩 꺼도 182/182 그대로 | 시험만 (코드 무변경): `ul_reader` R33 넷 · R36 둘 — 사유 글 · 승인 없음 · 주 값 미식별 · 다음 관문 거부를 줄마다 | 여섯 = 고치기 전 · 뒤 둘 다 통과 (지킬 줄이 이미 있음) · 변이 (그 줄 · 조건 하나 지움) 여섯 = 각각 그 시험 하나만 실패 (리뷰 핀 211/212 · §3-2 변이 표) |
| `ULPR-03` P3 | G2 원자 비교 (`ul_gates._dump_tokens` · 복원 · 중력 팔) 가 같은 ID 두 줄 · 다른 TIMESTEP · 잘린 덧줄에도 PASS (README "모든 경로에서 … ID 고유" 와 어긋남 · G2c 를 고친 자리 바로 옆) | `_dump_tokens(path, cols, step)` → (토큰 · 머리 step · 문제): 파서 문제 · 비교 열 · 요청 step · 같은 ID 두 줄 · 비유한 = 문제 → `g2_compare` = NOT_COMPUTED (관측 결손) · 시험 ↔ 원 머리 step 다름 · 빈 덤프 둘 (비교 대상 없음) = NOT_COMPUTED · 같은 부류 = `g2c_compare` 머리 step (시험 ↔ 원 · 요청) · 호출자 = 복원 `step=S0` · 중력 팔 `step=R_M` | `ul_gates` C5 7 (대조 1 + 6 = 고치기 전 6 실패) · `ul_reader` R35 둘 (같은 ID · 두 덤프 머리 S0 − 1,000) · R16 둘 (중력 팔 같은 ID · 두 덤프 머리 R_M − 1) = 고치기 전 4 실패 → 통과 |
| `ULPR-04` P3 (1저자 10-21 Q2) | G2c 열 결손이 VALUE_MISMATCH 로 분류 — 등록 §14-10 = 관측 결손 UNCONFIRMED · 수치 불일치 VALUE_MISMATCH · 기술 실패 SYNTAX_FAIL | `g2c_compare` · `g2_compare`: 파서 · 관측 문제 = NOT_COMPUTED (`OBS_NOTE`) · 집합 · 값 차이 (G2c 의 값이 다른 중복 쌍 키 포함) = FAIL → `restore_verdict` = FAIL 있으면 VALUE_MISMATCH · NOT_COMPUTED 면 UNCONFIRMED (기존 분류 그대로) · 실제 restore CLI = rc 2 · 증서 UNCONFIRMED (다른 UNCONFIRMED 와 같은 종료) · 관문 영향 없음 (RESTORED 아님 그대로) · 중력 팔 = 그대로 TECH (C12) | `ul_gates` C3 둘 · C4 넷 (기대 FAIL → NOT_COMPUTED) + C4 대조 (수치 불일치 = FAIL 그대로) · `ul_reader` R35 다섯 (복원 넷 + 실제 CLI · 기대 VALUE_MISMATCH → UNCONFIRMED) + R35 대조 (법선 힘 −0.5 → −0.6 = VALUE_MISMATCH 그대로) = 고치기 전 11 실패 → 통과 |

## 2. Q2 · Q3 · Q4 (계획 = 권고대로)

| 항목 | 수정 | 시험 |
|---|---|---|
| Q2 (가) 영수증 범위 (동작 변경 없음) | 판정문 권고 문구 그대로 — *"복원 / EXT 증서는 성공 완료 영수증이 필수이며, 일반 팔의 주 관측은 원 폴더에서 재판독한다.  재판독 가능성이 잡의 기술 성공을 뜻하지는 않는다."* — 키트 README §3 · §4 (관문) · 등록 §14-11 ④ · `_job_receipt` 설명 · 규칙 `restore_complete` 글.  "기술 실패 산출물 승인 재사용 0" 전칭 종결을 쓰지 않는다 · (나) (다음 제출에 앞 팔 성공 영수증) 는 채택하지 않음 | 문구 — 기존 R17 · R29 · M20 (RJ · RJ2 · EXT 증서 쪽) 그대로 |
| Q3 문법 사전 점검 원자료 재판독 | `ul_reader.grammar_prereq` ④ `_grammar_reread` — 그 런 kit 사본 (`run_manifest kit=`) 의 `read_history.py` · `history_params.json` sha256 = `GRAMMAR_READER` (= `history_test/SHA256SUMS` 의 그 두 줄 · 그 런 kit `SHA256SUMS` 에도 같은 값) 일 때만 `python3 -I <kit>/read_history.py <런> --grammar --params <kit>/history_params.json --out <임시>` (런 폴더에 쓰지 않는다) → 재판독 status PASS · exit_code 0 · rc 0 · 검사 19 = 판정 JSON (둘 다 참) 이어야 통과 · 판독기가 봉인 값이 아니면 실행하지 않고 거부 · 화면 줄 `reread=` · `reader_sha256=` (러너가 잡 기록 `grammar_line=` 에 남긴다) · 러너 스크립트 sha256 은 대조하지 않는다 | R36 — 양성 (원자료 = 승인된 판독기 자신의 합성기 꼴 · 재판독 PASS · 판독기 sha256 기록) · Codex 변조 넷 (GA 화면 ERROR · GB 첫 mesh z 99 · GB 화면 지움 · GB 마지막 상태 값 0 — 판정 JSON 그대로) · 판독기 셋 (kit 사본 판독기 고침 + kit SUMS · sums_sha256 맞춤 = Codex `different_reader_runner_seal` · 표 고침 · 판독기 없음) · 봉인 값 = 실제 파일 = `history_test/SHA256SUMS` = 9 실패 → 통과 · M25 (실제 러너 — M22 양성 판정 그대로 · 그 런 GA 화면 ERROR → RJ 의 LIGGGHTS 전 거부 · 호출 0 · RJ 폴더 없음) 1 실패 → 통과 · M22 양성 (지금 history_test 러너 + 읽는 쪽이 낸 판정) = 재판독 PASS 로 그대로 · (10-21 `ULPR-02`) kit `SHA256SUMS` 판독기 줄 대조 · 재판독 프로세스 rc 대조 = R36 둘이 줄마다 지킨다 (변이 = 그 시험만 실패) |
| Q4 비차단 셋 | ① `ul_lib.read_dump` — ID 열 (`id` · `c_cpl[7]` · `c_cpl[8]`) 정수 토큰 = float 없이 정확한 int → `exact_id` 가 그대로 대조 (`9007199254740993` 거부 · 정상 ID 그대로) · 소수 꼴 토큰이 float 로 정수로 가려지면 (`2.0000000000000001`) 파서 문제 ② 등록 §14-9 "지금 절차 · 강제하지 않는다" 아래 정정 줄 (지금 = 자동 사전 점검 + 원자료 재판독) ③ EXT rc 2 = PASS 아닌 모든 s0p 판정 (조건 미달 · 미계산 · 체크포인트 없음 — 물리 측정 실패만이 아니다) — README §3 · 등록 §14-11 ⑤ · 러너 주석 · 규칙 `stage_rc` 글 ④ R32 fixture 줄바꿈 무관 (`_w` LF 고정 쓰기) | `ul_lib` L14 (2^53 + 1 · 쌍 참조 · 긴 토큰) 2 실패 → 통과 · ④ = Linux 에서는 바이트 그대로라 판별 시험 없음 (Windows 에서 R32 양성이 다시 서는지 = 확인 부탁) |

**판단 범위 · 한정**: 재판독은 그 런 폴더가 **원래 자리** 일 때 뜻이 있다 (GA · GB 입력 기록 `ckpt.txt` · `vars.txt` = 절대 경로 — 옮긴 사본은 GA_args · GB_args 가 거짓) ·
실행 2 는 판독기 · 표가 봉인 값인 판 (`b1121b6b6` 이후 — 그 뒤 두 파일 바이트 그대로) 으로 돌린다 (`039abb141` 판독기 sha256 `18521ae7…` ≠ 봉인 `70f741a9…` → 그 판으로 낸 런은 거부 · 덱 같음) ·
문법 PASS = 기술 · 문법 검사이지 물리 검증이 아니다 (C19).
Q3 재판독은 그 런 kit 사본에 판독기 · 표 두 파일이 있어야 돈다 (러너 `run_history.sh` 는 둘을 싣는다) — Codex `grammar_provenance.py` 처럼 `SHA256SUMS` 만 둔 합성 사본이면 양성도 거부된다 (§0 탐침 안내).
`ULPR-01` 근거 = 덱 · 러너 소스의 쓰는 순서 (창 줄 → 단 줄 → 단 끝 사건 → `restart_unload` → 상태 파일 · UT R_M 단 = `restart_RM` · `state_RM` 만) + 러너 이어 돌림 = 마지막 `restart_unload_*` + 짝 상태 파일 (`run_unload.sh` · 덱 요약이 있으면 이어 돌리지 않는다) — 합성 기록 시험 · 실제 LIGGGHTS 재개로는 확인하지 않았다.

## 3. Linux 전체 로그

### 3-1. 10-21 갱신판 — `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/`

| 명령 (`python3 -I …` · 키트 폴더) | 리뷰 핀 `28b66e116` (`final/`) | 기준 `286a8d562` (`logs/base_286a8d562/` · 키트 = 10-15 판 그대로) | 시험 먼저 `f1b911f76` (`logs/st_tests_first/`) |
|---|---|---|---|
| `ul_lib` · `ul_s3` · `ul_observers` · `ul_gates` `--selftest` | rc 0 · 24 · 16 · 21 · 49 | rc 0 · 24 · 16 · 21 · 41 | `ul_gates` rc 1 · 37/49 (12 실패 = C5 6 · C3 2 · C4 4) · 나머지 셋 그대로 |
| `ul_reader.py --selftest` | rc 0 · 212/212 | rc 0 · 182/182 | rc 1 · 190/207 (17 실패 = R37 10 · R35 6 · R16 1) |
| `seal_kit.py --selftest` · `--check` | rc 0 (12) · rc 0 (76 파일 · 규칙 24 · 폐기 0) | 같음 | `--check` rc 0 (시험 먼저 커밋도 봉인을 다시 썼다) |
| `make_unload_decks.py --selftest` · `--check` | rc 0 (291) · rc 0 (덱 64) | 같음 | `--check` rc 0 (덱 64) |
| `history_test/make_history_decks.py --selftest` · `--check` | rc 0 (172) · rc 0 (덱 9 · 15 파일) | 같음 | `--check` rc 0 |
| `history_test/read_history.py --selftest` | rc 0 · 56/56 | 같음 | — (무변경) |
| `ul_runner_test.py --selftest` | rc 0 · 38/38 | 같음 | — (무변경) |

- 사이 판 (`logs/`): `ULPR-01` `55fff3eb1` = `ul_reader` 200/207 (7 실패 = R35 6 · R16 1 — ULPR-03 · 04 몫) · `ul_gates` 37/49 그대로 / `ULPR-03` · `04` `2932b63bc` = 207/207 · 49/49 /
  지킴 시험 첫째 `c21b1a051` = 210/210 / **고치기 전 판 + 지킴 시험 다섯** (`logs/prefix_guards/` — 시험 먼저 커밋 코드에 뒤 두 커밋의 시험만 얹은 사본) = `ul_reader` 191/212 (21 실패 = 시험 먼저 17 + 지킴 넷 · 지킴 하나 = 양성이라 고치기 전에도 통과).
- `final/` = 10-15 도구 `docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/tools/run_suite.py` 출력 (`summary.json` = 키트 폴더 git tree `d4628ce0…` = 리뷰 핀의 키트 트리 · 봉인 sha256 ·
  더러운 경로 = README 하나 (문서 커밋 전 · 봉인 밖)) · 다른 판 = 커밋마다 git archive 사본에서 같은 명령 (`logs/*/` · 목록 = `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/logs/index.json`).
- 변이 시험 (리뷰 핀 사본 · 한 줄씩) = §3-2 · 사전 리뷰 탐침 둘 + Codex 탐침 = §0 탐침 안내 — 결과 JSON · 화면 = 증거 폴더 `results/`.
- 환경 = Linux · Python 3.11.15 · GNU bash 5.2.21 · LIGGGHTS 없음 (가짜 `mpirun` · `lmp`).

### 3-2. 변이 시험 (10-21 · 리뷰 핀 사본 · 한 줄씩 · `docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/results/mutations_final.json`)

고친 줄 하나를 되돌리거나 끈 사본마다 해당 자체시험을 돌렸다 — 바꿀 글자가 그 파일에 정확히 한 번 · 그 파일 봉인 줄만 다시 계산 · 표적 시험 (이름 앞부분) 이 실패하고 대조 시험은 통과해야 '기대대로'.

| 묶음 | 변이 | 결과 (리뷰 핀) |
|---|---|---|
| `ULPR-02` 사유 줄 · 조건 여섯 | `resume_from` 밖 RESUME 사유 · k / step 숫자 아님 사유 · 사건 ↔ 상태 파일 불일치 사유 · 되감기 k > k_r 조건 · kit `SHA256SUMS` 판독기 줄 대조 · 재판독 rc 대조 — 각각 지움 | 여섯 다 `ul_reader` 211/212 (그 줄을 지키는 시험 하나만 실패) |
| `ULPR-01` 가지 열 | 증거 없을 때 버림 끔 · 옛 단 끝 사건 증명 끔 · 옛 · 새 둘 다와 맞음을 남김 · 옛 창과만 맞음 버림 끔 · 단 줄 ↔ 창 대조 끔 · 상태 파일 증거 끔 · 새 단 끝 사건 증명 끔 · 뒤 단 증거 끔 · 창 역행 없음 모순 끔 · 규칙 전체 끔 | 열 다 실패 — 209/212 하나 · 200/212 하나 (전체 끔 = R37 12) · 나머지 여덟 211/212 |
| `ULPR-03` 다섯 | G2 같은 ID 검사 · G2 요청 step · G2 시험 ↔ 원 머리 step · 빈 덤프 둘 · G2c 시험 ↔ 원 머리 step — 각각 끔 | 다섯 다 `ul_gates` 48/49 (같은 ID · 요청 step 은 `ul_reader` 210/212 도) |
| `ULPR-04` 둘 | G2c · G2 관측 결손을 옛 FAIL 로 | `ul_gates` 42/49 · 43/49 + `ul_reader` 207/212 · 208/212 |
| 호출자 둘 | 복원 `g2_compare(…, step=s0)` · 중력 팔 `step=rm` 인자 지움 | 둘 다 `ul_reader` 211/212 |
| 합계 | 25 | **25 실패 · 25 기대대로** |

- 첫 변이 판 (`c21b1a051` 사본 · 같은 25) 에서는 둘이 살아남았다 — 모순 규칙 (그 규칙의 시험이 옛 RM 사건이 새 단 줄과 같은 (k, step) 이라 '둘 다 증명' 모순으로도 걸렸다) ·
  복원 쪽 step 인자 (S0 프레임 머리 검사가 복원 판정을 이미 UNCONFIRMED 로 만들고 G2 상태를 지키는 시험이 없었다) → 지킴 시험 둘 (`28b66e116` · 고치기 전 판에서 둘 다 실패) → 위 표.

### 3-3. 10-15 첫 판 — `docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/`

| 명령 (`python3 -I …` · 키트 폴더) | 최종 (`final/` · 깨끗) | 시험 먼저 (`tests_first/` · 깨끗) |
|---|---|---|
| `ul_lib` · `ul_s3` · `ul_observers` · `ul_gates` `--selftest` | rc 0 · 24 · 16 · 21 · 41 | rc 1 · 0 · 0 · 1 (2 · 0 · 0 · 4 실패) |
| `ul_reader.py --selftest` | rc 0 · 182/182 | rc 1 · 18 실패 (옛 158 통과) |
| `seal_kit.py --selftest` · `--check` | rc 0 · rc 0 (76 파일 · 규칙 24 · 폐기 0) | 같음 |
| `make_unload_decks.py --selftest` · `--check` | rc 0 (291) · rc 0 (덱 64) | 같음 |
| `history_test/make_history_decks.py --selftest` · `--check` | rc 0 (172) · rc 0 (덱 9 · 15 파일) | 같음 |
| `history_test/read_history.py --selftest` | rc 0 · 56/56 | 같음 |
| `ul_runner_test.py --selftest` | rc 0 · 38/38 | rc 1 · 1 실패 (M25) |

- 환경 = Linux · Python 3.11.15 · GNU bash 5.2.21 · LIGGGHTS 없음 (가짜 `mpirun` · `lmp`).  로그를 낸 판 = 작업 트리 판 · 키트 폴더 내용 = 시험 먼저 `1c0b9fd65` · 리뷰 핀 (최종) 과 같다 (메인 세션 대조) —
  대응 확인 = 각 `summary.json` 의 키트 폴더 git tree (내용 해시) · 봉인 sha256 (증거 README §2).
- 봉인: 최종 키트 `SHA256SUMS` sha256 `441f66d71873faf2541f3d3945e82cb2b8045425eaa3b2c5bb63213327556c34` · `history_test/SHA256SUMS` `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d`.
- 시험 쪽 바꾼 것 (문법 런 fixture · `_w` LF · `_resume_layout` 인자) = 증거 README §4.

## 4. 명령 (Linux · 리뷰 핀 체크아웃 뒤)

```bash
K=docs/data/ps45_unload_20261009
for m in ul_lib ul_s3 ul_observers ul_gates ul_reader; do python3 -I $K/$m.py --selftest | tail -1; done   # 24 · 16 · 21 · 49 · 212 — 전부 PASS (10-15 판 = 41 · 182)
python3 -I $K/seal_kit.py --selftest | tail -1 && python3 -I $K/seal_kit.py --check                        # 76 파일 · 규칙 24 · 폐기 0
python3 -I $K/make_unload_decks.py --selftest | tail -1 && python3 -I $K/make_unload_decks.py --check       # 291 · 덱 64
python3 -I $K/history_test/make_history_decks.py --selftest | tail -1 && python3 -I $K/history_test/make_history_decks.py --check
python3 -I $K/history_test/read_history.py --selftest | tail -1                                           # 56 / 56
python3 -I $K/ul_runner_test.py --selftest | tail -1                                                      # 38 / 38 (bash 필요)
python3 docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/tools/run_suite.py $K /tmp/ulkrf_suite   # 13 명령 전부 · 로그 · rc
E=docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021                                         # 10-21 사전 리뷰 탐침 (리포에 쓰지 않는다 · 임시 = TMPDIR)
python3 -I -B $E/probe_resume_unfinished.py $K /tmp/pre_ul01.json   # ULPR-01 반례 9 경우 — failed_expectations []
python3 -I -B $E/probe_misc.py $K /tmp/probe_misc.json              # RESUME 토큰 · G2 · G2c · 중력 팔 · Q4 토큰 · Q3 kit 목록 16 경우
```

## 5. 묻는 것

| Q | 무엇 |
|---|---|
| Q1 | `ULKRF-01` — "경계 하나에 승인 한 번" (같은 경계 RESUME 둘 이상 = 승인 없음 · 사건 ↔ 상태 파일 불일치 · `resume_from` 밖 RESUME = 상충) 이 판정문 §4 최소 해결을 채우는가 · 중복을 하나로 줄여 승인하지 않고 **승인 자체를 거두는** 선택 (애매한 증거 = 버리지 않는다) 이 맞는가 |
| Q2 | `ULKRF-02` — 새 시도 시작 = step 역행 (창 · 단) 또는 단 기록 k 되돌아옴 (먼저 오는 쪽) 이 짧음 · 같음 · 김 · 무승인을 다 가르는가 · 창 기록은 step 역행만으로 충분한가 (덱이 같은 단의 창 끝을 같은 step 에 쓴다 — 새 시도 첫 창 = 옛 시도 첫 창 step) |
| Q3 | `ULKRF-03` — G2c 열 결손 = 기존 FAIL 경로 (복원 VALUE_MISMATCH) 로 충분한가 · 관측 결손이라 UNCONFIRMED 로 나눠야 하는가 (지금은 G2c 의 다른 파서 문제 — 소수 쌍 참조 등 — 와 같은 FAIL) → **10-21 답을 정함 (`ULPR-04` · 1저자 Q2)**: G2 · G2c 의 파서 · 관측 문제 = NOT_COMPUTED → 복원 UNCONFIRMED (등록 §14-10) · 값 차이만 FAIL → VALUE_MISMATCH — 이 분류에 이의 없는가 |
| Q4 | Q3 재판독 — 승인된 판독기 = 그 런 kit 사본의 두 파일이 봉인 값일 때만 (이 키트의 봉인 kit 사본은 `history_test` 를 싣지 않는다 — 봉인 K1) 이 판정문 Q4 "승인된 판독기로 raw 자료를 다시 읽어야" 를 채우는가 · 원래 자리 한정 · 판독기 판 한정 (`b1121b6b6` 이후) 이 실행 2 에 부담 · 틈이 없는가 |
| Q5 | Q2 문구 · Q4 비차단 셋 (정수 토큰 · §14-9 정정 · EXT rc 2 범위 · LF fixture) 이 판정문 §5 · §6 의 요구를 채우는가 · Windows 에서 R32 양성이 이제 서는가 |
| Q6 | 남은 해제 조건 = ibb 실행 2 의 원 보고 묶음 (같은 바이너리 · 승인된 덱 · 판독기 · 원자료 재판독 PASS) 인가 |
| Q8 (10-21) | `ULPR-01` — "승인 경계 뒤 줄 = 어느 시도가 썼는지 기록으로 증명될 때만" 이 다섯째 경우 (새 시도가 단 k_r + 1 줄을 다시 쓰기 전에 끝남 · TIMEOUT · GUARD · 이동 중) 를 닫는가 · 새 시도 증거 목록 (창 · 단 역행 · 경계 뒤 k ≥ k_r + 2 · RESUME 줄 뒤 사건 · 요약 · 경계 뒤 `state_unload_<s>`) 이 덱 · 러너의 쓰는 순서에서 옛 시도가 만들 수 없는 것들인가 · 시도 미확정 = 버림 (보수) 의 대가 (새 시도가 단 줄 → 단 끝 restart 사이에서 끊긴 드문 경우 그 단 줄도 버림 · 주 값 미식별 · 하한은 낮은 쪽으로만) 를 받아들일 수 있는가 · 덱에 시도 표지를 넣는 근본 해결 (생산 덱 64 · 봉인 바뀜) 을 이번 범위 밖에 둔 것이 맞는가 |
| Q9 (10-21) | `ULPR-03` — G2 원자 비교도 관측 파싱 규칙 (같은 ID 두 줄 · 다른 TIMESTEP · 잘린 덧줄 · NaN = 관측 결손 · 빈 덤프 둘 = 비교 대상 없음 · 요청 step 결합 · G2c 머리 step 도) → 복원 UNCONFIRMED · 중력 팔 TECH 가 README 의 "모든 경로에서 … ID 고유" 를 채우는가 · 시험 ↔ 원 머리 step 이 서로 같아도 요청 step 과 다르면 거부하는 것이 맞는가 |
| Q10 (10-21) | 정수 반올림 (기록 CSV 의 k · w · step · n_windows 소수 토큰 · Codex `fractional_resume_event_k` · `fractional_confirmation_k`) 을 이번에도 열어 둔 것 (판정문 §6 관찰) 에 이의 없는가 — `ULPR-01` 의 단 줄 ↔ 창 대조도 같은 반올림 값을 쓴다 |

## 6. 남은 것

- ✅ ibb 문법 fixture **실행 2 = PASS** (§7 · 10-15) — 원 보고 묶음 반입 · 승인된 판독기로 원자료 재판독 기록 → 그 `grammar_verdict.json` 이
  RJ · RJ2 · EXT 의 `GRAMMAR_VERDICT` (사전 점검이 그 런 폴더를 원래 자리에서 다시 읽는다).
- 원장 `ULKRF-01` · `02` · `03` → claimed_fixed (수정 `22a347722` · 원장 커밋 `44a034534`).
- (10-21) 원장 `ULPR-01`–`04` → claimed_fixed = 메인 세션 (이 갱신 가지는 원장을 고치지 않았다) · 수정 `55fff3eb1` · `2932b63bc` · 지킴 시험 `c21b1a051` · `28b66e116`.
  10-21 판독기 수정은 문법 사전 점검 (`grammar_prereq`) 코드를 바꾸지 않았다 → 실행 2 판정 · 그 원자료 재판독 결과는 그대로 쓴다 (§7).
- ⛔ 본 R · 10:0 연장 · U = 이 재확인 GO 뒤 (실행 2 PASS = ✅ 10-15).

## 7. 실행 2 결과 (10-15 · 1저자 ibb · 반입 = `docs/reviews/dem_unloading_grammar_fixture_runs_20261015/`)

| 런 | job · 시각 (KST) | 판 | history_test 봉인 | 판독기 | 단계 rc | 판정 |
|---|---|---|---|---|---|---|
| **실행 2** `gram_20261015_030225` | 285533 · 10-15 03:02 | `799459c85` | `8ff722d2…` | `70f741a9…` (= `GRAMMAR_READER`) | P 0 · GA 0 · GB 0 | **PASS · 19/19** |
| 반복 `gram_20261015_122956` | 286802 · 10-15 12:29 | `44a034534` | `8ff722d2…` | `70f741a9…` | P 0 · GA 0 · GB 0 | **PASS · 19/19** |
| 실행 1 · 1b (`192604` · `194645`) | 285220 · 285228 · 10-14 | `a30fe150e` | `debe8387…` | `18521ae7…` | P 0 · GA 1 | FAIL — `SELF-115` 결함 (1b = 같은 판 반복 · 이 반입으로 처음 기록) |

- LIGGGHTS sha256 = 넷 모두 `ee2d77261bac…` (등록 §11-1 ⓖ) · 덱 사본 (P · GA · GB) · 판 STL = `GRAMMAR_INPUTS` 봉인 값 · 표 `history_params.json` = 봉인 값 · 묶음 sha256 = 각 SLURM 화면의 "보낼 것" 값 (반입 README §1).
- **우리 트리 판독기 재판독** (리포 `read_history.py` · sha256 `70f741a9…`): 런의 절대 경로를 컨테이너에 새로 만들어 원래 자리에서 읽음 = 실행 2 · 반복 모두 **PASS · rc 0 · 검사 19 = 런 JSON 과 같음** · 옮긴 사본 = `GA_args` · `GB_args` 만 거짓 (입력 기록 절대 경로 — §2 의 "원래 자리 한정" 그대로) · 실행 1 · 1b = `Mismatched fix` 재현.  본 R 사전 점검의 kit 사본 판독기 재판독은 ibb 에서 (묶음에 kit 스크립트 없음).
- `GRAMMAR_VERDICT` 권고 = 실행 2 런 (`~/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json` · 첫 PASS) · 반복도 같은 판정 · ✅ 1저자 10-15 = 실행 2 런 (`4b1d67f62`).

| Q | 질문 |
|---|---|
| Q7 | 이 반입 (같은 바이너리 · 승인된 덱 · 판독기 출처 · 원래 자리 원자료 재판독 PASS) 으로 `ULKRR-01` 의 실행 부분 (판정문 10-15 "코드 닫힘 / 실행 열림") 이 닫히는가 · 실행 2 를 `GRAMMAR_VERDICT` 로 고정하는 데 이의 없는가 |

