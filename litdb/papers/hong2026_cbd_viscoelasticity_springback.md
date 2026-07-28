# Hong 2026 (Energy Storage Materials, ENSM 105321) — CBD 점탄성이 단결정 cathode의 시간의존 Spring-Back을 억제

> slug `hong2026_cbd_viscoelasticity_springback` · DOI `10.1016/j.ensm.2026.105321` · type `FEM·digital-twin` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_hong2026_cbd_viscoelasticity_springback.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Rakhwi Hong†, Jingyu Choi†, Jaejin Lim, Seungyeop Choi, Dongyoon Kang, Wonseok Yang,
Yong Min Lee\*, "Modulating Carbon Binder Domain Viscoelasticity Suppresses Time-Dependent
Spring-Back in Single-Crystal Cathodes", *Energy Storage Materials* (2026),
DOI 10.1016/j.ensm.2026.105321 (PII S2405-8297(26)00453-8, ENSM 105321).
Journal Pre-proof. 접수 2026-04-03, 수정 2026-06-08, 게재확정 2026-06-20. © 2026 Elsevier B.V.

**소속:** Yonsei University — (a) Dept. of Battery Engineering, (b) Dept. of Chemical & Biomolecular
Engineering, (c) Dept. of Battery Convergence Engineering. = 이용민 **Digital Twin Battery Lab (DTBL)**.
†Rakhwi Hong, Jingyu Choi 동등기여. 교신 yongmin@yonsei.ac.kr. **이해상충 없음.** 지원: NST (GTL24012-000),
MOTIE Technology Innovation Program/HRD (2410009726·RS-2025-00437259, 2410010799·RS-2025-00420590).
언어편집에 ChatGPT 5.2 사용(과학적 해석·결론은 저자 검증).

**소재계:** ★ **고-Ni 단결정 양극 활물질(CAM)** = **LiNi₀.₈₆₅Co₀.₀₅₄Mn₀.₀₇₅Al₀.₀₀₇O₂ (NCMA)**
(POSCO Future M, single-crystal) + **CBD = Super P(Imerys) 도전재 + PVDF(Solef 6020, Solvay) 바인더** +
**액체전해질 1.15 M LiPF₆ EC/EMC 3:7 (v/v)**; full-cell 음극 = **인조흑연(SCMG-AR, Showa Denko)**.
조성 양극 NCMA:Super P:PVDF = **96:2:2 wt%**, Al foil(15 µm), 목표밀도 **3.5 g/cm³**.
★★ **우리 LPSCl sulfide ASSB가 아니다** — **액체전해질 일반 LIB 양극(단결정 NCMA)**.
이 그룹(이용민 연세대 DTBL)의 **#285** 논문 — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.

**한 줄 핵심 변수:** **calendering 온도** — RT(25 °C) vs **HT(80 °C)**. 샘플코드 4종:
**RC-P**(RT-calendered pristine), **RC-S**(RT stored, 3주 보관), **HC-P**(HT pristine), **HC-S**(HT stored).

DB 동반 파일: 없음(생성 안 함). 주요 수치는 본 MD 본문 표에 모두 정리. SI(`mmc1.docx`) 텍스트
(Fig S1–S17 + Table S1–S2)는 디제스트 본문에 반영. SI에 동영상/머신판독불가 자료 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**단결정 CAM은 기계적으로 견고해 압축에너지를 입자 파괴로 소산하지 못한다**(다결정은 입계 균열로
소산). 그래서 calendering 압축응력이 **CBD(carbon binder domain)에 탄성적으로 저장**되고, 보관 중
**수 주에 걸쳐 천천히 풀리며 두께가 되돌아온다 = 시간의존 spring-back**(되튐). **CBD는 점탄성체이고
그 점탄성은 온도의존적**이다 — **RT calendering → 탄성 CBD → 응력 저장 → spring-back**(3주 +4 µm);
**HT(80 °C) calendering → 고분자 사슬 이동도↑ → 점성/compliant CBD → 응력 소산 → spring-back 억제**(3주
+1 µm). spring-back 억제는 **CAM–CBD 계면접촉↑ + pore 망 균질화 → 전자전도망 보존 → 저항증가 완화 +
장기 전기화학성능 보존**으로 이어진다.

**우리 hook (가장 중요, 2갈래):**
1. ✅ **검증:** 그들의 "**견고한 단결정 CAM + compliant CBD**" 그림 = **우리 MPM의 RIGID-AM scaffold +
   soft-plastic SE** 그림과 정확히 일치. 우리가 AM_S(single-crystal)를 **변형 안 하는 rigid scaffold**로
   둔 것이 이 논문으로 **실험 정당화**된다(단결정은 거의 안 깨지고 안 변형 → 모든 변형이 주변
   CBD/SE로 감).
2. ❗ **한계(정직히):** 그들의 spring-back은 **점탄성 = 시간의존(주)·온도의존**이다. 우리 MPM은
   **rate-independent von Mises J2**(시간 없음)이고 `--protocol hold`의 "relax"는 ~40 substep의 **순간
   기계적 settling**일 뿐이다 → **우리 MPM은 구조적으로 시간의존 spring-back을 재현할 수 없다**. 이것이
   CLAUDE.md가 "springback validation pending"으로 남겨둔 LIMIT의 **구체적 정체**다. **명백한 모델 한계**
   (하자라기보단 미구현 물리)이며, 아래 §7에서 심각도·해결책(Maxwell/Kelvin 점탄성 요소)을 구체화.

---

## 1. 배경 / 동기 (Introduction, p.4–5)

- LIB 전기화학성능은 전극화학뿐 아니라 **제조공정으로 결정되는 미세구조**에 강하게 의존. 그중
  **calendering(압연)**이 밀도·미세구조를 기계압축으로 제어 → 전자/이온 수송경로 + 기계 무결성 +
  입자패킹밀도 + pore 망 + AM↔CBD 계면접촉을 좌우(참고문헌 8–14). → 합리적 설계·정밀제어 필요.
- ★ **그러나 전극은 목표밀도로 압연해도 spring-back(두께 회복)을 본질적으로 겪는다**(참고 15,16).
  두께회복 = 미세구조 이완 + **CBD가 활물질 표면에서 떨어지며 pore 망 재분포**의 결과. 특히
  **AM–CBD 접촉면적 감소 → 전자전도경로 열화 → 내부저항↑ → 성능 저하**(참고 17).
- 기존 spring-back 연구는 대부분 **압력 해제 직후의 즉각 회복**에 집중(참고 18,19). **Kollenda et al.
  [20]**가 처음으로 **보관 중에도 두께회복이 진행됨(=시간의존 spring-back)**을 보고. 단 그들은 보관 중
  두께증가가 **무시할 만하다**고 봤는데, 이는 그들이 쓴 CAM이 **다결정(polycrystalline) 2차입자**였기
  때문 — **다결정은 입계 균열로 압축에너지를 소산**(particle fracture)한다(참고 21,22).
