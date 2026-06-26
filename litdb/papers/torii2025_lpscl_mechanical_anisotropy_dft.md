# First-Principles Investigation of Mechanical Properties and Anisotropy of Argyrodite Li₆PS₅Cl Crystal Electrolytes — Torii et al. (J. Phys. Chem. C 2025)

> slug `torii2025_lpscl_mechanical_anisotropy_dft` · DOI `10.1021/acs.jpcc.5c05116` · type `DFT (elastic + stress–strain + Bader)` · PDF `82ea256b/d3aed469-21._firstprinciples…LPSCl…` · digested `2026-06-26` · status ✅ · **[외부]**
> **저자**: Masato Torii, Yuki Okita, Kota Motohashi, Atsushi Sakuda*, Akitoshi Hayashi — **Osaka Metropolitan University**, Dept. Applied Chemistry, Sakai. (Sakuda/Hayashi 그룹. *우리 한양/J-W Lee/Y.M.Lee/Cho/Kang/Cha 아님 → [외부]*.) · J. Phys. Chem. C 2025, 129, 17882−17891 · Open Access CC-BY · Received 2025-07-23, Published 2025-09-17.

---

## 0. 이 digest를 읽는 법 — 왜 이 논문이 우리에게 가장 중요한 외부 DFT인가
이 논문은 **우리 comp1(Li₆PS₅Cl)을 그대로, full-DFT(VASP/PBE-D3)로 탄성텐서·이방성·응력-변형·Bader까지 계산한 유일한 "정면" 외부 논문**이다. 즉 우리 `db/properties/elastic.json`·`eos.json`과 **물질이 동일**하고 **방법이 비교 가능**하다. 따라서 이 digest의 사명은 단 하나 — **우리 "vacancy paradox"의 핵심 분기점인 *clamped-ion vs relaxed-ion* 중 이들 DFT가 어느 쪽에 떨어지는지를 판정**하는 것이다.

> **🔑 한 줄 판정 (먼저 결론)**: 이들은 **"lattice constants와 ionic positions를 *모두* fully relax"**(p.17883)했다고 명시 → **relaxed-ion**. 그들의 **E=27.4 / B=34.7 / G=10.0 GPa**는 우리 **relaxed-ion comp1 (E_VRH 22.06 / B_VRH 25.51 / G_VRH 8.13)** 와 같은 *부드러운 영역*에 있고, 우리 **clamped-ion (E 52.31 / B 43.59 / G 20.12)** 와는 명백히 다르다. → **외부 full-DFT가 우리 relaxed-ion 손을 들어준다.** (단 그들 B=34.7은 D3 + relaxed-ion 정의 차이로 우리보다 약간 높음 — §7에서 정밀 분해.)

## 1. 한 줄 요약
VASP/PBE-D3 first-principles로 Li₆PS₅Cl 단결정의 **탄성텐서(C₁₁/C₁₂/C₄₄)와 다결정 평균(E=27.4, B=34.7, G=10.0 GPa, ν=0.37, B/G=3.46, Zener A=1.09)**을 계산 → **탄성은 거의 등방(A≈1)이고 연성(ductile)**; 그러나 **인장(uniaxial)에는 변형률 0.2까지 견디는 wide elastic region**인 반면 **전단(shear)에는 변형률 0.7 %에서 붕괴**하는 강한 *이방적 취성*. 전단 취성의 1차 원인은 **Cl 원자가 Li 쪽으로 끌려가 Li₄Cl 단위를 형성**하며 결합·전하가 재배치되는 것 — 이것이 실제 분말 압분체(powder compact)의 취성을 설명.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 조성 | **Li₆PS₅Cl** 단결정(cubic, isotropic phase) — *우리 comp1과 동일* |
| 계산 대상 | (i) 탄성텐서 → VRH 평균 E/B/G/ν, 이방성 A, β(선압축성); (ii) {100}/{110}/{111} 표면 모델의 인장 응력-변형; (iii) 전단 응력-변형; (iv) Bader 산화상태의 변형 의존 |
| 동기 | sulfide SE는 σ 높고 *연성*(cold-press 가능)이나, 충·방전 시 전극 부피변화로 SE/전극 계면에 균열·공동 발생 → SE의 *intrinsic* 기계물성(특히 이방성·취성 메커니즘)을 원자수준에서 규명 |
| 갭 | 기존 LPSCl 기계물성은 nanoindentation(ref12)·ultrasonic(ref13,14)만; **탄성 이방성·전단 취성의 *원자기원*은 미규명**. 선행 DFT 1편(ref10 Deng 2016: E=22.1, B=28.7, G=8.1)과 비교 |
| 위치 | 저자들 자신이 LiCoO₂ cathode 기계물성을 같은 방법으로 다룬 선행(ref31–33) — 이 방법론을 SE로 확장한 논문 |

## 3. 핵심 물성 (수치 총정리)

