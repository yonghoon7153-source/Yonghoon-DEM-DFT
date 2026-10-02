---
title: One-step 일괄 ball milling 과 two-step(Li2S–C 선제작) 중 어느 쪽이 Li2S 이용률을 높이는가
description: "세 성분을 한 번에 가는가, Li2S–C 계면을 먼저 만들고 SE 를 나중에 붙이는가 — 같은 장비·같은 총 에너지에서 순서만 바꿨을 때 무엇이 달라지는가"
created: 2026-09-11
updated: 2026-10-04
type: research-question
tags: [mixing-process, composite-cathode, li2s, sulfide-electrolyte]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md, raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md, raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md, raw/papers/leej2025_halide-segregation-assb-lithium-chalcogen.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-mixed
status: active
feedsInto: "[[li2s-assb-reference-cell]] 의 혼합 공정 선택 · [[composite-cathode-mixing-routes]] 표의 결론 칸"
---

# One-step vs two-step 혼합

> [!question] Li2S·LPSCl·AB 를 **한 번에** ball milling 하는 것과, **Li2S–C 나노복합체를 먼저**
> 만든 뒤 LPSCl 을 mild mixing/BM 으로 더하는 것 중 어느 쪽이 pristine Li2S 의 이용률
> (첫 충전 활성화량·이후 비용량)을 높이는가? 그 차이는 **SE 보호** 때문인가 **Li2S–C 계면**
> 때문인가?

## 왜 중요한가

[[composite-cathode-mixing-routes]] 의 네 경로 중 셋(②③④)이 "Li2S–C 먼저, SE 나중" 구조다.
이 카드가 답하면 그 셋의 공통 전제가 서거나 무너진다. 또 one-step 이 이긴다면 공정이 가장
짧다는 실용적 이득이 있다.

## 가설

- **H1 (two-step 우세, 계면 이유)**: 탄소가 Li2S 를 먼저 감싸야 절연체 표면의 전자 접촉이 확보되고,
  SE 는 그 바깥에서 이온 경로만 맡는다 → [[carbon-dimensionality-electron-network]].
- **H2 (two-step 우세, SE 보호 이유)**: 고에너지 BM 이 LPSCl 을 손상(비정질화·전도도 저하·탄소와
  부반응)하므로 SE 를 고에너지 단계에서 빼는 것이 이득. **2026-09-30: 근거가 양쪽으로 들어왔다 —
  "손상은 실재하지만 그것이 성능을 정하지는 않는다" 가 현재 그림이다** (아래).
- **H3 (one-step 우세)**: 세 상을 나노 스케일로 동시에 섞어야 삼상 계면 밀도가 최대; two-step 의
  mild mixing 은 SE 를 Li2S–C 도메인 바깥에만 둔다. **2026-10-03: 저로딩 한정으로 범위가 좁아졌다.**
- **H4 (밀링 에너지 상한) — 2026-09-30 신설, 2026-10-03 에 스캔으로 확정 방향.** 순서가 아니라
  **에너지 총량에 최적점이 있다**. 적으면 계면이 안 생기고, 많으면 SE 가 죽는다.
- **★ H5 (로딩 의존) — 2026-10-03 신설.** **최적 혼합 경로는 로딩의 함수다.** 교차점이 존재하고
  그 아래에서는 one-step, 위에서는 two-step 이 이긴다. 그렇다면 이 카드의 질문은
  **"어느 쪽이 이기나" 가 아니라 "교차점이 어느 로딩인가" 로 바뀌어야 한다.**
- **H0 (차이 없음)**: 총 에너지가 같으면 순서는 무관.

## Evidence For

- **[2026-09-11] H1 방향의 액체계 선례 — Kim 2023.** 탄소 골격(Gr/CNT)을 용매 분산으로 먼저
  얽고 Li2S 와 BM 한 뒤 1 GPa 성형 → micro-Li2S(1–5 µm) 를 75 wt% 에서 `[도표]` ≈ 1150 mAh g⁻¹(S)
  로 활성화. 다만 **SE 가 없는 계**라 H2 와는 무관하고, BM 조건이 미기재라(G1) 에너지 비교도 불가.

### 2026-09-30 — 고체계 근거 (digest 5편)

