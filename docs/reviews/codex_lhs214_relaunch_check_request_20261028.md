# Codex 짧은 발사 확인 요청 — LHS214 다시 발사 다섯 단계 · 새 판 (2026-10-28 · B7 `35f032737` · ⬜ 리뷰 핀 = 메인 · 발송 = 1저자)

- 대신하는 것 = 초안 2 `docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` (10-21 · 미발송 · 고치지 않음).  고친 것 = 실행표 `docs/reviews/lhs214_relaunch_exec_sheet_20261027.md` §2-2 표 여섯 줄 (§7) + 10-28 사실 (B7 · WSL 반입 · S1 판정 · 194 손 대조 · `L214P-02`).
- 묻는 것 = 둘 (§4) — **Q1** 다섯 단계 ①–④ 가 끝났나 · **Q2** 실제 214 발사 (194 → 보충 20 · 같은 핀) GO 인가.  초안 2 의 Q1–Q6 은 이 둘에 묶었다 (새 질문 없음).
- 사전 공격 ① 대조표 = `docs/reviews/codex_lhs214_relaunch_check_request_20261028_claimcheck.md` (줄 · 주장 · 출처 · 결과).  발송 전 남은 칸 = 리뷰 핀 40 자리 · 부록 B 재측정 (메인) · `L214P-02` 수정 시점 = ⬜ 1저자 (§0) · 사전 공격 ③ (§6).

## 0. 이번에 닫는 것 / 닫지 않는 것

**닫는 것 (확인 요청 · Codex 10-20 판정 `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` §5 의 다섯 단계)**

| # | 단계 | 상태 (10-28) | 자리 |
|---|---|---|---|
| ① | 등록 비준 — 194 §3 · §5 머리 · §9-8 · §9-9 / 보충 §3 · §5 머리 · §9-3 · §9-4 + S0b (`SUPR-03`) | ✅ 10-21 — 비준 커밋 `f82929b06` · 대화 원문 커밋 `7f99be67c` · S0b 커밋 `fe23f2b83` (셋 다 B7 의 조상) | §2-1 |
| ② | 지문 재결합 — 두 §3 활성 = 체크아웃 `code_fp` · 인계 도구 · 배포 빌더 = 194 §3 ✅ 줄 | ✅ 문서 + WSL 실측 (B7 두 영수증) | §2-2 |
| ③ | B7 승인 핀 | ✅ 10-28 = `35f0327377a4213774010a090df4d224e50d29e1` (1저자 *"lhs 권고대로"* = 실행표 §5 Q1) · 194 §3 원문 *"문서 · 원장만"* 엄격 미충족 = 한정 (1저자 Q2 (가)) | §2-3 |
| ④ | 새 ROOT 둘 WSL 사전 점검 | ✅ 10-28 17:32 KST (1저자 · WSL `~/dem-audit`) · 반입 · 결과 전 기대와 다른 칸 0 (단계 0 이름 확인 화면 = 기록 없음 · §6) · 194 손 대조 ✅ 1저자 · S1 증거 보완 E1 · E2 처리 | §2-4 – §2-6 |
| — | 실제 214 발사의 발사 확인 범위 GO | ⬜ 이 요청 | §3 · Q2 |

**닫지 않는 것**

| 무엇 | 상태 |
|---|---|
| ⑤ 1저자 발사 승인 · 실제 실행 · 결과 · 등록 §5 관문 | ⛔ 별도 — 이 요청의 GO 는 발사 확인 범위이지 승인이 아니다 (실행표 §4-4 6 행) |
| `L214P-01` (= `LHS214-PRE-01` · P7 · P10 두 줄) | 닫힘 — Codex S1 10-28 (원장 verified · 두 줄 한정) · 다시 묻지 않는다 |
| `L214P-02` (P3 · `launch_eligibility` 1140 행 LF) | open — 이번 발사 = 코드 무변경 (B7 그대로) · 운영 = 전체 40 자리 `--approved-sha` (§3) · 한 줄 수정 = 214 발사 뒤 (메인 권고 · ⬜ 1저자 확인 대기) |
| v1.3 배포 | HOLD — H0 model_limit 행 = 주 타깃 배포 HOLD (194 §9-8 ⑤) |
| S3 | 별도 HOLD — `scripts/network_conductivity.py` 바뀜 → 재봉인 의무 |
| `L214R-S03` · `L214R-S05` | open · 한정 유지 |
| σ₀ 1.5 솔버 상수 | 이번 재봉인 밖 |
| `SUPR-03` 원장 상태 이동 | 메인 (이 판정 뒤) |
| 두 등록 §9 의 10-28 사전 점검 항목 | 아직 없음 — 기록 = 반입 폴더 + 이 요청서 · 발사 뒤 §9 기록 = 194 §3 126 줄 |
| B7 뒤 본 가지의 다른 트랙 변경 | 범위 밖 — LHS 범위 바이트 = B7 (§1-3) |