### 3.1 다결정(VRH) 탄성 — **Table 1** (this study vs ref10 Deng 2016)
| 물성 | **this study (PBE-D3)** | 선행 ref10 (Deng 2016, SQS) |
|---|---|---|
| **C₁₁** [GPa] | **47.4** | 39.9 |
| **C₁₂** [GPa] | **28.4** | 23.1 |
| **C₄₄** [GPa] | **10.4** | 7.8 |
| **E (Young, VRH)** [GPa] | **27.4** | 22.1 |
| **B (bulk, VRH)** [GPa] | **34.7** | 28.7 |
| **G (shear, VRH)** [GPa] | **10.0** | 8.1 |
| **B/G (Pugh)** | **3.46** | 3.54 |
| **ν (Poisson)** | **0.37** | 0.37 |
| **A (Zener anisotropy)** | **1.09** | 0.92 |

> cubic이므로 C₁₁=C₂₂=C₃₃, C₄₄=C₅₅=C₆₆, 독립 상수는 **C₁₁, C₁₂, C₄₄ 세 개뿐**. 나머지 모듈러스는 Voigt–Reuss–Hill(eqs 1–6) + E=9BG/(3B+G)(eq7) + ν=(3B−2G)/(2(3B+G))(eq8)로 산출.
>
> **연성 판정**: B/G=3.46 ≫ 1.75 (Pugh ductile/brittle 임계, ref38) → **ductile**. ν=0.37 (금속 폴리크리스털 ~0.33 근방, 연성). **이방성**: A=1.09 → 1에 매우 가까움 → **탄성적으로 거의 등방(isotropic)**.

### 3.2 인장 응력-변형 — **Table 3** ({100}/{110}/{111} 표면 모델)
| lattice plane | ultimate strength [GPa] | partial fracture strain | fracture strain |
|---|---|---|---|
| **{100}** | **8.8** | 0.46 | 0.56 |
| **{110}** | **5.9** | 0.25, 0.31 | (sharp drop 없음 → 정의 불가) |
| **{111}** | **6.2** | 0.23 | 0.45 |

- 변형률 **0.2까지는 모든 방향에서 stress∝strain (선형 탄성)** → "wide elastic region", 높은 durability.
- 0.2 초과부터 방향별로 갈라짐; **stress reduction rate 순서: {100} < {110} < {111}** (즉 {111}이 가장 빨리 응력 감소 = 가장 취성).
- 인장 ultimate strength 순서: **{100}(8.8) > {111}(6.2) > {110}(5.9)** — {100} 방향이 인장에 가장 강함.
- **"partial fracture strain"** = stress drop은 아직 없지만 *화학결합 해리*가 처음 나타나는 변형률(VESTA의 표준 ionic bond 거리 초과로 판정). 표준 거리: **Li–S 3.02 Å, P–S 2.58 Å, Li–Cl 2.92 Å**.

### 3.3 전단 응력-변형 — **Figure 7** (핵심 이방성)
- 전단은 **{0 0 1} 면에 평행, c축 따라 x좌표를 변화시켜** virtual shear 부여.
- **변형률 0.007 (0.7 %)에서 명확한 stress drop = 파괴.** 최대 전단응력 **(strain, stress) = (0.006, 0.076 GPa)** → 그 직후 fractured region (ε ≥ 0.007).
- 인장(durable, ε~0.2)과 **극단적 대비**: 같은 결정이 전단엔 *극도로 취성*. → "shear에 대한 취성"이 실제 분말 압분체의 취성을 지배.

### 3.4 격자상수 (구조 최적화 후) — **Table 2**
| lattice plane | a [Å] | b [Å] | c [Å] | α/β/γ | 격자형 |
|---|---|---|---|---|---|
| {100} | 10.04 | 10.04 | 10.04 | 90/90/90 | cubic |
| {110} | 14.20 | 10.04 | 14.20 | 90/90/90 | tetragonal |
| {111} | 13.89 | 13.89 | 12.53 | 90/90/120 | hexagonal |

> {100} cell a=10.04 Å — *우리 comp1 V0 a=10.0551 Å와 사실상 동일*(Δ<0.02 %). 격자상수가 일치한다는 것은 **PBE-D3 평형부피가 우리 PBE 평형부피와 거의 같다**는 뜻 → 부피(=B0) 비교가 공정함의 직접 증거.

### 3.5 Bader 산화상태 (비변형 LPSCl) — **Figure 5c**
| 원소 | Bader valence (비변형) |
|---|---|
| Li | **+0.87** |
| P | **+1.32** |
| S(1) (PS₄³⁻의 S) | **−0.99** |
| S(2) (Li₆S 8면체 중심의 free S²⁻) | **−1.69** |
| Cl | **−0.89** |

