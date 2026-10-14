# 반입 기록 — Codex DEM 언로딩 키트 재확인 (핀 `a30fe150e` · 2026-10-14)

- 판정문 (리포 사본) = `docs/reviews/codex_review_dem_unloading_kit_reverify_20261014.md` (묶음 루트의 같은 이름 파일 · 바이트 그대로 · sha256 `5474f6f07b8cc0797fb439ee8e5b5bb01b469ca50731cb144131de1e004a4088`).
- 받은 ZIP = `codex_dem_unloading_kit_reverify_a30fe150e_20261014.zip` · sha256 `04d9b92e2a93783665bab92a89e0cf66ec6a3ddb1b21c81e5ac0956224da20a8` · 3,649,846 B · 항목 405 (1저자 업로드).
- 반입 처리: 새 빈 폴더에 복사 → sha256 → 멤버 목록 (절대 경로 · `..` 0) → 풀기 → **묶음 안 스크립트 (탐침 · run_baselines.py 등) 는 실행하지 않았다**.
- `_members.tsv` = 405 항목 전부의 sha256 · 크기 · 처리 (`keep` 60 · `verdict` 1 · `drop` 344).

| 뺀 것 (`drop`) | 이유 |
|---|---|
| `source/` | 검토 핀 a30fe150e 의 git blob 과 sha256 203/203 같음 (반입 때 대조) |
| `comparison_base/` | 이전 검토 핀 2783061ea 의 git blob 과 sha256 94/94 같음 |
| `upstream/` | LIGGGHTS-PUBLIC 3d5c00f 공개 원본 47 (목록 = upstream_manifest.json · 이전 반입과 같은 처리) |

- 판정문 · 노트의 상대 경로 (`evidence/…` · `probes/…` · `notes/…` · `source/…`) 는 **묶음 루트 기준**이다 — 리포에서는 이 폴더가 그 루트다 (`source/…` 는 리포 같은 경로 = 핀 `a30fe150e`).  키트 경로 (`ul_reader.py` 등) 는 `docs/data/ps45_unload_20261009/` 기준 · 줄 번호 = 핀 `a30fe150e`.
- ★ `ULKRR-01` (문법 fixture 스칼라 ↔ 벡터) = 같은 결함을 우리도 **실제 바이너리**에서 봤다 — ibb job 285220 (10-14 19:26 · 같은 핀) 이 판정문이 소스로 예측한 그 줄 (`variable gr_P equal ${gr_P}`) 에서 `ERROR: Mismatched fix in variable formula (../variable.cpp:1315)` 로 멈췄다 (원장 `SELF-115` · 고침 `039abb141` · 판정문 §4 의 "해결 증거" 중 재생성 · 재봉인 · 타입 음성 시험 = 끝 · 실제 바이너리 PASS = ⬜ 실행 2).
