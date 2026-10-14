# Codex 짧은 재확인 요청 — DEM 언로딩 키트 재확인 반영 (ULKRR-02 · 03 · 04 · Q4–Q6 · Q5 문법 사전 점검) (2026-10-14 · 결과 0 건 · 리뷰 핀 `eaecfba2a` · 발송 = 1저자)

> **한 줄**: 재확인 판정 (핀 `a30fe150e` · **HOLD**) 의 새 P1 둘 (`ULKRR-02` · `03`) · P2 하나 (`ULKRR-04`) · §6 보강 셋 (Q4) 을 판정문 §4 · §6 · §9 의 최소 해결대로 고치고,
> 문법 fixture PASS 를 **R · EXT 실행 전 사전 점검**으로 강제했다 (Q5) · UC = fresh-attempt-only (Q6) — 시험 먼저 · LIGGGHTS 없음.  각 반례가 고친 트리에서 거부되고
> 양성 대조가 그대로인지, Linux 전체 로그가 §9-5 를 채우는지 짧게 판정해 달라.  `ULKRR-01` = `039abb141` (남은 것 = ibb 실제 바이너리 PASS · 실행 2).
> ✅ **1저자 10-14** — 수정 계획 dem_unloading_kit_reverify_fix_plan_20261014.md Q1–Q7 = 권고대로 (*"권고대로 해요"*).
> **리뷰 핀** = 이 정정판이 든 본 가지 커밋 (발송 때 1저자가 번호를 적는다 · 키트 코드 · 증거 바이트 = `eaecfba2a` 와 같다 · 원장 claimed_fixed = `4a8b55013`) · **기준** = `a30fe150e` (판정문 핀) · 이 수정 가지 시작 = `77b5885e0`.
> ⚠ **정정 10-14 밤 (`SELF-116`)**: 첫 판 (`eaecfba2a`) §0 · §3 · §6 의 커밋 번호 셋 (시험 먼저 · 수정 · README) 은 수정 작업 트리 (에이전트) 판이라 원격에 없었다 — 본 가지 번호로 바꿨다 (cherry-pick · `git patch-id` 같음 · 키트 트리 바이트 같음).  증거 폴더 이름 (`before_fix_tests_first_…/` · `after_fix_…/`) · `summary.json` 의 `git_head` 는 로그를 낸 작업 트리 판 그대로 둔다 (대응 = 증거 README §2).

## 0. 대상 · 지위

- 판정문 codex_review_dem_unloading_kit_reverify_20261014.md · 증거 codex_dem_unloading_kit_reverify_evidence_20261014 (탐침 스크립트는 **실행하지 않았다** — `evidence/*.json` · `notes/` 로
  반례를 읽고 우리 시험으로 다시 만들었다 · 판정문 §10 탐침을 고친 트리에서 다시 돌려 주면 좋다).
- 커밋 (본 가지): 시험 먼저 `b1121b6b6` → 수정 `e271bdd48` → README `70b3fefed` → 증거 · 이 요청서 첫 판 `eaecfba2a` → 원장 claimed_fixed `4a8b55013` → 이 정정판.
- 바뀐 곳 = 키트 `docs/data/ps45_unload_20261009/` — `ul_lib.py` · `ul_s3.py` · `ul_gates.py` · `ul_reader.py` · `run_unload.sh` · `run_unload_ibb.sbatch` (주석) · `seal_kit.py` (활성 규칙 22 → 24) ·
  `ul_runner_test.py` · README · `SHA256SUMS` · `active_rules.json` / 이력 시험 `history_test/` — `run_history.sh` (Q4 나) · `read_history.py` (모의 · 시험만) · `SHA256SUMS`.
- 바꾸지 않은 것: `unload_params.json` (바이트 = `a30fe150e`) · 생산 덱 64 (`make_unload_decks.py --check`) · 이력 시험 덱 아홉 · 판 STL · 표 · 생성기 (= `039abb141` 바이트) ·
  물리 목표 · P_meas 1 MPa · 0.10 %p · S1 · S2 · S4 · KE 계수 10 · S3 1e-3 · 판 법선력 부호 −1 · S0.
