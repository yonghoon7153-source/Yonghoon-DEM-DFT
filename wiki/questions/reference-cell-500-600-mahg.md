---
title: 무엇이 reference cell 을 500–600 mAh g⁻¹ 에서 막는가
description: "pristine Li2S ASSB reference cell 이 문헌 수준(500–600, 기준 미확인)에 못 미친다면 병목은 활성화인가, 퍼콜레이션인가, 입자인가, 아니면 단위 착시인가"
created: 2026-09-11
updated: 2026-09-30
type: research-question
tags: [li2s, assb, activation, composite-cathode, units]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-mixed
status: active
feedsInto: "[[li2s-assb-reference-cell]] 의 실험 설계 · [[anode-free-li2s-assb]] 의 Li 재고 상한"
---

# 무엇이 reference cell 을 500–600 mAh g⁻¹ 에서 막는가

> [!question] Li2S:LPSCl:AB = 30:50:20 pristine Li2S 셀에서 문헌 수준 500–600 mAh g⁻¹
> (기준 미확인) 을 재현하지 못한다면, 병목은 **첫 충전 활성화**인가, **전자/이온 퍼콜레이션**인가,
> **Li2S 입자 상태**인가, 아니면 **단위 정규화의 착시**인가?

## 왜 중요한가

이 답이 [[li2s-assb-reference-cell]] 의 다음 실험을 정하고, 활성화량은 곧
[[anode-free-li2s-assb]] 의 Li 재고 상한이다. 병목을 모르면 혼합 경로를 바꿔도
([[composite-cathode-mixing-routes]]) 무엇을 고쳤는지 모른다.

## 가설

- **H1 (활성화 제한)**: 첫 충전에서 Li2S 의 일부만 활성화되고, 활성화 안 된 몫은 뒤 사이클에서
  깨어나지 않는다 → 이후 용량 = 첫 충전 용량의 함수. [[li2s-activation-first-charge]].
- **H2 (퍼콜레이션 제한)**: AB 단일 탄소가 접촉 또는 두께 방향 네트워크 중 하나를 못 채우거나,
  탄소·SE 가 서로를 밀어내 삼상 계면이 부족 → [[carbon-dimensionality-electron-network]].
- **H3 (입자 제한)**: pristine Li2S 의 입자 크기·결정성이 커서 표면적이 부족; 나노화 정도가
  혼합 경로에 따라 다름.
- **H4 (단위 착시)**: 목표 500–600 이 `(S)` 기준인데 우리는 `(Li2S)` 기준으로 재고 있거나 그
  반대 → [[capacity-normalization-li2s-vs-sulfur]].

## Evidence For

- **[2026-09-11] H1 을 지지하는 액체계 선례 — Kim 2023 Fig. S1.** 첫 충전 용량을 25/50/75/100 %
  로 제한하자 이후 방전이 `[도표]` ≈ 270/530/730/930 mAh g⁻¹(S) 로 **20 사이클 동안 층 유지**.
  활성화 안 된 Li2S 는 안 깨어난다 (`raw/papers/kim2023_…` §9.1). 단 액체·Li 금속·LiNO3 조건.
- **[2026-09-11] H2 를 지지하는 액체계 선례 — Kim 2023 Fig. 4A/S4/5.** 접촉 탄소(Gr)와
  네트워크 탄소(CNT 3 wt%)를 나누자 활성화·수명이 함께 늘었고, 어느 하나만으로는 부족했다
  (CNT-only 는 활성화 실패, Gr-only 는 50 사이클 급사).
- **[2026-09-11] H4 는 사용자 진술 자체가 근거다** — 목표의 단위 기준이 명시되지 않았다
  (킥오프 기록 F4). Kim 2023 의 0.5 C 값도 (S) 기준 899.6 ↔ (Li2S) 기준 628 로 갈린다.

### 2026-09-30 — 고체계 근거가 들어왔다 (ASSB digest 2편)

지금까지 이 카드의 근거는 **액체계 Kim 2023 하나와 사용자 진술뿐**이었다. 아래 네 항목이
H1–H4 를 각각 고체계 실측으로 받친다.

- **[2026-09-30] H1 — 이 위키 최초의 고체계 직접 근거 (Zhang 2026).**
  같은 셀·같은 SE·같은 볼밀·같은 3.0 V 컷오프에서
  **pristine(상용) Li2S 첫 방전 `[도표]` ≈270 mAh g⁻¹(Li2S)** vs 반응형 나노결정–비정질 Li2S
  **`[인쇄]` 971** — **3.6배**. **우리도 pristine Li2S 를 쓴다** (`raw/papers/zhang2026_…` §5).
  단서 셋: (i) SE 가 **LPSCBr**(브로민)이지 우리 LPSCl 이 아니다; (ii) 탄소가 MWCNT 10 wt% 로
  우리 AB 20 wt% 와 다르다; (iii) **그 971 자체를 의심할 이유가 있다** — 첫 충전이 이론용량을
  넘고(≈1330 > 1166), LiI 전량 1 e⁻ 산화 몫 `[재현]` 152 mAh g⁻¹ 가 초과분과 크기가 맞아
  **요오드 산화환원이 "Li2S 용량" 에 섞였을 가능성**이 배제되지 않았다 (digest §12-2).
  → 그러므로 안전한 독법은 "**pristine Li2S 는 고체계에서 첫 방전 300 언저리**" 까지다.
