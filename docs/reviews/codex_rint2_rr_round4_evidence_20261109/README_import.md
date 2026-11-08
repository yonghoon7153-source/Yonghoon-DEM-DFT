# Codex Rint ② 재검토 회차 ④ (11-09) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rr_round4_20261109.md` — ZIP 원본 16,854 B · sha256 ae24483635ead3574001413df9599930e385a4fb88ca4de0710ac4ae98163da2 · CR 0 개 → 리포 사본 = 원본과 바이트 같음 (외부 절대 경로 · IP · 포트 · 사용자@호스트 0 → 가린 사본 아님 · 주소 검사에 걸린 11 곳 = `파일:줄` 표기 오탐 · 리포 `.gitattributes` 의 md = LF 규칙에도 바뀌지 않는다).
- 리뷰 핀 = `1f9f3607eb2f0118d322eeff780bba6eb17b85a2` (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · tree cc6aefe7a9013885c8da0d700cff1cc981033f77 = 묶음 안 원격 응답 (뺀 파일 remote_provenance.json) 의 commit tree = 우리 git 의 핀 tree) · 비교 기준 = `17d45fb9c` (회차 ③ 리뷰 핀) · 요청서 = `docs/reviews/codex_rint2_rr_round4_request_20261109.md` (Q1–Q5) · 핀 → 이 반입 바탕 `e814b73c3` 사이 5 커밋 (비 Rint 반입) · `scripts/` 변경 없음 (`git diff --stat` 빈 출력) → 판정문 줄 번호 = 바탕에서도 그대로.
- 우리가 보낸 ZIP = codex_rint2_rr_round4_1f9f3607eb2f.zip · 3,992,042 B · sha256 ab3d7da16df298be7378ea62251d06983e319860f8688f14e498256882d23b3f — 받은 묶음의 input/ 사본으로 다시 잼 (판정문 §1 기록값과 같음) · 리포 기록에는 이 값이 없었다 (요청서 §1 "ZIP = 리포 밖 · push 뒤 메인").  그 ZIP 안 = 443 항목 (파일 405 · 폴더 38) · testzip PASS · 절대 경로 · `..` · 심볼릭 링크 0.
- 받은 ZIP = `4f358fbf-codex_rint2_rr_round4_1f9f3607eb2f_independent_20261109.zip` · 8,726,395 B · sha256 8233c6e830228bf3c5d94d58e22093957fe36ec8993ede613bf44dae84cb77fe · 615 항목 (파일 615 · 폴더 0) = package/ 405 · input/ 2 · reference_round3/ 3 · 머리 12 · arm_contract/ 30 · docs_tests/ 19 · resume_attack/ 144 (리포 밖 빈 폴더에 풂 · 절대 경로 · `..` · 심볼릭 링크 · 역슬래시 · 암호 0).
- Codex 매니페스트 = 이 폴더 SHA256SUMS (받은 그대로 · 614 줄 · 자기 빼고 전부 · 92,451 B · sha256 9421d276…) ↔ 받은 파일 = 다름 0 · 매니페스트에 없는 파일 0 · 빠진 파일 0 (우리 대조 스크립트).  ⚠ 이름이 겹쳐 **우리 폴더 매니페스트 = `IMPORT_SHA256SUMS`** (회차 ③ 의 SHA256SUMS 자리 · 아래).
- package/ = 우리가 보낸 ZIP 의 다시 묶음 → **리포에 안 넣음**: PIN.txt (78 B · sha256 88ea3a3c00b9c9ea39cbbb94d17b7231debb9cca46eb612efc176dd98b786e48 · 핀 40 자리 + 가지 이름) · SHA256SUMS (404 줄 · 61,282 B · sha256 7428f6781e9d0d59f35b34d02e47ff2cf27c4b587294570a4f7a7e741da8625e · 우리 대조 다름 0) · repo/ 403 = **우리 대조 403 / 403 같음** (전수 · 파일마다 git blob id · 크기 ↔ `git ls-tree -r -l 1f9f3607e` · 핀 tree 밖 경로 0) · input/ ZIP 안 405 파일 = package/ 405 파일과 바이트 같음 405 / 405.  Codex 기록도 404 해시 · 403 blob 일치 (판정문 머리 · §7).
- 넣은 것 = **180 파일** (이 폴더 · ZIP 과 같은 상대 경로 · 바이트 그대로 · 리포 `.gitattributes` 의 증거 폴더 규칙 = `-text` 라 CRLF 그대로 남는다 · CRLF 든 파일 57) — 머리 8 + arm_contract/ 18 + docs_tests/ 18 + input/ 1 + resume_attack/ 135.  판정문 1 = 판정문 자리.
- 뺀 것 = **434** — package/ 405 + 우리가 보낸 ZIP 1 + 우리 git blob 사본 3 (reference_round3/ = `17d45fb9c` 의 scripts/rint_r_chain.py · scripts/test_rint_r_chain.py · docs/reviews/codex_rint2_rr_round3_request_20261108.md · sha256 같음 = 48f0e7ff… · fedba635… · ab9ce6df…) + 주소 꼴 25 (Windows 사용자 폴더 경로 22 · 사용자@호스트 꼴 1 = 합성 git 신원 · 외부 URL 2 = GitHub API 응답 · 그중 1 은 이메일 꼴도 · 실제 주소는 아니거나 리포 밖 것이나 주소 꼴은 리포에 안 넣음 · 이번 반입 지시) — 이름 · 바이트 · sha256 = 아래 전수 표.
- 주소 꼴 검사 (우리 스크립트 · package/ · ZIP 빼고 209 파일 · 패턴 = IPv4 · 사용자@호스트 · `-P` 포트 · 호스트:포트 · URL · 드라이브 문자 경로 · Users 경로 · /mnt/<드라이브>/Users · /home/<이름> · 계정 이름 · 컴퓨터 이름 · AppData) — 걸린 32 = 뺌 25 (위) + 다른 까닭으로 뺌 2 (reference_round3 의 두 .py = 우리 git blob 안 합성 git 신원 · 사용자@pts 글 · 시험용 사설 IP 꼴 값) + 오탐 5 (넣음 4 = REPRODUCE.md 드라이브 자리 표시 경로 (Users 없음) · docs_tests/REPORT.md `파일:줄` 표기 · docs_tests/test_rint_r_chain.diff `+@check` 장식자 · docs_tests/mutation_raw_records.json 우리 컨테이너 scratch 경로 (원 기록 `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/logs/mutation_rr3.json` 에 이미 있음) / 판정문 1 = `파일:줄` 표기).  반입 뒤 이 폴더 다시 검사 = 걸림은 위 오탐 넷 + 우리 재현 산출물의 우리 컨테이너 scratch 경로 (회차 ③ 의 rc.json 과 같은 꼴) · `+@check` 뿐 (Windows 사용자 경로 0 · 사용자@호스트 주소 0 · 외부 URL 0).
- 이 폴더 = 넣은 180 + `_repro_ours_20261109/` 205 (우리 산출 202 + README.md · build_record.json · comparison.json) + 이 README · `IMPORT_SHA256SUMS` = 이 폴더 파일 전부 (자기 빼고 · 386 줄 · `sha256sum -c` 꼴 · Codex 의 SHA256SUMS 도 한 줄).
- 반입 때 ZIP 안 스크립트는 리포 안에서도 받은 폴더에서도 실행하지 않았다 — REPRODUCE.md 의 9 개는 다 읽은 뒤 리포 밖 스크래치 실행 폴더에 복사해 (sha256 = 원본과 같음) 우리 핀 작업 트리에 대고 돌렸다 → `docs/reviews/codex_rint2_rr_round4_evidence_20261109/_repro_ours_20261109/README.md`.
- 환경 (Codex · 판정문 머리 · §7) = Windows · Python 3.12.14 · 작은 합성 입력 · 실제 판독 함수 · scratch Git 원장 · 실제 물리 풀이 · WSL / ibb / kgy · GPU · 제출 · 등록 · 운영 원장 변경 없음 · 전체 게이트 · 495 전체 사슬 · 전체 변이 캠페인 · 현장 자격 = 다시 돌리지 않음 · 작성 측 481 → 487 → 491 → 495 · 3.8 · 끝-끝 51 · 전체 변이 수 = 받은 로그 재집계 (이번 새 실행 횟수 아님 · REPRODUCE.md 끝).