- **★ [2026-09-30] H3(one-step 우세) 에 대한 이 위키 최초의 고체계 직접 근거 — Cronk 2026.**
  **같은 조성(활물질:LPSCl:AB = 30:50:20, 우리와 동일)·같은 SE·같은 탄소**에서 혼합 경로만 바꿨다
  (1 mg_S cm⁻², C/20, Li–In):

  | 경로 | 첫 방전 mAh g⁻¹(S) | 첫 사이클 CE |
  |---|---|---|
  | **one-step** (전 성분 500 rpm 1 h) | `[인쇄]` **≈1500** | **129 %** (초과분 = SE redox) |
  | multi-step (S/C 밀링 → SE **손혼합**) | `[도표]` ≈610 | 17 % |
  | hand-mix (mortar 1 h) | `[도표]` ≈200 | 미기재 |

  **Li2S 계에서는 hand-mix 가 사이클 자체를 못 한다.** 기전도 제시된다 — 밀링이 활물질 표면에
  **황 과잉 thiophosphate(Li3PS4+n) interphase** 를 만들고 그것이 리독스 매개체가 된다.
  ⚠ **반드시 같이 적을 단서**: 이 논문의 "multi-step" 은 SE 를 **손으로** 붙인 것이다. 우리가 말하는
  two-step(SE 를 mild BM 으로 붙임)과 다르다. → **배제된 것은 "SE 를 저에너지로 붙이는 경로" 이지
  two-step 일반이 아니다.**
- **[2026-09-30] H2 를 지지하는 쪽 (Cronk 2026).** `[인쇄]` **LPSCl 단독**을 1 h → 10 h 밀링하면
  이온 전도도가 **1.3×10⁻³ → 4×10⁻⁵ S cm⁻¹ (30배 하락)**. 고에너지 장시간 밀링이 SE 를 죽인다는
  직접 측정이다 — 이 카드 개설 당시 "근거 없음" 이던 자리가 채워졌다.
- **[2026-09-30] H2 를 반증하는 쪽 (Cronk 2026 · Lee 2026 · Zhang 2026 · Huang 2026).**
  - Cronk: 그런데 **황과 함께** 1 h 갈면 복합체 전도도가 오히려 **6×10⁻⁶ → 2×10⁻⁵ S cm⁻¹ 로 오른다.**
    그리고 Li2S 양극은 `[인쇄]` **밀링 직후 이미 LPSCl 의 절반이 LPS 로 환원돼 있는데도** 성능이 좋다.
  - Lee 2026: SE 를 **저에너지 2단계(200 rpm 1 h)에만** 넣었는데도 **Li2S–LPSCl 반응이 일어났다**
    (XPS S 2p ~163 eV 의 S–S, XRD 에 S8 없음, Cl 2p 에 LiCl 없음). **"나중에 약하게 넣으면
    보호된다" 는 전제가 화학 반응까지는 막지 못한다.**
  - Zhang 2026: two-step 인데 **2단계도 1400 rpm 고에너지**로 LPSCBr 과 함께 갈고, 그래도 작동한다.
  - Huang 2026: two-step 이고 2단계가 **350 rpm 4 h** 인데 상온 S 이용률 55–61 %.
  → 종합: **SE 손상은 실재하지만(전도도 30배·화학 반응) 그것이 셀 성능의 지배 변수는 아니다.**
- **[2026-09-30] H4(밀링 시간 상한) 의 근거.** 위 두 항을 합치면 순서 논쟁보다 **에너지 총량**이
  변수다. Cronk 의 one-step 이 **500 rpm 1 h** 로 짧고 세다는 점, LPSCl 단독은 10 h 에 죽는다는 점,
  Lee(250 rpm 6.5 h + 200 rpm 1 h)·Huang(350 rpm 4 h)·Zhang(1400 rpm 유효 2 h)·
  Qu(one-step 300 rpm 4 h)가 전부 다른 좌표에 있으면서 다 작동한다는 점이 그 방향이다.
- **[2026-09-30] one-step 이 실제로 쓰인다 (Qu 2025).** Li2S + Super C65 + LPSCl 을 **one-step**
  (Fritsch P7, ZrO2, 300 rpm 4 h) 으로 갈아 SE 50 wt% 복합양극을 만들었다 — **우리 조성과 같다.**
  단 절대 용량을 안 적어(digest G1) 우열 비교에는 못 쓴다.

### ★ 2026-10-03 — Kim 2025 가 이 카드를 부분적으로 답했다 (선양국 그룹)

이 카드가 2026-09-30 에 "우리가 말하는 two-step 은 아직 시험되지 않았다 — 그것이 다음 실험이다"
라고 적었다. **그 조건을 다룬 논문이 들어왔다.** 다만 두 가지 단서가 있다(아래).

**로딩 스캔 — 교차점이 보인다** (2차 방전, 0.1 C, 같은 최종 조성 S : LPSCl : CNT = 25 : 50 : 25):

