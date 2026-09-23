---
title: 복합양극 퍼콜레이션 이용률 (utilization level)
description: "Bielefeld 2019 utilization level θ = V_c/V_ν as the geometric surrogate for ASSB composite-cathode contact loss, its units, closed forms, and its own irreducible width"
created: 2026-09-16
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, dem-mpm, research]
sources: [raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md, raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/rahman2024_sbms-rul-solid-state-batteries.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
---

# 복합양극 퍼콜레이션 이용률 (utilization level)

> `assb` 축의 첫 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 수치의 정본은 원문 PDF 이고, 이 페이지의 값은 **사본**이다 — 인용 근거로 쓰지 않는다.
>
> **2026-09-16 갱신 (`assb` 3호 Liu 2024)**: 3호의 "contact loss" 는 **이 `θ` 와 같은
> 양이 아니고 변환도 안 된다** (§"3호는 이 `θ` 와 변환되지 않는다"). 대신 **`θ` 를
> 떨어뜨릴 구동력**과 그것이 **(양극 × 전해질) 쌍의 함수**라는 것을 준다.
>
> **2026-09-16 갱신 (`assb` 2호 Clausnitzer 2023)**: ① 이 `θ` 와 **정확히 같은 양**이
> 두 번째 논문에 다른 이름으로 있다 (§"두 논문의 좌표 대조"). ② 그러나 이 페이지가 세운
> 곱셈 `Q_apparent = θ_AM · Q_material` 은 **충분하지 않다** — 항이 하나 더 있고
> 그것은 [[assb-apparent-capacity-decomposition]] 에 있다.
>
> **2026-09-16 갱신 (`assb` 4호 Shi 2020 — 첫 실험 논문)**: ★ **이 양의 실측 대응물이
> 처음 들어왔다. 그리고 곱셈 형태를 6 배로 배반한다** (§"4호는 실측을 줬는데 …").

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

## ★ 3호(Liu 2024)는 이 `θ` 와 **변환되지 않는다** (2026-09-16 추가)

`assb` 3호(`raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md`)
도 "contact loss" 를 말하지만 **다른 양을 잰다**. 변환이 안 되는 이유 셋:

| | 1호·2호 | **3호 (Liu 2024)** |
|---|---|---|
| 길이척도 | **전극** (두께 20–140 / 50 µm, 수천 입자) | **이차입자 1 개**(2–12 µm)가 균질 전해질 블록에 박힘 (`[도표]` Fig. S1) |
| 접촉 손실의 좌표 | `θ` / `Connectivity` — **무차원 분율** | **계면 최대주응력** — **GPa** |
| 파괴·디본딩 | 없음 | **없음** (`[인쇄]` "does not explicitly account for mechanical fracture") |

1. **분모가 없다.** `θ` 는 분율이라 "전체 활물질" 분모가 필요한데 3호의 RVE 는 입자
   **1 개**이고 `[인쇄]` "assumed to be connected to the current collector **via the carbon
   binder**" — 즉 **`θ_AM ≡ 1` 인 세계**다.
2. **차원이 다르다.** 응력(Pa) → 분리 분율(무차원)에는 **파괴 판정 규칙**(임계 응력·
   에너지 방출률·계면 인성)이 필요한데 3호에 없다. 논문 스스로 cohesive zone /
   phase-field damage 를 **앞으로 넣을 것**으로 나열한다.
3. **경계조건이 반대다.** 1·2호는 SE 를 **이온 전도 매질**로만 보고 역학이 없다.
   3호는 SE 를 **역학 매질**로만 본다 — `[인쇄]` "Li-ion transport inside the solid
   electrolyte is **not considered explicitly**". **두 모델은 서로의 영점에서 작동한다.**

★ `[해석]` 그래서 3호의 기여는 `θ` 가 아니라 **`θ` 를 떨어뜨릴 구동력**과, 그 구동력이
**무엇의 함수인가**다:

> **`θ` 는 양극만의 성질이 아니다.** `[도표]` Fig. 4f·7c: 같은 양극·같은 운전조건에서
> 전해질 Young 률을 **1 → 30 → 150 GPa** (폴리머 → 황화물 → 산화물)로 바꾸면 계면
> 최대주응력이 **0.05 → 0.28 → 0.38 GPa (리튬화) / 0.55 GPa (탈리튬)**, 벌크 응력은
> **+0.75 → −0.2 → −1.5 GPa** 로 부호까지 뒤집힌다. 율(0.25C–5C)에 따른 산포는 그에 비해
> **작다** — `[인쇄]` "the reduction of the discharge rate is **not a solution**".

→ 이 페이지의 닫힌 형태(식 8, `A_spec` 멱법칙)에는 **SE 물성이 하나도 없다.**
`θ` 를 열화 축으로 쓰려면 **(양극 × 전해질) 쌍마다 다시 재야 한다.**

## ★★ 4호(Shi 2020)는 실측을 줬는데, 그 실측이 이 곱셈을 배반한다 (2026-09-16 추가)

`assb` 4호(`raw/papers/shi2020_mechanical-degradation-assb-cathode.md`)는 이 계보
**첫 실험 논문**이다 (FIB-SEM 토모그래피, NMC532+LZO / 비정질 LPS / CNF / In 음극).
접촉 손실을 **무차원 분율**로 준다 — 3호의 응력(GPa)과 달리 **차원은 맞다**.
그러나 **같은 양은 아니고, 그 사상이 미정이다**:

| | **1호·2호 (`θ` / Connectivity)** | **4호 (Shi 2020)** |
|---|---|---|
| 차원 | **부피** 분율 (클러스터 AM 부피 / AM 전체 부피) | **면적** 분율 (`A(NMC ∩ void) / A(NMC 전체)`) |
| 판정 | **Hoshen–Kopelman 퍼콜레이션** — 집전체/분리막까지 **경로**가 잇는가 | **국소 인접만** — 이 픽셀이 void 에 닿았는가. `percolat*` **0 회** |
| 분모 | AM 전체 부피 | NMC 전체 **표면적**. ⚠ **NMC–NMC 접촉도 "with contact"** 로 센다 (Li⁺ 경로가 아닌데) — 과소평가 방향 |
| 출처 | 계산 (합성 미시구조) | **실측** (FIB-SEM 50 nm 슬라이스 + Weka ML 4상 분할) |
| **시간축** | **없다** | **★ 있다 — 사이클 0 / 10 / 50** |

`[인쇄]` 4호의 값: **접촉 손실 면적 10.4 %** (50 사이클) ·
void 부피분율 **2.87 → 3.23 → 9.50 vol%** (0 / 10 / 50 사이클).

### ★★ 6 배 간극 — 면적 분율을 `θ_AM` 자리에 선형으로 넣으면 안 된다

4호는 같은 셀 계열에서 **300 MPa 재가압으로 용량을 되돌린다**:
`[인쇄]` 129 → (50 사이클) `[도표]` ≈2 → (재가압) **80 mAh g⁻¹**.
`[재현]` **되돌아온 몫 ≈60.5 %p**.

> 곱셈 `Q_apparent = θ_AM · Q_material` 에 면적 분율을 그대로 넣으면
> `θ_AM = 0.896` → 용량 손실 **10 %** 여야 한다. 실제 가역분은 **60 %p** 다.
> **≈6 배.** (원문은 두 수를 나란히 놓고도 **한 번도 비교하지 않는다** — 4호 digest D9.)

`[해석]` 가능한 설명 셋, **논문은 어느 것도 검증하지 않는다**:
1. **면적 → 부피 사상이 비선형(문턱)이다.** 4호 자신이 근거를 준다 —
   `[인쇄]` 접촉 손실이 입자 **한쪽에 몰리면** "all the Li ions … have a **much
   larger distance to travel**", 균일 분산이었다면 "diffusion gradients … would
   **rapidly fade out**". → **같은 면적이라도 분포에 따라 용량 영향이 다르다.**
2. **라벨과 관측이 다른 셀에서 왔다** (4호 digest D10 — 토모그래피 3 셀의 용량이
   **한 번도 보고되지 않는다**).
3. **회복분이 양극이 아니다** — `[도표]` 회복은 음극 쪽 `R_LF` 에서 65 %,
   양극 쪽 `R_MF` 에서 **23 %** 다 ([[assb-pressure-reapplication-separation-test]]).

★ **이것은 DEM 라벨 계획에 직접 걸린다**: DEM 이 싸게 주는 것도 대개 **접촉 수·
접촉 면적**이지 퍼콜레이션 부피분율이 아니다. **두 양 사이의 사상을 우리가 만들어야
한다** — 그리고 4호가 그 사상이 **선형이 아님**을 실측으로 보여 줬다.

### 그리고 이 실측 라벨에도 폭이 없다

- `error bar` · `standard deviation` · `uncertain*` · `replicate` · `seed`
  **전부 0 회** (본문+ESI). 조건당 **셀 1 개 · 구조 1 개**. → `assb` **4/4 편 연속.**
- **분할 정확도 수치가 없다.** ESI 가 Fig. S3 을 "showing the accuracy" 라 부르지만
  혼동행렬·검증셋·정확도 %가 없고, `[도표]` Fig. S2 에서 **CNF 와 LPS 회색도가 크게
  겹친다.** ESI 스스로 `[인쇄]` 오분류가 "especially within the **boundaries**" 에서
  난다고 적는다 — **접촉 손실은 정확히 그 경계에서 재는 양이다.**
- **해상도 바닥이 미명시**(슬라이스 50 nm·"sub-100 nm" 만, 면내 화소 없음)이고
  논문 스스로 `[인쇄]` "very small microfractures … **undetectable by the
  tomography**" 라 적는다 → **10.4 %·9.50 % 는 바닥 없는 하한이다.**

### ✅ 그래도 시간축이 처음 들어왔다 — 그런데 부드럽지 않다

`[인쇄]` 4호 결론: "mechanical degradation **does not progress gradually** …
the majority of the void formation and contact loss **likely occurs at later cycles
and over a short period**." `[도표]` void 2.87 → 3.23(10 사이클, +0.36) →
9.50(50 사이클, +6.27).

`[해석]` → **`θ_AM(N)` 을 부드러운 감소 함수(지수·멱)로 매개화하면 원리적으로 못
맞춘다. 문턱/계단이 필요하다.**
⚠ 단 이 결론은 위 "해상도 바닥" 과 충돌한다 — 초기 미세균열이 **안 보인 것**이라면
"후기에 몰린다" 는 **관측의 성질**일 수 있다 (4호 digest D12).
**우리가 싸게 공급할 수 있는 자리**: 검출 한계를 넣은 전방 모형으로 계단이 실재인지
아티팩트인지 가르기.

## 두 논문의 좌표 대조 (2026-09-16 추가)

Clausnitzer et al. 2023
(`raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md`, §7)
은 같은 양들을 **다른 이름과 다른 기준**으로 쓴다. 변환표:

| 개념 | Bielefeld 2019 | Clausnitzer 2023 | 변환 |
|---|---|---|---|
| 조성 (고상 기준) | `g^S_AM` | **`SVF_CAM`** (식 3) | **동일** |
| 조성 (전체 부피 기준) | `g^V_AM` | (안 씀) | `g^V = SVF × ρ_S` |
| 공극 | `φ` (공극률) | **`ρ_S`** (density after sintering) | **`ρ_S = 1 − φ`** |
| **이용률 / 연결성** | **`θ = V_c/V_ν`** (식 6) | **`Connectivity = 1 − n_iso/n_tot`** (식 4) | **동일** |
| 활성 계면적 | `A_spec,a` [m²/m³] | `A_act/V_ca` [1/cm] | **`1 m²/m³ = 10⁻² 1/cm`** |
| 굴곡도 | (없음) | `τ` (식 6) | — |
| 유효 전도도 | **(한 번도 계산 안 함)** | `σ_eff` [S/cm] (식 5) | — |

`θ ≡ Connectivity` 인 근거: 두 정의 모두 분모가 **그 상의 전체 부피**, 분자가
**경계면에 연결된 부분**이고, 경계면이 서로 같다 — 전자는 **집전체**, 이온은 **분리막**
(Clausnitzer `[인쇄]` "isolated SE clusters … not connected to the separator" ·
"isolated active material particles are not connected to the cathode current collector").
균일 복셀에서 복셀 수 비 = 부피 비다. → **두 논문의 숫자를 변환 없이 견줄 수 있다.**

⚠ **그러나 닫힌 형태는 옮길 수 없다.** 아래 식 (8) 과 `A_spec` 멱법칙의 적용 조건
("AM 구 · 균일 입도 · 겹침 없음 · SE 3 µm 고정")이 Clausnitzer 구조에서 **전부 깨진다**:
CAM 은 육각판 3 종 + 구 2 종 혼합, SE 는 구 3 종(0.5/1.0/2.5 µm) 다분산, 결합은
Voronoi 기하 소결이다 (2호 digest §4.2).

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

### ⚠ 이 곱은 **충분하지 않다** (2026-09-16, `assb` 2호가 준 반례)

Clausnitzer 2023 이 같은 논문 안에서 반례를 준다: `SVF_LCO = 69.4 %`, 소결 밀도 70 %,
입계 저항 무시 → `[도표]` **CAM 연결성 ≈100 %** 인데 **정규화 용량 ≈0.10**.
모든 AM 이 집전체에 붙어 있는데도 90 % 가 안 쓰인다 (이온 쪽 굴곡도·격리와 전류 탓).
→ **항이 하나 더 있다**: `Q_apparent = θ_AM · η(i) · Q_material`.
셋째 항과 그것을 분리하는 시험(율 스윕·이완)은 [[assb-apparent-capacity-decomposition]].

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

### ⚠ 그리고 이 규율이 후속 논문에서 **지켜지지 않았다** (2026-09-16)

Clausnitzer 2023 은 이 계보의 후속인데도 **오차 막대가 단 한 그림에도 없다**
(`standard deviation`·`error bar`·`seed` 각 **0 회**; `random` 1 회는 GB ID 배정).
**파라미터 점당 구조 1 개**다. 게다가 도메인이 더 작다 —
`[재현]` `25×25×50 / 80×80×140 = 31250/896000 ≈ **1/28.7**` 부피.
→ `[해석]` **산포는 Bielefeld 보다 클 가능성이 높은데 보고되지 않았다.** 그 논문
Fig. 10 의 "상위 3 개"(0.94 / 0.93 / 0.89) 같은 순위는 **신뢰 근거가 그 논문 안에 없다.**
이것은 우리가 그 논문에 **싸게 공급할 수 있는 것**이기도 하다 (N 개 실현 → 폭).

## 이 위키에서의 적용

- [[assb-contact-loss-vs-lampe]] 의 미결 항목 1("접촉 손실을 모델에 어떤 형태로 넣나")에
  **형태**를 준다: 용량 축 스케일에 곱해지는 기하 인자. **동역학(`θ_AM` 의 사이클 의존)은
  여전히 비어 있다** — 원문은 pristine 정적 기하만 모델링한다.
  ⚠ **2호를 읽고도 비어 있었다**: Clausnitzer 2023 도 `[인쇄]` "pore formation during cycling …
  **beyond the scope**" · "our current model **does not incorporate mechanics**" 이고
  **방전 1 회**다. 3호도 방전 1 회 + 충전 1 회. `assb` **3/3 편이 `θ` 의 시간축을 주지 않았다.**
  (다만 2호의 `ρ_S`(소결 밀도) 스윕이 **후보 대리 축**이다 — ⚠ 제조 공극과 사이클 균열은
  **공극의 분포**가 다를 수 있다.)
  → ✅ **4호(Shi 2020)가 처음 줬다** — 사이클 **0/10/50** 의 void 부피분율
  **2.87/3.23/9.50 vol%**. ⚠ 그러나 (a) 재는 양이 `θ` 가 아니라 **void 부피/접촉 면적**,
  (b) 3 점 · 각 점 **다른 셀** · 반복 0, (c) 모양이 **계단**이고 그 계단이
  **검출 한계의 산물일 수 있다**. (§"4호는 실측을 줬는데 …")
  ⚠ **3호를 읽고도 비어 있다**: Liu 2024 는 방전 1 회(+ 충전 1 회)이고 사이클 축 그림이
  **0 장**이며, 무엇보다 **파괴·디본딩 모형이 없다**. `assb` **3/3 편이 시간축을 주지
  않았다** — 그리고 이제 **공통 원인**이 보인다 (§"3호는 이 `θ` 와 변환되지 않는다").
- **`θ` 는 스칼라가 아니다** (2호가 추가): `[인쇄]` "The share of unconnected clusters
  **increases with increasing distance from the separator**." → forward model 에 넣을 때
  최소한 "평균 + 기울기" 두 수가 필요하다 ([[assb-apparent-capacity-decomposition]]).
- [[fitting-degeneracy]] 가 화학과 무관하게 재현될 자리 하나를 확인해 준다:
  `A_spec,a` 의 봉우리가 **평탄**하고(±3–4 vol% 구별 불가) 두께 20–140 µm 곡선이
  최적 근방에서 **겹친다** → 그 관측으로 미시구조를 역추정하면 flat valley 를 만난다.
  원문은 forward 전용이라 그 문제를 만나지 않았을 뿐이다.
- [[mode-identifiability-unmeasured-lineage]] 와 같은 형식의 관측이 `assb` 축에서도 성립한다:
  원문 저자들이 **8 편을 지목해** "공극률이 보고되지 않는다" 고 적었다. `assb` 축의
  "모두가 빠뜨린 필수 변수" 원장 — 현재 **공극률**(1호가 지목) +
  **LLZO 복합전극의 부분 전도도**(2호가 스스로 "문헌에 없다") +
  ~~**압력**~~ (`assb` 1–3 호가 0 회였고 **4호에서 해소** — 제작 100/300/100 MPa ·
  사이클 **~2 MPa 스프링** · **재가압 300 MPa**; ⚠ 스윕은 여전히 없다) +
  **구조·셀 실현 산포**(1호만 쟀다 — 2·3호는 `[인쇄]` "the **random arrangement** …
  play a critical role" 라고 적고도 실현 1 개, **4호는 실험인데도 조건당 셀 1 개 ·
  오차막대 0**. `assb` **4 편 중 3 편**) +
  **유일성·식별성**(`assb` **4/4 편이 안 쟀다**. 1–3 호는 forward 전용이라 원리적으로
  못 쟀고, ★ **4호는 역문제를 풀면서**(EIS 등가회로) `[인쇄]` 시간상수가 겹쳐 "not
  possible to precisely assign" 이라 적고도 `R_MF` 를 점추정으로 서사의 기둥에 쓴다) +
  **파괴·디본딩 모형**(1–3 호에 없다 — `θ(N)` 이 비어 있던 **진짜 이유**. 4호는 모형
  대신 **실측**으로 그 자리를 채웠다) +
  **접촉 면적 → 이용 가능 용량 사상**(★ **4호가 새로 연 공백** — 10.4 % ↔ 60 %p) +
  **분할·검출 한계의 정량**(4호: 분할 정확도 0, 면내 화소 크기 0) +
  **접근 가능한 코드**(3호: 공개된 것은 DAMASK v2.0.2, 실제로 쓴 것은 별 저장소 +
  기관 허가 + CLA. 공개본에는 Li 화학도, 논문이 "developed" 라고 적은 FEM 솔버도 없다).

## ★★ 이 `θ` 가 야생에서 어떻게 인용되는가 — 첫 실측 (2026-09-22 추가, `assb` 15호)

이 페이지는 1호의 `θ` 에서 용량·전압으로 내려가는 다리가 **원문에 없다**고 적어 왔다
(§"이 페이지가 주장하지 않는 것" 첫 항). **2026-09-22 에 그 공백이 바깥에서 어떻게
처리되는지의 첫 표본이 들어왔다** — `raw/papers/rahman2024_sbms-rul-solid-state-batteries.md`
(Rahman & Lu, *Proc. IISE Annual Conf. & Expo 2024*, Abstract ID 8085).

**(가) 1호를 BMS 문장의 근거로 쓴다 — 그리고 어긋난다.**
그 편의 ref **[5]** 가 1호이고, 인용된 **유일한 자리**가 `[인쇄]` "These technologies
[ANN, Adaptive Fuzzy Logic] … mainly address key challenges such as **load balancing,
state-of-charge estimation, and overall battery health monitoring [5, 6]**" 다.
1호 digest 가 전수 계수로 적은 원전의 상태는 `[인쇄]` **"셀 실험 0 개이고, 사이클링·
전압·용량이 없다"** · `voltage` **1 회(참고문헌 제목)** · **모델에 음극이 없다** 이다.
→ **어긋난다.** 서지도 틀렸다 — **연도 2018(원전 2019)**.

**(나) 다리가 없는 채로 결론만 건넌다.**
같은 편 §4.1 은 1호의 **속편**(ref [28], Bielefeld *ACS AMI* 12, 12821, 2020, 바인더 편)을
대체로 맞게 요약한 뒤 `[인쇄]` "**These aspects are crucial for optimizing SBMS in SSBs**"
로 끝낸다. **굴곡도·유효 전도도·활성 표면적에서 BMS 로 가는 문장이 0 줄이다** —
그 기하량이 셀 전압/용량으로 어떻게 내려오는지, BMS 가 무엇으로 관측하는지 없다.

`[해석]` **이 페이지가 `Q_apparent = θ_AM · Q_material` 을 "우리 해석" 이라고 못 박고
"원문은 용량도 전압도 주지 않는다" 고 경고한 것이 보수적이지 않았다.** 그 다리는
바깥에서 **건너뛰어진 채로** 인용된다. 우리가 `θ` 를 DEM 라벨로 쓸 때 **폭을 반드시
붙이기로 한 규율**([[near-optimal-set-width-measurement]])이 여기서 다시 정당화된다.

⚠ **15호 자체는 이 페이지에 아무 수치도 더하지 않는다** — `contact`·`capacity`·
`percolat*`·`θ` 가 전부 **0 회**인 6 쪽 회의록이고 1차 측정도 재인용 수치도 0 이다.
여기 적히는 것은 **인용 관계**뿐이다.

## ★★★★ measured 라벨이 왔다 — 그리고 1호 식 (8) 이 3–15 배 과대 예측한다 (2026-09-23 추가, `assb` 22호)

`raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md` (Strauss 외 2018, *ACS Energy Lett.* 3, 992−996)
— **1호가 이 `θ` 의 유일한 실험 대조로 인용한 ref 13** 이다.

### 무엇을 쟀나 — 역산이 아니다

첫 C/10 충전 뒤 복합양극을 ex situ XRD 로 찍어 **두 NCM 상**(충전된 상 `x ≈ 0.46–0.56` · pristine 격자 상)을
동시 Rietveld 정련 → **상 분율(무게)** = `[인쇄]` 불활성 **2 / 27 / 31 %** (d₅₀ 4.0 / 8.3 / 15.6 µm).
용량은 입력되지 않고 **나중에 독립 대조**로만 쓰인다(`[인쇄]` 90 / 92 / 153 ↔ 전기화학 84 / 95 / 162 mAh g⁻¹).
⇒ **`θ` 형 양이 처음으로 측정된 양이 된다.**

### 그러나 등호가 아니다 — 관측 연산자

| 이 페이지의 `1 − θ_AM` | 22호의 `f_inactive` |
|---|---|
| 전자 퍼콜레이팅 클러스터 밖 AM 부피 (기하, 이진) | 첫 C/10 충전에서 `x` 가 움직이지 않은 결정 영역의 무게 분율 |
| 이온 무관 | 전자 ∪ **이온** ∪ **SE 접촉 없음** ∪ **2차 입자 내부 코어** ∪ **율** |
| 전극 평균 | `[재현]` **집전체 면 표층 가중** — Cu Kα 반사 1/e 깊이 ≈3 µm(003) – ≈15 µm(2θ 90°), 전극 90 µm |

⇒ `f_inactive ≥ 1 − θ_AM^{elec}` (같은 자리에서). DEM `θ` 를 XRD 와 대려면 **(i) 깊이 가중 (ii) `θ_SE`
(iii) 입자 내부 항 (iv) 율** 을 모델 쪽에 붙인 관측 연산자가 필요하다.

### ★★★★ 1호 식 (8) 을 이 조성에 대면 — 공극률 없이도 비교된다 `[재현]`

7:3 wt 의 AM 부피 분율(고체 중)은 1호 자신의 밀도비(1호 G4 `ρ_AM/ρ_SE ≈ 2.35–2.45`)로 **48.8–49.8 vol%**.
**공극률은 이 값을 낮추기만** 하므로 무공극이 1호에 가장 유리한 상한이다.

| | `p_c(d)` (식 8) | AM − p_c | 1호 예측 불활성 | **측정 (XRD)** | **용량만의 상한** |
|---|---|---|---|---|---|
| NCM-S (4.0 µm) | 47.5 | +1.3 ~ +2.3 | ≈23–40 % | **2 %** | ≤3 % (C/30) |
| NCM-M (8.3 µm) | 53.2 | −3.4 ~ −4.4 | ≈95 % | **27 %** | ≤39 % (C/30) |
| NCM-L (15.6 µm) | 58.2 | −8.4 ~ −9.4 | ≈95–97 % | **31 %** | ≤44 % (C/50) |

(1호 5 µm 곡선을 `[인쇄]` "steepness … similar for all particle sizes" 에 기대 p_c 차만큼 옮겨 읽음.)
⇒ **순위는 맞고 크기는 3–15 배 어긋난다 — XRD 없이 용량만으로도 기각된다.** 1호의 "correlate well" 은
**순위 일치**의 표현이다. ⚠ 1호 쪽 사정(SE 3 µm 고정 · 구형 무겹침 · 밀링 없음)이 이 복합체와 다르므로
"모델이 틀렸다" 가 아니라 **"식 (8) 은 이 재료계의 불활성을 예측하지 못한다"** 까지다.

## 이 페이지가 주장하지 않는 것

- `θ_AM` 이 접촉 손실의 **올바른** 모형이라고 주장하지 않는다. 원문의 `θ` 는 접촉 저항을
  배제한 **정적 상한**이고 시간축이 없다.
- `Q_apparent = θ_AM · Q_material` 은 **우리 해석**이다 — 원문은 용량도 전압도 쓰지 않는다
  (전압축 자체가 논문에 없다).
- 원문이 유효 전도도(S/cm)를 계산했다고 주장하지 않는다. **한 번도 계산하지 않았다** —
  그럼에도 초록이 그 결과를 말한다 (digest §10 불일치 1).
  (그 공백은 **2호가 채웠다** — Clausnitzer 2023 은 식 (5) 로 `σ_eff` 를 S/cm 로 계산해
  Fig. 3·S4 에 찍는다.)
- **4호(Shi 2020)가 `θ_AM` 을 쟀다고 주장하지 않는다.** 4호는 **면적 분율**을 쟀고
  **퍼콜레이션 판정을 하지 않았다** (`percolat*` 0 회). 그리고 그 면적 분율을 이 곱에
  넣으면 자기 실험(압력 회복 60 %p)과 **6 배 어긋난다.**
- **4호의 10.4 %·9.50 % 가 확정값이라고 주장하지 않는다** — 분할 정확도 수치가 없고
  해상도 바닥이 미명시라 **하한**이다.

## 관련
- [[assb-apparent-capacity-decomposition]] — 이 곱에 **셋째 항 `η(i)`** 를 더한다. 반례와 분리 시험.
- [[assb-pressure-reapplication-separation-test]] — **이 `θ_AM` 을 (부분적으로) 되돌리는 조작.**
  4호의 실측이 여기 있고, 위 6 배 간극의 다른 쪽 끝이다.
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 개념이 그 미결 항목 1 에 답한다.
- [[fitting-degeneracy]] — 액체셀 축퇴. 여기서 재현될 자리를 이 페이지가 지목한다.
- [[near-optimal-set-width-measurement]] — 화학 무관한 폭 측정기. 이 forward map 위에도 걸린다.
- [[np-lip-ocv-reparametrization]] — 닫힌 형태 null 방향의 선례.
- [[mode-identifiability-unmeasured-lineage]] — "모두가 안 잰 것" 원장의 형식.
