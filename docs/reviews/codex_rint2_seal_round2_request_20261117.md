# Codex 봉인 전 묶음 2/2 — Rint ② 측정 결과 (⑥ 시도 3 · 4 · S0 단계 1 · Q11 최종 핀) + 봉인 숫자 · 봉인 꼴 (2026-11-17 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 1/2 (11-13 · 코드 묶음 · 측정 블록 설계 · HOLD · 새 P1 없음 → 고침 → 독립 재확인으로 RCPX-01–06 범위 한정 종결 · 전체 HOLD 그대로) 뒤 남은 한 번이다.  (1) 측정 셋이 봉인 숫자를 받치는지, (2) 봉인 꼴 (봉인본 = 새 파일) 이 등록 R 의 "봉인" 뜻을 지키는지, (3) 12 단위 · 원장 이어달리기 · 저장본 · 넘침 점 규칙 문장에 정직한 흐름에서 틀린 결과를 받는 길이 있는지를 반박해 달라.
> **리뷰 핀** = 이 요청서가 든 stoic 커밋 (40 자리 = ZIP PIN.txt · 가지 `claude/stoic-knuth-NObVQ`) · **코드 핀** = `64e4d213e8267bafaf3ae5af00a42996cefd3f33` (원격 `codex/rint-rtr01-receipt-1113` 끝 · 측정 셋의 핀 · 봉인 바탕) · **봉인 꼴** = scratch 커밋 c80d700bdd5915da82f77f839cb96ed4a5a6582e (부모 = 코드 핀 · 원격에 올리지 않음 · ZIP 의 extra/seal_candidate_v2_1/seal_form_G2_20261117.bundle 가지 seal-form-scratch · 묶음 sha256 6e8e1e2d5b104557d6701cf0ebfd53b80492e749652b4cca04c7a696d7af4313 · 봉인 날짜 자리 = 보기 20261120).
> **지위**: 결과 0 건 · σ 열람 0 · 봉인 전 · R 런 0.  봉인 후보는 내부 반박 리뷰 한 회 (독립 조수 · Codex 아님 · P1 0) 와 그 고침 (v2.1 · 시험 먼저) 을 거쳤다 (§7).

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 |
|---|---|
| ① 측정 결과가 봉인 숫자를 받치나 — ⑥ 시도 3 · 4 (11-16 · 코드 핀) · S0 단계 1 채택 확인 (E1–E4 · T1–T3) · Q11 최종 핀 (합성 계 다섯 쌍 비트 같음 · adopt True) (§2 · Q2 · Q6) | 결과 전 등록 넷의 **값** (`max_ladder_points` · `calib_rj_ratio_max` · `sv_cf_threshold` · `sv_cf_scope`) — Codex 의견 (Q3) 뒤 1저자 · S0 단계 2 전 |
| ② 봉인 숫자 — maxiter 5,000,000 · `max_hours` 168 · `max_attempts` 8 · 허용 기계 kgy · gabia · v100 · env_unit (3.8 · 1.24.4 · 1.10.1) · 넘침 점 배정 112 h 규칙 · 3 판 시간 어림 (§3 · Q2) | R 런 결과 · σ 값 · 감도 단계 (FIBRE · UNREG · GRID · SVORDER) 경로 (R 시작 전 따로 · 1저자 Q8) |
| ③ 봉인 꼴 — 봉인본 새 파일 · 원본 등록 R = 핀 판 + 머리 표지 한 줄 · 사슬 `--registration` · S0 단계 2 `--r-doc` · `scripts/` 무변경 → ⑥ 다시 없음 · 인자 누락 = 원본 (해시 ⬜) → `PLAN_HASH_UNREGISTERED` 멈춤 (§4 · Q1) | 봉인 날짜 · 가지 이름 · 봉인 커밋 · push · 두 기계 조립 같음 (11-12 Q10) · 봉인 직전 현장 확인 (PIN = 봉인 커밋) |
| ④ 12 단위 sh 블록 · 원장 이어달리기 (가-2) + `flock` 넘김 · 저장본 (기계마다 새 빈 폴더 `~/ca1_cjstore`) · 넘침 점 배정 규칙 문장 (§5 · Q4) | 넘김 수단 (1저자) · 운영 중 배정 |
| ⑤ 봉인 가지 문서 참조 처분 · `claims.json` = stoic 바이트 (§4 · Q5) · RCA-11 (P2 open) 이 봉인 값으로 이 R 에 한해 닫히는지 (Q7) | 열린 P3 (`RIMPR-04` · `P6R3-01` · `02` · `03` · `05`) · `RTR-01` · `RTRR-01` (owner codex · claimed_fixed) — §10 한정 |