## 판정 요약 (판정문 머리 · §1–§7 줄임)

| 범위 | 판정 |
|---|---|
| 전체 | **지정 11 항목 한정 닫힘 · 재개 정책 전체 HOLD** — 새 P1 · P2 0 · 새 P3 1 (`RR4-01`) · 물리 실행 · 생산 GO 미부여 · "닫힘" = 지정 반례 · 최소 해결 범위 한정 (판정문 머리 · §6 · §7 끝) |
| §1 Q1 닫힘 11 | RR3-01 · PC12-03 (앞 런 판독 완료 계약) · RR3-02 · PC13-01 (원 반례와 지정 보완 · **같은 부류 전체 종결은 불가** = PC14-02 · 03 생존) · PC13-02 · PC13-04 · PC14-01 · PC14-04 (선언된 값 영역) · PC14-05 · PC14-06 (지정 네 생존 변이 · 추가 M56 = RR4-01) · SELF-158 (문장 정정만) (원장 verified_scope = §1 그 행 그대로 + 머리 한정) |
| §1 끝 · 그대로 남음 | PC13-03 · PC14-02 · 03 · PC11-05–08 · SELF-155 실침대 · 현장 · 봉인 조건 · Codex 는 원장을 고치지 않음 |
| §2 Q2 | 팔 기록 계약 수용 (510 / 510 · 38 / 38 · 728 분류 예외 0 · 14 / 14 · 30 / 30 · 3 / 3) · 원 회차 ③ 탐침 원문 rc 1 (옛 결함 존재 assert 반전) · 두 assert 정정 사본 rc 0 · 계약 밖 = 완료 기록의 SHA ↔ 디스크 원자료 · 다른 런 정직 기록 차용 · zero 자유 칸 · 반복 수 상한 · "728 위조 전부 거부" 라고 쓰면 틀림 |
| §3 Q3 | 지정 재개 수정 (PC13-01 두 칸 · PC14-05 칸 결손) 수용 · **PC14-02** (R1 / R2 = 복사 / 새 런 경계 다시 적기 · 원천 남음 · 자격 True · 다음 순서 통과 · 풀기 전 다시 셈 통과 · R1 = 실제 recover rc 0 · resume_ok True) · **PC14-03** (attempt.resume_of null = True · found_attempts_problem 만 거부 · 3 시도 from 다시 결속 = True · found_attempts_problem 도 통과) = **열림** · "봉인 전 한 번 확인" 반대 · 최소 처리 ① (권고) 자격 결과 쓰기와 다음 재개 허용 전에 공통 검증 (복사 표기 ↔ 원천 launch/end + 필요한 파일 신원 · attempt.resume_of ↔ 원장 entry · resume.from ↔ 그 시점 유효 사슬 끝) ② 각 recover · 재개마다 외부 관문 (코드 단독 GO 라 부르지 않음) · 새 P1 / P2 로 중복 등재 안 함 |
| §4 새 P3 RR4-01 | 변이 M56 (`src.is_dir()` → `src.exists()`) = 비동치 — 일반 파일 attempt_1 + 옆 attempt_1.rejected.json 에서 현재 = 사유 · 변이 = None · 역사 검출률 = **45/50 · 비동치 생존 5** (M46 JSON 영역 동치 유지) · 현재 코드는 그 입력 거부 (현재 CLI 재개 허용 결함 아님) · 자리 = 회차 ④ 요청서 103 줄 · 사전 공격 14 REPORT.md 9 줄 · 그 폴더 probes/mutate.py 60 줄 · 원기록 |
| §5 Q4 | 기대 변경 수용 (CT06_ARM 14936 = 실패 출력 3 칸 → ct06_pub 14944 · 기존 시험 함수 삭제 0 · 본문 변경 = t_PC12C 하나 · pid / sid = 생산 함수와 일치) · 제출 로그 479 / 481 재집계 = 독립 전체 사슬 재실행 아님 |
| §6 Q5 | "코드 · 설계 · 문서 GO (재개 정책 포함) + 봉인 전 확인" = 그대로 줄 수 없음 · 쓸 수 있는 문장 = 판정문 §6 인용 그대로 · 현장 자격 · kgy S0 실침대 · SELF-155 채택 · 12 단위 끝-끝 · 숫자 / 실행 정책 · 새 계획 봉인 = 남은 이름 목록만으로 완료 처리 안 함 |
| §7 | 검증 회계 (포장 404 · repo 403 · 의존 26 같음 · ARM 9 검사군 · 재개 15 경우 + M54 · 실제 recover 4 · 작은 검사 24 / 24 · 선별 재실행 · M56 · 제출 원로그 재집계) · 미실행 = 전체 게이트 · 전체 사슬 · 전체 변이 캠페인 · Linux /proc · flock · NFS · 실제 SIGKILL / 호스트 · 연구 계산 |

## 원장 변경 (이 반입 커밋 · `docs/reviews/findings.json`)

| 무엇 | 항목 |
|---|---|
| claimed_fixed → **verified** 11 (verified_by codex · verified_sha `1f9f3607e` · verified_in = 판정문 · verified_scope = 머리 "codex 11-09 Rint ② 재검토 회차 ④ (리뷰 핀 1f9f3607e) · 지정 범위 한정 · 재개 정책 전체 HOLD" + §1 그 행 · claimed_fixed_sha · evidence_tests 그대로 · owner 11 / 11 = claude 먼저 확인) | RR3-01 · RR3-02 · PC12-03 · PC13-01 · PC13-02 · PC13-04 · PC14-01 · PC14-04 · PC14-05 · PC14-06 · SELF-158 |
| verified 중 note 덧붙임 | PC13-01 (같은 부류 전체 종결 불가 = PC14-02 · 03) · PC12-03 (회차 ③ 부분 → 닫힘 · 모든 재개 출처 변조까지는 아님) · PC14-06 (추가 M56 = RR4-01) |
| open 그대로 · note 에 판정문 답 | PC14-02 · PC14-03 (§3 결과 표 · 봉인 때 한 번 확인 반대 · 선택지 ① ②) |
| 새 open 1 | RR4-01 (P3) |
| 원장 수 | 1030 → 1031 · open 341 → 342 · claimed_fixed 366 → 355 · verified 312 → 323 · wontfix 11 그대로 |

