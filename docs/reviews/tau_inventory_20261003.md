# τ (굴곡도) 정의 전수 목록 — 2026-10-03 (읽기 전용 인벤토리)

- 리포 `/home/user/Yonghoon-DEM-DFT` · 브랜치 `claude/stoic-knuth-NObVQ` · HEAD `1afd37a9a` · 리포에 쓴 것 0 건.
- 방법: `git grep` 패턴 `tortuos · tau · τ · Dijkstra · Laplace · MacMullin · Bruggeman · formation factor · tau_ · _tau · tortuosity_` 를 `scripts/ · webapp/ (py · html · js) · docs/ · docs/data (CSV · TSV · JSON) · CLAUDE.md · 커밋된 pptx` 전체에 걸고, 이름 필터 없이 나온 식별자 (`tau_*` 150 여 종) 를 하나씩 정의 자리까지 따라갔다.
- 값 범위는 커밋된 CSV · JSON 만 읽었다.  저장되지 않는 τ (웹앱이 화면에서 계산하는 τ_Laplace 등) 는 **커밋된 σ · φ 열로 같은 식을 다시 계산**한 값이고 표에 「(유도)」 로 표시했다.  솔버는 돌리지 않았다.
- 판정 (문헌과 맞는가) 은 하지 않았다.  적은 것은 정의 · 입력 · 소비처 · 값 · 리포 안의 자기모순뿐이다.

---

## 0. 분류 기준과 총수

| 분류 | 정의 | 같은 구조에서의 값 관계 |
|---|---|---|
| (a) 기하 경로비 | τ = L_path / Δz (그래프 최단경로 길이 ÷ 두 끝의 z 차) | 흐름과 무관 |
| (b) 흐름 기반 √형 ("τ²-type") | σ_eff = σ₀·φ/τ² ⇒ τ = √(φ·σ₀/σ_eff) | (b) = √(c) |
| (c) 흐름 기반 선형 ("τ-type", tortuosity factor τ_F) | σ_eff = σ₀·φ/τ ⇒ τ = φ·σ₀/σ_eff | (c) = (b)² · COMSOL 5.6 Eq 6-6 의 τ_F, TauFactor · PyBaMM "tortuosity factor" 와 같은 꼴 |
| (d) 기타 | 경험식 · 파생 비 · 재표지 · 유령 키 · 암묵 τ | — |

**총 27 항목** = 계산 정의 18 [(a) 7 · (b) 6 · (c) 5] + 파생 · 재표지 · 유령 · 암묵 9 [(d)].
(τ 기호를 쓰지만 굴곡도가 아닌 것은 §10 에서 제외 목록으로 따로 적었다.)

---

## 1. 총괄표

| ID | 이름 (대표 키) | 분류 | 정의 (file:line) | 저장 위치 | 주 소비처 | 커밋 자료 값 (파일 · n · 범위) |
|---|---|---|---|---|---|---|
| T01 | τ_Dij 표본판 — `tortuosity_mean` · `_median` · `_std` · `_recommended` · `_use_median` | (a) | `scripts/dem_analysis_core.py:569–651` (호출 `:1330`) | `full_metrics.json` (`scripts/analyze_contacts.py:413–417`) · `network_summary.csv` 행 (`:240–242`) | 웹앱 τ 블록 · σ_brug · C(τ) · σ_thermal Ridge · 등급 · 예측기 · 2D 합성 · 그룹 표 | `docs/data/case_master.csv` mean n=163 1.149–17.49 (중앙 1.484) · LHS `docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv` n=117/130 1.281–8.101 (중앙 1.518) · lhsx 64/64 1.260–1.594 · `docs/data/design_performance_corpus.csv` `tau` n=291 1.149–4.324 |
| T02 | τ_Dij,all — `tortuosity_all_{mean,median,std,n,n_sources,recommended}` | (a) | `scripts/dem_analysis_core.py:654–736` (호출 `:1334`) · 커밋 `e7d2782c3` | `full_metrics.json` (`scripts/analyze_contacts.py:419–424`) · 백필 `scripts/tau_all_backfill.py` | 웹앱 τ 블록 행 · 그룹 표 · 보고서 표 | 커밋 표 없음 (case_master 에 열 없음) · ps45 5 건 1.194–1.235 (서술값, `docs/session_20260923_progress.md:833`) |
| T03 | 수확기 옛 τ (solid_zrange) — `tortuosity_dijkstra_SE` (= `tau_detail.tau_mean`) | (a) | `scripts/lhs_descriptor_harvest.py:1249–1358` → `_tau_sample` `:1361–1416` | 수확 JSON `tau_detail` · 설계 CSV | 설계 CSV (값) · 인계표에는 진단 열만 (값 보류 `scripts/lhs_design_dataset.py:739–742`) | `docs/data/lhs_design_20260818.csv` n=14/130 1.318–2.040 · `docs/data/lhsx_descriptors_cov_1e09f661d/` n=31/64 1.271–1.541 |
| T04 | 수확기 벽 τ — `tortuosity_SE_wall` · `_median` · `_status` · `tau_wall_*` | (a) | 같은 함수의 벽 밴드 `scripts/lhs_descriptor_harvest.py:1334–1350` + `_tau_sample` · 규약 문자열 `:229` | 수확 JSON `tau_wall_detail` | 인계표 · 배포 v1 · v1.1 · 10-21 덱 G5a | 인계 · 배포 130: n=106 1.292–4.151 (중앙 1.494) · 64: n=64 1.262–1.600 (1.365) · `_median` 1.284–3.929 · ps45 n=5 1.239–1.289 · 절단 수 0 |
| T05 | 뷰어 경로 τ — `se_clusters.json` `paths[].tortuosity` | (a) | `scripts/analyze_contacts.py:628–718` | 케이스 폴더 JSON (커밋 없음) | `webapp/static/js/viewer3d.js:1768` · 같은 경로에서 `gb_density_mean` · `path_*` 파생 (`:735–753`) | 커밋 없음 |
| T06 | 뷰어 legacy 경로 τ — `tortuosity_paths.json` | (a) | `scripts/analyze_contacts.py:808–841` | 케이스 폴더 JSON | `webapp/app.py:8375` · `:10722` (경로 서빙) | 커밋 없음 |
| T07 | τ_Dij_R (저항 가중 최단경로) · v59 proxy | (a)* | `scripts/physics_fit_v60_tau_R_real.py:78–199` · proxy `scripts/physics_fit_v59_tau_3way.py:76–82` | 미커밋 산출 | 오프라인 탐색 (CLAUDE.md:1783 "NO improvement") | 커밋 없음 |
| T08 | τ_Lap_eff (웹앱) — Hertz 열 · Physics 열 | (b) | `webapp/app.py:2605–2612` · `:2741–2746` | 저장 안 함 (표시할 때 계산) | 케이스 τ 비교 블록 · 비율 행 | (유도) case_master n=157 Hertz 1.395–60.39 (중앙 2.492) · Physics 1.198–66.34 (3.173) |
| T09 | τ_Lap_geom = τ_Laplace,bulk (웹앱) | (b) | `webapp/app.py:2613–2614` · `:2747–2748` | 저장 안 함 | 같은 블록 | (유도) n=157 0.789–20.80 (중앙 1.206) · **1 미만 26/157** |
| T10 | 등급 τ_Laplace,eff — `__tau_lap_eff` | (b) | `scripts/grade_engine.py:927–935` (σ 선택 `:775–784`) | 등급 축 | 등급 · `grade:<label>` 파라미터 | (유도) n=157 1.198–66.34 (중앙 3.173) |
| T11 | 등급 τ_Laplace,bulk — `__tau_lap_bulk` | (b) | `scripts/grade_engine.py:937–945` | 등급 축 | 등급 | (유도) T09 와 같은 수 (σ₀ 3.0) |
| T12 | COMSOL 2D 내보내기 `tau_Laplace_eff` (→ COMSOL 이름 `tau_eff`) · `tau_Laplace_bulk` (→ `tau_bulk`) | (b) | `scripts/export_comsol_2d.py:67–79` · `:104–107` | 내보내기 표 | COMSOL 2D 파라미터 | 커밋 산출물 없음 |
| T13 | 오프라인 재계산 계열 (`tau_Lap_eff` · `tau_Lap_geom` regime DB · `tau_L_eff` · `tau_L_geom` · `tau_lap_*` 백필 · `tau_Lap_eff_H` · `tau_eff_H` · `tau_Le_H/P` · `tau_lg`) | (b) | `scripts/build_tau_regime_db.py:43–48,93–95` · `scripts/compare_laplace_dijkstra.py:55–67` · `scripts/tau_all_backfill.py:125–134` · `scripts/physics_fit_v43_real_tau.py:4–8` · `scripts/physics_fit_v53_lasso.py:98` · `scripts/physics_fit_v59_tau_3way.py:57–61` · `scripts/physics_fit_v60_tau_R_real.py:209–212` · `scripts/compare_hertzian_vs_physics.py:59–71` · `scripts/screen_dataset.py:109` · `scripts/verify_case.py:205` | /tmp · 콘솔 · TSV (미커밋) | SI 그림 · 진단 | `docs/db/section7_10case_sweep.csv` `tau_Lap_eff` n=10 1.21–5.16 (생성기 · σ 모드 기록 없음) |
| T14 | STEP3 pore-τ — `step3.pore.tau` | (c) | `scripts/step3_sigma.py:1591–1672` (τ `:1663`) · 호출 `scripts/mpm_webapp_payload.py:2684–2703` | MPM payload | 케이스 STEP3 카드 `webapp/templates/single.html:608–612` · `viewer3d.js:5195,5357,5400,6302` · ML `tau_se` (T23) | `docs/data/sdcp318_sigma_sdcp_sweep/step3_sdcp*.json` n=4 전부 None (ε 1.26 %, D_rel 0) · CLAUDE.md:271–272 서술 1,415 (vox 0.15) → 4.97e9 (0.125) |
| T15 | Track-B τ_full — `step3.trackb.tau_full` | (c) | `scripts/step3_sigma.py:3286–3296` · `scripts/mpm_webapp_payload.py:2481–2506` | payload · `comsol_export` se_domain | COMSOL 하이브리드 패키지 (`scripts/comsol_export.py:404,448`) | 커밋 없음 (selftest 합성값만) |
| T16 | Track-B τ_geo — `step3.trackb.tau_geo` | (c) | `scripts/mpm_webapp_payload.py:2507–2520` | payload · se_domain | κ_dom (`scripts/step3_sigma.py:3298–3319`) | 커밋 없음 |
| T17 | τ_Lap² 계열 — `tau_sq_Lap_eff` · `tau_lap_eff_hertz_sq` · `tau_eff2` · `tau_sq_H/P` · 그림 τ²_Lap,eff | (c) 값 | `scripts/build_tau_regime_db.py:137` · `scripts/tau_all_backfill.py:134` · `scripts/analyze_network_results.py:166` · `scripts/compare_hertzian_vs_physics.py:70–71` · `scripts/plot_tau_regime_si.py:98–100` | /tmp · 콘솔 | SI 문헌 대조 그림 · 진단 | (유도) Hertz n=157 1.945–3646 (중앙 6.212) |
| T18 | 문헌 τ² 앵커 — `tau_ion_sq` · `tau_el_sq` (Minnmann 2021) | (c) 값 | `docs/data/minnmann2021_sigma_tau_porosity.csv` | 자료 | `scripts/plot_tau_regime_si.py:134–139` · `scripts/build_tau_regime_db.py:219–221` · 툴팁 `single.html:1847` | tau_ion_sq n=5 1–34 · tau_el_sq n=4 1–120 |
| T19 | C(τ) logpoly2 (σ_ionic T1 · σ_e Stage 22.5 · 예측기 v12) | (d) | τ 입력 `scripts/generate_comparison_plots.py:4789` · `:6067–6069` · 적합 `:4556–` · `webapp/predictor_engine.py:110–156` | 계수 live 적합 | 스케일링 법칙 · 예측기 | — |
| T20 | σ_brug 비 `sigma_ratio` = φ_SE·f_perc/τ² | (d) [(b) 꼴에 (a) τ] | `scripts/dem_analysis_core.py:1112–1154` (`:1147`) | `full_metrics` `sigma_ratio` · CSV 행 'σ_Bruggeman (mS/cm)' (×3.0, `scripts/analyze_contacts.py:276–278`) | 웹앱 σ_brug 행 · 예측기 `sigma_brug` · 툴팁 | case_master n=163 0–0.491 (중앙 0.128) · 식 재현 157/157 (rel 1e-3) |
| T21 | 네트워크 Bruggeman EMT 의 암묵 τ — `sigma_bruggeman` = φ^1.5 | (d) [암묵 (b) τ = φ^−0.25 · (c) τ_F = φ^−0.5] | `scripts/network_conductivity.py:1119–1125` · `:1167–1168` · `:1184–1185` | `full_metrics` (NET_MERGE_KEYS `webapp/pipeline_service.py:83–97`) | 웹앱 'σ_Bruggeman (mS/cm)' 주입 행 | case_master n=163 0.043–0.580 |
| T22 | 비율 — τ_Lap_eff/τ_Dij · τ_eff/τ_bulk · Le/Lg · Lg/D | (d) | `webapp/app.py:2626–2631,2760–2765` · `scripts/grade_engine.py:947–953` · `scripts/build_tau_regime_db.py:97–99` | 표시 · 등급 | 웹앱 · 등급 · SI 그림 | (유도) 웹앱 τ_Lap_eff_H/τ_Dij n=157 0.508–20.29 (중앙 1.711) · τ_eff_H/τ_bulk 1.76–3.50 (2.01 = √4.04) · 등급 overhead (Stage-E physics) 1.504–3.689 (2.588) |
| T23 | `tau_se` (사이클 대리모델 특징) | (c) 재표지 | `scripts/ml_cycle_surrogate.py:28,86` · `scripts/train_cycle_surrogate.py:223` | 특징 벡터 | ML | — |
| T24 | 예측기 · ML `tau` | (a) 재표지 | `webapp/predictor_engine.py:279–285,327` · `docs/data/design_performance_corpus.csv` `tau` · `scripts/ml_design_structure.py:65` · `webapp/structure_predictor.py:40,68` | 설계 코퍼스 · `docs/data/structure_model.json` | GPR/RF · 설계→구조 Ridge · 웹앱 예측기 | n=291 1.149–4.324 · structure_model `tau` nested R² 0.921 |
| T25 | PyBaMM "Bruggeman coefficient" ← τ | (d) | `webapp/pybamm_predictor.py:30,72` | — | 호출자 없음 (`__main__` `:218` 뿐) | — |
| T26 | 유령 키 (생산자 0) — `tortuosity_electronic_{recommended,mean}` · `tortuosity_lap_eff` · `tau_lap_eff` · `tau_dij` · `tau_dij_R` | (d) | 소비자만: `scripts/generate_comparison_plots.py:6067–6069,6480` · `scripts/electronic_nested_cv.py:187–191` · `scripts/thermal_form_screen.py:115` · `webapp/app.py:2893,2910` · `scripts/refresh_warnings.py:76,92` · `scripts/outlier_feed_report.py:99` · `scripts/build_metrics_db.py:56–58` · `scripts/physics_fit_v41_outlier.py:59–61` | 없음 | σ_e C(τ) 폴백 · 경고 | 커밋 자료 0 건 |
| T27 | formation factor F = σ_eff/σ_in (≤ 1) | (d) | `scripts/network_conductivity.py:13–15` · CLAUDE.md:150 · `docs/reviews/pellet_calib_freeze_20260825.md:144` | 원장 · 리뷰 문서 | 펠릿 · RVE 대조 | — |

