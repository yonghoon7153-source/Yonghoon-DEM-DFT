# Cronau 2021 (ACS Energy Lett. 6, 3072−3077) — Stack-pressure 딜레마: 미세결정 황화물 SE의 "신뢰할 수 있는" σ_ion 측정법

> slug `cronau2021_stack_pressure_ionic_conductivity` · DOI `10.1021/acsenergylett.1c01299` · type `experiment` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_cronau2021_stack_pressure_ionic_conductivity.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** M. Cronau, M. Szabo, C. König, T. B. Wassermann, B. Roling\*,
"How to Measure a Reliable Ionic Conductivity? The Stack Pressure Dilemma of
Microcrystalline Sulfide-Based Solid Electrolytes," *ACS Energy Letters*
**2021**, *6*, 3072−3077. DOI 10.1021/acsenergylett.1c01299.
Philipps-Universität Marburg (Roling 그룹). **Viewpoint** (6쪽). Open Access
(ACS AuthorChoice). Received 2021-06-23 / Accepted 2021-08-04.

**소재:** 황화물(thiophosphate) SE **6종**, **3개의 결정도 클래스(class)** ×
조성으로 구성. 우리 LPSCl(Li₆PS₅Cl)과 같은 **황화물(sulfide)** 패밀리 — 따라서
LIB 논문들과 달리 σ_grain은 **직접 전사 가능**한 시스템이다. 단, ⚠ **본 논문에
single-crystal Li₆PS₅Cl 측정은 없다**(아래 PROVENANCE §0 참조).

동반 데이터 파일:
- `docs/data/cronau2021_stack_pressure_ionic.csv` — Fig 2/3/4 디지타이즈 (TREND 전용, 근사).
- 기존 `docs/data/lpscl_electrolyte_params.md` 의 "exact single-crystal digit NOT verified
  (proxy)" 플래그를 본 digest가 **해소**한다 (→ §0 / §8).

---

## ★★★ §0. PROVENANCE 판정 (미션 핵심) — 가장 먼저 읽을 것 ★★★

우리 σ_ionic 생산식(Stage-E, T1)은 이 논문을 **두 군데**에서 근거로 든다:
`σ_grain = 3.0 mS/cm` ("Cronau 단결정 LPSCl") 와 `Cronau(r_SE)` sub-µm 3-시그모이드.
본 PDF를 전수 정독한 결과, 두 귀속 모두 **부분적으로 부정확**하다. 정직한 판정:

### (A) σ_grain = 3.0 mS/cm 의 출처 판정 → **이 논문에 그 숫자는 없다 (오귀속/연도 오기)**

| 질문 | 판정 |
|---|---|
| 3.0 mS/cm 이 본문/그림/표에 **직접** 나오는가? | ✗ **아니오.** "3.0 mS/cm" 라는 숫자는 본 논문 어디에도 없다. |
| **single-crystal Li₆PS₅Cl** 을 측정했는가? | ✗ **아니오.** 본 논문은 **단결정을 측정한 적이 없다.** 6종 모두 **분체-압분체(powder pellet)** — amorphous / glass-ceramic / **micro**crystalline. "single crystal" 이라는 단어는 논문에 **등장하지 않는다.** |
| Li₆PS₅**Cl** 자체를 측정했는가? | ✗ **아니오.** Cl-argyrodite는 **intro 인용**(ref 4 Feng, ref 13)으로만 언급. 측정한 argyrodite는 **Li₆PS₅Br** (Br!) 이다. 측정 6종: AM-Li₇P₃S₁₁, AM-80Li₂S·20P₂S₅, GC-Li₇P₃S₁₁, **GC-Li₆PS₅Br**, **µC-Li₆PS₅Br**, µC-Li₁₀GeP₂S₁₂. |
| 연도 "Cronau **2022**" (우리 코드/baseline) 가 맞는가? | ✗ **틀림.** PDF 명시 = **2021** (Received 2021-06-23, ACS Energy Lett. 2021, 6, 3072). 우리 docs의 "Cronau 2022"는 **본 2021 논문의 연도 오기**이다 (별도 Cronau 논문이 아님 — DOI 1c01299 동일). |

**그렇다면 3.0 mS/cm 의 진짜 출처는?** 본 논문이 측정한 값들 중 우리 LPSCl에 가장
가까운 µC-Li₆PS₅Br (Br-argyrodite, 미세결정) 의 **고압-plateau σ ≈ 2.0–2.4 mS/cm**
(Fig 2e, 486 MPa 제작 + 고 stack pressure)이다. 즉 **3.0 은 "이 논문이 준 단결정
값"이 아니라, 이 논문의 미세결정 Br-argyrodite plateau(~2.4) 와 다른 LPSCl 문헌
(예: cold-press 1–3, 소결 3–6 mS/cm; `lpscl_electrolyte_params.md`)을 종합한
프로젝트 채택값**이다. 본 논문은 그 **상한 근거(미세결정도 고압에서 ~2.4까지 도달)**
는 제공하지만, "3.0 single-crystal" 이라는 **정밀 라벨은 지지하지 않는다.**

