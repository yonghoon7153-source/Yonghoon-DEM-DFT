---
title: 팩 ISC/누설 검출에서 균등화 전류가 관측을 덮는가
description: "In a liquid-cell pack, when detecting/quantifying an internal short or leakage, does the balancing current mask the observation — and if so, what separates leakage from self-discharge spread, capacity spread and the balancer itself"
created: 2026-09-22
updated: 2026-09-22
type: research-question
tags: [battery, research, pack-fault]
sources: [raw/papers/lai2025_balanced-capacity-isc-detection-modules.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
status: open
feedsInto: "bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md — §3 후보 원인 칸 · §4 구분 시험 · §5 라벨 출처 칸의 팩-결함 판"
---

# 팩 ISC/누설 검출에서 균등화 전류가 관측을 덮는가

> **`pack-fault` 섹션의 닻이다.** 팩·모듈 레벨 **결함 검출**(ISC·누설·불균형)과 **균등화가
> 그 위에 겹치는 문제**를 다루는 논문은 `pack-fault` 태그를 달고 여기로 링크한다.
> 2026-09-22 사용자 결정으로 `assb` 와 **다른 섹션**으로 열었다
> (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-f-1).
>
> **경계 두 가지** (`wiki/SCHEMA.md` Tag Taxonomy): ① **`assb` 를 같이 붙이지 않는다** —
> 액체셀 팩이다. ② **열화 모드 지분(LLI/LAM) 페이지에 이 태그를 붙이지 않는다** — 결함
> **검출**과 모드 **정량**은 다른 물음이다. 이 카드는 `assb` 의 Q1~Q8 을 쓰지 않고
> **자기 물음(P1~P6)** 을 아래에 연다.

## 본진과의 관계 — 모양은 같고 물리량은 다르다

**다르다**: 여기의 출력은 **결함 전류(mA)·결함 셀**이고, 본진([[fitting-degeneracy]] ·
[[degradation-degeneracy]])의 출력은 **열화 모드 지분(LLI/LAM_PE/LAM_NE)** 이다. 이
섹션의 어떤 결과도 본진의 결론을 직접 건드리지 않는다.

**같다 — 문제의 모양이 셋 겹친다**:
1. **두 원인 → 같은 관측.** 한 셀의 SoC 가 상대적으로 내려가는 것은 (a) 내부단락/누설
   (b) 자기방전 산포 (c) 용량 편차 어느 것으로도 생긴다. 본진의 "LLI 와 LAM 이 같은 곡선을
   만든다" 와 같은 자리다.
2. **그 위에 조작이 겹친다.** 균등화기가 전하를 실어 보내 전압 격차를 **지운다.** 본진에서
   pOCV 필터링·목적함수 항 추가가 관측을 바꾸는 것과 같은 자리이고, `assb` 계열의 조작 쌍
   (율 스윕 · 재가압)에 대응하는 것이 여기서는 **수동 ↔ 능동 균등화** 쌍이다.
3. **유일성을 아무도 재지 않았다** — 그리고 잴 재료가 지면에 있다 (아래 Evidence).

★ **그리고 이 데이터셋에는 본진이 계속 못 가졌던 것이 있다** — 정답 라벨이 **설계값**이다
(ISC 저항 55/110/165/220/330 Ω 을 알고 심었다; `NEW_MODEL_REQUIREMENTS.md` §5 의
`measured` 급). ⚠ 단 **우리 축(LLI/LAM)의 라벨이 아니다.** 저항값은 열화 모드와 무관하다.

## 질문

> 팩에서 내부단락/누설을 검출·정량할 때, **균등화 전류가 그 관측을 덮는가.**
> 덮는다면 **무엇으로 가르는가** — 누설을 자기방전 산포·용량 편차·균등화기 자체와.

## 왜 중요한가

- `bms-balancing/` 의 균등화 축이 바로 이 조작을 다룬다. 균등화가 SoH·결함 관측을 어떻게
  왜곡하는지 없으면 균등화 알고리즘 평가에 결함 셀을 넣을 수 없다.
- 1호(Lai 2025)가 균등화를 **센서로 뒤집었다** (`[인쇄]` "convert battery equalizers into the
  equivalent current sensor"). 그러면 "덮는" 자리는 사라지지 않고 **SoH 오차 · dead-band ·
  전압≠SoC** 로 옮겨간다 — 그 세 자리의 크기를 재는 것이 이 카드의 일이다.
- 경쟁 방법(Kong 2018, [39])의 약점이 `[인쇄]` "**Sensitive to balancing**" 이다 — 이 물음이
  문헌에 이미 인쇄돼 있고, 아무도 폭을 재지 않았다.

## 가설

- **H1** — 균등화는 관측을 덮지 않고 **옮긴다**: 균등화 적분 자체가 누설의 관측이 되되, 그
  값의 유일성은 **SoH 입력의 정확도**에 걸린다 (1호 Fig. 7: 330 Ω 에서 SoH ±2 % → 누설 >100 %).
- **H2** — **자기방전 산포 방향은 정확 null** 이다: 셀 `l` 의 자기방전 증가와 ISC 누설은 전하
  수지 식에서 같은 항이라 어떤 균등화 관측으로도 갈리지 않는다. 가르려면 **다른 채널**(온도·
  전압 회복·부하 방향 반전)이 필요하다.
- **H3** — 수동 ↔ 능동 쌍은 **직교하지 않는다**: 능동 환류가 SoC 를 바꾸면 누설 `V/R` 도 바뀐다.

## 이 섹션의 자기 물음 — P1~P6 (수집 지침)

| # | 뽑을 것 | 왜 |
|---|---|---|
| P1 | **결함 라벨의 층위** — designed / derived / measured, 허용오차 유무 | 1호는 designed-R → derived-I |
| P2 | **후보 원인 칸** — 누설·자기방전·용량 편차·온도 중 무엇을 칸으로 두고 무엇을 가정으로 닫았나 | H2 |
| P3 | **dead-band 와 신호 크기** — 균등화 임계(mV·% SoC)와 누설이 만든 총 SoC 격차의 비 | 1호: 둘이 같은 크기(≈1 %)인데 오차 5 % — 미설명 |
| P4 | **수동 ↔ 능동을 같은 프로토콜에서 비교했나** | 1호 Test 5 는 프로토콜 혼입 |
| P5 | **균등화 없는 대조군**이 있나 | 1호 없음 (방법이 균등화 전제) |
| P6 | **유일성·폭** — SoH 등 nuisance 를 흔들 때 결함 추정치가 얼마나 움직이는지 결과표 옆에 붙였나 | 1호: 그림으로 재고 표에 안 붙임 |

### 수집 현황 — P1~P6 채움표

| 논문 | P1 라벨 | P2 원인 칸 | P3 dead-band | P4 같은 프로토콜 | P5 무균등화 대조 | P6 폭 |
|---|---|---|---|---|---|---|
| **Lai 2025 (`pack-fault` 1호)** | **designed-R** (55–330 Ω, 허용오차 없음) → **derived-I** (`V̄/R`) · SoH 기준 **measured**(프로토콜 없음) · 추정 SoH **fitted** | **용량 편차만 칸** (SoH 정규화). **자기방전은 정의로 배제**(`[인쇄]` 각주 2 "focuses on … current leakage, rather than the internal change") · 온도 고정 · 다중 셀 배제(식 9a) | **10 mV ≈ 1 % SoC**, 10 mA → 5 h. `[재현]` 330 Ω 시험의 총 누설 격차 ≈1.0 % = dead-band 인데 오차 5 % — **미설명** | **Tests 1–4 예**(FUDS) · **Test 5 아니오**(능동 5 사이클 ≈870 min ↔ 수동 2 사이클 ≈720 min) | **없다** | **없다** (`identifiab*`·`uniqu*`·`uncertaint*`·`error bar` 0 회). ★ 단 **Fig. 7 이 폭이다**: `[도표]` SoH_1 ±2 % → 330 Ω 누설 **>100 %**; 표에는 오차 한 숫자 |

## Evidence For (균등화가 관측을 덮는다 / 옮긴다)

- **2026-09-22, Lai 2025 (`raw/papers/lai2025_balanced-capacity-isc-detection-modules.md`)**:
  - 논문 자신이 세 기제를 인쇄한다 — `[인쇄]` "the controlling threshold of the balancing
    hardware is **10 mV**, corresponding to a SoC difference of about **1 %**" · "batteries
    with the **same voltage may not necessarily share same SoC**" · SoH 추정 "typical error of
    about **2 %**" → 권고 `[인쇄]` "**longer profile (e.g., > 10 h)**".
  - `[도표]` Fig. 3 vs 4: **같은 누설 셀의 서명 부호가 균등화 방식에 따라 반대**다 (능동 +0.23 Ah
    / 수동 −0.08 Ah, 55 Ω). `[재현]` 공개 데이터로 그 차이가 **환류 전하 0.714 Ah(6 셀 공통)**
    임을 확인 — 데이터셋 entity [[isc-balancing-dataset-est-d-24-12331]].
  - `[도표]` Fig. 8: Test 5 에서 **SoH 민감도가 능동 ≈0.13 %/% ↔ 수동 ≈6 %/% (≈45 배)** —
    본문은 `[인쇄]` "less influenced by the balancing method" 라 적는다. ⚠ 프로토콜 혼입(P4).
  - `[도표]` Fig. 5(b): 충전 구간이 있는 프로파일에서 **누설 셀이 최소 방전 셀이 아니다** —
    "누설 셀 = 균등화가 가장 적게 건드린 셀" 이라는 직관이 **부하 방향에 따라 깨진다.**
    본문 무언급.

## Evidence Against (덮지 않는다 — 균등화가 곧 관측이다)

- **2026-09-22, Lai 2025**: 참 SoH 를 주면 **10 조건 전부 |오차| < 1 mA** (Table 3/4; 상대
  0.1–7 %). `[재현]` 공개 데이터의 균등화 적분(열 12 + 열 13)이 논문 Fig. 3/4 의 balanced
  capacity 를 **0.01 Ah 안에서 재현**한다 — 균등화기의 기록이 그대로 관측이 된다는 논문의
  전제는 데이터로 성립한다.
- ⚠ 그러나 이것은 **SoH 를 알 때**의 이야기다. 추정 SoH 로 돌린 결과는 **2 개 숫자**(Table 6)
  이고 그중 수동 1 개는 **공개 데이터에서 깨진 파일**(`165_passive`)에 해당해 재현 불가.

## 새 제약 (1호가 준 것)

1. **자기방전 방향은 어떤 균등화 관측으로도 안 갈린다** (H2, 정확 null). 이 섹션의 "ISC" 는
   라벨에 "**한 셀의 초과 누설**" 이라고 적어야 한다.
2. **결과표에 폭을 붙여야 한다** — 1호의 Fig. 7 을 `(i_L, SoH_l)` 평면의 근최적 집합으로 다시
   그리는 것이 첫 실험 후보 ([[near-optimal-set-width-measurement]] 의 기계를 그대로).
3. **구분 시험 후보 하나**: **부하 방향 반전** — 누설은 방향 무관 방전이므로 방향을 바꿔도
   남는 성분이 누설이다 (1호 Fig. 5(b) 가 우연히 보여 준 것). 미실행.

## Status Log

- [2026-09-22] open — 섹션 개설 (사용자 결정, `ASSB_TRANSFER_NOTE.md` §6-3-f-1). 1호 Lai 2025
  흡수: `ISC_LEAKAGE_DATASET.md` §5 의 7 물음 중 **6 개 닫힘**(셀 #1 · Ω/사양 · 165=설계 ·
  검출+정량/폭 없음 · 균등화 영향 · 누설=derived), **17 열은 논문 무언급으로 미해결.**
  P1~P6 채움표 1 행. 공개 데이터 2 파일로 Fig. 3/4 재현 확인. 재현 불가 원장(`165_passive`)
  → entity.

## 이 카드가 주장하지 않는 것

- 1호의 방법이 틀렸다고 주장하지 않는다 — 폭이 없다는 것과 라벨의 뜻을 적었다.
- 이 팩에 실제로 자기방전 산포가 있었다고 주장하지 않는다.
- 이 섹션의 결과가 본진 LLI/LAM 결론에 쓰인다고 주장하지 않는다.

## 관련

- [[fitting-degeneracy]] — 모양이 같은 이웃 (물리량은 다름)
- [[isc-balancing-dataset-est-d-24-12331]] — 이 섹션의 유일한 measured 급 라벨 데이터
- [[near-optimal-set-width-measurement]] — P6 을 잴 기계
- `bms-balancing/docs/ISC_LEAKAGE_DATASET.md` · `bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md`
  §3·§4·§5 (repo-root 상대 경로, 내용 복사 금지)
