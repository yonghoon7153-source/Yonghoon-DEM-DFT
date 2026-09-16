---
title: ASSB 겉보기 용량의 3항 분해 — 재료 · 기하 · 동역학
description: "Q_apparent = θ_AM · η(i) · Q_material — ASSB 복합양극에서 겉보기 LAM_PE 로 보이는 것의 세 기원과, 율(rate)이 그중 하나만 지우는 성질 (Clausnitzer 2023 + Bielefeld 2019)"
created: 2026-09-16
updated: 2026-09-16
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# ASSB 겉보기 용량의 3항 분해 — 재료 · 기하 · 동역학

> `assb` 축의 두 번째 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]],
> 첫 번째는 [[composite-cathode-percolation-utilization]].
> 수치의 정본은 원문 PDF 이고, 이 페이지의 값은 **사본**이다 — 인용 근거로 쓰지 않는다.

## 정의

[[composite-cathode-percolation-utilization]] 이 세운 곱셈 축퇴
`Q_apparent = θ_AM · Q_material` 은 **필요조건일 뿐 충분조건이 아니다.**
Clausnitzer et al. 2023 (`raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md`)
이 같은 논문 안에서 반례를 준다 (§9.4·§15-2):

> `SVF_LCO = 69.4 %`, 소결 밀도 70 %, 입계 저항 무시 →
> `[도표]` **CAM 연결성 ≈100 %** (Fig. 6b) 인데 **정규화 용량 ≈0.10** (Fig. 8a).

**모든 활물질이 집전체에 연결돼 있는데도 90 % 가 안 쓰인다.** 따라서 최소 세 항이다:

```
Q_apparent  =  θ_AM(기하)  ·  η(i ; θ_SE, τ_SE, R_GB, D_CAM, σ_CAM)  ·  Q_material
                  ↑ 율 무관              ↑ 율 의존, i→0 에서 →1            ↑ 진짜 LAM_PE
```

`[해석]` **이 3항 분해는 우리 것이고 두 논문 어느 쪽의 식도 아니다.**

| 항 | 뜻 | 단위 | 누가 주나 |
|---|---|---|---|
| `Q_material` | 실제로 남아 있는 활물질의 이론 용량 | mAh | (아무도 안 잰다 — 이것이 우리가 찾는 `LAM_PE`) |
| **`θ_AM`** | 퍼콜레이팅 전도 클러스터에 속한 AM 부피 분율 | 무차원 | Bielefeld `θ = V_c/V_ν` (식 6) ≡ Clausnitzer `Connectivity = 1 − n_iso/n_tot` (식 4). **같은 양, 변환 불필요** |
| **`η(i)`** | 주어진 전류에서 도달 가능한 이용률 | 무차원 | Clausnitzer 의 `C_norm`(식 7/8) 이 이것(또는 `θ_AM·η`)을 잰다 |

⚠ **미확정 좌표 하나**: Clausnitzer 는 `[인쇄]` "isolated clusters were **removed** from
the input structure" 라고 적지만 식 (7) 의 `V_CAM` 이 제거 **전**인지 **후**인지 밝히지
않는다 → **`C_norm` 이 `θ_AM·η` 인지 `η` 만인지 확정되지 않았다**
(digest G1). 이 페이지의 분해를 수치로 쓰기 전에 반드시 풀어야 한다.

## ★ 왜 중요한가 — **율(rate)이 세 항 중 하나만 지운다**

Clausnitzer 가 인쇄한 두 문장을 붙이면 분리 시험이 나온다:

- `[인쇄, p5]` "At **lower current densities**, local currents and overpotentials are
  generally lower, resulting in **reduced sensitivity to microstructural variations**."
- `[인쇄, p8]` `R_GB,3` 에서 집전체 쪽 CAM 의 큰 부분이 방전 끝에도 **초기 Li 농도
  (`x ≈ 0.52`) 그대로** 남는다 (Fig. 5 히스토그램).

→ 세 성분의 거동이 갈린다:

| 성분 | `i → 0` 극한 | 전류 차단 후 이완 | OCV 곡선에서 |
|---|---|---|---|
| 진짜 `LAM_PE` | **그대로** | 회복 없음 | 용량 축이 줄어 있다 |
| 기하 접촉 손실 `1 − θ_AM` | **그대로** (경로가 끊겨 있다) | **회복 없음** | `LAM_PE` 와 **구별 불가** |
| **동역학 손실 `1 − η`** | **0 으로 사라진다** | **회복 있다** | 저율에서 사라진다 |

`[해석]` **처방**: ASSB 자료에서 `a_PE` 를 적합할 때 **최소 두 개 율**에서 같은 파라미터를
적합하고 **율 간 `a_PE` 차이**를 보고한다. 그 차이가 **동역학 성분의 하한**이다.
그러고도 남는 것이 `θ_AM · Q_material` 이고, **그 곱은 여전히 안 갈라진다** —
[[composite-cathode-percolation-utilization]] 의 결론은 무효화되지 않고 **범위가 좁아진다.**

