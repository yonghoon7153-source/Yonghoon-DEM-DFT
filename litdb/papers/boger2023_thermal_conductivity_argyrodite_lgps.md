# 리튬이온 전도성 고체전해질의 열전도도 — argyrodite 4종 + LGPS 를 LFA × 공극률 계열 × 포논 계산으로 — Böger (ACS Appl. Energy Mater. 2023) · ⚠ SI 만

> slug `boger2023_thermal_conductivity_argyrodite_lgps` · DOI `10.1021/acsaem.3c01977` [추정 — 파일명 `ae3c01977_si_001` 기준, 미확인] · type `exp (LFA thermal diffusivity × porosity series · EIS) + DFT phonon (CRYSTAL23 HSE06 · phonopy) + EMT (Bruggeman)` · PDF `ae3c01977_si_001.pdf` · digested `2026-09-26` · status ✅ SI-only (본문 미확인)

> ## ⛔⛔ 본문 미확인 — 이 카드는 **Supporting Information 만** digest 했다
> 사용자가 본문 PDF 를 받을 수 없었다. 읽은 것은 **SI 24쪽 전부** — Section S1–S9 · 식 1–12 · Figure S1–S15 (크롭 15장 전부 육안 확인) · 참고문헌 37개. **SI 에 표는 없다.**
> - **서지**: SI 에는 저널·권·쪽·DOI 가 **인쇄돼 있지 않다.** 아래 서지는 정본 `ketter2025_resistor_network_models_predict_transport_properties` 의 원문
>   (Ketter 2025 *Nat. Commun.* 참고문헌 **30번**) 에서 옮긴 것이다 — *"Böger, T., Bernges, T., Li, Y., Canepa, P. & Zeier, W. G. Thermal Conductivities of Lithium-Ion-Conducting
>   Solid Electrolytes. ACS Appl. Energy Mater. 6, 10704–10712 (2023)."* **(본문 미확인)**. 저자 5인·순서는 SI 표지(p. S1)와 **일치**한다.
> - **DOI**: `10.1021/acsaem.3c01977` 은 ACS SI 파일명 규칙(`ae3c01977_si_001`)에서 **추정**한 것이다 — **미확인**. 인용 전에 본문으로 확인할 것.
> - **제목이 다르다**: SI 표지 제목은 *"Supporting Information - On the thermal conductivities of lithium ion conducting solid electrolytes"* (출판 제목과 다름 — 그대로 기록).
>   PDF 메타: Word 원고명 `Supporting Information_ACS_AEM_submission_2nd_revision_v1.docx` · 작성자 `tboeger` · "Microsoft: Print To PDF" · 생성 **2023-09-26** (= 2차 수정본 SI).
> - **적지 않은 것**: 본문에만 있을 결론 — RT 의 κ_SE 수치 · 활성화에너지(본문 `Fig. 1a`) · κ(T) 해석(본문 `Fig. 5`, phonon-gas / diffuson 비교) · 조성 간 서열의 기전 설명.
> - 라벨: **SI-stated** = SI 텍스트에 인쇄 · **SI-in-figure** = SI 그림 **안** 주석으로 인쇄된 값 (예: `κ_SE = 0.71±0.04`) · **digitized ≈** = 그림에서 픽셀로 읽음 (방법·오차 §6) ·
>   **DERIVED(ours)** = 우리가 계산 · **2차 인용** = SI 가 다른 문헌에서 가져온 값 (그 원문 미확인) · **[본문 미확인]** = 본문에 있을 것으로 보이나 못 봄.
> - ± 의 정의(SD / 적합 표준오차)는 SI 에 **적혀 있지 않다** (§3.2 의 재적합으로 보면 **적합 표준오차의 크기**다 — 추론).
> - 본문 확보 시 채울 목록 → §14.

## 0. ★ SELF-51 판정 — 우리 `κ_SE = 0.7 W m⁻¹ K⁻¹` 의 근거가 이 SI 에 있는가

| 질문 | 답 | 근거 (SI 위치) | 등급 |
|---|---|---|---|
| SI 에 **Li₆PS₅Cl 의 κ** 가 있나 | **있다 — 치밀(φ_SE → 1) Bruggeman 외삽값 κ_SE = 0.71 ± 0.04 W m⁻¹ K⁻¹ @ 173 K (α = 3.2 ± 0.2)** · **0.65 ± 0.05 @ 523 K (α = 2.7 ± 0.3)**. 실온 κ_SE 는 SI 에 **숫자로 없다** | `Fig. S10` · `Fig. S11` 그림 안 주석 | SI-in-figure |
| **"0.66"** 은 SI 어디에 있나 | **없다.** 텍스트 24쪽 전문 · 그림 15장의 주석 전부 (κ_SE 0.49–0.71 · D_SE 0.29–0.34 · α) 를 확인 — 0.66 은 없다 ⇒ **본문 값으로 추정 [본문 미확인]** | 텍스트 추출 전수 + 15장 육안 | — |
| SI 만으로 **실온 κ_SE** 를 재구성하면 | **κ_SE(RT) = D_SE · c_p · ρ_SE = 0.34 ± 0.02 mm² s⁻¹ × 1.021 J g⁻¹ K⁻¹ × 1.860 g cm⁻³ = 0.646 ± 0.038 W m⁻¹ K⁻¹** (0.61–0.68) | D_SE = `Fig. S12` (SI-in-figure) · c_p = `Fig. S5` (digitized, `Fig. S7` 로 교차검증 0.1 %) · ρ_SE = Li₆PS₅Cl 결정학 밀도 **외부값** (정본 `ohno2020` SI Table S1 의 a = 9.8591 Å 로 우리 계산 1.8603; 이 SI 에는 격자상수 없음) | DERIVED |
| 실온 **펠릿 6개의 κ** 는 | φ 0.755 · 0.778 · 0.815 · 0.815 · 0.884 · 0.909 → κ_eff = D_eff · c_p · ρ_SE · φ = **0.269 · 0.334 · 0.387 · 0.387 · 0.439 · 0.497** — Ketter 2025 Source Data `Fig5b` 의 **Böger 점 (열 이름 `BM-vger`, 0.26928–0.49828)** 과 **0.3 % 안**에서 일치 | `Fig. S12` (digitized) · Ketter SD `Fig5b.csv` | DERIVED |
| 그 6점에 κ = κ_SE φ^α 를 맞추면 | **로그-선형 κ_SE = 0.661 (α 2.88)** · 비선형 최소제곱 0.642 ± 0.043 (α 2.71 ± 0.36) · κ_SE 를 0.66 에 고정하면 α = 2.85 | Ketter SD 의 Böger 점 재적합 | DERIVED |
| ⇒ **0.66 의 정체** | **실온 Bruggeman 적합의 κ_SE** (φ → 1 외삽) 로 읽는 것이 가장 자연스럽다 — 로그-선형 적합이 0.661 을 재현한다. ⚠ **추론** — 본문에서 문장·방법을 확인할 것 | — | 추론 |
| 측정·보정 방식 | **LFA 열확산 D** (NETZSCH LFA-467, 개량 Cape–Lehman) × **c_p ≈ c_V (DFT 포논 계산, 측정 아님)** × **기하밀도 ρ** · 펠릿 φ 0.75–0.91 (바이스 프레스 / **등방 100 · 600 MPa 40 min**, 이어 합성온도에서 **15 min 소결**) · 공극 보정 = **Bruggeman κ_eff = κ_SE φ^α (α 적합)** · 열확산은 D_eff = D_SE φ^(α−1) | SI p. S4–S5 · 식 8 · 10 · 11 · `Figs. S9–S12` | SI-stated |
| 우리 `0.7` 은 | **치밀 규약에서 방어된다** — 173 K 값 0.71 과 같고, 실온 재구성 0.646 ± 0.038 의 **+8 % (+1.4σ)**, 523 K 값 0.65 ± 0.05 의 +8 % (+1σ). 온도 의존이 약하다 (173 → 523 K 에서 −8 %, 오차 안) | 위 행들 | DERIVED |

**판정 (정직판)**:
1. **라벨은 고칠 수 있다 — 근거가 이제 SI 에 실물로 있다.** *"치밀(무공극) Li₆PS₅Cl, Böger 2023 SI `Figs. S10–S11` 의 Bruggeman 외삽 0.65–0.71 W m⁻¹ K⁻¹ (173–523 K);
   실온 ≈ 0.65 (SI `Fig. S12` D_SE × 계산 c_p × 결정학 ρ 로 재구성)"* — Ketter 카드 §0 **선택지 A 는 "Böger 확인 전 Assumed" 에서 "SI 근거 있음"으로 승격**된다.
   **선택지 B (값을 0.66 으로 + 직접 인용)** 는 **"0.66" 이라는 숫자 자체가 본문에만 있어** 아직 못 한다 — 그러나 0.7 → 0.66 은 오차(±0.04–0.05) 안이라 **값을 바꿀 실익은 작다.**
