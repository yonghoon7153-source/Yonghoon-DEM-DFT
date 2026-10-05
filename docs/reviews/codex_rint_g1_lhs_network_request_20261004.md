# Codex 검토 요청 — r_int G1 재검증 · LHS ④ 수정 (④a 협착 전력 몫 · ④b Love–Weber) · ⑤⑥⑦ 인계 생성기 · 망 경로 (τ ② 도우미 · 띠 규칙) · `stop_after='network'` 구현 (2026-10-04 · 10-05 보강)

> ⛔ **Codex 판정 (10-05) = HOLD · 새 P1 4** — 판정문 `docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` · 증거 `docs/reviews/codex_rint_g1_lhs_network_review_evidence_20261005/` · 원장 `RGL-01`~`10` · 우리 트리 재현 결정값 차이 0.
> RINT claimed_fixed 13 = verified (범위 한정 · `RINT-02` 는 적용 누락 부류만 — 보조 수렴은 `RGL-01`).  이 요청서에서 판정으로 **철회 · 한정**되는 서술 (본문은 발송본 그대로 둔다):
> ① :103 · Q5 *"σ 비트 동일 GOLD 8/8 · GOLD 8 침대"* — 8 = 단언 8 (합성 사슬 3 × 모드 2 · 소수 8 자리 반올림) (`RGL-10`) · 추출 중립성은 Codex 원시 float.hex 18/18 이 따로 지지 ·
> ② §5 설계 결정 (가) *"not_computed 거부"* — 정상 비관통도 생산자가 not_computed 로 내므로 일괄 거부에 반대 (Q11 · `RGL-02`) · T12d 양성 대조의 valid_zero 는 실 생산자가 내지 않는 상태 ·
> ③ §5-2 ④ *"(None · 비지 않은 사유)"* — 내부 예외도 통과 = 명세 자체의 부족 (`RGL-08`) · ④ §1-2 표 Spearman 0.270 · 0.954 — 도구의 동률 처리 결함 (`RGL-09` · 값이 틀렸다는 확정은 아님) ·
> ⑤ C1c *"몫은 경계 전도도 크기와 무관"* — 유한 전극에서 이상 전극 대비 +12.05 % (Q4 · FULL boundary 조건부) · ⑥ 재봉인 — 09-17 cutoff · frozen inventory 를 옮기지 않는다 (안 되면 저자 승인 별도 amendment · Q8).