## 1. 핀 · 보낼 것

| 역할 | 값 | 비고 |
|---|---|---|
| 가지 | `claude/stoic-knuth-NObVQ` | — |
| B7 승인 핀 (사전 점검 · 발사 체크아웃) | `35f0327377a4213774010a090df4d224e50d29e1` | 두 사전 점검 영수증 `git.sha` · `head.txt` · 모든 `--approved-sha` 값 |
| 리뷰 핀 | ⬜ 이 요청서를 담은 본 가지 커밋 — 메인이 push 뒤 발송 메시지 (ZIP 이면 PIN.txt) 에 40 자리 | 이 파일은 자기 커밋 SHA 를 담을 수 없다 · 이 판의 부모 커밋 = `003f715f8fa1ad6e954863153bd14391f2f3d7ca` |
| 대조 핀 (Codex 10-20 판정) | `34713ac9650ece7c8d59b7c4d9a2aefccee693ea` | — |
| S1 리뷰 핀 | `b7a979032160dc1d9514c612aa36ff0d6c28bf54` | ⚠ 승인 인자가 아니다 — 넣으면 P10 실패 (S1 판정문 §4 79 줄) |

### 1-2. 보낼 것

| # | 무엇 | 비고 |
|---|---|---|
| 1 | 이 요청서 · 대조표 | — |
| 2 | WSL 반입 폴더 `docs/reviews/lhs214_wsl_preflight_35f032737_1028/` (bundle 18 · MANIFEST · README · 단계 2 화면 원문) | 원 tgz `lhs_preflight_35f032737_1028_173239.tgz` (리포 밖 · 32,197 B · sha256 `9c05aef7…` — 전체 값 = 그 README) = S1 때 Codex 가 받은 tgz 와 같은 파일 (S1 ZIP `input/` 의 같은 tgz 의 멤버 18 = 반입 MANIFEST 18/18 · 부록 A-1) — 다시 보내지 않아도 된다 |
| 3 | 실행표 · 묶음 `docs/reviews/lhs214_relaunch_package_20261020.md` · 체크리스트 `docs/reviews/lhs214_wsl_receipt_checklist_20261024.md` | — |
| 4 | (이미 Codex 쪽) S1 정정본 `docs/reviews/codex_lhs214_pin_syntax_recheck_request_20261027_main.md` · S1 판정 반입 `docs/reviews/codex_lhs214_pin_syntax_review_20261028/codex_review_lhs214_pin_syntax_20261028.md` | 다시 묻지 않는다 |

### 1-3. 리뷰 핀 *"코드 = B7 바이트"* — 대조 집합 (실행표 §3-4 · 1저자 Q3)

본 가지에 다른 트랙 코드 커밋이 계속 들어오므로 트리 전체 같음이 아니라 아래 묶음의 `git diff --quiet` 로 본다.  지금 잰 구간 = B7 → 이 판의 부모 커밋 `003f715f8` (51 커밋 · 부록 A-3).

| 묶음 | rc | 비고 |
|---|---|---|
| LHS 핵심 40 (봉인 32 · 인계 2 · 배포 빌더 · 실행기 · 영수증 · 스모크 · 두 등록) | 0 | — |
| LHS 닫힘 78 (실행표 부록 A-C 방법) | 0 | — |
| 입력 자료 16 경로 (lhs · lhsx · lhss 수확 · 코호트 · union · 설계 · 어댑터 · 보충 묶음 · case15 · real14 · 인계표 · net194 기록) | 0 | 실행표 부록 A-G 의 자료 7 경로보다 넓게 (실행기 `COHORT_SPECS` · 영수증 도구 입력) |
| 게이트 · 등재 (A-G 의 `scripts/check_all.sh` · `docs/reviews/selftest_inventory.tsv`) | **1** | 다른 트랙 줄만 더함 (게이트 +25 줄 = 주석 + `run` 10 줄 — 믹서 D2 · D3 · ULPRI 다섯 · rint_first_result · kg50 둘 / 등재 +2 행 = kg50 · 지운 줄 0) · LHS 7 행 · fast 드라이버 줄 같음 |

→ 리뷰 핀이 정해지면 메인이 부록 B 로 B7 → 리뷰 핀을 다시 잰다 (위와 같은 rc 이어야).

## 2. 다섯 단계 — 근거

### 2-1. ① 비준 · S0b

