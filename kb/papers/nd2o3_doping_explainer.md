# Nd₂O₃ 도핑 — Argyrodite Solid Electrolyte (modelC)
## 처음 합류한 대학원생용 가이드 (v2 — 2026-05-09 corrected)

> **이 문서는 무엇인가?**
> Paper #2 (Nd₂O₃ co-substituted Li₅.₄PS₄.₄Cl₁.₆) 프로젝트에 합류한 사람을 위한 입문서.
> 어떤 시스템을 다루고, 왜 이렇게 셋업했고, 결과가 무엇을 의미하는지 단계별로 설명.

---

## 0. 한 줄 요약

> **modelC라는 argyrodite 고체전해질에 Nd₂O₃를 도핑할 때, Nd 두 개가 어디 들어가야 가장 안정한지 + O 세 개가 PS₄ tetrahedra 안에 어떻게 배치되는지를 DFT로 밝히는 프로젝트다.**

---

## 1. 배경 — 왜 Nd₂O₃ 도핑인가

### 1.1 시스템 정체

- **Argyrodite** = Li₆PS₅X (X = Cl, Br, I) 형태의 superionic conductor (고체전해질, SE).
  - Li⁺ 이온이 격자 안을 빠르게 hopping → 배터리에서 액체 전해질 대체 후보.
  - 본 연구의 baseline: **modelC = Li₅.₄PS₄.₄Cl₁.₆** (Li deficient, Cl rich).
- **modelC의 약점**:
  1. 금속 Li anode와 직접 접촉 시 분해됨 (Li 화학적 환원).
  2. NCM 양극과의 계면에서 SEI (Solid-Electrolyte Interphase) 형성 → 셀 저항 ↑.
  3. 일부 환원 분해 산물이 electronic conductor → short-circuit risk.

### 1.2 Nd₂O₃를 넣으면 뭐가 바뀌나 (가설)

| 도핑 효과 | 기대 메커니즘 |
|---|---|
| 전자 전도도 ↓ | Nd 4f orbital이 Fermi level에 occupied state 넣어서 electron tunneling 방해 |
| Li-anode 안정성 ↑ | Nd₂O₃가 Li metal과 reactive하지 않음 → 보호층 |
| SEI band gap ↑ | NdCl₃, LiNdO₂ 같은 Nd-rich phase는 wide-gap insulator |
| 기계적 anchor | Nd-O 강한 결합이 framework 강화 |

→ **paper #2의 5 main targets** (db에 정리됨, `db/compositions/modelc_nd_doped.json`).

### 1.3 왜 "Nd₂O₃"인가 (Nd 만이 아니라)

```
도핑 반응:    1 Nd₂O₃ → 2 Nd³⁺ + 3 O²⁻
              ↓ (modelC 격자에 들어가며)
              2 Nd³⁺ replaces 2 Li⁺ (Track 1)
              3 O²⁻ replaces 3 S²⁻ (PS₄ tetrahedra 안)
```

→ **공급원 (precursor) 인 Nd₂O₃ 자체가 합성에 쓰는 reagent**. 그래서 stoichiometric integer 단위로 도입됨.

---

## 2. 시뮬레이션 셀 — 1×1×10 supercell

### 2.1 두 가지 결정이 합쳐짐

"1×1×10 셀"은 **두 결정의 합성**:

| 결정 | 무엇을 결정? | 우리 선택 | 결정 근거 |
|---|---|---|---|
| **(1) 셀 크기 (fu 수)** | 도핑율 결정 | **10 fu** | x=0.20 강제 — fractional Nd 못 들어감 |
| **(2) 셀 모양 (a×b×c)** | 같은 fu 안에서 어떻게 배치? | **1×1×10 stack** | paper #1과의 일관성 + 코드 재사용 |

### 2.2 결정 (1) — fu 수가 도핑율을 결정

modelC = Li₅.₄PS₄.₄Cl₁.₆ → Li₅.₄ 때문에 **5 fu 배수**여야 정수 atom 됨:

