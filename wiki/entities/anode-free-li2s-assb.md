---
title: Anode-free Li2S ASSB
description: "reference cell 이 끝난 뒤 Li–In 음극을 anode-free 구성으로 바꾸는 2단계 프로젝트 — Li 원천이 양극(Li2S)에만 있으므로 첫 사이클 손실과 Li 침적 균일성이 전부다"
created: 2026-09-11
updated: 2026-10-06
type: entity
tags: [project, satellite, anode-free, li2s, assb]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md, raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md, raw/papers/park2026_low-pressure-operation-carbon-coated-current-collector-asslsb.md, raw/papers/kimjt2023_mixed-discharge-products-li2s2-li2s-asslsb.md, raw/papers/hong2026_high-valence-cation-lattice-expansion-activating-li2s.md, raw/papers/feng2026_anode-free-asslsb-fe-stabilized-polysulfides.md, raw/papers/gao2024_cu-i-codoping-activating-li2s-redox-kinetics-assb.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# Anode-free Li2S ASSB

## 개요

[[li2s-assb-reference-cell]] 의 다음 단계. Li–In 음극을 빼고 집전체 위에 Li 를 **셀 안에서
처음으로** 석출시키는 anode-free 구성. 계획 단계이며 실험은 시작되지 않았다 (2026-09-11).

## 왜 Li2S 여야 가능한가

Li2S 는 방전 상태의 활물질이라 **Li 원천이 양극에 있다**. 그래서 Li-free 음극(흑연·Si·집전체만)이
가능하다 — Kim et al. 2023 이 도입부에서 그대로 쓰는 논거이고(`raw/papers/kim2023_…` §2.2),
그 논문은 흑연 음극(N/P 1.2)으로 800 사이클을 돌렸다. anode-free 는 그 극한(N/P → 0)이다.

## 이 구성이 참이려면 참이어야 하는 것

1. **첫 충전에서 Li2S 가 충분히 활성화**되어야 한다 — 활성화 안 된 Li2S 는 뒤 사이클에서도
   깨어나지 않는다(Kim 2023 Fig. S1, [[li2s-activation-first-charge]]). anode-free 는 Li 재고가
   양극 활성화량 **그 자체**다.
2. **첫 사이클 비가역 손실이 작아야** 한다 — SEI 형성·SE 분해·Li 데드 형성이 전부 재고에서 빠진다.
3. **Li 침적이 균일**해야 한다 — Kim 2023 의 Li 금속 파우치 반쪽셀조차 중심부 Li 고갈로 30 사이클
   뒤 CE 가 요동했다(Fig. S10). 초기 Li 가 0 인 구성은 여유가 더 없다.
4. **스택 압력·집전체 계면**이 침적 형태를 정한다 — **2026-09-30 에 근거가 들어왔다**
   (아래 "근거: Zhang 2026" 절).

## 근거: Zhang 2026 (anode-free ASSLSB, 저압, Na 집전체)

`raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md` —
이 프로젝트를 **정면으로** 겨냥한 첫 논문이다. 위 4번 항목이 이것으로 채워진다.

### 집전체 — Cu 는 안 된다, Na 는 된다

| 관측 `[인쇄]` | 무엇을 말하나 |
|---|---|
| 대칭셀 계면저항 **Cu–Cu ≈140 vs Na–Na ≈26.5 Ω cm²** | Cu 는 황화물 SE 와 **접촉 불량 + 부식** |
| Li–Cu 반쪽셀은 **60 사이클에 단락** | Cu 집전체로는 anode-free 가 성립하지 않는다 |
| Na 항복강도 **0.19–0.28 MPa** → 1 MPa 에서도 소성변형으로 밀착 | **연성 집전체**가 저압 운전을 가능케 한다 |
| Li 은 Na 박 **위가 아니라 Na/SE 사이에** 깔린다 | 침적 위치가 집전체 연성에 따라 달라진다 |
| Li–Na 첫 사이클 CE **85.57 %**, 1000 사이클 평균 **99.857 %** | `[재현]` 고정 재고로는 200 사이클 누적 **75 %** 소모 |

### 스택 압력 — 무압은 불가

