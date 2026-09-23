---
title: "내부 리뷰 (Fable) — LPSCl | Ag–C | VGCF 점착일 계획: NO-GO (현재 판)"
date: 2026-09-23
updated: 2026-09-23
tags: [review, internal, fable, adhesion, wad, interface, lpscl, silver, graphite, uma, dft-verification]
status: 수신됨 — NO-GO(현재 판) · P0 4건 원문 대조 확인 끝 · 계획 v2 에 반영
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-23
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 내부 리뷰 (Fable) — LPSCl | Ag–C | VGCF 점착일 계획

- **대상**: `kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md` (초판, 커밋 `b27dd3b8e` 시점) + 재사용하려던 워크플로 원문
- **검토자**: 내부 적대 리뷰 에이전트 (Fable 모델) · 읽기 전용 · 2026-09-23
- **쌍둥이**: Codex 리뷰 BV (`codex_BV_prompt_wad_lpscl_ag_c_vgcf_2026_09_23.md`) — 이 리뷰를 본 뒤 개정해서 보낸다
- 아래 **§원문** 은 에이전트 출력을 그대로 옮겼다. 고치지 않는다. 우리 쪽 확인은 **§부록** 에 붙인다.

---

## 원문

**판정: NO-GO (현재 판) — 아래 P0 4건을 반영해 카드를 다시 쓰면 GO-with-fixes 로 재심.** 계획의 방향(같은 조작·W_sep 명명·α 보정 배제·기준값도 DFT 검증)은 맞다. 문제는 "기준값" 자체다 — 기준 계면의 셀이 기하적으로 맞지 않고, 기준값을 낸 프로토콜을 잘못 읽었고, 검증 짝(UMA ↔ PBE+D3)이 어긋난다. 이 셋을 안 고치면 "나란히 비교" 가 성립하지 않는다.

---

## 발견 (심각도순)

**1. [P0] 기준 계면 셀이 기하적으로 안 맞는다 — SE 는 정방 20.11 Å, 계면 셀은 육방 20.146 Å**
- 근거: SE 슬랩 = 52원자 관용 입방셀 2×2×3 (`adhesion_v6_anneal_test.py:40` `'repeat': [2,2,3]`, `kb/results/adhesion_final.md:15` 624원자·30 Å). `db/structures/comp1_V0_k444.cif` a = 10.055 Å → 측면 **2a = 20.11 Å, 90°, A = 404 Å²**. "prim" 표기는 오기다 — 13원자 원시셀 2×2×3 이면 156원자다. 계면 셀은 `build_ncm_1L` 의 `Lattice.hexagonal(2.878, …)` 7×7 (`run_cathode_interface.py:54-58`) → **20.146 Å, 120°, A = 351.5 Å²** — `adhesion.json` `Li6_v5_xyshift_FIX.A_Å2 = 351` 과 일치. 기록된 `strain_pct 0.2` = |20.146 − 20.11| / 20.11 = 0.18 % — **길이만 잰 값이고 각도(90° → 120°)는 어디에도 없다.** `adhesion.json` `xy_shift.trends.cross_family` 의 "SE density 1.78 at/Å²" = 624 / 351.5 — 진짜 (001) 슬랩 밀도 1.54 (= 624/404) 보다 **13 % 과밀**. 빌더 `build_interface` (`adhesion_v6_anneal_test.py:89-98`) 는 docstring 이 "Strain SE to NCM cell" 인데 수식은 `se_cart @ inv(ncm) % 1 @ ncm` — **변형이 아니라 wrap** 이다 (원자 데카르트 좌표 그대로, 주기성만 NCM 것으로 교체). 정방 격자 조각을 육방으로 타일링하면 셀 경계에 비정합 이음매 + 겹침이 생긴다. 팀 스스로 적어 뒀다: `adhesion.json` `phase1…anomalies.comp1_comp2_d_min_close` "possible cubic SE + hex NCM PBC artifact". v30u 쪽도 같다 — `run_li_migration_FINAL_combo.py:188-191` 은 육방 NCM 을 SE 셀에 `scale_atoms=False` 로 넣고, `generate_stacked_deq_orthogonal.py:84-87` 의 "already orthogonal → return" 분기가 comp1/2 셀이 직교였음을 시사한다. Li5.4 계열(R3m 육방축 |a₁| 14.12–14.18 vs 14.23, `mechanism_anion_O_descriptor.md:562-566`)은 육방-육방이라 이 문제가 없다 — **cubic comp1 이 제일 나쁜 기준값**이다.
- 왜 중요한가: (i) 기준값 20 seeds 의 큰 산포(0.555–1.85, comp2B 6.428, 5L 에서 40 % 이상치)가 이음매 아티팩트와 부합한다. (ii) 계획 L34/L62 의 "측면 육방 20.13 Å" 은 NCM 셀을 SE 셀로 착각한 것 — **Ag(111) 7×7 육방 설계와 변형률 표(−0.46/−0.80/−2.23 %) 전부가 잘못된 셀 위에 서 있다.**
- 고치기: ① 기준 계면 하나를 v6 빌더로 재생성해 셀 각도·최소 원자간 거리·경계 원자 배위·PS₄ 무결성을 본다(수 분). ② 모든 계면을 **SE 고유 정방셀 20.11 Å** 에 짓는다: NCM(001) 1L 직사각 7×4 (2.878 × 4.985 → 20.146 × 19.94, +0.18 / −0.85 %, 224원자) · **Ag(111) 직사각 7×4** (2.889 × 5.004 → 20.22 × 20.02, −0.55 / +0.45 %, 56원자/층 × 4 = 224). 둘 다 848원자로 대칭적이다. ③ 대안으로 육방 호환 (111) SE 슬랩(a/√2 = 7.11 Å, 2×2 ≈ 14.2 Å)이 있지만 종단이 바뀌어 "재사용" 이 아니다 — 비용 레버로만 적어 둔다.

