---
title: ASSB 겉보기 용량의 3항 분해 — 재료 · 기하 · 동역학
description: "Q_apparent = θ_AM · η(i) · Q_material — ASSB 복합양극에서 겉보기 LAM_PE 로 보이는 것의 세 기원과, 율(rate)이 그중 하나만 지우는 성질 (Clausnitzer 2023 + Bielefeld 2019)"
created: 2026-09-16
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md]
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
>
> **2026-09-16 갱신 (`assb` 3호 Liu 2024)**: ① **율 극한이 독립 모델에서 확인됐다**
> (§"율 극한이 …"). ② 그러나 **`Q_material` 도 율 의존**이라 분리 시험의 처방이
> 좁아졌다 (§"그러나 처방이 …"). ③ `θ(N)` 은 **3/3 편이 안 줬다.**
>
> **2026-09-16 갱신 (`assb` 4호 Shi 2020 — 첫 실험 논문)**: ★★ **두 번째 분리 연산자가
> 들어왔다** — 율이 `η` 를 지우듯 **압력 재인가가 `θ_AM` 을 (부분적으로) 되돌린다**
> ([[assb-pressure-reapplication-separation-test]]). 그리고 ★ **율 극한 논증이 실험에서
> 간접 검증됐다** (§"저율 셀이 …"). ⚠ 동시에 **`θ` 를 곱셈 인자로 쓰는 것이 6 배
> 어긋난다**는 실측 반례도 같이 왔다.

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

### ✅ 율 극한이 독립 모델에서 확인됐다 (2026-09-16, `assb` 3호 Liu 2024)

`assb` 3호(`raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md`)
는 이 계보 최초로 **율 스윕 전압곡선**을 준다 (SI Fig. S4: 0.25C·0.5C·1C·2C·5C ×
NMC811 이차입자 2/4/8/12 µm = 곡선 20 장, 3 V 컷오프). `[도표]` 정규화 용량 종점:

| | 2 µm | 4 µm | 8 µm | 12 µm |
|---|---|---|---|---|
| **0.25C** | ≈0.99 | ≈0.98 | ≈0.98 | **≈0.95** |
| 1C | ≈0.96 | ≈0.945 | ≈0.90 | ≈0.69 |
| 5C | ≈0.95 | ≈0.86 | ≈0.60 | **≈0.35** |

★ `[해석]` **`i → 0` 에서 모든 크기가 ≈1 로 수렴한다.** 그 모델에는 재료 손실도(첫
방전에는) 기하 손실도 없다 — 입자 **1 개**가 균질 전해질에 박혀 있고 탄소 바인더로
집전체에 연결됐다고 **가정**되므로 **`θ_AM ≡ 1`** 이다. 따라서 **관측된 용량 손실
전부가 `η(i)` 한 항**이고, 그것이 율과 함께 사라지는 것을 **직접 볼 수 있다.**
2호에서 두 문장으로 **추론**했던 것이 다른 모델·다른 길이척도에서 재현됐다.

### ⚠ 그러나 처방이 좁아졌다 — `Q_material` 도 율 의존이다

3호는 동시에 위 처방의 전제를 깬다. `[도표]` Fig. 5e (활물질 손실 = 소성전단 > 12 %
영역의 부피분율):

| 입자 지름 | 0.25C | 1C | 5C |
|---|---|---|---|
| 12 µm | 0.093 | 0.125 | **0.185** |
| 8 µm | 0.088 | 0.115 | 0.163 |
| 4 µm | 0.078 | 0.080 | 0.132 |
| 2 µm | 0.078 | 0.075 | 0.088 |

→ **고율 방전 자체가 진짜 재료 손실을 더 만든다** (12 µm 에서 2 배). 즉
`Q_material = Q_material(i, N)` 이다. **같은 셀에 두 율을 걸어 차이를 읽으면 그 차이는
동역학 성분의 하한이 아니라 (동역학 + 율유발 재료손실)의 합**이다.

`[해석]` **살아남는 설계 둘**:
(a) **저율 쌍만** 쓴다 (예: 0.1C vs 0.25C — 위 표에서 그 구간의 재료손실 증가분이 가장 작다),
(b) **율을 올렸다가 기준 율로 돌아와** 이력(hysteresis)을 재고 비가역분을 뺀다. **(b) 가 안전하다.**
⚠ 단 3호의 활물질 손실 축은 **적합된 문턱(12 %)** 위에 서 있고 오차 막대가 없다 —
위 수치는 **방향의 근거이지 크기의 근거가 아니다.**