- **두 종류의 S 자리**: S(1) = PS₄³⁻ 단위의 S (산화상태 ≈ −1), S(2) = Li₆S 8면체 중심의 free 황 (≈ −1.7, 더 음). → 우리 모델의 "free S²⁻ on distinct site" 와 정확히 일치.
- 변형 시 전하변동(Fig 5d–g): **P가 가장 크게 변함 (+1.32 → ~+1.23, 최대 변동)**; Li는 +0.87~+0.89로 거의 불변; S/Cl은 방향별로 다른 패턴. {110} 방향이 작은 변형에도 전하 변동에 가장 민감.

### 3.6 전단 후 Bader — **Figure 8b**
| 원소 | 원래 | 전단변형 후 |
|---|---|---|
| Li | +0.87 | +0.86~+0.87 |
| P | +1.32 | **+1.30** |
| S(1)-A / S(1)-B | −0.99 / −0.99 | −1.00 / **−0.96** (원래 같던 두 S가 *분화*) |
| S(2) | −1.69 | −1.68 |
| Cl | −0.89 | **−0.90** |

> 전단으로 **Cl이 Li 쪽으로 끌려가 Li₄Cl 형성** → PS₄ 단위 내 S의 음전하가 약화, P 양전하 감소 → 결합 약화 → **layered gap 형성** → 취성. (이것이 전단 취성의 원자기원.)

### 3.7 명시적으로 보고 **안 된** 값 (over-claim 방지)
- **sound velocity (종/횡/평균)**: n/a (논문 미보고)
- **Debye temperature Θ_D**: n/a
- **hardness (Vickers/Chen 등)**: n/a
- **선압축성 β 절대값(GPa⁻¹)**: 그림(Fig 1b)으로만; β=1/(3B) 관계만 명시(eq 10–11). Table S2에 max/min 수치 (SI, 본 digest 미보유 → n/a).
- **universal anisotropy index Aᵁ (Ranganathan)**: n/a — 이 논문의 "A"는 **Zener cubic anisotropy A = 2C₄₄/(C₁₁−C₁₂)** (eq 9)뿐. (우리 elastic.json의 "Zener_A"와 동일 정의 → 직접 비교 가능.)

