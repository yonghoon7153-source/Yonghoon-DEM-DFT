# Koo 2025 (Energy Storage Materials 78, 104270) — anti-solvent로 MWCNT 감싼 단결정 SC-NCA dry 양극 (99.6 wt%, 4.0 g/cm³) ★ #275(Joule 2026)의 2025 PRECURSOR / SISTER 논문

> slug `koo2025_cnt_wrapped_sc_nca_dry_cathode` · DOI `10.1016/j.ensm.2025.104270` · type `FEM·digital-twin` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Jin Kyo Koo†, Jaejin Lim†, Jeongmin Shin, Jae Kwon Seo, Chaeyeon Ha, Weerawat To A Ran,
Jung-Hun Lee, Yewon Kwon, **Yong Min Lee\***, Young-Jun Kim\*, "Dry-processed ultra-high-energy
cathodes (99.6wt%, 4.0 g cm⁻³) using single-crystalline Ni-rich oxides", *Energy Storage Materials*
**78** (2025) 104270, DOI 10.1016/j.ensm.2025.104270. 접수 2025-01-21 / 게재확정 2025-04-18 /
online 2025-04-19, © 2025 Elsevier. †Jin Kyo Koo, Jaejin Lim 동등기여. 교신 Y.M.L./Y.-J.K.

**소속:** (a) SKKU Advanced Institute of Nano Technology (SAINT), (b) Dept. of Nano Science &
Technology, Sungkyunkwan Univ.(Suwon) + (c) Dept. of Nano Engineering, SKKU + (d) SKKU Institute of
Energy Science & Technology (SIEST) + (e) Dept. of Chemical & Biomolecular Engineering, **Yonsei
University**(Seoul 03722, = 이용민 **Digital Twin Battery Lab, DTBL**) + (f) Dept. of Energy Science
& Engineering, **DGIST**. 교신 yongmin@yonsei.ac.kr (Y.M. Lee) / yjkim68@skku.edu (Y.-J. Kim).

★★ **이 논문 = #275(Koo, Joule 2026 "continuous SWCNT sheath")의 직계 PRECURSOR/SISTER** — **같은 lead
저자(Jin Kyo Koo, Jaejin Lim), 같은 핵심 컨셉**(CNT로 Ni-rich 양극을 감싸 별도 도전재 없이 dry-processed
초고밀도 전극). 2025-list 외(2025 ESM) → **DTBL 논문으로 file, #275에 cross-link**. **본 디제스트는 #275와
같은 부분은 짧게, NEW만 길게** 다룬다. 풀 디제스트 포맷 reference = `docs/lit_koo2026_swcnt_sheath_thick_electrode.md`.

**소재계:** ★ **단결정 SC-NCA(LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂, single-crystalline Ni-rich layered oxide)** 입자를
**MWCNT(multi-walled CNT, 외경 ~18 nm — SI Fig S8d에서 2D peak + I_D/I_G≈1.01로 MWCNT 확인)**로 **anti-
solvent "salting-out" 방법**(NaCl + EtOH in DMF, 삼투압 stress + 수소결합)으로 감싸(swathing/wrapping)
**conformal 도전층** 형성 → 별도 도전재(CB) 없이 연속 전자전도. binder = **PTFE 0.4 wt%**(dry fibrillation).
**dry process**. 조성 SC-NCA@CNT : PTFE = **99.6 : 0.4 wt%**(그중 CNT 0.4 + NCA 99.2), 도전재 별도첨가 0.
음극 = **인조흑연(AG)**, **액체전해질**(1.15 M LiPF₆ in EC:EMC:DMC 2.4:4:4 vol% + 1% LiPO₂F₂; coin은
W-SCOPE 분리막). ★★ **우리 LPSCl sulfide ASSB가 아니다 — NCA 양극 + 흑연 + 액체전해질 일반 LIB(dry).**
그러나 **CARBON-MORPHOLOGY 물리(연속 wrapping이 discrete CB를 이김, discrete가 이온채널 막음)는 소재-일반**
→ #275와 동일하게 우리 voxel CBD 발견에 전이.

DB 동반 파일: `docs/data/densification_porosity_db.csv` 등 **수치 DB에는 추가하지 않음**(NCA/흑연/액체 LIB →
σ/porosity 절대앵커 아님 — 앵커는 **Bazzoun(LPSCl)/Varkey(halide)/Minnmann(LPSCl cold-press)/#266/#271**).
SI(38p) = Fig S1–S28 + Table S1–S6 + Supplementary Note S2 → digital-twin 방법·anti-solvent 메커니즘·
**SC-vs-PC 데이터(Fig S23)**만 본문 반영(전부 정독 아님).

---

## ★ 한 문장 결론 — 이게 무엇이고 #275 대비 무엇이 NEW인가

**#275와 동일한 핵심 메시지**(CNT로 Ni-rich 입자를 감싸 → 연속 도전층 → 도전재 별도첨가 0 → 활물질 99.6 wt%,
ρ 4.0 g/cm³, 835 mAh/cm³ → discrete CB를 전자·이온 양축에서 이김; 3D digital twin이 pore-network·τ·D_eff로
증명; CB-wet 대비 균질 전자/이온 수송·저저항·장수명). **셀 수치 절대값은 NCA/흑연/액체 → 우리 ASSB에 전이 불가.**

★ **#275 대비 NEW 4가지(이 디제스트가 집중하는 곳):**
- **(a) 단결정(SC-NCA) 초점 + SC-vs-PC 비교** — #275는 다결정 NCMA. 여기는 **단결정 SC-NCA**가 주인공이고,
  **SC-vs-PC의 입자강도/SSA/kinetics를 직접 대비**(우리 AM_S 단결정 vs AM_P 다결정 + #266 + #285 + ⚠#11 관련).
- **(b) anti-solvent "salting-out" wrapping** — #275의 zeta-potential/PDDA 정전기 조립과 **다른 방법**:
  NaCl이 DMF에서 안 녹다가 EtOH 넣으면 이온화 → 삼투압 stress + 수소결합으로 CNT를 입자 표면에 석출/부착.
- **(c) MWCNT** (외경 ~18 nm, 2D Raman peak) vs #275의 **SWCNT**(~2 nm, RBM). ★ 같은 컨셉, 다른 CNT 종.
- **(d) 2025 digital-twin(GeoDict 2022)** — #275(GeoDict 2023)의 직전 버전. 본질적으로 같은 워크플로
  (FIB-SEM 토모 → 분할 → effective σ/D/τ + PNM + BESTmicro 1D 전기화학). pore-network 결과도 같은 방향.

**우리 hook(#275와 같음 — double-count 금지):** 이 논문은 우리 CBD 발견(전자: 연속망 필요 + 이온: discrete가
채널 막음)을 #275와 **똑같이 실험으로 증명**한다 → audit ✅#4(CBD continuous-sheath, 이미 #275로 EXPERIMENTAL
PROOF)를 **REINFORCE**할 뿐 **새 축을 더하지 않는다**. ★ 진짜 NEW 가치는 **(a) SC-vs-PC 데이터**(⚠#11 σ_e-방향
질문의 추가 datapoint)와 **(b) anti-solvent 방법**이다.

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- **#275와 공통:** 두꺼운 고활물질 전극이 VED·급속충전의 핵심이나, **습식(wet)은 건조 중 binder/carbon migration**,
  **건식(dry)은 도전재 응집(CB agglomeration)**이 병목. **PTFE fibrillation binder**로 용매-free 가능하나 CB가
  잘 분산 안 됨. ⇒ **CNT로 활물질을 감싸 도전재를 표면 통합 + 최소 binder + dry process**로 해결(통합 active-
  conductive 아키텍처). dry process는 conventional 대비 **제조비 −20~30% · 에너지 −20~50%**.