이것은 액체셀 축의 [[thermo-kinetic-loss-partition]] (ΔE / η 분해)와 **형식이 같고 대상이
다르다**: 거기서 `η` 는 **분극 전압**이었고 여기서 `η` 는 **겉보기 용량 인자**다.

### ★★ 저율 셀이 실험에서 이 논증을 간접 검증했다 (2026-09-16, `assb` 4호 Shi 2020)

`raw/papers/shi2020_mechanical-degradation-assb-cathode.md` (이 계보 **첫 실험 논문**).
`[재현]` 그 셀의 율은 **≈C/15** (0.05 mA cm⁻², NMC ≈3 mg, 8 mm 펠릿) — 2호(≈0.74 C)·
3호(0.25–5 C)보다 **한 자릿수 낮다.** 위 표와 3호 율 스윕을 그대로 적용하면
**`η ≈ 1` 이어야 한다.** 그런데 `[도표]` 50 사이클에서 겉보기 용량이 129 → **≈2
mAh g⁻¹** 다 (**≈98 % 손실**).

★ `[해석]` **저율에서도 살아남았으므로 `η(i)` 로 설명되지 않는다.** 남는 것은
`θ_AM` 과 `Q_material` 인데, **300 MPa 재가압으로 `[재현]` ≈60.5 %p 가 돌아왔다**
(`[인쇄]` 2 → 80 mAh g⁻¹). → **그중 최소 60 %p 가 기하 쪽이다.**
즉 위의 "율이 세 항 중 하나만 지운다" 가 **실험에서 처음으로 간접 확인됐다.**
⚠ 단 4호는 **율 스윕을 하지 않았다** — 직접 증명이 아니라 우리 추론이다.

### ⚠ 그리고 같은 논문이 `θ_AM` 의 **곱셈 형태**를 6 배로 배반한다

`[인쇄]` 같은 시점의 접촉 손실 **면적** 분율은 **10.4 %** 다. 곱셈에 그대로 넣으면
용량 손실 **10 %** 여야 하는데 압력 가역분이 **60 %p**. **≈6 배.**
→ **`θ_AM` 자리에 면적 분율을 선형으로 넣을 수 없다** (문턱/분포 의존).
자세히는 [[composite-cathode-percolation-utilization]] §"4호는 실측을 줬는데 …".

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

## ★★ 2026-09-16 (`assb` 6호 Lee 2020) — 분해에 **음극 두 항**이 붙고, `η` 가 **온도 축**으로 열린다

`raw/papers/lee2020_ag-c-anode-free-assb.md` (SAIT/Samsung, *Nature Energy* 2020).
**무음극(Ag–C) / Li₆PS₅Cl / LZO-NMC(Ni 90) 6.8 mAh cm⁻² / 60 °C / 0.6 Ah 파우치.**

```
현재:  Q_apparent = θ_AM · η(i, P) · Q_material            ← 양극 중심, 음극 무해 전제

6호가 요구하는 확장:

Q_apparent = θ_AM(N) · η(i, P, T) · Q_material
           −  L_anode(N)                     ← 음극이 삼키는 Li (비가역)   ★ 새 항
           +  Q_anode,rev(Li₉Ag₄, LiC_x)     ← 음극이 되돌려 주는 Li       ★ 새 항
```