`(a)*` = 경로는 저항 가중으로 고르지만 값은 유클리드 길이 ÷ Δz.

---

## 2. 정의 상세

### 2-A. 기하 경로비 (a)

| ID | 그래프 · 간선 | 출발 · 도착 집합 | 쌍 선택 | 길이 | 분모 | 거르기 · 통계 | 비관통 처리 |
|---|---|---|---|---|---|---|---|
| T01 | SE–SE **접촉 덤프** 그래프 (`calc_percolation` `:476–553`) · 간선 가중 = x·y 주기 최소상 중심 거리 (`_periodic_dist` `:558–566`) | 출발 = 바닥 띠 ∩ 관통 성분 (`:592–596`) · 도착 = 위 띠 ∩ top_reachable (`:586`) — 띠 = 중심 z ≤ 2·r_own / z ≥ plate_z − 2·r_own (`:500–503`) · 폴백 L1 15/85 % (`:505–510`) · L2 관측 SE z 범위 (`:516–523`) | 전 (출발 × 도착) 쌍을 `random.seed(42)` shuffle 후 앞 200 (`:611–615`) — 다른 성분 쌍이 예산을 먹는다 (무경로 → 버림) | 최단경로 위 중심 거리 합 (`:620–623`) | 두 입자 중심 z 차 \|Δz\| (`:624`) | 1 ≤ τ < 20 만 (`:629`) · mean · median · std (모집단) · `recommended` = std/mean > 0.5 이면 median (`:642–650`) | **관통 출발이 없으면 top_reachable 성분의 최저 z SE 를 출발로 승격** (`:598–605`) → 비관통에도 유한 τ |
| T02 | T01 과 같은 그래프 · 같은 간선 (`:704–710`) | 출발 = 바닥 띠 ∩ 관통 · 도착 = 위 띠 ∩ 관통 (`:689–690`) | 표본 없음 — 위 띠 관통 SE 전부를 출발로 둔 다중 출발 Dijkstra 한 번 → 각 바닥 SE 의 경로 최단 위쪽 SE (`:695–710`) | 그 최단경로 길이 | 그 짝의 z 차 (z_t − z_s) (`:717`) | 문턱 없음 · Δz ≤ 0 출발만 제외 (`:718–722`) · 같은 recommended 규칙 (`:733–735`) | 관통 성분 없으면 None (`:692–693`) |
| T03 | **원자 좌표 기하** 그래프 d ≤ r_i + r_j (`lhs_perc_extract._pairs_within` `scripts/lhs_perc_extract.py:167–`) · 간선 = 최소상 거리 `_mi_dist` (`:1221–1232`) | 띠 = **고체 (AM ∪ SE) z 범위** 양 끝에서 두께 r_SE,max, 입자 표면 기준 (`:1293–1325`) | **같은 성분 안에서만** 쌍 · `np.random.default_rng(42)` permutation 앞 200 (`:1383–1388`) | 최소상 길이 합 (`:1396–1397`) | \|Δz\| 중심 (`:1398`) | [1, 20) 절단 평균 · median · 무절단 평균 · 절단 수 따로 (`:1406–1415`) | 폴백 없음 · `ELECTRODE_BAND_EMPTY` / `NOT_PERCOLATING` 분리 (`:1351–1357`) |
| T04 | T03 과 같은 그래프 | 띠 = 바닥 벽 z = 0 · 플래튼 plate_z, 두께 r_SE,max, 입자 표면 기준 (`:1334–1340`) | T03 과 같은 `_tau_sample` | 같음 | 같음 | 같음 | 같음 · plate_z 없으면 `PLATE_Z_MISSING` (`:1283–1286`) |
| T05 | T01 그래프 | 관통 클러스터마다 바닥 ∩ 성분 · 위 ∩ 성분 (각 최대 15, seed 42 shuffle) (`:630–635`) | 최대 30 경로 · 오름차순 정렬 후 best 10 · mean 근접 10 · worst 10 (`:699–718`) | 경로 중심 거리 합 (`:665–670`) | \|Δz\| (`:678`) | 2 자리 반올림 · 필터 없음 | 관통 클러스터만 |
| T06 | T01 그래프 | 바닥 ∩ top_reachable · 위 ∩ top_reachable (`:813–814`) | i 번째 ↔ i 번째, 최대 5 (`:816–818`) | 같음 | \|Δz\| | 2 자리 반올림 | 무경로면 건너뜀 |
| T07 | `build_network` (physics) 망 · 간선 가중 `R_total` (`physics_fit_v60…:142–180`) | 관통 성분의 bottom · top (`:150–162`) | seed 42 shuffle 앞 n_pairs (80) | **R 가중 최단경로의** 유클리드 길이 | \|Δz\| (`:183`) | mean · median | 관통 없으면 None · proxy 는 τ_geom × (1 + 0.5·(1 − σ_full_H/σ_bulk)) (`v59:82`) |

