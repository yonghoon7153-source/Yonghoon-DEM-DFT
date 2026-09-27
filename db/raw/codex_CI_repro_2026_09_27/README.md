# Codex CI 재현 묶음 보존본 (2026-09-27)

- 1저자가 대화에 첨부한 `CI_review_and_repro_c25e0ce20.zip` 의 내용 **여덟 파일 그대로** (대상 커밋 c25e0ce20):
  `REVIEW_CI.md` (회신 전문) · `README_REPRO.md` (실행법) · `repro_ci.py` + `results_ci.json` + `repro_ci_run.log` (종합 재현 · 관측 기록) ·
  `repro_pack_ci.sh` (P1 최소 재현 — `BASH_ENV` 로 `find` 함수 하나만 주입 · 종료 4 기대) · `audit_metadata.py` + `metadata_ci.json` (신원·기하 대조 · native selftest 미완료 기록).
- 리뷰어의 Windows 경로·Git Bash 가정이 들어 있다 (`README_REPRO.md`). 이 저장소에서는 `bash db/raw/codex_CI_repro_2026_09_27/repro_pack_ci.sh db/inputs/wad_aprime_v5_vasp_2026_09_27` 이 그대로 돈다
  (고친 뒤 종료 0 · 고치기 전 커밋 c25e0ce20 에서는 종료 1 = 재현).
- 리뷰어 환경에는 `simple-dftd3` 가 없어 원 selftest 155 · 돌연변이 13 은 재현하지 않았다고 명시했다 (`metadata_ci.json`).
- 우리 쪽 회귀는 `tools/wad/build_v5_vasp_package.py --selftest` 의 CI 음성시험(v5 · 같은 BASH_ENV 주입 방식)이 맡는다.
- 회신 원문: `kb/reviews/codex_CI_reply_wad_aprime_v5_vasp_outsourcing_v4_2026_09_27.md`.
