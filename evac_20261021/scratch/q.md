# Codex 설계 리뷰 요청 — 탄소 접합 Rint ② + 첨가제 물리 (S0 · S1 · S2 v0 · S3 · 등록 R 초안) + Part B 조인 수정 재확인 (2026-10-20 · 결과 0 건 · 초안 · 발송 = 1저자)

## 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| **Part A** — 설계 v1 의 단계별 GO/HOLD (S0 · S1 · S2 v0 · S3 — "이 설계로 시험 먼저 → 구현에 들어가도 되는가") · 등록 R 초안의 판정 구조 (식별성 · holdout 오염 선언 · 구간 정보량 · 판정표 · 측정 한정어 · 금지 문장 — "무의미한 통과를 막는가") | 구현 · 시험 실행 결과 (코드 0 줄) · 수치 (런 0) · ①′ 정량 채택 · 생산 · 10-20 제출본 수치 · 현 세대 σ* (0.347 · 2.618) · 원고 · v1 (VA · SV · SA 간선 · 공동 점유 · SDCP 경유 새 간선 · 주기 정량 · 판 결합 면 α) · Super P · 역학 · SE 입계 ③ · Lee 2025 두 번째 holdout |
| **Part B** — 조인 수정 `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` (부분) · `SELF-124` 재확인 (지난 회차 판정문 §3 · §4 · §7 의 최소 해결) | `RIMPR-04` 전체 (결과 유한성 · 수치적으로 안정한 거리 · 오차폭 계산 = ①′ 정량 채택 전 · 원장 open 유지) · 조인 형식 검증 전체 완결 선언 |

> **범위 (Part A)**: 설계만 · 다음 세대 · 10-20 제출본 소급 없음 · 생산 규약 그대로 (PTFE `centerline` `CL-60` · 현 세대 σ*_VGCF · 브리지 0.48 µm · ①′ HOLD) · 모든 스위치 기본 끔 · 끄면 비트 동일 (계약 · 구현 전).
> **리뷰 핀** = ⬜ (메인이 채운다) · 대상 문서 셋 = 이 요청서와 같은 커밋 · 근거 계획 = 통합 계획 v1 (반입 커밋 `f507bdc74` — 리뷰 핀의 조상).
> **한 줄**: 1저자 10-20 범위 (*"PTFE 실제 부피 · 막 + SDCP 계면 + 맨 접점 R_c 보정 · SBE + 독립 자료로 정하고 DBE 는 예측 · 예측 전 합격 기준 등록"*) 를 통합 계획 v1 Q1–Q12 (✅ 권고대로) 위에서 단계별 구현 규칙 · 계약 · 먼저 쓸 시험 · 등록 판정 구조로 옮겼다.  지난 HOLD 부류 (R18 의 식별성 · 허용창을 신뢰구간처럼 · G2 의 구간 · 순서 · 단위 · 증서 결합 · 세대 섞임) 를 미리 막으려 했다 — 막지 못한 자리를 찾아 달라.

## 0. 보내는 것 (ZIP · 리뷰 핀의 blob 그대로)

