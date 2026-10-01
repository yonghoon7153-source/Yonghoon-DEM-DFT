> ⚠ 이 문서는 **읽기 전용 대조 조사** 원문이다 (10-01 · HEAD `d1ec42fba` · 조사 에이전트 작성 · 리포는 고치지 않음).  핵심 주장 둘 (배포 v1 의 HOLD 표지 누락 · 상수 열) 은 내가 다시 셌다 (J20-q).  원장 반영 = 다음 커밋 · 요청서 §2-A.

# DESC-01~09 · HND-01~06 — 배포 v1 시점에 실제로 참인 것 (HEAD `d1ec42fba` · 2026-10-01)

> 읽기 전용 조사.  리포는 수정하지 않았다.  판정문 두 편 (`docs/reviews/codex_verdict_lhs_descriptors_20260913.md` ·
> `docs/reviews/codex_verdict_lhs_porosity_thickness_20260924.md`) · 원장 `docs/reviews/findings.json` · 판단 J17–J20-p ·
> 배포 `docs/data/lhs_release_20261001/` · 인계표 `docs/data/{lhs,lhsx}_handover_20261001.csv` 와 **HEAD 코드**를 대조했다.

## 0. 방법 · 증거 표기

- **[V]** = 코드 · 데이터 · git 에서 직접 확인 (줄 번호는 HEAD 기준) · **[I]** = 추론.
- 판정 기준: 원장 항목에 **적힌 그대로** (인용된 함수 + Codex 반례).  배포 경로 (수확기 → 생성기 · 웹앱 배치) 에서만 해소된 경우는
  판정 칸에 그 범위를 같이 적었다 (예: `PARTIAL (배포 경로 FIXED · 인용 코드 OPEN)`).
- 실행한 것 (전부 읽기 전용 · 출력은 세션 scratchpad (리포 밖)):
  1. `scripts/lhs_descriptor_harvest.py --selftest` → rc 0 · ✓ 168 · ✗ 0 [V]
  2. `scripts/lhs_design_dataset.py --selftest` → **207/207 PASS** [V]
  3. 인계표 재생성 (커밋된 입력만 · 출력 = 스크래치패드): `--export-handover … --harvest docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d
     --webapp docs/data/{lhs,lhsx}_webapp_coverage_1e09f661d --webapp-groups contact,percolation` (+ lhsx 설계 · union) → **130 · 64 둘 다 커밋본과
     바이트 동일** · 관문 T1–T3 · D1–D5 · C1–C3 · 같은 프레임 |Δporosity| 최대 1.238e-10 %p 통과 [V]
  4. 배포 CSV ↔ 인계표: 같은 열 · 같은 행에서 **셀 차이 0** (130 · 64) [V]
  5. 탐침 스크립트 probe_now.py (로그 probe_now.log — 세션 scratchpad · 리포 밖) — HEAD 의 실제 함수에 Codex 반례를 넣었다 (§2) [V]
- ⚠ 조사 중 작업 트리에 **내가 만들지 않은 변경**이 생겼다: 02:09:57–02:10:35 UTC 에 문서 5 개 (`docs/data/area_s2_cohort_provenance.md` 등 —
  서버 주소를 `<주소>` 로 가림) 가 수정됨 = 다른 프로세스.  나는 리포 파일을 만들거나 고치지 않았다 (생성기 · 수확기 시험 전후 `git status` 동일 확인).

## 1. 요약 표

