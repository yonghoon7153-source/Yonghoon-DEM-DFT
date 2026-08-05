# Fundamentals of inorganic solid-state electrolytes for batteries — Famprikis / Canepa / Dawson / Islam* / Masquelier* (Nature Materials 2019, 18, 1278–1291)

> slug `famprikis2019_fundamentals_inorganic_sse` · DOI `10.1038/s41563-019-0431-3` · type `review (자체 계산·실험 0)` · PDF `litdb/inbox/56. Fundamentals of inorganic solid-state electrolytes for batteries.pdf` (최초 digest 시 임시본 `79dcf62a-56._Fundamentals_…pdf` — 동일 파일) · digested `2026-08-05` · **재투입 검증 `2026-08-06`**(inbox #56 · 분류 DFT — §17) · status ✅
> elements: Li, Na, Mg, H, B, N, O, F, Si, P, S, Cl, Ge, Br, I, Al, Ti, Zr, Ag, Sn, La, In, Co, Ni, Mn
> methods: DFT, AIMD, MD, MLIP, ESW, XPS, Raman, elastic
> **저자**: Theodosios Famprikis (Amiens LRCS/UPJV + Bath), Pieremanuele Canepa (Bath → NUS), James A. Dawson (Bath/Newcastle), **M. Saiful Islam\*** (Bath), **Christian Masquelier\*** (Amiens/RS2E) · 본문 11 pp · 그림 7 + 표 1 + Box 1 · refs 151 · Received 2018-10-31 / Published 2019-08-19

---

## 0. 이 digest 를 읽는 법 (먼저 읽을 것)

- **이 논문은 리뷰다. 자체 DFT·자체 실험이 하나도 없다.** 본문에 나오는 모든 숫자는 **소환값**(2차 인용)이고, 원출처 ref 번호를 이 digest 에 전부 붙여 놨다. `comparison_vs_ours.md` 에 이 논문 숫자를 우리 절대값과 같은 칸에 넣지 않는다.
- **이 리뷰의 진짜 가치는 "숫자"가 아니라 "축 정의"** 다. 특히 세 가지:
  1. **다중스케일 사다리** (Å → nm → µm → mm → cm) 와 각 스케일의 전도도 기호 (`Fig. 2`) — 우리 DFT(Å)와 DEM(µm)이 **어느 칸을 채우는지** 를 이 그림 하나로 말할 수 있다.
  2. **기계적 열화 4요소** (`Fig. 6`) — `E/G` · `K_Ic` · `σ_adh/γ_xfc` · `ε_electrochemical`. 우리 repo 의 elastic/adhesion json 이 이 그림의 **어느 라벨** 인지 1:1 대응된다.
  3. **음이온 이온화 퍼텐셜 사다리** (§5.3) — 우리 "**ESW onset 은 S-limited**" 규율의 **1차 문헌 근거**.
- ⚠ **사용자가 요청한 두 축의 결론을 먼저**:
  - **(1) DEM**: 직접 DEM 은 **없다**(단어 0회). Bruggeman/tortuosity **식도 없다**. 그러나 **DEM 이 채워야 할 칸을 이 리뷰가 정확히 파 놨다** — `Fig. 2` 의 µm–mm 구간, 그리고 §5.2 의 "contact area per volume of composite" · SE 부피분율 **<50 % / >25 %** 두 문턱. 자세히는 **§6 전체**.
  - **(2) K_IC / γ 수치**: **없다. 0 건.** `K_Ic` 는 `Fig. 6` 라벨과 본문 개념 문장으로만 나오고 **숫자가 단 하나도 안 붙는다**. γ 도 `γ_xfc` 기호뿐. 대신 **E/G 실측 소환값 3세트**(thiophosphate glass · garnet · LiBH₄)를 얻었고, 그중 하나가 **우리 relaxed-ion 값과 거의 정확히 일치**한다 — §7·§11.
- 전압은 전부 **Li/Li⁺ 기준**(별도 환산 불필요). 리뷰가 In/InLi 축을 쓰지 않는다.

---

## 1. 한 줄 요약

무기 고체전해질을 **① 다중스케일 이온수송(Å→cm) · ② 전기화학 안정성(계면 분해) · ③ 역학(접촉·파괴·전착) · ④ 공정경로(합성→치밀화→집적)** 네 기둥으로 재정리한 Nature Materials 튜토리얼 리뷰. **핵심 주장은 "σ_bulk 를 더 올리는 경쟁은 이미 끝났고(≈10 mS/cm 로 액체 수준 도달), 남은 병목은 전부 계면·미세구조·역학이다"** — 즉 물질탐색에서 **다중스케일·전기화학-기계 결합** 으로 축을 옮기라는 선언문.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자/소속 | Famprikis(LRCS Amiens + Bath), Canepa(Bath→NUS), Dawson(Bath→Newcastle), **Islam\***(Bath), **Masquelier\***(Amiens·RS2E) |
| 저널 | *Nature Materials* **18**, 1278–1291 (Dec 2019) |
| DOI | 10.1038/s41563-019-0431-3 |
| 유형 | **Review Article** — 자체 계산 0 · 자체 실험 0 · 소환값만 |
| 대상 조성 | 특정 조성 아님. 언급되는 계열: **thiophosphate**(Li₃PS₄·Li₇P₃S₁₁·Li₆PS₅Cl·Li₁₀GeP₂S₁₂·Li₂S–P₂S₅ glass), **garnet**(Li₇La₃Zr₂O₁₂), **NASICON/LISICON**(Li₄₊ₓSi₁₋ₓXₓO₄), **antiperovskite**(Li₂OHCl), **borohydride**(LiBH₄·LiCB₁₁H₁₂), **Na 계열**(Na₃PS₄·Na₁₁Sn₂PS₁₂·Na₃SbS₄·Na-β-Al₂O₃), **Mg 계열**, **LiPON**, **AgI/RbAg₄I₅** |
| 인용 규모 | refs 151 · Fig 7 · Table 1 · Box 1 |
| 우리 litdb 와의 관계 | **허브 논문**. 이 리뷰가 인용하는 ref 중 최소 5편이 우리 digest 로 이미 있다 → §15 |

---

## 3. 리뷰 구조 지도

```
Introduction ─┬─ Advantages of solid-state batteries (안전·수명·온도창·bipolar·에너지밀도)
              └─ Challenges facing solid electrolytes (Fig. 1: ①금속음극 ②계면 ③물리적 접촉)

Multiscale ion transport (Fig. 2)
   ├ Atomic scale (Å)      : Fig. 3 — 공공/직접침입형/협동(interstitialcy), Eq.(1)(2), bcc 음이온틀, paddle-wheel
   ├ (비정질)               : PDF+RMC, glass-ceramic, 나노결정, ML 퍼텐셜
   ├ Micro–meso (nm–µm)    : GB, 공간전하, 입계 misalignment, **기공률·접촉**
   ├ Macroscopic (µm)      : σ_macro ~10 mS/cm, 임피던스 재현성 1 order
   └ Device (mm)           : Z_device, **ASR = t/σ**, **contact area per volume**, 부피분율 <50 %/>25 %, Eq.(4) 공간전하

Electrochemical stability (Fig. 4, Fig. 5, Table 1)
   ├ redox 분해 Eq.(5) / 화학반응 Eq.(6) / 전기화학반응 Eq.(7)
   ├ 안정창 = μ_Li grand-potential (Richards 방법론) + 과전압 ±0.5 V
   ├ **음이온 IP 사다리** (산화) / 양이온 전자친화도 (환원)
   └ 계면 3시나리오: 본질안정 / 속도론적 안정화 / 인공보호  (Fig. 5b)

Mechanics (Fig. 6, Box 1)   ← ★ 사용자 축 (2)
   ├ 외부압력·순환응력, 미세역학(composite)
   ├ 접착: σ_adh, γ_xfc, 격자 misfit, 전하재배치
   ├ ε_electrochemical (전기화학 충격), zero-strain 전극
   ├ E/G — soft sulfide 는 유리하나 **취성**
   └ **K_Ic** — "결정 인자로 부상" 그러나 **미세구조 의존 → 실험으로만**
   Box 1: CCD 0.3 vs 3–10 mA/cm², Li 항복 0.8 MPa, Li 몰부피 ~10×, Monroe–Newman 무기SE 부적용, E/G 소환값 3세트

Processing routes (Fig. 7)  ← ★ 사용자 축 (1) 의 절반
   ├ Synthesis: solid-state / soft chemistry / mechanochemical
   ├ **Densification: 소결 vs 냉간·열간 가압, SPS**
   └ Integration: 박막 / **냉간가압 pellet-type** / sheet-type, 3D 구조

Conclusions: 물질탐색 · 계면 캐릭터라이제이션 · **공정/역학 표준화**
```

---

## 4. 수치 총정리 — **본문에 실제로 나오는 정량값 전부** (전부 소환값)

### 4.1 이온수송
| 값 | 맥락 | ref |
|---|---|---|
| **σ_macro ≈ 10 mS/cm (Li⁺)** / **1 mS/cm (Na⁺)** / **0.1 mS/cm (Mg²⁺)** | 상온 거시 전도도 최고 수준 | 7 / 59,60 / 61 |
| 액체 전해질 **~10 mS/cm** | 비교 기준 — "이미 대등" | — |
| **18 C @ 100 °C, 충방전 3분** | Kato et al. 초고속 사이클 | 7 |
| **> 10,000 cycles** | 박막 마이크로배터리 수명 | 4 |
| 동작 온도창 **−50 ~ 200 °C 이상** | 액체가 얼거나 끓는 구간 | — |
| **임피던스 유래 σ·Ea 가 연구그룹 간 약 1 order 산포** | Na₁₁Sn₂PS₁₂ 사례 | 59,60 |
| m ≈ **−1** (σ = σ₀T^m e^{−Ea/k_BT}) | Eq.(1) 의 온도 prefactor | — |
| Cl⁻ 도판트 on S²⁻ → Na⁺ **공공** 생성 / Si⁴⁺ on P⁵⁺ → Na⁺ **침입형** 생성 | Na₃PS₄ 결함화학 | 20 / 21 |

### 4.2 전기화학 안정성
| 값 | 맥락 | ref |
|---|---|---|
| **음이온 이온화 퍼텐셜 사다리 (산화 한계)**: **N³⁻ < P³⁻ < H⁻ ≪ S²⁻ < I⁻ < O²⁻ < Br⁻ < Cl⁻ ≪ F⁻** | 낮을수록 먼저 산화 = 창의 상한을 pin | 65 |
| 분해 과전압 **약 ±0.5 V** | Na₃PS₄ — 열역학 창 밖으로 창이 넓어지는 속도론적 여유 | 83 |
| LLZO vs Li⁰: 열역학 불안정하나 **0.05 V vs Li⁰**, 반응에너지 **20 meV/atom** | "거의 안정" 의 정량 | 65,80,84 |
| 계면상 저항 범위 **kΩ·cm² (지배적) ~ 무시 가능** | interphase 임피던스 스펙트럼 | 67,69–71 |
| μ_Li 계면 구배 **수 mV·nm⁻¹**, 공간전하 두께 **nm 급** | Eq.(4), `Fig. 4` | 6,77,78 |
| 반응식 Eq.(5) `2Li₃PᵛS₄ + 2e⁻ + 2Li⁺ ↔ Li₄P₂ᴵⱽS₆ + 2Li₂S`; 이어서 `Li₄P₂S₆ + 14e⁻ + 14Li⁺ → 2Li₃P + 6Li₂S` | Li₃PS₄ 의 Li 금속 환원 경로 | 65,79–81 |
| Eq.(6) `Na₃PS₄ + 2NaMO₂ → Na₃PO₄ + 2NaMS₂` (O²⁻–S²⁻ 교환) | 순수 화학반응 예 | 83,84 |
| Eq.(7) `2Li₃PS₄ + 3LiCoᴵᴵᴵO₂ → Coᴵᴵ(PO₃)₂ + 2Coᴵⱽ S₂ + 4S⁰ + 9e⁻ + 9Li⁺` | 전기화학반응 예 (실제로는 나노결정 intermixing, TEM) | 65 / 66 |

### 4.3 역학 (★ 축 2 — **이 리뷰 전체의 기계 수치는 아래가 전부**)
| 값 | 재료·조건 | ref | 원출처 |
|---|---|---|---|
| **E ≈ 20 GPa, G ≈ 7 GPa** | **soft thiophosphate glass (Li₂S–P₂S₅)** | **108** | McGrogan et al., *Adv. Energy Mater.* **7**, 1602011 (2017) — "Compliant **yet brittle**" |
| **E ≈ 150 GPa, G ≈ 60 GPa** | 단결정 산화물 garnet (LLZO) | **147** | Yu et al., *Chem. Mater.* **28**, 197 (2016) |
| **G ≈ 4 GPa** | LiBH₄ (가장 무른 축) | **148** | Ahmad et al., *ACS Cent. Sci.* (ML 스크리닝) |
| **항복강도 ~0.8 MPa (Li 금속)** | 알칼리 금속 | **144** | Masias et al., *J. Mater. Sci.* **54**, 2585 (2019) — elastic·**plastic·creep** 전부 |
| Li 금속 몰부피가 **어떤 무기 SE 보다 ~10× 크다** | 국소 팽창·응력의 근원 | **148** | — |
| 금속 음극에 걸리는 압축응력 **MPa 급** (→ Li 항복강도 초과) | 스택압 + 사이클 응력 | — | — |
| **CCD ≤ 0.3 mA/cm²** (실면적 기준, 상온, 대부분의 무기 Li SE) vs **목표 3–10 mA/cm²** | 임계전류밀도 | **10** | — |
| **K_Ic** | **값 없음. 기호와 개념 문장뿐** (`Fig. 6`) | 109 (Bucci 모델링) | ⚠ **수치 0건** |
| **γ_xfc** (화학적 계면에너지), **σ_adh** (박리에 필요한 압력) | **값 없음. 정의뿐** | 105 / 107 | Wang & Sakamoto, *J. Power Sources* **377**, 7 (2018) — σ_adh ↔ 계면저항 **상관 실증**(수치 미소환) |

### 4.4 미세구조·공정 (★ 축 1)
| 값 | 맥락 | ref |
|---|---|---|
| **복합양극 내 SE 부피분율 ≤ 50 %** | 에너지밀도 + **전자 percolation** 확보를 위한 상한 | **68** (Bielefeld/Janek) |
| **동 부피분율 ≥ 25 %** | **이온 percolation** 한계를 피하기 위한 하한 | **68** |
| "위 문턱은 **입도(분포)의 함수**" · 작은 입자 → 전자·이온 percolation 문턱 **둘 다 낮아지고** 전하이동 가능 유효면적 ↑ | 입도–percolation 결합 | 68,74,76 |
| 기공률 ↓ ⇒ 전도도 ↑ (입자–입자 접촉 강화) — **산화물·황화물 양쪽에서 확인** | 치밀화의 근거 | **55**(oxide, hot-press LLZO 상대밀도↔기계물성) / **58**(sulfide, Sakuda) |
| **ASR = t/σ**, 계면 임피던스 기여는 **접촉면적(단위 복합체 부피당)** 에만 의존 | 두께 무관 지표 | 68 |
| 복합전극에서 **실제 이온접촉 유효면적 ≪ 활물질 총면적** | 전기화학적으로만 추정 가능 | 72,73 |
| 균열전파 제어 인자: **입경 · 기공률 · 기존 균열 · 기공 연결성(pore connectivity)** | 파괴인성을 좌우하는 미세구조 변수 | 55 / 12 / 138 |
| 냉간가압(cold pressing)은 **랩 스케일에서 가장 보편**, 그러나 **스케일업·경질 산화물에는 제한적** | 공정 현실 | 118 |
| SPS(spark plasma sintering) = 미세구조 정밀제어의 **기준 방법**, 그러나 **비용상 금지적** | | 51,117 |

> ⚠ **없는 것**(찾았지만 논문에 없음): Bruggeman 지수·tortuosity 식·기공률 수치·상대밀도 수치·성형압/스택압 수치(MPa 급이라는 서술만)·입경 수치·K_Ic 수치·γ 수치·마찰계수·σ 절대값 표.

---

## 5. 섹션별 상세

### 5.1 Introduction — 왜 고체인가, 그리고 무엇이 막는가 (`Fig. 1`)

**장점 논거 5개**: ① 가연성 액체 부재 → 안전(단, "detailed thermal/mechanical abuse 연구는 아직 진행 중"이라고 스스로 유보), ② 고체는 반응성이 낮아 수명 기대 — 박막 마이크로배터리 >10,000 cycles 이지만 **"이 특성의 스케일업 가능성은 아직 입증 안 됨"**, ③ **−50 ~ 200 °C** 광온도창 + 고체는 **bulk polarization 이 없어** 고전류에 유리, ④ **bipolar stacking**(한 셀의 음극과 다음 셀의 양극을 같은 집전체에) → 고전압 단일 디바이스·패키징 감소(`Fig. 1`), ⑤ 금속 음극(Li·Na·Mg) 및 고전압 양극 사용 가능성.

**`Fig. 1` 의 3대 도전** (인셋 3개):
1. **금속 음극** — 불균일 전착(수지상 구조가 SE 를 관통하는 렌더링).
2. **계면** — 이온을 막는 blocking interphase (양극 입자와 SE 의 3D 볼륨 렌더링).
3. **물리적 접촉** — 양극 구형 입자가 SE 표면에 **점접촉**만 하고 있는 그림. **이 인셋이 곧 DEM 그림이다** (§6).

캡션의 한 줄이 중요하다: *"For commercial cells, **inactive volume (solid electrolyte, current collectors, porosity) should be minimized** and the electrodes should be balanced (chemically and mechanically)."* — 기공률을 **비활성 부피** 로 명시. 즉 리뷰 스스로 "기공률 최소화"를 설계 목표로 못박는다.

### 5.2 Multiscale ion transport — 이 리뷰의 뼈대 (`Fig. 2`)

**핵심 명제**: *"the final impedance of a device is a function of all these mechanisms"* — 소자 임피던스는 원자 → 소자 전 스케일의 곱이다. 그리고 각 스케일을 **직접 볼 수 있는 기법이 다르고 공간·시간 분해능이 제한** 되므로 **다기법 접근이 필수**.

**`Fig. 2` 를 실제로 본 내용** (figure-read):
- 스케일 사다리 5칸 — **Atomic (Å)** → **Micro (nm)** → **Macro (µm)** → **Device (mm)** → **Solid-state battery (cm)**.
- 각 칸의 서술자: 원자 = `E_Hop`, `ν_Hop` (팔면체/사면체 다면체가 그려진 결정격자); 마이크로 = `σ_crystal`(줄무늬 = 결정립 내부), `σ_GBi`(빨간 입계선), `σ_amorphous`(얼룩 = 비정질 영역); 매크로 = `σ_meso` (다결정 + **노란 영역 = 기공/2차상**, 균열 같은 선이 하나 보임); 디바이스 = `ASR charge transfer`, **`Contact area`**, `ASR xface` (파란 양극 입자가 연두 SE 매트릭스에 박혀 있고, **검은 톱니 = 공극/접촉상실** 에 빨간 ✗ 로 막힌 경로 표시); 셀 = `σ_macro`, `Z_SSB`.
- 아래 기법 바 **7개** — 스팬은 그림에서만 읽히므로 `fig_2.png`(폭 2186 px) 위에서 **픽셀로 실측**했다(2026-08-06 재검증). 스케일 앵커 px: Atomic(Å)≈300 · Micro(nm)≈700 · Macro(µm)≈1027 · Device(mm)≈1465 · SSB(cm)≈1913.

  | 기법 | 바 스팬 (px) | 실제 스케일 범위 | 색 = 분류 |
  |---|---|---|---|
  | Nuclear magnetic resonance | 85–913 | Å → nm(µm 직전) | **진파랑 = 직접 프로브** |
  | **Molecular dynamics** | 84–739 | Å → nm | **진파랑 = 직접 프로브** |
  | Impedance spectroscopy | 1058–2084 | µm → cm | **진파랑 = 직접 프로브** |
  | **Continuum modelling** | 836–2085 | nm(µm 직전) → cm | **진파랑 = 직접 프로브** |
  | Diffraction / PDF analysis | 310–1894 | **Å → cm (사다리 전 구간)** | 연파랑 = 보조 |
  | Electron microscopy | 310–1485 | Å → mm | 연파랑 = 보조 |
  | Vibrational spectroscopy | 86–1066 | **Å → µm** | 연파랑 = 보조 |

  ⚠ **초판 digest 정정 2건**: Diffraction/PDF 를 "nm~mm" 로, Vibrational spectroscopy 를 "Å~nm" 로 적었으나 **둘 다 과소**였다 (각각 Å→cm, Å→µm).
- ★ **캡션이 색으로 나누는 두 등급을 초판이 놓쳤다** — *"techniques utilized to **directly probe** ion transport (that is, **quantitatively determine the above descriptors**; in **dark blue**) and **complementary** methods used to aid interpretation (in **light blue**)"*. 즉 리뷰는 **Molecular dynamics 를 NMR·임피던스와 같은 등급의 "이온수송 직접·정량 프로브"로 분류**한다(회절·전자현미경·진동분광은 보조). **→ 우리 MLIP-MD 라인을 "보조 계산"이 아니라 *수송 서술자를 정량 산출하는 1차 기법*으로 자리매김할 수 있는 리뷰급 근거.** 마찬가지로 **continuum modelling 도 직접 프로브** 등급이다.
- ★ **우리 포지셔닝(정정된 형태)**: 초판은 *"µm 칸에 방법 바가 없다"* 고 썼는데 **이는 그림과 다르다** — µm(px 1027)을 지나는 바가 **4개**(Continuum · Diffraction/PDF · Electron microscopy · Vibrational spectroscopy)다. NMR 이 913 에서 끝나고 임피던스가 1058 에서 시작해 **첫 줄에만 µm 부근 흰 틈**이 생기는데, 초판은 그 틈을 사다리 전체의 공백으로 오독했다.
  **살아남는(그리고 더 강한) 주장**: 7개 바는 **전부 이온수송·구조 프로브**다. **역학량(강성·접착·소성·파괴)을 다루는 방법도, 접촉 기하를 *산출*하는 방법도 사다리에 단 하나도 없다** — 스케일이 아니라 **물리 축이 통째로 빠져 있다**. 리뷰는 `Contact area` 를 Device(mm) 칸의 서술자로 그려 놓고, 그것을 **입력으로 받는** continuum 만 사다리에 넣었지 **만들어내는** 방법은 넣지 않았다. DEM 이 정확히 그 자리다 → §6, §14④.

#### (a) Atomic scale (Å) — `Fig. 3`
- 이동 이온은 **음이온 골격**(O²⁻·S²⁻ 또는 폴리음이온)이 만드는 사이트/경로를 따라 확산. 사이트 에너지는 **배위환경** 이 결정(결정에서는 보통 사면체/팔면체).
- **bcc 음이온 골격 가설**: 최고 전도체(예 α-AgI, ref 17)에 공통. Wang et al.(ref 18) — bcc 는 **인접 사면체 간 직접 hop(저 Ea)** 을 허용하고 **고 Ea 인 사면체–팔면체 hop 을 강제하지 않는다**. Li₁₀GeP₂S₁₂, Li₇P₃S₁₁ 에서 확인 → 신물질 탐색의 설계 기준.
- **3가지 이동 기구** (`Fig. 3a`, 페이지 렌더로 확인 — 크롭에서는 잘림): ① **공공(vacancy) 확산**, ② **직접 침입형(direct interstitial)**, ③ **협동/상관(correlated, interstitialcy = knock-on)** — 침입형 이온이 이웃 격자이온을 밀어내고 그 자리를 차지.
- **Eq.(1)** `σ = q n u = σ₀ T^m e^{−E_a/k_BT}`, m ≈ −1. **E_a 는 결함 형성에너지 E_f 와 이동장벽 E_m 의 합** (외인성 영역에서는 E_f 가 사라지고 E_m 만 남는다).
- **Eq.(2)** `σ₀ = z (n q²/k_B) e^{ΔS_m/k_B} α₀² ν₀` — 기하인자 z(≤1), 이동 엔트로피 ΔS_m, hop 거리 α₀, 시도 진동수 ν₀.
- **`Fig. 3b`** (figure-read): 이중 우물 + 전이상태, `E_m` 화살표, `α₀` hop 거리, 우물 곡률로 `ν₀` 를 표현 — **점선 곡선 3개로 곡률(=ν₀)이 재료마다 다름** 을 시각화. 축에 눈금 없음(개념도).
- **`Fig. 3c`** (figure-read, 2026-08-06 확대 재확인): 준안정(침입형) – 안정 – 준안정 사이트의 3중 우물. 초록 이온이 왼쪽 준안정 사이트에서 안정 사이트로 들어가며 거기 있던 주황 이온을 오른쪽 준안정 사이트로 밀어낸다(협동 1회 사건).
  - **장벽**: `E_m^interstitialcy` 빨간 화살표는 **준안정 사이트 바닥 → 좌측 장벽 top**, 오른쪽 노란 화살표는 **안정 사이트 바닥 → 우측 장벽 top**. 노란 쪽이 **약 2배 길다** ⇒ 협동 기구가 장벽을 낮춘다. ⚠ **초판 표현 정정**: 노란 화살표를 "직접 hop" 이라고 불렀는데, 이것은 **같은 협동 사건 안에서 *안정 사이트에서 출발할 때* 보이는 장벽**(= `Fig. 3b` 의 `E_m` 에 해당하는 기준선)이지 별도의 직접-hop 곡선이 아니다. 비교 자체는 유효하다.
  - **거리**: `α₀` 는 **준안정→준안정 전 구간**(= 침입형 결함/전하가 옮겨간 거리), `α₀'` 는 **개별 이온의 실제 변위**(준안정→안정, ≈0.48 α₀). 둘 다 **그림에 명시 라벨**로 있고 본문에는 없다.
  - ★ **해석 주의(2026-08-06 정정)**: Eq.(2) 의 `α₀²` 에 들어가는 것은 **전하가 옮겨간 거리 = 긴 쪽 α₀** 다. 개별 이온이 α₀' 만 움직인다고 해서 σ₀ 가 그만큼 깎이지 않는다. **즉 이 그림대로면 협동 기구는 "장벽↓ + hop 거리 유지" 로 순이득**이다 — 초판이 `comparison_vs_ours.md` 에 적었던 "α₀² 가 줄어 상쇄된다" 는 **α₀ 를 잘못 집은 것이라 철회**한다(§17-⑥).
- **연질 골격(sulfide/selenide)의 두 경쟁 효과** (중요): ① 낮은 포논 진동수 → **E_a ↓** (도움), ② 동시에 **ν₀ ↓ 및 ΔS_m ↓ → Eq.(2) 의 prefactor σ₀ ↓** (해로움). Kraft(ref 29)는 **시도 진동수 ↔ 음속 유래 Debye 진동수** 상관을, Muy(ref 31)는 **E_a ↔ 포논 밴드센터**(비탄성 중성자산란) 상관을 보였다.
- **Paddle-wheel**: SO₄²⁻·PO₄³⁻ 등 폴리음이온의 회전이 이온이동을 돕는다는 가설. 계산이 PS₄³⁻(ref 32)·BH₄⁻(ref 33)·OH⁻ 쌍극자(ref 34)의 회전자유도와 σ 의 상관을 재부각. **QENS 직접 증거**는 LiCB₁₁H₁₂·NaCB₁₁H₁₂ 에서(refs 35,36).
- **Eq.(3) Nernst–Einstein**: `D = (u/q)k_BT = σ/(nq²) · H_R k_BT`, **H_R = Haven ratio**. ★ 리뷰가 명시적으로 유보를 단다: *"there is recent debate about the validity of equation (3) in the case of solid electrolytes where the migration of multiple charge carriers is highly correlated and/or in solid electrolytes that exhibit anisotropic migration pathways"* (ref 39, Marcolongo & Marzari). **→ 우리 CLAUDE.md 의 "σ 절대값 인용 금지, NE Haven=1" 규율의 문헌 근거** (§11).

#### (b) 비정질 / glass-ceramic
- 규칙적 배위·대칭 장거리 경로가 없으므로 **통일 이론이 없다**(refs 40,41). hopping 이론은 쓸 수 있지만 **단일 Ea 가 아니라 Ea 분포** 로 통계 처리해야 한다.
- 도구: **PDF(총산란) + reverse Monte Carlo** 로 원자배열·확산경로 직접 시각화(refs 42–44); NMR·진동분광·XPS 로 교차검증(refs 45,46).
- **AIMD 는 비정질에 필요한 셀 크기 때문에 어렵다**(ref 18) → **ML 유도 고전 퍼텐셜**(비정질 Li₃PO₄, ref 47)이 대안. — 우리 UMA/MLIP-MD 노선과 같은 논리.
- **glass-ceramic**: 제어된 결정화로 **준안정 결정상**(Li₇P₃S₁₁)을 석출 → σ 가 **수 자릿수** 증가. 나아가 "완전 비정질"로 알려졌던 **glassy Li₃PS₄** 가 실은 **비정질 매트릭스 속 나노결정** 임이 HRTEM 으로 밝혀짐(ref 49). Li₃PS₄(ref 48)·LiBH₄(ref 50)의 나노구조화도 같은 맥락.

#### (c) Micro–meso (nm–µm) — **입계와 기공** ★ DEM 접점 1
- nm–µm 조성/구조 불균일이 거시 σ 를 **지배** 할 수 있다 — 유리하게도(refs 48–50) 불리하게도(refs 51,52).
- **입계(GB)**: 대부분의 경우 **저항을 증가**시킨다. 기구 후보 — ① **양의 공간전하**(음이온 공공)가 이동 양이온을 밀어냄(ref 51), ② GB 가 **이온차단 불순물의 싱크**(ref 53), ③ 원자수준으로는 **결정립 misalignment 가 만드는 왜곡이 percolation 자체를 막는다**(ref 52).
- ★ **"The magnitude of the effect depends on the material and seems to be negligible for sulfide solid electrolytes"** (ref 54, Ganapathy/Wagemaker). **→ 황화물에서는 GB 화학이 아니라 접촉 기하(기공·접촉면적)가 지배 변수** = 우리가 주기셀 bulk DFT 를 쓰는 것에 대한 문헌 방어선이자, DEM 을 쓸 정당화.
- 반대 가능성도 열어둠: 특정 재료에서는 GB **표면을 따라** under-coordinated site 경로로 오히려 전도를 도울 수 있다.
- **기공/접촉** (이 절의 마지막 문단이 DEM 축의 원문):
  > *"Another source of resistance to ion transport … is **inadequate physical contact between solid particles**. In polycrystalline materials and composite electrodes, **the contact between solid particles must be maximized and maintained** … In contrast, **the existence of porosity implies the occurrence of tortuous paths for ion conduction and inhomogeneous current densities**. … Therefore, the **effective densification** of polycrystalline solid electrolytes and composite electrodes becomes crucial … but may represent a major challenge when the **mechanical properties and the processability** … are taken into account. **For both oxide⁵⁵ and sulfides⁵⁸, a decrease in porosity has been correlated with increased conductivity as a result of stronger grain–grain or particle–particle contact.**"*

#### (d) Macroscopic (µm) — 임피던스의 한계
- σ_macro 는 펠릿 임피던스로 측정. **각 성분(점접촉·GB·비정질·불순물) 분해는 "관측된 정전용량에 근거한 경험적 가설에 기댄 추상 모델 피팅"** 이 필요 — 리뷰가 이 방법의 취약성을 직접 인정한다.
- 결과: **그룹 간 σ·Ea 재현성이 약 1 자릿수** 산포(Na₁₁Sn₂PS₁₂ 사례). → **문헌 σ 절대값을 그대로 옮기지 말라는 경고를 리뷰 스스로 한다.**
- 도달값: Li⁺ 10 / Na⁺ 1 / Mg²⁺ 0.1 mS/cm — **액체(~10 mS/cm)와 직접 경쟁**.

#### (e) Device (mm) — ASR·접촉면적·percolation ★ DEM 접점 2
- **Z_device 는 σ_macro 로 예측 안 된다.** 예: Li₆PS₅Cl + 상용 LiCoO₂/NCM111/LiMn₂O₄ 조합에서 성능이 제한됨(ref 64). *"an electrolyte with much lower macroscopic conductivity can exhibit lower device impedance if it manifests more favourable compatibility with the electrodes."*
- **ASR = t/σ** (두께 무관 지표). *"The contribution of the ASRs to the overall impedance for a given material pair then only depends on the **area of ionic contact** between the solid electrolyte and active material, typically quantified in terms of **contact area per volume of composite**"*(ref 68) → **ASR 최소화 = 접촉면적 최대화**. 단, **"바로 그 접촉면적이 사이클 중 저항성 계면 형성·열화에 노출되는 면적"** 이라는 trade-off 를 명시.
- **부피분율 창**: 에너지밀도 + 전자 percolation → SE **< 50 %**; 이온 percolation 한계 회피 → SE **> 25 %** (둘 다 ref 68).
- **입도**: *"the above thresholds are also a function of **particle size (distribution)** in the composites and **smaller** electrode (and electrolyte) particle sizes promote **both lower electronic and ionic percolation thresholds**, respectively, and high active area of ionic contact available to charge transfer"*(refs 68,74,76).
- **공간전하** (`Fig. 4`, Eq.(4)): `V = −μ_Li/(qF)`. 계면에서 μ_Li 가 **수 mV·nm⁻¹** 로 급변 → **nm 급 공간전하층**. 고체는 액체보다 **유전율이 낮아 bulk polarization 을 못 하므로** 이 효과가 더 커질 수 있다.
- **`Fig. 4` figure-read**: SE 내부의 μ_Li 는 **평탄한 plateau**, 급경사는 양 계면에만. 초록 띠(= `Electrolyte stability window`, 양방향 화살표로 폭 표시) 안에 **SE bulk μ_Li 는 들어 있고, 음극(`V_anode`)·양극의 μ_Li 는 띠 밖**(아래·위)에 있다 → **분해 구동력은 bulk 가 아니라 계면에서 생긴다**는 그림. 하단 격자 만화: 음극쪽 = 사이트 대부분 채워짐(**공공 고갈 / 침입형 축적 → 양의 공간전하**), 양극쪽 = 대부분 비어 있음(**공공 축적 → 음의 공간전하**). x축은 "Solid electrolyte thickness (nm)", 눈금 없음.
  - ★ **초판 누락(2026-08-06 보강)**: 그림의 논지를 짊어지는 라벨이 **물음표 두 개**다 — 음극쪽 띠 아래 `Reduction to Li-rich interphase?`, 양극쪽 띠 위 `Oxidation to Li-poor interphase?`. **띠를 벗어난 구간에서 계면상이 생기느냐를 리뷰가 단정하지 않고 물음으로 남긴 것** — 우리 ESW onset 과 실험 CV 의 격차를 "속도론적 여유" 로 설명할 때 이 물음표가 그대로 근거가 된다.
  - ⚠ **크롭 잘림**: `fig_2.png` 와 달리 `fig_4.png` 는 **상단이 잘려** `μ_Li,cathode` 와 `Oxidation to Li-poor interphase?` 가 부분적으로만 보인다(위 내용은 PDF 원본 페이지로 확인).

### 5.3 Electrochemical stability (`Fig. 5`, `Table 1`)

- **용어 정리**(리뷰가 명시): **interface** = 두 상의 접촉 면적, **interphase** = 그 계면에서 전기화학 반응으로 **새로 생긴 상**.
- **3가지 반응 유형** (`Fig. 5a`, figure-read: 왼쪽 3패널이 각각 e⁻만 / 원자 E 만 / 둘 다 이동하는 그림):
  1. **Redox 분해** — `SE + ne⁻ ↔ SEⁿ⁻` (전자·이동양이온만 관여). Eq.(5) 가 예: Li₃PS₄ + Li → Li₄P₂S₆ + Li₂S → (더 환원되면) Li₃P + Li₂S. **부분 가역** 사례도 존재(Li₁₀GeP₂S₁₂ 단일물질 셀, ref 82).
  2. **화학 반응** — `xSE + yE → SEₓEᵧ` (전자 불필요). Eq.(6) O²⁻–S²⁻ 교환.
  3. **전기화학 반응** — `xSE + yE + ne⁻ → SEₓEᵧⁿ⁻`. Eq.(7) Li₃PS₄/LiCoO₂. 실제로는 화학량론 상이 아니라 **Co·S 나노결정 + P/Co/O/S 상호확산** 으로 나타남(TEM, ref 66).
- **안정창 계산법**: 분해반응 자유에너지를 전압의 함수로 → **Richards et al.(ref 65)의 μ_Li grand-potential 방법론**. Na(ref 84)·Mg(ref 85)로 확장되어 **안정창 라이브러리** 존재. 실제 창은 **속도론적 과전압**(Na₃PS₄ 기준 **±0.5 V**)만큼 넓어질 수 있고, 그 과전압 크기는 **전해질 내 하전종 이동도** 와 연결 → **"가장 잘 통하는 전해질이 가장 쉽게 분해된다"** 는 경향을 설명.
- ★★ **산화 한계 = 음이온이 결정**: *"The high-voltage oxidation stability of solid electrolytes is largely set by the anion framework and specifically its propensity to give up electrons, typically limited by **the anion with the lowest ionization potential**"* — 사다리 **N³⁻ < P³⁻ < H⁻ ≪ S²⁻ < I⁻ < O²⁻ < Br⁻ < Cl⁻ ≪ F⁻**(ref 65).
  **→ Li₆PS₅Cl 에서 가장 낮은 IP 음이온은 S²⁻ 이다. Cl⁻ 은 사다리에서 S²⁻ 보다 훨씬 위. 그러므로 Cl 을 늘려도 창의 상한은 여전히 S 가 pin 한다.** 이것이 우리 `axis ①`(intrinsic 0-pressure ESW onset = S-limited, comp1/modelc 모두 2.256 V 동일)의 **1차 문헌 근거**다.
- **환원 한계 = 양이온이 결정**: (비이동) 양이온의 **전자친화도**. 단, 전자친화도는 **구조·결합 특성에 좌우** — *"a phosphorus atom will be reduced more easily if **weakly bonded to sulfur** compared with when **strongly bonded to oxygen**, as exemplified by the increased stability of Li₃PO₄ compared with Li₃PS₄"*(ref 65). 나아가 **환원 안정성 ↔ 폴리음이온 단위의 결합 강성(bond stiffness)** 이 LISICON 계열에서 실험적으로 상관됨(ref 31, Muy).
  **→ 우리 O-도핑(LPSOCl)·B₂O₃ 라인의 물리가 여기 그대로 있다**: O 가 P 결합을 강화 → 환원 저항 ↑.
- 금속류 함유 SE(Ti in NASICON/perovskite, Ge in NASICON/LISICON/LGPS)는 저전압에서 **혼합전도 계면상(MCI)** 을 만들기 쉬워 위험.
- **`Fig. 5b` 계면 3시나리오** (figure-read, 2026-08-06 확대 재확인):
  - ⚠ **초판 정정**: `σ_xfc,ion ↑` / `σ_xfc,e⁻ ↓` 화살표는 **3패널 전부가 아니라 (2) Kinetic stabilization·(3) Artificial protection 두 패널에만** 붙어 있다. (1) Intrinsic stability 에는 `ΔG > 0` 만 있고 σ 화살표가 없다 — 반응이 없으니 계면상 전도도를 논할 필요가 없다는 뜻이라 **그림이 맞다**.
  - ★★ **논문 자체의 오류를 하나 찾았다** — `Fig. 5b` 는 **(2) Kinetic stabilization 에도 `ΔG > 0` 이라고 인쇄**해 놓았다. 그런데 **같은 그림의 캡션**은 *"(2) **kinetically stabilized decomposition**"* 이라 하고, **본문**은 *"**Given that reactivity is favoured**, the kinetics and consequently the extent of reaction are governed by the interfacial transport properties. If either is impeded, the reaction is blocked and the interface becomes kinetically stabilized"* 라고 한다. 즉 시나리오 (2)는 **분해가 열역학적으로 유리한(ΔG < 0) 채로 속도론이 막는 경우**이고, `ΔG > 0` 이면 그건 정의상 (1) Intrinsic stability 다. **⇒ `Fig. 5b`(2) 의 부호는 `ΔG < 0` 이어야 한다.** 인용할 때 그림을 그대로 옮기면 틀린다 (LiPON·garnet 예시도 전부 "분해가 일어나되 멈춘다" 쪽이다).
  - 패널 그림 자체는 일관된다: (1) 깨끗한 계면으로 Li⁺ 만 통과 / (2) 갈색 계면상이 생겼고 **e⁻ 는 빨간 ✗ 로 차단, Li⁺ 는 통과** / (3) 파란 인공 코팅층이 **e⁻ 차단, Li⁺ 통과**.
  - 세 시나리오의 내용:
  1. **본질적 안정 (ΔG > 0)** — 이상적이나 금속 전극과는 **거의 없다**. 예외: **Na-β-Al₂O₃ vs Na 금속**(ref 91). 논쟁 사례: 도핑 LLZO 가 Li 접촉에서 **약간 리튬화 → cubic→tetragonal 상전이**; tetragonal 이 σ 는 낮지만 **nm 급 필름이라 전도를 거의 안 막는다 = 이상적 계면상**(ref 92).
  2. **속도론적 안정화** — 분해는 하지만 계면상이 **이온전도 O / 전자절연 O** 이면 유한두께에서 멈춘다. **LiPON** 이 교과서 예: Li₃PO₄ + Li₃N 으로 분해되어 **nm 급·전기화학적 안정·이온전도성** 계면상 형성. **최악은 MCI** — 전자·이온 둘 다 통해 무한 성장 → 저항 폭증·금속음극 단락.
  3. **인공 보호** — 코팅(Li₄Ti₅O₁₂ ref 95, LiNb₁₋ₓTaₓO₃ refs 7,9, Li₁₋ₓB₁₋ₓCₓO₃ ref 96) — 주로 산화물, 주로 **양극쪽 산화 보호**. 기능 해석 두 갈래: **공간전하 완화** vs **전자·비-Li 원자 확산 차단**. 음극쪽 인공보호는 Li 는 시도되나 Na·Mg 는 **부족**. **dual-electrolyte**(환원 안정 SE 는 음극, 산화 안정 SE 는 양극) 도 대안.
  - 부수: SE 는 전극뿐 아니라 **도전재(카본)·집전체** 와도 redox 분해할 수 있다 → 코팅 전략을 **첨가제·집전체·전해질 입자 자체** 로 확장 필요.
- **`Table 1`** = 계면 캐릭터라이제이션 기법 카탈로그(기법 / 관측량 / **operando 가능?** / **서브마이크론 분해능?** / 대표문헌). **표 안에서 `X` 는 "해당됨" 체크 표시**다(빈칸 = 해당 없음, `NA` = 적용 불가). 계산은 두 줄뿐:
  - **"Phase diagrams from first principles"** — 조성·열역학 안정창 / operando `NA` / 서브마이크론 **빈칸** / refs 65,80.
  - **"Molecular dynamics"** — 원자구조·반응기구·확산도 / operando `NA` / **서브마이크론 `X` = 해당됨** / refs 84,138 (ref 138 = Cheng/Goddard, Li 전극/Li₆PS₅Cl 계면 reactive dynamics).
  - ⚠ 초판이 이 `X` 를 §5.3 에서는 "아니오", §9 에서는 "예" 로 엇갈리게 적었다 — **"예"가 맞다**(2026-08-06 정정). `Fig. 2` 가 MD 를 "직접 프로브" 로 분류한 것과도 일관된다.
- 계산의 한계 2가지를 리뷰가 못박는다: **(1) 상태도는 이미 아는 결정상 지식에 의존**(모르는 상은 못 찾음), **(2) 속도론적 안정화 효과를 명시적으로 못 담는다.**

### 5.4 Mechanics ★★ (`Fig. 6`) — 사용자 축 (2)

**전제**: *"the relationship between the mechanical properties of solid electrolytes and the performance of the solid-state battery is **still poorly understood**"* (2019 시점의 정직한 자백).

1. **외부 압력**: 랩 스케일에서 **전용 가압 셋업이 일상적**(refs 97,104). Zhang et al.(ref 13)은 **사이클과 함께 응력이 유의하게 진화** 함을 관측. → *"It is crucial to consider the solid-state battery as a **solid composite** and treat its **micromechanics**(ref 105), including its **resilience to form cracks** and the **delamination of interfaces**"* — **리뷰가 직접 "복합체 미세역학" 을 요구한다.**
2. **접착(adhesion)** = **electrochemomechanical coupling 의 대표 사례**. 기여 3성분:
   - **(1) 화학적 계면에너지 γ_xfc** — *"the difference in **bonding and coordination at the interface compared with the bulk**"*. ← **우리 `db/properties/adhesion.json` 의 γ_SE / W_ad 가 정확히 이 정의다.**
   - **(2) 접촉 두 상의 **격자 misfit** 에서 오는 기계적 변형**,
   - **(3) 계면 전하재배치에 의한 **정전 인력**(`Fig. 4`).
   - 실증: Li 금속 접촉각(wettability) 개선 처리 → 계면저항 ↓ (ref 106, "아마도 실접촉면적 급증 때문"). **Wang & Sakamoto(ref 107)**: **σ_adh(박리에 필요한 압력) ↔ Li/LLZO 계면저항** 직접 상관 → *"showing the direct link between **mechanical strength and effective ionic transport across interfaces**"*.
3. **전기화학 변형 ε_electrochemical (전기화학 충격)**: 전극이 삽입/탈리로 팽창·수축 → **국소 응력 → 균열·박리·입자 간 접촉상실**. 그 결과 **생긴 공극이 비활성 부피로 누적**. **액체와의 결정적 대비**: 액체에서는 전기화학 변형이 **정수압(hydrostatic)** 으로 균질 소산되고 액체가 새 공극을 **적셔 들어가 이온접촉을 유지** 하지만, 고체에서는 불가능. 또 음극/양극의 변형이 **불균등** 하여 **소자 스케일의 거시 압력 진화** 를 낳는다(ref 14). 완화책: **zero-strain 전극(Li₄Ti₅O₁₂)**(ref 13).
4. **탄성계수 E, G**: soft sulfide 가 응력수용에 유리하다는 통념. **그러나** — *"it has been demonstrated that such soft materials (for example, lithium thiophosphate glasses) **remain brittle and prone to fracture on stress**"*(ref 108). ← **"무르다 ≠ 안 깨진다"** 를 명확히 분리.
5. ★ **파괴인성 K_Ic**:
   > *"The resistance of solid materials to crack propagation is quantified by **fracture toughness, K_Ic, which is emerging as a determining factor** for charting the performance of solid-state batteries. **Bucci et al.**(ref 109) modelled the effects of **cycling-induced fracture**, namely **increased impedance and capacity loss**. They proposed that **high fracture toughness, typically exhibited by dense oxides**, is beneficial … **Unlike the elastic moduli, fracture toughness is heavily dependent on microstructural parameters, such as densification, grain size, impurities and the occurrence of pre-existing cracks and porosity.**"*
   그리고 결론:
   > *"DFT calculations can provide estimations for the **elastic moduli** of pristine materials, whose atomic structures are known(**ref 110 = Deng 2016**). However, the **fracture toughness greatly depends on the microstructure and will need to be determined experimentally.**"*
   **⇒ 이 리뷰의 판정: K_Ic 는 DFT 가 줄 수 없는 양이다.** 우리 repo 에 K_Ic 가 없는 것은 **누락이 아니라 방법론적 경계** 라는 뜻 — 다만 그 경계를 **넘는 도구가 DEM/FEM/CZM** 이라는 것도 같이 따라온다(§6).
6. **`Fig. 6` figure-read**: 육각 결정립으로 그린 SE 안에 **주황 지그재그 균열**이 뻗고 그 위에 `Fracture / K_Ic` 라벨 + 양방향 화살표(전파 방향). 균열을 가로지르려는 `Li⁺` 는 **빨간 ✗** 로 막힘 = **균열 = 이온 차단**. SE 에는 `E_SE, G_SE`, 전극(파란 곡면)에는 `E_E, G_E`. 왼쪽 아래 = **Adhesion** 영역에 `σ_adh, γ_xfc` 와 서로 당기는 작은 화살표들. 오른쪽 아래 = **Delamination** 영역에 `ε_electrochemical` 와 벌어진 갈색 계면선, 여기서도 Li⁺ 가 ✗. **눈금·수치는 없다.**
   - ★ **초판 누락(2026-08-06 보강)** — 이 그림에 `Li⁺` 가 **셋** 그려져 있고 **✗ 가 붙은 것은 둘뿐**이다: 균열을 건너려는 것(✗), 박리면을 건너려는 것(✗), 그리고 **Adhesion 영역에서 잘 붙은 계면을 ✗ 없이 통과하는 것**. 즉 그림 한 장이 **"역학적 온전함(접착 유지) = 이온 전달 유지 / 파괴·박리 = 이온 차단"** 을 3항 대비로 진술한다. 본문의 *"the direct link between **mechanical strength and effective ionic transport across interfaces**"*(ref 107) 가 그림에서 이렇게 구현돼 있다 — 우리 `adhesion.json`(W_ad) → 계면저항 서사의 시각 자료로 그대로 쓸 수 있다.

### 5.5 Box 1 — 금속 음극의 계면·전착 문제 ★★

**두 문제**: ① 환원성 → 전해질과 반응 → 저항 증가, ② **충전 중 불균일 전착 → 단락**. 고체가 액체보다 나을 것이라는 기대와 달리 **Na/Na-β-Al₂O₃**(ref 140)·**Ag/AgI·RbAg₄I₅**(ref 141)에서 오래전부터 관측됨. 그래서 실제로는 **Li–In, Li₄Ti₅O₁₂, Na–Sn** 같은 대체 음극을 쓴다.

**정량**:
- **CCD ≤ 0.3 mA/cm²** (실계면적 기준, 상온) vs **경쟁력 목표 3–10 mA/cm²** (ref 10) — **한 자릿수 이상의 격차**.
- CCD 를 좌우하는 인자: Li/SE 계면 **ASR**(refs 106,142), **온도**(ref 143), **전자전도도**(ref 137), **미세구조·표면 결함**(ref 12).
- 고체 셋업은 **가압 하에서 동작** 하고 사이클 응력이 추가된다 → 금속 음극은 **MPa 급 압축응력** 을 받는데 이는 **알칼리 금속 항복강도(Li ~0.8 MPa, ref 144)를 초과** 한다. **즉 Li 는 항상 소성 영역에 있다.**
- **Monroe–Newman 기준**(ref 145: 높은 전단탄성률이 안정 전착을 촉진)은 **고분자 전해질 얘기이고 무기 SE 에는 적용되지 않는다** — 이론적으로도(ref 146, Ahmad & Viswanathan PRL 2017) 실험적으로도(ref 12). 실증 스펙트럼:
  **soft thiophosphate glass (E ≈ 20 GPa, G ≈ 7 GPa, ref 108)** 부터 **stiff 단결정 garnet (E ≈ 150 GPa, G ≈ 60 GPa, ref 147)** 까지 **전 구간에서 Li 가 자란다.**
  오히려 **더 무른** 무기 SE/계면상(**LiBH₄, G ≈ 4 GPa**, ref 148)이 균질 전착에 유리할 수 있다는 반대 주장(ref 146)까지 소개.
- **파괴 기구 2단계**:
  (1) Li 가 **입계 및/또는 공극에서 우선 핵생성** — Li/SE 계면 불균일(거칠기·표면결함·낮은 접착·계면상 형성)이 **전류 핫스팟** 을 만든다. 핫스팟에 전류가 집중 → **고국소 압력·과전압**. **Li 의 몰부피가 어떤 무기 SE 보다 ~10× 커서** 극단적 국소 팽창 → SE 에 응력.
  (2) **균열이 결정립·입계·공극을 따라 전파** 하고 그 안으로 Li 가 침투 → 단락(ref 149). *"electrodeposition-induced mechanical failure is **counterintuitive**, given that metallic anodes typically have yield strengths that are **orders of magnitude lower** than those of the solid electrolytes"* — **약한 금속이 강한 세라믹을 쪼갠다** 는 역설을 명시.
  (3) 단락 후에는 전자전도로 전환 → **Joule 발열로 Li 용융** → 액체 Li 가 균열에서 흘러나와 단락이 일시 해제 → **전착 실험의 불규칙 전압 진동** 설명(refs 149,150).
  (4) 최근 제안: **전자가 SE bulk 를 관통해 음극에서 떨어진 곳에서 Li 를 직접 핵생성**(ref 137).
- **설계 원칙 6가지**: ① Li/SE 접착·젖음 개선(표면처리, ref 142) ② **기계적 폴리싱**(ref 143)·버퍼 박막 코팅(ref 106) ③ 분해를 설계해 **이온전도·전자차단 계면상** 유도(ref 151, LiI in Li₂S–P₂S₅) ④ **전극 미세구조화로 실표면적 증대 → footprint 당 CCD ↑**(ref 120, trilayer garnet) ⑤ **높은 K_Ic + 미세구조 제어(입경·기공률·기존 균열·기공 연결성)**(refs 55,12,138) ⑥ **SE 의 전자전도도 최소화**(ref 137).
- 리뷰의 결론: *"it is currently **unclear which of the aforementioned factors is the most crucial**"*.
- ⚠ Box 1 의 그림은 캡션이 *"Inhomogeneous Li deposition through solid electrolytes. **a**, … **b**, …"* 로 시작해 **"Fig. N" 표기가 없다** → 크로핑 도구가 앵커를 못 잡아 `litdb/figures/<slug>/` 에 **없다**. p.1286(PDF 9쪽) 원본 렌더로 확인했다(2026-08-06 재확인):
  - **패널 a `Inhomogeneous current`** — Li 금속(주황) 위 SE(연두 다결정). 불완전 접촉 자리와 **갈색 계면상**이 만든 두 지점으로 `Li⁺ current`(진한 주황 화살표)와 `e⁻ current`(연한 주황)가 **몰려들고**, 그 주변에 회색 `Stress field` 가 번진다 = **핫스팟**. 캡션: *"**Imperfect contact and interphase formation (brown) cause current hotspots**"*.
  - **패널 b `Crack propagation`** — 같은 구도에서 **입계·공극·결정립 내부** 세 자리에 검은 균열이 각각 뻗는다. 캡션: *"Preferential Li deposition in **grain boundaries, voids and/or within grains** creates localized stress resulting in fracture. **Li could be deposited directly in the bulk of solid electrolyte through electronic leakage if σ_el ≠ 0.**"*
  - **범례 5종**: Li⁺ current / e⁻ current / Stress field / Solid electrolyte / Li metal.
  - ★ 패널 a 는 **"불완전 접촉 → 전류 핫스팟"** 을 그림으로 못박는다 — 우리 DEM 축(접촉면적 분포)이 **전기화학적 실패**로 직결된다는 리뷰의 유일한 시각 진술이다.

### 5.6 Processing routes (`Fig. 7`) ★ — 사용자 축 (1) 의 나머지 절반

**3단계 파이프라인**: 합성 → **치밀화(densification)** → 집적(integration).

**(a) 합성 3경로**
| 경로 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **고상(shake & bake)** | 건분말 혼합 + 어닐 | 가장 직접적 | 고온·에너지 大, **휘발성분(Li₂O, Li₂S/S) 증발로 조성 제어 곤란** → 희생시약 필요(refs 29,55), 반응용기와의 반응성(refs 111,112) |
| **soft chemistry(용액)** | 용매 존재 하 반응 | **저온·스케일업 유리**, 순도·재현성 제어, **새 미세구조 창출로 수송 개선**(refs 48,56) | 용매 취급·회수 필요 |
| **mechanochemical(볼밀)** | 고에너지 입자 충돌 | 저온 반응(Li₆PS₅Cl, ref 113), **준안정상 핵생성**(cubic-Na₃PS₄, ref 114), 산업적으로 이미 존재 | **합성 파라미터↔산물 상관이 여전히 경험적**, 안전·에너지 때문에 스케일업 논쟁 중, **중량비·미디어·회전수 민감 → 재현성 문제** |

- 리뷰의 통찰: **높은 σ 는 종종 "준안정성"(양의 형성에너지)과 함께 온다**(Li₁₀GeP₂S₁₂ 및 그 Si 유사체 Li₁₁Si₂PS₁₂, ref 115) — **"높은 Li 이동도는 종종 안정성을 대가로 얻어진다."** 세 경로 모두 준안정상 접근이 가능한 이유는 각각 **급냉(고상)·충격에너지의 빠른 소산(볼밀)·용매–산물 상호작용과 표면효과(용액)**.

**(b) 치밀화** ★
> *"Solid electrolyte powders, regardless of the synthesis method, need to be further processed into high-aspect-ratio membranes or pellets. **High densification can be achieved through firing of green bodies (sintering) and cold or hot pressing of dry powders**, to achieve the desired microstructure(refs 25,116). **Softer materials such as sulfides and borohydrides might have a relative advantage against the typically refractory oxides due to their ability to be densified at low (even ambient) temperatures.** The method of reference is **spark plasma sintering**, which enables **precise control of the microstructure** and allows model experiments to probe its effects on ion transport(refs 51,117). However, such processing is currently **prohibitively costly**."*

**(c) 집적**
- **박막**만이 산업화된 경로(마이크로배터리)이나 **bulk 셀 스케일업에는 비용상 회의적**(ref 118).
- **냉간가압(cold-pressing) 건식 성분 = 랩 스케일 최다** 이나 *"its applicability for scale up and hard oxide solid electrolytes is **limited**"*(ref 118).
- **3D 전극 기하 설계가 핵심** — SE/전극 계면적 최대화 → 셀 전체 저항 최소화. mesostructured/interdigitated(마이크로배터리, ref 119), bulk 에서는 **porogen 을 쓴 'trilayer' 다공 SE 골격**(refs 118,120) 또는 **더 작은 양극 입자**(refs 76,121).
- **습식(용매) 경로의 장점 = 접촉면적**: 액체가 고체를 **적신 뒤 고체화** 되므로 solid–solid 계면을 만들기 쉽다. 보호코팅 대부분이 액상 전구체 유래(refs 70,95). 슬러리 공정은 **SE·활물질·도전재·바인더의 균질 혼합** 을 보장(refs 123,124) — **Li 이온전지 시트 전극 제조 흐름에 근접**(ref 73).
- **melt casting**: 저융점 antiperovskite Li₂OHCl 을 **녹여서 원하는 형상·두께로 직접 고화**(ref 126).
- **주변 안정성**: 황화물은 습기에서 **H₂S 방출**. HSAB(hard/soft acid–base) 개념으로 **공기 안정·수처리 가능** 조성 설계 — 예 **Na₃SbS₄**(ref 127). 산화물(LLZO·LISICON)도 **수화·양성자화·CO₂ 포획(탄산염 형성)** 으로 열화(refs 24,128).
- **`Fig. 7` figure-read**: 3열 색분류 — **파랑 = 건식(dry) 경로**, **초록 = 습식(wet) 경로**, **노랑 = 보조 방법**(High-energy ball mill, Spark plasma sinter — 즉 SPS 와 볼밀은 주 경로가 아니라 **어느 단계에나 끼워 넣을 수 있는 보조** 로 그려져 있다). 세로 3구역 = Synthesis / **Densification** / Integration. 종착점 2개: **'Pellet-type'**(파랑: Mix dry composite → Pelletize → (Sinter)) vs **'Sheet-type'**(초록: Mix composite slurry → Cast layer → (Infiltrate) → (Press and/or sinter)). 점선 = 단계 건너뛰기 경로.

### 5.7 Conclusions and outlook
- **물질탐색**: 고처리량 계산 + 실험. 전극도 **저·등방 부피팽창** 을 갖도록 새로 설계.
- **재료·계면 캐릭터라이제이션**: 국소 구조·기구·계면화학. **자가부동태(self-passivating) SE 동정** 이 핵심. **operando/in-situ** 로 **계면 반응과 압력 진화** 를 감시하는 새 실험법 필요.
- **공정과 소자 운전**: *"There are still many strategies to explore to further optimize both new and conventional electrolyte materials, such as chemical doping, novel synthesis/processing routes and **dense thin film preparation**. **Technical challenges to be addressed include developing highly scalable routes for synthesis and tailoring mechanical properties for stable operation of solid-state devices.** The definition of **reproducible protocols setting standards** in the synthesis of solid electrolytes and the assembly and cycling of solid-state batteries are crucial."*

---

## 6. ★★ DEM(이산요소법) 연결 — 별도 정리

> **결론 먼저**: 이 리뷰는 **DEM 을 하지 않고, DEM 이라는 단어도 없고, Bruggeman/tortuosity 식도 없다.** 그러나 **DEM 이 답해야 할 질문을 가장 권위 있는 형태로 정의해 놓은 문헌** 이다. 아래는 (i) 리뷰가 실제로 쓴 문장/숫자, (ii) 그것이 DEM 입력·출력으로 어떻게 번역되는지의 매핑, (iii) 우리 repo 앵커.

### 6.1 리뷰가 DEM 축에 실제로 준 것 (원문 기준, 6항목)

| # | 리뷰의 진술 | 정량성 | ref |
|---|---|---|---|
| D1 | **"입자 간 물리적 접촉 부족" 이 이온수송 저항의 독립적 원천**이며, 다결정·복합전극에서 **접촉을 최대화하고 유지** 해야 한다 | 정성 | — |
| D2 | **기공률 → tortuous 경로 + 불균일 전류밀도** → 거시 저항 증가 | 정성 (**식 없음**) | — |
| D3 | **기공률 ↓ ⇒ 전도도 ↑**, 기구는 **grain–grain / particle–particle 접촉 강화** — **산화물·황화물 양쪽에서 확인** | 정성(상관) | 55 / 58 |
| D4 | **ASR = t/σ**; 계면 임피던스 기여는 **"복합체 단위부피당 접촉면적"** 에만 의존 → **접촉면적 최대화**. 단, 그 면적이 곧 **열화 노출 면적** | 반정량 (정의) | 68 |
| D5 | **SE 부피분율 창: <50 %(전자 percolation·에너지밀도) / >25 %(이온 percolation)** | **정량 (2개)** | 68 |
| D6 | 위 문턱은 **입도 분포의 함수**; 입자가 작을수록 **전자·이온 percolation 문턱 둘 다 ↓**, 전하이동 유효면적 ↑ | 정성(방향) | 68,74,76 |
| D7 | 균열 전파 제어 = **입경·기공률·기존 균열·기공 연결성** | 정성 | 55,12,138 |
| D8 | **황화물·보로하이드라이드는 상온에서도 치밀화 가능**(연질), 산화물은 소결 필요. **냉간가압이 랩 표준**, 스케일업엔 제한 | 정성 | 118 |
| D9 | 금속음극은 **MPa 급 압축응력** 하에 있고 이는 **Li 항복강도 0.8 MPa 를 초과** → 항상 소성 | **정량** | 144 |

### 6.2 DEM 입력 파라미터 매핑표 ★ (우리가 만든 번역 — 리뷰에 없는 층위)

| DEM 입력/모델 요소 | 리뷰가 준 물리량 (§, ref) | 값 (소환) | 우리 repo 앵커 | 상태 |
|---|---|---|---|---|
| **법선 접촉강성 k_n** (Hertz: k_n ∝ E\* √R) | `E_SE`(`Fig. 6`), thiophosphate glass **E ≈ 20 GPa** (ref 108) | 20 GPa | `db/properties/elastic.json` relaxed-ion **E_VRH comp1 22.06 / modelc 27.66 GPa** | ✅ **거의 일치** |
| **접선 접촉강성 k_t** (∝ G) | `G_SE`, glass **G ≈ 7 GPa** (ref 108) | 7 GPa | 동 json **G_VRH comp1 8.13 GPa** | ✅ **거의 일치** |
| **소성 항복(EEPA/Thornton–Ning σ_y)** — SE 입자 | 없음 (리뷰는 "sulfide 는 상온 치밀화 가능"만) | n/a | 우리도 없음 | ❌ 공백 |
| **소성 항복 σ_y — Li 금속 입자/층** | **~0.8 MPa** (ref 144, Masias: elastic+plastic+**creep**) | 0.8 MPa | 없음 (우리는 Li 금속 역학 미계산) | ⚠ **DEM 쪽 소득** |
| **점착(JKR/DMT) 표면에너지 Δγ** | **γ_xfc** 정의 = "계면 vs bulk 의 결합·배위 차이" (§Mechanics) | **값 없음** | `db/properties/adhesion.json` **γ_SE(comp1) 1.211 J/m²**, W_ad(v2 melt) **1.107 ± 0.027 J/m²** | ⚠ 정의만 일치, 문헌 수치 없음 |
| **점착 파단응력 / pull-off** | **σ_adh** = "박리에 필요한 압력", **계면저항과 직접 상관 실증**(ref 107) | **값 없음** | W_ad → σ_adh 환산 미수행 | ⚠ 개념 다리만 |
| **입자 파쇄(bonded-particle breakage) 판정** | **K_Ic** (`Fig. 6`), "미세구조 의존 → **실험으로만**" | **값 없음** | 없음 (`fan2026` 리뷰의 **0.2–0.4 MPa·m¹ᐟ²** 가 litdb 유일 소환값) | ❌ **이 논문에서 소득 0** |
| **초기 패킹/상대밀도 목표** | 기공률↓⇒σ↑ (refs 55,58); 비활성 부피 최소화(`Fig. 1` 캡션) | 수치 없음 | `db/properties/cascade_v23_champions.csv` `anneal_dV_pct` (다른 축) | ⚠ 방향만 |
| **성형압 / 스택압 입력** | "MPa 급"(§Box 1) 외 수치 없음 | 반정량 | — (`miao2023` Table 1: 제조압 **50–510 MPa** 15행이 실제 앵커) | 다른 논문이 더 낫다 |
| **혼합 설계 제약 (SE 부피분율)** | **25 % ≤ φ_SE ≤ 50 %** (ref 68) | **정량** | DEM 조성 sweep 의 경계조건으로 바로 사용 가능 | ✅ **바로 쓸 수 있는 유일한 정량 제약** |
| **입도분포(PSD)** | "문턱은 PSD 의 함수, 작을수록 문턱↓·유효면적↑"(refs 68,74,76) | 정성 | `bielefeld2019…` / `schneider2023_particle_size_pressure_transport` digest | ✅ 방향, 수치는 원출처로 |
| **DEM 출력 → 유효 이온전도** | **ASR = t/σ**, 접촉면적/부피 (ref 68) | 정의 | `taufactor_tortuosity_factor_tomography_tool` digest, `bazzoun2026_dem_fem_rnm_ionic` | ✅ 출력 정의 일치 |
| **사이클 중 응력·박리** | **ε_electrochemical**, 음/양극 변형 불균등 → **거시 압력 진화**(ref 14) | 정성 | `bucci2017…czm`, `dem_mechanical_stresses_ssb_electrode_cycling` | ✅ |
| **마찰계수 µ** | **언급 자체가 없음** | — | — | ❌ 이 리뷰 밖 |

### 6.3 방법 사다리의 빈칸 = 우리 포지션 (★ 그림 기반 논거)

`Fig. 2` 하단 기법 바를 그대로 옮기면:

`Fig. 2` 하단 기법 바를 **픽셀 실측대로** 옮기면 (2026-08-06 재검증 — 초판의 눈대중 도면을 교체):

```
        Å         nm        µm        mm        cm
NMR     [==============]
MD      [==========]                                     <- 우리 MLIP-MD 여기
Imped.                     [========================]
Contin.              [==============================]
Diff/PDF[=======================================]
ElecMic [============================]
VibSpec [==================]
                           ^
        µm 칸은 4개 바(Contin./Diff-PDF/ElecMic/VibSpec)가 지난다 — 비어 있지 않다.
        비어 있는 것은 *스케일*이 아니라 *물리 축*이다:
        7개 바가 전부 이온수송·구조 프로브이고,
        역학량(강성·접착·소성·파괴)과 접촉 기하를 *산출*하는 방법은 단 하나도 없다.
```

- ⚠ **초판 정정**: 초판은 여기에 *"µm 칸에 방법 바가 없다"* 고 그렸는데 **그림과 다르다**. 첫 줄에서 NMR(…913 px)이 끝나고 임피던스(1058 px…)가 시작하며 µm 부근에 흰 틈이 생기는 것을 사다리 전체의 공백으로 오독한 것이다.
- **정정 후에도 우리 논거는 살아 있고 오히려 강해진다**: 리뷰는 `Fig. 2` 의 **Device(mm)** 칸에 **`Contact area` 를 서술자로 명시** 해 놓고, 그것을 **계산하는 방법은 사다리에 넣지 않았다.** `Continuum modelling` 은 접촉면적을 **입력으로 받는** 방법이지 **만들어내는** 방법이 아니다. 그리고 사다리에는 **역학 축 자체가 없다** — `Fig. 6` 이 `E/G·K_Ic·σ_adh/γ_xfc·ε` 를 성능 결정 인자로 세워 놓고도, `Fig. 2` 의 방법 사다리에는 그 양들을 산출하는 기법이 한 줄도 없다. **리뷰 내부의 두 그림이 서로 안 이어진다** (→ §14④).
- **DEM 은 정확히 그 빈칸을 채운다**: 입자 강성(E,G) + 점착(γ) + 소성(σ_y) + PSD + 성형압을 넣으면 **패킹·기공률·접촉면적·접촉수(coordination number)** 가 나오고, 그것이 곧 ref 68 의 "contact area per volume of composite" 이며 ASR 의 분모다.
- **∴ 우리 repo 이름(DEM-DFT)의 정당화가 이 그림 한 장으로 끝난다** — DFT 는 왼쪽 끝(E_hop, ν_hop, E/G/γ), DEM 은 가운데(접촉·기공), continuum/EIS 는 오른쪽. **두 끝을 우리가 다 갖고 있고, 리뷰가 비워 둔 가운데를 잇는 것이 기여다.**
- ⚠ 정직하게: 리뷰 저자들이 DEM 을 몰라서 뺐다기보다, **2019 년 시점에 SSB DEM 문헌이 거의 없었다**(우리 litdb 의 DEM 논문 대부분이 2020–2026). 즉 이건 "리뷰의 오류"가 아니라 **연대적 공백** 이고, 그래서 **"Famprikis 2019 가 정의한 빈칸을 2020년대 DEM 이 메웠다"** 는 서사가 성립한다.

### 6.4 DEM 관점의 원출처 추적 리스트 (이 리뷰에서 캐낸 것)
| ref | 문헌 | 왜 |
|---|---|---|
| **68** | **Bielefeld, Weber, Janek**, *JPCC* **123**, 1626 (2019) — Microstructural modeling of composite cathodes | **<50 %/>25 %·접촉면적/부피·percolation 문턱의 유일 원출처.** 우리 digest 있음 |
| **75** | **Froboese, …, Kwade**, *JES* **166**, A318 (2019) — Effect of microstructure on the ionic conductivity of an ASSB electrode | **Kwade 그룹(공정공학)** — tortuosity/미세구조↔σ 의 실측 원전. **우리 litdb 미보유 → 추천 1순위** |
| **76** | Strauss et al., *ACS Energy Lett.* **3**, 992 (2018) — cathode particle size ↔ capacity | 입경의 용량 영향 원전 |
| **74** | Braun, …, Ivers-Tiffée, *JPS* **393**, 119 (2018) | 연속체 모델로 ASSB 평가 |
| **55** | Kim, Y. et al., *J. Am. Ceram. Soc.* **99**, 1367 (2016) — **relative density ↔ mechanical properties of hot-pressed cubic LLZO** | **상대밀도–기계물성 직결**. DEM 검증용 |
| **58** | **Sakuda**, Hayashi, Tatsumisago, *Sci. Rep.* **3**, 2261 (2013) | 황화물 기공률↔σ. **우리 digest 있음** |
| **116** | Yi, Wang, Kieffer, Laine, *JPS* **352**, 156 (2017) — densification of cubic-LLZO 핵심 파라미터 | 소결 공정변수 |
| **118/139** | Schnell et al., *JPS* **382**, 160 (2018) / *EES* **12**, 1818 (2019) | **대량생산·비용** — DEM 공정 시나리오의 산업 맥락 |
| **137** | Shen, Dixit, Xiao, **Hatzell**, *ACS Energy Lett.* **3**, 1056 (2018) — **pore connectivity ↔ dendrite, 싱크로트론 X-ray 토모그래피** | **기공 연결성 = DEM 출력 그 자체.** 미보유 → 추천 2순위 |
| **144** | Masias et al., *J. Mater. Sci.* **54**, 2585 (2019) — Li 금속의 **탄성·소성·크리프** | **DEM 의 Li 접촉모델 파라미터 원전.** 미보유 → 추천 3순위 |

---

## 7. ★★ 기계적 물성 / 파괴 — 별도 정리 (사용자 축 2)

### 7.1 소득 판정표 (요청 항목별)

| 요청 항목 | 이 논문에 있나 | 값 | 판정 |
|---|---|---|---|
| **탄성계수 E** | **있음 (3세트)** | thiophosphate glass **20**, garnet **150**, — GPa | ✅ **소득** |
| **전단계수 G** | **있음 (3세트)** | glass **7**, garnet **60**, LiBH₄ **4** GPa | ✅ **소득** |
| **체적계수 B** | 없음 | n/a | ❌ |
| **Poisson ν** | 없음 | n/a | ❌ |
| **Pugh / 취성–연성 비 (G/B)** | **논의 없음** (수치도 없음). 대신 **"soft ≠ tough"** 라는 질적 명제 | n/a | ⚠ 개념만 |
| **파괴인성 K_IC** | **개념·기호만. 숫자 0** | **n/a** | ❌ **소득 없음** |
| **임계 에너지방출률 G_c** | 없음 (기호도 없음) | n/a | ❌ |
| **표면에너지 γ** | **γ_xfc 정의만** (계면 vs bulk 결합·배위 차) | **n/a** | ❌ 수치 없음 |
| **접착강도 σ_adh** | **정의 + 계면저항과의 상관 실증(ref 107)**. 숫자 없음 | n/a | ⚠ 개념 다리 |
| **임계 입자크기** | **없음** (입경이 K_Ic·percolation 에 중요하다는 서술만) | n/a | ❌ |
| **균열 핵생성/전파 기구** | **있음 (상세)** — Box 1 2단계 + `Fig. 6` | 정성 | ✅ 기구 소득 |
| **부피변화 ΔV 로 인한 응력** | **있음** — ε_electrochemical, **Li 몰부피 ~10×** | 반정량 | ✅ |
| **스택압 요구치** | **"MPa 급"** 서술만, 수치 없음 | n/a | ⚠ |
| **Li 침투/덴드라이트 역학 모델** | **있음** — 2단계 기구(핫스팟 핵생성 → 균열 전파 → Joule 용융). **wedge-opening 이라는 용어는 없음**; Monroe–Newman **부적용 판정** 명시 | 정성 + CCD 0.3 / 3–10 mA/cm² | ✅ **기구 소득** |
| **Li 금속 항복강도** | **있음 ~0.8 MPa** (ref 144) | **정량** | ✅ **소득** |

### 7.2 ★ 가장 중요한 한 줄 — 우리 relaxed-ion 값의 **독립 외부 실험 앵커**

> **ref 108 (McGrogan 2017, 나노인덴테이션 실측): Li₂S–P₂S₅ thiophosphate glass — E ≈ 20 GPa, G ≈ 7 GPa**
> **우리 (`elastic.json`, DFT PBE, **relaxed-ion**, stress–strain full C_ij): comp1 Li₆PS₅Cl — E_VRH = 22.06 GPa, G_VRH = 8.13 GPa**
> **우리 clamped-ion: E_VRH = 52.31, G_VRH = 20.12 GPa → 실측의 2.4–2.9배**

- **E 차 +10 %, G 차 +16 %.** 반면 clamped-ion 은 **2.4×(E)·2.9×(G)** 어긋난다.
- 이는 `elastic.json` 의 `vacancy_paradox_role` 주석("clamped-ion 이 experiment ~23 GPa 대비 2.3× 과대")을 **또 하나의 독립 문헌으로 확인** 한 것이고, **[Torii](full-DFT PBE-D3 relaxed-ion)** 과 **[Deng16](PBEsol ordered relaxed-ion)** 에 이어 **네 번째 외부 앵커** 다.
- ⚠ **"첫 실측 앵커" 라고 쓰면 틀린다** — `elastic.json` `vs_experiment` 가 이미 *"E_VRH 22.06 matches literature LPSCl (~23 GPa, e.g. He et al.); G_VRH 8.13 matches ~8 GPa expt"* 를 갖고 있다. 이번 값의 새로움은 **"또 하나의, 재료가 다른(유리) 독립 실측이 같은 자리를 가리킨다"** 는 데 있다.
- ⚠ **정직한 유보 3가지**: ① 재료가 다르다 — **Li₂S–P₂S₅ 유리** vs 우리 **결정질 argyrodite Li₆PS₅Cl**. ② 실측값은 **hot-press 시편의 값** 이라 **잔류 기공·GB 가 포함** → 진짜 단결정 값보다 **낮게** 나올 수 있다(즉 우연히 우리 값과 가까워졌을 여지). ③ 리뷰는 이 값을 **"≈"** 로만 인용하고 오차·시편 밀도를 안 준다. **∴ "우리 값이 실험으로 검증됐다" 라고 쓰지 말고, "같은 자릿수·같은 E/G 비(2.7–2.9)에 있고 clamped-ion 은 배제된다" 까지만.**
- 참고로 E/G 비: 실측 20/7 = **2.86**, 우리 relaxed 22.06/8.13 = **2.71**, 우리 clamped 52.31/20.12 = **2.60**. 비율은 셋 다 비슷하므로 **판별력은 절대값에 있다.**

### 7.3 K_IC 소득이 "0" 이라는 사실의 의미 (부정 결과도 결과다)
- 이 논문은 **K_Ic 를 "결정 인자로 부상 중" 이라고 격상시켜 놓고, 값을 하나도 주지 않는다.** 2019년 시점에 **황화물 SE 의 K_Ic 문헌이 사실상 없었다** 는 뜻이다.
- 그리고 **"fracture toughness … will need to be determined experimentally"** 라고 못박는다 → **우리 DFT 캠페인이 K_Ic 를 안 내놓는 것은 결함이 아니다.**
- litdb 전체에서 K_Ic 수치를 가진 유일한 소환값은 **`fan2026` §3.5 의 0.2–0.4 MPa·m¹ᐟ²** 이고, 그것도 리뷰의 재인용이다. **→ 우리가 K_Ic 를 다루려면 (i) 실험 협업 또는 (ii) DEM/CZM 에서 K_Ic 를 *입력 파라미터로 sweep* 하는 방식뿐이다.** 후자가 우리 repo 구조에 맞는다(`bucci2017…czm` = 이 리뷰 ref 109 와 동일 논문).

### 7.4 Monroe–Newman 판정 — 우리 §C 축의 정리에 직접 걸림
- 리뷰의 판정: **"무기 SE 에는 적용되지 않는다"** — 이론(ref 146 Ahmad & Viswanathan PRL 2017)과 실험(ref 12, E 20→150 GPa 전 구간에서 Li 성장) 양쪽.
- 우리 `comparison_vs_ours.md` §C 의 Monroe–Newman 주석(줄 324·331)은 **[Rupp]/[Miao23] 기준으로 "G≥2G_Li" 를 소개** 하고 있는데, **이 리뷰(2019, Nature Materials)가 그보다 앞서 그 기준을 무기 SE 에 대해 기각** 한다. `fan2026` 이 Monroe–Newman 을 아예 안 쓰고 K_Ic 로 갈아탄 것도 이 계보에서 설명된다.
- **∴ 우리 문서의 "두 기준이 대체인지 보완인지 미정" 이라는 미결 항목에 답이 하나 붙는다: Famprikis 2019 는 "대체" 쪽이다(Monroe 기각 → 파괴역학으로 이동).**

---

## 8. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | Bipolar 적층 SSB 셀 모식도 + 인셋 3개 = 고체전해질의 3대 도전: (1) 금속음극 불균일 전착(수지상), (2) 계면(이온 차단 계면상), (3) **물리적 접촉**(양극 구형 입자가 SE 표면에 점접촉만). 캡션이 "**비활성 부피(SE·집전체·기공률)를 최소화하라**"를 명시 | **인셋 (3) = DEM 그림 그 자체** — 우리 DEM 캠페인의 "왜"를 한 장으로 설명하는 슬라이드. deck 1페이지 후보 |
| 2 | **다중스케일 사다리** Å→nm→µm→mm→cm 와 각 스케일 서술자(E_Hop·ν_Hop / σ_crystal·σ_GBi·σ_amorphous / σ_meso / **ASR charge transfer·Contact area·ASR xface** / σ_macro·Z_SSB) + 하단 기법 스팬 바 7개. **진파랑 = 이온수송 직접·정량 프로브(NMR·MD·임피던스·continuum), 연파랑 = 보조(회절/PDF·전자현미경·진동분광)** | ★★ **우리 포지셔닝 도면**. DFT/MLIP-MD = 왼쪽 끝이며 리뷰 분류상 **"직접 프로브"** 등급. ⚠ **µm 칸이 비었다는 초판 서술은 오독**(4개 바가 지난다) — 실제 공백은 **역학·접촉 기하를 산출하는 방법이 사다리에 아예 없다**는 것. §5.2 픽셀 실측표·§6.3 참조 |
| 3a | 세 가지 양이온 이동 기구: 공공 / 직접 침입형 / **협동(interstitialcy)**. 안정·준안정 사이트를 색으로 구분 | 우리 BVSE 채널·MLIP-MD 확산 해석의 용어 고정 |
| 3b | 이중우물 에너지 프로파일 — E_m, hop 거리 α₀, 우물 곡률로 표현된 시도진동수 ν₀ (점선으로 곡률 변화) | Eq.(2) prefactor 를 그림으로 이해. 우리 Ea 만 보고 σ₀ 를 무시하면 안 된다는 시각적 근거 |
| 3c | 협동(interstitialcy) 프로파일 — **E_m^interstitialcy(준안정 사이트 기준)가 안정 사이트 기준 장벽의 절반쯤**. 거리 라벨 둘: **α₀ = 전하/결함이 옮겨간 거리(준안정→준안정), α₀' = 개별 이온의 변위(≈0.48 α₀)** | Cl-rich 의 D 증가를 "장벽 저하 + 협동" 으로 설명할 때의 도식. ⚠ Eq.(2)의 `α₀²` 에 들어가는 건 **긴 쪽 α₀** — "α₀' 때문에 σ₀ 가 상쇄된다"는 초판 해석은 철회(§5.2·§17-⑥) |
| 4 | SE 두께(nm)에 따른 μ_Li / 전압 프로파일. 안정창(초록 띠) 안에 **SE bulk μ_Li 는 들어 있고 양 전극 μ_Li 는 밖**; 계면에서만 급경사(**수 mV/nm**); 음극쪽 공공 고갈(양의 공간전하) / 양극쪽 공공 축적(음의 공간전하) | 우리 grand-potential ESW 가 **bulk 열역학** 임을 명확히 하는 그림. "onset 2.256 V" 는 이 띠의 상단이고, 실제 분해는 계면에서 시작한다 |
| 5a,b | (a) 계면 반응 3유형 = redox / chemical / electrochemical 반응식과 모식도. (b) 기능하는 계면 3시나리오 = 본질안정(ΔG>0, σ 화살표 없음) / **속도론적 안정화**(σ_xfc,ion↑ σ_xfc,e⁻↓, 갈색 계면상이 e⁻ 만 ✗) / **인공보호**(파란 코팅층이 e⁻ 만 ✗) | 우리 SEI/코팅 축(B₂O₃·Nd·LPSOCl)이 어느 시나리오를 노리는지 라벨링. `miao2023` F2 분류의 원형. ⚠ **그림 (2)의 `ΔG > 0` 은 논문 오식 — `ΔG < 0` 이어야 한다**(캡션·본문과 모순, §14-11). 슬라이드로 옮길 때 부호 교정 필수 |
| 6 | **기계적 열화 종합도**: SE(E_SE,G_SE)·전극(E_E,G_E), **Fracture K_Ic** 로 라벨된 균열이 결정립을 관통하며 **Li⁺ 경로를 ✗ 로 차단**, 왼쪽 **Adhesion(σ_adh, γ_xfc)**, 오른쪽 **Delamination(ε_electrochemical)**. **Li⁺ 가 셋 그려져 있고 ✗ 는 둘 — 균열·박리는 ✗, 잘 붙은 Adhesion 계면은 ✗ 없이 통과**. 수치·눈금 없음 | ★★ **우리 기계 축의 지도**. adhesion.json(γ_xfc·σ_adh 칸) / elastic.json(E,G 칸) / **비어 있는 K_Ic 칸** 을 이 그림 위에 그대로 표시하면 캠페인 공백도가 된다. 3항 Li⁺ 대비 = "역학적 온전함 ↔ 이온 전달" 을 한 장으로 보여주는 슬라이드 |
| 7 | 합성→치밀화→집적 공정 흐름도. **파랑=건식 / 초록=습식 / 노랑=보조(볼밀·SPS)**, 종착 **'Pellet-type' vs 'Sheet-type'** | 우리 DEM 시나리오(냉간가압 pellet vs 슬러리 sheet)가 이 그림의 어느 가지인지 고정. 건식전극 digest 계열과 연결 |
| Table 1 | 계면 캐릭터라이제이션 기법 카탈로그 — 기법 / 관측량 / operando 가능 / 서브마이크론 분해능 / 대표문헌. **계산은 "first-principles phase diagram" 과 "MD" 두 줄뿐** | 우리 계산이 실험 어느 칸을 대체/보완하는지의 지도. **계산 줄이 2개뿐이라는 사실 자체가 2019년 계산의 위치** |

> ⚠ **크로핑 상태 (2026-08-06 재투입 검증 후)**: 도구가 8장(fig 1–7 + Table 1)을 뽑았다.
> - ✅ **`fig_1.png`·`fig_4.png` 는 상단 잘림을 복구해 다시 뽑았다** — 이제 `(1) Metallic anodes`/`(2) Interfaces` 인셋 라벨과 `V_cathode`·`μ_Li,cathode`·`Oxidation to Li-poor interphase?` 가 모두 들어 있다(캡션 앵커 bbox 를 위로 24/29 pt 확장, `figures.json` 의 `recrop` 필드에 기록). 초판 digest 가 "잘림" 이라 적어 둔 부분은 **더 이상 유효하지 않다**.
> - ⚠ **`fig_3.png` 는 여전히 패널 a 가 없고 b 부터 시작하며 오른쪽에 본문 한 단이 들어와 있다** — 패널 a(3가지 이동 기구 모식도)는 페이지 렌더로만 확인.
> - ⚠ **Box 1 의 그림은 캡션이 "Fig. N" 이 아니라 `Inhomogeneous Li deposition through solid electrolytes. a, … b, …` 여서 추출 자체가 안 된다** — PDF 9쪽(p.1286) 원본 렌더로 확인(§5.5 에 상세 기술).

---

## 9. DFT/계산 방법 ★

> **이 논문은 자체 계산을 하지 않는다.** 아래는 리뷰가 **소개·평가하는** 계산 프레임이다. 조성별 code/functional/k-mesh 등은 **일절 없다**.

- **code / version**: n/a
- **functional / vdW / pseudo / k-points / ecut / supercell / DFT+U**: **전부 n/a**
- **리뷰가 다루는 계산 방법 4종**:
  1. **First-principles 상태도 + grand-potential 안정창** — **Richards et al.(ref 65)** 의 μ_Li proxy 방법론이 표준으로 제시됨. Na(ref 84)·Mg(ref 85)로 확장. **`Table 1`** 에 "Phase diagrams from first principles / 조성·열역학 안정창 / operando NA / 공간분해 NA" 로 등재.
     → **우리 `get_element_profile` 기반 ESW(2.256 V) 가 바로 이 계열이다.**
  2. **Molecular dynamics** — 확산도·반응기구·원자구조. `Table 1` 에 "operando NA / **서브마이크론 분해능 O**" 로 등재(refs 84,138 — ref 138 = Cheng/Goddard, **Li 전극/Li₆PS₅Cl 계면 reactive dynamics**).
     ⚠ 리뷰는 **AIMD 의 한계를 명시**: *"Due to the large system sizes required for satisfactory statistical analysis, direct probing of ion dynamics at the atomic scale by **ab initio molecular dynamics calculations can be difficult**"*(ref 18) — 특히 비정질.
  3. **ML 유도 고전 퍼텐셜(MLIP)** — 위 한계의 대안. **비정질 Li₃PO₄ 의 neural-network potential**(ref 47)을 "promising alternative" 로 명시.
     → **우리 UMA-s-1p1 MLIP-MD 노선의 문헌 정당화가 여기 있다.**
  4. **탄성계수 DFT** — *"DFT calculations can provide estimations for the elastic moduli of pristine materials, whose atomic structures are known"* (**ref 110 = Deng, Wang, Chu, Luo, Ong 2016**). **단, K_Ic 는 불가 → 실험으로만.**
  - 그 외 **continuum modelling** 을 `Fig. 2` 기법 바에 nm–cm 스팬으로 넣음(우리 DEM/FEM 축의 상위 카테고리).
- **무질서 처리**: 리뷰 차원에서 **언급 없음**(SQS·enumerate 등 단어 없음). 다만 비정질 취급 논의(PDF+RMC, Ea 분포)가 무질서의 질적 대응.
- **리뷰가 밝힌 계산의 구조적 한계 2가지** (그대로 인용 가능):
  - **(1) 상태도는 "이미 알려진 결정상"에 의존** — 미지의 상은 원리적으로 못 본다.
  - **(2) 속도론적 안정화 효과가 명시적으로 안 담긴다** — 그래서 계산창이 실제보다 좁게 나온다(Na₃PS₄ 기준 ±0.5 V 여유).

---

## 10. Post-processing ★

리뷰가 **표준으로 제시** 하는 후처리/해석 도구 (우리 파이프라인 대응 표기):

| 후처리 | 리뷰에서의 역할 | 우리 대응 |
|---|---|---|
| **Grand-potential 분해 에너지 → 안정창** | ESW 계산의 표준(ref 65) | `get_element_profile` (GG phase set, LiS4/SCl₃/Li₅PS₄Cl₂ 제외) → onset 2.256 V |
| **MSD → D → Nernst–Einstein σ** | Eq.(3), **Haven ratio H_R** 포함. ★ **상관 이동 시 유효성 논쟁 명시**(ref 39) | `tools/ionic/` MSD 2–50 ps 창, NE(H_R=1) — **리뷰가 우리 "σ 절대값 인용 금지" 규율을 지지** |
| **Arrhenius 피팅** | Eq.(1), **m ≈ −1 prefactor** 주의 | 우리는 **D 기반 Arrhenius**(600/800/1000 K) → T^m prefactor 문제 없음. 단 σ 로 환산해 피팅하면 σT vs σ 선택이 Ea 를 흔든다 |
| **PDF (총산란) + reverse Monte Carlo** | 비정질 구조·확산경로 시각화(refs 42–44) | 우리 미사용 (비정질 SEI 축에서 향후 후보) |
| **포논/음속 → Debye 진동수 → 시도진동수 ν₀** | Kraft(ref 29) 상관 | `kraft2017…` digest, 우리 phonon/ε∞ 라인 |
| **비탄성 중성자산란 → 포논 밴드센터 ↔ Ea** | Muy(ref 31) | 우리 미보유(실험) |
| **QENS** | paddle-wheel 회전 직접 증거(refs 35,36) | 우리 미보유 |
| **임피던스 등가회로 분해(정전용량 기준)** | σ_bulk/σ_GB/계면 분리 — **"경험적 가설 기반"** 이라고 리뷰가 자인 | `kim2025_impedance_decoupling_tlm_assb` digest |
| **XPS / TEM / ToF-SIMS / NDP / X-ray 토모그래피** | `Table 1` 계면 관측 카탈로그 | `db/properties/xps_reference_sei.csv` 앵커, `taufactor` (토모그래피→tortuosity) |

- **도구 이름(pymatgen·VESTA·LOBSTER 등) 은 하나도 안 나온다.** 리뷰 레벨이라 방법론 이름만.
- ⚠ **ICOHP/COHP·Bader·ELF·BVSE·NEB 는 이 리뷰에 없다.** 우리가 쓰는 결합·전하 분석 축은 이 리뷰의 사각지대.

---

## 11. 우리 DFT/캠페인 대비 → `../our_dft_baseline.md`

> **규율**: 아래 "이 논문" 열은 전부 **소환값**(2차 인용)이며 우리 절대값과 같은 축에 합치지 않는다. σ 절대값은 우리 쪽을 **적지 않는다**(CLAUDE.md). band gap 은 이 논문이 아예 안 다루므로 대조 자체가 없다.

| # | 항목 | 이 논문 (소환값·ref) | 우리 | 판정 / 이유 |
|---|---|---|---|---|
| 1 | **E (thiophosphate)** | **≈ 20 GPa** (glass, 나노인덴테이션, ref 108) | **relaxed-ion E_VRH comp1 22.06 / modelc 27.66 GPa** (PBE, full C_ij) | ✅✅ **정합(+10 %)**. **clamped-ion 52.31 은 2.4× 어긋나 배제** → `vacancy_paradox_role` 의 **네 번째 외부 앵커**([Deng16]·[Torii] 계산 + `elastic.json` 이 이미 갖고 있던 실측 ~23 GPa(He et al.)에 더해). ⚠ 재료 다름(유리 vs 결정 argyrodite), 시편 기공 포함 가능 → "검증됐다" 금지 |
| 2 | **G** | **≈ 7 GPa** (동 ref 108) | **G_VRH comp1 8.13 GPa** | ✅ **정합(+16 %)**. clamped 20.12 은 2.9× |
| 3 | **E/G 비** | 20/7 = **2.86** | relaxed 2.71 / clamped 2.60 | ⚠ **판별력 없음** — 비율은 셋 다 비슷. 판별은 **절대값**에서만 |
| 4 | **산화물 기준점** | garnet **E 150 / G 60 GPa** (ref 147) | 우리 계열 없음 | ✅ 스펙트럼 고정: 우리 argyrodite 는 **가장 무른 끝**(20–28 GPa). CAM(산화물, E 150–200) 과의 변형 불일치 서사와 일치 |
| 5 | **K_IC** | **없음 (개념·기호만)** | **없음** | ❌ **소득 0**. 리뷰가 "**실험으로만 결정 가능**" 이라고 못박음 → **우리 DFT 공백은 방법론적 경계**. litdb 유일 소환값은 `fan2026` **0.2–0.4 MPa·m¹ᐟ²** |
| 6 | **γ (표면·계면 에너지)** | **γ_xfc 정의만**("계면 vs bulk 의 결합·배위 차") | `adhesion.json` **γ_SE(comp1) 1.211 J/m²**, W_ad(v2) **1.107±0.027 J/m²** | ⚠ **정의는 정확히 우리 W_ad(Dupré)**. 수치 대조 불가 |
| 7 | **σ_adh (박리 압력)** | 정의 + **계면저항과 직접 상관 실증**(Wang & Sakamoto, ref 107). 수치 없음 | 미계산 | ⚠ **개념 다리**: 우리 W_ad → σ_adh 로 넘어가면 "기계 ↔ 이온수송" 을 잇는 실험 대응량이 생긴다 (H-리스트 후보) |
| 8 | **Li 금속 항복강도** | **~0.8 MPa** (ref 144) | 없음 | ⚠ **DEM 입력 소득** — Li 는 스택압(MPa)에서 **항상 소성** |
| 9 | **산화 한계 = 최저 IP 음이온** | **N³⁻<P³⁻<H⁻≪S²⁻<I⁻<O²⁻<Br⁻<Cl⁻≪F⁻** (ref 65) | comp1·modelc **onset 동일 2.256 V** (S²⁻-limited); Cl 증량은 **onset 이 아니라 분해량·산물·계면** 에 작용 | ✅✅ **기전 수준 정합**. LPSCl 에서 최저 IP 음이온 = **S²⁻** 이므로 Cl 을 늘려도 상한은 S 가 pin. **우리 axis ① 의 1차 문헌 근거**. ⚠ 이 사다리는 **0-pressure bulk 열역학** 축이지 계면·구속 축이 아니다 — "Cl-rich 산화안정" 은 **축 명시 필수** |
| 10 | **환원 한계 = 양이온 전자친화도, 결합의존** | P–S 약결합 → 환원 쉬움; **Li₃PO₄ > Li₃PS₄**(ref 65). **환원 안정성 ↔ 폴리음이온 결합강성**(ref 31) | 우리 환원 한계 **1.242 V**, OCV 1.717 V; O-도핑 LPSOCl·B₂O₃ 라인 | ✅ **우리 O-도핑 전략의 물리 근거**. ⚠ 우리 ICOHP 는 **Li–X**(−1.86/−2.10) 라 "폴리음이온 P–S 강성" 과 **다른 결합** — 직결 인용 금지. P–S/B–S ICOHP 를 따로 뽑아야 대응된다 |
| 11 | **Nernst–Einstein 유효성** | **명시적 유보**: 다중 이온이 **강하게 상관** 되거나 **이방 경로** 면 Eq.(3) 타당성 논쟁(ref 39) | 우리 σ = NE(**H_R = 1**), **절대값 인용 금지·비율도 멀티시드만** (CLAUDE.md) | ✅✅ **우리 규율의 문헌 근거**. 아르지로다이트는 리뷰가 말하는 "highly correlated" 의 전형(협동 hop) → **H_R=1 가정은 근사** 임을 digest 레벨에서 명시 가능 |
| 12 | **σ 재현성** | 그룹 간 **약 1 자릿수 산포**(Na₁₁Sn₂PS₁₂) | 우리 σ 절대값 인용 금지 규율 | ✅ **같은 결론에 독립 도달**. deck 에서 "문헌 σ 를 그대로 못 쓰는 이유" 인용처 |
| 13 | **GB 효과** | 대부분 저항 ↑, **그러나 황화물에서는 무시할 만함**(ref 54) | 우리는 **주기셀 bulk** 만 계산 | ✅ **우리 bulk 계산의 문헌 방어선** (`miao2023` "냉간가압 100–300 MPa 에서 GB 가 수송을 크게 안 막는다" 와 동일 결론) |
| 14 | **연질 골격의 양날** | Ea ↓ **그러나** ν₀·ΔS_m ↓ → **prefactor σ₀ ↓** (refs 29,30) | 우리 Ea comp1 0.253 / modelc 0.224 eV (MLIP-MD, 단일궤적) | ⚠ **우리는 prefactor 를 따로 안 본다**. Cl-rich 가 Ea 를 낮춰도 σ₀ 가 같이 내려가면 σ 이득이 상쇄될 수 있다 → **D 비율만 보는 현 규율의 사각지대** (H-리스트 후보) |
| 15 | **공간전하층(SCL)** | nm 급, **수 mV·nm⁻¹** — 그러나 **두께·전위 수치 없음** | 미계산 | ⚠ **양쪽 다 정성** — `miao2023` 과 동일하게 **SCL 은 숫자 0** |
| 16 | **band gap / 전자구조** | **다루지 않음** (gap 수치 0회) | canonical gap comp1 2.066 / modelc 2.099 eV (fixed-occ nscf) | — **대조 항목 없음** (충돌도 없음) |
| 17 | **DEM / 미세구조** | **DEM 없음**, Bruggeman 없음. **φ_SE 25–50 %** 만 정량 | DEM 캠페인(`INDEX_DEM.md`) | ⚠ §6 참조 — **정량 제약은 이 두 문턱뿐**, 나머지는 방향성 |

### 11.1 우리 축 요약 (한 문단)
이 리뷰는 **우리 계산값을 바꾸지 않는다**(gap·σ·Ea 대조 항목이 아예 없다). 대신 **우리 방법 선택과 인용 규율 4가지를 외부에서 지지** 한다 — ① relaxed-ion 이 옳다(E/G 실측 앵커), ② ESW onset 은 S 가 pin 한다(음이온 IP 사다리), ③ NE(H_R=1) σ 절대값은 못 믿는다(상관 이동 유보 + 그룹 간 1자릿수 산포), ④ 황화물 bulk 주기셀 계산은 GB 를 무시해도 된다. 그리고 **한 개의 새 공백을 판다**: **Eq.(2) 의 prefactor σ₀** — Cl-rich 의 Ea 이득이 ν₀·ΔS_m 손실로 상쇄되는지 우리는 확인한 적이 없다.

---

## 12. 적용 인사이트

1. **★ `Fig. 2` 를 우리 캠페인 전체 지도로 쓴다.** 왼쪽 끝(Å)=DFT(E_hop, E/G, γ, ESW), 가운데(µm)=**DEM**(접촉면적·기공률·패킹), 오른쪽(mm–cm)=continuum/EIS. **리뷰가 `Contact area` 라는 서술자를 그려 놓고 그것을 만들 방법을 사다리에 안 넣었다** → 우리 repo 이름(DEM-DFT)의 존재 이유가 이 그림 한 장으로 정당화된다. **deck 표지 슬라이드 1순위.**
2. **★ 기계 축의 공백도를 `Fig. 6` 위에 그린다.** 네 라벨 중 **E_SE/G_SE = elastic.json ✅**, **γ_xfc/σ_adh = adhesion.json ⚠(정의만 대응)**, **ε_electrochemical = cascade `anneal_dV_pct` ⚠**, **K_Ic = ❌ 공백**. 이 그림 하나로 "우리가 어디까지 왔고 무엇이 남았나"를 리뷰어에게 보여줄 수 있고, **K_Ic 공백은 리뷰 자신이 "실험으로만 가능" 이라고 면책** 해 준다.
3. **★ relaxed-ion 판정에 독립 실측 앵커가 하나 더 붙었다.** [Deng16](계산)·[Torii](계산)·`elastic.json` 기존 실측 메모(~23 GPa, He et al.)에 이어 **[McGrogan via Famprikis](실측 E 20 / G 7 GPa, Li₂S–P₂S₅ 유리)** — **clamped-ion 2.4× 과대** 진단이 4중으로 굳는다. 원고 §mechanics 의 방어 문장으로 쓸 수 있다(단 **유리 vs 결정** 유보 명기).
4. **음이온 IP 사다리를 axis ① 문장에 박는다.** "Li₆PS₅Cl 의 산화 상한은 **사다리에서 가장 낮은 S²⁻ 가 pin** 한다(Famprikis 2019, ref 65 = Richards 2016). Cl⁻ 은 S²⁻ 보다 훨씬 위이므로 Cl 증량은 onset 을 옮기지 못하고 **분해량·산물·계면** 을 바꾼다" — 우리 comp1/modelc onset 동일(2.256 V) 결과의 **기전 설명문**이 그대로 완성된다.
5. **NE/Haven 규율에 각주를 단다.** 리뷰가 "강하게 상관된 이동에서는 Eq.(3) 타당성이 논쟁 중"이라고 명시하므로, 우리 MSD→NE σ 에는 **"H_R=1 은 근사, 협동 hop 이 우세한 아르지로다이트에서는 계통오차 방향 미상"** 각주를 붙이는 것이 정직하고 방어적이다.
6. **새 계산 아이디어 — prefactor σ₀.** Eq.(2)로 보면 Cl-rich 의 이득은 Ea 뿐 아니라 **ν₀(포논/Debye)·ΔS_m** 에도 걸린다. 우리는 이미 phonon/ε∞ 라인이 있으므로 **comp1 vs modelc 의 Debye 진동수 비교** 를 붙이면 "Ea 만 보는" 현 서사에 두 번째 다리가 생긴다(Kraft ref 29 와 직결).
7. **DEM 파라미터 조달표(§6.2)를 캠페인 문서로 승격.** 지금 DEM 입력 중 **E,G 는 우리 DFT 로 자급**, **γ 는 우리 adhesion.json 으로 자급(단 σ_adh 환산 필요)**, **σ_y(SE)·K_Ic·µ 는 외부 조달** 이라는 구도가 명확해졌다. 조달 대상 문헌 3편(ref 75 Froboese/Kwade, ref 137 Shen/Hatzell, ref 144 Masias)은 **아직 우리 litdb 에 없다**.
8. **공정 서사를 `Fig. 7` 가지로 고정.** 우리 DEM 시나리오가 **'Pellet-type'(건식 냉간가압)** 인지 **'Sheet-type'(슬러리 캐스팅)** 인지 그림의 가지로 말하면 건식전극 digest 계열(`mun2025`·`liu2025`·`lee2025_corolling`)과 한 축에서 이어진다.

---

## 13. 인용 가능 문장 (deck/paper 용)

- "고체전지의 최종 임피던스는 원자에서 소자까지 **모든 스케일의 함수** 이며(Famprikis 2019, Fig. 2), 그 사다리에서 **µm 입자 스케일의 접촉면적을 산출하는 방법은 비어 있다** — 본 연구의 DEM 은 그 칸을 채운다."
- "황화물 SE 의 산화 상한은 **음이온 이온화 퍼텐셜이 가장 낮은 종** 이 결정한다(N³⁻<P³⁻<H⁻≪**S²⁻**<I⁻<O²⁻<Br⁻<Cl⁻≪F⁻). Li₆PS₅Cl 에서 그 종은 S²⁻ 이므로, Cl 치환은 창의 **상한을 옮기지 않고** 분해량·산물·계면을 바꾼다."
- "고체전해질의 **파괴인성은 탄성계수와 달리 미세구조(치밀도·입경·불순물·기존 균열·기공)에 강하게 의존하며, 실험으로 결정해야 한다**(Famprikis 2019) — 따라서 K_Ic 는 원자수준 DFT 의 산출물이 아니라 **DEM/CZM 의 입력 파라미터** 로 다루는 것이 옳다."
- "**무르다는 것이 안 깨진다는 뜻이 아니다** — thiophosphate glass 는 E ≈ 20 GPa 로 무르면서도 **취성이며 응력에서 파괴** 된다(McGrogan 2017, via Famprikis 2019)."
- "Monroe–Newman 의 전단탄성률 기준은 **무기 고체전해질에는 적용되지 않는다** — 이론적으로도, 그리고 **E 20 GPa 유리부터 150 GPa garnet 까지 전 구간에서 Li 가 자란다** 는 실험으로도(Famprikis 2019, Box 1)."
- "복합양극의 SE 부피분율은 **전자 percolation·에너지밀도 때문에 <50 %**, **이온 percolation 한계 때문에 >25 %** 라는 창 안에 있어야 하며, 이 문턱은 **입도 분포의 함수** 다(Bielefeld 2019, via Famprikis 2019)."
- "면적비저항 ASR = t/σ 의 기여는 **복합체 단위부피당 이온접촉 면적** 에만 의존한다 — 즉 **접촉면적을 계산하는 일이 곧 계면 임피던스를 계산하는 일** 이다."
- "임피던스로 얻은 전도도와 활성화에너지는 **연구그룹 간 약 한 자릿수까지 벌어질 수 있다**(Famprikis 2019) — 문헌 σ 절대값을 우리 계산값과 직접 비교하지 않는 이유."

---

## 14. 주의 / 한계 (비판적으로)

1. **자체 데이터가 없다 — 전 수치가 2차 인용이고, 대부분 "≈" 로 반올림돼 있다.** E ≈ 20 / G ≈ 7 / G ≈ 60 GPa 처럼 **오차·시편조건·측정법이 삭제된 채** 전달된다. 특히 **McGrogan 값(ref 108)은 시편 밀도·기공률이 안 붙어 있어** 우리 단결정 DFT 와의 +10 % 일치가 **얼마나 우연인지 판정 불가**. → **"실험이 우리를 검증했다" 는 주장 금지.**
2. **K_Ic 를 "결정 인자"로 격상해 놓고 값을 하나도 안 준다.** 이건 리뷰의 게으름이라기보다 2019년 문헌 부재의 반영이지만, 결과적으로 **"중요하다"는 수사만 남고 설계에 쓸 수 있는 수는 없다.** 우리가 K_Ic 를 언급할 때 이 논문을 **수치 출처로 인용하면 안 된다**(개념 출처로만).
3. **미세구조 축이 전부 정성이다.** 기공률·상대밀도·tortuosity·성형압·입경 — **단 하나의 수치도 없다.** Bruggeman 같은 유효매질 식도 없다. **정량 제약은 φ_SE 25–50 % 두 개뿐이고, 그것조차 단일 출처(ref 68)의 재인용이다.** → DEM 논문에서 이 리뷰를 인용할 때는 **"문제 정의" 인용** 이지 **"파라미터 출처" 인용이 아니다.**
4. **`Fig. 2` 의 방법 사다리에 역학 축이 통째로 없다.** (⚠ 2026-08-06 정정 — 초판은 이것을 "µm 칸이 비었다" 로 잘못 적었다. µm 은 4개 바가 지난다. §5.2·§6.3 참조.) 실제 구멍은 **물리 축**이다: 7개 바가 전부 이온수송·구조 프로브이고, `Fig. 6` 이 성능 결정 인자로 세운 `E/G·K_Ic·σ_adh/γ_xfc·ε_electrochemical` 를 **산출하는 기법은 사다리에 한 줄도 없다.** `Contact area` 를 서술자로 그려 놓고 그 계산 방법을 안 넣은 것도 같은 결(continuum 은 접촉면적을 **입력으로 받는다**). 2019년 시점의 연대적 공백이지만, **본문 주장("접촉을 최대화·유지해야 한다")·`Fig. 6` 과 `Fig. 2` 의 방법 스팬이 서로 안 이어지는 지점** 이므로 그대로 지적 가능하다.
5. **"soft sulfide 가 유리" 와 "soft sulfide 는 취성" 이 같은 문단에 병치되고 화해되지 않는다.** 리뷰는 두 명제를 나란히 놓고 넘어간다 — **어느 조건에서 연성 이점이 취성 위험을 이기는지(입경? 변형률 속도? 기공률?)** 에 대한 판정이 없다. 우리 `fan2026`(>3 µm 파쇄 / <1 µm 완화)이 그 판정의 후속이다.
6. **Monroe–Newman 기각과 "더 무른 SE 가 유리할 수 있다"(ref 146) 사이의 처방이 불확정.** 리뷰 스스로 *"currently unclear which of the aforementioned factors is the most crucial"* 로 끝낸다. **∴ 이 리뷰로 "무르면 좋다/나쁘다" 어느 쪽도 결론짓지 말 것.**
7. **공간전하층(SCL)이 `Fig. 4` 로 크게 그려지지만 수치가 0.** 두께·전위 강하·용량 어느 것도 없다. **`miao2023`·`fan2026` 과 똑같이 SCL 은 여전히 정성** — 3편의 리뷰가 6년에 걸쳐 같은 그림을 그리고 같은 숫자 부재를 반복한다는 점 자체가 리뷰어 코멘트 소재.
8. **Nernst–Einstein 유보를 달아 놓고, 정작 본문 σ 값들은 그 유보 없이 인용한다.** Eq.(3) 의 타당성을 문제 삼은 바로 다음 절에서 σ_macro 10 mS/cm 를 무유보로 쓴다. 내부 일관성 결함.
9. **시점 한계(2019).** halide SE(Li₃YCl₆·Li₂ZrCl₆ 계열)가 **사실상 부재** 하고, 고엔트로피·건식전극·MLIP 대규모 MD·**SSB DEM** 이 전부 이후 문헌이다. **2026년 우리 캠페인의 "현재 지형" 근거로는 쓰지 말고, "축 정의"의 고전으로만 인용.**
10. **우리 축과 무관한 것도 분명히**: ICOHP/COBI·Bader·ELF·BVSE·NEB·DOS/PDOS 가 **한 번도 안 나온다.** 우리의 결합·전하 분석 축은 이 리뷰의 사각지대이므로 **"리뷰가 지지한다" 고 쓸 수 없다.**
11. **★ `Fig. 5b` 의 부호 오류 (논문 자체의 오식)** — **(2) Kinetic stabilization 에 `ΔG > 0` 이라고 인쇄**돼 있는데, 같은 그림 캡션(*"kinetically stabilized **decomposition**"*)·본문(*"**Given that reactivity is favoured** … the reaction is blocked and the interface becomes kinetically stabilized"*)과 정면으로 모순된다. **`ΔG < 0` 이어야 한다.** ΔG>0 이면 그건 정의상 (1) Intrinsic stability 다. **⇒ 이 그림을 슬라이드로 그대로 옮기면 오류를 승계한다** — 인용 시 부호를 고치거나 캡션·본문 쪽을 인용할 것. (2026-08-06 재투입 검증에서 확인)
12. **(우리 쪽 도구 한계 — 논문 비판 아님, 2026-08-06 처리 완료)** 캡션 앵커 크로핑은 **그림이 캡션 위쪽으로 페이지 상단까지 뻗으면 위를 자른다**. `fig_1.png`(인셋 (1)·(2) 라벨)·`fig_4.png`(`μ_Li,cathode`·`Oxidation to Li-poor interphase?`)가 그 사례였고 **둘 다 bbox 를 확장해 다시 뽑았다**. **남은 것은 `fig_3.png`(패널 a 없음)와 Box 1 그림(캡션에 "Fig." 가 없어 추출 불가)** — 이 둘은 크롭만 보고 인용하지 말고 원본 페이지(4쪽·9쪽)를 같이 볼 것.

---

## 15. 이 리뷰 ↔ 우리 litdb 의 교차점 (허브 논문으로서의 가치)

이 리뷰가 인용하는 문헌 중 **우리가 이미 digest 를 가진 것**:

| ref | 문헌 | 우리 digest | 리뷰 안에서의 역할 |
|---|---|---|---|
| **110** | Deng, Wang, Chu, Luo, **Ong** 2016, *JES* 163, A67 | `deng2016_elastic_superionic_electrolytes_dft.md` | **"DFT 로 탄성계수를 낼 수 있다"의 유일 근거로 인용** — 우리 relaxed-ion 최근접 앵커가 리뷰의 표준이라는 뜻 |
| **109** | Bucci, Swamy, Chiang, Carter 2017, *JMCA* 5, 19422 | `bucci2017_chemomech_failure_assb_cycling_czm.md` | **K_Ic 담론의 유일 근거** — 사이클 유도 파괴 → 임피던스↑·용량손실 |
| **68** | Bielefeld, Weber, **Janek** 2019, *JPCC* 123, 1626 | `bielefeld2019_microstructural_modeling_composite_cathode.md` | **φ_SE 25–50 %·접촉면적/부피·percolation 문턱의 원출처** (§6 의 뼈대) |
| **58** | Sakuda, Hayashi, Tatsumisago 2013, *Sci. Rep.* 3, 2261 | `sakuda2013_sulfide_mechanical_property.md` | 황화물 기공률↔σ 상관의 근거 |
| **65** | Richards, Miara, Wang, Kim, **Ceder** 2016 | `richards2016_interface_stability_pseudobinary.md` | **μ_Li grand-potential ESW 방법론의 원전** + 음이온 IP 사다리 |
| **12** | Porz et al. 2017 (Li 침투 기구) | (미보유) | Box 1 파괴 기구 |
| **29** | Kraft et al. 2017, *JACS* (격자 분극성) | `kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` | ν₀ ↔ Debye 진동수 상관 |

**추천 조달 (미보유·우선순위순)**
1. **ref 75** Froboese …**Kwade** 2019 *JES* 166, A318 — ASSB 전극의 **미세구조↔이온전도도** (tortuosity 실측). **DEM 축 최우선.**
2. **ref 137** Shen, Dixit, Xiao, **Hatzell** 2018 *ACS Energy Lett.* 3, 1056 — **기공 연결성 ↔ 덴드라이트, X-ray 토모그래피.** DEM 출력의 직접 검증 대상.
3. **ref 144** Masias et al. 2019 *J. Mater. Sci.* 54, 2585 — **Li 금속의 탄성·소성·크리프.** DEM Li 접촉모델 파라미터.
4. **ref 108** McGrogan et al. 2017 *AEM* 7, 1602011 — **"Compliant yet brittle"**, E/G 실측 원전(+ 시편 밀도). §7.2 유보를 없애려면 필수.
5. **ref 55** Kim, Y. et al. 2016 *JACerS* 99, 1367 — **상대밀도 ↔ 기계물성**(hot-pressed LLZO).
6. **ref 146** Ahmad & Viswanathan 2017 *PRL* 119, 056003 — Monroe–Newman 무기SE 기각의 이론 원전.
7. **ref 147** Yu et al. 2016 *Chem. Mater.* 28, 197 — LLZO 탄성 실측(산화물 끝점).

---

## 16. 기법 용어 미니사전

- **ASR (area-specific resistance)** — `ASR = t/σ`. 두께 t 를 모르거나 무의미한 계면에서 쓰는 두께 무관 저항 지표. 단위 Ω·cm². 계면상은 두께가 안 정해지므로 σ 대신 ASR 로 말한다.
- **Haven ratio H_R** — Nernst–Einstein 에서 **추적자 확산계수(MSD 로 얻는 것)** 와 **전하 확산계수(σ 로 얻는 것)** 의 비. 이온이 서로 독립적으로 뛰면 1, **협동적으로 뛰면 1 에서 벗어난다**. 우리 MLIP-MD σ 는 H_R=1 을 가정한다 → 근사.
- **σ₀ prefactor / 시도진동수 ν₀ / 이동 엔트로피 ΔS_m** — Eq.(2). 같은 Ea 라도 σ₀ 가 다르면 σ 가 다르다. ν₀ 는 우물 바닥의 진동수(≈Debye 진동수), ΔS_m 은 전이상태에서의 엔트로피 변화.
- **interstitialcy (knock-on, 협동/상관 이동)** — 침입형 이온이 이웃 격자 이온을 밀어내고 그 자리에 들어가는 기구. 개별 이온의 이동거리는 짧지만 전하는 멀리 간다. 아르지로다이트의 빠른 확산이 이 유형.
- **bcc 음이온 골격 기준** — 음이온이 체심입방으로 배열하면 사면체–사면체 직접 hop 이 가능해 Ea 가 낮다는 설계 규칙(Wang/Ceder 2015).
- **paddle-wheel 효과** — PS₄³⁻·BH₄⁻ 같은 폴리음이온의 **회전** 이 양이온 이동을 돕는 현상.
- **PDF (pair distribution function) + reverse Monte Carlo** — 총산란 데이터에서 **비정질의 국소 원자배열** 을 역산하는 방법. 결정학적 장거리 질서가 없을 때의 구조 도구.
- **QENS (quasi-elastic neutron scattering)** — ps–ns 시간대의 회전·확산 운동을 직접 보는 중성자 기법. paddle-wheel 증거의 출처.
- **interface vs interphase** — **interface = 두 상의 접촉 면적(기하)**, **interphase = 그 자리에 새로 생긴 상(화학)**. 리뷰가 명시적으로 구분한다.
- **MCI (mixed-conducting interphase)** — 전자·이온을 **둘 다** 통과시키는 계면상. 반응이 멈추지 않아 두께가 무한히 자라며 최악의 시나리오.
- **grand-potential (μ_Li) 안정창** — Li 화학퍼텐셜을 전압의 대리변수로 삼아 분해반응 자유에너지를 전압 함수로 그리는 방법(Richards 2016). 우리 ESW 계산의 원리.
- **ε_electrochemical (전기화학 변형/충격)** — 이온 삽입·탈리에 따른 전극 부피변화가 만드는 변형. 고체에서는 정수압으로 소산되지 못해 국소 응력·균열이 된다.
- **σ_adh / γ_xfc** — 각각 **박리에 필요한 압력**(측정 가능한 강도)과 **화학적 계면에너지**(bulk 대비 결합·배위 차이). 우리 W_ad(Dupré) 가 후자에 해당.
- **K_Ic (mode-I 파괴인성)** — 균열 선단의 응력확대계수 임계값. 단위 MPa·m¹ᐟ². **탄성계수와 달리 미세구조 의존이 커서 계산으로 못 낸다** 는 것이 이 리뷰의 판정.
- **CCD (critical current density)** — 그 이상에서 금속 전착이 불안정해져 단락에 이르는 전류밀도. 무기 Li SE 는 대개 ≤0.3 mA/cm²(실면적), 목표는 3–10.
- **Monroe–Newman 기준** — 고분자 전해질에서 "전단탄성률이 충분히 크면 덴드라이트가 억제된다"는 선형안정성 기준(2005). **무기 SE 에는 적용되지 않는다**(이 리뷰의 판정).
- **percolation 문턱** — 무작위 혼합물에서 한 상이 시료를 관통하는 연결망을 이루기 시작하는 부피분율. 전자(도전재)와 이온(SE) 각각에 대해 따로 존재한다.
- **tortuosity(굴곡도)** — 유효 경로 길이 / 직선 거리. 기공이 많을수록 이온이 돌아가야 한다. **이 리뷰는 단어만 쓰고 식·값은 주지 않는다.**
- **SPS (spark plasma sintering)** — 펄스 전류로 분말을 급속 소결. 미세구조 정밀 제어가 가능해 "기준 방법"이지만 비용이 금지적.
- **green body** — 소결 전, 분말을 성형만 해 놓은 상태의 성형체. 소결은 이것을 굽는 과정.

---

## 17. 재투입 검증 로그 (2026-08-06 · inbox #56 · 사용자 분류 `DFT`)

논문이 `litdb/inbox/56. Fundamentals of inorganic solid-state electrolytes for batteries.pdf` 로 다시 들어와, **실물 PDF 텍스트 + 크로핑 PNG 를 다시 열어** 초판 digest(2026-08-05, 590줄)를 대조했다. 최초 digest 는 임시 업로드본(`79dcf62a-…`)으로 작성됐고, **같은 파일임을 확인**했다(14쪽·Fig 7+Table 1+Box 1·Nature Materials 18, 1278–1291).

### 실제로 본 것 / 안 본 것
- **본 그림 (7/8)**: `fig_1` `fig_2` `fig_3`(b,c 확대 포함) `fig_4` `fig_5`(라벨 확대 포함) `fig_6` `fig_7` + **Box 1 그림**(크로핑 없음 → PDF 9쪽 원본 렌더).
- **안 본 것 (1/8)**: `tab_1.png` — 표는 이미지보다 PDF 텍스트가 정확해서 텍스트로만 읽었다(우리 관례).
- `fig_2` 의 기법 바 스팬은 눈대중이 아니라 **PIL 픽셀 실측**으로 뽑았다.

### 확인된 것 (변경 없음)
- 역학 수치 3세트(**E≈20/G≈7** thiophosphate glass ref108 · **E≈150/G≈60** garnet ref147 · **G≈4** LiBH₄ ref148), **Li 항복 ~0.8 MPa**(ref144), **CCD ≤0.3 vs 목표 3–10 mA/cm²**(ref10), **Li 몰부피 ~10×** — 전부 Box 1 원문 그대로.
- **음이온 IP 사다리** `N³⁻ < P³⁻ < H⁻ ≪ S²⁻ < I⁻ < O²⁻ < Br⁻ < Cl⁻ ≪ F⁻`(ref65) — 원문 일치.
- **φ_SE `<50 %` / `>25 %`**(ref68), **GB 는 황화물서 무시할 만함**(ref54), **과전압 ±0.5 V**(ref83), **LLZO 0.05 V·20 meV/atom**(ref65,80), **σ 10/1/0.1 mS/cm**(ref7/59,60/61), **18 C @100 °C**, **>10,000 cycles** — 전부 원문 일치.
- **K_Ic·γ 수치 0건** 판정 유지. `Fig. 6` 에 기호만 있고 본문은 "실험으로만 결정" 이라고 못박는다.
- `Fig. 6` `Fig. 7` `Fig. 1`(인셋 3) 의 초판 figure-read 서술은 **전부 그림과 일치**.

### 정정·보강 6건
| # | 항목 | 초판 | 정정 |
|---|---|---|---|
| ① | `Fig. 2` 기법 바 스팬 | Diffraction/PDF "nm~mm" · Vibrational "Å~nm" | **Å→cm** · **Å→µm** (픽셀 실측, §5.2 표) |
| ② | `Fig. 2` 사다리의 공백 | "**µm 칸에 방법 바가 없다**" | **오독** — µm 은 4개 바가 지난다. 실제 공백은 **역학·접촉 기하 산출 방법이 사다리에 전무**(더 강한 논거로 교체, §6.3·§14④) |
| ③ | `Fig. 2` 색 등급 | 언급 없음 | **진파랑 = 이온수송 직접·정량 프로브 / 연파랑 = 보조**. 리뷰가 **MD 를 NMR·임피던스와 같은 "직접 프로브" 등급**으로 분류 → **우리 MLIP-MD 라인의 리뷰급 정당화**(신규 소득) |
| ④ | `Fig. 5b` (2) Kinetic stabilization | 부호 미확인 | **논문이 `ΔG > 0` 으로 오식** — 캡션("kinetically stabilized **decomposition**")·본문("**reactivity is favoured**")과 모순, **`ΔG < 0` 이어야 한다**. 인용 시 교정 필수(§14-11) |
| ⑤ | `Fig. 5b` σ_xfc 화살표 | "오른쪽 **3패널**에" | **(2)·(3) 두 패널에만**. (1) 은 반응이 없어 애초에 불필요 |
| ⑥ | `Fig. 3c` 의 α₀ | "α₀' < α₀ ⇒ Eq.(2) 의 **α₀² 가 줄어 협동 이득이 상쇄**" | **철회** — σ₀ 에 들어가는 α₀ 는 **전하가 옮겨간 긴 거리**이고 α₀' 는 개별 이온 변위다. 그림대로면 협동은 **장벽↓ + hop 거리 유지 = 순이득**. `comparison_vs_ours.md` §A 해당 줄도 함께 정정 |

**추가 보강**: `Fig. 4` 의 물음표 라벨 2개(`Reduction to Li-rich interphase?` / `Oxidation to Li-poor interphase?`), `Fig. 6` 의 **Li⁺ 3개 중 ✗ 는 2개**(접착 계면은 통과), **Box 1 그림 패널 a/b 상세 + 범례 5종**, `Table 1` 의 `X` = 체크 표시(→ **MD 는 서브마이크론 분해능 O**, 초판 §5.3/§9 불일치 해소).

### 크롭 처리
- ✅ **`fig_1.png`·`fig_4.png` 재크롭 완료** — 상단 잘림(인셋 (1)(2) 라벨 / `V_cathode`·`μ_Li,cathode`·`Oxidation to Li-poor interphase?`)을 bbox 를 위로 24·29 pt 확장해 복구했다. `figures.json` 의 `bbox`·`w`·`h` 갱신 + `recrop` 필드 기록.
- ⚠ **`fig_3.png`** 은 여전히 패널 a 없음(b 부터, 오른쪽에 본문 한 단 유입) — 도구가 `Fig. 3` 캡션 아래만 잡는다.
- ⚠ **Box 1 그림은 추출 불가**(캡션이 `Inhomogeneous Li deposition through solid electrolytes. a, …` 로 "Fig." 가 없다). 이 둘은 원본 페이지(4쪽·9쪽) 병행 필수.