**2. [P0] 기준값을 낸 프로토콜을 잘못 읽었다 — 기준값은 MQA 없는 relax-only, uma-s-1p1 이다**
- 근거: `kb/results/adhesion_final.md:6-9` "LBFGS relax only (no MQA — prevents Li interdiffusion)" · "Calculator: UMA (uma-s-1p1 …)" · "20 seeds per comp ran". `adhesion_energy.md:176` "4. Relax only (MQA 없음)". `adhesion_v6_anneal_test.py:185-189` "v5 reference (no anneal)". 800 K·500 K MQA 는 **시도했고 실패했다** — `adhesion_methods_comparison.md:84-86` "800K MQA … Li interdiffusion destroyed interface (58/248 atoms migrated). 500K MQA also showed Li crossing". 계획은 L45-46·L77·L106 에서 v5 = 800 K MQA 로 놓고 그걸 돌리려 한다. 계획 L52 "adhesion.json 에 UMA 판이 한 번도 없다" 는 사실이지만(실측 0건) `adhesion_final.md:8` 에 있고 repo 핀(`webapp/fairchem.py:64-70`)과 같다.
- 고치기: "v5 재사용" = **relax-only 레시피 + uma-s-1p1/omat + fmax·최대스텝 고정**으로 카드에 적는다. 800 K 단계는 뺀다(넣으려면 별도 이름의 2차 프로토콜). 렌즈 5 의 "800 K 에서 Ag–S 결합" 우려는 이걸로 대부분 소멸한다 — 남는 질문은 "LBFGS 이완만으로 Ag–S 접촉·Li/Ag 교환이 생기나" 다(10번).

