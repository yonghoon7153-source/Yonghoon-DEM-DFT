# 반입 기록 — Codex Rint G2 ①′ 구현 · 10-13 묶음 재검토 (2026-10-14)

- 판정문 = `docs/reviews/codex_review_rint_g2_impl_20261014.md` (묶음 안 원본 바이트 그대로 · sha256 `430a78413997332fc2d09abad2c5539afad64c8ee516c682347391f2753cf434`) · 검토 핀 `1087a9b2f` (Codex 가 브랜치 끝을 두 번 조회해 고정 · 트리 `f4784d3d…`).
- 요청서 = `docs/reviews/codex_rint_g2_impl_recheck_request_20261013.md` (리뷰 핀 `b74f31407` 로 작성 · 1저자 발송 · Codex 는 그 뒤 최신 끝 `1087a9b2f` 로 고정 — 그 사이 Rint 파일 변경 없음).
- 원 ZIP = Codex 작업 공간 `codex_rint_g2_impl_review_1087a9b2f_20261014.zip` (1저자 PC) — 원 ZIP sha256 은 받지 못했다 [미확인].
  1저자가 미니 ZIP 으로 다시 묶어 올림: `codex_rint_g2_impl_mini_20261014.zip` (348,819 B · sha256 `8539962b0e0803ed5fc2fde73e375ce519e25f44a3d9e92ed7d3f3a0107ddf51` · 원 ZIP 멤버 815 전부의 sha256 · 크기 목록).
- `_members.tsv` 열 = sha256 · 크기 · 상태 · 원 경로.  상태 = `keep` (이 폴더에 그대로 43) · `verdict` (판정문 자리로 1) · `drop` (넣지 않음 771).
- 넣지 않은 것 (`drop`):
  - `source/` 769 파일 = 검토 핀 `1087a9b2f` 의 git blob 과 sha256 **769 / 769 같음** (반입 때 `git show` 로 대조).
  - 묶음의 source_prior 폴더 step3_sigma.py (275,510 B) = git blob `4b33c7a4…` — ①′ 구현 전 판 (`1d9af09d0` 계열 · 수치 OFF 호환 대조의 옛 코드).
  - 묶음의 evidence 폴더 tree.json (3,129,211 B · GitHub tree 응답 · 미니 ZIP 상한 2 MB 초과).
- 묶음 안 스크립트 (`probes/` · `package_review.py` · `prepare_source.py` · `run_review_tests.py` · `verify_evidence.py`) 는 **실행하지 않았다** (반입 규칙 — 읽기만).
- 판정문 · `README.md` · `notes/` 의 상대 경로 (`source/` · `evidence/` · `probes/`) 는 Codex 묶음 루트 기준이다.

## 판정 요지 (원장에 옮긴 것)

- `RINTV-01` · `RINTV-02` = verified (범위 = 판정문 §8-1 · 원장 `verified_scope` — 고정 입력의 소유권 규칙 · raw 진단 ↔ 불변성 판정의 분리.  T3 정확도 · 생산 대표성은 포함하지 않는다).
- 새 결함 (open): `RIMP-01` (P2 · 기울어진 MMS 경계 반 셀이 계면 저항을 건너뜀) · `RIMP-02` (P2 · 조인 관문이 손상 · 미인증 입력을 PASS) · `RIMP-03` (P2 · 면적 포괄에 기록 유효숫자 S 미전달) ·
  `RIMP-04` (P2 · RRM N9 의미 검사기가 메타데이터 변경 · NaN 을 놓침) · `RIMP-05` (P2 · 계획의 격자 간격이 솔버 인자에 봉인되지 않음 — 막 전도도 기록의 4 배 반례) · `RIMP-06` (P3 · RRM 반환 기록에 CNC 수치가 라벨 없이 남음).
- ①′ 정량 채택 · 생산 = **HOLD 유지** · 제공 시험 229 개 + 두 자체시험 통과 (Windows — T4 두 시험은 최대 메모리 기록 어댑터로 재실행 · 원 실패 로그 동봉).
- 수정 계획 = `docs/reviews/rint_g2_impl_fix_plan_20261014.md` (Q1–Q6 · 1저자 비준 대기).
