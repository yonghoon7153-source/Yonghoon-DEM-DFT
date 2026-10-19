# 우리 트리 재현 — Codex 10-19 (핀 `685c2bbdb`) 빈 ATX 제목 반례 (`L214R-S06` = Codex L214S-CX01)

- 코드 = 본 가지 원격 HEAD (`scripts/supp20_input_receipt.py` 는 `685c2bbdb` 와 바이트 같음) · Linux · Python 3.11.17 · `OMP_NUM_THREADS=1`.
- 입력 = 반입 증거 `../lhs214s_recheck_20261019/evidence/s01_new_cases/` 19 문서 · 기대 = `../lhs214s_recheck_20261019/evidence/s01_heading_boundary_cases.json` (Codex 의 실제 결과 · 표준 파서 판정).
- 명령 (리포 루트 · 읽기 전용): `python3 -B docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/_repro_ours_20261019/repro_headings.py . docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019 out.json`
  (Codex 탐침은 실행하지 않았다 — 우리 스크립트가 Codex 입력 파일과 기대값만 읽는다).
- 결과 (`headings_ours.json`): 19 경우 · 표준 판정과 다름 **14** (잘못 수용 12 · 잘못 거부 2 · 대조 5 일치) · Codex 실제 결과 (rc · 실패 칸 · code_fp) 와 **차이 0**.
- S02 (Windows 23/29) 는 이 기계에서 다시 돌리지 않았다 — 같은 등록 입력이 Linux 에서는 세 목표를 정확히 낸다 (S02 증거 `docs/reviews/lhs214s_fix_evidence_20261019/tests/s02_after_normal.log` 30/30).  Windows 수치 = Codex 실측.