| 항목 | 근거 | 결과 |
|---|---|---|
| 비준판 문안 | 비준 커밋 `f82929b06` = 묶음 §1-4 · §1-5 diff (날짜 자리만 채움) · 대화 원문 커밋 `7f99be67c` = 두 등록 각 1 줄 (`git diff f82929b06 B7 -- <두 등록>` = 그 두 줄 · 부록 A-4) | 두 §3 활성 `2149f873…c3eb` · 대기 선언 0 (실행표 부록 A-R) · Codex S1 Q3 = 32 지문 · 두 등록 활성 지문 독립 재계산 일치 |
| 결과 열람 뒤 정책 개정 표지 | 194 §5 머리 · §9-9 / 보충 §9-4 | 비준판 문안에 있다 (10-14 실행 결과를 본 뒤 개정) |
| S0b (`SUPR-03` · claimed_fixed `fe23f2b83`) | 영수증 도구 sha256 `3d6110be…` = fe23f2b83 판 = B7 판 | WSL selftest 123/123 (B7) · 고치기 전 · 변이 수 = 초안 2 §3 Q5 · 10-23 작업 세션 사전 검토 `docs/reviews/codex_review_lhs214_preflight_20261023.md` = 타당 (외부 GO 아님 — 그 문서 3 줄) |

### 2-2. ② 재결합 — B7 · WSL 실측

| 항목 | 등록 · 기대 | WSL (B7 · 10-28) | 판정 |
|---|---|---|---|
| 봉인 32 `code_fp` | 두 §3 활성 `2149f873…c3eb` | 두 영수증 · 두 로그 코드 줄 = 같은 값 · CODE_FILES 32 · dirty False | 같음 |
| 기대 망 세대 | `g2` · 문제 0 · 모드 hertz · physics · hertz_h12 | 두 로그 · 두 영수증 `generation` 같음 (오류 '') | 같음 |
| 닫힘 · 지연 import · fork | 30 ⊆ 32 · 92 · 분류 밖 0 · 0 줄 (194 §3 188 줄) | 두 로그 ✓ 셋 · 두 영수증 `checks` 셋 true | 같음 |
| 입력 지문 194 | 194 §2 다섯 값 | 로그 `INPUT_DIGEST_JSON` = 실행표 §4-3 기대 줄과 글자 같음 | 같음 (손 대조 §2-5) |
| 입력 지문 보충 20 | 보충 §2 | 로그 줄 = 기대 줄 글자 같음 · 영수증 도구 칸 E1 ✓ (기계 대조) | 같음 |
| 인계 도구 2 · 배포 빌더 | 194 §3 ✅ 줄 `d1815155…` · `0e2ec7ef…` · `3096e33f…` | 보충 영수증 `recorded.tool_sha256` 같은 값 | 같음 |
| 실행기 `scripts/run_network_194_parallel.py` | 등록 값 없음 (`runner.sha256` = 기록 전용) | `3220be53…` (두 영수증) | **초안 2 와 다름** — `f4048aca…` → `3220be53…` (`09bf1813c` · P7 · P10 두 줄 · `L214P-01`) |
| 영수증 도구 · 스모크 | 기록 | `3d6110be…` · `feb3e84b…` (B7 바이트 · 부록 A-4) | — |

### 2-3. ③ B7

| 조건 | 결과 | 근거 |
|---|---|---|
| 정의 — 비준 문안이 들어간 push 된 본 가지 커밋 · 1저자가 고른 한 SHA · 그 체크아웃 194 dry-run 이 같은 code_fp (194 §3 187 줄) | ✓ | 1저자 10-28 Q1 · 두 영수증 code_fp (§2-2) |
| 실행표 §3-1 B1–B14 | ✓ — B10 · B11 은 WSL 단계 2 · 0 이 직접 (§2-4) | 실행표 §3 |
| `L214P-01` 수정 포함 | ✓ — `09bf1813c` 가 조상 · 두 영수증 `git.sha` 원문 = 40 자리 (끝 LF 없음) | `receipt_fields.txt` · 부록 A-2 |
| 사전 점검 ↔ 승인 SHA | ✓ — verify `approved_sha` · 영수증 도구 `inputs.approved_sha` = PIN 40 · P10 ✓ 둘 | 두 JSON · 부록 A-2 |
| 두 발사 manifest ↔ 승인 SHA (10-20 판정 §5 ③) | 발사 뒤 — 끝 블록 384 줄 (F7 · G7 · H1) | §3 |
| B15 — 194 §3 원문 125–126 줄 *"이 문서를 담은 커밋 또는 그 뒤 **문서 · 원장만** 바뀐 커밋"* | **엄격히 ✗** — 마지막 등록 커밋 `7f99be67c` → B7 = .py 37 파일 (scripts 35 · webapp 2) · 봉인 32 = 0 · 그중 LHS 실행기 = `09bf1813c` 두 줄 | 이유 = `L214P-01` 수정이 등록 마지막 커밋 뒤에 들어왔다 (수정을 담은 어느 후보도 같다) · 1저자 Q2 (가) = ✅ 줄 (187 줄) 기준으로 읽는다 · LHS 핵심 40 = S1 리뷰 핀 `b7a979032` 바이트 (rc 0 · 부록 A-4 · S1 판정문 §1 = 리뷰 핀 39 소스 blob = WSL 핀 · 두 등록 별도 동일) |

