# Ion-Conducting Cavity Filler Enabling In-Situ Formation of SEI in Sulfide-Based Solid Electrolyte Sheets for All-Solid-State Batteries — Kim et al. (Chem. Eng. J. 2026)

> slug `kim2026_iccf_molten_salt_sei_lpscl_sheet` · DOI `10.1016/j.cej.2026.173036` · type `exp + 보조 DFT(HOMO/LUMO) + digital-twin 시뮬(GeoDict)` · PDF `6bc71e96-07._Ionconteries.pdf` (+ SI `0a75f53b-07._Sup_Ioeries.docx`) · digested `2026-06-25` · status ✅
> **저자**: Minjae Kim ᵃ, Yongjun Kwon ᵇ (공동 1저자), Junhyeok Seo ᵃ, Hye Jeong Dong ᵃ, Hyobin Lee ᵇᶜ, Young-Gi Lee ᵈ, **Yong Min Lee** ᵇᶜᵉ*(corr.), **Kuk Young Cho** ᵃ*(corr.)
> ᵃ **한양대 Materials Science & Chemical Eng. (Ansan)** — Kuk Young Cho · ᵇ Yonsei Chemical & Biomolecular Eng. · ᶜ DGIST Energy Science · ᵈ ETRI Materials & Components · ᵉ Yonsei Battery Eng. · Yong Min Lee
> Chem. Eng. J. **529** (2026) 173036 · Received 2 Nov 2025 / Revised 20 Dec 2025 / Accepted 14 Jan 2026 / Available 15 Jan 2026

---

## 0. 이 digest를 읽는 법 (핵심 + 우리 비교의 의미)

이 논문은 **우리 연구실 계보(한양대 Kuk Young Cho lab + Yonsei Yong Min Lee)** 의 **실험** 논문이다. DFT 격자 도핑 논문이 아니라, **sheet-type LPSCl 고체전해질(solvent-casting로 제작)의 두 가지 고질병을 "액체 충진재" 하나로 동시에 해결**하는 공정·재료 논문이다.

**두 가지 병:**
1. **이온전도도 손실** — 용매 캐스팅(slurry → 톨루엔 증발) 시 시트 내부에 **열린-다공성 cavity(공동)·crack**가 생긴다. 이 공동이 Li⁺ 전도 경로를 끊어, 시트 σ가 펠릿 σ의 일부(보통 <40 %, 본 연구 baseline 시트 1.44 mS/cm)밖에 안 된다. 가압해도 완전히 못 메운다. (시트 다공성 = **34.2 ± 0.8 %**, Table S1)
2. **음극 계면 불안정** — 황화물 SE의 좁은 전기화학 안정창 → Li 음극과 부반응 → 전자전도성·불균일 SEI → dendrite·임피던스↑·CE↓·수명↓.

**해법 = ICCF (Ion-Conducting Cavity Filler):** ATMS(ambient-temperature molten salt = 사실상 이온성 액체 IL, 녹는점 <100 ℃)를 SE에 맞게 처방한 **소량의 액체**를 완성된 시트 표면에 **방울(drop)로 적셔** 모세관으로 내부 공동에 스며들게 한다. 이 액체가 (a) 공동을 메워 **끊긴 Li⁺ 경로를 재연결**(전도도 회복) + (b) 셀 작동 중 음극에서 분해되어 **in-situ SEI를 형성**(계면 안정화)한다. 저자들은 이 ICCF가 박힌 시트를 **"functional solid electrolyte"** 라 명명한다.

> ⚠ **개념 주의 (우리와의 관계):** 이건 **bulk 결정 격자를 바꾸는 것이 아니다.** 우리 프로젝트(comp1/modelc/Nd-도핑)는 **격자 안정성·산화창·Li 이동도·SEI 산물을 DFT로** 본다. 이 논문은 **동일한 두 목표(σ 회복 + 음극 in-situ SEI)** 를 **미세구조/계면(공동을 액체로 채움 + 액체 분해로 SEI)** 로 달성한다. 즉 **레버가 "결정"이 아니라 "미세구조·계면"** 이다 — 이 점이 우리 "σ_e/passivation은 bulk가 아니라 interphase 문제" 결론과 **개념적으로 평행**(§7, §8).

> ⚠ **전압 기준:** full cell·CCD·cycling은 **Li-In(또는 Li-In/Li-In 대칭) 기준**. (Li-In ≈ Li/Li⁺ −0.62 V; 본문 cut-off 1.9–3.7 V vs Li-In ≈ 2.52–4.32 V vs Li⁺/Li). XPS·HOMO/LUMO는 절대 eV.

---

## 1. 한 줄 요약

용매 캐스팅 LPSCl 시트의 내부 공동을 **TFSI⁻ 기반 ATMS에 LiTFSI(전도/Li⁺공급)+FEC(SEI 형성)를 처방한 ICCF** 소량 방울(≈5.4 wt%, 펠릿 환산 0.2 µL drop)로 채우면, **시트 이온전도도가 1.44 → 2.23 mS/cm로 회복(회복률 155 %, 펠릿 대비 70 %)** 되고, 동시에 셀 작동 중 **음극에 LiF-rich in-situ SEI**가 형성되어 **CCD 0.8 → 1.5 mA/cm², ASSB(LNO-NCM83‖Li-In) 100 cyc @0.1C 무단락(retention 70.2 %), 200 cyc @0.2C retention 64.3 %, 100사이클 후 R_ct 13,902 → 745 Ω(약 18.6배↓)** 을 달성한다. **승리 ATMS = [EMIM][TFSI]**(이유: **TFSI⁻가 황화물 SE와 화학적으로 가장 안정** — UV-Vis/접촉각/색변화 affinity test로 검증), 최종 처방 = **[EMIM][TFSI] : LiTFSI = 90:10(=1 M LiTFSI) + 5 wt% FEC**.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| SE | **sheet-type Li₆PS₅Cl (LPSCl)** — POSCO JK Solution, **D50 = 5 ± 2 µm** |
| 시트 공정 | **solvent-casting(slurry)**: LPSCl + NBR(아크릴로니트릴-부타디엔 고무) 바인더 + 톨루엔, 무게비 **LPSCl:NBR = 97:3** → doctor-blade 캐스팅 → RT 진공 24 h. 톨루엔 증발 → **열린-다공성 cavity 형성** |
| 핵심 문제 | (1) 공동이 Li⁺ 경로 차단 → σ 손실(가압으로도 못 메움) (2) 황화물-Li 음극 부반응 → 불량 SEI → dendrite |
| 핵심 해법 | **ICCF** = ATMS(IL) 기반 처방 액체를 완성 시트에 drop으로 적셔 공동 충진 + in-situ SEI |
| ATMS 후보 5종 | **[EMIM][TFSI], [PMIM][TFSI], [BVIM][TFSI], [BMPyr][TFSI]** (TFSI 음이온·다른 양이온) / **[EMIM][BF₄], [EMIM][DCA]** (EMIM 양이온·다른 음이온) |
| 최종 ICCF | **[EMIM][TFSI] : LiTFSI = 90:10 (= 1 M LiTFSI in [EMIM][TFSI]) + 5 wt% FEC** |
| 양극 (cathode) | **LNO(LiNbO₃ 0.5 wt%)-coated NCM83** (= LiNi₀.₈₃Mn₀.₁₁Co₀.₀₆O₂) |
| 음극 (anode) | **Li metal**(50 µm) / **Li-In**(In foil 100 µm); 대칭셀은 **Li-In‖Li-In** |
| 동기/갭 | 기존 시트 σ 회복 시도(바인더 선택[13,14], ML 최적 wet-slurry[15], IL을 **slurry에 직접 혼합**[16])은 한계: IL을 <40 %까지밖에 회복 못 하거나, **slurry에 IL 직접 혼합 시 오히려 σ↓**(상분리·바인더 응집). + 인공 보호층(pre-cell)은 복잡. → **drop으로 cavity만 채우면서 동시에 SEI까지** 만드는 단순한 한방 해법이 미개척 |