| 묶음 | 파일 |
|---|---|
| 대상 셋 | `docs/reviews/rint_carbon_additive_design_v1_20261020.md` (설계 v1) · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (등록 R 초안) · 이 요청서 |
| 근거 계획 · 초안 | `docs/reviews/rint_carbon_additive_plan_20261020.md` · `docs/reviews/rint_carbon_junction_brief_20261020.md` · `docs/reviews/additive_physics_brief_20261020.md` |
| 계약 정본 | `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` · `docs/reviews/contact_resistance_pipeline_draft_v3_20261006.md` · `docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md` |
| 지난 판정 | `docs/reviews/codex_r18_verdict_20260831.md` · `docs/reviews/ptfe_convention_prereg_20260829.md` · `docs/reviews/codex_review_rint_g2_design_20261006.md` · `docs/reviews/codex_review_rint_g2_v3_20261007.md` · `docs/reviews/codex_review_rint_g2_impl_20261014.md` · `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` · `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` |
| 현 세대 앵커 · 지위 | `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` · `docs/voxel_contact_free_gap.md` · `docs/reviews/sdcp_ion_calib_prereg_20260825.md` · `docs/reviews/lee_abs_sigma_e_prereg_20260923.md` |
| 붙을 코드 (읽기만) | `scripts/step3_sigma.py` · `scripts/mpm_webapp_payload.py` · `scripts/run_contract.py` · `scripts/fibre_segment_raster.py` · `scripts/fibre_1d_network.py` · `scripts/pellet_rve_sigma.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/sdcp_gain_verdict.py` · `webapp/mpm_lab_register.py` |
| Part B | `scripts/rint_iface_join.py` · `scripts/test_rint_g2_join.py` · `docs/reviews/rimprr_fix_plan_20261020.md` · `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/` (넷) |
| 카드 (정본 가지 · 읽기만) | `endo2001_vgcf_basic_properties_battery_applications` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `bazzoun2026_dem_fem_rnm_ionic` (가지 `origin/claude/friendly-meitner-lldvar`) |

---

## Part A — 설계 리뷰

### A-0. 사전 점검 (CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ①–④)

| 단계 | 결과 |
|---|---|
| ① 숫자 · 전칭 ↔ 출처 | 아래 A-0-1 표 (작성자가 한 줄씩 대조) · 설계 · R 의 *"비트 동일"* · *"no-op"* · *"정확"* 은 **계약 (구현이 지켜야 할 것)** 이지 측정된 사실이 아니다 — 구현 · 시험 전 |
| ② HOLD 부류 | 설계 §3-3 · §4-3 · §5-3 계약 표가 부류마다 한 줄 (NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 유니코드 숫자 · 증서 ↔ 결과 결합 · 다른 판본 증서 · 세대 섞임) — 함수가 아직 없어 "직접 돌리기" 는 시험 먼저 단계 (설계 §8) 에서 |
| ③ 독립 에이전트 반례 찾기 | ⬜ (메인이 채운다 — 작성자 설명 없이 문서 셋만 준 독립 리뷰 · 찾은 것은 고치거나 여기 한정으로) |
| ④ 닫는 것 / 닫지 않는 것 | 맨 위 표 |

#### A-0-1. 숫자 ↔ 출처 (설계 · R 에 쓴 것)

