# Impact of Conductive Agents in Sulfide Electrolyte Coating on Cathode Active Materials for Composite Electrodes in All-Solid-State Batteries — Kim et al. (Battery Energy 2025)

> slug `kim2025_conductive_agent_se_coating_cathode` · DOI `10.1002/bte2.20250027` (Battery Energy 2025; 4:e70044) · type `exp (전극 제작·미세구조·전기화학 — DFT/계산 없음)` · PDF `bed8fa69-08._Impactteries.pdf` (+ SI `00e03394-08._Sup_Imeries.docx`, figure-list S1–S12) · digested `2026-06-25` · status ✅
> **저자**: Dongyoung Kim ¹, Jongjun Lee ¹ (공동 1저자, "D. Kim and J. Lee contributed equally"), Seungyeop Choi ¹, Myunggeun Song ¹, Hyobin Lee ², **Yong Min Lee** ¹,²,³ *(corr., yongmin@yonsei.ac.kr)*
> ¹ **Yonsei Univ., Chemical & Biomolecular Engineering (Seoul)** · ² **DGIST, Energy Science & Engineering (Daegu)** · ³ **Yonsei Univ., Battery Engineering (Seoul)**
> Battery Energy **4** (2025) e70044 · Received 29 Apr 2025 / Revised 1 Aug 2025 / Accepted 9 Aug 2025 · OPEN ACCESS (CC-BY) · Funding: NST (No. GTL24011-000) + MOTIE Technology Innovation Program (No. 2410009726)

---

## 0. 이 digest를 읽는 법 (핵심 + 우리와의 관계)

이 논문은 **우리 연구실 계보(Yonsei Yong Min Lee group + DGIST)** 의 **실험·전극공정** 논문이다 — 막 digest한 [KimICCF] (Kim/Cho/Y.M.Lee, ICCF 시트, CEJ 2026)의 **자매편**. **결정 격자를 바꾸는 DFT 도핑 논문이 아니다.** 다루는 질문은 단 하나:

> **"고체전해질(SE)을 양극활물질(CAM) 표면에 코팅할 때, 그 코팅 공정에 도전재(CA)를 같이 넣으면 무슨 일이 일어나는가?"**

핵심 결론: **CA를 SE 코팅에 넣는 것 자체는 양날의 검이고, CA의 "차원(dimensionality)"이 결과를 가른다.**
- **CA 없음 (SE@CAM)** = CAM 표면에 **치밀한(dense) SE 코팅층** 형성 → 좋음(기준).
- **0D 카본블랙 Super P (SE-SP@CAM)** = Super P가 코팅층에 **응집·과잉(Super-P-rich layer)** → CAM 활성표면적↓·코팅층 전자전도↓ → **나쁨**.
- **1D 기상성장탄소섬유 VGCF (SE-VGCF@CAM)** = VGCF가 코팅층에 **드물게 박힘(embedded)** → 활성표면적↑·전자전도 경로 형성 → **좋음 (SE-SP보다 좋고, CA 없는 SE@CAM과 동등)**.

**메시지**: 양극 복합체 성능을 좌우하는 레버는 **코팅층의 형상(morphology)과 전자전도 경로**이며, 이는 **CA의 차원과 혼합 프로토콜(mixing protocol)** 로 결정된다. → 우리 프로젝트와의 연결은 **개념 수준**(레버 = 미세구조·계면·전자전도, bulk 결정 아님; §7·§8). **DFT 수치 직접 비교는 불가**(이 논문엔 계산 전혀 없음).

> ⚠ **전압 기준**: 모든 셀은 **NCM/Li half-cell** (반쪽전지, Li 금속 음극 — 단 음극은 In(Li-In) foil; 본문 "Li metal foil"). 충방전 cut-off **3.0–4.3 V** (CC/CV charge, CC discharge). [KimICCF]·[Zuo]의 Li-In 환산(−0.62 V) 같은 보정은 이 논문에서 불필요 — Li-In half-cell 절대전위 그대로 읽는다.

> ⚠ **약어 주의 (3종 전극 구분이 이 논문의 전부)**:
> - **SE@CAM** = CA 없이 SE만 코팅 (planetary mixing) → **dense** 코팅층 (기준, 좋음)
> - **SE-SP@CAM** = Super P를 SE 코팅 공정에 동시 투입 (single-step planetary mixing) → **Super-P-rich porous** 코팅층 (나쁨)
> - **SE-VGCF@CAM** = VGCF를 SE 코팅 공정에 동시 투입 (single-step) → **VGCF-embedded porous** 코팅층 (좋음)
> - (참고) **CAM** (manual mixing 대조군) = SE@CAM·SE-SP@CAM를 만들 때, SE-coated CAM에 Super P를 mortar/pestle로 손혼합. 본문 Fig S3에서 "denoted as CAM"으로 한 번 등장 — SE@CAM이 이 manual-mixing CAM보다 우수.

---

## 1. 한 줄 요약