⚠ verified_sha = 회차 ② · ③ 반입과 같은 9 자리 꼴 (`1f9f3607e` = 리뷰 핀 `1f9f3607eb2f0118d322eeff780bba6eb17b85a2`) · verified_by = 정본 actor `codex`.

수정 계획 (결과 0 건 · 코드 변경 없음 · 1저자 비준 대기) = `docs/reviews/rint2_rr4_fix_plan_20261109.md`.

## 우리 트리 재현

→ `docs/reviews/codex_rint2_rr_round4_evidence_20261109/_repro_ours_20261109/README.md` — REPRODUCE.md 명령 9 개 rc = 전부 0 (replay_original.py 안의 원문 탐침 rc 1 · 정정 사본 rc 0 = Codex 와 같음) · **판정값 차이 0** (PC14-02 R1 · R2 · PC14-03 attempt-null · from-rebind = 자격 True · 실제 recover 4 회 rc 0 · False · False · True · True · RR4-01 M56 = current 사유 · mutant null · ARM 510 · 38 · 728 · 14 · 30 · 3 · 작은 검사 24 / 24 · 선별 재실행 t_RR3A 9 · t_RR3B 6 · t_RR3C 48 · t_PA14A 11 · 묶음 확인 403 · 26 · 2 · 판정에 닿지 않는 차이 = 환경 판 · 시각 · 경로 글 · 폴더 지문 · 경로에서 나온 합성 token · Windows CRLF 합성 팔 파일 · Windows 전용 O_NONBLOCK 한 줄 · 키 나눔표 · 파일 목록 차례 — comparison.json 의 OTHER = 0).

## 뺀 파일의 내용 (요지 · 우리 재현 판)

뺀 파일 이름 = 받은 ZIP 안 이름 (리포 경로 아님 · 따옴표 없이 적음).

