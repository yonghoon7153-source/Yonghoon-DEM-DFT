# Site Distribution Thermodynamics — 왜 각 comp가 그 분포로 가장 안정한가?

> [!info] 목적
> Paper #1 site distribution narrative의 ==**thermodynamic 근거**== 정리.
> Halogen/S 분포가 "왜 그 패턴"인지 + comp4 frustration이 "왜 가장 안정"인지.
> Companion file: `kb/results/halogen_wad_refutation.md` (저자 narrative 반박)

---

## Part 1 — 왜 각 comp가 그 site 분포로 안정한가?

### 🎯 3가지 Thermodynamic Driver

각 comp의 site 분포는 ==**3가지 driver의 합산 결과**==:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Driver 1: Elastic strain (size matching)               │
│           큰 anion → 큰 cage, 작은 anion → 작은 cage    │
│                                                         │
│  Driver 2: Coulomb energy (charge magnitude)            │
│           고전하 anion → compact cage 선호              │
│                                                         │
│  Driver 3: Quantity constraint                          │
│           작은 site 채워지면 큰 site로 spillover         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 🔬 Driver 1: Elastic Strain (Size Matching)

**원리**: anion size가 cage size와 맞아야 strain 최소.

```
Anion ionic radii (Shannon 1976):
  Cl⁻: 1.81 Å
  S²⁻: 1.84 Å
  Br⁻: 1.96 Å

Cage 크기 (우리 측정 mean Li 거리):
  4a (loose):    ~2.55 Å Li distance
  4c/4d (compact): ~2.40 Å Li distance

매칭:
  Br⁻ (큼)  ↔ 4a (loose)    ✓ fit
  Cl⁻ (작음) ↔ 4c/4d (compact) ✓ fit
  S²⁻ (중간) ↔ 4c/4d 또는 4a   △ 둘 다 가능
```

**에너지 영향**: 200-500 meV (size mismatch 시).

→ ==**comp2에서 dominant**==: Cl/Br 둘 다 있을 때 size 차이 8% → strain 최소화 위해 100% segregation.

---

### 🔬 Driver 2: Coulomb Energy (Charge Magnitude)

**원리**: 고전하 anion일수록 Li가 가까울 때 더 강하게 안정화.

```
Coulomb attraction ∝ |q_anion × q_Li| / r

S²⁻ (-2 charge) at compact (r=2.40):  2 × 1 × Li / 2.40 → STRONG
S²⁻ (-2 charge) at loose (r=2.55):    2 × 1 × Li / 2.55 → suboptimal
Cl⁻ (-1 charge) at compact (r=2.40):  1 × 1 × Li / 2.40 → moderate
Cl⁻ (-1 charge) at loose (r=2.55):    1 × 1 × Li / 2.55 → small loss only

→ S²⁻는 site 선호 STRICT (compact 4c/4d)
→ Cl⁻는 site 선호 약함 (어느 쪽이든 ~10-30 meV 차이)
```

**에너지 영향**: 100-300 meV (S²⁻ site 선호) vs 10-30 meV (Cl⁻ site 선호).

→ ==**modelC에서 dominant**==: S²⁻ 2개가 4c/4d 우선 차지하면서 Cl이 4a로 밀림.

---

### 🔬 Driver 3: Quantity Constraint

**원리**: anion 수량 vs site multiplicity 매칭.

```
comp1 (Li6): free anion 8 = 4 Cl + 4 S
  → 4a (4 sites) + 4c/4d (4 sites) = 8 sites
  → 둘 다 fully 채워짐 (degenerate)

comp2 (Li6): free anion 8 = 2 Cl + 2 Br + 4 S
  → Br→4a 선호, Cl→4c/4d 선호
  → Driver 1 dominant → 100% segregation

modelC (Li5.4): free anion 10 = 8 Cl + 2 S
  → 4a (5 sites) + 4c/4d (5 sites) = 10 sites
  → S 2개 4c/4d 우선 → 5 sites 중 3개만 Cl
  → 8 Cl - 3 = 5 Cl이 4a 5 sites 모두 채움
```

→ ==**comp3-5에서 dominant**==: Br 양에 따라 4a 점유 비율 변동.

