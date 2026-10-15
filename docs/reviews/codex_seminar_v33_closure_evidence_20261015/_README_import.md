# 반입 기록 — Codex 연구세미나 덱 v3.3 종결 확인 (리뷰 핀 `aac17e11f` · 2026-10-15)

- 판정문 (리포 사본) = `docs/reviews/codex_review_seminar_v33_closure_20261015.md` (묶음 `seminar_closure_v33_20261015/` 의 같은 이름 파일 · 바이트 그대로 · sha256 `cd7dfffc64e2095e417c02f7946beb43ee246dd1d2f13711876513e8423b3676`).
- 판정 = **내용 · 수정 항목 종결 GO** — SEMV32-01–04 (원장 `SEM32-01`–`04`) · `SELF-117` 닫힘 · 새 P1/P2 없음 · Q1–Q7 동의 · 수치 재계산 · 새 런 요구 없음.
  발표 최종 GO 의 조건 = 발표 PC 의 PowerPoint 에서 3 장 (네이티브 수식 8 · 두 줄 출처 아래첨자 · 슬라이드 쇼) 표시 확인 — 1저자 직접 처리 (10-15 추적 닫음).
- 받은 것 = 1저자가 WSL 에서 만든 **미니 묶음** `codex_seminar_v33_closure_review_20261015_mini.zip` · sha256 `2924bfd516f104c4d43ca9854047bdee37f0829c429486768e58a808eb6ad4dc` · 328,538 B · 항목 23.
  원 Codex ZIP `codex_seminar_v33_closure_review_20261015.zip` (128 항목 · 55,093,848 B · sha256 `a1a4b5096d513251ad0c998151db242fe606790809263e1880ede8236def5e4d` = Codex 영수증 `_receipt.json` 의 값 · `crc_ok` · `all_member_hashes_ok`) 에서
  `input/` (우리 ZIP v9 사본) · `baseline/` (v3.2 기준) · `renders/` · 2 MB 넘는 파일 · 덱 · PDF · 그림을 뺀 것 — 원 ZIP 전 항목의 sha256 · 크기 · 넣음 여부 = `_members_original_zip.tsv` (미니를 만든 명령이 쓴 그대로 · keep 21 · drop 107).
- 반입 처리: 새 빈 폴더에 복사 → sha256 → 멤버 목록 (절대 경로 · `..` · 링크 0) → 풀기 → **묶음 안 스크립트 (`prepare_inputs.py` · `package_review.py` · `figure_package_probe.py` · `agents/*_probe.*` · `agents/visual_*.py`) 는 실행하지 않았다** (글로만 보존).
- `_members_mini.tsv` = 미니 묶음 23 항목 전부의 sha256 · 크기 · 처리 (`keep` 20 · `verdict` 1 · `meta` 2).
- ★ **리뷰 핀 기록** (판정문 §2 — ZIP v9 의 `PIN.txt` 에 최종 커밋 대신 설명과 base `db04a2a7a` 만 있었고, *"리포에 판정문을 반입할 때 실제 커밋을 기록해야 한다"*):
  리뷰 핀 = `aac17e11f` (요청서가 든 첫 본 가지 커밋 · 요청서 머리 줄).  우리 쪽 대조 (원 ZIP 목록의 sha256 ↔ `git show`): `input/repo/` 사본 19 + `input/` 요청서 = 그 핀의 blob 과 같음 **20/20** · `baseline/` v3.2 판정문 = 리포 `docs/reviews/codex_review_seminar_v32_recheck_20261015.md` 와 같음.
  제출 파일 해시 (판정문 §2 표): v3.3 PPTX `e787298e…` · PDF `706d6a1d…` = 요청서 §6 의 값 · ZIP v9 `2a95d16468b6ec6bb43f6b98d0c9ea21fcb025a4a22102953680e7473f278ba0` (ZIP 해시는 리포에 따로 적힌 적이 없다 — 이 값이 기록).
- 판정문 · 노트의 상대 경로 (`evidence/…` · `agents/…` · `input/` · `baseline/` · `renders/`) = **묶음 루트 (`seminar_closure_v33_20261015/`) 기준** — 리포에서는 이 폴더가 그 루트다 (`input/` · `baseline/` · `renders/` 는 위대로 뺐다).
  참조 검사 예외 = `docs/reviews/doc_refs_allowlist.tsv` 일곱 줄 (뺀 `agents/visual_geometry.json` 포함 · 해시 = `_members_original_zip.tsv`) · `docs/reviews/doc_refs_sha_exceptions.tsv` 한 줄 (`agents/equations.md` 의 LIGGGHTS-PUBLIC 공개 소스 핀 = 다른 저장소).
- 원장: `SEM32-01`–`04` · `SELF-117` → verified (verified_sha `aac17e11f` · 범위 = 연구세미나 발표물 내용 · 모델 검증 · 보류 실험 승인 아님).