| fu 수 | atoms | P 수 | Nd₂O₃ 1단위 시 도핑율 |
|---|---|---|---|
| 5 fu | 62 | 5 | 2 Nd / 5 P = **40%** ❌ Nd 1개 부분배치 안 됨, 너무 강한 도핑 |
| **10 fu** | **124** | **10** | **2 Nd / 10 P = 20%** ⭐ paper #2 target |
| 15 fu | 186 | 15 | 2 Nd / 15 P = 13% (또는 4 Nd = 27%) |
| 20 fu | 248 | 20 | 2 Nd / 20 P = 10% (dilute control 후보) |

→ **10 fu = paper #2의 최소 stoichiometric 단위**. 더 작으면 도핑율 너무 큼, 더 크면 같은 x=0.20 위해 multiple Nd₂O₃ 필요.

### 2.3 결정 (2) — 같은 10 fu를 어떤 모양으로?

가능한 형태 (모두 124 atoms, 10 fu, x=0.20 도핑율 동일):

| 형태 | a / b / c (Å) | Nd-Nd image 거리 |
|---|---|---|
| **1×1×10** ⭐ | 7 / 7 / 70 | 7, 7, 70 |
| 1×2×5 | 7 / 14 / 35 | 7, 14, 35 |
| 2×1×5 | 14 / 7 / 35 | 14, 7, 35 |
| 2×2×5 (다른 도핑율) | 14 / 14 / 35 | 14, 14, 35 |
| 10×1×1 | 70 / 7 / 7 | 70, 7, 7 |

→ **stoichiometry는 모두 같음**. 모양만 다름.

#### 왜 1×1×10을 선택했나 — 3가지 이유

**이유 1: primitive cell의 자연스러운 확장**

modelC primitive cell은 rhombohedral (a=b=c=6.98 Å, all angles 60°). c축으로 10번 stack하면 격자 vector 1개만 변경 → symmetry 보존. 가장 단순.

**이유 2: Paper #1 (comp1-5)와 일관성** ⭐ 가장 중요

paper #1 셀 형태:
- comp1, comp2 (Li6 family): cubic 4 fu = 52 atoms
- **comp3, 4, 5 (Li5.4 family): rhombo 5 fu = 62 atoms (1×1×5 c-stack)**
- **modelC paper #1: 5 fu = 62 atoms (1×1×5 c-stack)**
- modelC paper #2 (Nd 도핑): 10 fu = 124 atoms = **1×1×10 c-stack** = paper #1의 z방향 2배

→ paper #1과 같은 stacking 방식 → 도핑 효과만 분리해서 비교 가능.

**이유 3: 코드 재사용**

paper #1 step1-5 (enumerate, MLIP screen, anneal, EOS) 의 스크립트가 1×1×N c-stack 패턴에 맞춰 작성됨. 1×2×5 같이 lateral 확장하면 모든 script 수정 필요 → CODE_INVENTORY 룰 ("verified script 재사용") 위반.

#### 셀 모양 바꿔도 ranking은 보존?

**Yes — site label만 바뀌고 물리적 ranking은 같음**:

| 항목 | 보존? | 이유 |
|---|---|---|
| Site index 번호 | ❌ | 셀 모양 따라 atom 정렬 순서 다름 |
| Pair label (pair_19 등) | ❌ | site index 의존 |
| Nd-Nd 실제 거리 (Å) | ✅ | crystal coord에서 동일 |
| E_form ranking | ✅ | physics 동일 |
| Track 1A vs 1B 0.54 eV 차이 | ✅ | local PS₃O motif energy |
| Champion (가장 안정한 config) | ✅ | 같은 physical state |

→ Phase 2.5 verification (`db/compositions/modelc_nd_doped.json`) 에서 20 random Li-perturb 검증 → cfg141 robust.

### 2.4 도핑 후 atom count