| S 로딩 | one-step (M600) | two-step (M&M37) | 승자 |
|---|---|---|---|
| **3 mg cm⁻²** | **5.00 mAh cm⁻²** | 4.05 | ★ **one-step** |
| 6 mg cm⁻² | 4.80 | **7.43** | two-step |
| **10 mg cm⁻²** | 4.46 | **10.85** | **two-step (2.4배)** |

→ **H5 의 근거다. 교차점이 3–6 mg(S) cm⁻² 사이에 있다.**

- **H2(SE 보호) — 이 위키 최초의 직접 지지.** SE 보호를 설계의 **명시적 목표**로 삼고 효과를
  숫자로 보인 첫 논문이다. LPSCl 을 밀링 단계와 손혼합 단계로 **쪼갠 비율**만 바꿔 복합양극
  σ_Li⁺ 가 `[인쇄]` **0.07 → 0.14 → 0.16 → 0.42 mS cm⁻¹** (밀링 SE 10:0 → 5:5 → 3:7 → 1:9).
  밀링은 LPSCl 을 비정질화하고 Young's modulus 를 `[인쇄]` **21.98 → 4.63 GPa** 로 떨어뜨린다.
  ⚠ **단 이득은 고로딩에서만 나온다** → **"SE 보호는 전극이 두꺼울 때만 이득이다" 로 조건화**한다.
- **H4(밀링 에너지 상한) — 가장 강한 지지, 이 위키 최초의 "스캔".** 같은 장비·같은 6 h 에서
  rpm 만 바꾼 네 점이 **600 rpm 에 꼭지**를 만든다 (0.5 C 20사이클 `[도표]`
  **160 / 620 / 870 / 670 mAh g⁻¹(S)** @ 200 / 400 / 600 / 800 rpm). 저자 결론 `[인쇄]`:
  "excessive milling may deteriorate the ionic conductivity … crucial to optimize the milling
  conditions **within an appropriate range**."
  ⚠ 단 M800 의 방전/충전 쌍이 본문과 그림에서 어긋난다(digest G6) — **"과도한 밀링의 실패" 를
  M800 으로 인용하는 문장은 검증 불가**다. 꼭지의 존재는 다른 세 점으로도 선다.
- **H1(계면 이유) — 부분 지지하되 주체가 바뀐다.** 이 논문의 "계면" 은 탄소–활물질이 아니라
  **활물질–SE catenation 계면(3Li⁺–PS4+n³⁻)** 이고, 그것은 **1단계에서 SE 와 함께 갈아야** 생긴다.
  "탄소가 먼저 감싸야 한다" 는 여전히 반증이고(밀링 SE 10 % 인 M&M19 는 실패),
  **"활물질–SE 계면을 먼저 만들어야 한다" 로 대체**된다.
- **H3(one-step 우세) — 저로딩에서 지지, 고로딩에서 반증.** 틀린 가설이 아니라 **범위가 좁은 가설**이다.
- **H0 재반증** — 같은 최종 조성에서 순서만 바꿔 10 mg cm⁻² 에서 2.4배.

### Cronk 2026 과의 충돌은 세 축으로 해소된다

| | Cronk 2026 | Kim 2025 |
|---|---|---|
| 승리 경로 | one-step (밀링 SE **100 %**) | two-step (밀링 SE **60 %**) |
| 패배 경로 | multi-step (밀링 SE **0 %**) · hand-mix | **M&M19 (밀링 SE 10 %)** · M200 · M600 고로딩 |
| 로딩 | **1 mg(S) cm⁻²** | **3 / 6 / 10 / 12** |
| 밀링 | Retsch 500 rpm 1 h, BPR 30:1 | Fritsch P7 600 rpm 6 h, BPR ≈6:1 |
| 중간상 | Li3PS4+n (Raman·XANES·cryo-TEM) | 3Li⁺–PS4+n³⁻ (XPS S_B⁰ 162.1 eV·Raman·TGA) |

`[해석]` 셋으로 해소된다. ① Cronk 의 1 mg cm⁻² 은 Kim 의 교차점 **왼쪽**이다 — one-step 이 이기는
구간. ② **"two-step" 의 정의가 다르다** — Cronk 의 multi-step 은 밀링 SE 0 % 이고, Kim 의
M&M19(10 %)도 **똑같이 실패한다.** 즉 **두 논문은 "SE 를 밀링에서 완전히 빼면 안 된다" 에
합의한다.** ③ 밀링 좌표가 다르다(세고 짧게 vs 빠르고 길게, BPR 5배 차이).
**중간상이 독립적으로 같은 종으로 동정됐다**는 것도 큰 수확이다.

