---
title: LPSCl | Ag–C | VGCF 점착일(W_ad) — 계획 v2 (내부 리뷰 NO-GO 반영) · 보고량 카드 초안
date: 2026-09-23
updated: 2026-09-23
tags: [adhesion, wad, interface, lpscl, silver, graphite, vgcf, anode, dem-input, estimand, review-pending]
status: 계획 v2 — 내부(Fable) 리뷰 NO-GO(v1) 반영 끝 · Codex BV 발송 전 · 계산 0. 파이프라인은 두 리뷰 뒤에 건다 (1저자 2026-09-23)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# LPSCl | Ag–C | VGCF 점착일(W_ad) — 계획 v2 · 보고량 카드 초안

> **요청** (DEM 쪽, 1저자 전달 2026-09-23 · **수정본 반영**): 음극 적층 LPSCl | Ag–C | VGCF 의 두 계면
> ① LPSCl↔Ag–C ② Ag–C↔VGCF 를 구성 쌍으로 나눠(P1: **LPSCl↔Ag · Ag↔흑연**) DEM 박리 시험의 입력 점착일을 달라.
> 정확도 목표 = 자릿수(물리흡착 ≲ 0.3 J/m² vs 화학결합 ≳ 1 J/m²).
> **수정본의 핵심**: 주값 정의를 **기존 LPSCl|NCM 워크플로의 isolated slab W_ad** 에 맞춘다 · W_sep 도 같이 ·
> 계면 제작 프로토콜 **v5** 와 **SE 슬랩 재사용** · **MLIP 값은 DFT 단일점으로 검증** ⇒ LPSCl|Ag 를 LPSCl|NCM 과 바로 나란히 비교.
> 1저자: *"파이프라인 걸기 전에 Codex 랑 우리 자기 Fable 리뷰도 받고 하자."*
> **트랙**: 우리 DFT → **1저자 = 사용자** (결정이 그 자리에서 난다).

## 개정 이력 (위가 최신)

- **v2 (같은 날 오후)** — 내부 리뷰(Fable) **NO-GO** (`kb/reviews/internal_review_wad_agc_fable_2026_09_23.md`). P0 4건을 원문에 대 보고 전부 맞아서 반영했다. 바뀐 것:
  1. **기준값을 낸 방법을 잘못 읽었다.** v1 은 v5 = *800 K 표면 MQA* 로 적었다 — `surface_mqa_v5.yaml` 템플릿만 보고 결과 문서 `kb/results/adhesion_final.md` 를 안 봤다.
     실제 기준값은 **이완만(MQA 없음) · `uma-s-1p1` · 20 seeds** 다. 800 K MQA 는 시도했다가 Li 섞임으로 계면이 망가져 **버린 방법**이다.
  2. **기준 계면의 셀이 맞지 않는다** (§1 ⚠1). SE 는 **정방 20.11 Å** 인데 계면 셀은 NCM 의 **육방 20.146 Å** 이고, 빌더가 변형이 아니라 wrap 을 했다.
     ⇒ v1 의 *"SE 측면 육방 20.13 Å 에 Ag(111) 7×7"* 설계와 변형률 표는 **폐기**. 기준값 **숫자도 재사용하지 않고** 같은 파이프라인에서 다시 낸다.
  3. **검증 짝을 바꾼다.** UMA(omat) 는 **분산 없는 PBE(+U)** 를 배운 모델이라 짝은 **PBE(D3 없음)** 이다. v1 은 PBE+D3 와 붙여서 D3 몫이 "MLIP 오차" 로 읽힐 뻔했다.
     물리흡착 짝(Ag|흑연 · 흑연 층간)은 MLIP 를 건너 **DFT+D3 로 직접** 간다.
  4. ⛔ **v1 §1 ⚠4 의 "paper exp 0.194 J/m²" 는 단위 오독이었다.** 실험값은 AFM 의 **aJ**(에너지)다 — 원장 `adhesion.json` 의 오독을 내가 그대로 옮겼다(커밋 `b27dd3b8e`).
     원장에는 정오표를 달았다(`⛔_정정_2026_09_23_실험값_단위_aJ`). ⇒ *"v5 기준값은 실험의 약 5배"* · *"0.19 → 물리흡착 급"* 은 **철회**.
  5. **repo 금지 규칙을 카드에 넣는다**: *"MLIP 절대값을 인용하지 않는다 (σ · W_ad)"* (`webapp/fairchem.py` `OUR_BANS`) ⇒ DEM 에 **UMA 절대값은 못 넘긴다** (§6-1).
