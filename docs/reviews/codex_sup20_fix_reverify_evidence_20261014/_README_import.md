# 반입 기록 — Codex 보충 20 수정 재검증 (2026-10-14)

- 판정문 = `docs/reviews/codex_review_sup20_fix_reverify_20261014.md` (묶음 안 원본 바이트 그대로) · 리뷰 핀 `a9422d2e7` · 기준 `b429c3c1d`.
- 원 ZIP = Codex 작업 공간 `codex_sup20_fix_reverify_20261014.zip` (1저자 PC) — 원 ZIP sha256 은 받지 못했다 [미확인].
  1저자가 slim 으로 다시 묶어 올림: `codex_sup20_fix_reverify_20261014_slim.zip` (963,848 B · sha256 `c6ed97ec661c64c5f7bd4497fb8f5b6904156dc3e1d064835852d5d5a79f88e0`).
- 묶음표 `_members.tsv` (원 ZIP 전 멤버 1,134 = 남김 80 + 뺀 것 1,054 · sha256 · 크기 · keep/drop) 를 이 폴더에 둔다.
- 뺀 것 (slim 단계): `source/` 1,053 파일 = 리뷰 핀 `a9422d2e7` 의 git blob 과 sha256 · 크기 **1,053 / 1,053 같음** (반입 때 `git cat-file --batch` 로 대조) · `tree.json` 3,569,249 B (2 MB 초과 · Codex 쪽 파일 목록).
- 리포에 넣지 않은 것: `baseline/` 4 파일 = 기준 `b429c3c1d` 의 같은 경로 blob 과 같음 · `submitted/request.md` = 리포 HEAD · `339e2226d` 의 `docs/reviews/codex_sup20_fix_reverify_request_20261012.md` 와 같음 (핀 `a9422d2e7` 판과는 리뷰 핀 고정 문구만 다름).
- 판정문의 상대 경로 (`source/` · `evidence/` · `probes/`) 는 Codex 묶음 기준이다.

## 우리 트리 재현 (10-14 · HEAD — 리뷰 대상 스크립트는 핀과 같음: `git diff a9422d2e7 HEAD` 0 줄)

`python3 scripts/supp20_input_receipt.py --dry-run-log <이 폴더>/evidence/receipt_extra/<로그>` — 결과 원문 = `_repro_ours_20261014/<로그>.receipt.txt`.

| 로그 (Codex 생산) | 우리 rc | 뜻 |
|---|---|---|
| `wrong_tsv_full_log.log` (같은 20 ID · raw 표 · 다른 코호트 TSV) | 0 | `SUPR-01` 재현 (오수용) |
| `observation_off_truncated_before_stop.log` (관측 OFF 거부 로그를 중단 사유 앞에서 자름) | 0 | `SUPR-02` 재현 (오수용) |
| `missing_three_prerequisite_lines.log` (필수 검사 줄 셋 삭제) | 0 | `SUPR-02` 재현 (오수용) |
| `observation_off_full_log.log` (관측 OFF 전체 로그 · 대조) | 1 | 대조 = Codex 와 같음 |