> **선행 대비 핵심 차별:** 기존은 IL을 slurry에 **섞었다**(direct blending) → 톨루엔과 IL이 섞이지 않아 상분리·바인더 응집 → 큰 pore·σ↓. 본 연구는 **완성된 매끈한 시트 위에 drop**(infiltrate)으로 공동만 정밀 충진. (Fig 1c,d/1f,g가 5·10 wt% slurry-혼합의 나쁜 형상; LPSCl:NBR=97:3 매끈 시트가 Fig 1b/1e)

---

## 3. 핵심 물성 (수치 총정리)

### 3.1 이온전도도 / 전달수 / 회복률

| 샘플 | σ (RT, mS/cm) | 비고 / 출처 |
|---|---|---|
| **Reference LPSCl 시트** (baseline) | **1.44** | 공동 미충진, Fig 2e/3a |
| LPSCl_[EMIM][TFSI] (ATMS만) | **2.23** | **회복 155 %**(=1.55×baseline), Fig 2e/3a |
| LPSCl_[PMIM][TFSI] | **2.01** | Fig 2e |
| LPSCl_[EMIM][TFSI] **+ 1 M LiTFSI** | **1.95** | LiTFSI 첨가로 점도↑ → σ 약간↓, Fig 3a |
| LPSCl_1 M LiTFSI [EMIM][TFSI] **+ 5 wt% FEC** (=최종 ICCF) | **2.17** | FEC가 점도↓로 σ 회복, Fig 3a |
| (참고) **펠릿** LPSCl (375 MPa) | **3.2** | 시트 2.23 = 펠릿의 **70 %** 회복, Fig S9 |

- **회복률 155 %** = 시트 σ(2.23)/baseline 시트 σ(1.44). 펠릿 σ(3.2 mS/cm)의 **70 %** 도달 → 문헌의 기존 "<40 % 회복"(Fig 2f, Table S2 벤치마크) 상회.
- **slurry에 IL 직접 혼합 시(5·10 wt%):** σ = **1.05 / 1.12 mS/cm** → **baseline 1.44보다 낮음**(IL을 잘못 넣으면 역효과). → drop-infiltration 전략의 필요성 직접 증거.
- **Li⁺ 전달수 t⁺** (Bruce-Vincent, chronoamp+EIS): Reference LPSCl **0.97**(거의 SE만 전도) > LPSCl_1M LiTFSI+5wt%FEC **0.85** > LPSCl_1M LiTFSI [EMIM][TFSI] **0.75** > LPSCl_[EMIM][TFSI] **0.70**(Fig 3c). ATMS 넣으면 **음이온도 전도에 참여** → t⁺↓. **LiTFSI+FEC가 t⁺을 0.70→0.85로 회복**(Li⁺ 공급원·Li⁺-TFSI 배위 강화).
- **점도** (viscometer, 25 ℃): FEC **3.8** < [EMIM][TFSI] **39.1** < 1 M LiTFSI+5wt%FEC **63.0** < 1 M LiTFSI [EMIM][TFSI] **130.1** mPa·s (Fig 3b). → **FEC = co-solvent로 점도↓ → σ 회복**의 정량 근거.

### 3.2 ATMS 적합성 (cavity-wetting + 화학호환성)

| ATMS | 접촉각 (시트 위) | 색변화/UV-Vis affinity | 시트-soaked σ (Ti/SE/Ti) | PE-soaked σ | 판정 |
|---|---|---|---|---|---|
| **[EMIM][TFSI]** | **30.7°** (빠르게 wetting) | **무변화(투명 유지)** | **2.23 / [Table S3] 2.23** | 0.64 mS/cm | **✅ 승리** |
| [PMIM][TFSI] | **19.9°** (빠르게 wetting) | 무변화(투명) | 2.01 | 0.55 | ✅ (양이온만 다름, 무난) |
| [BVIM][TFSI] | n/a | 무변화 | 1.93 | 0.30 | ✅ (TFSI라 OK, Fig S6/S7) |
| [BMPyr][TFSI] | n/a | 무변화 | 1.73 | 0.27 | ✅ (TFSI라 OK) |
| **[EMIM][BF₄]** | **98.0°** (wetting 실패) | **색변화(다크 그린+노랑)** = 반응 | n/a | n/a | ❌ (BF₄⁻ 반응성) |
| **[EMIM][DCA]** | **85.1°** (wetting 실패) | **색변화(노랑+딥그린+블루)** = 강한 반응 | n/a | n/a | ❌ (DCA⁻ 최강 반응) |

- **핵심 통찰: 음이온(anion)이 황화물 호환성을 지배한다.** 같은 EMIM⁺이라도 **TFSI⁻(저극성)** = 호환/wetting OK, **BF₄⁻·DCA⁻(고극성)** = 분해/wetting 실패. **양이온(PMIM/BVIM/BMPyr)** 은 TFSI⁻이면 다 OK.
- **반응의 증거 = 색변화 + UV-Vis 폴리설파이드 피크:** SE가 부적합 ATMS와 만나면 **불안정 황종(폴리설파이드)이 녹아 나옴.** UV-Vis(LPSCl powder + ATMS 5:50 mg, 3일): **[S₂]⁻ 400 nm, [S₄]²⁻ 420 nm, [S₃]⁻ 475 nm**; BF₄: **[S₂]⁻ 400, [S₄]²⁻ 420, [S₃]⁻ 475**; DCA: 추가로 **[S₃]⁻ 617 nm**(더 강한 반응=DCA가 더 극성, NMP 같은 강극성 용매와 유사). 색: BF₄ = 다크 그린+노랑, DCA = 노랑+딥그린+블루. (Fig 2c,d)
- **극성 순서(이론·실측):** TFSI⁻ < BF₄⁻ < DCA⁻ (DFT 예측 + 실측 affinity 일치). → **저극성 anion(TFSI⁻) 선택이 황화물 시트 충진의 정량 기준**(기존엔 이런 호환성 평가 기준이 없었음).

