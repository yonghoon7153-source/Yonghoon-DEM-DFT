# DEM 언로딩 키트 수정 재확인 2 — Codex 발송 전 사전 공격 리뷰

검토일 2026-10-21 · 리뷰 핀 `92e6cda4d` (키트 폴더 · 등록 · 요청서 = `a76f59d0d` 까지 바이트 같음 — 직접 확인) · 기준 `eaecfba2a` (Codex 판정문 코드 핀)
대상 = 요청서 `docs/reviews/codex_dem_unloading_kit_fix_recheck2_request_20261015.md` (발송본 = 핀 채운 사본 `send_unload/…_SEND.md`)
방법 = 공통 지침 (`prereview_common.md`) — 코드 · 내 실행만 믿음 · 보장마다 작은 반례 · 변이 시험 · Codex 형식.  리포에 쓰지 않음 (작업 트리 = 핀 · 바뀐 파일 0 · 실행은 scratch 거울 사본).

## 0. 한 줄 결론

**그대로 보내지 말고 고친 뒤 보내기 — 새 P2 하나 (PRE-UL-01).**
요청서의 숫자 · 해시 · 시험 수 · 커밋 순서는 전부 맞다 (§4).  ULKRF-01 · 03 · Q3 · Q4 수정은 Codex 반례를 **옳은 이유로** 닫는다 (Codex 탐침 재실행 · 변이 시험 §5 · §6).
그러나 ULKRF-02 와 **같은 보장** (승인된 이어 돌림에서 끊긴 시도의 줄을 버림 · 새 시도 시작 식별) 에 새 반례가 있다: 새 시도가 단 k_r + 1 줄을 **다시 쓰기 전에** 끝나면 (TIMEOUT · GUARD · 이동 중 TIMEOUT)
옛 시도의 단 줄이 남아 정상 관측으로 쓰이고 **primary OK · ρ 0.2026077873428664 % · UVa ALLOW** 가 난다 — 같은 꼴 fresh 는 UNIDENTIFIED · 거부.
수정 전 (`eaecfba2a`) 에도 같은 결과라 이번 수정이 만든 것은 아니지만, 요청서 Q2 가 Codex 에 "짧음 · 같음 · 김 · 무승인을 다 가르는가" 를 묻는 바로 그 보장의 다섯째 경우 (**"없음"** — 새 시도가 그 단을 못 끝냄) 라서
Codex 가 같은 탐침 계열 (`resume_recheck.py`) 로 찾을 가능성이 높다 → ULKRF-02 재개방 = HOLD.

## 1. 권고

| 선택 | 내용 | 판단 |
|---|---|---|
| **권고** | PRE-UL-01 고침 (반례 먼저 · 판독기만 · 덱 · 봉인 표 · 물리 값 그대로) + PRE-UL-02 시험 넷 다섯 + 요청서 머리에 '이번에 닫는 것 / 닫지 않는 것' (§9) · Codex 탐침 재실행 안내 (PRE-UL-05) · Q3 근거 (PRE-UL-04) | 고친 범위가 작다 (판독기 한 함수 + 시험) · 실행 2 · 봉인 덱 64 · 이력 시험 폴더 무영향 (추정 — 판독기만 바뀜) |
| 대안 | 고치지 않고 보낼 때 = PRE-UL-01 을 '닫지 않는 것' 에 반례 숫자와 함께 적는다 | ULKRF-02 범위의 P2 라 Codex HOLD 가능성 높음 — 2 주째 HOLD 회차를 하나 더 쓰게 됨 |
| 하지 않을 것 | 덱 (64 생산 덱) 에 시도 표지를 넣는 근본 해결 | 봉인 덱 바뀜 → 재봉인 · 재검토 범위 큼 · 이번 회차 밖 |

## 2. 보장 목록 · 반례 · 결과

