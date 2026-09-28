# 재현 기록 (우리 쪽 · 2026-09-29)

- 우리 HEAD `c0c2d4f44` 에서 `python3 audit_prereg.py --out _reproduction_audit_results_HEAD_c0c2d4f44.json` → **118 PASS / 0 FAIL**.
- baseline blob `033fac54d73566ac1dad54f24cc28b9d0510ccbc` = 핀 `18787ab98` 의 `scripts/make_mixer_deck.py` — HEAD 의 같은 파일과 **동일** (git diff 0).
- 결과 JSON (864 항) 은 Codex 의 `audit_results.json` 과 **1 항만** 부동소수 끝자리가 다르다: `equivalence_power/cases/2/power` 0.062165056264889364 (Codex) vs 0.06216505626488936 (우리) — 수치 적분 환경 차.
- 제출 첨부 (`attachment_original.txt` · SHA256 011f7ea8…) = 커밋 `ea7cfef96` 판 `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` 의 **마크다운 문법 제거본** (제목 `#` · 코드 기호 · 굵게 표시만 다름 · 내용 동일).
- `review.md` = `docs/reviews/codex_review_mixer_highbo_round7_prereg_20260929.md` (같은 바이트).  DEM · MPI · SLURM · 생산 코드 변경은 이 반입에서도 없음.