- **v1 (같은 날 오전)** — 초판. 그 안에서 한 번 정정: 초판의 *"DFT 급 LPSCl 슬랩·워크플로가 없다"* 는 **틀렸다**(첫 검색 결과가 60개에서 잘렸는데 확인하지 않았다).

---

## 0. 한 줄 요약 (v2)

- **재사용하는 것 = 조작과 규약**: xy-shift 시드 · **이완만** · 분리 +30 Å(셀도 +30 Å) 단일점 · 진공 30 Å · SE 슬랩 규약(comp1 **관용 입방셀 2×2×3**, 624원자, 30 Å) · 계산기 `uma-s-1p1`/omat.
- **재사용하지 않는 것 = 기준값 숫자**(1.153 등). 셀이 wrap 으로 지어졌고 스크립트·슬랩 파일이 유실됐다 ⇒ **NCM 기준값부터 같은 파이프라인에서 다시 낸다.**
- **셀**: 전부 SE 고유 **정방 20.11 × 20.11 Å (A 404 Å²)** 위 — LiNiO₂ 1L 직사각 7×4(224원자) · Ag(111) 직사각 7×4 × 4층(224원자). 두 계면 모두 **848원자**.
- **검증**: 같은 기하에서 UMA ↔ **PBE(D3 없음)**. 헤드라인 후보는 PBE+D3 = PBE + ΔD3.
- **DEM 에 넘길 것**: UMA 절대값은 금지 규칙에 걸린다 → **같은 프로토콜 안의 Ag/NCM 비** 또는 **DFT 값** — 1저자 결정 (§6-1).

---

## 1. 워크플로 — 무엇이 있나 (repo 실측 · v2 에서 정정)

| 자산 | 내용 |
|---|---|
| `kb/results/adhesion_final.md` | **기준값을 낸 방법의 정본** — 결정질 슬랩 · xy-shift · **LBFGS 이완만(MQA 없음 — Li 섞임 방지)** · `W = (E_sep − E_int)/A`, 분리 30 Å + 셀 확장 · **`uma-s-1p1`** · 20 seeds · Li6 셀: NCM 7×7×1 · SE 2×2×3 · 624원자 · 30 Å · **A 351.5 Å²**. ⚠ 출판 표(comp1 **1.277**)는 20 중 **5 seeds 를 골랐다** (*"5 selected per family to match experimental ratios"*) |
| `kb/results/adhesion_100seeds_analysis.md` | 100 seeds: comp1 1.151 ± 0.245 · **5L NCM** comp1 2.674 ± 0.882 (12/20 유효) |
| `kb/methodology/adhesion_energy.md` | 정의 줄은 isolated slab · `v5_working` = 분리 후 **이완 없이 단일점** · 247줄 *"엄밀히는 무이완 분리라 work of separation 계열"* · Protocol 4 *"Relax only (MQA 없음)"* · 진공 30 Å 규칙 · 실험값은 **AFM aJ** (*"r≈10nm 접촉 πr² 환산 1 J/m² ↔ ~314 aJ; 절대 스케일은 순위·상관으로만"*) |
| `kb/methodology/adhesion_methods_comparison.md` | 800 K MQA → *"Li interdiffusion destroyed interface (58/248 atoms migrated)"* · 500 K 도 Li 횡단 ⇒ **이완만 채택** |
| `db/inputs/adhesion_templates/surface_mqa_v5.yaml` | ⚠ **기준값의 설정이 아니다** — 800 K MQA · `uma-s-1p2` · SE 2×2×1 (버린 방법의 템플릿) |
| `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` | v6 (NCM 고정 · SE 500 K) + 계면 빌더 `build_interface` — **wrap 빌더** (§1 ⚠1) |
| `tools/doping/run_cathode_interface.py` | v6 러너 · `build_ncm_1L` = LiNiO₂ **1층**, 육방 a 2.878 Å |
| `webapp/fairchem.py` `OUR_PINNED` · `OUR_BANS` | 핀 `uma-s-1p1`/omat · ⛔ **MLIP 절대값 인용 금지 (σ · W_ad)** — *"같은 프로토콜 안의 순서·비율만, 비율도 멀티시드로"* · 버전 올리면 **전부 다시 뽑는다** · omat 기준계 = **PBE/PBE+U** |
| `db/properties/adhesion.json` | 기록 — `xy_shift` 20 seeds · `cell_matching` · anomalies · ⛔ 정오표(실험값 aJ) |

