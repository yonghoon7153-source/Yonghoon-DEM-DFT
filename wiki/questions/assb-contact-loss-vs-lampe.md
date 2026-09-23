---
title: ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가
description: "In solid-state cells (Li-In / Li metal / anode-free), does OCV fitting separate true positive-electrode active material loss from contact/percolation loss"
created: 2026-09-16
updated: 2026-09-23
type: research-question
tags: [battery, degradation, research, assb]
sources: [raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md, raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md, raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md, raw/papers/illig2012_charge-transfer-contact-resistance-lfp-drt-ecm.md, raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md, raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md, raw/papers/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer.md, raw/papers/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell.md, raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md, raw/papers/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb.md, raw/papers/jin2015_lithium-silicide-anode-electrode-design-assb.md, raw/papers/fukunishi2023_graphite-three-electrode-impedance-cyclability.md, raw/papers/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential.md, raw/papers/nam2018_three-electrode-assb-failure-modes-li-in-depletion.md, raw/papers/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/thelen2024_probabilistic-ml-battery-health-review.md, raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md, raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/li2026_safety-aware-bms-active-intelligence.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/rahman2024_sbms-rul-solid-state-batteries.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md, raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md, raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/bicer2025_ssb-chemistry-bms-thermal-assembly-critical-review.md, raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md, raw/papers/liang2026_pulse-excitation-active-bms-comment.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: user-original
status: open
feedsInto: "bms-balancing/docs/ASSB_TRANSFER_NOTE.md — 그리고 그것이 새 모델 요구서의 ASSB 판으로 갈 때"
---

# ASSB 에서 OCV 적합이 LAM_PE 와 접촉 손실을 가를 수 있는가

> **ASSB 섹션의 닻이다.** 이 주제의 논문은 `assb` 태그를 달고 여기로 링크한다.
> 액체셀 계열(현재 `raw/papers/` 20 편)과 **섞지 않는다** — 음극 축이 다르다.
>
> ⚠ **보류 항목이다** (2026-09-16 사용자 결정): 지금 프로젝트가 끝난 뒤에 착수한다.
> 지금 하는 일은 **자료를 모으고 물음을 벼려 두는 것**까지다.

## 질문

전고체전지의 음극은 **Li-In 합금 · Li 금속 · 무음극**이고, 셋 다 작동 구간에서
**OCP 가 평탄**하다. 그러면 완전지 OCV 는 사실상 양극 곡선 하나가 늘어나고 밀린
것이다. 여기서:

> 복합양극의 **접촉 손실**(활물질이 고체전해질과 닿지 않게 됨)은 **용량이 준 것처럼**
> 보인다 — 물질은 그대로인데. **OCV 적합이 이것을 진짜 `LAM_PE` 와 가를 수 있는가?**

## 왜 이 물음인가 — 액체셀에서 막힌 자리가 여기서는 열릴 수 있다

액체셀 갈래(`bms-balancing/`)가 도달한 결론은 **"LAM 분할은 점추정으로 보고할 수
없고 폭과 함께 보고해야 한다"** 였고, 더 못 간 이유가 **measured 라벨이 없다**는
것이었다 (`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5 · §8-6).

ASSB 의 이 물음은 다르다 — **접촉 수·퍼콜레이션은 DEM 이 독립으로 준다.**
이 모노레포에 이미 DEM/MPM 계열이 있다(타 브랜치 소유, `dem-mpm` 태그).
그것이 **OCV 적합이 못 보는 바로 그 양**이므로, 액체셀에 없던 **독립 라벨**이 될 수
있다. 이것이 이 물음을 먼저 적어 두는 이유다.

## 지금까지 아는 것 — 실측 하나

`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 (2026-09-16, 합성):
현행 `Objective` 에 **평탄 상대극**을 끼우고(코드 수정 0) 축별 민감도를 쟀다.

| 흔든 축 | `Δ obj` |
|---|---:|
| `a_PE` | **+2.204e-01** |
| `b_PE` | **+4.399e-01** |
| `a_NE` | **+0.000e+00** |
| `b_NE` | **+0.000e+00** |
| `γ_Si` | **+0.000e+00** |

→ **5 → 3 파라미터 붕괴.** 액체셀 최악의 축퇴([[fitting-degeneracy]] 의 `LAM_NE ↔ γ_Si`)는
ASSB 에서 **개념 자체가 없어진다.** 대신 싸움이 **`LAM_PE ↔ 접촉 손실` 한 자리로 모인다.**

폭을 재는 기계([[near-optimal-set-width-measurement]])는 **그대로 쓴다** — 화학에
무관하게 "답이 하나로 정해지는가" 를 재기 때문이다. 파라미터가 3 개로 줄면 오히려
싼 문제가 된다.

⚠ 이것은 **우리 합성 양극 곡선에 평탄 상대극을 붙인 것**이지 ASSB 실자료가 아니다.

## 아직 모르는 것

1. **접촉 손실을 모델에 어떤 형태로 넣나** — 용량 축 스케일인가, 별도 칸인가,
   유효 활물질 분율인가. **이것이 정해져야 구분 시험이 설계된다.**
   → **형태는 정해졌다** (1호: 용량 축에 곱해지는 기하 인자 `θ_AM`).
   → **항이 하나 더 있다** (2호: 율 의존 인자 `η(i)`, [[assb-apparent-capacity-decomposition]]).
   → **남은 것은 시간축** (`θ(N)`) — `assb` **3/3 편이 안 줬다**.
   ⚠ 그리고 2호의 `C_norm` 이 `θ_AM` 을 포함하는지 아닌지 **원문에 안 적혀 있다**
   (2호 digest G1) — 3항 분해를 수치로 쓰기 전에 풀어야 할 좌표.
   → **3호(Liu 2024)가 시간축 대신 준 것은 `θ` 를 떨어뜨릴 구동력**이다: 계면
   **최대주응력**(GPa). ★ **그러나 좌표 변환이 안 된다** — 응력(Pa) → 분리 분율(무차원)
   에는 파괴 판정 규칙이 필요한데 **3호에 파괴·디본딩 모형이 없다**
   (`[인쇄]` "the current model does not explicitly account for mechanical fracture").
   → **1–3 호의 공백은 같은 한 조각이다: cohesive zone / phase-field damage.**
   → ★ **4호(Shi 2020)가 모형 대신 실측으로 시간축을 줬다** — void 부피분율이 사이클
   **0/10/50** 에 **2.87 → 3.23 → 9.50 vol%**. 모양은 **부드럽지 않고 계단**이다
   (`[인쇄]` "does **not progress gradually** … the majority … occurs at **later cycles
   and over a short period**"). ⚠ 3 점 · 각 점 **다른 셀** · 반복 0 이고, 그 "계단" 이
   **검출 한계의 산물일 수 있다** (같은 논문이 `[인쇄]` "very small microfractures …
   **undetectable by the tomography**").
   ⚠⚠ **그리고 4호의 양은 `θ` 가 아니다** — **접촉 면적분율**(10.4 %)이고, 그것을
   곱셈 인자 자리에 넣으면 **자기 압력 실험과 6 배 어긋난다**(아래 Evidence).
   → ★ **18호(Fukunishi 2023)가 접촉 면적을 처음으로 "측정된 양" 으로 만든다** —
   `[인쇄]` **Image-J 로 단면 SEM 에서 SE|활물질 접촉 면적**, 값은 **입자 크기 두 시료의
   비 2.0**(기하 계산 2.4 와 대조). ⚠ **절대 분율·오차·임계값이 없고**, 원자료 두 장은
   **배율·가속전압이 다르다**(캡션 "×2500" ↔ 스탬프 2500x/1000x). ⚠⚠ **그리고 노화
   축의 `θ(N)` 은 또 0 이다 — 이번에는 도구(Image-J)와 시편(Fig. 6·7)이 둘 다 같은
   지면에 있는데도.** ⇒ `θ(N)` 을 안 준 편이 **`assb` 18/18** 이다.
   → ★★★★ **다만 18호는 `θ(N)` 을 다른 통로로 준다** — **적합된 용량 파라미터**다.
   `[재현]` `C ≡ τ/R` 의 노화 전후 비가 **LPSI 0.37 · LPSCl 1.07** ⇒ **LPSI 는 유효 면적이
   ≈2.7 배 줄고 LPSCl 은 안 줄었다**(§18호 절 2). **이것이 이 카드가 지금까지 본 `θ(N)` 에
   가장 가까운 숫자**이고, ⚠ 측정이 아니라 **지면 두 열의 조합**이다.
2. **Li-In 기준 전위가 얼마나 안정한가.** 평탄한 것은 두 상 공존 영역 안에서만이다.
   벗어나면 기준이 이동하고 그것은 전체 곡선의 **밀기** — **`LLI` 와 같은 모양**이다.
   → ★★★★ **17호(Yanev 2024)가 이 항목에 답한다 — 이 계보에서 처음으로.**
   전용 페이지를 만들었다: [[assb-li-in-reference-potential-window]].
   요지 셋: **① 열역학 평탄 폭은 `[인쇄]` ±10 mV 안이고 그보다 좁게 잰 편이 없다**
   (그 ±10 mV 조차 `[재현]` CE–RE 옴 강하 ≈9.1 mV 와 구별되지 않는다) ·
   **② Li-rich 로 벗어나면 `[인쇄]` −0.2 V**(충전 중, 컷오프가 4.3 → 4.1 V) ·
   **③ 분리막 쪽 LiIn 이 고갈되면 `[인쇄]` +0.68 … +0.78 V**(방전 중) 이고
   `[재현]` **그 구간의 옴 몫은 0.2 %** 다(전류가 종료 기준 0.02 C 까지 떨어진 뒤에도
   ≈1.35 V 에 6 h 이상 머문다) ⇒ **과전압이 아니다.**
   ★★★★ 대표 숫자: **같은 프로토콜 · 전류 ≈0 · 같은 공칭 조성(40 at% Li) 의 두 Li-In
   음극이 `E_CE` = 0.61 ↔ 1.35 V, ≈0.74 V 갈린다. 차이는 제조법뿐이다.**
   ⚠ **16호(0.47–0.58 V)와 절대값이 다르고 둘 다 자기 기준극을 검증하지 않았다.**
   ⚠ **`E_CE(N)`(사이클)도 `E_CE(P)`(압력)도 여전히 0 편이다.**
   → ★★★ **18호(Fukunishi 2023)가 경계 조건의 윤곽을 준다 — 반대편 끝의 표본으로.**
   `[도표]` 두 전해질계 모두 **0.1 C 전 사이클에서 Li-In 이 완전 평탄(≈0.60 V)** 이고,
   `[재현]` 그 이유가 계산된다: **`x_Li` 37.7 → 40.0 at%**(2상역 한복판),
   **Li 재고 / 이동 전하 = 9.5 배**, **전류밀도 0.054 mA cm⁻²** = 17호 0.1 C 의 **1/5** ·
   17호 CA 의 **1/300**. ⇒ **17호와 모순이 아니다** — 17호는 (ㄴ)(ㄷ)을 깬 표본이고
   18호는 세 조건을 다 만족하는 표본이다: **(ㄱ) 조성이 2상역 안 · (ㄴ) Li 재고가 이동
   전하의 한 자릿수 이상 · (ㄷ) 전류밀도 ≲0.1 mA cm⁻².**
   ⚠ **셋 중 무엇이 지배적인지 가른 실험은 0 편.**
   → ★★ **그리고 18호가 "기준을 Li-In 에서 빼는 길" 을 보여 준다** — 제 3 물질
   기준극(**R-LTO 메시**, 전류가 흐르지 않는 3전극 전위 측정)을 쓰면 **Li-In 의 리튬화도
   변화가 기준 축에서 사라진다**. ⚠ **대신 가정이 옮겨간다**: `[인쇄]` "**Assuming** that
   the potential of the R-LTO reference electrode is **1.55 V**", 자기 셀 검증 0,
   안정성 근거가 `[인쇄]` **K–K 잔차**라는 **범주 오류**.
   → ★ **4호가 답이 아니라 경고를 준다**: 실험 논문이 `[인쇄]` "1.4–3.7 V vs In
   (2–4.3 V vs Li/Li⁺)" 로 **오프셋 0.6 V 를 고정 가정하고 검토하지 않는다**
   (`indium` 0 회). ⚠ **그런데 같은 논문의 EIS 에서 음극 쪽 `R_LF` 가
   `[도표]` ≈0.7 → ≈110 kΩ (≈157 배)로 자라고, 50 사이클에 전체 저항의 ≈93 % 다.**
   → **기준극이 가장 크게 변하는 계면인데 기준 전위를 불변으로 놓는다.**
   완전지 OCV 를 양극 곡선으로 읽는 우리 계획이 딛는 바로 그 가정이다.
3. **무음극의 dead Li 와 SEI Li** 는 OCV 에 똑같이 들어온다. 가르는 관측이 있나.
   → ★ **5호(Doux 2020)가 절반 답했다.** 같은 셀에서 **토모그래피(형태) + XRD(화학)**
   두 채널을 돌리면 **SEI 는 상으로 잡힌다** (Li₂S · LiCl · P₄ · Li₃P₇, Mo Kα 투과).
   ⚠ **dead Li 는 잡히지 않는다** — `[인쇄]` "lithium metal dendrites are **not
   directly detected by X-ray diffraction** due to the low amounts and low scattering
   efficiency of lithium metal", 그리고 토모그래피는 **밀도 대비**뿐이라
   Li(0.534 g cm⁻³)와 균열/공극(0)이 갈리지 않는다.
   ⚠⚠ 그 결과 같은 논문이 **같은 저밀도 대비를 Fig. 5b 에서는 "dendrite", Fig. S6
   에서는 "severe cracking"** 이라고 부른다 (5호 digest D6).
   `[해석]` **SEI Li 는 정량 가능한 길이 보이고, dead Li 는 아직 관측 수단이 없다.**
   → ★★ **6호(Lee 2020)가 이 계보 첫 무음극 셀로 채널 둘을 더했다** —
   ② **EELS Li 맵**(Li 특이 채널; `[도표]` **방전 후·100 사이클 후에도 Ag–C 층 안에
   Li 망이 남는다**, pristine 엔 없다) ③ **XRD 의 Li₉Ag₄**(Li 를 담은 상을 동정한
   첫 사례, 가역). **그래도 dead Li 는 못 가른다** — EELS 가 dead Li / LiC_x / SEI /
   합금 잔여를 구분하지 않는다. 단면 SEM 은 `[재현]` **1 µm = 용량의 3.0 %** 라
   사이클당 손실(0.011 %)보다 **≈270 배 거칠다**.
   ⚠⚠ 그리고 6호는 `[인쇄]` "the discharge capacity decays due to the generation of
   **isolated lithium**" 이라고 **기구로 지목하면서 한 번도 재지 않는다.**
   → ★★★ **대신 6호가 준 것은 "무음극에서 `LLI` 를 무엇으로 세는가" 의 답이다**:
   **전하 수지 둘뿐**(첫 사이클 비가역분 · 사이클당 CE)이고 **그 둘이 10 배 어긋난다.**
   자세히는 [[anode-free-li-inventory-accounting]].
   → ★★★ **7호(Spencer-Jolly 2023)가 처음으로 dead Li 를 숫자로 만들 재료를 준다 —
   그리고 그 뺄셈을 하지 않는다.** 같은 셀의 `[도표]` **충전 67.6 h · 방전 35.0 h**
   (둘 다 30 µA cm⁻²) → `[재현]` **2.03 ↔ 1.05 mAh cm⁻², 첫 사이클 효율 ≈52 %**.
   여기서 `[도표]` 계면상(SEI) 구간 **0.19** 를 빼면 **≈0.79 mAh cm⁻² (통과 전하의
   39 %)** 가 남는다. **방전 종료 회절에 `[인쇄]` "only graphite and Ag" 만 남으므로
   층 안에 저장된 Li 는 전부 돌아왔고**, 남는 통로는 **추가 SEI 와 고립 Li 금속**뿐이다.
   ⚠ **그 둘은 여전히 안 갈린다** — 5·6호의 한계가 그대로다.
   ⚠ 모집단: **반쪽전지 · 상온 · ≈C/68 · 1 사이클 · 층 용량의 4 배 과충전**.
   `LLI(N)` 로 옮길 수 없다. 자세히는 [[anode-free-li-inventory-accounting]] ·
   [[ag-c-interlayer-lithium-phase-path]].
4. **압력**이 상태변수다 (액체셀에 없던 것). 열화 모드가 압력 의존이면 "상태" 의
   정의부터 다시 해야 한다.
   ⚠ **`assb` 1–3 호가 `pressure` 0 회였다.** 3호(Liu 2024)는 계면 접촉 역학을 **본체로**
   다루면서도 스택 압력을 쓰지 않는다 — 대신 전해질 **탄성률·항복강도**가 그 자리를
   차지한다. `[해석]` 둘은 다른 축이다(재료 물성 vs 외부 경계조건).
   → ✅ **4호가 깼다. 그리고 압력이 상태변수를 넘어 `분리 연산자`가 된다** —
   50 사이클 후 **300 MPa 재가압**으로 용량이 `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹**.
   `[해석]` **율이 `η(i)` 를 지우듯, 압력이 `θ_AM` 을 (부분적으로) 되돌린다.**
   자세히는 [[assb-pressure-reapplication-separation-test]].
   ⚠ **남은 것**: 압력 **스윕**이 여전히 0 편이다 (4호도 각 1 점). 그리고 4호의
   사이클 압력 **~2 MPa 는 낮은 편**이라 이 셀의 급락이 저압의 산물일 가능성을
   논문이 검토하지 않는다.
   → ✅✅ **5호(Doux 2020)가 스윕을 줬다. 그리고 압력이 "좋은 방향으로만" 가는
   변수가 아니라는 것을 보인다** — [[assb-stack-pressure-operating-window]].
   `[인쇄]` **75 MPa 도금 전 기계적 단락 · 25 MPa 48 h · 20 MPa 190 h ·
   15 MPa 272 h · 10 MPa 474 h · 5 MPa >1000 h 무단락.**
   그리고 임피던스는 `[인쇄]` **1 MPa >500 Ω → 25 MPa 32 Ω**.
   ★ **세 가지가 우리 계획에 바로 걸린다**:
   ① **상한**(4호의 300 MPa 는 이 상한의 4 배) ②  **이력**(처녀 5 MPa 110 Ω ↔
   25 MPa 를 찍고 내려온 5 MPa 50 Ω → `θ(P)` 는 경로 의존 상태다)
   ③ **`η = η(i, P)`** (과전압 자체가 압력 함수 → 율 연산자와 압력 연산자가 직교하지 않는다).
   ⚠ **여전히 없는 것**: **압력 → 용량** 곡선. `assb` **5/5 편**이 안 줬다.
   → ✅✅✅ **6호(Lee 2020)가 압력 → 용량을 준다. 그리고 축이 하나가 아님을 보인다.**
   이 셀에는 압력이 **둘**이다: **제작 490 MPa (온간 등방압 WIP)** 와 **운전 2 MPa (지그)**.
   `[도표]` 운전 압력 **2/3/4 MPa** 에서 율특성이 **94.0 / 95.1 / 95.5 %** 이고
   300 사이클 유지율 곡선 셋이 **겹친다**. `[도표]` **무압 0.1 C 곡선**(SI Fig. 12,
   충전 ≈235 · 방전 ≈217 mAh g⁻¹)이 2 MPa 곡선(≈233 / ≈214)과 **구별되지 않는다**.
   `[해석]` **490 MPa WIP 가 이미 계면을 만들어 놓아서 운전 압력이 할 일이 없다** —
   5호에서 1 → 25 MPa 가 임피던스를 >15 배 움직였던 것과 정반대이고, 모순이 아니라
   **제작 압력 이력이 다르기 때문**이다. ⚠ 그리고 **운전 상한이 훨씬 낮다**:
   `[인쇄]` "the probability of short-circuiting increased upon application of high
   pressures **exceeding 4 MPa**" — **5호의 Li 금속 75 MPa 의 1/19**.
   ⚠⚠ **그 문장에 데이터가 없다** (Fig. S11 의 압력 점은 2·3·4 MPa 셋뿐).
   → [[assb-stack-pressure-operating-window]].
5. **양극이 LFP 면** 평탄해서 `(X1, X3)` 축퇴가 그대로 온다
   (`raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md`). NMC 면 기울기가 있다.

## 들어올 논문에서 뽑을 것 (수집 지침)

`assb` 태그를 달 논문을 읽을 때 **이 축들을 먼저 찾는다.** 없으면 "없다" 고 적는다 —
없다는 사실도 이 계보의 관측이다 (액체셀 17 편 중 유일성을 잰 논문이 0 편이었던 것처럼).

| # | 뽑을 것 | 왜 |
|---|---|---|
| Q1 | **접촉 손실을 어떻게 정량했나** — 단위·측정법·모델 형태 | 위 "모르는 것 1" |
| Q2 | **접촉 손실과 LAM 을 가르는 독립 관측**을 썼나 (단면 SEM·임피던스·압력 시험 등) | 라벨 출처 |
| Q3 | **라벨 출처 층위** — measured / fitted / 가정, 오차 막대 유무 | 요구서 §5 규칙 |
| Q4 | **유일성·식별성을 쟀나** (조건수·근최적 폭·프로파일) | 액체셀 계열은 17/17 이 안 쟀다 |
| Q5 | **Li-In 기준 전위 이동**을 다뤘나 / 무시했나 | 위 "모르는 것 2" |
| Q6 | **압력**을 통제·보고했나 | 위 "모르는 것 4" |
| Q7 | **무음극이면** dead Li 와 SEI Li 를 갈랐나, 무엇으로 | 위 "모르는 것 3" |
| Q8 | 양극 화학 (NMC / LFP / 기타) 과 **OCP 기울기** | 위 "모르는 것 5" |

### 수집 현황 — Q1~Q8 채움표

| 논문 | Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|---|
| Bielefeld 2019 (`assb` 1호) | **부분** (`θ`) | **없다** (실험 0) | computed-geometric | **없다** | 없다 | **없다** | 없다 | 부분 (밀도·입도만) |
| Clausnitzer 2023 (`assb` 2호) | **부분** (`Connectivity` ≡ `θ` + `ρ_S` 소결밀도 + `R_GB`) | **부분** (Minnmann 2021 EIS 부분 전도도 — **타 재료계** NMC622/Li₆PS₅Cl, 자기 실험 0) | computed-geometric + computed-electrochemical, **오차막대 0 · 점당 구조 1 개** | **없다** (순수 forward) | **없다** (`indium` 0회; Li 금속·이상 접촉) | **없다** (`pressure` 0회) | **없다** (Li 금속 무열화 가정) | **★ 있다** — LCO + NMC811, `U₀ = 4.2 V` 함수형, `U_cut = 3.4 V`, `x ∈ [0.525, 1]` / `[0.231, 1]` |
| **Liu 2024 (`assb` 3호)** | **없다** — 접촉 손실의 **양을 계산하지 않는다**. 대리로 계면 **최대주응력**(평균 378 MPa 방전 → 580 MPa 충전; SE Young 률 1→150 GPa 에서 0.05→0.55 GPa). **차원이 달라 `θ` 로 변환 불가** | **없다** (자기 실험 0 — 3/3 편 공통). ★ 단 **부정적 정보**: `[인쇄]` 실험의 활물질 손실은 rock-salt + **입계 파괴로 고립된 활물질**을 **둘 다 포함**한다 | **fitted 문턱** — 활물질 손실 라벨 = `소성전단 > 12 %`, 그 12 %는 **타 화학(Li-rich, ref 5) 실험 분포에 적합**. 오차막대 0 · 문턱 민감도 0 · **구조 실현 1 개** | **없다** (순수 forward, `identifiab*` 0회) | **없다** (`indium` 0회; **음극 자체를 모델링 안 한다**) | **없다** (`pressure` 0회 — 접촉 역학 논문인데) | **없다** (음극 없음) | **★★ 있다 — 이 계보 최초의 OCV 곡선.** NMC811 + Ta-LLZO, GITT OCV `1−θ` 0→1 에서 **≈3.0 → 4.4 V vs Li/Li⁺**, 전 구간 기울기 있음, 컷오프 3.0 V |
| **★ Shi 2020 (`assb` 4호 — 첫 실험 논문)** | **★ 있다, 무차원 분율로** — void 부피분율 **2.87 / 3.23 / 9.50 vol%** (사이클 **0/10/50**) + 접촉 손실 **면적 10.4 %** (50 사이클). ⚠ `θ` 와 **같은 양이 아니다**: **면적** vs 부피, **퍼콜레이션 판정 없음**(`percolat*` 0회), 분모에 **NMC–NMC 접촉 포함**, 면적→용량 **사상 없음** | **★★ 있다 — 3/3 편 연속 0 을 깬다.** ① FIB-SEM 토모그래피(3 셀) ② EIS(사이클 1/5/10/20/50/51) ③ ★ **300 MPa 재가압 개입** — 이 계보 최초의 "접촉 손실만 되돌리는 조작". ⚠ ①이 ②③과 **다른 셀** | **measured-but-ML-thresholded** (새 층위: 실측 영상 + Weka ML 분할, **정확도 수치 0**) + fitted(EIS 등가회로, 파라미터 표 0). **오차막대 0 · 조건당 셀 1 · 반복 0** | **없다 (4/4 편 0).** ★ 단 형태가 다르다 — `[인쇄]` EIS 시간상수가 겹쳐 "**not possible to precisely assign** a single frequency region" 이라 적고도 `R_MF` 를 **점추정으로** 서사의 기둥에 쓴다 | **★ 부분 — 계보 최초 In 금속 음극 실물.** `[인쇄]` "1.4–3.7 V vs In (2–4.3 V vs Li/Li⁺)" = **오프셋 0.6 V 고정 가정**. 안정성 논의 **0**. ⚠ 그런데 `[도표]` **음극 쪽 `R_LF` 가 ≈0.7 → ≈110 kΩ (≈157 배)** | **★★ 있다 — 3/3 편 0 을 깬다.** 제작 **100/300/100 MPa** · 사이클 **~2 MPa 스프링** · **재가압 300 MPa**. ⚠ **스윕 없음**(각 1 점), 전부 **ESI 에만** | **없다 (4/4 편 0)** — In 음극이라 dead Li 축 해당 없음. 그런데 **음극 형태학 미관찰** (`[인쇄]` "requires further study of the anode morphology") | **★★ 있다 — 계보 최초의 실측 사이클별 V–Q.** NMC532(LZO 6–8 nm) / 비정질 LPS / CNF 60:35:5, 전 구간 **기울기 있음**. `[도표]` 방전 시작 전압 사이클 5→34 에 **≈−300 mV**, 사이클 39→40 에 **≈−500 mV 계단**, ★ **충전 전압 비단조 진동** |

| **★ Doux 2020 (`assb` 5호 — 압력 스윕의 첫 편)** | **부분 — 단, 축이 음극이다.** 양극 `θ`·접촉면적·퍼콜레이션 **0**. 대신 **Li\|SE 계면 접촉의 전기적 대리량을 곡선으로**: 셀 임피던스 `[인쇄]` P=1→25 MPa 에서 **>500 → 32 Ω**, DC 과전압 `[도표]` **7.0 → 4.5 mV**, `[재현]` 계면 ASR **≈25 → ≈8 Ω cm²** | **★ 있다, 네 채널** — ① in situ **X-선 토모그래피**(≈1.18 µm) ② **같은 셀 XRD**(Mo Kα 투과, FullProf) ③ EIS ④ **로드셀 압력 실계측**(0–220 MPa, Instron 교정). ⚠ 갈라 주는 것은 **덴드라이트/SEI** 이지 LAM_PE/접촉 손실이 아니다 | **measured-electrical**(임피던스·과전압·수명) + **measured-morphological 정성**(토모 수치 0) + **measured-phase 비정량**(profile matching — 상 분율 0). **적합 라벨 0**, 오차막대 0, 조건당 셀 1. ★ **예외: Table S2 가 펠릿 4 개의 상대밀도 산포**(80.2/84.9/80.3/83.0 %) — **계보 최초의 반복** | **없다 (5/5 편 0).** `identifiab*` 0 회. ★ 형태가 또 다르다 — **등가회로 적합조차 없어** 이 논문에는 역문제 자체가 없다 (Nyquist 를 날것으로만 보여준다) | **부분 — 그리고 문제로 남는다.** Li–In 셀이 **대조군의 본체**인데 전압축을 `[인쇄]` "2.5–4.3 V vs Li/Li⁺" 로 적고 **vs In → vs Li/Li⁺ 오프셋을 명시·인용·검토하지 않는다**. `[인쇄]` Li vs Li–In 의 **역학 차이는 "아직 연구되지 않았다"** 고 스스로 적는다 | **★★★ 이 논문의 본체 — 계보 최초의 압력 스윕.** P→임피던스 **6 점**(+이력 1) · P→단락시간 **6 점** · P→과전압 **5 점**(+미보고 2 MPa). 제작압 370(펠릿)/25(Li)/120(Li–In) MPa. ★ **상한이 숫자로**: **75 MPa 도금 전 기계적 단락**, 25 MPa 48 h, 5 MPa >1000 h. ⚠ **압력→용량 곡선은 여전히 없다** | **★ 부분 — 4/4 편 0 이 깨지되 절반만.** **SEI 는 상으로 검출**(Li₂S·LiCl·P₄·Li₃P₇) 이지만 **정량 0**; **dead Li 는 검출 수단 자체가 없다** — `[인쇄]` "Li metal dendrites are **not directly detected by XRD**" 이고 토모는 **밀도 대비**뿐(Li 0.534 vs 균열 0 이 안 갈린다). `dead li`·`isolated` 0 회 | **있다(CC)** — **LNO 2 wt% 코팅 NCA**(LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂) : LPSCl : carbon = 11:16:1 wt, **3.55 mg cm⁻²**, 2.5–4.3 V vs Li/Li⁺, C/10, 전 구간 기울기. **OCV·GITT 없다**(`OCV` 0 회) |

| **★ Lee 2020 (`assb` 6호 — 첫 **무음극** · 첫 **산업체**(SAIT/Samsung) · 첫 **Ah 급 파우치**)** | **없다.** `contact loss` **1 회**뿐이고 그마저 **남의 논문 인용**(refs 5,37–39). `percolat*`·`tortuos*`·`inactive` **0 회**. 유일한 대리량 = Table S2 의 **셀 두께 −5.51 %**(644.5 → 609.0 µm, WIP 490 MPa). **`θ` 를 공정으로 처리하고 재지 않는다** | **많다 — 그러나 전부 음극이다.** SEM/EDS · TEM/HAADF · **EELS(Li 맵)** · SADP · **XRD(Li₉Ag₄)** · X-선 CT(820 nm) · CV(Cu↔SUS) · EIS(온도만). ⚠ **양극 사후 분석 0** (`degradation` 본문 0 회) → `LAM_PE` ↔ 접촉 손실을 가르는 관측은 **하나도 없다** | **measured-electrochemical**(용량·CE·율·온도) + **measured-morphological 정성**(수치 0, 전부 형용사) + **measured-phase 비정량**(Li₉Ag₄, Rietveld 없음). **적합 라벨 0**(`fit*`·`equivalent circuit` 0 회). ⚠ **셀 수가 어디에도 없다**(`n =`·`N =`·`error bar`·`standard deviation`·`replicate` 전부 0 회) — ★ 유일한 산포 = **Table S2 ±2.2–2.9 µm**(정의·n 없음) | **없다 (6/6 편).** `identifiab*` 0 회. **역문제를 아예 풀지 않는다**(등가회로도 곡선 적합도 없다) — 5호와 같은 형태 | **해당 없음** (`indium` 0 회, 무음극). ★ **그러나 같은 문제가 다른 옷을 입는다**: `[도표]` Fig. 4a + SI Fig. 4c 에서 **음극 전위가 앞 9.5–16.6 % 용량 동안 ≈1 → 0 V 를 훑는다** → **"무음극은 OCP 평탄" 이 그 구간에서 거짓** | **★★★ 있다 — 그리고 축을 둘로 쪼갠다.** **제작 490 MPa 등방(WIP, 계보 최고, 대기 중)** + **운전 2/3/4 MPa 스윕** + **무압 대조**. `[재현]` WIP 치밀화 −5.51 % 가 **7 일 무압에 +0.8 µm 만 복원**(비가역). `[도표]` 무압 0.1 C 곡선이 2 MPa 와 **구별 안 된다**. ⚠ `[인쇄]` **">4 MPa 단락 확률 증가" 는 데이터 0** | **★★ 부분 — 채널은 늘고 정량은 0.** ① 방전 단면 SEM(음성; `[재현]` 한계 1 µm = 용량의 **3.0 %**, 사이클당 손실의 **270 배**) ② ★ **EELS Li 맵** — `[도표]` **방전 후·100 사이클 후에도 Li 망 잔존**(pristine 엔 없음) ③ ★★ **XRD 로 Li₉Ag₄** — **Li 저장 상을 동정한 첫 사례**(가역) ④ CE. **dead Li 를 SEI·합금·LiC_x 와 가르는 수단은 없다**. `[인쇄]` "isolated lithium" 을 기구로 지목하고 **한 번도 안 잰다** | **★★ 있다 — 계보 최초로 음극 쪽 전압축.** LZO(5 nm)-**LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** : Li₆PS₅Cl : CNF : PTFE = 85:15:3:1.5, **6.8 mAh cm⁻²**, **215 mAh g⁻¹@0.2C**, 2.5–4.25 V, 전 구간 기울기. **OCV·GITT 0 회**. ★ **Fig. 4a** = 컷오프 전압 ↔ 면적용량 **5 점 사상**(3.5/3.55/3.6/4.0/4.25 V ↔ 0.5/0.64/1.12/5.0/6.75 mAh cm⁻²), ★★ **SI Fig. 16** = 사이클 1/200/400/600/800/1000 의 **V–Q 6 곡선** |

| **★ Spencer-Jolly 2023 (`assb` 7호 — 첫 **operando 회절** · 6호의 **외부 검증** · Bruce/Oxford)** | **없다.** `contact loss`·`percolat*`·`tortuos*` **0 회**. **양극이 아예 없다** — `[인쇄]` "these performances relate **only to the anode** and do not encompass … a composite cathode". 음극 계면 분리를 서론에서 언급만 하고 재지 않는다 | **★★ 있다, 다섯 채널 — 전부 음극.** ① **operando PXRD**(반사, Cu Kα, 시간 분해) ② **operando 싱크로트론 PXRD**(Diamond I12, 56 keV 투과, 스팟 50 µm) ③ ★ **전기화학을 뺀 ex situ 화학반응 PXRD**(LiC_x + Ag 혼합 — 계보 최초의 "화학만" 대조) ④ 평면 SEM/EDX(집전체 제거) ⑤ 단면 SEM/EDX. ⚠ `LAM_PE` ↔ 접촉 손실을 가르는 관측은 **0** | **measured-structural, 정성.** 상의 **존재/부재·순서**만. **Rietveld 0 · 상 분율 0 · 격자상수 0 · Δ2θ 수치 0**. 적합 라벨 0(등가회로·곡선적합 0). **오차막대 0 · 셀 수 어디에도 없음**(`n =`·`N =`·`error bar`·`standard deviation`·`replicate`·`uncertain*` 본문 13 쪽 + SI 6 쪽 **전수 0 회**) | **없다 (7/7 편).** `identifiab*` 0 회. **역문제를 아예 풀지 않는다** — 5·6호와 같은 형태 | **해당 없음** (`indium` 0 회, 상대극이 **Li 금속 박 50 µm**). ★ **대신 이 계보 최초로 음극 전위를 Li 기준으로 직접 읽는다**(반쪽전지). 그리고 6호의 "앞 구간이 평탄하지 않다" 를 **독립 재현**: `[도표]` SI Fig. 1 흑연 단독이 0.9 → 0 V 를 훑는 데 **용량의 ≈11.5 %**, Fig. 5 의 2 mA cm⁻² 는 **≈15 %** (6호 9.5–16.6 %) | **부분 — 6호 대비 후퇴.** 제작 **일축 400 MPa** + 운전 **2 MPa(원뿔 스프링)** 두 축 구조는 6호와 같지만 **스윕 0 · 로드셀 0 · 무압 대조 0 · 압력→용량 0**. `pressure` 5 회 · `MPa` **2 회**. 도금으로 스택이 두꺼워질 때의 압력 변화 보고 없음 | **★★★ 이 계보에서 가장 가까이 갔다 — 그런데 논문은 안 잰다.** `dead`·`isolated`·`Coulombic`·`efficiency` **전수 0 회**. 그러나 ① operando XRD 가 **Li 를 담은 상 11 종**을 시간축 위에서 동정 ② **자기 Fig. 1·3 의 시간축이 전하 수지를 닫을 재료를 준다** → `[재현]` **충전 2.03 · 방전 1.05 · SEI 0.19 mAh cm⁻² ⇒ 첫 사이클 효율 ≈52 %, 설명되지 않는 비가역분 ≈0.79 mAh cm⁻² = 통과 전하의 39 %** ③ 방전 후 **잔류 Li 의 형태학 증거**(Fig. 6C·6F 탄소 음성 영역). ⚠ **dead Li ↔ SEI 는 여전히 안 갈린다** | **없다 — 양극이 없다.** `OCV`·`open circuit`·`GITT` **0 회**. 전압축은 전부 **음극 쪽 정전류 곡선**이다 |

| **★ Li et al. 2026 (`assb` 8호 — 첫 **BMS·진단 종설** · ⚠ **Mini Review, 1차 측정 0**)** | **없다 — 정량 0.** `contact loss` **2 회** · `percolat*`·`tortuos*`·`θ` **0 회**. ★ **그러나 이 계보 최초로 "가르는 진단이 필요하다" 를 요구로 인쇄한다**: `[인쇄]` §6.1 "diagnostics capable of **distinguishing contact loss from ordinary electrochemical aging**"(Biçer 2025 — ⚠ 그것도 종설) | **없다 — 리뷰다** (자기 실험 0, 1차 데이터 0). ★ 대신 **처방**: EIS/DRT/GITT/**active bounded pulse** 네 채널의 역할 분담표(Table 3) + ASSB 용 `[인쇄]` "**pressure or force sensing**" · "**pressure-dependent impedance models**" | **★★★ 이 계보 최초로 라벨·불확실성 층위를 표의 열로 만든다 — 단 층위가 다르다.** Table 2 에 `Training/chemistry boundary`·`Validation level`·**`Uncertainty output`** 열. `[재현]` **보정된 불확실성 0 / 8** (CI 1 · "가능하나 미시연" 1 · "주산출 아님" 2 · "없음" 4), **`Cell` 검증 7 / 8**. `[인쇄]` "Field labels are limited"·"**no direct capacity labels**"·생산 추정기 3 요소(estimate + **calibrated uncertainty** + **validity flag**). ⚠⚠ **열화 모드 라벨은 0** — `LLI`·`LAM`·`degradation mode`·`incremental capacity`·`differential voltage`·`half-cell` **전수 0 회**. **이 리뷰의 SOH 는 끝까지 스칼라다** | **★★ 여전히 0 (8/8 편) — 그러나 성질이 바뀐다.** 이 계보 최초로 **식별 가능성을 실패 모드로 명명**한다 (`identifiab*` **5 회**; 1–7 호는 전부 0 회): `[인쇄]` Table 1 "ECMs … can **lose physical uniqueness**" · §2 "**Parameter identifiability** … can make a detailed model **appear more precise than the available measurements justify**" · Table 3 "**Ill-posed inversion needs regularization**" · ★ **Table 4 중기 실패 모드 "Unidentifiable pulse response"** · §3.1 "what **minimum excitation can resolve** the safety-relevant process". ⚠ **측정 0** — 조건수·프로파일 가능도·근최적 폭·Fisher/CRB 전부 없다. ⚠⚠ `poorly identifiable` 문장이 매단 인용이 **Si–C 음극 소재 종설**이다(D2) | **해당 없음** — `indium`·`Li–In` **0 회** | **★ 부분 — 재인용 수치 1 점 + 처방 3 개.** `[인쇄]` "stack pressure becomes a **coupled state/control variable**" · "Xu et al. (2024) note industrial requirements **below approximately 1 MPa**" · Table 4 장기 "**include pressure for solid state**" / 실패 모드 "**pressure/contact failure**". `[재현]` `MPa` **전체 1 회**, 값이 **1**. ★ **우리가 읽어 온 실험실 압력 창(2–490 MPa) 전체가 이 요구치 위에 있다.** ⚠ **재인용** — Xu 2024 를 받아야 한다 | **없다.** `plating` 9 회는 전부 **액체셀 저온 급속충전의 제약(gate)** 이고 dead Li ↔ SEI Li 분해는 0. `anode-free`·`dead li`·`isolated li` **0 회** | **없다** (ASSB 양극 화학 0, OCV 곡선 0). ★ **인접 관측 하나**: `[인쇄]` Li–S "voltage behavior contains **regions in which conventional OCV and Coulomb-counting assumptions are less informative**" · Na-ion "**OCV–SOC relations … require recalibration**" → **평탄/비정보 OCV 가 상태 추정을 깨는 문제가 다른 화학에서 반복된다** |

| **★★ Huo et al. 2025 (`assb` 9호 — 첫 **실험 + 파라미터 식별 동시** · 첫 **결합 전기화학-노화 모델** · 상하이교통대)** | **부분 — 그리고 자기 모순이다.** `[인쇄]` `A^p_eff = 0.4938` (무차원, 양극, BV 분모에 정의) = 이 계보 최초의 **모델 파라미터로서의 양극 접촉 면적비**. ⚠ (a) **적합값**, (b) **노화 중 고정** → `θ(N)` 0, (c) `[재현]` 자기 SEM 의 입자 반경(≈1.05 µm)을 쓰면 **0.055 로 9 배 움직인다**. `contact loss` 3 회는 전부 **남의 논문 인용**(refs 17,18,21) | **부분.** SEM(표면, 정성, 노화 1 + 신품 1) · EIS(2-전극, 등가회로) · **압력 센서 연속 시계열(★ 계보 최초)**. **XRD·XPS·TEM·ICP·적정·3-전극·반쪽전지(노화품) 전부 0.** `LAM_PE` 를 **적합 밖에서** 확인한 관측 **0 건** | ★★ **새 층위: `fitted-single-parameter`.** 노화 라벨 = **1-파라미터 PSO 적합**(`ε_p`)이고 정답축이 **자기 자신의 방전곡선**이다. 오차막대 0 · 셀 **2** · 반복 0 · `n =` 0 회. ★ **Table 3 에 provenance 열이 없고 6 개 값이 비공개**(`[인쇄]` "not disclosed") | **0 (9/9 편).** `uncertaint*`·`identifiab*`·`sensitiv*`·`confidence`·`Fisher`·`condition number`·`bootstrap`·`initial guess`·`multi-start`·`error bar`·`regulariz*`·`objective function` **전수 0 회**. ★★★ **성질이 또 바뀐다** — 8호가 "이름을 실패 모드 목록에 올렸다" 였다면 **9호는 자기 표 안에 축퇴의 지문 셋을 인쇄해 놓고 다르게 부른다**: ① `R_SEI` 분해가 동일 공정 두 셀에서 **+37 % / −80 %** 인데 `[인쇄]` "장비 정확도·**적합 오차**·열평형" 탓으로 지나간다 ② `A_eff·ε_p/R_s` **곱 축퇴** ③ `k_LAM` 셀 간 **2.15 배**를 `[인쇄]` "slightly different" | **해당 없음 → 그러나 새 형태로 열린다.** `indium`·`Li-In` 0 회. ★ **계보 최초의 합금(Li-Si) 음극**이고 모델은 `U^n_ocp(θn)` 를 **비평탄 보간 함수**로 둔다. `[재현]` 모델 N/P ≈ **3.14** → 사이클당 음극 화학량론 스윙 **31.8 %**. → **이 카드의 "전고체 음극은 평탄 → 5→3 붕괴" 가 이 셀에는 성립하지 않는다.** ⚠ N/P 는 SI 가 제출 거부한 값이고 **우리가 Table 3 에서 계산했다** | ★★ **있다 — 계보 최초의 `in operando` 연속 힘 시계열.** `[도표]` Fig. 6 이 12 사이클의 힘을 `Kg` 로 기록(고점 296.6 · 저점 294.0 · 스윙 2.6). `[재현]` 면적 7.854e−5 m² 환산 → **평균 ≈36.9 MPa · 주기 변조 ≈0.32 MPa**. ⚠ **`MPa` 0 회 · 제작 압력값 0 · 교정 0 · 스윕 0 · 노화 전 구간 추세 0**. ★★ **압력이 모델에 들어가지 않는다** — Eq. (2) 는 사이클 수만의 함수다 | **해당 없음** (Li-Si 합금 음극). `dead li`·`isolated` 0 회. ⚠ 그리고 **CE 를 SI 에서 명시적으로 제출 거부**한다 → `LLI` 의 전하 수지 채널이 닫힌다 | **있다(CC).** **단결정 NCM811 + H₃BO₃ 코팅**(★ 계보 최초의 붕산 코팅) : Li₆PS₅Cl : VGCF = **56:40:4 wt%**, `[재현]` **10.7 mg cm⁻²**, `[도표]` **2.0–4.3 V**, 전 구간 기울기 있음. ★ `[도표]` Fig. A.1(a) = **NCM811 반쪽전지 dV/dQ vs SOC** (계보 최초의 양극 반쪽셀 미분곡선) ⚠ **측정조건 전무**. **OCV·GITT 0 회** — 모델의 `U_ocp` 두 곡선은 출처가 없다 |

| **★★★ Vadhva, Hu, Johnson (3인 공동 1저자), Stocker, Braglia, Brett, Rettie 2021 (`assb` 10호 — 첫 **방법론 리뷰** · UCL + **HORIBA MIRA**(기업) · ⚠ **1차 측정 0**)** | **없다 (10/10 편).** `contact loss`·`percolat*`·`θ` **0 회**. 유일한 접점 = `[인쇄]` Fig. 9 본문 "**loss of interfacial contact in the composite cathode due to volumetric expansion**" — ★★ 그런데 그 문장이 **분해층 형성과 `and` 로 한 저항(`R_MF`)에 묶여 있다**. 가장 가까운 정량 채널은 **TLM + 전자차단 대칭셀의 유효 이온 굴곡도**(ref. 57 Kaiser) — `θ_AM` 과 같은 양이 아니다 | **★★ 있다 — 그러나 "가르는 관측" 이 아니라 "가르는 절차" 다.** ① **상보 대칭셀 쌍**(차단/가역) ② **저온으로 시상수 벌리기**(ref. 82 Bron — `R_gb` 를 −130 °C 에서 동정해 **실온 적합의 구속으로 되가져온다**) ③ **가압으로 큰 시상수 제거**(ref. 28, `[도표]` 400 MPa 에서 `R_int` 가 사라지자 `GB` 가 드러난다) ④ **DRT 로 개수를 먼저 정하기**(ref. 62) ⑤ **4 단자**(ref. 21) ⑥ **K–K / Lin-KK 사전 검증**(ref. 41–43). ⚠ **전부 재인용 · ASB 복합양극에 `LAM_PE` ↔ 접촉 손실로 적용된 사례 0** | **해당 없음 — 리뷰다** (1차 측정 0, 열화 라벨 0: `LLI`·`LAM`·`degradation mode`·`half-cell` 전수 0 회). ★ **새 층위 하나**: `[인쇄]` **기관 간 라운드로빈 산포** — `>1 mS cm⁻¹` 에서 상대 중앙값 오차 **22 %**, `<1` 에서 **~10 %** (⚠ 재인용, ⚠⚠ 인용 번호가 틀렸다 — D5). **"같은 양을 여러 기관이 재면 얼마나 벌어지는가" 의 첫 숫자** + `[인쇄]` **삼중 측정 권고** | **★★★ 0 이 깨진다 — 단 "쟀다" 가 아니라 "일반 현상임을 인쇄했다".** `[인쇄]` "**As no solution to an EIS spectrum is unique**" · "**The non-uniqueness of an ECM solution**" · "**the inclusion of more elements will tend to improve the fit**" · "how many time constants … **highly subjective**" · "Physical features **may not be visible**" · **AIC 로 회로 순위 매기기**(ref. 51,52; `[인쇄]` "only recently applied to **simulated** data") · **DRT 는 `ill-posed`, `regularization` 필요**. ★★ 그리고 **"분해 가능한 RC 개수 = 실험 조건의 함수" 를 다섯 사례로 보인다**(황화물 5 중 3 만 입계 분해 · LGPS 실온 원호 0 개 · 400 MPa 에서 GB 등장 · 폴리머 60 °C 에서 상경계 소멸 · **노화가 RQ 를 3→4 로**). ⚠ **측정 0** — `identifiab*`·`uncertaint*`·`confidence`·`condition number`·`error bar` **전수 0 회** | **★★ 부분 — 새 경고 둘.** `indium` 2 · `Li-In` 2 회. ① Li 금속이 비이상적이라 **Li-In 을 기준극 대안**으로 제시 ② ★★ `[인쇄]` **방전 중 In 음극 계면 저항이 리튬화도(In-rich 화)로 크게 증가** ⇒ **`R_anode(N)` 에서 노화분과 SoC 분이 안 갈린다** (4호 `R_LF` ≈157 배 해석에 직접 걸린다) ③ ★★★ `[인쇄]` **In–Li 음극 셀은 LMA 셀과 전극↔주파수 귀속이 반대다** ⇒ **"저주파=양극" 같은 보편 규칙이 없다**. ⚠ 전위 오프셋 안정성은 여전히 0 | **부분 — 값 3 개.** `[인쇄]` **~120 MPa**(σ 포화, 단 그것이 인가 최대압) · `[인쇄]` **~400 MPa**(Li₆PS₅Cl σ 는 거기까지 계속 증가, ref. 84 = **Doux JMCA 2020**, 우리 5호의 자매) · `[도표]` **400 MPa**(Fig. 11a, Li\|LLZO\|Li). ★★ **개념 기여가 값보다 크다**: ① `[인쇄]` "**<1 Ω cm², remained after the pressure was removed**" = **5호의 이력을 산화물에서 독립 재현** ② **압력이 분해능 연산자다** ③ `[인쇄]` 제언 2 가 **다변수(온도·압력·SoC) 시험**을 ECM 구축의 표준 처방으로 올린다. ⚠ **압력→용량 곡선 0 (10/10 편)** | **없다.** `dead li`·`isolated` 0 회. ★ 인접 둘: ① `[인쇄]` **soft short**(LLZO 내부 Li 석출)를 **`R_leak` ECM 원소**로 잡고 `R_b`·`R_gb` 안정성으로 부재 확인 ② `[인쇄]` **NLEIS 가 상용 LiB 에서 Li 도금 검출**(ref. 184). 둘 다 **석출**이지 **고립**이 아니다 | **없다.** `OCV` **1 회**(⚠ 그것도 `[인쇄]` "**OCV variation due to small capacity changes can affect the low-frequency range**" — 즉 **OCV 드리프트가 EIS 저주파를 오염시킨다**는 경고다). `GITT`·`half-cell` 0 회, **V–Q 곡선 0 장**. ★ 대신 `[도표]` Fig. 9b/9c = **SoC 축 위 EIS 10+10 점**(충전 3.305–3.599 V / 방전 3.442–2.000 V, LCO) — **전압축은 있고 용량축이 없다** |

| **★★★ Yu, Choi, Dunham, …, Farahati, Kim 2024 (`assb` 11호 — 첫 **graphite 음극 완전지** · 첫 **DRT** · **Schaeffler**(산업체) + Ohio State · *J. Power Sources* 597, 234116)** | **부분 — 단위가 Ω 다.** `contact loss`·`percolat*`·`tortuos*`·`θ` **0 회**. 대리량 = **P3 DRT 봉우리 높이**(`Ω` 또는 `Ω mg⁻¹`). ★ **계보 최초로 (i) 주파수로 국소화되고 (ii) 시계열이 있고(최장 6 점) (iii) 조작(재가압)으로 되돌려지는** 접촉 손실 대리량. ⚠ 셋이 막는다 — ① 무차원 분율이 아니다(용량 사상 0) ② ★★ **전극을 가르지 않는다** (`[도표]` Fig. 8 이 P3 에 **Cathode + Anode 둘 다** 찍는다) ③ `[인쇄]` Table 1 이 P3 를 "active material/SE **and/or** electrode/current-collector" 로 둔다 — **복합양극 내부 접촉과 집전체 접촉을 안 가른다** | **★★ 있다 — 네 조작, 그러나 전부 임피던스 안이다.** ① **완전지 ↔ NMC/In–Li ↔ graphite/In–Li 반쪽전지 분해**(계보 최초) ② **SE 입도 스윕**(nano ≤1 µm vs micro ≤20 µm) ③ **코팅 유무**(LiNbO₃ vs bare) ④ **재가압**(150 / >500 MPa). ⚠⚠ **형태학·화학 관측 0** — SEM·TEM·FIB 토모·XRD·XPS·ToF-SIMS **전수 0**. **접촉 손실을 임피던스 밖에서 확인한 관측 0 건** (4호가 FIB-SEM 으로 void 를 실측한 것과 정반대) | ★★ **새 층위: `inverted-nonunique`.** 라벨이 **ill-posed 역변환의 봉우리 높이**인데 **정규화 설정이 보고되지 않았다**(`regulariz*`·`λ`·`L-curve`·`GCV`·RBF shape **전수 0 회**). 그 위에 `[인쇄]` Fig. 2 캡션 — DRT 를 **"simulated Nyquist curves" 위에서** 계산했다 ⇒ **ECM 을 입력으로 받은 DRT**(순환). 오차막대 0 · 셀 수 0(`n =` 0 회) · 반복 0. ★ `[인쇄]` **"The authors do not have permission to share data."** ⚠⚠ **파라미터 표가 아예 없다** — 9호는 6 개를 "not disclosed" 로 **찍었는데** 38호는 구멍을 셀 기준조차 없다 (**어느 셀이 Cl 이고 어느 셀이 Br 인지도 끝까지 안 밝힌다**) | **0 (11/11 편).** `identifiab*`·`uniqu*`·`ill-posed`·`regulariz*`·`uncertaint*`·`confidence`·`error bar`·`Kramers`·`Kronig`·`condition number`·`Fisher`·`Bayes*`·`posterior`·`overfit*`·`degenerac*`·`λ`·`L-curve`·`GCV`·`cross-valid*` — **본문 + SI 전수 0 회**. ★★★ **성질이 다섯 번째로 바뀐다 — "잴 재료를 SI 에 인쇄해 놓고 뺄셈을 안 했다"**: `[도표]` **Fig. S3 가 같은 셀에서 배선만 바꿔 DRT 봉우리를 −15 % ~ +69 % 움직인다**(≈3 kHz −15 % · ≈0.03 Hz **+69 %** · 분해된 어깨 **1 개 유무 차이**), 그런데 **본문의 재가압 효과는 −10 ~ −25 %** 로 **그 폭 안**이다. 논문은 둘을 나란히 놓지 않는다. ★★ 두 번째 재료: `[재현]` **P3 의 보고 위치가 논문 안에서 500 Hz–10 kHz = 1.3 자릿수**인데 **P2–P3 간격은 0.8 자릿수**(`log₁₀(6000/900)=0.82`) ⇒ **이름표의 불확정성이 이름표 간격보다 크다** = P2(화학) ↔ P3(기계) 분리 붕괴 | **부분 — 값은 들어왔고 검토는 0.** `indium` **1 회** · `In–Li` 7 회. `[인쇄]` 반쪽전지 창 **−0.595 – 0.9 V**(음극) · **2.1–3.7 V**(양극) · 완전지 **2.7–4.2 V** ⇒ `[재현]` **오프셋 ≈0.60–0.62 V vs Li/Li⁺ 가 함의된다** (계보 최초로 소수 셋째 자리까지). ⚠ **명시·인용·안정성 논의 전부 0**. ⚠⚠ 10호의 경고(방전 중 In 계면 저항이 리튬화도로 변한다)를 **검토하지 않는다** — 모든 EIS 가 `[인쇄]` **완전지 기준 50 % SOC** 이고 **반쪽전지의 In–Li 리튬화도는 통제되지 않았다** | **★★★ 이 계보에서 가장 넓다 — 그리고 `압력 → 용량` 을 처음으로 준다.** 제작 `[인쇄]` **>500 MPa** · 운전 `[인쇄]` **20 MPa** · 재가압 **150 / >500 MPa**. `MPa` **48 회**. ★ **압력→용량 반쪽 3 점**(`[인쇄]` 165.0 / 166.9 / **173.1** mAh g⁻¹) + **완전지 2 점**(169.9 / 171.7) — **10/10 편이 못 준 칸이 채워진다**. ★★ 그리고 **압력 → 봉우리별 Δ**(`[도표]` Fig. 4d · 7d). ⚠ **효과가 4호의 1/12** (`[재현]` +4.91 % vs 4호 +60.5 %p) 인데 `[인쇄]` "agree with previous report by **Ceder et al. [21]**"(= 우리 4호) 라고만 쓰고 **크기를 비교하지 않는다**. ⚠⚠ **계측 수단 0** — `[도표]` Fig. S1 은 **볼트·너트**(정변위)인데 `[인쇄]` "remained **constant at 20 MPa**". ⚠⚠⚠ ★★ **선택성이 없다** — 재가압이 `[도표]` P1 **−11 %** · P2 **−10 %** · P3 **−16 %** · P4(전하이동) **−25 %** · 무표기 0.03 Hz **−27 %** 를 **전부** 줄인다 | **해당 없음** (graphite 음극). `dead li`·`isolated`·`plating` **0 회**. ★ 인접 하나 — `[인쇄]` graphite 반쪽 CE ">99.99 %" 인데 `[도표]` Fig. 6(a) 의 CE 축은 **5 %p 눈금**이라 0.01 % 를 분해 못 하고 **사이클 ≈65 에 ≈98.5 % 로 떨어지는 점**이 있다 (`[재현]` 용량 역산 평균은 ≈99.98 %/cycle 로 정합) | **★★★ 계보 최초의 graphite 음극 ASSB 완전지.** LiNbO₃-코팅 **NMC622** + **graphite** + Li₆PS₅X, **2.7–4.2 V**, C/3, `[인쇄]` **192.4 → 179.8(200 cy) → 169.9(500 cy) mAh g⁻¹**. `OCV`·`open circuit`·`GITT` **0 회**, **V–Q 곡선 0 장**(10호와 같다). ★★★★ **그런데 이 칸이 이 카드의 전제를 깬다** — graphite 는 **스테이지 평탄역이 여럿인 구조 있는 OCP** 다 ⇒ **"전고체 음극은 평탄 → 5→3 붕괴" 가 이 셀에 성립하지 않는다** (9호 Li-Si 에 이은 **두 번째 반례**이고 이쪽은 **상용 흑연**이라 더 직접적) |

| **Sadegh Kouhestani, Yi, Qi, Liu, Wang, Gao, Yu, Liu 2022 (`assb` 12호 — 첫 **PHM 종설** · Kansas + USTB + North Minzu · *Energies* 15, 6599 · ⚠ **Review, 1차 측정 0, 그림 7 장 전부 타 논문 재수록(LIB 6 + 2009 모식도 1)**)** | **없다 (12/12 편).** `contact loss`·`θ`·`percolat*` **0 회**. `contact area` 3 회 = 전부 §3.1.1 재인용 — `[인쇄]` "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe the contact area, which adjusts the current density in the 1-D Newman model** … the capacity drop was correlated with the loss of contact area", **값 0**. ★ `[해석]` 그 형태는 9호 `A^p_eff`(BV 분모)의 **조상 후보**(Tian & Qi 2017 → Shao 2022) — 원전 미확인 | **없다 — 리뷰다.** 인용 중 실험 영상이 모델에 들어간 것은 Fathiannasab 2021 토모그래피 1 편(재인용). ★★★ 그리고 **분리 물음을 정의에서 지운다**: `[인쇄]` §2.2 "**The loss of active materials mainly stems from the electrical contact loss** that is caused by graphite spalling, adhesive decomposition, collector corrosion, and electrode particle cracking" ⇒ 이 리뷰의 어휘에서 **`LAM ⊃ 접촉 손실`** 이고, 열거된 기구는 **전부 액체셀 것**. `[도표]` Fig. 6 의 "Contact Loss" 두 자리도 **집전체**(Cu 균열·Al 부식) | **해당 없음 + 날짜 하나.** SOH = `[인쇄]` 식 (6) 스칼라 `Q_max/Q_nominal`; 열화 모드 라벨 **0**(`LLI` 2 · `LAM` 1 회는 정의 문장뿐, 정량법 0 — 모드 정량 원전 두 편 refs 57·58 은 "**CL**" 이라는 낱말의 각주로만 쓰인다); Table 1 에 검증·불확실성·화학 열 **없음**(열이 Categories·Technique 둘); `[인쇄]` "Data Availability Statement: **Not applicable**". ★ `[인쇄]` "**very few instances where a battery can be completely exhausted or fully charged at the pack level**"(재인용) + `[인쇄]` "**most PHM techniques are based on simulation results and not experimental**"(1차) ⇒ 8호(2026)의 "no direct capacity labels" 와 같은 명제가 **2022 년에** 인쇄돼 있다 | **0 (12/12 편). 성질은 8호 이전 — 계보의 출발점을 날짜로 고정한다.** `identifiab*` **0** · `uniqu*` 1(무관: "no unique technique") · `ill-posed`·`regulariz*`·`confidence`·`error bar`·`standard deviation` **0** · `uncertaint*` 3(일반론). 가장 가까운 문장 셋: ① `[인쇄]` "difficult parameter identification"(×2, 실무 곤란) ② `[인쇄]` "large number of parameters … **inevitable errors in each parameter**" ③ 재인용 `[인쇄]` "**from a single impedance arc to a double impedance arc**" (노화·온도로, [84] LIB ECM) — 그리고 ②의 **반대 명제** `[인쇄]` "the more parameters … **the higher the accuracy**"(§3.1.3)가 같은 논문에 있다. ⇒ 8호가 이름을 붙인 것(`identifiab*` 5 회)이 **2022 년 PHM 종설에는 이름조차 없었다** | **없다.** `indium`·`In-Li`·`Li-In` 0 회 | **부분 — 재인용 1 값.** `[인쇄]` "optimal charging performance … under medium compressive pressures (**0.4–1 MPa**)" — ⚠ 출처가 **중복 인용번호 [60]**(D4) 탓에 Tian & Qi 2017 / Shao 2022 중 **확정 불가**. `[인쇄]` "anisotropic displacement of AM particles can also be prevented by applying **external compressive pressure**"(Fathiannasab). `stack` 0 · `MPa` 1 회. ★ 8호의 재인용 "<≈1 MPa"(Xu 2024, 산업 요구)와 **다른 원전에서 같은 자릿수** — 실험실 창(2–490 MPa)은 둘 다의 위 | **없다.** LLI 원인 = `[인쇄]` "SEI layer, lithium dendrite, and battery self-discharge"(LIB). `anode-free`·`dead li`·`isolated` 0 회 | **없다.** LCO(식 1; `[인쇄]` "LiCoO₂ **or LTO**" — LTO 는 음극, D1) · TiS₂ · LiPON 등 **이름만**. `OCV` 2 회(PNGV 설명 · Fig. 4 회로 기호) · `IC curve` 1 회 · `GITT` 1 회(Fabre 파라미터화) · **V–Q 곡선 0 장 · OCP 곡선 0 장**. 유일한 미분곡선 = `[도표]` 재수록 Fig. 5 의 dV/dQ 삽도. ⚠ `[도표]` 같은 Fig. 5 가 **`SOH = {FOI₁ … FOIₙ}` 벡터**를 인쇄하는데 본문 식 (6) 은 **스칼라** — 논문은 언급 없음(D20) |

| **Zheng, Xie, Zhang, Yang, Zhou, Zhu 2026 (`assb` 13호 — 첫 **그리드 용도 appraisal** · Nanjing Tech + **Huadian 전력연구원 + Shuangdeng(전지 제조사)** · *Energy* 345, 140229 · ⚠ **Perspective, 1차 측정 0, `[인쇄]` "No data was used", 그림 5 장 전부 모식도/레이더**)** | **없다 (정량 0).** `contact loss` **1 회**(M³ 시뮬 대상 열거) · `interfacial contact` 6 · `θ`·`percolat*`·`tortuos*` 0 · 단위·모델 형태 0. ★ 대신 **대리량을 지목한다**: `[인쇄]` "decay of **interfacial contact pressure** — a primary driver of impedance growth" → 압력 센서 시계열 = 접촉 손실의 관측 (9호가 힘을 **재고도 모델에 안 넣은** 자리를 처방으로 채운다). 인과 방향 `압력 감쇠 → 임피던스 ↑` 명시 | **없다 — perspective.** 처방 셋: ① 압전/박막 **압력 센서**(셀 스택 내장) ② `[인쇄]` "**EIS** could be used as a **proxy for contact integrity**"(주파수·특징 0, `DRT` 0) ③ **음향/초음파**(void·crack; 인용 [41] 은 음향 논문이 아님 D9). `LAM_PE` ↔ 접촉 손실을 가르는 관측으로 제시된 것 **0** | **해당 없음 + 정의 하나.** Table 1 ASSB 열 = 투영(재인용 2 + **무인용 5**, 10000–15000 cycles 무인용 G2), LCOS 식 (1) 입력(`d`·`P_charge`·`C_deg`) **미공개**(G1) → `$0.08–0.12/kWh` 재현 불가. ★ **라벨 정의는 인쇄됐다**: `[인쇄]` SOH 는 "**true active material loss**" ↔ "**reduction in usable capacity caused by rising impedance or increasing overpotentials**" 를 갈라야 한다 — **2 항 이분법**이고 **같은 절이 지배 실패 모드 1 번으로 꼽은 접촉 손실의 소속을 말하지 않는다** (`θ_AM` 이 문장에서 사라짐). 12호 `LAM ⊃ 접촉 손실` ↔ 13호 `LAM ∣ kinetic + 접촉 손실 미배정` — **두 종설의 분류가 다르고 둘 다 우리 3 항과 다르다** | **0 (13/13 편).** `identifiab*`·`ill-posed`·`regulariz*`·`uncertaint*`·`confidence`·`error bar` 전수 0, `uniqu*` 3 무관. ★ 성질: **역추정을 워크플로로 처방한다** — `[인쇄]` "These models **inversely estimate** the current state of interfacial contact **and** material properties" — 유일성 경고 **0**. 9호의 `A_eff·ε_p/R_s` 곱 축퇴가 정확히 "접촉 상태 ↔ 재료 물성" 사이에 있는데 이 논문은 그것을 모른다. ⇒ 8호(2026, `identifiab*` 5)와 **같은 해**에 이름 없이 역문제를 처방 — "2026 년 문헌은 식별 가능성을 안다" 는 8호 한 편의 일 | **해당 없음.** `indium`·`In-Li` 0. Li 금속 음극 자체를 `[인쇄]` "may be misguided" 로 배제 | **★★ 있다 — 이 편의 본체(값은 적다).** `pressure` **24** · `stack pressure` 7 · `pressure-less` 5 · `MPa` 본문 **2**(둘 다 `<5`). ① 1 차 주장 `[인쇄]` **`<5 MPa`** ×2(Si 음극 / 저압 아키텍처 문턱; 근거 [35]·[45], "5" 의 출처 미명시 G3) ② `[도표]` **Fig. 2 클래스별 창 — 본문에 없는 다섯 값**: Oxides **≥30** · Sulfides **5–20** · Halides **2–10** · Polymers **0/compliant** · Composites **1–10 MPa** (⚠ 권장 두 클래스 상단 10 = 문턱의 2 배, D4) ③ ★★ **상한의 두 번째 형태**: `[인쇄]` 고정 고압 → "creep and stress relaxation … **fatigue-driven micro-crack initiation** … gradually degrading interfacial contact" — 5호의 단락 상한(시간 ~h)과 **다른 축**(피로, ~년) ④ ★★ **압력 = 제어변수 + 정책**: `[인쇄]` "apply higher pressure during high-rate cycling … reduce pressure during extended rest periods or as the cell ages"(8호 "coupled state/control variable" + 정책) ⑤ 요구치 계보 세 번째: 8호 `<≈1`(Xu 2024) · 12호 `0.4–1`(Tian/Shao) · **13호 `<5`** — **원전 셋 다 다르고 자릿수 같음**; 실험실 창 2–490 MPa 은 셋 다의 위. ⚠ **압력→용량 · 스윕 · 이력 · 계측 전부 0** | **해당 없음.** Si 계 음극 권장. `dead li`·`isolated` 0 · `plating` 2(그리드 주파수조정 "resistance to lithium plating" · Table 2) | **★ 부분 — 처방과 경고, 곡선 0 장.** ① 양극 권장 **LFP / LFMP**(저전압 → 계면 열화 최소) ② `[인쇄]` "**flat voltage profiles** … (e.g., LFP cathodes) exhibit minimal voltage change over large SOC ranges" ③ ★ **운전 창 절단**: `[인쇄]` "**20–80 % SOC** … **impossible to obtain a full OCV curve** for calibration" ④ `[인쇄]` "distorted by **voltage hysteresis arising from mechanical stresses**"(인용·크기·전극 0, G6) ⑤ 음극 권장 **Si 계**(비평탄·이력 OCP — 논의 0, G10). `OCV` 1 회 · `GITT`·`dV/dQ`·`half-cell` 0 · **V–Q·OCP 0 장**. ★ 닻 "모르는 것 5"(LFP 평탄 → `(X1, X3)` 축퇴)가 그리드에서 **설계 권장 + 운전 창 절단 + 응력 이력** 세 겹으로 강화되고, "전고체 음극 = 평탄" 전제는 **세 번째로**(9호 Li-Si · 11호 graphite 에 이어 **설계 처방으로서**) 깨진다 |

| **★★ Oh, Kim, Kim, An, Kwon, Choi 2025 (`assb` 14호 — 첫 **열역학 도함수 진단** · 서울대 + **HMG-SNU JBRC(현대차)** · *Angew. Chem. Int. Ed.* 64, e202514910, **Hot Paper** · 실험 논문 + **SI .docx(진짜 SI, 표 0)** · ⚠ 자기 인용 21/74)** | **★ 있다 — 두 층위.** ① XRM 공극률 `[인쇄]` **4.5 → 9.8 vol%**(10 MPa, 50 cy) · **4.4 → 5.3**(20 MPa) — 4호 Shi 의 void vol%(2.87 → 9.50 @50 cy)와 **같은 종류·같은 자릿수** ② ★ **계보 최초의 비파괴 in situ 대리량** `F(dE/dP)_T` = `[인쇄]` **42.7 → 34.7 µJ mol⁻¹ Pa⁻¹(−18 %)**, 3 셀 `[도표]` 18.1–20.3 %. ⚠ 무차원 `θ` 아님 · 공극률→`dE/dP` 사상 **2 점** · `[재현]` **`dE/dP` 가 압력 구간에 2 배 의존**(0.44 mV/MPa @5–10 ↔ 0.23 @10–20, 신품끼리; 논문 무언급) · `LAM` **0 회** → **접촉 손실 = LAM 안/밖: 미언급** | **★★ 있다, 셋 — 그러나 가르는 쌍이 다르다.** 엔트로피메트리 `ΔS = −F(dE/dT)_P` · volumetry `ΔV = F(dE/dP)_T` · XRM/SEM. 주장은 `[인쇄]` "distinguish between **mechanical and chemical** degradation" — **`LAM_PE` ↔ 접촉 손실은 물음 자체가 없다.** ★★ 그리고 `[인쇄]` ΔS 는 "local physical **contact loss** … **as well as** an increase in the **interfacial resistance**" 를 **한 신호로** 받는다고 스스로 정의 ⇒ **ΔS 채널은 우리 쌍을 합친다.** 교차 실험 0(화학 단독 대조군 0 · 20 MPa 셀 엔트로피메트리 0). ★★★ 실익 = `[인쇄]` **void +5.3 %p 인 셀(86.0 %)과 +0.9 %p 인 셀(84.0 %)의 용량이 같다(역상관)** — 접촉 손실이 이 창에서는 **겉보기 `LAM_PE` 로 나타나지 않는다** | **measured-morphological**(XRM "window leveling" 문턱, 복셀·정확도 0) + **measured-thermodynamic**(ΔS drop `[도표]` 13–15 → 5.8–8 J mol⁻¹ K⁻¹ · volumetry drop 18–20 %; n = 3, **오차 막대 0**). ★ **"health" 등급(reuse/recondition/recycle)의 문턱값 0** — `[인쇄]` "quantitative metrics … requires analyzing many cells … currently difficult". 적합 라벨 0(`fit*` 0). ⚠ `[도표]` Fig. 3c "after" 곡선이 S2 세 셀 어느 것과도 끝점이 다르다(D2) | **0 (14/14 편) — 성질이 또 다르다: 역문제가 없다.** 관측이 **직접 열역학 도함수**이고 적합이 없으므로 조건수·프로파일이 **정의될 자리가 없다**; 대신 **귀속이 가정**이다(ΔS 변화 → "비균질", `dE/dP` 감소 → "void"), 대안 원인(재료 변화 · 음극 상수항 · 이완 · 압력 비선형) 배제 시험 0. `identifiab*`·`uncertaint*`·`error bar` **0**. ★ `[재현]` **sum rule 위반 후보**: 비균질은 OCV 축을 뭉갤 뿐 SOC 축 적분을 못 바꾸는데 `[도표]` 전 곡선 평균 ≈ −3.5 ↔ 후 ≈ +1.5 — 논문은 이 뺄셈을 안 한다 | **해당 없음(Li 금속) → 그러나 남는다.** `[인쇄]` "Li metal anode, whose potential can reasonably be assumed to remain constant" → 전부 양극 귀속. `[해석]` 식 (6)·(10) 의 음극항은 **상수 ≠ 0**(S°(Li) 29 J mol⁻¹ K⁻¹ · **V_m 13.0 cm³ mol⁻¹** — `[재현]` 이 항만으로 5 MPa 에 **0.67 mV**, 실측 2.2 mV 의 30 %); "10 MPa → Li creep → pore 무시" 는 pore 항 논거이지 상수항 논거가 아니다. 100 사이클 뒤 음극 계면 기여 미검토 | **★★★ 있다 — 이 계보에서 가장 새로운 형태: 압력이 관측 변수다.** 제작 100/350 MPa · 운전 **10 / 20 MPa** · 진단 **ΔP = −5 / −10 MPa (≤0.01 MPa)** · 처방 **>300 MPa**(**미수행**, 4호 미인용, Li 금속 셀에 5호 상한의 4 배). ① ★ **압력 → OCV 기울기 = 계보 최초의 `E(P)`**: `[인쇄]` 2.2 mV/5 MPa · 2.3 mV/10 MPa(**비선형, 오목**) ② 압력 → 공극률 2 점(9.8 / 5.3 %) ③ **압력 → 용량 2 점**(86.0 / 84.0 % — 역상관) ④ `[도표]` S16 재가압 뒤 **+0.4 mV 비가역 오프셋 + 감압 중 +0.5 mV 표류** = 노화 신호와 같은 자릿수(5호 이력의 그림자) ⑤ 20 MPa Li 금속 셀 `[재현]` ≈225 h 사이클에 단락 보고 0(5호 190 h 와 대조 — 설계·전류 다름). ⚠ 로드셀 명시 0 · 스윕 0(2 구간) | **해당 없음**(Li 금속). `dead li`·`isolated`·`plating` 0. CE `[도표]` S1 첫 사이클 ≈85 %, 이후 ≈98–99 %(눈금 20 %p) | **★★★ 있다 — 계보 최초로 ASSB 실셀의 OCV 축 위에 열역학 도함수를 준다.** LiNbO₃-**NCM811** / LPSCl / Li, **2.5–4.3 V**, 기울기 있음. `[도표]` ΔS(OCV) 3.53–4.25 V ≈28 점(5 % SOC 간격) + dQ/dV(OCV) 봉우리 **3.60 / 3.73(H1→M) / 4.00 / 4.18 V** 신품 → 후 3.75 + 둔덕 4.05. ⚠ **SOC 축 없음** — `E(x)` 곡선은 여전히 0 장. 접촉 손실 = LAM 안/밖: **미언급** |

| **Rahman, Lu 2024 (`assb` 15호 — 첫 **학회 회의록** · South Dakota State Univ. (Construction and Operations Management) · *Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085 · ⚠⚠ **6 쪽 · 1차 측정 0 · 재인용 수치도 0 · 본문 그림 1 장(타 논문 재수록) · 표 0 · 식 0**)** | **없다 — 계보에서 가장 없다.** `contact` **0 회**(낱말 자체가 논문에 없다) · `percolat*`·`θ` 0 · `capacity` **0 회** · `LAM`·`LLI` 0. ASSB 기하 어휘는 `tortuos*` **1 회**가 전부이고 그것도 ref [28](Bielefeld 2020 바인더 편) 요약 안이다 | **없다.** 1차 측정 0, 인용된 관측 수단도 0 (`EIS`·`impedance`·토모·XRD 전부 **0 회**). ⚠ **Figure 1 에는 "Impedance models" 가 있는데 본문에 0 회** — 그림이 **액체셀 종설(ref [16] Zou 2023)의 재수록**이라 본문보다 넓다 | ★ **`simulated` — 그리고 그것이 확인 가능한 유일한 라벨이다.** 이 편 전체에서 SSB + ML 인용은 ref **[22]**(Asheri 2023) 한 편이고 `[인쇄]` "data-driven multiscale **simulation** framework … focusing on **interface damage**". 자기 라벨 0 · 데이터셋 0 · `experiment*`·`measur*` **0 회** · 오차막대 0 | **없다 (0/15) — 성질이 여덟 번째다: 추정기 자체가 없다.** `identifiab*`·`uniqueness`·`condition number` **0 회**. 14호가 "역문제가 없어 조건수 자리가 없음" 이었다면 **15호는 RUL 추정기가 없어 역문제를 말할 대상이 없다.** ⚠ 그런데 `accuracy` **7 회** — **정확도 수치 0 · 불확실성 표기(`RMSE`·`MAE`·`error bar`·`uncertainty`) 0** | **없다.** `indium`·`Li-In` 0. 음극은 §4.1(나)의 "lithium-anode" 2 회뿐 | **없다 — `pressure` 0 회.** ⚠ 초록이 `[인쇄]` "sensitivity to various **operational** and environmental conditions" 를 약속하고 ASSB 운전 조건의 첫째(스택 압력)를 **낱말로도 쓰지 않는다** | **없다.** `dead`·`isolated`(본문)·`dendrit*` 0 | **없다.** `NMC`·`LFP`·`LCO` 0 · OCP 곡선 0. `OCV` **1 회**는 ref [17](Dang 2016, 액체셀)의 **SOC 대리 변수**로서 — **열화 모드와 연결되지 않는다** |

| **★★ Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling 2026 (`assb` 16호 — 첫 **3전극 실측** · 첫 **압력 본체 1차 측정** · Univ. Marburg (mar.quest) · *Batteries & Supercaps* 9, e70315 · ⚠ **열화 0 — `degrad*`·`aging`·`SOH`·`LAM`·`LLI` 전수 0회, 전부 신품 2번째 사이클**)** | **없다 — 그리고 "없다" 의 형태가 계보에서 가장 날카롭다.** `contact loss`·`percolat*`·`θ`·`void` **0 회**. `contact` 8 회는 전부 정성. ★★ 그런데 **식 (4)가 접촉 면적의 자리를 만들고 값을 1 로 못 박는다**: `[인쇄]` "**The area of the CAM particles in contact with the SE** normalized to the cathode volume is given by" `a_V = 3·ε_CAM/r_CAM` — **완전구 기하 면적, 접촉 분율 인자 없음**. ⇒ `θ_AM ≡ 1` 을 **이름을 붙인 채** 가정한 첫 편 | **★★ 있다 — 이 계보 최초의 전극 분해 관측.** ① **리튬화 Au/W μ-RE 3전극**(∅25 µm, 5 µA/30 min) → 양극·음극 임피던스 분리 ② **양극 두께 5 점 스윕**(26–219 µm) = TLM 의 여기 ③ **압력 2 점**. ★ **자기 검증이 있다**(계보 최초): `[인쇄]` 2E 완전지 = 3E(양극+음극) 합이 **10 kHz 아래에서 일치**. ⚠ 단 **열화가 아니라 신품 상태의 분해**이고 `LAM_PE` ↔ 접촉 손실을 가르는 데 쓰이지 않는다 | **fitted — 층위가 하나 더 깊다.** `j₀`·`τ`·`D_CAM`·`Q_DL`·`β` 가 `[재현]` **자유 파라미터 35 개 동시 적합**(공통 5 + R‖CPE 2×3×두께 5)의 출력. 고정 가정 8 개(`a_V`·`ε_SE`=0.505·`ε_CAM`=0.495·`σ`=0.47 S/m·`r_CAM`=2.5 µm[ref 30]·`dU/dc`=−3.48e−5·T·A) 가 **두 압력에 동일**. ⚠ `σ` 는 **97 MPa 에서만** 쟀다. **오차막대 0 · 반복 0 · 조건당 셀 1 · 잔차/상관 0 · 데이터 on request** | **없다 — 0 / 16.** `identifiab*`·`uniqu*`·`uncertaint*`·`condition number`·`error bar`·`confidence` **전수 0 회**. ★★ **아홉 번째 성질이고 처음으로 "축퇴를 실제로 밟으면서 모르는" 형태다**: 식 (4)+(5)에서 `R_semicircle = R·T·r_CAM/(3·F·**j₀·ε_CAM**·d)` ⇒ 데이터가 보는 것은 **`j₀ · ε_CAM / r_CAM` 한 조합**인데 뒤 둘을 고정해 **전부 `j₀` 로 읽는다**(0.74 → 1.33 A m⁻²). **9호에서 인쇄된 식으로 보인 곱 축퇴가 여기서는 실측 논문의 배정 선택으로 나타난다** → [[assb-lampe-contact-product-degeneracy]] | **★★★ 계보에서 가장 많이 준 편 — 네 겹.** ① **기준극이 Li–In 이 아니다**: 리튬화 **Au/W μ-RE**. ② **그 전위 안정성을 재지 않는다** — `stable` 3 회 중 **2 가 남의 논문**(Zhang LTO-RE 1.57 V · Hertle μ-RE 0 V), 자기 셀 검증 0. ③ `[도표]` **Fig. S1 리튬화 곡선에 평탄부가 없다** — 2.5 µAh 동안 **560 mV 표류**. ④ ★★★ `[도표]` **Fig. S3 의 In–Li 평탄 전위가 두 셀에서 0.58 V ↔ 0.47 V, ≈0.11 V 어긋난다** (둘 다 2상역 `x_Li` 0.18/0.14, `[재현]` 과전압 ≈5 mV 로 설명 불가, **논문 무언급**). ⑤ ★★★ **그 평탄 구간 안에서 음극 DRT 봉우리가 `[도표]` 18.6 → 1.2 (≈15 배) 움직인다** — **평탄 OCP 가 숨기는 양이 여기 있다** | **★★★ 본체다 — `pressure` 49 회(계보 최대, 13호 24 를 넘는다).** 제작 **389 MPa/3 min**(분리막 선압축 97), 운전 **97 / 389 MPa** = **계보 운전 압력 최댓값**(5호 Li 금속 상한 75 MPa 의 **5.2 배**, ⚠ 화학 다름). ★ **제작 = 운전인 첫 표본** — 6호가 쪼갠 두 축을 붙인다. ① **압력 → 임피던스 1 차**: 완전지 반원합 `[인쇄]` **23 → 11**(389) / **85 → 23 Ωcm²**(97), 3E 양극 **10 ↔ 20**, 음극 **4 ↔ 9 Ωcm²** ② **압력 → 공극률** `[인쇄]` **11.2 %(389) ↔ 12.9 %(97)** — 4 배 가압에 **1.7 %p** ③ ★★ **압력 → 용량이 SI 그림에만** `[도표]` 1 사이클 방전 **+9 … +59 %**(본문 `capacity` **1 회** = 서론). ⚠⚠ **스윕 아님(2 점) · 이력 0(`hysteres*` 0회) · 같은 셀 재측정 0 · 로드셀 시계열 0**. ★ 그리고 **두 점 다 389 MPa 제작 뒤라 97 MPa 은 필연적으로 하강 분기**인데 논문이 그 사실을 말하지 않는다 | **해당 없음.** In 음극. `dead`·`isolated`·`dendrit*` 0 회 | **★★ 있다 — 계보 최초로 `dU/dc` 를 숫자로 준다.** 단결정 **NMC 83|6|11**(3–6 µm, LiNbO₃ 1 wt%) + **Li₅.₃PS₄.₃ClBr₀.₇** + **In/InLi**, 70:30. 완전지 컷오프 **2.7–3.7 V vs In/InLi**, `[도표]` 양극 **3.2 → 4.25 V vs Li/Li⁺** 전 구간 기울기 있음. **`dU/dc_Li` = −3.48·10⁻⁵ V m³ mol⁻¹** (`[도표]` c ≈16 500–42 700 중 **23 000–30 000 국소 선형화**, 충·방전 **평균**을 평형 대리로 — 0.1 C pseudo-OCV). ★ **음극 OCP 완전 평탄**(0.47–0.58 V): 닻의 "ASSB 음극 = 평탄" 전제를 **In 계에서 실측 확인한 첫 표본**이고, **동시에 그 평탄함이 15 배 임피던스 변화를 숨긴다는 것도 보인다**(Q5 ⑤) |

| **★★★★ Yanev, Heubner, Nikolowski, Partsch, Auer, Michaelis 2024 (`assb` 17호 — 이 계보에서 **Q5 를 본체로 삼은 첫 편** · 두 번째 3전극 실측이자 **첫 전위 채널** · Fraunhofer IKTS + TU Dresden · *J. Electrochem. Soc.* 171, 020512, **Editors' Choice, CC BY** · ⚠ **열화 0 — 최대 5 사이클, `LAM`·`LLI`·`SOH`·`aging` 전수 0회**)** | **없다 (17/17) — 형태가 새롭다.** `contact surface` **1 회**가 `[인쇄]` "the Li depletion is primarily a function of the **contact surface between the SE and LiIn**" 로 **인과 변수를 지목**하고, `contact area` **1 회**가 `[인쇄]` "high **effective contact area** to the separator" 로 **처방의 근거**가 되는데 **값·단위·측정법이 0**. ★ 9호=적합(0.4938) · 16호=기하로 계산해 1 로 못 박음(θ≡1) · **17호=이름만**. ⚠ 그리고 이것은 **양극이 아니라 음극/분리막 계면**의 접촉이다 — 축이 다르다 | **★★★ 있다 — 계보 두 번째 전극 분해, 그리고 첫 "전위" 채널.** 16호가 임피던스를 전극별로 갈랐다면 17호는 **전위를 전극별로 가른다**(`E_WE`·`E_CE`·`E_cell` 시계열, Li 금속 RE). ★★★ **결정적 대조: 양극 임피던스가 두 음극에서 `[재현]` ≈31 ↔ ≈32.5 Ω (5 % 차)로 같다** ⇒ 용량·율 차이가 **전부 음극**. ★ 우리가 한 합산 검사 `[재현]`: `Z_WE/CE ≈ Z_WE/RE + Z_CE/RE` 가 **2 Hz 에서 두 셀 다 1 % 안**(HF 절편은 foil 만 7 % 어긋남) — **논문은 이 자기 검증을 하지 않는다**. ⚠⚠ **형태학·화학 관측 0** — XRD·EDS·XPS·**단면 SEM·post-mortem 전수 0**, Fig. 2 광학 사진 2 장이 전부 | ★★ **새 층위: `measured-potentiometric`.** 적합(9·16호)도 형태학(4·14호)도 열역학 도함수(14호)도 역변환(11호)도 아닌 **기준극 대비 전압계 판독**이다. ⚠ 오차막대 0 · 반복 0 · 조건당 셀 1(총 12) · `n =` 0 회 · 데이터 가용성 문장 0. ⚠⚠ **기준극 자체가 검증되지 않았다** — RE 는 LPSCl 안에 도금한 **Li 금속**인데 같은 논문 서론이 `[인쇄]` Li 금속의 "high reactivity towards sulfide SEs" 를 적는다. ★ 단 `[재현]` **합의 상한 ≈20 mV / 20 h** (복합 셀 `E_CE` 가 0.61–0.63 밖으로 안 나감) = **계보 최초의 기준극 표류 상한** | **없다 — 0 / 17. 열 번째 성질: "인쇄로 사양했다".** `identifiab*`·`uniqu*`·`uncertaint*`·`condition number`·`error bar`·`confidence`·`n =` **전수 0 회**. ★★ 그리고 **적합 어휘 자체가 0** — `fit*`·`equivalent circuit`·`ECM`·`CPE`·`capacitance`·`DRT` **전수 0**, `[인쇄]` "Detailed quantitative analyses and **modelling of the impedance spectra are beyond the scope of this study**". 계보: 안 쟀다(1–7) → 이름만(8) → 지문이 자기 표에(9) → 분야가 명제로(10) → 재료만(11) → 0(12·13) → 역문제 없음(14) → 추정기 없음(15) → 밟고 지나갔다(16) → **17호: 역문제가 눈앞에 있는데 지면이 명시적으로 사양했다.** ★ 그리고 **그 사양이 결론을 방어한다** — 결론은 적합의 출력이 아니라 **전압계 판독**이라 축퇴할 자리가 없다(14호는 귀속이 **가정**이었고 17호는 **배선**이다). ⚠ 단 그 배선에도 오염원 둘(옴 · RE 안정성)이 있고 **논문은 둘 다 안 다룬다** | **★★★★ 이 계보에서 가장 크게 채워진 칸이고 이 편의 본체다** → [[assb-li-in-reference-potential-window]]. `[인쇄]` 0.62 V 는 **인용값**(ref 26 Santhosha 2019 쿨로메트릭 적정)이고 **개방회로 실측이 0 회**(G1). 실측: 0.1 C **0.61(충전)/0.63(방전)** · 0.1 C 방전 종료 **foil `[도표]` ≈1.0 V** (논문 수치 없음) · CA 정상 **복합 0.64 ↔ foil `[인쇄]` 1.30–1.40** · 과리튬화 **≈0.42**. **전체 폭 0.42 → 1.40 V ≈ 0.98 V.** ★★★ 우리 옴 분리 `[재현]`(CE–RE 절편 `[도표]` foil ≈28.7 Ω, A = 1.131 cm²): 0.1 C **9.1 mV = 관측 편차의 ≈100 %** · CA 초기 **0.52 V = 76 %** · **CA 정상 ≈1.8 mV = 0.2 %** ⇒ **+0.73 V 는 과전압이 아니다.** ⚠ "평형 전위" 는 `[해석]` — **CA 후 이완 곡선을 안 쟀다**(G2) | **한 점.** 운전 `[인쇄]` **ca. 50 MPa**(2E) / **50 MPa**(3E), 제작 **500 MPa**(3E 분리막만 **375**). `pressure` 7 · `MPa` 13 · `stack pressure` 2 · **`hysteres*` 0**. **스윕 0 · 이력 0 · 계측 0 · 압력→용량 0 · `E_CE(P)` 0.** ★ 유일한 개념 기여가 **부정적**이다 — Wang et al.(ref 28, `[인쇄]` **14.3 at% Li 가 최적**)과의 정면 충돌을 `[인쇄]` "considerably higher rates and **lower stack and assembly pressure**" 로 넘기면서 **상대 압력값도 자기 스윕도 없다** | **해당 없음** (Li-In 음극). `dead`·`isolated` **0**. `dendrit*` **2** 는 Li 금속을 **피하는 사유**로만 | **★ 있다.** **단결정 NCM811** : Li₆PS₅Cl : VGCF = **73.2:24.0:2.8 wt%**, `[재현]` **19.1 mg cm⁻² · 2.80 mAh cm⁻² · 공칭 200 mAh g⁻¹**(역산 정합 ✔, 1 C = 2.80 mA cm⁻²). 창 **3.00–4.30 V vs Li⁺/Li (2.38–3.68 vs LiIn)**, `[도표]` **전 구간 기울기 있음**. ★ **V–Q 곡선 11 장**(Fig. 1a–c 10 + Fig. 4a) — 10·11호가 0 장이던 칸. ⚠ **`OCV`·`GITT` 0 회** — 곡선은 전부 0.1 C pseudo-OCV. 접촉 손실 = LAM 안/밖: **미언급** |

| **★★★★ Fukunishi, Tabuchi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023 (`assb` 18호 — 첫 **전극 분해 + 열화 동시** · 첫 **컷오프를 작업전극 전위에** · 첫 **K–K 검증** · Tokyo Tech + NEDO SOLiD-EV · *J. Power Sources* 564, 232864 · **16호가 지목한 유일한 외부 실측 대조군**)** | **★ 부분 — 계보에서 가장 가까이 갔다가 돌아선다.** ① `[인쇄]` **Image-J 로 SE\|활물질 접촉 면적을 실제로 쟀다**(계보 최초의 **이미지 기반 접촉 면적 측정**) — 그러나 값은 **입자 크기 두 시료의 비 2.0** 하나뿐이고 절대 면적·분율·오차·임계값 0(G6), 원자료 두 장은 **배율이 다르다**(D1: 캡션 "×2500" ↔ 스탬프 2500x/1000x, 15↔10 kV). ② 식 (4) `S_w = 3M/(dr)` 는 **완전구 기하 면적**이고 `[인쇄]` "**completely immersed**" 로 **접촉 분율을 소거**한다 — **16호의 `a_V = 3ε/r` 과 같은 자리·같은 수법**. ③ ★★★ **노화 축 `θ` 는 또 0** — 이번에는 **도구(Image-J)와 시편(Fig. 6·7)이 둘 다 지면에 있는데도**. ④ ★★★★ 말로는 가장 멀리 간다: `[인쇄]` "insulative layers **completely cover** the active material to make the particle **inactive**, such **dead particles** … no contribution to the charge transfer process. This could explain the **large capacity decrease**" = **`θ_AM` 의 기구 서술**, **값 0** | **★★★ 있다 — 계보 세 번째 전극 분해이고 열화를 동반한 첫 편.** ① **R-LTO 메시 3전극**(전극별 임피던스 **+ 전극별 충방전 곡선**) ② **입자 크기 스윕 2점**(= **면적 여기**) ③ **온도 3점**(Ea) ④ **SoC 5점** ⑤ **Al\|복합체\|Al 전자차단 대칭셀**(R2 귀속의 독립 근거) ⑥ **단면 FE-SEM + EDX 원소맵 노화 전후** ⑦ **전해질 2종 대조**. ★ `[인쇄]` **2전극 = 3전극 합** 자기 검증도 있다(⚠ 중주파에서 ≈13 %·≈60 Ω 어긋난다 — D10). ⚠ **`LAM_PE` ↔ 접촉 손실을 가르는 데 쓰인 조합은 0** — 접촉 면적은 **신품 입자크기 축에서만** 쟀다 | **fitted — 층이 하나 더 깊다.** 열화 라벨 = `R1..R4` 등가회로 적합값이고, **회로의 차수와 시상수가 DRT 에서 오고 DRT 는 λ 가 정한다**(`[인쇄]` "the time constants obtained from the DRT … were **fixed** and the other parameters were refined"). ★ **단 계보 최초로 ± 를 인쇄한다**(Table 1 의 Ea 4개 × 4조건, Table S1 의 `R3`·`p`) — ⚠ 3점 회귀·단일 적합의 표준오차이고 **셀 간 반복이 아니다**(`n =` 0회). ⚠ **`CPE2-C` 와 `τ3` 에만 ± 가 없다** = **우리 검사가 쓰는 바로 그 값**. ★★ 그리고 **용량 축은 fitted 가 아니다** — 0.1 C RPT 실측이고 **컷오프가 작업전극 전위**라 상대극 오염이 없다 | **0 / 18. ★ 열한 번째 성질 = "축퇴를 'A 또는 B' 로 인쇄하고 가르지 않는다".** `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·`error bar`·`n =` **전수 0회**(NFKC·대소문자 구분; `flam*`·`Soh` 오검출 0 확인). 그런데 `[인쇄]` "**the chemical composition at the interface or the contact area** between the NCM523 and electrolyte particles changed" 는 **우리 닻 물음의 두 항을 이름으로 나란히 적은 문장**이다. ★★ 그리고 **가를 입력을 자기 지면에 갖고 있다** — **9호가 "지문이 자기 표에" 였다면 18호는 "해답이 자기 표에"** 다 (Table S1 이 `R3`+`CPE2-C`+`p` 를, Fig. 5 가 노화 전후 `R`과 `τ` 를 함께 인쇄) | **★★★ 있다 — 성질이 세 편 중 가장 다르다.** ① **기준극이 Li-In 이 아니다**: **R-LTO**(부분환원 Li₄Ti₅O₁₂) 메시, `[인쇄]` 전위 **1.55 V vs Li/Li⁺ 를 가정** ⇒ **Li-In 이 처음으로 "기준" 이 아니라 "피측정 전극"** 이 된다. ② `[도표]` **Fig. 1(b)(d): 두 전해질계 모두 0.1 C 전 사이클에서 Li-In 이 완전 평탄 ≈0.60 V**(판독 분해능 ≈±30 mV — 17호의 ±10 mV 보다 좁게는 못 잰다). ③ ★★ `[재현]` **평탄한 이유가 설계에 있다**: `x_Li` **37.7 → 40.0 at%**, 재고비 **9.5배**, 전류밀도 **0.054 mA cm⁻²** = 17호 0.1 C 의 **1/5** · 17호 CA 의 **1/300** ⇒ **17호와 모순이 아니라 반대편 끝의 표본**. ④ ⚠ 기준 축이 **R-LTO 의 가정된 1.55 V** 로 옮겨갔고 자기 셀 검증 0, 안정성 근거가 `[인쇄]` **K–K 잔차**라는 **범주 오류** | **★ 거의 없다 — "없음" 의 형태가 가장 날카롭다.** `pressure`·`stack pressure`·`hysteres*` **본문 0회**, `MPa` **2회**(제작 **110 MPa** · 대칭셀 **150 MPa**). **운전 압력은 값도 장치도 문장도 없다** — 셀은 PET 관에 눌러 `[인쇄]` "Ar-filled polystyrene container" 에 넣는다. ⚠⚠ **그런데 이 편의 두 열화 기구 중 하나가 `void formation`**(`void` **7회** — 실측 편 최다)이고 LPSCl 의 R1′ 반원도 void 로 설명된다 ⇒ **압력에 가장 민감한 양을 주인공으로 삼으면서 압력을 통제하지 않은 첫 실측 편.** 비교: 16호 49회 · 17호 7회 · **18호 0회** | **해당 없음** (Li-In 음극). `dendrit*` 0. ⚠ **`dead` 1회는 음극이 아니라 양극이다** — `[인쇄]` "such **dead particles**"(절연층에 덮인 NCM 2차 입자). **낱말은 같고 대상이 다르다** | **★★ 있다 — 계보 최초의 조합.** **LiNbO₃ 코팅 NCM523**(D50 **5.0 / 11.2 µm**, 다결정) + **LPSI**(2.6 mS cm⁻¹) 또는 **LPSCl**(1.8 mS cm⁻¹) + **Li-In**. ⚠ **두 계의 복합양극 조성이 다르다**(49:43:8 ↔ 69:26:5 wt%) — 전해질 비교 전체가 교락. `[인쇄]` 창 **2.40–4.20 V vs Li/Li⁺**, 평탄 ≈3.7 V 뒤 전 구간 기울기, 0.1 C **140–150 mAh g⁻¹**(공칭 160), `[재현]` 로딩 **3.7–5.2 mg cm⁻²**(계보 최박). ★ **V–Q 곡선 6장**(양극 4 + **음극 2**) · ★★ **`R3(SoC)` 5점**(Fig. 2c: 180→80→60→57→60 Ω) = 계보에서 가장 조밀한 양극 전하이동 저항의 SOC 곡선. ⚠ `OCV`·`GITT` 0회 |

| **★★★★ Yoshida, Ikezawa, Okajima, Arai 2024 (`assb` 19호 — 첫 **4전극** · 첫 **기준 전위를 소거하는 설계** · 첫 **전극이 하나도 없는 편** · Tokyo Tech, **18호와 같은 계보** · *Electrochim. Acta* 497, 144523 · **CC BY**)** | **없다.** `contact area` **2회** · `contact loss` 1회(서론, 인용) · `θ`·`percolat*`·`porosit*`·`tortuos*` **0회**. ★ 접촉 면적이 인과로 불려 나오는 자리는 **하나**다: `[인쇄]` 압력 효과를 "possibly due to the **increases in the contact areas** of SE particles and SE pellets" — **값 0**. ⇒ **`R(P)` 는 있고 `θ(P)` 는 없다** (18호의 `R(N)` ↔ `θ(N)` 과 같은 모양) ⇒ **`assb` 19/19 편이 `θ` 를 어떤 상태축 위에서도 주지 않았다** | **해당 없음에 가깝다 — 활물질이 없다.** 채널은 많다(4전극 배선 · 단면적 `S` 3점 · RE 간격 `d` 4점 · **계면 유무 대조** · Li-In 3전극 임피던스 · 압력 2점 · 온도 4점) 그러나 **`LAM_PE` ↔ 접촉 손실을 가르는 데 쓰인 조합은 0**(가를 대상 자체가 없다). ★★★★ **대신 설계 형태를 준다 — 계보 최초의 "같은 재료 · 같은 공정 · 계면 하나만 추가" 대조군**(Fig. 7: LPSCl 단일 펠릿엔 `P2` 없음 → LPSCl\|LPSCl 적층엔 `P2` 생김, `[도표]` ≈8 Ω). **18호 검사 A 가 실패한 자리의 대안 설계**다 | **fitted(등가회로) + measured(Nyquist).** ± 는 **4점 Arrhenius 회귀 표준오차**뿐, 셀 간 반복 0(`n =` **실질 0회** — 정규식이 "Li: **In =** 25:75" 를 1건 오검출). ★★★★ **그런데 이 편이 스스로 산포 하한을 드러낸다**: `[도표]` LPSCl\|LPSCl 셀의 `Ea(R1)` = **45.5 ± 0.1** ↔ 같은 물질 Table 1 벌크 **40.5 ± 0.3** (`R1` 은 정의상 벌크뿐) ⇒ **5.0 kJ mol⁻¹ = 인쇄된 ± 의 12–50배, 논문 무언급**(D10). 저자 스스로 `[인쇄]` **성형법(냉간↔열간)이 `Ea` 를 11 kJ mol⁻¹ 움직인다**고 적는다. 다른 산포 둘: **Li-In 전극 임피던스 39↔172 Ω(4.4배, n=3)** · `[인쇄]` **`P3` 가 셀마다** — `[도표]` 4.8 Ω ↔ ≈35 Ω(**7배**) | **0 / 19. ★ 열두 번째 성질 = "어휘 없이 귀속을 실험으로 물었고, 설계의 절반이 판별력이 없다".** `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·`error bar`·`n =` **전수 0회**(NFKC·대소문자 구분; `[Ll]am[a-z]+`·`Soh\w*` 오검출 0 확인). ★ **성분의 정체를 적합 통계가 아니라 기하 섭동으로 묻는 첫 편**(단면적·RE 간격·계면 유무). ⚠ 그러나 ① **`1/S` 축은 벌크도 계면도 똑같이 스케일해 못 가른다**(논문도 `[인쇄]` "pellets **or** at the interface"), ② 결정적인 `d` 축이 **4점이고 하나가 4.5배 이상치**다 — `[도표]` `R2/d` = **17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹**, **이상치를 빼면 `R1`(1.12×)만큼 깨끗이 `d` 에 비례**(1.10×)해 **결론이 뒤집힌다**, ③ 적합 자체의 유일성(조건수·근최적 폭·다중 출발)은 **0**. ★★★★ **다만 비분리를 자기 데이터로 증명한 첫 편**: `[인쇄]` Li-In 전극 반원이 **P1(>1 kHz)·P2(1 kHz–0.1 Hz) 둘 다와 겹쳐** "**P1 and P2 are difficult to extract** from the … two-electrode system" | **★★★★ 있다 — 성질이 네 편 중 가장 다르다: 재지도 가정하지도 않고 *소거한다*.** ① 측정량이 `[인쇄]` **RE₂ − RE₁** 이라 R-LTO 의 절대 전위가 **상쇄된다** ⇒ `assum*` **0회**, "**1.55**" **0회** — **18호의 G4 가 생기지 않는다**. `[인쇄]` Fig. S1: 4전극은 "without the polarization of the **two counter electrodes**", 3전극은 **WE 분극 포함**, 2전극은 둘 다. ② ★★★ **새 바닥이 인쇄된다**: RE–RE 개방회로 **−4 / −5 / +25 mV**, `[인쇄]` "within the **reproducibility of the reference electrode potentials (ca. ±30 mV)**" = 계보 최초의 기준극 재현성 숫자 **이자 검출 하한**(⚠ **근거 미제시** — ref [18] Ikezawa 2020 에 있을 것). ③ ★★ **R-LTO 조성이 처음 인쇄된다**: **Li₇Ti₅O₁₂:Li₄Ti₅O₁₂ = 67:33 mol%**(2상 한복판) — 18호의 "partially reduced" 공백 절반 해소. ④ ★★★★ **Li-In 상대극의 비평탄을 4전극이 직접 찍는다**: `[인쇄]` "The potential change in the counter electrode is **not linear** … **asymmetric**" ⇒ **큐 메모의 출처 확정**. `[도표]` 200 s·≤0.7 mA CV 에서 `E_CE` **42 / 126 / 75 mV** 이동(`[재현]` **0.41–1.07 mA cm⁻²**), `[재현]` `ΔE/ΔI` = **44 / 221 / 83 Ω** = **같은 셀 계면 저항의 2–18배** ⇒ **"4전극이 더 재는 것" 의 정량 답**. ⑤ `[재현]` **(ㄱ)(ㄴ) 만족 · (ㄷ)만 깬 첫 표본**(재고 여유 **≈260배**) ⇒ **(ㄷ) 단독은 10⁻²–10⁻¹ V 대**, 17호의 0.7 V 는 **고갈**의 산물. ⚠ 이동이 **가역 분극**이라 17호의 **지속 이동**과 같은 양은 아니고, `[재현]` (a)의 42 mV 는 **CE–RE 옴(≈`R1`/2 ≈ 42 Ω)과 구별되지 않는다**. ⑥ ⚠⚠ **기준극 검증의 범주 오류는 그대로**: 18호 **K–K 잔차** → 19호 **진폭 비의존성**(선형성을 보지 기원을 보지 않는다) — **같은 그룹, 같은 구조** | **★★ 있다 — 계보 최저 압력대.** `pressure` **4회** · `kPa` **5회** · `MPa` 3회. 조립 `[인쇄]` **ca. 420 kPa**, 스윕 **560 / 840 kPa**(2점), 성형 **280 MPa**. ★ **8호가 인쇄한 산업 요구치 <≈1 MPa 안에 들어온 첫 편**(비교: 16호 97/389 · 17호 50 · 18호 미보고 · 5호 1–75 · 6호 2–4 MPa). ★★★★ **그리고 압력이 `R` 을 움직이고 `Ea` 를 안 움직인다**: `[도표]` 560→840 kPa 에서 `R1` **−6.5 %** · `R2` **−26 %**, `[인쇄]` "the **physical state of the interface does not affect the Ea** but the resistance values … **Ea as the essential parameter**" ⇒ **`Ea` 가 면적-불변 관측량**(곱 축퇴 처방의 새 채널). ⚠ 근거는 약하다 — **2점 · n=1 · 범위 1.5배**, `[재현]` **420 kPa 의 `R2`(21.5 Ω)가 560 kPa(≈24.7 Ω)보다 작아 추세와 반대**, 그리고 위 산포(≥5 kJ mol⁻¹)를 쓰면 **압력이 `Ea` 를 3 kJ mol⁻¹ 움직여도 못 본다** | **해당 없음** — Li-In 상대극이고 도금/스트리핑 실험이 없다. `dendrit*`·`dead`·`isolat*` **0회** | **해당 없음 — 전극이 없다.** 활물질·용량·V–Q **0**, `OCV`·`GITT` 0회, `degrad*`·`capacity`·`cycle life` **0회**. ★ 유일한 "개방회로" 는 **RE–RE 전위차**이고 `[인쇄]` **−4 / −5 / +25 mV** ⇒ **황화물 3종 사이에 검출 가능한 Li⁺ 활동도 차가 없다**(하한 ±30 mV). ★ 대신 물성을 준다: σ / `Ea` **3종**(LGPS 7.1 mS cm⁻¹ · 37±2 / LPSI 2.1 · 29.8±0.3 / LPSCl 1.8 · 40.5±0.3 kJ mol⁻¹) + **SE\|SE 계면 저항 4종**(LPSI\|LPSCl **21.5** · LGPS\|LPSI **12** · LGPS\|LPSCl **29.3** · LPSCl\|LPSCl `[도표]` **≈8** Ω)과 그 `Ea`(**41±3 / 27±3 / 42±1 / 39±2**) — `[인쇄]` **전부 낮은 σ 쪽 SE 의 벌크 `Ea` 와 같은 정도** |

| **★★★★ Chang, Choi, Kang, Park, Lim 2020 (`assb` 20호 — 첫 **매립형 기준극** · 첫 **전극별 전위 + 전극별 저항 동시** · 첫 **전극별 용량 손실 귀속** · **계보에서 시간이 가장 이르다(2019 접수)** · 창원대 + **RIST** + 세종대 · *Ionics* 26, 1555–1561, **Short Communication 7쪽, SI 없음**)** | **없다 — 0/20 유지.** `contact` 6회 중 **5회가 `contact resistance`**, `contact loss`·`θ`·`percolat*`·`tortuos*`·`porosit*`·`void` **전수 0회**. ★ 그래도 계보 최초의 **절대 Ω 예산 + 전극별 배분**이 나온다: `[인쇄]` σ = 1.8×10⁻⁴ S cm⁻¹ [12,26] ⇒ SE 자체 **448 Ω**, 측정 `R₀`(Cell) **810 Ω**, 차 **362 Ω** 을 *"layer-to-layer contact resistance"* 로 배정하고 `[인쇄]` **양극 쪽이 더 크다**(`R₀` 460 vs 355). `[재현]` **448 Ω 은 정확히 재현된다**(L=1240 µm, A=1.539 cm² ← `[도표]` Fig. 1a **⌀14 mm**) ⇒ 저자가 **In 박 110 µm 까지 SE 로 셌다**; 빼면 408 Ω ⇒ 접촉 몫 **402 Ω**(+11 %). ⚠⚠ **그러나 그 362 Ω 은 접촉이 아닐 수 있다**: 뺀 것은 분리막 슬래브뿐이고 남은 값에 `[도표]` **388 µm 양극 · 438 µm 음극 복합체 내부 이온 경로**가 통째로 들어 있다 — `[재현]` ε_SE=0.4·τ=2·평균 경로면 양극 복합체만 **≈350 Ω** ⇒ **접촉 없이 전부 설명된다**(G1 이 채워지면 확정). ⚠ 게다가 방향이 열화가 아니다 — 충전에서 `R₀` 가 **140 Ω 줄고** 이유는 `[인쇄]` *"not fully understood"* ⇒ **`R(방향)` 은 있고 `θ` 는 없다**, **20/20 편이 `θ` 를 어떤 축 위에서도 안 준다** | ★★ **+0.5 — 계보 최초의 *전극별 용량 손실 귀속*.** 관측은 **단일 정전류 스텝의 3시상수 분해**(`R₀` 순간 / `R_ct` 비선형 / `R_p` ~1 h 선형, 근거 ref [24] Barai 2018) × **3노드**(Cell·Cathode·Anode) × 2방향 = **18수**이고, **주파수 영역 없이 전극을 가른다**(본문 `impedance` **0회** — 5회 전부 참고문헌; `EIS`·`Nyquist`·`DRT` 0회). ★★★★ 그 관측으로 **첫 충전의 122 mAh g⁻¹(54 %) 손실을 양극이 아니라 음극에 배정**하고 `[인쇄]` *"the cause of the capacity fade … **could not have been elucidated without the three-electrode setup**"* 라고 적는다 ⇒ **17호 함정을 5년 먼저 명시적으로 피한 편**. ⚠ 다만 가르는 축이 **양극↔음극 · 옴↔비옴**이지 **접촉 손실↔LAM 이 아니다**(2사이클이라 가를 열화가 없다) ⇒ 반 칸 | ★ **새 층위 — `graphically-read-piecewise`.** measured 도 fitted 도 아니다: `fit*` **0회**, 잔차·공분산 없음, 값은 **Fig. 4 에 손으로 그은 점선 + 주황색 외삽 직선에서 읽은 것**이고 전부 **5 Ω 단위 반올림**이다. ⚠⚠ **정밀도**: `[재현]` 음극 `R_p`(방전) 60 Ω = **12 mV** 인데 패널 (c) 의 y 전폭이 **1.0 V** ⇒ **전폭의 1.2 %** 에서 읽었다(`R_ct` 135 Ω = 2.7 %) — **논문의 중심 주장(음극 `R_ct`·`R_p` 2~3배)이 여기 걸려 있고 오차 표기가 없다.** ★ 라벨의 절반은 **외부 문헌 상수 다섯 개**다(σ 1.8e-4 · `D_Li` 10⁻¹⁶→10⁻¹⁰→10⁻¹² · `D_anode` 10⁻⁸ · **0.62 V** · **2.5 V**) — 그런데 `assum*` 은 **0회** | **0 / 20.** `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·`error bar`·`n =`·`fit*` **전수 0회**(NFKC·대소문자 무시). ★ **열세 번째 성질 = "분해가 적합조차 아니어서 물을 대상이 없다"** — 적합을 안 했으므로 잔차도 공분산도 없고, **분해의 자유도가 데이터가 아니라 작도에 있다**(12호 "낱말이 없다" · 15호 "추정기가 없다" · 19호 "어휘 없이 기하로 물었다" 와 또 다르다). ⚠⚠⚠ **그리고 설계에 2요인 교락이 있다**: `[재현]` 방전 펄스는 **t=2.35 h(양극 x≈0.03, 음극 Li-rich 끝)**, 충전 펄스는 **t=70 h(양극 x≈0.95, 음극 Li-poor 끝)** ⇒ **방향(합금화↔탈합금화) ⊗ 조성이 완전 교락**, 셀은 1개. 저자 스스로 같은 쪽에서 `D_Li` 가 x 에 따라 **10⁶ 배** 움직인다고 적으므로 사소하지 않다 ⇒ `[인쇄]` "탈합금화가 합금화보다 빠르다" 는 **이 설계로 분리되지 않는다** | ★★ **+0.5 — 가정한다. 단 성질이 18호와 다르다.** `assum*` **0회** · `0.62` **2회** · `1.55` 0회. ★★★★ **가정이 문장이 아니라 *그림의 두 번째 축*으로 인쇄된다** — Fig. 2a·3b·4b,c,e,f 의 오른쪽 축 "Voltage (V vs. Li/Li⁺)" = 왼쪽 + 0.62 V ⇒ **낱말 지문으로는 절대 안 잡히는 가정**(우리 지문 관행에 남는 교훈). ① **0.62 V 의 출처가 확정된다**: ref [19] **Santhosha 2019** + ref [20] Takada 1996 = **17호가 "0.62 V 가 태어난 자리" 로 지목한 바로 그 논문**. ② 간접 확인은 **제3물질을 둘** 쓴다: `[인쇄]` `V₂`=1.904 V ↔ 문헌 TiS₂ 2.5 V − In 0.62 V = 1.88 ⇒ `[재현]` **24 mV 일치**(두 가정이 같은 방향으로 틀리면 통과한다). ③ ★★★★ **범주 오류 세 번째, 그러나 유일하게 판별력이 0 이 아니다**: `[인쇄]` *"V₁ was about the same as (V₂–V₃), **indicating that Li-In alloy may have been stably working as an embedded RE**"* — `V₂−V₃ = E_cat−E_an` 이므로 **`E_RE` 가 어떻게 표류해도 성립하는 항등식**이다(전위를 못 본다). **그런데** `[재현]` Fig. 2a 디지타이즈: **리튬화 전 `V₂−V₃` = 2.153 V vs `V₁` = 2.312 V ⇒ 159 mV 깨진다**, 리튬화 후 **5 mV** 로 닫힌다(논문 `[인쇄]` "~0.01 V") ⇒ **정정된 명제: 이 검사는 기준극의 *갈바닉 접촉*을 보지 *전위*를 보지 않는다.** ④ ★★★★ 그 159 mV 가 새 숫자를 준다: `[재현]` **신품(비리튬화) In 의 부유 전위 = 1.77–1.93 V vs Li/Li⁺ = In/LiIn 짝보다 1.15–1.31 V 높다** ⇒ **16호("설치·미검증")가 무엇을 위험에 뒀는지의 크기**. ⑤ ★★★★ **RE 재고 예산이라는 새 축**: `[재현]` 리튬화 20 µA×1 h = 0.020 mAh = **셀 용량의 1/675**, x̄ = **0.0053**(Fig. 2b 가 동정한 **In₁.₇Li₀.₃ = Li₀.₁₈In** 과 33배 차 ⇒ 리튬화가 **≈3.3 µm 표면층**에 갇힌 **구배 전극**). **190 h 실험에서 재고 90 % 를 지키려면 누설 < 10 nA** 여야 하고, **3전극은 기준극 표류를 공통 모드로 상쇄해 원리적으로 못 본다** ⇒ **19호 차분 설계의 물리적 근거가 20호 데이터 안에 있다.** ⑥ ★★ `[인쇄]` **배치가 관측 창을 정한다**는 계보 최초의 진술: 배면형(ref [10] Nam 2018)은 *"the contact resistance between layers … and the SE resistance itself … **were not incorporated into the voltage measurements**"* ⇒ 중앙 매립형은 옴 성분을 **창 안에** 넣는다. ⚠ 빼는 쪽: 전위를 **재지 않았고**, 동정된 상(In₁.₇Li₀.₃ 고용체 쪽)이 0.62 V 의 근거인 **In/LiIn 2상과 같지 않다**(G6). ⑦ **(ㄴ) 기준의 분모를 갈라야 한다**: 상대극이면 *이동 전하*, 참 기준극이면 ***누설 전하*** ⇒ **(ㄴ′) Li 재고 / (누설 × 시간) ≥ 10**, 계보 20/20 편이 누설을 안 쟀다 | **없다 — 0.** `pressure`·`MPa`·`kPa` **전수 0회**, `cold-pressed` 2회뿐 ⇒ **벌크형 황화물 ASSB 인데 압력 값이 한 개도 없다**(18호에 이은 **두 번째 완전 미보고**). ⚠ 이 편은 그 위에 **`R₀` 의 절대값을 접촉에 배정**하므로 미보고의 대가가 18호보다 크다 — 접촉 저항은 압력의 함수인데 압력이 없다 | **해당 없음** — 무음극 아님(Li₄.₄Si). `dendrit*`·`dead`·`isolat*`·`SEI`·`plating` **전수 0회**. ⚠⚠ **그러나** `[도표]` **1·2차 충전이 둘 다 음극 전위 ≈0.02–0.04 V vs Li/Li⁺ 에서 끝난다**(±30 mV, 저자의 0.62 V 축 위) ⇒ **Li 도금이 열역학적으로 열려 있는데 논문이 언급하지 않는다** — 계보에서 **합금 음극이 도금 전위까지 밀린 첫 기록** | ★ **+0.5 — 새 화학 TiS₂**(계보 최초의 황화물 양극). `[도표]` `E_cat(x)` 가 **x=0→0.95 에서 2.52 → 1.72 V, 전 구간 기울기 있음**(평탄역 없음) ⇒ **OCP 기울기가 큰 계열**. ★★ 그리고 **계보 최초로 두 전극의 전위 궤적이 같은 셀에서 동시에 인쇄된다** — 우리 α·β 가 요구하는 입력의 *형태* 그 자체다. `[도표]` 주요 눈금(Fig. 3b): 개방 `E_cat` 2.58 / `E_an` 0.18 → 1차 방전 끝 **1.72 / 0.442** → 1차 충전 끝 **2.396 / 0.019** → **1일 휴지 이완 2.243 / 0.148** → 2차 충전 끝 **2.408 / 0.043**. ★★★ `[재현]` **1일 휴지 뒤 `V₁` = 2.095 V 로 컷오프(2.4 V)보다 310 mV 아래** ⇒ **잘린 용량의 일부는 CC 전용 프로토콜의 산물이다**. ★★★ `[재현]` **면적용량 9.3 mAh cm⁻², 200 µA = C/72** — **극저율에서도 54 % 가 날아간다** ⇒ **`i→0` 이면 `η→0` 처방의 반례**(한계가 율이 아니라 두께·접근 분율에 걸려 있다). ⚠ 단 **통전 중 곡선(pOCV)** 이고 이완점은 3개뿐 · 용량은 `[인쇄]` 225 / 103 / ~105 mAh g⁻¹ · `[인쇄]` **셀을 일부러 최적화하지 않았다**(*"not intentionally optimized … so that the cell performance degradation could be readily observed"*) |

| **★★★★ Sedlmeier, Schuster, Schramm, Gasteiger 2023 (`assb` 21호 — 첫 **미세 기준극(리튬화 금선, GWRE)** · 첫 **파우치 3전극** · 첫 **방향만 바꾼 통제 실험(P4)** · 첫 **동일 조건 셀 간 ±(n = 3)** · 첫 **두 Q5 가지의 뿌리(Ikezawa 2020 · Nam 2018 · Santhosha 2019)를 함께 인용**, 20호도 ref 12 · TUM(Gasteiger) · *J. Electrochem. Soc.* 170, 030536, **CC BY, 13쪽, SI 없음**)** | **없다 — 0/21.** `contact loss`·`θ`·`percolat*`·`tortuos*` **0 회**. `contact` 12 회 중 물리 접촉은 `[인쇄]` *"a combination of the **physical contact resistance and the SEI resistance**"* 로 **한 반원(720 Hz)에 합쳐** 이름만 붙는다. `[인쇄]` 높은 저항을 *"the low fabrication (∼70 MPa) and the low applied stack pressure (∼20 MPa)"* 탓으로 돌리지만 **스윕 0** ⇒ **스물한 번째 0 의 성질 = "접촉을 이름 붙여 SEI 와 한 반원에 합치고, 압력 가설로 넘겼다"**. `[재현]` 저자가 "electrode resistance" 라 부른 375 / 750 Ω cm² 의 **≈65 % / ≈33 % 가 분리막 절반(≈245 Ω cm²)** 이다 | ★★ **+0.5 — "물질은 있는데 접근 불가" 를 "접근 가능" 과 독립 관측 둘로 가른 첫 편, 그리고 OCV 가 그 둘을 못 가른다는 것을 같은 셀에서 보인 첫 편.** 같은 InLi 박(≈24 at%, 공칭 재고 ≈14 mAh cm⁻²)을 **어느 면을 분리막에 대느냐만** 바꿔: 개방회로는 **둘 다 0.62 V(28 일 < 3 mV)**, 그러나 `[인쇄]` 0.2 mA cm⁻² 탈리튬은 **InLi-(In) 9 초 · 0.39 ± 0.21 µAh cm⁻²(재고의 3×10⁻⁵)** ↔ **InLi-(Li) 15 h · 3.0 mAh cm⁻² 평탄**, 저주파 임피던스는 **꼬리 ↔ 반원**(n = 3 씩, 순수 In 대조군 포함). ★ 그리고 `[인쇄]` *"this interpretation of the cell impedance is **incorrect**"* — **2전극 스펙트럼 모양 해석이 3전극으로 반박된 것을 저자가 인쇄한 계보 첫 사례**. ⚠ 반 칸인 이유: 대상이 **음극 Li 재고**이지 양극 활물질이 아니고, 열화가 아니라 **제조 상태**다 | **층 추가 — measured + 셀 간 반복 ± (n = 3, mean ± SD)**, 계보 최초의 **동일 조건 셀 간 ±**(18·19호의 ± 는 회귀 표준오차). ⚠⚠ 9 개 중 1 개 오기: 순수 In 9단계 `[인쇄]` **38 ± 0.8 µAh cm⁻²** 인데 같은 줄의 11.5 ± 3.0 분 · CE 76 ± 20 % 와 맞는 값은 `[재현]` **±10**(Q = i·t) · 그리고 `[인쇄]` "each cell type yielded **identical results**" 라면서 CE ±20 %. 저항은 전부 **Nyquist 판독 ≈값**(`fit*`·`equivalent circuit` 0) | **0 / 21.** `identifiab*`·`uniqu*`·`uncertaint*`·`degenera*`·`error bar`·`fit*` **전수 0 회**. ★ **열네 번째 성질 = "값의 정확도를 검사하고 배정의 유일성으로 읽었다"** — 8단계 저항 차(전하이동 ≈320 ↔ ≈90 Ω cm²)에 **경쟁 설명 셋(정렬 어긋남 · SEI · 계면 Li 고갈)을 인쇄하고 가르지 않은 채**, AC 저항 = DC 과전압 일치(`[재현]` 3 % / 6 %, **계보 최초의 시간↔주파수 영역 일치**)로 `[인쇄]` *"the impedance measurements yield reliable values"*. ★ 우리 곱 축퇴 처방 1단계(τ 형)가 그 셋 중 **정렬 어긋남을 기각**한다(`[재현]` C_CE/C_WE ≳ 1.4 ↔ 면적 예측 0.28) — **논문의 데이터 안에 가를 입력이 있었다**(18호와 같은 구조) | ★★ **+0.5 — 잰다(한 번) · 옮긴다 · 그리고 장기 표류는 잰다.** ① ★★★★ **P4 통제 실험**: 17호 foil 조립(Li 뒷면) = InLi-(In) 은 **재고가 있어도 못 쓴다**, 16호 조립(순수 In) 은 전기화학 리튬화 뒤 InLi-(Li) 와 같은 부류 ⇒ **"LiIn 이 어디 있느냐가 전부" 가 한 변수만 바꾼 데이터로 지지된다** ② ★★★★ **"0.62 V ✓ ≠ 재고 ✓"** — Li-In 상대극의 **기준 역할과 원천 역할이 한 전극 안에서 갈린다**(Fig. 9 가 두 칸 표로 그린다) ③ ★★★★ `[인쇄]` *"in an NCM|In cell, the potential of the indium CE **cannot be assumed to stay invariant at 0.62 V** … as this would depend on the overall loss of cyclable lithium"* — **0.62 V 가정의 부정이 조건과 기구(`LLI`)를 달고 문장으로 나온 첫 편**, 17호 함정의 원인 쪽 ④ ★★★ `[인쇄]` **"all potentials shift less than 3 mV" over 28 days** — 두 전극이 2상 평탄에 고정돼 있어 **기준극 표류가 공통 모드로 보인다** ⇒ 20호 "3전극은 자기 표류를 원리적으로 못 본다" 가 **"고정 전극이 없으면" 으로 좁혀진다**; `[재현]` 재고 **3 µAh**(셀의 1/4,000–1/21,000)가 ≈703 h 를 버텨 **누설 < ≈4.3 nA**(간접 상한 — **21/21 편이 누설을 직접 재지 않았다**) ⑤ ★★★★ **여섯 번째 형태 = 교정 이식**: GWRE 0.31 V 는 **Li\|Li 교정 셀(3 MPa, 2 h)** 에서 Li 대비 **측정**, InLi 셀(20 MPa)에는 `[인쇄]` *"calculated based on a GWRE potential of +0.31 V"* 로 **옮겨진다**. `assum*` **4** 회(기준 전위에 대해 **0**) · `0.62` **18** · `0.31` **7** — ★ **20호 맹점의 세 겹 반복**: 가정이 **"calculated" 라는 낱말**로 · Fig. 4 **두 번째 축**으로 · Fig. 6·8 은 **측정 축 없이 환산 축만**. ★★ 그리고 `[도표]` **부록 Fig. A·1 은 축 이름("vs. InLi-(Li) CE")과 숫자(+0.31 V)가 정확히 0.62 V 어긋난다**(크로퍼가 놓친 그림, 수동 크롭) — 유력한 읽기면 **A·1 은 InLi = 0.62 를 가정해 GWRE = 0.31 을, Fig. 4 는 GWRE = 0.31 을 가정해 InLi = 0.62 를 보인다(순환이 두 그림에)**. ⚠ 16호와 대질: 같은 "리튬화 금선" 이 **0 V(16호) ↔ 0.31 V(21호)** 두 관례 — `[추론]` 21호 Fig. 2a 의 이완 경로(≈0 → 0.25 → 0.31 V)가 **16호 셀 간 0.11 V 어긋남의 후보 설명** | **보고·통제, 스윕 0 — 칸 이동 없음.** 압착 **≈60 MPa**(InLi, 본문 논의는 ∼70 으로 오기) · **≈70 MPa**(분리막) · 체결 **3 MPa(Li\|Li, Li creep 방지) · 20 MPa(InLi 셀)**, 스프링 224 N mm⁻¹ + PTFE 발포 균압. ⚠ Li\|Li 는 **압력과 분리막 두께(2배)가 교락**. `[인쇄]` 압력 가설(높이면 과전압 ↓, Ikezawa 2020 3배 압착 ≈110 Ω cm²)은 **미시험**. 부수 `[인쇄]`: 원통 펠릿에서는 반경 팽창이 막혀 **Li creep 가 Li 를 분리막 쪽에 보낼 수 있다** — 셀 형상이 음극 계면 상태를 정할 수 있다는 첫 진술 | **해당 없음** — 무음극 아님. `dead`·`plating`·`dendrit*` 0 회. ★ 부수: `SEI` 8 회 — **SEI 형성 시점 대조**가 있다: `[인쇄]` 순수 In(≈2.1 V, LPSCl 안정)은 **첫 리튬화에서 SEI** ⇒ 넣은 Li 의 CE **76 ± 20 %**, InLi-(In)(30 일 넘게 0.62 V, LPSCl 불안정)은 **SEI 기성** ⇒ **98 ± 1.6 %** | **해당 없음 — 양극 없음**(InLi\|InLi · In\|InLi 대칭형). 음극 쪽 전위 눈금만: `[인쇄]` In/In₁Li₁ **0.62 V**(≈1–50 at%) · LixAu **0.31 V**(0<x<1.2) · ≈0.25 V(x≈1.3) · `[도표]` 순수 In 부유 **≈2.08–2.10 V**, **완전 탈리튬 뒤 ≈0.96 V**(열역학 짝이 없어 고정점이 아니다; 20호 신품 In 1.77–1.93 V) |
| **★★★★ Strauss, Bartsch, de Biasi, Kim, Janek, Hartmann, Brezesinski 2018 (`assb` 22호 — **1호의 ref 13** · 첫 **`θ` 형 양의 측정**(회절 상 분율) · 첫 **양극 상태를 상대극 전위 없이 읽은 편** · 첫 **3항 분해의 `θ`·`η` 동시 실측** · **계보에서 시간이 가장 이르다(2018-02 접수)** · KIT BELLA + JLU Giessen + **BASF** · *ACS Energy Lett.* 3, 992−996, Letter 5쪽 + SI 8쪽)** | **★ 부분 — 계보 최초의 `θ` 형 측정량.** `[인쇄]` 첫 C/10 충전 뒤 ex situ XRD 2상 Rietveld 로 **불활성(pristine 격자) CAM 분율 2 / 27 / 31 %**(d₅₀ 4.0 / 8.3 / 15.6 µm). **역산이 아니다** — 상 분율(scale factor → 무게 분율)이 먼저이고 용량은 **독립 대조**(`[인쇄]` 90 / 92 / 153 ↔ 전기화학 84 / 95 / 162 mAh g⁻¹). ⚠ 반 칸: 잰 것은 `1 − θ_AM` 의 **합집합 상한**(전자 ∪ 이온 ∪ SE 접촉 ∪ 입자 내부 코어 ∪ 율) · **신품 1 점** · `[재현]` **집전체 면 표층 가중**(Cu Kα 1/e 깊이 ≈3–15 µm / 전극 90 µm) · n 미기재. `θ(N)` 은 여전히 **0/22** | **★ 있다 — 구조 채널.** 불활성 상 = **pristine 격자**(물질은 그대로) ↔ 활성 상 = `x ≈ 0.46–0.56`(덜 충전) 을 **한 측정에서** 가른다 ⇒ `[재현]` **θ·η 분리**: L θ ≈0.69 · η ≈0.69, M 0.73 · 0.65 — **결손의 절반 이상이 '덜 충전' 쪽**. 보조: 율 스윕(C/30·C/50) · LIB 대조(같은 CAM, 크기 효과 없음). ⚠ 원인 배정("lack of electronic contact")은 **별도 펠릿 벌크 σ 와 병치** — `[도표]` σ_e/σ_ion ≈550 / ≈50 / ≈1.5 인데 불활성 M ≈ L, 그리고 Fig. 4 두 축 자릿수 간격이 달라 **L 의 σ_e ≥ σ_ion 이 그림에선 반대로 보인다** | **measured-crystallographic + 방법 오차 예산 인쇄(계보 첫 편)**: 상 분율 −3 % (L, M) · −11 % (S, 검출 한계), `x` ±0.02, **"side reactions … not taken into account"** 명시. ⚠ −11 % 의 단위(절대/상대) 모호 · `n =` 0 회 · ± 는 Rietveld esd `(1)` | **0 (22/22) — 열다섯 번째 성질: "측정이 분할을 대신했고, 원인은 병치됐다."** 적합이 없어 분할의 유일성 문제가 생기지 않고(용량 닫힘은 정당한 값 검증), 원인 대안은 **인쇄조차 안 됨**(18호보다 한 단계 앞). ★ 방법 안의 소형 비유일성을 밟고 지나감: **c(x) 가 x ≈ 0.5 에서 최대**라 두 가지가 있고 활성 상이 그 위에 앉는다 — `[인쇄]` L·M 의 a 가 같아(2.823) 단조 채널로는 x_L = x_M, 인쇄된 0.53 ↔ 0.56 은 **c 가지 선택**; 단조 V(x) 로 읽으면 `[도표]` **순서가 뒤집힌다** | **가정 — 일곱 번째 형태 "가정이 대조군 전압창을 정한다".** 순수 In 박(사전 리튬화 없음) · 기준극 0 · `[인쇄]` "corresponding to 4.4−2.9 V vs Li⁺/Li" · SI "0.6 V difference"(**0.62 는 0 회**). `[도표]` C/30 충전 개시 ≈3.05 V vs In/InLi ↔ LIB ≈3.64 V ⇒ **±30 mV 정합**. ★ **주 주장(XRD)은 17호 함정에서 설계상 면제**, 용량·CE 축은 노출(`[추론]` 순수 In 셀의 방전 끝은 음극이 Li 빈약으로 돌아가는 구간) | **보고·통제, 스윕 0.** 제조 125 / 375 / 125 MPa, 운전 **55 MPa**, 전도도 시편 375 · 250 MPa. 접촉 감소 기구("volume contraction during charging")는 **ref 18 인용**으로만 | 해당 없음 (In 음극) | **NCM622** + **구조 SOC 눈금**(operando a, c, V vs x; LIB) — OCP 는 LIB 곡선뿐. 새 화학 아님 |
| **★★★★ Koerver, Aygün, Leichtweiß, Dietrich, Zhang, Binder, Hartmann, Zeier, Janek 2017 (`assb` 23호 — **"접촉 손실의 실험 원전"**(1호 ref 7 · 22호 ref 9 · 21호 ref 29 · 18호 [23] · 9호 [17] · 3·4호, 이 위키 digest **여덟 편**이 인용) · 첫 **두 비-LAM 기구(계면층 ↔ 접촉)를 동시에 이름 붙인 편** · 첫 **양극 호 `R`·`C` 를 상태축 위 연속으로 인쇄한 편(두 셀 × 네 구간)** · 계보에서 **가장 이르다(2017-03 접수)** · JLU Giessen + KIT BELLA + **BASF** · *Chem. Mater.* 29, 5574−5582 + SI 7쪽)** | **없다 — 이름표 + 정성 영상.** `contact loss` 본문 7 회, 치수·분율·면적 **0**. 사후 SEM 이 N = 0(미사이클 분해 대조) · 1(충전) · 50(방전) 에서 **틈의 유무**만 준다 — 다른 셀의 파편. `[인쇄]` "not 100% dense … not every NCM particle is … well addressed" = `θ` 의 문장, 값 0. ★ **`θ(N)` 측정량 0/23**; 대리량으로는 첫 입력 — `C_SE/Cathode` 를 면적 대리로 읽으면(전제부) `[도표]` **N = 1→2 동안 In 셀 ×1.0–1.3, LTO 셀 ×0.9–1.0** ⇒ EIS 창이 보는 접촉 면적은 **줄지 않았다**(우리 조합, SEM 틈과 긴장). `[도표]` 틈 폭 ≈0.05–0.2 µm ⇒ `[재현]` 요구 ΔV/V ≈3δ/r ≈3–20 % — **원전은 ΔV 를 인쇄하지 않아 닫히지 않는다** | **★ +0.5 — 두 비-LAM 기구에 전용 독립 채널이 붙은 첫 편, 그리고 가르는 입력이 같은 지면에 있다.** XPS(S 2p·P 2p 산화종, 무전류 대조 2) = 계면층 **존재** · SEM(틈·음각, 미사이클 분해 대조) = 접촉 **존재** — 각자 몫 0. ★★ SI Fig. S2·S7 의 `R`·`C` 궤적으로 **우리가 가른다**: `R_SE/Cathode` ×1.5–2.45 동안 `C` ×0.96–1.05(면적 가설 ×0.41–0.66) — **두 셀·다섯 구간 전부 화학 형** ⇒ 원전 **본문** 배정(CEI)은 지지, **초록**의 "contact loss … further increasing the interfacial resistance" 는 불지지. S3 무전류 이완에서 `R₂·C₂` +5 % 보존 = 전제의 **부분 양성 대조**. **반 칸**: 가른 것은 `R` 변화분이지 **용량**이 아니고, 가른 주체가 우리이며, `LAM_PE` 채널(XRD) 0 | fitted(4-RQ, 위상 ≤4° 위 9 파라미터) + measured-chemical(XPS 정량 한 줄 "7.2 atom % ≈1 % of SE", 기준 미기재) + measured-morphological 정성. ★ **n = 4 를 인쇄하고 산포 0**("representative"); 오차 막대 정의 없음(`error`·`±` 0 회). `[도표]` Fig. 1 셀 ↔ Fig. 2 셀 방전 용량 ≈29 % 차 | **없다 (23/23).** 열여섯 번째 성질 = **"채널 분담 + 시간 분할 배정"** — 두 기구에 채널을 하나씩 주어 공존을 보이고, 몫은 첫 사이클("combination") ↔ 이후(CEI, 소거법)로 나눈다. 둘을 동시에 보는 양극 호는 "SOC 가 아니라 전위의 함수" 로 배정 — **첫 충전에서 SOC 와 전위가 단조 동행**해 판별력 0. 초록 ↔ 결론 배정 모순. 비유일성은 `[인쇄]` "to the best of our knowledge, assigned" · "guide-to-the-eye" · "difficult to interpret" 셋으로 인정, 수치 0 | **부분 — 여덟 번째 형태.** `[인쇄]` "**assumed** to be 0.6 V … and **1.55 V** … for lithium titanate"(refs 16·44) — **1.55 V 가정이 18호보다 6 년 이르다**. 축은 Fig. 1·S1 "vs Li/Li⁺"(환산) ↔ Fig. 2·4·S2 "vs Li⁺/InLi"(원). ★ 가정이 깨지는 곳 셋이 데이터에 남는다: 첫 충전 휴지 OCV `[도표]` ≈0.9 → 2.1 V("activation" 으로 **EIS 잘라 냄**) · `[재현]` 첫 충전 앞 SSB 곡선이 LIB 보다 ≈60 mV **낮다** ⇒ 상대극 ≥ ≈0.1 V 높음 · 방전 끝 `C_SE/Anode` **≈90 배 붕괴**("kinetic hindrance" 로 배정). ★★ **17호 함정 노출 + 대조군(LTO)이 같은 함정 공유** — 둘 다 무 Li 조립, 방전 끝 재고비 `[재현]` ≈1.4 | **보고·통제 — 스윕 없음.** 제작 35 kN ≈ **445/446 MPa**, 운전 "≈**70 MPa**" ↔ "5 kN (**64 MPa**)"(인쇄 불일치). `[인쇄]` "no additional solid electrolytes can fill the emerging voids". ★ S3 **무전류** 복합체 저항 ≈165 h 에 ≈×2.2(압력 미상) — 압력 일정에서도 시간에 따라 접촉이 변하는 첫 표본(판 a↔c 크기 ≈8 배 불일치) | **해당 없음** (In · LTO 음극; `plating`·`dead` 0) | **칸 이동 없음** — **NCM811**(코팅 없음, BASF) / β-Li₃PS₄ 70:30 wt 무탄소, 2.6–4.3 V vs Li(환산). 기여: 같은 CAM 의 **LIB ↔ SSB 첫 사이클 곡선 쌍**(LIB CE 85.9 % 는 그림에만) |
| **★★★ Stavola, Sun, Guida, Bruck, Cao, Okasinski, Chuang, Zhu, Gallaway 2023 (`assb` 24호 — 첫 **operando 깊이 분해**(싱크로트론 EDXRD, 20 µm 조각 6–8 개) · 첫 **굴곡도 인자 수치**(세 경로 병치) · 첫 **코팅 유무 통제 쌍** · 첫 **NMC111** · Northeastern + Argonne APS · *ACS Energy Lett.* 8, 1273−1280, Letter 8쪽 + SI 29쪽, **CC-BY 4.0**)** | **없다 — 칸 이동 없음.** `contact` 본문 6 · SI 7, 정량 0. ★ **`θ` 형 관측은 그림에 있다**: `[도표]` 80 % 셀 집전체 쪽 조각 6 의 (003) 한 봉우리가 **충전 1 내내 pristine 근처(≈65.9–66.0 keV)** — 저자는 식 S14 **높이 가중평균**으로 합쳤고, 그 전제("same area")는 자기 Fig. S6 에서 깨진다; 우리 판독 f ≈0.17–0.5(두 추정 불일치, 크기 근거 못 됨). ⚠ 자촉매 가짜 상분리(원전 ref 51)와도 양립. 접촉 변화가 **`τ²` "evolved"** 라는 수송 인자 이름으로 첫 등장(`[인쇄]` "rearrangement of particle contacts"; SI "tortuosity factor accounts … **point contacts**"). **`θ(N)` 0/24** (2 사이클) | **칸 이동 없음 — 층 하나: `η(z)` 공간 연산자.** 깊이별 `(1−x)` 로 **충전 중 구배 = `η(z)`**(반응파로 따라잡음 · 40 % 분리막 조각 방전 중 탈리튬 1.2 h = 두 경로 살아 있음)와 **첫 사이클 비가역 ≈0.2 Δx 가 깊이에 균일**(`[재현]` Fig. 3b–e, 방전 끝 전 조각 ≈0.80) ⇒ **비가역은 두께 수송이 아니다.** 그러나 접촉 ↔ `LAM_PE` 분리 0(열화 없음)이고 22호가 가른 **`θ` ↔ `η` 를 식 S14 로 다시 합친다** | **measured-crystallographic operando(깊이) + fitted(TLM σ_eff) + derived(`τ²`, 가정 `ε` 14 %) + fitted(COMSOL `a`, 수동 "tuned")**. `±` 0 · n = 1/조건 · `[도표]` Li 함량 **>1.0**(≈1.02–1.05) = 교정 오프셋 하한. ★ **같은 양(`τ²`)의 세 추정을 한 표(S9)에 병치한 계보 첫 편** — 작동 조성 ×1.3–3.4. ⚠⚠ **D1**: 이온 쪽 `τ²` 4 값이 **ε_LPSC 가 아니라 ε_CAM 으로 계산**(`[재현]` 4/4 ≤2 %) | **0 (24/24). 열일곱 번째 성질 = "비식별을 물리로 읽었다"** — ① i₀ 평탄 방향 → `[인쇄]` "not under kinetic limitation" ② EIS ↔ COMSOL 불일치 → "the tortuosity factor evolved" ③ `[인쇄]` "relatively insensitive to some parameters" 를 적고 그 파라미터를 7 자리로(같은 `R_el` 두 적합이 **1.35–2700 배**) ④ 가정 `ε` 로 나눈 `τ²` 추세 → "tipping point". ★ **Q4 의 첫 재료**: `σ_eff = σ_bulk·ε/τ²` 에서 `ε·τ²` 분할이 비식별이고, 원전 표에서 **같은 σ_eff 가 ε 규약만으로 ×1.6(인쇄) ↔ ×0.92(바른 ε)** 반대 추세 | **칸 이동 없음 — 아홉 번째 형태 "기준을 말하지 않는다".** 그림 전위 축 **전부 "Potential (V)", 기준 0** · `vs Li−In` SI **1 회** · `0.62` 0 · 기준극 0 · 모델은 `[인쇄]` "counter electrode … **arbitrary potential of 0 V**" + **OCP 없음**. 주 주장(깊이 `(1−x)`)은 **17호 함정 면제**(22호처럼 양극을 전위 없이 읽음); 노출된 곳은 **방전 끝 바닥 ≈0.80**(2.5 V vs Li−In 컷오프) — 양극 고리튬 동역학 ↔ In–Li 고갈이 **In–Li 조성 미기재로 안 갈림** | **보고·통제, 스윕 0 — 칸 이동 없음.** 운전 **50 MPa** · 제조 분리막 300 / 양극 100 / 음극 100 MPa · **EIS 차단 셀 50(이온 차단) / 150 MPa(전자 차단)**. ★ **제조 압력 차가 "굴곡도 진화" 와 교락** — 두 경로의 `σ_eff` 를 비교하는 시편이 다른 압력 이력(`[재현]` LPSC σ_eff COMSOL/EIS 70 % 0.93 · 80 % 0.34) | 해당 없음 (In–Li) | **칸 이동 없음** — **NMC111 은 계보 첫 화학** + 구조 SOC 눈금 `x = (c/a − 4.9722)/0.3552`(Buchberger, x < 0.5) + **σ_e(x)(식 S5) · D(x)(식 S4)** 인쇄. 그러나 **OCP `U(x)` 0** — 모델에도 없다 |
| **★★★ Zhou, Lu, Mish, Chen, Feng, Kim, Song, Kim, Liu 2025 (`assb` 25호 — 첫 **압력 × 미세구조 요인 설계**(운전 30 · 10 · 2 MPa × SE 입도 2) · 첫 **실험 논문이 스스로 DEM `θ` 를 돌린 편**(LAMMPS Hertz, 겹침 기준 민감도 표) · 첫 **저자가 `C ∝ 면적` 추론을 인쇄한 편** · UCSD + **LG Energy Solution** · *ACS Energy Lett.* 10, 966−974, Letter 9쪽 + SI 30쪽)** | **없다 — 칸 이동 없음.** 측정 접촉량 0(`contact loss` 0 회, 단면 SEM 조건당 한 시야·정성). **계산 `θ`** = DEM 이용률 `[인쇄]` coarse 94 / 83 / 56 / 20 % ↔ fine 100 / 100 / 94 / 28 %(겹침 0 / 2 / 5 / 10 %) — 캘린더링 375 MPa 한 시점, 운전 압력 0, 정의 둘(D17). ★ `[재현]` **30 · 10 MPa 첫 충전 비 coarse/fine 1.03**(Fig. 2c 벡터) ⇒ 2 % 기준의 "17 % 불활성" 과 모순, 데이터가 고르는 기준은 0 % 쪽. **`θ(N)` 0/25**; 23호 대리량(양극 `C` 평탄성) **적용 불가** — `C` 미인쇄 · DRT 겹침(D1) · 깨끗한 짝 하나의 판정이 범례에 걸려 `C` ×0.77 ↔ ×1.20 | **칸 이동 없음 — 층 하나: 요인 설계의 공통 모드 분리.** `[재현]` 30 → 2 MPa 초기(c2) 손해 coarse −26.5 ↔ fine −30.7 mAh g⁻¹(같다) · 감쇠 c2→c100 coarse −33/−38/**−64** ↔ fine −26/−27/**−22**(fine 압력 무관) ⇒ **미세구조가 바꾸는 것은 감쇠의 압력 의존뿐**. 율 극한(S18, 2 MPa) `i→0` 비 ≈0.89 ⇒ 0.1 C 결손의 ≈2/3 가 `η(i)`. 원전은 `[인쇄]` "bulk NCM811 structure **and** interfacial contact" · "`R_CEI` and `R_ct` are **indistinguishable**" 로 병치 | **computed-geometric**(DEM `θ` · 기하 τ, 기준 손잡이) + **fitted**(ECM, CPE 미인쇄) + **inverted**(DRT, 정규화 미기재) + measured-electrical. n 미기재 · 오차막대 0 · S8 펠릿 3 개가 유일 반복. ★★★ **새 층위 "그림 자료의 정체가 불확실"** — `[재현]` Fig. 3 DRT 12 곡선 중 5 개가 2 개(≤0.21 Ω), Nyquist "2 MPa 1 뒤" = "30 MPa 100 뒤"(≤0.8 Ω), S15 제목 반전, 인쇄 유지율 6 중 2 만 재현. ★ **암묵적 반복**: 2 MPa fine S18 ↔ Fig. 2c ≈30 mAh g⁻¹(≈20 %) = 압력 효과와 같은 크기 | **0 (25/25). 열여덟 번째 성질 = "민감도를 인쇄하고 그 손잡이로 검증을 맞췄다"** — Table 1 이 계보 첫 `θ` 계산 민감도 표(94 → 20 %, 비 비단조)인데 2 % 를 골라 "83 % ↔ ≈85 %" 로 맞추고 어긋남을 `[인쇄]` "further refinement of particle overlap is needed for the specific C-rate" 로 **같은 손잡이에 되돌린다**(예측 → 보정). 24호("둔감을 물리로")와 반대편 — 예민을 보고 한 값을 골랐다 | **칸 이동 없음 — 열 번째 형태 "Li 금속이라 기준을 문제 삼지 않는다 — 자기 적합이 상대극을 가장 큰 항으로 인쇄한다".** `vs Li` 0 · `reference` 0 · 축 "Voltage (V)". ★★★★ **17호 함정 노출** — `[도표]` S19 `R_SSE/anode` 가 모든 조건에서 `R_SSE/NCM` 의 2–4 배, 2 MPa coarse 380 → **2400** ↔ 125 → 660 Ω; `[재현]` 방전 전압 하강 ≈0.30–0.37 V 가 적합 `ΔR`×I(≈0.30 V)와 맞고 그중 **≈80 % 가 Li 계면**(1C ≡ 200 mAh g⁻¹ 가정). 저자는 음극 증가를 양극 부피 변화 탓으로(측정 0) | **★★ +0.5 — 계보 첫 양극 쪽 압력 스윕 × 미세구조.** 운전 **30 / 10 / 2 MPa**(제조 양극 375 · Li 30 MPa). 압력별 용량·감쇠·전극별 `R`(S19) 같은 지면 ⇒ **1 사이클까지 압력 효과는 공통 모드**(용량 · `R_NCM` ×1.8–1.9 · `R_anode` ×1.7–1.8 두 조성 같이), **상호작용은 감쇠에만**; 문턱 2–10 MPa. ★★★ **5호 위 벽의 반례 후보** — Li 금속 30 MPa 100 사이클 ≈1500–1700 h `[재현]` 단락 보고 0(5호: 25 MPa ≈48 h, 같은 UCSD, 인용 0). ⚠ 장치·계측 0(`load cell`·`torque` 0) · 이력 미기재(10·2 MPa 는 하강 분기) · n = 1 · 2 MPa EIS 기준점이 겹침 위 · 요구치 `[인쇄]` "≤5 MPa" 출처 없음 | 해당 없음 (Li 금속 박 100 µm, 무음극 아님). `dead`·`plating`·`dendrit*` 0. 기록: Li 계면 저항이 **압력 × 사이클 격자(3 × 2 × 2) 위에 인쇄된 첫 편** | **칸 이동 없음** — NCM811(자체 합성, 무코팅, 1–5 µm), 2.5–4.25 V, 0.1 C. GITT 3 쌍(100 사이클 뒤) 있으나 프로토콜 0 · `OCV` 0 회 |
| **★★★ Iwakiri, Delgado, Nogueira 2024 (`assb` 26호 — 제목에 "parameter estimation and **sensitivity analysis**" 가 든 계보 첫 편 · 첫 **추정 + 스윕이 같은 모델·같은 지면** · 첫 **박막 Li/LiPON/LCO** · 첫 **SE 에 농도 구배를 둔 모델**(이온 + 공공 해리) · NTNU + Simoldes Plásticos · *Electrochim. Acta* 508, 145202, CC BY, 18쪽 · ⚠ **모델 편 — 1차 실험 0, 데이터는 Raijmakers 2020 의 4 율 방전곡선 98 점을 빌림 · 열화 0**)** | **없다 — 0/26.** `contact` **0 회**(낱말 자체가 없다). 양극은 `[인쇄]` 유사균질 조밀막, 면적 `A` 는 기하 고정 ⇒ 접촉 변수의 자리가 없다. `[추론]` 들어간다면 **부분 박리 → `k¹_s`**, **고립 부피 → `a_max`** — 카드의 곱 축퇴(`A_eff·j₀` · `θ·Q`)의 박막판 | **없다** — 실험 0, 빌린 곡선 4 개(셀 1 개) | **fitted 점추정 on borrowed data** — ±0 · 반복 적합 0 · 잡음 모델 0(가능도 없음 → CI 의 틀 자체가 없다). ★ **새 층위 "문헌 대조가 같은 데이터의 출처 논문 값과의 대조"** + `[재현]` **적합 변수 10 중 7 이 정확히 문헌 ×1.0500**(인쇄 5 자리) — `[인쇄]` "not fed into the optimization algorithm" | **없다 (26/26 편 0).** ★★★★ **열아홉 번째 성질 — "평탄을 스스로 계산해 놓고, 평탄 위의 점을 값으로 인쇄하고, 그 점에서 본 둔감을 물리로 읽었다"**: "sensitivity analysis" = 1C 전방 모델의 **OAT 대역 스윕**(×0.1–500 · 동역학 ×5e-7–1e5) + 설계 KPI; `Fisher`·`Hessian`·`correlat`·`confidence`·`uncertain`·`profile likelihood` 전수 0, 본문은 그 낱말도 안 쓴다("parametric study" 16 회). 그런데 `[도표]` **Fig. 5a**(`D_e⁻` ×0.1–500 곡선 일치) · **Fig. 12a≡12b**(`k₁`↔`k₂`) · **Fig. 3≡15**(`D_M⊕`↔`a_max`, 전류 고정) = 비식별 방향 셋이 저자 그림에 있고, `[인쇄]` Table 3 `D_e⁻` 최적 **5.24×10⁻³ ↔ 문헌 5.06×10⁻¹³ (10 자릿수)**. `[재현]` 식 (30) 으로 문헌값이면 Fig. 5a 가 성립 안 한다(×0.1 → `D_p` ×0.365) ⇒ **그림은 표류한 적합점에서 그려졌고 저자는 그 둔감을 "느린 종이 지배" 로 결론에 올렸다.** 비식별을 **보인** 것은 우리(`[재현]`) — Q4 는 재지 않은 것이라 0 | **해당 없음** — Li 금속 음극, 전위 고정, 기준극 0. 음극 과전압을 `k₂`·`ρ_Li+Pt` 두 항으로 나누는데 `[도표]` Fig. 12a≡b 가 **그 나눔을 데이터가 못 한다**는 것을 보인다 | **없다**(`pressure`·`MPa` 0 회 — 박막) | **해당 없음**(Li 박, 열화 0) | **LCO 박막 — 기존 화학(2호에 LCO)**. 평형 곡선은 ref 10 에서 빌림(함수형·출처 그림 미인쇄), `[도표]` 4.2 V(`x` 0.5) → ≈3.9 V(0.8) → ≈3.7 V(0.99) 뒤 급락. `OCV` 0 회. ⚠ 셀 공칭 0.7 mAh ↔ `[재현]` 모델 `Q_ideal` **1.23 mAh**(모델 1C = 1.23 mA — Fig. 4 · 9 로 검산) |
| **★★★ Sinzig, Schmidt, Wall 2024 (`assb` 27호 — 계보 첫 **전역 민감도(Sobol 1·2·전차 + 95 % CI)** · 첫 **모델 대 모델 비교**(3차원 입자 분해 ↔ 균질화 P2D, 같은 방정식) · 첫 **"모델 불일치 민감도"**(`|∇d_SOC|`) · TUM 계산역학 + TUMint.Energy · *J. Electrochem. Soc.* 171, 120519, CC BY, 14쪽 · ⚠ **모델 편 — 실험 0 · 빌린 데이터도 0 · 열화 0**)** | **부분(계산) — 1호와 같은 층.** `[인쇄]` 전자 연결 분율 **`u = 0.93`**(생성 미세구조 1 개, DEM 재배열), `contact` **0 회**. ★ `[재현]` resolved 의 `SOC_end` 에 **`1 − u` = 0.07 바닥**(비연결 입자가 초기 SOC 에 머묾) — Fig. 11a 큰 `κ` 오프셋 **0.068** · Fig. 7 150 점 평균 차 **0.072**(벡터 좌표). `θ(N)` **0/27** | **없다** — 실험 0, 두 모델의 무잡음 출력뿐 | **model-vs-model reference** — 상위 충실도 모델을 `[인쇄]` "assumption" 으로 참값 삼음(= 우리 합성 truth 의 구조). ★ **민감도에 95 % CI 를 붙인 계보 첫 편**(단 GP 대리모형 · CI 출처 미기재) | **없다 (27/27 편 0).** ★★★★ **스무 번째 성질 — "적합성을 전역으로 재고, 그 안에서 나온 비식별의 재료 셋 — 전차 지수 0 · 두 모델의 일치 · 보정이 흡수하는 상수 — 을 전부 모델 적합성으로만 읽었다. 그리고 상수의 정체는 접촉 손실이었다"**: `[도표]` `S_T(D │ P2D) ≈ 0`(Fig. 8a) = 비식별의 충분조건인데 저자는 "P2D 가 `D` 영향을 과소평가" 로 읽음 · 두 모델 일치 영역 = 구조적 비식별인데 "P2D may be easily used" · `[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters" = 보정이 구조 오차를 먹는다는 명제, 그 상수를 저자는 "insufficient homogenization strategy" 로 배정 ↔ `[재현]` 크기가 `1 − u`. 데이터 0 · 단일 파라미터 · 대리모형 · 저자 판정 없음 · 결정적 그림(Fig. 3b "dashed line")이 **지면에 없음** ⇒ 반 칸 검토 후 접음 | **해당 없음** — Li 금속 음극, 모델 편 | **없다** — 틀 강성 500 MPa mm⁻¹ 한 값, 축 응력은 출력(`[도표]` 0 → ≈3.0–3.5 MPa, 예압 0), 스윕 0 | **해당 없음**(Li 금속 · 열화 0) | **NMC622 + LPS — 기존 화학**(22호 NCM622). OCV 는 ref 44(Kremer)에서 빌림. `[재현]` 벡터: 평탄 **3.67–3.69 V @ `χ` 0.81–0.97**, 하한 3.6 V 는 그보다 70–90 mV 아래 ⇒ `SOC_end` 는 **OCP 평탄이 증폭하는 문턱 출력**. `OCV` 0 회 |
| **★★ Bizeray, Kim, Duncan, Howey 2019 (`assb` 28호 — ⚠ **액체셀 · ASSB 아님** · 계보 첫 **식별성(셋째 줄)** — 구조적(전달함수 유일성) + 실제적(손실 등고선) · 큐 27 "방법론 원전" · Oxford + **SAIT** · *IEEE TCST* 27(5), 1862 · 26·27호 **둘 다 인용 0**)** | **없다 — 액체셀.** `contact` 3 회 = 전부 옴 "contact resistance"(`R0` 에 합침). `θ(N)` **0/28**. `[해석]` 그러나 묶음 대수로: 입자 통째 비연결 `ε → uε` 는 `Q_th` 에만 들어가 **LAM 과 같은 파라미터**, 표면 일부 접촉은 `k·A_eff` → `R_ct` → `R0` | **없다** (ASSB 관측 0). 액체셀 기준극(리튬 코팅 Cu 선, [35])으로 전극별 OCV 를 잰 것은 방법의 **전제** | **fitted(EIS 최소제곱) + 합성 참값 복원** — 합성 데이터가 **같은 선형화 SPM · 무잡음**(역범죄). 불확실성은 **등고선 그림뿐**, CI 0 · 셀 1 · 반복 0 | **★ 있다 — 단 액체셀(도구 칸). ASSB 0/28.** ★★★★ **스물한 번째 성질 — "도구는 있고 대상이 없다"**: 식별 집합 `θ̃ = (τ_d⁺, τ_d⁻, R_ct)` 에 **용량이 없다** — `Q_th`(LAM·접촉이 사는 자리)는 `[인쇄]` `β = α/Q_th = dU/dQ` 로 흡수돼 **기준극 입력**, `x⁰`(정렬, LLI)도 가정. `[인쇄]` 보편 범위 명제("any lithium-ion battery model … flat OCV … unidentifiability")는 **동역학** 파라미터에 관한 것이라 카드 방향(양극 용량 분할)에 닿지 않는다 ⇒ 반 칸 검토 후 접음. 26호 `k₁≡k₂` = 식 (50) 과 같은 구조 · `D_e⁻` 0 열 = 예외 1(`β = 0`)과 같은 부류 · 다른 기구 · 27호 `1 − u` = `Q_th` 손잡이 — 전부 우리 `[해석]` | **해당 없음** — Li-In 없음. 기준극 셀 ≠ 측정 셀 + 시간 영역 사후 **×0.78**(양극 OCV 기울기) = 21호 "교정 이식" 의 액체셀 선례 | **없다** (`pressure` 0, 상용 파우치) | **해당 없음** | **해당 없음(액체)** — Kokam NMC/흑연 740 mAh, 전극 OCV GITT 50 점(Fig. 5d: 음극 DoD ≈0–60 % 평탄 · 양극 ≈45–65 % 평탄) · 합성 LCO |
| **★★★ Yanev, Auer, Pertsch, Heubner, Nikolowski, Partsch, Michaelis 2024 (`assb` 29호 — 첫 **율 외삽으로 정적 ↔ 동적 용량을 가른 편**(CA + `Q(R) = Q_M/(1+2(Rα)ⁿ)`) · 첫 **ASSB 적합 공분산 진단**(OriginPro dependency, SI Table S2) · 첫 **접촉 손실 두 종류에 두 관측**(전자 비연결 → `Q_M` · 이온 피복 → `φ`) · 14 복합체(NCM811 gran/sc × LPSCl/BM × AM 51–90 wt%) · Fraunhofer IKTS, **17호와 같은 연구실**(17호 = ref 21) · *J. Electrochem. Soc.* 171, 050530, CC BY · ⚠ **신품(형성 2 사이클) · SI 미열람**)** | **없다 — 역산 둘.** `Q_M`(`[인쇄]` "indicator of the degree of electronically percolated AM") 14 점은 **용량 외삽**, `φ = √(D_ASSB/D_LIB)`(`[인쇄]` 53.3 → 18.0 % gran · 85.2 → 3.1 % sc) 14 점은 **`D_true` 공통 · LIB 피복률 100 % 가정** 위. 균열은 두 칸에 동시 배정. 단면 영상 0. **`θ(N)` 0/29** | **반 칸 검토 후 접음.** LIB 반쪽전지(같은 분말)가 **물질 용량 ↔ 이용률**을 가르는 신품판 채널이지만, 기준이 **0.1 C 유한 율**이라 한계가 아니다 — `[도표]` sc84 `Q_M` ≈236 ↔ `Q_LIB` 213(≈111 %) | **fitted-extrapolated**(`Q_M`) + ★ **derived-by-reference-ratio**(`φ` — 외부 액체 기준 수입, 기준 자체가 곱을 진다: `D_LIB` gran/sc 2.7 배) + fitted(TLM `σ_eff`) · 공칭 `ε`(`[재현]` 0.57/0.37/0.234/0.153, 형상 공통). 오차막대 0 · 조건당 1 셀 | **★ 반 칸 — ASSB 계보 첫 (0/28 → 0.5).** `[인쇄]` sc90 "not enough information … to accurately fit the Q_M and α … high dependencies close to unity in Table S2. Only the fit parameter n can be reasonably interpreted" — **저자가 돌린 공분산 진단 + 비식별 명제**, 식별 집합에 **용량 스케일 포함**(28호는 입력으로 뺐다). `[재현]` 식 (2) 고율 극한 `(Q_M/2)(Rα)⁻ⁿ` ⇒ 평탄이 창 밖이면 `Q_M·α⁻ⁿ` 한 조합 — 진단과 정합. **반 칸인 이유**: 값은 SI(미열람) · 국소 공분산만 · 축이 정적↔동적(`LAM_PE`↔접촉 아님) · ★ **진단을 해석에 전파 안 함**(sc90 `Q_M`·`α` 무표시 작도, 가장 센 이용률 주장 "sc84 최대 · LIB 초과" 가 평탄 없는 셀의 외삽) | **이동 없음 — 열한 번째 형태 "검증 이식"**: 2전극, 0.62 V 가정(ref 23 Santhosha, 숫자는 지면에 없음). 같은 음극 조성을 17호가 3전극으로 검증 — 그러나 검증 창(정상 ≈20 mV)과 `n` 을 읽는 창(CA 첫 구간, 17호 `[인쇄]` "ca. 0.9 V at the beginning")이 다르다 | **없다 (스윕)** — 제조 500 MPa · 운전 ca. 50 MPa 고정 | **해당 없음** | **이동 없음** — NCM811 **단결정 ↔ 다결정 첫 대조**, OCP 0(형성 곡선 SI) |
| **★★ Park 2024 (`assb` 30호 — 큐 29 · 첫 **산화물 SE 실험 셀**(소결 LATP 펠릿 150 µm) · 첫 **SE 없는 슬러리 양극**(NMC111:CB:PVDF, 0.57 mg cm⁻²) · 첫 **방향 비대칭(산화 ↔ 환원)을 주제로 한 편** · 홍익대 단독 저자 · *Materials* 17, 5014, CC BY, SI 없음 · ⚠ **셀 조건당 1 · 오차 0 · 액체 대조는 표 한 줄뿐**)** | **없다.** `contact` 6 회 전부 정성, 영상 0. **복합양극이 아니라 `θ` 의 자리(전극 안 비연결 입자)가 없다** — 접촉은 펠릿 한 면. **`θ(N)` 0/30** | **없다.** 사이클 손실(`[도표]` 0.1 C 블록 85 → 63, 고율 뒤 ≈48)을 가를 관측 0 — dQ/dV 는 손실 **전** 1–10 회뿐 · 손실 뒤 EIS 0. `[재현]` "고율 뒤 비가역" 은 고율 전 표류 속도 이하라 **고율 귀속부터 안 갈린다** | ★ **새 층위 둘**: **label-contradicts-own-figure** — `[재현]` b 의 산화/환원 배정이 Fig. 3 과 반대(인쇄 0.76/0.58 ↔ 그림 ≈0.58/≈0.73) · Table 1 "고체" 용량 행 ≠ Fig. 2a(고체셀) = "액체" 행 · **textbook-equation-with-unprinted-inputs** — Randles–Ševčík `A`·`C_Li`·`n`·`T` 미인쇄, 비만 재현(1.97 ↔ 1.94). 오차 0 · 1 셀 | **없다 — 스물두 번째 성질 "라벨이 자기 그림을 거스른다".** 민감도·적합 진단·식별성 도구 전부 0 (`identifiab` 0 · `fit` 0). 전제가 배타인 두 모형(멱법칙 b ≠ 0.5 ↔ Randles–Ševčík b = 0.5)을 같은 봉우리 전류에 병치 · `A·C·√D` 묶음(29호 `D_app ∝ 1/A²` 의 CV 판)의 액체 대비 10.9 배를 전부 `D` 에 배정 — 29호는 같은 구조를 **면적**에 배정했다 | **이동 없음 — 열두 번째 형태 "방향 비대칭의 일방 배정"**: 2전극, `[인쇄]` "Li-metal served as both the **reference** and counter electrodes" — 방향 의존 관측(b · `D`)을 양극과 LATP/NMC111 계면에 배정, **상대극의 석출 ↔ 박리 비대칭 언급 0**, 가를 **Li/LATP/Li 대칭셀은 지면에 있으나 전도도 한 숫자로 소진**. 17·25호 함정: `[재현]` 직렬 몫 ≈0.5–0.86 kΩ(대칭셀 호) ↔ CV 봉우리 이동 기울기 ≈0.54–0.65 kΩ — 같은 자릿수 (자기 적합 없음) | **없다 — 미보고.** 코인셀, `pressure` 1 = 펠릿 CIP 30 MPa | **해당 없음** (Li 박) | **이동 없음** — NMC111(24호 다음 두 번째) · OCP 0. `[해석]` "2상 평탄이 저 담지량으로 흐려졌다" 는 근거 없는 서술 |
| **★★ Chien, Liu, Menon, Brant, Brandell, Lacey 2023 (`assb` 31호 — 큐 30 · ⚠ **액체셀 · ASSB 아님**(1 M LiPF₆ EC/DEC, SI 26 쪽 고체셀 0) · 첫 **ICI(차단 √t) 방법 원전** · 첫 **"고지된 면적 배정"** · 3전극 Li 링 기준극 파우치 · Uppsala + Scania · *Nat. Commun.* 14, 2289, CC BY · zenodo 원자료 공개(미열람))** | **없다.** 접촉 어휘 0. Fig. 7 `D`(N)·`R`(N) 5 사이클 추적은 **측정**이지만 `A` = 신품 BET 고정 · 가로축 `Q`(`[인쇄]` 특징 ≈200 → ≈180 mAh g⁻¹ 이동) — ASSB 에서는 `φ²D` 곱 대리량 후보. **`θ(N)` 0/31** | **없다 (액체).** `R_ICI` ≈ EIS `R0+R1+R2` **합**(Fig. 6) — 성분 분리 아님. `R`↔`k` 는 시간 척도 분리, 실패 조건 `[인쇄]`(3.7 V 아래 CT 시상수 간섭). `[해석]` `R/k` 면적 소거 조합 — 인쇄 재료 없음 | ★ **새 층위 둘**: **measured-bundle-with-declared-constant**(`k`·준-OCP 기울기 측정 + `A`·`V` 상수, 고지 + 비교 한정) · **regression-SD-only error bars**(`[재현]` 방법 간 SD 0.56 = 2·√(0.26²+0.076²) ↔ 막대 10–30 %). 셀 2 · 온도 미통제 | **ASSB 0 — 도구 칸. 스물세 번째 성질 "공통 인자로 비교를 봉인하고, 절대 주장에서 봉인을 뗐다."** `[인쇄]` "BET-surface area may differ from the electrochemically active surface area … both … equally affected" — 비식별 **진단**이 아니라 **비교 불변성 선언**. 식별성 도구 0. `[재현]` 면적 정의(BET ↔ D50 구)만으로 `D` ×2.5 > 방법 간 불일치 | **해당 없음** — 액체 Li 링 기준극, 작업극만 보고(상대극 `R`·`k` 지면 0). 30호 "reference and counter" 의 **설계상 대조** | **없다** — operando Be 원판 "uniform stack pressure" 값 없음 | **해당 없음** | **해당 없음** (액체) — NMC811 준-OCP **기울기**(Fig. 4), 4.17–4.2 V 골 ×0.36 |
| **★ Biçer, Aksöz, Bakar, Odabaşı, Vonk, Soares 외 15 인 2025 (`assb` 32호 — 큐 31 · ⚠ **Review 49 쪽, 1차 측정 0** · 첫 **BMS + 열관리 + 조립 + LCA 통합 종설** · Sivas + Siro(셀 제조사) + Bozankaya(버스) + TechConcepts + INEGI · *Batteries* 11, 212, CC BY · **8호 §6.1 요구가 매단 원전 — 그 요구 (ㄷ) 가 없다**)** | **없다 — 0/32.** `contact loss` **0 회**. 접촉 불량의 결과를 `[인쇄]` "increased impedance, mechanical delamination, and eventual cell failure" 로만 적고 **용량 몫 0** — 분류 체계 네 번째 표본 **"접촉 = 임피던스"**. `θ(N)` 0/32 | **없다.** SSB BMS 권고 채널(압력 센서 + 피드백 · EIS "tracking dynamic internal resistance" · 서브셀 전류/온도) — 전부 **유지·추적** 용도, 모드를 **가르는** 용도 0 | 칸 없음 · **층 하나: 정의 없는 SoH + 정격 분모 SoC** (`[인쇄]` SoC = "instantaneous capacity to its **rated** capacity" → 감퇴가 SoC 로 샌다). "SEI" = solid electrolyte–electrode **interface** 로 재정의 | **ASSB 0 — 스물네 번째 성질 "선형 OCV 전제가 물음을 지운다."** `[인쇄]` "well-established **linear** relationship between SoC and OCV"(p.23) ↔ "nonlinear ... due to ... polarization resistance and polarization capacitance"(p.24). `identifiab` 0 · `uniqu` 10 전부 일상어 | **해당 없음** (기준극·In 0) | **칸 이동 없음** — `pressure` 14 · **`MPa` 0**. "pressure sensors and feedback control ... maintain optimal stack pressure" · 제조 ↔ 운전 압력 미구분 · Table 8 은 스택 압력을 덴드라이트에만 | **해당 없음** | **칸 이동 없음** — Table 1 SSB 양극 "LCO, NCA, LFP, vanadium oxide" · 공칭 "Bulk 2.5 V / Thin film 4.6 V"(출처 미기재), OCP 0 |
| **★ Zhang, Fu, Lu, Hu, Xia, Zhang, Wang, Zhou, Yan, Xia, Wang, Sun 2025 (`assb` 33호 — 큐 32 · ⚠ **Review 22 쪽, 1차 측정 0** · 첫 **저압 전용 종설** · 첫 **제조 ↔ 운전 압력을 명시적으로 가른 종설**(Table 1 두 열) · EIT Ningbo + USTC + UWO · *Adv. Mater.* 37, 2413499 · **8호가 "pressure reduction = commercialization problem" 을 매단 편 — 그 명제는 선다**)** | **없다 — `θ(N)` 0/33 · `θ(P)` 0.** 양극 접촉 손실은 [57](= 23호 Koerver 2017) 한 문단이고 수치 0 — 그리고 **원전 배정을 뒤집는다**: `[인쇄]` "loss of contact leads to a decrease in electrochemical activity **in subsequent cycles**" · "continuous application of external pressure ... **reactivation**"(인용 번호 없음) ↔ 23호 "contact loss should **only occur during the initial charge** ... ongoing capacity fade ... **interphase**". Sakka 2022 [120] 는 인용하나 CT 접촉 분율 **0 자**. `fraction`·`percolat*`·`tortuos*` 0 | **없다.** 재수록 압력 추적(DEP · 힘 센서 · σ₁₁)은 관측 채널이지만 가르는 용도 0 | 칸 없음 · **층 하나: "재수록 그림의 출처가 캡션과 본문에서 갈린다"** — Fig. 3I(캡션 [63] ↔ 본문 [78]) · Fig. 5(패널 A/B 뒤바뀜 + 번호 불일치) · Fig. 7C([119] ↔ [19]) = 그림 8 장 중 3 장 | **ASSB 0 — 스물다섯 번째 성질 "용량은 전략의 성적표 — 분해의 대상이 아니다."** `capacity` 18 회 전부 성능 수치 · `degradation mode`·`LLI`·`LAM`·`fit*`·`OCV`·`EIS` 0 | **해당 없음** (In-Li 5 회 전부 음극, 기준극 0) | **칸 이동 없음 — 층 둘.** ① 제조 ↔ 운전 **명시 분리**(32호 미분리) ② `[재현]` Table 1: 제조 7/8 행 360–500 MPa · 운전 9/10 행 ≤5 MPa ⇒ **"저압" = 고압 제조 · 저압 운전**(25호와 같은 모양). 압력 ↔ `θ` ↔ 감쇠의 **함수 0** — 압력–용량 원자료는 Fig. 3I(70/7/2 MPa **첫 사이클**, 출처 번호 둘로 갈림) 하나, Fig. 7B 는 2 MPa 한 점. 요구치 **< 2 / ≤ 2 MPa**(`[인쇄]` "To our knowledge", 출처 없음) = 계보 **다섯 번째 인쇄값**(≈1 · 0.4–1 · <5 · ≤5 · 2 — 원전 0). Xu 2024 = [11] 을 "hundreds of megapascals" 에만 인용, **"<≈1 MPa" 없음**. `[해석]` 재수록 상대극 압력 진동 0.7–2.3 MPa/사이클 ≈ 요구치 | **해당 없음 — 칸 이동 없음** (무음극 절은 중간층 · `R_tot` · 초기 CE 58.4 → 83.7 % 뿐) | **칸 이동 없음 — 입력 하나**: Fig. 3A/B([58] Koerver 2018) 양극 화학별 `ΔV/V₀(x)` · `V̄m(Li)(x)` — OCP 가 아니라 부피 쪽 상태함수, 14호 volumetry 의 기준 부피 |
| **★ Liang, Tao, Shi, Lyu, Ji, Dong, Mo 2026 (`assb` 34호 — 큐 33 · ⚠ **Comment 5 쪽, 1차 측정 0 · 데이터 0 · ASSB 아님(도구 칸)** · 첫 **능동 펄스 BMS 논평** · 위키 전체에서 첫 **D-optimality · PE · OED 처방** · UNSW + Chalmers + UTS · *npj Clean Energy* 2, 16, CC BY-NC-ND · 자기 인용 8/32)** | **없다 — `θ(N)` 0/34.** `contact` 1 회 = ref 29(Yang 2024 *Science*, **액체 Si 음극**) "transient voltage pulses … capacity recovery … by modulating … **interfacial contact of active materials**" — `[해석]` 4호 재가압과 같은 부류의 **복원 조작**(되돌리면 물질은 그대로)이지만 음극 · 액체 · 미열람 | **없다.** 펄스 채널은 **제안**이고 가르는 용도 0. `[인쇄]` "explicit mappings between pulse responses and electrochemical subprocesses **must be established**" — 사상이 아직 없다고 저자가 적는다 | 칸 없음 · **층 하나(제안형): learned-reconstruction features** — IC · DV · 등가 EIS 를 `[인쇄]` "deep learning and online identification of equivalent-circuit parameters" 로 **재구성**(refs 21–24). ⚠ ref 21 제목 "**10 Hz sampling**" ⇒ `[해석]` 나이퀴스트 5 Hz 위(계면 대역 10⁰–10³ Hz 의 ≈2.3 자릿수)는 **사전이 채운다**. + 역 UQ "probabilistic confidence interval rather than a deterministic value" — 요구만 | **ASSB 0 — 스물여섯 번째 성질 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다."** `identifiab*` **NFKC 뒤 3(+분절 1) — 정규화 전 0(합자 `ﬁ`)** · FIM 2 · CRLB 1 · D-optimality 1 · PE 3. `[인쇄]` "observability is redefined as a **controllable resource** rather than an intrinsic system constraint" · "CRLB, which is the inverse of the FIM"(특이 FIM 무언급). **계산 0 · 구조적 ↔ 실제적 비식별 구분 0**. 8호("Unidentifiable pulse response" = 실패 모드)와 **반대 방향**. 누적 0.5 = 29호 그대로 | **해당 없음** (Li-In · 기준극 0). `[해석]` 단자 펄스의 분극은 상대극 호를 품는다(17·20·25호) | **없다** (`pressure` 0 · `MPa` 0) | **해당 없음** — `[도표]` Fig. 1a 아이콘 "Inactive Li" 뿐, 본문 `inactive`·`dead` 0 | **없다** — 화학 미지정 "lithium-ion", `OCV` 0. ★ `[인쇄]` 불변량 예시 "**active material stoichiometric limits**" = α·β 가 푸는 양 — 근거 0, 그리고 Fig. 1b 가 **Degradation** 을 불변 사상의 도메인에 둔다(자기 긴장 D3) |
| **★ Roman, Saxena, Robu, Pecht, Flynn 2021 (`assb` 35호 — 큐 34 · ⚠ **ML 방법 논문 · 1차 실험 0(공개 데이터 CALCE · NASA · TRI · Oxford 179 셀) · 액체 상용 셀 · ASSB 아님(도구 칸)** · 첫 **불확실성 보정 + held-out 적중률 검사** · 8호 Table 2 의 "Confidence interval reported" 원전 · Heriot-Watt + **CALCE** + TU Delft · *Nat. Mach. Intell.* 3, 447 · SI 18 쪽)** | **없다 — `θ(N)` 0/35.** `contact` 0 | **없다.** 1차 측정 0. 유일한 저항 채널 `Lagged Pseudo Resistance`(`ΔV/I`)는 세 그룹 모두 특징 선택(RF-RFE-CV)에서 **탈락** — `[해석]` 용량 목표 선택은 분리 채널을 먼저 버린다 | 칸 없음 · **층 하나: measured scalar label + held-out-recalibrated predictive interval (coverage audited)** — 라벨 = 측정 방전 용량(Ah; 훈련만 RANSAC 세척) · 구간 = `μ ± 2σ`, 보정 전용 셀(5 · 10 · **1**)에 isotonic → 시험 셀 90 % 적중률 `C_score`(dNNe 86.28 · 91.02 · 91.17). 계보 첫 **"오차 막대가 맞는지를 held-out 에서 검사"**. ⚠ 셀 단위로는 흩어진다 — `figure-read ≈` Fig. 4b 보정 뒤 ≈74 %(보정 전 ≈92 %) · Fig. 5b 보정 뒤 ≈100 %(과소 확신). 모드 라벨 0 | **ASSB 0 — 스물일곱 번째 성질 "불확실성을 보정했다 — 분해가 없는 스칼라 위에서."** `identifiab` 0 · `LLI`·`LAM`·`degradation mode` 0 (NFKC 전후 동일). `calibrat` 35 · `uncertaint` 24 · `confidence` 22 인데 `electrode` 2. `[해석]` 축퇴 방향(같은 용량 · 다른 모드)에서 스칼라 예측은 변하지 않으므로 예측 구간은 그 폭을 **구조적으로 볼 수 없다**. 누적 0.5 = 29호 그대로 | **해당 없음** (기준극 0, 흑연 · LFP 액체) | **없다** (`pressure` 0 · `MPa` 0) | **해당 없음** — SI Note 1 리튬 도금은 "hypothesis" | **이동 없음** — LCO · LFP · LCO/NMC(`[인쇄]` "not verified"), OCP 0. 화학은 입력 아님 — 구간 정규화 [0, 1] 로 지운다. ⚠ **이름 충돌**: 이 편의 "α-accuracy · β" = 예측 띠 ±1.5 % · 띠 안 확률 질량(우리 α·β 아님) |
| **Thelen, Huan, Paulson, Onori, Hu, Hu 2024 (`assb` 36호 — 큐 35 · ⚠ **Review 33 쪽, 1차 측정 0, ASSB 0(도구 칸)** · 첫 **확률적 ML 종설**(GPR · RVM · BNN · 앙상블 · 샘플링) · Iowa State + Michigan + **Argonne** + Stanford + UConn · *npj Mater. Sustain.* 2, 14 · CC BY)** | **없다 — `θ(N)` 0/36.** `contact` 1 = Fig. 3 상자 "Loss of electric contact". ★ **분류 체계 여섯 번째 표본 "재작도가 연결을 지웠다"** — 원본(Birkl 2017 Fig. 1)의 `접촉 → LAM_NE/LAM_PE` 연결선이 이 편 Fig. 3 에 **0 개**(`[재현]` 선 객체 = 축선 · 구분선 2 개뿐)인데 캡션은 "their connections to the degradation modes" | **없다.** 종설. 전기 밖 채널은 Prosser 2021(발열 모델) 재인용뿐 | 칸 없음 · **층 하나: interval taxonomy printed (CI ⊂ PI ⊂ TI) — predictive only, diagnostics drawn as point** — 구간의 종류를 정의(pp. 18–19)와 그림(Fig. 13)으로 가른 계보 첫 편. 35호의 `μ ± 2σ` 는 이 정의로 **prediction interval**. ⚠ `[도표]` Fig. 4 여섯 문제 중 **Problem 4(모드 진단)만 불확실성 기호 없이 점**(`θ̂_d`), Problem 1 에는 오차 막대. 모드 진단 원전 13 편 소개에 불확실성 0 | **ASSB 0 — 스물여덟 번째 성질 "불확실성의 분류학을 세웠는데, 데이터를 더 모아도 줄지 않는 파라미터 불확실성의 칸이 없다."** `identifiab` 0. `[인쇄]` epistemic = "reducible" · "Model parameter uncertainty can be reduced by collecting more training data" · CI "collapses to the true value" — `[해석]` 구조적 비식별(곱 · LLI ↔ LAM)은 같은 데이터를 늘려도 능선으로 남는다. 사후(`posterior` 26)는 전부 **ML 가중치**의 사후. 가장 가까운 것은 재인용 Gasper 2021(부트스트랩 파라미터 분포 — "too many fittable parameters"). 누적 0.5 = 29호 그대로 | **해당 없음** | **없다** (`MPa` 0 · `pressure` 2 = 일반 조건 열거) | **해당 없음** | **이동 없음** — 화학 목록뿐, OCP 0. Fig. 15 좌표 `m_p` · `m_n` · `LII`(우리 창 모델의 3-파라미터판) |
| **★★★ Li, Fan, Zhang, Han, Wang, Liu, Jia, Guo, Zhu, He 2024 (`assb` 37호 — 큐 36 · **9호가 모델 · PSO · `A_eff` 정의를 위임한 원전**([27]) · 첫 **각주로 파라미터 층위를 표기한 ASSB 모델 편** · 첫 **이중층을 넣은 복합양극 모델** · SJTU + **Shanghai Firm-lithium(산업체)** · *eTransportation* 20, 100315 · ⚠ **신품만 — 노화 0, `LAM`·`LLI`·`degrad*` 0**)** | **없다 — `θ(N)` 0/37.** 접촉 양은 `A^p_eff` = 0.4938(BV 분모) 하나 — ★★★ **Table 1 각주 없음 · §3 측정 절차 없음 · 조성이 다른 9호 셀(56 ↔ 38 wt%)과 `A^p_eff` · `A^n_eff` 가 네 자리 같다** ⇒ 9호의 "적합값" 은 **출처 없는 상속값**(층: inherited-constant). `[인쇄]` 가정 "when the concentration … is calculated, assuming a uniform current density distribution on the surface" ⇒ `A_eff` 는 용량 · 확산에 없고 과전압에서 **`k_p` 와 정확한 곱**. 입자 통째 비연결의 자리는 `ε_p` 뿐(= `LAM_PE`) | **없다** — GITT · LSV-Tafel · 대칭 셀 이완 · 차단 셀 EIS · SEM 은 전부 신품 파라미터 추출용 | 칸 없음 · **층 하나: footnote-typed parameter table — the contact knob is the unmarked row** (각주 5 종 a–e 인데 `A_eff` · `ε_p` · `c_dl` · `t⁺` 무표기). 부수: `k_p` 인쇄값이 `[도표]` Fig. 5d 측정 11 점 밖(≈0.25×) · **율별 재적합 `D_p,ref(C-rate)`**(0.4 → 2 C ≈4.3 배) · 식 29 불일치(`D^p_SE` ×1.50) · `R_s` "Measured with SEM" 9.315 µm ↔ SI Fig. S1 입자 반경 ≈0.5–1.5 µm(9호 "9 배" 의 원천) | **ASSB 0 — 스물아홉 번째 성질 "접촉 면적의 자리를 새로 만들고, 그 자리가 반응 속도 상수와 곱으로만 들어가는 식을 인쇄한 뒤, 곱의 한쪽은 PSO 로 풀고 다른 쪽은 출처 없이 못 박았다 — 그리고 그 손잡이의 약한 용량 효과를 '가정 탓' 으로 인쇄했다."** `identifiab` 0. "sensitivity analysis" = 0.4 C OAT 6 판(첫 줄). `[인쇄]` `A_eff` 1 ↔ 0.3 "minimal deviation … attributed to the model's assumption of uniform current distribution" — `[재현]` 전압 +61 / −37 mV(RMSE 11.5 의 3–5 배), 용량만 불변. 누적 0.5 = 29호 그대로 | **이동 없음** — 반쪽전지 상대극 Li-In, Fig. 4a "(vs Li)" 환산 미기재. **열세 번째 형태 "차감 흡수"** — OCN = OCP − OCV 라 기준 오프셋이 OCN 에 들어가 완전지 식에서 상쇄 | **이동 없음** — `[인쇄]` SI Table S1 제작 480 · 36–50 · 120 · 360 MPa, 운전 **50 MPa 유지**. 스윕 0 | **해당 없음** (Li-Si) | **이동 없음** — NCM811(LiBO₃)/LPSCl/Li₄.₄Si 기존. 9호 G1 의 답이 절반: 반쪽전지 OCP + 차감 OCN(dQ/dV 봉우리 정렬), 측정 조건 0, `[인쇄]` 분극 포함 인정. OCN `[도표]` ≈0.27 → 0.18 V |
| **★★★★ Conforto, Ruess, Schröder, Trevisanello, Fantin, Richter, Janek 2021 (`assb` 38호 — 큐 37 · **큐의 마지막 편** · 9호 ref [30] · 37호가 Q1 1 순위로 넘긴 편 · Janek 그룹(23호 · 22호 계보) · 첫 **사이클마다(40 회 × 4 조건) 활성 질량을 잰 ASSB 편** · 첫 **두 물리 채널(이완 OCP ↔ 저주파 EIS 꼬리)로 겉보기 감쇠를 분해한 편** · NCM811 PC ↔ SC | Li₆PS₅Cl | In/InLi, ≈70 MPa · SI 미수령)** | **이동 없음 — `θ(N)` 0/38.** 측정 계열은 있다: `[도표]` Fig. 6 활성 질량 N = 40 PC ≈0.63/0.62 · SC ≈0.91/0.90 — 그러나 `m_act = Q_meas/q_act`(이완 OCP 두 점 → `Δx`)는 **`θ·ε_p` 합이고 용량에서 역산**(22호 반 칸 기준 미달). `[인쇄]` "disconnected … cannot contribute to the OCP any longer and can be considered inactive" — **OCV 기반 `LAM_PE` 측정에 기구 이름을 붙였다**; 배정은 "We suggest" + SC ↔ PC + 액체셀 TEM 인용(ref 14). **첫 `θ·(1−LAM)` 합 계열 1/38** | **+0.5** — 한 셀 · 한 사이클에서 두 채널이 "OCP-비활성 질량(`θ`∪LAM)" 과 "확산 경로 연장(`η_diff`)" 을 가른다(22호 신품 `θ ↔ η` 의 노화 · 사이클 해상판) + 동역학 불변 M/H2 봉우리(정성). 반 칸: 카드 핵심 분할(전자 비연결 ↔ 진짜 LAM) 0 · EIS 적합이 OCP 질량을 **고정 입력**으로 받는다 · `[재현]` 이완 1 h ↔ PC 후반 `τ = L²/D̃` ≈13–17 h · n = 1 | measured-electrochemical(두 점 이완 OCP, **기준 OCP–x 를 액체셀에서 수입**) + fitted(GA 다중 시작 중앙값 ± 최대 편차 — 신품 한 판만) · 오차 막대 0 · **닫힘 그림(Fig. 9)에 잔차 0 — `[도표]` (a) +12…+27 · (d) −14…−28 mAh g⁻¹, 본문 "good agreement for all"** | **0/38 — 서른 번째 성질 "식별 한계를 식으로 인쇄하고(`L < √(D̃/f_min)` = 1.8 µm @ 25 °C), 결론의 수를 그 한계 밖에 두었다"**(`L_diff,50` PC 4.8–5.6 µm). 식별 집합에 용량 스케일 없음(`C_diff` 고정) · `[해석]` 반무한 꼬리는 `L/(C_diff√D̃)` 하나 | 이동 없음 — **열네 번째 형태 "고정 전위가 게이지의 영점이다"**(`[인쇄]` "In/InLi anode with fixed potential"; `[재현]` 32 → ≈39 at% 2상역 안 · ±10 mV ≈ 활성 질량 ±4 %) | 보고 · 통제 — 제작 380 MPa 1 min · 운전 ≈70 MPa 고정, 한 값 | 해당 없음 (In/InLi) | 기존(NCM811 PC/SC) — `∂E/∂x` 0.38 V @ x 0.66 한 점(ref 19 차용), `C_diff/m` 520 ↔ `[재현]` 725(×0.72) |
| **★★★★ Sakka, Yamashige, Watanabe, Takeuchi, Uesugi, Uesugi, Orikasa 2022 (`assb` 39호 — 큐 40 · **2차 묶음 첫 편** · 원장 최상위(25호 ref 12 · 33호 ref [120]) · 리쓰메이칸 + **Toyota**(셀 설계) + SPring-8 · 첫 **3D 측정 접촉 면적 분율** · 첫 **압력 → 측정 양극 구조 → 측정 저항** 사슬 · NCM111(LiNbO₃)/LGPS/In–Li, **제조 가압 0 → 0 · 6 · 12 · 50 · 100 MPa**, 신품 · *JMCA* 10, 16602, CC-BY)** | **+0.5 — 표면 피복 `φ(P)`** (CT 화소 0.5 µm): `[인쇄]` "fraction of the area in contact between NCM and LGPS with respect to the surface area of the NCM particles" · `[도표]` Fig. 3c 78.3 / 74.9 / 77.9 / 84.3 / 82.7 %(비단조). **`θ` 아님 · `u`(통째 비연결) 보고 0** — 37호 기준 **`A_eff` 쪽 손잡이**. 반 칸: 신품(**`θ(N)` 0/39**) · 압력 = 제조 압력 · n = 1 · 분할 문턱 0 · ★ `[재현]` **분할이 고정 혼합물의 NCM/LGPS 부피비를 0.47 → 0.97 로 흔든다**(효과 ×1.10 보다 큼) · 0 MPa(공극률 44 %)에서도 `φ` ≈0.78 = 1 µm 아래 틈을 못 가르는 판정 | 이동 없음(**반 칸 검토 후 접음** — CT 는 독립 접촉 관측이나 신품이라 가를 `LAM_PE` 가 없다, 19호 선례) | 층 하나 — **measured-imaging, segmentation threshold unreported, phase ratio not conserved** + fitted ECM `R_ct`(적합표 0, 고압 두 점이 Nyquist 호와 ×2–3) · 오차 막대 0 | **0/39 — 서른한 번째 성질 "곱의 한 인자를 직접 재고, 나머지 인자가 변화의 96 %(로그)를 가져가는 것을 같은 지면에 둔 채 '대응한다' 로 읽었다"** (`[재현]` `R_ct` ×14 ↔ `φ` ×1.10 ⇒ `R_ct·φ` ×13). `uncertaint` · `error` 0 | 이동 없음 — **열다섯 번째 형태 "상대극 계면을 양극 접촉 면적에 흡수한다"**(2전극 `R_ct` 전부를 NCM/LGPS 에 배정, In–Li 언급 = 재료 목록뿐) | **+0.5 — 계보 첫 "압력 → 측정 양극 구조 → 측정 저항" 사슬**: 로드 트랜스듀서 · CT 5 점(공극률 · 부피분율 · `φ` · 굴곡도) · EIS 4 점(CT 와 동시) · 용량(다른 셀 3 점 + 같은 셀 5 단계). `[인쇄]` 제조 ↔ 스택 압력을 정의로 가르고 **자기 실험에서 같다고 명시**("no pressure was added during fabrication … corresponds to … fabrication pressure"). 반 칸: 단조 가압만(S14 되돌림 정성 1 장) · n = 1 · S3 압력 ↔ 사이클 교락(절대 방전은 12 → 100 MPa 에서 감소) · 2전극 | 해당 없음 (In–Li) | 이동 없음 — NCM111(LiNbO₃) · OCP 0. `[재현]` 첫 CE 61 → 27 %(압력 ↑ ⇒ LGPS 산화 분해 몫 ↑, 언급 0) |
| **★★★★ Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2020 (`assb` 40호 — 큐 41 · **2차 묶음 둘째 편** · 지목 5 회(16 · 17 · 18 · 19 · 21호) · **R-LTO 기준극의 원전** · 18호의 방법 원본(ref [27]) · Tokyo Tech + NEDO SOLiD-EV · 첫 **ASSB 3전극 EIS**(`[인쇄]` "first time") · LiNbO₃-LCO\|LGPS\|R-LTO 메시\|LGPS\|Li-In, 210 MPa, 신품 · *Electrochem. Commun.* 116, 106743, CC BY)** | **없다.** `contact` 2 회(고압 서론 · 기준극 전기 접속) · 양극 `θ`/`φ` 0 · **`θ(N)` 0/40** | 이동 없음(**반 칸 검토 후 접음** — 신품이라 가를 `LAM_PE` 가 없고, 분리의 근거가 2전극 = 3전극 합(키르히호프 항등)이다). 기여는 크기 하나: `[도표]` 2전극 적합이 LCO **R2 ×2.7 · R3 ×1.67 과대** — 1 kHz 이상 "양극 호" 의 ≈절반이 Li-In. `[재현]` 고주파 끝 LCO ≈12–13 : Li-In ≈33–35 Ω ≈ LGPS 질량 50 : 160 — **기준극 위치가 분리막 옴을 나눈다** | 층 하나 — **literature-witness offset + sum-identity validation** · ECM(CPE 값 · 잔차 0) · Ea ± = 3 점 회귀 · ★ `[도표]` **같은 상태 R3 세 값 30.6 / 37.7 / 45.5 Ω(×1.49, 스펙트럼 자체가 다름, 설명 0)** — SOC 효과(−7 %)보다 크다 | **0/40 — 서른두 번째 성질 "통과가 보장된 검사로 분리를 검증했다"**(합 항등 + 문헌 증인 일치 — 둘 다 틀린 분해 · 틀린 오프셋에서도 통과). `identifiab` · `uncertaint` · `calibrat` 0 | 이동 없음(**반 칸 검토 후 접음**) — **열여섯 번째 형태 "상호 증언"**: 1.55 V 는 ref [11](Costard 2017, 액체) 수입, 검증 = 환산한 두 평탄(LCO · Li-In)이 문헌 [5,17] 과 "coincident". **누설 0 · 드리프트 0(`leak` · `drift` 0) · Li 대비 0 · n 0 · ±30 mV 없음**. In 가지의 두 뿌리([5] Nam 2018 · [6] = 20호)를 인용하고 Li-In 을 기준극 재료로 기각하며, 상대극 Li-In 의 문헌값을 증인으로 쓴다. `[재현]` 증인 0.62 V 면 R-LTO = 1.5745 V — 1.55 ↔ 1.57 을 못 가른다. 부호 오기 "−0.60 V vs Li"(축은 +0.60) | 이동 없음 — "pressed … at 210 MPa" 한 값, 제조/운전 미구분 | 해당 없음 (Li-In) | 이동 없음 — LiNbO₃-LCO, SOC 5 점 전위 3.86–4.17 V(1.55 V 환산, 휴지 미기재) |
| **★★★★ Nam, Park, Oh, An, Jung 2018 (`assb` 41호 — 큐 42 · **2차 묶음 셋째 편** · 지목 4 회(17 · 20 · 21 · 40호) · **In 가지의 원전이자 계보에서 가장 이른 편(2018-07)** · 첫 **벌크형 ASSB 3전극**(`[인쇄]` "for the first time") · 첫 **기준극 재료 교체 대조**(Li 금속 ↔ Li₀.₅In) · 첫 **상대극 고갈층 단면 관측**(TOF-SIMS) · Hanyang + UNIST + **Hyundai Motor group** 자금 · *J. Mater. Chem. A* 6, 14867, SI 16 쪽)** | **없다.** `contact` 8 회 전부 접속 · 형성, `contact loss` 0. 양극 건전성은 SEM 정성 부정 한 줄(0.2 C 10 사이클) · **`θ(N)` 0/41** | 이동 없음(**반 칸 검토 후 접음** — 겉보기 WE 용량 손실을 CE 로 귀속한 것은 20 · 17호와 같은 층, 시점만 이르다; TOF-SIMS 는 상대극 고갈의 독립 관측이지만 대상이 `LAM_PE` ↔ 접촉이 아니다) | 층 하나 — **cutoff-identity terminal value**: Fig. 3c "CE 종단 전위" = WE 종단 + 0.62 V(컷오프가 WE/CE 에 걸린 항등식) · 기준극 교체 대조는 **수 미인쇄**("marginal difference") · n 0 · Table 1 행 이름 뒤바뀜 | **0/41 — 서른세 번째 성질 "전극 분해를 '진단' 으로 인쇄했다 — 분해가 분리막 옴을 어느 전극 채널에 싣는지 묻지 않고"**(배면형 RE → 옴 전부 CE 채널; "Gr < 0 V" 1 C ≈−0.02 ↔ 반전 계단 절반 ≈0.10 V). `identifiab` · `uncertaint` 0 | **+0.5 — 열일곱 번째 형태 "기준극 교체 대조"**: 본문 0.62 V 는 ref 33(Jung 2008 *AFM*) 수입, 그러나 SI Fig. S2 가 **같은 설계 셀을 Li 금속 기준극으로** 재 `[도표]` Li₀.₅In CE 중점 ≈**0.621 V**(방전 0.6267 · 충전 0.6144) · 두 기준극 셀 차 ≈**2 mV** — P8(재료 축 · 전위)의 첫 실행, 계보 최초. **반 칸인 이유**: 셀 간 · 전류 중 · 전류밀도 미인쇄 · n = 1 · 시간 0 · **수 미인쇄**. 그리고 조건 (2) 붕괴를 **TOF-SIMS 로 본 첫 편**(정성, 대조군 0). 40호 "상호 증언" 의 In 쪽 끝 — 순환 밖 측정 고리가 SI 에 하나 있다 | 이동 없음 — **제조 370 · 운전 74 MPa 명시 구분**(RE 층 74 / 15), 스윕 0 | 해당 없음 (Li-In · Gr · Si–C). ⚠ Gr 위 도금 Li 의 **관통 연성 단락**(Ni-NW 감지극 · ⁷Li NMR 264 ppm) | 이동 없음 — NCM622(첫 사이클 쿨롱 효율 79.1 % < Gr 92.5 % → **방전 끝을 양극이 낸다**) · OCP 기울기 0 |
| **★★★★ Santhosha, Medenbach, Buchheim, Adelhelm 2019 (`assb` 42호 — 큐 43 · **2차 묶음 넷째 편** · 지목 3 회(17 · 20 · 21호) · 인용 6 편(17 · 18 · 20 · 21 · 29 · 38호) · **In 가지 0.62 V 의 실온 측정 원전 — 액체셀** · 첫 **조성 분해 Li 대비 전위 곡선**(쿨로메트릭 적정 0–58 at%) · 첫 **상대극 조성별 고체 대칭셀** · FSU Jena(Adelhelm) · *Batteries & Supercaps* 2, 524, SI 5 쪽)** | **없다** — 양극 없음(CuS 2전극 곡선 둘뿐). ★ 칸 밖: `[인쇄]` "local **decontacting** due to the volume expansion"(InLi 형성 +53 %) — **상대극 자신의** 불활성 In `[재현]` ≈11 %. **`θ(N)` 0/42** | 이동 없음(**반 칸 검토 후 접음** — XRD 가 전기화학과 독립으로 InLi + 잔류 In 을 동정하나 대상이 상대극 상이다) | 층 하나 — **charge-derived composition axis**: at% Li = 통과 전하 ÷ In 몰(쿨롱 효율 100 % 가정, 액체 SEI 형성 인쇄) · 대칭셀 조성은 공칭 질량 — 인쇄 치수로는 44.1 → **49.6 at%**(평탄 끝 47 at% 를 가로지른다). 곡선 1 개 · n 0 | **0/42 — 서른네 번째 성질 "산포를 문장으로 인정하고 대표값을 세 자리로 인쇄했다"**(`[인쇄]` "experimental data scatters" ↔ 그림 "0.622 V"; 산포 크기 · 곡선 수 0). `identifiab` · `uncertaint` 0 | **+0.5 — 열여덟 번째 형태 "다른 전해질의 원전"**: Li 금속 대비 · **액체**(1 M LiTFSI DOL/DME) Swagelok 3전극 쿨로메트릭 적정, 1 h 펄스(`[재현]` ≈0.28 mA; 인쇄 전류 세 값 불일치) + **0.5 h 이완**, 실온(수치 미인쇄) — **평탄 ≈1–47 at% Li(x 0.01–0.89) · 0.622 V · InLi 단상 1.9 at% 에 −280 mV · 0.339 · 0.122 V**. `[도표]` 평탄 안 이완 OCV 0.625 → 0.610 V(**≈15 mV 처짐**, 잔여 분극 방향). **반 칸인 이유**: ASSB 밖 · 곡선 1 개(산포 인정, 수 0) · 이완 미검증 · 고체 셀은 대칭 2전극(Li 대비 0). 두 가지 영점(R-LTO 1.55 — 40호 Costard · In 0.62 — 이 편)이 **둘 다 액체셀 측정**임이 닫힌다; 41호 ASSB SI 판독 ≈0.621 과 ≈1 mV 안 | 이동 없음 — `MPa` 0 · SE 3 t / ∅10 mm(`[재현]` ≈375 MPa) · In/Li 압착 · 운전 미인쇄 | 해당 없음. ⚠ Li-rich In–Li \| β-Li₃PS₄ 저항 증가를 SE 환원으로 **해석**(사후 분석 · EIS 0, 빨강은 ±0.2 V 한계에 눌린 모양) | 이동 없음 — 양극 OCP 0(CuS). 대신 **상대극 OCP(x) 0–58 at%** 가 본체(Q5 쪽) |
| **★★★★ Fukunishi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023 (`assb` 43호 — 큐 44 · **2차 묶음 다섯째 편** · 19호 지목 · **18호와 다른 논문(같은 연구실의 흑연 음극 판)** · 40호 R-LTO 의 직계 후속 · 첫 **음극(흑연) 3전극 EIS + 열화** · 첫 **노화 전후 CPE 삼중(R · T · P) ± 완비** · 첫 **노화 전후 `Ea` 세 성분** · Tokyo Tech + NEDO SOLiD-EV · *ACS Appl. Energy Mater.* 6, 10908, SI 9 쪽)** | **없다 — `θ(N)` 0/43.** 식 (4) `[인쇄]` "the total surface area of the active material particles, **or** the interface area" = `θ ≡ 1` 인쇄(18호 "completely immersed" 와 같은 수법). 접촉 손실은 `[인쇄]` "The decrease in the CPE constant (CPEx-T and CPECT-T) also suggests the loss of contact area" 한 문장 — **`CPE_X-T` 는 ×5.2 증가**(D4). 입도 3 종은 첫 리튬화 비가역 용량의 면적 비례((B)·D 480–630)이지 접촉 분율이 아니다 | 이동 없음(**반 칸 검토 후 접음**) — 채널 셋(3전극 EIS R · T · P 전후 ± · `Ea` 전후 · 전극별 dQ/dV)이 한 셀에 있으나 원전은 **용량 → "loss of the active material"(dQ/dV 높이) · 저항 → 면적 · SEI** 로 채널마다 배정만 했다. `[재현]` 대조: 0.05 C 용량 비 `[도표]` 0.75–0.78 ↔ `R_CT` `C_eff` 비 0.43 ± 0.2 ≈ 1/`R` 0.47(면적 서명) ⇒ 면적 손실 > 용량 손실 — 일부는 피복(`A_eff`)이지 고립 아님; `LAM_NE` ↔ 고립(`u`)은 한 곱에 남는다. 3-a `Ea`(`R_CT` 22 → 27.5)는 반대로 말한다 | 층 하나 — **완전한 CPE 삼중(R · T · P) ± 가 노화 전후 둘 다**(18호는 전 상태 P 만, `C` ± 없음). ± = 적합 표준오차, n = 1, RT 500 → HT 50 이 **같은 셀** 누적 이력. 표 "@293 K" ↔ 본문 298 K(D1). 용량 → `LAM` 은 dQ/dV **높이**(넓이 0) — `[도표]` 봉우리 비 0.53–0.70 · 0.21 V 봉우리 ×1.03 로 균일 비례 모양 아님 | **0/43 — 서른다섯 번째 성질 "채널별 명명 — 같은 셀의 같은 열화를 용량 채널은 `LAM`, 임피던스 채널은 면적 · SEI 로 나눠 부르고 두 채널의 크기를 대조하지 않았다"**. 노화 뒤 세 `Ea` 27.6 · 27 · 27.5 수렴을 "nearly unchanged" 둘 + "decreased" 하나로 읽었다(자기 ± 로 ≈5–6σ, D5). `identifiab` · `uniqu*` · `uncertaint` · `degenera*` · `error` 0; `LAM` 0 이지만 구절 "loss of the active material" 1 | **+0.5 — 열아홉 번째 형태 "공통 모드 표류 판독"**: `[인쇄]` "a small potential shift of ca. 10 mV (negative direction) seen in **both** the graphite and Li−In electrodes, which could be caused by the change of the R-LTO reference electrode potential"(333 K 가속 뒤) — `[도표]` 흑연 dQ/dV 봉우리 리튬화 · 탈리튬화 **둘 다** −13 … −21 mV · Li-In 중점 0.609 → 0.593 V(−16) ⇒ `[재현]` 저항이면 반대 방향 → 공통 모드 ≈−14 mV. **R-LTO 가지 첫 표류 값.** 값은 또 인용(`[인쇄]` "**Suppose** … 1.55 V … [40,41]" Colbow · Ohzuku = 18호 경로), 증인은 흑연 단계 평탄 셋(GITT 0.195 · 0.110 · 0.068, 문헌값 미인쇄) + Li-In "0.60"([44] = 42호, 원전은 0.62 — D13). **반 칸인 이유**: "could" · n = 1 · 두 시점 · 같은 지면이 S2 합 일치로 "**proves** the stability"(범주 오류) · `[재현]` 0.622 대입 시 R-LTO ≈1.568(세 번째 ≈1.57). 컷오프 부호 오기 D7(계보 세 번째) · `leak` · `drift` 0 | 이동 없음 — 조립 110 · Li-In 압착 ≈100 MPa, 운전 압력 0, `pressure` 0 회(void · crack 은 서론 인용) | 해당 없음 — 흑연(컷오프 0 V vs Li 는 1.55 V 가정 위; `[재현]` R-LTO 1.568 이면 실제 ≈+18 mV) | 해당 없음(양극 없음). 칸 밖: **ASSB 안 흑연 준-OCP**(GITT 0.195 · 0.110 · 0.068 V) — 단계 평탄 = 음극 판 평탄 축퇴 재료 |
| **★★★ Jin, Park, Park, Lim 2015 (`assb` 44호 — 큐 45 · **2차 묶음 여섯째 편** · **20호의 셀 원전**(20호 ref [12]) · 같은 연구실(창원대 Lim) · 같은 레시피, **같은 셀은 아님**(SE 0.36 ↔ 1240 µm · 기준극 없음) · Li₄.₄Si 음극 7 설계 · *Electrochim. Acta* 185, 242, SI 없음)** | **없다 — `θ(N)` 0/44.** 신품 설계 비교(9–14 사이클). "effective contact area" 3.19 cm²(×2)는 **GITT `√D·S/θ` 곱**의 한 인자를 대조 셀 가정(Case 1 `S` = 기하 · 두 셀 `θ` = 1)으로 뗀 값 — `[재현]` 셋째 계단 하나(계단별 `S` 4.13 / 3.67 / 3.18) · 자기 BET ×8.7 ↔ ×2.07 · SEM 정성 한 장 · `contact loss` 0 | 반 칸 검토 후 접음 — 채널 다섯(BET · GITT · 2전극 EIS · dQ/dV · SEM)이 있으나 **열화 없음**; 용량 차는 "접촉 면적"(입도) · "전자 접촉"(`[인쇄]` "cannot numerically determine … it is obvious") · "수송 촉진"(구배)으로 **서술 배정**, Case 5 → 6 은 다섯 변수 교락. `[재현]` **Li 재고 수지 위반**(Case 6 2 방전 뒤 TiS₂ x ≈1.37 · Case 4 ≥1.04) — 방전 용량 일부가 TiS₂ 삽입이 아니다(우리 계산) | 층 하나 — **reference-cell-anchored product split**: 측정 곱을 대조 셀 가정으로 쪼개 한 인자에 이름; 인쇄 `D` 1.0 × 10⁻⁸ · `S` 3.19 = 세 계단 중 셋째 · Table 2 `ΔE_t` 78–99 mV ↔ Fig. 6 `[도표]` ≈40–45 mV(×≈2) · n = 1 · 오차 0 | **0/44 — 서른여섯 번째 성질 "대조 셀 가정으로 곱을 쪼갰다 — 그 가정의 근거(작업전극에 전해질 없음)가 처리 셀(Case 2)에도 그대로 성립하는데"**. `identifiab` · `uncertaint` · `fit*` · `error` 0 | 이동 없음 — **스무 번째 형태 "GITT `ΔE_s` 분자 안의 상대극 평탄 가정"**: 반쪽 Case 1/2 의 상대극이 **비리튬화 In 박**(질량 미인쇄), `0.62` · `plateau` · `assum*` 0 회. `[도표]` 같은 화학 두 셀의 이완 전압 0.434 ↔ 0.529 V(≈95 mV) · 이완 봉투 ≈0.1–0.2 V / 참여 2–6 % — **Li-Si 는 평탄 상대극이 아니다**(우리 판독이라 칸 밖) | 이동 없음 — 제조 **30 MPa** `[인쇄]`(SE 펠릿 · 셀 순차 압착) · 운전은 **Fig. 1 그림에만**("30MPa" 화살표 + "High oil pressure", 본문 0) · `pressure` 2 회 둘 다 가설(자료 0) · 스윕 0 | 해당 없음 — Li-Si 합금 | 이동 없음 — TiS₂(20호와 같은 화학) · 준-OCP 0. 칸 밖: Li-Si vs In 반쪽 GITT 이완 곡선 = 음극 판 평탄 전제의 반례 재료 |
| **★★★★ Hertle, Walther, Mogwitz, Schröder, Wu, Richter, Janek 2023 (`assb` 45호 — 큐 46 · **2차 묶음 일곱째 편** · 지목 2 회(16 · 21호) · **"0 V 리튬화 금선" 관례의 원전**(16호 ref [24]) · JLU Giessen(Janek) + **BASF** · *J. Electrochem. Soc.* 170, 040519, CC BY-NC-ND · 방법 논문, 신품)** | **없다 — `θ(N)` 0/45.** 신품 · `contact` 6 회 중 접촉 손실 0 · 사후 SEM 은 기준극 둘레 균열 정성 | 반 칸 검토 후 접음 — ① 2E 임피던스 분할 비유일성(`[인쇄]` "Both sets of parameters fit … equally well", Table S1 `R_Anode` 14 ↔ 3.9 Ω cm²)을 같은 셀 3E 음극 반쪽(S7, 호 ≈12–13)이 **Fit 1 로 고른다는 것은 우리 판독**(저자 미판정) ② 율 시험 2E 방전 부족(0.1 C `[도표]` 165 ↔ 3E 193)은 **LTO 상대극 Li 소진**(`[인쇄]` "no lithium excess" · "side reactions that are consuming Li") — 전극별 용량 귀속은 20 · 17 · 41호와 같은 층 ③ 열화 0 | 층 하나 — **in-cell plated reference**: 영점 = 도금 Li 상 정체 · 측정 축 차 −618 mV 인쇄 · 안정성은 기간("≥8 일")만, 추적 0 · 3E TLM 두 값(σ_eff 0.145 mS cm⁻¹ · R_CT 17.8 Ω cm²) ± 0 · n 미기재 | **0/45 — 서른일곱 번째 성질 "두 적합 병치로 비유일성을 인쇄하고, 3전극에서는 '물리적 의미' 로 한 모델을 골랐다 — 어느 쪽에서도 폭을 재지 않았다"**. `identifiab` · `uncertaint` 0 · `ambigu*` 2 · `unequivoc*` 3 | **+0.5 — 스물한 번째 형태 "셀 안 도금 Li: 영점을 상 정체(평탄 사다리)로 정하고, 기준극을 수명 있는 소모품으로 인쇄했다(재리튬화 'refresh')"**. `[인쇄]` Fig. 7 측정 축 −618 mV vs In/InLi(계보 첫 ASSB 안 Li 금속 ↔ In/InLi 인쇄 수; 42호 액체 0.622) · "≥8 일" · 실패 기구(얇은 Li 소진 · Au–Li 평탄 SE 환원). `[도표]` 사다리 AuLi/AuLi₃ 개방회로 −0.485 ↔ 도금 −0.618 V ⇒ 0.133 ↔ 문헌 0.134 V. 표류 수 0 · `drift` · `leak` 0 — **누설 0/45** · `[재현]` 소진 가정 소비 ≈39 nA. 16호 이식은 조건 밖(∅25 · 면적당 1/9.6 · NMC 상대 · 평탄 무) | 이동 없음 — 제조 2E 382 · 3E 40 → 374 MPa · **운전 63.7 MPa** 명시(알루미늄 틀) · TSRE "little to no pressure" → 성능 저하(정성) · 스윕 0 | 해당 없음 | 이동 없음 — NCM851005(BASF) · OCP 0. 칸 밖: LTO 평탄 vs 도금 Li `[도표]` ≈1.55 V(±≈10 mV — 1.55 ↔ 1.57 불가분) |
| **★★★ Schlenker, Stępień, Koch, Hupfer, Indris, Roling, Miß, Fuchs, Wilhelmi, Ehrenberg 2020 (`assb` 46호 — 큐 47 · **2차 묶음 여덟째 편** · 21호 ref 17 · **Au 도금 W 선 기준극의 계보상 가장 이른 ASSB 사용**(2019-12 투고) · KIT IAM + **Bosch** + **Marburg(Roling · Miß — 16호 공저자)** · *ACS AMI* 12, 20012 · Li\|Li₆PS₅Cl\|Li 대칭셀, 양극 없음)** | **없다 — `θ(N)` 0/46.** 양극 없음. Li\|SE 계면 면적은 `[인쇄]` "R ∼1/A" 로 **추론**, 면적 측정 0 (`contact area` 19 · `interface area` 14 — 계보에서 가장 짙은 면적 어휘) | 반 칸 검토 후 접음 — 음극 계면 "면적 ↔ SEI" 를 XPS(화학, S 2p ≤6 at%) + 3E EIS(박리 쪽 R3 `[도표]` ≈1.5 → 8.8 Ω, 도금 쪽 감소) + 면적 비대칭 셀(Fig. 7, 크기 미인쇄) + 압력(Fig. 6, **다른 SE**) 네 채널로 **논증**, `[인쇄]` "Still it is an open question if this effect of interface area is stronger than the influence of the SEI" · 양극 `LAM` 대상 0 | 층 하나 — **voltage-shape failure label + undefined error bars**: 단락 = `[인쇄]` "A sudden voltage drop indicates a short circuit" 한 기준 · Fig. 8 오차 막대 정의 · n 미인쇄 · Fig. 1e 점 3 개(적합선이 가운데 점 ×3 빗나감) | **0/46 — 서른여덟 번째 성질 "'A 또는 B' 를 인쇄하고 두 갈래를 같은 이름('decreasing active contact area')으로 끝냈다 — 스스로 'open question' 이라 적은 쪽을 결론의 'main focus' 로 올렸다"**. `identifiab` · `uncertaint` 0 | 이동 없음(**반 칸 검토 후 접음**) — **스물두 번째 형태 "영점이 들어가지 않는 자리: 같은 금속 대칭셀의 AC 분할 전용"**. Au 도금 W 선을 SE 분말에 매립 · 540 MPa 공동 압착 · `[인쇄]` "plated with lithium from both electrolytes [sic] to reach a constant potential of the reference" — 전하 · 전위 값 · 선 지름 **미인쇄**, `leak` · `drift` · `calibrat` 0 — **누설 0/46**. ★ 계보 판정: 21호 "Schlenker → Hertle → 16호" 는 **두 줄의 합류** — 하드웨어 · 저자(Marburg: 이 편 → 16호) + 영점(Giessen: Hertle → 16호 [24]); 이 편은 영점을 쓴 적이 없다(우리 판독) | 이동 없음 — 제조 540 MPa · 운전 0.1 kN(`[인쇄]` "only about 6 MPa", `[재현]` 0.126 cm² 면 8.0 · 0.16 cm² 면 6.3 MPa) · 스윕 4.4–44.2 MPa 는 **다른 SE 셀**(LiI–Li₃PS₄ 유리). 층 하나: **감압 이력** — `[도표]` R_Ws 13 → ≈32 Ω 되돌아옴, 고주파 절편 ≈97 → ≈89 Ω 은 안 돌아옴 | 이동 없음 — Li 대칭셀(무음극 아님). SEI 는 XPS 로 **찾았고 뚜렷하지 않았다**(보류) · `dead` 0 · `Coulomb*` 0 · 단락 = 전압 급락 한 기준, `[도표]` 붕괴가 여러 계단 · 단락 전 반주기 전압 ×≈0.7 감소(접촉 개선 ↔ 연성 단락 불가분 — **대칭셀은 OCV ≡ 0 이라 개방회로 서명이 없다**) · `[재현]` 한 전극 순 이동 ≤ 재고 3 % — Li 소모는 제한 기구 아님 | 해당 없음 — 양극 없음 |
| **★★★ Solchenbach, Pritzl, Kong, Landesfeind, Gasteiger 2016 (`assb` 47호 — 큐 48 · **2차 묶음 아홉째 편** · 지목 2 회(21호 ref 11 · 45호 ref [20]) · **금선 기준극(GWRE) 원전** · ⚠ **액체셀 · ASSB 아님**(LP57, Swagelok T-셀) · TUM(Gasteiger) · *J. Electrochem. Soc.* 163, A2265, CC BY · SI 없음)** | **없다 — `θ(N)` 0/47.** 액체 · 접촉 손실 대상 없음(`contact` 6 = 집전체 · 하우징 접촉 저항) | **해당 없음(액체) — 도구 칸.** 3전극 끝점 이동(흑연 방전 끝 `[도표]` +0.15 → +0.87 V vs GWRE · LFP 2.15 → ≈3.0 V)을 `[인쇄]` "the SOC of both electrodes slip" → `LLI` 지배로 **해석**(정량 · `LAM` 대조 0, 셀 1 개). 기준극 검증 셋을 범주별로: 위치(고주파 절편 대칭) · 분배(재조립 대칭셀) · 표류(PEIS ↔ GEIS) | 층 하나 — **external-partition-validated**(재조립 대칭셀 대조 "essentially identical" ↔ `[도표]` 흑연 호 폭 −9 % · 높이 −21 %, 같은 상태 다른 그림 ×0.63 — 산포 기준 없음) + **undefined n = 2 error bars**(Fig. 8) | **0/47 — 서른아홉 번째 성질 "검사마다 맞는 범주를 골랐고(위치 · 분배 · 표류), 판정의 분해능(같은 지면의 셀 간 산포)을 대지 않았다"**. `identifiab` · `uncertaint` · `Kramers` 0 | 이동 없음(**반 칸 검토 후 접음** — 액체) — **스물세 번째 형태 "원전 측정: Li 대비 개방회로를 수백 시간 추적하고, 영점의 사용 조건(초기 창 제외 · 리튬화 온도 = 운전 온도 · 절단면 노출 · 재리튬화)을 같이 인쇄"**. `[인쇄]` 0.311 V = LixAu(0 < x < ∼1.2) OCV · "> 500 h … < 2 mV after the initial 20 h" ↔ `[도표]` 20 h 뒤 ≈3 mV · 40 °C 리튬화 −1–2 mV · 25 °C 리튬화 → 40 °C ≈60 h 이탈. 누설 0/47, `[재현]` < ≈0.27 nA. **0.31 V = 사다리 맨 위 칸 · 0 V(45호) = 맨 아래 칸**. 21호 교정 이식 = 값 + 절차(안정성 명제 아님), 원전 조건 둘(노출 ×40 · 2 h 판독) 이탈 | 해당 없음 — 스프링 T-셀(값 0) · `MPa` 1 = 전극 압연 260 | 해당 없음 | 해당 없음(액체 LFP/흑연) — 칸 밖: LFP 평탄 3.11 V vs GWRE → 3.42 V vs Li |
| **★★★ Dugas, Dupraz, Quemin, Koç, Tarascon 2021 (`assb` 48호 — 큐 49 · **2차 묶음 열째 편** · 21호 ref 16 · **전면 Li₀.₅In : SE 복합 기준층**(링은 15 µm Al 집전체 — 21호 "circular … around the outer perimeter" 는 집전체를 읽었다) · 축대칭 기밀 3전극 셀 · Collège de France(Tarascon) · *J. Electrochem. Soc.* 168, 090508 · SI 없음 · 열화 0(최대 10 사이클))** | **없다 — `θ(N)` 0/48.** `contact` 3 = 기준극 전기 접점. `[인쇄]` 손 분쇄 LTFS 용량 초기 증가(`[도표]` ≈157 → ≈177 mA h g⁻¹)를 "could slightly improve the double percolation" 으로 — **접근 분율 증가 가설**, 측정 0 | **없다** — LTFS `R_CT`(SOC, N) 연속 추적(최대값 5 사이클 끝 1500 Ω cm²)은 **소거법 배정**(`[인쇄]` "β-LPS … not expected to be dependent on the state of charge") · 원인은 충방 비대칭 → 음이온 경로(`k` 쪽)로 해석 · 용량 분해 0 | 층 하나 — **fit-by-elimination + removal-test flag**: 호 정체를 기대로 소거해 지정 · `[인쇄]` "only indicative … the quality of the fit is not altered upon removal" · "repeated at least twice" 산포 0 | **0/48 — 마흔 번째 성질 "비식별성을 두 번 인쇄했다(2전극 합이 한 전극 모형으로 'satisfactory' 적합되며 중간 호 ×2.2 틀린다 · 제거해도 적합이 안 변하는 호는 지표일 뿐) — 폭은 재지 않았다"**. `identifiab` · `uncertaint` 0 · `decorrelat*` 1 | **+0.5 — 스물네 번째 형태 "같은 재료 기준극으로 상대극 창을 재고, 그 창을 용량 오차로 번역해 2전극의 허용 조건을 인쇄했다 — 축은 끝까지 'vs LiIn/In'"**. `[인쇄]` CE ±160 mV(β-LPS) → ±20 mV(argyrodite) "so that a 2 electrodes configuration can safely be employed … (20 mV correspond to ⩽2 mA h g⁻¹ at end of charge for NMC)" · 영점 = 인용 622 mV(42호) 한 번, **2전극 귀속 전제로**(3전극 환산 0) · 기준극 Li₀.₅In `[재현]` 33.3 at%(창 안) · 안정성 "hundreds of hours"(TiS₂ 680 h 곡선 겹침, 수 0) · **누설 0/48**. `[도표]` Fig. 10a Li 박 상대극 휴지 끝 **−0.62 ± ≈0.01 V vs LiIn/In**(우리 판독 — 셀 안 Li 증인, 원문 명제 0) | 이동 없음 — 제조 4 t cm⁻²(≈392 MPa) · 운전 1 t cm⁻²(≈98 MPa, 초기 토크 교정) · Li 셀 45 kg cm⁻²(≈4.4 MPa). 층 하나: **"분극 200 → 500 mV 는 압력 탓(simply originates)" 이 음극 교체와 교락** | 해당 없음 — Li 금속 CE 3전극 EIS 가 도금(저주파 호 성장, 5.6 · 3.7 mHz) · 박리(kHz 호 성장)의 주파수 영역을 가름, 해석은 가설("resistive layer" · "porosity") | LTFS(음이온 산화환원) · NMC622 · TiS₂ — OCP 수치 0 |
| **★★ Barai, Uddin, Widanage, McGordon, Jennings 2018 (`assb` 49호 — 큐 50 · **2차 묶음 열한째 편** · 20호 ref [24] · ⚠ **액체셀 · ASSB 아님**(상용 20 Ah LFP/흑연 파우치, 50 % SoC · 25 °C 한 상태) · 첫 **"측정 시간 척도 ↔ 저항 값" 교차 방법 비교**(DC 단일 · 다중 진폭 · 전환 펄스 · 1 kHz · EIS · 펄스-다중사인) · WMG Warwick · *Sci. Rep.* 8, 21, CC BY · SI 없음)** | **없다 — `θ(N)` 0/49.** 액체 · `contact` 0 회 | **해당 없음(액체) — 도구 칸.** 5 방법의 **총량**이 EIS \|Z\|(t = 1/f) 한 곡선에 모인다(`[재현]` 5 C: −6 … +11 %) — 시간 ↔ 주파수 **일관성**(31호 형태의 원전), 성분 분리는 원문이 스스로 사양(`[인쇄]` "inability to completely separate" · `R_p` "not well-defined" · "pre-defined"). 같은 이름이 방법마다 `R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13 | 층 둘 — **window-differenced reads under a declared convention**(성분 = 0.1 · 2 · 10 s 또는 251 · 2 · 0.1/0.01 Hz 읽기의 차, 규약 t = 1/f 는 "square wave … highest harmonic" 한 문장) · **unstated-origin ±, column-constant**(저율 두 열 = 1 mV ÷ I 와 일치 — 셀 수 미인쇄) | **0/49 — 마흔한 번째 성질 "비식별을 두 곳에 인쇄하고 결론에서 지웠다"**: 적합의 비유일성(`[인쇄]` "not uniquely identifiable" · "ambiguities … Ro and RCT" · "judged solely on closeness of fit") + 작도의 비분리("inability … to separate" · "usual prescription" · `R_p` "pre-defined") ↔ 결론 "EIS can accurately provide separation and identification of all the individual resistance components". 창 의존성은 식별 불가가 아니라 **시간 척도 정렬의 일관성**으로 처리. `[해석]` 적합된 직렬 R = **여기 대역 위쪽 끝의 \|Z\|**(다중사인 1.62 = \|Z\|(1 Hz) · DC 0.1 s 1.33 ≈ \|Z\|(10 Hz)) — 대역 끝이 값을 정한다. `identifiab` 3(파라미터 뜻 2) | 해당 없음 — 2전극 파우치, 기준극 0 | 없다 — `pressure` · `MPa` 0 | 해당 없음 | 해당 없음(액체 LFP/흑연) — `[인쇄]` 평탄 70–40 % SoC 라 10 s · 15 C 의 4.2 % SoC 변화 "little impact", 가파른 OCV 에서는 "more pronounced" — OCP 수치 0 |
| **★★★ Miß, Ramanayagam, Roling 2022 (`assb` 50호 — 큐 51 · **2차 묶음 열두째 편** · 16호 ref [30] = **16호 TLM 방법의 원본** · Univ. Marburg · *ACS AMI* 14, 38246 · 단결정 LCO · NMC83\|6\|11(둘 다 LiNbO₃) \| 0.67 Li₃PS₄·0.33 LiI \| In, 389 MPa 제조 = 운전, 두께 4 점 · ⚠ **열화 0 — 신품 2 사이클째 SOC50**)** | **없다 — `θ(N)` 0/50.** ★ 그러나 **`a_v = 3ε_CAM/r_CAM` "in contact to SE" 의 출생지**(16호가 옮긴 문장) — 접촉 분율 ≡ 1 을 이름 붙여 가정 · 초록이 `[인쇄]` "These contacts determine the Li⁺ exchange current density" 로 `j₀` 를 접촉이 정한다고 정의 · FIB-SEM/EDX 단면(Co · Ni · Mn · P · S)은 **반경 확인에만** | **부분 — 신품, 방법 원전.** 두께 4 점 × 2 재료로 `R_ion ∝ d` ↔ `R_CT/(a_v d) ∝ 1/d` 분리 — **NMC 만 전이 구간을 가로지른다**(`[재현]` 비 0.45 → 23) · **LCO 는 네 두께 전부 두꺼운 극한**(92 → 4,300) → `√(R_ion·R_CT/(a_v d))` 한 조합, `[인쇄]` 모형 두께 추세 불일치 "unclear at present" · 대칭 음극셀 반 빼기 · 차단셀 σ_eon/σ_ion(σ_ion 은 총량의 5.6 % 차분, `[재현]` τ ≈3.0 ↔ TLM 6.8). `LAM_PE` ↔ 접촉 손실은 대상 아님 | **simulation-matched, 목적함수 미인쇄** — `[인쇄]` "simulations … compared" · "good agreement"(`fit*` 4 회는 전부 `j₀` 밖) · 재료당 공유 6 파라미터(`j₀` · `Q_DL` · β "freely adjustable" + τ · `D` · `dU/dc` "variables", 시작값 문헌/1/30 C OCV) + NMC 고주파 R‖CPE 적합 · ± 0 · n 미인쇄 | **0/50 — 마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다"**: `[인쇄]` 수정 (ii) `a_v·τd → a_v·d`("for improving the agreement", 기하 논증) = `[재현]` `(j₀, Q_DL, dU/dc) → (j₀/τ, Q_DL/τ, τ·dU/dc)` 의 정확한 재척도(식 (1)이면 `j₀` LCO 25.8 → 4.2 · NMC 0.11 → 0.016 A m⁻², 대수 미인쇄) + 곱만 보이는 두꺼운 극한의 LCO 값 보고 → 모형 불일치 "unclear" → 비 논증 "leaves no doubt". 식별성 낱말 전수 0 | 기준극 0 · 축 "vs. In/InLi"(그림만) · **대칭셀 반 빼기**(40 at% · 조립 125 MPa 한 점 → `[재현]` ASSB 음극 ≈5–30 at% · 389 MPa, 양극 두께와 함께 증가) · `[도표]` LCO 52 µm 에서 뺀 −Z″ 가 ≈10–120 Hz 음수(과차감) — **스물다섯 번째 형태 "대칭셀 반 빼기"** · `dU/dc` 시작값은 완전지 전압 기울기(음극 평탄 암묵 가정) | 389 MPa 제조 = 운전 **한 점**(분리막 선압 97 · 대칭셀 125 · SE 펠릿 276). 초록 "under the application of stack pressures in the range of 400 MPa" 는 **압력을 바꾸지 않고** `j₀` 에 붙인 문장 — 결론이 "should be studied" 로 미룸 · 16호가 그 후속 | 해당 없음(In 음극) | **LCO + NMC 83\|6\|11**(LiNbO₃ ≈12 nm 구입 ↔ 1 wt% 졸–겔) · `dU/dc` 시작 `[인쇄]` −2.024 / −3.358 × 10⁻⁵(S6 범례, 1/30 C 충·방 평균) → 적합 −2.65 / −3.59 × 10⁻⁵ V m³ mol⁻¹(×1.31 / ×1.07) · `[도표]` 첫 방전 ≈170 / ≈171 mAh g⁻¹(인용 범위 180–200 · 190–200 아래) |
| **★★ Illig, Ender, Chrobak, Schmidt, Klotz, Ivers-Tiffée 2012 (`assb` 51호 — 큐 52 · **2차 묶음 열셋째 편** · 지목 3 회(18호 [29] · 11호 [9] · 47호 [35]) · ⚠ **액체셀 · ASSB 아님**(LFP 70:24:6 \| 1 M LiPF₆ EC:EMC \| Li 금속, 반쪽 + 두 대칭셀, 신품 10 사이클 뒤) · IWE KIT · *JES* 159, A952 · SI 없음)** | **없다 — `θ(N)` 0/51.** 이 편의 "접촉" 은 **양극층 \| Al 집전체**(`[인쇄]` "contact resistance (cathode/current collector)") — `contact` 20 회 중 CAM–전해질 · 입자 접촉 0. `[해석]` 전자 접촉 — 카드의 CAM\|SE 이온 접촉과 다른 물리 | **해당 없음(액체) — 도구 칸.** 직렬 두 호의 **이름**을 DRT 대역(1 kHz ↔ 1–8 Hz) + 대칭셀 배정 + `Ea`(P1C 0.45 ↔ P2C 0.06 eV) + SOC(P1C ×270 ↔ P2C 거의 무관)로 가르고 캘린더링 한 쌍으로 **방향만** 확인(두께 · 공극률 · 두 면적 동시, 음극도 변함). `[재현]` Table I → `C` P2C ≈1 µF · P1C ≈3 mF cm⁻² — **두 호는 `C` 세 자릿수로 갈린다**(저자 미사용). 곱 `A·j₀`(한 호 안)는 대상 아님 | **DRT-seeded CNLS ECM, 물리 이름은 소거 + 가정 + 문헌** — `[인쇄]` "a transfer process is always temperature activated" · P2C = "another cathodic process" + Gaberscek 2008 · ± 0 · 셀 1 · `[재현]` "178 ± 50" = Table II 범위 반폭 · `Q` · `n` · λ 미인쇄 | **0/51 — 마흔세 번째 성질 "불안정한 적합을 요소 제거로 안정시키고, 제거된 몫이 흘러갈 곳(주인공 호)을 스스로 인쇄한 뒤 '선험 설정 없음' 으로 닫았다"**: `[인쇄]` "The CNLS fit becomes unstable when including this additional loss process … neglected … overlaps with P2C" · Li\|Li 저주파 봉우리 "influence either … solid state diffusion or P3" ↔ 결론 "without any a priori settings". 식별성 낱말 · λ 전수 0 | 해당 없음 — 기준극 0, 대칭셀은 AC 전극 배정에만(빼기 없음) | 없다 — `pressure` · `MPa` 0(압연 압력 미인쇄) | 해당 없음 — Li 금속 덴드라이트 가설("Probably") | 해당 없음(액체 LFP) — OCP 0 |
| **★★★ Oh, Kwon, Choi S.H., Lee N., Sohn, Lee T., Lee T., Kim J.Y., Bae, Choi J.W. 2025 (`assb` 52호 — 큐 53 · **2차 묶음 열넷째 편** · 지목 2 회(13호 [34] · 14호 [10]) · **14호와 같은 연구실**(서울대 + HMG-SNU JBRC + 현대차) · *Adv. Energy Mater.* 15, 2404817 · MgSiGr(Mg 200 nm 위 SiGr) 과충전 음극 \| LPSCl \| LiNbO₃-NCM811, 펠릿 + 20 × 20 mm² 파우치, 25 °C · 본문 10 쪽 + SI 28 쪽)** | **없다 — `θ(N)` 0/52.** 접촉 관측은 **음극 \| SE XRM 한 쌍**(반쪽전지 · 첫 과충전–방전 1 회 뒤 · 압력 미인쇄) — `[인쇄]` "substantial contact loss along the interface" ↔ "interface porosity was much lower", **수치 · 문턱 0**, `[도표]` 두 기공 지도 모두 넓게 칠해짐. 양극 접촉 0 | **없다(양극).** 3 MPa 고정 **음극 교체**(SiGr · Li 10 µm · MgSiGr) · SEM-EDS · XRM · 반쪽 EIS(`R_B` · `R_CT` · `R_SEI`) — 전부 음극 계면. 양극 EIS · 영상 · 사후 분석 0 | **measured-2electrode + imaging-qualitative + ECM(EC-Lab, 인쇄 값 두 개)** · 실패 라벨 = 전압 잡음 · 무한 충전 · `R_B` 급감(`r_SS` 병렬 도식 S17) · ± 0 · 조건당 셀 1 · ⚠ **3 MPa CE 는 그림에만**(`[도표]` ≈85–97 %) | **0/52 — 마흔네 번째 성질 "가역성의 지표(CE)를 인쇄한 조건에서만 인쇄했다"**: 20 MPa "impressive average CE of 99.2 %" 는 본문, 3 MPa CE 는 그림에만 · 같은 지면 유지율과 대조 0(`[재현]` ∏CE 0.55 ↔ 83.7 %). 식별성 낱말 전수 0 | 해당 없음 — In 0, 반쪽전지 영점 = Li 박 상대극(박리 과전압이 도금 mV 판독에 섞임) | **반 칸 검토 후 접음.** 운전 **20 · 3 MPa**(스프링 — 상수 · 변위 · 계측 0) · 파우치 **3 MPa**(볼트 3.5 N·m — 변환 0) · 제조 150 · 380 · WIP 450 MPa 명시 · **반쪽 압력 미인쇄** · ⚠ 두 압력이 양극 적재 20 ↔ 6 mg cm⁻² · N/P 0.15 ↔ 0.66 과 **교락**(요인 설계 아님) · 저압 지배 인자 "음극 계면" = 3 MPa 고정 음극 교체로만 · MgSiGr 저압 감쇠 원인은 해석 한 줄 · 33호 띠(0.4–5) 안의 1차 운전값 | **없다.** 무음극형(도금 Li 가 용량의 85 · 34 %)인데 dead ↔ SEI 0 · `[재현]` 3 MPa 누적 충–방 결손 ≈575 mAh g⁻¹ > NCM811 Li 재고 ≈275 — **CE 결손 ≠ `LLI`** | NCM811(LiNbO₃) · OCP 0 |
| **★ Ren, Danner(공동 1저자), Moy, Finsterbusch, Hamann, Dippell, Fuchs, Müller, Hoft, Weber … Barai … Latz, Srinivasan, Janek, Sakamoto, Wachsman, Fattakhova-Rohlfing 2023 (`assb` 53호 — 큐 54 · **2차 묶음 열다섯째 편** · 02호 ref 17 · ⚠ **Perspective 34 쪽, 1차 측정 0 — 1차 기여는 P2D 사례 계산 하나** · LLZO 산화물 공소결 복합양극 · DLR(Danner · Latz) + FZJ + JLU(Janek) + ANL(Barai · Srinivasan) + KIT(A. Weber) 외 · *Adv. Energy Mater.* 13, 2201939, CC BY-NC)** | **없다 — `θ(N)` 0/53.** 자기 P2D 는 `θ ≡ 1`(`[인쇄]` SI "percolating network … full utilization" · "completely dense composite … without any porosity" · "Electrochemical and mechanical degradation processes are also neglected"). ★ **공백을 인쇄**: "There is yet no experimental study that incorporates percolation theory and its influence on mechanical degradation" · "no experimental technique has successfully estimated the fracture strength between the CAM and SE particles". 가리키는 `N` 축 원전 = 모델 1([127] Barai 2021 "ten cycles without showing saturation") + 산화물 용량 곡선 재인용 4([83] 1.8 → 0.4 / 100 · [104] 2.75 → 1.3 / 10 · [105] 1.2 → 0.8 / 5 · [12]/[83] 50–60 % / 50) — 접촉 분율 0. ⚠ 시간 배정: 첫 사이클 = 산화 · 이후 = "fatigue"(인용 0) — 인용 [103] = 23호는 반대 배정(33호에 이은 두 번째 역전) | **반 칸 검토 후 접음.** 산화물 특유의 **공정 대조** — FAST/SPS 치밀(≈95 %) 셀 "cracking … ruled out … electrochemical degradation"([105] 재인용, 근거 채널 · n 0) — 재가압(4호)과 반대 방향의 조작(막는다) | 층 하나: **계 간 이식 파라미터** — `[인쇄]` "In the absence of data on NMC811/LLZO interfaces, we define this resistance [LCO/LLZO ≈2600 + 황화물 NMC811 'similar'] as the state of the art" · OCV = 액체 18650 모델 곡선 · 결정론 사례 계산 | **0/53 — 마흔다섯 번째 성질 "분해 불가를 인쇄하고 가정으로 한쪽에 몰았는데, 표는 두 칸에 같은 값을 넣었다"**: `[인쇄]` "Deconvolution of the contributions in impedance data is challenging … we assume that most of the interfacial impedance can be attributed to resistive secondary phases" ↔ Table 3 `R_CT` 2600 = `R_SP` 2600 · OAT 스파이더 + "the order of the improvements is also crucial"(교호작용 인정, 정량 0) | 해당 없음 — Li 금속 설계. ⚠ 재수록 Fig. 4a 축 "V vs In-Li" ↔ 캡션 "Li metal anode" | **없음** — 산화물 셀 운전 압력 0(`MPa` 7 중 6 응력 · 강도, 1 황화물 ">10 MPa … impractical") · `[해석]` 소결 결합 파단은 재가압으로 안 되돌아간다 | 해당 없음 | 부분 — NMC811 OCV(SI-1a) = Sturm 2019 액체 18650 원전 · 평균 방전 전압 LCO 3.96 · NMC622 3.82 · NMC811 3.86 V |
| **★★ Neumann, Hamann, Danner, Hein, Becker-Steinberger, Wachsman, Latz 2021 (`assb` 54호 — 큐 55 · **2차 묶음 열여섯째 편** · 지목 3 회(02호 ref 38 · 27호 ref 14 · 53호 [27]) · ⚠ **양극 없음 — LLCZNO 고체전해질 자체의 수송**, 모델(DLR BEST) + 재사용 자료(FIB-SEM · 차단 EIS = Hamann 2020, 치밀 펠릿 EIS = Han 2016) · DLR–HIU + UMD · *ACS Appl. Energy Mater.* 4, 4786)** | **해당 없음** — CAM 0(Li · Au 대칭). 다공 SE 의 Li 피복 0–73 % 는 그려 넣은 스냅샷(`[인쇄]` "generated based on a visual interpretation of SEM images") | **없다** — 새 측정 0, XRD 는 2차상을 못 봄("below the detection limit") | ★ **새 층 — "재사용 스펙트럼 위 손 보정, 표 스스로 'calculated'"**: `i₀₀^GB` 6.91e-3 · `C_DL^GB` 9.75e-9 = Han 2016 치밀 펠릿 한 스펙트럼에서 "estimate … refined manually", 교정 시편 구조 = **가정**(GeoDict 다면체 15 ± 6 µm); Table S4 범례 "measured by the authors [°]" **0 개**; `σ⁰` 7.69e-4 = 외부 입력(문헌 범위 2.4–7.69e-4 의 윗끝, 벌크 절편은 대역 밖); `τ` = FIB-SEM 구조 계산(computed-geometric). 02호가 "measured in dense pellets" 로, 53호가 "similar to those measured in dense pellets" 로 옮기며 층위가 올라갔다 | **0/54 — 마흔여섯 번째 성질 "교정 단계에서 합을 입력으로 나누고, 적용 단계에서 같은 합의 비식별을 인쇄했다"**: `[인쇄]` "an exact deconvolution of both contributions via EIS is unfeasible without additional information on the GB composition"(본문 + SI 두 번) · 결론도 "bulk **and/or** GB" 유지 — 그러나 치밀 교정에서는 같은 벌크 ↔ 입계 분할을 입력 `σ⁰` 로 정했다. 온도 1(300 K) · 입도는 공극률과 교락 | 해당 없음 | **없음** — `MPa` 1 = 문헌 Li 음극 400 MPa | 해당 없음(Li 무한 저장소 가정) | 해당 없음 |
| **★★ Hlushkou, Reising, Kaiser, Spannenberger, Schlabach, Kato, Roling, Tallarek 2018 (`assb` 55호 — 큐 56 · **2차 묶음 열일곱째 편** · 01호 ref 16 지목("FIB-SEM 실측 미시구조") · Marburg(Roling · Tallarek) + KIT KNMF + **Toyota** · LCO(LiNbO₃)/비정질 LPSI, 탄소 없음 · 대칭셀 EIS 1 + FIB-SEM 재구성(35.6 nm × 100 nm) + 추적자 확산 모의 · 신품 · *JPS* 396, 363)** | **이동 없음** — 부피분율 **측정**(LCO 33.1 · SE 53.7 · void 13.2 %, ⚠ void 상 = 수지 + 잔류 void) · void 의 **경로 효과 계산**(가상 void → SE 치환: `D_eff/D⁰` 0.574 → 0.786, `τ` 1.74 → 1.27; `[재현]` `ε/τ` ×1.71, 로그 몫 `τ` 59 %). **`θ` · `φ` · `u` 0** — `percolat*` · `connect*` · `surface area` 0, LCO 표면 분할(LCO–SE ↔ LCO–void)을 같은 재구성에서 셀 수 있었으나 안 셌다(`[도표]` Fig. 4D 정성). `θ(N)` 0/55 | 이동 없음(**반 칸 검토 후 접음** — EIS ↔ 구조 모의는 수송 곱의 독립 관측 둘이나 신품 · 다른 시편 · 용량 축 아님) | ★ **층 하나 — "두 시편 · 두 경로의 `τ` 일치, 측정 쪽 `ε` 미인쇄, 영상 상은 수지와 void 를 합침"**: `τ_cond` 1.6 ± 0.1(EIS, `[재현]` 인쇄 `R` · `d` · σ⁰ 로 1.6 을 내려면 ε ≈0.65 — 공칭 0.62 → 1.53 · 영상 0.537 → 1.32) ↔ `τ_diff` 1.74(모의, ± 0); 분할 문턱(밝기 < 65) · 수작업 교정은 **SI 에만**; 부피분율 유한 크기 수렴 미보고 | **0/55 — 마흔일곱 번째 성질 "두 경로의 일치를 서로 다른 `ε` 로 나눈 `τ` 로 보고했다 — 관측 곱으로는 ×1.31 어긋나고, 그 차는 재지 않은 수지 몫에 배정했다"**: `[재현]` `σ_eff/σ⁰` EIS 0.406 ± 0.013 ↔ 모의 void 0.309 · 무공극 0.527; EIS 시편 void 미측정; 시편 차 넷(수지 · 충전 상태 · 압착 · 두께) 중 하나만 배정("most likely") | 해당 없음(Li \| Li 대칭셀) | **없음** — 제조 압력만(SE 276 MPa · 복합 4 t cm⁻² ≈392 MPa · FIB 펠릿 4 t cm⁻² 14 h), 운전 0 | 해당 없음 | 없음(LCO/LPSI 화학, OCP 0) |
| **★★ Bielefeld, Weber, Rueß, Glavas, Janek 2022 (`assb` 56호 — 큐 57 · **2차 묶음 열여덟째 편** · 지목 4 회(02호 ref 36 · 14호 [69] · 50호 ref 35 · 53호 [203]) · JLU Giessen(Janek) + **Volkswagen** · **FEM 모델 편 — 새 측정 0** · NCM811/Li₆PS₅Cl · 01호와 같은 저자 셋 · *JES* 169, 020539)** | **이동 없음 — 층 하나(모델 명제)** "피복률 `φ` 의 3D 모델 스윕: 저율 무감(`[도표]` 0.02 C 피복 손실 48 % 에 ≤ ≈7 mV · 용량 −3 %) · 고율 용량 손실처럼(0.5 C −25 %) · **`φ` 70 % 고정에서 void 크기만으로 과전압 ×2.6–4.5**". void 는 **접촉 자리에만** — 경로 효과 구성상 0(`[인쇄]` "not capable to quantify … ionic percolation"), 검증 모델은 void 14 % 를 SE 로 채움. **`θ` 는 손으로 1**(SI: 01호대로면 42 vol% 는 문턱 아래 → placeholder + "moved manually"). void 부피 스윕 · "pore 문턱" 0(`threshold` 0). `θ(N)` 0/56 | 없음 — 대조는 남의(Rueß 2020) 첫 충전 곡선 3 율, 오차 척도 0 | ★ **층 하나 — "비적합 선언 + 이산 선택(PSD 절단 · 수작업 연결 · 입력 세트) + `j₀` 면적 미정의"**: `[인쇄]` "none of the simulation input has been fitted" ↔ PSD "modified"(11 µm 절단, 실험 일치로 선택) · `j₀` = Rueß `R_CT` 에서 식 (12) `R_CT = RT/(zFAj₀)` — `A` 미정의(`[재현]` 규약 차 ≈×13.6) · `T` 273.15 K 인쇄 | **0/56 — 마흔여덟 번째 성질 "비유일성을 그림으로 보이고(상수 `{D̃₂, j₀,₁}` 가 SOC 의존 세트보다 0.5 C 에서 잘 맞는다 — 본문 'best') '물리적으로 옳다' 로 골랐다 — `j₀` 적합을 'Achilles heel' 로 경고했으나 식별성은 재지 않았다"** | 해당 없음(Li 금속 대극 모델, `j₀ᵃ` 3 A cm⁻²) | 없음(`MPa` 0 · `pressure` 1 추측문) | 해당 없음 | 층 하나 — NCM811 OCV(Fig. S2) = **02호 `U₀` 의 경유지, 원전 Rueß 2020** |
| **★★★ Bielefeld, Weber, Janek 2020 (`assb` 57호 — 큐 58 · **2차 묶음 열아홉째 편** · 지목 3 회(15호 [28] · 24호 ref 41 · 53호 [151b]) · 56호 ref 25 · JLU Giessen(Janek) + **Volkswagen** · **모델 편(GeoDict + EJ-heat 정상 전도) — 새 측정 0** · NCM/황화물 · 01호와 같은 저자 셋 · 01호 AM 배열 재사용 · *ACS AMI* 12, 12821)** | **이동 없음 — 층 하나(모델 명제)** "바인더는 `θ_AM` 을 구성상 안 움직이고(Fig. 5b 세 곡선 겹침) `A_spec,a`(피복 + SE 고립, 17–82 %) · `σ_eff`(70:30 `τ²` 4.2 → 6.4 · 10) · `θ_SE`(ε_AM 68 에서 → ≈55 %)를 한 손잡이로 깎는다; void 5 → 20 % 는 `σ_eff` ×≈2(세 점 · 단조)". **'pore 문턱' 0**(`threshold` 0 — 급변은 AM 분율 축뿐). 01호 `p_c` 는 Fig. 5b AM 이용률 49 → 50 vol% 무릎으로 **말없이 재현**. `θ(N)` 0/57 | 없음 — 대조는 남의 한 점(Kato 2018 `σ_eff` 0.68 ↔ 0.73) · 남의 GITT 면적 비(Nam 2018 *JPS*, 삼각형 4 개) | ★ **층 하나 — "유도된 `τ²`(σ⁰ε/σ_eff 이름표) + 가정 void 15 %(55호 수지 + void 13.2 % 출처 — 55호 D7 두 번째 전파) + 남의 GITT 면적 비('large errors' 자기 경고 · 작은 AM 점은 `p_c` 아래)"** | **0/57 — 마흔아홉 번째 성질 "적합 자유도의 무의미를 인쇄했다(수정 Bruggeman α · γ 'do not offer any further scientific insight') — 그러면서 자기 검증은 모르는 void 를 15 % 로 놓은 한 점 일치(곱 7 %)로 했고, 그 void 가 `σ_eff` 를 ×2 움직인다는 것을 같은 지면이 보인다"** | 해당 없음(음극 0) | 없음(`pressure` 0 · `MPa` 0) | 해당 없음 | 없음 — NCM811 196 mAh g⁻¹ · 4.76 g cm⁻³ 는 C-율 환산용, OCP 0 |
| **★★★ Asheri, Fathidoost, Glavas, Rezaei, Xu 2023 (`assb` 58호 — 큐 59 · **2차 묶음 스무째 · 마지막 편** · 15호 ref [22] "유일한 SSB-ML 인용" · **Volkswagen**(Asheri · Glavas — Glavas 는 56호 공저) + TU Darmstadt · **순수 계산 편(MOOSE 미세 화학-기계 CZM + FE² 두 단계 + 신경망 대리) — 실험 0** · 코드 저장소 `mFathidoost/battery` @ `4683a6f` 실행 없이 조회 · *Comput. Mater. Sci.* 226, 112186)** | **이동 없음 — 층 하나(모델 명제)** "박리 `⟨d⟩`(CZM 손상 면적 평균)는 `a = (S/V)(1−ε_e)(1−⟨d⟩)` 로 들어가지만 미세 입자 유입이 `d` 무관(`[코드]` 12,304 행 `soc_dot = 2\|j\|` ±0.13 %)이라 결합은 **`ε_p`(`LAM_PE`) 자리** — 37호 `A_eff ↔ k` 자리가 아니다; `[재현]` 저율 손실 `∫⟨d⟩dSOC` 8.9 · 3.9 % ↔ 1 C 셀 `[도표]` 8.7 · 3.1 %; `⟨d⟩` 는 한 방전 안 SOC 의 함수(개시 0.73–0.89)". `θ(N)` **0/58** — 한 방전 · 출력 ReLU 로 충전 불가 · 대리 입력에 `d` · `ξ` 없음(이력 없음) | 없음 — 실험 0(23호 SEM 재게재 한 장) | ★ **층 하나 — "simulated-surrogate: 원 모델 출력으로 학습 · 궤적 안 행 무작위 분할 · 셀 수준 손상 기준해 없음(FE² 미실행) · 불확실성 0"** + 코드 대조 어긋남(표 5 R²₁ = bigJ **학습** R² · `r2_score` 인자 역순 · 벤치마크 출력 `identity` · L2 항 없음 · 플럭스 척도 2609.6² — D1–D6) | **0/58 — 쉰 번째 성질 "대리의 충실도(원 모델 대비 R², 같은 궤적 안 행 분할)를 정확도로 인쇄했고 원 모델은 검증하지 않았다 — 그 원 모델에서 박리는 `LAM` 과 같은 손잡이다"** | 해당 없음(반쪽전지 · 음극 미해상) | 없음(`MPa` 0 · 스프링 경계뿐) | 해당 없음 | 없음 — 남의 액체셀 NMC OCP 적합식 입력 |

**1호 단독 1.5 → 2편 ≈2.5 → 3편 ≈3.0 → 4편 ≈5.5 → 5편 ≈6.5 → 6편 ≈7.0 → 7편 ≈7.0 → 8편 ≈7.0 → 9편 ≈7.5 → 10편 ≈8.0 → 11편 누적 ≈8.5 칸이다.** (12·13·14편 ≈8.5 유지 — 12·13호는 종설, 14호는 새 칸 대신 **층 셋**: Q1 "비파괴 대리량" · Q6 "압력 → OCV" · Q8 "OCV 축 열역학 도함수". **15편도 ≈8.5 유지 — 새 칸 0이고, 이 편은 Q1·Q4·Q6 에서 "안 쟀다" 가 아니라 "낱말이 없다" 여서 계보의 바닥을 찍는다.**
**→ 16편 ≈9.5 — 14편 만에 칸이 움직였다**: **Q2 +0.5**(전극 분해 관측이 처음으로 들어왔고, 2E = 3E 합으로 **자기 검증**까지 있다) ·
**Q5 +0.5**(기준극을 실제로 설치한 첫 편이고, 그 기준의 **셀 간 0.11 V 어긋남**을 지면이 인쇄한다).
**Q1·Q4 는 그대로 0** — 그리고 16호의 0 은 "낱말이 없다"(15호)도 "안 쟀다"(1–7호)도 아닌 **"밟고 지나갔다"** 다.)
**→ 17편 ≈10.0 — 두 편 연속으로 칸이 움직였다**: **Q5 +0.5** (16호가 기준극을 *설치*한
편이었다면 **17호는 기준 전위 자체를 재고 그 폭을 논문의 주제로 삼은 첫 편**이다.
`[인쇄]` ±10 mV ~ +0.78 V, `[인쇄]` −0.2 V, `[재현]` 옴 몫 0.2 % → 전용 페이지
[[assb-li-in-reference-potential-window]]).
**Q1·Q4 는 여전히 0** — 17호의 Q4 0 은 **"인쇄로 사양했다"** 다
(`[인쇄]` "beyond the scope of this study", `fit*` 전수 0 회).
**→ 18편 ≈10.5 — 세 편 연속으로 칸이 움직였다**: **Q1 +0.5** — **접촉 면적이 처음으로
"측정된 양"이 됐다** (`[인쇄]` Image-J 로 SE|활물질 접촉 면적, 비 **2.0**, 기하 계산
**2.4** 와 대조). **반 칸인 이유 둘**: 나온 것이 **비 하나**이고 절대 분율·오차가 없으며,
**노화 축의 `θ` 는 여전히 0** 이다 — 그런데 이번에는 **도구와 시편이 둘 다 지면에 있었다.**
**Q4 는 0/18** — 18호의 0 은 **"갈림을 인쇄하고 가르지 않았다"** 다
(`[인쇄]` "the chemical composition at the interface **or** the contact area … changed").
**→ 19편 ≈11.0 — 네 편 연속으로 칸이 움직였다**: **Q5 +0.5** — **기준극의 절대 전위를
가정하지도 재지도 않고 측정 구조로 소거한 첫 편**이다 (4전극의 측정량이 `RE₂ − RE₁` 이라
R-LTO 의 절대값이 상쇄된다; `assum*` **0 회**, "1.55" **0 회** — 18호의 G4 가 생기지 않는다).
**반 칸인 이유 둘**: 그 대신 들어온 **기준극 쌍 재현성 `[인쇄]` ca. ±30 mV 의 근거가
지면에 없고**, Li-In 상대극의 관측된 이동(`[도표]` **42–126 mV**)이 **가역 분극**이라
17호의 **지속 이동**과 같은 양이 아니다.
**Q1·Q4 는 그대로** (Q1 ≈0.5 · **Q4 0/19**) — 19호의 Q4 0 은 **"어휘 없이 귀속을
실험으로 물었고 설계의 절반이 판별력이 없었다"** 다 (단면적 축은 벌크도 계면도 `1/S`
로 스케일해 못 가르고, 결정적인 `d` 축은 **4 점 중 하나가 4.5 배 이상치**다).
⚠ **Q2 +0.5 를 검토했다가 접었다** — 19호에는 **활물질이 없어** `LAM_PE` ↔ 접촉 손실을
가를 대상 자체가 없다. 준 것은 값이 아니라 **대조군의 형태**(계면 하나만 추가)다.
**→ 20편 ≈12.5** (Q2·Q5·Q8 각 +0.5 — 전극별 용량 손실 귀속 · 가정이 축으로 들어가고 깨지는 모습 · TiS₂;
Q1 0/20 · Q4 0/20 "작도다" · Q6 0).
**→ 21편 ≈13.5 — Q2 +0.5 · Q5 +0.5**: **Q2** — 같은 InLi 박을 **어느 면을 분리막에 대느냐만** 바꿔
**OCV 는 같고(0.62 V) 접근 가능 재고는 수 자릿수 다른** 두 전극을 **펄스 전하 + 저주파 임피던스 부류**로
가른 첫 편(**반 칸** — 대상이 음극 Li 재고이고 제조 상태다). **Q5** — P4 통제 실험 · "0.62 V ✓ ≠ 재고 ✓" ·
"0.62 V 를 가정할 수 없다" 의 조건·기구(`LLI`) 인쇄 · 기준극 표류 < 3 mV / 28 일 · **여섯 번째 형태 = 교정 이식**.
**안 움직인 칸**: **Q1 0/21**("접촉을 이름 붙여 SEI 와 한 반원에 합치고 압력 가설로 넘겼다") ·
**Q4 0/21**(열네 번째 성질 = **"값의 정확도를 검사하고 배정의 유일성으로 읽었다"**) ·
**Q6 칸 이동 없음**(보고·통제, 스윕 0) · **Q7·Q8 해당 없음**(무음극 아님 · 양극 없음).
Q3 은 칸 대신 **층** 하나(동일 조건 셀 간 ± n = 3, 단 1 건 오기).
**→ 22편 ≈14.5 — Q1 +0.5 · Q2 +0.5, 그리고 Q1 이 `θ` 축에서 처음 움직였다**: **Q1** — 22호(Strauss 2018, 1호의
ref 13)의 **ex situ XRD 불활성 분율(2 / 27 / 31 %)은 용량에서 역산한 이름표가 아니라 회절 상 분율의 측정**이고
용량은 독립 대조로만 쓰인다(**반 칸** — `1 − θ_AM` 의 합집합 상한 · 신품 한 점 · 집전체 면 표층 가중 · n 미기재;
18호의 반 칸은 **면적 비**, 22호는 **쓰였나의 구조 측정** — 층위가 다르다). **Q2** — 같은 측정이 **pristine 격자(물질 그대로)
↔ 덜 충전된 활성 상** 을 갈라 `θ`·`η` 를 따로 준다(**반 칸** — 신품이라 가를 `LAM_PE` 가 없다).
**안 움직인 칸**: **Q4 0/22**(열다섯 번째 성질 = **"측정이 분할을 대신했고, 원인은 병치됐다"**) · **Q5 칸 이동 없음**
(0.6 V 가정, 일곱 번째 형태 "가정이 대조군 전압창을 정한다") · **Q6 칸 이동 없음**(보고·통제, 스윕 0) · **Q7 해당 없음** ·
**Q8 칸 이동 없음**(NCM622, 구조 SOC 눈금만). Q3 은 층 하나(**방법 오차 예산을 인쇄한 첫 편**).
**→ 23편 ≈15.0 — Q2 +0.5**: 23호(Koerver 2017, "접촉 손실의 실험 원전")는 **두 비-LAM 기구(계면층 ↔ 접촉)에 전용 채널**(XPS ↔ SEM)을
붙인 첫 편이고, **같은 지면(SI)이 양극 호의 `R`·`C` 를 두 셀 × 네 구간으로 인쇄**해 `R` 증가분을 **화학 형**으로 가를 수 있게 한다
(**반 칸** — 가른 것은 저항 변화분이지 용량이 아니고, 가른 것은 우리다; 원전은 채널 분담 + 시간 분할로 **배정**했다).
**안 움직인 칸**: **Q1 칸 이동 없음** — 접촉 손실은 **이름표 + 정성 SEM**, 치수·분율 0; **`θ(N)` 측정량 0/23**, 대리량(`C_SE/Cathode`,
전제부)으로는 N = 1→2 불변이 첫 입력 · **Q4 0/23**(열여섯 번째 성질 = **"채널 분담 + 시간 분할 배정"**) · **Q5 칸 이동 없음**(가정 명시,
여덟 번째 형태 = "깨지는 곳을 '활성화'·'음극 동역학' 으로 덮음") · **Q6 칸 이동 없음**(보고·통제, 스윕 0) · **Q7 해당 없음** ·
**Q8 칸 이동 없음**(NCM811 기존). Q3 은 층 하나(n = 4 인쇄, 산포 0).
**→ 24편 ≈15.0 — 새 칸 0**: 24호(Stavola 2023, 큐 23 — "01 이 '두께 효과는 유한 크기 인공물' 이라 한 자리")는 **01 을 반박하지도 지지하지도 않는다** — 01 의 인공물은
**모델 체적을 자를 때 전자 클러스터 소속이 부푸는 것**이고 01 은 `[인쇄]` "tortuosity, and resulting effective conductivities … not explicitly treated" 로 **이 편이 재는 항을 뺐다**; 이 편은
두께를 **스윕하지 않는다**(110 · 155 µm 는 조성과 교락, 50 µm 한 셀). 리튬화 구배는 **몸통이 `η(z)`** 이고 **`θ` 형 모집단이 섞여 있으며 식 S14 가 둘을 합친다**.
**안 움직인 칸**: **Q1**(정량 0, `θ` 형 관측은 그림에만, `θ(N)` 0/24) · **Q2**(층 — `η(z)` 공간 연산자, 비가역 깊이 균일) · **Q4 0/24**(열일곱 번째 성질 **"비식별을 물리로 읽었다"**;
재료 = D1 `ε` 규약 반전 · 세 `τ²` 병치 · 두 적합 1.35–2700 배) · **Q5**(아홉 번째 형태 "기준을 말하지 않는다") · **Q6**(보고·통제, 제조 압력 교락) · **Q8**(NMC111 첫, OCP 0) · **Q7 해당 없음**.
Q3 은 층 하나(같은 양의 세 추정 병치).
**→ 25편 ≈15.5 — Q6 +0.5**: 25호(Zhou 2025, 큐 24 — "저압 장수명", DEM 브랜치 앵커가 가리키는 편)는 **운전 압력 30 · 10 · 2 MPa × SE 입도 둘의 요인 설계**이고, 압력별 용량·감쇠·전극별 `R` 이
같은 지면에 있어 `[재현]` **초기 압력 손해는 두 미세구조에 공통(−26.5 ↔ −30.7 mAh g⁻¹), 미세구조가 바꾸는 것은 감쇠의 압력 의존뿐**(fine 감쇠 −26/−27/−22 ↔ coarse −33/−38/−64)이라는 분리가 나온다
(**반 칸** — 장치·계측 0 · 이력 미기재 · n = 1 · 셀 간 차 ≈20 % 가 효과와 같은 크기 · 2 MPa EIS 기준점이 그림 겹침 위). 5호 위 벽("Li 금속은 ≥25 MPa 에서 단락")에 **반례 후보**가 붙는다(30 MPa ≈1500–1700 h, 검증 불가).
**안 움직인 칸**: **Q1**(측정 접촉량 0 · DEM `θ` 는 계산 + 겹침 손잡이 94 → 20 % · 30/10 MPa 첫 충전 비 1.03 과 모순 · **`θ(N)` 0/25** · 23호 대리량 적용 불가) · **Q2**(층 — 공통 모드 분리 · 율 극한) ·
**Q4 0/25**(열여덟 번째 성질 **"민감도를 인쇄하고 그 손잡이로 검증을 맞췄다"**) · **Q5**(열 번째 형태 "Li 금속이라 기준을 문제 삼지 않는다 — 자기 적합이 상대극을 가장 큰 항으로 인쇄"; 17호 함정 — 전압 하강 ≈80 % Li 계면) ·
**Q8**(NCM811 기존, OCV 0) · **Q7 해당 없음**. Q3 은 층 둘(★ **그림 자료의 정체가 불확실한 첫 편** — Fig. 3 곡선 겹침 · S15 제목 반전 · 인쇄 유지율 6 중 2 재현; 암묵적 반복 ≈20 %).
**→ 26편 ≈15.5 — 새 칸 0**: 26호(Iwakiri 2024, 큐 25 — "Q4 확인용", 제목에 "sensitivity analysis" 가 든 첫 편)는 **Q4 를 움직이지 않는다 — 0/26.** 그 "민감도 분석" 은 1C 전방 모델의 **OAT 대역 스윕 + 설계 KPI** 이고 식별성 도구(FIM · 조건수 · 프로파일 · CI)는 전수 0 이다. ★ 그런데 **추정과 스윕이 같은 모델 · 같은 지면에 있는 계보 첫 편**이라 비식별 방향 셋이 저자 그림에 있고(Fig. 5a · 12a≡b · 3≡15), 그중 0 열 파라미터 `D_e⁻` 의 적합값이 문헌 대비 **10 자릿수** 표류해 Table 3 에 있다 — **보인 것은 우리의 `[재현]` 이다**(10호 기준: 인쇄된 명제도, 저자의 계산된 판정도 없다 ⇒ 반 칸 검토 후 접음).
**안 움직인 칸**: **전부** — Q1(`contact` 0 회, 모델에 자리 없음 · 0/26) · Q2(실험 0) · **Q4 0/26**(열아홉 번째 성질 **"평탄을 스스로 계산해 놓고, 평탄 위의 점을 값으로 인쇄하고, 그 점에서 본 둔감을 물리로 읽었다"**) · Q5 · Q7 해당 없음(Li 박) · Q6 없음 · Q8(LCO 기존). Q3 은 층 하나(**문헌 대조의 순환** — 대조 대상이 같은 데이터의 출처 논문 값, 7/10 이 정확히 ×1.0500). → 새 개념 [[assb-sensitivity-sweep-vs-identifiability]].
**→ 27편 ≈15.5 — 새 칸 0**: 27호(Sinzig 2024, 큐 26 — "Q4 확인용", 지문 표의 "전역 민감도를 제대로 한다")는 **Q4 를 움직이지 않는다 — 0/27.** 전역 민감도는 **제대로 했다**(Sobol 1·2·전차 + 95 % CI, GP 대리모형, Saltelli 추정기) — 그러나 26호 표로 **첫 줄(설계)의 전역판**이고, 묻는 것은 식별성이 아니라 **모델 적합성**(3D 입자 분해를 참값으로 가정, P2D 가 같은 출력을 내는 영역)이다. 데이터가 없다. ★ 그 안의 **비식별 재료 셋**(전차 지수 0 · 두 모델의 일치 · 보정이 흡수하는 상수)을 저자는 전부 적합성으로 읽었고, ★★★★ `[재현]` **그 상수(큰 `κ` 오프셋 0.068 · 150 점 평균 차 0.072)는 비연결 입자 몫 `1 − u` = 0.07 과 맞는다** — 저자 배정은 "insufficient homogenization strategy", `u` 를 넣는 처방은 `[인쇄]` **용량을 `A_el-c` 로 깎기**, 그 계산을 보일 Fig. 3b 점선은 **그림에 없다**. ⇒ 카드의 물음이 **모델 대 모델로** 재현된다: 물질은 그대로이고 연결만 끊긴 7 % 가 P2D 와 대조되면 **용량 오프셋**이 되고, P2D 에서 그 자리는 **`LAM_PE` 와 같은 손잡이 하나**다. 보인 것은 우리 `[재현]` 이다(26호 구분).
**안 움직인 칸**: **전부** — Q1(계산 `u`, 1호와 같은 층 · `θ(N)` 0/27) · Q2(실험 0) · **Q4 0/27**(스무 번째 성질) · Q5/Q7 해당 없음(Li 금속) · Q6(틀 강성 한 값, 응력은 출력) · Q8(NMC622 기존, OCV 빌림). Q3 은 층 하나(**모델 대 모델 참값 + CI 붙은 민감도**). → 갱신 [[assb-sensitivity-sweep-vs-identifiability]](전역판 · 모델 불일치 민감도 줄 · 적합성 ≠ 식별성) · [[assb-lampe-contact-product-degeneracy]](`A` 의 세 겹 짐) · [[assb-tortuosity-factor-effective-conductivity-split]](`τ` ↔ `τ²` 이름 충돌).
**→ 28편 ≈15.5 — 새 칸 0**: 28호(Bizeray 2019, 큐 27 — "방법론 원전 (액체셀)")는 **계보에서 처음으로 셋째 줄(식별성)에 선 편**이다 — 구조적 식별성(선형화 SPM 전달함수의 유일성)과 실제적 식별성(합성·실험 EIS 의 손실 등고선)을 둘 다 한다. 그러나 **액체셀이고, 식별 집합 `(τ_d⁺, τ_d⁻, R_ct)` 에 용량이 없다** — `Q_th` 는 `[인쇄]` `β = dU/dQ` 로 흡수돼 기준극 입력, `x⁰` 도 가정. ⇒ **ASSB Q4 0/28, 도구 칸만 채운다.** ★ `[해석]` 그 묶음(식 17–19)에 카드 물음을 올리면 **입자 통째 비연결은 LAM 과 같은 파라미터**(`ε` 는 `Q_th` 에만 있다)이고 표면 일부 접촉은 `R0` 로 사라진다 — 카드 전제(가를 정보는 모델 밖 관측)를 **묶음 대수로** 다시 얻는다.
**안 움직인 칸**: **전부** — Q1(액체, `θ(N)` 0/28) · Q2(ASSB 관측 0) · **Q4 ASSB 0/28**(스물한 번째 성질 **"도구는 있고 대상이 없다"**; 식별성을 잰 편은 계보 전체 1/28 — 이 편, 액체셀) · Q5 해당 없음(액체 기준극 = 방법 전제, ×0.78 사후 배율) · Q6 없음 · Q7 해당 없음 · Q8 해당 없음(액체). Q3 은 층 하나(**합성 참값 복원 — 같은 모델 · 무잡음**). → 새 개념 [[spm-grouped-parameter-identifiability]] · 갱신 [[assb-sensitivity-sweep-vs-identifiability]](셋째 줄 원전 · 처방 7) · [[assb-lampe-contact-product-degeneracy]](열한 번째 적용).
**→ 29편 ≈16.0 — Q4 +0.5, ASSB 계보에서 Q4 가 처음 움직였다**: 29호(Yanev 2024, 큐 28 — "`η(i)` 항 그 자체")는 CA 한 번의 율 곡선을 `Q(R) = Q_M/(1+2(Rα)ⁿ)` 로 적합해 **정적 용량(`Q_M`) ↔ 동역학적 결손(`α`·`n`)** 을 가르고, **그 분리가 언제 실패하는지를 저자 자신의 적합 공분산 진단으로 인쇄**한다 — `[인쇄]` sc90 "not enough information in the measured data to accurately fit the Q_M and α parameters, which is reflected by their high dependencies close to unity in Table S2."
근거가 **논문 명제 + 저자가 돌린 진단**이고(26·28호처럼 우리 `[재현]` 이 아니다), 식별 집합에 **용량 스케일이 들어 있다**(28호는 `Q_th` 를 입력으로 뺐다) ⇒ **반 칸**. [[assb-sensitivity-sweep-vs-identifiability]] 의 **둘째 줄(추정 데이터 위 `J` 의 평행 열)에 수치를 붙인 계보 첫 편**이다.
**반 칸인 이유 넷**: 진단 값은 SI Table S2(미열람) · 국소 공분산만(폭 · 프로파일 · CI 0) · 축이 **정적 ↔ 동적**이지 카드의 **`LAM_PE` ↔ 접촉**이 아니다(`Q_M` 이 둘을 합친다) · ★ **저자가 진단을 해석에 전파하지 않는다** — sc90 `Q_M`·`α` 를 무표시로 그리고, 가장 센 이용률 주장("`Q_M` 최대 sc84, LIB 기준 초과")이 `[인쇄]` "plateau … not clearly visible" 인 셀의 **외삽**(`[도표]` ≈236 ↔ 실측 177)이다.
**안 움직인 칸**: **Q1**(`Q_M` · `φ` 14 점씩 — 둘 다 역산, `φ` 는 `D_true` 공통 · LIB 100 % 가정 위 · `θ(N)` 0/29) · **Q2**(반 칸 검토 후 접음 — LIB 기준이 0.1 C 유한 율이라 이용률 >100 % 가 나온다) · **Q5**(열한 번째 형태 "검증 이식" — 17호가 3전극으로 검증한 같은 음극을 2전극으로, 검증 창 ≠ 해석 창) · **Q6**(500 / 50 MPa 고정) · **Q7 해당 없음** · **Q8**(NCM811, 단결정 첫 대조, OCP 0).
Q3 은 층 둘(**fitted-extrapolated** `Q_M` · **derived-by-reference-ratio** `φ`). ★ `[재현]` **이 편의 "확산성 한계" 와 "작은 접촉 면적" 은 같은 숫자의 두 이름이다** — `D_app ∝ 1/A²`(식 3)라 GITT 가 보는 것은 `D·(A_eff/V)²` = 28호 `τ_d` 묶음이고, 저자는 `D_LIB` 수입으로 쪼갰다. → 갱신 [[assb-sensitivity-sweep-vs-identifiability]](둘째 줄 첫 수치) · [[spm-grouped-parameter-identifiability]](GITT = `τ_d` 묶음) · [[assb-lampe-contact-product-degeneracy]](열두 번째 적용 · 처방 첫 줄의 실패 조건).
**→ 30편 ≈16.0 — 새 칸 0**: 30호(Park 2024, 큐 29 — "Q8 보조", 제목이 "비대칭 동역학을 풀었다")는 **비대칭을 측정으로 가르지 않았고, 비대칭의 부호를 자기 그림과 반대로 인쇄했다** — `[재현]` Fig. 3 의 봉우리 전류에서 b 를 다시 구하면 **산화 ≈0.58 · 환원 ≈0.73**, 인쇄는 산화 0.76 · 환원 0.58(초록 · 본문 · 캡션 · 표 네 곳 같은 방향). Table 1 의 "고체" 율 용량(90/54/28)도 고체셀 그림(Fig. 2a ≈61/40/10.5)이 아니라 **"액체" 행(61/40/11)과 일치**한다.
**안 움직인 칸**: **전부** — Q1(`contact` 정성 6 회, 복합양극이 아니라 `θ` 의 자리 자체가 없다 · `θ(N)` 0/30) · Q2(손실을 가를 관측 0, dQ/dV 는 손실 전 1–10 회만) · **Q4 0 — 스물두 번째 성질 "라벨이 자기 그림을 거스른다"**(ASSB 누적은 29호의 0.5 그대로; 29호 뒤 두 번째 식별성 명제 **없음**) · **Q5 열두 번째 형태 "방향 비대칭의 일방 배정"**(Li 금속을 "reference" 로 부르고 방향 의존 관측을 양극 쪽에 배정, 가를 대칭셀은 전도도로 소진; `[재현]` 대칭셀 직렬 몫 ≈0.5–0.86 kΩ ↔ CV 분극 ≈0.54–0.65 kΩ) · Q6(미보고) · Q7 해당 없음 · Q8(NMC111 두 번째, OCP 0).
Q3 은 층 둘(**label-contradicts-own-figure** · **textbook-equation-with-unprinted-inputs**). ★ 카드에 주는 것은 칸이 아니라 **경계 둘**: ① 율 스윕 처방의 **두 번째 실패 조건** — `[재현]` 29호 식을 Fig. 2a 에 걸면 `Q_M` ≈63 이 식별되지만(평탄이 창 안), 그 값은 0.1 C 블록에서만 −26 % 표류한 **뒤의** 용량이다 — **정적 용량이 스윕 중 움직이면 외삽값은 정적이 아니다** ② **외부 액체 기준은 배정 방향을 정하지 않는다** — Randles–Ševčík `D_app ∝ 1/(A·C)²` 이라 액체 대비 10.9 배는 유효 면적 ≈3.3 배로도 되는데 저자는 전부 `D` 에 배정했다(29호는 같은 구조를 면적에 배정). → 갱신 [[assb-lampe-contact-product-degeneracy]](열세 번째 적용 · 첫 줄 두 번째 실패 조건 · 액체 기준 줄 반대 배정) · [[spm-grouped-parameter-identifiability]](Randles–Ševčík = `A·C·√D` 묶음) · [[assb-sensitivity-sweep-vs-identifiability]](어느 줄에도 없는 편).
**→ 31편 ≈16.0 — 새 칸 0**: 31호(Chien et al. 2023, 큐 30 — "이 곡선이 얼마나 평형인가", 29·30호가 함께 지목한 "곱 `D·(A/V)²` 을 가를 후보")는 **곱을 가르지 않는다** — ICI 는 GITT 와 같은 식(식 19, `A` 가 제곱으로 든 입력)을 1–5 s 차단창에서 쓴다. `A` = BET 1.5 m² g⁻¹ 상수 → 전부 `D` 에 배정 = **같은 곱의 세 번째 배정**(29호 면적 · 30호 `D` · 31호 상수). 다른 점은 **첫 "고지된 배정"** 이라는 것: `[인쇄]` "The BET-surface area may differ from the electrochemically active surface area. However, … both of which are equally affected by this factor." — 비교 주장(ICI ≈ GITT)을 `A` 가 약분되는 비로 봉인했고, **사이클 추적 · operando 의 절대 주장에서는 그 봉인을 뗐다**. ⚠ **액체셀**(1 M LiPF₆, 본문·SI 모두 고체셀 0) ⇒ 28호처럼 **도구 칸**.
**안 움직인 칸**: **전부** — Q1(`contact` 0 · Fig. 7 `D`(N)·`R`(N) 은 측정된 추적이나 `A` 고정 · 가로축 `Q` · `θ(N)` 0/31) · Q2(`R_ICI` = EIS `R0+R1+R2` 합 — 성분 분리 아님, `C` 없음) · **Q4 ASSB 0 — 스물세 번째 성질 "공통 인자로 비교를 봉인하고, 절대 주장에서 봉인을 뗐다"**(누적 0.5 = 29호 그대로) · Q5 해당 없음(액체 Li 링 기준극 — 30호 함정을 **설계로 뺀** 대조 표본) · Q6 없음 · Q7 해당 없음 · Q8 해당 없음(액체, OCP **기울기** 곡선만).
Q3 은 층 둘(**measured-bundle-with-declared-constant** · **regression-SD-only error bars** — `D` 오차 = `k` 회귀 SD 뿐, 방법 간 SD 0.56 의 1/2–1/5). ★ 카드에 주는 것은 **구조 둘**(둘 다 `[해석]`, 식 19 대수): ① **GITT/ICI `D_app` 은 입자 통째 비연결에 불변(`u` 약분) · 표면 피복에 제곱 감응(`φ²D`)** — 카드의 두 접촉 손실이 **다른 축**(용량 ↔ `D_app`)으로 간다 ② **ICI 의 `R/k` 는 면적이 약분되는 조합**(`∝ √D/j₀`) — 곱 축퇴 처방의 시간 영역 후보, 이 편은 사이클 추적에 `k` 를 인쇄하지 않아 지면에서는 계산 불가(zenodo 원자료에 있음). 그리고 `[재현]` 두 경계: 신품 4.18 V `D` 골은 `k` 가 아니라 **OCP 기울기**(×0.36)가 만들고, operando `D` 급락은 저자가 상속한 "single-phase solid solution" 가정이 **자기 XRD(두 상)로 깨진 구간**이다. → 갱신 [[assb-lampe-contact-product-degeneracy]](열네 번째 적용 · `R/k` 새 줄 후보 · 세 번째 배정) · [[spm-grouped-parameter-identifiability]](ICI 묶음 · `u` 불변 · `φ²`) · [[assb-sensitivity-sweep-vs-identifiability]](방법 간 일치 ≠ 인자 식별).
**→ 32편 ≈16.0 — 새 칸 0**: 32호(Biçer et al. 2025, 큐 31 — "08 의 '접촉 손실 ↔ 보통 노화 분리 진단' 요구가 매단 유일한 인용")는 **종설이고 1차 측정 0** 이라 칸을 움직일 수 없다 — 그리고 **8호가 매단 요구 자체가 이 편에 없다**(`[인쇄]` 압력 센서 권고는 있다 · 압력 의존 임피던스는 절반 · "contact loss ↔ ordinary aging 진단" 은 0; `contact loss` 0 회). 이 편의 체계에서 접촉 불량은 **임피던스 · 박리 · 고장**으로만 가고 용량 몫이 없다 — 분류 체계 **네 번째 표본 "접촉 = 임피던스"**.
**안 움직인 칸**: **전부** — Q1(`contact loss` 0 · `θ(N)` 0/32) · Q2(BMS 권고 채널은 유지·추적용, 분리용 0) · **Q4 ASSB 0 — 스물네 번째 성질 "선형 OCV 전제가 물음을 지운다"**(`[인쇄]` "well-established linear relationship between SoC and OCV" ↔ 두 쪽 뒤 "nonlinear" — 자기 모순; 누적 0.5 = 29호 그대로) · Q5 · Q7 해당 없음 · Q6(`pressure` 14 · `MPa` 0, 제조 ↔ 운전 압력 미구분) · Q8(Table 1 공칭 전압뿐). 축 (b) 온도: **0**(`Arrhenius` 0 · 열관리 = 열폭주 안전). Q3 은 층 하나(**정의 없는 SoH + 정격 분모 SoC** — `[인쇄]` SoC = "instantaneous capacity to its rated capacity"). ★ 카드에 주는 것은 칸이 아니라 **계보 정정 하나**(요구 명제의 첫 인쇄 = 8호)와 **BMS 어휘 경고 셋**(SEI = interface 재정의 · balancing 이름 충돌 · bipolar 스택의 셀별 관측 가능성). → 갱신 [[assb-lampe-contact-product-degeneracy]](열다섯 번째 적용 — 대상 없음).
**→ 33편 ≈16.0 — 새 칸 0**: 33호(Zhang et al. 2025, 큐 32 — "Q6 주축, 24 번과 짝", 원장 기대 "32호 종설에 없는 압력 수치 공급, `MPa` 50")는 **종설이고 1차 측정 0** 이라 칸을 움직일 수 없다 — 그리고 **가진 압력 수치 50 개 중 "압력의 함수" 가 0 개**다. 압력 ↔ `θ` ↔ 감쇠의 정량 관계를 1차 원전으로 댄 문장이 없고, **Sakka 2022(`θ(P)` 측정 후보)는 [120] 으로 인용되지만 "3D 접촉 · 압력 방향" 명제에 붙어 수치 0** · **Xu 2024 는 [11] 로 인용되지만 "<≈1 MPa" 는 없다**(이 편의 값은 출처 없는 2 MPa). 8호 귀속("pressure reduction = central commercialization problem")은 **선다** — 32호와 반대 결과. 25호와는 **양방향 인용 모두 시점상 불가**(33호 온라인 2024-12-26 ↔ 25호 접수 2024-11-24), 25호 "≤5 MPa" 는 이 편에서 오지 않았다.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/33 · 유일한 양극 접촉 손실 문단이 23호 배정을 뒤집음) · Q2(관측 0) · **Q4 ASSB 0 — 스물다섯 번째 성질 "용량은 전략의 성적표"**(누적 0.5 = 29호 그대로) · Q5 · Q7 해당 없음 · Q6(층 둘: 제조 ↔ 운전 명시 분리 · "저압 = 고압 제조 · 저압 운전" `[재현]`) · Q8(부피 곡선 입력 하나). Q3 은 층 하나(**재수록 그림의 출처가 캡션과 본문에서 갈린다**, 8 장 중 3 장). ★ 카드에 주는 것은 칸이 아니라 **분류 체계 다섯 번째 표본**("접촉 손실 = 압력으로 되돌릴 수 있는 활성 감소" — 카드의 틀에 가장 가까운 종합 층 표현인데 **근거가 없다**)과 **역학 판 상대극 경고**(`[해석]` 재수록 합금·Si 음극 압력 진동 0.7–2.3 MPa/사이클 ≈ 산업 운전 압력, 양극만은 ≈0.05–0.07 MPa). → 갱신 [[assb-lampe-contact-product-degeneracy]](열여섯 번째 적용 — 대상 없음) · [[assb-stack-pressure-operating-window]](요구치 다섯 번째 · 압력 진동).
**→ 34편 ≈16.0 — 새 칸 0**: 34호(Liang et al. 2026, 큐 33 — "Q4 설계 축 — 우리 폭 측정기의 역방향", 원장이 이미 "1 차 측정이 없는 전망 논평" 으로 정정)는 **Comment 이고 데이터 0 · ASSB 0** 이라 칸을 움직일 수 없다. 지시의 핵심 물음 — **펄스가 곱 축퇴 처방의 어느 단계를 온보드로 실현한다고 쓰는가** — 의 답은 **"어느 단계도 아니다"**: `[인쇄]` 세 대역(옴 > 10³ Hz · 계면 분극 10⁰–10³ Hz · 확산 개시 < 10⁻¹ Hz)을 **이름으로만** 두고 `capacitan*` · `time constant` · `relaxation` **전부 0**, 등가 EIS 는 신경망 **재구성**이다 — 31호 `R_ICI`(합이지만 값이 있다)보다 한 층 아래. `[해석]` 우리 대수로는 한 펄스의 이완이 **1단계(τ 형) · 4단계(`C = τ/R`) · 31호 `R/k`** 를 모두 품는다 — ABMS 는 처방의 **자연 하드웨어**인데, 이 편이 권하는 두 설계(재구성 · 온도 불변 학습)는 각각 1단계의 적합 `C` 와 3-a 의 `Ea` 채널을 **지우는 방향**이다.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/34) · Q2(관측 0, ref 29 복원 조작은 후보) · **Q4 ASSB 0 — 스물여섯 번째 성질 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다"**(FIM · CRLB · D-optimality · PE 처방, 계산 0, 구조적 ↔ 실제적 비식별 구분 0; 누적 0.5 = 29호 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 없음. Q3 은 층 하나(**learned-reconstruction features**, 제안형). ★ 카드에 주는 것은 칸이 아니라 **지문 정정 하나**(큐 지문 `identifiab` 0 → **3**, `confidence interval` 0 → **1** — 합자 `ﬁ` 가 정규화 전 텍스트를 가렸다; 같은 검사로 **35 번 `confidence interval` 0 → 6**)와 **구조 하나**(`[해석]` D-optimality 는 모든 입력에서 FIM 이 특이한 곱 축퇴를 못 푼다 — OED 는 실제적 비식별만 줄이고 구조적 비식별은 모델 구조 + 대역이 가른다). → 갱신 [[assb-lampe-contact-product-degeneracy]](열일곱 번째 적용 — 한 펄스 이완 = 처방 공통 입력) · [[assb-sensitivity-sweep-vs-identifiability]](입력 설계 줄).
**→ 35편 ≈16.0 — 새 칸 0**: 35호(Roman et al. 2021, 큐 34 — "Q3 — 08 Table 2 여덟 행 중 유일하게 신뢰구간을 보고")는 **용량(Ah) 스칼라 하나**를 추정하는 ML 방법 논문이고(모드 분할 0 — 우리 물음과 차원이 1 ↔ ≥3), 데이터는 전부 **실측 공개 액체 셀**이라 역범죄는 없다. 지시의 물음 넷 — (a) 스칼라 · (b) 특징은 충전 상단 0.3 V 창의 범함수라 `[해석]` α·β 의 함수지만 LLI ↔ LAM 특징 공간 축퇴는 다루지 않음 · (c) 불확실성은 **예측 오차 보정**(isotonic + 적중률)이지 식별성이 아님 · (d) 실측, 역범죄 없음, 대신 **데이터셋 표지(`Nominal Capacity` · `Charge Current`)와 과거 측정 라벨의 합(`Lagged Cumulated Discharge Capacity`)이 선택된 입력**. ★★ 카드에 주는 것은 칸이 아니라 **8호 원장 정정 둘** — ① 8호 `[재현]` "보정된 불확실성 **0/8**" → 원전은 보정 전용 셀 + isotonic 재보정 + 90 % 적중률 표를 인쇄하므로 **1/8** · ② 8호 "RMSE 0.45 % (best)" → 0.45 % 는 **dNNe 의 RMSPE**, 같은 표 최저는 RF 0.14 %(초록 문장부터 어긋남) — 와 **구조 하나**(`[해석]` 목표 주도 특징 선택은 분리 채널을 버린다: 유일한 저항 채널이 세 그룹 모두 탈락).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/35) · Q2(관측 0, 저항 채널 탈락) · **Q4 ASSB 0 — 스물일곱 번째 성질 "불확실성을 보정했다 — 분해가 없는 스칼라 위에서"**(누적 0.5 = 29호 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 이동 없음. Q3 은 층 하나(**measured scalar label + held-out-recalibrated predictive interval**). → 갱신 [[assb-lampe-contact-product-degeneracy]](열여덟 번째 적용 — 적용 불가 · 선택 경로 경고) · [[assb-sensitivity-sweep-vs-identifiability]](예측 보정 ≠ 식별성 줄).
**→ 36편 ≈16.0 — 새 칸 0**: 36호(Thelen et al. 2024, 큐 35 — "Q3·Q4 불확실성 보정", 큐 지문이 "다섯의 머리" 로 꼽은 편)는 **확률적 ML 종설**이고 1차 측정 0 · ASSB 0 이라 칸을 움직일 수 없다. 지시의 물음 넷 — (a) **aleatory/epistemic 은 가르고(epistemic 을 model-form · parameter 로) 식별성은 없다**; 사후 폭은 **예측 분포 또는 ML 가중치**의 폭이라 우리 근최적 폭과 다른 대상이다(35호와 같은 층) · (b) **확률적 모드 진단 1차 원전 0 편** — 모드 진단 절(p. 20)과 물리 기반 절(pp. 21–22)이 드는 13 편 어디에도 불확실성 서술이 없고(`[재현]` 두 절 안 `uncertain` · `posterior` · `interval` · `Bayes` 0), 자기 문제 그림 Fig. 4 도 Problem 4 만 점으로 그렸다; 사후 상관에 가장 가까운 문장은 Ruan 2022 의 "모드가 본래 상관돼 있어 정확도를 올린다" — **학습 사전의 상관**이지 사후 상관이 아니다 · (c) **CI ↔ PI ↔ TI 를 정의로 가른다**(35호의 `μ ± 2σ` = PI) · (d) ASSB 0 → 도구 칸. ⇒ **Q4 · 원장 구조적 공백 1번의 공급처가 아니다.** ★ 카드에 주는 것은 칸이 아니라 **분류의 빈칸 하나**(`[해석]` 구조적 비식별은 aleatory 도 epistemic 도 아니다 — 데이터량 불변)와 **분류 체계 여섯 번째 표본**(Fig. 3 재작도가 접촉 손실의 모드 연결을 지웠다), 그리고 **큐 지문 정정**(`uncertaint` 205 · `Bayes` 53 · `posterior` 28 · `calibrat` 8 은 공백 소실로 붙은 낱말까지 센 부분문자열 수 — 규칙값 180 · 35 · 26 · 7).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/36) · Q2(관측 0) · **Q4 ASSB 0 — 스물여덟 번째 성질**(누적 0.5 = 29호 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 이동 없음. Q3 은 층 하나(**interval taxonomy printed — predictive only, diagnostics drawn as point**). → 갱신 [[assb-lampe-contact-product-degeneracy]](열아홉 번째 적용 — 대상 없음 · 확률 도구 경고 둘) · [[assb-sensitivity-sweep-vs-identifiability]](불확실성 분류 ≠ 식별성 줄).
**→ 37편 ≈16.0 — 새 칸 0**: 37호(Li et al. 2024, 큐 36 — "9호가 모델 · PSO · `A_eff` 를 위임한 원전")는 **복합양극 ASSB 연속체 모델의 원형**이고, 카드의 물음을 식 수준에서 가른다 — **표면 피복형 접촉 손실(`A^p_eff`)은 `LAM_PE` 와 다른 손잡이다**(용량 · 확산에 없다, 식 8 · 15 · 18) **그러나 반응 속도 상수 `k_p` 와 정확한 곱**이라 "접촉 ↔ 계면 화학" 의 항등이 되고(18호의 "or" 가 식이 된다), **입자 통째 비연결은 `ε_p`(= `LAM_PE`) 말고 자리가 없다**(27 · 28호 경고의 원형). 그리고 그 `A_eff` 값은 **출처 각주가 없고 조성이 다른 9호 셀과 네 자리 같다** — 측정도 셀별 적합도 아닌 상속 상수다. 식별성 명제 0 · 노화 0 · 칸을 움직일 근거 0.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/37 · `A_eff` 상속) · Q2(추출용 관측뿐) · **Q4 ASSB 0 — 스물아홉 번째 성질**(누적 0.5 = 29호 그대로) · Q5(열세 번째 형태 "차감 흡수") · Q6(50 MPa 한 값) · Q7 해당 없음 · Q8(기존 화학). Q3 은 층 하나(**footnote-typed table — the contact knob is the unmarked row**). ★ `[추론]` **이 모델로 ASSB 합성 truth 를 만들면 두 갈래 동어반복**: `A_eff(N)` 이면 OCV 에 안 보이고 `k_p(N)` 와 같다(그리고 `c_dl` 이 면적과 무관해 `R·C` 처방이 truth 에서 거짓) · `ε_p(N)` 이면 정의상 `LAM_PE`. → 갱신 [[assb-lampe-contact-product-degeneracy]](스무 번째 적용 — 원천 모델에 처방을 건다, `A_eff ↔ k` 항등 · 율별 재적합이 율 스윕을 먹는다) · [[assb-sensitivity-sweep-vs-identifiability]](설계 스윕이 항등 쌍의 한쪽만 흔든다) · [[spm-grouped-parameter-identifiability]](틀린 `R_s` 를 `D_p` · `k_p` 가 흡수).
**→ 38편 ≈16.5 — Q2 +0.5 (큐의 마지막 편)**: 38호(Conforto et al. 2021, 큐 37 — "Q1 을 깰 1 순위", 9호가 "정량한 몇 안 되는 문헌" 으로 지목하고 기각한 편)는 **사이클마다 무언가를 잰 첫 ASSB 편**이다 — 방전 전후 **이완 OCP 두 점**으로 활성 질량 `m_act(N)` 을, **저주파 EIS 꼬리**(EIS-PSD)로 확산 경로 분포 `L_diff(N)` 을 40 사이클 × 4 조건(PC/SC × low-V/high-V) 잰다. 그런데 **`m_act` 는 `θ·ε_p` 합이다** — `[인쇄]` "disconnected … cannot contribute to the OCP any longer and can be considered inactive" 는 비연결과 진짜 LAM 을 **정의상 같은 칸**에 넣는 문장이고, 그 칸 전체를 "We suggest" 로 접촉 손실에 배정한다(대안 상전이는 액체셀 TEM 인용 한 편으로 "low"). `[해석]` 평탄 상대극 + Li 과잉(`[재현]` ×2.75)이라 `m_act` 는 **우리 α 적합의 `α_PE` 를 두 점으로 읽은 것**이다 — 우리 degeneracy 가 설계상 지워져 α 가 식별되지만, 카드의 물음은 그 α **안**(`ε_p·θ`)에 있다. ⇒ **Q1 0**(용량 역산 · 합 · 배정 = 22호 반 칸 기준 미달, `θ(N)` 0/38). **Q2 반 칸**: 두 채널이 "OCP-비활성 질량" 과 "경로 연장" 을 가른다 — 22호 신품 `θ ↔ η` 분할의 **노화 · 사이클 해상판**(반 칸 — 카드 핵심 분할 0 · 채널이 `C_diff` 입력으로 묶임 · `[재현]` 이완 1 h 가 PC 후반 `τ` 의 1/13–1/17 · n = 1). ★ **9호의 기각이 그림으로 선다**: 본문 "good agreement for all the samples" ↔ `[도표]` Fig. 9 (a) +12…+27 · (d) −14…−28 mAh g⁻¹.
**안 움직인 칸**: Q1(`θ(N)` 0/38 · 첫 합 계열 1/38) · **Q4 0/38 — 서른 번째 성질 "식별 한계를 식으로 인쇄하고, 결론의 수를 그 한계 밖에 두었다"**(누적 0.5 = 29호 그대로; 식별 집합에 용량 스케일 없음) · Q5(열네 번째 형태 "고정 전위가 게이지의 영점이다") · Q6(≈70 MPa 한 값) · Q7 해당 없음 · Q8(기존 화학, `∂E/∂x` 한 점 차용). Q3 은 층 하나(**closure plot without residuals — two panels miss by 15–30 %**). → 갱신 [[assb-lampe-contact-product-degeneracy]](스물한 번째 적용 — 이완 OCP 두 점 줄 · 반무한 꼬리 곱 경고) · [[spm-grouped-parameter-identifiability]](38호 두 행) · [[assb-li-in-reference-potential-window]](고정 전위 = 게이지 영점).
**→ 39편 ≈17.5 — Q1 +0.5 · Q6 +0.5 (2차 묶음 첫 편)**: 39호(Sakka et al. 2022, 큐 40 — 원장 최상위 "`θ(P)` 측정 후보")는 **접촉 면적 분율을 X선 CT 로 직접 잰 첫 편**이다 — 그러나 잰 것은 **CAM 표면 중 SE 와 닿은 몫 `φ`**(표면 피복)이고, 카드의 `θ`(연결 분율)도 37호의 `u`(통째 비연결 — `ε_p` = `LAM_PE` 와 같은 칸)도 아니다. 37호 두 손잡이 중 **`k_p` 와 헷갈리는 쪽(`A_eff`)** 을 쟀다. **Q1 반 칸**: 절대 분율 · 3D · 압력 5 점(`[도표]` 0.78 / 0.75 / 0.78 / 0.84 / 0.83) — 18호(면적 **비**)·22호(XRD 상한)와 다른 층. 반 칸인 이유: 신품이라 **`θ(N)` 0/39** · 압력 = **제조 압력**(`[인쇄]` "no pressure was added during fabrication") · 분할 문턱 미인쇄 · `[재현]` **같은 분할이 고정 혼합물의 NCM/LGPS 부피비를 ×2 흔든다** · 해상도 0.5 µm 판정. **Q6 반 칸**: 같은 장치에서 CT 와 EIS 를 동시에 — 33호가 "압력의 함수 0" 이라 적은 자리의 첫 1차 원전(반 칸 — 단조 가압만 · n = 1 · S3 교락 · 2전극). ★★★★ **같은 지면이 곱 축퇴를 데이터로 드러낸다**: `[도표]` `R_ct` ×14 ↔ `φ` ×1.10 ⇒ `[재현]` `R_ct·φ` **×13** — CT 척도 면적은 `R_ct` 로그 변화의 ≈4 % 만 설명한다(곱 축퇴 처방 스물두 번째 적용). ★★★ **25호 ↔ 33호 인용은 둘 다 선다** — 25호 = 본문 결과(Fig. 3c · 6b), 33호 = 결론 제언("3D manner … even at low pressures", 원문 "it is expected"). ⚠ **"모델상 25 MPa 면 안정" 은 Sakka 에 없다** — Zhou 원문에서 ref 12 다음 **무인용 문장**이고, 우리 25호 digest 가 그것을 Sakka 에 붙였다.
**안 움직인 칸**: Q2(반 칸 검토 후 접음 — 신품) · **Q4 0/39 — 서른한 번째 성질 "곱의 한 인자를 직접 재고, 나머지 인자가 변화의 96 %(로그)를 가져가는 것을 같은 지면에 둔 채 '대응한다' 로 읽었다"**(누적 0.5 = 29호 그대로) · Q5(열다섯 번째 형태 "상대극 계면을 양극 접촉 면적에 흡수한다") · Q7 해당 없음 · Q8(OCP 0). Q3 은 층 하나(**measured-imaging, threshold unreported, phase ratio not conserved**). → 갱신 [[assb-lampe-contact-product-degeneracy]](스물두 번째 적용 · 표 새 줄 "영상 면적 → `R·φ` 검사") · [[assb-stack-pressure-operating-window]](39호 절 — 제조 압력 5 점 · 요구치 원전 지목 Wang 2021 *Joule*) · [[assb-pressure-reapplication-separation-test]](S14 되돌림 · 비직교 실측).
**→ 40편 ≈17.5 — 새 칸 0 (2차 묶음 둘째 편)**: 40호(Ikezawa et al. 2020, 큐 41 — 지목 5 회, 원장이 "두 Q5 가지가 만나는 자리" 로 올린 R-LTO 원전)는 **R-LTO 전위의 안정성 · 누설 · 드리프트를 재지 않았다.** 1.55 V 는 `[인쇄]` "reported redox potential … [11]"(Costard 2017, **액체셀**)에서 수입되고, 검증은 "these potentials can be calculated to be 3.90 and −0.60 V vs. Li|Li⁺, which are coincident with reported values [5,17]" — **가정한 기준으로 환산한 두 평탄을 문헌 두 값에 맞춘 것**이다(18호 digest 가 원전 없이 적은 P6 "인용 + 순환" 이 원전에서 확인). `leak` 0 · `drift` 0 · `30 mV` 0 — **원장 구조적 공백 3 은 그대로**이고, **19호 ±30 mV 의 근거 사슬은 원전에서 비어 끝난다.** `[재현]` 암묵적 표류 상한은 있다: Fig. 1d 의 (R-LTO − Li-In) 충·방전 중점이 0.1–1 C 에서 −0.9545 … −0.9515 V(≈3 mV) — 단 두 전극의 **차**라 공통 모드이고 순서 · 시간 미인쇄. **두 가지는 여기서 만난다**: 인용([5] Nam 2018 · [6] = **20호 Chang**) · 기각("lithium metal and Li-In alloy seem not suitable", 기계 강도) · 한 셀(Li-In 상대극의 문헌값이 R-LTO 의 증인) ⇒ **Q5 열여섯 번째 형태 "상호 증언"** — 한 가지의 가정값이 다른 가지의 검증 증인이 되고, 그 기준이 뒤(18호)에서 다시 Li-In ≈0.6 V 를 보고한다. `[재현]` 증인을 0.62 V 로 두면 R-LTO = **1.5745 V**(16호가 인용한 Zhang 1.57 V) — **이 검증은 1.55 와 1.57 을 가르지 못한다.** **Q5 반 칸 검토 후 접음**(새 측정 층이 아니라 예견된 순환의 원전 확인).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/40) · Q2(반 칸 검토 후 접음 — 신품 · 합 항등; 기여는 "2전극 양극 호의 ≈절반이 상대극" `[도표]` R2 ×2.7 · R3 ×1.67) · **Q4 0/40 — 서른두 번째 성질 "통과가 보장된 검사로 분리를 검증했다"**(누적 0.5 = 29호 그대로) · Q5(열여섯 번째 형태) · Q6(210 MPa 한 값) · Q7 해당 없음 · Q8(LCO, 환산 전위 5 점). Q3 은 층 하나(**literature-witness offset + sum-identity validation**; ★ 같은 상태 R3 세 값 ×1.49). ★ **다른 편이 이 원전에 대해 한 말 셋이 고쳐진다**: 21호 `[인쇄]` "report a delithiation overpotential … ∼40 mV … ∼110 Ω cm²" — 원전은 그 수를 인쇄하지 않았고 `[도표]` 40 mV 는 C/2 **충–방 폭**(42.8), 탈리튬만 21–23 mV ⇒ `[재현]` **≈58–63 Ω cm²**(분리막 몫 ≈26–27 포함) · 20호 digest "두 가지의 뿌리가 둘" → R-LTO 원전이 In 가지의 두 뿌리를 인용 · 17호 요약 "1 C 이상 Li-In 병목" → 원문 "relatively large overpotential at the end of the discharges"(용량 끝은 LCO 붕괴). → 갱신 [[assb-li-in-reference-potential-window]](40호 절 · 열여섯 번째 형태 · P6 원전 판정) · [[assb-lampe-contact-product-degeneracy]](스물세 번째 적용 · 새 줄 "3전극 옴 몫은 기준극 위치가 정한다").
**→ 41편 ≈18.0 — Q5 +0.5 (2차 묶음 셋째 편)**: 41호(Nam et al. 2018, 큐 42 — 원장 "In-rich depletion layer 원전", 지목 4 회)는 **In 가지에서 가장 이른 편**이고, 본문의 0.62 V 는 `[인쇄]` ref 33(**Jung 2008 *AFM*** — Santhosha 2019 이전의 수입 경로)에서 온다. 그러나 **SI Fig. S2 가 같은 설계의 셀을 기준극 재료만 바꿔(Li₀.₅In ↔ Li 금속) 잰다** — `[인쇄]` "calibration … by adding 0.62 V shows a marginal difference, compared with the case when using the Li metal RE". `[도표]` 인셋 화소 판독: Li 금속 대비 Li₀.₅In CE 중점 ≈**0.621 V**(반폭 ≈6 mV) · 두 기준극 셀 차 ≈**2 mV**. ⇒ **P8(기준극 재료를 바꿔 불변을 본다)의 재료 축 · 전위 판을 2018 원전이 이미 했다** — 계보가 "아무도 안 했다" 고 적어 온 검사다. **근거가 논문의 측정 + 인쇄된 판정**이므로 반 칸: **Q5 열일곱 번째 형태 "기준극 교체 대조"**. **반 칸인 이유**: 셀 간(한 셀 안 교체 아님) · 전류 중 · 전류밀도 미인쇄 · n = 1 · 시간 축 0 · **수를 인쇄하지 않아 인용 사슬에 안 들어갔다**(40호는 이 편에서 "0.62" 인용값만 가져가 "−0.60" 으로 옮겼다). 40호 "상호 증언" 의 In 쪽 끝은 **순환 밖 측정 고리 하나를 SI 에 갖고 있다** — 단 SE 가 Li₆PS₅Cl(40호 LGPS 는 Li 불안정으로 같은 대조 불가). **고갈층**: `[인쇄]` TOF-SIMS Li⁺ 단면 지도로 "Li-depleted layer … estimated to be 50 µm" — `[도표]` 반값 깊이 ≈49 µm ✓, **대조군(방전 전) 0 · Li 정량 0 · 시편 1 개**, `In-rich` 0 회 · "insulating" 은 결론 한 번(전도도 측정 0) ⇒ 21호 인용 "탈리튬 후 계면 Li 고갈을 실험으로 봤다" 는 **선다(정성)**, 단 CE 가 **분말**이라 21호의 **조립 방향**은 이 편이 시험하지 않았다.
**안 움직인 칸**: Q1(`θ(N)` 0/41 · SEM 정성 부정 한 줄) · Q2(반 칸 검토 후 접음 — 전극별 용량 귀속은 20 · 17호와 같은 층) · **Q4 0/41 — 서른세 번째 성질 "전극 분해를 '진단' 으로 인쇄했다 — 분해가 분리막 옴을 어느 전극 채널에 싣는지 묻지 않고"**(누적 0.5 = 29호 그대로) · Q6(제조 370 · 운전 74 MPa 명시 구분, 스윕 0) · Q7 해당 없음 · Q8(NCM622, 첫 사이클 79.1 %). Q3 은 층 하나(**cutoff-identity terminal value** — Fig. 3c CE 종단 전위 = WE 종단 + 0.62 V). ★ **다른 편이 이 원전에 대해 한 말**: 17호 "Li-depleted **In-rich** layers with **low Li conductivity**" → 두 낱말은 17호의 것 · 20호 "배면형은 옴을 측정 창 밖에 둔다" → **WE 채널에서만 참, 분리막 옴 전부가 CE 채널로 간다** · 40호 "1C 이상 Li-In 과전압 선례 [5]" → 이 편은 mA cm⁻² 이고 값은 컷오프 항등식 · 20호 digest "0.62 V 출생지 = Santhosha 2019" → **Santhosha 경로의 출생지**로 좁힌다. → 갱신 [[assb-li-in-reference-potential-window]](41호 절 · 열일곱 번째 형태 · P8 원전 실행) · [[assb-lampe-contact-product-degeneracy]](스물네 번째 적용 · 새 줄 "배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다").

**→ 42편 ≈18.5 — Q5 +0.5 (2차 묶음 넷째 편)**: 42호(Santhosha et al. 2019, 큐 43 — 원장 "0.62 V 의 출생지", 지목 3 회)는 **Li 금속 대비로 쟀다 — 단 액체셀에서.** `[인쇄]` "a Swagelok-type 3-electrode cell with liquid electrolyte … lithium … as counter electrode … and reference electrode" · 1 M LiTFSI DOL/DME · "1 h current pulses … each followed by a 0.5 h rest period" · 실온. 조성 축이 인쇄된 **계보 첫 Li 대비 전위 곡선**이다: 평탄 **0.622 V**(그림 인쇄) · `[인쇄]` "onset of the InLi-phase is already at 47 %" · InLi 균질역 1.9 at% 에 −280 mV · In₄Li₅ 0.339 · In₂Li₃ 0.122 V. `[도표]` 원본 래스터 판독: 평탄 ≈1–47 at%(x 0.01–0.89), 이완 OCV 가 그 안에서 **0.625 → 0.610 V(≈15 mV) 처진다**. ⇒ **α · β 이식 전제("상대극 평탄 = 상수")의 공칭 조성 창을 원전이 준다** — 단 그 창은 (2)(분리막 면 조성) · 율 · 온도를 말하지 않고, 17 · 21 · 41호의 이탈은 전부 창 **안**의 공칭 조성에서 일어났다. **근거가 논문의 측정 + 인쇄된 값**이므로 반 칸: **Q5 열여덟 번째 형태 "다른 전해질의 원전"** — 40호의 R-LTO 1.55 V(ref [11] Costard, 액체)와 짝을 이뤄 **계보의 두 영점이 둘 다 황화물 밖에서 측정됐다**. **반 칸인 이유**: ASSB 밖 · 곡선 1 개(`[인쇄]` "experimental data scatters", 수 0) · 이완 0.5 h 미검증 · 고체 쪽은 대칭 2전극(Li 대비 0). 고체 대칭셀(InLi-(In) 조립 — 21호가 "탈리튬 전류를 냈다" 로 인용한 셀)은 `[재현]` **셀 저항 12 Ω cm² 가 SE 자신의 옴 ≈400–570 Ω cm²(자기 SI 격자 · 전도도) 의 1/25–1/47** — 이온 경로로 입증되지 않는다(21호 creep 가설의 강한 판 = SE 우회 전자 경로와 양립).
**안 움직인 칸**: Q1(`θ(N)` 0/42 — 양극 없음; 상대극 불활성 In ≈11 % 는 칸 밖) · Q2(반 칸 검토 후 접음 — XRD 상 동정은 상대극) · **Q4 0/42 — 서른네 번째 성질 "산포를 문장으로 인정하고 대표값을 세 자리로 인쇄했다"**(누적 0.5 그대로) · Q6(`MPa` 0, 운전 압력 미인쇄) · Q7 · Q8(양극 OCP 0). Q3 층 하나(charge-derived composition axis).

**→ 43편 ≈19.0 — Q5 +0.5 (2차 묶음 다섯째 편)**: 43호(Fukunishi et al. 2023 *ACS AEM*, 큐 44 — 19호 지목; **18호와 다른 논문**, 같은 연구실의 흑연 음극 판)는 R-LTO 1.55 V 를 **다시 인용한다**(`[인쇄]` "Suppose … [40,41]") — 그러나 **R-LTO 가지에서 처음으로 표류 값을 인쇄한다**: `[인쇄]` 333 K 가속 열화 뒤 흑연 · Li-In **둘 다** ≈10 mV 음의 이동, "could be caused by the change of the R-LTO reference electrode potential". `[도표]` 흑연 봉우리가 리튬화 · 탈리튬화 **같은 방향**(−13 … −21 mV — 저항 증가라면 반대로 간다)이고 Li-In 중점도 −16 mV ⇒ 공통 모드 ≈−14 mV. **근거가 논문의 측정 + 인쇄된 배정**이므로 반 칸: **Q5 열아홉 번째 형태 "공통 모드 표류 판독"**(21호 ④ 의 논리를 R-LTO 가지에서 값과 함께 처음 적용). **반 칸인 이유**: "could" · n = 1 · 두 시점 · 같은 지면이 SI Fig. S2 임피던스 합 일치로 "proves the stability"(18호 K–K 와 같은 범주 오류) · 1.55 V 값 자체는 인용. ★★★★ **음극 쪽 곱 축퇴**: 반쪽전지(Li-In 저장소)라 WE 용량 손실에 `LLI` 가 없다 ⇒ 용량 채널은 `(1−LAM_NE)(1−u)` 한 곱. 원전은 이 곱에 "loss of the active material"(dQ/dV **높이**)이라는 이름 하나를 붙이고, 임피던스로 면적 손실을 **따로** 읽는다. `[재현]` 두 채널을 대면 면적 서명(`R_CT` `C` ×0.43 ± 0.2)이 용량(×0.76)보다 크다 — 면적 손실의 일부는 피복이지 고립이 아니고, `LAM_NE` ↔ 고립은 여전히 한 곱이다(우리 계산이라 Q2 는 접음).
**안 움직인 칸**: Q1(`θ(N)` 0/43 — 식 (4) 가 `θ ≡ 1` 을 인쇄) · Q2(반 칸 검토 후 접음 — 채널별 배정뿐, 가른 것은 우리 · 1단계 ↔ 3-a 충돌) · **Q4 0/43 — 서른다섯 번째 성질 "채널별 명명"**(누적 0.5 그대로) · Q6(운전 압력 0) · Q7 · Q8 해당 없음. Q3 층 하나(노화 전후 CPE 삼중 ± 완비).

**→ 44편 ≈19.0 — 새 칸 0 (2차 묶음 여섯째 편)**: 44호(Jin et al. 2015 *Electrochim. Acta*, 큐 45 — 원장 "20호 셀의 원전")는 **20호가 비운 G1 · G2 를 채우고 G3 을 반만 채운다** — G1 양극 TiS₂ : SE : 탄소 = **50 : 50 : 0 wt%**, `0.06 g` = 활물질(20호 N/P 8.4 선다) · G2 σ 1.8 × 10⁻⁴ = **30 MPa 냉간 펠릿 · 차단 SS · 1 kHz–7 MHz · 실온 · 절편 판독**(두께 · 온도 · n 미인쇄) · G3 제조 30 MPa 인쇄, 운전은 Fig. 1 그림에만. **같은 셀은 아니다**(같은 레시피 — SE 0.36 ↔ 1240 µm, 기준극 없음); `[재현]` 20호 음극 438 µm 는 **단층 Li-Si**(복합이면 ≥547 µm) · 20호 R17("362 Ω 전부 양극 복합체 이온 경로")은 SE 겉보기 분율 0.54–0.56 으로 다시 잡으면 **46–69 %**. 칸은 안 움직인다 — 이 편의 "effective contact area" 는 GITT 곱 `√D·S/θ` 를 **대조 셀 가정**으로 쪼갠 신품 값이고(그 가정의 근거 "작업전극에 전해질 없음" 이 처리 셀에도 성립), 용량 손실 배정은 전부 서술이다. `[재현]` **200 µA 세 셀에서 Li 재고 수지가 깨진다**(방전이 이전 충전을 넘어 TiS₂ x > 1) — "탈합금화가 합금화보다 빠르다"(이 편 → 20호) 의 원전 서술과 자기 데이터가 맞지 않는다(우리 계산이라 칸 밖).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/44 — GITT 곱의 한 인자) · Q2(반 칸 검토 후 접음 — 열화 없음, 수지 위반은 우리 계산) · **Q4 0/44 — 서른여섯 번째 성질 "대조 셀 가정으로 곱을 쪼갰다"**(누적 0.5 그대로) · Q5(스무 번째 형태 "GITT `ΔE_s` 안의 상대극 평탄 가정", 우리 판독) · Q6(제조 30 MPa 한 값) · Q7 해당 없음 · Q8(TiS₂). Q3 층 하나(reference-cell-anchored product split). → 갱신 [[assb-lampe-contact-product-degeneracy]](스물일곱 번째 적용 · 처방 표 새 줄 "대조 셀 가정으로 곱 쪼개기") · [[assb-li-in-reference-potential-window]](44호 절 — 스무 번째 형태).

**→ 45편 ≈19.5 — Q5 +0.5 (2차 묶음 일곱째 편)**: 45호(Hertle et al. 2023 *JES*, 큐 46 — 원장 ★★★ "μ-RE 원본, Q5 최대 공백", 16 · 21호 지목)는 **"0 V vs Li" 를 인용이 아니라 상 정체로 정한 원전**이다 — `[인쇄]` "After complete lithiation of gold to AuLi₃, lithium metal is plated on the μ-RE leading to another plateau of 0 V vs Li⁺/Li" · Fig. 7 측정 축 **−618 mV vs In/InLi**(셀 안 Li 금속 ↔ In/InLi — 계보 첫 ASSB 안 인쇄 수, 42호 액체 0.622 · 41호 SI 판독 ≈0.621) · "stable … for at least 8 days" · 실패 기구 인쇄(얇은 Li 는 SE 와 반응해 다른 전위 · Au–Li 평탄은 SE 환원으로 소진) · 유지 절차 인쇄("refreshed", 실험 사이 In/InLi 대비 점검). **근거가 논문의 측정 + 명제**라 반 칸: **Q5 스물한 번째 형태 "셀 안 도금 Li — 영점을 상 정체로, 기준극을 소모품으로"**. `[도표]` 사다리 교차 검사(AuLi/AuLi₃ 개방회로 −0.485 ↔ 도금 −0.618 ⇒ 0.133 ↔ 문헌 0.134 V)가 In/InLi 값에 기대지 않고 도금 Li 를 지지한다(우리 판독). **반 칸인 이유**: 표류 수 0 · 8 일 그림 0 · 누설 0/45 · n 미기재 · 618 mV 의 문장이 가정형("therefore exhibited") · 8 µAh 처방의 리튬화 곡선이 Fig. 7 어느 패널인지 불명. ★ **16호 이식은 조건 밖**(와이어 ∅25 ↔ 10 µm · 면적당 전하 0.27 ↔ 2.55 mAh cm⁻² · NMC 상대극 · 평탄 무) — `[해석]` 도금 Li 가 소진되면 기준은 **AuLi/AuLi₃ 칸(+0.133 V)** 으로 **계단 이동**하고, 그러면 In–Li 가 0.485 V 로 읽힌다 ↔ 16호 한 셀 0.47 V: **16호 0.11 V 의 새 후보**(가설). ★ 합 일치 검증(`[인쇄]` "validating the results of the reference electrode concept and construction")은 DC 전위를 보지 않고 **위치 artifact(재분배)도 합에서 상쇄**된다 — 20 · 40 · 43호 계열, 16호가 원전에서 가져간 검사.

**안 움직인 칸**: Q1(`θ(N)` 0/45) · Q2(반 칸 검토 후 접음 — 2E 적합 비유일성을 S7 이 고르는 것은 우리 판독 · 상대극 Li 소진 용량 귀속은 같은 층) · **Q4 0/45 — 서른일곱 번째 성질 "두 적합 병치로 비유일성을 인쇄하고, 3전극에서는 '물리적 의미' 로 한 모델을 골랐다"**(누적 0.5 그대로) · Q6(제조 382/374 · 운전 63.7 MPa 명시, 스윕 0) · Q7 해당 없음 · Q8(NCM851005, OCP 0). Q3 층 하나(in-cell plated reference). → 갱신 [[assb-li-in-reference-potential-window]](45호 절 — 스물한 번째 형태 · 조건 (9) · P10 · P11) · [[assb-lampe-contact-product-degeneracy]](스물여덟 번째 적용 · 처방 표 새 줄 "합 일치는 분배를 검증하지 않는다").

**→ 46편 ≈19.5 — 새 칸 0 (2차 묶음 여덟째 편)**: 46호(Schlenker et al. 2020 *ACS AMI*, 큐 47 — 21호 ref 17, 원장이 Hertle 행에 병합해 "'0 V 리튬화 금선' 관례의 출처" 후보로 둔 편)는 **기준극을 실제로 썼다 — Au 도금 W 선을 SE 분말에 묻어 함께 압착하고 두 Li 전극에서 Li 를 도금**했다(`[인쇄]` "to reach a constant potential of the reference"). 그러나 **기준 전위 값 · 검증 · 표류 · 누설이 전부 0** 이고, 기준극은 Li\|Li₆PS₅Cl\|Li **대칭셀의 EIS 분할에만** 쓰였다 — 같은 금속 셋 · AC 측정이라 **영점이 결과에 들어가지 않는 자리**다(스물두 번째 형태). Q5 **반 칸 검토 후 접음**: 기준 전위에 관한 논문의 측정 · 명제가 0 이고, 계보 판정은 저자 목록 · 인용 목록의 **우리 대조**다. ★ **계보 최종 판정**: 21호 `[추론]` "Schlenker → Hertle → 16호" 는 **두 줄이 16호에서 처음 만난 것**이다 — 하드웨어 · 저자 줄(이 편 2020, Roling · Miß → 16호 2026, Miß · Roling; 같은 Au 도금 W 선) + 영점 줄(Hertle 2023 Giessen → 16호, 인용 [24]); 이 편은 0 V 를 쓴 적이 없고 Hertle 은 이 편을 거치지 않았다(45호). `[해석]` 16호는 **영점이 필요 없던 자리의 선을 영점이 필요한 자리(NMC 상대 · DC 전위 축)로 옮기며 영점을 다른 연구실에서 빌렸다**. Q7: Li 금속 수명 기구를 저자는 **계면 면적 손실(void · Li 공공 확산) + 씨앗형 도금 → 국소 전류밀도 → 덴드라이트 단락** 으로 읽고 SEI 는 보류(XPS S 2p ≤6 at%) — 단락 판정은 `[인쇄]` "A sudden voltage drop" **한 기준**이고, 완만한 과전압 감소는 두 번(Fig. 1d · 7) **면적 증가**로 배정됐다. `[해석]` 대칭셀은 OCV ≡ 0 이라 연성 단락의 개방회로 서명이 원리적으로 안 보이고, 겉보기 저항 감소는 접촉 개선과 병렬 전자 경로가 같은 부호로 만든다 — 41호(CE 저하 = 누설)보다 한 층 더 가려진 자리.
**안 움직인 칸**: Q1(`θ(N)` 0/46 — 양극 없음) · Q2(반 칸 검토 후 접음 — 음극 계면 "면적 ↔ SEI" 네 채널 논증, 저자 "open question") · **Q4 0/46 — 서른여덟 번째 성질 "'A 또는 B' 를 인쇄하고 두 갈래를 같은 이름으로 끝냈다"**(누적 0.5 그대로) · Q6(층 하나 — 감압 이력, 다른 SE 셀) · Q7(무음극 아님 · SEI 보류 · dead Li 0) · Q8 해당 없음. Q3 층 하나(voltage-shape failure label + undefined error bars). → 갱신 [[assb-li-in-reference-potential-window]](46호 절 — 스물두 번째 형태 · 계보 판정) · [[assb-lampe-contact-product-degeneracy]](스물아홉 번째 적용 · 처방 표 새 줄 "역방향 반쪽 짝").

**→ 47편 ≈19.5 — 새 칸 0 (2차 묶음 아홉째 편)**: 47호(Solchenbach et al. 2016 *JES*, 큐 48 — 원장 ★★★ "금선 기준극 원전 (액체셀)", 21 · 45호 지목)는 **0.31 V 를 Li 금속 대비로 잰 원전**이다 — 액체 Li\|Li T-셀에서 150 nAh 로 금선 절단면을 리튬화하고 개방회로를 >500 h 추적했다(`[인쇄]` "relaxes to ∼0.311 V … LixAu alloy with 0 < x < ∼1.2"). 그리고 **영점을 쓸 조건을 같이 인쇄**했다 — 초기 ≈20 h 제외 · 리튬화 온도 = 운전 온도(25 → 40 °C 는 ≈60 h 에 이탈, 40 °C 리튬화는 −1–2 mV) · 절단면만 노출 · 재리튬화 복원. **Q5 반 칸 검토 후 접음**: 측정 · 명제가 전부 액체이고, ASSB 로 옮긴 근거는 지면에 0 — 28 · 31호 도구 칸 선례. ★ **0.31 V ↔ 0 V 는 같은 선의 다른 칸**(맨 위 · 맨 아래)이고, 45호 digest 의 "21호 0.31 V 는 사다리 어느 칸도 아니다" 는 원전 사다리(첫 칸 0.311 V, x 경계 ≈1.2)로 풀린다. ⚠ 45호가 이 편에 단 "134 / 215 mV" 는 지면에 없다(이 편은 Bach 2015 를 "∼0.3 · ∼0.2 V" 로 옮긴다). ★ **21호 교정 이식**: 가져간 것은 값(두 자리) + 절차이고, 원전 조건 넷 중 둘(단면 노출 → 0.5 mm 원통 ×40 · 리튬화 뒤 2 h 판독 → 원전이 뺀 초기 창 안)을 벗어났다 — 이식이 틀렸다는 증거는 없고 조건이 ASSB 에서 검사되지 않았다. 21호의 이식 자체는 ASSB 안(3 MPa Li\|Li → 20 MPa InLi)이다. "CE 거칠어짐" 은 원문 "We believe"(셀 1 개, `[재현]` 뺀 Li 0.77 nm).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/47 — 액체) · Q2(해당 없음 — 3전극 끝점 이동의 `LLI` 는 해석, 도구 칸) · **Q4 0/47 — 서른아홉 번째 성질 "검사마다 맞는 범주를 골랐고, 판정의 분해능을 대지 않았다"**(누적 0.5 그대로) · Q5(반 칸 검토 후 접음) · Q6 · Q7 · Q8 해당 없음. Q3 층 하나(external-partition-validated + undefined n = 2 error bars). → 갱신 [[assb-li-in-reference-potential-window]](47호 절 — 스물세 번째 형태 · 조건 (10)) · [[assb-lampe-contact-product-degeneracy]](서른 번째 적용 · 처방 표 새 줄 "외부 기준 줄의 다섯 번째 배정").

**→ 48편 ≈20.0 — Q5 +0.5 (2차 묶음 열째 편)**: 48호(Dugas et al. 2021 *JES*, 큐 49 — 21호 ref 16, 원장 "원형 InLi 기준극으로 EIS")는 **기준극이 링이 아니라 WE 와 CE 사이 단면 전체를 덮는 Li₀.₅In : SE 복합층**이고(링은 15 µm Al 집전체), 그 기준극으로 **같은 재료 상대극의 창을 재서 용량 오차로 번역하고 2전극의 허용 조건을 인쇄**했다 — `[인쇄]` "±160 mV"(β-LPS) → "±20 mV so that a 2 electrodes configuration can safely be employed with this electrolyte (20 mV correspond to ⩽2 mA h g⁻¹ at end of charge for NMC)". 계보에서 **상대극 창의 용량 번역을 원문이 스스로 한 첫 문장**이다 — 카드의 "상대극 전위 → 겉보기 `LAM_PE`" 경로의 크기를 저자가 적었다. **근거가 논문의 측정 + 명제라 반 칸**: **Q5 스물네 번째 형태**. **반 칸인 이유**: 창은 전류 중 분극(휴지 복귀 ≈0 ± 0.02 V 는 우리 판독) · 번역은 NMC 충전 끝 한 점 · 영점은 인용 622 mV(42호)이고 **3전극 축은 끝까지 "vs LiIn/In"**(환산 0) · 안정성 "hundreds of hours" 의 수 0 · 누설 0/48 · 산포 0. ★ 같은 지면 Fig. 10a(Li 박 상대극)의 휴지 끝이 기준극의 Li 대비 값을 그려 두었다 — `[도표]` **−0.62 ± ≈0.01 V vs LiIn/In**(우리 판독, 원문 명제 0 — 칸 밖). ★ **21호 인용 셋 대조**: 기하 묘사 ❌(집전체를 기준극으로) · 저주파 변화 "expected" ⚠ 약한 판(Li-In 은 방향 무관 **시간 단조 성장**, 방향 의존은 **Li 금속** 쪽) · 음극 저주파 호 = 전하이동 인용 ❌(이 편은 Li 저주파 호를 "resistive layer" 로, Li-In 은 배정 0). ★ 2전극 재구성: `[인쇄]` "the WE and CE impedances cannot be decorrelated in a 2 electrodes measurement" — WE 모형이 합을 "satisfactory" 적합하면서 중간 호를 139 → 307 Ω cm² 로 잘못 가져간다(같은 셀 시연).
**안 움직인 칸**: Q1(`θ(N)` 0/48 — 손 분쇄 "double percolation" 개선은 가설) · Q2(없다 — `R_CT` 소거법 배정, 곱 미분리) · **Q4 0/48 — 마흔 번째 성질 "비식별성을 두 번 인쇄했다 — 폭은 재지 않았다"**(누적 0.5 그대로) · Q6(층 하나 — 압력 단정의 교락) · Q7 해당 없음 · Q8(OCP 수치 0). Q3 층 하나(fit-by-elimination + removal-test flag). → 갱신 [[assb-li-in-reference-potential-window]](48호 절 — 스물네 번째 형태 · 조건 (11) · P8 상대극 판 · P11 앞 절반) · [[assb-lampe-contact-product-degeneracy]](서른한 번째 적용 · 처방 표 새 줄 "호 제거 검정 + 2전극 합 재구성").

**→ 49편 ≈20.0 — 새 칸 0 (2차 묶음 열한째 편)**: 49호(Barai et al. 2018 *Sci. Rep.*, 큐 50 — 원장 "`R₀`/`R_ct`/`R_p` 작도법 원전", 20호 ref [24])는 ⚠ **액체셀**(상용 20 Ah LFP/흑연 파우치)이고 한 상태(50 % SoC · 25 °C)에서 다섯 방법의 저항을 대조했다 — `[인쇄]` "when timescales match, the resistances derived via different techniques align". **판정: 총량은 같은 양의 다른 창, 성분 이름은 창 경계에 붙인 규약.** `[재현]` 5 C 펄스 `ΔV/ΔI(t)` ↔ EIS |Z|(t = 1/f) −6 … +11 % 로 총량이 한 곡선에 모이지만, 같은 이름의 성분은 방법마다 `R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13 흩어지고 EIS `R_p` 는 경계 0.1 → 0.01 Hz 로 ×3.9 — 원문 스스로 `R_p` "not well-defined" · "pre-defined", DC 분해 "inability to completely separate", ECM "not uniquely identifiable". **옳은 창은 `R₀` 에만 인쇄**("physically more meaningful … after 4ms" — Im Z = 0 교차, `[해석]` 인덕턴스 · 배선 의존), 10 Hz 장비의 `R₀` 과대 `[재현]` **+43 %**(= |Z|(10 Hz)). **Q4 마흔한 번째 성질 "비식별을 두 곳에 인쇄하고 결론에서 지웠다"**(결론 "EIS can accurately provide separation and identification of all the individual resistance components"). ⚠ 결론 "not the non-linearity … rather the timescale" 은 5 C 에서만 보였다 — 같은 10 s 창에서 진폭만으로 `[재현]` ×1.46, 대진폭 다중사인 ↔ 소진폭 EIS 가 ≈0.017 Hz 에서 −24 %. **새 칸 0 인 이유**: 액체 · 한 상태 · 열화 0 — 28 · 31 · 47호 도구 칸 선례. ★ **20호 대조**: 20호가 가져간 것은 원전 텍스트의 **모양 규칙**(곡선 → 직선, 원전 Fig. 1 모식의 선형 외삽 작도)이고 원전의 **시간 규약**("2 sec and 10 sec data points", 5 C · 50 % SoC · 4 h 휴지)은 두고 왔다 — `R_CT` 창 ×≈1.4–2.2 × 10³ · 전류 1/360. 원전 규약으로 1 h ↔ ≈0.28 mHz(원전 EIS 하한의 1/36, "diffusion dominated") ⇒ 20호 3-b 실패(10²–10³ 배)는 원전 틀의 예측과 같은 방향. "분해가 적합조차 아니다 — 작도다" 는 원전에서도 선다(원전도 적합이 아니고 분리 불가를 인쇄). 작도 규약의 실제 출처는 원전 ref 8 **Waag 2013**("usual prescription") — 20호 [25] 와 같은 편.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/49 — 액체) · Q2(해당 없음 — 도구 칸, 총량 일관성) · **Q4 0/49 — 마흔한 번째 성질**(누적 0.5 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 해당 없음. Q3 층 둘(window-differenced reads · unstated-origin ± column-constant). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른두 번째 적용 · 처방 표 새 줄 "창 규약") · [[assb-sensitivity-sweep-vs-identifiability]](49호 절 — 총량 일관성 ≠ 성분 식별 · 대역 끝 흡수).

**→ 50편 ≈20.0 — 새 칸 0 (2차 묶음 열두째 편)**: 50호(Miß · Ramanayagam · Roling 2022 *ACS AMI*, 큐 51 — 16호 ref [30], 원장 "TLM 원본 — 16호의 곱 축퇴 실측 표본이 기대는 모형")는 **곱 `A·j₀` 의 정면이고, 면적과 `j₀` 를 가르지 않았다** — `[인쇄]` "The active area of the CAM particles **in contact to SE** … `a_v = (3ε_CAM)/r_CAM`" · `R_CT = RT/(F j₀)` ⇒ 데이터가 정하는 것은 `j₀·a_v` 이고 `a_v` 는 **완전구 기하**(`r_CAM` 2.5 µm = SEM 으로 공급자 공칭 확인, 수 · 분포 0 · BET 0 · 영상 접촉 분율 0). **16호가 옮긴 "접촉 면적" 이름 붙은 문장의 출생지가 여기다.** 두께 가변은 `R_ion ∝ d` 와 `R_CT/(a_v d) ∝ 1/d` 를 가르지만 `a_v` · `j₀` 는 둘 다 d 무관이라 못 가른다 — NMC 에서만 전이를 가로지르고, **LCO 는 네 두께 전부 두꺼운 극한**(`√(R_ion R_CT/(a_v d))` 한 조합, `[인쇄]` 모형이 두께 추세를 못 따름 "unclear at present"). ★★★★ `[인쇄]` 수정 (ii) `a_v·τd → a_v·d`("for improving the agreement") 는 `[재현]` **`j₀` 를 정확히 ×τ(6.1 · 6.8) 옮기는 규약 선택**이다 — 식 (1)이면 LCO 25.8 → 4.2 · NMC 0.11 → 0.016 A m⁻², 액체 LCO 대비 "almost 2 orders" 의 ×6.1 이 이 한 줄. **비교의 유효성**: 같은 지면 LCO ↔ NMC 는 같은 규약이라 비(×235)가 규약 무관이고 `[재현]` 1단계 R·C 가 τ_CT ×106(`C_eff` ×2.2)으로 **면적 서명이 아니다 — 비교는 견딘다**; 반대로 16호의 "`j₀` 는 SE 전도도와 함께 오른다(≈한 자릿수, 이 편 0.11 대비)" 는 같은 분말 · 같은 규약 · 같은 389 MPa 에서 `1/R` ×12.1 · `C_eff` ×15.4 · **τ ×1.28 — 면적 서명**(전제 `C ∝ θ` 가 SE 교체로 약하다). 3-b ✅(`C_eff` 4.4 · 2.0 µF cm⁻², CAM 기하 면적당). **16호가 가져간 것**: `r_CAM` = 공칭 확인값(같은 분말이라 이식 정당, `[도표]` NMC 는 ≈1–2 µm 결정립 응집체) · 초기값 = 문헌(τ ← Kaiser 2018 · `D` ← 3 편) + 자기 1/30 C 기울기 · ⚠ 16호 `ε_SE 0.505 / ε_CAM 0.495` = **이 편 LCO 칸**(NMC 칸 0.491 / 0.509) · "같은 불일치가 [30] 에도 — 이유 기공 구조" 의 이유는 16호의 것(이 편 "unclear"). **Q4 마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다"**. **Q5 스물다섯 번째 형태 "대칭셀 반 빼기"** — 음극을 40 at% · 125 MPa 대칭셀에서 재어 ≈5–30 at% · 389 MPa 셀에서 뺐고(`[재현]`), `[도표]` 뺀 허수부가 ≈10–120 Hz 에서 음수.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/50 — θ ≡ 1 의 출생지) · Q2(부분 · 신품 방법 원전, `LAM_PE` ↔ 접촉 대상 아님) · **Q4 0/50 — 마흔두 번째 성질**(누적 0.5 그대로) · Q5(반 칸 검토 후 접음 — 조성 · 과차감은 우리 계산 · 판독) · Q6(한 점, 압력 주장 미시험) · Q7 해당 없음 · Q8(LCO 새 화학 + `dU/dc` 시작/적합 — 16호가 이미 준 칸). Q3 층 하나(simulation-matched, 목적함수 미인쇄). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른세 번째 적용 · 처방 표 새 줄 "면적 정규화 규약") · [[spm-grouped-parameter-identifiability]](50호 두 행 — TLM 극한 묶음 · 규약 재척도와 `dU/dc` 닻).

**→ 51편 ≈20.0 — 새 칸 0 (2차 묶음 열셋째 편)**: 51호(Illig et al. 2012 *JES*, 큐 52 — 18호 [29] · 11호 [9] · 47호 [35], 원장 "'전하이동과 접촉저항의 분리' — 곱 축퇴를 가르는 방법의 액체셀 원형")는 ⚠ **액체셀**이고, **제목의 "접촉 저항" 은 양극층 \| Al 집전체 계면**이다 — 카드의 접촉(CAM\|SE 이온 접촉, `θ`)과 다른 물리. **판정: 가른 것은 한 호 안의 곱이 아니라 직렬 두 호(P1C ↔ P2C)의 이름이다.** 채널은 DRT 대역(1 kHz ↔ 1–8 Hz, λ 미인쇄) · 대칭셀 배정 · **`Ea`(0.45 ↔ 0.06 eV — 주 판별자)** · SOC(P1C 7 → 1900 Ω cm² ↔ P2C 131–225) — 전부 측정이고, **이름은 가정**(`[인쇄]` "a transfer process is always temperature activated") + 소거 + 문헌(Gaberscek 2008)이 붙였다. 캘린더링 한 쌍(20 → 10 µm · 64.7 → 41.5 %)은 방향만(`[인쇄]` "proving"), 네 원인 동시 · 음극도 변함 · `[재현]` 고체량 ×0.83. `C` 는 식 (9) 한 줄로만 — `[재현]` Table I 에서 P2C ≈1 µF · P1C ≈3 mF cm⁻²(표 주파수 열 순서를 뒤집어야 `C` 가 온도 불변, D1) ⇒ **대역 분리의 실체는 `C` 의 세 자릿수 차**. `[도표]` 캘린더링 τ: P1C ×≈3.5 · P2C ×≈1/6 — 같은 계면 `C` 전제로는 면적 서명 아님, 그러나 **Fig. 15 도식은 P2C 의 CPE 를 비접촉(전해질 접면) 집전체에 그렸다** ⇒ `[해석]` 전자 접촉 호의 `C` 는 **접촉의 여집합**을 보고 접촉 증가가 τ 를 두 인자로 줄인다 — **처방 1단계 전제의 부호가 계면 종류에 달렸다.** ★ **ASSB 이식**: 방법 형태는 옮겨지고 **판별값은 안 옮겨진다** — 18호 ASSB Al\|복합체 전자 계면 R2 `Ea` 41–70 kJ mol⁻¹ 가 같은 셀 전하이동 R3 49–63 과 겹친다(이 편 P2C 5.8 · P1C 43.4). ★ **가져간 것 대조**: 18호 = DRT 참고문헌만(판별 채널 `Ea` 는 18호가 자기 셀에서 이미 쟀고 반대 결론) · 11호 = 대역("slightly above 10³ Hz")만, 정체 근거(온도)는 두고 왔다 — 원전 안에서 P2C 주파수가 캘린더링 ×≈6 · 반쪽 ↔ 대칭 ×≈2–3 움직인다 · 47호 = R–(R‖CPE)–W 단순화가 **이 편이 가른 두 호를 다시 합쳤다**(10 °C 이 편 LFP 는 P2C ≈150 > P1C ≈25).
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/51 — 액체, 전자 접촉) · Q2(해당 없음 — 도구 칸, 분배 단계) · **Q4 0/51 — 마흔세 번째 성질**(누적 0.5 그대로) · Q5(기준극 0) · Q6(`pressure` 0) · Q7 · Q8 해당 없음. Q3 층 하나(DRT-seeded ECM, names by elimination + assumption). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른네 번째 적용 · 처방 표 새 줄 "`C` 의 자리 · `Ea` 판별값은 계 고유").

**→ 52편 ≈20.0 — 새 칸 0 (2차 묶음 열넷째 편)**: 52호(Oh et al. 2025 *AEM*, 큐 53 — 13호 [34] · 14호 [10], 원장 ★★★ "저압 실셀 — 14호와 같은 연구실")는 **운전 압력을 명시하고 제조와 가른다**(스프링 20 · 3 MPa, 파우치 3 MPa ↔ 제조 150 · 380 · WIP 450 MPa) — 그러나 **압력 비교는 없다**: 20 ↔ 3 MPa 두 점이 양극 적재(20 ↔ 6 mg cm⁻²) · N/P(0.15 ↔ 0.66)와 같이 바뀌고, 반쪽전지 압력은 인쇄되지 않았다. 제목의 "extremely low N/P" 0.15 는 20 MPa 에서만이고 3 MPa 셀은 0.66 · 0.6 이다. 저자가 저압의 "most critical factor" 로 지목한 **음극 계면 안정성**은 3 MPa 고정 음극 교체(SiGr · Li 10 µm · MgSiGr — 15–21 사이클 단락 ↔ 75 사이클)로 받쳐지고, MgSiGr 자신의 저압 감쇠(64.7 %)는 해석 한 줄("volume changes during overcharging, especially under low stack pressure")뿐, **양극 관측 0**. **Q6 반 칸 검토 후 접음** — 운전값 명시는 41 · 45 · 46호도 했고, 요인(25호) · 스윕(39호)이 아니라 교락된 두 점이다; 33호 띠 안의 1차 운전값(실온 완전지 · 파우치)이라는 층 하나. ★★★★ **용량 제한 전극 · 손실 배정은 지면에 없다** — 2전극만, `LLI` · `LAM` 0 회. `[해석]` 충전 끝은 양극(도금 구간 음극 ≈−15…−22 mV vs Li), 방전 끝은 정할 재료가 없다 — α · β 전제(41호 "어느 전극이 끝을 내는가")는 판정 불가. ★★★★ **CE 는 여기서 `LLI` 대리가 아니다**(`[재현]`, 우리 계산이라 칸 밖): 20 MPa 평균 CE 99.2 %(`[인쇄]`) ↔ 유지율 83.7 % — ∏CE ≈0.55, 누적 결손 ≈95 ↔ 손실 ≈27 mAh g⁻¹; **3 MPa 는 CE 가 본문에 없고** `[도표]` ≈85–97 %, 누적 결손 ≈575 mAh g⁻¹ = **NCM811 Li 재고(≈275)의 ≈2 배**인데 용량은 65 % 남는다 ⇒ 결손 대부분이 누설 전자(저자 S17 의 병렬 `r_SS` 경로 · 부반응) 또는 SE 분해 보충 — 41호 "세 번째 오염" 의 실셀 크기 판. 면적당으로 바꾸면 두 압력의 결손은 ×≈1.8 차뿐이고 CE 차의 대부분은 적재 정규화다.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/52 — 음극 XRM 1 시점 정성) · Q2(없다 — 양극 채널 0) · **Q4 0/52 — 마흔네 번째 성질**(누적 0.5 그대로) · Q5 해당 없음(In 0 · Li 박 영점) · Q6(반 칸 검토 후 접음 — 교락) · Q7(없다 — dead ↔ SEI 0, CE 결손은 재고를 넘는다) · Q8(NCM811, OCP 0). Q3 층 하나(two-electrode CE printed for one condition only). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른다섯 번째 적용 · 처방 표 새 줄 "누적 충–방 결손 ↔ Li 재고 상한") · [[assb-stack-pressure-operating-window]](52호 절) · [[anode-free-li-inventory-accounting]](52호 절 — CE 결손이 재고를 넘는다).

**→ 53편 ≈20.0 — 새 칸 0 (2차 묶음 열다섯째 편)**: 53호(Ren · Danner et al. 2023 *AEM*, 큐 54 — 02호 ref 17, 원장 ★★ "`θ(N)` 시간축의 입구 — 1·2호가 동역학을 안 줬다", ⚠ Perspective · LLZO)는 **종설이고, 기대한 입구는 이 편 안에서 닫힌 문으로 확인된다**: 자기 P2D 사례 계산은 `θ ≡ 1`(퍼콜레이션 · 치밀 · 열화 무시를 `[인쇄]`)이고, `[인쇄]` "There is yet no experimental study that incorporates percolation theory and its influence on mechanical degradation" — **`θ(N)` 측정이 2022 년 문헌에 없다는 것을 종설이 적었다.** 문 뒤에 있는 것은 **사이클 축 박리 모델 하나**([127] Barai 2021 — "capacity fade cause[d] by mechanical detachment persists for ten cycles without showing saturation", 공저자 자기 인용)와 **산화물 용량 곡선 재인용 넷**(Tsai [83] · Rosen [104] · Ihrig [105]/[11] · Finsterbusch [12]) — 접촉 분율 0. ★★★★ **산화물 특유의 시점 둘**: 제조(냉각 — Yu [82] 모의 ≈1 GPa ↔ LLZO 파괴강도 100–150 MPa, "fracture … is possible during the cooling", `[재현]` CTE 차 0.2–0.25 × 10⁻⁵ K⁻¹ × ≈1000 K × 150–185 GPa ≈300–460 MPa) ⇒ `[해석]` **`θ₀` 는 공정 변수**(자유 소결 ≈80 % ↔ FAST/SPS ≈95 %) · 운전(첫 사이클 = 산화, 이후 = "fatigue failure … loss of electrochemically active surface area" — **인용 번호 없음**). ★★★ **시간 배정의 역전 — 종설 두 번째 표본**: 두 영역 문장이 인용한 [103] 은 황화물 23호이고 원문은 "contact loss should **only occur during the initial charge** … ongoing … interphase" — 같은 편 §5.2 는 23호를 원문대로 옮긴다("link this phenomenon to an irreversible resistance increase in the first cycle"). 33호(2025)가 같은 역전을 했고, 이 편(2022)이 먼저다. ★★★ **모델 쪽(Danner · Latz)**: P2D 의 `a` 는 SI 어디에도 정의되지 않고 `ε_CAM` 은 75 vol% 고정 — 37호 ① `ε_p` 자리는 없고, 접촉이 들어갈 수 있는 곳은 **`a·i₀₀`(37호 ② 곱) + `a/R_SP`(직렬 옴, 세 번째 곱)** 뿐. 서술은 "active surface area"([32] — 면적 자리)와 "isolation of particles"([122] · [108] — 고립 자리)를 **구분 없이** 쓰고, 제안은 미세구조 분해 + 역학 결합(1 · 2호 형)이다. `[재현]` 이 편의 improved 파라미터에서는 `a` 를 반으로 줄여도 10 mA 계면 과전압 ≈0.7 mV — **면적형 접촉 손실이 전압에 안 보이는 체제**. ⚠ 어긋남 15 건 — **D1 본문 state-of-the-art 1 mA "24 · 15 Wh kg⁻¹ (5 · 3 %)" ↔ Fig. 9D `[도표]` ≈120 · ≈115(23 · 20 %) ↔ SI-2 `[재현]` ≈112** · **D2 시간 배정 역전** · D3 `R_CT` = `R_SP` = 2600 두 칸 · D4 "2.75 → 1.3 after 10 cycles (Figure 7d)" ↔ Fig. 7d 사이클 0 · D5 `a` 미정의 · D8 Fig. 4a In-Li ↔ Li · D9 κ_eff ×10 · D10 `R_CT` 단독 가지 손실 ≈0 · D12 Bucci 문턱 7.5 % ↔ Fig. 4e 최대 ≈6.5 % · D14 결론 "because the SE will not flow to fill the cracks" ↔ 모델에 균열 0.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/53 — 층 하나 "공백의 인쇄") · Q2(반 칸 검토 후 접음 — FAST/SPS 기계 기구 배제 대조는 재인용) · **Q4 0/53 — 마흔다섯 번째 성질**(누적 0.5 그대로) · Q5 해당 없음(⚠ Fig. 4a 축) · Q6 없음 · Q7 해당 없음 · Q8 부분(액체 원전 OCV). Q3 층 하나(cross-system transplanted parameters). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른여섯 번째 적용 · 처방 표 새 줄 "전류 진폭 — 직렬 `R_SP` ↔ `R_CT`") · [[assb-interphase-vs-contact-loss-attribution]](계보 표 53호 행 — 시간 배정 역전) · [[assb-sensitivity-sweep-vs-identifiability]](53호 절 — OAT 스파이더 · 순서 의존 · `d50` 이중 손잡이).

**→ 54편 ≈20.0 — 새 칸 0 (2차 묶음 열여섯째 편)**: 54호(Neumann · Hamann · Danner … Wachsman · Latz 2021 *ACS AEM*, 큐 55 — 원장 ★★★ "GB 저항 모형 원전 + EIS 로 파라미터화된 measured 라벨", 지목 3 회 02 · 27 · 53호; ⚠ Neumann 2020 *ACS AMI* 와 다른 편)은 **양극이 없는 SE 자체의 수송 모델**이고, 세 인자를 **셋이 다른 방식으로** 정했다 — **굴곡도는 FIB-SEM 구조에서 계산**(복셀 위에서 풀어 파라미터 벡터 밖, `[재현]` 구조-만 전도도 ≈ `σ⁰·ε/τ_x²` — 표의 `τ` 는 기하 굴곡도), **벌크 `σ⁰` 7.69 × 10⁻⁴ 는 외부 입력**(`[인쇄]` "estimated … using EIS measurements on highly dense LLCZNO pellets", 문헌 범위 2.4–7.69 × 10⁻⁴ 의 윗끝; 교정 스펙트럼의 벌크 절편은 대역 밖 — `f_C,B` 1.40 × 10⁷ ↔ 장비 상한 ≈1.5 × 10⁷, `[도표]` 실험 호 시작 Re ≈12 ↔ 모델 벌크 절편 ≈28 Ω cm²), **입계 `i₀₀^GB` · `C_DL^GB` 는 재사용 치밀 펠릿 한 스펙트럼 위의 손 보정**(`[인쇄]` "estimate … refined manually", 교정 시편 = 가정된 15 ± 6 µm 다면체 ⇒ `[해석]` 정해진 것은 `d_dense·i₀₀^GB` 한 조합). **곱 `σ⁰·ε/τ²` 은 구조 계산으로 풀렸고, 남은 합 `R_bulk + R_GB` 는 저자가 비식별을 두 번 인쇄한다**("exact deconvolution … unfeasible") — 온도 1 · 입도 ↔ 공극률 교락 · 가르는 채널(고주파 절편 이동, SI S7 `[인쇄]`)이 대역 밖. ★★★★ **원장 "measured 라벨" ❌** — Table S4 범례의 "measured by the authors [°]" 표시 0 개, 전부 "calculated [*]"(σ 는 표시 없음) · 모드 라벨이 아니라 모델 파라미터 · 교정 대상은 남의 논문 스펙트럼 하나. ★★★ **53호 `β` 는 이 편에 없다**(멱지수 · 8 × 10⁻⁴ 0) — `[재현]` Fig. 8 판독에서 `β_tort` 2.31 = **56 % 한 점**(25 % 2.54 · 42 % 2.23), `β_GB` 1.39 는 **치밀 전 모형(2.1 × 10⁻⁴) 정규화에서만** 근처(1.36 · 0.70 · 1.46) ⇒ 그렇게 읽으면 53호의 `σ⁰` 8 × 10⁻⁴ 는 치밀-입계 인자 ×≈0.27 을 빠뜨린 값(53호 SotA `σ_eff` 4.7 × 10⁻⁶ → ≈1.3 × 10⁻⁶, 우리 재구성). 이식 조건 넷: `ε` 범위(0.43–0.75 → 0.25 외삽) · 입도 교락 · `σ⁰` 의 뜻(입자 내부 ↔ 치밀 전체) · 불일치 배정(이 편 "and/or" ↔ 53호 한 칸). ★★ `[재현]` **`C_DL^GB` 는 입계 두께를 정하지 않는다** — 벽돌층 등가 두께 ≈6.8 µm(ε_r 75); 원문의 "in the range reported in the literature" 는 계면당 F cm⁻² ↔ 셀상수 정규화 F 를 환산 없이 비교. ⚠ 어긋남 20 건 — **D3 표 범례 [°] 0** · D2 `R` 자리에 뤼드베리 상수 · D1 "β-LPS" · D6 "25%" ↔ `i₀₀` × 0.75(+33 %) · D7 56 % 구조-만 7.56e-5 ↔ 1.1e-4 · D15 `C` 단위 비교 · **D19 시나리오 1 ASR "fluctuates around 1100" ↔ Table S5 1064 → 655 단조 감소**.
**안 움직인 칸**: **전부** — Q1(해당 없음 — 양극 0) · Q2(없다 — 새 측정 0) · **Q4 0/54 — 마흔여섯 번째 성질**(누적 0.5 그대로; 비식별 인쇄는 SE 수송 계, 카드 방향 아님) · Q5 · Q7 · Q8 해당 없음 · Q6 없음. Q3 층 하나(**재사용 스펙트럼 위 손 보정 · 표 스스로 "calculated"** — 02 · 53호 입력의 상류). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른일곱 번째 적용 · 처방 표 새 줄 "벌크 특성 주파수 ↔ 측정 대역 상한") · [[assb-tortuosity-factor-effective-conductivity-split]](다섯 번째 표본 — 곱은 구조로, 합은 입력으로) · [[assb-sensitivity-sweep-vs-identifiability]](54호 절 — 두 한-파라미터 스윕이 같은 저주파 끝에 닿는다).

**→ 55편 ≈20.0 — 새 칸 0 (2차 묶음 열일곱째 편)**: 55호(Hlushkou · Reising · Kaiser · Spannenberger · Schlabach · Kato · Roling · Tallarek 2018 *JPS*, 큐 56 — 01호 ref 16, 원장 ★ "FIB-SEM **실측** 미시구조 — 합성 기하와 대조")는 **부피분율은 쟀고 연결성 · 접촉 면적은 0 이다** — FIB-SEM 590 장(화소 35.6 nm · 절편 100 nm · 부피 55.9 × 38.9 × 58.1 µm)에서 LCO 33.1 · SE 53.7 · void 13.2 %(`[인쇄]` void 상 = "stabilizing resin and residual voids" — 분리 0), LCO/SE 비 0.616 ↔ 혼합 0.613(39호와 달리 분할이 조성을 보존), CLD μ/k(LCO 3.3/3.64 — 구형이면 ≈12), 분할 문턱 · 수작업 교정은 SI 에만, 유한 크기는 μ · k 만(interparticle μ 는 끝까지 상승). **void 의 두 효과 중 경로만 갈랐다** — 같은 재구성에서 void → SE 가상 치환(LCO 고정)으로 `D_eff/D⁰` 0.574 → 0.786 · `τ` 1.74 → 1.27(`[재현]` `ε/τ` 0.309 → 0.527, 로그 몫 `ε` 41 · `τ` 59 %; Bruggeman 은 무공극 1.22 ✓ · 실제 `[인쇄]` 1.34 — `[재현]` 1.365); **접촉 효과(LCO 표면 중 void 몫 = `φ` 의 짝)는 계산 0**. ★★★★ **실측 대조는 `τ` 로 했고 그 일치는 `ε` 규약이 만든다** — `τ_cond` 1.6 ± 0.1(대칭셀 EIS, `R_ion` 97 ± 2 Ω · 208 ± 5 µm, n = 1) ↔ `τ_diff` 1.74 "close"; EIS 쪽 `ε` 미인쇄 · `[재현]` 관측 곱 `σ_eff/σ⁰` **0.406 ± 0.013** ↔ 모의 void **0.309**(×1.31) · 무공극 0.527 — EIS 시편의 void 는 **재지 않았고** 구조는 **다른 시편**(수지 함침 · 미충전 · 4 t cm⁻² 14 h)에서 계산 ⇒ **54호 "구조가 곱을 푼다" 는 같은 시편일 때의 명제**다(0.406 은 "void 13 % + Bruggeman" 0.394 와도 맞는다). ★★★ **01호 기대는 절반** — 실측 ✅, 01호의 양(`θ` · `A_Spec` · `p_c`)은 0 → 같은 양 대조 불가; 대조되는 것은 입자 형태(k 3.64 ↔ 단분산 구) · SE 연속 기질 · 그리고 01호가 뺀 굴곡도. ⚠ 어긋남 9 건 — **D5 `τ_cond` ↔ `[재현]` 1.53(공칭 ε)** · **D7 "void" = 수지 + void** · D2 "relative increase by 13%"(상대 +24.6 %) · D3 Bruggeman 1.34 ↔ 1.365 · D6 유한 크기 "all phases" ↔ SI 예외 외.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/55 — 부피분율 · 경로 효과는 있고 `θ` · `φ` · `u` 0) · Q2(반 칸 검토 후 접음 — 신품 · 다른 시편 · 수송 곱) · **Q4 0/55 — 마흔일곱 번째 성질**(누적 0.5 그대로) · Q5 · Q7 해당 없음 · Q6 없음(제조 압력만) · Q8 없음. Q3 층 하나(**두 시편 · 두 경로의 `τ` 일치, 측정 쪽 `ε` 미인쇄, 영상 상 = 수지 + void**). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른여덟 번째 적용 · 처방 표 새 줄 "두 경로 대조는 관측 곱으로, 같은 시편 · 같은 `ε` 로") · [[assb-tortuosity-factor-effective-conductivity-split]](여섯 번째 표본 — 두 경로를 한 편이 다 냈고 비교는 `τ` 로) · [[composite-cathode-percolation-utilization]](1호 ref 16 기대 판정).

**→ 56편 ≈20.0 — 새 칸 0 (2차 묶음 열여덟째 편)**: 56호(Bielefeld · Weber · Rueß · Glavas · Janek 2022 *JES*, 큐 57 — 원장 ★★ "pore(void) 문턱 → 1호 `p_c`", 원장 정정 "FEM 시뮬레이션")는 **void 를 접촉 자리(`φ`)에만 넣었고 경로 효과는 구성상 0, 검증 모델에서는 void 자체가 0 이다** — 입자형 재구성(검증 · PSD · `D̃`/`j₀`)은 `[인쇄]` "SE … in ideal contact, filling all remaining volume"(실험 void 14 % → SE; `[재현]` SE 부피 ×1.32), 1-입자-void 모델은 CAM 표면 반구로 피복률(100 → ≈52 %)과 크기(`d_CAM/d_Void` 1.2–10)를 스윕, 이온 퍼콜레이션은 "not capable to quantify". ★★★★ **01호 `p_c` 는 이 편에서 반례를 만났다** — SI `[인쇄]` 42 vol% 무작위 구는 01호대로면 전자 퍼콜레이션 불가 ↔ Rueß 셀은 문제 없음 → placeholder 트릭 + 고립 입자 "moved manually" ⇒ `θ` 는 입력 1. **"pore 문턱 → 저항 급증"(14호 [69] · 원장)은 이 편에 없다**(`threshold` · `surpass` 0 · void 부피 스윕 0). ★★★★ **`j₀` 는 FEM 출력이 아니라 입력**(Rueß EIS `R_CT` → 식 (12), `A` 미정의) — 50호 "10⁻⁵ A cm⁻² ≈ NMC 0.11" 은 EIS ↔ EIS 이고 면적 규약은 판정 불가(`[재현]` 모델 CAM 면적 기준 ASR ≈112 ↔ 기하 면적이면 ≈1520 Ω cm²). ★★★ **void 스윕은 `θ`-전용 조작이 아니고 `φ` 하나로도 요약되지 않는다**(모델 명제): `[도표]` 0.2 C @50 · `A` ≈53 % ≈47 mV ↔ `[재현]` BV 면적 몫 ≈21 mV(≈44 %) · `φ` 70 % 고정에서 크기 1.2 → 10 이 ≈50 → ≈19 mV — 37호 `A_eff ↔ k` 항등이 3D 에서 **부분 파괴**. 검증은 남의 첫 충전 곡선 3 율 · 오차 척도 0 · 본문 "best" 는 상수 세트(D3). 55호 표적(13.2 % · `τ` · `k_SE` · 0.616)과 같은 양 0 — 55호(경로만) ↔ 56호(접촉만)가 서로의 빈 칸. ⚠ 어긋남 14 건 — **D2 "none fitted" ↔ PSD 선택** · **D3 "best" 상수 ↔ 결론 "not capable"** · **D4 void 4 µm ↔ `[재현]` 5.8** · **D5 0.5 C 점 없음** · **D7 void 14 % "재구성" ↔ 0 %** · **D12 · D13 계보 귀속** · D1 `T` 273.15 K 외.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/56 — 층 하나 "`φ` 모델 스윕 · 분포가 두 번째 손잡이", 모델 명제) · Q2(없음) · **Q4 0/56 — 마흔여덟 번째 성질**(누적 0.5 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8(층 하나 — 02호 `U₀` 경유지). Q3 층 하나(**비적합 선언 + 이산 선택 + `j₀` 면적 미정의**). → 갱신 [[assb-lampe-contact-product-degeneracy]](서른아홉 번째 적용 · 처방 표 새 줄 "`φ` 고정 분포 스윕") · [[composite-cathode-percolation-utilization]](01호 `p_c` 의 반례와 수작업 강제) · [[assb-apparent-capacity-decomposition]](`u` 표본 — 연결된 큰 입자의 미활성).

**→ 57편 ≈20.0 — 새 칸 0 (2차 묶음 열아홉째 편)**: 57호(Bielefeld · Weber · Janek 2020 *ACS AMI*, 큐 58 — 원장 ★★★ "1호 직계 속편 · 24호 14 % void · `τ` 정의의 출처", 56호가 넘긴 "pore 문턱" 귀속 후보)는 **계보에서 void → 유효 이온 전도도를 계산한 유일한 Bielefeld 편이지만, "pore 문턱" 은 여기에도 없다** — void 스윕은 `φ_void` 5 · 10 · 20 % **세 점**(d 5 µm)이고 `[인쇄]` "2-fold higher effective conductivities for 5% void space, compared to 20%" 로 단조; `threshold` 0 · `abrupt` · `steep` 넷 다 **AM 분율 축**. 14호 문장의 세 요소(void 축 · 문턱 · 저항 급증)는 01 · 56 · 58 어디에도 함께 없다(01호 = 공극률 문턱 34 · 21 % 이나 퍼콜레이션 판정 · 전도도 0; 58 = 전도도이나 문턱 0; 56 = 둘 다 0) ⇒ **귀속 출처 불명**, 14호는 01 · 58 둘 다 인용 0. ★★★★ **유효 전도도 모델은 곱 `σ⁰·ε/τ²` 을 구성상 푼다 — `τ²` 는 `σ_eff` 의 이름표**(식 (11), `[재현]` Fig. 4 `τ²` 가 `σ⁰` 2.7 로 재현) · Bruggeman 은 최대 4 배 과소 · 수정식 α 2.02–1.21(`[재현]` 전도도 지수 3.02 · 2.21) — 저자 "do not offer any further scientific insight". **실험 대조는 한 점**(Kato 2018 `σ_eff` 0.68 ↔ 0.73, void 15 % 가정; `[재현]` 곱 비 1.07) — 같은 지면 void 손잡이가 ×2 라 검증이 아니라 가정과 모델의 공동 맞춤. ★★★★ **바인더 = `θ_AM` 불변(구성상) · `A_spec,a` ↓ 17–82 %(피복 + SE 고립 미분리) · `σ_eff` ↓ · `θ_SE` ↓** — 37호 틀로 `ε_p` 자리가 아니라 `A_eff·k` 자리와 `κ_eff` 자리를 한 손잡이로 깎는다(모델 명제); `[재현]` `τ²` 는 순수 SE `ε` 로 나눔 → 증가분은 경로 차단 몫. ★★★ **01호 `p_c` 계보**: 01 `p_c(d)` 출력 → 58 Fig. 5b 에 말없이 재현(49 → 50 vol%, `p_c` 낱말 0) + "탄소로 전자 비제한" 선언과 모순된 탄소 없는 `A_spec,a`(D8) → 56 반례 · 수작업 `θ = 1`. Nam 2018 대조의 "작은 AM 일치" 는 `p_c` 아래 ≈0 ÷ ≈0(D7). ★★★ **55호와(비교용)**: void 기본값 15 % 의 출처가 55호 13.2 %(수지 + void, D10) · void 효과 로그 몫 `τ²` 70 %(이 편 50:50) ↔ 55호 59 % — 같은 방향. **24호 귀속(D13)**: 24호 "14% … void (… 41 …)" · "point contacts" ↔ 이 편 15 % · `point contact` 0 — 원장 "14 % void 출처" 는 절반(τ² 정의 ✅ · 14 % ❌). ⚠ 어긋남 13 건 — **D1** 극한식 `lim_{d→0}` = 6.40(적합은 d → 0 에서 발산, 6.40 은 d = 1 µm 값) · **D3** 표 1 고출력 `τ²` 1.7 ↔ 인쇄 전류는 1.50 에서 나옴 · **D4** 바인더 전류 `v_SE` 규약(×1.30 · ×1.15 과대) · **D6 · D7** Nam 삼각형 4 개 · `p_c` 아래 점 · **D8** 탄소 가정 ↔ 탄소 없는 `A_spec,a` · **D12 · D13** 계보 귀속 외.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/57 — 층 하나 "바인더 = `θ_AM` 불변 · 두 곱 동시 손잡이", 모델 명제) · Q2(없음) · **Q4 0/57 — 마흔아홉 번째 성질**(누적 0.5 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 없음. Q3 층 하나(**유도 `τ²` + 가정 void + 남의 GITT 비**). → 갱신 [[assb-lampe-contact-product-degeneracy]](마흔 번째 적용 · 처방 표 새 줄 "한 공정 손잡이가 두 곱을 같이 깎을 때") · [[assb-tortuosity-factor-effective-conductivity-split]](일곱 번째 표본 — 구조 계산이 곱을 풀고, 검증은 가정 `ε` 로) · [[composite-cathode-percolation-utilization]](`p_c` 계보 01 → 58 → 56 · "pore 문턱" 귀속 판정).

**→ 58편 ≈20.0 — 새 칸 0 (2차 묶음 스무째 · 마지막 편)**: 58호(Asheri · Fathidoost · Glavas · Rezaei · Xu 2023 *Comput. Mater. Sci.*, 큐 59 — 15호가 지목한 "유일한 SSB-ML 인용", 원장 정정 "측정 아님, 시뮬 대리모형")는 **박리를 계산하는 계보 첫 편이지만, 박리가 거시 식에 들어가는 자리는 `LAM_PE` 다** — `[인쇄]` 식 (32) `a = (S/V)(1−ε_e)(1−⟨d⟩)` · "the loss of contact … is considered to be the same as ⟨d⟩" 는 면적의 말이지만, 미세 입자는 손상과 무관하게 전 표면으로 플럭스를 받는다(`[코드]` 학습 자료 12,304 행 전부 `soc_dot/(2|j|)` 0.9987–1.0013) ⇒ `a·(1−⟨d⟩)` 는 `ε_s(1−⟨d⟩)` 와 같은 결합(`[해석]`), `[재현]` 저율 극한 손실 `∫⟨d⟩dSOC/0.5` 8.9 % · 3.9 %(`G_c` 4.21 · 5.97) ↔ `[도표]` 1 C 셀 8.7 · 3.1 %. **`θ(N)` 은 구조적으로 0** — 한 방전(0.5 → 1 `c_max`) · 출력 ReLU 가 충전을 막는다 · 대리 입력에 `⟨d⟩` · `ξ` 없음(저자 "RNN … history effects" 를 향후 과제로). `[재현]` 손상은 사실상 **SOC 의 함수**(`|j|` ≤ 0.03 에서 궤적 겹침 ≈1 %) — Fig. 10 "higher C-rates … damage … evolves faster" 는 시간 축 명제. **대리는 원 모델의 식별성을 물려받고 검증도 원 모델 안에서 닫힌다** — `[코드]` 행 무작위 분할(같은 90 궤적의 이웃 시간 단계) · unseen `G_c` 5 · 10 은 범위 안 두 점 · 그 `j` 는 학습 격자 값 · 셀 수준 손상 계산은 FE² 기준해 없음 · 불확실성 0. ★★★ **코드 대조**: 표 4 ✅(R² 0.99796 · MSE 1.06×10⁻⁴) · **표 5 R²₁ 0.99184 = bigJ 노트북 *학습* R²** · 손상 노트북 셋 `r2_score(y_pred, y_true)` 인자 역순 · 벤치마크는 sklearn MLP · 출력 `identity`(지면 Keras · ReLU) · Keras 셋 L2 없음 · **D1 플럭스 척도** — 인쇄 `J_s` 783 · 261 · 183 = 자료 `j` × 2609.6, Fig. 8 채움 ≈245 s 는 `j` ÷ 2609.6 이어야(×6.8 × 10⁶). ⚠ 그림 둘이 서술과 어긋난다 — **D10** Fig. 10 전달 전하 2 C ≈3780 > 5 C ≈3575 > 1 C ≈3450(1 C·s) ↔ "delivered capacity is smaller" · **D11** Fig. 11 `G_c` 13.92 · 9 가 Fig. 9 무손상보다 늦게 끝난다. 15호 인용은 어휘상 맞으나 "degradation" = 한 방전 안 손상, SBMS 기능 0.
**안 움직인 칸**: **전부** — Q1(`θ(N)` 0/58 — 층 하나 "박리 = 결합상 `ε_p` 자리 · 한 방전 안 `⟨d⟩(SOC)`", 모델 명제) · Q2(없음) · **Q4 0/58 — 쉰 번째 성질**(누적 0.5 그대로) · Q5 · Q7 해당 없음 · Q6 없음 · Q8 없음. Q3 층 하나(**simulated-surrogate**). **2차 묶음(큐 40~59) 종료 — 스무 편에서 칸 이동 Q1 +0.5 · Q5 +2.5 · Q6 +0.5 — ≈16.5 → ≈20.0, 전부 39–48호 안, 49–58호 열 편 연속 새 칸 0; Q4 는 0/58 · `θ(N)` 측정량 0/58.** → 갱신 [[assb-lampe-contact-product-degeneracy]](마흔한 번째 적용 · 처방 표 새 줄 "박리 변수의 거시 자리는 미세 경계조건이 정한다") · [[assb-sensitivity-sweep-vs-identifiability]](C-율 · `G_c` OAT 스윕 표본).

## ★★★★ 2026-09-22 (19호 Yoshida et al. 2024) — **기준 전위를 재지도 가정하지도 않고 소거한 첫 편, 그리고 상대극이 관심 대역을 통째로 덮는다는 것을 저자가 인쇄한 첫 편**

`raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md`
(*Electrochim. Acta* **497** (2024) 144523, **CC BY 오픈액세스**, Tokyo Tech).
★ **18호와 같은 연구실의 같은 계보**다 — Ikezawa·Okajima·Arai 셋이 겹치고, 감사문이
**18호 제1저자 Goro Fukunishi** 에게 기술 자문을 사례한다. 큐 축은 **Q5**였고 메모는
*"상대극 전위 변화가 선형이 아니다"* 였다 — **그 메모는 맞다**(아래 절 2).

### 0. ⚠ 먼저 경계 — **이 편에는 전극이 없다**

복합양극도 활물질도 용량도 사이클도 없다. 잰 것은 **황화물 SE 펠릿 두 장을 포개서 만든
계면 하나의 Li⁺ 수송 저항**뿐이다. ⇒ **Q1·Q2·Q3(라벨)·Q7·Q8 에 구조적으로 기여할 수
없다.** 이 편이 이 카드에 들어오는 이유는 **Q5 의 구조**와 **Q2(분해 비유일성)의 계보**,
그리고 **곱 축퇴 처방의 세 번째 적용** 셋이다.

### 1. ★★★★ Q5 — 기준 전위를 **소거하는** 설계가 존재한다

계보는 **재지 않았다 → 가정했다 → 쟀다 → 가정을 옮겼다** 로 왔다.
19호는 **다섯 번째 형태**다: **측정량을 차분으로 잡아 절대값을 없앤다.**

- 4전극 = **RE 두 개(전위) + CE 두 개(전류)**, 두 RE 를 계면 **양쪽 펠릿 중앙면에 매립**.
  측정·제어되는 것은 `[인쇄]` **RE₂(오른쪽) − RE₁(왼쪽)** 이고,
  `[인쇄]` Fig. S1: "can measure or control the potential between two reference electrodes
  **without the polarization of the two counter electrodes**" (3전극은 **WE 분극을 포함**,
  2전극은 **둘 다 포함**).
- ⇒ **같은 재료의 RE 를 둘 쓰면 R-LTO 의 절대 전위가 상쇄된다.** 실제로 이 편에는
  `assum*` **0 회**, "**1.55**" **0 회**다 — **18호의 G4(“Assuming 1.55 V”)가 생기지 않는다.**
- ★★★ **대신 새 바닥이 인쇄된다**: `[인쇄]` 세 셀의 RE–RE 개방회로 전압이
  **−4 / −5 / +25 mV** 이고 "These potentials are **within the reproducibility of the
  reference electrode potentials (ca. ±30 mV)**".
  ⇒ **① 계보 최초의 인쇄된 기준극 재현성 숫자 ② 그것이 이 측정계의 검출 하한
  ③ 황화물 3 종 사이에 검출 가능한 Li⁺ 활동도 차가 없다.**
  ⚠ **±30 mV 의 근거가 지면에 없다** (데이터도 인용도 없다) — ref [18](Ikezawa 2020)에
  있을 가능성이 높고, 그것이 후속 1 순위인 이유다.
- ★★ **R-LTO 의 조성이 처음 인쇄된다**: `[인쇄]` **Li₇Ti₅O₁₂ : Li₄Ti₅O₁₂ = 67 : 33 mol%**
  ⇒ 2 상 한복판. **18호의 "partially reduced"(화학량론 불명) 공백이 절반 메워진다.**
- ⚠⚠ **그러나 기준극 검증의 범주 오류는 그대로다.** 18호는 **K–K 잔차**로 기준극 안정성을
  주장했고, 19호는 `[인쇄]` **진폭 비의존성**(10 mV ↔ 50 mV 중첩)으로 "**not derived from
  artifacts related to the RE**" 를 주장한다. **진폭 비의존성은 선형성을 보지 기원을 보지
  않는다** — 기하학적 수축·프로브 결합 같은 **선형 artifact 는 정의상 진폭 무관**이다.
  ⇒ **같은 그룹, 같은 구조의 추론이 두 번.** 올바른 검사는 **기준극 위치·개수·재료를 바꿔
  스펙트럼 불변을 보는 것**이고 두 편 다 안 한다.

### 2. ★★★★ 큐 메모의 출처 확정 — **"상대극 전위 변화가 선형이 아니다"**

> `[인쇄]` §3.2 마지막 문단: "The potential change in the counter electrode is **not
> linear**, and the voltammogram of the counter electrode is **asymmetric**, especially in
> the case of the LGPS | LPSCl cell. This result shows that the **polarization of the
> counter electrode affects the voltammogram** … measured with the **two-electrode system**
> using the Li-In counter electrode."

근거 그림은 **Fig. S4**(Li-In 상대극의 `E_CE`(t) + `I`–`E_CE`, 세 셀). `[도표]` 판독:

| 셀 | `E_CE` 진폭 (200 s, CV 1 사이클) | 전류 범위 | `[재현]` `ΔE/ΔI` | 같은 셀의 계면 저항 `R₂` |
|---|---:|---:|---:|---:|
| LPSI \| LPSCl | **≈42 mV** (−988 … −946) | +0.49 … −0.46 mA | **≈44 Ω** | 21.5 Ω |
| LGPS \| LPSI | **≈126 mV** (−1021 … −895) | +0.26 … −0.215 | **≈221 Ω** | 12 Ω |
| LGPS \| LPSCl | **≈75 mV** (−968 … −893) | +0.20 … −0.70 | **≈83 Ω** | 29.3 Ω |

★★★★ **"4전극이 3전극보다 무엇을 더 재는가" 의 정량 답이 여기 있다**:
**상대극 가지가 관심 신호보다 2–18 배 크다.**
★ **비선형의 실체**: `[도표]` LGPS\|LPSCl 에서 `E_CE` 의 극값이 **t ≈ 23 s · 124 s** 인데
CV 의 반전은 **50 s · 150 s** 다 — **27 초 앞서고, 하강 구간이 상승 구간의 1/4** 이다.
★★ **그리고 이것은 재고 고갈이 아니라 가역 분극이다** (`[재현]` CV 반주기 통과 전하가
Li 재고의 **0.39 %**, 200 s 뒤 `E_CE` 가 출발값으로 복귀).

### 3. ★★★★ Q5 의 경계 조건에서 **(ㄷ)만 깬 첫 표본**

18호 digest 가 세운 셋: **(ㄱ) 조성이 2 상역 안 · (ㄴ) Li 재고 / 이동 전하 ≥ 한 자릿수 ·
(ㄷ) 전류밀도 ≲ 0.1 mA cm⁻².**

| | 17호 (foil·CA) | 18호 | **19호** |
|---|---|---|---|
| (ㄱ) `x_Li` | 40 at% | 37.7 → 40.0 | **25 at%** ✅ |
| (ㄴ) 재고 여유 | ≈5 배 ❌(고갈) | 9.5 배 ✅ | **≈260 배** ✅✅ |
| (ㄷ) 전류밀도 | ≈16 mA cm⁻² ❌ | 0.054 ✅ | **0.41 – 1.07** ❌ |
| **관측 `ΔE_CE`** | **+680 … +780 mV**(지속) | **≈0** | **42 – 126 mV**(가역) |

⇒ ★★★ `[해석]` **재고 여유가 충분하면 전류밀도를 20 배 올려도 이동은 10⁻¹ V 에 못
미친다. 17호의 0.7 V 는 전류밀도가 아니라 고갈의 산물이다.**
⚠⚠ **네 편을 가로지르는 추론이고 통제 실험이 아니다** — SE·압력·조성·제조법이 전부 다르다.
그리고 19호의 이동은 **가역 분극**, 17호의 것은 **지속 이동**이라 같은 양이 아니다.
⚠ `[재현]` **(a)의 42 mV 는 CE–RE 옴 강하(≈`R₁`/2 ≈ 42 Ω)와 구별되지 않는다.**
(c)의 221 Ω 은 `R₁/2 ≈ 104 Ω` 의 2 배라 **절반은 옴이 아니다.**
★ `[재현]` 18호의 1.55 V 를 빌리면 **Li-In ≈ 0.60 V @ 25 at%** — 17호(0.61) · 18호(≈0.60)와
일치하고 **조성이 25 ↔ 40 at% 로 다르다** ⇒ 2 상 평탄의 교차 조성 확인.
⚠⚠ **1.55 V 는 이 편에 없는 값이다. 채움표에 올리지 않는다.**

### 4. ★★★★ Q2 — 분해 비유일성 계보의 **네 번째 층, 그리고 가장 근본적인 층**

`[인쇄]` Fig. S5(3전극으로 Li-In 전극 자신의 임피던스를 잰 것):
> "the Li-In electrode showed semicircles in the frequency ranges **overlapping with P1
> (above ca. 1 kHz) and P2 (ca. 1 kHz to 0.1 Hz)**" ·
> "**poor reproducibility of the InLi impedance**" ·
> "These results show that **P1 and P2 are difficult to extract from the impedance
> measured with the two-electrode system with InLi counter electrodes**."

`[도표]` **같은 공칭 Li-In 박(25 at%)의 전극 저항이 39 / 172 / 54 Ω — 4.4 배 (n = 3).**

계보에 놓으면:
- **10호(Vadhva)**: 유일해가 없다 + 귀속이 **화학의 함수**.
- **11호(Yu)**: 봉우리 이름표가 **상태·배선·조작**으로 흔들린다(−15 … +69 %).
- **16호**: 전극별 DRT 의 **합이 완전지 DRT 가 아니다**.
- **18호**: 같은 화학에서도 **양극 미세구조**(단결정 ↔ 다결정)가 "저주파 = 음극" 을 깬다.
- **19호**: ★ **음극 자체가 1 MHz – 0.1 Hz 전 대역에 걸쳐 있다.**
⇒ ★★★ **18호와 충돌이 아니라 보강이고, 한 층 아래다** — 양극을 바꿔도 음극은 그대로
거기 있다. `[해석]` **주파수만으로 성분을 전극에 배정하는 모든 절차는, 같은 셀에서
배선으로 검증되기 전까지 가설이다.** 그리고 **19호는 그 검증을 하는 배선을 보여 준다.**
→ [[drt-peak-count-nonidentifiability]]

### 5. ★★★★ 곱 축퇴 처방의 **세 번째 적용** — 부분 적용 + 전제 반증 + 대체 채널

입력은 **처음으로 완비**된다(Table 2 가 `R`·`Q`·`p`·`C`·`τ` 를 3 셀 × 2–3 성분 전수 인쇄,
`C` 는 저자가 **Brug 식**으로 직접 계산). 면적을 바꾼 조작도 셋이다(**압력 2 점 · 단면적
3 점 · 계면 유무 대조**). 그런데:

- **검사 A (절대 크기) ⇒ 전제 반증.** `[재현]` `P2` 의 `C` = **1.6–3.8 mF**,
  기하 단면(φ10 mm)으로 나누면 **2.0–4.8 mF cm⁻² = 이중층(10 µF cm⁻²)의 200–480 배**.
  **접촉 면적은 기하 면적을 넘을 수 없다** ⇒ **`P2` 의 `C` 는 접촉 면적의 대리가 아니다.**
  (`p` = 0.55–0.61 로 CPE 가 극단적으로 눌려 Brug 변환 자체가 불안정.)
  ⇒ **18호는 "예측보다 2–3 배 빗나감", 19호는 "물리 상한을 2–3 자릿수 초과".
  전제가 같은 방향으로 두 번 연속 깨졌다.**
- **검사 B (셀 간) ⇒ 두 채널이 70 배 충돌.** `[재현]` `τ₂` 가 **36–46 ms 로 ±13 % 안**
  ⇒ `C` 채널은 "**유효 면적만 다르다**"(면적 차 2.4 배)고 말한다. 그런데 `Ea(R₂)` 는
  **27 / 41 / 42 kJ mol⁻¹** 로 15 갈린다 ⇒ `[재현]` 전지수 인자가 **158–174 배** 보상해야 한다.
  **면적 차 2.4 배 ↔ 158 배.** ⚠ 단, 세 계면은 **물리적으로 다른 계면**이라
  "면적만 다르다" 가 애초에 성립할 이유가 없다 — 18호 검사 B(**동일 계면의 두 상태**)와
  성질이 다르다.
- **검사 C (압력) ⇒ 적용 불가.** `R₂` 는 `[도표]` 560→840 kPa 에서 **−26 %** 인데
  **`C`·`Q`·`p` 가 두 압력에서 인쇄되지 않는다.** ⇒ **18호와 정확히 반대의 결손**
  (18호는 `C` 가 있고 면적을 아는 조작이 실패했다).

★★★★ **대신 논문이 대체 채널을 준다**:
> `[인쇄]` "the **physical state of the interface does not affect the Ea** but the
> resistance values. It is thus proposed **Ea as the essential parameter** to describe the
> nature of the ion transport."
>
> ⇒ **`R(T) = A(θ)·exp(Ea/RT)` 에서 `Ea` 는 접촉 면적과 직교한다.**
> **노화 전후 `Ea` 를 같이 재면 `C_dl ∝ θ`(두 번 깨진 전제) 없이도
> "면적이 줄었나 화학이 나빠졌나" 의 필요조건 검사를 할 수 있다.**
> ⚠ **충분조건은 아니다** — `A` 에 면적 외의 항이 있다(검사 B 의 보상 효과가 증거).

★★★ **그리고 이것이 18호로 되돌아간다**: 18호는 `Ea` 를 **신품 축에서만** 쟀다.
**18호가 `Ea(노화 전후)` 를 쟀다면 검사 B 의 결론이 `C` 없이도 독립 확인됐을 것이다.**
→ [[assb-lampe-contact-product-degeneracy]] 처방에 줄 추가.
⚠⚠ **그런데 `Ea` 불변의 근거도 약하다** — 2 점 · n=1 · 범위 1.5 배, 그리고 아래 절 6 의
허용오차(≥5 kJ mol⁻¹)를 쓰면 **압력이 `Ea` 를 3 kJ mol⁻¹ 움직여도 못 본다.**

### 6. ★★★★ 이 편이 주는 **산포 하한** — 인쇄된 ± 의 12–50 배

`[도표]` **Fig. 7(c)**: LPSCl\|LPSCl 셀의 `Ea(R₁)` = **45.5 ± 0.1** kJ mol⁻¹.
`R₁` 은 정의상 **LPSCl 벌크뿐**인데, 같은 물질의 Table 1 값은 **40.5 ± 0.3** 이다.
⇒ **5.0 kJ mol⁻¹ 차이 = 인쇄된 ± 의 12–50 배. 논문은 언급하지 않는다.**
★ 그리고 저자 스스로 `[인쇄]` **LGPS 의 `Ea` 가 냉간↔열간 성형으로 11 kJ mol⁻¹ 움직인다**
고 적는다 — **`Ea` 는 물질 상수가 아니라 미세구조의 함수**다.
⇒ `[해석]` **모든 `Ea` 비교의 실질 허용오차는 ±0.1–3 이 아니라 ≥ ±5 kJ mol⁻¹.**
그 눈금으로 보면 논지의 네 비교는 통과하지만 **"다르다" 를 말할 해상도가 사라진다.**

다른 두 산포도 같은 지면에: **Li-In 전극 임피던스 4.4 배**(절 4) ·
`[인쇄]` **"the magnitude of P3 varies from cell to cell"** — `[도표]` Fig. 7(a)의 P3 는
**≈35 Ω** 로 Table 2 의 **4.8 Ω 의 7 배**이고 **이 편의 계면 저항(8–29 Ω)보다 크다.**
⇒ ★★ **정체 미상(`crack`, 본문 1 회, 영상 0)이고 셀마다 7 배 다르며 `P2` 바로 옆
주파수에 있는 성분이 회로 안에 있는데, `P2` 적합의 `P3` 민감도 검사가 0 이다.**

### 7. ⚠⚠ 중심 배정이 걸린 그림이 **4 점 · 이상치 1 개**다

논문의 배정(P1 = 벌크, P2 = 계면)은 두 스윕에 걸려 있다.
- **단면적 `S` 축은 판별력이 없다** — 벌크도 계면도 `1/S` 로 스케일한다. 논문도
  `[인쇄]` "within solid electrolyte pellets **or** at the interface" 라고만 적는다.
  `[도표]` 게다가 `R₂·S` 가 **112 / 105 / 244 Ω mm²** 로 **2.3 배** 흩어지는데
  "roughly in proportion" 이라 부른다.
- **그래서 전부가 `d` 축 하나에 걸린다.** `[도표]` Fig. 4(d) `R₂/d` =
  **17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹.**
  ⇒ **0.88 mm 의 15.0 Ω 를 빼면 남은 3 점은 `R₁` 만큼 깨끗하게 `d` 에 비례한다**
  (산포 **1.10 ×** ↔ `R₁` 의 **1.12 ×**) — **논문 결론과 반대**가 된다.
  **같은 4 점이 정반대의 두 읽기를 허용하고, 논문은 이상치를 언급하지 않는다.**
- ★★★ **다만 결론은 살아남는다** — 같은 지면의 **Fig. 7**(LPSCl 단일 펠릿 ↔ LPSCl\|LPSCl
  적층: **계면 하나만 추가하면 `P2` 가 생긴다**)이 훨씬 강하게 지지한다.
  ⇒ `[해석]` **논증 순서가 거꾸로다** — 약한 것이 1 차 근거이고 강한 것이 "consistent with" 다.
- ★★★★ **그리고 그 Fig. 7 이 우리에게 가장 값진 것**이다: **같은 재료 · 같은 공정 ·
  계면 하나만 추가한 대조군.** 접촉 손실 연구가 원하는 대조군의 교과서적 모양이고,
  **18호 검사 A(신품 입자 크기 축)가 실패했던 자리의 대안 설계**다.
  복합양극 판으로 옮기면: **같은 활물질·SE·공정에서 계면 수/면적만 바꾼 전극 쌍.**

### 8. ★★ Q6 — 계보 최저 압력대, 그리고 **산업 요구치 안에 들어온 첫 편**

`[인쇄]` 조립 **ca. 420 kPa**(토크 렌치), 스윕 **560 / 840 kPa**(2 점), 성형 **280 MPa**.
비교: 16호 97/389 MPa · 17호 50 MPa · 18호 **미보고** · 5호 1–75 MPa · 6호 2–4 MPa.
⇒ ★ **8호가 인쇄한 산업 요구치 <≈1 MPa 안에 들어오는 첫 편.**
⚠ 2 점 · 범위 1.5 배 · n=1, 그리고 `[재현]` **420 kPa 의 `R₂`(21.5 Ω, Table 2)가
560 kPa 의 `R₂`(≈24.7 Ω, Fig. 8b)보다 작다 — 압력 추세와 반대다.**
⇒ **셀 간 산포가 압력 효과보다 크다는 뜻이거나 같은 셀이 아니라는 뜻인데, 논문은 둘 다
확인하지 않는다.**

### 9. ⚠ `θ` 는 또 0 — **19/19**

`contact area` **2 회**, `θ`·`percolat*`·`porosit*`·`tortuos*` **0 회**.
접촉 면적이 인과로 불려 나오는 자리는 **하나**다: `[인쇄]` 압력 효과를 "possibly due to
the **increases in the contact areas** of SE particles and SE pellets". **값은 없다.**
⇒ **`R(P)` 는 있고 `θ(P)` 는 없다** — 18호에서 `R(N)` 은 있고 `θ(N)` 이 없던 것과 같은 모양.
**`assb` 19/19 편이 `θ` 를 어떤 상태축 위에서도 주지 않았다.**

### 10. ⚠ 어긋남 16 건 — 형태가 다르다 (지면 내부 정합)

전수는 digest 의 §어긋남 원장. 무거운 것 다섯:
**D10** `Ea` 자기 불일치 45.5 ↔ 40.5 (절 6) ·
**D5** 율결정 단계 지표가 본문 "(ii)" ↔ Fig. 6 의 "Slow"가 **(iii) 위치** ·
**D6** `R₂` vs `d` 의 이상치(절 7) ·
**D9** LGPS\|LPSCl 의 **CV 기울기 ≈114 Ω ↔ Nyquist 총합 183 Ω (1.6 배)** — 다른 두 셀은
5 % 안에서 맞는다 ·
**D3** Table 2 의 특성 주파수 **세 칸의 지수 부호가 틀렸다**(2.4×10⁻⁷ Hz = 48 일에 한 주기;
표 크롭을 직접 확인해 추출 오류가 아님을 확정). ★ 정정하면 **`P1` 의 꼭짓점이 측정 상한
7 MHz 밖**이고, `[도표]` 세 Nyquist 모두 고주파 쪽이 닫히지 않는다 ⇒ **`R₁` 은 외삽값**
((b)는 원호 208 Ω 중 **26 %** 만 측정됐다).

## ★★★★ 2026-09-22 (18호 Fukunishi et al. 2023) — **저자가 남긴 "A 또는 B" 를 저자의 표로 가른 첫 편**

`raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md`
(*J. Power Sources* **564** (2023) 232864, Tokyo Tech + NEDO SOLiD-EV).
**16호가 자기 ref [39] 로 든 유일한 외부 실측 대조군**이고, 큐 축은 **Q2 + 양극 열화**였다.

### 1. ★★★★ 이 카드의 물음이 **지면에 문장으로 인쇄된다 — 그리고 갈리지 않는다**

> `[인쇄]` "R3 drastically increased (6 times larger) during the durability tests.
> These results suggest that **the chemical composition at the interface or the contact area**
> between the NCM523 and electrolyte particles **changed**."

**이 계보에서 처음으로, 실험 논문이 우리 물음의 두 항(계면 화학 ↔ 접촉 면적)을
이름으로 나란히 적는다.** 그리고 **다음 문단으로 간다.**

두 번째 문장은 더 멀리 간다 — **`θ_AM` 의 기구를 서술한다**:

> `[인쇄]` "**if insulative layers completely cover the active material to make the particle
> inactive, such dead particles probably have no contribution to the charge transfer process.
> This could explain the large capacity decrease in the LPSI system.**"

★ **`assb` 계보에서 "덮여서 죽은 활물질이 용량 감소를 설명한다" 를 실측 논문이 말한 첫
문장**이다 ([[composite-cathode-percolation-utilization]] 의 `θ_AM` 이 문장으로 나타난 자리).
⚠ **분율·면적·값은 0.**

### 2. ★★★★ 그런데 **가를 입력이 같은 지면에 있다** — 16호 처방의 첫 성공

[[assb-lampe-contact-product-degeneracy]] 가 16호에서 세운 처방:
**`R_CT·C_dl` 은 면적이 소거된 조합, `C_dl` 단독은 면적에 비례** ⇒ 둘을 같이 보면 갈린다.

| 처방 입력 | 9호 | 16호 | 17호 | **18호** |
|---|---|---|---|---|
| `R_CT` · `C`/`Q` · `p` | 적합 / 없다 | Table 2 / Table 2 | 0 / 0 | ✅ **Table S1 + Fig. 5** |
| 면적을 바꾼 조작 | 없다 | 압력 2 점 | 없다 | ✅ **입자 크기 2 점 + 노화 전후** |
| 판정 | 곱을 적합했다 | 한쪽 끝을 골랐다 | 곱을 만들지 않았다 | ★ **우리가 곱을 만들었다** |

`[재현]` **열화 축** (Fig. 5 의 로그 막대 판독, `C ≡ τ/R`, 상대오차 ≈±18 %):

| 계 · 항 | `R` 비 | `τ` 비 | **`C` 비** | 순수 면적 예측 | 순수 동역학 예측 | 판정 |
|---|---:|---:|---:|---:|---:|---|
| **LPSI · R3** | 6.5 | 2.4 | **0.37 ± 0.07** | 0.15 | 1.00 | **둘 다** — 유효 면적 ≈2.7 배 감소 + 고유 `R_ct` ≈2.4 배 증가 |
| **LPSCl · R3** | 7.4 | 7.9 | **1.07 ± 0.19** | 0.13 | 1.00 | ★ **면적 손실 없음 — 전부 고유 동역학** |

★★★★ **그리고 이 분해가 같은 논문의 두 번째 관측과 독립으로 일치한다**: `[인쇄]`
**LPSI 에만** 2차 입자를 두르는 **O·P 퇴적층(2 µm)**이 생겼고 LPSCl 에는 `[인쇄]`
"not apparent" 다. **덮으면 면적이 준다** ⇒ LPSI 0.37 ✔ · LPSCl 1.07 ✔.
⇒ **저자의 "or" 가 갈린다: LPSCl 은 화학, LPSI 는 둘 다.**

⚠⚠ **단서 넷**: (ㄱ) `R`·`τ` 가 **로그 막대 판독값**(수치 표 없음) · (ㄴ) **노화 후 `p` 미공개**
⇒ `p` 가 함께 변하면 `τ/R` 는 유효용량이 아니다 · (ㄷ) `C_dl ∝ 면적` 은 **가정**이고
**신품 축의 검사 A 가 그 가정을 흔든다**(아래 3) · (ㄹ) **조건당 셀 1 개**.
⇒ **이것을 측정값으로 쓰지 않는다.** 주장은 **"같은 지면의 두 열을 곱하면 'or' 가
갈린다"** 까지다.

### 3. ⚠⚠ 검사 A(신품, 입자 크기 축) — **면적 설명이 자기 용량 데이터의 지지를 못 받는다**

논문의 논증: `R3` 비 0.5 = 접촉 면적 비 2.0–2.4 의 역수 ⇒ `R3` 는 계면 저항이고
`[인쇄]` "**uniform physical contact**" 다. **면적이 유일한 차이라면 `C_dl` 도 2.0–2.4 배여야
한다.** `[재현]` (`C_eff = Q^{1/p} R^{(1-p)/p}`):

| T | `R3(11.2)/R3(5.0)` | **`C_eff(5.0)/C_eff(11.2)`** | `p` 가 같나 |
|---|---:|---:|---|
| 283 K | 1.88 | **2.26** | ❌ 0.57 ↔ 0.76 |
| **293 K** | 2.10 | **0.68** | ✅ |
| **303 K** | 2.05 | **1.10** | ✅ |
| 면적 설명의 예측 | 2.0–2.4 | **2.0–2.4** | |

⇒ **`p` 가 같은 두 온도에서 2–3 배 어긋난다.** 맞는 유일한 온도(283 K)는 **`p` 가 달라
두 `Q` 의 차원이 애초에 다른** 온도다.
⚠ **반증이라고 적지 않는 이유**: `[재현]` **같은 계면의 `C_eff` 가 283/293/303 K 에서
5.82 / 1.32 / 1.49 µF 로 4.4 배 움직인다** — 이중층 용량이 20 K 에 4 배 변하는 물리는
없으므로 **`Q` 자체가 잘 안 정해지는 파라미터**다. 그리고 **Table S1 에서 ± 가 빠진 유일한
열이 `CPE2-C` 와 `τ3`** 다 — **우리 검사가 쓰는 바로 그 값.**

### 4. ★★★★ 17호가 연 오염 경로가 **18호에서는 설계상 닫혀 있다**

17호는 **2전극 완전지 전압 컷오프** 때문에 `E_CE` 상승이 양극 용량을 깎아 `LAM_PE` 를
흉내 내는 것을 보였다. **18호는 컷오프를 작업전극 전위에 건다**:
`[인쇄]` "The **cutoff potential of the working electrode** was set at 0.85–2.65 V".
게다가 `[도표]` Fig. 1(b)(d) 가 **상대극이 실제로 전 구간 평탄(≈0.60 V)** 임을 보인다.
⇒ `[인쇄]` "**the amount of effective active material decreased only in the LPSI system**" 은
**17호의 오염원이 제거된 상태의 진술**이고, **이 계보에서 양극 활물질 손실을 상대극 오염
없이 말한 첫 문장**이다. ⚠ **값이 없다** — 그래서 채움표에서 반 칸이다.

### 5. ★★★ Q5 — 17호와 **모순이 아니라 반대편 끝**, 그리고 경계 조건의 윤곽

`[재현]` 18호의 Li-In 상대극: **`x_Li` 37.7 → 40.0 at%**(In+LiIn 2상역 한복판),
**Li 재고 / 이동 전하 = 9.5 배**, **0.1 C = 0.054 mA cm⁻²**(17호 0.1 C 의 **1/5**,
17호 CA 의 **1/300**). ⇒ **17호가 본 고갈(+0.7 V)이 일어날 수 없는 설계**다.
★★ 두 편을 겹치면 [[assb-li-in-reference-potential-window]] 에 **경계 조건 셋**이 생긴다:
**(ㄱ) 조성이 2상역 안 · (ㄴ) Li 재고가 이동 전하의 한 자릿수 이상 · (ㄷ) 전류밀도
≲0.1 mA cm⁻²** 일 때 평탄하다. ⚠ **셋 중 무엇이 지배적인지 가른 실험은 0 편.**
⚠ 그리고 **가정은 사라지지 않고 옮겨갔다** — `[인쇄]` "**Assuming** that the potential of
the R-LTO reference electrode is **1.55 V**", 자기 셀 검증 0, 안정성 근거가 **K–K 잔차**(범주 오류).

### 6. ★★★★ 16호와의 3전극 배정 대질 — **절반만 재현되고, 어긋나는 절반이 더 중요하다**

16호 결론 2: `[인쇄]` "고·중주파 = 주로 양극, 저주파 = 주로 음극".

1. **고주파(≈1 MHz) = 양극–집전체 전자 접촉**: **같다.** ★ 그리고 18호 쪽에 **대칭셀
   독립 근거**가 있다(16호는 문헌 인용이었다) ⇒ **이 칸은 두 편이 서로를 보강한다.**
2. **중주파 = 양극 전하이동**: **같다** (16호 `[도표]` ≈30–50 Hz ↔ 18호 `[인쇄]` ≈1 kHz —
   1.5 자릿수 차이지만 배정은 같다).
3. ★★★★ **저주파는 다르다 — 그리고 16호가 그 사실을 알고 있다.** 16호는 `[인쇄]`
   "Fukunishi 는 **저주파 반원을 하나 더** 봤고 그것을 **2차 입자의 전하이동**으로 돌렸다.
   이 논문은 **단결정**이라 그 반원이 없다" 고 적는다. 18호를 읽으니 맞다 — `R4` 는
   **2차 입자 안쪽**이고 **단결정에는 있을 수 없다**. 그리고 `[인쇄]` 18호 자신이
   "The existence of R4 is **apparent when the three-electrode cell is applied to separate
   the Li-In component**" 라고 적는다.
4. **Warburg(< 1 Hz)도 양극이다** — 18호에서 가장 크게 자라는 성분(`[도표]` −Z″ 660 Ω)
   이고 **주파수만으로는 음극과 구별되지 않는다**. ⚠ **`Wo` 값은 지면에 없다.**

★★★★ `[해석]` **"분해의 비유일성" 계보에 층이 하나 더 붙는다**:
**10호** 화학이 바꾼다(In-Li ↔ Li 금속 귀속이 반대) → **11호** 상태·배선·조작이 흔든다 →
**16호** 전극별 DRT 의 합이 완전지가 아니다 → **18호 ★ 같은 화학에서도 양극의
미세구조(단결정 ↔ 다결정)가 "저주파 = 음극" 규칙을 깬다.**
⇒ **주파수 → 전극 규칙은 화학뿐 아니라 미세구조의 함수다.** ★ 이것은 **두 편이 서로를
인용하며 동의하는 내용**이라 `[해석]` 이 아니라 **문헌이 이미 말한 것**이다 —
다만 **두 편 다 "규칙이 없다" 로 일반화하지는 않는다.**

### 7. ★★★ DRT — **λ 가 봉우리 개수를 정하는 사슬이 지면에 그대로 있다**

`[인쇄]` 적합 절차: "First, **the time constants obtained from the DRT analysis were fixed**
and the other parameters were refined." ⇒ **λ → 봉우리 개수 → 회로 차수 → `R3`/`R4` 값.**
그리고 `[인쇄]` "the independent components of R2 to R4 are **confirmed** by using
**λ = 8.5 × 10⁻⁴**" · "by applying **adequate** regularization parameters
(LPSI: **λ = 6.0 × 10⁻²**, LPSCl: **λ = 8.5 × 10⁻⁴**)".
★★ **두 λ 가 70 배 다르고, 분해된 봉우리 개수도 3 ↔ 4 로 다르다** (SI Fig. S1 ↔ S2).
논문은 그 차이를 **재료 탓**(LPSCl 의 낮은 Young 계수 → void)으로 돌리지만
**λ 를 같게 두고 비교한 그림이 없다** ⇒ **"봉우리가 하나 더 있다" 와 "정규화가 70 배
약하다" 가 이 지면에서 구별되지 않는다.** → [[drt-peak-count-nonidentifiability]].
★ 반면 **C2(K–K/Lin-KK)는 이 계보 최초로 통과**한다(`[인쇄]` Lin-KK tools, KIT).
⚠ 다만 그 잔차를 `[인쇄]` **"기준극의 안정성"** 근거로 쓰는 것은 **범주 오류**이고,
잔차 축이 `[도표]` **무차원 ±0.6 스케일에 0.2–0.4** 까지 간다(0.4 % 라면 정상, 무차원이면
저주파에서 K–K 를 크게 벗어난다 — **어느 쪽이든 기준극 안정성은 따라오지 않는다**).

### 8. ⚠ Q6 — **압력이라는 낱말이 없는 열화 논문**

`pressure`·`stack pressure`·`hysteres*` **본문 0 회**. `MPa` 2 회(**110 MPa** 셀 제작 ·
**150 MPa** 대칭셀). **운전 압력은 값도 장치도 문장도 없다.**
⚠⚠ 그런데 이 편의 두 열화 기구 중 하나가 **`void formation`**(`void` **7 회** — 실측 편
최다)이고, LPSCl 의 추가 반원(`R1′`)도 `[인쇄]` "void formation" 으로 설명된다.
⇒ **압력에 가장 민감한 양을 주인공으로 삼으면서 압력을 통제하지 않은 첫 실측 편.**
→ [[assb-stack-pressure-operating-window]] 의 빈칸이 하나 더 구체화된다.

### 9. ⚠ 교락과 산포 — 이 편의 가장 큰 약점 둘

- **G3 교락**: `[인쇄]` 복합양극 조성이 **LPSI 계 49:43:8.0**, **LPSCl 계 69:26:5.0 wt%** 로
  다르다. 근거는 `[인쇄]` "optimized … **preliminary tests**" 뿐이고 데이터가 없다.
  ⇒ **전해질 비교 전체가 "전해질 종류" 와 "조성" 의 교락**이다 — 이 편의 중심 결론
  (LPSI 만 용량 손실 · void)이 그 위에 있다.
- **D17 산포**: `[재현]` 같은 이름표("LPSI · D50 5.0 µm · SoC 100 %")의 `R3` 가
  **Table S1 외삽 ≈55 Ω · Fig. 2c ≈60 Ω · Fig. 5a ≈79 Ω** 로 **1.45 배** 벌어진다.
  ⇒ **이 편에서 우리가 만들 수 있는 유일한 셀 간 산포 추정 ≈±20 %.**
  **노화 효과(6.5 배)는 그 위에 안전하게 서 있고, 입자 크기 효과(2.0 배)는 여유가 훨씬 적다.**
  논문은 이 세 값을 나란히 놓지 않는다.

## ★★★★ 2026-09-22 (17호 Yanev et al. 2024) — **"겉보기 `LAM_PE` 가 사실은 상대극" 을 한 셀 안에서 전극 분해로 실증한 첫 편**

`raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`.
단결정 NCM811 ‖ Li₆PS₅Cl ‖ **Li-In(제조법 3 종 × 조성 스윕)**, 운전 **50 MPa**,
**3전극(Li 금속 도금 Cu 선 RE)**, 0.1 C 및 CA(초기 ≈16 mA cm⁻²), **셀 12 개 · 조건당
n = 1 · 최대 5 사이클**. ⚠ **열화가 없는 편이다**(`LAM`·`LLI`·`SOH`·`aging` 전수 0 회).
그래서 이 카드에 주는 것은 **열화 라벨이 아니라 "라벨을 읽는 자(기준극)가 얼마나
흔들리는가" 의 1차 측정**이다.

### 1. ★★★★ 이 카드의 물음이 **한 셀 안에서, 전극 분해로** 실증된다

같은 두 셀(foil 40 at% ↔ 복합 40 at% + 40 % SE), 같은 양극, 같은 프로토콜:

| 2전극이 보는 것 | 3전극이 말하는 것 |
|---|---|
| **0.1 C 방전 용량이 6.6 % 작다** (`[도표]` 198 → 185 mAh g⁻¹), **곡선의 끝이 잘렸다** | `[재현]` **양극 임피던스가 동일**(≈31 ↔ ≈32.5 Ω, 5 % 차). `[도표]` `E_CE` 가 방전 끝에 0.62 → **≈1.0 V** 로 올라 `E_cell` 하한 2.38 V 에 조기 도달 ⇒ **양극이 3.0 V 대신 `[재현]` ≈3.4 V 에서 멈춘다** |
| **충전 용량이 40 mAh g⁻¹ 작다** (foil 50 at%) | `[인쇄]` 과리튬화(Li₅In₄·Li₃In₂)로 기준이 **−0.2 V** ⇒ `[인쇄]` **컷오프가 4.3 대신 4.1 V** |

★★★★ `[해석]` **"끝이 잘린 곡선" 은 `LAM_PE` 의 서명이고 "통째로 밀린 곡선" 은 `LLI` 의
서명인데, 둘 다 상대극 하나로 만들어진다.** 그리고 **저율일수록 작아 보일 뿐 사라지지
않는다** — `[재현]` 0.1 C **6.6 %** ↔ CA(초기 ≈5.7 C) **≈35 %**.
⇒ **우리 RPT 가 저율이라는 사실은 이 오독을 줄이지만 지우지 못한다.**

★ **이 계보의 Evidence For 에 붙는 형태가 새롭다**: 4·5·6·7호의 반례는 `LLI`·dead Li·
`θ` 쪽이었다. **17호는 "상대극 기준 전위 → 겉보기 `LAM_PE`" 경로를 닫아 보인 첫 편이다.**

### 2. ★★★★ Q5 — 평탄 전위의 실제 폭 (전용 페이지를 만들었다)

[[assb-li-in-reference-potential-window]]. 요지:

- **① 열역학 평탄 폭 = ±10 mV 안** — 그리고 `[재현]` **그 ±10 mV 는 CE–RE 분리막 옴
  강하(≈9.1 mV)와 구별되지 않는다** ⇒ **이 실험은 그보다 좁게 재지 못했다.**
  (닻의 "ASSB 음극은 평탄" 전제는 **이 조건에서는 성립한다** — Li 금속 기준극으로
  확인된 첫 사례다.)
- **② Li-rich 이탈 = `[인쇄]` −0.2 V** (충전 중, 전극 **전체** 조성)
- **③ In-rich 국소 고갈 = `[인쇄]` +0.68 … +0.78 V** (방전 중, **계면**)
- **전체 폭 0.42 → 1.40 V ≈ 0.98 V**, 양 끝이 모두 "Li-In 음극" 이라 불린 셀에서 나온다.

★★★ **우리가 한 옴 분리** `[재현]` (논문이 하지 않은 연결 — CE/RE 고주파 절편을
Fig. 5 에서 읽어 `E_CE` 편차에서 뺀다; `[도표]` foil ≈28.7 Ω, A = 1.131 cm²):

| 구간 | 전류 | `I·R(CE–RE)` | 관측 `ΔE_CE` | **옴 몫** |
|---|---:|---:|---:|---:|
| 0.1 C | 0.317 mA | 9.1 mV | `[인쇄]` ±10 mV | **≈100 %** |
| CA 초기 | ≈18 mA | 0.52 V | `[인쇄]` +0.68 V | **≈76 %** |
| **CA 정상** | **≤0.063 mA** | **≈1.8 mV** | `[인쇄]` **+0.73 V** | **≈0.2 %** |

⇒ ★★★★ **전류가 종료 기준(0.02 C)까지 떨어진 뒤에도 foil 의 `E_CE` 가 ≈1.35 V 에
6 h 이상 머문다. 옴이 아니다.** ⚠ "평형 전위" 라고 못 박으려면 **CA 후 이완 곡선**이
필요한데 논문은 셀 안에 RE 를 두고도 **재지 않았다**(digest G2).

★★★★ **대표 숫자**: **같은 프로토콜 · 전류 ≈0 · 같은 공칭 조성(40 at% Li) 의 두
Li-In 음극이 `E_CE` = 0.61 V ↔ 1.35 V, ≈0.74 V 갈린다. 차이는 제조법뿐이다.**

### 3. ★★★ 3항 분해에 **네 번째 항**이 필요하다

[[assb-apparent-capacity-decomposition]] 의 형태가 `Q_apparent = θ_AM · Q_material · η(i)`
였다. 기준 전위 이동은 **셋 중 어느 것도 아니다**:

```
Q_apparent = θ_AM · Q_material( E_cut^eff ) · η(i)
             E_cut^eff = E_cell,min + E_CE( i, x_Li, 제조법 )
```

★ **그래서 율 스윕 분리 시험이 이것을 지우지 못한다.** `i → 0` 이면 `η → 1` 이지만
기준 전위 이동은 **`η` 가 아니라 축의 원점**이다 — 17호에서 `i → 0` 극한(CA 종료 기준)
에서도 `ΔE_CE` 가 **+0.73 V** 로 남는다.

### 4. ★★ 쿨롱 효율을 `LLI` 대리로 쓰는 통로가 오염된다

②(충전 중 −0.2 V)와 ③(방전 중 +0.4–0.7 V)은 **충전 용량과 방전 용량을 서로 다른
이유로** 줄인다 ⇒ **그 비(CE)는 두 이동의 차를 포함한다.**
[[anode-free-li-inventory-accounting]] 에서 6호(Lee 2020)의 "CE 로 `LLI` 를 센다" 가
10 배 어긋났던 자리에, Li-In 셀에서는 **기준 전위라는 오염원이 하나 더** 붙는다.
⚠ 그리고 이 편의 CE 표(Table S1)는 그 자체로 못 쓴다 — 아래 6.

### 5. ★★ 곱 축퇴 검사 (16호 처방의 첫 적용) — **적용 불가, 그리고 그 이유가 정보다**

16호 처방은 "`R_CT·C_dl`(면적 소거)과 `C_dl`(면적 비례)을 같이 보면 `θ` 와 `j₀` 가
갈린다" 였다. **17호에는 입력이 없다** — `R_CT`·`C_dl`·`CPE`·등가회로 **전수 0 회**,
`[인쇄]` "modelling of the impedance spectra are **beyond the scope of this study**".

세 편의 실패 양식이 전부 다르다: **9호 = 곱을 적합했다** · **16호 = 곱 위에 서서 한쪽
끝을 골랐다(θ≡1)** · **17호 = 곱을 만들지 않았다**.
`[해석]` **역설적으로 17호가 가장 안전하다** — 배정하지 않았으므로 잘못 배정할 수 없다.
대신 **정량이 0 이라 가져갈 숫자도 없다.**

★★ **그래도 이 편에 곱 축퇴가 있다 — 다른 자리에서, 문장으로.**
SE 분말을 넣는 조작 **하나**가 (i) LiIn↔SE **접촉 면적**과 (ii) 음극 **유효 이온전도도**를
동시에 올리고, 논문은 같은 문단에서 두 이름을 번갈아 쓴다
(`[인쇄]` "high effective **contact area**" ↔ `[인쇄]` "confirms that the **effective
ionic conductivity** of the Li-In anode plays an important role"). **둘을 따로 움직인
실험이 없다.**
★★★ 그리고 그 배정이 숫자로도 안 받쳐진다 `[재현]`: 2전극 총 임피던스가 SE
**20 % ≈36 Ω → 40 % ≈27 Ω (Δ ≈9 Ω)** 인데, `[도표]` Fig. 5b 에서 **40 % SE 복합 음극의
임피던스 전체가 ≈6 Ω** 이다 ⇒ **Δ 9 Ω 을 음극에 다 줄 수 없고, 3전극은 40 % 쪽만 쟀다.**
⚠ **단서**: 이 축퇴는 **주 결론을 흔들지 않는다** — 주 결론은 면적/전도도 배정과
무관하게 **전압계 판독**에서 나온다. 흔들리는 것은 "왜 복합이 더 좋은가" 의 기구 설명뿐.

### 6. ⚠⚠ Table S1 의 "추세" 는 산포 대용의 1/4.4 `[재현]`

- foil 45 → 47 → 49 at% CE = **85.3 / 85.0 / 84.8 %** ⇒ 전 구간 변화 **0.5 %p**
- **같은 Li 함량(40 at%)** 의 복합 두 셀 = **82.7 ↔ 84.9 %** ⇒ **2.2 %p**
  (논문 스스로 이 둘의 율 성능 차이를 `[인쇄]` "**slight**" 라고 부른다)

⇒ **가장 가까운 산포 대용이 "추세" 의 4.4 배다.** 반복이 0 이라 **0.5 %p 에 대조할
오차 바닥이 논문 안에 없다.** 그 위에 `[인쇄]` "increased **SE degradation** at the
interface of Li rich anodes" 라는 **기구 주장**이 얹히는데 독립 관측은 0(XPS·XRD 전수 0).
`[해석]` **"Li 가 많을수록 SE 분해가 는다" 는 이 데이터로 주장될 수 없다.**

### 7. ★★★ 문헌 쪽에서 온 두 번째 "인쇄된 요구"

> `[인쇄]` "**the deconvolution of half-cell impedance spectra** e.g., when
> characterizing cathodic charge transfer phenomena, **could be severely complicated
> by overlapping anode impedance.**"
> `[인쇄]` "prevent the possibility of **misinterpretation of anodic effects as
> cathodic effects** in typical half cells."
> `[인쇄]` "**Insufficient reproducibility, which is hardly reported in ASSB half-cell
> studies, at moderate C-rates can be easily explained by anode dominated data.**"

★ 8호(Li 2026)가 `[인쇄]` "distinguishing **contact loss** from ordinary
electrochemical aging" 를 **요구**로 적은 데 이은 **두 번째 인쇄 요구**이고,
**이쪽은 1차 측정을 동반한다.** 그리고 첫 인용은
[[assb-lampe-contact-product-degeneracy]] 와 [[drt-peak-count-nonidentifiability]] 의
배정 문제에 **"음극 오염" 이라는 항을 하나 더 붙인다** — 16호가 `j₀·ε_CAM/r_CAM` 를
양극 것으로 읽을 때, 그 스펙트럼에 음극이 얼마나 섞였는지는 **16호도 우리도 모른다**.

### 8. ★★ 16호 ↔ 17호 대질 — 같은 "In 박 음극" 인데 반대다 (`[해석]`, 미검증)

16호의 음극은 **순수 In 박**이고 Li 가 **분리막 쪽에서 전기화학적으로** 들어온다 ⇒
**LiIn 이 필요한 자리에 생긴다.** 17호의 foil 음극은 Li 박을 **집전체 쪽에서 기계적으로**
누른 것이다 ⇒ `[인쇄]` "most of the generated Li-In phases remain embedded on the
**current collector side** … and do not reach the separator side."
⇒ 16호가 `x_Li` **0.05–0.28**(17호가 치명적이라 한 것보다 훨씬 Li-poor)인데도 음극
임피던스가 `[인쇄]` **4–9 Ω cm²** 로 작은 것이 설명된다
(17호 foil 은 `[재현]` **≥66 Ω cm², 100 mHz 에서 미폐**).
⚠⚠ **압력이 2–8 배 다르고**(50 ↔ 97/389 MPa) **SE·조성·전류·SOC 가 전부 다르다.**
**두 편을 가로지르는 가설이지 어느 편의 결론도 아니다.** 검증 실험은 17호 자신이
인용한다 — `[인쇄]` Sedlmeier(ref 21)가 **Li 쪽을 분리막으로 돌려** 보았고
**저장고는 커졌지만 SE 계면 안정성이 나빠졌다**.

### 9. ⚠ Q6 — 압력은 **한 점**이고, 유일한 기여가 부정적이다

운전 **50 MPa** 한 점, 제작 500 MPa(3E 분리막만 375). **스윕 0 · 이력 0(`hysteres*`
0 회) · 계측 0 · 압력→용량 0 · `E_CE(P)` 0.**
★ 그리고 Wang et al.(ref 28)이 `[인쇄]` **14.3 at% Li 가 최적**이라고 정반대를 주장하는데,
17호는 그 불일치를 `[인쇄]` "considerably higher rates and **lower stack and assembly
pressure**" 로 넘기면서 **상대의 압력값도 자기 스윕도 대지 않는다.**
`[해석]` **측정 없는 압력 귀속**이고, `assb` 계보에서 **압력이 설명 변수로 쓰이면서
데이터가 0 인 첫 사례**다.

## ★★★ 2026-09-22 (16호 Ramanayagam et al. 2026) — **접촉 면적의 자리를 만들고 값을 1 로 못 박는 첫 편**

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
NMC83|6|11(단결정) ‖ Li₅.₃PS₄.₃ClBr₀.₇ ‖ **In/InLi**, 제작·운전 **389 MPa** 또는 운전 **97 MPa**,
양극 두께 **26–219 µm 5 점**, **리튬화 Au/W μ-RE 3전극**, **SOC50 · 2 번째 사이클 · 셀 12 개 · n = 1**.
⚠ **열화가 없는 편이다** (`degrad*`·`aging`·`LAM`·`LLI`·`SOH` 전수 0 회). 그래서 이 카드에
주는 것은 **열화 라벨이 아니라 역문제의 구조**다.

1. ★★★ **식 하나가 이 카드의 물음을 그대로 담는다.** `[인쇄]` 식 (4):
   "**The area of the CAM particles in contact with the SE** normalized to the cathode volume"
   = `a_V = 3·ε_CAM / r_CAM`. **이름은 "접촉 면적" 인데 계산은 완전구 기하 면적이다** —
   접촉 분율 인자가 **없다**. 그리고 식 (5) `R_CT = RT/(F·j₀)` 와 얇은 전극 극한
   `R_semicircle = R_CT/(a_V·d)` 를 합치면 `[해석]`:
   ```
   측정량이 보는 것 = R·T·r_CAM / ( 3·F · j₀ · ε_CAM · d )   ⇒  식별되는 것은  j₀ · ε_CAM / r_CAM  한 조합
   ```
   **9호(Huo 2025)의 `A_eff·ε_p/R_s` 와 같은 자리**다. 다른 점은 9호가 **모델 논문**이었고
   16호는 **실측 논문**이며, **여기서는 저자가 실제로 한쪽 끝을 골라 잡는다** —
   `ε_CAM`·`r_CAM` 고정, 압력 차이 전부를 **`j₀` 0.74 → 1.33 A m⁻²** 로.
2. ★★★ **그리고 같은 Table 2 가 반대 배정을 품고 있다.** 이중층 CPE 계수
   `Q_DL` **0.18 → 0.54 (3.0 배)** 는 **계면 면적에 비례하는 양**이다. 접촉 분율 `θ` 를 넣으면
   `R_CT^meas = R_CT^true/θ`, `C^meas = θ·C^true` 이므로:

   | 배정 | `θ(389)/θ(97)` | `j₀^true` 비 | 논문의 **말**과 |
   |---|---:|---:|---|
   | 논문 (`θ ≡ 1`) | 1.0 | **1.80 증가** | 수치 결론 |
   | `Q_DL` 을 면적으로 읽음 | **3.0** | `[재현]` **0.60 감소** | `[인쇄]` "pressure improves the **interfacial contacts** … considerably" 와 정합 |

   `[해석]` **같은 데이터가 `j₀` 의 증가와 감소를 둘 다 허용한다.** 그리고 논문의 **문장**은
   둘째 배정을 말하고 **숫자**는 첫째 배정을 쓴다. ⚠ `β` 가 0.89 ↔ 0.81 로 달라 두 `Q` 는
   엄밀히 차원이 다르다 — `[재현]` Brug 류 유효용량으로 고치면 비가 **3.0 → ≈5.6** 으로
   **커진다**(결론 방향은 유지). 자세히는 [[assb-lampe-contact-product-degeneracy]].
3. ★★ **음극에는 면적 서사, 양극에는 동역학 서사 — 같은 논문 안에서.**
   `[도표]` Figure 5 모식도는 압력이 바꾸는 것을 **"interphase 를 통하는 칸의 개수"**
   (저압 통함 3/8 ↔ 고압 5/8)로 **그림으로 명시**한다. 그런데 §TLM 은 양극에서
   바로 그 **유효 면적을 고정**한다. `[해석]` **전극이 바뀌면 같은 현상의 이름이 바뀐다.**
4. ★★ **Q5 가 네 겹으로 채워진다** (위 표 16호 행). 요점만: 기준극이 **Li–In 이 아니라**
   리튬화 Au/W 이고 · **그 안정성을 인용으로 가정**하며 · `[도표]` **리튬화 곡선에 평탄부가 없고**
   (2.5 µAh 에 560 mV 표류) · `[도표]` **두 셀의 In–Li 평탄 전위가 0.58 ↔ 0.47 V 로 0.11 V
   어긋난 채** 같은 "vs Li/Li⁺" 축에 그려진다. `[재현]` 0.1 C 음극 과전압은 ≈5 mV 라 설명이 안 된다.
   ★ `[해석]` **완전지 OCV 를 "밀린 양극 곡선" 으로 읽는 계획에서, 밀린 양의 셀 간 재현성이
   0.1 V 자릿수라면 그것은 `LLI` 로 오독될 크기다.** 4호가 오프셋 0.6 V 를 고정 가정했던
   경고가 **기준극을 실제로 설치한 편에서도 사라지지 않는다.**
5. ★★★ **평탄 OCP 가 숨기는 양을 처음으로 숫자로 본다.** `[재현]` SI Table 의 `x_Li`
   (0.05–0.28)는 **In + InLi 2상 공존역 안**이고 `[도표]` Fig. S3 에서 음극 전위는 **완전 평탄**
   이다. **바로 그 구간에서** `[도표]` 음극 DRT 봉우리가 **18.6 → 1.2 (≈15 배)** 움직인다
   (97 MPa; 389 MPa 에서는 1.6 → 0.30, **5 배**). `[해석]` **닻의 출발 전제("ASSB 음극은 평탄이라
   완전지 OCV 는 양극 곡선 하나")가 열역학 축에서는 맞고 동역학 축에서는 완전히 틀린다.**
   OCV 적합이 `LAM_PE` 와 접촉 손실을 가르지 못하는 것과 **별개로**, 음극이 평탄하다는 사실이
   **음극이 조용하다는 뜻은 아니다.**
6. ⚠ **압력 이력에는 답하지 않는다 — 그리고 그 물음이 왜 중요한지를 보여 준다.**
   두 압력이 **다른 셀**이고, **둘 다 389 MPa 제작을 거친다.** ⇒ `[해석]` **97 MPa 데이터는
   전부 하강 분기**인데 논문은 두 압력을 **대칭적인 두 조건**처럼 비교한다 (`hysteres*` 0 회).
   5호(Doux)의 `θ(P)` 경로 의존이 참이면 이 비교의 해석이 달라진다.
7. **Q4 의 아홉 번째 성질 — "밟고 지나갔다".** 안 쟀다(1–7호) → 이름만(8호) → 지문이 자기 표
   안에(9호) → 분야가 명제로(10호) → 재료만(11호) → 0(12·13호) → 역문제가 없어 자리가 없음
   (14호) → 추정기가 없어 대상이 없음(15호) → **16호: 역문제를 풀고 축퇴한 조합 위에 서 있으면서
   `identifiab*`·`uncertaint*`·`error bar` 가 전수 0.** **여전히 0/16.**

★ **2026-09-22 (15호 Rahman & Lu 2024) — 새 칸 0. 이 편이 준 것은 근거가 아니라
**계보의 바닥 눈금**과, 이 위키 최초의 **원전 대조 실측** 둘이다.**

- ★★★ **1호(Bielefeld 2019)가 야생에서 어떻게 인용되는지를 처음 봤다 — 그리고 어긋난다.**
  15호 ref **[5]** 가 우리 1호이고, 인용된 **유일한 자리**가 `[인쇄]` "They mainly address
  key challenges such as **load balancing, state-of-charge estimation, and overall battery
  health monitoring [5, 6]**" 다. 우리 1호 digest 는 그 논문에 `[인쇄]` **"셀 실험 0,
  사이클링·전압·용량이 없다"** · `voltage` **1 회(그마저 참고문헌 제목)** · **모델에 음극이
  없다**고 전수 계수로 기록해 뒀다. **부하 균등화·SOC 추정·건전성 모니터링은 그 논문에
  없다.** ⚠ 서지도 틀렸다 — **연도 2018 (원전 2019)**, 저자 "W. Dominik A"(= Dominik A.
  **Weber**).
  `[해석]` **단순 번호 실수로 보기 어렵다** — 같은 저자의 **다른 논문 [28]**(2020 바인더
  편)이 §4.1 에 따로 있고 거기서는 내용이 대체로 맞게 요약된다. 서론의 `[5, 6]` 은
  "SSB 문헌임" 만으로 고른 **장식 인용**이다.
  ★ **이것이 우리에게 주는 것**: 1호 digest §12.4 에서 `Q_apparent = θ_AM · Q_material`
  을 **우리 해석**이라고 못 박고 "논문은 용량도 전압도 주지 않는다" 고 적었던 경고가
  **과하지 않았다는 증거**다. 바깥에서는 그 다리 없이 BMS 문장에 직결된다.
- ★★ **12호(Kouhestani 2022)와의 대조 — 어긋나지 않지만 껍데기만 간다.**
  15호 ref **[21]** 이 우리 12호이고, 쓰인 자리가 **FNN/RNN 의 교과서적 정의 한 문장**이다
  (우리 12호 digest 가 그 수준을 채록하지 않아 **어긋남은 미확인·정합 추정**).
  ★ 문제는 **12호의 자기 결론을 한 글자도 옮기지 않는다**는 것 — 우리가 Table 1 을 한 줄씩
  대조해 적은 `[재현]` **"SSB 실측 열화 데이터로 SOH/RUL 을 추정한 항목 0 / 28"** 과
  `[인쇄]` "most PHM techniques are based on **simulation** results and not experimental".
  `[해석]` **12호(2022)가 감사로 적어 둔 공백을 15호(2024)가 12호를 인용하면서 재생산한다.**
  12호 항목이 "2022 → 2026 사이 PHM 문헌은 identifiability 라는 **이름**을 얻었고 여전히
  재지 않았다" 로 끝났는데, **15호는 그 사이(2024)에서 이름조차 못 얻은 표본**이다
  (`identifiab*` **0 회**).
- ★★ **분류 체계 세 번째 표본 — "미도입" 유형.** 12호 = `LAM ⊃ 접촉 손실`(**정의로 병합**) ·
  13호 = **미배정** · **15호 = 어휘 미도입**(`contact` **0 회**). 세 편 다 **종설/전망/회의록**
  이고, **1차 측정이 있는 편(4·5·6·7·9·11·14호)은 전부 어떤 형태로든 접촉 축을 갖는다.**
  `[해석]` **접촉 손실이라는 구분은 실험 층위에서 강제되고 종합 층위에서 소실된다** —
  우리가 폭을 재서 공급하려는 대상이 **종합 층위**라는 뜻이다. ⚠ 표본 3 개, 다음 종설에서 다시 본다.
- ⚠ **Q4 의 성질 — 여덟 번째, 그리고 가장 얕다.** 안 쟀다(1–7호) → 이름만(8호) → 지문이
  자기 표 안에(9호) → 분야가 비유일성을 명제로(10호) → 재료만 인쇄(11호) → 0(12·13호) →
  역문제가 없어 조건수 자리가 없음(14호) → **15호: 추정기 자체가 없어 역문제를 말할
  대상이 없다.** 그런데 `accuracy` **7 회** : 정확도 수치 **0** : 불확실성 표기 **0**.
  **여전히 0/15.**
- ★ **후속 후보 1 순위 신설**: **Asheri et al., *Comput. Mater. Sci.* 226, 112186 (2023)**
  (이 편 ref [22]) — 이 계보에서 **ML × SSB 계면 손상**이 만나는 첫 좌표이고, **12호가
  감사한 28 슬롯에도 없던 항목**이다. 2 순위 **Bielefeld 2020 *ACS AMI* 12, 12821**
  (ref [28]) — 1호의 직계 속편, 1호 모집단 경고("탄소·바인더 없는 2 성분")의 바인더 축.

★★ **2026-09-22 (14호 Oh et al. 2025) — 새 칸 0, 그러나 이 카드의 물음에 가장 직접적인
실측 하나와 Q4 의 일곱 번째 성질이 들어왔다.**

- ★★★ **접촉 손실(void)이 겉보기 용량에 안 보인다는 실측** — `[인쇄]` void 4.5→9.8 % 셀
  86.0 % ↔ 4.4→5.3 % 셀 84.0 %. 이 카드의 물음이 "OCV 적합이 접촉 손실을 `LAM_PE` 로
  **오독**하는가" 였다면, 이 창(50 사이클, 10–20 MPa)에서는 **오독할 신호 자체가 용량에
  없다** — `θ_AM` 이 `p_c` 위에서 ≈1 로 버티는 1호 그림과 정합. `[해석]` 접촉 손실 → 용량
  사상은 **문턱형**이고, 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 정확히 보고하되 **void 가
  2 배 됐다는 사실을 놓친다** — 그것을 보는 것이 volumetry 다.
- ★★ **Q4 의 성질 — 일곱 번째: 역문제가 없어서 유일성 물음이 사라진 자리.** 8호 이름 →
  9호 지문 → 10호 명제 → 11호 재료 → 12·13호 0 → **14호: 관측이 직접 도함수라 조건수가
  정의될 자리가 없고, 그 대신 "귀속의 유일성"(ΔS 변화 = 비균질? `dE/dP` 감소 = void?)을
  아무도 묻지 않는다.** 여전히 **0/14**.
- ★★ **Q2 의 형태 — 세 번째**: 1–10호 형태학, 11호 조작, **14호 열역학 도함수**. 그리고
  이 편의 ΔS 는 스스로 우리 쌍(접촉 손실 + 계면 저항)을 **합친 신호**라고 정의한다 →
  분리 관측 후보는 **volumetry 쪽**이다 (`[해석]`, 아래 새 제약).
- ✅ **Q6 에 새 층** — 압력이 사이클 변수·개입이 아니라 **관측 변수**(소신호 ΔP = −5 MPa,
  가역). 계보 최초의 `E(P)` 두 구간과 그 **비선형**(2 배).
- ✅ **Q8 에 새 층** — OCV 축 위의 열역학 도함수 ≈28 점 × 3 셀 × 전·후. ⚠ SOC 축 없음.
- ⚠ **13호 후속 4 순위(Oh *AEM* 2025) = 이 편 ref [10], 같은 저자·연구실** → 1 순위로 승격.

★★★★ **2026-09-22 (11호 Yu et al. 2024) — 두 칸이 움직였고, Q4 의 성질이 다섯
번째로 바뀌었다.**

- ✅ **`Q1` 의 10/10 편 0 이 반쯤 깨졌다.** 여전히 **무차원 분율은 없다**(`θ` 0 회).
  그러나 이 계보 최초로 접촉 손실 대리량이 **주파수로 국소화되고 · 시계열이 있고 ·
  조작으로 되돌려진다**. ⚠ 그리고 같은 그림이 **그 대리량이 전극을 가르지 않는다**는
  것도 같이 인쇄한다 (Fig. 8 의 P3 에 Cathode + Anode).
- ✅✅ **`Q6` 의 마지막 빈칸(`압력 → 용량 곡선`)이 채워졌다** — 10/10 편이 못 주던
  것이다. 반쪽 3 점 + 완전지 2 점. ⚠ 다만 **점이 5 개이고 계측 수단이 없다**.
- ★★★ **`Q4` 의 성질 — 다섯 번째 변신**: 안 쟀다(1–7호) → 이름이 로드맵 실패 모드에
  (8호) → 지문이 자기 표 안에(9호) → 방법의 비유일성이 분야의 공식 문장(10호) →
  **11호: 축퇴의 크기를 잴 재료를 SI 에 인쇄해 놓고 본문 효과와 나란히 놓지 않는다.**
  **여전히 "쟀다" 가 아니다 — Q4 는 0/11 이다.** 7호가 `LLI` 뺄셈을 안 한 것과
  **같은 형태**이고, 축이 Q7 이 아니라 Q4 이며 재료가 **SI 에** 있다는 점이 다르다.
- ★★★ **`Q8` 이 이 카드의 출발 전제를 깼다** (위 표 끝 칸). **흑연 음극이면
  5 → 3 파라미터 붕괴가 성립하지 않는다.** 이 카드 §"지금까지 아는 것" 의 붕괴표는
  **Li-In / Li 금속 / 무음극 셀에만** 유효하다.
- ★★ **`Q2` 가 형태를 바꿨다** — 1–10 호에서 "가르는 관측" 은 **형태학**(FIB-SEM ·
  토모 · XRD)이었다. 11호는 **형태학이 0 인데 조작이 넷**이다(반쪽전지 분해 · 입도
  스윕 · 코팅 유무 · 재가압). `[해석]` **분해를 관측이 아니라 설계로 한다** —
  그래서 결론이 **설계가 통제한 것만큼만** 강하다.
- ⚠ **`Q3` 가 후퇴했다.** 9호는 표에 "not disclosed" 를 찍기라도 했는데 **11호는
  파라미터 표가 없다.** `[인쇄]` "The authors do not have permission to share data."

★★★ **10호가 `Q4` 의 0 을 처음으로 깼다 — 그리고 깬 방식을 정확히 적어야 한다.**
**"쟀다" 가 아니다**(측정 0, 10/10 편 그대로). **"축퇴가 일반 현상임을 방법론으로
인쇄했다"** 이다: `[인쇄]` "**no solution to an EIS spectrum is unique**" ·
"**the inclusion of more elements will tend to improve the fit**" ·
"how many time constants … **highly subjective**", 그리고 모델 선택을 **AIC** 라는
통계 문제로 명명한 뒤 `[인쇄]` "**thorough validation against experiment in the
context of ASBs is desirable**" 로 **열린 문제로 등록**한다.
→ **Q4 의 성질이 네 번째로 바뀌었다**: 안 쟀다(1–7호) → 이름이 로드맵 실패 모드에
올랐다(8호) → 지문이 자기 표 안에 있고 다르게 불린다(9호) →
**방법 자체가 비유일하다는 것이 분야의 공식 문장이 됐다(10호).**
⚠ **`Q1` 은 10/10 편이 여전히 0 이다.**
★ **9호가 반 칸을 늘렸다** — **Q6 이 "점·스윕" 에서 "시계열" 로** 바뀐 것과 **Q3 의 새 층위**(`fitted-single-parameter`)다.
★★★ **그리고 Q4 의 성질이 세 번째로 바뀌었다**: 1–7호 "안 쟀다" → 8호 "이름이 로드맵의
실패 모드 목록에 올랐다" → **9호 "지문이 자기 표 안에 있고 다르게 불린다".**
**Q1 과 Q4 의 0 은 9호도 채우지 못했다.** 그러나 9호는 **이 계보에서 처음으로
"열화 모드의 지분을 적합으로 정하는" 논문**이고, 그래서 **처음으로 이 카드의 Q4 가
관망이 아니라 직접 적용된다** — 자세한 것은 [[assb-lampe-contact-product-degeneracy]].
★ **8호도 칸을 늘리지 않았다** (Q1 정량 0 · Q4 이름만 · Q6 재인용 1 점 · Q3 는 다른 층위).
★★★ **대신 세 가지가 바뀌었다**:
① **Q4 의 성질** — 1–7 호 "`identifiab*` 0 회, 아무도 안 쟀다" →
**8호 "로드맵 표의 실패 모드 항목(`Unidentifiable pulse response`)으로 올라갔다"**.
4호가 EIS 축퇴를 인쇄로 인정한 것과 같은 계열이되, 이쪽은 **해야 할 일의 목록**에 있다.
② **Q1 의 성질** — 1–7 호 "일곱 편이 일곱 개의 다른 양을 접촉 손실이라 부른다" →
**8호 "접촉 손실과 보통 노화를 가르는 진단이 필요하다" 가 BMS 요구 사항으로 인쇄됐다.**
**이 카드의 질문이 문헌의 요구 목록에 올라 있다.**
③ **Q6 의 아래 벽** — 실험실 창 전체(2–490 MPa)가 **산업 요구치(<≈1 MPa) 위**에 있다.
⚠⚠ **8호는 Mini Review 다 — 1차 측정이 0 이고 위 수치는 전부 재인용이다.**
근거로 쓰려면 원 논문을 받아야 한다 (Status Log 의 후속 후보표).
★ **7호는 칸을 늘리지 않았다** (Q1·Q4 가 여전히 0, Q8 은 해당 없음, Q6 은 오히려 후퇴).
★★★ **대신 Q7 의 성질이 바뀌었다**: 5호 "수단이 없다" → 6호 "채널은 있고 정량이 0" →
**7호 "수치가 계산 가능하다"** (`[재현]` 0.79 mAh cm⁻² = 39 %). ⚠ **논문이 그 뺄셈을
하지 않는다** — 효율도 비가역분도 인쇄되지 않는다.
★★ 그리고 7호는 **6호를 외부에서 검증한 첫 편**이다 (§아래 Evidence).
★★ **5호가 Q6 을 "점" 에서 "곡선" 으로 바꿨고, Q7 의 4/4 편 0 을 절반 깼다.**
★★★ **6호는 Q6 을 "한 축" 에서 "두 축"(제작 ↔ 운전)으로 쪼갰고, Q7 에 채널 둘
(EELS Li 맵 · XRD Li₉Ag₄)을 더했다 — 정량은 여전히 0 이다.** 그리고 **Q5 를
"무음극이라 해당 없음" 으로 닫는 대신 같은 문제를 새 형태로 연다**(음극 전위가
앞 10–17 % 구간에서 평탄하지 않다). **Q1 과 Q4 는 6호도 채우지 못했다.**

- ✅✅ **Q6 이 두 축이 됐다.** 5호까지 "압력" 은 한 변수였다. 6호는 **제작 압력
  (490 MPa 등방, 비가역)** 과 **운전 압력(2 MPa)** 을 분리하고, **제작 압력이 충분하면
  운전 압력이 할 일이 없다**는 것을 무압 대조로 보인다 → [[assb-stack-pressure-operating-window]].
  ⚠ 동시에 **운전 상한이 훨씬 낮다**: `[인쇄]` **4 MPa 초과에서 단락 확률 증가**
  (5호의 Li 금속 75 MPa 의 **1/19**). ⚠⚠ **그 문장에 데이터가 없다.**
- ✅ **Q7 의 채널이 둘 늘었다 — 정량은 0 이다.** 5호가 "SEI 는 상으로 잡히고 dead Li 는
  수단이 없다" 로 남겼다. 6호는 **EELS Li 맵**(Li 특이 채널, 계보 최초)과
  **XRD 의 Li₉Ag₄**(Li 를 담은 그릇)을 더한다. **dead Li 만 여전히 수단이 없다** —
  그리고 6호는 **"isolated lithium" 을 열화 기구로 지목하고도 재지 않는다.**
  → 자세히는 [[anode-free-li-inventory-accounting]].
- ★★★ **새 축이 하나 열렸다: `LLI` 추정자의 분해능.** 6호 안에서 **20 mAh 셀은
  CE(99.97 %)와 유지율(92.5 %@300 = 99.974 %/cycle)이 맞고, 0.6 Ah 셀은 10 배
  어긋난다**(CE `[도표]` 99.89 % ⇒ 누적 결손 161 mAh g⁻¹ ↔ 실측 손실 16).
  **CE 축의 눈금조차 다르다**(95–101 vs 99.4–100.0). 논문은 두 셀을 **한 번도
  비교하지 않는다.** → **우리 폭 측정기가 바로 걸리는 자리.**
- ⚠ **Q1 은 여섯 편이 여섯 개의 다른 양을 다룬다 — 그리고 6호는 아예 안 잰다.**
  1호 기하 부피분율 · 2호 연결성 · 3호 계면 응력 · 4호 접촉 면적 + void 부피 ·
  5호 전기적 대리량(음극) · **6호 없음(공정으로 대체)**.
- **Q4(유일성)는 `assb` 6/6 편이 여전히 0.**

- ✅ **Q6 이 스윕이 됐다.** 4호는 각 1 점(2 MPa · 300 MPa)이었다. 5호는 **세 개의
  곡선**을 준다 — 그리고 **압력을 로드셀로 실제 계측한 첫 편**이다.
  ★ 가장 큰 수확은 **상한**이다: `[인쇄]` **75 MPa 는 도금 전에 이미 기계적으로
  단락한다.** → **4호의 300 MPa 재가압은 이 상한의 4 배**이고, Li 금속 셀에
  그대로 적용하면 **회복 용량을 읽기 전에 셀이 죽는다.**
  ⚠ 단 **모집단이 다르다** (4호 In 음극 vs 5호 Li 금속) — **상한은 음극 재료의 함수**다.
- ✅ **Q7 이 절반 깨졌다 (4/4 → 5호).** 이 계보 첫 **Li 금속 음극** 논문이고
  형태학을 3D in situ 로 본다. 그런데 **가른 것은 dead Li ↔ SEI Li 가 아니라
  "형태(토모) ↔ 화학(XRD)" 두 채널**이다. **SEI 는 상으로 잡히고 dead Li 는 안
  잡힌다** — Li 금속이 XRD 로 원리적으로 안 보이기 때문이다.
- ⚠ **Q1 은 다섯 편이 다섯 개의 다른 양을 "접촉 손실" 이라 부른다.** 5호의 것은
  **전기적 대리량(Ω)** 이고 **전극이 다르다(음극)**. `θ` 로 변환되지 않는다.
- **Q4(유일성)는 `assb` 5/5 편이 여전히 0.** 5호는 역문제를 **아예 풀지 않는다**
  (등가회로 0) — 4호가 "축퇴를 인쇄로 인정하고 점추정" 이었던 것과도 다른 형태다.
★★ **4호가 한 편에서 세 칸을 깼다: Q2(실험) · Q6(압력) · Q8(실측 전압곡선).**
그리고 Q1 을 **무차원 분율 + 시간축**으로 처음 채웠고, Q5 를 **부분**으로 열었으며,
Q3 에 새 층위(**measured-but-ML-thresholded**)를 추가했다.

- ✅ **Q2 가 깨졌다 (3/3 → 4호).** `assb` 1·2·3 호는 **전부 시뮬레이션**이었고 자기
  실험이 0 이었다. 4호는 **처음부터 끝까지 실험이고 시뮬레이션이 한 줄도 없다.**
  ★ 가장 큰 수확은 **개입**이다 — 50 사이클 후 **300 MPa 재가압**으로 용량이
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** 로 돌아왔다 (`[재현]` **+60.5 %p**).
  **진짜 재료 손실은 눌러도 안 돌아오고, 닿지 않던 활물질은 돌아온다** →
  [[assb-pressure-reapplication-separation-test]].
- ✅ **Q6 이 깨졌다 (3/3 → 4호).** 제작·사이클·개입 **세 역할**로 압력을 쓴다.
  ⚠ 단 **스윕이 없다**(사이클 2 MPa 1 점, 재가압 300 MPa 1 점)이고 압력값이
  **전부 ESI 에만** 있다 — 본문은 초록의 "large external pressure" 가 얼마인지도
  Fig. 1 캡션에서야 밝힌다.
- ✅ **Q8 이 실측으로 닫혔다.** 3호의 OCV 는 **액체 반쪽전지 GITT**(타 논문 입력)였다.
  4호는 **ASSB 실셀의 사이클별 V–Q** 를 준다. ⚠ 단 CC 곡선(≈C/15)이지 OCV 가 아니다
  (`OCV`·`open-circuit` 0 회).
- **Q4(유일성)는 `assb` 4/4 편이 여전히 0.** 1–3 호는 forward 전용이라 **원리적으로**
  못 쟀지만, ★ **4호는 역문제를 풀면서**(EIS 3-RC 등가회로) **축퇴를 인쇄로 인정하고도
  점추정을 보고한다.** → **이 축은 이제 "아무도 안 쟀다" 가 아니라 "재야 한다고
  문헌이 스스로 적어 놓았다" 가 됐다.**
- **Q7 은 4/4 편 0.** (4호는 In 음극이라 dead Li 축이 원래 없다 — 구조적 공백.)
- **Q1 은 네 편이 네 개의 다른 양을 "접촉 손실" 이라 부른다**: 기하 **부피**분율(1호) ·
  연결성(2호, 1호와 동일) · 계면 **인장응력**(3호, 차원 다름) ·
  **접촉 면적분율 + void 부피분율**(4호, 차원은 맞으나 **사상 미정**).
  ★ **4호의 실측이 1호의 곱셈 형태를 6 배로 배반한다** (10.4 % ↔ 60 %p, 아래 Evidence).

## Evidence For / Against

### For — "OCV 만으로는 못 가른다" 쪽 (2026-09-16, Bielefeld 2019)

- **접촉 손실이 `LAM_PE` 와 섞이는 방식이 확정됐다: 곱셈.**
  [[composite-cathode-percolation-utilization]] 의 `θ_AM` 은 재료량을 건드리지 않고
  **용량 축 스케일에 곱해진다** (`Q_apparent = θ_AM · Q_material`, 우리 해석).
  OCV 곡선은 **곱만** 본다 → 위 "모르는 것 1" 의 **형태**가 정해졌다.
- **`A_spec,a` 봉우리가 평탄하고 두께 곡선이 겹친다** — forward map 자체가 이미
  납작하다. [[fitting-degeneracy]] 가 화학 무관하게 재현될 자리.

### For 보강 (2026-09-16, Clausnitzer 2023) — **혼동원이 하나 더 있다**

- **곱셈 축퇴에 항이 하나 더 붙었다.** 같은 논문 안의 반례: `SVF_LCO = 69.4 %`,
  소결 밀도 70 %, 입계 저항 무시 → `[도표]` **CAM 연결성 ≈100 %** 인데 **정규화 용량 ≈0.10**.
  → `Q_apparent = θ_AM · **η(i)** · Q_material` ([[assb-apparent-capacity-decomposition]]).
  OCV 적합이 상대해야 할 것이 **둘이 아니라 셋**이다.
- **동역학 성분의 크기가 처음으로 숫자로 나왔다.** `[도표]` Fig. S5: 재료·기하가 전부
  동일하고 **입계 저항만** 0 → 3.6 Ω cm² 로 바꾸면 방전 용량이
  **1.37 → 0.385 mAh/cm²** — **겉보기 `LAM_PE` 72 %.** 재료 손실은 0 이다.
- **그리고 그 곡선은 아핀 스케일링이 아니다** (시작 전압 −175 mV, 기울기 다름).
  → `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 3 파라미터 창 모형으로는 **못 맞춘다.**

### For 보강 (2026-09-16, Liu 2024) — **문헌이 축퇴를 인쇄로 인정했다**

- ★★ **이 질문의 축퇴가 논문 문장으로 확인된 첫 사례.** `[인쇄]` "the experimental
  analysis of active cathode material loss generally involves the formation of **rock-salt
  phase AND isolated cathode materials induced by intergranular fracture**. Since this
  study does not explicitly consider crack formation, **only qualitative comparisons** are
  made between predictions and experimental characterisations."
  → **실험이 보고하는 "활물질 손실" 은 (진짜 재료 손실) + (기하적 고립 = 접촉 손실)의
  합이고, 그 측정으로는 안 갈라진다.** 우리가 물어 온 것이 그대로 적혀 있다.
  ⚠ 그런데 같은 논문이 **앞 항만 모델링하면서** 뒤 항까지 포함한 실험값과 Fig. 5e 에서
  겹쳐 놓는다 — 체계적으로 과소예측해야 정상인데 겹친다.
- ★ **진짜 `LAM_PE` 의 생성 기구가 처음 들어왔다.** 불균일 Li → 전위(소성전단) →
  격자변형 → 산소공공 형성에너지 하락(`[인쇄]` 10 % 인장에서 1.06 → 0.24 eV) →
  rock-salt. 즉 **`Q_material` 이 줄어드는 물리**. `[도표]` 12 µm 에서 활물질 손실이
  0.25C 0.093 → 5C **0.185**.
- ★ **그리고 그것이 율 의존이다** → 아래 "새 제약" 의 첫 항목.

### ⚠ For 에 붙는 **실측 반례** (2026-09-16, Shi 2020) — **곱셈 형태 자체가 6 배 어긋난다**

- ★★ **접촉 손실 면적 10.4 % ↔ 압력으로 되돌아온 용량 ≈60.5 %p.**
  `[인쇄]` 4호는 50 사이클 시료에서 "the estimated contact loss area is **10.4 % of the
  total cathode surface area**" 를 재고, 같은 논문에서 300 MPa 재가압으로
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** (129 기준 `[재현]` **+60.5 %p**) 를 회복한다.
  곱셈 `Q_apparent = θ_AM · Q_material` 에 면적 분율을 그대로 넣으면 손실이 **10 %**
  여야 한다. **≈6 배 어긋난다.** ⚠ **논문은 두 수를 나란히 놓고 한 번도 비교하지 않는다.**
- `[해석]` 가능한 설명 셋, 논문은 **어느 것도 검증하지 않는다**:
  ① **면적 → 부피 사상이 비선형(문턱)이다** — 4호 자신이 근거를 준다:
  `[인쇄]` 접촉 손실이 입자 **한쪽에 몰리면** "all the Li ions … have a **much larger
  distance to travel**", 균일 분산이면 "diffusion gradients … would **rapidly fade out**".
  ② **라벨과 관측이 다른 셀**이다 — **토모그래피 3 셀의 용량이 한 번도 보고되지 않는다.**
  ③ **회복분이 양극이 아니다** — 아래.
- ★★ **회복의 대부분이 음극이다.** `[도표]` Fig. 1(c) 재가압 회복률:
  **`R_LF`(음극 쪽) ≈65 %** · `R_HF` ≈46 % · **`R_MF`(양극 쪽) ≈23 %** (`[재현]`,
  `R_MF` 는 인쇄값 3283→2755 Ω). 그리고 50 사이클에 `R_LF ≈110 kΩ` 가 전체의 **≈93 %**.
  → **용량 회복률(≈61 %p)과 가장 잘 맞는 것은 양극이 아니라 음극이다.**
  ⚠ 4호의 초록·결론은 **양극 접촉 손실**로 돌린다 — **자기 그림이 다르게 말한다**
  (4호 digest D8). 본문 한 문단만 `[인쇄]` "some **anode delamination** could also exist"
  로 인정하고 만다.
- `[해석]` **우리에게 이것은 나쁜 소식이 아니라 좌표다**: `θ` 를 스칼라 곱셈 인자로
  쓰는 모형은 **실측과 6 배 틀린다.** DEM 이 싸게 주는 것도 **접촉 수·면적**이므로
  **면적 → 이용 가능 용량 사상을 우리가 만들어야 한다.**

### ⚠ For 에 붙는 **두 번째 실측 반례** (2026-09-16, Doux 2020) — **회복의 전극 귀속**

- ★★ **압력 실험은 양극 전용 조작이 아니다 — 양극이 없는 셀에서 증명된다.**
  5호의 Fig. 4c 셀은 **Li | Li₆PS₅Cl | Li 대칭셀**로 **복합양극이 아예 없다.**
  그런데 압력을 1 → 25 MPa 로 올리면 임피던스가 `[인쇄]` **>500 Ω → 32 Ω (>15 배)**
  움직이고, 25 MPa 를 찍고 5 MPa 로 내리면 `[인쇄]` **110 → ≈50 Ω** 로 **되돌아오지
  않는다**(영구 정합).
  → **압력이 되돌리는 접촉의 큰 몫이 음극/전해질 계면에 있다는 것이 독립 논문에서
  확인된다.** 4호의 `R_LF`(음극) 65 % vs `R_MF`(양극) 23 % 회복률과 **같은 방향**이다.
  `[해석]` **`ΔQ_mech` 를 통째로 양극 `θ_AM` 회복으로 읽으면 과대평가다** —
  분리 시험에 **전극 분해 관측**(3전극 또는 대칭셀 짝)이 필요하다.
- ★★ **그리고 처방에 상한이 생겼다.** `[인쇄]` Li 금속 / Li₆PS₅Cl(상대밀도 ≈82 %) /
  75 µA cm⁻² 에서 **75 MPa 는 도금 전에 이미 기계적으로 단락**한다.
  **4호가 쓴 300 MPa 는 그 4 배다.** ⚠ 모집단 차이(In 음극 vs Li 금속)를 붙여야 하지만,
  **연산자가 파괴적일 뿐 아니라 셀을 즉사시킬 수 있다**는 것이 숫자로 들어왔다.
  → [[assb-stack-pressure-operating-window]].
- ★ **율 연산자와 압력 연산자가 직교하지 않는다.** `[도표]` 5호 Fig. S4:
  같은 전류밀도(75 µA cm⁻²)에서 도금/탈리 과전압이 **5 MPa 7.0 mV ↔ 25 MPa 4.5 mV**.
  → **`η = η(i, P)`** 이고, `i→0` 으로 `η` 를 지우는 처방은 **압력을 고정한 채로만**
  성립한다. [[assb-apparent-capacity-decomposition]] 의 3 항 분해가 그만큼 좁아진다.

### ⚠ 세 번째 실측 반례 (2026-09-16, Lee 2020) — **`LLI` 쪽에서도 라벨이 안 닫힌다**

- ★★★ **같은 논문 안에서 `LLI` 의 두 추정자가 10 배 어긋난다.**
  0.6 Ah 무음극 파우치: `[도표]` CE 중앙값 **99.89 %** (사이클 0–800),
  `[인쇄]` 용량유지율 **95 % @600 · 89 % @1000**.
  `[재현]` CE 결손을 영구 Li 손실로 읽으면 누적 **161 mAh g⁻¹**, 실측 손실은
  **16 mAh g⁻¹**, 양극 전체 재고는 **215**. 89 % 를 설명하려면 CE 가 **99.988 %** 여야 한다.
  ★ **대조군이 같은 논문 안에 있다**: 20 mAh 소형 셀은 `[도표]` CE **99.97 %** ↔
  유지율 92.5 %@300 (= `[재현]` **99.974 %/cycle**) 로 **맞는다.**
  그리고 **CE 축의 눈금이 다르다** (Fig. 6g 95–101 vs SI Fig. 13c **99.4–100.0**).
  `[해석]` **셀이 커질수록 CE 의 상대 정밀도가 나빠지고, 그 순간 CE 는 `LLI` 의
  추정자가 아니라 계측 바닥이 된다.** 논문은 두 셀을 **한 번도 비교하지 않고**
  CE 계측 정밀도를 밝히지 않는다. → [[anode-free-li-inventory-accounting]].
- ★★ **그리고 `η` 가 `LLI` 도 가린다.** `[재현]` 이 셀의 0.5 C 방전 용량은
  146 mAh g⁻¹, 0.2 C 는 215 → **`η(0.5C) ≈ 0.68`**. **양극 재고의 32 % 가 운전 창
  밖에 있다** → Li 를 잃어도 양극이 쓰는 SOC 창이 이동할 뿐이다.
  `[해석]` **겉보기 용량유지율은 `LLI` 의 하한이다.** 완충 여력 `[재현]` 69 mAh g⁻¹
  으로는 위 간극(161)을 **부분적으로만** 설명한다.
  → [[assb-apparent-capacity-decomposition]] 의 `η` 가 `LAM_PE` 뿐 아니라 **`LLI` 도**
  가린다는 것이 실측으로 들어왔다.
- ★ **열화의 "계단" 이 음극에서도 나온다.** `[도표]` Lee Fig. 2d (맨 SUS 대조군,
  20 mAh, 0.1C/0.33C, 60 °C): 사이클 10 까지 ≈100 % → 15 에 ≈80 → **20 에 ≈50** →
  27 에 ≈20 → 50 에 **≈6 %**. **4호(Shi)의 양극 급락과 모양이 같은데 전극이 다르다.**
  `[해석]` → **"급락 = 양극 접촉 손실" 이라는 귀속이 위험하다.** `θ(N)` 을 계단으로
  모형화할 때 **어느 전극인지는 곡선 모양으로 정해지지 않는다.**
- ★ **1000 사이클 V–Q 는 "끝이 잘리는" 열화다.** `[도표]` SI Fig. 16 (0.5C/0.5C,
  사이클 1/200/400/600/800/1000): 충전·방전 곡선이 **0 ~ ≈110 mAh g⁻¹ 구간에서 거의
  완전히 포개지고** 방전 말단의 **무릎 하나만** 왼쪽으로 간다 (종점 146 → 131).
  `[해석]` **곡선 모양에 `LLI` 의 수평 이동 서명이 나타나지 않는다** — 움직이는
  자유도가 사실상 하나(용량 축 절단)다. **이 자료에 OCV 적합을 걸면 가를 정보가
  거의 없다.** ⚠ 단 CC 곡선이지 OCV 가 아니고, 저항 증가로도 같은 모양이 난다
  (그리고 **논문은 사이클 중 EIS 를 하지 않는다**).

### ⚠ 네 번째 실측 반례 (2026-09-16, Spencer-Jolly 2023) — **음극 OCP 가 충·방전에서 다른 곡선이다**

- ★★★ **충전 경로에 존재하지 않는 상이 방전 경로에 있다.** `[인쇄]` "The structural
  changes on discharge are **not simply the reverse** of those on charge" 이고, 구체적
  으로 `[인쇄]` "LiAg undergoes a phase transition from the **CsCl to the UPb
  structure** … more stable … when it is Li deficient … this explains why this
  structural form **only appears on discharge**."
  → **열역학적 이력이다** (동역학이 아니다). 그리고 율이 `[인쇄]` **30 µA cm⁻² ≈ C/68**,
  **상온**이다. `[해석]` **`i → 0` 으로 지울 수 없다.**
  → **[[halfcell-ocp-shape-invariance]] 의 "모양 불변" 이 ASSB 무음극 중간층에서
  깨지는 두 번째 방식**이고, 6호가 준 첫 번째(사이클에 따라 Ag 가 이동)보다
  **더 아프다** — **한 사이클 안에서** 깨지기 때문이다.
  자세히는 [[ag-c-interlayer-lithium-phase-path]].
- ★★ **`η(i)` 가 음극에서 급격히 비선형이다.** `[재현]` **2 mA cm⁻² 에서 과전압이
  ≈−0.09 V 로 3 h 내내 평평** ↔ **4 mA cm⁻² 에서 −0.16 → −1.15 V 로 자라다 ≈0.72 h
  (≈2.9 mAh cm⁻²)에 단락**. **전류 2 배에 과전압 ≈12 배.**
  그리고 **율이 상 조성 자체를 바꾼다** (`[인쇄]` 고율에서 "clear evidence of **Ag
  persisting** throughout charging") → **음극 쪽 `Q_material` 도 율 의존**이다.
  `[해석]` → [[assb-apparent-capacity-decomposition]] 의 율 스윕 분리 시험에서
  **두 율을 어디에 놓느냐가 결과를 지배한다** — 문턱 근처에서 `η` 가 사실상 발산한다.
- ★ **부분 단락 서명이 이 계보에서 세 번째로 나왔다.** `[인쇄]` 캡션은 "a sudden drop
  in cell potential to **approximately 0 V**" 라고 적지만 `[도표]` 실제로는 −1.15 V
  에서 한 번 ≈−0.1 V 로 튀었다가 **−0.5 ~ −0.9 V 로 되돌아가 톱니처럼 진동**한다
  (충전 시작점보다도 더 음이다). 4호의 **충전 전압 비단조 진동** · 5호의 **계단식
  붕괴**와 같은 계열이다. `[해석]` **`assb` 전용 판별 feature 후보에 근거가 하나 더.**
- ★ **6호가 "시료 준비 탓" 으로 돌린 자리에 첫 반례.** `[인쇄]` SI Fig. S3 (4 mA cm⁻²
  파괴 시료 단면): "Li metal nucleation and Li-Ag alloying **at the interface between
  the composite layer and Li₆PS₅Cl solid electrolyte**" — `[도표]` S 원소지도에서
  **전해질이 밀려난 자리에 5–15 µm 둥근 Li 덩어리**가 박혀 있다.
  ⚠ **파괴 조건에서만**이다 — 정상 저율에서는 도금이 층 **위**(집전체 쪽)에서 일어난다
  (SI Fig. S4). `[해석]` **6호를 반박하지는 못하고, "아티팩트로 돌리기 전에 대조를
  해야 한다" 까지가 주장 가능하다.**
- ⚠ **그리고 이 논문은 이 카드의 본체에 입력이 0 이다** — 양극이 없다.
  Q1(접촉 손실 정량)은 **7/7 편에서 비어 있다.**

### ★ 다섯 번째 — 반례가 아니라 **문헌 쪽의 요구** (2026-09-22, Li et al. 2026 · ⚠ Mini Review)

> ⚠⚠ **이 절의 모든 수치는 재인용이다.** 8호는 *Frontiers in Chemistry* 의 **Mini
> Review** 이고 1 차 측정이 0 이다. 아래 `[인쇄]` 는 "리뷰가 이렇게 적었다" 는 뜻이지
> "그 수치가 맞다" 는 뜻이 아니다.

- ★★★ **이 카드의 질문이 BMS 요구 사항으로 인쇄됐다.** `[인쇄]` §6.1: "A solid-state
  BMS may therefore need pressure or force sensing, pressure-dependent impedance models,
  and **diagnostics capable of distinguishing contact loss from ordinary electrochemical
  aging**" (Biçer et al. 2025).
  → 3호(Liu 2024)가 **축퇴가 존재한다**는 것을 인쇄로 확인했다면, 8호는
  **그것을 가르는 진단이 필요하다**는 것을 인쇄로 요구한다.
  ⚠ **정량은 0** 이고, 그 요구가 매단 인용 1 편도 **종설**이다.
- ★★ **식별 가능성이 처음으로 실패 모드 목록에 올랐다.** `[인쇄]` Table 4 중기 목표
  "Pack-level active diagnostics" 의 major failure mode = "**Unidentifiable pulse
  response**"; Table 1 "ECMs … can **lose physical uniqueness**"; Table 3 DRT
  "**Ill-posed inversion needs regularization**".
  `[인쇄]` §2 가 가장 세게 적는다: "**Parameter identifiability, cell-to-cell
  variability, and uncertain aging mechanisms can make a detailed model appear more
  precise than the available measurements justify.**"
  → `[해석]` **`degradation-degeneracy` 의 논지가 문헌 문장으로 존재한다.**
  ⚠⚠ **그러나 이 리뷰도 재지 않는다** — 조건수·프로파일 가능도·근최적 폭·Fisher/CRB
  **전부 0**. 그리고 그 문장에 붙은 인용 넷은 **전부 모형/매개화 논문**이며,
  `[인쇄]` "poorly identifiable" 문장이 매단 인용은 **Si–C 음극 소재 종설**이다
  (8호 digest D2). → **Q4 는 8/8 편 0 이다.**
- ★★ **산업 압력 요구치가 우리 압력 창 전체보다 아래다.** `[인쇄]` "Xu et al. (2024)
  note industrial requirements **below approximately 1 MPa**".
  `[재현]` `MPa` 가 12 쪽에 **1 회**뿐이고 그 값이 1 이다. 우리가 읽어 온 것:
  제작 **490**(6호)·**400**(7호) · 개입 **300**(4호) · 상한 **75**(5호) ·
  운전 **2–5**(5·6·7호). → **전부 위에 있다.**
  `[해석]` ① [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는
  **산업 셀에 더더욱 못 쓴다** ② 거꾸로 **`θ_AM` 의 시간 변화가 산업 조건에서 더 클
  것**이라는 방향이 생긴다. ⚠ **재인용이다 — Xu 2024 를 받아야 한다.**
- ★★ **"보정된 불확실성 0 / 8" — 세 번째 비어 있음 원장.** `[재현]` 8호 Table 2 의
  `Uncertainty output` 열을 세면 **보정된(calibrated) 불확실성을 보고한 편이 0 / 8**
  이다 (신뢰구간 1 · "가능하나 안전 보정 미시연" 1 · "주 산출 아님" 2 · "보고 없음" 4).
  `Validation level` 은 **7 / 8 이 `Cell`**.
  → 액체셀 **17/17 유일성 0** · `assb` **7/7 오차막대 0** 에 이어
  **BMS/SOH 추정 8/8 보정 불확실성 0** 이 붙는다. **세 계보가 같은 방향으로 비어 있다.**
  ⚠ 셋째 줄은 **리뷰가 고른 8 편을 리뷰의 분류대로 우리가 센 것**이고 원전 대조는 0 이다.
- ⚠ **재인용이 원전을 넘어서는 실측 사례가 잡혔다 — 우리 위키로 검증됨.**
  8호가 `[인쇄]` Table 3 에 "SOH RMSE **≤0.873 %** in Su et al. (2024)" 라고 적는다.
  우리는 그 원전의 digest 를 갖고 있다 (`raw/papers/su2024_drt-soh-health-features.md`):
  0.873 % 는 **5 셀 평균**이고 **cell5 는 1.607 %**(상한이 아니다), 게다가 같은 논문의
  **원시 EIS(0.573 %)·8-D(0.672 %) 가 제안 feature 를 모든 지표에서 이긴다.**
  → `[해석]` **리뷰가 원전의 과장을 `≤` 부등호로 한 단계 더 굳혔다.**
  **이 카드의 규율에 직결된다: 종설의 숫자를 이 위키의 근거로 삼지 않는다.**
- ⚠ **8호가 우리 축에 주는 것은 여기까지다.** ASSB 는 12 쪽 중 **한 문단(§6.1)**
  이고, `θ`·퍼콜레이션·면적분율·OCV 곡선·Li-In·dead Li 가 **전부 0** 이다.
  그리고 이 리뷰는 **열화 모드라는 개념을 한 번도 쓰지 않는다**
  (`LLI`·`LAM`·`degradation mode` 전수 0 회) — **Birkl 2017 을 인용해 놓고도**
  (8호 digest D8).

### ★★★ 여섯 번째 — **For 에 붙는 야생 실측** (2026-09-22, Huo et al. 2025)

앞의 다섯은 전부 "가르는 관측이 없다" 는 **부재**의 증거였다. 9호는 다르다 —
**가르지 않은 절차가 실제로 돌아가서 지분을 인쇄한 첫 사례**이고, 그 절차의
축퇴가 **같은 논문의 표 안에 세 개의 지문으로 남아 있다**.

| # | 지문 | 크기 | 논문이 부르는 이름 |
|---|---|---|---|
| 1 | `R_SEI` 분해가 **동일 화학·공정·프로토콜 두 셀**에서 부호까지 어긋남 (합계는 +23 %/+18 % 로 같은 방향) | **+37.1 % vs −79.7 %** | `[인쇄]` "**unexpected**" → "장비 정확도 · **적합 과정이 넣은 오차** · 열평형" |
| 2 | `A^p_eff · ε_p / R_s` **곱 축퇴** — 자기 SEM 의 입자 반경을 쓰면 `A_eff` 가 9 배 움직인다 | `A_eff ∈ [0.055, 0.494]` | 이름 없음. `[인쇄]` "retaining the **actual physical significance** of the parameters" |
| 3 | `k_LAM`(노화 속도 계수)이 **셀마다 다시 적합**되고 그 산포가 보고된 적합 오차보다 두 자릿수 크다 | **2.15 배 (≈115 %) vs "1 % 이내"** | `[인쇄]` "**slightly different**" |

★★★ **그리고 명제의 부정이 문자로 인쇄되어 있다** (`[인쇄]` 전문):

> "The values of certain parameters, such as `cp0`, `cn0`, `kp`, `kn`, `Dp` and
> `Dp_se`, **exhibit significant variations** … **To avoid potential
> misinterpretation, these values are not disclosed in this paper.** While such
> variations are expected …, **the robustness of the overall model and its
> predictive capabilities remain unaffected, as confirmed by our experimental
> results.**"

`[해석]` 세 단계다 — ① 적합 파라미터의 셀 간 산포를 **관측했다** ② 그 산포를
지면에서 **제거했다** ③ 제거의 정당화가 **적합도다**. 이것이
[[fitting-degeneracy]] 와 `degradation-degeneracy/` 가 측정으로 반박한 명제이고,
**3번 지문이 특히 인용 가치가 크다: 보고된 "정확도" 가 그 정확도를 만드는
파라미터의 셀 간 산포보다 두 자릿수 작다.**

⚠ **공정하게**: 두 셀은 **다른 노화 수준**(A 77 % · B 90 %)에서 측정됐으므로 합계
변화율의 유사성은 강하게 주장하지 않는다. **부호가 반대인 것만이 모호하지 않다.**
그리고 모집단이 **2** 뿐이라 산포의 폭 자체를 못 잰다.

★ 구조 유도는 [[assb-lampe-contact-product-degeneracy]] 에 있다.

### ★★★ 일곱 번째 — **방법론 쪽의 정식 근거** (2026-09-22, Vadhva et al. 2021 · ⚠ Review, 1차 측정 0)

9호가 **축퇴의 지문을 자기 표 안에 남기고 다르게 불렀다**면, 10호는 **그 지문이
지문이라는 것을 분야의 방법론 리뷰가 이미 인쇄해 두었다**는 것을 보인다.
⚠ **이것은 재인용 수치가 아니라 저자들의 1차 방법론적 주장이다** — 8호에서 세운
"리뷰 수치는 근거가 아니다" 규율의 **바깥에 있는 종류**다 (digest §12 참조).

**(가) 9호 §5.1 "하나의 원호에서 두 시상수" 에 대한 판정 — 다섯 문장** (전부 `[인쇄]`):

| # | 문장 | 9호에 대한 함의 |
|---|---|---|
| ① | "**As no solution to an EIS spectrum is unique**" | `R_SEI` 점추정에 근거가 없다 |
| ② | "**the inclusion of more elements will tend to improve the fit** of the equivalent circuit model" | **적합이 잘 맞는 것은 모델 선택의 증거가 아니다** |
| ③ | "using the **simplest ECM with the fewest elements possible** and ensuring that **physical and chemical meaning is maintained**" | 원호 1 개에 RQ 2 개 + W 는 이 원칙의 반대쪽 |
| ④ | "it is often challenging to **decipher how many time constants are present** in a given dataset and their assignment can be **highly subjective**" | "두 시상수" 라는 전제 자체가 주관이다 |
| ⑤ | "Physical features in the cell **may not be visible in the EIS spectra**" | 반대 방향(있는데 안 보임)도 동시에 열려 있다 |

`[재현]` 9호의 회로(`R_b` + RQ + RQ + `W`)는 자유 파라미터가 **1 + 3 + 3 + 2 = 9 개**
다(CPE 하나가 R·Q·α 셋). **원호 하나에 9 개를 맞춘 것이다** — 9호는 이 개수를 세지
않는다.

**(나) ★ 처방 — 그리고 9호는 넷 중 하나도 쓰지 않았다** (9호에 `Kramers`·`Kronig`·
`DRT`·`symmetric cell`·`AIC` **전수 0 회**):

| 처방 | 원전 사례 | 무엇을 하나 |
|---|---|---|
| **K–K / Lin-KK 사전 검증** | ref. 41–43 (Boukamp; **Schönleber Lin-KK**, KIT 2015 — 소프트웨어) | 적합 **전에** 데이터가 선형·정상·인과인지 판정 |
| **DRT 로 시상수 개수를 먼저 정한다** | ref. 62 Pang 2019 — `[인쇄]` "**unambiguously identified three semicircles**" | 개수를 **데이터가** 정하게 한다 |
| **조건을 바꿔 시상수를 벌린 뒤 구속으로 되가져온다** | ★ ref. 82 Bron (−130 °C 에서 `R_gb` 동정 → 실온 추적) · ref. 28 Krauskopf (400 MPa 로 `R_int` 제거 → `GB` 노출) | **여기(excitation)를 늘려 축퇴를 깬다** |
| **상보 대칭셀 쌍으로 전극을 귀속** | ref. 70 Iriyama · ref. 126 Ohta · ★ ref. 161 He (LFP 대칭셀 + Li 대칭셀 두 개로 **어느 계면이 변했는지 확정**) | 주파수 추론 대신 **직접 분리** |
| **AIC 로 회로를 순위 매긴다** | ref. 51,52 (Akaike 1974; **Ingdal 2019**) | 과적합을 **정보량 기준**으로 벌한다. ⚠ **실험 적용 0** |

**(다) ★★★ 새 명제 — "분해 가능한 RC 의 개수는 실험 조건의 함수다"**
리뷰가 다섯 곳에서 따로 서술하고 **한 명제로 모으지는 않는다. 우리가 모은다**:

| 사례 | 조건 | 개수 변화 |
|---|---|---|
| `[도표]` Fig. 8 (Bron, 황화물 5 종) | 동일 −130 °C | **5 중 3 만** `R_gb` 가 분해된다 — 입계는 **5 개 모두에 존재**한다 |
| `[도표]` Fig. 7 아래 인셋 (LGPS) | 27 °C | **원호 0 개** — 절편뿐인데 σ = 12 mS cm⁻¹ 가 거기서 나온다 |
| `[도표]` Fig. 11a (Krauskopf, LLZO) | 1 → 400 MPa | `R_int` 가 사라지자 **`GB` 원호가 나타난다** |
| `[인쇄]` Aziz (PEO) | 60 °C 초과 | **상경계 임피던스가 완전히 소멸** |
| ★ `[인쇄]` Larfaillou (LiPON) | **60 h / 60 °C 보관 노화** | **RQ 3 개 → 4 개**, 새 RQ 의 귀속은 `[인쇄]` "Li\|LiPON interface **and/or** in the LCO bulk" |

`[해석]` **마지막 줄이 우리 축에 가장 무겁다**: ① **모델 차수가 상태변수다** — 고정
회로로 노화 시계열을 적합하면(9호가 한 일) 모델이 틀린 구간이 생긴다 ②
**새로 생긴 저항이 음극 계면인지 양극 벌크인지 가르지 못한 채 출판된다.**

**(라) ★★ EIS 자체가 접촉 손실과 계면상 성장을 한 저항에 합친다** — 이 카드의 핵심:

> `[인쇄]` (Fig. 9 본문, In\|LGPS\|LCO): 충전 중 중주파 양극 계면 저항의 증가는
> "**loss of interfacial contact in the composite cathode due to volumetric
> expansion** **and** the **formation of a decomposition layer on exposed LCO**"
> 때문이다.

`[해석]` **두 기구가 하나의 `R_MF` 에 귀속되고, 가르는 관측은 이 논문에도 리뷰에도
없다.** [[assb-lampe-contact-product-degeneracy]] 가 **방전 V–Q 영역**에서 보인 곱
축퇴와 **같은 구조가 주파수 영역에서 반복된다** — 그리고 **두 축퇴는 독립이라 곱해진다**
(그 페이지의 처방표에서 "다중 SOC EIS" 에 ⚠ 가 붙는 이유).

**(마) ⚠ 관측의 자기 반증 사례 — 이 계보 최초**
> `[인쇄]` Itagaki 는 Li 기준극으로 in-situ EIS 를 분해해 **흑연 음극의 저주파
> 인덕턴스**를 추적했다. "**However**, a study using pulsed charge/discharge
> conditions on a similar cell set-up, concluded that this inductance feature was
> **measurement artefact, due to the violation of the QSS condition** at low
> frequencies."

`[해석]` **3 전극 · 기준극 · 전극 분해를 다 갖춘 측정에서도 저주파 특징이 물리가
아니라 아티팩트였다.** 우리 위키에 이만큼 직접적인 "관측에 붙은 물리 이름이 취소된"
사례가 없었다. **그리고 같은 논문 Table 1 은 여전히 저주파 인덕턴스를
`[인쇄]` "degradation processes" 로 적는다** (digest D6).

**(바) ⚠ 문헌의 EIS 수치가 전제 위반 상태로 쌓여 있다**
`[인쇄]` §2.1 기준은 섭동 **<50 mV**. 그런데 LGPS 를 발견한 *Nature Materials* 논문
(Kamaya 2011)에 대해 이 리뷰가 적는다 — `[인쇄]` "these EIS measurements were taken
with **large perturbation voltages of 100 to 500 mV, which may enter the non-linear
regime** and data were **not explicitly checked using K–K tests**."
`[해석]` **기준의 2–10 배**다. 분야 정초 수치가 선형성 검증 없이 인용되고 있다.

**(사) 재현성의 첫 숫자** — `[인쇄]` 5 화합물 기관 간 라운드로빈: 상대 **중앙값**
오차가 `>1 mS cm⁻¹` 재료에서 **22 %**, `<1 mS cm⁻¹` 에서 **~10 %**. 원인으로
`[인쇄]` "the **fitting of limited EIS data** and microstructural relaxation".
★ **재료가 좋을수록 산포가 커진다** — 시상수가 주파수창 밖으로 밀려 적합할 데이터가
줄기 때문이다. ⚠⚠ **재인용이고 인용 번호가 틀렸다**(본문 ref. [85] ↔ 실제 ref. [191]
Ohno *ACS Energy Lett.* 2020) — 원전을 받기 전까지 **방향만** 쓴다.
⚠⚠⚠ 그리고 이것은 **단일 파라미터 `σ_ion`** 의 산포다. `[해석]` **다중 RC 적합
파라미터의 산포는 이것보다 클 수밖에 없다** — 리뷰는 그 말을 하지 않는다.

### ★★★★ 여덟 번째 — **For 에 붙는 야생 실측, 그리고 10호의 경고가 데이터로 나타난 자리** (2026-09-22, Yu et al. 2024 · Schaeffler + Ohio State)

`raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md`
(*J. Power Sources* **597** (2024) 234116; 본문 8 쪽 + **SI `.docx`** 7,607 자 +
그림 S1–S5, 둘 다 sha256 봉인). **수치의 정본은 원문이고 아래는 사본이다.**

**이 편은 10호(Vadhva)가 처방한 DRT 를 실제로 돌린 첫 `assb` 논문이다.** 그리고
10호가 경고한 것들이 **데이터로 나타난다** — 논문이 알아채지 못한 채로.

**(가) ★★★ "분해 가능한 시상수 개수" 가 상태·조작·장비의 함수라는 것을 1 차
데이터로 네 번 보인다.** 10호는 이것을 **Larfaillou 2016 재인용**(신품 3 RQ →
노화 4 RQ)으로만 전했다. 11호에서는 우리가 그림을 직접 열어 셌다:

| 자리 | `[도표]` 무엇이 변하는가 |
|---|---|
| Fig. 2(a) 완전지 | 국소 극대 **2–3 (4 cy) → 5 (48 cy)**. P3 는 4 cy 에 **어깨**였다가 48 cy 에 **봉우리**가 된다 |
| Fig. 3(c) micro-SE 반쪽 | 중주파 극대 **1 개 (cy 3) → 2 개 (cy 29~)**. 그리고 cy 3 의 극대는 ≈9 × 10³ Hz 인데 이후 P2 는 ≈1.8 × 10⁴ Hz — **봉우리가 쪼개지며 자리를 옮긴다** |
| Fig. 6(c) graphite 반쪽 | **P4 가 없던 자리(평탄 ≈1.5)에 생긴다** (cy 133 에 ≈10 Hz, 5.5) |
| Fig. 7(d) 완전지 재가압 | **4 → 3** — 재가압 후 P3 의 독립 극대가 **사라진다** |

`[해석]` **노화가 개수를 올리고 개입이 개수를 내린다 ⇒ 모델 차수는 상태변수다.**
⚠ 그리고 **논문은 세 번 다 "봉우리가 커졌다" 고 적고 "봉우리가 생겼다" 고 적지
않는다** (`[인쇄]` "growth of P3 … peak intensities" · "P4 … exhibits a **gradual
increase** in peak intensity"). → **고정 회로로 노화 시계열을 적합하는 관행
(9호가 한 일) 전체에 대한 실측 반례다.**

**(나) ★★★★ 축퇴의 크기를 잴 재료가 SI 에 있고, 그 크기가 본문 효과와 같다.**
`[도표]` **Fig. S3** — 같은 셀(로 보이는 것)을 **배선만 바꿔** 잰 두 DRT:

| 봉우리 | Arbin+Gamry | Gamry 직결 | `[재현]` Δ |
|---|---:|---:|---:|
| ≈3.5 × 10⁵ Hz | 117 | 105 | −10 % |
| ★ ≈2 × 10⁴ Hz | **39 (분해된 어깨)** | **없음** | **특징 1 개 차이** |
| ≈3 × 10³ Hz (= P3 자리) | 78 | 66 | **−15 %** |
| ★ ≈3 × 10⁻² Hz | 45 | 76 | ★★ **+69 %** |

**본문이 물리로 해석한 변화**: 재가압이 P3 **−16 %** · P1 **−11 %** · P2 **−10 %** ·
P4 **−25 %**. → ★★★★★ **본문의 모든 개입 효과가 SI 의 배선 인공물 폭 안에 있다.**
논문은 이 비교를 하지 않는다 — `uncertaint*`·`error bar`·`uniqu*`·`regulariz*`
**전수 0 회**라서 **할 어휘가 없다**.
⚠ **공정하게**: 배선이 바뀌면 인덕턴스·접촉저항이 실제로 변하므로 일부는 진짜
물리이고, 두 측정의 최고 주파수가 **1 MHz ↔ 2 MHz** 로 다르며, "같은 셀" 이라는
명시가 SI 에 없다. **그러므로 69 % 는 상한이다.** 그러나 **상한조차 본문 효과보다
크다**는 것이 요점이다.

**(다) ★★★★ 이름표의 위치 불확정성이 이름표 간격보다 크다.**
`[재현]` P3 의 보고 위치: **~500 Hz**(§3.1 완전지) · **10³–10² Hz**(§3.1 NMC 반쪽) ·
**10⁴–10³ Hz**(§3.2) · **~1 kHz**(§3.3) · **~10³ Hz**(Table 1) · `[도표]` **0.9 kHz**
(Fig. 7d) · **1.3 kHz**(Fig. 4d) · **≈2.8 kHz**(Fig. 3c) ⇒ **500 Hz – 10 kHz =
1.3 자릿수**. 그런데 **P2–P3 간격은 0.8 자릿수** (`log₁₀(6000/900) = 0.82`).
★ `[인쇄]` Table 1 은 **P2 = 화학적 접촉(SEI/CEI)**, **P3 = 기계적 접촉**이다.
→ `[해석]` **화학 열화와 기계 열화의 분리가 바로 이 자리에서 무너진다.**

**(라) ★★★ 논문 자신의 결론 지도가 축퇴를 그림으로 인쇄한다.** `[도표]` **Fig. 8**:
- **P2 와 P3 에 `Cathode`(빨강)와 `Anode`(파랑)가 둘 다 찍혀 있다** ⇒
  **"P3 가 자랐다" 가 어느 전극인지 말해 주지 않는다.**
- **P4(음극 CT, 넓음)와 P5(양극 CT, 좁음)가 ≈10 Hz 에서 겹쳐 그려져 있다** ⇒
  **두 전극의 전하이동이 주파수로 분리되지 않는다.**
- **(P1′) 이 회색 점선이다** — 측정 대역(2 MHz) 위에 있어 **못 본 봉우리를 지도에
  그려 넣었다**. 그리고 `P1′` 는 본문·Table 1 에 **없다**.

**(마) ★★★ 압력 연산자가 직교하지 않는다 — 4호에 붙는 반례.**
`[도표]` Fig. 7(d): 재가압(>500 MPa)이 **P4(graphite 전하이동)를 −25 %** 줄인다.
Fig. 4(d): **P1(SE 입계/케이블) −11 %**, **P2(화학 접촉) −10 %**.
`[해석]` **기계적 조작이 "화학" 항과 "전하이동" 항도 같이 줄인다** ⇒
[[assb-pressure-reapplication-separation-test]] 의 `Q_apparent = θ_AM(P,N)·η(i)·
Q_material(N)` 에서 **`P` 가 `θ_AM` 에만 들어간다는 가정에 반례가 붙는다.**
⚠ 그리고 **회복 크기가 4호의 1/12** (`[재현]` +4.91 % vs `[재현]` +60.5 %p)인데
`[인쇄]` "agree with previous report by **Ceder et al. [21]**" 라고만 쓰고
**크기를 비교하지 않는다** — ref. [21] 이 바로 우리 **4호(Shi 2020)** 다.

**(바) ★★ 순환: DRT 가 ECM 을 입력으로 받는다.**
`[인쇄]` Fig. 2 캡션 — "The DRT peaks were computed **based on the simulated
Nyquist curves (green solid-line)** after subtracting the low-frequency data."
10호의 정답 절차(ref. 62 Pang 2019)는 **K–K → DRT 로 개수 결정 → 그 개수만큼
ECM** 인데, 11호는 **ECM 적합 → 그 곡선으로 DRT** 다. `[해석]` **DRT 가 분해할 수
있는 개수가 적합 모델의 차수에 의해 위에서 막힌다.**
⚠ SI 는 다르게 쓴다 — `[인쇄]` "the fitted model is subtracted from the
**measurement data**". **두 절차가 같은 논문 안에서 충돌한다** (digest D1).

**(사) 그리고 10호의 λ 공백(G4)은 메워지지 않았다 — 더 깊어졌다.**
`regulariz*`·`λ`·`L-curve`·`GCV`·`cross-valid*`·RBF shape factor **본문 + SI 전수
0 회**. 유일한 방법 서술이 `[인쇄]` "MATLAB-based DRT calculation code developed
by **T.H. Wan et al. [16]**" 한 줄이고, SI 는 DRT 를 **보통의 적합 문제**로
소개하며 `[인쇄]` **"The well-fitted `Z_DRT` can represent the actual physics in
the system"** 이라고 쓴다 — 10호의 `[인쇄]` "mathematically **ill-posed**,
requiring regularization" 의 **정반대 진술**이다.
`[재현]` 10호 처방 14 항목 채점: **✅ 2 · ⚠ 5 · ❌ 7** (digest §18).

### ★★ 열한 번째 — **For 에 붙는 야생 실측 + "관측 추가" 의 첫 실험 표본** (2026-09-22, Oh et al. 2025 · 실험, Hot Paper)

`raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` (*Angew. Chem. Int. Ed.* 64,
e202514910; 서울대 + HMG-SNU JBRC). 컴파일: [[assb-maxwell-ocv-derivative-channels]].

**이 편이 이 카드에 하는 일은 셋이다 — 실측 하나, 관측 축 하나, 경고 하나.**

1. ★★★ **실측 (For)**: `[인쇄]` 50 사이클 뒤 XRM 공극률 **4.5 → 9.8 %**(10 MPa) ↔ **4.4 →
   5.3 %**(20 MPa) 인데 용량 유지율은 **86.0 % ↔ 84.0 %** — void 가 2 배인 셀이 **더 높다**.
   논문은 "similar … internal voids may not directly affect the early-cycle performance" 로
   지나간다. `[해석]` 이 카드의 언어로: **접촉 손실이 이 창에서는 `Q_apparent` 에 전혀
   안 들어간다.** OCV 적합은 `LAM_PE ≈ 0` 을 (정확히) 보고하고 **void 2 배를 놓친다** —
   "OCV 만으로는 못 본다" 의 가장 깨끗한 형태(오독이 아니라 **무감**). 1호의 `θ_AM ≈ 1
   above p_c` 와 정합하고, 4호(면적 10.4 % ↔ 60 %p)의 반대쪽 끝이다 — **사상이 문턱형**이라는
   두 점.
2. ★★ **관측 축 (관측 추가)**: 이 편은 `E(x)` 를 적합하지 않고 같은 상태함수의 두 편미분
   `−F(∂E/∂T)_P = ΔS` · `F(∂E/∂P)_T = ΔV` 를 잰다 — [[constrained-crb-identifiability]] 의
   "관측 추가" 칸에 들어가는 **첫 ASSB 실험 표본**이다. `[해석]` 우리 쌍에 대한 새 행의
   부호: 균일 `LAM_PE`·완전 고립 접촉 손실은 둘 다 **아핀**이라 ΔS(x) 모양 불변(**새 행 = 0**);
   void 는 `dE/dP` 를 움직인다(**새 행 ≠ 0**, 이 편의 주장) ⇒ **분리 후보 행은 volumetry**이고
   **엔트로피메트리는 아니다** — 이 편은 반대로 ΔS 를 주 진단으로 둔다. ⚠ 실측 0, 우리 명제.
3. ⚠ **경고 (Against 쪽 단서)**: `[인쇄]` ΔS 는 "contact loss **as well as** … interfacial
   resistance" 를 한 신호로 받는다 — **이 편 스스로 우리 쌍을 합친 채널이라 정의한다.**
   그리고 volumetry 의 `dE/dP` 는 `[재현]` **압력 구간에 2 배 의존**(0.44 ↔ 0.23 mV/MPa,
   신품끼리)하고 **전·후 측정의 SOC 가 171 mV 다르다**(D7) — 관측 추가의 "새 행" 이
   상수가 아니라 `(P, x)` 의 함수라는 뜻. 상수 `ΔV` 로 넣으면 모델 오차가 된다.

**Q4 는 0/14 이고 성질이 일곱 번째로 바뀐다** — 역문제가 없어서 조건수가 정의될 자리가
없고, 대신 **귀속의 유일성**(ΔS 변화가 비균질인가 재료 변화인가; `[재현]` SOC 축 적분이
≈ −3.5 → ≈ +1.5 로 부호가 바뀌는 것은 비균질만으로는 안 나온다 — G8)을 아무도 묻지 않는다.

### ★ 열두 번째 — **근거가 아니라 "1호가 야생에서 어떻게 읽히는가" 의 첫 실측** (2026-09-22, Rahman & Lu 2024 · ⚠⚠ 학회 회의록 6 쪽, 1차 측정 0, **재인용 수치도 0**)

`raw/papers/rahman2024_sbms-rul-solid-state-batteries.md`
(*Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085; 6 쪽, SI 없음, sha256 봉인).

⚠ **이 절은 이 편의 주장을 근거로 쓰지 않는다.** 쓸 수 있는 주장이 없다 —
`[재현]` 본문 2,331 단어에서 인용 괄호·절 번호를 빼면 남는 숫자가 **`2024`(회의 연도) ·
`8085`(Abstract ID) · `19`(COVID-19) · `2021`·`2026`(연구비 기간)** 뿐이다.
`capacity`·`experiment*`·`measur*`·`contact`·`pressure` 가 **전부 0 회**다.
이 절이 쓰는 것은 **인용 관계 두 개**다.

**(가) ★★★ `assb` 1호가 인용되는 방식 — 어긋난다.**
이 편 ref **[5]** = 우리 1호 (Bielefeld, Weber, Janek, *JPCC* 123, 1626−1634).
인용된 **유일한 자리**가 서론의 이 문장이다:
`[인쇄]` "These technologies [ANN, Adaptive Fuzzy Logic] … mainly address key challenges
such as **load balancing, state-of-charge estimation, and overall battery health
monitoring [5, 6]**."
우리 1호 digest 가 전수 계수로 기록한 원전의 상태: `[인쇄]` **"셀 실험 0 개이고,
사이클링·전압·용량이 없다"** · Q5 행 `voltage` **1 회 — 그마저 참고문헌 제목** ·
**"모델에 음극이 없다 — 복합양극만"** · Q8 행 **"OCP 곡선이 없다. 전압축 자체가 없다."**
그 논문이 실제로 계산하는 것은 **이용률 `θ = V_c/V_ν`(식 6)** 와 **활성 계면적**이다.
→ **판정: 어긋난다.** 그리고 서지도 틀렸다 — **연도 2018(원전 2019)**, 저자 "W. Dominik A".
`[해석]` **번호 실수로 보기 어렵다**: 같은 저자의 **다른 논문 [28]**(2020 바인더 편)이
§4.1 에 따로 있고 거기서는 내용이 대체로 맞게 요약된다. 서론의 `[5, 6]` 은 "SSB 문헌임"
만으로 고른 **장식 인용**이다([6] 도 argyrodite 합성 논문).
★★ **이 카드에 주는 함의**: 1호 digest §12.4 에서 `Q_apparent = θ_AM · Q_material` 을
**우리 해석**이라고 못 박고 "논문은 용량도 전압도 주지 않는다" 고 적은 것이
**보수적이지 않았다** — 바깥에서는 그 다리가 없는 채로 **BMS 문장에 직결된다.**

**(나) ★★ `assb` 12호가 인용되는 방식 — 어긋나지 않지만 결론이 버려진다.**
이 편 ref **[21]** = 우리 12호 (Sadegh Kouhestani et al., *Energies* 15, 6599).
쓰인 자리는 §3.1 끝의 **교과서적 ANN 정의**(세 층 · FNN 비순환 vs RNN 순환) 한 문장이다.
⚠ 우리 12호 digest 가 그 수준을 채록하지 않았으므로 **어긋남 미확인(정합 추정)**.
★ 문제는 다른 데 있다 — **12호의 자기 결론이 전달되지 않는다**:
`[재현]`(12호 digest, Table 1 해체) **"SSB 의 실측 열화 데이터로 SOH/RUL 을 추정한 항목:
0 / 28"** · `[인쇄]`(12호 §4) "most PHM techniques are based on **simulation** results and
not experimental" · `[인쇄]`(12호 결론) "very few studies … **lack of accurate data**".
15호는 이 논문을 인용하면서 **그 위에 "SBMS 로 SSB 의 RUL 을 늘린다" 를 얹는다.**
`[해석]` **12호(2022)가 감사로 적어 둔 공백을, 15호(2024)가 12호를 인용하면서
그대로 재생산한다.** 12호 항목이 "2022 → 2026 사이 PHM 문헌은 identifiability 라는
**이름**을 얻었고 여전히 재지 않았다" 로 끝났는데, **15호는 그 사이(2024)에서 이름조차
못 얻은 표본**이다 (`identifiab*` **0 회**).

**(다) 이 편이 아는 유일한 SSB-ML 라벨 = `simulated`.**
`[인쇄]` ref [22] (Asheri 2023) — "a **data-driven multiscale simulation framework**
(leveraging artificial neural networks) to predict and analyze the degradation in
solid-state batteries, focusing on **interface damage** and its impact on cell
performance." `[재현]` 이 편 참고문헌 **33 편 중 SSB 15 · 액체 LIB/EV 14 · 배터리가
아닌 것 2**([27] Cu(II) 흡착, [31] COVID-19) — **그리고 SSB 집합과 ML/BMS 집합이
교차하지 않는다**([21] 종설·[22] 시뮬 제외). **"SSB 데이터에 ML 을 돌려 RUL 을 낸"
인용은 0 편이다.**

**(라) ⚠ 인용 구조 자체의 결함 — 결론의 근거가 도메인 밖이다.**
`[인쇄]` §5 "Significant progress has been made in integrating ANN and adaptive fuzzy
logic **in SBMS**, **as evidenced by** studies by Y. J. Wongt et al. **[27]**."
ref [27] = Wong et al., *Environ. Monit. Assess.* 192 (2020) — "**Cu(II) adsorption from
aqueous solution using biochar derived from rambutan peel**". **배터리 논문이 아니다.**
(§4.2 의 [31] COVID 논문은 적어도 `[인쇄]` "**could be insightful**" 로 유추임을 밝힌다 —
이 편에서 인용 위생이 지켜진 유일한 자리다.)

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 이 편은 근거를 주지 않는다.
이 절이 고정하는 것은 둘이다 — ① **우리 1호의 결과가 인용 체인을 타고 나갈 때
어디서 끊어지는가**(전압·용량으로 번역되는 층이 통째로 건너뛰어진다) ②
**분류 체계 세 번째 표본 "어휘 미도입"** (12호 병합 · 13호 미배정 · 15호 미도입;
셋 다 종합 층위 문헌이고, 1차 측정이 있는 편은 전부 접촉 축을 갖는다).

### ★★★ 열세 번째 — **For 에 붙는 가장 직접적인 실측 구조** (2026-09-22, Ramanayagam et al. 2026 · 실험, 3전극)

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
앞선 열두 항목이 "**OCV 로는 못 가른다**" 를 **모델의 구조**(1·2·3·9호)나 **관측의 부재**
(4–7호)나 **종합 층위의 침묵**(8·10·12·13·15호)에서 끌어왔다면, **16호는 처음으로
"가르지 못하는 순간" 자체를 지면에서 보여 준다.**

**For 에 들어가는 이유 — 세 문장으로**:
1. 논문이 **접촉 면적이라는 양에 이름을 붙이고**(식 4), **값을 완전 접촉으로 고정**하고,
   **압력이 접촉을 개선했다고 말로 결론**내면서, **숫자는 전부 `j₀`(동역학)에 넣는다.**
2. 그 결과 **같은 데이터가 `j₀` 증가(1.8 배)와 감소(0.60 배)를 둘 다 허용한다**
   (배정에 따라 — 위 §16호 항목 2).
3. **논문은 두 배정 중 하나를 고른 적이 없다.** 고를 관측이 그 지면에 없기 때문이다.

★ `[해석]` **이것이 우리 물음의 EIS 판이다.** 우리 카드는 "OCV 적합이 `LAM_PE` 와 접촉 손실을
가르는가" 를 묻는데, 16호는 **EIS + TLM 도 같은 자리에서 갈라지지 않는다**는 것을 보인다 —
그리고 **EIS 는 OCV 가 못 보는 것을 본다고 여겨지던 채널**이다. 즉 **"관측을 늘리면 갈린다"
의 가장 유력한 후보 하나가, 늘린 뒤에도 같은 곱 위에 서 있다.**
⚠ **단서**: 16호의 축퇴는 **신품 셀의 압력 효과**에 대한 것이지 **열화 지분**에 대한 것이 아니다.
이 편에는 열화가 없다(`LAM`·`LLI` 0 회). **구조가 같다는 것이지 결과를 옮긴 것이 아니다.**

★★ **그리고 이 편은 Against 쪽에도 재료를 준다** — 아래 §"Against" 마지막 항목
(`R_CT·C_dl` 채널). **같은 논문이 축퇴를 밟고, 축퇴를 깰 두 숫자를 인쇄해 놓고 쓰지 않는다.**

### ★★★★ 열네 번째 — **For 에 붙는 새 경로: 상대극 기준 전위 → 겉보기 `LAM_PE`** (2026-09-22, Yanev et al. 2024 · 실험, 3전극 + 전위 채널)

`raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`.
지금까지의 For 근거는 **양극 안**의 혼동(접촉 손실 ↔ 진짜 활물질 손실)이었다.
**17호가 여는 것은 바깥의 경로다 — 양극은 멀쩡한데 상대극 때문에 양극이 줄어 보인다.**

**같은 두 셀, 같은 양극, 같은 프로토콜, 0.1 C**:
- `[도표]` 방전 용량 **198 ↔ 185 mAh g⁻¹** (= **6.6 % 부족**), 방전 곡선이 `Q ≈ 170`
  까지 **구별되지 않고 끝의 무릎 위치만 다르다** ⇒ **`LAM_PE`(또는 컷오프 이동)의 서명**
- `[재현]` 3전극이 말하는 것: **양극 임피던스가 ≈31 ↔ ≈32.5 Ω (5 % 차)로 같다.**
  `[도표]` `E_CE` 가 방전 끝에 **0.62 → ≈1.0 V** ⇒ `E_cell` 하한 2.38 V 조기 도달 ⇒
  `[재현]` **양극이 3.0 V 대신 ≈3.4 V 에서 멈춘다.** **활물질은 그대로다.**

그리고 **반대 방향의 짝**도 같은 논문 안에 있다 — `[인쇄]` 과리튬화(50 at% foil)로
기준이 **−0.2 V** 내려가 `[인쇄]` **컷오프가 4.3 대신 4.1 V** 가 되고 **충전 용량이
40 mAh g⁻¹ 준다.** ⇒ **한 논문 안에서 `LAM_PE` 흉내와 `LLI` 흉내가 둘 다 나온다.**

★★★ `[해석]` **이것이 For 에 주는 것**: OCV/용량 채널만으로는 **"양극이 줄었다" 와
"상대극이 움직였다" 를 가를 수 없다.** 가른 것은 **세 번째 전극**이다. 그리고 이 편은
**그 세 번째 전극이 없으면 어떻게 되는지도 보여 준다** — 2전극 Fig. 1 에서 저자가
50 at% 셀의 기준 이동을 잡아낼 수 있었던 유일한 이유는 **Li 함량을 의도적으로 스윕해
곡선 모양의 변화를 봤기 때문**이고, **셀이 하나뿐이었다면 구별할 수 없다.**

⚠ **단서 넷**:
1. **열화가 아니다.** 최대 5 사이클, 신품, `LAM`·`LLI` 0 회. **제조 변수**의 실증이지
   `θ(N)`·`LLI(N)` 의 근거가 아니다.
2. **`n = 1`**(조건당 셀 1 개, 오차막대 0). 6.6 % 라는 숫자에 산포가 없다.
3. **기준극이 검증되지 않았다** — LPSCl 안의 Li 금속인데 같은 논문 서론이 그 조합의
   불안정을 적는다. `[재현]` 우리가 뽑은 상한은 **(RE 표류 + 음극 과전압 + 옴) 합
   ≈20 mV / 20 h** 뿐이다.
4. **0.1 C 의 ±10 mV "음극 과전압" 은 옴 강하(≈9.1 mV)와 구별되지 않는다** — 즉
   이 편이 **"평탄하다" 고 확인한 쪽의 분해능도 ±10 mV 가 바닥이다.**

→ [[assb-li-in-reference-potential-window]] (전용 페이지, 2026-09-22 신설).

### ★★★★ 열다섯 번째 — **For 에 붙는, 그러나 절반이 갈린 야생 실측** (2026-09-22, Fukunishi et al. 2023 · 실험, 3전극 + 열화)

`raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md`

**For 쪽 근거 — 지면이 갈림을 인쇄한다:**

> `[인쇄]` "R3 drastically increased (6 times larger) during the durability tests.
> These results suggest that **the chemical composition at the interface or the contact area**
> between the NCM523 and electrolyte particles changed."

**전극 분해된 임피던스 + 단면 SEM/EDX + 원소 맵을 다 갖춘 실측 논문이, 자기 관측량
하나(`R3`)로는 계면 화학과 접촉 면적을 못 가른다고 인쇄한다.** 이 카드가 액체셀에서
받았던 것과 같은 형태의 진술이고, **여기서는 ASSB 실험 지면에서 나온다.**

그리고 같은 절이 **`θ_AM` 을 용량 손실의 기구로 명시**한다:
`[인쇄]` "if insulative layers **completely cover** the active material to make the particle
**inactive**, such **dead particles** … **could explain the large capacity decrease**". **값 0.**

**⚠ Against 쪽으로 반쯤 넘어가는 이유 — 우리가 그 "or" 를 갈랐다:**

`[재현]` 저자의 **Fig. 5**(노화 전후 `R`과 `τ` 를 둘 다 인쇄)에 16호 처방을 적용하면
`C ≡ τ/R` 의 비가 **LPSI 0.37 ± 0.07 · LPSCl 1.07 ± 0.19** 이고, 순수 면적 손실이면
0.15 / 0.13, 순수 동역학이면 1.00 이어야 한다 ⇒ **LPSCl 은 화학만, LPSI 는 둘 다.**
★ 그리고 그 분해가 **같은 논문의 SEM(LPSI 에만 입자를 덮는 O·P 층 2 µm)과 독립으로
일치한다.**

⇒ `[해석]` **이 카드의 답이 "못 가른다" 에서 "관측을 하나 더 인쇄하면 갈린다" 로
한 칸 움직인다.** 필요한 추가 관측은 새 장비가 아니라 **이미 적합된 용량 파라미터를
같이 보고하는 것**이었다.
⚠⚠ **단, 이것은 측정이 아니다** — 로그 막대 판독 · 노화 후 `p` 미공개 · `C∝θ` 가정 ·
조건당 셀 1 개 위에 있다. 그리고 **같은 처방을 신품 입자크기 축에 적용하면(검사 A)
용량이 면적처럼 스케일하지 않는다**(`p` 가 같은 두 온도에서 0.68 / 1.10 vs 예측 2.0–2.4)
— 즉 **`C_dl ∝ 접촉 면적` 이라는 처방의 전제 자체가 이 데이터에서 흔들린다.**
⇒ **처방은 "쓸 수 있다" 가 아니라 "쓰려면 `C_dl` 의 면적 비례성을 먼저 검증해야 한다"
로 정련된다.**

### ★★★ 열여섯 번째 — **For 도 Against 도 아닌 "라벨의 바닥" 표본** (2026-09-22, Yoshida et al. 2024 · 실험, 4전극, **전극 없음**)

`raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md`.
이 편에는 **활물질도 용량도 사이클도 없다** — 재는 것은 **SE 펠릿 두 장을 포개서 만든
계면 하나**뿐이다. 그래서 `LAM_PE` ↔ 접촉 손실의 **직접 근거가 아니다.**
**그럼에도 이 카드에 들어오는 이유 셋**이고, 셋 다 **For 를 세게 만든다.**

**① 상대극이 관심 대역을 통째로 덮는다 — 그리고 저자가 그렇게 인쇄한다.**
`[인쇄]` Li-In 전극 자신의 반원이 **P1(>1 kHz)과 P2(1 kHz–0.1 Hz) 둘 다와 겹치고**,
그래서 "**P1 and P2 are difficult to extract** from the impedance measured with the
two-electrode system with InLi counter electrodes."
⇒ **For 가 지금까지 "OCV 로는 못 가른다" 였다면, 여기에 "2전극 EIS 로도 못 뽑는다" 가
붙는다.** 그리고 **해법이 알고리즘이 아니라 배선이다**(4전극).
`[도표]` 보태어: **같은 공칭 Li-In 박(25 at%)의 전극 저항이 39 / 172 / 54 Ω, 4.4 배 (n=3)**
⇒ 17호가 `E_CE` 축에서 준 **0.61 ↔ 1.35 V** 의 **임피던스 축 대응물**.

**② 등가회로 파라미터의 실질 오차가 인쇄된 ± 의 한 자릿수 위다.**
`[도표]` **LPSCl\|LPSCl 셀의 `Ea(R₁)` = 45.5 ± 0.1 ↔ 같은 물질의 Table 1 벌크
40.5 ± 0.3** (`R₁` 은 정의상 벌크뿐). **5.0 kJ mol⁻¹ = 인쇄된 ± 의 12–50 배, 논문 무언급.**
`[인쇄]` 저자 스스로 **성형법(냉간↔열간)이 `Ea` 를 11 kJ mol⁻¹ 움직인다**고 적는다.
⇒ `[해석]` **적합 라벨을 점추정으로 보고하는 관행에 대한 야생 눈금**이다 —
우리 "폭과 함께 보고하라" 의 `assb` 판 증거.
같은 지면의 다른 산포 둘: **`P3` 가 셀마다 7 배**(4.8 Ω ↔ `[도표]` ≈35 Ω) ·
`[재현]` **CV 기울기 ↔ Nyquist 총합이 한 셀에서 1.6 배 어긋난다**(114 ↔ 183 Ω).

**③ 그런데 이 편이 Against 쪽에도 재료를 준다 — 두 가지, 그리고 둘 다 설계다.**
아래 §"Against" 의 마지막 두 항목(**계면 유무 대조군** · **면적-불변 채널 `Ea`**).

★★ `[해석]` **그래서 이 편의 위치는 "근거" 가 아니라 "바닥" 이다.** 우리가 계속
"라벨이 점추정이다" 라고 비판할 때, **그 점추정의 실제 폭이 얼마인지**를 이 편이
자기 지면 안에서 세 번(Ea · Li-In · P3) 보여 준다.

### ★★★★ 열일곱 번째 — **For 에 붙는, 계보에서 가장 이른 "상대극이 용량을 끊는" 실측** (2026-09-22, Chang et al. 2020 · 실험, 3전극 매립 In, **2019 접수**)

`raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md`.

**① 2전극이었다면 통째로 `LAM_PE` 로 읽혔을 손실이 음극으로 되돌려진다.**
첫 충전에서 `[인쇄]` **122 mAh g⁻¹ (54 %)** 이 날아가는데, 3전극이 그 원인을
**양극이 아니라 음극**에 배정하고 `[인쇄]` *"the cause of the capacity fade …
**could not have been elucidated without the three-electrode setup**"* 라고 적는다.
⇒ **17호가 2024년에 실증한 "겉보기 `LAM_PE` = 상대극" 을 5년 먼저, 명시적으로
피한 편**이고, 두 편의 기구는 **반대**다: 17호는 상대극 전위가 **위로 +0.7 V
지속 이동**(고갈), 20호는 상대극 전위가 **아래로 0 V 로 내려앉아 충전을 끊는다**.
**둘 다 2전극 OCV 에서는 양극 쪽 용량 손실로 보인다.**

**② 그 배정을 내가 그림에서 독립으로 확인했고, 저자보다 강하다.**
`[도표]`(Fig. 3b 픽셀 디지타이즈, ±30 mV) **1·2차 충전이 둘 다 음극 전위
≈0.019 / 0.043 V vs Li/Li⁺ 에서 끝나고 양극은 2.40 V** 에 머문다(신품 2.52–2.58 V)
⇒ **충전을 끊는 것은 음극이다.** 저자는 이 수치를 적지 않았다.
⚠ 반대로 `[재현]` **저자가 든 근거(음극 저항의 방전→충전 증가 275 Ω = 55 mV)는
격차의 ≈12 %(≈15 mAh g⁻¹)만 설명한다** — **결론은 옳고 논거는 다른 데 있다.**

**③ `i → 0` 처방의 반례가 계보에서 처음 나온다.**
`[재현]` 면적용량 **9.3 mAh cm⁻²**, 200 µA = **C/72**. **극저율에서도 첫 사이클의
54 % 가 날아간다** ⇒ *"저율 RPT 면 `η` 가 지워진다"* 는 처방이 **두꺼운 전극에서
성립하지 않는다**(한계가 율이 아니라 두께·접근 가능 분율에 걸려 있다).
17호가 "율을 낮추면 줄지만 0 이 되지 않는다" 로 연 축의 **반대쪽 끝 표본**이다.

**④ 그리고 손실의 일부는 프로토콜 산물이다.**
`[재현]` **1일 휴지 뒤 `V₁` = 2.095 V 로 컷오프(2.4 V)보다 310 mV 아래**로 이완한다
⇒ CC 전용·고정 컷오프가 자른 몫이 있다. ⇒ **`LAM_PE` 라벨이 프로토콜의 함수**라는
것을 완전지에서 보여 주는 첫 표본이고, 우리 합성 truth 에서 **CC-only ↔ CCCV 가
라벨을 얼마나 움직이는지**는 바로 측정 가능한 물음이다(아직 안 돌렸다).

**⑤ 곱 축퇴가 방정식 없이, 진단 → 처방 사이에서 나타난다.**
진단은 **동역학**(`R_ct`, *"sluggish alloying"*)인데 처방은 **면적**
(`[인쇄]` *"refine the particle size and optimize the morphology **for larger
interface areas**"*)이다. `[재현]` 음극은 **8.4배 과잉**이고 사이클된 DOD 가
**11.2 %** 인데 그 11 % 에서 음극 전위가 0.29 V 움직여 충전을 끊는다 ⇒
**극심한 분극(a)** 과 **접근 가능한 음극 분율 ≈1/9 이하(b)** 를 이 편의 관측
(`R₀`·`R_ct`·`R_p`)으로는 **가를 수 없다**. ⇒ `θ_NE` ↔ `j₀` 곱 축퇴의 **음극 판**.

**⑥ 그리고 "라벨의 바닥" 을 또 한 겹 내린다 — 이번엔 적합조차 아니다.**
`R₀`/`R_ct`/`R_p` 는 **Fig. 4 에 손으로 그은 점선과 주황색 외삽 직선**에서 읽은
값이고(`fit*` 0회, 전부 5 Ω 반올림), `[재현]` 음극 `R_p` = **12 mV = 패널 y 전폭의
1.2 %** 에서 읽혔다. ⇒ 19호가 보여 준 "점추정의 실제 폭" 아래에 **"추정이 아니라
작도"** 라는 층이 하나 더 있다.

### ★★★★ 열여덟 번째 — **For 에 붙는 음극 판 실측: OCV 가 같고 접근 가능 재고가 수 자릿수 다르다** (2026-09-23, Sedlmeier et al. 2023 · 실험, 미세 기준극 3전극 파우치, n = 3)

`raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md`.

**① 이 카드의 물음이 음극 Li 재고에서 구조 그대로 나타난다.** 접촉 손실은 "물질은 있는데
접근 불가" 이고, 우리는 그것이 OCV 에서 진짜 손실과 갈리는지 묻는다. 21호는 **같은 InLi 박**
(≈24 at%, 공칭 재고 ≈14 mAh cm⁻²)을 **어느 면을 분리막에 대느냐만** 바꿔 둘을 만든다:

| | InLi-(In) (Li 박이 뒷면) | InLi-(Li) (Li 박 면이 분리막 쪽) |
|---|---|---|
| 개방회로 | `[인쇄]` **0.62 V**, 28 일 < 3 mV | `[인쇄]` **0.62 V** |
| 0.2 mA cm⁻² 로 Li 빼기 | `[인쇄]` **9 초, 0.39 ± 0.21 µAh cm⁻²** | `[인쇄]` **15 h, 3.0 mAh cm⁻², 평탄** |
| 저주파 임피던스 | Warburg 유사 꼬리 | ≈1 Hz 반원 |

⇒ **OCV 채널로는 구별 불가, 펄스·임피던스로는 수 자릿수.** "물질이 있다" 와 "접근 가능하다" 가
**열역학 채널에서 같은 값을 준다**는 것의 음극 판 실측이다. `[인쇄]` Fig. 9 가 이것을 두 칸
표로 그린다 — **"✓ Potential ✗ Accessible Li reservoir"**.

**② 그리고 `LLI` 가 상대극을 거쳐 `LAM_PE` 서명으로 나타나는 기구가 문장으로 있다.**
`[인쇄]` *"in an NCM|In cell, the potential of the indium CE **cannot be assumed to stay invariant
at 0.62 V** vs Li⁺/Li towards the end of discharge … as this would depend on the **overall loss of
cyclable lithium**"*. ⇒ 17호(열네 번째)가 실증한 "겉보기 `LAM_PE` = 상대극" 의 **원인 쪽**이
`LLI` 라는 것을 17호보다 앞서 인쇄한다(17호가 이 편을 ref 21 로 인용한다).
`[추론]` **상대극 재고가 없거나 못 쓰는 조립에서는 `LLI` 가 끝 절단(= `LAM_PE` 서명)으로 새어 든다.**

**③ ⚠ 이 편이 주지 않는 것.** 양극이 없고, 열화가 없고(신품·무사이클), 가르는 대상이
**접촉 면적이 아니라 음극 계면의 Li 상태**다. **`θ` 는 21/21 편 0 이다.** 가져올 수 있는 것은
**관측의 형태**(짧은 펄스 전하 + 저주파 부류)이고, 양극은 OCP 가 기울어 있어 그대로 옮겨지지
않는다(`[추론]`).

### ★★★★ 열아홉 번째 — **For 에 붙는 원전: "접촉 손실 → 용량 손실" 은 처음부터 서술이었고, 용량 몫은 한 번도 정해지지 않았다** (2026-09-23, Koerver et al. 2017 · 실험, EIS + XPS + SEM, 2전극 · LTO 대조)

`raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md`. 상세는 [[assb-interphase-vs-contact-loss-attribution]].

**① 원전이 두 기구를 가르지 않는다.** 첫 사이클 손실(176 → 124 mAh g⁻¹)은 `[인쇄]` "a **combination** of changes in the chemical
composition at the interface (oxidation) **as well as** contraction of the NCM particles" — 분할 숫자 0. 접촉 손실 쪽 문장은 전부
`[인쇄]` "expected" · "suspect" · "suggests" 이고, 치수·분율 0 이다.

**② 원전 숫자로 짠 손실 예산** (`[재현]`): 계면층의 **패러데이 몫** ≈4 %(`[인쇄]` "≈1 % of the SE", 양극 SE 기준) · **옴 몫**
≲3 %(`[도표]` 방전 무릎 ≈12 mAh g⁻¹ V⁻¹ × 25–100 mV) ⇒ **≳85 % 미배정.** 그 안에 `θ`(접촉·절연 고립) · `η(i)`(`[인쇄]` 0.25 C 에서
이미 66 mAh g⁻¹) · **상대극 고갈**이 섞여 있다 — **이 셀의 OCV 적합은 셋을 하나의 `LAM_PE`(또는 `LLI`)로 보고했을 것이다**(`[추론]`).

**③ 그리고 17호 경로가 여기서도 열려 있다.** `[인쇄]` "Upon further discharge, **In is fully delithiated**"; `[도표]` 방전 끝
`C_SE/Anode` ≈90 배 붕괴(LTO 대조도 ≈100 배) = 상대극이 평탄을 떠난 서명. 두 상대극 모두 **Li 없이 조립** — 방전 끝 재고비
`[재현]` ≈1.4. **대조군이 함정을 공유한다.**

**④ ⚠ 이 편이 주지 않는 것.** `θ` 값 · 부피 변화 % · 3전극 · 0.1 C 아래 율 · 첫 방전 후 SEM(틈이 닫히는지).

### ★★★ 스무 번째 — **For 에 붙는 operando 실측: 구조 채널도 가중평균하면 `θ` 와 `η` 를 OCV 처럼 합친다** (2026-09-23, Stavola et al. 2023 · 실험, operando 깊이 분해 EDXRD + 차단 셀 EIS + COMSOL)

`raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md`. 상세는 [[assb-tortuosity-factor-effective-conductivity-split]] · [[assb-apparent-capacity-decomposition]] §24호.

**① 두께 방향 구배의 몸통은 `η(z)` 다.** 110 µm NMC111–LPSC 에서 C/10 충전 1 중간점 `[인쇄]` Δx 0.145–0.338(가역 용량의 29–67 %). 지연된 조각도 반응파로 따라잡고,
40 % 셀 분리막 조각은 방전 중에도 1.2 h 탈리튬한다(두 경로가 살아 있는 입자). **OCV 적합이라면 이 지연 중 컷오프에 걸린 몫을 율 의존 겉보기 `LAM_PE` 로 보고했을 것이다**(`[추론]`).

**② 그러나 `θ` 형 모집단이 섞여 있고, 측정이 둘을 합친다.** `[도표]` 80 % 셀 집전체 쪽 조각 6 의 (003) 한 봉우리가 충전 1 내내 pristine 근처 — 22호의 "불활성" 모집단.
원전은 두 봉우리를 **높이 가중평균**(식 S14)으로 한 `x` 로 만든다. ⇒ **깊이 분해 회절도 모집단을 풀지 않으면 `θ`·`η` 분리가 사라진다** — OCV 가 못 가르는 것을 구조 채널이
가르려면 **scale 분율**을 써야 한다(22호 방식).

**③ 첫 사이클 비가역 ≈0.2 Δx(≈56 mAh g⁻¹)는 깊이에 균일** (`[재현]` Fig. 3b–e) — 두께 수송이 아니다. 입자 척도(고리튬 쪽 확산 · 계면층 · 동결 고립) ↔ 상대극(In–Li 조성 미기재)이
안 갈린다. 코팅 쌍이 이것을 **≈14 %** 만 줄인다(`[도표]`, n = 1 씩).

**④ ⚠ 이 편이 주지 않는 것.** 열화(2 사이클) · `θ(N)` · 기준극 · 율 스윕 · 공극률 측정 · 셀 간 산포 · OCP.

### ★★★ 스물한 번째 — **For 에 붙는 요인 설계: 압력은 두 미세구조를 같이 깎고, 2전극 감쇠의 전압 쪽은 저자 자신의 적합에서 대부분 Li 음극이다** (2026-09-23, Zhou et al. 2025 · 실험, 2전극 Li 금속 + EIS/DRT + DEM, 운전 압력 3 점 × SE 입도 2)

`raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md`. 상세는 [[assb-stack-pressure-operating-window]] §25호 · [[assb-lampe-contact-product-degeneracy]] §아홉 번째 적용 ·
[[composite-cathode-percolation-utilization]] §25호.

**① 계산된 `θ` 가 첫 충전과 맞지 않는다.** DEM 이용률(2 % 겹침 기준) coarse 83 % ↔ fine 100 % 이면 coarse 는 첫 **충전**부터 ≈17 % 적어야 한다. `[재현]` Fig. 2c 벡터 판독으로 30 · 10 MPa 의
첫 충전 비는 **1.03** — 차이는 **방전 쪽**(첫 사이클 비가역 42.6 ↔ 19.9 mAh g⁻¹)에 있다. **OCV 적합이라면 이 방전 쪽 손해를 겉보기 `LAM_PE` 로 보고했을 것이고, 원전은 그것을 "이용률" 로 불렀다** — 이름표 둘이 같은 자리에 붙는다(`[추론]`).

**② 압력 손해의 초기분은 공통 모드다.** 30 → 2 MPa 2 사이클 방전 손해 coarse −26.5 ↔ fine −30.7 mAh g⁻¹, 1 → 2 사이클 낙차 −12.7 ↔ −13.1 — **미세구조와 무관**하다.
그리고 `[도표]` S19 에서 1 사이클 뒤 `R_NCM`·`R_anode` 도 두 조성이 같이 ×1.7–1.9 ⇒ 초기 압력 손해를 양극 접촉 손실로 배정할 근거가 없다(두 셀이 공유하는 Li 음극 · 분리막이 후보).

**③ 감쇠의 전압 쪽은 대부분 Li 음극이다(저자 적합 기준).** 2 MPa coarse `ΔR_anode` ≈2020 ↔ `ΔR_NCM` ≈535 Ω, `[재현]` IR ≈0.30 V ↔ 방전 전압 하강 ≈0.30–0.37 V(벡터). **17호 함정이 Li 금속 저압에서 반복된다** —
평탄 OCP 는 기준 가정을 열역학적으로만 지킨다.

**④ ⚠ 이 편이 주지 않는 것.** 측정 접촉 분율 · `θ(N)` · `C`(CPE) · 기준극 · 셀 간 산포(암묵적으로 ≈20 %) · 압력 장치. 그리고 **Fig. 3 의 EIS/DRT 일부가 조건 이름을 바꿔 단 같은 곡선**이라(`[재현]` ≤0.8 Ω)
2 MPa 의 "1 사이클 뒤" 기준점을 쓸 수 없다.

### ★★★ 스물두 번째 — **For 에 붙는 모델 쪽 계산: 방전곡선 적합은 몸통의 평행 이동 일곱 개를 한 조합으로 보고, 용량 스케일과 수송을 한 조합으로 본다 — 저자 자신의 스윕이 그렸다** (2026-09-23, Iwakiri et al. 2024 · ⚠ 모델 편, 빌린 박막 데이터 4 율)

`raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md`. 상세는 [[assb-sensitivity-sweep-vs-identifiability]] · [[assb-lampe-contact-product-degeneracy]] §열 번째 적용.

**① 용량 스케일 ↔ 수송.** `[재현]` 인쇄된 식 (28)–(32) 를 `x`(정규화 용량) 좌표로 쓰면 양극 부분계는 `D_M⊕·a_max/I` 한 조합만 본다 — `[도표]` Fig. 3(확산 ×K) ≡ Fig. 15(`a_max` ×K, 전류 고정),
열한 곡선 끝 `x` 일치. **`a_max` 는 이 모델에서 활물질 양의 자리**(우리 `LAM_PE` 의 모델 짝)이고, 그것이 **확산과 같은 곡선족**을 낸다 ⇒ 정규화된 방전곡선에서 "활물질이 줄었다" 와
"수송이 느려졌다" 는 같은 모양이다(`[추론]` — 대칭을 깨는 것은 `I⁺₀ ∝ a_max` 하나와 절대 용량 축).

**② 몸통은 한 수로 보인다.** 전해질 셋 · `k₁` · `k₂` · `a_max`(C 고정) 스윕이 전부 **평행 이동**(끝 `x` 불변) — 한 율에서 과전압의 합만 보인다. 접촉 면적은 이 모델에서 `k¹_s` 로 들어가므로
(면적 `A` 기하 고정), **접촉 손실의 면적 몫은 전하이동 · 전해질 · 상대극 동역학과 같은 모양**이다(`[추론]`).

**③ ⚠ 이 편이 주지 않는 것.** 실험 · 열화 · 접촉 · 복합양극 — 전부 0. 이것은 **모델 안의 구조**이고 박막(입자 없음)이다. 9호 곱(`A_eff·ε_p/R_s`)의 **다른 모양**이지 같은 식이 아니다.

### ★★★★ 스물세 번째 — **For 에 붙는 모델 대 모델 계산: 참값 모델의 "연결만 끊긴 활물질" 은 축약 모델과 대조하면 용량 오프셋이 되고, 축약 모델에서 그 자리는 용량 손잡이 하나다** (2026-09-23, Sinzig et al. 2024 · ⚠ 모델 편, 실험 0)

`raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md`. 상세는 [[assb-sensitivity-sweep-vs-identifiability]] §27호 · [[assb-lampe-contact-product-degeneracy]] §27호.

**① 물질은 그대로, 쓰이지 않는다 — 3차원으로.** `[인쇄]` 생성 미세구조의 utilization `u = 0.93`, `[인쇄]` "the concentration in the non-connected particles remains at its initial value"(Fig. 4b 청색 입자). 카드 질문의 문장 그대로다.

**② 그것이 축약 모델 앞에서는 용량 오프셋이다.** `[재현]` SOC 가 모든 입자에 대해 적분되므로 resolved `SOC_end ≥ 1 − u = 0.07`. 벡터 좌표: Fig. 11a 큰 `κ` 에서 resolved 0.111 ↔ P2D 0.043(차 0.068; 바닥을 빼면 0.044 ↔ 0.043),
Fig. 7 150 점 평균 차 0.072 · resolved 최소 0.100(0/150 이 0.07 아래). 저자는 이 오프셋을 **"insufficient homogenization strategy"** 로 배정한다 — **다른 이름으로 읽혔다.**

**③ 축약 모델에서 그 자리는 `LAM_PE` 의 자리다.** `[인쇄]` "The utilization could be included within the P2D model by artificially reducing the available capacity of the cathode by a modification of the specific interface area `A_el-c`" —
**용량과 면적을 함께 깎는 손잡이 하나**. `[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters" ⇒ P2D 를 보정하면 접촉 손실은 **용량 손실로 흡수**된다.

**④ ⚠ 이 편이 주지 않는 것.** 실험 · 열화 · 사이클에 따른 `u(N)` — 전부 0. ②의 대응은 **우리 `[재현]`** 이고, 저자 쪽 계산(Fig. 3b "dashed line")은 그림에 없다. 연결 손실은 **전자** 연결(1호 `θ` 와 같은 종류)이지 CAM–SE 이온 접촉이 아니다.

### ★★★ 스물네 번째 — **For 에 붙는 묶음 대수: SPM 에서 입자 통째 비연결은 LAM 과 같은 파라미터다 — 식별성 원전의 식 위에서** (2026-09-23, Bizeray et al. 2019 · ⚠ **액체셀**, ASSB 아님)

`raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md`. 상세는 [[spm-grouped-parameter-identifiability]].

**① 원전이 인쇄한 것.** SPM 의 14 물리 파라미터는 전극마다 `τ_d = R²/D` · `τ_k = R/(2k√c_e)` · `Q_th = ±ε δ c_max F A` **여섯 묶음**으로만 보인다(`[인쇄]` 식 17–19 · 26–27, "only six independent parameters").
선형화 EIS 에서는 두 전극 동역학이 `R_ct` 하나로 합쳐지고(`[인쇄]` "infinite number of pairs"), `Q_th` 는 `β = dU/dQ` 안으로 들어가 **기준극으로 재는 입력**이 된다 — 식별되는 것은 `(τ_d⁺, τ_d⁻, R_ct)` 셋.

**② 카드 물음을 올리면 (`[해석]`).** `ε` 는 `Q_th` 에만 있다 ⇒ 입자 통째 비연결(`ε → uε`)은 **진짜 LAM(`ε ↓`)과 같은 파라미터의 같은 방향** — 근사적 축퇴가 아니라 항등이다. 표면 일부 접촉 손실(`a_eff`)은 `k·A_eff` 곱으로 `τ_k` 묶음에 들어가 `R_ct` → `R0`(옴·접촉·피막)로 사라진다.
27호의 오프셋 `1 − u`(P2D `A_el-c` 용량 손잡이)와 **같은 자리**이고, 원전 자신도 시간 영역에서 그 자리를 **사후 보정**(양극 OCV 기울기 ×0.78 ≡ `Q_th⁺` ×1.28)으로 돌렸다.

**③ ⚠ 이 편이 주지 않는 것.** ASSB · 접촉 · 열화 — 전부 0. ②는 **원문 명제가 아니라 우리 대수**다. SPM 은 전해질(ASSB 에서는 고체전해질) 수송을 무시한다.

### ★★★ 스물다섯 번째 — **For 에 붙는 ASSB 실측 경계: 용량 스케일은 준평형 데이터가 있어야 동역학과 갈린다 — 저자 자신의 공분산 진단이 그 경계를 인쇄했다** (2026-09-23, Yanev et al. 2024 · 실험, 2전극 CA + 대칭 셀 EIS/TLM + GITT, 14 복합체, 신품)

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md`.

**① 원전이 인쇄한 것.** CA 방전 한 번의 과도 전류를 `R(t) = I/∫I dt` 로 바꿔 `Q(R) = Q_M/(1+2(Rα)ⁿ)` 로 적합하고, `Q_M` 을 `[인쇄]` "the degree of electronically percolated AM, referred to as AM utilization" 으로 읽는다 — **용량 결손 ≡ 전자 비연결**(신품이라 LAM 항 없음, 물질 고유 차이는 같은 분말의 LIB 반쪽전지 193 · 213 mAh g⁻¹ 로 뗀다).
그리고 저율 평탄이 측정 창(0.02 C) 밖인 sc90 에서 `[인쇄]` "not enough information … to accurately fit the Q_M and α … high dependencies close to unity in Table S2."

**② 카드 물음으로 (`[해석]`).** `[재현]` 식 (2) 의 고율 극한은 `(Q_M/2)(Rα)⁻ⁿ` — 평탄이 없으면 데이터는 **`Q_M·α⁻ⁿ` 한 조합**만 본다. `Q_M` 은 `θ`·LAM·물질 용량의 합이므로, **ASSB 의 용량 스케일은 준평형(무한 저율) 데이터 없이는 `η` 와 갈리지 않는다** — 카드가 OCV 에 거는 전제의 실측 경계다.
그 경계는 한 셀만의 일이 아니다: `[도표]` **어느 셀의 CA 곡선도 0.02 C 에서 평탄하지 않고**, `Q_M` 은 평탄이 보이는 셀에서 실측보다 **낮고**(gran51 ≈185 ↔ 194) 안 보이는 셀에서 **높다**(sc84 ≈236 ↔ 177, LIB 213 초과). 저자의 이용률 결론 중 가장 센 것이 후자에서 나왔다.
또 접촉 손실의 **두 종류**를 두 칸에 둔다 — 전자 비연결 → 용량(`Q_M`) · 이온 피복 → 동역학(`φ`, GITT). 28호 묶음 표의 두 줄(입자 통째 비연결 → `Q_th` · 표면 일부 접촉 → `R_ct`)과 같은 갈림이고, 29호는 표면 쪽을 `R_ct` 가 아니라 **확산 묶음의 면적**으로 읽는다. 균열은 두 칸에 **동시에** 배정되고 몫은 안 갈린다.

**③ ⚠ 이 편이 주지 않는 것.** 열화(형성 2 사이클) · `LAM_PE` · OCV 곡선 · SI(진단 수치). `φ` 는 **측정이 아니라 `D_true` 공통 · LIB 100 % 가정 위의 비**이고, 이 편의 "확산성 한계" 와 "작은 접촉 면적" 은 `φ ≡ √(D_app/D_LIB)` 로 **같은 숫자**다.

### ★★ 스물여섯 번째 — **For 에 붙는 새 자리: Li 금속 반쪽전지의 방향 비대칭은 상대극과 양극이 합쳐진 양이고, 2전극은 그것을 양극에 배정한다** (2026-09-23, Park 2024 · 실험, 2전극 코인셀, LATP 펠릿 + 슬러리 양극)

`raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md`.

**① 원전이 인쇄한 것.** 주사율 CV 의 멱법칙 b 와 Randles–Ševčík `D` 가 산화 ↔ 환원에서 다르다는 것을 `[인쇄]` "space charge layers and high interfacial resistance at the **LATP/NMC111** interface" 와 NMC111 의 "bulk diffusion" 에 배정한다. 셀은 2전극이고 `[인쇄]` "Li-metal served as both the **reference** and counter electrodes".
**② 카드 물음으로 (`[해석]`).** 액체셀 반쪽전지의 관행(Li 과잉 → 상대극 무시)이 ASSB 에서 깨지는 **새 자리**다 — 상대극 Li\|SE 계면은 석출(충전) ↔ 박리(방전)에서 **다른 과정**이라, 2전극의 방향 비대칭은 두 전극 비대칭의 합이다. `[재현]` 이 편 자기 그림 두 장이 그 크기를 준다: 대칭셀 호로 어림한 직렬 몫 ≈0.5–0.86 kΩ ↔ CV 봉우리 이동 기울기 ≈0.54–0.65 kΩ(같은 자릿수). 카드의 3항 분해로 옮기면 **상대극의 방향 의존 저항이 양극 `η` 의 방향 비대칭으로 오배정**된다 — 17호("겉보기 `LAM_PE` 가 상대극") · 25호("감쇠 전압의 ≈80 % 가 Li 계면") 에 이은 **세 번째 형태, 이번에는 방향 축**.
그리고 이 편은 **액체 대조로 곱의 한 인자를 고른다** — Randles–Ševčík `D_app ∝ 1/(A·C)²` 에서 고체/액체 10.9 배를 전부 `D` 에 배정(29호는 같은 구조의 차이를 면적에 배정).
**③ ⚠ 이 편이 주지 않는 것.** 방향별 분극 측정 · 전극 분해 · 오차 · 반복. 그리고 **비대칭의 부호가 자기 그림과 반대**(`[재현]` b 산화 ≈0.58 ↔ 인쇄 0.76)라, 이 편의 서사 어느 쪽도 근거로 쓰지 않는다 — 쓰는 것은 **셀 설계가 만드는 오배정 경로**뿐이다.

### ★★ 스물일곱 번째 — **For 에 붙는 식 수준 구조: 확산계수 측정은 입자 통째 비연결에 눈멀고, 표면 피복에 제곱으로 민감하다 — 그리고 그 측정은 면적을 입력으로 받는다** (2026-09-23, Chien et al. 2023 · ⚠ **액체셀**, 3전극 · ICI 방법 원전)

`raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md`.

**① 원전이 인쇄한 것.** ICI(정전류 중 짧은 차단)의 `ΔE = −IR − Ik√Δt` 에서 `R`·`k` 를 뽑고, GITT 와 같은 식 `D = (4/π)(V/A)²((ΔE_OC/Δt_I)/(Ik))²` 로 `D` 를 낸다. `A` 는 BET 상수이고 `[인쇄]` "The BET-surface area may differ from the electrochemically active surface area. However, … both of which are equally affected by this factor."
**② 카드 물음으로 (`[해석]`).** 식 19 의 관측 비 `k·I/(dE_OC/dt_I) ∝ (V/A)/√D` 에서 **활성 분율 `u`(입자 통째 비연결)는 약분되고**, 표면 피복 `φ` 는 `D_app = φ²D` 로 남는다. ⇒ 카드의 두 접촉 손실은 **다른 축으로 간다** — 통째 비연결은 LAM 과 같이 **용량 축**(28호 묶음 `Q_th`), 표면 피복은 **`D_app` 축**. 29호가 `Q_M` · `φ` 로 두 칸에 둔 갈림의 식 수준 근거다. 그러나 `D_app` 축 안에서 `φ` 와 `D` 는 **곱**으로 남는다 — 이 편은 면적을 상수로 넣어 곱을 **배정**했다(29호 면적 · 30호 `D` 에 이은 세 번째 배정, 첫 고지된 배정).
가를 후보는 같은 차단 안에 있다 — 표면형 `R ∝ 1/A` · `k ∝ 1/(A√D)` 라 **`R/k` 에서 면적이 약분된다**. 이 편은 그 비를 만들지 않았다.
**③ ⚠ 이 편이 주지 않는 것.** 고체셀 · 접촉 · 사이클 뒤 면적 측정 · 사이클 추적의 `k`. 그리고 이 편의 사이클 `D` 감소는 **가정(단상 고용체)이 자기 XRD(두 상)로 깨진 구간**의 값이다 — 근거로 쓰는 것은 **식의 구조**뿐이다.

### ★★ 스물여덟 번째 — **For 도 Against 도 아닌 계보 정정: "접촉 손실 ↔ 보통 노화" 진단 요구의 출처는 8호 자신이다** (2026-09-23, Biçer et al. 2025 · ⚠ Review, 1차 측정 0)

`raw/papers/bicer2025_ssb-chemistry-bms-thermal-assembly-critical-review.md`.

**① 원전이 인쇄한 것.** SSB BMS 요구: `[인쇄]` "BMS designs for SSBs should integrate pressure sensors and feedback control systems to monitor and maintain optimal stack pressure" · "impedance-based diagnostics (e.g., EIS) ... tracking dynamic internal resistance changes" · Table 6 "SoH models must be tailored to SSB-specific degradation (e.g., interface degradation)". 접촉 불량의 결과는 `[인쇄]` "increased impedance, mechanical delamination, and eventual cell failure" — **용량 몫 0**, `contact loss` 0 회.
**② 카드 물음으로 (`[해석]`).** 8호가 이 편에 매단 "diagnostics capable of distinguishing contact loss from ordinary electrochemical aging" 은 **이 편에 없다** — 카드 물음의 문헌상 요구 측 첫 인쇄는 8호다. 이 편의 체계에서 접촉 손실은 **저항 축의 현상**이라 `LAM_PE` 와 구별할 물음이 애초에 생기지 않는다(분류 체계 네 번째 표본). 그리고 OCV–SoC 를 `[인쇄]` "well-established linear" 로 두는 추정 어휘는 **OCV 적합의 식별성 자체를 물을 자리가 없다**.
**③ ⚠ 이 편이 주지 않는 것.** 측정 · 압력 값 · 온도 의존(`Arrhenius` 0) · 모드 어휘(`LLI`·`LAM` 0) · 인용 사슬(제목 기준 불일치 12 건) — **칸을 움직일 근거로 쓰지 않는다.**

### ★★ 스물아홉 번째 — **For 도 Against 도 아닌 종합 층 표본: "접촉 손실 → 사이클 감쇠 → 압력으로 재활성" 이 원전 없이 만들어지는 자리** (2026-09-23, Zhang et al. 2025 · ⚠ Review, 1차 측정 0)

`raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md`.

**① 원전이 인쇄한 것.** §3.2.1 `[인쇄]` "the active material particles lose close contact with the SSEs due to the volume changes of NCM-811 ... **This loss of contact leads to a decrease in electrochemical activity in subsequent cycles. Continuous application of external pressure** has been identified as an effective method to maintain contact ... thereby ensuring the **reactivation** of these materials" — 앞 문장의 인용은 [57](= 23호 Koerver 2017), 재활성 문장은 인용 번호 없음.
**② 카드 물음으로 (`[해석]`).** 이 문단은 카드의 틀(접촉 손실 = 물질은 그대로인 **가역적 비활성**, `LAM_PE` 와 다르다)에 **가장 가까운 종합 층 표현**이다 — 분류 체계 다섯 번째 표본(12호 LAM ⊃ 접촉 · 13호 미배정 · 15호 어휘 미도입 · 32호 접촉 = 임피던스 · **33호 접촉 = 압력으로 되돌릴 수 있는 활성 감소**). 그러나 23호 원전은 접촉 손실을 **첫 충전에만**, 이후 감쇠를 **계면상**에 배정했고 압력을 바꾸지 않았다. 우리 위키에서 재가압 → `θ_AM` 되돌림을 실측한 4호(Shi 2020)는 이 편 참고문헌에 **없다**. ⇒ 종합 층에서 카드의 전제가 **근거 없이 참으로 인쇄**된다 — 카드가 **증명 없이 받아들이면 안 되는 형태**의 표본이다.
**③ ⚠ 이 편이 주지 않는 것.** `θ` · 접촉 분율 · 압력 스윕 × 사이클 · 모드 어휘(`LLI`·`LAM`·`fit*` 0). **칸을 움직일 근거로 쓰지 않는다.**

### ★★ 서른 번째 — **For 도 Against 도 아닌 도구 층 표본: 식별성을 입력 설계로 사겠다는 처방, 그리고 그 처방이 우리 폭 측정기의 짝이 되는 조건** (2026-09-23, Liang et al. 2026 · ⚠ Comment, 1차 측정 0, ASSB 0)

`raw/papers/liang2026_pulse-excitation-active-bms-comment.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "Under passive conditions … key electrochemical processes remain **weakly observable or even unidentifiable**" · "incremental capacity (IC) and differential voltage (DV) curves **lack sufficient information density**" · "Adaptive pulse protocols should be numerically optimized, utilizing criteria such as the **FIM or D-optimality** … This optimization ensures **maximum parameter identifiability** across various chemistries and aging stages" · 불변량 예시 "**active material stoichiometric limits**".
**② 카드 물음으로 (`[해석]`).** 카드의 곱(`A_eff·j₀`)은 **구조적** 비식별이다 — 출력이 곱으로만 의존하면 모든 입력에서 FIM 이 특이해 D-optimality 는 0 이고, 펄스 설계로 풀리지 않는다. 곱을 가르는 것은 **모델에 곱과 다르게 반응하는 항**(`C_dl ∝ A`, √t 항 `k ∝ 1/(A√D)`)과 **그 항이 보이는 대역의 샘플링**이다. 그 조건이 서면 한 펄스의 이완이 처방 1·4단계와 `R/k` 를 동시에 준다. 반대로 이 편의 권고 경로(재구성 · 불변 학습)는 그 입력을 지운다. 그리고 OED 는 국소(FIM)라 **설계 뒤 전역 폭**을 다시 재야 한다 — 우리 근최적 폭 측정이 OED 의 사후 검증 자리에 선다(큐의 "역방향" 을 짝으로 읽는 조건).
**③ ⚠ 이 편이 주지 않는 것.** 데이터 · 펄스 사양 · 샘플링 · 셀 화학 · 모드 어휘(`LLI`·`LAM` 0) · 전고체(`solid-state` 0 · `pressure` 0). **칸을 움직일 근거로 쓰지 않는다.**

### ★★ 서른한 번째 — **For 도 Against 도 아닌 도구 층 표본: 불확실성을 제대로 재는 파이프라인이 모드 축퇴에는 눈멀었다는 것을 구조로 보이는 편** (2026-09-23, Roman et al. 2021 · ⚠ ML 방법 논문, 1차 실험 0, 액체 셀, ASSB 0)

`raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "This work focuses on the battery's **capacity** as its health indicator" · "Uncertainty is quantified on the basis of **calibration error** and an adapted accuracy measure, the α−β accuracy zone" · "we perform **re-calibration using isotonic regression**" · "the calibration dataset is neither used in training nor testing" · "any algorithm must undergo uncertainty quantification checks before deployment". 특징의 물리 귀속은 SI Note 1 에서 **"hypothesis"**(음극 분극 · 리튬 도금).
**② 카드 물음으로 (`[해석]`).** 이 편은 8호가 요구한 생산 추정기 3 요소(estimate + calibrated uncertainty + validity flag) 중 **앞의 둘을 채운 원전**이다. 그러나 목표가 스칼라라서, 같은 용량을 내는 두 기구(접촉 손실 ↔ `LAM_PE`, LLI ↔ LAM)는 이 편에게 **같은 정답**이다. 예측 구간은 축퇴 방향의 폭을 볼 수 없다 — 그 방향에서 예측이 변하지 않기 때문이다. 그리고 선택 단계는 **용량과 직교하는 채널**(저항 · 용량성)을 버리도록 설계돼 있어, 분리의 재료가 입력에서 먼저 사라진다(유일한 저항 채널이 세 그룹 모두 탈락 — `[인쇄]` SI Tables 3–5). ⇒ **"보정된 SOH 구간이 좁다" 는 모드 분해가 정해졌다는 근거가 될 수 없다** — 이 카드가 BMS 쪽 성과를 옮겨 올 때의 경계다.
**③ ⚠ 이 편이 주지 않는 것.** 모드 어휘(`LLI` · `LAM` · `degradation mode` 0) · 전극 귀속 검사 · 온도 · 데이터셋 밖 시험 · 셀별 결과 분포 · 전고체(`pressure` 0). **칸을 움직일 근거로 쓰지 않는다.**

### ★★ 서른두 번째 — **For 도 Against 도 아닌 도구 층 표본: 확률적 ML 종설이 불확실성과 모드를 한 문서에 두고, 한 문장에서 만나게 하지 않는다** (2026-09-23, Thelen et al. 2024 · ⚠ Review, 1차 측정 0, 액체셀 중심, ASSB 0)

`raw/papers/thelen2024_probabilistic-ml-battery-health-review.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "'uncertainty' refers to the **predictive uncertainty** of an ML model … for a training/test sample point" · "Epistemic uncertainty … is thus **reducible** … Model parameter uncertainty can be reduced by collecting more training data" · "As the sample size approaches infinity, the confidence interval **collapses to the true value**" · 모드 진단: "the degradation modes could be **accurately quantified** by examining full-cell OCV data"(Birkl 요약) · "the degradation modes are **inherently correlated**, and these correlations can be exploited to improve diagnostic accuracy"(Ruan 요약) · BNN: "a mean-field approach **cannot capture parameter correlations** and tends to under-predict the uncertainty" · "This would require the probing … of **posterior results (not just posterior-predictive results** and not just looking at RMSE)".
**② 카드 물음으로 (`[해석]`).** 이 편의 분류(aleatory 비가역 · epistemic 가역)에는 **구조적 비식별**의 칸이 없다 — 곱 `A_eff·ε_p/R_s` 나 LLI ↔ LAM 조합은 같은 종류의 데이터를 무한히 모아도 사후가 점이 아니라 **능선**으로 수렴한다. 이 분류로 읽으면 곱 방향의 폭은 "데이터 부족(epistemic)" 으로 오독된다(34호 "식별성을 입력 설계로 산다" 와 같은 방향). 그리고 확률적 모드 진단이 나오더라도 두 경로가 곱 방향의 폭을 **지울 수 있다**: ① **평균장 VI**(이 편이 인쇄한 대로 상관을 못 잡고 불확실성을 줄인다) ② **상관된 학습 사전**(Ruan — 데이터가 못 가르는 방향을 사전이 정해 정확도를 올린다; 분포 밖 셀에서는 그 정확도가 사전의 몫이었음이 드러난다). ⇒ **이 카드가 확률적 진단 문헌을 옮길 때 먼저 볼 것은 폭의 크기가 아니라 공분산(능선)을 보고했는지다.**
**③ ⚠ 이 편이 주지 않는 것.** 확률적 모드 진단 원전(0/13) · 물리 파라미터 사후 · 식별성 어휘(`identifiab` 0) · 접촉 손실의 모드 배정(Fig. 3 연결선 0) · 전고체(`MPa` 0). **칸을 움직일 근거로 쓰지 않는다.** 후속 1 순위는 이 편이 재인용한 **Gasper 2021**(부트스트랩 파라미터 분포 — "too many fittable parameters")과 이 편 저자의 **Thelen 2022**(모드 진단 원전, 확률 출력 여부 미확인).

### ★★★ 서른세 번째 — **For 에 붙는 식 수준 구조 (원형 모델): 표면 접촉 손실은 `LAM_PE` 가 아니라 반응 속도 상수의 쌍둥이이고, 입자 통째 비연결은 `LAM_PE` 말고 자리가 없다** (2026-09-23, Li et al. 2024 · ⚠ 모델 + 신품 실험, 노화 0)

`raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md`.

**① 원전이 인쇄한 것.** `[인쇄]` 식 (8) `j^p_ct = (I − I^p_dl)/(A^p_eff·a_{s,p}·A·L_p)` · 식 (9) `a_{s,p} = 3ε_p/R_s` · 식 (15) 표면 플럭스 `−I/(a_{s,p}AL_pF)`(`A_eff` 없음) · 가정 "The effective contact area is considered. However, when the concentration of lithium-ion is calculated, assuming a uniform current density distribution on the surface of the active material" · Fig. 11 "the influence of the effective contact area on cell performance exhibits limited significance … This outcome is attributed to the model's assumption of uniform current distribution across the surface". Table 1 `A^p_eff` 0.4938 · `A^n_eff` 0.4095 — **각주(측정 방법) 없음**.
**② 카드 물음으로 (`[해석]`).** 이 모델 가족(9호 포함)에서 접촉 손실이 들어갈 자리는 **둘**이다: `A_eff`(BV 분모 — 용량 · 확산에 없고 `k_p` 와 정확한 곱) 와 `ε_p`(용량 · 확산 · 동역학 — `LAM_PE` 그 자체). ⇒ 카드 전제("접촉 손실은 용량이 준 것처럼 보인다")를 이 모델에 넣으면 `ε_p` 로 가야 하고, 그 순간 `LAM_PE` 와 **같은 파라미터**다 — **OCV 적합이 가를 수 없다는 것이 결과가 아니라 모델의 정의**가 된다. `A_eff` 로 넣으면 OCV 에 아예 안 보이고 `k_p`(계면 화학)와 가를 수 없다. 어느 쪽이든 "가를 정보는 모델 밖 관측에 있다" 는 For 쪽 결론을 **식으로** 다시 얻는다(28호 묶음 대수의 ASSB 원형판).
**③ ⚠ 이 편이 주지 않는 것.** 노화 데이터(0) · `θ` 의 측정 · 식별성 계산 · `A_eff` 의 출처. **칸을 움직일 근거로 쓰지 않는다.** 그리고 이 구조는 **이 편 · 9호 두 편의 식**에 관한 것이다 — `θ` 를 따로 가진 ASSB 모델이 있을 수 있다(미확인).

### ★★★★ 서른네 번째 — **For 에 붙는 실측 원전: "접촉 손실을 정량한" 원전이 한 것은 OCV 기반 `LAM_PE` 측정에 기구 이름을 붙인 것이다** (2026-09-23, Conforto et al. 2021 · 40 사이클 × 4 조건 · 조건당 셀 1 개)

`raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md`.

**① 원전이 인쇄한 것.** `[인쇄]` 식 (7) `m_act = Q_meas/q_act` — `q_act` 는 방전 전후 이완 OCP 를 액체셀 기준 OCP–x 에 대 얻은 `Δx` 에서 · "the equilibrium OCP of a cell with an NCM cathode (and an In/InLi anode **with fixed potential**) follows a well determined OCP function vs x" · "NCM particles that are disconnected from the electronic network **cannot contribute to the OCP any longer and can be considered inactive**" · "**We suggest** that the chemo-mechanical evolution … is the main cause" · 상전이형 손실은 "can be considered as low"(ref 14, 액체셀 TEM "2 nm … after 20 cycles"). `[도표]` Fig. 6 N = 40: PC ≈0.63/0.62 · SC ≈0.91/0.90.
**② 카드 물음으로 (`[해석]`).** 평탄 상대극 + Li 과잉(`[재현]` ×2.75)에서 `m_act` 는 양극 용량 스케일 — 우리 α 적합의 `α_PE` — 를 두 점으로 읽은 값이다. 그 설계가 우리 degeneracy(음극 곡선 · 오프셋)를 지워 α 는 식별되지만, **카드의 두 항(`ε_p` · `θ`)은 α 안에서 곱으로 남는다.** 원문은 이것을 결과가 아니라 **방법의 전제**로 인쇄했다("cannot contribute to the OCP … inactive") — 이 계보에서 "접촉 손실의 정량값" 으로 인용될 수를 만든 절차가, 정의상 `LAM_PE` 와 접촉 손실을 같은 칸에 넣는다.
**③ ⚠ 이 편이 주지 않는 것.** 비연결 입자의 보유 리튬 · 압력 되돌림 · `θ` 전용 조작(SC ↔ PC 는 입도 · 재소성과 교락) · 사이클 `R_ct`/`C_dl` 값 · SI(S1–S9). 이완 1 h 는 `[재현]` PC 후반 확산 시상수(≈13–17 h)보다 짧아, 합 자체가 동역학 손실을 일부 품을 수 있다(방향 `[추론]` — 질량 손실 과대).

### ★★★★ 서른다섯 번째 — **For 에 붙는 실측: 접촉 면적을 영상으로 직접 재도, 저항 변화의 대부분은 그 면적 밖에 있다** (2026-09-23, Sakka et al. 2022 · 실험, SPring-8 CT + 동시 EIS, 신품, 압력 5 점 · 점당 n = 1)

`raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "The contact area fraction represents the fraction of the area in contact between NCM and LGPS with respect to the surface area of the NCM particles" · "The fraction increases by approximately 10% when the pressure is greater than 50 MPa compared with … less than or equal to 12 MPa" · "the charge transfer resistance is inversely proportional to the pressure. This corresponds to the increase of the contact area fraction" · "The enhanced contact area fraction … led to an order of magnitude reduction in charge transfer resistance." `[도표]` `φ` 0.749 → 0.827 · `R_ct` 8.7 → 0.62 ×10⁵ Ω (6 → 100 MPa).
**② 카드 물음으로 (`[해석]`).** `φ` 는 37호의 `A_eff` 쪽 손잡이(OCV · 용량에 안 보이고 `k_p` 와 항등)다. 이 편은 그 손잡이를 **직접 재서** 곱의 나머지가 `[재현]` ×13 을 가져간다는 것을 보였다 — "접촉 면적" 이라는 이름표 아래 **해상도 아래 실접촉 · 계면 화학 · 상대극**이 섞여 있다. OCV 로 `LAM_PE` 와 접촉 손실을 가르기 이전에, **접촉 손실 안에서도** 측정 척도에 따라 다른 양이 된다.
**③ ⚠ 이 편이 주지 않는 것.** 사이클 뒤 구조(`θ(N)` 0/39) · 통째 비연결 `u` · 운전 압력(되돌림) 의 `φ` · 분할 문턱 · 반복 · 방향별 `φ` 수치. 분할이 고정 혼합물의 부피비를 ×2 흔든다(`[재현]`) — `φ` 추세의 **크기**는 서지 않는다.

### ★★★ 서른여섯 번째 — **For 에 붙는 계보 사실: 이 계보가 기준으로 삼은 R-LTO 전위는 원전에서 측정이 아니라 문헌 증인 합의였다** (2026-09-23, Ikezawa et al. 2020 · 실험, 3전극 EIS + 충방전, 신품, n 미기재)

`raw/papers/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "With reported redox potential of Li₇Ti₅O₁₂|Li₄Ti₅O₁₂ (1.55 V vs. Li|Li⁺) [11], these potentials can be calculated to be 3.90 and −0.60 V vs. Li|Li⁺, which are coincident with reported values [5,17]. This result clearly shows that the R-LTO electrode successfully worked" · "Good agreement between cell impedance measured with two-electrode configuration and the sum of LiCoO₂ impedance and Li-In impedance … showed that the impedances … were successfully separated" · "Larger values of R2 and R3 in the cell impedance indicated that the LiCoO₂ impedance was overestimated with … conventional two-electrode cells using Li-In negative electrodes".
**② 카드 물음으로 (`[해석]`).** 카드의 출발 전제("상대극은 평탄하므로 완전지 OCV 는 양극 곡선이 밀린 것")를 3전극으로 검사하려던 계보 전체가 기대는 영점(1.55 V)이 **원전에서 ±≈25 mV 분해능의 증인 합의**다(`[재현]` 증인 0.62 V 면 1.5745 V). 38호 척도(기준 ±10 mV ≈ 활성 질량 ±4 %)로 옮기면 **이 영점의 불확실만으로 `LAM_PE` 판독이 수 % 흔들린다** — 기준 전위를 절대로 쓰는 분해(18호 컷오프 환산)는 이 폭을 물려받는다. 그리고 같은 지면이 **2전극 양극 호의 ≈절반이 상대극**임을 보인다(R2 ×2.7 · R3 ×1.67, 신품).
**③ ⚠ 이 편이 주지 않는 것.** Li 대비 교정(LGPS 에서 Li 불안정 — 설계상 불가라고 서론이 말한다) · 누설 · 시간 안정성 · 셀 간 산포 · 열화. 같은 상태의 R3 가 세 값(×1.49)이라 SOC 축 귀속도 약하다.

### ★★★★ 서른일곱 번째 — **For 에 붙는 원전 실측: 2전극 반쪽전지의 "작업전극 용량 부족" 은 상대극이었고, 얇은 SE 완전지의 "쿨롱 효율 저하" 는 Li 손실이 아니라 누설이었다** (2026-09-23, Nam et al. 2018 · 실험, 벌크형 3전극 + TOF-SIMS + ⁷Li NMR + 감지극, 조건당 n 미기재)

`raw/papers/nam2018_three-electrode-assb-failure-modes-li-in-depletion.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "the overall discharge is ended by termination of Li–In CEs, not Sn WEs" · 적재 4 → 10 mg cm⁻² 에서 Sn 용량 534 → 307 mAh g⁻¹(액체 958) · "Li-depleted indium layer is formed at the top of the CE, impeding further movement of Li⁺ ions" · "NCM being in touch with Li metal will be chemically lithiated by consuming the as-contacted Li metal, which is the opposite direction to charge and causes leakage of current. Consequently, significant imbalance in the amount of charge and discharge … (or low coulombic efficiency)" — 쿨롱 효율 99.0 → 88.7 · 80.3 · 82.5 %(0.2 → 0.5 · 1 · 2 C, 50–60 µm SE) ↔ 99.5–99.8 %(730 µm).
**② 카드 물음으로 (`[해석]`).** 2전극 곡선이 보여 주는 두 신호가 **둘 다 다른 이름의 것**이다: 적재 의존 용량 부족은 `LAM`(작업전극)의 서명이지만 **상대극의 표면 접근성**이고(17호 "겉보기 `LAM_PE` 가 상대극" 의 2018 원형), 쿨롱 효율 저하는 `LLI` 대리의 서명이지만 **연성 단락 누설**이다(Li 는 NCM 으로 돌아간다). 3전극 없이는 둘 다 모드 라벨을 잘못 받는다. 그리고 첫 사이클 끝을 **양극이 낸다**(NCM 79.1 % < Gr 92.5 %) — 액체셀과 반대라 음극 여유 Li 가 작은 `LLI` 를 용량에서 가린다.
**③ ⚠ 이 편이 주지 않는 것.** 양극 `LAM` ↔ 접촉 분석(0 — SEM 정성 부정 한 줄) · EIS · 옴 보상(배면형 RE 라 분리막 옴 전부가 상대극 채널로; "Gr < 0 V" 는 반전 계단 절반 안) · 고갈층 대조군 · 정량 · 반복 · 누설 전류의 크기. 기준 전위 교체 대조(Fig. S2)는 수를 싣지 않았다.

### ★★★ 서른여덟 번째 — **For 에 붙는 원전 실측: 계보가 쓰는 In–Li 0.62 V 는 액체셀 적정값이고, 원전의 평탄은 공칭 조성 창 ≈1–47 at% 에서 ≈15 mV 처진다 — 그리고 원전의 고체 대칭셀 전압은 SE 옴보다 작다** (2026-09-23, Santhosha et al. 2019 · 실험, 액체 3전극 적정 + 고체 대칭 2전극, 조건당 곡선 1 개)

`raw/papers/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "Using a liquid electrolyte and hence being able to use a 3-electrode cell with a lithium reference electrode, we followed the phase formation during lithiation of indium" · "we were able to determine the room temperature equilibrium potential of the In–Li electrode within the (In)–InLi two phase region to 0.62 V vs. Li⁺/Li" · "the homogeneity range of the InLi phase at room temperature is about Δx ≈ 1.9 at%. Upon lithiation, the redox potential within this phase decreases by about 280 mV" · "making the In–Li electrode an attractive counter/reference electrode for SSBs" · "As long as the composition … is within the two phase region (In)–InLi, reversible Li⁺ insertion/deinsertion is possible with only 12 mV of overpotentials at a current density of 1 mA cm⁻². For too high lithium contents, however, the chemical stability toward the solid electrolyte is poor".
**② 카드 물음으로 (`[해석]`).** 카드의 출발 전제("상대극은 평탄하므로 완전지 OCV 는 양극 곡선이 밀린 것")가 기대는 수 **0.62 V 의 측정 원전은 액체셀**이고, 원전의 평탄 창은 **공칭 조성 ≈1–47 at%** 에 **≈15 mV 폭**(0.5 h 이완 프로토콜)이다. 38호 척도로 옮기면 `[재현]` 활성 질량 ≈±3 % — 기준을 "상수" 로 쓰는 분해가 **원전 조건에서도** 물려받는 폭이다. 창 밖은 **1.9 at% 에 −280 mV** — 상대극 조성이 창 끝을 넘는 순간 기준이 `LLI` 모양으로 옮겨 간다. 그리고 원전의 **공칭 조성 자체가 질량 ↔ 치수로 5.6 at% 어긋나 창 끝을 가로지른다**(44.1 ↔ 49.6 at%) — "질량 균형을 맞추라" 는 원전의 처방이 원전의 셀에서 검산되지 않는다.
**③ ⚠ 이 편이 주지 않는 것.** ASSB 안 Li 대비 전위(0 — 고체 셀은 대칭 2전극) · 곡선 반복 · 산포 크기 · 이완 검증 · 온도 수치 · 분리막 면 조성 · 사후 분석 · 고체 EIS. 대칭셀 전압이 SE 옴의 1/25–1/47 이라(`[재현]`) "InLi-(In) 이 1 mA cm⁻² 로 Li 를 냈다" 는 이온 경로로 입증되지 않는다.

### ★★★★ 서른아홉 번째 — **For 에 붙는 음극 실측: 반쪽전지 흑연의 용량 손실은 `LAM_NE` 와 고립이 한 곱이고, 원전은 그것을 dQ/dV 높이로 "loss of the active material" 이라 부른다 — 같은 셀의 임피던스 면적 서명은 용량 손실보다 크다** (2026-09-23, Fukunishi et al. 2023 *ACS AEM* · 실험, 흑연 \| LPSI 3전극, RT 500 → 333 K 50 사이클, 셀 1 개)

`raw/papers/fukunishi2023_graphite-three-electrode-impedance-cyclability.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "The differential plots (dQ/dP) … indicate that every peak intensity corresponding to the graphite staging is decreased. This means that capacity decrease mainly resulted from the loss of the active material." · "The doubled RCT suggests the decrease in the electrode−electrolyte interface area (for ionic paths) caused by the solid electrolyte decomposition. The decrease in the CPE constant (CPEx-T and CPECT-T) also suggests the loss of contact area." · Table 3(`R` · CPE-T · CPE-P 전후 ±) · Table 2(`Ea` 전후). 그리고 R-LTO 쪽: "a small potential shift of ca. 10 mV (negative direction) seen in both the graphite and Li−In electrodes, which could be caused by the change of the R-LTO reference electrode potential".
**② 카드 물음으로 (`[해석]`).** 상대극이 Li 저장소인 반쪽전지에서는 WE 용량에 `LLI` 가 없다 ⇒ 저율 용량 손실(`[도표]` ×0.75–0.78)은 `(1−LAM_NE)(1−u)` **한 곱**이고, 원전은 그 곱에 dQ/dV **높이**로 이름 하나를 붙였다(`[도표]` 봉우리 비 0.53–0.70 · 0.21 V ×1.03 — 균일 비례 모양이 아니다). 같은 셀 `R_CT` 호의 면적 서명(`[재현]` `C` ×0.43 ± 0.2 ≈ 1/`R` ×0.47)은 용량 손실보다 크다 — 1단계를 믿는 한 **면적 손실의 일부는 피복이지 고립이 아니고**, `LAM_NE` ↔ 고립은 **이 편의 어떤 채널로도 안 갈린다.** 카드 물음의 양극 구조가 **음극에서 그대로** 선다. 그리고 표류: 두 평탄 증인이 **같이** 움직인 것(공통 모드 ≈−14 mV, `[도표]`)을 원전이 기준극 탓일 수 있다고 인쇄 — ≈10 mV 급 기준 이동은 21호 척도로 활성 질량 몇 % 에 해당해 **완전지 분해의 `LAM`/`LLI` 흉내 크기**다.
**③ ⚠ 이 편이 주지 않는 것.** 양극 `LAM_PE`(양극 없음) · 봉우리 넓이 · 셀 반복 · 운전 압력 · 단면 영상(`θ`) · 흑연 BET. 1단계 ↔ 3-a 가 같은 호에서 충돌하고(`Ea` 22 → 27.5), 그 호의 `C`(20–46 mF)는 이중층 상한의 수백 배라 **면적 서명 자체가 조건부**다.

### ★★★ 마흔 번째 — **For 에 붙는 원전 실측: 20호 셀의 원전은 "접촉 면적" 을 GITT 곱의 한 인자를 대조 셀 가정으로 떼어 얻었고, 그 방전 용량은 Li 재고 수지를 넘는다** (2026-09-23, Jin et al. 2015 · 실험, 2전극 반쪽(In 박) GITT + 완전지 7 설계, 신품 + 9–14 사이클, 셀 1 개씩)

`raw/papers/jin2015_lithium-silicide-anode-electrode-design-assb.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "Because there was no addition of electrolyte to the working electrode (lithium silicide layer) in Case 1, S is simply the geometric area of the sample" · "Using DLi from Case 1, we can estimate the effective electrolyte/active material contact area of Case 2 (i.e., 3.19 cm², which is about 2-times higher than for Case 1)" · "the difference in the charge and discharge capacity is attributed to faster de-alloying than alloying in lithium silicide in the initial stage [30]" · "Although we cannot numerically determine the interfacial resistance at anode/current collector, it is obvious that …".
**② 카드 물음으로 (`[해석]`).** GITT 식은 `√D · S / θ`(θ = 참여 분율, `m_B` 안) 한 조합만 준다 — 카드의 곱(`LAM`/고립 ↔ 면적 ↔ 동역학)이 **식 한 줄에 그대로** 있다. 원전은 Case 1 의 가정(`S` 기하)으로 `D` 를 뽑고 Case 2 의 차이를 전부 `S` 에 줬는데, **Case 2 작업전극에도 전해질이 없다**(Fig. 2B). `[재현]` 자기 BET 비 ×8.7 ↔ `S` 비 ×2.07 · GITT 참여 용량 비(`[도표]` ≈×2.75)를 `θ` 로 넣으면 `S` 비 ≈×4.7–5.7 — **이름표가 가정 하나에 ×2.3–2.8 움직인다.** 그리고 `[재현]` 200 µA 세 완전지에서 방전이 이전 충전을 넘어 TiS₂ 를 x > 1 로 채운다 — **2전극 방전 용량 = 양극 용량이 아니다**(부반응 싱크 후보). 동역학 서술("de-alloying faster")은 이 수지를 통과하지 못한다(20호 셀은 통과: 2 방전 = 1 충전).
**③ ⚠ 이 편이 주지 않는 것.** 열화(9–14 사이클 설계 비교) · 3전극 · 운전 압력(그림에만) · 셀 반복 · 용량 정규화 기준 · In 박 상대극 질량. Table 2 `ΔE_t` 가 그림과 ×≈2 어긋난다.

### ★★★★ 마흔한 번째 — **For 에 붙는 원전 실측: "0 V 로 놓은 리튬화 금선" 의 원전은 영점을 도금 Li 의 상 정체로 정했고, 그 기준극은 수명이 있어 떨어지면 계단으로 옮겨 간다 — 그리고 같은 지면의 2전극 방전 용량 부족은 상대극 Li 소진이다** (2026-09-23, Hertle et al. 2023 · 실험, μ-RE 3전극 EIS + 율 시험, 신품, n 미기재)

`raw/papers/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "After complete lithiation of gold to AuLi₃, lithium metal is plated on the μ-RE leading to another plateau of 0 V vs Li⁺/Li" · "a mean thickness of 4 μm was used for the μ-RE, leading to a stable potential of 0 V vs Li⁺/Li for at least 8 days" · "it is possible that the lithium on the wire reacts completely with the SE which then results in a different potential of the RE" · "The In/InLi anode was assembled with the appropriate lithium/indium ratio and therefore exhibited a stable potential of 618 mV vs Li⁺/Li" · Fig. 7 "a stable potential of –618 mV vs In/InLi" · 율 시험 "LTO is delithiated when assembling the cell and no lithium excess is present" · "Interestingly this increase is happening early indicating side reactions that are consuming Li" · 2E 임피던스 "Both sets of parameters fit the experimental data equally well using the same equivalent circuit".
**② 카드 물음으로 (`[해석]`).** (a) **기준 이동이 계단형이다.** 도금 Li 가 있는 동안 0 V, 소진되면 기준극은 Au–Li 사다리의 다음 칸(`[도표]` AuLi/AuLi₃ **+0.133 V**)으로 올라선다 — 3전극 분해에서 **일정 오프셋**으로 숨어 `LLI`/`LAM_PE` 를 흉내 낼 크기다(43호 절: ≈10 mV 급 기준 이동이 이미 활성 질량 몇 % — 한 칸 133 mV 는 그보다 한 자릿수 크다). 원전은 그 끝을 "≥8 일" 이라는 **기간**으로만 인쇄하고 끝의 모양 · 크기를 보이지 않는다. 16호(원전 조건 밖: 면적당 전하 1/9.6)의 셀 간 0.11 V 는 이 한 칸(0.133 V)과 23 mV 차 — 후보. (b) **같은 지면의 2전극은 `LLI` 를 양극 용량 손실처럼 보인다.** 빈 LTO 상대극이 부반응으로 Li 를 잃어 0.1 C 방전 ≈160–165 mAh g⁻¹ 에서 1.55 → 3.2 V 로 뛰고(`[도표]`), 2E 방전은 165 · 3E(양극 컷오프)는 193 — 2전극만 보면 −15 % 가 양극 쪽이다. 17호(Li-In) · 21호(NCM\|In) 의 구조가 **LTO 상대극**에서 선다. (c) 2E 임피던스 분할의 비유일성이 **저자 문장**으로 인쇄됐다(`R_Anode` ×3.6) — 카드의 곱 축퇴와 같은 형태가 **전극 분배** 층에 있다.
**③ ⚠ 이 편이 주지 않는 것.** 표류 수 · 누설 · 반복 · 열화 · `θ` · 온도 축. 3E 의 165 → 193 구간 전하는 음극이 2.5–3.2 V 로 끌려가는 동안 흐른 것(음극 쪽 산화 부반응이 Li⁺ 원천 — `[해석]`, 원문 무언급). 검증(Fig. 10) 셀과 분석(Fig. 5 · 11 · S7) 셀이 다르다(`[재현]` 고주파 ≈49 ↔ ≈97 Ω cm²).

### ★★★ 마흔두 번째 — **For 에 붙는 음극 판 원전 실측: Li 금속 계면 저항 증가를 저자가 "면적 또는 절연 SEI" 로 인쇄하고 두 갈래를 모두 "활성 접촉 면적 감소" 로 끝냈다 — 그리고 그 셀에서 쓴 Au 도금 W 기준극은 영점이 필요 없는 자리였다** (2026-09-23, Schlenker et al. 2020 · 실험, Li\|Li₆PS₅Cl\|Li 대칭셀 + 매립 기준극 EIS + XPS + ToF-SIMS, 셀 수 대부분 미인쇄)

`raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "An increase of interface resistance can be highly correlated either with a decreasing interface area between lithium anode and electrolyte as R ∼1/A or an ionically insulating SEI formation at the interface, leading to a decreasing active contact area for lithium stripping" · "Still it is an open question if this effect of interface area is stronger than the influence of the SEI" · "A sudden voltage drop indicates a short circuit" · "the reference wire is plated with lithium from both electrolytes to reach a constant potential of the reference" · 결론 "A SEI should not be neglected, but the main focus should be put on the actual contact area".
**② 카드 물음으로 (`[해석]`).** (a) **곱이 저자 문장 안에서 한 이름으로 합쳐진다.** 계면 저항은 기하 접촉 × 화학적 통과 분율의 역수만 보고, 저자는 두 가설 모두를 "active contact area" 감소로 적었다 — 37호 `A_eff ↔ k` 항등의 Li 음극 판. 배정은 XPS 음성 · 가역성 논증(반주기마다 되풀이되는 상승) · 도금 쪽 반대 부호로 **논증**했고 측정으로 가르지 않았다. (b) **역방향 반쪽 짝**(박리 쪽 R3 ↑ · 도금 쪽 ↓ — 면적 가설은 부호 반대, 단조 계면층은 같은 부호) 은 좋은 판별 설계인데, 도금 쪽이 유도성 때문에 성분 분리가 막혀 반쪽만 남았다. (c) **기준극**: 영점 값 · 검증 0 — 같은 금속 대칭셀의 AC 측정이라 영점이 결과에 안 들어간다. 16호는 같은 선을 NMC 상대 · DC 전위 축으로 옮기며 Hertle(Giessen)의 0 V 를 빌렸다.
**③ ⚠ 이 편이 주지 않는 것.** 양극 · `θ` · 기준 전위 값 · 상태별 `C` · 온도 · 단락 확인(임피던스 · 해체) · 연성 단락 배제. 지면의 세 수(Fig. 8 · Fig. 4b · "about 6 MPa")는 인쇄된 Li 면적(∅4 mm)이 아니라 `[재현]` ≈0.16 cm² 에서 맞는다. Fig. 1 본문 ↔ 캡션 J·t 배정 뒤바뀜(`[재현]` 캡션이 맞다).

### ★★ 마흔세 번째 — **For 도 Against 도 아닌 계보 원전(액체): 계보의 0.31 V 는 Li 금속 대비로 잰 값이고, 원전은 그 영점을 쓸 조건을 인쇄했다 — 21호는 그중 둘 밖에서 읽었다** (2026-09-23, Solchenbach et al. 2016 · ⚠ 액체셀 실험, Li\|Li · LFP\|흑연 T-셀, 셀 1 개(VC 조건당 2))

`raw/papers/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "the potential of the GWRE shoots up to 0.318 V and then quickly relaxes to ∼0.311 V vs. Li/Li⁺, which corresponds to the OCV potential of a LixAu alloy with 0 < x < ∼1.2" · "remains stable for more than 500 h, varying by less than 2 mV after the initial 20 h" · "might not be suitable for highly accurate potential measurements during initial cycles" · "a re-lithiation … restored a stable GWRE potential of 0.311 V" · "We believe that this originates from the stripping of lithium … roughening" · "it is crucial to use a reference electrode with a stable and defined potential for WE - RE potential controlled impedance measurements at low frequencies" · 결론 "we could identify lithium inventory loss due to SEI growth as the dominant aging mechanism".
**② 카드 물음으로 (`[해석]`).** (a) **기준 전위의 원전 측정이 존재하고, 사용 조건이 붙어 있다** — 초기 창 · 온도 이력 · 노출 · 재리튬화. 계보가 이 값을 옮길 때 조건을 같이 옮기지 않았다(21호: 2 h · 원통 노출). 조건 밖이면 영점은 **mV 급(초기 +6–7 mV · 온도 1–2 mV)** 또는 **수십 mV 이탈**(온도 이력)로 움직이고, 3전극 분해에서 그 몫은 `LLI`/`LAM_PE` 흉내의 크기와 겹친다(43호 절: ≈10 mV 가 활성 질량 몇 %). (b) **표류 기준극은 PEIS 에서 완전지 스펙트럼까지 오염시킨다** — 합 일치 검사가 표류를 못 잡는 또 하나의 이유. (c) **3전극 끝점 이동(`LLI` 서명)은 측정, `LLI` 라벨은 해석** — 우리 α·β 가 완전지에서 풀려는 것이 액체에서는 측정으로 갈려 있으나, 정량 · `LAM` 과의 분리는 원전도 하지 않았다.
**③ ⚠ 이 편이 주지 않는 것.** ASSB · 압력 · 누설 측정 · 셀 간 산포 · 리튬화 깊이 · 0 V(도금) 칸. 45호가 이 편에 단 134 / 215 mV 는 지면에 없다.

### ★★★ 마흔네 번째 — **For 에 붙는 같은 셀 시연: 2전극 합은 한 전극 모형으로 "만족" 적합되며 귀속을 ×2.2 틀리고, 상대극 창의 용량 오차를 원문이 스스로 번역했다** (2026-09-23, Dugas et al. 2021 · 실험, 전면 Li₀.₅In : SE 기준층 3전극, 신품 · 최대 5 사이클)

`raw/papers/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "This implies that the WE and CE impedances cannot be decorrelated in a 2 electrodes measurement" · "its resistance is more than doubled (307 Ω cm² instead of 139). Obviously the difference corresponds to the contribution of the CE and should not be attributed to the WE" · "if such a spectrum evolves during cycling there is no way to identify which electrode is at the origin of the variations" · "±160 mV … ±20 mV so that a 2 electrodes configuration can safely be employed … (20 mV correspond to ⩽2 mA h g⁻¹ at end of charge for NMC)" · "Values in this area are only indicative of a negligible Rct since the quality of the fit is not altered upon removal of the corresponding loop".
**② 카드 물음으로 (`[해석]`).** (a) **적합 품질은 전극 귀속을 검사하지 않는다** — 같은 모형 족에서 두 전극 호의 합이 한 전극 호로 "satisfactory" 하게 맞는다. 2전극 완전지 EIS 로 양극 `R_CT` 변화를 접촉 손실 · `LAM_PE` 와 엮는 논증은 이 시연 앞에서 먼저 상대극 몫을 떼야 한다(17 · 40 · 45호와 같은 방향, 여기는 한 스펙트럼 대 한 모형의 직접 시연). (b) **상대극 창 → 용량 오차**를 원문이 번역했다: 20 mV ↔ ⩽2 mA h g⁻¹(NMC 충전 끝, 첫 충전 140 mA h g⁻¹ 의 ≈1.4 %) — 카드의 "상대극 전위 → 겉보기 `LAM_PE`" 경로의 크기 한 점. β-LPS 의 ±160 mV 는 그 8 배다(선형 외삽이면 ≈10 %, 우리 외삽 — OCP 기울기가 일정하지 않다). (c) 저자는 창이 좁은 전해질에서 **2전극이 안전하다**고 결론냈다 — 그 판단의 문턱(2 mA h g⁻¹)이 인쇄된 것이 이 편의 기여다.
**③ ⚠ 이 편이 주지 않는 것.** 열화 분해 · `LAM` · 접촉 손실 · `C`(상태축) · 셀 간 산포 · 기준극 누설 · Li 대비 영점 측정(인용 622 mV; Fig. 10a 판독은 우리 것).

### ★★ 마흔다섯 번째 — **For 도 Against 도 아닌 도구 원전(액체): 저항 "성분" 은 창 경계의 규약이고, 원전은 그것을 두 곳에 인쇄한 뒤 결론에서 지웠다 — 20호는 원전의 모양 규칙만 가져가고 시간 규약을 두고 왔다** (2026-09-23, Barai et al. 2018 · ⚠ 액체셀 실험, 상용 20 Ah LFP/흑연 파우치, 50 % SoC · 25 °C 한 상태, 셀 수 미인쇄)

`raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "the computed resistance is strongly dependent on the timescales of the technique employed and that when timescales match, the resistances derived via different techniques align" · "there in an inability to completely separate the different resistance components" (sic) · "Estimating polarisation resistance using EIS results is not well-defined" · "Rp isn't identified from a Nyquist plot, instead it is pre-defined" · "Although the ECM parameters are not uniquely identifiable" · "we follow the usual prescription of calculating Ro, RCT and Rp with DC methods8" · "it is therefore physically more meaningful to use the voltage drop after 4ms" · 결론 "EIS can accurately provide separation and identification of all the individual resistance components, Ro, RCT and Rp".
**② 카드 물음으로 (`[해석]`).** (a) **저항 성분 이름표(`R₀`/`R_CT`/`R_p`)는 식별된 양이 아니라 창 경계의 차**다 — 같은 셀 같은 상태에서 방법만 바꿔 `R_p` ×13, EIS 경계만 옮겨 ×3.9. 카드의 곱을 가르려는 논증이 "`R_CT` 가 늘었다" 에서 출발하면 먼저 **그 `R_CT` 가 어느 창의 차분인지**를 적어야 한다. (b) **관측 대역의 위쪽 끝이 직렬 저항의 값을 정한다** — 다중사인 ECM `R₀` = |Z|(1 Hz), DC 0.1 s = |Z|(10 Hz). ASSB 에서는 SE 벌크 · 입계 · 계면 호가 kHz–MHz 에 있어 샘플 간격에 따라 "옴" 이 계면 몫을 품는다 — 20호 "접촉 저항 362 Ω"(= 순간 `R₀` − SE 벌크)에 대역 조건이 하나 더 붙는다(20호 샘플 간격 미인쇄). (c) **20호는 원전의 모양 규칙(곡선 → 직선)을 가져가고 시간 규약(0.1 · 2 · 10 s, 5 C, 50 % SoC, 4 h 휴지)은 두고 왔다** — 창 ×10³, 전류 1/360. 원전 자신의 명제("governed by the measurement timescale")로 보면 20호 `R_CT` 는 원전 `R_CT` 와 다른 창의 양이고, 원전 규약으로 그 창(1 h ↔ ≈0.28 mHz)은 확산 대역이다 — 20호 3-b 실패와 같은 방향.
**③ ⚠ 이 편이 주지 않는 것.** ASSB · 열화 · 상태축(SoC · 온도 · 노화) · `C` · 시상수 · 셀 간 산포 · 면적. 그리고 **"시간 척도만이 값을 정한다" 는 5 C 에서만** 보였다 — 같은 지면 진폭 스윕(×1.46)과 대진폭 다중사인(−24 % @ ≈0.017 Hz)은 반대 증거다.

### ★★★ 마흔여섯 번째 — **For 에 붙는 방법 원전: 곱 `A·j₀` 에 `j₀` 라는 이름을 붙인 출생지 — 두께 가변은 이온 수송과 전하이동을 가르지만 면적과 `j₀` 는 못 가르고, 면적 규약 한 줄이 값의 ×τ 를 정한다** (2026-09-23, Miß et al. 2022 · 실험, 신품, 두께 4 점 × 2 재료, n 미인쇄)

`raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "The active area of the CAM particles in contact to SE normalized by the cathode volume is given by `a_v = (ε_CAM A_CAM)/V_CAM = (3ε_CAM)/r_CAM`" · "These contacts determine the Li⁺ exchange current density at the CAM | SE interfaces" · "the interfacial CAM | SE area normalized by the nominal cathode area should be better described by `a_v d`" · "the TLM predicts a semicircle resistance, which is independent of thickness … while the experimental spectra are characterized by a decrease … The origin of this discrepancy … is unclear at present" · "leaves no doubt about the much higher exchange current density of the LCO-based cathodes" · "Only the parameters `j₀`, `Q_DL`, and β were considered as freely adjustable parameters".
**② 카드 물음으로 (`[해석]`).** (a) **ASSB 복합양극 `j₀` 의 대표적 보고 방식이 면적을 기하로 고정한다** — 이 편과 16호의 `j₀` 는 `j₀^true × θ` 이고 저자의 틀(압력이 `j₀` 를 바꾼다)도 그 뜻이다. 열화 쪽으로 옮기면: 사이클에 따른 `j₀` 감소 보고는 이 규약에서 **접촉 손실과 계면 화학 변화를 한 이름으로** 받는다. (b) 곱을 가를 재료(`Q_DL`)가 같은 표에 있고, 1단계로 **같은 지면 비교는 서고(τ ×106) 편 간 비교는 면적 서명(τ ×1.28)** — 가르는 도구가 작동하는 모양의 실례. (c) 규약(`a_v·τd ↔ a_v·d`)이 값을 ×6–7 옮긴다 — 편 간 `j₀` 비교에는 규약 확인이 전제다.
**③ ⚠ 이 편이 주지 않는 것.** 열화 · `LAM` · θ 측정 · `Ea` · 셀 간 산포 · 기준극 · 원자료. R·C 판정은 `C ∝ θ` 전제 · Brug 근사 위의 우리 계산이다.

### ★★★ 마흔일곱 번째 — **For 에 붙는 저압 실셀: 2전극 용량 손실은 이름이 없고, 그 대리로 쓰인 쿨롱 효율은 Li 재고를 넘는 결손을 낸다** (2026-09-23, Oh et al. 2025 *AEM* · 실험, 펠릿 20 · 3 MPa + 파우치 3 MPa, 조건당 셀 1)

`raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "MgSiGr achieved an impressive average CE of 99.2 % for the 75 cycles" · "capacity retention of 83.7 %" · "maintained 64.7 % of the original capacity after 75 cycles under the challenging conditions of low stack pressure, room temperature, and a low N/P ratio of 0.66" · "the interfacial stability, the most critical factor for the cyclability of ASSBs operating at low stack pressure, highly depends on the lithiation kinetics of the anode" · 연성 단락은 "additional parallel resistance … (rSS) … which reduces RB and RCT accordingly".
**② 카드 물음으로 (`[해석]`).** (a) **N/P < 1 과충전 셀에서 2전극 곡선의 대부분은 양극 반쪽 곡선이다**(도금 구간 음극이 평탄) — `LLI` 는 슬리피지가 아니라 끝점 이동으로만 나타나고, 끝을 누가 내는지가 정해지지 않으면 `LLI` ↔ `LAM_PE` 가 같은 "용량 축 절단" 으로 보인다(45 · 48호 경로의 무음극형 판). (b) 그 끝을 정할 대리로 흔히 쓰는 CE 가 이 지면에서 스스로 깨진다: `[재현]` 3 MPa 누적 충–방 결손 ≈575 mAh g⁻¹ 는 NCM811 Li 재고 ≈275 의 ≈2 배, 20 MPa 도 결손 ≈95 ↔ 손실 ≈27 — **CE 결손을 `LLI` 로 넣으면 OCV 적합이 받는 `LLI` 사전값이 틀린 크기로 들어간다.** (c) 조건 간 CE 비교는 면적당 결손으로 바꿔야 한다 — 이 편의 두 압력은 CE 로 ×≈7, 면적당으로 ×≈1.8.
**③ ⚠ 이 편이 주지 않는 것.** 양극 채널 전부 · 끝 전극 · 3전극 · 반복 · 압력 계측 · 3 MPa CE 수치(그림만). ② 의 결손은 화소 판독(±1 %p) 위의 우리 계산이다.

### ★★ 마흔여덟 번째 — **For 에 붙는 종설의 인쇄: `θ(N)` 측정은 없고, 시간 배정은 인용을 거치며 뒤집힌다** (2026-09-23, Ren · Danner et al. 2023 *AEM* · ⚠ Perspective, 1차 기여는 P2D 사례 계산 하나)

`raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "There is yet no experimental study that incorporates percolation theory and its influence on mechanical degradation" · "no experimental technique has successfully estimated the fracture strength between the CAM and SE particles" · "the rapid capacity fade during the first charge/discharge step can be attributed to the electrochemical oxidation of the interface … whereas the slower subsequent decay is due to fatigue failure of the CAM/SE interface and loss of electrochemically active surface area" · "Loss of contact between CAM and SE leads to a decrease in electrochemically active surface area, which can substantially increase the charge transfer resistance and cause voltage and capacity fade"([32]) · "Deconvolution of the contributions in impedance data is challenging" · SI "Electrochemical and mechanical degradation processes are also neglected in the simulations".
**② 카드 물음으로 (`[해석]`).** (a) **`θ(N)` 의 1차 측정이 없다는 것이 2022 년 종설의 인쇄로 선다** — 카드가 `θ(N)` 0/53 을 세어 온 것이 표집의 우연이 아니라 문헌의 상태라는 방증. (b) **접촉 손실의 시간 모양(계단 ↔ 점진)이 편마다 반대로 적힌다** — 황화물 원전(23호)은 첫 충전의 계단, 이 편(산화물)과 33호는 이후 사이클의 점진. OCV 적합으로 `θ(N)` 을 truth 에 넣을 때 **모양 자체가 가정**이다. (c) 산화물에서는 `θ₀` 가 공정 변수(냉각 균열 · 소결 경로)이고 공정으로 기계 기구를 끈 대조(FAST/SPS)가 문헌에 있다 — 재가압(4호)의 반대 방향 조작. (d) DLR 계열의 모델은 접촉을 `ε_p` 가 아니라 **기하(면적 `a` · 연결)** 로 다룬다 — 37호 ① 동어반복 경로를 피하는 쪽이다.
**③ ⚠ 이 편이 주지 않는 것.** 자기 측정 전부 · 접촉 분율 · 인용 원전의 형태([127] 의 `θ` 정의, [105] 의 배제 근거) · 산화물 운전 압력. ①의 문장들은 재인용이고 이 digest 는 원전을 열지 않았다.

### ★★ 마흔아홉 번째 — **For 에 붙는 원전의 인쇄: 수송 곱은 구조 계산으로 떼어지지만, 남은 합은 EIS 로 "unfeasible" 하고, 그 값이 하류에서 "measured" 가 된다** (2026-09-23, Neumann · Hamann · Danner … Latz 2021 *ACS AEM* · ⚠ 양극 없음, 모델 + 재사용 자료)

`raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "Since both degradation mechanisms possess a similar effect on the impedance response, an exact deconvolution of both contributions via EIS is unfeasible without additional information on the GB composition." · SI "not fully separable by experimental EIS without additional knowledge of the structural and compositional changes of bulk and GB during sintering" · "we assume that the bulk polarization process is not fully resolved in the experiments" · "These measurements are used to estimate the hopping rate `k_hop` and the DL capacity `C_DL^GB` which are in a second step refined manually" · Table S4 범례 "measured by the authors (superscript [°])" — 표시 0 개.
**② 카드 물음으로 (`[해석]`).** (a) **구조 계산은 곱의 한 인자를 뗀다** — 굴곡도(`τ`)를 3D 재구성에서 계산하면 `σ⁰·ε/τ²` 곱은 풀린다(이 계보에서 수송 곱을 구조로 가른 표본). 카드의 동역학 곱(`A_eff·ε_p`)에 대응하는 조작은 **영상 면적**(39호)이다. (b) **그러나 직렬 합은 남는다** — 벌크 ↔ 입계처럼 같은 전류 경로 위 두 저항은 소신호 EIS 에서 합으로 보이고, 가르는 채널(고주파 절편 · 온도 · 진폭)이 없으면 원문 스스로 "unfeasible" 이다. 카드의 `R_SP` ↔ `R_CT`(53호)와 같은 구조. (c) **라벨 층위는 인용을 거치며 오른다** — 손 보정 · "calculated" 가 02호에서 "measured in dense pellets", 원장에서 "measured 라벨" 이 됐다. 합성 truth 의 파라미터 출처를 적을 때 **원전 표의 표기**까지 내려가 확인한다.
**③ ⚠ 이 편이 주지 않는 것.** 양극 · CAM\|SE 접촉 · 열화 시계열 · 새 측정 · 불확실성. 인용 원전(Han 2016 · Hamann 2020)은 열람하지 않았다.

### ★★ 쉰 번째 — **For 에 붙는 구조 ↔ EIS 대조의 원형: void 는 수송 곱으로 들어가고, 두 경로의 "일치" 는 `ε` 규약이 만든다** (2026-09-23, Hlushkou · Reising · Kaiser · Spannenberger · Schlabach · Kato · Roling · Tallarek 2018 *JPS* 396 · 실험 EIS 1 + FIB-SEM 재구성 모의, 신품)

`raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md`.

**① 원전이 인쇄한 것.** `[인쇄]` 식 (3) `τ_cond = (σ_ion,electrolyte/σ_ion,composite)·ε` · "an ionic conductivity-based tortuosity of τcond = 1.6 ± 0.1 was obtained" · "The corresponding value of τdiff … is 1.74, close to the ionic conductivity-based tortuosity" · "The small difference … is most likely caused by the small amount of mechanically stabilizing resin" · 무공극 가상 구조 "decrease the tortuosity … from 1.74 to 1.27" · "The voids not only reduced the volume fraction … but also transformed the geometry of the solid electrolyte phase into a far more tortuous one" · void 상 = "all space occupied by the stabilizing resin and residual voids".
**② 카드 물음으로 (`[해석]`).** (a) **void 는 수송 곱으로 들어간다** — 가상 치환(void → SE, LCO 고정)이 한 구조에서 void 의 경로 효과를 떼고(`[재현]` `ε/τ` ×1.71), 모의에 계면이 없어 **접촉 효과(`φ`)는 구성상 0** 이다. [[assb-tortuosity-factor-effective-conductivity-split]] 표 둘째 줄("경로 좁아짐 → `σ_eff` ↓")에 수가 붙은 첫 표본이고, 14호 D12(void 는 용량에 안 보임)와 방향이 맞는다. (b) **두 경로의 대조는 `τ` 가 아니라 곱으로 해야 판정이 된다** — EIS 쪽 `ε` 가 미인쇄라 `τ_cond` 1.6 은 `ε` ≈0.65 를 전제하고(`[재현]`), 관측 곱으로는 EIS 0.406 ↔ 모의 0.309(×1.31). 24호(두 경로 차 → "진화")와 같은 구조로 차이를 한 원인("수지")에 배정했다. (c) **구조 계산이 곱을 푸는 것은 같은 시편일 때다** — 54호 명제의 조건. 합성 truth 에서 `ε`·`τ` 를 구조로 줄 때 그 구조가 비교 대상 시편의 것인지를 먼저 적는다.
**③ ⚠ 이 편이 주지 않는 것.** `θ` · `φ` · `u` · 연결성 · 열화 시계열 · 용량 · 압력 축 · 불확실성(`τ_diff` ± 0, n = 1). 인용 원전(Thorat 2009 · Landesfeind 2016)과 같은 권의 Kaiser 2018 은 열람하지 않았다.

### ★★ 쉰한 번째 — **For 에 붙는 모델 명제: 표면 피복형 접촉 손실은 저율에 안 보이고 고율에서 용량 손실처럼 보이며, 같은 피복률에서도 분포가 과전압을 ×2.6–4.5 바꾼다** (2026-09-23, Bielefeld · Weber · Rueß · Glavas · Janek 2022 *JES* 169 · FEM 모델, 새 측정 0)

`raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "At the small charge rate of 0.02 C, the active surface area reduction due to voids does not noticeably affect the voltage profile" · "The surface effect, we observe, alone is dependent on the void size, the void distribution and its surface coverage" · "many uniformly distributed voids can partly compensate the local inactive surface area by lithium diffusion inside the CAM particle" · "this model approach is not capable to quantify the influence of voids in the cathode composite on ionic percolation" · SI "electronic percolation will not be achieved for randomly distributed spherical particles at this volume fraction … isolated particles … are then moved manually" · "the often performed fitting of j0 … should be rethought and used with caution".
**② 카드 물음으로 (`[해석]`).** (a) **OCV · 저율 적합은 `φ` 를 못 본다**(모델) — `[도표]` 0.02 C 피복 손실 48 % 에 void 과전압 ≤ ≈7 mV · 용량 −3 %. 그런데 0.5 C 에서는 −25 % 가 **용량 손실처럼** 나타난다 — 율이 섞인 자료를 `LAM_PE` 로 적합하면 `φ` 가 거기로 들어간다(37호 갈래 ① 의 3D 판). (b) **`φ` 는 한 스칼라가 아니다** — 같은 70 % 에서 void 크기만으로 ≈19 → ≈50 mV(0.2 C @50). `[재현]` BV 면적 몫은 ≈절반(0.2 C · `A` ≈53 %: ≈21 ↔ 47 mV) ⇒ 37호 `A_eff ↔ k` 항등이 해상 모델에서 **부분적으로 깨진다** — 곱을 가를 두 번째 서명(입자 내부 확산의 공간 불균일)이 원리적으로 있다. (c) 그러나 이 편의 **검증 모델은 void 를 SE 로 채우고 `θ` 를 손으로 1 로 놓은 채 실험에 "맞았다"** — 곡선 일치가 미세구조를 가리지 못한다는 표본이기도 하다(원뿔 모델이 0.5 C 에서 입자형보다 실험에 가깝다, `[도표]`).
**③ ⚠ 이 편이 주지 않는 것.** 실측 · `θ(N)` · void 부피 스윕 · 경로 효과 · `j₀` 균일 축소 대조 · 이중층 · 오차 척도 · 방전 · 사이클. `j₀` 의 면적 규약(식 (12) `A`)은 원전 Rueß 2020 에 있을 것 — 열람하지 않았다.

### ★★ 쉰두 번째 — **For 에 붙는 모델 명제: 바인더는 `θ_AM` 을 안 움직이면서 활성 면적과 이온 경로를 같이 깎는다 — 한 공정 손잡이가 두 곱에 동시에 들어간다** (2026-09-23, Bielefeld · Weber · Janek 2020 *ACS AMI* 12 · 모델, 새 측정 0)

`raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "the binder covers active interface area and may affect ionic transport throughout the cathode" · "Owing to the mechanism of binder generation that was used on an existing AM microstructure, the utilization level of the AM is not affected by the presence of the binder, but there is a significant effect on the SE utilization" · "The available interface for lithium insertion is reduced by at least 17% … and 29% … For high AM fractions, the reduction even amounts to 43 and 82%" · "a higher void space significantly lowers the ionic conductivity, with 2-fold higher effective conductivities for 5% void space, compared to 20%" · "these parameters do not offer any further scientific insight" · "a model microstructure can only be understood as the snapshot of a real ASSB cathode".
**② 카드 물음으로 (`[해석]`).** (a) **바인더는 `LAM_PE` 자리도 `θ` 자리도 아니다** — 구성상 `θ_AM` 불변, 움직이는 것은 `A_spec,a`(37호 `A_eff`)와 `σ_eff`(수송 곱)와 `θ_SE`. 합성 truth 에서 "`θ`·`ε_p` 불변 + 율 손실" 을 만드는 비-LAM 손잡이의 크기를 준다(70:30 · 0.10 에서 `[도표]` `A_spec,a` ×≈0.50 · `τ²` ×2.4). 저율 OCV 에는 안 보여야 하는 손잡이지만 이 편은 전압을 계산하지 않았다. (b) **두 곱이 한 손잡이에 묶인다** — 이 조작을 대조군으로 쓰면 면적 몫과 수송 몫, 그리고 SE 고립 몫이 곡선에서 섞인다; 이 편은 `A_spec,a` 감소를 피복과 SE 고립으로 가르지 않았다. (c) **"pore 문턱 → 저항 급증" 은 계보 원전에 없다** — 합성 truth 에 void 문턱을 입력하지 않는다.
**③ ⚠ 이 편이 주지 않는 것.** 전압 · 용량 · 시간축 · `θ(N)` · 반응 동역학 · 반복 배열 오차 · void 문턱. 실험 대조는 남의 `σ_eff` 한 점과 남의 GITT 면적 비(곱 `D·(A/V)²`)뿐. 인용 원전(Nam 2018 *JPS* · Kato 2018)은 열람하지 않았다.

### ★★ 쉰세 번째 — **For 에 붙는 모델 명제: 박리를 "활성 면적 감소" 로 선언한 두 단계 모델이 결합상 `LAM_PE` 손잡이를 만든다 — 그리고 사이클 축은 구조적으로 없다** (2026-09-23, Asheri · Fathidoost · Glavas · Rezaei · Xu 2023 *Comput. Mater. Sci.* 226 · 계산 + 신경망 대리, 실험 0)

`raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md`.

**① 원전이 인쇄한 것.** `[인쇄]` "a = S/V (1 − ε_e)(1 − ⟨d⟩)" (식 (32)) · "it is assumed that the delamination at the interface decreases the active interfacial area … the loss of contact between the active material and the solid electrolyte is considered to be the same as ⟨d⟩. In the limit case when ⟨d⟩ = 1, the whole interface is damaged and the active particle becomes isolated" · "a uniform ion flux is considered at the surface of the particles" · "the chemo-mechanical case was not simulated using the FE² method (due to very high computational costs)" · "Recurrent Neural Network, to account for the history effects" (향후 과제).
**② 카드 물음으로 (`[해석]`).** (a) **이름표와 결합이 다르다** — 글은 면적(37호 `A_eff` 쪽)을 말하지만 미세 입자 유입이 손상과 무관하므로(`[코드]` `soc_dot = 2|j|` 전 행) 거시 `a·(1−⟨d⟩)` 는 입자 분율 `⟨d⟩` 를 통째로 떼는 것과 같다 — **`ε_p` 자리**. `[재현]` 저율 극한 손실(미세 자료 `∫⟨d⟩dSOC`) 8.9 · 3.9 % ↔ 1 C 셀 `[도표]` 8.7 · 3.1 %. 이 모델로 만든 truth 에서 접촉 손실과 `LAM_PE` 는 **같은 파라미터**다(37호 새 제약 3 의 두 번째 표본). (b) **`θ(N)` 은 구조적으로 불가** — 출력 ReLU(충전 불가) · 이력 변수 없음 · 한 방전. 얻는 것은 방전 안 `⟨d⟩(SOC; G_c)` 곡선(개시 SOC 0.73–0.89, 끝 0.03–0.45) — "SOC 문턱형 동적 `LAM`" 이라는 모양 하나. (c) **ML 이 계면 손상을 다루는 계보 유일 편(15호 지목)의 ML 은 미세 FE 의 대리**이고, 그 "정확도" 는 같은 궤적 안 행 분할의 충실도다 — 식별성 · 불확실성은 원 모델 것을 넘지 못하고, 원 모델은 검증되지 않았다.
**③ ⚠ 이 편이 주지 않는 것.** 실험 · 측정 · 압력 · 사이클 · 충전 · 불확실성 · 셀 수준 기준해(손상 사례). 그리고 그림 둘이 서술과 어긋난다(Fig. 10 전하 축 율 순서 · Fig. 11 `G_c` 13.92 가 무손상보다 늦게 끝남) — 이 편의 C-율 · `G_c` 효과를 truth 모양으로 쓰기 전에 이 둘이 풀려야 한다. MOOSE 입력 · 결합 코드는 저장소에 없다.

### Against / 단서 — "독립 관측이 존재할 수 있다" 쪽

- ★★ **X선 CT 접촉 피복 — OCV 와 독립인 접촉 관측이 존재한다, 단 척도가 판정을 정한다** (2026-09-23, 39호 Sakka et al. 2022). 싱크로트론 CT(화소 0.5 µm)가 NCM 표면의 LGPS 피복 `φ` 를 3D 로 준다 — 전기화학과 **독립인 첫 접촉 측정량**. ⚠ 신품 · 압력 축뿐(사이클 0) · 0 MPa(공극률 44 %)에서도 `φ` ≈0.78 — 1 µm 아래 틈은 "접촉" 으로 판정된다 · 같은 분할이 부피비를 ×2 흔든다 · `R_ct` 변화의 ≈4 %(로그)만 설명. ⇒ 이 채널이 가를 수 있는 것은 **µm 척도의 박리 · 틈**이고, 그 아래 척도의 접촉 손실은 이 채널에도 OCV 에도 안 보인다. 노화 셀에 쓰려면 **같은 셀의 사이클 전후 CT** 가 필요하다(이 편 0).

- ★★★ **이완 OCP 두 점 ↔ 저주파 EIS 꼬리 — 겉보기 감쇠를 "비활성 질량" 과 "경로 연장" 으로 사이클마다 가르는 두 채널** (2026-09-23, 38호 Conforto et al. 2021). `[인쇄]` 두 채널을 40 사이클 추적해 "the loss of active mass and the increase in length of lithium diffusion pathway" 로 용량을 분해한다(Fig. 9). 22호 신품 `θ ↔ η` 분할의 노화판이다 → **Q2 반 칸**. ⚠ 가르는 것은 `θ·ε_p` ↔ `η_diff` 이지 카드의 두 항이 아니다 · EIS 적합이 OCP 질량을 **고정 입력**으로 받아 두 채널이 `L/(C_diff√D̃)` 곱으로 묶인다(`[해석]`, 반무한 영역) · 닫힘이 (a) +12…+27 · (d) −14…−28 mAh g⁻¹ 어긋난다(`[도표]`). ★ 용량성 극한(`Z → 1/(iωC_diff)`)에 닿는 주파수 · 온도에서 재면 `C_diff` 단독이 **OCV 와 독립인 활성 질량** — 이완 게이지의 교차 검사가 된다(`[해석]`, 이 편은 닿지 않았고 고정했다).

- ★★★ **율 외삽 + 적합 공분산 진단 — 정적(`θ`+LAM) ↔ 동적(`η`) 을 가르는 싼 채널, 그리고 그 채널이 스스로 경계를 알린다** (2026-09-23, 29호 Yanev et al. 2024). CA 한 번(0.02 C 종료)이면 14 복합체의 `Q_M`·`α`·`n` 이 나오고,
  dependency ≈1 이 "이 셀의 `Q_M` 은 데이터가 정하지 않았다" 를 표시한다. ⇒ OCV 적합에 붙일 **사전 검사**로 쓸 수 있다: **종료 율에서 곡선이 평탄한가 · `Q_M`–`α` 상관이 1 에 가까운가**.
  ⚠ 진단 값은 SI(미열람) · 신품 · 조건당 1 셀 · LAM 과 `θ` 는 여전히 한 칸(`Q_M`). 이 채널이 가르는 것은 카드의 물음이 아니라 그 **앞 단계**(용량에서 `η` 를 빼는 것)다.

- ★★★ **첫 충전 비 — `θ` 형 불활성의 가장 싼 부정 시험** (2026-09-23, 25호 Zhou et al. 2025 · Fig. 2c 벡터 판독). 이온 경로에 안 닿는 CAM 은 **충전과 방전을 같이** 깎는다 ⇒
  두 전극의 첫 충전이 같으면 둘의 차는 `θ` 가 아니다. 30 · 10 MPa 에서 비 **1.03**, 2 MPa 에서 0.86 — `θ` 형 차이는 **저압에서만** 나타날 수 있고, DEM(운전 압력 없음)은 그것을 원리적으로 못 낸다.
  ⚠ 충전 = 방전/CE 로 복원한 값(원전 표 0), 셀 하나씩.
- ★★ **요인 설계(압력 × 미세구조)의 공통 모드 분리** (같은 편). 두 미세구조가 **같이** 받는 손해는 한쪽 미세구조의 접촉 손실이 아니다 — 25호에서는 초기 손해 전부가 이쪽이다.
- ★★★ **operando 깊이 분해 회절 — 두께 방향 `η(z)` 와 조각별 `θ` 형 모집단을 같은 측정이 담는다**
  (2026-09-23, 24호 Stavola et al. 2023 · 싱크로트론 EDXRD, 20 µm 조각). 투과 기하라 22호의 정보 깊이 문제(한쪽 면 3–15 µm)가 없고, 전위 없이 양극 결정을 읽어
  17호 함정과 독립이다. `[도표]` 한쪽 면만 보면 C/10 첫 충전 끝에서도 전극 평균과 `(1−x)` **±0.08**(Δx 의 ±20 %) 어긋나고 부호는 σ_el/σ_ion 이 정한다.
  ⚠ **원전은 이봉을 가중평균해 `θ` 를 다시 합쳤다** · 셀 1 개/조건 · 2 사이클 · 게이지 = 양극의 1.48 %(중앙 한 기둥) · 교정 오프셋 ≥0.02–0.05.
  ⇒ **"`θ` ↔ `η` 를 OCV 밖에서 가르는 operando 채널" 은 존재한다 — 두 봉우리의 scale 분율을 조각별·시각별로 보고하면.**

- ★★★ **양극 호의 `R`·`C` 동시 궤적 — 계면층과 접촉 면적을 임피던스 안에서 가르는 입력이 원전 SI 에 있다**
  (2026-09-23, 23호 Koerver et al. 2017 · SI Fig. S2 · S6 · S7). `[도표]` 첫 충전 3.25 → 3.53 V 에서 `R_SE/Cathode` ≈105 → ≈257 Ω(×2.45)
  동안 `C_SE/Cathode` ≈1.8 → ≈1.9 µF(×1.05); 둘째 충전 ×1.5 ↔ ×1.0; LTO 대조 첫 충전 ×1.7 ↔ ×1.0, 첫 방전 ×1.8 ↔ ×0.96. 면적 가설은
  `C` 를 ×0.41–0.66 으로 떨어뜨려야 한다 ⇒ **EIS 창 안의 양극 저항 증가는 화학(계면층) 형.** 그리고 S3 **무전류** 기계 이완에서 한 호가
  `R·C` 를 +5 % 로 보존 — **면적 서명이 이 복합체에서 실제로 나올 수 있다**는 부분 양성 대조. ⚠ 전제 `C ∝ 면적`(18·19호에서 깨짐) ·
  CPE → C 환산식 미상 · 호가 위상 ≤4° 에서 겹친다 · **가른 것은 `R` 변화분이지 용량이 아니다** · 원전은 이 조합을 만들지 않았다.
  ⇒ **"접촉 손실 ↔ 계면층" 은 2전극 EIS 로도 갈릴 수 있다 — 두 값을 상태축 위 연속으로 인쇄하면.**

- ★★★★ **회절 상 분율 — "물질은 그대로인데 쓰이지 않은" 양극 활물질을 전기화학 밖에서 잰다**
  (2026-09-23, 22호 Strauss et al. 2018 · 실험, ex situ XRD 2상 Rietveld · 1호의 ref 13).
  `[인쇄]` 첫 C/10 충전 뒤 충전된 상(`x ≈ 0.46–0.56`) 옆에 **pristine 격자 그대로인 상**이 남고, 그 분율이
  **2 / 27 / 31 %**(d₅₀ 4.0 / 8.3 / 15.6 µm). 측정 원리가 **상 분율**이라 용량이 입력되지 않고, 용량은
  **독립 대조**로 닫힌다(`[인쇄]` 90 / 92 / 153 ↔ 84 / 95 / 162 mAh g⁻¹). `[추론]` **이 셀을 OCV 로 적합하면
  NCM-L 에서 ≈31 % 의 `LAM_PE` 를 보고했을 것인데 물질은 전부 그대로다** — 닻 물음의 정확한 사례를 구조
  채널이 깬다. ★ 그리고 `[재현]` 불활성(`θ` ≈0.69)과 덜 충전(`η` ≈0.69)이 **같은 크기**로 따로 나온다 —
  3항 분해의 첫 실측 분리. ⚠ **ex situ · 파괴 분석 · 신품 한 점**이고, 잰 것은 **`1 − θ_AM` 의 합집합 상한**
  (전자 ∪ 이온 ∪ SE 접촉 ∪ 입자 내부)이며, `[재현]` Cu Kα 반사의 정보 깊이(≈3–15 µm)가 **집전체 면 표층**만
  본다. ⚠⚠ 1호가 이것을 "correlate well" 로 인용했지만 `[재현]` **무공극 상한(AM ≈48–50 vol%)에서 1호 식 (8)
  은 불활성 ≈23–40 / ≈95 / ≈95–97 % 를 예측** — 측정 2 / 27 / 31 %, **용량만으로도 ≤3 / ≤39 / ≤44 %** 로 기각된다.
  ⇒ **DEM `θ` 와 XRD `1 − f_inactive` 를 잇는 관측 연산자 없이 등치하지 않는다.**

- ★★★★ **세 번째 전극(전위 채널) — 이 계보에서 가장 직접적인 분리 관측**
  (2026-09-22, 17호). 16호가 임피던스를 전극별로 갈랐다면 **17호는 전위를 전극별로
  가른다**, 그리고 그 판독은 **적합의 출력이 아니라 전압계의 출력**이다 —
  **축퇴할 자리가 없다.** `[재현]` 자기 검증도 성립한다:
  `Z_WE/CE ≈ Z_WE/RE + Z_CE/RE` 가 **2 Hz 에서 두 셀 다 1 % 안**
  (⚠ foil 의 고주파 절편만 7 % 어긋난다 — 음극 임피던스가 거대해 3전극 아티팩트가
  가장 크게 생길 조건이고, **논문은 이 합산 검사를 하지 않는다**).
  ⚠ **그러나 이것이 `LAM_PE` ↔ 접촉 손실을 가르지는 않는다.** 가르는 것은
  **양극 ↔ 음극**이다. **양극 안의 두 기구는 여전히 한 스펙트럼 안에 있다**
  (10호의 `R_MF` 경고 그대로). ★ 그리고 17호가 **반대 방향의 경고**를 하나 더 준다 —
  `[인쇄]` "the **deconvolution of half-cell impedance spectra** … could be **severely
  complicated by overlapping anode impedance**" ⇒ **3전극이 없으면 양극 스펙트럼에
  음극이 얼마나 섞였는지조차 모른다.** 9·16호의 양극 적합이 딛는 자리다.
- ★★★ **`R_CT · C_dl` 채널 — 접촉 면적이 소거되는 조합** (2026-09-22, 16호에서 유도).
  계면의 실제 접촉 분율을 `θ` 라 하면, 가정 면적으로 정규화한 측정값은
  `R_CT^meas = R_CT^true/θ` 이고 `C^meas = θ·C^true` 이므로 **곱 `R_CT·C` 에서 `θ` 가 사라진다.**
  ⇒ **`R_CT·C` = 접촉-무관 고유 시상수(동역학), `C` 단독 = 접촉 면적 비례(기하).**
  **둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**
  ★ 16호는 **두 값을 다 갖고 있으면서**(Table 2 의 `R_CT`·`Q_DL`) **그 조합을 만들지 않는다.**
  `[재현]` 만들어 보면 두 압력에서 `R_CT·Q` 가 **1.7 배**(유효용량 변환 시 3.1 배) 달라서
  **순수 면적 효과만으로는 설명되지 않는다** — 즉 이 채널은 실제로 **정보를 가지고 있다.**
  ⚠ 단서: CPE 지수 `β` 가 다르면 변환이 모형 의존적이다(Brug 등). **우리가 아직 재지 않았다** —
  여기 적는 것은 **설계**다. → [[assb-lampe-contact-product-degeneracy]] §처방표.
- **ex situ XRD 의 inactive AM 분율** = 원리적으로 `1 − θ_AM` 의 **measured 라벨**
  (Strauss et al., ACS Energy Lett. 2018, 3, 992−996; Bielefeld 2019 ref 13).
  액체셀에서 우리를 막았던 "measured 라벨 없음" 이 여기서는 **존재할 수 있다.**
  ⚠ 단 Bielefeld 는 그 대조를 **정성적으로만** 했고 스스로 무효화했다 —
  `[인쇄]` "the total packing density of AM used by Strauss et al. is not known,
  **as the porosity was not measured**".
- ★ **율(rate)이 세 항 중 하나를 지운다** (2026-09-16, Clausnitzer 2023 에서 우리가 추론).
  논문이 인쇄한 두 문장을 붙이면 분리 시험이 나온다 —
  `[인쇄]` "At **lower current densities** … **reduced sensitivity to microstructural
  variations**" + `[인쇄]` `R_GB,3` 에서 CAM 의 큰 부분이 방전 끝에도 **초기 Li 농도 그대로**
  남는다 (Fig. 5 히스토그램: `x ≈ 0.52` 에 큰 봉우리).
  → **진짜 `LAM_PE` 와 기하 접촉 손실은 `i→0` 에서 남고, 동역학 손실은 사라진다.**
  **최소 2 개 율에서 같은 파라미터를 적합하고 `a_PE` 차이를 보고하면** 동역학 성분의
  하한이 나온다. ⚠ **그러고도 `θ_AM · Q_material` 의 곱은 안 갈라진다** — 이 물음의 본체는
  살아 있고 **범위만 좁아진다.** 자세히는 [[assb-apparent-capacity-decomposition]].
- **제안된 독립 관측 하나가 늘었다**: **복합양극 EIS 의 이온·전자 부분 전도도**
  (Minnmann et al. 2021, ref 22). Clausnitzer 가 결론에서 **자기 검증의 첫 단계**로
  지목한다 — `[인쇄]` "impedance measurements for LCO/LLZO composite cathodes could be
  conducted to determine the ionic and electronic partial conductivities".
  ⚠ 단 **LLZO 계 측정은 문헌에 없다**고 같은 문단이 적는다.
- ★★ **압력 재인가 — 이 계보 최초의 "실제로 수행된" 분리 조작** (2026-09-16, Shi 2020).
  ex situ XRD 도 EIS 도 **관측**이지만, 300 MPa 재가압은 **개입**이다:
  **진짜 재료 손실(rock-salt·구조 붕괴)은 눌러도 안 돌아오고 접촉 손실은 돌아온다.**
  → `ΔQ_mech ≡ Q(P_high) − Q(P_low)` 가 **기하 접촉 손실의 용량 등가에 대한 상한**,
  따라서 **진짜 `LAM_PE` 의 하한**을 준다. 율 연산자와 짝이 된다:

  | 조작 | 지우는 항 | 근거 | 비파괴? |
  |---|---|---|---|
  | `i → 0` | `η(i)` | 2호(추론) → 3호(율 스윕 20 곡선) | ✅ |
  | **`P ↑`** | **`θ_AM`** | **4호 (실측 1 사례)** | ❌ 되돌릴 수 없다 |
  | 둘 다 하고 남는 것 | `Q_material` = 진짜 `LAM_PE` | — | — |

  자세히와 네 개의 경고는 [[assb-pressure-reapplication-separation-test]].
  ★ `[해석]` **이것이 이 카드의 답을 바꾸지는 않지만 우회로를 연다** — OCV **모양**
  으로는 못 갈라도, **압력 축을 하나 더 걸면 같은 셀 안에서 분해가 된다.**
- ★ **율 극한 논증이 실험에서 간접 검증됐다** (2026-09-16, Shi 2020).
  4호 셀의 율은 `[재현]` **≈C/15** 로 2호(≈0.74 C)·3호(0.25–5 C)보다 한 자릿수 낮다
  → `η ≈ 1` 이어야 한다. 그런데 겉보기 용량이 **≈98 %** 날아갔고 압력으로 **60 %p** 가
  돌아왔다. `[해석]` **저율에서도 살아남는 손실 = 기하 성분**. 2호의 분리 시험이
  예측한 그대로다. ⚠ 단 4호는 **율 스윕을 하지 않았다** — 직접 증명이 아니다.
- ★ **새 관측 후보: 충전 전압의 비단조 진동** (2026-09-16, Shi 2020 ESI Fig. S1(c) 인셋).
  `[도표]` 급락 직전 사이클(38·39)의 충전 곡선이 **단조 상승이 아니라 톱니**로 흔들린다.
  ESI 캡션 `[인쇄]`: "the voltage curve becomes **unstable** … **jumping up and down** …
  can be explained by the **intermittent Li transport to and from the
  contracting/expanding cathode particles**."
  `[해석]` **곡선의 모양(용량축·전압축)이 아니라 국소 비단조성이 관측량이다.**
  OCP 적합에서는 **잔차의 고주파 성분**으로 나타나고 보통 노이즈로 버려진다.
  액체셀에는 이 서명이 없다(전해질이 늘 젖어 있다) → **`assb` 전용 판별 feature 후보.**
  ⚠ 크기가 수치로 보고되지 않았고(figure-read 로 대략 ±50–100 mV) 셀 1 개의 5 사이클
  구간에서만 보였다.

- ★★★★ **"계면 하나만 추가" 대조군 — 접촉을 아는 대조군의 교과서적 형태**
  (2026-09-22, 19호 Yoshida 2024). 18호 검사 A 가 가르쳐 준 것은 **처방을 쓰려면
  면적을 아는 대조군이 필요하다**였고, 18호의 대조군(신품 입자 크기 2 종)은 **실패**했다.
  19호가 그 자리의 대안 설계를 보인다: `[도표]` **LPSCl 펠릿 한 장 안에 RE 둘을 함께
  성형한 셀에는 `P2` 가 없고**(Z′ 72→162 Ω, P1 + P3 만), **같은 LPSCl 펠릿 두 장을 포갠
  셀에는 `P2` 가 생긴다**(≈8 Ω).
  ⇒ **같은 재료 · 같은 공정 · 계면 하나만 다른 두 셀.** 복합양극 판으로 옮기면
  **같은 활물질·SE·공정에서 계면 수/면적만 바꾼 전극 쌍**이고, 그것이 `θ` 를 아는
  유일한 실험적 통로다.
  ⚠ 단서 셋: 두 셀의 `R₁` 이 **162 ↔ 291 Ω** 로 1.8 배 달라 `d`·`S` 가 다르고(값 미인쇄),
  `P3` 가 양쪽에 다 있으며 크기가 다르고, **n = 1** 이다.

- ★★★★ **면적-불변 채널 `Ea` — `C_dl` 을 쓰지 않는 두 번째 분리 관측**
  (2026-09-22, 19호). `[도표]` 압력 560→840 kPa 에서 `R₂` **−26 %** 인데
  `[인쇄]` "the **physical state of the interface does not affect the Ea** but the
  resistance values. It is thus proposed **Ea as the essential parameter** …"
  ⇒ `R(T) = A(θ)·exp(Ea/RT)` 에서 **`Ea` 는 접촉 면적과 직교한다.**
  ⇒ **노화 전후 `Ea` 를 같이 재면**: `Ea` 불변 + `R` 증가 ⇒ **면적/기하 쪽**과 양립 ·
  `Ea` 증가 ⇒ **화학/장벽 쪽**(면적만으로 설명 불가).
  ★★ **그리고 `C_dl ∝ θ` 라는 (두 번 깨진) 전제를 쓰지 않는다** — 19호에서 그 전제는
  `[재현]` **`P2` 의 `C` 가 기하 면적 기준 2.0–4.8 mF cm⁻² = 이중층의 200–480 배**로
  **물리 상한을 2–3 자릿수 초과**해 반증됐다.
  ⚠ **충분조건은 아니다** — `A` 에 면적 외 항이 있다. 19호 자신이 반례다:
  `[재현]` 세 계면의 `τ` 가 ±13 % 안(= `C` 는 면적 차 **2.4 배**를 말함)인데
  `Ea` 는 15 kJ mol⁻¹ 갈려 전지수 인자 **158–174 배** 보상이 필요하다 ⇒ **두 채널이
  70 배 충돌한다.**
  ⚠⚠ 그리고 19호의 `Ea` 불변 근거 자체가 **2 점 · n=1 · 범위 1.5 배**이고,
  같은 편이 드러낸 `Ea` 산포(**≥5 kJ mol⁻¹**)를 쓰면 **3 kJ mol⁻¹ 변화는 못 본다.**
  → [[assb-lampe-contact-product-degeneracy]] 처방에 줄로 등록.

### 우리 계획에 붙은 새 제약 (2026-09-16)

- ★ **DEM 라벨 자체가 폭을 갖는다.** Bielefeld 가 인쇄한 실측: 거시 파라미터를 전부
  고정해도 무작위 충전 배열만 바꾸면 임계 근방에서 `θ_AM` 이 **≈30 % ↔ ≈70 %** 로
  이봉으로 갈린다. → **DEM 산출을 라벨로 쓰려면 반드시 폭을 붙인다**
  (`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §5 의 규율을 우리 자신에게).
  그리고 **임계에서 멀리**(`p − p_c ≳ 5 vol%`) 작업해야 한다.
- **DEM 도메인 크기 수렴 시험이 선행 조건**이다 — Bielefeld Fig. 10 의 유한 크기 효과가
  얇은 도메인에서 `θ` 를 낙관 방향으로 편향시킨다.
- `θ_AM` 의 **시간 변화는 아직 아무도 안 줬다.** Bielefeld 는 pristine 정적 기하만 준다.
  ⚠ **2호를 읽고도 그대로다** — Clausnitzer 도 `[인쇄]` "pore formation during cycling …
  **beyond the scope**" · "our current model **does not incorporate mechanics**", 방전
  **1 회**. **`assb` 2/2 편이 시간축을 주지 않았다.** 다만 2호의 **소결 밀도 `ρ_S` 스윕**
  (60–93.1 %)이 **후보 대리 축**이다 (Fig. 8 이 그 지도). ⚠ 제조 공극과 사이클 균열은
  **공극의 분포**가 다를 수 있다 (사이클 균열은 CAM/SE 계면에 우선).
- ★ **산포 규율이 후속 논문에서 지켜지지 않았다.** Bielefeld 는 `θ` 의 실현 간 폭을
  인쇄했는데, Clausnitzer 는 **오차 막대 0 개 · 점당 구조 1 개**이고 도메인이
  `[재현]` **1/28.7 부피**로 더 작다. → **2호 Fig. 10 의 최적 순위(0.94/0.93/0.89)는
  신뢰 근거가 그 논문 안에 없다.** 우리가 N 개 실현으로 **싸게 무효화/검증할 수 있는 자리.**
- **`θ` 는 스칼라가 아니다** (2호가 추가): `[인쇄]` "The share of unconnected clusters
  **increases with increasing distance from the separator**" — `θ_SE(z)` 가 집전체 쪽에서
  떨어지고, `[도표]` Fig. 8b 에서 `SVF 69.4 %`·밀도 70 % 는 **전극의 90 % 가 이용률 ≈0** 이다.
  → forward model 에 `θ` 를 스칼라로 넣으면 집전체 쪽 손실을 **과소평가**한다.

### 새 제약 (2026-09-16, Liu 2024)

- ★★ **율 스윕 분리 시험이 좁아졌다.** [[assb-apparent-capacity-decomposition]] 의 처방
  ("두 율에서 적합 → `a_PE` 차이 = 동역학 성분의 하한")은 **`Q_material` 이 율에
  무관하다**는 전제 위에 있었다. 3호가 그 전제를 깬다 — `[도표]` Fig. 5e: 12 µm 에서
  활물질 손실이 **0.25C 0.093 → 5C 0.185 (2 배)**. **고율 방전 자체가 진짜 재료 손실을
  더 만든다.** → 살아남는 설계는 (a) **저율 쌍만** 쓰거나 (b) **율을 바꾼 뒤 기준 율로
  돌아와 이력을 재서** 비가역분을 빼는 것. 후자가 안전하다.
- ★ **`θ` 는 양극만의 성질이 아니라 (양극 × 전해질) 쌍의 성질이다.** `[도표]` Fig. 4f·7c:
  같은 양극·같은 운전조건에서 전해질 Young 률을 1 → 150 GPa 로 바꾸면 계면 응력이
  **0.05 → 0.55 GPa (≈8 배)**, 벌크 응력은 +0.75 → −1.5 GPa 로 부호가 뒤집힌다.
  → forward model 에 접촉 손실을 넣을 때 **전해질 탄성률·항복강도가 상태변수**다.
- ★ **`η` 의 지배 인자가 두 척도에 걸쳐 있다.** 전극 척도의 입계 저항(2호 `R_GB`)과
  **이차입자 내부 입계 확산도**(3호 `D_GB`) 둘 다. `[도표]` `D_GB` 를 0.05 ↔ 20 배로
  바꾸면 1C 용량이 **0.48 ↔ 0.985** — 재료도 기하도 같은데 겉보기 용량이 두 배다.
  그리고 **OCV 로는 안 보인다.**
- ★ **산포 규율이 3/3 편에서 안 지켜졌다.** 1호만 실현 간 폭을 쟀다. 3호는 본문에
  `[인쇄]` "the **random arrangement** of primary particles … play a critical role in
  dislocation heterogeneity" 라고 적고도 **실현 1 개**다 (`seed`·`standard deviation`·
  `error bar` 각 0 회). Fig. 3j·4e 의 분포는 **한 구조 안의 공간 분포**이지 실현 분포가
  아니다. → 우리가 N 개 실현으로 싸게 검증할 수 있는 자리가 하나 더 늘었다.
- **재현 가능성 원장에 새 표본**: 3호의 Code Availability 는 공개 DAMASK v2.0.2 를
  가리키지만 **이 연구가 쓴 코드는 별 저장소의 `plasticity_chemo_mechanics` 브랜치이고
  기관 허가 + CLA 승인이 있어야 접근된다**. 공개본(2018-05-22)에는 `lithium`·`intercalat`
  이 0 건이고 논문이 "developed" 라고 적은 **독립 FEM 솔버도 없다**.
  (상세는 3호 digest §6·§13 D16.)

### 새 제약 (2026-09-16, Shi 2020 — 실험이 들어오면서 붙은 것)

- ★★ **접촉 손실 라벨을 "면적" 으로 받으면 안 된다.** 4호가 실측으로 보인 6 배 간극
  (위 For 반례). **DEM 이 주는 것도 대개 접촉 수·면적**이므로 이 제약은 우리 계획에
  직접 걸린다 → **면적 → 이용 가능 용량 사상을 우리가 세워야 하고, 그것이 비선형이다.**
- ★ **실측 라벨에도 폭이 없다 — `assb` 4/4 편 연속.** 4호는 실험인데도
  `error bar` · `standard deviation` · `uncertain*` · `replicate` · `seed` **전부 0 회**
  (본문+ESI), 조건당 **셀 1 개**. 게다가 **분할(Weka ML) 정확도 수치가 없고**
  `[도표]` Fig. S2 에서 **CNF 와 LPS 회색도가 크게 겹친다** — ESI 스스로 오분류가
  `[인쇄]` "especially within the **boundaries**" 에서 난다고 적는데,
  **접촉 손실은 정확히 그 경계에서 재는 양이다.**
- ★ **검출 한계가 결론을 만들 수 있다.** 4호의 결론 `[인쇄]` "mechanical degradation
  **does not progress gradually**" 는 사이클 10 의 void 증가가 `[도표]` **+0.36 %p**
  뿐이라는 데 기댄다. 그런데 같은 논문이 뒤에서 `[인쇄]` "very small microfractures …
  **undetectable by the tomography**" 라고 적는다. **두 문장은 같이 설 수 없다.**
  → `[해석]` **우리가 싸게 공급할 수 있는 것**: 검출 한계(50 nm 슬라이스·면내 화소
  미명시)를 넣은 전방 모형으로 **"계단" 이 실재인지 아티팩트인지** 가르기.
- ★ **`θ(N)` 을 부드러운 함수로 매개화하면 안 된다.** 4호가 준 시간축은 **계단**이다
  (void 2.87 → 3.23 → 9.50 vol%; 용량은 사이클 ≈28–45 에 붕괴). 지수·멱 감쇠로는
  원리적으로 못 맞춘다.
- ★ **셀 간 산포가 구조적으로 크다.** 4호는 `[인쇄]` "the sudden drop … could be found
  **earlier or later**" 라고 적고, `[도표]` Fig. 1(a) 셀은 ≈2 mAh g⁻¹ 까지 바닥까지
  가는데 Fig. S1(a) 셀은 **사이클 39→40 한 번에 ≈84 → ≈43** 후 ≈27 에서 안정한다.
  **붕괴의 시간 구조가 셀마다 다르다.** → `θ(N)` 은 결정론적 곡선이 아니라 **확률변수**다.
  ⚠ 그런데 논문은 산포를 **한 번도 정량하지 않는다.**
- **재가압은 일회성 조작이다.** `[도표]` 재가압 후 5–6 사이클에 80 → **≈64 mAh g⁻¹**
  (`[재현]` ≈3 mAh g⁻¹/cycle = 초기 감쇠율의 **3 배**). 원문은 이 재감쇠를 언급하지
  않는다. → 분리 시험 설계에서 **압력 조작은 맨 마지막에 한 번**이어야 한다.
- **EIS 의 식별성이 새 전선이다.** `[인쇄]` "not possible to precisely assign a single
  frequency region … because of the **overlapping time constants**" 라고 적고도
  `R_MF` 954 → 3283 Ω 를 점추정으로 쓴다. → **우리 폭 측정기
  ([[near-optimal-set-width-measurement]])를 3-RC 등가회로에 그대로 걸 수 있다** —
  "244 % 증가" 가 유의한지가 판정 가능한 질문이 된다.

### 새 제약 (2026-09-16, Doux 2020 — 압력 스윕이 들어오면서 붙은 것)

- ★★★ **`P↑` 처방에 안전 한계가 붙는다**: `P_low < P_high < P_short(음극 재료,
  전해질 공극률, 전류밀도)`. Li 금속 + 황화물에서 `P_short ≈ 75 MPa` 이하이고
  25 MPa 도 48 h 밖에 못 버틴다. → **Li 금속·무음극 셀에서는 4호식 재가압 시험을
  그대로 못 쓴다.** 자세히는 [[assb-stack-pressure-operating-window]].
- ★★ **`θ_AM(P)` 을 단일값 함수로 쓰면 안 된다 — 이력이 있다.** 처녀 5 MPa 110 Ω ↔
  25 MPa 경유 후 5 MPa ≈50 Ω, `[재현]` 계면 과잉의 **77 % 가 영구 제거**.
  → 압력 스윕 실험은 **스윕 방향과 이력을 반드시 기록**한다.
- ★ **압력 축의 정보는 저압에 있다.** `[재현]` 계면 과잉이 15 MPa 에서 8 Ω,
  20 MPa 에서 3 Ω → 20 MPa 위는 벌크가 전부다. → [[near-optimal-set-width-measurement]]
  에 압력 2 점을 넣는다면 **(5, 25) 가 아니라 (1–2, 10–15)**.
- ★ **산포를 우리가 전파할 수 있다 — 그리고 문헌에 그 입력이 있다.** 5호 Table S2 가
  **펠릿 4 개**의 상대밀도를 인쇄한다 (80.2 / 84.9 / 80.3 / 83.0 %; `[재현]` s ≈2.3 %p
  → **공극률 15.1–19.8 %**). ★ `assb` **5 편 중 첫 반복 측정**이다.
  단락 기구가 **기공 퍼콜레이션**이므로 이 폭이 `t_short(P)` 로 증폭되는데
  **논문은 전파하지 않는다** (6 점 전부 N=1). → 이 저장소의 DEM/MPM 계열(타 브랜치)로
  **싸게 공급할 수 있는 자리**다.
- ★ **진단 feature 후보 둘이 늘었다.**
  ① **단락 전조로서의 임피던스 "감소"** — `[도표]` 5호 Fig. S2(본문 미인용):
  25 MPa 셀의 고주파 절편이 0/10/20 h 에 **36.6 → 34.3 → 30.7 Ω (−16 %)**,
  **단락 28 h 전**이다. 액체셀 소프트숏은 보통 CE 하락으로 오는데 여기서는
  **저항 자체가 내려간다** → `assb` 전용 서명 후보.
  ② **충전 곡선의 계단식 붕괴** — `[도표]` 5호 Fig. 1 의 Li 금속 셀이
  3.8 → **≈1.85 V 평탄부** → **≈1.2 V 평탄부** 로 내려간다 (본문은 "plummet" 한 마디).
  4호의 **비단조 진동**과 같은 계열이고 크기가 훨씬 크다.
- ⚠ **"압력이 높으면 좋다" 는 어느 쪽으로도 단순하지 않다.** 4호는 300 MPa 로
  용량을 살렸고 5호는 75 MPa 로 셀을 죽였다. **작용 지점이 다르기 때문이다**
  (양극 복합체 vs 음극/전해질 기공). → 압력을 상태변수로 넣을 때 **전극별로 다른
  부호**를 갖는다고 적어야 한다.

### 새 제약 (2026-09-16, Lee 2020 — 무음극이 들어오면서 붙은 것)

- ★★★ **"무음극은 OCP 가 평탄하다" 에 조건이 붙는다.** Ag–C 무음극에서
  `[인쇄]`+`[도표]` **앞 9.5–16.6 % 의 용량 동안 음극 전위가 ≈1 → 0 V 를 훑는다**
  (Fig. 4a 의 컷오프 5 점 사상 + SI Fig. 4c 의 Ag–C\|Li 반쪽전지).
  → `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 **3 파라미터 창 모형**
  (`a_PE, b_PE` + 평탄 상대극)은 **전압창 전체에 걸면 안 되고 3.6 V 위에서만** 성립한다.
  ⚠ 그리고 그 구간의 **모양이 음극 조성의 함수**다 (`[인쇄]` SI Fig. 14: Ag 를 늘리면
  3.5 V 부근에 작은 평탄역이 생긴다) → **음극 조성이 완전지 곡선 모양의 상태변수**다.
- ★★★ **제작 압력과 운전 압력은 다른 연산자다.** 위 미결 항목 4 참조.
  [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는 **이 셀에 적용
  불가**다 — 4호가 쓴 **300 MPa 는 이 셀 운전 상한(4 MPa)의 75 배**다.
  ⚠ 모집단이 다르다(펠릿 vs Ah 급 파우치 적층). 방향은 **무음극·대면적으로 갈수록
  운전 압력 창이 좁아진다.**
- ★★ **압축의 비가역성이 기하 채널에서도 확인됐다.** `[인쇄]` Table S2:
  WIP(490 MPa) 전후 셀 두께 **644.5 ± 2.9 → 609.0 ± 2.4 µm** (`[재현]` −5.51 %),
  **7 일 무압 방치 후 609.8 ± 2.6** (복원 +0.8 µm, 산포 안).
  → 5호가 임피던스로 준 `θ(P)` 이력(경로 의존)의 **독립 확인**이다.
  `[해석]` **제작 압력은 "한 번 치르는 비용" 이고 상태에 영구히 남는다.**
- ★★ **`LLI` 추정자의 분해능이 판정 대상이다.** [[near-optimal-set-width-measurement]]
  를 그대로 건다: "CE 99.8 % 와 99.99 % 를 구분할 정보가 자료에 있는가."
  6호의 두 셀(20 mAh 맞음 ↔ 0.6 Ah 10 배 어긋남)이 **정답이 있는 시험 문제**다.
- ★ **음극이 시간에 따라 바뀌는 재료다.** `[인쇄]` Ag 가 **매 사이클 집전체 쪽으로
  이동하고 돌아오지 않는다**(Fig. 3e,f 의 Top/Middle/Bottom 분포 변화).
  → [[halfcell-ocp-shape-invariance]] 의 "모양 불변" 가정이 **ASSB 무음극에서는
  음극 쪽에서 먼저** 깨진다.
- ★ **산포 규율이 6/6 편에서 안 지켜졌다.** 6호는 **산업체 · *Nature Energy* ·
  Ah 급 파우치 스케일업**인데도 `n =`·`N =`·`error bar`·`standard deviation`·
  `replicate`·`uncertain*` 이 **본문 10 쪽 + SI 18 쪽 전수 0 회**다. 유일한 산포는
  **Table S2 의 ±2.2–2.9 µm**(정의도 n 도 없다) — 5호 Table S2 에 이어 **두 번째이고
  둘 다 전기화학이 아니라 기하다.**
  ⚠ 정성적 산포 언급 둘(`[인쇄]` ">4 MPa 에서 단락 **확률** 증가", "C 단독에서 단락이
  **쉽게** 발생")은 **분모를 밝히지 않는다.**
- ⚠ **초록의 두 수치가 같은 셀의 것이 아니다.** `[인쇄]` ">900 Wh l⁻¹" 는
  **5 Ah 10-적층셀**(0.05 C, **무압**, 942)이고 `[인쇄]` "1,000 cycles" 는
  **0.6 Ah bi-cell**(0.5 C, 2 MPa, **703** Wh l⁻¹)이다. → **문헌에서 성능 수치를
  옮길 때 셀을 확인한다.**

### 새 제약 (2026-09-16, Spencer-Jolly 2023 — operando 회절이 들어오면서 붙은 것)

- ★★★ **음극에 OCP 가 하나가 아니다.** 충전용과 방전용이 따로 있어야 한다
  (충전에 없는 상이 방전에 있고, 그것이 **열역학적**이다). → ASSB 인수인계 노트 §1
  의 3 파라미터 창 모형은 **방향별로 따로 적합**해야 하고, 그 둘의 차이를 "열화" 로
  읽으면 **없는 열화를 만든다.**
- ★★ **모집단 경계가 넷이다** — 6호와 7호는 같은 재료계가 **아니다**:
  **탄소**(카본블랙 ↔ **흑연**) · **상대극**(완전지 ↔ **반쪽전지**) ·
  **사이클 수**(1000 ↔ **1**) · **제작 압력 방식**(등방 490 MPa ↔ **일축 400 MPa**).
  → **7호의 "Ag 는 임계전류를 못 올린다"(<2.5 mA cm⁻²)는 흑연 계의 판정**이고,
  6호의 3.2 mA cm⁻² × 1000 사이클과 **모순이 아니다** — 7호 자신이 `[인쇄]`
  "the **type of carbon chosen will have a significant impact**" 라고 적는다.
  **문헌에서 재료계 결론을 옮길 때 탄소 종류를 먼저 확인한다.**
- ★★ **Ag 의 시간 도함수는 여전히 없다.** 7호가 준 것은 **칸 사이의 화살표(경로)**
  이지 **그 시간 변화율**이 아니다 — `[도표]` Fig. 6 D→E→F 가 **1 사이클**이고,
  복귀율이 `[인쇄]` "a **return to a near-pristine state**" 라는 형용사 한 마디다.
  6호의 "100 사이클에 돌아오지 않는다" 와 **모순이 아니라 시간척도가 다르다.**
  → **사이클당 Ag 잔류를 재는 것이 여전히 비어 있는 자리다.**
- ★ **인쇄된 수치도 검산해야 한다.** `[인쇄]` "maximum capacity stored by alloying
  with Ag (approx. **0.60 mA h cm⁻²**)" 를 `[재현]` 자기 조성(5 µm · 5.7 vol% Ag)과
  Li₁₀Ag₃ 화학량론으로 재계산하면 **0.25** 다 (**≈2.4 배**; Ag 당 Li 8.3 개가 필요한데
  상평형 최대가 3.33 이다). **같은 문장의 흑연 0.28 은 `[재현]` 0.33 으로 맞는다.**
  → **이 값을 그대로 인용하면 안 된다** (7호 digest D2).
- ⚠ **산포 규율이 7/7 편에서 안 지켜졌다.** 7호도 `n =`·`N =`·`error bar`·
  `standard deviation`·`replicate`·`uncertain*` 가 **본문 13 쪽 + SI 6 쪽 전수 0 회**다.
  `[인쇄]` "Graphite alone and Ag-graphite composite layers were observed to have the
  **same failure point**" 가 **각 1 셀 비교**로 보인다.
  ★ **단 하나 나아진 것**: `[인쇄]` 원자료가 **Oxford Research Archive
  (DOI 10.5287/bodleian:kKBPZ282m)** 에 공개돼 있다 — **이 계보에서 자료를 공개
  저장소에 올린 첫 편**이다. (우리가 산포·검출한계를 직접 잴 수 있는 자리.)

### ★ 아홉 번째 — **반례도 근거도 아닌, 계보의 출발점을 날짜로 찍는 표본** (2026-09-22, Sadegh Kouhestani et al. 2022 · ⚠ Review, 1차 측정 0)

`raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`
(*Energies* **15** (2022) 6599; 본문 26 쪽, SI 없음, sha256 봉인). **수치는 전부 재인용이고
이 절에서 쓰는 것은 수치가 아니라 "2022 년 PHM 종설이 무엇을 어휘로 갖고 있었는가" 다.**

**(가) ★★★ 이 카드의 물음이 분류 차원에서 지워진 자리를 찍는다.**
`[인쇄]` §2.2 "**The loss of active materials mainly stems from the electrical contact
loss** that is caused by graphite spalling, adhesive decomposition, collector corrosion,
and electrode particle cracking." → 이 리뷰의 어휘에서 **`LAM ⊃ 접촉 손실`** 이다.
`[해석]` 3호(Liu 2024)가 `[인쇄]` "실험의 활물질 손실은 rock-salt + 파괴로 고립된 활물질을
둘 다 포함한다" 고 **실험의 한계로** 적은 병합을, 이 종설은 **정의로** 한다. 우리가 가르려는
두 양이 **PHM 문헌에서는 처음부터 한 낱말**이었다는 것 — 그리고 그 낱말의 기구 목록이
**전부 액체셀**(흑연 박리·바인더·집전체 부식·입자 균열)이고 `[도표]` Fig. 6 의 "Contact
Loss" 두 자리도 **Cu/Al 집전체**라는 것. **복합양극 AM|SE 계면은 이 리뷰에 없다.**

**(나) ★★ Q4 계보의 "1–7호 상태(안 쟀다)" 가 PHM 쪽에서도 같은 시점에 성립했음을 확인한다.**
`identifiab*` **0 회** (8호 Li 2026 은 5 회). 가장 가까운 문장이 `[인쇄]` "difficult parameter
identification" — **실무 곤란**으로만 — 과 `[인쇄]` "large number of parameters … inevitable
errors in each parameter" 이고, **같은 논문 §3.1.3 이 정반대**를 인쇄한다: `[인쇄]`
"Generally, **the more parameters** that are involved in the model, **the higher the
accuracy** of the model." → **모델 차수에 대한 두 방향 명제가 한 논문 안에서 화해되지
않은 채 있다.** 이것이 2022 년의 상태다.

**(다) ★ "모델 차수는 상태변수" 의 세 번째 독립 인쇄 — 단 액체셀 ECM, 재인용.**
`[인쇄]` §3.1.2 "the aging or temperature change of the LIB will cause the internal
impedance characteristics of the battery to change **from a single impedance arc to a
double impedance arc**, which significantly impacts the accuracy of the battery model [84]."
10호(Larfaillou 2016 재인용, LiPON RQ 3→4) · 11호(1차 DRT, 2–3→5) 에 이어 **셋째**.
⚠ ref [84](Cho 2012)가 실제로 그것을 보였는지는 원전 확인 전이다 →
[[drt-peak-count-nonidentifiability]].

**(라) ★★ `A_eff` 형 접촉 파라미터의 계보 입구.**
`[인쇄]` §3.1.1 "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe
the contact area, which adjusts the current density in the 1-D Newman model**. They found
that the capacity drop was correlated with the loss of contact area, and the optimal
charging performance could be obtained under medium compressive pressures (0.4–1 MPa)."
`[해석]` 9호(Huo 2025) Table 1 의 `A^p_eff`(BV 분모의 유효 접촉 면적비)와 **형태가
같다**. [[assb-lampe-contact-product-degeneracy]] 가 손으로 보인 `A_eff·ε_p/R_s` 곱 축퇴가
**2017 년 모델 형태에서 시작됐을 가능성**. ⚠ 두 저자에 같은 번호 [60] 이 붙어 있어
(digest D4) **`0.4–1 MPa` 의 출처는 이 지면으로 확정되지 않는다.** 원전 둘(Tian & Qi
*JES* 2017, 164, E3512 · Shao *Energy* 2022, 239, 121929)을 받아야 한다.

**(마) "라벨이 없다" 의 2022 년 판.** `[인쇄]` "very few instances where a battery can be
completely exhausted or fully charged at the pack level"(재인용, Yang 2021) ·
`[인쇄]` §4 "**most PHM techniques are based on simulation results and not
experimental**"(1차) · 결론 (1) `[인쇄]` "primarily used to estimate the **SOC** of SSBs" ·
(2) "very few studies … **lack of accurate data**". → **8호의 "no direct capacity labels"
와 같은 명제가 다른 원전에서 4 년 앞서 나온다.** 그리고 우리가 Table 1 을 한 줄씩 대조한
결과(digest §Table 1 해체) **SSB 실측 열화 데이터로 SOH/RUL 을 추정한 항목은 0 / 28** —
논문 자신의 결론과 일치한다.

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 이 편은 근거를 주지 않는다 —
**우리 물음이 문헌에서 어떤 어휘 상태에서 출발했는가**를 날짜와 함께 고정한다. 그것이
종설 두 편(8호·12호)을 넣고 얻은 것이다: **2022 → 2026 사이에 PHM 문헌은 "identifiability"
라는 이름을 얻었고(0 → 5 회), 여전히 재지는 않았다.**

### ★ 열 번째 — **근거가 아니라 "운전 조건이 OCV 채널을 설계상 닫는다" 는 요구 측 진술** (2026-09-22, Zheng et al. 2026 · ⚠ Perspective, 1차 측정 0, `[인쇄]` "No data was used")

`raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (*Energy* 345, 140229; Nanjing Tech +
Huadian 전력연구원 + Shuangdeng 전지 제조사 — **저자 소속이 수요 측**이다).

**이 편이 이 카드에 하는 일은 근거 추가가 아니라 "물음이 놓일 운전 조건" 을 인쇄한 것이다.**
세 문장이 한 문단에 있다 (§4):

1. `[인쇄]` "grid batteries rarely perform full cycles between 0 % and 100 % SOC. Instead, they
   operate within a limited window (e.g., **20–80 % SOC**) … making it **impossible to obtain a
   full open-circuit voltage (OCV) curve** for calibration."
2. `[인쇄]` "the **flat voltage profiles** of common ASSB pairings (e.g., **LFP cathodes**) exhibit
   minimal voltage change over large SOC ranges"
3. `[인쇄]` "these profiles can be **distorted by voltage hysteresis arising from mechanical
   stresses**"

그리고 같은 절이 **SOH 가 갈라야 할 두 항**을 정의한다: `[인쇄]` "distinguish between **true
active material loss** and a reduction in 'useable capacity' caused by **rising impedance or
increasing overpotentials**".

**세 가지가 이 카드에 걸린다**:

- ★★★ **접촉 손실이 이분법에서 사라졌다.** 같은 절 첫 문단은 ASSB 의 지배 실패 모드를
  `[인쇄]` "the gradual **loss of interfacial contact**, the propagation of cracks … chemo-mechanical
  evolution" 으로 꼽는다. 그런데 SOH 정의는 `LAM` ↔ `kinetic` 둘뿐이고 **접촉 손실이 어느
  쪽인지 적지 않는다.** 12호는 `LAM ⊃ 접촉 손실` 로 **정의에 흡수**했고, 13호는 **정의에서
  누락**했다 — 두 종설이 다른 방식으로 같은 결과(분리 물음이 없는 분류)에 도달한다.
  우리 3 항(`θ_AM · Q_material · η(i)`)과는 둘 다 다르다.
- ★★ **운전 창이 OCV 채널을 설계상 닫는다.** 이 카드의 물음("OCV 적합이 가를 수 있는가")은
  **완전 OCV 곡선**을 전제한다. 그리드 ASSB 는 (i) 20–80 % 창 (ii) LFP 평탄역 (iii) 응력
  이력 — 셋이 겹쳐 **그 전제가 설계 단계에서 없어진다.** `[해석]` 이 카드의 답이 "가를 수
  있다" 로 나오더라도 **그리드 용도에는 적용 창이 없다**; 반대로 이 카드의 폭 측정기는
  "부분 창에서 폭이 얼마나 벌어지는가" 를 잴 수 있고, 그것이 13호가 요구하는
  "multi-parameter SOH model" 에 우리가 공급할 수 있는 유일한 것이다
  ([[data-window-identifiability]] 의 ASSB 판).
- ★ **음극 전제의 세 번째 반례 — 이번엔 처방으로.** 13호는 Li 금속을 `[인쇄]` "may be
  misguided" 로 배제하고 **Si 계 음극**을 권한다. Si OCP 는 비평탄 + 이력(09-21 세미나:
  8 종 전부 닫힌 이력 루프). 9호(Li-Si 셀) · 11호(graphite 셀)에 이어 **"전고체 음극 = 평탄
  → 5→3 붕괴" 가 그리드 설계 처방에서도 성립하지 않는다.** ⚠ 13호는 Si OCP 를 한 번도
  논하지 않는다 (G10) — 좁은 창에서 SOC 를 추적하라고 요구하면서.

**Q4 는 0 / 13 이고 성질이 또 바뀐다**: 8호가 `identifiab*` 5 회로 이름을 붙였다면 **같은 해
13호는 이름 없이 역문제를 처방한다** — `[인쇄]` "These models **inversely estimate** the current
state of interfacial contact **and** material properties." 9호의 곱 축퇴 `A_eff·ε_p/R_s` 가
정확히 "접촉 상태 ↔ 재료 물성" 사이에 있다 ([[assb-lampe-contact-product-degeneracy]]). ⇒
"2026 년 PHM 문헌은 식별 가능성을 안다" 는 일반화는 **8호 한 편의 일**이다.

**이 절이 For / Against 어느 쪽인가**: **어느 쪽도 아니다.** 근거 0. 얻은 것은 **(a) 분류
체계 셋(12호·13호·우리)이 서로 다르다는 실측 (b) 물음의 적용 창이 그리드에서 설계상 닫힌다는
요구 측 진술 (c) 압력 창 요구치의 세 번째 독립 인쇄** (아래 새 제약 + [[assb-stack-pressure-operating-window]]).

### 새 제약 (2026-09-22, Li et al. 2026 — 종설이 들어오면서 붙은 것)

> ⚠ 이 절의 제약은 **1 차 측정이 아니라 문헌의 요구·재인용**에서 온다. 앞 절들(1–7호)의
> 제약과 **근거 강도가 다르다**.

- ★★ **압력 창의 아래 벽에 산업 요구치가 생겼다: `<≈1 MPa`** (재인용, Xu 2024).
  → [[assb-stack-pressure-operating-window]] 의 실측 창 전체가 그 위에 있다.
  `[해석]` 우리가 설계할 분리 시험의 **운전 압력 기준점**은 실험실 값(2–5 MPa)이
  아니라 이쪽이어야 하고, 그러면 **`θ_AM` 손실이 더 크고 더 빨리** 온다고 예상해야 한다.
  ⚠ **재인용이므로 Xu 2024 를 받기 전에는 설계 입력으로 쓰지 않는다.**
- ★★★ **우리 폭 측정기의 소비처가 문헌에 그려져 있고, 그 칸이 비어 있다.**
  `[도표]` 8호 Fig. 2 의 안전 감독기가
  `I_cmd = min(I_V, I_T, I_plate, I_power, I_imbalance, **I_uncertainty**)` 를 계산한다 —
  **여섯 번째 전류 상한을 추정 불확실성에서 뽑는데 계산법이 논문에 없다**
  (8호 digest G1). → [[near-optimal-set-width-measurement]] 가 그 입력의 재료를 만든다.
  ⚠ **폭 → 허용 전류의 사상은 아직 없다** — 빈칸의 좌표가 확인된 것까지다.
- ⚠ **종설의 수치를 이 카드의 근거로 올리지 않는다.** 8호가 재인용한
  `SOH RMSE ≤0.873 %` 가 **우리가 이미 가진 원전과 어긋난다**(위 Evidence).
  → **`[인쇄]`(원전) 와 `[재인용]`(종설) 을 구분해 적는다.** Q1~Q8 채움표의 8호 행은
  전부 재인용이다.
- ⚠ **BMS 문헌은 열화 모드를 쓰지 않는다.** 8호는 SOH 를 끝까지 **스칼라**로 다루고
  `LLI`·`LAM`·`degradation mode` 가 전수 0 회다 — **Birkl 2017 을 인용하면서도.**
  `[해석]` **우리 축(모드 분해)이 BMS 배치 문헌에 아직 도착하지 않았다.**
  이것은 공백이면서 동시에 **우리가 채울 수 있는 자리**다.

### 새 제약 (2026-09-22, Huo 2025 — 적합으로 지분을 정하는 첫 편이 들어오면서 붙은 것)

1. **★ "평탄 상대극 → 5→3 붕괴" 가 모든 ASSB 에 성립하지 않는다.** 이 카드와
   `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 은 상대극이 평탄하다는 전제에서
   `a_NE`·`b_NE`·`γ_Si` 의 민감도가 정확히 0 이 되는 것을 실측했다. 9호는
   **Li-Si 합금 음극**이고 모델이 `U^n_ocp(θn)` 를 **비평탄 보간 함수**로 둔다 —
   `[재현]` N/P ≈ **3.14** ⇒ 사이클당 음극 화학량론 스윙 **31.8 %**.
   **⇒ 이식 전에 상대극 화학을 먼저 갈라야 한다.** Li-In·Li 금속·무음극은 평탄
   가정이 살아 있고, **합금(Li-Si) 계열은 5 파라미터가 그대로 필요하다.**
2. **`θ_AM` 과 `η(i)` 가 한 파라미터에 묶이는 실제 사례가 생겼다.**
   [[assb-apparent-capacity-decomposition]] 의 3 항 분해에서 9호는 `ε_p` **하나**만
   푸는데 `a_s = 3ε_p/R_s` 도 같이 줄어 분극이 커진다 — `[재현]` 증폭 1.60 / 1.32.
   ⇒ **2호에서 세운 율 스윕 분리 시험(`i→0`)이 이 논문에 그대로 처방이 된다.**
   그리고 **증폭이 상수가 아니므로**(동작점 의존) 사후 보정으로 뺄 수 없다.
3. **압력이 상태변수로 측정됐는데 모델에 안 들어간다.** 9호가 이 계보 최초로
   **사이클 중 힘 연속 시계열**을 기록한다 (`[재현]` 평균 ≈36.9 MPa · 주기 변조
   ≈0.32 MPa). 그런데 노화 식 Eq. (2) 는 **사이클 수만의 함수**다. ⇒ 8호가
   제안한 "압력을 BMS 상태변수로" 와 **같은 공백이 실험 논문 쪽에서도 확인된다.**
4. **`LLI` 축을 닫는 방법이 하나 더 확인됐다 — 파라미터 동결.** 리튬 재고를 정하는
   두 수(`cp0`·`cn0`)가 신품에서 한 번 적합된 뒤 **노화 전 구간 고정**이고 **값이
   비공개**인데, 그 위에서 `[인쇄]` "minimal or no loss of lithium inventory" 를
   결론한다. 그리고 SI 가 **쿨롱 효율 제출을 명시적으로 거부**한다(`[인쇄]` "our
   analysis and modeling 에 쓰이지 않는다") — 6호에서 본 대로 **CE 는 `LLI` 의
   유일한 전하 수지 채널**이다. ⇒ **"LLI 없음" 이 관측이 아니라 설계의 결과인
   경우를 라벨 출처 검사에 추가한다.**
5. ⚠ **우리가 이 논문에 공급할 수 있는 것이 있다** — `A_eff · ε_p / R_s` 의 근최적
   폭. 우리 폭 측정기는 화학 무관이다. 필요한 입력은 **반쪽전지 OCP 두 곡선**(원전이
   출처를 안 적었다)과 **비공개 6 개 파라미터**뿐이다. ⇒ 후속 후보 1 순위가
   원전의 ref [27](같은 연구실의 모델 논문)인 이유다.

### 새 제약 (2026-09-22, Vadhva 2021 — 방법론 리뷰가 들어오면서 붙은 것)

1. **★ 주파수 대역으로 전극을 지목하는 모든 문장에 화학 꼬리표를 단다.**
   `[인쇄]` "full devices using a **LMA** and an intercalation cathode typically
   assign the **SE\|cathode interface as the lowest frequency arc**, while those
   utilising an **In–Li anode assign this to the SE\|anode interface**."
   ⇒ **우리 계보 4호(In 음극)와 9호(Li-Si 합금 음극)는 서로 다른 화학인데 둘 다
   주파수로 전극을 지목했다.** 9호의 `R_SEI`(중주파) ↔ `R_ct`(저주파) 귀속은
   **Li-Si 합금 완전지의 귀속을 확립한 연구가 리뷰에 없으므로 무보증**이다.
2. **★★ `R_anode(N)` 의 증가를 노화로 읽기 전에 SoC 를 고정했는지 확인한다.**
   `[인쇄]` In 음극 계면 저항이 **한 번의 방전 안에서도** 리튬화도(In-rich 화)에
   따라 크게 증가한다. ⇒ 4호의 `[도표]` `R_LF` ≈0.7 → ≈110 kΩ(≈157 배)에서
   **노화분과 SoC 분이 갈리지 않는다** — 4호는 사이클마다 같은 SoC 에서 쟀는지
   적지 않았다. **이 카드의 "모르는 것 2" 에 붙는 경고다.**
3. **★★★ EIS 를 `θ_AM` 의 독립 관측으로 쓰려는 계획에 조건을 단다.**
   `[인쇄]` 같은 `R_MF` 에 **접촉 손실**과 **분해층 성장**이 함께 귀속된다.
   ⇒ **EIS 는 [[assb-lampe-contact-product-degeneracy]] 의 곱 축퇴를 깨는 대가로
   새 축퇴를 들여온다.** 그 페이지 처방표의 "다중 SOC EIS" 는 **단독으로는 못 쓴다** —
   **압력 되돌림 또는 대칭셀 쌍과 반드시 짝지어야 한다.**
4. **모델 차수를 시간에 대해 고정하지 않는다.** `[인쇄]` Larfaillou: 신품 **3 RQ**
   → 60 h/60 °C 노화품 **4 RQ**, 새 RQ 의 귀속은 `[인쇄]` "Li\|LiPON interface
   **and/or** in the LCO bulk". ⇒ **노화 시계열을 고정 회로로 적합하는 절차(9호)에
   구조적 결함이 있다.** 그리고 **"and/or" 는 우리가 찾던 형태의 증거다** — 저항
   하나가 어느 전극 것인지 모르는 채 열화 서사에 들어간다.
5. **역문제를 풀기 전에 데이터가 그것을 감당하는지 먼저 판정한다 (실행 가능).**
   **Lin-KK**(ref. 43, KIT 소프트웨어)는 모델 없이 선형·정상·인과를 검사한다.
   ⇒ 우리가 언젠가 ASSB EIS 를 다루면 **첫 단계**이고, 문헌 EIS 를 인용할 때
   **"K–K 검증을 했는가" 가 라벨 출처 검사의 새 항목**이 된다
   (`[인쇄]` Kamaya 2011 은 100–500 mV 섭동에 K–K 검증 0 — 기준의 2–10 배).
6. **압력이 분해능 연산자이기도 하다 (새 축).**
   `[도표]` Fig. 11a: **400 MPa 에서 `R_int` 가 사라져야 `GB` 원호가 보인다.**
   ⇒ [[assb-pressure-reapplication-separation-test]] 의 `P↑` 는 **용량을 되돌리는
   연산자**일 뿐 아니라 **관측 가능한 시상수 개수를 바꾸는 연산자**다.
   그리고 `[인쇄]` "**<1 Ω cm², which remained after the pressure was removed**" 는
   [[assb-stack-pressure-operating-window]] 가 5호에서 잡은 **이력**의 **산화물
   독립 재현**이다. ⚠ 400 MPa 는 5호의 Li\|황화물 상한(75 MPa)의 **5.3 배** —
   **창은 전해질 재료의 함수**라는 기존 단서와 일치한다.
7. **⚠ 우리 위키가 이 리뷰보다 한 칸 앞서 있는 자리가 하나 있다.**
   리뷰는 `[인쇄]` ML+EIS 의 예로 **ref. 174 = Zhang et al. *Nat. Commun.* 2020**
   을 든다. **그 논문은 우리가 이미 가지고 있다** ([[zhang2020-eis-aging-dataset]]):
   `state I~IX` 중 **넷이 DC 전류 중** 측정이라 리뷰 자신의 `stability` 요건을
   위반하고, **모드 라벨이 없으며**, ARD 가 고른 두 주파수가 **비식별**이다.
   ⇒ **리뷰의 "ASB 로 옮기자" 는 권고에 우리가 붙일 단서가 이미 검증돼 있다.**

### 새 제약 (2026-09-22, Yu 2024 — DRT 를 실제로 돌린 첫 편이 들어오면서 붙은 것)

1. ★★★★ **이 카드의 출발 전제가 음극 재료의 함수라는 것이 확정됐다.**
   §"지금까지 아는 것" 의 **5 → 3 파라미터 붕괴**는 `a_NE`·`b_NE`·`γ_Si` 의
   민감도가 **0** 이라는 것에서 나왔고, 그것은 **음극 OCP 가 평탄**할 때만 참이다.
   11호의 음극은 **graphite** — 스테이지 평탄역이 여럿인 **구조 있는 OCP** 다.
   ⇒ **붕괴표에 단서를 단다: "Li-In / Li 금속 / 무음극 셀에 한함."**
   9호(Li-Si)에 이어 **두 번째 반례**이고, 이쪽은 **액체셀과 같은 상용 흑연**이라
   `LLI ↔ LAM_NE` 축퇴가 **그대로 이식된다.** (`γ_Si` 축만 안 온다.)
2. ★★★★ **"DRT 를 쓰면 개수 문제가 풀린다" 는 기대를 접는다.**
   8호가 DRT 를 처방했고 10호가 `[인쇄]` "A powerful tool to **guide ECM
   selection**" 이라 적었다. 11호가 실제로 돌린 결과는:
   **개수가 사이클로 늘고(3 사례) · 조작으로 줄고(1 사례) · 배선으로 바뀐다(1 사례).**
   ⇒ **DRT 는 개수를 "재는" 도구가 아니라 개수가 무엇에 달려 있는지 보여 주는
   도구다.** 우리가 9호·11호에 적용할 판정은 **"몇 개가 맞는가" 가 아니라
   "개수가 정해지는가" 여야 한다.**
3. ★★★ **우리 폭 측정기가 붙을 자리가 구체적으로 특정됐다.**
   11호가 남긴 것은 **nuisance 1 점 변동**(Fig. S3, 배선 1 회 교체)이다.
   [[near-optimal-set-width-measurement]] 의 기계를 여기에 붙이면
   **`λ` 를 격자로 흔들어 봉우리 개수·위치·높이의 궤적**을 만들 수 있고,
   그것이 **"DRT 로 잰 저항 증가분" 에 폭을 붙이는 최소 절차**다.
   ⇒ **화학·방법에 무관하게 "답이 하나로 정해지는가" 를 재는 우리 논리가
   EIS·DRT 축에도 그대로 이식된다**는 것이 이 편으로 확인된다.
4. ⚠ **압력을 "θ_AM 전용 연산자" 로 쓰지 않는다.**
   [[assb-pressure-reapplication-separation-test]] 는 4호 1 편(1 셀 1 점)에
   기대어 있었다. 11호가 **5 점**을 주면서 동시에 **선택성이 없다**는 것을 보였다
   (`[도표]` 재가압이 P1·P2·P3·P4 를 **전부** 10–27 % 줄인다).
   ⇒ 그 개념 페이지의 `confidence: low` 는 **유지**하고, 반례를 본문에 적는다.
5. ⚠ **산업체 논문의 provenance 가 9호보다 뒤다.**
   9호는 Table 3 에 6 개 값을 `[인쇄]` "not disclosed" 로 **찍어 두어** 구멍을
   셀 수 있었다. 11호는 **파라미터 표가 없다** — 조성비·로딩·두께·N/P·입도·
   코팅 두께·`Ω mg⁻¹` 정규화 질량·**어느 셀이 Cl 이고 어느 셀이 Br 인지**가
   전부 없고, `[인쇄]` "The authors do not have permission to share data."
   ⇒ **`assb` 산업체 편(9·11호, 그리고 36호 예정)에는 "구멍을 찍었는가" 를
   별도 항목으로 기록한다.**

### 새 제약 (2026-09-22, Sadegh Kouhestani 2022 — PHM 종설이 들어오면서 붙은 것)

1. ★★ **`LAM` 이라는 낱말을 문헌에서 받을 때 "접촉 손실을 포함하는가" 를 먼저 묻는다.**
   12호가 `[인쇄]` "The loss of active materials **mainly stems from** the electrical
   contact loss" 로 정의했으므로, PHM 계열 논문의 `LAM` 은 **우리 `LAM_PE` 가 아니라
   `1 − θ_AM·(Q_material/Q₀)` 전체**일 수 있다. 라벨 층위 표(Q3)에 **"LAM 의 정의 범위"**
   를 적는다 — 이 칸이 없으면 액체셀 `LAM` 수치를 ASSB 로 옮길 때 두 양이 섞인다.
2. ★★ **`A_eff` 형 파라미터의 원전을 받기 전까지 9호의 곱 축퇴를 "Huo 2025 고유" 로
   적지 않는다.** 12호가 Tian & Qi 2017 · Shao 2022 를 같은 형태로 소개했으므로
   `evidenceScope: single-source` 는 유지하되 **"P2D 계열에 널리 반복될 가능성"** 을
   [[assb-lampe-contact-product-degeneracy]] 에 이미 적어 둔 그대로 두고, 원전 두 편을
   **큐 후속 1·2 순위**로 올린다.
3. ★ **종설의 "≈1 MPa" 는 두 원전에서 독립적으로 나왔으나, 둘 다 우리 근거가 아니다.**
   8호 "<≈1 MPa"(Xu 2024, 산업 요구) · 12호 "0.4–1 MPa"(Tian/Shao, 모델 최적, 출처
   미확정). [[assb-stack-pressure-operating-window]] 의 **아래 벽 후보**로만 두고 값은
   원전 확인 후 적는다.
4. ⚠ **인용 위생이 무너진 종설은 재인용 수치를 위키에 옮기지 않는다 — 방향도.**
   12호는 인용번호 오류·제목-내용 뒤바뀜이 **21 건**(digest D1–D21)이고 접수→승인이
   9 일이다. 10호(D5 인용번호 1 건)·8호(Su 2024 숫자 어긋남 1 건)에 적용한 규율을
   **더 강하게** 적용한다: 이 편에서는 **"이 지면에 이렇게 적혀 있다" 이상을 쓰지 않는다.**

### 새 제약 (2026-09-22, Zheng 2026 — 그리드 appraisal 이 들어오면서 붙은 것)

1. ★★ **적용 창을 명시한다.** 이 카드가 답을 내면 그 답에 **"완전 OCV 곡선이 있을 때"**
   라는 조건을 붙인다. 13호가 그리드 운전을 `[인쇄]` "20–80 % SOC … impossible to obtain a
   full OCV curve" 로 적었으므로, **부분 창에서의 근최적 폭**을 별도 결과로 낸다
   ([[data-window-identifiability]] · [[near-optimal-set-width-measurement]]). 창을 안 적은
   분리 진술은 그리드에는 무효다.
2. ★★ **압력 창의 위 벽을 둘로 나눠 적는다.** 5호(Doux)의 위 벽 = **단락**(Li 크리프, ~h).
   13호의 위 벽 = `[인쇄]` "creep and stress relaxation … fatigue-driven micro-crack initiation"
   (**피로**, ~년, 1 차 주장·데이터 0). 둘은 기구·시간 스케일이 다르므로
   [[assb-stack-pressure-operating-window]] 에서 **한 숫자로 합치지 않는다.**
3. ★ **압력 요구치는 세 원전이 독립 수렴한 자릿수로만 쓴다** — 8호 `<≈1`(Xu 2024) · 12호
   `0.4–1`(Tian/Shao) · 13호 `<5`(Si 근거 [35]/[45]). **세 값 모두 원전 미수령**이고 13호의
   "5" 는 인용 문장이 값을 주는지 확인되지 않았다(G3). 위키에는 "≈1–5 MPa, 종설 셋" 까지만.
4. ★ **접촉 손실의 소속을 라벨 정의에 명시하도록 요구한다.** 12호(흡수)·13호(누락)가 보여
   준 대로 종설의 `LAM` 정의가 접촉 손실을 어디 두는지 제각각이다. 앞으로 들어오는 `assb`
   논문은 Q3 판정에 **"접촉 손실 = LAM 안 / 밖 / 미언급"** 한 칸을 더 적는다.
5. ⚠ **13호의 수치를 근거로 옮기지 않는다.** Table 1 의 ASSB 열은 투영(무인용 5 항목),
   LCOS 는 입력 미공개(G1), `<5 MPa` 는 출처 미명시(G3), Fig. 2 의 다섯 창은 `[도표]` 이고
   산정 규칙 0(G8). "이 지면에 이렇게 적혀 있다" 까지만.

### 새 제약 (2026-09-22, Oh 2025 — 열역학 도함수 진단이 들어오면서 붙은 것)

1. ★★ **접촉 손실 → 용량 사상을 문턱형으로 적는다.** 4호(면적 10.4 % ↔ 60 %p)와 14호
   (void 2 배 ↔ 용량 불변)가 같은 사상의 **양 끝**이다. 우리 3 항의 `θ_AM` 은 void 분율의
   함수가 아니라 **퍼콜레이션의 함수**이고, 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을
   보고하면서 void 성장을 **놓친다**(오독이 아니라 무감). 분리 시험을 설계할 때 **문턱
   위·아래 두 표본**이 필요하다.
2. ★★ **관측 추가 후보를 volumetry 로 등록한다 — 단, 상수가 아니라 곡선으로.** `dE/dP` 는
   압력 구간에 2 배(D4), SOC 에 미지(D7)로 의존한다. 근최적 폭 측정에 넣을 때는 `E(P, x)`
   면을 먼저 모델링하고, 선형 `ΔV` 상수를 쓰지 않는다. 소신호(ΔP = −5 MPa, 가역)와
   대신호(`P↑` 300 MPa, 비가역)를 **다른 연산자**로 적는다
   ([[assb-pressure-reapplication-separation-test]]).
3. ★ **엔트로피메트리를 분리 관측으로 쓰지 않는다.** 균일 `LAM_PE` 와 완전 고립 접촉
   손실은 둘 다 아핀이라 ΔS(x) 모양이 안 바뀐다(`[해석]`). 대신 **아핀 전제의 검사**로
   쓴다 — `E(x)` 와 `∂E/∂T(x)` 가 같은 (α, β) 로 재조정되는가 ([[halfcell-ocp-shape-invariance]]).
4. ★ **sum rule 을 검사 항목으로 둔다.** `∫(dS/dx)dx` 는 상태함수 차이 — 전·후가 다르면
   비균질이 아니라 재료·창·음극 변화다. 14호는 그 뺄셈을 안 했고(7호·11호와 같은 형태),
   우리가 그림에서 할 수 있다.
5. ⚠ **비파괴 진단의 라벨에도 문턱값 0 이다.** reuse/recondition/recycle 의 수치 기준이
   없고 논문 스스로 "many cells … currently difficult" 라 적는다 — 14호의 등급을 Q3 의
   measured 라벨로 옮기지 않는다.

### 새 제약 (2026-09-22, Chang 2020 — 매립 기준극 + 전극별 용량 귀속이 들어오면서 붙은 것)

1. ★★★★ **저율이 `η` 를 지운다고 가정하지 않는다.** `[재현]` **C/72** 에서도 첫
   사이클의 54 % 가 날아간 실측이 있다(면적용량 9.3 mAh cm⁻²). ASSB 이식판에서
   **율 스윕 분리 시험의 전제(`i→0 ⇒ η→0`)를 두께 축과 함께 다시 세운다.**
2. ★★★★ **"잘린 용량" 을 라벨로 쓰기 전에 프로토콜 몫을 뺀다.** `[재현]` 1일
   휴지 뒤 `V₁` 이 컷오프보다 **310 mV** 아래 — CC 전용·고정 컷오프가 만든
   겉보기 손실이다. **CC-only ↔ CCCV 가 `LAM_PE` 라벨을 얼마나 움직이는가**를
   합성 truth 에서 돌린다(미실행).
3. ★★★ **성분에 물리 이름을 붙이기 전에 시상수를 검산한다 — 시간 영역에도.**
   `[재현]` 이 편의 `R_ct` 구간은 τ ≈ 10³ s 라 `C = τ/R ≈ 1 F cm⁻²`, 이중층
   상한의 **10²–10³ 배** ⇒ **전하이동이 아니다.** 곱 축퇴 처방에 **4단계**를
   더한다: *"주파수 영역 분해가 없다고 이 검사를 면제받지 않는다."*
4. ★★★ **기준극에는 재고 예산이 있다.** `[재현]` 이 편의 RE Li 재고 = 셀의
   **1/675**, 190 h 실험에서 재고를 지키려면 **누설 < 10 nA**. 그리고 **3전극은
   자기 기준극의 표류를 공통 모드로 상쇄해 원리적으로 못 본다.** ⇒ Q5 요구에
   **(ㄴ′) Li 재고 / (누설 × 시간) ≥ 10** 을 추가하거나, 19호처럼 **차분으로
   소거**한다. 계보 **20/20 편이 누설을 안 쟀다.**
5. ★★ **기준극 배치는 무엇이 관측되는지를 정한다.** `[인쇄]` 중앙 매립형은
   층간 접촉 저항과 SE 옴을 **측정 창 안에** 넣고, 배면형(Nam 2018)은 밖에 둔다.
   ⇒ 우리 3항 분해에서 **어느 항이 관측 가능한가**가 배선의 함수다.
6. ⚠ **잔차에 이름을 붙이지 않는다.** `[재현]` 이 편의 "접촉 저항 362 Ω" 은
   `R₀ − L/(σA)` 의 잔차이고, **복합전극 내부 이온 경로만으로 ≈350 Ω** 이 나온다.
   **뺄셈으로 만든 양에 물리 이름을 붙이려면 뺀 항의 완전성을 먼저 보인다.**

### 새 제약 (2026-09-23, Sedlmeier 2023 — 미세 기준극 + 방향 통제 실험이 들어오면서 붙은 것)

1. ★★★★ **개방회로 0.62 V 를 "상대극이 원천이다" 의 증거로 쓰지 않는다.** `[인쇄]` 같은 0.62 V 에서
   꺼낼 수 있는 Li 가 **0.39 µAh cm⁻² ↔ 3.0 mAh cm⁻²**. ASSB 이식판에서 상대극을 평탄 상수로 둘 때
   **조립 방향(Li 가 분리막 쪽인가)을 입력 메타데이터로 요구**한다. 모르면 `LLI` 가 `LAM_PE` 로 새는
   통로를 열어 둔 채로 적합하는 것이다.
2. ★★★ **3전극 자료의 기준 전위는 "같은 셀에서 잰 것인가, 옮긴 것인가" 를 먼저 본다.** 21호의 InLi
   0.62 V 는 **잰 차 0.31 V + 옮긴 0.31 V** 이고, 그 이식이 `assum*` 이 아니라 **"calculated based on"**
   으로 인쇄된다 ⇒ **낱말 지문에 "calculated/converted … based on" 을 추가**한다. 그리고 **축 이름과
   숫자가 맞는지** 본다(21호 Fig. A·1 은 0.62 V 어긋난다).
3. ★★★ **"과전압" 에서 분리막 IR 을 뺀다.** `[재현]` 21호의 375 / 750 Ω cm² 중 **≈245 Ω cm²**(33–65 %)가
   분리막 절반이다. 3전극이라도 **WE–RE 구간의 옴은 측정 창 안**이다(17호 P3 와 같은 자리).
4. ★★ **기준극 표류는 고정된 전극이 있으면 3전극으로도 보인다.** 20호의 "원리적으로 못 본다" 를
   **"2상 평탄 전극이 옆에 없으면"** 으로 좁힌다. 21호는 그 조건에서 **< 3 mV / 28 일**, `[재현]` 누설
   **< ≈4.3 nA**(간접 상한). ⇒ Q5 요구의 (ㄴ′) 를 보일 때 **고정 전극 대조를 기본 배선으로** 쓴다.
5. ★★ **저주파 부류는 계면 서브마이크론 층이 정한다.** `[재현]` 50 µAh cm⁻²(≈0.35 µm LiIn, 재고의
   0.36 %)로 꼬리 ↔ 반원이 뒤집힌다 ⇒ **음극 저주파 기여를 SOC·전류 방향 이력과 함께 적는다.**

### 새 제약 (2026-09-23, Strauss 2018 — 회절 상 분율이 `θ` 의 측정으로 들어오면서 붙은 것)

1. ★★★★ **XRD 불활성 분율을 `1 − θ_AM` 으로 곧장 쓰지 않는다.** 관측 연산자가 필요하다: (i) **정보 깊이 가중**
   (반사 기하는 한쪽 면 수–수십 µm) (ii) **이온 쪽 고립** (iii) **2차 입자 내부 코어**(이봉으로는 입자 전체 고립과
   못 가른다) (iv) **율**(C/10 한 점이면 `θ` 의 율 불변을 가정한 것이다). DEM 이 주는 것은 (i)~(iii) 이 없는 `θ` 다.
2. ★★★ **열화 판에서는 "pristine = 불활성" 규칙이 깨진다.** 사이클 중 고립된 입자는 **고립 당시 SOC 에 얼어붙는다**
   ⇒ **두 SOC 에서 회절을 찍어 "SOC 를 따라가지 않는 상" 의 분율**을 `1 − θ(N)` 으로 쓴다.
3. ★★★ **측정 면을 메타데이터로 요구한다** — 집전체 면인가 분리막 면인가. 전자 고립은 집전체 면에서 가장 드물고
   이온 고립은 가장 흔하다 ⇒ 같은 전극도 **어느 면을 보느냐로 원인 해석이 뒤집힌다.**
4. ★★ **원인 배정에 쓰인 벌크 부분 전도도는 두 축의 자릿수 간격과 정상 상태 도달을 확인하고 읽는다.** 22호 Fig. 4
   는 좌 5 자릿수 ↔ 우 3 자릿수라 NCM-L 의 σ_e ≥ σ_ion 이 반대로 보이고, `[도표]` 전자 차단 측정은 60 h 에도 전류가
   내려간다(`[재현]` C = τ/R ≈0.4–0.8 F cm⁻² — 계면이 아니라 화학량 분극) ⇒ **σ_ion 은 상한**이다.
5. ★★ **모델 `p_c(d)` 를 실험 조성에 댈 때 공극률을 모른다는 것은 비교 불가의 이유가 아니다** — 공극률은 AM 부피
   분율을 **낮추기만** 하므로 **무공극 상한**에서 비교하면 된다. 1호는 그 비교를 하지 않았다.

### 새 제약 (2026-09-23, Koerver 2017 — "접촉 손실의 실험 원전" 이 들어오면서 붙은 것)

1. ★★★★ **접촉 손실의 크기 근거로 23호를 쓰지 않는다.** 원전은 존재(SEM)만 보였고 용량 몫·치수·분율이 0 이다. 이식판에 접촉 손실을
   넣을 때 크기의 문헌 근거는 **22호(XRD 불활성 분율, 신품)** 뿐이다.
2. ★★★ **양극 호는 `R` 만 보고하지 말고 `C` 를 같은 상태축 위로 같이 적는다** — 23호 SI 가 보인 대로 그것만으로 계면층 ↔ 접촉 면적의
   1차 분류가 된다. 전제 `C ∝ 면적` 은 **같은 셀의 무전류 이완**(화학 불변을 XPS 로 확인)에서 `R·C` 보존으로 먼저 검사한다.
3. ★★★ **무 Li 상대극 셀(순수 In · 비리튬화 LTO)의 방전 끝 수 % 는 상대극이 끊을 수 있다** — 재고비 ≈Q_ch/Q_dis. 2전극 EIS 의 저주파
   `C` 두 자릿수 붕괴를 평탄 이탈 서명으로 쓰고, 그 구간은 OCV 적합 창에서 뺀다. **상대극 교체 대조는 두 상대극이 같은 결함을 공유하지
   않을 때만 대조다.**
4. ★★ **"SOC 가 아니라 전위의 함수" 논거는 첫 충전에서 판별력이 없다** — SOC 와 전위가 단조 동행한다. 시점으로 기구를 가르려면 격자
   `V(x)` 곡선이 같은 지면에 있어야 한다.
5. ★★ **인용 문장의 강도를 원전과 대조한다** — 원전의 "expected · suspect · suggests" 가 후속에서 평서문이 되고(1호 "throughout"),
   회피가 증명이 되고(1호 탄소), 기구가 바뀌고(18호 공간전하), 초록의 약한 문장이 채택된다(9호). **숫자 오기만이 인용 오류가 아니다.**

### 새 제약 (2026-09-23, Stavola 2023 — operando 깊이 분해와 굴곡도 인자가 들어오면서 붙은 것)

1. ★★★★ **`τ²`(또는 Bruggeman 지수)를 측정값으로 쓰지 않는다.** 재는 것은 `σ_eff` 하나이고 `τ² = ε·σ_bulk/σ_eff` 는 **가정 `ε` 로 나눈 이름표**다 — 24호 원전 표에서
   같은 `σ_eff` 가 `ε` 규약만으로 반대 추세(×1.6 ↔ ×0.92)를 낸다. 이식판 모델에 수송 항을 넣을 때 **`ε`·`τ` 를 따로 파라미터로 두지 않는다.**
2. ★★★ **깊이 분해·이봉 회절 자료는 가중평균 `x̄` 가 아니라 모집단별 scale 분율로 받는다** — 가중평균은 `θ` 를 `η` 에 섞는다(24호 식 S14). 그리고 가중 전제("same area")를
   봉우리 폭으로 검사한다.
3. ★★★ **두 영역(EIS ↔ operando/DC) 값의 차이를 "진화" 로 읽기 전에 두 시편의 제조 압력·두께·`ε` 를 맞춘다** — 24호는 50/150 ↔ 100 MPa.
4. ★★ **"i₀ 를 흔들어도 안 변한다" 는 식별 불가의 증거이지 기구 부재의 증거가 아니다** — 민감도 결과를 물리 결론으로 옮기지 않는다(Q4 열일곱 번째 성질).
5. ★★ **첫 사이클 비가역의 깊이 분포를 본다** — 균일하면 두께 수송(`η(z)`)이 아니다. 그 다음이 입자 척도 ↔ 상대극의 분리이고, 그것은 기준극이나 상대극 재고 기록 없이는 안 된다.

### 새 제약 (2026-09-23, Zhou 2025 — 압력 × 미세구조 요인 설계와 실험 논문의 DEM `θ` 가 들어오면서 붙은 것)

1. ★★★★ **벡터 그림은 인쇄 수치보다 먼저 좌표로 읽는다** — 25호는 인쇄 유지율 6 중 2 만 그림에서 재현되고, Fig. 3 의 곡선 5 개가 2 개의 곡선이다. 그림 자료의 정체를 확인하기 전에는
   라벨 층위(Q3)를 묻지 않는다. 채움표에 들어가는 25호 값은 전부 `[도표·벡터]` 로 적는다.
2. ★★★ **계산 `θ`(DEM 이용률)를 받을 때는 연결 기준의 구간 전체를 받는다** — 25호 Table 1 은 겹침 0–10 % 에서 94 → 20 %. 한 값만 옮기면 그 값은 손잡이의 한 점이다.
   그리고 **첫 충전 비**로 먼저 부정 시험을 건다(Against 첫 항목).
3. ★★★ **2전극 감쇠를 양극 기구로 배정하기 전에, 같은 지면의 적합에서 상대극 저항의 몫을 확인한다** — 25호는 저자 자신의 S19 가 Li 계면을 가장 큰 항으로 인쇄했다.
4. ★★ **"저압" 은 운전 압력과 제조 압력을 나눠 적는다** — 25호의 저압은 운전 2 MPa · 제조 375 / 30 MPa 이다(5호 이력의 하강 분기).
5. ★★ **셀 간 산포를 같은 지면의 다른 그림에서 찾는다** — 25호 S18 ↔ Fig. 2c 가 같은 조건 ≈20 % 차를 준다. 원전이 n 을 적지 않아도 암묵적 반복이 있을 수 있다.

### 새 제약 (2026-09-23, Iwakiri 2024 — "parameter estimation and sensitivity analysis" 가 제목에 든 모델 편이 들어오면서 붙은 것)

1. ★★★★ **"sensitivity analysis" 를 식별성 증거로 세지 않는다** — 설계 스윕 · 추정 민감도 · 식별성의 세 줄([[assb-sensitivity-sweep-vs-identifiability]])로 먼저 분류한다. 26호는 첫 줄이다.
2. ★★★★ **추정 논문이 스윕도 인쇄했으면 스윕 그림을 겹친다** — 평행 · 0 열을 찾고, 그 파라미터의 **적합값 ÷ 문헌값**을 본다. 26호 `D_e⁻` 는 10 자릿수였다.
3. ★★★ **"문헌과 일치" 를 받기 전에 그 문헌이 같은 데이터의 출처인지 본다** — 26호의 문헌값은 데이터 출처 논문(ref 10)의 값이고, 적합 변수 7/10 이 정확히 ×1.0500 이다.
4. ★★ **모델 C-rate 의 분모를 확인한다** — 26호는 `Q_ideal`(적합 대상 `a_max` 의 함수)로 정의해 모델 1C = 1.23 mA ↔ 셀 공칭 0.7 mAh. 분모가 적합 변수면 입력 전류가 반복마다 바뀐다.

### 새 제약 (2026-09-23, Sinzig 2024 — 전역 민감도를 제대로 한 모델 대 모델 비교 편이 들어오면서 붙은 것)

1. ★★★★ **"전역 민감도(Sobol)" 도 식별성 증거로 세지 않는다 — 먼저 출력이 데이터인지 설계 KPI 인지 적는다.** 27호는 설계 KPI(`SOC_end`) 위의 전역판이다. 전차 지수 ≈0 은 비식별의 충분조건으로만 쓴다.
2. ★★★★ **모델 적합성과 식별성을 섞지 않는다** — "두 모델이 같은 곡선을 낸다" 는 적합성의 통과이면서 **모델 구조의 비식별**이다. 둘 중 무엇으로 읽는지 적는다.
3. ★★★★ **모델 비교 논문의 "보정 가능한 상수 차이" 는 알려진 구조량과 대조한다** — 27호의 상수는 비연결 몫 `1 − u` 와 맞았다. 보정은 그 상수를 **용량 손잡이**로 흡수한다.
4. ★★★ **ASSB 판 합성 truth 를 P2D 로 만들지 않는다** — 균질화 P2D 에서 접촉(연결) 손실의 자리는 `A_el-c`(용량 · 면적) 하나라, truth 단계에서 접촉 손실 = `LAM_PE` 가 된다. 연결 분율을 독립된 자리로 가진 모델이 필요하다.
5. ★★ **문턱 출력의 증폭을 확인한다** — `SOC_end` 는 OCP 평탄(3.67–3.69 V) 바로 아래 하한(3.6 V)에서 과전압 수십 mV 로 크게 움직인다. "배수" 로 인쇄된 모델 차는 출력 척도의 성질일 수 있다.
6. ★★ **낱말 지문은 NFKC 정규화 뒤에 센다** — IOP/ECS 조판의 `ﬁ` 합자가 `identifiab`·`fit` 을 0 으로 만든다(27호에서 0 → 1).

### 새 제약 (2026-09-23, Bizeray 2019 — 식별성 방법론 원전(액체셀)이 들어오면서 붙은 것)

1. ★★★★ **"식별성을 했다" 다음에 "식별 집합에 무엇이 있나" 를 적는다.** 28호는 동역학 축만 식별하고 **모드 축(용량 스케일 `Q_th` · 정렬 `x⁰`)을 입력으로 뺐다** — 그런 논문은 Q4 의 대상이 아니다.
2. ★★★★ **ASSB 모델의 묶음을 먼저 적는다** — 접촉(연결) 분율이 `ε` 처럼 **용량 묶음에만** 곱해지는 모델이면, 그 모델 안에서 접촉 손실 ↔ `LAM_PE` 는 항등이다(28호 SPM · 27호 P2D `A_el-c`). 가를 입력은 모델 밖에서 온다.
3. ★★★ **식별성 원전의 EIS 파이프라인을 그대로 옮기지 않는다** — 고주파 반원(`R_CT ∥ C_dl`)을 버리는 설계라 곱 축퇴 처방 1단계가 입구에서 막힌다.
4. ★★★ **사후 보정 손잡이가 어느 묶음에 걸리는지 본다** — 28호의 ×0.78(OCV 기울기)은 식별 집합에서 뺀 용량 스케일 자체다. 검증 데이터로 돌렸으면 그 그림은 독립 검증이 아니다.
5. ★★ **평탄 음극(Li-In · Li 금속)은 원전의 기준으로 "쉬운 쪽"이다** — `β₋ ≈ 0` 이면 음극 동역학이 전달함수에서 빠져 전극 맞바꿈 대칭이 없고 양극 `τ_d` 가 한 DoD 에서 식별된다(`[해석]`, 원전 Fig. 2 5·25 % · Fig. 5a 의 모양). **어려움은 동역학이 아니라 용량 스케일에 있다** — 이 카드의 물음 그대로.
6. ★★ **낱말 지문은 NFKC 뒤에, 쪽 머리글을 빼고 센다** — 28호 큐 지문 `identifiab` 9 는 전부 대문자 머리글이었고 본문은 합자 속에 있었다(정규화 뒤 54). IOP/ECS(27호)만의 문제가 아니다.

### 새 제약 (2026-09-23, Yanev 2024 — 율 외삽 적합과 ASSB 첫 적합 공분산 진단이 들어오면서 붙은 것)

1. ★★★★ **외삽 용량(`Q_M`, "무한 저율 용량")을 쓰기 전에 종료 율에서 곡선이 평탄한지 본다.** 평탄이 창 밖이면 용량 스케일과 동역학 시간척도가 한 조합(`Q_M·α⁻ⁿ`)이다 — 29호 sc84 는 실측 177 → 외삽 ≈236 이었다.
2. ★★★★ **논문이 식별성 진단을 인쇄했으면, 그 진단이 경고한 셀이 결론의 어디에 쓰였는지 추적한다.** 29호는 sc90 을 진단으로 제외해 놓고, 같은 문제를 가진 sc84 의 외삽값으로 "이용률 최대 · LIB 초과 · 절연 SE 껍질" 을 말했다.
3. ★★★ **이용률의 분모(물질 용량 기준)가 한계인지 확인한다** — 유한 율(0.1 C) 액체 반쪽전지 용량은 이용률 >100 % 를 허용한다. 기준이 한계가 아니면 `θ` 는 정의되지 않는다.
4. ★★★ **GITT `D` 는 `D·(A_eff/V)²` 다** — 면적을 BET 로 넣은 "겉보기 `D`" 의 차이를 확산으로 읽든 접촉 면적으로 읽든 **같은 숫자의 이름 붙이기**다. 둘을 가르는 것은 수입한 기준(`D_LIB`)이고, 그 기준도 면적을 진다(gran/sc 2.7 배).
5. ★★ **`n` ≈0.5 를 "고체 확산" 으로 읽지 않는다** — CA 누적 전하의 시간 지수이고, 다공 전극 이온 전송선(TLM)도 √t 를 준다. 저항 = SE · 확산 = AM 배정은 가정이다.
6. ★★ **두 "독립" 측정이 실험 설계 위에서 공선인지 본다** — 29호 `σ_eff` ↔ `D` Spearman 0.94(13 셀). 공선인 두 회귀변수 중 "더 잘 모이는 쪽" 은 병목의 증거가 아니다.
7. ★★ **2전극 율 시험의 고율 꼬리는 상대극 과도를 포함한다** — 같은 연구실 17호의 3전극이 같은 음극에서 CA 시작 ca. 0.9 V 를 인쇄했다. 검증된 창과 해석하는 창이 같은지 적는다(Q5 열한 번째 형태).

### 새 제약 (2026-09-23, Park 2024 — 방향 비대칭을 2전극으로 잰 편이 들어오면서 붙은 것)

1. ★★★★ **인쇄된 방향 라벨(산화/환원 · 고체/액체)을 쓰기 전에 그 논문 자기 그림에서 한 번 다시 구한다.** 30호는 b 의 산화/환원이 그림과 반대였고(`[재현]` 0.58/0.73 ↔ 인쇄 0.76/0.58), Table 1 용량 행이 그림과 맞지 않았다. 정리 표만 읽으면 둘 다 놓친다.
2. ★★★★ **2전극 방향 비대칭은 두 전극의 합이다** — Li 금속 · Li-In 상대극은 충전 ↔ 방전에서 다른 과정(석출 ↔ 박리)을 한다. 방향 비대칭을 양극에 배정하려면 **대칭셀 방향별 분극**(±i) 또는 3전극으로 상대극 몫의 상한을 먼저 뺀다(Q5 열두 번째 형태).
3. ★★★ **율 스윕 외삽(`Q_M`)은 스윕 중 정적 용량이 움직이지 않을 때만 정적이다** — 블록당 수십 사이클의 율 시험은 표류와 율을 섞는다(30호 0.1 C 블록만 −26 %). 29호의 "종료 율 평탄" 조건과 **별개의** 두 번째 조건이다.
4. ★★★ **액체 대조로 `D` 를 비교하면 먼저 면적이 같은 대조인지 본다** — Randles–Ševčík · GITT 모두 `D_app ∝ 1/A²`. 다공 전극 전체가 젖는 액체 ↔ 펠릿 한 면이 닿는 고체는 **면적이 정의상 다른 대조**다.
5. ★★ **SE 전도도가 대칭셀 호를 포함하는지 본다** — 30호 σ 는 펠릿 면적이 무엇이든 고주파 절편만으로는 안 나오는 값이었다(`[재현]` ≥239 Ω 필요 ↔ 절편 ≈125 Ω). 호에 **Li\|SE 계면이 섞여 있으면 상대극 몫이 "SE 물성" 으로 흡수**된다.
6. ★★ **대소문자 무시 지문은 짧은 낱말에서 부풀린다** — 30호 `ICI` 21(coeff**ici**ent) · `MPa` 20(co**mpa**re) · `LLI` 2. 큐 30 번(ICI) 지문은 **대소문자 구분 + 낱말 경계**로 센다.

### 새 제약 (2026-09-23, Biçer 2025 — BMS·열관리 종설이 들어오면서 붙은 것)

1. ★★★★ **종설의 요구 문장을 계보의 "요구 측 인쇄" 로 셀 때, 그 문장이 매단 인용을 한 칸 더 올라가 확인한다.** 8호 §6.1 의 "contact loss ↔ ordinary aging 진단" 은 32호에 없다 — 인용 한 칸 위에서 명제가 사라졌다. 요구의 첫 인쇄 = 8호.
2. ★★★ **BMS 문헌의 "SOH" · "SEI" · "balancing" 은 우리 어휘와 이름만 같을 수 있다.** 32호: SoH 정의 0 · SoC 분모 = 정격 용량 · SEI = solid electrolyte–electrode **interface** · balancing = 팩 셀 간 평준화(우리 = 전극 화학량론 정렬). BMS 쪽 근거를 옮길 때 **정의를 먼저 대조**한다.
3. ★★★ **OCV–SoC 를 "선형" 으로 두는 추정기 서술에서는 전극 분해의 식별성을 물을 수 없다** (`[해석]`) — 선형 OCP 에서 스케일·오프셋은 한 조합이다. BMS 쪽 제안을 우리 분해 파이프라인에 붙일 때 **그 제안이 OCP 모양을 입력으로 쓰는지**부터 본다.
4. ★★ **bipolar 적층 ASSB 에서는 셀별 OCV 곡선의 관측 가능성이 먼저다** (`[해석]`, 32호 Fig. 3 이 그 구조를 그린다) — α·β 하네스는 셀별 곡선을 입력으로 받는다. 스택 전압만 보이는 패키지면 식별성 이전에 관측이 없다.
5. ★★ **그림의 소수점 표기와 본문의 천 단위 표기를 대조한다** — 32호 Fig. 6B `5.473 KJ/g` → 본문 `5473 kJ.g−1`(×1000). 점을 천 단위 구분자로 쓰는 표(32호 Table 1 "2.200 mAh")가 같은 지면에 있으면 특히.

### 새 제약 (2026-09-23, Zhang 2025 — 저압 종설이 들어오면서 붙은 것)

1. ★★★★ **종설의 "요구치" 는 단일 값이 아니라 띠로 적는다** — 계보 5 편이 네 값(≈1 · 0.4–1 · 2 · 5 MPa)을 인쇄했고 **확인된 원전은 0**. 33호는 Xu 2024 를 인용하면서도 8호의 "<≈1 MPa" 를 옮기지 않는다. 산업 아래 벽 = **0.4–5 MPa 띠 + 원전 0**.
2. ★★★ **같은 원전을 두 편이 인용하면 두 명제를 나란히 놓고 본다** — Sakka 2022 는 25호에서 "`θ(P)` CT 분율", 33호에서 "3D 접촉 · 압력 방향". 인용 횟수는 원전의 **어느 명제**가 쓰였는지 말하지 않는다.
3. ★★★ **종합 층에서 "접촉 손실 → 사이클 감쇠" 문장을 만나면 그 인용 원전의 배정을 확인한다** — 33호 §3.2.1 은 23호의 "첫 충전 = 접촉 / 이후 = 계면상" 배정을 뒤집어 옮겼다.
4. ★★ `[해석]` **압력 되돌림 분리 시험은 상대극 압력 진동을 먼저 뺀다** — 재수록 원자료에서 합금·Si 음극 셀의 사이클당 ΔP ≈0.7–2.3 MPa(기저 20–45 MPa, 정변위) ↔ 양극만 ≈0.05–0.07 MPa. 산업 운전 압력(≤2 MPa)에서 이 진동은 조작 변수 `P` 와 같은 크기다.
5. ★★ **재수록 그림의 수치는 캡션 · 본문의 출처 번호가 일치할 때만 원전에 귀속한다** — 33호 그림 8 장 중 3 장이 갈린다.

### 새 제약 (2026-09-23, Liang 2026 — 능동 펄스 BMS 논평이 들어오면서 붙은 것)

1. ★★★★ **낱말 지문은 NFKC 정규화 뒤에 센다 — 원시 텍스트 층의 0 은 "없음" 이 아니다.** 34호에서 합자 `ﬁ` 가 `identifiab`(0 → 3) · `confidence interval`(0 → 1) 을 가렸고, 같은 검사로 큐 35 번 `confidence interval` 도 0 → 6 이다. 그리고 텍스트 층은 위첨자 음부호를 잃는다(34호 `10⁻¹ Hz` → "101Hz") — 대역 · 지수 값은 렌더로 확인한다.
2. ★★★ **"입력 설계로 식별성을 높인다" 는 명제를 만나면 구조적 ↔ 실제적 비식별을 먼저 가른다** — D-optimality · PE · OED 는 FIM 이 정칙인 방향만 개선한다. 곱 축퇴처럼 모든 입력에서 FIM 이 특이하면 입력 설계는 0 을 준다.
3. ★★★ **재구성 특징(학습 사상이 만든 EIS · IC · DV)은 처방 입력이 아니다** — 처방이 요구하는 것은 적합된 `R` · τ · `k` 다. 재구성 경로를 쓰면 샘플링 대역(나이퀴스트)과 사전의 몫을 먼저 적는다.
4. ★★ **"불변 특징" 학습은 처방의 채널을 버릴 수 있다** — 온도 불변 사상은 3단계-a(`Ea`) 의 재료를, 열화 불변 사상은 α·β 가 푸는 화학량론 한계를 지운다.
5. ★★ **"bipolar" 는 두 뜻이다** — 34호 "bipolar pulse sequences"(양·음 교대 펄스) ≠ 32호 bipolar 적층(셀 직렬 일체형). 펄스는 **입력** 설계이고 32호의 결손은 **출력**(셀별 전압) 관측이라 서로를 메우지 않는다.


### 새 제약 (2026-09-23, Roman 2021 — 불확실성 보정 SOH 파이프라인이 들어오면서 붙은 것)

1. ★★★★ **예측 구간의 보정은 식별성이 아니다.** 적중률 · 날카로움 · β 는 스칼라 목표 위에서 닫힌다. 모드 분해의 유일성은 **해 집합의 폭**으로만 말한다 — BMS 쪽 "calibrated uncertainty" 를 Q4 근거로 옮기지 않는다.
2. ★★★ **SOH 를 목표로 한 특징 선택 목록에서 분리 채널을 찾지 않는다** (`[해석]`) — 분리 정보는 용량과 직교하므로 선택이 먼저 버린다(35호: 저항 채널 3/3 그룹 탈락). 34호의 "사상이 지운다" 에 이은 두 번째 경로("선택이 지운다").
3. ★★★ **`C_score`(목표 적중률) 는 목표와의 거리로 읽는다** — 90 % 목표에서 100 은 과소 확신, 55 는 과대 확신이다. 35호 본문은 100 을 칭찬하고 54.70 을 "low calibration error" 로 적는다. 그리고 **그룹 평균 적중률 ≠ 셀 적중률**(35호 Fig. 4b 한 셀은 보정 뒤 ≈74 %).
4. ★★ **ML 입력 목록에서 데이터셋 표지와 과거 라벨을 먼저 찾는다** — 정격 용량 · 충전 전류(여러 데이터 묶음이 섞인 그룹에서 묶음 표지) · 누적 방전 용량(이전 사이클 측정 라벨의 합). 있으면 "online · unknown capacity" 주장의 조건을 다시 적는다.
5. ★★ **이름 충돌 — "α-accuracy · β"(Saxena 2008 예측 지표) ≠ 우리 α·β(전극 스케일 · 오프셋).** BMS/PHM 문헌을 옮길 때 `α_acc` · `β_mass` 로 적는다. 그리고 낱말 지문 열의 **대소문자 규칙**을 표에 명시한다(큐 34 번 `calibrat` 39 = 대소문자 무시, 규칙대로면 36).

### 새 제약 (2026-09-23, Thelen 2024 — 확률적 ML 종설이 들어오면서 붙은 것)

1. ★★★★ **불확실성을 aleatory/epistemic 으로만 가르는 문헌에서 식별성의 자리를 찾지 않는다.** 구조적 비식별은 **데이터량 불변**이라 둘 어디에도 안 맞는다 — 폭을 보고할 때는 "구조적 폭(데이터량 불변) ↔ 잡음 폭(데이터량에 따라 줄어듦)" 으로 가른다.
2. ★★★ **확률적 모드 진단을 만나면 공분산/능선을 보고했는지 먼저 본다** — 평균장 VI 와 상관된 학습 사전은 둘 다 곱 방향의 폭을 지운다. 주변분포만 좁게 보고됐으면 Q4 근거가 아니다.
3. ★★★ **"사후(posterior)" 가 무엇의 사후인지 적는다** — ML 가중치 `θ` · RVM 가중치 `ω` 의 사후는 물리 파라미터의 해 집합이 아니다(36호 `posterior` 26 회 전부 가중치).
4. ★★ **구간 이름은 36호 정의로 부른다** — CI(평균 · 파라미터의 정밀도) ⊂ PI(새 표본 하나) ⊂ TI(모집단 비율). BMS/PHM 문헌의 "confidence interval" 이 실제로 무엇인지(35호 = PI) 대조한다.
5. ★★ **재작도된 기구→모드 그림은 원본과 대조한다** — 36호 Fig. 3 은 Birkl 원본의 연결선을 전부 잃었고 캡션만 연결을 말한다. 접촉 손실의 소속은 **원본**에서 읽는다.
6. ★★ **낱말 지문은 부분문자열 수와 규칙 수를 함께 적는다** — pymupdf 추출에서 공백이 사라진 줄이 있으면 낱말 경계 규칙이 낱말을 놓치고(36호 `uncertaint` 9), 줄끝 분철도 놓친다(+10). 아래 첨자가 붙은 약어(`LAMPE`)는 `\bLAM\b` 에 안 걸린다.

### 새 제약 (2026-09-23, Li 2024 — 9호가 위임한 원형 모델이 들어오면서 붙은 것)

1. ★★★★ **ASSB 합성 truth 에 접촉 손실을 넣을 때 `ε_p` 도 `A_eff` 도 쓰지 않는다** (`[추론]`) — `ε_p` 면 `LAM_PE` 와 정의상 같고, `A_eff` 면 OCV 에 안 보이며 `k` 와 항등이다. 필요한 것: 용량에 곱해지되 `ε_p` 와 별개인 `θ` · 비연결 입자가 자기 SOC 의 리튬을 붙듦(`_li`) · 죽은 부피가 전해질이 되지 않음 · `θ` 에만 반응하는 조작(압력 되돌림) · 면적에 비례하는 이중층. 우리 `LAM_PE` 코드의 형태는 `degradation-degeneracy/docs/07_LAM_LLI.md` §2 가 정본이다. → **2026-09-23 사용자 결정(마): 이 목록과 뒤 편들의 추가분을 [[assb-synthetic-truth-contact-loss-requirements]] (R1–R8) 로 분리했다.**
2. ★★★ **모델 논문의 접촉 파라미터는 각주(층위)부터 본다** — 37호 `A_eff` 는 각주 없이 다른 셀(9호)로 네 자리 그대로 옮겨졌다. 같은 연구실의 후속 편에서 같은 값을 보면 **셀 성질이 아니라 모델 상수**로 읽는다.
3. ★★★ **율별로 다시 맞춘 파라미터(37호 `D_p,ref(C-rate)`)가 있으면 율 스윕을 분리 근거로 쓰지 않는다** — 율에 따른 잔여 손실이 그 파라미터로 먼저 들어간다.
4. ★★ **"Measured with SEM" 입자 반경은 같은 지면의 SEM 과 대조한다** — 37호 9.315 µm ↔ Fig. S1 ≈0.5–1.5 µm. 틀린 `R_s` 는 `D_p`(`R_s²/D_p`) · `k_p`(`k·ε/R_s`)가 흡수해 적합을 깨지 않는다.
5. ★★ **"sensitivity" 판정이 용량에서 한 말인지 전압에서 한 말인지 적는다** — 37호 "minimal deviation" 은 용량 끝점에서만 맞고 전압은 RMSE 의 3–5 배 움직인다.

### 새 제약 (2026-09-23, Conforto 2021 — 사이클 해상 활성 질량이 "접촉 손실 정량" 으로 들어오면서 붙은 것)

1. ★★★★ **38호 `m_act(N)` 을 접촉 손실 `θ(N)` 으로 쓰지 않는다.** 이완 OCP 두 점이 재는 것은 `θ·ε_p` 합(= 우리 `LAM_PE` 라벨과 같은 층)이다. 쓸 수 있다면 **합의 상한 후보** — 그것도 이완 편향(아래 2)과 방법 바닥(Fig. 6 SC ≈1.005)을 적고서.
2. ★★★ **이완 OCP 로 질량 · SOC 를 잴 때 이완 시간을 `L²/D̃` 와 같이 적는다.** 접촉 손실(경로 연장)은 그 조건을 스스로 깬다 — 38호 1 h ↔ `[재현]` PC N = 40 ≈13–17 h. 편향 방향 `[추론]`: 겉보기 `Δx` ↑ → 질량 손실 과대 → 동역학 손실이 질량 채널로 샌다.
3. ★★★ **EIS 저주파 꼬리로 경로 · 면적을 읽을 때는 용량성 극한에 닿았는지 먼저 본다.** 안 닿았으면 꼬리는 `L/(C_diff·√D̃)` 곱 하나이고, `C_diff` 를 다른 채널(OCP 질량)에서 고정하면 두 채널이 곱으로 거래한다. 닿았으면 `C_diff` 단독이 OCV 독립 활성 질량이다.
4. ★★ **평탄 상대극 셀의 활성 질량 분해능을 기준 전위 폭으로 적는다** — `[재현]` 3.77 V 기울기(0.38 V)로 ±10 mV ≈ ±4 %. 38호 SC 의 40 사이클 신호(≈9–10 %)와 같은 자릿수다.
5. ★★ **Li 과잉 반쪽전지의 "LLI 아닌 X 가 감쇠를 설명한다" 는 대안 공간이 설계상 좁다는 것과 같이 읽는다** — 38호 `[재현]` Li 재고 ×2.75: LLI 는 용량에 안 보인다. 남은 경쟁자는 계면 저항(38호 분해에 항 없음)이다.
6. ★★ **용량 분해 닫힘 그림은 패널별 잔차로 읽는다** — 38호 "good agreement for all the samples" 는 네 패널 중 둘에서만 선다. 9호의 기각("relatively large")은 그림에 맞다.
7. `[해석]` **37호 truth 요구 목록에 여섯째 후보**: OCV 관측의 **이완 시간**을 truth 파라미터로 둔다 — 그래야 `θ` 손실이 질량 채널과 동역학 채널 사이에서 어떻게 새는지 시험된다.

### 새 제약 (2026-09-23, Sakka 2022 — 영상으로 잰 접촉 면적 분율이 들어오면서 붙은 것)

1. ★★★★ **"접촉 면적 분율" 은 분모와 척도를 같이 적는다.** 39호 `φ` = NCM 표면 중 LGPS 와 닿은 몫(표면 피복, `A_eff` 쪽) · CT 화소 0.5 µm. 이것을 카드의 `θ`(연결 분율) · 37호의 `u`(통째 비연결 = `ε_p` 칸)로 옮기지 않는다.
2. ★★★★ **영상 면적과 `R_ct` 가 같이 있으면 `R_ct·φ` 를 먼저 본다** — 39호 ×13. 일정하지 않으면 "면적이 저항을 설명한다" 는 주장은 지면 안에서 기각된다.
3. ★★★ **분할의 질량수지를 검산한다** — 고정 혼합물의 상 부피비는 압력 · 사이클에 불변이어야 한다. 39호 NCM/LGPS 0.47 → 0.97. 흔들림이 효과보다 크면 추세의 크기를 쓰지 않는다.
4. ★★★ **압력 스윕의 "압력" 이 제조 압력인지 운전 압력인지 먼저 가른다** — 39호는 제조 가압 0 이라 스윕 압력 = 최대 압력 = 제조 압력(`[인쇄]`). 운전 압력(되돌림) 의 `φ` 로 쓰지 않는다. 16호(제작 = 운전)와 같은 부류, 25 · 33호(고압 제조 · 저압 운전)와 다른 부류.
5. ★★ **같은 셀 단계 가압의 용량은 사이클 번호와 교락된다** — 39호 S3 는 정규화("같은 사이클의 6 MPa 셀 대비")로만 증가하고 절대값은 12 → 100 MPa 에서 준다.
6. `[해석]` **37호 truth 요구 목록에 일곱째 후보**: **접촉 판정의 길이 척도** — 같은 미세구조가 0.5 µm 판정에서 `φ` ≈0.8 이고 `R_ct` 는 그 아래 척도에서 ×13 움직인다. truth 에 `φ` 를 넣을 때 척도를 파라미터로 둔다.

### 새 제약 (2026-09-23, Nam 2018 — In 가지의 원전 3전극이 들어오면서 붙은 것)

1. ★★★★ **3전극 논문을 읽을 때 기준극 위치와 "측정 채널 ↔ 파생 채널" 을 먼저 적는다.** 41호는 RE 가 **WE 뒷면**이고 CE 전위가 **WE/RE − WE/CE 파생**이라 분리막 옴 전부가 CE 채널로 간다(40호는 1 : 3.2 로 나눴다). 파생 채널의 부호 판정("Gr < 0 V")은 **전류 반전 계단의 절반**과 먼저 비교한다 — 41호 1 C ≈−0.02 ↔ ≈0.10 V.
2. ★★★ **컷오프가 WE/CE 에 걸린 셀의 "상대극 종단 전위" 는 항등식이다**(E_CE = E_WE + 오프셋). 어느 전극이 끝을 냈는가의 표시로만 쓰고, 상대극 과전압의 크기 곡선으로 쓰지 않는다(41호 Fig. 3c · 40호가 "선례" 로 인용).
3. ★★★ **쿨롱 효율을 `LLI` 로 읽기 전에 연성 단락을 배제한다** — 고율 충전 끝 이상 평탄 · 율 의존 쿨롱 효율 급락 · 얇은 SE 가 서명(41호). 무음극 재고 회계([[anode-free-li-inventory-accounting]])와 상대극 경로에 이은 **세 번째 오염 경로**.
4. ★★ **기준 전위 대조는 수를 인쇄할 때만 인용 사슬에 들어간다** — 41호의 Li 금속 대조(≈2 mV)는 SI 그림에만 있어 40호가 "0.62" 인용값을 가져갔다. 우리 요구서에서 기준 전위는 **측정값 · 조건 · 분해능**을 같이 적는다(처방 P11).
5. `[해석]` **α · β 이식 요구 하나**: ASSB 에서는 방전 끝을 **양극이 낼 수 있다**(41호 NCM 79.1 % < Gr 92.5 %). 균등화 · 모드 적합이 "음극이 끝을 낸다" 를 전제하면 첫 사이클부터 틀린다 — 끝을 내는 전극을 **3전극 한 번으로 확인**하고 시작한다.

### 새 제약 (2026-09-23, Santhosha 2019 — 0.62 V 의 액체셀 원전이 들어오면서 붙은 것)

1. ★★★★ **기준 전위를 인용할 때 원전의 전해질 · 셀 형식 · 이완 시간 · 조성 창을 같이 적는다.** In 0.62 V = 액체(LiTFSI DOL/DME) 3전극 · 0.5 h 이완 · 실온 · ≈1–47 at%(42호) · R-LTO 1.55 V = 액체(40호 → Costard). **계보의 두 영점 모두 ASSB 안 Li 대비 인쇄 측정이 0 이다** — 41호 SI 판독(≈0.621)이 유일한 간접 대조.
2. ★★★★ **"공칭 조성 창 안" 은 평탄의 필요조건이지 충분조건이 아니다.** 원전 창(≈1–47 at%)은 (2) 분리막 면 조성 · 율 · 온도를 말하지 않고, 17 · 21 · 41호의 이탈(+0.4 … +0.78 V)은 전부 창 안의 공칭 조성에서 일어났다. α · β 입력 명세에 창과 (2) 검사(P12 전류 펄스)를 **둘 다** 요구한다.
3. ★★★ **상대극 조성은 질량과 치수 둘로 검산하고 오차 막대를 단다** — 42호 44.1(질량) ↔ 49.6 at%(치수)가 창 끝(47)을 가로지른다. 창 끝 너머는 1.9 at% 에 −280 mV 다.
4. ★★★ **2전극 · 대칭셀 저항을 SE 벌크 옴(두께 ÷ 전도도)과 먼저 비교한다** — 작으면 전자 경로를 먼저 의심하고, 그 셀의 "상대극이 전류를 냈다" 류 명제를 이온 전류로 인용하지 않는다(42호 ×1/25–1/47).
5. ★★ **같은 축 이름 아래 다른 기준이 있는지 본다** — 42호 SI Fig. S3 는 두 조성의 상대극(공칭 0.62 ↔ <0.2 V)을 같은 "V, Li⁺/Li-In" 축 · 같은 0.7–3.0 V 창에 그리고 차이를 히스테리시스로 읽는다. `[재현]` 중점이 기대 이동(≥+0.4 V)을 보이지 않는다(≈−0.03 V) — 공칭 조성 ≠ 작동 기준의 표본 후보.
6. `[해석]` **상대극에도 카드의 곱이 있다** — 42호 `[인쇄]` InLi 형성 부피 +53 % → "local decontacting" → 불활성 In(`[재현]` ≈11 %). 반쪽전지 · 완전지에서 상대극 용량 창이 공칭보다 좁아지면 그 끝은 양극 `LAM` 서명으로 보인다(17호 경로의 재료 쪽 원인 하나).

### 새 제약 (2026-09-23, Fukunishi 2023 *ACS AEM* — 흑연 음극 3전극 열화가 들어오면서 붙은 것)

1. ★★★★ **반쪽전지 음극의 용량 손실을 `LAM_NE` 로 읽지 않는다 — `(1−LAM_NE)(1−u)` 곱으로 적는다.** 상대극 저장소가 `LLI` 를 지우므로 남는 것은 물질 손실과 고립(접촉)이다. 우리 α · β 이식판이 반쪽전지 음극 자료를 받으면 이 곱을 **한 칸**으로 둔다.
2. ★★★★ **dQ/dV 로 `LAM` 을 배정할 때 봉우리 높이가 아니라 넓이(적분)를 쓰고, 봉우리마다의 비를 적는다** — 43호 높이 비 0.53–1.03 은 용량 비 0.76 과 모양이 다르다(넓어짐).
3. ★★★ **면적 서명(1단계)을 같은 셀 저율 용량 비와 대조한다** — 면적 비 < 용량 비면 피복 손실이 있다(고립만으로는 설명 불가). 그리고 **3-b(`C` 가 이중층 상한 안인가)를 먼저** 본다.
4. ★★★ **노화 뒤 여러 호의 `Ea` 가 한 값으로 모이면 성분별 기구 배정을 멈추고 근최적 폭부터 본다** — 43호 27.6 · 27 · 27.5.
5. ★★ **기준극 표류는 두 평탄 증인의 공통 모드로 읽을 수 있다 — 단 증인 값 자체의 인용 오차(0.60 ↔ 0.62)는 절대값을 못 정한다.** 합 일치(2전극 = 3전극 합)는 표류 검사가 아니다.
6. ★★ **"3.0 mg composite" 류 질량 모호성은 4단계(DC 히스테리시스 ↔ EIS `ΔR`)로 검산한다** — 전류가 ×5 갈리면 예측 과전압도 ×5 갈린다.

### 새 제약 (2026-09-23, Jin 2015 — 20호 셀 원전 · GITT 유효 면적이 들어오면서 붙은 것)

1. ★★★★ **GITT(Weppner–Huggins) 로 얻은 "유효 접촉 면적" 을 `S` 로 읽지 않는다 — `√D · S / θ` 로 적는다.** 한 셀의 가정으로 한 인자를 고정했다면, **그 가정의 근거가 비교 셀에도 성립하는지**를 먼저 본다(성립하면 쪼개기는 선택이다).
2. ★★★ **GITT 인용값은 계단별 값과 함께 가져온다** — 44호 인쇄 `D` · `S` 는 세 계단 중 하나(계단 간 ×2.5 · ×1.3).
3. ★★★ **2전극 완전지의 방전–충전 차를 전극 동역학에 배정하기 전에 Li 재고 수지(양극 빈자리 상한)를 한 줄로 검사한다** — 방전이 이전 충전을 넘어 양극 상한을 넘으면 방전 용량 일부는 양극 삽입이 아니다. 41호 누설(충전 > 방전)과 반대 부호의 오염.
4. ★★ **반쪽전지 GITT 의 `ΔE_s` 는 상대극 평탄 가정을 품는다** — 상대극(In 박)의 질량 · 조립 리튬화 상태가 없으면 `D` 는 `ΔE_s²` 로 그 가정을 증폭한다(계단당 1 mV → ×0.72–1.35).
5. ★★ **셀 원전과 파생 셀을 "같은 셀" 로 합치지 않는다** — 레시피가 같아도 SE 두께(×3.4) · 기준극 · 창이 다르면 원전의 σ · `D` 는 파생 셀에 조건부로만 옮겨진다.

### 새 제약 (2026-09-23, Hertle 2023 — "0 V 리튬화 금선" 원전이 들어오면서 붙은 것)

1. ★★★★ **리튬화 금선 기준극을 "0 V" 로 쓰려면 도금 Li 가 남아 있다는 증거를 같이 적는다** — 리튬화 곡선에서 사다리(Au/AuLi → AuLi/AuLi₃ → 도금 평탄) 도달 · 여분 전하 · 측정 시점. 원전 처방은 ∅10 µm · In/InLi 상대 · 8 µAh(2.55 mAh cm⁻²)이고 "≥8 일" 이다. 그 밖(16호 ∅25 µm · NMC 상대 · 0.27 mAh cm⁻²)은 0 V 를 물려받지 않는다.
2. ★★★★ **도금형 기준극의 이동은 연속 표류가 아니라 칸(+0.133 · ≈+0.215–0.25 V)이다** — 셀 간 · 시점 간 어긋남이 칸 크기에 가까우면 기준극 상태를 먼저 의심한다(16호 0.11 V).
3. ★★★ **3전극 반쪽 합 = 완전지(`Z_CR + Z_RA = Z_CA`)를 기준극 검증으로 쓰지 않는다** — 같은 셀이면 항등식이고, DC 전위도 위치 artifact(재분배)도 합에서 보이지 않는다. 20 · 40 · 43호 · 이 편(16호가 가져감) — 검증은 **개방회로로 알려진 평탄 대조 + 위치 · 재료 섭동**(P8 · P10).
4. ★★★ **반쪽 스펙트럼에만 있는 고주파 호는 `C` 상한으로 먼저 거른다** — 이 편 호 #1("SE separator") `[재현]` ≈10 nF ↔ 분리막 기하 10–100 pF.
5. ★★ **2전극 방전 용량 부족을 양극에 배정하기 전에 상대극이 Li 여분을 가졌는지 본다** — 빈 채로 조립한 상대극(LTO · 순수 In)은 첫 부반응의 `LLI` 만큼 방전 끝을 자른다.

### 새 제약 (2026-09-23, Schlenker 2020 — Au 도금 W 선 기준극의 가장 이른 ASSB 사용 · Li 금속 대칭셀 수명이 들어오면서 붙은 것)

1. ★★★★ **기준극의 하드웨어 출처와 영점 출처를 따로 적는다** — 같은 Au 도금 W 선이 Marburg(이 편 → 16호) 와 Giessen(Hertle) 에서 따로 쓰였고, 영점(0 V)은 Giessen 에만 있다. "같은 선" 이 "같은 영점" 을 물려주지 않는다.
2. ★★★ **영점이 필요 없는 자리(같은 금속 대칭셀 · AC 전용)에서 쓴 기준극을 영점의 선례로 인용하지 않는다** — 그 자리의 기준극 정보는 0 이다. 옮길 때는 P11(측정 셀 안 개방회로 대조)을 새 자리에서 한다. 같은 금속 대칭셀이면 RE–WE · RE–CE 개방회로 ≈0 V 두 숫자가 공짜 검증이다.
3. ★★★ **Li 금속 음극에서 겉보기 저항 · 과전압의 완만한 감소를 "접촉 개선" 으로 읽기 전에 연성 단락을 배제한다** — 대칭셀은 OCV ≡ 0 이라 개방회로 서명이 없으므로 단락 뒤 EIS 저주파 실수축 수렴 · 전압–전류 선형성을 쓴다. 완전지에서는 개방회로 자기방전이 가르는 신호다.
4. ★★ **"면적 또는 계면층" 을 가를 때 같은 셀 두 반쪽의 역방향 짝을 쓴다** — 박리 · 도금(양극이면 충 · 방) 쪽 부호가 반대면 형태, 같으면 단조 계면층. 한 반쪽에만 유도성 · 이상 호가 있으면 짝이 깨졌다고 적는다(45호 3-b 거름망).

### 새 제약 (2026-09-23, Solchenbach 2016 — 금선 기준극 원전(액체)이 들어오면서 붙은 것)

1. ★★★ **리튬화 금선을 0.31 V 로 쓰면 원전 사용 조건을 같이 적는다** — 리튬화 뒤 경과 시간(원전 초기 ≈20 h 제외, `[도표]` < 2 mV 는 ≈50 h 뒤) · 리튬화 온도 = 운전 온도 · 노출 형태(원전 = 절단면만) · 재리튬화 이력. 조건 밖이면 영점을 **±수 mV 불확실**로 적는다.
2. ★★★ **0.31 V 와 0 V 를 같은 선의 다른 칸으로 적는다** — 리튬화 량 · 리튬화 중 전위(원전 ≈0.2 V = 위 칸 · 45호 도금 평탄 = 아래 칸)로 어느 칸인지 보인다. 칸 값 표는 두 편이 다르다(0.3 / 0.2 ↔ 0.215 / 0.134 V) — 인용할 때 어느 표인지 밝힌다.
3. ★★ **"리튬화한 쪽 전극이 작다" 를 거칠어짐으로 적지 않는다** — 원전도 추론("We believe")이다. 면적 서명(τ 보존)까지만 적고, 원인은 대조군(반대 전극에서 리튬화)으로 가른다.
4. ★★ **기준극 검증을 범주별로 나눈다** — 위치(고주파 절편 대칭 · 분리막 질량비), 분배(외부 기준: 재조립 대칭셀), 표류(PEIS ↔ GEIS 또는 개방회로 추적). 각 검사의 **분해능은 같은 조건 셀 간 산포**로 적는다.

### 새 제약 (2026-09-23, Dugas 2021 — 전면 복합 기준층 · 상대극 창의 용량 번역이 들어오면서 붙은 것)

1. ★★★ **2전극 EIS 적합을 전극 귀속의 근거로 쓰지 않는다** — "적합이 만족스럽다" 는 귀속을 검사하지 않는다(48호: WE 모형이 WE + CE 합을 맞추며 중간 호 ×2.2). 같은 셀 3전극 반쪽 합으로 **한 전극 모형이 합을 맞추는지** 먼저 보고, 맞으면 그 호는 2전극에서 귀속 불가로 적는다.
2. ★★★ **상대극(또는 기준극) 창을 용량 오차로 번역해 적는다** — 창(mV) × 그 SOC 의 OCP 기울기 ⇒ mA h g⁻¹. 48호 원문 한 점(20 mV ↔ ⩽2 mA h g⁻¹, NMC 충전 끝)이 형식이다. 창이 전류 중 분극인지 휴지 이동인지 같이 적는다.
3. ★★ **기준극 기하를 원문 그림으로 확인한다** — "원형 기준극" 같은 2차 묘사를 옮기지 않는다(48호: 원형은 집전체, 기준극은 전면층). 전면층이면 층 질량 · 합금 분율 · 층 iR 을 적는다(쌍극 교환 — 개념 페이지 조건 (11)).
4. ★★ **호 제거 검정의 결과를 값 옆에 적는다** — 빼도 적합이 같으면 그 값은 곱의 입력이 아니다.

### 새 제약 (2026-09-23, Barai 2018 — 측정 시간 척도 ↔ 저항 값의 교차 방법 원전(액체)이 들어오면서 붙은 것)

1. ★★★ **시간 영역 저항 성분은 창 경계와 함께 적는다** — `R₀` · `R_CT` · `R_p` 를 쓰면 각각 **몇 초(또는 몇 Hz)에서 몇 초까지의 차분인지**, 경계가 시점 규약인지 모양 작도인지를 값 옆에 적는다. 경계 없는 성분 값은 방법 간 · 편 간 비교에 쓰지 않는다(49호: 같은 이름 ×2.0 · ×2.9 · ×13).
2. ★★★ **"순간" · "옴" 저항은 대역 위쪽 끝과 함께 적는다** — 샘플 간격 · 여기 최고 주파수보다 빠른 과정은 전부 거기 흡수된다(49호: 0.1 s = |Z|(10 Hz), +43 %). ASSB 에서 `R₀` 에서 SE 벌크를 빼 "접촉" 을 얻는 계산(20호)은 대역 끝이 SE · 입계 · 계면 호보다 느리면 계면 몫을 접촉으로 부른다.
3. ★★ **시간 ↔ 주파수 일치를 쓸 때 대응 규약과 스펙트럼 기울기를 같이 적는다** — t = 1/f 인지 1/(2πf) 인지, 그 대역의 |Z| 가 decade 당 몇 % 변하는지. 평탄한 스펙트럼에서 일치는 시간 척도를 ≈1 decade 로만 가른다(49호 R8).
4. ★★ **진폭을 적는다** — 같은 창에서도 진폭이 값을 바꾼다(49호 10 s 창 ×1.46, 대진폭 ↔ 소진폭 −24 % @ ≈0.017 Hz). 20호식 저율(C/72) 값과 고율 펄스 값을 같은 이름으로 대지 않는다.

### 새 제약 (2026-09-23, Miß 2022 — 16호 TLM 의 원본 · 면적 규약이 들어오면서 붙은 것)

1. ★★★ **`j₀` 는 면적 규약과 함께 적는다** — `a_v` 의 출처(구 기하 `3ε/r` · BET · 영상), `r` 이 측정인지 공칭 확인인지, TLM 이면 `a_v·τd` 인지 `a_v·d` 인지. 규약이 다르면 편 간 비교는 방향까지만(50호: 규약 한 줄이 ×6–7).
2. ★★★ **"`j₀` 가 X 와 함께 변한다" 는 `R_CT` 와 `C_dl` 을 같이 보고 적는다** — 같은 규약 · 같은 분말에서 τ = `R·C` 가 보존되면 면적 서명이다(50호 ↔ 16호: τ ×1.28 · `1/R` ×12). SE 가 바뀌면 `C ∝ θ` 전제가 약하다는 것도 같이 적는다.
3. ★★ **두께 스윕이 전이 구간을 가로지르는지 적는다** — 두꺼운 극한만 본 재료(50호 LCO)의 `j₀` 는 τ 와 한 조합이다.
4. ★★ **상대극을 다른 셀에서 재어 빼면 그 셀의 조성 · 압력을 대상 셀과 대조한다** — 뺀 허수부의 부호를 확인한다(50호: 40 at% · 125 MPa ↔ ≈5–30 at% · 389 MPa, ≈10–120 Hz 음수).

### 새 제약 (2026-09-23, Oh 2025 *AEM* — 저압 N/P < 1 과충전 실셀 · 두 압력의 CE 가 들어오면서 붙은 것)

1. ★★★ **2전극 CE 를 `LLI` 로 쓰기 전에 누적 충–방 결손을 Li 재고 상한과 대조한다** — Σ(Q_ch − Q_dis) 가 양극 이론 Li 재고 · 형성 때 남은 저장소 · 관측 용량 손실의 합을 넘으면 초과분은 누설이다(52호: 3 MPa ≈575 ↔ 재고 ≈275).
2. ★★ **조건 간 CE 비교는 면적당 결손으로 적는다** — 양극 적재가 다르면 CE 차의 대부분이 분모다(52호: CE ×≈7 ↔ 면적당 ×≈1.8).
3. ★★ **평탄 음극(도금 Li) 셀은 끝 전극 모드를 먼저 정한다** — 양극이 방전 끝을 내면 Li 를 잃어도 CE ≈1 이고 `LLI` 는 저장소가 소진될 때까지 안 보인다; 음극이 끝을 내면 `LLI` 가 곧 용량 손실이다.
4. ★ **압력 두 점은 적재 · N/P 와 교락됐는지 먼저 본다** — 52호 20 ↔ 3 MPa 는 양극 20 ↔ 6 mg cm⁻² · N/P 0.15 ↔ 0.66 과 같이 바뀌었다.

### 새 제약 (2026-09-23, Ren · Danner 2023 — 산화물 공소결 복합양극 종설 · 시간 배정 역전이 두 번째로 나오면서 붙은 것)

1. ★★★ **접촉 손실의 시간 배정(첫 사이클 ↔ 이후)은 1차 원전에서 확인한다** — 종설 두 편(33 · 53호)이 23호 원문("only … initial charge")과 반대로 적었다. `θ(N)` 을 truth 에 넣을 때 계단형 · 점진형을 **가정으로 표시**하고 둘 다 돌린다.
2. ★★★ **산화물(소결) 복합양극은 `θ₀` 를 공정 변수로 적는다** — 소결 경로 · 상대밀도 · 냉각 이력 · 소결조제. 사이클 전 `θ` 를 1 로 두지 않는다(53호 모델은 1 로 뒀다). `[해석]` 소결 결합 파단은 재가압으로 안 되돌아가므로 재가압 분리 시험은 산화물에 그대로 옮기지 않는다.
3. ★★ **모델의 입경 손잡이가 확산 길이와 계면 면적을 같이 움직이는지 본다** — `a = 3ε/r` 규약이면 "확산 길이" 민감도는 곱이다(53호 `d50` 10 → 0.1 µm).
4. ★★ **직렬 계면 저항(`R_CT` · `R_SP`) 분할이 가정인지 적는다** — 소신호 EIS 는 합만 본다; 전류 진폭 의존(로그 ↔ 선형)이 두 칸을 가른다. 면적(접촉)은 두 칸 모두의 공통 인자로 남는다.

### 새 제약 (2026-09-23, Neumann 2021 — SE 입계 모형 원전 · 53호 `β` 의 출처가 들어오면서 붙은 것)

1. ★★★ **파라미터 출처는 원전 표의 표기까지 내려가 적는다** — "measured" 가 인용 두 단계를 거치며 붙은 사례(원전 Table S4 [°] 0 개 → 02호 "measured in dense pellets" → 원장 "measured 라벨"). 합성 truth · 모델 입력 표에 **측정 / 손 보정 / 외부 입력 / 구조 계산** 네 칸을 둔다.
2. ★★★ **SE 벌크 ↔ 입계(또는 SE ↔ 계면) 합을 나눈 값을 쓰기 전에 `f_C,B = σ/(2πε₀ε_r)` 를 측정 대역 상한과 비교한다** — 대역 밖이면 벌크 몫은 입력이다(54호 1.4–1.8 × 10⁷ ↔ 1.5 × 10⁷).
3. ★★ **펠릿에서 얻은 SE 유효 전도도 지수(`ε^β`)를 복합양극에 옮길 때 `ε` 범위 · 입도 · `σ⁰` 의 뜻을 같이 옮긴다** — 53호는 셋 다 어긋난다(0.43–0.75 → 0.25 · 입도 교락 · 입자 내부 ↔ 치밀 전체).
4. ★★ **교정된 `C` 가 물리 두께와 10² 배 이상 어긋나면 면적 · 두께 서명으로 쓰지 않는다** — 54호 `C_DL^GB` 등가 두께 ≈6.8 µm.

### 새 제약 (2026-09-23, Hlushkou 2018 — 구조 ↔ EIS 두 경로의 대조 원형 · void 의 수송 효과 계산이 들어오면서 붙은 것)

1. ★★★ **측정 경로와 구조 계산 경로를 비교할 때는 `τ` 가 아니라 관측 곱 `σ_eff/σ⁰`(= `ε/τ`)로, 같은 시편 · 같은 `ε` 로 한다** — 55호: `τ` 1.6 ↔ 1.74(9 %) · 곱 0.406 ↔ 0.309(31 %). EIS 쪽 `ε` 가 인쇄되지 않으면 그 `τ` 는 쓰지 않는다.
2. ★★★ **영상의 "void" 상에 수지 · 비전도 첨가물이 섞였는지 확인한다** — 55호 void 13.2 % = 수지 + 잔류 void(분리 0). 합성 truth 의 공극률 입력으로 옮기기 전에 측정 시편의 공극률(밀도 · 질량-두께 폐합)을 따로 찾는다.
3. ★★ **공극을 `ε` 만 줄이는 입력(Bruggeman)으로 넣으면 `τ` 를 과소평가한다** — 55호 `[인쇄]` 무공극 1.27 ↔ Bruggeman 1.22(맞음) · 실제 1.74 ↔ `[재현]` 1.365(틀림); 함의 지수 a 1.59 → 1.89. DEM · 합성 구조에서는 `τ` 를 구조로 계산한다.
4. ★★ `[해석]` **재구성 위 상 치환(void → SE)은 한 구조에서 void 의 경로 효과와 접촉 효과를 가를 수 있는 자리다** — 수송 모의와 함께 CAM 표면 분할(CAM–SE ↔ CAM–void)을 세면 된다. 55호는 경로만 했다.

### 새 제약 (2026-09-23, Bielefeld 2022 — void 를 접촉 자리에만 넣은 3D FEM · 01호 `p_c` 의 반례가 들어오면서 붙은 것)

1. ★★★ **표면 피복형 접촉 손실을 truth 에 넣을 때는 피복률 `φ` 와 함께 피복의 공간 분포(void 크기)를 기록한다** — 56호(모델): `φ` 70 % 고정에서 크기만으로 과전압 ×2.6–4.5. `φ` 한 칸으로 요약한 truth 는 이 차이를 가정으로 지운다.
2. ★★★ **"비적합" 선언 옆에 이산 선택 목록을 적는다** — PSD 절단 · 입력 세트 · 수작업 연결 같은 선택이 실험 일치로 이루어졌으면 곱의 한 인자(여기선 면적 — PSD 가 0.113–0.173 m² g⁻¹ 를 정한다)가 사실상 맞춰진 것이다.
3. ★★ **검증 모델에서 공극을 SE 로 채우지 않는다** — 56호 입자형 모델은 실험 void 14 % 를 SE 로 채웠다(`[재현]` SE ×1.32). 37호 조건 (iii)("죽은 부피가 전해질이 되지 않는다")의 공극 판이다.
4. ★★ **`j₀` 를 문헌에서 들여올 때 `R_CT → j₀` 환산의 면적 `A` 와 온도를 원전에서 확인한다** — 56호 식 (12) `A` 미정의 · `T` 273.15 K 인쇄. 규약 차는 `[재현]` ≈×13.6(모델 CAM 면적 ↔ 전극 단면).
5. ★★ `[해석]` **"퍼콜레이션 모델이 실험과 어긋나면 구조를 손으로 맞춘다" 는 기록은 `θ` 의 관측 불가능성 표본이다** — 01호 `p_c` 예측(42 vol% 는 문턱 아래)과 실험 셀이 어긋났고, 결과는 `θ` 입력 1. ASSB truth 에서 `θ` 를 정할 때 퍼콜레이션 모델 한 개의 출력을 쓰지 않는다.

### 새 제약 (2026-09-23, Bielefeld 2020 — void · 바인더 → 유효 이온 전도도 모델과 "pore 문턱" 귀속 판정이 들어오면서 붙은 것)

1. ★★★ **"void(pore) 문턱 → 저항 급증" 을 truth 입력으로 쓰지 않는다** — 14호가 56호에 붙인 문장은 01 · 56 · 58 어디에도 문장 그대로 없다(57호 §7). 01호의 공극률 문턱(≈34 %)은 퍼콜레이션 이용률 판정이고, 57호 void → `σ_eff` 는 세 점 단조(×2)다.
2. ★★★ **공정 손잡이(바인더 · void)를 대조군으로 쓸 때 두 곱의 몫을 따로 적는다** — 57호(모델): 바인더는 `θ_AM` 불변 · `A_spec,a` ↓ · `σ_eff` ↓ · `θ_SE` ↓ 를 동시에 만든다. `A_eff` 하나로 요약한 truth 는 수송 몫을 가정으로 지운다.
3. ★★ **검증 일치 폭을 가정 손잡이 폭과 비교한다** — 모르는 입력(void)을 가정한 한 점 대조(57호 Kato: 곱 7 %)는, 그 입력의 영향(같은 지면 ×2)보다 일치가 좁으면 모델 검증이 아니다.
4. ★★ **구조 모델의 면적 비와 GITT "접촉 면적" 을 대조할 때 GITT 쪽은 `D·(A/V)²` 곱으로 적고, 모델이 퍼콜레이션 문턱 아래인 점은 뺀다** — 57호 Fig. 5d 의 "작은 AM 일치" 는 ≈0 ÷ ≈0 이다.
5. ★★ `[해석]` **`τ²` 를 옮길 때 나눈 `ε` 의 규약(순수 SE · SE+바인더 · void 포함 여부)을 같이 옮긴다** — 57호 자신이 `τ²` 는 순수 SE 로 나누고 전류 추정은 SE+바인더로 곱해 ×1.15–1.30 을 만든다(D4).

### 새 제약 (2026-09-23, Asheri 2023 — 박리 CZM 두 단계 모델 + 신경망 대리가 들어오면서 붙은 것)

1. ★★★ **미세-거시 결합 모델로 truth 를 만들 때 손상 변수의 자리를 질량 보존으로 검사한다** — "미세 입자 채움 속도 × 입자 부피 분율 = 거시 소스" 가 손상이 있을 때도 성립하는가. 성립하지 않으면(58호: 미세 유입 `d` 무관 · 거시 `a·(1−⟨d⟩)`) 그 변수는 `A_eff` 가 아니라 `ε_p` 손잡이다. 보조 검사: 저율 극한 용량 손실이 `∫⟨d⟩dSOC` 면 `ε_p` 자리, ≈0 이면 `A_eff·k` 자리.
2. ★★★ **이력 변수(손상 · 경화)를 기억 없는 대리로 넘기지 않는다** — 58호 대리는 입력에 `⟨d⟩` · `ξ` 가 없고 출력 ReLU 가 충전을 막는다. `θ(N)` truth 에는 상태를 입력으로 받는 대리(또는 원 모델)만 쓴다.
3. ★★ **대리모형 검증은 궤적(또는 격자점) 단위로 나눈다** — 행 무작위 분할의 R²(58호 0.99)는 같은 궤적 안 보간 충실도다. unseen 검증은 학습 격자 밖의 **플럭스** 와 **재료 파라미터**를 함께 빼야 한다(58호는 `G_c` 두 점만, `j` 는 격자 값).
4. ★★ **"율이 손상을 빠르게 한다" 류는 전하(리튬화) 축으로 다시 적는다** — 58호 미세 자료에서 손상은 SOC 의 함수이고, 시간 축 "빠름" 은 대부분 시간 압축이다.

## Status Log

- **2026-09-16 (개설)** — 카드 생성. `assb` 섹션의 닻으로 지정. 보류 항목.
- **2026-09-16 (ingest 1)** — `assb` 1호 논문 흡수:
  `raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md`.
  컴파일: [[composite-cathode-percolation-utilization]].
  **미결 항목 1 의 "형태" 가 정해졌고 "동역학" 이 남았다.** Q1~Q8 채움표 개설 (1.5/8).
  후속 후보 1 순위 = Strauss et al. 2018 (ref 13, measured `1 − θ_AM`),
  2 순위 = Koerver et al. 2017 (ref 7, 접촉 손실의 실험 원전 + 용량축).
- **2026-09-16 (ingest 2)** — `assb` 2호 논문 흡수:
  `raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md`
  (Clausnitzer et al., *Batteries & Supercaps* 2023, 6, e202300167; 본문 16쪽 + SI 10쪽,
  둘 다 sha256 봉인). 컴파일: 새 개념 [[assb-apparent-capacity-decomposition]] +
  [[composite-cathode-percolation-utilization]] 갱신(좌표 변환표 · 반례 · 산포 후퇴).
  **셋 중 하나가 들어왔다**: **전압축 ★있다**(`U₀ 4.2 V`·`U_cut 3.4 V`·Fig. S5 `V`–`Q`·
  `Wh/kg_cell`) / **동역학(시간축) 없다**(방전 1회, 사이클 0, 역학 0) /
  **시드 산포 없다**(오차막대 0, 점당 구조 1개 — 1호보다 **후퇴**).
  최대 수확은 **`θ` 만으로는 겉보기 용량을 설명 못 한다는 논문 내부 반례**와,
  그로부터 나온 **율 스윕 분리 시험**. Q1~Q8 채움표에 행 추가 (누적 ≈2.5/8).
  후속 후보 1 순위 = Ren/Danner/Finsterbusch/Latz et al. *Adv. Energy Mater.* 2022, 2201939
  (ref 17 — 이 논문이 열화·최적화 양쪽에서 가장 많이 인용, `θ(N)` 시간축의 입구),
  2 순위 = Neumann et al. *ACS AEM* 2021, 4, 4786 (ref 38 — GB 모형 원전 + EIS measured 라벨).
- **2026-09-16 (ingest 3)** — `assb` 3호 논문 흡수:
  `raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md`
  (Liu, Roters, Raabe, *Nat. Commun.* 2024, 15, 7970; 본문 18쪽 + SI 10쪽, 둘 다 sha256 봉인).
  컴파일: 새 개념 페이지 없음(SCHEMA Page Thresholds — 이 논문의 좌표는 `θ` 로 변환되지
  않아 기존 두 개념에 **제약**으로 붙는 편이 정확하다), 대신
  [[assb-apparent-capacity-decomposition]] 과 [[composite-cathode-percolation-utilization]]
  양쪽 갱신.
  **셋 중 하나만 들어왔다**: **OCV 곡선 ★있다**(SI Fig. S2, GITT, 3.0→4.4 V) ·
  **율 스윕 ★있다**(SI Fig. S4, 0.25–5C × 4 크기 = 20 곡선 — `i→0` 에서 전 크기 ≈1 로
  수렴, 3항 분해의 `η(i)→1` 이 독립 모델에서 확인됨) /
  **`θ(N)` 시간축 없다**(방전 1 회 + 충전 1 회, 사이클 축 0 장, **파괴·디본딩 모형 없음**) /
  **실험 없다**(자기 실험 0, 3/3 편 공통; 대조 자료는 **Si 음극·황화물 셀**(Fig. 4a)과
  **액체셀**(Fig. 5e)에서 왔다) / **시드 산포 없다**(실현 1 개 — "무작위 배열이 결정적"
  이라고 적고도).
  최대 수확 둘: ① `[인쇄]` **"실험의 활물질 손실은 rock-salt + 파괴로 고립된 활물질을
  둘 다 포함한다"** — 이 카드의 축퇴가 문헌 문장으로 확인됐다. ② **`Q_material` 이 율
  의존**이라 우리 율 스윕 분리 시험이 좁아졌다.
  어긋남 원장 **18 건**(1호 8 · 2호 14 · 3호 18), 그중 무거운 묶음은
  **D3·D4·D5·D6**(초록의 접촉 손실 인과 주장 ↔ 모델에 파괴 없음 · Fig. 5 의 손실 기준이
  자기 방전곡선과 화해 안 됨 · "kinetic capacity loss" 가 세 곳에서 다른 뜻 ·
  Fig. 7 의 "≥90 % usable capacity" 라벨이 자기 Fig. 5d 와 모순) —
  **결론을 떠받치는 문장이 자기 그림과 충돌하는** 2호와 같은 형태다.
  Q1~Q8 채움표에 행 추가 (누적 ≈3.0/8).
  후속 후보 1 순위 = **Koerver et al. *Chem. Mater.* 2017, 29, 5574** (3 편이 모두 인용;
  접촉 손실의 실험 원전 + 용량축 + 사이클 — **`θ(N)` 은 실험 쪽에서만 나온다**),
  2 순위 = **Shin et al. *Adv. Energy Mater.* 2023, 13, 2301220** (저압 조건 ASSB 열화 —
  **Q6 을 채울 첫 후보**).

- **2026-09-16 (ingest 4)** — `assb` 4호 논문 흡수:
  `raw/papers/shi2020_mechanical-degradation-assb-cathode.md`
  (Shi, Zhang, Tu, Wang, Scott, Ceder, *J. Mater. Chem. A* **8** (2020) 17399–17404,
  doi `10.1039/d0ta06985j`; 본문 6쪽 + ESI 7쪽, 둘 다 sha256 봉인).
  ⚠ **업로드 파일명이 서로 바뀌어 있었다** — `Sup_` 이 붙은 쪽이 본문이다 (digest 머리).
  컴파일: **새 개념 페이지 1**([[assb-pressure-reapplication-separation-test]]) +
  [[composite-cathode-percolation-utilization]] · [[assb-apparent-capacity-decomposition]]
  양쪽 갱신.
  ★★ **이 계보 첫 실험 논문이고, 한 편에서 세 칸을 깼다**:
  **Q2(자기 실험 — 3/3 편 연속 0 이던 칸)** · **Q6(압력 — 3/3 편 `pressure` 0 회였던 칸)** ·
  **Q8(실측 사이클별 V–Q — 3호의 OCV 는 타 논문 액체 반쪽전지 GITT 였다)**.
  그리고 Q1 을 **무차원 분율 + 시간축**으로, Q5 를 **부분**으로 열었다.
  Q1~Q8 채움표에 행 추가 (**4편 누적 ≈5.5/8**). **남은 0: Q4(유일성) · Q7(dead Li).**
  최대 수확 셋:
  ① ★★ **분리 연산자가 하나 더 생겼다** — 50 사이클 후 **300 MPa 재가압**으로 용량이
  `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** (`[재현]` **+60.5 %p**). 율이 `η(i)` 를 지우듯
  **압력이 `θ_AM` 을 되돌린다**. **OCV 밖의 축**이 열렸다.
  ② ★★ **곱셈 형태의 실측 반례** — 같은 시점 접촉 손실 **면적 10.4 %** 인데 압력
  가역분이 **60 %p**. **≈6 배.** 논문은 두 수를 **한 번도 비교하지 않는다**(D9).
  ③ ★★ **논문의 인과가 자기 EIS 와 충돌한다** — `[도표]` 50 사이클에서
  **음극 쪽 `R_LF ≈110 kΩ` 가 전체 저항의 ≈93 %**(양극 `R_MF` ≈3.3 kΩ, **33 배**),
  재가압 회복률도 **LF 65 % vs MF 23 %**. 그런데 초록·결론은 **양극 접촉 손실**로
  돌린다(D8). → **Q5(In 기준극 안정성)가 채워지면서 동시에 문제로 드러났다.**
  어긋남 원장 **18 건**(1호 8 · 2호 14 · 3호 18 · 4호 18), 무거운 묶음은
  **D8(인과 ↔ 자기 EIS) · D9(10.4 % ↔ 60 %p 무비교) · D10(라벨과 관측이 다른 셀 —
  토모그래피 3 셀의 용량이 한 번도 없다) · D12(검출 한계가 "후기에 몰린다" 결론을
  만들었을 수 있다)**. **2·3호와 같은 형태다 — 결론을 떠받치는 문장이 자기 그림과 충돌.**
  그 밖: 전압창이 본문 `1.4–3.7 V vs In` ↔ ESI `2–3.7 V vs In` 로 다르고(D1, 그림이
  본문 편), 본문이 Fig. 1 (c)/(d) 를 바꿔 쓰고(D2), 급락 후 값을 "<20 mAh g⁻¹" 로
  적지만 `[도표]` 실제는 **≈2**(D3), 재구성 부피가 캡션의 "all 60×40×30 µm³" 와
  **하나도 안 맞고 pristine 이 0.62 배**(D4), 재가압 후 **재감쇠(80→≈64)를 언급하지
  않는다**(D17), 압력값이 **전부 ESI 에만** 있다(D16).
  그림: 크로핑 6 장 **전부 열람**. ⚠ ESI **Fig. S3** 은 캡션 줄바꿈(`Fi`/`gure S3.`)
  때문에 크로핑되지 않아 **보지 못했다** (Weka 분할 워크플로, 정확도 수치 없음).
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1·2·3·4 호가
  모두 인용; 4호가 `θ(N)` 3 점을 줬지만 **용량과 같은 셀에서** 주지 못했다),
  2 순위 **Koerver 2018** (`EES` 11, 2142 — ASSB 화학역학 종설 + **스택 압력 스윕**,
  Q6 을 스윕으로 채울 후보), 3 순위 **Neumann/Danner/Latz 2020** (`ACS AMI` 12, 9277 —
  **4호의 실측 기하를 2호 계보 전방 모형에 꽂는 다리**),
  4 순위 **Zhang/Scott/Ceder 2020** (`AEM` 1903778 — 같은 저자의 **LZO 코팅 불안정성**,
  4호가 정량하지 않고 남긴 화학 열화 몫).

- **2026-09-16 (ingest 5)** — `assb` 5호 논문 흡수:
  `raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md`
  (Doux, Nguyen, Tan, Banerjee, Wang, Wu, Jo, Yang, **Meng**, *Adv. Energy Mater.*
  **10** (2020) 1903253, doi `10.1002/aenm.201903253`, UCSD; 본문 6 쪽 + SI 8 쪽,
  **둘 다 sha256 봉인**). ✅ **업로드 파일명이 이번에는 내용과 맞다** (4호의 뒤바뀜 사고
  재발 없음 — 쪽수·첫 줄로 확인).
  컴파일: **새 개념 페이지 1**([[assb-stack-pressure-operating-window]]) +
  [[assb-pressure-reapplication-separation-test]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  이 논문은 **음극 축**이고 그 페이지는 이미 **320 줄**로 SCHEMA 200 줄 권고를 넘겼다
  (분할 제안은 사용자 판단 대기).
  ★★ **이 편의 일**: 4호가 **점**으로 준 압력을 **곡선**으로 바꿨다 —
  **P→임피던스 6 점 · P→단락시간 6 점 · P→과전압 5 점**, 그리고 압력을
  **로드셀로 실계측한 첫 편**(0–220 MPa, Instron 교정).
  Q1~Q8 채움표에 행 추가 (**5편 누적 ≈6.5/8**). **남은 0: Q4(유일성) 하나뿐.**
  최대 수확 넷:
  ① ★★★ **상한이 숫자로 들어왔다** — `[인쇄]` **75 MPa 는 도금 전에 이미 기계적으로
  단락**하고 25 MPa 는 48 h. **4호의 300 MPa 재가압은 이 상한의 4 배**다.
  ⚠ 모집단 차이(4호 In 음극 ↔ 5호 Li 금속) → **상한은 음극 재료의 함수**.
  ② ★★ **회복의 전극 귀속이 갈렸다** — 5호 Fig. 4c 셀은 **양극이 없는 대칭셀**인데
  압력이 임피던스를 **>15 배** 움직인다. 4호의 `R_LF` 65 % vs `R_MF` 23 % 와 같은 방향
  → **`ΔQ_mech` 를 양극 `θ_AM` 회복으로 읽으면 과대.**
  ③ ★★ **이력** — 처녀 5 MPa 110 Ω ↔ 25 MPa 경유 후 5 MPa ≈50 Ω (`[재현]` 계면 과잉의
  **77 % 영구 제거**) → **`θ(P)` 는 함수가 아니라 경로 의존 상태다.**
  ④ ★ **Q7 이 절반 깨졌다** — SEI 는 XRD 로 **상(相) 검출**(Li₂S·LiCl·P₄·Li₃P₇),
  **dead Li 는 검출 수단이 없다**(`[인쇄]` Li 금속은 XRD 로 안 보이고 토모는 밀도
  대비뿐). 그리고 Table S2 가 **이 계보 첫 반복 측정**(펠릿 4 개 상대밀도)이다.
  어긋남 원장 **20 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · **5호 20**), 무거운 묶음은
  **D1–D6**: `[인쇄]` "과전압이 전 과정 일정했다 → 계면이 안정하다" 가 **자기 SI
  Fig. S4 다섯 패널 전부에서 8–28 % 증가**로 반증되고(D1), 본문이 **Fig. S5 를
  "1000 h" 의 근거로 인용하는데 Fig. S5 는 92 h 다**(D2), **Fig. S2·S3·S4 를 본문이
  한 번도 인용하지 않으며**(D3) 그중 **Fig. S3 은 Methods 에도 없는 2 MPa 조건**이라
  결론의 "optimal 5 MPa" 에 **하한 탐색이 없다**(D4), **Fig. S2 는 단락 28 h 전에
  임피던스가 −16 % 떨어지는 전조**인데 해석되지 않고(D5), **"덴드라이트" 동정에
  독립 근거가 없다**(D6 — `[인쇄]` Li 는 XRD 로 안 보이고, 같은 저밀도 대비를
  Fig. S6 에서는 "severe cracking" 이라 부른다).
  → **2·3·4 호와 같은 형태이되 새 변종이다: 인용조차 되지 않은 SI 가 본문을 반증한다.**
  그림: 크로핑 13 장(그림 11 + 표 2) 중 **그림 11 장 전부 열람**, 표 2 장은
  도구 권고대로 PDF 텍스트로 읽었다.
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–4 호가 모두
  인용, 접촉 손실의 실험 원전 + 용량축 + 사이클),
  2 순위 **inbox 의 15번** (*Elucidating the Influence of Stack Pressure on Anode and
  Cathode Impedance of All-Solid-State Batteries via Three-Electrode Measurements* —
  ★ **이 ingest 가 남긴 정확히 그 공백**(전극 분해 + 압력)을 겨냥한다),
  3 순위 **inbox 의 24번** (*Tailored Cathode Composite Microstructure Enables Long
  Cycle Life at **Low Pressure*** — 압력 창의 아래 벽),
  4 순위 **Kasemchainan 2019** (`Nat. Mater.` 18, 1105 — 탈리 void·임계전류밀도,
  5호가 "우리는 void 가 없다" 고 반박한 상대 논문).

- **2026-09-16 (ingest 6)** — `assb` 6호 논문 흡수:
  `raw/papers/lee2020_ag-c-anode-free-assb.md`
  (Lee, Fujiki, Jung, Suzuki, Yashiro, Omoda, Ko, Shiratsuchi, Sugimoto, Ryu, Ku,
  Watanabe, Park, **Aihara**, **Im**, Han, *Nature Energy* **5** (2020) 299–308,
  doi `10.1038/s41560-020-0575-z`, **SAIT + Samsung R&D Japan**; 본문 10 쪽 + SI 18 쪽,
  **둘 다 sha256 봉인**). ✅ **업로드 파일명이 내용과 맞다** (4호의 뒤바뀜 재발 없음 —
  쪽수와 첫 쪽 텍스트로 확인; SI 1 쪽에 `SUPPLEMENTARY INFORMATION / … unedited.`).
  컴파일: **새 개념 페이지 1**([[anode-free-li-inventory-accounting]]) +
  [[assb-stack-pressure-operating-window]] · [[assb-apparent-capacity-decomposition]] ·
  [[assb-pressure-reapplication-separation-test]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  지시이기도 하고(이미 320 줄), 내용상으로도 이 논문은 **양극 `θ` 에 대해 아무것도
  주지 않는다**(Q1 = 없다).
  ★★ **이 편이 계보에서 처음인 것 셋**: **무음극(anode-free)** · **산업체 논문**
  (저자 16 명 전원 삼성) · **Ah 급 파우치 셀**.
  Q1~Q8 채움표에 행 추가 (**6편 누적 ≈7.0/8**). **남은 0: Q1(양극 접촉 손실 정량) ·
  Q4(유일성).**
  최대 수확 넷:
  ① ★★★ **`LLI` 추정자의 분해능이 새 전선이 됐다** — 같은 논문 안에서 **20 mAh 셀은
  CE(99.97 %)와 유지율(92.5 %@300)이 맞고 0.6 Ah 셀은 10 배 어긋난다**
  (`[도표]` CE 99.89 % ⇒ 누적 결손 `[재현]` **161 mAh g⁻¹** ↔ 실측 손실 **16**,
  양극 재고 **215**). **CE 축의 눈금조차 다르다**(95–101 vs 99.4–100.0).
  논문은 두 셀을 **한 번도 비교하지 않는다.**
  ② ★★★ **압력이 두 축으로 갈렸다** — **제작 490 MPa 등방(WIP, 비가역: Table S2 에서
  7 일 무압 복원 +0.8 µm)** vs **운전 2 MPa**. `[도표]` **무압 0.1 C 가 2 MPa 와 구별
  안 된다** → 5호의 "압력이 계면을 만든다" 와 모순이 아니라 **제작 압력 이력이 다르다.**
  ⚠ 운전 상한 `[인쇄]` **">4 MPa 단락 확률 증가" 는 데이터 0**.
  ③ ★★ **Q7 에 채널 둘 추가, 정량 0** — **EELS Li 맵**(방전 후·100 사이클 후에도
  Li 망 잔존)과 **XRD 의 Li₉Ag₄**(Li 저장 상 동정, 가역). **dead Li 만 여전히 수단
  없음**이고, `[인쇄]` "isolated lithium" 을 기구로 지목하고 **안 잰다.**
  ④ ★★ **"무음극은 OCP 평탄" 이 앞 10–17 % 구간에서 거짓** (Fig. 4a + SI Fig. 4c:
  음극 전위가 ≈1 → 0 V) → ASSB 인수인계 노트 §1 의 3 파라미터 창 모형은
  **3.6 V 위에서만** 성립한다.
  어긋남 원장 **14 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · **6호 14**).
  ⚠ **2–5 호보다 적고 가볍다** — *Nature Energy* 의 편집 품질이 보이고, 5호의 변종
  (**인용조차 안 된 SI 가 본문을 반증**)은 **여기 없다**(모든 SI 그림이 본문에서
  인용된다). 무거운 것은 넷: **D2**(CE ↔ 유지율 10 배, 위 ①) · **D1**(초록·라벨
  ">99.8 % CE" ↔ `[도표]` **900–1000 사이클 구간 중앙값 99.21 % · 최저 97.42 %**,
  언급 0) · **D3**(">4 MPa 단락" 에 데이터 0) · **D6**(`[인쇄]` "no residual Li
  deposits … were found" ↔ `[도표]` Fig. 5i·5l 의 **EELS Li 망 잔존**).
  그 밖: 운전 압력이 세 곳에서 2–4 / 2 / 2 MPa(D4), C 단독 율특성이 SI 안에서
  75 % ↔ ≈92 %(D5), C 의 전기화학 활성에 대한 두 문장 충돌(D5-b), 에너지밀도 두께
  예산 594 µm ↔ 실측 609.0 µm 이고 **Ag–C 층이 표에 없다**(D7), 도금 Li 두께–전하량
  수지가 **110/82/76 % 로 비단조**(D10), 초록의 ">900 Wh l⁻¹" 와 "1,000 cycles" 가
  **다른 셀**(D13).
  그림: 크로핑 **26 장**(본문 5 + SI 18 + 표 3) 중 **그림 12 장 열람**, 표 3 장은
  도구 권고대로 PDF 텍스트로 읽었다. ⚠ **Fig. 6 은 크로퍼가 "영역 없음" 으로
  제외**해서 `pymupdf` 로 8 쪽을 직접 렌더해 봤고, **Fig. S10(WIP 전후 SEM)은
  크로퍼가 "그래픽 없음" 으로 제외했고 열지 않았다** — 그래서 Q1 판정은 Table S2
  수치와 본문 서술에만 근거한다.
  ★ Fig. 6g 와 SI Fig. 16 은 **PDF 텍스트층의 축 눈금 좌표로 축을 교정한 뒤** 화소를
  읽었고, 교정을 **논문 인쇄값(600 사이클 95 % · 1000 사이클 89 %)으로 검증**했다.
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–5 호가 모두
  인용하고 **6호도 ref 38 로 인용**한다; Q1 의 실험 원전이고 **여섯 편이 모두 안 준
  것**이 이것 하나다), 2 순위 **inbox 의 15번** (*… Stack Pressure on Anode and
  Cathode Impedance … via Three-Electrode Measurements* — 6호가 남긴 **전극 귀속**
  공백 정조준), 3 순위 **Genovese/Louli/Weber/Hames/Dahn 2018** (`JES` 165, A3321 —
  6호 ref 23, ***무음극 셀의 CE 측정법 그 자체***; 위 ① 의 분해능 문제를 직격한다),
  4 순위 **Zhang et al. 2017** (`JMCA` 5, 9929 — 6호 ref 46, **운전 중 압력 변화
  실측**; G12(정압인가 정변위인가)의 답이 여기 있을 수 있다).

- **2026-09-16 (ingest 7)** — `assb` 7호 논문 흡수:
  `raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`
  (Spencer-Jolly, Agarwal, Doerrer, Hu, Zhang, Melvin, Gao, Gao, Adamson, Magdysyuk,
  Grant, House, **Bruce**, *Joule* **7** (2023) 503–514, doi
  `10.1016/j.joule.2023.02.001`, **University of Oxford + Diamond Light Source**;
  본문 13 쪽 + SI 6 쪽, **둘 다 sha256 봉인**).
  ✅ 업로드 파일명이 내용과 맞다 (쪽수·1 쪽 텍스트로 확인). ⚠ 같은 업로드의
  `Sup1_` (2 쪽, *Standardized data reporting for batteries* **제출 양식**)은
  사용자 지시대로 **읽지 않았고 근거에 없다.**
  컴파일: **새 개념 페이지 1**([[ag-c-interlayer-lithium-phase-path]]) +
  [[anode-free-li-inventory-accounting]] · [[assb-apparent-capacity-decomposition]] ·
  [[assb-stack-pressure-operating-window]] · [[halfcell-ocp-shape-invariance]] 갱신.
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 건드리지 않았다** —
  지시이기도 하고(이미 339 줄), 내용상으로도 이 논문은 **양극에 아무것도 주지 않는다**.
  ★★ **이 편이 계보에서 처음인 것 셋**: **operando 회절**(실험실 + 싱크로트론) ·
  **6호의 외부 검증**(삼성 논문을 학계가 다시 잰 첫 편) · **원자료 공개**
  (Oxford Research Archive).
  Q1~Q8 채움표에 행 추가 (**7편 누적 ≈7.0/8 — 칸은 안 늘었다**).
  **남은 0: Q1(양극 접촉 손실 정량) · Q4(유일성).** Q6 은 6호 대비 **후퇴**.
  최대 수확 넷:
  ① ★★★ **dead Li 가 처음으로 숫자가 될 수 있게 됐다** — `[도표]` 충전 67.6 h ·
  방전 35.0 h (둘 다 30 µA cm⁻²) ⇒ `[재현]` **2.03 ↔ 1.05 mAh cm⁻², 효율 ≈52 %**,
  SEI 구간 0.19 를 빼면 **≈0.79 mAh cm⁻² = 통과 전하의 39 %** 가 설명되지 않는다.
  방전 종료 회절에 `[인쇄]` "only graphite and Ag" 만 남으므로 층 내부 Li 는 전부
  돌아왔다. ⚠ **논문은 이 뺄셈을 하지 않는다** (`Coulombic`·`efficiency`·`dead`·
  `isolated` **전수 0 회**). ⚠ **SEI ↔ dead Li 는 여전히 안 갈린다.**
  ② ★★★ **음극 OCP 가 충전과 방전에서 다른 곡선이다** — `[인쇄]` 충전에 없는 상
  (LiAg 의 **UPb 다형**)이 방전에 나타나고, 논문이 그것을 **열역학적 안정성**으로
  설명한다. 율은 ≈**C/68**·상온 → **`i→0` 으로 지울 수 없는 이력**이다.
  → [[halfcell-ocp-shape-invariance]] 의 두 번째 파괴 방식이고 **한 사이클 안**이다.
  ③ ★★ **6호의 "Ag 는 돌아오지 않는다" 에 대한 답** — `[도표]` Fig. 6 D→E→F 와
  SI Fig. S4: 충전에 **Ag 가 층 밖으로 나가 집전체 계면의 균일막**이 되고 방전에
  **다시 층 안 불연속 군집**으로 돌아온다(`[인쇄]` "near-pristine").
  **모순이 아니라 시간척도가 다르다** (7호 1 사이클 ↔ 6호 100 사이클).
  ⚠ **사이클당 잔류는 여전히 아무도 안 쟀다.**
  ④ ★★ **Ag 는 임계전류를 못 올린다** — `[인쇄]` 흑연 단독과 **같은 failure point**
  (둘 다 2.0 안정 / **2.5 mA cm⁻² 단락**). ⚠ **흑연 계의 판정**이고 6호는 카본블랙
  으로 3.2 mA cm⁻² × 1000 사이클이다 → **모집단 경계 넷**(탄소·상대극·사이클 수·
  제작 압력 방식)을 digest §15 에 표로 박아 두었다.
  어긋남 원장 **13 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · 6호 14 · **7호 13**).
  ★ **이 계보에서 가장 적다** — `[해석]` 1 사이클·반쪽전지라 주장 표면적이 작고,
  **초록이 자기 결과보다 세게 말하지 않는다**(2–5 호의 지배 패턴이 없다).
  무거운 넷: **D2**(`[인쇄]` Ag 합금 예산 **0.60 mAh cm⁻²** ↔ `[재현]` 자기 조성으로
  **0.25**, ≈2.4 배) · **D3**(**첫 사이클 효율을 한 번도 안 적는다**) ·
  **D4**(**비가역분 39 % 의 행방을 계산하지 않으면서** 결론에서는 "Li 가 남는다" 고
  적는다) · **D8**(Fig. 6(0.1 mA cm⁻²·60 °C)의 Ag 를 **Fig. 1(30 µA cm⁻²·상온)** 의
  상으로 귀속 — 같은 논문이 "율이 오르면 Li–Ag 반응이 뒤처진다" 를 보였는데도;
  게다가 **Fig. 6 의 조건이 Methods 두 범주 어디에도 없다**).
  그 밖: Fig. 3(방전) 캡션이 "**charging** profile"(D1), Fig. 1 의 **Li 막대 시작
  시점에 근거 없음**(D5), SI Fig. S2a 의 **Li 피크가 잡음 대비 2–3 배**(D6),
  **집전체가 실험마다 Cu ↔ SUS**(D9), `[인쇄]` "Fig. S1 에 Ag 합금 전압 특징 없음"
  ↔ `[도표]` **어깨가 있다**(D10), 캡션 "≈0 V 로 급락" ↔ `[도표]` **−0.5 ~ −0.9 V
  톱니**(D11).
  그림: 크로핑 **11 장 전부 열람** (본문 6 + SI 5). ✅ **6호에서 있었던 "크로퍼가
  핵심 그림 제외" 사고 없음** — 제외된 그림 0 장.
  ★ Fig. 1·3 의 **상 막대와 시간축**, Fig. 4 의 **전압축**은 400 dpi 재렌더 +
  **화소 좌표 판독**으로 읽었고, 시간축 교정을 **인쇄값(2 mA h cm⁻²)으로 검증**했다.
  ⚠ **Methods 는 260 dpi 로 직접 렌더해 읽었다** — 본문 PDF 폰트가 **µ 를 전부
  떨어뜨려**(`30 µA cm⁻²`→`30 mA cm⁻²`, `5 µm`→`5 mm`) 텍스트 추출값을 쓰면
  **단위를 세 자리 틀린다.**
  후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 1–6 호가 모두
  인용; Q1 의 실험 원전이고 **일곱 편이 모두 안 준 것**이 이것 하나다),
  2 순위 **Gao/…/Bruce 2022** (`Joule` 6, 636 — **7호 ref 44, 같은 그룹의 "저압에서
  작동하는 복합양극"**; 7호가 `[인쇄]` 스스로 "양극은 다루지 않았다" 고 가리킨 곳이고
  **Q1 과 Q6 을 동시에 칠 수 있다**),
  3 순위 **inbox 의 15번** (3전극 + 압력 — 6호·7호가 남긴 **전극 귀속** 공백),
  4 순위 **Kasemchainan 2019** (`Nat. Mater.` 18, 1105 — 7호 ref 49, **상대극 void
  형성**; 7호가 "5 mm Li 상대극으로 그 기여를 줄였다" 고 적은 근거의 원전이고,
  §7 전하 수지의 **상대극 쪽 오차원**이 거기 있다).

- **2026-09-22 (ingest 8)** — `assb` 8호 자료 흡수:
  `raw/papers/li2026_safety-aware-bms-active-intelligence.md`
  (Li F, Li Y, Wu W, Qiao H, Jiang L, *Frontiers in Chemistry* **14** (2026) 1960882,
  doi `10.3389/fchem.2026.1960882`, **TYPE: Mini Review**, Shandong Huayu University of
  Technology; 본문 **12 쪽**, SI 없음, **sha256 봉인**
  `a54b551671eea230…`). ✅ 업로드 파일이 지정과 일치 (쪽수·sha256·DOI 확인).
  ★★ **큐에서 처음으로 성격이 다른 자료다** — 1–7 호는 ASSB 미세구조·계면·전극
  논문(시뮬레이션 3 + 실험 4)이었고, 8호는 **BMS·진단 종설**이며 **ASSB 는 12 쪽 중
  한 문단(§6.1)** 에만 나온다.
  ⚠⚠ **Mini Review 다 — 1 차 측정이 0 이고 모든 수치가 재인용이다.**
  digest 머리와 채움표 행에 그 사실을 박아 두었다.
  컴파일: **새 개념 페이지 없음** (SCHEMA Page Thresholds — 1 차 근거가 없어 개념
  페이지를 세울 재료가 안 된다). 대신 **이 카드에 채움표 행 + Evidence 1 절 +
  새 제약 1 절**, 그리고 [[assb-stack-pressure-operating-window]] 에 산업 요구치
  한 줄. ⚠ [[composite-cathode-percolation-utilization]] 은 **건드리지 않았다**
  (339 줄, 분할 대기 — 지시이기도 하고 내용상으로도 8호는 `θ` 에 아무것도 안 준다).
  Q1~Q8 채움표에 행 추가 (**8편 누적 ≈7.0/8 — 칸은 안 늘었다**).
  **남은 0: Q1(양극 접촉 손실 정량) · Q4(유일성).**
  최대 수확 넷:
  ① ★★★ **이 카드의 질문이 BMS 요구 사항으로 인쇄됐다** — `[인쇄]` §6.1
  "diagnostics capable of **distinguishing contact loss from ordinary electrochemical
  aging**". 3호가 **축퇴의 존재**를 인쇄로 확인했다면 8호는 **그것을 가르는 진단의
  필요**를 인쇄로 요구한다. ⚠ 정량 0, 그 요구가 매단 인용 1 편도 종설.
  ② ★★ **Q4 의 성질이 바뀌었다** — `identifiab*` **5 회**(1–7 호는 전부 0 회)이고
  **Table 4 의 중기 실패 모드에 "Unidentifiable pulse response"** 가 항목으로 있다.
  `[인쇄]` §2 "Parameter identifiability … can make a detailed model **appear more
  precise than the available measurements justify**" 는 우리 논지 그대로다.
  ⚠⚠ **그래도 측정은 0** — 조건수·프로파일 가능도·근최적 폭·CRB 전부 없다.
  **Q4 는 8/8 편 0.**
  ③ ★★ **세 번째 "비어 있음" 원장** — `[재현]` Table 2 8 편에서 **보정된 불확실성
  0 / 8**, `Cell` 검증 **7 / 8**. 액체셀 17/17(유일성 0) · `assb` 7/7(오차막대 0) 과
  **같은 방향**이다. ⚠ 리뷰의 분류를 우리가 센 것이고 원전 대조는 0 이다.
  ④ ★★ **압력 창의 아래 벽** — `[인쇄]` "industrial requirements **below approximately
  1 MPa**"(Xu 2024 재인용). `[재현]` `MPa` 가 12 쪽에 **1 회**이고 그 값이 1 이다 —
  **우리가 읽어 온 실험실 창(2–490 MPa) 전체가 그 위에 있다.**
  ★ **그리고 우리 폭 측정기의 소비처가 그려져 있다** — `[도표]` Fig. 2 의
  `I_cmd = min(…, **I_uncertainty**)` 인데 **계산법이 논문에 없다**(G1) →
  [[near-optimal-set-width-measurement]] 가 들어갈 빈칸.
  어긋남 원장 **10 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · 6호 14 · 7호 13 ·
  **8호 10**). ★ **형태가 다르다** — 자기 실험이 0 이므로 "결론이 자기 그림과 충돌"
  대신 **인용 어긋남**이 주종이다. 무거운 넷:
  **D1**(★★★ `[인쇄]` "SOH RMSE **≤0.873 %** in Su et al. (2024)" ↔ **우리가 가진
  원전**은 5 셀 **평균**이고 cell5 **1.607 %**, 게다가 같은 논문의 원시 EIS 0.573 %·
  8-D 0.672 % 가 **제안 feature 를 모든 지표에서 이긴다** — **리뷰가 과장을 `≤` 로
  굳혔다**) · **D2**(`poorly identifiable` 문장이 매단 인용이 **Si–C 음극 소재 종설**,
  *Front. Mech. Eng.* 12, 1860708 — 자매지 자기인용) ·
  **D3**(`[도표]` Fig. 2 가 "**lexicographic**" 이라 적고 **`min()`** 을 계산한다 —
  min 은 순서 불변이라 §4 의 5 단계 우선순위가 결과에 영향이 없다; **이 논문의 중심
  구조 주장이 자기 그림에 구현돼 있지 않다**) ·
  **D4**(`[인쇄]` §6.2 "safety supervisor **in Figure 1**" ↔ `[도표]` **Figure 1 에
  그 상자가 없다**; 초록의 "**layered** vehicle–edge–cloud" 도 그림엔 층이 없고
  **여섯 상자가 전부 대칭 양방향 화살표**다 — 본문이 반대한 바로 그 구조).
  그 밖: 심사 응답 문장이 게재본에 남아 있고(D5 — "the **reviewers' request**",
  "the **reviewer's example**", "**The uploaded** 2023 review"; `[인쇄]` Generative AI
  statement 로 **Figure 1 은 생성형 AI 제작**, 접수→게재 **39 일**),
  PyBaMM 인용의 학술지·권·쪽이 DOI 와 다른 출판물을 가리키고(D6, DOI 접두로 판단),
  `Liu et al. (2025)` 가 두 편인데 a/b 구분이 없으며(D7),
  **Birkl 2017 이 EIS/DRT 표에 붙어 있고 이 리뷰는 열화 모드를 한 번도 쓰지 않는다**
  (D8 — `LLI`·`LAM`·`degradation mode` 전수 0 회),
  Table 2 의 `Computational burden` 이 기준 없는 형용사이며(D9),
  자기 권고(팩 검증·보정 불확실성)를 만족하는 증거가 표 안에 **1 행 / 0 행**이다(D10).
  그림: 크로핑 **6 장**(fig 2 + tab 4) 중 **fig 2 장 전부 열람**, 표 4 장은 도구
  권고대로 PDF 텍스트로 읽었다 (Table 3 은 fig_2 크롭에 함께 들어와 **이미지로도
  이중 확인**). ✅ **크로퍼 누락 0** — `pymupdf` 로 센 PDF 내장 이미지 **2 개**와 일치.
  ✅ **µ 탈락 위험 없음** — 이 PDF 에는 `µ` 가 필요한 수치가 하나도 없고,
  `−20 °C to 60 °C`·`>120 titration points` 는 fig_2 크롭에서 눈으로 재확인했다.
  ★★★ **이 편의 실익은 수치가 아니라 원 논문 지도다** (digest §15). 후속 후보:
  1 순위 **Xu, Yang, Li 2024** (*Adv. Energy Mater.* **14**, 2303539, doi
  `10.1002/aenm.202303539` — `<1 MPa` 의 출처, **Q6**; ⚠ 그것도 종설),
  2 순위 **Zhang, Fu, Lu, Hu, Xia, Zhang et al. 2025** (*Adv. Mater.* **37**, 2413499,
  doi `10.1002/adma.202413499` — 저압 ASSB 전용, **Q6·Q1**; inbox **24번**과 짝),
  3 순위 **Biçer, Aksöz, Bakar, Odabaşı, Oyucu, Soares et al. 2025** (*Batteries*
  **11**, 212, doi `10.3390/batteries11060212` — "접촉 손실 ↔ 보통 노화 분리 진단"
  요구가 매단 **유일한** 인용, **Q1·Q2**),
  4 순위 **Liang, Tao, Shi, Lyu, Ji, Dong et al. 2026** (*npj Clean Energy* **2**, 16,
  doi `10.1038/s44406-026-00040-w` — **active pulse 원전**, 우리 폭 측정기의 역방향:
  "원하는 폭을 얻으려면 최소 어떤 여기가 필요한가", **Q4 설계 축**),
  5 순위 **LeBel, Messier, Sari, Trovão 2022** (*J. Energy Storage* **54**, 105303,
  doi `10.1016/j.est.2022.105303` — GITT OCV/동적 응답면 원전, `>120 titration
  points` × −20~60 °C, **Q3·Q8**),
  6 순위 **Roman, Saxena, Robu, Pecht, Flynn 2021** (*Nat. Mach. Intell.* **3**, 447,
  doi `10.1038/s42256-021-00312-3` — Table 2 **8 행 중 유일하게 신뢰구간을 보고**,
  **Q3**),
  7 순위 **Thelen, Huan, Paulson, Onori, Hu, Hu 2024** (*npj Mater. Sustain.* **2**, 14,
  doi `10.1038/s44296-024-00011-1` — 불확실성 **보정** 종설, **Q3·Q4**).
  ⚠ **1–3 순위가 전부 종설이다** — §6.1 은 **종설이 종설 셋을 인용한 문단**이고
  그 아래에 1 차 측정이 없다. **Q1 의 1 차 원전은 여전히 `assb` 1–7 호 쪽에 있고,
  닻의 오랜 1 순위 Koerver 2017 은 이 리뷰가 인용조차 하지 않는다**
  (참고문헌 48 편에 `Koerver` **0 회**).

- **2026-09-22 (ingest 9)** — `assb` 9호 논문 흡수:
  `raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md`
  (Huo, Li, Fan, Zhang 외, *J. Power Sources* **627** (2025) 235830; 본문 11쪽 +
  **SI(.docx)**, sha256 봉인). 컴파일: **새 개념 페이지**
  [[assb-lampe-contact-product-degeneracy]].
  **Q1~Q8: 8편 ≈7.0 → 9편 누적 ≈7.5 칸.** 늘어난 것은 **Q6**(압력이 "점·스윕" 에서
  **연속 시계열**로) 반 칸과 **Q3 의 새 층위**(`fitted-single-parameter`)다.
  **Q1·Q4 의 0 은 9호도 못 채웠다** — 그러나 **Q4 의 성질이 세 번째로 바뀌었다**:
  안 쟀다(1–7호) → 이름이 로드맵의 실패 모드에 올랐다(8호) → **지문이 자기 표 안에
  있고 다르게 불린다(9호)**.
  ★★★ **이 편이 큐에서 우리 문제와 가장 가깝다.** 이 계보 최초로 **실험과 파라미터
  식별을 한 논문 안에서 잇고**, 그래서 처음으로 **열화 모드의 지분 자체를 적합으로
  정한다**. 그 절차를 다섯 축으로 캐물은 답: ① 식별 절차 = **1-파라미터 PSO**(`ε_p`
  하나), 정답축이 자기 방전곡선 ② 유일성 증거 **0** (`uncertaint*`·`identifiab*`·
  `sensitiv*`·`Fisher`·`condition number`·`bootstrap`·`multi-start`·`error bar`·
  `regulariz*` 전수 0회) ③ **여러 모드를 같이 놓고 지분을 비교한 적이 없다** —
  `LLI`·`LAM_NE` 는 모델에 **좌표가 없고** `ε_p` 하나만 푸므로 **잔차가 갈 곳이 하나**
  다 ④ fitting 밖의 독립 관측 **0건**(SEM 은 표면·정성, EIS 는 같은 역문제) ⑤ SOH
  "1 % 이내" 는 **훈련 잔차**이고 예측 오차가 아니다 — 대조군 **0건**, 08호의 Su 2024
  패턴과는 다르다(숫자는 정직하고 **설계**가 문제다).
  ★★ **가장 단단한 결과 둘**: (a) `A^p_eff · ε_p / R_s` **곱 축퇴를 인쇄된 식에서 손으로
  유도**했고 자기 SEM 이 `A_eff` 를 **9 배** 배반한다 (b) `[인쇄]` **"파라미터가 흔들려도
  적합이 잘 되니 괜찮다" 가 문자로 인쇄되어 있고**, 같은 논문이 그 명제의 **반례 셋**을
  자기 지면에 남긴다 (`R_SEI` **+37 %/−80 %** · 곱 축퇴 · `k_LAM` **2.15 배 vs 1 %**).
  어긋남 **9건**(D1~D9) + 공백 12건. 크로퍼가 **Fig. A.1(부록 DVA)을 빠뜨려** 수동으로
  뽑았다 (06호식 누락의 재발 — `fig_a1_manual.png`).
  후속 후보 1 순위 = 원전 **ref [27]**(같은 연구실 *eTransportation* 20, 100315 —
  모델·PSO·`A_eff` 정의를 전부 위임한 곳), 2 순위 = **ref [30] Conforto 2021**
  (9호 스스로 "정량한 몇 안 되는 문헌" 으로 지목하고 `[인쇄]` "오차가 비교적 크다" 로
  기각한다 — **그 오차의 크기를 우리가 직접 봐야 한다**, 방법이 **relaxed OCP + EIS-PSD**
  라 우리 축과 직결), 3 순위 = **ref [21] Yu 2024 DRT**(§5.1 의 병합 원호를 가르는 도구).

- **2026-09-22 (ingest 10)** — `assb` 10호 논문 흡수:
  `raw/papers/vadhva2021_eis-for-assb-theory-methods.md`
  (Vadhva, Hu, Johnson [3인 공동 1저자], Stocker, Braglia, Brett, **Rettie**(교신),
  *ChemElectroChem* **2021**, *8*, 1930–1947, doi `10.1002/celc.202100108`,
  **Reviews**, CC-BY open access; 본문 **18 쪽**, **SI 없음**(업로드 큐에 `10._Sup_*`
  부재 + 본문에 supporting/supplementary 0 회), sha256 봉인).
  소속: **UCL Electrochemical Innovation Lab** + **The Faraday Institution** +
  **HORIBA MIRA Ltd.**(기업 — Stocker·Braglia, 확인 완료).
  자금 **Faraday Institution LiSTAR** + **HORIBA-MIRA/UCL/EPSRC CASE studentship**.
  컴파일: **새 개념 페이지 없음** (이 논문의 명제는 기존 두 페이지의 같은 축이고,
  새로 만들면 "EIS 일반 설명" 으로 흐른다 — SCHEMA Page Thresholds). 대신
  [[assb-lampe-contact-product-degeneracy]] · [[fitting-degeneracy]] ·
  [[assb-stack-pressure-operating-window]] 보강.
  **Q1~Q8: 9편 ≈7.5 → 10편 누적 ≈8.0 칸.**
  ★★★ **`Q4` 의 0 이 처음으로 깨졌다 — 그리고 깬 방식이 중요하다.**
  **"우리 대신 쟀다" 가 아니다**(측정 0; `identifiab*`·`uncertaint*`·`confidence`·
  `condition number`·`error bar` **전수 0 회** — 10/10 편이 여전히 안 쟀다).
  **"축퇴가 일반 현상임을 방법론으로 인쇄했다"** 이다: `[인쇄]` "**no solution to an
  EIS spectrum is unique**" · "**the inclusion of more elements will tend to improve
  the fit**" · "how many time constants … **highly subjective**" · DRT 는
  **`ill-posed`, regularization 필요** · 모델 선택을 **AIC** 로 명명하고
  `[인쇄]` "**validation against experiment in the context of ASBs is desirable**"
  로 **열린 문제 등록**. ⇒ Q4 의 성질이 **네 번째로** 바뀌었다.
  ★★★ **9호 §5.1(하나의 원호에서 두 시상수)에 정식 근거를 준다** — 판정 5 문장 +
  처방 5 개(K–K/Lin-KK · DRT 로 개수 결정 · **저온·가압으로 시상수 벌리기** ·
  **대칭셀 쌍** · AIC). **9호는 그중 하나도 쓰지 않았다**(`Kramers`·`DRT`·
  `symmetric cell`·`AIC` 전수 0 회). `[재현]` 9호 회로의 자유 파라미터는 **9 개**
  (`R_b`1 + RQ3 + RQ3 + W2)이고 **원호는 1 개**다.
  ★★ **DRT 를 다룬다 — 그리고 비판적으로 다룬다**(`DRT` 13 회). 8호의 "ill-posed
  inversion needs regularization" 처방이 여기서 EIS 쪽 1차 진술로 확인되고,
  개선 경로 3 개(**일반화 DRT** Danzer / **Bayesian DRT** Huang / **2D DRT** Mertens)
  와 원전이 붙는다. ⚠ 자기 DRT 계산은 0(Fig. 6d 는 재인용).
  ★★ **새 명제 하나**: **"분해 가능한 RC 의 개수는 실험 조건의 함수다"** — 다섯 사례
  (황화물 5 중 3 만 입계 분해 · LGPS 실온 원호 0 개 · **400 MPa 에서 GB 등장** ·
  폴리머 60 °C 에서 상경계 소멸 · **노화가 RQ 를 3→4 로, 새 RQ 귀속은 `and/or`**).
  ★ **이 카드의 Q2 에 직격**: `[인쇄]` Fig. 9 본문이 **접촉 손실과 분해층 성장을
  한 `R_MF` 에 함께 귀속**한다 ⇒ **EIS 는 곱 축퇴를 깨는 대가로 새 축퇴를 들여온다.**
  어긋남 **6 건**(D1 위상각 식 역전 · D2 Eq.3 차원 불일치 · D3 "~10⁹ orders of
  magnitude" · D4 본문↔캡션 패널 글자 한 칸 어긋남 · D5 라운드로빈 인용 번호 오류
  [85]↔[191] · D6 저주파 인덕턴스에 두 이름) + 공백 8 건. **방법론적 주장 자체에는
  어긋남을 못 찾았다.**
  크로퍼: **15 장 = Fig. 1–14 + Table 1, 누락 0**(⚠ `fig_7.png`/`fig_8.png` 가 같은
  두 단 영역을 **중복** 크롭 — 누락은 아니다). **실제로 본 것 8 장**
  (Fig. 2·5·6·7·8·9·11·12) + 본문 4 곳 페이지 렌더(Eq. 3 · Eq. 5 · "10⁹" · `μAh`).
  ✅ **µ 탈락 없음** — 이 PDF 는 `μAh`·`μm` 를 정상 추출하고 렌더로 재확인했다.
  후속 후보 1 순위 = **ref [52] Ingdal, Johnsen, Harrington** *Electrochim. Acta*
  **2019**, *317*, 648–653 (**AIC 로 등가회로 순위 — Q4 의 계산기**),
  2 순위 = **ref [191] Ohno et al.** *ACS Energy Lett.* **2020** (라운드로빈 원전,
  **22 % / ~10 %** 의 출처 — D5 때문에 더더욱 필요, **Q3**),
  3 순위 = **ref [82] Bron, Dehnen, Roling** *J. Power Sources* **2016**, *329*, 530
  (저온으로 축퇴를 깨는 실물, **Q4·Q2**),
  4 순위 = **ref [97] Zhang, Weber, …, Zeier, Janek** *ACS AMI* **2017**, *9*, 17835
  (In\|LGPS\|LCO SoC 분해 EIS — **접촉 손실 + 분해층이 한 저항에 묶인 원전**,
  **Q1·Q2·Q5**; 4호의 `R_LF`/`R_MF` 해석을 검증할 유일한 편),
  5 순위 = **ref [28] Krauskopf et al.** *ACS AMI* **2019**, *11*, 14463 (**Q6**,
  압력 이력의 산화물 판),
  6 순위 = **ref [84] Doux et al.** *J. Mater. Chem. A* **2020**, *8*, 5049
  (우리 5호의 **자매 논문**, Li₆PS₅Cl σ 가 ~400 MPa 까지 증가, **Q6**),
  7 순위 = **ref [57] Kaiser et al.** *J. Power Sources* **2018**, *396*, 175
  (**TLM + 전자차단 대칭셀로 복합전극 이온 굴곡도 정량** — `θ_AM` 에 가장 가까운
  실측 채널, **Q1**),
  8 순위 = **ref [172] Huang, Papac, O'Hayre** *Electrochim. Acta* **2020**, *367*
  (**Bayesian DRT** — 봉우리에 사후분포를 붙이는 경로, 8호의 "calibrated
  uncertainty" 요구와 직결),
  9 순위 = **ref [73] Larfaillou et al.** *J. Power Sources* **2016**, *319*, 139
  (**노화가 RQ 를 3→4 로 바꾼다** — "모델 차수가 상태변수" 의 원전).
  도구 후보: **ref [43] Schönleber, Lin-KK**(KIT 2015).
  ⚠ **정정 하나**: ref [190] 의 **Bielefeld, Weber, Janek** *ACS AMI* **2020**, *12*,
  12821 은 우리 **1호(Bielefeld 2019, *J. Phys. Chem. C*)와 다른 논문**이다(후속).
- **2026-09-22 (ingest 11 — 큐 38번, 순서를 당겨서)** — `assb` 11호 흡수:
  `raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md`
  (Yu, Choi, Dunham, Ghahremani, Liu, Lindemann, Garver, Barchiesi, Farahati,
  Kim, *J. Power Sources* **597** (2024) 234116 — **Schaeffler Transmission
  Systems LLC**(산업체) + **Ohio State University**; 본문 8 쪽 + **SI `.docx`**
  7,607 자 + 그림 S1–S5, 본문·SI 둘 다 sha256 봉인).
  **10호(Vadhva) 와 짝으로 읽으려고 순서를 당겼다** — 10호가 DRT 를 `[인쇄]`
  "ill-posed … requiring regularization" 으로 판정하고 λ 선택 규칙을 공백(G4)으로
  남겼고, **11호가 그 DRT 를 실제로 돌린 첫 `assb` 논문**이기 때문이다.
  **그림 14 장 모두 등록 · 12 장 열람**(본문 Fig. 1–8 + SI Fig. S1–S5;
  Table 1 은 텍스트로). ★ **SI 가 `.docx` 라 크로퍼가 못 읽어 `zipfile` 로
  `word/media/image1–5.png` 를 직접 꺼냈다** — 텍스트만 긁었으면 §12(Fig. S2)·
  §13(Fig. S3)·§10(Fig. 1 = Fig. S3 동일 데이터)을 **통째로 놓쳤다.**
  **결과 여섯**:
  ① **`Q1` 이 반쯤 깨지고 `Q6` 의 마지막 빈칸(`압력 → 용량`)이 채워졌다**
     (누적 **≈8.5 / 8** 칸; 반쪽 3 점 165.0/166.9/**173.1**, 완전지 2 점 169.9/171.7).
  ② ★★★ **`Q4` 의 성질이 다섯 번째로 바뀌었다 — "잴 재료를 SI 에 인쇄하고
     뺄셈을 안 했다".** `[도표]` Fig. S3 가 **같은 셀에서 배선만 바꿔 DRT 봉우리를
     −15 % ~ +69 %** 움직이는데, 본문의 재가압 효과는 **−10 ~ −25 %** 로 그 폭
     **안**이다. **Q4 측정은 여전히 0 / 11.**
  ③ ★★★ **"모델 차수는 상태변수" 가 1 차 데이터로 네 번 확인됐다**
     (Fig. 2a 2–3→5 · Fig. 3c 1→2 · Fig. 6c P4 신생 · Fig. 7d 4→3 재가압).
     10호가 Larfaillou 재인용으로만 전한 것의 **직접 재현**.
  ④ ★★★ **`Q8` 이 이 카드의 출발 전제를 깼다** — **graphite 음극 완전지**라
     "전고체 음극은 평탄 → 5→3 붕괴" 가 성립하지 않는다 (9호 Li-Si 에 이은
     두 번째 반례, 이쪽은 상용 흑연).
  ⑤ ⚠ **압력 연산자가 직교하지 않는다** — 재가압이 P1·P2·P3·**P4(전하이동)** 를
     전부 10–27 % 줄인다 ⇒ [[assb-pressure-reapplication-separation-test]] 에
     반례 기록, `confidence: low` 유지.
  ⑥ **어긋남 18 건** (D1 전처리 이중 서술 · D2 P1 주파수 최대 2 자릿수 ·
     D3 "P3 만 줄었다" 가 그림에 없다 · D10 본문이 자기 Fig. 1 을 잘못 묘사 ·
     **D11 Fig. 1 은 "Illustration" 이 아니라 Fig. S3 하단의 실측** ·
     D13 DRT 봉우리가 측정 대역(0.1 Hz) 밖에 있다 …).
  컴파일: 새 개념 [[drt-peak-count-nonidentifiability]] +
  [[fitting-degeneracy]] Q4 계보 갱신 + [[assb-pressure-reapplication-separation-test]] 반례.
  후속 후보 1 순위 = **Wan, Saccoccio, Chen, Ciucci, DRTtools** (*Electrochim.
  Acta* 184 (2015) 483 — **λ 와 RBF shape factor 가 이 논문의 인터페이스**이고
  G1 을 닫는 유일한 경로), 2 순위 = **Hori, Kanno, …, Ivers-Tiffée** (*J. Power
  Sources* 556 (2023) 232450 — 같은 재료계 EIS–DRT, 봉우리 귀속의 외부 검증),
  3 순위 = **Danzer, generalized DRT** (*Batteries* 5 (2019) 53 — 10호가 지목하고
  11호가 **인용만 하고 안 쓴** 것), 4 순위 = **Illig 2012 + Schmidt 2011**
  (P3 = "solid-solid contact impedance" 귀속의 **원전**; 액체셀 LFP/Al 의
  주파수대를 황화물 복합양극에 이식한 것이 정당한지 확인해야 한다).
- **2026-09-22 (ingest 12)** — `assb` 12호 논문 흡수 (큐 11번 — 38·39 를 당겨 끝낸 뒤
  큐 순서로 복귀한 첫 편): `raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`
  (Sadegh Kouhestani, Yi, Qi, Liu, Wang, Gao, Yu, Liu, *Energies* **15** (2022) 6599,
  doi `10.3390/en15186599`, MDPI CC BY; 본문 26 쪽, **SI 없음**, sha256 봉인).
  ⚠ **Review — 1차 측정 0. 그림 7 장 전부 타 논문 재수록**(LIB 6 + Palacín 2009 모식도 1)
  이라 **이 논문에는 SSB 데이터 그림이 0 장**이다. **그림 7 장 전부 열어 봤다**(Table 1 은
  텍스트로 전사). **결과 다섯**:
  ① **Q1~Q8 어느 칸에도 새 칸을 더하지 않는다** (누적 **≈8.5 / 8 유지**). Q4 는 **0 / 12**.
  ② ★★★ **분리 물음이 정의에서 지워진 자리를 찍었다** — `[인쇄]` "The loss of active
     materials **mainly stems from** the electrical contact loss" ⇒ PHM 어휘에서
     `LAM ⊃ 접촉 손실`. 기구 목록은 **전부 액체셀**, Fig. 6 의 "Contact Loss" 는 **집전체**.
  ③ ★★ **Q4 계보의 출발점을 날짜로 고정** — `identifiab*` **0**(8호는 5), 가장 가까운
     어휘가 "difficult parameter identification"(실무 곤란)이고, **같은 논문이 모델 차수에
     대해 정반대 두 문장**을 인쇄한다(§3.1.2 "inevitable errors in each parameter" ↔
     §3.1.3 "the more parameters … the higher the accuracy").
  ④ ★★ **`A_eff` 형 접촉 파라미터의 계보 입구** — `[인쇄]` Tian & Qi 2017 / Shao 2022
     "a parameter to describe the contact area, which adjusts the current density in the
     1-D Newman model" = 9호 `A^p_eff` 와 같은 형태. ⚠ 두 저자에 같은 번호 [60] → `0.4–1
     MPa` 출처 미확정(D4).
  ⑤ **Table 1 ("PHM techniques for SSB") 28 슬롯을 한 줄씩 대조**: SSB 실측 열화 데이터로
     SOH/RUL **0 / 28** (납축전지 ECM · 전방십자인대 예후 · 1976 kNN 이 들어 있다).
     논문 자신의 결론 (1)(2)와 일치.
  **어긋남 21 건**(D1 "LiCoO₂ or LTO" · D4 중복 [60] · D5 Deng [79] 이중 용도 · D6 "Song
  [29]" = Tian 종설 · **D7 §3.3.1/3.3.2 제목 뒤바뀜** · **D8 Table 1** · D9 ECM 식별법
  인용 4 건 전부 무관 · **D13 모델 차수 두 명제 충돌** · **D20 Fig. 5 `SOH = {FOI}` 벡터 ↔
  식 (6) 스칼라** …). 공백 10 건(G1~G10). 접수→승인 **9 일**.
  컴파일: **새 개념 페이지 없음**(이 편의 명제는 전부 기존 페이지의 같은 축이고 1차 내용이
  0 — SCHEMA Page Thresholds). 대신 이 카드(채움표 12행 + Evidence 아홉 번째 절 + 새 제약
  4 개 + 이 항목 + "주장하지 않는 것" 1 항) · [[assb-lampe-contact-product-degeneracy]]
  (`A_eff` 계보 절) · [[drt-peak-count-nonidentifiability]] ("원호 1→2" 세 번째 인쇄) ·
  [[fitting-degeneracy]] (Q4 계보에 2022 년 표본).
  8호와의 대조: **공통 원전 0 건**이라 "같은 원전을 다르게 적었는가" 는 수행 불가; 대신
  **같은 명제 둘(라벨 부재 · ≈1 MPa)이 다른 원전에서 독립적으로** 나왔다.
  후속 후보 1 순위 = **Tian & Qi, *J. Electrochem. Soc.* 2017, 164, E3512** (`A_eff` 원전
  후보), 2 순위 = **Shao et al., *Energy* 2022, 239, 121929** (접촉 면적 손실 + 압력 —
  Q1·Q6 동시, `0.4–1 MPa` 의 진짜 출처), 3 순위 = **Kim, Lin, … Chung, *Electrochim. Acta*
  2019, 317, 663** (Table 1 유일의 SSB 상태추정 — 관측 가능성을 다뤘는지; ⚠ 10호 후속
  1 순위 Ingdal 2019 와 같은 권), 4 순위 = **Schmidt, Bitzer, Imre, Guzzella, *JPS* 2010,
  195, 7634** (용량 손실 ↔ 율 특성 저하의 모델 기반 구분 — 우리 3항 분해의 액체셀 원형).

- **2026-09-22 (ingest 13)** — `assb` 13호 논문 흡수 (큐 12번):
  `raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (Zheng, Xie, Zhang, Yang, Zhou, Zhu,
  *Energy* **345** (2026) 140229, doi `10.1016/j.energy.2026.140229`, Elsevier; 본문 10 쪽,
  **SI 없음**, sha256 봉인, PDF `496f3b4580a81b9b…` 실측 일치). 접수→승인 **51 일**.
  ⚠ **Perspective — 1차 측정 0, `[인쇄]` "No data was used", 그림 5 장 전부 모식도/레이더
  (데이터 그림 0 장).** **그림 5 장 전부 열어 봤다** (Table 1·2 는 텍스트 전사). 큐 등록 축은
  Q3·Q4 였으나 **실제 접점은 Q6·Q8** 로 판정. **결과 다섯**:
  ① **새 칸 0 (누적 ≈8.5 / 8 유지, Q4 0 / 13).** Q6·Q8 의 이미 채워진 칸에 **층**이 하나씩.
  ② ★★★ **접촉 손실이 SOH 정의에서 사라진 자리를 찍었다** — `[인쇄]` "distinguish between
     **true active material loss** and a reduction in 'useable capacity' caused by **rising
     impedance or increasing overpotentials**"(2 항) ↔ 같은 절 "dominant failure modes … the
     gradual **loss of interfacial contact**". 12호 `LAM ⊃ 접촉 손실`(흡수) · 13호 미배정(누락)
     · 우리 3 항 — **분류 셋이 전부 다르다.**
  ③ ★★ **운전 창이 OCV 채널을 설계상 닫는다** — `[인쇄]` "20–80 % SOC … impossible to obtain a
     full OCV curve" + LFP 평탄 + "voltage hysteresis arising from mechanical stresses"(인용 0).
     이 카드의 답에 **"완전 OCV 곡선 조건"** 을 붙이고 부분 창 폭을 별도로 낸다.
  ④ ★★ **Q6 — 요구치 세 번째 독립 인쇄 + 위 벽의 두 번째 형태**: `[인쇄]` `<5 MPa` ×2(1 차
     주장, 근거 [35]/[45], "5" 출처 미명시) · `[도표]` Fig. 2 클래스 창(Oxides ≥30 · Sulfides
     5–20 · Halides 2–10 · Polymers 0 · Composites 1–10 MPa — **본문에 없는 값**) · `[인쇄]`
     고정 고압 → creep/피로 미세균열(단락과 다른 시간 축) · `[인쇄]` 능동 응력 관리 정책
     (율↑→P↑, 휴지/노화→P↓) · 인과 `압력 감쇠 → 임피던스 ↑`.
  ⑤ ★ **Q4 성질 변화 — 이름 없이 역문제를 처방**: `[인쇄]` "inversely estimate the current
     state of interfacial contact and material properties", `identifiab*` 0. 8호와 같은 해.
  **어긋남 12 건**(D2 "45–55 %" ↔ 끝점 45.5/50 · **D3 Fig. 1 그리드 삼각 숫자 0 + EV CE
  99.98 % 는 10000 사이클에 13.5 %** · **D4 `<5 MPa` ↔ Fig. 2 권장 클래스 상단 10 MPa** ·
  **D5 Fig. 3 SSB BMS 온도 입력 없음 ↔ §4 열관리 필수** · D6 `j = 5 mA cm⁻²` ⇒ 로딩 ≈10 mAh
  cm⁻² 미기재 · D7 Table 2 열화 어휘 = 액체셀 · D8 Fig. 2 가 수명 축 제외 · D9/D10 인용 무관 ·
  D12 수명 목표 무인용). 공백 12 건(G1~G12). 자기 인용 6/56 — 권장 복합전해질의 유일한
  수치 예가 자기 논문 [29].
  컴파일: **새 개념 페이지 없음**(1 차 내용 0 · 명제 전부 기존 축 — SCHEMA Page Thresholds).
  이 카드(채움표 13행 + Evidence **열 번째** 절 + 새 제약 5 개 + 이 항목 + "주장하지 않는 것"
  1 항) · [[assb-stack-pressure-operating-window]] (요구치 계보 + 피로형 상한 + 제어 정책) ·
  [[assb-apparent-capacity-decomposition]] (2 항 이분법에서 `θ_AM` 이 빠진 자리) ·
  [[fitting-degeneracy]] (Q4 계보 2026 년 두 번째 표본 — 이름 없는 역추정 처방).
  12호와의 대조: **공통 원전 0 건**(12호의 Tian·Shao·Hu·Fathiannasab 가 13호에 없고 13호의
  Schmaltz·Albertus·Li Qianya·Gu·Pang 2021 이 12호에 없다). 10호와는 **같은 그룹(Offer/
  Marinescu)의 다른 논문**(Pang 2019 *PCCP* ↔ Pang 2021 *Mater. Today*) — 공통 원전 아님.
  ⇒ "같은 원전을 두 리뷰가 다르게 적었는가" 는 이 쌍에서도 수행 불가; 대신 **압력 요구치
  ≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴**한다는 것이 실측.
  후속 후보 1 순위 = **Li Qianya et al., *Nat. Energy* 2025, 10, 1064** ("The critical importance
  of stack pressure in batteries" — 13호 [23], Q6 요구 창 정본 후보) · 2 순위 = **Zhang et al.,
  *Nat. Commun.* 2025, 16, 1013** (무외압 Si ASSB — 압력 0 에서의 접촉 손실 시계열, Q1·Q6) ·
  3 순위 = **Li Menglin et al., *AFM* 2025, 35, 2415696** (`<5 MPa` 근거 후보) · 4 순위 =
  **Gu et al., *AEM* 2023, 13, 2203153** (응력 측정 종설 — 9호 힘 시계열의 측정법 계보).
  큐 13~37 과 겹침 검색 **0 건**.

- **2026-09-22 (ingest 14)** — `assb` 14호 논문 흡수 (큐 13번 — **"OCV 경쟁 접근"** 으로
  등록된 편): `raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` (Oh⁺, Kim⁺,
  Kim, An, Kwon, **Choi Jang Wook**, *Angew. Chem. Int. Ed.* **64** (2025) e202514910,
  doi `10.1002/anie.202514910`, **Batteries Hot Paper**, CC BY-NC-ND; 본문 9 쪽 + **SI .docx**
  (Experimental + Note S1 + Fig. S1–S16, 표 0), PDF `fa35a5cdd5d3fcec…` · SI
  `ce0b9a35c96ef99c…` 실측 일치). 접수→승인 **35 일**. 서울대 + **HMG-SNU JBRC(현대차)**.
  자기 인용 **21/74**. ⚠ 지면은 *Angew. Chem.* 독일어판 조판이지만 **본문 영어**.
  **실험 논문** (엔트로피메트리 3 셀 · volumetry 3+1 셀 · XRM 4 · SEM). 크로핑 본문 **6 장
  전부 봄**, SI 16 장 중 **11 장 봄**(S1·S2·S3·S4·S7·S8·S9·S12·S13·S14·S16; 안 본 것 S5·S6·
  S10·S11·S15 형태학 패널). 합자 잔존 0; ⚠ 대소문자 무시 집계에서 `SOH` 5 회는 전부 저자
  "**Soh**n" — 약어 재집계.
  **판정: "OCV 경쟁" 이 아니라 "OCV 의 관측 추가"** — `E(x)` 를 적합하지 않고 같은 상태함수의
  두 편미분 `−F(∂E/∂T)_P` · `F(∂E/∂P)_T` 를 잰다. 분리 주장은 mechanical ↔ chemical 이고
  `LAM_PE` ↔ 접촉 손실은 물음 자체가 없다. **결과 다섯**:
  ① **새 칸 0 (14편 누적 ≈8.5/8 유지, Q4 0/14).** 층 셋 — Q1 비파괴 대리량 `F(dE/dP)`
     42.7 → 34.7 µJ mol⁻¹ Pa⁻¹(−18 %) · Q6 계보 최초 `E(P)`(2 구간, **비선형 2 배**) · Q8
     OCV 축 열역학 도함수 ≈28 점 × 3 셀.
  ② ★★★ **void 2 배에 용량 불변**(86.0 ↔ 84.0 %, 역상관) — 접촉 손실이 문턱 아래에서
     `Q_apparent` 에 안 들어간다 = OCV 적합의 **무감** 형태. 4호의 반대쪽 끝.
  ③ ★★ **Q4 성질 일곱 번째** — 역문제 없음 → 조건수 정의 자리 없음, 귀속 유일성 미검토.
     `[재현]` ΔS SOC 축 적분 부호 반전(≈ −3.5 → +1.5)은 비균질만으로 안 나온다(sum rule, G8).
  ④ ★★ ΔS 는 `[인쇄]` "contact loss as well as interfacial resistance" 를 **한 신호로** 받는다
     고 스스로 정의 → 분리 후보 행은 **volumetry**(우리 `[해석]`, 실측 0).
  ⑤ ⚠ Li 금속 음극항을 "constant" 로 두지만 식 (10) 의 `V_m(Li)` 13 cm³ mol⁻¹ 은 **상수 ≠ 0**
     이고 `[재현]` 실측 2.2 mV 의 30 % 크기; 실측 `dE/dP` 는 격자 몰부피로 설명되지 않는
     **유효 컴플라이언스**.
  **어긋남 15 건**(D1 Fig. 3a 이탈 ≈2–4 mV ↔ ΔS 함의 0.47 mV · **D2 Fig. 3c "after" 가 S2 세
  셀 어느 것과도 다름** · **D4 신품 volumetry 42.5 ↔ 22.2 = 압력 구간 2 배** · D6 Fig. 6 등급
  규칙 ↔ 본문 · **D7 전·후 volumetry OCV 171 mV 차** · D11 화학 단독 대조군 0 · D12 "similar"
  로 덮인 역상관 · D13 음극 상수항). 공백 14 건(G1 등급 문턱 0 · G3 `dE` 판독 규칙 0 · G7
  SOC 축 0 · G8 sum rule · G11 >300 MPa 미수행 · G12 (ΔS, ¬ΔV) 칸 없음).
  컴파일: **새 개념 페이지 1** [[assb-maxwell-ocv-derivative-channels]] (관측 축이 새롭고
  이 카드·CRB 페이지·압력 페이지 셋에서 반복 참조된다 — SCHEMA Page Thresholds 충족).
  이 카드(채움표 14행 + Evidence **열한 번째** 절 + 새 제약 5 개 + 이 항목 + "주장하지 않는
  것" 1 항) · [[assb-pressure-reapplication-separation-test]] (소신호 판) ·
  [[assb-stack-pressure-operating-window]] (`E(P)` 첫 데이터 + 20 MPa Li 금속 ≈225 h) ·
  [[assb-apparent-capacity-decomposition]] (void ≠ `Q_apparent` 실측) ·
  [[constrained-crb-identifiability]] (관측 추가의 첫 ASSB 표본) · [[fitting-degeneracy]]
  (Q4 계보 2025 표본 — 역문제 없는 형태) · [[halfcell-ocp-shape-invariance]] (두 번째 상태함수
  검사). `index.md` +1.
  13호와의 대조: **공통 원전 1 건** — **Oh *AEM* 2025**(13호 [34] = 14호 [10], 14호 저자의
  **자기 논문**) ⇒ 13호 후속 4 순위가 14호 저자 자신의 저압 실셀이므로 **1 순위로 승격**.
  우리 계보와의 인용: 5호 Doux 2020 = 14호 [35] · 4호 Shi 2020 미인용 · 1호 Bielefeld 2019
  대신 Bielefeld 2022 = [69].
  후속 후보 1 순위 = **Oh et al., *AEM* 2025, 15, 2404817**(ref [10], 저압 실셀 — Q6) · 2 순위 =
  **Bielefeld et al., *JES* 2022, 169, 020539**(ref [69], pore 문턱 → 저항 급증 = 1호 `p_c` 의
  실험판 — Q1) · 3 순위 = **Kim … Choi, *PNAS* 2022, 119, e2211436119**(ref [56], 엔트로피메트리
  원전 — SOC 축·sum rule) · 4 순위 = **Kim … Yazami, Choi, *EES* 2020, 13, 286**(ref [57]) ·
  5 순위 = **LePage 2019 *JES* 166, A89**(ref [70], "10 MPa Li creep") · 6 순위 = Lewis 2021
  *Nat. Mater.* / Lu 2022 *Sci. Adv.*(refs [73][74], "void 가 초기 성능에 안 보인다" 원전).
  큐 14~37 겹침 **0 건**(Bielefeld 는 2019 편만 큐에 있음).
- **2026-09-22 (ingest 15)** — `assb` **15호** 흡수:
  `raw/papers/rahman2024_sbms-rul-solid-state-batteries.md`
  (Rahman & Lu, *Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085; **6 쪽**, SI 없음,
  PDF sha256 `0d99b00e…`, 본문 sha256 봉인). **첫 학회 회의록**이고 **이 계보에서 심사
  강도가 가장 낮은 표본**이다 — DOI·접수/게재 일자·심사 기록 전부 없다.
  ⚠⚠ **1차 측정 0 을 넘어 재인용 수치도 0** (12·13호보다 한 단계 아래):
  `[재현]` 본문 2,331 단어에서 인용 괄호·절 번호를 빼면 남는 숫자가 **2024 · 8085 · 19 ·
  2021 · 2026** 뿐이고, `capacity`·`experiment*`·`measur*`·`contact`·`pressure` 가 **전부 0 회**.
  본문 그림 **1 장**(액체셀 종설 ref [16] Zou 2023 의 재수록) · 표 0 · 식 0.
  컴파일: **새 개념 0** (6 쪽 회의록에 새 축이 없다). 갱신 — 닻 이 카드(채움표 15호 행 +
  Evidence 열두 번째 + 이 항목) · [[composite-cathode-percolation-utilization]]
  (1호가 야생에서 인용되는 방식 1 절 추가). `index.md` 변동 없음(새 컴파일 페이지 0).
  ★★ **최대 수확은 논문의 내용이 아니라 인용 관계 둘이다** — 이 위키 최초로
  **우리가 이미 읽은 원전을 인용하는 편**이 들어왔다:
  ① **ref [5] = 1호, 어긋난다** (기하 모형 논문이 "부하 균등화·SOC 추정·건전성 모니터링"
  의 근거 · 연도 2018 오기) ② **ref [21] = 12호, 어긋나지 않지만 12호의 결론
  (`[재현]` SSB 실측 열화 라벨 **0/28**)을 버리고 FNN/RNN 정의만 가져간다.**
  ★ **분류 체계 세 번째 표본 = "어휘 미도입"** (12호 병합 · 13호 미배정 · 15호 미도입) →
  `[해석]` **접촉 구분은 실험 층위에서 강제되고 종합 층위에서 소실된다** (표본 3, 잠정).
  Q1~Q8 채움표 행 추가 (**누적 ≈8.5/8 유지, 새 칸 0**). **Q4 여덟 번째 성질 — 가장 얕은 0**
  (추정기 자체가 없다; `accuracy` 7 회 : 수치 0 : 불확실성 0). **여전히 0/15.**
  어긋남 원장 **11 건**(원전 대조로 확인된 것 2 · 제목 기준 판단 3 · 나머지는 내부 정합).
  후속 후보 1 순위 = **Asheri et al., *Comput. Mater. Sci.* 226, 112186 (2023)**(ref [22] —
  ML × SSB **계면 손상**, 12호의 28 슬롯에도 없던 좌표) · 2 순위 = **Bielefeld et al.,
  *ACS AMI* 12, 12821 (2020)**(ref [28] — 1호의 직계 속편, 바인더·탄소 축) ·
  3 순위 = Zou et al., *JES* 73, 109069 (2023)(ref [16], Figure 1 의 원전; ⚠ 액체셀이므로
  `assb` 태그 금지) · 4 순위 = Lipu et al., *JES* 55, 105752 (2022)(ref [33] — 이 편
  참고문헌 중 **제목에 RUL 이 있는 유일한 편**인데 15호가 RUL 을 안 가져왔다; ⚠ 액체셀).
- ★★★ **2026-09-22 (ingest 16)** — `assb` 16호 흡수:
  `raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`
  (Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling, *Batteries & Supercaps* **2026**, 9,
  e70315, doi `10.1002/batt.70315`, **CC BY**; 본문 10 쪽 + **SI 6 쪽**, 둘 다 sha256 봉인).
  **큐 15번 · 이 큐 3전극 실측 5편(15·16·18·19·20)의 첫 편.**
  크로핑 19 장 중 **11 개 파일을 실제로 봄**(본문 Fig. 1–7 전부 + SI S1·S2·S3·S4 + Fig. 3 의
  (b)(d) 확대 · S2 양 패널 확대 · S3 하단 확대). 안 본 것: SI S5·S6(Bode 적합)·S7(XRD)·
  S8(Arrhenius), 표 크롭 4 장.
  ★★★ **계보 최초 3 건**: ① **3전극 전극 분해**(리튬화 Au/W μ-RE ∅25 µm) + `[인쇄]`
  **2E = 3E 합(10 kHz 아래)** 자기 검증 ② **압력을 본체로 삼은 1차 측정**(`pressure` **49 회** —
  계보 최대) ③ **DRT 정규화 λ = 0.05 를 인쇄** ([[drt-peak-count-nonidentifiability]] 의
  **C1 최초 ✅**; C2–C5 는 전부 ❌).
  ★★★ **가장 큰 수확은 축퇴의 실측 표본**: `[인쇄]` 식 (4) 가 "접촉 면적" 이라 이름 붙인 양을
  **완전구 기하 면적**(`3ε_CAM/r_CAM`)으로 계산 ⇒ `[해석]` 측정량이 보는 것은
  **`j₀ · ε_CAM / r_CAM` 한 조합**(9호 `A_eff·ε_p/R_s` 와 같은 자리)인데 **뒤 둘을 고정해
  전부 `j₀` 로 읽는다**(0.74 → 1.33 A m⁻²). 같은 Table 2 의 `Q_DL` **0.18 → 0.54 (3 배)** 를
  면적으로 읽으면 `[재현]` **`j₀` 가 0.60 배로 감소** — **같은 데이터, 반대 결론**.
  → [[assb-lampe-contact-product-degeneracy]] (**single-source → multi-source-primary**,
  처방표에 **`R_CT·C_dl` 채널** 신설).
  ★★ **Q5 가 네 겹으로 채워졌다**: 기준극이 Li–In 이 **아니고**(Au/W) · 안정성을 **인용으로
  가정**(`stable` 3 중 2 가 남의 논문) · `[도표]` **리튬화 곡선에 평탄부 없음**(2.5 µAh 에
  560 mV 표류) · `[도표]` **두 셀의 In–Li 평탄 전위가 0.58 ↔ 0.47 V (0.11 V) 어긋남**,
  `[재현]` 과전압 ≈5 mV 로 설명 불가, **논문 무언급**.
  ★★★ **그리고 평탄 OCP 구간 안에서 음극 DRT 가 `[도표]` 18.6 → 1.2 (≈15 배)** 움직인다 —
  **"음극이 평탄하다" ≠ "음극이 조용하다".**
  **Q6**: 운전 **97 / 389 MPa** = 계보 최댓값(5호 Li 금속 상한의 5.2 배, ⚠ 화학 다름),
  **제작 = 운전인 첫 표본**, 압력 → 임피던스 1 차(완전지 반원합 `[인쇄]` 23↔85 Ωcm²),
  압력 → 공극률 `[인쇄]` **11.2 ↔ 12.9 %**, 압력 → 용량 `[도표]` **+9 … +59 %**(SI 그림에만,
  본문 `capacity` **1 회**). ⚠ **스윕 아님(2 점) · 이력 0 · 두 압력이 다른 셀 · 97 MPa 은
  필연적 하강 분기**(논문 무언급) → 5호의 `θ(P)` 이력 물음은 **여전히 미해결**.
  **어긋남 원장 12 건**(D1 본문 "In 박 두께 동일" ↔ SI 67–109 µm · D3 "2 배 넘게" ↔ `[재현]`
  1.797 · D6 완전지 DRT 의 τ≈10⁻⁴ 봉우리가 **양극·음극 어디에도 없다** · D7 **부분(4.6)이
  전체(3.1)보다 크다** …), 공백 원장 **16 건**(G3 `D_CAM` 3.1 배 무언급 · G5 분리막 저항 비공개 ·
  G9 `x_Li` 와 두께가 완전 공선 · G12 용량 미논의 …).
  **Q1~Q8 채움표 16호 행 추가 — 누적 ≈8.5 → ≈9.5** (Q2 +0.5 전극 분해 관측 · Q5 +0.5 기준극 실측).
  **Q4 아홉 번째 성질 = "밟고 지나갔다" — 여전히 0/16.**
  컴파일: [[assb-lampe-contact-product-degeneracy]] · [[assb-stack-pressure-operating-window]] ·
  [[drt-peak-count-nonidentifiability]] 갱신. **새 개념 페이지는 만들지 않았다** (세 페이지가
  이미 이 편의 세 축을 담고 있다).
  후속 후보 1 순위 = ★ **Miß, Ramanayagam, Roling, *ACS AMI* 14 (2022) 38246**(ref [30] —
  이 편 **TLM 방법의 원본**이자 `r_CAM`·초기값·비교 `j₀` 의 출처. 원본을 봐야 이 편의 고정
  가정이 어디서 왔는지 닫힌다) · 2 순위 = **König, Ramanayagam, Kraus, Roling,
  *Batteries & Supercaps* 7 (2024) e202300578**(ref [31] — 음극 heterogeneous interphase
  모형의 원본, 대칭셀 판) · 3 순위 = **Hertle et al., *JES* 170 (2023) 40519**(ref [24] —
  μ-RE 원본, "0 V vs Li⁺/Li 안정" 의 **유일한 근거**; Q5 의 G6 이 여기서 닫힌다) ·
  4 순위 = **Fukunishi et al., *J. Power Sources* 564 (2023) 232864**(ref [39] —
  ★ **큐 17번과 같은 논문**이고 이 편의 유일한 외부 실측 대조군, 그리고 **열화를 다룬다**) ·
  5 순위 = Roling et al., **chemRxiv 2025** `10.26434/chemrxiv-2025-qj66b`(ref [34] —
  공극률–압력 관계의 출처, ⚠ 심사 전 프리프린트인데 이 편의 두께 전부가 여기 걸려 있다).

- **2026-09-22 (ingest 17)** — `assb` 17호 논문 흡수:
  `raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`
  (Yanev, Heubner, Nikolowski, Partsch, Auer, Michaelis, *J. Electrochem. Soc.* **171**
  (2024) 020512, doi `10.1149/1945-7111/ad2594`, **Editors' Choice · CC BY 4.0**,
  Fraunhofer IKTS + TU Dresden; 본문 8 쪽 + SI 2 쪽, 둘 다 sha256 봉인).
  크로핑 **6 장 전부 열람** + 캡션 크로퍼가 놓친 **Figure 2**(사진)를 `get_image_rects`
  로 직접 렌더해 열람 + Fig. 1(g–i, d–f, a–c) · Fig. 4(a, c, d) · Fig. 5(a, b) 를
  500–1100 dpi 로 재크롭해 수치 판독. **안 본 것 0.**
  ★★★★ **이 계보에서 Q5(Li-In 기준 전위)를 본체로 삼은 첫 편이고, 이 카드의 물음을
  한 셀 안에서 전극 분해로 실증한다**: 같은 양극·같은 프로토콜·0.1 C 에서 2전극이 보는
  것은 `[도표]` **방전 용량 198 → 185 mAh g⁻¹(−6.6 %) + 곡선 끝이 잘림**(= `LAM_PE` 의
  서명)인데, 3전극이 말하는 것은 `[재현]` **양극 임피던스 동일(≈31 ↔ ≈32.5 Ω), 전부
  상대극**이다 — `[도표]` `E_CE` 가 방전 끝에 0.62 → **≈1.0 V** 로 올라 양극이 3.0 V 대신
  `[재현]` **≈3.4 V** 에서 멈춘다. 반대 방향의 짝도 같은 논문에 있다: `[인쇄]` 과리튬화로
  기준이 **−0.2 V** → **컷오프 4.3 → 4.1 V** → 충전 용량 40 mAh g⁻¹ 감소(= `LLI` 흉내).
  ★★★★ **Q5 의 실제 폭** (→ **새 개념 페이지** [[assb-li-in-reference-potential-window]]):
  **① 열역학 평탄 ±10 mV 안** · **② Li-rich 이탈 `[인쇄]` −0.2 V** ·
  **③ In-rich 국소 고갈 `[인쇄]` +0.68 … +0.78 V** ⇒ **전체 폭 0.42 → 1.40 V ≈ 0.98 V.**
  ★★★ **우리가 한 옴 분리** `[재현]`(CE–RE 고주파 절편 `[도표]` foil ≈28.7 Ω, A = 1.131 cm²):
  0.1 C **9.1 mV = 관측 편차의 ≈100 %** · CA 초기 **0.52 V = 76 %** ·
  **CA 정상 ≈1.8 mV = 0.2 %** ⇒ **전류가 종료 기준까지 떨어진 뒤에도 남는 +0.73 V 는
  과전압이 아니다.** ⚠ "평형 전위" 는 `[해석]` — **CA 후 이완 곡선을 안 쟀다**.
  ★★★ **곱 축퇴 검사(16호 처방)의 첫 적용은 "적용 불가"** — `R_CT`·`C_dl`·`CPE`·
  등가회로 **전수 0 회**, `[인쇄]` "modelling of the impedance spectra are **beyond the
  scope of this study**". 세 편의 실패 양식이 다르다: **9호 적합 · 16호 한쪽 끝 선택
  (θ≡1) · 17호 만들지 않음**. 대신 이 편에는 **면적 ↔ 유효 이온전도도 공변**이라는
  다른 형태가 있고, `[재현]` 2전극 SE 20→40 wt% 의 Δ **≈9 Ω** 이 `[도표]` **복합 음극
  전체(≈6 Ω)보다 크다** ⇒ 음극 귀속의 근거가 0(3전극은 40 % 쪽만).
  **Q4 열 번째 성질 = "인쇄로 사양했다"** (`identifiab*`·`uncertaint*`·`error bar`·
  **`fit*` 전수 0 회**). ★ 그리고 **그 사양이 결론을 방어한다** — 결론이 적합의 출력이
  아니라 **전압계 판독**이라 축퇴할 자리가 없다(14호는 귀속이 **가정**, 17호는 **배선**).
  **여전히 0/17.**
  **Q1~Q8 채움표 17호 행 추가 — 누적 ≈9.5 → ≈10.0** (**Q5 +0.5**, 두 편 연속으로 칸이
  움직였다). **Q1·Q4 는 그대로 0.**
  어긋남 원장 **15 건**: **D3 In 75 mg + Li 3.6–4.4 mg ⇒ `[재현]` 44.3–49.3 at% ↔ 라벨
  45–50 at%**(논문 스스로 2 at% 가 결정적이라 쓴다 — 0.7 at% 는 그 단차의 35 %) ·
  **D4 2전극 30 °C ↔ 3전극 "room temperature" 인데 목적이 "reproduce"**(`[재현]` 면적
  정규화 HF 저항 ≈29 ↔ ≈47 Ω cm²) · **D6 3전극 foil 셀(40 at%)이 2전극의 어떤 foil 셀
  (45–50 at%)도 아니다 — 권장 조성 49 at% 는 전극 분해로 검증된 적이 없다** ·
  **D7 Fig. 2 의 시편은 "10 mm 를 13 mm 다이에" 눌러 측면 유동이 허용된 기하**인데 실제
  셀은 구속돼 있다 · **D8 "ca. 50 % SOC" 자기 모순** · **D11 Table S1 의 "추세"(0.5 %p)가
  산포 대용(2.2 %p)의 1/4.4** · **D12 ref 32 = 우리 10호 Vadhva 2021 인데, 원전은 "In–Li
  셀은 LMA 셀과 귀속이 반대 … system-by-system basis" 라고 쓰고 17호는 "established" 로
  옮긴다**(⚠ 자기 화학에 대해서는 정합, 우리 위키의 **원전 대조 두 번째 사례**) ·
  **D14 EIS 를 충전 상태 + 5 h 이완에서 쟀는데 foil 음극이 100 mHz 에서도 닫히지 않는다** ·
  **D15 RE 도금 전하가 음극에서 나오는데 조성은 "40 at% 고정"**(`[재현]` 셀 면적 기준이면
  foil −2.8 at% · 복합 −4.5 at%, ⚠ 기준 면적 미명시). 공백 원장 **12 건**(G1 개방회로
  `E_CE` 0 회 · G2 CA 후 이완 0 · G4 적합 0 · G7 화학·단면 분석 0 · G8 압력 한 점).
  ★ 그리고 `[재현]` **우리가 한 자기 검증**: `Z_WE/CE ≈ Z_WE/RE + Z_CE/RE` 가 **2 Hz 에서
  두 셀 다 1 % 안**(foil HF 절편만 7 % 어긋남) — **논문은 이 검사를 하지 않는다.**
  그리고 `[재현]` **RE 표류 상한 ≈20 mV / 20 h** (복합 셀 `E_CE` 가 0.61–0.63 밖으로
  안 나감) = **계보 최초의 기준극 표류 상한**(⚠ 세 항의 합의 상한).
  컴파일: **새 개념 페이지 1** [[assb-li-in-reference-potential-window]] (`assb` 열째) +
  이 카드(채움표 17행 · 17호 절 9 항 · Evidence For **열네 번째** · Against 에 "세 번째
  전극" 항 · "아직 모르는 것 2" 갱신 · "주장하지 않는 것" 6 항) +
  [[assb-lampe-contact-product-degeneracy]] · [[assb-stack-pressure-operating-window]] 갱신.
  후속 후보 1 순위 = ★★★ **Santhosha, Medenbach, Buchheim, Adelhelm,
  *Batteries & Supercaps* 2019**(ref 26 — **0.62 V 가 태어난 자리**, 쿨로메트릭 적정.
  우리 Q5 의 열역학 바닥이고 16호(0.58↔0.47 V)·17호(±10 mV)의 산포를 대조할 유일한 기준.
  ⚠ 서지가 `[인쇄]` "414, 359 (2019)" 로 권호가 이상하다) ·
  2 순위 = ★★★ **Nam, Park, Oh, An, Jung, *J. Mater. Chem. A* 2018, 6, 14867**(ref 20 —
  **Li-In-SE 복합 음극의 원전**이자 "Li-depleted In-rich layers" 의 원전; 17호의 처방과
  기구 설명이 전부 여기서 온다) ·
  3 순위 = ★★★ **Sedlmeier, Schuster, Schramm, Gasteiger, *JES* 2023, 170, 030536**(ref 21 —
  **Li 박 방향을 뒤집은 실험이 이미 여기 있다**; 위 §8 의 검증 실험) ·
  4 순위 = **Ikezawa, Fukunishi, …, Kanno, Arai, *Electrochem. Commun.* 2020, 116, 106743**
  (ref 16 — ⚠ **큐 17번(Fukunishi 2023)과 같은 그룹**이고 16호의 유일한 외부 대조군이었다.
  **큐 17번을 먼저 읽는 것이 경제적일 수 있다**) ·
  5 순위 = **Yanev et al., *JES* 2022, 169, 090519**(ref 29 — 이 편의 CA 율시험 방법 원전;
  "저율 평탄 + 급락 = 양극 제한" 형태 기준의 근거가 여기 있어야 한다) ·
  6 순위 = **Wang, Zhao, …, Huang, *eScience* 2023, 3, 100087**(ref 28 — 17호와 **정면
  충돌**, `[인쇄]` 14.3 at% Li 가 최적. Q5·Q6 양쪽).
  ⚠ **큐 대조**: 큐 **17**(Fukunishi 2023) · **19**(embedded indium RE) · **20**(μ-RE,
  Indium-Lithium anodes) 세 편이 전부 이 축이다. **위 1·2·3 순위는 큐에 없다.**

- ★★★★ **2026-09-22 (18호 Fukunishi et al. 2023) — `assb` 18호, 큐 17번.**
  `raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md`
  (*J. Power Sources* **564** (2023) 232864, Tokyo Tech + NEDO SOLiD-EV; 본문 10 쪽 +
  SI 6 쪽; **16호가 지목한 유일한 외부 실측 대조군**).
  크로핑 **13 장** 중 **그림 11 장 전부 열람** + 캡션이 없어 크로퍼가 놓친 **1 쪽
  Graphical Abstract 를 직접 렌더**해 열람. 안 본 것은 표 크롭 2 장(PDF 텍스트 사용).
  누락은 `get_images()`/`get_drawings()` 페이지별 계수로 기계 확인 — **놓친 그래픽은
  무캡션 도판 1 건뿐**.
  ★★★★ **최대 수확 둘.** ① **이 카드의 물음이 지면에 문장으로 인쇄되고 갈리지 않는다**:
  `[인쇄]` "the **chemical composition at the interface or the contact area** … changed",
  그리고 `[인쇄]` "insulative layers **completely cover** … such **dead particles** …
  could explain the **large capacity decrease**"(= `θ_AM` 의 기구 서술, 값 0).
  ② ★★★★ **16호 처방의 첫 성공 — 저자의 표로 저자의 "or" 를 갈랐다.** `[재현]`
  `C ≡ τ/R` 의 노화 전후 비 **LPSI 0.37 ± 0.07 · LPSCl 1.07 ± 0.19**(순수 면적 0.15/0.13 ·
  순수 동역학 1.00) ⇒ **LPSCl 은 화학만, LPSI 는 면적 ≈1/2.7 + 화학 ≈2.4 배.**
  ★ 그 분해가 **같은 논문의 SEM(LPSI 에만 입자를 덮는 O·P 층 2 µm)과 독립으로 일치한다.**
  ⚠ 측정이 아니라 **지면 두 열의 조합**이다(로그 막대 판독 · 노화 후 `p` 미공개 ·
  `C∝θ` 가정 · 조건당 셀 1).
  ★★★ **17호가 연 오염 경로가 설계상 닫혀 있다** — `[인쇄]` 컷오프가 **작업전극 전위**
  (0.85–2.65 V)이고 `[도표]` 상대극이 전 구간 평탄(≈0.60 V) ⇒ `[인쇄]` "the amount of
  **effective active material** decreased **only in the LPSI system**" 은 **상대극 오염 없이
  말해진 첫 양극 활물질 손실 문장**이다(⚠ 값 0).
  ★★★ **16호와의 3전극 배정 대질**: 고주파(집전체)·중주파(전하이동)는 **같고**,
  **저주파가 다르다** — 다결정 NCM523 은 **2차 입자 내부 반원(`R4`, ~1 Hz)**을 저주파에
  하나 더 놓고, 그것이 음극 기여와 겹친다. 16호는 단결정이라 없다(두 편이 서로 인용하며
  동의한다). ⇒ **"저주파 = 음극" 규칙은 화학뿐 아니라 양극 미세구조의 함수다.**
  ★★ **DRT**: C1(λ) ✅ 두 값 인쇄 — 다만 **LPSI 6.0×10⁻² ↔ LPSCl 8.5×10⁻⁴ 로 70 배** 다르고
  봉우리 개수도 3 ↔ 4 다. **C2(K–K/Lin-KK) 계보 최초 ✅** — ⚠ 그 잔차를 `[인쇄]`
  **기준극 안정성**의 근거로 쓰는 것은 범주 오류.
  ⚠ **Q6**: `pressure` **본문 0 회**(제작 110/150 MPa 두 값뿐, 운전 압력 미보고)인데
  주 열화 기구가 **void 형성**이다. ⚠ **교락**: 두 전해질계의 **복합양극 조성이 다르다**
  (49:43:8 ↔ 69:26:5 wt%). ⚠ **산포**: `[재현]` 같은 이름표의 `R3` 가 세 곳에서 **1.45 배**
  벌어진다(≈±20 %).
  **채움표 18호 행 — 누적 ≈10.0 → ≈10.5** (**Q1 +0.5**, 접촉 면적이 처음으로 측정된 양이
  됐다; 비뿐이고 `θ(N)` 은 0 이라 반 칸). **Q4 0/18 — 열한 번째 성질 = "갈림을 인쇄하고
  가르지 않았다".**
  후속 후보 1 순위 = **Ikezawa et al., *Electrochem. Commun.* 116 (2020) 106743**(ref 27 —
  **R-LTO 기준극과 이 편 방법의 원전**; 1.55 V 의 근거와 안정성 데이터가 거기 있어야 한다).
  ⚠ **16·17·18호 세 편이 전부 이 한 편을 가리키는데 큐에 없다.**
- **2026-09-22 (ingest 19)** — `assb` **19호** 흡수 (큐 18번):
  `raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md`
  (Yoshida, Ikezawa, Okajima, Arai, *Electrochim. Acta* **497** (2024) 144523,
  **CC BY**; 본문 9 쪽 + SI 9 쪽. 크로핑 17 장 중 **그림 9 장 직접 열람** +
  **캡션이 "Figure S 5" 로 띄어져 크로퍼가 놓친 Fig. S5 를 SI p.6 직접 렌더로 열람**).
  ★ **18호와 같은 연구실의 같은 계보** — Ikezawa·Okajima·Arai 가 겹치고 감사문이
  **18호 제1저자 Fukunishi** 에게 기술 자문을 사례한다. **큐가 확인하라던
  Ikezawa 2020 (*Electrochem. Commun.* 116, 106743)은 여기서도 인용된다 — ref [18].**
  ⚠ **먼저 경계**: 이 편에는 **전극이 없다**(활물질·용량·사이클 0). Q1·Q2·Q3(라벨)·Q7·Q8
  에 구조적으로 기여할 수 없다.
  ★★★★ **Q5 — 계보 다섯 번째 형태: 재지도 가정하지도 않고 *소거한다*.** 4전극의 측정량이
  `[인쇄]` **RE₂ − RE₁** 이라 R-LTO 의 절대 전위가 상쇄된다 ⇒ `assum*` **0 회**,
  "**1.55**" **0 회** (18호의 G4 가 생기지 않는다). 대신 새 바닥이 인쇄된다:
  RE–RE 개방회로 **−4 / −5 / +25 mV**, `[인쇄]` "within the **reproducibility of the
  reference electrode potentials (ca. ±30 mV)**" = **계보 최초의 기준극 재현성 숫자이자
  검출 하한** (⚠ **근거 미제시**). ★ **R-LTO 조성도 처음 인쇄된다** —
  **Li₇Ti₅O₁₂:Li₄Ti₅O₁₂ = 67:33 mol%**(2 상 한복판), 18호의 "partially reduced" 공백 절반 해소.
  ★★★★ **큐 메모("상대극 전위 변화가 비선형")의 출처 확정** — §3.2 마지막 문단,
  `[인쇄]` "The potential change in the counter electrode is **not linear** … **asymmetric**",
  근거 그림 **Fig. S4**. `[도표]` 200 s·≤0.7 mA CV 에서 `E_CE` **42 / 126 / 75 mV** 이동,
  `[재현]` `ΔE/ΔI` = **44 / 221 / 83 Ω = 같은 셀 계면 저항의 2–18 배**
  ⇒ **"4전극이 3전극보다 무엇을 더 재는가" 의 정량 답**. `[재현]` **(ㄱ)(ㄴ) 만족 ·
  (ㄷ)만 깬 첫 표본**(재고 여유 ≈260 배, `j` = 0.41–1.07 mA cm⁻²) ⇒ **(ㄷ) 단독은
  10⁻²–10⁻¹ V 대**, 17호의 0.7 V 는 **고갈**의 산물. ⚠ 이동이 **가역 분극**이라 같은 양은 아니다.
  ★★★★ **Q2 — 비분리를 자기 데이터로 증명한 첫 편**: `[인쇄]` Li-In 전극 반원이
  **P1(>1 kHz)·P2(1 kHz–0.1 Hz) 둘 다와 겹쳐** "**difficult to extract** … two-electrode
  system". `[도표]` 같은 공칭 Li-In 의 전극 저항 **39/172/54 Ω = 4.4 배 (n=3)**.
  ⇒ **10·11·16·18호 계보의 네 번째이자 가장 근본적인 층**(양극을 바꿔도 음극은 거기 있다).
  ★★★★ **곱 축퇴 처방 세 번째 적용 = 부분 적용 + 전제 반증 + 대체 채널.**
  입력은 처음 완비(Table 2 가 `R`·`Q`·`p`·`C`·`τ` 전수, `C` 는 저자가 Brug 식으로 계산)
  이고 면적 조작도 셋(압력 2 점 · 단면적 3 점 · 계면 유무 대조)인데:
  **검사 A** `[재현]` `P2` 의 `C` 가 기하 면적 기준 **2.0–4.8 mF cm⁻² = 이중층의 200–480 배**
  ⇒ **물리 상한 2–3 자릿수 초과, 전제 `C ∝ θ` 반증**(18호의 "2–3 배 빗나감" 에 이어 두 번째).
  **검사 B** `[재현]` `τ₂` 가 ±13 % 안(면적 차 2.4 배)인데 `Ea(R₂)` 는 **27/41/42 kJ mol⁻¹**
  ⇒ 전지수 인자 **158–174 배** 필요 ⇒ **두 채널이 70 배 충돌**.
  **검사 C** 압력 축에 `C` 가 안 붙어 있다(18호와 정반대의 결손).
  ★ **대신 `[인쇄]` "the physical state of the interface does not affect the Ea but the
  resistance values … Ea as the essential parameter"** ⇒ **`Ea` = 면적-불변 채널**.
  ⇒ **18호가 `Ea(노화 전후)` 를 쟀다면 검사 B 가 `C` 없이 독립 확인됐을 것이다.**
  ★★★★ **산포 하한**: `[도표]` LPSCl\|LPSCl 의 `Ea(R₁)` **45.5 ± 0.1** ↔ 같은 물질
  Table 1 벌크 **40.5 ± 0.3** ⇒ **5.0 kJ mol⁻¹ = 인쇄된 ± 의 12–50 배, 논문 무언급**(D10).
  ⚠⚠ **중심 배정이 4 점 · 이상치 1 개에 걸려 있다**: `S` 축은 벌크·계면을 못 가르고
  (둘 다 `1/S`), `d` 축의 `[도표]` `R₂/d` = **17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹** —
  이상치를 빼면 `R₁` 만큼 `d` 에 비례해 **결론이 뒤집힌다**. ★ 다만 같은 지면의
  **Fig. 7(계면 유무 대조)** 가 훨씬 강하게 지지한다 — **논증 순서가 거꾸로다.**
  **Q6**: 운전 **ca. 420 / 560 / 840 kPa** = **계보 최저 대역**이고 **8호가 인쇄한 산업
  요구치 <≈1 MPa 안에 들어온 첫 편**. ⚠ 2 점 · n=1, `[재현]` 420 kPa 의 `R₂` 가
  560 kPa 보다 작아 **추세와 반대**.
  **어긋남 16 건** (D10 `Ea` 자기 불일치 · D5 율결정 단계 지표가 본문 "(ii)" ↔ Fig. 6 의
  "Slow" 는 **(iii) 위치** · D6 `R₂`–`d` 이상치 · D9 CV 기울기 114 Ω ↔ Nyquist 183 Ω ·
  D3 Table 2 특성 주파수 **세 칸의 지수 부호 오타**, 정정하면 `P1` 꼭짓점이 **측정 상한
  7 MHz 밖** ⇒ `R₁` 은 외삽값 · D1 Fig. S5 패널 배정이 본문 ↔ SI 캡션에서 다르다).
  **채움표 19호 행 — 누적 ≈10.5 → ≈11.0** (**Q5 +0.5**; **Q1 ≈0.5 · Q4 0/19 유지** —
  **열두 번째 성질 = "어휘 없이 귀속을 실험으로 물었고 설계의 절반이 판별력이 없다"**).
  ⚠ **Q2 +0.5 를 검토했다가 접었다** — 활물질이 없어 가를 대상 자체가 없다.
  컴파일: [[assb-li-in-reference-potential-window]](4전극 층 추가) ·
  [[assb-lampe-contact-product-degeneracy]](처방 세 번째 적용 + `Ea` 채널) ·
  [[drt-peak-count-nonidentifiability]](네 번째 층).
  후속 후보 1 순위 = **Ikezawa 2020 (ref 18) — 세 번째 지목**(16·17·18·19호 **네 편**이
  가리키고, **±30 mV 와 1.55 V 의 근거가 둘 다 거기 있어야 한다**) ·
  2 순위 = **Fukunishi et al., *ACS Appl. Energy Mater.* 6 (2023) 10908**(ref 19 —
  **흑연 복합전극 3전극 + cyclability**, `θ(N)`·`Ea(N)` 가 있을 가능성이 계보에서 가장
  높다) · 3 순위 = **Abe 2005 (ref 14, `Ea` 로 율결정 단계를 정한 원전)**.
  ⚠ **1–3 순위 전부 큐에 없다.**

- **2026-09-22** — `assb` **20호** 흡수 (큐 **19번**, Chang·Choi·Kang·Park·Lim 2020,
  *Ionics* 26, 1555–1561, **Short Communication 7쪽, SI 없음**, 창원대 + RIST + 세종대).
  `raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md`.
  ★★★★ **계보 판정이 바뀐다 — 이 편은 Ikezawa 2020 을 가리키지 않고 가리킬 수 없다**
  (접수 2019-08-06 · 게재 2019-12-23). 16·17·18·19호가 전부 가리킨 그 논문의 **다섯
  번째가 아니라 그 앞**이다. 대신 **다른 공통 조상 둘**을 가리키고 둘 다 **17호가 이미
  지목한 것**이다 — ref [10] **Nam 2018 *JMCA*** · ref [19] **Santhosha 2019** ⇒
  **Q5 계보는 둘이다**(R-LTO 가지 4편 → Ikezawa 2020 / **In 가지 17·20호 → Nam·Santhosha**).
  **Q5 답**: **가정한다**(0.62 V). `assum*` **0회** · `0.62` **2회** — ★ **가정이 문장이
  아니라 그림의 두 번째 축("V vs. Li/Li⁺" = 왼쪽 + 0.62)으로 인쇄되기 때문**이고,
  **낱말 지문으로는 안 잡힌다.** ★★★★ 그러나 **가정이 깨지는 모습이 자기 그림에 남아
  있다**: `[재현]` **비리튬화 In 에서 `V₁ = V₂−V₃` 가 159 mV 깨지고 리튬화 뒤 5 mV 로
  닫힌다** ⇒ 신품 In 부유 전위 **1.77–1.93 V = 짝보다 1.15–1.31 V 높다**, 그리고 **정정된
  명제: 이 검사는 기준극의 *접촉*을 보지 *전위*를 보지 않는다**(범주 오류 세 번째 —
  18호 K–K · 19호 진폭 비의존 · 20호 키르히호프 항등식 — **단 유일하게 판별력 ≠ 0**).
  ★★★★ **17호 함정을 5년 먼저 피했다**: 첫 충전 **122 mAh g⁻¹(54 %)** 손실을 3전극이
  **음극**에 배정, `[도표]` 두 충전 모두 음극 **≈0.02–0.04 V vs Li/Li⁺** 에서 종료(양극은
  2.40 V) — 저자가 안 적은 수치다. ⚠ `[재현]` **저자 논거(275 Ω = 55 mV)는 격차의 12 %
  만 설명**하고, **방향 ⊗ 조성 교락**(방전 펄스 x≈0.03·음극 Li-rich ↔ 충전 펄스 x≈0.95·
  음극 Li-poor)이 있어 "탈합금화 > 합금화" 는 분리되지 않으며, `[재현]` **1일 휴지 뒤
  `V₁` 이 컷오프보다 310 mV 아래**라 손실의 일부는 **프로토콜 산물**이다.
  ★★★ **곱 축퇴 처방**: 1·2단계 **적용 불가**(등가회로·`C_dl`·`Ea`·`fit*`·본문
  `impedance` 전수 0회), **3단계는 시간 영역으로 번역해 적용되고 즉시 실패한다** —
  `[재현]` τ ≈ 10³ s ⇒ `C = τ/R ≈ 1 F cm⁻²` = 이중층 상한의 **10²–10³ 배**(19호 200–480배)
  ⇒ **`R_ct` 라 부른 성분은 전하이동이 아니다** ⇒ **처방 4단계 신설**.
  ★★★ **새 축 — 기준극 재고 예산**: `[재현]` RE Li 재고 = 셀의 **1/675**, 누설 **< 10 nA**
  요구, **3전극은 자기 표류를 공통 모드로 상쇄해 못 본다** ⇒ **19호 차분 설계의 물리적
  근거가 20호 데이터 안에 있다.** (ㄴ) 기준의 분모를 **이동 전하 ↔ 누설 전하**로 가른다.
  **채움표 20호 행 — 누적 ≈11.0 → ≈12.5** (**Q2 +0.5** 전극별 용량 손실 귀속 · **Q5 +0.5** ·
  **Q8 +0.5** 새 화학 TiS₂ + 두 전극 전위 궤적 동시 인쇄).
  **안 움직인 칸**: **Q1 0/20**(`θ`·`contact loss` 0회; `[재현]` "접촉 362 Ω" 은 복합전극
  내부 이온 경로만으로 ≈350 Ω 이 나와 **이름표가 데이터에 요구되지 않는다**) ·
  **Q4 0/20**(열세 번째 성질 = **"분해가 적합조차 아니다 — 작도다"**) ·
  **Q6 0**(`pressure`·`MPa`·`kPa` 전수 0회, **두 번째 완전 미보고**).
  ⚠ **Q7 해당 없음이나 기록 하나**: 합금 음극이 **도금 전위까지 밀린 첫 사례**인데
  논문에 `plating`·`dead`·`dendrit*` 0회.
  컴파일: **새 개념 0** (7쪽 Short Communication 에 새 축을 세울 분량이 없다).
  갱신 — 이 카드(채움표 20호 행 + Evidence For **열일곱 번째** + 새 제약 6개 + 이 항목) ·
  [[assb-lampe-contact-product-degeneracy]](**처방 네 번째 적용 + 4단계 신설**:
  시간 영역 `C = τ/R` 상한 검사, 그리고 **음극 판 곱 축퇴**) ·
  [[assb-li-in-reference-potential-window]](**다섯 번째 형태** + 조건 (5′)(누설 분모)·
  (7)(프로브 리튬화) 추가 + 처방 **P10**(누설/재고 예산)).
  후속 후보 1순위 = **Nam 2018 *JMCA* 6, 14867**(17호·20호 **동시 지목**, 제목이 곧
  failure modes) · 2순위 = **Santhosha 2019 *Batteries & Supercaps* 2**(0.62 V 의 출생지,
  **두 번째 지목**) · 3순위 = **Jin·Park·Park·Lim 2015 *Electrochim. Acta* 185, 242**
  (이 편의 셀 원전 — 공백 G1·G2·G3 의 답) · 4순위 = **Barai 2018 *Sci. Rep.* 8, 21**
  (`R₀`/`R_ct`/`R_p` 작도법 원전, 제목이 **measurement timescale**).
  ⚠ **1–4순위 전부 큐에 없다.**

- **2026-09-23** — `assb` **21호** 흡수 (큐 **20번**, Sedlmeier·Schuster·Schramm·Gasteiger 2023,
  *J. Electrochem. Soc.* 170, 030536, **CC BY, 13쪽, SI 없음**, TUM Gasteiger).
  `raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md`.
  ★★★★ **17호가 지목한 후속(ref 21)이자 개념 페이지 처방 P4 의 통제 실험**: 같은 InLi 박을 방향만
  바꿔(n = 3 씩) **"LiIn 이 분리막 면에 있느냐가 전부"** 를 지지한다 — 16↔17호 대질이 처음으로 한 변수만
  바꾼 데이터를 얻었다. ★★★★ **"0.62 V ✓ ≠ 재고 ✓"**: InLi-(In) 은 28 일 0.62 V(< 3 mV)인데 0.2 mA cm⁻²
  에서 **9 초 · 0.39 µAh cm⁻²**, InLi-(Li) 는 **15 h · 3.0 mAh cm⁻²**. ★★★★ `[인쇄]` **"cannot be assumed to
  stay invariant at 0.62 V"** — 0.62 V 가정의 부정이 조건(NCM|In, 방전 끝)과 기구(`LLI`)를 달고 나온 첫 문장.
  ★★★ **Q5 여섯 번째 형태 = 교정 이식**: GWRE 0.31 V 를 Li|Li 교정 셀에서 재고 InLi 셀로 옮긴다 —
  `assum*` 4 회(기준 전위엔 0) · `0.62` 18 · `0.31` 7, 가정이 **"calculated based on"** 으로 · Fig. 4 두 번째 축으로 ·
  Fig. 6·8 은 환산 축만으로 — 그리고 **크로퍼가 놓친 부록 Fig. A·1 의 축 이름과 숫자가 정확히 0.62 V
  어긋난다**(순환이 두 그림에). ★★★ **기준극 표류 < 3 mV / 28 일**(고정 전극 두 개로 공통 모드가 보인다 —
  20호 명제 정련), `[재현]` **누설 < ≈4.3 nA**(간접; 직접 측정 21/21 편 0).
  ★★★ **곱 축퇴 처방 다섯 번째 적용**: 1단계를 **τ 형**으로(꼭짓점 주파수) — Li|Li 쌍은 **면적 서명 통과**,
  InLi 쌍은 **정렬 어긋남 기각**(`[재현]` C 비 ≳1.4 ↔ 0.28); 3단계-b 로 **"전하이동" 저주파 호의 C ≈0.5–0.6 mF cm⁻²
  = 이중층 비용량의 ≈50–64 배**(세 번째 실패, 단 관대한 상한 10⁻² F cm⁻² 로는 통과 — 개념 페이지의 두 기준값이
  섞여 있음을 기록); 4단계로 6단계 "이중층 충전" 설명이 **10²–10³ 배** 실패.
  ⚠⚠ `[재현]` **저자의 D ≥ 4.4×10⁻⁸ cm² s⁻¹ 와 1 at% 고용체는 9 초와 양립하지 않는다**(Sand ≈54 분 · ≈181 µAh cm⁻²,
  ≈360–465 배) — OCV 가 c 를 1 at% 근처로 묶으므로 **틀린 쪽은 D**(1단계 과도는 WE 벌크 확산이 아니다).
  ⚠ **어긋남 14 건**(D1 순수 In 38 ± 0.8 → ±10 · D2 A·1 0.62 V · D5 압착 60 ↔ 70 MPa · D14 "Warburg ⇒ 전하이동 없음").
  **채움표 21호 행 — 누적 ≈12.5 → ≈13.5** (**Q2 +0.5** "있음 ↔ 접근 가능" 을 독립 관측 둘로 · **Q5 +0.5**).
  **안 움직인 칸**: **Q1 0/21**(접촉을 이름 붙여 SEI 와 한 반원에 합치고 압력 가설로 넘겼다) · **Q4 0/21**(열네 번째
  성질 = **"값의 정확도를 검사하고 배정의 유일성으로 읽었다"**) · **Q6 칸 이동 없음**(보고·통제, 스윕 0) ·
  **Q7·Q8 해당 없음**. Q3 은 층 하나(계보 최초 동일 조건 셀 간 ± n = 3).
  그림: 크로퍼 9장 + **부록 A·1 수동 400 dpi**, **10장 전부 봤다 — 안 본 것 0장**.
  컴파일: **새 개념 0** — 기존 두 페이지 갱신: [[assb-li-in-reference-potential-window]](21호 절 · ③ 의 두 성질 ·
  평탄 조건 정련 · P4 실행 · 16↔17호 대질 판정 · P11) · [[assb-lampe-contact-product-degeneracy]](다섯 번째 적용).
  후속 1순위 = **Ikezawa 2020**(**다섯 번째 지목** — 21호가 InLi-(In) 조립의 예로도 인용해 **두 Q5 가지가 만나는 자리**) ·
  2순위 = **Nam 2018 *JMCA***(세 번째 지목, 계면 고갈 원전) · 3순위 = **Santhosha 2019**(세 번째 지목) ·
  4순위 = **Solchenbach 2016 *JES* 163, A2265**(GWRE · 0.31 V 원전). ⚠ **1–4순위 전부 큐에 없다.**

- **2026-09-23** — `assb` **22호** 흡수 (큐 **21번**, Strauss·Bartsch·de Biasi·Kim·Janek·Hartmann·Brezesinski 2018,
  *ACS Energy Lett.* 3, 992−996, Letter 5쪽 + SI 8쪽, KIT BELLA + JLU Giessen + BASF — **1호의 ref 13**).
  `raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md`.
  ★★★★ **Q1 이 `θ` 축에서 처음 움직였다** — 불활성 CAM 분율 **2 / 27 / 31 %** 는 **회절 상 분율의 측정**이고(용량 비입력),
  용량은 독립 대조로 닫힌다(±7 %). 큐 메모 *"ex situ XRD 의 inactive AM 분율 = `1 − θ_AM`"* 은 **반만 맞다** —
  측정은 맞고, **등호는 아니다**(합집합 상한 · `[재현]` 집전체 면 ≈3–15 µm 표층 · 신품 C/10 한 점).
  ★★★ **3항 분해의 첫 실측 분리**: `[재현]` NCM-L θ ≈0.69 · η ≈0.69 — 결손의 절반은 불활성이 아니라 **활성 입자의 덜 충전**.
  ★★★★ **1호 대질**: 인용 네 가지는 원문과 맞는다(`poros*` 0 회 확인). 그러나 `[재현]` **무공극 상한에서 1호 식 (8) 은 불활성을
  ≈23–40 / ≈95 / ≈95–97 % 로 예측**하고, 측정은 2 / 27 / 31 %, **용량만의 상한 ≤3 / ≤39 / ≤44 %** ⇒ "correlate well" 은 **순위만**
  맞다. ⚠⚠ **원인 배정("lack of electronic contact")은 병치**: `[도표]` σ_e/σ_ion ≈550 / ≈50 / ≈1.5, 불활성 M ≈ L; Fig. 4 두 축
  자릿수 간격 불일치. **곱 축퇴 처방 여섯 번째 적용** — 1·3단계 ❌(`impedan*` 0), 2단계 ⚠(LIB 대조 · M↔L 같은 로트 쌍, 면적 미측정),
  4단계 ✅(DC 분극 과도 C ≈0.4–0.8 F cm⁻² = 화학량 분극 ⇒ σ_ion 상한); ★ **처방 표에 없던 채널 "SOC 추종 상 분율"** 이 `θ·ε_p` 를 뗀다.
  **17호 함정**: 주 주장(XRD)은 **설계상 면제**(양극을 전위 없이 읽은 첫 편), 용량·CE 축은 노출. **Q5 일곱 번째 형태**
  = "가정이 대조군 전압창을 정한다"(0.6 V, `[도표]` ±30 mV 정합). **Q4 0/22** — 열다섯 번째 성질 = **"측정이 분할을 대신했고
  원인은 병치됐다"**, 그리고 c(x) 가지 선택을 밟고 지나감(`[도표]` V(x) 로 읽으면 L·M 의 x 순서가 뒤집힌다).
  **채움표 22호 행 — 누적 ≈13.5 → ≈14.5** (**Q1 +0.5** · **Q2 +0.5**). **안 움직인 칸**: Q4 · Q5 · Q6 · Q8(칸 이동 없음) · Q7(해당 없음).
  ⚠ 어긋남 12 건(D1 σ 식 차원 역전 · D2 20 µm 체 ↔ d₅₀ 15.6 · D6 L 의 Q_XRD > Q_echem · D7 S7 분리층 · D8 Fig. 4 축).
  그림: 크로퍼 11장(본문 4 + SI 7) + 표 1 — **그림 11장 전부 봤다, 안 본 것 0장**.
  컴파일: **새 개념 0** — 기존 세 페이지 갱신: [[composite-cathode-percolation-utilization]](measured 라벨과 1호 대질) ·
  [[assb-apparent-capacity-decomposition]](θ·η 첫 실측 분리) · [[assb-lampe-contact-product-degeneracy]](여섯 번째 적용).
  후속 1순위 = **Koerver 2017 *Chem. Mater.*(큐 22, 이 편 ref 9, 본문 4 회 인용)** · 2순위 = **Zhang 2017 *JMCA* 5, 9929**(ref 18, 셀 장치 원전) ·
  3순위 = **Zhang 2017 *ACS AMI* 9, 17835**(ref 16, 같은 연구망 복합체 토모그래피 — 공극률 후보).

- **2026-09-23** — `assb` **23호** 흡수 (큐 **22번**, Koerver·Aygün·Leichtweiß·Dietrich·Zhang·Binder·Hartmann·Zeier·Janek 2017,
  *Chem. Mater.* 29, 5574−5582, Article 9쪽 + SI 7쪽, JLU Giessen + KIT BELLA + BASF — **1호 ref 7 · 22호 ref 9 · 21호 ref 29 · 18호 [23] · 9호 [17]**).
  `raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md`.
  큐 메모 *"접촉 손실의 실험 원전 + 전압·용량축"* 은 **반만 맞다** — **실험 원전은 맞다**(계보 최초 SEM 틈 + 미사이클 분해 대조, 전압·용량축
  Fig. 1), **정량 원전은 아니다**(치수·분율·용량 몫 0). ★★★★ **원전은 계면층 ↔ 접촉을 가르지 않는다** — XPS ↔ SEM 채널 분담으로 존재를
  보이고 몫은 시간 분할로 배정; 초록 ↔ 결론이 `ΔR` 을 다르게 배정. ★★★★ **SI 가 가른다(우리 조합)**: `R_SE/Cathode` ×1.5–2.45 동안
  `C` ×0.96–1.05(두 셀·다섯 구간) ⇒ `R` 증가분은 **화학 형**; S3 무전류 이완이 전제의 부분 양성 대조. **곱 축퇴 처방 일곱 번째 적용**
  — 1단계 ✅(계보 첫 **상태축 위 연속**) · 2단계 ⚠(무전류 이완 = 전제 양성 대조, 한 호만) · 3-a ❌ · 3-b 양극 호 ✅(DL 의 ≈1–2 %) / 음극 호 ❌
  (50–640 배) · 4단계 ⚠(DC 100 ↔ EIS 25 mV, 충전만 이동 = 창 이동). ★★★ `[재현]` 손실 예산: 계면층 패러데이 ≈4 % + 옴 ≲3 % ⇒ **≳85 % 미배정**.
  ★★★★ **17호 함정 노출 + 대조군 공유** (두 상대극 무 Li 조립, 방전 끝 `C_anode` ≈90–100 배 붕괴). **Q5 여덟 번째 형태** = "가정을 명시하고
  깨지는 곳을 '활성화'·'음극 동역학' 으로 덮음"(`[재현]` 첫 충전 앞 상대극 ≥ ≈0.1 V 높음). ★★★ **인용 대질**: 숫자 오기 0 — 대신 강도 과장
  (1호) · 회피의 증명화(1호 탄소) · **기구 치환(18호 "space charge", 원전 0 회)** · 초록 채택(9호); 22호 ref 9 네 문장·21호 ref 29 두 문장은 원문과 맞다.
  **채움표 23호 행 — 누적 ≈14.5 → ≈15.0** (**Q2 +0.5**). **안 움직인 칸**: Q1(이름표 + 정성, `θ(N)` 측정량 0/23) · Q4 0/23(열여섯 번째 성질
  "채널 분담 + 시간 분할 배정") · Q5 · Q6 · Q8(칸 이동 없음) · Q7(해당 없음). Q3 층 하나(n = 4 인쇄, 산포 0).
  ⚠ 어긋남 18 건(D2 Ω·cm⁻² = R/A 차원 역전 · D6 "IR 증가" ↔ 충전만 이동 · D10 S3 판 a↔c ≈8 배 · D11 초록 ↔ 결론 · D15 "0.6 V" 두 뜻).
  그림: 크로퍼 14장(본문 6 + SI 8) — **14장 전부 봤다, 안 본 것 0장** (+ Fig. 6 원본 SEM 픽셀 계측).
  컴파일: **새 개념 [[assb-interphase-vs-contact-loss-attribution]]** + 갱신 [[assb-lampe-contact-product-degeneracy]](일곱 번째 적용) ·
  [[assb-apparent-capacity-decomposition]](손실 예산) · [[assb-li-in-reference-potential-window]](여덟 번째 형태 · P13).
  후속 1순위 = **Zhang 2017 *ACS AMI* 9, 17835**(ref 29, 방법 원전) · 2순위 = **Kondrakov 2017 *JPCC* 121, 3286**(ref 41, NCM811 ΔV) ·
  3순위 = **Ishidzu 2016 *SSI* 288, 176**(ref 48).

- **2026-09-23 (ingest 24, `assb` 24호 Stavola et al. 2023 · *ACS Energy Lett.* 8, 1273−1280 · CC-BY 4.0)** — 큐 **23번**. Northeastern + Argonne APS 6-BM.
  큐 메모 *"01 이 '두께 효과는 유한 크기 인공물' 이라 한 자리를 실측으로 친다"* 는 **자리는 맞고 타격은 아니다** — 01 의 인공물은 모델 체적의 클러스터 통계이고
  01 은 `[인쇄]` 이 편이 재는 항(굴곡도·유효 전도도)을 **스스로 뺐다**; 이 편은 두께를 스윕하지 않고(110 · 155 µm 교락, 50 µm 한 셀) **1호를 인용하지도 않는다**(ref 41 = Bielefeld 2020).
  ★★★★ **리튬화 구배 = `η(z)` 몸통 + `θ` 형 모집단**(`[도표]` 80 % 조각 6 의 pristine 근처 봉우리), 측정 원리(식 S14 높이 가중평균)가 둘을 합침 — 전제 "same area" 는 Fig. S6 에서 깨짐.
  ★★★ `[재현]` **첫 사이클 비가역 ≈0.2 Δx 가 깊이 균일** ⇒ 두께 수송 아님; 코팅 쌍 −14 %. ★★★★ **D1**: 이온 쪽 `τ²` 4 값이 **ε_CAM 으로 계산**(4/4 ≤2 %) — "tipping point" ×1.6 ↔ 바른 ε ×0.92.
  ★★★ **σ_eff 로 비교하면 "굴곡도 진화" 는 80 % 셀 ≈3 배 하나**(LPSC COMSOL/EIS 0.93 · 0.34) — 압력(50/150 ↔ 100 MPa) · `ε` · 모델(OCP 없음) · 접촉 어느 쪽에도 배정; 옴 강하 차수로도 80 % 만 부족.
  **곱 축퇴 처방 여덟 번째 적용** — 1단계 ❌(상태축 0) · 2단계 ⚠(**코팅 쌍 = 화학 대조, 계보 첫**) · 3-a ❌ · 3-b ❌ · **4단계 ✅(70 % 통과 · 80 % 실패)**; 처방 표에 두 줄(코팅 쌍 · 두 영역 시편 조건).
  **채움표 24호 행 — 누적 ≈15.0 → ≈15.0 (새 칸 0).** 안 움직인 칸: Q1(`θ(N)` 0/24) · Q2(층) · **Q4 0/24**(열일곱 번째 성질 **"비식별을 물리로 읽었다"**) · Q5(아홉 번째 형태 "기준을 말하지 않는다") ·
  Q6 · Q8(NMC111 첫, OCP 0) · Q7(해당 없음). Q3 층 하나(같은 `τ²` 세 추정 병치).
  ⚠ 어긋남 17 건(D1 ε 규약 · D2 가중 전제 · D3 "<0.02" ↔ ≈0.04–0.07 · D4 Δx 인쇄 ↔ 그림 · D5 Li 함량 >1 · D9 모델 10 h ↔ 실험 6.6/7.5 h · D17 코팅 행 불일치).
  그림: 크로퍼 23장(본문 6 + SI 17) + **TOC 수동 1장 — 24장 전부 봤다, 안 본 것 0장**.
  컴파일: **새 개념 [[assb-tortuosity-factor-effective-conductivity-split]]** + 갱신 [[assb-lampe-contact-product-degeneracy]](여덟 번째 적용) · [[assb-apparent-capacity-decomposition]](`η(z)` · 관측 연산자) ·
  [[assb-interphase-vs-contact-loss-attribution]](코팅 쌍 첫 표본 · 세 번째 이름) · [[composite-cathode-percolation-utilization]](01 대질).
  후속 1순위 = **Bielefeld 2020 *ACS AMI* 12, 12821**(ref 41, 원장에 있음) · 2순위 = **Minnmann 2021 *JES* 168, 040537**(ref 42, 원장에 있음) · 3순위 = **Davis 2021 *ACS Energy Lett.* 6, 2993**(ref 39, 황화물 operando 광학 `η(z)`).
- **2026-09-23 (ingest 25, `assb` 25호 Zhou et al. 2025 · *ACS Energy Lett.* 10, 966−974)** — 큐 **24번**. UCSD + LG Energy Solution. DEM 브랜치 앵커 CSV 는 **읽지 않았다**(하드룰 1).
  큐 메모 *"Q1·Q6"* 중 **Q6 은 맞다**(운전 압력 3 점 × SE 입도 2 — 계보 첫 양극 쪽 요인 설계) · **Q1 은 계산뿐이다**(DEM 이용률, 측정 접촉량 0).
  ★★★★ `[재현]` **압력 손해의 초기분은 공통 모드(−26.5 ↔ −30.7 mAh g⁻¹), 미세구조는 감쇠의 압력 의존만 바꾼다**(fine −26/−27/−22 ↔ coarse −33/−38/−64). ★★★★ **DEM `θ` 는 겹침 손잡이 94 → 20 %**, 30/10 MPa 첫 충전 비 1.03 과 모순.
  ★★★★ **그림 무결성**: Fig. 3 DRT 12 곡선 중 5 개가 2 개(≤0.21 Ω) · Nyquist "2 MPa 1 뒤" = "30 MPa 100 뒤"(≤0.8 Ω) · S15 제목 반전 · 인쇄 유지율 6 중 2 재현 · 18/20/22 는 V–Q 판에서만(2 MPa 는 coarse 2 사이클 ↔ fine 1 사이클).
  ★★★★ **17호 함정 노출** — S19 에서 Li 계면이 가장 큰 항, 2 MPa coarse 전압 하강의 ≈80 %. ★★★ **5호 위 벽 반례 후보**(Li 금속 30 MPa ≈1500–1700 h, 같은 UCSD, 인용 0).
  **곱 축퇴 처방 아홉 번째 적용** — 1단계 ❌(`C` 미인쇄, τ 대리가 겹침·범례에 걸림) · **2단계 ✅(부분) SE 입도 쌍 + BET: C 비 1.7–2.5 ↔ 면적 예측 1.75 · BET 1.53** · 3-a ❌ · **3-b ✅(≈2–27 µF cm⁻²)** · 4단계 ❌;
  ★ 저자가 `C ∝ 면적` 을 스스로 인쇄한 첫 편 — 단 **입계(P1)** 에 걸어 벽돌층 모형과 방향이 반대(`[추론]`).
  **채움표 25호 행 — 누적 ≈15.0 → ≈15.5 (Q6 +0.5).** 안 움직인 칸: Q1(`θ(N)` 0/25) · Q2(층) · **Q4 0/25**(열여덟 번째 성질 **"민감도를 인쇄하고 그 손잡이로 검증을 맞췄다"**) ·
  Q5(열 번째 형태) · Q8 · Q7(해당 없음). Q3 층 둘(그림 자료 정체 불확실 · 암묵적 반복 ≈20 %).
  ⚠ 어긋남 22 건(D1–D3 그림 겹침·제목 반전 · D4–D7 인쇄 ↔ 그림 · D11 σ "very close" ↔ ×0.66 · D16 음극 없는 셀의 "음극" 봉우리 · D17 이용률 정의 둘 · D20 이론밀도 1.64 ↔ 1.86).
  그림: 크로퍼 25장(본문 4 + SI 21) + **TOC 수동 1장 — 26장 전부 봤다, 안 본 것 0장**; Fig. 2·3 은 벡터 좌표 추출.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](아홉 번째 적용 + 처방 표 한 줄) · [[assb-stack-pressure-operating-window]](요인 설계 · 5호 대질) · [[composite-cathode-percolation-utilization]](계산 `θ` 손잡이 · 첫 충전 시험) ·
  [[assb-apparent-capacity-decomposition]](공통 모드 · 율 극한) · [[assb-tortuosity-factor-effective-conductivity-split]](기하 τ = 계산, `σ_eff` 미측정).
  후속 1순위 = **Sakka 2022 *JMCA* 10, 16602**(ref 12, CT 로 압력별 접촉 면적 분율 — `θ(P)` 측정 후보) · 2순위 = **Shi 2020 *AEM* 10, 1902881**(ref 14, DEM 이용률 방법 원전, 원장에 있음) · 3순위 = **Xu 2024 *AEM* 14, 2303539**(ref 11, 요구치 출처).
- **2026-09-23 (ingest 26, `assb` 26호 Iwakiri, Delgado, Nogueira 2024 · *Electrochim. Acta* 508, 145202 · CC BY)** — 큐 **25번**("Q4 확인용"). NTNU + Simoldes Plásticos. 모델 편(빌린 Raijmakers 2020 박막 Li/LiPON/LCO 4 율 방전곡선).
  큐 표 낱말 지문(`identifiab` 0 · `uniqu` 0 · `sensitiv` 3 · `OCV` 0)은 **전수 재집계로 같다** — 그리고 `sensitiv` 3 = 제목 · Table 1 열 머리 · "less sensitive to air". 본문 이름은 "parametric study".
  ★★★★ **Q4 판정 — 0/26, 움직이지 않는다.** "sensitivity analysis" = 1C 전방 모델의 OAT 대역 스윕 + 설계 KPI; FIM · 조건수 · 프로파일 · CI 전수 0; 추정은 Nelder–Mead 점추정.
  ★★★★ 그러나 **추정 + 스윕이 같은 지면인 계보 첫 편**이라 비식별 방향 셋이 저자 그림에 있다 — Fig. 5a(`D_e⁻` 0 열) · Fig. 12a≡b(`k₁`↔`k₂`) · Fig. 3≡15(`D_M⊕`↔`a_max`, `[재현]` `x` 좌표 스케일 대칭).
  ★★★★ `[인쇄]` Table 3 `D_e⁻` **5.24×10⁻³ ↔ 문헌 5.06×10⁻¹³**(300 dpi 렌더 확인); `[재현]` 식 (30) 으로 문헌값이면 Fig. 5a · 5b 가 성립 안 한다 ⇒ **스윕은 표류한 적합점에서 돌았고 저자는 그 둔감을 물리로 결론에 올렸다.**
  ★★★ `[재현]` 적합 변수 10 중 **7 이 정확히 문헌 ×1.0500** ↔ `[인쇄]` "not fed into the optimization algorithm". ★★ 모델 1C = 1.23 mA(`Q_ideal` 기준, Fig. 4·9·13 으로 검산) ↔ 셀 0.7 mAh.
  **Q4 열아홉 번째 성질 = "평탄을 스스로 계산해 놓고, 평탄 위의 점을 값으로 인쇄하고, 그 점에서 본 둔감을 물리로 읽었다"**(24호 + 25호의 합성, 한 걸음 더 — 원전 수치만으로 비식별 재현 가능).
  반 칸 검토 후 접음 — 비식별을 **보인** 것은 우리 `[재현]` 이고 원전은 명제도 판정도 없다(10호 구분).
  **곱 축퇴 처방 열 번째 적용** — 1–4단계 전부 ❌(모델이 이중층을 가정으로 배제 · EIS 0 · 한 온도 · 펄스 0); "율 스윕" 줄은 데이터가 있고 분리 시험으로 안 씀; "`J^T J`" 줄은 열이 인쇄됐고 곱은 안 만듦.
  **채움표 26호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 하나(문헌 대조의 순환).
  ⚠ 어긋남 14 건(D1 `D_e⁻` 10 자릿수 · D2 ×1.0500 · D3 식 36 부피 누락 · D4 0.7 ↔ 1.23 mAh · D5 Fig. 5 ↔ 식 30 · D7 캡션 ↔ 본문 · D8 Fig. 16 ↔ 15 · **D9 Fig. 21 "Case 1.0" = Case 1.5**).
  그림: 크로퍼 21장 + 표 3 — **그림 21장 전부 봤다, 안 본 것 0장** (+ Table 3 p7 300 dpi 수동 렌더).
  컴파일: **새 개념 [[assb-sensitivity-sweep-vs-identifiability]]** + 갱신 [[assb-lampe-contact-product-degeneracy]](열 번째 적용 + 처방 표 한 줄).
  후속 1순위 = **Raijmakers 2020 *Electrochim. Acta* 330, 135147**(ref 10, 데이터 · 문헌값 · 평형 곡선의 단일 출처) · 2순위 = **Firouz 2020 *J. Energy Storage* 28, 101184**(ref 17, 인용 중 유일하게 제목에 "system identification") ·
  3순위 = **Deng 2021 *IEEE TTE* 7, 464**(ref 16, 축약 ASSB 모델) — 셋 다 원장 "구조적 공백 1번"(역문제·식별성 ASSB) 후보.
- **2026-09-23 (ingest 27, `assb` 27호 Sinzig, Schmidt, Wall 2024 · *J. Electrochem. Soc.* 171, 120519 · CC BY)** — 큐 **26번**("Q4 확인용"). TUM 계산역학 + TUMint.Energy. 모델 편(3D 입자 분해 ↔ 균질화 P2D, NMC622/LPS/Li, 실험 0).
  큐 낱말 지문(`identifiab` 0 · `uniqu` 0 · `sensitiv` 26 · `Sobol` 29 · `OCV` 0)은 **합자 그대로는 같다** — NFKC 정규화 뒤 `identifiab` **1**("phenomena … identifiable", 파라미터 뜻 아님). 지문 도구 맹점 = `ﬁ` 합자.
  ★★★★ **Q4 판정 — 0/27, 움직이지 않는다.** 전역 민감도는 제대로(Sobol 1·2·전차 + 95 % CI · GP 대리 · 150 표본 · 2¹⁴ MC); 26호 표로 **첫 줄의 전역판** + 새 줄 "모델 불일치 민감도" `|∇d_SOC|`. 묻는 것은 **모델 적합성**.
  ★★★★ 비식별 재료 셋(`S_T(D │ P2D) ≈ 0` · 두 모델 일치 영역 · `[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters")을 저자는 전부 적합성으로 읽었다.
  ★★★★ `[재현]` 벡터 좌표 — 그 상수(큰 `κ` 오프셋 0.068 · Fig. 7 150 점 평균 차 0.072)는 **비연결 몫 `1 − u` = 0.07**. 저자 배정 "insufficient homogenization strategy"; `u` 처방은 `[인쇄]` `A_el-c` 로 용량 깎기; 그 곡선(Fig. 3b 점선)은 **그림에 없다**(경로 전수 4 개).
  ★★★ `A_el-c` 의 세 겹 짐(면적 0.329 · 용량 0.344 · `u` 0.320) — `[재현]` 로그정규 실제 비표면적 0.216 의 ≈1.5 배. `D/d²`: `d̄` 는 개수 평균 6.85 µm ↔ `d₄₃` 12.9 µm(`(d₄₃/d̄)²` ≈3.5). `τ` = 24호의 `τ²`(이름 충돌).
  ★★ `[재현]` OCV 평탄 3.67–3.69 V @ `χ` 0.81–0.97 ↔ 하한 3.6 V ⇒ `SOC_end` 는 문턱 출력, "factor five"(`[재현]` 최대 6.4) 군집이 그 대역.
  **Q4 스무 번째 성질 = "적합성을 전역으로 재고, 그 안의 비식별 재료 셋을 전부 모델 적합성으로만 읽었다. 그리고 상수의 정체는 접촉 손실이었다."** 반 칸 검토 후 접음 — 데이터 0 · 단일 파라미터 · 대리모형 · 저자 판정 없음 · 결정적 그림 부재.
  **곱 축퇴 처방 — 적용 대상 아님(모델 편, 데이터 0)**; 모델 쪽 세 번째 표본(`A` 한 손잡이).
  **채움표 27호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 하나(모델 대 모델 참값 + CI 붙은 민감도).
  ⚠ 어긋남 15 건(**D1 Fig. 3b 점선 없음** · **D2 Fig. 13 ≈0 영역의 `D` 방향 반대** · D3 `m_SOC` 선형 ↔ `lg` · D4–D6 Sobol 서술 ↔ 그림 · **D7 Fig. 14a 점선 색 뒤바뀜** · D8 Fig. 14b 캡션 색 · D9 AM 비 0.4 ↔ 0.47 · D15 "factor five" ↔ 6.4).
  그림: 크로퍼 15장 — **15장 전부 봤다, 안 본 것 0장** (+ 쪽 렌더 26장 · 벡터 추출 Fig. 3b·7·9a·11a·14b).
  컴파일: 새 개념 0 · 갱신 [[assb-sensitivity-sweep-vs-identifiability]] · [[assb-lampe-contact-product-degeneracy]] · [[assb-tortuosity-factor-effective-conductivity-split]].
  후속 1순위 = **Khalik 2021 *J. Power Sources* 499, 229901**(ref 27, DFN 파라미터 그룹화 — 곱 쌍 도구 후보) · 2순위 = **Lu, Trimboli, Fan, Wang, Plett 2022 *JES* 169, 080504**(ref 28) · 3순위 = **Schmidt, Sinzig, Wall 2024 *JES* 171, 100502**(ref 18, resolved 모델의 박리 = 접촉 손실 기구).
- **2026-09-23 (ingest 28, `assb` 28호 Bizeray, Kim, Duncan, Howey 2019 · *IEEE TCST* 27(5), 1862 · ⚠ 액체셀)** — 큐 **27번**("방법론 원전 (액체셀)"). Oxford + SAIT. 선형화 SPM 의 구조적 · 실제적 식별성, 합성(LCO) + 실험(Kokam NMC 740 mAh) EIS.
  큐 낱말 지문 재집계 — `identifiab` 추출 그대로 **9 = 전부 대문자 쪽 머리글**, **NFKC 뒤 54**(본문 42). `OCV` 67 · `GITT` 2 · `sensitiv` 7 · `Sobol` 0 · `all-solid-state` 0. 합자 맹점이 IEEE 에도 있다.
  ★★★★ **Q4 판정 — ASSB 0/28, 도구 칸만 채운다.** 계보 첫 셋째 줄(식별성)이지만 액체셀이고, 식별 집합 `(τ_d⁺, τ_d⁻, R_ct)` 에 **용량이 없다**(`Q_th` → `β = dU/dQ` 기준극 입력, `x⁰` 가정). 보편 범위 명제("any lithium-ion battery model … flat OCV")는 동역학 파라미터에 관한 것 ⇒ 반 칸 검토 후 접음.
  **Q4 스물한 번째 성질 = "도구는 있고 대상이 없다."**
  ★★★ `[해석]` 묶음 대조: 26호 `k₁≡k₂` = 식 (50) 같은 구조 · 26호 `D_e⁻` 0 열 = 예외 1(`β = 0`) 같은 부류 · 다른 기구 · 26호 `D·a_max` = `θ₂ = τ_d/(3Q_th)` 같은 부류 · 27호 `1 − u` = `Q_th` 손잡이 같은 자리. **입자 통째 비연결 ≡ LAM**(SPM 묶음에서 항등).
  ★★★ `[재현]` Fig. 9 벡터 — "max 20 mV" 는 양의 최대, 적색 최소 **−42.9 mV**(RMS 10.3 ✓); ×0.78 사후 보정은 검증과 같은 데이터. `[재현]` Table I `D₊` 1.0×10⁻¹¹ 은 그림과 10³ 불일치(Fig. 1 점근선으로 판정 — 그림은 1.0×10⁻¹⁴).
  **곱 축퇴 처방 열한 번째 적용** — 1–4단계 전부 ❌(반원 설계상 제외 · 한 온도 · 셀 하나); 곱의 액체 SPM 원형은 식 18 · 26 에 있다.
  **채움표 28호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 하나(합성 참값 복원 — 같은 모델 · 무잡음).
  ⚠ 어긋남 8 건(D1 `D₊` ×10³ · D2 `τ_d⁻` 2841 ↔ ≈4000 · D3 `A` 이름·단위 · **D4 max 20 ↔ −42.9 mV** · D5 60000 ↔ 50 147 s · D6 둘째 최소 확인 불가 · D7 비독립 검증 · D8 `R_ct(DoD)` 를 비용으로 읽음).
  그림: 크로퍼 9 장 — **9 장 전부 봤다, 안 본 것 0 장** (+ Table II 쪽 렌더 · Fig. 9 벡터 추출).
  컴파일: **새 개념 [[spm-grouped-parameter-identifiability]]**(도구 페이지, `assb` 태그 없음) · 갱신 [[assb-sensitivity-sweep-vs-identifiability]] · [[assb-lampe-contact-product-degeneracy]].
  후속 1순위 = **Forman, Moura, Stein, Fathy 2012 *J. Power Sources* 210, 263**(ref 18, DFN 의 Fisher 식별성 — 정량 도구) · 2순위 = **Alavi, Mahdi, Payne, Howey 2016 arXiv 1505.00153**(ref 33, Randles 회로 식별성 — ASSB EIS 쪽 도구) · 3순위 = **Santhanagopalan, Guo, White 2007 *JES* 154, A198**(ref 30, 모델 판별).
- **2026-09-23 (ingest 29, `assb` 29호 Yanev, Auer, Pertsch, Heubner, Nikolowski, Partsch, Michaelis 2024 · *J. Electrochem. Soc.* 171, 050530 · CC BY)** — 큐 **28번**("`η(i)` 항 그 자체 + OCV 곡선 최유력"). Fraunhofer IKTS — **17호와 같은 연구실**(17호 = ref 21). 14 복합체 CA + 대칭 셀 EIS/TLM + GITT, 신품. **SI 미열람**(업로드 없음, IOP 접근 정책상 차단).
  큐 낱말 지문 재집계(NFKC 전/후): `identifiab` 0/0 · `uniqu` 0/0 · `GITT` 20/20 · `OCV` 0/0 — **큐 지문이 정규화 전후 모두 맞다.** 정규화가 바꾼 것은 `fit` 0 → 20 · `identif*` 1 → 4(일상어). 합자 `ﬁ` 99 · `ﬂ` 17. 식별성 신호는 지문 열에 없는 낱말 **`dependenc*` 2**(둘 다 적합 공분산 진단)에 있었다. ⚠ `LAM`·`LLI` 는 대소문자 구분 낱말로 0 — 무시하면 "ball-milled" 오검출로 18.
  큐 메모의 "GITT 로 재면서 OCV 곡선이라 부르지 않을 수 있다" 는 **반만 맞다** — GITT 는 `D` 다섯 점용이고 준평형 전위는 지면에 없다.
  ★★★★ **Q4 판정 — +0.5, ASSB 계보 첫.** `[인쇄]` sc90 `Q_M`·`α` "high dependencies close to unity in Table S2" · "Only the fit parameter n can be reasonably interpreted" = 저자가 돌린 공분산 진단 + 비식별 명제, 식별 집합에 용량 스케일 포함. `[재현]` 식 (2) 고율 극한이 `Q_M·α⁻ⁿ` 한 조합 — 정합. 반 칸 이유: SI 미열람 · 국소 · 축이 정적↔동적 · 진단 미전파(sc84 외삽 ≈236 이 "LIB 초과" 결론).
  ★★★ `[재현]` Table I: `ε` 역산 0.57/0.37/0.234/0.153(형상 공통 = 공칭) · `φ` 는 √ 로 13/14 행 정합 · **sc73-BM 행에 전사 오류 둘**(`φ` 70.8 ↔ 74.7, `τ` 2.6 ↔ 2.9) · sc84 `D` 표 ↔ 그림 불일치 · `σ_eff`–`D` Spearman 0.94. `[해석]` `n` = CA 누적 전하 시간 지수 → TLM √t 가 `n` 0.5 를 흉내 낼 수 있다(판별 안 함). GITT `D_app` = `D·(A_eff/V)²` = 28호 `τ_d` 묶음.
  **곱 축퇴 처방 열두 번째 적용** — 1단계 ❌(`C` 미인쇄) · **2단계 부분 ✅**(SE 입도 쌍 + BET: `φ` 비 1.02–2.29 < BET 비 3.7, 방향 통과) · 3단계 ❌ · 4단계 ✅ 자릿수 양립(CA `α` ↔ GITT `L²/D`, 같은 곱이라 일관성일 뿐). 처방 첫 줄("율 스윕, `i → 0` 포함")의 **계보 첫 실적용 + 실패 조건 인쇄**.
  **채움표 29호 행 — 누적 ≈15.5 → ≈16.0 (Q4 +0.5).** 안 움직인 칸: Q1(역산 둘, `θ(N)` 0/29) · Q2(반 칸 검토 후 접음 — LIB 기준 0.1 C, 이용률 ≈111 %) · Q5(열한 번째 형태 "검증 이식") · Q6 · Q7 해당 없음 · Q8. Q3 층 둘(fitted-extrapolated · derived-by-reference-ratio).
  ⚠ 어긋남 15 건(**D1 "175 and 195" 순서 반대 · D3 sc84 `D` 표↔그림 · D4 sc73-BM 두 칸 · D6 `Q_M` < 실측 저율 · D7 sc84 외삽 해석 · D9 sc90 무표시 작도** · D8 `n` 범위 밖 둘 · D13 단위 오기 · D15 master line = guide to the eye).
  그림: 크로퍼 7 장 — **7 장 전부 봤다, 안 본 것 0 장** (+ 식 1–5 렌더 · Fig. 2c/2d 확대). SI 그림 8 · 표 2 **못 봤다**.
  컴파일: 새 개념 0 · 갱신 [[assb-sensitivity-sweep-vs-identifiability]](둘째 줄 첫 수치) · [[spm-grouped-parameter-identifiability]](GITT = `τ_d` 묶음, `Q_M` ↔ `Q_th`) · [[assb-lampe-contact-product-degeneracy]](열두 번째 적용 · 새 줄 "외부 액체 기준 수입").
  후속 1순위 = **Tian et al. 2020 *J. Power Sources* 468, 228220**(ref 19, 식 (2) 와 `n` 배정의 원전 — TLM √t 대안을 다뤘나) · 2순위 = **Yanev et al. 2022 *JES* 169, 090519**(ref 20, 같은 방법의 ASSB 첫 판) · 3순위 = **이 편의 SI**(Table S2 dependency 값 — 반 칸의 근거 자체) · 4순위 = **Kaiser et al. 2018 *JPS* 396, 175**(ref 22, `τ` 식 · TLM).
- **2026-09-23 (ingest 30, `assb` 30호 Park 2024 · *Materials* 17, 5014 · CC BY · 단독 저자)** — 큐 **29번**("Q8 보조"). 홍익대. Li \| 소결 LATP 펠릿(150 µm) \| NMC111 슬러리 전극(0.57 mg cm⁻², SE 없음) 2전극 CR2032 + 액체 대조(표만). 주사율 CV(멱법칙 b · Randles–Ševčík · Dunn) + 율 스윕(블록당 ≈50 사이클). SI 없음.
  큐 낱말 지문 재집계(NFKC 전/후): `identifiab` 0/0 · `uniqu` 1/1 · `sensitiv` 1/1 · `GITT` 0/0 · `OCV` 0/0 — **정규화 전후 모두 큐 지문과 같다.** 합자 0 개, 정규화가 바꾼 문자는 `µ` → `μ` 3 개뿐. ⚠ 대소문자 무시 오검출이 크다 — `ICI` 21 · `MPa` 20 · `LLI` 2(대소문자 구분 낱말로는 0 · 1 · 0). `fit` 1 도 "bene-fits".
  ★★★★ **Q4 판정 — 0 (ASSB 누적 0.5 유지). 스물두 번째 성질 = "라벨이 자기 그림을 거스른다".** `[재현]` Fig. 3a·b·c 교차 판독 b: 산화 ≈0.58 · 환원 ≈0.73 ↔ 인쇄 0.76 · 0.58(네 곳). 전제가 배타인 두 모형(b ≠ 0.5 ↔ Randles–Ševčík)을 같은 봉우리 전류에 병치. 29호 뒤 두 번째 식별성 명제 없음.
  ★★★★ **Q5 — 열두 번째 형태 "방향 비대칭의 일방 배정".** Li 금속 "reference and counter", 방향 의존 관측을 양극 · LATP/NMC111 계면에 배정, 상대극 석출/박리 언급 0, Li/LATP/Li 대칭셀은 σ 한 값으로 소진. `[재현]` σ = 2.0 × 10⁻⁵ 는 펠릿 ∅ ≤ 20 mm 에서 ≥239 Ω 필요 ↔ 절편 ≈125 Ω ⇒ 호(입계 + Li\|LATP 계면) 포함 · 직렬 몫 ≈0.5–0.86 kΩ ↔ CV 봉우리 이동 ≈0.54–0.65 kΩ.
  ★★★ `[재현]` Table 1 "고체" 용량 90/54/28 ≠ Fig. 2a(고체셀) ≈61/40/10.5 = "액체" 행 61/40/11 · Randles–Ševčík 기울기 비² 1.94 ↔ 인쇄 `D` 비 1.97(같은 `A`·`C`) · 액체/고체 `D` 10.9 = 유효 면적 ≈3.3 배로도 설명 · Dunn 비(면적 소거)로는 저자 배정이 면적당 표면 용량 4.3 배를 요구 · 29호 식을 Fig. 2a 에 걸면 `Q_M` ≈63 · `n` ≈2.5(29호 해석 범위 밖) — `Q_M` 은 0.1 C 블록 −26 % 표류 **뒤의** 값 · "고율 뒤 비가역" 은 고율 전 표류 속도 이하.
  **곱 축퇴 처방 열세 번째 적용** — 1단계 ❌(양극 EIS 0) · 2단계 ❌(액체 대조 = 면적이 정의상 다른 대조) · 3단계 ❌ · 4단계 ⚠ 부분(Dunn `k₁/k₂` 면적 소거 조합, 긴장만). 처방 첫 줄에 **두 번째 실패 조건**(스윕 중 정적 용량 표류) · 외부 액체 기준 줄에 **반대 배정 표본**.
  **채움표 30호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 둘(label-contradicts-own-figure · textbook-equation-with-unprinted-inputs).
  ⚠ 어긋남 17 건(**D1 b 배정 반대 · D2 Table 1 용량 행 · D5 "activation" ↔ 봉우리 −62 % · D6 dQ/dV 는 손실 전 · D7 고율 귀속 · D9 Randles–Ševčík 전제 위반 · D11 σ 인용 없음·호 포함** · D8 축 단위 · D14 문단 중복 · D15 첫 CE ≤57 % 무논의 등).
  그림: 크로퍼 4 장 — **4 장 전부 봤다, 안 본 것 0 장** (+ Fig. 2a 확대 · Table 1 쪽 렌더). SI 없음.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열세 번째 적용) · [[spm-grouped-parameter-identifiability]](Randles–Ševčík 묶음) · [[assb-sensitivity-sweep-vs-identifiability]](세 줄 밖 표본).
  후속 1순위 = **큐 30 ICI 확산계수(*Nat. Commun.* 2023)** — 이 편 Randles–Ševčík `D` 의 대체 방법, `A` 처리와 2전극 상대극 처리를 본다 · 2순위 = **Nomura et al. 2019 *Angew. Chem.* 131, 5346**(ref 33, 공간전하층 실측 원전 — 이 편은 인용만) · 3순위 = **Yu … Wagemaker 2017 *Nat. Commun.* 8, 1086**(ref 6, 계면 수송을 따로 재는 방법).
- **2026-09-23 (ingest 31, `assb` 31호 Chien, Liu, Menon, Brant, Brandell, Lacey 2023 · *Nat. Commun.* 14, 2289 · CC BY · ⚠ 액체셀)** — 큐 **30번**("이 곡선이 얼마나 평형인가"). Uppsala Ångström + Scania. NMC811 | Li 링 기준극 | Li, 1 M LiPF₆ 3전극 파우치 ×2. 수정 GITT(600 s 펄스 · 1 h 휴지 · EIS) 로 GITT ↔ ICI ↔ EIS 대조 + 표준 ICI 55 사이클 + operando XRD. 본문 9 쪽 + SI 26 쪽 둘 다 전수. **보충 데이터 ZIP 미열람**(사용자 기계).
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): `GITT` 94 → **92**(94 는 부분문자열: `GITTin` · `GITT5`) · `ICI` 100 → **99**(100 은 대소문자 무시 — "simpl**ici**ty") · `open circuit` 5 ✓ · `equilibri*` 4 ✓ · `identifiab`/`uniqu`/`sensitiv`/`Sobol`/`OCV` 0. ★ **대소문자 무시 `ici` 는 NFKC 뒤 100 → 162** — 합자 `ﬃ`·`ﬁ` 가 `coefficient` 류 오검출 62 를 가리고 있었다(27·28호와 반대 방향: 이번엔 합자가 **오검출**을 막았다). `fit` 0 → 9 도 전부 합자 속. SI 는 합자 0, 수학 이탤릭 ≈150 자만 바뀜.
  ★★★★ **핵심 물음 판정 — ICI 는 곱 `D·(A/V)²` 을 가르지 않는다.** 식 19 에 `A` 가 제곱 입력, `A` = BET 1.5 m² g⁻¹ 상수 → 전부 `D` = **세 번째 배정, 첫 고지된 배정**(`[인쇄]` BET 고지 + 비교 한정). 봉인은 Fig. 7·8 · 결론의 절대 주장에서 풀린다. `[해석]` `u` 불변 · `φ²` 감응 · `R/k` 면적 소거 조합.
  ★★★ `[재현]` SI Note 1 한계 37.7 · 26.8 s · Note 2 12.8 s 전부 재현 — 단 "τ₁ > 1.27 r_p²/D is more likely" 는 자기 숫자(5080 s > 600 s)와 반대 · 면적 정의(BET ↔ D50 구)만으로 `D` ×2.52 > 방법 간 SD 0.56 · 길이 척도 둘(`r_p` 2 µm ↔ `3V/A_BET` 1.26 µm → 반무한 한계 ≈5.1 s, ICI 창 1–5 s 가 경계) · 방법 간 `D` SD = 2·√(0.26²+0.076²) = 0.54 ↔ 인쇄 0.56 · 신품 4.18 V `D` 골 = 기울기 ×0.36 ÷ `k` ×0.53 → 예측 ×0.46 ↔ 그림 ×0.36(`k` 는 오히려 준다) · Fig. 1 한 차단 `I` 0.056 mA → `k` ≈6.4 Ω s^-½ · `D` ≈5 × 10⁻¹² · Fig. 8 극값 한 면적 인자로 부분만 양립.
  **곱 축퇴 처방 열네 번째 적용** — 1단계 ❌(`C` 미인쇄) · 2단계 ❌(면적 대조 0) · 3단계 ❌ · 4단계 ✅ 양립(ICI ↔ EIS `k = σ√(8/π)` · `R` 일치 — 같은 곱이라 일관성). **새 줄 후보 `R/k`**(시간 영역 면적 소거, 조건: `R0` 제거 · 반무한 창 · ASSB 는 3전극 전제). 이 편 데이터로는 계산 불가.
  **채움표 31호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** 안 움직인 칸: 전부(Q1 `θ(N)` 0/31 · Q2 합 저항 · **Q4 ASSB 0, 스물세 번째 성질** · Q5/Q7/Q8 해당 없음 · Q6 없음). Q3 층 둘(measured-bundle-with-declared-constant · regression-SD-only error bars).
  큐 §6-3-c 대조: 액체 ✓ · 3전극 ✓(지면은 작업극만) · `A` 상수 ✓(★ 논문이 한 문장으로 다룸, 비교 한정) · ⚠ ICI 창 코드 0.1–0.9 s ↔ 지면 1–5 s(확인 불가) · ★ `SeqRef_003_1ph.csv` 스캔 13–14 동결은 **저자가 인쇄**("poor fit of the model" · 두 상) — 우리 "degeneracy 지문" 판독의 저자 이름은 **모델 오지정**이고 저자가 두 상 정련으로 고쳤다. 스캔 23–29 동결 · 둘째 `Rwp` 언덕은 **무언급**.
  ⚠ 어긋남 20 건(**D1·D3·D4 SI 그림 번호 오지시 셋 · D2 SD 0.086 ↔ 0.076 · D8 "no systematic error" ↔ 3.7–3.8 V 편차 · D9 Fig. 1 (c)↔(e) · D12 극값 시각 · D13 "uniformly" · D15 표준 ICI 무대조 · D19 단상 가정 ↔ 두 상** 등).
  그림: 크로퍼 26 장 — **15 장 직접 봤다**(본문 8 전부 + SI 8·10·12·13·15·16·18) + p.3 렌더 · Fig. 1c 확대. **안 본 것 11 장**(SI 1–7 · 9 · 11 · 14 · 17).
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열네 번째 적용 · `R/k` 새 줄 후보 · 세 번째 배정) · [[spm-grouped-parameter-identifiability]](ICI 행 · `u` 불변) · [[assb-sensitivity-sweep-vs-identifiability]](방법 간 일치 ≠ 인자 식별).
  후속 1순위 = **Geng, Chien, Lacey, Thiringer, Brandell 2022 *Electrochim. Acta* 404, 139727**(ref 19, 같은 그룹의 `D` 추정 타당성 — `A` 를 변수로 다뤘나) · 2순위 = **Chouchane, Primo, Franco 2020 *JPCL* 11, 2775**(ref 24, 메조스케일 유효 면적 → `D` 두 자릿수 흩어짐) · 3순위 = **zenodo 원자료로 `R/k` 계산**(사용자 기계) · 4순위 = **Xu et al. 2021 *Nat. Mater.* 20, 84**(fatigued 상 = 고 SOC 비참여 분율).

- **2026-09-23 (ingest 32, `assb` 32호 Biçer, Aksöz, Bakar, Odabaşı, Vonk, Soares 외 15 인 2025 · *Batteries* 11, 212 · CC BY · ⚠ Review, 1차 측정 0)** — 큐 **31번**("08 의 '접촉 손실 ↔ 보통 노화 분리 진단' 요구가 매단 유일한 인용"). Sivas + Kayseri + Siro(셀 제조사) + TechConcepts + Bozankaya(버스) + INEGI 외, EU Horizon "EXTENDED". 49 쪽(본문 42 + 참고문헌 160), SI 없음. 1차 전기화학 0 — 그림 12 장은 모식도 3 · 재수록 5 · 액체 LIB LCA 5(캡션 [151], 자체 계산 여부 미확정).
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): **11 열 전부 일치**(`identifiab` 0 · `uncertaint` 3 · CI/Bayes/posterior/calibrat 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 1 · `contact loss` 0 · `MPa` 0). NFKC 가 바꾼 문자 31 자(터키어 결합 부호 19 · `µ` 2) · **합자 0** → 정규화 전후 수 동일. 대소문자 무시 오검출: `LLI` 42 · `LAM` 28 · `MPa` 142 · `ICA` 380.
  ★★★ **8호 인용 대조 — 요구 (ㄷ) 가 원전에 없다.** 8호 §6.1 이 이 편에 매단 3 요소 중 (ㄱ) 압력 센서 ✅(`[인쇄]` p.27 "integrate pressure sensors and feedback control systems ... maintain optimal stack pressure") · (ㄴ) 압력 의존 임피던스 모델 ⚠(EIS 권고만, 압력 연결 0) · (ㄷ) **"contact loss ↔ ordinary electrochemical aging 진단" ❌**(`contact loss` 0 · `distinguish*` 2 회 무관). 큐 메모의 가설 확인 — **요구 명제의 첫 인쇄는 8호 자신**이다.
  ★★ 축 판정: **(a) BMS** — 관측 = V·I·T + 권고(압력 센서 · EIS · 서브셀 전류/온도), 구별 = **0**. "SSB 고유 열화" 는 **저항 증가 한 축**을 **추적**하라는 요구뿐이고, 접촉 불량의 결과를 `[인쇄]` "increased impedance, mechanical delamination, and eventual cell failure" 로만 적는다 — **분류 체계 네 번째 표본 "접촉 = 임피던스, 용량 몫 없음"**(12호 LAM ⊃ 접촉 · 13호 미배정 · 15호 어휘 미도입에 이어). 압력 센서는 **유지 수단**이지 진단 채널이 아니다(13호보다 한 층 얕다). **(b) 온도** — **0**: `Arrhenius` 0 · 열화 `Ea` 0; 열관리 = 열폭주 안전(DSC/ARC, [135] Wu 2021 재서술), 온도 → 열화 속도는 §7 한 문장(식·값·인용 0). **(c) 압력** — `pressure` 14 · `MPa` 0, 제조 압력 ↔ 운전 스택 압력 미구분, Table 8 은 스택 압력을 덴드라이트 억제에만 배정.
  ★★ `[해석]` **BMS 어휘의 두 전제가 식별성 물음을 지운다**: `[인쇄]` "well-established **linear** relationship between SoC and OCV"(p.23, p.24 의 "nonlinear" 와 자기 모순 D3) — 선형 OCP 에서 전극 스케일·오프셋은 한 조합 · `[인쇄]` SoC = "instantaneous capacity to its **rated** capacity" — SoC 와 SoH 가 한 숫자. 그리고 `[인쇄]` "SEI" = "solid electrolyte–electrode **interface**" 재정의(D9). ★ `[해석]` Fig. 3(bipolar 내부 직렬 "14.4 V")은 §4.1 토폴로지 전부의 전제(셀별 전압 접근)를 없앤다 — **셀별 OCV 곡선의 관측 가능성**이 식별성보다 먼저 온다(이 편은 안 묻는다).
  **채움표 32호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q1 0/32 · Q2 없음 · Q3 층 하나(**정의 없는 SoH + 정격 분모 SoC**) · **Q4 ASSB 0, 스물네 번째 성질 "선형 OCV 전제가 물음을 지운다"** · Q5/Q7 해당 없음 · Q6/Q8 칸 이동 없음.
  **곱 축퇴 처방 열다섯 번째 적용 — 적용 불가, 대상 없음**(1–4단계 전부 ❌: `C` 낱말 0 · 면적 대조 0 · `Ea` 0 · 시간 영역 0). `[해석]` 다만 이 편이 BMS 에 요구하는 센서(EIS · 온도 · 압력)가 처방 1 · 3-a 단계와 압력 되돌림 축의 **입력 채널**이다 — 번역은 우리 것.
  수치 표본 대조: 우리 위키가 원전을 가진 것은 **LGPS 전도도 하나**(10호 경유 Kamaya 12 mS cm⁻¹ ↔ Table 3 "~10⁻²–10⁻³" ✅). LGPS "운전 −30~100 °C · 180 °C 충방전"([4] 2022 학회 논문)은 Kamaya 측정 온도창(−110~110 °C)과 **양이 달라 대조 불가**. ⚠ 어긋남 13 건 + 사소: **D2 Fig. 6B 5.473 kJ/g → 본문 5473 kJ g⁻¹(×1000)** · **D3 OCV 선형/비선형** · **D4 산화물 전도도 10⁻⁵–10⁻⁷ ↔ Table 3 10⁻⁴–10⁻³** · D5 액체 분해 ~100 °C ↔ Fig. 4 ≈200–260 · **D6 "replacing SSEs with organic liquid electrolytes is necessary"(방향 반전)** · D7 약속된 식 0 · **D8 인용 불일치 12 건(제목 기준 — [123]/[124] 열관리 → 칼만 필터 · [122] 1998 → "recent" ML · [142] 2006 액체 분리막 → ASSB H₂S · [27] 태양전지 → 셀 밸런싱 등)** · D10 "Sulfite" · D11 Fig. 3 서술.
  그림: 크로퍼 20 장(그림 12 + 표 8) — **4 장 봤다(Fig. 1 · 3 · 4 · 6), 그중 3 장이 본문과 어긋난다**; 안 본 것 Fig. 2 · 5 · 7–12(우리 축 밖), 표는 텍스트로 대조.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열다섯 번째 적용 — 대상 없음 + BMS 센서 ↔ 처방 단계 대응표).
  후속: 참고문헌 160 편 중 **Q1 · Q4 · 곱 분리 · 기준극 누설을 채울 1차 후보 0 편**(제목 기준). 약한 후보 — **Celen 2021 IEEE SysCon**(ref 11, 160 편 중 유일한 ASSB-ECM 1차, 이 편은 재료 수치에 인용) · **Kan 2024 *Energy Storage Mater.* 68**(ref 124, 온도별 SSB — 축 (b) 의 `Ea` 후보, 종설). 압력 값은 **큐 32(Zhang 2025 저압 종설)** 가 받는다.

- **2026-09-23 (ingest 33, `assb` 33호 Zhang, Fu, Lu, Hu, Xia, Zhang, Wang, Zhou, Yan, Xia, Wang, Sun 2025 · *Adv. Mater.* 37, 2413499 · CC BY-NC-ND · ⚠ Review, 1차 측정 0)** — 큐 **32번**("Q6 주축 · 24 번과 짝"). EIT Ningbo + USTC + UWO. 22 쪽(본문 16 + 참고문헌 124 + 약력), SI 없음. 그림 8 장 전부 모식 · 재수록.
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): **11 열 전부 일치**(`contact loss` 4 · `MPa` 50 · 나머지 0). NFKC 변경 204 자(합자 `ﬁ` 83 · `ﬀ` 82 · `ﬂ` 21 · `ﬃ` 7 + 수학 이탤릭 10 + `¸` 1) — **지문 열은 전후 동일**, 열 밖에서는 합자가 `effect` 0 → 30 · `significant` 0 → 29 · `identif` 0 → 2(둘 다 식별성과 무관)를 가린다. 대소문자 무시 오검출 `LLI` 23 · `MPa` 81.
  ★★★ **판정**: Q6 칸 이동 없음(압력 수치 50 개 중 압력의 **함수** 0) · Q1 칸 이동 없음(`θ(N)` 0/33 · `θ(P)` 0) · **Sakka 2022 = [120] 인용, 단 "3D 접촉 · 압력 방향" 명제에, 수치 0** · **Xu 2024 = [11] 인용, 단 "hundreds of megapascals" 에만, "<≈1 MPa" 없음** · 제조 ↔ 운전 압력 **명시 분리 ✅**(종설 계보 첫).
  ★★★ **귀속 검사**: 8호 "pressure reduction = central commercialization problem (Zhang 2025)" ✅ 선다(32호와 반대) · 25호 짝 "인용 아님" ✅ — **양방향 시점상 불가** · 25호 "≤5 MPa" ❌ 이 편에서 오지 않음(이 편 2 MPa, 출처 없음) · 원장 "압력 수치 공급" ✅ 절반(값 ≈30 개, 함수 0).
  수치 표본 대조 7 건: 5호 Doux 3 건 ✅(>1000 h · 48 h/75 MPa · "hundredfold"·18 %; 5호가 짚은 92 h 근거 그림 문제를 그대로 물려받음) · 6호 Lee 방향 ✅ · 자기 Fig. 7B `[재현]` 65/96 %/−13 % ✅ · **23호 Koerver 2건 ❌**(접촉 손실 배정 뒤집음 D1 · 재활성 명제 원전 없음 G4).
  **채움표 33호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물다섯 번째 성질 "용량은 전략의 성적표" · Q3 층 하나(재수록 그림 출처 갈림 3/8) · Q6 층 둘 · Q8 입력 하나.
  **곱 축퇴 처방 열여섯 번째 적용 — 적용 불가, 대상 없음**(1–4단계 전부 ❌). `[해석]` 대신 교란 하나: 압력 축을 조작 변수로 쓰면 상대극 ΔP(0.7–2.3 MPa/사이클)가 같은 크기로 섞인다.
  ⚠ 어긋남 12 건: **D1 23호 배정 뒤집음** · **D2 Fig. 3I 출처 [63] ↔ [78] + "similar capacity" 가 ≈−10 % 를 덮음** · **D3 Fig. 2D μC "independent" ↔ 그림은 GC 와 같은 궤적** · **D4 "most labs 50–600 MPa"(출처 0, 우리 표본과 불일치)** · D5 Fig. 5 A/B 뒤바뀜 · D6 80 °C 출처 둘 · D7 Fig. 7C · D8 중복 참고문헌 2 쌍 외.
  그림: 크로퍼 9 장(그림 8 + 표 1) — **6 장 봤다(Fig. 1 · 2 · 3 · 4 · 5 · 7), 그중 4 장이 본문과 어긋난다(1 · 2 · 3 · 5)**; 안 본 것 Fig. 6 · 8, Table 1 은 텍스트 전사.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열여섯 번째 적용) · [[assb-stack-pressure-operating-window]](요구치 다섯 번째 · 제조/운전 분리 · 압력 진동 표).
  후속: **Sakka 2022**(지목 2 회, 여전히 `θ(P)` 유일 후보) · **Xu 2024**("<≈1" 확인처가 이 원문뿐 — 승격 제안) · **Koerver 2018 *EES***(4호 · 33호 지목 2 회 — 부피 곡선 + 압력 추적) · Gao 2022 *Joule*(2 MPa · 컷오프 → 부피 변화 ↔ 감쇠) · Cronau 2021(SE 압분, DEM 보정 후보) · Zhang 2017 *JMCA*(지목 3 회째). **Q1 · Q4 · 곱 분리 · 기준극 누설 1차 후보 0.**

- **2026-09-23 (ingest 34, `assb` 34호 Liang, Tao, Shi, Lyu, Ji, Dong, Mo 2026 · *npj Clean Energy* 2, 16 · CC BY-NC-ND · ⚠ Comment 5 쪽, 1차 측정 0, 데이터 0)** — 큐 **33번**("Q4 설계 축 — 우리 폭 측정기의 역방향"). UNSW + Chalmers + UTS. 그림 1 장(개념 모식), 식 0, 표 0. 자기 인용 8/32.
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): **11 열 중 9 열 일치 · 2 열 불일치** — `identifiab` 0 → **3**(+ 하이픈 분절 1 · `unidentifiable` 1) · `confidence interval` 0 → **1**. 둘 다 **정규화 전 0**(합자 `ﬁ` 67 자). NFKC 변경 76 자. ⇒ 큐 문서의 "`identifiab` 은 다섯 편 전부 0 회" 는 이 편에 대해 틀리다. 같은 검사를 31·32·34·35 원본에 걸면 `identifiab` 넷 다 0 → 0, **35 번 `confidence interval` 0 → 6**.
  ★★★ **판정**: 펄스가 처방의 **어느 단계도 명제로 실현하지 않는다** — 세 대역 이름(옴 · 계면 분극 · 확산 개시) + 신경망 재구성, `C` · 시상수 · 이완 · 조합 0(31호 `R_ICI` 보다 한 층 아래). `[해석]` 한 펄스 이완 = 1단계 τ 형 · 4단계 · `R/k` 의 공통 입력(조건: kHz 급 샘플링 · 2전극 합 · `C ∝ A` 전제 · √t 창 분리). OCV 분해에 대해서는 **대체 쪽**(IC/DV "정보 밀도 부족" → 재구성) + 불변량 예시 "active material stoichiometric limits"(α·β 의 양, 근거 0, Fig. 1b 열화 도메인과 긴장). ASSB 0 → 도구 칸. 32호 bipolar 적층과 무관(이름 충돌만).
  **채움표 34호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물여섯 번째 성질 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다" · Q3 층 하나(learned-reconstruction features, 제안형).
  **곱 축퇴 처방 열일곱 번째 적용 — 적용 불가(데이터 0), 대신 온보드 번역 한 줄**(한 펄스 이완 = 처방 공통 입력; 이 편의 재구성 · 불변 학습은 그 입력을 지우는 방향).
  ⚠ 어긋남 8 건: D1 반복 문장 셋 · **D2 확산 개시 < 10⁻¹ Hz ↔ "ms–s" 창** · **D3 화학량론 한계 "불변" ↔ Fig. 1b 열화 도메인** · D4 그림 ↔ 캡션 라벨 · **D5 "CRLB = FIM⁻¹"(특이 FIM 무언급)** · D6 ref 28 Li 금속 논문을 Li 이온 도금 방지로 인용 · D7 · D8 OED 현재형 ↔ 미래 과제.
  그림: 크로퍼 0 장(벡터 그림) → 수동 크롭 1 장 — **1/1 장 봤다**. 본문과 어긋난 것: 라벨 2 개(D4) · 기간 표기(D7).
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열일곱 번째 적용) · [[assb-sensitivity-sweep-vs-identifiability]](입력 설계 줄).
  후속(제목 기준, 미열람): **Jiang·Tao·Lee·Moura 2026 *Joule*** (ref 19, CRLB 정확도 한계) · **Li·West·Preindl 2023 *JPS* 580** (ref 24, 펄스로 열화 특성화) · **Tang 2023 *iScience*** (ref 21, 10 Hz 재구성 EIS) · **Yang 2024 *Science* 386** (ref 29, 접촉 복원 펄스 → 용량 회복, 액체 Si) · Tao 2025 *EES* (ref 14, degradation pattern decoupling). **Q1 · 곱 분리 · 기준극 누설 1차 후보 0.**

- **2026-09-23 (ingest 35, `assb` 35호 Roman, Saxena, Robu, Pecht, Flynn 2021 · *Nat. Mach. Intell.* 3, 447–456 · 본문 10 + SI 18 쪽 · ⚠ ML 방법 논문, 1차 실험 0, 액체 셀)** — 큐 **34번**("Q3 — 08 Table 2 에서 유일하게 신뢰구간 보고"). Heriot-Watt + CALCE + TU Delft. 179 셀(CALCE · NASA · TRI · Oxford), 네 알고리즘(BRR · GPR · RF · dNNe), 특징 30 → 18/5/5.
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): **11 열 중 10 열 일치 · 합자 가림 0**(NFKC 변경 본문 124 자 · SI 86 자, 지문 열 밖). `calibrat` 39 는 대소문자 무시 수(규칙대로 36). **큐 35 번 `confidence interval` 0 → 6 을 35 번 원본에서 직접 확인**(여섯 개 전부 `conﬁdence`, pp. 18–19) — 큐 표 정정.
  ★★★ **판정**: (a) 용량(Ah) 스칼라 하나 — 모드 분할 0, 차원 1 ↔ ≥3 · (b) 특징 = 충전 상단 0.3 V 창 · CV 꼬리의 범함수 → `[해석]` α·β 의 함수, 정규화 모양 특징은 균일 스케일에 불변 · 특징 공간 LLI ↔ LAM 축퇴는 다루지 않음 · (c) 불확실성 = **예측 오차 보정**(isotonic + 보정 전용 셀 + 90 % 적중률), 식별성 아님 · (d) 전부 실측, 역범죄 없음 — 대신 데이터셋 표지 · 과거 라벨 합이 선택된 입력. ASSB 0 → 도구 칸.
  **채움표 35호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물일곱 번째 성질 "불확실성을 보정했다 — 분해가 없는 스칼라 위에서" · Q3 층 하나(measured scalar label + held-out-recalibrated predictive interval).
  **8호 원장 정정 둘**: 보정된 불확실성 0/8 → **1/8** · "RMSE 0.45 % (best)" → dNNe RMSPE, 최저는 RF 0.14 %.
  **곱 축퇴 처방 열여덟 번째 적용 — 적용 불가(물리 모델 0), 경고 한 줄**(목표 주도 특징 선택은 분리 채널을 버린다).
  ⚠ 어긋남 21 건: **D1 그룹 ↔ 프로토콜 뒤바뀜** · **D2 초록 "best 0.45 %"** · **D3 결론 RMSPE 0.97 = 합 ÷ 2(`[재현]` 0.65)** · **D4 Group I 분할 23/10/5/19 ↔ `[재현]` 24/11/5/18** · **D5 셀 38 정체** · **D6 PEP 97.71 ↔ Fig. 2d** · D7 그림 번호 · D8 · D9 `C_score` 해석 · D10 단위 · D11 "unsupervised" · **D12 Fig. 1c 창 ≈0.09 V ↔ 0.3 V** · D13 SI 특징 표 · **D14 SI Fig. 10 캡션 a/b 뒤바뀜** · D15–D21.
  그림: 크로퍼 그림 18 + 표 11, 본문 Fig. 2 · 4 · 5 는 크로퍼가 놓쳐 수동 크롭 · Fig. 1 재크롭 — **9 장 봤다(본문 Fig. 1–5 · SI Fig. 4 · 8 · 10 · SI Table 2 쪽)**; 본문과 어긋난 것 Fig. 1(창 폭) · Fig. 2(PEP · 셀 정체) · SI Fig. 8(선택점) · SI Fig. 10(캡션).
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열여덟 번째 적용) · [[assb-sensitivity-sweep-vs-identifiability]](예측 보정 ≠ 식별성).
  후속(제목 기준): Kuleshov 2018(ref 62, 재보정 원전) · Richardson 2018 *IEEE TII*(ref 32, 같은 Oxford 데이터 GPR) · Birkl 2017 박사논문(SI ref 22, Group III 원 데이터 — 모드 분해와 같은 셀일 가능성) · Saxena 2008(ref 64, α-accuracy 원 정의). **Q1 · Q4 · 곱 분리 · 기준극 누설 1차 후보 0.**

- **2026-09-23 (ingest 36, `assb` 36호 Thelen, Huan, Paulson, Onori, Hu, Hu 2024 · *npj Mater. Sustain.* 2, 14 · Review 33 쪽 · CC BY · ⚠ 1차 측정 0, ASSB 0)** — 큐 **35번**("Q3·Q4 — 불확실성 보정"). Iowa State + Michigan + Argonne + Stanford + UConn.
  ★★★ **판정**: (a) aleatory/epistemic(→ model-form · parameter) 은 가르고 **식별성은 없다** — 사후 폭 = 예측 분포 또는 ML 가중치, 근최적 폭과 다른 대상 · (b) **확률적 모드 진단 1차 원전 0/13**, Fig. 4 도 Problem 4 만 점 · (c) **CI ⊂ PI ⊂ TI 정의**(35호 `μ ± 2σ` = PI) · (d) ASSB 0 → 도구 칸.
  **채움표 36호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물여덟 번째 성질 "불확실성의 분류학을 세웠는데, 데이터를 더 모아도 줄지 않는 파라미터 불확실성의 칸이 없다" · Q3 층 하나 · Q1 분류 체계 여섯 번째 표본("재작도가 연결을 지웠다").
  큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말 경계): NFKC 변경 684 자(합자 `ﬁ` 481). **정정 네 열** — `uncertaint` 205 → **180** · `Bayes` 53 → **35** · `posterior` 28 → **26** · `calibrat` 8 → **7**(큐 값은 공백 소실로 붙은 낱말까지 센 부분문자열 · 문서 전체 수와 정확히 일치; 35호의 "대소문자 차이" 추정은 절반만 맞다) · `confidence interval` **6** 확인(정규화 전 0) · `LAM` 5 는 규칙상 맞으나 가림(`LAMPE`/`LAMNE` 13, 접두 18) · 나머지 여섯 열 일치.
  **곱 축퇴 처방 열아홉 번째 적용 — 대상 없음**, 확률 도구 경고 둘(곱 방향 폭은 데이터량 불변 · 평균장 VI 와 상관된 사전이 폭을 지운다).
  ⚠ 어긋남 12 건: **D1 Fig. 3 캡션 "connections" ↔ 연결선 0** · D2 Severson "2021" ↔ 2019 · **D3 절 교차참조 5 곳 오지정** · D4 `2σ` ↔ 1.96 · D5 ARD `N` ↔ `D` · D6 isotropic · **D7 Roman "RF lowest accuracy" 그룹 의존** · **D8 CI 문단 내부 긴장** · D9 부트스트랩 반복 수 ↔ 구간 · D10 "2 % error" 대상 혼용 · D11 `θ̂_d` 글리프 · D12 모드 진단 절 담당 미기재.
  그림: 크로퍼 18 장(Fig. 2 · 9 제외) + Fig. 3 · 4 수동 재렌더 — **5 장 봤다(Fig. 3 · 4 · 7 · 13 · 15)**; 본문과 어긋난 것 Fig. 3(연결선 0) · Fig. 7(`2σ`). 안 본 것 Fig. 1 · 2 · 5 · 6 · 8 · 9 · 10 · 11 · 12 · 14 · 16–20.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](열아홉 번째 적용) · [[assb-sensitivity-sweep-vs-identifiability]](불확실성 분류 ≠ 식별성).
  후속(제목 기준, 미열람): **Gasper 2021 *JES* 168, 020502**(ref 52, 부트스트랩 파라미터 불확실성) · Gasper 2022 *JES* 169, 080518(ref 169) · **Thelen 2022 *ESM* 50, 668**(ref 81, 모드 진단 — 확률 여부 미확인) · **Ruan 2022 *Energy AI* 9**(ref 196, 상관된 모드) · Schmitt 2023 *JES(t)* 59(ref 192, 부분 창 모드 추정) · Dubarry 2017 · Costa 2022 · Lui 2021 · Pannala 2024. **확률적 모드 진단 · Q1 · 곱 분리 1차 후보 0. 큐 36 · 37 은 인용되지 않는다.**

- **2026-09-23 (ingest 37, `assb` 37호 Li, Fan, Zhang, Han, Wang, Liu, Jia, Guo, Zhu, He 2024 · *eTransportation* 20, 100315 · 본문 15 쪽 + SI .docx · ⚠ 모델 + 신품 실험, 노화 0)** — 큐 **36번**("9호가 모델 · PSO · `A_eff` 정의를 위임한 곳"). SJTU + Shanghai Firm-lithium(산업체, CRediT "Resources"). 9호와 저자 6/10 겹침.
  ★★★★ **판정**: (a) **표면 접촉 손실 `A_eff` 는 `LAM_PE` 와 다른 손잡이 — 용량(식 18) · 확산(식 15)에 없고 과전압에서 `k_p` 와 정확한 곱**; 입자 통째 비연결의 자리는 `ε_p`(= `LAM_PE`) 뿐 · (b) Table 1 각주 5 종, **`A_eff` · `ε_p` · `c_dl` 무표기 · `A_eff` 두 값이 9호와 네 자리 같다**, `k_p` 는 측정 범위 밖(≈0.25×) · (c) 식별성 명제 0, "sensitivity" = 0.4 C OAT · (d) 합성 truth 로 쓰면 두 갈래 동어반복.
  **채움표 37호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q1 `θ(N)` 0/37 · Q4 ASSB 0 스물아홉 번째 성질 · Q3 층 하나 · Q5 열세 번째 형태 "차감 흡수" · Q6 50 MPa 한 값.
  **9호 공백 대조**: G1 절반(반쪽전지 + 차감, 조건 0) · G2 부분(각주) · G3 이 편 셀 값은 인쇄(9호 비공개는 이 편 관행이 아니다) · G4 부분(목적함수) · 9호 "9 배"(`R_s` ↔ SEM)의 원천이 이 편.
  **곱 축퇴 처방 스무 번째 적용 — 원천 모델에 건다**: 1단계는 모델 구조(`c_dl` 면적 무관)가 막는다 · 4단계는 파라미터 통과 / 그림 실패(이완 ≈10² s ↔ `R·C` 1.5–7 ms) · 율 스윕 줄 **세 번째 실패 조건**(율별 재적합 파라미터).
  ⚠ 어긋남 14 건: **D1 `R_s` ↔ SEM** · **D2 `A_eff` 상속** · **D3 `k_p` 범위 밖** · D4 식 29 ×1.50 · D5 식 52 부호 + `D_SE` ×6.1(두께 미기재) · **D6 "minimal" ↔ ±40–60 mV** · **D7 이완 시상수 4–5 자릿수** · D8 `κ^p` 미정의 · D9 각주 c · D10 dQ/dV ↔ OCN · D11 검증 율 꺾임 · D12 "contact area" 이중 용법 · D13 Fig. 11f 잘림 · D14 이중층 결론 근거 그림 0.
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 1(확산계수 보정 — 불확실성 아님) · `LLI` 0 · `LAM` 0(접두로도 0) · `degradation mode` 0 · `contact loss` 0 · `MPa` 0(SI 1). NFKC 변경 8 자(`´`) — 열 변화 0. 소프트 하이픈 81(NFKC 가 안 지운다) — `identif*` 6 → 7.
  그림: 크로퍼 13 + SI SEM 1 — **8 장 + 표 1 봤다(Fig. 2 · 4 · 5 · 6 · 8 · 9 · 11 · S1 + Table 1 상단)**; 본문과 어긋난 것 Fig. 4b · 5c · 5d · 8a · 9c/f · 11b/e · 11f · S1. 안 본 것 Fig. 1 · 3 · 7 · 10 · Table 2 이미지 · SI 수식 WMF.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](스무 번째 적용 · 9호 `A_eff` 정정) · [[assb-sensitivity-sweep-vs-identifiability]] · [[spm-grouped-parameter-identifiability]].
  후속(제목 기준, 미열람): **Raijmakers 2020 *Electrochim. Acta* 330**(ref 14, 이중층 항의 조상 — `c_dl` 이 면적에 비례하나) · **Deng 2021 *IEEE TTE* 7**(ref 29, ASSB ROM) · Kim 2019 *Electrochim. Acta* 317(ref 21, ASSB 상태 추정) · Froboese 2019 *JES* 166(ref 30, `brug` 3.67 출처). 큐 37 · 38 인용 0.

- **2026-09-23 (ingest 38, `assb` 38호 Conforto, Ruess, Schröder, Trevisanello, Fantin, Richter, Janek 2021 · *J. Electrochem. Soc.* 168, 070546 · 12 쪽 · OA CC BY · SI 미수령)** — 큐 **37번**("Q1 을 깰 1 순위", **큐의 마지막 편**). JLU Giessen + TU Braunschweig, 분말 · 자금 Volkswagen AG.
  ★★★★ **판정**: (a) 사이클마다 **이완 OCP 두 점 → 활성 질량** · **저주파 EIS → 확산 경로 분포** 를 잰다 — 활성 질량은 `θ·ε_p` 합이고 용량 역산, 전부를 "We suggest" 로 접촉 손실에 배정(잔차 배정이 아니라 **합 측정 + 이름 붙이기**) · (b) 접촉 ↔ `LAM_PE` 실험 분리 0(보유 리튬 0 자 · 재가압 0 · LLI 는 Li 과잉으로 설계상 안 보임) · (c) SC ↔ PC 대조(입도 · 재소성 교락) · (d) 전자 비연결 → `C_diff` 질량(= `ε_p`), SE 접촉 · 균열 → `L_diff`, 반무한 꼬리는 `L/(C_diff√D̃)` 곱.
  **채움표 38호 행 — 누적 ≈16.0 → ≈16.5 (Q2 +0.5).** Q1 `θ(N)` 0/38(첫 `θ·(1−LAM)` 합 계열 1/38) · Q4 0/38 서른 번째 성질 · Q3 층 하나 · Q5 열네 번째 형태 "고정 전위가 게이지의 영점이다" · Q6 ≈70 MPa 한 값.
  ★★★ **9호 기각 대조**: 9호 "error … relatively large" ↔ 본문 "good agreement for all" ↔ `[도표]` Fig. 9 (a) +12…+27 · (d) −14…−28 mAh g⁻¹ — **9호가 그림에 맞다.** 이 편의 "fitting error is relatively large (Fig. S8)" 는 다른 문장이다.
  **곱 축퇴 처방 스물한 번째 적용**: 새 줄 "이완 OCP 두 점 = 연결 질량" + 경고 줄 "반무한 꼬리 곱 `L/(C_diff√D̃)`".
  ⚠ 어긋남 11 건: **D1 닫힘** · **D2 Fig. 9 가는 선 ↔ Fig. 6** · D3 SC "<2" ↔ 2.0 · **D4 Fig. 5d ↔ 9a 같은 조건 ≈37 mAh g⁻¹** · D5 `R_int` 라벨 · **D6 `C_diff/m` ×0.72** · D7 질량 >1 · D8 high-V "enhanced" · D9–D11.
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 2 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · **`contact loss` 13** · `MPa` 2. NFKC 변경 121 자(`ﬁ` 102 · `ﬂ` 5 · `˜` 14) — 열 변화 0. 소프트 하이픈 0 · 줄끝 하이픈 이음 열 변화 0.
  그림: 크로퍼 9 — **6 장 봤다(Fig. 4 · 5 · 6 · 7 · 8 · 9, Fig. 9 패널 확대)**; 본문과 어긋난 것 Fig. 9 · 8d · 5d↔9a · 7a · 6. 안 본 것 Fig. 1 · 2 · 3(모식 · 모사). SI 없음.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](스물한 번째 적용 · 표 두 줄) · [[spm-grouped-parameter-identifiability]](38호 두 행) · [[assb-li-in-reference-potential-window]](고정 전위 = 게이지 영점).
  후속(제목 기준, 미열람 — **큐 밖**): **Bartsch 2019 *Chem. Commun.* 55, 11223**(ref 47, operando XRD 활성 질량 — 같은 양의 OCV 독립 게이지) · Ruess 2020 *JES* 167, 100532(ref 19) · Fantin 2021 *Chem. Mater.* 33, 2624(ref 41, SC 재소성) · Lin 2014 *Nat. Commun.* 5, 3529(ref 14, 상전이 배제의 유일한 근거) · Schönleber 2015/2017(refs 32 · 31, DDC).

- **2026-09-23 (ingest 39, `assb` 39호 Sakka, Yamashige, Watanabe, Takeuchi, Uesugi, Uesugi, Orikasa 2022 · *J. Mater. Chem. A* 10, 16602–16609 · 본문 8 + SI 16 쪽 · CC-BY 4.0)** — 큐 **40번**(**2차 묶음 40~59 의 첫 편**, 원장 최상위 "`θ(P)` 측정 후보"). 리쓰메이칸 + Toyota(셀 설계) + JASRI/SPring-8 BL20XU.
  ★★★★ **판정**: (a) **X선 CT 로 접촉 면적 분율을 쟀다 — 표면 피복 `φ`**(NCM 표면 중 LGPS 와 닿은 몫), `θ` · `u` 아님 → 37호 기준 **`A_eff` 쪽 손잡이** · (b) **압력 축뿐**(0 · 6 · 12 · 50 · 100 MPa, 신품), **`θ(N)` 0/39**, 그 압력은 **제조 압력**(`[인쇄]` "no pressure was added during fabrication") · (c) 분할 문턱 미인쇄 · `[재현]` 분할이 고정 혼합물의 NCM/LGPS 부피비를 0.47 → 0.97 로 흔든다 · 0 MPa 에서도 `φ` ≈0.78 · (d) 같은 지면의 `R_ct` ×14 ↔ `φ` ×1.10 ⇒ `R_ct·φ` ×13.
  **채움표 39호 행 — 누적 ≈16.5 → ≈17.5 (Q1 +0.5 · Q6 +0.5).** Q2 반 칸 검토 후 접음(신품) · Q4 0/39 서른한 번째 성질 · Q5 열다섯 번째 형태 · Q3 층 하나.
  ★★★ **25호 ↔ 33호 인용 판정**: 둘 다 선다 — 25호 = 결과(Fig. 3c · 6b), 33호 = 결론 제언. ⚠ **25호 digest 의 "모델상 25 MPa 면 안정" 은 Sakka 에 없다**(Zhou 원문의 무인용 인접 문장 — 우리 오귀속).
  ★★★ **DEM 보정 목표**: 조건부 — 1순위 복합층 공극률(P) 5 점(인쇄 라벨 44 → 23 %) · 2순위 3 상 부피분율(질량수지 결함) · `φ(P)` 는 "0.5 µm 판정에서 0.75–0.85" 범위 제약 · 비등방성 정성. DEM/MPM 파일은 건드리지 않았다.
  **곱 축퇴 처방 스물두 번째 적용**: 2단계를 측정된 면적으로 건 첫 표본 — 면적 가설이 CT 척도에서 기각. 새 줄 "영상 면적 → `R·φ` 검사".
  ⚠ 어긋남 12 건: D1 Fig. 1 ↔ 2 · D2 Fig. 3b ↔ 3c · **D3 결론 방향 어휘 반전** · **D4 "≈10 %" ↔ 비단조** · D5 · **D6 질량수지** · **D7 S3 절대 ↔ 정규화** · **D8 고압 `R_ct` ↔ Nyquist ×2–3** · D9 "logarithmic" · D10 · D11 ref 23 = 41 · D12 셀 간 ≈30 %.
  낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 0 · **`MPa` 30**(SI 22). NFKC 변경 38 자(`ﬀ` 30 · `ﬃ` 7 · `ﬂ` 1) — 열 변화 0. `fi` 는 글리프째 소실 — `identi*` 1(무관). 줄끝 하이픈 이음: `stack pressure` 10 → 11, 지문 열 변화 0. 보조: `contact area` 13 · `tortuosity` 21 · `threshold` 0 · `error` 0.
  그림: 크로퍼 23 — **15 장 봤다(Fig. 1–6 · S1–S4 · S7 · S13–S16)**; 안 본 것 Fig. 7 · S5 · S6 · S8–S12. 본문과 어긋난 것 Fig. 3c · 3b · S3 · S15.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]] · [[assb-stack-pressure-operating-window]] · [[assb-pressure-reapplication-separation-test]].
  후속(서지 기준, 미열람 — **큐 41–59 에 없음**): **Wang · Kazyak · Dasgupta · Sakamoto 2021 *Joule* 5, 1371**(ref 22, "1 MPa practically" — 요구치 원전 지목) · **Ohashi … Hirai 2020 *JPS* 470, 228437**(ref 24) · **Ohashi … Hirai 2021 *JPS* 483, 229212**(ref 25) · Fathiannasab 2021 *JPS* 483, 229028(ref 18) · Doux 2020 *JMCA* 8, 5049(ref 15, 5호와 다른 논문).

- **2026-09-23 (ingest 40, `assb` 40호 Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2020 · *Electrochem. Commun.* 116, 106743 · 5 쪽 · CC BY · SI 없음)** — 큐 **41번**(2차 묶음 둘째 편, 지목 5 회 — 16 · 17 · 18 · 19 · 21호). Tokyo Tech + NEDO SOLiD-EV.
  ★★★★ **Q5 판정**: (a) **누설 0 · 드리프트 0**(`leak` · `drift` 0) — 원장 구조적 공백 3 그대로 · (b) 1.55 V = ref [11] Costard 2017(액체) 수입, 검증은 환산한 두 평탄 ↔ 문헌 [5,17] 일치 = P6 순환의 원전 확인 · (c) 19호 ±30 mV 의 근거 **없음** · (d) 두 가지가 만난다 — 인용([5] Nam 2018 · [6] = 20호) · 기각(Li-In 은 기준극 부적합) · 한 셀(Li-In 문헌값이 증인) ⇒ **열여섯 번째 형태 "상호 증언"** · (e) `[재현]` 증인 0.62 V 면 1.5745 V — 1.55 ↔ 1.57 불가분 · (f) 부호 오기 "−0.60 V vs Li"(축 +0.60).
  **채움표 40호 행 — 누적 ≈17.5 → ≈17.5 (새 칸 0).** Q5 · Q2 반 칸 검토 후 접음 · Q4 0/40 서른두 번째 성질 · Q3 층 하나(같은 상태 R3 세 값 ×1.49).
  **곱 축퇴 처방 스물세 번째 적용**: 3-a `Ea` ✅(재료만, `[재현]` 55.4 · 37.2 ✓) · 3-b `C₂` ≈23 nF ↔ 표면 산화물 귀속 긴장 · 4단계 ✅(Li-In DC ↔ EIS) · 새 줄 "3전극 옴 몫은 기준극 위치가 정한다".
  ⚠ 어긋남 6 건(D1 부호 · D2 [6] 은 LTO 를 안 쓴다 · **D3 R3 세 값** · D4 라벨 · D5 서지 · D6 "직선 이탈"). 다른 편의 인용 교정: 21호 "∼40 mV ∼110 Ω cm²" → 충–방 폭, 탈리튬만 ≈58–63 Ω cm².
  낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 0 · `MPa` 1. NFKC 변경 0 · 줄끝 하이픈 이음 열 변화 0. 보조: `leak` 0 · `drift` 0 · `assum*` 0 · `1.55` 1 · `30 mV` 0.
  그림: 크로퍼 3 — **3 장 다 봤다**(화소 판독: 1c · 1d · 2a · 2d · 3b · 3d). 본문과 어긋난 것 Fig. 1d(D1) · 2d/3b/3d(D3) · 3d(D6).
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]] · [[assb-lampe-contact-product-degeneracy]].
  후속: **Costard · Ender · Weiss · Ivers-Tiffée 2017 *JES* 164, A80**(ref [11] — 1.55 V 의 유일한 근거, 큐에 없음) · **Nam 2018 *JMCA* 6, 14867**(ref [5] — 큐 42) · Ender · Illig · Ivers-Tiffée 2017 *JES* 164, A71(ref [10]) · Braun 2018 *JPS* 393, 119(ref [28]).

- **2026-09-23 (ingest 41, `assb` 41호 Nam, Park, Oh, An, Jung 2018 · *J. Mater. Chem. A* 6, 14867 · 9 쪽 + SI 16 쪽 · CC 표기 없음)** — 큐 **42번**(2차 묶음 셋째 편, 지목 4 회 — 17 · 20 · 21 · 40호). Hanyang + UNIST, Hyundai Motor group 자금. **In 가지에서 가장 이른 편(2018-07).**
  ★★★★ **Q5 판정**: (a) 본문 0.62 V = ref 33 **Jung 2008 *AFM*** 수입(Santhosha 2019 이전 경로; 23호 "0.6 V" 의 ref 16 도 같은 Jung 연구실 종설) · (b) **SI Fig. S2 = 같은 설계 셀의 기준극 재료 교체(Li₀.₅In ↔ Li 금속)** — `[인쇄]` "marginal difference", `[도표]` Li 대비 CE 중점 ≈0.621 V · 두 셀 차 ≈2 mV — **P8 재료 축의 원전 실행, 수 미인쇄** · (c) 40호 "상호 증언" 의 In 쪽 끝 — 순환 밖 고리 하나(SI), 40호는 인용값만 가져가 "−0.60" 으로 옮김 · (d) **열일곱 번째 형태 "기준극 교체 대조"** + 가정이 컷오프를 정한다(WE/CE −0.62 V).
  ★★★★ **고갈층**: TOF-SIMS Li⁺ 단면 지도 한 쌍, `[인쇄]` "estimated to be 50 µm" ↔ `[도표]` 반값 깊이 ≈49 µm · 대조군 0 · 정량 0 · `In-rich` 0 회 · "insulating" 측정 0 · `[재현]` 전하 수지 완전 고갈 등가 ≈25–34 µm(자릿수 일치, 가정 넷). 21호 인용은 선다(정성), 조립 방향은 미시험(분말 CE).
  **채움표 41호 행 — 누적 ≈17.5 → ≈18.0 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/41 서른세 번째 성질 · Q3 층 하나(cutoff-identity terminal value).
  **곱 축퇴 처방 스물네 번째 적용**: 1–3단계 ❌(EIS 0) · 4단계 ⚠ 반전 계단 상한만 · 새 줄 "배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다 — 파생 채널 부호 판정은 계단 절반과 먼저 비교".
  ⚠ 어긋남 10 건: **D1 Table 1 행 이름 뒤바뀜** · **D2 컷오프 부호** · D3 Mo 박 ↔ Ti · **D4 Fig. 3c 항등식** · **D5 Gr < 0 V ↔ 계단** · D6 CE 양 규칙 두 문장 · D7 ref 35/36 다중 사용 · D8–D10 교차 편(40호 −0.60 · 17호 In-rich · 40호 1 C 선례).
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · **`calibrat` 1**(Q5 문장 — 기준 전위 환산) · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 0 · `MPa` 6(SI 0). NFKC 변경 57 자 — 열 변화 0; `fi` 일부 글리프 소실(`identiab` 0) · 줄끝 하이픈 53 곳 이음 열 변화 0. 보조: `leak` 1(연성 단락) · `drift` 0 · `assum*` 0 · `0.62` 4 · `ohmic` 0 · `overpotential` 0 · `In-rich` 0 · `insulat*` 1.
  그림: 크로퍼 20(S8 누락) — **8 장 봤다(Fig. 2–6 · S2 · S4 · S10)**, 화소 판독 S2 인셋 · 4a · 5b · S10b; 안 본 것 Fig. 1 · S1 · S3 · S5–S7 · S9 · S11–S14. 본문과 어긋난 것 Fig. 2c/2d/S2(D2) · 3c(D4) · 5b(D5) · S4a(D3) · 6(음극 ≈3.4–3.6 V 무언급).
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]] · [[assb-lampe-contact-product-degeneracy]].
  후속(서지 기준, 미열람 — **큐 43–59 인용 0**): **Jung, Lee, Kim, Kwon, Oh 2008 *AFM* 18, 3010**(ref 33 — 이 편 0.62 V 의 유일한 근거) · **Jung, Oh, Nam, Park 2015 *Isr. J. Chem.* 55, 472**(ref 9 — 23호 ref 16 과 같은 논문) · Zhang … Janek 2017 *ACS AMI* 9, 17835(ref 34 — In–SE 저주파 저항 방전 끝 증가) · Yu, Bates, Jellison, Hart 1997 *JES* 144, 524(ref 37).
- **2026-09-23 (ingest 42, `assb` 42호 Santhosha, Medenbach, Buchheim, Adelhelm 2019 · *Batteries & Supercaps* 2, 524–529 · 6 쪽 + SI 5 쪽 · CC 표기 없음)** — 큐 **43번**(2차 묶음 넷째 편, 지목 3 회 — 17 · 20 · 21호; 인용 6 편). FSU Jena(Adelhelm). 2019-03 게재 — 41호(2018-07)와 20호(2019-08 접수) 사이.
  ★★★★ **Q5 판정**: (a) **Li 금속 대비 — 액체셀**(1 M LiTFSI DOL/DME, Swagelok 3전극, 1 h 펄스 + 0.5 h 이완, 실온 수치 미인쇄, 곡선 1 개, `[인쇄]` "experimental data scatters") · (b) **평탄 창**: 0.622 V(그림) · ≈1–47 at%(`[도표]`) · InLi 단상 1.9 at% / −280 mV · 0.339 · 0.122 V · 평탄 안 이완 OCV ≈15 mV 처짐(`[도표]`) · (c) **열여덟 번째 형태 "다른 전해질의 원전"** — 두 가지 영점(R-LTO · In)이 둘 다 액체셀 측정 · 41호 ASSB SI 판독과 ≈1 mV · (d) 출생지를 "실온 · 조성 분해 · Li 대비 측정의 출생지" 로 좁힘(0.6 V 는 [17] Wen–Huggins · [18] Takada 1996 · [19] Webb 2014 가 앞선다).
  ★★★★ **21호 어긋남**: 대칭셀은 **InLi-(In) 조립**(In → Li 순 압착), ±1 mA cm⁻² × 1 h × 100 사이클 — 21호의 9 초와 전하 ≈2,600 배. 21호 digest 의 `[추론]` 대안(전기화학 리튬화분)은 **대칭셀 첫 반주기에 적용 불가**, 그런데 Fig. 3 시간 축이 ≈7 h 에서 시작. `[재현]` **셀 저항 12 Ω cm² < SE 옴 ≈400–570 Ω cm²(1/25–1/47)** — 이온 경로로 입증 안 됨, creep 의 강한 판(SE 우회)과 양립.
  ★★★ **계면 안정성**: Li-rich(≈75 at%) 80 → 200 mV · 200 Ω cm² — DC 분극만, 사후 분석 · 고체 EIS 0, 빨강은 ±0.2 V 한계에 눌린 모양(하한). `leak` · `drift` 0 — **누설 직접 측정 0/42**, 공백 3 그대로.
  **채움표 42호 행 — 누적 ≈18.0 → ≈18.5 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/42 서른네 번째 성질 · Q3 층 하나(charge-derived composition axis).
  **곱 축퇴 처방 스물다섯 번째 적용**: 1단계 ⚠ 액체 EIS R·C — 저자의 면적 설명("low remaining amount of In")을 C 가 ≈20 % 만 받친다 · 4단계 액체 ✅ / 고체 ❌ · 새 줄 "4단계를 SE 옴 하한과 먼저 대조한다".
  ⚠ 어긋남 13 건: **D1 전류 세 값** · **D2 대칭셀 < SE 옴** · **D3 SI 비 뒤집힘(1.23 = 1/0.81)** · D4 CPE_SL 동일 · D5 ΔrG · **D6 질량 ↔ 치수(44.1 ↔ 49.6 at%)** · D7 상도 참조 [9a] · D8 SI 공간군 · Arrhenius · D9 12 mV ↔ +15/−18 · D10 CuS 창 · D11–D13 교차 편(21호 "brittle" · 20호 x ≤ 1.0 · 17호 서지).
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 0 · `MPa` 0(SI 0). NFKC 변경 4 자 — 열 변화 0; `µ` · 반각 대시 · 음수 부호 추출 소실 · 줄끝 하이픈 34 곳 이음 열 변화 0. 보조: `leak` 0 · `drift` 0 · `assum*` 0 · `scatter*` 1 · `0.62` 6 · `ohmic` 0 · `creep` 0 · `brittle` 0 · `contact` 5("decontacting" 1).
  그림: 크로퍼 9(그림 6 · 표 3) — **그림 6 장 전부 봤다**(Fig. 1–3 · S1–S3), 원본 래스터 화소 판독 Fig. 1 · 2a · 3; 표 3 장은 텍스트로. 본문과 어긋난 것 Fig. 2 캡션(D1) · 3(D2 · D9 · 7 h 시작 · ±0.2 V) · S1(D8) · S2(D3) · S3(D10 · 중점).
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](42호 절 · 조건 (1) 원전 창 · 정의표 ② · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](스물다섯 번째 적용).
  후속(서지 기준, 미열람 — **큐 44–59 인용 0**): **Takada, Aotani, Iwamoto, Kondo 1996 *SSI* 86–88, 877**(ref 18 — ASSB 쪽 0.6 V 뿌리 후보, 20호 [20]) · **Wen, Huggins 1980 *Mater. Res. Bull.* 15, 1225**(ref 17 — 415 °C 0.5 V) · **Webb, Baggetto, Bridges, Veith 2014 *JPS* 248, 1105**(ref 19 — 실온 대조) · Sangster, Pelton 1991 *J. Phase Equilib.* 12, 37(ref 12a — 상도 원전 후보) · Wenzel … Janek 2016 *Chem. Mater.* 28, 2400(ref 16b).
- **2026-09-23 (ingest 43, `assb` 43호 Fukunishi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023 · *ACS Appl. Energy Mater.* 6, 10908–10917 · 10 쪽 + SI 9 쪽 · 오픈액세스 표기 없음)** — 큐 **44번**(2차 묶음 다섯째 편, 19호 지목). Tokyo Tech(Arai) — **18호(NCM523 JPS)와 다른 논문**, 흑연 \| LPSI 복합음극 · R-LTO 메시 3전극 · Li-In CE · 110 MPa · RT 1 C × 500 → **같은 셀** 333 K 1 C × 50.
  ★★★★ **음극 열화 배정**: 저항 분해 = 측정(Table 3 `R` · CPE-T · CPE-P 전후 ± · Table 2 `Ea` 전후) · 용량 → `LAM` = 해석(dQ/dV 높이 한 문장). `[도표]` 0.05 C 용량 ≈223 → ≈168(×0.75–0.78) · 봉우리 높이 비 0.53–0.70 · 0.21 V 봉우리 ×1.03 — 균일 비례 아님. `[재현]` `R_CT` `C_eff` 46 → 20 mF(×0.43 ± 0.2) ≈ 1/`R` ×0.47 · τ ×0.92 = 면적 서명 ⇒ 면적 > 용량 손실. 3-a 는 반대(`Ea` 22 → 27.5), 노화 뒤 세 `Ea` 27.5 수렴(무언급).
  ★★★ **Q5 판정**: 1.55 V = "Suppose" + [40,41](Colbow · Ohzuku — 18호 경로) · 증인 = 흑연 GITT 평탄 셋(문헌값 미인쇄) + Li-In "0.60"([44] = 42호, 원전 0.62 — D13) · **표류 ≈10 mV(인쇄) / 공통 모드 ≈−14 · −16 mV(`[도표]`)** — R-LTO 가지 첫 표류 값 · 안정성은 S2 합 일치로 "proves"(범주 오류) · `[재현]` R-LTO ≈1.568(세 번째 ≈1.57) · 2전극 컷오프 부호 오기(D7, 계보 세 번째).
  **채움표 43호 행 — 누적 ≈18.5 → ≈19.0 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/43 서른다섯 번째 성질 · Q3 층 하나(노화 전후 CPE 삼중 ± 완비).
  **곱 축퇴 처방 스물여섯 번째 적용(음극 첫 적용)**: 1단계 ✅ 완비(`R_CT` 면적 서명 · `R_X` P 오차로 미정) · 2단계 ⚠ 입도는 비가역 용량만 · 3-a ✅ 입력 / ❌ 1단계와 충돌 · 3-b ❌ `R_CT` `C` 20–46 mF = 이중층 ×270–3,200("전하이동" 네 번째) · 4단계 ✅(복합체 질량 읽기: 1.8 ↔ ≈1.5 mV — "3.0 mg" 모호성을 푼다) · 새 줄 "면적 서명 ↔ 저율 용량 비 대조(반쪽전지 음극)".
  ⚠ 어긋남 15 건: D1 293 ↔ 298 K · D2 28 ↔ 29.4 Ω · **D3 "doubled" ↔ ×1.60** · **D4 CPE_X-T "decrease" ↔ ×5.2** · **D5 `Ea` "nearly unchanged" ↔ +4.7 · +5.5** · D6 1 Hz ↔ 0.10 Hz · **D7 컷오프 부호** · D8 11.0 ↔ 11.2 µm · D9 절 번호 · **D10 RT "few changes" ↔ 1 C −21 %** · **D11 "every peak" ↔ ×1.03** · D12 Fig. 4 순서 · **D13 0.60 ↔ 0.62** · D14 서지 · D15 "proves the stability" ↔ "could be caused by the change of the R-LTO".
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 0 · `conf.interval` 0 · `Bayes` 0 · `posterior` 0 · `calibrat` 0 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 0 · `MPa` 2(SI 0). NFKC 변경 본문 0 · SI 36(전각 괄호) — 열 변화 0 · 줄끝 하이픈 23 곳 이음 열 변화 0. 보조: `leak` 0 · `drift` 0 · `Suppos*` 1 · `assum*` 1(피막, 기준 전위 아님) · `prove*` 1 · `capacitan*` 0 · `pressure` 0 · `"loss of the active material"` 1.
  그림: 크로퍼 16(그림 13 · 표 3) — **그림 9 장 봤다(Fig. 1 · 2 · 4 · 5 · S2 · S4 · S5 · S7 · S8)**, 화소 판독 1b · 4a · 4b · 4d · S7a; fig_S7 은 띠만 잘려 쪽 렌더로 봄. 안 본 것 Fig. 3 · S1 · S3 · S6. 본문과 어긋난 것 4d(D11) · 4 순서(D12) · S4(D7) · S7a(D10).
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](43호 절) · [[assb-lampe-contact-product-degeneracy]](스물여섯 번째 적용 · 처방 표 새 줄).
  후속(서지 기준, 미열람 — **큐 45–59 인용 0**): **Kuratani, Sakuda, Takeuchi, Kobayashi 2020 *ACS AEM* 3, 5472**(ref 24 — 흑연 void 형성, 음극 `θ(N)` 후보) · Otoyama … Tatsumisago 2018 *SSI* 323, 123(ref 25) · Lee … Ahn 2022 *ACS AEM* 5, 5227(ref 26 — 압력 crack healing) · Höltschi … Novák 2020 *JES* 167, 110558(ref 27) · Yu … Fukutsuka 2022 *Electrochemistry* 90, 037003(ref 30).
- **2026-09-23 (ingest 44, `assb` 44호 Jin, Park, Park, Lim 2015 · *Electrochim. Acta* 185, 242–249 · 8 쪽 · SI 없음 · © Elsevier)** — 큐 **45번**(2차 묶음 여섯째 편, 원장 "20호 셀의 원전"). 창원대 Lim + 세종대 Park — 20호와 같은 두 기관 · 같은 교신저자, 4 년 이르다.
  ★★★★ **20호 공백 대조**: G1 ✅ 양극 TiS₂ : SE : 탄소 = 50 : 50 : 0 wt%, `0.06 g` = 활물질(20호 R7 N/P 8.4 선다), 음극 도전재 0 · G2 ✅ σ 1.8 × 10⁻⁴ = 70:30 유리 30 MPa 펠릿 · SS 차단 · 1 kHz–7 MHz · 실온 · 절편 판독(`[도표]` ≈380 Ω → `[재현]` 두께 ≈1.05 mm; 두께 · 온도 · n 미인쇄) · G3 ⚠ 제조 30 MPa 인쇄, 운전은 Fig. 1 그림에만. **같은 셀 아님 — 같은 레시피**(SE 0.36 ↔ 1240 µm · 기준극 없음 · 창은 그림 1.1–2.4 V 로 일치). `[재현]` 20호 음극 = 단층 Li-Si(복합이면 ≥547 µm > 438) · 20호 R17 → 362 Ω 의 **46–69 %**(SE 겉보기 분율 0.54–0.56, TiS₂ 밀도 · 굴곡도는 가정).
  ★★★★ **GITT "effective contact area"** = `√D·S/θ` 곱을 대조 셀 가정으로 쪼갬 — Case 2 작업전극에도 전해질 없음(가정 근거 대칭) · 인쇄값 = 셋째 계단(`D` 2.50/1.66/1.01e-8 · `S` 4.13/3.67/3.18) · BET ×8.7 ↔ ×2.07 · `θ` 민감도 ×2.3–2.8 · r²/D ≈9 s ≪ 600 s(자기 "short diffusion path" 와 충돌) · Table 2 `ΔE_t` ↔ Fig. 6 ×≈2.
  ★★★★ **Li 재고 수지 위반**(`[재현]`): Case 6 x ≈1.37(2 사이클) · Case 4 ≥1.04(3 사이클) · Case 3 누적 — "탈합금화가 빠르다"(이 편 → 20호) 와 모순; 20호 셀은 수지 통과.
  **채움표 44호 행 — 누적 ≈19.0 → ≈19.0 (새 칸 0).** Q2 반 칸 검토 후 접음 · Q4 0/44 서른여섯 번째 성질 "대조 셀 가정으로 곱을 쪼갰다" · Q5 스무 번째 형태 "GITT `ΔE_s` 안의 상대극 평탄 가정"(`[도표]` 같은 화학 두 셀 이완 전압 ≈95 mV 차) · Q6 제조 30 MPa · Q3 층 하나(reference-cell-anchored product split).
  **곱 축퇴 처방 스물일곱 번째 적용**: 2단계 ✅(부분, SM 쌍 + BET — 계보에서 가장 이른 면적 대조군, 면적 가설 로그 ≈34 %) · 1 · 3단계 ❌ · 4단계 옴 하한 ✓(분리막 130 ↔ Fig. 9B ≈100–120 Ω) · 새 줄 "대조 셀 가정으로 곱 쪼개기(GITT)".
  ⚠ 어긋남 15 건: **D1 창 1–2.5 ↔ 1.1–2.4 V** · **D2 `ΔE_t` 표 ↔ 그림 ×2** · D3 Case 1 ↔ 3 · D4 150–210 ↔ 227 · **D5 수지** · **D6 Li₁₂Si₇ 저항률** · **D7 `S` 처리 비대칭** · D8 셋째 계단 · D9 반무한 · D10 기호 · D11 10⁻⁷ "similar" · D12 "no trend" ↔ ±25 % · D13 electrical ↔ ionic · D14 참고문헌(연도 · 권/쪽 · [16] = [32]) · D15 부피 변화 기대.
  낱말 지문(NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문): `MPa` 2 외 10 열 전부 0. NFKC 변경 40 자(`ﬁ` 32 · `ﬂ` 7 · `¼` 1) — 열 변화 0 · `µ` · 음수 지수 추출 소실(쪽 렌더 확인) · 줄끝 하이픈 19 곳 이음 열 변화 0. 보조: `leak` 0 · `drift` 0 · `assum*` 0 · `0.62` 0 · `plateau` · `flat` 0 · `indium` 4 · `contact area` 3 · `pressure` 2 · `obvious` 2 · `fit*` 0 · `Coulomb*` 0.
  그림: 크로퍼 12(그림 11 + 표 1) — **그림 11 장 전부 봤다**, 화소 판독 Fig. 6 인셋(`ΔE_s` 로 보정 검증). 본문과 어긋난 것 Fig. 1(운전 압력 그림에만) · 6(D2 · 95 mV) · 8/9C(D1 · D4 · D5 · D12) · 11A(D3).
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](스물일곱 번째 적용 · 처방 표 새 줄) · [[assb-li-in-reference-potential-window]](44호 절).
  후속(서지 기준, 미열람 — **큐 46–59 인용 0**): **Park, Song, Choi, Jin, Lim 2014 *JJAP* 53, 08NK02**(ref 20 — 자기 선행, Li-Si XRD · SEM · SM 입도) · **Liu … Wu 2005 *JPS* 140, 149**(ref 30 — "탈합금화가 빠르다" 의 유일한 근거) · Shen, Cao, Rahn, Yang 2013 *JES* 160, A1842(ref 29 — GITT 식) · Hayashi … Minami 2001 *J. Am. Ceram. Soc.* 84, 477(ref 28 — σ) · Asl, Keith, Lim, Zhu, Kim 2012 *Electrochim. Acta* 79, 8(ref 17 — 축 압력 의존).

- **2026-09-23 (ingest 45, `assb` 45호 Hertle, Walther, Mogwitz, Schröder, Wu, Richter, Janek 2023 · *J. Electrochem. Soc.* 170, 040519 · 9 쪽 + SI 5 쪽 · CC BY-NC-ND)** — 큐 **46번**(2차 묶음 일곱째 편, 원장 ★★★ "μ-RE 원본 — Q5 최대 공백", 16 · 21호 지목). JLU Giessen(Janek) + BASF — 16호(Marburg) · 21호(TUM)와 다른 연구실. Au 도금 W ∅10 µm μ-RE, In/InLi 상대로 1 µA × 8 h 리튬화.
  ★★★★ **Q5 판정**: 0 V = **도금 Li 상 정체**(Li 금속 대조 셀 없음) · Fig. 7 측정 축 **−618 mV vs In/InLi**(계보 첫 ASSB 안 인쇄 수) · `[도표]` 사다리 AuLi/AuLi₃ 개방회로 −0.485 ↔ 도금 −0.618 ⇒ **0.133 ↔ 문헌 0.134 V** · 안정성 "≥8 일"(그림 · mV 0, `drift` 0) · 점검 = 실험 사이 In/InLi 대비 + "refresh" · 누설 0/45 · `[재현]` 소진 가정 소비 ≈39 nA(12.5 µA cm⁻²) → (5′) ≥10 은 ≤ ≈19 h. **스물한 번째 형태 "셀 안 도금 Li — 영점을 상 정체로, 기준극을 소모품으로"**.
  ★★★★ **16호 이식 = 조건 밖**: ∅25 ↔ 10 µm · 면적당 0.27 ↔ 2.55 mAh cm⁻² · NMC 상대(사다리 판독 불가) · 평탄 무 · `[재현]` 도금 여분 ≤1.1 µAh(Li ≤0.55 µm, Au 분율 가정) · 수명 척도 ≤ ≈9 h. `[해석]` 16호 0.11 V 새 후보 = AuLi/AuLi₃ 칸(0.133 V)으로의 계단 이동.
  ★★★ **합 일치 검증** = 범주 오류 계열(DC · 위치 artifact 둘 다 합에서 안 보인다) · >10 kHz 편차 원인 원문 0(`[해석]` 기준극 채널 측정 artifact 후보 — 위치 artifact 는 합에서 상쇄) · 검증 셀(Fig. 10) ≠ 분석 셀(Fig. 5 · 11 · S7, `[재현]` 반쪽 합 96.5 ↔ 98 · 165 ↔ 165).
  ★★★ 2E 적합 비유일성 인쇄(`R_Anode` 14 ↔ 3.9) → `[재현]` S7 이 Fit 1 을 고름(저자 미판정) · 3E 양극은 TLM ↔ 직렬 둘 다 맞고 "physically meaningful" 로 선택. 율 시험: 2E 방전 부족 = LTO 상대극 Li 소진(0.1 C 165 ↔ 193, `[인쇄]` "side reactions that are consuming Li").
  **채움표 45호 행 — 누적 ≈19.0 → ≈19.5 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/45 서른일곱 번째 성질 · Q6 운전 63.7 MPa 명시 · Q3 층 하나(in-cell plated reference).
  **곱 축퇴 처방 스물여덟 번째 적용**: 1 · 2 · 3-a · 4단계 ❌ · 3-b ✅ 호 #1 배정 실패(≈10 nF ↔ 10–100 pF) · 새 줄 "합 일치는 분배를 검증하지 않는다 — 반쪽에만 있는 고주파 호는 3-b 로 먼저 거른다".
  ⚠ 어긋남 19 건: **D1 방전 순서** · **D2 컷오프 셋** · **D3 Li 두께 4.3/4/5 ↔ 6.9–11.7 µm** · D4 `Q_AuLi3` = 7 wt% · **D5 Chang 1.26 ↔ 12.6 %** · D6 적합 순서 · D7 Table S1 단위 · D8 TLM 표 부재 · D9 SI 결손 · D10 주파수 · **D11 "geometry unchanged" ↔ SE ×3.3** · **D12 검증 셀 ≠ 분석 셀** · D13 TSRE · D14 Fig. 7 캡션 · D15 환산 0.62/0.63 외.
  낱말 지문: `MPa` 7(제조 5 · 운전 2) 외 10 열 전부 0 · `leak` · `drift` · `calibrat` · `0.62` 0 · `618` 2 · `stable` 16(μ-RE 11, 수치 판정 0) · `refresh*` 2 · `ambigu*` 2 · `unequivoc*` 3.
  그림: 크로퍼 21(그림 20 + 표 1) — **15 장 봤다**(Fig. 1 · 3–13 · S1 · S5 · S7), 화소 판독 Fig. 7 · 10 · 13. 안 본 것 Fig. 2 · S2 · S3 · S4 · S6.
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](45호 절 · 조건 (9) · P10 · P11) · [[assb-lampe-contact-product-degeneracy]](스물여덟 번째 적용 · 처방 표 새 줄).
  후속(서지 기준, 미열람 — **큐 47–59 인용은 48 Solchenbach 하나**, 47 Schlenker 인용 0): **Solchenbach … Gasteiger 2016 *JES* 163, A2265**(ref 20 — 큐 48, 금선 선례 · Au–Li 평탄) · **Bach … Renner 2015 *Electrochim. Acta* 164, 81**(ref 33 — 134/215 mV 측정 원전) · Braun … Ivers-Tiffée 2018 *JPS* 393, 119(ref 38 — TLM) · Klink … La Mantia 2012 *Electrochem. Commun.* 22, 120(ref 19 — 3전극 artifact).

- **2026-09-23 (ingest 46, `assb` 46호 Schlenker, Stępień, Koch, Hupfer, Indris, Roling, Miß, Fuchs, Wilhelmi, Ehrenberg 2020 · *ACS Appl. Mater. Interfaces* 12, 20012 · 14 쪽 · SI 없음 · © ACS)** — 큐 **47번**(2차 묶음 여덟째 편, 21호 ref 17 · 원장 Hertle 행 병합). KIT IAM + Bosch + Marburg(Roling · Miß). Li\|Li₆PS₅Cl\|Li 대칭셀(Li ∅4 mm × 60 µm, 540 MPa 펠릿, 파우치 0.1 kN), Au 도금 W 선 매립 기준극.
  ★★★★ **Q5 판정**: 기준극 **썼다**(EIS 분할 전용) · 영점 값 · 리튬화 전하 · 선 지름 · 검증 · 표류 · 누설 **전부 0** — 스물두 번째 형태 "영점이 들어가지 않는 자리". **계보 최종 판정**: 21호 "Schlenker → Hertle → 16호" = 하드웨어 · 저자 줄(Marburg) + 영점 줄(Giessen) 의 16호 합류, 이 편은 0 V 의 출처가 아니다.
  ★★★★ **Q7 판정**: 수명 기구 = 저자 해석 "계면 면적 손실(void · 공공 확산) + 씨앗형 도금 → 국소 전류 → 덴드라이트", SEI 보류(XPS S 2p ≤6 at%), Li 소모 무관(`[재현]` 순 이동 ≤3 %). 단락 = "sudden voltage drop" 한 기준 · `[도표]` 붕괴 여러 계단 · 단락 전 계단 ×≈0.7 감소 — 연성 단락 배제 0, 대칭셀은 개방회로 서명 없음. CE 통로 없음.
  **채움표 46호 행 — 누적 ≈19.5 → ≈19.5 (새 칸 0).** Q5 · Q2 반 칸 검토 후 접음 · Q4 0/46 서른여덟 번째 성질 · Q6 층 하나(감압 이력, 다른 SE) · Q3 층 하나.
  **곱 축퇴 처방 스물아홉 번째 적용**(음극 계면): 1 · 3-a ❌ · 2단계 ⚠(면적 비대칭 셀 · 압력 — 판독이 R·C 아님) · 3-b 판정 불가(규격화 면적 미인쇄) · 4단계 ✅ 부분(`[재현]` DC 77–117 ↔ EIS 합 ≈24 Ω cm² — ≥2/3 가 0.1 Hz 아래) · 새 줄 "역방향 반쪽 짝".
  ⚠ 어긋남 16 건: **D1 Fig. 1 J·t 본문 ↔ 캡션** · **D2 Fig. 4b 축 "µm" = 분** · **D3 Li 면적 0.126 ↔ `[재현]` ≈0.16 cm²** · **D4 "10^10 F/cm²"** · **D6 Fig. 1e ↔ Fig. 8** · D7 "medium current density" · D8 Fig. 11 패널 · **D9 Fig. 6 단위 · α** · D10–D16.
  낱말 지문: `contact loss` 1(Li 음극) · `MPa` 14 외 9 열 전부 0 · `leak` · `drift` · `calibrat` · `Coulomb*` · `soft` · `dead` 0 · `SEI` 30 · `dendrit*` 27 · `contact area` 19 · `interface area` 14.
  그림: 크로퍼 11 — **7 장 봤다**(Fig. 1 · 2 · 3 · 4 · 6 · 7 · 8), 안 본 것 Fig. 5 · 9 · 10 · 11(모식도 · 형태 영상). 렌더 확인 p3 · p5.
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](46호 절) · [[assb-lampe-contact-product-degeneracy]](스물아홉 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 47 행 + 지문 ¹².
  후속(서지 기준, 미열람 — **큐 48–59 인용 0**): **Kasemchainan … Bruce 2019 *Nat. Mater.* 18, 1105**(ref 13 — 임계 박리 전류 · void) · **Krauskopf … Janek 2019 *ACS AMI* 11, 14463**(ref 14 — 공공 · 압력 ↔ 경도) · Wenzel … Janek 2018 *SSI* 318, 102(ref 38 — 아지로다이트 \| Li 계면층) · **Bron, Roling, Dehnen 2017 *JPS* 352, 127**(ref 45 — Roling, 혼합 전도 계면층 임피던스) · Wang, Sakamoto 2018 *JPS* 377, 7(ref 51) · Xu … Greer 2017 *PNAS* 114, 57(ref 54).

- **2026-09-23 (ingest 47, `assb` 47호 Solchenbach, Pritzl, Kong, Landesfeind, Gasteiger 2016 · *J. Electrochem. Soc.* 163, A2265 · 8 쪽 · SI 없음 · CC BY · ⚠ 액체셀)** — 큐 **48번**(2차 묶음 아홉째 편, 21호 ref 11 · 45호 ref [20]). TUM(Gasteiger). Swagelok T-셀 · LP57 · Au ∅50 µm + 폴리이미드 7 µm, 절단면만 노출 · 150 nA × 1 h.
  ★★★ **Q5 판정**: 0.311 V = **Li 금속 대비 측정**(액체 Li\|Li) · LixAu(0 < x < ∼1.2) 첫 단 OCV · >500 h 추적 `[도표]` 20 h 뒤 ≈3 mV(인쇄 < 2 mV, D1) · 40 °C 리튬화 −1–2 mV · 25 → 40 °C ≈60 h 이탈 · 재리튬화 복원 · 누설 0/47(`[재현]` < ≈0.27 nA) — **스물세 번째 형태 "원전 측정 + 영점 사용 조건"**. **0.31 V ↔ 0 V = 같은 선의 맨 위 · 맨 아래 칸.** 45호 "134 / 215 mV [20]" 은 지면에 없음(D6).
  ★★★ **21호 교정 이식 판정**: 가져간 것 = 값(두 자리) + 절차 · 원전 조건 둘(노출 ×40 · 2 h 판독) 이탈 · 장기 안정성은 21호 자기 측정 — 틀렸다는 증거 없음, ASSB 검사 없음. 원장 "액체 값을 ASSB 로" 는 정밀하지 않다(21호 이식은 ASSB 안). "CE 거칠어짐" = "We believe"(셀 1, `[재현]` 0.77 nm).
  ★★ **3전극 아티팩트**: 원전 기구는 표류(≲1 Hz, PEIS 에서 완전지까지) · 위치(기하) 둘 — **45호 >10 kHz 편차의 원인 후보 추가 0**.
  **채움표 47호 행 — 누적 ≈19.5 → ≈19.5 (새 칸 0).** Q5 반 칸 검토 후 접음(액체) · Q4 0/47 서른아홉 번째 성질 · Q3 층 하나 · Q2 해당 없음(도구 칸).
  **곱 축퇴 처방 서른 번째 적용**(액체, 도구 칸): 1단계 ✅ τ 형 면적 서명(Li\|Li) · 3-b ✅ "전하이동" ×700–1000 실패(다섯 번째, 첫 액체) · 2단계 ⚠ 새 줄 "외부 기준 줄의 다섯 번째 배정 — 연구 간 비교"(`[재현]` 거칠기 비 4.2 ↔ `R_CT` 비 3.2–6.0).
  ⚠ 어긋남 12 건: **D1 20 h ↔ ≈3 mV** · **D2 "quickly" ↔ 수백 h** · **D4 "essentially identical" ↔ −9 / −21 %** · **D5 같은 상태 흑연 호 ×0.63** · **D6 134 / 215 mV 부재(교차 편)** · **D7 "∼5-fold" ↔ 4.2** · D8 · D9 · **D11 x ≤ 1.2 ↔ 축 확산 느림** 외.
  낱말 지문: `MPa` 1(압연) 외 10 열 전부 0 · `calibrat` · `leak` · `pressure` 0 · `drift` 11 · `0.311` 6 · `artefact` 7.
  그림: 크로퍼 8 — **8 장 다 봤다**, 화소 판독 Fig. 2b · 2c · 5 · 6a.
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](47호 절 · 조건 (10)) · [[assb-lampe-contact-product-degeneracy]](서른 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 48 행 + 지문 ¹³.
  후속(서지 기준, 미열람 — **큐 49–59 인용은 52 Illig 2012 하나**): **Bach … Renner 2015 *Electrochim. Acta* 164, 81**(ref 25 — 칸 값 두 표의 원전) · Bach … Renner 2016 *Chem. Mater.* 28, 2941(ref 30) · Ender, Weber, Ivers-Tiffée 2012 *JES* 159, A128(ref 14) · Dees, Jansen, Abraham 2007 *JPS* 174, 1001(ref 15) · Victoria, Ramanathan 2011 *Electrochim. Acta* 56, 2606(ref 17).
- **2026-09-23 (ingest 48, `assb` 48호 Dugas, Dupraz, Quemin, Koç, Tarascon 2021 · *J. Electrochem. Soc.* 168, 090508 · 9 쪽 · SI 없음 · © ECS)** — 큐 **49번**(2차 묶음 열째 편, 21호 ref 16). Collège de France(Tarascon). 축대칭 기밀 3전극 셀(∅8 mm) · **전면 Li₀.₅In : SE 60 : 40 기준층**(링 = 15 µm Al 집전체) · WE LTFS · NMC622 · TiS₂ · SE β-Li₃PS₄ / Li₆PS₅Cl · CE Li₀.₅In(Li₀.₉In) 복합 또는 Li 박 · 제조 4 t · 운전 1 t cm⁻²(Li 셀 45 kg cm⁻²).
  ★★★ **Q5 판정**: 영점 = 인용 622 mV(42호)를 **2전극 귀속 전제로 한 번** · 3전극 축은 끝까지 "vs LiIn/In"(환산 0) · 기준극 Li₀.₅In `[재현]` 33.3 at%(42호 창 안; CE Li₀.₉In 47.4 at% = 창 끝) · `[인쇄]` CE 창 ±160 → ±20 mV + **"20 mV ↔ ⩽2 mA h g⁻¹ … 2 electrodes … can safely be employed"** — **스물네 번째 형태** · 안정성 "hundreds of hours"(TiS₂ 680 h 곡선 겹침, 수 0) · 누설 0/48 · `[도표]` Fig. 10a Li 박 상대극 휴지 끝 −0.62 ± ≈0.01 V vs LiIn/In(우리 판독 — 41호 SI 에 이은 두 번째 ASSB 안 그림 판독, 45호 인쇄 −618 보다 앞).
  ★★★ **기하**: 21호 "circular … RE around the outer perimeter" = **집전체를 기준극으로 읽음** — 원장 · 21호 digest 문구가 물려받음. `[해석]` 기준극이 전류 경로 안 — 합금 ≈28–32 vol% → 쌍극 교환 가능성(C/20 급 mV 이하 추정, 측정 0) → 개념 페이지 조건 (11). 분배 대조 `[도표]` 고주파 절편 WE 쪽 283 · CE 쪽 ≈296 Ω cm² ↔ SE 40 : 45 mg — 근사 통과.
  ★★★ **21호 인용 셋**: 기하 ❌ · "LF changes upon lithiation and delithiation are expected" ⚠ 약한 판(Li-In = 방향 무관 시간 단조 성장, `[도표]` 꼭짓점 670 → 44 → 54 → 5.6 mHz; 방향 의존은 Li 금속) · 음극 저주파 호 = 전하이동 ❌(이 편 Li 저주파 호 = "resistive layer", Li-In 배정 0). 21호 자기 모순 "In:Li 1:2 (In1Li0.5)" 기록.
  ★★★ **2전극 재구성 = 비식별성 시연**(검증으로 쓰지 않음 — 45 · 43 · 40호의 합 일치 "validating" 과 범주 대조): WE 모형이 합을 "satisfactory" 적합, 중간 호 139 → 307 Ω cm² · "cannot be decorrelated". 검증은 양의 Im 호 부재 한 기준 · **기준극 없는 2전극 셀 EIS 대조 0**(셀은 지면에 있었다).
  **채움표 48호 행 — 누적 ≈19.5 → ≈20.0 (Q5 +0.5).** Q4 0/48 마흔 번째 성질 · Q3 층 하나 · Q6 층 하나(압력 단정 교락) · Q1 · Q2 없음.
  **곱 축퇴 처방 서른한 번째 적용**: 1단계 ❌(`C` 없음) · 2단계 ⚠(볼밀 ↔ 손 분쇄 = 면적 · 화학 교락) · 3-b ✅ 느린 "전하이동" 두 호 `[재현]` ≈33 mF · ≈0.2–0.3 F cm⁻² 실패(여섯 번째 계열) · 볼밀 NMC 7.6 µF cm⁻² 통과 · 4단계 ✅ 부분(Li CE DC ≈2–6 ↔ EIS ≈0.5–1.2 kΩ cm²) · 새 줄 "호 제거 검정 + 2전극 합 재구성".
  ⚠ 어긋남 15 건: **D1 "1.9 mS cm⁻¹" ↔ 자기 β-LPS ≈0.2(×10)** · **D2 "33%" ↔ 23 %** · D3 4,670 ↔ 그림 ≈4,490 · **D4 "Fig. 6c" = Fig. 8c** · D6 "20%" ↔ 14 % · **D7 540 ↔ 그림 670 mHz** · **D8 "simply originates from … pressure"(음극 교체와 교락)** · **D9 "superimposed" ↔ 사이클별 다른 패널** · D12–D15 교차 편(21호 기하 · 전하이동 인용 · 1:2 · 원장 문구).
  낱말 지문: `calibrat` 1(토크 ↔ 압력) · `MPa` 0(t cm⁻² 6 · kg cm⁻² 3) 외 9 열 0 · `leak` · `drift` · `assum*` 0 · `expect*` 4 · `622` 1 · `artefact` 5 · `decorrelat*` 1.
  그림: 크로퍼 10 — **10 장 다 봤다**, 화소 판독 Fig. 3a · 5c · 7 · 9a · 10a.
  컴파일: 새 개념 0 · 갱신 [[assb-li-in-reference-potential-window]](48호 절 · 조건 (11) · P8 · P11) · [[assb-lampe-contact-product-degeneracy]](서른한 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 49 행 + 지문 ¹⁴.
  후속(서지 기준, 미열람 — **큐 50–59 인용 0**): **Costard … Ivers-Tiffée 2017 *JES* 164, A80**(ref 15 — "ideal geometry" 근거, 40호 1.55 V 근거와 같은 편: 두 번째 지목) · Ender, Illig, Ivers-Tiffée 2017 *JES* 164, A71(ref 6) · Klink … La Mantia 2012 *Electrochem. Commun.* 22, 120(ref 5) · Kasemchainan … Bruce 2019 *Nat. Mater.* 18, 1105(ref 8) · Marchini … Tarascon 2020 *ACS AMI* 12, 15145(ref 18) · Kaiser … Roling 2018 *JPS* 396, 175(ref 23).
- **2026-09-23 (ingest 49, `assb` 49호 Barai, Uddin, Widanage, McGordon, Jennings 2018 · *Sci. Rep.* 8, 21 · 13 쪽 · SI 없음 · CC BY · ⚠ 액체셀)** — 큐 **50번**(2차 묶음 열한째 편, 20호 ref [24]). WMG Warwick. 상용 20 Ah LFP/흑연 파우치 · 50 % SoC · 25 °C · 4 h 휴지 · DC 단일(5 C × 18 s) · 다중 진폭(1 · 2 · 5 · 15 C × 10 s) · 전환 · 1 kHz(Hioki) · EIS(10 mHz–100 kHz, 0.2–1.4 A) · 펄스-다중사인(2차 ECM).
  ★★★★ **판정**: 총량은 **같은 양의 다른 창**(`[재현]` 5 C `ΔV/ΔI(t)` ↔ EIS |Z|(t = 1/f) −6 … +11 %) · 성분 이름은 **창 경계의 규약**(`R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13, EIS `R_p` 경계만 ×3.9) · 옳은 창은 `R₀` 에만("after 4ms" = Im Z = 0, `[해석]` 배선 의존) · 10 Hz 장비 `R₀` +43 % = |Z|(10 Hz).
  ★★★ **식별**: 비유일성 두 곳(ECM "not uniquely identifiable" · DC "inability to completely separate", `R_p` "pre-defined") → 결론이 지움("EIS can accurately provide separation and identification") — **Q4 마흔한 번째 성질**. `[해석]` 적합된 직렬 R = 여기 대역 위쪽 끝의 |Z|(다중사인 `R₀` 1.62 = |Z|(1 Hz)).
  ★★★ **20호 대조**: 가져간 것 = 모양 규칙(원전 Fig. 1 모식의 선형 외삽 작도 · 본문 "shallow, linear") · 두고 온 것 = 시간 규약(0.1 · 2 · 10 s) · 조건(5 C ↔ C/72, 50 % SoC · 4 h 휴지 ↔ 구간 시작 · 20 min) — `R_CT` 창 ×≈1.4–2.2 × 10³. "작도다" 판정은 원전에서도 선다. 작도 규약의 출처는 원전 ref 8 Waag 2013(20호 [25]).
  ⚠ **결론 긴장**: "not the non-linearity" ↔ 10 s 창 진폭 ×1.46 · 대진폭 다중사인 −24 % @ ≈0.017 Hz · 다중사인 총 2.83 은 ECM ω→0 외삽(최저 여기 점 ≈1.98).
  **채움표 49호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/49 마흔한 번째 성질 · Q3 층 둘 · Q2 해당 없음(도구 칸).
  **곱 축퇴 처방 서른두 번째 적용**(액체, 도구 칸): 1 · 2 · 3-a ❌ · 3-b 판정 불가(면적 미인쇄) · 4단계 ✅ 총량(성분은 원문이 "not meaningful") · 새 줄 "창 규약".
  ⚠ 어긋남 15 건: D1 Table 2 캡션 · 율 수 · D2 1.71 ↔ 1.72 · D3 EIS `R₀` 시간 <0.001 ↔ 4 ms · **D4 Re ↔ |Z| 혼용(0.01 Hz 2.94 = |Z|, Re ≈2.62)** · **D5 결론 "separation and identification" ↔ "not well-defined"** · **D6 "not the non-linearity" ↔ 진폭 ×1.46** · D7 EIS 진폭 무관 = 소신호 범위 · D8 `R_D` ↔ `R_p` · D9 기호 누락 · **D10 0.01 Hz ↔ ≈0.017 Hz** · D11–D15.
  낱말 지문: `identifiab` 3(파라미터 뜻 2) · `uncertaint` 1(열량계) · 나머지 9 열 0 · `timescale` 20 · `window` 0 · `pre-defined` 3 · `ambigu*` 3 · `contact` · `pressure` 0.
  그림: 크로퍼 7 — **7 장 다 봤다**, 화소 판독 Fig. 5a · 5b · 6a · 7b.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른두 번째 적용 · 처방 표 새 줄) · [[assb-sensitivity-sweep-vs-identifiability]](49호 절) · 큐 문서 §6-3-g 50 행 + 지문 ¹⁵.
  후속(서지 기준, 미열람 — **큐 51–59 인용 0**): **Waag, Käbitz, Sauer 2013 *Applied Energy* 102, 885**(ref 8 — 작도 규약 출처, 20호 [25] 와 같은 편: 두 번째 지목) · Schweiger et al. 2010 *Sensors* 10, 5604(ref 22) · Widanage et al. 2016 *JPS* 324, 61 · 70(refs 21 · 20) · Barai et al. 2015 *JPS* 280, 74(ref 18) · Smith & Wang 2006 *JPS* 161, 628(ref 28).
- **2026-09-23 (ingest 50, `assb` 50호 Miß, Ramanayagam, Roling 2022 · *ACS AMI* 14, 38246 · 본문 9 쪽 + SI 8 쪽)** — 큐 **51번**(2차 묶음 열두째 편, 16호 ref [30]). Univ. Marburg. 단결정 LCO(LiNbO₃ ≈12 nm) · NMC 83\|6\|11(LiNbO₃ 1 wt%) \| 0.67 Li₃PS₄·0.33 LiI(0.8 mS cm⁻¹) \| In, 70 : 30 · 탄소 0 · 389 MPa · 두께 4 점(계산값) · SOC50 · 2 사이클째 EIS 0.1 MHz–0.5 mHz · 음극은 In–Li 대칭셀(40 at% · 125 MPa)의 절반을 뺌 · TLM(Huang–Zhang) + CPE + 수정 (ii).
  ★★★★ **판정**: 면적 = 완전구 기하 `a_v = 3ε/r`("in contact to SE", `r` = SEM 공칭 확인) — **`j₀` 와 면적을 가르지 않았다**, 저자 틀에서 `j₀` 는 접촉을 품는다 · 두께 가변은 `R_ion` ↔ `R_CT` 만(NMC 전이 통과 · LCO 전부 두꺼운 극한) · `[재현]` 수정 (ii) = `j₀` ×τ 재척도(식 1 이면 LCO 4.2 · NMC 0.016).
  ★★★ **비교**: LCO ↔ NMC `j₀` 25.8 ↔ 0.11(×235) — `[재현]` τ_CT ×106 · `C_eff` ×2.2 ⇒ 면적 서명 아님(견딘다) · 16호 ↔ 이 편 NMC τ ×1.28 ⇒ 면적 서명(16호 SE 전도도 서사가 곱을 안 가름) · 액체 대비 "2 orders" 의 ×6.1 이 규약 · Bielefeld 2022(큐 57) 10⁻⁵ A cm⁻² = 0.1 A m⁻² ≈ NMC 0.11(지면 논의 0). 3-b ✅ 4.4 · 2.0 µF cm⁻².
  ★★★ **16호 대조**: `r_CAM` 공칭 확인(NMC 는 `[도표]` ≈1–2 µm 결정립 응집체) · 초기값 문헌 + 1/30 C · `ε` 0.505/0.495 = 이 편 **LCO** 칸 · "기공 구조" 이유는 16호의 것 · 16호 공백 "비교 대상 `j₀`" = 0.11(×12.1).
  **채움표 50호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/50 **마흔두 번째 성질** · Q5 **스물다섯 번째 형태**(반 칸 검토 후 접음) · Q3 층 하나(simulation-matched).
  **곱 축퇴 처방 서른세 번째 적용**: 1단계 ✅ 완비(같은 지면 · 편 간) · 2단계 척도만 · 3-a ❌ · 3-b ✅ · 4단계 ❌ · 새 줄 "면적 정규화 규약".
  ⚠ 어긋남 14 건: **D1 첫 방전 "good agreement … 180−200 · 190−200" ↔ `[도표]` ≈170 · ≈171** · D2 입경 3–6 ↔ 4–6 µm · D3 공극 이중 처리(×1.1) · D4 `j₀` 0.113 ↔ 0.11 · D5 σ 20 ↔ 25 °C · **D6 SI σ_ion ⇒ τ ≈3.0 ↔ 6.8** · **D7 과차감(Fig. 5a)** · D8 "freely adjustable" ↔ Table 2 · **D9 LCO 모형 두께 추세 "unclear"** · D10 221 µm 모의 ≈94 ↔ ≈82 · D11 Fig. 5b 비단조 · D12 압력 한 점 · D13 refs 30 = 33 · D14 오기.
  낱말 지문: `identifiab` · `uncertaint` · `calibrat` · `LLI` · `LAM` · `contact loss` 0 · `MPa` 8(SI 1) · `simulat*` 19 · `fit*` 4(`j₀` 밖) · `contact` 9.
  그림: 크로퍼 15(+ 표 4) — **12 장 봤다**(Fig. 2–8 · S2 · S3 · S5 · S6 · S7), 안 본 것 Fig. 1 · S1 · S4 · 식은 쪽 렌더로.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른세 번째 적용 · 처방 표 새 줄) · [[spm-grouped-parameter-identifiability]](50호 두 행) · 큐 문서 §6-3-g 51 행 + 지문 ¹⁶.
  후속(서지 기준, 미열람 — **큐 52–59 인용: 57 Bielefeld 2022 만**): **Kaiser … Roling 2018 *JPS* 396, 175**(ref 24 — τ 시작값 · 대칭셀 TLM, 다시 지목) · Cronau … Roling 2020 *Batter. Supercaps* 3, 611(ref 36 — 두께 가변 TLM 원형) · Morasch … Suthar 2021 *JES* 168, 080519(ref 34) · **Hess … Cuniberti 2015 *JPS* 299, 156**(ref 31 — 비교 기준 LCO 0.4 A m⁻² 의 규약) · **Minnmann … Janek 2021 *JES* 168, 040537**(SI ref 4 — 원장 TLM 원전) · Huang & Zhang 2016 *JES* 163, A1983(ref 46) · Kroll … Tallarek 2021 *JPS* 505, 230064(ref 37 — 공극 10 %).
- **2026-09-23 (ingest 52, `assb` 52호 Oh, Kwon, Choi, …, Choi 2025 · *Adv. Energy Mater.* 15, 2404817 · 본문 10 쪽 + SI 28 쪽)** — 큐 **53번**(2차 묶음 열넷째 편, 13호 [34] · 14호 [10], 14호와 같은 연구실). MgSiGr(Mg 200 nm 스퍼터 위 SiGr 0.8 mg cm⁻²) 과충전 음극 \| LPSCl \| LiNbO₃-NCM811 · 제조 150/380 MPa(펠릿) · WIP 450 MPa 75 °C(파우치) · 운전 20 · 3 MPa(스프링) · 파우치 3 MPa(볼트 3.5 N·m) · 25 °C · 2전극만.
  ★★★★ **판정**: 운전 압력 명시 · 제조와 분리 — **압력 비교 없음**(두 점이 적재 20 ↔ 6 mg · N/P 0.15 ↔ 0.66 과 교락, 반쪽 압력 미인쇄) · 저압 지배 인자 "음극 계면" = 3 MPa 고정 음극 교체로만 · MgSiGr 저압 감쇠 원인은 해석 한 줄 · 양극 관측 0 · 제목의 두 조건(N/P 0.15 + 3 MPa)은 한 셀에서 안 만난다.
  ★★★★ **용량 제한 전극 · 배정 없음** — `LLI` · `LAM` 0 · 방전 끝 전극 판정 불가(α · β 전제). ★★★★ `[재현]` **CE ≠ `LLI`**: 20 MPa ∏CE 0.55 ↔ 83.7 % · 3 MPa 누적 결손 ≈575 mAh g⁻¹ > Li 재고 ≈275 · 면적당 ×≈1.8(CE ×≈7 은 적재 정규화).
  **채움표 52호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q6 반 칸 검토 후 접음 · Q4 0/52 **마흔네 번째 성질** · Q3 층 하나 · Q1 · Q2 · Q7 없음.
  **곱 축퇴 처방 서른다섯 번째 적용**: 1–4단계 전부 ❌(양극 채널 0) · 새 줄 "누적 충–방 결손 ↔ Li 재고 상한 · 관측 손실 대조".
  ⚠ 어긋남 14 건: **D1 제목 두 조건 비동시** · **D2 완전지 N/P 재현 불가(675 ↔ ≈890 mAh g⁻¹)** · **D3 `R_B` 감소 = "tolerance" ↔ S17 병렬 경로** · D4 "much lower" ↔ 두 기공 지도 · **D5 3 MPa CE 무언급 · 결손 > 재고** · **D6 99.2 % ↔ 83.7 %** · D7 13호 [34] 약한 판 · **D8 압력 "Precise control" ↔ 상수 · 변환 0(토크 `[재현]` 17–29 MPa @4 cm²)** · D9 S18 N/P 0.32 ↔ 0.22 · D10 3 MPa MgSiGr 첫 용량 < Li 10 µm · D11 277 ↔ S11B CV 640 · D12 파우치 ≈45 % 미인쇄 · D13 방전 용량 "증가" = 연성 단락 · D14 Li 층 ≈9 ↔ ≈16 µm.
  낱말 지문: `identifiab` · `uncertaint` · `calibrat` · `LLI` · `LAM` 0 · `contact loss` 1(음극) · `MPa` 13(SI 2) · `dead` · `reservoir` · `inventory` · `leak` 0 · `retention` 1.
  그림: 크로퍼 34(본문 7 + SI 25 + 표 2) — **14 장 봤다**(Fig. 1–6 · S11 · S15 · S17 · S19 · S23 · S25 · 표 S1 · S2), 화소 판독 Fig. 4D · 6D, 안 본 것 20 장(Fig. 7 · S1–S10 · S12–S14 · S16 · S18 · S20–S22 · S24).
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른다섯 번째 적용 · 처방 표 새 줄) · [[assb-stack-pressure-operating-window]](52호 절) · [[anode-free-li-inventory-accounting]](52호 절) · 큐 문서 §6-3-g 53 행 + 지문 ¹⁸.
  후속(서지 기준, 미열람 — **큐 54–59 인용 0**): **Oh … Choi 2024 *Energy Storage Mater.* 71, 103606 · Oh … Choi 2023 *AEM* 13, 2301508**(refs 12b · 12c — 같은 연구실 압력 편) · **Menkin … Grey 2024 *Faraday Discuss.* 248, 277**(ref 23 — 연성 단락 병렬 저항 틀) · Chen … Li 2021 *ACS AEM* 4, 4879 · Yan … Chen 2022 *AEM* 12, 2102283(refs 16a · 16b — 저압 void 자가 치유 불가).

- **2026-09-23 (ingest 53, `assb` 53호 Ren, Danner, …, Latz, Srinivasan, Janek, Sakamoto, Wachsman, Fattakhova-Rohlfing 2023 · *Adv. Energy Mater.* 13, 2201939 · ⚠ Perspective 34 쪽 + SI 15 쪽, CC BY-NC)** — 큐 **54번**(2차 묶음 열다섯째 편, 02호 ref 17). LLZO 산화물 공소결 복합양극 종설 + 자기 P2D 사례 계산(NMC811/LLZO 75 vol% · 50/100 µm · 1/10 mA cm⁻², 문헌 파라미터).
  ★★★★ **판정**: `θ(N)` 0/53 — 자기 모델 `θ ≡ 1`(열화 무시 인쇄) · **공백을 인쇄**("no experimental study that incorporates percolation theory") · `N` 축 원전 = Barai 2021 [127] 모델 한 편 + 산화물 용량 곡선 재인용 넷(접촉 분율 0). 산화물 시점 = 제조(냉각 응력 ≈1 GPa 모의 ↔ 100–150 MPa, "possible") + 운전("fatigue", 인용 0). ★★★ 시간 배정 역전(인용 [103] = 23호 반대 배정) — 33호에 이은 두 번째. 모델: `a` 미정의 · `ε_CAM` 고정 · 접촉 자리 = `a·i₀₀` + `a/R_SP`.
  **채움표 53호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(공백의 인쇄) · Q2 반 칸 검토 후 접음 · Q4 0/53 **마흔다섯 번째 성질** · Q3 층 하나(계 간 이식) · Q8 부분.
  **곱 축퇴 처방 서른여섯 번째 적용**: 1–4단계 ❌ · 새 줄 "전류 진폭(선형 ↔ 로그) — 직렬 `R_SP` ↔ `R_CT` 를 가르고 면적은 둘 다에 남는다" · `[재현]` improved 체제에서 면적형 접촉 손실 전압 비가시.
  ⚠ 어긋남 15 건: **D1 state-of-the-art 24 · 15 ↔ 그림 ≈120 · ≈115 ↔ SI ≈112** · **D2 시간 배정 역전** · D3 `R_CT` = `R_SP` 2600 · D4 Fig. 7d 사이클 0 · D5 `a` 미정의 · D8 In-Li ↔ Li · D9 κ_eff ×10 · D10 `R_CT` 가지 ≈0 · D12 7.5 % 문턱 ↔ 6.5 % · D14 결론 "cracks" ↔ 모델 0 외.
  낱말 지문: 11 열 중 `contact loss` 5(황화물 4 · 일반 1) · `MPa` 7(응력 6 · 황화물 운전 1) 외 0 · `crack*` 17 · `CTE` 19 · `delaminat*` 8 · `fatigue` 1 · `Deconvol*` 1.
  그림: 크로퍼 13 + 수동 2 — **Read 7 장**(Fig. 1 · 4 · 5 · 7 · 9 · SI-1 · SI-2), 안 봄 Fig. 2 · 3 · 6 · 8, 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른여섯 번째 적용 · 처방 표 새 줄) · [[assb-interphase-vs-contact-loss-attribution]](계보 표 53호 행) · [[assb-sensitivity-sweep-vs-identifiability]](53호 절) · 큐 문서 §6-3-g 54 행 + 지문 ¹⁹.
  후속(서지 기준, 미열람 — **큐 55 · 57 · 58 인용**, 56 · 59 0): **Barai … Srinivasan 2021 *Chem. Mater.* 33, 5527**([127] — 사이클 축 박리 모델) · **Ihrig … Guillon 2021 *JPS* 482, 228905**([105] — 기계 기구 배제 대조) · **Tsai … Guillon 2019 *Sustain. Energy Fuels* 3, 280**([83]) · **Neumann … Latz 2020 *ACS AMI* 12, 9277**([32] — 접촉 → 활성 면적) · Finsterbusch, Danner … 2018 *ACS AMI* 10, 22329([12]) · Bucci … Carter 2018 *PRM* 2, 105407([126]) · Mücke … 2021 *JPS* 489, 229430([108]).
- **2026-09-23 (ingest 54, `assb` 54호 Neumann, Hamann, Danner, Hein, Becker-Steinberger, Wachsman, Latz 2021 · *ACS Appl. Energy Mater.* 4, 4786 · 본문 19 쪽 + SI 26 쪽, © ACS)** — 큐 **55번**(2차 묶음 열여섯째 편, 지목 3 회 02 · 27 · 53호). LLCZNO 가넷 SE 다공층 셋(56 · 42 · 25 %) FIB-SEM 재구성 + 워터셰드 입자 분할 + BEST 미세구조 모델(입계 BV + 공간전하층 축전) · 차단 Au EIS 모의 · 삼층 Li 대칭 셀 ASR.
  ★★★★ **판정**: 굴곡도 = 구조 계산(✅ 곱 풀림) · `σ⁰` = 외부 입력(벌크 절편 대역 밖) · 입계 = 재사용 치밀 펠릿 한 스펙트럼 위 손 보정(가정 입도 15 µm) — 남은 합 벌크 ↔ 입계는 원문이 "unfeasible" 두 번 인쇄. 원장 "measured 라벨" ❌(Table S4 [°] 0 개). 53호 `β_tort` 2.31 = 56 % 한 점 · `β_GB` 1.39 는 치밀 정규화에서만 근처 → 53호 `σ⁰` 뜻 어긋남(`[재현]` ×≈0.27).
  **채움표 54호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q3 새 층(재사용 스펙트럼 위 손 보정) · Q4 0/54 **마흔여섯 번째 성질** · Q1 · Q5 · Q7 · Q8 해당 없음 · Q2 · Q6 없음.
  **곱 축퇴 처방 서른일곱 번째 적용**: 1단계 `C` 두께 불가(`[재현]` ≈6.8 µm) · 2단계 부분(교락) · 3-a ❌ · 4단계 모델에만(ASR −38 %) · 새 줄 "벌크 특성 주파수 ↔ 측정 대역 상한".
  ⚠ 어긋남 20 건: **D3 [°] 0** · D2 뤼드베리 상수 · D1 β-LPS · D6 25 % ↔ +33 % · D7 7.56e-5 ↔ 1.1e-4 · D15 `C` 단위 · **D19 "fluctuates" ↔ 단조 감소** 외.
  낱말 지문: 11 열 중 `MPa` 1(문헌 Li 음극) 외 0 · `deconvol*` 1/1 · `unfeasible` 1/1 · `separab*` 0/1 · `fit*` 1/5(본문 1 = 남의 ECM) · `activation` · `Arrhenius` 0.
  그림: 크로퍼 27 장 — **Read 9 장**(Fig. 4 · 5 · 6 · 7 · 8 · S1 · S4 · S5 + 표 S4), 안 봄 Fig. 1–3 · 9–12 · S2 · S3 · S6–S9, 나머지 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른일곱 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](54호 절) · [[assb-sensitivity-sweep-vs-identifiability]](54호 절) · 큐 문서 §6-3-g 55 행 + 지문 ²⁰.
  후속(서지 기준, 미열람 — 큐 56–59 인용 0): **Hamann … Wachsman 2020 *Adv. Funct. Mater.* 30, 1910362**([30] — 실험 자료 원전, 협착 인자 ↔ 기하 굴곡도) · **Han … Hu 2016 *Nat. Mater.* 16, 572**([9] — `σ⁰` · 교정 스펙트럼) · Fleig & Maier 1999 *J. Eur. Ceram. Soc.* 19, 693([63] — 벽돌층 한계) · Irvine 1990 *Adv. Mater.* 2, 132([61]) · Hein … Latz 2020 *JES* 167, 013546([34]).
- **2026-09-23 (ingest 55, `assb` 55호 Hlushkou, Reising, Kaiser, Spannenberger, Schlabach, Kato, Roling, Tallarek 2018 · *J. Power Sources* 396, 363 · 본문 8 쪽 + SI 5 쪽, © Elsevier)** — 큐 **56번**(2차 묶음 열일곱째 편, 01호 ref 16). LCO(LiNbO₃)/비정질 LPSI 복합양극(탄소 없음) — 대칭셀 EIS 1(Li₀.₇₁CoO₂) + 별도 수지 함침 시편 FIB-SEM 재구성 + 추적자 확산 모의 + 가상 void → SE 치환.
  ★★★★ **판정**: 부피분율 측정(LCO 33.1 · SE 53.7 · void 13.2 % — void = 수지 + 잔류 void) · 연결성 · 접촉 면적 0 · void 의 경로 효과만 계산(`τ` 1.74 → 1.27, `[재현]` `ε/τ` ×1.71, 로그 몫 `τ` 59 %) · 실측 대조는 `τ` 로(1.6 ↔ 1.74) — EIS `ε` 미인쇄, `[재현]` 곱 0.406 ↔ 0.309(×1.31), EIS 시편 void 미측정 ⇒ 구조가 곱을 푼 것은 FIB 시편뿐. 01호 기대 절반(같은 양 대조 불가).
  **채움표 55호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q3 층 하나(두 시편 · 두 경로의 `τ` 일치) · Q4 0/55 **마흔일곱 번째 성질** · Q1 이동 없음 · Q2 반 칸 검토 후 접음 · Q5 · Q7 해당 없음 · Q6 · Q8 없음.
  **곱 축퇴 처방 서른여덟 번째 적용**: 1단계 `C` 0 · 2단계 부분(디지털 치환 — 수송만) · 3-a ❌ · 4단계 ❌(시편 넷 차이) · 새 줄 "두 경로 대조는 관측 곱으로, 같은 시편 · 같은 `ε` 로".
  ⚠ 어긋남 9 건: **D5 `τ_cond` ↔ `[재현]` 1.53(공칭 ε)** · **D7 "void" = 수지 + void** · D2 "relative 13%" ↔ +24.6 % · D3 Bruggeman 1.34 ↔ 1.365 · D6 유한 크기 "all phases" ↔ SI 예외 · D1 500 kHz ↔ 1 MHz 외.
  낱말 지문: 11 열 중 `MPa` 1(SE 펠릿 276) 외 0 · `void*` 43/6 · `resin` 9/2 · `tortuos*` 26 · `percolat*` · `connect*` · `surface area` · `isolat*` 0 · `manual*` 0/3(SI 만).
  그림: 자동 8 + 수동 3(측면 캡션 Fig. 2 · 4 · 6) — **그림 8 장 전부 Read**(Fig. 1 은 쪽 렌더), 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른여덟 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](여섯 번째 표본) · [[composite-cathode-percolation-utilization]](1호 ref 16 기대 판정) · 큐 문서 §6-3-g 56 행 + 지문 ²¹.
  후속(서지 기준, 미열람 — 큐 57–59 는 이 편보다 늦어 인용 0): **Thorat … Wheeler 2009 *JPS* 188, 592**([22] — 대칭셀 굴곡도 원전) · **Landesfeind … Gasteiger 2016 *JES* 163, A1373**([13]) · **Siroma … Ioroi 2016 *JPS* 316, 215**([19]) · Asano … Tatsumisago 2017 *JES* 164, A3960([20]) · Müllner … Tallarek 2014 *Mater. Today* 17, 404([31] — 대표 부피) · 같은 권 **Kaiser … Roling 2018 *JPS* 396, 175**(원장 ★★, 인용 0).
- **2026-09-23 (ingest 56, `assb` 56호 Bielefeld, Weber, Rueß, Glavas, Janek 2022 · *J. Electrochem. Soc.* 169, 020539 · 본문 13 쪽 + SI 15 쪽, © ECS)** — 큐 **57번**(2차 묶음 열여덟째 편, 지목 4 회: 02 · 14 · 50 · 53호). NCM811/Li₆PS₅Cl 복합양극 **FEM**(COMSOL) — 입자형 재구성(GeoDict, 40³ µm³) · 1-입자-void · 원뿔 구조화 셋, 새 측정 0, 대조는 Rueß 2020 첫 충전 3 율.
  ★★★★ **판정**: void 는 **접촉 자리(`φ`)에만** — 1-입자 표면 반구로 피복률 100 → ≈52 % · 크기 비 1.2–10 스윕, 경로 효과 구성상 0(`[인쇄]` "not capable to quantify … ionic percolation"), 검증 모델은 void 14 % → SE · **`θ` 는 손으로 1**(SI: 01호대로면 42 vol% 는 문턱 아래 → placeholder + "moved manually") · 둘을 갈랐나 ❌ · **`j₀` 는 입력**(Rueß `R_CT` → 식 (12), `A` 미정의; 50호 일치는 EIS ↔ EIS, 규약 판정 불가) · 실험 대조 = 남의 곡선 3 율, 오차 척도 0 · **"pore 문턱" 0**(14호 [69] 귀속 불확인) · `θ(N)` 0 · θ-전용 조작 ❌(`φ` 조작, 그것도 분포 의존).
  **채움표 56호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나(비적합 선언 + 이산 선택 + `j₀` 면적 미정의) · Q4 0/56 **마흔여덟 번째 성질** · Q8 층 하나(02호 `U₀` 경유지) · Q2 · Q6 없음 · Q5 · Q7 해당 없음.
  **곱 축퇴 처방 서른아홉 번째 적용**: 1단계 ❌(`C` 0) · 2단계 모델판 둘(피복률 · `φ` 고정 분포) · 3-a ❌ · 4단계 ❌ · 율 스윕 줄 모델 확인(0.02 C 가 `φ` 를 지운다) · 새 줄 "`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사"(`[재현]` BV 몫 ≈44 %).
  ⚠ 어긋남 14 건: **D2 "none fitted" ↔ PSD 선택** · **D3 "best" 상수 세트 ↔ 결론 "not capable"** · **D4 void 최대 4 µm ↔ `[재현]` 5.8 µm · "two 4 µm voids" 30 % ↔ 16 %** · **D5 0.5 C 점 없음 · 50 ↔ ≈40 mV** · **D7 void 14 % 재구성 ↔ 0 %** · **D12 14호 [69] · D13 50호 ref 35 서술** · D1 `T` 273.15 K · D6 "g m⁻²" 외.
  낱말 지문: 11 열 중 `uncertaint` 1(Conforto EIS-PSD) · `contact loss` 5(전부 해석 · 권고) 외 0 · `threshold` · `surpass` 0 · `Achilles` 1 · `caution` 1 · `percolat*` 2/6 · `manual*` 0/2(SI 만) · `error` 0.
  그림: 자동 17 + 수동 2(SI S2 · S7) — **Read 11 장**(Fig. 2 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · S3 · S2 · S7) + S5 쪽 렌더, 안 봄 Fig. 1 · 3 · 11 · S1 · S4 · S6 · S8, 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](서른아홉 번째 적용 · 처방 표 새 줄) · [[composite-cathode-percolation-utilization]](01호 `p_c` 반례 · 수작업 강제) · [[assb-apparent-capacity-decomposition]](`u` 모델 표본) · 큐 문서 §6-3-g 57 행 + 지문 ²².
  후속(서지 기준, 미열람): **Ruess … Janek 2020 *JES* 167, 100532**([10] — 모든 입력의 원전: 식 (12) `A` · 온도 · `R_CT(V)`) · **Bielefeld · Weber · Janek 2020 *ACS AMI* 12, 12821**([25] = 큐 58 — 굴곡도, 14호 "pore 문턱" 귀속 후보) · Minnmann … Janek 2021 *JES* 168, 040537([27]) · Neumann … Latz 2020 *ACS AMI* 12, 9277([38]) · Trevisanello … Janek 2021 *AEM* 11, 2003400([11] — BET 0.2).
- **2026-09-23 (ingest 57, `assb` 57호 Bielefeld, Weber, Janek 2020 · *ACS Appl. Mater. Interfaces* 12, 12821–12833 · 본문 13 쪽 + SI 6 쪽, © ACS)** — 큐 **58번**(2차 묶음 열아홉째 편, 지목 3 회: 15 · 24 · 53호 + 56호 ref 25). NCM/황화물 복합양극 **모델**(GeoDict 합성 구조 + EJ-heat 정상 전도, 01호 AM 배열 재사용), 새 측정 0, 대조는 Kato 2018 `σ_eff` 한 점 · Nam 2018 GITT 면적 비.
  ★★★★ **판정**: "pore 문턱" 은 **여기에도 없다**(`threshold` 0 · void 5 · 10 · 20 % 세 점 단조 ×2 · 급변은 AM 축뿐) — 01 · 56 · 58 어디에도 14호 문장 그대로의 근거 없음 ⇒ **출처 불명** · 유효 전도도 = 구성상 곱이 풀린 모델(`τ²` = `σ⁰ε/σ_eff` 이름표) · Bruggeman ×4 과소 · 검증 한 점은 가정 void 15 % 위(곱 7 % ↔ void 손잡이 ×2) · **바인더 = `θ_AM` 불변 · `A_spec,a` · `σ_eff` · `θ_SE` 동시 감소**(모델) · 01호 `p_c` 는 Fig. 5b 에 말없이 재현(49 → 50 vol%).
  **채움표 57호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나(유도 `τ²` + 가정 void + 남의 GITT 비) · Q4 0/57 **마흔아홉 번째 성질** · Q2 · Q6 · Q8 없음 · Q5 · Q7 해당 없음.
  **곱 축퇴 처방 마흔 번째 적용**: 1단계 ❌ · 2단계 모델판(바인더 쌍) + 실험 쪽 GITT 곱 · 3-a · 4단계 ❌ · 수송 곱 줄 구성상 풀림 · 55호 줄의 실패형(시편 `ε` 가정) · 새 줄 "한 공정 손잡이가 두 곱을 같이 깎을 때 — 면적 비와 수송 비를 같은 모델에서 따로, GITT '면적' 은 곱으로".
  ⚠ 어긋남 13 건: **D1** 극한식 d → 0 = 6.40(발산하는 멱법칙) · **D2** 70:30 SE:AM ↔ AM:SE · **D3** 표 1 고출력 `τ²` 1.7 ↔ 전류는 1.50 에서 · **D4** 바인더 전류 규약 ×1.15–1.30 · D5 캡션 색 · **D6 · D7** Nam 삼각형 4 개 · `p_c` 아래 점 · **D8** 탄소 가정 ↔ 탄소 없는 `A_spec,a` · D9 표본 간격 · **D10** 55호 13.2 % = 수지 + void · D11 LPS ↔ LPSCl · **D12** 14호 [69] · **D13** 24호 14 % · point contacts.
  낱말 지문: 11 열 중 `contact loss` 1(서론 일반론) 외 0 · `threshold` 0 · `surpass` 0 · `abrupt` 2 · `steep` 2(전부 AM 축) · `void*` 49/5 · `tortuos*` 70/1 · `Bruggeman` 20 · `binder` 72/14 · `percolat*` 11/0 · `pressure` 0 · `error` 1.
  그림: 자동 13(제외 1 — S1 벡터) — **Read 6 장**(Fig. 1 · 2 · 4 · 5 · 6 · S4) + Fig. 5b · 5d 확대 + 극한식 쪽 렌더, 안 봄 Fig. 3 · S2 · S3 · S5(적합식은 텍스트), 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](마흔 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](일곱 번째 표본) · [[composite-cathode-percolation-utilization]](`p_c` 계보 · "pore 문턱" 귀속) · 큐 문서 §6-3-g 58 행 + 지문 ²³.
  후속(서지 기준, 미열람): **Nam, Oh, Jung, Jung 2018 *JPS* 375, 93**([25] — Fig. 5d GITT 면적의 원전 · `D` 불변 가정 · 삼각형 4 개) · **Kato … Kanno 2018 *JPCL* 9, 607**([44] — 유일한 `σ_eff` 검증점) · **Froboese … Kwade 2019 *JES* 166, A318**([27] — 실험 모형계 굴곡도) · Shi … Ceder 2020 *AEM* 10, 1902881([28] — 04호와 다른 Shi) · Braun … Ivers-Tiffée 2018 *JPS* 393, 119([52] — 접촉 저항 40 Ω cm²) · Landesfeind 2016 *JES* 163, A1373([47] — 지목 2 회째).

- **2026-09-23 (ingest 58, `assb` 58호 Asheri, Fathidoost, Glavas, Rezaei, Xu 2023 · *Comput. Mater. Sci.* 226, 112186 · 본문 15 쪽, SI 없음, © Elsevier)** — 큐 **59번**(2차 묶음 스무째 · **마지막 편**, 15호 ref [22] "유일한 SSB-ML 인용"). VW + TU Darmstadt, MOOSE 미세 화학-기계 CZM(2D 원판 AM + SE) → 신경망 대리(은닉 1 층 128 · 2048 · 3072, `j` 로 셋) → FE² 두 단계 셀(Li 금속 반쪽전지, 1D). 실험 0. 사용자 제공 코드 저장소 `github.com/mFathidoost/battery` @ `4683a6f` 를 **실행 없이** 조회(`.sav` 미로드 · 노트북 JSON · 데이터 파싱) — 라이선스 미표기, 복사 0.
  ★★★★ **판정**: 박리 `⟨d⟩` 는 `a·(1−⟨d⟩)` 로만 들어가고 미세 유입은 `d` 무관(`[코드]` `soc_dot = 2|j|` 12,304 행) ⇒ **결합상 `ε_p`(`LAM_PE`) 자리** · `[재현]` 저율 손실 8.9 · 3.9 % ↔ 1 C 셀 8.7 · 3.1 % · **`θ(N)` 구조적 0**(한 방전 · ReLU 충전 불가 · 이력 없음) · 손상은 사실상 SOC 의 함수 · 대리 검증은 궤적 안 행 분할 + 범위 안 `G_c` 두 점, 셀 손상 기준해 0, 불확실성 0.
  **채움표 58호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나(simulated-surrogate) · Q4 0/58 **쉰 번째 성질** · Q2 · Q6 · Q8 없음 · Q5 · Q7 해당 없음. **2차 묶음 종료**: 스무 편 ≈16.5 → ≈20.0(Q1 +0.5 · Q5 +2.5 · Q6 +0.5), 마지막 열 편 새 칸 0.
  **곱 축퇴 처방 마흔한 번째 적용**: 1 · 3 · 4단계 ❌ · 2단계 모델판(손상 on/off)이 이름은 면적, 결합은 `LAM` · 율 스윕 줄 ❌(그림이 전하 축 율 순서를 어김) · 새 줄 "박리 변수의 거시 자리는 미세 경계조건이 정한다 — 질량 보존 검사 + 저율 극한 손실로 `ε_p` ↔ `A_eff·k` 를 가른다".
  ⚠ 어긋남 14 건: **D1** 플럭스 척도(인쇄 `J_s` = `j` × 2609.6, Fig. 8 시간은 `j` ÷ 2609.6 — ×6.8 × 10⁶) · D2 벤치마크 범위 · **D3** 벤치마크 sklearn · 출력 `identity` · **D4** 표 5 R²₁ = 학습 R², R²₂,₃ 노트북에 없음 · **D5** `r2_score` 인자 역순 · D6 L2 없음 · D7 ReLU ≥ 0 · D8 식 (26) `η = 0` 에서 플럭스 ≠ 0 · D9 식 (45) `D` 누락 · **D10** Fig. 10 2 C > 1 C 전하 · **D11** Fig. 11 13.92 > 무손상 · D12 unseen 설계 · D13 `D₁` · D14 "thermodynamics law".
  낱말 지문: 11 열 중 `calibrat` 2(학습의 뜻 1 · 남의 편 1) · `contact loss` 3(결론, 정량 0) 외 0 · `delamina*` 22 · `surrogate` 34 · `unseen` 4 · `extrapol*` 0 · `cycl*` 2(서론) · `MPa` 0.
  그림: 자동 16(그림 11 · 표 5) — **Read 6 장**(Fig. 5 · 7 · 8 · 9 · 10 · 11) + Fig. 9–11 원본 래스터 픽셀 판독 + 식 (26)(32)(45) 렌더, 안 봄 Fig. 1 · 2 · 3 · 4 · 6, 표는 텍스트.
  컴파일: 새 개념 0 · 갱신 [[assb-lampe-contact-product-degeneracy]](마흔한 번째 적용 · 처방 표 새 줄) · [[assb-sensitivity-sweep-vs-identifiability]](OAT 스윕 표본) · 큐 문서 §6-3-g 59 행 + 지문 ²⁴.
  후속(서지 기준, 미열람, 큐 밖): **Rezaei, Asheri, Xu 2021 *JMPS* 157, 104612**([11] — CZM 원전; 손상이 플럭스를 막는 판이 있는지) · **Bai, Zhao, Liu, Xu 2019 *JPS* 422, 92**([31] — 식 (32) `a` 출처 · FE² 원형) · Sultanova & Figiel 2021 *Comput. Mater. Sci.* 186, 109990([19]) · Bucci … Carter 2017 *JMCA* 5, 19422([16]) · Fathiannasab … Chen 2020 *JES* 167, 100558([33]) · Wolff, Röder, Krewer 2018 *Electrochim. Acta* 284, 639([29]).

## 이 페이지가 주장하지 않는 것

- ASSB 실셀 자료를 **본 적이 없다.**
  → ⚠ **2026-09-16 정정**: `assb` 4호(Shi 2020)가 **ASSB 실셀 실험 자료**다
  (FIB-SEM 토모그래피 + EIS + 용량곡선), **5호(Doux 2020)도 실험 논문이다**
  (X-선 토모그래피 + XRD + EIS + 압력 실계측). 다만 **원자료(raw data)** 를 받은 것은
  아니고 **논문에 인쇄된 값과 그림을 읽은 것**이다.
- "OCV 로 못 가른다" 를 **결론으로 적지 않았다** — 그것이 이 물음이다.
- 액체셀 결론(`LAM_NE 최광 · LLI 최협`)을 ASSB 로 **옮기지 않는다.** 음극 축이
  아예 다르므로 모집단이 다르다.
- ★ **2026-09-22 추가**: **종설(8호)의 수치를 이 카드의 근거로 삼지 않는다.**
  `<≈1 MPa`·`SOH RMSE ≤0.873 %`·Table 2 의 여덟 숫자는 전부 **재인용**이고,
  그중 하나는 **우리가 가진 원전과 이미 어긋난다**(D1). 원 논문을 받기 전까지
  "리뷰가 이렇게 적었다" 이상으로 쓰지 않는다.
  → **2026-09-23 (35호)**: Table 2 Roman 행의 원전을 받았다 — 8호 원장 **두 곳이 또 어긋난다**(보정된 불확실성 0/8 → 1/8 · "best 0.45 %" 는 dNNe RMSPE). Table 2 여덟 행 중 원전을 대조한 것은 **이 1 행**이고 어긋난다. 8호의 재인용을 원전과 대조한 것은 누계 **2 편**(§3.1 Su 2024 = D1 · Table 2 Roman 2021), 둘 다 어긋남.
- ★ **Q4 가 깨졌다고 주장하지 않는다.** 8호도 **유일성을 재지 않았다** — 이름을
  실패 모드 목록에 올렸을 뿐이다. `assb` **8 / 8 편 0** 이다.
- ★★ **2026-09-22 정정·확장 (10호)**: **Q4 의 칸은 채워졌으나 "쟀다" 는 여전히
  0 이다.** 10호가 깬 것은 **"아무도 이 문제를 이름 붙이지 않았다" 는 상태**이지
  **"아무도 재지 않았다" 는 상태**가 아니다. **유일성·식별성을 수치로 잰 `assb`
  논문은 10 / 10 편 중 0 편이다** — 조건수 · 프로파일 가능도 · 근최적 폭 ·
  Fisher/CRB 가 전부 0 이다. 이 구분을 흐리지 않는다.
- ★ **10호의 재인용 수치를 이 카드의 근거로 삼지 않는다.** `22 % / ~10 %` ·
  `~120 MPa` · `~400 MPa` · `<1 Ω cm²` 는 전부 남의 논문 값이고, 그중 하나는
  **인용 번호가 틀렸다**(digest D5). 원전을 받기 전까지 **방향만** 쓴다.
  ⚠ 단 **방법론적 주장**(비유일성 · 최소 원소 · ill-posedness · 주관적 귀속)은
  **저자들의 1차 주장**이므로 이 규율의 바깥이다 — 그렇게 구분해서 인용한다.
- ★★★ **2026-09-22 (11호 Yu 2024) — 세 가지를 주장하지 않는다.**
  ① **"Q4 가 측정됐다" 고 하지 않는다.** 11호도 재지 않았다 (**0 / 11 편**).
  우리가 한 것은 **논문이 인쇄한 두 그림(Fig. S3, Fig. 4d/7d)을 나란히 놓고
  크기를 비교한 것**이고, 그 비교는 **우리 `[재현]` 이지 논문의 주장이 아니다.**
  ② **"DRT 봉우리 높이가 배선 때문에 69 % 틀렸다" 고 하지 않는다.** 배선이
  바뀌면 인덕턴스·접촉저항이 **실제로** 바뀌고, 두 측정의 최고 주파수가
  **1 MHz ↔ 2 MHz** 로 다르며, SI 가 **"같은 셀" 이라고 명시하지 않는다.**
  우리가 말하는 것은 **"인공물의 상한이 본문 효과보다 크다"** 까지다.
  ③ **11호의 봉우리 개수(5–6)를 "정답" 으로 삼지 않는다.** 같은 논문이
  개수가 **사이클·조작·배선의 함수**라는 것을 보여 준다 —
  9호를 판정할 때 쓰는 것은 **"2 개는 모자란다"** 가 아니라
  **"개수를 고르는 규칙이 문헌에 없다"** 이다.
  ④ ⚠ **그림에서 읽은 봉우리 높이·위치는 전부 `[도표]` 다.** 세로 판독 오차
  ±1–3, 가로 ≈1/4 자릿수. 이 값들을 정본으로 인용하지 않는다.
- ★ **2026-09-22 (12호 Sadegh Kouhestani 2022) — 세 가지를 주장하지 않는다.**
  ① **이 종설의 어느 수치도 이 카드의 근거로 쓰지 않는다** — `0.4–1 MPa`·EV 판매 통계·
  `40–70 °C` 전부 재인용이고, 인용번호 오류가 21 건이라 **귀속 자체가 불확실**하다.
  ② **"PHM 분야가 LAM 과 접촉 손실을 같은 것으로 본다" 고 일반화하지 않는다.** 확인된 것은
  **이 종설 한 편의 §2.2 정의 문장**이고, 그 원전(Hu 2020 *Joule*)이 같은 정의를 쓰는지는
  원전을 받아야 안다.
  ③ **`A_eff` 가 Tian & Qi 2017 에서 왔다고 주장하지 않는다.** 12호의 한 문장에서 **형태가
  같다**는 것까지이고, 9호(Huo 2025)가 그 논문을 인용하는지는 **확인하지 않았다**.
- ★ **2026-09-22 (13호 Zheng 2026) — 세 가지를 주장하지 않는다.**
  ① **"그리드 ASSB 는 LFP + Si 다" 를 사실로 옮기지 않는다** — 13호의 **권장**이고, 저자
  소속(전력연구원 + 전지 제조사)이 수요 측이며 권장 복합전해질의 유일한 수치 예가 **자기
  논문**이다. 이 카드가 받는 것은 "그런 설계가 요구되고 있다" 는 진술까지다.
  ② **`<5 MPa` 를 압력 창의 값으로 쓰지 않는다.** 1 차 주장이지만 인용 문장이 값을 주는지
  확인되지 않았고(G3), 같은 논문의 Fig. 2 가 권장 클래스에 상단 10 MPa 를 준다(D4). Fig. 2
  의 다섯 창은 `[도표]` 이고 산정 규칙이 없다(G8).
  ③ **"접촉 손실을 임피던스 쪽에 둔다" 가 13호의 입장이라고 단정하지 않는다.** 13호는
  소속을 **적지 않았다** — 우리가 확인한 것은 **누락**이지 배정이 아니다. 12호의
  `LAM ⊃ 접촉 손실` 과 나란히 놓을 때도 "다른 방식으로 분리 물음이 없다" 까지만 말한다.
- ★ **2026-09-22 (14호 Oh 2025) — 세 가지를 주장하지 않는다.**
  ① **"volumetry 가 `LAM_PE` ↔ 접촉 손실을 가른다" 고 하지 않는다.** 새 감도 행의 부호표
  (ΔS 행 = 0 / `dE/dP` 행 ≠ 0)는 **우리 `[해석]`** 이고 실측 0 이다 — 논문은 그 물음을
  두지 않았고, 폭 측정기로 검사할 명제로만 등록한다.
  ② **42.7 µJ mol⁻¹ Pa⁻¹ 를 "ΔV" 라는 재료 상수로 옮기지 않는다.** 같은 신품에서 압력
  구간에 따라 2 배(D4), 전·후 측정의 SOC 가 171 mV 다르다(D7). `E(P, x)` 면이 모델링되기
  전까지 "이 셀에서 이 구간에 이 값" 까지만.
  ③ **"void 는 용량에 안 보인다" 를 일반화하지 않는다.** 50 사이클 · 조건당 셀 1 · 2 점 ·
  0.5C 의 것이고, 4호는 같은 자릿수의 void 에서 98 % 손실을 봤다. 우리가 받는 것은
  **사상이 문턱형이라는 두 점**까지다. 그리고 **Q4 는 0/14** — 역문제가 없다는 것은
  "유일성이 필요 없다" 가 아니라 "귀속의 유일성을 아무도 안 물었다" 이다.
- ★ **2026-09-22 (15호 Rahman & Lu 2024) — 다섯 가지를 주장하지 않는다.**
  ① **이 편의 어떤 문장도 이 카드의 근거로 쓰지 않는다.** 1차 측정 0 · **재인용 수치도 0**
  이고, 우리가 가져온 것은 **인용 관계 두 개**뿐이다.
  ② **"[5] 인용이 어긋난다" 는 우리 1호 digest 대조로 확인된 것**이고, 그 digest 자체는
  원문 PDF 의 **사본**이다 — 논문·보고서에 옮기려면 원문 두 편을 다시 편다.
  ③ **"[21](12호) 인용이 원전과 맞다" 고 단정하지 않는다.** 우리 12호 digest 가 FNN/RNN
  정의 수준을 채록하지 않아 **어긋남 미확인(정합 추정)** 이다. 우리가 말하는 것은
  "12호의 **결론**이 전달되지 않았다" 까지다.
  ④ **ref [28]·[22]·[16]·[15]·[2] 를 읽지 않았다.** 그들에 대한 판단은 **제목·서지
  수준**이고, 특히 D6(Janek & Zeier 논조 반대)은 **제목만으로 한 판단**이다.
  ⑤ **"IISE 회의록이 심사를 받지 않았다" 고 주장하지 않는다.** PDF 에 심사 기록·DOI·
  접수일이 **없다**는 것만 적었다.
- ★★ **2026-09-22 (16호 Ramanayagam et al. 2026) — 다섯 가지를 주장하지 않는다.**
  ① **논문의 결론(압력이 `j₀` 를 올린다)이 틀렸다고 주장하지 않는다.** 주장하는 것은
  **그 절차가 `j₀` 와 접촉 면적을 가른 절차가 아니라는 것**이고, 근거는 **논문 자신의
  식 (4)·(5) 와 자신의 Table 2** 다.
  ② **`j₀^true` 가 실제로 감소한다고 주장하지 않는다.** 대안 배정(0.60 배)은 `Q_DL` 을
  면적으로 읽었을 때의 **결과**이지 우리 측정이 아니다. 주장은 **"같은 데이터가 반대
  결론을 허용한다"** 까지다. ⚠ `β` 가 달라(0.89 ↔ 0.81) 두 `Q` 는 엄밀히 차원이 다르다.
  ③ **In–Li 평탄 전위의 0.11 V 차이를 압력 효과라고 하지 않는다.** 기준극 오프셋이 더
  그럴듯하고, **둘 다 논문이 검토하지 않았다**는 것이 요점이다. `[재현]` 0.38 mV MPa⁻¹ 가
  14호의 `dE/dP`(0.23–0.44)와 같은 자릿수인 것도 **우연일 수 있다** — 화학·셀·측정이 다르다.
  ④ **이 편의 압력 값을 다른 셀로 옮기지 않는다.** In 음극 · 단결정 NMC83|6|11 ·
  argyrodite · ∅12 mm · 0.1 C · **신품 2 번째 사이클**이다. 5호의 Li 금속 75 MPa 상한과
  **같은 축에서 비교할 수 없다**.
  ⑤ **이 편에서 열화에 관한 어떤 것도 가져오지 않는다.** `degrad*`·`aging`·`LAM`·`LLI`·
  `SOH` 가 **전수 0 회**다. 우리가 받는 것은 **역문제의 구조**이지 열화 지분이 아니다.
- ★★★★ **2026-09-22 (17호 Yanev et al. 2024) — 여섯 가지를 주장하지 않는다.**
  ① **논문의 결론이 틀렸다고 주장하지 않는다.** 주 결론(foil Li-In 음극이 율 제한이고
  Li-In-SE 복합이 그것을 완화한다)은 **전극 분해 전위 측정**이 떠받치고, 그것은 이
  계보에서 가장 직접적인 종류다. 비판은 **`n=1` · 옴 분리 · 기준극 검증 · 배정**에 있다.
  ② **"기준 전위가 1.35 V 로 옮겨 갔다" 고 단정하지 않는다.** 확실한 것은 `[재현]`
  **"옴이 아니다"**(옴 몫 0.2 %)까지다. **평형 전위라는 해석에는 CA 후 이완 곡선이
  필요하고, 논문은 셀 안에 RE 를 두고도 재지 않았다.**
  ③ **0.98 V 를 Li-In 물질의 성질로 옮기지 않는다.** 그것은 **조성 × 제조법 × 율** 의
  폭이다. **열역학 평탄 폭은 이 편에서 ±10 mV 안이고, 그 ±10 mV 조차 옴 강하와
  구별되지 않아 더 좁게 재지 못했다.**
  ④ **압력을 결론에 넣지 않는다.** **50 MPa 한 점**이고, 16호와의 대질(§8)은 **가설**이다
  (압력이 2–8 배 다르고 SE·조성·전류·SOC 가 전부 다르다).
  ⑤ **Table S1 의 CE 를 `LLI` 대리로 쓰지 않는다** — `[재현]` "추세"(0.5 %p)가 유일한
  산포 대용(2.2 %p)보다 작고 반복이 0 이다. 그 위의 "SE 분해" 기구 주장도 받지 않는다
  (독립 관측 0).
  ⑥ **Q4 는 여전히 0 / 17 이다.** 17호는 유일성을 **잰 것이 아니라 역문제를 안 푼 것**
  이다 (`[인쇄]` "beyond the scope of this study"). 그 덕에 이 편의 결론이 축퇴에 덜
  노출되지만, **그것은 "쟀다" 가 아니다.**
- ★★★★ **2026-09-22 (18호 Fukunishi et al. 2023) — 여섯 가지를 주장하지 않는다.**
  ① **논문의 결론(R3 증가가 주 원인, R4 는 2차 입자 내부)이 틀렸다고 주장하지 않는다.**
  비판은 **교락(두 계의 양극 조성이 다르다) · 산포(같은 이름표의 `R3` 가 1.45 배) ·
  배정 근거(접촉 면적 원자료 두 장의 배율이 다르다) · λ 선택**에 있다.
  ② ★★ **`C` 비 분해(LPSI 면적 ≈1/2.7 + 화학 ≈2.4 배)를 측정값으로 쓰지 않는다.**
  그것은 **로그 막대에서 읽은 두 수의 비**이고, 노화 후 `p` 미공개 · `C ∝ θ` 가정 ·
  조건당 셀 1 위에 있다. 주장은 **"같은 지면의 두 열을 곱하면 저자가 남긴 'or' 가
  갈린다"** 까지다.
  ③ **"활성 접촉이 입자 표면의 ≈2 %" 를 수치로 인용하지 않는다** — 이중층 비용량
  10 µF cm⁻² 는 **우리 가정**이고, 같은 계면의 `C_eff` 가 283/293/303 K 에서 **4.4 배**
  흔들린다. 다만 **방향은 분명하다: `[인쇄]` "completely immersed" · "uniform physical
  contact" 와 자기 용량 데이터가 맞지 않는다.**
  ④ **LPSI ↔ LPSCl 의 차이를 전해질의 성질로 옮기지 않는다** — **복합양극 조성이
  다르다**(49:43:8 ↔ 69:26:5 wt%, 근거는 "preliminary tests" 뿐).
  ⑤ **이 편의 열화 값을 다른 셀로 옮기지 않는다** — `[재현]` **3.7–5.2 mg cm⁻²** 의
  초박형 전극, **0.54 mA cm⁻²(1.0 C)**, **333 K · 50 사이클**, **운전 압력 미상**이다.
  그리고 **압력에 대해 아무것도 주장하지 않는다**(`pressure` 0 회).
  ⑥ **Q4 는 0 / 18 이다.** 저자들이 갈림을 **인쇄했다**는 것이 **갈랐다**는 뜻은 아니다.
- ★ **2026-09-23 (21호 Sedlmeier 2023) — 셋을 주장하지 않는다.**
  ① **"OCV 로 접촉 손실을 못 가른다" 를 21호로 증명했다고 하지 않는다.** 21호가 보인 것은 **음극 Li 재고**에서
  "있음 ↔ 접근 가능" 이 OCV 에서 같다는 것이고, 양극은 OCP 가 기울어 있어 **같은 논리가 그대로 서지 않는다.**
  ② **Fig. A·1 이 틀렸다고 단정하지 않는다** — 축 이름대로면 Fig. 4 와 0.62 V 어긋난다는 것까지이고,
  "숫자가 이미 환산된 것" 이라는 읽기는 `[추론]` 이다.
  ③ **16호의 0.11 V 어긋남을 설명했다고 하지 않는다** — 리튬화 금선의 이완 경로는 **후보**이고, 16호의
  측정 시점을 모른다.
- ★ **2026-09-23 (22호 Strauss 2018) — 넷을 주장하지 않는다.**
  ① **XRD 불활성 분율이 `1 − θ_AM` 이라고 하지 않는다** — 측정이라는 것(역산이 아니라는 것)과 **합집합 상한**이라는 것까지다.
  ② **원인이 이온 고립이라고 하지 않는다** — 저자의 "전자" 배정이 **자기 데이터로 시험되지 않았다**는 것까지다. 정보 깊이
  논증(`[재현]` ≈3–15 µm)은 NIST 근사 감쇠계수와 가정 공극률 위의 **방향성**이다.
  ③ **1호 모델이 틀렸다고 단정하지 않는다** — 1호의 SE 3 µm 고정·구형 무겹침이 이 복합체와 다르다. 주장은 "1호 식 (8) 은 이
  재료계의 불활성을 **공극률 없이도** 3–15 배 과대 예측한다" 이다.
  ④ **`θ·η` 표의 `η` 를 절대값으로 쓰지 않는다** — 분모(`Q_full` ≈196 mAh g⁻¹)가 **LIB 4.4 V** 기준이고 ASSB 컷오프는 0.6 V 가정 위에 있다.
- ★ **2026-09-23 (23호 Koerver 2017) — 넷을 주장하지 않는다.**
  ① **23호 셀에 접촉 손실이 없었다고 하지 않는다** — "EIS 창 안의 양극 저항 증가는 `C` 가 따라가지 않아 면적 형이 아니다(전제 `C ∝ 면적` 위)"
  까지다. 완전 고립 입자는 호에서 빠질 뿐이고, 창 밖(< 1 Hz) 과정과 분해 뒤 생긴 틈은 판정 밖이다.
  ② **손실 예산의 ≳85 % 를 접촉 손실로 돌리지 않는다** — `η(i)` 와 상대극 고갈이 같은 칸에 있다. 3.7 % 도 "≈1 % of SE" 의 기준(미기재)에 걸린다.
  ③ **상대극이 첫 사이클 손실의 몇 %를 만들었다고 하지 않는다** — 평탄 이탈의 서명(`C_anode` 붕괴)과 구조적 필연(재고비 ≈1.4)까지다.
  ④ **3·4호가 23호를 잘못 인용했다고 하지 않는다** — 그 두 편의 인용 문장은 대조하지 않았다.
- ★ **2026-09-23 (24호 Stavola 2023) — 넷을 주장하지 않는다.**
  ① **80 % 조각 6 의 비반응 모집단이 `θ`(고립)라고 하지 않는다** — pristine 근처에 충전 내내 남았다는 `[도표]` 관측까지이고, 자촉매 가짜 상분리·계면층과 양립한다.
  ② **"굴곡도가 진화하지 않았다" 고 하지 않는다** — `σ_eff` 로 보면 80 % 셀 ≈3 배이고 그 배정이 안 갈린다는 것까지다.
  ③ **01 이 틀렸거나 맞았다고 하지 않는다** — 다른 양이라는 것까지다.
  ④ **22호 불활성 분율이 과대라고 하지 않는다** — 한쪽 면 편향이 ±0.08 까지 가능하고 부호가 σ 비에 달렸다는 것, 22호 안에 반대 신호(NCM-S 2 %)가 있다는 것까지다.
- ★ **2026-09-23 (25호 Zhou 2025) — 넷을 주장하지 않는다.**
  ① **Fig. 3 곡선 겹침의 원인을 주장하지 않는다** — 벡터 경로가 ≤0.8 Ω 로 같아 **표시된 조건 전부가 서로 다른 측정일 수는 없다**는 것까지다. 어느 쪽이 원 데이터인지 모른다.
  ② **미세구조가 저압 감쇠를 못 줄인다고 하지 않는다** — 그림은 인쇄보다 **큰** 유지율 차를 보인다. 주장은 초기 손해가 공통 모드라는 것과, 감쇠의 전압 쪽이 저자 적합에서 Li 계면이라는 것까지다.
  ③ **Li 음극이 용량 감쇠의 원인이라고 하지 않는다** — 2전극은 용량 손실의 전극 배정을 못 한다. 저항 배정까지다.
  ④ **5호의 위 벽이 틀렸다고 하지 않는다** — 25호는 압력 장치·계측이 없고 셀이 하나씩이다. "반례 후보" 까지다.
- ★ **2026-09-23 (26호 Iwakiri 2024) — 넷을 주장하지 않는다.**
  ① **Q4 가 움직였다고 하지 않는다** — 26호는 식별성을 재지도, 명제로 쓰지도 않았다. 비식별 세 방향은 **저자 그림을 우리가 겹친 것**이고 `D_e⁻` 판정은 **우리가 식 (30) 으로 한 예측**이다.
  ② **Nelder–Mead 가 시작점에서 안 움직였다고 단정하지 않는다** — 7/10 이 정확히 ×1.0500 인 비율표까지가 사실이고 시작점 해석은 `[추론]` 이다(시작점 미기재).
  ③ **`D_M⊕`↔`a_max` 대칭을 "LAM 과 수송은 못 가른다" 로 일반화하지 않는다** — 박막 1차원 모델의 `x` 좌표 안의 대칭이고, 절대 용량 축과 `I⁺₀ ∝ a_max` 가 깬다.
  ④ **이 편의 수치를 ASSB 복합양극으로 옮기지 않는다** — 박막(입자 · 공극 · 접촉 없음), 빌린 데이터 한 셀, 열화 0 이다.
- ★ **2026-09-23 (27호 Sinzig 2024) — 넷을 주장하지 않는다.**
  ① **Q4 가 움직였다고 하지 않는다** — 27호에는 데이터가 없고, 저자는 식별성을 재지도 명제로 쓰지도 않았다. `u` ↔ 오프셋 대응은 **우리가 벡터 좌표로 한 `[재현]`** 이다.
  ② **큰 `κ` 오프셋이 전부 접촉 손실이라고 단정하지 않는다** — 0.068 ↔ 0.07 일치까지이고, `u` 가 부피 분율인지 · P2D 면적 과대(≈1.5 배)가 상쇄되는지는 모른다.
  ③ **"P2D 는 접촉 손실을 원리적으로 못 가른다" 로 일반화하지 않는다** — 균질화 P2D 한 형식(`A` 한 손잡이)의 구조다.
  ④ **27호의 수치를 실셀로 옮기지 않는다** — 참값도 모델이다(`[인쇄]` "assumption"), 미세구조 1 개 · 전자 연결만 · 열화 0.
- ★ **2026-09-23 (28호 Bizeray 2019) — 넷을 주장하지 않는다.**
  ① **Q4 가 움직였다고 하지 않는다** — 28호는 식별성을 쟀지만 **액체셀**이고, 카드 방향(양극 용량 분할)은 식별 집합 밖(입력)이다.
  ② **"SPM 에서 접촉 손실 ≡ LAM" 을 원문의 주장으로 적지 않는다** — 식 19 묶음 위의 우리 대수이고, **입자 통째 비연결**에만 해당한다.
  ③ **SPM 이 ASSB 에 맞는다고 하지 않는다** — SPM 은 전해질 수송을 무시하고, 27호에서 ASSB 복합양극의 이온 수송(`κ`)이 지배 인자였다.
  ④ **28호의 `τ_d` 값을 인용하지 않는다** — 셀 하나 · CI 0 · DoD 선택이 `[인쇄]` "somewhat arbitrarily" · 단독값과 합 적합이 ×4.6 어긋난다.
- ★ **2026-09-23 (31호 Chien 2023) — 넷을 주장하지 않는다.**
  ① **Q4 가 움직였다고 하지 않는다** — 액체셀이고, 인쇄된 BET 문장은 비식별의 진단이 아니라 **비교가 면적에 불변이라는 선언**이다.
  ② **"`D_app` 은 LAM 에 눈멀었다" 를 원문의 주장으로 적지 않는다** — 식 19 위의 우리 대수이고, 반무한 창 · 균질 모집단 · 액체 쪽 확산 무시 위다.
  ③ **`R/k` 가 면적을 가른다고 하지 않는다** — 후보다. `R` 에서 면적 무관 항을 빼야 하고, 이 편 지면에는 계산 재료(사이클별 `k`)가 없다. 검증 0.
  ④ **이 편의 사이클 `D` 감소가 면적 손실이라고 하지 않는다** — Fig. 8 에서 한 면적 인자는 충전 끝에서만 양립하고, 그 구간은 저자 가정(단상)이 깨진 곳이다. "배정이 안 갈린다" 까지다.
- ★ **2026-09-23 (36호 Thelen 2024) — 넷을 주장하지 않는다.**
  ① **확률적 모드 진단 문헌이 없다고 하지 않는다** — 이 종설이 **제시하지 않았다**까지다. 모드 진단 원전 13 편은 열지 않았고, Thelen 2022 · Navidi 2024(co-kriging 사후 분산)처럼 확률 출력을 가진 편이 있을 수 있다.
  ② **"구조적 비식별은 aleatory/epistemic 밖이다" 를 원문의 주장으로 적지 않는다** — 원문은 식별성을 말하지 않는다. 표는 원문 정의(reducible · CI 붕괴) 위에 우리가 얹은 대비다. 분류 원전(Der Kiureghian 2009)이 그 자리를 어떻게 두는지는 미확인.
  ③ **Ruan 2022 가 비식별을 사전으로 가렸다고 하지 않는다** — 재인용 한 문장에서 읽은 가능성이고, 원전의 검증 설계(분포 밖 시험 유무)를 보지 않았다.
  ④ **Fig. 3 의 연결선 부재를 저자의 분류 주장으로 읽지 않는다** — 재작도 과정의 누락일 수 있다. 사실은 "이 편 지면에서 접촉 손실은 어느 모드에도 그려져 있지 않고, 캡션은 연결이 있다고 말한다" 까지다.
- ★ **2026-09-23 (38호 Conforto 2021) — 넷을 주장하지 않는다.**
  ① **Q1 이 움직였다고 하지 않는다** — `m_act(N)` 은 측정이지만 `θ·ε_p` 합이고 용량 역산이다. "첫 합 계열 1/38" 은 칸이 아니라 기록이다.
  ② **이완 편향의 크기를 쟀다고 하지 않는다** — 방향과 자릿수만 `[추론]` 이고, 방전 뒤 이완 시간 · 입자 간 리튬 교환은 원문에 없다.
  ③ **Fig. 9 가는 선과 Fig. 6 의 불일치를 오류라고 하지 않는다** — 구성은 SI Fig. S9 에 있고 보지 않았다.
  ④ **`m_act` 가 우리 α 와 같다는 것을 원문의 주장으로 적지 않는다** — 평탄 상대극 위에서 우리가 세운 대응이다(우리 코드 형태의 정본은 `degradation-degeneracy/docs/07_LAM_LLI.md`).
- ★ **2026-09-23 (49호 Barai 2018) — 셋을 주장하지 않는다.** ① **Q4 가 움직였다고 하지 않는다** — 액체셀이고, 비유일성 문장은 ECM · DC 분해에 관한 것이지 카드 방향(양극 용량 분할)이 아니다. ② **"t = 1/f 규약이 틀렸다" · "결론이 틀렸다" 고 하지 않는다** — R8 · R9 는 그림 판독 위의 대조이고, 주장은 "일치의 분해능 ≈1 decade · 시간 척도 단독 명제는 5 C 한 진폭에서 보였다" 까지다. ③ **20호의 결론(음극이 원인)을 흔들지 않는다** — 흔드는 것은 20호 `R_CT` · "접촉 저항" 의 이름표와 경계 규칙이다.
- ★ **2026-09-23 (50호 Miß 2022) — 셋을 주장하지 않는다.** ① **`j₀` 25.8 · 0.11 이 틀렸다고 하지 않는다** — 그 값이 `j₀·θ` 이고 규약 한 줄이 ×τ 를 정한다는 것까지(근거는 논문 자신의 식 (1)(5)(7)과 수정 (ii) 문장). ② **16호의 SE 전도도 서사가 틀렸다고 하지 않는다** — 편 간 R·C 면적 서명은 다른 SE 사이 `C ∝ θ` 라는 약한 전제 위의 우리 계산이다. ③ **과차감의 원인을 음극 조성 · 압력 불일치로 확정하지 않는다** — 로그 축 점 부재 판독 + 비가역 Li 위치 가정 위 조성 계산의 방향 정합까지다.
- ★ **2026-09-23 (54호 Neumann 2021) — 셋을 주장하지 않는다.** ① **입계가 SE 저항을 지배한다는 원문 결론이 틀렸다고 하지 않는다** — 그 분할을 입력 `σ⁰` 가 정했고 교정 데이터가 벌크 절편을 보지 못했다는 것까지(저자 자신의 "not fully resolved"). ② **53호의 `β_GB` 1.39 가 틀렸다고 하지 않는다** — 이 편 수치에서 1.39 를 정확히 재현하지 못했고, 근처 값을 주는 유일한 읽기에서 `σ⁰` 의 뜻이 어긋난다는 것은 우리 재구성이다. ③ **`C_DL^GB` 등가 두께 ≈6.8 µm 를 원문의 주장으로 적지 않는다** — 벽돌층 · ε_r 75 · 15 µm 간격 가정 위의 우리 계산이다.
- ★ **2026-09-23 (55호 Hlushkou 2018) — 셋을 주장하지 않는다.** ① **void 가 이온 수송을 해친다는 원문 결론이 틀렸다고 하지 않는다** — 구조 안의 치환 계산은 그 결론을 받친다; 주장은 두 경로의 "일치" 가 `ε` 규약 위에 있고 곱으로는 ×1.31 어긋난다는 것까지. ② **EIS 시편의 `ε` ≈0.65 를 저자가 쓴 값이라고 적지 않는다** — 인쇄 `R` · `d` · σ⁰ 와 관 내경 가정에서 역산한 우리 값이다. ③ **void 의 접촉 효과가 작다고 하지 않는다** — 이 편에 그 양이 없다(Fig. 4D 는 정성).
- ★ **2026-09-23 (57호 Bielefeld 2020) — 셋을 주장하지 않는다.** ① **"pore 문턱은 없다" 고 하지 않는다** — 01 · 56 · 58 세 편에서 14호 문장 그대로의 근거를 찾지 못했다는 것까지다(14호가 다른 문헌을 뜻했을 가능성은 남는다). ② **바인더가 실셀에서 면적을 17–82 % 깎는다고 하지 않는다** — 모델 출력이고, 실험 쪽은 남의 GITT 비(곱)다. ③ **D3 · D4 의 인쇄 전류가 틀렸다고 단정하지 않는다** — 인쇄 식 · 입력으로 재계산하면 어긋난다는 것까지다(D4 의 `τ²` 규약은 그림 판독으로 정했다).
- ★ **2026-09-23 (58호 Asheri 2023) — 셋을 주장하지 않는다.** ① **"박리는 실제로 `LAM_PE` 다" 라고 하지 않는다** — 이 모델의 결합이 `ε_p` 자리라는 것까지다(인쇄 식 + 자료 질량 보존 + 그림 판독; MOOSE 입력 미열람). ② **표 5 가 조작됐다고 하지 않는다** — 저장소 노트북 출력과 안 맞는다는 것까지(다른 실행일 가능성이 크다). ③ **D10 · D11 을 수치 결함으로 확정하지 않는다** — 그림 판독(±≈25 s)과 서술 · 식의 대조까지다.