| # | 보장 (요청서 · 코드가 내세움) | 자리 | 작은 반례 | 결과 |
|---|---|---|---|---|
| G1 | 경계 하나에 승인 한 번 — 같은 경계 RESUME 둘 이상 = 승인 없음 + 사유 | `ul_reader.py:116–154` | Codex `one_auth_two_rollbacks` · `duplicate_event_only` · 같은 step 다른 k | ✅ 거부 (R33 · Codex 탐침 재실행 · 변이 = 중복 검사 지우면 R33 셋 실패) |
| G2 | `resume_from` 밖 RESUME = 승인 없음 + 사유 | `:138–139` | R1c (resume_from 3270000 · RESUME 3269999 덧붙임) | ✅ 거부 (내 탐침) · ⚠ **시험 없음** (변이 생존 — PRE-UL-02) |
| G3 | RESUME k · step 숫자 아님 = 승인 없음 + 사유 | `:136–137` | R1d (`RESUME,x,s_r`) | ✅ 거부 (내 탐침) · ⚠ 시험 없음 (변이 생존) |
| G4 | 사건 ↔ 상태 파일 불일치 = 상충 사유 | `:148–153` | R28 ev_k · state_k | ✅ 거부 — 단 R28 은 `_supersede` 의 ULKRR-02 사유로 통과 → 이 사유 줄은 시험 없음 (변이 생존) |
| G5 | 사건 되감기 = 경계마다 한 번 · 버릴 사건 k > k_r | `:224–235` | 승인 경계 뒤 k ≤ k_r 사건 | 코드 확인 · ⚠ k 조건 시험 없음 (변이 생존) |
| G6 | 새 시도 시작 = step 역행 또는 (단 CSV) k 되돌아옴 — 먼저 오는 쪽 · 짧음 · 같음 · 김 | `:157–190` | R34 4→5 · 4→4 · 5→4 · Codex `resume_completed_hold_5_windows` | ✅ (R34 · Codex 탐침 재실행 · 변이 = kback 끄면 R34 4→5 만 실패) |
| **G7** | **끊긴 시도가 남긴 줄 = 승인 경계에서 버림 · 버린 행을 정상 관측으로 쓰지 않는다 (README §5 이어 돌림 경계 · 등록 §14-10 · §14-11 ①)** | `:157–190` · `:224–235` | **새 시도가 단 k_r + 1 줄을 쓰기 전에 끝남** (TIMEOUT · GUARD · 이동 중 TIMEOUT) | ❌ **PRE-UL-01** — 옛 단 줄 생존 → OK · UVa ALLOW |
| G8 | G2c 필수 열 결손 = 예외 없이 FAIL + 사유 (양쪽 · 실제 CLI) | `ul_gates.py:252–274` | `c_cpl[7]` · `[8]` → `not_…` (시험 · 원 · 둘 다) · 중력 팔 `_g_restore` | ✅ (C4 · R35 · 내 탐침 — 양쪽 결손 FAIL · 중력 팔 G2c FAIL → `_g_restore` FAIL · 예외 없음) · 분류는 PRE-UL-04 |
| G9 | 관측 파싱 "모든 경로에서 … 머리 step · 행 수 · ID 고유" (README §5) | `ul_gates.py:215–240` (`_dump_tokens` · `g2_compare`) | G2 시험 덤프에 같은 ID 두 줄 (첫 줄 x 다름) · TIMESTEP 9999999 · 열 수 다른 덧줄 | ⚠ 셋 다 G2 PASS — **PRE-UL-03** (P3 · 고친 G2c 의 옆 자리) |
| G10 | 문법 사전 점검 = 승인된 판독기로 원자료 재판독 · 봉인 밖 판독기 = 실행 안 함 | `ul_reader.py:1262–1388` | R36 넷 · Codex `grammar_provenance` (kit 사본에 판독기 넣은 판) · kit SHA256SUMS 판독기 줄만 다름 (Q3a) | ✅ 변조 넷 = 재판독 FAIL 로 거부 · 봉인 밖 = 실행 안 함 · 목록 불일치 거부 · ⚠ 목록 대조 · rc 대조 줄 시험 없음 (변이 생존) |
| G11 | ID 열 정수 토큰 = float 없이 정확한 int (2^53 + 1 거부 · 가려진 비정수 = 파서 문제) | `ul_lib.py:316–405` | `9007199254740993` · `…993.0` · `2.0000000000000001` · 아랍 숫자 2^53+1 · `0x10` · `nan` · `-1` · `0` | ✅ 전부 거부 (토큰 17 표 · `probes_out/probe_misc_pin.json`) · 변이 둘 다 L14 실패 |
| G12 | 실행 2 = PASS 19/19 · 같은 LMP · 봉인 판독기 · 원래 자리 재판독 = JSON | 반입 폴더 | 묶음 해시 · 멤버 · 판정 · 경로 바꾼 '원래 자리' 모의 + `grammar_prereq` | ✅ 모의 재판독 PASS · 검사 19 = JSON · **`grammar_prereq` 전체 PASS** (§6) · 옮긴 사본 = GA_args · GB_args 만 거짓 |

## 3. 결함 표 (Codex 형식)

### PRE-UL-01 · P2 · 새 시도가 단 k_r + 1 을 끝내지 못하면 옛 시도의 단 줄이 정상 관측으로 남는다

