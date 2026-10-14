# 반입 기록 — Codex DEM 언로딩 키트 재검토 증거 (핀 `2783061ea` · 2026-10-14)

- 판정문 (리포 사본) = `docs/reviews/codex_review_dem_unloading_kit_20261014.md` (묶음 루트의 같은 이름 파일 · 바이트 그대로).
- 받은 ZIP = `codex_dem_unloading_kit_review_2783061ea_20261014.zip` · sha256 `f6941302ea4d53f0a1d262cd3929ca7ccf9a94b797a50e8a857f33c7961e67a2` · 2,849,961 B · 항목 1,352 · 풀면 10,991,675 B (1저자 업로드).
- 반입 처리: 새 빈 폴더에 복사 → sha256 → 멤버 목록 (절대 경로 · `..` · 링크 0) → 풀기 → **묶음 안 스크립트 (탐침 · reproduce.py 등) 는 실행하지 않았다** (받은 코드 = 신뢰하지 않는 자료 · 읽기만).
- 묶음 `source/` 197 파일 = 리포 `2783061ea` 의 같은 경로와 **바이트 같음 197/197** (내 대조 · `git show` sha256).

## 무엇을 넣었나 (`_members.tsv` = 1,352 항목 전부의 크기 · sha256 · 처리)

| 처리 | 수 | 무엇 |
|---|---|---|
| 그대로 | 57 | 판정문 · README · PACKAGE_MANIFEST.json · source_manifest.json · upstream_manifest.json · `evidence/` 맨 위 파일 (판정 JSON · 자체시험 로그 · 재현 로그) · `probes/` 8 · `notes/` 3 · `submitted/` · 묶음 도구 스크립트 5 |
| 한 파일로 묶음 | 696 | 합성 반례 입력 (reader_cases · reader_continuation · observer_cases · history_restore_probe) → `evidence/_cases_20261014.tgz` (sha256 `fe824653829cb06624cfecf3952f9e3614eacbac675f5c92eb3ed552cb078ac3`) |
| 뺌 | 599 | `source/` (리포 핀 사본) · `upstream/` (LIGGGHTS-PUBLIC 3d5c00f 공개 원본 47 — 목록 = upstream_manifest.json) · `tree.json` (파일 목록) · `evidence/history_actual/` (= 리포 이력 시험 보고 묶음을 푼 것) · `evidence/history_no_syn/` (같은 묶음에서 SYN 만 뺀 사본) |

- 판정문 · 노트의 상대 경로 (`evidence/…` · `probes/…` · `notes/…` · `source/…`) 는 **묶음 루트 기준**이다 — 리포에서는 이 폴더가 그 루트다 (`source/…` 는 리포 같은 경로).
- 우리 트리 재현: 이번 반입은 Codex 탐침을 돌리지 않았다 (위 처리 규칙).  각 반례는 수정 단계에서 **우리 시험으로 먼저 다시 만든다** (시험 먼저 · 고치기 전 실패 확인) — 수정 계획 `docs/reviews/dem_unloading_kit_fix_plan_20261014.md`.