### ⚠ 그래도 우리 실험은 여전히 필요하다 — 두 가지 단서

1. **활물질이 S8 이지 Li2S 가 아니다.** 이 논문에 Li2S 데이터는 한 줄도 없다.
2. **"mild mixing" 의 정체가 유발(agate mortar) 손혼합 15 분이다** — Thinky 도 저속 BM 도 아니다.
   우리가 말하는 two-step(SE 를 **mild BM** 으로 붙임)은 **아직도 시험되지 않았다.**
→ 즉 이 카드의 "다음 실험" 은 유효하고, **로딩을 변수로 넣어야 한다**는 조건이 추가됐다.

### ★★ 2026-10-02 — Lee (Jieun) 2025 *Science* 가 H2 의 **부호를 바꾼다**

H2 는 지금까지 **"고에너지 밀링이 LPSCl 을 손상시키므로 two-step 이 유리하다"** 였다. `leej2025_…`
는 같은 손상을 **설계 수단**으로 쓴다 — **2000 rpm 5 h one-step UHS 혼합 중 LPSCl 에서 할로겐이
분리되어 활물질 표면에 LiCl 층을 만들고**, 그것이 유효 Li⁺ 수송을 올린다고 주장한다
(4 mg cm⁻²·70 MPa·25 °C 에서 **6.28 mAh cm⁻²**, 100사이클 98.9 %).

- **H3(one-step 우세) — 강한 지지, 그리고 새 기전.** `[해석]` **one-step 이기 때문에** SE 와 활물질이
  같은 용기에서 갈려 그 계면층이 생긴다. two-step 은 SE 를 나중에 손혼합으로 넣으므로 **그 반응이
  일어날 기회 자체가 없다.**
- **★ H2 의 서술이 뒤집힌다.** "two-step 은 SE 를 고에너지에서 **보호한다**" 는 **장점** 서술이,
  이 논문 기준으로는 **"계면 LiCl 을 포기한다"** 는 **비용** 서술이 된다. **같은 사실의 두 이름**이다.
  → 이 카드는 이제 **"SE 를 보호할 것인가, SE 를 재료로 쓸 것인가"** 라는 선택으로 읽어야 한다.
- **H4(밀링 에너지 상한) — 강한 지지, 그리고 상한과 하한이 둘 다 보였다.** `[인쇄]` **400 rpm 과
  1 h 에서는 분리가 일어나지 않고**(문턱 = 하한), **10 h 에서는 LPSCl 결정구조가 붕괴**해 성능이
  무너진다(상한). → **최적점이 존재한다는 것을 한 논문 안의 세 점(1/5/10 h)으로 보인 두 번째 사례**
  다 (첫째는 Kim 2025 의 rpm 스캔 200/400/600/800).
  ★ 축이 다르다는 점이 중요하다 — **Kim 2025 는 세기, Lee J 2025 는 시간**이고 둘 다 **중간이 최적**이다.
- ★★ **밀링 ↔ 비밀링 직접 대조가 이 위키에 처음 들어왔다.** 그 논문은 **손혼합(상온)** 에서 Cl:P 가
  **1.00 그대로**이고, **손혼합 + 145 °C 3 h** 에서 **1.38** 로 **기계력 없이 열만으로** 부분 분리된다.
  → `[해석]` **기전 후보는 밀링의 "기계력" 이 아니라 "국부 발열" 이다.** ⚠ 그런데 그 논문은
  **혼합 중 온도를 재지 않았다** — 가장 값싸게 메울 수 있었던 공백이다.
- **H1(계면 이유) — 주체가 또 바뀐다.** Kim 2025 에서 "계면" 이 탄소–활물질에서 SE–활물질로
  옮겨갔고, 여기서는 **SE 에서 떨어져 나온 LiCl–활물질**이 된다.
- ⚠ **이 논문은 밀링 조건을 거의 적지 않았다** — 본문에 **`ball`·`mill` 이라는 단어가 없고**
  장비·BPR·볼·용기·분위기·조성비 전부 미기재다(Methods 전량 SI, 미확보). **H4 의 좌표로는
  "2000 rpm · 5 h" 두 점만** 넣을 수 있다 ([[composite-cathode-mixing-routes]] 소견 3).

## Evidence Against

