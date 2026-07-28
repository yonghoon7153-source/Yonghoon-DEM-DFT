# Revealing the Impact of Cl Substitution on the Crystallization Behavior and Interfacial Stability of Superionic Lithium Argyrodites — Liu et al. (Adv. Funct. Mater. 2022)

> slug `liu2022_cl_crystallization_interface_argyrodite` · DOI `10.1002/adfm.202207978` · type `exp + DFT/AIMD 보조` · PDF `82ea256b/0b781b71-14._Revealodites.pdf` · digested `2026-06-26` · status ✅
> **저자**: Yu Liu, Han Su, **Yu Zhong** (교신), **Xiuli Wang** (교신), Xinhui Xia, Changdong Gu, **Jiangping Tu** (교신) — State Key Lab of Silicon Materials, School of Materials Science & Engineering, **Zhejiang University** (Hangzhou, China). Adv. Funct. Mater. 2022, 32, 2207978. Received 2022-07-13, published 2022-09-16.
> **태그**: **[외부]** (Zhejiang Univ. — Hanyang/Jong-Won Lee/Y.M.Lee/Cho/Kang/Cha 아님). National NSF China U20A20126·51971201 지원.

> ⚠ **혼동 주의 — 이 논문 ≠ Zuo 2022 Angew**. 둘 다 "LPSCl vs Li₅.₅PS₄.₅Cl₁.₅ Cl 치환" 주제이고 둘 다 2022년이라 INDEX의 Excel exp#10·calc#10 행이 Zuo의 DOI(`10.1002/anie.202213228`)와 *섞여* 기록돼 있었으나, **이 PDF의 실제 정체는 Zhejiang Univ. Tu 그룹의 AdvFunctMater 논문**(DOI `10.1002/adfm.202207978`, Excel exp#2·계산#? / DFT시트 #4와 동일). Zuo는 Giessen(Janek)·NCM85 양극 계면·ToF-SIMS/DEMS 실험 중심; **Liu(본 논문)는 *결정화(annealing)* + *Li 금속 음극* 계면 + AIMD/RDF**가 핵심으로 **다른 논문·다른 그룹·다른 초점**.

---

## 0. 이 digest를 읽는 법
이 논문은 두 개의 질문을 *결정화*와 *음극 계면* 두 축에서 답한다. (1) **"Cl을 더 넣으면(LPSCl→Li₅.₅PS₄.₅Cl₁.₅) annealing(소결) 거동이 어떻게 바뀌고, 왜 그것이 σ를 끌어올리나?"** (2) **"높은 Cl이 왜 Li 금속에 더 안정한가(dendrite 억제·환원 저항)?"** — Zuo가 *양극*(cathode) 계면을 본 데 반해 본 논문은 **음극(Li metal)** 계면을 본다. 핵심 도구는 **annealing 온도 시리즈 XRD/Rietveld + EIS + CCD/long-cycle Li 대칭셀 + AIMD/RDF(Li/argyrodite–Li metal 계면)**. 결론: Cl-rich는 *결정화로* (LPSCl은 σ가 결정화도에만, LPSCl₁.₅는 결정화도 *그리고* S²⁻/Cl⁻ 무질서에 둘 다 의존) σ↑(최고 **8.0 mS/cm**), inter-cage Li 경로 활성화, **음극에서 PS₄ 분해가 더 느림**(RDF로 입증) + **LiCl-rich SEI**로 dendrite 억제(CCD 0.95→**1.40 mA/cm²**, 대칭셀 500 h vs short).

> ⚠ **전압 기준**: 본 논문 full cell은 **Li-In(InLi) 음극** 기준(2.5–4.25 V vs Li⁺/Li, C/5). 대칭셀·CCD는 Li 금속. (Zuo와 달리 명시적 In/InLi vs Li/Li⁺ 환산 보정 식은 주지 않음 — full cell 전압은 Li⁺/Li 기준으로 직접 표기.)