### 2-B. 흐름 기반 √형 (b) — 모두 τ = √(φ·σ₀/σ)

| ID | φ (출처 · 규약) | σ₀ | σ (모드) | 단면 정규화 | 식 위치 |
|---|---|---|---|---|---|
| T08 H | `phi_se` = SE 구 부피 합 ÷ (Lx·Ly·plate_z) — **겹침 두 번 셈** (`dem_analysis_core.py:1125–1129`) | `_sigma_grain_context(metrics)` = 3.0 mS/cm × (짝맞는 `temperature_provenance` 배수) · Cronau 없음 (`webapp/app.py:7495–7558`) | `sigma_full_mScm` = 접촉망 FULL (R_bulk + Holm R_c) · Hertz 계열 면적 (c_cpl[22]) · Stage-E 아님 | σ = G_eff·T/A, A = **상자 전 단면** Lx·Ly, T = plate_z (`network_conductivity.py:853–857`) | `app.py:2610` · `:2744` |
| T08 P | 같음 | 같음 | `sigma_full_mScm_physics` (Tabor+volume 면적) | 같음 | `app.py:2611–2612` · `:2745–2746` |
| T09 | 같음 | 같음 | `sigma_bulk_net_mScm` = CONTACT_FREE (R_bulk = (d/2)/(σπr²) 둘, `network_conductivity.py:401–403`) — Hertz ↔ physics 차 ≤ 0.19 % (case_master 157 행) | 같음 | `app.py:2613–2614` · `:2747–2748` |
| T10 | 같음 | **3.0 고정** (`grade_engine.py:932`) | 첫 번째로 있는 것: `sigma_full_mScm_stage_e_physics` → `_physics` → `_stage_e` → raw (`:775–784`) — Stage-E = Cronau(r_SE) · 파괴 계수 · (운전 T) 포함 | 같음 | `grade_engine.py:927–935` |
| T11 | 같음 | 3.0 고정 | `sigma_bulk_net_mScm` | 같음 | `grade_engine.py:937–945` |
| T12 | 같음 | 3.0 (`export_comsol_2d.py:48`) | eff: stage_e_physics → physics → raw (`:68–69`) · bulk: `sigma_bulk_net_mScm` (`:70`) | 같음 | `export_comsol_2d.py:73–79` |
| T13 | 같음 (`phi_se`) | regime DB 3.0 (`build_tau_regime_db.py:28`) · compare = 무차원 σ (`sigma_full` = σ_eff/σ_bulk, `compare_laplace_dijkstra.py:50–67`) · 백필 = 웹앱 함수 (`tau_all_backfill.py:73–82`) · 피팅 스크립트 3.0 | regime DB raw Hertz (`:86–95`) · compare 무차원 FULL · CF · 백필 Hertz · physics · CF · v43 · v53 Hertz · v59 · v60 σ_P (physics) | 같음 | 위 표 T13 행 |

### 2-C. 흐름 기반 선형 (c)

| ID | φ | σ₀ (또는 D₀) | σ_eff | 정규화 | 식 위치 |
|---|---|---|---|---|---|
| T14 | ε_total = 잘린 격자 (z ≤ 두께) 의 모든 void 복셀 분율 · 닫힌 기공 포함 · PTFE 점은 고체로 찍음 (`step3_sigma.py:1633–1643`) | D₀ = 1 (void σ=1, 고체 0) | D_rel = `solve_sigma_z` σ_eff (판 띠 = vox) (`:1648–1650`) | I·L/(A·ΔV), A = **격자 전 단면** nx·ny·vox² (`:1059–1060`), L = z_top | τ = ε/D_rel (`:1663`) — docstring "[tortuosity FACTOR: D_eff = D0·ε/τ]" (`:1596`) |
| T15 | φ_full = 잘린 격자에서 이온 전도상 (σ_i > 0 · 실재) 복셀 분율 (`mpm_webapp_payload.py:2484–2486`) | σ_bulk = 전도상 σ_ion 이 하나일 때 그 값 (STEP3 σ 표 · 선언 온도) · 둘 이상이면 None (`:2489–2505`) | 이온 솔브 `_res3i['sigma_eff']` | 같음 (전 단면) | `tau_from_solve` τ = φ·σ_bulk/σ_eff (`step3_sigma.py:3286–3296`) |
| T16 | φ_geo = 1 − AM 복셀 분율 (`:2517`) | 1 | AM=0 · 나머지 (void 포함) =1 의 잘린 격자 솔브 (`:2513–2516`) | 같음 | 같은 함수 (`:2518`) |
| T17 | T08 · T09 와 같음 | 같음 | 같음 | 같음 | τ² = φ·σ₀/σ (= (c) 값) |
| T18 | Minnmann: φ = 1 − CAM_vol − porosity (14 % 가정) | σ_i,0 (bulk 펠릿 1.6 mS/cm 등) | EIS-TLM | 논문 Eq 4 | `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md:143–150` |

### 2-D. 기타 (d)

| ID | 무엇 | 식 · 입력 | 위치 | 비고 |
|---|---|---|---|---|
| T19 | C(τ) | exp(a + b·ln τ + c·ln²τ), τ = `tortuosity_recommended` → `tortuosity_mean` (σ_ionic T1) · `tortuosity_electronic_*` → SE τ 폴백 (σ_e) · 예측기 v12 는 T24 (mean 우선) | `generate_comparison_plots.py:4789` · `:6067–6069` · `predictor_engine.py:110–156` | σ_ionic 기준 φ > 0.19 · f_p > 0 행만 (`:4790`) |
| T20 | σ_brug/σ_grain | φ_SE (구 부피 합) × f_perc / τ_rec² · 웹앱 행은 ×3.0 (리터럴) | `dem_analysis_core.py:1147` · `analyze_contacts.py:276–278` | case_master 157/157 재현 |
| T21 | Bruggeman EMT | σ_bulk·φ^1.5 · φ = 망 노드 (전 SE) 구 부피 합 ÷ 상자 (`network_conductivity.py:1120–1123`) | `network_conductivity.py:1125` | 암묵 τ: (b) φ^−0.25 · (c) φ^−0.5 (`docs/bruggeman_tortuosity_network_20261002.md:75`) |
| T22 | 비율 | 웹앱 τ_Lap_eff/τ_Dij (τ_Dij = `tortuosity_mean`) · 등급 τ_eff/τ_bulk = √(σ_bulk_net/σ_full) · regime DB Le/D · Le/Lg · Lg/D | 위 표 | §7 I-06 참조 |
| T23 | `tau_se` | = `step3['pore']['tau']` (T14) | `ml_cycle_surrogate.py:86` | §7 I-03 |
| T24 | ML `tau` | `m.get('tortuosity_mean', m.get('tortuosity_recommended', 0))` · τ ≤ 0 또는 τ > 8 이면 행 전체 제외 (`:283–285`) | `predictor_engine.py:279` | 하한 1.0 표기 `structure_predictor.py:68` |
| T25 | PyBaMM | `param["Positive electrode Bruggeman coefficient (electrolyte)"] = tau` — τ 를 지수 b (κ·ε^b) 자리에 넣음 · ε = 기공률 | `pybamm_predictor.py:72` | 호출자 없음 |
| T26 | 유령 키 | 생산자 grep 0 · 커밋 JSON · CSV 0 | 위 표 | §7 I-05 |
| T27 | formation factor | F_e = σ_eff/σ_AM,input (Archie 의 σ_bulk/σ_eff 와 역수) | `network_conductivity.py:15` | τ 와 F = φ/τ_F 관계 |

---

## 3. 이름 · 라벨 원문 (verbatim)