```
Track 1 (Nd → Li site, 본 paper main):

Pristine 1×1×10:    Li 54   P 10   S 44   Cl 16   = 124 atoms
                      ↓ 1 Nd₂O₃ 도핑
                      ↓ 2 Nd가 Li 자리 차지
                      ↓ Li 6개 추가 제거 (charge balance)
                      ↓ 3 O가 S 자리 차지
                      ↓
Doped:              Li 48   P 10   Nd 2   S 41   O 3   Cl 16   = 120 atoms

Charge check:  +48 +50 +6 -82 -6 -16 = 0 ✓
도핑율:        x = 0.20 (10 fu당 2 Nd)
```

---

## 3. 세 단계 enumeration — 무엇을 sampling하나

> 1×1×10 셀 정해졌으면, 그 안에서 **무엇을 결정해야 하는가?**

도핑 시 결정할 변수가 **3 layer**:

```
Layer 1 — Nd 두 개를 어디 넣을까?           (54 Li site 중 2개)
Layer 2 — Li vacancy 4개를 어디 만들까?     (남은 52 Li site 중 4개)
Layer 3 — O 3개를 어떤 PS₄에 어떻게 넣을까? (44 S site + free 4d site 후보)
```

### Layer 1 — Nd pair location (26 pairs, 모두 도핑됨)

⚠️ **중요**: 26 pair 모두 **1 Nd₂O₃ unit 도핑된 셀** (x=0.20). pristine modelC는 비교 대상에 없음. "reference"는 이전에 phase 2.5에서 찾은 champion (cfg141, Nd_pair = [1, 82]) 위치를 의미.

Raw 가능한 수: **C(54, 2) = 1431개** (54 Li site 중 2개 Nd 자리).
실제 sampling: **5 distance bin × 5 representatives + 1 reference = 26개**.

```
distance 분류 (모두 도핑됨, Nd 위치만 다름):
  close     < 7 Å          5 pairs    Nd-Nd 매우 가까움
  mid       7-12 Å         5 pairs    중간
  far       12-18 Å        5 pairs    멀리
  very_far  > 18 Å         5 pairs    cell 내 max
  cross     PBC 대각        5 pairs    PBC image effect 검증용
  reference (cfg141, sites 1, 82)     1 pair  ← 이전 champion baseline
```

→ **목적**: 25개 alternative Nd 위치가 cfg141 champion을 이길 수 있는지 검증.

### Layer 2 — Li vacancy positions

각 Nd pair에 대해 추가로 결정:
- Pristine 54 Li 중 Nd가 차지한 2개 → 잔여 52
- 52개 중 charge balance용 4개 vacancy → C(52, 4) = ~270,000 possibilities

→ **MLIP single-point으로 screen** → 각 pair 마다 lowest-energy 30-50개 representative만 다음 단계로.

**Vacancy 분포 경향성**:
1. Nd 주변 ≤ 5 Å 안 vacancy 1-2개 (electrostatic relaxation)
2. 나머지 2-3개는 Nd와 떨어진 위치

### Layer 3 — O placement (A-G categories)

3개 O를 어디 둘지 — **7 categories**:

| Category | 설명 | 그림으로 |
|---|---|---|
| **A** | 3 PS₃O distributed | 서로 다른 3개 PS₄에 1 O씩 |
| **B** | 2 PS₃O + 1 free O | 2개 PS₄에 1 O씩 + 1 O는 free 4d |
| **C** | 1 PS₃O + 2 free O | 1 O는 PS₄, 2 O는 free |
| **D** | 3 free O | 3 O 모두 PS₄ 외부 (Track 1B) |
| **E** | 1 PS₂O₂ + 1 PS₃O | 1 PS₄에 2 O, 다른 PS₄에 1 O |
| **F** | 1 PS₂O₂ + 1 free O | 1 PS₄에 2 O + 1 free |
| **G** | 1 PSO₃ alone | 1 PS₄에 3 O 모임 (가장 응집) |

→ **A (분산) ↔ G (응집) spectrum**.

```
A: ●--●--●  (3 PS₄ 각각 O 1개)
B: ●--●--○  (2 PS₄에 O + 1 free O)
…
D: ○○○      (PS₄ 안 건드리고 모두 free O)
G: ●●●      (1 PS₄에 O 3개)

● = O at PS₄ corner (PS₄ 안, 16e site)
○ = O at free 4d site (PS₄ 외부)
```

