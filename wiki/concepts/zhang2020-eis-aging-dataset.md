---
title: 우리가 쓰는 EIS 노화 데이터셋의 정체 (Zhang 2020, Zenodo 3633835)
description: "LiCoO2/graphite 45 mAh 12셀 · 3온도 · 사이클 안 9시점 EIS. Su 2024 SI 로 입수했으나 원 출처는 Zhang et al. Nat. Commun. 2020 이며, state I~IX 는 열화 단계가 아니라 한 충방전 사이클 안의 측정 시점이다"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/su2024_drt-soh-health-features.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
---

# 우리가 쓰는 EIS 노화 데이터셋의 정체 (Zhang 2020, Zenodo 3633835)

## 정의

satellite [[mode-observability]] 의 Phase 2(SEV 실측 대조)가 쓰는 EIS 데이터의
**원 출처와 좌표계**. 우리는 이것을 Su 2024 의 SI zip 으로 입수했지만
(`mode-observability/data/su2024/EIS data/`, 176파일 90 MB), **Su 는 이 데이터를
재는 사람이 아니라 재사용한 사람**이다.

**원 출처** (Su 2024 §2.1 + Data availability + 참조 [32] 로 확정 —
근거는 raw digest `raw/papers/su2024_drt-soh-health-features.md` §2.1):

> Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee,
> *Identifying degradation patterns of lithium ion batteries from impedance
> spectroscopy using machine learning*, **Nature Communications 11 (2020)**,
> DOI **10.1038/s41467-020-15235-7**.
> 데이터: **Zenodo DOI 10.5281/zenodo.3633835**.

Su 2024 의 Data availability 전문: "We used an **open dataset** at
doi:https://doi.org/10.5281/zenodo.3633835, reference number [32]."

## 좌표계 (Su 2024 §2.1 이 인쇄한 것)

| 축 | 값 | 비고 |
|---|---|---|
| 화학 | **LiCoO₂ / graphite** | 형태(코인/파우치/원통)는 **Su 원문에 없다** |
| 공칭 용량 | **45 mAh** (→ 1C = 45 mA) | 우리 capacity 파일의 45.00 mA 와 일치 |
| 셀 | **12개**: 25 °C **8개**(25C01–08) · 35 °C **2개**(35C01–02) · 45 °C **2개**(45C01–02) | 온도별 8개가 **아니다** |
| `state I~IX` | **한 충방전 사이클 안의 아홉 측정 시점** | 열화 단계도 SOH 등급도 아니다 |
| `state V` | **100 % SOC, 15분 휴지 후** | 나머지 8개 state 의 SOC/시점은 Su 원문에 **없다** |
| 열화 축 | 파일 안의 **`cycle number` 열** | state 축과 직교한다 |
| EIS | 정현파 **전류 5 mA** (≈ C/9) · **60 주파수** · **0.02 Hz – 20 kHz** | 우리 실측(4,920행 = 60 × 82 스펙트럼)과 일치 |
| 포맷 | BioLogic EC-Lab (`time/s · cycle number · freq/Hz · Re(Z) · -Im(Z) · |Z| · Phase(Z)`) | Su 는 파일 포맷을 다루지 않는다 |

## 왜 중요한가

**1. 인용의 정본이 바뀐다.** 이 데이터로 낸 어떤 수치도 1차 출처는
**Zhang 2020 / Zenodo 3633835** 이고, Su 2024 는 "이 데이터로 무엇을 했는가" 의
**선행연구**로 인용한다. `mode-observability/manifests/README.md` 에 걸려 있던
"출처 확정 전에는 'Su 2024 SI' 로만 적는다" 는 유보는 이것으로 해제됐다.

**2. `state` 축을 오해하면 Phase 2 설계가 통째로 틀린다.** `state I~IX` 를
열화 단계로 읽으면 한 파일 안의 82개 스펙트럼이 무엇인지 설명되지 않는다.
정답은 **state = SOC/시점, cycle = 열화**다. 따라서 두 종류의 스윕이 가능하다:

- (a) **state 고정 → cycle 스윕** = 노화 추적. Su 2024 가 한 것 (state V 만).
- (b) **cycle 고정 → state I~IX 스윕** = **SOC 의존성 추적**. **아무도 안 했다.**

`[해석]` SEV 는 R_ct 의 **stoichiometry(= SOC) 의존성**을 읽는 feature 다
([[pvs-sev-degradation-mode-features]]). 그렇다면 (b) 야말로 SEV 의 실측
대응물에 가깝고, 이 데이터셋에서 **가장 덜 쓰인 자원**이다.

**3. Su 가 쓴 것은 데이터셋의 일부뿐이다.** 12셀 중 **5셀**(25C01/02/03/05/06),
3온도 중 **25 °C 하나**, 9 state 중 **state V 하나**. 25C04·25C07·25C08 과
35 °C·45 °C 전부, 그리고 state 축 전체가 미사용이다.

## 미확인 항목 (Zhang 2020 원문에서 닫아야 할 것)

우리 실측과 Su 의 서술이 어긋나는 지점 — 전부 **Su 원문으로는 닫히지 않는다**:

1. **셀 형태.** Su 는 형태를 한 번도 적지 않는다. 45 mAh 규모와 명명으로 보아
   코인셀(LIR2032 급)로 추정되나 **확인 전이다**.
2. **셀 목록.** Su 는 12셀(25 °C 8 + 35 °C 2 + 45 °C 2)만 열거한다. 우리
   manifests 의 파일명 패턴이 온도별 01–08 을 시사하면 **둘 중 하나가 틀렸다**.
3. **파일 수 176.** 12셀 × 9 state = 108 EIS + 용량 12 = **120** 과 맞지 않는다.
   `__MACOSX` 그림자 파일·추가 파일 여부를 확인해야 한다.
4. **`EIS_state_VI_25C42.txt`** (셀번호 42). Su 의 열거로 설명되지 않는다.
5. **사이클링 프로토콜(충방전 전류·전압창).** Su 는 적지 않는다 — EIS 조건만
   옮겨 적었다.
6. **헤더 유무가 섞인 이유.** Su 는 파일 포맷을 다루지 않는다.

## 이 위키에서의 적용

- [[mode-observability]] Phase 2 의 데이터 층 정본. 매니페스트 문서는
  `mode-observability/manifests/README.md` (living reference, 내용 복사 금지).
- [[pvs-sev-lli-lampe-separability]] 의 SEV 축을 **실측으로** 건드리는 유일한
  통로. 다만 이 데이터셋에는 **LLI/LAM 라벨이 없다** — Su 도, (확인 필요하나)
  Zhang 2020 도 열화 모드를 재지 않는다. 즉 이 데이터로는 "SEV 가 모드를
  가르는가" 를 직접 물을 수 없고, **"SEV 축 자체가 셀 간에 재현되는가"** 만
  물을 수 있다. 그 구분을 흐리지 않는다.
- Su 2024 의 결과를 **재현 baseline** 으로 쓸 수 있다 (같은 5셀·같은 state).
  단 DRT 설정이 "DRTtools, λ=1E-3, 나머지 default" 로만 인쇄돼 완전 재현은
  어렵다 — raw digest §2.3 참조.

## 관련
- [[mode-observability]] — 이 데이터를 쓰는 satellite
- [[pvs-sev-lli-lampe-separability]] — 이 데이터가 답할 수 있는 질문과 없는 질문
- [[pvs-sev-degradation-mode-features]] — SEV 의 정의와 SOC 의존성 축
- [[interpretable-ml-battery-prognosis-taxonomy]] — Su 2024 가 이 데이터로 한
  작업이 앉는 분류 자리 (§4.4 EIS 유래 physics-inspired feature)