### 3.3 전기화학 성능 (CCD / cycling / 임피던스)

| 지표 | Ref LPSCl | _[EMIM][TFSI] | _1M LiTFSI [EMIM][TFSI] | **_1M LiTFSI +5wt% FEC** | 출처 |
|---|---|---|---|---|---|
| **CCD** (Li-In 대칭, 0.1 mA/cm² step) | 0.8 mA/cm² | **0.6**(악화!) | 1.0 | **1.5 mA/cm²** | Fig 5a–d |
| **대칭셀 0.3 mAh/cm² 300 h** | overpot. **154 mV**(불안정) | — | — | **55 mV**(안정) | Fig S17 / 본문 |
| **ASSB 0.1C @50℃ 100 cyc 초기용량** | 180.2 / 180.1 mAh/g (cell 1/2, 85cyc short) | (낮음) | 약간↑ | **186.5 mAh/g** | Fig 6a |
| **ASSB 100 cyc retention** | short @85 | — | — | **70.2 %** | Fig 6a |
| **ASSB 0.2C 200 cyc retention** | — | — | — | **64.3 %** | Fig 7b |
| **100사이클 후 R_ct** (EIS fit) | — | **13,902 Ω** | **5,143 Ω** | **745 Ω** | Table S7 / Fig 6b, S18 |
| R_b / R_s1 / R_s2 (100cyc) | — | 13.1/92.3/259.0 | 15.4/75.3/237.5 | **14.2/73.2/229.7** | Table S7 |

- **CCD 역설(중요):** ATMS만(=[EMIM][TFSI]) 넣으면 CCD가 **0.8 → 0.6으로 오히려 악화** — IL에 **Li⁺ 공급원이 없어** 추가 Li가 ATMS-LPSCl 사이를 이동 → charge-transfer 임피던스↑·초기 용량 손실. **LiTFSI 추가 → 1.0**, **+FEC → 1.5**로 단계적 회복. → **"IL만으로는 안 되고, Li⁺-source(LiTFSI)+SEI-former(FEC) 처방이 필수"** 라는 본 논문의 핵심 처방 논리.
- **R_ct 18.6배 감소**(13,902→745 Ω): FEC의 LiF-rich SEI 효과. DRT(Fig S19)는 100사이클 후 R_ct 증가가 **계면 전기화학 과정의 decoupling**임을 보임.

### 3.4 다공성·열안정성·digital-twin

- **시트 다공성:** **34.2 ± 0.8 %** (10개 평균, Table S1; ρ_a = 0.97/1.6 + 0.03/0.98 환산). 시트 두께 ≈ **55–61 µm** (작동 시 60 MPa 가압).
- **ICCF 로딩량:** **≈ 5.4 wt%** (시트 총무게 기준, "well-applied drop") — 펠릿 환산 **0.2 µL drop**(다공도 기반 공동 부피 추정). → **극소량으로 전셀 성능 개선**("a minimal amount of ICCF").
- **T_d (분해온도, dynamic TGA, 5 ℃/min, 25–550 ℃):** [EMIM][TFSI]·1M LiTFSI·1M LiTFSI+5wt%FEC 모두 **onset ≈ 325 ℃** (Fig S13) → 높은 열안정성. + **IL 무게손실 0.175 %** (120 ℃ 6 h 건조; 중국 표준 T/CSAE 434-2025 기반 정량, Fig S14) → 비휘발성, ASSB 정의 충족.
- **부반응 없음:** ICCF(FEC+LiTFSI) 첨가 후 **UV-Vis·XRD 신규 피크/시프트 없음**(Fig S11, S12) → ICCF가 LPSCl과 부반응 안 함.
- **Digital-twin(GeoDict) σ 시뮬:** §4 상세. 시뮬 σ **1.96**(1M LiTFSI)·**2.10**(+FEC) mS/cm vs 실측 **1.95·2.17** → **잘 일치**. 이온 전류밀도 평균 **2624 → 3975 A/m²**(Ref → ICCF), RSD↓(더 균일).

---

## 4. DFT / 시뮬레이션 / digital-twin 방법 ★

이 논문의 "계산"은 두 갈래로, **둘 다 보조적**이다: (A) 분자 수준 **HOMO/LUMO(DFT)** 로 SEI 형성 경향 설명, (B) **digital-twin 미세구조 시뮬(GeoDict)** 로 σ 회복을 가시화·검증. **결정질 LPSCl의 band structure/AIMD/grand-potential은 없음** (우리 영역과 직접 겹치는 DFT는 아님).

### (A) HOMO/LUMO DFT — SEI 형성 경향 (Fig 3h, Table S4)
- **code:** **"Material square"** (= Materials Square, 클라우드 DFT 플랫폼; Gaussian-류 분자 계산)
- **basis / functional:** **B3LYP / 6-311++G** (분자 LUMO·HOMO 최적화). ⚠ **periodic plane-wave 아님 — 분자 cluster 계산**(IL 양이온/음이온·LiTFSI·FEC·Li⁺ 배위 complex).
- **대상 분자:** [EMIM][TFSI], Li⁺+[EMIM][TFSI], TFSI⁻, LiTFSI, FEC, Li⁺+FEC.
- **무질서 처리:** 해당 없음(분자 계산).
- **계산값 (Table S4, eV):**

  | 분자 | HOMO | LUMO |
  |---|---|---|
  | [EMIM][TFSI] | **−6.66** | **−0.89** |
  | Li⁺ + [EMIM][TFSI] | **−10.93** | **−4.14** |
  | TFSI⁻ | **−3.71** | **+4.29** |
  | LiTFSI | **−7.56** | **−1.53** |
  | FEC | **−8.25** | **+0.41** |
  | Li⁺ + FEC | **−13.47** | **−5.48** |

- **해석 (전기화학 안정성 logic):** 첨가제는 전해질보다 **HOMO가 높으면(산화 먼저, → 양극서 CEI)** 또는 **LUMO가 낮으면(환원 먼저, → 음극서 SEI)** 먼저 반응한다. **LUMO 순서: Li⁺+FEC(−5.48) < Li⁺+[EMIM][TFSI](−4.14) < LiTFSI(−1.53)** → **Li⁺-FEC complex가 LUMO 최저 = 음극에서 가장 먼저 환원 = SEI 형성 주역**. + Li⁺ 배위 시 FEC LUMO가 +0.41 → −5.48로 급강하 → "더 쉽게 환원". 순수 [EMIM][TFSI]는 LUMO 낮음 → 분해로 **고저항 유기 SEI** 우려 → LiTFSI가 [EMIM][TFSI]를 안정화(LiTFSI 결합)해 반응속도 완화.
- **결론:** 처방의 화학적 정당화 — **FEC = LiF-rich(무기) SEI former**(분해 산물 주로 LiF, low ionic/electronic conductivity지만 안정 → 표면 안정화), LiTFSI = Li⁺ source + [EMIM][TFSI] 안정화.