- ★ **대조: 단결정(single-crystal, monolithic) CAM은 균열기반 에너지소산을 억제**(참고 23,24) →
  **시간의존 spring-back이 더 커질 수 있다**. 그러나 단결정 cathode의 시간의존 spring-back 거동과 그
  미세구조·전기화학 영향은 **거의 연구되지 않음**.
- **본 연구 가설(명시):** 복합양극 = **기계적으로 견고한 단결정 CAM + 상대적으로 무른(ductile) CBD**
  (도전탄소 + 고분자 바인더). 단결정의 균열저항을 고려하면 **calendering 압축응력의 상당 부분이 CBD에
  수용(accommodate)**될 것. CBD는 **polymer-rich·점탄성**이므로 **시간의존 변형 + 응력이완**을 겪고,
  이것이 **압연 후 두께회복을 지배**할 것(참고 25,26).
- **공정변수 선택:** PVDF 바인더의 **온도의존 점탄성 응답**(참고 27–29)에 착안해 **calendering 온도**를
  제어가능 공정변수로 선택. RT·HT 비교연구 + **2D 단면 SEM 기반 미세구조 정량 + 모델링/시뮬레이션**을
  결합해 온도의존 기계응답 ↔ 미세구조진화 ↔ 전기화학성능을 상관(Fig 1).

**약어 정리:** CAM = cathode active material(단결정 NCMA). CBD = carbon binder domain(Super P + PVDF).
RT = room-temperature(25 °C). HT = high-temperature(80 °C). RC/HC = RT/HT-calendered.
P/S = pristine(압연 후 24 h 내) / stored(3주 보관 후). DC-IR = DC internal resistance. HPPC = hybrid
pulse power characterization. DMA = dynamic mechanical analysis. h_max = 최대 압입깊이.

---

## 2. 소재 & 제작 (Experimental Section, p.16–18)

### 2.1 CBD 점탄성 특성용 필름
- **CBD 필름:** Super P : PVDF(Solef 6020) = **1:1 wt%**, 슬러리 캐스팅 후 **100 °C 건조** → CBD 필름.
  (전극 조성 96:2:2의 도전재:바인더 = 2:2 = **1:1**과 일치 → 전극 내 CBD를 모사한 모델필름.)

### 2.2 양극 / 음극 / 셀
- **양극:** NCMA(86.5:5.4:7.5:0.7, single-crystal, POSCO Future M) : Super P(Imerys) : PVDF(Solef 6020) =
  **96:2:2 wt%**, NMP 슬러리, doctor-blade, **Al foil 15 µm**. **areal loading 20.325 mg/cm²**(= areal
  capacity **4 mAh/cm²**, 205 mAh/g 기준). 120 °C 1 h 건조 → **gap-controlled roll press(CLP-2025, CIS)**로
  **RT(25 °C) 또는 HT(80 °C)** 압연 → 목표밀도 **3.5 g/cm³**.
- **음극(full-cell용):** 인조흑연(94 wt%, SCMG-AR Showa Denko) + 도전재(1.5 wt%) + 수계 binder(CMC+SBR,
  4.5 wt%), Cu foil 10 µm, **areal loading 13.5 mg/cm²**, 60 °C 2 h 건조 → roll press **1.6 g/cm³**.
- **Half-cell:** CR2032, Li metal 200 µm 상대전극, PE separator(11–150; 11 µm), 전해질 **1.15 M LiPF₆
  EC/EMC 3:7 (v/v)** 200 µL. 양극 Ø12 mm, separator Ø18, Li Ø16.2. 진공건조 60 °C 12 h.
- **Full-cell:** 양극 Ø12 / 음극 Ø14, **N/P ratio ~1.15**, CR2032, Ar 글러브박스, 동일 separator·전해질.

### 2.3 전기화학 프로토콜
- 12 h 휴지(전해질 침투) → **pre-cycle 3.0–4.3 V**: formation 0.1C CC charge/discharge → 안정화 3사이클
  0.2C(CC/CV charge, CC discharge).
- **HPPC:** 10 s 전류펄스 = **방전 5C / 충전 3.75C / 충전 1.25C**, 40 s 휴지. **SoC 100→0% 10% 간격**. →
  DC-IR 산출.
- **EIS:** VMP-300(BioLogic), 진폭 10 mV, **5 MHz–50 mHz**.
- **Rate capability(full-cell):** 방전 0.2→10C(0.2/0.5/1/2/3/5/7/10C, back to 0.2C), 충전 0.2C 고정, 3.0–4.3 V.
- **Cycling(full-cell):** **500 사이클 @1C**(CC/CV charge, CC discharge), 3.0–4.3 V. 전 측정 25 °C 챔버.

### 2.4 미세구조·기계·시뮬 측정
- **Nanoindentation(CBD 필름):** UNHT3(Anton Paar), **구형 다이아 압자(SD-C13)**, RT(25)·HT(80, 30 min
  열평형). 선형하중, 취득 20 Hz, **최대하중 5 mN**, 하중/제하 15 mN/min, 최대하중 **유지 2 s**. → 하중-변위
  곡선에서 **h_max** + **dissipation energy ratio**(loading–unloading 히스테리시스 면적/입력에너지) 추출.
- **DMA:** DMA Q800(TA Instruments), **인장모드 1 Hz, strain 0.01–1%**, RT(25)·HT(80) 열평형. → **E′(저장
  탄성률), E″(손실), tan δ = E″/E′** 추출.
- **Electronic resistance:** RM2610(HIOKI), **50 mA, 전압 compliance 5 V**, 46-point probe(SI Fig S5). 양극
  pristine·stored bulk 전자저항.
- **2D FE-SEM 재구성:** ArBlade 5000(Hitachi) ion milling → FE-SEM(JSM-7610F-Plus, JEOL) 단면. **수동
  labeling**으로 CAM/CBD/pore 3상 분할(SI Fig S12).
- **정량분석:** GeoDict 2025 **MatDict**(계면접촉면적), **PoreDict**(pore size 분포), **ConductoDict**(2D 단면
  → 두께방향 정상상태 Ohmic 전도 → 유효전자전도도). 경계조건 ΔV=1 V(inlet 1 V/outlet 0), FVM.
  σ_eff = J·L/ΔV (식; J=면평균 전류밀도, L=두께방향 도메인길이). **입력파라미터(Table S2):**
  CAM 전자전도도 **0.7 S/m**, CBD **500 S/m**.

---

## 3. 핵심 메커니즘 — 왜 단결정에서 CBD 점탄성이 spring-back을 지배하는가

**(1) 단결정 CAM = 견고(rigid, monolithic).** 다결정 2차입자는 입계(grain boundary)를 따라 균열이
생겨 **압축에너지를 입자파괴로 소산**(Kollenda [20]에서 두께회복 무시할 만했던 이유). **단결정은 입계가
없어 균열기반 소산이 거의 없다**(참고 23,24) → 압축에너지가 입자 밖으로 빠질 길이 없다.

