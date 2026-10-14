# SUPR-01 · SUPR-02 수정 계획 (2026-10-14 · ✅ 1저자 비준 10-14 (Q1–Q4 권고대로 · *"lhs는 권고대로 하고"*) · 결과 0 건)

> 근거 = Codex 보충 20 수정 재검증 `docs/reviews/codex_review_sup20_fix_reverify_20261014.md` (리뷰 핀 `a9422d2e7`) · 반입 · 우리 트리 재현 = `docs/reviews/codex_sup20_fix_reverify_evidence_20261014/_README_import.md`.
> 판정 요지: SUP20-01 · 02 **닫힘 (verified)** · 새 P1 없음 · 새 P2 둘 (영수증 경로 · Codex 표기 SUP20R-01 · 02 → 원장 `SUPR-01` · `SUPR-02`) · **사전 점검 진입 허용 · 실제 194 · 보충 20 발사와 v1.3 배포 = HOLD**.
> 범위: 고치는 파일 = `scripts/supp20_input_receipt.py` (영수증) · `scripts/run_network_194_parallel.py` (사전 점검 출력) · 등록 §4 명령 문구.  둘 다 수치 봉인 32 (`CODE_FILES` · `code_fp e8b2496b…`) **밖** — 봉인 · 수치 · 계산은 바뀌지 않는다.  실행기 파일 지문은 바뀌므로 발사 manifest 에 기록된다.
>   ⛔ **정정 10-14 (`SELF-112`)** — 위 문장은 거짓이다: 발사 manifest 의 코드 지문 칸은 git sha · 봉인 32 (`code_hashes`) · 인계 도구 (`handover_code_hashes`) 뿐이고 실행기 파일 sha256 칸은 없다.  실행기 판 = git sha · 실행기 파일 지문 = 사전 점검 완료 영수증 `runner.sha256` (§4 ④).

## 1. 결함과 최소 해결 (판정문 §4 · §5 그대로)

| 원장 | 무엇이 새나 | 우리 재현 (10-14 · HEAD) | 최소 해결 |
|---|---|---|---|
| `SUPR-01` | 사전 점검 로그의 입력 지문에 코호트 TSV 해시가 없고 영수증 E1 · 코호트 줄도 이름 · 개수만 본다 → 다른 TSV 로 돈 dry-run 로그가 통과 | `wrong_tsv_full_log` rc 0 | 사전 점검이 실제 쓴 `INPUT_DIGEST_KEYS` 전부 (코호트별 TSV sha 포함) 를 기계가 읽는 출력으로 · 영수증이 등록값 · 반입 재계산과 비교 · 부재 = 거부 · TSV 만 바꾼 로그 거부 시험 상주 |
| `SUPR-02` | E5 가 ⛔ · ✗ 부재만 본다 → 중단 사유 앞에서 잘린 로그 · 필수 검사 줄 셋이 빠진 로그가 통과 | `observation_off_truncated_before_stop` rc 0 · `missing_three_prerequisite_lines` rc 0 · 대조 `observation_off_full_log` rc 1 | 필수 세 항목 + `observe_imports=true` 의 명시 성공 값 · 한 실행에 결합된 완료 상태와 정상 종료 · 원본 전체 로그 · 인자 · 출력 해시 · 종료코드 보존 · 잘린 · 결손 반례 상주 · 등록 §4 grep 명령 정정 |

## 2. 1저자가 정할 것