### (B) Digital-twin 미세구조 + σ/전류밀도 시뮬 (Fig 4, S15–S16, Table S5–S6)
- **도구:** **GeoDict 2025** — **GrainGeo**(가상 구조 생성) + **ConductoDict**(σ·이온 전류밀도).
- **가상 시트:** pristine LPSCl 입자(ρ=1.6 g/cm³)를 **D50 = 5 µm convex 다면체**로, NBR(ρ=1.0) 3 wt% 포함. **50 µm × 50 µm × 시트두께**, **voxel 0.2 µm**.
- **두 모델:** (a) LPSCl+NBR만, (b) LPSCl+NBR+**ICCF**(공동 채움). vol% 일치 검증: **Target vs Model**(Table S5) — Ref: LPSCl 88.23/88.17, NBR 4.37/4.37 · ICCF: LPSCl 76.23/76.27, NBR 3.77/3.77, IL **20.00/19.96** vol%.
- **σ 계산:** ConductoDict, **두께 방향 1 V**. **입자-입자 contact resistivity**와 **LPSCl/ATMS biphasic ion-transport resistivity**를 포함.
- **Contact resistivity 보정:** 4개 다공도(28.2/17.7/10.3/7.4 %) 시트의 실측 σ에 맞춰 **R_cont = 0.06–0.09 Ω·cm²**를 스캔, **RMSE 최소 = R_cont = 0.07 Ω·cm²**(RMSE 0.15) 채택 (Eq 3, Table S6).
- **Biphasic(LPSCl/ATMS) ion-transport resistivity:** **0.08 Ω·cm²** 로 피팅 — **기존 유기용매-황화물 계면(보통 >10 Ω·cm²)보다 훨씬 낮음.** 이유: TFSI⁻의 **낮은 donor number** → desolvation 활성화에너지↓ + 화학호환성(UV-Vis 검증) → 계면 저항 작음.
- **결과 (Fig 4):**
  - 시뮬 σ **1.96**(1M LiTFSI) / **2.10**(+FEC) mS/cm vs 실측 **1.95 / 2.17** → **정량 일치** → digital-twin 모델 타당성 검증.
  - **이온 전류밀도** (midplane x–y, z 스캔 평균): Ref LPSCl **2624 A/m²** → ICCF(+FEC) **3975 A/m²** (더 높음). **RSD↓**(Eq 4, =std/mean) → ICCF가 **전류 분포를 더 균일하게**(공동 채워 dead-zone 제거).
  - 3D 가시화(Fig 4a,b): 7.4 % 다공도 Ref vs 20 % IL 채운 시트 — IL(하늘색)이 공동 채움.

---

## 5. 결과 — 섹션별 상세 (전 figure·전 수치)

### 5.1 LPSCl 시트 + ICCF 제작 (Fig 1, §3.1)
- **다공성 = 34.2 ± 0.8 %**(Table S1) — 황화물 시트 일반 범위(~40 %) 내. 공동이 σ 손실 + 기계 불안정(crack·변형) 동시 유발.
- **ICCF 정의:** 비휘발·열안정·난연(flame-retardant) 액체로 공동을 채움 → Li⁺ 전도망 연속 확장.
- **ATMS 자체 = IL**(녹는점 <100 ℃, 정전기력으로 액체): 비휘발·무시할 증기압·고전도·난연 → 액체 전해질로 매력적.
- **slurry 직접혼합 실패(중요):** ATMS는 톨루엔과 **불혼화(immiscible)·불용** → slurry에 넣으면 **상분리 → 큰 pore·바인더 응집**(Fig S1). 5·10 wt% 직접혼합 시트 σ = **1.05·1.12 < baseline 1.44**(Fig 1c,d 외형 나쁨, 1f,g SEM 거침). vs **LPSCl:NBR 97:3** 시트 = 매끈(Fig 1b 외형, 1e SEM).
- **해법 = drop infiltration:** 완성 매끈 시트 위에 ICCF 0.2 µL drop → 모세관으로 공동 채움. cross-section SEM(Fig S4): ATMS 영역이 더 어두운 contrast = 공동에 완전 침투.
- **Fig 1a 스킴:** "Optimized LPSCl sheet(공동·crack로 Li⁺ 경로 끊김, 빨간 X)" → ICCF → "Functional solid electrolyte(빨간 ICCF가 공동 채워 Li⁺ 경로 연결)".

### 5.2 ATMS-LPSCl 호환성 기준 (Fig 2, §3.2) — **승리 ATMS 선정의 핵심**
- **wetting(접촉각, Fig 2b/S3):** [EMIM][TFSI] **30.7°**, [PMIM][TFSI] **19.9°** → 빠르게 적심. [EMIM][BF₄] **98.0°**, [EMIM][DCA] **85.1°** → 시간 지나도 안 적심. **음이온이 wetting 지배.**
- **화학호환성(색·UV-Vis, Fig 2c,d):** §3.2 표 참조. TFSI⁻ = 투명 유지(무반응), BF₄⁻·DCA⁻ = 색변화(폴리설파이드 leach). **TFSI⁻ 검증 보강:** [BVIM][TFSI]·[BMPyr][TFSI]도 wetting OK·투명 유지(Fig S6,S7) → "TFSI⁻ 시스템의 우월한 안정성 확인".
- **고극성 anion = 고반응성**: DCA⁻가 BF₄⁻보다 강한 폴리설파이드 생성(617 nm 추가) = NMP 같은 강극성 용매처럼 작용. **이론(DFT 극성) 예측과 실측 일치.**
- **σ 회복(Fig 2e):** [EMIM][TFSI] **2.23**(155 %)·[PMIM][TFSI] **2.01** > Ref **1.44**. **펠릿 σ(3.2)의 70 %** 도달(Fig 2f/S9) → 문헌 "<40 % 회복"(Table S2 21건 벤치마크) 상회.
- **추가 검증:** PE separator·LPSCl 시트에 TFSI⁻ ATMS 적신 σ(Table S3): ATMS σ가 높을수록 soaked 시트 σ도 높음(상관). → ATMS 자체 전도가 시트 σ 기여 확인.

