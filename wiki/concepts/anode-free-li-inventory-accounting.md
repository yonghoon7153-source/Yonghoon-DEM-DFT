---
title: 무음극 ASSB 의 Li 인벤토리 계정 — 무엇으로 세고, 어디까지 갈리나
description: "In an anode-free ASSB there is no Li reservoir, so LLI must be read off charge balance alone. Lee 2020 gives exactly two estimators (first-cycle irreversible capacity and per-cycle Coulombic efficiency) plus three Li-specific observation channels (SEM absence, EELS Li map, XRD of Li9Ag4) — and the two estimators disagree by 10x in the same paper"
created: 2026-09-16
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# 무음극 ASSB 의 Li 인벤토리 계정 — 무엇으로 세고, 어디까지 갈리나

> `assb` 축의 **다섯 번째** 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 앞의 넷: [[composite-cathode-percolation-utilization]] (`θ_AM`) ·
> [[assb-apparent-capacity-decomposition]] (3 항 분해) ·
> [[assb-pressure-reapplication-separation-test]] (`P↑` 분리 연산자) ·
> [[assb-stack-pressure-operating-window]] (압력 창).
>
> 이 페이지는 **음극 축**이다. 앞의 넷이 `LAM_PE`↔접촉 손실을 다뤘다면 여기는
> **`LLI` 를 무엇으로 세는가**다.
>
> 수치의 정본은 원문 PDF 이고 여기 값은 **사본**이다 — 인용 근거로 쓰지 않는다.
> **모집단**: Lee 2020 = Ag:C=1:3 무음극 / Li₆PS₅Cl / LZO-NMC(Ni 90) 6.8 mAh cm⁻² /
> **60 °C** / 2.5–4.25 V / 조건당 **셀 수 미상**.

## 정의

무음극(anode-free) 셀에는 **Li 저장고가 없다.** 셀 안의 모든 순환 가능 Li 는
처음에 양극에 있었고, 음극 쪽에 남은 Li 는 **전부 손실**이다. 그래서 `LLI` 는
원리적으로 **전하 수지 하나**로 정의된다:

```
LLI_cum(N)  =  Σ_{i≤N} ( Q_ch,i − Q_dis,i )        ← 누적 결손
             =  SEI-Li  +  dead Li  +  합금 Li(Li₉Ag₄)  +  LiC_x  +  ...
```

**문제는 두 가지다.**
1. 우변의 네 항을 **가르는 관측이 없다** (아래 §"네 개의 채널").
2. 좌변을 재는 **두 개의 추정자**(첫 사이클 비가역분, 사이클당 CE)가
   **같은 값을 주지 않는다** (아래 §"두 추정자가 안 맞는다").

## 추정자 둘 — Lee 2020 이 실제로 주는 것

`raw/papers/lee2020_ag-c-anode-free-assb.md` (`assb` 6호, SAIT/Samsung,
*Nature Energy* 5, 299–308).

### (a) 첫 사이클 비가역분 — ★ 전극 귀속이 되는 유일한 조각

`[도표]` SI Fig. 7 (0.1 C 충전 / 0.2 C 방전, **같은 양극**, Ag–C 유/무):

| | 충전 | 방전 | `[재현]` ICE | `[재현]` 비가역 |
|---|---:|---:|---:|---:|
| **Ag–C 有** | ≈233 mAh g⁻¹ | ≈214 | **91.8 %** | **19 mAh g⁻¹ (8.2 %)** |
| **Ag–C 無** | ≈233 | ≈217 | 93.1 % | 16 (6.9 %) |

★ **차분 ≈3 mAh g⁻¹ (≈1.3 %p) 가 Ag–C 층에 귀속되는 몫의 상한**이다.
`assb` 계보에서 **전극에 귀속 가능한 첫 `LLI` 조각**이다.
⚠ 셀 1 개씩, 오차 없음. 그리고 **나머지 16 mAh g⁻¹ 은 귀속되지 않는다.**

### (b) 사이클당 CE 결손

| 셀 | CE (`[도표]`) | 용량유지율 (`[인쇄]`) | `[재현]` 유지율이 함의하는 CE | 맞나 |
|---|---:|---:|---:|:--:|
| **20 mAh** 소형 파우치 (SI Fig. 13) | **99.97 %** | 92.5 % @ 300 | **99.974 %** | ✅ |
| **0.6 Ah** 프로토타입 (Fig. 6g) | **99.89 %** | 95 % @600 · **89 % @1000** | **99.988 %** | ❌ **10 배** |