| Q | 질문 | 선택지 | 권고 |
|---|---|---|---|
| Q1 | `SUPR-01` 입력 지문 연결 | (가) 사전 점검이 `INPUT_DIGEST_JSON {…}` 한 줄 (전체 키 · 코호트별 TSV sha) 을 내고 영수증이 등록 §2 값 · 반입 재계산과 셋을 대조 · 부재 거부 (나) 파일 경로 문자열 대조 | **(가)** — Codex 가 (나) 를 대체로 인정하지 않는다 (판정문 §4 ③) |
| Q2 | `SUPR-02` 완료 증거 | (가) 사전 점검이 끝날 때 구조화 영수증 JSON (필수 세 항목 · `observe_imports` · 완료 표지 · 종료코드 · 인자 · 전체 로그 sha256) 을 원자적으로 쓰고 영수증 도구는 그 JSON + 전체 로그를 요구 (grep 로그 단독 = 거부) (나) 텍스트 로그 유지 + 완료 줄 · 성공 줄 명시 요구 | **(가)** — 판정문 §5 ② "가능하면 구조화 영수증" · 등록 §4 명령은 grep 대신 전체 로그 + JSON 보존으로 정정 |
| Q3 | 같은 도구에서 E2 (로그의 git short) 를 승인 SHA 와 대조할지 (판정문 §6 "추가 범위 주의" — 새 결함 아님) | (가) `--approved-sha` 인자로 대조 · 부재 = 경고 (나) 그대로 | **(가)** — 같은 파일 · 작은 변경 · 발사 핀 확인이 손으로만 남지 않게 |
| Q4 | 발사 승인을 미리 적을 때의 문구 | 판정문 §3 문구 그대로 | **그대로** — *"수정본의 사전 점검 착수를 승인한다. 실제 생산 발사는 최종 핀의 fast16+real4, 깨끗한 트리, 두 새 ROOT, import 관측 ON, 전체 입력 지문 일치와 정상 dry-run 완료가 모두 확인된 뒤에만 허용한다."* |

> ✅ **1저자 비준 10-14** — Q1–Q4 **권고대로** (Q1 (가) `INPUT_DIGEST_JSON` 한 줄 · 셋 대조 · Q2 (가) 구조화 완료 영수증 + 전체 로그 · grep 로그 단독 거부 · Q3 (가) `--approved-sha` · 부재 = 경고 · Q4 = 판정문 §3 문구 그대로) ·
> 1저자 *"lhs는 권고대로 하고"* → §3 순서대로 (반례 먼저).  Q4 문구는 조건부 승인이다 — 실제 발사 승인이 아니다.

## 3. 순서 (비준 뒤)

1. 반례 먼저 — Codex 로그 셋 (`wrong_tsv_full_log` · `observation_off_truncated_before_stop` · `missing_three_prerequisite_lines`) 을 영수증 시험에 상주 → 고치기 전 실패 확인 · 정상 로그 · `observation_off_full_log` 대조.
2. Q1 · Q2 (· Q3) 구현 → 영수증 · 실행기 자체 시험 · `test_lhs_release_v13` · 게이트.
3. 등록 §4 명령 정정 (보충 20 등록 · 194 등록의 사전 점검 줄) — 결과 0 건 문구 정정.
4. Codex 짧은 재확인 (수정 diff + 반례 재실행) → 판정문 §6 의 2–7 단계 (WSL 사전 점검 → 1저자 실제 발사 승인 → 194 → 보충 20 → 배치별 감사 · 다시 읽기 · τ/인계 관문 → v1.3 결합 관문).

## 4. 실행 기록 (10-14 · 결과 0 건 — 수치 · 봉인 32 · 계산 무변경)

| 단계 | 커밋 | 내용 |
|---|---|---|
| ① 비준 기록 | `df43b1210` | 이 문서 머리 · §2 끝 |
| ② 반례 먼저 | `df45a6219` | 영수증 시험 (a)–(i) + 등록 명령 밖 인자 · 승인 SHA · Codex 로그 다섯 · 실행기 시험 ㊲a–㊲i — 고치기 전 코드에서 실패 확인 |
| ③ 구현 | `8af6cbae3` | Q1 · Q2 · Q3 — 실행기 `scripts/run_network_194_parallel.py` · 영수증 도구 `scripts/supp20_input_receipt.py` (둘 다 봉인 32 · HANDOVER_FILES 밖) |
| ④ 문서 | 이 기록을 담은 커밋 | 등록 §4 정정 둘 · 10-12 수정 계획 "영수증 쓰는 법" 의 옛 tee · `--dry-run-log` 블록 아래 정정 표지 한 줄 (원문 보존) · 이 기록 · 재확인 요청서 `docs/reviews/codex_supr_fix_reverify_request_20261014.md` · 시험 등재 두 줄 |