> **재귀속 권고:** 코드 주석 `σ_grain = 3.0 mS/cm "Cronau 2022 Li6PS5Cl single-crystal"`
> →  `σ_grain = 3.0 mS/cm — LPSCl grain-interior 프로젝트 채택값. 근거: Cronau **2021**
> (µC-Li₆PS₅**Br** 고압 plateau ~2.0–2.4 mS/cm, 본 논문) + cold-press/소결 LPSCl 문헌
> 1–6 mS/cm 종합. ⚠ single-crystal LPSCl 직접측정 아님.`
> 이는 `lpscl_electrolyte_params.md`가 이미 단 플래그("exact single-crystal digit
> NOT verified (proxy)")를 **확정**해준다 — 본 정독으로 그 플래그는 "확인됨: 단결정값
> 아님" 으로 닫힌다.

### (B) Cronau(r_SE) sub-µm 크기 인자의 출처 판정 → **(c) 느슨함 / 재명명 필요 (measured 아님, defensible-하지만-class-기반)**

논제에서 요구한 a/b/c 중 답:

| 옵션 | 판정 |
|---|---|
| (a) sub-µm 입자반경 → σ 감소가 본 논문에 **직접 측정**되어 있다 | ✗ **아님.** 본 논문은 **입자 반경(particle radius) r 의 함수로 σ 를 측정하지 않았다.** σ 의 독립변수는 **(i) stack pressure, (ii) fabrication pressure, (iii) 결정도 클래스(AM/GC/µC)** 뿐이다. r_SE → σ 곡선·표·breakpoint(0.03/0.1/0.3/0.5 µm)는 **논문에 존재하지 않는다.** |
| (b) 결정도/GB 논증의 **방어 가능한 외삽**이다 | △ **부분적.** 본 논문의 핵심 메커니즘 — "µC 입자는 서로 **소결(sinter)되지 않아** grain 사이에 gap/pore가 남고, 이것이 σ 를 낮춘다; pressure가 그 gap을 닫아야 한다" — 은 "미세결정성 → grain contact 불량 → σ 감소" 라는 **방향성**을 강하게 지지한다. 우리 인자가 "미세결정 → σ↓" **부호**를 옳게 잡은 점은 이 논문이 뒷받침한다. **그러나 그것은 입자크기 r 의 연속함수가 아니라 결정도 클래스의 이산(discrete) 효과**이다. |
| (c) 느슨하게 귀속됨 | ✅ **이것이 가장 정직한 판정.** 3-시그모이드의 **구체적 breakpoint(0.5/0.3/0.1/0.03 µm)와 plateau(1.0/0.90/0.65/0.33)** 는 본 논문에서 **측정·도출된 적이 없다.** 이 값들은 (아마도) 다른 출처 또는 프로젝트 경험에서 왔고, 본 논문은 그 **정성적 방향(미세결정·sub-µm → σ↓)** 만 보증한다. |

> **재명명 권고:** `Cronau(r_SE)` 인자의 물리적 의미를 **"입자크기 σ_grain 감쇠"**가
> 아니라 **"결정도/grain-contact 효율 인자"**로 재명명하라. 본 논문의 메커니즘은
> _입자가 작아서_ σ 가 낮은 게 아니라, _미세결정이 소결 안 되어 grain-boundary contact가
> 나빠서_ σ 가 낮은 것이다 (amorphous/GC는 가압-소결되어 이 문제가 없다). breakpoint
> 수치(0.5/0.3/0.1/0.03 µm)는 "Cronau가 측정" 이 아니라 **"미세결정-GB 논증을 따른
> 경험적 sub-µm 외삽"** 으로 정직하게 표기. (Trevisanello digest가 σ_S/σ_P 오귀속을
> 잡아낸 것과 동일한 정밀도.)
>
> **단, 인자를 폐기할 필요는 없다.** 부호와 정성적 메커니즘은 이 논문이 강하게 지지하고,
> LOOCV +0.0043 의 실측 개선도 있으므로 — **유지하되 라벨/근거만 정직화**하면 된다.

### (C) 한 줄 요약
- **연도:** 2021 (우리 "2022"는 오기, 같은 DOI).
- **σ_grain=3.0:** single-crystal LPSCl 직접값 **아님**. 본 논문 µC-Li₆PS₅Br plateau(~2.4) + 타 LPSCl 문헌(1–6) 종합 채택값. 사용 자체는 합리적, **라벨만 부정확**.
- **Cronau(r_SE):** sub-µm 반경 법칙은 본 논문에 **없음**. 본 논문은 **결정도-클래스·압력** 효과. 인자의 **방향(미세결정→σ↓)은 지지**, **breakpoint 수치는 미지지** → **(c) 느슨, 재명명 권고.**

---

## 1. 동기 / 핵심 질문 (Intro)

ASSB가 LIB 대비 (i) Li-metal 음극으로 부피에너지밀도 ~70 %↑, (ii) 불연성 SE로
화재위험↓ 의 두 이유로 유망. 황화물 SE는 합성 쉽고 액체전해질에 필적하는 Li⁺ σ 를
내는 가장 유망한 클래스. 본 Viewpoint가 던지는 질문:

> **"보고된 σ_ion 값을 어떻게 믿을 것인가?"** 같은 소재라도 **(1) 펠릿 제작 시 압력
> (fabrication pressure) 과 (2) σ 측정 시 셀에 가하는 압력 (stack pressure) 에 따라
> σ 가 크게 달라진다.** 특히 **비-어닐링(non-annealed) 시료**에서 문헌값 산포가 극심하다.**

핵심 동기 사실 (intro에서 인용):
- **Tatsumisago et al. (ref 21):** amorphous 75Li₂S·25P₂S₅ 는 **fabrication pressure**
  를 높이면(펠릿 압축) σ 가 크게 증가.
- **Meng et al. (ref 22, Doux 2020):** crystalline Li₆PS₅Cl 는 **fabrication pressure
  AND stack pressure** 둘 다 높이면 σ 가 유의하게 증가.
- ★ **Round-robin (ref 23, Ohno/Zeier 2020 interlab study):** **같은 합성 배치**의
  같은 소재를 **8개 연구실**이 각자의 프로토콜로 측정 → σ 산포가 **약 1 order of
  magnitude (10배)**. (→ 우리 σ_ionic 포락선 ~0.03–0.14 mS/cm 의 lab-간 허용오차
  논증과 직결, §6.)

**연구 갭:** 위 선행연구들은 amorphous **또는** crystalline 한쪽에 집중. 본 논문은
**amorphous (AM) / glass-ceramic (GC) / microcrystalline (µC)** 세 클래스를
**fabrication pressure × stack pressure** 평면에서 **체계적·동시** 비교한 최초.

