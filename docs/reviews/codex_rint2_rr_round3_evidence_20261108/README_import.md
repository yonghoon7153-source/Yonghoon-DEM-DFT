# Codex Rint ② 재검토 회차 ③ (11-08) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rr_round3_20261108.md` — ZIP 원본 23,532 B · sha256 098266a25ef7fb62215db130582d094fb546785bfa6b934f5da608d047819f2d · CR 0 개 → 리포 사본 = 원본과 바이트 같음 (리포 `.gitattributes` 의 md = LF 규칙에도 바뀌지 않는다).
- 리뷰 핀 = `17d45fb9cdfc7033bdfd41509527cea23ba1654c` (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · tree 6989fd20dca6fba46fcf5eb6955dc8e9f12f2586 = 판정문 §1 의 원격 고정 tree) · 비교 기준 = `6917c3c9f` (회차 ② 리뷰 핀) · 요청서 = `docs/reviews/codex_rint2_rr_round3_request_20261108.md` (Q1–Q6 · 핀 → 이 반입 바탕 `f5fb89792` 사이 요청서 · `scripts/rint_r_chain.py` 변경 없음 = `git diff --stat` 빈 출력).
- 우리가 보낸 ZIP = codex_rint2_rr_round3_17d45fb9cdfc.zip · 6,043,906 B · sha256 b11412c0741fc9151e661d88d225644f699f385c2d61d5e7f751e0614bcaa37e (판정문 §1 · `integrity.json` 기록값 = 진행 기록 11-08 발송 줄 · 이 반입에서 다시 재지 않음).
- 받은 ZIP = `3bd430cb-codex_rint2_rr_round3_independent_review_17d45fb9cdfc_20261108.zip` · 6,331,734 B · sha256 ff57f37aa1869c07be52a0b4a7fc1c654603e9c906607d8563b27d088e2f1756 · 736 항목 = package/ 662 · 머리 24 · contracts_p2p4_git_evidence/ 13 · pc12_attack/ 10 · preattack12_replay/ 8 · round2_replay/ 7 · s0_memory/ 12 (리포 밖 빈 폴더에 `python3 -I` 로 풂 · 절대 경로 · `..` · 심볼릭 링크 0).
- Codex 매니페스트 `docs/reviews/codex_rint2_rr_round3_evidence_20261108/EVIDENCE_MANIFEST.sha256` (735 줄 · 자기 빼고 전부) ↔ 받은 파일 = 다름 0 · 매니페스트에 없는 파일 0 (자기 뺌) · 빠진 파일 0 (우리 대조 스크립트 · ZIP 안 `verify_evidence.py` 는 돌리지 않았다).
- package/ = 우리가 보낸 ZIP 의 다시 묶음 → **리포에 안 넣음**: PIN.txt (78 B · sha256 e9c099199ba3cfab5dd470c92c63f1642c44a0c1110c182f0d3cdeaf25b25cc6 · 핀 40 자리 + 가지 이름) · SHA256SUMS (661 줄 · 101,282 B · sha256 aa502f09e3f4dd18134fdcea1f00636a5d806ef5e4b6c20b6d242aac67592ab4 · 우리 대조 다름 0) · repo/ 660 = **우리 대조 660 / 660 같음** (전수 · 파일마다 git blob id · 크기 ↔ `git ls-tree -r -l 17d45fb9c` · 핀 tree 밖 경로 0) · Codex 기록도 660 / 660 (판정문 §1 · `integrity.json`).
- 넣은 것 = **55 파일** (이 폴더 · ZIP 과 같은 상대 경로 · 바이트 그대로 · 리포 `.gitattributes` 의 증거 폴더 규칙 = `-text` 라 CRLF 그대로 남는다) — 머리 19 + contracts_p2p4_git_evidence/ 12 + pc12_attack/ 7 + preattack12_replay/ 4 + round2_replay/ 5 + s0_memory/ 8.  판정문 1 = 판정문 자리.
- 뺀 것 = **680** — package/ 662 + 주소 꼴 16 (Windows 사용자 폴더 경로 15 · 사용자@호스트 꼴 1 = 합성 git 신원 · 실제 주소는 아니나 주소 꼴은 리포에 안 넣음 · 이번 반입 지시) + 우리 git blob 사본 2 (remote_old_carbon_3b12fbe2d.py = `git show 3b12fbe2d:scripts/carbon_junction.py` · remote_old_census_39104710a.py = `git show 39104710a:scripts/ca_s0_census.py` · sha256 같음 = 5460dad1… · 6e527e6c… · 리포 기록에 이미 있음) — 이름 · 바이트 · sha256 = 아래 전수 표.
- 주소 꼴 검사 (우리 스크립트 · non-package 74 · 패턴 = IPv4 · 사용자@호스트 · `-P` 포트 · 드라이브 문자 + Users 경로 · /mnt/<드라이브>/Users · 계정 이름 · 컴퓨터 이름 꼴) — 걸린 21 = 뺌 16 + 오탐 5 (넣음 4 = `s0_memory/probe_s0_memory.py` 행렬곱 연산자 · `s0_memory/REVIEW_Q5.md` 파일·커밋 표기 · `replay_preattack12.py` 컨테이너 리포 경로 · `REPRODUCE.md` 드라이브 자리 표시 경로 (Users 없음) / 다른 까닭으로 뺌 1 = remote_old_carbon_3b12fbe2d.py 변수 이름) · 반입 뒤 이 폴더 다시 검사 = 걸림은 위 오탐 넷뿐 (Windows 사용자 경로 0 · 사용자@호스트 주소 0).
- 이 폴더 = 넣은 55 + `_repro_ours_20261108/` 54 (우리 산출 51 + README.md · build_record.json · comparison.json) + 이 README · `SHA256SUMS` = 이 폴더 파일 전부 (자기 빼고 · 110 줄 · `sha256sum -c` 꼴).
- 반입 때 ZIP 안 스크립트는 리포 안에서도 받은 폴더에서도 실행하지 않았다 — 탐침 7 개는 다 읽은 뒤 리포 밖 스크래치 실행 폴더에 복사해 (sha256 = 원본과 같음) 우리 핀 작업 트리에 대고 돌렸다 → `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/README.md`.
- 환경 (Codex · 판정문 §1) = Windows · Python 3.12.14 (NumPy 2.5.3 · SciPy 1.16.3 = S0 결과 JSON) · 고정 소스 + 작은 합성 입력 · O_NONBLOCK 0 대체 = 일반 임시 파일 시험만 · 옛 Git 탐침 재생 = 가짜 /proc · 호스트 · 단일 스레드 잠금 대체 · 실제 Linux FIFO · 신호 · PID · flock · NFS · GPU · kgy 자격 시험 아님 · 작성 측 Python 3.8.20 / 3.11 기록 = 수령 근거 (독립 실행 횟수 아님) · 실제 호스트 · S0 실침대 · R 런 · 등록 · 배포 · 통합 · 원장 변경 · 전체 공유 게이트 = 하지 않음.

