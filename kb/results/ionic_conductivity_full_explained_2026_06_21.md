# 이온전도도 완전 정리 — LPSCl(comp1) vs LPSCl₁.₆(modelc)

> **목적**: comp1(LPSCl)보다 modelc(LPSCl₁.₆)가 왜 Li⁺ 전도가 ~4배 빠른지를
> **구조 → 정적 분석(ELF·BVS/BVSE) → 동적 분석(AIMD·Li-density)**으로 빈틈없이.
> 4가지 분석이 서로 안 겹치게 각자 다른 조각을 맡는 구조. 보고/논문용 레퍼런스.
> 날짜 2026-06-21. 수치 출처: `db/properties/li_transport.json`, `elastic.json`,
> `db/compositions/{comp1,modelc}.json`, BVSE paired 5×5×5 슬라이드.

---

## 0. 한 줄 요약 (TL;DR)

- **modelc(LPSCl₁.₆)는 comp1(LPSCl)보다 σ_Li ~4배** (3.35 → 13.96 mS/cm, AIMD-MLIP). 실험 x=0.6 = 11.34 mS/cm와 일치.
- 원인 = Cl-rich 치환(Li₆PS₅Cl → Li₅.₄PS₄.₄Cl₁.₆)의 **이중 메커니즘**:
  1. **anti-site Cl disorder → 이동장벽 Ea↓** (0.253 → 0.224 eV, ×1.75 @600K)
  2. **Li vacancy → 운반자 농도↑** (D₀, ×1.41)
- **4가지 분석의 역할 (안 겹침)**:
  | 분석 | 무엇을 | 결론 |
  |---|---|---|
  | **ELF** | 결합 *성격* | Li–Cl·Li–S 이온, PS₄ 공유 — **조성 무관하게 유지(대조)** |
  | **BVS/BVSE** | *정적* Li 에너지 landscape | anti-site Cl → Li 환경 **bimodal**(60%가 +15% 불안정) |
  | **AIMD** | *정량* Ea·D·σ | **Ea↓ + D₀↑** (이중 메커니즘 증거) |
  | **Li-density cube** | Li *동적* 분포 | Li이 inter-cage(Cl) 영역까지 **비편재화** (Li-on-Cl 0→55.6%) |

---

## 1. 두 시스템

| | **comp1 = LPSCl** | **modelc = LPSCl₁.₆** |
|---|---|---|
| 화학식 | Li₆PS₅Cl | Li₅.₄PS₄.₄Cl₁.₆ |
| 셀 | cubic F-43m, 4 f.u. | rhombohedral, 5 f.u. |
| 총 원자 | 52 | 62 |
| Li | 24 | 27 |
| P | 4 | 5 |
| S (PS₄ / 자유 S²⁻) | 20 (16 / **4**) | 22 (20 / **2**) |
| Cl | **4** | **8** |
| Li vacancy | 0 | **3** (Li 27 vs full 30) |
| cage 중심(자유 S²⁻) | 4 | 2 |

**핵심 차이**: Cl-rich 치환은 (1) 자유 S²⁻ 자리(4a/4d)를 **Cl로 치환**(anti-site, Cl 4→8) + (2) 전하보상으로 **Li 제거**(vacancy 0→3). 이 두 변화가 그대로 이중 메커니즘이 됨.

---

## 2. 결과 — σ_Li ~4배 (AIMD-MLIP)

**방법**: UMA-s-1p1 (task=omat) MLIP, Langevin NVT **600/800/1000 K**,
MSD → D(Einstein) → Arrhenius(Ea) → Nernst–Einstein(σ).

| | Ea (eV) | D(600K) (cm²/s) | σ(300K) (mS/cm) |
|---|---|---|---|
| **comp1 (LPSCl, 4 f.u.)** | **0.2532** | 3.09×10⁻⁶ | **3.35** |
| **modelc (LPSCl₁.₆, 5 f.u.)** | **0.2235** | 7.90×10⁻⁶ | **13.96** |
| 비 (modelc/comp1) | −0.030 eV | ×2.6 | **×4.2** |