**다루는 4개 황화물 sub-class (intro):**
1. LGPS형 결정질 Li₁₀MP₂S₁₂ (M=Ge,Sn)
2. argyrodite형 결정질 Li₆₋ₓPS₅₋ₓCl₁₊ₓ ← (우리 시스템 패밀리; 단 **본 논문 측정은 Br**)
3. glass-ceramic, 예: Li₇P₃S₁₁
4. amorphous Li₂S–P₂S₅, Li₂S–P₂S₅–LiI

---

## 2. 측정 소재 6종과 클래스 정의 (Methods)

ball-milling 으로 제작. 합성 직후(as-prepared) 상태에 따라 클래스가 갈린다:

| 클래스 | 정의 (논문) | 본 논문 측정 소재 |
|---|---|---|
| **AM (amorphous)** | 합성 직후 대부분 **비정질**. | AM-Li₇P₃S₁₁, AM-80Li₂S·20P₂S₅ |
| **GC (glass-ceramic)** | 비정질 매트릭스 + **nanocrystallite** 부분결정화. Li₇P₃S₁₁ 은 ~260 °C **저온 어닐링**으로 AM→GC 전환. | GC-Li₇P₃S₁₁, GC-Li₆PS₅Br |
| **µC (microcrystalline)** | **고온 어닐링(~550 °C)** 으로 고결정화 → **micron-크기 결정립**. | µC-Li₁₀GeP₂S₁₂, µC-Li₆PS₅Cl(준비됨), µC-Li₆PS₅Br, µC-Li₅.₅PS₄.₅Cl₁.₅ |

★ 본 논문 결과의 **중심 대비**는 **{AM, GC} (비정질상 함유) vs µC (완전결정·micron-grain)**.
- AM·GC: 비정질 입자가 fabrication pressure로 **소결(sinter)·치밀화** → grain 사이 결합.
- µC: micron 결정립이 **소결되지 않음**(서로 안 붙음) → grain 사이 gap/pore 잔존.

**측정 셋업 (Methods):**
- SE 펠릿을 두 **tungsten-carbide(WC) 전극** 사이에 끼움. 펠릿 면에 metal film(미스퍼터)
  또는 sputtered metal. **최대 ~500 MPa** stack pressure 인가.
- 대안: 펠릿 면에 metal film을 **sputter** 한 뒤 전용 셀에서 **낮은 stack pressure
  (~10 MPa)** 로 측정 (전극접촉 확보됨).
- σ 는 **stack pressure 의 함수**로 plot (각 fabrication pressure 별 곡선).

---

## 3. Figure 1 — 압력의존 형태(morphology) 모식도 (논문의 중심 그림)

논문 1쪽 우측. **fabrication pressure 가 µC vs AM/GC 입자에 미치는 형태변화** 만화.

| 구분 | High fabrication pressure 일 때 | High fabrication pressure 해제(release) 후 |
|---|---|---|
| **µC (microcrystalline)** | micron 결정립들이 압력으로 가까워지나 **서로 소결 안 됨** (boundary 유지). | 압력 해제 → 결정립 사이 **gap/pore 다시 벌어짐** → grain contact 손실. |
| **AM / GC (amorphous·glass-ceramic)** | 비정질 입자가 **pressure-induced sintering** → 입자끼리 융합·치밀화. | 소결은 **비가역(irreversible)** → 압력 해제해도 **치밀상태 유지**. |

**캡션 핵심 (그대로):** "while the particles in amorphous or glass ceramic materials
undergo a **pressure-induced sintering process**, the microcrystalline particles are
**only densified** by the fabrication pressure, **but not sintered together**. This
distinct morphology exerts a strong influence on the Li⁺ ion conductivity after
**release** of the fabrication pressure."

→ ★ **이것이 (B) Cronau(r_SE) 인자의 진짜 물리다:** µC(미세결정)의 낮은 effective σ 는
**"입자가 작아서"가 아니라 "소결 안 되어 grain-boundary contact가 나빠서"**다.
우리 인자가 "미세결정→σ↓" 부호를 옳게 잡은 근거가 바로 이 그림 — 단 **r 의 함수가
아니라 클래스(소결가능성)의 함수**라는 점이 핵심 차이.

---

## 4. Figure 2 — σ_ion vs Stack Pressure (6 패널, 핵심 데이터)

6개 소재 각각에 대해 **5개 fabrication pressure** (97.34 / 194.69 / 292.03 / 389.30 /
486.73 MPa) 별로 σ vs **stack pressure** (0–500 MPa) 곡선. 배경 색띠 = 거동 regime.

### 패널별 (a)–(f) — 디지타이즈 TREND 값 (★ 근사, 그림에서 읽음)

| 패널 | 소재 | 클래스 | y축 단위 | 고압-plateau σ (최고 fab.) | regime 띠 |
|---|---|---|---|---|---|
| (a) | Li₇P₃S₁₁ | AM | S/cm (×10⁻⁴) | ~2.0–2.5 ×10⁻⁴ S/cm = **~0.20–0.25 mS/cm** | red→green |
| (b) | 80Li₂S·20P₂S₅ | AM | S/cm (×10⁻⁴) | ~6 ×10⁻⁴ S/cm = **~0.6 mS/cm** | red→green |
| (c) | Li₇P₃S₁₁ | GC | **mS/cm** (×10⁻³ 표기) | ~2.0–2.5 ×10⁻³ S/cm = **~2.0–2.5 mS/cm** | red→green |
| (d) | Li₆PS₅Br | GC | S/cm (×10⁻⁴) | ~8–9 ×10⁻⁴ S/cm = **~0.8–0.9 mS/cm** | red→green |
| (e) | **Li₆PS₅Br** | **µC** | S/cm (×10⁻³) | ~2.0–2.4 ×10⁻³ S/cm = **~2.0–2.4 mS/cm** ★ | red→**yellow**→green |
| (f) | Li₁₀GeP₂S₁₂ | µC | S/cm (×10⁻³) | ~5–6 ×10⁻³ S/cm = **~5–6 mS/cm** | red→**yellow**→green |