### 5.3 ICCF 처방 (Fig 3, §3.3) — LiTFSI + FEC
- **σ vs 점도 trade-off(Fig 3a,b):** ATMS만 2.23 → +1M LiTFSI 1.95(점도 39.1→130.1로 σ↓) → +5wt%FEC 2.17(FEC 점도 3.8로 co-solvent 작용 → σ 회복). → **FEC는 σ 살리면서 SEI까지.**
- **t⁺(Fig 3c):** Ref 0.97 → ATMS만 0.70(음이온 전도) → +LiTFSI 0.75 → +FEC **0.85**(Li⁺ source·배위로 회복).
- **HOMO/LUMO(Fig 3h):** §4(A). Li⁺-FEC LUMO 최저(−5.48) = 음극 SEI 주역. Li⁺ coordinating → "More reduction"(음극)/ "More oxidation"(양극) 방향 도식.
- **SEI 스킴(Fig 3i):** Ref = "Non-uniform & cracking SEI" + inhomogeneous Li⁺ flux + dendrite. ICCF([EMIM][TFSI]+LiTFSI+FEC) = "Uniform & stable SEI" + uniform Li⁺ flux. (= 본 논문 메커니즘 그림)

### 5.4 Digital-twin (Fig 4, §3.4) — §4(B) 상세. 시뮬 σ 1.96/2.10 ≈ 실측 1.95/2.17; 전류밀도 2624→3975 A/m², RSD↓(균일).

### 5.5 음극/전해질 계면 — CCD + XPS SEI (Fig 5, §3.5) — **in-situ SEI 메커니즘 핵심**
- **CCD(Fig 5a–d):** Ref 0.8 → [EMIM][TFSI] **0.6(악화)** → +LiTFSI 1.0 → **+FEC 1.5 mA/cm²**. (역설: IL만은 Li⁺ source 없어 악화 → LiTFSI·FEC 필수.)
- **대칭셀 300 h(Fig S17):** Ref overpotential **154 mV**(불안정, 공동 = 불균일 flux) vs +FEC **55 mV**(안정).
- **XPS S 2p(Fig 5e–h, Li-In 음극면, formation cycle 후):**
  - Ref LPSCl: **P–S–P 161.7·162.9 eV**(LPSCl 분해 유래) + **Li₂S 160.5·161.7 eV** → Li₂S 생성(SE 분해).
  - [EMIM][TFSI]·1M LiTFSI: 모두 Li₂S 피크 존재.
  - **+5wt%FEC: Li₂S 피크 감소**(Fig 5h) → **FEC가 Li₂S(SE 분해 산물) 생성을 유의하게 억제.**
- **XPS F 1s(Fig 5i–l):**
  - Ref LPSCl: **신호 없음**(F 없음).
  - [EMIM][TFSI]·1M LiTFSI·+FEC: **CF₃ 688 eV**(TFSI⁻ 유래) + **LiF 684 eV**.
  - **+5wt%FEC: LiF 피크 강도 증가** → **FEC가 음극에 LiF-rich SEI 형성**(LiF = TFSI⁻·LiTFSI 분해 + FEC 분해 모두에서).
- **메커니즘 결론:** FEC가 음극에 **LiF-rich(저표면에너지·저확산속도) SEI** 형성 → **균일 Li 증착 촉진 + SE 분해(Li₂S) 억제** → dendrite·부반응 억제. **실험 계면 분석이 §3.3 DFT HOMO/LUMO 예측을 뒷받침**(저자 명시).

### 5.6 ASSB 셀 성능 (Fig 6, 7, §3.6)
- **0.1C @50℃ 100 cyc(Fig 6a):** Ref LPSCl cell 1·2 초기 **180.2·180.1 mAh/g** → **85사이클서 short-circuit**. [EMIM][TFSI]·1M LiTFSI = 100사이클 무단락이나 용량 낮음(IL만은 초기 charge-transfer 임피던스↑로 용량 손실, LiTFSI가 개선). **+FEC = 186.5 mAh/g, retention 70.2 %.**
- **EIS 100cyc 후(Fig 6b, Table S7):** R_ct **13,902(EMIM/TFSI) → 5,143(+LiTFSI) → 745 Ω(+FEC)**. R_b·R_s1·R_s2도 +FEC서 최소. DRT(Fig S19): R_ct 증가 = 계면 과정 decoupling.
- **Post-mortem SEM(Fig 6c,d / S20):** Ref·[EMIM][TFSI]·1M LiTFSI 음극·양극 = **거칠고 불균일(심한 부반응·잔류 부산물)**. **+FEC = porous·균일 형상**(안정 SEI가 균일 stripping/plating). 양극 계면도 +FEC가 안정.
- **0.2C @50℃ 200 cyc(Fig 7b):** +FEC **retention 64.3 %**, 무단락. (Fig 7a 스킴: Ref = unstable SEI+dendrite vs functional SE = high σ + robust SEI.)

---

## 6. 메커니즘 종합 (이중 기능: σ 회복 + in-situ SEI)

**기능 1 — 이온전도도 회복 (미세구조):**
용매 캐스팅 공동(34.2 %)이 Li⁺ 경로를 끊음 → ICCF drop(≈5.4 wt%)이 공동 채워 **연속 Li⁺ 망 복원** → σ 1.44 → 2.23 mS/cm(155 %, 펠릿 70 %). digital-twin이 σ·전류밀도 균일화 검증(2624→3975 A/m²). **핵심: bulk 결정이 아니라 "공동(미세구조)" 이 σ 손실 원인 → 미세구조를 메우는 것이 레버.**

**기능 2 — in-situ SEI (계면 화학):**
셀 작동 중 음극에서 **Li⁺-FEC complex(LUMO −5.48, 최저)가 먼저 환원** → **LiF-rich SEI**(+ TFSI⁻/LiTFSI 분해 LiF) 형성. 이 SEI가 (a) **SE 분해(Li₂S) 억제**(XPS), (b) **균일 Li flux**(overpot 154→55 mV), (c) **dendrite/부반응 억제**(SEM 균일) → CCD 0.8→1.5, R_ct 18.6×↓, cycling 안정. **핵심: 황화물의 나쁜 native SEI(전자전도 Li₂S/Li₃P)를 LiF-rich(전자절연 성향)로 교체** — 이는 우리 "전자절연 interphase = self-limiting passivation" 논리와 **같은 목표**(§7).

**처방의 3요소 분업:** [EMIM][TFSI](TFSI⁻ = 황화물 호환·wetting·공동충진) + LiTFSI(Li⁺ source·t⁺ 회복·IL 안정화·CCD 회복) + FEC(점도↓로 σ 회복 + LiF-rich SEI former). **하나라도 빠지면**(ATMS만) CCD·용량 악화 → 셋 다 필요.

---

## 7. 우리 DFT 대비 (comp1 / modelc / Nd) → `../our_dft_baseline.md`

> ⚠ 이 논문은 **실험·공정 논문**(분자 HOMO/LUMO + GeoDict 보조)이라 우리 **bulk 결정 DFT(밴드/AIMD/grand-potential)와 직접 수치 대조는 제한적**이다. 비교의 진짜 가치는 **"같은 목표(σ 회복 + 음극 in-situ SEI)에 대한 다른 레버(미세구조·계면 vs 격자)"** 의 개념 정렬, 그리고 **"σ_e/passivation은 bulk가 아니라 interphase 문제"** 라는 우리 결론과의 평행이다.