| Q | 구현 |
|---|---|
| Q1 (`SUPR-01`) | 실행기 화면에 `INPUT_DIGEST_JSON {…}` 한 줄 (`INPUT_DIGEST_KEYS` 전부 · 코호트별 TSV sha256 · 사람이 읽는 줄은 그대로) · 영수증 도구 E1 = 로그의 그 한 줄 = 등록 §2 = 반입 파일 재계산 (실행기 `plan_input_digest`) · 부재 · 둘 · JSON 아님 · 키 결손 = 거부 · 경로 문자열 비교 없음 |
| Q2 (`SUPR-02`) | `run --dry-run --preflight-receipt P.json` — 실행기가 자기 화면 전체를 직접 잡아 P.log + 영수증 JSON 을 원자적으로 (로그 먼저) · 멈춰도 · LaunchError 여도 (실제 종료코드 · 멈춘 사유) · `--dry-run` 없이 · ROOT 안 · 이미 있는 영수증 = 거부 · 끝까지 돈 dry-run 의 마지막 줄 `PREFLIGHT_DRY_RUN_COMPLETE rc 0` · 필수 세 검사 = 명시 성공 값 (`preflight_check_values` — 값이 없으면 ✗) · 대조 = 실행기 `preflight_receipt_checks` P0–P10 (194 · 보충 20 공용 · CLI `preflight-verify`) · 영수증 도구 `--preflight-receipt` = P0–P10 + E1 · E2 · `--dry-run-log` (텍스트 로그 단독) = E0 거부 |
| Q3 | `--approved-sha` (7–40 hex · 접두) = 사전 점검 영수증 git sha · 로그 짧은 sha (P10) · manifest git.sha (F7 · G7) · 부재 = notes 경고 (실패 아님) |
| Q4 | 문구만 (이 문서 §2) — 실제 발사 승인 아님 |

| 시험 | 고치기 전 (반례만 더함) | 고친 뒤 |
|---|---|---|
| `scripts/supp20_input_receipt.py --selftest` | **32/88** (56 FAIL — 새 반례 58 중 옛 판도 거부하던 둘 = 관측 OFF 전체 화면 · Codex `observation_off_full_log` 만 통과) | **88/88** (12 s) |
| `scripts/run_network_194_parallel.py --selftest` | **130/139** (㊲ 9 FAIL) | **139/139** (86 s) |
| `scripts/supp20_input_receipt.py` (컨테이너 범위) | rc 0 · 11 칸 | rc 0 · 11 칸 (+ notes 경고 — `--approved-sha` 없음) |
| `scripts/test_lhs_release_v13.py` | 256/256 | 256/256 |
| `check_doc_refs` · ban-sweep · `check_method_discipline` · `check_selftest_inventory` | — | 전부 통과 (전체 게이트 `check_all.sh` = 병합 뒤 본 세션) |
| 봉인 32 (실행기 `code_fp(code_hashes())`) | `e8b2496b…` | 같음 |

Codex 반례 로그 다섯 (`evidence/receipt_extra/` · 바이트 그대로 · `--dry-run-log`):