## 판정 요약 (판정문 머리 · §2 · §3 · §4 · §5 · §6 · §7 줄임)

| 범위 | 판정 |
|---|---|
| 전체 | **HOLD** — 지정 수정 대부분 수용 · PC12-03 부분 · SELF-155 부분 · 재개 정책을 포함한 일괄 GO 불가 · "닫힘" = 지정 반례 · 최소 해결 범위 한정 (실제 환경 자격 · 생산 GO 아님) · 이전 verified 35 전수 재심 안 함 |
| 새 finding | P1 0 · P2 1 (`RR3-01` 검사 실패 때 보존한 파일 해시 목록을 앞 런 판독 완료로 오인 · `scripts/rint_r_chain.py` 4168–4175 · 4993–4995 · 2131–2141 · 4356–4359 · 3418–3424 · 5076–5079 = 핀 줄) · P3 1 (`RR3-02` 회차 ③ 요청서 한정표 83–86 줄 · 대조 93–94 줄 · §5-3 에 PC12 이전 설명이 현재형으로 남음) |
| §3 닫힘 30 | RR2-01 · 02 · 03 · PC6-05 · PC6-13 · PC9-01–07 · PC10-01–10 · PC11-01–04 · PC12-01 · 02 · 04 · 05 (원장 verified_scope = §3 그 행 그대로 + 머리 한정) |
| §3 부분 2 | PC12-03 (옛 rc 실패 / 빈 목록 반례는 차단 · 남은 부류 = RR3-01 · 봉인 전 보완) · SELF-155 (후보 검색 · CP-ORD · 두 예외 · 새 계획 SHA = 합성 범위 수용 · 실침대 메모리 · 시간 · 종료 · 완성 산출물 미확인) |
| 이번 답으로 닫지 않음 | PC9-08 wontfix · PC11-05–08 open · SELF-158 · PC6-03 · 06 · PC7-06 · 07 · RINT2-T01 · L01 |
| §4 Q2 · Q3 | 정책 원칙 (생산자 꼴 표 · 모순 거부) 수용 · 이번 코드가 그 원칙을 완결했다는 판단은 반대 (RR3-01) · 옛 탐침 기대 변경 8 + §4 ①–④ 범위 변경 수용 (② 목표는 맞고 구현의 충분조건이 틀림) · Codex 독립 실행 = 301 / 309 같음 · 8 변경 · 역사 파일 검사 2 미실행 (작성 측 303 / 311 을 옮기지 않음) · 원 p2 / p4 최소 실제 Git 12 / 12 |
| §5 Q4 봉인 전 | ① RR3-01 보완 ② RR3-02 정정 ③ PC11-05–08 · PC12 한정은 자동 격상 안 함 — 단 최종 계획 · 시도 기록이 미검증 영역 (요청 칸 · 유일 런 이름 · 실제 순서 · launch/end 결합 · 필요한 chain_end · 복사 출처) 을 쓰지 않는지 봉인 전 확인에 넣음 · 결손을 구형 예외로 흡수하고 일반 정책 GO 주장 금지 ④ 현장 자격 · 원인 미확정 최초 실패 기록 · 검토 핀 → 봉인 핀 diff · 의존 지문 = 그대로 |
| §6 Q5 | 두 예외 · CP-ORD 이동 · 새 계획 SHA 수용 · kgy "rc 0 + 여섯 파일" = 필요한 완료 점검이지 채택 충분조건 아님 → 자식 rc (`docs/reviews/rint2_s0_mem_fix_20261106/tools/run2.sh` 15 줄 = rss.log 의 rc) · 여섯 산출물 실제 읽기 + 같은 실행 결속 · 새 빈 폴더 · SBE 한 침대 · σ 비열람 · 무쓰기 · 실패 보존 · 환경 · 종료 · 시간 · "표본 최대 RSS" · 순서 그대로 · kgy 실행 승인 · 실측 성공 인증 아님 |
| §7 Q6 | "코드 · 설계 · 문서 GO (재개 정책 포함) + 봉인 전 확인" = 이 핀에 쓸 수 없음 · 순서 = S0 단계1 → s_min → ⑥ → 기하 · 반복 수 → 숫자 · 실행 정책 → 새 계획 / 핀 봉인 → S0 단계2 → 등록 R 진입 판단 · 이번 회신으로 쓸 수 있는 문장 = 판정문 §7 인용 그대로 |

