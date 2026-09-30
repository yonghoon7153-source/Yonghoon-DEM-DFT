# 5번 배치 (봉인 `1e09f661d`) 판독 — 옛 기준선 대조 · 새 열 분포 · LHSC-07~10

> **반입 10-01** — 서브에이전트 원문 그대로 (이 세션 scratchpad `cov5_report.md` · 분석 = 인라인 · 방법은 §6).  원자료는 이제 `docs/data/{lhs,lhsx}_{descriptors_cov,webapp_coverage}_1e09f661d/` (README).  ⚠ **이 보고 뒤 확인된 것**: §5-1 `dirty` 의 원인 = 피복 단계가 추적 파일 `docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv` 를 덮어쓴 것 (1저자 WSL `git status` · `git diff` — 코드 변경 아님 · `LHS-27`) · §4-4 v2 빈칸과 §3-1 포화의 공통 원인 = 접촉별 추정 면적 합에 표면 한도가 없다 (J20-m · `LHS-25`) · 값 합리성 = `docs/reviews/lhs_coverage_reasonableness_20261001.md`.

- 작성 2026-09-30 · 읽기 전용 (리포 무수정 · 이 파일 하나만 씀) · 분석 = python 인라인
- 새 산출물 (tar 추출본): `…/scratchpad/cov5/docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` · `{lhs,lhsx}_webapp_coverage_1e09f661d/`
- 옛 기준선 (커밋본): `docs/data/{lhs,lhsx}_descriptors_20260929/` · `docs/data/{lhs,lhsx}_webapp_contact_20260929/`
- 비교 방식: 수확 JSON 은 평탄화 후 키마다 파싱값 `==` (허용오차 없음) · metrics_flat.csv 는 칸 **문자열** 동일 · 케이스는 id 로 짝지음
- 봉인 커밋 `1e09f661d` 는 이 리포에 실재 (2026-09-30 08:30:54 UTC)

---

## 0. 한눈에

| 항목 | LHS 130 | lhsx 64 | 판정 |
|---|---|---|---|
| 수확기 | 130/130 `status OK` · rc 0 · sha_verified 130 · mesh `exact` 130 | 64/64 동일 | ✅ |
| 웹앱 배치 (`--stop-after coverage`) | done **130** · partial/failed/REFUSED 0 | done **64** | ✅ |
| physics v2 상태 | ok **113** · blank **17** | ok **63** · blank **1** (`lhsx_009`) | blank 18/18 = LHSC-01 (a) 분모 무효 |
| 옛 ↔ 새 — 수확기 기존 키 | 30,446 비교 중 비동일 169 = 규칙 문자열 130 + `wall_touch` 39 칸 (7 침대) | 14,956 중 64 = 규칙 문자열만 | ✅ 의도된 변경만 · 부동소수 잡음조차 0 |
| 옛 ↔ 새 — 웹앱 공통 열 | 232 열 × 130 행 문자열 동일 | 231 열 × 64 행 동일 | ✅ Δ = 0 |
| 수확기 ↔ 웹앱 같은 양 | porosity ≤ 1.24e-10 %p · Hertz 피복 ≤ 1.4e-14 %p · 두께 0 · 상 개수 0 불일치 | ≤ 2.5e-10 %p · ≤ 1.4e-14 %p · 0 · 0 | ✅ |
| ⚠ 코드 출처 (`dirty`) | 웹앱 run #2 (129 건) **dirty=true** | run #1 · #2 (64 건 전부) **dirty=true** | 🔴 확인 필요 (§5-1) |
| LHSC-08 근접 접선 | 산출물에 수 없음 · 정확 접선(깊이 = 0) 11 입자 / 7 침대 (옛↔새 차로 역산) | 0 | 부분만 평가 가능 |
| LHSC-09 단일 영상 | 최대 (r1+r2)/(L/2) = **0.600** · 중복 쌍 0 | **0.5998** · 중복 쌍 0 | ✅ (덱 반경 상한 기준) |
| LHSC-10 v2 코퍼스 값 | 침대 빈칸 13.1 % · AM 무효 0.0059 % · cap 충돌 중앙 4.79 % (최대 62.3 %) · 100 % 클립 중앙 28.5 % | 1.6 % · 0.0022 % · 1.84 % (최대 4.51 %) · **100 %** | ⚠ 함수 검토 거리 (§4-4) |

---

## 1. 완결성

### 1-1 수확기 (`_batch_summary.json` + 케이스 JSON)

| | LHS | lhsx |
|---|---|---|
| 케이스 JSON / 파일 수 | 130 / 131 (+ summary) | 64 / 65 |
| n_target · n_ok | 130 · 130 | 64 · 64 |
| rc · status | 0 × 130 · OK × 130 | 0 × 64 · OK × 64 |
| design_family | bimodal 100 · mono_AM_P 15 · mono_AM_S 15 | bimodal 48 · mono_AM_P 8 · mono_AM_S 8 |
| sha_verified · mesh_pick | True 130 · exact 130 | True 64 · exact 64 |
| 옛 summary 와 다른 필드 | `cmd` · `out` (출력 경로) 만 | 같음 |
| 코드 출처 필드 | **없음** (git sha · dirty 키 0 개 — 디렉터리 이름만 `1e09f661d`) | 없음 |

### 1-2 웹앱 배치 (`status.json`)