- ★ **#275 대비 NEW = 단결정 NCA + SC-vs-PC 논쟁(이 논문 intro의 고유 부분):**
  - **다결정 PC-NCA의 근본 문제 = 입계균열(intergranular cracking).** 장기 cycling에서 이방성 팽창·수축 →
    1차입자 분리 → 입계균열 → 전해질 침투 → 계면 부반응(산소발생·rock-salt·TM dissolution) 가속. 형태조절·
    doping·coating으로도 해결 안 됨.
  - **단결정 SC-NCA(LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂)가 대안** — grain boundary 없음 → 입계균열 면역 → 장기 cycling 우수.
    BUT 상용화엔 도전 과제.
  - ★★ **SC vs PC kinetics는 문헌이 충돌(conflicting reports) — 이 논문의 명시적 주제:**
    - **Sun et al. (ref 19):** 단결정의 큰 1차입자 → **확산거리(diffusion distance) 길어짐 → kinetics ↓**;
      또 polycrystal에 있던 입자-전해질 계면의 fast diffusion path가 단결정엔 없음.
    - **Ma et al. (ref 20):** 단결정이 polycrystal **대비 Li⁺ 수송·rate 우수**(메커니즘은 불명확).
    - **Jung et al. (ref 21, ASSB):** PC vs SC를 **고체전해질 ASSB에서 비교** — 단결정이 더 작아서(작은 입자)
      **고체전해질→입자 표면까지 Li⁺ 확산거리 ↓ → rate ↑**. (단, ASSB는 입계침투가 안 일어남 = 액체와 다름.)
    - ⇒ **"입자크기가 PC vs SC의 kinetics·rate를 좌우하는가?"가 미해결** → 이 논문은 추가 규명이 필요하다고 명시.
  - **★ SC-vs-PC 물성차 (intro 명시):** **입자크기·비표면적(SSA)·morphology가 SC와 PC를 구분.** ★★
    **SSA: 단결정 SC-NCA = 0.88 m²/g vs 다결정 PC-NCA = 0.31 m²/g**(SC가 ~2.8× 큼 — 작은 입자/큰 표면). 큰
    SSA·작은 입자는 통상 **더 많은 CB·PVDF binder를 요구**(도전경로·접착 확보) → 단결정에 종전 PC용 CB 방식을
    그대로 쓰면 mismatch("crack-free SC-NCA의 고밀도 잠재력"을 못 살림). ⇒ **SC-NCA에 맞춤형(전자·이온 균형)
    전극설계 필요** → CNT-wrapping으로 최소 도전재.
  - ★ **단결정 활물질 surface = 전자·Li⁺ 수송이 일어나는 곳** → 표면 전자전도 향상이 결정적 → CNT를 표면에
    균일 부착(0.4 wt%) → 별도 도전재 0 → **종전 상용설계의 2–5 wt% 도전재 제거**.

