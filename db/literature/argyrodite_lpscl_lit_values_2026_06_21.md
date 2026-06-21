# LPSCl / LPSCl1.6 문헌 물성값 종합 (2026-06-21) — 비배터리 물리·계산 포함

배경조사(웹 5-agent). **우리 DFT/MLIP 값과의 대조 + novelty gap** 정리.

> ⚠️ **신뢰도 주의**: 조사 시 WebFetch(전문 PDF)가 403으로 막혀, 값은 검색 스니펫(초록/그림캡션/SI 색인)에서 추출. 아래 "★검증필요" 표시는 해당 논문 안에 있으나 정확한 수치를 직접 확인 못 한 항목 → 인용 전 원문 fetch 권장. DOI는 확인된 것만 기재.

---

## 0. 가장 중요한 두 가지 (보고용 헤드라인)

1. **x=0.6 (Li5.4PS4.4Cl1.6 = 우리 modelc)는 문헌에서 "이온전도도"만 보고됨** — 탄성/전자/진동/상세구조는 **미보고**. 정식 Cl-rich 기준상(canonical)은 x=0.5 (Li5.5PS4.5Cl1.5, Adeli/Nazar 2019). → **우리 modelc의 DFT/MLIP 물성(E_VRH, Cij, gap, ELF/Bader, σ)은 novel.**
2. **우리 값이 문헌과 정량 일치** (아래 §8 대조표): 특히 relaxed-ion E_VRH comp1 **22.1 GPa = Torii 2025 DFT 22.1** (거의 정확), modelc σ **~14 mS/cm ≈ 실험 x=0.6 11.34**.

---

## 1. 구조 (격자상수·밀도·결합)
| 값 | 물성 | 조성 | 방법 | 출처 |
|---|---|---|---|---|
| **a = 9.859 Å** (F-43m, Z=4) | 격자상수 | LPSCl | 단결정 XRD 296K | Deiseroth *Angew.* 2008, DOI 10.1002/anie.200703900 |
| a = 9.857 Å | 격자상수 | LPSCl | XRD/Rietveld | Hanghofer *PCCP* 2019, 10.1039/C9CP00664H |
| a = 10.31 Å (과대) | 격자상수 | LPSCl | DFT-PBEsol | Solid State Sci. 2023, S0921452623002995 |
| ρ = 1.64 g/cm³ | 밀도 | LPSCl | cell | 다수 |
| P–S 2.06 / Li–S 2.33,2.42 / Li–Cl 2.44,2.67 Å | 결합길이 | LPSCl | DFT-PBE | Materials Project mp-985592 |
| Cl-rich → 격자 수축(Cl⁻<S²⁻) | 격자 | Li5.5PS4.5Cl1.5 | 중성자 | Adeli/Nazar *Angew.* 2019 |

## 2. S²⁻/Cl⁻ anti-site disorder (argyrodite 핵심)
| 값 | 조성 | 방법 | 출처 |
|---|---|---|---|
| **Cl⁻ 38.5%@4a / 61.5%@4d** | LPSCl | XRD/Rietveld | Hanghofer 2019 |
| Cl⁻ 39%@4a / 62%@4d | LPSCl | 중성자+MEM | Gautam *ChemComm* 2021, 10.1039/D1CC03083C |
| **~40–50% disorder가 Li 연결성 최대** | LPSCl | uMLIP-MD | arXiv:2502.09970 |
| σ 최적 disorder window 37.5–50% | LPSCl | NNP-MD | Lee/Han *Chem.Mater.* 2025, 10.1021/acs.chemmater.4c01152 |
| 이온반지름 S²⁻=1.84, Cl⁻=1.81 Å (유사→혼합) | — | — | Kraft 2017 |

→ 우리 BVSE/AIMD의 anti-site Cl 효과와 직접 연결. (우리 modelc는 Cl 1.6/fu, 4a+4c 점유.)