**자리:** `ul_reader.py:157–190` (`_supersede` — 새 시도 시작을 **그 CSV 안의 첫 새 줄** 로만 식별) · `:224–235` (사건 되감기는 RESUME 위치로 옛 사건을 버림) · 덱 순서 `decks/ps_7_3_r45/in.UT.liggghts:267` (단 줄) → `:298` (RM 사건) → `:299–311` (restart_RM · 상태 · `ul_rm` 은 `restart_unload` 를 쓰지 않음) · 러너 `run_unload.sh:267` (재개 = 마지막 `restart_unload_*`).

**반례 (합성 · 판독기 실제 함수 사슬 · `probe_resume_unfinished.py`):** 7:3 UT 사다리 (교차 k2 · 확인 k3 · k4 · RM k4).  옛 시도 = k4 유지 4 창 · k4 단 줄 · RM 사건까지 쓴 뒤 요약 전에 끊김 →
마지막 `restart_unload` = k3 끝 3,350,000 → 러너 RESUME (k 3 · 3,350,000) · `resume_from` · 상태 파일 (승인 정상) → 새 시도가 k4 창 둘을 쓴 뒤 끝남.

| 경우 | 기대 (fresh 같은 꼴) | 핀 `92e6cda4d` | 기준 `eaecfba2a` |
|---|---|---|---|
| A1 fresh · k4 유지 중 TIMEOUT | UNIDENTIFIED (확인 단 2 없음) · UVa 거부 | UNIDENTIFIED · 거부 | 같음 |
| **A2 재개 · k4 창 둘 뒤 TIMEOUT** | A1 과 같음 | **OK · ρ 0.2026077873428664 % · 단 k [0,1,2,3,4] · 버린 줄 4 (창만) · UVa ALLOW** | 같음 |
| A3 fresh · k4 GUARD | UNIDENTIFIED · 거부 | UNIDENTIFIED · 거부 | 같음 |
| **A4 재개 · k4 GUARD** (요약 GUARD) | A3 과 같음 | **OK · UVa ALLOW** (GUARD 가 난 시도인데 옛 k4 줄로 확인 단 2 충족) | 같음 |
| **A5 재개 · k4 이동 중 TIMEOUT** (새 창 없음) | UNIDENTIFIED | **OK · 버린 줄 0 · UVa ALLOW** (옛 k4 창 넷 + 단 줄 그대로 · 옛 RM 사건만 버려짐) | 같음 |
| B1 fresh · 교차 전 k3 TIMEOUT | LOWER_BOUND 0.225119763714296 % | 같음 | 같음 |
| **B2 재개 · k3 창 둘 뒤 TIMEOUT** | B1 과 같음 | LOWER_BOUND **0.27014371645715524 %** (옛 k3 줄로 하한이 커짐 · 관문 무영향) | 같음 |

같은 폴더 안에서 사건 기록은 옛 시도 사건을 버리고 (RM 사라짐 → UTc · G_UT3 관문은 닫힘) 창 기록은 새 시도로 바뀌었는데 단 기록만 옛 시도 줄을 쓴다 — 확인 단 2 의 "등록 정상 완료" (등록 §14-1) 를 끊긴 시도 줄이 채운다.
⚠ 실제 LIGGGHTS 재개에서 난 것이 아니다 (합성 · 덱 · 러너 순서로 근거).  두 실패가 겹쳐야 한다 (옛 시도가 R_M 단 줄 뒤 · 요약 전 끊김 + 새 시도가 그 단 안에서 끝남) — 각각은 정상 실패 꼴 (변조 없음).

**최소 해결 (후보 · 설계 검토 — 시험 안 함):**
① **단 줄 ↔ 그 단 창 기록 결합** — 남은 단 줄마다 `n_windows` = 남은 같은 k 창 수 · 단 step = 그 k 마지막 창 step (덱 `:229` · `:267` 이 같은 `ul_w` · `ul_step` 을 쓴다) · 아니면 문제 → A2 · A4 · B2 거부.
② **버린 옛 사건이 있는 승인 경계** — RESUME 되감기에서 버린 사건 (step > s_r) 이 있으면 그 사건 step 까지의 창 · 단 줄 중 **그 CSV 에서 새 시도 시작이 식별되지 않은 줄** 은 옛 시도 줄 → 버림 (또는 미식별) → A5 거부 (R_M 단은 늘 RM 사건이 단 줄 바로 뒤).
③ 남는 모호 (옛 사건 없음 · 새 창 없음 — 사건 없는 SEARCH · 확인 1 단) 는 확인 단 2 가 비어 주 값 OK 로 가지 않음 (추정) — 요청서 '닫지 않는 것' 에 한정으로 적는다.
시험 = A1–A5 · B1 · B2 꼴 (TIMEOUT · GUARD · 이동 중 TIMEOUT · 무사건 단) + 기존 양성 (R33 대조 · R34 넷 · R28 · R23 UTc) 그대로.  ⚠ ① 은 분리 · 재접촉 · UTc · 중력 팔 덱 경로에서 단 줄 n_windows ↔ 창 수가 늘 같은지 먼저 확인.

