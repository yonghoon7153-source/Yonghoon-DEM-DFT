---
title: "리뷰 BV 프롬프트 — LPSCl | Ag–C | VGCF 점착일: 기존 LPSCl|NCM 워크플로를 재사용해도 같은 양을 재는가"
date: 2026-09-23
updated: 2026-09-23
tags: [review, codex, adhesion, wad, interface, lpscl, silver, graphite, estimand, uma, dft-verification]
status: 발송대기 — 1저자가 보낸다. 내부 Fable 리뷰와 병행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 BV — LPSCl | Ag–C | VGCF 점착일: 기존 LPSCl|NCM 워크플로를 재사용해도 같은 양을 재는가

**보고량 카드 §1–3 형식**으로 묻는다. 번들 검사가 아니라 *"무엇을 원하고, 어떤 식으로 재고,
이 계에서 그게 잘 정의되는가"* 다. **계산은 아직 0 이다.** 1저자 지시로 이 리뷰와 내부(Fable) 리뷰를 받은 뒤에
보고량 카드를 봉인하고 파이프라인을 건다.

- 계획·카드 초안: `kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md` (이 프롬프트의 근거 전부)
- 재사용 대상 워크플로: `kb/methodology/adhesion_energy.md` · `db/inputs/adhesion_templates/{surface_mqa_v5.yaml, adhesion_v6_anneal_test.py}` ·
  `tools/doping/run_cathode_interface.py` · `db/properties/adhesion.json`

## §0. 요청 (DEM 쪽 → 우리)

음극 적층 **LPSCl(Li₆PS₅Cl) | Ag–C 인터레이어 | VGCF** 의 박리 저항을 DEM(LIGGGHTS) 박리 시험으로 보려 한다. DEM 은 점착에너지를
입력으로 받을 뿐이라 **원자 스케일 점착일**을 DFT 로 달라는 요청이다. Ag–C 는 복합체라 구성 쌍으로 나눈다:
**P1 = LPSCl↔Ag(111) · Ag(111)↔흑연(0001)** · P2 = LPSCl↔탄소 · 흑연 층간(기준) · P3 = LiAg · 결함 흑연.
정확도 목표는 **자릿수**다 — 물리흡착 급(≲ 0.3 J/m²)인지 화학결합 급(≳ 1 J/m²)인지.

**요청 수정본**: 주값을 **기존 LPSCl|NCM 워크플로의 "isolated slab W_ad"** 에 맞추고 W_sep 도 같이 달라 ·
**v5 계면 제작 프로토콜과 SE 슬랩을 재사용** · **MLIP 값은 DFT 단일점으로 검증** ⇒ LPSCl|Ag 를 LPSCl|NCM 과 바로 나란히 비교.

## §1. 무엇을 원하나 (보고량)

기존 LPSCl|NCM 과 **같은 조작**으로 낸 LPSCl|Ag · Ag|흑연 의 분리일 **분포**(xy registry 시드별)를,
NCM 기준값 분포와 나란히 놓고 자릿수를 판정한다 — **DFT 단일점으로 검증된** 값으로.

**비교 기준값 (repo 실측)**: `adhesion.json` `adhesion_v5_crystalline_slab.xy_shift.comp1` —
20 seeds · **평균 1.153 · 표준편차 0.392 · 중앙값 0.962 · 범위 0.555–1.850 J/m²** ·
SE prim 2×2×3 (624원자 · 두께 30 Å) · NCM 7×7×1 · A 351 Å² · 변형 0.2 % (`cell_matching.Li6_v5_xyshift_FIX`). 계산기는 UMA.

## §2. 어떻게 재나 (제안)

```
W_sep(s)  = [E_sep(s) − E_int(s)] / A      # 워크플로 v5_working 과 같은 조작: 분리 +30 Å, 셀 +30 Å, 이완 없이 단일점
W_ad(s)   = [E_A^rel + E_B^rel − E_int(s)] / A   # 각 슬랩을 같은 셀·같은 변형에서 이완 — 워크플로에 없던 값
W^DFT     = 같은 식, 에너지만 PBE+D3(BJ) 단일점 (UMA 기하 위)   ·   W^noD3 = 같은 기하에서 D3 항을 뺀 값
UBER E(d) = 이완 계면을 강체로 0.2–0.5 Å 간격, 평형 + 8 Å
```

