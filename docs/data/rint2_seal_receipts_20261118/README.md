# Rint ② 봉인 관문 영수증 (20261118 · 봉인 커밋에서 잰 것 · 결과 0 건 · σ 열람 0)

- **봉인 커밋** = `29643188524f4fe31f81db5eb252edaa8cbbef7c` (가지 claude/rint2-seal-20261118 · 부모 = 코드 핀 `64e4d213e` · 나무 d92f0c8dacc5b4c9c6772b7b589673af826a4734 · 서명 ssh 서명 (gpgsig 머리 있음 · 이 컨테이너에는 allowedSigners 파일이 없어 %G? = N) · 2026-11-18 00:01:18 +0900) — Codex 2/2 판정문 (`docs/reviews/codex_review_rint2_seal_round2_20261117.md`) §7-2 "필요한 봉인 관문 = 실제 그 커밋의 영수증" 의 기록.  이 커밋 안에 둘 수 없어 (커밋 sha 가 바뀐다) stoic 에 둔다.
- 잰 곳 = 봉인 커밋을 뗀 작업 트리 (깨끗 · 이 세션 · Linux · Python 3.11.18) · 원격 추적 ref = 그때 본 리포 판.  리포 쓰기 0.

## 가. 가벼운 관문 (`seal_receipts.sh` · 이 폴더의 r*.txt)

| # | 무엇 | 결과 | 파일 |
|---|---|---|---|
| ⓪ | 신원 — 봉인 파일 다섯 sha256 · 커밋 줄 | 계획 d8595a52… · 봉인본 bcc0c118… · 명령 문서 eda9d541… · 원본 자리 dcdd1d37… · 봉인 기록 README | `receipts/r0_identity.txt` |
| ③ | sh 사슬 명령 인자 대조 (`check_sh_commands.py` · 기대 셈 봉인본 13 + 1 · kgy 14 + 1) | 문제 없음 · rc 0 | `receipts/r3_sh_commands.txt` |
| ④ | `--stage plan-doc --check-doc` | 봉인본 = `PLAN_DOC_SAME` rc 0 · 기본 (원본 자리) = `PLAN_DOC_MISMATCH` rc 3 (기대대로) | `receipts/r4_plan_doc.txt` |
| ④′ | 사슬 함수 (final 꼴) | 봉인본 해시 줄 둘 = 계획 · S0 sha256 · 원본 자리 = `PLAN_HASH_UNREGISTERED` · `S0_PLAN_HASH_UNREGISTERED` · `require_plan_numbers` 통과 · 결과 final OK | `receipts/r4b_chain_functions.txt` |
| ⑤ | S0 단계 2 관문 `ca_s0_census.verify_plan_commit` (이 커밋 · `--r-doc` 꼴) | 봉인본 → 통과 (S0 sha256 6346d9ed… · R 계획 결합 d8595a52…) · 기본 (원본 자리) → 거부 · 기대대로 | `receipts/r5_s0_stage2_gate.txt` |
| ⑥ | 철회값 등록부 (바뀐 파일 60 · 등록부 42 패턴) | 문제 0 · rc 0 | `receipts/r6_ban_new_text.txt` |
| ⑦ | 규율 검사 (핀 판 `scripts/check_method_discipline.py`) | 0 오류 (경고 17) · rc 0 | `receipts/r7_check_method_discipline.txt` |
| 참조 | `scripts/check_doc_refs.py` (원격 추적 ref = 그때 본 리포 판) | 깨진 참조 없음 · rc 0 | `receipts/r9_check_doc_refs.txt` |
| 경계 | 다섯 경로 · CODE_FILES 20 · S0 일곱 · 규율 검사 입력 | 바뀐 파일 60 (새 56 · 고침 4 · 지움 0) · 다섯 경로 같음 · 안쪽 바뀜 없음 · 규율 입력 안 = `docs/reviews/claims.json` 하나 (stoic 2da71fe5a 판 바이트) · rc 0 | `receipts/r10_seal_files.txt` |
| 도구 | `make_sealed_copy.py --selftest` | 35/35 PASS | `receipts/r11_make_sealed_copy_selftest.txt` |
| 다시 만들기 | 핀 원본 + 이 커밋의 조각 · 계획 · S0 계획 → `--final` | 출력 넷 + 목록 = 이 커밋 바이트와 같음 | `receipts/r12_rebuild.txt` |

## 나. 게이트 (봉인 커밋 · 핀 판 `scripts/check_all.sh` · 같은 HEAD · 깨끗한 트리)

- **세 조각 = 188 단계 실패 0** — 1–120 120/120 · 121–138 18/18 · 139–188 50/50 · 같은 HEAD (봉인 커밋) · 깨끗한 트리 · 머리 줄 · 요약 = `gate/seal_gate_parts.txt` · 단계 시간 = `gate/seal_gate_p1_times.tsv` · `gate/seal_gate_p2_times.tsv` · `gate/seal_gate_p3_times.tsv`.
- 예행 (같은 나무의 scratch 시험 커밋 · 판정에 쓰지 않음) = 1–120 120/120 · 121–138 18/18 실패 0 (11-17 밤).
- ⚠ 첫 진짜 1–120 = 작업 컨테이너 재시작으로 2 단계에서 끊김 → 다시 띄운 첫 판 = **디스크 가득** (/ 99 % · 687 MB 남음) 으로 113 · 119 · 120 실패 (저장본 쓰기 `built_write_skipped` · 봉인 내용 무관) → litdb 정본 작업 트리 둘 (깨끗 · 원격 안) · /tmp 시험 찌꺼기 정리 (12 GB) 뒤 다시 = 통과 · 기록 = `gate/seal_gate_p1_first_rerun_disk_full.txt`.
- push = 2026-11-18 03:55 KST (origin/claude/rint2-seal-20261118 = 봉인 커밋 · 새 가지 · 1저자 11-17 허락).

## 다. 사다리 점 상한 16 시간 예산 (Codex 2/2 §7-1 · 3 판 모형 그대로)

- 원자료 = `budget16/` — 모형 사본 (`time_budget_v3_stoic.py` = stoic `b3481336c` 판 blob 5289b602…) · 12 · 13 · 16 점 출력 JSON (12 점 = 3 판 리포 JSON 과 바이트 같음) · 비교 스크립트 · 읽은 것 = 봉인 기록 README §라 (봉인 가지).
- 요점 — 16 점이면 늦은 기계 사다리 +7.4 h · 주 GPU 끝 191.6 – 216.1 h (12-05 24:00 여유 167.9 – 192.4 h · 시작 11-20 가정) · 대체 꼴 kgy 한 대 33.4 h · 넘침 하나 41.4 h · ⚠ 민감도 "DBE 비 두 배" 높은 끝 = 여유 5.9 → −1.6 h (16 점을 다 쓰고 DBE 비가 두 배일 때만) · 추정.

## 라. 한정

- 이 영수증 = 봉인 꼴 · 결속 · 경계의 확인이다 — 현장 자격 (두 기계 수령 · venv · GPU · 드라이버 · 조립 같음) · S0 단계 2 · R 실행 승인은 닫지 않는다 (1저자 · 따로 · 판정문 §7 "봉인 뒤 실제 실행 전 별도 조건").
- 완료 보장 아님 · RCA-11 = 이 R 의 입력 · 선택 고정만 한정 종결 · env_unit ≠ 전체 실행 환경 (봉인본 머리 절 한정 ① ② ③).
