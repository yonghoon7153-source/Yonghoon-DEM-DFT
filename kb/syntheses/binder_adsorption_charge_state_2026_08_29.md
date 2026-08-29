---
title: "음이온성 바인더의 흡착에너지 — ICEP 의 (−H) 는 탈양성자가 아니라 H 이동이었다"
date: 2026-08-29
updated: 2026-08-29
tags: [binder, adsorption, charge-state, estimand, pcet, sdcp, literature, castep]
status: 판독 완료 — ICEP 본문 + SI, Kang 본문 + SI 모두 확보
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-29
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
targetVenue:
---

# ⛔ 한 줄

> **ICEP Figure 2g 의 네 막대는 같은 양이 아니다.**
> 세 번째(`AMPS(−H)`)만 **화학반응(표면으로의 H 이동)** 이고 나머지 셋은 **흡착**인데,
> 축에도 본문에도 그 말이 없다. 그리고 그 반응의 **최종 상태가 정의돼 있지 않다.**

## 하자 — 심각도 순

| | 하자 | 왜 치명적인가 | 근거 |
|---|---|---|---|
| 🔴 **P0** | **환원된 TM 의 상태 선택 규칙이 없다** | H 가 표면으로 가면 **TM 하나가 환원**된다(Ni³⁺→Ni²⁺). 그런데 `spin-polarized` + `U(Ni 6.0/Co 3.4/Mn 3.9)` 를 쓰면서 **FM/AFM 배열도, 환원 전자가 어느 자리에 어느 스핀으로 앉는지도 한 줄이 없다.** 그 선택에 따라 −2.243 이 움직인다 ⇒ **어느 상태의 값인지 말할 수 없다** | SI Experimental Section (전체) |
| 🟠 **P1** | **`(−H)` 만 반응 좌표가 다른데 축이 침묵한다** | 나머지 셋은 물리흡착/수소결합, 이건 화학흡착이다. 한 축에 올리면 독자는 네 막대를 **"결합 세기 순위"** 로 읽는다 | Fig 2g vs Fig S13 캡션 |
| 🟠 **P1** | **본문이 그 막대를 아예 안 다룬다** | 본문 DFT 단락은 *"dissected into **two** representative functional blocks, denoted as **ICEP_AN and ICEP_AMPS**"* — **둘**이라고 못박는다. `(−H)` 는 그림·캡션에만 있는 **예고 없는 네 번째 막대** | 본문 p.6–7 |
| 🟠 **P1** | **`(−H)` 의 기준 분자가 명시돼 있지 않다** | 식 (5) 의 분자 목록이 *"PVDF, ICEP_AN, or **ICEP_AMPS**"* 셋뿐이다. `(−H)` 를 무엇에 대해 뺐는지 SI 가 안 적는다 ⇒ 값의 정의가 독자 추론에 맡겨진다 | SI 식 (5) 설명문 |
| 🟡 P2 | **본문에 binding energy 수치가 0개** | 네 값 전부 `figure-read`. 본문이 쓰는 것은 "AMPS > PVDF" 부등호 하나 ⇒ 그림이 논지를 지탱하지 않는다 | 본문 p.6–7 |
| 🟡 P2 | Γ-only(1×1×1) 로 5×4 초격자 표면 최적화 · 컷오프 **300 eV** · 흡착 자세 탐색 절차·시드·오차막대 없음 | 수치 신뢰구간이 없다 | SI |

## 인용 가부

| | |
|---|---|
| ✅ **인용 가능** | *"AMPS 블록이 PVDF 보다 NCM811 에 강하게 결합한다"* (부등호) · 술포네이트–표면 O 수소결합이라는 **메커니즘** |
| ⛔ **인용 금지** | **−2.243 eV** — 흡착에너지가 아니라 **반응에너지**이고 최종 상태가 미정의 · **네 막대의 크기 순위** · `(−H)` 를 "탈양성자 SO₃⁻" 라고 부르는 것 |

## Thesis