LiNbO₃-coated NCM711(D50 7 µm) 위에 Li₆PS₅Cl(LPSCl, D50 1 µm)를 planetary-mixer로 코팅할 때, **CA 없이 코팅하면 치밀한 SE층(SE@CAM, 50–500 nm, 첫방전 185.3 mAh/g·CE 81.6 %, 200 cyc retention 70.9 %)** 이 형성된다. 같은 공정에 **0D Super P를 넣으면(SE-SP@CAM)** Super P가 코팅층(500 nm–2 µm)에 응집해 **Super-P-rich**가 되어 CAM-SE 접촉을 막고 코팅층 **전자전도도가 3,000배 낮아지고(3.3×10⁻² → 1.0×10⁻⁵ S/cm), 활성표면적이 절반(1.00→0.51 S)** 으로 줄어 **성능이 크게 나빠진다(첫방전 151.6 mAh/g·CE 78.0 %, 200 cyc 113.0 mAh/g·retention 70.9 %)**. 반면 **1D VGCF를 넣으면(SE-VGCF@CAM)** VGCF가 코팅층에 드물게 박혀 **다공성 SE층 + 전자전도 경로**를 형성, **전자전도도가 SE@CAM 수준으로 회복(1.4×10⁻² S/cm)** 되고 **첫방전 183.5 mAh/g·CE 82.7 %, 200 cyc 117.3 mAh/g·retention 76.8 %** 로 **SE-SP보다 우수하고 SE@CAM과 동등**한 성능을 낸다. 차이의 근원은 **CA의 차원(0D vs 1D)이 코팅 중 LPSCl 변형·CA 분산을 다르게 만들기 때문**: 작은 0D Super P는 변형하는 LPSCl 속에 쉽게 매립되어 dense·Super-P-rich 층을 만들고, 길고 굵은 1D VGCF(직경 ~150 nm, 길이 ~10 µm)는 LPSCl의 전단(shear) 변형을 방해해 다공성 층에 sparse하게 박힌다. **결론: composite cathode 성능의 레버는 코팅층 형상·전자전도 경로이며, CA 선택(차원)과 mixing protocol이 그것을 지배한다.**

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 시스템 | **ASSB composite cathode** (황화물 SE 기반) — SE를 CAM에 코팅하는 공정 + CA 투입의 영향 |
| **CAM** | **LiNbO₃-coated NCM711** = LiNbO₂-coated Li(Ni₀.₇₀Co₀.₁₅Mn₀.₁₅)O₂, **D50 = 7 µm** (LiNbO₃ = 표준 양극 코팅, 황화물-NCM 계면 보호) |
| **SE** | **Li₆PS₅Cl (LPSCl)** = POSCO JK Solution, **D50 = 1 µm** (= 우리 **comp1** 베이스 조성) |
| **CA (도전재)** | **Super P** (0D 카본블랙, Imerys, 1차입자 ~40 nm) / **VGCF** (1D 기상성장탄소섬유, Showa Denko, 직경 ~150 nm·길이 ~10 µm) |
| **무게비** (composite cathode) | **CAM : SE : CA = 68.0 : 29.1 : 2.9 wt%** |
| **코팅 장비** | **planetary mixer (AR-100, Thinky Corporation), 2000 rpm, 5 h** |
| **3종 전극** | **SE@CAM**(CA無, dense) / **SE-SP@CAM**(0D, Super-P-rich) / **SE-VGCF@CAM**(1D, VGCF-embedded) |
| 음극 | **Li metal foil (Honjo Metal)** — half-cell (본문은 "Li metal"; 일부 표기 NCM/Li) |
| SE 분리막 | **LPSCl pellet, 150 mg, D50 5 µm, PEEK mold 13 mm, 70 MPa** pelletizing |
| 셀 압력 | 복합양극 26.5 mg → LPSCl pellet 한쪽에 올려 **370 MPa·1 min** 가압, Li foil 반대쪽, 셀 작동 **50 MPa** |
| 동기/갭 | 복합양극은 **CAM·SE·CA·(binder)** 로 구성, 큰 활성표면적 + well-connected ion/electron 경로 필요. SE 코팅(CAM 위)은 활성표면적↑·입자응집↓·분산↑로 성능↑·열화↓ → 널리 연구됨. 그러나 **"코팅 공정"·"전기화학 성능" 위주 연구뿐**, **CA가 SE 코팅 *중에* 미치는 영향은 거의 미개척** |
| 핵심 미개척 | SE-coated CAM에서 **SE가 CAM-CA 접촉을 막아 전자전도를 방해**할 수 있음([39,40]) → **CA와 그 분포를 코팅 시 신중히 고려해야 함**. + **mixing protocol이 복합체 내 물질분포를 크게 좌우**([32,39–42]). 이 둘이 미탐구 |

> **선행 대비 차별**: 기존(refs 29–33, 37 등)은 SE 코팅 공정 개발·성능 향상에 집중. 이 논문은 처음으로 **CA를 SE 코팅 공정에 넣었을 때 CA 분포·코팅층 형상·복합전극 구조가 어떻게 달라지나** 를 0D vs 1D CA로 체계 비교 — **"CA 차원이 코팅 형상을 지배"** 라는 새 변수 제시.

---

## 3. 핵심 물성 (수치 총정리)

### 3.1 전기화학 성능 (3종 전극 직접 비교) — **이 논문의 정량 핵심**

| 지표 | **SE@CAM** (dense) | **SE-SP@CAM** (Super-P-rich) | **SE-VGCF@CAM** (embedded) | 출처/조건 |
|---|---|---|---|---|
| **첫 방전용량** (0.1C, 25 ℃) | **185.3 mAh/g** | **151.6 mAh/g** | **183.5 mAh/g** | Fig 4a / 5d |
| **초기 CE** (1st coulombic efficiency) | **81.6 %** | **78.0 %** | **82.7 %** | Fig 4a / 5d |
| **200 cyc 후 방전용량** (0.1C charge / 0.5C discharge, cycling test) | n/a (Fig 4f·5f 추세선, 명시 수치 없음 — SE-SP·VGCF보다 높음) | **113.0 mAh/g** | **117.3 mAh/g** | Fig 4f / 5f |
| **200 cyc 용량유지율** | n/a (명시 없음, 최상위 추세) | **70.9 %** | **76.8 %** | Fig 4f / 5f |
| **rate capability** (0.1→2.0C) | 우수(기준) | **나쁨** (C-rate↑일수록 급강하) | SE@CAM과 **유사** (단 C-rate↑서 SE-SP보다 덜 떨어짐, SE@CAM보다 약간↓) | Fig 4e / 5e |
| **분극(polarization)** | 작음 | **큼** (poor electrode structure) | 작음 | Fig 4b (GITT) |

- **명시된 비교 문장(본문)**: SE-VGCF@CAM 첫방전 **183.5 mAh/g·CE 82.7 %** = "higher than SE-SP@CAM (151.6, 78.0 %) and comparable to SE@CAM (185.3, 81.6 %)". 200 cyc: SE-VGCF **117.3 mAh/g·76.8 %** = "comparable to SE@CAM (113.0 mAh/g·70.9 %)... while maintaining significantly higher discharge capacity than SE-SP@CAM throughout cycling".
- ⚠ **숫자 주의**: 본문은 **200 cyc 절대용량을 SE@CAM 113.0/70.9 %, SE-VGCF@CAM 117.3/76.8 %** 로 쓰는데, 이는 **SE-SP@CAM의 cycling 수치(113.0·70.9 %)와 SE@CAM을 한 비교 문장에서 묶어** "VGCF가 SE@CAM과 comparable" 이라 서술한 부분과 텍스트가 겹친다. 직접 읽히는 확정 수치: **SE-SP@CAM = 113.0 mAh/g·70.9 % @200 cyc** (Fig 4f 명시), **SE-VGCF@CAM = 117.3 mAh/g·76.8 % @200 cyc** (Fig 5f 명시). SE@CAM의 200 cyc 절대값은 추세선상 최상위지만 본문이 별도 숫자로 못 박지 않음 → **"n/a (최상위 추세)"** 로 기록.

### 3.2 코팅층 전자/이온 전도도 (electron-/ion-blocking cell 측정) — **메커니즘 정량 핵심**

| 전극 | **전자전도도 σ_e** (DC 50 mV, electron-blocking Ti/composite/Ti) | **이온전도도 σ_i** (EIS, ion-blocking) | 출처 |
|---|---|---|---|
| **SE@CAM** | **3.3×10⁻² S/cm** | **1.3×10⁻⁴ S/cm** | Fig 3i–k |
| **SE-SP@CAM** | **1.0×10⁻⁵ S/cm** (= **3 orders 낮음**) | **0.9×10⁻⁴ S/cm** (약간↓) | Fig 3i–k |
| **SE-VGCF@CAM** | **1.4×10⁻² S/cm** (= SE@CAM 수준, SP보다 **3 orders 높음**) | **1.6×10⁻⁴ S/cm** (SE@CAM과 유사) | Fig 5c / S10 |