| ID | 위치 | 원문 |
|---|---|---|
| T01 | `scripts/analyze_contacts.py:240–242` | `'Tortuosity mean'` · `'Tortuosity median'` · `'Tortuosity std'` |
| T01 | `webapp/app.py:2088–2090` | `'Tortuosity ⟨τ_Dijkstra⟩ (geodesic)'` · `'Tortuosity median(τ_Dijkstra)'` · `'Tortuosity σ(τ_Dijkstra)'` |
| T01 | `webapp/app.py:2134–2135` | `'τ_Dij (Dijkstra, 기하만)'` → `'τ_Dijkstra — geodesic-only (geometric)'` |
| T01 | `scripts/grade_engine.py:196–199` | `'label': 'τ_Dijkstra (geodesic)'` · `'formula': 'Dijkstra median geodesic tortuosity (geometric path length / z)'` |
| T01 | `webapp/templates/single.html:1819–1823` | title `'Tortuosity (굴곡도) — Dijkstra geodesic'` · formula `'τ_Dij = L_path / L_direct …'` · meaning `'… σ_eff ∝ σ_bulk/τ² 관계 — 단 COMSOL 입력은 Dijkstra 아니라 τ_Lap_eff (GB constriction 포함) 사용 권장. τ_Dij 만 쓰면 실제 저항의 ~3× 과소평가.'` |
| T01 | `webapp/templates/group.html:1429` | `'Tortuosity': '수식: τ = L_path / L_direct … 유효 전도도: σ_eff ∝ 1/τ² → τ 영향이 제곱으로 큼.'` |
| T01 | `webapp/app.py:6705` · `:3908` · `:7302` | `('Tortuosity', '', 'tortuosity_mean', 'SE 네트워크')` · `('Tortuosity', 'tortuosity_mean')` |
| T02 | `webapp/app.py:2136–2137` | `'τ_Dij,all (Dijkstra 전체, 기하만)'` → `'τ_Dijkstra,all — every bottom SE, shortest path to top (geometric)'` |
| T02 | `webapp/templates/single.html:1835` | `'… 같은 침대에서 τ_Dij 와 같거나 작다 (옆 우회가 빠진다) …'` |
| T03 | `scripts/lhs_descriptor_harvest.py:1280` | `tau_convention='harvest_v1/solid_zrange/rSEmax/no_fallback/same_component'` |
| T04 | `scripts/lhs_descriptor_harvest.py:229` | `TAU_WALL_CONVENTION = 'harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component'` |
| T04 | `docs/data/lhs_release_20261001_v11/README.md:98` | `'τ 는 벽 인접 띠에서 선택한 같은 성분의 SE 중심 쌍에 대해, 기하 최단경로 길이를 해당 쌍의 z 방향 중심 간격으로 나눈 값이다. … 수송 τ (tortuosity factor) 가 아니다'` |
| T04 | `docs/report_20261021/build_deck_v2.py:316` · `:325` | `['굴곡도 (벽 기준)', 'τ_wall', '–', '전해질 최단 경로 길이 / 두께']` · `'τ_wall = L_path / L'` |
| T08 | `webapp/app.py:1947` · `:2140–2141` | `'τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)'` → `'τ_Laplace,eff ⭐ — Laplacian + constriction (COMSOL / EIS input)'` |
| T09 | `webapp/app.py:1946` · `:2138–2139` | `'τ_Lap_geom (Laplace, GB 제외)'` → `'τ_Laplace,bulk — Laplacian without constriction'` |
| T09 | `webapp/templates/single.html:1837–1842` | formula `'τ_Lap_geom = √(φ_SE × σ_grain / σ_bulk_net)'` · meaning `'참고 지표. 일반적으로 τ_Dij 의 0.8배 정도 (병렬 경로 덕분에 조금 낮음). COMSOL 입력엔 부적합 (GB 구성력 누락).'` |
| T10 | `scripts/grade_engine.py:164–166` | `'τ_Laplace,eff ⭐ (σ_grain **3.0 고정**)'` · `'√(φ_SE × **3.0** / σ_full)  — Stage E physics 우선, σ_grain 은 **상수 3 mS/cm**'` |
| T11 | `scripts/grade_engine.py:177–180` | `'τ_Laplace,bulk (구조, σ_grain **3.0 고정**)'` · meaning `'Bruggeman 가정 φ^−0.5 ≈ 1.85.  **τ_Dijkstra 와 다른 정량이고 서로의 대체 열이 아니다** (L4-04).'` |
| T12 | `scripts/export_comsol_2d.py:104–109` | `('tau_Laplace_eff', …, 'tau_eff', '★ 3D tortuosity (COMSOL/EIS input) = √(φ·σ_grain/σ_full)')` · `('tau_Laplace_bulk', …, 'tau_bulk', '3D geometric tortuosity (no constriction)')` · `('tau_Dijkstra', …, 'tau_geo', '3D geodesic tortuosity')` |
| T14 | `scripts/mpm_webapp_payload.py:2700–2702` | `'STRUCTURAL pore-diffusion τ (D_eff/D0 = ε/τ, TauFactor 규약, ε_total 기준; 닫힌 기공은 τ를 올림) — SE-망 σ_ionic과 별개 축, 수송 폼 대입 금지; …'` |
| T14 | `webapp/static/js/viewer3d.js:5357` | `'기공(void)상 유효확산 tortuosity (D_eff/D0 = ε/τ) · 구조 지표 — Li⁺ 수송 τ 아님(수송은 SE 접촉망 σ_ion) · …'` |
| T15 · T16 | `scripts/mpm_webapp_payload.py:2470` · `scripts/comsol_export.py:49` | `'tau_convention': 'linear: sigma_eff = sigma_bulk*phi/tau'` |
| T17 | `scripts/tau_all_backfill.py:16` | `'… 웹앱 τ 비교 블록과 같은 식 √(φ_SE · σ_grain / σ) · σ_grain = 웹앱 _sigma_grain_mS_cm — 그 제곱 (tortuosity factor) · CF/FULL.'` |
| T22 | `webapp/app.py:2142–2143` | `'τ_Lap_eff / τ_Dij'` → `'Constriction overhead, τ_Laplace,eff / τ_Dijkstra'` |
| T22 | `webapp/templates/single.html:1850–1853` | title `'τ_Lap_eff / τ_Dij — Dijkstra surrogate factor'` · meaning `'n=56 case median 이 1.76×. …'` |
| T22 | `scripts/grade_engine.py:186–188` | `'Constriction overhead τ_eff/τ_bulk (= √저항비)'` · `'τ_Laplace,eff / τ_Laplace,bulk = **√(σ_bulk_net/σ_full)**'` |
| T24 | `webapp/structure_predictor.py:40` · `webapp/templates/predictor.html:732` | `'tau': ('τ  굴곡도', '')` · `tau: ['τ', 'Tortuosity']` |

**같은 양의 다른 이름 (별칭 묶음)**
- T09 = `τ_Lap_geom` = `τ_Laplace,bulk` = `__tau_lap_bulk` = `tau_lap_bulk` = `tau_Laplace_bulk` (COMSOL 이름 `tau_bulk`) = `τ_Laplace_geom` / `tau_L_geom` = `tau_lg` = regime DB `Lg`.
- T08 = `τ_Lap_eff` = `τ_Laplace,eff` = `tau_lap_eff_h/_p` = `tau_Laplace_eff` (COMSOL 이름 `tau_eff`) = `tau_L_eff` = `tau_Le_H/P` = `tau_eff_H` = `tau_Lap_eff_H` = 경고 코드의 `tau_le` (유령 키로 읽음).
- (c) 값 = T08² = `tau_sq_Lap_eff` = `tau_lap_eff_hertz_sq` = `tau_eff2` = `tau_sq_H/P` = SI 그림 `τ²_Lap,eff` = Minnmann `τ²` (같은 Eq 4 형태).

---

## 4. 소비처 매트릭스

| 소비처 | 쓰는 τ | 키 · 우선순위 | 위치 |
|---|---|---|---|
| σ_ionic T1 스케일링 법칙 C(τ) | T01 | `tortuosity_recommended` → `tortuosity_mean` | `scripts/generate_comparison_plots.py:4789` (+ 그림 경로 `:4600,4678,4984,5107,5185,5301,5331`) |
| σ_e Stage 22.5 C(τ) | T26 → T01 | `tortuosity_electronic_recommended` → `_electronic_mean` → `tortuosity_recommended` → `tortuosity_mean` | `scripts/generate_comparison_plots.py:6067–6069` |
| σ_thermal T1 Ridge | T01 std · median | `tortuosity_std` · `tortuosity_median` | `scripts/generate_comparison_plots.py:6909,6919` |
| 웹앱 예측기 (GPR/RF · v12) | T24 (T01) · 자동 `fm_tortuosity_*` 타깃 | `tortuosity_mean` → `recommended` · τ > 8 행 제외 | `webapp/predictor_engine.py:279–285,344–357` |
| 설계→구조 Ridge | T24 | 코퍼스 `tau` | `scripts/ml_design_structure.py:65` · `docs/data/structure_model.json` |
| 등급 | T10 · T11 · T22 (τ_eff/τ_bulk) · T01 | `tortuosity_recommended` → `mean` | `scripts/grade_engine.py:163–202,925–953` |
| 웹앱 케이스 τ 비교 블록 | T01 (mean) · T02 · T09 · T08 H/P · T22 (τ_Lap_eff/τ_Dij) | `tortuosity_mean` | `webapp/app.py:2593–2631,2733–2765` |
| 웹앱 CSV 행 · 경고 | T01 mean · median · std | — | `scripts/analyze_contacts.py:240–242,517–531` |
| 웹앱 σ_Bruggeman · σ_brug 행 · 툴팁 · MD 보고서 | T20 (T01 recommended) · T21 | `sigma_ratio` · `sigma_bruggeman_mScm` | `scripts/analyze_contacts.py:276–278` · `webapp/app.py:2559–2591,2706–2731,9412–9416` · `single.html:1981–1990,2133–2146` |
| 웹앱 그룹 표 · 파라미터 목록 · 보고서 | T01 mean · T02 | `tortuosity_mean` · `tortuosity_all_mean` | `webapp/app.py:3908–3909,6705–6706,7302–7303,7331–7334` |
| 그룹 그림 percolation_tortuosity | T01 | 그림 = recommended (`:578`) · CSV 내보내기 = mean (`:7426`) | `scripts/generate_comparison_plots.py` |
| 웹앱 경고 (τ_Lap_eff) | T26 (유령) | `tortuosity_lap_eff` · `tau_lap_eff` | `webapp/app.py:2893–2915` · `scripts/refresh_warnings.py:76–95` |
| MPM 뷰어 · STEP3 카드 | T14 · T05 | `step3.pore.tau` · `paths[].tortuosity` | `viewer3d.js:1768,5195,5357,5400,6302` · `single.html:608–612` |
| LHS 인계표 · 배포 v1 · v1.1 | T04 (값) · T03 (진단만) | `tortuosity_SE_wall(_median)` | `scripts/lhs_design_dataset.py:874–895,727–745,953–985,1972–1976` |
| COMSOL 하이브리드 패키지 | T15 · T16 (+ κ_dom) | 선형 규약 | `scripts/comsol_export.py:404,448,620–629` |
| COMSOL 2D 파라미터 표 | T12 + T01 (이름 `tau_geo`) | `tortuosity_recommended` → mean | `scripts/export_comsol_2d.py:104–109` |
| 사이클 대리모델 ML | T23 (= T14) | `step3.pore.tau` | `scripts/ml_cycle_surrogate.py:86` · `scripts/train_cycle_surrogate.py:223` |
| 2D 미세구조 합성 | T01 | recommended → mean → median | `scripts/extract_2d_microstructure.py:583–584,828` |
| SI 그림 · regime DB | T13 · T17 · T18 · T22 | `tortuosity_mean` | `scripts/build_tau_regime_db.py` · `scripts/plot_tau_regime_si.py` |
| 10-21 · 10-01 보고 덱 | T04 · T01 | `tortuosity_SE_wall` | `docs/report_20261021/make_figs.py:109–121` · `build_deck_v2.py:316,325,336` · `docs/report_20261001/build_deck.py:558` |
| PyBaMM (휴면) | T25 | 인자 `tau` | `webapp/pybamm_predictor.py:72` |

