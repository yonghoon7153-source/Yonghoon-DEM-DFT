---
title: "음이온성 바인더의 흡착에너지 — 탈양성자 상태를 어떻게 다루나 (ICEP vs Kang 대조)"
date: 2026-08-29
updated: 2026-08-29
tags: [binder, adsorption, charge-state, estimand, nnp, pcet, sdcp, literature]
status: 진행 — 두 논문 본문 판독 완료, ICEP SI 미확보
confidence: high
verificationStatus: partial
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
targetVenue:
---

## Thesis

바인더의 산성기(-SO₃H·-COOH)에서 H 를 뗀 구조로 흡착에너지를 재고 그것을 H 가 있는
구조의 값과 **같은 축에 올리면**, 두 막대의 차이는 "탈양성자화 효과" 가 아니라
**조성이 다른 두 분자의 값**이다. 물어야 할 양은 흡착에너지가 아니라 **양성자 이동
반응에너지**이고, 그건 양변 중성·조성 보존으로 정의된다.

---

## 0. 무엇을 봤고 무엇을 안 봤나

| 자료 | 상태 |
|---|---|
| **ICEP** — *Adv. Mater.* **2025**, 37, 2506266, 본문 p.3–15 | ✅ **직접 읽음** |
| ICEP **Supporting Information** (Figure S12·S13, Experimental Section) | ⛔ **미확보** — 계산 조건이 여기 있다 |
| **Kang** — *Adv. Mater.* **2025**, 37, 2416872, 본문 p.5–14 + **SI p.1–9** | ✅ **직접 읽음** |

⚠ ICEP 의 **계산 method(코드·범함수·전하 처리)는 본문에 없다.** 본문 어디에도
Experimental Section 이 없고 SI 로 넘어간다. 따라서 §1-3 은 **미확정**이다.

---

# I. ICEP 논문 (*Adv. Mater.* 2025, 37, 2506266)

## 1-1. 무슨 논문인가

- **ICEP** = ionically conductive elastic polymer. RAFT 로 만든 **삼블록**
  `P(AN-co-AMPS)-b-PEO₄₆-b-P(AN-co-AMPS)`, Mw ≈ 100 kDa.
- `[AN]/[AMPS]` 비로 **ICEP-5 / ICEP-8 / ICEP-19** 세 조성. **ICEP-8 채택**
  (x/y ≈ 8; 파단신율 283 %, 인성 601.2 J m⁻³ vs PVDF 31.8 % · 151.8 J m⁻³).
- 기능기 역할 배정: **AMPS 의 SO₃H = 빠른 Li 전도 + 수소결합**, **AN = 구조/기계 물성**,
  **PEO = 유연성 + Li 전도**, 아미드 **N–H = 수소결합**.
- 계: **NCM811** 양극, Li 금속 풀셀. 초고로딩 62.4 mg cm⁻², 12.7 mAh cm⁻².

## 1-2. ⭐ 본문의 DFT 단락은 **이것 하나가 전부다** (p.6 하단 → p.7 상단)

> "To further elucidate the molecular origins of this interfacial behavior, we conducted
> **density functional theory (DFT) calculations** to investigate the binding interactions
> between model segments of the ICEP and PVDF polymers and the NCM811 surface
> (Figure S12, Supporting Information). The ICEP structure was **dissected into two
> representative functional blocks, denoted as ICEP_AN and ICEP_AMPS**. Notably,
> **ICEP_AMPS exhibited a significantly stronger binding affinity to the NCM811 surface
> compared to PVDF**, primarily due to **robust hydrogen bonding between the sulfonate
> group and surface oxygen atoms** (Figure 2g and Figure S13, Supporting Information).
> These DFT calculation results provide direct theoretical support for the experimentally
> observed interfacial adhesion and cohesion achieved with ICEP-8 binder."

Figure 2g 캡션:

> "Binding energies and optimized structures of ICEP_AN, ICEP_AMPS, **ICEP_AMPS (-H)**,
> and PVDF on **NCM811 (001) surface**."

## 1-3. 여기서 확정되는 것 세 가지

### ① **`AMPS(−H)` 는 본문에 한 번도 안 나온다** ✅ 확정

본문은 *"**two** representative functional blocks, denoted as ICEP_AN and ICEP_AMPS"* 라고
쓴다. **둘**이다. `(−H)` 는 **그림과 캡션에만** 있는 **예고 없는 네 번째 막대**다.