- **핵심 역설**: **Super P(도전재)를 더 넣었는데 코팅층 전자전도도가 오히려 3,000배 떨어진다(3.3×10⁻² → 1.0×10⁻⁵ S/cm).** 이유: Super P가 코팅층에 응집해 **SE-SE 이온경로**와 **CAM-CA 전자경로**를 동시에 교란 — Super P가 코팅층에 갇혀 코팅층 밖 도전망과 단절(Fig 2의 "Super P가 코팅층 안에 응집, 밖엔 거의 없음"). VGCF는 길어서 코팅층 안팎을 잇는 전자경로 형성 → σ_e 회복.
- **이온전도도**는 세 전극 모두 비슷한 차수(0.9–1.6×10⁻⁴ S/cm) — SE-SP가 약간 낮음(코팅층 내 SE 입자가 응집 Super P에 의해 SE-SE 이온경로에서 고립).

### 3.3 활성표면적 (GITT 기반 상대 active surface area)

| 전극 | 상대 활성표면적 (a.u., SE@CAM=1.00 기준) | 출처 |
|---|---|---|
| **SE@CAM** | **1.00 S** (기준) | Fig 4c |
| **SE-SP@CAM** | **0.51 S** (= **절반**) | Fig 4c |

- **계산식 (GITT diffusion, Eq 본문)**: D = (4/πτ)(m_NCM·V_M / M_NCM·S)² (ΔE_s/ΔE_t)²
  - D = Li⁺ 확산계수, τ = 펄스 지속시간, m_NCM = NCM 로딩량, V_M = NCM 몰부피, M_NCM = NCM 분자량, **S = 활성표면적**, ΔE_s = 정상상태 전압변화, ΔE_t = 과도 전압변화.
  - SE@CAM 활성표면적을 **1.00 S로 고정** → SE-SP@CAM = **0.51 S** (CAM-SE 접촉이 Super P 과잉 코팅층 때문에 절반으로 감소).
- ⚠ SE-VGCF@CAM의 활성표면적은 본문에 별도 수치 없으나, "VGCF가 다공성 SE 코팅층을 형성해 **활성표면적을 늘린다(enlarging the active surface area)**" 로 정성 서술. 다공성 = CAM 노출↑ = 활성표면적↑.

### 3.4 코팅층 형상 (SEM/EDS, 3종 전극) — **morphology 정량/정성**

| 전극 | 코팅층 두께 | 코팅층 구조 | CA 분포 | 출처 |
|---|---|---|---|---|
| **bare NCM** | — | polyhedral·angular, 매끈, 명확한 grain boundary | — | Fig 1b |
| **SE@CAM** | **~50–500 nm** | **dense (치밀)**, 상대적으로 균일. CAM 표면을 **완전히 덮지 않음**(노출 영역 = CAM-CA contact point, white arrow) | Super P가 SE-coated CAM 표면에 **불균일 산포(uneven, mortar 손혼합)**. CAM 각진 모양→둥글어지고 표면 bumpy, grain boundary 가려짐 | Fig 1c, 2a–e |
| **SE-SP@CAM** | **~500 nm – 2 µm** (훨씬 두꺼움) | **porous (다공성)**, 두 상으로 구성: 밝은 회색=LPSCl, 어두운=Super P. **Super P가 코팅층 상당부분 차지·불균일 분포**. dense층 형성 안 됨 | Super P가 **CAM 주위로 응집(agglomerate)**, 코팅층 밖엔 소량만. EDS C: SE@CAM=균일, SE-SP@CAM=CAM 주위만 부분응집 | Fig 1d, 2f–j, 3e–h |
| **SE-VGCF@CAM** | (다공성, 두께 명시 없음) | **porous LPSCl 코팅층** — LPSCl이 CAM 표면서 **부분 분쇄(partial crushing)**, **VGCF가 코팅층 전반에 sparse하게 박힘** | rod-shaped VGCF가 표면에 소량 관찰. CAM·SE 분포는 SE@CAM·SE-SP@CAM과 유의차 없음(EDS Ni/S) | Fig 5a,b, S7–S9 |

- **SE@CAM EDS (Fig 2b–e, cross-section)**: 코팅층 = LPSCl + 산포된 Super P. 코팅층이 CAM을 **완전히 덮지 않음** → 노출 CAM이 **CAM-CA 접촉점** 제공(white arrow) → 전자전도 촉진.
- **SE-SP@CAM EDS (Fig 2g–j)**: LPSCl과 Super P가 코팅층 전반에 **불균일 분포**, Super P가 코팅층 상당부분 점유. LPSCl 입자가 코팅층 안팎에서 **원래 형상 유지** → Super P가 코팅 중 LPSCl 전단변형을 완화(LPSCl이 덜 변형).

---

## 4. DFT / 계산 방법 ★

**해당 없음.** 이 논문은 **순수 실험·전극공정 논문**으로 **DFT·AIMD·MLIP·digital-twin 등 어떤 계산도 포함하지 않는다.** ([KimICCF]가 분자 HOMO/LUMO + GeoDict를 보조로 쓴 것과 대조 — 이 자매편은 계산 0.) → **우리 bulk 결정 DFT(밴드/AIMD/grand-potential)와 수치 대조 불가**; 비교는 **개념(레버·미세구조)** 수준에서만(§7).

> 우리 H-list(못 보는 것)와의 관계: 이 논문은 **device-level 전극 미세구조·전자전도 경로**를 다루는데, 이는 우리 bulk DFT가 원천적으로 못 보는 영역. [KimICCF]의 GeoDict digital-twin이 시트 σ를 메웠다면, 이 논문은 **복합양극의 σ_e/활성표면적이 형상으로 결정됨을 실험으로** 보여 — 우리 "lever = microstructure/interphase" 결론의 **실험적 보강**(계산 없이).

---

## 5. 결과 — 섹션별 상세 (전 figure·전 수치)

### 5.1 코팅 공정과 표면 형상 (Fig 1, §3 도입)
- **공정 스킴 (Fig 1a)**:
  - **SE@CAM (2-step)**: NCM711 + LPSCl을 planetary mixer **2000 rpm 5 h** → SE-coated CAM. 그 다음 **Super P 추가 → mortar/pestle 손혼합(hand mixing)**. → CAM이 **LPSCl로만 코팅**될 것으로 기대.
  - **SE-SP@CAM (1-step)**: NCM, LPSCl, Super P를 **동시 투입 → planetary 2000 rpm 5 h**. → 코팅층이 **LPSCl + Super P 둘 다**로 구성될 것으로 기대.
  - **SE-VGCF@CAM (1-step)**: SE-SP@CAM과 **동일 공정**이되 Super P 대신 **VGCF** 사용.