| | LHS | lhsx |
|---|---|---|
| status | done 130 | done 64 |
| failed_stages | [] × 130 | [] × 64 |
| 단계 | Parse → Bimodal Contact Analysis → Coverage (100) · Parse → Contact Analysis → Coverage (30) — 전부 rc 0 · ok | 48 · 16 동일 |
| mode | bimodal 100 · standard 30 | bimodal 48 · standard 16 |
| type_map_fold (mono 이름 접기, SELF-66) | 30 건 (`1:AM_S,2:SE` 20 · `1:AM_P,2:SE` 10) | 16 건 (12 · 4) |
| 네 원자료 sha = 수확 JSON `raw.*.sha256` | 130/130 | 64/64 |
| 네 sha · contact_scan · type_map · mode = 09-29 기준선 | 130/130 동일 | 64/64 동일 |
| atom_frames · contact n_frames | 1 × 130 · 1 × 130 | 1 × 64 · 1 × 64 |
| elapsed_s (최소/중앙/최대 · 합) | 1.3 / 16.25 / 99.3 s · 0.83 h | 9.2 / 36.75 / 131.1 s · 0.82 h |
| runs | #1 2026-09-30T23:06:19 · `1e09f661d` · **dirty=false** → 1 건 (`lhs00_000`) · #2 23:52:45 · `1e09f661d` · **dirty=true** → 129 건 (마지막 10-01T00:40:50) | #1 23:07:19 · **dirty=true** → 1 건 (`lhsx_001`) · #2 10-01T01:18:27 · **dirty=true** → 63 건 (마지막 02:06:03) |
| 09-29 기준선 runs (대조) | `4b42179ec` · `27933b44e` 둘 다 dirty=false | 같음 |

### 1-3 physics v2 상태 (`coverage_status_physics_v2`, status.json = CSV 194/194 일치)

| | LHS | lhsx |
|---|---|---|
| ok / blank / 기타 | **113 / 17 / 0** | **63 / 1 / 0** |
| blank 사유 | 17/17 = *"AM N 개의 v2 자유 표면 ≤ 0 = 분모 무효 … 이웃 AM–AM v2 면적 합이 표면적 이상 (LHSC-01)"* | 1/1 같은 사유 |
| blank ⇔ `n_free_surface_nonpositive > 0` · 사유 속 N = 열 값 | 0 불일치 | 0 불일치 |
| `n_radius_invalid` · `n_contacts_unknown_id` · `n_contact_failures` | 0 × 130 | 0 × 64 |
| v2 `n_am` = 수확기 AM 개수 | 130/130 | 64/64 |

blank 침대와 무효 AM 수 (전부 bimodal · 첫 사례 AM 반경 = 그 침대의 AM_S):

| LHS 케이스 | 무효 AM | | LHS 케이스 | 무효 AM |
|---|---|---|---|---|
| lhs00_000 | 5 | | lhs00_063 | 1 (r 1.0 µm) |
| lhs00_001 | 14 | | lhs00_074 | 3 |
| lhs00_013 | 1 | | lhs00_076 | 3 |
| lhs00_023 | 12 | | lhs00_080 | 6 |
| lhs00_030 | 2 | | lhs00_082 | 3 (r 1.0 µm) |
| lhs00_034 | 1 | | lhs00_093 | 2 |
| lhs00_050 | 2 | | lhs00_095 | 8 |
| lhs00_053 | 4 | | lhs00_096 | 2 |
| lhs00_098 | 1 | | **합** | **70** |
| **lhsx_009** | 3 (r_AM_S 0.683 µm) | | | |

---

## 2. 옛 ↔ 새 동일성 (새 코드가 바꾸면 안 되는 양)

### 2-1 수확기 JSON — 기존 키 전부

| | LHS | lhsx |
|---|---|---|
| 옛 JSON 의 고유 평탄 키 | 247 | 246 |
| 비교 칸 (키 × 케이스) | 30,446 | 14,956 |
| 정확 일치 | 30,277 | 14,892 |
| 비동일 | **169** = `wall_touch_rule` 문자열 130 + `wall_touch` 값 39 | **64** = `wall_touch_rule` 문자열만 |
| 옛에만 있는 키 · 사라진 케이스 | 0 · 0 | 0 · 0 |
| 새 키 (고유) | 448 = `coverage_wall_split` 296 · `contact_area_check` 126 · `coverage_wallexcl_detail` 10 · `contact_gate` 8 · 벽 제외 pct/status 8 | 같음 |

정확 일치 (max |Δ| = **0**, 부동소수 잡음도 없음) 인 대표 양 — 130/64 전부:
`phi_se` · `phi_am` · `porosity_sphere_pct_RECORD_ONLY` · `handover_qc.*` (porosity 3 변형 · 두께 `thickness_wall_gap_um` · pushback · envelope · 벽 밖 부피 · sha 4) · `phase_counts.*` · `plate_z_sim` · `H_sim` · `V_box_sim` · `coverage_AM_{P,S,total,only}_hertz_pct` + status · `coverage_detail.*` · `tortuosity_dijkstra_SE` (밴드 τ) · `tortuosity_dijkstra_SE_wall` (벽 τ) · `tau_detail.*` · `tau_wall_detail.*` · `wall_record.*` (floor · plate · pushback · clipped) · `boundary_qc.*` · `contact_scan.*` · `deck_floor.*` · `raw.*`.