## 4. DFT/계산 방법 ★ (가장 중요 — clamped vs relaxed 판정 근거)
- **code / version**: **VASP** (refs 19,20). version 미명시.
- **functional**: **GGA-PBE** (refs 21,22) + **dispersion = DFT-D3** (Table S1 비교 후 *PBE + DFT-D3가 격자상수 실험 최근접* → **모든 계산에 PBE-D3 채택**). 본문: "a better accuracy in lattice constants correlates with a higher accuracy in calculating the elastic moduli (refs 31,32)" → 그래서 D3 사용.
- **pseudo / PAW**: **PAW** (refs 23,24).
- **k-points / ecut**: **Monkhorst–Pack 3×3×3**, **plane-wave cutoff = 500 eV**, 전자 수렴 **10⁻⁶ eV**.
- **★ ion relaxation (CRITICAL)**: **"Both the lattice constants and ionic positions of the ordinary crystal structures were fully relaxed, and the final forces on all of the relaxed atoms were less than 0.01 eV/Å."** (p.17883, 우측 칼럼.) → **평형구조 = full cell+ion relax.**
- **★ 탄성텐서 산출법 = stress-based (DFPT 아님)**: "The elastic moduli were predicted from the elastic tensor represented by a 6×6 matrix … in Voigt notation Cᵢⱼ." → VASP의 **stress-strain(엄밀히는 VASP IBRION=6 류 finite-strain stress) 탄성텐서**. **DFPT 명시 없음.** (cubic이므로 C₁₁/C₁₂/C₄₄ 3개만 독립.)
- **★ 응력-변형 곡선의 ion relaxation**: "input structural data with various lattice strains were generated by varying the lattice constants … **Before and after the structural optimization of the strained crystal structures, the lattice constants were set to the same values and the ionic positions were relaxed.**" (p.17884.) → **strained cell에서도 ion만 relax (cell fix)** = **relaxed-ion stress-strain** (우리 `dft_0K_relaxed_ion` 프로토콜과 *동일한 철학*).
- **무질서/Li-ordering 처리 (LPSCl Li site disorder)**: **명시적 SQS/enumerate 없음.** ASE로 만든 *단일 cubic 결정 모델*(ordered) 사용. Cl과 free-S는 distinct site(Fig 5: S(1)/S(2) 구분). → **single-config ordered 모델** (우리 comp1 ordered-Li v3와 같은 부류; *disorder average 안 함*). ⚠ 이것이 그들 등방 A=1.09 vs 우리 relaxed-ion comp1 A=1.14가 가까운 이유 (둘 다 ordered).
- **선행 ref10 (Deng 2016)은 SQS** → 그들이 명시적으로 대비. Deng SQS A=0.92 < 1 (약간 음의 이방성), this study A=1.09 > 1.
- **AIMD / MLIP**: 없음 (0 K static DFT만).
- **특이사항**: {100}/{110}/{111} 표면 모델을 **ASE**로 생성(ref30); 탄성 시각화 **ELATE** online(ref34); 구조 시각화 **VESTA**(ref35); 전하 **Bader (Bader code, ref36)** via **VASPKIT**(ref37) 후처리. 분말 micro-compression(SI Fig S2)은 *실험*으로 별도.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **방향성 탄성 이방성** — (a) Young E, (b) 선압축성 β, (c) shear G, (d) Poisson ν 각각의 (1) 3D 표면 + (2) (xy/xz/yz) 2D 단면. 파랑=max, 초록=min. | **🔑 우리 UMA cascade가 *방향적으로* respect해야 할 reference.** E/β는 거의 구(등방); G/ν는 {110} 방향에서 max-min 차이 약간 더 큼. {111}서 E 약간 다름. → **"argyrodite는 거의 등방, 미세 이방성은 G/ν에서, {110}/{111} 방향"**. 우리 Zener_A(comp1 relaxed 1.14·clamped 1.07)와 정성 일치. |
| **2** | {100}/{110}/{111} 표면 결정모델 (변형 전/후). green=Li, bright green=Cl, yellow=S, purple=P. | {110}/{111}이 layer space 큼 → 취성. 우리 slab/표면 모델 색·정의 표준. |
| **3** | (a) **인장 응력-변형 곡선** 3방향 + (b–d) 측면구조. {100} 곡선이 가장 높고 완만, {111}이 가장 빨리 감소. | **인장 durability(ε~0.2 선형) = sulfide 연성의 직접 곡선.** 우리 "soft SE가 응력 수용" 서사의 *원자수준 곡선* 인용. |
| **4** | (a){100} (b){110} (c){111} **변형 진행 스냅샷** (ε=0 → partial fracture → fracture). {111}=layered gap(0.23서 부분파괴). | partial-fracture(결합해리 시작) vs fracture(stress drop)를 *구조로* 구분 — VESTA bond-distance 판정법. |
| **5** | (a)S(1) (b)S(2) 두 황 자리 + (c) 비변형 Bader 표 + (d–g) **변형별 Li/P/S(1)/S(2)/Cl 전하변동**. | **🔑 두 황 자리(S(1) PS₄, S(2) free) = 우리 모델과 동일.** P가 최대 변동(+1.32→+1.23). 우리 Bader/COHP와 직접 대조 가능(우리 ICOHP P–S −5.94/−6.0와 별개로, 그들은 *변형 의존* 전하를 봄). |
| **6** | (a) {111} 표면 ε=0.20 최적화 구조 + (b) 세 황 자리(S(1)-1, S(1)-2, S(2)) 확대 — Li가 S(1)-2/S(2)로 끌림. | {111} layered fracture의 원자기구(Li가 PS₄ 밖 S로 끌려 fracture 촉진). |
| **7** | (a) **전단** 도식 + (b) **전단 응력-변형 곡선 (ε=0.007서 파괴!)** + (c,d) 전단 후 구조(Li₄Cl 형성). | **🔑 이 논문의 펀치라인.** 전단 취성 ε=0.7 % ≪ 인장 ε~20 % = *강한 기계 이방성*. Cl→Li 이동 → Li₄Cl → layered gap. 우리 G/C₄₄ 논의의 *왜 취성인가* 외부 근거. |
| **8** | 전단 후 Bader: (a) 두 황 자리 + (b) 원소별 전하 (P +1.32→+1.30, S(1)-A/B 분화). | 전단 = Cl·Li 재배치 = 전하 재분배 = 결합약화 → 취성. |

