# LHS214 사전 점검 SHA 형식 수정 재확인 요청 — 본 가지 SHA 정정본 (2026-10-27 · 원본 = Codex 작업 세션 10-24 작성 · 원본은 고치지 않음 · ⬜ 발송 = 1저자)

- 원본: `docs/reviews/codex_lhs214_pin_syntax_recheck_request_20261024.md` — 8 줄 *"기준 리뷰 핀은 … 최종 리뷰 핀·전체 gate 영수증은 canonical 반입과 검증을 마친 root가 지정한다"*.  10-27 본 가지 `cherry-pick -x` (대응표 `docs/collab/claude_to_codex/20261027-0220_nonrint-merge-sha-map.md` #26–#29) 뒤 그 자리를 채운 판이다.
- 이 정정본이 원본과 다른 것 = ① 맨 위 닫는 것 / 닫지 않는 것 ② 핀을 본 가지 커밋으로 (§1) ③ 메인이 이 컨테이너에서 다시 잰 대조 (§2) ④ 덧붙인 질문 5 하나.  원본의 *"수정과 경계"* · *"실제 검증"* 절은 원본에서 그대로 읽는다 (여기 옮겨 적지 않음) · 질문 1–4 = 원문 그대로 (§3).
- 함께 읽을 것: 실행표 `docs/reviews/lhs214_relaunch_exec_sheet_20261027.md` (B7 · WSL · 발사 확인은 그쪽).

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (확인 요청) | 자리 |
|---|---|
| `LHS214-PRE-01` (P3 · 10-23 사전 검토의 임시 ID · 공유 원장 미등재) — 사전 점검 영수증 `git.sha` = 승인된 40 자리 + LF 를 P7 · P10 이 받던 형식 결함의 수정 (`_HEX40.match(gsha)` → `.fullmatch(gsha)` 두 곳) | `scripts/run_network_194_parallel.py` 2049 · 2082 줄 · 본 가지 수정 커밋 `09bf1813c1b5a188c0caf056ad490ea0f86da8fb` |
| 원본의 Codex 가지 핀 → 본 가지 핀 · 리뷰 핀 지정 (원본 8 줄의 "root 가 지정" 자리) | §1 |

| 닫지 않는 것 | 상태 |
|---|---|
| B7 승인 핀 · 새 ROOT 둘 WSL 사전 점검 · 194 손 대조 · 발사 범위 확인 | 발사 확인 요청서 `docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` — WSL 묶음 반입 뒤 새 판 |
| `launch_eligibility` 의 `_HEX40.match(g['sha'])` (manifest `git.sha` 꼴 · 1140 줄) | 원 수정 범위 밖 그대로 (원본 "수정과 경계" — 다른 호출자 `launch_eligibility` 는 바꾸지 않았다) · 발사 manifest 를 승인 SHA 와 대조하는 F7 · G7 은 `re.fullmatch(r'[0-9a-f]{40}', …)` (`scripts/supp20_input_receipt.py` 357–361 줄) |
| P10 의 승인 SHA 정규화 `str(approved_sha).strip().lower()` (2079 줄) | 기존 7–40 자리 규약 그대로 (원본 "승인 SHA의 기존 7–40자리 규약 … 바꾸지 않았다") — 영수증 쪽 `git.sha` 는 정규화 없이 전체 문자열 검사 |
| 원장 등재 (`LHS214-PRE-01`) · `SUPR-03` verified · S3 · v1.3 · `L214R-S03` · `L214R-S05` | 메인 · 1저자 몫 · 한정 그대로 |

## 1. 핀 — 원 Codex 가지 → 본 가지 `claude/stoic-knuth-NObVQ`

| 역할 | 원 커밋 (`codex/lhs214-relaunch` · 본 가지 머리의 조상 아님 · 원격 추적 ref 에서 닿음) | 본 가지 커밋 (머리 `35f0327377a4213774010a090df4d224e50d29e1` 의 조상) | 대조 (이 컨테이너 · §2 A-1) |
|---|---|---|---|
| 독립 사전 검토 (10-23) | `e41d091f5ac948b3529eaed3aae03eb380dad9e0` | `481b964d04a644e1e74cff9bf3b2c9f89ecb8c38` | LHS 핵심 40 · LHS214 증거 rc 0 · `-x` 꼬리 = 원 커밋 |
| 기준 리뷰 핀 (원본 8 줄) | `ffbd438e7522d58eb069561fe58020f4086707ac` | `1baa0d9b7a9d5b2c6b101b5d203eacb1e18fd6ca` | 같음 |
| 수정 | `ed6ed401f904d9f818cbdced42d111a7b1efb8d2` | `09bf1813c1b5a188c0caf056ad490ea0f86da8fb` | 같음 |
| 수정 전체 게이트 기록 (원 최종) | `854857e576a2a8aba07ec861dbee39d4bb59efae` | `b7a979032160dc1d9514c612aa36ff0d6c28bf54` | 같음 |

- **리뷰 핀 (제안 · ⬜ 1저자 확인) = 커밋 `b7a979032160dc1d9514c612aa36ff0d6c28bf54`** (= 원 최종 `854857e57` 의 본 가지 반입).  본 가지 머리 `35f032737` 도 같은 범위 바이트 같음 (§2 A-1).
  ⚠ 이 리뷰 핀은 B7 승인 핀이 아니다 (체크리스트 `docs/reviews/lhs214_wsl_receipt_checklist_20261024.md` 20 줄 · Codex 마감 답장 `docs/collab/codex_to_claude/20261027-0451_nonrint-close-reply.md` 19 줄) — B7 = 실행표 §3 · 1저자 Q1.
- 함께 보낼 것: 원본 요청서 · 이 정정본 · ZIP `codex-lhs214-relaunch-854857e576a2.zip` (sha256 `d83c3d27…` — 전체 값 = `docs/reviews/nonrint_handoff_20261026.md` 73 줄).  ZIP 은 원 가지 판이다 (본 가지 리뷰 핀과 §2 A-1 범위 바이트 같음 · 그 밖 파일은 다를 수 있다).

## 2. 메인 대조 (이 컨테이너 · 10-27 · 저장소 명령 · 해시만 — 자체 시험 · 게이트는 다시 돌리지 않았다)

| # | 무엇 | 결과 | 근거 (명령 · 파일) |
|---|---|---|---|
| A-1 | 원 커밋 ↔ 본 가지 커밋 넷 · 원 최종 ↔ 본 가지 머리 · 본 가지 반입 최종 ↔ 머리 (6 쌍): LHS 핵심 40 (봉인 `CODE_FILES` 32 · 인계 2 · 배포 빌더 · 실행기 · 영수증 · 스모크 · 두 등록 문서) · LHS214 증거 (10-23 검토문 · 증거 폴더 · 10-24 요청서 · 증거 폴더 · 체크리스트) | 6 쌍 전부 `git diff --quiet` rc 0 · rc 0 | 실행표 부록 A-M |
| A-2 | 본 가지 커밋 넷의 `cherry picked from commit` 꼬리 | 4/4 = 위 표의 원 커밋 | `git log -1 --format=%B <커밋>` |
| A-3 | 실행기 sha256 (`git show <커밋>:scripts/run_network_194_parallel.py \| sha256sum`) | 수정 전 `f4048aca…` (34713ac96 · f82929b06 · ffbd438e7 · 1baa0d9b7) → 수정 뒤 `3220be53…` (ed6ed401f · 09bf1813c · 854857e57 · b7a979032 · 머리 35f032737) | 실행표 부록 A-M |
| A-4 | 수정 범위 | `git diff 34713ac96 HEAD -- scripts/run_network_194_parallel.py` = 2 줄 바뀜 (2049 · 2082 — `.match` → `.fullmatch`) · `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/runner.diff` 와 같은 두 줄 | 실행표 부록 A-D |
| A-5 | 봉인 32 · 활성 지문 | 34713ac96 → 머리 봉인 32 rc 0 · 머리 `code_fp(code_hashes())` = 두 등록 §3 활성 = `2149f873…c3eb` · 대기 선언 0 | 실행표 부록 A-R |
| A-6 | 영수증 도구 | 머리 sha256 `3d6110be…` = S0b 수정 `fe23f2b83` 판 (fe23f2b83 → 머리 rc 0) | 실행표 부록 A-D |
| A-7 | 원 기록 — 여섯 경계 | 수정 전 `failed_boundaries` = `trailing_LF` · `test_rc` 1 / 수정 뒤 [] · 0 · `boundary_cases` 6 | `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/red/summary.json` · `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/green/summary.json` |
| A-8 | 원 기록 — 영수증 selftest | 수정 전 · 뒤 둘 다 `123/123 PASS` | 같은 두 파일 · `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/green/receipt_selftest.log` 126 줄 |
| A-9 | 원 기록 — 독립 코드 검토 (10-24) | 20 꼴 × 승인 SHA 셋 (전체 · 7 자리 · 없음) = 60 기대 일치 · 막는 결함 없음 | `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/independent/review.md` |
| A-10 | 원 기록 — 전체 게이트 (원 가지) | 후보 `ed6ed401f…` · 155 PASS / 0 FAIL · rc 0 | `docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/full_gate_receipt.json` (`pass_lane_count` · `fail_lane_count` · `exit_code`) |
| A-11 | 본 가지 통합 게이트 (10-27) | 검사 tree = 커밋 `8a2c92da9` 의 tree · ✓ 157 줄 · ✗ 0 줄 · 159 줄 `✓ fast 자기검사 전수` · 161 줄 `✓ 전부 통과` — fast 등재에 실행기 · 영수증 · 스모크 (fast16) selftest 가 들어 있다 (그 tree 의 `scripts/check_all.sh` 425 줄 · 머리 428 줄 · `scripts/check_selftest_inventory.py` 514 줄) · 그 tree 와 머리의 LHS 닫힘 78 모듈 rc 0 | `docs/reviews/nonrint_integration_20261027/gate_8a2c92da9.log` · 실행표 부록 A-C |

## 3. 확인 요청 — 원본 1–4 (원문 그대로) + 메인 덧붙임 5

1. P7/P10 두 호출의 전체 문자열 검사가 LF 반례를 막고 정상 핀·다른 hex 거부·승인 SHA 기존 동작을 유지하는가.
2. 새 경계 시험이 실제 생산 검사기를 사용하며, 기존 정상 preflight·합성 launch 회귀와 S0b를 약화시키지 않는가.
3. 수정이 봉인 32·등록 지문·다른 SHA 사용처·물리 값에 닿지 않는가.
4. [WSL 실제 입력·영수증 체크리스트](lhs214_wsl_receipt_checklist_20261024.md)가 기존 패키지를 중복하거나 합성 증거를 실제 측정으로 승격하지 않는가.
5. (메인 덧붙임) §0 *닫지 않는 것* 의 둘 — `launch_eligibility` 1140 줄의 `.match` 와 P10 의 승인 SHA 정규화 — 을 이 수정 범위 밖에 두는 판단이 맞는가.  막아야 하면 등급 · 반례 (B7 · WSL 사전 점검 전에 알면 사전 점검을 다시 하지 않는다).

## 4. 한정

- 이 정정본의 대조는 해시 · git 대조 (§2 A-1 – A-6 · A-11 의 닫힘) 와 원 기록 인용 (A-7 – A-10) 이다.  메인이 이 컨테이너에서 자체 시험 · 게이트를 다시 돌리지 않았다.
- 컨테이너 = Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1 — WSL 실측 아님 · B7 아님 · 발사 GO 아님.
- 사전 공격 리뷰 (CLAUDE.md 규칙): ① 이 정정본의 숫자 · 전칭 = §2 명령 출력 · ② · ③ = 10-24 독립 코드 검토 (A-9 · 같은 실행기 바이트 `3220be53…`) 를 이어 쓴다 (새로 돌리지 않음) · ④ = §0.