### 2-2 `wall_touch` 변경 = 벽 규칙 통일 (item 4 · 의도된 변경)

규칙: 옛 `z − r ≤ z_floor · z + r ≥ plate_z` (접선 포함) → 새 `깊이 r − (plate_z − z) > 0` (접선 = 깊이 0 은 비접촉) — `wall_record` · `wall_touch` · 벽 분할이 한 함수 `_wall_contact`.

| 침대 | 벽 · 상 | 옛 n_plate → 새 | 상 입자 수 |
|---|---|---|---|
| lhs00_001 | plate · AM_S | 746 → 742 (−4) | 39,728 |
| lhs00_004 | plate · AM_S | 61 → 60 | 2,476 |
| lhs00_021 | plate · AM_S | 151 → 150 | 3,722 |
| lhs00_053 | plate · AM_S | 1,393 → 1,391 (−2) | 59,647 |
| lhs00_063 | plate · AM_S | 34 → 33 | 1,244 |
| lhs00_074 | plate · AM_S | 1,170 → 1,169 | 59,666 |
| lhs00_083 | plate · SE | 664 → 663 | 12,564 |
| lhsx 64 | — | 변경 0 | |

- 바닥 쪽 변경 0 · 합 = AM_S 10 + SE 1 = **11 입자** (각 침대 `AM` 합계 칸도 같은 만큼).
- 새 `wall_touch` = 새 `wall_record.n_touch_by_phase` : **194/194 일치**. 옛 JSON 에서는 13 칸 (7 침대) 불일치 → 이번에 사라짐.
- `either` · `plate` 비율 최대 변화 = 1/N_phase (예 lhs00_063 AM_S plate 2.733 % → 2.653 %).
- 벽 제외 피복률 값에는 무영향 (접선 입자의 cap = 2πr·clip(0) = 0) · 영향은 벽 분할 **분류**와 비율뿐.

### 2-3 웹앱 `metrics_flat.csv` — 공통 열 전부

| | LHS | lhsx |
|---|---|---|
| 행 (옛 · 새) | 130 · 130 | 64 · 64 |
| 공통 열 | 232 | 231 |
| 130/64 행 모두 문자열 동일 | **232/232** | **231/231** |
| 옛에만 있는 열 | 0 | 0 |
| 새 열 | 82 = 7a AM–SE CN 분포 3 + legacy Physics 40 + physics v2 39 | 82 |

비교한 공통 열 묶음 (전부 Δ = 0): porosity (ε_sphere) 1 · 두께 `thickness_um` · `plate_z_source` · φ_SE/φ_AM · 상 개수 `n_AM_P/n_AM_S/n_SE` · 계면 개수 `area_<쌍>_n` 7 · 계면 면적 `area_<쌍>_total/mean` 14 · SE–SE CN 10 (`se_se_cn*` · `_perc` · `_eff_area` · `_aug*`) · AM–AM CN 2 + `am_am_n_contacts/mean_area/total_area` · AM–SE CN (`am_se_cn_mean` · `_surface_weighted` · 상별 mean/std/median/max) · 퍼콜레이션 (`percolation_pct` · `top_reachable_pct` · `ionic_active_pct` · `n_components` · `n_large_components`) · Hertz 계열 피복 `coverage_AM_{P,S}_{mean,std}` · τ 5 (`tortuosity_*`) · 파괴·힘 (`n_*_AM_AM` · `frac_*` · `fracture_index*` · `fn_*` · `R_min/P_c/F/F_over_Pc_*`) · 응력비 · overlap · 입력 파라미터 (`inp.*`) 등.
status.json 의 case 필드도 `when` · `stop_after` · `stages` · `elapsed_s` 외 전부 동일 (새 필드 = `coverage_status_physics_v2` 하나).

### 2-4 이번 대조로 **평가할 수 없는** 양

| 양 | 이유 |
|---|---|
| porosity **union** | 새 · 옛 수확기 · 웹앱 산출 어디에도 없다 (웹앱 분석기가 union 을 직접 저장하는 ②-a `f3cb141ae` 는 봉인 **이후** 세대). 인계표의 union 열은 별도 데이터 (`docs/data/lhs_union_20260927`) |
| legacy **Physics** 피복 (`*_physics`, `_rough`, `A_binding_share_*`, `path_*_physics`) | 옛 기준선 = `--stop-after contact` (coverage 단계 없음) → 새 배치에만 있다. 커밋된 LHS/lhsx 옛 값 없음 (`case_master.csv` · `design_performance_corpus.csv` 에 LHS 행 0) |

---

## 3. 새 양의 분포

### 3-1 피복률 계열 (케이스 수 | 최소 | 중앙 | 최대, %)