> ⚠ y축 prefactor 가 패널마다 다르다(×10⁻⁴ vs ×10⁻³) — 절대 비교 시 주의. 위 값은
> 그림 눈금에서 읽은 **TREND 근사**이며 false precision 금지.

### 거동 regime (배경 색)의 의미 (본문)

- **red regime (저 stack pressure, ~0–30/50 MPa):** **모든** 소재에서 σ 가 stack
  pressure 와 함께 **급격히 상승**. 원인 = **펠릿/WC전극 접촉 불량** (전극접촉 인공물,
  소재 본질 아님). → 이 구간 σ 는 **신뢰 불가**.
- **green regime (AM·GC, stack pressure > 30–50 MPa):** σ 가 **거의 일정(plateau)** →
  전극접촉 충분 → **참(true bulk) σ 에 근접**. **stack pressure 무관.**
- ★ **yellow regime (µC만, ~50–200/250 MPa):** **두 번째** stack-pressure 의존 구간.
  σ 가 약하지만 **계속 상승** (green처럼 평평해지지 않음). 원인 = µC 결정립 사이의
  **gap/pore 를 닫으려면 추가 stack pressure 필요**. µC 는 ~200–250 MPa **이상**에서야
  비로소 plateau (green).

**핵심 대비 (본문):**
- **AM·GC:** stack pressure > ~50 MPa 면 σ plateau (stack-pressure 무관). **σ 는 주로
  fabrication pressure 에 의해 결정**(비가역 소결로 치밀도 고정).
- **µC:** stack pressure 의존성이 **훨씬 강함**(yellow regime). fabrication pressure
  의존성은 **훨씬 약함** (소결 안 되므로 fab.로 치밀화가 잘 안 됨).

---

## 5. Figure 3 — σ_ion vs Fabrication Pressure (GC vs µC 직접대비)

GC-Li₆PS₅Br (a) 와 µC-Li₆PS₅Br (b) 를 **fabrication pressure(0–500 MPa)** 축으로 plot,
**4개 stack pressure** (5 / 50 / 100 / 300 MPa) 별 곡선. (Fig 2와 축을 바꾼 cut.)

### (a) GC-Li₆PS₅Br
- stack pressure **5 MPa**(낮음): fabrication pressure 올려도 σ 가 오히려 **감소**처럼
  보임 — 본문 설명: 저 stack pressure 에서는 전극접촉 불량이 지배 → **비재현 접촉의
  인공물**(σ 의 겉보기 감소는 실제 아님).
- stack pressure **≥ 50 MPa**: σ 가 **fabrication pressure 와 함께 명확히 상승**
  (~3×10⁻⁴ → ~9×10⁻⁴ mS/cm). 펠릿 **치밀화(densification)** + 비정질입자 **소결**로
  tortuosity↓·입자간 장벽↓. 400–500 MPa 에서 fab. 의존성이 약화(leveling, 밀도 포화).
- ★ σ 가 **stack pressure 5→50 MPa 에서 사실상 동일**(50 이상 plateau) = **GC 는
  stack-pressure 무관**(전극접촉만 확보되면).

### (b) µC-Li₆PS₅Br
- 모든 stack pressure 에서 fabrication pressure 의존성이 **GC 보다 훨씬 약함**(거의
  평탄) → micron 결정립이 fab. 압력으로 **소결되지 않으므로** 치밀화 효과가 작다.
- 대신 **stack pressure 가 곡선을 위로 평행이동** → µC 는 **stack-pressure 가 σ 의
  주 레버**(yellow regime 의 그림-3 표현).

→ ★ **(B) 인자의 핵심 증거:** **같은 조성(Li₆PS₅Br)**, 결정도만 다를 때(GC vs µC)
σ-압력 거동이 **질적으로 다르다.** GC(부분비정질)는 fab.로 소결·치밀 → 높고 안정한 σ;
µC(완전결정·소결불가)는 fab. 둔감·stack 민감 → 압력 해제시 grain gap 으로 σ 손실.
**"미세결정 = 페널티"** 는 입자크기가 아니라 **소결가능성(=비정질상 함유 여부)** 의 문제.

---

## 6. Figure 4 — FIB-SEM 단면 (메커니즘의 직접 시각증거 + ★ 절대 σ 숫자)

4개 대표 펠릿의 FIB 단면 SEM. **여기 캡션에 본 논문에서 가장 신뢰할 σ 절대값들이 명시됨**:

| 패널 | 시료 | fabrication pressure | **Li⁺ σ (캡션 명시값)** | 형태 관찰 |
|---|---|---|---|---|
| (a) | GC-Li₆PS₅Br | **98 MPa** | **0.15 mS/cm** | 다공성·입자경계 보임 |
| (b) | GC-Li₆PS₅Br | **392 MPa** | **0.65 mS/cm** | **치밀화**, 비정질입자 **융합**·크기증가 (소결) |
| (c) | µC-Li₆PS₅Br (**펠릿어닐링 전**) | 392 MPa | **0.59 mS/cm** | micron 결정립 **개별 식별**, **서로 안 붙음(미소결)** |
| (d) | µC-Li₆PS₅Br (**550 °C 펠릿어닐링 후**) | 392 MPa | **2.40 mS/cm** ★ | 결정립 **소결됨** → σ **4×↑** |

**메커니즘 결론 (본문):**
- **GC (a)→(b):** fabrication pressure 98→392 MPa → 비정질입자 **pressure-induced
  sintering** → 입자 융합·크기↑ → 치밀화 → σ 0.15→0.65 mS/cm (**~4.3×**). 이 소결은
  **비가역** → 압력 해제 후에도 치밀상태·높은 σ 유지.
