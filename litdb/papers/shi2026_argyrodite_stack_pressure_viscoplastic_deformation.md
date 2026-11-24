<!-- 2026-11-24 litdb-curator (병렬 배치 · 이 편에서 쓴 파일 = 이 digest + litdb/figures/<slug>/ 둘뿐).
     크롭 25장 (도구 24 + 손 크롭 tab_S2 1) 중 그림 10장을 Read 로 실독 + 패널 확대 3장 (Fig. 2C 길이 · Fig. 2D · Fig. 5D).
     SI3 (MATLAB 스크립트 3 + .mat 29) 를 읽기만 해서 Fig. 2C · Fig. 5D 를 다시 냈다 (§8b) — 데이터는 litdb 로 복사하지 않았다. -->

# Stack pressure effects and viscoplastic deformation in argyrodite solid-state electrolyte — Shi et al. (*Matter* **2026**, 9, 102767)

> slug `shi2026_argyrodite_stack_pressure_viscoplastic_deformation` · DOI `10.1016/j.matt.2026.102767` · type `exp + FEM (Li/LPSCl/Li 대칭셀 CCD · 영전류 유지 · nanoindentation · Vickers indentation · 차단전극 ASR · cryo-FIB-SEM 공극 영상분석 · Abaqus UMAT 점소성 역해석 · 공극 contact FEM · 균열 J-적분 — 원자단위 계산 없음)` · PDF `litdb/inbox/viscoplastic2026_argyrodite_stack_pressure_main.pdf` (본문 17 pp) + `…_SI1.pdf` (SI 23 pp · Fig. S1–S14 · Table S1–S3 · Video S1–S4 설명) + `…_SI2.pdf` (2 pp · Cell Press 배터리 표준 보고 양식) + SI3 코드 (`litdb/inbox/shi2026_sup3/codes/` · git 무시 · §8b) · digested `2026-11-24` · status ✅ · 태그 **[외부]**
> elements: Li, P, S, Cl
> methods: elastic, Raman

> **저자**: Changmin Shi\* (Brown Univ. School of Engineering → Syracuse Univ. MAE) · Yixian Wang (UT Austin) · Xing Liu (Brown → NJIT) · Cristina López-Pernía (Brown) · John Watt (LANL · CINT) · Chenjie Gan (Brown) · Aleksander Mijailovic (Brown) · Pradeep R. Guduru (Brown) · David Mitlin\* (UT Austin) · **Brian W. Sheldon\*** (Brown · lead contact). 교신 3 인 (Shi · Mitlin · Sheldon).
> 접수 2025-06-25 · 수정 2025-09-23 · 채택 2026-03-13 · 온라인 2026-04-10 · 권호 *Matter* 9, 102767 (2026-07-01) · © Elsevier (OA 아님 · TDM/AI 훈련 금지 문구) · 자금 DOE Battery500 · Welch Foundation F-2206 · ONR (Guduru) · **SK On** (Brown 쪽) · 이해충돌 없음 신고.
> 기여: 개념·실험 설계 Shi · Sheldon / 전기화학 Shi / 역학 실험 López-Pernía / 현미경 Wang · Watt / 모델링 Liu · Gan. SI3 의 `script_for_pore.m` 머리말 "develop by Chenjie" = Chenjie Gan.
> Jeff Sakamoto 는 **저자가 아니다** (참고문헌 15 · 19 · 44 에만 공저자로 나온다).
>
> **계보 (같은 Sheldon–Guduru 그룹)**: Athanasiou 2022 *Cell Rep. Phys. Sci.* (황화물 **유리** 점소성 · 압입 FEM 역해석의 원전 · ref 20 · litdb 없음) → `[Song25Mech]` `song2025_porous_argyrodite_modulus_fracture_toughness` (**같은 펠릿 공정** 1 µm · 360 MPa · 60 °C 2 h · 기공 13 ± 2 % · mm 스케일 E 4.7 GPa · K_Ic 0.17 MPa·m^½ · ref 38) → **본 논문** (그 펠릿의 점소성 + Li\|LPSCl 계면 공극 닫힘 + 스택압 · 유지 운전 프로토콜).

---

## 0. 이 digest 를 읽는 법

**축**: DEM · 연속체 (역학 · 접촉 · 크리프) 다. webapp `literature_track()` 판정 = `dem` (slug · type · 제목 낱말 점수 dem 3 [`fem` · `contact` · `indentation`] 대 dft 1 [`argyrodite`]) → `INDEX_DEM.md` 생성 표에 자동으로 실린다 (묶음은 제목에 묶음 낱말이 없어 '기타'). 원자단위 계산은 **없다**.

이 논문이 우리에게 주는 것은 셋이다.
1. **Li₆PS₅Cl 의 점소성 구성식 상수** (`Table 2` · 식 1) — 우리 계와 같은 전해질. DEM 접촉 소성 · 연속체 SE 층에 바로 넣고 싶은 값이다 → §3a 에 **원문 표 그대로** 모았다.
2. **Li\|LPSCl 계면 공극의 시간 변화 통계** (`Fig. 2C–D` · `Fig. 5D`) + 그 **원자료 (SI3)** — 8 MPa 에서 영전류 유지 0 → 12 min → 1 h → 5 h 동안 공극 길이 · 폭 · 밀도 · 면적 분율. W_ad 보고서 7 절 (점착과 공극) 의 실험 대조 표적.
3. **공극 · 덴드라이트 FEM 세 가지** — 탄성 응력 집중 (`Fig. 5B–C`) · Li 항복에 따른 접촉률 (`Fig. 5E–F`) · 균열 구동력 G_net 의 유지 중 완화 (`Fig. 6`).

**값을 쓰기 전에 알아둘 것 넷** (상세 §10).
- ① `Table 2` 의 **E 22.1 GPa · ν 0.30 은 측정이 아니라 문헌값**인데, 그 인용 (ref 37) 이 **Abaqus 사용자 매뉴얼**이다. 22.1 GPa 는 Deng 2016 DFT (조밀 단결정 · PBEsol · `deng2016_elastic_superionic_electrolytes_dft`) 의 Li₆PS₅Cl E 와 같은 수이고, ν 는 Deng 의 0.37 과 다르다. 같은 그룹 · 같은 펠릿 공정의 `[Song25Mech]` 은 mm 스케일 **E 4.7 ± 1.1 GPa** 를 쟀다.
- ② **Y_SE 0.35 GPa · ε̇₀ 1×10⁻⁵ s⁻¹ · n 4** 는 20 mN Berkovich 압입의 **40–60 s 유지 구간 '상대 깊이 변화'** 에 맞춘 값이다 (`Fig. S10` · 표면 거칠기 때문에 절대 깊이를 버렸다고 저자가 밝힌다). 식 1 은 **과응력 꼴**이라 σ < Y_SE 에서는 소성 흐름이 0 이다 ⇒ **스택압 (수 MPa) 에서의 LPSCl 크리프는 이 식으로 낼 수 없다** (저자도 차단전극 ASR 감소를 *"나노압입이 못 보는 더 느린 과정"* 이라 쓴다, p.11).
- ③ 저자 결론상 5 h 동안 공극을 닫는 주체는 **Li 쪽 확산 크리프 (Coble)** 이고, LPSCl 은 공극 끝에서도 **탄성** (최대 116 MPa < 350 MPa) 이다. "SE 가 점소성이라 공극이 닫힌다" 로 읽으면 틀린다.
- ④ 본문 · 캡션 · 그림 사이에 **패널 번호 · 압력 (8 vs 10 MPa) · 정의 어긋남이 여럿** 있고, SI3 로 다시 내 보면 `Fig. 5D` 는 8 점 중 6–7 점이 맞지만 **`Fig. 2D` 는 Methods 정의로 재현되지 않는다** (§8b · §10).

