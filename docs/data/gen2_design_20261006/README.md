# 접촉망 세대 2 설계 근거 (C1 · C2 · 2026-10-06 저녁)

설계 기록 = `docs/reviews/gen2_network_design_20261006.md` (결정표 · 1저자 비준 · 구현 뒤 실측).  이 폴더 = 그 표의 수치를 낸 스크립트 · 출력 **실행 당시 사본**.

- `c1/` — 전극 (L2-05) · Hertz 협착 (H0 · H1 · H12) · CF 가드.  `DECISIONS_C1.md` = 설계 요약 원본.
  FV 기준: `fv_sphere_chain.py` (구 사슬 · `fv_sphere_chain_table.txt`) · `fv_lattice3d*.py` (SC · BCC · FCC 격자 · `lat_*.log` · `br_SC03.log`) · `fv_oct.py` (`oct_*.log`) · `fv_random.py` (무작위 충전 · `rand_*.log`).
  실침대 망: `net_beds.py` · `net_beds_physics.py` · `net_beds_diag.py` (`net_beds_*.json/.log`) · `l205_demo.py` (막다른 가지) · `lhs194_estimates.py` (194 행 효과 추정) · `chain_compare.py` · `sc_codex_check.py`.
- `c2/` — Physics 면적 (L1-01 · 02 · 03 · 08 · DESC-03 · 10 · SELF-28 · LHS-25 · 26).  `DECISIONS_C2.md` = 설계 요약 원본.
  `g2lib.py` (제안 함수) · `eval_bed*.py` · `fastsolve.py` (규칙 A/B · floor 후보 · 쌍별 E* · `eval_*.out/.json`) · `cov_union*.py` (⑥ 합집합 피복 · `cov_*`) ·
  `force_balance.py` · `force_check.py` · `eval_fdem.py` (세대 3 질문 — DEM 힘 ↔ real-E 재구성 힘) · `eval_floor_alt.py` · `lhs26_fixture/` (⑦ 모양 인자) · `ledger_entries.txt` (원장 문안 초안).

넣지 않은 것 (같은 내용이 리포에 있다):
- 리포 모듈 사본 (`lib/` · `head/`) — `git show <sha>:scripts/<모듈>` 로 복원.  C1 의 sha = `c1/LIB_HEAD_SHA.txt`.
- 덤프 사본 (`data/`) — `docs/data/real14_reference_20260928/{atom,contact}_2060000.liggghts.gz` · `docs/data/case15_corner_20261001/{atom,contact}_v4_1710000.liggghts.gz` 를 푼 것.

⚠ 경로 · 상수를 고치지 않은 사본이라 그대로는 돌지 않을 수 있다 (`lib/` · `data/` 자리).  구현 뒤 수치는 리포 시험이 지킨다 —
`scripts/test_physics_area_g2.py` · `scripts/test_network_dirichlet.py` · `scripts/test_network_generation2.py` · `scripts/test_network_boundary_rule.py`.