| 숫자 | 출처 |
|---|---|
| SBE 1.63 · DBE 4.68 mS/cm · 비 2.86 · 7.016 / 2.178 Ω · 90 / 80 µm · 지름 10 mm · 쌍 저항 7.003–7.023 / 2.141–2.199 Ω | 등록 v2 §1 |
| σ* 0.347 S/cm · SBE 8 팔 1.6209 · DBE 1.8877 · 비 1.1646 · DBE 8 팔 CV 0.28 % · σ_VGCF 2.618 (×7.54) · S2 2.54 (×7.32) · DBE dof 26,734,242 · 반복 30,000 미수렴 → 60,000 · SBE 704–992 s · DBE 2,578–3,054 s | 등록 v2 §7 |
| 시딩 138,988 → 116,532 점 | 등록 v2 §7 R2 |
| VGCF 1 × 10⁻⁴ (흑연화) · 1 × 10⁻³ Ω·cm (탄화) · p. 1289 stated | [카드] Endo 2001 |
| 7,853.98 · 11,309.7 S/cm (직경 보존 · vox 0.15 · 0.125) · 대비 1.9 × 10⁶ · 축방향 g ≈ 1.2 × 10³ | [우리 산술] |
| rope Ø0.248 · fibre Ø0.048 µm · 개수 13 : 87 (N = 100) | [카드] Lee 2025 EES Fig. S2c |
| 캡슐 부피 ≈ 0.88 V_true · (다) 표현 부피 ≈ 0.16 배 | [우리 산술 · 추정] (잘림 −10.3 % = 초안 additive brief §1 · `CL-67`) |
| PTFE V_true 2,580.52 / 1,290.26 µm³ · centerline 표현 비 0.4278 / 0.4222 · 2 배 밴드 | `docs/reviews/ptfe_convention_prereg_20260829.md` §2 · 측정 결과 |
| Q 0.840 · Lee 보간 0.44 | `docs/reviews/lee_abs_sigma_e_prereg_20260923.md` §5 |
| Lee 2026 1.0/0.5 wt% 비 0.70 · VGCF 83 S/cm · ±3 % | [카드] Lee 2026 Small Table S2 · p. 13 |
| PTFE 0.5 / 2 / 5 wt% → σ_e 34 / 4.5 / 0.011 mS/cm | [카드] Lee 2025 Nat. Commun. SI Fig. 5 stated |
| 펠릿 이온 3.57 / 0.97 / 2.86 mS/cm · 전자 0.30 / 0.12 / 1.53 × 10⁻⁷ S/cm · PTFE 9.17 · SDCP 14.60 vol% | `docs/reviews/sdcp_ion_calib_prereg_20260825.md` §1–2 |
| σ_NCM 0.0041 · σ_SDCP 256.6 S/cm | `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md` 15 행 · 등록 v2 §2 |
| G0 = ln(4.68/1.8877) = 0.908 · 0.454 (×1.57) · 0.908 (×2.48) · 0.1 G0 = 0.091 · R_S/R_D ≈ 3.2 | [우리 산술] |
| vox 0.125 dof 45.4 M | CLAUDE.md SR-01 절 (CL-41 계열 실측) |
| SDCP 구 게이트 d/vox ≥ 2 | `scripts/step3_sigma.py` 666 행 |

### A-1. 단계별 GO/HOLD