**재현:** `bash run_probe.sh probe_resume_unfinished.py m_pin/docs/data/ps45_unload_20261009 probes_out/pre_ul01_pin.json` (기준 = `m_base/…` · 결과 `probes_out/pre_ul01_{pin,base_eaecfba2a}.json`).

### PRE-UL-02 · P3 · 수정이 더한 사유 줄 · 조건 다섯이 시험 없다 (변이 생존)

| 변이 (고친 줄 하나를 끔) | 자체시험 결과 | 요청서 · README 주장 |
|---|---|---|
| `resume_from` 밖 RESUME 사유 삭제 | 182/182 그대로 | §1 "resume_from 밖 RESUME = 승인 없음 + 사유" |
| RESUME k · step 숫자 아님 사유 삭제 | 182/182 | README "k · step 숫자 아님 = 승인 없음 + 사유" |
| 사건 ↔ 상태 파일 불일치 사유 삭제 | 182/182 (R28 은 `_supersede` ULKRR-02 사유로 통과) | §1 "사건 ↔ 상태 파일 불일치" |
| 사건 되감기 `버릴 사건 k > k_r` 조건 삭제 | 182/182 | §1 "버릴 사건 k > k_r" |
| `_grammar_reread` kit SHA256SUMS 판독기 줄 대조 (`listed`) 삭제 | 182/182 | §2 Q3 "그 런 kit SHA256SUMS 에도 같은 값일 때만" |
| `_grammar_reread` 프로세스 rc ≠ 0 조건 삭제 | 182/182 | §2 Q3 "rc 0" |

동작은 맞다 (내 탐침 R1c · R1d · Q3a 가 거부 확인 · Codex `different_reader_runner_seal` 은 kit 사본에 판독기를 넣으면 목록 대조로 거부 — §6) — 시험이 그 줄을 지키지 않는다.
**최소 해결:** R33 에 셋 (밖 step · 숫자 아님 · 상태 불일치 — 사유 문자열 `ULKRF-01` 단언) · 사건 되감기 k ≤ k_r 하나 · R36 에 "kit 판독기 파일 = 봉인 · SHA256SUMS 판독기 줄만 다름 (sums_sha256 맞춤)" 하나.  rc 조건은 시험이 어렵다면 '시험 없음' 한정으로 둔다.

### PRE-UL-03 · P3 · G2 원자 비교 파서 (`_dump_tokens`) 가 관측 파싱 규칙 밖 — 고친 G2c 의 옆 자리

**자리:** `ul_gates.py:215–240` — 복원 판정 G2 (`ul_reader.py:1425`) · 중력 팔 복원 G2 (`ul_reader.py:950`).  열 수 다른 줄을 조용히 건너뛰고 · 같은 ID 는 뒤 줄이 덮고 · TIMESTEP · NUMBER OF ATOMS 를 보지 않는다.
**반례 (`probe_misc.py`):** 원 덤프 원자 5 · 시험 덤프 = 원자 3 의 다른 x 줄 + 원 5 줄 (선언 6) → **G2 PASS** · 시험 덤프 TIMESTEP 9999999 → PASS · 원자 3 의 잘린 덧줄 → PASS.  같은 파일을 `ul_lib.read_dump` 는 ok (ID 고유는 호출자 몫) — G2 경로에는 그 호출자 검사가 없다.
README §5 관측 파싱 행 "모든 경로에서 덤프 전부 읽힘 (머리 · 열 · 행 수 · 유한) · 머리 step = 요청 step · ID 고유" 와 어긋남.  실제 LIGGGHTS 출력 사례 아님 · RESTORED 오발행은 다른 검사 (G1 · G2c · PRE=POST) 와 함께 걸려야 함 — 끝까지 (restore 판정) 만든 반례는 아님.
**최소 해결:** G2 도 `read_dump` (ok · 머리 step · 선언 수) + `ids_of` 고유 검사 뒤 토큰 비교 · 또는 README 문구를 "G2 = 토큰 비교 (중복 · 머리 미검사)" 로 한정.

### PRE-UL-04 · P3 · G2c 열 결손 (관측 결손) 이 VALUE_MISMATCH 로 분류 — 등록 규칙과 어긋남 (요청서 Q3 로 공개)

