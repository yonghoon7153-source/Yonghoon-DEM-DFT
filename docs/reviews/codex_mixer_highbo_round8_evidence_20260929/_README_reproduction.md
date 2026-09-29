# 재현 (우리 HEAD `7e0f751c8`, 2026-09-29)

- 원 묶음 `docs/reviews/codex_mixer_highbo_round8_bundle_20260929.md` sha256 = `b7caae05…` = Codex 대상 (MANIFEST bundle_original.md 와 동일).
- HEAD `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` sha256 = `ab20ef77…` · 245 행 = Codex 가 추출한 v2.2 (`prereg_v22_extracted.md`).
- baseline 핀 `make_mixer_deck.py` blob `033fac54` · `measure_mixing_index.py` blob `53da219a` = HEAD 의 같은 파일 (git hash-object).
- `audit_round8.py` 를 baseline = HEAD 스크립트 사본으로 실행 → **15 PASS / 0 FAIL** · 결과 JSON 181 항 전부 동일 (`_reproduction_audit_results_HEAD_7e0f751c8.json`).
- 시뮬레이션 · ibb · 생산 코드 변경 없음.  판정문 = `../codex_review_mixer_highbo_round8_prereg_20260929.md` (= review.md).