| id | 심각도 | Codex 가 말한 결함 (한 줄) | 판정 | 근거 (커밋 · 파일:줄 · 시험/관문 · J-id) | 남은 것 | 배포 열 영향 |
|---|---|---|---|---|---|---|
| DESC-01 (재확인) | P1 | τ 실패가 φ_SE · φ_AM 키까지 삼킨다 | **FIXED** | `f3cb141ae` · `dem_analysis_core.py:1047-1056` · `analyze_contacts.py:484-489` · `webapp/test_closed_param_values.py:206-219` [C] · 수확기 selftest ① | 웹앱 φ_AM 은 여전히 잔차식 (`analyze_contacts.py:489`) — 결함 본체 아님 | 없음 (배포 φ = 수확기 직접 합 → 질량 보존 φ) |
| DESC-02 | P1 | 비관통인데 τ=1 · 관통인데 τ=None (fallback source · 성분 밖 쌍이 200 예산 소진) | **PARTIAL** (배포 경로 FIXED · 인용 코드 OPEN) | 수확기 벽 τ `lhs_descriptor_harvest.py:1249-1416` (`716850ced` · `5f3836afc`) · 생성기 T1–T3 `lhs_design_dataset.py:953-982 · 1968-1971` (`6870a85a5`) · selftest ② ③ ⑰ · 탐침 P1 · P2 · J20-n | 웹앱 `calc_tortuosity` (`dem_analysis_core.py:598-615`) 두 반례 **HEAD 에서 재현** → full_metrics `tortuosity_*` · `predictor_engine.py:279` 로 흐름 · selftest ③ 은 반례 ② 를 분별 못 함 | 없음 (배포 τ = 수확기 벽 τ · 비관통 24 빈칸) |
| DESC-03 | P1 | Physics 피복률: 확대 DEM 길이 ÷ 미확대 5 nm → cap 선택 뒤집힘 | **MOOT** (인계·배포) · 코드 **OPEN** | J20-m · `06e8c01e2` · `webapp/test_coverage_handover_scope.py:98-109` (K4: 인계표 4 판 physics 열 0) · 수확기 plastic_coverage 미사용 (selftest ⑬ · LHSC-05 verified) | `coverage_physics_vs_hertzian.py:455-467` → `plastic_coverage.py:51 · 362-363` 그대로 (DESC-10 순서 제약 · 의도된 보류) · v2 후보 = LHSC-10 미검증 · 웹앱 · 망 전도도 · 등급은 v1 사용 (LHS-25) | 없음 |
| DESC-04 | P2 | τ 이름이 통계량 (mean/median/recommended) · 경계 폴백 · 절단을 정하지 않는다 | **PARTIAL** (배포 경로 FIXED · 인용 코드 OPEN) | `HANDOVER_TAU_WALL` `lhs_design_dataset.py:874-891` (평균 · 중앙값 따로 · recommended 없음) · 규약 문자열 강제 `:1820-1821` · 세대 혼합 거부 `:1723-1726` · 옛 열 보류 `:738-742` · `tau_wall_n_truncated` 0/194 | 웹앱 `calc_tortuosity` 3 키 · 자동 전환 (`:641-650`) · 무기록 절단 (`:627-630`) · `calc_percolation` L1/L2 폴백 (`:505-523`, LHS-17 open) 그대로 | 값 영향 없음: 퍼콜 열의 폴백은 130 감사 L0 130/130 (J20-b) · 64 는 벽 밴드 인원 ≥ 758/824 로 미발동 [I] |
| DESC-05 | P2 | 0 · N/A · invalid 가 한 값으로 접힌다 (없는 상 · 분모 붕괴 · mono map 크래시 · 직경 휴리스틱) | **PARTIAL** (배포 경로 FIXED · 웹앱 잔여) | 수확기 `_coverage_from_sums` `:1112-1151` (N_A_PHASE_ABSENT · 분모 ≤ 0 제외 + 셈) · selftest ⑥ ⑦ · `514691646` (`analyze_contacts.py:168-185 · 870-889`) · `_mono_design_phase` `lhs_design_dataset.py:1299-1332` (`06b24cdd0`) · 인계표 `cov_n_free_surf_invalid` = `cov_n_capped` = 0 (194/194) | 웹앱 `calc_coverage` 가 분모 ≤ 0 을 여전히 **0 으로 접는다** (`dem_analysis_core.py:288` · 탐침 P4) · cap/분모붕괴 수 미산출 | 없음 |
| DESC-06 | P2 | 덤프를 읽었다고 같은 최종 프레임이 아니다 (종류별 최신 독립 선택 · 다중 프레임 이어 붙임 · 무메시 벽 추정) · 완료 압력 검사 요구 | **PARTIAL** | 수확기 timestep 일치 `:1426-1430` (selftest ⑧) · 플래튼 추정 금지 `:1438-1446` (⑨) · 같은 step 메시 `lhs_harvest_batch.py:109-142` · 배치 sha · 프레임 · 중복 관문 `lhs_webapp_batch.py:126-147` (`0a8c22ab2`, selftest ⑧–⑪) · 생성기 같은 프레임 `lhs_design_dataset.py:1945-1953` · union 짝 `:1450-1466` · 배치 status 130/64 프레임 1 · 중복 0 | ① 웹앱 파서 그대로 (`parse_liggghts.py:252-258 · 17-76` · `dem_analysis_core.py:171-186` — 탐침 P7 · P8 재현) ② **완료 압력 검사가 어디에도 없다** (수확 · 배치 · 봉인 grep 0) → CANNOT TELL ③ 접촉 감사 원자료 미반입 | 확인된 영향 없음 · ② 가 틀린 런이 있으면 그 행의 **전 측정 열** |
| DESC-07 | P2 | ε 와 C_total 은 정의 종속 — 일곱 독립 회귀로 세면 안 된다 · 실측 N 을 몰래 넣지 말 것 | **PARTIAL** | porosity 항등식 `build_handover` `:1811-1815` · 질량 보존 닫힘 `:1477-1482` (1e-9) · CN 항등식 G1–G7 · J20-i · j · P3 · 배포 README §3 · 프롬프트 규칙 1 · 3 · 배포엔 실측 N 만 (`n_*_measured`) | 회귀 단계 (다운스트림) 강제 불가 · coverage 가중평균 항등식은 `fill_descriptors` (`:653-664`) 에만 있고 **인계표 경로에는 없다** (README §3 "전부 1e-9 로 검사" 과장 · 데이터는 정확히 성립 — 최대 차 0) | 항등식 묶음 열 (`porosity_union_exact_pct` ↔ `phi_*_mass_conserving` · `coverage_AM_total_hertz_pct` ↔ P/S · `am_se_cn_mean` · `_surface_weighted` · `se_se_cn` · `am_am_cn` · `se_se_cn_n_perc`) — 문서화됨 |
| DESC-08 | P2 | 291 코퍼스 loader 가 d_am=0 40 행 수용 · 존재상 불일치 · MPM/DEM 혼합 잔존 | **OPEN** | — (`ml_design_structure.py` 는 `335247212` 이후 변경 0 · 그 커밋은 `use_porosity_pct` **소비**만 막음 `:428`) | `load_corpus` `:566-583` 실제 호출 → d_am=0 **40 행 수용** · `predictor_engine.py:237-243 · 310` d_am = max(입력 반경) 그대로 · 배포 README 에 291 병합 금지 경고 없음 | 직접 영향 없음 (생성기 291 경로 AST 금지 ⑮e `:2270-2277`) · 병합하면 오염 |
| DESC-09 | P2 | 미실행 8 개가 한 수준을 통째로 비움 · `finite_size_flag` 는 설계의 결정론적 함수 | **PARTIAL** | 130/130 · 부분 인계 거부 `:1703-1706` · mono_AM_S × d_SE 2 µm 다섯 점 배포에 값 | 해석 한정어 ("고정 finite-box 규약 안의 예측") 가 배포 README 에 없다 · `rve_um` (130 행 전부 50) · `pressure_MPa` · `e_se_gpa` · `loading_mAh_cm2` (전부 상수) 를 X 후보로 적었다 | 전 Y 열의 해석 범위 · 상수 X 4 열 |
| HND-01 | P1 | (나) pushback 을 hard-bottom 보정으로 해석 · (가) 는 명목 장부값 | **FIXED** (인계) · 배포 MOOT | J18 철회 (`lhs_handover_judgments_20260924.md:261`) · `af528e24d` 이름 (`*_spheresum_nominal_gap` · `*_pushback_equiv` "hard-bottom 예측 아님" · `*_clipped_spheresum_gap` · `boundary_model_id`) `lhs_design_dataset.py:771-780 · 820` · `lhs_descriptor_harvest.py:1044-1046` · selftest ⑮ HND-01 | (관찰) 배포의 유일한 두께 `thickness_mass_conserving_um` 도 산술 장부값 — Codex 가 ACCEPT 한 `thickness_wall_gap_um` 은 배포에 없다 (Codex 미검토) | 없음 ((가)(나)(다) 미포함) |
| HND-02 | P2 | `check_deck_floor` 가 unfix · 재정의 · 부분 group 벽을 통과시킨다 | **FIXED** | `af528e24d` `lhs_descriptor_harvest.py:835-909` · selftest ⑮ HND-02 (unfix · 재정의 · group · include) · 봉인 커밋 `1e09f661d` 포함 · 배포 원천 194 수확 전부 새 문법 (`deck_floor.grammar` · z 0 · 활성 벽 1) | 정적 판독 한계 (마지막 `run` 뒤 정의 · 움직이는 벽 등) [I] | 없음 |
| HND-03 | P1 | 중심이 평면을 넘은 입자 (1.98r = 아래쪽 점착 평형) 를 "정상 압입" 으로 기록만 | **PARTIAL** | `_wall_side` `:938-962` (`outside_cap_depth_over_r` · `contact_overlap_over_r`) · `boundary_state` · `BOUNDARY_CENTER_OUT` → HOLD `:1031-1052` · selftest ⑮ · q/φf/kc 덱 확인 (J18 E) | ① 기전 "조건부 재현" — 바이너리 · 관통 시점 프레임 · 접촉 이력 미확인 ② **배포가 HOLD 를 버렸다** — 경계 이탈 **130 중 43 · 64 중 11** 이 무표지 타깃 ③ 경계 입자의 τ 밴드 · 접촉망 영향 미측정 | **있음**: 그 54 행의 전 측정 열 (특히 `tortuosity_SE_wall*` · `percolation_pct` · `top_reachable_pct` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc` · `wall_touch_frac_*_floor` · CN · coverage · 벽 밖 부피를 다르게 다루는 `porosity_union_exact_pct` / `thickness_mass_conserving_um` / `phi_*_mass_conserving`) |
| HND-04 | P1 | `build_handover` 가 벽 진단 · 적격성을 버리고 음수 porosity · φ 합 > 1 을 OK 로 | **PARTIAL** (생성기 FIXED · 배포에서 재발) | `af528e24d` `HANDOVER_EXTRA` `lhs_design_dataset.py:750-827` · `DEFAULT_HARVEST_DIR` `:747` · 생성기 selftest ⑰ (lhs00_005 e2e `:2189-2216`) · 인계표 HOLD 59/130 · 62/64 | 배포 (`8b84ba476`) 가 적격성 · 경계 QC · 프로비넌스 열을 **전부 뺐다** · 배포 부분집합 생성 도구/시험이 리포에 없다 · J19 ④ (union 기준 적격성) 미비준 | **있음**: HOLD 121 행 (59 + 62) 이 무표지 · 단 배포 φ · porosity 자체로는 반례 불가 (φ 합 = 1 − ε_union · union ∈ (0,100) `:1467`) |
| HND-05 | P2 | `calc_porosity_dual` ε_union = 쌍 렌즈뿐 (삼중 교집합 · 완전 포함 · 벽 clipping 없음) | **PARTIAL** (배포 FIXED · 인용 함수 OPEN) | 정확 MC union `lhs_union_webapp.coverage` (`42e3ca460`) · 웹앱 `calc_porosity_union_exact` `dem_analysis_core.py:115-168` (`90c6c9670`) · 시험 `webapp/test_closed_param_exact_union.py` X3 (벽) · X5 (같은 자리 세 구) · 질량 보존 φ (J20-e) | `calc_porosity_dual` `:47-109` 그대로 — 탐침 P5: **1.878672 < 4.188790 · 동심 12.566371** (Codex 수치 그대로) · 여전히 `porosity_union` 이름으로 저장 (표시만 "쌍 렌즈") | 없음 |
| HND-06 | P2 | `plate_z_from_stl` 이 평판 검사 없이 꼭짓점 z 평균을 높이로 | **FIXED** (인용 함수) | `af528e24d` `lhs_descriptor_harvest.py:796-817` (폭 > 1e-7 sim 거부) · selftest ⑮ HND-06 · 탐침 P6 거부 · `1e09f661d` 포함 · 194 수확 `plate_z_source = mesh_stl` | 웹앱 `parse_liggghts.parse_mesh_stl` `:79-108` 그대로 (탐침 P6: 1.0) — SELF-49 소관 | 없음 (같은 STL sha · 같은 프레임 관문 · union 두께 짝 1e-6 µm 로 수확기 plate_z 에 묶임) |
| SELF-21 | P2 | 철회된 권고 ("5 개 제외") 를 인용 | **PARTIAL** | 판정문 부록 "내 요청서의 오류" 2 (`codex_verdict_lhs_descriptors_20260913.md:362-367`) 에서 철회 | 처방 (인용 판정문 끝까지 · 정정 배너 grep) 을 강제하는 도구 없음 | 없음 |

**집계 (요청 14 건 = DESC-02~09 · HND-01~06)**: FIXED 3 (HND-01 · 02 · 06) · MOOT 1 (DESC-03, 코드는 OPEN) · PARTIAL 9 (DESC-02 · 04 · 05 · 06 · 07 · 09 · HND-03 · 04 · 05) ·
OPEN 1 (DESC-08) · CANNOT TELL 0 (DESC-06 의 "완료 압력" 하위 항목만 CANNOT TELL).  + DESC-01 FIXED (재확인) · SELF-21 PARTIAL.

## 2. 탐침 — Codex 반례를 HEAD 함수에 그대로 [V]

| 탐침 | 반례 | 웹앱 함수 (생산 · 코퍼스 경로) | 배포 경로 함수 |
|---|---|---|---|
| P1 | DESC-02 ① 바닥 고립 3 + 위 기둥 (바닥 미연결) | `calc_percolation` 0.0 · `calc_tortuosity` mean = recommended = **1.0**, n 3 → **재현** | 수확기 벽 τ `NOT_PERCOLATING` · τ 없음 · 관통 성분 0 |
| P2 | DESC-02 ② 직선 관통 기둥 200 개 (각자 성분) | percolation 100 · τ **None**, n 0 → **재현** | `OK` · τ 1.0 · 200/200 유효 · 관통 성분 200 |
| P3 | DESC-04 τ [1, 1, 10] | mean 4 · median 1 · std/mean 1.06 → `use_median` True (`:641-650` 규칙) | 평균 · 중앙값 별도 열 · recommended 없음 |
| P4 | DESC-05 AM–AM 면적 > 표면 | `calc_coverage` AM_P mean **0.0** (n 2, 분모붕괴가 0 으로) → **재현** | 수확기: 분모 ≤ 0 제외 + `n_free_surface_invalid` (selftest ⑦) |
| P5 | HND-05 r=1 세 구 · 쌍 거리 0.2 / 동심 셋 | 쌍 렌즈 V_union **1.878672** (< 한 구 4.188790) / **12.566371** → **재현** | 정확 MC 5.21 ± 0.05 / 4.20 (참값 4.189) |
| P6 | HND-06 z = 0 · 2 삼각형 STL | `parse_mesh_stl` plate_z **1.0** → **재현** | `plate_z_from_stl` 거부 (BedRefusal) |
| P7 | DESC-06 atom_100 + contact_200 (2 프레임) + mesh | `parse_liggghts` rc **0** · contacts.csv **2 행** (접촉 1) → **재현** | 수확기 `TIMESTEP 불일치` 거부 · 배치는 프레임 ≠ 1 거부 |
| P8 | DESC-06 무메시 | `get_plate_z` → (0.019, `estimated_center`) — 라벨만 남김 | 수확기: 플래튼 추정 금지 (selftest ⑨) |

⇒ **배포 경로는 여덟 반례 전부에 안전하고, 웹앱 (생산 · 코퍼스 · 일반 업로드) 경로는 일곱을 여전히 재현한다** [V].

## 3. 항목별

### DESC-01 (claimed_fixed 재확인) — FIXED
- [V] `dem_analysis_core.py:1047-1056` — τ 가 없거나 ≤ 0 이면 `{'phi_se', tau: None, sigma_ratio: None}` 를 돌려준다 (옛 `return None` 제거).
- [V] `analyze_contacts.py:484-489` — φ_SE · φ_AM 을 τ 조건 밖에서 싣고 `sigma_ratio` 만 조건부.  시험 `webapp/test_closed_param_values.py:206-219` [C] (SE–SE 접촉 0 침대) · 커밋 `f3cb141ae`.
- [V] 배포 φ 는 웹앱이 아니라 수확기 `volumes_and_phi` 직접 합 (`lhs_descriptor_harvest.py:1017-1018`) → `_union_cols` 질량 보존 φ (`lhs_design_dataset.py:1474-1483`).  5번 웹앱 배치 (`1e09f661d`) 는 이 수정 **이전** 코드지만 φ 를 거기서 가져오지 않으므로 무관.
- [V] 경미한 잔여: 웹앱 φ_AM = `1 − φ_SE − ε/100` 잔차식 (`analyze_contacts.py:489`) — 판정문 표의 "다른 상이 있으면 일반화 불가" 지적은 남는다 (DESC-01 본체 아님).

### DESC-02 — PARTIAL (배포 경로 FIXED · 인용 코드 OPEN)
- [V] 인용 코드 그대로: `dem_analysis_core.py:598-605` (바닥 source 없으면 위 성분 최저 z 승격) · `:610-615` (전수 쌍 shuffle 후 200 개).  `git log -S` 로 이 블록은
  `660600a44` (2026-04-24 반입) 이후 변경 없음.  탐침 P1 · P2 가 **두 방향 모두 재현**.
- [V] 배포 τ = 수확기 `tortuosity_se` → `_tau_sample` (`lhs_descriptor_harvest.py:1249-1416`): 승격 없음 · **같은 성분 안 쌍만** (`:1374-1384`) · 상태 분리 (`OK` ·
  `NOT_PERCOLATING` · `ELECTRODE_BAND_EMPTY` · `NO_VALID_SAMPLED_PAIR`, `:216-226`) · 벽 밴드 (`TAU_WALL_CONVENTION` `:229`).  생성기 T1 (관통 성분 수 = 상태 = 수확 벽 밴드 진단)
  · T2 (값 · 표본 수) · T3 (비관통 ⟺ `percolation_pct` 0) — 재생성에서 130/130 · 64/64 [V].
- [V] Codex 처방 "유한 τ 는 조건부 목표로만" = 배포 README §7 규칙 2 (관통 분류 → 관통 침대만 τ 회귀) · 비관통 24 빈칸.
- [I] 수확기 selftest ③ (`:1706-1718`, 기둥 1 + 밴드 밖 외톨이 300) 은 옛 알고리즘도 통과하는 구성이라 반례 ② 를 **분별하지 못한다**.  성질은 구성상 보장되고 (`:1384`)
  탐침 P2 가 확인했지만, 200 기둥 반례를 상주 시험으로 옮길 것을 권한다.
- [V] 웹앱 τ 는 여전히 모든 웹앱 케이스의 `full_metrics` (`tortuosity_mean/median/recommended`) · `calc_effective_conductivity` σ 비 · 예측기 학습 필터
  (`webapp/predictor_engine.py:279`) 로 흐른다 — 배포 밖이지만 코퍼스 안.

### DESC-03 — MOOT (인계 · 배포) · 코드 OPEN
- [V] `coverage_physics_vs_hertzian.py:455-467` 는 sim 단위 δ · R* 를 `film_area_from_overlap` 에 넘기고, `plastic_coverage.py:51` `H_FILM_MIN = 5.0e-9` · `:362-363`
  `A_volume = V_overlap / H_FILM_MIN` 그대로 = 결함 그대로.  DESC-10 (P1 open) 의 "단위만 먼저 고치지 말 것" 순서 제약에 따른 **의도된 보류**.
- [V] v2 후보 (`film_area_physics_v2` · 두께 = `H_FILM_MIN × length_scale`, `coverage_physics_vs_hertzian.py:377`) 는 단위가 맞지만 `LHSC-10` 미검증 ·
  `LHS-25` (접촉 면적 합에 표면 한도 없음 → 포화 · 분모 붕괴 18 침대).
- [V] 인계 · 배포는 physics v1 · v2 · rough 를 싣지 않는다 (J20-m · `06e8c01e2` · K4 가 인계표 0930/1001 네 판에서 physics 열 0 을 강제).  배포 coverage 3 열 출처 = 수확기 c_cpl[22].
- [V] 수확기는 plastic_coverage 를 가져오지 않는다 (selftest ⑬ AST · `lens_geometry` 분리 · LHSC-05 verified).
- 남은 것: 웹앱 화면 · 망 전도도 Stage-E physics · 등급 physics 축은 여전히 v1 을 쓴다 (`LHS-25` ①② 열림).

### DESC-04 — PARTIAL (배포 경로 FIXED · 인용 코드 OPEN)
- [V] 웹앱 그대로: `calc_tortuosity` 3 키 + 분산 큰 경우 `recommended = median` 자동 전환 (`:641-650`) · `[1, 20)` 절단 (잘린 수 기록 없음, `:627-630`) ·
  `calc_percolation` L1/L2 폴백 (`:505-523`, 어느 단계가 쓰였는지 산출물에 없음 = `LHS-17` open).
- [V] 배포: `tortuosity_SE_wall` = 절단 평균 · `tortuosity_SE_wall_median` 별도 · recommended 없음 (`lhs_design_dataset.py:874-891`) · 규약 문자열이 다르면 거부 (`:1820-1821`) ·
  수확 세대 혼합 거부 (`:1723-1726`) · 옛 `tortuosity_dijkstra_SE` 는 `HANDOVER_HELD_BACK` (`:738-742`) · 수확기 τ 는 밴드 폴백 없음 (빈 밴드 = `ELECTRODE_BAND_EMPTY`).
- [V] 절단: 인계표 `tau_wall_n_truncated` = 0 (194/194) ⇒ 배포 절단 평균 = 무절단 평균.  (`tau_mean_untruncated` 는 수확 JSON 에만, 배포엔 없음.)
- [V/I] 배포의 퍼콜 열 (`percolation_pct` · `top_reachable_pct` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc`) 은 웹앱 `calc_percolation` 산출이다.  130 은 J20-b 감사가
  L0 130/130 (원자료 미반입 — 판단문 기록 기준) · 64 는 감사 미실행.  SE 가 단분산이면 수확기 벽 밴드 = 웹앱 L0 밴드 (J20-b F8) 이고 인계표 `tau_wall_n_bot` 최소 758 ·
  `tau_wall_n_top` 최소 824 (130 은 106 · 28) ≥ 3 [V] ⇒ 64 에서도 폴백 미발동 [I].

