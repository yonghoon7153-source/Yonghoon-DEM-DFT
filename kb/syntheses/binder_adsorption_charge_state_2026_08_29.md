---
title: "음이온성 바인더의 흡착에너지 — 탈양성자 상태를 어떻게 다루나 (ICEP vs Kang 대조)"
date: 2026-08-29
updated: 2026-08-29
tags: [binder, adsorption, charge-state, estimand, nnp, pcet, sdcp, literature]
status: 진행 — ICEP 본문 판독 대기 (논문 에이전트)
confidence: medium
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
구조의 값과 **같은 축에 올리면**, 그 두 막대의 차이는 "탈양성자화 효과" 가 아니라
**조성이 다른 두 분자의 값**이다. 물어야 할 양은 흡착에너지가 아니라 **양성자 이동
반응에너지**이고, 그건 양변 중성·조성 보존으로 정의된다.

---

## 0. 무엇을 봤고 무엇을 안 봤나

| 자료 | 상태 |
|---|---|
| Kang et al., *Adv. Mater.* **2025**, 37, 2416872 — 본문 p.5–14 + SI p.1–9 | ✅ **직접 읽음** |
| ICEP 논문 (AN/AMPS 코폴리머, NCM) — **binding energy 그림** | ✅ 그림만 봄 (`figure-read ≈`) |
| ICEP 논문 **본문·SI 계산 method** | ⛔ **아직 안 봤다** — 논문 에이전트 진행 중 |

⚠ 아래 ICEP 관련 서술 중 **계산 조건에 대한 것은 전부 추정**이다. §5 의 확인 항목이
채워지기 전에는 확정으로 쓰지 않는다.

---

## 1. Kang 논문은 DFT 를 안 썼다 (확인됨)

SI *Computational method* (p.7–8) 원문:

> "**Deep-learning based density functional theory (DFT)** and molecular dynamics (MD)
> simulations were conducted using the **preferred potential (PFP) version v3.0.0** as a
> **universal neural network potential (NNP)** estimator for the computation of atomic forces.
> The calculations were performed using **Matlantis** software"

- Figure 4c 의 흡착에너지는 **PFP(Matlantis) NNP 값**이다. 이름만 "DFT-based" 다.
- **Gaussian16 B3LYP/6-31G + diffuse 2 + d/p 분극** 은 **FTIR 진동수 배정 전용**이다.
- 슬랩: NMC622 `LiNi₀.₆Mn₀.₂Co₀.₂O₂`, *R-3m*, **fully lithiated**, **2×2×1**, 진공 **40 Å**,
  하반부 고정. TM 층은 같은 원소끼리 √3 간격 배치.
- 최적화: ASE **L-BFGS**, `fmax_threshold = 0.01 eV`.
- 정의: `E_ads = E_slab-binder − (E_slab + E_binder)`.
- MD: **NVT Langevin, 400 K, 10 ps, 1 fs, friction 0.01**, 하반부 고정.
- 흡착점 탐색: PC 분자를 **15 configuration 으로 회전**시켜 각각 계산.

### 1-1. 이것이 "이온 상태로 붙여도 되나" 의 답이다

**범용 NNP 에는 전하 입력칸이 없다.** 원자종 + 좌표만 받는다. 그래서 H 를 뗀 구조를
NNP 에 넣으면 그건 "SO₃⁻ (음이온)" 이 아니라 **H 가 하나 없는 중성 조성**이다.
전자 하나의 행방은 모델이 정하는 게 아니라, 훈련셋이 중성 주기계였으니 **암묵적으로 중성**이다.
물리적으로는 SO₃⁻ 보다 **SO₃• 라디칼**에 가깝다.

⇒ 그림에 `SO₃⁻` 로 그려져 있어도 계산이 음이온을 표현했다는 뜻이 아니다.

---

## 2. Kang 은 같은 문제를 **짝이온으로** 풀었다 (확인됨)

Kang 의 PC 도 -COO⁻ 를 가진 음이온성 바인더다. 그런데 원료가 **sodium** CMC 라 Na⁺ 가
실제로 있다. 그래서 흡착 상태를 **Na 개수로 선언**했다:

| 상태 | E_ads | 설명 |
|---|---:|---|
| **PC_2Na** | **−2.24 eV** | Na 2개가 NMC 표면 O 에 결합 |
| **PC_1Na** | −1.12 eV | Na 1개 |
| **PC_0Na** | −0.37 eV | Na 없이 −OH·−COOH 의 장거리 쌍극자 상호작용 |
| PTFE_dimer | −0.09 eV | NMC 의 O 와 PTFE 의 F 가 정전기적으로 **반발** |

**전하 중성을 유지하면서 음이온기를 표현하는 정석**이다:
조성 보존 · 총전하 0 · **상태 이름에 Na 개수가 박혀 있다**.

그리고 결정적으로 — **결합 세기를 정하는 것은 COO⁻ 자체가 아니라 Na 가 몇 개 다리를
놓느냐**다 (2.24 → 1.12 → 0.37). "음이온기가 세게 붙는다" 가 아니라 "짝이온이 다리를
놓는다" 가 물리다.

⚠ 다만 이건 **사전 설계가 아니라 사후 분류**로 읽힌다 — 본문은 15개 회전 configuration 을
돌린 뒤 *"The adsorption states were **classified into** three categories"* 라고 쓴다.
(사전 선언인지 사후 분류인지는 논문 에이전트 확인 대기.)

---

## 3. ICEP 그림의 문제 — 뺄셈이 정의되지 않는다

`figure-read ≈` (그림에서만 읽은 값):

| | E_bind |
|---|---:|
| ICEP_AN | ≈ −0.162 eV |
| ICEP_AMPS | ≈ −1.819 eV |
| **ICEP_AMPS (−H)** | ≈ **−2.243 eV** |
| PVDF | ≈ −0.703 eV |

`E_bind(X) = E(slab+X) − E(slab) − E(X)` 는 **X 가 양변에 같으므로 X 마다 내부적으로 정합**이다.
따라서:

- ✅ **AMPS vs PVDF 비교는 성립한다.** (서로 다른 분자를 각자 정합한 기준으로 잰 값)
- ⛔ **AMPS vs AMPS(−H) 차이는 성립하지 않는다.** 두 X 의 **조성이 다르다.**
  그 차 −0.424 eV 안에는 H 제거 에너지가 섞여 있고, 만약 한쪽이 하전됐다면
  **전하 상태 불일치**까지 섞인다.

**그래서 "H 있을 때/없을 때를 분리 안 하고 바로 PVDF 로 갔다" 는 흠이 아니라 오히려
방어 가능한 쪽이다.** 진짜 문제는 **그 둘을 한 축 위에 나란히 그렸다**는 것이다 —
막대 넷을 한 그래프에 올리면 독자는 당연히 −1.819 와 −2.243 을 뺀다.
**비교하면 안 되는 것을 비교 가능하게 그려 놨다.**

---

## 4. 물어야 할 양은 흡착에너지가 아니다

실제 과정이 `-SO₃H + NMC → -SO₃⁻ + H⁺ + e⁻(→NMC)` 라면, 정의되는 양은 **양성자 이동
반응에너지**다:

```
ΔE_PT = E(NMC–H + binder⁻) − E(NMC + binder–H)
```

- 양변 **둘 다 중성**이고 **조성이 보존**된다.
- 전자가 어디로 갔는지 **물을 필요가 없다** — 반응 양변에 다 들어 있다.
- 짝이온을 쓰는 Kang 식과 같은 목적(중성 유지)을 다른 방법(반응식 닫기)으로 달성한다.

**PEDOT 이 다른 이유**: self-doped 라 전자가 폴리머 골격에 비편재화될 수 있다.
AMPS 는 갈 데가 NMC 뿐이라 H 와 전자가 **같이** NMC 로 간다.

### 4-1. 우리 쪽 연결

- 우리는 이 양을 이미 갖고 있다 — **`U_PCET`** (SDCP 캠페인).
- 이 함정은 **2026-08-28 에 카드로 박아놨다**:
  *"admissible state 가 여럿인데 **선택·집계 규칙이 없으면** scalar estimand 는 정의되지 않는다"*
  (`kb/methodology/estimand_before_running_2026_08_28.md`).
- 회신 O 의 정정: *"고치는 법은 전 계에 같은 NUPDOWN 값이 **아니라** 같은
  **state-selection policy** 다."*
