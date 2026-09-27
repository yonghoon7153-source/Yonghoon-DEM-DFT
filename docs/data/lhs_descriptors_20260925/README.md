# LHS 130 구조 디스크립터 — 재수확 v2 (2026-09-25)

`docs/data/lhs_descriptors_20260924/` 를 **대체**한다 (그 판과 공통 값은 전부 같다 — Δ = 0).  이 판에서 새로 생긴 것은
`handover_qc` (인계 QC 평면) 와 `boundary_qc` 의 상태 셋 — `calculation_status` · `physical_target_status` · `hold_reason_codes` — 이다
(판단 J18, Codex `HND-01` ~ `HND-06`, 코드 `af528e24d`).

## 출처

- WSL (`DESKTOP-IK8J81H` · `/home/yonghoon71`) 에서 `~/dem-web` 의 수확기 v2 를 인터프리터 `~/Yonghoon-DEM-DFT/venv` 로.
  측정 규약 ID `harvest_v2_20260925/spheresum_nominal_gap/wall_z0/exact_step_mesh`.  수확 때 코드의 정확한 커밋은 배치 요약에 없다 `[미확인]`
  (규약 ID 는 `af528e24d` 가 도입한 것).
- `scripts/lhs_harvest_batch.py --verify-sha` → 성공 **130/130** · 메시 `exact` 130 · 봉인 코호트 (`docs/data/area_s2_cohort.tsv`) sha 대조 130.
- 교차검사 `scripts/lhs_phi_crosscheck.py` (웹앱 `dem_analysis_core.calc_porosity` 를 **직접 호출**) → `_phi_crosscheck.tsv`: SAME 130 · 최대 잔차 5.6e-14 %p.
  남은 1 행은 코호트의 `perc` 행 (케이스가 아니다).

## 상태 (130)

| | 건수 |
|---|---|
| `physical_target_status` OK | 71 |
| HOLD — `BOUNDARY_CENTER_OUT` 만 | 41 |
| HOLD — `NEGATIVE_POROSITY` 만 | 16 |
| HOLD — 둘 다 | 2 |

⇒ 경계 이탈 **43** · 음수 **18** (판단 J18 D 의 두 수).  `calculation_status` 는 130 전부 OK (계산 성공 여부 — 물리 적격성과 따로다).

## 값 (가) = 웹앱 규약 ε_sphere

중앙 **9.89 %** (−2.43 … 27.07).  ⚠ SE 가 고체의 50 % 를 넘는 침대에서 음수가 된다 — 겹침 이중계상 (판단 J19).
겹침을 뺀 값 (ε_union) 은 `docs/data/lhs_union_20260927/`.
