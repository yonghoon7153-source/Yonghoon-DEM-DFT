# 🚨 WHY ADHESION — DFT의 한계와 Paper #2의 존재 이유

> **모든 새 session 시작 시 첫 번째로 읽음** (CLAUDE.md, CODE_INVENTORY.md와 함께)
>
> Paper #1 (B₀, E, Cij)에서 vacancy 효과 capture 실패 → Paper #2 adhesion이 유일한 micro-macro 연결 통로

---

## 핵심 — 한 줄 요약

**Paper #1 DFT mechanical은 vacancy 효과를 잡지 못해서, Paper #2 adhesion (Wad)이 vacancy chemistry → 거시 mechanical 연결의 유일한 quantitative bridge가 됨.**

---

## 1. 실험이 보여주는 vacancy의 stiffening effect

### Nanoindentation E (거시 측정, 실험값)

```
Li6 family:    LPSC1.0 (8.0 GPa)  > LPSC0.5Br0.5 (7.6)
Li5.4 family:  LPSC1.0Br0.6 (18.3) > LPSC0.8Br0.8 (16.5) > LPSC0.6Br1.0 (15.8)

  → Cross-family: Li5.4 (~16-18) >> Li6 (~7-8)
  → vacancy로 E 더 큼 (counterintuitive하지만 nanoindentation으로 확인)
```

### AFM/peel-test Wad (실험)

```
Li6 family:    LPSC1.0 (194 aJ) > LPSC0.5Br0.5 (180)
Li5.4 family:  LPSC1.0Br0.6 (316) > LPSC0.8Br0.8 (298) > LPSC0.6Br1.0 (249)
  
  → Cross-family: Li5.4 (~250-316) > Li6 (~180-194)  ← 같은 vacancy effect
```

**둘 다 거시 측정 (실험)** — vacancy 있는 게 더 단단. counterintuitive하지만 모든 mechanical 측정에서 일관됨.

가능한 mechanism:
- Li-Li repulsion 감소 (Li6 = 빽빽 packed → 반발 큼 → soft)
- Li5.4 = vacancy 풀어줌 → PS4 framework 자유롭게 조여짐 → stiff
- Halogen sublattice (Cl/Br) 정렬도 향상

---

## 2. Paper #1 DFT vs Nanoindentation 실험

### B₀ (Bulk modulus)
```
DFT (paper #1): comp1(26.2) > comp2(25.8) > comp5(22.9) > modelC(21.7) ≈ comp3(20.8) ≈ comp4(20.8) GPa
실험 trend (E 기반 추정): Li5.4 > Li6

→ DFT cross-family: Li6 > Li5.4 (실험 반대 방향)
→ within-family Br trend는 일부 잡음 (comp1>comp2, comp3>comp4>comp5)
```

### Young's modulus E
```
DFT (paper #1, 600K snapshot): comp1(29.1) > comp2(28.6) > comp3(27.3) > comp4(26.4) > comp5(25.8) GPa
실험 (nanoindentation):         comp1(8.0)  > comp2(7.6)  | comp3(18.3) > comp4(16.5) > comp5(15.8)

DFT 결과 vs nanoindentation:
  - 절대값: DFT 26-29 vs 실험 8-18 (DFT 1.5-3배 큼)
  - cross-family ordering: 정반대
    DFT      = Li6 > Li5.4
    실험      = Li5.4 > Li6 (vacancy stiffening)
  - vacancy effect 못 잡음 → 단순히 Br effect 정도만 표현됨
```

### C₄₄ (shear constant) — 더 큰 문제
```
DFT clamped-ion (0K): C₄₄ Li ordering에 매우 민감
  comp5에서 ΔC₄₄ = 12.7 GPa (47% 변동)
  
결과:
  - Li ordering별로 C₄₄ 너무 다양 → 절대값 결정 불가
  - 600K MD snapshot으로 평균하면 thermal disorder 포함되지만
    여전히 vacancy mechanism은 직접 capture 못 함
```

---

## 3. 왜 DFT에서 vacancy 효과가 안 잡히나

### bond length / Bader proxy 한계
```
micro proxies: bond length (Li-S, Li-Cl, P-S) + Bader charge
  ↓
macro: B₀, E, Cij

문제:
  - vacancy로 인한 Li framework 재배열 → bond length 변화 작음
  - Bader charge는 vacancy 직접 표현 못 함
  - "Li density" 효과가 dominant (Li6 = 더 많은 Li = 더 많은 결합 → DFT는 더 stiff로 예측)
  - 실제로는 Li ordering / vacancy → softening 메커니즘이 우세
  - DFT가 ordering optimize 못 한 채 결과 도출 → 실험과 반대
```