| Q | 단계 | 묻는 것 |
|---|---|---|
| A1 | S0 | σ 칸이 없는 기하 census (설계 §2) 로 문턱 (tol_ff · L_par · r_port · tol_P · tol_sj · 긴 접촉 법칙) 을 정하고 R 개정 (결과 0 건) 으로 커밋한 뒤 σ 를 여는 절차가 "결과 전 등록" 과 충돌하지 않는가 (초안 junction brief §6 Q9) · B0 를 이 리뷰와 병렬로 해도 되는가 |
| A2 | S1 정의 | 면 개구율 연산자 (K × K 중점 구적 · 불투과 · g = α·g0 · 같은 물체 안 면 면제 ⓐ–ⓒ · α = 0 = 절단 연결성 · 판 결합 미적용) 가 R18 Q6 의 "보존형 capsule face 연산자" 와 같은 물건인가 · 면제 규칙 (같은 sid 탄소 · SDCP · 같은 pid AM 면 제외 / SE\|SE 는 적용) 이 '자르기' 인공물을 빼면서 새 인공물을 만들지 않는가 |
| A3 | S1 이중 계상 | `ptfe_stamp` 축의 새 값 (`face_alpha` · `capsule` 예약값과 다른 이름) + sid 격자 = `off` 격자 + `ptfe_cells_observed` = 0 실물 검사로 centerline 과의 이중 계상이 닫히는가 |
| A4 | S1 지름 · 부피 | (가) "rope Ø0.248 단일 + 시더 부피 처방 길이 그대로" 의 읽기 · 캡슐 부피 비에 `CL-60` 등록의 2 배 밴드 [0.5, 2] 를 S1 사용 관문으로 다시 쓰는 것 · (다) 개수비 분할 (부피 0.16 배) 을 판정 표지에서 빼고 보고만 하는 것 |
| A5 | S1 종료조건 | 설계 §3-4 F1–F15 가 R18 종료조건 8 (α = 1/0 · 상호성 · KCL · 회전/반사 · 주기 seam · 고정 기하 격자 조임 · origin · 투여 단조) 을 덮는가 — 특히 주기 seam 을 "정량 모드 거부 (생산 비주기)" 로 대신한 것 |
| A6 | S1-P | 원고 펠릿 9:1 을 피브릴 펠릿 RVE 위 **사전 점검** (손잡이 없는 연산자 · 맞추지 않음 · 불합격 = 판정 문장 한정어) 으로 쓰는 분류가 R18 의 *"0.97 에 다시 맞추면 calibration"* 경고와 양립하는가 · 불합격 결과의 처리 |
| A7 | S2 구조 | 멤버십 dof + instance 간선 + 등록 쌍 면 절단 + 실제 그래프 가지치기 (설계 §4-1) 가 J1 · J3 · J7 · J12 를 충족하나 · 비탄소 면 · 판 결합의 기하 최근접 멤버십 (집합 규칙) 으로 J9 가 충분한가 |
| A8 | S2 범위 | VA · SV · SA = 지금 규약 (융합) 을 선언해 그대로 두고 VA 소산 몫을 보고하는 v0 가 받아들일 만한가 (R_j 가 크면 VA 우회 편향) · 연속 중심선 없는 침대 거부 · 긴 접촉 · 미등록 면 법칙 처리 |
| A9 | S2 값 지위 | R_j = 모형 내부 순 접합값 (포트 = 셀 중심 · de-embedding 없음 · `rj_reference_plane = model_internal_port_centre`) 이 J4 와 양립하나 · R_j = 0 축약을 사다리 천장 · 시험 기준으로만 쓰는 것이 J6 을 만족하나 |
| A10 | 세대 · 영수증 | 켤 때만 쓰는 `ca_ext` 블록 + `physics_protocol_id` 의 `p3ca-` 접두 (블록 없으면 지금 함수 · 바이트 그대로) — "블록 부재 = 끔" 이 R3-CX-03 ("키 부재 = 모름") 의 예외인데, 그 길을 producer 게시 전 검사 · 러너 요청 해시 · 판정기 기대 세대 셋으로 막은 것이 충분한가 · 규칙 M 의 새 분류 `protocol_ext` |
| A11 | S3 | c ∈ {0, 1} 두 끝 · c = 1 = **같은 그래프의 정확한 축약** 을 "젖음 상한" 으로 정의 (옛 면 융합이 아니라) · 새 간선 없음 · 펠릿 SDCP 9:1 = 구성상 no-op (판별력 없음이라 적는다) · SDCP 부피 스탬프와의 이중 계상 논거 (두 끝에 같이 있다 → 차 = 막 증분) |
| A12 | P-junc | PTFE–접합 법칙 {P0 · P1} 을 v0 로 당겨 구간의 "PTFE 법칙 밴드" 로 쓰고 face_alpha 에서만 허용하는 것 · 덮임 기준 (최근접점 ↔ PTFE 중심선 ≤ r_P + r_f + tol_P) |
| A13 | 수렴 | σ 대비 1.9 × 10⁶ + 접합 간선에서 수렴 증서 셋 (CG info 0 · 판 전류 균형 ≤ 1e-6 · 사다리마다 rtol 1e-10 재풀이 |Δσ|/σ ≤ 1e-4) 이 충분한가 · 전처리를 값 봉인 숫자 탐침으로 정하는 것 |

### A-2. 등록 R 초안

