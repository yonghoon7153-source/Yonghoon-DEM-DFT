---
title: ASSB 겉보기 용량의 3항 분해 — 재료 · 기하 · 동역학
description: "Q_apparent = θ_AM · η(i) · Q_material — ASSB 복합양극에서 겉보기 LAM_PE 로 보이는 것의 세 기원과, 율(rate)이 그중 하나만 지우는 성질 (Clausnitzer 2023 + Bielefeld 2019)"
created: 2026-09-16
updated: 2026-09-29
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/minnmann2022_designing-cathodes-cam-ssb-perspective.md, raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md, raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md, raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md, raw/papers/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients.md, raw/papers/li2020_synchrotron-operando-depth-profiling-soc-gradients-thick-nmc811.md, raw/papers/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance.md, raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md, raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md, raw/papers/park2021_fictitious-phase-separation-electro-autocatalysis-layered-oxides.md, raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md, raw/papers/ishidzu2016_ncm-ni-fraction-lattice-volume-change-cycle-fade.md, raw/papers/jung2015_sulfide-assb-bulk-type-issues-challenges-review.md, raw/papers/zaghib1999_lto-negative-electrode-spe-polymer-li-ion.md, raw/papers/kondrakov2017_ncm111-ncm811-lattice-strain-particle-shrinkage-cracking.md, raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md, raw/papers/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft.md, raw/papers/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density.md, raw/papers/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md, raw/papers/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps.md, raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md]
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

## ★★★★ 2026-09-23 (`assb` 22호 Strauss 2018, **실험 · ex situ XRD**) — **`θ` 와 `η` 가 처음으로 따로 측정됐다**

`raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md`. 첫 C/10 충전 뒤 2상 Rietveld 가 두 양을
**한 측정에서** 준다: 불활성(pristine 격자) 상의 분율 → `θ`, 활성 상의 `x(Li)` → `η`(덜 충전된 정도).
`[재현]` `η = (1.02 − x_active)/(1.02 − 0.31)` (분모 = LIB 4.4 V 까지의 Δx, 교정 곡선 끝점):

| | θ `[인쇄]` 기반 | η `[재현]` | θ·η | ln θ | ln η |
|---|---|---|---|---|---|
| NCM-S (d₅₀ 4.0) | 0.98 | 0.79 | 0.77 | −0.02 | −0.24 |
| NCM-M (8.3) | 0.73 | 0.65 | 0.47 | −0.31 | **−0.43** |
| NCM-L (15.6) | 0.69 | 0.69 | 0.48 | **−0.37** | **−0.37** |

- ★★★ **`Q_material` 은 그대로다** — 불활성 상의 격자가 pristine 과 같다(교정 분해능 안). 즉 이 셀에서
  **겉보기 용량 결손 전부가 `θ` 와 `η`** 이고 진짜 `LAM_PE` 는 0 이다. OCV 적합이라면 L 에서 ≈31 % 의
  `LAM_PE` 를 보고했을 것이다(`[추론]`).
- ★★ **율 연산자는 극저율에서도 불완전하다** — `[인쇄]` L 은 C/50 에서도 110 mAh g⁻¹; `θ` 가 율 불변이라면
  `[재현]` η(C/50) ≈ 110/(0.69 × 196) ≈ **0.81**. **또는 `θ` 자체가 율 의존**이다. 22호는 XRD 를 C/10 한 점에서만
  찍어 **둘을 못 가른다** — 이 페이지의 "`θ_AM` 은 율 무관" 가정이 **처음으로 시험 가능한 형태**가 됐지만 시험되지 않았다.
- ⚠ 17호 네 번째 항(`E_cut^eff`)과의 관계: `θ` 와 `x_active` 는 **양극 결정에서 직접** 읽었으므로 상대극 전위와 무관하다.
  그러나 `η` 의 분모(무엇이 "완전 충전" 인가)와 ASSB 컷오프는 **0.6 V 가정** 위에 있다.
- ⚠ 모집단: NCM622/β-Li₃PS₄ 무탄소 · In 음극 · 55 MPa · 신품 첫 충전 · 집전체 면 표층(정보 깊이 ≈3–15 µm).

## ★★★ 2026-09-23 (`assb` 23호 Koerver 2017, **실험 · EIS + XPS + SEM**) — **"접촉 손실의 원전" 의 첫 사이클 손실을 원전 숫자로 나눠 보면 대부분이 미배정이다**

`raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md`. NCM811/β-Li₃PS₄ 무탄소 | In 박(무 Li). 첫 사이클 `[인쇄]` **176 → 124 mAh g⁻¹**
(손실 52 = 0.437 mAh). 원전은 이것을 `[인쇄]` "combination"(계면층 + 수축 접촉 손실)이라 하고 **나누지 않는다.** 원전이 준 숫자로 나눌 수 있는 것만 나누면 (`[재현]`):

| 경로 | 3항 분해의 자리 | 크기 | 근거 |
|---|---|---|---|
| 계면층의 **패러데이 전하**(SE 산화) | 충전 용량에만 들어가는 비가역 전하 | **≈0.016 mAh ≈ 4 %** | `[인쇄]` "≈1 % of the solid electrolyte" 를 양극 SE 3.6 mg · 3 e⁻/PS₄ 상한으로 (셀 전체 SE 기준이면 65 % — 기준 미기재) |
| 계면층의 **옴 이동**(ΔR 140 Ω = 23.5 mV · DC 100 mV) | `η(i)` | **≲1–2 mAh g⁻¹ ≈ ≲3 %** | `[도표]` 방전 무릎 기울기 ≈12 mAh g⁻¹ V⁻¹ (컷오프 부근) |
| **미배정** | `θ`(접촉·절연 고립) · `η(i)` 의 나머지 · **상대극 고갈(네 번째 항 `E_CE`)** | **≳85 %** | — |

- ★★ **`η(i)` 가 크다는 신호는 원전에 있다**: `[인쇄]` 0.25 C 에서 66, 0.5 C 에서 4 mAh g⁻¹ — 0.1 C 도 `i → 0` 극한이 아니다. 그런데 **0.1 C 아래 율이 없다**
  (율 연산자로 `η` 를 지울 수 없다).
- ★★★ **네 번째 항이 이 셀에서 구조적으로 켜져 있다**: 상대극이 **Li 없이** 조립돼 방전 끝 재고비가 ≈Q_ch/Q_dis ≈1.4 이고, `[도표]` 방전 끝 `C_SE/Anode` 가
  ≈90 배 무너진다(평탄 이탈 서명). LTO 대조도 같다. ⇒ 17호에서 세운 `E_cut^eff = E_cell,min + E_CE(i, x_Li, 제조법)` 의 `x_Li` 항이 **방전 끝에서 0 이 아니다.**
- ⚠ **`θ` 는 여기서도 값이 없다.** SEM 틈은 존재만, 그리고 원전 SI 의 양극 호 `C` 궤적은 EIS 창 안의 접촉 면적 변화를 보지 못한다
  ([[assb-interphase-vs-contact-loss-attribution]]). 이 표는 **"접촉 손실이 크다"** 의 근거가 아니라 **"원전이 정량한 경로로는 손실이 안 닫힌다"** 의 근거다.

## ★★★★ 2026-09-23 (`assb` 24호 Stavola 2023, **실험 · operando 깊이 분해 EDXRD**) — **`η` 에 깊이 축이 붙고, 깊이 분해도 가중평균하면 `θ` 를 다시 합친다**

`raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md`. NMC111–Li₆PS₅Cl 무탄소, 110 µm(40 % 는 155 µm), 50 MPa, C/10,
20 µm 조각 6–8 개의 `(1−x)` 를 첫 두 사이클 내내. 22호가 **한쪽 면 · ex situ** 에서 한 일을 **깊이 전체 · operando** 에서 한다.

- ★★★ **`η(i)` 는 `η(i, z)` 다.** 충전 1 중간점 깊이 방향 `[인쇄]` Δx 0.145–0.338(가역 용량의 29–67 %)이 **옴 강하로 생기는 이용 지연**이다 — 지연된 조각도 반응파로
  따라잡고(Fig. S10), 40 % 셀 분리막 조각은 **방전 중에도 탈리튬**한다(`[인쇄]` 1.2 h, 0.79 → 0.74; 두 경로가 살아 있는 입자). 방향은 σ_el/σ_ion 이 정한다(70 % 집전체 쪽 ↔
  80 % 분리막 쪽 "flip").
- ★★★★ **관측 연산자**: 보고값 `(1−x̄)_k = (1 − f_k)(1 − x_active,k) + f_k(1 − x_stuck,k)` — `f_k` 는 조각별 `1 − θ`. 원전은 두 (003) 봉우리를 **높이 가중평균**(식 S14)으로
  합친다. `[도표]` **80 % 셀 집전체 쪽 조각 6 의 한 봉우리가 충전 1 내내 pristine 근처**(Fig. S17) — 22호가 "불활성" 이라 부른 모집단이 **그림에 있고 숫자에 없다**.
  ⚠ 자촉매 가짜 상분리(원전 ref 51)와도 양립 — `θ` 로 단정하지 않는다. ⇒ **분리 연산자 후보 셋째 — "깊이 분해" — 는 모집단별(scale 분율)로 풀어야 `θ` 가 떨어진다.**
- ★★★ **첫 사이클 비가역은 깊이에 균일하다** (`[재현]` Fig. 3b–e): 조각별 충전 1 − 방전 1 ≈0.20–0.21(70·80 %) — 방전 1 끝 전 조각이 `(1−x)` ≈0.80 에 모인다.
  ⇒ **비가역 ≈56 mAh g⁻¹(23호 52 와 같은 크기대)은 `η(z)` 가 아니다** — 입자 척도(고리튬 쪽 확산 둔화 · 계면층 · 동결 고립) 또는 **네 번째 항(상대극)**. In–Li 조성 미기재로
  마지막 둘이 안 갈린다. ★ **코팅 쌍**(70 %, LLSTO)이 비가역을 **≈14 %** 만 줄인다(`[도표]`, n = 1 씩) — 23호 손실 예산("계면층 몫 ≲7 %, ≳85 % 미배정")과 같은 방향.
- ★★ **22호의 표층 편향 크기**: `[도표]` 충전 1 끝 집전체 면 ↔ 전극 평균 **±0.08 `(1−x)`**(80 % 뒤처짐 · 40 % 앞섬), 부호는 σ_el/σ_ion. 한쪽 면 측정의 `η` 는 C/10 에서도 ±20 % 흔들린다.
- ★★ 쿨롱 ↔ XRD 폐합 여섯 중 다섯이 ±7 %(`[재현]`) — 그러나 **둘 다 전 CAM 질량으로 나누므로 `θ` 를 못 본다.** 22호의 "용량 독립 대조" 도 같은 한계다.
- ⚠ 모집단: 신품 2 사이클 · 셀 1 개/조건 · In–Li(조성 미상) · 기준극 0 · 율 C/10 한 점(율 연산자와 교차 불가). 수송 쪽 곱(`σ_eff = σ_bulk·ε/τ²`)은
  [[assb-tortuosity-factor-effective-conductivity-split]].