| 로그 | 고치기 전 | 고친 뒤 (CLI) | 고친 뒤 · 정상 영수증에 넣은 위조 포장 (selftest S10b) |
|---|---|---|---|
| `wrong_tsv_full_log.log` | rc 0 | rc 1 (E0) | 거부 (INPUT_DIGEST_JSON 없음 P2 · 완료 표지 없음 P3 ⊆ 실패) |
| `wrong_tsv_registered_grep.log` | rc 0 | rc 1 (E0) | 거부 (같음) |
| `observation_off_full_log.log` | rc 1 | rc 1 (E0) | 거부 (같음) |
| `observation_off_truncated_before_stop.log` | rc 0 | rc 1 (E0) | 거부 (같음) |
| `missing_three_prerequisite_lines.log` | rc 0 | rc 1 (E0) | 거부 (같음) |

- (a) 의 값 거부: 같은 20 ID · raw 표 · 코호트 TSV 첫 행 `deck_sha256` 한 글자만 바꾼 파일 (실제 `build_plan` · `plan_input_digest` · `print_preflight` · 실행기 rc 0 · 새 꼴 로그가 그 TSV sha 를 싣는다) → 실패 칸 = **E1 · P9 둘뿐** · Codex `alternate_cohort.tsv` (sha256 `8d5dcbd2…`) 도 같음.
- 반례 시험은 진짜 실행기 dry-run (`NP.main`) 을 돈다 — 대역 = `git_info` (깨끗한 트리) · `raw_problems` (원 dump 는 WSL 에만) · `_guard_posix` (윈도 검토 환경) + 한 번 잰 진짜 `derive_generation` · `code_dependency_closure` · `lazy_import_census` 재사용 (시간만).

### 계획과 다른 점 · 정정

1. **대조 함수는 실행기에** (`preflight_receipt_checks` · `parse_preflight_log` — 화면 생산자와 같은 파일) — 영수증 도구는 그것을 부르고 등록 값 대조 (E1 · E2) 만 더한다.  옛 텍스트 화면 대조 E1–E6 · 줄 꼴 정규식 사본은 지웠다 (규율 ①).
2. **Q3 를 manifest 에도** (F7 · G7) — 같은 인자 · 같은 목적 (판정문 §6 "H1 은 두 manifest 의 상호 일치이지 승인 핀과의 일치가 아니다").
3. **194 쪽 등록 §2 값 대조 칸 없음** — `preflight-verify` 는 로그 = 영수증 = 이 체크아웃 재계산 · ID 지문 (등록 집합 production194) 까지 · raw 표 `da7c93f9…` · 코호트 TSV 둘은 문서에서 읽어 대조하지 않는다 (보충 20 은 영수증 도구 E1) → 194 등록 §4 정정 블록에 손 대조 줄을 적었다 (옛 grep 줄과 같은 수준).  10-14 HEAD 에서 §2 표 = 커밋된 입력 재계산 (같음 · 읽기 전용 확인).  ⬜ 자동화할지 = 1저자.
4. **머리 범위 줄 "실행기 파일 지문은 바뀌므로 발사 manifest 에 기록된다" 정정** — manifest 의 코드 지문 칸은 git sha · 봉인 32 (`code_hashes`) · 인계 도구 (`handover_code_hashes`) 뿐이다 (실행기 파일 sha256 칸은 없다 · 실행기 판은 git sha 로만) · 실행기 파일 지문 = 완료 영수증 `runner.sha256` · 영수증 도구 `recorded.tool_sha256`.
5. **194 등록 §1 단계 2 의 dry-run 줄** (`--observe-imports` 없음) — §3b (10-09 비준) 뒤 사전 점검 ⛔ (rc 2) 인 줄이었다 · 원문 그대로 두고 주석 두 줄 (§4 정정 블록과 같은 꼴로) 만 더했다.
6. **화면의 필수 세 검사** — 값이 비었거나 꼴이 다르면 이제 ✗ (옛: ✓) · 실제 사전 점검은 늘 값이 있어 생산 화면은 같은 글자.
7. 영수증 이름 — 이미 있으면 거부 (옛 증거를 덮지 않는다) → 등록 명령은 시각을 붙인 이름 (`${R}_preflight_<월일_시분초>.json`).