- **µC (c):** fabrication 392 MPa 로도 micron 결정립이 **소결 안 됨** (단면에서 결정립
  사이 경계 뚜렷). 원인 추정 = **결정립 간 격자방위 불일치(lattice misorientation)**
  로 소결 방해. → fab. 압력 해제시 **gap/pore 형성** → σ 측정 중 stack pressure 로 그
  gap 을 닫아줘야 함(yellow regime).
- **µC (d):** 펠릿을 **550 °C 추가 어닐링** → 결정립 **소결** → σ 0.59→**2.40 mS/cm**
  (**~4×↑**). = µC 도 **열처리하면** GC 수준 σ 도달 가능 (단 압력만으로는 불가).

★ **(A) σ_grain 출처 정밀화:** 본 논문의 **µC-Li₆PS₅Br 최고 σ = 2.40 mS/cm**
(어닐링 펠릿, Fig 4d) = 이 논문이 보고하는 LPSCl-친척(argyrodite)의 **최선 plateau**.
우리 채택 **3.0** 은 이보다 **약간 높고**(Br→Cl 차이 + 소결/단결정 외삽 + 타 문헌 1–6
종합), 따라서 "이 논문이 3.0 을 줬다"가 아니라 "이 논문이 **상한 ~2.4** 를 주고, 우리가
약간 위로 채택" 이 정확한 서술이다.

---

## 7. Figure 5 — "신뢰할 수 있는 σ 측정" 프로토콜 (논문의 처방, 4 시나리오)

µC vs AM/GC 형태를 4개 압력시나리오로 만화화. **green hook(✓) = 신뢰값, red X(✗) =
비신뢰값.** "측정 프로토콜을 어떻게 짜야 참 bulk σ 에 가까운가"의 시각 가이드.

| 시나리오 | µC (미세결정) | AM/GC (비정질함유) |
|---|---|---|
| **Low fab. & low stack** | ✗ (gap 안닫힘 + 전극접촉 불량) | ✗ (치밀화 부족 + 전극접촉 불량) |
| **High fab. & high stack** | ✓ (gap 닫힘) | ✓ (소결·치밀 + 접촉확보) |
| **Low stack after high fab.** | ✗ (압력해제 → gap 다시 열림) | ✓ (소결 비가역 → 치밀 유지) ★ |
| **Annealed pellet under low stack** | ✓ (어닐링으로 결정립 소결됨) | ✓ |

★ 결정적 칸 = **"Low stack after high fabrication"**: AM/GC 는 ✓ (소결 비가역이라
저 stack 에서도 참값), µC 는 ✗ (소결 안 됐으니 압력 풀면 gap 재형성 → σ 손실).
이 한 칸이 µC 와 AM/GC 를 가르는 본질.

### 논문의 측정 프로토콜 처방 (본문 요약)

- **AM / GC:** fabrication pressure **400–500 MPa** 로 강하게 압축(비가역 치밀화 확보)
  → 그 뒤 σ 측정은 **낮은 stack pressure** 면 충분. metal sputter 전극이면 **5–10 MPa**,
  WC 직접접촉이면 **~30–50 MPa** 면 plateau(참값).
- **µC:** 압력만으론 소결 안 되므로 두 갈래:
  - (i) 펠릿 면 metal **sputter 없이**: σ 측정 중 **stack pressure 200–250 MPa 이상**
    필요(grain gap 강제로 닫기).
  - (ii) **펠릿 어닐링(550 °C) + metal sputter** 후: **5–10 MPa** 저 stack 으로 충분.
- **요지:** **고 fabrication pressure(400–500)는 필수**(치밀화), 그러나 **σ 측정 시
  stack pressure 는 — 비가역치밀이 됐다면 — 낮게**(전극접촉만). µC 는 어닐링 없이는
  이 "저 stack 신뢰값" 이 불가능.

### ASSB 적용 함의 (본문, 우리와 직결)

- 고에너지밀도엔 **Li-metal 음극** → 운전 stack pressure 를 **100 MPa 충분히 아래**로
  유지해야 함 (ref 25 Doux). → 그런데 **µC 는 저 stack 에서 σ 가 낮음**(gap) → **µC 는
  ASSB 운전조건에서 잠재력 발휘 못 함.** AM/GC 가 유리.
- 단 ASSB 내부 SE 입자는 **고온 어닐링 불가**(바인더·CAM 의 열안정성 한계) → µC 를
  ASSB 안에서 소결시킬 수 없음 → "µC 는 ASSB 에서 최대 σ 도달 어렵다"고 결론.

---

## 8. 핵심 숫자 총정리 (본 논문에서 실제로 측정/명시된 값만)

| 항목 | 값 | 출처(논문 위치) | digitized? |
|---|---|---|---|
| GC-Li₆PS₅Br σ @ 98 MPa fab. | **0.15 mS/cm** | Fig 4a 캡션 | 명시(stated) |
| GC-Li₆PS₅Br σ @ 392 MPa fab. | **0.65 mS/cm** | Fig 4b 캡션 | 명시 |
| µC-Li₆PS₅Br σ @ 392 fab., 어닐링 **전** | **0.59 mS/cm** | Fig 4c 캡션 | 명시 |
| µC-Li₆PS₅Br σ @ 392 fab., 550 °C **어닐링 후** | **2.40 mS/cm** ★ | Fig 4d 캡션 | 명시 |
| µC-Li₆PS₅Br plateau (고 fab., 고 stack) | ~2.0–2.4 mS/cm | Fig 2e | digitized(근사) |
| µC-Li₁₀GeP₂S₁₂ plateau | ~5–6 mS/cm | Fig 2f | digitized |
| GC-Li₇P₃S₁₁ plateau | ~2.0–2.5 mS/cm | Fig 2c | digitized |
| AM-80Li₂S·20P₂S₅ plateau | ~0.6 mS/cm | Fig 2b | digitized |
| AM-Li₇P₃S₁₁ plateau | ~0.2–0.25 mS/cm | Fig 2a | digitized |
| GC-Li₆PS₅Br plateau (Fig 2d) | ~0.8–0.9 mS/cm | Fig 2d | digitized |
| red→green 전이 (전극접촉 확보) | stack pressure **~30–50 MPa** | 본문/Fig 2 | 명시 |
| µC yellow regime 폭 | stack ~**50→200–250 MPa** | 본문/Fig 2e,f | 명시 |
| µC plateau 도달 stack pressure | **> 200–250 MPa** (어닐링 없을 때) | 본문 | 명시 |
| AM/GC 권장 fabrication pressure | **400–500 MPa** | 본문/Fig 5 | 명시 |
| AM/GC 권장 측정 stack (sputter 전극) | **5–10 MPa** | 본문 | 명시 |
| AM/GC 권장 측정 stack (WC 직접) | **~30–50 MPa** | 본문 | 명시 |
| 측정 fabrication pressure 세트 | 97.34 / 194.69 / 292.03 / 389.30 / 486.73 MPa | Fig 2 범례 | 명시 |
| inter-lab σ 산포 (round-robin, ref 23) | **~1 order of magnitude (10×)**, 8개 연구실 | intro | 명시(인용) |
| ★ **3.0 mS/cm** (우리 σ_grain) | **본 논문에 없음** | — | **오귀속** |
| ★ **single-crystal LPSCl σ** | **본 논문에 없음** (단결정 미측정, Cl 미측정) | — | **오귀속** |
| ★ **r_SE → σ sub-µm 법칙** | **본 논문에 없음** (압력·클래스만) | — | **미지지** |