## ★★★ 2026-09-23 (`assb` 25호 Zhou 2025, **실험 · 2전극 · 압력 × 미세구조**) — **충전 쪽은 같고 방전 쪽이 다르다; 초기 압력 손해는 공통 모드**

`raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md`. 값은 전부 `[도표·벡터]`(Fig. 2c 표식 좌표) 또는 그것으로 한 `[재현]`.

- **`θ` 항의 부정 시험 — 첫 충전.** `θ` 는 충전·방전을 같이 깎는다. 30 · 10 MPa 첫 충전 coarse 216.1 / 213.2 ↔ fine 210.3 / 206.7 mAh g⁻¹(비 1.03) — **`θ` 차 0**. 차이는 첫 방전(비가역 42.6 ↔ 19.9)에 있다
  ⇒ 이 셀들의 초기 차는 `η`(리튬화 쪽) 또는 계면층 형이다(23호 손실 예산과 같은 자리).
- **율 극한**(S18, 2 MPa, `[도표]`): coarse/fine 비 0.84 / 0.80 / 0.73 / 0.66(0.1 / 0.2 / 0.3 / 0.5 C) → `i→0` ≈**0.89** ⇒ 0.1 C 결손 ≈16 % 중 ≈11 %p 만 율 무관(`θ`·`LLI` 후보).
  이 페이지의 "율이 `η(i)` 만 지운다" 의 **실험 적용 예**다(4 점 · 셀 한 쌍).
- **공통 모드** — 30 → 2 MPa 2 사이클 방전 손해 coarse −26.5 ↔ fine −30.7: **미세구조 무관 손해**는 복합양극의 `θ`·`η` 어느 쪽으로도 배정하면 안 된다(두 셀이 공유하는 Li 음극 · 분리막이 후보) —
  17호의 **네 번째 항(상대극 컷오프)** 자리. 저자 적합(S19)에서도 Li 계면이 가장 큰 항이다.