> ⚠️ **comp1은 반드시 4 f.u.(natural cell)**: 5 f.u. cubic 슈퍼셀은 Ea 0.172의 **artifact**를 줌. 두 시스템 비교 시 each 고유 셀로.

---

## 3. 왜 빨라지나 — 이중 메커니즘

전도도 분해:
$$\sigma \;\propto\; \underbrace{n}_{\text{운반자 수}} \times \underbrace{D_0}_{\text{prefactor}} \times \exp\!\left(-\frac{E_a}{k_BT}\right)$$

Cl-rich가 만든 두 변화가 각각 다른 항을 건드림:

### 3a. anti-site Cl disorder → **Ea↓** (×1.75 @600K)
- anti-site Cl(원래 S²⁻ 자리에 Cl)이 주변 Li 자리를 **불안정하게(에너지↑)** 만듦 → Li 자리(well)가 **얕아짐** → 넘을 장벽이 낮아짐 ("landscape 평탄화 / 바닥 들어올리기").
- 그 영향 영역이 **inter-cage 길목(Cl 근처)** → **inter-cage 장벽 = Ea**가 낮아짐.
- 정량: exp[(0.2532−0.2235)/k_B·600K] ≈ **×1.75**.

### 3b. Li vacancy → **운반자↑ (D₀↑)** (×1.41)
- Cl-rich는 전하보상으로 Li을 빼서 **빈자리(vacancy) 3개** 생성 → Li이 점프해 들어갈 **빈 칸**↑ → carrier/prefactor↑.
- 정량: D₀(modelc)/D₀(comp1) ≈ **×1.41**.

### 합 — 온도가 열쇠
**Ea 효과 `exp(ΔEa/k_BT)`는 온도 의존**(저온일수록 큼), D₀/carrier는 T-무관. 그래서 같은 이중 메커니즘이 **온도마다 다른 배수**를 줌:

| 양 | Ea 효과 | × D₀/carrier | = 곱 | 실측 |
|---|---|---|---|---|
| **D @600K** | ×1.78 | ×1.41 | ×2.5 | D₆₀₀ 비 ×2.6 ✓ |
| **σ @300K** | **×3.2** | ×1.41 | **×4.5** | σ 비 **×4.2** ✓ |

→ σ(300K)가 D(600K)보다 더 벌어지는 이유 = **Ea 효과가 저온에서 커지기** 때문. 즉 이중 메커니즘이 σ ×4를 **온전히 설명**(미설명 잔차 없음); 두 효과 거의 동등 기여.
(ΔEa = 0.2532 − 0.2235 = **0.0297 eV**, k_BT₃₀₀ = 0.0259 eV → exp(0.0297/0.0259) = **3.2**)

---

## 4. intra-cage / inter-cage (방 비유 🏠)

argyrodite Li 전도의 기본 그림:
- **cage = 방 하나.** 방 한가운데 **자유 S²⁻**, 둘레를 **Li이 돎.**
- **PS₄ = 벽/기둥** (공유결합 강체, **안 움직임**, 통로 모양만 정함).
- **Cl = 방과 방 사이 문**(gateway).

| | 위치 | 점프 | 장벽 | 전도 기여 |
|---|---|---|---|---|
| **intra-cage** | 방 *안* (자유 S²⁻ 둘레) | doublet/intra | **낮음** | 빠르지만 *국소* (제자리) |
| **inter-cage** | 방 *사이* 문 (Cl 근처) | inter | **높음 = Ea** | **율속(병목)** = 장거리 전도 결정 |

- **측정 Ea = inter-cage 장벽** (멀리 가려면 반드시 문 통과). intra-cage가 아무리 빨라도 방 안에만 있으면 σ=0.
- **NMR 두 Ea** 근거: 국소(short-range) ~0.1–0.2 eV(intra) / 장거리(σ) ~0.3–0.4 eV(inter).
- **modelc**: anti-site Cl + vacancy가 이 **문(inter-cage)을 넓혀** Li이 방을 더 쉽게 건넘 → σ↑.

