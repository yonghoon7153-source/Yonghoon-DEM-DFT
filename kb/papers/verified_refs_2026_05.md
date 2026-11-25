# Verified Literature References — Paper #1 (2026-05-05)

> [!info] Status
> All paper titles verified by user via direct paper access / CrossRef API. ==**Paper-ready citation list**==. LLM-paraphrased entries cleaned + replaced.

---

## ✅ 8 Verified References

### 1. **kraft2018** (J. Am. Chem. Soc.)
> Kraft, M. A. et al. **Influence of Lattice Polarizability on the Ionic Conductivity in the Lithium Superionic Argyrodites Li₆PS₅X (X = Cl, Br, I)**.
> *J. Am. Chem. Soc.* **140**, 16330 (2018). DOI: 10.1021/jacs.7b06327
>
> **우리 활용**: q²/r framework + polarizability 분석 (Section 2)

### 2. **adeli2019** (Angew. Chem. Int. Ed.)
> Adeli, P. et al. **Boosting Solid-State Diffusivity and Conductivity in Lithium Superionic Argyrodites by Halide Substitution**.
> *Angew. Chem. Int. Ed.* **58**, 8681 (2019).
>
> **우리 활용**: Li(6-x)PS(5-x)Cl(1+x) framework — at x=0.6 = ==**우리 modelC 정확 동일**== (Section 3)

### 3. **yuwagemaker2023** (ACS)
> Yu, Wagemaker, et al. **From anionic disorder to fast ion transport in Br-rich argyrodites**.
> 2023. PMC11823417
>
> **우리 활용**: 4d-Li cage interaction 약화 mechanism (Section 2)

### 4. **wagemaker2020** (Chem. Mater.) — *DOI 4c02010 = 실제 2024년*
> Wagemaker group. **Decoding Structural Disorder, Synthesis Methods, and Short- and Long-Range Lithium-Ion Transport in Lithium Argyrodites (Li₆₋ₓPS₅₋ₓBr₁₊ₓ)**.
> *Chem. Mater.* (2024). DOI: 10.1021/acs.chemmater.4c02010
> URL: https://pubs.acs.org/doi/10.1021/acs.chemmater.4c02010
>
> **DB id**: `yuwagemaker2024_decoding`
> **우리 활용**: Li₆₋ₓPS₅₋ₓBr₁₊ₓ at x=0.6 = comp5 (Br-dominant), companion Cl-rich = modelC (Section 2-3)

### 5. **zuo2023** (Angew. Chem. Int. Ed.)
> Zuo, T. et al. **Impact of the Chlorination of Lithium Argyrodites on the Electrolyte/Cathode Interface in Solid-State Batteries**.
> *Angew. Chem. Int. Ed.* (2023). DOI: 10.1002/anie.202213228
>
> **우리 활용**: Cl-rich + NCM interface trade-off (conductivity vs decomposition) (Section 4)

### 6. **sicolo2022** (J. Phys. Chem. C)
> Sicolo, S. et al. **Interfacial Stability of Layered LiNiₓMnᵧCo₁₋ₓ₋ᵧO₂ Cathodes with Sulfide Solid Electrolytes in All-Solid-State Rechargeable Lithium-Ion Batteries from First-Principles Calculations**.
> *J. Phys. Chem. C* (2022). DOI: 10.1021/acs.jpcc.2c05336
>
> **우리 활용**: NCM-sulfide DFT 계면 prior art — adhesion v5/v6 method ref (Section 4)

### 7. **wang2019** (J. Power Sources)
> Wang, Yu, Ganapathy, van Eck, van Eijck (Wagemaker group). **A lithium argyrodite Li₆PS₅Cl₀.₅Br₀.₅ electrolyte with improved bulk and interfacial conductivity**.
> *J. Power Sources* (2019). DOI: 10.1016/j.jpowsour.2018.11.029
>
> **DB id**: `wang2019_li6ps5cl0p5br0p5`
> **우리 활용**: ==**Li6PS5Cl0.5Br0.5 = comp2 정확 동일**== — experimental anchor for our comp2 v2 measurements (Section 1, Section 4)

### 8. **gautam2023** (Chem. Mater.)
> Gautam et al. **Exploring the Relationship Between Halide Substitution, Structural Disorder, and Lithium Distribution in Lithium Argyrodites (Li₆₋ₓPS₅₋ₓBr₁₊ₓ)**.
> *Chem. Mater.* (2023). DOI: 10.1021/acs.chemmater.3c01525
>
> **우리 활용**: Cl⁻ at 4d = 60% quantitative ratio — modelC v2 Li-Cl elongation의 정량 backing (Section 2)

---

## 🗑️ Removed (Hallucination)

- ~~`wagemaker2020_lideficient`: "Li-deficient argyrodite review"~~  
  → CrossRef 검색 후 NO matching paper. LLM이 fabricated review article. The 9.4 mS/cm result actually originates from **adeli2019** (Nazar group). Replaced by **wang2019**.

---

## 📊 우리 시스템과 매칭되는 논문 매트릭스

| 우리 composition | Direct experimental match | Computational prior art |
|------------------|---------------------------|-------------------------|
| **comp1** Li6PS5Cl | (deiseroth2006 baseline) | kraft2018 |
| **comp2** Li6PS5Cl0.5Br0.5 | ⭐ **wang2019** (정확 동일) | kraft2018, sicolo2022 |
| **comp3-5** Li5.4PS4.4Cl1-xBr0.6+x | (gautam2023 framework) | kraft2018, adeli2019 |
| **modelC** Li5.4PS4.4Cl1.6 | ⭐ **adeli2019** (Li(6-x)PS(5-x)Cl(1+x) at x=0.6) | gautam2023 (4a/4d), wagemaker2020 |

---

## 📋 7-Narrative Citation Plan

| # | 우리 narrative | 1순위 ref | 2순위 ref |
|---|----------------|-----------|-----------|
| 1 | q²/r framework / charge magnitude | kraft2018 | (zhang2024 if needed) |
| 2 | 4a/4d site distribution | gautam2023 ⭐ | yuwagemaker2023, wagemaker2020 |
| 3 | Li5.4 vacancy framework | adeli2019 ⭐ | (kraft2018 polarizability) |
| 4 | comp4 frustration anomaly | (our data primary) | yuwagemaker2023 (disorder framework) |
| 5 | modelC Li-Cl elongation | gautam2023 ⭐ | yuwagemaker2023 |
| 6 | Wad enhancement (Cl-rich) | zuo2023 | wang2019 (interfacial conductivity) |
| 7 | NCM interface methodology | sicolo2022 | — |
| ★ | comp2 experimental anchor | **wang2019** ⭐ | — |

---

## 🔗 관련 파일

- `db/literature/refs.json` — full ref entries (DOI, key_quote, supports_our_finding 등)
- `kb/results/halogen_wad_refutation.md` — 6-fact author rebuttal
- `kb/papers/narrative_with_literature_steps.md` — paper writing scaffold

---

#paper1 #verified-refs #literature #2026-05-05
