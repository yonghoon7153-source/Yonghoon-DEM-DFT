---
title: "리뷰 BV 프롬프트 — LPSCl | Ag–C | VGCF 점착일: 기존 LPSCl|NCM 워크플로를 재사용해도 같은 양을 재는가 (v2)"
date: 2026-09-23
updated: 2026-09-23
tags: [review, codex, adhesion, wad, interface, lpscl, silver, graphite, estimand, uma, dft-verification]
status: 발송됨 · 회신 수령 (NO-GO) → codex_BV_reply_wad_lpscl_ag_c_vgcf_2026_09_23.md
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 BV — LPSCl | Ag–C | VGCF 점착일: 기존 LPSCl|NCM 워크플로를 재사용해도 같은 양을 재는가

> **이 판(v2)을 보낸다.** 초판(커밋 `b27dd3b8e`)은 보내기 전에 내부 리뷰에서 세 곳이 틀린 것으로 드러났다 —
> ① 기준값을 낸 방법(800 K MQA 로 읽었는데 **이완만**이었다) ② 계면 셀(육방으로 읽었는데 SE 는 **정방**) ③ 실험값 단위(**aJ** 를 J/m² 로 옮겼다).

**보고량 카드 §1–3 형식**으로 묻는다. 번들 검사가 아니라 *"무엇을 원하고, 어떤 식으로 재고, 이 계에서 그게 잘 정의되는가"* 다.
**계산은 아직 0 이다.** 1저자 지시로 이 리뷰와 내부 리뷰를 받은 뒤에 카드를 봉인하고 파이프라인을 건다.

- 계획·카드 초안 **v2**: `kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md` (이 프롬프트의 근거 전부)
- 내부 리뷰(Fable, **NO-GO** — v1 대상): `kb/reviews/internal_review_wad_agc_fable_2026_09_23.md` — P0 4건을 우리가 원문에 대 확인했고 v2 에 반영했다.
  **내부 리뷰의 제안값(문턱·절차)에 동의하지 않으면 그렇게 말해 달라** — 그걸 그대로 받으려고 보내는 게 아니다.
- 재사용 대상 워크플로 정본: `kb/results/adhesion_final.md` · `kb/methodology/adhesion_energy.md` · `kb/methodology/adhesion_methods_comparison.md` ·
  `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` · `tools/doping/run_cathode_interface.py` · `db/properties/adhesion.json` · `webapp/fairchem.py`

## §0. 요청 (DEM 쪽 → 우리)

음극 적층 **LPSCl(Li₆PS₅Cl) | Ag–C 인터레이어 | VGCF** 의 박리 저항을 DEM(LIGGGHTS) 박리 시험으로 보려 한다. DEM 은 점착일을 입력으로 받을 뿐이라
**원자 스케일 점착일**을 DFT 로 달라는 요청이다. Ag–C 는 복합체라 구성 쌍으로 나눈다: **P1 = LPSCl↔Ag(111) · Ag(111)↔흑연(0001)** ·
P2 = LPSCl↔탄소 · 흑연 층간 · P3 = LiAg · 결함 흑연. 정확도 목표는 **자릿수** — 물리흡착 급(≲ 0.3 J/m²)인지 화학결합 급(≳ 1 J/m²)인지.

**요청 수정본**: 주값을 **기존 LPSCl|NCM 워크플로의 "isolated slab W_ad"** 에 맞추고 W_sep 도 같이 · **v5 계면 제작 프로토콜과 SE 슬랩 재사용** ·
**MLIP 값은 DFT 단일점으로 검증** ⇒ LPSCl|Ag 를 LPSCl|NCM 과 바로 나란히 비교.

## §1. 무엇을 원하나 (보고량)

**같은 조작 · 같은 SE 셀 규약 · 같은 계산기**로 낸 LPSCl|Ag 와 (다시 낸) LPSCl|NCM 의 **W 분포**(xy registry 시드별)를 나란히 놓고,
그 **비**와 자릿수 급을 — 같은 기하의 **DFT(PBE)로 검증된** 짝으로 — 말한다. 헤드라인 절대값은 DFT(PBE+D3) 에서만.

## §2. 어떻게 재나 (v2 제안)

```
W_sep(s)  = [E_sep(s) − E_int(s)] / A            # 분리 +30 Å · 셀 +30 Å · 이완 없음 (워크플로와 같은 조작)
W_ad(s)   = [E_A^rel + E_B^rel − E_int(s)] / A   # 각 슬랩을 같은 셀에서 이완 — 워크플로에 없던 값 (항상 W_ad ≤ W_sep)
W^PBE     = 같은 식 · PBE(+U: NCM 쪽) 단일점 · UMA 기하 위 · D3 없음      ← UMA 의 검증 짝
W^PBE+D3  = W^PBE + ΔD3(같은 기하 · D3(BJ) 가산항)                        ← 헤드라인 후보
UBER E(d) = 이완 계면 강체 z-스캔, 평형 + 8 Å
```