(주의: cage 중심은 *자유* S²⁻. PS₄의 S는 *벽*. modelc는 자유 S²⁻이 2개뿐이고 그 자리들이 대부분 Cl로 치환됨 = anti-site.)

---

## 5. 네 가지 분석이 각각 보여주는 것

### 5a. ELF (Electron Localization Function) — 결합 성격 [대조]
- **Li–Cl, Li–S(자유), Li–S(PS₄) 전부 이온결합**: 음이온 둘레 구형 껍질 + Li과의 사이 저-ELF "도랑(moat)". bond-min ELF **0.05–0.07**.
- **P–S 공유결합**: 두 원자 사이 ELF 다리(attractor), midpoint 0.94, bond-min 0.29.
- **comp1 = modelc 동일** → **Cl을 늘려도 결합 성격은 안 바뀜.**
- **역할 = 대조(control)**: σ↑가 "결합(공유성) 변화" 때문이 아님을 **배제**. 변화는 *구조 disorder·vacancy*이지 *결합 종류*가 아님.

### 5b. BVS/BVSE — 정적 Li 에너지 landscape [원인]
- **결과**: comp1은 Li 환경 단일(BVS 1.60–1.64), modelc는 **bimodal** — 39.8%는 그대로 + **60.2%가 anti-site Cl 인접에서 +15%(BVS 1.83–1.89)**로 불안정해짐.
- 이 bimodal = **anti-site Cl이 Li landscape를 재편**한 정적 fingerprint (= 3a의 원인).
- (상세 공식·해석은 §6.)

### 5c. AIMD — 정량 Ea·D·σ [증거]
- **Ea 0.253→0.224**, σ 3.35→13.96. 이중 메커니즘(Ea↓ + D₀↑)을 **직접 정량**.
- BVS가 못 보는 **vacancy·동역학**까지 포함 → σ의 최종 답.

### 5d. Li-density cube (AIMD 점유) — Li 동적 분포 [시각]
- **cage descriptor**: Li-on-Cl(=Cl 근처 Li 점유) comp1 **0%** → modelc **55.6%**, cage-Cl 0.50→0.80.
- = modelc Li이 **inter-cage(Cl) 영역까지 비편재화** → 문이 열림 (3a와 일관).
- isosurface = Li 점유 밀도 등고면; 레벨 낮추면 inter-cage 다리가 연결돼 보임.

---

## 6. BVS / BVSE 정확히 (개념·공식·해석·확장·한계)

### 6.1 Bond Valence (한 결합의 "값")
Pauling: 결합마다 **valence(결합값)**가 있고, 한 원자의 모든 결합값 합 = 그 원자의 산화수.
한 결합(양이온 i–음이온 j, 거리 $d_{ij}$):
$$s_{ij} = \exp\!\left(\frac{R_0 - d_{ij}}{b}\right)$$
- $R_0$ = 그 양이온–음이온 쌍의 **기준 거리**(tabulated; $s=1$이 되는 길이). Li–S, Li–Cl마다 다름.
- $b$ ≈ **0.37 Å** (Brown–Altermatt 보편값; Adams *softBV*는 쌍별 미세조정).
- **짧을수록 $s$ 지수적으로 커짐** (가까이 = 강하게 결합).

### 6.2 Bond Valence Sum (BVS)
$$V_i = \sum_j s_{ij} = \sum_j \exp\!\left(\frac{R_0 - d_{ij}}{b}\right)$$
**valence sum rule**: $V_i$ = 형식 산화수. **Li⁺ → 이상값 $V=1$.**
실제 BVS가 1에서 벗어난 정도 = 그 자리(환경)의 **strain**.

### 6.3 벗어남(deviation)의 뜻
| BVS | 뜻 |
|---|---|
| $V=1$ | 이상적 — Li 딱 맞게 결합 |
| $V>1$ (**over-bonded**) | 자리가 너무 좁음/Li이 음이온에 너무 가까움 → 눌림 → **불안정(에너지↑)** |
| $V<1$ (**under-bonded**) | 자리가 너무 큼/Li 헐렁 → 역시 불안정 |

