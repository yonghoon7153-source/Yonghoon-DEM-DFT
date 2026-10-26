# 우리 트리 재현 (10-26 · Claude)

- 받은 ZIP sha256 `9944f044a898897714974de2d788df9ae8c39a069c7cf457ec6c77a42ebb5f42` (672,344 B) · 판정문 = `docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md`.
- `snapshot/repo/` 48 파일 = 우리 커밋 `3056eef12` blob 과 바이트 같음 (48/48 · 차이 0) → 그 사본에서 돈 탐침 = 우리 트리.
- Codex 탐침 다섯 (`docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_design/probe_design.py` · `docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_restart/probe_source_semantics.py` · `docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_restart/probe_seeded_rounding.py` · `docs/reviews/codex_kg50_decks_review_20261026/evidence/root/probe_numerics_and_endpoint.py` · `docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_decks/probe_terminal_cadence.py`) 를 우리 환경 (Python 3.11) 에서 다시 돌림 = 모두 rc 0.
- 결과 JSON 다섯 잎 단위 대조: terminal_cadence 114 · probe_design 232 · seeded_rounding 133 · semantic_probe 95 잎 = 차이 0 · root_probe 158 잎 중 차이 4 = `/sources[0–3]/path` (소스 파일 절대 경로 — 환경) · 판정값 차이 0.
- 실행하지 않은 것: LIGGGHTS · MPI · scheduler (Codex 와 같음) · `probe_resume_gates.py` (Bash harness — Codex 도 실행 증거에서 뺌).
