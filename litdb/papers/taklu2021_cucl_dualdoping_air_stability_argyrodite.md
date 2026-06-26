# Dual CuCl doped argyrodite superconductor to boost interfacial compatibility and air stability for all-solid-state Li metal batteries — Taklu et al. (Nano Energy 2021)

> slug `taklu2021_cucl_dualdoping_air_stability_argyrodite` · DOI `10.1016/j.nanoen.2021.106542` · type `exp (+ DFT 보조: VASP/PAW Li migration path)` · PDF `82ea256b-cd968a22-20._Dual_C…teries.pdf` · digested `2026-06-26` · status ✅
> **저자**: **Bereket Woldegbreal Taklu**, **Wei-Nien Su**(교신), Yosef Nikodimos, Keseven Lakshmanan, Nigusu Tiruneh Temesgen, Pei-Xuan Lin, Shi-Kai Jiang, Chen-Jui Huang, Di-Yan Wang, Hwo-Shuenn Sheu, **She-Huang Wu**(교신), **Bing Joe Hwang**(교신) · Nano Energy **90** (2021) 106542
> **소속**: **National Taiwan University of Science and Technology (NTUST)** Nano-electrochemistry Lab + Dept. Chem. Eng. + Tunghai Univ. + **NSRRC**(싱크로트론) · **외부 그룹 (≠ 우리 한양/Jong-Won Lee/Y.M.Lee/Cho/Cha/Kang)**

---

## 0. 이 digest를 읽는 법 (그리고 stray-파일 / 중복 검증 결과)

**검증 통과 — 신규 논문, 중복 아님.** 파일명 "20._Dual_C…teries"는 잘렸지만 **표지(p.1) 확인 결과 = "Dual CuCl doped argyrodite … air stability … batteries"** — 정확히 argyrodite 황화물 SE 논문. li2025(CuBr₂)·cha2024(dual-compatible halide)·sundar2025(coating) 중 어느 것의 재업로드도 아님 (아래 **중복-구분표** 참조).

> ### ⚠⚠ li2025와의 관계 — **자매(sibling)지만 별개 논문** (force-fit / 중복 처리 금지)
> | 항목 | **이 논문 (Taklu 2021)** | **li2025 (Li et al. ESM 2025)** |
> |---|---|---|
> | 도펀트 | **CuCl** (Cu + Cl) | **CuBr₂** (Cu + Br) |
> | 모체 | **Li₆PS₅Cl** (stoichiometric, x=0) | **Li₅.₅PS₄.₅Cl₁.₅** (Cl-rich, x=0) |
> | 일반식 | **Li₆₊₃ₓP₁₋ₓCuₓS₅₋ₓCl₁₊ₓ** (0≤x≤0.5) | Li₅.₅₊₃ₓP₁₋ₓCuₓS₄.₅Cl₁.₅₋₂ₓBr₂ₓ |
> | 최적 | **x=0.1 = Li₆.₃P₀.₉Cu₀.₁S₄.₉Cl₁.₁ (LPSC-1)** | x=0.1 = Li₅.₈P₀.₉Cu₀.₁S₄.₅Cl₁.₃Br₀.₂ (LPSC-CB) |
> | σ (RT) | **4.34 mS/cm** | 10.3 mS/cm |
> | 그룹/년 | **NTUST(대만)·Hwang / 2021** | USTB·Tsinghua / 2025 |
> | DFT 디테일 | **VASP + PAW 명시** (Li 이동거리 계산) | **functional 미명시**(n/a) |
> | 대기안정 기전 | **Cu₃PS₄ 형성** + soft-acid Cu (HSAB) | Cu–S>P–S (물 흡착 ΔE), HSAB |
> | 양극 | (full cell 없음 — 대칭셀·CV 중심) | LCO + FeS₂ full cell |
>
> **=> Taklu 2021 = li2025의 *4년 앞선 예고편*.** 둘 다 "Cu 양이온을 P자리(4b)에 + 할라이드 음이온으로 *이원* 도핑 → σ + Li 금속 호환 + 대기안정 동시 개선" 이라는 **같은 전략 패밀리**. 단 변수(Cl vs Br)·모체(stoich vs Cl-rich)·DFT 깊이·full-cell 유무가 달라 **별개 entry로 보관 가치**. li2025는 본 논문(ref52 Wang Li₄Cu₈GeS₆ + Cu 도핑 일반)을 통해 "Cu 도핑이 σ↑+대기안정"을 이미 알고 출발 — Taklu가 그 **argyrodite-CuCl 원조 중 하나**.

이 논문이 푸는 질문: **"naturally abundant·저가 CuCl 하나를 argyrodite에 *이원*(Cu 양이온 + Cl 음이온) 도핑하면, (1) 이온전도, (2) Li 금속과의 계면 호환성/dendrite 억제, (3) 대기(H₂S) 안정성을 *동시에* 끌어올릴 수 있는가?"** 핵심 통찰 3개:
- **(a) σ↑**: Cu²⁺가 P⁵⁺ 자리(4b)를 일부 치환 → 전하중성 위해 **Li⁺ 추가**(carrier↑) + **Cl⁻ 추가가 4a/4c S²⁻ 자리 무질서↑** + Cu–P EN 차가 작아 **Li₆S cage 안 두 48h Li 거리 단축**(3.298→2.997 Å) → intra-cage doublet jump 쉬워짐 → **σ 1.11→4.34 mS/cm**(x=0.1).
- **(b) Li 금속 계면 안정·dendrite 억제**: Cu가 P자리서 **(P/Cu)S₄ 강공유결합**을 만들어 PS₄ tetrahedra rigid화 → 분해 억제 + **전자전도 σ_e 최저(1.49×10⁻⁹ S/cm)** → CCD **0.75→3.0 mA/cm²**(4배↑), 대칭셀 2400 h/400 h/200 h(전류별) 안정, **8 V까지 ultra-wide ESW**(CV 분해전류 *160배* 감소).
- **(c) 대기안정**: soft acid Cu(I)가 **Cu₃PS₄**(또는 (P/Cu)S₄ 강 Cu–S)를 형성 → thio-phosphate의 **oxophilicity↓**(물·O 친화도↓) → **H₂S 발생 절반**(1.07→0.49 cm³/g, 즉 ~2배 억제).

> ⚠ **전압 기준 혼용 — 본 논문 *2종 동시 사용***: planar/composite CV 일부는 **In/InLi 기준**(Fig 3a,b,e), Li 금속 셀 CV·대칭셀은 **Li/Li⁺ 기준**(Fig 3c,d,f). "8 V stability"는 **In/InLi 기준**(Fig 3b, C-LPSC-1\|LPSC-1\|In) — Li/Li⁺로는 **≈8.6 V**가 아니라 그대로 **8 V vs In/InLi**로 인용해야 함(0~8 V 스캔). **인용 시 기준 반드시 병기.**
> ⚠ **명명**: **LPSC-P** = Li₆PS₅Cl (도핑 안 한 모체, x=0) / **LPSC-1** (= LPCS-1, 오타 혼재) = **Li₆.₃P₀.₉Cu₀.₁S₄.₉Cl₁.₁** (최적 도핑, x=0.1) / **LPS** = Li₃PS₄ (대기안정 비교용 reference).

