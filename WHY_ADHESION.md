# 🚨 WHY ADHESION — Paper #2의 존재 이유

> **모든 새 session 첫 번째로 읽음** (CLAUDE.md, CODE_INVENTORY.md와 함께)
>
> Paper #1에서 DFT가 vacancy 효과를 못 잡았다. Paper #2 adhesion은 그 한계를 넘는 유일한 통로.

---

## 한 줄 요약

**거시 mechanical 측정 (nanoindentation, peel test)에서 Li5.4 vacancy가 stiffer/stronger한데, paper #1 DFT (B₀, E, Cij)는 이걸 못 잡아냈다. Wad만이 vacancy chemistry → 거시 mechanical 직접 연결할 수 있어서 paper #2의 main breakthrough가 됨.**

---

## 1. 거시 mechanical 실험 — vacancy → stiffer

### Nanoindentation (Young's modulus E, 실험)
```
Li6 family (no vacancy):
  LPSC1.0      :  8.0 GPa
  LPSC0.5Br0.5 :  7.6 GPa

Li5.4 family (43% vacancy):
  LPSC1.0Br0.6 : 18.3 GPa
  LPSC0.8Br0.8 : 16.5 GPa
  LPSC0.6Br1.0 : 15.8 GPa

→ Li5.4 (~16-18) >> Li6 (~7-8)
→ Vacancy로 E 2배 이상 stiffer
```

### Adhesion (Wad, AFM/peel-test 실험)
```
Li6:    LPSC1.0 (194 aJ) > LPSC0.5Br0.5 (180)
Li5.4:  LPSC1.0Br0.6 (316) > LPSC0.8Br0.8 (298) > LPSC0.6Br1.0 (249)

→ Li5.4 (~250-316) > Li6 (~180-194)
→ Vacancy로 Wad ↑ (같은 stiffening trend)
```

**둘 다 거시 측정 실험값**. counterintuitive하지만 모든 mechanical 측정에서 일관: **vacancy가 단단하게 만듦**.

가능한 mechanism:
- Li-Li repulsion 감소 (Li6 = packed → 반발 큼 → soft)
- Li5.4 = vacancy → PS₄ framework가 stress-free하게 자기 위치로
- Halogen sublattice 정렬도 향상

---

## 2. Paper #1 DFT의 두 가지 결정적 한계

### 한계 1: C₄₄가 Li ordering에 너무 민감 → 절대값 신뢰 불가
```
Cij DFT (clamped-ion 0K):
  comp5 결과: Li ordering 1개 vs 다른 ordering
    ΔC₄₄ = 12.7 GPa (47% 변동)
  
문제:
  - 어떤 Li ordering 골라야 할지 결정 불가
  - 절대값이 ordering 선택에 매우 의존적
  - 실험 (thermal averaging)과 직접 비교 어려움
  
시도한 mitigation:
  - 600K MD snapshot averaging (5개 snapshot × VRH)
  - 일부 개선되지만 여전히 cross-family는 못 잡음
```

### 한계 2: 영률에서 vacancy effect 실종 → Br effect만 보임
```
DFT 600K snapshot E (paper #1):
  comp1: 29.1
  comp2: 28.6
  comp3: 27.3
  comp4: 26.4
  comp5: 25.8 GPa

→ 단조 감소: comp1>comp2>comp3>comp4>comp5
→ Br ↑ → E ↓ 인 trend만 보임 (within-family)
→ Cross-family에서 Li5.4가 Li6보다 작음 (정반대)

실험 nanoindentation:
  Li6:    8.0, 7.6
  Li5.4: 18.3, 16.5, 15.8
  → Cross-family에서 Li5.4가 Li6보다 2배 이상 큼

DFT는 Br effect (작은 차이) 정도만 capture
Vacancy effect (큰 차이) 못 capture
```