**(2) 그래서 압축응력이 CBD로 간다.** 견고한 단결정 사이의 **무른 CBD가 calendering 응력의 상당부분을
수용**(저자 가설·확인). CBD는 polymer-rich → **점탄성체**.

**(3) CBD 점탄성이 "저장 vs 소산"을 가른다 — 온도가 스위치.**
- **RT(25 °C):** 고분자 사슬 이동도 낮음 → CBD가 **탄성적(elastic, low-compressibility)** → calendering
  응력을 **탄성에너지로 저장(stored)** → 보관 중 천천히 풀림 → **두께회복(spring-back)**.
- **HT(80 °C):** 사슬 이동도↑ → CBD가 **점성/유동적(viscous, fluid-like, high-compressibility, compliant)**
  → calendering 중 응력을 **소산(relaxed/dissipated)** → 탄성 복원력↓ → **spring-back 억제**.

**(4) 결과 = 미세구조·전기화학 보존.** HT의 compliant CBD는 (i) 더 낮은 압축력으로 목표밀도 도달(잔류응력↓
→ spring-back 구동력↓), (ii) **AM–CBD 접촉면적↑**(더 잘 흘러 감싸므로, ~25%↑), (iii) **보관 후 pore 망이
더 균질**(큰 pore 생성 억제). → 전자전도망 보존 → 저항증가 완화 → 장기 성능 보존.

⇒ 우리 식으로: **"견고한 단결정은 변형/파괴로 에너지를 못 빼므로 모든 압축수용이 무른 점탄성 CBD로
몰리고, 그 CBD의 시간·온도 의존 응력이완이 보관 중 두께·미세구조·전자망을 결정한다."** 이건
압축역학(우리 MPM 영역) + 전자전도망(우리 DEM 영역)의 교차점이며, **단결정=rigid AM**이라는 우리 모델
가정의 실험 실증인 동시에 **시간의존(점탄성)**이라는 우리가 안 가진 축을 드러낸다.

---

## 4. 섹션별 결과 — 모든 수치

### 4.1 전극밀도 효과 (§2.1, Fig 2 + Fig S1–S3, p.5–7)

먼저 "적절한 치밀화는 이롭다"를 확립(spring-back 연구의 출발점인 목표밀도 3.5 g/cm³를 정당화).

**밀도 sweep 3.1 / 3.3 / 3.5 g/cm³ (half-cell, NCMA):**
- ★ **3.5 g/cm³ = 유의미한 입자균열 없이 도달가능한 최대밀도**(Fig S1: 3.5 vs 3.7 g/cm³ SEM 비교 —
  **3.7에서 입자균열이 뚜렷**해짐). → 이후 spring-back 연구는 **3.5 g/cm³ 고정**.
- **EIS(SoC 50%, Fig 2b):** 고밀도(3.5)일수록 **총 임피던스 최소**.
- **DC-IR(HPPC, Fig 2c + Fig S2):** 전 SoC 범위에서 같은 추세 — **고밀도일수록 DC-IR↓**.
- **Rate capability(Fig 2d + Fig S3):** **3.5 g/cm³이 3.3·3.1보다 우수**(0.2–10C, 충전 0.2C 고정).
- 해석(Fig 2a): 치밀화 → **이온경로 단축 + inter-component 접착↑ + 연속 전자경로** → 저항↓·성능↑.
  (단 과도한 치밀화는 pore 망 열화·입자균열 위험 — 참고 30–32 → 그래서 3.5가 상한.)

### 4.2 단결정 cathode의 시간의존 spring-back (§2.2, Fig 3 + Table S1, p.7–8)

★ 본 논문의 핵심 발견 1: **단결정 양극은 보관 중 시간의존 spring-back을 보인다.**

**두께변화(RT-calendered, 2D 단면 SEM 측정, Fig 3a,b):**
| 상태 | 두께 (µm) |
|---|---|
| Pristine(압연 24 h 내) | **58** |
| 1주 보관 | ~59.x |
| 2주 보관 | ~60.x |
| 3주 보관 | **61.7** (≈ 62) |
- ★ **3주에 걸쳐 ~58 → ~62 µm, 즉 약 +4 µm 증가**(점진적 증가 = 시간의존). → Li⁺ 수송경로 길어질 수
  있음(이온동역학 영향).
- ★ **대조 — 다결정(polycrystalline) 양극(Fig S4):** 같은 밀도(3.5)·같은 3주 보관에서 **두께변화 거의
  없음**(Table S1: 66 µm 유지). 이유 = **입계 균열이 압축 중·후 저장응력을 소산**(단결정의 제한된
  응력이완과 대조).

**Table S1 정량(시간의존 두께, 각 type 다지점 측정):**
| Type | Pristine | 1주 | 2주 | 3주 |
|---|---|---|---|---|
| **단결정 (RC)** | 58 | 59 / 60 / 62 | 60 / 60 / 62 | 61 / 61 / 61 |
| **단결정 (HC)** | 58 | 58 / 59 / 59 | 58 / 58 / 59 | 58 / 58 / 59 |
| **다결정 (RC)** | 66 | 66 / 66 / 67 | 66 / 66 / 66 | 66 / 66 / 66 |
→ ★ **단결정 RC만 증가(+3~4 µm), 단결정 HC와 다결정 RC는 거의 변화 없음.** 단결정 HC가 변화 없는 것이
**HT가 spring-back을 억제**한다는 핵심증거(아래 §4.4). 다결정 RC가 변화 없는 것이 **균열소산**의 증거.

**전자저항(46-point probe, Fig 3c):** ★ **stored가 pristine보다 bulk 전자저항↑**:
- **pristine 0.50 → stored 0.56 Ω·cm**(약 +12%). → spring-back이 **전자전도망을 약화**(AM–CBD 접촉
  감소로 전자경로 단절). spring-back ↔ 전자저항↑ ↔ 성능열화의 연결고리.

### 4.3 CBD 점탄성의 온도의존성 (§2.3, Fig 4a–d + Fig S6,S7, p.8–9)

★ 핵심 발견 2: **CBD 점탄성은 온도의존이고, HT에서 더 compliant·소산적이다.** (메커니즘의 직접 측정.)

**Nanoindentation(CBD 필름, Fig 4a–c):**
- ★ **h_max(최대 압입깊이): RT ~1193 nm → HT ~1948 nm**(약 +63%). 동일 하중조건에서 더 깊이 들어감 =
  HT에서 **국소 변형성(compliance)↑**(CBD 망이 더 잘 눌림).
- ★ **dissipation energy ratio: RT 0.62 → HT 0.67**(절대 +0.05, **HT가 7.9% 더 큼**). 히스테리시스 면적↑
  = 제하 시 회복 안 되는 에너지↑ = **점성 소산↑ + 탄성저장↓** → spring-back 구동력↓.

**DMA(CBD 필름, 인장 1 Hz, Fig 4d + Fig S7):**
- ★ **저장탄성률 E′: HT가 RT 대비 −41.2% 감소**(strain 0.0001–0.01 곡선; Fig 4d 화살표). HT에서 CBD가
  **더 쉽게 변형**(nanoindentation과 일치).