`[인쇄]` 운전 스택압 **0 / 1 / 4 MPa** 를 비교했고 in-situ 실측은 3.2–3.8 / 1.2–1.4 MPa.
**0 MPa 는 60 사이클에 붕괴한다.** 성형 압력(SE 250 MPa · 양극 400 MPa)과 운전 압력은
**다른 축**이며 이 논문은 둘을 구분해 적은 드문 사례다 (Huang 2026 은 운전압을 아예 안 적었다).

#### ★ 2026-10-06 — "표준 운전 압력" 같은 것은 문헌에 없다

digest 가 16편이 된 지금 운전 압력의 문헌 좌표는 이렇다:

| 논문 | 운전 압력 | 근거를 댔는가 |
|---|---|---|
| **Qu 2025** | **7 MPa** | 정압/정용적 fixture 를 자작해 **변위·압력을 실측** ✓ |
| **Zhang 2026** (이 절) | **0 / 1 / 4 MPa** 비교 | in-situ 실측 ✓, **0 MPa 는 60사이클에 붕괴** |
| **Zhang (Jiaxu) 2026** | **15 / 30 / 100 MPa** | **압력별 EIS 로 골랐다** ✓ — `[인쇄]` **무압 356 Ω**, 1·3·5·10 MPa 에서 감소, **15–100 MPa 거의 불변(포화)** |
| **Jeong 2026** · **Gao 2024** | **50 MPa** | 근거 없음 |
| **Kim JT 2023** | **150 MPa** | 근거 없음 |
| **Hong 2026** | **200 MPa** | 근거 없음 — 이 위키 최고치 |
| **Feng 2026** | **50 MPa** | 그림 주석에만. ★ 그 대신 **압력–온도 교환을 명시**한다 (아래) |
| **Park 2026** | **1 → 75 MPa 7단계 스캔** | ✓ **같은 셀에서 3사이클씩** — 이 위키 최고 해상도. 10 MPa 상온 350사이클 78 % |

→ **0–200 MPa 로 흩어진다** (유효 좌표만 봐도 7–150 MPa, **21배**). 그래서 이 위키는 어떤 문헌값도
"표준" 으로 가져오지 않고 **우리 fixture 의 압력을 재서 적는다.** 압력 축은 2026-10-06 에 별도
카드로 분리했다 → [[operating-stack-pressure-floor]].
★ **그리고 고압 논문의 성능은 접촉 문제가 지워진 상태의 수치**이므로 저압에 외삽되지 않는다 —
Hong 200 MPa · Kim JT 150 MPa 의 수명을 우리 조건의 기대값으로 쓰면 안 된다.

★ 두 가지를 더 기억한다.
1. **무압이 불가하다는 독립 근거가 둘이 됐다** — Zhang 2026 의 "0 MPa 60사이클 붕괴" 와
   Zhang Jiaxu 2026 의 **"0 MPa 에서 356 Ω"** 이다. 후자는 **셀을 죽이지 않고 숫자로** 보여준다.
2. **저압은 공짜가 아니다.** 같은 Zhang Jiaxu 2026 안에서 **15 MPa 50사이클 `[도표]` ≈69 %
   vs 30 MPa 50사이클 94.3 %** — 압력 2배로 유지율이 **25 %p** 바뀐다. 그 논문의 헤드라인
   사이클 수(4,500 / 30,000 / 140,000)는 **전부 100 MPa** 이고 저자 스스로 `[인쇄]`
   "impractical for real-world applications" 라 쓴다.

→ **우리가 가장 먼저 할 측정은 압력-EIS 스윕(0/1/3/5/10/15/30 MPa)** 이다. 셀 1개 반나절이면
우리 운전 압력에 근거가 생긴다 ([[reference-cell-500-600-mahg]] 2026-10-06 에서 2순위로 올렸다).

### ★★ 2026-10-06 — "anode-less" · "Li-metal-free" 는 anode-free 가 아니다

`feng2026_…` 가 이 프로젝트의 **정의를 명문화해야 할 경계 사례**다. 제목이 **"Anode-less"** 이고
초록이 Li-metal-free 를 내세우는데, 실제 공정은 이렇다 — `[인쇄]` KB : MCMB = **3 : 7 wt** 탄소
복합음극(33.8 µm, 공극률 34.5 %)을 만들고 **셀을 조립한 뒤 "stoichiometric amount" 의 Li 박을
눌러 붙여 80 °C 8 h 프리리튬화**한다.