| 항목 | 이 논문 (Kim/Cho exp) | 우리 (DFT) | 일치/차이 + 이유 |
|---|---|---|---|
| **SE 베이스** | **Li₆PS₅Cl** (D50 5 µm) | **comp1 = Li₆PS₅Cl** | **= 동일 베이스 조성** (우리 comp1의 실험 카운터파트) |
| **σ 절대값** | 시트 1.44→2.23, 펠릿 3.2 mS/cm (RT 실측) | D(600K) 3.09e-6 cm²/s, Ea 0.253 eV (AIMD, RT 외삽) | △ **직접 비교 불가** — 우리는 bulk 단결정 AIMD(미세구조 無), 이들은 시트/펠릿 실측(공동 지배). **둘 다 "bulk 잠재력 ≫ 실현 σ"** 를 보임(우리 외삽 high vs 시트 1.44) → **미세구조가 병목**임을 양쪽이 시사 |
| **σ 손실의 원인** | **공동(34.2 %) = 미세구조** (가압으로 못 메움) | bulk σ는 inter-cage Li jump(Cl 4c 무질서) | **개념 일치: σ는 bulk 결정만으로 안 정해짐.** 우리 "σ_e는 interphase, σ_Li는 microstructure/percolation 변수" 결론과 **평행** |
| **음극 in-situ SEI 산물** | **LiF-rich**(+Li₂S 억제) — XPS F1s 684 eV | comp1/modelc 0 V grand-potential → **Li₃P + Li₂S + LiCl** | **목표 일치/산물 다름:** 우리 native 환원산물은 Li₂S/Li₃P(전자전도 우려)+LiCl(절연). 이들은 그 native SEI를 **외부 LiF로 덮어** 개선. → **둘 다 "전자절연 passivation으로 self-limiting"** 가 목표. LiF·LiCl·Li₂O 모두 wide-gap 절연 interphase 패밀리 |
| **electron-blocking interphase 논리** | LiF-rich SEI로 SE 분해(Li₂S) 억제 (XPS) | NdPO₄/Li₂O/Li₃PO₄ 등 wide-gap "electron-blocking interphase"가 우리 중심 메커니즘 | **개념 직결:** 우리 "전자절연 interphase가 분해 차단" = 이들의 "LiF-rich SEI가 SE 분해 억제". **우리 DFT가 '어떤 산물이 절연인가'(Li₂O/Li₃PO₄/NdPO₄/LiCl), 이들이 '어떤 액체 처방이 그 절연 SEI를 in-situ로 만드나'(FEC→LiF)** → 상보적 |
| **SEI 형성 경향 계산** | 분자 **HOMO/LUMO(B3LYP/6-311++G)** — LUMO 최저=먼저 환원 | 우리 grand-potential ESW(주기적 결정, get_element_profile) | **방법 상이:** 그들=분자 cluster frontier orbital(첨가제 우선 분해 판정), 우리=고체 chemical-potential decomposition(어떤 고체상으로 분해). 둘 다 "무엇이 먼저/무엇으로 분해"를 다른 각도로 |
| **산화/CEI** | 양극 안정화는 부수(주로 음극 SEI) | 우리 B③ cathode 계면(Zuo Eq1/Eq2) | 약한 연결 — 이 논문은 음극 중심 |
| **무질서/도핑** | 없음(액체 충진) | comp1/modelc(Cl 무질서), Nd 도핑, 47-도판트 cascade | **직교 전략:** 격자 도핑(우리) ⟂ 액체 cavity-filler(이들). 같은 목표·다른 레버 |
| **band gap / 전자구조** | 없음(분자 HOMO/LUMO만) | comp1 2.066 / modelc 2.099 eV (PBE) | 비교 대상 없음 |

---

## 8. 적용 인사이트 (우리 연구에 어떻게) ★

1. **🔑 "σ_e/passivation은 bulk 결정이 아니라 interphase·microstructure 문제" — 실험적 동반 근거.** 우리 cascade에서 막 찾은 **"σ_e는 interphase이지 bulk가 아니다"** 와, 이 논문의 **"σ 손실은 공동(미세구조)이고, SEI는 계면 화학"** 은 **같은 메시지의 양 날개**다. deck에서 "우리 DFT(격자) + 같은 그룹 실험(미세구조/계면) = 레버가 결정이 아니라 interphase라는 결론에 수렴"으로 묶을 수 있다 — **매우 강한 프레이밍**.

2. **🔑 "electron-blocking interphase" 메커니즘의 실험 평행.** 우리 중심 주장(NdPO₄/Li₂O/Li₃PO₄ 등 **wide-gap 전자절연 interphase가 분해 차단**)을, 이 논문은 **LiF-rich SEI가 SE 분해(Li₂S)를 억제**(XPS F1s/S2p)하는 것으로 실험 입증한다. → **"우리 DFT가 예측하는 절연 SEI 산물(LiF/LiCl/Li₂O/Li₃PO₄)의 in-situ 형성을, 같은 그룹이 액체 처방으로 실현"** 는 paper companion 문장 가능.

3. **🔑 우리 그룹(한양대 Kuk Young Cho + Yonsei Yong Min Lee) 논문 → 직접 citable companion.** 우리 LPSCl DFT의 **실험 맥락/응용** 으로 인용 적합. "lattice route(우리 DFT 도핑) ↔ interphase route(이 논문 ICCF)" 를 한 그룹의 상보 전략으로 제시 가능.

4. **LiCl/LiF 절연 interphase 패밀리 일관성.** modelc(Cl-rich)가 음극서 **LiCl**(전자절연 gap 6.22, [Lu]) 생성 ↔ 이 논문 FEC가 **LiF**(전자절연) 생성 ↔ [Liu23] MgF₂의 LiF ↔ [Ke] Li₂O. **"음극 passivation의 정답 = wide-gap 절연 interphase(LiF/LiCl/Li₂O 계열)"** 라는 우리 comparison §E·§G 결론에 **TFSI/FEC 액체 처방 경로**를 한 줄 추가.

5. **"우리 DFT가 못 보는 것(미세구조 σ)을 누가 메우나" 의 모범 답.** 우리 H-list(못 하는 것)에 **시트/펠릿 microstructure σ(공동·percolation)** 가 있다 — 이 논문의 **GeoDict digital-twin(GrainGeo+ConductoDict, contact 0.07 + biphasic 0.08 Ω·cm²)** 이 그 틀. 우리가 bulk AIMD σ만 보는 한계를 인정할 때 인용할 정량 방법.