등록 §14-10 "관측 결손 = UNCONFIRMED · 수치 불일치 = VALUE_MISMATCH · 기술 실패 = SYNTAX_FAIL (따로)" · `ul_gates.restoration_verdict` docstring "None = 관측 결손 → 미확인 · 수치 불일치와 섞지 않는다" · README 복원 행 "UNCONFIRMED (관측 결손) · VALUE_MISMATCH (수치)".
지금 = G2c 파서 문제 (열 결손 · 소수 쌍 ID — ULKRR-04 부터) → `status FAIL` → `prepost False` → **VALUE_MISMATCH**.  관문 영향 없음 (둘 다 RESTORED 아님).
요청서 Q3 가 이 선택을 묻고 있으므로 결함으로 부풀리지 않는다 — 다만 **우리 등록이 이미 답 (UNCONFIRMED) 을 적어 두었다** 는 것을 요청서 Q3 에 적거나, 파서 문제 = `NOT_COMPUTED`/`OBS_FAIL` → `prepost None` → UNCONFIRMED 로 고친다 (C4 · R35 의 기대 상태 문자열만 바뀜).

### PRE-UL-05 · P3 · 요청서의 Codex 탐침 재실행 안내가 고친 트리의 결과와 어긋남

요청서 §0 "판정문 §7 탐침을 고친 트리에서 다시 돌려 주면 좋다" — 그대로 돌리면 (내가 핀 사본에서 실행):
- `resume_recheck.py` = **37 중 35** · 남는 둘 = `fractional_resume_event_k` · `fractional_confirmation_k` (정수 반올림 — Codex 판정문 §6 "결함으로 세지 않음" · 이번에 안 고침).  요청서는 이 둘을 언급하지 않는다.
- `grammar_provenance.py` = `all_expectations_satisfied false` — **양성 대조 (`positive_actual_reader`) 까지 거부** (사유 = "kit 사본 read_history.py · history_params.json sha256 None — 승인 밖 판독기").  Codex 합성 kit 사본 (`kit_metadata/`) 에 SHA256SUMS 만 있고 판독기 · 표가 없어서다 (Q3 설계대로).
  kit 사본에 두 파일 (봉인 바이트) 을 넣은 판 (`probes/grammar_provenance_kitreader.py`) = 양성 허용 · 음성 11 그대로 거부 · 원자료 변조 넷 = **재판독 FAIL 로** 거부 · `different_reader_runner_seal` = kit 목록 대조로 거부 (Codex 의 옛 기대 `gate True` 다섯 = 이번 Q3 가 의도해서 뒤집은 것).
- `receipt_ids_recheck.py` = **줄 296 `IndexError` 로 끝남** (요약 JSON 없음) — 정밀도 블록이 `1.0000000000000001` 토큰의 행을 `dump['rows'][0]` 로 읽는데, Q4 수정이 그 토큰 (float 가 정수 1 로 가리는 비정수) 을 파서 문제로 거부해 행이 없다.  Q4 가 의도대로 동작한 결과다.
  그 블록만 빈 행을 허용하면 끝까지 돈다: 92 단언 중 기대 불일치 하나 = `g2c_missing_column_actual_cli` — 그 기대 자체가 옛 결함 꼴 (KeyError · rc 1) 이라 고친 트리의 rc 2 · VALUE_MISMATCH · UB 거부가 '불일치' 로 찍힌다 (= 수정 신호).
이 세 가지를 요청서에 적어 두지 않으면 Codex 가 "고친 트리에서 양성 거부 · 기대 미충족 · 탐침 예외" 를 회귀로 읽을 수 있다.

## 4. 숫자 · 전칭 대조 (요청서 ↔ 내 실행)