| | 뜻 |
|---|---|
| **anode-free** (우리 2단계 목표) | **Li 원천이 양극(Li2S)에만 있다.** 음극 쪽에 Li 을 넣는 공정이 없다 |
| **"anode-less" / "Li-metal-free"** (이 논문) | **완성된 셀에 Li 금속 층이 없다.** Li 금속 공정은 **그대로 있다** |

→ **제조 이점이 없다.** 그리고 **그 Li 양이 "stoichiometric" 이라고만 적혀 있어 실제 Li 재고 비를
아무도 계산하지 못한다.** 이 위키는 이 셀을 **"프리리튬화 탄소 호스트 음극"** 으로 분류하고,
우리 단계로는 **2.5단계**(1단계 Li–In 과 2단계 anode-free 사이)로 적는다.
`[해석]` 문헌을 읽을 때 **"anode-free" 라는 단어를 믿지 말고 음극 공정에 Li 금속이 등장하는지**
본다. 그것이 이 프로젝트의 성패를 가르는 유일한 질문이다.

#### ★ N/P 를 적은 드문 논문 — 그런데 그 N/P 는 Li 재고 비가 아니다

`[인쇄]` **N/P = 1.03**. 식이 `[재현]` 으로 정확히 복원된다:

```
음극 수용량 = 33.8 µm × 0.345(공극률) × 0.534 g cm⁻³(ρ_Li) × 3861 mAh g⁻¹ = 2.40 mAh cm⁻²
N/P = 2.40 ÷ (1166 mAh g⁻¹(Li2S) × 2 mg cm⁻²) = 2.40 ÷ 2.332 = 1.029  ✓
```

★ **두 가지를 읽어야 한다.**
1. **분모가 이론용량이다.** 실측 첫 충전(1.72 mAh cm⁻²)으로 바꾸면 `[재현]` **N/P = 1.40** 으로
   Gao 2024 의 코인셀 1.64 와 같은 급이 된다. **"N/P 1.03" 은 보수적으로 보이지만 실제로는 아니다.**
2. **프리리튬화 Li 이 분자에도 분모에도 없다.** 즉 이 N/P 는 **호스트의 공간 비**이고
   **Li 재고 비가 아니다.** 게다가 분자는 **공극을 Li 로 100 % 채운다는 가정**이라 낙관적 상한이다.

→ **그래도 그 식 자체는 우리에게 바로 쓸 수 있다**: `음극 호스트 두께 × 공극률 × 0.534 × 3861 ÷
양극 면적용량`. 우리가 anode-free 로 갈 때 **집전체 위에 Li 이 들어갈 공간이 있는지**를 셀을
만들기 전에 계산하는 식이다. **단 분모는 반드시 실측 면적용량으로 쓴다.**

#### ICE 좌표 (2026-10-06 갱신)

| ICE | 논문 | 읽는 법 |
|---|---|---|
| **110–113 %** | Yu 2024 (CuS) | 방전 > 충전 — **Cu 가역 → Li 재고 순손실** |
| **>120 %** (축 상단 잘림) | **Feng 2026 의 pristine Li2S 대조셀** | `[도표]` CE 108·112·117 % 로 올라가다 1.5 C 구간에서 축을 넘는다. 저자는 "slightly exceeding 100 %" 로만 쓰고 **Li–In 재고 소모 가능성을 배제하지 않는다** |
| **99 %** | **Feng 2026 (FLS 반쪽셀)** | 이 위키 최상위권. 이후 CE 98–102 % 로 깨끗하다 |
| **≈92 %** `[재현]` | Feng 2026 풀셀 | ★ **논문이 풀셀 ICE 를 보고하지 않는다** — 그림 마커에서 역산한 값이다 |
| 89 % | Liu 2026 (Li4SnS4) | Sn 불변 → **먹는 서명 없음** |
| 85.2 % | Gao 2024 | |
| 83 % | Cronk 2026 anode-free 파우치 | |
| 72.7 % `[재현]` | Gao 2024 파우치 | |
| **첫 방전 = 첫 충전의 1.5–1.6배** | Park 2026 | **압도적 최악** — Li–In 재고 + SE 환원에서 Li 가 왔다. anode-free 외삽 불가 |

