# Impact of the Chlorination of Lithium Argyrodites on the Electrolyte/Cathode Interface in Solid-State Batteries — Zuo et al. (Angew. Chem. Int. Ed. 2022/2023)

> slug `zuo2022_chlorination_cathode_interface` · DOI `10.1002/anie.202213228` · type `exp (+ DFT 보조)` · PDF `d0102fe3-Angew…Zuo….pdf` · digested `2026-06-23` · status ✅
> **저자**: Tong-Tong Zuo, Felix Walther, Jun Hao Teo, Raffael Rueß, Yubo Wang, Marcus Rohnke, Daniel Schröder, Linda F. Nazar, Jürgen Janek (Giessen / KIT / Braunschweig / Waterloo) · 62, e202213228

---

## 0. 이 digest를 읽는 법
이 논문은 **"Cl을 더 넣으면(LPSCl→Li5.5PS4.5Cl1.5) 산화안정성은 나빠 보이는데 셀 성능은 왜 더 좋아지나?"** 라는 역설을 실험으로 푼다. 핵심 통찰: **분해의 "양"(electrochemical decomposition)과 분해 "산물의 질"(어떤 CEI가 생기나)은 별개**이고, Cl-rich는 더 많이 분해되지만 *덜 해로운 산물*(기체 SO₂·폴리설파이드 ↑, 저항성 고체 sulfate/phosphate ↓)을 만들어 계면 저항이 덜 오른다.

> ⚠ **전압 기준**: 본문 대부분 **In/InLi 기준**. Li/Li⁺ 기준 = **+0.62 V** (예: 3.7 V vs In/InLi ≈ 4.32 V vs Li/Li⁺). 메커니즘의 "≥4.2 V"는 Li/Li⁺ 기준.