## 원장 변경 (이 반입 커밋 · `docs/reviews/findings.json`)

| 무엇 | 항목 |
|---|---|
| claimed_fixed → **verified** 30 (verified_by codex · verified_sha `17d45fb9c` · verified_in = 판정문 · verified_scope = §3 그 행 + 머리 한정 · claimed_fixed_sha · evidence_tests 그대로) | RR2-01 · RR2-02 · RR2-03 · PC6-05 · PC6-13 · PC9-01 · 02 · 03 · 04 · 05 · 06 · 07 · PC10-01 · 02 · 03 · 04 · 05 · 06 · 07 · 08 · 09 · 10 · PC11-01 · 02 · 03 · 04 · PC12-01 · 02 · 04 · 05 |
| 부분 — 상태 그대로 (claimed_fixed) · note 에 남는 범위 (회차 ② 반입 관례 = 부분은 상태 그대로 · 남은 분기는 새 항목 — PC6-13 ↔ RR2-01) | PC12-03 (남은 부류 = RR3-01) · SELF-155 (남은 것 = kgy S0 단계 1 실침대 재실행 · 채택 조건 = 판정문 §6) |
| open 그대로 · note 에 판정문 답 | PC11-05 · 06 · 07 · 08 (§5 ③ = 자동 격상 안 함 · 봉인 전 확인 항목) |
| 새 open 2 | RR3-01 (P2) · RR3-02 (P3) |
| 원장 수 | 1015 → 1017 · open 341 → 343 · claimed_fixed 381 → 351 · verified 282 → 312 · wontfix 11 그대로 |