| Q | 묻는 것 |
|---|---|
| A14 | **식별성** — "각 시나리오 모형 (P × c) 마다 손잡이 R_j,0 하나 · SBE 한 점" · σ_VGCF = Endo 고정 (다음 세대에서 묶음 σ* 는 손잡이가 아니다 · 통합 계획 §1 문장의 정정 읽기) · 이온 σ₀,eff = 다른 채널 · 다른 자료 · 판정 밖 · 금지 목록 (R §2) 으로 두 손잡이가 한 점으로 정해지는 꼴이 남지 않는가 |
| A15 | **holdout 오염** — 4.68 이 현 세대 보정에 쓰였다는 선언과 지키는 다섯 (R §1) 으로 충분한가 · 더 막아야 할 것은 |
| A16 | **구간** — 네 모서리의 최소 · 최대 (모서리마다 재보정 → 보정을 건너 Rayleigh 순서 불성립) 가 맞는가 · origin 규칙 (R §4-2) · 한 법칙 끝이 보정 불가면 판정 전체 `CALIB_IMPOSSIBLE` |
| A17 | **정보량 · 판정** — W 등급 (G0 = 0.908 기준 · 0.454 / 0.908) · 자리 p · 영 모형 대비 S · 판정표 · 감도 표지 (`*_SENSITIVE` 이면 PASS 문장 금지) 가 "구간이 넓어서 통과" 를 막는가 · R18 의 "허용창을 신뢰구간처럼 다룬 범주 오류" 를 되풀이하지 않는가 |
| A18 | **측정 꼴** — 점 4.68 로 판정 (넓히지 않음) · 알려진 성분만 정량 · 접촉 저항 부호 논거 (같은 R_c · s < R_S/R_D) · Q11 두께 계열의 런 전 / 후 처리 |
| A19 | **격자** — vox 0.20 불가 (SDCP 게이트) · 0.125 선택 단계 · *"격자 의존이 줄었다"* = 현 세대 같은 두 vox 대비 둘 다 작을 때만 |
| A20 | **금지 문장** (R §7-2) 에 빠진 것 |

### A-3. 판정을 바라는 형태

- 단계마다 GO / 조건부 GO / HOLD + 최소 해제 조건 · 새 결함은 P1/P2/P3 + 반례 (가능하면 실제 함수 · 합성 픽스처) · 숫자 합격선을 Codex 가 대신 정하지 않는 것은 지난 회차들과 같다 (⬜ = 1저자).

---

## Part B — 조인 수정 재확인 (뼈대 · ⬜ = 메인이 채운다)

### B-0. 대상

| 원장 | 지난 판정문 (`docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md`) | 수정 | 시험 (같은 시험 판 · 고치기 전 → 뒤) |
|---|---|---|---|
| `RIMPR-R01` (Codex `RIMPRR-01`) P3 | §3 — 구역 분류 `startswith()` + 표지 전역 `replace()` → 헤더 정상화 false-PASS 10 건 | 구역 이름 = 정확한 단어 경계 · 표지 하나만 앞에서 제거 | `scripts/test_rint_g2_join.py` 152/206 → 206/206 (실패 54 = 새 반례 전부 · `docs/reviews/rimprr_fix_plan_20261020.md` §3 결과) |
| `RIMPR-03` P3 | §4 — 정수 정규식 `\d` 가 전각 · 아라비아-인도 숫자를 받음 | ASCII 숫자만 (`int_token`) | 같은 파일 |
| `RIMPR-04` P3 (부분) | §4 — 입력 유한 ≠ 계산 결과 유한 (1e160 → `inf > inf` 거짓 → PASS) | 파생값 유한성 fail-closed (`derived_nonfinite` · G-frame f6 · G-geo `delta_bound_um` · AM–AM 면적) · **원장 open 유지** (연기 조건 ①) | 같은 파일 |
| `SELF-124` P3 | §7 · §1 — 요청서의 범위 한정 없는 *"봉인 32 무변경"* · 다른 두 시험 판 숫자 | 요청서 정정 표지 (판정문 §7 권장 문장 · 81/138 구분) | — |