`[해석]` **CE 가 100 % 를 넘는 것은 좋은 신호가 아니다** — anode-free 에서는 **음극 Li 이 양극으로
넘어오고 있다**는 뜻일 수 있다. 우리는 **첫 사이클 CE 와 이후 수십 사이클 CE 를 함께** 보고,
**100 % 를 넘으면 그만큼을 Li 재고 손실로 가정**한다.

#### Li 재고를 먹지 않는 첨가제 — Liu 2026 이 반례를 준다 (2026-10-06)

anode-free 에서 첨가제의 1차 비용은 **무게가 아니라 Li 재고**다. 첫 사이클에 Li 을 먹는
첨가제는 음극에 깔 Li 을 그만큼 줄인다. 두 사례가 정반대다:

| | **Yu 2024 CuS** | **Liu 2026 Li4SnS4** |
|---|---|---|
| 첫 사이클 CE | **110–113 %** (방전 > 충전) | **89 %** (방전 < 충전) |
| 중심금속 | CuS ↔ Cu₂₋ₓS **가역** (Li 을 왕복시킨다) | **Sn⁴⁺ 불변** (ex situ XPS 9지점) |
| anode-free 관점 | **순손실** — 먹은 Li 이 양극에 갇힌다 | **먹는 서명이 없다** |

`[해석]` 그래서 첨가제를 검토할 때 **ICE 와 중심금속의 산화상태 가역성을 함께** 본다.
Liu 의 ICE 89 % 는 **Cronk 2026 의 anode-free 파우치 ICE 83 % 보다 높다.**
⚠ 단 Liu 의 셀은 anode-free 가 아니라 **Si 음극 파우치**이고, 펠릿셀 음극은 논문에 안 적혀 있다.

### anode-free 의 진짜 손실 구간 `[해석]`

full cell 첫 CE **≈68–73 %** 이고 **초기 5 사이클에 ≈45 % 를 잃는다.** 이것이 Li 재고가
사라지는 구간이다 — 그런데 **논문은 이 손실을 한 번도 설명하지 않는다** (digest §12-1).
anode-free 논문에서 **Li 재고 수지를 한 줄도 쓰지 않은 것**이 이 논문의 가장 큰 결함이고,
우리가 채워야 할 자리다.

### 우리가 바로 쓸 진단 2개 `[인쇄]`

1. **충전 중 압력 상승 = Li 석출.** 압력 셀이 있으면 침적을 직접 본다.
2. **방전 말기 ≈1.65 V 단차 = Li 재고 소진 신호** (Fig. S11). 재고가 마르면 곡선에 단이 생긴다.

### 이 논문이 답하지 않는 것

- Na 의 **0.4 V 기생 산화**가 Li 스트리핑 피크보다 크다 (Fig. S9) — 그 몫이 무엇인지 불명.
- full cell **사후 Na 분석이 없다** — 1000 사이클 대칭셀 결과를 full cell 에 그대로 옮길 수 없다.
- 전해질층이 **127 mg cm⁻² (복합양극의 27배)** 라 셀 수준 에너지밀도 계산이 논문에 아예 없다.
- 그들의 Li2S 는 **반응형**(PI3 경로, 실제 43.8 wt% PI3)이다. 우리 pristine 경로와 다르다 —
  [[reference-cell-500-600-mahg]] H1·H3 참조.

## 상태

- **2026-09-11** — 계획. reference cell 이 목표를 달성하면 착수. 그전에 anode-free ASSB 문헌
  (Li 석출 균일성·집전체 코팅·압력) 을 ingest 해 이 페이지의 4번 항목을 채운다.
- **2026-09-30** — 4번 항목 채움 (Zhang 2026). 결론 셋: **Cu 집전체는 배제**(60 사이클 단락) ·
  **무압 운전 배제**(0 MPa 60 사이클 붕괴, 최소 1 MPa) · **초기 5 사이클 45 % 손실이 진짜 과제**다.
  다음에 필요한 것: 연성 집전체가 **Na 여야 하는지**(In·Ag·Sn 대안), 그리고 **Li 재고 수지를
  정량하는 방법** — 이 논문에 없다.

## 관련

- [[li2s-assb-reference-cell]] — 선행 프로젝트
- [[reference-cell-500-600-mahg]] — 그쪽 답이 이쪽의 Li 재고 상한을 정한다
- [[li2s-activation-first-charge]]
