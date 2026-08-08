# Release validation (2026-08-08)

이 문서는 계산 결과가 아니라 **실행·분석 패키지의 회귀검증 기록**이야. 아래 에너지는
가짜 OUTCAR fixture로 만든 값이므로 과학적으로 인용하면 안 돼.

## Static checks

- `scan.py`, `vasp_stage.py`: Python compile 통과
- `run.sh`, `watch.sh`, `vasp_run.sh`: `bash -n` 통과
- package와 생성 VASP input manifest: SHA-256 전 항목 통과

## Generation checks

- `--scope pilot`: 18 templates = surface 16 + molecule 2, relax/static 36 executions
- full-eligible fixture의 `--scope all`: 54 templates = surface 50 + molecule 4,
  relax/static 108 executions(실제 UMA 격리 수에 따라 동적 감소)
- 모든 surface `structure_id`: 서로 다른 magnetic seed 2개
- dimer relaxed 후보 1개를 합법적으로 격리한 handoff: all-scope가 중단되지 않고
  52 templates / 104 executions로 동적 생성
- 생성 묶음에 `UPSTREAM_DFT_HANDOFF.json`, full source hashes,
  `PACKAGE_COMMIT.txt`, runner와 protocol hashes 포함

## Analyzer end-to-end fixture

- all-scope 54/54 relax/static 완료 fixture와 dynamic dense selection을 끝까지 분석
- OUTCAR identity, final CONTCAR, fixed-atom/cell, force, molecular topology,
  periodic image, clean-slab 대비 상부 재구성, Li/Ni/O/other registry,
  48-Ni moment, seed-pair, gas-box와 k-point 경로 실행 확인
- dimer fixture: numeric-pass 경로 도달
- C10 fixture: matched starts가 mixed registry로 합쳐져 `BLOCKED_GEOMETRY` 확인

## Negative tests

- magnetic seed 한쪽의 OUTCAR `SYSTEM`을 변조하면 analyzer exit code `2`,
  `surface_seed_pair_matrix_complete=false`, `INCOMPLETE_AUDIT`
- dimer gas-box 에너지를 0.199 eV 이동하면 계산 반환은 보존하지만
  adsorption 상태는 `BLOCKED_GAS_BOX_CONVERGENCE`, 전체 numeric gate는 false
- matched branch의 자유 상부 Li 한 개를 clean-slab 대비 1.2 Å 이동하면 analyzer
  exit code `2`, seed-pair matrix false, `top-layer Li extraction/reconstruction` 사유 기록

## 아직 실제 계산에서 확인할 것

- Gabia UMA pilot/full screen의 실제 후보
- VASP 서버의 메모리·벽시계·전자/이온 수렴
- winning branches의 Ni local moment와 LDAU occupation matrix 수동 감사
- U, dispersion, coverage, slab-thickness 민감도

따라서 이 release 검증은 “코드 경로가 의도대로 통과·차단된다”는 증거이고,
Li/Ni contact preference나 adsorption energy의 결과는 아니야.