- **tan δ(=E″/E′) vs 온도(Fig S7):** 온도↑ → tan δ↑(점성 비중↑). → HT에서 CBD가 점성지배 영역으로
  이동(PVDF 사슬 이동도 증가). (정량 절대값은 SI 그림 — 추세: 고온일수록 tan δ 큼.)

**Gap-controlled roll press 치밀화 효율(Fig 4e):** RT·HT에서 roll gap을 점진적으로 줄이며 밀도 추적:
- ★ **RT는 목표밀도(3.5 g/cm³) 도달에 roll gap을 60 µm까지 줄여야** 함(높은 압축 demand).
- ★ **HT는 더 큰 roll gap 70 µm에서도 목표밀도 도달**(치밀화 효율↑). → **HT CBD가 더 compliant →
  더 낮은 압축력으로 같은 밀도** → **잔류응력↓ → spring-back 구동력↓**.

### 4.4 온도의존 spring-back & 전기화학 (§2.4, Fig 5 + Fig S8–S11, p.9–11)

★ 핵심 발견 3: **HT calendering이 시간의존 spring-back을 억제하고 성능을 보존한다.**

**두께(RT vs HT, pristine vs 3주 stored, Fig 5a + Fig S8):**
| 코드 | 두께 (µm) |
|---|---|
| **RC-P** (RT pristine) | **58** |
| **RC-S** (RT stored 3주) | **~62** (+4 µm) |
| **HC-P** (HT pristine) | **58** |
| **HC-S** (HT stored 3주) | **~59** (+1 µm) |
- ★ **RT는 3주에 +~4 µm, HT는 +~1 µm만**. Fig S8 시간추적: RT는 점진증가, **HT는 회복이 효과적으로 억제**.
  → **HT calendering이 시간의존 spring-back을 완화**(확정).

**내부저항(EIS, Fig 5b):**
- pristine 비교: ★ **HC-P가 RC-P보다 총저항 ~30% 낮음**(HT의 더 유리한 미세구조).
- 3주 보관 후: **RC-S는 임피던스 크게 증가, HC-S는 소폭 증가만**. → 순서 **HC-P < HC-S < RC-P < RC-S**.
  RC-S의 큰 증가 = **보관 중 spring-back → 미세구조 재배열 → 수송경로 단절** 때문.
- **DC-IR(HPPC, Fig 5c + Fig S9):** 전 SoC에서 같은 순서(HC-P < HC-S < RC-P < RC-S).

**Rate capability(full-cell, Fig 5d + Fig S10):**
- pristine: **HC-P가 RC-P보다 전 C-rate에서 높은 방전용량**.
- 3주 후: 둘 다 감소하나 **RT의 열화가 훨씬 큼**. ★ **RC-S는 RC-P 대비 전 C-rate 용량 크게 하락**;
  **HC-S는 HC-P에 근접 유지**(HT의 작은 저항증가와 일치).

**Cycling(full-cell 500 사이클 @1C, Fig 5e + Fig S11):**
| 코드 | 500사이클 후 용량 (mAh/g) | 용량유지율 |
|---|---|---|
| **HC-P** | **116.4** | **69.9%** |
| **HC-S** | **104.6** | **67.2%** |
| **RC-P** | **105.0** | **62.6%** |
| **RC-S** | **49.3** | **32.4%** ← 최악 |
- ★ **HC-S는 보관 후에도 유지율 거의 불변**(초기용량만 약간↓, retention 67.2% ≈ HC-P 69.9%).
- ★ **RC-S가 가장 심한 열화(49.3 mAh/g, 32.4%)** — 보관 중 spring-back이 미세구조를 망가뜨림.
- RC-P(62.6%)는 500사이클 용량이 HC-S와 비슷하나 유지율이 낮음(RT 압연 미세구조가 덜 안정).
- ⇒ **HT calendering이 초기 성능을 높이고 보관 후에도 spring-back 억제로 그것을 유지**.

### 4.5 미세구조 분석 (§2.5, Fig 6 + Fig S12–S17, p.11–13) — ★ 우리가 이식할 정량 방법

보관 후 성능차의 **미세구조 기원**을 RC-S vs HC-S로 규명(2D SEM 재구성 기반).

**단면 SEM(Fig 6a,b):** Fig 5a 두께추세와 일치 — **RC-S는 보관 후 두께 크게 증가, HC-S는 소폭**.

**2D 재구성 구조모델(수동 labeling → CAM/CBD/pore 3상, Fig 6c,d + Fig S12):**
- ★ **CAM–CBD 계면접촉면적(GeoDict MatDict, Fig 6e + Fig S13): HC-S가 RC-S보다 ~25% 높음**
  (RC-S 2.5 → HC-S 3.x ×10³ µm 단위, Fig 6e 막대). = **HT의 더 compliant한 CBD가 추가 CAM–CBD 접촉을
  형성**(더 잘 흘러 감싸므로). → 전자공급 계면 보존.
- **복합전극–집전체 계면접촉(Fig S15):** RC-S vs HC-S에서 **foil 근처 계면접촉 차이 뚜렷** — **HC-S가
  집전체 근처 접촉 우수**. → CC→복합전극 전류주입 더 효율. (CBD–CC specific surface area, Fig S15c.)

**전자전도 시뮬(GeoDict ConductoDict, 2D 단면 → 두께방향, Fig 6g–i + Fig S16,S17):**
- **전류밀도 맵(Fig 6g,h + Fig S16):** ★ **HC-S가 더 분산된 전류밀도장(reduced current localization)**;
  RC-S는 전류가 국소화(localized, 핫스팟). (Fig S17 streamline = 전류흐름선 시각화.)
- ★ **유효전자전도도(전류밀도맵에서 추출, Fig 6i): HC-S가 RC-S보다 ~50% 높음**(RC-S 0.19 → HC-S 0.32
  S/cm 단위, Fig 6i 막대). → spring-back 억제가 **전자전도망을 정량적으로 보존**.

**Pore size 분포(GeoDict PoreDict, Fig 6f + Fig S14):**
- ★ **RC-S는 ~2 µm보다 큰 pore 존재 + 넓은 분포**(구조 이질성↑). **HC-S는 ~2 µm 초과 pore 거의 없고
  좁은 분포**(균질). → RT의 spring-back이 **큰 pore 생성 + 이질성↑ → 비균일 이온/전자 수송 → 성능열화**.
- ⇒ **HT-calendered가 더 낮은 저항·더 나은 성능을 보관 후에도 보존하는 미세구조적 이유**: AM–CBD 접촉↑ +
  pore 망 균질 + 전자전도도↑.

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.5):** 개념도 — RT(elastic CBD, low-compressibility → 응력저장 → 작은 AM–CBD 접촉 →
  spring-back) vs HT(compliant CBD, high-compressibility → 응력이완 → 큰 AM–CBD 접촉 → spring-back 억제).
  단결정 활물질 회색구 + CBD 노란상. → ★ **메커니즘 1장 요약**(우리 rigid-AM + soft-CBD 그림과 대조).