- 실행 없음 (본 R · 10:0 연장 · U · H0–H5 · 문법 fixture 실제 바이너리).  원장 `docs/reviews/findings.json` 은 이 수정 가지에서 고치지 않았다 (claimed_fixed = 메인 세션).

## 1. 결함 ↔ 수정 ↔ 시험

| 원장 | 판정문 최소 해결 | 수정 · 자리 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|
| `ULKRR-01` P1 | scalar 정정 · 재봉인 · 타입 음성 시험 → 실제 바이너리 PASS | `039abb141` (입력 셋 · 검사 ⑰) — 이 판에서 덱 · 생성기 손대지 않음 | ⬜ ibb 실행 2 (README §1-6) |
| `ULKRR-02` P1 | 허가된 재개 경계에서만 행 교체 · 그 밖 중복 · 역행 step/k = 미식별 · no-RESUME 반례 + 진짜 RESUME 양성을 선택 · 관문까지 | `ul_reader._resume_auth` (RESUME 사건 (k_r, s_r) + 러너 `resume_from=s_r` + 상태 파일 `restart/state_unload_<s_r>.in` 의 `ul_rstep` · `ul_k`) · `_supersede` (버릴 줄 = s_r 뒤 · k > k_r · 버린 뒤 앞 줄 = (k_r, s_r) · 새 첫 줄 = k_r + 1 · 경계마다 한 번) · `_order_problems` (k 역행 · 같은 k 의 w 중복 · 역행 · 숫자 아님) · 사건 되감기도 같은 규칙 | `ul_reader` R28 — Codex `duplicate_without_resume` (확인 단 k 3 steady 0 중복) · 창 중복 · 경계 반례 넷 (resume_from 없음 · 사건 k ≠ · 상태 파일 k ≠ · 상태 파일 없음) = 6 실패 → 6 거부 (주 값 미식별 · 선택 UNRESOLVED · UVa 거부) · 양성 대조 (단 2 의 남긴 줄 3 버림 · 주 값 OK · need_UV → UVa 허용) · R10 · `ul_runner_test` M23 (러너가 쓴 `resume_from` 으로 같은 결과 · UVb 허용) |
| `ULKRR-03` P1 | 완료 영수증 `fails=0` **과** `reader_rc=0` 둘 다 · 누락 · 비정수 · 비영 거부 · 결과 파일 발행 뒤 실패 음성 · 정상 `UNIDENTIFIED`/rc 0 양성 | `ul_reader._job_receipt` (끝 줄 · 두 키 한 번씩 · `\d+` · 0) · `_job_restored` (RJ · RJ2 증서 + 영수증 + `grammar_prereq=PASS`) · `gate('RJ2')` = S0′ 결정 PASS + 그 EXT 잡 영수증 | R29 — 끝 줄 `reader_rc=120` · 없음 · `x` · 문법 줄 없음 · **실제 판독기 CLI stdout 닫힘** (restore 증서 · kebase 기준 파일을 쓴 뒤 둘 다 rc 120 → 러너 기록 꼴 → UB 거부) · RJ2 (EXT `fails=1` · `reader_rc=1` · 없음 · 끝 줄 없음 = 거부) = 6 실패 → 통과 · `ul_runner_test` M20 (실제 러너 — `restore` · `kebase` 가 파일을 쓴 뒤 rc 120 → `reader_restore_rc=120` · 끝 `reader_rc=120` / `reader_rc=2` → UB 거부) · 양성 R14 · M6 · M17 (정상 미식별 rc 0 그대로) |
| `ULKRR-04` P2 | 필수 열 · 파서 오류를 먼저 · ID = 유한 양의 정확한 정수 · S0 · 현재 원자 · 복원 관측 · 쌍 참조 · 두 실제 경로 음성 | `ul_lib.exact_id` · `ids_of` (2^53 이하 · bool · 글자 거부) · `ul_reader._s0_dump` · `_atom_frame` · `_obs_frame` · `restore_verdict` S0 · `_s3_at` 쌍 참조 · `ul_s3.s3_residual` · `ul_gates._contacts` (G2c) — 끝점 S3 사유가 판정 why 에 붙는다 | R30 — UN 1 → 1.5 (Codex `fractional_un_id`) · PRE 2 → 2.5 · 원 S0 `id` 열 없음 · 끝점 원자 2 → 2.5 (`parsing_fractional_atom_id`) · 끝점 `id` 열 없음 (`parsing_missing_column` — 고치기 전 `KeyError`) · S0 열 없음 · 쌍 참조 2 → 2.5 = 7 실패 → 7 거부 (사유 · 예외 없음) · `ul_lib` L13 · `ul_s3` F12 · `ul_gates` C3 |