| 요청서 주장 | 내 실행 · git | 판정 |
|---|---|---|
| `ul_lib` · `ul_s3` · `ul_observers` · `ul_gates` = 24 · 16 · 21 · 41 (rc 0) | ✓ 줄 24 · 16 · 21 · 41 · rc 0 (핀) | 같음 |
| 시험 먼저 = rc 1 · 0 · 0 · 1 (2 · 0 · 0 · 4 실패) | `1c0b9fd65` 거울: 22/24 · 16 · 21 · 37/41 | 같음 |
| `ul_reader` 182/182 · 시험 먼저 18 실패 (옛 158 통과) | 182/182 · 시험 먼저 164/182 (R33 3 · R34 1 · R35 5 · R36 9 실패 · 새 대조 6 통과) | 같음 |
| `seal_kit` selftest · check = 76 파일 · 규칙 24 · 폐기 0 | ✓ (핀 · 시험 먼저 둘 다) | 같음 |
| `make_unload_decks` 291 · 덱 64 | ✓ 291 · 64 | 같음 |
| `make_history_decks` 172 · 덱 9 · 15 파일 | ✓ | 같음 |
| `read_history` 56/56 | ✓ | 같음 |
| `ul_runner_test` 38/38 · 시험 먼저 1 실패 (M25) | ✓ 38/38 · 시험 먼저 37/38 (M25) | 같음 |
| 키트 SHA256SUMS `441f66d7…6c34` · history `8ff722d2…b928d` · `unload_params.json` 무변경 | ✓ (sha256sum · SUMS 줄 diff 없음) · `sha256sum -c` 둘 다 OK | 같음 |
| 커밋 순서 1c0b9fd65 → 22a347722 → fcc0d6a75 → 4803b959c → 44a034534 → 92e6cda4d | ✓ git log | 같음 |
| 증거 summary `kit_git_tree` = 시험 먼저 · 핀 | ✓ `523d1920…` = `1c0b9fd65` 트리 · `91f62b8c…` = `fcc0d6a75` = 핀 트리 | 같음 |
| `039abb141` 판독기 `18521ae7…` ≠ 봉인 `70f741a9…` · `b1121b6b6` 이후 판독기 · 표 바이트 그대로 | ✓ (커밋별 sha · 14 커밋) | 같음 |
| 실행 2 · 반복 = 판 `799459c85` · `44a034534` · LMP `ee2d7726…` · history 봉인 `8ff722d2…` · 판독기 `70f741a9…` · 단계 rc 0/0/0 · 19/19 | ✓ (묶음 run_manifest · 판정 JSON · kit SUMS) | 같음 |
| 실행 1 · 1b = `a30fe150e` · `debe8387…` · `18521ae7…` · GA rc 1 · Mismatched fix | ✓ (묶음 · 재판독 문제 글 그대로) | 같음 |
| 묶음 sha256 = SLURM 화면 "보낼 것" 값 | ✓ 넷 + H0–H5 `be0acbd7…` (zip 화면 여섯) | 같음 |
| 발송 메모: 핀 → `a76f59d0d` 사이 키트 · 등록 · 요청서 무변경 · 바뀐 것 = 반입 README 한 줄 (`4b1d67f62`) | ✓ `git diff --stat` = 반입 README 1 줄 | 같음 |
| §0 "`run_unload.sh` (주석 한 줄)" | diff = 주석 1 줄 → 2 줄 | 사소 (고칠 필요 없음) |

## 5. 변이 시험 (고친 줄 하나씩 · 거울 사본 · 봉인 줄만 다시 계산)

| 변이 | 결과 | 옳은 이유? |
|---|---|---|
| ULKRF-01 중복 경계 검사 끔 | ❌ R33 셋 실패 (one_auth_two_rollbacks · duplicate_event_only · 같은 step 다른 k) · 대조 통과 | ✓ |
| ULKRF-02 `kback` 끔 | ❌ R34 4→5 하나 실패 · 대조 · 같음/짧음 · 무승인 통과 | ✓ |
| `kback` 을 창 CSV 에도 | ❌ 대량 실패 | ✓ (단 CSV 한정이 맞다) |
| ULKRF-03 `_contacts` 조기 반환 끔 | ❌ C4 넷 · R35 다섯 실패 (KeyError) | ✓ |
| Q3 재판독 끔 | ❌ R36 일곱 · M25 실패 · R32 통과 | ✓ |
| Q4 정수 토큰 끔 · Decimal 가림 검사 끔 | ❌ L14 둘 · 하나 | ✓ |
| Q4 `_w` LF 되돌림 | 생존 (Linux 판별 불가 — 요청서가 공개) | 공개됨 |
| 사유 줄 · 조건 다섯 (PRE-UL-02) | 생존 | ✗ 시험 없음 |

## 6. Codex 탐침 재실행 (판정문 §7 · 핀 사본 · scratch)