## ★★★ 두 추정자가 안 맞는다 — 그리고 정답이 같은 논문 안에 있다

`[재현]` 0.6 Ah 셀에서 CE 99.89 % 를 **영구 Li 손실**로 읽으면
사이클당 0.16 mAh g⁻¹ × 1000 = **누적 161 mAh g⁻¹**.
실제 관측된 손실은 **16 mAh g⁻¹** 이고 양극 전체 재고는 **215 mAh g⁻¹** 다.
**약 10 배 어긋난다.**

두 가지 해석만 남는다:

| 해석 | 함의 | 이 논문의 증거 |
|---|---|---|
| **① CE 가 계측 바닥에 걸려 있다** | 참 CE ≈99.99 %, ">99.8 %" 는 **하한 선언** | ★ 20 mAh 셀은 **CE 축이 99.4–100.0** 으로 확대돼 있고 값이 **맞는다.** 0.6 Ah 셀의 축은 **95–101** — **분해능 자체가 다르다** |
| **② 결손의 상당 부분이 가역이다** | Ag–C 층이 Li 를 **빌려 갔다 돌려준다** | `[인쇄]` Li₉Ag₄ 가 방전 후 사라진다 (XRD). ⚠ 그러나 `[재현]` Ag 저장 상한은 **셀의 0.45–0.89 %** 로 1000 사이클치 결손(≈110 %)에 **턱없이 모자란다** |

`[해석]` **①이 압도적으로 그럴듯하다.** 그리고 논문은 **두 셀을 한 번도 비교하지
않고**, CE 의 계측 정밀도를 **명시하지 않는다**.

> ★★★ **우리에게 남는 명제**: 무음극 셀에서 **CE 는 `LLI` 의 추정자이지만,
> 그 유용성은 전적으로 분해능이 정한다.** 사이클당 열화율이 0.011 % 인 셀에서
> CE 를 0.1 % 정밀도로 재면 **아무것도 못 센다.**
> "CE 99.8 % 와 99.99 % 를 구분할 정보가 자료에 있는가" 는 판정 가능한 질문이고,
> [[near-optimal-set-width-measurement]] 가 그대로 걸린다.

## ★★ `η` 가 `LLI` 의 완충기다 — 유지율은 하한만 준다

`[재현]` 같은 셀의 0.5 C 방전 용량은 146 mAh g⁻¹, 0.2 C 는 215 →
**`η(0.5C) ≈ 0.68`**. **양극 재고의 32 % 가 운전 창 밖에 있다.**

`[해석]` Li 를 잃어도 양극이 쓰는 SOC 창이 **이동할 뿐** 용량은 덜 준다.
→ **겉보기 용량유지율은 `LLI` 의 하한이다.** 완충 여력은
`[재현]` **69 mAh g⁻¹** (215 − 146) 이고, 위 D2 의 간극(161 mAh g⁻¹)을
**부분적으로만** 설명한다.

이것은 [[assb-apparent-capacity-decomposition]] 의 `η` 가 **`LAM_PE` 뿐 아니라
`LLI` 도 가린다**는 뜻이다 — 3 항 분해가 상대해야 할 것이 하나 더 늘었다.
액체셀 축의 같은 좌표는 [[np-lip-ocv-reparametrization]] 의 `N/P` · `Li/P` 다.

## ★★★ 세 번째 추정자 — operando 상 동정 + 전하 수지 (2026-09-16, 7호)

`raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`
(Spencer-Jolly et al., *Joule* 7, 503–514, Bruce 그룹/Oxford).
⚠ **모집단이 다르다**: **흑연**(카본블랙 아님) · **반쪽전지**(상대극 Li 금속) ·
**상온 30 µA cm⁻² ≈ C/68** · **1 사이클** · 통과 전하가 층 용량의 **≈4 배**.
**6호의 완전지 수치와 직접 비교하지 않는다.**

이 논문은 `Coulombic`·`efficiency`·`dead`·`isolated` 를 **본문+SI 전수 0 회** 쓴다.
**그런데 자기 Fig. 1(충전)·Fig. 3(방전)의 시간축이 수지를 닫을 재료를 준다.**