## 2. 보강 · 결정 (계획 Q4 · Q5 · Q6)

| 항목 | 수정 | 시험 |
|---|---|---|
| Q4 (가) §6-1 창 연속 | `separation(…, w_steps)` — 같은 k 안 앞 창 → 이 창이 w + 1 · 창 끝 step 간격 = 그 팔 W (`_arm_wsteps`: 런 폴더 덱 사본 → 없으면 표 W0 ÷ dt_factor) · 아니면 `gap_index` = 연속 끊김 (OBS_MISSING 과 같이) · DONE 불일치 사유에 끊김 | R31 — Codex `separation_missing_csv_window` (w 1 · 2 · 4 · 5 · 6) · 간격만 틀림 (w 3 + 1,000) = SEP_INCOMPLETE (주 값 OK) · 양성 예산 끝 선언 w 12 → w 15 = DONE |
| Q4 (나) §6-2 문법 러너 | `run_history.sh`: P → GA · GA → GB (그리고 H0–H5 의 P → 소비) = 앞 단계 rc 0 **과** 산출물 둘 다 | `read_history` S38–S40 (모의가 파일을 다 쓴 뒤 rc 1) — 고치기 전 GB · GA · 소비가 돌았다 |
| Q4 (다) §6-3 EXT | 첫 `s0p` rc **2** (등록된 연장 요청) + 끝 체크포인트일 때만 EXT2 · 그 밖 비영 rc = EXT2 없이 멈춤 · 판독기 rc 보존 | `ul_runner_test` M21 (첫 `s0p` rc 1 → EXT2 없음 · `reader_s0p_rc=1` 한 번 · 끝 `reader_rc=1`) · 대조 M19 (rc 2 → EXT2) |
| Q5 문법 PASS 강제 | `run_unload.sh` 사전 점검 `grammar_check` — `RJ` · `RJ2` · `EXT` 는 `GRAMMAR_VERDICT` 필수 → `ul_reader.py grammar <판정> --lmp-sha <지금 바이너리>` (`grammar_prereq`) · rc ≠ 0 = LIGGGHTS 전에 멈춤 (`--preflight-only` 도) · 통과 = 잡 기록 `grammar_prereq=PASS` · `grammar_verdict=` · `grammar_verdict_sha256=` · RESTORED 관문이 그 줄도 요구 | R32 (반례 19 · 다른 바이너리 · 양성 · 봉인 값 = history_test 실제 sha256) · M22 (판정 없음 · FAIL · 덱 사본 다름 · LMP 다름 = LIGGGHTS 호출 0 · RJ 폴더 없음 · EXT · preflight-only · 양성 = **지금 history_test 러너 + 읽는 쪽이 낸 판정** · 같은 가짜 바이너리) · 증거 §5 (`039abb141` 러너 · 읽는 쪽 판정 → PASS · 다른 바이너리 REFUSE) |
| Q6 UC | `RESUME=1 UC` = 앞에서 거부 ("fresh-attempt-only" · 기록 그대로) · 새 시도 = 보존된 앞 시도 폴더를 잡 기록 `prior_attempts=` 에 · README §3 (새 폴더는 재시도 한도 · 결과 선택을 초기화하지 않는다 · 판단 = 1저자) | M24 |