---

## 5. 규약 주장 원문 (COMSOL · EIS · 문헌 규약)

참고 기준 (요청서): COMSOL 5.6 Eq 6-6 은 f = ε/τ_F, Bruggeman τ_F = ε^(−1/2) ⇒ COMSOL τ = φσ₀/σ_eff = (리포 √τ)² = (c).

| file:line | 원문 | 대상 τ | 실제 계산 분류 |
|---|---|---|---|
| `webapp/app.py:2606` | `# τ_Lap_eff = √(φ_SE × σ_grain / σ_full) ← COMSOL input (GB 포함)` | T08 | (b) |
| `webapp/app.py:2615` · `:2740` | `'── τ 비교 (Dijkstra vs Laplace, COMSOL input = τ_Lap_eff) ──'` | T08 | (b) |
| `webapp/app.py:2051` | `'── 굴곡도 비교 (Tortuosity — Dijkstra vs Laplacian; COMSOL/EIS input = τ_Laplace,eff) ──'` | T08 | (b) |
| `webapp/app.py:1947` · `:2623` · `:2757` | `'τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)'` | T08 | (b) |
| `webapp/app.py:2141` | `'τ_Laplace,eff ⭐ — Laplacian + constriction (COMSOL / EIS input)'` | T08 | (b) |
| `webapp/templates/single.html:1844` | `title: 'τ_Lap_eff — Laplace effective tortuosity (COMSOL input)'` | T08 | (b) |
| `webapp/templates/single.html:1846` | `'… effective tortuosity — EIS 측정값과 동일 레벨.\n\n⭐ COMSOL 의 σ_catholyte / τ_effective 입력에 사용하는 값.'` | T08 | (b) |
| `webapp/templates/single.html:1847` | `'Minnmann 2021 EIS τ_ion = 2.07 (42 vol% CAM) 와 우리 DEM τ_Lap_eff = 2.10 (input_particulate_11, 42.7 vol% SE) 이 1.4% 오차로 일치 — … 이 값을 COMSOL 에 넣어야 정확한 catholyte 전도 모델 작동.'` | T08 H (확인: case_master 의 이 케이스 Hertz 2.100 · physics 2.369) | (b) |
| `webapp/templates/single.html:1823` | `'… 단 COMSOL 입력은 Dijkstra 아니라 τ_Lap_eff (GB constriction 포함) 사용 권장. …'` | T08 | (b) |
| `webapp/templates/single.html:1841` · `:1852` | `'COMSOL 입력엔 부적합 (GB 구성력 누락).'` · `'Dijkstra geodesic 이 COMSOL-comparable effective τ 대비 얼마나 낮은지.'` | T09 · T22 | (b) |
| `scripts/grade_engine.py:14` | `τ_Laplace,eff ≤ 2.5         — Tippens 2019, Famprikis 2019` | T10 | (b) |
| `scripts/grade_engine.py:167` | `'COMSOL/EIS input tortuosity (Tippens 2019, Famprikis 2019). '` | T10 | (b) |
| `scripts/grade_engine.py:925` | `# τ_Laplace,eff (COMSOL/EIS input) — same formula as webapp/app.py:2026` | T10 | (b) |
| `scripts/export_comsol_2d.py:72` · `:105` | `# τ_Laplace,eff = √(φ_SE × σ_grain / σ_full)  — COMSOL/EIS input` · `'★ 3D tortuosity (COMSOL/EIS input) = √(φ·σ_grain/σ_full)'` | T12 | (b) |
| `scripts/lhs_design_dataset.py:884` (→ 인계 · 배포 열 사전 `lhs_release_20261001_v11_columns.tsv:66` · `lhsx_…:65` · `lhs_handover_20261001_columns.tsv:123`) | `'… COMSOL/EIS 입력 τ 는 τ_Laplace,eff = √(φ_SE·σ_grain/σ_full) (망 단계 · 이 표에 없음) …'` | T08 (예정) | (b) |
| `scripts/lhs_design_dataset.py:3192` · `:3222` | `열 사전 = 기하 최단경로 · 수송 τ 아님 (COMSOL 입력은 τ_Laplace,eff)` (selftest 문자열 강제) | T08 | (b) |
| `docs/data/lhs_release_20261001/README.md:51` | `'**수송 τ 가 아니다** — COMSOL · 유효 전도도 입력용 τ (τ_Laplace) 는 이 표에 없다'` | T08 | (b) |
| `scripts/plot_section7_design_rules.py:106` | `'τ_Laplace,eff — COMSOL/EIS input'` | `section7` CSV 값 | (b) |
| `scripts/physics_fit_v59_tau_3way.py:15–17` | `τ_Lap_eff = √(φ · σ_grain / σ_full) … Standard in continuum models (Newman, Bruggeman, COMSOL).` | T13 | (b) |
| `docs/GRADING_STORY.md:80` | `\| τ_Laplace,eff \| 1.0 \| COMSOL/EIS input \|` | T10 | (b) |
| `docs/bruggeman_tortuosity_network_20261002.md:32` | `\| τ_Laplace,eff \| √(φ_SE · σ_grain / σ_full) \| … — **COMSOL · EIS 입력** \|` | T08 | (b) |
| `docs/stage4_electrochem_research.md:13–15` · `:44` | `PyBaMM option {"transport efficiency": "tortuosity factor"} … (ℬ = ε/τ) **instead of the Bruggeman ε^1.5 guess** every COMSOL user makes.  We have τ_Laplace,eff` · `pv["Positive electrode tortuosity factor (electrolyte)"] = OUR_TAU   # ← τ_Laplace,eff` | T08 → PyBaMM τ_F 자리 | (b) 를 (c) 자리에 |
| CLAUDE.md:25 | `벽 τ = **기하 최단경로 — 수송 τ 아님** (… · COMSOL 입력 τ_Laplace,eff 는 망 단계 = 나중)` | T04 · T08 | (a) · (b) |
| **반대 방향 서술 (리포 자신)** | | | |
| `scripts/step3_sigma.py:3289–3291` | `⚠ 관례 지뢰: build_tau_regime_db._tau_from_sigma 는 √(φ·σ/σ_eff) = **τ² 관례**다.  같은 구조가 선형 τ=4 ↔ √ 관례 2 로 두 배 다르게 읽힌다.  COMSOL 의 tortuosity 입력은 통상 선형(σ_eff = σ·ε/τ) → Track-B export 는 전부 이 함수로 통일하고 관례를 함께 적는다.` | T15 · T16 | (c) |
| `scripts/comsol_export.py:622–629` | `이 패키지의 τ 는 전부 **선형** 관례다 … **같은 물리가 τ = 4 ↔ 2 로 갈린다** — COMSOL Effective transport parameter 에 넣기 전에 그 인터페이스의 τ 정의(1승/2승)를 반드시 확인할 것.` | T15 · T16 | (c) |
| `docs/comsol_trackb_pipeline.md:59–62` | `**선형**: σ_eff = σ_bulk·φ/τ.  build_tau_regime_db 의 √ 는 **τ² 관례** — 같은 해가 τ=4 ↔ 2 로 갈린다.` | T15 · T16 | (c) |
| `docs/stage2_model_audit_vs_literature.md:55` | `**Phase 4 입력 = σ_ionic-anchored 역산** τ = ε·σ_grain/σ_ionic.  그러면 PyBaMM이 σ_eff = σ_grain·ε/τ = σ_ionic을 **정확히 재현**` | (예정) | (c) |
| `docs/seminar_20260806_glossary.md:16–31` · `seminar_20260806.pptx` slide19 | `우리 안에 **두 규약이 공존한다**` · 발표 권고 `σ_eff = σ_bulk · φ / τ (선형 관례 명시)` | — | (c) 권고 |
| **기타 규약 주장** | | | |
| `docs/literature_review_dem_mpm_assb.md:106` | `**TauFactor(Cooper 2016)**: τ=ε·D/D_eff = **우리 τ_Laplace,*bulk***` | T09 ↔ TauFactor | (c) 정의 = (b) 값이라 적음 |
| `scripts/compare_laplace_dijkstra.py:10–12` | `Relation: σ_ratio = ε_SE / τ² (Bruggeman-like, ε = φ_SE for SE-network)` | T13 | (b) |
| `docs/sigma_ionic_physics_derivation.md:352` | `σ_eff = σ_bulk × ε / τ² (Bruggeman) or σ_bulk / τ (Wiedemann–Franz limit).` | T19 의 τ (T01) | (b) · (c) 병기 |
| `docs/pipeline_step1_to_step5_guide.md:611` | `**굴곡도 τ**: 이온이 돌아가는 정도. σ_eff = σ_grain·φ/τ².` | 일반 | (b) |
| `webapp/templates/single.html:1845` | `(σ_grain = … mS/cm, LPSCl bulk MLIP-MD value)` | σ₀ 출처 | — |

---

## 6. 커밋 자료 값 (상세)

### 6-1. 저장된 열

