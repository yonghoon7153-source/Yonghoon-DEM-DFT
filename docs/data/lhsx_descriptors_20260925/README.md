# lhsx 64 구조 디스크립터 — LHS 확장 v2 수확 (2026-09-25)

설계 `docs/data/lhs_ext_design_v2_20260829.csv` (상자 `docs/data/lhs_ext_box_v2_20260829.json`) 의 64 건.  130 과 **같은 수확기 · 같은 규약**
(`harvest_v2_20260925/spheresum_nominal_gap/wall_z0/exact_step_mesh`).

## 출처

- WSL (`DESKTOP-IK8J81H` · `/home/yonghoon71`) · 원본 `~/lhsx_local` · 봉인 코호트 `_cohort.tsv` (이 폴더 — 원본 `~/lhsx_cohort_20260925.tsv`, 도구 커밋 `2d8c67822`).
- `lhs_harvest_batch --verify-sha` → 성공 **64/64** · 메시 `exact` 64 · sha 대조 64.  수확 때 코드 커밋 `[미확인]` (130 과 같은 세대).
- 교차검사 (`_phi_crosscheck.tsv`, 웹앱 `calc_porosity` 직접 호출) → SAME 64 · 최대 잔차 4.6e-14 %p.

## 설계 영역 — 130 과 다른 점

확장은 **SE 질량분율** `pdd_SE` 를 0.306–0.699 로 올렸다 (130 은 0.05–0.30) ⇒ 고체 중 SE 부피 0.51–0.85 (130 은 0.11–0.51).  반지름 · AM_P 몫은
130 상자와 겹친다.

## 상태 (64)

| | 건수 |
|---|---|
| `physical_target_status` OK | **2** (`lhsx_001` · `lhsx_040`) |
| HOLD — `NEGATIVE_POROSITY` 만 | 51 |
| HOLD — 둘 다 | 9 |
| HOLD — `BOUNDARY_CENTER_OUT` 만 | 2 |

## 값 (가) = 웹앱 규약 ε_sphere

중앙 **−4.26 %** (−8.40 … 1.52) — 음수 60/64.  수확 · 덱 결함이 아니다 (판단 J19): SE 가 하중을 지는 영역에서 **SE–SE 겹침이 두 번 세어진다**.
겹침을 뺀 정확한 union 은 64 건 전부 양수 (5.43 … 9.43 %) — `docs/data/lhs_union_20260927/`.