### DESC-05 — PARTIAL (배포 경로 FIXED · 웹앱 잔여)
- (a) [V] 없는 상 = `N_A_PHASE_ABSENT` · 존재 + 무접촉 = 0 (`lhs_descriptor_harvest.py:1128-1139`, selftest ⑥) · 생성기 계약 ② 상태 ≠ OK 면 빈칸 (`lhs_design_dataset.py:1798-1800`) · 배포 README §3-1.
- (b) [V] 수확기는 분모 ≤ 0 을 **제외하고 센다** (`:1120-1122`, selftest ⑦) · 인계표 `cov_n_free_surf_invalid` = 0 · `cov_n_capped` = 0 (194/194).  [V] 웹앱 `calc_coverage`
  (`dem_analysis_core.py:288`) 는 그대로 `… if free > 0 else 0` — 탐침 P4 재현.
- (c) [V] mono map `np.min(빈 배열)` → `514691646` (09-22): 빈 상은 '—' (`analyze_contacts.py:168-185`) + 계산 **전** type_map ↔ 덤프 관문 (`:870-889`).
- (d) [V] Codex 가 "결함 주장 아님" 으로 남긴 직경 휴리스틱 (r > 4 µm → AM_P) 은 실제로 mono **9 건** (130 의 5 · 64 의 4) 에서 설계와 어긋났다 — 생성기가 설계 block 으로
  옮기고 (`_mono_design_phase` `:1299-1332`, `06b24cdd0`) 웹앱 이름을 `wa_mono_phase_name_webapp` 에 남긴다 (J20-f · J20-k (B)).  수확기는 `--n-types` 로 상을 정한다.
