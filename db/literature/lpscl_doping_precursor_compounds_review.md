# LPSCl Doping — Precursor Compound Combinations (Literature Review)

**작성**: 2026-05-15
**목적**: 실제 합성에서 LPSCl에 도핑되는 화합물 조합을 메커니즘별로 분류. 우리
`tools/doping/substitute_compound.py` 설계의 reference.

LPSCl는 ball mill / 액상 / wet-milling 모두 가능하고 다양한 precursor에서
synthesis 가능 — 그래서 **단일 원소 substitution이 아니라 chemical compound 단위
substitution**이 실제 도핑 메커니즘.

---

## 0. 메커니즘 분류 (4 types)

| Type | 메커니즘 | 예 | charge balance |
|------|---------|----|----|
| **A. 이온 화합물 분해** (set substitution) | precursor가 cation+anion 동시에 lattice 진입 | Nd₂O₃, Al₂O₃, MgO, ZnO, Li₂O | 자동 (compound이 neutral) |
| **B. Halide 풍부화** (Li vacancy 생성) | S²⁻ → Cl⁻로 치환, Li 1개 vacancy 자동 | Li₅.₅PS₄.₅Cl₁.₅, Li₅.₄PS₄.₄Cl₁.₆ | 자동 (전하 보존) |
| **C. Aliovalent cation + halide co-substitution** | Al³⁺ at Li, Cl at S 동시 | Li₅.₄Al₀.₁PS₄.₇Cl₁.₃ | 명시적 stoichiometry |
| **D. Additive (lattice 아닌 부가물)** | 별도 phase로 SEI 형성에 기여 | LiBH₄ 5 wt%, Li₃PS₄ glass | substitution 아님 |

---

## 1. Type A — 이온 화합물 set substitution

### 1.1 Nd₂O₃ (우리 paper #2, BML 슬라이드)
- Nd³⁺ × 2 → Li⁺ 사이트에 (각 Nd 자리당 Li 2개 vacancy 추가 필요?)
- O²⁻ × 3 → S²⁻ 사이트에 (charge swap, Li vacancy 불필요)
- **Compound charge**: 2(+3) + 3(−2) = +6 − 6 = 0 ✓ (neutral)
- **Net Li sublattice 영향**: Nd³⁺ × 2 at Li → ΔQ_cation = (3−1)×2 = +4
  - O²⁻ × 3 at S → ΔQ_anion = (−2−(−2))×3 = 0
  - 전체: +4 → Li vacancy 4개 필요
- Sundar 2025 reference 그룹 (Argonne)이 비슷한 형태 시뮬

### 1.2 Al₂O₃ — alumina coating common precursor
- Al³⁺ × 2 + O²⁻ × 3 동일 패턴
- Sundar 2025 paper coating screening 상위권

### 1.3 MgO — 가장 단순
- Mg²⁺ × 1 + O²⁻ × 1
- Compound 1 unit당: Mg charge +2, O charge −2, balanced
- Net: Mg → Li (charge diff +1), O → S (charge diff 0) → Li vac 1
- Sundar 2025 Top oxide

### 1.4 ZnO — Li6PS5Br에서 보고됨 (sister Br argyrodite)
- Zn²⁺ + O²⁻, MgO와 동일 패턴

### 1.5 Li₂O — pure Li source (Li-rich + O-substitution)
- 2 Li⁺ + 1 O²⁻
- Compound neutral
- "Li2O 부분 substitution Li₆PS₅Cl 또는 Li₆PS₅Br" 보고됨
- 효과: Li 함량 유지(또는 증가) + O 도핑
- Implementation: O를 S 자리에 substitute, Li는 interstitial 또는 기존 자리 보충

### 1.6 P₂O₅, Li₃PO₄ — PO₄³⁻ 단위 도입
- "P₂O₅ into Li5.5PS4.5Cl1.5" — PO₄/PS₄ 부분 swap
- "Li₃PO₄ into Li6PS5Cl" — PO₄³⁻ tetrahedron 자체가 PS₄ 자리에
- **이건 set substitution보다 polyhedron substitution** → 별도 모드

### 1.7 SnO₂ — Li6PS5I 보고
- Sn⁴⁺ + 2 O²⁻
- Compound neutral
- Sn at P site (P5+ → Sn4+, donor → −1 vacancy 필요 다른 자리)

---

## 2. Type B — Halide 풍부화 (Li vacancy 자동)

