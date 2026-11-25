---
title: Nd₂O₃ 도핑 — 열역학 창과 전자구조가 **같은 방향으로** 진다
date: 2026-08-12
updated: 2026-08-12
tags: [nd, lpscl, esw, gap, doping]
status: 진행
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
targetVenue:
---

## Thesis

Nd₂O₃ 를 LPSCl1.6 에 넣으면 **intrinsic ESW 가 좁아지고**(0.90 → 0.40 V),
그 창 밖에서 나오는 Nd 생성물이 **전자를 못 막는다**(Nd₂S₃ 0.77 eV) — 독립된 두 축이
같은 결론을 가리킨다.

## Argument

### 축 1 — 열역학 (grand-potential ESW, MP GGA+U hull)

`db/properties/nd_doped_lpscl_esw.json` · 원자료 `tools/oxidation/esw_nd_result.txt`
(gabia 2026-06-24). modelc 를 **같은 6원소 hull(Cl-Li-Nd-O-P-S, 321 엔트리)에서
재실행**한 것이 대조군이고, 4원소 hull 결과를 정확히 재현했다 — 즉 아래 차이는
hull 아티팩트가 아니라 진짜 O/Nd 화학이다.

| | 환원 한계 | OCV | 산화 onset | intrinsic 창 |
|---|---:|---:|---:|---:|
| nd (Nd₂O₃ 도핑) | 1.52 V | 1.72 V | **1.92 V** | **0.40 V** |
| modelc (대조) | 1.24 V | 1.72 V | 2.14 V | 0.90 V |

Nd-S/P/O redox 가 **modelc 창 안에서** 일어나 창을 양쪽에서 갉아먹는다.
산화 onset 이 1.92 V 로 내려간 것이 핵심이다 (modelc 2.14 V).

### 축 2 — 전자구조 (우리 QE, PBE frozen-4f)

`db/properties/sei_electronic.json` `*_frozen4f`. 1.52–2.45 V 구간 생성물이
전부 좁은 갭/전도성이다. **wide-gap passivation 은 2.45 V(NdPO₄) 부터**다.

| 상 | gap (eV) | |
|---|---:|---|
| Nd₂O₃ | 3.948 | 절연체 (MP 3.81, +3.6%) |
| LiNdO₂ | 3.698 | 절연체 |
| **Nd₂S₃** | **0.770** | **좁은 갭 — Li₃P(0.709) 옆자리** |

Nd₂S₃ 는 **OCV(1.72 V) 자가분해 생성물**이다:
`nd → 0.925 Li₃PS₄ + 0.1 Nd₂S₃ + 0.1 Li₂S + 0.075 Li₃PO₄ + 1.6 LiCl`.
전극 계면이 아니라 **벌크에서, 전류 없이도** 나온다. 국소가 아니라 전체다.

### 두 축이 독립이라는 점

축 1 은 MP 엔트리의 형성에너지(전체 hull), 축 2 는 우리 QE 의 fixed-occ 고유값이다.
데이터 출처도 방법도 다르다. 그런데 같은 곳을 가리킨다 — "Nd 는 창 안에서 반응하고,
그 산물이 전자를 흘린다".

## Counter-arguments

**(a) "HSAB 로는 Nd³⁺ 가 하드 산이라 O 를 붙들어야 한다 — Nd₂S₃ 가 생기면 안 된다."**
→ **반박됨.** 선호도 논증은 **재고가 충분할 때만** 성립한다. x=0.2 면 O 가 모자라
Nd 를 다 채울 수 없고, hull 은 남는 Nd 를 황으로 보낸다. V=0 에서도
`0.3 Li₂O + 0.8 Li₃P` 로 **Li₃P 가 여전히 우세**하다 — O 는 부분 전환만 한다.
(2026-08-12 에 이 논증을 폈다가 hull 로 직접 반증됨. 선호도 ≠ 화학량론.)

**(b) "MP 에너지라 우리 QE 와 정합하지 않는다."**
→ 절반 유효. 축 1 의 절대 전압을 우리 DFT 값처럼 인용하면 안 된다. 다만 nd 와
modelc 를 **같은 hull 에서** 비교했으므로 *차이*(0.40 vs 0.90 V)는 살아 있다.
축 2 는 우리 값이고 둘을 섞지 않았다.

**(c) "PBE 갭은 30–50% 과소니 0.77 eV 도 실제로는 1.2–1.5 eV 아닌가."**
→ 유효하지만 결론을 안 바꾼다. 절대값이 아니라 **무리**가 문제다 — 같은 과소 보정을
받아도 Nd₂S₃ 는 Li₃P(0.709) 무리에 남고 절연체 무리(3.4~6.3)로 안 간다.
⛔ 절대값 인용 금지, 순위로만.

**(d) "OCV 분해가 열역학이지 속도가 아니다 — 실제로 안 일어날 수 있다."**
→ **미해결.** hull 은 구동력만 말한다. 실제 형성 속도·핵생성 장벽은 안 봤다.
modelc 도 OCV 에서 자가분해하는데 실제로 쓰이는 것이 그 증거다. 다만 우리 주장은
**modelc 대비 상대적 악화**라 이 반론의 영향을 덜 받는다.

## Gap

- **속도**를 안 봤다 (반론 d). Nd₂S₃ 형성의 핵생성/확산 장벽 미측정.
- 나머지 Nd 4종(NdPO₄·NdOCl·NdCl₃·NdS)은 아직 **MP 소환값**이다.
  `tools/figures/plot_nd_sei_gaps.py` 하드코딩. 우리 값 3 + MP 4 를 **출처 표시 없이
  섞지 말 것** — Nd₂S₃ 는 우리 0.77 vs MP 1.79 로 2배 넘게 다르다.
- Nd₂S₃ 의 **이온전도도**는 안 쟀다. 전자를 흘려도 이온을 잘 통과시키면 판정이
  달라질 여지가 있다 (그래도 전자 누설은 그대로 문제다).
- Nd 도핑의 **긍정 축**(있다면)이 이 카드에 없다 — GB/계면 효과, O 량 비례 효과는
  별도로 봐야 한다. 이 카드는 ESW·전자구조 두 축만 판정한다.
