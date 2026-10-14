# 밀도 세대 (density generations) — 2026-10-14 밤

> 정본 표 = `scripts/additives.py` 의 `DENS_GENERATIONS` · `DENS_CARRIED_FROM_GEN1`.  이 문서는 결정 · 도구 · 연기 항목의 기록이다.

## 1. 결정 (1저자 10-14 밤)

| 항목 | 내용 |
|---|---|
| 랩 표준 진밀도 | SE (LPSCl) **1.64** · NCM (PC · SC 같음) **4.85** g/cm³ |
| 범위 | **(가) 앞으로만** — 새 런 · 새 분석은 랩 표준 · 이미 만든 결과는 만든 때의 밀도 (gen1 = AM 4.80 · SE 2.00) 그대로 (바이트 그대로 · 재실행 없음) |
| 규칙 | 전역 상수를 조용히 바꾸지 않는다 · 도구마다 쓴 세대를 **명시** (`--dens-gen` · `dens_gen=`) 하고 매니페스트 · 산출물에 기록 · 시험 먼저 · 웹앱 같은 묶음 (봉인 파일은 §6 으로 연기) |
| ⚠ 1.64 의 지위 | "랩 표준값" 이다.  물리적 골격 (진) 밀도인지는 1저자와 논의 중 (결정학 Li6PS5Cl ≈ 1.86 이 거론됨 — 출처 카드 확인 전 · 인용 아님).  실측 세대 (예: He 피크노미터) 를 표 한 항목으로 더할 수 있게 만들었다 (§7) |

## 2. 세대 표 (g/cm³)

| 세대 | AM (NCM) | SE (LPSCl) | VGCF | SuperP | PTFE | SDCP | SWCNT | 지위 |
|---|---|---|---|---|---|---|---|---|
| `gen1` | 4.80 | 2.00 | 2.00 | 1.90 | 2.20 | 1.30 | 1.35 | 옛 결과 전부 · `DENS` **그 객체** (기본값) |
| `lab20261014` | **4.85** | **1.64** | 2.00\* | 1.90\* | 2.20\* | 1.30\* | 1.35\* | 1저자 랩 표준 (SE · NCM 두 값) |

\* = no lab value — gen1 value carried (`DENS_CARRIED_FROM_GEN1['lab20261014']`).  기록 (§4) 에도 옮긴 상 목록이 같이 남는다.

## 3. 효과 크기 (산술 · 세대 미지정 = 왼쪽 값 그대로)

| 양 | gen1 | lab20261014 | 근거 |
|---|---|---|---|
| AM:SE = 80:18 wt% 의 SE 부피 몫 (P:S 무관 — NCM 한 밀도) | 35.06 % | 39.95 % (+4.89 %p) | `additives.py --selftest-dens` D⑦ · 믹서 DG③ |
| 믹서 100 k 원자 · CGF 151.4 · 3 상 — 원자 수 AM_P · AM_S · SE | 176 · 859 · 98,965 | 143 · 699 · 99,158 | `plan()` (같은 원자 예산에서 AM_P −19 %) |
| 믹서 드럼 R · Rayleigh dt (AM_S 가 정함) | 13.138 mm · 7.055e-7 s | 12.583 mm · 7.092e-7 s (×√(4.85/4.80)) | 믹서 DG④ |
| 믹서 LC 팔 SE–SE CED (같은 Bo_code 0.21244) | 10,458 J/m³ | 9,789 J/m³ | Bo = F_coh/W · W ∝ ρ |
| Phase A 옛 캠페인 침대 VGCF 1 wt% 개수 · AM wt% | 26,813 · 81.03 % | 26,208 · 83.76 % | `phase_a_precompute.py` ⑦ (개수 비 = 고체 질량 비) |
| 킷 VGCF 2 wt% dilate-z λ (합성 · AM≈SE 부피 / AM 많음) | 1.0473 / 1.0588 | 1.0457 / 1.0589 | `mpm_input_from_case.py --selftest-dens` K4 |
| mpm3d 스캐폴드 침대 밀도 (부피 1:1 · 침대 2) | 3.400 | 3.245 g/cm³ | `mpm3d_compaction.py --selftest` DG2 |

## 4. 도구별