---

## 9. 비교 vs 우리 DEM+MPM (focused §)

### 9-1. σ_grain = 3.0 mS/cm — 값과 조건 판정
- **값 출처:** 위 §0/§6 — 본 논문은 **3.0 도, single-crystal LPSCl 도 주지 않는다.**
  가장 가까운 측정은 **µC-Li₆PS₅Br 어닐링 σ = 2.40 mS/cm** (Br, 미세결정-소결).
  우리 3.0 은 **이 ~2.4 + 타 LPSCl 문헌(cold-press 1–3, 소결 3–6)** 의 종합 채택값.
- **GB 포함 여부:** 본 논문 값은 **전부 압분체(pellet) σ** = **grain-boundary 포함**.
  단결정(GB 제거) σ 가 **아니다.** 따라서 우리 σ_grain 을 "grain-interior(단결정)"
  로 부르는 것은 **물리적으로도 부정확**(이 논문값은 GB-inclusive). Bazzoun digest 의
  "pellet 1.02 mS/cm (GB-incl) < Cronau 단결정 3.0" 대비와 일관되게, **"3.0 은
  GB-제거된 grain-interior가 아니라 잘-소결된 압분체 plateau의 상단"** 으로 봐야 한다.
- **stack-pressure 특정값인가?** 본 논문의 모든 σ 는 **고 fabrication + plateau(고
  stack)** 조건. 즉 우리 3.0 은 "압력무관 본질 grain σ" 라기보다 **"최적압력에서
  달성가능한 최선 σ"** 에 가깝다. 우리 식이 이를 **포화 상한**처럼 쓰는 것은 합리적이나,
  "단결정 본질값" 이라는 함의는 과대.
- **판정:** **사용값 3.0 mS/cm 은 합리적 범위**(Br 2.4 ~ 소결 LPSCl 3–6 사이). **라벨만
  교정**: "Cronau **2021** µC-Li₆PS₅Br plateau(~2.4) + LPSCl 문헌 종합; single-crystal
  아님, GB-inclusive pellet 기준 상한."

### 9-2. Cronau(r_SE) sub-µm 인자 — measured / defensible / loose 판정
- **measured?** ✗ — 본 논문에 r 의존 σ 곡선 없음.
- **defensible?** △ — "미세결정·소결불량 → grain-contact↓ → σ↓" **부호·메커니즘은
  강하게 지지**(Fig 1/3/4/5 전체가 이 논증). 단 **이산 클래스 효과**(AM/GC vs µC)이지
  연속 r-법칙이 아님.
- **loose?** ✅ — 3-시그모이드 breakpoint(0.5/0.3/0.1/0.03 µm)·plateau(1/0.90/0.65/0.33)
  의 **구체적 수치는 본 논문에서 도출 불가**. 다른 출처/경험 추정.
- **판정·권고:** **인자 유지**(부호 옳음 + LOOCV +0.0043 실측 개선), 그러나
  (i) **라벨 재명명** → "결정도/grain-contact 효율 인자(Cronau 2021 미세결정-소결
  메커니즘 기반 경험적 sub-µm 외삽)", (ii) breakpoint 수치는 "Cronau 측정" 이 아니라
  "경험 외삽" 으로 정직 표기, (iii) 이상적으로는 **r 보다 "결정도/소결상태" 변수**
  (또는 합성 클래스 플래그)로 재파라미터화하는 것이 물리적으로 더 정확. (현 corpus 에
  sub-µm 케이스가 1개뿐이라 실측 구분 불가 → 당장은 라벨 교정으로 충분.)

### 9-3. stack pressure vs fabrication pressure — 우리 압력 스토리와 매핑 ★
이 논문의 **두 압력 구분**은 우리 DEM/MPM 의 **두 압력 단계**와 정확히 대응한다:

| Cronau 2021 | 의미 | 우리 모델 대응 |
|---|---|---|
| **fabrication pressure** (펠릿 제작, 400–500 MPa) | 비가역 치밀화·소결 결정 | 우리 **cold-press 300 MPa** (DEM/MPM compaction target). Minnmann 10 %@300 anchor. |
| **stack pressure** (운전·측정, 5–250 MPa) | 전극접촉·grain gap 폐쇄 (가역) | 우리 **운전 압력 40–70 MPa** + EIS 측정조건. |
| red regime 전이 ~30–50 MPa | 전극접촉 확보 임계 | — (우리는 전극접촉을 모델링 안 함; 우리 σ 는 내부 network) |
| µC yellow plateau > 200–250 MPa | grain gap 폐쇄 임계 | 우리 **DEM Heckel P_y = 138 MPa** / σ-saturation. Bazzoun·Varkey 의 "σ-vs-P 가 ~400 MPa 에서 포화"와 같은 계열의 knee. |

