# Cho 2026 (Energy Storage Materials 89 (2026) 105186, DOI 10.1016/j.ensm.2026.105186) — 전자-이온 폴리머 복합막(EIPC=GO+PAA) + PCET 반응으로 Zn 음극 안정화 (수계 Zn-ion, AZIB)

**인용:** Yanghyun Cho§, Nayeon Jung§, Jongha Hwang, Minhee Park, Won Bo Lee, Chi Keung Song,
Wonseok Hyun, **Yong Min Lee**, Ga Young Jeong, **Bumjoon Seo\***, **Myung-Jun Kwak\***,
**Woo-Jin Song\***, "Electronic-ionic polymer composite with proton-coupled electron transfer
reaction: From low N/P ratio to high zinc utilization for aqueous zinc ion batteries",
*Energy Storage Materials* 89 (2026) 105186, DOI 10.1016/j.ensm.2026.105186.
접수 2025-12-23 / 수정 2026-04-28 / 게재확정 2026-05-02 / 온라인 2026-05-03.
§Yanghyun Cho·Nayeon Jung 동등기여.

**소속:** (1) Dept. of Chemical Eng. & Applied Chemistry, **충남대(Chungnam Nat'l Univ, CNU)** —
제1저자 Y. Cho / 교신 W.-J. Song; (2) Dept. of Chemical & Biological Eng. + (c) Transdisciplinary
Innovations, **서울대(SNU)** — N. Jung·W. B. Lee; (d/e) Dept. of Battery Eng. + Chemical &
Biomolecular Eng., **연세대(Yonsei)** — **Yong Min Lee**; (f) Materials Science & Eng.,
**금오공대(Kumoh Nat'l Inst. Tech.)** — W. Hyun; (g) **광주과기원(GIST)** — G. Y. Jeong; (h)
Advanced Batteries Research Center, **한국전자기술연구원(KETI, Seongnam)** — 교신 M.-J. Kwak; (i)
Chemical & Biomolecular Eng., **서울과기대(SeoulTech)** — 교신 B. Seo; (j) Organic Materials Eng.
+ (k) Inst. for Carbon Fusion Tech.(InCFT), **충남대**. 교신 bseo@seoultech.ac.kr ·
myngjoon@keti.re.kr · wjsong@cnu.ac.kr.

★★ **LEAD = Woo-Jin Song(충남대) + Bumjoon Seo(서울과기대) + Myung-Jun Kwak(KETI).**
**Yong Min Lee(연세대 DTBL)는 공저자**(주도 아님) — DTBL 핵심 #266/#285/#286과 달리 협업·주변부.

**소재계:** ★ **수계 Zn-ion 전지(AZIB)** — **Zn metal 음극** 표면에 **EIPC(electronic-ionic polymer
composite) = 그래핀옥사이드(GO) + 폴리(아크릴산)(PAA, M_w≈240k) 8:2 복합막**을 spin-coating(0.5 wt%
PAA-GO 용액, ~1.5 µm 두께)으로 코팅(EIPC@Zn). 전해질 = **2 M ZnSO₄ 수계**(coin: 75 µL, pH ~4.45).
양극(상대) = **Zn₀.₂₅V₂O₅(ZVO, 하이드로써멀)** 표준 full-cell, 추가로 **Na₂V₆O₁₆(NVO)·AC@I₂·MnO₂**
(파우치, dry-process PTFE 바인더 75:20:5, >22 mg cm⁻²). 음극 Zn foil 250 µm(coin)·10 µm(파우치/고DOD).
★★ **우리 LPSCl sulfide ASSB가 아니다** — **수계 Zn²⁺ 화학 + Zn 금속 음극 표면 코팅(고분자막·PCET·
desolvation·덴드라이트)**. 우리 프로젝트(sulfide ASSB **양극** 압축 + 수송, Li⁺, DEM 접촉망 + MPM 소성)와
**이온(Zn²⁺ ≠ Li⁺)·전극(음극 ≠ 양극)·물리(도금/덴드라이트/탈용매 ≠ 입자압축/접촉전도)가 전부 다르다.**

**한 줄 핵심 변수:** **EIPC 막의 "전자전도(rGO)+이온조절(PAA)" 이중기능 + PCET(proton-coupled electron
transfer)** — 산성 전해질에서 GO가 Zn에 의해 **rGO로 환원**(전자전도↑)되고, PAA의 −COOH가 Zn²⁺와 배위
+ GO에 양성자/전자 동시이동(PCET) → **Zn²⁺ 탈용매 촉진·002-배향 Zn 도금·덴드라이트/HER 억제**.

★ **"electronic-ionic"의 의미(혼동 절대금지):** 제목의 "전자-이온"은 **Zn 음극 위 고분자 코팅막의 혼합전도**
(rGO 전자전도 + PAA 이온조절)를 뜻한다 — **우리 복합양극의 σ_e/σ_ionic 접촉망과 무관**. 같은 단어지만
**물리·전극·이온이 전부 다르다**(아래 §6 비교 참조).

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 (매우 낮은) 관련성

**GO+PAA 전자-이온 복합막(EIPC)을 Zn 금속 음극에 코팅하면, 산성 전해질에서 GO→rGO 환원으로 전자전도를 얻고
PAA의 PCET 반응이 Zn²⁺ 탈용매(desolvation E_a 28.23→9.44 kJ mol⁻¹)와 배위를 조절해, 002-배향의 균일·무덴드
라이트 Zn 도금(DOD ≈51%·calendar 300 h·CE 99.70% over 3000 cycles)을 달성하고, MnO₂ 파우치셀에서 낮은
N/P 0.74·높은 DOD ≈85%를 100 cycle 안정 구현한다** — DFT(결합·탈용매·proton-transfer 에너지)로 메커니즘을
세우고 EIS/XRD/SEM/XPS로 검증.

**우리 프로젝트 관련성(매우 낮음, TIER-4):** 이 논문은 **수계 Zn-ion 전지의 Zn 금속 음극 표면 고분자 코팅**
(EIPC·PCET·Zn²⁺ 탈용매·덴드라이트/HER 억제)이다 — 우리 **LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM 양극
압축·수송(Kirchhoff/Holm σ triad)**과 이온(Zn²⁺ vs Li⁺)·전극(음극 vs 양극)·소재(수계 GO/PAA ≠ LPSCl/NMC811)·
물리(도금/탈용매/덴드라이트 ≠ 고체입자 압축·접촉전도)가 전부 다르다. **Yong Min Lee는 공저자(주도 아님).**
제목 "electronic-ionic"은 **Zn 음극 코팅막의 혼합전도**일 뿐 **우리 양극 transport 네트워크가 아니다.**
**transport/압축/σ/porosity 앵커가 절대 아니다**(그건 Bazzoun(LPSCl)·Varkey(halide)·Minnmann이 담당).
**관련성을 부풀리지 않는다.**

---

## 1. 배경 / 동기 (Introduction + §2.1, p.1–2)

- **AZIB의 약속과 문제.** 수계 Zn-ion 전지 = 높은 이론용량(Zn 음극 **820 mAh g⁻¹ / 5854 mAh L⁻¹**), 낮은
  작동전압(−0.76 V vs SHE), 저가·안전(수계). 그러나 **Zn 음극의 본질적 무질서 도금(disordered deposition)**이
  실용화를 막음.
- **수계 부반응.** 전극-전해질 계면에서 수화 Zn²⁺(H₃O⁺ 환원) → **수소발생반응(HER)** → 느슨한 황산아연수산화물
  (Zn₄SO₄(OH)₆·xH₂O, ZHS) 형성 → 이온선택성 결여 → 직접접촉·표면불균일 → 분극↑·덴드라이트↑·수명↓.
- **표면개질 전략.** Zn 음극 표면보호막이 직접접촉·부반응·덴드라이트를 물리적으로 막음. 고분자막(유연·등각 코팅)이
  무기막보다 유리. 특히 **극성 작용기(C=O, −COOH)** 다수 보유 폴리머가 다수의 **transient Zn²⁺ 흡착site** 제공
  → Zn²⁺ 수송 강화·자유수 침투 차단·HER 억제. GO = 큰 표면적·다수 산소작용기로 Zn²⁺ 흡착·이온이동 촉진 후보.
- **GO의 한계.** GO는 강한 π-π로 **재적층(restack)·응집** → 용매 내 불균일 분산 → 불균일막·낮은 전기전도. →
  구조설계로 GO 기반 복합막의 Zn²⁺ 수송·계면안정성 제어 필요.
- **본 연구(명시):** **PAA + GO 전자-이온 복합막(EIPC)** — PAA의 다수 −COOH가 GO의 −OH/epoxy와 **강한 수소결합
  + 정전기 상호작용** → π-π 재적층/응집 억제·분산↑. 핵심: PAA-GO 사이 **PCET(proton-coupled electron transfer)**
  → 전자밀도 재분배 → Zn²⁺ 탈용매 안정화. ⇒ EIPC@Zn: 대칭셀 DOD ≈51%·calendar 300 h·CE 99.70% over 3000 cyc·
  MnO₂ 고로딩(25.8 mg cm⁻²) 파우치 저-N/P 0.74·고-DOD ≈85% 100 cyc.

**약어:** AZIB=aqueous zinc-ion battery; EIPC=electronic-ionic polymer composite; GO/rGO=(reduced)
graphene oxide; PAA=poly(acrylic acid); PCET=proton-coupled electron transfer; DOD=depth of discharge;
N/P=음극/양극 용량비; HER=hydrogen evolution reaction; ZHS=Zn₄SO₄(OH)₆·xH₂O(황산아연수산화물); EDL=
electric double layer; ZVO=Zn₀.₂₅V₂O₅; NVO=Na₂V₆O₁₆; t_Zn²⁺=Zn²⁺ 수송수(transference number); SAICAS=
표면/계면 절삭분석; CPC=cumulative plating capacity; RTC=relative texture coefficient.

---

## 2. 소재 & 제작 (Experimental Section, SI)

### 2.1 EIPC@Zn 코팅 (Fig 1, Fig S1–S18)
- **GO 합성:** modified Hummers법(흑연+NaNO₃+H₂SO₄+KMnO₄ → H₂O₂·HCl 세척 → 동결건조).
- **EIPC 코팅(spin-coating):** **GO 분말 : PAA 바인더 = 8:2(질량비)**, DI water 용매로 **0.5 wt% PAA-GO 용액**
  (sonication 1 h + 1일 교반). Zn foil(250 µm, IPA/아세톤/에탄올 세척) 위에 1000 rpm 30 s → 3000 rpm 60 s →
  50 °C 1 h 건조. **막 두께 ~1.5 µm**(SEM/EDS, Fig S4 — 균일 carbon층, Zn 청색·C 주황).
- **GO→rGO 자발 환원:** Zn foil을 산성 전해질(2 M ZnSO₄, pH 4~5)에 담그면 **Zn → Zn²⁺ 산화 + GO → rGO 환원**
  (−0.4 V vs SHE @ pH 4–5에서 redox 개시) → 표면 갈변·암화(Fig S13). Raman G–D' (PAA-rGO@Zn) ≈25 = C/O ~500
  (명확한 rGO 환원, Fig S6).
- **비교 폴리머:** PVDF-GO(소수성·약 vdW), CMC-GO(친수성이나 수계에서 Na⁺ 해리로 GO 결합 약화) vs PAA-GO.
  동일 8:2·0.5 wt% 조건. → PAA-GO만 균일·강접착(아래 §3·§4).

### 2.2 양극·셀 (Experimental Section, SI)
- **ZVO 양극:** Zn₀.₂₅V₂O₅(하이드로써멀 210 °C 48 h). ZVO:carbon black:PVDF = 7:2:1, Ti foil, 면로딩 ~2 mg cm⁻²,
  12 mm 디스크. 추가 양극: **NVO**(Na₂V₆O₁₆), **AC@I₂**(활성탄+I₂ 1:1, PAA 바인더 8:1:1, ~2 mg cm⁻²).
- **MnO₂ 파우치(실용 검증):** **dry-electrode(solvent-free) PTFE 바인더** MnO₂:Super P:PTFE = 75:20:5,
  three-roll mill 압연·프레스, **>22 mg cm⁻²**(고로딩), 30×40 mm. 음극 = 10 µm Zn(bare/EIPC, 이론용량
  ~5.8548 mAh cm⁻²), GF/C separator 260 µm, 전해질 **2 M ZnSO₄ + 0.4 M MnSO₄(1.5 mL)**, 진공실링·24 h 휴지.
- **DFT(SI):** **VASP 6.2.0, PAW-PBE + DFT-D3(BJ), cutoff 450 eV, (2×2×1) k-mesh, EDIFF 1e−5 eV·force
  0.05 eV/Å, VASPsol 암시적 용매(ε_water=78.4), Zn(002) 4층 슬랩(하단 2층 고정).** 탈용매: [Zn(H₂O)ₙ]²⁺
  (n=6,5,4,3) ORCA B3LYP/def2-TZVP 최적화 → VASP 재이완. DOS/PDOS(3×3×1, LORBIT=11). 분자 MEP는 B3LYP/def2-TZVP.

### 2.3 측정 (Experimental Section, SI)
- coin CR2032, 2-전극. 대칭셀(Zn‖Zn)·비대칭(Zn‖Cu, stripping cutoff 0.5 V)·full(ZVO/NVO/AC@I₂). EIS 1 MHz–
  100 mHz(10 mV). CP 1 mA cm⁻²/1 mAh cm⁻². CA −150 mV. LSV 1 mV s⁻¹(HER, Zn‖Ti). 4-point probe(전도도).
  SAICAS(계면접착, 0.5 N → 0.2 N). XRD texture coefficient(TC/RTC, std Zn PDF 00-004-0831).

---

## 3. 핵심 메커니즘 — PCET 중심 4축 (§2.1–2.4)

**(1) PAA–GO 수소결합·정전기 → GO 안정화(재적층/응집 억제).** PAA 다수 −COOH가 GO −OH/epoxy와 강한 수소결합
(FT-IR O–H 신축 2800–3800 cm⁻¹ blue-shift, Fig 2a) + 정전기. → π-π 재적층 억제·분산안정(zeta PAA-GO **−17.9 mV**
최고, vs PVDF −10.9 / CMC −10.8 mV, Fig S16) → 균일·등각 막. PAA-GO C=C(1648)·C–O–C(1062) 피크 감소 +
1566 cm⁻¹ 비대칭 신축 → **GO 부분환원·sp² 회복**(PCET 정합). SAICAS 접착: PAA-GO **149.8 N m⁻¹** > CMC 144.4 >
PVDF 138.7; peel-off 1.9 N(최강).

**(2) PCET(양성자-전자 동시이동) → GO 환원 + Zn²⁺ 탈용매 안정화.** PAA의 −COOH가 GO에 **양성자(H⁺) 공급 +
전자이동**을 동시에(PCET) → 산소작용기 제거·sp² 국소회복 → GO→rGO(전자전도↑). XPS C 1s: PAA-GO sp² C–C
**19.38%**↑·C=O↓. ⇒ rGO 전자전도 + PAA 이온조절 = **전자-이온 혼합전도막**. 부분탈수 계면 [Zn(H₂O)ₓ]²⁺
(x=5,4,3) 안정화 → 탈용매 장벽↓.

**(3) DFT 결합·전하재분배 + proton-transfer 에너지.** (아래 §5 DFT 표 참조.) PAA-GO 결합에너지 **−1.498 eV**가
가장 강함(monolayer 흡착; vs PVDF −0.412 / CMC −0.602). CDD(Fig 3a): PAA-GO에서 계면 전하재분배(전자축적/고갈)
가장 광범위 → 강한 전자결합. 계면 proton-transfer 에너지 ΔE_PT(Fig 3c): **Zn(002)에서 +0.307 eV**(양수 = 양성자
보유 −COOH 상태가 더 안정 → Zn 표면엔 H* 흡착이 불리), **GO에서 ~0 eV**(epoxy-O로 양성자이동 용이) → **PAA는
Zn보다 GO로 양성자를 더 쉽게 넘김** = PCET이 Zn이 아니라 GO 환원으로 가는 정합. DOS/PDOS: PAA-GO가 E_F 근처
상태밀도 최대(±0.1/0.2 eV 윈도, Table S2) → 계면 전자전달 유리.

**(4) Zn²⁺ 강한 흡착·낮은 탈용매장벽 → 002-배향 균일 도금.** Zn²⁺ 흡착에너지(Fig 4h): bare Zn **−6.23 eV** →
EIPC@Zn **−7.42 eV**(더 음수 = 강한 흡착) → Zn²⁺-rich EDL 형성. 누적 탈용매(Fig 4g): bare Zn은 6→5/5→4/4→3 전부
양수(ΔE 0.324/0.405/0.032 eV) vs EIPC@Zn 6→5 **−0.094 eV**(음수)·이후 0.584/0.058 → 누적 탈용매 EIPC가 더 낮음
→ **부분탈수 Zn²⁺ 안정화·탈용매 촉진**. ⇒ 002-배향(I(002)/I(100) bare 0.42 → EIPC **1.13**, RTC 002↑) 균일·무덴
드라이트 도금.

⇒ 우리 식으로: **음극 표면 고분자막이 (전자전도 rGO + 이온조절 PAA + PCET 탈용매)으로 Zn 도금 균일성·계면화학을
제어** — 모두 **음극측 도금 동역학·탈용매·SEI/계면화학**이 주체. 우리 모델은 **양극측 입자압축·접촉전도**이며,
도금/덴드라이트/탈용매/PCET를 다루지 않는다. **개념·수치·메커니즘 차용 없음**(아래 §6).

---

## 4. 섹션별 결과 — 모든 수치 (Results, p.2–8)

### 4.0 헤드라인 수치 (Abstract + Conclusion)
| 지표 | 값 | 비고 |
|---|---|---|
| **대칭셀 DOD(고DOD 수명)** | **≈51%**(50 µm Zn, 15 mA cm⁻²/15 mAh cm⁻²) | abstract 핵심 |
| **calendar(휴지) 수명** | **300 h**(intermittent calendar) | vs bare Zn 149 h |
| **쿨롱효율 CE** | **99.70% over 3000 cycles**(Zn‖Cu, 4 mA cm⁻²/1 mAh cm⁻²) | CPC 3040 mAh cm⁻² |
| **MnO₂ 파우치 N/P** | **0.74**(저-N/P 실용) | 고DOD ≈85%, 25.8 mg cm⁻² |
| **MnO₂ 파우치 DOD** | **≈85%** | 100 cyc 안정 @1 A g⁻¹ (76.52% @100th) |
| **대칭셀 장수명** | **1500 h @ 1/1**(overpotential **36.12 mV**) | vs bare Zn fail @96 h(short) |
| **Zn²⁺ 수송수 t_Zn²⁺** | **0.82**(PAA-rGO@Zn) | vs PVDF 0.75 / CMC 0.63 (Table S1) |
| **탈용매 활성화에너지 E_a** | bare **28.23** → EIPC **9.44 kJ mol⁻¹** | Arrhenius(R_ct vs T, Fig 4c) |
| **부식전류 I_corr** | bare **1.85** → EIPC **0.47 mA cm⁻²** | Tafel, 내식성 **75%↑**(Fig 4a) |
| **교환전류 i₀** | bare **4.82** → EIPC **5.95 mA cm⁻²** | 도금/탈리 동역학(Fig S37) |
| **XRD I(002)/I(100)** | bare **0.42** → EIPC **1.13** | 100 cyc 후 002-배향(Fig 4f) |
| **Zn²⁺ 흡착에너지(DFT)** | bare **−6.23** → EIPC **−7.42 eV** | Fig 4h |
| **PAA-GO 결합에너지(DFT)** | **−1.498 eV**(monolayer) | vs PVDF −0.412 / CMC −0.602 (Fig 3a) |

### 4.1 EIPC 계면 형성/물성 (Fig 1–2, §2.1–2.2)
- **FT-IR(Fig 2a):** PAA-GO O–H 신축 blue-shift(2800–3800 cm⁻¹) = PAA −COOH ↔ GO −OH/epoxy 수소결합(인접 GO 간
  결합 아님). C=C(1648)↓·C–O–C(1062)↓·1566 cm⁻¹ 비대칭 신축 출현 → GO 부분환원·sp² 회복.
- **Raman(Fig 2b):** I_D/I_G — PVDF-GO 0.99 / CMC-GO 0.96 / **PAA-GO 1.04**(구조왜곡↑·sp² 복원↑·G밴드 blue-shift).
- **XPS(Fig S10–S12):** PAA-GO sp² C–C **19.38%**↑·C=O↓(PCET 정합). Zn 2p PAA-GO **1021.6 eV** red-shift =
  강한 Zn-O 극성결합·계면 전하이동.
- **UPS/work function(Fig S14–S15):** PAA-GO **4.04 eV**(최저, vs PVDF 3.65 / CMC 3.86) → 계면 전자전달 유리.
- **4-point probe(Fig S23):** PAA-rGO@Zn 시트저항 **177.81 Ω sq⁻¹**·전도도 **37.7 S cm⁻¹** > CMC-rGO@Zn
  250.68 Ω sq⁻¹·26.5 S cm⁻¹ → rGO 전자전도 우위.
- **areal capacitance(Cu‖Cu, CV, Fig 2e):** PVDF-rGO 10.81 / CMC-rGO 11.99 / **PAA-rGO 43.23 mF cm⁻²**
  → PAA-rGO EDL Zn²⁺ 흡착site 풍부.
- **핵생성 과전위(Fig 2f, @1 mA cm⁻²):** PVDF-rGO 24 / CMC-rGO 21 / **PAA-rGO 26 mV**(주: 본 도표에선 PAA가 미세히
  높으나 — 핵생성장벽 자체보다 **균일성/배향**이 본 논문 강조점; Zn‖Cu CV 기준 EIPC nucleation overpotential은
  bare 대비 유의 감소). 도금형상(Fig 2g, Fig S22): PVDF-rGO 돌출·CMC-rGO 불균일 덴드라이트 vs **PAA-rGO 매끈·미세·
  무응집** = 균일 핵생성.
- **t_Zn²⁺(Fig 2d, Table S1):** PAA-rGO **0.82**(R₀ 137.40·R_s 156.23 Ω, I₀ 139.24·I_ss 31.73 µA) > PVDF 0.75 >
  CMC 0.63 → 농도구배·덴드라이트 억제.

### 4.2 DFT 메커니즘 (Fig 3, §2.3)
- **결합에너지(monolayer 흡착, Fig 3a):** PVDF-GO −0.412 / CMC-GO −0.602 / **PAA-GO −1.498 eV**(최강). (SI Fig S26:
  bilayer intercalation 형상에선 PAA-GO −1.850·CMC-GO −2.411 eV — 형상의존.) CDD: PAA-GO 계면 전하재분배 가장 광범위.
- **proton-transfer 에너지 ΔE_PT(Fig 3c):** Zn(002) **+0.307 eV**(−COOH 보유 상태가 안정 → Zn 표면 H* 불리),
  GO **~0 eV**(epoxy-O로 양성자이동 용이) → PAA는 Zn보다 GO로 양성자 우선이동(PCET → GO 환원). C2 탄소 sp³→sp²
  복원(C–C 1.455→1.430 Å, out-of-plane 0.178→0.061 Å, ∠C–C–C 118.52°→119.82°).
- **DOS/PDOS(Fig 3d–f, Table S2):** PAA-GO E_F 근처 total/C 2p/O 2p PDOS 최대(±0.1·±0.2 eV 윈도) → 계면 전자전달 유리.

### 4.3 내식성·Zn 도금 거동 (Fig 4, §2.4)
- **Tafel(Fig 4a):** GO→rGO 환원전위 양의 shift(−9.5 → −7.0 mV) → I_corr bare 1.85 → EIPC **0.47 mA cm⁻²**
  (내식성 **75%↑**). 14일 침지(Fig S30–S31): bare Zn ZHS 육방시트 다수 vs EIPC 매끈·ZHS無.
- **calendar(Fig 4b):** 24 h 휴지 intermittent → EIPC **300 h** > bare Zn **149 h**(self-corrosion 억제).
- **탈용매 E_a(Arrhenius, Fig 4c, Table S3):** R_ct(30–70 °C) bare Zn 1057→330.9 Ω / EIPC 277.5→179.7 Ω →
  **E_a bare 28.23 → EIPC 9.44 kJ mol⁻¹**(탈용매·계면전하이동 촉진).
- **CA 확산(Fig 4d, −150 mV):** bare Zn 점증 전류(2D 확산·Zn²⁺ 응집) vs EIPC 안정 전류(3D 확산·균일 flux).
- **i₀(Fig S37):** EIPC **5.95** > bare **4.82 mA cm⁻²**.
- **100 cyc 형상/XRD(Fig 4e,f):** bare Zn 불규칙·덴드라이트 vs EIPC 매끈·무덴드라이트. I(002)/I(100) bare 0.42 →
  EIPC **1.13**(002 수평배향), RTC 002↑(Table S4: EIPC 002 24.43% vs bare 10.35%).
- **HER(Fig S29, LSV):** H₂ onset bare Zn −0.86 V → EIPC **−1.49 V**(vs Zn²⁺/Zn) → HER 유의 억제.
- **DFT 흡착(Fig 4h):** Zn²⁺ bare −6.23 → EIPC **−7.42 eV**; 누적 탈용매 EIPC < bare(Fig 4g).

### 4.4 대칭셀 수명·가역성 (Fig 5, §2.5)
- **1/1 장수명(Fig 5a):** Zn foil 250 µm(DOD 0.7%) — EIPC **1500 h** 안정·overpotential **36.12 mV**, bare Zn
  96 h 후 단락(전압요동·dead Zn).
- **고DOD(Fig 5c):** 50 µm Zn(**DOD 51%**) 15 mA cm⁻²/15 mAh cm⁻²; 10 µm Zn(**DOD 17%**) 15 mA cm⁻² **150 h** 안정
  → 높은 Zn 이용률에서도 무단락·가역.
- **Zn‖Cu CE(Fig 5d):** **avg CE 99.70% @3040th**(4 mA cm⁻²/1 mAh cm⁻²) / 99.57% @152th. **CPC 3040 mAh cm⁻²**.
  voltage polarization ΔV bare 78.58 → EIPC **58.42 mV**(Fig 5e). 고율 8 mA cm⁻²까지 저과전위(Fig 5b).
- **고율 10 mA cm⁻²(Fig S39):** EIPC 900 h 저·가역 hysteresis. 저온(Fig S41): EIPC 무-soft-short, 저온 계면탈용매.
- **문헌비교(Fig 5f, Table S5):** CPC 3040·cycle 3040·avg CE 99.70% — 최근 Zn 비대칭셀 보고 대비 우위.

### 4.5 Full-cell 실용 검증 (Fig 6, §2.6)
- **ZVO(Fig 6a,b):** EIPC@Zn‖ZVO 초기용량↑·저분극, **용량유지 77.63% @2000th**(4 A g⁻¹, avg CE 99.93%) vs bare
  불안정·soft short. 율속 0.1–0.5 A g⁻¹ EIPC 우위(Fig 6c). 자기방전(Fig 6d, 24 h 휴지): EIPC **86.3%** > bare 80.3%.
- **NVO(Fig 6e, Fig S48):** EIPC@Zn‖NVO **용량유지 97.46% @4700th**(3 A g⁻¹) — 장수명.
- **AC@I₂(Fig S50):** EIPC@Zn‖I₂ 율속 1–5 A g⁻¹ 안정.
- **MnO₂ 파우치(Fig 6f, Fig S51, Table S6):** **고로딩 25.8 mg cm⁻²(>22)·N/P 0.74·DOD 85%·10 µm Zn**, 1 A g⁻¹에서
  **avg CE 99.09% @100th·용량유지 76.52% @100th** → 저-N/P·고-DOD 실용조건 검증. (N/P 계산: ρ_Zn 7.14·Zn 820·
  cathode 308 mAh g⁻¹·면적 12 cm², anode 5.8548 / cathode 6.8684–7.9464 mAh cm⁻².)

---

## 5. 그림 한 장씩 — 무엇을 보이고 (우리는 거의 안 씀)

- **Fig 1:** EIPC@Zn 계면 — (a) 모식: spin-coating PAA-GO → 산성전해질에서 PAA-rGO 자기조립·H⁺ 유도환원, (b) GO
  안정화·PCET·수소결합 모식 + 용매구조 안정화(Zn²⁺ 흡착·빠른 탈용매).
- **Fig 2:** PVDF/CMC/PAA-rGO@Zn 비교 — (a) FT-IR(수소결합), (b) Raman I_D/I_G(0.99/0.96/1.04), **(c) 4-point
  전도**, (d) t_Zn²⁺(0.75/0.63/**0.82**), (e) areal capacitance(10.81/11.99/**43.23 mF cm⁻²**), (f) 핵생성 과전위
  (24/21/26 mV), (g) 도금 메커니즘 모식(vdW 응집 / 정전 불균일 / **배위 균일**).
- **Fig 3:** ★ DFT — **(a) CDD + 결합에너지(PVDF −0.412 / CMC −0.602 / PAA −1.498 eV)**, (b) PAA-GO sp³→sp² 국소
  복원, **(c) proton-transfer 에너지(PAA-Zn +0.307 / PAA-GO ~0 eV)**, (d) total DOS, (e) GO-C 2p PDOS, (f) GO-O
  2p PDOS(PAA-GO E_F 근처 최대).
- **Fig 4:** ★ Zn²⁺ 배위·탈용매 — (a) Tafel(I_corr 1.85→0.47, η 75%↑), (b) calendar 300 vs 149 h, **(c) Arrhenius
  E_a 28.23→9.44 kJ mol⁻¹**, (d) CA 2D vs 3D 확산, (e) 100 cyc SEM, **(f) XRD I(002)/I(100) 0.42→1.13**, (g) 누적
  탈용매 프로파일, **(h) Zn²⁺ 흡착 −6.23→−7.42 eV**, (i) Zn²⁺ 배위결합 모식.
- **Fig 5:** EIPC@Zn 대칭셀 — **(a) 1/1 1500 h(36.12 mV) vs bare 96 h 단락**, (b) 율속 0.5–8 mA cm⁻², (c) 고DOD
  51%(50µm)·17%(10µm), **(d) Zn‖Cu CPC 3040·avg CE 99.70%**, (e) V곡선 ΔV 58.42 vs 78.58 mV, (f) 문헌비교(CPC/
  cycle/CE), (g) 도금 모식(bare 부식·HER·덴드라이트 vs EIPC 무덴드라이트).
- **Fig 6:** full-cell 실용 — (a) ZVO CV, **(b) ZVO 77.63% @2000th**, (c) ZVO 율속, (d) 자기방전 86.3 vs 80.3%,
  **(e) NVO 97.46% @4700th**, **(f) MnO₂ 파우치 N/P 0.74·DOD 85%·25.8 mg cm⁻²·76.52% @100th**.

### SI 주요(스킴): S1 PAA-GO 수소결합 모식, S2 PAA비율별 핵생성/대칭셀, S3 PAA-GO 결합site, **S4 EIPC@Zn SEM/EDS
(~1.5 µm)**, S5 Raman G-매핑(균일·스크래치), S6 PAA-rGO Raman(C/O~500), S9 수소결합 비율, S10–S12 C 1s·Zn 2p XPS
(sp² 19.38%·Zn-O 1021.6 eV), S14–S15 UPS work function(PAA-GO 4.04 eV), **S16 zeta(PAA-GO −17.9 mV)**, S17 SAICAS
(149.8 N m⁻¹)·peel(1.9 N), S19 EIS(t_Zn²⁺용), **S23 4-point(PAA-rGO 177.81 Ω sq⁻¹·37.7 S cm⁻¹)**, S24 MEP(PVDF/
CMC/PAA), S26 bilayer 결합에너지(PAA −1.850·CMC −2.411 eV), S27 PAA-Zn intact/deprotonated, **S29 HER onset
−1.49 vs −0.86 V**, S30–S31 14일 침지(ZHS), **S34 EIS vs T(Table S3)**, S37 i₀(5.95 vs 4.82), S39 10 mA 900 h,
S40 in-situ EIS DOD 51%, S44 ZVO N/P~1.7, S45 NVO 사전사이클, S48 NVO, S50 AC@I₂ 율속, **S51 MnO₂ 파우치 N/P 0.74·
DOD 85%**, **Table S1 t_Zn²⁺(0.75/0.63/0.82)**, Table S4 RTC(002 24.43 vs 10.35%), Table S5 문헌비교, **Table S6
N/P(0.74 — anode 5.8548 / cathode 6.8684·7.9464 mAh cm⁻²).**

---

## 6. 기술 미니용어집 (우리 맥락)

- **EIPC(전자-이온 폴리머 복합막):** GO(rGO 환원 시 전자전도) + PAA(−COOH 이온조절) 혼합전도 코팅막. ★ "electronic-
  ionic" = **음극 표면막의 혼합전도**(전자 rGO + 이온 PAA)이지 **우리 복합양극의 σ_e/σ_ionic 접촉망이 아니다.**
- **PCET(proton-coupled electron transfer):** 양성자+전자 동시이동 — PAA −COOH가 GO에 H⁺·e⁻ 동시공급 → GO 환원·
  Zn²⁺ 탈용매 안정화. 우리 ASSB transport엔 PCET 축 없음(고체전해질·전자화학반응 없음).
- **desolvation(탈용매) / E_a:** 수화 [Zn(H₂O)ₙ]²⁺에서 H₂O 제거 장벽(Arrhenius R_ct vs T). bare 28.23 → EIPC
  9.44 kJ mol⁻¹. 우리는 **무용매 고체 SE 입자 압축**이라 탈용매 축 없음.
- **t_Zn²⁺(수송수) / EDL:** 음이온 대비 Zn²⁺ 수송분율(EIS+CA). PAA-rGO 0.82. 우리 σ_ionic는 **고체 SE 접촉망 Li⁺
  전도**(Kirchhoff/Holm)이지 전해질 수송수가 아니다.
- **DOD / N/P / CPC:** depth of discharge(Zn 이용률)·음극/양극 용량비·누적도금용량 — 셀설계 지표. 우리 양극 압축/
  porosity와 무관.
- **002-배향 / RTC:** Zn(002) 우선배향(수평 도금·무덴드라이트). XRD texture. 우리 morphology엔 도금배향 축 없음.
- **HER / ZHS:** 수소발생·황산아연수산화물 부산물(수계 부반응). 우리 ASSB엔 수계 부반응 없음.
- **DFT 흡착·CDD·proton-transfer 에너지:** Zn(002) 슬랩 위 폴리머/Zn²⁺/H⁺ 흡착·전하재분배(VASP-PBE+sol). = 분자/
  슬랩 스케일 DFT(우리 DFT-DEM=입자접촉 σ_grain). 스케일 달라 상보 아님.

---

## ★ 7. 비교 vs 우리 DEM+MPM — 짧고 정직하게 (TIER-4 / 주변부, 모델 영향 0)

⚠ **대전제:** 이 논문은 **수계 Zn-ion 전지의 Zn 금속 음극 표면 고분자 코팅막**(EIPC=GO+PAA·PCET·Zn²⁺ 탈용매·
덴드라이트/HER 억제·002 배향)이다. 우리 모델은 **LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM 양극 압축 + 수송
(Kirchhoff/Holm σ triad, Li⁺)**다. **이온(Zn²⁺ vs Li⁺), 전극(음극 도금 vs 양극 압축), 소재(수계 GO/PAA·
ZnSO₄ ≠ LPSCl SE/NMC811·무전해질), 스케일(분자/슬랩 DFT·EIS ≠ 입자 DEM/연속체 MPM), 물리(도금/탈용매/덴드라이트/
PCET ≠ 고체입자 압축·접촉전도)가 전부 다르다.** **Yong Min Lee는 공저자(주도 아님)** → DTBL 핵심 #266/#285/#286과
달리 협업·주변부.

### ★ "electronic-ionic" 단어 — 우리 σ_e/σ_ionic 네트워크가 절대 아니다 (혼동 금지)
- 제목의 "electronic-ionic polymer composite"는 **Zn 음극 위 ~1.5 µm 고분자 코팅막의 혼합전도**(GO→rGO 전자전도
  + PAA −COOH 이온조절)를 가리킨다. — 이는 **막(film) 단위 혼합전도**이지, 우리가 다루는 **복합양극 입자 접촉망의
  σ_electronic(AM-AM Kirchhoff) + σ_ionic(SE-SE Kirchhoff) + σ_thermal triad**와 **물리·스케일·전극이 전부 다르다.**
  같은 단어를 본다고 우리 transport 네트워크 맥락으로 끌어오지 않는다. **수치·폼·메커니즘 전이 없음.**

### 우리 우위 / frame[5] (간단)
- 그들: **음극측 도금 동역학·덴드라이트/HER 억제·PCET·Zn²⁺ 탈용매·002 배향 + 분자/슬랩 DFT(VASP+sol) + 수계 EIS·
  full-cell·파우치(저-N/P·고-DOD).** 강력하지만 **양극 입자압축역학 없음·explicit 접촉 σ triad(ionic/e/thermal) 없음·
  소성 입자 morphology 없음·압력→미세구조→σ 예측 없음**(우리 DEM+MPM 영역).
- 우리: **압력→미세구조→σ(ionic/e/thermal) 예측 + MPM 소성 void-fill/morphology + voxel FV + fracture.** 그들 분자/
  슬랩 DFT는 우리 입자스케일 모델과 **스케일이 달라 상보조차 아님.**
- ⇒ **이 논문은 우리 파이프라인의 입력단도 출력단도 아니다.** 순수 문헌 맥락(수계 Zn 음극 코팅막·PCET·탈용매).
  **모델 하자/검증/앵커 어느 것도 아님 — TIER-4 유지.**

### 비교 요약표
| 축 | Cho 2026 (#279, EIPC@Zn·수계 AZIB) | 우리 (LPSCl ASSB, DEM+MPM) | 판정 |
|---|---|---|---|
| 이온·전극·스케일 | Zn²⁺ 음극 도금막(GO/PAA·분자 DFT) + 수계 ZnSO₄ | Li⁺ LPSCl SE+NMC811 양극 입자 접촉망 | ⚠ 전부 다름 — 전이불가 |
| "전자-이온" 의미 | 음극 코팅막의 혼합전도(rGO+PAA) | 양극 입자 접촉망 σ_e+σ_ionic triad | ✗ 동음이의 — 물리 무관 |
| 핵심 물리 | Zn 도금·PCET·탈용매·덴드라이트/HER | 입자압축·접촉 σ·소성 void-fill | ✗ 대응 안 됨 |
| DFT | 분자/슬랩 흡착·CDD·proton-transfer(VASP+sol) | 입자스케일 DFT-DEM(σ_grain) | 스케일 달라 상보 아님 |
| 수치 앵커 | ✗ (수계·음극·도금) | Bazzoun/Varkey/Minnmann/#266 | **앵커 아님** |

---

## ★ 8. 우리 작업에 넣을 인사이트 — 정직하게 없음

1) **모델 영향 0 — 순수 문헌 맥락(아카이브 완전성 항목).** 이 논문은 우리 DEM+MPM transport/압축 어디에도 꽂히지
   않는다(수계 Zn 음극 코팅막 + PCET + 탈용매 + 덴드라이트/HER). 가치는 **"DTBL Yong Min Lee 공저 논문 카탈로그
   완전성"** 뿐. **수치·폼·메커니즘 전이 없음.**

2) **"electronic-ionic" 동음이의 주의(혼동 절대금지).** 그들 "전자-이온"은 **음극 위 GO/PAA 코팅막의 혼합전도**
   (rGO 전자 + PAA 이온)이고, 우리 "전자-이온"은 **양극 입자 접촉망의 σ_e+σ_ionic triad**다. 같은 단어지만 전극·
   스케일·물리가 전부 다르다 — 제목만 보고 transport 앵커로 오인하지 않는다.

3) **DFT 스케일 구분 명확화(상보 아님).** 그들 DFT = **분자/슬랩 흡착·proton-transfer 에너지(VASP+sol, GO/Zn(002)
   슬랩)**; 우리 DFT-DEM = **입자스케일 σ_grain 앵커**. 둘은 스케일이 달라 cross-validation도 division-of-labor도 아니다.

### 보너스 실행 항목
- **#279 인덱스 갱신**(완료): 1줄 카탈로그 행을 검증 수치로 보강(EIPC=GO+PAA 8:2·~1.5 µm·PCET; DOD ≈51%·calendar
  300 h·CE 99.70% @3000·MnO₂ 파우치 N/P 0.74·DOD ≈85%·25.8 mg cm⁻²; t_Zn²⁺ 0.82·E_a 28.23→9.44 kJ mol⁻¹·I_corr
  1.85→0.47·002 I-ratio 0.42→1.13·Zn²⁺ 흡착 −6.23→−7.42 eV; LEAD=Song/Seo/Kwak, Y.M.Lee 공저). **TIER-4(· 타
  화학계) 유지.**
- ⚠ **역할 구분(혼동 금지):**
  - **#279(이 논문, EIPC@Zn·수계 AZIB):** **수계 Zn 음극 코팅막·PCET·탈용매.** 모델 영향 0, TIER-4. "전자-이온"
    동음이의 — 우리 σ 네트워크 아님.
  - **#280(Choi, 탄성 Li metal anode·액체):** 음극 도금 계면공학 + 응력완화 테마 먼 인접(TIER-4).
  - **#282(Kim, c-CNF/NCM811·액체):** PFAS-free 바인더 맥락 + 전하→분산 개념 인접(TIER-3).
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann이 담당.**
- DFT 보충데이터(분자/슬랩 흡착·CDD)는 우리 입자스케일과 무관 → 파싱·DB화 불필요(노트만 유지).