- **표면 SEM (Fig 1b–d)**:
  - **bare NCM (1b)**: polyhedral·angular, 명확한 grain boundary, 매끈.
  - **SE@CAM (1c)**: 각진 모양→둥글어짐, 표면 bumpy, grain boundary 가려짐 = **SE 코팅층 형성 성공**. 추가로 **clustered Super P가 표면에 불균일 산포**(mortar 손혼합 탓).
  - **SE-SP@CAM (1d)**: **dense층 관찰 안 됨**. 대신 **불규칙 LPSCl 입자가 표면에 조밀 산포하되 원래 형상 유지**. CAM 표면에 **Super P 거의 없음** → Super P가 코팅층 *안에* 갇힘 시사.
- (Fig S1: LPSCl·Super P 원료 SEM. Super P 1차입자 ~40 nm.)

### 5.2 단면 형상·EDS (Fig 2) — **dense vs porous의 근거**
- **SE@CAM (2a–e)**: 코팅층 **~50–500 nm, 상대적 dense**. EDS: 코팅층 = LPSCl + 외곽 SE층에 산포된 Super P. **코팅층이 CAM 완전피복 안 함** → 노출 CAM = CAM-CA 접촉점(white arrow) → 전자전도 촉진.
- **SE-SP@CAM (2f–j)**: 코팅층 **~500 nm–2 µm, porous**, 두 상(밝은 LPSCl / 어두운 Super P) 혼재, **Super P가 상당부분·불균일**. LPSCl 입자 **원형 유지(코팅 안팎)** → Super P가 LPSCl 전단변형 완화. EDS(2g–j): LPSCl·Super P **불균일 분포**.

### 5.3 복합전극 단면·EDS + 전도도 (Fig 3) — **σ_e 3,000배 격차**
- **Cross-section + EDS (3a–h)**: SE@CAM·SE-SP@CAM 복합전극의 CAM·SE 분포는 **유의차 없음**(Ni, S map). 차이는 **dark-gray Super P(C)**: SE@CAM = **균일 분산(homogeneous)**, SE-SP@CAM = **CAM 주위만 응집(agglomerate), 그 외 영역엔 소량**.
- **DC polarization (3i)**: 전자전도도. **SE@CAM 3.3×10⁻² S/cm vs SE-SP@CAM 1.0×10⁻⁵ S/cm (3 orders 낮음).** 이유: Super P가 코팅층 안에 응집 → 코팅된 CAM 입자 간 전자연결 차단.
- **Nyquist (3j) + 이온전도도 (3k)**: SE-SP@CAM이 SE@CAM보다 높은 계면저항(poor structure·low σ_e·작은 활성표면적). **σ_i: SE-SP@CAM 0.9×10⁻⁴ < SE@CAM 1.3×10⁻⁴ S/cm** (약간↓ — SE 입자가 응집 Super P에 의해 SE-SE 이온경로에서 고립).
- **결론(3)**: Super P를 코팅 공정에 넣으면 **코팅층이 근본적으로 바뀌어** 복합전극 구조·물성에 큰 악영향. **mixing protocol이 전극 구조·성능을 크게 좌우** 강조.

### 5.4 전기화학 성능 SE@CAM vs SE-SP@CAM (Fig 4)
- **첫 충방전 0.1C (4a)**: SE@CAM **185.3 mAh/g·CE 81.6 %** > manual-mixing 대조군 CAM(Fig S3) → **SE 코팅이 성능↑**. SE-SP@CAM **151.6 mAh/g·CE 78.0 %** (낮음).
- **GITT polarization (4b, S4)**: SE-SP@CAM 분극 큼 (poor structure).
- **상대 활성표면적 (4c)**: SE@CAM **1.00 S** 기준, SE-SP@CAM **0.51 S** (절반) — CAM-SE 접촉이 Super P 과잉 코팅 탓에 절반.
- **Nyquist (4d)**: SE-SP@CAM 계면저항 큼.
- **rate (4e, S5·S6)**: SE-SP@CAM C-rate↑일수록 급강하(poor rate).
- **cycling (4f, 0.1C charge/0.5C discharge)**: SE-SP@CAM **200 cyc 113.0 mAh/g·retention 70.9 %**. SE@CAM이 throughout 더 높음. → "Super P를 SE 코팅에 넣으면 전극구조·성능 크게 악화. **mixing protocol 변경이 구조·성능 크게 좌우**."

### 5.5 VGCF로 차원 효과 검증 (Fig 5) — **이 논문의 클라이맥스**
- **형상 (5a,b, S7–S9)**: SE-SP@CAM과 **같은 1-step 공정**인데 형상이 **확연히 다름**. LPSCl이 CAM 표면서 **부분 분쇄**(SE-SP에선 LPSCl 원형 유지였음). **VGCF가 표면에 소량(rod-shaped)** + 단면서 **porous LPSCl 코팅층 + 코팅층 전반에 sparse VGCF**. EDS(S8,S9): CAM·SE 분포는 타 전극과 유사, VGCF 존재 확인.
- **차원 메커니즘 (본문, 매우 중요)**:
  - **Super P = 0D, 1차입자 ~40 nm** → 작고 둥글어 **변형하는 LPSCl 속에 쉽게 매립** → 상대적 **compact(dense에 가까운) 코팅층** (단, Super P 과잉으로 Super-P-rich). LPSCl 전단변형을 Super P가 완화 → LPSCl 원형 유지.
  - **VGCF = 1D, 직경 ~150 nm·길이 ~10 µm (NCM 입경에 필적)** → **높은 종횡비 → LPSCl의 전단변형(shear)을 방해 → 코팅층이 더 porous** + VGCF가 sparse하게 박힘. LPSCl은 (Super P 보호 없이) 부분 분쇄.
- **전도도 (5c, S10)**: **SE-VGCF@CAM σ_e = 1.4×10⁻² S/cm** = SE-SP@CAM(1.0×10⁻⁵)보다 **3 orders 높음**, SE@CAM(3.3×10⁻²)과 **comparable**. **σ_i = 1.6×10⁻⁴ S/cm** = SE@CAM(1.3×10⁻⁴)과 유사. → VGCF가 코팅층 전반에 **균일 전자경로** 형성 + porous 구조로 **활성표면적↑**. "1-step VGCF 코팅이 2-step SE@CAM(+추가 Super P 혼합)과 동등한 전도/구조를 더 간단하게 달성."
- **전기화학 (5d–f)**:
  - **첫방전 0.1C (5d)**: SE-VGCF@CAM **183.5 mAh/g·CE 82.7 %** = SE-SP@CAM(151.6·78.0 %)보다 높고 SE@CAM(185.3·81.6 %)과 comparable.
  - **rate (5e, S11·S12)**: SE-VGCF@CAM ≈ SE@CAM (단 C-rate↑서 SE@CAM보다 약간 더 떨어짐, 그래도 SE-SP보다 훨씬 우수).
  - **cycling 200 cyc (5f, 0.1C charge/0.5C discharge)**: SE-VGCF@CAM **117.3 mAh/g·retention 76.8 %** = SE@CAM과 comparable, SE-SP@CAM보다 throughout 높음.