- **Fig 2 (p.6):** 밀도효과 — (a) 치밀화 모식(이온경로 단축·접착↑·연속 전자경로), (b) EIS Nyquist
  (3.1/3.3/3.5), (c) DC-IR vs SoC, (d) rate capability(0.2–10C). → **목표밀도 3.5 정당화**(우리 압축밀도 축).
- **Fig 3 (p.8):** ★ spring-back 핵심 — (a) **단면 SEM pristine vs 3주 stored**(두께증가 가시), (b)
  **두께 vs 보관시간**(58→61.7 µm), (c) **bulk 전자저항 막대**(pristine 0.50 vs stored 0.56 Ω·cm). →
  **시간의존 spring-back + 전자저항↑ 증거**(우리 MPM springback 한계의 표적 데이터).
- **Fig 4 (p.9):** ★ CBD 점탄성 — (a) **nanoindentation 하중-변위(RT·HT, dissipation/storage 면적)**, (b)
  **h_max 막대(1193 vs 1948 nm)**, (c) **dissipation energy ratio(0.62 vs 0.67)**, (d) **DMA E′-strain
  (−41.2%)**, (e) **roll gap vs 밀도/두께(RT는 gap 60, HT는 70 µm에서 목표 도달)**. → **점탄성 정량
  (우리 CBD 기계물성 입력 후보 + 우리가 안 가진 온도축)**.
- **Fig 5 (p.11):** 온도효과 — (a) **4코드 두께 막대(RC-P 58/RC-S 62/HC-P 58/HC-S 59)**, (b) EIS Nyquist
  4코드, (c) DC-IR vs SoC, (d) rate capability 4코드, (e) **500사이클 cycling(retention 69.9/67.2/62.6/
  32.4%)**. → **HT가 spring-back 억제로 성능보존**(설계결론).
- **Fig 6 (p.12):** ★ 미세구조 정량 — (a,b) **RC-S/HC-S 단면 SEM**, (c,d) **재구성 2D 구조모델(CAM/CBD/
  CC 분할)**, (e) **CAM–CBD 계면접촉면적(+25%)**, (f) **pore size 분포(RC-S 큰 pore·이질 vs HC-S 균질)**,
  (g,h) **2D 전류밀도 맵(HC-S 분산 vs RC-S 국소)**, (i) **유효전자전도도(0.19 vs 0.32, +50%)**. → ★
  **2D SEM 재구성 → GeoDict 정량(접촉·pore·전도) 전체 워크플로**(우리 voxel/mpm3d에 이식 대상).

### SI Figures (S1–S17) + Tables
- **Fig S1:** 3.5 vs 3.7 g/cm³ SEM — **3.7에서 입자균열 뚜렷**(3.5가 균열없는 상한밀도 근거).
- **Fig S2:** HPPC 프로토콜[1] + 3.1/3.3/3.5 밀도 전류·전압 프로파일.
- **Fig S3:** 3.1/3.3/3.5 밀도 rate capability 전압곡선.
- **Fig S4:** ★ **다결정 양극(3.5 g/cm³)** — (a) SEM, (b) 3주 두께변화(**66 µm 유지 = spring-back 무**).
  단결정과 대조(균열소산).
- **Fig S5:** **전자저항 측정시스템 + 46-point probe 모식**[2](RM2610).
- **Fig S6:** **CBD 필름(점탄성 시료) + nanoindentation 시스템 + 측정모식**[3].
- **Fig S7:** ★ **온도의존 tan δ(DMA)**[4,5] — 온도↑ → tan δ↑(PVDF 점성지배 이동).
- **Fig S8:** ★ **RT vs HT 3주 두께추적** — (a) RT 점진증가, (b) **HT 회복 억제**.
- **Fig S9:** RC-P/RC-S/HC-P/HC-S HPPC 전류·전압 프로파일.
- **Fig S10:** 4코드 full-cell rate capability 전압곡선.
- **Fig S11:** 4코드 full-cell 500사이클 cycling 전압곡선.
- **Fig S12:** ★ **수동 labeling으로 cathode 구조모델 재구성 과정**[6,7](2D SEM → CAM/CBD/pore 3상).
- **Fig S13:** ★ **CAM–CBD 접촉영역(RC-S vs HC-S 재구성 2D)**[8](Fig 6e 정량 원본).
- **Fig S14:** **pore 상(RC-S vs HC-S)**[9,10](Fig 6f 정량 원본).
- **Fig S15:** **집전체 영역(SEM·재구성) + CBD–CC specific surface area**[8](Fig S15c).
- **Fig S16:** **전자 전류밀도 분포(RC-S vs HC-S 2D 맵)**[11](Fig 6g,h 원본 분포).
- **Fig S17:** **전류밀도 streamline 시각화(RC-S vs HC-S)**.
- **Table S1:** ★ **시간의존 두께(단결정 RC·HC + 다결정 RC, pristine→3주)** — 위 §4.2 표.
- **Table S2:** **전자전도 시뮬 입력파라미터**[12,13] — Δφ(inlet 1 V/outlet 0 V), **CAM σ_e = 0.7 S/m**,
  **CBD σ_e = 500 S/m**(CBD가 CAM보다 ~700× 전도성 → 전자망은 CBD가 지배).

---

## 6. 기술 미니용어집 (우리 맥락)

- **Spring-back(되튐):** calendering 압력해제 후 전극두께가 회복되는 현상. **즉각 spring-back**(압력해제
  직후) vs ★ **시간의존 spring-back**(보관 중 수 주에 걸쳐 진행 — 이 논문 주제). 우리 MPM `--protocol
  hold`의 "relax"는 ~40 substep **순간 settling**일 뿐 → 시간의존 회복 미구현.
- **CBD (carbon binder domain):** 도전탄소(Super P) + 고분자 바인더(PVDF)의 복합상. **polymer-rich →
  점탄성**. 우리 `additives.py`는 CBD 구성상(PTFE/SuperP/VGCF)을 **기하/부피**로만 모델 — **점탄성 기계
  거동 없음**.
- **Viscoelasticity(점탄성):** 응력에 **탄성(즉시·가역) + 점성(시간지연·소산)** 응답이 공존. 측정:
  **DMA(E′ 저장·E″ 손실·tan δ=E″/E′)** + **nanoindentation(h_max·dissipation ratio)**. **tan δ↑ =
  점성지배 = 소산↑**. 우리 J2 소성은 **rate-independent**(시간·점성 없음).
- **단결정 vs 다결정 CAM:** **단결정(single-crystal, monolithic)** = 입계 없는 단일결정 → **균열저항 큼 →
  에너지소산 못함 → spring-back↑**(= 우리 **AM_S**). **다결정(polycrystalline)** = 입계 있는 2차입자 →
  **입계균열로 소산 → spring-back 무**(= 우리 **AM_P**). 우리 DEM/MPM은 둘을 **크기+σ_AM만** 다른 강체구로
  취급(역학차이 없음).