| 도구 | 옵션 | 밀도가 들어가는 곳 | 미지정 | 지정 시 기록 |
|---|---|---|---|---|
| `scripts/additives.py` | API `dens(세대)` · `dens_record(세대)` · `vol_fracs` · `recipe_counts` · `recipe_counts_real` 의 `dens_gen=` · 데모 CLI `--dens-gen` | 부피분율 · 첨가제 질량 → 부피 · 개수 | gen1 `DENS` 그대로 · 기록 키 없음 | 결과 dict 끝에 `dens_gen` · `dens_g_cm3` · `dens_carried_from_gen1` |
| `scripts/mpm3d_compaction.py` | `--dens-gen` | 스캐폴드 `bulk_density_g_cm3` · `--add-recipe` 첨가제 개수 · 부피 (add_pvs → 공극률) | 옛 인라인 식과 비트 동일 | metrics + `--save-state` meta.  `--am-scaffold` 없으면 거부 (밀도 안 쓰임) · `--load-state` 는 state 세대와 같아야 함 (옛 state = gen1) |
| `scripts/mpm_input_from_case.py` | `--dens-gen` | VGCF dilate-z 의 φ_VGCF · 킷의 mpm3d 호출 | 킷 바이트 그대로 | `mpm_input.json` + `run_mpm.sh` 압밀 호출 · `run_a1_anchors.sh` COMMON 에 `--dens-gen` (payload 호출에는 안 굽는다) |
| `scripts/mpm_webapp_payload.py` | 없음 (밀도로 계산하지 않음 — 규칙 M 회계 그대로) | — | 그대로 | mpm3d metrics 의 세대 기록을 `SIM_CARRY_KEYS` 로 그대로 싣는다 |
| `scripts/phase_a_precompute.py` | `--dens-gen` | ② 첨가제 개수 | 옛 출력 그대로 | 화면 · JSON (`dens_*` + `campaign_validation_dens_gen`).  ③ 옛 캠페인 대조는 **gen1 고정** (`CAMPAIGN_DENS_GEN`) |
| `scripts/make_mixer_deck.py` | `--dens-gen` (선택지 = 로컬 사본 표) · `plan(…, dens_gen=)` | 부피분율 → 템플릿 수 · 드럼 · Rayleigh dt · Bo ↔ CED · `density constant` | 덱 · 메타 바이트 그대로 (골든 ㉟ · DP① · ST①) | 덱 머리 주석 두 줄 + `deck_meta.json` (기본 덱도 세대를 주면 메타를 쓴다).  **D2 (`--gm-*`) 덱은 `--dens-gen` 필수** (CLI · `deck` · `deck_meta` 모두 거부) |
| `scripts/step3_sigma.py` · `scripts/comsol_export.py` | 없음 | 확인 결과 밀도가 계산에 안 들어간다 | — | — (선언 ≠ 사용을 피해 옵션을 만들지 않음) |

믹서 생성기는 리포 밖 단독 실행을 위해 표의 **사본**을 둔다 — 셀프테스트 DG① 가 `scripts/additives.py` 를 AST 로 읽어 네 상 (AM · SE · VGCF · PTFE) 값과 옮긴 상 목록을 대조한다.

## 5. 바이트 동일 (세대 미지정)

- 셀프테스트: 믹서 골든 해시 (㉟ · DP① · ST①) 그대로 통과 · additives D⑧ (옛 식 독립 산술) · mpm3d DG1 (무작위 200 · 옛 인라인 식) · 킷 K1 · K2 · phase_a ⑥ · payload ⑦.
- 기준 커밋 `2751918db` 의 도구와 같은 입력으로 돌려 비교 (작업 트리 밖 임시 폴더 · 10-14 밤): additives 함수 1,500 호출 (repr · 키 순서까지) · 데모 CLI 3 · 믹서 덱 94 (옛 팔 전부 × 설정 5) + CLI 6 회 출력 파일 전부 · phase_a 화면 + JSON 2 경로 · 킷 28 (케이스 4 × 옵션 7, 파일 전부 · 화면) · payload 1 (픽스처 + sim metrics) = **전부 같음**.  다른 것은 코드 신원 필드뿐이다 — `deck_meta.json` 의 `generator_sha256` · payload 매니페스트의 `code_sha` · `project_module_digest` (바뀐 파일의 해시라 정의상 다르다).  payload 의 실행 환경 스캔 (`untracked_codelike` · `risk`) 도 달랐는데 옛 트리를 git 밖 폴더에 풀어서 생긴 하네스 차이다 (코드 차이 아님).
- 일부러 바뀐 동작 하나: `--gm-*` 를 `--dens-gen` 없이 주면 거부한다 (D2 덱 = 새 세대 덱).  D2 덱은 아직 등록 전 개발 덱이다.

## 6. 연기 — 봉인 파일 · 웹앱 (LHS 재봉인 묶음)

`scripts/run_network_194_parallel.py` 의 `CODE_FILES` 32 파일은 건드리지 않았다.  재봉인 묶음에서 할 것:

| 파일 | 자리 | 바꿀 것 | 시험 |
|---|---|---|---|
| `scripts/grade_engine.py` | L46 `RHO_AM_G_CC = 4.8` · L1040 `__Q_volumetric_mAhcc` (`rho_am, rho_se = RHO_AM_G_CC, 2.0`) · L1265 · L1281 `__Q_areal_mAhcm2` · L522 축 설명 문자열 · L1012–1013 주석 | 케이스 metrics 의 `dens_gen` (없으면 gen1) 으로 AM · SE 밀도를 고른다.  `grade_engine` 은 numpy 를 import 하지 않으므로 믹서와 같은 방식 (두 상 사본 + `additives.py` AST 대조 셀프테스트) 을 권한다.  축 출력에 쓴 세대를 같이 싣는다 | 기본 = 옛 값 비트 동일 (코퍼스 몇 케이스) · lab = Q_vol · Q_areal 이 조화평균 식대로 바뀜 · 모르는 세대 거부 · 사본 = 정본 |
| `scripts/grade_engine.py` | L1711–1714 `whatif_carbon_additive` (`rho_avg 3.5` · `rho_carbon 2.0`) · L1746–1748 `_ADD_RHO` · `_RHO_SOLID 3.5` | 세대와 묶을지 1저자 결정 (지금은 세대 밖 어림값) — 묶으면 `_ADD_RHO` 는 세대 표의 첨가제 값 | 같은 방식 |
| `webapp/app.py` | `mpm_input_package` (`/results/<case_id>/mpm-input`, `--add-recipe` 를 붙이는 곳) | `&densgen=` 쿼리 → 생성기 `--dens-gen` (화이트리스트 = 표의 키 · 빈 값 = 안 붙임 = 킷 바이트 그대로) · 다운로드 이름에 세대 꼬리 | `webapp/test_temp_pressure_wiring.py` 와 같은 틀 — 미지정 = CLI 직접 실행과 멤버 바이트 동일 · 지정 = `mpm_input.json` 기록 · 모르는 값 400 |
| `webapp/templates/single.html` · `webapp/static/js/viewer3d.js` (봉인 밖이지만 같은 묶음으로 미룸) | single.html L484 `bulk_density_g_cm3` 칸 · viewer3d.js L8040–8041 (`SE/solid · ρ_bulk`) · L8241 `row('scalar', 'bulk_density_g_cm3', …)` | `mpm_metrics.dens_gen` 이 있으면 밀도 옆에 세대 표지 (`lab20261014` · 옮긴 상 툴팁) · 없으면 "gen1 (기록 없음 = 옛 산출물)" | 표지 문자열 시험 (기록 있음 · 없음) |

## 7. 세 번째 세대 더하기 (예: He 피크노미터 실측)

1. `scripts/additives.py` 의 `DENS_GENERATIONS` 에 한 항목 (모든 상 · 실측 없는 상은 gen1 값) + `DENS_CARRIED_FROM_GEN1` 에 그 세대의 옮긴 상.
2. `scripts/make_mixer_deck.py` 의 사본 두 표에 같은 항목 (네 상) — 안 하면 셀프테스트 DG① 가 실패한다.
3. 다른 도구는 손댈 것 없다 (`--dens-gen` 선택지 · 검증은 표에서 읽는다).  세대 이름은 측정 날짜를 담는다 (예: `pyc20261101`).

## 8. 이 묶음 밖 (후속 후보)

| 자리 | 상태 |
|---|---|
| `scripts/mixer_deck_readback.py` (`REG_DENSITY` 4800 · 2000) · `scripts/mixer_deck_diff.py` (`expected_deck` 이 gen1 계획) | lab 덱을 **거부** (fail-closed — 템플릿 밀도가 등록값과 다르다).  D2 덱을 발사 관문에 올릴 때 세대를 읽게 고친다 |
| DEM 덱 · 2D MPM 의 하드코딩 4800 · 2000 (`scripts/lhs_ext_materialize.py` · `scripts/make_ps_sweep_decks.py` · `scripts/diag_se_percolation_threshold.py` · `scripts/mpm2d_composition.py` · `scripts/mpm2d_jamming.py`) | 세대 2 DEM 프로토콜 (`docs/reviews/dem_protocol_gen2_plan_draft_20261014.md`) 에서 다룬다 |
| `scripts/validate_additive_seeding.py` · `scripts/preview_sdcp_mixing.py` · `scripts/sr01_realbed_ab.py` | `recipe_counts_real` 기본 (gen1) 을 부르는 그림 · 역사 도구 — 옵션 없음 |