- 우리 결과: LPSCl Li은 BVS **1.6**(이미 over-bonded), anti-site 인접 60%가 **1.85**(더 over-bonded = 더 불안정 = **더 얕은 well**).
- 절대값 1.6은 $R_0$ 파라미터·argyrodite 특성 때문; **의미 있는 건 1.6→1.85 상대 이동.**
- **왜 이게 Ea↓로 이어지나**: $E_a = E(\text{고개}) - E(\text{Li 자리})$. anti-site가 Li 자리(바닥)를 +15% **끌어올림** → 넘을 높이 줄어듦 → **장벽↓** ("바닥 들어올리기").

### 6.4 BVS → BVSE (Bond Valence **Site Energy**)
BVS는 "값"일 뿐 — 이걸 에너지 지형으로 바꾼 게 BVSE (Adams, *softBV*):
$$E_{\text{BVSE}}(\mathbf r) = \underbrace{E_{\text{Morse}}(\text{Li–anion})}_{\text{음이온 인력(BV로 매개)}} + \underbrace{E_{\text{Coulomb}}(\text{Li–cation})}_{\text{양이온 반발}}$$
- 가상 Li⁺를 격자점마다 놓고 $E_{\text{BVSE}}(\mathbf r)$ 계산 → **3D 에너지 지도**.
- **낮은 BVSE = Li 자리·통로(channel)**, **안장점 = 이동 장벽 ≈ Ea**.
- 슬라이드 "**BVSE ≤ 0.30**"은 **site energy(eV) 임계값** → 그 이하 = "Li 접근 가능 채널".
- ⚠️ 두 양 구분: **BVS = 무차원 합(~1.6)**, **BVSE = eV 에너지(채널 임계 0.30)**.

### 6.5 우리 사용법 (paired 5×5×5)
- "**identical cubic lattice (50.275 Å), grid 100³, cutoff 5 Å — only chemistry differs**": 똑같은 격자에 LPSCl vs LPSCl₁.₆ **화학만 바꿔**(300 S→Cl, −300 Li) BVS 지도 비교 = **anti-site Cl 효과만 분리**.
- 결과 (5 f.u.×... = paired supercell, LPSCl 6500 atoms / LPSCl₁.₆ 6200):

  | 구분 | n_Li | 비율 | BVS peak | 환경 |
  |---|---|---|---|---|
  | LPSCl (단일) | 3000 | 100% | 1.60–1.64 | F-43m ordered |
  | LPSCl₁.₆ low (A) | 1074 | 39.8% | 1.60–1.64 | LPSCl-like (anti-site 멈) |
  | LPSCl₁.₆ high (B) | 1626 | **60.2%** | **1.83–1.89** | **anti-site Cl 인접 (+15%)** |

- **60.2% = 5.4×300/2700 정확 closure** (조성에서 예측되는 anti-site 영향 Li 비율과 일치).
- **BVS +15% ↔ ICOHP +40% per-bond**: 같은 anti-site를 **독립된 두 probe**(bond-valence·COHP)가 같은 방향으로 확인.
- **저-BVSE 채널**: LPSCl **8.75%** → LPSCl₁.₆ **7.4% (−15%)**.

### 6.6 ⚠️ "채널 −15%인데 σ는 ×4" 역설 해소
- 정적 BVSE "채널 %"는 **깊은 well만** 셈 → 60% Li을 끌어올리면(bimodal) 채널이 **−15%로 작아 *보임***.
- 그러나 그 끌어올려진 Li이 바로 **얕은 well = 잘 hopping = Ea 낮은** 애들 → **채널 −15%와 Ea↓는 같은 anti-site 효과의 두 얼굴** (정적 지표가 부호를 거꾸로 줄 뿐).
- 게다가 정적 BVSE는 **vacancy(carrier)를 못 봄** → σ↑의 절반(D₀)을 놓침.
- → **정량 Ea↓·σ↑는 AIMD가 마무리.** (BVS=원인, AIMD=증거, cube=정황.)