6. **TFSI⁻ 호환성 기준 = 황화물-액체 계면 설계 원칙.** "저-donor-number·저극성 anion(TFSI⁻) = 황화물과 호환(폴리설파이드 leach 안 함, biphasic 0.08 Ω·cm²)" 는, 우리가 향후 **하이브리드(고체+액체 함침) 또는 계면 chempot 모델**을 할 때 anion 선택 기준으로 차용.

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a | 스킴: 공동(Li⁺ 끊김) → ICCF → functional SE(경로 연결) | "미세구조가 σ 레버" 도식 |
| 1b–g | 매끈 시트(97:3) vs 5·10wt% slurry-혼합 나쁜 형상(외형+SEM) | IL을 잘못 넣으면 역효과 = drop 전략 정당화 |
| 2a | ATMS 양이온/음이온 분자구조(PMIM/EMIM/TFSI/BF₄/DCA) | — |
| 2b,c | wetting(접촉각) + 색변화 affinity(TFSI 투명/BF₄·DCA 색변화) | **anion이 황화물 호환성 지배** 증거 |
| 2d | UV-Vis 폴리설파이드 피크([S₂]400/[S₄]420/[S₃]475·617) | 황화물-액체 부반응 정량(폴리설파이드 leach) |
| 2e,f | σ 회복 막대 + 문헌 회복률 벤치마크(155 %·70 %) | **σ 회복 정량**, Table S2 21건 대비 |
| 3a,b | σ vs 점도(LiTFSI↑점도→σ↓, FEC co-solvent→σ회복) | 처방 trade-off 정량 |
| 3c | t⁺(0.97→0.70→0.85) | ATMS가 음이온 전도 추가, FEC 회복 |
| 3d–g | chronoamp + EIS(전후) | t⁺ 측정 raw |
| **3h** | **HOMO/LUMO 도식**(Li⁺-FEC LUMO −5.48 최저) | **SEI 형성 경향 DFT logic**(우리 ESW와 다른 각도) |
| 3i | SEI 스킴(Ref crack/dendrite vs ICCF uniform) | 메커니즘 그림 |
| 4a,b | 3D digital-twin(공동→IL 채움) | 미세구조 σ 가시화 방법 |
| 4c | 시뮬 σ ≈ 실측(1.96/2.10 vs 1.95/2.17) | digital-twin 검증 |
| 4d–f | 이온 전류밀도 3D/2D + 평균(2624→3975 A/m²) | σ 균일화 정량(RSD↓) |
| 5a–d | CCD(0.8→0.6→1.0→**1.5**) | 처방 단계별 계면 안정성 |
| **5e–h** | **XPS S2p**(Li₂S, +FEC서 Li₂S↓) | **SE 분해 억제** 직접 증거 |
| **5i–l** | **XPS F1s**(CF₃ 688·**LiF 684**, +FEC서 LiF↑) | **LiF-rich SEI** = 전자절연 passivation 실험 입증 |
| 6a | ASSB 100cyc(Ref 85서 short, +FEC 70.2 %) | 성능 우위 |
| 6b | EIS 100cyc 후(R_ct 745 최소) | 계면 안정 정량 |
| 6c,d | post-mortem SEM(음극·양극) | +FEC 균일 형상 |
| 7a,b | 스킴 + 200cyc 0.2C(retention 64.3 %) | 장수명 |
| **SI** | S1(슬러리 형성 메커니즘) · S2/S8/S9/S10(Nyquist·σ) · S3(접촉각 시간) · S4(cross-SEM 침투) · S5–S7(TFSI wetting/색) · S11–S12(UV-Vis/XRD 부반응無) · S13(TGA T_d 325℃) · S14(IL 손실 0.175 %) · S15–S16(digital-twin 다공도) · S17(대칭 300h 154→55mV) · S18/S19(EIS fit·DRT) · S20(계면 SEM) · **Table S1**(다공 34.2 %) · **S2**(회복률 21건) · **S3**(ATMS σ) · **S4**(HOMO/LUMO) · **S5**(vol%) · **S6**(RMSE·R_cont 0.07) · **S7**(R_ct fit) | 각 SI = 위 본문 수치의 raw 근거 |

---

## 10. Post-processing ★

- **σ 측정:** Ti/SE/Ti blocking 대칭셀, 1 Hz–3 MHz(시트) / 1 MHz–10 mHz(셀), Eq 1 σ = L/(R_b·A). 기록 = mS/cm, 회복률 %.
- **t⁺(전달수):** chronoamperometry(ΔV 10 mV) + EIS, Eq 2(Bruce-Vincent: t⁺=I_ss(ΔV−I₀R₀)/[I₀(ΔV−I_ss R_ss)]). Li/SE/Li.
- **CCD:** Li-In‖Li-In, plating/stripping 0.1 mA/cm² step 증가 → short 직전 전류밀도.
- **EIS → 등가회로 fit(Fig S18, Table S7):** R_b·R_s1·R_s2·R_ct 분해. **DRT(Fig S19)** 로 계면 과정 시간상수 분리(decoupling).
- **XPS:** K-Alpha+, Li-In 음극면(formation cycle 후), air-tight transfer. S2p(P-S-P 161.7/162.9, Li₂S 160.5/161.7) · F1s(CF₃ 688, LiF 684). 기록 = 종 동정·상대강도.
- **UV-Vis affinity(Mega-800):** LPSCl powder + ATMS 분산 후 여과·큐벳, 350–700 nm. 폴리설파이드 피크([S₂]400/[S₄]420/[S₃]475·617) = 부반응 정량. **(황화물-액체 호환성 스크리닝 기법 — 차용 가치)**
- **접촉각:** dry room(dew point <−60 ℃), 1 µL drop. 점도 = viscometer 25 ℃. T_d = dynamic TGA 5 ℃/min.
- **Digital-twin:** GeoDict GrainGeo(구조) + ConductoDict(σ·전류밀도). contact resistivity RMSE 최소화(Eq 3) = 0.07 Ω·cm², biphasic 0.08 Ω·cm². RSD = std/mean(Eq 4, 균일도).
- **HOMO/LUMO:** Materials Square, B3LYP/6-311++G, 분자 frontier orbital → 산화/환원 우선순위.
- **XRD:** Rigaku D/MAX-2500, 20–70° 2θ, air-tight holder. → ICCF 부반응 無 검증(Fig S11c, S12).

> 우리 적용: **(a) UV-Vis 폴리설파이드 정량 = 황화물-액체/계면 부반응 스크리닝 틀**, **(b) GeoDict digital-twin = 우리 bulk AIMD가 못 보는 microstructure σ(공동·percolation)의 정량 보강**, **(c) XPS F1s/S2p로 "LiF-rich 절연 SEI vs SE 분해(Li₂S)" 분리 = 우리 DFT 절연-interphase 예측의 실험 검증 틀**.

---

## 11. 우리가 아직 못 하는 것 / 이 논문이 메우는 것