- ★ **E_eff softening 스토리 지지 여부:** **간접 지지.** 이 논문은 "압분체 σ 는 저
  stack 에서 grain-contact 불량으로 **본질값보다 낮게** 측정된다(전극·grain gap 인공물);
  고압에서야 참값 도달" 을 보인다. 우리 DEM 의 **18× E softening** 은 "강체구 DEM 이
  못 잡는 granular rearrangement/GB-slide/micro-fracture 를 effective modulus 로
  lumping" 하는 것 — **둘 다 "압력으로 닫히는 grain-contact 결함"이 σ/치밀화를
  지배한다는 같은 물리**를 다른 층위에서 본다. 단 **직접 정량매핑은 아님**(이 논문은
  σ-vs-stack 의 거시현상, 우리는 contact-network 의 미시모델).
- ★ **Heckel knee 매핑:** 우리 DEM Heckel **P_y = 138 MPa** + 운전 40–70 MPa 는, 이
  논문의 **"red→green 전이 30–50 MPa(접촉확보) / µC yellow 종료 200–250 MPa(gap폐쇄)"**
  사이에 위치. 즉 우리 운전압력대(40–70 MPa)는 **AM/GC 라면 plateau(참 σ), µC 라면
  아직 yellow(σ 미포화)** 구간 — **"우리 SE 가 AM/GC 처럼 거동해야 운전압에서 σ 가
  믿을만하다"** 는 함의. (우리 LPSCl 이 실제로 어느 클래스인지가 중요 → §10.)

### 9-4. inter-lab 1 order 산포 → 우리 σ 포락선 허용오차
- round-robin(ref 23) 의 **8-lab × 10배 산포**는, 우리 σ_ionic 포락선 **~0.03–0.14
  mS/cm** (Bazzoun exp anchor)·우리 식 LOOCV 0.975(median |err| ~7.7 %) 의 **정량
  맥락**을 준다: **문헌 σ 자체가 프로토콜로 10× 흔들리므로**, 우리 모델-실험 일치를
  "±몇 %" 가 아니라 **"이 lab-간 10× 산포 안에서 일관"** 으로 논증해야 정직하다. 즉
  **단일 "참 σ" 가 존재하지 않는다** — 압력·프로토콜 의존이라는 게 이 논문의 메시지.

### 9-5. 정직성 — 전사 가능성 (이건 우리 시스템이다)
- LIB 양극 논문들(Trevisanello 등)과 **결정적으로 다름:** 이건 **황화물 SE, 우리
  LPSCl 의 친척(argyrodite Li₆PS₅Br + LGPS + Li₇P₃S₁₁)**. → **σ_grain 의 절대값·압력
  거동은 직접 전사 가능**한 드문 논문.
- **단, 두 단서:** (i) 측정은 **Br-argyrodite**(우리는 **Cl**) — 같은 패밀리지만
  조성차로 σ 절대값 다름(Cl 가 보통 약간 더 높음). (ii) 값은 **GB-포함 압분체** σ —
  우리가 "grain-interior" 라 부르는 것과 물리적 층위가 다름(GB 미제거).
- ⇒ **σ_grain=3.0 의 사용은 정당, 라벨·연도만 교정.** Cronau(r_SE) 는 부호 정당,
  수치 외삽임을 명기.

---

## 10. 정직한 한계 / 우리가 주의할 점 (§10 critical caveats)

1. ★ **single-crystal 도, Cl-argyrodite 도, r-법칙도 본 논문에 없다** (§0). 우리 코드
   주석 3곳(`generate_comparison_plots.py` 근방 σ_grain 주석, `our_dem_baseline.md`,
   `lpscl_electrolyte_params.md`)의 "Cronau 2022 single-crystal Li6PS5Cl" 는 **연도
   오기 + 소재 오기 + 라벨 오기** 의 3중 부정확. 사용값 자체(3.0)는 합리적이나 **출처
   서술을 교정**해야 manuscript 에서 안전.
2. **클래스(소결가능성)가 입자크기보다 본질.** 본 논문의 σ 페널티는 "작은 입자"가
   아니라 "미세결정(=소결 안 되는 완전결정)" 때문. 우리 Cronau(r_SE) 가 **반경**을
   변수로 쓰는 한, 이 논문을 근거로 대는 것은 **메커니즘 불일치**(반경≠소결상태).
   다행히 "sub-µm→σ↓" 방향은 우연히 일치(작은 ball-milled 입자는 종종 미세결정·고결함).
3. **digitized vs stated 엄격구분:** Fig 4 캡션 4값(0.15/0.65/0.59/2.40 mS/cm)만
   **명시값**. Fig 2/3 plateau 는 **그림 눈금 근사(TREND)** — y축 prefactor 패널별
   상이(×10⁻⁴/×10⁻³)하니 false precision 금지.
4. **이건 SE-only 펠릿(blocking electrode) σ** — composite(CAM+SE) 도, transport
   network 도, 입자형상도 다루지 않음. **frame[5] 측면에서 이 논문은 "재료 σ_grain 의
   상한·압력의존" 만 주고**, 우리 DEM(contact-network transport)·MPM(morphology) 의
   어느 절반도 대체하지 않는다 — **재료 baseline 입력**일 뿐.
5. **우리 LPSCl 이 어느 클래스인가가 미해결:** 우리 LPSCl 이 ball-milled 미세결정(µC)
   이면, 운전압력 40–70 MPa(yellow 구간)에서 σ 가 **포화 안 됨**(이 논문). 우리 식의
   σ_grain=3.0 plateau 가정은 **"AM/GC 처럼 잘 소결된 SE"** 를 암묵 가정 — 실제
   ball-milled LPSCl 이 µC 라면 운전 σ 는 더 낮을 수 있다. (→ 우리 Cronau(r_SE)
   감쇠가 부분적으로 이걸 보정 중이라 볼 수도 있으나, 명시적 "클래스" 변수가 더 정확.)