## 1. 한 줄 요약
Cl-rich(Li5.5PS4.5Cl1.5)는 LPSCl보다 **더 쉽게/많이 전기화학 분해**(CV 전류 2×, 낮은 onset, DSC/TGA 덜 안정)되지만, 고전압서 NCM 산소와의 반응 산물이 **기체(SO₂)·폴리설파이드로 더 빠지고 고체 산화물(sulfate/phosphate)을 덜 만들어** → 계면 저항 증가율이 낮고(8.9 < 13.2 Ω·h⁻⁰·⁵) → **셀 성능·수명이 더 좋다**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교 | **Li6PS5Cl (Cl 1.0)** vs **Li5.5PS4.5Cl1.5 (Cl 1.5)** |
| 양극 | 단결정 **NCM85** — H2-H3 전이서 격자 O 방출하는 고-Ni |
| 질문 | halogenation이 (a) SE 전기화학 분해, (b) cathode 계면 화학 분해를 어떻게 바꾸나 |
| 갭 | 기존(Kraft/Gautam)은 halide가 σ↑까지만; **계면 안정성 영향 미지** |
| 선행(Dewald/Tan) | LPSCl 산화 = **S²⁻→폴리설파이드(S⁰/Sₓ²⁻)** 지배; CAM 접촉 시 oxygenated S/P 추가 분해; NCM의 O₂/¹O₂가 SE와 반응해 SO₂ |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSCl | Li5.5PS4.5Cl1.5 | 출처/조건 |
|---|---|---|---|
| σ (RT) | **2.9 mS/cm** | **7.0 mS/cm** | 본문 (intro: 소결 시 12까지) |
| XRD 불순물 | 없음 | **LiCl** (35°,50°) | Fig S1 (Cl 용해한계) |
| CV 산화전류 | 1× | **~2×** | Fig 1a,b (SE/C, 0.05 mV/s, 20 wt% C65) |
| CV peak 위치 | — | **동일** | Fig S2 → 메커니즘 같음 |
| CV onset | 기준 | **더 낮음(apparent)** | Fig S2 |
| 완전산화 전자수 | **5 e⁻/f.u.** | **4 e⁻/f.u.** | Reaction 1–3 |
| DSC 융점/결정화 | 535/532 °C | **523/493 °C** | Fig S3a (incongruent) |
| TGA 질량손실 onset | 없음 | **315 °C** | Fig S3b |
| R_cat 증가율(√t) | **13.2 Ω·h⁻⁰·⁵** | **8.9** | Fig 2d (NCM85, 3.7 V, 30 h) |
| 초기 충/방전(0.5C) | 215/165 | 215/**170** | Fig 3, CE 77%→**79%** |
| 50 사이클 | 133 | **145 mAh/g** | Fig 3 |
| O₂(DEMS) | 6.7 | 6.8 µmol/g (≈동일) | Fig 6, SOC>80% |
| SO₂ | 적음 | **많음** | Fig 6 |

## 4. 재료 & 방법
- **합성**: 고상 반응. Cl1.5엔 LiCl 잉여상 동반.
- **CV 전극**: SE + **20 wt% C65** (분해 증폭), 대극 In/InLi.
- **셀**: NCM85(단결정)+SE 복합양극 / SE 분리막 / In(Li). 0.5C=0.96 mA/cm².
- **기법**: CV(0.05 mV/s) · EIS+TLM · GITT · ToF-SIMS(aging 60 h@3.7 V, cycling 100회 후) · DEMS(C/20, 45 °C, 2–3.9 V, O₂ m/z32·SO₂ m/z64) · DSC/TGA · XRD.
- **이론**: 분해 반응식(Reaction 1–3) 단순화. (상세 hull 비중 작음 → 우리 grand-potential이 보완·검증, §11)

## 5. 결과 — 섹션별 상세

### 5.1 합성·전도도·상순도
σ 2.9→7.0 mS/cm (Cl↑). 단 **Cl1.5에 LiCl 불순물**(XRD 35°/50°) — Cl 과량이 용해한계 넘어 석출. (→ modelc Cl1.6도 잠재 이슈)

### 5.2 CV — 전기화학 분해 (Fig 1a,b, S2)
SE/카본 복합서 Cl1.5가 **~2× 산화전류**, **peak 동일**, **onset 더 낮음**. 해석: (a) 더 취약, (b) 메커니즘 동일. 2× = "더 많이" 또는 "더 완전히" 분해.
🔑 **critical**: 2× ≈ σ비(2.4×) → 상당부분 **전도도(접근성)** 효과 가능 (intrinsic 반응성으로만 보면 과대). 본문은 "equal carbon contact 가정".

### 5.3 분해 반응식 (Reaction 1–3)
1. `Li6PS5Cl → LiCl + Li3PS4 + S + 2Li⁺ + 2e⁻`
2. `Li5.5PS4.5Cl1.5 → 1.5 LiCl + Li3PS4 + 0.5 S + Li⁺ + e⁻` ← 첫 산화 **전자 1개(LPSCl의 절반)**, LiCl 1.5배
3. `Li3PS4 → 0.5 P2S5 + 1.5 S + 3Li⁺ + 3e⁻`
🔑 **핵심 비대칭**: Cl-rich는 *덜 격하게* 분해(전자 적게)하고 **불활성 LiCl을 더** 만든다 → 산물이 덜 해로움의 화학적 뿌리.

### 5.4 DSC/TGA (Fig S3)
융점 535/532→523/493 °C + incongruent melting → Cl1.5 **열역학적으로 덜 안정**. TGA: Cl1.5만 315 °C부터 손실. → CV "낮은 onset"의 열역학 근거. (단 *bulk SE 자체* metastability — 0K hull 못 잡음, 우리 ESW 한계와 연결)

### 5.5 GITT (Fig S4a)
<3 V: 두 SE 내부저항 동일. >3 V: Cl1.5/C 저항 **더 빨리 증가**. 분해는 **전압 의존**.

### 5.6 ToF-SIMS (aging 전, Fig 1c,d)
S⁻ 증가: LPSCl **6.7×** vs Cl1.5 **10.4×**; Cl⁻: **5.1×** vs **6.7×**. Cl1.5 분해 더 많음.

### 5.7 임피던스/TLM (Fig 2)
3.7 V 충전 후 30 h, 25분마다 EIS. **Gerischer형** → **TLM**으로 R_ct·R_el·R_ion 분해. **R_cat=√(R_ct(R_el+R_ion))**. 증가율(√t): LPSCl **13.2** vs Cl1.5 **8.9 Ω·h⁻⁰·⁵** → **Cl-rich 계면 열화 느림**. 메커니즘: NCM 표면 전기화학 분해 + NCM **O 방출(>3.6 V vs In/InLi)** 화학 분해 (parabolic=복합).

### 5.8 사이클·rate (Fig 3)
초기 215/165(CE77%) vs 215/170(CE**79%**); 50cyc 133 vs **145**. 고율속 Cl1.5 우수. 4-셀 분해: **저C=복합양극 율속**, **고C=SE 분리막 σ 율속** → 고-σ Cl-rich 유리.

### 5.9 ToF-SIMS (cycling 100회 후) — **반전 핵심** (Fig 4, 5)
- S⁻·Cl⁻: 둘 다↑, Cl1.5 더 큼.
- **PO₃⁻/SO₃⁻ (산소관여 고체 = phosphate/sulfate)**: **LPSCl 더 많음, Cl1.5 적음**.
- **폴리설파이드 Sₓ⁻(S4+S5+S6)**: **Cl1.5 더 많음**.
- Fig 5 RGB: **PO₃/SO₄(sulfate) = NCM 쪽 안쪽층**, **Sₓ(폴리설파이드)=전해질 쪽 바깥층**.
→ Cl-rich 계면 = 저항성 고체 산화물 ↓, 기체/폴리설파이드 ↑ = **얇고 덜 저항성 CEI**.

### 5.10 DEMS (Fig 6)
**O₂**: NCM 격자서 SOC>80%(>4.2 V vs Li⁺/Li) 방출, **거의 동일(6.7 vs 6.8 µmol/g_NCM)**. **SO₂**: **Cl1.5 더 많이**. → 같은 O₂가 Cl-rich서 **고체 sulfate 대신 기체 SO₂로** = "gas diversion".

## 6. 메커니즘 종합 (Fig 7)
- **<4.2 V (vs Li⁺/Li)**: SE **전기화학 분해**(delithiation, S 산화) 지배 — Cl-rich가 더 분해.
- **≥4.2 V**: NCM **산소 방출**의 **oxygen-involving degradation** 지배 → 기체(SO₂)+고체(sulfate/phosphate).
- **차이**: LPSCl=산화 고체 더 → 두껍고 저항 큰 CEI. Cl-rich=기체+폴리설파이드로 더 빠짐 → 얇은 CEI → 낮은 R_int → 좋은 셀. (내부층=O₂+Li₂CO₃ 분해; 외부층=SE delithiation)

## 7. 전체 논증 흐름
σ↑ → CV 2×·낮은 onset + DSC/TGA 불안정 + ToF-SIMS S/Cl↑ ⟹ **Cl-rich 더 분해** → ToF-SIMS(PO₃/SO₃↓, Sₓ↑)+DEMS(SO₂↑) ⟹ **산물 덜 해로움** → R_cat 8.9<13.2 + 145>133 ⟹ **셀 더 좋다** → Fig 7로 닫음.

## 8. DFT/계산 방법 ★
실험 중심; 이론은 Reaction 1–3 단순화가 전부. DFT 디테일(functional·k·supercell)은 이 논문서 거의 없음 → **우리 grand-potential이 이 화학을 채워 검증**(§11).

## 9. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| S1 | XRD, Cl1.5 LiCl 불순물 | Cl 용해한계(modelc Cl1.6 잠재) |
| 1a,b | CV 2×·같은 peak | 분해 양 직접증거; peak동일=우리 onset동일 정합 |
| 1c,d | ToF-SIMS S/Cl (aging 전) | 분해 정도 정량 |
| S2 | CV onset/peak | "낮은 onset(apparent)" |
| S3 | DSC/TGA | 열역학 metastability(우리 ESW 못잡는 축) |
| S4 | GITT | 전압 의존 분해 |
| 2a–d | EIS+TLM, R_cat √t | 계면 열화 속도(8.9<13.2) 정량 |
| 3a–e | 사이클·rate·4셀 | 성능 우위+율속 병목(저C양극/고C분리막) |
| 4 | ToF-SIMS PO₃/SO₃ vs Sₓ | **반전핵심**: 고체산화물↓·폴리설파이드↑ |
| 5 | RGB 공간분포(내부 sulfate/외부 polysulfide) | CEI 층구조 |
| 6 | DEMS O₂(동일)·SO₂(↑) | gas diversion 정량 |
| 7 | 메커니즘(<4.2V 분해/≥4.2V O-deg) | 산화단계 도식(deck) |

## 10. Post-processing ★
- **CV**(SE/C, 0.05 mV/s): onset·전류로 산화 취약성. 기록=전류비·peak전위.
- **EIS→TLM**: Gerischer 피팅, R_cat=√(R_ct(R_el+R_ion)). 기록=√t 기울기(Ω·h⁻⁰·⁵).
- **GITT**: IR drop=내부저항, 전압스캔.
- **ToF-SIMS**: 음이온 2차이온 정규화 + depth/2D map. 기록=fold증가·종분포·RGB.
- **DEMS**: operando MS m/z32(O₂)/64(SO₂). 기록=µmol/g_NCM.
- **DSC/TGA**: 융점/결정화/질량손실 °C.
> 우리 적용: **TLM rate const + ToF-SIMS 종분리(고체산화물 vs 폴리설파이드/기체)** = "계면 분해 양 vs 질" 정량 틀 차용.

## 11. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`
| 항목 | Zuo(exp) | 우리(DFT) | 일치/차이+이유 |
|---|---|---|---|
| 분해 stoichiometry | Eq1 2e⁻+1.0LiCl / Eq2 1e⁻+1.5LiCl | comp1 1.75Li+1.0LiCl / modelc 0.7Li+1.6LiCl | **✓✓ 강한 일치** — grand-potential이 독립 재현(검증) |
| 산화 onset | same peak + apparent 낮음 | 2.14 V 동일(S²⁻-limited) | **✓ 일치** — Zuo "낮은 onset"=2×전류 apparent |
| Cl-rich 반응성(CV 2×) | 더 반응 | interface dE +2.5%(noise) | △ **2×≈σ비(2.4×) 접근성**, intrinsic 아님 |
| 셀 우수(R_cat↓) | gas diversion→얇은 CEI | **못 봄**(closed solid-hull, 기체상 X) | ✗ 한계 → 실험 인용 |
| metastability(DSC/TGA) | Cl-rich 덜 안정 | composition-기반 ESW ranking 불가 | ✗ 범위밖 → E_above_hull 보강 |

## 12. 적용 인사이트 (깊게)
1. **deck 프레이밍 확정**: "Cl-rich = intrinsic 분해는 많지만(낮은 onset·2×) 산물이 좋아(LiCl↑·기체↑·고체산화물↓) CEI 얇고 계면저항 덜 올라 → 셀 우수." Zuo가 실험 근거.
2. **우리 ESW 강점**: grand-potential이 Eq1/Eq2 분해 화학 독립 재현 → "검증됨".
3. **"2× 전류"=전도도(접근성)로 해석** — interface dE(+2.5%)는 noise라 intrinsic 주장 금지.
4. **산화안정성 축 명명**: 이 논문=계면 cycling 축(③) Cl-rich 승. intrinsic(①)·구속(②)·calendar(④)와 분리.
5. **정직한 한계**: gas diversion·metastability는 우리 모델 밖(기체상·무질서) → 향후 (a) 기체 chempot 계면, (b) E_above_hull(SQS).
6. **정량 틀 차용**: TLM rate const, ToF-SIMS 종분리 → 우리 계면 "양 vs 질" 도구.
7. **modelc Cl1.6 용해한계 주의**: Cl1.5서 이미 LiCl 불순물 → Cl1.6 더 위험, 2차상 명시.

## 13. 인용 가능 문장
- "Our grand-potential decomposition reactions reproduce Zuo et al.'s Eq1/Eq2 (fewer e⁻/Li and more inert LiCl for the Cl-rich phase), cross-validating the calculated chemistry."
- "The ~2× CV current of the Cl-rich electrolyte scales with its ~2.4× higher ionic conductivity → accessibility, not intrinsic reactivity."
- "Chlorination is a trade-off: more electrochemical decomposition but milder, gas-diverting products → lower interfacial resistance growth (8.9 vs 13.2 Ω·h⁻⁰·⁵) and better cycling (CE 79 vs 77%)."

## 14. 주의/한계
- Zuo Cl-rich=**Cl1.5**; modelc=**Cl1.6** (동일시 금지).
- "낮은 onset"=Fig S2 soft claim(apparent); **thermodynamic onset 동일**(같은 peak).
- 전압기준 혼용(In/InLi vs Li/Li⁺ +0.62 V).
- CV "equal carbon contact 가정" → 2×에 접촉/전도도 기여 포함 가능.
- NCM85 특정 — 다른 cathode면 O-degradation 다름.

## 15. 기법 용어 미니사전
- **CV**: 전위 스캔 전류; SE/카본서 산화전류=분해 속도.
- **TLM**: 다공성 복합전극 임피던스를 이온·전자·전하이동 저항 분해.
- **Gerischer impedance**: 화학반응+확산 결합 임피던스(계면 반응성).
- **GITT**: 전류펄스+이완 IR drop·확산; 여기선 전압별 내부저항.
- **ToF-SIMS**: 이온빔으로 깎으며 2차이온 질량분석 → 분해종 공간/깊이 분포.
- **DEMS**: operando 가스 질량분석(O₂/SO₂) — 기체 산물 정량.
- **CEI**: cathode-electrolyte interphase.
- **R_cat=√(R_ct(R_el+R_ion))**: TLM 유효 양극 저항.