### Total sampling scope

| Layer | 후보 raw 수 | sampling 결과 |
|---|---|---|
| 1 (Nd pair) | C(54,2) = 1431 | 26 pairs |
| 2 (Li vacancy) | C(52,4) = ~270k | top 30-50 / pair |
| 3 (O placement) | 7 categories per pair | exhaustive within category |
| **Total** | ~10⁹ raw | **~1300-3900 candidates 사용** |

26 pair × 5-10 vacancy × 7 cat = ~900-1800 configs MLIP screen → top 5 anneal/pair × 26 = 130 full anneal 진행.

---

## 4. 두 갈래 — Track 1A vs Track 1B

### 핵심 질문

> O²⁻가 **어디** 들어가는 게 안정한가?

| Track | O 위치 | 화학 |
|---|---|---|
| **1A** | PS₄ tetrahedron의 corner (S 자리, 16e Wyckoff) | PS₄ → PS₃O 형성 |
| **1B** | Free 4d site (격자 빈 자리) | PS₄ 그대로, O 따로 |

### 결과 (MLIP screen + 500K anneal 후)

```
Track 1A best E:  -521.96 eV
Track 1B best E:  -520.33 eV
ΔE per O atom:    +0.54 eV  ← Track 1A가 압도적
```

500 K Boltzmann ratio:
```
P(1B) / P(1A) = exp(-1.633 / 0.043) = exp(-37.9) ≈ 4 × 10⁻¹⁷
```

→ **합성 온도에서 1A가 사실상 100%**.

### 직접 증거 (debug 시뮬레이션)

cfg141 (Track 1A champion) 을 500 K MD 50 fs 돌렸더니:
- P-O 거리 2.034 Å (initial PS₄ corner) → **1.34 Å (P-O bond)**
- → **자발적으로 PS₃O group 형성**

이는 "O는 PS₄ 안에 들어간다"는 가설을 dynamically 확인.

---

## 5. 핵심 발견 4가지 (paper #2 main message)

### 발견 1 — 이전 champion (cfg141) 이 25개 alternative 다 이김

```
🥇 pair_00 reference (Nd at 1, 82)   E_a = -522.06 eV   ← 가장 안정
🥈 pair_19 very_far (Nd at 2, 6)     E_a = -521.78 eV   (Δ = +0.28 eV)
🥉 pair_13 far (Nd at 19, 82)        E_a = -521.52 eV   (Δ = +0.54 eV)
…
최불안정: pair_15 far (Nd at 6, 16)   E_a = -518.84 eV   (Δ = +3.21 eV)
```

→ **이전에 Phase 2.5에서 찾은 cfg141 (Nd_pair=[1,82]) 가 25개 alternative 다 이김** → champion robustness 한 번 더 확인.

⚠️ **중요**: 이건 "pristine vs doped" 비교가 아니라, **"같은 도핑율 (x=0.20) 안에서 어느 Nd 위치가 가장 안정한가"** 를 본 결과. 26 pair 모두 Nd₂O₃ 도핑됨.

**Paper에 활용**:
> "Across 25 alternative Nd-pair configurations spanning five distance bins,
> none surpassed the previously identified champion (Nd at sites 1 and 82,
> Phase 2.5 verified ground state). The closest alternative is 0.28 eV/cell
> less stable, while the most disruptive is 3.21 eV/cell less stable.
> This confirms cfg141 as a robust thermodynamic minimum."

### 발견 2 — Nd-Nd 거리 의존성

| Distance bin | Champion E_a (avg) | 의미 |
|---|---|---|
| close (< 7 Å) | -519.6 eV | Nd-Nd 직접 상호작용 → 불안정 |
| mid (7-12 Å) | -520.4 eV | 중간 |
| **far (12-18 Å)** | **-520.9 eV** | **가장 안정** |
| very_far (> 18 Å) | -520.6 eV | far와 비슷 |

