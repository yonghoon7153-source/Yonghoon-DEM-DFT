# Codex 재검증 3 요청 묶음 — LHSC-03 R3 · LHSC-04 R3a · R3b · P3 수정 (2026-09-30 밤)

요청서 = `docs/reviews/codex_lhs_coverage_reverify3_request_20260930.md`.  판정 대상 = `codex_lhs_coverage_reverify2_verdict_20260930.md` 의 잔여 전부.

| 파일 | 무엇 |
|---|---|
| `0014-LHS-item-2-Codex-LHSC-04-R3a-R3b-P3.patch` | 수확기 — 생산자 산술 오차 모델 E · 미인증 · 음수 면적 · pin · `n_detect_1pct` · 라벨 (커밋 `044220b1a`) |
| `0015-run_pipeline-coverage-v2-Codex-LHSC-03-R3-P2-P3.patch` | 웹앱 검증기 — 분율 · 개수 원장 · 집계 항등식 · blank h_film (커밋 `220b1426e`) |
| `source_manifest.json` | base `ca0471d19` → tip `220b1426e` · 패치 바이트 · sha256 · 적용 후 3 파일 sha256 · git blob (만든 순간 계산) |
| `selftests_220b1426e.log` | 고친 트리의 셀프테스트 6 (rc 전부 0 · 수확기 160 · 파이프라인 212) |
| `fixed_tree_reproduction/` | Codex 재검증 2 스크립트를 **무변경**으로 고친 트리에 실행한 결과 (schema · producer · geometry) · 원본 `audit_power.py` 의 KeyError (의도된 키 제거) · 같은 탐색의 새 키 판 `audit_power_r3.py` + 결과 |
| `SHA256SUMS` | 이 폴더 전체 (이 README · SHA256SUMS 제외) |

적용: 재검증 2 의 후보 사본 (= `ca0471d19` · Codex 후보 10 파일과 CRLF 정규화 뒤 동일) 위에 0014 → 0015 순서로 `git am` (또는 `git apply`).