### 6.7 BVS/BVSE의 한계 (정확히)
- **경험식**(양자역학 아님) → 장벽은 **근사/정성적**; DFT·AIMD로 검증 필요.
- **정적**: vacancy·동역학·전자구조 못 봄 → σ×4의 vacancy 기여를 놓침.
- 좋은 용도: **빠른 경로 스크리닝, 채널 시각화, 같은 구조 화학 비교**(우리 paired처럼).

---

## 7. 문헌 검증

| 우리 값 | 문헌 | 평가 |
|---|---|---|
| modelc σ ~14 mS/cm | 실험 x=0.6 = **11.34** (J. Power Sources 2023, 583, 233579) | ★우수 일치 |
| comp1 σ 3.35 | 실험 LPSCl 2.5–4.7 | 범위 내 |
| comp1 Ea 0.253 / modelc 0.224 | 실험 LPSCl 0.33–0.38, Li₅.₅Cl₁.₅ 0.29 | MLIP끼리 일치, 실험보다 낮음(MLIP 경향) |
| anti-site → σ↑ | 37.5–50% disorder가 σ 최대 (Lee/Han *Chem.Mater.* 2025) | 정성 일치 |
| AIMD-MLIP 사용 정당성 | "Liquid-like dynamics" — VDOS non-Debye, quasi-harmonic 붕괴 (*Nat. Phys.* 2025, 10.1038/s41567-024-02707-6) | 우리 접근 benchmark |

---

## 8. 보고용 핵심 문장 + figure 체크리스트

**한 단락 (그대로 사용 가능)**:
> ELF로 Li–Cl·Li–S 이온결합과 PS₄ 공유결합이 조성 무관하게 유지됨을 확인(대조). BVS/BVSE로 anti-site Cl이 Li 환경을 bimodal(60.2%가 +15%)로 쪼개 inter-cage landscape를 평탄화함을 확인(원인). AIMD로 inter-cage 활성화에너지 감소(0.253→0.224 eV)와 Li-vacancy 운반자 증가를 정량 확인하고, Li-density cube로 Li이 inter-cage(Cl) 영역까지 비편재화(Li-on-Cl 0→55.6%)됨을 시각 확인. → **anti-site(Ea↓ ×1.75) + vacancy(carrier↑ ×1.41)의 이중 메커니즘으로 σ ~4배.**

**figure 체크리스트**:
- [ ] ELF: P–S 공유(다리) vs Li–Cl/Li–S 이온(껍질+도랑), comp1=modelc.
- [ ] BVS: bimodal 히스토그램 (LPSCl 단일 vs LPSCl₁.₆ 40/60) + 채널 −15% 주석.
- [ ] AIMD: MSD 3패널(600/800/1000K) + Arrhenius(Ea) + σ 표.
- [ ] Li-density cube: comp1(고립 cage) vs modelc(연결망), 정규화 isolevel, 자유S(cage)·Cl(inter) 라벨.

---

## 9. 한계·주의 (정직하게)
- σ 절대값은 MLIP(UMA) — 실험과 ~배수 차 가능; **trend(modelc>comp1)·Ea가 robust**.
- comp1 5 f.u.는 artifact (Ea 0.172) → **4 f.u. natural cell 사용**.
- 이중 메커니즘 분해(×1.75·×1.41)는 600K Ea + D₀ 기반 추정; 실측 σ비 ×4와 정성 일치.
- BVS/BVSE는 정적·경험식 → 원인 제시용, 정량은 AIMD.
- Li-density cube 비교는 **정규화 isolevel** 필수(셀·Li수 다름).

---

### 부록 — 관련 파일
- 수치: `db/properties/li_transport.json`
- ELF 그림/도구: `docs/figures/elf_licl/`, `tools/figures/plot_elf_*.py`
- MSD CSV: `docs/figures/msd_compare/msd_compare_comp1_modelc.csv`
- BVSE paired: `db/compositions/comp1.json` (`bvse_5x5x5_paired_2026_06_03`)
- cage descriptor: `tools/ionic/cage_jump_descriptors.py`, `kb/results/ionic_cage_descriptors_comp1_modelc.md`
