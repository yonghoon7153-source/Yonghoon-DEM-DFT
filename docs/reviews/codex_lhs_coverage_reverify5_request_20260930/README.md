# Codex 재검증 5 요청 묶음 (2026-09-30 밤)

요청서 = `docs/reviews/codex_lhs_coverage_reverify5_request_20260930.md`.  적용: 재검증 4 후보 (= `9ab4bc320`) 위에 0018 → 0019.

| 파일 | 무엇 |
|---|---|
| `0018-…n_clip-n_am-100-std-0-Codex.patch` · `0019-…producer_pin-hosts-Codex-LHSC.patch` | 수정 (커밋 `b0f581e14` · `6e4ef6925`) |
| `source_manifest.json` | base · tip · 패치 · 적용 후 3 파일 sha256 · git blob |
| `selftests_6e4ef6925.log` | 셀프테스트 6 (rc 0) — 수확기 165 · 파이프라인 216 |
| `fixed_tree_reproduction/` | Codex 재검증 4 스크립트 (r5 · r4 · schema · numeric_domain · producer) 무변경 실행 결과 (`r5_results_before_fix_9ab4bc320.json` = 수정 전 트리 · `audit_r5_fixed.stdout` = 고친 트리 화면 출력) |
| `SHA256SUMS` | 이 폴더 (README · SHA256SUMS 제외) |