| 탐침 | 핀 결과 | 비고 |
|---|---|---|
| `resume_recheck.py` | 37 중 35 · 남음 = 반올림 둘 | 옛 실패 셋 (중복 승인 둘 · 5 창) 닫힘 |
| `grammar_provenance.py` (그대로) | 양성까지 거부 (kit 사본에 판독기 없음) | PRE-UL-05 |
| 같은 탐침 · kit 사본에 판독기 · 표 (`grammar_provenance_kitreader.py`) | 양성 허용 · 음성 11 거부 · 변조 넷 = 재판독 FAIL 거부 · 다른 판독기 = 목록 대조 거부 | Q3 의도대로 |
| `grammar_types.py` · `history_actual.py` · `kit_byte_checks.py` | rc 0 · 덱 64/64 바이트 같음 · H0–H5 재판독 | — |
| `grammar_windows_r32.py` | rc 1 = Windows 진단 탐침 (Linux 에서 CRLF 0) | 판정 무관 |
| `receipt_ids_recheck.py` (그대로) | **끝 블록에서 `IndexError`** (줄 296 · 요약 JSON 미기록) — 정밀도 블록이 토큰 `1.0000000000000001` 의 행이 있다고 가정하는데 Q4 수정이 그 가려진 비정수 토큰을 파서 문제로 거부해 행이 0 | Q4 가 의도대로 동작한 결과 · Codex 가 고친 트리에서 돌리면 그대로 깨진다 → PRE-UL-05 (c) |
| 같은 탐침 · 정밀도 블록만 빈 행 허용 (`receipt_ids_recheck_q4tolerant.py`) | 92 단언 · 기대 불일치 **하나 = `g2c_missing_column_actual_cli`** — 그 기대가 옛 결함 꼴 ("unhandled KeyError") 을 적어 둔 것이라, 핀에서 rc 2 · Traceback 없음 · `restore_verdict.json` = VALUE_MISMATCH · 다음 UB 거부로 바뀐 것이 **수정 신호** · 기준 (`eaecfba2a`) 의 불일치 둘 (`g2c_c_cpl7_missing` · `g2c_c_cpl8_missing`) = 핀에서 충족 · 범위 관찰 다섯 (일반 팔 영수증 · UV 실패 영수증 · 정밀도 경계) 그대로 · 정밀도 = `9007199254740993` 거부 · `1.0000000000000001` 파서 문제 | ULKRF-03 · Q4 수정 확인 (Codex 탐침으로) |

### 6-1. 실행 2 반입 재확인 (`probe_run2.py`)

묶음 넷 · zip sha256 = README · SHA256SUMS.received 같음 · 멤버에 절대 경로 · `..` · 링크 0 · 실행 2 · 반복: 판정 PASS 19/19 · 단계 rc 0/0/0 · 덱 사본 셋 + 판 STL = `GRAMMAR_INPUTS` · kit SUMS sha256 = manifest `sums_sha256` · kit 판독기 줄 = `70f741a9…` · 표 줄 = `7a5279f0…`.
옮긴 사본 재판독 = `GA_args` · `GB_args` 만 거짓.  절대 경로 접두를 scratch 로 바꾼 '원래 자리' 모의 (바꾼 파일 = GA · GB `ckpt.txt` · `vars.txt` · `run_manifest.txt` · `grammar_verdict.json` — 그 밖 바이트 그대로 · kit 사본 = 리포 history_test 바이트 = `799459c85` kit 바이트) → 재판독 PASS · 검사 19 = JSON · **`ul_reader.grammar_prereq(…, ee2d7726…)` = PASS · 문제 0** (실행 2 · 반복 둘 다).

## 7. 확인했지만 결함 아님

- 유니코드 숫자: `resume_from=３２７００００` (전각) 승인 · ID 토큰 `٣` · `３` · `1_000` · `1e3` = 같은 값으로 받음 — 값이 같아 틀린 값 아님 (관찰).
- RESUME step · k 소수 토큰 (`3270000.4` · `1.4`) 반올림 승인 = Codex 판정문 §6 의 "정수 반올림 관찰" 그대로 (이번 수정 범위 밖 · PRE-UL-05 에 '닫지 않는 것' 으로).
- 같은 `resume_from` 두 줄 = 집합으로 합쳐짐 · RESUME 둘이면 중복 거부 — 무해.  서로 다른 경계 둘의 이어 돌림 (러너가 두 번째 재개를 막음 · `run_unload.sh:88`) 은 판독기가 경계마다 승인 — 보장 "경계 하나에 승인 한 번" 과 모순 아님.
- Q3 재판독: `python3 -I` 라 kit 폴더 모듈 끼워 넣기 없음 · `read_history.py --grammar` 경로는 표준 라이브러리 + 자기 파일만 (`make_history_decks` import 는 합성 · 모의 경로뿐) · `--params` 명시 · `--out` 임시 폴더 · 런 폴더에 안 씀.
- Q4 ③ EXT rc 2 범위: `s0p` = PASS 아니면 rc 2 (NOT_COMPUTED · FAIL · F3) — 문구 맞음.
- 중력 팔 G2c 열 결손 → `_g_restore` FAIL (예외 없음) → 팔 TECH.

## 8. 못 본 것과 이유

- 실제 LIGGGHTS · MPI · SLURM — 없음 (지시).  PRE-UL-01 은 합성 기록 + 덱 · 러너 소스 순서로 근거.
- ibb 의 실제 kit 사본으로 `grammar_prereq` — 묶음에 kit 스크립트 없음 → 경로 바꾼 모의로 대신 (§6-1).  원래 절대 경로 (`/home/yonghoon/…`) 는 scratch 밖이라 만들지 않음.
- Windows R32 (CRLF) — Linux 에서 판별 불가 · 요청서가 Codex 에 맡김 (그대로).
- PRE-UL-01 최소 해결 ① ② 를 실제로 넣어 본 시험 — 하지 않음 (리포에 쓰지 않음 · 설계 검토만).
- PRE-UL-03 을 복원 판정 끝 (RESTORED) 까지 이어 본 반례 — 함수 수준까지만.