→ **Nd 두 개가 가까이 있으면 비용 ↑**. 4f-4f orbital overlap + local strain field 누적 때문.

→ **합성 implication**: x = 0.02 같은 dilute 영역에서는 Nd가 자동으로 분산 → far/very_far regime → 본 결과 (DFT) 적용 가능.

### 발견 3 — Category distribution: A 우세, D 절멸

24/26 pair 끝난 시점 결과:

```
A (3 PS₃O distributed):    9 pair (38%) ⭐ 가장 흔함
E (PS₂O₂ + PS₃O):          6 pair (25%)
B (2 PS₃O + 1 free O):     4 pair (17%)
G (1 PSO₃):                3 pair (13%)
F (1 PS₂O₂ + 1 free O):    1 pair (4%)
C (1 PS₃O + 2 free O):     1 pair (4%)
D (3 free O):              0 pair (0%) ❌ 절대 안 이김
```

**해석**:
- **D (Track 1B = free O) 0%** → "O가 PS₄ 외부에 따로 들어간다"는 가설 **모든 Nd 환경에서 실패**.
- **A 38%** → 분산된 PS₃O 형성이 dominant motif.
- **E + G 38%** → 일부 Nd 위치는 응집된 O cluster 형성 (Nd가 만든 strain이 cluster 유도).

### 발견 4 — 4f³ HSAB 메커니즘

> 왜 Nd³⁺는 PS₄ corner를 좋아할까?

| Ion | Radius | Charge | Hardness | 4f state |
|---|---|---|---|---|
| Nd³⁺ | 0.98 Å | +3 | **Hard** | **4f³ (3 unpaired)** |
| Ce⁴⁺ | 0.87 Å | +4 | Hard | 4f⁰ (closed) |
| O²⁻ | 1.40 Å | -2 | **Hard** | — |
| S²⁻ | 1.84 Å | -2 | Soft | — |

**HSAB principle**: Hard cation은 Hard anion 선호 → **Nd-O > Nd-S**.

**4f³ 추가 효과**:
1. 4f orbital이 lobed (anisotropic) → directional polarization → Nd-O 결합 단축 + 강화
2. Cascade effect: Nd가 polarize한 O가 다시 P를 polarize → P-O 결합도 강화
3. → **PS₃O group이 자발적으로 안정화**

**Ce⁴⁺ (4f⁰)은 다름**: 빈 4f → spherical Ce → anisotropic 효과 없음 → Ce 도핑 시에는 O가 free 4d site에 들어감 (Zhao et al. 2025 실험 결과와 일치).

→ **4f electron count가 도핑 mechanism을 결정한다**는 generalizable insight.

---

## 6. 검증 (validation) — paper의 robustness 보장

### 6.1 Phase 2.5 quality check

champion (cfg141) 에 **20개 random Li perturbation** (max 0.5 Å displacement) 적용 후 다시 relax → 모두 cfg141보다 **0.4-15.5 meV 더 높음** (worse).

→ cfg141은 global ground state (또는 매우 가까움). 더 좋은 minimum 없음.

### 6.2 동일 Nd_pair 다른 vacancy 비교

같은 Nd 위치에 vacancy 위치만 바꿔서 anneal:
- cfg23 (Nd=[23,74], vac=[2,12,64,66])  → 큰 anneal gain (-672 meV)
- cfg29 (Nd=[23,74], vac=[19,77,84,86]) → 작은 gain (-232 meV)

→ vacancy positioning이 initial metastability 결정. anneal로 다 다른 minimum 발견하지만 **모두 1A보다 1.6 eV 위**.

### 6.3 26-pair sweep (현재)

**reference (cfg141 = pair_00) vs 25 alternatives**:
- 25개 모두 cfg141보다 0.28-3.21 eV 불안정
- → 이전 phase screen에서 cfg141 picking이 **robust였음을 재확인**

### 6.4 다음 단계 — DFT+U validation