⚠ verified_sha = 회차 ② 반입과 같은 9 자리 꼴 (`17d45fb9c` = 리뷰 핀 `17d45fb9cdfc7033bdfd41509527cea23ba1654c`) · verified_by = 정본 actor `codex` · "codex 11-08 Rint ② 재검토 회차 ③ (리뷰 핀 17d45fb9c)" 표지 = verified_scope 머리.

수정 계획 (결과 0 건 · 1저자 비준 대기) = `docs/reviews/rint2_rr3_fix_plan_20261108.md`.

## 우리 트리 재현

→ `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/README.md` — 탐침 7 개 rc = Codex 와 같음 (6 개 rc 0 · 옛 탐침 rc 1 = 301 / 309 기록 그대로) · **판정값 차이 0** (RR3-01 표 · PC12 요청 255 / 21 · 끝 기록 175 행 · contracts 105 / 105 · 원 p2 / p4 Git 12 / 12 · S0 575 / 575 · 55 / 55 · 19 / 19 · 계획 결속 18 / 18 잎 · 옛 탐침 301 / 309 · 판정에 닿지 않는 차이 = 환경 판 · 시각 · 경로 글 · 폴더 지문 · fixture 커밋 번호 · Windows CRLF 합성 팔 파일 · Codex 첫 실행 옛 모듈 사본의 끝 LF).

## 뺀 파일의 내용 (요지 · 우리 재현 판)

뺀 파일 이름 = 받은 ZIP 안 이름 (리포 경로 아님 · 따옴표 없이 적음).

- pc12_attack/REVIEW.md — PC11 / PC12 하위 보고 · 결론 = 판정문 §2 RR3-01 · §3 PC11 / 12 행과 같음 · 판정문에 없는 보조 관측 둘: (a) 그룹 기록 판독 (`scripts/rint_r_chain.py` 3738 `_read_group_json`) 은 아직 일반 `json.loads` — PC12-04 엄격 JSON = 단계 요약 한정 (이 관측만으로 P2 를 만들지 않음) · (b) Q4 한정 = 끝 기록 결합 부재 · 요청 칸 부재 · 런 이름 중복 / 순서 미검사 · 임의 UTC / 다른 칸 · 지수 넘침 수 · 풀기 전 전용 STOPS 목록 미열거 (새 결함으로 격상 안 함 · 봉인 전 확인 대상) → 수정 계획 §4.
- pc12_attack/counterexample_original_ledger.jsonl · pc12_attack/counterexample_edited_ledger.jsonl · contracts_p2p4_git_evidence/results.json · round2_replay/residual_rc_integration.json · s0_memory/targeted_memory_summary.json — 우리 재현 판 = `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/` 의 같은 상대 자리 (잎 대조 = `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/comparison.json`).
- contracts_p2p4_git.py = 탐침 (우리 실행 사본 sha256 = 원본과 같음 · `docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/build_record.json`) · round2_replay/probe_runtime.py = `docs/reviews/codex_rint2_rr_round3_evidence_20261108/run_old_probe.py` 가 만드는 적응 사본 (우리 실행이 다시 만듦 · sha256 다름 = REPO 경로 글 · Windows 에서만 넣는 한 줄 · comparison.json 의 adaptation 행) · preattack12_replay/harness_adapted.py = 다시 만들지 않음 (replay_preattack12.py 안 돌림).
- 첫 실행 실패 보존 기록 (판정문 §8 이 공개한 실패 · 제품 결함으로도 후속 PASS 로도 세지 않음) — preattack12_replay/p2_real_ledger.py.log · preattack12_replay/p4_tl_none_after_fail.py.log (Windows symlink 권한 중단) · preattack12_replay/p5_misc_b.py.log (원 p5 의 None 첨자 TypeError) · s0_memory/targeted_memory_first_temp_permission.log · s0_memory/targeted_memory_first_temp_permission_summary.json · s0_memory/targeted_s0_memory_first_temp_permission.log (시스템 임시 폴더 권한) · old_probe_first_attempt_missing_historical.log (역사 report_c 파일 없음).

## 항목 전수 (736 · package/repo/ 660 = 한 줄로 묶음 · 처분 = 넣음 · 판정문 자리 · 뺌)

"넣음" = 이 폴더의 같은 상대 경로에 바이트 그대로.