## 1. 한 줄 요약
Cl-rich Li₅.₅PS₄.₅Cl₁.₅는 LPSCl보다 (a) **450 °C annealing서 가장 높은 σ=8.0 mS/cm**(LPSCl은 550 °C서 2.62), (b) **AIMD로 본 inter-cage Li 경로 활성화**(MSD 3배·전 방향 확대), (c) **음극에서 PS₄³⁻ 분해가 더 느리고**(RDF: LPSCl은 10 ps서 P–S 깨짐 / Cl-rich는 35 ps까지 유지) **LiCl-rich SEI**로 dendrite 억제 → CCD 0.95→**1.40 mA/cm²**, 대칭셀 안정 cycling 500 h, NCM811 full cell 100 cyc 유지율 30.6→**80.4 %**. 단 **고-Cl은 annealing window가 좁고**(LiCl·thio-LISICON 불순물이 σ를 깎음, 450 °C서만 순상) Cl이 용해한계 넘으면 석출.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교 | **Li₆PS₅Cl (LPSCl, Cl 1.0)** vs **Li₅.₅PS₄.₅Cl₁.₅ (LPSCl₁.₅, Cl 1.5)** |
| 합성 | **ultra-fast ball milling 1 h → annealing 300–550 °C, 5 h** (그룹 선행 공정 인용) |
| 음극 | **Li 금속**(대칭셀·CCD·full cell Li) + **Li-In alloy**(full cell 일부) |
| 양극 | **LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811)**, 복합양극(SE:NCM = 7:3 mass) |
| 질문 1 | 고-Cl이 **annealing(결정화)** 거동·σ를 어떻게 바꾸나 (LPSCl₁.₅서 미해결이라 명시) |
| 질문 2 | 고-Cl이 **Li 금속 계면**(dendrite·환원분해)을 왜 개선하나 |
| 갭 | 대부분 선행연구는 Cl↑로 σ만; **annealing 효과 + Li-metal 계면 full-cell 비교는 미답** |
| 선행 인용 | Klerk(4d S²⁻/Cl⁻ 무질서↔σ 양의 관계, 75% 무질서 시 최고)·Adeli(Li₅.₅PS₄.₅Cl₁.₅ 9.4 mS/cm, Ea 낮음)·Kim(rapid thermal, 10.2 mS/cm) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSCl (Li₆PS₅Cl) | LPSCl₁.₅ (Li₅.₅PS₄.₅Cl₁.₅) | 출처/조건 |
|---|---|---|---|
| σ (RT, as-milled) | **1.10 mS/cm** | **2.13 mS/cm** | Fig 2a (as-milled도 Cl-rich가 ≈2× → annealing 없이도 Cl이 σ↑) |
| σ (RT, 최적) | **2.62 mS/cm @550 °C** | **8.00 mS/cm @450 °C** | Fig 2a (각 조성 최고점 annealing 다름) |
| σ annealing 경향 | 단조↑ (300→550 °C) | **450 °C 피크**, 300·350 °C서 <1 mS/cm (불순물) | Fig 2a |
| Ea (eV) | ~0.30–0.36 (annealing 의존, 비단조) | **0.28 (최저, @450 °C)** | Fig 2b (Adeli 보고와 유사) |
| 격자상수 a (Å) | **9.85** (LPSCl-550) | **9.81** (LPSCl₁.₅-450) | Rietveld Table S1/S2 (Cl-rich가 셀 *수축*) |
| S²⁻/Cl⁻ 4d 무질서 | **13.3 %** (LPSCl-550) | **61.7 %** (LPSCl₁.₅-450) | Rietveld (Cl-rich가 무질서 ↑↑) |
| Rietveld 잔차 R_wp/R_p | 3.78 / 2.36 % | 3.04 / 1.92 % | Fig 1d,e |
| 입자크기 | ≈5 µm | ≈5 µm | Fig S3 (동일) |
| 사이트 점유(도식) | Cl 90%/S @4a, Cl 60%/S @4d, S @16e, P @4b | (동일 골격, 4a/4d Cl 함량 ↑) | Fig 1a |
| CCD (critical current density) | **0.95 mA/cm²** (LPSCl-550) | **1.40 mA/cm²** (LPSCl₁.₅-450) ·1.08 (LPSCl₁.₅-550) | Fig 3a–c (step 0.064 mA/cm², 1 h 각) |
| 대칭셀 overpotential (0.2 mA/cm²) | 16 mV → 88 mV (500 h 후) | **5 → 9 mV** (500 h) | Fig 3d |
| 대칭셀 0.5 mA/cm² | short @60 h | **안정 200 h** | Fig 3e, Fig S7c |
| 계면저항(대칭셀 cycling) | 65 → >600 Ω | **34 → 50 Ω** | Fig S7a,b |
| MSD (AIMD, 상대) | 1× | **≈3×** (전 3방향 비례 확대) | Fig S5 |
| AIMD 온도 | 900 K (probability density) / 300 K (계면 RDF) | 동일 | 본문·Exp |
| Full cell 초기방전 (Li-In, C/5) | 141 mAh/g, CE **72.0 %** | **155.4 mAh/g, CE 77.6 %** | Fig 5a |
| Full cell 100 cyc 유지율 (Li-In) | (낮음) | **83.8 %** | 본문 |
| Full cell (Li metal) 초기방전 | 130.2 → 43.1 mAh/g (100 cyc, **유지율 30.6 %**) | 151.4 mAh/g, **80.4 %** (100 cyc) | Fig 6b |
| Full cell 평균 CE (6–100 cyc) | 99.5 % | **97.9 %** | 본문(주의: LPSCl이 더 높으나 용량 급감) |
| 양극 계면저항(100 cyc 후, Table S3) | **276 Ω** | **142.8 Ω** | Fig 5d (NCM/SE 부반응 LPSCl이 더 심함) |
| 불순물 (annealing 의존) | 없음(전 온도 순상) | **LiCl + thio-LISICON**(350 °C 최대, 450 °C 소멸, 550 °C LiCl 재출현) | Fig 1b,c |
| LiCl 용해 흡열 (DSC) | — | ≈425 °C endotherm (LiCl 용해) | Fig S2 |

## 4. 재료 & 방법