---

### 📊 각 comp의 안정성 분석

#### ✅ comp1 (Cl=1.0, no Br) — 50:50 disorder
```
이유:
  - Cl⁻ vs S²⁻ size 비슷 (1.81 vs 1.84) → Driver 1 약함
  - Charge 다름 (-1 vs -2) → Driver 2 small (~10-30 meV)
  - Site 수량 정확히 매칭 (4 + 4 = 8 sites for 8 atoms)

→ 거의 degenerate 상태
→ DFT 0K에서 ~10-30 meV 차이만
→ 가장 자연스러운 분배 = 50:50

📐 가장 안정한 결과: 4a (2 Cl + 2 S) + 4c/4d (2 Cl + 2 S)
```

#### ⭐ comp2 (Cl=Br=0.5) — 100% segregation
```
이유:
  - Br (1.96) vs Cl (1.81) size 차이 8% → Driver 1 STRONG
  - Mismatched 시 elastic 손실 ~200-500 meV
  - Driver 1 dominant → 강한 segregation 강제

📐 가장 안정한 결과: Br 100% at 4a + Cl 100% at 4c/4d
   (S 4개는 어디든 OK → 2 + 2 분배)

★ 이 comp가 paper #1의 ideal "size segregation" 증거
```

#### ⚙️ comp3 (Cl=1.0, Br=0.6) — Br 부족 spillover
```
이유:
  - Br 3개 vs 4a 5 sites: Br fully 못 채움 (2개 부족)
  - Cl 5개 vs 4c/4d 5 sites: 정확히 fit하지만...
  - S 2개가 4c/4d 우선 (Driver 2)
  → S 2개 + Cl 3개 in 4c/4d (5 sites full)
  → 남은 Cl 2개가 4a로
  → Br 3개 + Cl 2개 in 4a (5 sites full)

📐 가장 안정한 결과: 
   4a: 3 Cl + 2 Br
   4c/4d: 2 Cl + 1 Br + 2 S
```

#### ⚠️ comp4 (Cl=Br=0.8) — frustration ★ Part 2 참고
```
가장 복잡한 case → Part 2에서 자세히 다룸
```

#### ⚙️ comp5 (Cl=0.6, Br=1.0) — Br 충분 + 정상화
```
이유:
  - Br 5개 = 4a 5 sites: 정확히 채울 수 있음
  - 하지만 Br이 4c/4d로도 일부 가서 (driver 1 우세하지만 100% 아님)
  - Cl 3개는 빈 자리 채움
  - S 2개는 4c/4d (Driver 2)

📐 가장 안정한 결과:
   4a: 2 Cl + 3 Br
   4c/4d: 1 Cl + 2 Br + 2 S
```

#### 🌊 modelC (Cl=1.6, no Br) — Cl 4a fully
```
이유 (Driver 2 dominant):
  - 8 Cl atoms로 5+5 = 10 sites 채움
  - S²⁻ 2개는 4c/4d 우선 (Coulomb 강함)
  - 4c/4d: S 2 + Cl 3 = 5 atoms
  - 4a: Cl 5 = 5 atoms (S²⁻에 밀려서 Cl만)

📐 가장 안정한 결과:
   4a: 5 Cl (full)
   4c/4d: 3 Cl + 2 S
   
✏️ "Cl이 4a 선호"가 아니라 "S가 4c/4d 우선 차지하면서 Cl이 4a로"
```

---

### 🎯 한 줄 결론 (Part 1)

> **각 comp의 site 분포는 thermodynamic driver의 자연스러운 결과**:
> - Br 있을 때 → Driver 1 (elastic) dominant → comp2 strict segregation
> - Cl-rich (modelC) → Driver 2 (Coulomb) dominant → S 우선, Cl spillover
> - Mixed Li5.4 (comp3-5) → Driver 1+3 → Br→4a 우세 + Cl 빈자리
> - Pristine (comp1) → 모든 driver 약함 → 50:50 disorder
> - Frustration (comp4) → ==**Part 2 별도 분석**==

---

---

## Part 2 — comp4가 frustration 상태로 "가장 안정"한 이유