- 남은 것: 웹앱 `calc_coverage` 분모 붕괴 → 0 · cap/붕괴 수 미산출 (배포 coverage 는 수확기 값이라 무영향).  rough 모양 인자 이름 의존 `LHS-26` (배포 밖).

### DESC-06 — PARTIAL
- [V] 배포 경로 관문: 수확기 atom/contact TIMESTEP 일치 (`lhs_descriptor_harvest.py:1426-1430`, ⑧) · 플래튼은 메시나 명시값만 (`:1438-1446`, ⑨) · 같은 step 메시만
  (`lhs_harvest_batch.py:109-142`, `latest_le` 폐지) · 배치: 네 파일 sha = 수확 JSON · contact/atom 프레임 = 1 · 중복 · 자기쌍 거부 (`lhs_webapp_batch.py:126-147`, `0a8c22ab2`,
  selftest ⑧–⑪) · 생성기 같은 프레임 |Δporosity| ≤ 0.05 %p (`lhs_design_dataset.py:1945-1953`, 재생성 실측 1.238e-10 %p) · union 짝 (구 부피 합 1e-9 · 두께 1e-6 µm · 입자 수, `:1450-1466`).
  5번 배치 `status.json`: 130 · 64 전부 contact · atom 프레임 1 · 중복 0 [V].