ICEP 의 `AMPS(−H)` 는 **탈양성자 음이온이 아니라 H 가 슬랩으로 옮겨간 상태**다
(SI Figure S13 캡션 명시). 따라서 조성·전하가 보존되고 **두 막대의 뺄셈은 정의된다** —
그것은 흡착에너지 차가 아니라 **표면으로의 H 이동 에너지**다.
남는 문제는 전하가 아니라 **H 이동으로 TM 이 환원되는데 상태 선택 규칙이 없다**는 것이다.

> ⛔ **2026-08-29 자기정정**: 이 카드의 초판은 *"조성이 다른 두 분자라 뺄셈이 정의되지
> 않는다"* 고 썼다. **틀렸다.** 그림만 보고 `(−H)` 를 원자 제거로 읽었는데,
> SI 캡션이 H **이동**이라고 못박는다. 아래 §1-4③·§II-1 에 정정 내용을 남긴다.
> — 우리가 저 논문을 비판한 바로 그 방식(그림만 보고 판정)으로 우리가 틀렸다.

---

## 0. 무엇을 봤나

| 자료 | 상태 |
|---|---|
| **ICEP** 본문 — *Adv. Mater.* **2025**, 37, 2506266, p.3–15 | ✅ 직접 읽음 |
| **ICEP SI** — Experimental Section + Figure S12·S13 캡션 | ✅ **직접 읽음** (docx) |
| **Kang** 본문 — *Adv. Mater.* **2025**, 37, 2416872, p.5–14 | ✅ 직접 읽음 |
| **Kang SI** — Computational method p.7–8 | ✅ 직접 읽음 |
| ICEP Figure S13 **그림 자체** (원자별 접촉) | ⛔ 캡션만 봄 |

---

# I. ICEP (*Adv. Mater.* 2025, 37, 2506266)

## 1-1. 무슨 논문인가

- **ICEP** = ionically conductive elastic polymer. RAFT 삼블록
  `P(AN-co-AMPS)-b-PEO₄₆-b-P(AN-co-AMPS)`, Mw ≈ 100 kDa.
- `[AN]/[AMPS]` 비로 **ICEP-5 / 8 / 19**. **ICEP-8 채택**
  (파단신율 283 % · 인성 601.2 J m⁻³ vs PVDF 31.8 % · 151.8 J m⁻³).
- 기능기 배정: **AMPS 의 SO₃H = Li 전도 + 수소결합** · **AN = 기계물성** ·
  **PEO = 유연성 + Li 전도** · 아미드 **N–H = 수소결합**.
- 계: **NCM811**, Li 금속 풀셀, 초고로딩 **62.4 mg cm⁻² · 12.7 mAh cm⁻²**.

## 1-2. 계산 조건 (SI Experimental Section) — **실제 DFT 다**

| 항목 | 값 |
|---|---|
| 코드 | **CASTEP** (Clark 2005) — 평면파, Materials Studio 계열 |
| 범함수 | **GGA-PBE** |
| 스핀 | **spin-polarized** ✅ |
| PP | **ultrasoft** |
| vdW | **Tkatchenko–Scheffler** |
| 최적화 | BFGS (원자위치 + 셀 파라미터) |
| 수렴 | E 2×10⁻⁵ eV/at · F **0.05 eV/Å** · σ 0.1 GPa · d 2×10⁻³ Å · SCF 2×10⁻⁶ eV/at |
| **컷오프** | **300 eV** |
| **k-point** | LiNiO₂ 단위셀 최적화 **6×6×1** · **NCM811 (001) 표면 = 1×1×1 (Γ 만)** |
| **Hubbard U** | **Ni 6.0 · Co 3.4 · Mn 3.9 eV** |
| 슬랩 | (001), Ni:Co:Mn = 8:1:1 → **32 Ni · 4 Co · 4 Mn**, **8층**, **5×4 초격자** |
| 구속·진공 | **하단 2층 고정**, **진공 > 15 Å** (Fig S12 캡션) |