| `[재현]` | 값 | 근거 |
|---|---:|---|
| 충전 통과 | **2.03 mAh cm⁻²** | `[도표]` 67.6 h × 30 µA cm⁻² (`[인쇄]` "2 mA h cm⁻²" 와 일치) |
| 방전 회수 | **1.05** | `[도표]` 35.0 h × 30 µA cm⁻² |
| 계면상(SEI) 구간 | **0.19** | `[도표]` Fig. 1 분홍 배경 0 → 6.5 h |
| **첫 사이클 효율** | **≈52 %** | 1.05 / 2.03 |
| ★ **설명되지 않는 비가역분** | **≈0.79 mAh cm⁻² = 통과 전하의 39 %** | 2.03 − 1.05 − 0.19 |

**왜 dead Li 후보인가**: 방전 종료 회절에 `[인쇄]` "only **graphite and Ag** are
observed" → 층 **안에** 저장된 Li(LiC_x + Li_xAg)는 **전부 돌아왔다**. 남는 통로는
**추가 SEI** 와 **전기적으로 고립된 Li 금속** 둘뿐이다.
⚠ **그 둘은 여전히 안 갈린다** — 이 계정의 본래 한계가 그대로다.
⚠ 그리고 이 계산은 **Fig. 1 과 Fig. 3 이 같은 셀**이라는 가정 위에 선다
(논문이 적지 않는다). 상세·오차·대안 해석은 7호 digest §7.

> ★★★ **`assb` 7 편 중 처음으로 "안 돌아온 Li" 가 숫자로 떨어진다.**
> 5호 = "수단이 없다" · 6호 = "기구로 지목하고 안 잰다" · **7호 = 재지 않았지만
> 잴 재료를 인쇄했다.** 그리고 그 값이 크다.
> ⚠ **사이클 축이 없으므로 `LLI(N)` 로 옮길 수 없다.** 한 점이다.

★ 같은 논문의 **상(相) 경로**(무엇이 어느 그릇에 들어갔다 나오는가)는
[[ag-c-interlayer-lithium-phase-path]] 로 분리했다 — 이 페이지는 **총량**을 맡는다.

## 네 개의 채널 — 그리고 무엇이 안 갈리나

| # | 채널 | 무엇을 보나 | 정량 | 한계 |
|---|---|---|:--:|---|
| ① | **방전 상태 단면 SEM** | 도금 Li 층의 **소멸** | ✗ | `[재현]` 치밀 Li 1 µm = **0.206 mAh cm⁻²** = 6.8 의 **3.0 %**. 사이클당 손실(0.011 %)보다 **≈270 배 거칠다**. **음성 증거만** |
| ② | ★ **EELS Li 맵** | Ag–C 층 **내부** Li, nm 척도 | ✗ | `[도표]` **방전 후·100 사이클 후에도 Li 망이 남는다** (pristine 에는 없다). dead Li / LiC_x / SEI / 합금 잔여를 **못 가른다** |
| ③ | ★★ **XRD 의 Li₉Ag₄** | **합금에 담긴 Li** — 상으로 동정 | ✗ | 가역적(방전 후 소멸) → **dead Li 가 아니라 "돌아오는 Li" 의 그릇**. Rietveld 없음 |
| ④ | **CE + 용량유지율** | 총 결손 | ○ | **전극·화학종 귀속 0**, 그리고 둘이 안 맞는다 |
| ⑤ | ★★ **operando PXRD 상 순서 + 전하 수지** (7호) | Li 를 담은 **모든 상**을 시간축 위에서 (LiC_x 5 종 · Li–Ag 5 종 · Li 금속) + 그 나머지 | **△** (총량만 `[재현]`, 상 분율 ✗) | **Rietveld 0** → 상별로 못 나눈다. **SEI ↔ dead Li 안 갈림**. 1 사이클 · 반쪽전지 |

★★ **5호(Doux 2020)와 합치면 이렇게 된다**:

| 화학종 | 관측 수단 | 누가 | 정량 |
|---|---|---|:--:|
| **SEI Li** | XRD 상 검출 (Li₂S · LiCl · P₄ · Li₃P₇) | 5호 | ✗ |
| **합금 Li** | XRD 상 검출 (Li₉Ag₄) | **6호** | ✗ |
| **LiC_x** | (EELS 가 C 입자 위 Li 를 보지만 화학 이동 미사용) | 6호 | ✗ |
| **dead Li** (전기적 고립 Li 금속) | **없다** — XRD 로 Li 금속이 안 보이고(5호), 토모는 밀도 대비뿐(5호), SEM 은 3 % 이하를 못 본다(6호) | — | ✗ |

