# τ 판단 메모 적대 리뷰 — 코드 진실 렌즈 (2026-10-03)

- 대상: `docs/reviews/tau_conventions_judgment_v1_20261003.md` (§2 · §3 · §4 · §6 의 file:line 주장 + 지정 (a)–(h))
- 리포: `claude/stoic-knuth-NObVQ` HEAD `1afd37a9a` — **읽기만** (리뷰 뒤 `git status --short` 0 줄).
- 재계산: `scratchpad/rev_code_recalc.py` (커밋된 `docs/data/case_master.csv` 로 n = 157 유도값 전부 재산출) · 메모의 `tau_chain_check.py` · `tau_chain_check2.py` 를 그대로 재실행 (리포 코드 import · 쓰기 0) · 릴리스 · 인계 · 설계 CSV 직접 조인.  솔버 (DEM · MPM) 는 돌리지 않았다.
- 판정: **확인** = 줄이 있고 메모가 말한 그대로 · **부분** = 줄은 맞지만 범위 · 해석 · 근거가 어긋남 · **틀림** · **검증 불가** = 커밋 자료로 못 가림.

## 1. 판정표

| # | 메모 주장 (§) | 판정 | 근거 (file:line · 수치) | 메모에 필요한 수정 |
|---|---|---|---|---|
| **(a) √T 의 "COMSOL/EIS input" 라벨 · selftest** | | | | |
| 1 | §4 TAU-01 · §2 T08 — 웹앱 라벨 `app.py:1947 · 2050–2051 · 2140–2141 · 2606 · 2615 · 2623 · 2740 · 2757 · 9543–9544` | 확인 | 전 줄 실재 · 문구 그대로 ("COMSOL/EIS" · "COMSOL input = τ_Lap_eff" · 툴팁 "COMSOL/EIS에 넣는 핵심 값").  식 `:2610` · `:2744` = √(φ·σ₀/σ_full) | 없음 |
| 2 | §4 TAU-01 — `single.html:1823 · 1841 · 1843–1847 · 1852` | 확인 | :1844 "(COMSOL input)" · :1846 "COMSOL 의 σ_catholyte / τ_effective 입력" · :1847 Minnmann 2.07 ↔ 2.10 "1.4% … parameter-free external validation" · :1845 "LPSCl bulk MLIP-MD value" | 없음 |
| 3 | §4 TAU-01 · TAU-16 — `grade_engine.py:14 · 164–167 · 925` | 확인 | :14 "τ_Laplace,eff ≤ 2.5 — Tippens 2019, Famprikis 2019" · :167 "COMSOL/EIS input tortuosity" · :925 "(COMSOL/EIS input)" · 문턱 [1.8 … 6.0] :165 | 없음 |
| 4 | §2 T12 · TAU-01 — `export_comsol_2d.py:660` README 식 φ 자리 반대 | 확인 | :660 `σ_eff = σ_grain / (φ·tau_eff²)` ↔ 정의 :72–75 τ² = φσ₀/σ_full ⇒ σ_full = φσ₀/τ² (φ 는 분자) | 없음 |
| 5 | §2 T12 "**COMSOL τ_F 칸에 √T**" (정의 결함) | 부분 | τ_eff 를 COMSOL tortuosity · 수송보정 칸에 **배선하는 코드는 없다**: `export_comsol_2d.py:104–105` 는 이름 붙은 파라미터 (`tau_eff`, 설명 "COMSOL/EIS input") 를 표로 낼 뿐이고 README :658–660 은 SE 도메인에 `sigma_i` 를 직접 넣고 tau_eff 는 "검산용".  Track-B `comsol_export.py:49 · 622–629` 는 선형 관례 | "τ_F 칸에 √T" → "COMSOL 파라미터 표에 √T 를 'COMSOL/EIS input' 으로 표기 (자동 배선 없음 — 사용자가 Tortuosity 칸에 넣으면 √T 배 과대) + README 검산식 φ 반대" |
| 6 | §4 TAU-01 — `lhs_design_dataset.py:884` (→ 배포 · 인계 열 사전 TSV) | 부분 | :884 문구 실재.  **커밋 TSV 6 개**가 같은 문구를 담는다: `lhs_handover_20261001_columns.tsv` · `lhsx_handover_20261001_columns.tsv` · 배포 v1 `lhs/lhsx_release_20261001_columns.tsv` · v1.1 `lhs/lhsx_release_20261001_v11_columns.tsv` (git grep "COMSOL/EIS 입력" 각 1) — v1 · v1.1 은 **이미 전달된 배포** (Codex GO 10-01) | 수정 범위에 6 파일 명시 · 전달본은 코드 수정으로 안 고쳐진다 → 배포 정정 (v1.2 또는 정오표) 을 결정 항목으로 |
| 7 | §4 TAU-01 "**3192 · 3222 (selftest 가 옛 문구를 강제)**" | 부분 | :3192 는 **주석**.  강제는 :3222–3223 `chk('㉓b …', '기하 최단경로' in _tm and 'COMSOL' in _tm and 'τ_Laplace' in _tm and 'N/A' in _tm and '200 쌍' in _tm)` — **낱말 두 개 ('COMSOL' · 'τ_Laplace') 존재만** 본다.  √ 식도 "EIS" 도 강제하지 않는다 → "COMSOL Tortuosity 입력 = T (= τ_Laplace,eff²)" 로 고치면 시험 **수정 없이 통과** | "selftest 가 옛 문구를 강제" → "selftest 는 'COMSOL' · 'τ_Laplace' 낱말만 강제 — 새 문구가 둘 중 하나를 빼면 그때 ㉓b 를 먼저 바꾼다" |
| 8 | §4 TAU-01 — `plot_section7_design_rules.py:106` · `docs/bruggeman_tortuosity_network_20261002.md:32` · `docs/stage4_electrochem_research.md:44` · CLAUDE.md:25 | 확인 | 각 줄 문구 실재 (stage4 :44 는 PyBaMM "tortuosity factor (electrolyte)" 칸에 τ_Laplace,eff 를 넣는 **문서** 코드) | 없음 |
| **(b) 한 이름 "τ_Laplace,eff" 에 σ 입력 넷** | | | | |
| 9 | §4 TAU-03 · §2 T10/T12 — 웹앱 raw H/P + T 짝 σ₀ · 등급 Stage-E 우선 + 3.0 · **COMSOL 2D 같음** · regime DB raw H + 3.0 | 부분 | 넷 다 실재: `app.py:2599–2612` + `_sigma_grain_context` :7495 · `grade_engine.py:775–784` (stage_e_physics → physics → **stage_e** → raw) + :932 (3.0) · `export_comsol_2d.py:69–70` (stage_e_physics → physics → raw — **stage_e 단계 없음**) + :48 · `build_tau_regime_db.py:28 · 90 · 95`.  등급 ≠ COMSOL 2D (Hertz Stage-E 만 있는 케이스에서 갈림) | "COMSOL 2D 같음" → "COMSOL 2D 는 등급과 사슬이 한 칸 다르다 (`sigma_full_mScm_stage_e` 없음)" — 변형은 최소 다섯 |
| 10 | §2 T10 · TAU-03 — 등급/웹앱 H 0.852–1.584 (1.227), n = 157 | 확인 | 재계산 0.8516 · 1.227 · 1.584 (n 157).  ★ 단서: `sigma_full_mScm_stage_e_physics` ≠ `_physics` 는 **157 중 1 건** (비 0.687) — 등급 τ = 웹앱 physics τ 가 156/157 | 이 비는 거의 전부 **Hertz ↔ physics 모드 차**이지 Stage-E (Cronau · 파괴) 차가 아님을 적는다 (§0 #5 · T10 근거 문장 정밀화 — 정의 결함 판정 자체는 유지) |
| 11 | §4 TAU-03 (I-02) — `grade_engine.py:925` "same formula as webapp/app.py:2026" ↔ :169 "앱 표시값과 같은 공식이 아니다" | 확인 | 두 줄 실재 · 모순.  덧: `app.py:2026` 은 지금 라벨 별칭 주석 줄 (낡은 줄 번호) | 낡은 줄 번호도 함께 고칠 대상에 |
| 12 | §2 T22 · TAU-08 — 등급 overhead = 분자 Stage-E physics ÷ 분모 raw CF | 확인 | `grade_engine.py:947–953` 이 `__tau_lap_eff` (:929 `_sigma_ionic_effective`) ÷ `__tau_lap_bulk` (:938 raw `sigma_bulk_net_mScm`) — 설명 :187 "√(σ_bulk_net/σ_full)" 과 다름 · 재계산 1.504–3.689 (2.588) | 없음 |
| 13 | §3-1 σ₀ 는 T 에서 약분 (`network_conductivity.py:1156` · `:1226`) | 확인 | 이온 망 `k_weight = 1` (:373) · `sigma_rel = 1` (:399–400) · :1156 `sigma_full_mScm = sigma_full·sigma_bulk·1000` · :1226 `se_material.sigma_grain_S_cm(T)` · `sigma_full`×3 ↔ `_mScm` 최대 상대차 0.11 % (반올림, #M9) | 없음 |
| **(c) CF 가지 T < 1** | | | | |
| 14 | §3-5 — CF 간선 R = d/(σπr²) (`network_conductivity.py:401–403`) | 확인 | :401–402 `R_bulk_i = (d_ij/2)/(σ_rel·k·π·r_i²)` · :403 합 — 반쪽마다 **입자 단면 전체**의 원기둥 | 없음 |
| 15 | §3-5 — T_CF = (4/3)·r·d·N(N−1)/L² → (4/3)(r/d) · 솔버 실측 0.6445 · 0.7413 · T_FULL 2.11–2.18 | 확인 | 손 유도 일치 (σ = G·L/A, `:853–857`, L = plate_z = (N−1)d + 2r · φ 구합 :1119–1123).  재실행: N30 d/r 1.9998 → 0.6445 (식 0.6445) · N30 1.78 → 0.7182 · N120 1.78 → 0.7413 · N120 1.9998 → 0.6612 · T_FULL 2.108 / 2.176 | 없음 |
| 16 | §2 T09 · §3-7 — T_CF < 1 이 26/157 · T_CF 0.62–433 (1.454) · √ 0.789–20.80 (1.206) | 확인 | 재계산 26/157 (input_S_1 · S_2 · particulate_1/4/5/7/10 · 8mAh_3 · 1mAh_2 · 1mAh_100_3/4 · 2mAh_real_4/5 · a5_p00–p10 · a6_p02–p10 · a7_p08/p10) · 0.6218–432.6 (1.454) | 없음 |
| 17 | §3-5 · T09 — T < 1 의 원인 = 원기둥 R_bulk | 확인 (단서) | 26 건 전부 `plate_z_source = mesh` (157/157) → L2 판 높이 과대 원인 아님 · 전부 SE 많음 (φ 0.36–0.69 · overlap_mean 9–23 %).  ⚠ 원인 하나 더: L0 띠 노드 등전위 + 정규화 L = plate_z (#M5) 도 T 를 낮춘다 — 26 건과 나머지의 2r_SE/L 중앙 0.041 vs 0.031 이라 주원인은 아님 | §3-5 에 "띠 끝 효과 (L0 포함) 가 r/L 차수로 같은 방향" 한 줄 |
| **(d) physics σ < Hertz σ · ψ 분모** | | | | |
| 18 | §3-7 — 143/157 에서 σ_P < σ_H · 중앙 비 0.664 | 확인 | 재계산 143/157 · 0.6644 (0.3985–1.379) | 없음 |
| 19 | §3-7 — 탄성 가지 밖 physics 면적 ≥ c_cpl[22] (`plastic_coverage.py:393–395`) 인데 저항이 더 큼 → ψ 분모 (`network_conductivity.py:444`, `L2-01`) 가 주원인 후보 | 확인 (보강 가능) | :395 `A_plastic = max(elastic_area, ligg_val, A_cap)` · 망은 `ligg_area=ca_sim` 전달 (:317–319) · :444 legacy `1/(2σ a_eff ψ)` · 기본 `PSI_PLACEMENT_DEFAULT = PSI_DIVIDE` (:73) · a_eff 가 r_min 에 걸리면 ψ = 0 → R_c = 0 (:446–453, 오히려 σ↑).  커밋 자료: 탄성 가지 몫 `A_binding_share_total_pct.elastic` 최대 0.9 % (중앙 0.1) · CF 는 모드 무관 (≤ 0.19 %) · **협착만 망 σ_P/σ_H = 0.21–0.89 (중앙 0.39, n 43**, `network_dual.ratio_physics_over_hertzian.sigma_constr_net`) | "후보" → "커밋 자료와 정합 (탄성 몫 ≤ 0.9 % · 협착만 비 0.39 · CF 동일)" 으로 근거 추가.  곱 배치 반전은 여전히 [미검증] |
| **(e) LHS-25 — Tabor 힘 · 3 배 기준** | | | | |
| 20 | §6-2 — 코드의 F 는 평형 DEM 힘이 아니라 실제 E 로 다시 만든 힘 | 확인 | `plastic_coverage.py:349` `F_real = (4/3)·E_STAR_AM_SE_REAL·√R*·δ^1.5` · :352 `A_tabor = F_real/H_REAL_SE` · E* = 22.415 GPa (:35–45) · H 0.85 GPa (:40) · δ = DEM 겹침.  피복률 경로도 같은 식 (:538–539) | 없음 |
| 21 | §6-1 — "≈ 3 배" 의 기준 원판 = LIGGGHTS c_cpl[22] 교차 원판 | 확인 | Hertz 피복률 · Hertz 망 모두 `contact_area` = c_cpl[22] (`parse_liggghts.py:56` · `coverage_physics_vs_hertzian.py:456–511` · `dem_analysis_core.py:270–276` · `network_conductivity.py:303 · 353`) · 출처 `lhs_coverage_reasonableness_20261001.md:189 · 246` 실재.  3 배는 **침대 합 비율** (접촉별 비 아님) | 없음 (3 배가 집계 비임은 이미 적혀 있음) |
| 22 | §6-1 — "A_LIGG/A_Hertz = 2 − d/(2r), r 0.5 · δ/R* 0.05 에서 1.9875 배" | **틀림 (표기)** | 메모 §3-5 의 d = **중심 간격**이면 2 − d/(2r) = **1.0125**.  1.9875 는 2 − **δ**/(2r) (δ = 겹침) 일 때만 나온다 (산술 확인).  `parse_liggghts.py:53` 주석이 d 를 겹침 뜻으로 쓴 것을 그대로 옮김 | "2 − δ/(2r) (δ = 겹침)" 으로 · 같은 문서 안 d 두 뜻 제거 |
| 23 | §6-2 — κ ≈ E*_real/E*_DEM ≈ 15 (AM–SE) · ≈ 30 (SE–SE) → 포화 문턱 ≈ 30–60 MPa · "DEM 의 AM 모듈러스 [미확인]" | 부분 | [미확인] 은 **풀린다**: 생산 덱 `youngsModulus peratomtype 1.4e8 1.4e8 0.135e7` (14 덱) · ν 0.25/0.30 → E*_DEM 1.469 / 0.742 GPa → 비 15.3 / 30.2 (Hertz 척도로는 맞음).  그러나 생산 접촉법칙은 **hooke/hysteresis** (`pair_style … hooke/hysteresis` 40 덱 · `dem_perturbation.py:62` "input_real_14 … hooke/hysteresis") — F_DEM = k_n·δ (선형) 이라 κ = F_real/F_DEM ∝ √δ / k_n 으로 **δ 의존**이고 E* 비가 아니다 | "Hertz 근사" → "생산 DEM 은 hooke/hysteresis 라 κ 는 E* 비로 정해지지 않음 — 30–60 MPa 는 Hertz-DEM 가정의 예시값 · C1 실측으로만" · AM 모듈러스 140 GPa (덱 값) 기입.  C1 은 c_cpl[13–15] 힘을 덱 단위계로 일관 환산 (`DESC-03` 길이 · 두께 혼용) 할 것을 명시 |
| **(f) S3 봉인 수치 모듈** | | | | |
| 24 | §4 머리 · §6-5 — `seal_s3_prerun.py:99–100` `NUMERIC_MODULES` 에 두 파일 | 확인 | :99–100 = network_conductivity · plastic_coverage · **audit_constriction_deleted · extract_se_network_diagnostics** (넷) | 넷임을 적는다 (참고) |
| 25 | §4 머리 — "주석 한 줄도 바이트 지문을 바꿔 S3 런 검증에 걸린다" (= 건드리면 안 된다) | 부분 | 기전: `run_s3_psi.verify_code_bundle` (`run_s3_psi.py:243–278`) 이 **봉인 파일의 모듈 sha256 ≠ 지금 트리 · 커밋**이면 그 봉인을 거부.  게이트 selftest (`check_all.sh:234` → ⑫d) 는 **커밋 안 된 (dirty)** 수정만 잡는다.  커밋된 수정을 금지하지 않는다 — 재봉인 (baseline 재계산) 을 강제할 뿐 | "금지" → "바꾸면 S3 봉인을 다시 해야 한다 (봉인 거부) · 게이트는 미커밋만 잡는다" |
| 26 | §4 머리 — "09-28 `c0c2d4f44` 가 이 파일을 바꾼 이력 → 현재 봉인 상태 [미확인]" | 부분 | `plastic_coverage.py` 도 09-29 에 **세 번** 바뀌었다 (`114f5514d` · `00cc8461b` · `d64dd9cdf`) · 봉인 창은 `SEAL_DEADLINE 2026-09-17 23:59 KST` (:40–51) · 리포에 봉인 파일 없음 (`docs/data/s3_prerun_seal.json` 부재 · `s3_preflag_baseline.json` 에 code_bundle 없음) ⇒ 09-17 봉인이 있었다면 **이미 두 모듈 모두 어긋나** 거부 상태 | 근거에 plastic_coverage 3 커밋 추가 · "추가 수정의 한계비용 = 어차피 필요한 재봉인" 을 적고, 봉인 밖 도우미 권고는 유지 |
| **(g) L1 띠 폴백** | | | | |
| 27 | §3-5 덤 — 사슬 하나면 L1 (`network_conductivity.py:230–235`) 이 조용히 켜져 T_CF 0.511 · 0.570 · 0.530 = 21–29 % 낮음 | 확인 | 재실행 0.5113 · 0.5697 · 0.5295 (네 사슬 대비 0.793 · 0.793 · 0.714).  기전 확인: 띠 노드는 source/sink 에 큰 g 로 묶여 등전위 (:620–666) → 띠 사이 결합 23/29 = 0.793 · 85/119 = 0.714 (해석값 일치) · 정규화는 plate_z (:853–857) | 없음 |
| 28 | §5-2 G1 — σ 26–40 % 과대 | 확인 | 1/0.793 = 1.26 · 1/0.714 = 1.40 | 없음 |
| 29 | §3-5 덤 · TAU-14 — `LHS-17` 의 폴백이 σ · T 값도 바꾼다 (새 증거) · LHS 130/130 L0 | 확인 | `LHS-17` 은 영향 열로 `percolation_pct · n_components · electronic_*_fraction · se_se_cn_*_perc` 만 적음 (σ 없음) → 새 증거 맞음.  L0 130/130 · 폴백 0 = 원장 note (09-29 WSL) | 없음 |
| 30 | §3-5 덤 — 역사 코퍼스 폴백 빈도 [미확인] | 검증 불가 | case_master 에 띠 규칙 · n_bottom · n_top 열 없음 (421 열 전수).  L2 의 한 원인 (판 높이 과대) 은 `plate_z_source = mesh` 157/157 로 배제되나 L1 은 못 가림 | 그대로 [미확인] (L2 과대 원인 배제는 추가 가능) |
| **(h) 비관통 침대의 유한 τ_Dij · 유령 키** | | | | |
| 31 | §2 T01 · TAU-05 — 폴백 `dem_analysis_core.py:598–605` · docstring :573 "both percolating" · 도착 :586 | 확인 | :598–605 = 관통 출발 없으면 top_reachable 성분의 최저 z SE 를 출발로 승격 → 비관통에도 유한 τ · :573 · :586 · seed :612 · 200 :615 · [1, 20) :629 | 없음 |
| 32 | §2 T01 — `DESC-02W` case_master 6/163 · LHS 11/130 | 확인 | 재계산: input_2mAh_real_16 · a9_p00/02/06/08/10 (τ 1.71–17.49) · lhs00_030 · 037 · 041 · 079 · 082 · 105 · 107 · 108 · 111 · 112 · 128 (`docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv`) | 없음 |
| 33 | §2 T26 · TAU-06 — 유령 키 `tortuosity_electronic_*` · `tortuosity_lap_eff` · `tau_lap_eff` · `tau_dij` | 확인 | 소비자: `generate_comparison_plots.py:6067–6069 · 6480` · `electronic_nested_cv.py:190` · `generate_fitting_report.py:675` · `app.py:2893 · 2910` · `refresh_warnings.py:76 · 92`.  생산자 0 — 접두 결합 (`'electronic_' +` · f-문자열) 도 0 · 망 결합 (`network_conductivity.py:1305–1318`) · `NET_MERGE_KEYS` (`pipeline_service.py:83–97`) 에 없음 · `physics_fit_v41/v42/v59/v60` 는 지역 dict 에만 씀 | 없음 |
| 34 | §4 TAU-05 — "비관통-SE 6 침대는 σ_e · κ 값이 있어 그 적합에 들어 있을 수 있다 [미확인]" | 부분 | **풀린다**: case_master 열 기준 6/6 이 σ_e Stage 22.5 필터를 **전부 통과** — σ_e 타깃 (`electronic_sigma_full_mScm_stage_e` 0.46–10.7 · 둘 다 fallback 아님) · `_EXCLUDED_NAMES_EL` 25 이름 밖 · φ_AM 0.567–0.608 > 0.30 · am_am_cn · am_am_mean_area · r_AM · electronic_percolating_fraction > 0 · τ > 0 (유령 키 → SE τ, a9_p10 은 17.49) (`generate_comparison_plots.py:6060–6083`).  σ_thermal T1 은 `R_brug_over_full_physics` · `asr_ionic` 결측 (σ_ion 없음) 으로 **이미 빠져 있다** (:6939–6970) | "σ_e 생 적합에 6 행 들어 있음 → TAU-05 는 σ_e 비트 불변을 **깬다** (1저자 결정 필요 확정) · σ_thermal 무영향" 으로 |
| **그 밖 (§2 · §3 · §5 · §6 · §7 스팟 점검)** | | | | |
| 35 | §3-2 · §3-3 표 (Minnmann · Park 띠) | 확인 | 재계산 일치.  φ 0.330 띠만 n 56 · T_P 8.75 (메모 57 · 8.77) — 중심 0.329 로 잡으면 57 · 8.77 (반올림 차) | 띠 중심값 명기 |
| 36 | §3-4 — T/φ^−½ H 3.40 (2.54–6.71) · P 5.42 · √T/τ_Dij 1.711 · 2.09 · √T_CF/τ_Dij 0.80 (0.69–1.03) | 확인 | 재계산 3.401 · 5.424 · 1.711 · 2.091 · 0.8007 (0.688–1.028) | 없음 |
| 37 | §3-6 — φ_SE,mc·L_mc = φ_구합·L_gap (`dem_analysis_core.py:1274–1283`) · L_gap/L_mc LHS 0.898–0.985 (0.959) · lhsx 0.867–0.931 (0.894) · union 비 0.980 | 확인 | 대수 확인 (k = 1 − ε_exact 약분) · 배포 v1.1 CSV 재계산 동일 · case_master 0.9802 | 없음 |
| 38 | §5-2 G5 — "G_eff ≤ 2·Σg (`network_conductivity.py:846`)" | 부분 | :846 은 `if os.environ.get('NETWORK_DEBUG'):` 안의 **출력뿐** (판정 아님).  실제 솔버 관문 = `G_eff > 1.1·Σg` → CG 재시도 → None (:778–818) · `sigma_ratio > 1.5` 거부 (:870–878) | 근거를 :778 · :878 로 · 2·Σg 를 쓰려면 새 도우미의 **새 규칙**이라 적는다 |
| 39 | §6-7 — LHS-26 9 침대 · 반지름 규칙 | 확인 | `type_map_resolve.py:134` (r > `AM_P_RADIUS_CUT_SIM` 0.004 :48 → AM_P) · `coverage_physics_vs_hertzian.py:534` · `dem_analysis_core.py:26–30` (1.40 / 1.10) · `lhs_design_dataset.py:365` · 설계 CSV: lhs00_118 3.0 · 121 4.0 · 124 3.0 · 125 3.5 · 126 2.5 · lhsx_003 3.17 · 017 2.80 · 048 2.72 · 062 3.80 µm (모두 mono_AM_P) | 없음 |
| 40 | §6-3 — 라게르 도구 없음 · pyvoro 미설치 | 확인 | git grep laguerre / radical plane / power diagram / pyvoro 0 · `import pyvoro` 실패 (scipy Voronoi 는 비가중만) | 없음 |
| 41 | §7 — 위상 dead-end LHS 중앙 0.03 % (최대 10.98) · lhsx ≤ 0.04 % · 비관통 SE 몫 중앙 0.27 % · p90 10.2 % · 최대 56.8 % | 확인 | 재계산 0.029 · 10.976 · 0.044 · 56.80.  0.27 · 10.2 는 **하위 분위 규약** (보간 규약이면 0.283 · 10.72) | 분위 규약 한 마디 |
| 42 | §4 TAU-09 — 망 `active_fraction` = 바닥 기준 ↔ `ionic_active_pct` = 위 기준 | 확인 | `network_conductivity.py:999–1021` (bottom_reachable) · `dem_analysis_core.py:741–768` (top_reachable_se) | 없음 |
| 43 | §4 TAU-10 — CLAUDE.md 464 · 1101 · 1123 · 1143 · 1259 · 1310 · 1322 · 1325 · 1356 · 1392 · `mpm3d_compaction.py:19 · 618` | 확인 | 전 줄에 "Minnmann … 10 %" 앵커 문구 실재 (문헌 부재 여부는 이 렌즈 밖) | 없음 |
| 44 | §2 T27 — f_H 3.5e-5–0.356 (0.0467) · docstring `network_conductivity.py:13–15` | 확인 | 재계산 동일 · :14–15 `F_e = σ_eff / σ_AM,input` | 없음 |
| 45 | §2 T14 · T23 · TAU-04 — pore-τ 금지 문구 · ML `tau_se` | 확인 | `step3_sigma.py:1623–1625` "do NOT substitute this τ into the transport forms" · :1663 τ = ε/D_rel · `ml_cycle_surrogate.py:28 · 86` · `train_cycle_surrogate.py:223` | 없음 |
| 46 | §2 T25 · TAU-15 — PyBaMM τ → Bruggeman 지수 자리 | 확인 | `pybamm_predictor.py:70` (공극) · :72 `"Positive electrode Bruggeman coefficient (electrolyte)"] = tau` | 없음 |
| 47 | §4 TAU-16 — "Tippens 2019, Famprikis 2019" 출처 없음 (감사 D #97) | 부분 | `audit_D_carded.md:30` 은 **Famprikis 카드만** 대조 (M) — Tippens 2019 는 감사하지 않았다 | "Famprikis 카드에 없음 · Tippens [미확인]" |
| 48 | §2 T01 · T02 · T04 줄 번호와 값 | 확인 | `dem_analysis_core.py:569–651 · 654–736` · `lhs_descriptor_harvest.py:229 · 1334–1350 · 1361` · T01 LHS 117/130 1.281–8.101 (1.518) · lhsx 64 1.260–1.594 · T04 106 1.292–4.151 (1.494) · 64 1.262–1.600 (1.365) | 없음 |
| 49 | §5-1 — f_mc = f_gap·L_gap/L_mc · T = φ_mc/f_mc = 현행 웹앱 T | 확인 | 대수 = §3-6 항등식 · 솔버 f = `sigma_full` (:857, 무차원 · 8 자리) | 없음 (단 #M9) |

## 2. 메모가 놓친 결함 (코드 렌즈)

| # | 결함 | 근거 | 메모에 넣을 것 |
|---|---|---|---|
| M1 | **웹앱 physics τ 칸이 physics σ 가 없으면 조용히 Hertz 값을 쓴다** (비율 행 `ratio_p` 도) | `app.py:2611–2612` · `2745–2746` `… if sig_full_p and sig_full_p > 0 else tau_lap_eff_h` | §5 physics HOLD · G6 과 충돌 (physics 를 빈칸으로 둔 침대가 화면에선 physics 값처럼 보인다) → TAU 신설 (P2, 시험: physics 키 없는 metrics → physics 칸 "—") · J20-l 웹앱 짝 |
| M2 | **비관통이면 `sigma_full_status` 가 'valid_zero' 가 아니라 'not_computed'** — `solve_network` 가 관통 성분이 없으면 (None, None) 을 돌려준다.  docstring 의 "'valid_zero' = 퍼콜 경로 없음" 은 도달 불가 | `network_conductivity.py:540–576` ↔ `:94–112` · 결과 dict :1164 | §5-2 G2 · G3 의 NOT_PERCOLATING ↔ SOLVER_ANOMALY 판별은 `sigma_full_status` 로 못 한다 → `percolating_fraction == 0` (또는 `calc_percolation`) 으로 명시.  F-12 sentinel 결함 자체도 등재 후보 (봉인 모듈이라 S3 뒤) |
| M3 | G5 근거 줄이 디버그 전용 (#38) | `network_conductivity.py:833–849` | #38 대로 |
| M4 | **`constriction_dominant` 경고도 죽어 있다** — `constriction_pct` · `constriction_fraction_pct` 생산자 0 (비슷한 `_constriction_pct` 는 그룹 표 전용 지역 키) | `app.py:2903` · `refresh_warnings.py:86` ↔ `app.py:6832` | T26 · TAU-06 의 같은 경고 묶음 (협착 서사) 에 포함 |
| M5 | **L0 띠도 띠 노드를 등전위로 묶고 정규화는 plate_z** — 실효 길이가 L 보다 짧아 T 를 r/L 차수로 낮춘다 (L1 폴백과 같은 기전, 크기만 작다) | 곧은 사슬 4 개 (L0) 에서 T_CF/극한 = 0.967 @ 2r/L 0.033 · 코퍼스 2r_SE/L 중앙 0.031–0.041 · 최대 0.086 | §5-3 한정어: "T 는 띠 끝 처리로 수 % (얇고 SE 굵은 침대에서 더) 낮게 나온다 — 크기는 침대 실측 전 추정" |
| M6 | 열 사전 문구가 이미 전달된 배포본에 들어 있다 (#6) | 커밋 TSV 6 개 | 배포 정정 결정 (TAU-01 범위) |
| M7 | κ 추정의 접촉법칙 · 단위 (#23) | 덱 40 개 hooke/hysteresis · `DESC-03` | §6-2 · C1 |
| M8 | TAU-05 의 실제 파급 (#34) | case_master 필터 재현 | σ_e Stage 22.5 생 적합 6 행 탈락 확정 → 1저자 결정 (동결 vs 재적합) 을 "가능성" 이 아니라 "필수" 로 |
| M9 | (작음) `sigma_full_mScm` 은 소수 6 자리 반올림 (`:1156`) — φσ₀/σ_full_mScm 와 φ/`sigma_full` 이 코퍼스에서 최대 0.11 % 다르다 | case_master `sigma_full`×3 ↔ `sigma_full_mScm` | G4 "비트 동일" 시험 · 인계 T 는 무차원 `sigma_full` (8 자리) 로 계산 |

## 3. 판정 집계

- 49 행: **확인 37 · 부분 10 · 틀림 1 · 검증 불가 1**.
- 틀림: #22 (§6-1 A_LIGG/A_Hertz 식 — 메모 자신의 d 정의로는 1.0125, 1.9875 는 δ 일 때).
- 부분: #5 (T12 τ_F 칸 — 자동 배선 없음) · #6 (TSV 6 개 · 전달본) · #7 (selftest 는 낱말 둘만 강제) · #9 (COMSOL 2D ≠ 등급 사슬) · #23 (κ 는 hooke 법칙에서 E* 비 아님 · AM 모듈러스는 덱에서 풀림) · #25 · #26 (봉인 = 재봉인 강제이지 금지 아님 · plastic_coverage 09-29 세 커밋 누락) · #34 (6 침대 σ_e 적합 포함 확정 · 열 무영향) · #38 (:846 디버그 전용) · #47 (Tippens 미감사).
- 재계산이 메모와 어긋난 수치는 없다 (반올림 · 분위 규약 차 두 건만: #35 · #41).