⇒ *"위에 있을 때랑 밑에 있을 때랑 분리를 안 하고 바로 PVDF 비교로 갔다"* 는
**원문으로 확인됐다.** 분리를 안 한 정도가 아니라 **언급 자체가 없다.**

### ② **본문에 binding energy 수치가 하나도 없다** ✅ 확정

−0.162 / −1.819 / −2.243 / −0.703 eV 는 **전부 `figure-read ≈`** 다. 본문은 값을 인용하지
않고 *"significantly stronger ... compared to PVDF"* 라는 **정성 서술만** 한다.

⇒ *"그냥 figure 용일 수도 있어"* 라는 판단이 맞다. 논지가 실제로 쓰는 것은
**"AMPS > PVDF"** 라는 부등호 하나뿐이고, 네 막대의 크기 관계는 본문이 안 쓴다.

### ③ 🔴 **메커니즘 서술과 `(−H)` 그림이 서로 안 맞는다**

본문이 대는 이유는 *"**sulfonate group** 과 표면 O 사이의 수소결합"* 이다.
그런데 `(−H)` 는 **그 H 를 뗀 것**이라 술포네이트가 **수소결합 주개가 될 수 없다.**
그럼에도 그림에는 `ICEP_AMPS` 와 `ICEP_AMPS (−H)` **둘 다** "Hydrogen bonding" 화살표가
붙어 있다 (`figure-read`).

남는 주개는 **아미드 N–H** 뿐이다 — AMPS 는 acrylamide 라 N–H 가 있고, 본문도 FT-IR 절에서
*"The N–H bending vibration frequency (≈1540 cm⁻¹) of the AMPS unit"* 를 따로 다룬다.
즉 `(−H)` 막대가 가장 센데(−2.243), **본문이 그 세기의 근거로 댄 결합은 그 구조에 없다.**

⚠ 이건 그림 판독 기반 지적이다. Figure S13 이 원자별 접촉을 보여 줄 수 있으므로
**SI 확보 전까지 확정으로 쓰지 않는다.**

## 1-4. ⛔ 아직 모르는 것 — ICEP SI 없이는 못 닫는다

| 물음 | 왜 중요한가 |
|---|---|
| 코드·범함수·vdW·U·k-point | "DFT" 라고만 썼다. 실제 DFT 면 전하를 **지정할 수 있다** |
| **`AMPS(−H)` 의 총전하가 0 인가 −1 인가** | 이 한 줄이 §3 판정을 확정한다 |
| 하전이면 **배경전하(jellium) / `NELECT`** 처리 | 없으면 하전 슬랩의 발산 항이 안 잡힌다 |
| **뗀 H 의 참조상태** (H• / ½H₂ / H⁺) | 명시가 없으면 `E_bind` 의 `E(X)` 가 정의 안 된다 |
| 슬랩 두께·진공·고정층·리튬화 상태 | (001) 이라는 것만 캡션에 있다 |
| 스핀/자성 (Ni³⁺ 는 열린 껍질이다) | 우리 2026-08-28 카드의 그 위험신호 |

**Kang 과 달리 ICEP 는 "DFT" 라고 명시했다.** 그러면 전하를 지정할 **수단은 있다** —
문제는 지정했는지, 했다면 무엇으로 했는지를 본문이 말하지 않는다는 것이다.

---

# II. 판정 — 무엇이 정의되고 무엇이 안 되나

`E_bind(X) = E(slab+X) − E(slab) − E(X)` 는 **X 가 양변에 같으므로 X 마다 내부적으로 정합**이다.

- ✅ **AMPS vs PVDF 비교는 성립한다.** 서로 다른 분자를 각자 정합한 기준으로 잰 값이다.
  그리고 이것이 본문이 실제로 주장하는 전부다.
- ⛔ **AMPS vs AMPS(−H) 차이는 성립하지 않는다.** 두 X 의 **조성이 다르다.**
  차이 −0.424 eV 안에는 H 제거 에너지가 섞여 있고, 한쪽이 하전됐다면 **전하 상태 불일치**까지
  섞인다.

**그래서 "PVDF 로 바로 간 것" 은 흠이 아니라 오히려 방어 가능한 쪽이다.**
진짜 문제는 **비교하면 안 되는 두 막대를 한 축 위에 나란히 그려 놓은 것**이다 —
막대 넷을 한 그래프에 올리면 독자는 당연히 −1.819 와 −2.243 을 뺀다.

