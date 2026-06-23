# Impact of the Chlorination of Lithium Argyrodites on the Electrolyte/Cathode Interface — Zuo et al. (Angew. Chem. Int. Ed. 2022/2023)

> slug `zuo2022_chlorination_cathode_interface` · DOI `10.1002/anie.202213228` · type `exp` (DFT 보조) · PDF `d0102fe3-Angew…Zuo….pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
Cl-rich(Li₅.₅PS₄.₅Cl₁.₅)는 Li₆PS₅Cl보다 **더 쉽게 분해**되지만(CV 2×, 낮은 onset, DSC/TGA 덜 안정), 분해 **산물이 더 양호**(산화 고체 sulfate/phosphate↓, 기체 SO₂·폴리설파이드↑) → **계면 저항 증가 느림 → 셀 성능 더 좋음**. "산화안정성(분해 양) ≠ 배터리 성능"의 결정적 사례.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| Zuo, Walther, Teo, Rueß, Wang, Rohnke, Schröder, Nazar, Janek | Angew. Chem. Int. Ed. 62, e202213228 (2022/2023) | 10.1002/anie.202213228 | Li₆PS₅Cl, Li₅.₅PS₄.₅Cl₁.₅ | exp + DFT 보조 |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| 이온전도도 σ | 2.9 → **7.0 mS/cm** | RT, Cl 1.0→1.5 | Cl-rich↑ |
| 산화 onset (CV) | Cl-rich가 더 낮음(apparent) | SE/C, 0.05 mV/s | peak 위치는 **동일** |
| CV 전류 | Cl-rich **~2×** | 동일 scan | ≈ σ 비(2.4×) → 접근성 효과 |
| R_cat 증가율 | 13.2 → **8.9 Ω·h⁻⁰·⁵** | NCM85, 3.7 V | Cl-rich 계면 열화 **느림** |
| 셀 용량(50cyc) | 133 → **145 mAh/g** | NCM85, 0.5C | Cl-rich↑ (CE 77→79%) |
| 열안정성(DSC) | 535/532 → 523/493 °C | | Cl-rich 덜 안정 |

## 4. DFT/계산 방법 ★
- 주로 **실험** 논문. DFT는 분해상 해석 보조(decomposition reactions Eq1–3, 단순화).
- Eq1: Li₆PS₅Cl → LiCl + Li₃PS₄ + S + 2Li⁺ + 2e⁻
- Eq2: Li₅.₅PS₄.₅Cl₁.₅ → 1.5 LiCl + Li₃PS₄ + 0.5 S + Li⁺ + e⁻ (전자 **1개** = comp의 절반)
- Eq3(완전산화): Li₃PS₄ → 0.5 P₂S₅ + 1.5 S + 3Li⁺ + 3e⁻

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a,b | CV (SE/C), Cl-rich 2× 전류·같은 peak | 산화 "양"의 직접 증거. peak 동일 = 우리 onset 동일과 정합 |
| 1c,d | ToF-SIMS S⁻/Cl⁻ (3.7 V 60 h) | 분해 정도 정량 |
| 2a–d | 임피던스 + TLM, R_cat √t 기울기 | 계면 열화 속도 비교(8.9<13.2) |
| 3a–e | 사이클·rate 성능 | Cl-rich 성능 우위 |
| 4,5 | ToF-SIMS PO₃⁻/SO₃⁻(고체 산화물) vs Sₓ⁻(폴리설파이드) | **Cl-rich = 산화 고체↓, 폴리설파이드↑** (핵심 반전) |
| 6 | DEMS O₂(=NCM 격자)·SO₂ | O₂ 동일, Cl-rich SO₂↑ = 기체 diversion |
| 7 | 메커니즘 (저전압 분해 / 고전압 O-degradation ≥4.2 V) | 산화 단계 도식 |

## 6. Post-processing ★
- **CV** (SE/carbon 복합전극, 0.05 mV/s) → 분해 onset·전류로 산화 취약성 정량
- **EIS + transmission line model (TLM)**: R_cat = √(R_ct(R_el+R_ion)), √t 기울기로 계면 열화율
- **ToF-SIMS** depth profile: 분해 산물 화학종(S⁻/Cl⁻/PO₃⁻/SO₃⁻/Sₓ⁻) 분류
- **DEMS** gassing: O₂(m/z32)·SO₂(m/z64) 정량
- **DSC/TGA**: 열역학적 (불)안정성

## 7. 우리 DFT 대비 (comp1 / modelc)
| 항목 | Zuo | 우리 | 차이 / 이유 |
|---|---|---|---|
| 분해 stoichiometry | Eq1 2e⁻+1.0 LiCl / Eq2 1e⁻+1.5 LiCl | comp1 1.75Li+1.0LiCl / modelc 0.7Li+1.6LiCl | **강한 일치** (우리 ESW가 독립 재현) |
| 산화 onset | "same peak potentials" | 2.14 V 동일 | **일치** (Zuo "낮은 onset"은 2× 전류의 apparent) |
| Cl-rich 반응성(CV 2×) | 더 반응 | interface dE +2.5%(≈noise) | 2× = **전도도(2.4×) 접근성**, intrinsic 아님 |
| 셀 우수(R_cat↓) | gas diversion → 얇은 CEI | **못 봄** (closed solid-hull, 기체상 X) | 우리 한계 → 실험 인용 |
| metastability(DSC/TGA) | Cl-rich 덜 안정 | composition-기반 → ranking 불가 | 범위 밖 (E_above_hull 필요) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **deck 프레이밍**: "Cl-rich = intrinsic 분해는 더 많지만 산물이 좋아 계면·성능 유리" — Zuo가 실험 근거.
- ② **우리 ESW의 강점 부각**: grand-potential이 Zuo Eq1/Eq2 분해 화학을 독립 재현 → 검증된 계산.
- ③ **2× 전류는 전도도로 해석**(intrinsic 반응성 아님) — interface dE +2.5%는 noise라 인용 자제.
- ④ **우리가 못 보는 것 명시**: 기체 diversion·metastability는 실험 영역(정직성).

## 9. 인용 가능 문장 (deck/paper용)
- "Our grand-potential decomposition reactions reproduce Zuo's experimentally-inferred Eq1/Eq2 (fewer e⁻/Li and more inert LiCl for the Cl-rich phase), cross-validating the calculation."
- "The ~2× CV current of the Cl-rich electrolyte tracks its ~2.4× higher ionic conductivity, i.e. accessibility rather than intrinsic reactivity."

## 10. 주의/한계
- Zuo Cl-rich = Cl1.5; 우리 modelc = Cl1.6 (근사).
- "낮은 onset"은 Fig S2의 soft claim(apparent) — thermodynamic onset은 동일(같은 peak).