- **DMA tan δ:** 손실계수. 온도↑/주파수↓ → 고분자 점성↑ → tan δ↑. spring-back ∝ 탄성저장 ∝ 1/(점성소산).
- **h_max / dissipation energy ratio:** nanoindentation 최대깊이(compliance 지표) / 히스테리시스 소산비율
  (점성소산 지표). HT에서 둘 다↑ = compliant·소산적.
- **HPPC / DC-IR:** hybrid pulse power로 SoC별 DC 내부저항 측정. 우리 transport와 대응(저항 = 1/σ).
- **GeoDict(MatDict/PoreDict/ConductoDict):** 상용 미세구조 정량/전도 솔버. 우리 `voxel_conductivity`/
  `viz_mpm_continuum`와 **같은 역할**(재구성 미세구조 → 접촉면적·pore·유효전도도). #286(Yoo)도 GeoDict 사용.
- **Roll gap:** gap-controlled roll press의 롤 간격. 작을수록 강압축. HT는 큰 gap(70 µm)에서도 목표밀도 →
  치밀화 효율↑. 우리 압축은 압력/변위제어 → roll gap은 우리에게 없는 **공정 dial**.

---

## ★ 7. 비교 vs 우리 DEM+MPM (frame [1]–[5])

⚠ **대전제(맨 먼저):** 이 논문은 **단결정 NCMA 양극 + 액체전해질 일반 LIB**다 — 우리 **LPSCl sulfide
ASSB**가 **아니다**. #286(Yoo, 흑연음극)과 마찬가지로 **절대 전기화학 수치(용량·DC-IR·rate·retention)는
전이 불가**다. **그러나 #286과 결정적으로 다른 점:** #286은 **액체 pore 수송**(우리와 무관)이 주제였지만,
**이 논문은 입자/CBD 역학**(단결정 견고성, 균열, 압축, spring-back, CBD 점탄성)이 주제다 — 그리고 **그
역학은 우리 MPM/DEM 압축역학과 직접 관련**(우리 AM_S = single-crystal). ⇒ **역학 인사이트는 (주의해서)
전이되고, 전기화학 절대값은 전이 안 된다.** (수치 σ 앵커는 Bazzoun#, porosity 앵커는 Varkey/Minnmann.)

### (a) 견고한 단결정 AM = 우리 RIGID AM ✓ — frame[1]/[2] 검증
- **그들:** **단결정 CAM = mechanically rigid, monolithic** → 균열·변형으로 에너지를 못 빼므로 **모든
  압축수용이 주변 CBD로 몰린다**(논문 가설이자 결과). 다결정만 입계균열로 소산.
- **우리:** **MPM은 AM을 변형 안 하는 RIGID scaffold**로 둔다(CLAUDE.md: "AM rigid + SE plastic";
  `mpm3d_compaction.py`의 `--am-scaffold`는 DEM AM 위치를 **고정 grid obstacle**로 박음, AM material point
  없음). DEM도 AM은 **eternal rigid sphere**. **소성변형은 soft SE(또는 CBD)만** 한다.
- ✅ **frame[1]/[2] 검증:** 이 논문은 **"단결정은 거의 안 변형/안 깨지고, 무른 상(CBD/SE)이 압축을
  수용한다"**를 실험으로 직접 보인다 = **우리 rigid-AM + soft-plastic-SE 분담의 실험 정당화**. 우리가
  AM_S(single-crystal)를 변형 안 하는 scaffold로 둔 게 **물리적으로 옳다**(단결정은 실제로 그렇게
  거동). → Stage-2 audit #7의 "단결정 견고성" 측면을 **검증 쪽으로** 굳힘.
- ⚠ **단, 우리 SE ↔ 그들 CBD는 같은 "무른 수용상"이지만 물성이 다름:** 우리 무른 상은 **LPSCl SE**(이온
  전도 + 소성), 그들 무른 상은 **PVDF+carbon CBD**(전자전도 + 점탄성). 역할(압축수용)은 같으나 **소재가
  다르므로 σ_y·E·점탄성 수치는 전이 안 함**.

### (b) 다결정 균열 에너지소산 = 우리 GAP (DEM Auerbach vs MPM)
- **그들:** **다결정 2차입자는 입계 균열로 압축에너지 소산** → spring-back 무(Fig S4: 66 µm 유지). 이게
  단결정 vs 다결정 spring-back 차이의 **유일한 메커니즘**.
- **우리 — 두 모델이 다르게 부족:**
  - **MPM:** AM이 rigid scaffold → **입자 균열 자체가 없다**. 다결정의 입계균열 소산을 **전혀 모델 못함**.
    우리 MPM에서 AM_P와 AM_S는 **둘 다 안 깨지는 동일 rigid scaffold** → spring-back 관점에서 **구별
    불가**. ❗ 이건 chemo-mechanical(향후) 한계.
  - **DEM:** **transport 쪽에는 균열이 있다** — fracture-aware Holm(f_intact), **Auerbach 균열**, force-chain.
    단 우리 DEM 균열은 **전자/이온 σ 감소(broken contact)**를 위한 것이지 **압축에너지 소산 → 두께/
    spring-back**을 위한 게 아니다. 그리고 **단결정 vs 다결정 균열경향 차이**(다결정이 더 잘 깸)는
    우리 DEM에 **없다**(균열은 force/Auerbach 기준이지 입자 내부구조 기준이 아님).
- 판정: **frame[5] 분업 부분확인** — 균열은 우리 **DEM(transport-side)**이 소유하나, **(i) 압축에너지
  소산 → spring-back 연결**과 **(ii) poly>single 균열경향 구분**은 **둘 다 없다**. 이 논문은 **균열이
  spring-back을 막는 메커니즘**을 보임 → 우리가 균열을 **역학(두께/응력) 쪽으로 확장**할 동기.

### (c) ★ 점탄성 시간의존 spring-back vs 우리 rate-independent J2 MPM — ❗ 정직한 한계 (핵심)
- **그들:** spring-back은 **점탄성 = (i) 시간의존(3주에 걸쳐 +4 µm 점진증가, Fig 3b/S8) + (ii) 온도의존
  (RT 탄성저장 vs HT 점성소산)**. 측정으로 직접 증명(DMA tan δ vs 온도, nanoindentation dissipation ratio).
- **우리:** MPM 구성식 = **rate-independent von Mises J2 소성**. **시간(t)이 구성식에 없다.** `--protocol
  hold`의 이완은 코드상 `wall_vel=0` 후 **`relax >= 40` substep**의 settling(스트레스 재분포)일 뿐
  (`mpm3d_compaction.py:636-642`) → **즉각·평형 settling이지 시간상수를 가진 점성이완이 아니다**. 온도축도
  **전혀 없다**(우리 σ_y·E는 상온 고정값).
- ❗ **결론(정직히): 우리 MPM은 구조적으로 시간의존 spring-back을 재현할 수 없다.** 이유:
  1. **점성 요소 부재** — J2는 탄소성(탄성+ rate-independent 소성)일 뿐. 시간의존 회복(creep/relaxation)을
     내는 **dashpot(점성)**이 구성식에 없다. spring-back = 탄성저장응력이 점성을 통해 **시간에 걸쳐**
     풀리는 것인데, 우리는 **점성이 없어 "시간에 걸쳐"가 불가능**.
  2. **온도의존 부재** — RT↔HT 스위치(이 논문의 설계변수)가 우리에게 **없다**. tan δ(T) 같은 온도-점탄성
     map이 없다.
  3. **CBD 역학 부재** — 그들은 spring-back을 **CBD가 지배**한다 보는데, 우리 CBD(`additives.py`)는
     **기하/부피상**일 뿐 기계물성(E·점탄성) 없음. spring-back을 낼 **주체 자체가 우리 모델에 없다**.
- **심각도 판정:** 이건 **"하자(bug)"가 아니라 "미구현 물리(structural scope limit)"**다. 우리 MPM은
  **압력하 평형 미세구조·morphology·porosity**(정적 압축의 종점)를 옳게 준다 — 거기엔 spring-back이
  필요 없다. spring-back은 **압력해제 후 시간진화**라는 **다른 물리축**이고, 우리는 그 축을 **애초에 안
  다룬다**(CLAUDE.md "springback validation pending"의 정체가 바로 이것). ⇒ **전이가능 결론(우리가 옳게
  하는 것)에는 영향 없음**; 단 **"우리 모델로 spring-back을 예측한다"고 주장하면 안 된다**(할 수 없음).
- ★ **구체적 해결책(이 논문이 알려주는 길):** spring-back을 다루려면 **점탄성 요소를 추가**해야 함:
  - **Maxwell 요소(스프링+직렬 dashpot):** 응력이완 `σ(t)=σ₀·exp(−t/τ_relax)`, τ_relax = η/E. HT는
    η↓(점성↓·이동도↑) → τ_relax↓ → 빠른 이완 → 압연 중 이미 소산 → spring-back↓. RT는 η↑ → τ_relax 큼 →
    보관 중(주 단위) 천천히 이완 → spring-back. **이 논문의 RT/HT 거동을 정확히 재현하는 최소모델**.
  - **Kelvin-Voigt 요소(스프링∥dashpot):** 변형지연(creep) `ε(t)=σ/E·(1−exp(−t/τ))`. 두께회복의
    **점진성**(Fig 3b 곡선)을 모델.
  - **표준선형고체(SLS, Maxwell+병렬스프링):** 즉각 + 시간의존 응답 동시 → spring-back의 즉각+시간의존
    2성분을 모두. **권장.**
  - **온도 입력:** η(T) 또는 E(T)를 **DMA tan δ(T)**(Fig S7)·E′(−41.2%, Fig 4d)로 캘리브 → 우리 σ_y·E를
    온도함수로. (단 LPSCl SE는 PVDF가 아니므로 **그들 수치 직접차용 금지** — 점탄성 **프레임워크**만 이식,
    LPSCl/SE-CBD 자체 점탄성 측정 필요.)
  - ⇒ 이건 **MPM 구성식 확장 프로젝트**(rate-independent J2 → viscoelastic-plastic). 작지 않은 작업이나
    **개념적으로 명확**하고, 이 논문이 **검증 데이터(두께 vs 시간, tan δ vs T)**를 제공.

### (d) CBD 점탄성 vs 우리 기하 CBD (`additives.py`)
- **그들:** **CBD 점탄성이 THE 설계 파라미터**(spring-back을 직접 지배). DMA E′·tan δ·nanoindentation으로
  정량.
- **우리:** `additives.py`는 CBD를 **PTFE/SuperP/VGCF 상**으로 **기하/부피/전자블로킹**만 모델 — **기계
  물성(E·σ_y·점탄성) 자체가 없다**. CBD는 우리에게 **σ 네트워크의 장애물/브리지**일 뿐 **응력을 저장·
  소산하는 역학체가 아니다**.
- ❗ **갭:** spring-back을 다루려면 **CBD에 점탄성 기계물성을 부여**해야 함(위 (c)의 SLS 요소). 현재 우리
  CBD는 **수동상(passive phase)**이고, 이 논문은 CBD가 **능동적 응력저장체(active stress reservoir)**임을
  보인다. → 우리 모델에서 **CBD를 역학적으로 활성화**(MPM에 CBD material point + 점탄성 구성식)하는 게
  spring-back으로 가는 길.
- ⚠ 단 **transport-only Stage-2에선 현 단순화가 정당** — 정적 압축 종점의 σ·coverage엔 CBD 점탄성이
  불필요(평형 미세구조만 필요). spring-back(시간진화)으로 갈 때만 필요.
- **frame[5] 분업:** 그들은 **CBD를 점탄성 역학체 + 전자전도체(σ_e=500 S/m)**로 다루지만 **explicit
  입자접촉 σ triad도, 소성 morphology 예측도, 압력→미세구조 예측도 없다**(post-mortem 재구성). 우리
  DEM+MPM이 그들에게 없는 **입자스케일 압축역학 예측 + σ triad**를 가짐.

### (e) Calendering 온도 = 우리에게 없는 설계축
- **그들:** **calendering 온도(RT 25 vs HT 80 °C)가 핵심 dial** — CBD 점탄성을 바꿔 치밀화 효율(roll gap
  60→70 µm)·잔류응력·spring-back·미세구조·성능을 모두 조절.
- **우리:** 압축을 **압력(300 MPa)/변위제어**로만 함. **온도축이 전혀 없다.** roll gap(공정 dial)도 없음
  (우리는 목표압력/밀도 직접 지정).
- ❗ **갭:** 온도-의존 점탄성을 넣지 않는 한 우리는 **"HT가 spring-back을 줄인다" 같은 공정온도 효과를
  예측 불가**. (c)의 점탄성 요소 + η(T)/E(T)를 넣으면 비로소 온도축이 생김.
- ⚠ 단 **우리 타깃(LPSCl ASSB)은 cold-press가 표준**(상온 고압) — HT calendering은 **액체 LIB 양극 공정**.
  ASSB에 온도축이 얼마나 중요한지는 별개 질문(고온소결 ASSB도 있으나 우리 cold-press 프레임과 다름). →
  **일반 LIB로 확장하거나 ASSB 고온공정을 다룰 때만** 우선순위. 현재 ASSB cold-press 프레임엔 **선택적**.

### 비교 요약표
| 축 | Hong 2026 (단결정 NCMA/액체) | 우리 (LPSCl ASSB) | 판정/이식 |
|---|---|---|---|
| 소재 | 단결정 NCMA + 액체전해질 | LPSCl SE + NMC811 | ⚠ 전기화학 절대값 전이불가, 역학은 전이(주의) |
| 단결정=rigid AM | 견고 → 압축이 CBD로 몰림 | MPM AM rigid scaffold + soft SE | ✅ **검증**(우리 rigid-AM 정당화) |
| 다결정 균열소산 | 입계균열 → spring-back 무 | DEM Auerbach/Holm(transport만), MPM 균열無 | ❗ 역학-spring-back 연결 + poly/single 균열차 GAP |
| 시간의존 spring-back | 점탄성(3주 +4µm, 온도의존) | rate-independent J2, hold=순간 settling | ❗ **재현 불가**(미구현 물리, 해결=SLS 점탄성) |
| CBD 역학 | 점탄성 = THE 설계변수(DMA/nanoindent) | additives.py CBD = 기하/부피만 | ❗ CBD 역학 활성화 필요(spring-back용) |
| Calendering 온도 | RT/HT = 핵심 dial | 압력/변위만, 온도 없음 | ❗ 온도축 GAP(η(T)/E(T) 필요; ASSB엔 선택적) |
| 미세구조 정량 | 2D SEM 재구성 → GeoDict(접촉·pore·σ_e) | voxel/mpm3d, DEM scaffold | ★ 워크플로 이식(접촉면적·pore·전류밀도맵) |
| 우리 고유 | (없음: post-mortem 재구성) | DEM 접촉 σ triad + MPM 소성예측 + 압력→구조 | 그들엔 입자스케일 예측 없음 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3–5가지

1) ✅ **"단결정 = 변형 안 하는 rigid AM"이 실험으로 검증됨 — 우리 MPM scaffold 가정이 옳다.**
   이 논문은 단결정 CAM이 균열·변형으로 에너지를 못 빼므로 **모든 압축수용이 무른 CBD/SE로 몰린다**를
   직접 보인다. 우리가 AM_S(single-crystal)를 **고정 grid scaffold**(`--am-scaffold`)로, soft SE만
   소성변형으로 둔 건 **물리적으로 정당**. → Stage-2 audit #7의 단결정 견고성 측면을 **✅ 검증**으로 굳히고,
   "우리 rigid-AM은 단순화가 아니라 단결정의 실제 거동"이라 서술 가능.