- 커밋 (Part B 가 보는 것): 시험 먼저 `12d894c09` · 수정 `a2cfd0365` · 기록 (원장 · 계획 · CLAUDE.md · 진행) `654385e4c`.
- diff = `git diff 12d894c09~1 a2cfd0365 -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py`.
- 그 밖 회귀 (계획 §3 결과 · 이 컨테이너 Linux): `scripts/test_rint_g2_am_iface.py` 136/136 · `scripts/test_rint_g2_rrm.py` 55/55 · `scripts/test_rint_t4_census.py` 8/8 · `scripts/test_rint_t43_order.py` 6/6 · `scripts/test_rint_t2_dev.py` 23/23 · `scripts/step3_sigma.py --selftest` · `--selftest-rint` PASS · `scripts/rint_t41_census.py --selftest` PASS — ⬜ 메인이 리뷰 핀에서 다시 돌려 숫자를 확인한다.

### B-1. 탐침 재실행 요청 (지난 회차 증거 · 무변경 · 계획 §3-4 의 기대)

| 탐침 | 고친 뒤 기대 |
|---|---|
| `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_probe.py` | 헤더 반례 10 = 거부 · 그 밖 판정 그대로 |
| `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_minimal_replay.py` | 최소 반례 둘 (`ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS`) = 거부 |
| `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_review.py` | 전각 정수 = 거부 (`int_token`) · 그 밖 판정 그대로 |
| `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_overflow_replay.py` | 1e160 반례 = 거부 (`derived_nonfinite`) · 1e150 대조 = 그대로 REJECT |

- 정상 입력 유지 (계획 §3 결과): real14 PASS · 457/457/457 · AM–AM 660 · case15 PASS · 104/104/104 · 119 · 입자 · id 사상 · `dem_am_am` 배열 바이트 · `delta_bound_um` 같음 · 바뀐 것 = 기록의 새 칸 · 판 · 규칙 문구 (`fp_join` 이 바뀐다 · 고정 대조하는 곳 없음) — ⬜ 메인 확인.

### B-2. 사전 리뷰 결과 (CLAUDE.md ①–③) — ⬜ 메인이 채운다

| 단계 | 결과 |
|---|---|
| ① 요청서 · 커밋 메시지 · 원장 · 계획의 숫자 · 전칭 ↔ git · 시험 출력 | ⬜ |
| ② 바뀐 함수에 HOLD 부류 직접 실행 (NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 유니코드 숫자 · 공백 · 탭 · CRLF · gzip · 다른 판본) | ⬜ |
| ③ 독립 에이전트 (diff 만) 반례 · 변이 시험 | ⬜ |

### B-3. 질문

| Q | 묻는 것 |
|---|---|
| B1 | `RIMPR-R01` 이 판정문 §3 최소 해결 (정확한 단어 경계 · 표지 한 번 제거 · 나머지 토큰은 기존 열 · 상자 검사로) 로 닫히는가 · 정상 공백 · 탭 · 쓰지 않는 진단 열을 새로 거짓 거부하지 않는가 |
| B2 | `RIMPR-03` (ASCII 정수만) 이 닫히는가 · 생산 ASCII `%g` 덤프 무영향 |
| B3 | `RIMPR-04` 의 파생값 유한성 fail-closed 가 판정문 §4 의 연기 조건 ③ (조인을 소비자 관문처럼 믿지 않음) 을 코드로 받치는가 · open 유지 (조건 ①) · 남은 것 (안정한 거리 · 오차폭 계산 = 정량 채택 전) 이 맞게 적혔는가 |
| B4 | `SELF-124` 정정 문구가 판정문 §7 권장 문장 · §1 구분과 같은가 |
| B5 | 새 결함 (P1/P2/P3) |

### B-4. 리뷰 핀 · 한정

- 리뷰 핀 = ⬜ (메인이 채운다 — Part A 문서 셋과 같은 커밋이거나 그 뒤).
- 기준 = 지난 회차 리뷰 핀 `2b9efa253` (대조 핀 `dcb97f1ed`).
- 한정: 이 컨테이너 · 정상 침대 둘 (real14 · case15) 결과 · 시험 먼저 → 수정 두 커밋은 본 가지에 그대로 (합치지 않음) · ①′ 정량 채택 · 생산 HOLD 그대로.