### 4.1 합성·전기화학 (실험)
- **합성**: Li₂S·P₂S₅·LiCl 출발물(LPSCl = 62.5/12.5/25.0 wt%; LPSCl₁.₅ = 50.0/12.5/37.5 wt%) → **ultra-fast mechanical (ball) milling**(125 mL ZrO₂ pot, ⌀10 mm ball ×25, **150 rpm 1 min** — 주: 본문은 "ultra-fast 1 h", Exp은 "150 rpm 1 min"으로 표기 불일치 가능, 그룹 선행공정 ref38) → **300–550 °C, 5 h** annealing(Ar glovebox, O₂·H₂O <0.1 ppm).
- **XRD**: Rigaku SmartLab, Cu Kα(λ=1.5418 Å), 10–90°, Kapton으로 대기차단, zero-bg holder. **Rietveld(FullProf)** → 격자상수·4d S²⁻/Cl⁻ 무질서.
- **SEM**: Hitachi SU8010.
- **EIS**: PARSTAT MC, 1 MHz–1 Hz(bulk, ±200 mV) / 1 MHz–0.01 Hz(셀, ±10 mV), 25–65 °C, 카본코팅 Al foil 양면, 360 MPa 2 min 펠릿.
- **DSC**: TA DSC250, N₂, 25–500 °C, 5 °C/min.
- **XPS**: Thermo ESCALAB / monochromatic Al Kα(1486.6 eV), C 1s 284.8 eV 보정, XPSPEAK asymmetric Gaussian-Lorentzian fit (post-mortem Li/argyrodite 계면).
- **셀**: 대칭셀 = SE 150 mg @240 MPa 2 min + Li 양면 @50 MPa 1 min. **CCD** = step-increased 전류(step 0.064 mA/cm², plating/strip 각 1 h). Full cell(PEEK, ⌀10 mm) = SE층 120 mg @240 MPa + 복합양극 7 mg(6.24 mg/cm², SE:NCM811 7:3 ball-mill 1 h) @360 MPa 3 min + In/Li foil 또는 Li. **C/5, 2.5–4.25 V vs Li⁺/Li**, 면적용량 1.12 mAh/cm².

### 4.2 DFT / AIMD (계산) ★
- **code**: **VASP** (Kresse/Furthmüller), **PAW**, **PBE-GGA**.
- **무질서 처리**: Rietveld 구조 파라미터로 시작 → **모든 대칭적으로 구별되는 Li⁶PS₅Cl·Li₅.₅PS₄.₅Cl₁.₅ 구조를 *enumeration*** (Li⁺/vacancy 부분점유 + S²⁻/Cl⁻ 무질서 처리) → **electrostatic energy 최저(Ewald) 구조를 채택** → 그 위에 Li metal 부착. ⇒ **enumerate + lowest-Ewald single-config** (SQS 아님, AIMD 비용 때문).
- **계면 모델**: Li(110) 표면 + argyrodite(100) 표면 **lattice mismatch <5%**로 매칭. (LPSCl₁.₅ 계면은 LPSCl 계면과 4a/4d Cl 함량만 다른 동형, Fig S8.)
- **AIMD**: **NVT ensemble**, time step **2 fs**, total **50 ps**, **Γ-only**(1-point), **lower ecut**(인용: MP 설정 정합), **300 K**(계면 RDF). 별도 **bulk Li 확률밀도·MSD는 900 K**(Fig 2f,g·S5).
- **relaxation/EOS**: 구조완화·총에너지는 **Materials Project(MP) 설정**과 정합.
- **MP DB 사용**: 참조물질(Li₇PS₆·Li₆PS₅Cl·Li₁₀GeP₂S₁₂·Li₃PS₄·Li₇P₃S₁₁·Na₃PS₄ / LiP·Li₃P 등)의 P–S·Li–P 결합길이를 MP에서 받아 RDF 피크 귀속.
- **post-processing 패키지**: **pymatgen-diffusion**(probability density·MSD), **vaspy(vasppy)**(RDF 계산).
- **특이사항**: bulk σ/Ea를 **직접 AIMD로 보고하지 않고**(Excel 계산시트엔 LPSCl AIMD 0.43 / LPSCl₁.₅ 14.55 mS/cm로 기재돼 있으나 *본 PDF 본문엔 AIMD σ 절대값 수치 없음* — Li 확률밀도·MSD 정성/상대 비교만), σ 절대값은 EIS 실험에 의존. 계면 분해는 RDF 시간추적이 핵심 산출물.

## 5. 결과 — 섹션별 상세

### 5.1 합성 도식·사이트 (Fig 1a)
입방 argyrodite(F-43m) 골격: **S @16e, P @4b, Cl(90%)/S @4a, Cl(60%)/S @4d**. Cl을 더 넣으면 4a·4d의 Cl 비중↑ + S²⁻/Cl⁻ 무질서↑. annealing은 ball-milled glass-ceramic을 결정화시킨다.

### 5.2 결정화·XRD — **두 조성의 결정적 차이** (Fig 1b,c)
- **LPSCl(Fig 1b)**: 전 annealing 온도(300–550 °C)서 **순수 argyrodite, 불순물 없음**. 강한 peak 위치(2θ≈30°)가 annealing 온도와 **무관 = 격자상수 불변**. annealing은 *결정화도만* 올림(peak/background 비↑).
- **LPSCl₁.₅(Fig 1c)**: annealing 온도에 **민감**. 350 °C서 **thio-LISICON + LiCl 불순물 최대**; 온도↑로 불순물↓ → **450 °C서 순상**(LiCl이 격자에 용해 → S²⁻/Cl⁻ 무질서·셀 수축 유발); 550 °C서 **LiCl 재석출**(과량 Cl 용해한계 초과 + 멜팅점 강하로 부분 용융). LPSCl₁.₅의 강한 peak는 annealing으로 **고각 이동**(격자 수축) — LPSCl과 정반대.
- **DSC(Fig S2)**: LPSCl₁.₅만 ≈425 °C endotherm = LiCl 용해. → "450 °C가 순상 window"의 열적 근거.

### 5.3 Rietveld (Fig 1d,e, Table S1/S2)
LPSCl-550·LPSCl₁.₅-450이 peak/bg 최고라 정밀 정련 대상. **격자상수 9.85→9.81 Å(수축)**, **4d S²⁻/Cl⁻ 무질서 13.3 %→61.7 %**. 즉 Cl-rich는 *더 작은 셀 + 훨씬 큰 음이온 무질서*. (Klerk 예측 "4d 무질서↑↔σ↑"의 실험 확인.)