| 칸 | 6호가 주는 것 | 값 |
|---|---|---|
| `η(i)` | 율 스윕 5 점 (0.2–2.0 C) | `[인쇄]` Q₁.₀C/Q₀.₂C **93 %**, 2.0 C 이용률 >80 %. `[재현]` **0.5 C 에서 146/215 = 0.68** |
| **`η(T)`** ★ 새 축 | **온도 스윕 6 점** (60 → −10 °C, 충전은 60 °C 고정) | `[인쇄]` 45 °C **99.5 %** · 25 °C **90.7 %** · −10 °C **>40 %**. 계면 저항 `[인쇄]` 60 °C **5** ↔ 25 °C **50 Ω cm²** |
| `η(P)` | 운전 압력 3 점 + 무압 | `[도표]` 2/3/4 MPa → 94.0/95.1/95.5 %; **무압 0.1 C 는 2 MPa 와 구별 안 됨** |
| `θ_AM` | **없다** — 공정(WIP 490 MPa)으로 처리하고 재지 않는다 | Table S2 의 **−5.51 % 치밀화**가 유일한 대리량 |
| `Q_material` | **없다** — 양극 사후 분석 0 | — |
| **`L_anode`** | 첫 사이클 비가역 + CE 결손 | `[재현]` **19 mAh g⁻¹ (8.2 %)**, 그중 Ag–C 귀속 **≤3 mAh g⁻¹** (유/무 차분) |
| **`Q_anode,rev`** | Li₉Ag₄ (XRD 로 동정, 가역) + LiC_x | `[재현]` Ag 몫 **≤0.89 %** of 셀 (Ag 8–16 mg Ah⁻¹ × 559 mAh g⁻¹) |

★★★ **가장 중요한 한 줄**: `[재현]` **0.5 C 에서 `η ≈ 0.68` 이다.**
**양극 재고의 32 % 가 운전 창 밖에 있고**, 그만큼 Li 손실이 용량 손실로 즉시
나타나지 않는다. → **`η` 가 `LAM_PE` 뿐 아니라 `LLI` 도 가린다.**
`[해석]` **겉보기 용량유지율은 `LLI` 의 하한이다.**
자세히는 [[anode-free-li-inventory-accounting]].

★ `η(T)` 가 새로 열린 것도 같은 구조다 — `[인쇄]` −10 °C 에서 용량의 절반이
사라지는데 **재료는 그대로**다. 계면 저항이 10 배로 오른 결과다.
→ **3 항 분해의 `η` 는 `(i, P, T)` 의 함수이고, 세 축이 서로 직교하지 않는다**
(5호가 `i ↔ P` 비직교를 이미 보였다).

## ★★ 2026-09-16 (`assb` 7호 Spencer-Jolly 2023) — **음극 쪽 `Q_material` 도 율 의존이고, `η(i)` 가 급격히 비선형이다**

3호(Liu 2024)가 **양극**에서 보인 것("고율 방전 자체가 진짜 재료 손실을 더 만든다")
의 **음극 판**이 왔다. `raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`.

- ★ **율이 상(相) 조성을 바꾼다.** 저율(30 µA cm⁻², 상온)에서는 흑연과 Ag 가 함께
  리튬화되는데, 고율(2·4 mA cm⁻², 60 °C)에서는 `[인쇄]` "**No change is evident in
  the Ag peaks** … the rapid insertion of Li into graphite … is significantly **faster
  than the reaction of lithiated graphite with the Ag**" 이고 4 mA cm⁻² 에서는
  `[인쇄]` "**clear evidence of Ag persisting throughout charging**".
  → **같은 전하를 통과시켜도 율에 따라 Li 가 들어간 그릇이 다르다.**
  `Q_material`(음극)이 율의 함수다. 상세는 [[ag-c-interlayer-lithium-phase-path]].
- ★★ **`η(i)` 의 비선형성이 숫자로**: `[재현]` 2 mA cm⁻² 에서 과전압이 **≈−0.09 V 로
  3 h 내내 평평** ↔ 4 mA cm⁻² 에서 **−0.16 → −1.15 V 로 자라다 ≈0.72 h 에 단락**.
  **전류 2 배에 과전압 ≈12 배.** → 율 스윕 분리 시험에서 **"두 율" 을 어디에 놓느냐가
  결과를 지배한다** — 문턱 근처에서는 `η` 가 사실상 발산한다.
- ⚠ **모집단**: Ag–흑연 무음극 중간층 / 반쪽전지 / 1 사이클 / 셀 수 미상.
  양극 축으로 옮기지 않는다.

## ★ 2026-09-22 (`assb` 13호 Zheng 2026, **그리드 appraisal · Perspective, 1차 측정 0**) — 수요 측이 요구한 분해는 **2 항**이고, `θ_AM` 이 빠져 있다

`raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (*Energy* 345, 140229; 전력연구원 +
전지 제조사 공저). 그리드 BMS 가 갈라야 할 것을 §4 가 이렇게 적는다:

`[인쇄]` "The BMS must instead **distinguish between true active material loss and a reduction in
'useable capacity' caused by rising impedance or increasing overpotentials** that effectively
shrink the operational voltage window at practical power rates. This requires the development of
new, **multi-parameter SOH models** … to provide a nuanced assessment of **degradation root causes**."

이 페이지 어휘로 옮기면 **`Q_material` ↔ `η(i)`** 두 항이다. **`θ_AM` 이 없다.** 그런데
같은 절 첫 문단이 ASSB 의 지배 실패 모드를 `[인쇄]` "the gradual **loss of interfacial
contact**, the propagation of cracks within brittle solid electrolytes, and the chemo-mechanical
evolution of electrode-electrolyte interfaces" 로 꼽는다 — **1 번이 접촉 손실**이다.

`[해석]` 세 가지:
1. **수요 측 요구서가 3 항 중 두 항만 적었다.** 접촉 손실이 "true active material loss" 인지
   "rising impedance" 인지 논문은 말하지 않는다 — 우리 분해에서는 **어느 쪽도 아닌 세 번째
   항**이고, 4호(Shi 2020)의 재가압 회복(≈60 %p)이 그것이 `η` 로 환원되지 않음을 보였다.
2. 12호(Kouhestani 2022)는 `LAM ⊃ 접촉 손실` 로 **정의에 흡수**, 13호는 **정의에서 누락** —
   **두 종설이 다른 방식으로 같은 결과**(분리 물음이 없는 분류)에 이른다. 분류 체계가
   셋(12호·13호·이 페이지)이라는 것 자체가 실측이다.
3. ★ 13호의 운전 조건이 이 분해의 **관측 가능성**을 바꾼다: `[인쇄]` "20–80 % SOC …
   impossible to obtain a full OCV curve" + LFP 평탄 + "voltage hysteresis arising from mechanical
   stresses". `η(i)` 는 율 연산자로, `θ_AM` 은 압력 연산자로 지울 수 있지만 **`Q_material`
   은 OCV 전 구간이 있어야 잰다** — 그리드 창에서는 그 항이 **가장 안 보이는 항**이 된다.
   → [[data-window-identifiability]] 의 ASSB 판이 필요한 자리.

⚠ 13호는 데이터 0 이다. 이 절이 더한 것은 **요구서의 형태**이지 분해의 근거가 아니다.

## ★★★ 2026-09-22 (`assb` 14호 Oh 2025, **실험**) — **void 가 `Q_apparent` 에 안 들어가는 실측**: `θ_AM` 은 void 의 함수가 아니라 퍼콜레이션의 함수다

`raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` → [[assb-maxwell-ocv-derivative-channels]].

`[인쇄]` NCM811‖LPSCl‖Li, 50 사이클 0.5C: XRM 공극률 **4.5 → 9.8 %**(10 MPa) ↔ **4.4 → 5.3 %**
(20 MPa) 인데 용량 유지율 **86.0 % ↔ 84.0 %**. void 가 2 배인 셀이 **더 높다**. 논문은
"similar … internal voids may not directly affect the early-cycle performance [73,74]" 로
지나간다.

`[해석]` 이 페이지의 언어로 — **`θ_AM` 이 두 셀에서 모두 ≈1** 이다. void 부피분율 +5.3 %p
가 `Q_apparent` 를 전혀 안 움직였으므로, **`θ_AM` 은 void 분율의 연속 함수가 아니라
퍼콜레이션 문턱의 함수**([[composite-cathode-percolation-utilization]] 의 `p_c`)이고, 이
창은 문턱 **아래**다. 4호 Shi(면적 10.4 % ↔ 60 %p 회복)는 문턱 **위**다. ⇒ **접촉 손실 →
용량 사상은 문턱형**이고 두 실험이 그 양 끝을 찍는다.

이것이 이 페이지의 3 항에 주는 것:
- **`θ_AM` 을 형태학(void %)에서 직접 읽을 수 없다** — 사상에 문턱이 있다. 1호의 `p_c` 가
  실험에서 처음 **간접** 확인된 자리 (14호 ref [69] Bielefeld 2022 가 그 실험 원전 후보).
- **문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 정확히 보고하고 void 성장을 놓친다** — 닻
  물음(오독)의 반대편, **무감**. 그것을 보는 관측이 `F(∂E/∂P)_T`(−18 %)다.
- ⚠ 모집단: 50 사이클 · 조건당 셀 1 · 2 점 · 0.5C · 10–20 MPa. 그리고 두 셀의 **초기 용량이
  다르다**(`[도표]` 138 ↔ 144 mAh g⁻¹) — 20 MPa 셀이 처음부터 더 컸다.

## ★★★★ 2026-09-22 (`assb` 17호 Yanev 2024, **실험 · 3전극**) — **네 번째 항이 필요하다: 컷오프가 상대극의 함수다**

`raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`.
이 페이지의 세 항은 전부 **양극 안**의 것이었다. 17호가 보이는 것은 **양극 밖**에서
`Q_apparent` 를 깎는 통로이고, **세 항 중 어느 것도 아니다.**

```
Q_apparent = θ_AM · Q_material( E_cut^eff ) · η(i)
             E_cut^eff = E_cell,min + E_CE( i, x_Li, 제조법 )