| τ | 파일 | n | min | 중앙 | max | 비고 |
|---|---|---|---|---|---|---|
| T01 `tortuosity_mean` | `docs/data/case_master.csv` | 163 | 1.149 | 1.484 | 17.49 | `use_median` True 2/163 → recommended ≠ mean 2 행 (a9_p02 2.871 vs 2.222 · a9_p06 4.201 vs 4.464) |
| T01 `tortuosity_std` | 같음 | 163 | 0 | 0.108 | 2.418 | 모집단 std |
| T01 `fm__tortuosity_mean` | `docs/case_summary.csv` | 85 | 1.149 | 1.430 | 4.324 | |
| T24 `tau` | `docs/data/design_performance_corpus.csv` | 291 | 1.149 | 1.430 | 4.324 | τ > 8 제외 뒤 |
| T01 `tortuosity_mean` | `docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv` (= `_20260929` · `coverage_1e09f661d` 같은 값) | 117/130 | 1.281 | 1.518 | 8.101 | 비관통 11 행 포함 (§7 I-04) |
| T01 | `docs/data/lhsx_webapp_contact_d1ec42fba/metrics_flat.csv` | 64 | 1.260 | 1.361 | 1.594 | |
| T03 | `docs/data/lhs_design_20260818.csv` | 14/130 | 1.318 | 1.471 | 2.040 | 상태: BAND_EMPTY 110 · NOT_PERC 6 · OK 14 |
| T04 | `docs/data/lhs_handover_20261001.csv` · 배포 v1 · v1.1 | 106/130 | 1.292 | 1.494 | 4.151 | 무절단 평균 = 같은 값 (절단 0) |
| T04 | `docs/data/lhsx_handover_20261001.csv` · 배포 | 64/64 | 1.262 | 1.365 | 1.600 | |
| T04 | ps45 `…/post_fix/ps45_handover.csv` | 5 | 1.239 | 1.255 | 1.289 | |
| T08 표기 | `docs/db/section7_10case_sweep.csv` `tau_Lap_eff` | 10 | 1.21 | 2.695 | 5.16 | σ 모드 기록 없음 |
| T14 | `docs/data/sdcp318_sigma_sdcp_sweep/step3_sdcp{15,50,250,1500}.json` | 4 | — | — | — | 전부 None (비관통 기공) |
| T18 | `docs/data/minnmann2021_sigma_tau_porosity.csv` | 5 · 4 | 1 · 1 | 4.3 · 5.85 | 34 · 120 | `tau_ion_sq` · `tau_el_sq` |
| T20 `sigma_ratio` | case_master | 163 | 0 | 0.128 | 0.491 | |
| T21 `sigma_bruggeman` | case_master | 163 | 0.043 | 0.161 | 0.580 | 무차원 |
| CF/FULL `R_brug_over_full` | case_master | 157 | 3.10 | 4.04 | 12.24 | = (τ_eff_H/τ_geom)² |

### 6-2. 저장 안 되는 τ — 커밋 열로 같은 식 재계산 (유도, case_master n=157)

| 식 | min | p25 | 중앙 | p75 | max |
|---|---|---|---|---|---|
| T08 H √(φ·3.0/σ_full) | 1.395 | 2.068 | 2.492 | 3.627 | 60.39 |
| T08 P √(φ·3.0/σ_full_physics) | 1.198 | 2.550 | 3.173 | 4.428 | 66.34 |
| T09 √(φ·3.0/σ_bulk_net) | 0.789 | 1.080 | 1.206 | 1.573 | 20.80 |
| T10 (stage_e_physics 우선) | 1.198 | 2.550 | 3.173 | 4.428 | 66.34 |
| T17 τ²_H = φ·3.0/σ_full | 1.945 | — | 6.212 | — | 3646 |
| T22 T08H/T01 | 0.508 | 1.372 | 1.711 | 2.098 | 20.29 |
| T22 T09/T01 | 0.275 | 0.688 | 0.801 | 1.028 | 6.988 |
| T08H/T09 (= √(CF/FULL) · 웹앱에 이 행은 없다) | 1.76 | 1.881 | 2.01 | 2.273 | 3.499 |
| T22 등급 overhead T10/T11 | 1.504 | 2.42 | 2.588 | 2.738 | 3.689 |
| T10/T08H | 0.852 | 1.13 | 1.227 | 1.28 | 1.584 |

(25 °C 코퍼스라 σ₀ = 3.0 이 웹앱 함수 값과 같다.  T10 은 Stage-E physics 가 대부분 physics 와 같아 (비 중앙 1.0 · 최소 0.687) T08 P 와 거의 같다.)

### 6-3. 같은 침대에서 T01 ↔ T04 대조 (LHS 130, 커밋 자료 조인)

| 묶음 | n | 결과 |
|---|---|---|
| 둘 다 값 | 106 | T01 mean ÷ T04 mean 중앙 0.9999 (0.925–1.112) · \|차\| 최대 0.214 |
| **T01 만 값 (T04 = NOT_PERCOLATING, percolation_pct 0.0)** | **11** | lhs00_030 1.516 · 037 2.461 · 041 1.291 · 079 8.101 · 082 2.296 · 105 6.159 · 107 1.398 · 108 2.894 · 111 2.552 · 112 3.329 · 128 1.784 |
| 둘 다 없음 | 13 | |
| T04 만 값 | 0 | |

---

## 7. 불일치 목록

