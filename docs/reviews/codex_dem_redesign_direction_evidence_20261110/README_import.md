# Codex 반박 리뷰 — [DEM 우선 (수영)] 방향 메모 3.1 판 (11-10) · 반입 기록

- 판정문 = `docs/reviews/codex_review_dem_redesign_direction_20261110.md` — 받은 묶음 안 원본 31065 B · sha256 ee1d011e301640719e1e7e811ab124562f044b19682a60aee3f35d3a5e0d9058 · CR 0 · 주소 꼴 0 → 리포 사본 = 원본과 바이트 같음 (공개 논문 URL 은 그대로).
- 리뷰 핀 = `13eb293cd` (13eb293cd9ac44502517c81e8f5e9b7ae02d817f · 가지 B) · litdb 카드 핀 = `099116169` (정본 가지) · 우리가 보낸 ZIP = codex_dem_redesign_direction_13eb293cd9ac.zip (2360081 B · sha256 9680133b… · Codex 입력 대조 = 같음).
- 받은 것 = 1저자가 대화에 올린 판정 · 증거 ZIP (2453250 B · sha256 d3c9202209cb9f6a4d19bdfb22e669e6fbec4accaa73e8d061b72fa646dff9a2 · 항목 83) · 빈 폴더에 `python3 -I` 로 풀어 검사 (위험 경로 0 · 중복 0 · CRC 이상 0).
- 넣은 것 = **29 파일** (바이트 그대로 · 목록 `IMPORT_SHA256SUMS` · `_import_manifest.json`) · 뺀 것 = **54** — 우리가 보낸 ZIP 사본 48 (package/) · 우리 리포 blob 사본 4 (remote_sources/ 의 docs · scripts 사본 · 그 대조 결과 verification.json 은 넣음) · 주소 꼴 1 (branches_review/REPORT.md · Windows 실행 경로 줄 · 이름 · sha256 만) · 판정문 1 (위 자리).

## 우리 환경 재현 (메인 세션)

- 받은 묶음 사본에서 `python3 -I -X utf8 -B reproduce_review.py` (Linux · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1) = **PASS** · 세 탐침 (branches_review/independent_enumeration.py · physics_review/counterexamples.py · code_arithmetic_review/reproduce.py) rc 0 · 기대 JSON 과 같음 (rtol 1e-10) · 입력 48 파일 · 해시 47 행 · 핀 blob 46 · 연구 런 0 · 원격 호스트 0 → `_repro_ours_20261110/reproduce_review_ours.json` (경로 칸 = 자리 표시).

## 처분

`docs/reviews/dem_redesign_direction_20261109/verdict_disposition_20261110.md` — 원장 DRD-01 – DRD-13 open · SELF-161 메모 · 메모 3.2 = 본 세션 (판정문 §7 최소 후속 처분 순서) · 전체 HOLD.
