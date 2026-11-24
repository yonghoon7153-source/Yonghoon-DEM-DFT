run1_* — 실행기 459b5f4c2b2fc44a3d0995ce89814644a64048f91d0a32734974f95115427139 로 한 실행기 시험의 최종 기록 1 차 (2026-11-24T12:41:56Z–12:46:31Z) · 대체됨 · 보존.
결과: selftest_runner 21 / 21 (rc 0) · mutation_proof_runner 10 / 10 (rc 0) · runner_vs_oct.diff (그 실행기 기준).
대체한 이유: 정적 자체 검토에서 실행기가 승인 블록의 요청서 경로를 고정하지 않음을 찾았다 — 블록이 다른 요청서 (예: v1) 를 그 요청서의 맞는 sha 와 함께 가리키면
  precheck 를 통과했다 (sha 만 대조 · 경로는 블록에서 읽음). 재현 시험 T15 를 먼저 쓰고 (red_runner.*) 실행기에 요청서 경로 대조를 더한 뒤 (변이 RM9) 다시 기록했다.
사본: run1_selftest_runner.py · run1_mutation_proof_runner.py (그때의 시험) · run1_reil_c4_env_reseal_run.py (그때의 실행기 바이트). 이 사본들은 실행하지 않는다 — 보존만.
