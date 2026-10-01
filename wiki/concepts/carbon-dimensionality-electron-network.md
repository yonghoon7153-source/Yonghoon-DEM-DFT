---
title: 도전재 차원 분리 — 2D 접촉 vs 1D 네트워크
description: "절연체 Li2S 양극에서 탄소의 두 역할(접촉면적 vs 장거리 전자 경로)을 차원이 다른 탄소로 나눠 맡기는 설계 — Kim 2023 의 Gr/CNT 근거와 우리 AB 단일 탄소에의 함의"
created: 2026-09-11
updated: 2026-10-06
type: concept
tags: [carbon, composite-cathode, li2s, activation, liquid-electrolyte]
sources: [raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kwok2023_interfacial-redox-mediator-high-performance-asslsb.md, raw/papers/gao2024_cu-i-codoping-activating-li2s-redox-kinetics-assb.md, raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
---

# 도전재 차원 분리 — 2D 접촉 vs 1D 네트워크

## 정의

절연체 활물질(Li2S) 양극에서 도전재가 해야 하는 일은 둘이다: (a) 활물질 표면과 **넓게 닿아**
전자를 주고받는 것, (b) 전극 **두께 방향으로 끊기지 않는** 전자 경로를 만드는 것. Kim et al.
2023 (`raw/papers/kim2023_…`)은 (a)를 2D 그래핀에, (b)를 1D MWCNT 에 나눠 맡기고 두 역할이
**분리 가능하고 서로 대체되지 않음**을 보였다.

## 근거 (Kim 2023)

| 관측 | 무엇을 말하나 |
|---|---|
| 탄소만 펠릿의 두께 방향 I–V: Gr/CNT 가 Gr 보다 `[인쇄]` ~35 % 높은 전류 (Fig. 1D) | 그래핀은 in-plane 은 좋지만 through-plane 이 약하다; CNT 가 그 축을 잇는다 |
| 첫 충전 활성화: Gr/CNT > Gr ≫ CNT-only (Fig. 4A; CNT-only 는 `[도표]` 방전 ~630 mAh g⁻¹(S)) | 1D 탄소만으로는 micro-Li2S 가 활성화되지 않는다 — 접촉면적이 필요 (단 CNT 25 wt% 조건, G8) |
| CNT 비율 스윕 (Fig. S4): 7:1(**3.125 wt%**) 만 Gr 단독보다 낫고 4:1 은 동등, 1:1 은 크게 나쁨 | 네트워크용 탄소는 **소량**이 최적; 과량은 접촉용 탄소를 대체해 활성화를 깎는다 |
| 사이클 후 (Fig. 5): Li2S/Gr 은 ~50 사이클에 급사, 표면이 sulfate·polythionate 로 passivation; Gr/CNT 는 CNT 형태 온존·passivation 적음·Li2S XPS 피크 잔존 | 접촉 탄소 표면이 죽어도 **네트워크 탄소가 전도 경로를 유지**하면 셀이 산다 |
| 50 % SoC cryo-TEM: Gr/CNT 는 <10–100 nm 로 고르게, Li2S/Gr 은 200–500 nm 큰 Li2S 잔존 (Fig. 7 vs S6) | 네트워크가 있어야 전극 전체가 **균일하게** 반응한다 |

## 우리 셀에의 함의 (`[해석]`)

- 우리 [[li2s-assb-composite-cathode]] 의 도전재는 **acetylene black 단일**(20 wt%)이다.
  AB 는 0D 입자 사슬이라 접촉도 네트워크도 "어느 정도" 하지만 어느 쪽도 최적은 아니다.
- Kim 2023 의 처방을 옮기면: AB 의 **일부(수 wt%)를 CNT 로 대체**해 두께 방향 네트워크를
  더하는 실험이 값싸다. 단 고체계에서는 탄소가 SE 를 밀어내 **이온 경로**를 끊을 수 있으므로,
  탄소 총량은 늘리지 않고 **구성만 바꾸는** 것이 첫 실험이다.
- 검증은 Kim 2023 의 논증 순서를 그대로 쓴다: (i) 탄소+SE 만의 펠릿 전자 전도도 → (ii) 첫 충전
  활성화량 → (iii) 사이클 후 단면 — 세 단계가 같은 방향을 가리켜야 "네트워크 효과" 다.

## 이 위키에서의 적용

- [[reference-cell-500-600-mahg]] H2(퍼콜레이션 제한) 의 구체안.
- [[composite-cathode-mixing-routes]] ② two-step 은 탄소 골격을 먼저 만드는 경로라 이 개념과 결합된다.
- [[li2s-activation-first-charge]] — 접촉 탄소가 활성화를, 네트워크 탄소가 수명을 맡는다는 분업.

## 2026-10-01 — 고체계에서는 이 개념의 전제가 흔들린다

이 개념은 **액체계 논문 하나**(Kim 2023)에서 왔고 "전자 경로를 잘 잇는 것이 좋다" 를 전제한다.
고체계 ASSB digest 네 편이 그 전제를 직접 건드렸다 — Yu 2024 는 복합체 전자 전도도를 **200배
낮추고도** 이용률을 올렸고, Huang 2026 은 **14배 올려서** 비슷한 개선을 얻었다.
→ 논지와 반론은 [[interface-quality-not-bulk-conductivity]] 에 있다.
이 개념의 "접촉 vs 네트워크" 분업 자체는 유효하지만, **고체계에서 그 분업의 상대가 탄소가
아니라 SE·첨가제·계면상일 수 있다**는 단서를 달고 읽어야 한다.

## ★ 2026-10-06 — 탄소를 **아예 넣지 않는** 선택지가 있다 (Kwok 2023)

이 개념이 암묵적으로 전제하던 것은 "복합양극에 탄소가 들어간다, 문제는 몇 차원·몇 wt% 냐" 였다.
**Kwok 2023 (*EES* 16, 610, Nazar) 의 양극에는 탄소가 0 wt% 다** — Li2S : LiVS2 : LPSCl =
`[인쇄]` **30 : 20 : 50 wt%** 이고 Fig. 1B 범례에도 탄소 입자가 없다. 그 셀이 상온 1 mA cm⁻² 에서
**1,000 사이클**을 돈다.

전자를 나르는 것은 **활물질을 감싼 <30 nm LiVS2 껍질**(혼합전도체)이다. 즉 **"탄소가 전자망을
만든다" 가 유일한 설계가 아니다** — 활물질 표면 자체를 전도성으로 만들면 탄소가 하던 일을
가져간다. 그리고 그 껍질은 전자만이 아니라 Li⁺ 도 나른다: `[인쇄]` SE 를 하나도 안 섞은 LVS
분말이 이미 σ_Li⁺ = **1.3×10⁻⁵ S cm⁻¹** 다 (Li2S 자체는 10⁻⁹ 급).

`[해석]` 우리 AB 20 wt% 에 대한 함의는 "AB 를 빼라" 가 아니라 **"AB 20 wt% 가 무슨 일을 하는지를
먼저 측정하라"** 다. 탄소 없이도 되는 셀이 있다면, 우리 AB 가 **전자망으로서 필요한 양**과
**부피를 먹는 양** 중 어느 쪽에 더 가까운지가 열린 질문이 된다
([[dc-polarization-conductivity-separation]] 의 `AB 10/20/30 wt%` 스윕).
대조 좌표: **Gao 2024 는 VGCF(1D) 10 wt% 단일**로 2.4 mA cm⁻² 를 돌린다.

### ⚠ raw digest 정정 — `yu2024_…` 의 G16 전제가 틀렸다

`raw/papers/yu2024_…md` 의 공백표 **G16** 은 Fig. 4a 참조 패턴에 "CNT" 가 끼어 있는 것을 보고
*"같은 그룹 Kwok 2023 *EES* 16, 610 의 양극이 CNT 를 쓴다"* 를 근거로 **Yu 의 양극에도 CNT 가
들어갔을 가능성**을 제기했다. **그 전제가 사실이 아니다 — Kwok 2023 의 양극에는 탄소가 전혀
없다** (조성 30:20:50, Fig. 1B 범례).
raw 는 불변(하드룰 3)이므로 **정정은 여기 2층에 남긴다.** G16 의 **관측**(참조 패턴에 CNT 가
있는데 본문이 한 번도 언급하지 않는다)은 **그대로 유효**하고, **추론의 근거만 무효**다.
Yu 의 양극에 탄소 도전재가 따로 들어갔는지는 **여전히 SI 없이는 확정 불가**다.

## 한계·불확실성

- 근거가 액체계 논문 하나다 (`single-source`). 액체계의 passivation 화학(sulfate·polythionate)은
  고체계에 그대로 있지 않다 — 대신 SE 분해물이 같은 자리를 차지할 수 있다 (미검증).
- Kim 2023 의 CNT 최적값(3.125 wt%)은 Gr 기반 조성에서의 값이며 AB 기반에 이식되지 않는다.