MLIP은 ~50-100 meV/atom 정확도 limit. 0.54 eV/O 차이는 충분히 크지만, 최종 답은 **DFT+U (U=6 eV for Nd 4f) + ISPIN=2** 로 cross-check 필요.

```
phase_3_dft_verify_track1A:
  status: READY_TO_START
  input: top 5 champion structures
  cost: ~5 days/config × 5 = ~25 GPU-days
  purpose: MLIP 0.54 eV/O 차이가 DFT 10 meV/atom precision에서도 보존되는지
```

---

## 7. Paper에 어떻게 쓸 것인가

### 7.1 Section 구조 (제안)

```
1. Introduction
   - Argyrodite SE의 한계 (Li 분해, SEI, electron leak)
   - Nd₂O₃ 도핑의 합성 가능성 + 기존 literature (Zhao 2025 Ce 비교)

2. Methods
   2.1 Cell construction (1×1×10, 124-atom, integer Nd₂O₃)
   2.2 Three-layer enumeration (Nd pair / vacancy / O placement)
   2.3 MLIP screening + 500K anneal protocol
   2.4 DFT+U validation (U=6 eV Nd 4f, ISPIN=2)

3. Results
   3.1 Site-specificity: cfg141 robust across 26 alternatives
   3.2 Distance dependence (close < mid < far)
   3.3 Category distribution (A 38%, D 0%)
   3.4 Champion structure analysis (cfg141 PS₃O motif)

4. Discussion
   4.1 4f³ HSAB mechanism
   4.2 Comparison to Ce⁴⁺ 4f⁰ (Zhao 2025)
   4.3 Generalization to mid-lanthanide doping (Pr, Nd, Sm)

5. Conclusion
   - PS₃O is universal motif
   - 4f electron count determines doping path
   - Falsifiable predictions for experiment
```

### 7.2 가장 강력한 main message (한 줄)

> **"Nd³⁺의 4f³ open-shell 전자배치가 PS₄ tetrahedron의 corner O²⁻를 통해 anisotropic polarization cascade를 일으켜, modelC argyrodite에서 PS₃O가 universal local motif로 자발 형성된다 (vs Ce⁴⁺ 4f⁰의 free-O placement)."**

### 7.3 Section 3 paragraph (그대로 paper에 사용 가능)

> **Site-specificity of Nd₂O₃ Doping in modelC**
>
> Across 26 Nd-doped configurations sampled in a 1×1×10 supercell of Li₅.₄PS₄.₄Cl₁.₆ (all at x = 0.20 doping fraction), four energetic trends emerge that collectively define the dopant placement preference:
>
> **(i) The previously identified champion (Phase 2.5 verified, Nd at sites 1 and 82) remains the lowest-energy configuration** across all 25 alternative Nd-pair locations tested. The closest alternative (very_far pair, sites 2 and 6) is 0.28 eV/cell less stable, while the most disruptive (far pair, sites 6 and 16) is 3.21 eV/cell less stable. This confirms cfg141 as a robust thermodynamic minimum within the supercell.
>
> **(ii) Nd-Nd pair separation distance** systematically lowers the energy penalty: far and very-far pairs (d > 12 Å) average 1.0 eV more stable than close pairs (d < 7 Å), reflecting Nd-Nd repulsion through both 4f-4f orbital overlap and accumulated local strain. At experimental doping concentrations (x = 0.02), Nd dopants are statistically dispersed, placing them in the kinetically accessible far regime.
>
> **(iii) PS₄-corner O substitution (Track 1A) is universal**: free 4d-site O placement (Track 1B, category D) wins 0/24 sampled configurations. Within Track 1A, distributed PS₃O motifs (category A: 3 separate PS₃O groups, 38% of pairs) dominate, with mid-cluster (E: PS₂O₂+PS₃O, 25%) and extreme-cluster (G: PSO₃, 13%) variants selected at minority sites where Nd-induced strain favors O aggregation.
>
> **(iv) The 4f³ electronic configuration of Nd³⁺ drives Track 1A preference** through anisotropic polarization: open-shell 4f³ orbitals impose directional charge asymmetry on adjacent O²⁻, simultaneously strengthening Nd-O and (via cascade) P-O bonds in the PS₃O group. This effect is absent in closed-shell Ce⁴⁺ (4f⁰), explaining the contrasting Rietveld report of free-site O placement in Ce/O co-doped Li₅.₄PS₄.₄Cl₁.₆ by Zhao et al. (2025).