## II-1. 물어야 할 양은 흡착에너지가 아니다

실제 과정이 `-SO₃H + NMC → -SO₃⁻ + H⁺ + e⁻(→NMC)` 라면 정의되는 양은 **양성자 이동
반응에너지**다:

```
ΔE_PT = E(NMC–H + binder⁻) − E(NMC + binder–H)
```

- 양변 **둘 다 중성**, **조성 보존**.
- 전자가 어디로 갔는지 **물을 필요가 없다** — 반응 양변에 다 들어 있다.

**PEDOT 이 다른 이유**: self-doped 라 전자가 폴리머 골격에 비편재화될 수 있다.
AMPS 는 갈 데가 NMC 뿐이라 H 와 전자가 **같이** NMC 로 간다.

## II-2. 우리 쪽 연결

- 이 양을 이미 갖고 있다 — **`U_PCET`** (SDCP). 다만 **분자계 정의뿐이고 산화물 슬랩 버전은 없다.**
- 함정은 **2026-08-28 에 카드로 박아놨다**:
  *"admissible state 가 여럿인데 **선택·집계 규칙이 없으면** scalar estimand 는 정의되지 않는다"*
  (`kb/methodology/estimand_before_running_2026_08_28.md`).
- 회신 O 의 정정: *"고치는 법은 전 계에 같은 NUPDOWN 값이 **아니라** 같은
  **state-selection policy** 다."*
- ICEP Figure 2g 는 **그 규칙 없이 상태 둘을 한 축에 올린** 사례다. 우리가 wave1 에서
  *"제약된 기준에서 자유로운 복합체를 뺐다"* 로 걸린 것과 **같은 층위**다.

---

# III. Kang 논문 — 같은 문제를 **짝이온으로** 푼 대조군

*Adv. Mater.* **2025**, 37, 2416872, "Bollard-Anchored Binder System" (PAA-CMC 그래프트
= **PC**, + PTFE, NMC622 건식전극).

## III-1. 🔴 Kang 은 DFT 를 안 썼다 (SI p.7–8, 확인됨)

> "**Deep-learning based density functional theory (DFT)** and molecular dynamics (MD)
> simulations were conducted using the **preferred potential (PFP) version v3.0.0** as a
> **universal neural network potential (NNP)** estimator for the computation of atomic
> forces. The calculations were performed using **Matlantis** software"

- Figure 4c 흡착에너지 = **PFP(Matlantis) NNP 값**. 이름만 "DFT-based" 다.
- **Gaussian16 B3LYP/6-31G + diffuse 2 + d/p 분극** 은 **FTIR 진동수 배정 전용**.
- 슬랩: NMC622 `LiNi₀.₆Mn₀.₂Co₀.₂O₂`, *R-3m*, **fully lithiated**, **2×2×1**, 진공 **40 Å**,
  하반부 고정. TM 층은 같은 원소끼리 √3 간격.
- 최적화 ASE **L-BFGS**, `fmax 0.01`. 정의 `E_ads = E_slab-binder − (E_slab + E_binder)`.
- MD: **NVT Langevin, 400 K, 10 ps, 1 fs, friction 0.01**.
- 흡착점: PC 를 **15 configuration 으로 회전**시켜 각각 계산.

### 왜 이게 "이온 상태로 붙여도 되나" 의 절반이 되나

**범용 NNP 에는 전하 입력칸이 없다.** 원자종 + 좌표만 받는다. H 를 뗀 구조를 NNP 에
넣으면 그건 "SO₃⁻" 가 아니라 **H 가 하나 없는 중성 조성**이다. 전자 하나의 행방은
모델이 정하는 게 아니라 훈련셋이 중성 주기계였으니 **암묵적으로 중성**이다.
물리적으로는 SO₃⁻ 보다 **SO₃• 라디칼**에 가깝다.

⇒ **Kang 방식이었다면** 그림에 `SO₃⁻` 로 그려도 계산은 음이온이 아니다.
**ICEP 는 "DFT" 라고 썼으므로 이 논거가 그대로 적용되지 않는다** — §1-4 확인이 필요하다.

## III-2. Kang 의 해법 = 짝이온을 계에 넣고 **개수를 상태 이름으로**

PC 도 -COO⁻ 를 가진 음이온성 바인더다. 그런데 원료가 **sodium** CMC 라 Na⁺ 가 실제로 있다.