| ID | 유형 | 내용 | 근거 (file:line) | 수치 증거 | 원장 |
|---|---|---|---|---|---|
| **I-01** | 규약 라벨 | √형 (b) τ_Lap_eff 를 "COMSOL input" 으로 표기 — 리포 자신은 COMSOL τ 를 선형 (c) 이라 적고, 그 제곱을 "tortuosity factor" 라 부른다 | 주장: §5 표의 √형 COMSOL 주장 행 전부 (`webapp/app.py:2606,2615,2051,2141` · `single.html:1844–1847` · `grade_engine.py:167,925` · `export_comsol_2d.py:72,105` · `lhs_design_dataset.py:884` → 배포 열 사전) · 반대: `step3_sigma.py:3289–3291` · `comsol_export.py:49,622–629` · `tau_all_backfill.py:16` | 코퍼스 중앙 T08H 2.49 ↔ 그 제곱 6.21 (2.5 배) | 등재 없음 |
| **I-02** | 동명이질 (σ · σ₀) | "τ_Laplace,eff" 한 이름에 σ 입력 넷: 웹앱 raw Hertz/physics + T-정합 σ₀ (`app.py:2610–2612`) · 등급 Stage-E physics 우선 + σ₀ 3.0 고정 (`grade_engine.py:932`, `:775–784`) · COMSOL 2D 같은 Stage-E 우선 (`export_comsol_2d.py:68–75`) · regime DB raw Hertz (`build_tau_regime_db.py:95`).  Stage-E σ 는 Cronau(r_SE) · 파괴 계수를 포함하는데 σ₀ 3.0 에는 Cronau 가 없다.  `grade_engine.py:925` 주석 "same formula as webapp/app.py:2026" 은 같은 파일 `:169–173` "앱 표시값과 같은 공식이 아니다" 와 모순 | 위 | 등급/웹앱 Hertz 중앙 1.227 (0.85–1.58, n=157) · particulate_11 2.100 (H) vs 2.369 (등급) | L4-04 (claimed_fixed — 온도 · 라벨만, Stage-E σ 선택 · Cronau 불일치는 미기재) |
| **I-03** | 재표지 | pore-τ (void 확산 τ_F) 가 ML 특징 `tau_se` 로 들어간다 — STEP3 자신이 "수송 폼 대입 금지" | `ml_cycle_surrogate.py:28,86` · `train_cycle_surrogate.py:223` ↔ `step3_sigma.py:1623–1625` · `mpm_webapp_payload.py:2700–2702` | — | 같은 부류의 R_tort 결함은 `docs/defense_review_20260720.md:60` 에서 고쳤다 · ML 쪽은 등재 없음 |
| **I-04** | 정의 ↔ 관통 | 웹앱 T01 이 비관통 침대에 유한 τ — 폴백이 top_reachable 성분 최저 z 를 출발로 승격.  docstring "both percolating" (`dem_analysis_core.py:573`) ↔ 코드 도착 = top ∩ top_reachable (`:586`), 폴백 (`:598–605`) | 위 | LHS 커밋 자료 11/130 (1.29–8.10) · case_master 6/163 (input_2mAh_real_16 · a9_p00/02/06/08/10, 최대 17.49) | DESC-02 verified · **DESC-02W open** · census `case_master_column_census_20260919.tsv` COND_tau |
| **I-05** | 유령 키 | `tortuosity_electronic_*` 생산자 0 → σ_e C(τ) 가 조용히 SE 이온 τ 사용, 그런데 `generate_fitting_report.py:675` 은 "τ = tortuosity_electronic_recommended (전자 경로의 굴곡도)".  `tortuosity_lap_eff`/`tau_lap_eff` 생산자 0 → 경고 `tau_lap_eff_extreme/high` · `tau_ratio_extreme` 이 발화할 수 없다 | `generate_comparison_plots.py:6067–6069,6480` · `webapp/app.py:2893–2915` · `refresh_warnings.py:76–95` · `outlier_feed_report.py:99` · `build_metrics_db.py:56–58` | 커밋 JSON · CSV 0 건 | physics_fit_v41 쪽만 감사 기록 (`docs/data/audit_20260914_gap_r2/wave1_summary.json:216`) · findings 등재 없음 |
| I-06 | 동명이질 (비율) | "Constriction overhead" 가 둘: 웹앱 영문 라벨 = τ_Lap_eff/τ_Dij · 등급 = τ_eff/τ_bulk.  툴팁은 같은 행을 "Dijkstra surrogate factor" 로도 부른다 | `app.py:2142–2143` ↔ `grade_engine.py:185–188` · `single.html:1850` | 중앙 1.711 vs 2.01 (H) / 2.588 (등급) | L4-04 가 "서로의 대체 열이 아니다" 로만 언급 |
| I-07 | 동명이질 (σ_Bruggeman) | 'σ_Bruggeman (mS/cm)' 행이 경로에 따라 T20 (3.0·φ·f_perc/τ_rec², 리터럴 3.0) 또는 T21 (σ_bulk·φ^1.5) — `_has_label` 로 먼저 쓴 쪽이 남는다.  툴팁은 T20 식.  'R_brug (과대추정 배수)' 툴팁은 τ 식 (σ_Bruggeman/σ_ionic) 이라 적지만 값은 CF/FULL.  "3~10× 과대추정" 문구 잔존 (10-02 철회와 모순) | `analyze_contacts.py:276–277` ↔ `app.py:2559–2561,2707–2710` · `single.html:1994–1999,1987,1989,2060,2148` ↔ `dem_analysis_core.py:1115–1117` | T21/T20 비 중앙 1.25 (0.79–9.18, n=157) | L2-07 (키 이름) · 툴팁 미기재 |
| I-08 | 동명이질 (geo/geom) | "geo/geom" 이 셋: τ_Lap_geom (b, CF 망) · Track-B τ_geo (c, AM 장애물 복셀) · COMSOL 2D 파라미터 `tau_geo` = Dijkstra (a).  같은 표에서 `tau_Laplace_bulk` 를 "3D geometric tortuosity" 라 부름 | `app.py:2613` · `mpm_webapp_payload.py:2518–2520` · `export_comsol_2d.py:106–109` | — | 없음 |
| I-09 | 규약 혼용 (Bruggeman 기준) | (b) 축 τ_Laplace,bulk 의 기준을 "Bruggeman φ^−0.5 ≈ 1.85" 로 적음 — (b) 규약에서 Bruggeman 은 φ^−0.25 (리포 문서 · SI 그림 코드).  TauFactor τ (c) 를 τ_Laplace,bulk (b) 와 같다고 적음 | `grade_engine.py:180` ↔ `docs/bruggeman_tortuosity_network_20261002.md:75` · `plot_tau_regime_si.py:159–160` · `docs/literature_review_dem_mpm_assb.md:106` | φ_SE 중앙 0.295: φ^−0.25 = 1.36 · φ^−0.5 = 1.84 | GAP3-37 (그림만 고침) |
| I-10 | 키 선택 (mean ↔ recommended) | 같은 T01 을 법칙 · 등급 · COMSOL 2D 는 recommended 우선, 웹앱 τ 블록 · 비율 · 예측기 · 설계 코퍼스 · 그룹 표는 mean 우선.  같은 그림이 그림 = recommended / CSV = mean.  등급 라벨 "Dijkstra median" 인데 키는 recommended (161/163 = mean) | `generate_comparison_plots.py:4789,578` ↔ `:7426` · `app.py:2600,2738` · `predictor_engine.py:279` · `grade_engine.py:196–199` | 차이 2/163 행 (비관통 폴백 행) | DESC-04 · **DESC-04W open** |
| I-11 | PyBaMM 처방 충돌 | 같은 "Phase 4 τ 입력" 을 문서 하나는 √ τ_Laplace,eff 를 PyBaMM tortuosity factor (c) 자리에, 다른 하나는 선형 τ = ε·σ_grain/σ_ionic 로 적음.  휴면 코드는 τ 를 Bruggeman 지수 자리에 넣음 (ε = 기공률) | `docs/stage4_electrochem_research.md:44` ↔ `docs/stage2_model_audit_vs_literature.md:55` · `webapp/pybamm_predictor.py:72` | — | 없음 |
| I-12 | 분모 서술 | τ_wall 분모를 "두께 L" 로 적은 덱 · v1 README — 실제는 짝의 중심 z 간격 | `docs/report_20261021/build_deck_v2.py:316,325` · `report_20261021_v2.pptx` slide14 · `report_20261001_draft.pptx` slide14 (`τ = L_path / L_z`) · `docs/data/lhs_release_20261001/README.md:51` ↔ `lhs_descriptor_harvest.py:1398–1400` | — | LREL-05 open (v1.1 README 만 정정) |
| I-13 | φ 불일치 | τ_Lap 계열은 구 부피 합 φ (겹침 두 번 셈) — 같은 케이스 화면 · 인계표는 질량 보존 φ (`phi_se_mass_conserving`) 를 나란히 낸다.  인계 열 사전은 τ_Laplace,eff 를 나중에 싣는다면서 φ 정의를 안 적음 | `dem_analysis_core.py:1125–1129` ↔ `:1281–1283` · `app.py:2276` · `lhs_design_dataset.py:884` | T09 < 1 이 26/157 (φ · R_bulk 모델 영향, `docs/bruggeman_tortuosity_network_20261002.md:41–64`) | J20-e (인계 φ 결정) |
| I-14 | 물리 라벨 | 접촉 (Holm 협착) 을 "GB" 로 표기 ('GB 포함/제외') — σ₀ 3.0 이 이미 펠릿 입계를 포함한다는 정본과 어긋남 | `app.py:1946–1947,2140` · `single.html:1822,1841,1846` ↔ `docs/bruggeman_tortuosity_network_20261002.md:95–96` · CLAUDE.md SELF-51 · CL-91 | — | 없음 |
| I-15 | σ₀ 출처 라벨 | 같은 3.0 이 "LPSCl bulk MLIP-MD value" · "LPSCl bulk grain σ (constant)" · "펠릿값 (Cronau 2021 SI S2c)" 로 제각각 | `single.html:1845` · `export_comsol_2d.py:48,94–95` ↔ `build_tau_regime_db.py:28` · `single.html` σ_ionic 툴팁 | — | SELF-51 (원고 표) |
| I-16 | 낡은 수치 | 툴팁 "n=56 case median 1.76×" · "outlier(τ=77 등)" — 계산은 τ ≥ 20 을 버린다 | `single.html:1853` · `:1858` ↔ `dem_analysis_core.py:629` | 지금 1.711 (n=157) · 1.829 (n=85) | 없음 |
| I-17 | 보장 안 된 부등식 | "τ_Dij,all 은 같은 침대에서 τ_Dij 와 같거나 작다" — 정의상 보장 아님 (서로 다른 짝 · 다른 Δz), 시험은 빗 기하 하나 | `single.html:1835` · `docs/bruggeman_tortuosity_network_20261002.md:30` ↔ `webapp/test_tortuosity_all.py:101` | ps45 5 건 3.5–4.3 % 작음 (서술값) | 없음 |
| I-18 | 문헌식 전사 | Minnmann Eq 4 를 τ² = (σ_eff/σ_0)·φ 로 적음 (역수 빠짐) — 같은 문서 다른 줄은 (σ_eff/σ_0)⁻¹·φ | `docs/data/minnmann2021_sigma_tau_porosity.csv:2` · `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md:147` ↔ `:33` | — | 없음 |
| I-19 | 법칙 라벨 표류 | MD 보고서 · 예측기가 σ_ion 생산 법칙을 "v12-clean v3 … C_blend(τ)" (n=57) 로 표기 — 생산 T1 은 다른 밑식 · τ 키도 다름 (mean 우선 · τ ≤ 8) | `app.py:9455–9460` · `predictor_engine.py:88–156,279` ↔ `generate_comparison_plots.py:4457–4468,4789` | — | L5-01 open (τ > 8 행 제외 선별) |
| I-20 | 출처 없는 기준 | 죽은 경고 문구 "Wang 70% CAM 레짐 상당" — Wang 2023 τ 출처 0 건 | `app.py:2897` · `refresh_warnings.py:80` ↔ `plot_tau_regime_si.py:116–129` | — | GAP3-37 |
| I-21 | 정본 서술 (역사 절) | CLAUDE.md 의 8mAh_real_10 설명 "form uses Laplace which over-penalizes" — 코드의 C(τ) 는 Dijkstra τ | CLAUDE.md:2076–2077 (DEPRECATED 절, `:2065`) ↔ `generate_comparison_plots.py:4789` | 이 케이스 τ_Lap_eff_H 3.531 / τ_Dij 1.292 = 2.73 (현행 표 CLAUDE.md:1908 과 일치) | 없음 |
| I-22 | 문서 줄 번호 | 용어집이 인용한 줄 번호가 낡음 (`pipeline_step1_to_step5_guide.md:585` → 지금 611 · `step3_sigma.py:1089` → 지금 3286) | `docs/seminar_20260806_glossary.md:20–21` | — | 없음 |

---

## 8. 원장 · CLAUDE.md 대조

| 원장 ID | 상태 | 요지 | 관련 τ |
|---|---|---|---|
| DESC-01 | verified | τ 실패가 φ 까지 삼킴 → 고침 (`dem_analysis_core.py:1136–1144`) | T01 · T20 |
| DESC-02 | verified | τ 가 관통을 보증 안 함 · 결측이 미퍼콜을 뜻하지 않음 | T01 · T03 |
| DESC-02W | **open** P2 | 웹앱 calc_tortuosity 가 두 반례를 그대로 재현 (배포는 무관) | T01 |
| DESC-04 | claimed_fixed P2 | 이름이 통계량 · 경계 · 절단을 정하지 않음 (수확기 쪽 해결) | T03 · T04 |
| DESC-04W | **open** P3 | 웹앱 τ 이름 · 자동 전환 · 무기록 절단 · 띠 폴백 남음 | T01 |
| HARV-01 | claimed_fixed P1 | 수확기 τ 가 좌표 원점에 의존 (9.66 배) → 최소상 통일 | T03 · T04 |
| LHS-08 | **open** P1 | 옛 τ 130 중 14 · 두 원인 한 값 → 벽 τ 새 열로 공급 | T03 · T04 |
| L4-04 | claimed_fixed P2 | τ 분모 · 온도 · 라벨이 소비자마다 다름 (등급 σ₀ 3.0) — 라벨만 수정 | T08 · T10 · T22 |
| L5-01 | **open** P1 | 예측기가 τ > 8 등으로 행 전체를 버려 σ 로 코호트 선별 | T24 |
| LREL-05 | **open** P2 | README τ 분모 "길 / 두께" 오기 (v1.1 README 정정, 덱 미정정) | T04 |
| GAP3-37 | claimed_fixed P2 | SI 그림 두 참조선 규약 불일치 · α=2.36 출처 없음 | T17 · T18 |
| GAP3-39 | claimed_fixed P1 | SI 그림 생성기 fail-open | T17 |
| DR3-07 | claimed_fixed P2 | vox ≤ 0.125 pore-τ 폐기 (1,415 → 4.97e9) | T14 |
| claims.json | — | **τ 규약을 정하는 CL 항목 없음 · quotation_ban 에 τ 항목 없음** (CL-65 는 문헌 언급뿐) | 전체 |
| 감사 D #97 | M (불일치) | 등급 문턱 "τ_Laplace,eff ≤ 2.5 — Tippens 2019, Famprikis 2019" 는 Famprikis 카드에 없음 (`docs/reviews/citation_root_audit_20260925/audit_D_carded.md:30`) | T10 |

