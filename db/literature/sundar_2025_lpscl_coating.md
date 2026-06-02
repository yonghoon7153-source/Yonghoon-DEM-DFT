# 📄 Sundar et al. 2025 — Computationally-Guided LPSCl Oxide Coating

> **Reference**: Sundar, A., Kim, T., Lagunas, F., Mane, A. U., Eze, U. D.,
> Ginter, C., Pathak, R., Tepavcevic, S., Elam, J. W., Hood, Z. D., Zapol, P.,
> Connell, J. G. *Adv. Sci.* **2025**, e13191.
> DOI: [10.1002/advs.202513191](https://doi.org/10.1002/advs.202513191)
> Affiliation: **Argonne National Lab** + UChicago.
> Patent filed by Argonne authors.

> **Status for our project**: 본 paper는 **우리 디지털 트윈 프로젝트와 동일
> 영역**이지만 (LPSCl 코팅), 우리가 가는 길보다 **2-step DFT-only 워크플로우**
> 라 더 느리고 제한적. 우리 프로젝트의 **차별화 포인트 + 흡수할 점** 을 명확히
> 정리.

---

## 1. 그들의 핵심 결론 (3줄)

1. ALD 기반 LPSCl powder 코팅 후보 **MgO, ZrO₂, ZnO** 식별. **MgO가 다목적 best**
   (이온전도도 ↑, 전자전도도 ↓, Li metal 안정성 ↑, ASR ↓, CCD ↑).
2. Critical insight: **반응 생성물의 이온/전자 전도도가 Coating 자체의
   thermodynamic stability 보다 더 예측력 있음**.
3. ALD MgO 실험 검증 — DFT 예측대로 LiMgO/Li-Mg 형성 + Li metal 안정성 향상 +
   CCD 0.9 mA/cm² 달성.

---

## 2. 그들의 방법론 (2-step screening)

```
Step 1: Thermodynamic Stability (Materials Project DFT 데이터)
  ├─ ΔE for LPSCl||Coating  ← 17 oxides screened
  ├─ ΔE for Li||Coating
  └─ ΔE for Cathode||Coating (LCO, LMO)
  → Heatmap (periodic table)
  → Top 10 candidates with ΔE > -0.5 eV/atom (low driving force)

Step 2: Electronic + Transport Properties (VASP + HSE06)
  ├─ Bandgap (bulk + 1nm slab) — should be > LPSCl (3.92 eV)
  ├─ Li migration barrier in reaction products (CI-NEB)
  └─ DFT-PBE for migration; HSE06 for bandgaps
  → Final ranking: MgO, Al₂O₃, ZrO₂ stable; ZnO, ZrO₂ shows bandgap reduction

Result: 3 selected for ALD synthesis (MgO, ZrO₂, ZnO) + experiment validation
```

**계산 비용**: 모든 단계가 DFT (VASP HSE06). 17 oxide × 3 interface × 2 phase
= ~100+ DFT calculations + NEB. Total cost: 대략 ~1000-10000 CPU-hours.

---

## 3. 핵심 정량 결과 (그들 paper)

### Table 1 — LPSCl||Oxide 안정성 (top 10)
| Oxide | ΔE (eV/atom) | 비고 |
|-------|------------:|------|
| SiO₂ | 0.000 | 가장 stable (no reaction) |
| Al₂O₃ | −0.044 | their previous work |
| ZrO₂ | −0.097 | bandgap 7.16 eV |
| MgO | **−0.125** | bandgap 8.12 eV, **best multifaceted** |
| TiO₂ | −0.126 | |
| Sc₂O₃ | −0.132 | |
| Y₂O₃ | −0.176 | bandgap 6+ eV |
| Nb₂O₅ | −0.200 | |
| MnO | −0.202 | bandgap 2 eV (낮음) |
| Cr₂O₃ | −0.256 | |
| CaO | −0.304 | |
| ZnO | −0.372 | most reactive but multifaceted benefits |

### Table 2 — Li||Oxide 안정성 (top, ZnO=−0.653 cutoff)
| Oxide | ΔE (eV/atom) |
|-------|------------:|
| Y₂O₃ | 0.000 (no reaction) |
| CaO | 0.000 |
| Sc₂O₃ | −0.034 |
| **MgO** | **−0.040** |
| ZrO₂ | −0.185 |
| **Al₂O₃** | **−0.220** |
| TiO₂ | −0.357 |
| SiO₂ | −0.447 |
| MnO | −0.557 |
| Nb₂O₅ | −0.585 |
| Cr₂O₃ | −0.611 |
| ZnO | −0.653 |

### 실험 검증 (XPS + EIS + CCD)
| Coating | 이온 전도도 (vs. uncoated) | 전자 전도도 (vs. uncoated) | CCD |
|---------|---------------------------|----------------------------|-----|
| Al₂O₃ | 1.5× | 0.81× (~20% 감소) | improved |
| MgO | 1.0× (no change) | **0.11× (10× 감소)** | **0.9 mA/cm² ✓** |
| ZnO | **1.2× (20% 증가)** | **0.17× (6× 감소)** | improved |
| ZrO₂ | **0.12 mS/cm (10× 감소)** | 2× 증가 | not best |

---

## 4. 우리 프로젝트와의 비교 (gap analysis)

| 측면 | Sundar 2025 (Argonne) | **본 프로젝트 (BML, 우리)** |
|------|----------------------|---------------------------|
| **Target** | 표면 oxide coating (ALD) | **Bulk doping (cation/anion)** + 표면 |
| **Methodology** | DFT-only (VASP HSE06) | **UMA + DFT + ML surrogate** (3-tier) |
| **Cost per candidate** | ~100-1000 CPU-h DFT | **~10 sec UMA** (1000× faster) |
| **Throughput** | 17 oxides | **10⁴-10⁵ candidates** (Phase 2 목표) |
| **Active learning** | 없음 | **BoTorch + Ax** (Phase 2) |
| **Inverse design** | 없음 | **Generative model** (Phase 3) |
| **Mechanical properties** | 없음 | EOS B₀ (이미 검증) |
| **Adhesion energy W_ad** | 간접 (ΔE만) | **직접 (UMA, R=+0.989 검증)** |
| **Family-internal trend** | 없음 | **comp3>4>5 mechanism (paper-validated)** |
| **Literature DB 자동화** | 없음 | **OpenAlex + S2 + Claude** |
| **Patent status** | Filed (Argonne) | (없음, 우리 차별화 가능) |

---

## 5. 우리가 흡수할 점 (steal smart)

### 5.1 Methodology 흡수
1. **3-interface analysis**: Electrolyte||Coating, Anode||Coating, Cathode||Coating
   → 우리도 모든 후보를 3 interface에 대해 평가
2. **Reaction enthalpy ΔE** as Tier-0 filter
   → Materials Project DFT 데이터 활용 (no compute cost)
3. **Bandgap criterion**: bulk + thin film 둘 다 보기
   → ZnO 사례처럼 bulk vs slab bandgap 다른 case 주의
4. **Reaction product Li migration barrier** as critical descriptor
   → 우리 descriptor catalog Tier-2에 추가
5. **CI-NEB for Li migration** workflow
   → atomate2의 NEB module 활용 (이미 지원)

### 5.2 핵심 인사이트 흡수
- "Reaction product properties > Coating thermodynamic stability"
  → 우리 Tier-1 descriptor 우선순위에 반영. 단순 ΔE 만 보지 말고 product의
    bandgap + Li conductivity 같이 봐야 함.
- "MgO is best multifaceted candidate" — Pareto multi-objective 검증 사례
  → 우리 active learning multi-objective 함수 정의 시 reference

### 5.3 Reference 라이브러리 추가
이 paper의 reference 78개 → 우리 literature DB의 priority 키워드 확장:
- `argyrodite oxide coating ALD`
- `LPSCl Al2O3 MgO ZnO ZrO2`
- `solid electrolyte cathode coating thermodynamic stability`
- `Li migration barrier reaction product`

---

## 6. 우리 차별화 포인트 (defensible vs Sundar 2025)

### 6.1 Speed + Scale
- 그들: 17 oxides DFT screening = 수개월
- 우리: **UMA 10초/후보 → 10,000 후보 1주일**
- 차이: **1000× 빠름**

### 6.2 Methodology 진화
- 그들: 2-step DFT (Tier 1 ΔE + Tier 2 bandgap/NEB)
- 우리: **3-tier UMA → ML surrogate → active learning**
- 차이: 정량적 + dynamic (그들은 static screening)

### 6.3 Bulk doping 영역 확장
- 그들: 표면 oxide coating only (~30개 후보)
- 우리: **bulk cation/anion 도핑** (29 dopants × 5 sites × 5 concentrations
  = 725 base combinations) + 표면도 가능
- 차이: chemical space 25× 넓음

### 6.4 우리 paper validation 활용
- 그들: paper Wad ↔ DFT ΔE 직접 비교 없음
- 우리: **paper Wad R=+0.989 검증된 UMA pipeline** 보유
- 차이: 신뢰도 정량 수치로 입증 가능

### 6.5 Multi-mechanism descriptor
- 그들: ΔE + bandgap + NEB = 3 descriptor
- 우리: **Cl-O density (R=+0.975) + S-O density (R=−0.973) +
  vacancy-mediated W_ad + bulk Cl trend (R=+0.97)** + 모든 Tier-1~3
  (60+ descriptor catalog)
- 차이: 메커니즘 분해 능력 우월

---

## 7. Action items 업데이트 (Sundar paper 반영)

### Phase 1 즉시 추가 (~1주)
- [ ] **3-interface ΔE 계산 모듈 추가**:
  `scripts/descriptors/compute_interface_dE.py`
  - LPSCl||Coating, Li||Coating, Cathode||Coating
  - Materials Project API로 reaction enthalpy 자동 계산
- [ ] **Bandgap descriptor 추가** (Tier-3 → Tier-2 승격):
  `scripts/descriptors/compute_bandgap.py` (HSE06 또는 PBE+U)
- [ ] **NEB Li migration barrier**:
  `scripts/descriptors/compute_neb_barrier.py` (atomate2 wrapping)

### Phase 2 (~3개월)
- [ ] Sundar의 17 oxide를 우리 pipeline으로 재계산 → **validation**
  (그들 결과 재현하면 신뢰도 증명)
- [ ] MgO를 reference로 우리 ML surrogate 검증
- [ ] Reaction product properties 자동 추출 + 평가

### Phase 3 (~6개월)
- [ ] 표면 coating + bulk doping **combined screening** (그들 못 한 영역)
- [ ] Active learning으로 Sundar 17 oxide 외 신규 chemistry 발굴
- [ ] 실험 partner와 top-3 신규 후보 합성

---

## 8. Paper에서 가져올 직접 자료

### Reference 라이브러리에 추가 (우선)
- [13] **Hood et al.** — Al₂O₃/LPSCl ALD original (그들 prior work, Argonne)
- [32-37] LLZO + NCM oxide coating screening papers
- [38-41] coating descriptors (Li migration, bandgap, interfacial barriers)
- [42] LPSCl Al₂O₃ ALD oxidizing atmosphere
- [44] ZnO bandgap experimental (3.40 eV)

### 그들의 Top oxide list 자체를 출발점으로
**MgO, Al₂O₃, ZrO₂, ZnO, SiO₂, TiO₂, Sc₂O₃, Y₂O₃, Nb₂O₅** — 우리 doping
screening의 anion site 비교 reference로.

### Materials Project Selenium WebDriver 방식
그들이 사용한 reaction enthalpy 자동 추출 — 우리도 같은 방식 + atomate2
통합 가능.

---

## 9. 결론

**Sundar 2025는 우리 프로젝트의 직접 경쟁자 (sibling work)**, 하지만:
- 그들이 못 한 것 = 우리가 할 것:
  1. UMA-accelerated screening (1000× faster)
  2. Bulk doping space (25× wider)
  3. ML surrogate + active learning (dynamic, not static)
  4. Mechanical descriptor 통합
  5. Direct Wad validation (R=+0.989)
- **우리 역할**: Sundar 결과를 reproduce하면서 (validation) + 그들 못 다룬
  영역 (bulk doping + ML)을 새로 개척.
- **Patent 회피**: 그들 patent는 oxide coating chemistry. 우리 bulk doping +
  ML platform은 별도 IP space.

**Strategic positioning**: "Sundar et al. demonstrated DFT-based screening for
LPSCl coatings. We extend this to a comprehensive UMA-ML digital twin
platform that screens 1000× more candidates and discovers novel bulk doping
chemistries beyond their oxide library."

---

## 10. 다음 단계

1. **Phase 1 sub-task**: Sundar의 Top-3 oxide (MgO, Al₂O₃, ZnO) UMA로 재계산
   → 그들 DFT 결과와 비교 → **UMA 신뢰도 cross-validation** (우리 paper 외에
   추가 검증 케이스 확보)
2. **Mechanism MD에 Sundar 인용 추가** — Section 12 references 확장
3. **Literature DB priority keyword 확장** (위 5.3)

다음 세션에서 이 cross-validation 스크립트 작성 + Sundar 결과 재현부터
시작하면 강력한 baseline 확보.