**3. [P0] 기준값을 숫자로 재사용하지 말고 같은 파이프라인에서 다시 뽑는다 — 그리고 "기존 NCM 값" 이 하나가 아니다**
- 근거: 스크립트 유실(`adhesion.json` `v9_to_v22.context` "서버 lost"), 슬랩 파일도 repo 에 없다(계획 L75 — 재생성 슬랩은 원본과 다른 파일이다), 1번의 셀 문제, 그리고 repo 규율 `webapp/fairchem.py:82-84` "버전을 올리면 옛 값과 새 값을 자동 병합하지 말고 전부 다시 뽑는다". 비용은 작다 — `Li6_mqa_status` 가 820원자 MQA 6000스텝 + 이완에 8 min/seed 였으니 relax-only 20 seeds 는 3 시간 안이다. comp1 의 "기존 값" 후보: **1.153 ± 0.39 (20 seeds, `adhesion_charts_comparison.md` 가 "Honest" 라 부른 것)** · **1.151 ± 0.245 (100 seeds, `adhesion_100seeds_analysis.md:10`)** · **1.277 (20 중 5 seeds 42,49,52,58,60 을 "to match experimental ratios" 로 고른 것, R = 0.9999, `adhesion_final.md:9,33-35`)** · 1.107 (v2 melt) · 논문 #1 출판 관례 = WELLS_RAW − α·dW = 2.708 − 2.633 ≈ **0.08** (`tools/adhesion_v30u/README.md:7-13`) · v6 stage11 **45–80** (`adhesion_calibration_decision…:30-34`) · 5L NCM 2.67 ± 0.88. 같은 계면에 0.08 ~ 80 J/m² 가 공존한다.
- 고치기: DEM 팀에 이 대응표(이름 → 조작 → comp1 값)를 보여 주고 무엇을 "isolated slab W_ad" 라 부른 건지 **그들이 고르게** 한다. **1.277 은 어떤 경우에도 기준값이 아니다**(선별). 기준값 = 통합 파이프라인 재계산 20 seeds(시드 42–61 사전 고정) + 100-seed 세트와 중앙값·IQR 로 1회 대조.

**4. [P0] 검증 짝이 틀렸다 — UMA(omat) 는 분산 없는 PBE(+U) 기준계다. 비교 대상은 W^PBE(noD3) 여야 한다**
- 근거: `webapp/fairchem.py:76-78` "omat 기준계는 PBE/PBE+U(VASP 5.4)", `db/external/omat24/README.md:68`. 계획 §2 L97 은 W^UMA 를 W^{PBE+D3(BJ)} 와 비교한다 → D3 몫(0.1–0.3 J/m²)이 통째로 "MLIP 오차" 로 읽힌다. 물리흡착 짝(Ag|흑연, 흑연 층간)은 PBE ≈ UMA 가 거의 안 붙어 **UMA 이완 기하가 정의되지 않는다** — "UMA 이완 → DFT 단일점" 설계가 P1-b·P2 에서 무너진다.
- 고치기: 검증 짝 = **W^UMA ↔ W^{PBE,noD3}** (같은 기하). 헤드라인 W^{PBE+D3} = W^{noD3} + ΔD3 — D3 는 SCF 후 가산항이라 고정 기하에서 **정확히** 분해된다(QE `vdw_corr='grimme-d3', dftd3_version=4`, `tools/vgcf_hbn/make_qe_inputs.py:51-52` 에 이미 있다). 단 "D3 끈 이완" 은 아니라고 적는다. Ag|흑연·흑연 층간(36–114원자)은 **DFT+D3 로 직접**, E(d) 스캔 포함 — 값싸다. 흑연 층간(실험 0.37 J/m²)을 DFT 세팅 대조 잡으로 봉인.

**5. [P1] NCM 기준값의 DFT 검증은 §3 을 다시 채워야 한다 — LiNiO₂ 1L 은 SDCP 가 여덟 번 반려된 그 계다**
- 근거: 계획 L109 는 "Ag 금속·LPSCl 절연 — 스미어링 같게" 만 답한다. 기준값 쪽 1L LiNiO₂ 시트는 +U·스핀·자기 basin 여럿(`estimand_card.md:83-99`, CLAUDE.md "기준과 대상이 같은 제약인가"). 게다가 DFT 급이 다르다(NCM PBE+U vs Ag PBE) — DFT 열은 급이 균일하지 않다. UMA 가 이 계에서 실패한 기록이 둘 있다: `v26c_MACE_cross_check` "UMA Wad R = −0.76 (inverted)" · `paper2_stage11` 45–225 J/m² "100–1000× over".
- 고치기: U 값·스핀 초기화·상태선택 규칙을 카드에 선언하고, **기준값 DFT 검증을 Ag 보다 먼저** 돈다 — 기준값이 존재하는지를 이게 결정한다.

**6. [P1] 기준값이 DEM 의 두께수렴 기준(ΔW < 0.05)을 못 넘는다**
- 근거: 1L LiNiO₂ 1.153 → 2L NCM811 ~2.0 (+74 %, `adhesion_final.md:228-232`) → 5L 2.674 ± 0.882 (12/20 유효, "cross-family FAILED", `adhesion_100seeds_analysis.md` §5L).
- 고치기: 기준값을 "1L LiNiO₂ 시트 · 두께 미수렴" 으로 라벨해 DEM 에 공개한다. 재계산 기준값에 3L 을 쓸지 비용을 물어 결정.