**Q5 사전 점검 대조 항목** (`ul_reader.grammar_prereq`): ① 판정 JSON — schema `ps45_unload_grammar_verdict_v1` · status PASS · exit_code 정수 0 · 검사 19 (`GRAMMAR_CHECKS`) 전부 `true`
② 런 — 판정 `run_dir` = 판정 파일이 놓인 폴더 (realpath) · `run_manifest.txt` `mode=gram` · `end` · `lmp_sha256` = 지금 돌릴 바이너리 ③ 덱 출처 — 단계 P · GA · GB 의 `rc` 0 · `deck.txt` ·
덱 사본 (`in.hist_producer` · `in.hist_grammar`) + `plate_hist.stl` sha256 = `GRAMMAR_INPUTS` (`039abb141` 판 · selftest 가 history_test 실제 파일과 대조) · 그 런의 kit `SHA256SUMS`
(sha256 = run_manifest `sums_sha256`) 가 같은 값.  러너 · 읽는 쪽 스크립트 sha256 은 대조하지 않는다 — 이 판의 러너 수정 (Q4 나) 이 `039abb141` 로 낸 실행 2 판정을 무효로 만들지 않게.

## 3. Linux 전체 로그 (판정문 §9-5) — `docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/`

| 명령 (`python3 -I …` · 키트 폴더) | 최종 (`70b3fefed` 와 같은 키트 트리 · 깨끗) | 시험 먼저 (`b1121b6b6` 와 같은 키트 트리) |
|---|---|---|
| `ul_lib` · `ul_s3` · `ul_observers` · `ul_gates` `--selftest` | rc 0 · 21 · 16 · 21 · 37 | rc 1 · 1 · 0 · 1 (2 · 2 · 0 · 1 실패) |
| `ul_reader.py --selftest` | rc 0 · 158/158 | rc 1 · 44 실패 |
| `seal_kit.py --selftest` · `--check` | rc 0 · rc 0 (76 파일 · 규칙 24 · 폐기 0) | rc 0 · rc 0 (규칙 22) |
| `make_unload_decks.py --selftest` · `--check` | rc 0 (291) · rc 0 (덱 64) | 같음 |
| `history_test/make_history_decks.py --selftest` · `--check` | rc 0 · rc 0 (덱 9 · 15 파일) | 같음 |
| `history_test/read_history.py --selftest` (러너 모의 · 보고 묶음 포함) | rc 0 · 56/56 | rc 1 · 3 실패 |
| `ul_runner_test.py --selftest` (모의 러너 전체 · 보고 묶음 M19) | rc 0 · 37/37 | rc 1 · 9 실패 |

- 환경 = Linux · Python 3.11.15 · GNU bash 5.2.21 · LIGGGHTS 없음 (가짜 `mpirun` · `lmp`).  작업 시작 판 `77b5885e0` 도 같은 명령 전부 rc 0 (`baseline_77b5885e0/`).
- 봉인: 키트 `SHA256SUMS` sha256 `3bd18ff6adad9e8656721504bcfb58558bc3655b991bc6e73668ceee39a73767` · `history_test/SHA256SUMS` `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d`.
- 시험 쪽 수정 둘 (쓰기로 연 뒤 읽음) 과 R31 단위 시험 기대 하나의 정정 = 증거 README §4 에 적었다.

## 4. 명령 (Linux · 리뷰 핀 체크아웃 뒤)