### 5.4 전도도·활성화에너지 (Fig 2a–d)
- **σ**: as-milled도 Cl-rich가 2배(1.10 vs 2.13). 최적 = **LPSCl₁.₅-450 8.0 mS/cm** > LPSCl-550 2.62. 저온 annealing(300·350 °C) LPSCl₁.₅는 불순물로 <1 mS/cm.
- **Ea(Fig 2b)**: LPSCl₁.₅-450 = **0.28 eV 최저**. LPSCl₁.₅의 Ea-vs-annealing은 σ와 **역경향**(불순물 많을수록 Ea↑).
- 🔑 **핵심 해석**: LPSCl σ↑ = **결정화도(crystallinity)만**의 함수. LPSCl₁.₅ σ↑ = **결정화도 *그리고* S²⁻/Cl⁻ 무질서** 둘 다 — LPSCl₁.₅-450과 LPSCl₁.₅-550은 결정화도 비슷하나 σ 다름(LiCl·thio-LISICON 불순물이 자체 저전도 + 결정화도 저하). → **Cl의 σ 기여는 무질서를 통한 *본질적* 효과**.

### 5.5 Li⁺ 확률밀도·MSD — inter-cage 활성화 (Fig 2e–g, S5)
- **Fig 2f (LPSCl)**: Li⁺가 **Li₆S 팔면체 cage 안에 갇힘**(intra-cage), inter-cage 통로 미활성. 검은 점선=intra-cage, 빨강 화살표=inter-cage.
- **Fig 2g (LPSCl₁.₅)**: **inter-cage 경로 활성화 + Li 전 방향 비편재화**. cage 사이가 연결돼 밝게 이어짐.
- **MSD(Fig S5)**: LPSCl₁.₅ 총 MSD ≈ **LPSCl의 3배**, **세 방향 모두 비례 확대** = 등방적 inter-cage 망 활성화.
- → "Cl-rich가 σ 높은 *물리*": 단순 carrier 수가 아니라 **inter-cage 호핑 통로 개방**.

### 5.6 CCD·dendrite (Fig 3a–c)
step-increased 전류서 전압 급강하 = short(dendrite). **LPSCl-550 CCD 0.95 / LPSCl₁.₅-450 1.40 / LPSCl₁.₅-550 1.08 mA/cm²**. 같은 Cl-rich라도 **450(고-σ, 1.40) > 550(저-σ, 1.08)** → **σ가 CCD 지배**(전류분포 균일화). 그리고 같은 σ대(LPSCl₁.₅-550 vs LPSCl-550)서도 Cl-rich가 높음(1.08 > 0.95) → **Cl 함량 자체도 dendrite 억제에 기여**(LiCl-rich SEI). 본문: "σ↑ → 전류밀도 분포 균일 → dendrite 억제".

### 5.7 장기 대칭셀 (Fig 3d,e, S7)
- 0.2 mA/cm²·0.2 mAh/cm²: **LPSCl/Li overpotential 16→88 mV(500 h, 계속 열화)** vs **LPSCl₁.₅/Li 5→9 mV(평탄)**. 계면저항 65→>600 Ω vs **34→50 Ω**(Fig S7a,b) → LPSCl/Li 계면이 cycling 중 *계속 악화*, Cl-rich는 안정.
- 0.5 mA/cm²·0.5 mAh/cm²: LPSCl/Li **60 h서 short**(post-mortem Nyquist, Fig S7c) vs LPSCl₁.₅/Li **200 h 평탄**.

### 5.8 음극 계면 AIMD/RDF — **메커니즘 핵심** (Fig 4)
Li(110)/argyrodite(100) 계면, 300 K, 50 ps.
- **Fig 4a**: Li-LPSCl 초기 구조(노랑 S·보라 P·연두 Cl·진녹 Li). **Fig 4b**: 20 ps 스냅샷 — **reduced P + 미반응 Li 층**(PS₄ 깨짐). **Fig 4c**: LPSCl₁.₅ 20 ps — **unbroken PS₄ tetrahedron + reduced P 1개만** = 분해 덜 됨.
- **P–S RDF(Fig 4d–f)**: 모든 sulfide가 ≈2.02 Å P–S(PS₄³⁻). **Li-LPSCl: 10 ps 후 2.02 Å peak 급감 = PS₄ 분해**(Fig 4e). **Li-LPSCl₁.₅: 35 ps까지 2.02 Å 유지 = 훨씬 느린 분해**(Fig 4f). → Cl-rich가 환원에 **동역학적으로 더 안정**.
- **Li-P RDF(Fig 4g–i)**: reduced LiₓPᵧ(≈2.5 Å) 형성. LPSCl이 더 빨리·많이 LiₓPᵧ 생성. 즉 **PS₄³⁻ + P → Li가 환원 → LiₓPᵧ**(실험 XPS와 일치). LPSCl₁.₅는 fully-reduced P 1개뿐.
- **요지**: 두 모델 차이는 **4a/4d Cl 함량뿐** → **고-Cl이 reduction 저항을 본질적으로 높인다**.

### 5.9 Li/argyrodite post-mortem XPS (본문, Fig S10)
대칭셀 cycling 후. **PS₄³⁻ 특성 P 2p(131.9 eV) peak이 Li/LPSCl 계면서 더 약함** = LPSCl이 더 분해. S 2p·Cl 2p(Fig S10b,c)도 Li-LPSCl₁.₅서 **LiCl 더 많고 Li₂S 적음** = Cl-rich가 LiCl-rich(절연) SEI·Li₂S(전도) 적음. → AIMD를 실험으로 확증.