**7. [P1] "UMA 진공 민감도" 는 물리가 아니라 미진단 버그 신호 — 불변성 대조 잡 없이는 어떤 값도 못 쓴다**
- 근거: 유한 컷오프(~6 Å) MLIP 의 에너지는 국소 기여의 합이라 컷오프 밖 진공 크기에 의존할 수 없다. `adhesion_energy.md:134-139` 의 "60 Å 에서 10배" · `debug_history` "E_ncm = +248 eV" 는 그래프 구성/wrap 문제(원자가 셀 밖, pbc 처리)의 서명이고, "세 조건"(L141-146)은 원인 모르는 우회다. 계획은 이걸 규칙으로 재사용한다(L33).
- 고치기: 파이프라인 첫 잡 = 같은 슬랩을 진공 20/30/40/60 Å 에 wrap 해 E 가 1 meV/atom 안에서 같은지. UBER E(8 Å) ≈ E_sep(30 Å) (0.02 J/m² 안), 시드별 W_ad ≤ W_sep. 하나라도 어기면 정지.

**8. [P1] DFT 비용·설계가 계획에 없다 — repo 자체 견적은 계면 1건에 48 h KISTI 다**
- 근거: `adhesion_calibration_decision_2026_05_17.md:88-91`. 계획 L78 의 "~30회" 는 W_ad 항(시드당 +2)·UBER DFT(2 seeds × ~15점)·NCM +U 를 빼 먹었다 — 70회 이상. 금속 슬랩 k-점(Γ vs 2×2×1), 스미어링, PAW Ag + GBRV USPP 혼용(`generate_dft_inputs.py:41-45,64`; ecut 52/520), 계면 쌍극자 점검이 없다.
- 고치기: 프로브 1건(시드 하나의 E_int + E_sep)으로 실측 후 예산. E_sep 은 **분리 슬랩 두 개**로(같은 측면셀, 30 Å 이격은 D3 꼬리까지 동일) — 비용 절반. DFT 진공은 15 Å 로 줄여도 된다(장부에 적는다). 시드는 적응형: UMA 최저·중앙값 2개 먼저, 게이트 실패 시 5개로.

**9. [P1] 문턱·비교 규칙을 지금 봉인 — 계획 L114 의 규칙은 기준값 자체를 "보류" 로 만든다**
- 근거: 기준값 범위 0.555–1.85 가 1 J/m² 를 걸친다. 이력에 선별이 있다(`adhesion_final.md:9,34` "only seed with perfect order"; `adhesion_charts_comparison.md` "outliers >4.0 removed").
- 제안: 시드별 |W^{PBE} − W^{UMA}| ≤ max(0.15 J/m², 25 %) **그리고** 검증 시드 전부 급(<0.3 / 중간 / >1) 일치 **그리고** 부호 일치. 실패 → DFT 값이 보고값이 되고 UMA 는 기하 표본기로 격하. 급 판정은 **중앙값 + IQR** 로(평균 아님), 분포 차이는 Mann–Whitney. 시드 목록 사전 고정, 제외는 사전 선언 게이트(LBFGS 미수렴 `run_cathode_interface.py:180-193`, 반응 플래그, PS₄ 무결성)만.

**10. [P1] 반응성 게이트를 상태선택 정책으로 적는다**
- 근거: MP 벌크 반응에너지(Ag 는 귀금속이라 ~0, LiAg 는 강환원)는 접촉면 Ag–S 화학·Li/Ag 교환(Ag-argyrodite 가 존재한다)을 못 잡는다. repo 에 UMA 이완이 PS₄ 를 깬 선례가 있다(`db/structures/lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated`).
- 고치기: 시드별 관측량 + 문턱 사전 선언 — Ag–S < 2.5 Å 개수/Å²(접촉 플래그), SE 안의 Ag / Ag 안의 S·Li(반응 플래그 → 급격 계면 통계에서 제외·별도 보고), P–S 4배위 유지. 고정은 기준값과 같게 전부 자유(Ag 층간거리 기록).