## 1. 보내는 것 (ZIP · repo/ = 리뷰 핀 blob 그대로 · extra/ · PIN.txt · ZIP_MANIFEST.tsv)

만드는 법 = `docs/reviews/rint2_seal_round2_20261117/build_zip.py` (`--paths` = 같은 폴더 `zip_paths.txt` · repo/ 파일마다 git blob sha1 다시 대조 · 같은 입력 = 같은 바이트).

| 묶음 | 파일 |
|---|---|
| 이 요청서 · 기록 | `docs/reviews/codex_rint2_seal_round2_request_20261117.md` · `docs/reviews/rint2_seal_round2_20261117/` (README · 기록 묶음 tgz = 봉인 후보 v2 · v2.1 · 내부 리뷰 + 재현 · 도구 · 경로 목록) |
| 측정 기록 | `docs/data/rint2_probe6_a3_20261116/` · `docs/data/rint2_probe6_a4_20261116/` · `docs/data/rint2_s0_sbe_20261116/` (`ADOPTION_CHECK.md` 포함) · `docs/data/rint2_q11_gpu_check_kgy_20261116/` · S0 결과 전 등록 `docs/reviews/rint2_s0_store_probe_20261112/README.md` · `docs/reviews/rint2_q14_finalpin_preparation_20261113/` |
| 시간 · 결정 · 원장 | `docs/reviews/rint2_time_reestimate_20261111/README.md` (끝 절 = 3 판 · §3-6b · §3-6c 결정) + `v3/` · `docs/reviews/rint2_dev_probe_ledger_20261026.md` · `docs/reviews/findings.json` |
| 등록 · 명령 (리뷰 핀 blob = 코드 핀 blob 같음) | `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · `docs/reviews/rint2_kgy_commands_20261020.md` |
| 1/2 기록 | `docs/reviews/codex_rint2_codepkg_review_request_20261113.md` · `docs/reviews/rint2_codepkg_20261113/codex_rebuttal1_fixes_README.md` · `docs/reviews/rint2_rtr01_destination_audit_20261113/received_verdict.md` |
| extra/ (리포에 풀어 두지 않은 것) | seal_candidate_v2_1/ (README · 도구 · 조각 둘 · 계획 후보 · 도구 출력 · 증거 · 봉인 꼴 묶음) · internal_review/ (REVIEW.md · repro/) · code_pin_tree.txt (코드 핀 `git ls-tree -r`) · README.txt |

## 2. 측정 결과 (원자료 = 위 폴더 · σ 없음)

| 측정 | 핀 · 기계 | 결과 |
|---|---|---|
| ⑥ 시도 3 (11-16 13:12:08 → 15:42:53 KST · 저장본 켬 · 빈 폴더 → 짓고 씀) | `64e4d213e` · kgy (Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0 · RTX 3090) | 판독 rc 0 (PROBE_OK · 증서 POSITIVE_SOLVED · ⓐ–ⓓ 참) · 미지수 26,529,223 · 주 풀이 277,885 반복 · 이어 풀기 84,485 · 잔차 1.0519e-12 · 판 전류 불균형 9.63612e-07 · 9,045 s (탄소 접합 목록 짓기 4,223 s) · RSS 최대 34,349,912 kB · audit `built_written` |
| ⑥ 시도 4 (15:54:26 → 17:16:38 KST · 시도 3 저장본 그대로 → 읽음) | 같음 · `code_same_as_attempt3=1` | 판독 rc 0 · 위와 같은 반복 · 잔차 · 불균형 · 4,932 s (목록 읽기 88 s) · RSS 최대 34,164,888 kB · audit `hit` · **팔 JSON = 시도 3 과 바이트 같음** · 결과 전 기대 (같은 칸 · 준비 초 4 < 3) 맞음 |
| 견줌: ⑥ 시도 2 (11-11 · 핀 `5bca50c88` · A 꼴 · 저장본 없음) | kgy | 주 277,885 · 이어 84,485 · 잔차 1.0519e-12 · 불균형 9.63612e-07 (판독기 출력 자릿수 안에서 시도 3 · 4 와 같음 [관찰]) · 22,345 s → 시도 2 ÷ 4 = 4.53 · 2 ÷ 3 = 2.47 [산술] |
| S0 단계 1 다시 (11-16 00:48:09 → 02:20:56 UTC) | `64e4d213e` · kgy | 결과 전 기대 E1–E4 · 문턱 T1–T3 모두 기대대로 (`ADOPTION_CHECK.md`) · n_instances 117,583 · S0 계획 sha256 `6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520` · 쓰기 120.095 s · 읽기 86.327 s (짓기의 2.15 %) · VmHWM 증가 0.67 GiB · 저장본 파일 1,340,095,705 B · kit JSON 508 칸 중 11-13 과 다른 7 = 허용 목록 · 코드 지문 7/7 = 핀 blob |
| Q11 최종 핀 (11-16 01:07:35Z → 01:11:59Z · 합성 계 n 26,463,592 · 실침대 아님) | 옛 `11a794674` ↔ 새 `64e4d213e` · kgy | 다섯 쌍 비트 같음 (control 둘 · short 200 · main 2,631 · resolve 621) · main 반복당 0.048628 → 0.010934 s = 4.447 배 (S0 가 같은 기계에서 도는 중 · 참고값) · `CONSUME adopt = True` |

## 3. 봉인 숫자와 근거 (값 = 1저자 11-17 결정 · 3 판 §3-4 · §3-6b · §3-6c)

| 칸 | 값 | 근거 (3 판 산술 · 추정 표지 그대로) |
|---|---|---|
| maxiter (`p2_extra` = `--step3-maxiter 5000000`) | 5,000,000 | SBE 주 풀이 277,885 의 17.99 배 · 한도까지 한 풀이 kgy 14.6 h · gabia 21.2 h (s 1) · 옛 세대 DBE ÷ SBE 반복 비 (4.34, 8.68] × m 2 = 17.4 배를 덮음 (여유 1.04 · 새 세대에서 그 비가 맞는다는 근거 없음 [추정]) |
| `exec_policy.max_hours` | 168 | 가장 긴 한 런 = gabia 첫 넘침 점 (8 팔 · 짓기 5) 60.4 h (DBE 2.933 · m 1) → 2.78 배 · DBE 두 배 1.39 · m 2 1.74 · 둘 다 0.87 (못 덮음) |
| `exec_policy.max_attempts` | 8 | 채택 = 원장 차례로 처음 "결과 전 멈춤이 아닌" 시도 → 수가 커도 고르는 길이 늘지 않음 · 10-19 꼴 (풀기 전 멈춤 넷) 뒤에도 셋 남음 |
| 허용 기계 · env_unit | kgy · gabia · v100 · 3.8 · 1.24.4 · 1.10.1 | R venv = 두 기계 `~/dem-venv` (3.8.10 · 1.24.4 · 1.10.1 · cupy 12.3.0 · 11-17 현장 확인 [1저자 출력]) |
| 넘침 점 배정 규칙 | 그 기계의 첫 점 어림 > 112 h (= 168 의 2/3) 이면 주지 않음 · 둘 다 넘으면 멈추고 1저자 | 168 h 를 넘는 8 팔 점은 결과 뒤 TIME_LIMIT → 같은 기계 재실행만 · 끝나지 못함 · 어림 꼴 = 3 판 §3-3 (4) "팔 전체" (kgy 49.0 h · gabia 60.4 h) |
| 마감 | 12-05 (토) 24:00 KST (GPU 팔 끝) | 3 판 본 표 (사슬 꼴 · gabia GPU 1.456 배 · 단위 7 / 5 · DBE 비 2.933 · m 1): s 1 · 팔 전체 184.2–208.7 h → 11-20 00:00 시작이면 11-27 16시 – 11-28 16시 · 여유 175.3–199.8 h · 넘김 지연 d h 면 끝 + 7d [추정] |

## 4. 봉인 꼴 (봉인 후보 v2.1 · extra/seal_candidate_v2_1/README.md)

- **꼴** = 봉인본 새 파일 `docs/reviews/rint2_seal_<날짜>/registration_R_sealed.md` (원본 747 줄이 순서대로 다 있고 바뀐 줄 = 숫자 칸 · 해시 칸 · 블록 자리뿐 · 도구 `make_sealed_copy.py` 가 핀 판 원본 + 조각 + 계획 파일에서 만든다 · 같은 입력 = 같은 바이트) · 원본 등록 R = 핀 판 + 머리 표지 한 줄 (해시 칸 ⬜ 그대로) · 명령 문서 = 제자리 고침 (K 조각) · 계획 = `docs/data/rint2_r_plan_<날짜>/ca1_plan.json` (`rint-r-plan-v3` · 후보 sha256 f09b3efbe50d104d7e294a6b3dce8bda5214d267a4fecfc99b7e50023396d3c4 = 넷 null · 봉인 값 아님 · 봉인 때 도구 `--final` 필수).
- **왜 새 파일인가** — 같은 원본에 블록을 넣으면 시험 PC18 · EP06 · E17 이 실패 (실제 등록 R 에 블록이 없다는 가정) → 시험을 고치면 `scripts/` 변경 → 원장 §2 로 ⑥ 다시 재기 · 새 파일이면 둘 다 피한다.
- **봉인 꼴 커밋 (v2.1 · c80d700bd · 그 앞 판 0a6939cb3 = 봉인 기록 폴더 README · 증거만 다름) 에서 잰 것** [후보 실측 · 내부 리뷰가 v2 판에서 따로 재현 §7]: 사슬 시험 전체 506/506 (538.0 s) · E17 1/1 · K01 · PC18 · PC20 · EP06 4/4 · 두 문서 sh 블록 사슬 명령 (봉인본 13 + S0 1 · 명령 문서 14 + 1) 전부 `--registration` / `--r-doc` = 봉인본 · 독립 셈과 같음 · 문제 0 · `--stage plan-doc --check-doc --registration <봉인본>` rc 0 `PLAN_DOC_SAME` · 기본 (원본) rc 3 · S0 단계 2 관문 (`verify_plan_commit(..., r_doc=봉인본)`) = 후보는 결과 전 넷 null 사유로 거부 · 기본 r_doc 거부 · 고정물 값 계획 (`--final`) 통과 · 원본 자리 · 원장을 읽는 게이트 시험 셋 357 · 84 · 186 (FAIL 0) · 핀 판 규율 검사 0 오류 (경고 17) · 문서 참조 rc 0 · 철회값 스윕 (바뀐 파일 83) 문제 0 · 다섯 경로 · CODE_FILES 20 · S0 일곱 안의 바뀐 파일 0.
- **봉인 값** — v2 와 바이트 같음 (계획 후보 · 원본 자리 sha256 1cf4a7b4… · u · tol_ff · tol_P · tol_sj · S0 해시 · maxiter · 168 h · 8 · 기계 · env_unit) · 봉인본 · 명령 문서 바이트는 v2.1 글 고침으로 바뀜 (봉인본 sha256 3787864a… · 명령 문서 bef29b6b…).
- **봉인 가지에 넣는 것 · 가리키는 것** — 넣음: 봉인 기록 폴더 (README · 도구 · 조각 · 증거) · 봉인본 · 원본 자리 (표지) · 명령 문서 · 원장 (stoic 바이트) · 계획 · 자료 폴더 셋 (S0 · ⑥ 시도 3 · 4) · q14 준비 두 파일 · `docs/reviews/claims.json` (stoic `2da71fe5a` 바이트 = 핀 판과의 차이가 11-16 S0 kit JSON 사본의 `allowed_in` 두 덩어리뿐 · 없으면 철회값 스윕 4 건) · 가리킴 (넣지 않음): 3 판 README · `v3/` = stoic 커밋 · 경로 · blob (그 커밋 `b3481336c` · `b80f10d08` · `c0c3b1ff5` 는 11-17 07:09 UTC 측정으로 원격 stoic 안).

## 5. 12 단위 · 원장 이어달리기 · 저장본 · 넘침 점 (봉인본 §10-1b · §10-6 – §10-8 · 명령 문서 §3-1b)

- 사다리 P0 = kgy · P1 = gabia · 12 단위 첫 배정 kgy 7 · gabia 5 · 합치는 기계 = kgy · 합친 폴더 `ca1_predict` · `ca1_predict_x` (봉인 밖).
- 원장 공유 (가-2) = 두 대 동시 · 단위 시작 뒤 원장을 넘김 (`<원장>/.git/rint_r_ledger.lock` 에 `flock` · 대기 상한 120 s = 사슬 `LEDGER_LOCK_WAIT_S`) · 받는 쪽 = 세워 둔 자리에서 먼저 `pull --ff-only` 뒤 되살림 · 끝 커밋 = 넘김 기록이면 `RECV_OK` (v2.1) · 끝난 사슬 rc 3 → 원장이 돌아온 뒤 `--stage recover` · 넘김 수단 = 1저자.
- 저장본 = 기계마다 새 빈 폴더 `~/ca1_cjstore` (⑥ · S0 시험 저장본 안 씀).
- 실행 트리 = 기존 트리 저장소에서 새로 뗌 · 봉인 직전 확인 줄 = 두 기계 같은 한 줄 (기대 `3.8.10 1.24.4 1.10.1 12.3.0`) · S0 단계 2 줄 = venv 켬 + 판 출력 + same-version 확인 `&&` 뒤 실행 · rc 줄 (v2.1).

## 6. 결과 전 등록 넷 (값 = 1저자 · Codex 의견만)

| 칸 | 등록 글이 지금 말하는 것 |
|---|---|
| `max_ladder_points` | "점 수 상한 12 … 상한 = ⬜" · RCA-01 회로 = 정확히 12 점 · 천장 근처 꺾임 망 = 13 점 · 사슬에 기본값 없음 · 3 판 시간 표 = 법칙마다 12 점 가정 (점 하나 = kgy 1.4 h · gabia 1.9 h) |
| `calib_rj_ratio_max` | "폭 상한 (넘으면 `CALIB_UNIDENTIFIED`) = ⬜" · 권고 숫자 없음 · `'none'` = 상한 없음으로 등록 가능 |
| `sv_cf_threshold` | "비 문턱 (넘으면 `SV_DEPENDENT` · 차단) = ⬜" · 꼴 = 유한 ≥ 1 |
| `sv_cf_scope` | 기록된 결정 = `all3` (10-23 · 재검토 수정 계획 Q5 (가)) · 칸 표시는 봉인 때 |

## 7. 내부 반박 리뷰 (독립 조수 · Codex 아님 · 배경 · 닫힘 근거 아님 · 기록 = 기록 묶음 tgz · extra/internal_review/)

- 대상 = v2 봉인 꼴 커밋 (bea3cb33a) · sparse 사본에서 다시 잼 · 결과 = **P1 0 · P2 2 · P3 12** · 권고 = 봉인 보류 안 함.  P1 후보로 끝까지 본 넷 (빠진 `--registration` · `--r-doc` · 두 기계 절대 경로 차 · 원장 넘김 창 (흉내) · `claims.json` 바꿈) = 모두 결과 전 멈춤 또는 판정 무관.
- **P2-1** 증거 ③ 도구가 꼴이 다른 명령 줄을 조용히 빼고 rc 0 (변이 D2 · D3 · D4 · D8b · D10) → v2.1 고침 · 도구 자기 시험 6/19 → 19/19 (고치기 전 판에서 빠뜨림 재현 뒤).
- **P2-2** 봉인 도구가 계획이 실제로 돌 수 있는지 (두 계획 대조 · 결과 전 넷 · Q3 꼴) 를 안 봄 → v2.1 고침 · 도구 자기 시험 17/35 → 35/35 (v2 의 17 그대로 통과) · 리뷰 변이 34 중 거부 19 → 30 (남은 통과 4 = 설계대로) · 리뷰의 틀린 계획 다섯 = 봉인본을 만들기 전에 rc 2.
- **P3 12** = 고침 7 (측정 시점 표지 · 조각 꼴 허점 · (2b) venv · 판 출력 · rc · 받는 쪽 차례 · 증거 도구 날짜 인자 · 값 대조 · 작은 글 (러너 통과 줄 733)) · 한정 5 (§10).
- 숫자 대조 = 틀림 1 (러너 줄 734 → 733 · 고침) · 낡음 3 (측정 뒤 원격 상태 · 고침) · 그 밖 줄 번호 106/107 · 크기 · sha · 셈 · 3 판 산술 맞음.

## 8. Codex 질문 (반증 가능한 꼴)

- **Q1 (봉인 꼴)** 봉인본 = 새 파일 꼴이 등록 R 의 "봉인" 뜻을 지키나 — 정직한 흐름 (끊김 · 재부팅 · 다른 기계 재실행 · 폴더 옮김) 에서 어느 단계가 원본 (해시 ⬜) 이나 다른 문서를 읽고 결과를 받아들이는 반례가 있나.  인자 누락 fail-closed (`PLAN_HASH_UNREGISTERED`) 로 충분한가.
- **Q2 (숫자 ↔ 측정)** 5,000,000 · 168 h · 8 · 112 h 규칙이 §2 실측과 3 판 모형에서 따라 나오나 — 특히 DBE 반복 비를 봉인 전에 못 잰다는 한정 아래 5,000,000 이 결과 뒤 NOT_COMPUTED 를 막는 값으로 충분한가.
- **Q3 (결과 전 넷)** §6 의 넷에 대한 의견 (값 결정 = 1저자).
- **Q4 (12 단위 · 이어달리기 · 저장본 · 넘침 점)** §5 문장의 빈틈 — 정직한 흐름에서 틀린 결과를 받는 길 (재개 규칙 처분 기준 = 우리 규칙 ⑤ · 손으로 고친 · 어긋난 기록은 멈춤 확인만).
- **Q5 (봉인 가지 참조 · 등록부)** 3 판을 넣지 않고 stoic 커밋 · 경로 · blob 으로 가리키는 처분 · `claims.json` = stoic 바이트 · q14 두 파일 넣음 — 받을 수 있나.
- **Q6 (코드 핀 채택)** `scripts/` 무변경 · 원장 §2 핀 칸 = 풀이 코드 목록 기준 (11-12 Q5) 이라 ⑥ 다시 재기 없이 `64e4d213e` 의 시도 3 · 4 · S0 · Q11 을 R 의 근거로 쓰는 것이 맞나.
- **Q7 (RCA-11 · P2 open)** S0 "수식 고정" 의 표본화 의존 (u = 점 간격 중앙값 / 2) · s_min 자유 선택 — 봉인이 S0 계획 값 (u · tol_ff = 0.07381254285530132 µm · s_min 0 µm) 을 고정하는 것으로 이 R 에 한해 닫히나.
- **Q8 (GO 조건)** 이 묶음과 "봉인 GO" 사이에 남은 최소 조건 목록.

## 9. 다시 돌리는 법

- 봉인 꼴: `git clone --shared --no-checkout <리포> <사본>` → 사본에서 묶음 (extra/seal_candidate_v2_1/seal_form_G2_20261117.bundle) 의 `refs/heads/seal-form-scratch` 를 fetch (전제 커밋 = 코드 핀) → checkout → extra/seal_candidate_v2_1/README.md §아 의 명령.
- 측정: 위 기록 폴더의 SHA256SUMS · README 대조표.

## 10. 한정 (알려진 것 — 새 결함으로 다시 세지 말고 받을 수 있는지만)

- (v2.1 한정 ①) S0 단계 2 관문 결과 "후보 = 넷 null 사유로 거부" 는 관문의 첫 실패만 보인다 — 뒤 대조 (tol_ff · len_law) 의 증거 = 고정물 값 계획 통과 + v2.1 도구의 만들기 전 거부.
- (②) 사슬 `--check-doc` rc 0 = 블록 같음 (계획 바이트 아님) · 계획 바이트를 묶는 것 = 단계마다 해시 줄 대조 · `--stage ledger --init` 은 등록을 읽지 않는다.
- (③) 넘김 기록 표는 실행 트리 밖 사본에 적는다 (실행 트리 안 문서를 고치면 `CODE_PIN_MISMATCH` 로 멈춤 · 틀린 결과 없음).
- (④) `--registration` 을 빼면 멈추지만 시도 하나 (최대 8) · 판정 폴더 하나를 쓴다.
- (⑤) 원본 자리 머리 표지 한 줄로 원본 줄 번호가 핀 판보다 1 밀린다 (판 없이 줄 번호를 적은 문서 6 개 · 55 줄 · 리뷰 실측).
- env_unit 만 틀린 계획은 봉인 도구가 보지 않는다 (사슬이 결과 전에 `CODE_PIN_MISMATCH` 로 멈춤) · 증거 ③ 도구는 `--out` 값 · 단위 이름 ↔ 첫 배정을 보지 않는다 · 원장 넘김 흉내 도구는 봉인 커밋 밖 (파일 구성을 앞 판과 같게).
- `scripts/check_doc_refs.py` 는 한 백틱 안 `<커밋>:<경로>` 꼴을 읽지 않는다 → stoic 가리킴은 `git cat-file -e` 로 따로 확인했다.
- 봉인 꼴 트리에서 리포 게이트 전체는 돌리지 않았다 (`scripts/test_rint_r_chain_e2e.py` 전체 · `scripts/test_rint_r_chain_e2e12.py`) [미확인].
- 열린 P3 (`RIMPR-04` · `P6R3-01` · `02` · `03` · `05`) · `RTR-01` · `RTRR-01` (owner codex · claimed_fixed · 구현자 = 검증자 규약으로 verified 로 올리지 않음).
- 남은 현장 [미확인]: 기존 트리 `origin` 이 봉인 가지를 받는지 · DBE 저장본 파일 크기 · 실침대 C 꼴 속도 (gabia) · kgy GPU · 드라이버 (봉인 직전 줄) · PIN = 봉인 커밋 확인 · 두 기계 조립 같음 · kgy git 2.25.1 에서 `-c pull.rebase=false` 효과 [추정].