### 5.10 Full cell (NCM811) (Fig 5, 6)
- **Li-In 음극(Fig 5a,b)**: NCM/LPSCl 141 mAh/g·CE 72.0 % vs NCM/LPSCl₁.₅ **155.4·77.6 %**, 100 cyc 유지율 **83.8 %**. → 고-Cl이 NCM과의 부반응도 억제(CE↑).
- **양극 EIS(Fig 5c,d, Table S3)**: cycling 후 mid-freq 반원(양극-SE 계면저항) LPSCl **276 Ω** ≫ LPSCl₁.₅ **142.8 Ω**. → NCM/LPSCl 부반응이 더 심함.
- **양극 post-mortem XPS(Fig 5e,f)**: cycled NCM/LPSCl이 **산화 S(sulfate/sulfite)·산화 P(oxidized phosphorus) 더 많고 argyrodite 상 적음** → NCM 계면 산화가 더 격함. (Zuo의 cathode-side 결론과 *방향 일치*: 고-Cl이 NCM 계면 산화 산물 적음 — 단 Zuo는 "gas diversion/polysulfide", 본 논문은 단순히 "less oxidized solid".)
- **Li 금속 음극(Fig 6a–c)**: NCM/LPSCl/Li **130.2→43.1 mAh/g(유지율 30.6 %)** + **12th cycle soft short**(충전 중 전압강하, Fig 6c) vs NCM/LPSCl₁.₅/Li **151.4·80.4 %**(100 cyc, 안정).
- **Fig 6d 종합 도식**: Cl-rich의 3대 이점 — ① **cathode/electrolyte 계면 highly stable CEI**(less oxidation·low R), ② **enhanced Li⁺ conduction ~8 mS/cm·activated inter-cage jumps**, ③ **anode/electrolyte LiCl-rich SEI**(dendrite 억제·환원 안정).

## 6. 메커니즘 종합
1. **결정화(annealing)**: LPSCl = σ가 결정화도에만 의존(전 온도 순상, 격자 불변). LPSCl₁.₅ = LiCl이 격자에 용해(450 °C)되며 **S²⁻/Cl⁻ 무질서 61.7 % + 셀 수축** → σ 본질적 향상; 단 over-/under-anneal 시 LiCl·thio-LISICON 불순물이 σ 깎음(좁은 window).
2. **Li 전도**: 무질서가 **inter-cage 호핑 통로** 개방(Fig 2g) → MSD 3배·등방. (intra-cage cage-hop만으론 σ 한계.)
3. **음극 안정**: 고-Cl이 (a) AIMD로 본 **PS₄³⁻ 환원 분해를 동역학적으로 지연**(P–S 2.02 Å 35 ps 유지), (b) **LiCl-rich SEI**(고표면에너지·저전자전도) 형성 → 전자전달 차단·dendrite 억제. → CCD↑·대칭셀 500 h·full cell 80.4 %.
4. **양극 안정**: 고-Cl이 NCM과의 산화 부반응 산물(oxidized S/P)도 적게 → R_cat 낮음(142.8 < 276 Ω), CE↑.

## 7. 전체 논증 흐름
Cl↑ → (as-milled σ 2×) → annealing 시리즈 XRD/Rietveld(LPSCl 결정화도만 / LPSCl₁.₅ 무질서 61.7%+수축, 좁은 window) → σ 8.0·Ea 0.28(@450) + AIMD inter-cage 활성화(MSD 3×) ⟹ **Cl-rich σ 본질적↑** → CCD 1.40 + 대칭셀 500 h + AIMD/RDF(PS₄ 35 ps 유지) + XPS(LiCl↑·Li₂S↓) ⟹ **Cl-rich 음극 안정(dendrite·환원)** → full cell 80.4 % + R_cat 142.8 ⟹ **셀 전체 우수** → Fig 6d 3대 이점 도식으로 닫음.

## 8. DFT/계산 방법 상세 ★ (재확인)
| 항목 | 값 |
|---|---|
| code/level | VASP, PAW, **PBE-GGA** |
| 무질서 | **enumerate 모든 대칭구별 구조 → lowest-electrostatic(Ewald) single-config** (SQS 아님) |
| 계면 | Li(110)//argyrodite(100), lattice mismatch <5% |
| AIMD | **NVT**, **2 fs**, **50 ps**, **Γ-only**, lower ecut, **300 K**(계면) / **900 K**(bulk 확률밀도·MSD) |
| 설정 정합 | Materials Project (relaxation·energy) |
| post-proc | **pymatgen-diffusion**(prob. density·MSD), **vaspy/vasppy**(RDF) |
| 핵심 산출 | (1) bulk Li 확률밀도·MSD(inter-cage), (2) **계면 P–S·Li–P RDF의 시간(0–50 ps) 진화 heatmap**(분해 추적) |
| 한계 | bulk σ/Ea **AIMD 절대값 본문 미보고**(상대/정성만); 단일 배열이라 무질서 앙상블 평균 아님; Γ-only·lower ecut(정확도 trade-off, 대규모 계면 비용 탓) |

> 우리 관점: 이 AIMD 셋업은 **우리 것과 동급/유사**(VASP/PBE/NVT/Γ급, MP 정합). 차이 = (1) **계면 RDF 시간추적**(우리는 grand-potential 정적 hull로 *산물*만, 동역학 분해속도는 못 봄) — 차용 가치 높음. (2) 무질서를 **enumerate→lowest-Ewald single config**(우리 modelc도 유사 철학 — SQS 아님). (3) bulk σ는 본문서 실험 EIS에 위임(Excel 계산시트의 AIMD σ 0.43/14.55는 본 PDF 본문에 *근거 수치 없음* → 인용 시 "Excel 메타데이터, 본문 미확인"으로 표기).