`[해석]` **Q7 은 5호에서 절반 깨졌고 6호에서도 절반이다.** 채널이 둘 늘었지만
**정량이 0 이고**, **dead Li 만 여전히 수단이 없다.**
⚠ 그리고 6호는 `[인쇄]` "the discharge capacity decays due to the generation of
**isolated lithium**" 이라고 **기구로 지목하면서 한 번도 재지 않는다.**

## 음극이 인벤토리의 **양쪽**에 있다 — Ag 의 자리

[[assb-apparent-capacity-decomposition]] 의 `Q_apparent = θ_AM · η(i,P) · Q_material`
는 **음극이 무해하다**는 전제로 세워졌다. Ag–C 무음극은 그 전제를 깬다:

| Ag 의 역할 | 근거 (`[인쇄]`) | 들어갈 칸 |
|---|---|---|
| Li 를 담는 활물질 (Li₉Ag₄) | XRD Fig. 5n · Fig. 4 의 3.5–3.55 V | **`Q_material`** (음극 쪽). `[재현]` **559 mAh g⁻¹(Ag)**, 셀 기준 **0.45–0.89 %** |
| 핵생성 자리 = 접촉·균일성 | "lowers the nucleation energy" | **`θ`** (음극 계면) |
| 전하이동 속도론 | SI Note 1; Ag 단독의 율 붕괴 | **`η(i)`** |
| ★ **비가역 Li 저장소** | SI Note 3 "irreversible Li remaining in Ag NPs" | **`LLI` 쪽 항** |
| ★★ **매 사이클 이동하는 상태변수** | "continuously moves … does not return" | `θ`·`η` 의 **시간 의존 파라미터** |

★ `[재현]` **상한이 계산된다**: Li₉Ag₄ 완전 형성을 가정해도 Ag 가 삼킬 수 있는
Li 는 **셀 용량의 0.89 % 이하**다 (Ag 8–16 mg Ah⁻¹, 2.25 Li/Ag).
→ **첫 사이클 비가역 8.2 % 중 Ag 합금이 설명하는 것은 최대 1/9.**
나머지는 SEI + dead Li + LiC_x 이고, **이 논문은 그 셋을 가르지 않는다.**

## ★★★ 네 번째 표본 — N/P < 1 과충전 셀: CE 결손이 Li 재고를 **넘는다** (2026-09-23, 52호)

`raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md` (Oh … Choi 2025, *Adv. Energy Mater.* 15, 2404817).
⚠ **모집단**: 무음극이 아니라 **"무음극형"** — SiGr 소량(0.8 mg cm⁻²) 아래 Mg 200 nm, 용량의 85 %(N/P 0.15) · 34 %(N/P 0.66)가 Li 도금. LiNbO₃-NCM811 \| LPSCl · **25 °C** · 20 · 3 MPa · 조건당 셀 1.

| 셀 | CE | 유지율 (`[인쇄]`) | `[재현]` 누적 충–방 결손 | 관측 손실 | 맞나 |
|---|---:|---:|---:|---:|:--:|
| 20 MPa · N/P 0.15 | 평균 **99.2 %**(`[인쇄]`) | 83.7 % @75 | ≈**95** mAh g⁻¹ | ≈27 | ❌ ≈3.5 배 |
| 3 MPa · N/P 0.66 | `[도표]` **≈85–97 %**(본문 무언급) | 64.7 % @75 | ≈**575** | ≈40 | ❌ **재고(≈275)의 ≈2 배** |

Lee 2020(6호)의 어긋남은 **해석 ①(CE 계측 바닥)** 이 압도적이었다. 여기서는 그 해석이 **안 선다** — 3 MPa CE 는 85–97 % 로 바닥과 거리가 멀다. 남는 해석(`[해석]`): **누설 전자**(저자 자신이 SI S17 에 그린 연성 단락 병렬 `r_SS` — 충전 중 Li 이동 없이 전하가 흐른다) 또는 **SE 분해가 재고를 보충**(양극 쪽 LPSCl 산화가 Li⁺ 를 내고 음극에 도금 — 그 자체가 부반응). 어느 쪽이든 **이 셀에서 CE 는 `LLI` 의 추정자가 아니다.**