2. ⚠ **"치밀 LPSCl κ" 에는 폭이 있다 (같은 Zeier 그룹 안에서)**: Böger 펠릿(소결)은 φ 0.884 에서 0.439, Ketter 펠릿(등방 500 MPa 60 min, 카드 기록에 소결 언급 없음)은
   φ 0.879 에서 **0.323 (0.74×)**. Ketter 의 한 점을 **Böger 의 α (2.7–3.2)** 로 치밀 쪽에 되돌리면 **0.46–0.49** (DERIVED — α 가 옮겨 간다는 **가정** 위의 값).
   ⇒ 치밀 LPSCl κ 후보 = **0.46–0.49 (Ketter 배치, 가정 의존) ~ 0.65–0.71 (Böger 배치, SI)**. 우리 0.7 은 그 **상단**이다.
3. ⚠ **규약 충돌은 이 SI 로 풀리지 않는다 — 오히려 크기가 보인다.** κ_SE (Böger) 는 **공극을 뺀(φ→1) 치밀 외삽값**, 우리 σ_grain 3.0 은 **고적층압 펠릿 total 값**
   (정본 `cronau2021` SI `Fig. S2c`) 이다. 이 SI 가 열 채널에 대해 주는 크기: φ = 0.88 펠릿 ↔ 치밀의 비 = φ^α = **0.66–0.71** (α 2.7–3.2, DERIVED) — 즉 **펠릿값을 치밀 상 입력으로
   쓰면 열에서는 ~30 % 과소**. σ_ion 쪽에 같은 배율을 쓸 근거는 **없다** (이온 α 는 이 SI 에 없고, 입계 이온 저항은 열 경계저항과 다른 물리) → §7-2.

## 1. 한 줄 요약
Zeier 그룹(뮌스터) + Canepa 그룹(NUS/휴스턴)이 **물질마다 한 배치로** 고체전해질 5종 — **Li₆PS₅Cl (상용)** · Li₅.₅PS₄.₅Cl₁.₅ · Li₆PS₅Br · Li₆PS₅I · Li₁₀GeP₂S₁₂ — 을
밀도가 다른 펠릿 5–6개씩(φ_SE ≈ 0.66–0.91)으로 만들어 **LFA 로 열확산 D(T) (173 → 523–623 K)** 를 재고, **DFT 포논 c_V** 와 기하밀도로 κ = D·c_p·ρ 를 얻은 뒤
**Bruggeman 멱법칙 κ_eff = κ_SE φ^α** 로 공극을 벗겨 **치밀 κ_SE** 를 냈다 → SI 가 보여 주는 결과: **κ_SE 0.49–0.71 W m⁻¹ K⁻¹ (173 · 523 K, 5종 전부)** ·
**공극 지수 α 2.1–3.2 (이상적 구형 1.5 보다 훨씬 가파름)** · **κ_SE 의 온도 의존 약함 (LPSCl −8 % · Br +24 % · I +41 % / 173 → 523 K)** = 결정질 phonon-gas 의 1/T 와 거리가 멀다 ·
이온 전도의 열 기여 **≤ 0.012 W m⁻¹ K⁻¹ (무시)** · Li₆PS₅Cl 과 Li₆PS₅I 의 원자당 c_V 는 거의 같다 (173 K < 5 %, 298 K < 1 %).
⇒ **우리 `κ_SE = 0.7` 은 "치밀 Li₆PS₅Cl, Böger SI" 로 재라벨할 수 있다** (§0). 동시에 α ≈ 3 은 **우리 순수-SE 침대 κ 를 재는 검증 표적**이 된다 (§8-②).

## 2. 메타
| 저자 (SI p. S1, 5인 · \* 교신) | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| **Thorben Böger**ᵃ·ᵇ, Tim Bernges ᵃ, Yuheng Li ᶜ, **Pieremanuele Canepa** ᶜ·ᵈ·ᵉ, **Wolfgang G. Zeier\*** ᵃ·ᵇ·ᶠ | *ACS Appl. Energy Mater.* **6**, 10704–10712 (2023) — **Ketter 2025 ref 30 에서 옮김 (본문 미확인)** | `10.1021/acsaem.3c01977` [추정 — 파일명 기준, 미확인] | Li₆PS₅Cl · Li₅.₅PS₄.₅Cl₁.₅ · Li₆PS₅Br · Li₆PS₅I · Li₁₀GeP₂S₁₂ | 실험 (LFA · EIS · XRD) + DFT 포논 (c_V · 포논 DOS) + 유효매질 해석 |

소속 (SI p. S1, stated): ᵃ Univ. Münster, Institute of Inorganic and Analytical Chemistry · ᵇ **BACCARA** 대학원 (Münster) · ᶜ NUS Materials Science & Engineering ·
ᵈ NUS Chemical & Biomolecular Engineering · ᵉ Univ. of Houston, Electrical & Computer Engineering · ᶠ **FZ Jülich IEK-12 (Helmholtz-Institut Münster)**. 교신 wzeier@uni-muenster.de.
계보: Bernges·Zeier 는 정본 `ketter2025_…` (RN 모델) · `ohno2020_…` (round robin) · `schlautmann2023_…` 의 공저자 — **같은 그룹의 κ 데이터가 Ketter 2025 `Fig. 5b` 에 재사용**됐다 (§12).

## 3. 핵심 수치

### 3.1 시료 — 합성 · 상순도 (SI p. S3–S4, `Figs. S13–S14`)
| 시료 | 출처 / 합성 (stated) | XRD 전 (`Fig. S13`, SI-in-figure) | XRD 후 — LFA 뒤 (`Fig. S14`, SI-in-figure) | 펠릿 φ_SE |
|---|---|---|---|---|
| **Li₆PS₅Cl** | **상용 구매** (공급사 미기재) | R_wp 7.3 %, gof 1.4 · F-43m 만 표기 | R_wp **15 %**, gof **3.5** · **LiCl 4.9 wt% · Li₂S 2.2 wt%** | 0.755 · 0.778 · 0.815 · 0.815 · 0.884 · 0.909 (digitized; Ketter SD 75.443–90.865 %) |
| Li₅.₅PS₄.₅Cl₁.₅ | 고상 723 K 1 주 → 분쇄 → 723 K 2 일 | R_wp 9.9 %, gof 1.5 · Li₁₅(PS₄)₄Cl₃ 1.9 wt% · LiCl 1.7 wt% | R_wp 7.1 %, gof 1.7 · Li₁₅(PS₄)₄Cl₃ **9.5 wt%** · LiCl **5.7 wt%** | 73.2 · 73.7 · 77.4 · 77.5 · 86.2 · 86.8 % (`Fig. S7a` 범례, SI-in-figure) |
| Li₆PS₅Br | 고상 823 K 2 주 | R_wp 7.8 %, gof 1.8 | R_wp 8.5 %, gof 1.4 | 79.6 · 80.5 · 82.2 · 83.0 · 86.3 · 88.8 % (`Fig. S7c`) |
| Li₆PS₅I | 고상 823 K 2 주 | R_wp 6.2 %, gof 2.1 | R_wp 6.9 %, gof 1.7 | 78.9 · 81.7 · 82.0 · 89.3 · 90.5 % (`Fig. S7e`) |
| Li₁₀GeP₂S₁₂ | 기계화학 (Fritsch P7, 400 rpm) → 펠릿 → 773 K 20 h | R_wp 6.1 %, gof 1.9 · P4₂/nmc | R_wp 7.4 %, gof 1.6 | ≈ 0.663 · 0.679 · 0.717 (겹친 2점) · 0.817 · 0.822 (digitized, `Fig. S10`) |

- 합성 상세 (stated): Li₂S (Alfa Aesar 99.9 %) · P₄S₁₀ (Sigma-Aldrich) · LiCl (Alfa 99 %, **볼밀 24 × 10 min / 10 min 휴지, 500 rpm** 선처리) · LiBr (Alfa > 99 %) · LiI (Alfa 99.95 %) ·
  마노 유발 15 min · **탄소코팅 석영 앰플을 1073 K 동적 진공 2 h 건조** 후 진공봉입 · 승온 100 K/h, 자연냉각. LGPS = Li₂S · P₄S₁₀ · GeS (99.99 %) · S (99.999 %, **3 % 과량**) —
  80 mL ZrO₂ 용기 · 볼:시료 10:1 · Ø5 mm 볼 · (10 min 밀링 + 15 min 휴지) × 25 cycle @ 400 rpm 을 **3회** (사이 10 min 손분쇄) → 펠릿 → 773 K 20 h (17 °C/h).
- XRD (stated): Stoe Stadi P, Debye–Scherrer, Ge(111) 단색기, Dectris Mythen 2X 1K, Cu Kα₁ 1.5406 Å, 2θ 10–70° (q 0.71–4.68 Å⁻¹), 0.015° 간격 · Pawley → Rietveld (수정 TCH pseudo-Voigt).
- 텍스트 결론 (stated, p. S19): LiBr·LiI 부상 < 1.5 wt% · Cl 계는 LiCl 이 "약간 더" · **argyrodite 상순도 > 85 wt%** · LFA 뒤 *"No significant degradations"* (`Fig. S14` 캡션).
  ⚠ 그림 수치와의 긴장은 §11-4·§11-5.
- **"같은 배치"**: 모든 측정은 각 물질의 **같은 배치**로 했다 (p. S3, stated) — 조성 간 차이를 미세구조·화학량론 변동과 분리하려는 설계.

