# 반입 기록 — Codex SUPR 수정 재확인 (2026-10-14)

- 판정문 = `docs/reviews/codex_review_supr_fix_reverify_20261014.md` (묶음 안 원본 바이트 그대로 · sha256 `10aca0b1a46fa8c9ec05f46e7f41e4e0440da2ba7912dd5e5889cf19a0c59135`) · 검토 핀 `df647d4e3` · 기준 핀 `a9422d2e7`.
- 원 ZIP = Codex 작업 공간 `codex_supr_fix_reverify_df647d4e3_20261014.zip` (1저자 PC) — 원 ZIP sha256 은 받지 못했다 [미확인].
  1저자가 미니 ZIP 으로 다시 묶어 올림: `codex_supr_reverify_mini_20261014.zip` (2,286,915 B · sha256 `8d2022922becd208ffd5ea689305ba2942590668e5c99d4d6bcc30cee904f5bd` · 원 ZIP 멤버 1,395 전부의 sha256 · 크기 목록 포함).
- `_members.tsv` 열 = sha256 · 크기 · 상태 · 원 경로.  상태 = `keep` (이 폴더에 그대로 170) · `verdict` (판정문 자리로 1) · `tgz` (아래 묶음 안 131) · `drop` (넣지 않음 1,093).
- 넣지 않은 것 (`drop`):
  - `source/` 1,087 파일 = 검토 핀 `df647d4e3` 의 git blob 과 sha256 · 크기 **1,087 / 1,087 같음** (반입 때 `git show` 로 대조).
  - `baseline/` 4 파일 = 기준 핀 `a9422d2e7` 의 같은 경로 blob 과 같음 (두 등록 문서 · 실행기 · 영수증 도구).
  - 묶음의 evidence 폴더 tree.json (3,776,567 B · GitHub tree 응답 · 미니 ZIP 상한 2 MB 초과) · compare.json (1,810,656 B · GitHub compare 응답 — 같은 정보 = git 이력).
- 묶은 것 (`tgz`): `evidence/digest_probe/production194_altered_harvest/` (Codex 반례 입력 = 기술자 130 + `_batch_summary.json`) → `evidence/digest_probe/_production194_altered_harvest.tgz`
  (377,173 B · sha256 `b75e6403453e82b154d2305541648e84162cb1af4b8fe4a7e79a829bc69529dd` · 이름 정렬 · mtime 0 · 멤버 이름 = `production194_altered_harvest/<파일>`).
- 묶음 안 스크립트 (`probes/` · `package_review.py` · `prepare_source.py`) 는 **실행하지 않았다** (반입 규칙 — 읽기만).
- 판정문 · `README.md` · `notes/` 의 상대 경로 (`source/` · `baseline/` · `evidence/` · `probes/`) 는 Codex 묶음 루트 기준이다 (`notes/` 안 다섯 = `docs/reviews/doc_refs_allowlist.tsv`).

## 우리 트리 재현 (10-14 · HEAD `1087a9b2f` — `scripts/` · `webapp/` = 검토 핀 `df647d4e3` 과 diff 0 · Linux)

| 확인 | 우리 결과 | Codex |
|---|---|---|
| `scripts/supp20_input_receipt.py --selftest` | 88/88 PASS | 88/88 (의존성 경로 연결 뒤 · 처음 79/88 = SciPy 없는 환경) |
| `scripts/supp20_input_receipt.py` (기본 컨테이너 입력) | rc 0 · 대조 11 칸 · 다름 0 | rc 0 · 11 칸 |
| `scripts/test_lhs_release_v13.py` | 256 PASS · 0 FAIL | 254 PASS · 2 FAIL (V10a POSIX 경로 문자열 · V16a Git checkout HEAD = Windows · 부분 스냅샷) |
| `scripts/run_network_194_parallel.py --selftest` | 139/139 | 독립 재현 안 함 (Linux 전용) |
| 옛 로그 다섯 → `--dry-run-log` (`docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/`) | 다섯 다 rc 1 (E0) | 다섯 다 rc 1 |

원문 = `_repro_ours_20261014/` (요약 `summary.txt` · 로그별 `*.receipt.txt`).

## 원장에 옮긴 것

- `SUPR-01` · `SUPR-02` = verified (범위 = 원장 `verified_scope`).
- 닫힘과 별개인 발사 전 조건 (판정문 §2 · §3): ① 194 는 P0–P10 rc 0 만으로 등록 §2 일치를 주장하지 않는다 (반례 = lhs TSV 끝 개행 하나) → 다섯 값 전체 대조 기록 (1저자 10-14 = 이번 발사는 손 대조 · 자동 대조 = v1.3 뒤)
  ② 실제 발사 = `--approved-sha` ③ `runner.sha256` = 기록 전용 (P0–P10 이 비교하지 않는다) — *"실행 도구 파일 지문까지 자동 인증"* 이라 쓰지 않는다 ④ 영수증 + 로그 전체 일관 위조 = 범위 밖 · 두 파일 원자성 = 파일별.