이것은 액체셀 축의 [[thermo-kinetic-loss-partition]] (ΔE / η 분해)와 **형식이 같고 대상이
다르다**: 거기서 `η` 는 **분극 전압**이었고 여기서 `η` 는 **겉보기 용량 인자**다.

## 동역학 성분의 크기 — 이 계보 최초의 전압축 숫자

Clausnitzer Fig. S5 `[도표]` (`SVF_LCO = 50 %`, 소결밀도 93.1 %, `d_CAM` 2.00 / `d_SE`
1.41 µm, **1 mA/cm² ≈ 0.74 C**, 3.4 V 컷오프). **재료·기하가 전부 동일하고 입계 저항만 다르다**:

| 경우 | `R_GB` (Ω cm²) | 시작 전압 | 3.4 V 도달 용량 | 겉보기 `LAM_PE` |
|---|---:|---:|---:|---:|
| `w/o GBs` | 0 | ≈4.155 V | **≈1.37 mAh/cm²** | 0 % (기준) |
| `R_GB,1` | 3.6e-2 | ≈4.135 V | ≈1.36 | ≈1 % |
| `R_GB,2` | 3.6e-1 | ≈4.085 V | ≈1.31 | ≈4 % |
| `R_GB,3` | 3.6 | **≈3.98 V** | **≈0.385** | **≈72 %** |

`[해석]` ★ **재료 손실 0 인데 겉보기 용량 손실 72 %.** 그리고 곡선이 **수평 스케일링이
아니다** — 시작 전압이 175 mV 낮고 기울기가 다르다. 따라서
`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1 의 아핀 창 매개화(`a_PE, b_PE`)로는
이 곡선을 맞출 수 없다. **나쁜 소식이 아니라 관측 가능성이다**: 아핀 잔차의 구조적
패턴(특히 곡선 끝의 급락)이 동역학 성분의 지표가 될 수 있다.
[[halfcell-ocp-shape-invariance]] 의 "모양 불변" 가정이 ASSB 에서 **어디서 먼저
깨지는가**의 첫 후보.

## `θ` 는 스칼라가 아니다 — 공간 분포가 있다

Bielefeld 의 `θ_AM` 은 전극 전체에 대한 **스칼라 하나**였다. Clausnitzer 가 그것을 깬다:

- `[인쇄, p9]` "The share of unconnected clusters **increases with increasing distance from
  the separator**." (Fig. 6c 의 3D 이미지가 이를 보여 준다 — 격리 SE 가 집전체 쪽에 몰린다.)
- `[도표]` Fig. 8b, `SVF_LCO = 69.4 %`, 소결밀도 70 %: CAM 이용률이 분리막에서 ≈0.95 →
  5 µm 만에 0.3 아래 → 20 µm 부터 ≈0. **전극의 90 % 가 이용률 ≈0.**

`[해석]` → DEM 산출을 forward model 에 주입할 때 `θ` 를 스칼라로 넣으면 **집전체 쪽
손실을 과소평가**한다. 최소한 "평균 + 기울기" 두 수가 필요하다.

## 이 페이지가 주장하지 않는 것

- **3항 분해가 논문의 식이라고 주장하지 않는다.** 우리 해석이고, 위 G1 때문에 `C_norm` 이
  `θ_AM` 을 포함하는지조차 확정되지 않았다.
- **율 스윕이 수행됐다고 주장하지 않는다.** Clausnitzer 는 **단일 율(1 mA/cm²)** 로만
  돌았다. 율 의존은 논문의 두 문장에서 **추론한 것**이다.
- **`η` 가 열화 축이라고 주장하지 않는다.** Clausnitzer 의 `R_GB` 는 **제조 변수**(소결
  공정)이지 사이클 변수가 아니다. 사이클 중 `R_GB` 나 `θ` 가 어떻게 변하는지는
  **`assb` 2 편 모두 다루지 않았다** — 논문 스스로 `[인쇄]` "beyond the scope".
- 이 수치들은 **LCO/LLZO 소결 복합양극 · Li 금속 음극(이상 접촉) · 두께 50 µm ·
  방전 1 회 · 구조 실현 1 개**라는 한 모집단의 것이다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지가 그 미결 항목 1 의 **세 번째 항**을 추가한다.
- [[composite-cathode-percolation-utilization]] — `θ_AM` 의 정의와 곱셈 축퇴. 이 페이지가 그 위에 `η` 를 얹는다.
- [[thermo-kinetic-loss-partition]] — 액체셀 축의 같은 형식(전류를 관측 축으로 쓰는 분해).
- [[fitting-degeneracy]] — 이 3 항 중 앞의 두 항이 OCV 에 대해 만드는 null 방향.
- [[near-optimal-set-width-measurement]] — 율을 하나 더 넣었을 때 폭이 얼마나 줄어드는지 잴 기계.
- [[halfcell-ocp-shape-invariance]] — 아핀 창 모형이 깨지는 자리.
