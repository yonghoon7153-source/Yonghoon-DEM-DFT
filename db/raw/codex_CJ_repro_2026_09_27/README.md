# Codex CJ 재현 묶음 보존본 (2026-09-27)

- 1저자가 대화에 첨부한 `CJ_review_and_repro_a2374014b.zip` 의 내용 **열세 파일 그대로** (대상 커밋 a2374014b):
  `REVIEW_CJ.md` (회신 전문) · `README_REPRO_CJ.md` (실행법) · `probe_pack_cj.py` + `pack_cj_results.json` + `pack_cj_run.log` (P1 포장 경계 재현 · BASH_ENV 주입 — `mgmt_echo_error` · `manifest_echo_error` 가 필수 수정 · `sha_*` · `second_mv_error` · `post_promotion_cleanup_error` 는 권고/잔여위험) ·
  `probe_semantics_cj.py` + `semantic_cj_results.json` (TITEL_TRUNCATED · 무엔트로피 None 집계) · `repro_ci.py` + `repro_pack_ci.sh` + `results_ci.json` + `ci_regression.log` (CI 회귀 — 원문 sha 는 CI 때와 같음 · 이번 커밋에서 통과) · `audit_metadata.py` + `metadata_ci.json` (신원·기하 · native selftest 미완료 기록).
- 실행: `python3 db/raw/codex_CJ_repro_2026_09_27/probe_pack_cj.py --source . --bash /bin/bash --assert-fixed` — 고치기 전 커밋 a2374014b 에서는 최종 assertion 실패(= 재현 성공) · 고친 뒤 종료 0.
- 리뷰어 환경에는 `simple-dftd3` 가 없어 원 selftest 175 · 돌연변이 11 은 재현하지 않았다고 명시했다.
- 우리 쪽 회귀는 `tools/wad/build_v5_vasp_package.py --selftest` 의 CJ 음성시험(v6)이 맡고, 이 폴더의 `probe_pack_cj.py` 를 selftest 가 있으면 그대로 돌린다.
- 회신 원문: `kb/reviews/codex_CJ_reply_wad_aprime_v5_vasp_outsourcing_v5_2026_09_27.md`.