| 상태 | E_ads | 설명 |
|---|---:|---|
| **PC_2Na** | **−2.24 eV** | Na 2개가 NMC 표면 O 에 결합 |
| **PC_1Na** | −1.12 eV | Na 1개 |
| **PC_0Na** | −0.37 eV | Na 없이 −OH·−COOH 의 장거리 쌍극자 |
| PTFE_dimer | −0.09 eV | 표면 O 와 PTFE 의 F 가 **정전기적 반발** |

**전하 중성을 유지하면서 음이온기를 표현하는 정석**: 조성 보존 · 총전하 0 ·
**상태 이름에 Na 개수가 박혀 있다.**

그리고 결정적으로 — **결합 세기를 정하는 것은 COO⁻ 자체가 아니라 Na 가 몇 개 다리를
놓느냐**다 (2.24 → 1.12 → 0.37). "음이온기가 세게 붙는다" 가 아니라
**"짝이온이 다리를 놓는다"** 가 물리다.

⚠ 다만 이건 **사전 설계가 아니라 사후 분류**로 읽힌다 — 15개 회전 configuration 을 돌린 뒤
*"The adsorption states were **classified into** three categories"*.

## III-3. 덤 — Kang Figure 4c 축 단위가 틀렸다 (확인됨)

축 라벨 **"Adsorption energy (kJ mol⁻¹)"**, 축 범위 **0.5 ~ −2.5**.
본문 값 **−2.24 / −1.12 / −0.37 / −0.09 eV**. −2.24 eV = **−216 kJ/mol** 이라 그 축에
안 들어간다. 축 범위가 eV 와 정확히 맞으므로 **단위 라벨 오기**다. 게재본에 남아 있다.

---

## Counter-arguments (보존)

**반론 ①** — "NNP 도 훈련셋에 이온성 계가 있으면 국소 전하를 흉내 낼 수 있다."
→ 부분적으로 타당하다. NNP 는 **국소 화학환경**으로 에너지를 내므로 Na⁺-SO₃⁻ 같은
환경이 훈련셋에 있으면 그 환경의 에너지는 잘 낸다. 그러나 **총전하를 입력으로 받지
않으므로** 같은 원자배열에 대해 중성/음이온 두 상태를 **구별해 줄 수 없다.**
"흉내" 와 "선택" 은 다르다. NNP 값이 틀렸다는 뜻이 아니라 **어느 상태를 잰 것인지 말할 수
없다**는 뜻이다.

**반론 ②** — "슬랩이 NCM 이라 전자를 받아 주므로 중성으로 돌려도 실제로는 전하이동이
일어나 자동으로 옳은 상태가 된다."
→ 배영진의 논지이고 **물리적으로 가장 그럴듯하다.** 다만 그렇다면 그 계산이 재는 것은
"SO₃⁻ 의 흡착에너지" 가 아니라 **§II-1 의 ΔE_PT 에 가까운 무언가**이고, H 원자 하나가
계에서 **사라진** 상태라 반응식이 닫히지 않는다. **반론이 맞을수록 "흡착에너지" 라는
이름이 더 틀린다.**

**반론 ③** — "논문들이 다 이렇게 한다. 우리가 과하게 판다."
→ 관행인 것은 맞다. 그러나 우리는 SDCP 에서 **같은 오류로 여덟 번 반려**됐다
(`CLAUDE.md` 계산 규율). 관행을 근거로 삼으면 그 여덟 번이 무의미해진다.
그리고 이번 판독의 결론은 *"ICEP 가 틀렸다"* 가 아니라 **"그 그림에서 뺄셈을 하면 안 된다"**
다 — 논문의 주장(AMPS > PVDF)은 그대로 살아 있다.

---

## Gap

- **ICEP SI 미확보** — §1-4 표 전부. 특히 `AMPS(−H)` 총전하 한 줄.
- §1-3 ③ (메커니즘–그림 불일치)은 **그림 판독 기반**이다. Figure S13 로 확인해야 확정.
- Kang 의 Na 상태 분류가 사전 설계인지 사후 분류인지 미확정 (SI Fig S15).
- **`U_PCET` 의 산화물 슬랩 버전이 없다.** 우리가 이 지적을 실제로 쓰려면 만들어야 한다.
- 두 논문 다 **오차막대·시드가 없다.** 단일 구조 흡착에너지의 재현성은 어느 쪽도 안 보인다.
  (Kang 은 15 configuration 의 분포를 SI Fig S15 에 두었다고 하나 미확인.)