| 계열 · 열 | LHS | lhsx |
|---|---|---|
| Hertz-geom (c_cpl[22]) AM_P — 웹앱 `coverage_AM_P_mean` ¹ | 110 \| 2.312 \| 21.678 \| 49.173 | 52 \| 39.893 \| 52.777 \| 63.100 |
| Hertz-geom AM_S — 웹앱 `coverage_AM_S_mean` ¹ | 120 \| 2.534 \| 22.740 \| 50.048 | 60 \| 37.929 \| 52.232 \| 61.278 |
| Hertz-geom AM 전체 — 수확기 `coverage_AM_total_hertz_pct` | 130 \| 2.439 \| 21.433 \| 50.007 | 64 \| 37.932 \| 52.542 \| 61.429 |
| 벽 제외 AM 전체 — 수확기 `coverage_AM_total_wallexcl_pct` (새) | 130 \| 2.763 \| 21.918 \| 50.497 | 64 \| 38.208 \| 53.031 \| 62.477 |
| 벽 제외 AM_P · AM_S · AM(mono) (새) | 100 \| 2.629 \| 22.795 \| 49.916 · 100 \| 2.865 \| 24.281 \| 50.522 · 30 \| 2.975 \| 19.683 \| 48.223 | 48 \| 40.824 \| 53.455 \| 63.806 · 48 \| 38.204 \| 51.728 \| 61.740 · 16 \| 46.935 \| 55.658 \| 62.477 |
| Δ(벽 제외 − Hertz) AM 전체, %p | 130 \| 0.016 \| 0.428 \| 2.111 (음수 0) | 64 \| 0.122 \| 0.445 \| 2.163 (음수 0) |
| legacy Physics AM_P `coverage_AM_P_mean_physics` ¹ | 110 \| 5.500 \| 68.163 \| 100 | 52 \| 99.907 \| 100 \| 100 |
| legacy Physics AM_S ¹ | 120 \| 6.230 \| 74.782 \| 100 | 60 \| 96.575 \| 100 \| 100 |
| legacy Physics AM 전체 `coverage_AM_mean_physics` | 130 \| 5.916 \| 73.529 \| 100 | 64 \| 96.580 \| 100 \| 100 |
| legacy Physics rough AM 전체 | 130 \| 4.165 \| 67.006 \| 99.982 | 64 \| 95.259 \| 99.996 \| 100 |
| physics v2 AM_P (후보) | 93 \| 5.792 \| 72.729 \| 100 | 51 \| 100 \| 100 \| 100 |
| physics v2 AM_S (후보) | 103 \| 6.707 \| 82.159 \| 100 | 59 \| 96.772 \| 100 \| 100 |
| physics v2 AM 전체 (후보) | 113 \| 6.214 \| 78.116 \| 100 | 63 \| 96.777 \| 100 \| 100 |
| Δ(v2 − legacy Physics) AM 전체, %p | 113 \| 0 \| +1.227 \| +3.327 (음수 0 · 0 인 침대 2) | 63 \| 0 \| 0 \| +0.197 (0 인 침대 41) |
| Δ(legacy Physics − Hertz) AM_P / AM_S, %p | 110 \| 3.19 \| 45.82 \| 67.12 / 120 \| 3.70 \| 51.92 \| 63.80 | 52 \| 36.90 \| 47.22 \| 60.11 / 60 \| 38.72 \| 47.75 \| 58.65 |

¹ 웹앱 상별 열은 mono 를 **반지름 이름**으로 싣는다 (LHS mono 30 = AM_S 이름 20 · AM_P 이름 10 · lhsx 16 = 12 · 4 · `wa_mono_phase_name_webapp`). 수확기 상별 열은 bimodal 만 (100/48), mono 는 `AM_only`.

- v2 ≥ legacy 가 항상 성립하는 이유 (코드 확인): legacy Physics 분모는 `4πr² − ΣA_LIGG(AM–AM)` (기하 면적 · `max(…, 0)`), v2 분모는 `4πr² − ΣA_v2(AM–AM)` (Physics 크기 면적 · "분자와 같은 장부") → v2 분모가 작다 → 피복 ↑, 그리고 같은 이유로 작은 AM_S 에서 분모 ≤ 0 → 침대 빈칸.
- 면적 비 v2 / legacy Physics (ok 침대): AM–SE LHS 0.983–1.000 (중앙 0.9999) · lhsx 0.9999–1.000 · SE–SE LHS 0.982–1.000 · lhsx 0.9998–1.000 · **AM–AM** LHS 0.970–0.998 (중앙 0.994) · lhsx **0.896**–0.998 (중앙 0.966).
- legacy Physics / Hertz-geom 면적 비: AM–SE LHS 2.41–4.28 (중앙 3.46) · lhsx 3.23–4.19 · SE–SE LHS 3.08–4.24 · lhsx 4.00–4.30.
- ⚠ **lhsx (SE-rich 0.50) 는 Physics 두 계열 모두 포화**: v2 에서 AM 전부가 100 % 로 잘린 침대 **41/64**, ≥ 99 % 인 침대 54/64 · legacy 중앙 100 % → 판별력 없음. Hertz-geom 과 벽 제외는 38–64 % 범위로 살아 있다.

### 3-2 physics v2 진단 열 (ok 침대 · 자기일관 검사)

| 열 | LHS (n \| 최소 \| 중앙 \| 최대) | lhsx |
|---|---|---|
| `n_contacts_physics_v2` | 113 \| 4,616 \| 93,255 \| 414,748 | 63 \| 53,623 \| 185,490 \| 619,716 |
| elastic 가지 (δ/R* < onset) 비율 % | 0.019 \| 0.084 \| 3.617 | 0.0026 \| 0.019 \| 0.077 |
| volume-cap 가지 비율 % | 0.395 \| 3.03 \| 52.34 | 0.364 \| 1.00 \| 4.04 |
| `cap_conflict_frac_physics_v2` | 0.0179 \| 0.0479 \| **0.623** | 0.0145 \| 0.0184 \| 0.0451 |
| AM 100 % 클립 비율 (`n_coverage_clipped_100/n_am`, 전 침대) | 130 \| 0 \| 28.5 % \| 100 % (≥99 % 침대 14 · =100 % 2) | 64 \| 86.1 % \| **100 %** \| 100 % |
| `h_film_sim_physics_v2` | 5e-06 상수 | 5e-06 상수 |