**결합에너지 식 (5)**:
```
E_bind = E_total − ( E_molecule + E_NCM811 surface )
```
> "where …, …, and … are the total energy of the system, the energy of the
> **PVDF, ICEP_AN, or ICEP_AMPS molecule**, and the energy of (001) surface of NCM811"

⚠ 이 목록에 **`ICEP_AMPS (−H)` 는 없다.** 즉 `(−H)` 막대의 기준 분자를 SI 가 따로 안 정한다.

## 1-3. ⭐ 결정적 문장 — Figure S13 캡션

> "Figure S13. Geometrically optimized structures of ICEP_AN, ICEP_AMPS, ICEP_AMPS (-H),
> and PVDF. **Note that ICEP_AMPS (-H) indicates hydrogen transfer from ICEP_AMPS to the
> NCM811 (001) surface.**"

**`(−H)` 는 원자를 뺀 게 아니라 H 를 슬랩으로 옮긴 것이다.**

- H 가 **계 안에 남아 있다** ⇒ **조성 보존**
- 총전하 **0 유지** ⇒ 음이온도 라디칼도 아니다
- `NELECT`·배경전하 이야기가 SI 에 없는 게 **정상**이다 — 필요가 없다

## 1-4. 본문에서 확정되는 것 (SI 를 봐도 안 바뀜)

### ① `(−H)` 는 **본문에 한 번도 안 나온다** ✅ 유지

본문 DFT 단락 전체:

> "…we conducted **density functional theory (DFT) calculations**… The ICEP structure was
> **dissected into two representative functional blocks, denoted as ICEP_AN and ICEP_AMPS**.
> Notably, **ICEP_AMPS exhibited a significantly stronger binding affinity … compared to
> PVDF**, primarily due to robust hydrogen bonding between the sulfonate group and surface
> oxygen atoms (Figure 2g and Figure S13)."

**"two"** 라고 못박고 둘만 이름을 댄다. `(−H)` 는 **그림·캡션에만** 있다.
⇒ *"분리를 안 하고 바로 PVDF 비교로 갔다"* 는 원문으로 확인. **언급 자체가 없다.**

### ② 본문에 binding energy **수치가 하나도 없다** ✅ 유지

−0.162 / −1.819 / −2.243 / −0.703 eV 는 전부 `figure-read ≈`.
본문이 쓰는 것은 **"AMPS > PVDF"** 부등호 하나뿐이다.

### ③ ⛔ **철회** — "메커니즘 서술과 그림이 안 맞는다"

초판에서 *"`(−H)` 는 술포네이트가 H 를 잃어 수소결합 주개가 될 수 없는데 그림엔 화살표가
있다"* 고 썼다. **철회한다.** H 가 표면으로 갔으므로 이제 **표면 O–H 가 주개**이고
술포네이트 O 가 받개다. 방향만 뒤집혔을 뿐 *"sulfonate group 과 surface oxygen atoms
사이의 수소결합"* 이라는 본문 서술은 **두 경우 다 맞다.**

---

# II. 판정 (정정판)

## II-1. 뺄셈은 **정의될 수 있다** — 단 기준이 명시되지 않았다

조성이 보존되므로 두 막대를 같은 기준으로 놓을 수 있다. 읽기가 둘이다:

| 읽기 | `E_molecule` | 결과 |
|---|---|---|
| **(a)** SI 목록대로 `ICEP_AMPS` (온전한 분자) | 양쪽 동일 | **조성 균형 ✅** — 차 −0.424 eV = **흡착 복합체 안에서의 H 이동 에너지** |
| (b) `(−H)` 조각을 따로 기준으로 | 서로 다름 | 조성 불균형 ⇒ 차가 정의 안 됨 |

SI 의 기준 분자 목록이 **"PVDF, ICEP_AN, or ICEP_AMPS"** 세 개뿐이고 `(−H)` 를 따로 안
적었으므로 **(a) 가 자연스러운 읽기**다. 그러면 −0.424 eV 는 다름 아닌

