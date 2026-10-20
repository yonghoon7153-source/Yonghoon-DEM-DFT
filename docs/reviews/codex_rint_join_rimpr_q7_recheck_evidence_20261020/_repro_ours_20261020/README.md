# 우리 트리 재현 — Codex Rint 조인 · Q7 재확인 (검토 핀 `2b9efa253` · 대조 핀 `dcb97f1ed` · 2026-10-20)

결과 표 = `../_README_import.md` 의 *우리 트리 재현* 절.  이 폴더는 그 표의 근거 파일이다.

- `probe_path_changes.diff` — Codex 탐침 6 종을 묶음 밖으로 복사할 때 바꾼 줄 전부 (경로 상수만: 현재 코드 = 작업 트리 · 대조 코드 = `git archive dcb97f1ed` ·
  옛 10-15 반례 = 묶음 원본 · `run_submitted.py` 는 Windows 전용 resource 대체 폴더를 PYTHONPATH 에서 뺌 — Linux 에는 진짜 모듈이 있다).  만든 도구 = `tools/patch_probes.py`.
- 우리 출력 (작은 것만): `structure_minimal_replay.json` · `numeric_overflow_replay_current.json` · `numeric_overflow_replay_baseline.json` · `q7_independent.json` · `submitted_new.json` · `submitted_old.json`.
  큰 출력 (구조 · 수치 결과 JSON · φ npz · 시험 로그) 은 넣지 않고 sha256 · 크기만 `results_ours.json` 의 `our_outputs_not_copied_here` 에 적었다.
- `results_ours.json` — 환경 · 시험 집계 (우리 ↔ Codex) · Q7 σ 여섯 값과 상대차 · N9b φ 해시 · 행렬 해시 대조.
- `tools/` — 대조에 쓴 읽기 전용 도구 (`json_compare.py` = 경로 · 시각 · 환경 칸을 뺀 재귀 대조 · `fixture_cmp.py` · `fail_sets.py` · `q7_summary.py` · `q7_maxrel.py` · `npz_cmp.py` ·
  `tree_vs_lstree.py` · `manifest_vs_lstree.py` · `seal_scope.py` · `prior_vs_repo_named.py` · `verify_package_manifest.py`) 와 반입 도구 (`list_zip.py` · `safe_extract.py` · `untar.py` ·
  `build_import.py` · `build_repro_folder.py`).  스크래치 절대 경로가 박혀 있다 (그 기계 · 그 시각의 기록).
- 실행 순서 (묶음 밖 복사본에서 · `python3 -I -X utf8 -B`): `structure_minimal_replay.py` → `structure_probe.py` → `numeric_review.py` → `numeric_review.py --baseline` →
  `numeric_overflow_replay.py` → `numeric_overflow_replay.py --baseline` (현재 수치 탐침이 만든 입력을 읽는다) → `q7_independent.py` → `run_submitted.py new` → `run_submitted.py old`.
  작업 트리에는 아무것도 쓰지 않았다 (실행 뒤 `git status` 변화 0 · 시험 임시 폴더 = 복사본 아래).