- **메커니즘 스킴 (5g)**: **SE-SP@CAM** = CAM 주위 Super P 응집(코팅층 안), 전자경로 부분 단절. **SE-VGCF@CAM** = VGCF가 입자 간·코팅층 전반을 가로질러 e⁻ 경로 + Li⁺ 경로 함께 표시 → "VGCF-embedded porous 코팅층이 e⁻/Li⁺ 둘 다 잘 흐르게".

### 5.6 결론 (Conclusion 섹션)
- CA를 SE 코팅 공정에 넣을 때 효과는 **CA 차원에 좌우**: **SE@CAM = dense층(좋음)**; **SE-SP@CAM(0D) = Super-P-rich층 → 활성표면적·σ_e↓ → 나쁨**; **SE-VGCF@CAM(1D) = VGCF-embedded porous층 → 활성표면적·전자전도↑ → SE-SP보다 우수, SE@CAM과 동등(더 간단한 1-step 공정으로)**.
- **CA가 복합전극 구조·성능을 결정적으로 좌우** → **mixing protocol과 CA 선택(차원)이 ASSB 전극 제작의 핵심.**

---

## 6. 메커니즘 종합 — **왜 VGCF(1D)가 Super P(0D)를 이기나**

**한 문장**: CA의 **차원(0D vs 1D)** 이 코팅 중 LPSCl의 변형 거동과 CA 분산을 다르게 만들어, **0D Super P는 dense·Super-P-rich(전자전도·활성표면적↓) 층**을, **1D VGCF는 porous·전자경로-연결(전자전도·활성표면적↑) 층**을 만든다.

**0D Super P (SE-SP@CAM) — 왜 나쁜가:**
1. Super P(1차입자 ~40 nm)는 작고 둥글어 **planetary mixing 중 변형하는 LPSCl 속에 쉽게 매립** → LPSCl 전단변형을 **완화**(LPSCl 원형 유지) → 상대적으로 두꺼운(500 nm–2 µm) **Super-P-rich** 코팅층.
2. Super P가 **CAM 주위 코팅층 안에 응집** → 코팅층 밖 도전망과 단절 → **CAM-SE 접촉 차단 → 활성표면적 1.00→0.51 S (절반)**.
3. 응집 Super P가 SE-SE 이온경로·CAM-CA 전자경로 동시 교란 → **σ_e 3.3×10⁻²→1.0×10⁻⁵ S/cm (3,000배↓)**, σ_i 약간↓.
4. → 높은 계면저항·큰 분극·poor rate·낮은 용량(151.6 mAh/g)·낮은 retention.

**1D VGCF (SE-VGCF@CAM) — 왜 좋은가:**
1. VGCF(직경 ~150 nm·길이 ~10 µm, NCM 입경 7 µm에 필적)는 **높은 종횡비** → LPSCl의 **전단변형을 방해** → 코팅층이 **porous**(LPSCl 부분 분쇄, Super P처럼 완화 안 됨) → **CAM 노출↑ = 활성표면적↑**.
2. VGCF가 **코팅층 전반에 sparse하게 박혀** 입자 간·코팅 안팎을 잇는 **연속 전자경로** 형성 → **σ_e가 SE@CAM 수준으로 회복(1.4×10⁻² S/cm)**.
3. porous 구조라 σ_i도 유지(1.6×10⁻⁴ S/cm) → e⁻·Li⁺ 둘 다 원활.
4. → SE@CAM과 동등한 용량(183.5 mAh/g·CE 82.7 %)·retention(76.8 %)을, **더 간단한 1-step 공정**으로.

**왜 SE@CAM(CA無)이 기준으로 좋은가:**
- CA 없이 LPSCl만 코팅 → **dense·thin(50–500 nm)** 층, CAM을 완전피복하지 않아 **노출 CAM이 CAM-CA 접촉점** 제공 → σ_e 최고(3.3×10⁻²), 활성표면적 기준(1.00). 단 **2-step**(코팅 후 Super P 손혼합) 필요. VGCF는 이 성능을 **1-step**으로 달성한 점이 실용적 진전.

**핵심 통찰 3종:**
- (i) **"도전재를 넣으면 전자전도가 좋아진다"는 순진한 가정이 0D에선 깨진다** — Super P 과잉이 오히려 σ_e를 3,000배 낮춤. 형상이 양이 아니라 분포·연결성을 지배.
- (ii) **CA 차원 = 코팅 형상 변수** — 0D(매립→dense/Super-P-rich) vs 1D(전단방해→porous/embedded).
- (iii) **mixing protocol(1-step vs 2-step) + CA 선택이 device 성능의 직접 레버** — bulk 재료가 같아도(LPSCl·NCM711 동일) 결과가 갈림.

---

## 7. 우리 DFT 대비 (comp1 / modelc / Nd) → `../our_dft_baseline.md`

> ⚠ 이 논문은 **계산이 전혀 없는 순수 실험·전극공정 논문**이다. 우리 **bulk 결정 DFT(밴드/AIMD/grand-potential/elastic)와 수치 대조는 불가능**하다. 비교의 가치는 오직 **개념·landscape 수준** — "ASSB 성능의 레버가 bulk 결정이 아니라 미세구조·계면·전자전도 경로"라는 우리 결론과의 평행, 그리고 [KimICCF]와 함께 **같은 그룹의 실험 cathode-side ↔ 우리 DFT bulk/anode-side** 라는 동반 구도. **NO DFT-number comparison.**

