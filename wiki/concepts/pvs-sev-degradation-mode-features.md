---
title: PVS·SEV — 열화 모드 진단용 physics-inspired feature 2종
description: "ICA 할선 기울기(PVS)와 스케일링된 충전종료 전압강하(SEV)의 정의, 물리 귀속, 그리고 모드별 부호 구조"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md, raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# PVS·SEV — 열화 모드 진단용 physics-inspired feature 2종

## 정의

2026-09-02 BML 세미나(김시원)가 제안한, half-cell OCP fitting 에 의존하지 않고
LLI/LAM_PE/LAM_NE 를 추정하기 위한 도메인 지식 기반 feature 두 개.

### PVS — peak-to-valley slope (ICA 유래)

0.05C pseudo-OCV 에서 얻은 ICA(dQ/dV) 곡선의 **두 번째 peak 과 두 번째
valley**(약 3.55–3.9 V)를 잇는 **할선의 기울기**.

```
PVS = [ (dQ/dV)_peak2 − (dQ/dV)_valley2 ] / ( V_peak2 − V_valley2 )
```

- **Peak2 = 양극(PE)** — NCM811 의 H1 → M 상전이
- **Valley2 = 음극(NE)** — graphite stage 2 단일상 영역
- 이 둘을 고른 이유는 mid-SOC 에 있어 **SOH 가 크게 떨어진 뒤에도 형상이
  유지**되기 때문 (구술 03:29).

### SEV — scaled EOC ΔV (current interruption 유래)

0.2C 충전 중 주기적으로 전류를 끊고(30 s 완화) **t = 1 s 시점의 전압 강하 ΔV**
를 SOC 마다 잰다. ΔV 는 SOC 에 대해 **U 자형**을 그린다. 셀별 min–max
스케일링 후 **충전 종료(EOC) 지점의 값**이 SEV.

- 물리 귀속: SOC-sweep EIS 의 DRT 에서 뽑은 **양극 charge-transfer 저항
  R_ct,PE** 와 ΔV 의 SOC 개형이 나란하다 → SEV 는 R_ct,PE 의 stoichiometry
  의존성을 반영한다.
- pristine 0.21 → EOL 1.00 (원문 p.10).

## 모드별 부호 구조 (이 페이지의 핵심)

P2D 시뮬레이션(PVS, 원문 p.8)과 stoichiometric-window 모식도(SEV, 원문 p.11)가
주는 방향:

| 열화 모드 | PVS | SEV |
|---|---|---|
| LLI | ↑ | ↑ |
| LAM_PE | ↑ | ↑ |
| LAM_NE | ↓ (최대) | ↓ |
| Si loss | ↓ (완만) | 미제시 |
| Gr loss | ↓ | 미제시 |

**두 feature 의 부호 패턴이 같다.** 둘 다 `{LLI, LAM_PE}` 를 한 부호로,
`{LAM_NE}` 를 반대 부호로 놓는다.

## 왜 중요한가

부호 패턴이 같다는 것은, 두 feature 를 **함께 써도 LLI 와 LAM_PE 를 가르는 새
방향이 생기지 않는다**는 뜻이다 — 3차원 모드 공간 `(LLI, LAM_PE, LAM_NE)` 에
대해 두 관측이 사실상 같은 1개 대비(양극·재고 그룹 vs 음극)를 재고 있다.
이것은 [[fitting-degeneracy]] 가 full-cell OCV fitting 에서 말하는 것과 **같은
형태의 문제**이며, 관측을 OCV 에서 ICA+CI 로 바꾸었다고 사라지지 않는다.

원문은 이 점을 주장하지도 부정하지도 않는다 — 각 feature 가 "모드에 따라
방향성을 갖는다"까지만 보인다. 두 feature 의 부호표를 나란히 놓은 것은 이
페이지다. 검증은 열린 질문 [[pvs-sev-lli-lampe-separability]] 로 추적한다.

## 이 위키에서의 적용

- [[degradation-degeneracy]] 는 합성 truth 로 **분해의 식별 가능성 자체**를
  판정한다. 이 세미나의 feature 는 그 판정 대상에 넣을 수 있는 **새 관측
  후보**다 — 우리 파이프라인의 목적함수에 PVS·SEV 항을 얹고 degeneracy 지표가
  개선되는지가 곧바로 실험 가능한 질문이 된다.
- 반대 방향의 기여도 있다. 원문 p.13 의 전극 수준 정답 축이 **"Fitted"**
  (= half-cell OCV fitting 출력)이므로, 우리 프로젝트가 내는 **라벨 불확실성
  경계**가 그 MAE 수치의 해석에 필요한 입력이 된다.
- 원문 p.15 의 discussion point 3종이 모두 우리 축과 겹친다: fitting quality
  개선 · LAM_NE 를 Si/Gr 로 분리 · dQ/dV 계산 방식에 따른 PVS 변화. 세 번째는
  우리 쪽 평활화 민감도 작업과 같은 축이다.

## 불확실성

- 부호표의 PVS 행은 도표에서 눈으로 읽은 방향이고, 수치 자체는 원문 도표가
  정본이다. SEV 행은 모식도(정성)만 있고 정량 스윕이 원문에 없다.
- p.8 은 모드를 **하나씩** 넣은 단독 스윕만 보여 준다. 두 모드가 동시에
  진행할 때 PVS 가 가법적인지는 원문 미제시 — 부호 구조 논증의 가장 큰 공백.