## 1. 한 줄 요약
Li₆PS₅Cl에 **CuCl을 이원 도핑**(Cu²⁺→P⁵⁺ 4b자리 → Li⁺ 추가 + 48h-Li 거리 단축; Cl⁻ 추가 → 4a/4c S²⁻ 무질서↑)하면 **σ=4.34 mS/cm(RT, x=0.1)·Ea 0.30→0.25 eV** 가 되고, Cu가 만드는 **(P/Cu)S₄ 강공유결합**이 ⓐ 전자전도 σ_e 최저(1.49×10⁻⁹ S/cm)→ Li 금속과 **CCD 0.75→3.0 mA/cm²·8 V(vs In/InLi) ultra-wide ESW·대칭셀 2400 h** 의 dendrite 억제와 ⓑ **Cu₃PS₄ 형성으로 oxophilicity↓→H₂S 발생 절반(1.07→0.49 cm³/g)** 의 대기안정을 *동시에* 제공한다 (ball-mill-free 고상합성, ex-situ XPS·AC 임피던스·싱크로트론 XRD로 검증).

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교 | **LPSC-P (Li₆PS₅Cl, x=0)** vs **LPSC-1 (Li₆.₃P₀.₉Cu₀.₁S₄.₉Cl₁.₁, x=0.1)** + 중간 조성 (x=0.1/0.2/0.3/0.4/0.5) |
| 일반식 | **Li₆₊₃ₓP₁₋ₓCuₓS₅₋ₓCl₁₊ₓ** (CuCl이 P·S 일부 치환, Cu→4b·Cl→4a/4c) |
| 양극 | **full cell 없음** — 초점은 SE 자체(σ)·Li 금속 계면(대칭셀·CV)·대기안정(H₂S). composite는 SE+카본(C65) 70:30 |
| 질문 | 저가·풍부한 **CuCl 단일 전구체**로 Cu(양이온)+Cl(음이온) *이원* 도핑 시 σ·Li호환·대기안정 *동시* 개선되는가 |
| 동기/전략 | (1) **σ**: Zeier류 "charge carrier + anion site-disorder"(EN 차 작은 Cu–S로 lattice 팽창+무질서); (2) **계면**: Li 금속 비호환(Li₂S/LiX/Li₃P 분해층·σ_e↑→dendrite) 극복; (3) **대기**: HSAB — **soft acid Cu**가 soft base S²⁻와 강결합 → P–S 가수분해 억제(Hayashi/Ohtomo MₓOᵧ 첨가 H₂S 억제 선행과 같은 결, 단 여기선 격자 도핑) |
| 선행 | Cu in LGPS(Zhang ref23/Wang Li₄Cu₈GeS₆ ref52), Sn-치환 Li₄SnS₄(Kwak ref6), ZnO(ref24), MₓOᵧ H₂S 억제(Hayashi/Ohtomo ref33/34), Sb/Si 도핑 peak split(ref19–21), HSAB(Pearson ref64) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSC-P (x=0) | **LPSC-1 (x=0.1)** | 출처/조건 |
|---|---|---|---|
| **σ (RT)** | **1.11 mS/cm** | **4.34 mS/cm** (≈3.9×) | abstract·Fig 2 (cold-pressed pellet, 360 MPa) |
| **Ea** | **~0.30 eV** | **0.25 eV** (최저) | Fig 2b,c (Arrhenius, 303–333 K) |
| **σ_e (전자전도)** | 0.6 mA/cm² CCD에 대응 高 σ_e | **1.49×10⁻⁹ S/cm** (최저) | Fig 4b,c (DC polarization, 1 V SUS\|SE\|SUS) |
| **CCD (대칭 Li)** | **0.75 mA/cm²** | **3.0 mA/cm²** (4×) | Fig 5a,b (step galvanostatic, 50 °C) |
| **ESW (CV)** | 0.4 V·>5 V서 분해전류(Li 금속) | **8 V까지 무분해**(vs In/InLi) | Fig 3b (C-LPSC-1\|LPSC-1\|In) |
| **CV faradic 전류** | 1× (sulfur 산화 S²⁻→S⁰/Sₓ, P³⁺→P⁵⁺ ~0.62 V) | **~160× 작음** | Fig 3c,d (2nd cycle 비교) |
| **H₂S 발생 (55–60 % RH, 24 min)** | **1.07 cm³/g** | **0.49 cm³/g** (≈절반) | Fig 8a (vs LPS=Li₃PS₄ **~1.8 cm³/g** 최악) |
| **밴드갭** | **n/a** (계산·측정 안 함) | **n/a** | — (이 논문은 gap 미보고) |
| **기계 E/B/G·C_ij** | **n/a** | **n/a** | — (탄성계수 미계산) |
| **산화 onset (grand-potential)** | **n/a** | **n/a** | — (CV onset만, 정량 phase-stability 안 함) |

### 합성 최적화 (σ vs 소결조건·도핑량) — Fig 2a
- **소결온도** (x=0.1, 15 h): 350 °C **1.11** / 400 **1.63** / 450 **2.82** / 500 **3.49** / **550 °C 4.18** (peak) / 600 °C **0.52** (불순물상·황 석출로 급락). → **최적 550 °C.**
- **소결시간** (x=0.1, 550 °C): 1 h **2.48** / 5 h **2.96** / 10 h **3.41** / **15 h 4.23** (peak) / 20 h **2.68** mS/cm. → **최적 15 h.**
- **도핑량** (550 °C, 15 h): x=0.1서 **4.34 mS/cm·Ea 0.25 eV 최적**; x↑(0.2→0.5)서 σ↓·Ea↑(0.5서 0.36 eV) — **Cu⁺ 용해한계**(이온반경 0.77 Å, CN6) + Li₂S·LiCl 2차상 석출. **화산형(volcano).**