## 3. 탄성/역학 (별개 연구 3개 — 섞지 말 것)
| 값 | 조성 | 방법 | 출처 |
|---|---|---|---|
| **B/G/E = 34.7/10.0/27.4 GPa, ν=0.37** | LPSCl | DFT-PBE VRH | Deng/Ong *JES* 2016, 10.1149/2.0061602jes |
| **B/G/E = 28.7/8.1/22.1 GPa, B/G=3.46(연성)** | LPSCl | DFT 응력-변형 | **Torii** *JPCC* 2025, 10.1021/acs.jpcc.5c05116 |
| **E = 28.0 ± 1.8 GPa (dense)** | LPSCl | **실험** | Torii 2025 내 보고 |
| E = 4.7±1.1 GPa (porous), K_IC 0.17 MPa·m^0.5 | LPSCl | 실험+FEM | *ACS AEM* 10.1021/acsaem.4c03143 |
| c11/c12/c44, 경도, 음속, Debye T ★검증필요 | LPSCl | DFT/실험 | Torii 2025 / Kraft *JACS* 2017 10.1021/jacs.7b06327 |
| x=0.6 탄성텐서 **없음**; off-stoich Li가 modulus↓ | x=0.6 | — | Mohayman *ACS AEM* 2025, 10.1021/acsaenm.5c00184 |

## 4. 전자/광학
| 값 | 조성 | 방법 | 출처 |
|---|---|---|---|
| Eg = 2.15–2.45 eV (PBE) | LPSCl | DFT-GGA/PBE | Stamminger *Chem.Mater.* 2019, 10.1021/acs.chemmater.9b02047 |
| Eg = 3.11 eV (mBJ) / 3.30 (HSE06) | LPSCl | DFT hybrid | SSSci 2023 / Stamminger |
| VBM = S 3p, direct gap @Γ | LPSCl | pDOS/COHP | 다수, RSC Adv 2022 10.1039/d2ra05900b |
| σ_electronic ≈ 10⁻⁹ S/cm | LPSCl | DC 분극 | "Devil in Defects" *Chem.Mater.* 2021 10.1021/acs.chemmater.1c02345 |
| ESW ~1.7–2.3 V (좁음) | LPSCl | DFT grand-potential | Zhu/He/Mo *ACS AMI* 2015; Richards/Ceder 2016 |
| ε0/ε∞, n(0) ★검증필요 | LPSCl | DFT | RSC Adv 2022 10.1039/d2ra05900b |

## 5. 진동(Raman/IR)·포논
| 값 | 조성 | 방법 | 출처 |
|---|---|---|---|
| **ν1 = 425 cm⁻¹** (PS4³⁻ 대칭신축, 시그니처) | LPSCl | Raman(실험) | 다수(Zeier/Wilkening) |
| 199, 272 cm⁻¹ (ν2/ν4 굽힘) | LPSCl | Raman | 다수 |
| 573, 600 cm⁻¹ (ν3 비대칭신축) | LPSCl | Raman | 다수 |
| ordered 구조 imaginary/soft 포논(0K 동적 불안정) | LPSCl | DFT/DFPT | arXiv:2407.04126; PCCP 2022 |
| **VDOS가 ω² Debye에서 크게 벗어남(액체형 crossover)** | LPSCl | 중성자+ML-MD | **Nat. Phys. 2025** "Liquid-like dynamics", 10.1038/s41567-024-02707-6 |

→ **Nat. Phys. 2025가 우리 MLIP-MD 진동/확산 검증의 최적 benchmark** (quasi-harmonic 붕괴 = 우리도 같은 이유로 AIMD-MLIP 씀).

## 6. 열역학
| 값 | 조성 | 방법 | 출처 |
|---|---|---|---|
| **E_hull = 21 meV/atom (metastable)** | LPSCl | DFT 0K | Deng/Ong *Chem.Mater.* 2017, 10.1021/acs.chemmater.6b02648 |
| 분해 → Li2S + Li3PS4 + LiCl | LPSCl | DFT | *JMCA* 2024, 10.1039/d4ta05159a |
| cubic 안정 > ~613.9 K(계산) / 결정화 ~330°C(DSC) | LPSCl | DFT+Cp / 실험 | *JMCA* 2024 / 다수 |
| Cp 최초 계산(기존 값 부재) | LPSCl | DFT-AIMD | *JMCA* 2024 |