**11. [P1] 면(face)·종단을 고정한다** — F-43m 은 반전대칭이 없어 두 (001) 면이 다르다. v30u 는 comp1 에 face 'A' 를 썼다(`run_li_migration_FINAL_combo.py:42`), 종단은 에너지 최소화된 적 없다(`adhesion.json` `correction_5`). NCM 을 봤던 그 면을 Ag 에도 쓴다고 카드에 적는다.

**12. [P2] 헤드라인 W_sep vs W_ad** — DEM 접촉법칙(JKR/DMT/cohesive)이 받는 건 열역학적 W_ad(이완)다. W_sep 은 상계. 둘 다 내고 헤드라인은 DEM 의 접촉모델이 정하게 한다. 계획 L53 의 명명 정정은 맞다.

**13. [P2] 변형 방향** — 같은 셀 W_sep·W_ad 는 변형에너지가 정확히 상쇄되므로 방향 변경이 비교성을 깨지 않는다(출판 관례의 α·ΔW_strain 이 바로 그 항이고 계획 L100 이 빼는 게 맞다). 단 변형률 표는 1번 셀로 다시 계산 — Ag(111) 직사각 7×4: −0.55/+0.45 % (a 4.086), −2.3/−1.3 % (a 4.16).

**14. [P2] 출처 기록** — `db/knowledge/fairchem/models.json` 13개 항목의 sha256 이 전부 `ff7e8d71…` 로 같다 → 체크포인트 해시가 아니다. 러너가 실제 `.pt` 해시·fairchem 버전·task·fmax·스텝·수렴 여부·D3 항을 시드별 CSV 에 남긴다.

**15. [P2] 원장** — `decisions.json` 에 adhesion 항목 0건. "기존 워크플로 관례" 는 비준된 적이 없다. 카드의 proposed 결정은 기준값과 Ag 양쪽의 보고량을 함께 정의해야 한다. 부수: `adhesion.json` `cell_matching` 에 "(2,2,2) 416at ADOPTED" 와 "(2,2,3) 624at FINAL" 이 공존, yaml 은 z-cut 통계·`uma-s-1p2`, `adhesion_energy.md:97` 도 1p2 — 카드 봉인 때 같이 고친다.

**16. [P2] P2 쌍 LPSCl↔탄소의 셀 매칭이 비어 있다**(계획 L64 "—"). 정방 20.11 Å 에 그래핀 직사각셀은 잘 안 맞는다(8×5: −2.1/+5.9 %). 뒤로 미루되 미해결이라고 적는다.

---

## plan 에서 맞는 것
- 워크플로 값을 조작상 **W_sep** 으로 부르고 이완 W_ad 를 따로 내는 것 (L53, L95-96).
- 출판 관례 α·ΔW_strain 을 넣지 않는 것 (L100) — 실험 순위에 맞춘 항이고 Ag 대응물이 없다.
- 선별된 1.277 이 아니라 20 seeds 전체 통계를 기준으로 삼고 W(s) 전부를 내는 것 (L35, L105).
- 기준값에도 DFT 검증을 거는 것 (L131) — 계획이 생각한 것보다 더 중요하다(5번).
- UMA 신뢰성을 "모른다" 고 쓰고 DFT 검증을 판정 조건으로 둔 것 (L107).
- UMA/PBE 격자상수 차이를 보고 두 단계 셀을 같게 잡는 것 (L67).
- MP 사전검사를 gabia `uma` env 로 가는 것 (L76) · Ag 4→6층 점검 (L79, L112).