### 3.2 ★ 치밀 κ_SE · 공극 지수 α — 5종 전부 (`Figs. S10–S12` 그림 안 주석 = SI-in-figure)
| SE | **κ_SE @ 173 K** (W m⁻¹ K⁻¹) | α @ 173 K | **κ_SE @ 523 K** | α @ 523 K | **D_SE @ 실온** (mm² s⁻¹) | α_D @ 실온 | κ_SE 173→523 K |
|---|---|---|---|---|---|---|---|
| **Li₆PS₅Cl** | **0.71 ± 0.04** | 3.2 ± 0.2 | **0.65 ± 0.05** | 2.7 ± 0.3 | **0.34 ± 0.02** | 1.8 ± 0.4 | −8 % |
| Li₅.₅PS₄.₅Cl₁.₅ | 0.55 ± 0.03 | 2.4 ± 0.2 | 0.54 ± 0.04 | 2.1 ± 0.3 | 0.29 ± 0.02 | 1.6 ± 0.3 | −2 % |
| Li₆PS₅Br | 0.49 ± 0.019 | 2.2 ± 0.2 | 0.61 ± 0.01 | 2.7 ± 0.1 | 0.30 ± 0.01 | 1.7 ± 0.2 | +24 % |
| Li₆PS₅I | 0.49 ± 0.02 | 2.4 ± 0.2 | 0.69 ± 0.05 | 3.1 ± 0.4 | 0.33 ± 0.01 | 1.5 ± 0.2 | +41 % |
| Li₁₀GeP₂S₁₂ | 0.58 ± 0.05 | 2.6 ± 0.3 | 0.63 ± 0.04 | 2.61 ± 0.20 | 0.34 ± 0.02 | 1.8 ± 0.2 | +9 % |

- **실온 κ_SE 는 5종 모두 SI 에 없다** — Li₆PS₅Cl 만 §0 처럼 재구성했다 (**0.646 ± 0.038**, DERIVED). 나머지는 결정학 밀도가 SI 에 없어 재구성하지 않았다 [본문 미확인].
- **폭**: κ_SE 전체 0.49–0.71 W m⁻¹ K⁻¹ — **다섯 SE 가 한 자릿수 안, 서로 1.5× 안**이다. Li₆PS₅Cl 이 173 K 에서 가장 높다.
- **온도 의존** (DERIVED): phonon-gas(움클랍) 1/T 라면 173 → 523 K 에서 **−67 %** 여야 하는데 관측은 −8 % … **+41 %**. ⇒ 결정질 포논 기체보다 **유리-유사(diffuson) 거동**에 가깝다
  (본문 `Fig. 5` 가 phonon-gas·diffuson 기준선과 비교 — SI 식 12 는 그 diffuson 기준선의 식; 해석 본문은 [본문 미확인]).