## 9. '이번에 닫는 것 / 닫지 않는 것' (요청서 맨 위 — 초안 · 지금 요청서에 없음)

**이번에 닫는 것** (수정 재확인 판정 10-15 · 코드 핀 `eaecfba2a` 의 잔여 · 최소 해결 그대로):
- `ULKRF-01` 같은 경계 RESUME 중복 · 상충 = 승인 없음 + 사유 (판정문 §4 · `one_auth_two_rollbacks` · `duplicate_event_only`).
- `ULKRF-02` 승인된 재시도의 단 끝이 옛 시도보다 짧음 · 같음 · 김 = 새 시도 시작 식별 (`resume_completed_hold_5_windows`) · 무승인 되돌아옴 = 미식별 그대로.
  (PRE-UL-01 을 고치면: 새 시도가 그 단을 끝내지 못함 (TIMEOUT · GUARD · 이동 중) 도 여기에 — 고치지 않으면 아래 '닫지 않는 것' 으로)
- `ULKRF-03` G2c 필수 열 결손 (양쪽 · 실제 restore CLI) = 예외 없이 FAIL + 사유 · RESTORED 아님.
- Q2 영수증 범위 문구 (판정문 권고 문구 그대로 · 동작 변경 없음) · Q3 문법 사전 점검 원자료 재판독 (승인된 판독기 · 봉인 값일 때만) · Q4 비차단 셋 (정수 ID 토큰 · §14-9 정정 · EXT rc 2 범위 · LF fixture).
- `ULKRR-01` 의 실행 부분 = ibb 실행 2 PASS 19/19 반입 (§7 · Q7 판단 요청).

**닫지 않는 것** (이번 범위 밖 · 그대로 열림):
- 본 R · 10:0 연장 · U 의 GO (실행 · 결과 0 건).
- 정수 반올림 (k · w · step 의 소수 토큰 — 판정문 §6 관찰 · 탐침 `fractional_resume_event_k` · `fractional_confirmation_k` 는 고친 트리에서도 기대 미충족 그대로).
- Windows 에서 R32 양성 (Linux 판별 불가 — Codex 확인 요청).
- G2 원자 비교 파서 (`_dump_tokens`) 의 머리 step · 행 수 · ID 고유 (PRE-UL-03 — 고치지 않으면 README 문구 한정).
- G2c 파서 문제의 분류 VALUE_MISMATCH ↔ UNCONFIRMED (Q3 질문 — 등록 §14-10 은 관측 결손 = UNCONFIRMED).
- 재판독은 그 폴더의 **지금** 원자료를 다시 읽는다 — 런 뒤 원자료가 바뀌지 않았다는 영수증 (원자료 sha256 기록) 은 없다 · 원래 자리 한정 · 판독기 판 한정 (`b1121b6b6` 이후).
- (고치지 않을 때만) PRE-UL-01.

## 10. 재실행 (scratch · 리포에 쓰지 않음)

```bash
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload
bash $S/mk_mirror.sh 92e6cda4d $S/m_pin ; bash $S/mk_mirror.sh eaecfba2a $S/m_base ; bash $S/mk_mirror.sh 1c0b9fd65 $S/m_testsfirst
bash $S/run_selftests.sh $S/m_pin $S/pin ul_lib ul_s3 ul_observers ul_gates ul_reader     # 24 · 16 · 21 · 41 · 182
bash $S/run_probe.sh probe_resume_unfinished.py m_pin/docs/data/ps45_unload_20261009 probes_out/pre_ul01_pin.json   # PRE-UL-01
bash $S/run_probe.sh probe_misc.py m_pin/docs/data/ps45_unload_20261009 probes_out/probe_misc_pin.json               # G2/G3/G9/G11 · Q3a
bash $S/run_probe.sh probe_run2.py /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a93377624c009ba18 m_pin/docs/data/ps45_unload_20261009 probes_out/run2
bash $S/run_probe.sh mutate.py m_pin mut_work probes_out/mutations_reader.json        # 변이 (이름 주면 그것만)
bash $S/setup_codex_rerun.sh 92e6cda4d $S/codex_rerun_pin ; bash $S/run_codex_probes.sh $S/codex_rerun_pin resume_recheck grammar_provenance history_actual kit_byte_checks
```