> **성격** — 코드 재검증 (G1–G4) + 망 경로 구현 리뷰 (G5 · 10-05 1저자 *"먼저 구현하고 같이 요청서로 codex에 보내자"* — 설계만 보내던 계획을 바꿔 구현을 같이 싣는다).  1저자 순서판 (10-04 · *"순서 꼬이지 않게"*) 의 2번: 두 통으로 나눴던 요청 (r_int G1 재검증 · LHS 망 감사) 을
> **한 통**으로 묶는다 — 설계만 보내고 다시 고치는 왕복을 줄이려는 것이다 (coverage 는 5 회 왕복).  발송 = 1저자.
>
> **고정** — 코드 = 이 요청서 커밋 (브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8`).  검토 대상 커밋 (오래된 순):
>
> | 커밋 | 내용 | 원장 |
> |---|---|---|
> | `f1f92d009` | r_int G1-1 — 같은 상 계면 소유 상 강제 · AM je sid 소유권 (`je_definition = am-final-sid-v2`) · 진단 맥락 지문 · je 정의 표지 | RINT-01 · 03 · 11 · 12 · 19 |
> | `3e79aa61c` | r_int G1-2 — 요청 ↔ 네 솔브 적용 영수증 (`run_contract.interface_record_ok` · 세 소비자 공용) · CLI 모순 요청 거부 · 채널 검사 · 레지스트리 | RINT-02 · 13 · 14 · 20 |
> | `9d918d411` | r_int G1-3 — Joule bulk-only 범위 · r-ON STEP4 저장 거부 · r-ON 반응 솔브 비활성 · 상/계면 · 단자 R_int 명명 | RINT-04 · 05 · 17 · 18 |
> | `c911adf05` | τ 결정 16 ② — 안 A 띠 규칙 기록 (`network_conductivity.boundary_sets` 추출 · 동작 중립) · 이온 인계 도우미 `scripts/tau_flux.py` (게이트 G1–G6 · 모드 꼬리) · 웹앱 상태 행 | TAU-14 · 22 · 25 |
> | `2993b8ce8` | LHS 감사 J20-s — ③ φ_SE 마감 · ④–⑦ 1차 · 검사기 `scripts/lhs_stress_constriction_audit.py` | LHS-29 ~ 32 (등재) |
> | `23c3e32be` | RINT-03 실침대 측정 도구 `scripts/rint03_je_compare.py` (읽기 전용) | RINT-03 |
> | `17944f99b` | RINT-03 실측 (§1-2 · 증거 `docs/data/rint03_je_20261005/`) + 도구 수렴 필드 (T5 · T6 — 미수렴을 `UNCONVERGED` 로) | RINT-03 · SELF-85 |
> | `e501d8702` | ④b Love–Weber 입자 응력 새 열 | LHS-29 |
> | `0786e420b` | ④a 협착 저항 전력 몫 새 열 · 옛 행 이름표 · physics 칸 복사 정정 | LHS-30 · SELF-82 |
> | `6e754ec15` | ⑤⑥⑦ 인계 생성기 묶음 (f1 · fracture · area · 명시 제외 · 관문) | LHS-31 · 32 |
> | `14ac9b344` | ②b TAU-03 — 등급 τ · overhead = Hertz 원 솔버 σ + 짝 σ₀ (한 도우미) · COMSOL 2D 두 모드 행 · regime DB (G6 · 선택) | TAU-03 · 16 · SELF-84 |
> | (이 요청서 커밋) | `stop_after='network'` — 망 정지 계약 `pipeline_service.network_stop_verdict` · `app._network_and_stage_e(stop_before_stage_e=…)` · 배치 `--stop-after network` (§5) | — (새 기능 · G5) |
>
> ⚠ `network_conductivity.py` 는 S3 수치 모듈 (`seal_s3_prerun.NUMERIC_MODULES`) 이다 — `c911adf05` · `0786e420b` 가 바꿨다 → S3 전에 **재봉인** (봉인 = 수정 금지가 아니라 재봉인 강제 · τ 결정 16).
>
> ⛔ **값을 인용하는 단계가 아니다** — 아래 real_14 수치는 크기 확인용 (LHS 침대가 아니라 같은 물리 · 같은 덤프 형식의 침대 한 건) 이고, LHS 값은 G5 GO 뒤 배치에서 생긴다.

## §0 요지 — 판정해 달라는 것

| # | 판정 | 대상 |
|---|---|---|
| G1 | GO / HOLD | **r_int G1 재검증** — 위 세 커밋이 claimed_fixed 13 건 (RINT-01 ~ 05 · 11 ~ 14 · 17 ~ 20) 을 닫는가 + RINT-03 실침대 측정 (§1-2) 이 "선언된 예외" (r-OFF 에서도 바뀌는 je) 를 정당화하는가 |
| G2 | GO / HOLD | **④b Love–Weber** — 새 열의 정의 · 검사 · 벽 처리 · 웹앱 표지 (LHS-29) |
| G3 | GO / HOLD | **④a 전력 몫 + 망 모듈 변경** — `constriction_power_share` 정의 (LHS-30) · 안 A 추출의 비트 동일 · 머지 경로 |
| G4 | GO / HOLD | **⑤⑥⑦ 생성기** — 묶음 · 명시 제외 · 관문 ⑤F1 · ⑥R1–R3 · ⑦A1–A5 · 열 사전 한정어 (LHS-31 · 32) |
| G5 | GO / HOLD | **망 경로** — `stop_after='network'` **구현** (이 요청서 커밋 · §5) + `tau_flux` 게이트 + 배치 계획 (130 + 64) + 재봉인 순서.  이 코드로 재봉인 → WSL 배치를 돌려도 되는가 |
| G6 | GO / HOLD (선택) | **②b TAU-03** — 등급 τ · overhead 축 = Hertz 원 솔버 σ + 짝 σ₀ (한 도우미 `tau_flux.tau2_from_metrics` · `se_material.sigma_grain_context`) · COMSOL 2D 두 모드 행 · regime DB (§5-4) |
| Q1–Q10 | 답 | §7 |

## §1 r_int G1 재검증

### §1-1 claimed_fixed 13 건

| 원장 | 판정문 결함 (요약) | 수정 | 시험 |
|---|---|---|---|
| RINT-01 (P1) | r-ON same-sid 면이 AM pid 를 섬유 경계로 읽음 | 같은 상 계면 = AM_P · AM_S 만 (파서 + 솔버) | `scripts/test_rint_receipts.py` · `step3_sigma.py --selftest-rint` |
| RINT-02 | 주 솔브만 검사하면 wetted/bare 누락 변이가 초록 | 요청 ↔ 네 솔브 적용 영수증 — producer 게시 전 · `check_arm` · 판정기 공용 · AST 변이 4/4 거부 | 〃 |
| RINT-03 | iid 만으론 r-OFF 입자별 AM 전류 오염 (121–127×) | je = 최종 sid AM 셀만 (`je_definition = am-final-sid-v2`) — **r-OFF 에서도 바뀌는 선언된 예외** | 〃 + §1-2 실침대 |
| RINT-04 | Joule 지도 = bulk 만 | `bulk_only` 범위 표지 · 지도 밖 계면 몫 기록 | 〃 |
| RINT-05 | STEP4 · reaction = 막 없는 scope | r-ON + STEP4 저장 거부 · r-ON 반응 솔브 끔 | 〃 |
| RINT-11 · 12 · 13 · 14 · 17 · 18 · 19 · 20 (P3) | ULP · 형 변환 · compare_dirs · 모순 CLI · 명명 · 뷰어 · 진단 맥락 · 레지스트리 | 각 커밋 메시지 · 원장 note | 〃 |

열린 채 (G2 · 설계): RINT-06 ~ 10 · 15 · 16 — 순서판 5번 (①′ v2 초안) 에서.

### §1-2 RINT-03 실침대 측정 — **kgy 실측 10-05 (세 그리드 · 세 해 수렴)**

- 도구: `scripts/rint03_je_compare.py` (읽기 전용 · selftest 9/9 — 10-05 에 T5 · T6 수렴 계약 추가, 아래 ⚠) — `step4_grid.npz` → σ_e 재풀이 (r 끔 · payload 와 같은 z_top · z_bot = origin_shift z · periodic) →
  **같은 해**에서 입자별 AM 전류 옛 정의 (pid ≥ 0) ↔ 새 정의 (`am-final-sid-v2`) · 복제 새 정의 = `per_particle_current` 검산 (다르면 거부 — 세 그리드 모두 통과).
- 그리드 = 킷의 실제 `step4_grid.npz` (vox 0.4 µm) — payload 가 옛 je 를 계산한 **바로 그 배열**이다 (`mpm_webapp_payload.py` 의 `per_particle_current` 호출과
  `--save-step4-grid` 저장이 같은 sid3 · pid3 · σ_e 표 · z_top 을 쓴다).  재풀이 = CPU Jacobi-CG.
- 수렴: 세 로그 모두 `⚠ STEP3 CG not converged` 줄이 없다 (그 줄은 info ≠ 0 또는 resid > 1e-6 일 때 찍힌다).  ⚠ 실행 당시 판은 JSON 에 `cg_info` · `resid` 를 싣지 않았다
  (미수렴이어도 `status: OK` — 자기 결함 `SELF-85`) → 이 측정의 수렴 증거는 **로그 줄**이고 (증거 README 에 전문), 도구는 이 커밋에서 고쳤다 (수렴 계약을 못 채우면 `UNCONVERGED`).

| 침대 | 격자 · dof | AM 입자 | 오염 입자 | AM 번호를 단 비-AM 셀 | 옛 je 질량 중 비-AM 셀 몫 | 옛/새 비 중앙 · p90 · 최대 | 비 > 1.1 · > 2 | Spearman | top 10 % 겹침 | 재풀이 σ_e (검산용) |
|---|---|---|---|---|---|---|---|---|---|---|
| VGCF 4 wt% · PTFE 1 wt% (`VGCF_PTFE_4_1`) | 126×126×316 · 3,589,135 | 1,498 | **1,498 (100 %)** | 93,352 | **97.4 %** | **42.6 · 91.9 · 204** | 1,498 · 1,495 | **0.270** | **14 %** | 4.15 S/cm |
| VGCF 1 wt% · PTFE 1 wt% (`VGCF_PTFE_1_1`) | 126×126×292 · 2,724,342 | 1,498 | 1,497 | 26,649 | 6.4 % | 1.05 · 1.22 · 27.3 | 348 · 33 | 0.954 | 91 % | 5.29 × 10⁻³ S/cm |
| ps45 5:5 (`kit_ps_5_5_r45` — AM + SE 만) | 125×125×284 · 2,297,784 | 2,491 | 0 | 0 | 0 % | 1 · 1 · 1 | 0 · 0 | 1.000 | 100 % | 1.05 × 10⁻³ S/cm |

읽기:
1. **탄소 망이 σ_e 를 지배하는 침대 (4 wt% — 재풀이 σ_e 가 1 wt% 의 약 780 배) 에서 옛 je 는 AM 전류가 아니라 탄소 전류였다** — 옛 je 질량의 97.4 % 가
   AM 번호를 물려받은 비-AM 셀 (탄소) 에서 왔고, 모든 입자가 오염됐으며 (비 중앙 42.6×), 입자 순위가 거의 무관하다 (Spearman 0.27 · top 10 % 겹침 14 % — 무작위 기댓값 10 %).
2. **탄소가 σ_e 를 지배하지 않는 침대 (1 wt%) 는 평균이 작고 꼬리가 있다** — 비 중앙 1.05× · 옛 je 질량의 6.4 % · 순위 대체로 유지 (0.954) — 그러나 33 입자는 2 배 넘게, 최대 27 배 부풀었다.
3. **AM 셀을 덮은 비-AM 셀이 없는 침대에서는 두 정의가 같다** (음성 대조 — 비 1 · Spearman 1).  SE 158,766 개 침대에서 0 이므로 SE 는 AM 번호를 남기지 않는다
   ⇒ VGCF 침대의 셀 수는 첨가제 (VGCF · PTFE) 스탬프 몫이다.

⇒ "선언된 예외" (r 를 끈 산출에서도 je 가 바뀐다) 의 크기 = **첨가제가 AM 셀을 덮는 정도 × 탄소 망이 전류를 나르는 정도**.  탄소가 σ_e 를 지배하는 침대에서 옛 je 는 다른 양
(탄소 전류) 이었으므로 정의를 고치지 않을 길이 없다는 것이 우리 판단이다 (Q2).

한정어:
- 값은 **vox 0.4 격자의 값**이다 — VGCF (Ø 0.15 µm) 가 한 셀 폭으로 찍혀 단면이 약 9 배 (CL-11 의 σ 직경보존 재척도는 전도도만 보정한다) 이고 AM 경계 셀을 덮는다
  ⇒ 오염의 **크기**는 격자 의존이다.  **방향** (옛 je 에 탄소 전류가 섞인다) 은 정의에서 나온다.
- σ_e 열은 같은 해의 재풀이 검산값이다 — 인용값이 아니다 (vox 0.4 = 격자 미수렴 축, CL-24).
- `n_carbon_cells_with_am_pid` (표의 "AM 번호를 단 비-AM 셀") 는 이름과 달리 PTFE 등을 포함한 비-AM 셀 **전부**를 센다.  전류는 도체만 나르므로 질량 몫은 탄소 몫이다
  (도구 머리말에 명시 · 열 이름은 이미 낸 JSON 과 맞추려고 그대로 둔다).
- 증거: `docs/data/rint03_je_20261005/` (JSON 셋 = 1저자 붙여 넣기 · 도구 형식 재직렬화와 일치 · 로그 줄 · 실행 명령).

## §2 ④b Love–Weber 입자 응력 (LHS-29 · `e501d8702`)

- 결함: 옛 `stress_cv` · `stress_ratio_<상>` = LIGGGHTS `compute stress/atom` ÷ 입자 부피 — 접촉 virial 을 두 입자에 0.5 · (x_i − x_j) ⊗ F 로 똑같이 나눈다
  (공개 소스 `pair_gran_base.h` `ev_tally_xyz` · `pair.cpp` `Pair::ev_tally_xyz`).  크기 다른 쌍에서 큰 입자 과소 · 작은 입자 과대.
- 새 정의: σ_i = (1/V_i) Σ_c (x_c − x_i) ⊗ f_c (접촉점 c_cpl[24–26] · 힘 c_cpl[10–12] · 인장 양수 · x·y 최소영상) · VM = 전체 텐서 대칭부 ·
  요약 통계 = 옛 열과 같은 정의 (규약만 다름).  `LW_DEFINITION = love_weber_branch_full_tensor_v1`.
- 검사 (실패 = 값 키 없이 상태에 사유): 열 · 유한값 · id 짝 · max|F − (Fn + Ft)|/max|F| ≤ 1e-3 · 접촉점 ≤ 1.01 r · 전체 virial Σ V σ_LW = Σ c_strs ≤ 1 % (real_14 5.0e-5).
- 벽: 바닥 z − r < 0 · 판 z + r > plate_z (mesh 일 때만) · 옆면 = x·y 주기 가정 (덱을 읽지 않는다).
- real_14: CV 213.1 → **120.7 %** · AM_P 0.884 → **2.737** (벽 제외 3.016 · AM_P 벽 접촉 41.7 %).
- 시험: `scripts/test_love_weber_stress.py` 42/42 · `webapp/test_stress_lw_labels.py` 33/33.
- 안 한 것: 등급 축 전환 (값 = 재분석 뒤 · 등급값 보고 뒤) · `stress_z_layer_cv` LW 판.

## §3 ④a 협착 저항 전력 몫 + 망 모듈 변경 (LHS-30 · `0786e420b` · `c911adf05`)

- 결함: `bulk_resistance_fraction` = 간선별 R_bulk/R_total 의 **비가중 평균** (L2-08 = 이름표만) → 거시 전력 몫 아님 (real_14 이온 hertz 0.766 ↔ I²R 가중 0.786).
- 새 열: `constriction_power_share_{ion,el,th}_{hertz,physics}` = **같은 FULL 해**의 Σ I²R_c / Σ I²R_total (관통 간선만 · 가상 전극 연결 제외) + `_status`
  (관통 없음 = None · 0 으로 안 채움).  `run_decomposition` 이 FULL 해를 늘 전류장과 함께 받는다 (해는 같다 — σ 비트 동일 GOLD 8/8).
- 머지: hertz = `network_conductivity.json` → `NET_MERGE_KEYS` · physics = dual 에서 이름 그대로 (`NET_PHYSICS_TAILED_KEYS`) · 스캐너 같은 규칙.
- 안 A (`c911adf05`): `boundary_sets` 추출 (추출 전 기준값과 비트 동일) · `boundary_rule` L0/L1/L2 · `boundary_band_frac` (이온 · 전자 · 열) 기록.
- real_14 (감사기 6/6): 이온 hertz 78.6 % · physics 82.8 % · 전자 83.3 / 83.0 · 열 61.6 / 54.4.
- 시험: `scripts/test_constriction_power_share.py` 16/16 · `webapp/test_constriction_power_labels.py` 21/21 · `scripts/test_network_boundary_rule.py` 8/8.

## §4 ⑤⑥⑦ 인계 생성기 (LHS-31 · 32 · `6e754ec15`)

- 묶음 (`lhs_design_dataset.py --webapp-groups … f1,fracture,area` · 셋 다 접촉 단계 산출): ⑤ `se_se_cn_aug` · `_std` · `_n_extra` · `_h_spread_sim` ·
  ⑥ `fracture_index_force` · `n_total_AM_AM_force` · `frac_<단계>_force_pct` × 5 · `n_<단계>_force_AM_AM` × 5 (힘 기반 전체 집계만) ·
  ⑦ `area_<쌍>_mean` · `_total` (쌍 7) · `se_se_cn_eff_area` · `_perc` · `am_am_mean_area` · `am_am_total_area`.
- 명시 제외 (`WA_EXCLUDED` — census ✅ 여도 먼저): `path_hop_area_*` (선별 표본 · LHS-32) · δ 판 파괴 · 상 쌍별 파괴 (분모 max(n, 1)) · physics 면적 (J20-m).
- 관문 (웹앱 원 행으로): ⑤F1 aug = se_se_cn + 2 · n_extra / N_SE · ⑥R1–R3 단계 합 = 전체 · 반올림 반폭 (0.005 · 5e-5) · 전체 ≤ am_am_n_contacts ·
  ⑦A1–A5 평균 × 개수 = 총합 · 접촉 0 쌍 = 평균 N/A · 총합 0 · AM전체 = 상별 합 · AM–AM 총합 = 쌍 합 · eff_area = 2 · area_SE_SE_total / (N_SE · 4π r_SE²) · eff_area_perc 빈칸 ⟺ 비관통.
- 10-01 원자료 (`d1ec42fba`) 메모리 실행: 130/130 · 64/64 통과 (인계표 재생성 = G5 뒤).
- 시험: `lhs_design_dataset.py --selftest` 233/233 (㉕a–z 26 먼저 실패 확인) · `webapp/test_s567_labels.py` 13/13.

## §5 망 경로 — `stop_after='network'` (구현 · 이 요청서 커밋 · 코드와 설계를 판정해 달라)

### §5-1 왜

τ 인계 (tau2 · f · 결정 16) 와 ④a 는 **망 단계**에서만 생긴다.  지금 배치 (`scripts/lhs_webapp_batch.py`) 의 정지점은 `contact` · `coverage` 뿐이고,
`stop_after=None` (전체) 은 Stage E · 그림 · 고급 분석 · 자동 DB 까지 돈다 (건당 575–743 s).

### §5-2 구현 (설계 10-04 → 구현 10-05 · 시험 먼저)

| 항목 | 구현 |
|---|---|
| 값 | `app.PIPELINE_STOP_AFTER = (None, 'contact', 'coverage', 'network')` — 밖의 값은 ValueError (지금 규칙 그대로 · `Network` · `network ` 도 거부) |
| 정지 위치 | `app._network_and_stage_e(…, stop_before_stage_e=True)` — network solver (지금 lock · stash · 내용 verify 그대로) → baseline 머지 → 채널 판정 → **망 정지 계약** → return.  Stage E · 이중 공극률 · 그림 · 고급 분석 · 자동 DB 는 돌지 않는다.  피복 단계는 전체 실행과 같은 optional 계약.  멈추기 전 명령 = 전체 실행의 앞부분 (인자까지 같다) |
| 내용 계약 (`pipeline_service.network_stop_verdict(results_dir, run_id)` · required 단계 · fail-closed) | ① `network_content_verdict(strict=True)` ② full_metrics `network_run_id` · `active_network_run_id` = **이번 실행** run_id · `network_solver_status` = success ③ 두 모드 dual `sigma_full_status` ∈ {computed, valid_zero} — computed 면 full_metrics σ (`sigma_full_mScm` · `sigma_full_mScm_physics` = `tau_flux.METRIC_SIGMA_KEY`) 가 dual 의 **같은 값** (양수), valid_zero (비관통) 면 둘 다 None ④ 두 모드 `constriction_power_share_ion_<꼬리>` + `_status` — full_metrics = dual 이고 (값 0–1 · computed) 또는 (None · 비지 않은 사유) ⑤ dual 두 모드 `boundary_rule` ∈ {L0, L1, L2} (생산자 `BOUNDARY_RULES`) · `boundary_band_frac` 유한 양수.  하나라도 어기면 단계 `Network stop contract (stop_after=network)` 실패 → `failed` |
| ★ 설계에 없던 결정 둘 | (가) ③ 에서 `sigma_full_status = not_computed` 를 **거부** — 이온 채널 판정은 σ None 을 `valid_null` (ok) 로 통과시켜 '비관통' 과 '못 풂' 을 못 가른다 · 계약은 원 σ 상태로 가른다 (Q11) (나) `stop_after='network'` + `preserve_network=True` → **ValueError** — 망을 새로 푸는 정지점에 solver 미호출 · 옛 세대 복원을 섞지 않는다 (계약 ② 도 run_id None 이라 실패) (Q11) |
| 상태 | `_stopped_after(stages, log, 'network', network_run_id=…)` — 끝의 판정과 같은 `summarize` · 반환에 이번 실행 `network_run_id` (contact · coverage 는 None 그대로) |
| atoms-only | `LHSC-02` 규칙 그대로 — `stop_after='network'` 도 계산 · 도장 · 러너 호출 없이 failed (T11g 에 network 추가) |
| 배치 | `lhs_webapp_batch.py --stop-after network` · status.json `stop_after` · 케이스 기록에 `network_run_id` · 다른 정지점 · 전체 폴더와 섞기 거부 (어느 방향이든 rc 2) |
| 시험 | `webapp/test_pipeline_provenance.py` **217/227 → 227/227** (옛 코드 실패 10 = T11g × 2 · T12a × 2 · T12b × 2 · T12c · T12d · T12f · T12g) — T12a 두 모드 끝 = network solver · Stage E · 이중 공극률 · 고급 분석 없음 · 반환 run_id = full_metrics 도장 · physics σ 머지 / T12b 명령 = 전체 실행 앞부분 / T12c 계약 변이 9 종 (③ physics not_computed · computed 인데 σ None · legacy ≠ Hertz 세대 섞임 · ④ 값 · 상태 둘 다 없음 · 1.3 · None 인데 computed · ⑤ 띠 규칙 없음 · L9 · 띠 폭 NaN) 전부 failed / T12d 양성 대조 (SE 비관통 두 모드 valid_zero · 띠 폴백 L1) done / T12e preserve → ValueError / T12f solver rc 1 → failed · Stage E 없음 / T12g ② 다른 run_id · None 거부 · `lhs_webapp_batch.py --selftest` ⑲ · ⑳ (옛 파서 = `SystemExit 2` · 섞기 통과 → 고친 뒤 통과) |
| 웹앱 화면 | 해당 없음 — `stopped_after` 는 배치 전용 필드이고 화면에 정지점 표시가 없다 (J20-l: 없음을 적는다) |
| 그다음 | `scripts/tau_flux.py <케이스 폴더>…` → f · tau2 · tau (두 모드) · 게이트 G1–G6 (§5-3).  tau_flux 입력의 장부 (L_gap · L_mc · φ_mc) · `percolation_pct` 는 **접촉 단계** (`analyze_contacts` — bimodal 도 같은 함수) 가 쓰므로 Stage E 앞 정지로 빠지는 입력이 없다 |
| 재봉인 | 구현 (이 커밋) → **Codex GO** → (판정 반영 수정) → 게이트 → **재봉인** (`seal_s3_prerun` · `network_conductivity.py` 가 S3 수치 모듈) → WSL 배치.  배치와 S3 가 같은 봉인 수치 모듈을 쓰게 한다 |

### §5-3 `tau_flux` 게이트 (`c911adf05` · 결정 16 §5-2)

| 순서 | 게이트 | 실패 시 |
|---|---|---|
| 0 | 그 모드 망 결과 · 장부 (L_gap · L_mc · φ_mc) · calc_percolation 값 | `NOT_COMPUTED` (`missing_input`) |
| 1 | G1 띠 = 솔버 기록 `boundary_rule` L0 (기록 없는 옛 산출물은 짐작 안 함) | `BAND_FALLBACK` |
| 2 | G2 솔버 관통 == calc_percolation (`sigma_full_status` 로 판정 안 함) | `NOT_COMPUTED` (`percolation_disagree`) |
| 3 | G4 온도 짝 (두 모드 σ₀ · T 같음) | `NOT_COMPUTED` (`temperature_mismatch`) |
| 4 | G3 비관통 | `NOT_PERCOLATING` — f = 0 · tau2 · tau 빈칸 |
| 5 | 관통인데 σ 없음 · 0 · 비유한 | `NOT_COMPUTED` (`solver_guard`) |
| 6 | G5 f > φ (T < 1) | `MODEL_BELOW_CONTINUUM_BOUND` — 값 유지 + 표지 |

G6 = 메타 `ion_net_constriction_<m>` · 두 모드 다 물리 타깃 HOLD (값은 싣는다).  시험 `scripts/test_tau_flux.py` 35/35.

### §5-4 ②b TAU-03 (커밋 `14ac9b344` · 원장 `0ab9c6c4f` · 1저자 비준 10-04 밤)

- 등급값 보고 (case_master 157): 옛 등급 τ 축 = Stage-E physics σ 157/157 + σ₀ 3.0 고정 → Hertz 로 바꾸면 τ 축 107 바뀜 (전부 좋아짐) · overhead 122 · 종합 3.
- 도우미: `tau_flux.tau2_value(φ, σ₀, σ)` · `tau2_from_metrics(metrics, mode)` (mode = hertz · physics · bulk · physics 없으면 None) · σ₀ = `se_material.sigma_grain_context` (웹앱 함수를 옮김).
- 소비처: 웹앱 τ 블록 · 등급 τ · τ_bulk · overhead · COMSOL 2D (f_ion_<mode> · tau2_ion_<mode> · Stage-E 행 τ 이름 없음) · regime DB.
- 시험: `webapp/test_tau_grade_unify.py` 19/19 (옛 코드 1/19) · `webapp/test_tau_labels.py` 43/43 · `grade_engine.py --selftest`.
- 그대로: ASR 축 · σ_ionic Stage E 축 (τ 아님) · ④a/④b 등급 축 전환 (값 = 재분석 뒤).

## §6 이 묶음이 바꾸지 않는 것

- 등급 축 ④b CV(σ_VM) · ④a 협착 비율 — 코퍼스 재분석 값이 생긴 뒤 등급값 보고 → 1저자 비준 (τ 축은 §5-4 로 이미 바뀜).
- 인계표 · 배포본 — G5 GO → 배치 → tau_flux → v1.2.
- r_int ②–⑥ · ①′ 면적 규약 (RINT-06 ~ 10) — 순서판 5번.

## §7 질문

- **Q1 (G1)** — RINT-02 처방 (영수증 · AST 변이 4/4) 이 wetted/bare 변이 **부류**를 닫는가, 아니면 그 넷만 닫는가.
- **Q2 (G1 · RINT-03)** — `am-final-sid-v2` 를 r-OFF 에서도 바뀌는 "선언된 예외" 로 두는 것이 맞는가 (§1-2 실측과 함께).  옛 je 를 쓰던 소비처 (STEP4 · 뷰어) 에 남은 것이 있는가.
- **Q3 (G2)** — 벽 판정 (바닥 z − r < 0 · 판은 mesh 일 때만 · 옆면 주기 가정) 과 virial 1 % 검사가 LHS 침대 (주기 x·y · 판 mesh) 에 충분한가.  비대칭 ‖σ − σᵀ‖/‖σ‖ 중앙 0.0105 를 대칭부로 처리하는 것이 맞는가.
- **Q4 (G3)** — 전력 몫에서 가상 전극 연결 간선의 소산을 빼는 것이 맞는가 (분모 · 분자 둘 다).  비관통 = None (0 아님) 규칙.
- **Q5 (G3)** — 안 A 추출 뒤 비트 동일을 GOLD 8 침대로 본 것이 충분한가.
- **Q6 (G4)** — 반올림 반폭 관문 (0.005 · 5e-5) · 접촉 0 쌍 총합 0 채움 (평균 N/A) · `path_hop_area` · 상 쌍별 파괴 제외의 근거가 충분한가.
- **Q7 (G5)** — 정지 위치 (Stage E 앞) 와 내용 계약 ①–⑤ (`network_stop_verdict`) 가 충분한가.  빠진 키 · 상태는.  같은 세대 판정을 full_metrics ↔ dual **값 일치**로 본 것이 맞는가.
- **Q8 (G5)** — 재봉인 순서 (구현 → 게이트 → 재봉인 → 배치) 가 맞는가.  배치를 봉인 전에 돌리면 무엇이 깨지는가.
- **Q9 (G6)** — 등급 · COMSOL 의 τ 를 원 솔버 Hertz σ + 짝 σ₀ 로 통일한 것이 결정 6 을 닫는가.  COMSOL 2D 에서 두 모드 행 + Stage-E 행 (짝 아님 경고) 구성이 오용을 막는가.
- **Q10** — 그 밖에 이 경로에서 보이는 P1.
- **Q11 (G5 · 설계에 없던 결정)** — (가) `sigma_full_status = not_computed` 거부가 맞는가 (못 푼 침대가 done 으로 넘어가지 않게 — 대신 그런 침대는 배치에서 failed 로 남는다).  (나) `preserve_network` 와 `stop_after='network'` 를 ValueError 로 막은 것이 맞는가.

## §8 출력 형식

- 발견마다 P1 / P2 / P3 · file:line · 재현 · 최소 수정.
- G1 ~ G6 각각 GO / HOLD + 해제 조건.
- Q1 ~ Q10 답.
- 우리 시험을 고정 트리에서 다시 돌린 결과 (같은 값인지).

## §9-1 RINT-03 실측 명령 (kgy · 1저자 실행 · 원 체크아웃의 HEAD 는 바꾸지 않는다)

```bash
# ① 브랜치 끝을 임시 워크트리로 (원 체크아웃 ~/dem-vgcfE 의 HEAD 는 그대로)
cd ~/dem-vgcfE && git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8
git worktree remove --force /tmp/rint03_wt 2>/dev/null; git worktree add --detach /tmp/rint03_wt FETCH_HEAD
cd /tmp/rint03_wt && git log --oneline -1 && python3 scripts/rint03_je_compare.py --selftest
# ② 후보 그리드 찾기 (첨가제 · 탄소가 찍힌 침대일수록 의미가 있다 — 크기 순)
find ~ -name step4_grid.npz -size +1M -printf '%s\t%TY-%Tm-%Td\t%p\n' 2>/dev/null | sort -n | tail -20
# ③ 고른 그리드 (작은 것 하나부터 · 큰 그리드는 σ_e 재풀이에 메모리가 많이 든다)
python3 scripts/rint03_je_compare.py <GRID.npz> [<GRID2.npz>] --json ~/rint03_je_20261004.json
# ④ 정리 (선택)
cd ~/dem-vgcfE && git worktree remove --force /tmp/rint03_wt
```

## §9 재현

```bash
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git checkout FETCH_HEAD
python3 scripts/step3_sigma.py --selftest-rint
python3 scripts/test_rint_receipts.py
python3 scripts/rint03_je_compare.py --selftest
python3 scripts/test_love_weber_stress.py
python3 scripts/test_constriction_power_share.py
python3 scripts/test_network_boundary_rule.py
python3 scripts/test_tau_flux.py
python3 scripts/lhs_design_dataset.py --selftest
python3 webapp/test_stress_lw_labels.py && python3 webapp/test_constriction_power_labels.py && python3 webapp/test_s567_labels.py
python3 webapp/test_tau_grade_unify.py && python3 webapp/test_tau_labels.py && python3 scripts/grade_engine.py --selftest
python3 scripts/lhs_stress_constriction_audit.py --selftest
python3 webapp/test_pipeline_provenance.py          # T12 망 정지 (stop_after='network') · T11g atoms-only
python3 scripts/lhs_webapp_batch.py --selftest      # ⑲ · ⑳ --stop-after network
```