- **[2026-09-30] H2 — 이 위키 최초의 고체계 직접 근거 (Huang 2026).**
  **우리와 거의 같은 셀**(LPSCl · Li–In · 상온 · 양극 450 MPa)에서 첨가제 없이 **탄소만** 넣은
  S/KB/LPSC 양극의 0.1 C 첫 방전 **S 이용률 `[도표]` 39 %**, 혼합 이온–전자 전도체를 **6 wt%**
  넣으면 **76 %** (분극전압 0.56 → 0.38 V). 복합체 DC 분극 전도도
  σ_e⁻ 1.71 → **23.80** mS cm⁻¹ · σ_Li⁺ 2.41×10⁻⁵ → **6.50×10⁻³** mS cm⁻¹
  (`raw/papers/huang2026_…` Table S3). **고체계에서는 탄소만으로 삼상 계면이 모자란다.**
  단서 셋: S8 양극이지 Li2S 가 아니다 · 0 wt% 조건은 **첫 사이클 1회뿐이고 사이클 데이터가 없다** ·
  0 wt% 에서 빠진 10 wt% 를 무엇으로 채웠는지 미기재.
- **[2026-09-30] H3 — 이 위키 최초의 근거 (Zhang 2026).** `[인쇄]` **격자상수는 그대로**
  (a = 5.7189 Å)인데 **나노결정화 + 비정질화만으로 3.6배**. 즉 병목이 결정 구조가 아니라
  **도메인 크기·비정질 분율**이라는 뜻이다. 단 SEM 은 여전히 **1–5 µm 이차입자** —
  "나노" 는 일차 도메인 수준이고 이차입자는 우리 pristine 과 같은 크기다.
- **[2026-09-30] H4 — 실질적인 답 하나 (Zhang 2026 · Huang 2026).**
  Zhang 2026 의 안정 구간을 **복합양극 기준**으로 환산하면 `[재현]` **143–159 mAh g⁻¹(composite)**.
  우리 목표 500–600 mAh g⁻¹(Li2S) × 30 wt% = **150–180 mAh g⁻¹(composite)** — **같은 대역이다.**
  → 우리 목표가 비현실적인 게 아니라 **어느 분모로 말하느냐**의 문제일 수 있다.
  또한 Huang 2026 이 ASSB 문헌도 `(S)` 기준을 쓴다는 실례다 (§2.3 에 명시).
  단 Zhang 2026 은 **단위 기준을 글자로 밝히지 않아** digest 가 두 간접 증거(Fig. 5a 의 이론용량
  수직선 ≈1166 · Fig. S12 의 1 C = 3.26 mA cm⁻² / 2.81 mg cm⁻² = 1160 mA g⁻¹)로 `(Li2S)` 로
  확정했다 — 그 근거째로 인용해야 한다.

## Evidence Against

- **[2026-09-30] H2 에 대한 부분 반증 (Zhang 2026).** 탄소가 **MWCNT 10 wt% 뿐**인데 971
  mAh g⁻¹(Li2S) 가 나왔다. 탄소량이 퍼콜레이션의 전부라면 이 값이 안 나온다 — 단 그 셀은
  **in-situ 생성된 비정질 thiophosphate 상이 이온 경로를 맡은** 조건이므로, "탄소가 적어도 된다"
  가 아니라 "**이온 경로를 다른 상이 맡으면 탄소를 줄일 수 있다**" 로 읽어야 한다.
- **[2026-09-30] H1 에 대해 Huang 2026 은 근거를 주지 않는다** (반증도 지지도 아님). S8 출발이라
  첫 스텝이 방전이고, Li2S 첫 충전 과전압·컷오프·활성화량에 대해 **한 글자도 없다**. 이 공백을
  기록해 두는 것이 다음 논문 탐색의 방향이다 — **Li2S 출발 ASSB 논문**이 더 필요하다.
- H3 에 대한 반증은 아직 없다.

## 답하는 방법 (설계)

1. **H4 먼저** — 비용 0. 목표 값의 출처 논문을 가져와 분모를 확인한다.
2. **H1** — 우리 셀에서 Fig. S1 재현: 첫 충전을 25/50/75/100 % 로 끊고 이후 방전을 본다.
   층이 유지되면 H1; 뒤 사이클에서 따라 올라오면 활성화가 아니라 **동역학**(H2/H3) 이다.
3. **H2** — 탄소+SE 만의 펠릿 전자 전도도(두께 방향) 와 AB→AB+CNT(소량) 치환 비교.
4. **H3** — 혼합 경로별 Li2S 입도·XRD 를 [[mixing-equipment-ball-mill-thinky]] 양식으로 기록하고
   활성화량과 대응.

## Status Log
- [2026-09-11] active — 카드 개설. 근거는 Kim 2023(액체계) 하나와 사용자 진술뿐. 다음: ASSB
  Li2S 논문 ingest 로 H3 근거·목표 단위 확인.
- [2026-09-30] active — ASSB digest 2편(Huang 2026 · Zhang 2026) 라우팅 완료. **네 가설 모두
  고체계 근거를 얻었다** (H3 는 최초). 판정이 가장 값싼 순서로 다음 두 실험이 확정됐다:
  (a) **DC 분극으로 우리 30:50:20 펠릿의 σ_e⁻·σ_Li⁺ 를 따로 잰다** — 셀 조립 없이 H2 를 가른다
  (`raw/papers/huang2026_…` §10.4, 출처 Kwok 2023 *EES* 16, 610). AB 10/20/30 wt% 로 반복하면
  "탄소가 모자란가 남는가" 가 곧장 나온다.
  (b) **첫 충전을 25/50/75/100 % 로 끊는 Fig. S1 재현** — H1. 우리가 pristine 을 쓰므로
  Zhang 2026 의 ≈270 이 우리 기준선 후보다.
  여전히 미해결: **Li2S 출발 ASSB 논문**이 더 필요하고(H1), LPSCl 산화 창 수치가 없다.