- **α 는 이상적 구형 개재물(1.5)보다 훨씬 크다 — 2.1–3.2** ⇒ 펠릿의 공극은 부피 배제 이상의 벌점(목·접촉·공극 형상)을 준다 (SI p. S11: *"The exponent α is often used as a fitting parameter,
  because the actual microstructure is more complex than the idealized spherical inclusions assumed … corresponding to α = 1.5"*).
- **실온 닫힘 검산** (DERIVED): 식 11 에 따르면 α_D = α − 1. `Fig. S12` 의 α_D + 1 = **2.8 / 2.6 / 2.7 / 2.5 / 2.8** ↔ `Fig. S9` 의 298 K α (digitized) **2.92 / 2.55 / 2.70 / 2.53 / 2.77** — 5종 모두 0.12 안.
- **재적합** (DERIVED — 그림에서 LPSCl 점을 디지타이즈해 다시 맞춤): 173 K 비가중 0.671 ± 0.034 (α 2.96 ± 0.28) · **세로 오차막대 가중 0.69–0.70 (α 3.14–3.15)** ≈ 주석 0.71 ± 0.04 (3.2 ± 0.2) ·
  523 K 0.63–0.64 (α 2.54–2.69) ≈ 0.65 ± 0.05 (2.7 ± 0.3) · 실온 D 0.340 (α_D 1.75–1.87) ≈ 0.34 ± 0.02 (1.8 ± 0.4). ⇒ 주석값은 **가중 적합으로 재현**되고, ± 는 적합 표준오차 크기다 (**추론**).

### 3.3 ★ Li₆PS₅Cl — 펠릿 6개 (DERIVED / digitized)
| φ_SE | κ_eff @ 173 K (digitized) | κ_eff @ 523 K (digitized) | D_eff @ 실온 (digitized, mm² s⁻¹) | κ_eff @ 실온 = D·c_p·ρ_SE·φ (DERIVED) | Ketter SD `Fig5b` (Böger 점) |
|---|---|---|---|---|---|
| 0.755 | 0.282 | 0.282 | 0.1875 | **0.269** | 0.26928 (φ 75.443) |
| 0.778 | 0.329 | 0.343 | 0.226 | **0.334** | 0.33444 (77.808) |
| 0.815 | 0.356 | 0.390 (겹친 2점의 중심) | 0.250 (겹친 2점의 중심) | **0.387** | 0.38293 (81.515) |
| 0.815 | 0.385 | 〃 | 〃 | 〃 | 0.39223 (81.515) |
| 0.884 | 0.445 | 0.444 | 0.261 | **0.439** | 0.43964 (88.340) |
| 0.909 | 0.518 | 0.497 | 0.288 | **0.497** | 0.49828 (90.865) |

- c_p(298 K) = 1.021 J g⁻¹ K⁻¹ (§3.5) · ρ_SE = 1.860 g cm⁻³ (외부, §0). 실온 재구성이 Ketter Source Data 와 **0.3 % 안**에서 맞는다 ⇒ **ρ_SE ≈ 1.86 · c_p ≈ 1.02 를 Böger 도 썼다**는 뜻이다 (추론).
- **φ 쌍 구조 (추론)**: 6 펠릿이 (0.755, 0.778) · (0.815, 0.815) · (0.884, 0.909) 세 쌍으로 모인다 — SI 의 세 성형법(**바이스 프레스 < 등방 100 MPa < 등방 600 MPa**, 40 min)과
  한 쌍씩 대응하는 것으로 보이지만 **SI 는 펠릿↔방법 대응을 적지 않는다**. 그래서 이 점들을 압밀 곡선(Heckel 등)으로 쓰지 않는다.
- 실온 α (φ 0.75–0.91 범위 적합): 2.71 (비선형) – 2.88 (로그-선형) — `Fig. S9` 의 298 K 값 2.92 (digitized) 와 정합.
- 173 K 와 523 K 의 같은 펠릿 κ_eff 가 대부분 ± 5 % 안이다 (0.282 ↔ 0.282 · 0.445 ↔ 0.444 · 0.329 ↔ 0.343 · 0.518 ↔ 0.497) — LPSCl 은 이 온도창에서 κ 가 **거의 평평**하다.

### 3.4 공극 지수 α 의 온도 의존 (`Fig. S9`, digitized ≈ ± 0.02; 오차막대 ± 0.2–0.4)
| SE | α (173 K) | α (≈ 298 K) | α (≈ 523 K) | 끝점 | 추세 |
|---|---|---|---|---|---|
| **Li₆PS₅Cl** | 3.21 | 2.92 | 2.68 | **≈ 623 K: 2.19** (다른 4종은 523–573 K 에서 끝) | 완만 감소 |
| Li₅.₅PS₄.₅Cl₁.₅ | 2.36 | 2.55 | 2.06 | 523 K | ≤ 323 K 2.4–2.8 → ≥ 373 K 2.0–2.2 |
| Li₆PS₅Br | 2.17 | 2.70 | 2.68 | 574 K: 2.48 | 173 K 만 낮다 |
| Li₆PS₅I | 2.52 | 2.53 | 3.07 | 573 K: 3.03 | ≥ 424 K 상승 (2.97–3.16) |
| Li₁₀GeP₂S₁₂ | 2.61 | 2.77 | 2.61 | 574 K: 2.61 | 평평 (2.58–2.94) |

- 캡션 (stated): *"the Bruggeman exponents are constant within uncertainty in the investigated temperature range"* — 대부분 맞지만 **LPSCl 3.21 (173 K) ↔ 2.19 (623 K)** 과
  **I 2.40 (198 K) ↔ 3.16 (473 K)** 은 오차막대가 겹치지 않는다 (§11-6).
- 측정 온도 (digitized): 173 · 198 · 223 · 248 · 273 · 298 · 323 · 373 · 423 · 473 · 523 (· 573 · 623) K — 저온은 25 K, 고온은 50 K 간격.

### 3.5 비열 c_V (`Figs. S5 · S7`; c_p ≈ c_V)
| 양 | 173 K | 298 K | 523 K | → Dulong–Petit | 등급 |
|---|---|---|---|---|---|
| Li₆PS₅Cl, 원자 1 mol 당 (J mol⁻¹ K⁻¹) | ≈ 16.4 | **≈ 21.1** | ≈ 23.5 | 3R = 24.94 | `Fig. S5` digitized (173 K 는 S7 경유) |
| **Li₆PS₅Cl, g 당 (J g⁻¹ K⁻¹)** | ≈ 0.80 | **≈ 1.02** | ≈ 1.14 | 1.208 | DERIVED (÷ M̄ = 20.646 g mol⁻¹) |
| Li₅.₅PS₄.₅Cl₁.₅, g 당 | 0.770 | 0.989 | 1.102 | 1.17 (그림) / 1.169 (3R/M̄) | `Fig. S7b` digitized |
| Li₆PS₅Br, g 당 | 0.683 | 0.877 | 0.977 | 1.04 / 1.036 | `Fig. S7d` digitized |
| Li₆PS₅I, g 당 | 0.594 | 0.762 | 0.850 | 0.90 / 0.901 | `Fig. S7f` digitized |

- **교차검증** (DERIVED): SI 는 Li₅.₅PS₄.₅Cl₁.₅ · Li₆PS₅Br 의 c_V 를 **Li₆PS₅Cl 의 포논 DOS** 로 계산했다고 적는다 (p. S8). 실제로 `Fig. S5` 의 298 K 원자당 21.08 을 각 M̄ 로 나누면
  **0.988 / 0.876 / 0.762** — `Fig. S7` 판독 **0.989 / 0.877 / 0.762** 와 0.1 % 안. ⇒ 우리 디지타이즈와 SI 의 서술이 서로를 검증한다. Ketter 카드의 1.022 J g⁻¹ K⁻¹ (298 K, "Böger 포논 계산") 과도 일치.
- Li₆PS₅Cl ↔ Li₆PS₅I 원자당 c_V 차이: **173 K < 5 % · 298 K < 1 %** (stated). 무거운 음이온일수록 **g 당** c_V 는 낮다 (평균 몰질량 ↑, stated).
- **c_p − c_V 팽창항** (식 1, stated): B·α_V²·T/ρ < **0.2 %** — B 를 **실험(펠릿) 체적탄성률** "< 6 GPa (LGPS, ref 17) · 1.5 GPa (argyrodite, ref 18)" 로 넣었다 (**2차 인용**);
  α_V = 3.4 × 10⁻⁵ (LGPS, ref 17) · 6.5–6.9 × 10⁻⁵ K⁻¹ (argyrodite, ref 20) (2차 인용; 선·체적 구분 미기재). 저자 논리: 계산 B (ref 19 Deng 2016) 는 *"fully dense, single-crystal"* 가정이라 펠릿에 안 맞는다.
  ⚠ **우리 DFT B₀ 26.23 GPa 를 넣으면 팽창항은 1.7–2.0 %** (DERIVED) — 어느 쪽이든 c_p ≈ c_V 근사는 **2 % 안**에서 성립한다.

### 3.6 열 수송의 이온 기여 (Section S5, stated)
- 이온 Lorenz 수 (Rice & Roth, ref 23): **κ_i = L_i · T · σ_i**, **L_i = [9 L₀ / (2π² z²)] · E_A/(k_B T)**, L₀ = (π²/3)(k_B/e)² (Wiedemann–Franz, 식 3–4).
- 가장 잘 흐르는 두 SE 의 σ_i 를 **최고 측정온도로 외삽**: κ_i = **0.012 (Li₅.₅PS₄.₅Cl₁.₅) · 0.003 W m⁻¹ K⁻¹ (LGPS)** · 실온 **4.0 × 10⁻⁵ · 3.3 × 10⁻⁵** ⇒ *"within uncertainty … not considered"*.
  ⇒ 우리 κ 모델이 이온 열전도 항을 두지 않는 것은 **정당**하다 (실온에서 κ_SE 의 10⁻⁴ 배).

### 3.7 이온전도 (Section S1 · `Figs. S1–S2`) — **같은 시료의 펠릿 total σ**
- 측정 (stated, p. S6): PEIS **7 MHz–100 mHz, 233–333 K**, Biologic SP-300 · **가압셀 (광택 스테인리스 스탬프), 토크 10 Nm** (ref 14 Zhang 2017) · 측정 전 **단축 370 MPa 3 min** 치밀화.
  토크 → 적층압(MPa) 환산은 SI 에 **없다**. 펠릿 밀도·두께도 없다.
- 등가회로 (stated, 문장이 꼬여 있음 — §11-8): 이 4종은 bulk/GB 를 분리할 수 없어 **두 번째 반원 대신 단순 옴 저항**을 썼다. LPSCl 의 233 K Nyquist 는 **본문**에 있다.
- **σ(298 K) · E_a** (digitized `Fig. S2`, ln(σT) vs 1000/T — ±0.03 in ln ⇒ ±3 %; 12 온도 333 · 323 · 313 · 303 · 298 · 293 · 283 · 273 · 263 · 253 · 243 · 233 K):

| SE | ln(σT) @ 298 K | **σ₂₉₈ (mS cm⁻¹)** | E_a (σT 형, 적합창에 따라) | 비고 |
|---|---|---|---|---|
| **Li₆PS₅Cl** | −0.29 | **≈ 2.5** (2.4–2.5) | ≈ 0.38 (333–283 K) · 0.41–0.42 (전 구간) | 273 K 이하 마커가 Br 삼각형에 일부 가림 |
| Li₅.₅PS₄.₅Cl₁.₅ | (LGPS 마커에 가림) | ≈ 5.8–6.5 (저온 가시점 적합의 외삽) | ≈ 0.38–0.40 | 298 K 점 직접 판독은 가림 때문에 편향 |
| Li₆PS₅Br | −0.78 | ≈ 1.5 | ≈ 0.33 | — |
| Li₆PS₅I | −6.80 | ≈ 0.0037 (3.7 µS cm⁻¹) | ≈ 0.36 | — |
| Li₁₀GeP₂S₁₂ | 0.63 | ≈ 6.3 | ≈ 0.29 | — |

- **E_a 의 stated 값은 본문 `Fig. 1a`** 에 있다 [본문 미확인] — 위 E_a 는 디지타이즈 경향값이다.
- `Fig. S1` (233 K) Nyquist 의 총 비저항 (figure-read ≈): Li₅.₅ ≈ 9.3 kΩ·cm · Br ≈ 21 kΩ·cm · I ≈ 10.2 MΩ·cm · LGPS ≈ 3.35 kΩ·cm → σ₂₃₃ ≈ 1.1 × 10⁻⁴ · 4.8 × 10⁻⁵ · 9.8 × 10⁻⁸ · 3.0 × 10⁻⁴ S cm⁻¹
  — `Fig. S2` 의 233 K 점 (1.12 × 10⁻⁴ · 4.9 × 10⁻⁵ · 1.02 × 10⁻⁷ · 3.15 × 10⁻⁴) 과 5 % 안 (DERIVED 교차검증).
- ⚠ 캡션은 온도창을 *"233 K to 273 K"* 라 적지만 그림·실험절은 **233–333 K** (§11-1).

### 3.8 유효매질 모델 비교 (Section S6 · `Fig. S6`, stated)
- 비교한 5 모델: **Voigt** (병렬, 식 5 — 상한) · **Reuss** (직렬, 식 6 — 하한) · **Maxwell** (식 7 — 무한희석, 충전재 < 20–25 % 에서만 유효) · **Bruggeman** (식 8, 구형 개재물이면 α = 1.5) ·
  **Meredith–Tobias** (식 9 — 입자 크기 두 종만 가정).
- 계산 조건: **κ_SE = 0.5 · κ_Ar = 0.017 W m⁻¹ K⁻¹**, 기공 전도 유무 (κ_g = 0) 둘 다. 결론: 높은 φ_SE 에서 Maxwell · Bruggeman · Meredith–Tobias 는 거의 같고, **기공의 기체 전도 영향도 작다**
  (그림 오른쪽 확대: φ = 0.75–1.0 에서 κ_eff/κ_SE 차 ≲ 0.02, figure-read). ⇒ **기공 비전도 가정 + α 재보정이 쉬운 Bruggeman** 을 채택.
- ⚠ 그 비교는 **α = 1.5** 에서만 했다. α ≈ 2.9 로 식 8 을 풀면 Ar 기공의 기여가 φ 0.85–0.90 에서 **+2.4–4 %**, φ 0.75 에서 **+9 %** 로 커진다 (DERIVED, §7 표 "기공의 기체 전도" 행).

### 3.9 포논 (Section S3 · `Figs. S3–S4`, stated + figure-read)
- Li₆PS₅Cl: 포논 가지 **대부분이 거의 무분산 = 군속도가 매우 낮다** · Li 진동 **5–15 THz** · P 는 **≈ 17 THz** 에 몰림 · S 는 전 대역 · Cl 사영 DOS 는 저주파(< ~5 THz, figure-read).
- Li 배열이 다른 **두 번째 최저에너지 배열**(`Fig. S3b`)도 같은 결론 = 배열 선택에 둔감 (저자 결론).
- Li₆PS₅I (`Fig. S4`): I 사영 DOS 가 더 낮은 주파수 (≈ 1.5–2 THz 피크, figure-read) · 그 밖엔 차이 없음.
- 대역 상한 ≈ 18 THz (figure-read).

## 4. 측정·계산 방법 ★
- **DEM / MPM / FEM / 수송 솔버**: **해당 없음.** 이 논문은 우리 두 κ 솔버(접촉망 `network_conductivity.py` · STEP3 복셀 FV `step3_sigma.py`)가 **공통으로 곱하는 입력** κ_SE 와,
  그 입력이 **다공 미세구조에서 어떻게 깎이는지 (α)** 의 실험값을 준다. frame[5] 어느 절반도 소유하지 않는다 — **입력층 + 검증 표적**.
- **입자 처리 ★**: 해당 없음 (실험). 펠릿 = 분말 **바이스 프레스 / 등방 100 · 600 MPa (40 min)** 압분체 → 각 물질의 합성온도에서 **15 min 소결** (*"to avoid hysteresis during thermal cycling"*).
  ⚠ **상용 Li₆PS₅Cl 의 "합성온도" 는 정의되지 않는다** (SI 미기재, §11-9). 입도·PSD·SEM 은 SI 에 없다.
- **LFA** (stated): NETZSCH **LFA-467** · 실온 이하 **MCT 검출기 + ZnS 창**, 실온 이상 **InSb 검출기 + 사파이어 창** · 검출 시간·증폭 자동 · 온도당 **3 샷 (173 K 는 5 샷)** ·
  **개량 Cape–Lehman 모델** (refs 1–2: Blumm & Opfermann 2002 · Cape & Lehman 1963) · 적외 흡수·방사 + 공기/수분 차단용 **흑연 스프레이 코팅 (N₂ 글러브박스)**.
- **κ = D · c_p · ρ** (본문 식 1 [본문 미확인]; SI 식 10 이 이 형태를 쓴다) · **c_p ≈ c_V (DFT)** · **ρ = 기하밀도**.
- **공극 보정**: Bruggeman 일반형 (식 8) φ_SE = (κ_eff − κ_g) / [(κ_eff/κ_SE)^(1−1/α) (κ_SE − κ_g)] → κ_g = 0 이면 **κ_eff = κ_SE φ^α** (그림의 적합식).
  열확산은 ρ/ρ_SE ≈ φ 를 써서 **D_eff = D_SE φ^(α−1)** (식 10–11) — *"a by one reduced Bruggeman exponent can be expected"*. ρ_SE = *"density at full consolidation"* (값 미기재).
- **DFT 포논** (stated; SI 의 괄호 표기 = Li₆PS₅I 값): Li/공공 배열 **전수 열거 — Li₆PS₅Cl 927 (Li₆PS₅I 4752)** (pymatgen) → Ewald 에너지 최저 **500 (1000)** 개 → 대칭 중복 제거 → DFT 완화 → 최저 에너지 구조 채택.
  **CRYSTAL23 · HSE06 · triple-zeta valence + polarization 기저 (Vilela Oliveira 2019) · 6 × 6 × 6 k · 에너지 수렴 10⁻⁷ Ha**. 포논 = **phonopy 유한변위 0.01 Å** ·
  에너지 수렴 10⁻¹¹ Ha (10⁻¹⁰ Ha) · **2 × 2 × 2 초셀 (104 원자)** · 2 × 2 × 2 k · 후처리 q 20 × 20 × 20 · **비해석항(NAC) 보정**. **음이온 무질서는 다루지 않았다** (배열 수 관리).
  Li₆PS₅Br · Li₅.₅PS₄.₅Cl₁.₅ 는 Li₆PS₅Cl DOS 로 근사 · LGPS 는 문헌 DOS (ref 16 Xu 2022).
- **c_V** (식 2): c_V = (3R/M̄_w) ∫ g(ω) (ħω/k_BT)² e^{ħω/k_BT} / (e^{ħω/k_BT} − 1)² dω.
- **diffuson 기준선** (식 12, ref 32 Agne 2018): κ_diff(T) = P · n^{1/3} k_B/π · ω_avg(T), ω_avg(T) = ∫ [g(ω)/3n] (ħω/k_BT)² e^{…}/(e^{…} − 1)² ω dω · **P = 에너지 전달 성공 확률 (적합 인자, ref 33)**.
  이 선을 쓴 κ(T) 비교는 본문 `Fig. 5` [본문 미확인].
- **EIS**: §3.7.

## 5. Figure set ★  (크롭 15장 — 전부 육안 확인; 수동 재크롭 기록은 `figures.json` 의 `note` · `pdf_map.tsv`)
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| S1 | Li₅.₅PS₄.₅Cl₁.₅ · Li₆PS₅Br · Li₆PS₅I · LGPS 의 **233 K Nyquist** (비저항 축) + 등가회로 적합 (빨강 = 호, 초록 = 전극/2차 과정) | 총 비저항 → σ₂₃₃ (§3.7) · I 만 MΩ·cm 단위 |
| S2 | **5종 아레니우스** ln(σT) vs 1000/T (233–333 K, 12 온도) | **LPSCl 펠릿 σ₂₉₈ ≈ 2.5 mS cm⁻¹** (digitized) — 우리 σ_grain 3.0 · `ohno2020` 분포와 같은 자리 (§7) · ⚠ x 축 제목이 SI 원 래스터에서 잘림 |
| S3 | **Li₆PS₅Cl** Γ–X 포논 분산 + 원자사영 DOS, Li 배열 두 개 (a)(b) | 무분산 가지 = 낮은 군속도 = 낮은 κ 의 미시 근거 · 배열 둔감 |
| S4 | **Li₆PS₅I** Γ–X 분산 + 사영 DOS | I 모드가 더 낮은 주파수 |
| S5 | **원자당 c_V(T)** — Li₆PS₅Cl · Li₆PS₅I · LGPS → Dulong–Petit | **LPSCl c_V(298) ≈ 21.1 J mol⁻¹ K⁻¹ = 1.02 J g⁻¹ K⁻¹** (digitized/DERIVED) — 과도 열해석 도입 시 입력 |
| S6 | EMT 5종 κ_eff/κ_SE vs φ_SE (κ_SE 0.5, Ar 0.017, 기공 전도 유무) | 높은 φ 에서 모델 수렴 · 기공 기체 전도 작음 ⇒ 우리 `K_PORE_THERMAL = 0` 근거 (α = 1.5 한정) · ⚠ φ 축 제목 원 래스터에서 잘림 |
| S7 | (a)(c)(e) Li₅.₅ · Br · I 의 **D(T)**, φ 색 구분 · (b)(d)(f) **g 당 c_V(T)** | D 는 ~300 K 까지 감소 후 평평 · **φ 순서가 D 순서와 어긋나는 쌍** (Li₅.₅ 86.8 % < 86.2 % · I 90.5 % < 89.3 % @ 고온) — 밀도 오차 수준 · c_V 판독이 S5 와 0.1 % 로 맞음 |
| S8 | Li₅.₅ · Br · I 의 **κ_eff(T)**, φ 색 구분 (**수동 크롭** — 캡션이 다음 쪽) | Br·I 는 T 와 함께 **증가** (Br 88.8 %: ≈ 0.38 → 0.465 · I 90.5 %: ≈ 0.385 → 0.51, figure-read) · Li₅.₅ 는 ~300 K 부근 오목 · ⚠ 캡션은 "diffusivities" 라 적지만 축은 κ (§11-3) |
| S9 | **Bruggeman 지수 α(T)**, 5종 | α 2.0–3.2 · LPSCl 은 173 K 3.2 → 623 K 2.2 (§3.4) — **우리 모델의 공극 지수 검증 표적** |
| S10 | **173 K** κ_eff vs φ_SE + 적합 — **κ_SE · α 주석** | ★ **LPSCl κ_SE = 0.71 ± 0.04 (α 3.2 ± 0.2)** — 우리 0.7 과 같은 값 · ⚠ φ 축 제목 원 래스터에서 반쯤 잘림 |
| S11 | **523 K** κ_eff vs φ_SE + 적합 | ★ **LPSCl 0.65 ± 0.05 (α 2.7 ± 0.3)** — 온도 의존 약함 |
| S12 | **실온 D_eff vs φ_SE** + 적합 (D_SE · α 주석) + 공극/SE 도식 | ★ **LPSCl D_SE = 0.34 ± 0.02 mm² s⁻¹** → 실온 κ_SE 재구성 0.646 (§0) · 주석의 α 는 식 11 의 (α − 1) |
| S13 | 5종 XRD + Rietveld (합성·구입 직후) | 상순도 · Li₅.₅ 부상 Li₁₅(PS₄)₄Cl₃ 1.9 · LiCl 1.7 wt% |
| S14 | 5종 XRD + Rietveld (**LFA 뒤**) | ⚠ LPSCl 에 LiCl 4.9 + Li₂S 2.2 wt% (R_wp 15 %) · Li₅.₅ 부상 15.2 wt% — "열화 없음" 문장과 긴장 (§11-4·5) |
| S15 | 결정구조 (a) Li₆PS₅X (Li 케이지, 4a/4c 무질서 X/S) (b) LGPS (16h c 축 확산) | 구조 설명용 — 수치 없음 |

## 6. Post-processing ★
- **그들 (SI 범위)**: LFA 신호 → 개량 Cape–Lehman 적합 → D(T) · κ = D·c_p·ρ · 온도별 **Bruggeman 멱법칙 적합** (κ_SE, α; `Figs. S9–S11`) · 실온 D 에 같은 형 (`Fig. S12`) ·
  EMT 5종 비교 (`Fig. S6`) · 포논 DOS → c_V (식 2) · diffuson 기준선 (식 12) · 이온 Lorenz 수로 κ_i 상한 · EIS 등가회로 적합 → 아레니우스.
- **우리가 추가한 것 (DERIVED / digitized — 전부 SI 그림으로 재현 가능)**:
  - **디지타이즈 방법**: SI 의 그림은 "Microsoft Print-to-PDF" 로 **가로 띠 래스터(원 해상도 ≈ 2,900 dpi)** 로 박혀 있다 → 600 dpi 로 렌더 → 안쪽 **눈금선**(축당 3–5개)으로 축 보정 (잔차 < 1 px) →
    **viridis 색 마스크 + 형태학적 침식**(같은 색 적합곡선과 마커를 분리) → 마커 중심. 가려진 마커는 **바운딩박스 가장자리 + 반폭**으로 보정.
    판독 불확도: `Fig. S2` ln(σT) ± 0.03 · `Fig. S5` ± 0.1 J mol⁻¹ K⁻¹ (173 K 부근 경사 구간은 ± 0.3) · `Fig. S7` ± 0.005 J g⁻¹ K⁻¹ · `Figs. S10–S12` φ ± 0.003, κ/D ± 0.003.
  - **닫힘 검산 4개**: ① `Fig. S7` g 당 c_V ↔ `Fig. S5` 원자당 ÷ M̄ (0.1 %) ② Dulong–Petit 선 1.171 / 1.036 / 0.900 ↔ 3R/M̄ 1.169 / 1.036 / 0.901 ③ 실온 κ_eff 재구성 ↔ Ketter SD (0.3 %)
    ④ `Fig. S1` 233 K 비저항 ↔ `Fig. S2` 233 K 점 (5 %).
  - 주석값 **재적합** (비가중 · 오차막대 가중 · 로그-선형) — §3.2.
  - 우리 코드 상수와의 대조 (§7) · 규약 충돌의 크기 φ^α (§0-3).

## 7. 우리 DEM+MPM 대비 ★  →  `our_dem_baseline.md` (⚠ 이 브랜치에선 자리표시 — 우리 값은 작업 브랜치 코드에서 인용)
우리 값의 출처: 작업 브랜치 `claude/stoic-knuth-NObVQ` @ `e8c4ea84c` (2026-09-25) — `scripts/network_conductivity.py:132` `K_SE_THERMAL = 0.7e-2  # W/(cm·K) ≈ 0.7 W/(m·K), LPSCl (Ketter 2025)` ·
`scripts/step3_sigma.py:1035–1041` (K 표; `K_PORE_THERMAL = 0.0` "[ASSUMED; 가스면 ~2.6e-4]") · `scripts/mpm_webapp_payload.py:2579–2581` (trust 문자열 "SE=Ketter2025(LPSCl) 문헌앵커") ·
`scripts/network_conductivity.py:1545` (selftest *"thermal prefactor untouched (no κ(T) anchor, §F1)"*). 원장 `SELF-51` (작업 브랜치 `docs/reviews/findings.json`).

| 항목 | 이 논문 (SI) | 우리 | 같음/다름 · 이유 |
|---|---|---|---|
| **κ_SE 값** | 치밀 외삽 **0.71 ± 0.04 (173 K) · 0.65 ± 0.05 (523 K)** (SI-in-figure) · 실온 재구성 **0.646 ± 0.038** (DERIVED) · 본문 인용값 0.66 [본문 미확인] | **0.7 W m⁻¹ K⁻¹** (두 솔버 공통) | **같다** — 173 K 값과 일치, 실온 재구성 대비 +8 % (+1.4σ). **양의 종류도 같다**: 둘 다 **공극을 뺀 고체상** 값이고, 우리 솔버는 공극(복셀)·접촉(망)을 따로 둔다 |
| **출처 라벨** | Böger 2023 SI `Figs. S10–S12` | "Ketter 2025 (LPSCl)" — Ketter 의 LPSCl 은 **0.32 (펠릿)**, 0.71 은 **NCM83** (정본 ketter 카드 §0) | **라벨 오귀속 확정 → 교체 대상.** 값은 방어되나 근거 문헌이 다르다 |
| 양의 **정확한 정의** | φ 0.75–0.91 펠릿 6개에 **멱법칙 κ_eff = κ_SE φ^α 를 φ → 1 로 외삽** — 단결정 아님 · **15 min 소결** 펠릿 · 외삽 거리 Δφ ≈ 0.09 | "LPSCl 고체상" (정의 없음) | ⚠ 치밀 **다결정** 외삽값이지 입내(grain-interior)/단결정이 아니다. 소결이 목(neck)을 키웠다면 **냉간압밀인 우리 전극보다 높게** 잡힌 값일 수 있다 — 같은 그룹 냉간·등방 펠릿(Ketter)은 같은 φ 에서 0.74× (§0-2, 추론) |
| **온도 의존** | LPSCl κ_SE 173 → 523 K **−8 %** (오차 안) · 다른 4종 −2 … +41 % · 1/T 아님 | κ_SE **상수** (κ(T) 없음; selftest 가 "no κ(T) anchor" 라 적음) | **상수 가정이 지지된다** — 이제 **앵커가 있다** (173 · 523 K + 실온 재구성). 운전 온도(25–60 °C) 창에서 κ_SE 변화는 **1 % 미만** (추론; 173·523 K 두 점 선형 보간 — 주석 오차 ±6–8 % 보다 작다) |
| **기공의 기체 전도** | Ar 0.017 · 모델 비교상 영향 작음 (α = 1.5) | `K_PORE_THERMAL = 0` | **정합** — 단 α ≈ 2.9 로 식 8 을 풀면 φ 0.85–0.90 에서 기체 기여 **+2.4–4 % (Ar) / +3.6–6 % (N₂·공기 0.026)**, φ 0.75 에서 +9–13 % (DERIVED). ⇒ 우리 0 가정은 κ_eff 를 **최대 수 % 과소** (다공 쪽일수록 커짐) |
| **공극 지수 α** (미세구조 벌점) | **α 2.7–3.2** (LPSCl), 2.1–3.2 (5종) — 이상 구형 1.5 보다 훨씬 큼 | 두 솔버 모두 α 를 **입력하지 않는다** — 미세구조에서 **창발** | ★ **검증 표적** (frame[4]): 순수-SE 침대의 κ_eff/κ_SE vs φ 가 φ^~2.9 를 재현하는가. STEP3 는 접촉 저항 0 (`CL-81` CONTACT_FREE) 이라 **더 작은 α (이상 1.5 쪽)** 를 낼 것으로 **예상** — 그 차가 **열 채널의 협착 결손 크기**다 (미실행, §8-②) |
| **c_p** | Li₆PS₅Cl 1.02 J g⁻¹ K⁻¹ (298 K, 계산 c_V) | 코드에 c_p **없음** (정상상태 κ 만) | 무관 — 과도 열해석(Joule ΔT(t)) 도입 시 입력 후보 |
| **이온 열전도** | ≤ 0.012 W m⁻¹ K⁻¹ (고온 상한) · 실온 4 × 10⁻⁵ | 항 없음 | **정합** (무시 정당) |
| **펠릿 σ_ion** | 같은 상용 LPSCl, 단축 370 MPa 3 min · 가압셀 10 Nm · **σ₂₉₈ ≈ 2.5 mS cm⁻¹** (digitized) · E_a ≈ 0.38–0.42 (digitized) | σ_grain **3.0 mS cm⁻¹** (µC 펠릿 고적층압 평탄, `cronau2021` SI) · E_a 밴드 0.29 / 0.41 / 0.46 | 2.5 는 `ohno2020` 8 랩 분포(0.44–2.98) 안, 우리 3.0 의 0.83× — **한 편 더의 펠릿 total 값** (규약 판정에는 새 정보 없음; 적층압 MPa 미기재) |
| **SE 두 입력의 규약** | 이 논문 자신도 **σ = 펠릿 total**, **κ = 치밀 외삽** (한 편 안에서 규약이 다르다) | σ_grain 3.0 = 펠릿 (`cronau2021` SI), κ_SE 0.7 = 치밀 (이 카드) | ⚠ **어긋남은 그대로다** — 이 SI 는 κ 쪽의 크기만 준다 (φ 0.88 에서 치밀/펠릿 = 1/φ^α ≈ **1.4–1.5**). σ 쪽 배율은 이 SI 로 **정할 수 없다** (§7-2) |
| 채널 | κ 만 (+ 보조 σ_ion) | σ_ion · σ_e · κ | 우리 삼중항 중 **κ 입력 하나**와 **κ 의 공극 벌점** 검증에 걸린다 |
| frame[5] | 입력층 + 검증 표적 | κ 는 접촉망(DEM)·복셀 FV(MPM STEP3) **둘 다** 낸다 | κ_SE 절대 불확실도는 두 솔버의 절대 κ 에 **공통모드**로 들어가고, 같은 κ_SE 를 쓰는 **상대비교에서는 상쇄**된다 |

### 7-2. 규약 충돌 — 이 데이터가 말하는 것과 말하지 못하는 것
- **말하는 것**: 열 채널에서 "펠릿 κ" 와 "치밀 κ" 의 차는 **φ^α** 이고, LPSCl 에서 α ≈ 2.7–3.2 라 φ = 0.88 에서 **0.66–0.71** 이다. 우리 솔버는 공극을 명시하므로
  κ 는 **치밀 규약이 맞다** (펠릿값 0.32–0.44 를 넣으면 공극 벌점을 **이중계상** — Ketter 카드 선택지 C 와 같은 결론).
- **말하지 못하는 것**: σ_ion 의 치밀값. 이 SI 의 σ 는 **펠릿 total 하나** (밀도 미기재)이고 σ(φ) 계열이 없다. 이온의 공극 지수는 열과 같을 이유가 없다 —
  입계 이온 저항과 열 경계저항(Kapitza)은 다른 물리이고, 크기 계층도 다르다. ⇒ *"κ 가 치밀이니 σ_grain 도 1/φ^α 로 올리자"* 는 **이 SI 로 정당화되지 않는다.**
- ⇒ 규약 통일(Ketter 카드 선택지 D)은 여전히 **1저자 결정**이다. 이 카드가 보태는 것: ① κ 는 치밀 규약으로 **출처가 섰다** ② 펠릿↔치밀 차의 **열 채널 크기**는 ~30 % 다
  ③ σ 쪽 크기는 여전히 **n/a** (σ 의 치밀값이 필요하면 σ(φ) 계열이 있는 다른 원문이 필요).

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **`K_SE_THERMAL` 라벨 교체 (값 유지)** — 제안 문구: *"0.7 W/(m·K): dense (pore-free) Li₆PS₅Cl, Bruggeman-extrapolated from LFA pellet series —
  Böger et al. 2023 SI Figs. S10–S11 (0.71 ± 0.04 at 173 K, 0.65 ± 0.05 at 523 K; RT ≈ 0.65 reconstructed from SI Fig. S12). NOT Ketter 2025 (0.32 there is a porous pellet; 0.71 is NCM83)."*
  ⚠ DOI 는 미확인 — 서지는 Ketter 2025 ref 30 형식으로만.
- ② **순수-SE 침대로 α 를 잰다 (새 검증, frame[4])** — MPM 순수-SE 침대(또는 real_14 류에서 SE 만)의 공극률을 바꿔 가며 STEP3 κ_eff/κ_SE 를 풀고 멱지수를 적합 → **실험 α 2.7–3.2 (LPSCl)** 와 대조.
  예상(추론): CONTACT_FREE 복셀은 α ≈ 1.5–2 → 실험 대비 κ 과대 (φ 0.9 에서 0.9^1.5/0.9^2.9 ≈ **1.16×**). 그 차가 **열 채널의 목/접촉 결손 크기**이고, CL-81 의 이온 채널 논의와 **같은 구조의 두 번째 증거**가 된다.
  접촉망(DEM) κ 도 같은 표적으로 잰다 — 두 솔버가 α 를 어떻게 내는지가 frame[5] 의 κ 분업 근거가 된다.
- ③ **`K_PORE_THERMAL = 0` 의 오차 한계 문장** — *"기체 전도 무시는 κ_eff 를 φ_solid ≥ 0.85 에서 ≲ 4–6 % 과소 (Bruggeman 일반형, α ≈ 2.9, Ar/N₂)"* (DERIVED).
- ④ **κ(T) 앵커** — selftest 의 *"no κ(T) anchor"* 를 *"κ_SE(T) 평평: 173 → 523 K −8 % (Böger SI)"* 로 갱신할 근거. 상수 κ 유지 (값 변경 없음).
- ⑤ **"치밀 LPSCl κ" 불확실도 밴드** — 원고·SI 표에서 **0.46–0.71** (Ketter 배치 가정 의존 ~ Böger) 로 적거나, 최소한 *"같은 그룹의 다른 배치 펠릿은 같은 밀도에서 0.74×"* 를 각주로.
- ⑥ **c_p (과도 해석 대비)** — Li₆PS₅Cl 0.80 / 1.02 / 1.14 J g⁻¹ K⁻¹ @ 173 / 298 / 523 K (계산 c_V, digitized/DERIVED).
- ⑦ **LPSCl 펠릿 σ 한 점 추가** — 상용 LPSCl · 370 MPa · 가압셀 → σ₂₉₈ ≈ 2.5 mS cm⁻¹ (digitized). `ohno2020` §8-④ 의 **프로토콜 꼬리표** 규율대로: 성형 370 MPa 3 min · SS 스탬프 · 토크 10 Nm (MPa 미기재) · 밀도 미기재 · 233–333 K.

## 9. 인용 가능 문장 (deck/paper용)
- (EN, 우리 κ_SE — SI 근거) *"The solid-phase thermal conductivity of Li₆PS₅Cl used in both transport solvers (0.7 W m⁻¹ K⁻¹) corresponds to the dense, pore-free value obtained by
  Böger et al. from a Bruggeman extrapolation of laser-flash measurements on pellets with 75–91 % relative density (0.71 ± 0.04 W m⁻¹ K⁻¹ at 173 K and 0.65 ± 0.05 W m⁻¹ K⁻¹ at 523 K;
  Supporting Information of ref. [Böger 2023])."* — ⚠ 서지는 Ketter 2025 ref 30 형식, **DOI 미확인**.
- (EN, 공극 벌점) *"For Li₆PS₅Cl, the effective thermal conductivity of porous pellets scales as φ^α with α ≈ 2.7–3.2, well above the value of 1.5 expected for spherical inclusions [Böger 2023, SI]."*
- (EN, 이온 기여) *"The ionic contribution to heat transport is negligible (≤ 0.012 W m⁻¹ K⁻¹ even at the highest measurement temperature) [Böger 2023, SI]."*
- ⛔ *"Böger 2023 reports 0.66 W m⁻¹ K⁻¹ for Li₆PS₅Cl"* 는 **본문 확인 전 쓰지 말 것** — SI 에 그 숫자가 없다 (Ketter 2025 가 그 값을 인용했다는 사실만 인용 가능).

## 10. 주의/한계 (over-claim 방지)
- **SI 만** — 실온 κ_SE · E_a · κ(T) 해석 · 조성 서열의 기전은 본문에 있다. 본문이 SI 그림과 다른 적합 방법을 쓸 수 있다 (재적합에서 가중 방식에 따라 κ_SE 가 0.64–0.66 사이에서 움직인다).
- **치밀 외삽값**이다 — 단결정·입내값이 아니고, φ 0.91 → 1.00 을 **멱법칙으로 외삽**한 값이다. 멱법칙이 치밀 극한까지 성립하는지 SI 는 보이지 않는다.
- **소결 펠릿** — 냉간압밀 복합 전극의 SE 상과 목(neck) 상태가 다를 수 있다. 같은 그룹 다른 배치(Ketter, 등방 500 MPa)와 **같은 φ 에서 26 % 차** — 배치·전처리 의존이 크다.
- **c_p 는 계산값** (측정 아님) — κ 는 c_p 에 선형이다. c_V ↔ c_p 차는 ≤ 2 % (§3.5) 이지만, 포논 모델 자체 오차는 SI 에 정량되지 않았다. ρ 는 **기하밀도** (φ 오차 ± 2 % 급, Ketter SD `xerr = 2`).
- **상용 LPSCl** — 공급사·입도·결정도 미기재 · **LFA 뒤 LiCl 4.9 + Li₂S 2.2 wt%** (§11-4) · 623 K 까지 가열된 흔적(α 점).
- **순수 SE 펠릿** — 복합체(AM + SE + 첨가제) κ 는 이 논문 밖 (그 짝은 정본 `ketter2025`). 할라이드·산화물·Li₃PS₄ 는 **이 SI 에 없다** (본문 비교 문헌표 여부 [본문 미확인]).
- **digitized 값은 TREND 전용** — 자릿수 이상의 정밀도로 인용하지 말 것 (§6 의 불확도).

## 11. SI 내부 불일치·모호 (감사 — κ_SE 주석값에는 영향 없음)
1. `Fig. S2` 캡션: *"temperature range from 233 K to 273 K"* ↔ 그림의 점·실험절(p. S6): **233–333 K** (12 온도).
2. Section S9 끝 (p. S17): *"The acquired diffractograms and the corresponding Rietveld refinements are shown in Figures S1 and S2"* → 실제로는 **`Figs. S13–S14`** (S1–S2 는 Nyquist/아레니우스).
3. **`Fig. S8` 캡션 = "thermal diffusivities"** 인데 세 패널의 y 축은 모두 **κ / W m⁻¹ K⁻¹** — 캡션 오기 (내용상 열전도도). x 축 제목도 없다.
4. `Fig. S14` 캡션 *"No significant degradations occur"* ↔ 같은 그림의 **Li₆PS₅Cl: LiCl 4.9 wt% · Li₂S 2.2 wt%, R_wp 15 %, gof 3.5** (LFA 전 `Fig. S13` 은 부상 표기 없이 R_wp 7.3 %, gof 1.4).
   LFA 전 부상이 정련되지 않았던 것인지, LFA 중 생긴 것인지 SI 는 가르지 않는다. (argyrodite ≥ 93 wt% 로 텍스트의 "> 85 wt%" 는 만족.)
5. Li₅.₅PS₄.₅Cl₁.₅ LFA 뒤 부상 **Li₁₅(PS₄)₄Cl₃ 9.5 + LiCl 5.7 = 15.2 wt%** ⇒ argyrodite **84.8 wt%** (DERIVED) — 텍스트의 **"> 85 wt%"** 경계에 걸린다 (반올림 문제일 수 있음). LFA 전 3.6 wt% → 후 15.2 wt% (4.2×).
6. `Fig. S9` 캡션 *"constant within uncertainty"* ↔ LPSCl **3.21 (173 K) vs 2.19 (≈ 623 K)**, I **2.40 (198 K) vs 3.16 (473 K)** — 오차막대 (± 0.2–0.4) 가 겹치지 않는 쌍이 있다 (digitized).
   또 `Fig. S9` 의 I 173 K 점 ≈ 2.52 ↔ `Fig. S10` 주석 2.4 ± 0.2 (0.12 차, digitized).
7. `Fig. S12` 의 적합식 표기 *"D_eff = D_SE φ^α"* — 식 11 에 따르면 여기 α 는 **(α_κ − 1)** 이다. 같은 기호를 두 뜻으로 썼다 (수치는 §3.2 닫힘 검산대로 정합).
8. Section S1 (p. S2) 문장 *"instead of a simple ohmic resistance was used instead of the second semicircle"* — 문장이 꼬여 있다 (뜻: 두 번째 반원 대신 **단순 옴 저항**).
9. p. S4 *"All samples were sintered for 15 min at their respective synthesis temperature"* — **상용 Li₆PS₅Cl 의 합성온도는 정의되지 않는다** (값 미기재). LPSCl 만 ≈ 623 K 점이 있다.
10. `Fig. S2` · `Fig. S6` · `Figs. S10–S11` 의 x 축 제목이 **SI 원 래스터 안에서** 잘려 있다 (래스터 끝 = 캡션 시작 직전) — 복구 불가, 우리 크롭 결함 아님.
11. p. S4 "Power X-ray diffraction" (Powder 오기) · `Fig. S15a` 범례 "(4c)(16e)" 겹침 — 표기 문제.
12. p. S8 의 체적탄성률 "1.5 GPa (ref 18 Kraft 2017)" — 정본 `kraft2017` 카드는 *"Kraft 는 B/G 를 따로 보고하지 않음 (speed of sound · Debye · C_ij 만)"* 이라 기록한다.
    그 카드의 figure-read 음속 (v_L ≈ 1480, v_T ≈ 1050 m s⁻¹, 85 % 펠릿 ρ ≈ 1.58 g cm⁻³) 으로 B = ρ(v_L² − 4/3 v_T²) ≈ **1.1–1.2 GPa** (DERIVED) — "1.5 GPa" 는 **같은 자릿수의 펠릿 유도값**으로 보인다 (추정; Kraft 원문 대조 필요).
- ⇒ **Li₆PS₅Cl 의 κ_SE · α · D_SE 주석값은 전부 재적합·닫힘 검산으로 재현된다.** 이 카드의 결론에 걸리는 불일치는 없다.

## 12. 다른 카드의 2차 인용 대조 (SI 로 판정할 수 있는 범위)
| 카드 (정본) | 적힌 말 | SI 판정 |
|---|---|---|
| `ketter2025_resistor_network_models_predict_transport_properties` §0 · §3 표 (L136) · §10-13 · §14 | "치밀 LPSCl 입력 **0.66 (Böger 2023 — 미확인)**" · "Böger 실측점 6개 (φ 75.4–90.9 %) 0.269–0.498" · "0.66 이 무엇인지 (치밀 외삽? 별도 시료?)" | **0.66 은 SI 에 없다** (본문 값으로 추정). SI 로 재구성한 실온 κ_SE = **0.646 ± 0.038** · 로그-선형 재적합 **0.661** ⇒ **"치밀 외삽(실온 Bruggeman 적합)"** 쪽으로 판정 (추론). 6점 0.269–0.497 은 SI `Fig. S12` 로 **0.3 % 안에서 재현** ✓ |
| 같은 카드 §3 표 (L73) | "C_V 0.798 (173 K) · **1.022 (298 K)** · 1.081 (373 K) J g⁻¹ K⁻¹ — LPSCl = Böger 의 포논 계산" | ✓ `Fig. S5` / `Fig. S7` 판독 **0.80 / 1.02** (173 / 298 K) — 일치 |
| 같은 카드 §0 (L27) | "Ketter 펠릿을 RN 기공 모델로 치밀 쪽에 되돌리면 ≈ 0.44 (모델 의존)" | Böger 의 **α 2.7–3.2** 로 되돌리면 **0.46–0.49** (DERIVED) — 같은 결론(0.44–0.49 대)이 **다른 경로**로 나온다. "치밀 LPSCl κ 0.44–0.71" 폭은 유지 |
| `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` §(C_ij 주의) | "Kraft 는 B/G 를 따로 보고하지 않음" | 이 SI 는 Kraft 를 **"실험 체적탄성률 1.5 GPa"** 의 출처로 인용 — 긴장 (§11-12). 그 카드는 **다른 세션 소관이라 고치지 않았다** |
| `comparison_vs_ours.md` §H `[Ling26]` 행 | "LPSC 필름 α(열확산) 0.174 / 0.189 mm² s⁻¹ · k ≈ 0.22 W m⁻¹ K⁻¹ (우리 환산)" | 크기 대조만 (다른 시료·다른 기하): Böger LPSCl 펠릿 실온 D_eff **0.19–0.29 mm² s⁻¹** (φ 0.75–0.91) · 치밀 D_SE 0.34 — Ling 필름 값은 Böger 계열의 **φ ≈ 0.69–0.76** 자리 (DERIVED: D_eff = 0.34 φ^1.8 역산 0.69–0.72 · 최근접 실측점 φ 0.755 → 0.1875) |

## 13. 용어 (mini-glossary)
- **LFA (laser flash analysis)** — 얇은 원판 한쪽을 레이저 펄스로 가열하고 반대쪽 적외 신호의 상승곡선으로 **열확산 D** 를 얻는다. κ = D · c_p · ρ.
- **Cape–Lehman (개량)** — 유한 펄스 폭·열손실을 넣은 LFA 신호 해석 모델.
- **Bruggeman 지수 α** — κ_eff = κ_SE φ^α 의 α. 구형 개재물 이론값 1.5; 실제 압분체는 목·접촉·공극 형상 때문에 더 커진다 (여기 2.1–3.2). 열확산은 α − 1.
- **치밀 외삽 κ_SE** — 다공 펠릿 계열의 적합을 φ = 1 로 외삽한 값. 공극 벌점은 빠지지만 **입계 열저항은 남을 수 있다** — 단결정 κ 가 아니다.
- **Dulong–Petit 한계** — 고온에서 c_V → 3R (원자 1 mol 당 24.94 J mol⁻¹ K⁻¹).
- **phonon-gas vs diffuson** — 결정의 포논 기체(움클랍 산란 → κ ∝ 1/T) vs 무질서계의 **확산적 진동 에너지 전달**(κ 가 T 에 둔감·증가). diffuson 모델의 P 는 "에너지 전달 성공 확률".
- **이온 Lorenz 수 L_i** — 이온 전도가 나르는 열을 σ_i 로 환산하는 계수 (Wiedemann–Franz 의 이온판).
- **Kapitza (계면 열)저항** — 입계·접촉을 가로지를 때의 온도 불연속 저항. 우리 STEP3 κ 라벨의 "Kapitza 무시 → 상한" 과 같은 것.

## 14. 본문 확보 시 채울 것 (TODO)
- **실온 κ_SE 5종 (본문 수치/그림)** — 특히 LPSCl **"0.66"** 의 정의·적합 방법 (로그-선형인지 가중인지) 과 ± 의 정의.
- **서지 확정** — 권·쪽·DOI (`10.1021/acsaem.3c01977` 추정) · 출판 제목.
- 본문 `Fig. 1a` 의 **E_a** (stated) · LPSCl 233 K Nyquist · 본문 `Fig. 5` κ(T) 와 diffuson 적합 P · 조성 서열(Cl > LGPS > Cl-rich > Br ≈ I @ 173 K)의 **기전 설명**.
- 펠릿↔성형법 대응 · LPSCl 공급사·소결 온도 · 문헌 비교(할라이드·산화물) 여부.
- 본문 그림을 받으면 `extract_figures.py --slug boger2023_thermal_conductivity_argyrodite_lgps --pdf <본문> --pdf <SI>` — ⚠ **`--clean` 금지** (S8 수동 크롭 · S1/S6 재크롭이 사라진다, `pdf_map.tsv`).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