## 7. 이온전도 (LPSCl vs Cl-rich vs **우리 x=0.6**)
| σ(RT) | 조성 | 제법 | 출처 |
|---|---|---|---|
| ~2.5 mS/cm | LPSCl | cold-press | Adeli/Nazar 2019 |
| 9.4 / 12.0 mS/cm | Li5.5PS4.5Cl1.5 | cold-press / sintered | **Adeli/Nazar** *Angew.* 2019, 10.1002/anie.201814222 |
| **11.34 mS/cm** | **Li5.4PS4.4Cl1.6 (x=0.6=modelc)** | sintered 480°C | DRT, *J. Power Sources* 2023, **583, 233579** |
| 6.18 mS/cm | Li5.4PS4.4Cl1.6 | wet-mill | RG 354794236 |
| Ea: LPSCl 0.33–0.38 / Li5.5Cl1.5 0.29 eV | — | EIS | Kraft 2017 / Adeli 2019 |
| D=1.0×10⁻⁷ cm²/s(298K) | Li5.5PS4.5Cl1.5 | NMR | Adeli 2019 |
| MLIP σ≈30 mS/cm(50%disorder), Ea 0.20–0.26 | LPSCl | NNP/MTP-MD | Lee/Han 2025; arXiv:2407.04126 |

---

## 8. ★ 우리 값 vs 문헌 대조 (검증)
| 물성 | 우리 값 | 문헌 | 평가 |
|---|---|---|---|
| **E_VRH (relaxed-ion) comp1** | **22.06 GPa** | Torii DFT **22.1**; 실험 28.0±1.8 | ★거의 정확 일치(DFT), 실험보다 낮음(이상적 단결정/포로시티 차이) |
| EOS B0 comp1 | 26.2 GPa | Torii B 28.7 / Deng 34.7 | 범위 내, 낮은 쪽 |
| band gap comp1 (PBE) | 2.25–2.28 eV | PBE 2.15–2.45 | ✓ 일치 |
| Li–S / Li–Cl comp1 | 2.46 / 2.49–2.61 | 2.33,2.42 / 2.44,2.67 | 같은 범위 |
| Ea comp1 (4fu MLIP) | 0.253 eV | 실험 0.33–0.38; MLIP 0.20–0.26 | MLIP끼리 일치, 실험보다 낮음(MLIP 경향) |
| **σ300 modelc** | **~14 mS/cm** | **실험 x=0.6 = 11.34** | ★우수 일치(MLIP 과대 ~1.2배뿐) |
| disorder→σ | 우리 anti-site Cl 효과 | 37.5–50% 최적 (Lee/Han) | ✓ 정성 일치 |

## 9. novelty gap (우리 연구 강점)
- **x=0.6 (modelc)**: 탄성 Cij/E_VRH, band gap, ELF/Bader, 진동, 상세 site disorder = **문헌 미보고** → 우리 DFT/MLIP가 최초 제공.
- Nd2O3 공도핑(우리 nd): 문헌 직접값 없음 (La+O 유사 Electrochim. Acta 2025만).

## 10. 원문 fetch 우선순위 (WebFetch 복구 시)
1. **Torii *JPCC* 2025, 10.1021/acs.jpcc.5c05116** → c11/c12/c44 전체 텐서, 경도, 음속, Debye T (우리 Cij 직접 비교용)
2. Kraft/Zeier *JACS* 2017, 10.1021/jacs.7b06327 → 실험 음속·Debye T·lattice polarizability
3. RSC Adv 2022, 10.1039/d2ra05900b → ε0/ε∞, n(0) (우리 polarizability 논의용)
4. Nat. Phys. 2025, 10.1038/s41567-024-02707-6 → 중성자+ML-MD VDOS (MLIP 검증)
5. Adeli/Nazar *Angew.* 2019, 10.1002/anie.201814222 → Cl-rich 격자·점유 SI