| 항목 | 이 논문 (Kim/Y.M.Lee exp) | 우리 (DFT) | 관계 + 이유 |
|---|---|---|---|
| **SE 베이스** | **Li₆PS₅Cl** (POSCO JK, D50 1 µm) | **comp1 = Li₆PS₅Cl** | **= 동일 베이스 조성** (우리 comp1의 실험 카운터파트). modelc(Cl 1.6)는 **다룸 없음** |
| **연구 차원** | **device-level 복합양극 미세구조·전자전도 경로** (코팅 형상·CA 분포) | **bulk 단결정 결정구조·전자/이온/기계 물성** | **직교(orthogonal)** — 같은 재료(LPSCl)의 완전히 다른 스케일. 직접 수치 비교 대상 없음 |
| **성능 레버** | **코팅층 형상 + 전자전도 경로**(CA 차원·mixing) — bulk 재료 동일해도 성능 갈림 | bulk σ(inter-cage Li jump), gap, ESW, elastic | **🔑 개념 일치**: ASSB 성능은 bulk 결정만으로 안 정해짐. 우리 "lever = interphase/microstructure, not bulk lattice" 결론과 **평행** |
| **σ_e (전자전도)** | 코팅층 **σ_e가 형상으로 3,000배 변동**(3.3×10⁻²↔1.0×10⁻⁵ S/cm) — 양극측 device σ_e | 우리 σ_e 미측정 (bulk gap 2.066/2.098 eV PBE = wide-gap insulator) | **개념 평행, 수치 무관**: 우리 σ_e 논의는 SE 자체 전자절연(passivation), 이 논문 σ_e는 복합양극 도전망. **같은 단어 다른 대상** — 직접 비교 금지 |
| **활성표면적/계면** | GITT로 상대 활성표면적(1.00↔0.51 S) | 우리 계면 slab 미계산(gap H) | 우리가 못 보는 device 계면 면적을 실험이 정량 |
| **이온전도 σ_i** | 복합양극 σ_i ~0.9–1.6×10⁻⁴ S/cm (형상 영향 작음) | D(600K) 3.09e-6 cm²/s, Ea 0.253 eV (bulk AIMD) | △ **직접 비교 불가** — 복합전극 σ_i(SE+CAM+CA+공극) ≠ bulk 단결정 σ. [KimICCF] σ 논의(device≠bulk)와 같은 맥락 |
| **무질서/도핑/밴드/ESW/elastic** | 없음 | comp1/modelc, Nd, 47-도판트 cascade | **비교 대상 자체 없음** (계산 0) |

---

## 8. 적용 인사이트 (우리 연구에 어떻게) ★

1. **🔑 "ASSB 성능 레버 = 미세구조·계면·전자전도, bulk 결정 아님" — 또 하나의 실험 동반 근거 (cathode-side).** [KimICCF]가 **음극/시트 측**(공동 σ 손실 + LiF SEI)에서 이 메시지를 줬다면, 이 논문은 **양극 측**(코팅 형상·CA 차원이 σ_e 3,000배·활성표면적 2배 좌우)에서 같은 메시지를 준다. → **deck 프레이밍: "같은 그룹의 두 실험 논문(음극/시트 [KimICCF] + 양극 [KimCA])이, 우리 DFT(bulk 격자·산화창·Li 이동도)와 합쳐, 'ASSB의 진짜 레버는 결정이 아니라 interphase/microstructure'라는 결론에 양면으로 수렴"** — 매우 강한 landscape 문장.

2. **🔑 동일 SE = comp1 — 같은 그룹·같은 재료의 cathode-side 응용 맥락.** 우리 LPSCl(comp1) DFT의 **실험적 활용처**로 직접 인용 가능. "우리가 DFT로 보는 LPSCl이, 같은 그룹의 실험에서 NCM711 양극 복합체로 어떻게 쓰이고 무엇이 성능을 좌우하나"를 한 문장으로 연결. (단 modelc Cl-rich는 이 논문에 없음 → Cl-rich 일반화 금지.)

3. **[KimICCF]와 짝 — "같은 그룹의 실험 cathode-side ↔ sheet-side, 우리 DFT bulk/anode-side" 의 3각 구도.** 세 논문이 한 그룹(Yonsei Y.M.Lee + 한양대 Cho + DGIST) 안에서 **(a) bulk 격자/산화창/Li 이동도 = 우리 DFT**, **(b) 시트 σ 회복 + 음극 in-situ SEI = [KimICCF]**, **(c) 양극 복합체 전자전도·형상 = [KimCA]** 로 분업 — ASSB의 bulk·anode·cathode·sheet 전 영역을 커버한다는 프레이밍. paper/deck의 "우리 연구의 위치(landscape)" 슬라이드 한 장.

4. **"전자전도는 양(amount)이 아니라 분포·연결성"이라는 device 교훈.** Super P를 더 넣었는데 σ_e가 3,000배 떨어진 역설은, 우리 σ_e/passivation 논의("gap·도핑량만으로 σ_e가 안 정해진다; defect/carrier/percolation이 지배")와 **개념적으로 같은 결**. device 스케일에선 percolation·형상이, bulk 스케일에선 defect/carrier가 σ_e를 지배 — "σ_e는 단순 스칼라가 아니다"의 양면.

5. **우리 H-list(못 하는 것)에 "복합양극 미세구조·전자전도 경로"가 있음을 명시할 근거.** 우리 bulk DFT는 코팅 형상·CA 분포·활성표면적을 원천적으로 못 본다. 이 논문(+[KimICCF] GeoDict)은 그 영역을 **실험/digital-twin으로** 다룬다 — "우리 DFT가 못 보는 device 영역을 같은 그룹의 실험이 메운다"는 정직한 분업 서술.