★ **완충 방향이 하나 더**: `η` 완충(위 §) 말고 **끝 전극 모드**가 있다 — 양극이 방전 끝을 내면 음극에 남은 Li 가 손실을 흡수해 **CE ≈1 인 채로 재고가 준다**; 음극이 끝을 내면 `LLI` 가 곧 용량이다. 이 편은 어느 모드인지 가를 재료(3전극 · dV/dQ)가 없다. 형성 때 음극에 남은 Li(`[도표]` 20 MPa 충전 ≈200 − 방전 185 ≈15 mAh g⁻¹)가 저장소 상한이다.
★ **조건 간 비교는 면적당으로**: `[재현]` 두 압력의 결손은 ≈0.025 ↔ ≈0.046 mAh cm⁻² 사이클⁻¹(×≈1.8) — CE 차 ×≈7 의 대부분은 양극 적재 20 ↔ 6 mg cm⁻² 다.

> ★★★ **우리에게 남는 명제(6호 명제의 짝)**: CE 가 `LLI` 추정자가 되려면 분해능(6호)만이 아니라 **누설이 0 이라는 것과 끝 전극 모드**가 먼저 서야 한다. 누적 결손이 재고를 넘는지는 한 줄로 검사된다 — [[assb-lampe-contact-product-degeneracy]] 처방 표 "누적 충–방 결손 ↔ Li 재고 상한".

Q7(dead Li ↔ SEI Li): 이 편도 **0** — `dead` · 적정 · 재고 수지 낱말 0, SEI 는 SiGr 반쪽 Nyquist 의 새 반원 이름뿐.

## 이 페이지가 주장하지 않는 것

- **CE 가 틀렸다고 주장하지 않는다.** 위 ①/② 중 어느 쪽인지는 원문에 계측
  정밀도가 없어서 **정할 수 없다.** 주장하는 것은 **두 추정자가 같은 물리를
  지지하지 않고 논문이 그것을 검토하지 않았다**는 것뿐이다.
- **EELS 의 Li 신호가 dead Li 라고 주장하지 않는다.** LiC_x·SEI·합금 잔여일 수 있다.
- **이 계정이 양극 축에 답한다고 주장하지 않는다.** Lee 2020 은 양극 사후 분석이
  **0** 이고, [[assb-contact-loss-vs-lampe]] 의 본체(`LAM_PE` ↔ 접촉 손실)에는
  입력을 주지 않는다.
- **이 숫자들을 다른 무음극 계로 옮기지 않는다.** Ag–C / 60 °C / 0.5 C /
  6.8 mAh cm⁻² 한 모집단이고 **셀 수가 밝혀져 있지 않다.**
- **7호의 `[재현]` 0.79 mAh cm⁻² 가 전부 dead Li 라고 주장하지 않는다.** 계속되는
  SEI 성장이 같은 뺄셈에 들어간다. 주장하는 것은 **① 크기가 이 정도이고 ② 논문이
  그 뺄셈을 하지 않았다**는 것뿐이다. 그리고 그것은 **반쪽전지 한 점**이다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지가 그 미결 항목 3(무음극의
  dead Li ↔ SEI Li)에 **채널 다섯과 그 한계**를 넣는다.
- [[ag-c-interlayer-lithium-phase-path]] — 같은 Ag–C 계의 **상(相) 경로**. 이 페이지가
  **총량**, 저 페이지가 **그릇**을 맡는다.
- [[assb-apparent-capacity-decomposition]] — 3 항 분해. 이 페이지가 **음극 인벤토리
  항**을 요구하고, `η` 가 `LLI` 도 가린다는 것을 더한다.
- [[assb-stack-pressure-operating-window]] — 같은 논문이 압력 축도 쪼갠다 (제작 ↔ 운전).
- [[near-optimal-set-width-measurement]] — "CE 99.8 % 와 99.99 % 를 가를 정보가 있는가"
  를 판정하는 기계.
- [[np-lip-ocv-reparametrization]] — 액체셀 축에서 같은 완충 현상(`N/P` 가 크면 `LLI` 가
  곡선에 안 나타난다)의 좌표.
- [[halfcell-ocp-shape-invariance]] — 이 셀에서는 **음극 쪽에서 먼저 깨진다**: Ag 가
  매 사이클 이동해 음극 OCP 의 "모양 불변" 가정이 사이클 축에서 무너진다.