## 9. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 합성 도식 + 사이트(Cl 90%@4a·60%@4d, S 16e, P 4b) | 우리 modelc 4a/4d Cl 분포 시각 레퍼런스 |
| 1b,c | annealing XRD (LPSCl 순상 vs LPSCl₁.₅ LiCl/thio-LISICON window) | **Cl 용해한계·2차상 = modelc(Cl1.6) 실재 위험** 직접증거 |
| 1d,e | Rietveld(격자 9.85→9.81, 무질서 13.3→61.7%) | 무질서↑↔σ↑ 실험 정량(우리 D↑/Ea↓ 짝) |
| 2a | σ bars(8.0 @450) | 문헌 σ anchor; comp1→modelc D비(2.6×)와 비교 |
| 2b | Ea(0.28 최저) | 우리 Ea 0.224 modelc와 같은 결(Cl-rich 낮음) |
| 2c,d | Nyquist·Arrhenius | 표준 |
| **2e–g** | **Li 확률밀도(intra-cage→inter-cage 활성화)** | **우리 inter-cage 멘탈모델·percolation의 직접 시각 증거** |
| S5 | MSD 3×·등방 | inter-cage 망 정량 |
| 3a–c | CCD(0.95/1.40/1.08) | dendrite↔σ·Cl 함량 분리(σ가 주) |
| 3d,e | 대칭셀 500 h·short | 음극 안정 직접증거 |
| S7 | 계면저항 cycling(34→50 vs 65→600) | 음극 계면 열화 속도 |
| **4a–c** | **계면 스냅샷(LPSCl PS₄ 깨짐 / LPSCl₁.₅ unbroken)** | **환원분해 시각화** |
| **4d–i** | **P–S·Li–P RDF 시간 heatmap(10 ps vs 35 ps 분해)** | **★ 분해 *속도*를 RDF 시간추적으로 — 우리 grand-potential(정적)이 못 보는 동역학 차용 1순위** |
| S8 | LPSCl₁.₅ 계면(4a/4d Cl만 다름) | 변수 통제(Cl 함량만) |
| S9,S10 | Li–S/Li–Cl RDF, post-mortem XPS(P 131.9·S 2p·Cl 2p) | LiCl↑·Li₂S↓·PS₄↓ 실험확증 |
| 5a–f | full cell Li-In·EIS·XPS(sulfate/oxidized P) | 양극 계면 LPSCl 더 산화(R 276 vs 142.8) |
| 6a–d | full cell Li metal + **3대 이점 도식** | deck "Cl-rich 종합 이점" 한 장 |

## 10. Post-processing ★
- **Rietveld(FullProf)**: XRD → 격자상수·**4d S²⁻/Cl⁻ 무질서 %**. 기록 = R_wp/R_p·점유.
- **EIS/Arrhenius**: σ(RT)·Ea(25–65 °C). 펠릿 360 MPa.
- **CCD(step-increased)**: 전압 급강하 onset = critical current. step 0.064 mA/cm².
- **AIMD Li 확률밀도**(pymatgen-diffusion): intra/inter-cage 통로 시각화. + **MSD 3방향**.
- **계면 RDF 시간추적**(vaspy): P–S(2.02 Å, PS₄)·Li–P(2.5 Å, LiₓPᵧ) peak의 **0–50 ps heatmap** → 분해 *속도* 정량(언제 PS₄ 깨지나). ← **본 논문의 가장 독창적 도구**.
- **post-mortem XPS**(XPSPEAK): P 2p 131.9(PS₄)·S 2p·Cl 2p·sulfate/oxidized P. C 1s 284.8 보정.
> 우리 적용: **계면 RDF 시간추적**으로 "Cl-rich 분해가 *더 느리다*"를 동역학으로 — 우리 grand-potential(어떤 산물·thermo onset)을 **AIMD 계면 RDF(분해 *속도*)** 로 보완하면 "Cl-rich 음극 이점"의 thermo+kinetic 양면.