```

★★★ **실측** (같은 양극·같은 프로토콜·0.1 C, 셀 둘):
`[도표]` 방전 용량 **198 ↔ 185 mAh g⁻¹ (−6.6 %)** · `[재현]` **양극 임피던스는 같다**
(≈31 ↔ ≈32.5 Ω, 5 % 차) · `[도표]` `E_CE` 가 방전 끝에 **0.62 → ≈1.0 V** ⇒
`[재현]` **양극이 3.0 V 가 아니라 ≈3.4 V 에서 멈춘다.**
⇒ **`θ_AM` 도 `Q_material` 도 `η` 도 변하지 않았는데 `Q_apparent` 가 6.6 % 줄었다.**

### ★★★ 이것이 이 페이지의 **분리 시험을 깬다**

이 페이지의 핵심 처방은 **"율을 낮추면 `η(i) → 1` 이 되어 동역학 성분이 지워진다"**
였다. **기준 전위 이동은 지워지지 않는다** — `η` 가 아니라 **축의 원점**이기 때문이다.

`[재현]` 17호에서 `i → 0` 극한(CA 종료 기준 **0.02 C**)에서도 `ΔE_CE` 가 **+0.73 V**
로 남는다. 옴 몫은 **0.2 %**(≈1.8 mV). 그리고 율 의존성은 **있지만 0 으로 안 간다**:
0.1 C 에서 **6.6 %**, CA(초기 ≈5.7 C)에서 **≈35 %**.

`[해석]` ⇒ **저율 쌍 처방(`i → 0` 두 점)은 `η` 를 지우되 `E_cut^eff` 이동을 `θ_AM` 이나
`Q_material` 쪽으로 밀어 넣는다.** 이 항을 빼려면 **상대극 전위를 따로 재야 한다**
(= 세 번째 전극), 또는 **상대극이 정말 평탄함을 독립으로 보여야 한다**.

### ⚠ 모집단

Li-In 음극 셀의 것이다. **Li 금속·무음극에 그대로 옮기지 않는다.**
그리고 17호는 **최대 5 사이클 · 신품 · 압력 한 점 · 조건당 셀 1 개**다 —
**`E_CE(N)` 은 0 편**이라 이 항이 **사이클에 따라 어떻게 커지는지 모른다.**
자세히는 [[assb-li-in-reference-potential-window]].

## 이 페이지가 주장하지 않는 것

- **3항 분해가 논문의 식이라고 주장하지 않는다.** 우리 해석이고, 위 G1 때문에 `C_norm` 이
  `θ_AM` 을 포함하는지조차 확정되지 않았다.
- **율 스윕이 수행됐다고 주장하지 않는다.** Clausnitzer 는 **단일 율(1 mA/cm²)** 로만
  돌았다. 율 의존은 논문의 두 문장에서 **추론한 것**이다.
- **`η` 가 열화 축이라고 주장하지 않는다.** Clausnitzer 의 `R_GB` 는 **제조 변수**(소결
  공정)이지 사이클 변수가 아니다. 사이클 중 `R_GB` 나 `θ` 가 어떻게 변하는지는
  **`assb` 1–3 호가 다루지 않았다** — 2호는 `[인쇄]` "beyond the scope", 3호는 방전
  1 회 + 충전 1 회에 **파괴·디본딩 모형 자체가 없다**.
  → **4호가 실측으로 일부 채웠다**: `[도표]` void 부피분율이 사이클 0/10/50 에
  **2.87 / 3.23 / 9.50 vol%**, `[도표]` EIS 저항이 사이클 1→50 에 전 대역 증가
  (`R_MF` `[인쇄]` 954 → 3283 Ω). ⚠ 단 **3 점 · 각 점 다른 셀 · 반복 0** 이고,
  `θ` 가 아니라 **void 부피/접촉 면적**이다.
- **4호의 회복분(60 %p)이 양극 것이라고 주장하지 않는다.** `[도표]` 재가압 회복률은
  음극 쪽 `R_LF` 에서 **≈65 %**, 양극 쪽 `R_MF` 에서 **≈23 %** 다. 4호 초록·결론은
  양극으로 돌리지만 자기 그림이 다르게 말한다 (4호 digest D8).
- **3호가 `θ_AM` 을 쟀다고 주장하지 않는다.** 3호의 RVE 에서 `θ_AM` 은 **가정으로 1** 이다
  (입자 1 개 + "탄소 바인더로 집전체에 연결" 가정). 위 율 극한이 깨끗한 것은 **다른 두
  항이 그 모델에서 0 이기 때문**이고, 실제 전극에서는 `θ_AM < 1` 이 남는다.
- **`η` 의 지배 인자가 하나라고 주장하지 않는다.** 전극 척도(2호: 굴곡도·`R_GB`)와
  입자 척도(3호: 입계 확산도 `D_GB`) **둘 다**다. `[도표]` 3호 Fig. 6h 에서 `D_GB` 를
  `0.05 → 20 × D_bulk` 로 바꾸면 1C 정규화 용량이 **0.48 → 0.985** — 재료도 기하도 같은데
  겉보기 용량이 두 배이고, **OCV 로는 안 보인다.**
- 이 수치들은 **LCO/LLZO 소결 복합양극 · Li 금속 음극(이상 접촉) · 두께 50 µm ·
  방전 1 회 · 구조 실현 1 개**라는 한 모집단의 것이다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지가 그 미결 항목 1 의 **세 번째 항**을 추가한다.
- [[composite-cathode-percolation-utilization]] — `θ_AM` 의 정의와 곱셈 축퇴. 이 페이지가 그 위에 `η` 를 얹는다.
- [[assb-pressure-reapplication-separation-test]] — **두 번째 분리 연산자.** 율이 `η` 를
  지우고, 압력이 `θ_AM` 을 되돌린다. 남는 것이 `Q_material` 이다.
- [[anode-free-li-inventory-accounting]] — **음극 두 항**(`L_anode`, `Q_anode,rev`)의
  본체. 그리고 `η` 가 `LLI` 를 가린다는 것의 수치.
- [[assb-stack-pressure-operating-window]] — `η(P)` 의 축. 6호가 **제작 ↔ 운전**으로 쪼갰다.
- [[thermo-kinetic-loss-partition]] — 액체셀 축의 같은 형식(전류를 관측 축으로 쓰는 분해).
- [[ag-c-interlayer-lithium-phase-path]] — 음극 쪽 `Q_material` 이 율 의존이라는 것의 출처(7호).
- [[fitting-degeneracy]] — 이 3 항 중 앞의 두 항이 OCV 에 대해 만드는 null 방향.
- [[near-optimal-set-width-measurement]] — 율을 하나 더 넣었을 때 폭이 얼마나 줄어드는지 잴 기계.
- [[assb-maxwell-ocv-derivative-channels]] — **void ≠ `Q_apparent`** 실측(14호)과 그것을 보는 관측 `F(∂E/∂P)_T`.
- [[halfcell-ocp-shape-invariance]] — 아핀 창 모형이 깨지는 자리. 3호가 **두 번째 경로**를
  연다: 식 (21) 의 `μ_mech = −(1/C_max) F_c S · ∂V_c/∂θ` 때문에 **OCV 자체가 응력 의존**이다
  (⚠ 3호는 그 크기를 보고하지 않는다 — `μ_mech` 를 끈 대조군이 없다).
