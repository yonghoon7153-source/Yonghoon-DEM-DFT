---
title: Anode-free Li2S ASSB
description: "reference cell 이 끝난 뒤 Li–In 음극을 anode-free 구성으로 바꾸는 2단계 프로젝트 — Li 원천이 양극(Li2S)에만 있으므로 첫 사이클 손실과 Li 침적 균일성이 전부다"
created: 2026-09-11
updated: 2026-09-30
type: entity
tags: [project, satellite, anode-free, li2s, assb]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md]
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