항등식 (ok 침대 전부 0 위반): Σ binding 가지 (elastic+tabor+volume+geom+none) = `n_contacts` · Σ 쌍별 cap 충돌 = `cap_conflict_n` · `cap_conflict_frac` = n/n_contacts (1e-6) · `n_cap_branch` = n_contacts − elastic · v2 접촉 수 = legacy `A_binding_total_n_contacts` = 접촉 덤프 행 수 (194/194). `none` 가지 = 0 전부.

cap 충돌 상위 (LHS): lhs00_123 0.623 (mono · AM 95 % · r_SE 0.5) · lhs00_020 0.565 · lhs00_062 0.370 · lhs00_128 0.331 · lhs00_018 0.266 — 10 % 초과 25/113 · AM 95 % 침대 16 중 13 · volume-cap 비율과 상관 r = 0.943 · am_pct 와 r = 0.628.

### 3-3 벽 분할 (수확기 `coverage_wall_split`, 어느 벽이든 심한 쪽 · AM 만)

| 분류 | LHS AM 수 | lhsx AM 수 | LHS (케이스 × 상) 묶음 평균 피복의 중앙 · 벽 제외 · 가린 면 | lhsx |
|---|---|---|---|---|
| interior | 1,110,464 | 125,751 | 22.38 % · 22.38 % · 0 | 53.84 · 53.84 · 0 |
| touch | 73,740 | 9,584 | 19.10 % · 22.26 % · 10.5 % | 46.59 · 50.57 · 7.7 % |
| center_out | 602 (37 침대) | 15 (8 침대) | 0 % · 0 % (최대 **100 %**) · 99 % | 0.089 · 9.34 (최대 31.6) · 99 % |
| fully_out | 18 (9 침대) | 4 (2 침대) | 0.248 % · 제외 · 100 % | 0.334 · 제외 · 100 % |
| 합 | 1,184,824 (= v2 n_am 합) | 135,354 (= v2 n_am 합) | | |

- 벽 제외 분모 ≤ 0 으로 빠진 AM (`coverage_wallexcl_detail.n_free_surface_invalid`) = fully_out 과 정확히 같다: LHS 18 AM / 9 침대 (최대 lhs00_098 5 · AM 의 ≤ 0.050 %) · lhsx 4 AM / 2 침대 (lhsx_006 3 · lhsx_009 1 · ≤ 0.020 %).
- `n_capped` (벽 제외): lhs00_004 한 건 = center_out AM_S 1 개가 원 피복 0.72 % → 벽 제외 **100 %** (가려지지 않은 면 ≈ 1 % 에 SE 가 닿음). 오늘 식 `n_capped` 는 0 × 194.

### 3-4 면적 대조 (item 2 · `contact_area_check`, 진단 전용)

| | LHS | lhsx |
|---|---|---|
| 행 (= 비교 · 시험) | 18,111,468 (AM–AM 3,158,862 · AM–SE 6,122,169 · SE–SE 8,830,437 · 주기 플래그 691,370 = 3.8 %) | 14,694,721 (150,033 · 2,328,336 · 12,216,352 · 주기 475,147 = 3.2 %) |
| 초과 · 미인증 · 음수 · 0 면적 · 경계 가지 · 하한 0 · 넓은 포괄 | 0 · 0 · 0 · 0 · 0 · 0 · 0 | 전부 0 |
| 1 % 검출 보증 `n_detect_1pct` | 전 행 | 전 행 |
| 6 유효숫자 초과 토큰 (면적 · δ · 반경) · 고아 · 비유한 | 0 · 0 · 0 · 0 · 0 | 0 |
| rel_diff_max (침대별) | 6.15e-6 … 9.77e-6 (중앙 7.72e-6) | 6.29e-6 … 9.09e-6 |
| producer_bound_rel_max | 최대 3.19e-4 | 최대 2.78e-9 |
| status · pin | OK 130 · `installed_build_pinned` **False 130** · 소스 해시 로컬 확인 True 130 · sha `71c4d3b5…` | OK 64 · False 64 · True 64 · 같은 sha |

### 3-5 접촉 문 (item 3 · `contact_gate`) — 194/194

n_dup_pairs 0 · n_dup_rows 0 · n_self_rows 0 · n_orphan_rows 0 · n_orphan_ids 0 · 행 = 고유 쌍 · 행 = contact_scan 행 · δ ≤ 0 행 0 · 프레임 1.

### 3-6 τ (수확기)

| 기준선 | LHS 밴드 τ (`status.tortuosity`) | LHS 벽 τ (`status.tortuosity_wall`) |
|---|---|---|
| 09-19 | OK 14 · NOT_PERCOLATING 116 | — |
| 09-24 · 09-25 | OK 14 · ELECTRODE_BAND_EMPTY 110 · NOT_PERCOLATING 6 | — |
| 09-29 (옛 기준선) | 같음 | **OK 106 · NOT_PERCOLATING 24** |
| **5번** | 같음 (값 비트 동일) | **OK 106 · NOT_PERCOLATING 24** (값 비트 동일) |