| gap (우리) | 이 논문이 제공 | 보강 방향 |
|---|---|---|
| 시트/펠릿 microstructure σ(공동·percolation) — 우리는 bulk 단결정 AIMD만 | **GeoDict digital-twin**(GrainGeo+ConductoDict, contact 0.07 + biphasic 0.08 Ω·cm²) | bulk σ ≠ device σ의 정량 다리 |
| 음극 in-situ SEI의 *실측* 산물·전자절연성 | **XPS LiF-rich SEI + Li₂S 억제** | 우리 grand-potential 환원산물(Li₂S/Li₃P/LiCl) 예측의 실험 카운터파트 |
| 첨가제(액체) 우선분해 판정 | **분자 HOMO/LUMO(LUMO 최저=먼저 환원)** | 우리 고체 grand-potential과 다른 각도(첨가제 chemistry) |
| 황화물-액체 계면 호환성 기준 | **anion 극성/donor number(TFSI⁻=호환) + UV-Vis affinity** | 향후 하이브리드/계면 chempot 모델 anion 선택 |

---

## 12. 인용 가능 문장 (deck/paper용)

- "Our group's own experimental work (Kim et al., Cho/Lee labs, CEJ 2026) shows that the conductivity loss in solvent-cast Li₆PS₅Cl sheets is governed by **interior cavities (34.2 % porosity), not the bulk crystal** — recovered to 155 % (70 % of pellet) by a minimal ICCF drop — paralleling our DFT conclusion that the operative lever for σ_e/passivation is the **interphase/microstructure, not the bulk lattice**."
- "The ICCF forms a **LiF-rich in-situ SEI** that suppresses Li₂S formation (XPS S2p/F1s), the **experimental analogue of our DFT 'electron-blocking interphase' mechanism** (wide-gap Li₂O/Li₃PO₄/NdPO₄/LiCl) — both routes converge on a wide-gap, electronically insulating passivation layer."
- "TFSI⁻'s low donor number/polarity makes it chemically compatible with sulfide SE (no polysulfide leaching by UV-Vis; biphasic interfacial resistivity 0.08 Ω·cm², far below the >10 Ω·cm² of typical organic solvents)."
- "A digital-twin (GeoDict GrainGeo+ConductoDict) reproduces the measured sheet conductivity (sim 1.96/2.10 vs exp 1.95/2.17 mS/cm) and shows the cavity filler raises and homogenizes the ionic current density (2624 → 3975 A/m²)."

## 13. 주의 / 한계 (over-claim 방지)

- **DFT 직접 비교 금지:** 이들의 "DFT"는 **분자 HOMO/LUMO(B3LYP/6-311++G)** — 우리 **주기적 결정 PBE 밴드/AIMD/grand-potential과 종류가 다름.** band gap·ESW·elastic 수치 대조는 부적절. 비교는 **개념(목표·레버)** 수준에서만.
- **σ 절대값 비교 금지:** 그들 = 시트/펠릿 실측(미세구조 지배), 우리 = bulk 단결정 AIMD RT-외삽. "둘 다 미세구조가 병목" 정도의 **개념 정렬만** 정당.
- **"전자절연 SEI" 주장의 한계:** LiF는 절연(전자/이온 모두 낮음)이라 본문도 "low ionic/electronic conductivity"라 명시 — **σ_e를 직접 측정하지 않음**(우리 [Liu23]의 DC분극 σ_e 같은 값 없음). "electron-blocking"은 **간접 추론**(Li₂S 억제 + 안정 cycling)이지 σ_e 실측 아님.
- **레버 직교성:** 이 논문은 **격자 도핑(우리)과 무관한 액체 충진** 경로. "우리 도핑이 이걸 한다"는 식의 인과 혼동 금지 — **같은 목표·독립 수단.**
- **모델 단순화:** digital-twin은 pristine LPSCl 입자 가정(crack·바인더 비균일 단순화). contact/biphasic resistivity는 **실측 fit 파라미터**(first-principles 아님).
- **전압 기준:** CCD·cycling = Li-In 기준(Li⁺/Li −0.62 V). HOMO/LUMO = 절대 eV(분자, vs SHE/Li 환산 안 됨).
- **Cl-rich(modelc) 비교 시 주의:** 이 논문 SE = **Li₆PS₅Cl(Cl 1.0)** = 우리 **comp1**. **modelc(Cl 1.6)는 다룸 없음** — Cl-rich 일반화 금지.

## 14. 기법 용어 미니사전

- **ATMS (ambient-temperature molten salt):** 상온서 액체인 용융염 = 사실상 **이온성 액체(IL)**. 녹는점 <100 ℃, 비휘발·난연·고전도. 본 논문 cation: PMIM⁺(propyl-methylimidazolium)·EMIM⁺(ethyl-methylimidazolium)·BVIM⁺(butyl-vinylimidazolium)·BMPyr⁺(methyl-pyrrolidinium)·BMIM⁺. anion: TFSI⁻(bis(trifluoromethanesulfonyl)imide)·BF₄⁻·DCA⁻(dicyanamide).
- **ICCF (ion-conducting cavity filler):** ATMS에 LiTFSI(Li⁺ source)+FEC(SEI former)를 처방한, 시트 공동 충진용 액체. 본 논문 신조어.
- **FEC (fluoroethylene carbonate):** LiB의 대표 SEI-forming 첨가제, 분해 시 **LiF-rich 무기 SEI** 형성. 본 논문은 SE에 처음 적용.
- **functional solid electrolyte:** ICCF 함침 시트 — "고체 + 소량 액체" 의 기능성 복합. 액체전해질 셀과 구분되는 본 논문 개념.
- **donor number:** 용매/액체의 Lewis 염기성(전자쌍 주는 능력). 낮으면 desolvation 활성화E↓·황화물과 부반응↓ → TFSI⁻이 낮아 호환.
- **HOMO/LUMO:** 분자 최고점유/최저비점유 궤도. **LUMO 낮음 = 환원 쉬움(음극서 먼저 분해 → SEI)**, HOMO 높음 = 산화 쉬움(양극서 CEI).
- **digital twin:** 실제 시트 미세구조를 모사한 가상 3D 모델(GeoDict). 입자 다면체+공동+바인더로 σ·전류밀도 시뮬.
- **GrainGeo / ConductoDict:** GeoDict 모듈 — 구조 생성 / 전도(σ·전류밀도) 해석.
- **biphasic ion-transport resistivity:** LPSCl(고체)과 ATMS(액체) 두 상 사이 Li⁺ 이동 계면 저항(본 논문 fit 0.08 Ω·cm²).
- **RSD (relative standard deviation):** std/mean — 전류밀도 분포 균일도(낮을수록 균일).
- **DRT (distribution of relaxation times):** EIS를 시간상수별로 분해 → 계면 전기화학 과정 구분.
- **CCD (critical current density):** short 직전 임계 전류밀도 — 음극/SE 계면 안정성 지표.
- **t⁺ (transference number):** 전체 전도 중 Li⁺ 기여 분율. 1에 가까울수록 SE만 전도(음이온 정지).