### 절대값 신뢰성 문제
```
Cij DFT (clamped-ion 0K):
  Li ordering 1개 선택해서 계산 → 그 ordering의 C44만 반영
  실험은 thermally averaged ordering → DFT와 systematic gap

결과:
  E_DFT > E_실험 (3-4배)
  Cross-family ordering 신뢰 불가
  Within-family Br trend는 작은 차이라 일부 일치
```

---

## 4. 그래서 Wad (Paper #2)가 unique한 이유

### Wad의 micro-macro 직접 연결
```
DFT 계산 → adhesion energy
  ↓ (proxy 불필요)
실험 peeling test → adhesion energy

→ Direct comparison, no proxy interpretation
→ vacancy chemistry (under-coordinated Li → NCM O 결합)이 직접 Wad에 반영
```

### Wad가 capture 가능한 vacancy mechanism
```
Li5.4 (vacancy 있음):
  표면 Li under-coordinated (vacancy 인접)
  → NCM O와 적극 결합 형성 (chemical anchor)
  → 추가 binding contribution
  → Wad 큼

Li6 (vacancy 없음):
  표면 Li 모두 saturated
  → NCM O와 약한 결합만 (정전기 + vdW)
  → Wad 작음

cross-family: Li5.4 > Li6 (실험 일치)
```

---

## 5. Paper 흐름

### Paper #1 (이미 완료)
```
주제: Halogen substitution effect on bulk mechanical properties
결과: B₀, E, Cij DFT 계산
한계: vacancy 효과 못 잡음 (cross-family 실험 반대)
가치: within-family Br effect 정량화 + thermal Cij protocol 제안
```

### Paper #2 (진행 중) — Adhesion이 main
```
주제: Vacancy chemical anchor effect on SE/NCM adhesion
가설: Li5.4 vacancy → 표면 under-coordinated Li → NCM O 결합 → Wad 증가
검증: 
  - Phase 1 (rigid binding curve): vacancy 효과 일부만 보임
  - Phase 2 (LBFGS-relaxed Wad): cross-family ordering 검증 필요 ⭐
  - 만약 Li5.4 > Li6 → Wad가 vacancy mechanism direct capture
                       → Paper #1 한계 극복
                       → Paper #2 main breakthrough

paper #2 unique value:
  "Adhesion is the only mechanical micro-to-macro bridge that 
   captures vacancy chemistry without proxy interpretation"
```

### Paper #2 narrative 후보
```
"Bulk mechanical properties (B₀, E) computed via DFT proxy 
 (bond length, Bader charge) fail to reproduce the experimental 
 cross-family stiffening from Li5.4 vacancy.

 In contrast, adhesion energy Wad — directly computable from 
 LBFGS-relaxed SE/NCM interfaces — captures the vacancy 
 chemical anchor mechanism: under-coordinated Li in Li5.4 
 forms additional Li-O bonds with NCM cathode, providing 
 quantitative micro-to-macro bridge for interfacial 
 mechanical reliability."
```

---

## 6. 모든 후속 작업의 자세

```
✓ adhesion 우선 (Paper #2 main)
✓ Wad가 paper #1 못 잡은 vacancy 효과 잡는지 검증이 critical
✓ Phase 2 protocol 정확히 paper #1 v5 mimic해서 cross-family 시도
✓ 만약 v7도 inversion이면 fundamental 차이 (slab/cell convention) 의심
```

```
✗ B₀/E/Cij 추가 정밀화 시도 (paper #1에서 한계 인정)
✗ bond length / Bader로 vacancy effect 직접 explain 시도
```

---

## 7. 관련 파일

- `db/properties/elastic.json` — paper #1 Cij/E 결과 (vacancy 못 잡은 증거)
- `db/properties/eos.json` — paper #1 B₀ 결과
- `db/properties/adhesion.json` — paper #2 Wad 결과 (진행 중)
- `kb/results/halogen_wad_refutation.md` — paper #1 cross-family 한계 분석
- `kb/methodology/elastic_constants.md` — DFT Cij 한계 + thermal averaging

---

#paper #adhesion #vacancy-effect #limitations #micro-macro #breakthrough