- [V] 웹앱 일반 경로 그대로: `parse_liggghts.py:252-258` (종류별 최신 독립) · `:17-34` · `:37-76` (프레임 이어 붙임) · `dem_analysis_core.py:171-186` (무메시 = 최고 중심) —
  탐침 P7 · P8 재현.  원장 note 도 "웹앱 파서 자체는 그대로 (열림)" 이라 적는다.
- **CANNOT TELL — 완료 압력**: 원장 note · 판정문 §3 이 요구한 "완료 압력" 검사가 수확 · 배치 · 봉인 (`seal_area_cohort.py`) 어디에도 없다 [V: grep 0].  배포 README §1 은
  "300 MPa 압밀 뒤 한 프레임" 이라 적는다.  같은 step 메시에서 플래튼 − 고체 윗면 −1.21 … −0.27 µm (J12 · J16) 는 판이 침대를 누르고 있다는 것까지이지 목표 압력 도달의 증거가 아니다 [I].
- [V] 접촉 감사 원자료 (`docs/data/lhs_contact_audit_20260929/`) · 퍼콜 감사 원자료 (`lhs_perc_audit_20260929/`) 는 리포에 없다 — "130/130 CLEAN" 은 판단문 기록뿐.

### DESC-07 — PARTIAL
- [V] 생산자 측 강제: ε_sphere 항등식 재검사 (`build_handover` `:1811-1815`) · 질량 보존 φ 닫힘 1e-9 (`:1477-1482`) · CN 항등식 (J20-i · j · 7c G1–G7) · P3 (`se_se_cn_n_perc`).
  배포 README §3 · 프롬프트 규칙 1 (X = 설계 입력만 — `n_*_measured` 는 X 가 아님) · 규칙 3 (항등식 열 ≠ 독립 타깃).  배포는 실측 N (`n_*_measured`) 만 싣고 설계 추정 N 은 안 싣는다.