## 11. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | Liu(이 논문) | 우리(DFT) | 일치/차이 + 이유 |
|---|---|---|---|
| Cl-rich σ↑ | 2.62→8.0 mS/cm(exp, +무질서 inter-cage) | D(600K) 3.09→**7.90×10⁻⁶**(2.6×), Ea 0.253→**0.224** | **✓✓ 같은 방향·기전**(무질서·inter-cage). 절대값은 EIS RT vs 우리 AIMD 외삽 → Arrhenius로만 비교 |
| inter-cage 활성화 | Fig 2g 확률밀도, MSD 3× 등방 | 우리 percolation/inter-cage 분석·D↑ | **✓✓ 직접 시각 정합** — 우리 "inter-cage 멘탈모델"의 *문헌 그림 증거* |
| 무질서 정량 | Rietveld 4d 13.3→61.7 % | modelc = Cl-rich enumerate single-config | **✓ 같은 물리**(무질서↑↔σ↑, Klerk). 우리도 SQS 아닌 단일배열 |
| Ea | 0.28 eV(@450, 최저) | modelc **0.224 eV** | **✓ 같은 결**(Cl-rich 낮음). 절대값 차 = exp vs AIMD·무질서 배열 의존 |
| 음극 환원 분해 *속도* | AIMD RDF: PS₄ LPSCl 10 ps / Cl-rich 35 ps 유지 → **Cl-rich 환원 동역학 더 안정** | 우리 grand-potential = **0V 환원산물만**(Li₃P+Li₂S+LiCl, thermo) — **분해 *속도* 못 봄** | **△ 보완 관계**: 우리=어떤 산물(thermo)·동일 화학; Liu=얼마나 빨리(kinetic). 둘 다 LiCl/LiₓPᵧ/Li₂S. **"Cl-rich 음극 유리"의 kinetic 증거를 Liu가 제공**(우리 정적 hull 밖) |
| 음극 환원 산물 | XPS: LiCl↑·Li₂S↓·LiₓPᵧ | comp1/modelc 0V → **Li₃P + Li₂S + LiCl** | **✓ 동일 chemistry**. LiCl=절연 passivator(우리 sei_products LiCl 6.65 eV) → Liu의 "LiCl-rich SEI 이점"에 우리 gap이 의미부여 |
| 음극 Cl-rich 유불리 | **Cl-rich 유리**(CCD 1.40·500 h, AIMD 느린 분해, LiCl SEI) | (우리 ESW=thermo onset만) | **[Lu]와 같은 진영**(Cl-rich 음극 유리, LiCl passivation). [GG](moderate 유리)와는 충돌 → §E 화해표 참조 |
| 양극 NCM 계면 | Cl-rich 산화 산물 적음(R 142.8<276, oxidized S/P↓) | grand-potential이 [Zuo]Eq1/Eq2 분해 stoich 재현 | **✓ 방향 일치**(고-Cl이 NCM 계면 덜 산화). 단 Liu는 "less oxidized solid"만, Zuo의 gas/polysulfide diversion 메커니즘은 없음 |
| 격자 수축(Cl-rich) | a 9.85→9.81 Å | 우리 EOS V0 254.16→**243.29 Å³/fu**(modelc 더 작음) | **✓✓ 일치** — Cl-rich 셀 수축 |
| 산화 onset(intrinsic) | (직접 ESW 계산 없음) | comp1=modelc **2.256 V**(S²⁻-limited) | n/a — Liu는 intrinsic ESW 안 봄(annealing·계면만) |
| 기계(E/B/G) | n/a (측정·계산 없음) | E_VRH 22.06→27.66 | n/a |
| 전자구조(gap) | n/a | comp1 2.066 / modelc 2.099 (PBE) | n/a |

## 12. 적용 인사이트 (깊게)
1. **inter-cage 멘탈모델의 *문헌 시각 증거*** (가장 큰 수확): Fig 2e–g가 "LPSCl=intra-cage trap / Cl-rich=inter-cage 활성화"를 Li 확률밀도로 직접 그린다. 우리 percolation/inter-cage 서사(comp1→modelc D↑·Ea↓)의 **그림 레퍼런스**로 deck에 인용 가능 — 그리고 우리 cascade의 **`migration_volume_fraction`(bottleneck/inter-cage 창)** 개념과 정확히 맞물림(Liu13 hydrate analogy의 "window→trap/cross"를 *실제 argyrodite Li*로 본 셈).
2. **계면 RDF 시간추적 = 우리 grand-potential의 kinetic 보완**: 우리 ESW는 *어떤 산물(thermo)*만 — Liu의 P–S RDF heatmap(10 ps vs 35 ps)은 *얼마나 빨리 분해되나(kinetic)*. **"Cl-rich 음극 유리"를 우리는 thermo onset 동일로만 보고 못 했는데, Liu가 AIMD kinetic으로 채움** → 우리 H목록(못 하는 것)의 "음극 분해 동역학"을 메우는 외부 증거. 향후 우리도 Li//argyrodite AIMD RDF 가능(셋업 동급).
3. **modelc(Cl 1.6) 용해한계 = 실재 위험**: LPSCl₁.₅(Cl 1.5)서 이미 LiCl·thio-LISICON 불순물이 **450 °C 좁은 window**서만 소멸, 550 °C 재석출. → **Cl 1.6은 더 위험**, 우리 modelc를 "이상적 단일상"으로만 다루면 실험 현실과 괴리. deck·논문서 2차상 명시.
4. **Cl-rich 음극 유리 진영 보강([Lu]와 동맹)**: Liu = "Cl-rich가 AIMD로 환원 느림 + LiCl-rich SEI"로 **음극 유리**. [Lu](4d-Cl 자기분해→LiCl passivation)와 같은 결론, [GG](과안정 → moderate Cl 유리)와 충돌. §E 화해표: **"Cl 양"이 아니라 "LiCl 절연 SEI 형성 여부"가 관건** — Liu는 그 SEI를 XPS로 직접 봄.
5. **σ↔CCD 분리 정량**: Fig 3a–c가 같은 Cl-rich라도 σ(450>550)가 CCD를 지배(1.40>1.08)함을 보임 → "dendrite 억제 = σ(전류 균일화) *주* + Cl 함량(LiCl SEI) *부*"의 깔끔한 분해. 우리 "σ는 device 레버" 서사와 정합.
6. **정직한 한계 표기**: 본 PDF는 **bulk AIMD σ 절대값을 본문서 안 줌**(Excel의 0.43/14.55 mS/cm는 메타데이터, 근거 수치 미확인) → 인용 시 "AIMD는 정성/상대(MSD·확률밀도)만, σ 절대값은 EIS 실험"으로.