### 2.1 Li₆₋ₓPS₅₋ₓCl₁₊ₓ family
- x=0: Li₆PS₅Cl (baseline)
- x=0.3: **Li₅.₇PS₄.₇Cl₁.₃** — Kraft 2017 JACS
- x=0.5: **Li₅.₅PS₄.₅Cl₁.₅** — Kraft 2017, **σ = 9.4 mS/cm (4× baseline)** ⭐
- 보통 0.5가 한계 (solid solution limit)
- x=0.6: **Li₅.₄PS₄.₄Cl₁.₆** = 형님 modelc

### Mechanism
- S²⁻ 사이트에서 Cl⁻로 치환 → -1 charge 차
- 각 swap당 Li 1개 vacancy (자동)
- 결과: Li 사이트 disorder ↑, anion site disorder ↑, Li⁺ diffusion 향상
- **Note**: 우리 코드에선 "S 1개 → Cl 1개 + Li vacancy 1개" 로 모델링

### 2.2 NEI 상용 제품 (Li5.5PS4.5Cl1.5)
- σ = 9.4 mS/cm cold-pressed, 12.0 mS/cm sintered
- 상업적으로 생산됨

---

## 3. Type C — Aliovalent cation + halide co-substitution

### 3.1 Al + Cl co-doped (Yu et al. *Nanomaterials* 2022)
DOI: 10.3390/nano12244355

- **Formula**: Li₆₋ₓ₋₃ᵧAlᵧPS₅₋ₓCl₁₊ₓ (0≤x≤0.7, 0≤y≤0.2)
- **Optimal**: Li₅.₄Al₀.₁PS₄.₇Cl₁.₃ (x=0.3, y=0.1)
- **σ = 7.29 mS/cm @ RT, Eₐ = 0.09 eV**
- 4.7× baseline LPSCl

### Mechanism
- Al³⁺ at Li site → +2 net cation charge (per Al, replacing Li⁺)
- Cl⁻ at S site → -1 net anion charge (per Cl)
- 0.1 Al × (+2) = +0.2 vs 0.3 Cl × (-1) = -0.3 → 약간 over-compensate, 추가 Li vac 발생
- Formula 확인: Li 6 − x − 3y = 6 − 0.3 − 0.3 = 5.4 ✓ (3 Li vacancy per Al + 1 per Cl)
- 작은 ionic radius로 lattice 수축 (smaller Al + Cl) → lattice 정렬

### 3.2 일반화
- Mₙ⁺ at Li + Cl at S → formula: Li₆₋ₓ₋ₙᵧMᵧPS₅₋ₓCl₁₊ₓ
- M ∈ {Al³⁺, Y³⁺, Ga³⁺, Sc³⁺, …} 다양

---

## 4. Type D — Additive (lattice 외부)

### 4.1 LiBH₄ (Wang *Adv. Mater.* 2025, ORNL) ⭐
DOI: 10.1002/adma.202506095

- **5 wt% LiBH₄ + LPSCl 복합체** ("5LBH-LPSCl")
- LPSCl lattice 변경 없음, 별도 boron-hydride phase로 분산
- **CCD = 7.3 mA/cm² (baseline 2.6)** — Li dendrite 억제
- ASSB 400 cycle @ 0.5C, 83% capacity retention
- AF-ASSB (anode-free) 600 cycle, 0.04% loss/cycle

### Mechanism
- In situ XPS + ToF-SIMS: **tri-layer SEI = Li₃P / LiBH₄ / Li₂S**
- electron blocking + Li⁺ transport 동시
- baseline LPSCl는 SEI가 Li₃P/Li₂S 두꺼움 → crack 유발

### 4.2 우리 코드에서 처리?
- Lattice substitution 모델로는 불가 (composite phase)
- Surface model + Wad 계산 영역 (별도 워크플로우)

---

## 5. Mixed halide (Br, I)

### 5.1 Li₆PS₅Cl₁₋ₓBrₓ — 우리 v0 paper
- Cl/Br solid solution
- comp2 (Cl₀.₅Br₀.₅), comp3-5 (Br rich)
- Isovalent substitution at Cl_4d/4a site

### 5.2 Li₆PS₅I — separate phase
- I 단독 변종 (Cl-poor side)
- σ slightly lower than Cl/Br, but stabler

### 5.3 I-F dual-doped (JPCC 2023)
- Cl 자리에 I + F 동시 (dual halide)
- 두 halide가 Cl 사이트에서 disorder

---

## 6. Synthesis route 분류