### 결정구조 / 자리 귀속 (Rietveld + Raman + XPS)
| 항목 | 값 | 비고 |
|---|---|---|
| 공간군 | **F-43m** (cubic argyrodite, ICSD #259205 referenced) | 전 조성 동일 구조 (Fig 1a) |
| **Cu 자리** | **4b** (P자리 공유) — Rietveld | Cu²⁺/P⁵⁺ 헤테로치환, "framework former" (Fig 2d 모식도) |
| **Cl 자리** | **4a + 4c** (S²⁻ 자리) — Rietveld | 음이온 site-disorder↑ |
| **Li 자리 / 추가 Li** | 48h (mobile); 전하중성 위한 **추가 Li⁺는 24g 자리** | 24g가 인접 Li₆S cage 간 **doublet jump의 bridge**(48h–24g–48h intercage) |
| **48h–48h Li 거리 (cage 내)** | **3.298 (LPSC-P) → 2.997 Å (LPSC-1)** | **단축 → intra-cage doublet jump 쉬움·Ea↓** (Fig 2d, DFT) |
| **48h–48h Li 거리 (cage 간)** | **3.970 → 4.189 Å** | 격자팽창으로 *증가*(intercage 약간 불리)하나 24g bridge가 보상 |
| 격자상수 a | x↑ 시 팽창 (피크 저각 이동) | Cu⁺(0.77 Å)·Cl⁻ 큰 이온 + Cu–S(EN 차 작음) (Fig 1a) |
| 2차상 (x>0.1) | **Li₂S, LiCl** (피크 split·신규 peak) | Cu가 4b서 P 치환 → P 부족분이 Li₂S/LiCl로 (Sb/Si 도핑 peak split과 동류) |

### Raman / XPS / 분해산물 (정성·정량)
| 항목 | 값 | 비고 (Fig) |
|---|---|---|
| Raman PS₄³⁻ (주피크) | **424 cm⁻¹** (LPSC-P) → Cu 도핑 시 **red-shift**(격자팽창) | Fig 1b (싱크로트론, 532 nm) |
| Raman 진동모드 (PS₄³⁻) | ν_deform **199/278**, ν_sym **424**, ν_asym **569/600 cm⁻¹** | Fig 1d,e (deconvolution) |
| **Raman Cu–S (신규)** | **475 cm⁻¹** (x=0.1, (P/Cu)S₄ 형성) + **255 cm⁻¹** | Fig 1c,d — **P→Cu 치환 직접 증거**, S–S band 219 cm⁻¹도 동반 |
| Cl 2p XPS | **198.81 / 200.44 eV** (doublet, 변화 없음 = 격자 Cl) | Fig S14a |
| P 2p XPS (PS₄³⁻) | **131.56 eV** (fresh) | Fig S14b |
| Li 1s XPS | LiCl **56.38 eV** (5th cycle 후 LPSC-P) / **55.6 eV** (LPSC-1, 약함) | Fig 7a |
| S 2p (PS₄³⁻) | **161.51 / 162.84 eV** (doublet) | Fig 7b, fresh+cycled |
| **Li₂S (LPSC-P 분해)** | S 2p **160.9 eV** (black, cycled) — 강 / poly-sulfide P₂Sₙ **163.52 eV** | Fig 7b — **LPSC-P/Li 계면 심한 분해 (LPSC-1엔 약함)** |
| 산화종 (LPSC-P cathode-shell) | **P₂S₅ 133.16·134.14 eV** + phosphate **PO₄³⁻**(산소 오염) | Fig S14b — LPSC-P 산화 |
| **Cu 2p XPS** | **932.3 eV** (distinct, before/after cycle 불변) | Fig S14c — Cu(I) 격자 진입·안정 확인 |
| **Cu₃PS₄ (대기노출)** | XRD 신규 peak **~51°** (LPSC-1-AE-S) | Fig 8b — 노출 후 Cu₃PS₄ 형성 = 대기안정 산물 |

### 계면 저항 진화 (time-resolved EIS, Fig 7c)
- **R/R₀** (대칭셀 aging, 0/3/5/12/24 h): **LPSC-P 지수적 증가**(R/R₀ ~1.5↑, 저항성 passivation·Li₂S 형성) / **LPSC-1 거의 평탄**(R/R₀ ~1.1). → Wenzel류 "저항성 interphase 성장 = Li kinetics 저하"를 LPSC-1이 회피.

## 4. 재료 & 방법 (실험)
- **합성**: **ball-mill-free 고상반응** (논문 강조점 — 저비용·확장성). 전구체 Li₂S(99.9 %) + P₂S₅(≥99.99 %) + LiCl(99.995 %) + **CuCl(≥99 %)** 화학량론 혼합 → **agate mortar 0.5 h 손분쇄** → pellet(360 MPa) → 진공 석영관 봉입 → **5 °C/min 승온·자연냉각** 어닐. (li2025·통상 argyrodite의 ball-mill과 대조 — *밀링 없이* 고상.)
- **최적화**: 소결온도(350–600 °C, 50 °C 간격)·시간(1–20 h)·도핑량(x=0→0.5)을 σ로 스캔 → **550 °C·15 h·x=0.1**.
- **구조분석**:
  - **싱크로트론 XRD** (NSRRC TLS01C2, 15 keV, λ=0.774916 Å, 60 s) + **GSAS-II Rietveld**(F-43m·자리점유·격자상수; Cu→4b, Cl→4a/4c 확정).
  - **Raman** (Uni-RAM, 532 nm; Kapton capillary 또는 airtight glass sandwich로 대기차단) — PS₄³⁻ 진동모드 + **Cu–S 475 cm⁻¹** 신규 band.
  - **SEM/EDX** (FE-SEM) — light-gray 분말, 입자형상·원소(P/S/Cl/Cu) 균일 분포(toluene 0.5 h sonication 후).
- **전기화학**:
  - **AC 임피던스** (Bio-Logic VMP3, SAS, SUS 차단전극, 1 MHz–1 Hz·10 mV) → σ_total·Ea(Arrhenius 303–333 K).
  - **DC polarization** (1 V, SUS\|SE\|SUS, chronoamperometry) → **σ_e**(전자전도, Fig 4c).
  - **CV** (Li\|SE\|Pt planar + composite C-SE\|SE\|M; M=Li or In; 0.5 mV/s; SE-카본 70:30 C65 complex로 분해 증폭) → 산화·환원 분해창. **In/InLi(Li-free) 대극으로 SE 자체 분해 분리** + Li 금속 대극으로 실사용 호환.
  - **CCD** (대칭 Li\|SE\|Li, 50 °C; step size 0.1 mA/cm²[0.1≤x≤1] / 0.2[1≤x≤3]) → critical current density.
  - **대칭 Li plating/stripping** (0.1/1/3 mA/cm², BT-2000) → 2400 h(0.1)·400 h(1)·200 h(3) 과전압 안정성.
  - **time-resolved EIS** (대칭셀 aging, 0.5 mA/cm² 방전상태) → 계면저항 R/R₀ 진화 (Fig 7c).
- **계면 화학**: **ex-situ XPS** (fresh / 5th cycle / short-circuit 후; pellet-side + Li-side; 0.5 mA/cm²) → Li 1s·P 2p·S 2p·Cu 2p·Cl 2p. SEM(Li anode 단면 morphology)·EDX mapping(Cu/S/Cl/P).
- **대기/대기안정**: **H₂S gas sensor**(GX-2009, 100 mg pellet, 55–60 % RH desiccator + micro-fan, 2 min마다 25 min) — LPSC-P / LPSC-1 / LPS(Li₃PS₄) 비교. **노출 후 XRD**(LPSC-1-AE = humidity 66 % 1 h, -AE-S = 추가 550 °C 1 h 소결) → Cu₃PS₄ 형성·구조 유지 확인.

## 5. 결과 — 섹션별 상세 (수치 전부)

### 5.1 구조·자리 귀속 (Fig 1, 2d)
싱크로트론 XRD: 전 조성(x=0–0.5) **F-43m cubic argyrodite** 유지, ICSD #259205(Li₆PS₅Cl)와 일치. x↑ 시 **피크 저각 이동(격자팽창)** — Cu⁺(0.77 Å)·Cl⁻ 큰 이온 + Cu–S(EN 차 작음). **x>0.1서 Li₂S·LiCl 2차상**(피크 split·신규) — Cu가 4b서 P를 치환하면서 잉여 Li₂S/LiCl 석출(Sb-Li₄SnS₄·Si-Li₆PS₅I 도핑서 본 peak split과 동류). **Rietveld → Cu=4b(P자리 공유)·Cl=4a/4c(S자리)** 확정. Raman: PS₄³⁻ 주피크 **424 cm⁻¹**가 Cu 도핑 시 red-shift(격자팽창), **신규 Cu–S band 475 cm⁻¹**(+255 cm⁻¹) = **P→Cu 치환 직접 증거**((P₁₋ₓCuₓ)S₄⁽³⁺⁴ˣ⁾ 형성).

### 5.2 이온전도 — σ·Ea (Fig 2)
- 합성 최적화(§3): **550 °C·15 h·x=0.1 → σ 4.34 mS/cm·Ea 0.25 eV**. 600 °C·소결과다·x>0.1은 모두 불순물상으로 σ↓.
- **σ↑ 3대 기전** (Fig 2d, DFT 거리분석):
  1. **charge carrier↑**: Cu²⁺→P⁵⁺ 헤테로치환 → 전하중성 위해 **Li⁺ 추가**(24g 자리).
  2. **anion disorder↑**: Cl⁻ 추가가 **4a/4c S²⁻ 자리 무질서** 증가 (Zeier "site-disorder→σ↑").
  3. **cage 내 Li 거리 단축**: Li₆S cage 안 **48h–48h 거리 3.298→2.997 Å** → intra-cage doublet jump(48h–48h) 활성화·Ea↓. 추가 Li⁺(24g)는 인접 cage 간 **doublet jump의 bridge**(48h–24g–48h intercage)로 Ea 추가 하강. (cage 간 48h–48h는 3.970→4.189 Å로 *늘지만* 24g bridge가 보상.)
  - **EN 차 작은 Cu(1.95)–S(2.58)** 가 Ge–S(Ge 2.01)와 유사 → LGPS(12 mS/cm)·Li₆PS₅GeS(5.4) 류의 polarizability 향상과 같은 결.

### 5.3 전기화학 안정성 — CV (Fig 3)
- **planar 전극** (LPSC-P\|LPSC-1\|Pt, In/InLi 대극, Fig S6a): LPSC-1은 0–8 V서 **분해전류 없음**; LPSC-P는 0.4 V·>5 V서 분해. *단* 저자 자신이 "**planar는 SE-Li 접촉 적고 kinetic 느려 분해 과소평가**"(Dewald ref49)라 명시 → composite로 재확인.
- **composite (SE+카본 70:30)** (Fig 3a–f, 분해 증폭):
  - **In/InLi 대극** (Fig 3a vs 3b): C-LPSC-P는 **S²⁻→S⁰/Sₓ²⁻**(bridging sulfur 산화)·**P³⁺→P⁵⁺ ~0.62 V** 강 분해전류(mA level); **C-LPSC-1은 0–8 V 무분해**(완전 소멸). → **8 V ultra-wide ESW(vs In/InLi) — "이 고전압 안정성을 보고한 첫 신소재"**(저자 주장).
  - **Li 금속 대극** (Fig 3c vs 3d): C-LPSC-P는 sulfur 산화 전류 noise + 단락; **C-LPSC-1은 매우 작은 faradic 전류**(sulfur 산화), **2nd cycle서 LPSC-P 대비 ~160배 작음**(Fig 3c,d,f). Cu(I)가 **(P₁₋ₓCuₓ)S₄ 강공유결합·rigid framework**로 bridging sulfur(–[S]ₙ–)를 안정화 → 산화·환원 *둘 다* 억제.
  - 🔑 **메커니즘 주장**: "Cu(I)가 P 자리서 strong covalent bond + rigid S²⁻ framework → bridging sulfur 안정 → ultra-high (P/Cu)S₄ 안정성, **이전 미보고**." (단 — §10 비판: 8 V는 *thermodynamic* ESW가 아니라 *kinetic*(carbon 접촉·접근성), 황화물 진짜 산화창 <3 V는 Banik/우리 grand-potential 합의.)

### 5.4 Li 금속 계면 — 대칭셀·CCD (Fig 5, 4b,c)
- **CCD** (50 °C, step): **LPSC-P 0.75 → LPSC-1 3.0 mA/cm²** (4×). x별 화산형(x=0.1 최적; 다른 x는 0.89–1.05 mA/cm²). **σ_e가 레버**: Fig 4b가 **σ_e vs CCD 역상관** 직접 — LPSC-1 σ_e **1.49×10⁻⁹ S/cm**(최저) ↔ CCD 최고; LPSC-P σ_e **8.75×10⁻⁹**(최고) ↔ CCD 최저 0.75. (Han ref27 "최저 σ_e가 dendrite 억제" 인용.)
- **대칭 Li plating/stripping**:
  - **0.1 mA/cm²** (0.5 mAh/cm²): LPSC-1 **2400 h 무overpotential alteration**(17.76→24.11 mV 미세); LPSC-P **38 cyc 후 voltage drop·dendrite**(과전압 11.35→13.76 mV, 2000 h대) (Fig 5a, S8).
  - **1 mA/cm²**: LPSC-1 **>400 h** 안정 flat plateau (Fig S9).
  - **3 mA/cm²** (50 °C): **LPSC-P는 ~5–10 h서 severe Li-incompatibility·과전압 폭주·단락**(Fig 5c); **LPSC-1은 >200 h flat plateau**(Fig 5d). 최고전류서도 ultra-high 가역성(Fig S12).
- **morphology** (Fig 6): LPSC-P pellet은 5th cycle·단락 후 **black spot·mossy Li·균열·void**(불균일 plating, Li-sulfide 응집); **LPSC-1은 smooth·void 거의 없음·강한 접착**(EDX: LPSC-P S 불균일 응집 / LPSC-1 균질). LPSC-P는 Li-sulfide(Li₂S) 형성이 cyclability 저하.

### 5.5 계면 화학 — ex-situ XPS·time-resolved EIS (Fig 7)
- **XPS 5th cycle** (0.5 mA/cm²): **LPSC-P Li 1s에 LiCl 56.38 eV 신규 + S 2p에 Li₂S 160.9 eV(강)·poly-sulfide P₂Sₙ 163.52 eV**(심한 분해, 저전도 Li₂S 형성); **LPSC-1은 LiCl 신호 약함(55.6 eV)·PS₄³⁻ 유지·(P/Cu)S₄ tetrahedra 무손상**(분해 미미). Cu 2p **932.3 eV** before/after 불변(Cu 안정). Cl 2p **198.81/200.44 eV** 불변.
- **time-resolved EIS** (Fig 7c): **R/R₀ LPSC-P 지수적 증가**(저항성 passivation 성장·Li kinetics 저하, Wenzel ref59 정합) / **LPSC-1 거의 평탄** → 저항성 interphase 형성 회피.
- **모식도** (Fig 7d): (I) Li kinetics → (II) Li metal → (III) void formation·contact loss·Li dendrite. LPSC-P는 passivation layer 두껍게·접촉손실; LPSC-1은 얇은 안정층.

### 5.6 대기안정 — H₂S·Cu₃PS₄ (Fig 8)
- **H₂S 발생** (55–60 % RH, 24 min): **LPS(Li₃PS₄) ~1.8 cm³/g(최악) > LPSC-P 1.07 > LPSC-1 0.49 cm³/g**. → CuCl 도핑이 H₂S를 **~절반(2배 억제)**. 14 min 시점 0.18/0.49/1.07로 갈림.
- **기전**: soft acid **Cu(I)** 가 **Cu₃PS₄**(또는 (P/Cu)S₄ 강 Cu–S)를 형성 → thio-phosphate **oxophilicity↓**(물·O 친화도↓) → 가수분해(H₂S 방출) 억제. **HSAB**: soft acid는 soft base(S²⁻) 선호·hard base(O²⁻/H₂O) 회피 → Cu가 S를 "잡아" P–S 보호. (Hayashi/Ohtomo MₓOᵧ·Wang Li₄Cu₈GeS₆ 선행과 같은 결, 단 격자 도핑.)
- **노출 후 XRD** (Fig 8b): LPSC-1-AE(66 % RH 1 h)·-AE-S(추가 550 °C 1 h)서 argyrodite 주피크 유지 + **신규 ~51° = Cu₃PS₄**(+ 미동정 미량). LPSC-P는 직접 노출 시 즉각 colorization·급분해. → **CuCl 도핑이 구조 무결성·대기내성 향상**.

## 6. DFT/계산 방법 ★
> ⚠ **DFT 사용은 *최소* — Li 이동경로/거리 1건이 전부.** code·PAW는 명시, 그러나 functional·k·ecut·supercell·무질서 처리는 **미명시**. gap·DOS·탄성·ESW·계면 슬랩·물 흡착 **전부 안 함**(li2025보다도 DFT 얕음). **방어적 인용 시 "DFT (VASP/PAW; functional·k 미상, Li-path 거리만)"로 표기.**

- **code**: **VASP** (Vienna Ab-initio Simulation Package) — ref43/44 (Kresse-Hafner/Kresse-Furthmüller) 명시.
- **PAW**: **projector augmented-wave** (Blöchl ref45) 명시.
- **functional**: **미명시** (GGA-PBE 추정이나 본문 근거 없음 → "n/a").
- **pseudo / k-points / ecut(wfc,rho) / supercell / nat**: **전부 n/a** (본문·SI 미제공).
- **DFT+U / AIMD / MLIP**: **없음** (정적 거리계산만).
- **무질서 처리(SQS/enumerate/single-config)**: **n/a** — "their most stable geometry"로 Li₆PS₅Cl·Li₆.₃P₀.₉Cu₀.₁S₄.₉Cl₁.₁ 구조 최적화 후 Li 거리 측정. 단일 안정배열로 보이나 명시 없음.
- **수행한 계산 (1건)**:
  - **Li 이동경로 거리** (Fig 2d): 두 구조의 **48h–48h Li 거리** 측정 →
    - **cage 내(intra, Li₆S group)**: **3.298 (LPSC-P) → 2.997 Å (LPSC-1)** = 단축 → intra-cage doublet jump(48h–48h) 쉬워짐·Ea↓.
    - **cage 간(inter, 인접 Li₆S group)**: **3.970 → 4.189 Å** = 격자팽창으로 *증가* → intercage 약간 불리하나, **추가 Li⁺가 24g 자리에 들어가 48h–24g–48h doublet jump bridge** 역할로 보상 → 종합 Ea↓.

> 우리 대비: 이 논문 DFT는 **"기하 거리→정성적 σ 해석"** 수준으로, 우리 AIMD(D·Ea)·grand-potential·elastic·PDOS와 **방법 동급이 아님**(우리가 훨씬 깊음). 단 **"intra-cage Li 거리 단축·24g bridge가 intercage doublet jump를 매개"** 는 우리 inter-cage hopping·`migration_volume_fraction` 멘탈모델과 *정성적으로* 같은 그림. 절대 거리(2.997/4.189 Å)는 functional/구조 미상이라 직접 비교 부적절.

## 7. Post-processing ★
- **DC polarization → σ_e**: 1 V 정전압(SUS\|SE\|SUS) chronoamperometry 정상상태 전류 → 전자전도도. 기록=S/cm 절대값. **(우리 미측정 — 차용 가능 지표; Fig 4b가 σ_e vs CCD 역상관 직접.)**
- **CCD step**: 대칭 Li 전류 단계 증가, short 직전 = CCD. 기록=mA/cm². x별 화산형.
- **CV** (planar + composite SE/카본): 산화(S²⁻→S⁰/Sₓ·P³⁺→P⁵⁺ 0.62 V)·환원 전류로 분해 취약성. 기록=peak 전위·전류크기·"몇 배 작은가"(160×). **In/InLi(SE자체) vs Li 금속(실사용) 두 대극으로 분리.**
- **AC 임피던스 (time-resolved)**: aging 중 R/R₀ → 저항성 interphase 성장 진단(LPSC-P 지수증가 vs LPSC-1 평탄).
- **Rietveld (GSAS-II)**: 격자상수·자리점유(Cu→4b, Cl→4a/4c).
- **Raman deconvolution**: PS₄³⁻ 진동모드(199/278/424/569/600) + Cu–S 475 cm⁻¹ 분리 → 결합변화·치환 정량.
- **H₂S gas sensor**: RH 노출 중 누적 H₂S(cm³/g) → 대기안정 정량. **노출 후 XRD**로 Cu₃PS₄ 산물·구조유지 확인.
- **ex-situ XPS**: Li 1s·S 2p·P 2p·Cu 2p·Cl 2p, fresh/cycled/short-circuit + pellet/Li-side → 분해종(Li₂S 160.9·LiCl 56.38·P₂Sₙ 163.52·Cu 932.3) 동정.
> 우리 적용: **σ_e DC-polarization 측정값(LPSC-1 1.49×10⁻⁹·LPSC-P 8.75×10⁻⁹ S/cm)** 은 우리가 못 가진 **실측 전자전도 anchor** (li2025 1.02×10⁻⁸→3.35×10⁻⁹·Liu23 8.16×10⁻⁹과 같은 ~10⁻⁸–10⁻⁹ S/cm 줄, **세 번째 anchor**). **σ_e↔CCD 역상관(Fig 4b)** 은 우리 "SEI/bulk 전자절연=dendrite 레버" 서사의 또 하나 실측 증거.

## 8. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a** | x=0–0.5 XRD + 확대 (저각 이동=격자팽창) + 불순물(x>0.1 Li₂S/LiCl) | 도핑 용해한계 (Cl-rich LiCl 불순물과 같은 결) |
| **1b,c** | Raman x별 + Cu–S **475 cm⁻¹** 확대 (x=0.1) | **P→Cu 치환 직접 증거**(Cu–S band) |
| 1d,e | Raman deconvolution 150–350·500–650 cm⁻¹ (Cu–S vs Li-P-S) | 진동모드 귀속·결합변화 |
| **2a** | σ vs 소결온도(brown)·시간(blue) — **550 °C/15 h peak 4.18–4.23** | 합성 최적화 곡선(우리 조성 최적화와 평행) |
| **2b** | Arrhenius (x별) — σ·Ea | Ea 추출 |
| **2c** | σ·Ea vs x (화산형, x=0.1 σ 최고·Ea 최저 0.25) | σ-x volcano(Cu 용해한계) |
| **2d** | **Li 이동경로 + 48h Li 거리** (Li₆PS₅Cl 3.298/3.970 vs LPSC-1 2.997/4.189 Å) | **DFT Li-path**: intra 단축·24g bridge=σ↑ 논리 |
| 3a,b | CV composite (In/InLi 대극): C-LPSC-P 강분해 / **C-LPSC-1 0–8 V 무분해** | "8 V ESW(vs In/InLi)" — ⚠ kinetic |
| **3c,d** | CV composite (Li 대극): C-LPSC-P noise·단락 / C-LPSC-1 **~160× 작은 전류** | Li 금속서도 분해 억제 |
| 3e,f | CV 2nd cycle (In·Li 대극) 비교 | 가역성·분해전류 비 |
| **4b** | **σ_e vs CCD (역상관)** x별 — LPSC-1 σ_e 1.49e-9 ↔ CCD 3.0 | **"σ_e↓→CCD↑" 직접 증거**(우리 dendrite 레버) |
| 4c | chronoamperometry σ_e (SUS\|SE\|SUS) | σ_e 실측법 |
| **5a,b** | CCD step (LPSC-P 0.75 / **LPSC-1 3.0 mA/cm²**) | dendrite 억제 정량(4×) |
| **5c,d** | 대칭 Li 3 mA/cm²: LPSC-P 단락(severe) / **LPSC-1 >200 h 안정** | 고전류 음극 계면 |
| **6a** | SEM Li 표면(fresh/5th/short) — LPSC-P void·mossy / LPSC-1 smooth | 음극 morphology(dendrite) |
| 6b | EDX Li-side (Cu/S/Cl/P) — LPSC-P S 불균일 / LPSC-1 균질 | 분해 균일성 |
| **7a,b** | cycled XPS Li 1s·S 2p — **LPSC-P Li₂S(160.9)·LiCl(56.38)·P₂Sₙ(163.52) / LPSC-1 약함** | 계면 분해 정량(음극) |
| **7c** | time-resolved EIS R/R₀ — LPSC-P 지수증가 / LPSC-1 평탄 | 저항성 interphase 성장 진단 |
| 7d | 계면 모식도 (I kinetics/II Li/III void·dendrite) | 음극 계면 도식 |
| **8a** | H₂S 발생 (LPS ~1.8 / LPSC-P 1.07 / **LPSC-1 0.49 cm³/g**) | 대기안정 정량(절반) |
| **8b** | 노출후 XRD — **Cu₃PS₄ ~51°** 형성·구조유지 | 대기내성 구조 증거(Cu₃PS₄ 산물) |
| S6 | planar CV (분해 과소평가 한계) | 측정법 caveat |
| S8,S9 | 대칭 Li 0.1(2400 h)·1 mA/cm²(400 h) | 장수명 |
| S14a,b,c | XPS Cl 2p(198.81/200.44)·P 2p(131.56→P₂S₅ 133.16)·**Cu 2p 932.3** | 도펀트·산화종 화학상태 |

## 9. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> ⚠ **핵심 주의**: 본 논문 모체 **LPSC-P = Li₆PS₅Cl = 우리 comp1과 동일 조성**. 단 도핑 변수가 **CuCl(Cu양이온+Cl음이온)** 이라 우리 modelc(Cl만 증량)와 **변수 종류가 다름** — "도핑→σ↑·Ea↓·계면안정" 방향은 비교 가능하나 *원인 분해(Cu vs Cl)* 는 직접 대응 불가.

| 항목 | 이 논문 (LPSC-P / LPSC-1) | 우리 (comp1 / modelc) | 일치 / 차이 + 이유 |
|---|---|---|---|
| **모체 조성** | LPSC-P = **Li₆PS₅Cl** | **comp1 = Li₆PS₅Cl** | **✓ 동일 모체** (직접 출발점 일치) |
| **σ 도핑 빠름** | LPSC-P 1.11 → LPSC-1 **4.34 mS/cm** (3.9×) | D(600K) 3.09→7.90e-6, Ea 0.253→0.224 | **✓ trend 일치**(도핑이 σ↑). 단 이들 변수=CuCl(Cu+Cl), 우리=Cl만(modelc). **메커니즘 공통 결**(carrier↑·무질서↑·cage Li거리). 절대값=실험 EIS vs 우리 AIMD |
| **Ea↓** | ~0.30 → **0.25 eV** | 0.253 → **0.224 eV** | **✓ 일치**(도핑 시 Ea↓). 절대값 LPSC-P 0.30 vs 우리 comp1 0.253 = 실험(cold-press EIS) vs AIMD 방법차. 둘 다 ~0.25 수렴 |
| **cage Li 거리** | 48h–48h intra **3.298→2.997 Å**; inter 3.970→4.189 | 우리 BVSE/AIMD inter-cage hop 분석 | △ **정성 일치**(intra 단축·24g bridge=σ↑) — 우리 inter-cage 멘탈모델과 같은 그림. 절대거리는 functional 미상이라 비교 부적절 |
| **σ_e 절대값** | LPSC-P **8.75×10⁻⁹** / LPSC-1 **1.49×10⁻⁹ S/cm** | 우리 **미측정** (gap=wide insulator로만 추론) | ✗ 우리 못 봄 → **세 번째 실측 anchor 제공**(li2025 1.02e-8→3.35e-9·Liu23 8.16e-9과 같은 줄). **σ_e↔CCD 역상관(Fig 4b)** = dendrite 레버 직접증거 |
| **환원 산물 (음극)** | LPSC-P→**Li₂S(160.9)+Li₃P+P₂Sₙ**(XPS, 심한 분해)·LiCl | comp1/modelc 0V→**Li₃P+Li₂S+LiCl** | **✓ 동일 chemistry**(Li₂S+Li₃P+LiCl). LPSC-1은 (P/Cu)S₄ rigid화로 이 분해 *억제* |
| **산화 분해 (CV)** | S²⁻→S⁰/Sₓ·P³⁺→P⁵⁺(~0.62 V vs In/InLi); LPSC-P 강·LPSC-1 160× 작음 | grand-potential onset 2.256 V → P₂S₇+S | **△ 산물 일치(S²⁻ 산화)**. 단 이 논문 "8 V ESW(vs In/InLi)"는 *kinetic*(carbon 접근성) — 우리 thermo onset 2.256 V·Banik과 **충돌하는 over-claim**(§10) |
| **밴드갭** | **n/a** (미계산·미측정) | comp1 2.066 / modelc 2.098 (PBE) | ✗ 비교 불가 — 이 논문 gap 안 봄 |
| **기계 E/B/G** | **n/a** | E_VRH comp1 22.06 / modelc 27.66; B₀ 26.23/21.71 | ✗ 비교 불가 — 이 논문 탄성 안 봄 |
| **대기안정 (H₂S)** | H₂S 1.07→**0.49 cm³/g**; Cu₃PS₄ 형성·oxophilicity↓ | 우리 **범위 밖**(0K closed hull·기체 X) | ✗ 우리 못 봄 → 정성 인용. 단 우리 oxophilicity descriptor·"강결합→안정"(ICOHP) 논리와 결이 같음 |

## 10. 적용 인사이트 (깊게) — 우리 축에 매핑
> **이 논문이 우리 work에 닿는 곳 = 도핑(F축)·이온전도(A축)·전자구조/σ_e(D축)·음극 계면(E축).** li2025의 자매라 인사이트 골격은 li2025와 평행하되, **(1) 모체가 우리 comp1과 동일(Li₆PS₅Cl)**, **(2) Cl 음이온(Br 아님)이라 우리 Cl-rich 축과 더 가까움**, **(3) DFT Li-path 거리분석**, **(4) Cu₃PS₄ 대기안정 산물**이 차별점.

1. **σ 축 = "무질서·extra-Li⁺가 공통 레버"의 *세 번째* 사례 (Cu+Cl)**: LPSC-P 1.11→LPSC-1 4.34 mS/cm·Ea 0.30→0.25 = 우리 comp1→modelc(Ea 0.253→0.224)와 **같은 방향**. 우리=Cl만, li2025=Cu+Br, **이 논문=Cu+Cl** → "Cl이든 Cu든 Br이든 *carrier 추가·anion disorder·cage Li 거리*가 σ↑의 공통 레버"라는 일반화 강화. **특히 모체가 동일 Li₆PS₅Cl(comp1)** 이라 비교축이 가장 깨끗. (Excel exp#9 mixed-halide·li2025 CuBr₂와 한 줄.)
2. **σ_e 실측 anchor 3개째 + σ_e↔CCD 역상관**: 우리는 bulk σ_e를 못 쟀고 gap(2.07)으로 "wide insulator"라고만 했는데, 이 논문이 **σ_e=8.75×10⁻⁹(LPSC-P)·1.49×10⁻⁹(LPSC-1) S/cm** 를 DC polarization으로 실측 + **σ_e vs CCD 역상관(Fig 4b)** 을 *직접* 보임. → slide25 "σ_e가 dendrite 레버"의 **외부 실측 근거**(li2025 1.02e-8→3.35e-9·Liu23 8.16e-9에 이어 세 번째 anchor, 모두 ~10⁻⁸–10⁻⁹ S/cm 일치). ⚠ 단 σ_e 차이가 gap만이 아니라 Cu defect/carrier 복합(§10).
3. **음극 계면 = (P/Cu)S₄ rigid framework가 native 분해 억제 (우리 'electron-blocking interphase' 패밀리와 *다른 메커니즘*)**: li2025·우리 cascade는 **wide-gap 절연 *분해산물*(LiCl/LiBr/Li₂O/Li₃PO₄)이 e⁻ leak 차단**인데, 이 논문은 **bulk SE 자체를 (P/Cu)S₄로 rigid·저-σ_e화 → 애초에 분해를 덜 일으킴**(Li₂S/Li₃P 자체가 적게 생김). → 우리 "절연 SEI" 패밀리와 **목표는 같으나(dendrite 억제) 레버 위치가 다름**(분해산물 절연 ↔ 모체 자체 보강). 도핑 cascade 설계 시 "산물을 절연으로"와 "모체를 분해저항으로" 두 갈래가 있음을 상기시킴.
4. **대기안정 = 결합강도/oxophilicity descriptor의 또 다른 실증 (Cu₃PS₄·HSAB)**: soft acid Cu가 **Cu₃PS₄/(P/Cu)S₄ 강 Cu–S** 로 PS₄ oxophilicity↓·가수분해 억제(H₂S 1.07→0.49 cm³/g) = li2025 "Cu–S>P–S"(물흡착 ΔE)·우리 **oxophilicity/ICOHP "강결합→안정"** 논리와 같은 결. 우리 O-doping이 **P–O(ICOHP −8.43, +41 % vs P–S)** 로 host를 bonding-lock하는 것과 평행 — "강한 음이온-host 결합이 분해(가수분해/산화) 저항". (단 우리는 대기안정 직접 계산 못 함 → §H 기체상 gap; 이 논문은 Cu₃PS₄ *산물*을 XRD로 동정 = li2025보다 산물 증거 구체적.)
5. **dual-doping = cascade 동기 ③ (양이온+음이온 동시)의 *원조 사례***: 우리 cascade(Mg/Cl/O/F)·li2025(Cu+Br)에 더해 **Cu+Cl** = "어떤 *쌍*이 σ·σ_e·계면·대기안정을 동시에 주나"의 또 한 예. 특히 **CuCl 단일 전구체로 Cu·Cl 동시 공급**(li2025 CuBr₂와 같은 "한 염으로 두 도펀트") = 합성 단순성. 우리 cascade가 단일원소 도판트뿐 아니라 **metal-halide 염(MCl/MBr)** 형태 co-doping도 후보로 고려할 근거.
6. **ball-mill-free 고상합성**: 이 논문 셀링포인트 중 하나(저비용·확장성). 우리 DFT엔 직접 무관하나, "고상 vs 밀링"이 무질서 정도·자리점유·2차상에 영향(σ 절대값 차)을 줌을 상기 — 문헌 σ 절대값 비교 시 합성법도 변수.

## 11. 인용 가능 문장 (deck/paper용)
- "Taklu et al. (Nano Energy 2021) reach σ = 4.34 mS/cm (Ea 0.25 eV) by CuCl dual doping of **Li₆PS₅Cl** (vs 1.11 mS/cm, 0.30 eV undoped) — same starting host as our comp1, the same disorder/extra-Li⁺/shortened-cage-Li lever (48h–48h 3.298→2.997 Å) that drives our comp1→modelc Ea drop (0.253→0.224 eV), here via Cu²⁺/P⁵⁺ + Cl⁻ instead of Cl⁻ alone."
- "Their measured electronic conductivities (LPSC-P 8.75×10⁻⁹, CuCl-doped 1.49×10⁻⁹ S/cm, inversely correlated with CCD 0.75→3.0 mA/cm²) give a third external anchor (with Li25 1.02e-8→3.35e-9 and Liu23 8.16e-9) for our otherwise gap-only σ_e / dendrite argument."
- "CuCl doping halves H₂S evolution (1.07→0.49 cm³/g) by forming Cu₃PS₄ / strong Cu–S bonds that lower the thiophosphate oxophilicity (HSAB, soft-acid Cu) — a bond-strength-driven stability that parallels our P–O bonding-lock (ICOHP −8.43 eV) in the O-doping route."
- "⚠ Their '8 V ultra-wide window' is vs In/InLi on a carbon-composite electrode and is *kinetic* (accessibility), not a thermodynamic ESW — the intrinsic sulfide oxidation onset stays S²⁻-limited at ~2.3 V (Banik; our grand-potential 2.256 V)."

## 12. 주의 / 한계 (over-claim 방지 — **비판적**)
- ⚠⚠ **"8 V ultra-wide ESW"는 thermodynamic 아님 — kinetic over-claim**: Fig 3b의 8 V는 **(a) In/InLi 기준**(Li/Li⁺ 환산 아님), **(b) carbon-composite·planar의 *접근성/kinetic*** 측정. 저자 자신이 planar는 "분해 과소평가"라 했지만 composite 8 V도 **황화물 *intrinsic* 산화창이 아님** — Banik(VBM=S 3p→onset S-limited)·Zuo·우리 grand-potential(2.256 V)은 황화물 진짜 산화 onset이 **<3 V**임에 합의. **"CuCl이 산화창을 8 V로 넓혔다"는 인용 절대 금지** — "carbon-composite 셀에서 kinetic 분해전류가 160× 작아졌다"로만. (Cu가 bridging-S를 *kinetically* 안정화하는 건 사실이나 thermodynamic window 확장과 별개.)
- ⚠ **DFT 극히 얕음**: code(VASP)·PAW만, **functional·k·ecut·supercell·무질서 전부 미명시 + gap·DOS·탄성·ESW·계면·물흡착 *전부 안 함*** (li2025보다도 얕음 — Li 거리 1건). → 우리 값과 정량 비교는 **σ·Ea·σ_e(실험)·산물 chemistry(XPS)** 수준에서만; DFT 절대값(2.997/4.189 Å)은 방향·정성만.
- ⚠ **변수가 다중(Cu+Cl 동시)**: σ↑·CCD↑·대기안정↑이 **Cu 효과인지 Cl 효과인지 분리 안 됨**(Cu만/Cl만 대조군 없음 — Cl은 모체에도 1.0 있음). → "CuCl 도핑이 ~"로만, "Cu가 σ를 올린다" 단일귀속 금지. (li2025와 동일 caveat.)
- ⚠ **σ_e 차이 ≠ 단일원인**: σ_e 8.75e-9→1.49e-9(~6×↓)는 Cu가 만든 전자구조 변화 + carrier·defect 동시 → 단일 분리 불가. gap은 아예 미측정.
- ⚠ **자리귀속 모델 의존**: Cu→4b(P자리)·Cl→4a/4c는 Rietveld 추론이나, lab/싱크로트론 분해능 한계로 Cu@4b vs Cu@Li 등 완전 확정 어려움(우리 [Liu23] Mg@P 비판·li2025 caveat과 같은 류). Cu 산화상태도 본문 Cu²⁺(P치환 논리)와 Cu(I)(HSAB·Cu₃PS₄ 논리)가 **혼재** — 정합성 약함(§Cu valence 모호).
- ⚠ **대칭셀 조건 vs 실사용**: CCD 3.0·2400 h는 **0.1–3 mA/cm²의 낮은 면적용량**(0.5 mAh/cm²)·**50 °C**. full cell·실온·고면적용량 데이터 **없음**(li2025의 LCO/FeS₂ full cell과 대조 — 이 논문은 full-cell 성능 미검증).
- ⚠ **Cu₃PS₄ 대기산물**: XRD 신규 ~51° 1개 peak로 Cu₃PS₄ 동정 — 단일 peak 귀속이라 확정성 보통(미동정 미량상 동반 언급).
- **외부 그룹** (NTUST 대만·Hwang) — 우리 그룹 논문 아님. **INDEX 우리그룹 태그 금지.**

## 13. 기법 용어 미니사전
- **HSAB (Hard-Soft Acid-Base)**: soft acid(Cu⁺/Cu²⁺)는 soft base(S²⁻)와 강결합 선호·hard base(O²⁻/H₂O) 회피 → Cu–S>P–S → 가수분해(H₂S) 저항. 도펀트 선택·대기안정 원리.
- **DC polarization (σ_e)**: 정전압(1 V) 인가 후 정상상태 전류 = 전자(만의) 전도도(이온 차단). dendrite 레버.
- **CCD (critical current density)**: dendrite/short 없이 견디는 최대 전류밀도(mA/cm²).
- **헤테로치환 (heterovalent substitution)**: Cu→P⁵⁺(가수 다름) → 전하중성 위해 Li⁺ 추가 생성 → carrier↑.
- **48h / 24g / 4a / 4c / 4b 자리**: argyrodite(F-43m) Wyckoff — 48h=mobile Li, 24g=추가 Li(intercage bridge), 4a/4c=S²⁻/halide(disorder), 4b=P(여기 Cu 치환).
- **doublet jump**: cage 내 48h–48h(intra) 또는 cage 간 48h–24g–48h(inter) Li 이동의 짝 점프 — argyrodite σ의 핵심 경로.
- **oxophilicity**: 산소(물) 친화도. 높으면 가수분해(H₂S 방출) 쉬움. Cu 도핑이 이를 낮춤.
- **(P/Cu)S₄ / Cu₃PS₄**: Cu가 P 자리서 만드는 강 Cu–S 공유 framework(전자구조 rigid화·대기안정 산물).
- **In/InLi 대극**: Li-free 대극(SE 자체 분해를 Li-금속 부반응과 분리) — 전압기준이 Li/Li⁺와 다름.
- **ball-mill-free 고상합성**: 볼밀 없이 손분쇄+소결만 — 저비용·확장성(이 논문 셀링포인트), 단 무질서·자리점유에 영향.