```
ΔE_PT = E[slab–H ··· AMPS⁻] − E[slab ··· AMPS–H]
```

즉 **우리가 "이걸 계산해야 한다" 고 한 바로 그 양**이다. 그들은 계산해 놓고
**이름을 안 붙였고 본문에서 논하지 않았다.**

⚠ (a) 는 **추론**이다. SI 가 명시하지 않았으므로 확정이 아니다.

## II-2. 그래서 진짜 남는 문제는 전하가 아니다

`(−H)` 는 **화학흡착(H 이동)** 이고 나머지 셋은 **물리흡착/수소결합**이다.
**서로 다른 과정을 같은 축에 이름표 없이 올렸다.** 독자는 네 막대를 "결합 세기 순위" 로
읽는데, 세 번째만 반응 좌표가 다르다.

그리고 이게 우리 규율과 정확히 만나는 지점:

> **H 가 표면으로 옮겨가면 TM 하나가 환원된다** (Ni³⁺ → Ni²⁺).
> 그런데 `spin-polarized` + `U(Ni 6.0)` 를 쓰면서 **슬랩의 자기 배열(FM/AFM)이나
> 환원된 상태의 스핀 선택 규칙을 SI 가 한 줄도 안 적는다.**

`admissible state 가 여럿인데 선택·집계 규칙이 없으면 scalar estimand 는 정의되지 않는다`
(`kb/methodology/estimand_before_running_2026_08_28.md`) — **열린 껍질 · 자성 기판 ·
산화환원 활성** 세 위험신호가 전부 켜져 있다. 우리가 wave1 에서
*"제약된 기준에서 자유로운 복합체를 뺐다"* 로 걸린 것과 같은 층위다.

회신 O: *"고치는 법은 전 계에 같은 NUPDOWN 값이 아니라 같은 **state-selection policy** 다."*

## II-3. 부차적 약점

- **Γ-only (1×1×1)** 로 5×4 초격자 표면 최적화 — 측면으로 크긴 하나 금속성 계에 성기다.
- **컷오프 300 eV** — USPP 라 가능하지만 O·S 포함 계에 낮은 편.
- **시드·오차막대 없음.** 흡착 자세 탐색 절차가 SI 에 없다 (Kang 은 15 회전을 적었다).
- 결합에너지 정의에 **분자의 기하 이완 여부**(고정 vs 재이완)가 안 적혀 있다.

## II-4. 배영진 논지 — **캡션으로 확증됨**

> "전자가 애초에 NCM쪽으로 H랑 전자랑 같이 NCM 쪽으로 이동한거같은디"

**맞다.** 캡션이 *"hydrogen transfer from ICEP_AMPS to the NCM811 (001) surface"* 라고
직접 말한다. H 원자(양성자 + 전자)가 통째로 표면으로 간다. 그리고 PEDOT 대비
*"self-doping 이 아니라서"* 라는 설명도 맞는 방향이다 — 전자가 폴리머에 남을 곳이 없다.

---

# III. Kang — 같은 문제를 **짝이온으로** 푼 대조군

*Adv. Mater.* **2025**, 37, 2416872, PAA-CMC 그래프트(**PC**) + PTFE, NMC622 건식전극.

## III-1. 🔴 Kang 은 DFT 를 안 썼다 (SI p.7–8)

> "**Deep-learning based density functional theory (DFT)** and MD simulations were conducted
> using the **preferred potential (PFP) version v3.0.0** as a **universal neural network
> potential (NNP)** estimator … using **Matlantis** software"

- Figure 4c 값 = **PFP NNP**. Gaussian16 B3LYP 는 **FTIR 진동수 배정 전용**.
- 슬랩 NMC622 *R-3m* **fully lithiated 2×2×1**, 진공 **40 Å**, 하반부 고정.
- ASE **L-BFGS** `fmax 0.01` · `E_ads = E_slab-binder − (E_slab + E_binder)`.
- MD **NVT Langevin 400 K · 10 ps · 1 fs · friction 0.01**.
- 흡착점: **15 configuration 회전**.