| Route | 특징 | 적합 doping type |
|-------|------|------------------|
| Ball mill (mechanochemical) | dry, 30~50h, energy-intensive | 거의 모든 type (A/B/C 다 됨) |
| Wet-milling + post-anneal | solvent mediated | type A oxides, type B halide-rich |
| Liquid-phase (acetonitrile + thiol) | low T, gram scale | O-doping, oxide precursors |
| Solid-state synthesis | high T (500~600°C), 단순 | type B, C |
| Sintering | post-densification, σ 향상 | 후처리 |

---

## 7. 우리 `tools/doping/substitute_compound.py` 설계 매핑

### 7.1 Type A — 자동화 가능, 우선순위 1
```bash
# Nd2O3 5 mol% (4 f.u. cell 기준 → 0.2 Nd2O3 unit ≈ 0.4 Nd + 0.6 O 정수화 = 1 + 2)
python3 substitute_compound.py --compound Nd2O3 --x_compound 0.05 \
    --cation_site Li_24g --anion_site S_16e
```
입력: compound formula, mole fraction, cation/anion target sites.
출력: 자동 charge balance + Li vacancy 추가.

### 7.2 Type B — halide 풍부화
```bash
# Li5.4PS4.4Cl1.6 만들기 (S→Cl swap + Li vacancy 자동)
python3 substitute_compound.py --halide_rich Cl --excess 0.6 \
    --anion_site S_4a
```
입력: target halide, excess 분량 (per f.u.).
출력: Li vacancy 자동 (1 per swap).

### 7.3 Type C — aliovalent cation + halide
```bash
# Al0.1 + Cl0.3 dual doping
python3 substitute_compound.py --compound2 "Al,Cl" --y_cation 0.1 --x_anion 0.3
```
입력: cation+anion 비율 (independent).
출력: Yu et al. 2022 형식 formula 자동 생성.

### 7.4 Type D — 처리 안 함 (lattice 외부)
LiBH₄ 같은 additive는 별도 surface model이 필요. doping screening 범위 밖.

---

## 8. 참고문헌 핵심 (인용용)

| 출처 | DOI | 핵심 |
|------|-----|------|
| Yu et al. *Nanomaterials* 12, 4355 (2022) | 10.3390/nano12244355 | Al-Cl co-doping σ 7.29 mS/cm |
| Adeli et al. *Angew Chem* 58, 8681 (2019) | 10.1002/anie.201814222 | Halide-rich family Li6−xPS5−xCl1+x |
| Kraft et al. *JACS* 139, 10909 (2017) | 10.1021/jacs.7b06327 | Li5.5PS4.5Cl1.5 9.4 mS/cm |
| Zhao et al. *Solid State Ionics* 401, 116333 (2023) | 10.1016/j.ssi.2023.116333 | Liquid-phase O-doping |
| Wang et al. *J. Power Sources* 412, 29 (2019) | — | NMR Li distribution |
| Pustorino et al. *Chem Mater* 37, 313 (2025) | 10.1021/acs.chemmater.4c02577 | Li ordering ↔ B0 |
| Pham et al. *ACS AMI* 13, 51850 (2021) | 10.1021/acsami.1c14573 | Li6PS5-xClOx best x=0.25 |
| Wang et al. *Adv Mater* 2506095 (2025) | 10.1002/adma.202506095 | LiBH₄ doping mechanism |
| Sundar et al. (2025) | (Argonne) | Coating screening, oxide precursors |
| Huang et al. *Energy Technol* 13 (2025) | 10.1002/ente.202401420 | Doping strategies review |

---

## 9. 우리 작업 우선순위

1. **즉시**: `substitute_compound.py` Type A 구현 (Nd₂O₃ 첫 케이스 — paper #2 직결)
2. **다음**: Type B halide-rich (Li5.4PS4.4Cl1.6 ≡ modelc 재현 가능해짐)
3. **그 다음**: Type C aliovalent co-doping (Al-Cl 검증된 chemistry)
4. **Future**: Type D는 별도 surface/SEI workflow

특히 (1)이 즉시 가치 큼 — KISTI에서 진행 중인 Nd-doped paper #2가 결국 **Nd₂O₃
substitution**이므로, 단일 원소 Nd 모드가 아니라 정확한 화합물 단위 substitution
모델이 필요. 현재 `prepare_dft_eos_nd.py`가 사용하는 enumerate_mixed_O.py도
이 로직과 align 필요.