- [V] 빈틈: coverage 가중평균 항등식 (DESC-07 ②) 은 `fill_descriptors` (`:653-664`) 에서만 검사하고 `--export-handover` 경로 (`build_handover`) 엔 없다 → README §3 의
  "생성기가 전부 1e-9 로 검사했다" 는 `coverage_AM_total` 에 대해 사실이 아니다.  데이터는 정확히 성립 (bimodal 100 · 48 행, 최대 차 0).
- 남은 것: "관측 N 을 몰래 넣지 말 것 · 일곱을 독립 성능으로 세지 말 것" 은 다운스트림 회귀 단계 — 생산자가 강제할 수 없다 (원장 note 자신의 결론과 같다).

### DESC-08 — OPEN
- [V] `ml_design_structure.load_corpus` (`:566-583`) 를 실제로 불렀다: 291 행 중 **d_am = 0 40 행 수용**, 타깃에 `use_porosity_pct` 포함.  `335247212` (09-13) 은
  `RESTRICTED_TARGETS` (`:428`) 로 그 열의 **제안 · 소비**만 막았다 — 적재 · closure 잔차는 그대로.  `webapp/predictor_engine.py:237-243 · 310` d_am = max(입력 반경) 도 그대로.
- [V] 130/64 는 분리돼 있다: 생성기에 291 경로가 없다 (selftest ⑮e AST `:2270-2277`) · 수확기 계약 ⑥.
- [V] 배포 README 에 "291/옛 코퍼스와 합치지 말 것" 이 없다 (J20-m 인계 한정어 ⑥ "옛 코퍼스와 섞을 때 치밀도 보정 필요" 도 미반영).

### DESC-09 — PARTIAL
- [V] 앞 절반 닫힘: 130/130 · 부분 인계 거부 (`build_handover` `:1703-1706`) · mono_AM_S × d_SE 2 µm 다섯 점 배포에 값 (`105` · `108` · `111` 비관통 → τ 빈칸 ·
  `109` τ 1.42 · `110` τ 2.09).
- [V] 뒤 절반: `finite_size_flag` 는 배포에 없다 (인계표엔 있음).  그러나 "고정 finite-box 규약 안의 예측" 한정어가 README 에 없고, README §2 · 프롬프트 규칙 1 이
  `rve_um` 을 X 후보로 적는데 130 행 전부 50 이다 (`pressure_MPa` 300 · `e_se_gpa` 1.35 · `loading_mAh_cm2` 2.0 도 상수).

### HND-01 — FIXED (인계) · 배포 MOOT
- [V] J18 이 J17 의 "(나) ≈ 단단한 바닥" 을 철회 (`lhs_handover_judgments_20260924.md:261`) · `af528e24d` 가 이름을 규약으로 고정 — `phi_*_spheresum_nominal_gap` ·
  `porosity_spheresum_nominal_gap_pct` · `*_pushback_equiv` ("hard-bottom 예측 아님 (HND-01)") · `*_clipped_spheresum_gap` · `boundary_model_id` (`lhs_design_dataset.py:771-780 · 820` ·
  `lhs_descriptor_harvest.py:1044-1046`) · selftest ⑮ HND-01.  남은 "hard-bottom" 문장은 철회 표시가 붙은 이력 문서뿐 [V: grep].
- [V] 배포는 (가) · (나) · (다) 를 하나도 싣지 않는다.
- 관찰 [V/I]: 배포 두께는 `thickness_mass_conserving_um` (= H_gap × (1 − ε_sphere)/(1 − ε_union) · 벽 밖 부피와 겹침 부피를 두께로 보냄 · H_mc/H 중앙 1.043, 64 는 1.118) 하나다.
  Codex 가 ACCEPT 한 주 두께 `thickness_wall_gap_um` 은 배포에 없다.  HND-01 과 같은 부류 ("산술 장부값을 물리 두께로") 의 위험이고 J19 ② 는 판정 **뒤** 저자 비준이라 Codex 가 보지 않았다.

### HND-02 — FIXED
- [V] `check_deck_floor` (`lhs_descriptor_harvest.py:835-909`, `af528e24d`): fix id 생명주기 (unfix → 삭제 · 같은 id 재정의 → 교체) · group = all 요구 · 흐름 제어 뒤 정의/삭제 ·
  include · read_restart · read_data · python → "검증 불가" 거부.  Codex 세 변이 + include = selftest ⑮ (이번 실행 통과).
- [V] 봉인 커밋 `1e09f661d` 에 포함 · 배포 원천 수확 194 건 전부 `deck_floor.grammar` = 새 문법 · z 0.0 · 활성 벽 1 · `boundary_model_id` · `deck_wall_type` 열.
- 남은 것 [I]: 정적 판독의 한계 (마지막 `run` 뒤 정의된 벽 · 움직이는 벽 등) — Codex 가 요구한 "지원 문법 제한" 안의 잔여.