### ⚠1 기준 계면의 셀이 맞지 않는다 (내부 리뷰 P0-1 · 원문 대조 확인)
- **SE**: `db/structures/comp1_V0_k444.cif` 는 입방 a = 10.055 Å → 관용셀 2×2 = **20.11 × 20.11 Å, 90°, 404 Å²**.
  원장의 *"prim 2×2×3"* 은 오기다 — 13원자 원시셀이면 156원자이고, 624원자는 52원자 관용셀 × 12 다.
- **계면 셀**: LiNiO₂ 육방 7×7 = **20.146 Å, 120°, 351.5 Å²**. 기록된 A = 351.5 와 *"변형 0.2 %"* 는 **변 길이만** 비교한 값이다(각도 90° → 120° 는 어디에도 없다).
- **빌더** `build_interface`: `se_frac = se_cart @ inv(ncm_cell)` → xy 이동 → `% 1.0` → `@ ncm_cell`. 주석은 *"applies xy strain"* 인데
  데카르트 좌표를 NCM 기저로 옮겼다 되돌리므로 **좌표는 안 변한다** — 변형이 아니라 **wrap** 이다. 404 Å² 정방 조각을 351.5 Å² 육방 셀에 접어 넣으면
  **13 % 과밀**(원장이 쓴 *"1.78 at/Å²"* = 624/351.5 · 정방이면 1.54) + 경계에서 원자가 겹친다.
  원장 스스로 적어 뒀다: *"d_min=1.0-1.1 Å … possible cubic SE + hex NCM PBC artifact"* (최근접 원자간 거리 ~1 Å).
- ⚠ 기준값 20 seeds 를 낸 **v5 원본 빌더는 유실**됐다. 증거가 전부 같은 방향이지만 **추정**이다 — V100 백업 슬랩의 셀·최근접 거리로 갈린다 (§6-3).
- ⇒ 기준값 숫자는 **재사용하지 않는다.** 올바른 셀에서 NCM 기준값부터 다시 낸다 (§3 단계 1).
  (comp3–5 는 육방축 슬랩이라 육방–육방이다 — 이 문제가 작다. 이 캠페인과 무관하지만 기록.)

### ⚠2 "isolated slab W_ad" 는 조작상 W_sep 이다 (v1 유지)
정의 줄은 isolated slab 이지만 실제 조작은 **분리 후 이완 없는 단일점**이고, 방법론 문서 247줄이 스스로 *"work of separation 계열 (W_ad 의 상계)"* 라 적었다.
⇒ 요청서 용어로 **이 값은 W_sep** 이다. 이완 슬랩 W_ad 는 워크플로에 없고 새로 낸다.

### ⚠3 comp1|NCM 에 원장 숫자가 여럿이다 (v2 정정 — v1 표는 aJ 오독 포함)

| 무엇 | comp1 (J/m²) | 조작 | 근거 |
|---|---|---|---|
| 20 seeds (골라내지 않은 통계) | 평균 1.153 · 중앙값 0.962 · 0.555–1.850 | 이완만 · 분리 단일점 · UMA 1p1 · **wrap 셀** | `adhesion.json` `xy_shift` |
| 100 seeds | 1.151 ± 0.245 | 같음 | `adhesion_100seeds_analysis.md` |
| 출판 표 | 1.277 | **20 중 5 seeds 선별** — ⛔ 기준값 아님 | `adhesion_final.md` |
| 2L NCM811 | ~2.0 (+74 %) | 두께 2층 | `adhesion_final.md` |
| 5L NCM | 2.674 ± 0.882 (12/20) | 두께 5층 | `adhesion_100seeds_analysis.md` |
| paper #1 출판식 | 0.075 (= 2.708 − 2.633) | `WELLS_RAW − α·ΔW_strain`, α = 1 | `db/properties/alpha_sensitivity_FINAL.json` |
| v6 stage 11 | 45–80 | NCM 고정 500 K + 분리 — 원장 자진단 *"artificial dangling-bond energy"* | `adhesion.json` `paper2_stage11…` |