## ★★★★ 2026-09-23 (`assb` 29호 Yanev 2024, **실험 · 2전극 CA · 14 복합체 · 신품**) — **율 극한을 적합으로 실행한 첫 편, 그리고 그 극한이 언제 안 보이는지를 저자가 인쇄했다**

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md`. 17호와 같은 연구실.

- **이 페이지 "율이 세 항 중 하나만 지운다" 의 계보 첫 체계적 실행.** CA 방전 한 번(0.02 C 종료)을 `R = I/∫I dt` 로 바꿔 `Q(R) = Q_M/(1+2(Rα)ⁿ)` 로 적합 — `Q_M` = `[인쇄]` "maximum capacity which can be discharged at an infinitely low rate" = 이 페이지의 **`θ_AM·Q_material`**, `α`·`n` = **`η(i)`**.
  `Q_material` 은 같은 분말의 LIB 반쪽전지(0.1 C, gran 193 · sc 213 mAh g⁻¹)로 떼어 `Q_M/Q_LIB` = 이용률 — **3항이 신품에서 셋 다 이름을 얻는다**.
- ★★★★ **극한이 안 보이면 `θ·Q` 와 `η` 는 한 조합이다.** `[인쇄]` sc90 "not enough information … to accurately fit the Q_M and α … high dependencies close to unity"; `[재현]` 고율 극한 `(Q_M/2)(Rα)⁻ⁿ` 는 `Q_M·α⁻ⁿ` 만 본다.
  `[도표]` 실제로 **어느 셀도 0.02 C 에서 평탄하지 않다** — `Q_M` 은 평탄이 보이는 셀에서 실측보다 낮고(gran51 ≈185 ↔ 194) 안 보이는 셀에서 높다(sc84 ≈236 ↔ 177 · LIB 213 초과).
  ⇒ 위 처방("최소 두 율, `i → 0` 포함")에 **조건**이 붙는다: **최저 율이 평탄 안에 있어야** 극한이 `η` 를 지운다. 곡선이 로그 축 끝까지 기울어 있으면 외삽 용량은 식 모양의 산물이다.
- ⚠ 3호(Liu)가 좁힌 처방(`Q_material` 도 율 의존)과는 **독립인 두 번째 좁힘**이다 — 3호는 고율이 재료를 깎는 문제, 29호는 저율이 창 밖인 문제.
- **동역학 항 안에서** 29호는 저항성(SE, `n` → 1) ↔ 확산성(AM, `n` → 0.5)을 가르고, 확산성 결손을 **AM|SE 피복률 `φ`**(`√(D_app/D_LIB)`, 53 → 18 % · 85 → 3 %)로 돌린다 — 표면 일부 접촉 손실이 **용량이 아니라 `η`** 로 간다는 이 페이지 [[assb-tortuosity-factor-effective-conductivity-split]] 표 셋째 줄의 실측 판. ⚠ `φ` 는 가정 위의 비이고, `n` ≈0.5 는 catholyte 전송선(TLM)의 √t 와도 양립한다(판별 안 함).
- 2전극 — 17호의 **네 번째 항(상대극 컷오프·과도)** 은 빠져 있다. 같은 음극 조성에서 17호가 CA 시작 `E_CE` ca. 0.9 V 를 인쇄했고, `n` 은 바로 그 첫 구간의 기울기다.
- ↳ **2026-09-28 29호 SI 보강**(`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md`): ① 위 조건(최저 율이 평탄 안)의 **수치** — Tab. S2 dependency 순위가 창 끝 평탄 도달률과 ρ −0.991, 도달률 ≲0.8 이면 ≥0.97. ② **외삽 `θ·Q` 의 물리 상한** — 형성 첫 CCCV 충전(Fig. S6)이 그 셀이 뽑은 전하를 준다: sc84 `Q_M` 236 > ≈209 · sc90-BM 179–205 > ≈158 mAh g⁻¹ — 극한이 안 보이면 외삽이 상한 밖으로 간다. ③ ★ **방향 비대칭** — sc90 은 첫 충전에서 ≈103 mAh g⁻¹ 을 뽑고 0.1 C 방전 ≈17 · CA ≈26 · `Q_M` 60: `θ_AM·Q_material` 칸(`Q_M`)이 비연결이 아니라 **재리튬화 쪽 `η`** 를 품는다. 충전 전하와 방전 외삽의 차가 이 페이지 3항에 **방향 축**을 요구한다(`[해석]` · 신품 한 편 · SE 산화 상한 ≈9 mAh g⁻¹ 로 대부분 배제).

## ★★ 2026-09-23 (`assb` 56호 Bielefeld 2022, **FEM 모델 · 새 측정 0**) — **표면 피복과 큰 입자, 둘 다 `η(i)` 항으로 들어간다 — 그리고 `θ_AM` 은 손으로 1 이었다**

`raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md`. 모델 명제다(실측 0).

- **표면 피복(void)은 `η(i)` 에만 산다** — `[도표]` 1-입자 모델 피복 손실 48 %: 0.02 C 컷오프 용량 −3 % · 0.5 C **−25 %**. 율 극한이 지운다 — 이 페이지 핵심 성질("율이 셋 중 하나만 지운다")의 3D 해상 모델 확인. 그러나 **같은 피복률에서 분포가 과전압을 ×2.6–4.5 바꾼다**(Fig. 9) — `η(i)` 가 피복률 한 스칼라의 함수가 아니다.
- **큰 입자의 "not activated at all" 도 `η(i)` 다** — `[인쇄]` L-PSD(≤ 20 µm) 큰 입자 중심이 0.2 C 끝에 리튬화된 채 남는다(Fig. 6). 모든 입자가 연결돼 있으므로 `θ_AM` 이 아니고, `[도표]` 0.02 C 에서 L ≈178 ↔ S ≈188 mAh g⁻¹ 로 대부분 돌아온다.
- **`θ_AM` 은 이 편에서 출력이 아니라 입력 1** — SI `[인쇄]` 42 vol% 무작위 구는 1호 모델대로면 퍼콜레이션 불가 → placeholder + 고립 입자 "moved manually". ⇒ 이 편의 모든 용량 차이는 설계상 `η(i)` 쪽이다 — 3 항 분해를 이 모델로 채점하면 `θ_AM` 칸은 비어 있다.
- ⚠ 검증 모델은 실험 void 14 % 를 SE 로 채웠다 — 실험의 `η(i)` 에 들어 있을 void 몫이 모델에 없는데 "good agreement" 로 닫혔다.

## ★★ 2026-09-28 (`assb` 64호 Koerver 2017 *JMCA*, **실험 · 컷오프 넷 × 25 사이클 · 23호와 같은 셀 설계**) — **산화환원 계면층은 3 항 곱 밖의 덧셈 항이고, 첫 방전 결손의 일부는 둘째 사이클에 돌아오는 `η` 다**

`raw/papers/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps.md`. NCM811 : β-Li₃PS₄ 70 : 30 무탄소 | In 박(무 Li) · 상한 4.0 / 4.3 / 4.6 / 5.0 V vs Li · 0.1 C · 컷오프당 셀 2.

- ★★ **덧셈 항.** `[인쇄]` "In the end, every redox reaction of the electrolyte in the electrode will add up to the total capacity obtained for each cycle" — 계면층의 가역 전하는 이 페이지의 곱에 들어가지 않고 **더해진다**:
  `Q_apparent = θ_AM · η(i) · Q_material + Q_SE,rev` (`[해석]`). 크기는 원전에 0 · `[재현]` 상한 = 양극 복합체 SE 3.6 mg 전부 1 e⁻/PS₄ ≈**0.54 mAh = 64 mAh g⁻¹_NCM**(2 e⁻ 면 ×2). OCV 적합이 이 항을 `Q_material`(스케일)에 흡수하면 계면층이 자라는 셀에서 겉보기 `LAM_PE` 가 **작아 보인다**(방향만). 5.0 V 둘째 방전 평탄이 그 전압 서명 후보(크기 인쇄 0).
- ★ **비가역 몫은 충전 쪽에만 들어가고 `LLI` 가 아니다** — SE 산화는 Li⁺ 를 음극에 쌓는다(Fig. 8 캡션) ⇒ 무 Li In 셀의 첫 사이클 CE 결손 = `θ`(고립) + `η` + NCM 비가역 + **SE 산화 전하**. 23호 예산의 "계면층 패러데이 몫 ≈4 %" 는 SE 1 % 기준이었다 — 64호 상한은 그 몫이 원리적으로 첫 결손(58–79 mAh g⁻¹)과 같은 자릿수까지 갈 수 있다는 것까지만 말한다.
- ★★ **첫 방전 결손의 ≈28–37 % 는 되돌아오는 `η` 다**(4.0–4.6 V) — `[도표]` 둘째 − 첫 방전 +21.0 · ≈+27 · +22.4 mAh g⁻¹(결손 58 · 73 · 79 의 36 · 37 · 28 %) · 5.0 V ≈+3(4 %). 4.0 V 에서 방전 상태 `R_cathode/SE` 105.8 → 58.7 Ω 과 동행(`[인쇄]` "formation"). ⚠ 4.0 V 의 그 호는 `C` 0.1–0.85 mF(다른 셀 ×250–700)라 양극 것이라는 근거가 약하다 — 되돌아온 몫이 음극 쪽 `η` 일 가능성도 남는다.
- ⚠ **5.0 V 감쇠(둘째 129 → 25 번째 49 mAh g⁻¹)의 칸은 정해지지 않는다** — NCM 산소 방출(인용[34,35] · `Q_material`) · 계면층 저항(`R` ×5.5 · `η`) · 저주파 호 ≥2.5 kΩ(음극 배정 · 네 번째 항)이 같이 있고 **율 극한 대조 0**(0.1 C 한 율).

## ★★★ 2026-09-28 (`assb` 65호 Nam 2018 *JPS*, **실험 · 반쪽 13 전극 공정 대조 · 신품**) — **첫 충전 상한: 공정이 바꾼 첫 방전 중 `θ_AM` 몫은 첫 충전 차로 위에서 막히고, 나머지는 방전 쪽 `η` 다**

`raw/papers/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage.md`. NCM622(LiNbO₃) : Li₆PS₅Cl : C65 (: NBR 1.4 wt%) \| Li₀.₅In · 건식 ↔ 슬러리 × 70 · 80 · 85 wt% × 20 · 28 mg cm⁻² + 예비혼합 · 0.1 C · 30 °C · 3.0–4.3 V vs Li/Li⁺ · 셀 수 미인쇄.

- ★★★ **방향 축으로 3 항을 가른다.** `θ_AM`(통째 고립)은 신품 첫 충전(완전 리튬화 → 탈리튬)과 첫 방전을 같은 비율로 깎고, `η`(재리튬화 말단 · 계면 · 수송)는 방전만 깎는다 ⇒ 대조군 사이 첫 충전 비는 `θ_AM` 변화의 **상한**:
  `Δθ/θ ≤ ΔQ_ch/Q_ch` → 첫 방전 결손 중 `θ` 몫 ≤ `Q_dis·(ΔQ_ch/Q_ch)/ΔQ_dis`.
  `[도표]` 첫 충전(Fig. 2 · 7d) ↔ `[인쇄]` 첫 방전(표 1): 바인더 70L 187.8 → ≈182.7 · 155 → 133 ⇒ ≤19 % · 80L 185.1 → 177.3 · 152 → 122 ⇒ ≤21 % · 85L 179.2 → 158.7 · 130 → 95 ⇒ ≤42 % · 70H ≈0 · 80H ≤16 % · 예비혼합 158.3 → 173.7 · 94.8 → 126.9 ⇒ ≤29 %.
  ⇒ `[해석]` 바인더 · 예비혼합이 바꾼 0.1 C 첫 방전의 **≥58–100 % 는 `η` 칸**이다 — 이 페이지 식에서 `θ_AM·Q_material` 이 아니라 `η(i)` 가 움직였다. 29호 SI 의 "방향 비대칭"(신품 한 셀) · 25호의 "충전 쪽은 같고 방전 쪽이 다르다"(압력)에 이은 **세 번째 같은 모양 · 첫 공정 대조판**.
- ★★ **율 시험 뒤의 회복** — `[도표]` S6: 두꺼운(H) 전극은 30 사이클 율 시험 뒤 0.1 C 가 첫 사이클보다 크다(D85H 85 → 88.5 · W85H 78 → 89.1 · D70H 149 → 153.8) — 첫 방전이 `η` 로 잘린 몫이 돌아온다(64호 "첫 결손의 `η` 형 회복" 과 같은 방향).
- ⚠ 조건: 같은 충전 컷오프 · 같은 율 · 첫 충전 SE 산화 전하(64호 덧셈 항 `Q_SE,rev`)가 두 전극에 다르게 섞이지 않을 것 · 판독 ±1 mAh g⁻¹ · 셀 하나씩 · 충전 쪽 분극이 섞일수록 상한이 느슨해진다(방향은 유지). 같은 편의 GITT 피복률은 `θ` 가 약분된 양(연결 입자 기준)이라 이 상한과 경쟁하지 않는다([[assb-lampe-contact-product-degeneracy]] 65호 줄).

## ★★ 2026-09-28 (`assb` 66호 de Biasi 2017 *JPCC*, **실험 · 액체 반쪽 · operando XRD 교정 · ASSB 아님**) — **22호 `η` 는 교정 곡선의 축을 빌린다: `θ`(상 분율)는 교정 없이 서고, `x_active` · `η` · 용량 닫힘은 교정 셀의 통과 전하에 걸린다**

`raw/papers/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density.md`. NCM 여섯 조성 · 파우치 LIB(Li 금속 · LP47) · 넷째 충전 C/10 · 표 S1 101 행. 교정 자체는 [[nmc-lattice-li-content-calibration]].

- ★★★ **교정 축 = 통과 전하.** `[인쇄]` "The lithium content was calculated from the electrochemical data"(22호 교정 캡션도 같은 문장) · "we assumed that Coulombic efficiencies of less than 100% are a result of Li loss from the cathode material only" · 공칭 δ₀ 1.02 · ICP 0
  ⇒ 이 페이지 22호 절의 `η = (1.02 − x_active)/(1.02 − 0.31)` 은 분자 · 분모 모두 교정 셀(액체, θ_ref = 1)의 전하 눈금 위에 있다.
- ★★★ **교정 선택의 크기** `[재현]`: 같은 연구망 두 NCM622 교정이 x ≈0.067 가로 이동 → 22호 활성 상 `x` 가 교정 선택만으로 시편마다 0.10–0.16 폭(L 0.41–0.57 · M 0.41–0.54 · S 0.36–0.45)을 오간다 ⇒ `η` 는 ≈±0.1 움직이고 `θ` 는 안 움직인다.
  22호 L 의 "θ ≈0.69 · η ≈0.69 — 결손의 절반" 분할은 `θ` 쪽이 측정 · `η` 쪽이 교정 규약 위다.
- ★★ **용량 닫힘도 교정 의존** — 22호 ±7 %(자기 교정) → 이 편 곡선(원시 V)이면 L · M +11…+16 %. 닫힘은 "상 분율 + 교정" 합성의 검증이지 상 분율 단독의 검증이 아니다.
- ⚠ 모집단: 액체 반쪽 · 넷째 사이클 · BASF 로트 — ASSB 에서 잰 교정 곡선은 이 위키에 0.

## ★★ 2026-09-28 (`assb` 67호 Kondrakov 2017 *JPCC*, **실험 + 계산 · 액체 반쪽 · NCM811 · ASSB 아님**) — **겉보기 감쇠의 `η` 몫에 저자가 이름을 붙였고, 22호 `η` 가 기대는 교정 축은 같은 연구망 안에서 규약이 셋이다**

`raw/papers/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft.md`. NCM811 코인 컷오프 여섯 × 50 사이클 · operando XRD(전처리 셀) · 22호 ref 21. 교정 규약은 [[nmc-lattice-li-content-calibration]] 67호 절.

- ★★ **`η` 몫의 인쇄 표본(액체).** `[인쇄]` "the capacity fading is virtually enhanced at such conditions because overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage.
  Thus, the data shown in Figure 1a reflect the 'worst-case performance'" — 정전압 없는 반쪽전지 사이클에서 겉보기 용량 감쇠의 일부가 **분극(`η`)** 이라는 저자 문장(양 0). 3항 분해의 `η` 항이
  액체셀에서도 "균열 → 과전압" 경로로 이름 붙은 표본이다.
- ★★ **22호 `η` 의 교정 축 — 규약 항의 크기.** 66호 절의 "교정 선택으로 `η` ≈±0.1" 중 **규약 항**은 같은 연구망에서 0.10(`x₀` 1.00 ↔ 0.90)까지 흔들린다(`[재현]` NCM811 쌍 전압 맞춤 +0.10). 22호 첫 충전
  교정은 규약 항과 시편 항을 전압 맞춤으로 가르지 못한다(+0.157 → +0.033) — `θ`(상 분율)는 여전히 교정 없이 선다.
- ⚠ 모집단: 액체 반쪽 · NCM811 · BASF 전극 — ASSB 에서 잰 교정 곡선은 이 위키에 여전히 0.

## ★★ 2026-09-28 (`assb` 68호 Chen 2013 *Energies*, **SOFC 해석 모형 · 실험 0 · ASSB 아님**) — **SOFC 식에는 용량 칸이 없다: `1 − P^e` 는 반응 자리에만 들어가고, ASSB 로 옮기면 `θ_AM` 칸으로 가야 한다**

`raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md` (22호 ref 26 — 22호가 "in agreement with percolation theory" 로 기댄 원전).

- 이 편은 3 항 분해의 `θ_AM` 과 **같은 양**(전자 퍼콜레이팅 클러스터 소속 분율 `P^e`)을 해석식으로 준다 — `[재현]` `θ₀ = P^e(6ψρ/(ψρ + 1 − ψ))`, ρ = SE/CAM Sauter 반경비. 정적 · 무한계 · 폭 0.
- ★ 그러나 SOFC 는 **저장 용량이 없다** — 끊긴 LSCF 는 **반응 자리만** 잃고(식 (7) · (9) 의 곱), 이 편에서 `P^e` 가 들어가는 곳은 전부 **동역학 쪽**(TPB 길이 · 표면 자리)이다. ASSB 로 옮기면 끊긴
  CAM 은 용량을 잃으므로 같은 `P^e` 가 `θ_AM`(용량 곱) 칸에 들어가야 한다 — `[해석]` **SOFC 식을 그대로 가져오면 `θ` 를 `η` 칸(반응 자리 ↔ 과전압)에만 넣는 모형이 된다.**
- 22호 `θ`(= 1 − `f_inactive`)와 대면: 저자 배정 읽기로 세 점 동시 불가 · 상한 읽기로 M 의 불활성 거의 전부가 전자 밖 — 3 항 분해에서 22호 M 의 `θ` 몫은 이 식으로 정해지지 않는다(68호 digest §(b)).

## ★★ 2026-09-28 (`assb` 69호 Kondrakov 2017 *JPCC* 121, 3286, **실험 · 액체 반쪽 · NCM111 · NCM811 · ASSB 아님**) — **첫 충전의 앞머리 전하는 격자를 움직이지 않고, "균열 → 용량" 은 이 편에서 상관이다**

`raw/papers/kondrakov2017_ncm111-ncm811-lattice-strain-particle-shrinkage-cracking.md`. 코인 45 °C · C/2 · 80 사이클 · 신품 파우치 operando XRD 두 사이클 · 광학 입자 부피(둘째 사이클) · 단면 SEM. 교정
규약은 [[nmc-lattice-li-content-calibration]] 69호 절.

- ★★ **첫 충전 용량 안의 "격자 무응답" 몫.** `[재현]` NCM811 첫 충전 앞머리 Δx ≈0.12–0.18 이 3.77 V 평탄에서 격자를 움직이지 않는다(둘째 충전은 0.01–0.04) — 첫 사이클 결손(0.106)과 같은 자릿수.
  3 항 분해로 옮기면 첫 충전 전하가 전부 활성 입자의 탈리튬이라는 가정(65호 "첫 충전 상한" 의 분자)에 **벌크 탈리튬이 아닌 전하**가 섞일 수 있다 — 섞이면 상한이 느슨해지는 방향(`[해석]` ·
  액체 NCM811 · NCM111 에는 없다).
- ★★ **"균열 → 용량 감쇠" 는 두 조성 대비의 상관.** `[인쇄]` "may be caused by the volume changes … a hypothesis that requires experimental proof" · "it may also lead to a loss of electrical contact of the
  active electrode regions" — `θ`(고립) 경로에 이름만 붙는다. 광학 크기 신호의 균열 기여는 "linear background subtraction" 으로 지워졌다 — 사이클 축 `θ` 의 측정 후보가 양으로 남지 않았다.
- ★ **`η` 쪽 — 평균 방전 전압 하락의 전극 귀속 미분리.** `[도표]` C/2 평균 방전 전압 NCM811 −0.25 V · NCM111 −0.13 V / 77 사이클; `[인쇄]` "the lithium anode and other cell components also contribute
  to the increase in cell resistance" ↔ 결론 "related to the impedance buildup in the cathode"(EIS 0).
- ★ **틈 채널의 θ 몫(23호).** 23호 첫 충전 176 mAh g⁻¹ 을 이 편 **첫 충전** 축(θ = 1)에 놓으면 격자 −2.0…−2.4 % — 23호 틈을 격자로 내려면 활성 입자가 4.3 V 상태(−5.1 %)에 가야 하고 그 θ 는
  ≈0.85; 입자 수축(광학 −7.8 %)은 격자의 ×1.5 라 층위도 몫이 된다.
- ⚠ 모집단: 액체 반쪽 · 두 조성 · BASF 전극 · 45 °C(사이클) ↔ 25 °C(격자) — ASSB 에서 잰 것은 여전히 0.

## ★ 2026-09-28 (`assb` 70호 Zaghib 1999 *JPS* 81–82, 300, **실험 · LTO 음극 · Li 금속 2전극 · 무용매 SPE · 60/80 °C · ASSB 아님**) — **R-LTO 영점의 '원전' 값은 2전극 부하 셀 전압이고, CE ≈101 % 인 채 용량이 −44 % 다**

`raw/papers/zaghib1999_lto-negative-electrode-spe-polymer-li-ion.md`. 4 cm² 실험 셀 C/12(Fig. 4) · Ah 급 셀 s852(60 °C · 1.75 Ah) · s851(80 °C · 2.7 Ah) 사이클(형식 미인쇄) · ASI(전류 차단 5 · 30 s).

- ★★ **`E_cut^eff` 의 원점 쪽 — R-LTO 영점의 원전 값은 부하 셀 전압이다.** `[도표]` Fig. 4 방전 평탄 1.54 → 1.50 V · 충전 1.67 → 1.59 V(C/12 · 2전극 · SPE · 온도 미지정) · 차 0.09–0.13 V · `[인쇄]` "about 1.5 V" — `1.55` 0 회. 4 항 분해의 `E_CE(i, x, 제조법)` 에 R-LTO 를 넣을 때 그 상수(1.55)의 23호 경로 원전이 "±0.05 V 띠 안의 값" 으로 넓어진다 — [[assb-li-in-reference-potential-window]] 70호 절.
- ★★ **CE 는 손실을 안 본다 — 폴리머 판.** `[도표]` Effic. Ah ≈101 %(정의 미인쇄)로 1495 사이클 평탄 ↔ 방전 용량 1.75 → 0.98 Ah(−44 %) · Effic. Wh 96 → 88 % · ASI ≈95–100 → 270–292 Ω cm². `Q_apparent` 의 감쇠가 `θ_AM` · `Q_material` · `η` 어디로 가는지 이 편은 0 — `η`(ASI ×1.7–3 · Wh 효율 −8 %p) 몫이 있다는 방향만.
- ★ **양극이 없는 반쪽 — `LAM_PE` 자리가 비어 있다.** LTO 가 이 셀의 (+) 이고 Li 금속이 (−) — 3 항 분해의 양극 항은 LTO 자신이며, 용량 −44 % 를 LTO 손실 · Li | SPE 계면 · SPE 열화로 가르는 자료가 없다(2전극 · EIS 0).
- ⚠ 모집단: 1999 · SPE · 60–80 °C · n = 1 · 오차 0 · 셀 형식 미인쇄 — ASSB 로 옮길 수치 없음.

## ★ 2026-09-28 (`assb` 71호 Jung 2015 *Isr. J. Chem.* 55, 472, **종설 · 1차 측정 0**) — **치밀화 ↔ 이용률은 재인용 정성이고, `E_cut^eff` 의 원점(상대극 영점)이 한 지면에 두 관례다**

`raw/papers/jung2015_sulfide-assb-bulk-type-issues-challenges-review.md`. 황화물 bulk 형 ASSB 종설(UNIST Jung · 2015) — 그림은 거의 전부 재인용, 압력 값 0.

- ★ **`θ_AM` 쪽 — 재인용.** `[인쇄]`(재인용 [4,9,42v]) 열간 압착(> Tg) → "poreless, dense pellets" → "increased utilization of the active materials … as demonstrated in the case of Li₄Ti₅O₁₂" · `[도표]` Fig. 13c 완전지(LTO/80Li₂S·20P₂S₅/LiNbO₃-LCO) 방전 ≈120 ↔ ≈54 mAh g⁻¹ — 같은 대조에 "massive interfacial reaction"(LCO)이 같이 들어 있어 `θ_AM` 몫을 가를 수 없다(압력 · 이용률 정의 미인쇄). 이 편 자신의 진술(인용 0): 복합전극 설계가 "morphology, percolation of SEs, and contacts between the active materials and the SE" 에 좌우 · 이상 구조 = SE 균일 피복 + 탄소 배선 · SE 30–65 wt%(조사).
- ★ **`η` 쪽 — 재인용.** Li₇P₃S₁₁ 냉간 압착 펠릿 1.4 ↔ 치밀화 17 mS cm⁻¹(표 1 · [4,21e]) — SE 유효 전도도가 제조 이력(입계)을 품는다. 판정 근거로 쓰지 않는다.
- ★★ **`E_cut^eff` 의 원점 — 상대극 영점 두 관례.** 본문 Li-In 0.62 V(재인용 [42b] Takada 1996 + [62] Jung 2008 · 0<x<1) ↔ 옮겨 실은 이중 축 그림(Fig. 8b · 9c) `[재현]` 0.600 V — 환산 컷오프가 관례에 따라 20 mV 다르다. 그리고 LiCoO₂/In 첫 충전 곡선은 `[도표]` ≈0.4 V 에서 시작한다(Fig. 6a) — 무 Li 상대극이 짝을 찾기 전 구간의 `E_CE` 는 영점 상수가 아니다([[assb-li-in-reference-potential-window]] 71호 절).
- ⚠ 모집단: 2015 종설 · 재인용 · 압력 값 · 오차 · 셀 수 0 — 옮길 수치 없음.

## ★ 2026-09-28 (`assb` 72호 Ishidzu 2016 *SSI* 288, 176, **실험 · 액체 반쪽 · 여섯 조성 · 3전극 EIS(`R` 만) · ASSB 아님**) — **유지율 감쇠의 배정이 R 이름표 둘로 끝난다: `θ_AM` 은 R2 로 배제, 나머지는 R3(계면)로 — `Q_material` 몫은 묻지 않았다**

`raw/papers/ishidzu2016_ncm-ni-fraction-lattice-volume-change-cycle-fade.md`. 3전극 셀 · 2.5–4.5 V · 0.5 C · 40 °C 사이클(표 2 로 100 사이클) · 유지율은 전후 0.1 C · 25 °C · EIS 4.5 V · 40 °C.

- ★★ **`θ_AM` 쪽 — 배제의 근거가 이름표다.** `[인쇄]` "If R2 increased, a part of cathode particles would be electronically isolated. So, it implied that the cathode particle utilization was not greatly
  influenced after the cycling" ↔ 표 2 R2 ×2.6–3.0 · R2 의 대상은 양극층 ‖ 집전체(51호) · 완전 고립 입자는 호에서 빠진다 — 3 항 분해의 `θ_AM` 은 이 편에서 **재지 않고 이름표로 1 에 고정**된다.
- ★★ **`η` · 계면 쪽 — R3 가 몫을 받는다.** R3 ×10.6–34(40 °C · 4.5 V) · `[인쇄]` "the capacity degradation was mainly related to the cathode/electrolyte interface". `[재현]` R1 + R2 + R3(100 사이클) ×
  0.1 C 전류(적재 10 mg cm⁻² × 2.01 cm² · 1C = 초기 용량 가정) ≈52 mV(A) · 73 mV(F) — 유지율은 25 °C 에서 쟀고 방전 곡선 기울기가 인쇄되지 않아 `η` 몫을 용량으로 바꾸지 못한다.
- ★ **`Q_material` 쪽 — 묻지 않았다.** 격자 `ΔV`(첫 충전 · 4.5 V)는 재료 상태 신호지만 사이클 뒤 격자 · 방전 곡선 · 반쪽 재측정 0 — `LAM`(재료) ↔ `θ`(연결) ↔ `η` 셋의 몫이 유지율 75.7 → 62.7 % 한 수에 묶여
  있다. 저자의 균열 서사("create new interface … active for the electrolyte oxidation")는 `θ` 가 아니라 계면 면적 · `j₀` 쪽이다.
- ⚠ 모집단: 액체 반쪽 · 자체 공침 여섯 조성 · 셀 수 · 오차 0 · 조건 셋(`ΔV` 0.05 C · 유지 25 °C 0.1 C · R 40 °C 4.5 V)이 섞인다 — ASSB 로 옮길 수치는 없다.

## ★ 2026-09-28 (`assb` 73호 Minnmann 2021 *JES* 168, 040537, **실험 · 신품 · 무탄소 NCM-622 \| Li₆PS₅Cl · 조성 스윕 · VGCF 쌍 · SE 입도 쌍 · In/(InLi)ₓ 반쪽**) — **신품에서 `θ_AM` 과 `η` 를 개입 쌍 둘로 가르려 한 편: 도전재 쌍은 `θ₀`(상한 ≈13 %), SE 입도 쌍은 `η` 쪽 — 그러나 저율 판정은 그림 정규화에 걸린다**

`raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md`. 반쪽 셀 12 mg(15.3 mg cm⁻²) · 25 °C · ≈40 MPa · 0.1 · 0.25 · 0.5 · 1 C(200 mAh g⁻¹ 가정) · 셀 둘 · 전압 창 미인쇄 · 방전 비용량만(곡선 SI).

- ★★ **`θ_AM` 쪽 — 도전재 개입 쌍.** 33 vol%(무탄소) + VGCF(1 mg / 100 mg): `[도표]` q_mat +19.7 · +22.4 · +17.0 · +10.8 mAh g⁻¹(0.1 · 0.25 · 0.5 · 1 C) — `[인쇄]` "increased its material-specific charge during charging (Table SIV) and discharging by 10–20 mAh g⁻¹ at all C-rates. This indicates that this improvement is mainly caused by creating additional contacts to CAM particles that would have been isolated" — 65호 "첫 충전 상한" 과 같은 논리(충 · 방이 같이 늘면 고립)를 저자가 인쇄 · 충전 값은 SI · 율 의존이 ≈2 배 폭이라 `θ₀` 몫은 **0.1 C 이득 ≈13 %(= 1 − 137.3/157.0)를 상한**으로만 쓴다.
- ★★ **`η` 쪽 — 이온 수송이 고 CAM 의 율 손실을 쥔다.** 61 vol%: 0.1 C 132.3 → 1 C 15.4 mAh g⁻¹(−88 %) ↔ 33 vol% 137.2 → 81.9(−40 %) · σ_ion,eff 3.04e-6 ↔ ≈2.6–2.9e-4 S cm⁻¹ · τ²_ion 130 — 저자 "direct correlation"(정량 옴 강하 ↔ 용량 대조 0). 61 vol% + VGCF 는 오히려 1 C 에서 −53 %(저자 가설 "degradation at the carbon-solid electrolyte interface during cycling" — 측정 0).
- ★ **SE 입도 쌍 — 한 손잡이가 두 항을 같이.** 61 vol% coarse ↔ fine SE: σ_ion ×3.2 · σ_el ×0.49 · 용량 ↑(0.25 C 이상은 어느 읽기로도). ⚠ 저율(0.1 C) 이득은 Fig. 6 coarse 막대가 q_mat 축 이름표 아래 **q_com 값**이라(D1) 132.3 ↔ 133.3(+0.8 %) 또는 155(+17 %) 사이 — `θ` 증가 여부를 가를 수 없다.
- ⚠ 모집단: 신품 · 0 % SoC EIS · 조성당 셀 수 · 산포 미인쇄 · 방전 곡선 · OCV 0 — `Q_material` 은 200 mAh g⁻¹ 가정.

## ★★ 2026-09-28 (`assb` 74호 Park 2021 *Nat. Mater.* 20, 991, **실험 + 모형 · 액체 반쪽(Li 금속 · LP-40) · NMC111 판 · 응집체 · operando XRD · 급랭 STXM · ASSB 아님**) — **`η` 에 충전 쪽 성분이 붙는다: 전기-자촉매 지연 무리는 한 사이클 안에서 `θ_AM` 과 같은 서명이고, 가르는 것은 시간 궤적(휴지 · 율 · 깊이 · 다음 사이클)이다**

`raw/papers/park2021_fictitious-phase-separation-electro-autocatalysis-layered-oxides.md`. 파우치 · 4 : 4 : 2 · ≈20 µm · 판 2.24C · 응집체 4C ↔ C/15 · 둘째 사이클 · 급랭 STXM(2C · C/20) · 형성 뒤 방전 끝 정전압으로 완전 리튬화.

- ★★ **`θ_AM` 과 같은 모양의 `η`.** 빠른 탈리튬에서 입자 간 이봉 — `[도표]` 평균 0.80 에서 넓이 42.6 % 가 Li > 0.933(Fig. 2a) · `[데이터]` Source Data 과잉(Li ≥0.95) 최대 +0.235 → 충전 끝 +0.002. 충전 컷오프에 남은 미반응 무리는 첫 충전을 깎고,
  방전에서는 이미 차 있으니 첫 방전도 같은 양 깎는다 — **한 사이클 안에서는 `θ_AM` 과 구별되지 않는다.** `[인쇄]` 기구: 탈리튬될수록 커지는 교환전류(식 S3 `A > 0`) · 리튬화는 율과 무관하게 자억제 · 문턱 ∝ `j₀`(판 · 출발 1.0 →
  0.231 C) · 완전 리튬화 출발에서 가장 크다.
- ★★ **65호 "첫 충전 상한" 은 선다 — 느슨해진다.** 상한 부등식(`θ` 변화 ≤ `ΔQ_ch/Q_ch`)은 그대로이고, 상한과 참 `θ` 사이 틈에 충전 쪽 동역학이 들어간다 — 신품 첫 충전(완전 리튬화 출발)이 그 성분이 가장 큰 조건이다.
  29호 SI 의 "방향 비대칭"(방전 쪽 `η`)에 **셋째 성분(충전 쪽 · 자촉매)** 이 붙는다.
- ★★ **`θ` 판정의 시간 궤적 조건(`[해석]` — 원전 명제를 옮김).** 미반응 무리를 `θ_AM` 으로 셀 때 (i) 셀 안 휴지(연결 유지) — 자촉매 무리는 1/`j₀`(미반응 무리의 Li) 척도로 풀린다(`[재현]` Python FP 이식 · 식 S20 `j₀` · 액체 ≈3–6 분 ·
  시간 ∝ 1/`j₀`) (ii) 문턱 아래 율 또는 율 계열 (iii) 더 깊은 충전(합쳐짐) (iv) 다음 사이클 회복 — 넷 다 `θ` 는 안 움직인다. **급랭(교환 차단)은 가르지 않는다**(S27 21 h — 두 가설 모두 남긴다). 원전은 셀 안 휴지를 재지 않았다.
- ★ **22호 두 상** — 22호 C/10(= 원전 단위 0.065 C) 은 원전 C/15(액체 단봉)와 같은 전류 · 자촉매 설명엔 ASSB `j₀(x≈1)` ≲ 액체 판의 1/30(`[재현]` 규모 논증) · 22호 ex situ(펠릿째 ≈5.1 h)는 암묵적 휴지 → `θ` 쪽
  조건부 근거(측정까지 시간 · 해체 뒤 연결 미인쇄). 무탄소 복합체의 **전자 접촉 옴 자촉매**(원전 Fig. 4d)는 `θ` 와 같은 모양으로 남는 연결된 `η` 형의 넷째 후보다(`[해석]`).
- ⚠ 모집단: 액체 · Li 금속 · 신품 · 셀 수 · XRD 온도 미인쇄 · ASSB `j₀(x)` 0 — 3 항 분해로 옮길 수치는 없고 **조건**만 옮긴다.

## ★★ 2026-09-29 (`assb` 76호 Davis 2021 *ACS Energy Lett.* 6, 2993, **실험 + 2D 해상 모형 · 흑연 \| Li₆PS₅Cl 복합 음극 · Li 금속 반쪽 · 60 °C · 7 MPa · CC-CV 리튬화 · operando 광학 · 양극 아님**) — **`θ` 판정의 시간 궤적 조건에 두 줄이 붙는다: 정전압 유지는 넷째 연산자(구동력 있음 — 휴지와 다르다)이고, 확산 시간이 프로토콜 창보다 길면 연결된 재고도 `θ` 처럼 보인다**

`raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md`. 흑연 40 · 60 · 80 · 100 wt% × 1.87 · 4 mAh cm⁻² · CC-CV(C/16–1C · 정전압은 1/C 시간까지) · 자유 단면 operando 광학(흑연 단계 색 — 범주형) · 셀 안 휴지 0.

- ★★ **`η` 를 가리키는 연산자 넷 — 셀 안 휴지는 0.** ① **정전압 유지** — `[인쇄]` 40 % Gr "At the end of charging, a uniform gold color is observed in the graphite throughout the electrode" · 모형 "fully homogenized at 100% SOC due to the extended CV hold" ② **끝 저율** — `[인쇄]` "permanent capacity loss does not occur during cycling" · `[도표]` 끝 C/16 / 첫 C/16 0.967–0.982 ③ **역방향** — `[도표]` S6 탈리튬 끝 금색 분류 0.00 ④ **다음 사이클** — `[도표]` 같은 율 두 사이클 차 ≤0.011 mAh cm⁻². 넷 다 율 손실이 되돌아온다(`η`)는 쪽이다. ⚠ 정전압 유지는 구동력을 건 채 기다리는 연산자라, 74호 절의 (i) 셀 안 휴지(재분배만)와 같은 칸이 아니다(`[해석]`).
- ★★ **확산 시간 창 — `θ` 와 `η` 가 프로토콜 안에서 안 갈리는 자리.** 80 % Gr 은 `[인쇄]` "nearly the entire electrode acts as one large graphite region" · 1.87 mAh cm⁻² 셀에서 C/16 CC-CV 로도 `[도표]` 이론의 84 %(100 % Gr 76 %) · `[재현]` 두께 방향 τ_D = L²/D(75 µm) ≈20 h(문헌 `D`) – 204 h(모형 `D`) ≫ C/16 16 h(operando 20 h). 연결은 살아 있어도 확산 시간이 창보다 길면 첫 충전에도 방전에도 안 쓰이는 재고 — **`θ` 와 같은 서명**이다. `[해석]` 미반응 재고를 `θ_AM` 으로 세기 전에 τ_D 와 프로토콜 창(율 · 정전압 시간)을 나란히 적는다(보류 (두) 의 근거 — 결정 안 함).
- ★ **`θ` 형 후보가 그림에 있다 — 판별 입력은 없다.** `[도표]` "100 % SOC" 프레임(Fig. 4F = S6A)의 집전체 쪽 위 15 % 띠에서 흑연 분류 픽셀 0.44–0.68 이 어둡고, 0 → 100 → 0 % 내내 색이 그대로인 ≈14 µm 입자 하나 — 본문 "uniform gold" 와 다르다(76호 D6 · 저자 무언급). 고립 흑연(`θ`) · 미완 `η` · 비흑연 이물을 가를 입력(셀 안 휴지 · 다음 사이클 영상 · 성분 분석)이 지면에 없다. 자리는 24호 `θ` 형 모집단과 같은 **집전체 쪽**이다 — 이온 한계 복합체에서 가장 늦은 자리와 안 되는 자리가 겹친다.
- ★ **영역 안 구배는 74호 자촉매와 다른 무늬다.** 흑연 영역은 SE 경계에서 속으로 리튬화된다(가장자리 금색 · 속 파랑/빨강 — 껍질-속) · `[인쇄]` 고체 확산으로 배정 · 모형 `D` 는 문헌의 1/10(근거 0)이라 그 크기가 인자에 걸린다. 74호 입자 간 이봉(같은 거리 입자끼리 다른 상태)과 공간 무늬가 다르다.
- ⚠ 모집단: 흑연 음극 · Li 금속 · 60 °C · 신품 14 사이클 · 조건당 셀 1 · 광학은 범주형 표면(색 → `x` 수치 교정 0) — 3 항 분해로 옮길 수치는 없고 **조건**만 옮긴다.

## ★★ 2026-09-29 (`assb` 77호 Shi 2020 *Adv. Energy Mater.* 10, 1902881, **모형(DEM + 입자 그래프) + 실험 · 신품 · LZO-NMC532 \| 75Li₂S–25P₂S₅ · CNF 5 wt% · In 박 · 첫 사이클 열 셀**) — **정적 `θ` 모형이 첫 방전에 맞고 첫 충전에는 안 맞는다: 충전(5 h CV) ↔ 방전(CC) 비대칭이 λ 에 따라 커지는 몫은 `θ` 칸 밖이다**

`raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md`. 모형 `θ_CAM`(부피 가중 · 이진 · 이온 반쪽 · 정적) × 155 mAh g⁻¹(실험 최대값 닻) ↔ 첫 방전(0.05 mA cm⁻² · `[재현]` C/18.5–C/24.7 · 방전 끝 ≈1.40 V) · 셀 안 휴지 0 · 율 하나 · 다음 사이클 0.

- ★★ **3항으로 쓰면** `Q_dis/155 = θ · η(i) · (Q_material/155)` — 닻 155 는 "가장 좋은 셀의 `η·Q_material`" 이고 모형은 `θ` 한 인자만 계산한다. 대조가 맞는다(RMS 8.4 mAh g⁻¹)는 것은 "θ × 최선 셀의 η·Q" 가 방전과 비슷하다는 것이지 `θ` 칸이 맞았다는 것이 아니다.
- ★★ **`θ` 칸 밖의 몫 넷** — `[도표]` ① CE 가 λ 와 함께 0.74 → 0.50(통째 고립은 CE 를 안 바꾼다) ② CV 가 충전에 더한 몫이 저 θ 셀 +19–22 ↔ 고 θ 셀 +10 mAh g⁻¹(충전에도 느린 몫 — CV 가 일부 거둔다 · 방전엔 CV 없음) ③ 저 θ 셀 방전은 평탄이 없다(3.0 V 위 34 % · 2.0 → 1.4 V 에 10–12 %) ④ 12 µm 쌍은 충전이 같고(186.8 ↔ 186.6) 방전만 13 mAh g⁻¹ 차. `[해석]` 넷 다 `η`(수송 한계) 또는 한 사이클 안의 연결 변화(수축 — 24호 기구) 칸이다 — 가르는 입력은 0.
- ★★ **첫 충전 상한(65호 처방)이 원전 DEM 에 걸린다** — 두 저 λ 셀에서 `Q_ch/Q_ch,ref` 0.71 · 0.64 > 모형 θ 0.56 · 0.48. 치우침: 부반응 충전은 SE 가 작을수록 커질 쪽이라 기준 셀(3 µm)이 더 많이 품는다 — 모순을 약하게 하지 않는 방향. `[해석]` 모형 θ 가 "통째 고립" 이 아니라 "CC 방전에서 느려 못 쓰는 몫" 까지 흉내 내고 있을 수 있다 — 성긴 SE 망은 고립과 느림을 함께 만든다.
- ★ **컷오프가 겉보기를 움직인다** — 인쇄 창 "2–3.7 V versus In" ↔ 그림 방전 끝 ≈1.40 V · 저 θ 셀은 2.0 ↔ 1.4 V 사이에서 방전의 10–12 % 를 낸다(고 θ 셀 1–2 %). `η` 가 큰 셀일수록 컷오프 선택이 "이용률" 에 크게 걸린다.
- ⚠ 모집단: 신품 · 첫 사이클 · 조건당 셀 1 · 오차 0 · 온도 미인쇄 · 두 NMC 공급처 다름 — 3 항 분해로 옮길 수치는 없고 **조건**만 옮긴다(`θ` 판정 전에 충전 CV ↔ 방전 CC 비대칭 · CV 몫 · 컷오프를 적는다 — 보류 (두) 근거).

## ★★ 2026-09-29 (`assb` 78호 Buchberger 2015 *J. Electrochem. Soc.* 162, A2737, **실험 · 액체 풀셀(흑연 \| NMC111 · Swagelok) · 1C/1C 노화 · 사후 XRD · 반쪽 재조립 · PGAA · 2전극 EIS · ASSB 아님**) — **재고(LLI) 몫은 방전 끝 양극 격자로 따로 읽히지만 영점이 규약이고, 나머지(LAM ↔ `η`)는 반쪽 0.1 C 에서도 안 갈린다**

`raw/papers/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance.md`. 조건 셋 × 두 셀 · ≤300 사이클 · 교정은 [[nmc-lattice-li-content-calibration]] 78호 절 · 절차의 대가는 [[reference-electrode-halfcell-dma]] 78호 절.

- ★★ **액체 풀셀에서 이 페이지의 분해는 재고 항 하나가 더 붙는다** — `Q_1C = (재고로 정해지는 창) × η(1 C) × Q_material` 에서 저자는 재고 몫을 격자로 따로 읽었다(`[인쇄]` 표 I ΔC_active-Li). 60 °C 셀은 재고 몫이 손실의 92–94 % · 25 °C 셀 48–49 % · 4.6 V 셀 45–46 %(상한).
- ★★ **영점이 규약이다** — 재고 몫 = 278 × (x_aged − x_ref) 의 x_ref 를 전하로 셌다(0.084 ↔ 0.109 → 7.0 mAh g⁻¹ · 형성 뒤 흑연 저장소 ≈4–5 mAh g⁻¹). 경미 셀에서는 영점 폭이 신호보다 크다 — "재고 몫" 도 `θ` · `η` 처럼 **정의를 달고** 옮긴다(`[해석]`).
- ★★ **나머지 몫 — `η` 와 `Q_material`(LAM) 이 반쪽 0.1 C 에서도 안 갈린다** — 4.6 V NMC 반쪽 0.1 C 방전 86 · 71 ↔ 153 mAh g⁻¹. `[인쇄]` "indicating either a substantial loss of active material or substantially increased impedance" →
  TM 용출(PGAA ≤0.77 mol%)만 지우고 `η`(저항)로 배정. 이 페이지의 "율이 한 항만 지운다" 처방은 **저속 · 정전압 끝 용량이 있어야** 서는데 이 편 율 시험은 0.1 C 가 가장 느리다 — 0.1 C 가 `η → 1` 극한이 아니다(`[해석]`).
- ★ **첫 사이클 결손의 칸** — NMC ICL(0.085)은 방전 끝 확산 지연(`η` 쪽)이고 정전압 30 h 로 격자가 원형까지 돌아온다(`[인쇄]` · 격자 확인) — `Q_material` 결손이 아니다. 풀셀 첫 사이클 결손은 NMC ICL 과 흑연 SEI 의 **큰 쪽**(`[인쇄]`).
- ⚠ 모집단: 액체 · 흑연 음극 · NMC111 · 조건당 두 셀 — ASSB 로 옮길 수치는 없고 **조건**만 옮긴다(재고 몫을 따로 읽을 때 영점 · 방전 끝 한계 전극을 적는다 · "LAM 또는 저항" 을 한 기구 제거로 닫지 않는다).

## ★★ 2026-09-29 (`assb` 79호 Li Z. 2020 *Chem. Mater.* 32, 6358, **실험 · 액체 Li 반쪽 · 두꺼운 NMC811 캐스트 필름 170–172 µm · operando 방사형 깊이 회절 · C/10 CC-CV 한 사이클 · C/3 아홉 · 율당 셀 1 · ASSB 아님**) — **"불활성" 층이 시간 궤적에서 `η` 로 드러난다: 역방향 구동 중 계속 반응 · 여러 주기 드리프트가 `θ` 판정 조건의 두 줄이 되고, 쿨롱 효율 결손이 `η` 저장일 수 있다**

`raw/papers/li2020_synchrotron-operando-depth-profiling-soc-gradients-thick-nmc811.md`. 깊이 SOC 는 자기 교정 ASOC(교정은 [[nmc-lattice-li-content-calibration]] 79호 절) · 깊이 창은 기울기 기하(끝 주사 = 중첩 평균) · 셀 안 휴지 계획 0.

- ★★ **3 항으로 쓰면** 두꺼운 전극의 겉보기 용량 부족은 `η(i, z)` 가 거의 전부다 — C/3 방전은 명목의 21–27 %(`[인쇄]` 표 S2)인데 뒤층까지 연결돼 있고(아래), 깊이 방향 구배(앞 0.8 ↔ 뒤 0.2)가 주기마다 되풀이된다. `θ` · `Q_material` 칸의 몫은 이 편에서 드러나지 않는다(`[해석]` — 사이클 · 열화 0).
- ★★ **"불활성" 이름표의 반례** — `[인쇄]` 충전 중간 뒤층 "no longer electrochemically active" → 방전 전환 뒤 "continues to increase its state of charge to up to two additional hours" · C/3 뒤층 "generally insensitive to the changing potential" → 18 h(인쇄)에 +0.45. `[도표]` −191 +0.20(≤2 h) · 2.8 V 유지 중 뒤층 방전 최고 속도(−0.09 … −0.15 h⁻¹) · −154 +0.46 / 16 h(포화 없음) · C/3 주기 최대 시각의 깊이 지연 0–0.5 h. ⇒ 74호 절 조건 목록에 **(v) 역방향 구동 중 계속 반응**(연결의 양성 서명 — 고립이면 불가 · 24호 40 % 셀에 이은 둘째 표본)과 **(vi) 여러 주기 드리프트**(76호 "τ_D ↔ 창" 의 액체 표본)를 붙일 근거(보류 (두) — 결정 안 함). 셀 안 휴지(i)는 계획 0 · 계획 밖 ≈0.3 h 한 번(Fig. 4c — 구배 ≈0.05 일 때 · 정보 없음).
- ★★ **쿨롱 효율 결손 ↔ `η` 저장** — `[재현]` C/3 아홉 사이클 알짜 과잉 103.4 mAh g⁻¹ · 첫 여덟 95.3 ↔ 셀 평균 ASOC 드리프트 +0.39 가 한 척도(1 ASOC ≈246 mAh g⁻¹)로 맞는다 — "과잉 전하 = 부반응" 이 아니라 뒤층 SOC 저장(저자 판정 · 실질은 드리프트 ↔ 진폭 비). 3 항 분해 밖에서 CE 로 LLI 를 세는 회계가 `η` 저장을 재고 손실로 넣는 자리(`[해석]` — 보류 (브)).
- ★ **평균 순서가 `η(z)` 값을 바꾼다** — 두 상 조각에서 격자를 먼저 평균하면 비선형 `V(x)` 때문에 SOC 가 0.2 치우치고 역전 구간의 흐름 부호가 바뀐다(79호 D16) — 깊이 분해 관측을 `η(z)` 로 옮길 때 평균 순서를 적는다.
- ⚠ 모집단: 액체 · Li 금속 반쪽 · 신품 · 율당 셀 1 · 0.68 mm 분리막 · 2전극 — 3 항 분해로 옮길 수치는 없고 **조건**만 옮긴다.

## ★★ 2026-09-29 (`assb` 80호 Okasinski 2020 *PCCP* 22, 21977, **실험 + 모형 · 액체 NCM523/흑연 CR2032 코인셀 여덟 구성 · in situ EDXRD 프로필로메트리(측면 × 깊이) · 형성 뒤 한 번 충전 → 휴지 · 구성당 셀 1 · ASSB 아님**) — **셀 안 휴지의 첫 직접 표본 — 그러나 흑연(다상)에서는 휴지 지속이 `θ` 의 서명이 아니다: 휴지 연산자에 재료 조건이 붙고, `η` 에 측면 축 `η(r)` 이 더해진다**

`raw/papers/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients.md`. 측면 윤곽은 흑연 상 분율(LiC₆ · LiC₁₂ — 교정 불필요) · 양극 x̌ 는 NCM523 `a` 시그모이드(교정은 [[nmc-lattice-li-content-calibration]] 80호 절) · 압축 불균일은 [[assb-stack-pressure-operating-window]] 80호 절.

- ★★★ **휴지 연산자의 재료 조건** — `[인쇄]` "the cells were charged under various conditions and allowed to rest" · "This non-uniformity persisted even after the cells were at rest for several hours" · 방법 절 "in multiphase materials such as lithiated graphite, Li⁺ ion gradients persist almost indefinitely as phase boundaries serve as barriers to the Li⁺ ion diffusion" · 양극 "varies little even in these edge regions …, suggesting smoothing of lithium concentration gradients in the absence of current". ⇒ 74호 절 조건 목록의 **(i) 셀 안 휴지** 줄에 붙일 조건: **휴지 뒤 지속은 고용체 창에서만 `θ` 쪽 근거 · 다상 평탄 창(흑연 LiC₁₂/LiC₆ · In/InLi · NCM811 H2/H3 구간)에서는 근거가 아니다**(`[해석]` — 원전 인쇄를 옮김 · 보류 (두) — 결정 안 함). 74 · 76 · 77 · 78 · 79호 다섯 편이 비워 둔 휴지 칸을 이 편이 처음 채우되, 채운 자리가 다상 재료라 `θ` 판정력이 없다. 휴지 길이 · 측정 시각 · 주사 순서 · 휴지 전 양극 지도는 미인쇄다.
- ★★ **측면 축 `η(r)`** — 이 페이지의 `η(i)` 는 지금까지 깊이(`η(z)`) · 입자 척도였다. 80호: 흑연 가장자리 ≈2 mm 띠(`[재현]` 면적 50 %)가 ≈0.95C 충전에서 `[도표]` Δu₀ 0.08–0.11(셀 1) · 0.27–0.30(셀 2) 늦다 — LiC₁₂ 까지 반응한 연결 영역(`θ` 형 영역 0)이고, 저자 기구는 "a greater resistivity near the electrode edge"(분리막 압축 — 저항 측정 0 · 모형 Ξ 0.75 가정). 측면 균일 모형으로 겉보기 용량을 적합하면 이 몫이 `θ_AM` 이나 `ε_p` 자리로 샌다 — `[재현]` 면적 평균이 중앙보다 절대 x 로 5–8 % 낮다(0.611 ↔ 0.644 · 0.779 ↔ 0.847 · 보류 (러) 경고 쪽).
- ★ **느린 율 한 프레임** — 셀 8(C/12.3 · x 1.0)의 ESI S4 포스터(y = −7 mm)에서도 가장 바깥은 Cu 쪽 LiC₁₂ 우세(`[도표]` ≈12 ↔ LiC₆ ≈5) — 율 연산자로 지워지지 않는 가장자리 몫의 후보다(대면 결손 · 고립 · 큰 저항 중 무엇인지 지면으로 못 가른다 · 한 프레임 · 가운데 미확인).
- ⚠ 모집단: 액체 · 흑연 ‖ NCM523 풀셀 · 신품 · 구성당 셀 1 · 형성 뒤 한 번 충전 · 역방향 · 다음 사이클 0 — 수치는 옮기지 않고 **조건**(휴지의 재료 조건 · 측면 축)만 옮긴다.

## ★★ 2026-09-29 (`assb` 82호 Schlautmann 2023 *Adv. Energy Mater.* 13, 2302309, **실험 + 모형 · 신품 · 시판 Li₆PS₅Cl 네 입도 × NCM811 70 : 30 · 무탄소 · In/LiIn 반쪽 셀 50 MPa · 셀 셋 · 차단 대칭 셀 + GeoDict**) — **C/20 결손은 수송 옴 강하 밖에 있고, 율 되돌림이 1C 결손(`η`)과 C/20 결손(`θ` 형 · `A_eff` · 첫 사이클 손실 후보)을 가른다 — 그러나 C/20 결손의 배분은 갈리지 않는다**

`raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md`. 수송 측정 · 규약은 [[assb-tortuosity-factor-effective-conductivity-split]] 열두 번째 표본 · 입도 대표값과 λ 는 [[composite-cathode-percolation-utilization]] 82호 절.

- ★★★ **크기 검사 — 옴 강하로는 안 된다** `[재현]`(가정 두께 55–62 µm · 측정 AC σ_eff): C/20 이온 IR **2.3–4.2 mV** ↔ C/20 결손 S − XL 30(6b) · 46 mAh g⁻¹(본문 — S = 셀 하나) · 1C 이온 + 전자 IR 차 XL − S **≤ +28 mV** ↔ `[도표]` Fig. 4b 같은 용량 전압 간격 **0.33 V(25 mAh g⁻¹) → 0.92 V(47)**. ⇒ `η(i)` 의 옴 몫은 작고, 남는 `η`(반응 분포 · 입자 안 확산)와 면적 × `j₀` 가 이 편 자료로 갈리지 않는다.
- ★★ **율 되돌림 연산자** — Fig. 4d 1C 뒤 C/20: S ≈180 → 189 · M ≈162 · L 154 → 151 · XL 144 → 140 — 1C 결손은 돌아온다(`η`) · C/20 의 S ↔ XL 차(≈30–45)는 남는다 → `θ` 형 · `A_eff` · 첫 사이클 손실 후보(74호 절 조건 목록의 "문턱 아래 율 · 다음 사이클 회복" 표본 · 셀 안 휴지 0).
- ★★ **첫 충전 상한** `[재현]` — XL/S 첫 충전 비 0.83(본문) · 0.92(S 셋 평균) ↔ 첫 방전 비 0.77 · 0.85 → 통째 고립 몫 상한 8–17 % · 방전 결손 중 6–7 %p 는 충전 뒤에 생김 · 첫 CE ≈80 → 74 %(SE 입도를 따름 — 같은 NCM811). 25 · 65 · 77호 절과 같은 모양.
- ★ **50 사이클 dip** — N1 → 최소 −4.7 → −13.9 %(S → XL) · 최소 8–10 → 27 사이클 · 저자 배정 분해 계면층[21](측정 0) — `[해석]` 모형 면적이 가장 큰 S 의 dip 이 가장 작아 "계면층 ∝ 면적" 과 긴장.
- ⚠ 모집단: 신품 · 50 MPa 한 점 · 반쪽 셀 2전극 · 대표값 규약(본문 S = 셀 하나 ± 셋 SD — 82호 D1) · 대칭 셀(455–516 µm) ↔ 반쪽 셀(55–62 µm) 두께 ×8.3 — 수치는 옮기지 않고 **검사 순서**(옴 강하 크기 → 율 되돌림 → 첫 충전 상한)만 옮긴다.

## ★★ 2026-09-29 (`assb` 85호 Wang Y. · Li X. 2024 *Adv. Mater.* 36, 2309306, **실험 · 신품 EIS + 4000 사이클 · 단결정 NMC83 \| LPSCl1.5 세 판 \| Si–G\|Li · Si–Cl\|G\|Li 완전지 · 50 MPa · RT 22–30 °C · 셀 하나씩**) — **SE 입도 판 사이의 차는 0.3 C 에서 ≤10 % 이고 4 C 에서 −35 … −65 % 다 — 정적 몫은 작고 `η(i)` 가 크며, 4000 사이클 감쇠(−20 … −26 %)의 배분은 0 이다**

`raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md`. 수송 · 굴곡도 이름표는 [[assb-tortuosity-factor-effective-conductivity-split]] 열세 번째 표본 · 퍼콜 문턱 · λ 는 [[composite-cathode-percolation-utilization]] 85호 절.

- ★★ **율 축** `[도표]`(그림 2a · Si–G 음극 · 25 °C): 0.3 C mixed 165 · large 150 · small 152 → 4 C 116 · 75 · 55 mAh g⁻¹ — 정적 차 ≤10 % · 율 차 −35 … −53 %(mixed 기준) → `η` 가 지배 · 저자 이름표는 large = "접촉 부족" · small = "굴곡도"(둘 다 신품 EIS 호 순서 위).
- ★★ **율 되돌림 연산자**(S4 `[도표]`): 4 C 방전 ≈143 → 뒤따르는 0.3 C 꼬리 ≈5–10 → 합 ≈150(충전 컷오프 150 고정) — 4 C 결손은 돌아온다(`η`) · 셀 안 휴지 0 · 다음 사이클 0.
- ★ **온도 축**(그림 2h · 0.3 C · Si–Cl): 25 → −5 °C 에서 mixed/Si–Cl 171 → 86 · large 138 → 48 · small 146 → 43 — 저온에서 판 차가 벌어짐(`η(T)`) · 저자 배정 없음.
- ★ **첫 충전 상한** `[도표]`: 그림 2b 0.3 C 충전 ≈205 ↔ 방전 ≈165(사이클 번호 미인쇄 · Si–G\|Li 음극의 SEI · Si 몫 미분리) — 재료가 아니다.
- ★ **사이클 축**: 18 · 23 · 27 mg cm⁻² 셀 4275 · 2504 · 4200 사이클 `[도표]` −20 … −26 %(수치 인쇄 0) · CE ≈1.00(±1 % 눈금) · 사이클 중 EIS 0 · 사후 양극 0 → `θ` · `LAM_PE` · `η` · Li 재고 몫 0. `[재현·외부 밀도]` Li 박 15 µm ≈3.1 mAh cm⁻²(양극 ×1.14) — 감쇠 0.6 mAh cm⁻² 가 전부 LLI 라면 평균 CE 99.994 %.
- ⚠ 모집단: 셀 하나씩 · 비교군이 다른 음극 위(2a Si–G ↔ 2g · 2h Si–Cl) · 면적 미인쇄 — 수치는 옮기지 않고 **검사 순서**(저율 차 → 율 되돌림 → 온도 축)만 옮긴다.

## ★★ 2026-09-29 (`assb` 86호 Kim J.T. … 2023 *J. Mater. Chem. A* 11, 20549, **실험 · NCM523(LPSCl 코팅 ↔ bare) \| Li₆PS₅Cl \| Li₀.₅In 분말 · 2032 코인 무외압 · 0.1C 100 사이클 · 30 °C · EIS 1 · 50 · 100(충전 상태) · GITT 2 h 휴지 · 셀 하나씩**) — **Li 재고 셀(×2.7)에서 bare 의 −31 % 는 LLI 로 닫히지 않고, 충전 상태 저항 증가(+102 mV at 0.1C)로도 닫히지 않는다 — 남는 것은 정적 몫(`θ` · `LAM_PE`) 또는 방전 끝 저항(미측정)이고, 코팅 쌍의 첫 충전 등가는 신품 정적 차 ≈0 을 준다**

`raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md`.

- **3 항 분해 자리**: `η(i)` — 율 0.1 → 1C 에서 LP2 −33 % · bare −64 %(`[도표]` 그림 4c) · 되돌림 LP2 99 % · bare 91 % → **bare 의 미회복 9 % 는 정적**(20 사이클) · `θ` / `LAM_PE` — 첫 충전 등가(`[재현]` 202.1 ↔ 201.9 mAh g⁻¹) → 코팅 쌍의 신품 정적 차 ≈0 · 사이클 축 정적 몫(−31 % 의 대부분)은 `θ` ↔ `LAM_PE` 미분리 · 재고 — `[재현]` Li₀.₅In 11.3 mAh ≫ 첫 충전 4.24 → LLI 밖.
- **IR 예산** `[재현]`: bare ΔR(1 → 100 · 충전 상태 · S12) +269 Ω → 0.1C(0.378 mA) +102 mV · LP2 +63 Ω → +24 mV — 그림 4a 곡선(≈3.0 V 평탄 → 급락)에서 0.1 V 는 수 mAh g⁻¹ · 그러나 GITT 꼬리(ΔV ≈0.95 V · 0.5C)가 방전 끝 저항이 크다는 것을 보여 방전 끝 `η` 몫은 열려 있다(사이클 뒤 방전 끝 EIS 0).
- **CE 결손 ≠ 용량 손실**: bare CE `[도표]` 2–10 사이클 93 → 99 % — 누적 결손(≈25–30 mAh g⁻¹)이 같은 구간 용량 손실(≈6)보다 크다 → 기생 산화 전하(64호 방향 · SE 산화)로 읽히는 재고 셀의 특성 · 코팅 셀은 2 사이클부터 ≈99.5 %.
- **시간 궤적 조건(두)**: 율 되돌림 ✓ · 셀 안 휴지 = GITT 2 h(QOCV 포락선 — 같은 용량에서 가팔라지는가 라는 `θ` 검사의 원자료인데 ΔV 만 그렸다) · 다음 사이클 ✓(100) · 역방향 0.
- 이 편이 안 준 것: 방전 끝 EIS · 사후 양극 정량(공극 분율 · 격자) · `θ` ↔ `LAM_PE` 를 가를 채널 · 셀 수.

## ★ 2026-09-29 (`assb` 87호 Minnmann · Strauss · … · Janek 2022 *Adv. Energy Mater.* 12, 2201425, **종설(Perspective) · 1차 측정 0 · 이 편 계산: 식 (1) ↔ 그림 4**) — **입도 상한 식 `L ≤ √(3D̃/C-rate)` 는 `η(i)` 항(율을 낮추면 돌아오는 몫)의 크기 창이고, 이 편은 접촉 손실 · 균열을 이 경로("longer transport pathways and lower capacities")로 적는다 — `θ`(정적)와 구별되는 쪽**

`raw/papers/minnmann2022_designing-cathodes-cam-ssb-perspective.md`.

- ★★ **식 (1)** `[인쇄]` `L ≤ √(3D̃_Li/C-rate)` · "C-rate (in units of h⁻¹)" · 기준 "at least 83% of the theoretical specific capacity of a spherical CAM particle"[69] — `[재현]` **C-rate ÷ 3600 s** 로만 그림 4 선이 재현된다(0.1 · 1 C 여덟 점 ≤2 % · 5 C 1–4 % — h⁻¹ 그대로면 ×60 · 87호 D6).
- ★★ **크기 창** `[재현]`(그림 4 `[도표·화소]` D̃ 띠 × 식 (1)): NCM(이온 D̃ 4.46×10⁻¹³–1.05×10⁻¹¹ cm² s⁻¹ [7]) — 0.1 C 2.2–10.6 · 1 C 0.69–3.4 · 5 C 0.31–1.5 µm / LFP(전자 D̃ [71]) — 0.1 C 1.2–4.6 · 5 C 0.17–0.65 µm. 이 창을 넘는 입자는 그 율에서 "83 %" 기준 아래 — 율을 낮추면 돌아오는 몫(`η`).
- ★ **기준 "83 %"** — [69] 위임(미열람) · 우리 구 확산 산술(정전류 · 표면 포화 · 점근식 `Δc_s = (JR/D)(3Dt/R² + 1/5)`, `[재현·가정]`): L = 지름이면 **95 %** · L = 반지름이면 **80 %** — 미폐합.
- ★ **배정 문장** `[인쇄]` §4.1 "This can lead to contact loss between CAM and SE or cracking of secondary CAM particles, which ultimately results in longer transport pathways and lower capacities (see Equation (1)).[86,91]" — 접촉 손실 · 균열 → 확산 길이 ↑ → 율 의존 용량 ↓ = `η(i)` 쪽 서술 · 같은 편 §2.2 SE 기지 균열 → "capacity fading due to loss of contact to CAM upon prolonged cycling" 은 기구 없이 용량에 배정 — **두 배정이 한 지면에** 있고 가르는 기준(율 되돌림 · 휴지)은 0.
- ★ **첫 사이클 결손** `[인쇄]` "In LIBs, the capacity lost in the first cycle, linked to the kinetic limitations of the CAM at the end of discharge, is effectively used for the formation of the SEI"(인용 0) — 한 문장에 두 배정(CAM 동역학 `η` · SEI 재고).
- ⚠ 모집단: 종설 — 수치는 식 · 인용 값 · 우리 산술이다. 옮기는 것은 **"율 의존 크기 창은 식 (1) 의 단위 · 기준을 재현한 뒤에"** 라는 검사 순서다. 재수록 그림 7a([86]) 율 되돌림(P/LPSX −13 % 미회복 `[도표]`)은 판정 입력이 아니다.



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
- ★ **2026-09-28 (65호)**: **첫 충전 상한을 `θ_AM` 의 측정으로 쓰지 않는다** — 공정 대조군 사이의 상한이고, 판독 ±1 mAh g⁻¹ · 셀 하나씩 위다. D85H 는 두 충전 곡선이 겹쳐 판정 밖이다.
- ★ **2026-09-28 (66호)**: **22호 `η` 값이 틀렸다고 하지 않는다** — 교정 규약에 따라 ≈±0.1 움직일 수 있다는 것까지이고, 어느 교정이 참 Li 함량에 맞는지는 화학 분석 0 이라 모른다.
- ★ **2026-09-28 (67호)**: **Fig. 1a 감쇠의 `η` 몫을 정량했다고 하지 않는다** — 저자 문장이고 양은 0 이다(정전압 없는 반쪽 · C/2). 규약 항 0.10 은 NCM811 쌍의 `[재현]` 이다.
- ★ **2026-09-28 (74호)**: **충전 쪽 자촉매 성분의 크기를 ASSB `η` 로 옮기지 않는다** — 액체 · 판 입자 · 2.24C 의 미반응 넓이(42.6 %)와 Source Data 과잉(+0.235)은 조건 논거의 근거이지 ASSB 값이 아니다. 22호 암묵적 휴지 논증과 옴 자촉매 후보는 조건부 `[해석]` 이다.
- ★ **2026-09-29 (76호)**: **80 · 100 % Gr 의 미이용 16–24 % 를 `θ` 로도 `η` 로도 확정하지 않는다** — 모형 배정(고체 확산)과 `[재현]` τ_D 범위(모형 · 문헌 `D`)가 `η` 쪽을 가리킬 뿐, 정전압 끝 상태 그림 · 셀 안 휴지가 없다. 흑연 음극 편이라 양극 `θ_AM` 수치로 옮기지 않는다.
- ★ **2026-09-29 (77호)**: **충 ↔ 방 비대칭 · CV 몫을 `η` 로도 동적 `θ` 로도 확정하지 않는다** — 셀 안 휴지 · 율 · 다음 사이클이 지면에 없다. 첫 충전 상한 위반 둘도 조건당 셀 1 · 기준 셀 하나 위의 검사다.
- ★ **2026-09-29 (78호)**: **액체 풀셀의 재고 몫(ΔC_active-Li)을 이 페이지 3 항의 어느 칸 값으로도 옮기지 않는다** — 영점(0.084 ↔ 0.109 · 형성 저장소)이 규약이고 4.6 V 셀은 분극 한계라 상한이다. 4.6 V NMC 반쪽 저하를 `η` 로도 `Q_material` 로도 확정하지 않는다.
- ★ **2026-09-29 (79호)**: **"불활성" 층의 `η` 판정을 ASSB 로 옮기지 않는다** — 액체 · 전해액 농도 기구(저자 정성)의 표본이고, 옮기는 것은 연산자(역방향 계속 반응 · 여러 주기 드리프트)다. 과잉 충전 전하가 전부 `η` 저장이라고도 하지 않는다(드리프트 ↔ 진폭 비 `[재현]` 까지 · 1C 알짜 미기재).
- ★ **2026-09-29 (80호)**: **흑연 휴지 지속을 `θ` 로 읽지 않고, 양극 평탄을 연결의 증명으로도 쓰지 않는다** — 휴지 전 양극 지도 · 휴지 길이 · 측정 시각이 미인쇄다. 측면 `η(r)` 의 원인(분리막 압축)도 저자 배정이다(대안 하나만 수치 배제 · 원인 크기 Ξ 는 가정).
- ★ **2026-09-29 (82호)**: **82호 C/20 결손을 `θ` 로 배정하지 않는다** — 옴 강하 밖이라는 것과 첫 충전 상한까지이고, `A_eff` · 첫 사이클 손실과 가르는 입력(사이클 중 EIS · 사후 단면 · BET)이 없다. 두께는 밀도 · void 가정 위의 `[재현]` 이다.
- ★ **2026-09-29 (85호)**: **85호 4 C 결손을 굴곡도로 배정하지 않는다** — `η(i)` 라는 것까지이고, 그 `η` 가 수송(R1 · R2)인지 계면(R3)인지는 면적 없는 신품 EIS 로 갈리지 않는다.
- ★ **2026-09-29 (86호)**: **86호 bare 감쇠를 정적 몫으로 확정하지 않는다** — 충전 상태 저항으로 설명되지 않는다는 것까지이고, 방전 끝 저항은 미측정이다(GITT 꼬리 ≈0.95 V). CE 결손을 기생 전하로 확정하지도 않는다 — 재고 셀에서 용량에 안 찍힌다는 산술까지다.
- ★ **2026-09-29 (87호)**: **식 (1) 의 크기 창을 우리 셀의 `η` 몫으로 옮기지 않는다** — D̃ 띠는 그림 판독(인용 [7] · [71])이고 "83 %" 기준은 원전([69]) 미열람이며, 80 / 95 % 는 우리가 고른 기준(정전류 · 표면 포화)의 산술이다.

## 관련
- [[nmc-lattice-li-content-calibration]] — 22호 `η` 가 기대는 격자 ↔ `x` 교정 곡선의 축 규약 · 단조 채널 · 이송 오차(66호).
- [[assb-interphase-vs-contact-loss-attribution]] — 계면층 ↔ 접촉 손실(둘 다 `θ`·`η` 에 들어간다)의 분리. 23호 손실 예산의 근거.
- [[assb-tortuosity-factor-effective-conductivity-split]] — `η(z)` 를 정하는 수송 곱 `σ_bulk·ε/τ²`; 부분 접촉 손실이 `τ²` 로 들어가는 자리(24호).
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