### 2-4. ④ WSL 사전 점검 — 단계 0–6 (결과 전 기대 = 실행표 §4-3)

파일 = `docs/reviews/lhs214_wsl_preflight_35f032737_1028/bundle/` (18 · `MANIFEST.sha256` 18/18 OK · 부록 A-1).

| 단계 | 결과 전 기대 | WSL 실측 (10-28 · 1저자) | 파일 |
|---|---|---|---|
| 0 | 핀 일치 · dirty 0 · 이미 있는 이름 없음 · 10-14 ROOT 둘 그대로 | `head.txt` = PIN · `step0.txt` = 17:32:39 KST · PIN · PY `/home/yonghoon71/Yonghoon-DEM-DFT/.venv/bin/python3` · 새 경로 넷 (R194 · RS · PF194 · PFS) + LOGD · `ls -d` 가 10-14 ROOT 둘을 찍음 | `step0.txt` · `head.txt` (핀 일치 · dirty 0 = 반입 README 의 1저자 화면 요약 · 이름 확인 화면 줄 = 기록 없음 — §6) |
| 1 | 보통 = 격리 | 둘 다 Python 3.12.3 · NumPy 2.5.2 · SciPy 1.18.1 · networkx 3.7 · 같은 실행 파일 (10-14 WSL 과 같은 판 · 194 §9-7) | `env.txt` |
| 2 | 다섯 rc 0 · 시험 뒤 dirty 0 | fast16 16/16 · real4 4/4 · reread 전부 통과 (검사 줄 ✓ 29 · ✗ 0) · 실행기 139/139 · 영수증 123/123 · `rc=0` 다섯 · 시험 뒤 dirty 0 | 로그 다섯 · 화면 원문 `docs/reviews/lhs214_wsl_preflight_35f032737_1028/step2_screen_paste_1028_1736.txt` (tgz 밖) |
| 3 | dry-run 0 · 코드 줄 · g2 · 30 ⊆ 32 · 92 · fork 0 · 입력 줄 · 원자료 0 · ⛔ 없음 / verify 0 · 11 칸 다름 0 | 영수증 `exit_code` 0 · `completed` true · 마지막 줄 `PREFLIGHT_DRY_RUN_COMPLETE rc 0` · 로그 ⛔ 0 줄 · 기대 줄 전부 / verify `rc` 0 · P0–P10 11/11 · 승인 = PIN 40 | net194 영수증 JSON · 로그 · verify JSON |
| 4 | dry-run 0 · 영수증 도구 0 · 24 칸 다름 0 | 영수증 `exit_code` 0 · 영수증 도구 `rc` 0 · 24/24 (R0 · A1–A2 · B1–B3 · C1–C4 · D1 · P0–P10 · E1 · E2) · 승인 = PIN 40 · manifest 입력 null (사전 점검 범위) | netsupp20 영수증 JSON · 로그 · 영수증 도구 JSON |
| 5 | 194 두 줄 = 등록 · 두 영수증 `'35f0…'` 40 False `3220be53…` `2149f873…` 32 | 같음 (두 줄 · 두 영수증 다) · `receipts_sha256.txt` 네 값 (영수증 둘 · 로그 둘) = 반입 MANIFEST 값 · 두 로그 sha256 · 바이트 = 영수증 `log.sha256` · `bytes` (194 4,628 B · 보충 4,390 B) | `handcheck_194_lines.txt` · `receipt_fields.txt` · `receipts_sha256.txt` |
| 6 | tgz 하나 · sha256 한 줄 | 32,197 B · sha256 `9c05aef7…` (반입 README) · `dirty.txt` 0 B | 반입 README |

### 2-5. 194 손 대조 표 (채운 판 · 묶음 §5 표 = 체크리스트 §3)