⚠ **범용 NNP 에는 전하 입력칸이 없다.** 원자종 + 좌표만 받는다. 그래서 Kang 방식에서는
음이온/중성을 **구별해 지정할 수 없다**. **ICEP 는 CASTEP 이므로 이 제약이 없다** —
두 논문의 차이가 여기서 갈린다.

## III-2. Kang 의 해법 = 짝이온을 넣고 **개수를 상태 이름으로**

PC 도 −COO⁻ 를 갖지만 원료가 **sodium** CMC 라 Na⁺ 가 실제로 있다.

| 상태 | E_ads | 설명 |
|---|---:|---|
| **PC_2Na** | **−2.24 eV** | Na 2개가 표면 O 에 결합 |
| **PC_1Na** | −1.12 eV | Na 1개 |
| **PC_0Na** | −0.37 eV | −OH·−COOH 의 장거리 쌍극자만 |
| PTFE_dimer | −0.09 eV | 표면 O 와 F 가 **정전기적 반발** |

조성 보존 · 총전하 0 · **상태 이름에 Na 개수**.

### 🔴 그런데 결합하는 것이 **음이온기가 아니라 짝이온**이다 (2026-08-29 확인)

- **15 배열 전부 Na 가 2개다.** `PC_1Na`·`PC_0Na` 의 숫자는 총 Na 수가 아니라
  **표면에 접촉한 Na 수**다 (본문 *"the **free Na site** in the PC_1Na system"* 이 확정).
- 결합 모티프: 각 Na⁺ 가 위로 카복실레이트 O 2개(4원환 킬레이트), 아래로 **표면 O 2개**
  → **`–COO⁻ ··· Na⁺ ··· O²⁻` 양이온 브리지**.
- ⇒ **유기 음이온기가 산화물에 직접 붙지 않는다.** −2.24 eV 는 "COO⁻ 결합" 이 아니라
  **"Na⁺ 2개 결합"** 이다. 2.24 → 1.12 → 0.37 이 Na 개수를 따라가는 이유가 이것이다.
- **사후 분류 확정**: SI Fig S15 의 배열 수가 **8 + 3 + 4 = 15** 로 회전 수와 정확히 같다.
  사전 설계였다면 5/5/5 가 나왔을 것이다. 라벨은 이완 **후** 서술이다.
- `PC_0Na` class 는 **스프레드(0.59 eV) > 평균(0.37 eV)** 라 그 평균 자체가 의미 없다.
  (S15 실측: −0.71 / −0.34 / −0.29 / −0.12)

### ⇒ **우리 SDCP 에 그대로 걸리는 함정**

*"음이온기를 짝이온으로 중화하면 된다"* 는 공짜 선택이 아니다. **짝이온을 넣는 순간
그것이 결합 자리가 된다.** 우리가 −SO₃⁻ 를 Li⁺ 로 중화하면 재는 것이
**술포네이트 결합이 아니라 Li⁺ 브리지**일 수 있다 — **estimand 가 조용히 바뀐다.**
Kang 은 이 사실을 논문에서 밝히지 않았고(모티프 서술이 없다), 우리는 이걸
`sdcp_doped` 재개 조건 ①(**짝이온 확정**)에 이미 갖고 있다. 그 조건이 왜 필요한지의
**실물 근거가 이제 생겼다.**

## III-3. 덤 — Kang Figure 4c 축 단위 오기 (확인됨)

축 라벨 **"Adsorption energy (kJ mol⁻¹)"**, 축 범위 0.5 ~ −2.5, 본문 값 −2.24 eV.
−2.24 eV = **−216 kJ/mol** 이라 그 축에 안 들어간다. **단위 라벨이 틀렸다.**

## III-4. 두 논문이 같은 문제를 푼 두 방식