> ⚠ **honest guardrail (반드시 지킬 것)**: 이 논문은 **계산이 전혀 없으므로 어떤 DFT 수치 대조도 하지 말 것.** σ_e·σ_i 절대값을 우리 값과 비교 금지(대상·스케일 다름). 비교는 **"같은 SE(comp1) + 레버가 미세구조라는 개념 정렬 + 같은 그룹 동반 논문"** 의 landscape 수준에서만. "우리 도핑이 이 양극 성능을 개선한다"는 식의 인과 혼동 절대 금지 — **독립적·상보적 영역.**

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a** | 공정 스킴: SE@CAM(2-step: planetary→hand mix Super P) / SE-SP@CAM(1-step planetary) | "mixing protocol이 형상 레버" 도식 |
| 1b | bare NCM SEM (polyhedral, 매끈) | 코팅 전 기준 형상 |
| 1c | SE@CAM SEM (둥글어짐·bumpy = dense 코팅 + 산포 Super P) | dense 코팅의 외형 |
| 1d | SE-SP@CAM SEM (LPSCl 원형 유지·산포, Super P 표면에 거의 없음=코팅층 안에 갇힘) | Super-P-rich 코팅 단서 |
| **2a–e** | SE@CAM 단면+EDS(Ni/S/C): **~50–500 nm dense 코팅, CAM 미완전피복(접촉점 white arrow), Super P 산포** | dense·thin 코팅 구조 |
| **2f–j** | SE-SP@CAM 단면+EDS: **~500 nm–2 µm porous, LPSCl+Super P 불균일, LPSCl 원형 유지** | Super-P-rich·porous 구조 |
| **3a–h** | SE@CAM vs SE-SP@CAM 복합전극 단면+EDS(Ni/S/C): C 분포 — SE@CAM 균일 / SE-SP CAM 주위 응집 | 복합전극 도전망 분포 차이 |
| **3i** | **DC polarization → σ_e: SE@CAM 3.3×10⁻² vs SE-SP@CAM 1.0×10⁻⁵ S/cm (3 orders)** | **σ_e 역설** 정량 (양 아니라 분포) |
| 3j | Nyquist(electron-blocking) | 계면저항 비교 |
| **3k** | 막대: σ_e·σ_i 비교 (σ_i 0.9 vs 1.3×10⁻⁴) | 형상이 σ_e만 크게, σ_i는 약간 |
| **4a** | 첫 충방전 0.1C: SE@CAM 185.3/81.6 % vs SE-SP@CAM 151.6/78.0 % | 성능 격차 정량 |
| 4b | GITT polarization (SE-SP 큼) | 분극 = poor structure |
| **4c** | **상대 활성표면적: SE@CAM 1.00 vs SE-SP@CAM 0.51 S (절반)** | GITT-기반 활성표면적 정량법 차용 |
| 4d | Nyquist (SE-SP 계면저항↑) | — |
| 4e | rate 0.1→2.0C (SE-SP 급강하) | rate 병목 |
| **4f** | cycling 200 cyc: SE-SP@CAM 113.0 mAh/g·70.9 %; SE@CAM 최상위 | 수명 비교 |
| **5a,b** | SE-VGCF@CAM 표면·단면 SEM (porous LPSCl + sparse rod VGCF, LPSCl 부분분쇄) | 1D CA의 다공 코팅 |
| **5c** | 막대: σ_e·σ_i 3종 — **SE-VGCF σ_e 1.4×10⁻² ≈ SE@CAM, ≫ SE-SP** | **VGCF가 σ_e 회복** 정량 |
| **5d** | 첫방전: SE-VGCF 183.5/82.7 % ≈ SE@CAM, > SE-SP | VGCF=SE@CAM 동등 |
| 5e | rate (VGCF ≈ SE@CAM) | — |
| **5f** | cycling 200 cyc: SE-VGCF 117.3 mAh/g·76.8 % ≈ SE@CAM, > SE-SP | 수명 동등 |
| **5g** | 메커니즘 스킴: SE-SP(Super P 응집·e⁻ 단절) vs SE-VGCF(VGCF 가로질러 e⁻+Li⁺ 경로) | **차원 메커니즘** 그림 (deck) |
| **SI** | **S1**(LPSCl·Super P 원료 SEM) · **S2**(ion-/electron-blocking cell 스킴) · **S3**(CAM[manual] vs SE@CAM 첫충방전·rate — SE 코팅 우위) · **S4**(GITT @SOC 50 %) · **S5**(0.1–2.0C 프로파일 SE@/SE-SP) · **S6**(rate SE@/SE-SP) · **S7**(VGCF 원료 SEM, 직경~150 nm·길이~10 µm) · **S8·S9**(SE-VGCF 단면+EDS Ni/S/C) · **S10**(SE-VGCF DC분극·Nyquist) · **S11**(SE-VGCF 0.1–2.0C 프로파일) · **S12**(rate 3종 비교) | SI는 본문 figure의 raw·VGCF 보강. **추가 수치 없음(figure-list형 캡션)** |

---

## 10. Post-processing / 측정 기법 ★

> 이 논문엔 계산 후처리(NEB/Bader/COHP/DOS/grand-potential/ELF 등)가 **없다.** 대신 **전극 미세구조·전기화학 측정 기법** 정리:

- **FE-SEM/EDS** (S-4800, Hitachi): 표면·원료 형상 + 원소 mapping(Ni/S/C). 기록 = 코팅층 두께(nm–µm)·CA 분포 정성.
- **FIB-SEM** (Helios NanoLab 600, FEI): **단면(cross-section)** 미세구조 — 코팅층 dense vs porous, CA 매립/박힘. (핵심 형상 증거 Fig 2·3·5.)
- **전자전도도 σ_e** (electron-blocking, **Ti/composite/Ti**, 200 mg @370 MPa, **DC 50 mV**): 형상별 σ_e. 기록 = S/cm (3 orders 격차).
- **이온전도도 σ_i** (ion-blocking, EIS, VSP-300 BioLogic, **14.1 mV, 5 MHz–10 mHz**): 복합전극 σ_i.
  - ⚠ σ_e 측정용 셀 구성: composite/Ti 한쪽 + **LPSCl 150 mg 양쪽 + Li foil → Li/LPSCl/composite/LPSCl/Li electron-blocking 셀** (본문 §2.3).
- **GITT** (WBCS3000Le32, WonATech; 0.5C pulse 60 s + 2 h rest): Li⁺ 확산계수 D + **상대 활성표면적 S** 계산 (Eq: D=(4/πτ)(m_NCM V_M/M_NCM S)²(ΔE_s/ΔE_t)²). 기록 = 활성표면적 a.u.(SE@CAM=1.00 기준).
- **EIS/Nyquist**: 계면저항 비교 (poor structure → 큰 반원).
- **충방전·rate·cycling** (WBCS3000Le32): pre-cycling 0.1C CC/CV, **3.0–4.3 V**, rate 0.1–2.0C, cycling 0.1C charge/0.5C discharge. 기록 = mAh/g·CE %·retention %.

> 우리 적용: **(a) GITT-기반 상대 활성표면적 정량법** = 복합양극 CAM-SE 접촉면적의 정량 지표(우리가 device 계면을 논할 때 차용). **(b) electron-/ion-blocking cell로 σ_e·σ_i 분리** = "전자전도 vs 이온전도"를 device에서 분리하는 틀(우리 bulk σ_e/σ_i 논의의 실험 대응). **(c) FIB-SEM 단면 형상** = 우리 DFT가 못 보는 코팅층 미세구조의 실측.

---

## 11. 우리가 아직 못 하는 것 / 이 논문이 메우는 것

| gap (우리) | 이 논문이 제공 | 보강 방향 |
|---|---|---|
| **복합양극 미세구조·전자전도 경로**(코팅 형상·CA 분포·활성표면적) — 우리는 bulk 단결정 DFT만 | **FIB-SEM 단면 + electron-blocking σ_e + GITT 활성표면적** (형상이 σ_e 3,000배·면적 2배 좌우) | bulk 재료 물성 ≠ device 성능의 정량 다리 (cathode-side) |
| **CA(도전재) 차원이 전극 형상에 미치는 영향** | **0D Super P(dense/Super-P-rich) vs 1D VGCF(porous/embedded)** 체계 비교 | 우리 재료(LPSCl)가 실제 양극에서 쓰일 때의 공정 변수 |
| device-level σ_e(percolation·연결성) | **electron-blocking DC + Nyquist** | 우리 bulk σ_e(defect/carrier) 논의의 device 카운터파트 |

> [KimICCF]가 **시트/펠릿 σ(GeoDict digital-twin)** 와 **음극 SEI(XPS)** 를 메웠다면, 이 논문은 **양극 복합체 형상·전자전도(FIB-SEM·σ_e·활성표면적)** 를 메운다 — 같은 그룹의 실험이 우리 bulk DFT의 device-side 공백을 양극·음극·시트 전 영역에서 채우는 구도.

---

## 12. 인용 가능 문장 (deck/paper용)