6. **SI 미업로드:** Table S1(권장 측정조건 요약), Fig S1–S7(추가 AM/GC/µC σ-vs-압력,
   XRD, SEM)은 본 digest 범위 밖 — 본문 6쪽 기준. SI 의 정확한 σ 수치/추가 소재가
   §8 표를 더 채울 수 있음(추후 SI 입수 시 보강).

---

## 11. 우리 작업에 가장 날카로운 3가지 insight

1. ★ **provenance 교정 (manuscript-blocking):** σ_grain=3.0 의 주석을 "Cronau **2021**
   µC-Li₆PS₅**Br** plateau ~2.4 + LPSCl 문헌 종합 (single-crystal 아님, GB-inclusive)"
   로, 연도 2022→2021 로, "single-crystal" 라벨 제거로 교정. Trevisanello σ_S/σ_P
   오귀속과 **쌍을 이루는** 두 번째 출처-교정 항목. (값은 그대로 둬도 됨.)
2. ★ **Cronau(r_SE) 재명명·재근거:** "입자크기 σ 감쇠" → **"결정도/소결-grain-contact
   효율 인자"**. 부호·메커니즘은 이 논문이 강력 지지(Fig 1/3/4/5), **breakpoint 수치는
   경험 외삽** 명기. 이상적 개선 = r 대신 **합성-클래스/결정도 플래그**로 재파라미터화.
3. ★ **두 압력 구분을 우리 압력 스토리에 명시 도입:** fabrication(우리 300 MPa
   cold-press) vs stack(우리 40–70 MPa 운전) 를 분리하고, **운전압력대가 이 논문의
   "µC yellow(σ 미포화) / AM·GC green(σ 포화)" 어디에 떨어지는지**를 명시. 이는 (i)
   우리 E_eff softening(압력으로 닫히는 grain-contact 결함의 lumping)·(ii) Heckel
   P_y=138·(iii) Bazzoun/Varkey 의 σ-vs-P ~400 MPa 포화 knee 를 하나의 **"압력으로
   grain-contact 가 닫히며 σ 가 포화한다"** 서사로 묶는 결정적 문헌 앵커.

---

## 12. 미니 용어집 (technique glossary)

- **fabrication pressure (제작압력):** SE 분말을 펠릿으로 **압축**할 때 가하는 압력
  (본 논문 400–500 MPa 권장). 비정질·GC 에서는 **비가역 소결·치밀화**를 일으켜 σ 를
  영구히 높임. 우리의 cold-press 300 MPa 에 해당.
- **stack pressure (스택압력):** σ 를 **측정**할 때(또는 ASSB **운전** 시) 셀/전극에
  지속적으로 가하는 압력. 가역적 — 전극접촉·grain gap 폐쇄에 관여. 우리 운전 40–70 MPa.
- **microcrystalline (µC):** 고온(~550 °C) 어닐링으로 **micron 크기 결정립**이 된 SE.
  결정립끼리 **소결 안 됨**(격자방위 불일치) → 압력 해제시 grain gap → σ 손실. ASSB
  운전조건(저 stack)에서 불리.
- **glass-ceramic (GC):** 비정질 매트릭스 + nanocrystallite. fabrication pressure 로
  **비가역 소결** 가능 → 높고 안정한 σ. (Li₇P₃S₁₁ 은 저온 어닐링으로 AM→GC.)
- **amorphous (AM):** 합성 직후 대부분 비정질. GC 와 함께 **pressure-induced sintering**
  으로 치밀화.
- **pressure-induced sintering (압력유도 소결):** 비정질입자가 압력으로 표면에너지를
  낮추며 **융합·치밀화**하는 과정. **비가역** → 압력 해제 후에도 치밀상태 유지. (µC
  결정립은 이게 안 일어남.) → Fig 4a→4b 의 입자 융합·크기증가가 직접 증거.
- **stack pressure dilemma (제목의 딜레마):** "고 fabrication 으로 치밀화는 해야 하나,
  σ 측정/운전 시 stack pressure 를 얼마로? — µC 는 저 stack 에서 gap 으로 σ 가 낮고,
  AM/GC 는 (소결 비가역이라) 저 stack 으로도 참값" 이라는, **소재 클래스마다 답이 다른**
  측정-프로토콜 딜레마.
- **round-robin / interlaboratory study (ref 23):** 같은 시료를 여러 연구실이 각자
  측정 → 프로토콜 의존 산포 정량. 본 논문 인용값 = **8-lab, ~10× 산포**.
- **red/green/yellow regime:** Fig 2 배경색. red=전극접촉불량(σ 상승, 비신뢰),
  green=plateau(참값), yellow=µC 전용 2차 stack 의존(grain gap 폐쇄 중).

---

## 13. 한 줄 결론

Cronau **2021**(2022 아님)은 **우리 황화물 시스템 패밀리**(argyrodite Li₆PS₅Br + LGPS
+ Li₇P₃S₁₁, 단 **Cl/단결정 미측정**)에서 **σ 가 fabrication·stack 두 압력과 결정도
클래스(AM/GC vs µC)에 따라 ~10× 흔들린다**는 측정-신뢰성 Viewpoint. **우리 σ_grain=3.0
은 이 논문이 준 "단결정값"이 아니라 µC-Br plateau(~2.4)+LPSCl 문헌 종합 채택값(라벨
교정 필요)**, **Cronau(r_SE) 인자의 "미세결정→σ↓" 부호는 이 논문이 강력 지지하나
sub-µm 반경 breakpoint 수치는 미지지(재명명 필요)**, 그리고 **두 압력 구분은 우리
cold-press(300)/운전(40–70) · E_eff softening · Heckel P_y=138 압력 서사에 바로
들어맞는 결정적 앵커**다.