### HND-03 — PARTIAL
- [V] 상태 분리: `_wall_side` (`:938-962`) 가 `outside_cap_depth_over_r` 와 `contact_overlap_over_r` 를 따로 · 중심 밖 · 통째로 밖 수 · `boundary_state` ·
  `BOUNDARY_CENTER_OUT` → `physical_target_status = HOLD` (`:1031-1052`) · selftest ⑮.  LHS 덱 m6/m7/m8 = 생산 덱 (사용자 grep, J18 E) → "재현됨 (조건부)".
- [V] 인계표: `BOUNDARY_CENTER_OUT` **130 중 43** (bimodal 38 · mono_AM_P 3 · mono_AM_S 2 · FULLY_OUT 16 · CENTER_CROSSED 27 · 중심 밖 입자 682 · 그중 벽 τ OK 32) ·
  **64 중 11** (FULLY_OUT 5 · CENTER_CROSSED 6).
- 남은 것: ① 실행 바이너리 · 관통 시점 프레임 · 접촉 이력 미확인 (J18 E "나중에") ② **배포 (`8b84ba476`) 가 상태 열을 뺐고 README 에 경계 이탈 언급이 없다** — Codex 처방
  "43 케이스의 물리 타깃 = HOLD_BOUNDARY" 가 외부 전달에서 사라졌다 [V] ③ 경계 입자 (바닥 아래 매달린 SE 포함) 가 벽 밴드 τ · 퍼콜 밴드 · CN 에 주는 영향은 재지 않았다 [I].

### HND-04 — PARTIAL (생성기 FIXED · 배포에서 재발)
- [V] 생성기: `HANDOVER_EXTRA` (`lhs_design_dataset.py:750-827`) 가 두께 · 명목 alias · 경계 QC · `calculation_status` / `physical_target_status` / `hold_reason_codes` /
  `phi_sum_gt_one` · 규약 ID · sha 4 종 · 덱 바닥을 싣고, 기본 수확 = 0925 (`:747`) · 1001 판은 `cov_1e09f661d` 를 명시 지정.  selftest ⑰ (lhs00_005 실측값 e2e, `:2189-2216`).
  인계표 실제: HOLD 59/130 · 62/64 · `phi_sum_gt_one` 18 · 60.
- [V] 배포: 적격성 · 경계 QC · 프로비넌스 열이 **0 개** (J20-o "상태 열 · 내부 QC 제외").  README §5 는 "정본 표에 있다" 고만 한다.  배포 부분집합을 만든 도구 · 회귀 시험이
  리포에 없다 (`scripts` · `webapp` 에 `lhs_release` 참조 0 · 커밋은 CSV 를 직접 추가 · 게이트 로그는 스크래치패드).  ⇒ Codex §8 마지막 문단 ("외부 전달 CSV 에서 버리면 계약 실패") 이 배포 단계에서 다시 났다.
- [V] 배포 값 자체로는 원 반례 불가: φ = 질량 보존 (합 = 1 − ε_union) · porosity = union (0, 100) 관문 (`:1467`).  다만 J19 ④ (적격성을 union 기준으로 재정의) 가 비준 범위 밖이라
  HOLD 59 중 NEGATIVE_POROSITY 만인 16 (64 는 51) 이 배포 규약에서 풀린다는 **기록**이 없다.

### HND-05 — PARTIAL (배포 FIXED · 인용 함수 OPEN)
- [V] `calc_porosity_dual` (`dem_analysis_core.py:47-109`) 그대로 — 쌍 렌즈 · d ≤ 0 건너뜀 (`:90`) · 벽 clipping 없음.  탐침 P5 가 Codex 수치를 **소수 여섯째 자리까지** 재현.
  이 값은 여전히 `porosity_union` 키로 full_metrics 에 저장된다 (`f3cb141ae` 이후 분석기가 직접) — 화면 표지만 "쌍 렌즈 (벽 밖 미제거)" (J20-l ① · SELF-72).
- [V] 배포 union = 정확 MC (`lhs_union_webapp.coverage`, `42e3ca460` · 웹앱 `calc_porosity_union_exact` `:115-168`, `90c6c9670`) · 시험 X3 (바닥 관통 구) · X5 (같은 자리 세 구)
  (`webapp/test_closed_param_exact_union.py:60-95`) · 상별 배분 = 질량 보존 장부 (J20-e) — "union porosity + 옛 φ 둘" 혼합은 배포에 없다.

### HND-06 — FIXED (인용 함수)
- [V] `plate_stl_info` · `plate_z_from_stl` (`lhs_descriptor_harvest.py:796-817`): 꼭짓점 z 폭 > 1e-7 sim 이면 거부 · selftest ⑮ HND-06 · 탐침 P6 거부 · 봉인 커밋 포함 · NaN 꼭짓점은
  `volumes_and_phi` 에서 거부 (`:1011-1012`).
- [V] 배포 경로의 웹앱 배치는 무검사 `parse_mesh_stl` 을 쓰지만 같은 STL (sha 관문) · 같은 프레임 관문 · union 두께 짝으로 수확기 plate_z 에 묶인다.
- 남은 것: 웹앱 `parse_mesh_stl` (`parse_liggghts.py:79-108`) — 탐침 P6 = 1.0.  SELF-49 (항목 3) 에서 계속.

### SELF-21 — PARTIAL
- [V] 사례는 판정문 부록에서 철회됨.  [V] 처방 (인용 판정문을 끝까지 · 정정 배너 먼저) 을 강제하는 도구는 없다 (`scripts` · `.github` 에 SELF-21 참조 0).  배포 무관.

## 4. 가로지르는 발견 (놀라운 것 순)

1. **배포가 HOLD 121 행을 무표지로 내보냈다** — 130 중 59 · 64 중 62 가 인계표에서 `physical_target_status = HOLD` 이고 그중 경계 이탈 43 · 11.  배포엔 상태 열 · README 언급이 없다 [V].
   HND-03 · HND-04 가 요구한 "적격성 분리" 가 외부 전달 직전에 빠졌다.
