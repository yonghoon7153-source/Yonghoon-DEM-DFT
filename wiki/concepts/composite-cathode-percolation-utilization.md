---
title: 복합양극 퍼콜레이션 이용률 (utilization level)
description: "Bielefeld 2019 utilization level θ = V_c/V_ν as the geometric surrogate for ASSB composite-cathode contact loss, its units, closed forms, and its own irreducible width"
created: 2026-09-16
updated: 2026-09-16
type: concept
tags: [assb, battery, degradation, dem-mpm, research]
sources: [raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# 복합양극 퍼콜레이션 이용률 (utilization level)

> `assb` 축의 첫 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 수치의 정본은 원문 PDF 이고, 이 페이지의 값은 **사본**이다 — 인용 근거로 쓰지 않는다.

## 정의

Bielefeld, Weber, Janek (2019) 의 **식 (6)**:

```
θ = V_c / V_ν
```

`ν` = 고상 성분(AM 또는 SE), `c` = 그 성분이 속하는 **퍼콜레이팅 전도 클러스터**.
즉 **"퍼콜레이팅 클러스터에 속한 성분 부피 / 그 성분의 전체 부피"**, 무차원 %.

- **AM** 은 **전자** 클러스터에만 배정된다 (SE 는 단일 이온 전도체라 전자 전도도 무시).
  클러스터는 **집전체 쪽 경계면**에서 자란다.
- **SE** 는 **이온** 클러스터에만 배정된다 (AM 의 이온 전도도는 5–6 자릿수 낮다고 가정).
  클러스터는 **분리막 쪽 경계면**에서 자란다.
- 판정은 **Hoshen−Kopelman** 클러스터 알고리즘. **접촉 저항·수축 저항은 명시적으로 배제**
  → `θ_AM` 은 쓸 수 있는 AM 의 **상한**이다.

⚠ 원문 §RESULTS 의 **산문**은 `θ` 를 "클러스터에 속한 부피와 **속하지 않은** 부피의 비"
라고 쓰지만, 그림에서 `θ` 가 100 % 로 포화하므로 **식 (6) 이 맞고 산문이 틀렸다**
(digest §10 불일치 2).

### 짝이 되는 양

| 기호 | 정의 | 단위 |
|---|---|---|
| `A_spec` | 한 클러스터의 표면적 / 구조 부피 | m²/m³ |
| **`A_spec,a`** | **이온 클러스터 ↔ 전자 클러스터 계면적** / 구조 부피 — "리튬 삽입에 실제로 쓸 수 있는 면적" | m²/m³ |
| `A_spec,geo` | 기하 상한 `= 6 g^V_AM / d` (식 7) | m²/m³ |
| `p_c` | 퍼콜레이션 임계 — **10 배열 평균 `θ_AM` 이 40 % 가 되는 `g^V_AM`** (40 % 는 임의 문턱) | vol% |

`[해석]` `θ_AM` 이 **열역학적 용량**(얼마나 많은 AM 이 쓰이는가)에 대응한다면
`A_spec,a` 는 **동역학**(얼마나 빨리)에 대응한다. 원문은 **둘 다 전압으로 번역하지 않는다.**

## 왜 중요한가 — 접촉 손실이 `LAM_PE` 와 섞이는 **곱셈 축퇴**

[[assb-contact-loss-vs-lampe]] 가 묻는 접촉 손실("활물질이 SE 와 닿지 않게 됨 —
물질은 그대로인데 용량이 준 것처럼 보인다")은 이 언어로 쓰면 **`θ_AM` 의 하락**이다.
우리 아핀 창 좌표계(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1)에 얹으면:

```
Q_apparent(PE) = θ_AM(조성, 공극률, 입자크기) · Q_material(PE)
```

`[해석]` → **접촉 손실과 진짜 `LAM_PE` 는 용량 축 스케일 `a_PE` 안에서 곱으로 섞인다.**
OCV 곡선은 **곱만** 본다. 이는 [[np-lip-ocv-reparametrization]] 의 "SOC 정규화 OCV 는
비(比)에만 의존" 과 같은 종류의 닫힌 형태 null 방향이되, `LAM_PE` 축 **안에서** 일어난다.
따라서 물어야 할 것은 "OCV 가 가르는가"(답은 이미 정해져 있다)가 아니라
**"독립 관측 하나를 넣으면 [[near-optimal-set-width-measurement]] 의 폭이 얼마나 줄어드는가"** 다.

## 인터페이스 사양 — 단위가 어긋나기 쉬운 자리

DEM 산출을 합성 forward model 에 주입할 때 쓸 좌표. **부피분율에 두 종류가 있다.**

| 기호 | 기준 | 어디에 나오나 |
|---|---|---|
| `g^V_AM` | **전체 구조 부피** (공극 **포함**) | 원문 그림들의 **아래 x 축** ("Total fraction of AM") |
| `g^S_AM` | **고상만** (`g^S_AM + g^S_SE = 1`) | 원문 그림들의 **위 x 축** = **"72/28 vol%" 같은 조성 표기** |

변환: **`g^S_AM = g^V_AM / (1 − φ)`** (식 9) · `g^V_AM = (1 − φ)(1 − g^S_SE)` (식 4).

⚠ 원문 **식 (5)** 의 좌변 `g^V_SE` 는 위 규약을 배반한다 — 출력이 전체 부피 기준이 아니라
**SE 하부구조(= AM 이 아닌 부피) 기준**이다. 미시구조 **생성 절차용**이지 보고용이 아니다.

### 닫힌 형태 둘 (적용 조건을 떼지 말 것)

```
p_c = [ 7.83 · ln(d/µm) + 36.67 ] vol%                              (식 8)
A_spec(p − p_c) = 1.73e5 · ((p − p_c)/vol%)^0.41  m²/m³             (Fig. 4 범례)
```

적용 조건: **AM 구·균일 입도·겹침 없음 · SE 볼록다면체 3 µm 고정 · 무탄소·무바인더 ·
전자 클러스터**. 둘째 식의 프리팩터는 **d = 10 µm 전용**이고 원문은 다른 `d` 로의
스케일링을 주지 않는다.

## ★ 이 양 자체가 폭을 갖는다

원문 §전자 전도 (인쇄): 조성·공극률·입자 크기를 **전부 고정해도** 무작위 충전 배열만
바꾸면 임계 근방에서 `θ_AM` 이 **≈30 % 와 ≈70 % 로 이봉(bimodal)** 으로 갈린다 — 폭 ≈40 %p.
Fig. 4 (인쇄): 임계 바로 위(`p − p_c = 1 vol%`)에서 `A_spec` 표준편차가 평균의 **≈±32 %**
(8 배열), `p − p_c = 5 vol%` 에서는 **≈±2 %** 로 줄어든다.

`[해석]` 두 가지가 따라 나온다.

1. **DEM 이 "독립 라벨" 을 준다는 계획은, 그 라벨 자체에 폭을 붙여야 성립한다.**
   액체셀 계열에서 우리가 "라벨에 오차 막대가 없다" 를 비판해 온 것과 같은 규율이
   우리 자신에게 적용된다.
2. **임계에서 멀리 떨어진 곳에서 일해야 한다** (`p − p_c ≳ 5 vol%`). 처방이 같은 논문
   안에 있다.

그리고 원문의 **유한 크기 효과**(얇은 전극에서 `A_spec,a` 가 부풀려진다 — 45 vol% 에서
20 µm 가 140 µm 의 약 6 배)는 우리에게 **DEM 도메인 크기 수렴 시험이 선행 조건**임을 뜻한다.

## 이 위키에서의 적용

- [[assb-contact-loss-vs-lampe]] 의 미결 항목 1("접촉 손실을 모델에 어떤 형태로 넣나")에
  **형태**를 준다: 용량 축 스케일에 곱해지는 기하 인자. **동역학(`θ_AM` 의 사이클 의존)은
  여전히 비어 있다** — 원문은 pristine 정적 기하만 모델링한다.
- [[fitting-degeneracy]] 가 화학과 무관하게 재현될 자리 하나를 확인해 준다:
  `A_spec,a` 의 봉우리가 **평탄**하고(±3–4 vol% 구별 불가) 두께 20–140 µm 곡선이
  최적 근방에서 **겹친다** → 그 관측으로 미시구조를 역추정하면 flat valley 를 만난다.
  원문은 forward 전용이라 그 문제를 만나지 않았을 뿐이다.
- [[mode-identifiability-unmeasured-lineage]] 와 같은 형식의 관측이 `assb` 축에서도 성립한다:
  원문 저자들이 **8 편을 지목해** "공극률이 보고되지 않는다" 고 적었다. `assb` 축의
  "모두가 빠뜨린 필수 변수" 원장 — 현재 **공극률**(원문이 지목) + **압력**(우리가 지목,
  원문에 0 회).

## 이 페이지가 주장하지 않는 것

- `θ_AM` 이 접촉 손실의 **올바른** 모형이라고 주장하지 않는다. 원문의 `θ` 는 접촉 저항을
  배제한 **정적 상한**이고 시간축이 없다.
- `Q_apparent = θ_AM · Q_material` 은 **우리 해석**이다 — 원문은 용량도 전압도 쓰지 않는다
  (전압축 자체가 논문에 없다).
- 원문이 유효 전도도(S/cm)를 계산했다고 주장하지 않는다. **한 번도 계산하지 않았다** —
  그럼에도 초록이 그 결과를 말한다 (digest §10 불일치 1).

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 개념이 그 미결 항목 1 에 답한다.
- [[fitting-degeneracy]] — 액체셀 축퇴. 여기서 재현될 자리를 이 페이지가 지목한다.
- [[near-optimal-set-width-measurement]] — 화학 무관한 폭 측정기. 이 forward map 위에도 걸린다.
- [[np-lip-ocv-reparametrization]] — 닫힌 형태 null 방향의 선례.
- [[mode-identifiability-unmeasured-lineage]] — "모두가 안 잰 것" 원장의 형식.