- **실험(paper #1, AFM)**: comp1 **194 aJ** (comp1–5 = 180–316 aJ). **면적당 에너지가 아니다** — J/m² 로 바꾸려면 접촉 반경을 가정해야 한다(방법론 문서 가정 r ≈ 10 nm → 1 J/m² ≈ 314 aJ).
  원장이 인용한 *"Sundar 2025: 0.2–0.4 J/m²"* 는 litdb 의 그 digest 에 점착 값이 없다 — **귀속 미확인**.
- ⇒ 같은 comp1|NCM 이 **두께와 조작에 따라 1–2.7 J/m²** 를 움직인다 (출판식·v6 은 별개의 양). DEM 두께수렴 기준(ΔW < 0.05)은 기준 쪽이 못 넘는다 → 새 기준값은 **"1L LiNiO₂ 시트 · 두께 미수렴"** 으로 라벨한다 (내부 리뷰 P1-6).

---

## 2. 계면별 셀 (v2 — SE 고유 정방셀 20.11 Å 위)

| 계면 | 셀 | 변형 (SE 에 맞춤) | 원자 |
|---|---|---|---|
| **기준 LPSCl↔NCM** | SE 관용 2×2×3 (정방 20.11 Å · 30 Å · 624) + **LiNiO₂(001) 1L 직사각 7×4** (2.878 × 4.985 → 20.146 × 19.939 Å) | NCM −0.18 % / +0.86 % | 624 + 224 = **848** |
| **P1-a LPSCl↔Ag** | 같은 SE + **Ag(111) 직사각 7×4 · 4층** (a 4.086: 2.889 × 5.004 → 20.225 × 20.017 Å) | Ag −0.57 % / +0.46 % (a 4.086) · −0.91 % / +0.12 % (4.10) · **−2.33 % / −1.32 % (PBE 4.16)** | 624 + 224 = **848** |
| **P1-b Ag↔흑연** | Ag(111) × 흑연(0001) 작은 초격자 — 워크플로 밖 · **DFT+D3 직접** | (√3×√3)R30° Ag / 흑연 2×2 류 — 셀은 봉인 때 다시 계산 | 36–114 |
| P2 LPSCl↔탄소 | ⚠ **미해결** — 정방 20.11 Å 에 그래핀 직사각이 잘 안 맞는다 (8×5: −2.1 / +5.9 %) | — | — |
| P2 흑연 층간 | **DFT 세팅 대조 잡** (문헌 소환값 ~0.37 J/m² 와 비교 — litdb 원문 확보 전 봉인 금지) | — | 4–8 |

- **면·종단**: F-43m 은 반전대칭이 없어 두 (001) 면이 다르다 → comp1 **face 'A'** (v30u 선례, `tools/adhesion_v30u/run_li_migration_FINAL_combo.py`)로 고정하고 NCM·Ag 에 **같은 면**을 쓴다.
- **SE 원본**: repo 에 있는 것은 `db/structures/comp1_V0_k444.cif` (a 10.055). 옛 슬랩이 쓴 원격 `comp1_V0.cif` 와 같은지는 **확인 전** — 어차피 재생성이라 새 기준값·Ag 가 같은 파일을 쓰면 된다.
- ⚠ UMA 이완 격자와 PBE 격자가 다르다(Ag 4.086 → 4.16) → 두 단계에서 **같은 셀**을 쓰고 변형률을 표에 적는다.

---

## 3. 단계와 비용 (⚠ 규모 감각 — 약속 아님)

| 단계 | 내용 | 어림 |
|---|---|---|
| 0 | **불변성 대조 잡 (UMA)** — 같은 슬랩을 진공 20/30/40/60 Å 에 놓고 E 가 **1 meV/atom** 안에서 같은지 · UBER E(8 Å) ≈ E_sep(30 Å) (**0.02 J/m²** 안). 어기면 **정지** (원장의 *"60 Å 에서 10배"* 는 국소 MLIP 로는 설명이 안 된다 — 진단 전에는 어떤 값도 못 쓴다) | GPU 분 단위 |
| 0-a | **wrap 가설 확인** — 옛 빌더로 기준 계면 1개를 재생성해 최근접 거리·밀도·PS₄ 무결성 (+ 가능하면 V100 백업 슬랩 셀, §6-3) | 분 |
| 0-b | MP 반응에너지 사전검사 (gabia `uma` env) — **참고용**: 벌크 반응에너지는 접촉면 Ag–S 화학·Li/Ag 교환을 못 잡는다 | 0 |
| 1 | **NCM 기준값 재계산** — UMA 1p1/omat · 이완만 · 848원자 · 시드 **42–61 사전 고정 (20)** · W_sep + W_ad + UBER(2 seeds) | GPU ~3 h (820원자 MQA+이완 8 min/seed 실측 기준 — 이완만이면 더 짧다) |
| 2 | **P1-a LPSCl↔Ag** — 같은 조건 20 seeds + W_ad + UBER | GPU ~3 h |
| 3 | **DFT 검증** — ① 프로브 1건(시드 1개: E_int + **분리 슬랩 둘**)으로 시간 실측 → 예산 ② 적응형: UMA 최저·중앙값 **2 seeds** 먼저, 게이트 실패 시 5 ③ **NCM 먼저**(상태선택 정책 선언 뒤) → Ag | 848원자 단일점 — repo 견적 **계면 1건 ~48 h KISTI**. 실측 전 약속 안 함 |
| 4 | **P1-b Ag↔흑연 · 흑연 층간** — DFT+D3 직접, E(d) 스캔 포함 | 작다 (36–114원자) |
| 5 | 두께 — Ag 4 → 6층 1 seed · NCM 은 1L 라벨 (3L 은 §6-4) | 소 |

GPU: gabia = b2o3 사건 빈도 MD (≈5–6일) → 끝나면 modelc_2x 탄성 · kgy = 공유. DFT 는 **KISTI**. DFT 설정(금속 슬랩 k-점 · 스미어링 · PAW/USPP 혼용 · 계면 쌍극자)은 프로브에서 정한다.

---

## 4. 보고량 카드 초안 v2 (proposed — 비준 전)

### §1 무엇을 원하는가
> **같은 조작 · 같은 SE 셀 규약 · 같은 계산기**로 낸 LPSCl|Ag 와 (다시 낸) LPSCl|NCM 의 **W 분포**를 나란히 놓고, 그 **비**와 자릿수 급을 —
> 같은 기하의 **DFT(PBE) 로 검증된** 짝으로 — 말한다. 헤드라인 절대값은 DFT(PBE+D3) 에서만.

### §1-c 답하지 않는 것
> 반응 **후** 계면(Ag–S 화합물 · LiAg 합금 뒤) · 실험 박리강도 · 실접촉면적·구동압(DEM 층의 몫) · `α·ΔW_strain` 보정값과의 비교 ·
> **두께 수렴된** NCM 값 (1L 라벨) · **UMA 절대값** (repo 금지 규칙) · AFM aJ 와의 절대 비교.

### §2 재는 양
```
W_sep(s)  = [E_sep(s) − E_int(s)] / A            # 분리 +30 Å · 셀 +30 Å · 이완 없음 (워크플로와 같은 조작)
W_ad(s)   = [E_A^rel + E_B^rel − E_int(s)] / A   # 각 슬랩을 같은 셀에서 이완 (워크플로에 없던 값) — 항상 W_ad ≤ W_sep
W^PBE     = 같은 식 · PBE(+U: NCM 쪽) 단일점 · UMA 기하 위 · D3 없음      ← UMA 의 검증 짝
W^PBE+D3  = W^PBE + ΔD3(같은 기하 · D3(BJ) 가산항 — 고정 기하에서 정확히 분해)   ← 헤드라인 후보
UBER E(d) = 이완 계면을 강체로 z-스캔, 평형 + 8 Å
```
s = xy-shift 시드. A = 404 Å² (정방 20.11²). *"D3 끈 값"* = **W^PBE** (같은 기하에서 D3 항 제외) — *D3 끄고 이완한 값*이 **아니다** (물리흡착 계면은 D3 없이 이완하면 떨어진다).
⛔ `− α·ΔW_strain` 보정은 넣지 않는다 (실험 순위로 맞춘 항이고 Ag 에 대응물이 없다. 같은 셀의 W_sep·W_ad 에서 변형에너지는 상쇄된다).

### §3 잘 정의되는가
| 물음 | 답 | 처리 |
|---|---|---|
| 상태가 하나인가 | 아니다 — xy registry 20개 | 스칼라로 뭉치지 않는다: **W(s) 전부 + 중앙값·IQR** (평균 아님) |
| 반응성 계면인가 | 이완만으로도 Ag–S 접촉 · Li/Ag 교환이 생길 수 있다 (Ag-argyrodite 가 존재) · UMA 이완이 PS₄ 를 깬 선례 (`lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated`) | 시드별 관측량·문턱 **사전 선언**: Ag–S < 2.5 Å 개수/Å² (접촉 플래그) · SE 안 Ag / Ag 안 S·Li (**반응 플래그** → 급격 계면 통계에서 빼고 따로 보고) · P–S 4배위 유지 |
| NCM 쪽 DFT 상태가 하나인가 | **아니다** — LiNiO₂ 1L: +U · 스핀 · 자기 basin 여럿 (SDCP 가 여덟 번 반려된 그 종류) | U 값 · 스핀 초기화 · **상태선택 규칙**을 카드에 선언 → **NCM 을 Ag 보다 먼저** (기준값이 존재하는지를 이게 정한다) |
| DFT 급이 같은가 | NCM PBE+U vs Ag PBE | U 를 명시하고 표에 급을 같이 적는다 |
| MLIP 가 믿을 만한가 | 모른다 — 진공 민감도(미진단) · 이 계열에서 UMA 순위 역전 기록(R −0.76) | 단계 0 불변성 대조 + DFT 게이트 (§4) |
| 기준값이 하나인가 | 아니다 (§1 ⚠3) · 셀 wrap 의심 (§1 ⚠1) | **같은 파이프라인 재계산 20 seeds**, 옛 100-seed 세트와 중앙값·IQR 로 1회 대조만 (병합 금지) |
| 참조 상태가 같은 전자 상태인가 | Ag 금속 · LPSCl 절연 · NCM +U | 스미어링을 모든 항에 같게 · 분리 슬랩 둘도 같은 설정 |

### §4 게이트 (proposed — Codex 뒤 봉인)
- **불변성**: 진공 20/30/40/60 Å E 차 ≤ 1 meV/atom · UBER E(8 Å) vs E_sep ≤ 0.02 J/m² · 시드별 W_ad ≤ W_sep. **하나라도 어기면 정지.**
- **DFT 검증** (내부 리뷰 제안값): 시드별 |W^PBE − W^UMA| ≤ **max(0.15 J/m², 25 %)** **그리고** 급(< 0.3 / 중간 / > 1) 일치 **그리고** 부호 일치.
  실패 → **DFT 값이 보고값**이 되고 UMA 는 기하 표본기로 격하.
- **두께**: Ag 4 → 6층 ΔW < 0.05 J/m² (요청서) · NCM 은 1L 라벨.
- **분포 비교**: 중앙값 + IQR · Mann–Whitney. 시드 목록 사전 고정(42–61). 제외는 **사전 선언 게이트만** (LBFGS 미수렴 · 반응 플래그 · PS₄ 무결성).

### §5 주장 / 비주장
- ✅ *"같은 조작(xy-shift · 이완만 · 분리 단일점) · 같은 SE 셀 · 같은 계산기(uma-s-1p1/omat)에서 LPSCl|Ag 와 LPSCl|NCM(1L LiNiO₂ · 두께 미수렴)의 W_sep 비는 … ; DFT(PBE) 검증 n seeds 통과"*
- ✅ (DFT 게이트 통과 시) *"PBE+D3 단일점 W_sep(Ag) = … (n seeds, 중앙값·IQR)"*
- ⛔ UMA 절대값 인용 · ⛔ 옛 기준값 숫자(1.153 · 1.277 등)와 새 값 병합 · ⛔ `α·ΔW_strain` 보정값과 비교 · ⛔ AFM aJ 를 J/m² 로 · ⛔ 시드 하나로 결론 · ⛔ 계산 안 한 칸을 문헌으로 채우기

---

## 5. 리뷰 (1저자 지시)

1. **내부 (Fable)** — **NO-GO (v1)** → `kb/reviews/internal_review_wad_agc_fable_2026_09_23.md`. P0 4건 원문 대조 확인 · 이 v2 에 반영.
2. **Codex BV** — v2 기준으로 개정해서 보낸다 (`kb/reviews/codex_BV_prompt_wad_lpscl_ag_c_vgcf_2026_09_23.md`).
3. 두 리뷰 반영 → 카드 봉인 → `decisions.json` proposed (**NCM 기준값과 Ag 보고량을 함께 정의** — 지금 adhesion 결정은 0건) → 1저자 비준 → 파이프라인.

## 6. 결정 필요 (1저자 — 이 트랙의 1저자는 사용자)

1. **DEM 에 무엇을 넘기나** — UMA 절대값은 금지 규칙에 걸린다. 남는 것:
   (a) **DFT 값** (PBE+D3 헤드라인 · PBE 짝) · (b) **같은 프로토콜의 Ag/NCM 비** (NCM 절대 기준은 DEM 쪽이 고른다) ·
   (c) 비 × 실험 NCM — 실험이 **aJ** 라 J/m² 기준이 없다(접촉 반경 가정 필요) → 권하지 않는다.
2. **DEM 쪽에 대응표(§1 ⚠3)를 보여 주고** 그쪽이 말한 "isolated slab W_ad" 가 어느 것이었는지 **고르게 할지** — 권고: 보여 준다. 그걸 모르면 "나란히" 가 성립하지 않는다.
3. **V100 백업 확인** (wrap 가설) — `comp*_v5xy_s52.xyz` 의 셀과 최근접 거리. 1저자 쪽 실행. 안 해도 계획은 안 바뀐다(어차피 재계산) — 원장 정오표의 **확정도**만 바뀐다.
4. **NCM 두께** — 1L 라벨로 갈지, 3L 까지 볼지 (비용).
5. **기계** — UMA 단계 GPU (gabia 는 b2o3 뒤 탄성 대기) · DFT 는 KISTI.

## 출처
- 정본: `kb/results/adhesion_final.md` · `kb/results/adhesion_100seeds_analysis.md` · `kb/methodology/adhesion_energy.md` · `kb/methodology/adhesion_methods_comparison.md` · `kb/methodology/adhesion_calibration_decision_2026_05_17.md`
- 코드: `db/inputs/adhesion_templates/{surface_mqa_v5.yaml, adhesion_v6_anneal_test.py}` · `tools/doping/run_cathode_interface.py` · `tools/adhesion_v30u/` · `webapp/fairchem.py` · `tools/vgcf_hbn/make_qe_inputs.py` (QE D3(BJ))
- 원장: `db/properties/adhesion.json` (`xy_shift` · `cell_matching` · anomalies · ⛔ 정오표) · `db/properties/alpha_sensitivity_FINAL.json` · `db/structures/comp1_V0_k444.cif`
- 리뷰: `kb/reviews/internal_review_wad_agc_fable_2026_09_23.md` (내부 · NO-GO v1) · `kb/reviews/codex_BV_prompt_wad_lpscl_ag_c_vgcf_2026_09_23.md`
- 문헌: `kb/papers/adhesion_literature_review.md` · litdb: bucci2017 · bucci2018 · choi2025 · doux2020 · cronau2021 · dmt1975 · thorntonning1998 · pasha2014 · thakur2014 · luding2008 · fan2026