2. **배포 부분집합은 커밋된 도구 · 시험 없이 만들어졌다** (`8b84ba476`).  값은 인계표와 셀 차이 0 이고 인계표는 HEAD 에서 바이트 동일로 재생성되지만 [V], 열 선택 규칙은 재현 도구가 없다.
3. **웹앱 (생산 · 코퍼스 · 일반 업로드) 은 Codex 반례 여덟 중 일곱을 여전히 재현한다** (P1 · P2 · P4 · P5 · P6 · P7 · P8) [V] — 배포가 안전한 이유는 수확기 · 관문이라는 **다른 구현**이다.
4. **"완료 압력" 은 아무도 검사하지 않는다** — README 는 "300 MPa 압밀 뒤" 라 적지만 기계 증거가 없다 (DESC-06 잔여 · CANNOT TELL).
5. README 문구 넷: coverage_total 항등식 "검사했다" 과장 (DESC-07) · 상수 열 넷을 X 후보로 (DESC-09) · 291 병합 경고 없음 (DESC-08) · finite-box 한정어 없음 (DESC-09).
6. 배포의 유일한 두께가 유도 장부값 H_mc 이고 Codex 가 ACCEPT 한 H_gap 이 없다 (HND-01 관찰).
7. 감사 원자료 미반입 (접촉 · 퍼콜) — "130/130 CLEAN" 이 판단문 기록뿐 · lhsx 퍼콜 감사 미실행은 벽 밴드 인원 (≥ 758 · 824) 으로 폴백 미발동까지는 추론 가능.

## 5. 원장 상태 변경 제안 (⚠ 제안일 뿐 — 원장은 고치지 않았다 · `verified` 는 원장 규칙상 owner 와 다른 검증자 필요)

- `DESC-01` → **claimed_fixed 유지 · verified 후보** (검증자 = 사용자 또는 Codex) — 근거 `f3cb141ae` · `dem_analysis_core.py:1047-1056` · `analyze_contacts.py:484-489` · `webapp/test_closed_param_values.py` [C].
- `DESC-02` → **open 유지 + 범위 분할**: (a) "LHS 인계 · 배포 경로" = claimed_fixed (sha `716850ced` · `5f3836afc` · `6870a85a5` · evidence 수확기 selftest ② ③ ⑰ · 생성기 ㉓ T1–T3 · 탐침 P1/P2)
  (b) 웹앱 `calc_tortuosity` 잔여 = 새 항목 (open) · 200 기둥 반례를 상주 시험으로.
- `DESC-03` → **open 유지** (DESC-10 순서 제약) · note 에 "인계 · 배포 범위 밖 (J20-m · K4 `06e8c01e2`)".
- `DESC-04` → DESC-02 와 같은 **분할**: 인계 경로 claimed_fixed (`5f3836afc` · `6870a85a5` · `HANDOVER_HELD_BACK` `a5e181384`) · 웹앱 3 키 · 무기록 절단 · `LHS-17` 폴백은 open.
- `DESC-05` → **claimed_fixed (범위 = LHS 수확 · 생성 · 웹앱 type_map)** — `716850ced` · `514691646` · `06b24cdd0` · evidence 수확기 ⑥ ⑦ · `analyze_contacts` 관문 · 생성기 ⑯d 계열 ·
  웹앱 `calc_coverage:288` 분모 붕괴 → 0 은 새 항목 (SELF-49 류).
- `DESC-06` → **open 유지** — note 에 "완료 압력 검사 부재 (수확 · 배치 · 봉인 grep 0) · 접촉 감사 원자료 미반입" 추가.
- `DESC-07` → **claimed_fixed 제안 (생산자 측)** — 단 먼저 `build_handover` 에 coverage 가중평균 관문을 넣거나 README §3 문구를 고칠 것 · 검증 = ML 첫 보고에서 항등식 열을 독립 성능으로 세지 않았는지.
- `DESC-08` → **open 유지** · 배포 README 에 "291/옛 코퍼스와 병합 금지 (d_am=0 40 행 · use_porosity_pct 혼합)" 문장 추가.
- `DESC-09` → **open 유지** → README 에 "RVE 50 µm · 300 MPa · E_SE 1.35 · 2 mAh/cm² 고정 — 고정 finite-box 규약 안의 예측" + 상수 X 열 표기 뒤 claimed_fixed.
- `HND-01` → **claimed_fixed** (`af528e24d` · 수확기 ⑮ HND-01 · J18 철회) — 배포 두께 H_mc 는 별도 질문으로 (Codex 재검 대상).
- `HND-02` → **claimed_fixed** (`af528e24d` · selftest ⑮ HND-02 · 194 수확 `deck_floor.grammar`).
- `HND-03` → **open 유지** + 배포 v1.1 에 `boundary_state` · `physical_target_status` · `hold_reason_codes` (또는 README 에 행 목록) 를 싣는 작업을 note 에.
- `HND-04` → **분할**: 생성기 = claimed_fixed (`af528e24d` · ⑰) · 배포 = 새 항목 (예 `REL-01`: "배포 묶음이 적격성 · 경계 QC · 프로비넌스를 버린다 · 배포 생성 도구 미커밋").
- `HND-05` → **open 유지** 또는 "인계 · 배포" 범위 claimed_fixed (`42e3ca460` · `90c6c9670` · X3/X5) — 웹앱 `porosity_union` 이름 · 쌍 렌즈는 SELF-49/SELF-72 쪽에 남김.
- `HND-06` → **claimed_fixed** (`af528e24d` · selftest ⑮ HND-06) — 웹앱 `parse_mesh_stl` 은 SELF-49 에 남김.
- `SELF-21` → 변경 제안 없음 (open — 도구 없음).
- 새 항목 후보: `REL-01` (위) · 완료 압력 미검사 (DESC-06 잔여를 독립 항목으로) · README 문구 넷 (§4-5).

## 부록 — 스크래치패드 산출물 (세션 scratchpad · 리포 밖)

`probe_now.py` · `probe_now.log` (탐침) · `gen_selftest.log` (207/207) · `repro_lhs_handover.csv` · `repro_lhsx_handover.csv` (+ `_columns.tsv`, 커밋본과 바이트 동일) ·
`repro130.log` · `repro64.log` · `gs_before.txt`.  수확기 selftest 로그는 스크래치패드 최상위 `harvest_selftest.log`.