- **[2026-09-30] H1(two-step 우세, 계면 이유) 에 대한 반증 — Cronk 2026.** Li2S–C 를 먼저 만들고
  SE 를 나중에 붙인 multi-step 이 one-step 보다 **훨씬 나빴다**(≈610 vs ≈1500 mAh g⁻¹(S)).
  "탄소가 먼저 감싸야 한다" 는 논리만으로는 이 결과가 설명되지 않는다 — 삼상을 **동시에** 섞는
  것이 이기고, 그 이유는 밀링이 만드는 **활물질–SE 계면상**이다. 단 그 multi-step 은 SE 를 손으로
  붙인 것이라(위 단서) two-step 일반에 대한 반증은 아니다.
- **[2026-09-30] H0(차이 없음) 반증** — 같은 조성·같은 장비에서 경로만 바꿔 7배 차이가 났다.

## 답하는 방법 (설계)

1. 같은 planetary BM, 같은 용기·볼·BPR·총 시간으로 (a) one-step, (b) Li2S+AB 먼저 → LPSCl 을
   같은 밀에서 짧게, (c) Li2S+AB 먼저 → LPSCl 을 Thinky 로 mild. 조건은
   [[mixing-equipment-ball-mill-thinky]] 양식으로 전부 기록.
2. 지표: 첫 충전 활성화량(mAh g⁻¹(Li2S)), 이후 비용량, 탄소+SE 펠릿 전자 전도도, SE 의 XRD/
   이온 전도도(H2 분리용).
3. H2 를 가르려면 **LPSCl 만** 같은 BM 조건에 노출한 뒤 이온 전도도를 재는 대조가 필요하다.
4. **★ 2026-10-03 추가 — 로딩을 축으로 넣는다.** Kim 2025 의 교차점이 3–6 mg(S) cm⁻² 이므로
   우리 Li2S 계에서도 **최소 두 로딩**(교차점 추정 아래·위)에서 각 경로를 돌려야 한다.
   한 로딩에서만 비교하면 "어느 쪽이 이긴다" 는 결론이 그 로딩에만 유효하다.
5. **SE 분할비를 변수로.** Kim 2025 는 밀링 SE : 손혼합 SE 를 10:0 / 5:5 / 3:7 / 1:9 / 3:2 로
   쪼갰고 조성(S 함량)에 따라 최적비가 달랐다(25 wt% → 3:7, 35 wt% → 3:2).
   **0:10 과 10:0 만 보는 이분법을 버린다** → [[composite-cathode-mixing-routes]].

## Status Log
- [2026-09-11] open — 카드 개설. 근거는 액체계 선례 하나. ASSB 혼합 공정 논문 ingest 가 다음.
- [2026-09-30] **active 로 승격** (`confidence: low → medium`). ASSB digest 5편이 들어왔다.
  **H3(one-step 우세)에 고체계 직접 근거**가 생겼고(Cronk 2026, 우리와 같은 조성에서 7배 차이),
  **H1 은 반증**을 받았다. **H2(SE 보호)는 양쪽 근거**가 다 들어와 "손상은 실재하지만 성능의
  지배 변수는 아니다" 로 정리됐다 — 이 카드 개설 당시 "근거 없음" 이던 자리다.
  **H4(밀링 시간 상한) 신설** — 순서보다 에너지 총량이 실효 변수일 수 있다.
  남은 판정: Cronk 의 multi-step 은 SE 를 **손으로** 붙인 것이므로 **우리가 말하는 two-step
  (SE 를 mild BM)은 아직 시험되지 않았다.** 그것이 이 카드의 다음 실험이다.
- [2026-10-03] active — **Kim 2025(선양국 그룹)가 이 카드를 부분적으로 답했다.**
  **H5(로딩 의존) 신설** — 최적 경로가 로딩의 함수이고 **교차점이 3–6 mg(S) cm⁻²** 에 있다.
  카드의 질문을 "어느 쪽이 이기나" 에서 **"교차점이 어느 로딩인가"** 로 고쳐야 한다.
  **H2(SE 보호)에 이 위키 최초의 직접 지지**가 들어왔으나 **고로딩 한정**으로 조건화했다.
  **H4 에 최초의 rpm 스캔**(600 rpm 꼭지). **H3 는 저로딩 한정으로 범위 축소.**
  Cronk 와의 충돌은 세 축(로딩·two-step 정의·밀링 좌표)으로 해소되고, **두 논문이 "SE 를 밀링에서
  완전히 빼면 안 된다" 에 합의**한다.
  **우리 실험은 여전히 필요하다** — 그 논문은 S8 이고 mild mixing 이 유발 손혼합이라,
  Li2S + mild **BM** 조건은 미시험이다. 설계에 **로딩 축을 추가**한다.