### 왜 못 잡나
```
bond length / Bader proxy:
  bond: vacancy로 인한 framework 재배열 → bond length 변화 작음
  Bader: vacancy 자체를 charge로 표현 못 함
  
DFT mechanical:
  ordering 1개 선택 → 그 ordering 결과만 반영
  실제 thermally averaged ordering 표현 어려움
  C44 ordering sensitivity로 noise 큼

micro proxies로는 vacancy mechanism 표현 한계 명확
```

---

## 3. Wad만이 vacancy mechanism 직접 capture 가능

### Wad의 micro-macro 직접 연결
```
DFT 계산 → Wad (J/m²)
  ↓ proxy 불필요
실험 peel test → Wad

→ 직접 비교, no interpretation
→ vacancy chemistry가 직접 Wad에 반영
```

### Vacancy chemical anchor mechanism (가설)
```
Li5.4 (vacancy 있음):
  표면 Li under-coordinated (vacancy 인접)
  → NCM O와 적극 결합 (chemical anchor)
  → Wad 큼

Li6 (vacancy 없음):
  표면 Li 모두 saturated
  → NCM O와 약한 결합만
  → Wad 작음

cross-family: Li5.4 > Li6 (실험 일치)
```

### Paper #2 검증의 stakes
```
v7 (paper #1 v5 protocol mimic) 결과:
  Li5.4 > Li6 (cross-family) → Wad가 vacancy mechanism capture ✓
                                Paper #1 한계 극복 → Paper #2 main breakthrough
                                
  Li5.4 < Li6 (inversion)    → Wad도 못 잡음
                                fundamental issue (DFT/MLIP 자체 한계)
                                Paper #2 narrative 어려움
```

---

## 4. Paper 흐름 정리

### Paper #1 (완료)
```
주제: Halogen substitution effect on bulk mechanical properties
계산: B₀, E, Cij (DFT EOS + finite strain elastic)
결과:
  ✓ within-family Br trend (comp1>comp2, comp3>comp4>comp5)
  ✗ cross-family vacancy effect 정반대 (Li6>Li5.4)
  ✗ C44 절대값 불신 (Li ordering 47% 변동)
  
가치: Br substitution → property tuning 정량화
한계: vacancy mechanism 표현 실패
```

### Paper #2 (진행 중) — Adhesion main
```
주제: Vacancy chemical anchor effect on SE/NCM adhesion
가설: Li5.4 vacancy → 표면 under-coordinated Li → NCM O 결합 → Wad ↑

unique value:
  "Adhesion is the only mechanical micro-to-macro bridge that 
   captures vacancy chemistry without proxy interpretation"
   
검증 status:
  Phase 1 (rigid binding curve): vacancy effect 일부 (Br trend만 일치)
  Phase 2 (LBFGS-relaxed Wad):   cross-family ordering 검증 중 ⭐
```

---

## 5. 모든 후속 작업 자세

### 우선
- ✓ Adhesion (Paper #2 main)
- ✓ Wad가 paper #1 못 잡은 vacancy 효과 잡는지 검증
- ✓ Phase 2 protocol 정확히 paper #1 v5 mimic
- ✓ Cross-family 일치 시 → "vacancy chemical anchor" 결정적 증거

### 안 함
- ✗ B₀/E/Cij 추가 정밀화 (paper #1 한계 인정)
- ✗ bond length / Bader로 vacancy effect 직접 explain 시도
- ✗ DFT C44 ordering sensitivity 해소 시도 (intractable)

---

## 6. 관련 파일

- `db/properties/elastic.json` — paper #1 Cij/E 결과 (vacancy 못 잡음)
- `db/properties/eos.json` — paper #1 B₀ 결과
- `db/properties/adhesion.json` — paper #2 Wad 결과 (진행 중)
- `kb/results/halogen_wad_refutation.md` — paper #1 cross-family 한계 분석
- `kb/methodology/elastic_constants.md` — DFT Cij Li ordering 문제

---

#paper #adhesion #vacancy #limitations #micro-macro #breakthrough #must-read
