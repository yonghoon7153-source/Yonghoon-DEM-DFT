# Lee 2023 (Battery Energy 2, 20220061) — 디지털트윈 기반 SIC-SPE vs LPSCl 복합양극 구조·전기화학 분석 ★ DTBL 디지털트윈 계보의 가장 이른 논문(2023) + LPSCl 전극 구조지표

**인용:** Jongjun Lee, Seoungwoo Byun, **Hyobin Lee**, Youngjoon Roh, Dahee Jin, **Jaejin Lim**, Jihun Song,
Cyril Bubu Dzakpasu, Joonam Park, **Yong Min Lee\*** — "Digital-Twin-Driven Structural and Electrochemical
Analysis of Li⁺ Single-Ion Conducting Polymer Electrolyte for All-Solid-State Batteries," *Battery Energy*
**2** (2023) 20220061, DOI **10.1002/bte2.20220061**. Received 2022-11-02 · Revised 2022-11-18 · Accepted
2022-11-20 · Published 2023. © 2023 The Authors. **Open Access (CC BY)**, Xijing University & John Wiley &
Sons Australia. **Article type = RAPID COMMUNICATION** (7 pages). 소속: ¹DGIST 에너지공학과 · ²DGIST
에너지공학연구센터. 교신 **yongmin@dgist.ac.kr** (당시 DGIST; 이후 연세대 DTBL). 지원: 과기정통부
(NRF-2022M3J1A1054326) + 산업부(20012326).