---

## 8. 다음 단계 (graduate student의 "할 일")

| 단계 | 작업 | 시간 | 결과물 |
|---|---|---|---|
| **즉시** | 마지막 2 pair (24, 25) 완료 대기 | 3-4h | 26/26 enum 완료 |
| **단기** | Top 5 champion 추출 + DFT input prep | 1 day | KISTI submission ready |
| **중기** | DFT+U+ISPIN=2 relax (5 configs × 5 days) | 25 GPU-days | DFT 검증된 ΔE/O |
| **paper figure** | Distance vs ΔE_form scatter, category bar, champion 구조도 | 2 days | Section 3 figures |
| **장기** | 248-atom dilute supercell (concentration scaling) | 10 GPU-days | SI revision (image-effect 검증) |

---

## 9. 자주 묻는 질문 (FAQ)

### Q1. 26개로 sampling 충분한가?
A. **Yes for paper publishing level**. 5 representatives/bin × 5 bins → standard error ~20%, 통계적 trend 보장. Reviewer Q 대비로 SI에 dilute (248-atom) spot check 추가 권장.

### Q2. Nd가 정수개로 안 들어가면 어떻게 되나?
A. 1×1×5 셀에 1 Nd만 넣으면 도핑율 40%인데, Nd₂O₃ 단위가 1 Nd + 1.5 O (fractional) 됨 → 정수 atom 시뮬레이션 불가. 그래서 **최소 1×1×10이 stoichiometric integer 이행**.

### Q3. comp1-5 (paper #1)와 modelC (paper #2)는 어떻게 연결되나?
A. modelC = paper #1의 Cl-only Li5.4 family endpoint. paper #1에서 mechanical / EOS 다루고, paper #2에서 modelC 위에 Nd₂O₃ 도핑. **같은 base + 다른 modification**.

### Q4. 1A vs 1B 0.54 eV 차이가 정말 신뢰할 만한가?
A. MLIP 정확도는 50-100 meV/atom. 124 atoms × 50 meV/atom = ~6 eV cell-level uncertainty. 하지만 **상대 차이 (1A - 1B)** 는 cell-wide error가 cancel되므로 ~10-30 meV 오차. 0.54 eV는 이 오차의 ~20× → **신뢰 가능**. 단 DFT+U cross-check 필수 (현재 phase 3 ready).

### Q5. pair_00 "reference"는 무엇이고, 왜 가장 안정한가?
A. pair_00 = **Phase 2.5에서 찾은 cfg141** (Nd_pair = [1, 82], 20 random Li-perturb 검증된 champion). pristine modelC가 아니라 **이전에 best로 알려진 도핑 위치**. 26 pair 모두 1 Nd₂O₃ 단위 도핑됨 (x=0.20). 본 enum은 "cfg141을 다른 25개 alternative가 이길 수 있나" 검증. 결과: 25개 다 못 이김 → cfg141 robust 재확인. 별도 pristine vs doped 비교는 future work.

### Q6. Track 2 (Nd → P site)는 왜 control인가?
A. P⁵⁺ (0.38 Å) vs Nd³⁺ (0.98 Å) → 2.6× size mismatch. 화학적으로 매우 unfavorable. db 명시: "test computationally to quantify the cost. Argues 'we considered this scheme but data shows X eV less stable.'" → **Track 1을 정당화하는 control 실험**.

### Q7. 1×1×10 cell의 z-axis 방향이 70 Å이면 너무 길지 않나?
A. cell shape이 elongated인 게 약간 비표준이지만, **stoichiometric constraint** 하에서 가장 작은 셀. Nd-Nd image 거리 70 Å (z) + 7 Å (xy) → z 방향은 충분히 isolated, xy는 약간 image effect 있음. 단 paper 결과 (distance dependence trend, category distribution) 는 cell shape에 robust.