2) ❗ **우리 MPM은 시간의존 spring-back을 구조적으로 못 한다 — 명백한 scope 한계(하자 아닌 미구현).**
   spring-back = **점성을 통한 시간의존 응력이완** + **온도의존**인데, 우리 J2는 **rate-independent**(시간·
   점성·온도 전무)이고 hold-relax는 **순간 settling**이다. 우리는 **정적 압축 종점**(morphology/porosity)을
   옳게 주지만 **압력해제 후 시간진화는 안 다룬다**. ⇒ **"우리 모델로 spring-back 예측"은 주장 불가**.
   해결책은 명확: **MPM 구성식에 점탄성 요소(SLS: Maxwell+병렬스프링) 추가 + η(T)/E(T)를 DMA로 캘리브**.
   이 논문이 **검증 데이터(두께 vs 시간, tan δ vs T, dissipation ratio)**를 모두 제공 → 향후 viscoelastic-MPM
   프로젝트의 reference. (CLAUDE.md "springback validation pending"의 **정체가 바로 이것**임을 명시.)

3) ❗ **균열-spring-back 연결 + poly/single 균열차이가 우리에게 없다 — DEM 균열을 역학으로 확장할 동기.**
   우리 DEM은 균열을 **transport-side(broken contact → σ↓, Auerbach/Holm)**로만 쓴다. 이 논문은 균열이
   **압축에너지를 소산해 spring-back을 막는다**(다결정)는 **역학적 역할**을 보인다 — 우리에겐 (i) 균열→
   에너지소산→두께 연결, (ii) **다결정이 단결정보다 잘 깸**(입계)이라는 입자내부구조 의존 균열경향, **둘 다
   없다**. AM_P/AM_S가 우리 모델에선 **둘 다 안 깨지는 동일 rigid scaffold**라 spring-back 관점에서 구별
   불가. → chemo-mechanical(Phase 4 degradation)로 갈 때 **poly↔single 균열역학 구분**이 필요(이 논문 +
   #266 + #262가 같은 방향).

4) ★ **CBD를 "수동 기하상"에서 "능동 점탄성 역학체"로 — spring-back의 주체.**
   이 논문의 가장 큰 개념전환: **CBD가 spring-back을 지배하는 능동 응력저장/소산체**다. 우리 `additives.py`
   CBD는 **전자블로킹 기하상**일 뿐 응력을 저장·소산하지 않는다. spring-back/공정온도 효과를 다루려면
   **MPM에 CBD material point + 점탄성 구성식 + σ_e=500 S/m 전도성**을 부여해 CBD를 역학적으로 활성화해야
   한다. (transport-only Stage-2엔 불필요 — 정적 종점만 필요.)

