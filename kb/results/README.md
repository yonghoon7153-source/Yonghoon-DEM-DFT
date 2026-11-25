---
title: "kb/results 지도 — 계별로 지금 유효한 것 / 마감 근거 / 접힌 역사"
date: 2026-09-09
updated: 2026-09-09
tags: [index, results, map, closure, retraction]
status: 운영중
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: interpretive
evidenceScope: multi-source-primary
---

# kb/results 지도 — 계별 세 줄

> **왜 이 파일인가**: 이 폴더는 결과 해석 카드 90여 장이 **평면 알파벳**으로 쌓여 있고,
> 화면(`/log`)은 그걸 파일명 역순으로 깔기만 한다. 날짜도 지위도 안 보여서
> *"지금 b2o3 에 대해 말할 수 있는 게 뭐냐"* 를 알려면 카드를 다 열어야 하고,
> 열어 보면 **여러 장이 철회된 값을 '최종' 이라고 말한다.** 계마다 세 줄만 적는다.
>
> ⛔ **이 파일은 값을 갖지 않는다.** 숫자의 정본은 언제나 `db/properties/` 이고,
> 인용 가능 여부는 `canonical_registry.json` + `citation_hazards.json` 이 정한다.
> ⛔ **이 지도가 못 하는 것**: 카드 90여 장을 전수 검증하지 않았다 —
> 2026-09-09 감사에서 **배너를 실제로 단 11장**과 마감 원장에 등록된 축만 확실하다.
> 여기 안 적힌 카드는 "괜찮다" 가 아니라 **"아직 안 봤다"** 이다.

## b2o3 (B₂O₃-도핑 LPSCl1.6)

| | |
|---|---|
| **지금 유효** | 마감 카드가 **열거한 셋뿐** — **gap 1.9671 eV** · **탄성 +13 %**(modelc 대비) · **ELF/ICOHP**(B–S 최강 · P–O 신규 motif). ⚠ 방향이 MD 와 반대(강화·보존)이고 **그 모순은 미해결**이다 |
| **범위 밖이지만 열거되지 않음** | convex hull(+37.5 meV/atom) · phonon 안정성 — **둘 다 UMA(MLIP) 산출물이지 DFT 가 아니다** · BVSE 채널(+45 %)은 정적 결합원자가 기하. 인용하려면 각자의 근거로 따로 서야 한다 |
| **마감 근거** | `db/properties/b2o3_md_closed_retrospective_2026_08_25.json` (`D-2026-09-07-b2o3-md-closure-retrospective`, active) · 인용위험 `HZ-b2o3-md-ea` **BLOCKED** · 재개용 전향 카드 `b2o3_cell_expansion_prereg_2026_09_07.json` |
| **접힌 역사** | MD 6장 — `b2o3_champion_status_2026_07_03` · `b2o3_SEMIFINAL_report_2026_07_09` · `b2o3_md_600K_multiseed_2026_07_02` · `b2o3_vs_lpscl16_md_2026_07_02` · `b2o3_bvse_channel_2026_07_02` · `b2o3_anode_interface_MD_dynamics_2026_07_06` (2026-09-09 에 전부 마감 배너를 달았다) |

⛔ **UMA-MD 전도도 축 전체(D·Ea·σ·구간 Ea)에서 인용 가능한 수는 0개다.** `0.199`·`0.206`·
`0.21±0.03`·`0.2234`·구간 `0.222` 전부. σ 비 1.08/0.82/1.15 로 **"동등"·"σ 보존"** 이라고
쓰지 않는다(레지스트리 `md-sigma-ratio-v1__NON_CITABLE`) — 그 셋은 **600/800/1000 K** 값이다.
가장 잘 관리된 카드는 `b2o3_arrhenius_curvature_2026_08_23.md`(인공물 가설 3개를 각각 반증 +
자기정정 + "이 카드가 못 하는 것" 절) — **나머지를 이 형식에 맞추는 것이 목표**다.

## comp1 (LPSCl) ↔ modelc (LPSCl1.6)

| | |
|---|---|
| **지금 유효** | 0 K DFT 축 — gap **2.066 / 2.099 eV**(fixed-occ nscf) · `B0_GPa` · `E_VRH_GPa` · `ICOHP_PS` (넷 다 레지스트리 `canonical`). 그리고 DFT 가 아닌 정적 축: **BVSE 기하** · 구조 관측(anti-site Cl · Li 공공 · Voronoi) |
| **금지** | **σ 절대값**(3.35 / 13.96 mS/cm) · **"σ 4배"** · 조성 간 Ea 대조(`HZ-cross-system-Ea` **BLOCKED**) · "실험과 일치" 서술. `MD_Ea_eV_singleseed@comp1` 은 단일시드 `provisional` + `cross_composition_ranking` 금지 |
| **접힌 역사** | σ 5장 — `MASTER_structure_property_logic_2026_06_21` · `ionic_conductivity_full_explained_2026_06_21` · `ionic_conductivity_synthesis_comp1_modelc` · `deck_ionic_section_additions` · `lpscl_vs_lpscl16_v3_comparison` (2026-09-09 배너) |