- **워크플로에서 재사용하는 것 = 조작**: xy-shift 시드 · **LBFGS 이완만 (MQA 없음)** · 분리 단일점 · 진공 30 Å · 계산기 `uma-s-1p1`/omat (repo 핀).
- **재사용하지 않는 것 = 기준값 숫자** — 셀 문제(§3-2) · 스크립트·슬랩 유실 · repo 규율 *"버전을 올리면 옛 값과 새 값을 병합하지 말고 전부 다시 뽑는다"*. ⇒ NCM 기준값을 같은 파이프라인에서 다시 낸다 (시드 42–61 사전 고정).
- **셀** — 전부 SE 고유 **정방 20.11 × 20.11 Å (A 404 Å²)** 위: SE comp1 관용 입방셀 2×2×3 (624원자 · 30 Å · face 'A') +
  기준 **LiNiO₂(001) 1L 직사각 7×4** (NCM −0.18 / +0.86 %, 224원자) · **Ag(111) 직사각 7×4 × 4층** (Ag −0.57 / +0.46 % @ a 4.086 · −2.33 / −1.32 % @ PBE 4.16, 224원자). 둘 다 848원자.
- **P1-b Ag↔흑연 · 흑연 층간**: 물리흡착 짝이라 UMA(분산 없음)로는 기하가 정의되지 않는다 → **DFT+D3 로 직접**, E(d) 스캔 포함. 흑연 층간 = DFT 세팅 대조 잡.
- **첫 잡 = 불변성 대조**: 같은 슬랩을 진공 20/30/40/60 Å 에 놓고 E 가 1 meV/atom 안에서 같은지 · UBER E(8 Å) ≈ E_sep(30 Å) (0.02 J/m² 안) · 시드별 W_ad ≤ W_sep. 어기면 정지.
- **DFT**: 프로브 1건(시드 1개: E_int + 분리 슬랩 둘)으로 시간 실측 → 적응형 2 → 5 seeds · **NCM 을 Ag 보다 먼저**. repo 견적은 계면 1건 ~48 h KISTI.
- **반응성**: 시드별 관측량 사전 선언 — Ag–S < 2.5 Å 개수/Å² (접촉) · SE 안 Ag / Ag 안 S·Li (반응 → 급격 계면 통계에서 빼고 따로) · P–S 4배위. MP 벌크 반응에너지는 참고용.
- ⛔ 출판 관례 `W = WELLS_RAW − α·ΔW_strain` (α = 1) 는 넣지 않는다 — 실험 순위로 맞춘 항이고 Ag 대응물이 없다.

## §3. 잘 정의되는가 — 우리가 스스로 못 닫은 것 (repo 실측)

1. **"isolated slab W_ad" 는 조작상 W_sep 이다.** 정의 줄(`adhesion_energy.md`)은 isolated slab 인데 `v5_working` 은 *"No relax after separation — single point only"* 이고,
   같은 문서가 *"엄밀히는 무이완 분리라 work of separation 계열 (W_ad 의 상계)"* 라고 스스로 적었다.
2. **기준 계면의 셀이 맞지 않는다 (추정 — 원본 빌더 유실).** SE 는 입방 a = 10.055 Å → 2×2 = **정방 20.11 Å · 404 Å²** 인데, 기록된 계면 면적은 **351.5 Å²** = LiNiO₂ 육방 7×7 (20.146 Å · 120°).
   남은 빌더(`adhesion_v6_anneal_test.py` `build_interface`)는 `se_frac = se_cart @ inv(ncm_cell)` → xy 이동 → `% 1.0` → `@ ncm_cell` — 주석은 *"applies xy strain"* 인데 **좌표가 안 변하는 wrap** 이다.
   원장은 SE 밀도를 *"1.78 at/Å²"* (= 624/351.5, 정방이면 1.54) 로 썼고, *"d_min=1.0-1.1 Å … possible cubic SE + hex NCM PBC artifact"* 라고 스스로 의심했다.
3. **UMA 진공 민감도가 진단되지 않았다.** *"진공 60 Å 에서 W 10배"* · *"E_ncm = +248 eV"* 기록 뒤 *"진공 30 Å + 분리 시 셀 확장 + 분리 후 무이완"* 세 조건이 **우회 규칙**으로 굳었다. 국소 MLIP 의 에너지는 수용장 밖 진공에 의존할 수 없어야 한다.
4. **NCM 기준은 1L LiNiO₂ 시트다.** 두께: 1L 1.153 → 2L NCM811 ~2.0 (+74 %) → 5L 2.674 ± 0.882 (12/20 유효) — DEM 의 두께수렴 기준(ΔW < 0.05)을 못 넘는다.
   DFT 쪽은 +U · 스핀 · 자기 basin 이 여럿이다 (우리가 SDCP 흡착에너지를 여덟 번 반려당한 종류).
5. **comp1|NCM 에 원장 숫자가 여럿이고 선별 이력이 있다.** 20 seeds 1.153 (평균) · 100 seeds 1.151 · **출판 표 1.277 = 20 중 5 seeds 를 "to match experimental ratios" 로 고른 것** ·
   차트는 *"outliers >4.0 removed"* · 출판식 0.075 · v6 45–80 (원장 자진단 *"artificial dangling-bond energy"*). 이 계열에서 UMA 원시 우물의 순위가 실험과 **역전**된 기록도 있다 (R −0.76).