```bash
K=docs/data/ps45_unload_20261009
for m in ul_lib ul_s3 ul_observers ul_gates ul_reader; do python3 -I $K/$m.py --selftest | tail -1; done   # 21 · 16 · 21 · 37 · 158 — 전부 PASS
python3 -I $K/seal_kit.py --selftest | tail -1 && python3 -I $K/seal_kit.py --check                        # 76 파일 · 규칙 24 · 폐기 0
python3 -I $K/make_unload_decks.py --selftest | tail -1 && python3 -I $K/make_unload_decks.py --check       # 291 · 덱 64
python3 -I $K/history_test/make_history_decks.py --selftest | tail -1 && python3 -I $K/history_test/make_history_decks.py --check
python3 -I $K/history_test/read_history.py --selftest | tail -1                                           # 56 / 56
python3 -I $K/ul_runner_test.py --selftest | tail -1                                                      # 37 / 37 (bash 필요)
python3 docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/tools/grammar_039_probe.py "$PWD" $K /tmp/gram039.json   # 039abb141 판정 → 사전 점검
```

## 5. 묻는 것

| Q | 무엇 |
|---|---|
| Q1 | `ULKRR-02` 승인 경계 = RESUME 사건 + 러너 `resume_from` + 상태 파일 (`ul_rstep` · `ul_k`) + 행 구조 (버릴 줄 = s_r 뒤 · k > k_r · 앞 줄 = (k_r, s_r) · 새 첫 줄 k_r + 1) — "허가된 재개 경계" 로 충분하고 정상 재개를 막지 않는가 (UTc 의 RESUME 은 부모 경계 · 그 기록에는 역행이 없다) |
| Q2 | `ULKRR-03` 영수증을 읽는 관문 = RJ · RJ2 복원 증서 · RJ2 (EXT 영수증).  개발 · UV · 최종 · 중력 팔 관문은 영수증 대신 런 폴더에서 판정을 다시 계산한다 (판독기가 쓴 `arm_verdict.json` 을 재사용하지 않는다) — 이 범위로 "기술 실패 잡의 산출물을 승인으로 재사용하지 않는다" 가 닫히는가 |
| Q3 | `ULKRR-04` ID 규약 자리 (S0 · 단 끝 · 창 끝 프레임 · 복원 PRE · POST · R_END · UN · S3 쌍 · G2c) 가 빠짐없는가 (G2 는 글자 그대로 int 변환이라 소수가 원래 거부 · 이력 시험 읽는 쪽은 범위 밖 — 실측 H0–H5 판정은 그대로) |
| Q4 | Q5 사전 점검이 "본 R 전" 강제 · 출처 (판정 · 덱 · 같은 바이너리) 대조로 충분한가 · 러너 · 읽는 쪽 스크립트 sha256 을 대조하지 않는 선택이 타당한가 · RESTORED 관문이 `grammar_prereq=PASS` 기록을 요구하는 것 (증서 재사용 쪽) 이 맞는가 · 사전 점검은 판정 JSON 을 **다시 계산하지 않는다** (그 런의 kit 읽는 쪽을 다시 돌리는 것 = 선택 · 손으로 고친 판정의 남는 틈) — 필요한가 |
| Q5 | Q4 (가) — 창 간격 W 를 덱 사본에서 (없으면 표) 읽는 것 · 빈 구간 뒤 연속 두 0 창의 새 선언 허용이 등록 §14-7 과 맞는가 |
| Q6 | 남은 해제 조건 = ibb 실행 2 (실제 바이너리 문법 PASS) 뿐인가 — 그 PASS + 이 판으로 본 R · 10:0 연장 해제 범위가 되는가 |

## 6. 남은 것

- ⬜ ibb 문법 fixture **실행 2** (실제 LIGGGHTS · 1저자 · README §1-6 명령 그대로 · `039abb141` 또는 이 판 = 같은 덱) → 보고 묶음 반입 → 그 `grammar_verdict.json` 이 §3 RJ · RJ2 · EXT 의 `GRAMMAR_VERDICT`.
- ✅ 원장 (`4a8b55013`): `ULKRR-02` · `03` · `04` → claimed_fixed (`e271bdd48`) · `ULKRR-01` = claimed_fixed `039abb141` (남은 증거 = 실행 2 PASS).
- ⛔ 본 R · 10:0 연장 · U = 이 재확인 GO + 실행 2 PASS 뒤.