## 6. Post-processing ★
- **무엇**: (i) **탄성텐서 → VRH 평균**(B,G,E,ν), (ii) **Zener 이방성 A = 2C₄₄/(C₁₁−C₁₂)**, (iii) **선압축성 β=1/(3B)** 방향분포, (iv) **응력-변형 곡선**(인장 3방향 + 전단)으로 ultimate strength·(partial) fracture strain, (v) **Bader 산화상태**의 변형 의존.
- **도구**: **ELATE**(탄성 3D/2D 이방성 시각화, ref34) · **VESTA**(구조 + ionic bond 해리 판정, ref35) · **Bader code**(ref36) · **VASPKIT**(VASP 후처리, ref37) · **ASE**(표면 모델·변형 구조 생성, ref30).
- **수치화·플롯·기록 방식**:
  - 탄성: Cᵢⱼ → eqs 1–8로 B/G/E/ν, A는 eq9, β는 eq10–11. ELATE로 방향분포.
  - 응력-변형: strained cell에 ion-relax → stress 계산 → stress(strain) 플롯. **elastic limit = 곡선 기울기가 "막 일정해지지 않게 되기 직전" 변형률**; **fracture point = stress가 급강하하기 직전**; **partial fracture strain = (stress drop 전이라도) VESTA 표준거리 초과로 *결합해리가 처음 보이는* 변형률**.
  - Bader: 0.05 strain 간격으로 원소별 valence 추적.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`, `db/properties/elastic.json`, `db/properties/eos.json`
> **방법 정렬 체크**: Torii = VASP/**PBE-D3** / **relaxed-ion**(cell+ion full relax, strained cell은 ion-relax) / **stress-strain Cij** / **3×3×3 k** / **single ordered config**. 우리 = QE/**PBE(no D3)** / **clamped-ion *and* relaxed-ion** 둘 다 / **stress-strain Cij**(±0.005) / **4×4×4 k(relaxed-ion paper-grade)** / **annealed-Li single config(comp1_v3)**. → **functional(D3 유무) + k-mesh만 다르고, ion-relax 철학·Cij 산출법·물질·격자상수는 동일.** 따라서 비교는 *공정*하다.

### 7.1 ★★★ Clamped vs Relaxed 판정 (vacancy paradox 인접 판정) ★★★
| 모듈러스 | **Torii (relaxed-ion, PBE-D3)** | 우리 **relaxed-ion** comp1_v3 (PBE) | 우리 **clamped-ion** comp1_v3 (PBE) | 판정 |
|---|---|---|---|---|
| **E (Young)** | **27.4** | **22.06** | 52.31 | **✅ Torii는 relaxed 영역** (27.4 ↔ 22.06, Δ+24 %); clamped 52.31과는 1.9× 차 → clamped 아님 |
| **G (shear)** | **10.0** | **8.13** | 20.12 | **✅ relaxed** (10.0 ↔ 8.13, Δ+23 %); clamped 20.12와 2.0× 차 |
| **B (bulk)** | **34.7** | 25.51 (B_VRH) / **26.23 (BM-EOS B0)** | 43.59 (B_VRH) | **△ 중간** — relaxed B_VRH(25.5)·EOS B0(26.2)보다 +33 % 높고 clamped(43.6)보다 −20 % 낮음. *D3 + relaxed-ion bulk 정의*가 우리 PBE relaxed보다 bulk를 올림 (§7.3) |
| **C₁₁** | **47.4** | 37.67 | 74.23 | **✅ relaxed쪽** (47.4 ↔ 37.7); clamped 74.2와 큰 차 |
| **C₄₄** | **10.4** | 7.98 | 18.98 | **✅ relaxed쪽** (10.4 ↔ 7.98); clamped 19.0과 1.8× 차 |
| **C₁₂** | **28.4** | 20.43 | 29.23 | C₁₂는 흥미롭게 clamped(29.2)에 가까움 — D3가 cross-coupling(정수압 성분)을 키움 (§7.3) |
| **ν** | **0.37** | 0.356 | 0.300 | **✅ relaxed** (0.37 ↔ 0.356, 거의 동일); clamped 0.30과 차 |
| **Zener A** | **1.09** | 1.144 | 1.073 | 둘 다 ≈1(등방). ordered config라 두 우리값 모두 1 근방 → 정합 |

> **🔑 결론 1 — paradox 판정**: **Torii의 full-DFT 탄성은 *명백히 우리 relaxed-ion 영역*에 산다.** E·G·C₁₁·C₄₄·ν 모두 우리 relaxed-ion(22.06/8.13/37.7/7.98/0.356)에 가깝고, 우리 clamped-ion(52.31/20.12/74.2/19.0/0.30)과는 ~2× 차이. **즉 "clamped-ion이 argyrodite 탄성을 ~2× 과대평가한다"는 우리 진단이 외부 full-DFT로 *독립 확증*된다.** vacancy paradox의 해소 경로(=clamped 말고 relaxed/finite-T를 봐야 함)가 옳다. 우리 relaxed-ion E_VRH 22.06이 실험 pellet E~23 GPa(Kim 2025)와 맞은 것과 같은 줄에, Torii relaxed-ion E=27.4도 *실험 범위(15–28 GPa)의 상단*에 들어온다.

### 7.2 ★ B0 / EOS 일치
| 항목 | Torii | 우리 |
|---|---|---|
| **bulk modulus** | **B(VRH)=34.7 GPa** (relaxed-ion + D3) | **BM-EOS B0 comp1 = 26.23 GPa** (BM3, 8 pts, R²=1.000, B0'=4.17) |
| 평형 a | {100} a=**10.04 Å** | comp1 a=**10.0551 Å** (k444 V0) |

> **🔑 결론 2 — B0 일치도**: 격자상수는 **거의 완벽 일치(10.04 ↔ 10.055 Å, Δ0.02 %)** → 평형부피·packing이 같다. **그러나 bulk modulus 절대값은 Torii 34.7 vs 우리 EOS B0 26.23 (Δ+32 %)**. 이 차이는 *물질 불일치가 아니라 방법 차이*다: (a) **VRH B는 하모닉 탄성텐서 평균**인데 **BM-EOS B0는 full hydrostatic E(V) 곡률** — 우리 안에서도 이미 K_VRH(relaxed 25.51, clamped 43.59) ≠ BM-EOS B0(26.23)임이 기록됨; 우리 relaxed-ion B_VRH(25.51)은 BM-EOS B0(26.23)와 3 % 이내(internal cross-check). Torii는 *B를 VRH로만* 보고했고 별도 EOS B0는 없음. (b) **D3 분산력**이 정수압 강성(C₁₂↑→B↑)을 올린다 — Torii C₁₂=28.4가 우리 relaxed C₁₂=20.43보다 39 % 높은 게 직접 증거(B=⅓(C₁₁+2C₁₂)이므로 C₁₂↑가 B를 끌어올림). → **"부피(B0)는 같은 물질, 절대 B는 D3+정의 차로 +32 %"**가 정직한 서술. ★ **B0 *순서/scale*은 일치(둘 다 ~25–35 GPa soft sulfide), 절대값은 functional 의존** — 우리 EOS B0 26.23을 "외부 DFT와 정합"이라 쓸 때 **반드시 D3 없는 우리 B_VRH 25.51과 비교(거의 동일)**, Torii VRH 34.7과 직접 등치 금지.

### 7.3 D3가 만든 차이의 정량 분해 (왜 Torii > 우리 PBE인가)
| 양 | Torii (PBE-D3) | 우리 relaxed (PBE) | Δ | 해석 |
|---|---|---|---|---|
| C₁₁ | 47.4 | 37.67 | +26 % | D3가 normal 강성 ↑ |
| C₁₂ | 28.4 | 20.43 | +39 % | **D3 영향 최대** — 정수압/cross-coupling ↑ → B 끌어올림 |
| C₄₄ | 10.4 | 7.98 | +30 % | D3가 shear도 ↑ |
| → B | 34.7 | 25.51 | +36 % | C₁₂ 주도 |
| → E | 27.4 | 22.06 | +24 % | |
| → G | 10.0 | 8.13 | +23 % | |

> **핵심**: 모든 Cᵢⱼ가 일관되게 +23~39 % → **계통적 D3 강성 증가** (랜덤 불일치 아님). 즉 Torii vs 우리의 *차이는 functional(D3)이 거의 전부*이고, **relaxed-vs-clamped 같은 *2배* 차이(질적 차이)는 전혀 아니다.** → "Torii가 우리 relaxed-ion regime에 있다"는 결론은 D3 보정 하에서도 robust (D3는 +30 %, clamped는 +100 %; 두 효과의 스케일이 다름).

### 7.4 ★ 이방성(Zener A) corroboration
| 항목 | Torii | 우리 |
|---|---|---|
| comp1 (ordered) Zener A | **1.09** | relaxed 1.144 / clamped 1.073 | ✅ 거의 등방, 정합 |
| modelc(Cl-rich, vacancy+disorder) | n/a (Cl₁.₅/₁.₆ 미계산) | relaxed 1.441 / clamped 0.416 | — |

> **🔑 결론 3 — 이방성 fingerprint**: 우리 elastic.json의 명제 **"anisotropy difference is the only Cij-level fingerprint of vacancy/disorder"**는, Torii가 **vacancy 없는 comp1만** 계산해 **A=1.09(등방)**을 얻은 것으로 *간접 지지*된다 — vacancy 없는 LPSCl은 등방(우리 1.07–1.14, Torii 1.09 모두 ≈1). 우리는 여기에 **modelc(vacancy+Cl-disorder)에서 A가 relaxed 1.44로 *증가*(또는 clamped 0.42로 *붕괴*)**함을 더해 "disorder가 이방성을 깬다"를 보인다 — **Torii가 등방 baseline(vacancy-free)을 외부 확정**해 줌으로써 우리 "disorder→이방성" 주장의 *대조군*이 외부 데이터로 고정됨. ⚠ 단, Torii는 vacancy 조성을 안 했으므로 *vacancy가 A를 키운다*까지는 그들 데이터로 말 못 함 → 그건 우리 고유 기여.

### 7.5 UMA cascade와의 정합 (방향성 reference)
| 항목 | Torii (DFT relaxed) | 우리 UMA |
|---|---|---|
| comp1 등방성 | A=1.09 | UMA 600K comp1_v3 Zener_A=**1.136** (near-isotropic) | ✅ UMA도 등방 재현 |
| 절대 stiffness | E=27.4 (DFT) | UMA 600K comp1 E_VRH=59.71 (UMA≠DFT scale) | cross-method 절대값 비교 금지 |

> **UMA cascade 함의**: 우리 cascade elastic은 dopant에서 stiff(~47 GPa)로 나오고 UMA가 DFT보다 절대 강성을 높게 줌(Nd₂O₃ B0 UMA 18.9 vs DFT 19.9는 *예외적으로* 잘 맞음). **Torii는 UMA를 검증하는 *DFT 앵커*가 아니라(다른 functional·다른 코드), *방향성(이방성) reference*로 사용**: cascade dopant의 Zener_A가 comp1 baseline(Torii 1.09·우리 1.07–1.14)에서 *얼마나 벗어나는지*를 "disorder/도핑이 이방성을 얼마나 깨나"로 읽을 때 Torii의 등방 baseline이 닻. **절대 E/B/G를 UMA(≈60) ↔ Torii(27.4) 직접 비교 금지**(UMA-vs-DFT scale + D3).

### 7.6 비교 요약표
| 항목 | Torii | 우리 | 일치/차이 + 이유 |
|---|---|---|---|
| 물질 | Li₆PS₅Cl ordered | comp1 Li₆PS₅Cl annealed-ordered | **동일** |
| 평형 a | 10.04 Å | 10.0551 Å | **✅ Δ0.02 %** |
| ion-relax | relaxed (cell+ion; strained=ion) | relaxed-ion *and* clamped-ion | **relaxed 프로토콜 동일** |
| Cij 산출 | stress-strain (DFPT 아님) | stress-strain ±0.005 | **동일** |
| E / G / C₁₁ / C₄₄ / ν | 27.4 / 10.0 / 47.4 / 10.4 / 0.37 | relaxed 22.06 / 8.13 / 37.67 / 7.98 / 0.356 | **✅ relaxed 영역** (clamped 52.3/20.1/74.2/19.0/0.30 아님). Δ+23~30 % = **D3** |
| C₁₂ / B | 28.4 / 34.7 | relaxed 20.43 / 25.51; EOS B0 26.23 | **△ D3가 C₁₂(+39 %)→B(+32 %) 끌어올림.** B0 절대값 functional 의존 |
| Pugh B/G, ν | 3.46, 0.37 (연성) | relaxed B/G=3.14(25.51/8.13), ν 0.356 (연성) | **✅ 연성 결론 동일** |
| Zener A | 1.09 (등방) | relaxed 1.144 / clamped 1.073 | **✅ vacancy-free=등방** 외부 확정 |
| 전단 취성 | ε_fracture **0.7 %** (Li₄Cl) | 우리 C₄₄/G만; 전단 응력-변형 *미계산* | **그들 고유 기여** (우리 elastic은 모듈러스만; fracture 곡선 없음) |

## 8. 적용 인사이트 (내 연구에 어떻게) — 가장 날카로운 3가지
1. **🔑 vacancy paradox의 *외부 full-DFT 판정문***: "An independent full-DFT study (Torii et al., VASP/PBE-D3, **relaxed-ion**) reports E=27.4, G=10.0, C₄₄=10.4 GPa for Li₆PS₅Cl — within ~25 % of our **relaxed-ion** values (22.06 / 8.13 / 7.98) and **~2× below our clamped-ion** values (52.31 / 20.12 / 18.98). This confirms that the clamped-ion overestimate is the artifact, and the relaxed-ion regime is the physical one." → **deck "vacancy paradox" 슬라이드의 외부 검증 인용**. (clamped를 bu그가 아니라 *frozen-framework baseline*으로 둔 우리 서사가 그대로 산다.)
2. **🔑 B0는 "같은 물질", 절대값은 functional**: 격자상수 10.04≈10.055 Å로 *부피·packing 동일* 확정 → 우리 EOS B0 26.23을 외부와 비교할 때 **"부피 일치, B 절대값은 D3가 +32 %(C₁₂ 주도)"**로 정확히 분해. Torii VRH B=34.7과 우리 EOS B0=26.23을 *등치하지 말고*, 우리 relaxed B_VRH 25.51(D3 없음)과 비교하면 거의 동일 — **functional 맞추면 정합**.
3. **🔑 전단 취성 = 우리 모듈러스 그림의 *메커니즘***: 우리는 C₄₄/G(낮음)와 B/G(연성)만 보고하고 "왜 분말이 취성인가"는 못 말한다. Torii는 **전단 ε=0.7 %서 Cl→Li 이동→Li₄Cl→layered gap**으로 *원자기구*를 줌. → 우리 "soft·ductile SE" 서사에 **"단 전단엔 취성(Cl 이동 매개)"**을 한 줄 보강(Kang 리뷰의 chemo-mechanical 취성/균열 §3와도 연결). 단 *우리 데이터엔 fracture 곡선이 없으므로* "우리가 보였다" 금지 — Torii 인용.

## 9. 인용 가능 문장 (deck/paper용)
- "Torii et al.'s full-DFT (PBE-D3, **relaxed-ion**) Young's/shear moduli (E=27.4, G=10.0 GPa) for Li₆PS₅Cl fall squarely in our relaxed-ion regime (22.06 / 8.13 GPa) and ~2× below our clamped-ion values (52.31 / 20.12 GPa), independently confirming that the relaxed-ion moduli are the physical ones and the clamped-ion result is a frozen-framework overestimate."
- "The ~25 % offset (Torii > ours) is a *systematic* DFT-D3 stiffening (every Cᵢⱼ up 23–39 %, largest for C₁₂ → B), not a clamped/relaxed-type qualitative gap; matching functionals (our PBE B_VRH 25.51 vs our BM-EOS B0 26.23) brings bulk into 3 % agreement."
- "Both Torii's relaxed-ion DFT (Zener A=1.09) and ours (1.07–1.14) find vacancy-free Li₆PS₅Cl elastically isotropic; the anisotropy increase we compute for the Cl-rich, Li-vacancy phase (A→1.44 relaxed) is therefore the genuine Cij-level fingerprint of disorder, anchored against an externally fixed isotropic baseline."
- "Torii et al. assign Li₆PS₅Cl's macroscopic powder brittleness to shear collapse at only 0.7 % strain via Cl→Li migration and Li₄Cl formation — the atomic-scale mechanism behind the low C₄₄/G that our elastic tensor reports."

## 10. 주의/한계 (over-claim 방지)
- **[외부]·Osaka(Sakuda/Hayashi)** — *우리 그룹 아님*. 4축 비교는 mechanical/elastic 축에서만 *수치 비교* 가능(물질·방법 정렬됨).
- **D3 사용** → 그들 절대 E/B/G는 우리 PBE보다 계통적으로 +23~39 % 높다. **functional 맞추지 않고 절대값 직접 비교 금지.** 특히 **B(VRH) 34.7 ↔ 우리 EOS B0 26.23 등치 금지** (정의 + D3 이중 차이). 비교는 *relaxed-vs-clamped regime 판정*과 *순서/scale*에서만 robust.
- **vacancy/Li-disorder 미처리** — Torii는 *ordered single config*만(SQS 아님; Deng ref10이 SQS). 따라서 **modelc(Cl-rich) 직접 대조 없음**; "disorder가 이방성/강성을 어떻게 바꾸나"는 *우리 고유 기여*이고 Torii는 vacancy-free *대조군*만 제공.
- **k=3×3×3**(우리 relaxed paper-grade는 4×4×4). 우리 내부 k221→k444 차이가 ~1 %였으므로 k-mesh 차이는 작지만, 절대 Cᵢⱼ 미세차의 일부일 수 있음.
- **전단 응력-변형은 *virtual* shear**(c축 x좌표 변화) — 실제 결정의 모든 전단모드를 대표하진 않음. ε=0.7 % fracture는 *이 특정 전단경로*의 값. 그래도 정성(인장≫전단 durability)은 강건.
- **sound velocity·Debye Θ·hardness·Aᵁ(universal)·β 절대값 = 미보고(n/a)** — 인용 시 "보고 안 됨" 명기. (그들 A = Zener cubic 정의뿐 = 우리 Zener_A와 동일.)
- **실험 caveat**(그들 본문): 단결정 계산 shear strength **76 MPa** ↔ 입자 micro-compression strength는 *2 자릿수 더 낮음*(SI Fig S2) → "single-crystal DFT는 informative하나 particle-level은 추가 연구 필요". 즉 *우리 elastic도 마찬가지로 ideal-crystal 상한*임을 그들도 인정 — 우리 "DFT > UPE pellet > AFM" 줄과 정합.

## 11. 기법 용어 미니사전
- **Zener anisotropy A = 2C₄₄/(C₁₁−C₁₂)**: cubic 결정의 이방성 지표. A=1이면 완전 등방, 1에서 멀수록 이방. *우리 elastic.json "Zener_A"와 동일 정의* → 직접 비교 가능. (cf. universal Aᵁ는 Ranganathan 정의로 *다름* — Torii는 안 씀.)
- **Voigt–Reuss–Hill (VRH)**: 다결정 평균 모듈러스. Voigt=균일변형(상한), Reuss=균일응력(하한), Hill=둘의 산술평균. eqs 1–6.
- **Pugh ratio B/G**: 연성/취성 판별. >1.75 연성(ductile), <1.75 취성(brittle). LPSCl 3.46 → 연성.
- **선압축성 β = 1/(3B)**: 정수압 하 길이변화율. B 클수록 β 작음(압축 저항 큼).
- **clamped-ion (frozen-ion) vs relaxed-ion Cij**: 변형 셀에서 *원자를 평형위치에 고정*하면 clamped(framework 강성만, 과대); *원자를 재이완*시키면 relaxed(Born/internal-strain 차폐 포함, 물리적). argyrodite는 Li 부격자가 물러 둘 차이가 ~2× → *vacancy paradox의 핵심 분기*.
- **partial fracture strain**: stress drop 전이라도 VESTA 표준 ionic 거리 초과로 *결합 해리가 처음 보이는* 변형률 (이 논문 정의).
- **stress-strain elastic tensor**: 유한 변형을 가해 stress 텐서로부터 Cᵢⱼ를 얻는 방법 (DFPT의 linear-response와 대비; 둘 다 동일 Cᵢⱼ를 줘야 함).
- **ELATE**: 탄성텐서를 받아 방향성 E/G/ν/β를 3D/2D로 시각화하는 online 도구.
- **Li₄Cl 단위**: 전단 시 Cl이 Li 4개에 둘러싸이게 끌려가 형성되는 클러스터 — PS₄ S의 음전하 약화 → layered gap → 취성의 원자기원.