| CLAUDE.md 줄 | 내용 |
|---|---|
| 25 | 벽 τ = 기하 최단경로 — 수송 τ 아님 · 130 OK 106 · 1.29–4.15 · 64 1.26–1.60 · "COMSOL 입력 τ_Laplace,eff 는 망 단계 = 나중" |
| 271–272 | pore-τ 1,415 → 4.97e9 (DR3-07) |
| 289 | shift 팔 오염 4 건 중 "τ_geo crop" — 열림 |
| 1689 | grade 파생 τ_Laplace 를 그룹 비교 파라미터로 노출 |
| 1783 | v59/v60 τ_Dijkstra_R — 개선 없음 |
| 1824 · 1856 · 1992 | σ_ionic T1 의 C(τ) logpoly2 (어느 τ 인지 명시 없음 — 코드는 T01) |
| 1908 | 8mAh_real_10 "τ_Laplace ratio 2.73×" (= T08H/T01) |
| 2076–2077 | (역사 절) "form uses Laplace" — I-21 |
| 2201 · 2213 | σ_thermal T1 특징 `tortuosity_std` · `tortuosity_median` |
| 2303 · 2411 · 2459 | σ_e C(τ) (τ 출처 명시 없음 — 코드는 T26 → T01) |
| 150 | Bazzoun 대비 formation factor 0.388 / 0.973 / 1.235 (T27 용어) |

---

## 9. 리포에 기록된 문헌 τ 규약 (판정 아님 · 문서 원문 기준)

| 문헌 (리포 카드 · 자료) | 리포가 적은 정의 | 분류 | 위치 |
|---|---|---|---|
| Minnmann 2021 JES | τ_i = l_i/l_0 (Eq 3) · τ_i² = (σ_i,eff/σ_i,0)⁻¹·φ_i (Eq 4) · 보고값 = τ² (tortuosity factor) | (a) 정의 + (c) 값 (기호 τ²) | `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md:33,146–147` |
| Bielefeld 2020 | σ_eff,ion = (ε_SE/τ²)·σ_bulk,SE · τ² = (σ_bulk/σ_eff)·ε (Eq 11) · Bruggeman τ² = ε^(−1/2) | (c) 값 (기호 τ²) | `docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:122,497` · `docs/data/bielefeld2020_sigma_binder.csv:25,43` |
| Oh 2026 | τ_ion = ε/(σ_eff/σ) (MacMullin 류) | (c) | `docs/lit_oh2026_bimodal_composite_cathode.md:117,427` · `docs/data/oh2026_bimodal_sigma_porosity.csv:11` |
| Lim 2025 | τ_e = ε_e·D_e/D_e,eff | (c) | `docs/lit_lim2025_virtual_calendering_framework.md:153` |
| Yoo 2026 | τ² = R_ion·A·ε·κ/(2d) | (c) 값 (기호 τ²) | `docs/lit_yoo2026_porosity_gradient_dry_electrode.md:136` |
| Koo 2026 | D_eff = D_int·ε/τ | (c) | `docs/lit_koo2026_swcnt_sheath_thick_electrode.md:406` |
| Lee 2023 | "tortuosity factor 1.31 (geodesic)" | (a) 값에 (c) 이름 | `docs/lit_lee2023_sicspe_digitaltwin_assb.md:387` |
| Huang 2025 | TauFactor 상별 · 방향별 τ | (c) | `docs/data/huang2025_etc_vs_microstructure.csv:4` |
| TauFactor (Cooper 2016) | τ = ε·D/D_eff | (c) | `docs/literature_review_dem_mpm_assb.md:106` · `step3_sigma.py:1592–1596` |
| PyBaMM | "transport efficiency": "tortuosity factor" → ε/τ | (c) | `docs/stage4_electrochem_research.md:13–15,34` |

---

## 10. τ 기호지만 굴곡도가 아닌 것 (제외)

| 이름 | 뜻 | 위치 |
|---|---|---|
| DRT `tau` · `tau_s` · `tau_ct` · `tau_w` | 이완 시간 상수 [s] | `scripts/eis_drt_ica.py` · `webapp/app.py:4978–4992,5205,5259,5347` · `templates/eis.html` |
| `tau_w` · `b_gap_relax` | 시간 상수 | `scripts/step6_surrogate.py:209–218` |
| `tau_x/y/z` | Moulinec–Suquet 분극장 | `scripts/fft_homogenize.py:15–18,193–201` |
| `τ_int` | 적분 상관 시간 | `tools/ionic/msd_diffusive_check.py:335–360` |
| `tau_f` | 고스트 띠 폭 (접촉 감사) | `scripts/lhs_contact_audit.py:448` |
| `tau` (`fit_rint_curve`) | R_int(N) 포화 상수 | `scripts/fit_rint_curve.py:87` |
| `V12_TAU_C` · `tau_c_win` · `tau_c_BL` | C_blend 시그모이드 중심 (T19 의 모수) | `webapp/predictor_engine.py:97–100` · `generate_comparison_plots.py` · `physics_fit_v46–v49` |
| `bruggeman_fallback_fired_any` | Stage-E `fallback_weighted_factor` 표지 (τ 없음) | `scripts/run_network_full_corrections.py:610–613` |

---

## 11. 출발점 검증 (요청서 "verify, don't trust")

| 요청서 출발점 | 확인 결과 |
|---|---|
| `webapp/app.py` 2600–2620 · 2735–2750 의 `tau_lap_eff_h/_p` · `tau_lap_geom` · "COMSOL input" 주석 | 맞다 — 식 `:2610–2614` · `:2744–2748`, 주석 `:2606` |
| `scripts/network_conductivity.py` 의 `tortuosity_mean/median/std` | **아니다** — 이 파일은 τ 를 계산하지 않는다.  정의는 `dem_analysis_core.calc_tortuosity` (`:569–651`), 저장은 `analyze_contacts.py:413–417`.  σ 정규화 `:853–857` (A = Lx·Ly 전 단면 · T = plate_z) 는 맞다 |
| τ_Dij,all (`e7d2782c3` · `tau_all_backfill.py`) | 맞다 — `dem_analysis_core.py:654–736` · 웹앱 행 `app.py:2618–2620,2752–2754` |
| 수확기 벽 τ (`harvest_v3/wall_z0_plate` · "수송 τ 아님") | 맞다 — `lhs_descriptor_harvest.py:229,1334–1350` · 열 사전 `lhs_design_dataset.py:879–885` |
| STEP3 pore-τ · "τ_geo crop" | pore-τ 는 `step3_sigma.pore_tau` (`voxel_conductivity.py` 아님).  "τ_geo crop" 은 Track-B τ_geo 의 잘린 격자 (`mpm_webapp_payload.py:2509–2515`) · CLAUDE.md:289 의 shift 팔 오염 항목 (열림) |
| C(τ) 의 τ 키 | `tortuosity_recommended` → `tortuosity_mean` (`generate_comparison_plots.py:4789`) · σ_e 는 유령 키 → 같은 SE τ |
| grade τ_Laplace 축 · `build_tau_regime_db` · "tortuosity_factor" 이름 | 축 맞다.  `tortuosity_factor` 라는 **키는 코드에 없다** — 문구로만 (`step3_sigma.py:1596` · `tau_all_backfill.py:16` · 배포 README:98,125) · 문헌 CSV 한 행 (`bielefeld2020_sigma_binder.csv:25`) |

---

## 12. 방법 · 한계

- 값 표의 「(유도)」 는 커밋된 `case_master.csv` 의 `phi_se` · `sigma_full_mScm` · `_physics` · `_stage_e_physics` · `sigma_bulk_net_mScm` 로 각 소비처 식을 그대로 계산한 것 (σ₀ = 3.0, 25 °C 코퍼스).  스크립트는 스크래치패드에만 있다 (`tau_cols.py` · `derive_tau.py`).
- T01 ↔ T04 대조는 `docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv` 와 `lhs_handover_20261001.csv` 를 `case`/`case_id` 로 붙였다.
- 케이스 폴더 (`webapp/results/<id>/`) 는 커밋돼 있지 않아 T05 · T06 · T15 · T16 의 실값은 볼 수 없었다.
- `screening_*` · `physics_fit_v*` 오프라인 스크립트 다수는 같은 T01 키를 읽는 소비자라 개별 행으로 나누지 않고 T13 · T19 에 묶었다 (정규식 집계: recommended → mean 형태 65 파일 (`webapp/app.py` 는 두 형태 모두) · mean → recommended 4 파일 (`webapp/predictor_engine.py` · `scripts/hybrid_predictor.py` · `scripts/ml_predictor.py` · `scripts/symbolic_regression.py`) · `tortuosity_mean` 단독 19 파일 · 이 정규식 밖에 recommended 단독 소비자 (`grade_engine.py:196` · `extract_2d_microstructure.py:583` · `section5_validity_filter.py:85,107`) 가 더 있다).