> **본 digest 에서 실제로 본 그림 (Read · 2026-11-24)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. S10` `Fig. S11` `Fig. S12` `Fig. S14` — **10장** (+ 확대 3장: `Fig. 2C` 길이 · `Fig. 2D` · `Fig. 5D`).
> 안 본 것: `Fig. S1`–`Fig. S9` (열처리 EIS · XRD · Raman · SEM · CCD · 단면 석출 — 값은 SI 본문 글자에서) · `Fig. S13` (Video S4 기하) · 표 5장 `Table 1` `Table 2` `Table S1` `Table S2` `Table S3` (PDF 글자가 더 정확 — 이미지는 안 읽었다).
> 그림에서만 읽은 값은 **`figure-read ≈`**, SI3 원자료에서 다시 낸 값은 **`[SI3 재계산]`**, 논문에 없는 우리 산수는 **`[우리 산술]`** 로 표시했다.

---

## 1. 한 줄 요약

Li\|Li₆PS₅Cl\|Li 대칭셀을 3–8 MPa 스택압에서 돌리면서 반주기마다 **영전류 유지 (12 min · 1 h · 5 h)** 를 넣으면 CCD 가 유지 시간 · 압력과 함께 커져 **8 MPa · 5 h 에서 최고 4.8 mA/cm²** (막대 평균은 figure-read ≈4.2) — 같은 압력 무유지 **1.8–2.4** 의 2–3 배다. 같은 유지 동안 cryo-FIB-SEM 으로 본 계면 공극은 **길이가 ≈2 µm → ≈0.7 µm** 로 줄고 (폭 ≈0.2–0.3 µm 는 거의 그대로) 면적 분율이 **figure-read ≈14–16 % → ≈2.3 %** (5 h) 로 떨어지며, 계면 저항 R_SEI+CT 가 figure-read **≈11.4 → ≈9.9 Ω·cm²** 로 준다. 저자 해석은 *"닫힘에 수 시간이 걸린다 → Li 의 고전 소성 (항복 0.7–0.8 MPa · FEM 상 수 초 이내) 이 아니라 **Li 의 확산 크리프 (Coble · 8 MPa · d 100 µm 에서 2.1×10⁴ s)** 가 지배하고, 공극 벽 Li 는 SEI 때문에 더 단단하다"* 이다. LPSCl 자체는 나노압입에서 점소성 (**Y_SE 0.35 GPa · ε̇₀ 10⁻⁵ s⁻¹ · n 4**) 이고, 차단전극 ASR 이 8 MPa 5 h 동안 figure-read **≈5 %** (5 MPa ≈2.5 %) 줄어 저응력의 느린 변형도 시사하지만, 성능 향상의 주된 원인은 아니라고 본다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | **Li₆PS₅Cl (NEI Corp. 분말, 입경 ≈1 µm)** 펠릿 — 360 MPa · 4 min 상온 일축 압축 → 60 °C (주 시편) · 100 · 250 °C 2 h 후열처리. 대조 = **LLZTO** (Li₆.₄La₃Zr₁.₄Ta₀.₆O₁₂, Toshima) |
| 셀 | Li 박 (100–250 µm) 양쪽 대칭셀 · MTI split cell · 하중 센서로 스택압 제어 · 상온 |
| 던지는 질문 | 스택압의 효과는 **압력 크기만이 아니라 시간 (점소성 · 속도 의존 변형)** 에서 오는가? 그렇다면 **어느 재료의 어떤 기전**인가 (Li 의 저항복 소성 · Li 의 크리프 · SE 의 점소성)? |
| 문헌 갭 | ① 쓰이는 스택압 (3–10 MPa) 이 Li 항복 (0.7–0.8 MPa) 보다 한 자릿수 큰데 "Li 의 낮은 항복 → 접촉 개선" 가설은 제대로 시험된 적 없다 (p.2) ② argyrodite 의 속도 의존 변형 자료가 거의 없다 (p.5) ③ Li₆PS₅Cl 의 항복응력은 보고된 적 없다 (p.2 — 저자 주장) |
| 접근 | 전기화학 (유지 시간 · 압력 매트릭스 + 준사인파 프로토콜) → 공극 영상 (cryo-FIB-SEM · 유지 시간별) → SE 역학 (나노압입 · Vickers · 차단전극 ASR) → FEM (탄성 응력 · 소성 접촉 · 균열 G_net) → Li 크리프 기전 시간 비교 (Table S1–S2) |
| 결론 | 공극 닫힘 = **Li 확산 크리프 (Coble)** 가 지배 · LPSCl 점소성은 고응력 자리 (덴드라이트 끝 · 입자 접점) 에서 의미 |

---

## 3. 핵심 수치 총정리 ★

### 3a. ★ DEM · 연속체 입력표 — **원문 표 · 문장 그대로**

**(1) `Table 2` "Li6PS5Cl mechanical properties" (본문 p.8)** — 원문 그대로:

| E (GPa) | ν | Y_SE (GPa) | ε̇₀ | n |
|---|---|---|---|---|
| 22.1 | 0.30 | 0.35 | 0.00001 | 4 |

- 구성식 (식 1, p.7): **σ / Y_SE = (1 + ε̇ᵖ / ε̇₀)^(1/n)** — σ = 등가 인장응력 (von Mises) · Y_SE = 정적 항복강도 · ε̇₀ = 기준 변형률 속도 (단위 표기 없음 — 식의 꼴상 s⁻¹) · n = 변형률 속도 경화 지수. 탄성부는 선형 (E · ν 는 문헌값, ref 37 = Abaqus 매뉴얼 — §10-①).
- 역으로 풀면 **ε̇ᵖ = ε̇₀ [(σ/Y_SE)ⁿ − 1]** (σ > Y_SE 일 때만) [우리 산술]: σ = 1.1 Y → 4.6×10⁻⁶ s⁻¹ · 1.5 Y → 4.1×10⁻⁵ s⁻¹ · 2 Y (0.70 GPa) → 1.5×10⁻⁴ s⁻¹ (1 h 에 ε ≈ 0.54). **σ ≤ 0.35 GPa 에서는 0** — 스택압 영역의 LPSCl 크리프는 이 식 밖이다.
- 맞춘 자료: Berkovich 20 mN · 5 mN/s · 유지 40 s (+ `Fig. S10` 에는 60 s 유지 곡선도 있다) · 0.2 mN 까지 제하 후 90 s 유지 · 4 표면 · 간격 > 150 µm · 광유 속. **절대 깊이가 아니라 유지 · 제하 단계의 상대 깊이 변화**에 맞췄다 (p.14, `Fig. S10`).
- 모델: Peirce 형 대변형 탄–점소성 UMAT (Abaqus) · 강체 Berkovich (65.3°) 마찰 없음 · 원기둥 R 120 µm · H 60 µm 의 1/6 대칭 · C3D6 + C3D8 > 100,000 요소 · 바닥 고정.

**(2) Li 금속 — 접촉 FEM 입력 (본문 Methods p.14, 원문)**
> *"A similar rate-dependent plasticity model (Equation 1) was implemented to model the deformation of Li metal (with Young's modulus of **5 GPa**[44]; Poisson's ratio of **0.3**[44]; characteristic strain rate of **0.05/s**[41,42]; strain-rate-hardening parameter as **6.6**[43]; and equivalent yield strength as a variable parameter)."* · *"different equivalent yield strengths for Li (**1, 2, 4, 8, and 16 MPa**)"* · *"The stack pressure was set at 8 MPa for all cases"* · *"A frictionless hard contact boundary condition"*.
- 문헌 Li 항복 (p.10): *"Analysis of rate-dependent plasticity in Li that is based on nanoindentation data corresponds to a yield stress of **0.7–0.8 MPa**[31,32]"* (Anand & Narayan) · 그 소성 흐름의 시간 규모 *"on the order of several seconds"*.
- 덴드라이트 끝 FEM 의 Li: *"Li metal is treated with **perfect plasticity**"* — 항복값은 적혀 있지 않다.
- ⚠ 참고문헌 41 · 42 는 펄스 전류 · CCD 논문 (Reisecker 2023 · Morchhale 2024) 이라 '0.05/s' 의 출처로 맞지 않아 보인다 (§10-⑫).

**(3) `Table S1` "Creep Mechanisms and Characteristic Time" (SI p.12)** — 원문 그대로 (t_c = 변형률 속도의 역수 @ σ = 8 MPa · 결정립 d = 100 µm · 순수 Li · 출처 Jeong & Kim 2024):

| Model | Temp. | Mechanism | t_c [s] @ σ = 8 MPa, d = 100 µm |
|---|---|---|---|
| Dislocation glide | Low | dislocation undergo glide motion | 10⁻⁵ |
| Nabarro-Herring model | High | diffusional creep | 2.446 × 10¹⁵ |
| Coble model | High | diffusional creep | 2.099 × 10⁴ (5 hours) |
| Lattice-diffusion controlled GBS | High | Grain boundary sliding | 2.552 × 10² (4.3 mins) |
| Pipe-diffusion controlled GBS | High | Grain boundary sliding | 5.885 × 10⁵ (163 hours) |
| Grain-boundary-diffusion controlled GBS | High | Grain boundary sliding | 1.336 × 10⁹ |
| Harper-Dorn model | High, near melting | Dislocation slip creep | 1.721 × 10⁻³ |
| Lattice-diffusion controlled DCC | High | Dislocation slip creep | 1.516 × 10⁻⁵ |
| Pipe-diffusion controlled DCC | High | Dislocation slip creep | 1.588 × 10⁻⁸ |

(GBS = grain boundary sliding · DCC = dislocation climb creep · 원문 오타 "udergo" 는 고쳐 적었다.) ⚠ 2.099×10⁴ s = **5.8 h** [우리 산술] (원문 괄호는 "5 hours").

**(4) `Table S2` + 순수 Li 물성 (SI p.13–14)** — 원문 그대로 (값 열 = 무차원 상수 k_i, 출처 Jeong & Kim 2024):

| Mechanism | Equation (원문 글자 그대로) | Value |
|---|---|---|
| Nabarro-Herring | δ₁ = k1(Dₗ/d2)(Eb3/k6T)(σ/E) | 14 |
| Coble | δ₂ = k2(Dₓₓb3/d3)(E b3/k6T)(σ/E) | 50 |
| GBS — Lattice-diffusion controlled (GBS-D1) | δ3 = k3(D1/d2)(σ/E) 2 | 8.47×10⁹ (Present analysis) |
| GBS — Pipe-diffusion controlled (GBS-Dp) | δ4 = k4α(Dp/d2)(σ/E)4 | 4.24×10¹⁰ (Present analysis) |
| GBS — Grain-boundary-diffusion controlled (GBS-Dxx) | δ5 = k5(Dxxb/d3)(σ/E) 2 | 5.32×10⁷ (Present analysis) |
| Harper-Dorn | δ6 = k6(D1/b2)(Eb3* k6T)(σ/E) | 1.7×10⁻¹¹ |
| Lattice-diffusion controlled DCC (DCC-D1) | δ7 = k7(D1/b2)(σ/E)4 | 5.17×10¹² (Present analysis) |
| Pipe-diffusion controlled DCC (DCC-Dp) | δ8 = k8(Dp/b2)(σ/E)7 | 5.74×10¹⁵ (Present analysis) |

- 순수 Li 상수 (원문 그대로): **b = 3.04×10⁻¹⁰ m** · **G = 3.08×[1−2.28×10⁻¹⁰(T−300)] GPa** · **v = 0.36** · **E = 8.24×[1−2.28×10⁻³(T−300)] GPa** ("calculated using the relation of 2G(1+v)") · **D1 = 3.14×10⁻⁴ exp(−55700/RT) m²/s** · **DxxDp = 7.1×10⁻⁵ exp(33700/RT) m²/s**.
- ⚠ 글자 그대로 옮긴 것이라 **오타가 섞여 있다** — `k6T` 는 k_BT 의 깨진 글자 · G 의 온도계수 10⁻¹⁰ 은 E 의 10⁻³ 과 어긋남 · 'DxxDp' 는 두 확산계수 (입계 D_gb · 전위관 D_p) 가 붙은 꼴이고 지수의 부호가 양수 · 2G(1+v) = 2 × 3.08 × 1.36 = **8.38** GPa ≠ 8.24 [우리 산술]. **이 상수를 쓰려면 원전 (Jeong & Kim 2024 *ACS Energy Lett.* 9, 3237) 에서 다시 확인한다.**
- 홉 수 검산 (D1 의 Q = 55.7 kJ/mol = 0.577 eV 를 장벽처럼 읽을 때) [우리 산술]: Γ = ν₀·exp(−Q/kT) · ν₀ 10¹³ s⁻¹ (**가정**) · T 298 K → Γ ≈ 1.7×10³ s⁻¹ · 평균 대기 ≈ 0.6 ms · 5 h (1.8×10⁴ s) 동안 N ≈ 3×10⁷. ⇒ "수 시간 걸린다" 는 원자 홉이 느려서가 아니라 **확산 거리 (Coble 은 t ∝ d³/σ)** 에서 나온다. 같은 상수로 D_l(25 °C) ≈ **5×10⁻¹⁰ cm²/s** [우리 산술] — 본문이 쓴 *"measured Li diffusivities of ∼10⁻¹¹ to 10⁻¹⁰ cm²/s"* (p.10) 보다 크다.

**(5) 시편 · 미세구조 · 공정 (DEM 압밀 · 침대 조건)**

| 양 | 값 | 출처 |
|---|---|---|
| 분말 | Li₆PS₅Cl (NEI Corp.) · 입경 (결정립) ≈1 µm *"dictated by the starting powders"* | p.2 · Methods p.11 |
| 성형 | **360 MPa · 4 min · 상온 · 일축** (Spectra Services 프레스) | Methods p.11 |
| 후열처리 | 60 · 100 · 250 °C · 2 h (진공 오븐 Isotemp 281A) — **60 °C 가 주 시편** | Methods p.11 |
| 상대밀도 | 무처리 85–89 % · 60 °C **85–89 %** · 100 °C 84–89 % · 250 °C 83–92 % (막대 평균 figure-read ≈87 %) — 진밀도 분모 미기재 | `Fig. S14` (실독) |
| 기공률 | **≈8–17 %** | 본문 p.2 |
| 펠릿 두께 | Methods 는 `Fig. S14` 에 있다고 하나 **그림에 없다** | §10 |
| σ_ion (상온 EIS) | 무처리 **0.70** · 60 °C **0.53** · 100 °C **0.52** · 250 °C **0.44 mS/cm** | SI p.1 (`Fig. S1` 미독) |
| Li\|SE 초기 계면 ASR (사이클 전, 8 MPa) | 무처리 23 · 60 °C **11** · 100 °C 12 · 250 °C 37 Ω·cm² | SI `Fig. S6` 캡션 (미독) |
| 셀 사전 압착 | 모든 split cell 에 **10 MPa · 10 min** 를 건 뒤 0 · 3 · 5 · 8 MPa 로 시험 | Methods p.12 |
| Li 박 | 100–250 µm (두께 영향 적다는 선행 연구 인용 — Haslam 2022) | Methods p.12 |

**(6) 공극 · FEM 기하 (계면 연속체 모델 입력)**

| 양 | 값 | 출처 |
|---|---|---|
| 사이클 직후 공극 | 동전 모양 · Li 와 LPSCl 양쪽으로 **≈200 nm** 깊이 · 계면 따라 **최대 ≈5 µm** | p.4 · `Fig. 2A–B` |
| 탄성 FEM 의 공극 | **길이 ≈3 µm × 폭 0.5 µm** (반쪽 1.5 µm 그림) · 스택압 **10 MPa** (캡션 · 그림 글자) — 본문은 8 MPa | `Fig. 5A–B` |
| 탄성 FEM 최대 응력 | von Mises **116 MPa** · 공극 가장자리 LPSCl 쪽 · ≈2 nm² 요소 (메시를 줄이면 커진다고 저자 인정) | `Fig. 5C` · p.8–9 |
| 접촉 FEM 기하 | **W 80 µm · L 105 µm · h 10 µm** (렌즈형 공극, 위 LPSCl · 아래 Li 가 같은 기하) · 스택압 8 MPa | `Fig. S12` (실독) |
| 접촉률 @ 8 MPa | Li 항복 16 MPa → **10 %** · 8 MPa → **20 %** (그림 글자) · 4 MPa → figure-read ≈48 % (다항 외삽) · 2 · 1 MPa → 100 % (외삽 + Video S4) | `Fig. 5E–F` |
| 균열 FEM | 대칭 반쪽 · CPE8R ≈100,000 · 균열 벽 균일 압력 p(t) · 영역 J-적분 → G_net | Methods p.14 |

### 3b. 전기화학 — CCD (`Table 1` 원문 + 그림 판독)

**`Table 1` "CCD comparisons with published results" (본문 p.4) — 원문 그대로**

| Cycling protocol | Temp. (°C) | Stack pressure (MPa) | CCD (mA/cm²) | Li capacity (mAh/cm²) | Reference |
|---|---|---|---|---|---|
| Conventional protocol | 25 | 1 | 0.4 | 0.4 | Wan et al. (ref 25) |
| Conventional protocol | 25 | 1 | 0.6 | 0.6 | Wan et al. (ref 25) |
| Conventional protocol | ∼24 | 3 | ∼0.9 | 0.63 | Zeng et al. (ref 26) |
| Conventional protocol | 25 | N/A | 0.4 | 0.2 | Chen et al. (ref 27) |
| 5-h hold cycling protocol | 25 | 3 | 1.3 | 0.5 | this work |
| 5-h hold cycling protocol | 25 | 5 | 3.0 | 0.5 | this work |
| 5-h hold cycling protocol | 25 | 8 | 4.8 | 0.5 | this work |
| Sinusoidal-like cycling protocol | 25 | 8 | 1.2 | 4.8 | this work |

각주 a: *"These prior results are comparable to our work, in that interfacial modifications were not employed."*

**유지 시간 × 압력 매트릭스 (`Fig. 1C` 막대 · figure-read ≈ · 막대 정의 · 셀 수 미기재)**

| 스택압 | 5 h | 1 h | 12 min | 무유지 |
|---|---|---|---|---|
| 8 MPa | **≈4.2** (막대 ≈2.9–4.8) · 최고 4.8 (본문) | **≈3.35** (≈2.95–3.7) · 최고 3.7 (SI p.7) | ≈2.35 (≈2.3–2.4) | 1.8 (`Fig. 1B` 대표 셀) · 1.8–2.4 (SI p.5) |
| 5 MPa | ≈2.1 (≈1.6–3.0) · 최고 3.0 (`Fig. S8a`) | ≈1.3 (≈1.1–1.5) | ≈1.1 | 그림 없음 (유지 시작 = 0.4 mA/cm² 뒤 → 최소 CCD ≈0.7 로 역산 [우리 산술]) |
| 3 MPa | ≈1.25 (≈1.2–1.3) · 최고 1.3 (`Fig. S8b`) | ≈0.7 (≈0.6–0.8) | ≈0.85 (≈0.6–1.1) | 그림 없음 |

⚠ **`Table 1` 의 'this work' 4.8 · 3.0 · 1.3 은 막대 평균이 아니라 막대 위 끝 (최고 셀)** 이다 — 문헌 쪽 값과 대등 비교가 아니다 (§10-②).

**나머지 전기화학 수치**

| 시험 | 값 | 출처 |
|---|---|---|
| 평균 과전압 (8 MPa) | 1.6 → 2.0 mA/cm²: 대조 figure-read ≈0.083 → ≈0.099 V · 5 h 유지 ≈0.074 → ≈0.149 V (≈1.7 mA/cm² 에서 교차 — 유지 쪽이 더 크다) | `Fig. 1D` |
| type 2 (준사인파, 1 h 유지 흉내) CCD | **3.9 mA/cm²** (8 MPa · ≈83 h) — 1 h type 1 보다 약간 높고 총 시간은 짧다 | `Fig. 1E` |
| 반주기 4 h 고정 CCD | type 2 **1.2 mA/cm² / 4.8 mAh/cm²** · 대조 **1.0 / 4.0** | `Fig. 1F` |
| 수명 (1.0 mA/cm² · 0.5 mAh/cm²) | type 2 figure-read ≈100 h · 대조 ≈42 h (대표 곡선 하나씩) · 본문 *"average lifetime more than double"* | `Fig. 1G` |
| 단면 석출 (한쪽으로만 도금) | 무유지 **48 µm (9.9 mAh/cm²)** → 5 h 유지 **81 µm (16.7 mAh/cm²)** | p.2 · `Fig. S9` (미독) |
| LLZTO 대칭셀 8 MPa | 5 h 유지 2 셀 · 무유지 1 셀 — 모두 ≈20–23 h 에 무너짐 · 과전압 ≈1–1.6 V (figure-read) · *"CCD is quite the same"* | `Fig. S11` (실독) |

### 3c. 공극 통계 (8 MPa · 1.5 mA/cm² 사이클 직후 → 유지)

| 유지 | 길이 µm (PLT / STR) | 폭 µm | 밀도 µm⁻¹ | 선 분율 % `Fig. 2D` | 면적 분율 % `Fig. 5D` |
|---|---|---|---|---|---|
| 0 | ≈2.15 / ≈1.62 | ≈0.23 / ≈0.26 | ≈0.34 / ≈0.48 | ≈7.0 / ≈7.2 | ≈14.2 / ≈16.4 |
| 12 min | ≈2.27 / ≈2.13 | ≈0.29 / ≈0.25 | ≈0.29 / ≈0.28 | ≈6.4 / ≈6.2 | ≈13.7 / ≈11.7 |
| 1 h | ≈1.17 / ≈1.0 | ≈0.30 / ≈0.20 | ≈0.37 / ≈0.34 | ≈5.75 / ≈5.2 | ≈9.6 / ≈5.7 |
| 5 h | ≈0.72 / ≈0.77 | ≈0.19 / ≈0.17 | ≈0.15 / ≈0.15 | ≈3.85 / ≈3.35 | ≈2.3 / ≈2.3 |

전부 figure-read ≈ (PLT = 도금 쪽 · STR = 탈리 쪽). 길이 · 폭 · 밀도는 SI3 `DataPoint.mat` 로 다시 낸 값과 맞춰 본 뒤 두 자리로 적었다 (5 h STR 길이만 그림 ≈0.77 대 재계산 1.045 — §8b). 시간 축: 길이가 1 h 에서 이미 절반, 폭은 거의 그대로 (*"voids shrink faster along the interface"*). **선 분율 (`Fig. 2D`) 과 면적 분율 (`Fig. 5D`) 은 다른 양**이다 — 둘을 섞지 않는다.

### 3d. 임피던스

| 양 | 값 | 출처 |
|---|---|---|
| 대칭셀 등가회로 | R_b + (R_SEI+CT ∥ CPE_SEI+CT) · R_b ≈18 Ω·cm² 로 5 h 고정 | `Fig. 2E` 캡션 |
| R_SEI+CT (8 MPa · 1.5 mA/cm² 사이클 뒤) | 0 → 12 min → 1 h → 5 h: figure-read **≈11.4 → ≈11.5 → ≈10.1 → ≈9.9 Ω·cm²** (≈−13 %) | `Fig. 2F` |
| Nyquist 호 | Z′ figure-read ≈17 → ≈38–45 Ω·cm² (호 지름 ≈22–27 — `Fig. 2F` 값의 약 2 배 · 두 계면 나눔 여부 미기재) | `Fig. 2E` |
| 차단전극 ASR (스테인리스 · 정규화) | 5 h 뒤: LPSCl 8 MPa figure-read **≈0.946** · LPSCl 5 MPa **≈0.975** · LLZTO 8 MPa **≈1.001** (0 h = 1) — 감소의 대부분이 첫 12 min–1 h | `Fig. 4G` |
| EIS 조건 | 10 mV · 주파수 *"1 to 100 kHz and 1 to 1 Hz"* (원문 글자 깨짐) · Biologic VMP3 / Gamry 1000E · σ = l/(R·S) | Methods p.12 |

### 3e. 압입

| 시험 | 값 | 출처 |
|---|---|---|
| 석영 표준 (광유 속) | 20 mN · 최대 깊이 figure-read ≈0.39 µm · 잔류 ≈0.19 · 제하 시작 '어깨' 없음 → 광유 점성 배제 | `Fig. 4A` |
| LPSCl 부하–제하 (5 mN/s) | 최대 figure-read ≈3.6 µm (부하 곡선이 ≈0.6 µm 에서 시작) · 잔류 ≈1.85 · 제하 시작에 깊이가 더 들어가는 '코 (nose)' | `Fig. 4B` |
| LPSCl 다단 (40 s 유지 · 0.2 mN 90 s) | 최대 figure-read ≈1.8 µm · 40 s 유지 크리프 ≈0.07 µm · 제하 회복 ≈0.1 µm · 둘째 유지 변화가 첫째보다 훨씬 작다 | `Fig. 4C` |
| 맞춤 곡선 | 상대 깊이 figure-read ≈−0.03 → ≈+0.12 µm (40 s 유지) · 제하 4 s 에 ≈−0.15 · FEM (빨강) 이 실험 (파랑 여러 줄) 에 겹친다 | `Fig. S10` |
| Vickers 29.4 N | 대각선 figure-read ≈377 (0 min) · ≈385 (12 min) · ≈380 (60 min) · ≈415 (180 min) · ≈415 µm (300 min) · 오차 ±13–32 | `Fig. 4D` |
| Vickers 깊이 | ≈54 · ≈55 · ≈54 · ≈59 · ≈59 µm — **대각선 / 7 과 다섯 점 모두 같다** (Vickers 기하 h = d/7) → 독립 측정이 아니다 [우리 산술] | `Fig. 4E` |
| Vickers FEM (Table 2 상수) | 깊이 figure-read ≈25 µm (0) → ≈37–38 µm (평탄) — 실험 ≈54–59 µm 보다 ≈35 % 얕다 | `Fig. 4F` |
| Vickers 경도 [우리 산술 · 논문에 없음] | HV = 1.8544 F/d²: 0 min **≈0.38 GPa** → 5 h **≈0.32 GPa** · Tabor Y ≈ H/3 ≈ **0.13 → 0.11 GPa** (금속 관계 · 황화물 검증 안 됨) | `Fig. 4D` 값 |

### 3f. FEM 결과

| 모델 | 값 | 출처 |
|---|---|---|
| 탄성 공극 (10 MPa) | 최대 von Mises 116 MPa < Y_SE 350 MPa → *"deformation of this SE is primarily elastic here"* · Li 쪽은 항복 (0.7–0.8 MPa) 을 *"far above"* | `Fig. 5B–C` · p.8–9 |
| 소성 접촉 (8 MPa) | FEM 실선은 p/Y₀ ≈1.0–1.55 · 접촉률 figure-read ≈24–40 % 에서 끝나고 (세로선), 그 너머는 **다항 외삽 (점선)** · 별 = 8 MPa 점 | `Fig. 5F` |
| 닫힘 시간 (Li 고전 소성) | 본문 *"over several seconds"* · SI 하한 추정 t̂ = ε̄ᵖ / max ε̇ᵖ: Y₀ 16 MPa → ε̇ᵖ 127 s⁻¹ · ε̄ᵖ 0.42 · **t̂ 0.003 s** / 8 MPa → 3617 s⁻¹ · 2.5 · **0.0007 s** / 4 MPa → 5.6×10⁶ s⁻¹ · 7.8 · **1.4×10⁻⁶ s** | p.10 · SI p.16 |
| 균열 G_net (유지 있음) | 압력 0→6 MPa (0–5 h) · 유지 · 6→18 (10–15 h) · 유지 · 18→36 (20–25 h) · 유지 — G_net figure-read ≈0.31 (6 MPa · 유지 중 완화 없음) · ≈0.77 → ≈0.69 J/m² (18 MPa 유지) · ≈0.96 → ≈0.74 J/m² (36 MPa 유지) | `Fig. 6A` |
| 균열 G_net (유지 없음) | 0 → 36 MPa (15 h) · G_net ≈0.96 J/m² 에 도달 — **같은 압력의 최고값은 유지 유무와 같다** | `Fig. 6B` |
| 압력 상승 속도 | ṗ = C_iikl δ_kl i / (3 F V_m l) (Li 석출 = 고유 변형, 둘레 구속 가정) — l (길이 척도) 값 미기재 | SI p.17–18 |

### 3g. 열처리 선택 (SI `Fig. S1`–`Fig. S7` — 그림 미독 · 글자만)

- σ_ion 은 열처리로 **떨어진다** (0.70 → 0.53 → 0.52 → 0.44 mS/cm). XRD 는 불순물 없음 (`Fig. S2`), Raman 은 무처리 ≈280 · 425 · 570 cm⁻¹ (PS₄³⁻) · 온도와 함께 ≈200 cm⁻¹ 강해짐 · 100 · 250 °C 에서 480 cm⁻¹ (S₈ 의 S–S) · 250 °C 에서 ≈360 cm⁻¹ 둔덕 (Li₂S₄ 또는 비정질 P₂Sₓ) · 425 cm⁻¹ 넓어지고 낮은 쪽으로 이동 (`Fig. S3`) → 저자: 소량 분해.
- SEM: 열처리 후 **표면**이 약간 치밀 (`Fig. S4`) · 단면은 차이 없음 (`Fig. S5`) · 상대밀도도 차이 없음 (`Fig. S14`).
- 초기 계면 ASR 은 60 · 100 °C 가 절반 (11 · 12 대 23 · 37 Ω·cm²) · CCD 는 60 °C 가 최고 (**1.8–2.4 mA/cm²** @ 8 MPa) → 60 °C 채택 (`Fig. S6`–`Fig. S7`). 스택압 0 · 3 · 5 · 8 MPa 중 8 MPa 가 최고 CCD (`Fig. S7c`, 수치 미기재).

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 펠릿 · 셀
- Li₆PS₅Cl 분말 (NEI) → **360 MPa · 4 min 상온 일축** (Spectra Services) → 진공 오븐 (Isotemp 281A) **60 / 100 / 250 °C · 2 h**. 두께 · 상대밀도는 `Fig. S14` (실제로는 상대밀도만 있다).
- σ_ion 셀: 기밀 Swagelok (X2 Lab). CCD 셀: **split cell (MTI)** · Li 박 양쪽 (작동 · 상대 전극). LLZTO 대칭셀도 같은 구성 (LLZTO 표면 처리 기술 없음 — §10-⑨).
- 모든 조립은 Ar 글러브박스 (O₂ < 5 ppm · H₂O < 5 ppm).

### 4b. 스택압
- 모든 split cell 에 **10 MPa · 10 min** 를 먼저 건 뒤 시험 압력 (**0 · 3 · 5 · 8 MPa**) 으로 바꾼다. 압력은 하중 센서 셀 (MTI) 로 감시 · 제어.
- 차단전극 ASR 셀은 **시험 내내 일정 압력** (Methods 는 "8 MPa" 라 하지만 `Fig. 4G` 에는 LPSCl 5 MPa 곡선도 있다).

### 4c. 전기화학 프로토콜 (전부 상온 · Biologic VMP3)
- **기본 CCD**: 0.1 mA/cm² 부터 0.1 씩 올림 · 반주기 용량 0.5 mAh/cm² 고정 (`Fig. 1F` 제외) · 대칭 (반대 방향 반주기).
- **type 1 (영전류 유지)**: 유지 12 min · 1 h · 5 h. 유지는 **각 조건의 최소 CCD 보다 0.3 mA/cm² 낮은 전류부터** 시작 — 8 MPa 는 1.5 mA/cm² 뒤, 5 · 3 MPa 는 0.4 mA/cm² 뒤. 유지는 반주기마다 (SI `Fig. S8` 캡션 *"holding time of 5 hours per half cycle"*).
- **한쪽 석출 시험**: 0.1 mA/cm² 5 h → 0.2 부터 0.1 씩 · 단계 30 min. 유지 (12 min · 1 h · 5 h) 는 1.6 mA/cm² 석출 뒤부터.
- **type 2 (준사인파 · `Fig. 1E`)**: 1 h 유지 type 1 을 흉내. 0.1 → 1.5 mA/cm² 까지는 type 1 과 같고, 그 뒤 반주기 = 0.1 · 0.3 · 0.5 mA/cm² 각 10 min → 최고 X (1.6, 다음 1.7 …) 를 0.2 mAh/cm² 만큼 (Y = 0.2/X × 60 min) → 0.5 · 0.3 · 0.1 각 10 min. 반주기 총 0.5 mAh/cm² (`Table S3` 이 X = 1.6 예시 · *"X = cycle number / 10"*).
- **반주기 4 h 고정 (`Fig. 1F`)**: 대조 = 0.1 → 1.0 mA/cm² (0.1 씩) · type 2 = 평균이 같도록 x · 3x · 5x · 7x · 5x · 3x · x (첫 주기 0.025 · 0.075 · 0.125 · 0.175 mA/cm² · x = 0.025 × 주기 번호) · 최고 전류 60 min · 나머지 30 min.
- **수명 (`Fig. 1G`)**: 0.1 → 1.0 mA/cm² 올린 뒤 1.0 mA/cm² · 0.5 mAh/cm² 반복. type 2 = 0.25 · 0.75 · 1.25 (각 3.75 min) → 1.75 (7.5 min) → 1.25 · 0.75 · 0.25 (각 3.75 min) — 평균 1.0.
- CCD 의 판정 기준 (단락의 전압 신호) 은 **명시되지 않았다**.

### 4d. EIS
- 10 mV · 정전위 · Biologic VMP3 또는 Gamry 1000E · 주파수 *"1 to 100 kHz and 1 to 1 Hz for conductivity measurement and Li-Li symmetric cell"* (글자 깨짐 — 범위 확정 불가) · σ = l / (R × S).
- 차단전극: LPSCl 은 360 MPa · 4 min 상온 압축 + 스테인리스 (60 °C 열처리 여부 미기재) · LLZTO 는 사포 600 → 1,200 · Pt/Au 나노 코팅 스퍼터 + 스테인리스.

### 4e. 특성분석
- XRD Bruker D8 Discovery 2D (Kapton 밀봉 — ★ 피크 = Kapton) · ESEM Thermo Quattro S 20 kV · Raman WITec Alpha 300 (532 nm · 27 mW · 0.5 s × 300 누적 · Ar 밀폐 · 시료당 4–6 지점).
- **cryo-FIB-SEM**: Thermo Scios 2 DualBeam · 저온 스테이지 · EDAX Octane Elite EDS. 셀은 8 MPa 에서 0.1 → 1.5 mA/cm² (0.1 씩) 사이클 후 해체 → Leica VCT500 진공 운반 → Leica EM ACE600 로 Pt 10 nm → 액체 질소 냉각 · **< −150 °C** → Ga⁺ 30 keV · 50 nA 거친 단면 → 7 nA 정리.

### 4f. 공극 영상 분석 (본문 Methods + SI3 코드 §8b)
- MATLAB Image Segmenter · 회색조 문턱 미세조정 + 닫힌 형태 마스크 (Otsu) → 계면 근처의 검은 화소 섬 = 공극 (계면 방향 길이 · 수직 방향 폭).
- **선 분율 (`Fig. 2D`)** = *"cumulative length of the islands over the total length of the selected"* · **면적 분율 (`Fig. 5D`)** = 계면을 가로지르는 **3.6 µm 폭 띠** 안의 검은 화소 면적 (⚠ 코드의 띠 폭은 51 px × 5/209 µm = 1.22 µm — §8b).
- 표본: 유지 시간 (0 · 12 min · 1 h · 5 h) × 도금 · 탈리 쪽마다 **이미지 3–5 장**, 이미지당 공극 3–10 개 (SI3 실제: 이미지 2–5 장 · 공극 1–10 개).

### 4g. 나노압입
- Bruker TI 950 TriboIndenter · fluid tip · 시편을 광유 (Alfa Aesar) 에 완전히 잠금 (유리 페트리 접시) · 기기 컴플라이언스는 광유 속 석영 깊이 프로파일로 교정.
- 조건당 **4 표면 · 중심 간격 > 150 µm**. `Fig. 4A–B`: 20 mN · 5 mN/s 부하 · 같은 속도 제하. `Fig. 4C`: 20 mN (5 mN/s) → **40 s 유지** → 0.2 mN (peak 의 1 %) 까지 5 mN/s 제하 → **90 s 유지** → 0 mN.
- 압입 깊이 < 결정립 (≈1 µm) 이라고 본문이 쓰지만 (p.5), 그림의 깊이는 ≈1.8–3.6 µm 다 (§10-⑥).

### 4h. Vickers 압입
- 29.4 N (캡션) · 최고 하중 유지 0 · 12 min · 1 h · 3 h · 5 h (그림 x 축). 본문은 *"more detailed information is provided in the Methods section"* 이라 하지만 **Methods 에 Vickers 절이 없다** (기기 · 부하 속도 · 깊이 측정법 미기재).

### 4i. FEM 4 종 (Abaqus · 본문 *"The modeling code is shared in Code S1"*)
1. **점소성 완화 (덴드라이트 끝)**: LPSCl = UMAT (식 1) · Li = 완전 소성 (항복값 미기재) · 준정적 (최소 메시 1 µm · LPSCl 음속 ≈600 m/s → 고체파 시간 ≪ 모사 시간) · Li 석출 부피 변화 = Li 에 Y 방향 열팽창 · 충전 구간은 부피 증가, 유지 구간은 부피 유지 · LPSCl–Li 경접촉 (떨어지지 않음) · ≈20,000 요소 (끝 부근 세분). — 이 모델의 결과 그림이 어느 것인지는 본문에 대응이 없다.
2. **Berkovich 역해석**: §3a (1) 참조. 적합 = 상대 깊이 변화 (`Fig. S10`).
3. **균열 구동력**: 대칭 반쪽 (그림의 노란 영역) · CPE8R ≈100,000 · 균열 끝 세분 · 균열 벽에 시간 의존 균일 압력 p(t) · 영역 J-적분 → **G_net** (`Fig. 6`). 균열 길이 · 형상 값은 **미기재**.
4. **Li–SE 접촉**: LPSCl = `Table 2` · Li = 식 1 (E 5 GPa · ν 0.3 · ε̇₀ 0.05 s⁻¹ · n 6.6 · Y₀ 1 · 2 · 4 · 8 · 16 MPa) · **마찰 없는 경접촉** · 거친 LPSCl 면이 Li 를 압입하며 접촉 면적이 늘어남 · 8 MPa (`Fig. 5E–F` · `Fig. S12` · Video S1–S3). Video S4 = 속도 무관 완전 탄–소성 Li (`Fig. S13`) → 공극 완전 닫힘.
- ⚠ **받은 SI3 에는 FEM (UMAT · 입력 파일) 이 없다** — MATLAB 공극 분석 스크립트 3 개와 .mat 29 개뿐이다 (§8b).

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 왜 60 °C · 8 MPa 인가 (SI `Fig. S1`–`Fig. S7` — 미독, 글자만)
열처리는 σ_ion 을 **낮추지만** (0.70 → 0.53 mS/cm @ 60 °C) 계면 ASR 을 절반으로 (23 → 11 Ω·cm²) 줄이고 CCD 가 가장 높았다 (1.8–2.4 mA/cm² @ 8 MPa). 저자는 60 · 100 °C 의 ASR 감소를 **표면 치밀화** (`Fig. S4`), 250 °C 의 악화를 **표면 분해** (`Fig. S3` Raman S₈ · P₂Sₓ) 로 설명한다. 스택압은 코인 · 파우치 셀 수준인 10 MPa 미만에서 골랐고 8 MPa 가 최고였다. 상대밀도는 열처리와 무관하게 ≈85–89 % (`Fig. S14` 실독 · 막대 ≈87 %).

### 5.2 type 1 — 유지가 CCD 를 올린다 (`Fig. 1A–D` 실독)
- `Fig. 1A`: 기존 (사각파) · type 1 (반주기 사이 0 전류 유지 — 빨간 선) · type 2 (계단식 준사인파). 반주기 용량은 셋 다 **0.5 mAh/cm²**.
- `Fig. 1B`: 8 MPa 에서 5 h 유지 셀 (위, 빨강) 은 **≈400 h · CCD 4.8 mA/cm²** (전압 ±0.4 V 축), 무유지 셀 (아래, 청록) 은 **≈35 h · CCD 1.8 mA/cm²** (±0.2 V 축). 유지는 1.5 mA/cm² 뒤에 시작 (캡션).
- `Fig. 1C`: 막대 9 개 — 압력 (8 > 5 > 3 MPa) 과 유지 시간 (5 h > 1 h > 12 min) 의 단조 경향. 3 MPa 에서는 1 h (≈0.7) 가 12 min (≈0.85) 보다 낮아 단조가 깨진다 (막대 겹침). 막대 정의 · 셀 수는 없다.
- `Fig. 1D`: 1.6–2.0 mA/cm² 평균 과전압 — 유지 셀이 1.7 mA/cm² 위에서 **더 크다** (2.0 에서 ≈0.149 대 ≈0.099 V). 저자: 유지가 SEI 를 더 키운다 · 누적적 (p.8).
- 저자 주장 (p.2): 문헌 Li₆PS₅Cl CCD 0.4–0.9 mA/cm² (1–3 MPa · 0.2–0.63 mAh/cm²) 대비 4.8 은 **계면 개질 없이** 얻은 매우 높은 값 · 3 MPa 결과는 기존 프로토콜 문헌 (Zeng 2022) 과 비슷.

### 5.3 한쪽 석출 (`Fig. S9` — 미독)
유지가 없으면 48 µm (9.9 mAh/cm²), 5 h 유지면 81 µm (16.7 mAh/cm²) 까지 석출한 뒤 단락. 유지 효과가 대칭 사이클에 국한되지 않는다는 증거로 쓴다.

### 5.4 type 2 — 실용 프로토콜로도 된다 (`Fig. 1E–G` 실독)
- `Fig. 1E`: 3.9 mA/cm² (≈83 h · 전압 ±0.8 V 까지 커짐) — 1 h type 1 (최고 3.7) 보다 약간 높고 시간은 짧다 → *"rate-dependent deformation is relevant in both cases"*.
- `Fig. 1F`: 반주기 4 h 고정이라는 보수적 조건에서도 type 2 1.2 / 4.8 mAh/cm² > 대조 1.0 / 4.0.
- `Fig. 1G`: 1.0 mA/cm² 수명 — 대표 곡선은 대조 ≈42 h · type 2 ≈100 h (figure-read). 본문은 *"average lifetime more than double"* 이라 하지만 셀 수 · 평균 · 산포는 그림에도 본문에도 없다.

### 5.5 공극 영상 — 유지 동안 닫힌다 (`Fig. 2A–D` · `Fig. 5A` · `Fig. 5D` 실독)
- `Fig. 2A–B`: 탈리 쪽 (A) · 도금 쪽 (B) cryo-FIB 단면, 왼→오 0 · 12 min · 1 h · 5 h · 스케일 3 µm. 계면이 세로로 놓이고 한쪽이 Li (매끈한 FIB 줄무늬) · 다른 쪽이 LPSCl (입자 질감).
- 사이클 직후 공극: 동전 모양 · 양쪽으로 ≈200 nm · 계면 따라 최대 ≈5 µm · 큰 것과 작은 것 공존 · 밀도 높음 (p.4).
- `Fig. 2C` (길이 · 폭 · 밀도): 길이 ≈2 µm (0 · 12 min) → ≈1.0–1.2 (1 h) → ≈0.7–0.8 µm (5 h) · 폭 ≈0.2–0.3 µm 거의 일정 · 밀도 ≈0.3–0.5 → ≈0.15 µm⁻¹ (일부 공극이 아예 사라짐). 오차막대가 매우 크다 (0 h 길이 ≈0.1–4.6 µm).
- `Fig. 2D` (선 분율): ≈7 % → ≈3.5 % — 도금 쪽 막대는 좁고 탈리 쪽은 넓다 (≈5.6–10.7 %). ⚠ 이 그림은 SI3 로 재현되지 않는다 (§8b).
- `Fig. 5D` (면적 분율 vs √t): 도금 ≈14.2 → ≈13.7 → ≈9.6 → ≈2.3 % · 탈리 ≈16.4 → ≈11.7 → ≈5.7 → ≈2.3 %. 저자는 *"roughly linear"* 를 확산 지배의 표지로 읽는다 — 그림의 탈리 쪽은 √t 에 대해 **위로 오목** (기울기 0–7.75 구간 ≈1.4 %/min^½ → 7.75–17.3 구간 ≈0.36) 이고, 4 점 · 큰 오차막대로는 다른 꼴 (지수 감쇠 등) 과 가를 수 없다 (§10-④).
- 탈리 쪽이 약간 더 빨리 닫히는 경향 — 오차 범위 안이라 결론 아님 (p.10) · 저자는 탈리가 직전 도금의 SEI 를 바꾸기 때문일 수 있다고 본다.
- 이 기법으로는 **SEI 가 보이지 않는다** (p.4).

### 5.6 계면 저항이 따라 준다 (`Fig. 2E–F` 실독)
Nyquist 의 고주파 절편 R_b ≈18 Ω·cm² 는 5 h 동안 그대로이고 호만 약간 줄어든다. R_SEI+CT 는 ≈11.4 (0) → ≈11.5 (12 min) → ≈10.1 (1 h) → ≈9.9 Ω·cm² (5 h). 저자: 공극 닫힘 = 접촉 면적 증가 → 계면 저항 감소와 *"roughly consistent"*. 단 차단전극에서 본 LPSCl 자체의 변화 (`Fig. 4G`) 도 이 감소에 기여할 수 있다고 스스로 단서를 단다 (p.8).

### 5.7 개념도 — 스프링 · 대시팟 · 마찰 슬라이더 (`Fig. 3` 실독)
- `Fig. 3A`: 스프링 (탄성) · 대시팟 (점성) · 마찰 슬라이더 (항복) · 탄–소성 (슬라이더 + 스프링 직렬) · **점소성 = (대시팟 ∥ 슬라이더) + 스프링 직렬** ("Concept in This Work" — Bingham 형 탄–점소성). 본문이 슬라이더 + 스프링 직렬을 *"e.g., a Maxwell model"* 이라 부르는 것은 용어가 어긋난다 (Maxwell = 스프링 + 대시팟 직렬).
- `Fig. 3B`: (i) 물결진 Li 면과 SE 접점의 변형에너지 집중 · (ii) 덴드라이트 끝 = **Li 가 아직 안 찬 덴드라이트 균열 (unfilled dendritic crack)** 둘레 변형에너지.
- `Fig. 3C`: 탄성 SE 는 에너지를 쌓기만 하고 (i · ii 위), 점소성 SE 는 소산한다 (i · ii 아래, "Energy Dissipation").
- 본문 p.4 의 *"the two mechanisms shown in Figures 4B and 4C"* 는 **`Fig. 3B` · `Fig. 3C`** 의 오기다.

### 5.8 LPSCl 나노압입 — 점소성 (`Fig. 4A–C` · `Fig. S10` 실독)
석영은 제하 시작에 어깨가 없고, LPSCl 은 5 mN/s 까지도 제하 시작에 깊이가 더 들어가는 '코' 가 보인다 → 광유가 아니라 LPSCl 고유의 점성. 다단 시험에서 40 s 유지 중 깊이 증가 (점탄성 + 점소성) 가 0.2 mN 유지 중 회복 (점탄성) 보다 훨씬 크다 → 그 차가 속도 의존 점소성. `Fig. S10` 의 FEM 맞춤으로 `Table 2` 를 얻었다. ⚠ 같은 20 mN 인데 `Fig. 4B` (최대 ≈3.6 · 잔류 ≈1.85 µm) 와 `Fig. 4C` (최대 ≈1.8 · 회복 ≈0.1 µm) 의 깊이 · 탄성 회복이 크게 다르다 — 저자가 말한 표면 거칠기 · 기공의 크기를 보여 준다 (§10-⑥).

### 5.9 Vickers — 큰 스케일에서도 점소성, 그러나 모델보다 무르다 (`Fig. 4D–F` 실독)
유지 시간이 0 → 5 h 로 늘면 대각선 ≈377 → ≈415 µm · 깊이 ≈54 → ≈59 µm (180 min 점에서 이미 포화). 압흔 (≈400 µm) 은 결정립 (≈1 µm) 보다 훨씬 커서 기공 · 입자 접점을 평균한다. Table 2 상수로 돌린 FEM 은 깊이를 ≈37–38 µm 로 **얕게** 예측 → *"the relative amount of plastic deformation with the Vickers indents is qualitatively larger"* · *"not just a localized phenomenon"* · 기공 · 입자 상호작용 · 더 큰 시편 시험 (Song 2025) 에서도 차이가 난다고 쓴다. 오차막대 (±13–32 µm) 가 0 → 60 min 점들과 겹쳐, 유지 의존성은 180 min 이후 두 점의 평균 이동 (≈+35 µm) 에 기댄다.

### 5.10 차단전극 ASR — 스택압에서의 LPSCl 느린 변형 (`Fig. 4G` 실독)
압입은 국부 압력이 스택압보다 훨씬 크므로, 스택압 수준을 보려고 SS\|LPSCl\|SS (와 SS\|LLZTO\|SS) 를 일정 압력에서 5 h 유지하며 EIS 를 쟀다. 정규화 ASR: LPSCl 8 MPa ≈0.975 (12 min) → ≈0.964 (1–2 h) → ≈0.948 (3 h) → ≈0.946 (5 h) · LPSCl 5 MPa ≈0.98 → ≈0.973 → ≈0.975 · LLZTO 8 MPa ≈1.00 (변화 없음). 저자: 벌크 · 계면 중 어느 쪽인지 가를 수 없지만, **나노압입 항복보다 훨씬 낮은 응력에서 큰 스케일 크리프 (입자 재배열 등)** 가 LPSCl 에서 일어날 수 있다는 해석 (p.7). 절대 ASR 값 · 셀 수 · 오차막대는 없다.

### 5.11 LLZTO 대조 (`Fig. S11` 실독)
LLZTO 8 MPa 대칭셀은 5 h 유지 (2 셀) 와 무유지 (1 셀) 모두 ≈20–23 h 에 무너졌고 과전압이 ≈1–1.6 V 까지 올랐다 — 유지 효과 없음. 저자는 *"preliminary"* · 기전 해석은 별도 연구가 필요하다고 스스로 한정한다 (p.7). 뒤에서는 이 결과를 *"SEI 가 적은 LLZTO 에서는 Li 가 공극으로 훨씬 빨리 흐른다"* (Roach 2025) 는 SEI 가설의 방증으로도 쓴다 (p.10).

### 5.12 다른 유지 연구와의 차이 (p.7–8)
마이크로초 펄스 (Reisecker 2023) 는 시간 규모가 ≈10 자릿수 짧아 무관. Morchhale 2024 는 argyrodite 에서 **20 MPa** 로 유지 ≤ 30 min · **5 min 유지에서 CCD 향상 → 더 길면 약간 감소** — 이 논문은 낮은 압력에서 5 min (그림은 12 min) 유지로는 향상이 없고 수 시간 유지에서 크게 향상 → 높은 압력에서는 다른 기전이 지배한다고 해석.

### 5.13 탄성 FEM — 공극 끝 응력 (`Fig. 5A–C` 실독)
`Fig. 5A` 의 공극 (점선 타원 ≈3 µm × 0.5 µm) 을 본떠, 위 Li · 아래 LPSCl 로 탄성 FEM (그림 글자 · 캡션 **10 MPa**). 최대 von Mises **116 MPa** 가 3 상 접점 (LPSCl/Li/공극) 근처 · 공극 가장자리 LPSCl 쪽에 집중 (≈2 nm² 요소). 이 값은 Y_SE 350 MPa 보다 작다 → LPSCl 은 여기서 **주로 탄성** · Li 쪽은 항복 (0.7–0.8 MPa) 을 훨씬 넘어 **소성 예상**. 응력 집중이 길쭉한 모양에서 오므로, 공극이 **계면 방향으로 더 빨리 줄어드는** 관찰 (`Fig. 2C`) 과 맞는다고 본다. SI 는 Li 벌크 ≈10 MPa → 공극 모서리 ≈100 MPa 로 적는다 (SI p.14).

### 5.14 소성 접촉 FEM — Li 가 그렇게 무르면 수 초 만에 닫혀야 한다 (`Fig. 5E–F` · `Fig. S12` 실독)
거친 LPSCl 면이 Li 를 누르는 2 상 모델 (W 80 · L 105 · h 10 µm). 등가 항복 Y₀ 16 MPa 면 접촉률 10 %, 8 MPa 면 20 % (`Fig. 5E` 의 빨간 영역 = 그 응력 등고면 = 항복 영역). `Fig. 5F` 는 접촉률 대 p/Y₀ — FEM 실선은 접촉률 ≈24–40 % 에서 끊기고 (세로선), 100 % 는 **다항 외삽 (점선)** 이다. 별 (8 MPa) 위치: Y₀ 16 → ≈11 % · 8 → ≈21 % · 4 → ≈48 % · 2 · 1 → 100 % (외삽의 끝점). 저자 결론: **Y₀ ≤ 2 MPa 이면 완전 닫힘 · 수 초 안** (Video S1–S4 · SI 하한 추정은 ms–µs) → 문헌 Li 항복 (0.7–0.8 MPa) 으로는 실험의 **수 시간**을 설명 못 한다 → *"classical plasticity in the metal is not active around the voids"* · 공극 벽 Li 는 **SEI (Li–LPSCl 반응 생성물) 때문에 항복이 더 높다** · 또는 **전해질과의 젖음이 나빠서 (poor wetting)** 공극 채움이 막힌다 (p.10).

### 5.15 느린 닫힘 = Li 확산 크리프 (`Table S1` · `Table S2` · p.10)
저응력에서 기전이 바뀌는 것은 금속에서 흔하다. 스택압이 확산 크리프와 전위 소성 둘 다를 구동하지만, 실험을 설명하려면 공극 둘레의 빠른 소성이 *"꺼져야"* 한다 (SEI 가설과 정합). `Fig. 5D` 의 √t 거의 선형 + Li 확산계수 10⁻¹¹–10⁻¹⁰ cm²/s 의 √(Dt) ≈ 4–10 µm (5 h) ≈ 공극 크기 → 확산 지배. Jeong & Kim 2024 의 기전 시간표에서 **Coble 크리프 (수 시간)** 가 관찰과 맞고, 나머지는 훨씬 짧거나 (나노압입 멱법칙 · 전위) 훨씬 길다 (Nabarro–Herring · 입계 확산 GBS). SI: 스택압 P 의 일축 응력 상태에서 등가 인장응력 = P (8 MPa) · 공극 모서리 응력 집중 → 세 확산 기전 (Coble ∝ σ · 격자 확산 GBS ∝ σ² · 전위관 확산 GBS ∝ σ⁴) 모두 더 빨라진다. LPSCl 의 느린 크리프도 공극 닫힘에 일부 기여할 수 있다 (`Fig. 4G` 와 정합).

### 5.16 덴드라이트 균열 구동력 — 유지가 G_net 을 풀어 준다 (`Fig. 6` 실독)
Li 가 찬 덴드라이트 균열 안 압력 상승 속도 ṗ 를 전류에 비례로 두고 (SI p.17–18), 유지 = 압력 고정으로 모사. `Fig. 6A` (유지 있음): 6 MPa 유지 중 G_net ≈0.31 J/m² 는 **변하지 않고**, 18 MPa 유지 중 ≈0.77 → ≈0.69, 36 MPa 유지 중 ≈0.96 → ≈0.74 J/m² 로 준다 (소성 영역이 시간에 따라 커지며 소산 증가 · 균열이 길수록 완화가 크다고 본문은 쓴다). `Fig. 6B` (유지 없음): 15 h 에 36 MPa · G_net ≈0.96. ⚠ **같은 압력에서의 최고 G_net 은 유지 유무와 같다** — 부하가 다시 시작되면 G_net 이 곧 무유지 곡선 값으로 돌아온다 (§10-⑦). 이 FEM 은 나노압입 상수만 쓰므로 큰 스케일 효과 (스택압 크리프 · 입자 재배열) 는 빠져 있다.

### 5.17 결론 (p.11)
① 유지 시간 × 압력의 체계적 변화가 **수 시간 규모의 속도 의존 변형**이 성능을 바꾼다는 분명한 증거 · ② 최고 CCD 4.8 mA/cm² (5 h · 8 MPa) · ③ Li\|SE 계면 공극 닫힘은 **Li 의 비교적 느린 확산 크리프**가 주로 지배 · Li 의 낮은 문헌 항복은 큰 역할이 없다 (SEI 가 공극 벽 Li 의 물성을 바꿨을 수 있음 — 직접 조사 안 함) · ④ LPSCl 은 나노압입에서 뚜렷한 점소성 · 8 MPa 차단전극 ASR 감소는 나노압입이 못 보는 더 느린 변형을 시사 · 나노압입 항복값에서 SE 소성은 가압 덴드라이트 둘레 응력을 풀어 줄 것 · ⑤ SE 의 속도 의존 변형은 같은 시간 규모에서 덜 두드러지고, 응력이 높은 자리 (덴드라이트 둘레 · 입자 접점) 에서 의미가 있을 것.

---

## 6. 메커니즘 종합 — 논증의 사슬

1. **관찰 A (전기화학)**: 유지 시간이 길수록 · 압력이 높을수록 CCD ↑ (`Fig. 1C`) → 스택압 효과는 **속도 의존** (점소성) 이다.
2. **관찰 B (영상)**: 8 MPa 5 h 유지 동안 공극이 길이 방향으로 줄고 일부는 사라진다 (`Fig. 2C` · `Fig. 5D`) · 계면 저항도 준다 (`Fig. 2F`) → 성능 향상 ↔ 공극 닫힘 (접촉 면적 증가) 상관.
3. **누가 흐르나 (LPSCl)**: 나노압입 점소성 (Y_SE 0.35 GPa) 이지만 공극 끝 탄성 응력 116 MPa < 350 MPa → **LPSCl 은 공극 끝에서 탄성** (`Fig. 5C`). 차단전극 ASR 의 느린 감소 (`Fig. 4G`) 는 저응력 큰 스케일 크리프의 단서일 뿐 (≈5 %).
4. **누가 흐르나 (Li)**: 문헌 Li 항복 0.7–0.8 MPa · 8 MPa ≫ 항복 → FEM 은 **수 초 (SI 하한 ms–µs) 안에 완전 닫힘** (`Fig. 5F`) → 실험 (수 시간) 과 모순 → 공극 벽 Li 는 고전 소성이 *"꺼져"* 있다 → **가설: SEI (반응 생성물) 가 섞인 Li 는 항복이 높다** · 또는 젖음 불량.
5. **그럼 시간 규모는 무엇이 정하나**: 면적 분율 ∝ √t (`Fig. 5D`) + √(Dt) ≈ 공극 크기 + Coble 크리프의 t_c ≈ 2.1×10⁴ s (`Table S1`) → **Li 확산 크리프 (Coble)** 가 닫힘을 지배.
6. **덴드라이트 쪽 (LPSCl 점소성의 몫)**: 압력 상승 중 유지는 LPSCl 소성 영역을 키워 G_net 을 풀어 준다 (`Fig. 6`) → 빠른 충전일수록 균열에 불리 · 유지가 덴드라이트 균열을 늦출 수 있다.
7. **보조 증거**: LLZTO (SEI 적음 · 탄성 SE) 에서는 유지 효과 없음 (`Fig. S11`) · 탈리 쪽이 약간 빨리 닫힘 (SEI 변화).
⇒ **최종 그림**: "Li 확산 크리프가 공극을 닫는 주역 (수 시간) · LPSCl 점소성은 고응력 자리 (덴드라이트 끝 · 입자 접점) 의 조연 · 낮은 Li 항복은 SEI 때문에 계면에서 작동하지 않는다". 4–5 의 연결 고리 (SEI 경화 · 젖음 · Coble 의 d = 100 µm 가정) 는 **직접 측정되지 않은 가설**이다 (§10).

---

## 7. 우리 대비 ★ (`../our_dft_baseline.md` · `../our_dem_baseline.md` · W_ad 보고서)

### 7a. 우리 DFT 기준선 (축 C · 기계) — 겹치는 것은 E 하나뿐
| 항목 | 이 논문 | 우리 | 같은가 / 왜 |
|---|---|---|---|
| E (Li₆PS₅Cl) | **22.1 GPa** (`Table 2` · 문헌값 · 인용 = Abaqus 매뉴얼) | comp1 **E_VRH 22.06 GPa** (DFT 0 K relaxed-ion 전 C_ij · canonical · `comparison_group` `elastic-dft-relaxedion-comp1comp2-v1`) | **같은 수지만 독립 확인이 아니다** — 이 논문 값의 출처로 보이는 Deng 2016 (PBEsol · 조밀 단결정 · 22.1) 이 원래 우리 relaxed-ion 과 0.2 % 차다 (`deng2016_…` §7.2). 이 논문은 측정하지 않았다 |
| ν | 0.30 | (기준표에 없음) | Deng 0.37 과도 다르다 — 출처 불명 |
| 펠릿 겉보기 E | — (안 쟀다) | — | 같은 그룹 같은 공정 `[Song25Mech]` **4.7 ± 1.1 GPa** (mm 굽힘) — 조밀 결정 E 와 **다른 물리량** (I-3 규율) |
| B₀ · G · C_ij | n/a | comp1 B₀ 26.23 GPa (BM3) 등 | 비교 불가 |
| 항복 · 크리프 (Y_SE · ε̇₀ · n) | 0.35 GPa · 10⁻⁵ s⁻¹ · 4 | **없음** (DFT 로 항복을 안 낸다) | 우리 원장에 대응 양 없음 |
| σ_ion | 0.53 mS/cm (60 °C 펠릿 · 상온 EIS) | MLIP-MD (다른 양) | 비교하지 않는다 |
| gap · ESW · Ea · ICOHP | n/a | 있음 | 이 논문은 다루지 않는다 |
⚠ 우리 탄성은 조성 간 비교가 CONDITIONAL (`HZ-elastic-cross-composition`) — 여기서는 comp1 하나만 썼다.

### 7b. 우리 DEM 기준선 — **값이 없다**
`our_dem_baseline.md` 는 자리표시 (값 0 개) 다. 그래서 이 논문 값과 숫자로 맞대 볼 우리 DEM 정본이 없다. 대신 **쓰는 자리**를 적는다 (`comparison_vs_ours_DEM.md` §I-3 규율 — *"벌크값을 입자 입력으로 넣지 말 것 · 입자 입력 = 결정/국소 (DFT 22.06, 나노압입) · 벌크 = 창발 침대 검증용"*):
- **입자 (국소) 층**: E 22.1 (조밀 · DFT 계열) · **Y_SE 0.35 GPa** (나노압입 역해석 · 여러 결정립 평균 · 5–10 µm 압흔) → DEM 탄–소성 접촉의 항복 후보. 단 식 1 은 과응력 꼴 · 40–60 s 유지에만 맞췄다.
- **침대 (겉보기) 층 — 검증 표적**: Vickers 경도 [우리 산술] HV ≈0.38 → ≈0.32 GPa (5 h) → Tabor Y ≈0.13 GPa · `lee2025_heckel_…` 의 Heckel σ_y,eff ≈0.10–0.13 GPa 와 같은 자릿수 (둘 다 기공 포함 펠릿 · 다른 시험 — 같은 양으로 놓지 않는다) · `[Song25Mech]` E 4.7 GPa.
- **스택압 크리프**: 식 1 로 못 낸다 (σ < Y 에서 0). 저응력 크리프의 실험 표지는 차단전극 ASR −5 % (8 MPa · 5 h) 뿐이고 구성식이 없다.

### 7c. W_ad 보고서 — 위치만 (값은 싣지 않는다)
- 보고서: `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html`. 쌍 목록 (2 절) = C–C · Ag–C · LPSCl\|Ag(111) · LPSCl\|흑연 — **Li\|LPSCl 쌍은 없다.** 7 절 = Li 친화성 정량화 (Li 원자 흡착 · Li 금속–재료 W → Young–Dupré 젖음각 · 합금 구동력) — **제안 단계 · 아직 계산 안 함**.
- 이 논문이 그 7 절에 주는 것: ① 저자 스스로 *"Poor wetting with the electrolyte is another possible factor that may limit void filling"* (p.10) 이라 쓰지만 **정량이 없다** — Li\|LPSCl 의 W/γ_Li (젖음각) 가 그 빈칸을 채울 양이다. ② 접촉 FEM 은 **마찰 없는 경접촉 = 점착 0** 이다 — W 를 경계 조건으로 넣을 자리가 비어 있다. ③ 실측 공극 크기 · 밀도 · 닫힘 시간 (`Fig. 2C` · `Fig. 5D` · SI3) = 점착 · 젖음을 넣은 모델의 대조 표적.
- ⛔ 우리 W (DFT 열역학 점착일) 와 이 논문의 어떤 양도 같은 줄에 놓지 않는다 — 이 논문에는 점착 측정값이 없다.

### 7d. 판정 요약
| 축 | 판정 |
|---|---|
| 같은 것 | E 22.1 ≈ 우리 comp1 22.06 — 출처 계열이 같아서 (독립 확인 아님) |
| 다른 것 (진짜) | 이 논문의 물리 (점소성 · 크리프 · 공극 닫힘 · 스택압 프로토콜) 는 우리 DFT 원장에 **대응 양이 없다** — 차이가 아니라 **공백** |
| 방법 의존 | Y_SE 는 '상대 깊이 변화' 맞춤 · E 고정 (문헌) · 40–60 s 창 — E 나 맞춤 창을 바꾸면 Y · ε̇₀ · n 이 같이 움직인다 (공동 맞춤) |
| 우리에게 새것 | Li 크리프 시간표 (`Table S1`) · Li 접촉 FEM 입력 · 공극 통계 원자료 (SI3) |

---

## 8. 계산 · 후처리 방법 ★

**DFT · AIMD · MLIP — 없다.** code · functional · pseudo · k-point · ecut · supercell · DFT+U · AIMD · MLIP · 무질서 처리 전부 **n/a**. 이 논문의 '계산' 은 연속체 FEM 과 영상 분석뿐이다.

- **FEM 코드**: Abaqus (판 미기재 · ref 37 = *ABAQUS (2010) Analysis User's Manual*) + 사용자 재료 UMAT (Peirce 형 대변형 탄–점소성). 요소: C3D6 + C3D8 (> 100,000 · Berkovich 1/6 모델) · CPE8R (≈100,000 · 균열 반쪽 · 평면 변형) · 덴드라이트 끝 모델 ≈20,000. 접촉: 마찰 없는 강체 압자 · LPSCl–Li 경접촉. 균열: 영역 J-적분 → G_net. 상세 §4i.
- **물성 입력의 출처**: LPSCl E · ν = 문헌 (인용 오류) · Y_SE · ε̇₀ · n = 이 논문 맞춤 · Li = Masias 2019 (E · ν) + ref 41–43 (ε̇₀ · n) · Li 크리프 상수 = Jeong & Kim 2024.
- **영상 후처리**: MATLAB Image Segmenter (Otsu 문턱 + 손 마스크) → SI3 스크립트 3 개로 길이 · 폭 · 밀도 · 선 분율 · 면적 분율 (§8b).
- **EIS 맞춤**: R_b + (R ∥ CPE) 등가회로 · 맞춤 소프트웨어 미기재.
- **수치화 · 기록**: 오차막대 정의가 본문에 없다. SI3 로 다시 내 보면 `Fig. 5D` 막대 = **이미지별 값의 ±1 표본 SD** 로 읽힌다 (§8b). Video S1–S4 (FEM 동영상) 는 받지 못했다.

---

## 8b. 코드 (Sup3) — 받은 것 · 하는 일 · 다시 내 본 결과 ★

> 2026-11-24 수령 (메인 세션 전달). **읽기만 했다** — 스크립트는 실행하지 않았고 (MATLAB 없음), `.mat` 은 `python3 -I` + `scipy.io.loadmat` (scipy 1.18.1 · numpy 2.5.3) 으로 열어 값만 읽었다. 데이터 파일은 litdb 로 복사하지 않았다. 재계산용 임시 스크립트는 세션 스크래치에만 두었다.

### 받은 것
- 위치: `litdb/inbox/shi2026_sup3/codes/` (git 무시 — `.gitignore` 11 행 `litdb/inbox/`) · 39 MB.
- 받은 zip sha256 (사용자가 Windows 에서 원본 38 MB zip 을 코드 · 데이터로 나눠 보냄): code `1C1516C90432591F731E5C1BE928C4572CC381507AFD0409CB54C48600F25699` · data part1 `958E0538F748D0832DE8DFF81E388A0136958F53BF34C1E49777BB890B8B6571` · part2 `87AF7D1968B94D6B96667D1EF5EDFE6510FD6E76328571D34A92731321BCE531`.
- 스크립트 3 개 (sha256 앞 16 자리): `script_sparse.m` 40 줄 `52ff1d2964088a83` · `script_for_pore.m` 298 줄 `396d6067df655e40` · `script_2D_void_fraction.m` 56 줄 `f0a5bdfb1d223e51`.
- `.mat` 29 개 (MATLAB 5.0 · MACI64 · 2024-05-27 생성): `DataPoint.mat` 1 + 이미지 파일 28 (아래 이름 규칙). `script_for_pore.m` 머리말 *"develop by Chenjie; modified 01/23/2025"*.
- ⚠ **FEM 코드는 없다.** 본문은 *"The modeling code is shared in Code S1"* · *"The modeling code is provided"* 라 하지만 받은 SI3 는 **공극 영상 분석**뿐이다 (UMAT · Abaqus 입력 없음). Video S1–S4 도 없다.

### 파일 이름 규칙 (본문 · SI 와 맞춰 확인)
| 조각 | 뜻 | 근거 |
|---|---|---|
| `h0` · `min12` · `h1` · `h5` | 영전류 유지 **0 min · 12 min · 1 h · 5 h** | 파일 안 `DataPoint.time` = 0 · 12 · 60 · 300 (전부 확인) · 본문 Methods 의 유지 시간 |
| `PLT` · `STR` | **도금 (plating) 쪽 · 탈리 (stripping) 쪽** 계면 — 마지막 반주기에 Li 가 쌓인 쪽 · 빠진 쪽 | `Fig. 2A` (Stripping Side) · `Fig. 2B` (Plating Side) · `DataPoint.mat` 변수 `data_*_plt` · `data_*_str` |
| `DP1`–`DP3` | **data point = 이미지 번호** (한 조건의 서로 다른 FIB-SEM 이미지) | Methods *"Three to five images were analyzed … for each hold time"* |
| `_1` · `_2` | 같은 DP 번호 아래 **다른 원본 이미지** — 원본 변수 이름이 다르다 (예: `h5_PLT_DP2_1` = `x1_067` · `h5_PLT_DP2_2` = `x1_070`) | 파일 안 원본 이미지 변수 |
| 원본 이미지 변수 `x1_NNN` | 1094 × 1536 uint8 회색조 SEM 원본 · NNN = 이미지 일련번호 (h0 330–346 · h1/h5 037–106 · min12 436–451) | 변수 크기 · 이름 |
- 조건별 이미지 수: h0 PLT **2** (DP2 없음 — `DataPoint.mat` 에는 3 개) · h0 STR 3 · min12 PLT 3 · STR 3 · h1 PLT 3 · STR 4 · h5 PLT 5 · STR 4 = 28 파일 (`DataPoint.mat` 은 29 항목 중 h0 PLT 둘째만 파일이 없다 — 27/28 항목이 파일의 `DataPoint` 와 정확히 같다).

### `.mat` 변수 (이미지 파일 27/28 에 공통)
| 변수 | 크기 · 형 | 뜻 (스크립트로 확인 / ⁽ᵗ⁾ = 추정) | 단위 |
|---|---|---|---|
| `x1_NNN` | 1094 × 1536 uint8 (0–255) | 원본 FIB-SEM 이미지 | px |
| `maskedImage`, `maskedImage1` (+ `maskedImage2` 13 파일 · `maskedImage3` 2 파일) | N × W uint8 (0–255) | 마스크를 씌운 회색조 띠 ⁽ᵗ⁾ | px |
| `BW_sparse` | N × W uint8 {0,1} | **최종 이진 마스크 — 0 = 검정 = 공극** (두 스크립트의 입력) | px |
| `BW` (+ `BW1` 3 · `BW2` 1) | N × W uint8 {0,1} | 다른 이진 마스크 — 27/27 파일에서 `BW_sparse` 와 **수천 화소** 다르다 · 어느 단계인지 코드 · 본문에 없음 ⁽ᵗ⁾ | px |
| `count_area` | N × W uint8 (6–129) | 미상 (스크립트가 안 쓴다) | — |
| `isblack` | 1 × k uint16 | 검은 화소가 있는 행 번호 ⁽ᵗ⁾ (k/N = `ratio` 로 확인, h0_PLT_DP1 417/926 = 0.4503) | 행 |
| `isblackorwhite` | 1 × N uint8 (≤ 51) | 행별 화소 개수 ⁽ᵗ⁾ | px |
| `ratio` | 스칼라 | = numel(`isblack`) / N | — |
| `D1_vector` | 1 × N uint8 | 행별 공극 두께 (검은 화소 수) — `script_sparse.m` | px |
| `number` · `density` | 스칼라 | 공극 개수 · 계면 길이당 개수 | 개 · µm⁻¹ |
| `average_width` · `max_width` · `crack_length` | 1 × number float | 공극별 평균 폭 · 최대 폭 · 길이 | µm |
| `scale` | 스칼라 0.02392 | **5 µm / 209 px** | µm/px |
| `DataPoint` | 1 × 1 struct | {number · density · average_width · max_width · crack_length · total_length · time} | 위와 같음 · total_length µm · time min |
| `i` · `index` · `ans` | 루프 잔여 · `ans` 는 h0_PLT_DP1 만 (0.0865) | — | — |
- 크기: N = 526–1025 행 (= 계면 방향 **12.6–24.5 µm**) · W = **51** (대부분) · 101 · 151 · 851 (h1 묶음 — 계면이 기울어진 잘라내기).
- `DataPoint.mat`: struct 배열 8 개 `data_{0h,12min,1h,5h}_{plt,str}` — 크기 plt 3 · 3 · 3 · 5 · str 3 · 3 · 4 · 4.

### 세 스크립트가 하는 일
1. **`script_sparse.m` (이미지 한 장 → `DataPoint`)** — 입력 `BW_sparse` (행 = 계면 방향 위치 · 열 = 계면을 가로지르는 51 px 띠).
   - 행 i 가 **검은 화소 ≥ 2 개**면 그 행의 공극 두께 D1(i) = 검은 화소 수, 아니면 0 (`sum(row) > W − 2` → 0).
   - `bwlabel(D1_vector)` 로 0 아닌 행의 연속 구간 = 공극 하나. **길이 = (마지막 행 − 첫 행) × scale** (1 행짜리 공극은 길이 0 — 실제로 h0_PLT_DP3 에 0 이 있다) · 평균 폭 = 구간의 D1 평균 × scale · 최대 폭 · **밀도 = 개수 / (N × scale)** µm⁻¹ · total_length = N × scale.
   - 끝 두 줄이 `DataPoint.time = 12;` · `save min12_STR_DP3.mat` 로 **박혀 있다** — 이미지마다 손으로 고쳐 돌린 틀이고, `save` 는 작업 공간 전체를 저장한다 (그래서 각 파일에 중간 변수가 다 들어 있다). `D1_vector` 를 비우지 않는다 (앞 이미지 값이 남을 수 있는 꼴 — 저장된 파일에서는 길이 = N 으로 문제 없음).
   - → 본문 대응: `Fig. 2C` 의 입력 · Methods 의 *"number density, average length, and width"*.
2. **`script_for_pore.m` (`DataPoint.mat` → `Fig. 2C`·`Fig. 2D` 꼴 그림 10 장)** — `load` 가 없어 `DataPoint.mat` 을 미리 불러 둬야 한다. 유지 시간 [0 12 60 300] min 마다 이미지별 값의 **산점 + 평균선**: 밀도 · mean(crack_length) · mean(average_width) · **선 분율 = Σ crack_length / total_length** (y 라벨 'porosity%' 이지만 값은 0–1 분수) · 선 분율의 semilog 그림 2 장 (본문에 없음). 오차막대는 **계산하지 않는다**.
3. **`script_2D_void_fraction.m` (폴더의 PLT · STR `.mat` 전부 → `Fig. 5D` 꼴)** — `BlackPixelRatio` = 검은 화소 / 전체 · `Angle` = π/2 − atan((W − 51)/N) · **`Mod_ratio` = 검은 화소 / (51 × N / sin(Angle))** — 띠를 51 px 폭으로 보고 기운 잘라내기를 보정. 결과는 `BlackPixelRatios.mat` 에 저장 (받은 묶음에 없음).
- 이 코드가 **못 하는 것**: 이진화 (Otsu 문턱 · 손 마스크 · `BW` → `BW_sparse`) 는 스크립트가 아니다 (Image Segmenter 대화형) · 오차막대 · `Fig. 2D` 의 % 값 · FEM.

### 다시 내 본 결과 (읽기만 · `python3 -I` · scipy)
**`Fig. 5D` (면적 분율) — `Mod_ratio` 를 조건별로 평균 [SI3 재계산] 대 그림 [figure-read ≈]**

| 조건 | 이미지 | 그림 평균 (막대) | 재계산 평균 ± SD [최소–최대] | 판정 |
|---|---|---|---|---|
| 0 · PLT | 2 (+ 빠진 1) | ≈14.2 (≈13.2–15.2) | 13.80 [13.05–14.55] | 빠진 DP2 가 ≈15.0 % 면 평균 · 위 막대가 맞는다 |
| 0 · STR | 3 | ≈16.4 (≈13.9–18.8) | **16.37 ± 2.47** | ✅ |
| 12 min · PLT | 3 | ≈13.7 (≈10.9–16.5) | **17.03 ± 3.14** [13.44–19.28] | ❌ 그림이 ≈3.3 %p 낮다 |
| 12 min · STR | 3 | ≈11.7 (≈10.25–13.2) | **11.73 ± 1.48** | ✅ |
| 1 h · PLT | 3 | ≈9.6 (≈8.6–10.6) | **9.61 ± 1.02** | ✅ |
| 1 h · STR | 4 | ≈5.7 (≈4.2–7.1) | 5.42 ± 1.80 | ≈ (막대 아래 끝 ≈0.6 차) |
| 5 h · PLT | 5 | ≈2.3 (위 끝 ≈3.6) | 2.19 ± 2.04 | ≈ (막대 폭 다름) |
| 5 h · STR | 4 | ≈2.3 (≈0.8–3.8) | **2.28 ± 1.50** | ✅ |
⇒ 막대 = **이미지별 값의 ±1 표본 SD (n−1)** 로 읽힌다 (✅ 4 점은 평균 · 막대 끝이 소수 첫째 자리까지 맞는다). **12 min 도금 쪽만 어긋난다** — 올라온 데이터대로면 도금 쪽은 14.2 → **17.0** → 9.6 → 2.2 % 로 12 min 에 오히려 올랐다가 떨어진다 (그림은 단조 감소).
⚠ 같은 파일의 다른 마스크 `BW` 로 같은 식을 돌리면 도금 7.4 → 5.9 → 8.4 → 4.3 % · 탈리 11.9 → 9.7 → 4.7 → 2.0 % [SI3 재계산] — **닫힘의 크기 (≈85 % 감소) 는 최종 마스크 다듬기 (`BW` → `BW_sparse`) 에 크게 기대고, 그 규칙은 코드 · 본문에 없다.**

**`Fig. 2C` (길이 · 폭 · 밀도) — `script_for_pore.m` 의 평균 (이미지별 값의 평균) [SI3 재계산]**

| 유지 | PLT 길이 / 폭 / 밀도 | STR 길이 / 폭 / 밀도 | 그림 대조 |
|---|---|---|---|
| 0 | 2.153 / 0.234 / 0.336 | 1.615 / 0.261 / 0.477 | ✅ |
| 12 min | 2.267 / 0.290 / 0.285 | 2.135 / 0.245 / 0.284 | ✅ |
| 1 h | 1.173 / 0.299 / 0.367 | 0.998 / 0.202 / 0.344 | ✅ |
| 5 h | 0.724 / 0.191 / 0.148 | **1.045** / 0.174 / 0.153 | STR 길이 ❌ (그림 ≈0.77) |
(길이 · 폭 µm · 밀도 µm⁻¹.) 5 h STR 의 이미지별 평균 길이는 0.754 · **1.878** · 0.975 · 0.574 µm — 1.878 (DP2 · 공극 2 개) 을 빼면 0.768 로 그림과 맞는다 (우연일 수도 있다). 오차막대는 이미지 평균의 산포보다 훨씬 넓어 (0 h 길이 ≈0.1–4.6 µm) 공극 하나하나의 산포로 보이지만, 모은 공극의 SD · 최소–최대 어느 것과도 네 점이 다 맞지는 않는다 (12 min 최대 6.15 · 7.49 µm 대 막대 위 끝 ≈4.7 · 4.45).

**`Fig. 2D` (선 분율) — Methods 정의로 재현되지 않는다 ❌**
Methods 정의 (*"cumulative length of the islands over the total length of the selected"*) = `script_for_pore.m` 의 Σ 길이 / 전체 길이로 내면 [SI3 재계산] 도금 **71.1 → 64.9 → 42.1 → 11.9 %** · 탈리 **77.1 → 60.1 → 31.3 → 14.5 %** — 그림 (≈7.0 → 6.4 → 5.75 → 3.85 % · ≈7.2 → 6.2 → 5.2 → 3.35 %) 의 **약 10 배 (0 h)** 다. ÷10 · 공극당 평균 분율 (9.1 → 3.0 %) · 면적형 (길이 × 폭) 을 대 봤지만 네 점이 다 맞는 정의는 없었다. 덧붙여, 51 px 띠에서 '검은 화소 ≥ 2' 기준이면 사이클 직후 계면의 **≈70 %** 가 공극 행으로 잡힌다 (h0_PLT_DP1 639/926 행) — 계면을 따라 얇은 검은 띠 (D1 ≈7–11 px ≈0.17–0.26 µm) 가 거의 이어져 있다는 뜻이다.

**그 밖의 점검**
- 저장된 `D1_vector` 와 저장된 `BW_sparse` 로 다시 낸 D1 이 **15/27 파일에서 1–11 행** 어긋난다 → 공극 수가 4 파일에서 달라진다 (h0_STR_DP2 8 대 10 · h1_PLT_DP3 10 대 11 · min12_PLT_DP2 **7 대 11** · min12_PLT_DP3 6 대 7) · 길이 분율 변화는 ≤ 1.3 %p. 마스크를 고친 뒤 D1 을 다시 안 냈거나 그 반대 — 논문 값은 **저장된 쪽** (`DataPoint`) 이다.
- 이미지당 공극 **1–10 개** (Methods "three to ten" 과 다름 — 5 h 이미지 셋은 1 개).
- 띠 폭: 코드 51 px × 0.02392 µm/px = **1.22 µm** ↔ Methods · `Fig. 5D` 캡션 *"3.6-µm-wide region"* — 맞지 않는다 (설명 없음).
- 기운 잘라내기 보정 (`Mod_ratio`) 은 h1 묶음 7 파일에만 작동한다 (W 101–851) — 보정 전 · 후 차가 커서 (h1_PLT_DP1 0.77 % → 10.11 %) h1 점의 값은 이 기하 가정에 기댄다.