**★ 계보 위치 — 이 그룹(이용민 DTBL) 디지털트윈의 "초기" 논문(2023):** 모델러 = **Hyobin Lee + Jaejin Lim**
(= 우리가 비교하는 #266/#271/#262/#281의 디지털트윈 모델러 본인들 — 이 2023 논문이 그들 GeoDict 워크플로의
**이른 시드**). 동료심사 ACS EL 2024 도구논문(#18 = Kim 2024, `lit_kim2024_digital_twin_acsenergyletters.md`)이
정의한 **top-down/reconstruction(GeoDict) 방법론의 이른 실제 적용 사례**이며, 같은 GeoDict 라인(#266/#271/#281/
#263/#275)의 **2023년판 원형**. ⚠ **#260–286 리스트엔 번호 없음**(2026 리스트 밖, 2023 논문) → 계보 항목으로
`literature_yonsei_dtbl_2026.md`에 추가.

**소재계 ⚠ 두 갈래:**
- ★★ **headline = SIC-SPE**(단일이온전도 고분자전해질, Li-치환 sulfonated tetrafluoroethylene copolymer =
  Li-Nafion, σ 0.2×10⁻³ S/cm) — **우리 LPSCl 황화물 focus가 아님**. SIC-SPE 절대값(과전압·용량·t₊)은 **이-셀-특이**.
- ★ **비교군 = Li₆PS₅Cl(LPSCl)**(황화물 SE, σ 2.2×10⁻³ S/cm) — **우리 정확한 SE**. 활물질 = **LiNbO₃-coated
  NMC711**(LiNi₀.₇Mn₀.₁₅Co₀.₁₅O₂, D50 8.0 µm) 양쪽 공통. ⇒ ★ **이 논문이 디지털트윈으로 산출한 "LPSCl 전극"의
  SE 부피분율 / tortuosity / AM-SE 접촉(coverage) / 유효 σ_ionic = 우리 DEM+MPM 출력과 정확히 같은 축, 같은
  소재계(이른) reference.**

**DB 동반:** 이 논문은 **단일압력(500 MPa 양극 압착)·digitized 아님(텍스트 명시 수치)**이라 새 CSV 행은 만들지
않음(아래 §7에서 "참고 reference"로만 기록). LPSCl σ_ionic 절대 앵커는 **Bazzoun/#271/Varkey/Minnmann/#266** 유지
(이 논문 σ는 **digital-twin 출력 = 입력 intrinsic σ + 구조의 곱**이라 실측 EIS 앵커와 위상이 다름 — §7·§10 주의).
머신판독 불가 자료(동영상 등) 없음. SI = 텍스트 추출본만(`scratchpad/SI_21.txt`) — 그림 이미지 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 (적당히) 중요한가

**"SE의 고유 이온전도도가 낮아도, 복합양극 구조(SE 부피분율↑·tortuosity↓·AM-SE 접촉↑)가 좋으면 셀 성능은
대등하다"** — SIC-SPE(고분자, σ가 LPSCl의 1/10)가 **저압(수십 MPa)에서 활물질과 밀착(intimate contact)**하여
LPSCl(고압 500 MPa 필요)과 **대등한 방전용량·율속**을 내는 이유를, **3D 디지털트윈(GeoDict)**으로 분해해 보인
Rapid Communication. SIC-SPE 전극이 LPSCl 전극보다 **SE 부피분율↑(32.1 vs 26.1 vol%)·tortuosity↓(1.08 vs 1.31)·
AM coverage↑(68.2 vs 38.8%)** → 더 낮은 과전압.

**★ 우리 hook(정직하게 — 중간 관련도):**
- ✅ **(가장 큰 가치) LPSCl 전극의 디지털트윈 구조지표가 우리 출력과 1:1 같은 축:** **SE-vol 26.1 vol% /
  tortuosity 1.31 / AM coverage 38.8% / 유효 σ_ionic 4.28×10⁻⁵ S/cm**. 이건 **우리 DEM(porosity/φ_SE·τ_Laplace/
  τ_Dijkstra·Stage-E coverage·Kirchhoff σ_ionic)이 내는 바로 그 네 지표**를, **같은 소재계(LPSCl+NMC711)**로,
  **2023년에(이 그룹의 이른 시점)** 산출한 reference다.
- ✅ **디지털트윈 = GeoDict top-down/reconstruct(출력단)** — `positioning_vs_geodict.md`의 "GeoDict는 구조를
  줘야 함(측정 조성·밀도·BET 입력) ↔ 우리는 공정→구조 예측(입력단)"을, **이 그룹의 가장 이른 GeoDict 사례**로
  재확인. #18(ACS EL 2024)·#271(2026)·#266(2026)의 **2023 원형**.
- ⚠ **headline 소재(SIC-SPE 고분자)는 우리 focus 아님** + **셀 절대값(과전압·용량 163/146.5/…/55.8 mAh/g)은
  이-셀-특이(비전이)** + **σ는 digital-twin 출력(입력 intrinsic σ의 구조-가중)이지 from-scratch 예측이 아님** →
  LPSCl **구조지표 4종**과 **positioning(GeoDict reconstruct)**만 가져온다.

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- EV용 LIB 안전성 요구 → **ASSB** 연구 활발. SE의 저인화성 = 화재·폭발 저항, 넓은 전기화학창 = 고전압 양극 가능.
- ASSB SE 연구는 주로 **무기 SE(황화물·산화물)**에 집중: 고유 σ 높음(10⁻²–10⁻⁴ S/cm @25°C), 전이수 t₊≈1,
  기계강성으로 Li 덴드라이트 억제. **그러나 문제**: ① 전극에서 AM/SE·SE/SE **접촉 형성에 고압·소결 필요**;
  소결 후에도 입자간 **공극(void) 불가피**; ② **고두께·계면/입계 저항**.
- **고분자 SE(SPE)** 재조명: ① AM과 **intimate contact** 형성 → 큰 AM-SE 계면; ② **고압 불요**(제조 단순·고에너지
  밀도); ③ 가공성·대면적·양산성. **그러나** SPE는 **σ 낮음(<10⁻⁴ S/cm @25°C)** + 다수가 **dual-ion(t₊<0.5)** →
  전체 σ의 절반 미만만 Li⁺ 기여 + 국소 이온분극·불균일 Li 증착·덴드라이트.
- **본 연구(명시):** **dual-ion의 낮은 t₊**를 해결하려 **sulfonated tetrafluoroethylene copolymer 기반 SIC-SPE**
  (σ 0.2×10⁻³ S/cm @25°C, t₊≈1) 제시. **3D 디지털트윈(GeoDict)**으로 SIC-SPE 전극이 LPSCl 전극보다 **AM-SE 계면↑
  + 잘 연결된 percolation 경로**를 가져 **낮은 과전압**을 냄을 입증. ★ **= "고분자라도 구조가 좋으면 무기 SE와 대등"
  이라는 구조-우선 명제.**

---

## 2. 소재 & 디지털트윈 방법 (Experimental, SI §1 + 본문 §2)

### 2.1 SIC-SPE 제조 (SI §1.1)
- 상용 **Nafion(Dupont)** → 물 500 mL + **LiOH·H₂O 21 g**, 60°C 3 h 처리(H⁺→Li⁺ 치환) → 세척·진공건조. =
  **Li-Nafion**(Li-C₇HF₁₃O₅S·C₂F₄). 자유막(free-standing) **30 µm**(목표 무기 SE 수준 박막), 비틀림·접힘 견딤(Fig S2).

### 2.2 NMC711 양극 제조 (SI §1.2)
- **SIC-SPE 양극(슬러리, NMP):** LiNbO₃-coated **NMC711 78.4 wt% + Super P 2 wt% + SIC-SPE 19.6 wt%** →
  Al foil(15 µm) 캐스팅·130°C 1 h 건조. **NMC711 로딩 16 mg/cm² (≈2.0 mAh/cm²)**, 롤프레스로 **전극밀도 2.9 g/cm³**.
- **LPSCl 양극(슬러리, xylene):** LiNbO₃-coated **NMC711 : LPSCl : Super P : NBR = 76.8 : 19.2 : 2 : 2 wt%**,
  Thinky 2000 rpm 30 min → Al 집전체 닥터블레이드·60°C 24 h 진공건조. **셀 조립:** LPSCl 분말 150 mg을 **50 MPa**
  사전펠릿화(PEEK 몰드 ⌀13 mm) → 양극(⌀13 mm) 올리고 **500 MPa 재압착** → 반대편 Li foil + **30 MPa** 토크 고정.
- ⚠ **= 무기 SE(LPSCl)는 500 MPa 고압 필요, 고분자(SIC-SPE)는 슬러리캐스팅 직접 밀착(수십 MPa)** — 이 논문의 핵심 대비.

### 2.3 ★ 디지털트윈 (3D 구조 형성) (SI §1.3) — GeoDict GrainGeo, reconstruct-from-measurement
**전부 GeoDict 2022(Math2Market)의 GrainGeo 모듈로 가상 생성.** 핵심 디테일:
- **밀도 입력:** NMC711 **4.44 g/cm³**, SIC-SPE **1.80 g/cm³**, Super P **1.98 g/cm³**, LPSCl **2.07 g/cm³**,
  NBR **1.00 g/cm³**.
- **조성(wt%):** SIC-SPE 전극 = NMC711 : SIC-SPE : Super P = **78.4 : 19.6 : 2.0**; LPSCl 전극 = NMC711 :
  LPSCl : NBR : Super P = **76.8 : 19.2 : 2 : 2**.
- ★ **전극 설계 입력(측정값 매칭):** **SIC-SPE 전극 = 2.94 g/cm³, 54 µm, 15.9 mg/cm²**; **LPSCl 전극 =
  2.81 g/cm³, 58 µm, 16.3 mg/cm²**. (= 실측 전극밀도·두께·로딩을 디지털트윈에 주입.)
- **입자 형상:** **균일 구형(uniform spherical)** — NMC(**D50 8.0 µm**), LPSCl(**D50 2.3 µm**); SIC-SPE·NBR은
  **고분자 상**으로 채움. ⚠ **구형·단일크기 = 우리 DEM 구-입자와 같은 단순화**(다결정/다분산 PSD 없음).
- **도메인:** **40 µm × 40 µm × 두께(thickness)**, **cubic voxel 0.2 µm**.

### 2.4 ★ 기하·전기화학 물성 계산 (SI §1.4–1.5)
- **MatDict 모듈:** SE의 **연결성(percolation path)** + **geodesic tortuosity** + **추정 표면적(estimated surface
  area)** → AM-SE **접촉면적**.
- ★ **ConductoDict 모듈:** **유효 이온전도도(σ_eff)** 계산 — 경계조건 **ΔV = 1**(상·하면 전위차 1 V) 인가, 구조
  전체 이온수송 풀이. ★★ **intrinsic σ는 입력**(SIC-SPE 0.2×10⁻³, LPSCl 2.×10⁻³ S/cm 주입), σ_eff가 출력.
- **BatteryDict + BESTmicro 솔버(BatteryDesigner):** 디지털트윈 solid-state 셀 구성 → **0.1C, 25°C** 전기화학
  시뮬(이온 flux·표면 과전압·lithiation 분포). 입력 파라미터 = **Table S2**(아래 §2.5).
- ★ **= GeoDict GrainGeo 재구성(측정 조성·밀도·두께 입력) → MatDict/ConductoDict로 구조지표·σ_eff 출력 →
  BESTmicro 1D-ish 전기화학.** = **top-down/reconstruct 디지털트윈**(#18 ACS EL taxonomy의 "bottom-up stochastic"
  요소도 일부 — 측정 파라미터→가상생성 — 있으나, **구조를 측정에서 주입하고 압력→구조 예측은 안 함** → positioning상
  reconstruct 쪽; #271/#266/#281과 같은 GeoDict 라인).

### 2.5 디지털트윈 전기화학 입력 (Table S2) — ★ intrinsic σ는 입력
| 파라미터 | SIC-SPE(Li-Nafion) | LPSCl |
|---|---|---|
| **intrinsic 이온전도도 (S/cm)** | **2.0×10⁻⁴** | **2.×10⁻³** (= 2.2×10⁻³) |
| intrinsic 전자전도도 NMC711 (S/cm) | 9.0×10⁻³ | 9.0×10⁻³ |
| intrinsic Li 확산계수 SE (m²/s) | 1.3×10⁻¹⁰ | 1.0×10⁻¹¹ |
| **Li 전이수 t₊** | **0.94** | **0.99** |
| Li 농도 (mol/m³) | 1700.0 | 7711.9 |

⚠ ★ **σ_eff(§4.2)는 이 intrinsic σ를 구조(SE-vol·τ)로 가중한 출력** → 우리 from-scratch Kirchhoff σ와 정보론적
위상 다름(§10).

---

## 3. 핵심 메커니즘 — 구조가 σ 결손을 보상 (Fig 1, Fig 3, Fig 4)

**(1) SIC-SPE = 저압 intimate contact → SE-vol↑·τ↓·coverage↑.** 고분자는 슬러리캐스팅에서 AM 표면을 **균일·광범위
밀착**(Fig 1 "Intimate contact" + 모식). 저밀도(SIC-SPE 1.80 g/cm³ ≪ LPSCl 2.07)라 **같은 wt%에서 SE 부피분율이
더 큼**(32.1 vs 26.1 vol%) + NBR 같은 **추가 절연상이 없음** → AM-SE 계면↑·이온경로 연속.

**(2) LPSCl = 고압 펠릿화에도 void·NBR 절연상 → τ↑·coverage↓.** 무기 SE는 입자간 void 불가피 + **NBR 바인더
(비전도)**가 부피 차지 → 더 **tortuous한 이온경로**(τ 1.31 > 1.08) + **AM coverage 38.8% ≪ 68.2%**.

**(3) ❗ 핵심 통찰 — σ_eff/intrinsic 비율이 역전:** intrinsic σ는 LPSCl(2.2×10⁻³)이 SIC-SPE(2.0×10⁻⁴)의 **11배**.
그러나 구조 손실 후 **σ_eff는 LPSCl 4.28×10⁻⁵ vs SIC-SPE 2.85×10⁻⁵** — 격차가 **1.5배로 좁혀짐**. 핵심:
**LPSCl 전극은 intrinsic σ의 1.9%만 유지**(void·NBR·고τ로 대부분 손실), **SIC-SPE 전극은 14.3% 유지**(좋은
percolation·저τ). ⇒ **"고분자의 우수한 구조가 낮은 intrinsic σ를 보상"** = 구조-우선 명제의 정량 증거.

**(4) 이온 flux·과전압 분포(Fig 4):** SIC-SPE 전극 = **저-flux가 잘-분산된 SE에 균일** → 집전체 주변부까지 대부분
AM이 lithiation; LPSCl 전극 = **국소 집중된 이온 flux**(전극/전해질 계면 근처 한정 AM만 반응) → 높은 Li 수송
과전압. ⇒ SIC-SPE의 **잘-연결된 percolation + 큰 AM-SE 계면 → 더 균일·낮은 과전압**.

---

## 4. 섹션별 결과 — 모든 수치 (Results & Discussion, §2, p.3–6)

### 4.1 SIC-SPE 자체 물성 (Fig 2, Table S1)
- **막:** SIC-SPE 자유막 **30 µm**(목표 무기 SE 수준), 유연(비틀림·접힘 OK, Fig S2).
- ★ **σ_ionic(Fig 2A, 아레니우스):** **0.2×10⁻³ S/cm @25°C, 6.1×10⁻³ S/cm @60°C**. → 보고된 다수 SPE보다 높고
  일부 무기 SE와 대등(Table S1: 70Li2S-30P2S5 3.2×10⁻³ / LGPS 1.2×10⁻² / **LPSCl 2.9×10⁻³** / LATP 3.0×10⁻³ /
  LLZO 3.0×10⁻⁴ … 본 SIC-SPE 2.0×10⁻⁴, t₊ 0.94).
- ★ **Li 전이수 t₊ = 0.94(Fig 2B, 크로노암페로메트리+EIS)** → 단일이온전도체(SIC) 확인; 무기 SE 수준.
- **Fig 2C:** σ_ionic·t₊ 막대 비교(PEO-LiTFSI / LLZO / LPSCl / SIC-SPE). SIC-SPE는 σ는 중간이나 **t₊≈1**로 무기 SE급.
- **전기화학 안정성:** **4.6 V까지 안정**(Fig S6, LSV) → 고전압 양극 호환. **난연성**: 화염노출 후 형상 유지(Fig S5).
- **Li 도금/스트리핑:** Li/SIC-SPE/Cu·Li/SIC-SPE/Li 안정(Fig S3, S4).

### 4.2 ★ 셀 전기화학 — SIC-SPE ≈ LPSCl (Fig 2D, 2E)
- ★ **율속별 방전용량(0.1/0.2/0.5/1.0/2.0C, 25°C, Fig 2E):** SIC-SPE = **163.0 / 146.5 / 125.5 / 95.4 / 55.8 mAh/g**.
  LPSCl 셀과 **대등**(Fig 2E 겹침). ⚠ **이-셀-특이 절대값(비전이).**
- **충방전 곡선(0.1C, Fig 2D):** SIC-SPE vs LPSCl 거의 겹침. → ★ **"intrinsic σ가 10배 낮은데도(0.2 vs 2.2×10⁻³)
  용량·율속이 LPSCl과 비슷"** = 구조 분석 동기.

### 4.3 ★★ 디지털트윈 구조지표 — SIC-SPE vs LPSCl (Fig 3) ★ 우리 출력과 1:1
★ 핵심 — **GeoDict 재구성으로 SE 부피분율·tortuosity·유효 σ_ionic·AM coverage 정량.**

**3D 디지털트윈 구조(Fig 3A SIC-SPE / 3B LPSCl):** AM(NMC711) + SE(SIC-SPE 파랑 / LPSCl 노랑) 재구성.

**★★ SE 부피분율(Fig 3A·3B 라벨):**
| 전극 | **SE 부피분율 (vol%)** |
|---|---|
| **SIC-SPE** | **32.1** |
| **LPSCl** | **26.1** |
→ SIC-SPE↑ 이유: **고분자 저밀도(1.80 g/cm³ ≪ LPSCl 2.07) + 추가 바인더(NBR) 부피 없음** → 같은 wt%에서 부피분율↑.

**★★ Tortuosity factor(SI Fig S8, 본문 §2):**
| 전극 | **tortuosity factor** |
|---|---|
| **SIC-SPE** | **1.08** |
| **LPSCl** | **1.31** |
→ SIC-SPE = **균일·연속 이온경로**(저τ); LPSCl = **void + 절연 NBR**로 **더 tortuous**(고τ).

**★★ 유효 이온전도도 σ_eff(Fig 3C 막대):**
| 전극 | intrinsic σ (S/cm) | **σ_eff (S/cm)** | **σ_eff/intrinsic** |
|---|---|---|---|
| **SIC-SPE** | 2.00×10⁻⁴ | **2.85×10⁻⁵** | **14.3%** |
| **LPSCl** | 2.20×10⁻³ | **4.28×10⁻⁵** | **1.9%** |
→ ★ **LPSCl σ_eff(4.28×10⁻⁵)가 SIC-SPE(2.85×10⁻⁵)보다 여전히 높음**(intrinsic 11배 우위가 남아). **그러나
LPSCl은 intrinsic의 1.9%만, SIC-SPE는 14.3% 유지** → **percolation/τ가 좋은 SIC-SPE가 구조손실을 압도적으로 덜 봄**.

**★★ AM coverage(AM-SE 접촉, Fig 3D SIC-SPE / 3E LPSCl, coverage ratio = 계면접촉면적/AM 총표면적):**
| 전극 | **AM coverage (%)** |
|---|---|
| **SIC-SPE** | **68.2** |
| **LPSCl** | **38.8** |
→ ★ SIC-SPE가 **AM 표면의 68.2%**를 SE로 덮음(저압 intimate contact); LPSCl은 **38.8%만**(void·고압에도 불완전).
**= AM-SE 계면이 큰 SIC-SPE가 더 많은 반응면적 → 낮은 과전압.**

### 4.4 ★ 디지털트윈 전기화학 — 이온 flux·과전압·lithiation (Fig 4)
★ 핵심 — **BESTmicro 전기화학 시뮬로 이온 flux·표면 과전압·lithiation 공간분포.**
- **이온 flux(Fig 4B SIC-SPE / 4F LPSCl, range 0–500 pmol·cm²·s⁻¹? [그림 컬러바 0–500]):** SIC-SPE = **저-flux가
  잘-분산된 SE에 균일**; LPSCl = **국소 집중**(높은 Li 수송 과전압 시사).
- **표면 과전압(Fig 4C SIC-SPE / 4G LPSCl, 0 to −10 mV):** AM 표면 lithiation 반응 분포. SIC-SPE = **집전체 주변부
  까지 대부분 AM이 과전압**(넓은 반응면적); LPSCl = **전극/전해질 계면 근처 한정 AM만**.
- **lithiation 상태(Fig 4D SIC-SPE / 4H LPSCl, 0–100%):** SIC-SPE = **더 넓은 AM 표면적·높은 lithiation**;
  LPSCl = **제한된 AM**. ⇒ SIC-SPE의 큰 AM-SE 계면 → 더 높은 lithiation·낮은 과전압.

### 4.5 종합·전망 (Conclusion, p.6)
- **결론:** SIC-SPE(σ 0.2×10⁻³, intrinsic이 LPSCl 2.2×10⁻³의 1/10)가 **대등한 방전용량·율속**을 냄. 디지털트윈이
  그 이유 = **SE 부피분율↑·tortuosity↓·AM-SE 접촉↑(단일이온 전도상)**임을 규명. ⇒ ★ **"좋은 구조를 만드는
  전해질(SIC-SPE)을 찾는 것이 σ 높은 전해질을 찾는 것만큼 중요"** + **디지털트윈이 복합양극 이해·설계에 필수**.
- **전망:** SIC-SPE 고유 σ를 더 높이되 고분자의 탄성·유연 유지; 부피분율·tortuosity·접촉면적을 디지털트윈으로
  설계·제어.

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.2):** SIC-SPE의 장점 모식 — 자유막·유연, AM과 intimate contact(좌상 SEM-like + SO₃⁻/Li⁺ 모식),
  양산성(롤투롤), **저압(Tens of MPa)·무 고압소결**(×표시 고압 프레스). → 고분자 SE의 저압 밀착 컨셉.
- **Fig 2 (p.3):** SIC-SPE 자체+셀 — (A) σ vs T(0.2×10⁻³@25/6.1×10⁻³@60°C). (B) t₊=0.94(CA+EIS). (C) σ·t₊
  막대(vs PEO-LiTFSI/LLZO/LPSCl). (D) 충방전(0.1C, SIC-SPE vs LPSCl 겹침). (E) ★ **율속(0.1–2C, 163/146.5/
  125.5/95.4/55.8 mAh/g, LPSCl과 대등)**. → 셀 대등성(동기).
- **Fig 3 (p.5):** ★★ 디지털트윈 핵심 — (A) SIC-SPE 3D(**SE-vol 32.1 vol%**). (B) LPSCl 3D(**26.1 vol%**).
  (C) ★ **intrinsic vs σ_eff 막대**(SIC-SPE 2.0×10⁻⁴→2.85×10⁻⁵ / LPSCl 2.20×10⁻³→4.28×10⁻⁵). (D) SIC-SPE
  **AM coverage 68.2%**. (E) LPSCl **AM coverage 38.8%**. → **우리 SE-vol/σ_ionic/coverage 출력과 1:1**.
- **Fig 4 (p.6):** ★ 디지털트윈 전기화학 — (A) SIC-SPE 셀구조 / (E) LPSCl. (B)(F) **이온 flux**(SIC-SPE 균일
  vs LPSCl 집중, 0–500). (C)(G) **표면 과전압**(0 to −10 mV). (D)(H) **lithiation**(0–100%). → SIC-SPE 균일·
  넓은 반응·저과전압.

### SI Figures/Tables (S1–S10, S1–S2)
- **Fig S1:** SIC-SPE 분자구조 + ATR-FTIR(Li⁺ 치환 전후). **Fig S2:** 자유막 이미지·두께·비틀림/접힘.
- **Fig S3:** Li 도금/스트리핑 전압곡선 + SEM. **Fig S4:** Li/SIC-SPE/Li 대칭셀 과전압.
- **Fig S5:** 난연성(화염 후 형상유지). **Fig S6:** 산화 LSV(4.6 V 안정).
- **Fig S7:** SIC-SPE solid-state 셀 제작공정 + 단면 SEM(전해질/전극 계면).
- ★ **Fig S8:** **percolation pathway**(디지털트윈, (a) SIC-SPE / (b) LPSCl) — **tortuosity 1.08 vs 1.31 출처**.
- **Fig S9:** 셀 상세구성(SIC-SPE / LPSCl). **Fig S10:** 실험 vs 시뮬 데이터 비교(SIC-SPE / LPSCl) — 검증.
- ★ **Table S1:** 보고된 SE들의 σ·t₊(70Li2S-30P2S5 / LGPS / **LPSCl 2.9×10⁻³** / LATP / LLZO / 각종 SPE /
  본 SIC-SPE 2.0×10⁻⁴, t₊ 0.94).
- ★★ **Table S2:** 디지털트윈 입력 파라미터(§2.5 표 — intrinsic σ_ion/σ_e/D_Li/t₊/c_Li, SIC-SPE vs LPSCl).

---

## 6. 기술 미니용어집 (우리 맥락)

- **SIC-SPE (single-ion conducting solid polymer electrolyte):** Li-치환 sulfonated tetrafluoroethylene
  copolymer(= Li-Nafion). σ 0.2×10⁻³ S/cm, **t₊=0.94**(단일이온). ⚠ **고분자 = 우리 LPSCl 황화물 focus 아님**.
- **t₊ (Li 전이수):** 전체 이온전류 중 Li⁺ 기여 비율. dual-ion SPE는 <0.5(절반 미만 Li⁺ 기여), SIC-SPE·무기 SE는
  ≈1. 우리 모델엔 t₊ 축 없음(우리 σ_ionic = Li⁺ 전도 가정).
- **SE 부피분율 (vol%):** 디지털트윈에서 SE가 차지하는 부피비(SIC-SPE 32.1 / LPSCl 26.1). ★ **우리 φ_SE(SE 부피
  분율)의 출력단 대응** — porosity·composition으로부터 우리도 산출.
- **Tortuosity factor (geodesic τ):** 이온경로의 우회도. MatDict geodesic tortuosity로 계산(SIC-SPE 1.08 /
  LPSCl 1.31). ★ **우리 τ_Laplace,eff·τ_Dijkstra(측지/유효 tortuosity)의 출력단 대응** — 단 정의·도메인 차이
  (그들 geodesic vs 우리 Laplace/Dijkstra) → 절대 1:1 아니고 **추세·자릿수 비교**.
- **AM coverage (%):** AM 표면 중 SE가 덮은 비율(= 계면접촉면적/AM 총표면적; SIC-SPE 68.2 / LPSCl 38.8). ★★
  **우리 Stage-E coverage(Tabor/Hertz, cov_AM)의 출력단 대응**(#271 LPSCl coverage 26–36%와 같은 축; LPSCl
  38.8%는 #271 Pwd 35%/PTFE 36%와 자릿수 일치).
- **σ_eff (effective ionic conductivity):** ConductoDict로 구조 전체에 ΔV=1 인가해 푼 **유효** σ. ★ **intrinsic σ는
  입력**, σ_eff가 출력(SIC-SPE 2.85×10⁻⁵ / LPSCl 4.28×10⁻⁵). ⚠ **우리 Kirchhoff σ_ionic은 from-scratch 출력
  (intrinsic σ_grain·구조 → σ), 위상 다름**(§10).
- **GeoDict GrainGeo / MatDict / ConductoDict / BatteryDict-BESTmicro:** GeoDict 2022 모듈군 — GrainGeo(가상
  구조 생성)·MatDict(percolation·τ·표면적)·ConductoDict(유효 σ, FV)·BESTmicro(전기화학 솔버). ★ **GeoDict 기반
  top-down/reconstruct 디지털트윈**(= #271/#266/#281과 같은 도구 라인; 우리 voxel FV = ConductoDict 무료 대응 +
  Kirchhoff/Holm 접촉망 추가).
- **digital twin (top-down/reconstruct):** 측정 조성·밀도·두께·BET를 가상구조에 주입해 재구성 → 유효물성 출력.
  ★ **우리 DEM+MPM(공정→구조 예측, 입력단)과 반대 방향** — `positioning_vs_geodict.md` / #18 ACS EL taxonomy.
- **intimate contact (저압 밀착):** 고분자 SE가 슬러리캐스팅에서 AM 표면을 광범위·균일 덮음(수십 MPa, 고압소결
  불요). 우리 모델은 dry-press 황화물(고압)만 — 고분자 저압밀착은 비전이.

---

## ★ 7. 우리 DEM+MPM 비교 (LPSCl 전극 구조지표 = 우리 출력의 이른 같은-소재계 reference) [frame [4]/[5]]

⚠ **대전제 — 두 갈래로 정직히 나눈다:**
- **(A) headline SIC-SPE(고분자):** **우리 LPSCl 황화물 focus가 아님** → SIC-SPE 절대값(σ 0.2×10⁻³·t₊ 0.94·과전압·
  용량·SE-vol 32.1/τ 1.08/coverage 68.2)은 **비전이**(고분자 SE의 저압 intimate contact는 우리 dry-press 황화물
  물리와 다른 계).
- **(B) 비교군 LPSCl 전극:** **우리 정확한 SE(Li₆PS₅Cl) + 우리 활물질(NMC711)** → ★ **디지털트윈이 산출한 LPSCl
  전극의 4개 구조지표가 우리 DEM+MPM 출력과 같은 축, 같은 소재계, 이른(2023) reference.** 이것만 가져온다.

### (a) ★★ LPSCl 전극 디지털트윈 구조지표 = 우리 출력 4종 (핵심 — 추출 대상)

| 디지털트윈 지표 (LPSCl 전극) | **Lee 2023 값** | **우리 DEM+MPM 대응 출력** | 정합 판정 |
|---|---|---|---|
| **SE 부피분율** | **26.1 vol%** | φ_SE(SE 부피분율; porosity·composition에서) — 우리 real_14 φ_SE≈25–28 % | ✅ **자릿수 일치**(우리 생산 φ_SE 대역) |
| **Tortuosity factor** | **1.31** (geodesic) | τ_Laplace,eff / τ_Dijkstra(측지/유효) — 우리 a9_50 τ_Laplace,eff 3.29@p06 | ⚠ **정의 다름**(그들 geodesic vs 우리 Laplace) → 추세만; 단 #266 τ_ion 11.13(MacMullin류)보다 그들 1.31은 다른 정규화 |
| **AM coverage** | **38.8 %** | Stage-E coverage(Tabor/Hertz, cov_AM) — 우리 real_14 Tabor 48–52 % | ✅ **자릿수 일치**(+ #271 LPSCl coverage 35–36%와 거의 같음) |
| **유효 σ_ionic (σ_eff)** | **4.28×10⁻⁵ S/cm = 0.0428 mS/cm** | Kirchhoff σ_ionic — 우리 DEM 범위 ~0.04–0.18 mS/cm | ✅ **하단에 in-range**(단 위상 주의 — 아래 §10) |

**★ 핵심 추출 결론:**
- ✅ **SE-vol 26.1 vol% + AM coverage 38.8%는 우리 출력 대역에 정확히 들어감.** 특히 coverage 38.8%는 **#271
  (Hong 2026)의 LPSCl coverage 35%(Pwd)/36%(PTFE)/26%(NBR)**와 거의 같은 값 → **2개 독립 디지털트윈(2023 Lee +
  2026 Hong)이 LPSCl 전극 AM coverage를 ~26–39%로 수렴** → **우리 Stage-E coverage(Tabor 48–52%, Hertz ~18%)의
  외부 reference**(우리 Tabor가 약간 높은 건 소성 spread 포함 — Hertz 18%가 그들 geometric coverage에 더 가까움).
- ✅ **유효 σ_ionic 0.0428 mS/cm가 우리 DEM 하단(~0.04)에 in-range** — 단 **그들 σ_eff는 intrinsic σ를 구조로
  가중한 출력**이라 **Bazzoun/#271 실측 EIS σ(0.042–0.137)와 위상이 다름**(§10). 그래도 **자릿수(10⁻²–10⁻¹ mS/cm)
  수렴**은 우리 σ_ionic envelope과 합치.
- ⚠ **tortuosity는 정의 차로 절대비교 불가** — 그들 geodesic τ 1.31은 **순수 기하 우회도**(σ_eff/σ_bulk 정규화의
  MacMullin τ 11–16과 다른 척도), 우리 τ_Laplace,eff(constriction 포함, ~3)와도 다름. **추세(SE-vol↑·void↓→τ↓)만 일치.**

### (b) ★ 디지털트윈 = GeoDict top-down/reconstruct(출력단) — positioning 계보 재확인 (frame[5])

**그들 디지털트윈 = GeoDict 기반 reconstruct-from-measurement(출력단 특성화):**
- §2.3이 명시: **GeoDict GrainGeo로 측정 조성·밀도(2.81–2.94 g/cm³)·두께(54–58 µm)·로딩(15.9–16.3 mg/cm²)에
  맞춰 가상 재구성** → **MatDict(percolation·τ·표면적) + ConductoDict(σ_eff, FV) + BESTmicro(전기화학)**로
  구조지표·이온 flux 출력. **intrinsic σ는 입력**(Table S2).
- ⇒ **구조를 측정/조성/밀도에서 재구성하고, 그 위에서 유효물성을 FV로 푼다. 압력·공정에서 구조가 어떻게 나오는지는
  예측하지 않는다**(밀도·두께가 입력). = **GeoDict 출력단 특성화** — `positioning_vs_geodict.md`의 정확히 그 패턴,
  **이 그룹의 가장 이른(2023) 사례**(#18 ACS EL 2024 taxonomy의 "top-down/reconstruction" 정의에 선행 부합;
  #271/#266/#281/#263/#275의 2023 원형).

**우리 DEM+MPM = predict-from-process(입력단 예측):**
- DEM(LIGGGHTS hooke/hysteresis) + MPM(Taichi J2): **압력·조성·입경·첨가제 → 미세구조**를 예측(GrainGeo가 못 하는
  입력단). 그 위에 voxel FV(= ConductoDict 무료 대응) + **Kirchhoff/Holm 접촉망**(연속체 FV가 놓치는 점접촉
  constriction σ_ionic) + Stage-E 소성 접촉면적 + MPM 소성 morphology/void-fill + fracture.

**판정표:**
| 축 | Lee 2023 디지털트윈 (GeoDict) | 우리 DEM+MPM |
|---|---|---|
| 미세구조 출처 | **측정 조성·밀도·두께로 재구성** | **압력·조성에서 예측** ★(GeoDict 불가) |
| 솔버 | ConductoDict FV(연속체) | voxel FV(연속체, 복제) **+ Kirchhoff/Holm 접촉망** ★ |
| σ_ionic | **출력이나 = intrinsic 입력 × 구조**(자기일관 가중) | **출력 = σ_grain × 접촉망**(from-scratch) ★ |
| SE-vol | 출력(26.1 vol%) | 출력(φ_SE) — **대응** ✓ |
| tortuosity | 출력(geodesic 1.31) | 출력(τ_Laplace/Dijkstra) — 정의差, 추세만 |
| AM coverage | 출력(38.8%) | 출력(Stage-E Tabor/Hertz) — **대응** ✓ |
| 입자 형상 | **균일 구·단일크기** | DEM 구(같은 단순화) + **MPM 소성 shape** ★ |
| 소성 morphology·void-fill | ✗(고정 형상) | ✅ MPM ★ |
| 입자파괴·force chain | ✗ | ✅ DEM ★ |
| 시간진화(degradation) | ✗(단일 스냅샷) | ✗(우리도 없음) |

- **frame[4](독립 교차검증):** 그들 LPSCl 구조지표(SE-vol 26.1·coverage 38.8·σ_eff 0.0428)가 **우리 출력 대역과
  같은 자릿수**에 들면 두 접근이 같은 물리를 가리킨다 = 교차검증. 단 **그들 σ_eff는 intrinsic 입력의 구조-가중**이라
  **우리 from-scratch σ와 정보론적 위상이 다름**(완전한 cross-fit 아님 — §10).
- **frame[5](분업):** 그들 디지털트윈은 **이온 transport 출력단**(SE-vol·τ·coverage·σ_eff·flux)에 머물고
  **압력→구조 예측·접촉망 constriction·소성·파괴가 없다**(GrainGeo 고정 구형). 우리는 입력단 예측 + 접촉망 +
  MPM/fracture가 더 넓다. **그들 LPSCl coverage 38.8% = 우리 Stage-E coverage 검증 reference**(우리 Hertz~18%/
  Tabor~50%가 그들 38.8%를 사이에 둠).
- ★ **계보 강화:** #18(Kim 2024 ACS EL, peer-reviewed)이 명명한 **top-down/bottom-up**의 **GeoDict top-down 사례**가
  이미 **2023(이 논문)**에 있었다 → `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야 함"을 이 그룹의 **이른
  원형**으로 재확인. **#271(2026 같은 소재계 σ 앵커)·#266(2026 bimodal)의 직계 선조.**

### (c) ⚠ SIC-SPE(고분자)·셀 절대값 = 비전이 + 공통 GAP

- **SIC-SPE 고분자 전체 = 비전이:** σ 0.2×10⁻³·t₊ 0.94·SE-vol 32.1·τ 1.08·coverage 68.2·과전압·용량은 **고분자
  SE의 저압 intimate contact** 결과. 우리 DEM+MPM은 **dry-press 황화물(LPSCl + AM + (PTFE)) 고압 압축**만 모델 →
  **SIC-SPE 항 없음**. 셀 율속(163/146.5/…/55.8 mAh/g)도 **이-셀-특이**(NMC711 로딩·SE·작동조건 특정).
- ❗ **공통 GAP — 시간진화 없음:** 그들 디지털트윈도 **단일 스냅샷**(cycling 열화·spring-back 없음) → 우리(단일
  압축 스냅샷)와 같은 한계. 둘 다 **정적 구조-물성**만.
- ⚠ **t₊ 축 부재:** 그들은 t₊(0.94 vs 0.99)로 dual-ion 문제를 다루나, **우리 σ_ionic은 t₊≈1(Li⁺ 전도) 가정** →
  t₊ 변조는 우리 모델 밖(LPSCl t₊ 0.99는 우리 가정과 합치하므로 LPSCl 쪽은 문제없음).

### 비교 요약표
| 축 | Lee 2023 (SIC-SPE & LPSCl, ASSB) | 우리 (LPSCl ASSB, DEM+MPM) | 전이/판정 |
|---|---|---|---|
| 소재 headline | **SIC-SPE 고분자** | ✗(focus 아님) | ⚠ 비전이 |
| 소재 비교군 | **LPSCl SE + NMC711** | **동일 ✓** | ★ 구조지표 reference |
| SE-vol(LPSCl) | **26.1 vol%** | φ_SE ~25–28 % | ✅ 자릿수 일치 |
| AM coverage(LPSCl) | **38.8 %** | Stage-E Hertz ~18 / Tabor ~50 % | ✅ 사이에 위치(+ #271 35–36%) |
| tortuosity(LPSCl) | **1.31 (geodesic)** | τ_Laplace,eff ~3 | ⚠ 정의差, 추세만 |
| σ_eff(LPSCl) | **0.0428 mS/cm** | DEM ~0.04–0.18 | ✅ 하단 in-range(위상 주의) |
| 디지털트윈 | **GeoDict reconstruct(출력단), σ 입력** | **DEM+MPM predict(입력단), σ 출력** | frame[5] 분업; positioning 이른 원형 |
| 소성·파괴 | ✗ | ✅ MPM/DEM | frame[5] 우리 우위 |
| 시간 열화 | 단일 스냅샷(없음) | 단일 스냅샷(없음) | 공통 GAP |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 (정직하게 — 중간 관련도)

1) ✅ **LPSCl 전극 구조지표 4종 = 우리 출력의 이른(2023) 같은-소재계 reference.**
   **SE-vol 26.1 vol% / tortuosity 1.31 / AM coverage 38.8% / σ_eff 0.0428 mS/cm**. SE-vol·coverage·σ_eff는
   **우리 DEM+MPM 출력 대역에 자릿수 일치**; 특히 **coverage 38.8%는 #271(Hong 2026) LPSCl coverage 35–36%와
   거의 같음** → **2개 독립 디지털트윈이 LPSCl 전극 AM coverage ~26–39%로 수렴** = 우리 Stage-E coverage(Hertz
   18 / Tabor 50%)의 외부 검증 reference. ★ **이게 이 논문의 최대 가치(우리 출력과 같은 축).**

2) ✅ **디지털트윈 = GeoDict top-down/reconstruct의 이 그룹 가장 이른(2023) 원형 → positioning 계보 강화.**
   측정 조성·밀도·두께를 GrainGeo에 주입 재구성 → ConductoDict FV로 σ_eff·구조지표 출력(**intrinsic σ는 입력**).
   = `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야 함(reconstruct) ↔ 우리는 예측(predict, 입력단)"을 이
   그룹의 **이른 사례**로 재확인. **#18(ACS EL 2024 taxonomy)·#271/#266(2026)의 직계 선조** → 우리 공정→구조
   예측 + 접촉망 superset 논지의 계보적 근거(2023부터 GeoDict 출력단에 머물러 왔음).

3) ⚠ **σ_eff는 "intrinsic σ × 구조" 출력이라 우리 from-scratch σ와 위상이 다름 — 절대 σ 앵커는 아니다.**
   그들 σ_eff(LPSCl 0.0428)는 **intrinsic 2.2×10⁻³을 구조(SE-vol·τ)로 가중**한 값(intrinsic의 1.9% 유지). 우리
   Kirchhoff σ_ionic은 **σ_grain·접촉망에서 from-scratch 예측**. ⇒ **σ 절대 검증 앵커는 Bazzoun/#271/Varkey/
   Minnmann/#266 유지**(이 논문 σ는 자릿수 in-range reference로만; 정밀 1:1 아님). headline SIC-SPE(고분자)·셀
   절대값은 비전이.

### 보너스 — 추출한 LPSCl 전극 디지털트윈 수치(우리 reference)
- SE 부피분율 **26.1 vol%**, tortuosity factor **1.31**(geodesic), AM coverage **38.8 %**, 유효 σ_ionic
  **4.28×10⁻⁵ S/cm = 0.0428 mS/cm**(intrinsic LPSCl 2.20×10⁻³ → σ_eff/intrinsic = **1.9%**). 전극밀도 2.81 g/cm³,
  두께 58 µm, NMC711 로딩 16.3 mg/cm², LPSCl D50 2.3 µm, NMC711 D50 8.0 µm. 조성 NMC711:LPSCl:NBR:Super P =
  76.8:19.2:2:2 wt%. (SIC-SPE 전극은 비교용: SE-vol 32.1 / τ 1.08 / coverage 68.2 / σ_eff 2.85×10⁻⁵.)

---

## 9. comparison_vs_ours / properties 반영 메모

- **축 B(transport triad):** Lee 2023 LPSCl σ_eff 0.0428 mS/cm = 우리 σ_ionic envelope(0.04–0.18) 하단에 in-range
  (**digital-twin 출력 = intrinsic×구조라 위상 주의** — 절대 앵커 아님, 자릿수 reference). LPSCl tortuosity 1.31
  (geodesic) = 우리 τ 출력의 다른-정규화 reference.
- **축 C(coverage/mechanics):** ★ LPSCl AM coverage 38.8% = 우리 Stage-E coverage(Hertz 18 / Tabor 50%) 사이에
  위치 + #271 35–36%와 수렴 → **2개 독립 디지털트윈으로 LPSCl coverage ~26–39% 검증 reference**.
- **축 A(compaction/porosity):** LPSCl SE-vol 26.1 vol% = 우리 φ_SE 대역(real_14 ~25–28%) 일치(이른 same-system).
- **축 E(where-we-validate-lit):** LPSCl 구조지표 4종이 우리 출력 대역과 자릿수 일치 = frame[4] 약한 교차검증
  (σ 위상 차로 정밀 1:1 아님).
- **축 F(what-we-can't-do-yet):** SIC-SPE 고분자 저압 intimate contact, t₊ 변조, 시간(cycling) 열화 = 미모델
  (공통 GAP).
- **positioning:** GeoDict top-down/reconstruct의 이 그룹 가장 이른(2023) 사례 → #18/#271/#266의 계보 선조
  (`positioning_vs_geodict.md`·#18 cross-ref).

---

## ★ 10. 비판적 한계 (over-claim 금지)

- **σ_eff는 입력의 자기참조 가중(가장 중요한 위상 주의):** 그들 σ_eff(LPSCl 0.0428)는 **실측 intrinsic σ
  (2.2×10⁻³)를 구조로 가중**한 출력 — **모델이 σ를 from-scratch 예측한 게 아니다**(intrinsic은 Table S2 입력).
  ⇒ 우리 Kirchhoff σ_ionic(σ_grain·접촉망에서 순추론)과 **정보론적 위상이 다름** → "σ_eff 0.0428이 우리 0.04와
  비슷"은 **자릿수 reference**지 **점대점 검증이 아니다**. σ 절대 앵커는 Bazzoun/#271/Minnmann/#266 유지.
- **단일압력·digitized 아님이나 단일조건:** LPSCl 전극 = **500 MPa 압착 1조건**(우리 300 MPa·Bazzoun 400 MPa·#271
  350 MPa과 다름; 압력↑→σ↑·porosity↓). 수치는 텍스트 명시(digitized 아님 = 정밀)지만 **1조건 1전극** → 다압력·
  다조성 일반화 미검증.
- **tortuosity 정의 불일치:** 그들 geodesic τ(1.31)는 **순수 기하 우회도**, 우리 τ_Laplace,eff(constriction 포함,
  ~3)·#266 MacMullin τ_ion(11–16)과 **다른 척도** → SE-vol↑→τ↓ 추세만 일치, 절대값 비교 불가.
- **구형·단일크기 단순화:** 디지털트윈 입자 = **균일 구·단일 D50**(NMC 8.0 / LPSCl 2.3 µm) → 다결정·다분산 PSD·
  bimodal 없음 = 우리 DEM 구-입자와 같은 한계(우리 MPM 소성 shape·Furnas bimodal이 그들엔 없음 — frame[5] 우리
  우위). **소성 형상변화·void-fill·force chain·파괴 전무**(GrainGeo 고정 구형).
- **headline = 고분자(비-우리-소재계):** 이 논문의 주역은 SIC-SPE(고분자)다 — **우리 LPSCl 황화물 focus가 아님**.
  우리가 가져오는 건 **LPSCl 비교군의 구조지표 4종 + GeoDict positioning**뿐. SIC-SPE 결론(저압밀착·t₊·과전압)은
  우리 모델과 무관(비전이).
- **σ_eff 비율 해석 주의:** "LPSCl 1.9% vs SIC-SPE 14.3% 유지"는 **그들 구조+intrinsic 가정 하의 상대값** —
  LPSCl이 NBR 절연상(2 wt%)을 포함하는 조성(SIC-SPE 전극엔 NBR 없음)이라 **조성이 다른 두 전극의 비교**임을 유념
  (순수 SE 차이 아님; SIC-SPE 전극은 바인더-free, LPSCl 전극은 NBR 2 wt% 포함 → coverage·σ_eff 격차의 일부는
  NBR 절연상 탓 — #271이 같은 NBR 효과를 정량).
- **rigid-sphere/연속체 공통 한계:** 그들 GeoDict(고정 구형)도 우리 DEM(강체구+overlap-proxy)도 **소성 입자
  형상변화 없음**(우리 MPM만 있음). 그들은 **σ 입력 + 단일 스냅샷**이라 압축역학·접촉망·소성·파괴가 전무 →
  frame[5]에서 우리가 더 넓음은 분명하나, **그들 강점(실측 셀 검증 + GeoDict robust 연속체 + 2023 이른 사례)**은
  정직히 인정.
