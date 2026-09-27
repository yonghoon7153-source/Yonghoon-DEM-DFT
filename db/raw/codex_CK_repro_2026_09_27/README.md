# Codex CK 재현 묶음 보존본 (2026-09-27 · **GO**)

- 1저자가 대화에 첨부한 `CK_review_and_repro_f4441c426.zip` 의 내용 **열여덟 파일 그대로** (대상 커밋 f4441c426 · 판정 GO):
  `REVIEW_CK.md` (회신 전문) · `README_REPRO_CK.md` (실행법) · `probe_pack_ck.py` + `pack_ck_results.json` + `pack_ck_run.log` + `pack_ck_focused.log` (CK 추가 차단 시험 16 + 신뢰 경계 진단 1 — 성공을 돌려주는 find 가 stdout.log 를 빼는 경우) ·
  `check_results_ck.py` (저장 결과 재단언) · CJ 원본 `probe_pack_cj.py` + `pack_cj_results.json` · `probe_semantics_cj.py` + `semantic_cj_results.json` + `semantic_ck_run.log` · CI 원본 `repro_ci.py` + `results_ci.json` + `ci_regression.log` · `audit_metadata.py` + `metadata_ci.json` + `metadata_run.log`.
  이름에 CI/CJ 가 남은 JSON 도 **이번 CK 커밋에서 다시 돌린** 결과다 (리뷰어 명시 · 내부 identity/runner sha 로 구분).
- 리뷰어 환경에는 `simple-dftd3` 가 없어 원 selftest 194 · 돌연변이 12 는 재현하지 않았다고 명시했다. Windows Git Bash/GNU 도구에서 수행 — 업체 Linux 환경의 실행 검증은 아니다.
- 실행: `python3 db/raw/codex_CK_repro_2026_09_27/probe_pack_ck.py --source . --bash /bin/bash` (복사본 폴더에서 · 결과 JSON 을 옆에 쓴다).
- 회신 원문: `kb/reviews/codex_CK_reply_wad_aprime_v5_vasp_outsourcing_v6_2026_09_27.md`.