- "Our group's companion experimental work (Kim et al., Y.M. Lee lab, Battery Energy 2025) on the **cathode-composite side** shows that ASSB performance is governed by the **coating-layer morphology and electron-conduction pathway** — set by the **conductive-agent dimensionality (0D Super P vs 1D VGCF) and mixing protocol** — not by the bulk SE crystal, paralleling our DFT conclusion that the operative lever is the **interphase/microstructure, not the bulk lattice**."
- "Incorporating 0D Super P during SE coating paradoxically **dropped the composite electron conductivity by three orders of magnitude (3.3×10⁻² → 1.0×10⁻⁵ S cm⁻¹) and halved the active surface area (1.00 → 0.51)**, because the agglomerated carbon black isolates the SE coating and CAM-CA contacts — electron transport is governed by distribution/connectivity, not by the amount of conductive agent."
- "A 1D VGCF-embedded porous SE coating recovered the electron conductivity to the CA-free baseline level (1.4×10⁻² S cm⁻¹) and matched its capacity/retention (183.5 mAh g⁻¹, CE 82.7 %, 76.8 % over 200 cyc) in a simpler single-step process."
- "Together with the ICCF sheet study (Kim et al., CEJ 2026), this paper forms the **same group's experimental cathode-side and sheet/anode-side companions** to our DFT bulk/anode work, jointly placing the operative lever for ASSBs on **microstructure/interphase and electron transport** rather than the bulk crystal."
- "The SE used (Li₆PS₅Cl, POSCO JK, D50 1 µm) is the experimental counterpart of our comp1 baseline; this is a pure electrode-engineering study with **no first-principles content**, so the comparison is conceptual/landscape only — no DFT-number cross-check."

## 13. 주의 / 한계 (over-claim 방지)

- **계산 0 → DFT 수치 비교 절대 금지.** 이 논문엔 어떤 first-principles/digital-twin도 없다(σ는 모두 실측). band gap·ESW·elastic·bulk σ 등 우리 DFT 수치와의 대조는 **부적절**. 비교는 **개념(레버·미세구조)·landscape·동일SE** 수준만.
- **σ_e/σ_i 절대값 비교 금지.** 이들 = **복합양극 device σ**(SE+CAM+CA+공극의 effective). 우리 = bulk 단결정 또는 SE 자체 논의. **같은 단어(σ_e) 다른 대상.** "우리 LPSCl σ_e가 이것"이라고 매핑 금지.
- **레버 직교성.** 이 논문은 **양극 복합체 제작(코팅·CA·mixing)** 영역으로, **우리 격자 도핑과 무관**. "우리 도핑이 이 양극 성능을 개선한다"는 인과 혼동 절대 금지 — 같은 목표 영역도 아니고 독립적.
- **modelc(Cl-rich) 없음.** SE = **Li₆PS₅Cl(Cl 1.0)=comp1**만. Cl-rich 일반화·modelc 연결 금지.
- **CAM 특정.** LiNbO₃-coated NCM711(D50 7 µm) 한정. 다른 양극(NCM85/811, single-crystal 등)이면 LPSCl 변형·코팅 형상이 다를 수 있음.
- **200 cyc 수치 텍스트 겹침**: 본문이 SE-SP@CAM(113.0/70.9 %)과 SE@CAM을 한 비교 문장에서 묶음 → **SE@CAM 200 cyc 절대값은 별도로 못 박히지 않음**(추세상 최상위). 확정 수치는 SE-SP 113.0·70.9 %, SE-VGCF 117.3·76.8 %. SE@CAM 200 cyc은 "n/a(최상위 추세)"로만 인용.
- **활성표면적 SE-VGCF 수치 없음**: "다공성→활성표면적↑" 정성만; SE-SP의 0.51 S 같은 정량값은 SE-VGCF에 대해 본문에 없음.
- **rate 미세 차이**: SE-VGCF가 SE@CAM "comparable"이나 **C-rate↑서 SE@CAM보다 약간 더 떨어짐** — "완전 동등" 아닌 "거의 동등(SP보다 훨씬 우수)"으로 정확히 인용.

## 14. 기법 용어 미니사전

- **CAM (cathode active material)**: 양극활물질. 여기선 **LiNbO₃-coated NCM711** (= Li(Ni₀.₇Co₀.₁₅Mn₀.₁₅)O₂, LiNbO₃ 표면코팅으로 황화물-NCM 계면 부반응 억제).
- **SE coating on CAM (SE@CAM 등)**: 양극활물질 표면에 고체전해질을 코팅 → 활성표면적↑·입자응집↓·이온경로 연결·cycling 열화 억제. 본 논문의 대상 공정.
- **CA (conductive agent / 도전재)**: 복합전극의 전자전도 보조재. **Super P**(0D 카본블랙, 1차입자 ~40 nm) vs **VGCF**(1D 기상성장탄소섬유, 직경 ~150 nm·길이 ~10 µm).
- **dimensionality (차원)**: CA의 형상 차원. 0D(구형 입자) vs 1D(섬유). 본 논문 핵심 변수 — 코팅 중 LPSCl 변형·CA 분산을 다르게 만듦.
- **dense vs porous coating layer**: 치밀(SE@CAM, 50–500 nm) vs 다공성(SE-SP@CAM 500 nm–2 µm, SE-VGCF@CAM). 다공성=CAM 노출↑=활성표면적↑.
- **Super-P-rich layer**: Super P가 과잉·응집한 코팅층 — 전자전도↓·활성표면적↓의 원인(역설).
- **mixing protocol (혼합 프로토콜)**: 1-step(전부 동시 planetary mixing) vs 2-step(SE 코팅 후 CA 손혼합). 물질분포·형상을 크게 좌우.
- **planetary mixer (AR-100, Thinky)**: 자전·공전 혼합기. 2000 rpm 5 h로 SE 코팅 수행.
- **active surface area (활성표면적)**: CAM-SE 접촉면적(전기화학 반응이 일어나는 면적). GITT diffusion 식에서 상대값(S, a.u.)으로 산출 — SE@CAM 1.00 vs SE-SP@CAM 0.51.
- **GITT (galvanostatic intermittent titration technique)**: 전류펄스+이완으로 Li⁺ 확산계수 D 측정; 본 논문은 식을 변형해 **상대 활성표면적 S** 산출.
- **electron-blocking / ion-blocking cell**: 전자만/이온만 차단하는 셀 구성으로 σ_i / σ_e 를 각각 분리 측정. (electron-blocking = Li/LPSCl/composite/LPSCl/Li → σ_e; ion-blocking = Ti/composite/Ti EIS → σ_i.)
- **CC/CV (constant current / constant voltage)**: 충전 모드(정전류 후 정전압). 본 논문 충전 = CC/CV, 방전 = CC.
- **CE (coulombic efficiency)**: 방전/충전 용량비. 첫 사이클 CE = 비가역 용량 손실 지표.
- **VGCF (vapor-grown carbon fiber)**: 기상성장탄소섬유. 1D 고종횡비 도전재 — 본 논문서 코팅층 전자경로 형성·다공화에 유리.