- 영수증 = WSL `/home/yonghoon71/net194_35f032737_1028_preflight_1028_173239.json` (반입본 sha256 `5834fbc573a53eb0fadd49f3bdbc1d3326bb8f90ad3ce1bd546457784f02226e`) · 전체 로그 sha256 `6aa80dc1e75673482c13f69ab52e9f8ea1e8c6318af19e7638f4b9de34d133eb` (4,628 B = 영수증 `log.sha256` · `bytes`) · 승인 핀 = B7 · 이 영수증 = verify P0–P10 11/11 을 통과한 바로 그 실행.
- 확인: WSL 작업 = 1저자 (10-28 17:32:39 KST · `step0.txt`) · **손 대조 확인자 = 1저자 ✅ 10-28 밤 *"ㅇㅇ 권고대로 해"*** (시각 미기록 · 실행표 V10) · 독립 대조 = Codex S1 판정문 §4 (10-28 · 여섯 칸 일치 · WSL 작업자 신원을 대신하지 않음).

| 칸 | 등록 값 (전체 · 194 §2 · §3) | 로그 실측 (전체 · `handcheck_194_lines.txt`) | 일치 |
|---|---|---|---|
| n · missing_raw_sha | 194 · [] | 194 · [] | ✓ |
| ids_sha256 | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | ✓ |
| raw_sha256_table_sha256 | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` | ✓ |
| cohort_tsv_sha256.lhs | `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` | `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` | ✓ |
| cohort_tsv_sha256.lhsx | `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` | `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` | ✓ |
| code_fp · CODE_FILES 수 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · 32 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · 32 | ✓ |

### 2-6. S1 판정문 §5 증거 보완 E1 · E2 (⚠ 영수증 도구 칸 E1 · E2 = 입력 지문 · code_fp 기계 대조와 다른 이름)

| 항목 | S1 판정 | 처리 |
|---|---|---|
| 증거 보완 E1 — 자체시험 다섯의 실제 셸 종료코드 | 18 파일에 따로 없음 · 화면 기록을 회수하면 재실행 불요 | 1저자 단계 2 화면 (대화 붙여 넣기 → `docs/reviews/lhs214_wsl_preflight_35f032737_1028/step2_screen_paste_1028_1736.txt` · 리포 첫 기록 = 커밋 `003f715f8`) = `fast16 rc=0` · `real4 rc=0` · `reread rc=0` · `runner rc=0` · `receipt rc=0` · 시험 뒤 dirty 0 · ⚠ tgz 밖 (MANIFEST 18 에 없음) |
| 증거 보완 E2 — 수령표의 신원 · 확인 기록 연결 | 독립 대조와 WSL 작업 기록을 각자 출처로 | 체크리스트 머리 10-28 줄 (반입 폴더 · 화면 원문 · S1 §4 연결 · "미수령" = 10-24 시점) · 실행표 끝 절 · 손 대조 확인자 = 1저자 (§2-5) · 단계 3 · 4 종료코드 = 영수증 `exit_code` 0 · verify · 영수증 도구 JSON `rc` 0 (S1 §5 = 그 기록은 누락 아님) |

## 3. 발사 블록 · `L214P-02` 운영 (Q2 확인 거리)

- 끝 블록 = 묶음 §4 376–385 줄 (⑤ 승인 뒤에만 · 같은 핀): 380 줄 194 `run --root "$R194" --observe-imports` → 382 줄 194 등록 §4 완료 뒤 확인 (audit · 재시도 예외) → 383 줄 보충 20 `run --root "$RS" --cohorts lhss --observe-imports` → 384 줄 발사 영수증 `--manifest "$RS/manifest.json" --primary-manifest "$R194/manifest.json" --approved-sha "$PIN"`.
- `--approved-sha` 를 받는 명령 = 사전 점검 둘 (실행표 §4-2 167 · 172 줄 · 실행됨 · 둘 다 PIN 40) + 발사 뒤 384 줄 하나.  `run` 은 받지 않는다 (묶음 §3 293 줄).
- 끝 블록의 `$PIN` = 단계 0 의 40 자리 (실행표 §4-2 138 줄) · 같은 단계 140 줄 `[ "$(git rev-parse HEAD)" = "$PIN" ]` 은 40 자리 HEAD 와 다르면 `⛔ 핀 다름` 을 찍는다 ⇒ 384 줄은 전체 40 자리 승인값을 준다 (생략 · 7 자리 아님).
- `L214P-02` 와의 관계 (S1 판정문 §3 Q5 표 65–71 줄): `launch_eligibility` 1140 행 (발사 영수증의 F1 · G1) 은 SHA+LF 를 받지만, 전체 40 자리 승인값이면 F7 · G7 (`scripts/supp20_input_receipt.py` 357–361 줄 · 원문 `re.fullmatch(r'[0-9a-f]{40}', …)` + 승인값 접두) 이 거부한다 · 승인값을 빼면 rc 0 (7 자리면 마지막 한 자리만 다른 같은 오값 둘이 rc 0) — 끝 블록은 빼지도 줄이지도 않는다.  이번 발사 = 코드 무변경 (B7 그대로) · 한 줄 수정 = 214 발사 뒤 (메인 권고 · ⬜ 1저자 확인 대기).
- 다른 셸이면 (379 줄) 변수 줄을 다시 쓰되 ROOT · 영수증 이름은 사전 점검 그대로 = `step0.txt` 값 — R194 `/home/yonghoon71/net194_35f032737_1028` · RS `/home/yonghoon71/netsupp20_35f032737_1028` (dry-run 은 ROOT 를 만들지 않는다 — 실행표 §4-2 144 줄 주석).  S1 판정문 §5 (124 줄) *"외부 발사 범위 확인, 실제 승인 PIN과 실행 직전 환경·ROOT 점검은 기존 절차대로 남는다"* = 단계 0 의 체크아웃 · 핀 일치 · dirty 줄 (실행표 §4-2 139–141 줄).
- 구 ROOT (10-14 `~/net194_1087a9b2f` · `~/netsupp20_1087a9b2f` · 그 영수증) = 지우지 · 옮기지 · retry · merge 하지 않는다 · 실패 기록을 사후 성공으로 덮지 않는다 (묶음 §5 표 · 10-20 판정 §5 ⑤ · 10-28 단계 0 `ls -d` = 그 ROOT 둘 있음).

## 4. 질문

- **Q1. 다섯 단계 ①–④ 가 끝났는가 (§2).**  확인 거리 (초안 2 Q1–Q5 를 묶음):
  ① 비준판 문안이 10-20 판정 §5 ① (대기 선언을 승인 지문으로 자동 취급 안 함 · 역사 보존 · 결과 열람 뒤 변경 이력) 을 채우는가 · S0b 새 기대 (상태가 정한 지문 = 체크아웃 `code_fp` 64 자리 · S11g 일곱 꼴) 가 시험 약화가 아닌가 (수 · 변이 = 초안 2 §3 Q5).
  ② 재결합 (§2-2) — 지문 (봉인 32 · 세대 · 입력 · 인계 2 · 빌더) 은 초안 2 와 같고, 다른 것 = 실행기 기록 해시 (`L214P-01` 두 줄).
  ③ B7 = `35f032737` — B15 엄격 문구 미충족을 ✅ 줄 기준으로 읽는 판단 (1저자 Q2 (가) · §2-3) 이 맞는가.
  ④ WSL 기록 (§2-4 – §2-6) 이 사전 점검 · 194 손 대조 · S1 증거 보완 E1 · E2 를 채우는가.
- **Q2. 실제 214 발사 (194 → 보충 20 · 같은 핀 B7 · §3 끝 블록 그대로) 가 발사 확인 범위에서 GO 인가.**  HOLD 면 남은 조건만 · 새 결함이 있으면 등급 · 반례 (`L214P-02` 운영 = §3 포함).

## 5. 시험 수 — 출처 구분 (같은 수로 섞지 않는다)

| 시험 | WSL · B7 (10-28 · 3.12.3 · 2.5.2 · 1.18.1 · 3.7) | 그 밖 기록 (한정) |
|---|---|---|
| `scripts/wsl_network_smoke.py --selftest` (fast16) | 16/16 · rc 0 | 10-14 WSL 16/16 (핀 `1087a9b2f` · 194 §9-7) |
| `scripts/wsl_network_smoke.py --selftest-real` (real4) | 4/4 · rc 0 | 10-14 WSL 4/4 |
| `scripts/g2_network_reread.py --selftest` | 전부 통과 · 검사 줄 ✓ 29 · ✗ 0 · rc 0 | 컨테이너 10-21 ✓ 29 (초안 2 §4) |
| `scripts/run_network_194_parallel.py --selftest` | 139/139 · rc 0 — 실행기 `3220be53…` 판의 첫 WSL 실측 | 10-14 WSL · 컨테이너 10-21 = 139/139 (둘 다 `f4048aca…` 판) |
| `scripts/supp20_input_receipt.py --selftest` | 123/123 · rc 0 | 컨테이너 10-21 123/123 · Codex S1 Windows (3.12.14 · 2.5.3 · 1.16.3 · 3.7) 123/123 · 10-14 WSL 88/88 (옛 판) |
| 시험 뒤 dirty | 0 | — |
| 194 사전 점검 | dry-run `exit_code` 0 · verify rc 0 · P0–P10 11/11 | Codex S1 독립 11/11 |
| 보충 20 사전 점검 | dry-run `exit_code` 0 · 영수증 도구 rc 0 · 24/24 | Codex S1 독립 24/24 |

## 6. 하지 않은 것 · 한정

- 이 판의 측정 = 이 컨테이너 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1) 의 `git` · `sha256sum` · JSON 읽기 (부록 A) — 자체 시험 · 게이트 · 실행기 검증 함수 (`preflight-verify` · 영수증 도구) 를 다시 돌리지 않았다.  체크리스트 §4 *"같은 코드/핀의 영수증 검증 재현"* = Codex S1 판정문 §4 독립 재검증 (11/11 · 24/24) 이 있다 — 메인 별도 재현 없음.
- WSL 원 dump 를 다시 읽지 않았다 (S1 §4 도 같음) — P8 *"원자료 · 메시 문제 0 건"* 은 WSL 실행의 기록이다.
- 두 로그의 ⚠ 줄 *"Codex 세대 2 재검증 2 (10-07) = HOLD …"* = 실행기 고정 문구 (`scripts/run_network_194_parallel.py` 1877 줄) — 지금 상태가 아니다.
- 단계 0 의 이름 확인 · 단계 3 · 4 의 셸 `rc=` 화면 원문은 리포에 없다 — 반입 README 의 1저자 화면 요약 · 영수증 JSON `exit_code` 0 · verify · 영수증 도구 JSON `rc` 0 으로 본다.  단계 2 화면 원문은 tgz 밖이다.
- 사전 공격 리뷰 (CLAUDE.md): ① = 대조표 · ② = 해당 없음 (코드 무변경 · B7 그대로) · ③ 독립 에이전트 반례 = 이 판에서 하지 않음 · ④ = §0.
- 리뷰 핀 쪽 대조 (§1-3) 는 B7 → 이 판의 부모로 쟀다 — 리뷰 핀에서 다시 (부록 B · 메인).

## 7. 초안 2 → 새 판 (실행표 §2-2 여섯 줄)

| §2-2 자리 (초안 2) | 새 판 자리 |
|---|---|
| §0 ③ (11 줄 · B7 후보 · *"문서만"*) | §0 ③ · §2-3 (B7 = Q1 · B15 · Q2 (가)) |
| §1 (31 줄 · B7 ⬜ · 리뷰 핀 ⬜ · *"코드 = 승인 핀과 바이트 같음 · 문서만 다름"*) | §1 · §1-3 (Q3 대조 집합 · 다른 트랙 커밋) |
| §2 표 (40 줄 · 실행기 rc 0) | §2-2 (실행기 다름 · 두 줄) |
| §0 · §3 (`LHS214-PRE-01` · 10-23 검토 · 10-24 수정 없음) | §0 (`L214P-01` 닫힘) · §2-1 (10-23 검토) · §2-6 · §3 (S1 판정) |
| §4 회귀 (10-21 컨테이너 수) | §5 (WSL 수 + 그 밖 기록은 한정) |
| Q4 (*"⬜ 반입 뒤"*) | §2-4 – §2-6 (반입 폴더 · tgz sha256 · 손 대조 표 채운 판 · `step0.txt`) · §4 Q1 ④ |

## 부록 A. 가벼운 대조 — 명령 · 출력 (이 컨테이너 · 10-28 · 작업 트리 = 부모 `003f715f8` + 이 판)

### A-1. 반입 묶음 무결성

```bash
cd docs/reviews/lhs214_wsl_preflight_35f032737_1028/bundle && sha256sum -c ../MANIFEST.sha256 | grep -c ': OK'      # 18
sha256sum docs/reviews/codex_lhs214_pin_syntax_review_20261028/received_codex_lhs214_pin_syntax_review_20261028.zip   # 리포 루트에서
# S1 ZIP 의 input/lhs_preflight_35f032737_1028_173239.tgz 를 메모리에서 열어 멤버 sha256 ↔ 반입 MANIFEST (python3 -I · zipfile · tarfile · 풀지 않음)
```

```text
18
6b2e09c995834cb36a2b3c79bd431eab7cfbb03d12ccfb061d646d6eab35e46c  (4,454,350 B = README_import 값)
input tgz sha256 9c05aef7591ad10af70af52c01508b494ddc71855322b0ce367f42f67a5be0b8 · 32,197 B · tar 멤버 19 (파일 18 · 폴더 1) · 반입 MANIFEST 와 18/18 같음
```

### A-2. 두 영수증 · verify · 영수증 도구 JSON (python3 -I · 읽기만)

```text
net194   git.sha '35f0327377a4213774010a090df4d224e50d29e1' len 40 fullmatch40 True == PIN True dirty False
         log.sha256 == sha256(로그) True · 4628 B · code_fp 2149f873…c3eb · 32 · runner 3220be53…66ac8
         completed True · dry_run True · exit_code 0 · observe_imports True · 로그 INPUT_DIGEST 1 줄 = 실행표 기대 줄 · 끝 줄 'PREFLIGHT_DRY_RUN_COMPLETE rc 0'