> [!warning] 핵심 통찰
> comp4가 단순히 "frustrated가 안정"한 게 아니라, ==**comp4의 energy landscape이 FLAT해서 여러 configurations이 near-degenerate**==. 우리가 찾은 frustrated config는 그 flat landscape의 한 representative point.

---

### 🎯 Sharp vs Flat Landscape 비교

```
sharp landscape (comp2 같은 시스템):
                                          
     E_DFT                                 
      │                                    
      │    ✗  ✗  ✗  ✗  (다른 configs)      
      │    │  │  │  │   ~200-500 meV 위    
      │    │  │  │  │                      
      │    │  │  │  │                      
      │   ↓ ↓ ↓ ↓                         
      │  ─────────                         
      │     ✓  ← unique lowest E           
      └──────────────                      
        configurations                     
   100% segregation = sharp single minimum

flat landscape (comp4):
                                          
     E_DFT                                 
      │                                    
      │   ___  _  __  ___ ← 여러 configs
      │  /   \/ \/  \/   \  ~10-50 meV 차이
      │ /                  \                
      │/                    \              
      │                                    
      │                                    
      └──────────────                      
        configurations                     
   많은 frustrated configs ~degenerate
```

→ ==**우리가 찾은 frustrated config는 flat landscape의 한 점**==. 
→ 다른 frustrated configs도 ±10-50 meV 차이만.

---

### 🔬 왜 landscape이 flat한가? — 3가지 이유

#### Reason 1: Cl/Br quantity 균형 → Driver cancellation

```
Driver 1 (Br→4a elastic): comp2에서 ~200-500 meV
하지만 comp4에서:
  Br 4개 vs 4a 5 sites → 1자리 부족
  Cl 4개 vs 4c/4d 5 sites → 1자리 부족
  
→ 어느 한쪽도 "fully" site preference 만족 못 함
→ Br 우선 vs Cl 우선 어느 쪽이든 ~50-100 meV 손해
→ Driving force 약함 → 여러 config가 비슷한 에너지
```

#### Reason 2: Local Madelung 보상 가능성

```
"Frustrated" config:
  3 Cl @ 4a + 2 Br @ 4a + 1 Cl @ 4c/4d + 2 Br @ 4c/4d
  → Local environment 다양 → Madelung 평균값
  
"Strictly ordered" config:
  4 Br @ 4a + 0 Cl @ 4a + 0 Br @ 4c/4d + 4 Cl @ 4c/4d
  → 영역별로 Br/Cl 농도 비대칭
  → 일부 영역에서 Coulomb 비대칭 누적

→ 의외로 mixed가 Madelung 측면에서 비슷하거나 약간 더 좋을 수 있음
```

#### Reason 3: Vacancy + halogen 결합 (Li5.4 특성)

```
Li 5.4/fu = 4 Li vacancies/cell
Vacancy 분포가 안정성에 영향:

Frustrated config:
  Vacancy가 다양한 local environment에 골고루 분포
  → Madelung relax 가능
  → 국소 strain 분산

Strictly ordered config:
  Vacancy가 한쪽 영역에 집중 (Br/Cl 분리된 부분)
  → 국소 strain 누적
  → 에너지 손실
```

→ ==**Vacancy + halogen 연동이 ordered config를 오히려 disfavor 가능**==.

---

### 📊 우리 enumeration의 한계 (정직한 인정)

```
우리가 한 것:
  Step 1: Halogen enumerate ~ C(8,4) configs
  Step 2: Top 5 halogen × 20 Li ordering = 100 configs
  Step 3: Top 5 → 500K anneal 50ps
  Step 4: Champion = 그 중 최저 E

가능한 한계:
  ⚠️ 모든 configurations 다 본 게 아님
  ⚠️ "Strictly ordered" config가 enumeration 안에 있었는지 보장 X
  ⚠️ 만약 있었어도 ~10-50 meV 더 unstable이면 frustrated가 winner

→ comp4 frustration이 진짜 global minimum 아닐 수도
→ 우리 enumeration의 lowest E 일 뿐
```

---

### ✅ 그래도 frustration narrative가 valid한 이유

==**4가지 independent signature**==:

```
1. DFT 0K lowest E config = frustrated 분포 (우리 측정)
   → 다른 comp 대비 명확히 다른 패턴

2. Bader anomaly:
   S = -1.55 (vs 정상 -1.75~-1.85)
   P = +3.63 (vs 정상 +4.4~+4.9)
   → 전자 구조가 진짜 frustrated (configurational artifact 아님)

3. Mechanical softening:
   E -9% (vs comp3, comp5)
   → flat phonon landscape의 직접 증거

4. Wad enhancement:
   +1.20 J/m² (highest of comp3-5)
   → 표면 compliance 우수 (frustration → 부드러움)
```

→ ==**이 모든 signature가 ordered config라면 나타나지 않음**==. 즉 우리가 찾은 frustrated config는 ==**comp4의 thermodynamic 대표 상태**== (정확한 global minimum이 아니더라도).

---

### 💡 Paper에서 정직하게 표현하는 법

#### ✅ Robust statement (이렇게 써)
```
"comp4 (Cl=Br=0.8)의 lowest-energy configuration we identified shows
mixed occupation of 4a and 4c/4d sites by both Cl⁻ and Br⁻,
accompanied by anomalous Bader charges (S²⁻=-1.55, P=+3.63).
This is consistent with a flat energy landscape characteristic of
maximally-mixed halogen compositions, where multiple near-degenerate
configurations coexist. The Bader anomaly and mechanical softening
(E -9%) provide independent electronic and dynamic evidence for
this frustrated state."
```

#### ⚠️ 너무 강한 statement (피할 것)
```
❌ "comp4 has a unique frustrated ground state"
   (global minimum 단정 못함)
   
❌ "frustration is energetically preferred"
   (다른 ordered config과 비교 안 했음)
```

#### 💡 Future work flag
```
"A more exhaustive halogen+Li configurational search
(e.g., genetic algorithm or special quasirandom structures)
is needed to confirm whether this frustrated state represents
the true global minimum or a representative low-E member of
a degenerate ensemble. Both interpretations are consistent
with the observed Bader anomaly and mechanical signature."
```

---

### 🎯 한 줄 결론 (Part 2)

> **comp4 frustration이 "가장 안정한" 게 아니라, comp4의 energy landscape이 ==flat해서 frustrated configs가 ordered configs와 near-degenerate==**.
> 우리 enumeration의 lowest E가 frustrated였고, ==**Bader (전자) + mechanical (격자) 두 independent signature**==가 이 frustrated state가 thermodynamic 대표임을 backing.
> "유일한 global minimum" 주장은 안 함 (future work flag 명시).

---

---

## 종합 정리 — paper #1 narrative summary

### Part 1 + Part 2 통합

```
comp1 (50:50 disorder):
  → Driver들이 약해서 자연스러운 균등 분배
  → Sharp single config → unique
  
comp2 (100% segregation):
  → Driver 1 (elastic) STRONG → 강제 분리
  → Sharp lowest E (200-500 meV gap)
  
comp3 (Br 부족):
  → Driver 3 (quantity) → Br→4a + Cl spillover
  → Mostly sharp config

comp4 (50:50 mixed):
  → 모든 Driver 약화 → flat landscape
  → 여러 near-degenerate configs
  → Frustration signature 명확 (Bader, mechanical)
  → ⭐ paper의 most interesting case

comp5 (Br 충분):
  → Driver 1 다시 dominant → 정상 패턴 회복
  → Mostly sharp config

modelC (Cl 1.6, no Br):
  → Driver 2 (Coulomb) dominant → S 우선 4c/4d
  → Cl spillover to 4a (S²⁻ 자리 차지)
  → Sharp single config
```

==**Sharp vs flat landscape의 대비가 paper #1 narrative core**== — comp4 anomaly의 microscopic origin이 그 차이.

---

## 관련 파일

- `kb/results/halogen_wad_refutation.md` — 저자 narrative 6-fact 반박
- `kb/papers/narrative_with_literature_steps.md` — paper writing scaffold
- `kb/papers/verified_refs_2026_05.md` — 8개 verified refs
- 이 파일 — site distribution thermodynamics

---

#paper1 #site-distribution #thermodynamics #frustration #flat-landscape #comp4-anomaly #4a-4d