| | ICEP | Kang |
|---|---|---|
| 엔진 | **CASTEP DFT** (전하 지정 가능) | **PFP NNP** (전하 개념 없음) |
| 음이온기 처리 | **H 를 슬랩으로 옮겨** 중성 유지 | **Na⁺ 짝이온**을 계에 넣어 중성 유지 |
| 상태 선언 | ⛔ 그림 라벨 `(−H)` 뿐, 본문 무언급 | 🟡 `PC_2Na / 1Na / 0Na` 로 이름에 박음 — **단 사후 명명** |
| 상태별 논의 | ⛔ 없음 | ✅ 세 값을 본문에서 비교 |
| 자기상태 정책 | ⛔ 없음 (spin-pol + U 인데) | 해당 없음 (NNP) |
| 무엇이 실제로 결합하나 | 술포네이트 ↔ 표면 O (본문 서술) | 🔴 **Na⁺ 브리지** — 음이온기는 표면에 안 닿는다 (논문 미언급) |

**두 방법 다 "중성을 유지한다" 는 같은 원칙**을 지킨다. 갈리는 것은
**그 상태를 이름 붙여 선언했는가**다 — 다만 Kang 의 우위는 **"사후 명명" 까지**다.
Fig S15 가 사후분류를 확정했으므로 *"결과 전에 상태를 선언했다"* 는 등급은 줄 수 없다.
ICEP 는 그 명명조차 없고, 그 선택이 −2.243 vs −1.819 = **0.424 eV** 를 가른다.

---

## Counter-arguments (보존)

**반론 ①** — "NNP 도 훈련셋에 이온성 계가 있으면 국소 전하를 흉내 낼 수 있다."
→ 부분적으로 타당하다. 다만 **총전하를 입력으로 받지 않으므로** 같은 원자배열의
중성/음이온 두 상태를 **구별해 줄 수 없다.** 값이 틀렸다는 뜻이 아니라
**어느 상태를 잰 것인지 말할 수 없다**는 뜻이다.

**반론 ②** — "슬랩이 전자를 받아 주므로 중성으로 돌려도 자동으로 옳은 상태가 된다."
→ 배영진 논지. **ICEP 에서는 이게 맞았다** (§1-3 캡션). 다만 그렇다면 그 막대는
흡착에너지가 아니라 **반응에너지**이고, 같은 축에 올릴 때 **그렇게 말해야** 한다.

**반론 ③** — "논문들이 다 이렇게 한다. 우리가 과하게 판다."
→ 관행인 것은 맞다. 그러나 이번 판독에서 **우리 초판이 틀렸던 것도 같은 이유**다 —
그림만 보고 판정했다. SI 한 줄이 결론을 뒤집었다. **관행을 근거로 삼든 그림을 근거로
삼든, 원문을 안 보면 틀린다**는 것이 이번 교훈이다.

**반론 ④ (신규)** — "그럼 ICEP 그림에 문제가 없는 것 아닌가?"
→ 뺄셈은 정의된다. 그러나 **`(−H)` 만 반응 좌표가 다른데 축이 그걸 안 말한다**,
**본문이 그 막대를 아예 안 다룬다**, **환원된 TM 의 스핀 상태 선택 규칙이 없다** —
세 가지는 그대로 남는다.

---

## Gap

- **ICEP `(−H)` 의 기준 분자**가 SI 에 명시되지 않았다 (§II-1 (a) 는 추론).
- Figure S13 **그림 자체**를 못 봤다 — 표면 O–H 결합 위치와 H 이동 후 국소 구조 미확인.
- ICEP 슬랩의 **자기 배열·환원 TM 의 스핀 상태** 미기재.
- Kang 의 Na 상태 분류가 사전 설계인지 사후 분류인지 미확정 (SI Fig S15).
- **`U_PCET` 의 산화물 슬랩 버전이 없다.** 이 지적을 우리 계에 쓰려면 만들어야 한다.
- 두 논문 다 **오차막대·시드 없음.**