| 5번 | LHS | lhsx |
|---|---|---|
| 밴드 τ 상태 · 값 | OK 14 · EMPTY 110 · NOT_PERC 6 · τ 1.318 / 1.471 / 2.040 | OK 31 · EMPTY 30 · NOT_PERC 3 · τ 1.271 / 1.390 / 1.541 |
| 벽 τ 상태 | OK **106** · NOT_PERC 24 (bimodal 83/17 · mono_AM_P 13/2 · mono_AM_S 10/5) | OK **64** · NOT_PERC 0 |
| 벽 τ_mean 최소/중앙/최대 | 1.292 / 1.494 / 4.151 | 1.262 / 1.365 / 1.600 |
| 벽 τ_median | 1.284 / 1.490 / 3.929 | 1.254 / 1.357 / 1.595 |
| n_valid · n_truncated · 성분 | 200 (OK 전부) · 0 · 1 (NOT_PERC 는 0) | 200 · 0 · 1 |
| 규약 | `harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component` 전부 | 같음 |

- 벽 τ 는 **5번에서 새로 생긴 것이 아니다** — 09-29 기준선에 이미 있고 (진단 예측 106/130 과 일치), 5번 값은 그것과 비트 동일. 5번의 τ 변화 = 0.
- LHS NOT_PERC 24 집합 = 웹앱 `se_se_cn_perc` 빈칸 24 = 웹앱 `path_hop_area_mean_physics` 빈칸 24 (**같은 집합**).
- 비관통 24 : lhs00_001 · 012 · 018 · 023 · 026 · 030 · 037 · 041 · 053 · 062 · 074 · 075 · 079 · 082 · 083 · 087 · 093 · 105 · 107 · 108 · 111 · 112 · 126 · 128.

### 3-7 7a AM–SE CN 전체 분포 (웹앱 새 열 · 접촉 단계 값)

| 열 | LHS (최소/중앙/최대) | lhsx |
|---|---|---|
| `am_se_cn_std` | 0.632 / 11.04 / 265.4 | 2.131 / 16.28 / 124.8 |
| `am_se_cn_median` | **0** (lhs00_093) / 16 / 609.5 | 6 / 34.5 / 407 |
| `am_se_cn_max` | 8 / 106.5 / 786 | 20 / 178.5 / 836 |

자기일관: 전체 max = max(상별 max) 194/194 · 전체 median ∈ [상별 median] 194/194 · mono 는 전체 = 단일 상 (median · std) 46/46.

---

## 4. LHSC-07 ~ 10 보고 항목

### 4-1 LHSC-07 (P3 · CLI `--all` 중첩 archive skip · 손상 JSON rc 0)

| 확인 | 결과 |
|---|---|
| 5번이 탄 경로 | `lhs_webapp_batch.py --stop-after coverage` (status `stop_after = coverage` 194/194) — `coverage_physics_vs_hertzian.py --all` CLI 는 **안 탔다** |
| 필수 단계 판정 | "Coverage Physics vs Hertzian" 단계 rc 0 · ok 194/194 · v2 상태 문자열 194/194 가 `ok` 또는 비지 않은 `blank: 사유` (빈 문자열 · `not_run` 0) · 조용한 skip 흔적 없음 |
| 항목 자체 | **평가 불가** — 결함은 직접 CLI 경로 (재귀 발견 뒤 basename · 깊이 1 탐색 · 손상 full_metrics 경고만) 에 있고, 배치 산출물은 그 경로를 실행하지 않는다. 열림 유지 · CLI rc 0 을 완료 증서로 쓰지 말 것 |

### 4-2 LHSC-08 (P3 · 벽 규칙 = 저장 좌표에서 깊이 > 0 · 근접 접선 수 미보고)

| 확인 | 결과 |
|---|---|
| 상 · 벽별 **근접 접선 수** (\|r − z + z_wall\| ≤ 토큰 반올림 반폭 합) | **산출물에 없다** — 수확 JSON · status · CSV 어디에도 해당 필드 없음 (키 검색 tangent/near 0) · 원 atom dump + STL 없이 셀 수 없음 → 원자료에서 세야 함 |
| 정확 접선 (저장값 산술로 깊이 = 0) — 옛 ≤ ↔ 새 > 규칙 차로 역산 | LHS **11 입자 / 7 침대** — 전부 **플래튼** (AM_S 10: lhs00_001 4 · 053 2 · 004 · 021 · 063 · 074 각 1 · SE 1: lhs00_083) · 바닥 0 · lhsx 0 |
| 이 역산의 한계 | 하한일 뿐 — 플래튼 z 는 STL 꼭짓점 z **평균**이라 LHS 35/130 · lhsx 20/64 침대에서 `plate_z_sim` 이 1e-17 급 산술 잔재를 가진다 (예 `0.03396670000000001`). 그 침대에서는 토큰상 접선이 깊이 ±1e-18 로 나와 **잔재 부호**가 분류를 정한다 (역산에 안 잡힘). 정확 접선 7 침대는 전부 plate_z 가 깨끗한 6 유효숫자 |
| STL 정밀도 | 별도 필드 없음 · `plate_z_sim` 값 (6 유효숫자 또는 그 평균 잔재) 로 보아 STL 토큰도 6 유효숫자로 **추정** (확인 아님) |
| 영향 크기 (이번 변경분) | 상별 비율 최대 1/N_phase (lhs00_063 AM_S plate 2.733 → 2.653 %) · 벽 제외 피복 값 영향 0 (cap 높이 0) · 분류 (touch ↔ interior) 만 이동 |
| 분모 0 근처 민감도 실례 | lhs00_004 center_out AM_S 1 개: 원 0.72 % → 벽 제외 100 % (가린 면 ≈ 99 %) — Codex 가 적은 "분모가 0 근처면 민감도 보장 못 함" 의 실측 사례 |