- arm_contract/REPORT.md — ARM 하위 보고 (영문) · 결론 = 판정문 §2 · §1 의 RR3-01 · PC12-03 · PC13-02 · 04 · PC14-01 · 04 행과 같음 · 판정문에 없는 보조 관측: (a) 묶음 맨 위 arm_contract/ 의 원문 탐침 · 로그 · 원장 둘 · chain_side_rows.json = 앞선 중복 재생 (감사용 보존) (b) 목표 행 큰 정수 사유 글 길이 97–105 자 (c) 개발 중 리뷰 스크립트 오류 셋 (요청 env 정규화 · Runner 인수 순서 · 재사용 merge 대상) = 리뷰 스크립트에서만 고침 · 제품 결함으로도 통과로도 세지 않음 (판정문 §7) · 우리 재현 판 = `_repro_ours_20261109/arm_contract/results.json` · `_repro_ours_20261109/arm_contract/value_matrix.json`.
- resume_attack/REPORT.md — 재개 하위 보고 (한글) · 결론 = 판정문 §3 · §1 의 PC13-01 · PC14-05 · 06 행과 같음 · 판정문보다 자세한 것 (수정 계획 §1 · §2 에 옮김): R1 = 요약 7 칸 · R2 = 6 칸 편집 (payload · 로그 · launch/end · attempt.json 그대로 · only_summary_changed True) · attempt-null 경로 자리 = read_attempt 3473–3489 (키 · schema · 번호 · target · 커밋 꼴만) · resume_rerun_problem 4388–4396 (null = 새 시도로 봄) · recover 원장 대조 7948–7951 (target · 시작 커밋 조상만) · 사슬 사전 다시 셈 3792–3799 · found_attempts_problem 4843–4848 = 판정 · 합치기까지 미뤄짐 · from 경로 = 범위 4403–4409 만 · 자동 확인 권고 구체안 (found_attempts_problem 계약 재사용 · from = 그 시도 앞까지의 adoption(…, upto=n).effective · copied / new 경계 = 원천 · 대상 launch/end 결합 + 복사 기록 바이트 · 그 뒤 실제 첫 새 런에 payload 다시 대조 · 양성 보존 = 정직 복사 · 첫 새 런 전 멈춤 · 부분 재실행 멈춤 · 대조 뒤 멈춤 · 3 시도 사슬) · 매회 수동 관문 대안 (책임 · 시점 · 불변 증거 · 해제 조건 · 표현 = "매회 수동 확인을 조건으로 한 제한적 재개 운영 수용") · 우리 재현 판 = `_repro_ours_20261109/resume_attack/results.json`.
- resume_attack/results.json · resume_attack/frozen_cases/*/synthetic_ledger.jsonl (6) · scoped_regression.json · docs_tests/tiny_checks.json · arm_contract/ 원장 (closure_replay 2 · original_replay 2 · 맨 위 2) · arm_contract/original_replay/stderr.log — 우리 재현 판 = `_repro_ours_20261109/` 의 같은 상대 자리 (맨 위 둘 빼고 · 잎 대조 = `_repro_ours_20261109/comparison.json`).
- resume_attack/probe_resume_independent.py = 탐침 (합성 git 신원 꼴 하나) · 우리 실행 사본 sha256 = 원본 83622e5a83bd0de7c97d4a368c0b3fe66ce4fb08def54fabe0a0bd80d79fa014 (`_repro_ours_20261109/build_record.json`).
- remote_provenance.json (GitHub API 응답 = 핀 commit · tree 들 · 작성자 이메일 칸) — 우리 git 대조: 핀 commit tree = cc6aefe7a9013885c8da0d700cff1cc981033f77 (`git rev-parse 1f9f3607e^{tree}`) · repo/ 403 = 핀 blob 403 / 403 같음 (위).
- dependency_delta.json (GitHub API 트리 응답 = 옛 핀 · 새 핀 scripts/) — 우리 git 대조: 의존 28 (package/repo/scripts) 에 대해 `git diff --name-only 17d45fb9c 1f9f3607e --` = rint_r_chain.py · test_rint_r_chain.py 둘만 (26 같음 · 판정문 §1 과 같음).
- arm_contract/ 의 개발 실패 셋 (initial · second · third_harness_failure.json) · original_pc12_probe.log — Codex 개발 · 앞선 중복 재생 기록 (판정문 §7 · arm_contract/REPORT.md 끝) · 다시 만들지 않음.
- input/codex_rint2_rr_round4_1f9f3607eb2f.zip = 우리가 보낸 ZIP (= package/) · reference_round3/ = 우리 git `17d45fb9c` 사본 셋.

## 항목 전수 (615 · package/repo/ 403 = 한 줄로 묶음 · 처분 = 넣음 · 판정문 자리 · 뺌)

"넣음" = 이 폴더의 같은 상대 경로에 바이트 그대로.

| # | ZIP 항목 | 바이트 | sha256 | 처분 | 까닭 · 대조 |
|---:|---|---:|---|---|---|
| 1 | REPRODUCE.md | 4,879 | 48adc3a2e620118b5e31388b37fda59aa13f3f667e988024d63ebe3ee08b6f4c | 넣음 | 바이트 그대로 (주소 검사 오탐 = 드라이브 자리 표시 경로 (C:/path/to/pinned/repo · Users 없음)) |
| 2 | SHA256SUMS | 92,451 | 9421d276100dff023dd651d10bc033d543d3c88994d8d976e9e108bd3f88b343 | 넣음 | 바이트 그대로 |
| 3 | arm_contract/REPORT.md | 8,698 | 91b311009b36b72120da0031cef1bfe8847c0afde752ea3db41a69df7e45ca0e | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 4 | arm_contract/chain_side_rows.json | 64,698 | 8f687d6530081abb194fd9b74292792d9be05e6f981d3b8bf9c74440068afcb4 | 넣음 | 바이트 그대로 |
| 5 | arm_contract/closure_oracle.diff | 1,327 | 501a73bbecdbe4a6c012cd8490a48931ba1d6372a202d75a6299c6c8554ce965 | 넣음 | 바이트 그대로 |
| 6 | arm_contract/closure_replay/chain_side_rows.json | 64,698 | 8f687d6530081abb194fd9b74292792d9be05e6f981d3b8bf9c74440068afcb4 | 넣음 | 바이트 그대로 |
| 7 | arm_contract/closure_replay/counterexample_edited_ledger.jsonl | 1,027 | 00e47fef05586ccb364a709cc5228c305213b93984dea5fe938c4f75312e1899 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/arm_contract/closure_replay/counterexample_edited_ledger.jsonl` |
| 8 | arm_contract/closure_replay/counterexample_edited_summary.json | 719 | f87169b86e8f1235477197e751b7e846340f2f188d2c6ac1905f79e93b311bcc | 넣음 | 바이트 그대로 |
| 9 | arm_contract/closure_replay/counterexample_original_ledger.jsonl | 1,027 | bbe09f27b7b33360a4373d6fbb505243691195364f68a9d177f0726bfd6e74e7 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/arm_contract/closure_replay/counterexample_original_ledger.jsonl` |
| 10 | arm_contract/closure_replay/counterexample_original_summary.json | 721 | b02251263fee425d276c94f493a9fcb2949301ab9c54459174c6280ef4dbf972 | 넣음 | 바이트 그대로 |
| 11 | arm_contract/closure_replay/probe.py | 13,123 | fef77a65331b0b08f57d791db28f69e0e8cb8eb2728305ede221c87a366398ab | 넣음 | 바이트 그대로 |
| 12 | arm_contract/closure_replay/results.json | 8,977 | 41e8f183bb7b21aeda87abfa399bb3d73874ec626298cf062849d6548b81f16a | 넣음 | 바이트 그대로 |
| 13 | arm_contract/closure_replay/stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 넣음 | 바이트 그대로 |
| 14 | arm_contract/closure_replay/stdout.log | 8,979 | 6283c8d7c400ee4c54bbb788c1c83e45c7c02cc9f6303264cc6ea122210fc847 | 넣음 | 바이트 그대로 |
| 15 | arm_contract/counterexample_edited_ledger.jsonl | 1,011 | 9bcb9c8ea0d603c254b667dc000d9fbe12c33e7b01de1456aebd6eb5e970ae63 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 16 | arm_contract/counterexample_original_ledger.jsonl | 1,011 | ee8b7aa430b421190136af9448c0ceae2410eaca58aa8c633c8ed7559b123bb7 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 17 | arm_contract/initial_harness_failure.json | 42,780 | cf286c7e64fe0e9ebf52117d6a2d30453f21201937fbc0c53720f6d0d7ccba27 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 18 | arm_contract/original_pc12_probe.log | 320 | 208e95181425f9062c942dad1550ee4b2f804468f6beaa7a6a2266ec352cf30c | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 19 | arm_contract/original_pc12_probe.py | 13,097 | 7f335c758c036c6de5ab10ef5b9ab3d35d6eb10ab3f0182694bdea03914b74d7 | 넣음 | 바이트 그대로 |
| 20 | arm_contract/original_replay/chain_side_rows.json | 64,698 | 8f687d6530081abb194fd9b74292792d9be05e6f981d3b8bf9c74440068afcb4 | 넣음 | 바이트 그대로 |
| 21 | arm_contract/original_replay/counterexample_edited_ledger.jsonl | 1,028 | 88abdf3f867f2049a952992d06675b01558d210cb566cb52c76ef470c9ce0243 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/arm_contract/original_replay/counterexample_edited_ledger.jsonl` |
| 22 | arm_contract/original_replay/counterexample_original_ledger.jsonl | 1,028 | a482e5a0ad5550c21bfbf1f0519dc81763018eabf431360018bc8224a0417f51 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/arm_contract/original_replay/counterexample_original_ledger.jsonl` |
| 23 | arm_contract/original_replay/probe.py | 13,097 | 7f335c758c036c6de5ab10ef5b9ab3d35d6eb10ab3f0182694bdea03914b74d7 | 넣음 | 바이트 그대로 |
| 24 | arm_contract/original_replay/stderr.log | 322 | 5bc54eeb4079767a8750cc071260d7452ed38fdef46133106a3791ae6a875607 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/arm_contract/original_replay/stderr.log` |
| 25 | arm_contract/original_replay/stdout.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 넣음 | 바이트 그대로 |
| 26 | arm_contract/probe_arm_contract.py | 18,635 | 58bb5fbbaa658d01746cacfb288f29dc400280d1a6e19c3530f1b0e7cdffc51f | 넣음 | 바이트 그대로 |
| 27 | arm_contract/replay_original.py | 1,988 | be657aa017841520e137c832488e781c91bb67526a8dd55c631d2870904ae258 | 넣음 | 바이트 그대로 |
| 28 | arm_contract/replay_results.json | 572 | fdff945c4c760b53d3857d870412655be5a18fd9e11f1e88d34aad61073e5d13 | 넣음 | 바이트 그대로 |
| 29 | arm_contract/results.json | 48,165 | b9d297cbb542cb60915b763db758034de575efb45c5bd07c1727cdfa1bd201b9 | 넣음 | 바이트 그대로 |
| 30 | arm_contract/second_harness_failure.json | 41,996 | c931f216acad04cd6820af50e3312fe017965684dd12e3ee9a826342006795d7 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 31 | arm_contract/third_harness_failure.json | 48,334 | 57d71ee216f737b543bc447fd21df5f1c8db08c944f9023a07398025362920f8 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 32 | arm_contract/value_matrix.json | 75,082 | 50c23f823df3aebd2d6cc3340f66575994be964543ac9d3f6f0f764b4121f633 | 넣음 | 바이트 그대로 |
| 33 | build_evidence.py | 2,130 | 04467e5ab31fde79f8b66edefffc8e3ccd43950ccb8ca63b7532359ddb1c9919 | 넣음 | 바이트 그대로 |
| 34 | codex_review_rint2_rr_round4_20261109.md | 16,854 | ae24483635ead3574001413df9599930e385a4fb88ca4de0710ac4ae98163da2 | 판정문 자리 | `docs/reviews/codex_review_rint2_rr_round4_20261109.md` · 바이트 같음 (CR 0) |
| 35 | dependency_delta.json | 228,168 | 4494fa2844dfcf11457f395ad21f8f7ae5dbfd2f1d37cee25255d485bb4ffc49 | 뺌 | 주소 꼴 = 외부 URL (GitHub API 응답 · 저장소 소유자 경로) → 이름 · sha256 만 · 내용 = 우리 git 대조 (의존 28 중 바뀜 2 · 같음 26 · 아래 "뺀 파일의 내용") |
| 36 | docs_tests/REPORT.md | 14,764 | 864920a40067cc906a7e17486aaa4bd9ea3e4bf05d13a19164dd0d95262098ec | 넣음 | 바이트 그대로 (주소 검사 오탐 = 파일:줄 표기 (예 rint_r_chain.py:2177–2180)) |
| 37 | docs_tests/audit_docs_tests.py | 6,607 | 01b826c78fac146caed77a2dab1cbb6a07031ab20deca1e73ad004bfa6518d34 | 넣음 | 바이트 그대로 |
| 38 | docs_tests/codex_rint2_rr_round3_request_20261108.diff | 18,507 | d124f19c36f2fd415af9469081a4b4f0c891502a9782ed7a3892eb6d8794e4ac | 넣음 | 바이트 그대로 |
| 39 | docs_tests/diff_inventory.json | 2,384 | cac24cb2a889cf52b861124ecc4fe805fb6e8659f2ba3d665b8adde1cb248f41 | 넣음 | 바이트 그대로 |
| 40 | docs_tests/m56_result.json | 1,055 | 777758d2e2a21c0d0e8ffaf42717ce159b491dd3c0dac238206cba6c0dfeec91 | 넣음 | 바이트 그대로 |
| 41 | docs_tests/m56_synthetic/attempt_1 | 17 | b0980e73caaef2dbc7b2acf951ecbb36a39ec3753a6046a3ee20fcaab4af3041 | 넣음 | 바이트 그대로 |
| 42 | docs_tests/m56_synthetic/attempt_1.rejected.json | 4 | e3566b3a06430868d71e9287dfd6c6c520a3da027aabea01951d407ee131dc2f | 넣음 | 바이트 그대로 |
| 43 | docs_tests/mutation_counts.json | 546 | 0d32b223b5015a9d654c0cdd2bcb1246ac55a0ae2cc3906405781be50ff111fc | 넣음 | 바이트 그대로 |
| 44 | docs_tests/mutation_raw_records.json | 21,452 | 20f728ac985ca6535b60fc1bcb7174edbe0e7878139049e6d9d22f6a8615ca9e | 넣음 | 바이트 그대로 (주소 검사 오탐 = 우리 컨테이너 scratch 경로 (/tmp/claude-0/… · 원 기록 docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/logs/mutation_rr3.json 에 이미 있음)) |
| 45 | docs_tests/preattack14_mutation_counts.json | 965 | ed998a9f334b19e8889a32e410dee59dd46f60dfe2f0cecd66c2b61aa5956de4 | 넣음 | 바이트 그대로 |
| 46 | docs_tests/probe_m56.py | 1,991 | da066c2a3d2d18c64026fb5e1e34d69de072155dffb3b9bd2ff63c6b2589bd63 | 넣음 | 바이트 그대로 |
| 47 | docs_tests/raw_log_counts.json | 20,322 | 0e723b435622eb55593ff832e15619b904d437352332da5818ca33b7c2004608 | 넣음 | 바이트 그대로 |
| 48 | docs_tests/rint_r_chain.diff | 39,836 | 6f52c0736c6741446508b2e8fa35175600667f5d8241e28f70d033cd9205642f | 넣음 | 바이트 그대로 |
| 49 | docs_tests/row_counts.json | 8,513 | 75769dbd247de0ba39e58aadc759d8bc174eaee0a65b1a38a4a3083736f07047 | 넣음 | 바이트 그대로 |
| 50 | docs_tests/rr3_02_corrections.json | 4,141 | 309959242ae6d76a998234f19b7dc2a4da076e33d334bad657bc8f661ebe2687 | 넣음 | 바이트 그대로 |
| 51 | docs_tests/survivor_coverage.json | 1,369 | e35f3878ea9796b927121aa3c0aa0ecd3e5a7473ca7ff899ec2ce6e3fee8ac2a | 넣음 | 바이트 그대로 |
| 52 | docs_tests/test_rint_r_chain.diff | 87,624 | 29a774bc5a70dd508620f715d57d5fe73934227bf41cbcac60b4a9f8c23b677e | 넣음 | 바이트 그대로 (주소 검사 오탐 = +@check 장식자 (사용자@호스트 꼴 오탐)) |
| 53 | docs_tests/tiny_checks.json | 5,177 | 7dc9f5134ca3ba5a82803a8d78ec4fdcbfb8afe53a497bd49e40d736c8bf0161 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/docs_tests/tiny_checks.json` |
| 54 | docs_tests/tiny_docs_tests.py | 5,163 | bdba8adb5bb867841b937f588f30664d56302f0a2c309e859103f7986e5e0530 | 넣음 | 바이트 그대로 |
| 55 | input/CODEX_PASTE_round4.md | 2,896 | a60bfa218e9b07773df00336daa97570c9f766e5c3f7cbdd3332a7d64ff0bf59 | 넣음 | 바이트 그대로 |
| 56 | input/codex_rint2_rr_round4_1f9f3607eb2f.zip | 3,992,042 | ab3d7da16df298be7378ea62251d06983e319860f8688f14e498256882d23b3f | 뺌 | 우리가 보낸 ZIP 자체 · 안 443 항목 (파일 405) = package/ 405 파일과 바이트 같음 405 / 405 · testzip PASS |
| 57 | integrity.json | 115,026 | f9fc1b46b4239b174290c630ae05307bd4fb3572063a714352b7b020669b2f7c | 넣음 | 바이트 그대로 |
| 58 | package/PIN.txt | 78 | 88ea3a3c00b9c9ea39cbbb94d17b7231debb9cca46eb612efc176dd98b786e48 | 뺌 | 우리가 보낸 ZIP 의 PIN.txt (핀 40 자리 + 가지 이름) |
| 59 | package/SHA256SUMS | 61,282 | 7428f6781e9d0d59f35b34d02e47ff2cf27c4b587294570a4f7a7e741da8625e | 뺌 | 우리가 보낸 ZIP 의 SHA256SUMS (404 줄 · 우리 대조 다름 0) |
| 60 | package/repo/ | 13,516,825 | (파일마다 · Codex SHA256SUMS · 위 package/SHA256SUMS) | 뺌 | 403 파일 = 우리 핀 `1f9f3607e` blob · git blob id 403 / 403 같음 (`git ls-tree -r -l` 대조) · 핀 tree 밖 경로 0 |
| 61 | reference_round3/docs/reviews/codex_rint2_rr_round3_request_20261108.md | 39,146 | ab9ce6dff6df858c66f8776b8c893c5155bcc7121a48edebf075648efdb7f6e1 | 뺌 | = 우리 git `17d45fb9c:docs/reviews/codex_rint2_rr_round3_request_20261108.md` (sha256 같음 · 리포 기록에 있음) |
| 62 | reference_round3/scripts/rint_r_chain.py | 591,849 | 48f0e7fff068eea752407ad56955c159e937f8a33801148786b0d5a3e650f95c | 뺌 | = 우리 git `17d45fb9c:scripts/rint_r_chain.py` (sha256 같음 · 리포 기록에 있음) |
| 63 | reference_round3/scripts/test_rint_r_chain.py | 1,025,689 | fedba635c5ea52e88d38341308637a025b44665c0c3e40cb49cdae50af5c7811 | 뺌 | = 우리 git `17d45fb9c:scripts/test_rint_r_chain.py` (sha256 같음 · 리포 기록에 있음) |
| 64 | remote_provenance.json | 692,786 | d96d7b36089a728662d39387aae1d777f9839b3a256b0e156453d8f5183c3f35 | 뺌 | 주소 꼴 = 외부 URL (GitHub API 응답 · 저장소 소유자 경로) + 이메일 꼴 → 이름 · sha256 만 · 내용 = 우리 git 대조 (핀 commit tree cc6aefe7… · 아래 "뺀 파일의 내용") |
| 65 | resume_attack/REPORT.md | 13,315 | a62cedac15209bd01fe8e6cf4a70c2795731fccefb028bb477e9e54e472f04f5 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 66 | resume_attack/cli_PC13_two_fields.log | 155 | 622132acd33edd4a79b22b83f20a54610ddd49e64263d890d5a7a5eae6fd51b6 | 넣음 | 바이트 그대로 |
| 67 | resume_attack/cli_PC14_02_R1.log | 154 | b6d9a1605224d5e535b568a4e5bdb9b3507bc1941eb7f9e315af4222bfde5628 | 넣음 | 바이트 그대로 |
| 68 | resume_attack/cli_PC14_03_attempt_null.log | 154 | b6d9a1605224d5e535b568a4e5bdb9b3507bc1941eb7f9e315af4222bfde5628 | 넣음 | 바이트 그대로 |
| 69 | resume_attack/cli_honest_mismatch.log | 153 | 7c646b6f424c9eba3a3cf609cf37b5690f2d0397aef7a844b71020f5f6ab033f | 넣음 | 바이트 그대로 |
| 70 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 71 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 72 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 73 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 74 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 75 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/groups/L02_ceiling.end.json | 165 | 11421b4574f35903480fd416aac05e9a558c53be70356bab8c67b7dcfd796145 | 넣음 | 바이트 그대로 |
| 76 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/groups/L02_ceiling.launch.json | 103 | 17cd83aaf893f46f21e31ed6f343cda0c0c855681943235c9ae51a5306c5ebde | 넣음 | 바이트 그대로 |
| 77 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 78 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 79 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 80 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 81 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 36 | 47c419cf1fdf3fb2908e018c2fb5a611dd83367855e7488d69e43d202f682548 | 넣음 | 바이트 그대로 |
| 82 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/attempt.json | 172 | 8577c253165287bced23f3572f05ce7119c9e2cd1a934d7b2d89451543ac212f | 넣음 | 바이트 그대로 |
| 83 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 84 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 85 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/groups/L02_ceiling.end.json | 165 | 612a67684ad80102e32c76ed2877874fda62a3cd1a90835d4368492df13aeb21 | 넣음 | 바이트 그대로 |
| 86 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/groups/L02_ceiling.launch.json | 103 | f969b8c8531c5f8e1321a19d3af1f66fb1a6df11246355e4ec3f78abcfb0076b | 넣음 | 바이트 그대로 |
| 87 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/ladder_summary.json | 2,088 | ef621317264368a14102b4e2598978d6a84a27fa4c495383660247bfeb876574 | 넣음 | 바이트 그대로 |
| 88 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 89 | resume_attack/frozen_cases/PC13_01_two_fields/attempt_2/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 90 | resume_attack/frozen_cases/PC13_01_two_fields/synthetic_ledger.jsonl | 2,032 | 4baa69c6f237534be323382c163fe1d4126e98ac09ed0b1817546f7a21495d82 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/PC13_01_two_fields/synthetic_ledger.jsonl` |
| 91 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 92 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 93 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 94 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 95 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 96 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/groups/L02_ceiling.end.json | 165 | 11421b4574f35903480fd416aac05e9a558c53be70356bab8c67b7dcfd796145 | 넣음 | 바이트 그대로 |
| 97 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/groups/L02_ceiling.launch.json | 103 | 17cd83aaf893f46f21e31ed6f343cda0c0c855681943235c9ae51a5306c5ebde | 넣음 | 바이트 그대로 |
| 98 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 99 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 100 | resume_attack/frozen_cases/PC14_02_R1/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 101 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 102 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 36 | 47c419cf1fdf3fb2908e018c2fb5a611dd83367855e7488d69e43d202f682548 | 넣음 | 바이트 그대로 |
| 103 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/attempt.json | 172 | 8577c253165287bced23f3572f05ce7119c9e2cd1a934d7b2d89451543ac212f | 넣음 | 바이트 그대로 |
| 104 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 105 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 106 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/groups/L02_ceiling.end.json | 165 | 612a67684ad80102e32c76ed2877874fda62a3cd1a90835d4368492df13aeb21 | 넣음 | 바이트 그대로 |
| 107 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/groups/L02_ceiling.launch.json | 103 | f969b8c8531c5f8e1321a19d3af1f66fb1a6df11246355e4ec3f78abcfb0076b | 넣음 | 바이트 그대로 |
| 108 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/ladder_summary.json | 2,036 | e489a56abe616b491681524b0956f7e353ddbbe668a2031510d53891541e4c29 | 넣음 | 바이트 그대로 |
| 109 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 110 | resume_attack/frozen_cases/PC14_02_R1/attempt_2/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 111 | resume_attack/frozen_cases/PC14_02_R1/synthetic_ledger.jsonl | 2,015 | 84058c8abfae27587a7086c30e6803d95a02f0f07655b93b3b6173eb64bd9b90 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/PC14_02_R1/synthetic_ledger.jsonl` |
| 112 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 113 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 114 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 115 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 116 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 117 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/groups/L02_ceiling.end.json | 165 | 11421b4574f35903480fd416aac05e9a558c53be70356bab8c67b7dcfd796145 | 넣음 | 바이트 그대로 |
| 118 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/groups/L02_ceiling.launch.json | 103 | 17cd83aaf893f46f21e31ed6f343cda0c0c855681943235c9ae51a5306c5ebde | 넣음 | 바이트 그대로 |
| 119 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 120 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 121 | resume_attack/frozen_cases/PC14_02_R2/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 122 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 123 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 36 | 47c419cf1fdf3fb2908e018c2fb5a611dd83367855e7488d69e43d202f682548 | 넣음 | 바이트 그대로 |
| 124 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/attempt.json | 172 | 8577c253165287bced23f3572f05ce7119c9e2cd1a934d7b2d89451543ac212f | 넣음 | 바이트 그대로 |
| 125 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 126 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 127 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/groups/L02_ceiling.end.json | 165 | 612a67684ad80102e32c76ed2877874fda62a3cd1a90835d4368492df13aeb21 | 넣음 | 바이트 그대로 |
| 128 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/groups/L02_ceiling.launch.json | 103 | f969b8c8531c5f8e1321a19d3af1f66fb1a6df11246355e4ec3f78abcfb0076b | 넣음 | 바이트 그대로 |
| 129 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/ladder_summary.json | 2,046 | c75848e750142c7d538b9a23588bb790aeddfa4928803b97473ec30a4db2fa04 | 넣음 | 바이트 그대로 |
| 130 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 131 | resume_attack/frozen_cases/PC14_02_R2/attempt_2/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 132 | resume_attack/frozen_cases/PC14_02_R2/synthetic_ledger.jsonl | 2,015 | 029165def47b25150512bf971aeea211a9ef047c8d4317a3eb39eb67c740e207 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/PC14_02_R2/synthetic_ledger.jsonl` |
| 133 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 134 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 135 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 136 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 137 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 138 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/groups/L02_ceiling.end.json | 165 | 11421b4574f35903480fd416aac05e9a558c53be70356bab8c67b7dcfd796145 | 넣음 | 바이트 그대로 |
| 139 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/groups/L02_ceiling.launch.json | 103 | 17cd83aaf893f46f21e31ed6f343cda0c0c855681943235c9ae51a5306c5ebde | 넣음 | 바이트 그대로 |
| 140 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 141 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 142 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 143 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 144 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 36 | 47c419cf1fdf3fb2908e018c2fb5a611dd83367855e7488d69e43d202f682548 | 넣음 | 바이트 그대로 |
| 145 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/attempt.json | 175 | ff963ad30e2bac1e00ead1e7fdc5fdd6c890b50d2ece95fb4e583699fd996191 | 넣음 | 바이트 그대로 |
| 146 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 147 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 148 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/groups/L02_ceiling.end.json | 165 | 612a67684ad80102e32c76ed2877874fda62a3cd1a90835d4368492df13aeb21 | 넣음 | 바이트 그대로 |
| 149 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/groups/L02_ceiling.launch.json | 103 | f969b8c8531c5f8e1321a19d3af1f66fb1a6df11246355e4ec3f78abcfb0076b | 넣음 | 바이트 그대로 |
| 150 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/ladder_summary.json | 1,886 | ba6dfa6388dd93a1b386c680c344f901691c01e900ad23c8c351bc4fb2da9b14 | 넣음 | 바이트 그대로 |
| 151 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 152 | resume_attack/frozen_cases/PC14_03_attempt_null/attempt_2/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 153 | resume_attack/frozen_cases/PC14_03_attempt_null/synthetic_ledger.jsonl | 2,035 | e5dc78ecfc318a663a1a8a970d5487cc6bfe17408168bf23d8af68330f3252b9 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/PC14_03_attempt_null/synthetic_ledger.jsonl` |
| 154 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 155 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 156 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 157 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/groups/L01_floor.end.json | 163 | 50ed8b31dc587b9fe8a5bdc679d9d0536ee7f557f5be84189f18a8dbb301d897 | 넣음 | 바이트 그대로 |
| 158 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/groups/L01_floor.launch.json | 101 | f91f055722f5b813eb9cbf4a8d33d4f38bb7620c9434c1d90f10d7358c0e8815 | 넣음 | 바이트 그대로 |
| 159 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/groups/L02_ceiling.end.json | 165 | a4d0cb717608edba2aacdf8ac07f674ceb59484f827459e9819f0194cf6bb7d8 | 넣음 | 바이트 그대로 |
| 160 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/groups/L02_ceiling.launch.json | 103 | b620d7fa74e6198bfdca7bb85228da3567de66841c1918b72c7c2fa0f4dafed1 | 넣음 | 바이트 그대로 |
| 161 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 162 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 163 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 164 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 165 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 44 | a846a6fcee2e540c3b2d91a89b2fea055fb673d2433cd9a21f58833e72253f90 | 넣음 | 바이트 그대로 |
| 166 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/attempt.json | 172 | 8577c253165287bced23f3572f05ce7119c9e2cd1a934d7b2d89451543ac212f | 넣음 | 바이트 그대로 |
| 167 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/groups/L01_floor.end.json | 163 | 50ed8b31dc587b9fe8a5bdc679d9d0536ee7f557f5be84189f18a8dbb301d897 | 넣음 | 바이트 그대로 |
| 168 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/groups/L01_floor.launch.json | 101 | f91f055722f5b813eb9cbf4a8d33d4f38bb7620c9434c1d90f10d7358c0e8815 | 넣음 | 바이트 그대로 |
| 169 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/groups/L02_ceiling.end.json | 165 | bac7e91036dbbd497fc4bfbe753a33ec5ca2cf97b26afe0cd33b2654d09bf163 | 넣음 | 바이트 그대로 |
| 170 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/groups/L02_ceiling.launch.json | 103 | 4927c2347886f7dfda210c56841edfd67ae82571929a1251f65dc219f92f3dec | 넣음 | 바이트 그대로 |
| 171 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/ladder_summary.json | 1,469 | 6179c5a2c6b695d3c4e228057e4f69aa02d87de9b430c00313d363b3297b6590 | 넣음 | 바이트 그대로 |
| 172 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 173 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_2/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 174 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 175 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 176 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/attempt.json | 172 | 38c6a2b96439fbc9eea6e64e5f25bd8e884e0bb95d9e805e03f81cebe89fd3f3 | 넣음 | 바이트 그대로 |
| 177 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/groups/L01_floor.end.json | 163 | 50ed8b31dc587b9fe8a5bdc679d9d0536ee7f557f5be84189f18a8dbb301d897 | 넣음 | 바이트 그대로 |
| 178 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/groups/L01_floor.launch.json | 101 | f91f055722f5b813eb9cbf4a8d33d4f38bb7620c9434c1d90f10d7358c0e8815 | 넣음 | 바이트 그대로 |
| 179 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/groups/L02_ceiling.end.json | 165 | 3af215a335a43aea4f7f797422c2339c9a8973eeb925af9a095eb13c6ec05d70 | 넣음 | 바이트 그대로 |
| 180 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/groups/L02_ceiling.launch.json | 103 | f4a40dd84be625d91852f61a92fd1bd59e51c00fdc67a260f8451a028a6983e8 | 넣음 | 바이트 그대로 |
| 181 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/ladder_summary.json | 2,087 | 80874edcd4c7757fc5060515bd3c88853168eeb09b5c0b8c61bc4d634ea0208e | 넣음 | 바이트 그대로 |
| 182 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 183 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/attempt_3/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 184 | resume_attack/frozen_cases/PC14_03_from_rebind_forged/synthetic_ledger.jsonl | 2,997 | 8c953d49fcb1edb6db3e47eb1d19c42be6a86affc734224573e09dc9567b07bd | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/PC14_03_from_rebind_forged/synthetic_ledger.jsonl` |
| 185 | resume_attack/frozen_cases/honest_mismatch/attempt_1/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 186 | resume_attack/frozen_cases/honest_mismatch/attempt_1/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 35 | a82664881df3195193e90b77269140063beac2c2dda3f9bedcb445bd0488aa98 | 넣음 | 바이트 그대로 |
| 187 | resume_attack/frozen_cases/honest_mismatch/attempt_1/attempt.json | 175 | 81e028dce277c0f02cf1b1443245256ed3f1c2f9dcef8590c946f9a26418729b | 넣음 | 바이트 그대로 |
| 188 | resume_attack/frozen_cases/honest_mismatch/attempt_1/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 189 | resume_attack/frozen_cases/honest_mismatch/attempt_1/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 190 | resume_attack/frozen_cases/honest_mismatch/attempt_1/groups/L02_ceiling.end.json | 165 | 11421b4574f35903480fd416aac05e9a558c53be70356bab8c67b7dcfd796145 | 넣음 | 바이트 그대로 |
| 191 | resume_attack/frozen_cases/honest_mismatch/attempt_1/groups/L02_ceiling.launch.json | 103 | 17cd83aaf893f46f21e31ed6f343cda0c0c855681943235c9ae51a5306c5ebde | 넣음 | 바이트 그대로 |
| 192 | resume_attack/frozen_cases/honest_mismatch/attempt_1/ladder_summary.json | 1,336 | bef434a58ef53c056ab04b6ef329572bc00fd3a7ec1fb8771dd63b31228e812a | 넣음 | 바이트 그대로 |
| 193 | resume_attack/frozen_cases/honest_mismatch/attempt_1/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 194 | resume_attack/frozen_cases/honest_mismatch/attempt_1/logs/L02_ceiling.log | 23 | a15147f0bb9260419c5c117f56eb8f485fc1395adf48a271cba8d28e0ca8ee01 | 넣음 | 바이트 그대로 |
| 195 | resume_attack/frozen_cases/honest_mismatch/attempt_2/L01_floor_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 26 | b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81 | 넣음 | 바이트 그대로 |
| 196 | resume_attack/frozen_cases/honest_mismatch/attempt_2/L02_ceiling_arm1/p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json | 36 | 47c419cf1fdf3fb2908e018c2fb5a611dd83367855e7488d69e43d202f682548 | 넣음 | 바이트 그대로 |
| 197 | resume_attack/frozen_cases/honest_mismatch/attempt_2/attempt.json | 172 | 8577c253165287bced23f3572f05ce7119c9e2cd1a934d7b2d89451543ac212f | 넣음 | 바이트 그대로 |
| 198 | resume_attack/frozen_cases/honest_mismatch/attempt_2/groups/L01_floor.end.json | 163 | 6a2ec956ff58baf1e1f6711b6768ae2abe50cd4fa7571336644fc82d45a8ed75 | 넣음 | 바이트 그대로 |
| 199 | resume_attack/frozen_cases/honest_mismatch/attempt_2/groups/L01_floor.launch.json | 101 | 5df6ef1e4d42d0a3cfec409545d71f8b0286640e47346c1f5515dcd580c1d407 | 넣음 | 바이트 그대로 |
| 200 | resume_attack/frozen_cases/honest_mismatch/attempt_2/groups/L02_ceiling.end.json | 165 | 612a67684ad80102e32c76ed2877874fda62a3cd1a90835d4368492df13aeb21 | 넣음 | 바이트 그대로 |
| 201 | resume_attack/frozen_cases/honest_mismatch/attempt_2/groups/L02_ceiling.launch.json | 103 | f969b8c8531c5f8e1321a19d3af1f66fb1a6df11246355e4ec3f78abcfb0076b | 넣음 | 바이트 그대로 |
| 202 | resume_attack/frozen_cases/honest_mismatch/attempt_2/ladder_summary.json | 2,095 | 16147bf4b2e701a57398b72836ca7cabe8d0f0aa74957ab114df0074ab55a593 | 넣음 | 바이트 그대로 |
| 203 | resume_attack/frozen_cases/honest_mismatch/attempt_2/logs/L01_floor.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 204 | resume_attack/frozen_cases/honest_mismatch/attempt_2/logs/L02_ceiling.log | 19 | 559e7cca7f0bdd509ad935bbbb1b274e4505e845065a0f698216bcf000fe8aec | 넣음 | 바이트 그대로 |
| 205 | resume_attack/frozen_cases/honest_mismatch/synthetic_ledger.jsonl | 2,031 | 81d8276e4e0e4c11dff029d9b43a031ed389870e79f0ae60a4b585c816d4dce4 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/frozen_cases/honest_mismatch/synthetic_ledger.jsonl` |
| 206 | resume_attack/probe_resume_independent.py | 17,381 | 83622e5a83bd0de7c97d4a368c0b3fe66ce4fb08def54fabe0a0bd80d79fa014 | 뺌 | 주소 꼴 = 사용자@호스트 (합성 git 신원) → 이름 · sha256 만 · 우리 실행 사본 sha256 같음 (`_repro_ours_20261109/build_record.json`) |
| 207 | resume_attack/results.json | 19,675 | 835eead1bcea97c7cc2df7ece1048e325b007f3ea049a804aa3af734d8485db0 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/resume_attack/results.json` |
| 208 | resume_attack/run.log | 1,789 | c4831b2da5a9a8d72f740f08e26e21097891474495a0ba298af850b31c1f7b72 | 넣음 | 바이트 그대로 |
| 209 | scoped_regression.json | 16,676 | 21a8cba0475a87e1e86266e96b9e400da1f3df80cd4782f214aa3085d954fd38 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261109/scoped_regression.json` |
| 210 | scoped_regression.py | 2,794 | f9f089177815830da5e1867e6240548f3a485d096c6715b917098c49d6f10f4f | 넣음 | 바이트 그대로 |
| 211 | verdict.json | 900 | 6692c65e12de51e83dbcc0962a632735e1bb5dcf0e3d2f27b1918093b2042402 | 넣음 | 바이트 그대로 |
| 212 | verify_bundle.py | 2,388 | 267cb641ec05df9b3475bc8bde56da37ab93c6942666b204cccab2d8a3c78b1b | 넣음 | 바이트 그대로 |
| 213 | verify_remote_binding.py | 1,778 | 17cf2e7f968e1fc87c16c8df5a7a320c1071741b0ad69cfa8a39c450b6cf854b | 넣음 | 바이트 그대로 |