⚠ 이 카드들이 쓰는 **"AIMD" 는 실제로 MLIP-MD(UMA-s-1p1, omat)** 다 — 방법 라벨을 그대로 옮기면 오기다.

## LPSOCl (O 치환)

| | |
|---|---|
| **지금 유효** | 0 K DFT 축 — gap **2.2309**(canonical) · `E_VRH_GPa` 35.04(canonical) · `ICOHP_PS` −6.04(canonical). P–O −8.413 은 `kb/methodology/computational_methods_canonical.md` §5 기록이고 **레지스트리 항목은 아니다**. COHP 곡선 원자료는 ⚠ **곡선 면적 ≠ ICOHP**(창 커버리지 표기 필수) |
| **진행/조건** | 3×3×1 400 ps 9런 — **닫힘 조건이 결과 보기 전에 확정됨**(`D-2026-09-08-lpsocl-box331-closure-conditions`, active · `lpsocl_box331_closure_conditions_2026_09_07.json`). 62원자 Ea 0.2867 은 **셀 조건부**이고 3×3×1 은 **다른 보고량**이다 |
| **접힌 역사** | `lpsocl_box_size_600K_2026_08_18`(셀로 D 1.65×) · `mlip_md_diffusive_gate_2026_08_01`(⚠ β 0.8 문턱은 폐기 — 결론은 유효) |

## SDCP (분자·표면 계열)

| | |
|---|---|
| **지금 유효** | `sdcp_wave1_citable_2026_08_25.md` — **논문에 쓰는 값 한 장**(원자료에서 재유도, 손 전사 0). 다른 sdcp 카드는 여기를 가리킨다 |
| **마감 근거** | `db/properties/sdcp_neutral_closed_2026_08_28.json` · `sdcp_doped_closed_2026_08_28.json` (둘 다 active·ratified) |
| **금지** | doped E_ads **수치 일체** · *"doped 가 중성보다 강하게/약하게 붙는다"*(비교 자체가 미정의) · 철회된 `dE_extract +0.336` |

## Nd / SEI / 접착(W_ad) / cascade

- **Nd·SEI**: gap 3종 자체 측정(frozen-4f) **3.948 / 3.698 / 0.770 eV** 가 정본, MP 인용 우회는 폐기.
  ⚠ **UMA 는 Li₃N 에 사용 금지**(CLAUDE.md) — `db/interphases/li3n.json` 의 UMA 경로 값은 철회 계열이다.
- **접착 W_ad**: ⛔ **`canonical_registry.json` 에도 `citation_hazards.json` 에도 등록돼 있지 않다.**
  논문에 쓴 표는 20 시드 중 **5 시드를 고른 판**(R=0.9999)이고, 100 시드 통계
  (`adhesion_100seeds_analysis.md`)는 Li5.4 내부 순위를 유의하지 않다고 한다.
  **어느 세대를 정본으로 삼을지는 1저자 결정** — 그 전까지 순위 주장 금지.
- **cascade**: 회신 AL(2026-08-30) **NO-GO hold**. 보고량은 2026-09-08 재정의
  (`cascade_d_rel_estimand_2026_09_08.json`, active) · 봉인 `cascade_seal_v2_2026_09_08.json`.
  **v1 의 front·순위는 인용 금지**(무효 사유와 함께 보존만).

## 이 폴더에 대한 규율

1. **`정본:` 포인터는 kb/results 안을 가리키지 않는다** — 카드끼리 가리키면 사슬이 같이 늙는다
   (SEMIFINAL 이 그 사례다). `db/properties/` 또는 `kb/methodology/` 를 가리킨다.
2. **철회는 원문 보존 + 반증 병기** (kb/SCHEMA.md Update Policy). 배너만 얹고 값은 지우지 않는다.
3. **음성 결과 카드는 지우지 않는다** — `single_li_neb_invalid_argyrodite_2026_08_21` ·
   `sdcp_slab_plateau_broken_2026_08_03` · `md_beta_estimator_disagreement_2026_08_25` ·
   `champion_pool_size_bias_2026_08_18` · `halogen_wad_refutation`. 다시 유도하는 데 제일 비싸다.
