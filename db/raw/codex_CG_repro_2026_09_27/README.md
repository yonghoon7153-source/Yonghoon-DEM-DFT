# Codex CG 재현 결과 보존본 (2026-09-27)

- `results_pasted.json` — Codex CG 리뷰어가 대화에 붙여 보낸 결과 JSON **전문** (1저자 붙여넣기 · 대상 커밋 c8d77dfd5). 리뷰어가 말한 `results.json`/`focused_results.json` 중 어느 파일인지는 적혀 있지 않았다 — 둘의 항목이 섞여 있다 (CF 회귀 + P1 집중 재현 + 선택 권고).
- ⚠ 재현 스크립트 `repro_cg.py` · `focused_cg.py` 는 **받지 못했다** (회신에 이름만 있다). 리뷰어의 Windows 경로(`C:/…`)는 리뷰어 쪽 스냅샷이다.
- 리뷰어 환경에는 `simple-dftd3` 가 없어 원 selftest 130 · 돌연변이 38 은 재현하지 않았다고 명시했다 (`native_selftest.not_completed`).
- 우리 쪽 재현·회귀는 `tools/wad/build_v5_vasp_package.py --selftest` 의 CG 음성시험(v4)이 맡는다.
- 회신 원문: `kb/reviews/codex_CG_reply_wad_aprime_v5_vasp_outsourcing_v3_2026_09_27.md`.