5) ★ **2D SEM 재구성 → GeoDict 정량 워크플로 이식(접촉면적·pore size·전류밀도맵·유효 σ_e).**
   #286(Yoo)에 이어 **또 한 번** 이 그룹이 **2D SEM 수동labeling → GeoDict(MatDict 접촉면적/PoreDict pore/
   ConductoDict 유효전도도) → 전류밀도맵**을 쓴다. 우리 `voxel_conductivity`/`viz_mpm_continuum`이 같은
   역할이나 **CAM–CBD 계면접촉면적**(+25%)·**전류밀도 국소화/분산 맵**(Fig 6g–i)·**pore size 분포로 구조
   이질성**(>2 µm pore 유무) 정량은 우리 출력에 **추가 후보**. 특히 **전류밀도 localization 맵**은 우리
   StageE coverage/force-chain과 대응하는 **시각적 전자망 건강 지표**.

### 보너스 실행 항목
- **#285 인덱스 갱신**(아래 완료): web-abstract 수준 → 검증 수치(58→61.7 µm spring-back, RC-S 32.4% vs
  HC-S 67.2% retention, h_max 1193→1948 nm, E′ −41.2%, dissipation 0.62→0.67, AM–CBD 접촉 +25%,
  유효 σ_e +50%, CAM/CBD σ_e 0.7/500 S/m)로 교체.
- **Stage-2 audit #7 갱신 입력(사용자가 직접 fold):** 이 논문은 #7(poly/single 역학)을 **두 방향**으로
  움직임 — (i) **단결정=rigid 검증**(✅, 우리 scaffold 정당) + (ii) **다결정 균열소산·시간의존 spring-back은
  GAP**(❗, chemo-mechanical 한계). 그리고 **새 audit 항목 후보 = "시간의존 spring-back / 점탄성 CBD"**(우리
  MPM rate-independent → scope 밖, 해결=SLS 점탄성).
- ⚠ **혼동 금지:** #286(Yoo, 흑연/액체, **방법·설계 청사진**)과 이 논문(#285, 단결정 NCMA/액체, **역학
  검증 + spring-back 한계**)은 역할이 다르다. #285는 **우리 rigid-AM 가정을 검증**하고 동시에 **점탄성
  spring-back이라는 미구현 축을 정확히 지목**하는 소스다(수치 σ/porosity 앵커는 Bazzoun/Varkey/Minnmann).