netsupp20 (같은 검사 전부 True · 로그 4390 B · INPUT_DIGEST 줄 = 실행표 기대 둘째 줄)
verify rc 0 · approved 35f0327377a4213774010a090df4d224e50d29e1 · 11 칸 전부 ok (P0–P10)
영수증 도구 rc 0 · approved 같음 · 24 칸 전부 ok · manifest · primary_manifest 입력 None · 등록 code_fp 2149f873…c3eb · 대기 None
로그 ⛔ 줄 수: net194 0 · netsupp20 0
```

### A-3. B7 → 부모 `003f715f8` (Q3 대조 집합)

```bash
B7=35f0327377a4213774010a090df4d224e50d29e1; H=003f715f8fa1ad6e954863153bd14391f2f3d7ca
git rev-list --count "$B7..$H"                                   # 51
# CORE · CL · IN = 부록 B 의 세 변수
git diff --quiet "$B7" "$H" -- $CORE; git diff --quiet "$B7" "$H" -- $CL; git diff --quiet "$B7" "$H" -- $IN
git diff --stat "$B7" "$H" -- scripts/check_all.sh docs/reviews/selftest_inventory.tsv
git diff --name-only "$B7" "$H" -- 'scripts/*.py' 'webapp/*.py' | wc -l
```

```text
51
LHS 핵심 40 rc=0 · 닫힘 78 rc=0 (변경 0) · 입력 자료 16 경로 rc=0
scripts/check_all.sh | 25 +++ · docs/reviews/selftest_inventory.tsv | 2 ++ (더함만) · LHS 7 행 sha256 같음 · `--run-fast` 줄 1 = 1
.py 11 (scripts 10 = kg50 둘 · rint 둘 · 시험 여섯 / webapp 1 = 시험) — 닫힘 78 밖
```

### A-4. B15 · 핀 사이 바이트 (git 만)

```text
7f99be67c..B7 : .py 37 (scripts 35 · webapp 2) · 봉인 32 = 0 · 실행기 = 09bf1813c 하나 (2 insertions · 2 deletions = 2049 · 2082 줄 .match → .fullmatch)
f82929b06..B7 : 두 등록 각 1 줄 (7f99be67c) · LHS 핵심 40 은 그 둘 + 실행기만 다름
b7a979032..B7 : LHS 핵심 40 rc 0 · 09bf1813c..B7 : rc 0 · 34713ac96..B7 봉인 32 rc 0
B7 sha256 : 실행기 3220be53…66ac8 · 영수증 도구 3d6110be…f950 · 스모크 feb3e84b…1b11 · 인계 d1815155…e1f0 · 0e2ec7ef…5cd8 · 빌더 3096e33f…1383 (= 이 판의 부모 바이트)
B7 1140 줄 `_HEX40.match(g['sha'])` (그대로) · 2049 · 2082 줄 `_HEX40.fullmatch(gsha)` · 1877 줄 = 고정 ⚠ 문구 · 영수증 도구 357–361 줄 = F7 · G7 fullmatch 40
```

## 부록 B. 리뷰 핀 대조 명령 (메인 · Q3 · 리뷰 핀이 정해진 뒤)

```bash
B7=35f0327377a4213774010a090df4d224e50d29e1; REV=<리뷰 핀 40 자리>
CORE=$(python3 -I -c "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(' '.join(list(N.CODE_FILES) + list(N.HANDOVER_FILES) + ['scripts/lhs_release_build.py', 'scripts/run_network_194_parallel.py', 'scripts/supp20_input_receipt.py', 'scripts/wsl_network_smoke.py', 'docs/reviews/lhs_network_batch_registration_20261007_g2.md', 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md']))")
CL=<실행표 부록 A-C 의 닫힘 78 출력>        # 같은 AST 걷기 (시작 = 도구 6 + 봉인 32)
IN="docs/data/lhs_descriptors_cov_1e09f661d docs/data/area_s2_cohort.tsv docs/data/lhs_union_20260927 docs/data/lhsx_descriptors_cov_1e09f661d docs/data/lhsx_descriptors_20260925 docs/data/lhsx_design_adapted_20260929.csv docs/data/lhss_descriptors_cov_1e09f661d docs/data/lhss_union_1e09f661d docs/data/lhss_design_adapted_20261012.csv docs/data/lhs_supp_runs_20261006 docs/data/lhs_supp_design_20261006.csv docs/data/case15_corner_20261001 docs/data/lhs_handover_20261001.csv docs/data/lhsx_handover_20261001.csv docs/data/real14_reference_20260928 docs/data/lhs_network194_11fcf91e8"
for S in CORE CL IN; do git diff --quiet "$B7" "$REV" -- ${!S}; echo "$S rc=$?"; done      # 셋 다 0 이어야
```