## Codex 에 꼭 물을 것
1. 정방 SE(관용셀 2×2×3, 20.11 Å) 를 육방 NCM 7×7 셀(20.146 Å, 120°)에 `se_frac = se_cart @ inv(ncm_cell); % 1.0` 으로 넣는 것은 변형인가 wrap 인가 — 기준값 20 seeds 가 이 빌더로 나왔다면 그 W 는 무엇을 잰 것이고, 재생성 없이 Ag 와 비교할 수 있는가.
2. UMA(omat) 가 분산 없는 PBE(+U) 기준계라면 검증 짝은 PBE(noD3) 여야 하지 않나 — 물리흡착 짝(Ag|흑연·층간)은 MLIP 단계를 건너 DFT+D3 로 직접 가야 하나.
3. 유한 컷오프 MLIP 에서 진공 30→60 Å 이 W 를 10배 바꿨다는 기록을 어떻게 해석하나 — 어떤 불변성 대조 잡을 통과해야 그 파이프라인의 에너지를 믿나.
4. 1L LiNiO₂ 기준값(1L 1.15 → 5L 2.67)을 DEM 의 ΔW < 0.05 기준 아래에서 "기준값" 으로 쓸 수 있나 — 쓴다면 NCM 쪽 DFT 검증의 U·스핀·basin 상태선택 정책은.
5. 봉인 문턱 숫자(|ΔW| 절대·상대, 급 일치)와 실패 시 처리(DFT 값 승격 vs UMA 폐기), 그리고 DEM 접촉모델에 맞는 헤드라인(W_ad vs W_sep) — 결정 가능한 답으로.

---

**확인 못 한 것(해소 방법):** 기준값 20 seeds 를 낸 v5 원본 스크립트와 `comp1_slab_v2.xyz` 는 repo 에 없다. 1번의 셀 판단은 남은 코드 경로(v6 빌더·NCM 빌더·CIF 격자·기록된 A·밀도·변형률)의 정합에서 나온 추정이다 — V100 백업의 슬랩 파일을 읽어 `cell` 과 이웃거리 히스토그램을 뽑으면 한 번에 갈린다. UMA 진공 민감도(7번)도 20/30/40/60 Å 대조 잡 하나로 갈린다.

---

## 부록 — 우리 쪽 확인 (2026-09-23, 원문 대조)

### A. 원문에 대 본 주장 (P0 전부 + 인용 근거)

| # | 주장 | 결과 | 본 곳 |
|---|---|---|---|
| 1 | SE 는 입방 a = 10.055 Å (90°) | ✅ | `db/structures/comp1_V0_k444.cif` `_cell_length_a 10.0551` · `_cell_angle_gamma 90.0` |
| 1 | comp1 은 `repeat [2,2,3]` · `ncm_nx 7` | ✅ | `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` COMPS |
| 1 | NCM 은 육방 a = 2.878 Å (7×7 → 20.146 Å, 120°) | ✅ | `tools/doping/run_cathode_interface.py` `build_ncm_1L` |
| 1 | 빌더는 **변형이 아니라 wrap** | ✅ | `adhesion_v6_anneal_test.py` `build_interface`: `se_frac = se_cart @ ncm_inv` → `% 1.0` → `se_frac @ ncm_cell`. 데카르트 좌표를 NCM 기저로 옮겼다 되돌리므로 **좌표는 그대로**이고 주기만 바뀐다. 주석은 *"applies xy strain"* 이다 — 주석과 수식이 다르다 |
| 1 | 계면 A = 351.5 Å² (= 육방 셀) | ✅ | `kb/results/adhesion_final.md` 표 (`Li6 … 351.5`) |
| 1 | SE 밀도 1.78 at/Å² 를 썼다 (정방이면 1.545) | ✅ | `adhesion.json` `cross_family` (*"1.38 vs 1.78 at/A2"*) |
| 1 | 팀이 스스로 의심했다 | ✅ | `adhesion.json` `comp1_comp2_d_min_close`: *"d_min=1.0-1.1 Å … possible cubic SE + hex NCM PBC artifact"* — **최근접 원자간 거리 ~1 Å** |
| 2 | 기준값은 relax-only · MQA 없음 · `uma-s-1p1` · 20 seeds | ✅ | `adhesion_final.md` Method 절 · `adhesion_energy.md` Protocol 4 *"Relax only (MQA 없음)"* |
| 2 | 800 K MQA 는 시도했다 실패 | ✅ | `kb/methodology/adhesion_methods_comparison.md` *"58/248 atoms migrated"* |
| 3 | 100 seeds 1.151 ± 0.245 · 5L 2.674 ± 0.882 | ✅ | `kb/results/adhesion_100seeds_analysis.md` |
| 3 | 출판 표 1.277 은 **20 중 5 seeds 선별** | ✅ | `adhesion_final.md`: *"5 selected per family to match experimental ratios"* · 시드 (42, 49, 52, 58, 60) · figure seed 52 *"only seed with perfect order"* |
| 3 | "버전 올리면 전부 다시 뽑는다" 규율 | ✅ | `webapp/fairchem.py` `OUR_BANS` |
| 4 | omat 기준계 = PBE/PBE+U (분산 없음) | ✅ | `webapp/fairchem.py` `OUR_BANS` |
| 4 | QE D3(BJ) 입력이 이미 있다 | ✅ | `tools/vgcf_hbn/make_qe_inputs.py` `vdw_corr='grimme-d3'` · `dftd3_version=4` |
| 6 | 1L → 2L +74 % | ✅ | `adhesion_final.md` 두께 표 |
| 8 | DFT 계면 1건 ~48 h KISTI | ✅ | `kb/methodology/adhesion_calibration_decision_2026_05_17.md` Option C |
| 10 | UMA 이완이 PS₄ 를 깬 선례 파일 | ✅ | `db/structures/lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated` |
| 11 | comp1 face 'A' | ✅ | `tools/adhesion_v30u/run_li_migration_FINAL_combo.py` COMPS |
| 14 | models.json 13개 sha 가 전부 같다 | ✅ | `ff7e8d71f6114301` 13/13 |
| 15 | decisions.json 에 adhesion 결정 0건 | ✅ | 57건 중 0 |