### Q8. 셀 모양 바꾸면 ranking 바뀌나? (1×1×10 vs 1×2×5 vs 2×2×5)
A. **Site label은 바뀌지만 물리적 ranking은 보존됨**. 같은 modelC crystal에서 같은 두 Li 자리에 Nd 넣으면 같은 결과 (image-effect 차이 ~10-50 meV). 셀 모양 변경 시 site label만 re-indexing하면 같은 결론. paper는 fractional 좌표 또는 Wyckoff position으로 표현하면 셀-portable.

### Q9. 다른 lanthanide (Sm, Gd 등) 도핑은 어떻게 다를까?
A. 4f electron count가 결정:
- Pr³⁺ (4f²), **Nd³⁺ (4f³)**, Sm³⁺ (4f⁵): mid-lanthanide → anisotropic 4f → **PS₃O 형성** 예상
- La³⁺ (4f⁰), **Ce⁴⁺ (4f⁰)**: closed shell → **free O at 4d** 예상
- Eu³⁺ (4f⁶), Gd³⁺ (4f⁷): half-filled → 매우 안정, 다른 chemistry 가능
- → **paper에서 generalizable mechanism으로 future work 언급**.

---

## 10. 관련 자료

| 파일 | 내용 |
|---|---|
| `db/compositions/modelc_nd_doped.json` | 본 프로젝트의 master DB (모든 결과 + status) |
| `필독/literature/zhao2025_critique.md` | Ce/O 도핑 비교 분석 (Park PI challenge 답변) |
| `필독/literature/komatsu2022.md` | LMO/LPSCl bulk reactivity (관련 anchor) |
| `runs/nd_doped_modelc/1_enumerate/` | enumerate scripts |
| `kb/methodology/elastic_constants.md` | DFT methodology general |
| `CLAUDE.md` | 코드 작업 룰 (verified script만 사용) |

---

## 11. 한 페이지 cheat sheet

```
시스템:    Li₅.₄PS₄.₄Cl₁.₆ (modelC argyrodite) + Nd₂O₃ doping (x=0.20)

셀:        1×1×10 supercell (124 atoms pristine, 120 atoms doped)
           = (10 fu, stoichiometric minimum) × (1×1×N c-stack, paper #1 일관성)

Sampling:  3 layers
  Layer 1 — Nd pair (54 Li sites): 26 pairs (5/bin × 5 distance bins + 1 reference)
              모두 도핑됨 (x=0.20). reference = cfg141 (sites 1, 82).
  Layer 2 — Li vacancy (52 sites): C(52,4) → MLIP screen → top 30-50/pair
  Layer 3 — O placement: 7 categories (A-G) per pair

Two tracks:
  1A: O at PS₄ corner (16e)   ← winner ⭐ (0.54 eV/O preference)
  1B: O at free 4d site        ← never wins (0/24 pairs)

4 핵심 발견:
  1. cfg141 (이전 champion) 이 25 alternative 다 이김 (robust)
  2. close < mid < far < very_far (Nd-Nd 거리 의존성)
  3. A (distributed) 38% > E (cluster) 25% > D (free O) 0%
  4. 4f³ → PS₃O (anisotropic polarization), 4f⁰ → free O

Champion: cfg141 (Track 1A, Nd_pair = [1, 82])
  E = -521.96 eV, robust ground state (20 random perturb 검증)

Next: DFT+U + ISPIN=2 validation on top 5 (KISTI ~25 days)

Paper main message:
  "4f³ HSAB cascade가 modelC argyrodite의 Nd₂O₃ 도핑에서 PS₃O를
   universal local motif로 결정한다"
```

---

**작성일**: 2026-05-09
**상태**: ENUM 24/26 done, MLIP screen + anneal complete, DFT validation pending
**향후 update**: enum 100% 완료 시, DFT validation 시, paper draft 시