### 4-3 LHSC-09 (P3 · 단일 주기 영상 전제)

| 확인 | 결과 |
|---|---|
| 주기 길이 | 경계 `('pp','pp','ff')` 194/194 · 상자 x·y = 0.05 sim (50 µm) 194/194 (웹앱 덱 판독 `inp.box_x/y` = 수확기 √(V_box/H) · 불일치 0) → 최단 주기 길이 L = 50 µm |
| 최대 가능 반경합 | 덱이 상마다 `radius constant` (monodisperse) → 행의 r1+r2 ≤ 2·r_max. LHS 최대 2·r_max = **15.0 µm** (lhs00_004, r 7.5 µm) · lhsx **14.994 µm** (lhsx_032) |
| 조건 r1+r2 < L/2 = 25 µm | 최대 비 **0.600** (LHS) · **0.5998** (lhsx) → 위반 가능 행 **0 / 18,111,468** · **0 / 14,694,721** — 한 쌍의 두 영상이 동시에 닿는 기하가 불가능 |
| 원자료 쪽 증거 | `contact_gate` 중복 무순서 쌍 0 · 중복 행 0 · 자기쌍 0 (194/194) · 주기 플래그 행 691,370 / 475,147 도 면적 대조 초과 0 |
| 한정 | 행별 반경을 원 dump 에서 다시 센 것이 아니라 **덱 반경의 상한**으로 보인 것 (LIGGGHTS `radius constant` 전제). 64 는 64 자체 값으로 보였다 (130 의 옛 감사 0 건을 옮긴 것 아님) |

### 4-4 LHSC-10 (P3 · v2 = 미검증 후보 연산자)

| 코퍼스 값 | LHS | lhsx |
|---|---|---|
| 침대 빈칸율 (한 AM 무효 → 침대 전체 빈칸) | **17/130 = 13.1 %** | 1/64 = 1.6 % |
| AM 단위 무효 분모율 | 70 / 1,184,824 = **0.0059 %** | 3 / 135,354 = 0.0022 % |
| 빈칸의 설계 집중 | bimodal r_AM_S 0.5 µm **15/20** · 1.0 µm 2/20 · 1.5–2.5 µm 0/60 · mono 0/30 (중앙 am_pct 90 vs ok 80) | lhsx_009 (r_AM_S 0.683 µm) |
| cap 충돌률 (ok 침대, 접촉 대비) | 중앙 4.79 % · 최대 62.3 % · > 10 % 25/113 | 중앙 1.84 % · 최대 4.51 % |
| 100 % 클립률 (AM 대비) | 중앙 28.5 % · 전 AM 클립 침대 2 | 중앙 **100 %** · 전 AM 클립 침대 41/64 |
| 근접 접선 / onset 근처 접촉 수 | **산출물에 없음** — 가지 분할 (elastic = δ/R* < onset: 침대당 12–1,220 개 · 0.019–3.6 %) 만 있고 onset (`DR_YIELD_ONSET` 0.00113) 주변 띠의 수는 없다 | 12–150 개 · 0.0026–0.077 % |
| 라벨 | `rule_physics_v2` 문자열 (194 동일) 은 식만 적고 **"미검증 후보" 표지가 없다** · 상태는 `ok` 뿐 → 표지는 인계 열 사전이 실어야 한다 (CSV 만 보는 소비자는 모른다). 웹앱 **화면**의 후보 표지는 봉인 이후 `90c6c9670` 에서 들어갔고 배치 산출물에는 없다 | 같음 |
| legacy 는 v2 빈칸 침대에서도 계산됨 | `coverage_AM_mean_physics` 130/130 | 64/64 |

해석 한 줄: v2 빈칸은 무작위가 아니라 **가장 작은 AM_S 칸에 몰린 설계 공간 구멍**이고 (v2 가 AM–AM 에도 Physics 크기 면적을 빼기 때문 — §3-1), 인계 열로 쓰면 r_AM_S 0.5 µm 층이 거의 통째로 빠진다. lhsx 에서는 v2 · legacy Physics 모두 포화 (판별력 0).

---

## 5. 이상 · 주의 목록