6. **실험 기준은 AFM aJ 다 (J/m² 아님).** comp1–5 = 180–316 **aJ**. 방법론 문서는 *"r≈10nm 접촉 πr² 환산 1 J/m² ↔ ~314 aJ; 절대 스케일은 순위·상관으로만"* 이라 했는데,
   원장 일부가 같은 숫자를 *"0.18–0.32 J/m²"* · *"Sundar 2025: 0.2–0.4 J/m²"* 로 적었다 (오독 — 정오표를 달았다).
7. **repo 금지 규칙과 요청이 부딪힌다.** `webapp/fairchem.py` `OUR_BANS`: *"MLIP 절대값을 인용하지 않는다 (σ · W_ad) — 같은 프로토콜 안의 순서·비율만, 비율도 멀티시드로"*. DEM 은 **절대값(J/m²)** 을 원한다.

## §4. 질문

- **Q1 (헤드라인)**: DEM 접촉법칙(JKR · DMT · cohesive zone)이 받는 것은 열역학적 **W_ad(이완)** 이고 W_sep 은 상계라는 내부 리뷰 판단에 동의하나? 둘 다 내되 **헤드라인은 무엇**이어야 하나?
- **Q2 (기준값 셀)**: §3-2 의 빌더로 정방 SE 를 육방 셀에 wrap 한 계면에서 나온 W 는 **무엇을 잰 것**인가? 옛 숫자를 "레거시 프로토콜" 로라도 남겨 둘 이유가 있나, 아니면 **정방 셀 재계산**(NCM 직사각 7×4)으로 완전히 대체하는 게 맞나?
- **Q3 (불변성)**: §3-3 을 어떻게 해석하나? 우리 대조 잡(진공 20/30/40/60 Å ≤ 1 meV/atom · UBER E(8 Å) vs E_sep ≤ 0.02 J/m² · W_ad ≤ W_sep)이 **충분하고 필요한가**? 빠진 것은?
- **Q4 (검증 짝)**: UMA(omat = 분산 없는 PBE/PBE+U 기준계) ↔ **W^PBE(D3 없음)** 를 같은 기하에서 비교하는 것이 맞나? **UMA 기하 위 DFT 단일점**이 W 의 검증으로 유효한가 — DFT 힘(그 기하에서의 잔류 힘)을 추가 게이트로 둬야 하나?
- **Q5 (문턱 — 숫자로)**: 내부 리뷰 제안 — 시드별 |W^PBE − W^UMA| ≤ **max(0.15 J/m², 25 %)** **그리고** 급 일치 **그리고** 부호 일치, 실패 시 **DFT 값이 보고값**·UMA 는 기하 표본기로 격하, 적응형 2 → 5 seeds. 받나, 고치나?
- **Q6 (NCM 상태선택)**: LiNiO₂ 1L 의 DFT 기준을 잘 정의하려면 어떤 **상태선택 규칙**이 필요한가 (U 값 · 스핀 초기화 · 강자성 고정 vs N 개 초기화 중 최저)? NCM 검증을 **Ag 보다 먼저** 두고 그게 실패하면 비교 전체를 멈추는 순서가 맞나?
- **Q7 (두께)**: 1L 기준값을 DEM 의 ΔW < 0.05 기준 아래에서 **"1L · 두께 미수렴" 라벨**로만 써도 되나, 아니면 3L 이상이 **필수**인가?
- **Q8 (반응성)**: §2 의 시드별 관측량(Ag–S < 2.5 Å/Å² · SE 안 Ag · Ag 안 S·Li · P–S 4배위)을 **상태선택 정책**으로 쓰는 것이 충분한가? 문턱 숫자는?
- **Q9 (DEM 에 넘길 것)**: §3-7 아래에서 방어 가능한 것은 — (a) **DFT 값** (PBE+D3 헤드라인 · PBE 짝) · (b) **같은 프로토콜의 Ag/NCM 비**만 · (c) 비 × 실험 NCM (실험이 aJ 라 접촉 반경 가정 필요)?
  그리고 **"UMA 기하 위 DFT 단일점"** 은 금지 규칙의 "MLIP 절대값" 에 걸리나?
- **Q10 (물리흡착 짝)**: Ag↔흑연 · 흑연 층간을 DFT+D3 로 직접 갈 때 최소 규약은 (registry 수 · 이완 vs 강체 E(d) · k-점)? 흑연 층간 대조 잡의 **기준값과 허용 폭**은?
- **Q11 (분포 비교)**: 중앙값 + IQR · Mann–Whitney · 시드 42–61 사전 고정 · 제외는 사전 선언 게이트(LBFGS 미수렴 · 반응 플래그 · PS₄ 무결성)만 — 적절한가?
  시드 분포가 0.3–1 J/m² 를 걸치면 **급 판정 보류**로 두는 규칙은?

## §5. 받고 싶은 것
GO / GO-with-fixes / NO-GO 와, Q1–Q11 각각에 대한 **결정 가능한 답**. 문턱(Q5 · Q8 · Q10)은 숫자로.