- **P1-a LPSCl↔Ag**: 재사용 SE 슬랩(측면 육방 20.13 Å) 위에 **Ag(111) 7×7 · 4층**(196원자) — Ag 변형 −0.46 %(a 4.086 Å) ·
  −0.80 %(4.10) · −2.23 %(PBE 4.16). 합계 ≈ **820원자**. v5 MQA → 이완 → 분리 단일점. **xy-shift 20 seeds** (기준과 같은 수).
- **P1-b Ag↔흑연**: 기존 워크플로 밖이다. (√3×√3)R30° Ag / 흑연 2×2 (−1.7 %) 류 작은 셀 · 시드 8.
- **DFT 검증**: PBE+D3(BJ) 단일점으로 E_int·E_sep — **P1-a 5 seeds + P1-b 4 seeds + NCM 기준값 5 seeds**.
- **반응성 사전검사**: MP 반응에너지 (LPSCl+Ag · LPSCl+LiAg · LPSCl+C · Ag+C) — 음이면 값의 이름을 "급격 계면·반응 전" 으로.
- ⛔ 출판 관례(paper #1)의 `W = WELLS_RAW − α·ΔW_strain` (α=1.0 · Li5.4 균일 0.44) 는 **넣지 않는다** — 실험 순위로 맞춘 항이고 Ag 에 대응물이 없다.

## §3. 잘 정의되는가 — 우리가 스스로 못 닫은 것

1. **"isolated slab W_ad" 는 조작상 W_sep 이다.** 정의 줄(`adhesion_energy.md` 7줄)은 isolated slab 인데, `v5_working`(141–159줄)은
   *"No relax after separation — single point only"* 이고, 247줄이 *"엄밀히는 무이완 분리라 work of separation 계열 (W_ad 의 상계)"* 라고 스스로 적었다.
2. **v5 인가 v6 인가 · UMA 판.** 수정본은 v5(`surface_mqa_v5.yaml`: `uma-s-1p2` · 800 K 표면 연화)를 쓰라 한다. 러너(`run_cathode_interface.py`)는
   v6(`uma-s-1p1` · NCM 고정 500 K)을 *"verified production"* 이라 부른다. `adhesion.json` 에는 UMA 판 문자열(`1p1`·`1p2`)이 **한 번도** 없다 → 기준값 20 seeds 가
   어느 판에서 나왔는지 **repo 안에서 확정할 수 없다.** 단 v6 은 절대값으로 쓸 수 없다는 것이 원장에 이미 있다(아래 7).
3. **변형 방향이 바뀐다.** NCM 워크플로는 SE 를 NCM 에 맞춰 늘렸다. 우리는 SE 슬랩을 그대로 두고 **Ag 를** 맞추려 한다.
4. **반응성 금속 + 800 K.** v5 의 800 K 표면 연화에서 Ag–S 결합·Ag 이동이 생길 수 있다. NCM 은 v6 에서 고정됐다.
5. **UMA 가 이 계에서 믿을 만한가.** UMA 는 진공 60 Å 에서 W 를 10배 과대로 냈다(`adhesion.json` `vacuum_sensitivity`). Ag–황화물 계면 검증 기록이 없다.
6. **워크플로 이력에 선별 흔적이 있다** — `adhesion.json` 527줄: *"v5 paper #1 결과 — 서버 lost, R²=0.9999 cross-family match는 user-curated (artificial selection)"*.
7. **"LPSCl|NCM 값" 이 하나가 아니다 — comp1|NCM 한 계면에 원장 숫자가 넷이고 자릿수가 다르다.**

   | 무엇 | comp1 | 근거 |
   |---|---|---|
   | 원장이 *"paper exp"* 로 부르는 기준 | 0.194 J/m² (comp1–5 = 0.180–0.316) | `tools/adhesion_v30u/alpha_sensitivity_FINAL.py` `PAPER` (mJ/m²) · `adhesion.json` 1369줄 |
   | **v5 xy-shift · UMA · 분리 단일점** (재사용하려는 기준값) | 중앙값 0.962 · 평균 1.153 | `adhesion.json` 165–205줄 |
   | paper #1 출판식 `WELLS_RAW − α·ΔW_strain` (α=1) | 0.075 (= 2.708 − 2.633) · comp2 −0.064 | `db/properties/alpha_sensitivity_FINAL.json` `uniform` α=1.0 |
   | v6 (`run_cathode_interface.py`) | 45–80 (5 seeds) | `adhesion.json` 1486–1498줄: *"100-1000x over … rigid separation creates artificial dangling-bond energy"* |

   v5 기준값은 "paper exp" 의 약 5배다. 요청서의 자릿수 판정(≲ 0.3 / ≳ 1)에 NCM 을 넣으면 **어느 숫자를 쓰느냐에 따라 등급이 바뀐다**.
   "paper exp" 의 측정 방식·출처는 repo 에서 확인하지 못했다 — `adhesion.json` 1498줄이 가리키는 Sundar 2025 의 litdb digest 에는 점착 값이 없다.
   원장은 paper #2 에서 v6 절대값 대신 **보정비**(`stage11 × Wad_comp1_paper1 / Wad_comp1_stage11`, Option A)를 채택한 적이 있다 — **같은 NCM 계 안에서**였다.

## §4. 질문

- **Q1 (정의)**: 워크플로 값을 **W_sep** 으로 부르고, 이완 슬랩 **W_ad** 를 따로 내는 것이 맞나? DEM 입력의 **헤드라인**은 둘 중 무엇이어야 하나 (NCM 과의 비교성 vs 열역학적 의미)?
- **Q2 (기준값 판)**: 기준값의 UMA 판·프로토콜(v5/v6)을 repo 로 확정할 수 없으면, **Ag 를 돌리기 전에 NCM 기준값을 우리가 고른 판으로 다시 내야** 하나 (몇 seeds)? 아니면 옛 값을 "판 미상" 으로 두고 비교를 포기해야 하나?
- **Q3 (변형 방향)**: SE 슬랩을 그대로 두고 Ag 를 −0.5 ~ −2.2 % 변형하는 것이 비교성을 해치나? 절차 동일성을 위해 SE 를 늘려야 하나?
- **Q4 (MQA)**: Ag 면을 NCM 처럼 **고정**하고 SE 만 풀어야 하나, v5 그대로 800 K 연화를 해야 하나? 둘 다 돌려서 보고하는 것이 맞나?
- **Q5 (DFT 검증)**: UMA 기하 위 DFT 단일점(E_int·E_sep)이 W 의 검증으로 **유효한가**? 5 seeds 로 충분한가? **결과 보기 전에 봉인할 허용 폭**(예: 시드별 |W^DFT − W^UMA| ≤ 0.1 J/m² 또는 20 %)은 무엇이 적절하고, 넘으면 DFT 값을 쓰나 UMA 값을 버리나?
- **Q6 (D3 끔)**: "같은 기하에서 D3 항을 뺀 값" 을 요청서의 "D3 끈 값" 으로 보고해도 되나? 물리흡착 계면은 D3 없이 이완하면 떨어져 나가 값이 정의되지 않는다.
- **Q7 (반응성)**: MP 반응에너지 사전검사를 게이트로 쓸 때 문턱은? 반응이 유리하면 급격 계면 W 를 **보고는 하되 이름을 붙이는** 우리 처리가 충분한가?
- **Q8 (비교 규칙)**: 20 seeds 분포끼리의 비교를 무엇으로 하나 (중앙값·범위 겹침·순위검정)? "분포 전체가 0.3–1 을 걸치면 판정 보류" 는 적절한가?
- **Q9 (Ag↔흑연)**: 워크플로 밖 계면에서 "같은 규약" 을 지키는 최소 조건은 무엇인가 (시드 수 · MQA 유무 · 분리 조작)?
- **Q10 (DEM 에 넘길 절대값 — §3.7)**: 셋 중 무엇이 방어 가능한가 —
  (a) 우리 프로토콜의 절대값 그대로 (UMA 또는 DFT 단일점) ·
  (b) 같은 프로토콜의 **Ag/NCM 비만** 넘기고 NCM 절대 기준은 DEM 쪽이 고른다 ·
  (c) 비 × "paper exp" NCM 값 (원장 paper #2 Option A 방식).
  (c) 는 **금속(Ag)–황화물과 산화물(NCM)–황화물 사이에 프로토콜 오차가 같은 배수**라는 가정이다. 그 가정을 이 계에서 시험할 방법이 있나 (예: DFT 단일점의 W^DFT/W^UMA 비를 두 계에서 비교)?
  그리고 "paper exp" 처럼 출처를 repo 에서 확인 못 한 값을 기준으로 **써도 되나**?

## §5. 받고 싶은 것
GO / GO-with-fixes / NO-GO 와, Q1–Q10 각각에 대한 **결정 가능한 답**. 봉인할 문턱(Q5)은 숫자로.