| # | 등급 | 내용 | 근거 · 권고 |
|---|---|---|---|
| 5-1 | 🔴 출처 | 웹앱 run 의 `dirty = true` — **193/194 케이스** (LHS run #2 129 건 · lhsx 64 건 전부). `dirty` 는 `git status --porcelain --untracked-files=no` (추적 파일만) 이므로 **추적 파일 하나 이상이 `1e09f661d` 와 달랐다** (새 산출 폴더 같은 미추적 파일은 원인이 아님). 깨끗했던 것은 스모크 `lhs00_000` 하나 (23:06:19) — 1 분 뒤 23:07:19 lhsx 스모크부터 dirty. 수확기 JSON 에는 코드 출처 필드가 아예 없다 | 완화: 기존 키 · 공통 열 전부가 깨끗한 커밋 (`4b42179ec` · `27933b44e`) 으로 만든 09-29 값과 비트 동일 · 새 열 항등식 전부 성립. 그래도 새 열 코드 세대는 산출물로 증명 불가. WSL 에서 `git -C ~/dem-audit status --porcelain --untracked-files=no` · `git -C ~/dem-audit diff --stat` 로 무엇이 바뀌었는지 확인 → 코드 파일이면 dirty 런 1 건 (예 `lhs00_001`) 을 깨끗한 트리에서 새 out-dir 로 다시 돌려 행 대조. 추정 후보 (확인 아님): 10-01 커밋 `923ca5c3c` 가 "WSL numpy 2.5.2 에서 수확기 selftest ⑰ 이 1 ULP 로 실패" 를 적는다 — 로컬 선수정이었다면 selftest 코드만 바뀐 것 |
| 5-2 | 🟡 설계 | v2 빈칸 17 = r_AM_S 0.5 µm 칸 편중 (§4-4) | 함수 검토 (LHSC-10) 때 AM–AM 분모 장부 규약을 먼저 |
| 5-3 | 🟡 판별력 | lhsx Physics 두 계열 포화 (v2 전 AM 클립 41/64 · legacy 중앙 100 %) | lhsx 인계 coverage 는 Hertz-geom · 벽 제외만 의미 |
| 5-4 | 🟡 기존 | 웹앱 φ_SE · φ_AM 빈칸 13 (LHS) = 웹앱 τ 빈칸 13 과 같은 집합 (lhs00_001 · 012 · 018 · 023 · 026 · 053 · 062 · 074 · 075 · 083 · 087 · 093 · 126) — `LHS-24 (c)` / `DESC-01` (τ 없으면 φ 안 냄) · 봉인 이후 ②-a `f3cb141ae` 에서 고침 → 5번은 고치기 **전** 세대 | 수확기 φ 는 130/130 있음 (웹앱 − 수확기 \|Δ\| ≤ 1.6e-12 LHS · ≤ 2.8e-12 lhsx) · 세대 섞지 말 것 |
| 5-5 | 🟡 기존 | 웹앱 τ 가 있는데 퍼콜 0 인 침대 11 (lhs00_030 · 037 · 041 · 079 · 082 · 105 · 107 · 108 · 111 · 112 · 128 · τ 1.29–8.10 · `percolation_pct` 0 · 수확기 벽 τ NOT_PERC) — `DESC-02` (τ 가 관통을 보증하지 않음) 의 실례 · 09-29 와 동일 (새 것 아님) | τ 인계는 수확기 벽 τ 로 · 웹앱 τ 를 쓰지 말 것 |
| 5-6 | ⚪ 형식 | CSV 빈 부모 열 3 (`cap_conflict_n_by_pair_physics_v2` · `A_binding_counts_total_physics_v2` · `A_binding_counts_AM_SE_physics_v2` — 자식 `.키` 열이 값을 가짐) · 기존 빈 열 `meta.ps_ratio` · `meta.created` · lhsx `-0.0` 칸 4 (`coverage_AM(_S)_delta_pct_rough`) · 두 코호트 CSV 의 v2 열 **순서**가 다름 (첫 행이 blank 냐 ok 냐) — 열 집합은 같음 | 인계 생성기는 열 이름으로 읽을 것 |
| 5-7 | ⚪ 확인됨 | NaN · inf 칸 0 (두 CSV · 수확 JSON 새 키) · 음수는 정의상 음수인 `*_delta_pct_rough` 뿐 · 수확기 새 키 음수 0 | — |
| 5-8 | ⚪ 세대 | 봉인 뒤 바뀐 코드: `webapp/` (① `a9f310769` · ②-a `f3cb141ae` · ②-b·③ `90c6c9670` = 3 커밋) · 수확기는 selftest 만 (`923ca5c3c`, 계산 무변경). 배치 · coverage · lens · plastic · harvest_batch · export_master_csv · type_map_resolve 는 `1e09f661d` = HEAD | 5번 값 = 봉인 세대 · HEAD 웹앱으로 다시 돌리면 φ · union · 숫자형 등이 달라진다 (의도된 변경) |

---

## 6. 재현 메모

- 수확기 대조: 옛 · 새 JSON 을 재귀 평탄화 (스칼라 목록은 튜플) 후 키 교집합에서 `==`; 변경 키는 케이스 · 값 목록.
- 웹앱 대조: `csv.DictReader` 후 공통 열의 칸 문자열 비교 (숫자 재해석 없이 동일).
- 수확기 ↔ 웹앱: porosity (`porosity` ↔ `porosity_sphere_pct_RECORD_ONLY`) · 두께 (`thickness_um` ↔ `handover_qc.thickness_wall_gap_um`) · φ · 상 개수 · Hertz 피복 (`coverage_AM_{P,S}_mean` ↔ `coverage_AM_{P,S}_hertz_pct` · mono 는 `AM_only`) · sha · contact_scan.
- 인계표 `docs/data/{lhs,lhsx}_handover_20260930.csv` 의 Hertz 피복 · porosity · φ 도 5번 수확기 값과 차이 0 (mono 빈칸 차이는 7b 설계 상 칸 채움 규약).