## 13. 인용 가능 문장
- "Liu et al. visualize the intra-cage→inter-cage transition directly via AIMD Li⁺ probability density: in Li₆PS₅Cl Li is trapped in Li₆S octahedra, whereas in Li₅.₅PS₄.₅Cl₁.₅ inter-cage pathways activate (MSD ≈3× larger, isotropic) — the picture behind our comp1→modelc D increase."
- "Interface AIMD RDF shows PS₄³⁻ (P–S 2.02 Å) breaks within 10 ps against Li for LPSCl but survives to 35 ps for the Cl-rich phase — a kinetic complement to our static grand-potential reduction chemistry (both give Li₃P/Li₂S/LiCl)."
- "Even before annealing, the Cl-rich electrolyte is ≈2× more conductive (1.10 vs 2.13 mS/cm); Cl raises σ intrinsically through S²⁻/Cl⁻ disorder (Rietveld 13.3→61.7 % at 4d), not merely through crystallinity."
- "The Cl-rich phase only reaches phase purity in a narrow 450 °C window — LiCl and thio-LISICON impurities reappear otherwise — a real caution for our modelc (Cl 1.6) being treated as a single phase."

## 14. 주의/한계 (over-claim 방지)
- **≠ Zuo 2022 Angew** (다른 그룹·DOI·초점: Liu=음극+annealing+AIMD / Zuo=양극+ToF-SIMS/DEMS). INDEX Excel exp#10·calc#10의 DOI 혼선 정정 필요.
- **bulk AIMD σ 절대값 본문 미보고** — Excel 0.43/14.55 mS/cm는 본 PDF서 근거 못 찾음 → 인용 금지(또는 "메타데이터, 본문 미확인").
- AIMD = **단일 lowest-Ewald 배열·Γ-only·lower ecut·50 ps** → 무질서 앙상블 평균 아님, 절대 분해속도 정량보단 *상대 비교*(LPSCl vs Cl-rich)로만.
- 계면 RDF "10 ps vs 35 ps"는 두 모델의 *상대* 분해속도; 절대 시간척도는 짧은 AIMD라 정량 약함.
- σ "8.0 mS/cm"는 **LPSCl₁.₅-450 특정 시료**; annealing window 좁아 재현 민감(불순물).
- full cell 전압 = Li⁺/Li(Li 음극) 또는 Li-In — 본문 표기 따라 음극 명시.
- Cl-rich "음극 유리"는 [Lu]와 동맹이나 [GG]와 충돌 → 단일 결론 금지, 축(LiCl SEI 형성 여부) 명명.
- 합성 "ball milling 1 h" vs Exp "150 rpm 1 min" 표기 불일치(그룹 선행공정 인용 탓) — 공정 세부는 ref38 원전.
- **Klerk 재인용 원문 대조 (2026-07-28, `deklerk2016_diffusion_site_disorder_argyrodite.md` §13)**: §2의 "Klerk … 75% 무질서 시 최고" — **핵심은 정확**(de Klerk 원문: 4d(=Klerk 표기 4c, cage-center) **Cl 점유 75 %=4a:4c 1:3에서 limiting jump rate 최대, 50:50 대비 2×** — SI Table S2 정밀값 6.20/3.12×10¹⁰ s⁻¹=1.99×, σ_J 기준 300–600 K 일관; 단 **Li₆PS₅Cl(Cl 1.0)·분포당 단일 배열·σ_J(limiting-rate) 지표** 조건부 예측이고 σ*_MSD 기준으론 600 K 역전). 두 가지 주의: ① "무질서↔σ 양의 관계"는 **비단조**(0 %·100 % 모두 저전도 — all-4c는 doublet 붕괴로 σ 급락)를 단조로 축약한 표현; ② Klerk 최적은 Cl 1.0 기준이라 LPSCl₁.₅(실측 61.7 %)에 그대로 적용은 원문도 경고한 외삽(X·조성별 최적 상이 명시). 2024 MTP-MLIP 대규모 재검(INDEX 계산#8)은 25 % 피크 보고=최적 % 자체가 방법 의존.

## 15. 기법 용어 미니사전
- **annealing(소결)**: ball-milled glass-ceramic을 가열해 결정화. 결정화도(peak/bg 비)·불순물·격자상수 제어.
- **thio-LISICON**: Li₄GeS₄형 황화물 이온전도체. 여기선 LPSCl₁.₅ 저온 annealing서 생기는 *불순물 상*(σ 깎음).
- **4d S²⁻/Cl⁻ 무질서**: argyrodite 4d Wyckoff 자리를 S²⁻·Cl⁻가 공유 점유하는 비율. 높을수록 Li 호핑 통로↑→σ↑(Klerk).
- **intra-cage vs inter-cage**: Li₆S 팔면체 *안* 호핑(intra, 갇힘) vs *사이* 호핑(inter, 장거리 전도). inter 활성화가 고-σ 관건.
- **probability density(Li)**: AIMD 궤적서 Li 위치 점유 밀도 3D map → 확산 통로 시각화(pymatgen-diffusion).
- **MSD**: mean square displacement; 기울기 ∝ 확산계수 D. 3방향 분해로 등방성 판별.
- **RDF g(r)**: radial distribution function; 특정 원자쌍 거리 분포. P–S 2.02 Å=PS₄³⁻, Li–P 2.5 Å=환원 LiₓPᵧ. **시간(0–50 ps) heatmap으로 분해 속도 추적**.
- **CCD (critical current density)**: dendrite로 short 나기 직전 최대 전류밀도. step-increased로 측정.
- **lowest-electrostatic(Ewald) config**: 부분점유·무질서 구조를 enumerate 후 Madelung(Ewald) 에너지 최저 배열 선택(SQS 대안, AIMD 비용 절감).
