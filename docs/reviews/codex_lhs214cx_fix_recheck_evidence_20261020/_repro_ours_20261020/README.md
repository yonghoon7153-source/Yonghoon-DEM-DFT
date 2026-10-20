# 우리 트리 재현 — Codex LHS214 S06 · S02 재확인 (검토 핀 `34713ac96` · 대조 핀 `685c2bbdb` · 10-20)

- 기계 = 이 컨테이너 (Linux 6.18 x86_64 · 4 vCPU · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 (system dist-packages) · markdown-it-py **없음** ·
  OMP · OpenBLAS · MKL · NumExpr 스레드 1).  Codex = Windows 11 build 26200 · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · markdown-it-py 3.0.0.
- 우리 트리의 LHS214 코드 = 검토 핀 코드 (Codex `source_manifest.json` 2,135 중 다른 9 = 그 뒤 문서 넷 + Rint 파일 다섯 · `tree_cmp.json`).
- 시험 · 영수증은 **작업 트리를 건드리기 전** (깨끗한 트리) 에 돌렸다 · 임시 · 웹앱 · Matplotlib 폴더 = 스크래치 (`tools/run_ours.py`) · `-B` (바이트코드 안 씀).
- 대조 표 · 판정 = 상위 `_README_import.md` §우리 트리 재현.  기계가 읽는 요약 = `results_ours.json`.

| 파일 | 무엇 · 어떻게 |
|---|---|
| `out/current_boundary.log` · `.json` | `scripts/test_l214r_r01_restored_full.py` 원본 그대로 (검토 핀 판 = 작업 트리 판) · 40/40 rc 0 · 10.1 s |
| `out/baseline_boundary.log` · `.json` | 대조 핀 판 (`git show 685c2bbdb:` · sha256 `eaff4ba4…` = 판정문 §4-1 표) 을 `tools/run_baseline_exec.py` 로 실행 — 파일을 트리에 쓰지 않고 `__file__` 만 우리 트리 시험 자리로 (모듈 · `docs/data` 를 우리 트리에서 읽게) · 30/30 rc 0 · Rint 모듈은 import 안 됨 |
| `out/current_receipt_selftest.log` · `.json` | `scripts/supp20_input_receipt.py --selftest` 원본 그대로 · 어댑터 없음 · 122/122 rc 0 · 33 s |
| `out/actual_receipt.log` · `.json` · `out/actual_receipt_ours.json` | 인자 없는 실제 보충 20 등록 영수증 (`--json` 만) · rc 1 · 실패 칸 D1 하나 |
| `s02_probe/` | Codex `docs/reviews/codex_lhs214cx_fix_recheck_evidence_20261020/probes/s02/adversary.py` 의 묶음 밖 복사본 (경로 상수만 바꿈 = probe_path_changes.diff) 을 `python3 -I -X utf8 -B` 로 core · axis · mutants · failclosed (sweep 은 브리프 지시로 안 돌림) — 탐침이 쓴 JSON · 로그 + 화면 (`*.stdout` · stderr 는 넷 다 빈 출력) |
| `s06_nooracle.json` | `tools/s06_nooracle.py` — markdown-it-py 가 없어 Codex `docs/reviews/codex_lhs214cx_fix_recheck_evidence_20261020/probes/s06/parser_audit.py` 는 못 돈다 → 같은 생성 코드 (그대로 옮김) · 같은 입력으로 우리 새 도구 · 대조 핀 도구 판정과 전체 `receipt()` 를 내고 Codex 기록 (oracle `expected` 는 기록값을 데이터로 씀) 과 대조 · 메모리 안 어댑터 둘 (git_info = 선언 핀 · 대조 핀 도구의 모듈 전역 REPO = 우리 트리) |
| `scope_ours.json` · `tree_cmp.json` | git 으로 직접 (`git ls-tree -r -l -z` 세 판) — 봉인 32 · HANDOVER 2 · 등록 문서 · 배포 빌더 · 생산 · 소비 바이트 · 고정 입력 상수 · FULL 정책 줄 · 재계산 지문 / 묶음 evidence/tree.json (해시만) ↔ `git ls-tree -r 34713ac96` · manifest ↔ 핀 blob |
| `results_ours.json` | 위 출력을 모은 대조 요약 (`tools/results_ours.py`) |
| `tools/` | 이 반입의 재현 · 묶음 처리에 쓴 우리 도구 13 (묶음 검사 · 풀기 · 분류 · 반입 조립 · 실행 래퍼 · 탐침 복사 · S06 판별 · 범위 · 요약) — 원장 · 참조 예외 · CLAUDE.md · 진행 기록 편집 도구는 넣지 않았다 (결과 = 이 반입 커밋의 diff) |

- 실행하지 않은 Codex 스크립트 (상위 폴더 기준) = intake.py (GitHub 네트워크) · package_review.py (ZIP 쓰기) · probes/run_original.py (우리 두 시험의 하위 프로세스 래퍼 — 두 시험을 직접 돌림) ·
  probes/s06/parser_audit.py · supplementary.py · generation_environment.py (markdown-it-py) · probes/scope/cx_scope_audit.py (Codex 작업 공간 `source/` 스냅샷 필요 → git 직접).
- 한정: 판정값 재현이다 — `check_all.sh` 전체 · WSL · 새 214 · 생산 σ 재계산 아님.  S06 oracle 자체 (markdown-it-py 토큰) 는 재현하지 않았다 (8,736 · 30,000 은 옛 ↔ 새 판정 차이 수 = 필요조건 대조).