**약어:** SC-NCA = single-crystalline Ni-rich oxide LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂(우리 **AM_S = single** 대응).
PC-NCA = polycrystalline 동일조성(우리 **AM_P = poly** 대응). MWCNT = multi-walled carbon nanotube
(외경 ~18 nm, 1D). CB = carbon black(Super P, 0D, 우리 SuperP 대응). CBD = carbon-binder domain.
SSA = specific surface area(비표면적, BET). VED/GED = volumetric/gravimetric energy density.
PNM = pore network model. FIB-SEM = focused-ion-beam SEM tomography. KPFM 미사용(#275엔 있음).
SSRM = scanning spreading resistance microscopy. TLM = transmission line model(R_ion 추출). DMF =
dimethylformamide(비극성 분산용매). PAN/PVP = CNT ink 분산제. **CB-wet / CB-dry / CNT-dry** = 3종
전극 코드(여기선 SWCNT-wet 없음 — #275의 4종과 차이).

---

## 2. anti-solvent "salting-out" MWCNT wrapping 메커니즘 (Fig 1, §"Uniform wrapping of CNTs onto SC-NCA"; §4.1 Methods) ★ NEW vs #275

★ **핵심 발견 1 (#275 대비 NEW = 조립 메커니즘이 다름):** **#275는 zeta-potential/PDDA 정전 조립; 여기는
anti-solvent salting-out(삼투압 + 수소결합).**

**anti-solvent salting-out 4단계 조립(Fig 1a 모식 + §4.1):**

| 단계 | 조작 | 물리 |
|---|---|---|
| ① 분산 | SC-NCA(총 3 g) + MWCNT ink를 **DMF**(비극성)에서 vortex 1 min | CNT가 van der Waals + π-π로 응집하려는 경향 → ink로 분산 |
| ② NaCl 투입 | **NaCl 0.25 wt%**(SC-NCA 대비) 첨가, vortex 1 min | NaCl은 DMF에 거의 안 녹음(용해도 ~0) → 고체상으로 잔존 |
| ③ EtOH(anti-solvent) + 원심 | **EtOH 6 mL** 첨가, vortex → 원심분리(**2000 rpm, 1 min**) | ★ EtOH(극성) 들어오면 NaCl이 **이온화(Na⁺·Cl⁻)** → 이온이 주변 용매분자를 강하게 끌어당겨(solvation) **자유 CNT 주위 ionic strength ↓ → ion depletion area** 형성 → CNT의 정전 안정화 붕괴 → 반발력 약화 → **CNT 응집·석출("salting out")** + **삼투압 stress(osmotic stress)**가 CNT를 입자 표면으로 밀어붙임 |
| ④ 부착·건조 | swathed 분말 원심수거 → 진공건조 **120°C 12 h** | ★ **PAN(polyacrylonitrile, CNT ink 분산제)의 nitrile(–C≡N)기가 SC-NCA 표면의 hydroxyl(–OH)기와 수소결합** → CNT가 SC-NCA 표면에 부착 고정 → conformal coating |

- **물리 요약:** NaCl이 EtOH로 이온화 → 국소 ionic strength 교란 → CNT 정전반발 약화 → CNT 석출(salting out)
  + 삼투압이 입자로 압박 → PAN–OH 수소결합으로 표면 고정. **#275의 "PDDA로 표면전하 반전→정전인력"과 전혀
  다른 화학.** (둘 다 결과는 "conformal 도전 wrapping"으로 동일.)

**CNT ink 농도 최적화(Fig 1b–f + SI Fig S1, S4, S5):**
- **CNT ink 농도 0.25–1.0 wt%** 4수준(Fig 1b FE-SEM): 농도↑ → SC-NCA 표면 CNT coverage·균일도↑.
- **BET SSA(Fig 1d):** bare SC-NCA ~**0.7** → CNT-swathed 0.25/0.5/0.75/1.0 wt%에서 ~**1.0/1.4/1.6/2.1 m²/g**
  단조↑(CNT 양↑). **탄소함량(Fig 1e, CS 분석):** bare ~0.05 → 0.25/0.5/0.75/1.0에서 ~0.3/0.5/0.55/1.1 wt%
  단조↑. ★ **0.75 wt% ink가 최적**(균일 + 적정 coverage); **1.0 wt%는 과량 → 미부착 CNT 응집 잉여**(SI Fig S4b
  FE-SEM 응집 + Fig S5b "unclean dry sheet" + Fig S4 viscosity↑로 부착 저해) → **0.75 wt% = "extremely sleek
  dry electrode"**(Fig S5a). (★ 본문 후속에서 최종 전극 조성은 CNT 0.4 wt%로 정리 — Table S4/S15.)

★★ **분말 전기전도(Fig 1f + SI Fig S2/S3) — 핵심 수치:**
- **(SC-NCA + CB) 98:2 분말:** 최대압축에서 **≈ 4.7×10⁻² S/cm**.
- **SC-NCA@CNT 0.75 wt% 분말:** **≈ 2.3×10⁻¹ S/cm** = **CB 2 wt% 대비 4배 이상 높음**(최소 CNT ≈0.5 wt%로도
  CB 2 wt% 능가). press power 4→20 kN로 단조↑(Fig 1f). ★ **흥미로운 비단조:** 1.0 wt% CNT는 0.75 wt%보다
  **분말전도 낮음**(잉여 CNT 응집 → ink viscosity↑ → 균일부착 저해; 본문 명시).
- **분말 packing density(SI Fig S3a):** **SC-NCA@CNT > SC-NCA:CB(98:2)**, 모든 press power(4–20 kN)에서 — CB
  무첨가로 packing↑. → CNT-wrapped는 추가 도전재 없이 전도 + packing 둘 다 이득.

**coating 검증(Fig 1c + SI Fig S6, S7):**
- **HR-TEM(Fig 1c):** SC-NCA 표면에 **MWCNT 층(외경 ~18 nm)** 잘 부착(scale bar 10 nm).
- **FE-SEM(SI Fig S6a,b):** bare SC-NCA = 매끈 vs SC-NCA@CNT = 표면 CNT 망. **XRD(Fig S6c):** wrapping 전후
  층상구조(003/101/104…) **유지**(불순물상·구조변화 없음). **confocal Raman(Fig S7):** D/G band(CNT) + Ni-rich
  cathode(560 cm⁻¹) 균일 분포 → CNT 균일 부착. ★ **(SI Fig S8d) MWCNT 확인:** D/G + **2D peak(~2700 cm⁻¹)** +
  **I_D/I_G = 1.01** → multi-walled. (Super P는 Fig S8c, I_D/I_G=0.99, 2D peak 없음.) ⇒ **#275의 SWCNT(RBM ~150
  cm⁻¹)와 명확히 다른 CNT 종**.

---

## 3. 3종 전극(CB-wet/CB-dry/CNT-dry) 비교 — powder rheology + 전자/이온 수송 (Fig 2–4) ★ #275와 동일 방향(짧게)

★ **핵심 발견 2 (#275와 동일):** **CNT-dry가 최고밀도·균질 전자/이온·저저항.** (#275는 4종 SWCNT-wet 포함, 여기는
3종.)

**전극 조성·밀도(Fig 3i,j + SI Table S4, S15):**

| 전극 | 조성(wt%) | binder | 밀도 ρ (g/cm³) | 두께 (µm) | loading (mg/cm²) |
|---|---|---|---|---|---|
| **CB-wet** | SC-NCA:CB:PVDF = **96:2:2** | PVDF | **3.6** | 66.5 | 23.96 |
| **CB-dry** | SC-NCA:CB:PTFE = **96:2:2** | PTFE | 3.6 | — | — |
| ★ **CNT-dry** | SC-NCA@CNT:PTFE = **99.6:0.4** (CNT 0.4 / NCA 99.2) | PTFE | ★ **4.0** | 57.7 | 23.09 |

(CNT-dry = 활물질 99.6 wt%, **별도 도전재 0**. Q_areal ~4.6 mAh/cm² 공통.)

**powder rheology(Fig 2 + Fig 3d–h, SI Fig S11/S12):**
- **SC-NCA:CB(98:2) vs CNT@NCA powder:** total energy **46 vs 35 mJ**, cohesion **2.0 vs 1.6 kPa**,
  flow function FF **2.16 vs 2.68**(높을수록 흐름성↑). ★ **CNT@NCA가 흐름성 좋고 응집 적음**(CB 미세입자 제거).
  → PTFE fibrillation·균일 시트화 용이(Fig S11: NCA:CB는 mixing 후에도 불균일, CNT@NCA는 fine·uniform).
- **단면 SEM(Fig 3 + SI Fig S10):** **CB-wet = SC-NCA↔CB 점접촉**(Fig S10a "good contact despite non-uniform"),
  **CB-dry = CB가 fibrillated PTFE에 엉켜 SC-NCA와 접촉 불량**(Fig S10b "Lack of contact"), **CNT-dry = 밀도
  4.0 + CNT 표면 도전망**. **MIP 기공분포(Fig 3k):** CB-wet/CNT-dry 총기공 유사하나 **CNT-dry는 200–300 nm 큰
  기공(전해질 채움) 빈도↑**(CBD 부재 → SC-NCA 사이 open pore).

**전극 면저항 맵(SI Fig S10c, 15점/전극):** ★ **CB-wet 평균 ~15–25 Ω·cm / CB-dry ~26–34 Ω·cm(최악, CB 접촉
불량) / CNT-dry ~5–7 Ω·cm(최저·균질)**. → CNT 연속 도전망이 균일 저저항.

**전자/이온 수송(Fig 4 + SI Note S2, Table S1):**
- **rate(half-cell, Fig 4a):** 0.2–5C에서 CB-wet ≈ CNT-dry까지 비슷하나 **5C에서 CNT-dry 75% vs CB-wet 62%
  유지**(CNT-dry가 도전재 적음에도 고율 우수). CB-dry는 최악.
- **SSRM 단면 저항맵(Fig 4b, cycling 전):** CNT-dry = 균일 저저항(10⁻⁴–10⁻³ Ω 청색) / CB-wet = 넓은 분포
  (10⁻³–10² Ω, CB 응집·PVDF 절연부). 저항 히스토그램(Fig 4c): ★ **CNT-dry 평균 1.856 GΩ vs CB-wet 6.411 GΩ**.
- ★ **이온저항 R_ion(대칭셀 EIS, TLM, Fig 4d,e):** **CB-wet 8.84 Ω vs CNT-dry 7.85 Ω**(Gasteiner τ 식).
- ★★ **tortuosity τ(EIS 기반, SI Note S2 식 τ = R_ion·A·ε / (L·ρ); Table S1):** **CB-wet 1.75 vs CNT-dry 1.03**
  (porosity ε: CB-wet 0.14 / CNT-dry 0.083 — MIP). **CNT-dry가 밀도 높고(ρ 4.0) 기공률 낮은데도 τ가 낮음**
  (덜 우회) = 잘 발달된 기공망.
  ⚠ **이 τ(EIS 1.75/1.03)는 digital-twin τ(Fig 4f, §아래 2.05/1.26)와 다른 값** — **두 방법(EIS-TLM vs digital-
  twin diffusion sim)**의 차이. 절대값 비교 시 어느 방법인지 명시 필요.
- **전자/이온 경로 모식(Fig 4g):** CB-wet(CBD가 e⁻·Li⁺ 막음) vs CNT-dry(표면 CNT가 e⁻, 빈 기공이 Li⁺) → 균질.

---

## 4. 3D digital-twin 시뮬레이션 (Fig 5 + SI Fig S14–S22) ★ #275와 본질 동일(GeoDict 2022, 짧게 + 차이만)

★ **핵심 발견 3 (#275와 동일 워크플로):** **digital twin이 CNT-dry의 pore-network·effective σ/D/τ·균질 농도를 정량
검증.** (#275 = GeoDict 2023; 여기 = **GeoDict 2022** = 직전 버전. PNM·effective·1D 전기화학 구조 동일.)

**방법(SI §4.7–4.9):**
- **FIB-SEM tomography:** **총 840장**(#275는 820장), ion milling interval, **voxel 32.5 & 37.22 nm**, 3D domain.
  FFT + nonlocal means 필터 → trilinear rescale → **Unet AI 분할 + multiphase 분할**(SC-NCA/CBD or PTFE/pore/Al
  4상; SI Fig S14). 재구성 부피분율 vs 이론 **편차 CB-wet <2.64 %p / CNT-dry 0.13 %p**(SI Fig S15/S16 — Table:
  CB-wet SC-NCA 76.58/CBD 8.58→9.79/pore 14.84%; CNT-dry SC-NCA 83.97/PTFE 0.74/CNT 1.81/pore 13.47%).
- **effective 물성(GeoDict 2022 ConductoDict + DiffuDict, SI Fig S19):** voxel에 Ohm 법칙(σ_s,eff/σ_e,eff,
  ΔV=1 V Dirichlet)·Fick(D_e,eff, Δc=1 mol/m³)을 **3방향(x in-plane / y thickness / z in-plane)**으로 풀어 균질화.
  지배식 j_s=−σ_s,eff∇φ_s, j_e=−(ε_e σ_e/τ_e²)∇φ_e, J=−(ε_e D_e/τ_e²)∇c_e.
- **PNM(SI Fig S17):** watershed → ball-and-stick → 등가반경·coordination number·connectivity. (#275/#286과 동일.)
- **1D 전기화학(SI Fig S20–S22, Table Fig S21):** **BESTmicro(Fraunhofer ITWM)**로 **5C 방전** 시뮬(재구성 3D +
  가상 Cu/Li/separator/Al, 15×15×15 µm³ domain). 지배식 = 전하보존·물질보존·Fick·Ohm·**Butler-Volmer**. OCP =
  GITT(0.05C), c_max=37,097 mol/m³(실측용량 205 mAh/g·진밀도 4.8), **σ_s = 4.03 [a] / 29.03 [b] S/m**(활물질
  전자전도, 두 문헌값), σ_e 0.9327 S/m, D_e 3.8346e-10, D_s 1.5e-15 m²/s, t₊ 0.25, BV k 2.4e-6, 298.15 K.

**digital-twin 정량 결과(Fig 5 + SI Fig S17–S19):**
- **closed pore(고립기공) 비율(Fig 5e):** ★ **CB-wet 17.72 % vs CNT-dry 2.4 %** — CB-wet의 고립기공이 **7.4배**
  많음(대부분 CB-wet의 다공 CBD에 갇힘 → Li⁺ 수송 기여 못 함). CNT-dry = CBD 부재 → 기공 잘 연결.
- **PNM 등가반경·coordination(Fig 5h,i + SI Fig S17c–e):** 등가반경 50th pctile **CB-wet 1.903 vs CNT-dry 2.723
  µm**(CNT-dry 큰 기공); coordination number 50th **CB-wet 3 vs CNT-dry 4**(CNT-dry 연결↑); connectivity bandwidth
  CNT-dry > CB-wet(장거리 연결).
- ★★ **effective 물성(SI Fig S18a, S19) — 핵심 수치:**
  - **유효 전자전도 σ_s,eff(Fig 5/SI Fig S18a):** ★ **CNT-dry가 CB-wet의 3.1배**(experiment ≈ sim, CB-wet ~4.5 vs
    CNT-dry ~14 S/m; exp-sim 편차 4.2 %). 전자 current density 맵(Fig S18b,c): CNT-dry 전극 전체 균일 / CB-wet
    국소 CBD에 집중("Large carbon binder region"에 갇힘).
  - **유효확산 D_e,eff(SI Fig S19a):** CNT-dry > CB-wet(x/y/z); 두께방향(y) CB-wet ~3.8e-12 vs CNT-dry ~1.1e-11 m²/s
    수준(이방성 있음). **유효 이온전도 σ_e,eff(Fig S19b):** CNT-dry > CB-wet(z방향 ~0.041 vs ~0.012 S/m).
  - ★ **tortuosity τ(digital-twin, 두께방향 y; Fig 4f & SI Fig S19c):** **CB-wet 2.05 vs CNT-dry 1.26**(τ **36 %**
    감소). + 이방성(x/y/z 별도). ⚠ **EIS-TLM τ(1.75/1.03, Table S1)와 다른 값** = 방법 차이(앞서 명시).
- **1D 방전 시뮬(Fig 5j,k + SI Fig S22):** 5C 종료 시 — **전해질 Li⁺ 농도(Fig S22a,b): CB-wet = 두께방향 큰 구배**
  (separator측 ~2.3 M → 바닥 <0.5 M 고갈) / **CNT-dry = 균일 ~1.0–1.3 M**. **고체 Li⁺·current density·과전압맵
  (Fig 5j,k): CNT-dry 균일 / CB-wet 표면집중·불균질.** 과전압 분해(Fig S22e,f): CB-wet의 큰 ohmic+농도 과전압.
- **특정접촉면적(MatDict, 본문):** **CNT-dry의 활물질↔CBD 접촉면적이 CB-wet 대비 ~77 % 낮음**(점접촉 최소,
  CBD 부재) + 활물질↔기공 접촉(반응 site)↑ → 균일 flux.

⇒ **digital-twin 결론(#275와 동일):** CNT-dry = 우월한 Li⁺/e⁻ 수송(σ_s,eff 3.1×, τ↓ 36 %, 고립기공 2.4 vs
17.72 %, 균일 농도/전류) → 두꺼운 고밀도 전극의 미세구조적 근거.

---

## 5. ★★ SC-vs-PC 비교 (SI Fig S23, intro) — ⚠#11 σ_e-방향 질문의 추가 datapoint (이 디제스트의 핵심 NEW)

★ **핵심 발견 4 (#275에 없는 NEW):** **이 논문은 단결정(SC) vs 다결정(PC) NCA를 직접 대비한다 — 단 "전자전도"가
아니라 "입자강도·균열·SSA·kinetics(문헌충돌)" 축에서.**

### (a) ★★ SC-vs-PC 입자강도·균열 (SI Fig S23) — 정량 데이터 있음
- **입자강도(particle strength @ 10% shape strain, nano-press, H = 2.8P/(π·d_p²)):**
  ★★ **SC-NCA = 111.63 MPa vs PC-NCA = 48.96 MPa** → **단결정이 ~2.3× 강함(견고).**
- **균열(area fraction of microcracks, 단면 SEM):** ★ **PC-NCA@3.6 g/cc = 7.8 % microcrack vs SC-NCA@4.0 g/cc =
  0 %(no microcrack)** — 단결정은 4.0 g/cc 고밀도 압축에도 균열 없음, 다결정은 3.6 g/cc에서도 7.8 % 균열.
  (Fig S23d PC-NCA = 입계균열 다수 / S23e SC-NCA = 균열 없음.)
- ⇒ **"단결정은 견고 → 고밀도 압축(4.0 g/cc) 가능, 다결정은 입계균열로 못 감"** = CNT-dry가 단결정을 쓴 이유.

### (b) ★ SC-vs-PC SSA (intro)
- ★ **SSA: SC-NCA 0.88 m²/g vs PC-NCA 0.31 m²/g**(SC ~2.8× 큼 — 작은 입자/큰 표면).

### (c) ⚠⚠ SC-vs-PC 전자전도/kinetics — **이 논문은 직접 수치 비교를 주지 않는다(정직히 명시)**
★★ **⚠#11(σ_e composition-direction) 질문에 이 논문이 주는 것 / 안 주는 것을 정확히:**
- **이 논문은 SC-NCA vs PC-NCA의 "전자전도(σ_e)"를 직접 측정·비교하지 않는다.** 분말전도(Fig 1f)는 모두 **SC-NCA**
  기반(SC-NCA+CB vs SC-NCA@CNT)이고, σ_s(활물질 전자전도) = 4.03/29.03 S/m은 **문헌값**(SC-vs-PC 구분 아님).
- **kinetics/rate에 대해서는 "문헌이 충돌한다(conflicting)"고 명시**(intro): Sun(SC 확산거리↑→kinetics↓) vs
  Ma(SC가 Li⁺ 수송↑) vs Jung(ASSB에서 작은 SC가 확산거리↓→rate↑). ⇒ **이 논문 자체는 SC-vs-PC kinetics 우열을
  결론짓지 않고, "입자크기가 좌우하며 추가 규명 필요"라고만 함.** 자기 데이터로는 **SC-NCA를 채택한 이유 = 전자/
  kinetics 우월이 아니라 (a)의 기계적 견고성·무균열 고밀도화**다.
- ★ **⚠#11에 대한 함의(정직한 해석):**
  - **우리 ⚠#11 질문 = "σ_e가 큰 다결정(AM_P)에서 높은가, 작은 단결정(AM_S)에서 높은가"** (#266 σ_NCWA-poly 13.7
    ≫ σ_NCM-single 2.45 = 다결정↑ vs 우리 σ_e 끝점가정 σ_S-single 10 > σ_P-poly 5 = 단결정↑, 부호 반대).
  - **이 논문(Koo 2025)은 이 질문에 직접 답하지 않는다** — SC-vs-PC를 **재료 고유 σ_e**가 아니라 **입자강도·SSA·
    (문헌충돌) kinetics**로 다룸. ⇒ **⚠#11의 추가 "전자전도 datapoint"로는 약함**(직접 σ_e 수치 없음).
  - **다만 간접 시사 2가지:** ① **SSA(SC 0.88 > PC 0.31)** = 단결정이 더 작은 입자 → **입자수·접촉수가 많다** →
    우리 σ_e의 "접촉수 지배(작은 입자↑)" 가정과 **방향 일치**(우리 σ_S-single↑ 가정을 약하게 지지). ② **kinetics
    문헌충돌**은 #266(다결정 σ_e↑)과 우리(단결정 σ_e↑)의 부호 충돌이 **literature-wide 미해결**임을 재확인 →
    **⚠#11은 "한 논문으로 결판 안 나는 material-dependent 문제"**라는 우리 audit 판단을 **강화**.
  - ⇒ **⚠#11 결론: Koo 2025는 #266의 "다결정 σ_NCWA↑"를 뒤집는 직접 반례(단결정 σ_e↑ 수치)를 주지 않는다.**
    SSA(작은 단결정→접촉수↑)는 우리 가정 방향과 부호가 같지만 **재료 고유 σ_e가 아니라 기하(접촉수) 논거** →
    **#266의 재료-고유 σ_e(다결정 13.7 ≫ 단결정 2.45)와 직접 모순되지 않는다**(두 효과는 다른 축: 재료 고유 σ
    vs 입자수/접촉수). **σ_e-방향은 여전히 재료·기하 둘 다 의존 → ⚠#11 유지**(이 논문은 "kinetics 문헌충돌"
    증거로 추가될 뿐 결판 datapoint 아님).

---

## 6. 장기 cycling·full cell·고에너지밀도 (Fig 6–8 + SI Fig S25–S28, Table S2–S6) ★ #275와 동일 방향(짧게)

★ **핵심 발견 5 (#275와 동일):** 균질 CNT 도전망 = 균일 반응 = 장수명 + 고에너지밀도.

- **half-cell(Fig 3i 본문 + SI Fig S24/S25):** 0.2C에서 CNT-dry **208 mAh/g vs CB-wet 202 mAh/g**; 부피용량
  ★ **CNT-dry Q_vol ≈ 835 mAh/cm³** (208 × 4.0) **vs CB-wet ~744** (202 × 3.6) — **ρ 4.0의 효과**. (Table S5: 0.2C
  CNT-dry 835 vs CB-wet 738.) 0.5C 25사이클 거의 무손실(Fig S25).
- **full cell(CNT-dry‖AG, Fig 6a–c + SI Fig S26):** ★ **500사이클 80–85 % 유지**(2.8–4.4 V, 0.5C, RT) vs CB-wet
  급감(<50 % @100cyc). 부피용량 CNT-dry 791 mAh/cm³ (CB-wet 685, +15.6 %). **평균 CE 99.8 %**(Fig S26).
  고면적부하(~11 mAh/cm²) full cell(Fig 6b): **CNT-dry SOH 92 %@50cyc vs CB-wet 82 %/CB-dry 82 %**.
- **고온 안정성(SI Fig S27):** 60°C, 2.75–4.4 V, 0.5C — CNT-dry(dry) > CB-wet(wet) 유지(단결정 무균열 + 표면
  CNT가 전해질 노출↓). 300사이클 full cell도 CNT-dry 우위.
- ★★ **10 Ah pouch 고에너지밀도(Fig 6e + SI Table S6):** **CNT-dry‖Gr: GED 303.9 Wh/kg · VED 858.1 Wh/L**
  (셀용량 10.04 Ah, nominal 3.7 V, 셀부피 0.433 L, 셀무게 122.26 g) vs CB-wet‖Gr 295.2 / 813.9. (초록·본문은
  반올림 셀레벨 ~303.9 Wh/kg · 858 Wh/L; coin 전극레벨 Q_vol 835.) **Fig 6e: this work = 상용 LIB(NCM111→
  NCM90/LNO) 라인 상회**(99.6 wt% AM + ρ 4.0의 효과). **250사이클 pouch(SI Fig S28) 안정.**
- **문헌비교(Table S2/S3):** SC-NCA@CNT(99.6:0.4, ρ 4.0, Q_vol 832, 500cyc 80 %)가 **종전 dry-processed 전극
  (VGCF/CB+PTFE, ρ 2.4–3.1, Q_vol 322–540)을 밀도·부피용량에서 크게 상회**. SWCNT(ozone-treated, ref [4]
  ρ 3.2–3.4)보다도 높은 밀도.

---

## 7. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것 (#275와 겹치는 건 짧게)

### 본문 Figures
- **Fig 1 (p.3):** ★ NEW 조립 — (a) **anti-solvent salting-out 4단계 모식**(NaCl+EtOH 이온화→ion depletion→
  삼투압→H-bonding). (b) FE-SEM CNT ink 0.25–1.0 wt%. (c) HR-TEM(MWCNT 18 nm). (d) **BET SSA**(bare 0.7→
  1.0 wt% 2.1). (e) **탄소함량**. (f) ★ **분말전도**(SC-NCA+CB 0.047 vs SC-NCA@CNT 0.23 S/cm, 4×). → ★ **#275의
  zeta wrapping과 다른 anti-solvent 메커니즘 증거**.
- **Fig 2 (p.4):** wet vs dry 공정 모식 + dry 시퀀스(feedstock→3-roll→sheet). #275/#276과 동일(짧게).
- **Fig 3 (p.5):** ★ powder rheology + 아키텍처 — (a–c) CB-dry 단면(CB 응집). (d–f) **flowability**(total energy
  46 vs 35 mJ, cohesion 2.0 vs 1.6, FF 2.16 vs 2.68). (g,h) dry sheet 사진. (i,j) **CB-wet 3.6 vs CNT-dry 4.0
  g/cc 단면+EDS C-map**. (k) **MIP 기공분포**(CNT-dry 200–300 nm 큰 기공↑). → carbon morphology가 packing·기공
  결정(우리 CBD seeding 대응).
- **Fig 4 (p.6):** ★ 전자/이온 수송 — (a) **rate**(5C CNT-dry 75 vs CB-wet 62 %). (b) **SSRM 저항맵**(CNT-dry
  균질). (c) **저항 히스토그램**(CNT-dry 1.856 vs CB-wet 6.411 GΩ). (d,e) **대칭셀 EIS R_ion**(8.84 vs 7.85 Ω).
  (f) **tortuosity**(CB-wet 2.05 vs CNT-dry 1.26 — digital-twin값). (g) **e⁻/Li⁺ 경로 모식**. → ★ **우리 전자축(연속
  망이 균일·저저항) + 이온축(τ↓) 발견의 실험증명**(#275와 같음).
- **Fig 5 (p.8):** ★★ digital twin = 우리 voxel/Phase-4 — (a,b) **재구성 3D**(SC-NCA/CBD or PTFE/pore/Al). (c–e)
  **diffusion flux + 고립기공(CB-wet 17.72 vs CNT-dry 2.4 %)**. (f,g) **고립기공 3D viz**. (h,i) **특정접촉면적**
  (NCA‖CBD vs NCA‖pore). (j,k) **5C 방전 3D맵**(농도·전자/이온 current density·과전압, CNT-dry 균일). → ★
  **GeoDict 2022 effective(σ_s,eff 3.1×/τ 36 %↓/closed pore) + BESTmicro 1D = 우리 voxel FV+PyBaMM blueprint**.
- **Fig 6 (p.10):** 장기+고에너지 — (a) **500cyc**(CNT-dry 80–85 %). (b) **고부하 SOH**(92 vs 82 %). (c) **pouch
  250cyc**. (d) **5축 레이더**(AM%·용량·밀도·Q_vol·cycle). (e) **VED vs 비용량 산업비교**(this work 상회). → ★
  레이더(#275/#281 동일, predictor 출력 후보).

### SI Figures + Notes (정독: anti-solvent + SC-vs-PC + digital-twin)
- **Fig S1:** MWCNT HR-TEM(20 nm scale) + CNT ink 0.25–1.0 wt% 사진. **Fig S2:** 분말전도 4-probe 압력셀(4–20 kN).
  **Fig S3:** ★ packing density SC-NCA@CNT > SC-NCA:CB(98:2). **Fig S4:** ★ swathing 사진(0.75 최적 vs 1.0 잉여
  CNT 응집 FE-SEM). **Fig S5:** dry sheet(0.75 sleek vs 1.0 unclean). **Fig S6:** FE-SEM(bare vs CNT) + **XRD
  구조유지**. **Fig S7:** confocal Raman map(CNT 균일). **Fig S8:** ★★ Raman — CB-wet map + **Super P I_D/I_G=0.99
  (2D 없음) vs MWCNT I_D/I_G=1.01 + 2D peak**(MWCNT 확정). **Fig S9:** CB-dry top SEM+EDS(CB 응집). **Fig S10:**
  ★ 단면 SEM(CB-wet 점접촉/CB-dry 접촉불량) + **면저항 맵 3종**(CNT-dry 5–7 vs CB-wet 15–25 vs CB-dry 26–34 Ω·cm).
  **Fig S11:** powder 사진(CNT@NCA fine·uniform). **Fig S12:** powder rheology 장치.
- **Fig S13:** CB-dry/CB-wet 전압곡선(0.1–5C). **Note S2 + Table S1:** ★ **τ EIS-TLM 식 + CB-wet 1.75 / CNT-dry
  1.03**(ε 0.14/0.083, R_ion 8.84/7.85). **Fig S14:** ★ FIB-SEM 분할·재구성 모식(Unet). **Fig S15:** ★ 토모+이론
  부피분율(CB-wet SC-NCA 76.58/CBD 8.58/pore 14.84; CNT-dry SC-NCA 83.97/PTFE 0.74/CNT 1.81/pore 13.47%; 진밀도
  NCA 4.8/PVDF 1.77/PTFE 2.2/CB·CNT 1.8). **Fig S16:** 재구성 vs 이론 편차(CB-wet <1.29 %p / CNT-dry <0.36 %p).
  **Fig S17:** ★ PNM(2D 기공맵·등가반경 1.903 vs 2.723 µm·coordination 3 vs 4). **Fig S18:** ★ **σ_s,eff exp vs sim
  (CNT-dry 3.1×) + 전자 current density 맵**(CB-wet 국소집중). **Fig S19:** ★ **effective D_e/σ_e/τ 3방향 이방성 +
  지배식·기호**. **Fig S20:** half-cell 1D 모델(Cu/Li/sep/cathode/Al). **Fig S21:** ★ **1D 파라미터**(GITT OCP,
  c_max 37097, σ_s 4.03/29.03, BV식). **Fig S22:** ★ **5C 방전 농도·과전압 분해**(CB-wet 큰 구배).
- **Fig S23:** ★★ **SC-vs-PC 입자강도(111.63 vs 48.96 MPa) + 균열(PC 7.8 % vs SC 0 %) + 단면 SEM**. **Fig S24/S25:**
  CB-wet vs CNT-dry 전압·cycling. **Fig S26:** full cell CE(99.8 %). **Fig S27:** 60°C cycling. **Fig S28:** pouch
  250cyc. **Table S2/S3:** 문헌비교. **Table S4:** 셀 사양. **Table S5/S6:** Q_vol·pouch VED/GED 계산.

---

## 8. 기술 미니용어집 (우리 맥락, #275와 겹치는 항목은 생략)

- **anti-solvent "salting-out"(반용매 염석):** 비극성 용매(DMF)에 안 녹는 염(NaCl)을 넣고 극성 anti-solvent
  (EtOH)를 첨가 → 염이 이온화 → 국소 ionic strength 교란(ion depletion) → 분산 colloid(CNT)의 정전 안정화 붕괴
  → 석출/응집 + 삼투압 stress로 입자 표면에 부착. ★ **#275의 zeta/PDDA 정전조립과 다른 wrapping 화학.** 우리엔
  직접 대응 없음(LPSCl 표면화학 별도) — CBD seeding(`nucleate_frac`)의 "어떻게 도전재를 표면에 붙이나"의 제2 경로.
- **SC-NCA vs PC-NCA(단결정 vs 다결정 NCA):** 단결정 = grain boundary 없음 → 입계균열 면역·견고(111.63 MPa)·
  무균열 고밀도화(4.0 g/cc) 가능 but SSA 큼(0.88)·확산거리 길 수 있음(문헌충돌). 다결정 = 입계균열·SSA 작음
  (0.31)·견고성 낮음(48.96 MPa). = 우리 **AM_S(single) vs AM_P(poly)** 직접 대응(#266/#285 일관).
- **particle strength @ 10% shape strain(입자강도):** nano-press로 입자를 10% 변형시키는 압력 H=2.8P/(πd²).
  단결정 2.3× 강함 → 우리 MPM의 **AM rigid scaffold + 단결정 견고성**(#285) 정당화. 우리 fracture(Auerbach)의
  재료강도 입력 후보(단, NCA 액체계 — LPSCl ASSB 직접앵커 아님).
- **σ_s (active material electronic conductivity):** 활물질 자체 전자전도 = 4.03 / 29.03 S/m(문헌 두 값).
  우리 σ_e 끝점(σ_AM)의 reference 후보(단 NCA — 우리는 NCM811 ~50 mS/cm = 5 S/m 기준; #266 σ_NCWA 13.7 ≫
  σ_NCM 2.45 mS/cm와 단위·재료 다름 → 직접 대입 금지).
- **closed/isolated pore(고립기공):** bulk 기공망에서 단절 → Li⁺ 수송 기여 못 함. CB-wet 17.72 vs CNT-dry 2.4 %.
  = 우리 SE 퍼콜레이션의 "dead-SE"(고립 SE 채널) 기공판(#275 동일).
- **tortuosity τ — 두 방법 주의:** (i) **EIS-TLM**(SI Note S2, R_ion·A·ε/(L·ρ)): 1.75/1.03. (ii) **digital-twin
  diffusion sim**(GeoDict, ε_e·D_e/τ²): 2.05/1.26. **같은 전극인데 방법 따라 값 다름** → 우리 τ_Laplace vs
  τ_Dijkstra 선택의 실증(어느 정의인지 항상 명시). #286(EIS vs 확산 2-방법)과 동일 교훈.

---

## ★ 9. 비교 vs 우리 DEM+MPM (frame [1]–[5]) — audit ✅#4 REINFORCE(double-count 금지) + ⚠#11 + positioning

⚠ **대전제(맨 먼저, #275/#284/#285/#286과 동일):** 이 논문은 **단결정 NCA 양극 + 흑연 음극 + 액체전해질 dry-
processed 일반 LIB**다 — 우리 **LPSCl sulfide ASSB(고체전해질, 무전해질 contact-network)**가 **아니다**. 따라서:
- **셀 전기화학 절대값은 전이 불가.** 858 Wh/L · 304 Wh/kg · 835 mAh/cm³ · 208 mAh/g · τ 1.03–2.05 · σ_s,eff 3.1× ·
  500cyc 80–85 % 등은 **NCA/흑연/액체전해질** 값이고 Li⁺가 **전해질을 통해 확산**하는 물리다 — 우리 σ_ionic/e는
  **SE/AM 입자 접촉망의 Kirchhoff/Holm 전도**(무전해질). **수치 σ/porosity 앵커는 Bazzoun(LPSCl)/Varkey(halide)/
  Minnmann(LPSCl cold-press)/#266/#271이 담당** — 이 논문에서 안 가져온다.
- ★ **강하게 전이되는 것 = CARBON-MORPHOLOGY 물리(소재-일반):** **(i) 연속 도전망이 두꺼운 전극 전자전도를 이기고
  discrete 도전재는 연속망을 못 만든다; (ii) discrete 도전재는 이온수송 채널(전해질 기공)을 막는다.** 전해질 종류·
  활물질 무관한 기하·퍼콜레이션 물리.

### (a) ★ audit ✅#4 (CBD continuous-sheath) — **REINFORCE만, double-count 금지**
- **우리 발견:** voxel carbon-only에서 discrete carbon(SuperP/짧은 VGCF)은 두꺼운 전극 self-percolate 불가(σ=0;
  carbon ~6–7 % 셀 ≪ 31 % 3D site-percolation threshold) + SuperP가 SE 이온망을 VGCF보다 1.8× 더 막음
  (σ_ionic SuperP 0.0168 < VGCF 0.0298 mS/cm).
- **이 논문(Koo 2025):** CB-wet/CB-dry(discrete CB)는 응집·점접촉·고저항·고립기공 17.72 % / CNT-dry(연속 wrapping)는
  균질·저저항(5–7 Ω·cm)·σ_s,eff 3.1×·τ↓·고립기공 2.4 % → **#275와 똑같이 "연속 도전망이 discrete를 이긴다 +
  discrete가 이온채널 막는다"를 실험 증명.**
- ★★ **그러나 이건 audit ✅#4를 이미 #275가 EXPERIMENTAL PROOF로 닫은 것과 동일한 검증** — **새 축을 더하지
  않는다.** Koo 2025와 Koo 2026(#275)은 **같은 저자·같은 컨셉의 sister 논문**이므로 **하나의 증거 라인**으로 취급
  (두 편을 독립 2점으로 세면 double-count). ⇒ **audit ✅#4 = "Koo 그룹 CNT-wrapping(2025 ESM MWCNT/anti-solvent
  + 2026 Joule SWCNT/zeta) = 우리 CBD 발견의 실험적 증명"** 한 줄로 묶어 인용. (`stage2_model_audit_vs_literature.md`는
  본 task에서 건드리지 않음 — 차후 유저 fold 시 #275 항목에 "Koo 2025 sister 동반" 각주만.)

### (b) ⚠⚠ ⚠#11 (σ_e composition-direction) — SC-vs-PC datapoint (이 논문의 진짜 NEW 기여)
- **⚠#11 질문:** σ_e가 큰 다결정(AM_P)에서 높은가(#266 σ_NCWA 13.7 ≫ σ_NCM 2.45) vs 작은 단결정(AM_S)에서
  높은가(우리 끝점가정 σ_S-single 10 > σ_P-poly 5) — 부호 반대, material-dependent.
- ★ **이 논문이 주는 것:** **SC-vs-PC를 직접 대비하지만 "전자전도(σ_e)" 축이 아니다.** 준 것 = **입자강도(SC 111.63
  ≫ PC 48.96 MPa)·균열(PC 7.8 % vs SC 0 %)·SSA(SC 0.88 > PC 0.31)·kinetics(문헌충돌, 결론 안 냄)**.
- ★ **⚠#11에 대한 정직한 평가:**
  - **이 논문은 #266의 "다결정 σ_e↑(13.7 vs 2.45)"를 뒤집는 직접 반례(단결정 σ_e 수치↑)를 주지 않는다.** SC-NCA를
    쓴 이유는 **전자/kinetics 우월이 아니라 기계적 견고성·무균열 고밀도화**다.
  - **간접 시사:** SSA(SC 0.88 > PC 0.31 = 단결정이 더 작은 입자 → 접촉수↑)는 **우리 σ_e "접촉수 지배(작은 입자↑)"
    가정과 부호 일치**(약한 지지). 단 이건 **재료 고유 σ가 아니라 기하(접촉수) 논거** → #266의 재료-고유 σ(다결정↑)와
    **다른 축이라 직접 모순 아님**(두 효과 공존 가능: 재료 고유 σ는 다결정↑ + 입자수/접촉수는 단결정↑).
  - **kinetics 문헌충돌**(Sun vs Ma vs Jung)은 **SC-vs-PC 우열이 literature-wide 미해결**임을 재확인 → 우리 audit의
    "⚠#11은 한 논문으로 결판 안 나는 material-dependent 문제" 판단을 **강화**.
  - ⇒ **⚠#11 유지.** Koo 2025는 ⚠#11에 **"σ_e 방향 결판 datapoint"가 아니라 "SC-vs-PC가 재료·기하·kinetics
    모두에서 단순하지 않다는 추가 증거"**로 들어간다. **우리 σ_e 끝점가정(σ_S > σ_P)을 재검토 항목으로 유지**하되,
    이 논문이 그 가정을 확정·반박하지는 않는다(직접 σ_e 수치 부재). **재검토는 여전히 #266(직접 σ_e 수치) 중심.**

### (c) ★ digital twin = GeoDict reconstruct (positioning 재확인)
- 이 논문 digital twin = **GeoDict 2022**(#275 GeoDict 2023, #271/#281/#286 동일 도구군)로 **FIB-SEM 토모 →
  분할 → effective σ/D/τ + PNM + BESTmicro 1D**. = **측정된 구조를 입력으로 받아 reconstruct(출력단)** =
  `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야 함"을 **NCA dry 양극 사례로 또 재확인**. 우리 DEM+MPM은
  **압력→미세구조 예측(입력단) + 소성 morphology + 접촉 σ triad + granular constriction + fracture** superset.
  (`positioning_vs_geodict.md`는 본 task에서 건드리지 않음 — 재확인 사실만 기록.)
- ★ 이식 후보(#275와 동일): (i) **voxel FV에 확산모드 → D_eff/τ 출력**(그들 σ_s,eff 3.1×·τ 1.26 ↔ 우리 contact-
  network τ frame[4] 교차검증; #281 DiffuDict); (ii) **PNM pore-side 지표**(기공 CN·connectivity·closed pore
  2.4/17.72 % = 우리 dead-SE 고립채널 기공판).

### (d) ★ SC 견고성·무균열 = 우리 MPM rigid-AM scaffold 정당화(#285 일관)
- **SC-NCA 111.63 MPa·무균열 4.0 g/cc** = 우리 MPM의 **단결정 AM_S를 rigid `--am-scaffold` 고정 obstacle로 둔 게
  옳음**(#285 "단결정=견고→압축이 무른 상으로 몰림"과 동일 정당화). 다결정 PC-NCA 7.8 % 균열 = 우리 fracture
  severe(큰 다결정 분쇄, #266 ΔP·D1 max @CAM10:0)와 방향 일치. ⚠ NCA 액체계 → σ/porosity 절대앵커 아님(역학 정성).

### (e) ⚠ 비전이 / GAP
- **anti-solvent wrapping·MWCNT vs SWCNT·dry 흑연음극·액체전해질·pouch VED** = process/재료-specific → 우리 모델 없음.
- **SC-vs-PC kinetics 문헌충돌**은 우리도 그들도 단일 스냅샷 → 공통 GAP(Phase 4 chemo-mechanical 후보).
- ★ **제3 morphology(미모델, #275와 동일):** CNT **surface-conformal wrapping** = 우리 SuperP(분산점)도 VGCF
  (interstitial 섬유)도 아닌 제3 morphology → `additives.py` `surface_conformal` future 옵션(#275 디제스트에 이미
  기록 — 여기서 중복 강조만).

### ★ 우리 우위(frame [5] 재확인)
- 그들 = **post-mortem 측정(SSRM/EIS) + digital-twin(고정 토모 미세구조, 출력단)**; 우리 DEM+MPM = **압력→미세구조→
  σ triad 예측(입력단) + 소성 morphology + voxel FV로 carbon σ_e gain·σ_ionic blocking mechanistic 정량**. 그들엔
  입자스케일 압축예측·접촉 σ triad·소성 SHAPE 없음. ⇒ frame[5] 분업 재확인.

---

## 10. 한계·전이경계 (정직하게)

- ⚠⚠ **소재계 = 단결정 NCA + 흑연 + 액체전해질 dry LIB ≠ 우리 LPSCl sulfide ASSB.** 셀 절대값(VED/GED/Q/τ/σ_s,eff/
  retention)은 **전이 불가** — Li⁺가 전해질 확산, 우리는 무전해질 접촉망. **σ/porosity 앵커는 Bazzoun/Varkey/
  Minnmann/#266/#271.**
- ⚠ **#275와 같은 증거 라인(double-count 금지):** Koo 2025(MWCNT/anti-solvent)와 Koo 2026 #275(SWCNT/zeta)는 같은
  저자·같은 컨셉 sister 논문 → CBD audit ✅#4의 **하나의 증거**로 묶음. 두 편을 독립 2점으로 세지 말 것.
- ⚠ **⚠#11에 σ_e-방향 결판 datapoint 아님:** SC-vs-PC를 **전자전도가 아니라 입자강도·SSA·(문헌충돌)kinetics**로
  다룸. 직접 σ_e 수치 없음 → #266의 "다결정 σ_e↑"를 반박/확정 못 함. ⚠#11 재검토는 #266 중심 유지.
- ⚠ **τ 두 값(EIS 1.75/1.03 vs digital-twin 2.05/1.26):** 방법 따라 다름 → 어느 정의인지 명시(우리 τ_Laplace vs
  τ_Dijkstra 선택 실증).
- ⚠ **σ_s 4.03/29.03 S/m·진밀도 4.8·c_max 37097** 등은 **NCA 문헌값** — 우리 NCM811(50 mS/cm)·#266(σ_NCWA 13.7/
  σ_NCM 2.45 mS/cm)와 단위·재료 다름 → 직접 대입 금지.
- ⚠ **2D digital twin 아님(3D FIB-SEM 토모) but 단일 스냅샷** — 시간(cycling) chemo-mechanical은 우리·그들 공통 GAP.
- ⚠ **digitized 값 주의:** Fig 1d/e(SSA·탄소함량), Fig S18a(σ_s,eff), Fig S19(effective)는 **막대그래프에서 읽은
  근사 TREND** — 본문/표 명시값(SSA 0.88/0.31, 입자강도 111.63/48.96, τ Table S1 1.75/1.03, closed pore 17.72/2.4,
  Q_vol 835, VED 858.1)만 정밀. digitized는 TREND only.

---

## 11. DB 후보 (직접 추가 안 함 — 유저 결정)

- **densification_porosity_db.csv:** ★ **추가하지 않음** — NCA/흑연/액체 LIB → porosity·σ 절대앵커 아님. (porosity
  ε CB-wet 0.14 / CNT-dry 0.083는 NCA dry 전극값, 우리 LPSCl ASSB와 무관.) 앵커는 Bazzoun/Varkey/Minnmann/#266/#271.
- **참고 기록용 수치(본 MD 표에만, DB 미추가):** SC-vs-PC 입자강도 111.63/48.96 MPa·균열 7.8/0 %·SSA 0.88/0.31;
  τ EIS 1.75/1.03 & digital-twin 2.05/1.26; closed pore 17.72/2.4 %; σ_s,eff 3.1×; Q_vol 835; VED 858.1 / GED 303.9.
- **cross-link:** #275(`docs/lit_koo2026_swcnt_sheath_thick_electrode.md`) — sister/successor. SC-vs-PC는 #266
  (`docs/lit_oh2026_bimodal_composite_cathode.md` σ_NCWA/σ_NCM) + #285(`docs/lit_hong2026_cbd_viscoelasticity_
  springback.md` 단결정 견고성)와 연결.

---

## 12. 한 줄 결론(우리 작업용)

**Koo 2025(ESM, MWCNT/anti-solvent SC-NCA dry 양극)는 #275(Joule 2026, SWCNT/zeta)의 직계 sister/precursor로
"CNT-wrapping 연속 도전층이 discrete CB를 전자·이온 양축에서 이긴다"를 똑같이 실험 증명 → audit ✅#4를 REINFORCE할 뿐
새 축 아님(double-count 금지); 진짜 NEW = (a) 단결정 SC-vs-PC 데이터(입자강도 111.63 vs 48.96 MPa·SSA 0.88 vs 0.31·
kinetics 문헌충돌)와 (b) anti-solvent salting-out 방법 — 단 SC-vs-PC를 "전자전도(σ_e)"가 아니라 기계강도·SSA로 다뤄
⚠#11(σ_e composition-direction)의 결판 datapoint는 아니고(직접 σ_e 수치 없음, #266의 다결정 σ_e↑를 반박/확정 못 함)
"SC-vs-PC가 재료·기하·kinetics 모두에서 단순치 않다"는 추가 증거로만 들어간다; digital twin은 GeoDict 2022 reconstruct
(출력단)로 positioning 재확인. ⚠ 단결정 NCA+흑연+액체 = 우리 LPSCl ASSB 아님 → 셀 절대값 전이불가, σ/porosity 앵커는
Bazzoun/Varkey/Minnmann/#266/#271 유지.**
