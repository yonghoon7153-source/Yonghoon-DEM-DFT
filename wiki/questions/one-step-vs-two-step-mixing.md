---
title: One-step 일괄 ball milling 과 two-step(Li2S–C 선제작) 중 어느 쪽이 Li2S 이용률을 높이는가
description: "세 성분을 한 번에 가는가, Li2S–C 계면을 먼저 만들고 SE 를 나중에 붙이는가 — 같은 장비·같은 총 에너지에서 순서만 바꿨을 때 무엇이 달라지는가"
created: 2026-09-11
updated: 2026-09-30
type: research-question
tags: [mixing-process, composite-cathode, li2s, sulfide-electrolyte]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md, raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md]
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
  mild mixing 은 SE 를 Li2S–C 도메인 바깥에만 둔다.
- **H4 (밀링 시간 상한) — 2026-09-30 신설.** 순서가 아니라 **에너지 총량에 최적점이 있다**.
  적으면 계면이 안 생기고, 많으면 SE 가 죽는다. 이쪽이 one-step/two-step 논쟁보다 실효 변수일 수 있다.
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

## Status Log
- [2026-09-11] open — 카드 개설. 근거는 액체계 선례 하나. ASSB 혼합 공정 논문 ingest 가 다음.
- [2026-09-30] **active 로 승격** (`confidence: low → medium`). ASSB digest 5편이 들어왔다.
  **H3(one-step 우세)에 고체계 직접 근거**가 생겼고(Cronk 2026, 우리와 같은 조성에서 7배 차이),
  **H1 은 반증**을 받았다. **H2(SE 보호)는 양쪽 근거**가 다 들어와 "손상은 실재하지만 성능의
  지배 변수는 아니다" 로 정리됐다 — 이 카드 개설 당시 "근거 없음" 이던 자리다.
  **H4(밀링 시간 상한) 신설** — 순서보다 에너지 총량이 실효 변수일 수 있다.
  남은 판정: Cronk 의 multi-step 은 SE 를 **손으로** 붙인 것이므로 **우리가 말하는 two-step
  (SE 를 mild BM)은 아직 시험되지 않았다.** 그것이 이 카드의 다음 실험이다.