| # | ZIP 항목 | 바이트 | sha256 | 처분 | 까닭 · 대조 |
|---:|---|---:|---|---|---|
| 1 | EVIDENCE_MANIFEST.sha256 | 114,721 | 0aaabac515f53d19134997150346b3a418d2f72839894e4d57f94ff2a8fdb3dc | 넣음 | 바이트 그대로 |
| 2 | REPRODUCE.md | 5,167 | 0693e39fac114cd91b62c5ee3547fee2f028c1c4cf3a204fb6546cfacb48fa54 | 넣음 | 바이트 그대로 |
| 3 | codex_review_rint2_rr_round3_20261108.md | 23,532 | 098266a25ef7fb62215db130582d094fb546785bfa6b934f5da608d047819f2d | 판정문 자리 | `docs/reviews/codex_review_rint2_rr_round3_20261108.md` · 바이트 같음 (CR 없음) |
| 4 | contracts_p2p4_git.py | 7,712 | 04401e10fab6c5223c8db10c2e4d11604235f5580df588189b54f474c5aac70b | 뺌 | 주소 꼴 = 사용자@호스트 (합성 git 신원) → 이름 · sha256 만 · 우리 실행 사본 sha256 같음 (`_repro_ours_20261108/build_record.json`) |
| 5 | contracts_p2p4_git_evidence/p2_1a.log | 101 | 6d5bd7424f13f5fb7757ff0bba13d531808a00c1bfd09cf90ec88bdcc8ddd700 | 넣음 | 바이트 그대로 |
| 6 | contracts_p2p4_git_evidence/p2_1b.log | 101 | 6d5bd7424f13f5fb7757ff0bba13d531808a00c1bfd09cf90ec88bdcc8ddd700 | 넣음 | 바이트 그대로 |
| 7 | contracts_p2p4_git_evidence/p2_1c.log | 101 | 6d5bd7424f13f5fb7757ff0bba13d531808a00c1bfd09cf90ec88bdcc8ddd700 | 넣음 | 바이트 그대로 |
| 8 | contracts_p2p4_git_evidence/p2_2a.log | 102 | 5308e3217ed03c3012c41ab0945db2d3981008668d2fdbb4e47a794fa7834a60 | 넣음 | 바이트 그대로 |
| 9 | contracts_p2p4_git_evidence/p2_2b.log | 110 | 9f595c322ac6b19ca4ec720951d62cb8e047bc7daa19a5ce43c9461db2fc7fc5 | 넣음 | 바이트 그대로 |
| 10 | contracts_p2p4_git_evidence/p2_2c.log | 110 | 9f595c322ac6b19ca4ec720951d62cb8e047bc7daa19a5ce43c9461db2fc7fc5 | 넣음 | 바이트 그대로 |
| 11 | contracts_p2p4_git_evidence/p4_L02.log | 100 | 8ef95f54d91a6534d112d772b78711c4f2a99ddb275aab2431a63fe0aa495679 | 넣음 | 바이트 그대로 |
| 12 | contracts_p2p4_git_evidence/p4_honest.log | 102 | 5308e3217ed03c3012c41ab0945db2d3981008668d2fdbb4e47a794fa7834a60 | 넣음 | 바이트 그대로 |
| 13 | contracts_p2p4_git_evidence/p4_zzz.log | 100 | 8ef95f54d91a6534d112d772b78711c4f2a99ddb275aab2431a63fe0aa495679 | 넣음 | 바이트 그대로 |
| 14 | contracts_p2p4_git_evidence/positive_GU_rc0.log | 109 | 6a7036f9e3cf9a52ec912bef9ca8b7a0b8e676fa50d45aef732043b5f8904318 | 넣음 | 바이트 그대로 |
| 15 | contracts_p2p4_git_evidence/positive_signal.log | 98 | 07f65bc092342677178e9f3673716be8b08e0b9fd9781a1f106e4f0ac2ac055a | 넣음 | 바이트 그대로 |
| 16 | contracts_p2p4_git_evidence/positive_timeout.log | 99 | 96e7e301c56bb09e481d8eb73603a79335a75c9ad9d28f034750795a361ac9f2 | 넣음 | 바이트 그대로 |
| 17 | contracts_p2p4_git_evidence/results.json | 29,047 | 3fe0d2947704f34e68c001ff8a6150cc11c65f6f601824b7f5f41a772820bbb5 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261108/contracts_p2p4_git_evidence/results.json` |
| 18 | contracts_probe.py | 10,741 | c6ca404e92ee35b6d23be6ef884029b441ac0bfe47aab163f6d6ad2a140723c6 | 넣음 | 바이트 그대로 |
| 19 | contracts_probe_results.json | 18,658 | 388dd6c128116164ff9f66062bd92faa045bc595fee57273240912897a70d9cf | 넣음 | 바이트 그대로 |
| 20 | contracts_probe_results_initial_quote_locator_error.json | 16,608 | bfee217c8497f929c3422a7b47205b65c771023238d4e73d8abb05874996a95f | 넣음 | 바이트 그대로 |
| 21 | contracts_review.md | 17,406 | f511af685d43ba067c31f8206ef8c48a89210b5f98f3eb6449e67cf818d83f23 | 넣음 | 바이트 그대로 |
| 22 | final_source_preservation.json | 101 | be7330c491ca16f386023529ba2936f6c588790b433739d41cf0d06165632e65 | 넣음 | 바이트 그대로 |
| 23 | integrity.json | 276,697 | 6364b1211b7c29c10d6894b404628a73dc81bb719986c2663df0038909d983f3 | 넣음 | 바이트 그대로 |
| 24 | old_probe.log | 743 | 788a40d47f07d066afa4338bccbdf441695058c29e956bebf2509d2cd5efb1d9 | 넣음 | 바이트 그대로 |
| 25 | old_probe_first_attempt_missing_historical.log | 1,776 | 8e30e2de0d19f1e3b69be329d07cb833260b210c75a7c35aea9d4578233cc6ba | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 26 | package/PIN.txt | 78 | e9c099199ba3cfab5dd470c92c63f1642c44a0c1110c182f0d3cdeaf25b25cc6 | 뺌 | 우리가 보낸 ZIP 의 PIN.txt (핀 40 자리 + 가지 이름) |
| 27 | package/SHA256SUMS | 101,282 | aa502f09e3f4dd18134fdcea1f00636a5d806ef5e4b6c20b6d242aac67592ab4 | 뺌 | 우리가 보낸 ZIP 의 SHA256SUMS (661 줄 · 우리 대조 다름 0) |
| 28 | package/repo/ | 20,321,199 | (파일마다 · 매니페스트) | 뺌 | 660 파일 = 우리 핀 `17d45fb9c` blob · 크기 660 / 660 같음 (`git ls-tree -r -l` 대조) · 파일별 sha256 = `EVIDENCE_MANIFEST.sha256` |
| 29 | package_evidence.py | 2,298 | 027421ad9cd46f54417dd25068a1b8731d0fc660ee7f23dda24422cbf92d27a0 | 넣음 | 바이트 그대로 |
| 30 | pc12_attack/REVIEW.md | 8,937 | 3d185e3e8bfcd721cdd4ae1ec7a9d24599d87f149b50f86ff7f335d092edc692 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 31 | pc12_attack/chain_side_rows.json | 64,698 | 8f687d6530081abb194fd9b74292792d9be05e6f981d3b8bf9c74440068afcb4 | 넣음 | 바이트 그대로 |
| 32 | pc12_attack/counterexample_edited_ledger.jsonl | 1,009 | 8e701fc9c8f283783778f650742577b9cecf9c811a6808853bc97ba76eb6ad69 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261108/pc12_attack/counterexample_edited_ledger.jsonl` |
| 33 | pc12_attack/counterexample_edited_summary.json | 719 | f87169b86e8f1235477197e751b7e846340f2f188d2c6ac1905f79e93b311bcc | 넣음 | 바이트 그대로 |
| 34 | pc12_attack/counterexample_original_ledger.jsonl | 1,010 | 94f52938bbdcb9ffac10b451ca4f5301f32ca4e55903928f40358398cf671f49 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261108/pc12_attack/counterexample_original_ledger.jsonl` |
| 35 | pc12_attack/counterexample_original_summary.json | 721 | b02251263fee425d276c94f493a9fcb2949301ab9c54459174c6280ef4dbf972 | 넣음 | 바이트 그대로 |
| 36 | pc12_attack/parent_reproduction.log | 8,265 | 09b7f740917b22129870c6f55f2eb32c91333d53fe3c7751d5589c4925f81d78 | 넣음 | 바이트 그대로 |
| 37 | pc12_attack/probe_pc12_independent.py | 13,097 | 7f335c758c036c6de5ab10ef5b9ab3d35d6eb10ab3f0182694bdea03914b74d7 | 넣음 | 바이트 그대로 |
| 38 | pc12_attack/results.json | 8,263 | 9b377cf7f63fd85a4852b60efe7a764ae40e91e838db418db0d619248ed156f9 | 넣음 | 바이트 그대로 |
| 39 | pc12_attack/run_stdout.json | 8,265 | 4fd7b3870dfad6f2105387906efb9a13994f6be9b32d9ef2b5d694c2ed7afee5 | 넣음 | 바이트 그대로 |
| 40 | preattack12_first_missing_gitignore.log | 358 | 45574eade6acd119dcc9776afb5bed75c5b8948197308b17bf38d651172503a8 | 넣음 | 바이트 그대로 |
| 41 | preattack12_replay/harness_adapted.py | 1,145 | 2d7511e85f8b0071b0cc86378b3011a92c235f49514fd0de32871d8b5396f7b0 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 42 | preattack12_replay/p1_outdir_coedit.py.log | 2,265 | b212c23cfdf75f4ae250c92beb3e4523c0eec041ccddc23bdf189c501ea89ff2 | 넣음 | 바이트 그대로 |
| 43 | preattack12_replay/p2_real_ledger.py.log | 1,906 | fae3eadac7287d847d353405a74f45e39cb498269d68f9eb5de342c6c2678bdd | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 44 | preattack12_replay/p4_tl_none_after_fail.py.log | 1,913 | ede7a8c3f696387d78ed92776f52c2c535603f97068c4c5a33efa82928ecf8ca | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 45 | preattack12_replay/p5_misc_b.py.log | 1,124 | c9a54179f1395ad55e82084023deebe47149e78ab7872a87d4c4deca645ea542 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 46 | preattack12_replay/p5_none_safe.log | 846 | a4e6b0d35e56f275a3e1e196f48f1a0a92cef7d5dee1d87996455fd2b83cbde5 | 넣음 | 바이트 그대로 |
| 47 | preattack12_replay/p6_rejected.py.log | 1,397 | 861790db4f14c95953835b32896856db0af327a6755e1f7f0ce4cee532610914 | 넣음 | 바이트 그대로 |
| 48 | preattack12_replay/replay_metadata.json | 1,619 | d155bfd8e0fecfe67da4932c5f7fdbd8ac8ef8ac0da5cc28b45f0b4e4915d798 | 넣음 | 바이트 그대로 |
| 49 | preattack12_replay_run.log | 360 | 8d91d1f4d0ea2bde91e8d241415970147856bac4300078958b72ff81d521bca7 | 넣음 | 바이트 그대로 |
| 50 | remote_blob_check.json | 138,985 | 715144f28d5337c2f7010ac8dd6d0d1b58b53983f75e0ebc0677d3e254456ee3 | 넣음 | 바이트 그대로 |
| 51 | remote_dependency_diff.json | 5,576 | bd78bb7fd151d58b477607f244f56be4138d21126f4e7113712b4296b3aca271 | 넣음 | 바이트 그대로 |
| 52 | remote_gitignore | 2,925 | 1fb39d29f01dfc72c0c753526fdf334683cf1c735f00ec3638ad5d0051cb1b69 | 넣음 | 바이트 그대로 |
| 53 | remote_old_carbon_3b12fbe2d.py | 191,737 | 5460dad164839b115eea07f5df21087af1ff214c221e4838d940f7de9f9ca221 | 뺌 | = 우리 git `3b12fbe2d:scripts/carbon_junction.py` (sha256 같음 · 리포 기록에 있음) |
| 54 | remote_old_census_39104710a.py | 111,991 | 6e527e6c7a16251c585443abb922325170975f63d953204d209065c2dc951937 | 뺌 | = 우리 git `39104710a:scripts/ca_s0_census.py` (sha256 같음 · 리포 기록에 있음) |
| 55 | replay_preattack12.py | 4,423 | 6a905ca309bc27367c4343fb07af64c5dec7929ed313d50907581108e3e434d0 | 넣음 | 바이트 그대로 |
| 56 | review_result.json | 6,417 | d669b07c40d129be7dbd5cfee2a8dd161cd79ca6890c26385e5418a7758bb303 | 넣음 | 바이트 그대로 |
| 57 | round2_replay/adaptation.json | 628 | 83aa7280ff5394a1369d9dbe82d9e4c23c55a568d81c9329bcc833ae7cc2688a | 넣음 | 바이트 그대로 |
| 58 | round2_replay/candidate_fix_results.json | 1,225 | b3d05ca4941802baebabb5265251532e173f74c6b7f61683c79567808fbbe646 | 넣음 | 바이트 그대로 |
| 59 | round2_replay/marker_child.py | 271 | f19122be1d5f1b83caf657ae23b1b562eb7aad3e97e2e6cb809beab34cc1eea7 | 넣음 | 바이트 그대로 |
| 60 | round2_replay/probe_runtime.py | 22,846 | 422c875144dc0854e0fa314a26a9db5110ece65861dd6c4bf4d7aba0f25a4448 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 (+ 사용자@호스트 꼴) → 이름 · sha256 만 |
| 61 | round2_replay/residual_rc.json | 1,929 | 8ce4f4fd09537946aa0d49b70b5177e5501666bc945ac7378339737f85404518 | 넣음 | 바이트 그대로 |
| 62 | round2_replay/residual_rc_integration.json | 3,269 | 9eceae5f3f1c3eb81785791a64cc97c375b64db0472494abb93eeb504fee7e9a | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261108/round2_replay/residual_rc_integration.json` |
| 63 | round2_replay/results.json | 46,489 | 1331a3d5255c040fdc3584c5e1b6c90883599982ceb021c0c349bc9ece567355 | 넣음 | 바이트 그대로 |
| 64 | run_old_probe.py | 2,089 | bd2ff652e15b4845f14727468f2a28234bd3b3c4cceb096870f361f5d946bc53 | 넣음 | 바이트 그대로 |
| 65 | s0_memory/REVIEW_Q5.md | 9,160 | 410ee03ace3884ac130dcc1c768c42beac7ba5849841573bc975631515808a0a | 넣음 | 바이트 그대로 |
| 66 | s0_memory/independent_results.json | 72,550 | 91051398ea6c1962a867a697778f2d228b77c78a646effbf131a5f67fa8bf79a | 넣음 | 바이트 그대로 |
| 67 | s0_memory/plan_binding.json | 1,211 | 8c1f98a96b6b961946502900f11479b9b55e12f057be30bdc9714e448ac2ec5d | 넣음 | 바이트 그대로 |
| 68 | s0_memory/probe_plan_binding.py | 1,885 | 914028c9262110caf7be101efde4c6e31fe6a6a156ec325bccee05aa75234197 | 넣음 | 바이트 그대로 |
| 69 | s0_memory/probe_s0_memory.py | 6,018 | 841f3fc1c0683e5bac128e342bd88426e5f0ea89d8859c9be2dc9e30000490ae | 넣음 | 바이트 그대로 |
| 70 | s0_memory/run_targeted_memory.py | 2,777 | 81de5e23cf6fef0c18eff4ab07f6213dcadd3ae74e4f981fe5cee63ceebbd7fd | 넣음 | 바이트 그대로 |
| 71 | s0_memory/targeted_memory.log | 9,300 | 4298f25bd32a0c5579d202b63d546437b4224add5f3390b4b0d33f2dcca2f137 | 넣음 | 바이트 그대로 |
| 72 | s0_memory/targeted_memory_first_temp_permission.log | 9,412 | 0c9b5eb2be1d2f6bc00b403639231c77f78a8d707fa0d7548b95cabc7e247a67 | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 73 | s0_memory/targeted_memory_first_temp_permission_summary.json | 930 | 7328417c4fee367f8d274f65f1e808006d9d84aaadb861a0f82f9745ad09958d | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 74 | s0_memory/targeted_memory_summary.json | 877 | ccb2de07e2bc558bcff8a79173cfd298cb6adba308f0f773657df0969637bfab | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 · 우리 재현 판 = `_repro_ours_20261108/s0_memory/targeted_memory_summary.json` |
| 75 | s0_memory/targeted_s0_memory.log | 2,934 | 7e1339a51510e3b2f510118b5f88e37c94dacf228153d82b027e0637be1c1362 | 넣음 | 바이트 그대로 |
| 76 | s0_memory/targeted_s0_memory_first_temp_permission.log | 3,431 | d6043d1c37d62133ee663abba0513c863d79870788b6a45294cadab6f1908c4d | 뺌 | 주소 꼴 = Windows 사용자 폴더 경로 → 이름 · sha256 만 |
| 77 | verify_evidence.py | 588 | 85fc10a312c88699f45c2d54862751020c3cf45de927c51720a9f92d5b521a9e | 넣음 | 바이트 그대로 |