- ICEP 그림은 **그 규칙 없이 상태 둘을 한 축에 올린** 사례다. 우리가 wave1 에서
  *"제약된 기준에서 자유로운 복합체를 뺐다"* 로 걸린 것과 **같은 층위의 오류**다.

---

## 5. ICEP 논문에서 확인해야 할 것 (⛔ 미확인 — 논문 에이전트 진행 중)

1. **엔진**: VASP/QE 같은 실제 DFT 인가, PFP·M3GNet·CHGNet 같은 범용 NNP 인가?
   - NNP 면 → §1-1 그대로. 전하는 애초에 표현 불가.
   - VASP 면 → **`NELECT` 조정·배경전하(jellium)** 언급이 method 에 반드시 있어야 한다.
     없으면 총전하 0 = 라디칼 계산이다.
2. **AMPS(−H) 의 총전하**: 0 인가 −1 인가?
3. **뗀 H 의 참조상태**: H•(원자) · ½H₂ · H⁺ 중 무엇인가? (명시 없으면 그 자체가 결함)
4. **본문에 AMPS 와 AMPS(−H) 를 직접 비교하는 문장이 있는가?**
   없다면 "그림 용" 판단이 확정된다.
5. 슬랩: NCM 조성·표면 지수·두께·진공·고정층·리튬화 상태.

---

## Counter-arguments (보존)

**반론 ①** — "NNP 도 훈련셋에 이온성 계가 있으면 국소 전하를 흉내 낼 수 있다."
→ 부분적으로 타당하다. NNP 는 **국소 화학환경**으로 에너지를 내므로, 훈련셋에
Na⁺-SO₃⁻ 같은 환경이 있으면 그 환경의 에너지는 잘 낸다. 그러나 **총전하를 입력으로
받지 않으므로** 같은 원자배열에 대해 중성/음이온 두 상태를 **구별해 줄 수 없다**.
"흉내" 와 "선택" 은 다르다. 반박이 이 반론을 지우지는 않는다 — NNP 값이 무조건
틀렸다는 뜻이 아니라, **어느 상태를 잰 것인지 말할 수 없다**는 뜻이다.

**반론 ②** — "슬랩이 금속성(NMC)이라 전자를 받아 주므로 중성 계로 돌려도 실제로는
전하이동이 일어나 자동으로 옳은 상태가 된다."
→ 이게 배영진의 논지이고 **물리적으로 가장 그럴듯하다**. 다만 그렇다면 그 계산이 재는
것은 "SO₃⁻ 의 흡착에너지" 가 아니라 **§4 의 ΔE_PT 에 가까운 무언가**이고, H 원자
하나가 계에서 **사라진** 상태라 반응식이 닫히지 않는다. 즉 반론이 맞을수록
**흡착에너지라는 이름이 더 틀린다.**

**반론 ③** — "논문들이 다 이렇게 한다. 우리가 과하게 판다."
→ 관행인 것은 맞다. 그러나 우리는 SDCP 에서 **같은 오류로 여덟 번 반려**됐다
(`CLAUDE.md` 계산 규율). 관행을 근거로 삼으면 그 여덟 번이 무의미해진다.

---

## Gap

- ICEP 본문 미판독 (§5 전부).
- Kang 의 Na 상태 분류가 **사전 설계인지 사후 분류인지** 미확정.
- ΔE_PT 를 실제로 우리 계에서 계산한 적은 없다 — `U_PCET` 은 SDCP 분자계 정의이고
  **산화물 슬랩 버전은 없다**.
- 두 논문 다 **오차막대·시드가 없다** (Kang 은 15 configuration 의 평균/분포를 SI Fig S15 에
  두었다고 하나 미확인). 단일 구조 흡착에너지의 재현성은 어느 쪽도 보이지 않는다.

---

## 덤 — Kang Figure 4c 축 단위가 틀렸다 (확인됨)

축 라벨: **"Adsorption energy (kJ mol⁻¹)"**, 축 범위 **0.5 ~ −2.5**.
본문 값: **−2.24 / −1.12 / −0.37 / −0.09 eV**.

−2.24 eV = **−216 kJ/mol** 이라 그 축에 들어가지 않는다. 축 범위가 eV 와 정확히 맞으므로
**단위 라벨이 오기**다. *Adv. Mater.* 게재본에 남아 있는 오류다.