### B. 대 보지 못한 것
- **1번의 결정적 확인** — 기준값 20 seeds 를 낸 **v5 원본 빌더**는 유실됐다. 위 증거(A = 351.5 · 밀도 1.78 · d_min ~1 Å · v6 빌더)는 전부 같은 방향이지만 **추정**이다. V100 백업의 `comp*_v5xy_s52.xyz`(또는 `comp1_slab_v2.xyz`) 셀과 최근접 거리 분포를 보면 갈린다 — 1저자 쪽 실행.
- **7번의 물리 논증**(유한 컷오프 MLIP 는 진공에 불변이어야 한다) — 논증은 타당하지만 UMA 의 수용장(층수 × 컷오프)을 우리가 재지 않았다. 리뷰가 제안한 **진공 불변성 대조 잡**이 이걸 가른다 (싸다).
- 5번 LiNiO₂ 1L 의 상태 다중성 — 계산 전이라 확인 대상이 아니다. 카드에 상태선택 정책으로 적는다.

### C. 리뷰가 놓친 것 (우리가 찾음)
1. ⛔ **repo 금지 규칙: MLIP 절대값을 인용하지 않는다 (σ · W_ad)** — `webapp/fairchem.py` `OUR_BANS`: *"같은 프로토콜 안의 순서·비율만 쓴다. 비율도 멀티시드로 판정한 것만."*
   DEM 쪽은 **절대값(J/m²)** 을 원한다. ⇒ UMA 절대값은 넘길 수 없다. 넘길 수 있는 것은 **같은 프로토콜 안의 비(Ag/NCM)** 또는 **DFT 값**이다 (DFT 단일점을 UMA 기하 위에서 낸 값이 이 금지에 걸리는지는 선언이 필요하다).
2. ⛔ **"실험값" 은 J/m² 가 아니라 AFM 의 aJ 다.** `adhesion_final.md` 표 머리 *"Expt (aJ)"* · `adhesion_energy.md` *"paper AFM aJ 값 194–316, r≈10nm 접촉 πr² 환산 1 J/m² ↔ ~314 aJ; 절대 스케일은 순위·상관으로만 비교"*.
   그런데 `adhesion.json` 은 같은 숫자를 *"Experimental Wad is +0.18-0.32 J/m²"* · *"Sundar 2025: 0.2-0.4 J/m²"* 로 적었다 — **숫자가 aJ 값과 똑같다 → 단위 오독이다.** 접촉 반경을 가정하지 않으면 J/m² 로 못 바꾼다 (r ≈ 10 nm 가정이면 194 aJ ≈ 0.62 J/m²).
   ⚠ **이 오독을 우리가 커밋 `b27dd3b8e` 에서 계획 §1 ⚠4 · BV §3.7 로 옮겼다** ("paper exp 0.194 J/m²", "v5 기준값은 그 약 5배", "0.19 → 물리흡착 급"). 다음 커밋에서 정정한다.
