# Codex 짧은 재확인 요청 — DEM 언로딩 키트 수정 재확인 반영 (ULKRF-01 · 02 · 03 · Q2 · Q3 · Q4) (2026-10-15 · 결과 0 건 · 발송 = 1저자)

> **발송 메모 (10-21)** — 이 요청서는 10-15 에 쓴 그대로다 (리뷰 핀 `92e6cda4d`).  핀 뒤 현재 HEAD `a76f59d0d` 까지 키트 폴더 `docs/data/ps45_unload_20261009/` · 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` · 이 요청서는 **바뀌지 않았다** (git diff 0).  핀 뒤 바뀐 것 = 실행 반입 README 한 줄 — §7 의 "⬜ 1저자 확인 (발사 때)" 가 **✅ 1저자 10-15 `GRAMMAR_VERDICT` = 실행 2** 로 (`4b1d67f62`).  Q7 은 그 확인을 전제로 판단해 달라.

> **사전 리뷰 반영 (10-21 · 대안 판 — PRE-UL-01 을 고치지 않고 보낼 때 · 고치면 이 블록 ①의 '닫지 않는 것' 첫 줄을 '닫는 것' 으로 옮기고 새 핀 · 시험 수로 다시 쓴다)**
>
> **이번에 닫는 것** — 수정 재확인 판정 (코드 핀 `eaecfba2a`) 의 잔여 P2 셋과 Q2–Q4 를 판정문 §4 · §7 최소 해결대로:
> `ULKRF-01` 같은 경계 RESUME 중복 · 상충 = 승인 없음 + 사유 · `ULKRF-02` 승인된 재시도의 단 끝이 옛 시도보다 짧음 · 같음 · 김 = 새 시도 시작 식별 (무승인 되돌아옴 = 미식별 그대로) ·
> `ULKRF-03` G2c 필수 열 결손 (양쪽 · 실제 restore CLI) = 예외 없이 FAIL + 사유 · Q2 영수증 범위 문구 · Q3 문법 사전 점검 원자료 재판독 · Q4 비차단 셋 · `ULKRR-01` 실행 부분 (실행 2 반입 · §7 Q7).
>
> **이번에 닫지 않는 것** (그대로 열림 · 숨기지 않는다):
> - **이어 돌림의 새 시도가 단 k_r + 1 줄을 다시 쓰기 전에 끝나는 경우** (TIMEOUT · GUARD · 이동 중 TIMEOUT) — 옛 시도의 그 단 줄이 남아 정상 관측으로 쓰인다.  합성 반례 (판독기 실제 함수 사슬):
>   옛 시도가 R_M 단 (k4) 줄 · RM 사건까지 쓰고 요약 전 끊김 → RESUME (k 3 · k3 끝) → 새 시도가 k4 창 둘 뒤 TIMEOUT = **primary OK · ρ 0.2026077873428664 % · UVa ALLOW**
>   (같은 꼴 fresh = UNIDENTIFIED · 거부) · GUARD 로 끝남 · 이동 중 TIMEOUT (새 창 없음) 도 같음 · 교차 전 단이면 LOWER_BOUND 0.2251 → 0.2701 %.  수정 전 (`eaecfba2a`) 에도 같은 결과 (이번 수정이 만든 것 아님).
>   후보 해결 = 단 줄 ↔ 그 단 창 기록 결합 (n_windows · 마지막 창 step) + 버린 옛 사건 구간의 창 · 단 줄 정리 (사전 리뷰 PRE-UL-01).
> - 정수 반올림 (k · w · step 의 소수 토큰 — 판정문 §6 관찰) — 판정문 §7 `resume_recheck.py` 를 고친 트리에서 돌리면 37 중 35 · 남는 둘 = `fractional_resume_event_k` · `fractional_confirmation_k` (이번에 고치지 않음).
> - G2 원자 비교 파서 (`ul_gates._dump_tokens` — 복원 · 중력 팔 G2) 의 머리 step · 선언 수 · ID 고유 미검사 (같은 ID 두 줄 · 다른 TIMESTEP · 열 수 다른 덧줄에도 G2 PASS — 손상 입력 방어 · README §5 '모든 경로에서' 는 G2 에 아직 서지 않는다).
> - G2c 파서 문제의 분류 = 지금 VALUE_MISMATCH (아래 Q3 — 등록 §14-10 은 "관측 결손 = UNCONFIRMED · 수치 불일치 = VALUE_MISMATCH 따로").
> - 수정이 더한 사유 줄 일부는 자체시험이 지키지 않는다 (변이 생존 — `resume_from` 밖 RESUME · k/step 숫자 아님 · 사건 ↔ 상태 파일 불일치 사유 · 사건 되감기 k > k_r 조건 · Q3 kit SHA256SUMS 판독기 줄 대조 · 재판독 rc) — 동작은 사전 리뷰 탐침으로 확인.
> - 재판독은 그 폴더의 **지금** 원자료를 다시 읽는다 — 런 뒤 원자료가 바뀌지 않았다는 영수증 (원자료 sha256 기록) 은 없다 · 원래 자리 한정 · 판독기 판 한정.
> - 본 R · 10:0 연장 · U 의 GO · Windows R32 (Codex 확인 요청 그대로).

> **한 줄**: 수정 재확인 판정 (코드 핀 `eaecfba2a` · **HOLD**) 의 새 P2 셋 (`ULKRF-01` · `02` · `03`) 을 판정문 §4 · §7 의 최소 해결대로 고치고, Q2 범위를 판정문 권고 문구 그대로 적고,
> 문법 사전 점검이 그 런 폴더 원자료를 **승인된 판독기로 다시 읽게** 했다 (Q3) · 비차단 셋 (Q4) 도 같이 — 시험 먼저 · LIGGGHTS 없음.  각 반례가 고친 트리에서 거부되고
> 양성 대조가 그대로인지, Linux 전체 로그가 지원 환경 실행 기록을 채우는지 짧게 판정해 달라.  남은 실행 = ibb 문법 fixture 실행 2 (실제 바이너리 · 원 보고 묶음).
> ✅ **1저자 10-15** — 수정 계획 dem_unloading_kit_fix_recheck_fix_plan_20261015.md Q1–Q4 = 권고대로 (*"권고대로 부탁해"*).
> **리뷰 핀** = **`92e6cda4d`** — **실행 2 반입판** (§7 · 10-21 채움 · 키트 폴더 = `fcc0d6a75` 와 바이트 같음) · **기준** = `eaecfba2a` (판정문 코드 핀).  이 요청서 · 증거 README 는 작업 트리 커밋 번호를 적지 않는다 (`SELF-116`).

## 0. 대상 · 지위

- 판정문 codex_review_dem_unloading_kit_fix_recheck_20261015.md · 증거 codex_dem_unloading_kit_fix_recheck_evidence_20261015 (탐침 스크립트는 **실행하지 않았다** — `notes/` ·
  `evidence/*.json` · 탐침 글로 반례를 읽고 우리 시험으로 다시 만들었다 · 판정문 §7 탐침을 고친 트리에서 다시 돌려 주면 좋다 — 사전 리뷰 (10-21) 가 고친 트리에서 돌려 본 결과:
  `resume_recheck.py` 37 중 35 (남는 둘 = 정수 반올림 관찰 · 위 '닫지 않는 것') · `grammar_provenance.py` 는 **그 합성 kit 사본 (`kit_metadata/`) 에 `read_history.py` · `history_params.json` 이 없어**
  양성 (`positive_actual_reader`) 까지 '승인 밖 판독기' 로 거부된다 (Q3 설계대로 — 실제 ibb kit 사본에는 두 파일이 있다) · kit 사본에 두 파일 (봉인 바이트) 을 넣으면 양성 허용 · 음성 11 그대로 거부 ·
  원자료 변조 넷 = 재판독 FAIL 로 거부 · `different_reader_runner_seal` = kit 목록 대조로 거부 (옛 기대 `gate True` 다섯 = Q3 가 의도해서 뒤집은 것) ·
  `receipt_ids_recheck.py` 는 끝 정밀도 블록 (줄 296) 에서 `IndexError` — 토큰 `1.0000000000000001` 을 Q4 가 파서 문제로 거부해 행이 없다 (Q4 가 의도대로 동작) ·
  그 블록만 빈 행을 허용하면 92 단언 중 기대 불일치 하나 = `g2c_missing_column_actual_cli` — 그 기대가 옛 결함 꼴 (KeyError · rc 1) 을 적어 둔 것이라 고친 트리의 rc 2 · VALUE_MISMATCH · 다음 UB 거부가
  '불일치' 로 찍힌다 (= ULKRF-03 수정 신호) · `g2c_c_cpl7_missing` · `g2c_c_cpl8_missing` = 충족).
- 커밋 (본 가지 · 순서): 시험 먼저 `1c0b9fd65` → 수정 `22a347722` → 문서 · 증거 · 이 요청서 첫 판 `fcc0d6a75` → 참조 검사기 도달 기준 `4803b959c` (키트 밖) → 원장 `44a034534` → 실행 2 반입 + §7 (= 리뷰 핀 · 키트 무변경).
- 바뀐 곳 = 키트 `docs/data/ps45_unload_20261009/` — `ul_lib.py` · `ul_gates.py` · `ul_reader.py` · `run_unload.sh` (주석 한 줄 — EXT rc 2 범위) · `seal_kit.py` (규칙 글 · 증인 ·
  규칙 수 24 그대로) · `ul_runner_test.py` · README · `SHA256SUMS` · `active_rules.json` / 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §14-9 정정 줄 · §14-11 (결과 0 건).
- 바꾸지 않은 것: `unload_params.json` · 생산 덱 64 (`make_unload_decks.py --check`) · 이력 시험 폴더 전부 (`history_test/SHA256SUMS` sha256 `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d`
  그대로 — 덱 아홉 · 판 STL · 표 · 생성기 · 판독기 · 러너) · 물리 목표 · P_meas 1 MPa · 0.10 %p · S1–S4 · KE 계수 10 · S3 1e-3 · 판 법선력 부호 −1 · S0.
- 실행 없음 (본 R · 10:0 연장 · U · H0–H5 · 문법 fixture 실제 바이너리).  원장 `docs/reviews/findings.json` 은 이 수정 가지에서 고치지 않았다 (claimed_fixed = 메인 세션).

## 1. 결함 ↔ 수정 ↔ 시험

| 원장 | 판정문 최소 해결 | 수정 · 자리 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|
| `ULKRF-01` P2 | 승인 · 소비를 고유 경계와 연결 · 중복 · 상충 RESUME = 사유 있는 거부 · 사건 정리도 같은 규칙 · 정상 재개 양성 유지 | `ul_reader._resume_auth` → (승인, 문제): 러너 `resume_from` step 마다 RESUME 정확히 한 줄 · 둘 이상 (같은 k 중복 · 다른 k 상충) · 사건 ↔ 상태 파일 불일치 · `resume_from` 밖 RESUME = 승인 없음 + 사유 · `read_run` 사건 되감기 = 경계마다 한 번 · 버릴 사건 k > k_r · `_supersede` 소비 = 경계 값 (목록 번호 아님) · `resume_from` 없는 폴더 (UTc) = 승인 · 문제 없음 (부모 경계 규칙 그대로) | `ul_reader` R33 — `one_auth_two_rollbacks` (resume_from 한 줄 · 상태 파일 하나 · 같은 RESUME 두 줄 · 묶음 둘) · `duplicate_event_only` · 같은 step 다른 k = 3 실패 (주 값 OK · UVa 허용) → 3 거부 (사유 `ULKRF-01` · 승인 없음 · 남긴 줄 · 옛 사건 버리지 않음) · 대조 = 진짜 한 번 (승인 하나 · 남긴 줄 3) · `one_event_two_rollbacks` (거부) 그대로 · R28 · R10 · R23 (UTc) · M23 그대로 |
| `ULKRF-02` P2 | 승인된 시도 경계로 새 구간 식별 · 짧음 · 같음 · 김 + 무승인 중복 · 모든 중복 k 삭제 금지 | `_supersede(…, steps_csv)` — 새 시도 시작 = 승인 경계 뒤 먼저 오는 쪽: step 역행 (창 · 단 CSV) 또는 단 CSV 에서 k 가 k_r + 1 로 되돌아옴 (k ≤ 앞 줄 k) · 그 줄 = (k_r + 1 · step > s_r) · 버릴 줄 = s_r 뒤 (k > k_r) · 앞 줄 = (k_r, s_r) · 승인 없는 되돌아옴 = 문제 (미식별) | R34 — 생성 UT 덱 제어 흐름 (`make_unload_decks.deck_sim`) 으로 단 k 2 = 4 · 5 창 (P 0.0010 · 0.0009 · 0.0008 ×3 → S1 [0, 0, 0, 1, 1] · 정상 끝 = 다섯째 창) · 4 → 5 (Codex `resume_completed_hold_5_windows`) = 1 실패 (k [0, 1, 2, 2, 3, 4] 미식별) → 통과 (옛 창 넷 + 단 줄 버림 · 주 값 OK · UVa 허용) · 4 → 4 · 5 → 4 · 새 시도 단독 · 무승인 4 → 5 (= 미식별 그대로) 통과 그대로 |
| `ULKRF-03` P2 | `_contacts` 가 파서 `ok=False` 를 먼저 · g2c FAIL + why · 양쪽 파일 · 실제 restore CLI · 채우기 · 삭제 금지 | `ul_gates._contacts` — `d['ok']` 거짓이면 열을 읽기 전에 돌려준다 → `g2c_compare` 기존 FAIL + 사유 (열 이름 문제) → 복원 = VALUE_MISMATCH (RESTORED 아님 · `prepost` 거짓 · 기존 FAIL 경로) | `ul_gates` C4 (시험 · 원 쪽 × `c_cpl[7]` · `[8]` = 4 `KeyError` → FAIL + 사유) · `ul_reader` R35 (복원 판정 4 · 다음 제출 UB 거부 · **실제 restore CLI** = rc 1 Traceback → rc 2 · `restore_verdict.json` RESTORED 아님 · G2c FAIL + 사유 · 덤프 바이트 그대로) = 9 실패 → 통과 |

## 2. Q2 · Q3 · Q4 (계획 = 권고대로)

| 항목 | 수정 | 시험 |
|---|---|---|
| Q2 (가) 영수증 범위 (동작 변경 없음) | 판정문 권고 문구 그대로 — *"복원 / EXT 증서는 성공 완료 영수증이 필수이며, 일반 팔의 주 관측은 원 폴더에서 재판독한다.  재판독 가능성이 잡의 기술 성공을 뜻하지는 않는다."* — 키트 README §3 · §4 (관문) · 등록 §14-11 ④ · `_job_receipt` 설명 · 규칙 `restore_complete` 글.  "기술 실패 산출물 승인 재사용 0" 전칭 종결을 쓰지 않는다 · (나) (다음 제출에 앞 팔 성공 영수증) 는 채택하지 않음 | 문구 — 기존 R17 · R29 · M20 (RJ · RJ2 · EXT 증서 쪽) 그대로 |
| Q3 문법 사전 점검 원자료 재판독 | `ul_reader.grammar_prereq` ④ `_grammar_reread` — 그 런 kit 사본 (`run_manifest kit=`) 의 `read_history.py` · `history_params.json` sha256 = `GRAMMAR_READER` (= `history_test/SHA256SUMS` 의 그 두 줄 · 그 런 kit `SHA256SUMS` 에도 같은 값) 일 때만 `python3 -I <kit>/read_history.py <런> --grammar --params <kit>/history_params.json --out <임시>` (런 폴더에 쓰지 않는다) → 재판독 status PASS · exit_code 0 · rc 0 · 검사 19 = 판정 JSON (둘 다 참) 이어야 통과 · 판독기가 봉인 값이 아니면 실행하지 않고 거부 · 화면 줄 `reread=` · `reader_sha256=` (러너가 잡 기록 `grammar_line=` 에 남긴다) · 러너 스크립트 sha256 은 대조하지 않는다 | R36 — 양성 (원자료 = 승인된 판독기 자신의 합성기 꼴 · 재판독 PASS · 판독기 sha256 기록) · Codex 변조 넷 (GA 화면 ERROR · GB 첫 mesh z 99 · GB 화면 지움 · GB 마지막 상태 값 0 — 판정 JSON 그대로) · 판독기 셋 (kit 사본 판독기 고침 + kit SUMS · sums_sha256 맞춤 = Codex `different_reader_runner_seal` · 표 고침 · 판독기 없음) · 봉인 값 = 실제 파일 = `history_test/SHA256SUMS` = 9 실패 → 통과 · M25 (실제 러너 — M22 양성 판정 그대로 · 그 런 GA 화면 ERROR → RJ 의 LIGGGHTS 전 거부 · 호출 0 · RJ 폴더 없음) 1 실패 → 통과 · M22 양성 (지금 history_test 러너 + 읽는 쪽이 낸 판정) = 재판독 PASS 로 그대로 |
| Q4 비차단 셋 | ① `ul_lib.read_dump` — ID 열 (`id` · `c_cpl[7]` · `c_cpl[8]`) 정수 토큰 = float 없이 정확한 int → `exact_id` 가 그대로 대조 (`9007199254740993` 거부 · 정상 ID 그대로) · 소수 꼴 토큰이 float 로 정수로 가려지면 (`2.0000000000000001`) 파서 문제 ② 등록 §14-9 "지금 절차 · 강제하지 않는다" 아래 정정 줄 (지금 = 자동 사전 점검 + 원자료 재판독) ③ EXT rc 2 = PASS 아닌 모든 s0p 판정 (조건 미달 · 미계산 · 체크포인트 없음 — 물리 측정 실패만이 아니다) — README §3 · 등록 §14-11 ⑤ · 러너 주석 · 규칙 `stage_rc` 글 ④ R32 fixture 줄바꿈 무관 (`_w` LF 고정 쓰기) | `ul_lib` L14 (2^53 + 1 · 쌍 참조 · 긴 토큰) 2 실패 → 통과 · ④ = Linux 에서는 바이트 그대로라 판별 시험 없음 (Windows 에서 R32 양성이 다시 서는지 = 확인 부탁) |

**판단 범위 · 한정**: 재판독은 그 런 폴더가 **원래 자리** 일 때 뜻이 있다 (GA · GB 입력 기록 `ckpt.txt` · `vars.txt` = 절대 경로 — 옮긴 사본은 GA_args · GB_args 가 거짓) ·
실행 2 는 판독기 · 표가 봉인 값인 판 (`b1121b6b6` 이후 — 그 뒤 두 파일 바이트 그대로) 으로 돌린다 (`039abb141` 판독기 sha256 `18521ae7…` ≠ 봉인 `70f741a9…` → 그 판으로 낸 런은 거부 · 덱 같음) ·
문법 PASS = 기술 · 문법 검사이지 물리 검증이 아니다 (C19).

## 3. Linux 전체 로그 — `docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/`

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
for m in ul_lib ul_s3 ul_observers ul_gates ul_reader; do python3 -I $K/$m.py --selftest | tail -1; done   # 24 · 16 · 21 · 41 · 182 — 전부 PASS
python3 -I $K/seal_kit.py --selftest | tail -1 && python3 -I $K/seal_kit.py --check                        # 76 파일 · 규칙 24 · 폐기 0
python3 -I $K/make_unload_decks.py --selftest | tail -1 && python3 -I $K/make_unload_decks.py --check       # 291 · 덱 64
python3 -I $K/history_test/make_history_decks.py --selftest | tail -1 && python3 -I $K/history_test/make_history_decks.py --check
python3 -I $K/history_test/read_history.py --selftest | tail -1                                           # 56 / 56
python3 -I $K/ul_runner_test.py --selftest | tail -1                                                      # 38 / 38 (bash 필요)
python3 docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/tools/run_suite.py $K /tmp/ulkrf_suite   # 13 명령 전부 · 로그 · rc
```

## 5. 묻는 것

| Q | 무엇 |
|---|---|
| Q1 | `ULKRF-01` — "경계 하나에 승인 한 번" (같은 경계 RESUME 둘 이상 = 승인 없음 · 사건 ↔ 상태 파일 불일치 · `resume_from` 밖 RESUME = 상충) 이 판정문 §4 최소 해결을 채우는가 · 중복을 하나로 줄여 승인하지 않고 **승인 자체를 거두는** 선택 (애매한 증거 = 버리지 않는다) 이 맞는가 |
| Q2 | `ULKRF-02` — 새 시도 시작 = step 역행 (창 · 단) 또는 단 기록 k 되돌아옴 (먼저 오는 쪽) 이 짧음 · 같음 · 김 · 무승인을 다 가르는가 · 창 기록은 step 역행만으로 충분한가 (덱이 같은 단의 창 끝을 같은 step 에 쓴다 — 새 시도 첫 창 = 옛 시도 첫 창 step) · ⚠ 다섯째 경우 = 새 시도가 그 단 줄을 쓰기 전에 끝남 (위 '닫지 않는 것' 첫 줄 — 지금 판독기는 옛 줄을 남긴다) |
| Q3 | `ULKRF-03` — G2c 열 결손 = 기존 FAIL 경로 (복원 VALUE_MISMATCH) 로 충분한가 · 관측 결손이라 UNCONFIRMED 로 나눠야 하는가 (지금은 G2c 의 다른 파서 문제 — 소수 쌍 참조 등 — 와 같은 FAIL · ⚠ 우리 등록 §14-10 · `ul_gates.restoration_verdict` 설명은 "관측 결손 = UNCONFIRMED · 수치 불일치와 섞지 않는다" 라 적는다 — 지금 분류는 그 문장과 어긋난다 · 관문 영향 없음 (둘 다 RESTORED 아님)) |
| Q4 | Q3 재판독 — 승인된 판독기 = 그 런 kit 사본의 두 파일이 봉인 값일 때만 (이 키트의 봉인 kit 사본은 `history_test` 를 싣지 않는다 — 봉인 K1) 이 판정문 Q4 "승인된 판독기로 raw 자료를 다시 읽어야" 를 채우는가 · 원래 자리 한정 · 판독기 판 한정 (`b1121b6b6` 이후) 이 실행 2 에 부담 · 틈이 없는가 |
| Q5 | Q2 문구 · Q4 비차단 셋 (정수 토큰 · §14-9 정정 · EXT rc 2 범위 · LF fixture) 이 판정문 §5 · §6 의 요구를 채우는가 · Windows 에서 R32 양성이 이제 서는가 |
| Q6 | 남은 해제 조건 = ibb 실행 2 의 원 보고 묶음 (같은 바이너리 · 승인된 덱 · 판독기 · 원자료 재판독 PASS) 인가 |

## 6. 남은 것

- ✅ ibb 문법 fixture **실행 2 = PASS** (§7 · 10-15) — 원 보고 묶음 반입 · 승인된 판독기로 원자료 재판독 기록 → 그 `grammar_verdict.json` 이
  RJ · RJ2 · EXT 의 `GRAMMAR_VERDICT` (사전 점검이 그 런 폴더를 원래 자리에서 다시 읽는다).
- 원장 `ULKRF-01` · `02` · `03` → claimed_fixed (수정 `22a347722` · 원장 커밋 `44a034534`).
- ⛔ 본 R · 10:0 연장 · U = 이 재확인 GO + 실행 2 PASS 뒤.

## 7. 실행 2 결과 (10-15 · 1저자 ibb · 반입 = `docs/reviews/dem_unloading_grammar_fixture_runs_20261015/`)

| 런 | job · 시각 (KST) | 판 | history_test 봉인 | 판독기 | 단계 rc | 판정 |
|---|---|---|---|---|---|---|
| **실행 2** `gram_20261015_030225` | 285533 · 10-15 03:02 | `799459c85` | `8ff722d2…` | `70f741a9…` (= `GRAMMAR_READER`) | P 0 · GA 0 · GB 0 | **PASS · 19/19** |
| 반복 `gram_20261015_122956` | 286802 · 10-15 12:29 | `44a034534` | `8ff722d2…` | `70f741a9…` | P 0 · GA 0 · GB 0 | **PASS · 19/19** |
| 실행 1 · 1b (`192604` · `194645`) | 285220 · 285228 · 10-14 | `a30fe150e` | `debe8387…` | `18521ae7…` | P 0 · GA 1 | FAIL — `SELF-115` 결함 (1b = 같은 판 반복 · 이 반입으로 처음 기록) |

- LIGGGHTS sha256 = 넷 모두 `ee2d77261bac…` (등록 §11-1 ⓖ) · 덱 사본 (P · GA · GB) · 판 STL = `GRAMMAR_INPUTS` 봉인 값 · 표 `history_params.json` = 봉인 값 · 묶음 sha256 = 각 SLURM 화면의 "보낼 것" 값 (반입 README §1).
- **우리 트리 판독기 재판독** (리포 `read_history.py` · sha256 `70f741a9…`): 런의 절대 경로를 컨테이너에 새로 만들어 원래 자리에서 읽음 = 실행 2 · 반복 모두 **PASS · rc 0 · 검사 19 = 런 JSON 과 같음** · 옮긴 사본 = `GA_args` · `GB_args` 만 거짓 (입력 기록 절대 경로 — §2 의 "원래 자리 한정" 그대로) · 실행 1 · 1b = `Mismatched fix` 재현.  본 R 사전 점검의 kit 사본 판독기 재판독은 ibb 에서 (묶음에 kit 스크립트 없음).
- `GRAMMAR_VERDICT` = 실행 2 런 (`~/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json` · 첫 PASS) · 반복도 같은 판정 · ✅ 1저자 10-15 확인 (발송 메모 · `4b1d67f62`).
- 사전 리뷰 (10-21) 재확인: 묶음 sha256 = SLURM 화면 "보낼 것" 값 (넷) · 절대 경로 접두를 바꾼 '원래 자리' 모의 (kit 사본 = 리포 `history_test` 바이트 = `799459c85` kit 바이트 + 묶음의 kit SHA256SUMS) 에서
  재판독 PASS · 검사 19 = 런 JSON · `ul_reader.grammar_prereq` 전체 PASS · 문제 0 (실행 2 · 반복) — ibb kit 사본 자체로 돈 것은 아니다.

| Q | 질문 |
|---|---|
| Q7 | 이 반입 (같은 바이너리 · 승인된 덱 · 판독기 출처 · 원래 자리 원자료 재판독 PASS) 으로 `ULKRR-01` 의 실행 부분 (판정문 10-15 "코드 닫힘 / 실행 열림") 이 닫히는가 · 실행 2 를 `GRAMMAR_VERDICT` 로 고정하는 데 이의 없는가 |

