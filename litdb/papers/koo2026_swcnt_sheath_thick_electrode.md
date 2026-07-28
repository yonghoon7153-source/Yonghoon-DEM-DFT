# Koo 2026 (Joule 10, 102392) — 연속 SWCNT sheath가 두꺼운 dry 전극에서 초고에너지밀도 + 급속충전 (★ 우리 CBD SuperP-vs-VGCF 발견의 실험적 증명)

> slug `koo2026_swcnt_sheath_thick_electrode` · DOI `10.1016/j.joule.2026.102392` · type `FEM·digital-twin` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_koo2026_swcnt_sheath_thick_electrode.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Jin Kyo Koo†, Jaejin Lim†, Chaeyeon Ha, Yewon Kwon, Jae Kwon Seo, Hyun-seung Kim\*,
**Yong Min Lee\***, Young-Jun Kim\*, "A continuous carbon nanotube sheath enables ultrahigh
energy density and fast charging in dry-processed thick electrodes", *Joule* **10** (2026)
102392, DOI 10.1016/j.joule.2026.102392 (2026-07-15 게재, © 2026 Elsevier). †Jin Kyo Koo,
Jaejin Lim 동등기여. lead contact Young-Jun Kim. ⁷

**소속:** (1) SKKU Advanced Institute of Nano Technology (SAINT), (2) Dept. of Nano Science &
Technology, Sungkyunkwan University(Suwon) + (3) Dept. of Chemical & Biomolecular Engineering,
**Yonsei University**(Seoul 03722, = 이용민 **Digital Twin Battery Lab, DTBL**) + (4) Dept. of
Energy, Sungkyunkwan University + (5) SKKU Institute of Energy Science & Technology (SIEST).
교신 hskim0113@skku.edu(H.-s.K.) / yongmin@yonsei.ac.kr(Y.M.L.) / yjkim68@skku.edu(Y.-J.K.).
이 그룹(Yonsei DTBL, 이용민)의 **#275** — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.

**소재계:** ★ **NCMA(LiNi₀.₈Co₀.₁₅Mn₀.₀₃Al₀.₀₂O₂) Ni-rich 양극** 입자를 **단일벽 탄소나노튜브
(SWCNT, OCSiAl, 외경 ~2 nm)**로 **zeta-potential 변조**(양이온성 고분자 **PDDA**, poly(diallyl
dimethylammonium chloride))를 통해 **정전기적으로 감싸(wrapping)** 활물질 표면에 **연속·conformal
도전 sheath**(vein-like 정맥형 섬유망)를 형성. binder = **PTFE 0.3 wt%**(dry fibrillation),
도전재 별도첨가 없음(SWCNT 0.2 wt%만) → **활물질 99.7 wt%**. **dry-to-dry** 셀(dry 양극 + dry
흑연 음극) + **액체전해질**(1.15 M LiPF₆ EC:DEC:DMC 25:45:30 vol% + 1% VC + 1% LiPO₂F₂).
★★ **우리 LPSCl sulfide ASSB가 아니다 — NCMA 양극 + 흑연 음극 + 액체전해질 일반 LIB(dry-processed).**
그러나 ★ **CARBON-MORPHOLOGY 물리(연속 1D sheath가 두꺼운 전극 전도를 이기고, discrete 도전재는
이온채널을 막는다)는 소재-일반(material-general)**이라 우리 voxel CBD 발견에 **직접 전이**된다.

DB 동반 파일: `docs/data/densification_porosity_db.csv` 등 수치 DB에는 **추가하지 않음**(이 논문은
NCMA/흑연/액체 LIB → σ/porosity 절대앵커 아님 — **Bazzoun(LPSCl)/Varkey(halide)/Minnmann(LPSCl
cold-press)/#266이 앵커 담당**). 주요 수치는 본 MD 표에 정리. SI(60p) = Fig S1–S42 + Table S1–S10
+ Supplemental Note 1–6 → digital-twin 방법·zeta 조립·digital-twin VMS만 본문에 반영(전부 정독 아님).

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**기존 도전재(carbon black, 짧은 fibre)는 두꺼운 전극에서 연속 전자망을 못 만들고 이온채널까지
막는다 — 이걸 NCMA 입자 표면을 SWCNT로 "연속 conformal sheath"로 감싸 해결한다.** SWCNT가 활물질
표면을 정맥형(vein-like)으로 완전히 덮어 **균일한 전자전도망**을 만들고, 도전재를 입자 표면에
"통합(integrated active material–conductive agent)"하여 **전해질이 채우는 기공(이온채널)을 비우므로**
**전자·이온 둘 다 균일**해진다. 결과: 활물질 99.7 wt%, 밀도 ~4.0 g/cm³, 면적용량 >11 mAh/cm²(~200 µm
초후막)에서 **945 Wh/L · 310 Wh/kg**, **20분에 80% SOC** 급속충전, **500사이클 78% 유지**.

**우리 hook(가장 중요 — 이 디제스트의 심장):** 이 논문은 우리 CBD 작업의 **두 발견을 동시에 실험으로
증명**한다.
- **(전자축)** 우리는 voxel carbon-only 테스트에서 **discrete carbon(SuperP 점/짧은 VGCF)은 두꺼운
  전극을 self-percolate 못 한다(σ=0; carbon ≈6–7% 셀 ≪ 31% 3D site-percolation threshold)**를 보였다.
  #275는 정확히 **"conventional conductive additives… fail to form continuous networks"**(서론 명시)을
  문제로 지목하고 **continuous SWCNT sheath**(engineered 1D 연속망)로 해결한다 → 우리 "discrete carbon
  = gap-filler, never backbone, 두꺼운 전극엔 연속 도전망 필요" 결론의 **실험적 증명**.
- **(이온축)** 우리는 voxel σ_ionic에서 **SuperP가 SE 이온망을 VGCF보다 ~1.8× 더 막는다(σ_ionic
  SuperP 0.0168 < VGCF 0.0298 mS/cm)**를 측정했다. #275는 **"[conventional additives] obstruct
  ion-transport channels"**(서론 명시)이라고 정확히 같은 문제를 말하고, sheath를 **활물질 표면에 통합**해
  **기공(이온채널)을 비워** 이온수송을 살린다(digital-twin: SWCNT-dry 유효확산계수 2.5× ↑, 균일 Li⁺).
  → 우리 "discrete carbon obstructs ion channels" 결론의 **실험적 증명**.
⇒ **#275 = 우리 voxel CBD 발견(전자: 연속 1D 필요 + 이온: discrete가 채널 막음)의 EXPERIMENTAL PROOF.**
추가로 **SWCNT conformal sheath = 우리가 모델하지 않는 제3의 도전재 morphology**(표면-순응형, 우리
SuperP=분산점 / VGCF=interstitial 섬유 둘 다 아님) — **두꺼운 전극에서 실제로 이기는 morphology** →
`scripts/additives.py`의 future 옵션 + 정직한 한계로 명시. 그들 **3D digital twin = 우리 voxel/Phase-4**
접근(GeoDict effective + COMSOL식 1D 방전) — 같은 그룹 #281/#286의 반복 digital-twin 활용.

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- **두꺼운 전극(thick electrode)이 부피에너지밀도(VED)·급속충전의 핵심.** 두꺼운 전극은 주어진 용량에
  필요한 적층(stacked layer) 수를 줄여 **비활성 부품(separator·집전체) 분율↓ → VED↑**. mobility 응용
  (EV·항공)에서는 **VED + 급속충전이 가장 중요한 지표**(설치공간 제한 + 잦은 급속 재충전).
- **활물질 함량 최대화 = 용량은 활물질에서만 나오므로.** 그러나 기계·전기 무결성에 도전재+binder 필수.
  이들은 활물질보다 진밀도 낮음 → 과량이면 전극밀도↓ → 전체 VED↓. ⇒ **고(高)활물질 두꺼운 전극 설계가
  실용 LIB의 가장 어려운 목표.**
- **❗ 습식(wet slurry) 공정의 한계 = 건조 중 binder migration.** 슬러리는 용매제거(건조) 필요 →
  **용매가 증발하며 binder + 사전분산된 도전 carbon이 재분포(migration)** → **전자전도 불균일 + 국소
  전기화학반응 + (두꺼우면) 내부 크랙**.
- **★ 건식(dry) 공정 = 용매 없음 → binder migration 제거.** 통상 **PTFE fibrillation binder**(용매·건조
  불필요, 강한 입자-입자 접착) 사용 → 두껍고 고에너지 전극에 유리. **❗ 그러나 dry도 고유 난제:
  도전 carbon의 응집(agglomeration)** — 활물질·carbon·binder를 kneading/extrusion에서 동시 혼합해야 해
  **균질 분산이 어려움**(VED 향상의 주요 병목). + **PTFE가 음극에 부적합하다는 통념**(전해질환원/탈불소화).
- ★ **본 연구(명시):** **습식·건식 양쪽의 한계를 동시에 푸는 전략 — SWCNT로 NCMA 입자를 감싸기.**
  CNT를 통상 슬러리에 넣으려면 큰 용매량 필요(고형분↓·두꺼운 전극화 방해) → 대신 **SWCNT를 NCMA에
  계면상호작용으로 직접 부착(wrapping)** → 고형분·두꺼운 전극 + 용매-free 공정과 양립. NCMA가 SWCNT로
  균일하게 감싸지면 **SWCNT가 본질적(intrinsic) 도전망으로 기능 → 별도 혼합 도전재 불필요**. + **dry
  공정에서 음극 PTFE binder 호환성도 검증**(dry-to-dry full cell).
- **★ 통합 활물질–도전재(integrated active material–conductive agent) 아키텍처:** 통상 도전재(대량
  첨가해도 연속망을 못 이루고 이온수송채널을 막음)와 달리, **SWCNT sheath는 활물질 표면을 따라 선형·
  conformal 도전 프레임을 제공** → **입자간 공간(interparticle space)을 통한 효율적 Li⁺ 수송**과
  **전극 전체의 일관된 전자전도**를 동시 보장 → 고에너지 두꺼운 전극의 급속충전 강화.

**약어:** SWCNT = single-walled carbon nanotube(단일벽 CNT, 외경 ~2 nm, 1D). NCMA = Ni-rich 양극
LiNi₀.₈Co₀.₁₅Mn₀.₀₃Al₀.₀₂O₂. PDDA = poly(diallyl dimethylammonium chloride)(양이온성 고분자, ζ
중화제). CB = carbon black(carbon black, 0D, 우리 SuperP 대응). CBD = carbon-binder domain(CB-wet에서
CB+PVDF 복합상). VED = volumetric energy density(부피에너지밀도). GED = gravimetric ED(중량에너지밀도).
PNM = pore network model(기공망 모델). FIB-SEM = focused-ion-beam SEM tomography. KPFM = Kelvin
probe force microscopy(켈빈 프로브, work function = SOC 균질도). DRT = distribution of relaxation
times. SAICAS = surface and interfacial cutting analysis(접착력). VMS = von Mises stress.
**CB-wet / CB-dry / SWCNT-wet / SWCNT-dry** = 4종 전극 코드(carbon source × 공정).

---

## 2. SWCNT-NCMA 자발 조립 메커니즘 — zeta-potential 변조 (Fig 1, §"Zeta potential modulation")

★ 핵심 발견 1: **반대전하 정전인력으로 SWCNT가 NCMA를 conformal하게 감싼다.**

**zeta-potential 4단계 조립(Fig 1A 모식 + Fig 1B 측정):**

| 단계 | 입자/물질 | zeta potential (mV) | 의미 |
|---|---|---|---|
| ① 출발 | bare NCMA(Ni-rich) | **−33.8** | 음전하 표면 |
| ① 출발 | bare SWCNT (well-dispersed) | **−35.0** | 음전하 → NCMA와 정전기 **반발**(직접 못 붙음) |
| ② 양이온 고분자 코팅 | PDDA-coated NCMA | **+14.2** (목표 +14) | PDDA(양이온)로 표면전하 **반전** |
| ③ SWCNT 부착 | SWCNT-coated NCMA | **≈ −1.92**(≈ −1.9) | 음전하 SWCNT가 양전하 NCMA에 강한 정전인력으로 부착 → **거의 중성** = **완전 coverage·정전기 자가조립 완료** |

- **물리:** NCMA(−33.8)와 SWCNT(−35.0)는 둘 다 음전하 → 그냥 섞으면 반발. **PDDA로 NCMA를 +14.2 mV로
  반전** → 음전하 SWCNT가 정전인력으로 끌려와 표면을 덮음 → 합성물 zeta가 **−1.92 mV(near-neutral)** =
  표면전하 중화 = **연속·완전 coating**의 지표(전하가 상쇄되었다 = SWCNT가 양전하 자리를 모두 덮었다).
- **(SI Fig S3)** bare SWCNT ζ = −3.4 mV(잘 안 분산, 응집) → **functionalized SWCNT(f-SWCNT) ζ = −35 mV**
  (정전기 안정 분산). 즉 SWCNT 자체도 분산을 위해 표면개질됨. (SI Note S1: SWCNT ink = OCSiAl SWCNT
  0.04 wt% in NMP + PVP:PAN 1:1 분산제 0.02 wt%, 고전단 8000 rpm 1h → 1500 bar 고압균질기 15회.)

**coating 검증(SEM/TEM/AFM/EDS/Raman/XRD):**
- **FE-SEM·HR-TEM·AFM(Fig 1C–E + SI Fig S4,S5):** **bare NCMA = 매끈한 표면**(응집 1차입자로 구성,
  Fig 1C, E₁). **SWCNT-wrapped NCMA = 2차입자 전체를 덮는 conformal nanotube 층**(Fig 1D, E₂; SI Fig
  S4 = 무작위 9개 입자 모두 균일 wrapping). ★ **"vein-like fibrous network reminiscent of melon peels"**
  (멜론 껍질의 정맥형 섬유망) = sheath의 핵심 형태 서술.
- **EDS(SI Fig S5C):** SWCNT의 **탄소(C)가 전이금속(Ni·Co·Mn·Al)과 co-localized 균질 분포** → 표면
  전체에 SWCNT 균일.
- **Raman(Fig 1F):** SWCNT-NCMA만 **radial breathing modes(~150 cm⁻¹) + 높은 G/D 비** → SWCNT 특징 확인.
  **고전단 슬러리 혼합(>2000 rpm) 후에도 SWCNT 신호 유지**(wet 공정에서도 부착 견고).
- **XRD(SI Fig S6):** NCMA 본연의 층상구조 wrapping 후에도 **유지**(불순물상·구조변화 없음) = 조립이
  활물질을 손상시키지 않음.

**분말 전기전도(Fig 2B + SI Fig S7):**
- **(NCMA+CB) 99:1 분말:** 압력↑로 전도↑, 최대압축에서 **≈ 0.06 S/cm**.
- **SWCNT-wrapped NCMA 분말:** **≈ 0.20 S/cm로 일관되게 높음(>3배)** → conformal CNT 도전경로 덕.
- (SI Fig S7) SWCNT loading 0.001→0.006 g/3g NCMA로 분말전도 단조↑(0.005–0.006 g에서 ~0.18–0.20 S/cm).
  → 적은 SWCNT로도 CB 1 wt%를 능가.

---

## 3. SWCNT-dry 전극 = 두꺼운 전극의 균질 활용 (Fig 2, §"SWCNT-dry electrode design")

★ 핵심 발견 2: **SWCNT sheath + 최소 PTFE → 전자·이온 균질 + 초후막(11.4 mAh/cm²) 제작 가능.**

**전자/이온 도전망 비교(Fig 2A 모식):**
- **CB-wet:** 응집된 carbon black + PVDF binder 층이 NCMA를 덮음 → **전자·Li⁺ 수송 모두 방해**(heterogeneous
  electronic/ionic conduction). CBD(carbon-binder domain)가 bulky·tortuous → **Li⁺가 전해질 속을 가야 하는데
  CBD가 막음**.
- **SWCNT-dry:** **NCMA에 균일 SWCNT coating + fibrillated PTFE** → **homogeneous electronic/ionic conduction**.
  도전재가 표면에 통합되어 **기공(이온채널)을 안 막음**.

**PTFE 함량 최적화(SI Fig S8):** SWCNT-dry를 PTFE **0.1/0.3/0.5 wt%**로 제작·전기화학평가 →
★ **0.3 wt%가 최적**(C-rate 전반 분극 최소). 0.1 wt%는 통상 PVDF 습식엔 부족하나 **PTFE fibrillation은
0.3 wt%로 충분한 응집력**. (SI Fig S9: 0.3 wt% PVDF 습식은 folding 시 delamination → PTFE의 우월한
접착. SI Fig S10: 0.3 wt% PTFE dry는 large-area 시트 robust.)

**전극밀도(Fig 3 본문):** 최소 binder(0.3 wt% PTFE) → **SWCNT-dry 밀도 ρ = ~4.0 g/cm³** (상용 CB-wet
3.6 g/cm³보다 훨씬 높음) → 고에너지 조건.

**저항 vs 면적용량(Fig 2C):** Q_areal = 5 / 6.5 / 8.5 mAh/cm²에서 부피저항(volumetric resistance).
- ★ **CB-wet: Q_areal↑ → 저항 급증(10 → 40 Ω·cm)** + **균열(cracks) 발생**.
- ★ **SWCNT-dry: 낮고 안정한 5–10 Ω·cm 유지**(면적용량 무관) → **잘 연결된 SWCNT 도전망이 두꺼운
  전극에서도 균일 전류분포**.

**rate capability(half-cell, Fig 2D):** Q_areal 5/6.5/8.5 mAh/cm²에서 SWCNT-dry가 **전 C-rate에서
CB-wet 능가**(SWCNT가 도전재 적음에도). 특히 고율에서 차이 큼.

**초후막 제작(SI Fig S12):** CB-wet은 **Q_areal ~10 mAh/cm² 시도 시 건조 후 심한 균열 → 셀조립 불가**.
★ **SWCNT-dry는 Q_areal = 11.4 mAh/cm²(>11 mAh/cm²)도 성공 제작** → 초기방전 **215 mAh/g**(NCMA 실용
용량 4.3 V cutoff 근접). = **SWCNT 도전망이 고면적부하에서도 반응구배를 완화**.

**KPFM(work function = SOC 균질도, Fig 2E–J):** 고부하(8.5 mAh/cm²) 전극 1C 충전 후 입자별 work function.
- ★ **CB-wet = 입자간 work function 큰 편차(P1–P3 분산, 넓은 분포 5.8–6.1 eV) = Heterogeneous SOC**
  (입자마다 리튬화 정도 다름 = 불균일 반응).
- ★ **SWCNT-dry = 좁은 단일 peak(5.95 eV 중심) = Homogeneous SOC**(균일 리튬화) → **연속 SWCNT
  도전망이 균일 전류분포 보장**.

**ex-situ XRD(SI Fig S13):** 4.1 V(H2→H3 전이 전)에서 둘 다 H2상 단일. **4.4 V(전이 후): CB-wet =
잔여 H2 peak(느린 상전이) / SWCNT-dry = 더 완전한 H3상** → CB-wet의 느린 상전이 = 불균일 전류분포 +
구조변형. SWCNT-dry는 반응 균질 → 완전 상전이.

---

## 4. 구조·기계·고에너지밀도 설계 (Fig 3, §"Design strategy to maximize VED")

★ 핵심 발견 3: **4종 전극(CB-dry/CB-wet/SWCNT-wet/SWCNT-dry) 체계 비교 → SWCNT-dry가 최고밀도·무손상·
접착·전기화학 안정 모두 1위.**

**4종 전극 설계(commercial-level Q_areal ≈ 5 mAh/cm², m_areal ≈ 23 mg/cm²):**

| 전극 | 조성(wt%) | binder | 밀도 ρ (g/cm³) | 비고 |
|---|---|---|---|---|
| **CB-wet** | NCMA:CB:PVDF = **98:1:1** | PVDF | **3.6** | 통상 습식 baseline |
| **CB-dry** | NCMA:CB:PTFE = **98:1:1** | PTFE | 3.6 | 건식 + CB |
| **SWCNT-wet** | SWCNT-NCMA:CB:PVDF = **99(98.8:0.2):0:1** | PVDF | **3.8** | wrapped + 습식 |
| ★ **SWCNT-dry** | SWCNT-NCMA:CB:PTFE = **99.7(99.5:0.2):0:0.3** | PTFE | ★ **4.0** | wrapped + 건식(최고밀도) |

(SWCNT-dry = 활물질 99.7 wt% = SWCNT-NCMA 99.7, 그중 SWCNT 0.2 + PTFE 0.3. **별도 도전재 0**.)

**단면 SEM(Fig 3A–D, 저배율 A₁–D₁ / 고배율 A₂–D₂,A₃–D₃):**
- ★ **CB-dry(A): 심한 균열(cracks)** + CB 응집으로 CB↔NCMA **접착 불량(poor contact)**.
- **CB-wet(B):** 두께 보존·합리적 입자접촉이나 **carbon black point-contact**(점접촉만).
- **SWCNT-wet(C):** 밀도 3.8(CB 제거로↑)이나 open pore 잔존. **SWCNT가 NCMA에 conformal 부착, 도전망
  형성(Wrap-around SWCNT layer)**.
- ★ **SWCNT-dry(D): 최고밀도 4.0, 구조손상 없음**(PTFE fibrillation 효과적 + NCMA가 SWCNT로 균일 sheath).
  고배율: **Wrap-around SWCNT layer + PTFE fibrillation**(D₃).

**접착력(SAICAS, Fig 3E,F):** ★ **SWCNT-dry(0.3 wt% PTFE) 평균 접착력 0.47 N > CB-wet(1.0 wt% PVDF)
0.43 N** → **나노화 CB 부재로 PTFE가 SWCNT-wrapped NCMA를 선택적으로 결합**, 최소 binder로 더 강한
기계무결성. (EDS: CB·binder 응집이 CB계엔 있고 SWCNT계엔 억제 — SI Fig S14.)

**DC-IR(HPPC, Fig 3G):** 직렬저항 순서 **CB-dry > CB-wet > SWCNT-wet > SWCNT-dry**. SWCNT계가 SOC
전범위에서 현저히 낮음(개선된 전자전도). (SWCNT-dry ~12 Ω, CB-dry ~20 Ω.)

**half-cell cycling·rate(Fig 3H,I):**
- (Fig 3H, 2.75–4.3 V, 1C, RT, 1C = 5 mA/cm²) **부피용량 SWCNT-dry > SWCNT-wet > CB-wet > CB-dry**.
  CB계 초기 679/710 mAh/cm³ → 30사이클 후 **58.3/68.3% 유지**(급감). SWCNT계 762/820 → **84.3/89.6% 유지**.
- (Fig 3I, rate) 고율(>2C)에서 차이 극명: 용량유지 **SWCNT-dry 87.5%@2C / 21.4%@5C vs CB-wet 70.2%/11.2%**.
- ⇒ **SWCNT-dry = 최고 VED + 기계robustness + 전기화학 안정 동시 달성.**

---

## 5. 3D digital-twin 시뮬레이션 — SWCNT-dry 우월성 검증 (Fig 4, §"Digital-twin simulation") ★ 우리 voxel/Phase-4 대응

★ 핵심 발견 4: **3D digital twin이 SWCNT-dry의 기공망·유효확산·전자/이온 균질성을 정량 검증.**

**방법(SI Note S2–S4):**
- **(a) FIB-SEM tomography(SI Note S2):** Xe⁺ plasma FIB(Helios 5)로 시편 → Ga⁺ FIB-SEM(crossbeam 550)
  **serial milling 820장**. milling interval **32.5 nm**, pixel **31.01 nm(CB-wet)/37.22 nm(SWCNT-dry)**
  (≤40 nm voxel), 3D domain **33×31×27 µm³**. FFT+non-local means 필터 → gray-value thresholding +
  watershed + **CNN(U-net) 분할**. 재구성 부피분율 vs 이론값 상대오차 **6.56%(CB-wet)/5.45%(SWCNT-dry)**.
  도구 = **GeoDict 2023(Math2Market)**.
- **(b) PNM(SI Note S3):** 분할 3D label에 **marker-based watershed**로 개별 기공·연결 식별 →
  ball-and-stick. 등가반경 r_eq(V_pore=4/3·π·r_eq³), **coordination number**(한 기공에 연결된 기공 수),
  **pore connectivity matrix**(대칭, 대각=0; 인덱스=Cartesian 좌표 → bandwidth↑ = 장거리 연결). MATLAB +
  open-source(Rabbani 2014).
- **(c) 전기화학 모델(SI Note S4):** **2C-rate 방전**을 GeoDict 2023으로(재구성 3D 미세구조 + 가상 Cu
  집전체·Li foil·separator·Al 집전체). 지배방정식 = **전하보존+전기중성·물질보존·Fick 법칙·Ohm 법칙·
  Butler-Volmer**(Table S5). OCP = 0.01C 방전곡선, σ_s(활물질 전자전도) 실측, c_max = 측정용량(213 mAh/g)
  ·진밀도(4.8 g/cm³)·Faraday로 계산. 전해질 = EC/EMC 3:7 + 1.15 M LiPF₆ @298.15 K(문헌). D_s·BV 상수 문헌.
  → 방전곡선 시뮬 vs 실측 **상대오차 ~2.15%**(검증됨).

**기공구조 정량(Fig 4A–C):**
- **pore connectivity matrix(Fig 4A CB-wet / 4B SWCNT-dry):** ★ **SWCNT-dry의 bandwidth가 CB-wet보다
  넓음** → **장거리 연결 likelihood↑**. (SI Fig S22C: SWCNT-dry std **30% 높음** = 더 넓은 기공연결.)
- **closed pore % + tortuosity(Fig 4C):** ★ **closed pore(bulk 기공망에서 고립 → Li⁺ 수송 기여 못 함)
  부피분율 CB-wet이 SWCNT-dry의 2배**. **tortuosity factor CB-wet 2.31 vs SWCNT-dry 1.28**(SWCNT-dry가
  훨씬 덜 우회).
- (SI Fig S22A,B) SWCNT-dry는 등가반경 **12% 더 큼** + coordination number **9% 더 높음** → 더 좋은 기공구조.

**유효확산계수(Fig 4D) — ★ 핵심 수치:**
- **유효확산 D_eff = D_int · ε/τ** (Equation 1; ε=기공률, τ=tortuosity; eff=유효, int=본연(bulk)).
- ★★ **SWCNT-dry D_eff ≈ 2.5×10⁻¹¹ m²/s vs CB-wet ≈ 1.0×10⁻¹¹ m²/s = SWCNT-dry가 거의 2.5배 높음.**
  (낮은 tortuosity 1.28 + 높은 기공률 덕.) → "**2.5-fold higher lithium-ion diffusivity**" 헤드라인.

**전류밀도·Li⁺ 농도 분포(Fig 4E–G + 4H,I, 2C 방전 종료):**
- **이온 전류밀도(Fig 4E):** ★ **SWCNT-dry = 균일 전류밀도 + 전극 바닥(집전체측)에서도 적정 농도 유지** /
  **CB-wet = 제한된 percolation 경로에 집중 + 급강하**(상부서도).
- **전해질 농도구배(Fig 4H):** ★ **CB-wet = 두께 방향 큰 농도구배**(separator측 1.8 M → 바닥 <0.2 M
  고갈, 구배 29.7 mM/µm) / **SWCNT-dry = 균일 ~0.9 M**(구배 ~4배 낮은 7.8 mM/µm). → 잘 발달된 기공망이
  하부까지 Li⁺ 공급.
- **고체 Li⁺ 농도(Fig 4G,I):** ★ **SWCNT-dry = 두께 전반 균일 고체 Li⁺**(균일·높음) / **CB-wet = 표면
  집중 + 바닥으로 확장**(반응 불균질, Li 확산/이동이 심하게 방해됨). → SWCNT-dry의 균일 반응 = 더 낮은
  과전압 + 높은 방전용량(급속방전에서).
- **특정접촉면적(SI Fig S23,S24):** SWCNT-dry는 PTFE 고유 fibril 형태 덕에 **활물질↔binder 접촉면적
  64% 더 낮음**(점접촉 최소) + **활물질↔기공 접촉(반응 site) 15% 더 높음**(SI Fig S24) → 균일 flux +
  활물질 표면 SWCNT 전자전도 → 전기화학 성능↑.

**electrochemo-mechanical(VMS) digital twin(SI Note S5, Fig S28):** 재구성 3D + Li⁺ 농도의존 strain/stress
(이전 digital-twin 프레임). **NCMA: Young's modulus 105 GPa, Poisson 0.27(NCM811 값 채용), 3.4 vol% 팽창**
가정, 모든 상 탄성(소성 미포함, preliminary). SoL 149 mAh/g(CB-wet cutoff 도달점)에서:
- ★ **SWCNT-dry = 균일·낮은 von Mises stress / CB-wet = 강한 국소 응력**(불균일 Li⁺ intercalation 탓).
- VMS > 0.50/0.75/1.00/1.25 GPa 부피분율: **모든 threshold에서 SWCNT-dry가 일관되게 낮음**, >1.25 GPa
  분율은 **CB-wet의 ~절반**. → 균일 반응동역학 = 균일·완만한 기계변형 = 균열 억제(Fig 6 degradation과 연결).

⇒ **digital twin 결론: SWCNT-dry = 우월한 Li⁺/e⁻ 수송(2.5× D_eff, τ 1.28 vs 2.31, 균일 농도/전류/응력)
→ 두꺼운 전극 급속충전·장수명의 미세구조적 근거.**

---

## 6. 장기 cycling·degradation·full cell·pouch (Fig 5–8)

★ 핵심 발견 5: **균질 SWCNT 도전망 = 균일 팽창/수축 → 균열 억제 → 장수명 + 945 Wh/L pouch.**

**full-cell cycling(SWCNT-dry‖Gr-wet, 96:1:1.5:1.5 흑연음극, ρ~1.4 g/cm³, Q_areal 5.5 mAh/cm², N/P 1.1;
1C/1C, Fig 5A,B):** 4종 전극 비교.
- ★ **SWCNT-dry = 300사이클 81% 유지 + 평균 CE 99.64%(최고)** vs CB-wet 72.7%(CE 99.43). 초기 부피용량
  **SWCNT-dry 792 mAh/cm³**(>CB-wet 685, +15.6%). dry 단독(robust 도전망 없이)은 장기 불충분(CB-dry 최악).

**SSRM 저항분포(300사이클 후, Fig 5D–I):** scanning spreading resistance microscopy로 단면 저항맵.
- **사이클 전:** CB계 = 불균일 저항(CB 응집부 저저항 + 고저항 영역) / SWCNT계 = 균질(CB계의 ~1/10 저항).
- ★ **300사이클 후:** **CB계 = 내부저항 폭증(최대 10⁴ GΩ)** — microcracking + 부피변화 전기적 고립.
  **SWCNT-dry = robust**(SWCNT망 + PTFE binder 수송 유지, 넓은 면적 저저항 유지).
- 저항 히스토그램(Fig 5H): ★ **CB-wet 평균 6.62 GΩ(넓은 분포) vs SWCNT-dry 0.6 GΩ(좁은 저저항 집중)**.
  line profile(Fig 5I): CB-wet 입자 = 심한 내부손상 / SWCNT-dry 입자 = 균일 저저항.

**구조안정성(300사이클 후 FIB-SEM·HAADF-STEM·EELS, Fig 6):**
- **CB-wet(heterogeneous degradation):** 1차입자 **두꺼운 rock-salt상 ~9 nm**(표면→내부), 심한 입계균열·
  입자고립. EELS = 표면 산소손실 + 전이금속 환원(NiF 형성, TM dissolution). **불균일 부피변화 → 입자 고립
  → 후막 비활성 rock-salt → cascade 부반응**(Fig 6E₁).
- ★ **SWCNT-dry(homogeneous degradation):** **얇은 rock-salt ~2–4 nm**, 내부 층상구조 무결, 균열 적음.
  ★ **연속·균질 SWCNT 도전망이 1차입자의 동기적(synchronous) 팽창·수축 유도** → 초기 입계균열 억제 →
  cascade 차단(Fig 6E₂). = 균일 전자전도 = 균일 반응 = 균일 기계거동.

**극한조건 안정성(SI Note S6, Fig S29–S33):** CB-wet의 응집 CB는 큰 비표면적 → 고전압(>4.4 V)·고온
(>60°C)에서 전해질 부반응·가스발생. **SWCNT-wrapped NCMA의 BET 비표면적 = pristine NCMA와 유사**
(SI Fig S30) → 전해질 노출 최소 → 가스발생·TM dissolution 억제. in-situ 압력셀(4.6 V, 60°C): CB-wet
>4.4 V 급격 압력증가 vs SWCNT-dry 완만. 60°C 1C cycling: CB-wet 150사이클 후 용량 0 vs SWCNT-dry
~120 mAh/g 안정.

**급속충전 full cell(SWCNT-dry‖Gr-dry, Fig 7):** 음극도 dry화(흑연 PTFE binder, inactive <0.5 wt% =
통상 3–4 wt% SBR/CMC 대비 큰 개선, 활물질 99.5 wt%, ρ 1.65 g/cm³). dry-to-dry.
- (Fig 7A,B 전압곡선) **CB-wet‖Gr-wet은 첫 사이클부터 큰 과전압 + 3C 고율서 4.3 V cutoff 조기도달** /
  **SWCNT-dry‖Gr-dry는 과전압 작음**(in-situ DRT: SEI·확산 저항 둘 다 SWCNT-dry서 충전 중 억제).
- ★ **(Fig 7C) 3C 충전 CC mode 도달 SOC: SWCNT-dry 92% vs CB-wet 65%**(CB-wet은 도금위험으로 CV 의존).
  (Fig 7D,E SOC-시간) ★ **SWCNT-dry = 20분에 80% SOC(3C, 도금 없음) / CB-wet = 30분**.
- (Fig 7F,G 에너지 vs 시간) **3C에서 SWCNT-dry가 GED·VED 모두 상회** + (Fig 7H 10 Ah 모식) 셀레벨
  GED/VED.

**10 Ah pouch·고에너지밀도(Fig 7F–I 본문 + Fig 8 + Table S9,S10):**
- ★★ **SWCNT-dry‖Gr-dry 10 Ah pouch: VED 945 Wh/L · GED 315 Wh/kg** (Q_areal 5 mAh/cm²; Table S10
  계산: 1st 방전 213.11 mAh/g, nominal 3.71 V, 셀용량 10.34 Ah, 셀부피 0.405 L, 셀무게 121.64 g).
  20분 급속충전(3C, 80% SOC) 후 **conventional 대비 +33% 에너지 유지**.
- (Fig 8A 레이더 / 8B,C VED·GED vs cycle / 8D VED vs Q_areal / 8E 산업로드맵 대비) **SWCNT-dry‖Gr-dry =
  현행 EV 셀(Ref 1–4: KIA EV6/Audi e-tron/Tesla M3/Samsung INR21700) 능가 + 2030 미래로드맵(Ref 5–10:
  prismatic/cylindrical/pouch) 수준의 945 Wh/L 달성**(Fig 8E: this work 945 = 최고).
- **(Table S9)** SWCNT-dry 양극: 두께 58 µm, loading 23.32 mg/cm², 밀도 4.0; Gr-dry 음극: 두께 98 µm,
  loading 16.26, 밀도 1.65; N/P 1.1; coin Φ12/Φ14, pouch 40×50/44×54 mm.
- **(Table S10)** 비교: CB-wet‖Gr/SiC-wet(400/500/600 mAh/g 음극) 787/794.6/885.6 Wh/L vs **SWCNT-dry‖
  Gr-dry 944.6 Wh/L**(VED 최고) + GED 315.2(최고). 고용량 Si/C 음극(Gr/SiC) 블렌드는 낮은 ICE·높은
  리튬화 전위로 trade-off → SWCNT-dry가 둘 다(VED+급속충전) 이김.

**결론(p.13):** dry 공정의 도전재 응집 + 음극 PTFE 통념을 zeta-modulation SWCNT wrapping + roll-to-roll
dry로 해결 → 활물질 99.7 wt% + ρ 4.0 g/cm³ + 945 Wh/L + 80% SOC@20분 + 78%@500cyc → 차세대 고에너지
급속충전 LIB의 실용 경로.

---

## 7. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.3):** ★ 조립 핵심 — (A) **zeta 4단계 wrapping 모식**, (B) **zeta 측정**(NCMA −33.8 / PDDA-NCMA
  +14.2 / SWCNT −35.0 / SWCNT-NCMA −1.92 mV). (C,D) FE-SEM(bare 매끈 vs SWCNT-wrapped). (E₁,E₂) AFM.
  (F) Raman(SWCNT RBM+G/D). → ★ **continuous conformal sheath의 정전기 조립 증거**(우리가 모델 안 하는
  surface-conformal morphology의 실제 형성 메커니즘).
- **Fig 2 (p.4):** ★ 전자/이온 균질 — (A) **CB-wet(응집 CBD가 전자·이온 막음) vs SWCNT-dry(통합 sheath →
  homogeneous) 모식**. (B) **분말전도**(CB+NCMA 0.06 vs SWCNT-NCMA 0.20 S/cm). (C) **저항 vs Q_areal**
  (CB-wet 10→40 Ω·cm + 균열 vs SWCNT-dry 5–10 안정). (D) **rate**. (E–J) **KPFM work function**(CB-wet
  heterogeneous SOC 넓은 분포 vs SWCNT-dry homogeneous 5.95 eV 단일 peak). → ★ **"discrete carbon이
  두꺼운 전극서 불균일·고저항, 연속 sheath가 균일·저저항" = 우리 전자축 발견의 실험 증명**.
- **Fig 3 (p.5):** ★ 4종 전극 + VED — (A–D) **단면 SEM**(CB-dry 균열/CB-wet 점접촉/SWCNT-wet wrap/
  SWCNT-dry 밀도4.0 무손상). (E,F) **SAICAS 접착**(SWCNT-dry 0.47 N > CB-wet 0.43, binder 1/3로). (G)
  **DC-IR**(SWCNT-dry 최저). (H) **cycling**(SWCNT-dry 84–90%@30cyc vs CB 58–68). (I) **rate**. → ★
  **4종 계통비교로 "carbon source(CB vs SWCNT) × 공정(wet vs dry)"의 영향 분리** = 우리 SuperP vs VGCF
  비교의 실험 확장판(우리는 carbon TYPE만, 그들은 type×process).
- **Fig 4 (p.7):** ★★ digital twin = 우리 voxel/Phase-4 — (A,B) **pore connectivity matrix**(SWCNT-dry
  bandwidth↑). (C) **closed pore %(CB-wet 2×) + tortuosity(2.31 vs 1.28)**. (D) **유효확산
  D_eff(SWCNT-dry 2.5× = 2.5e-11 vs 1.0e-11 m²/s)**. (E–G) **3D 전류밀도·전해질·고체Li⁺**. (H,I)
  **두께-SOC 농도맵**(CB-wet 큰 구배 vs SWCNT-dry 균일). → ★ **그들 GeoDict effective(τ/D_eff) +
  COMSOL식 1D 방전 = 우리 voxel FV → PyBaMM Phase-4의 published blueprint**; 그들 2.5× D_eff ↔ 우리
  유효-transport 추출.
- **Fig 5 (p.9):** 장기 + SSRM — (A,B) **300cyc cycling/CE**(SWCNT-dry 81%·CE99.64 vs CB-wet 72.7·99.43).
  (C) **Nyquist**(SWCNT-dry 저항증가 작음). (D–G) **SSRM 저항맵**(전/후, SWCNT-dry 균질·저저항 유지). (H)
  **저항 히스토그램**(CB-wet 6.62 vs SWCNT-dry 0.6 GΩ). (I) **line profile**. → 균질 도전망 = 장기 안정.
- **Fig 6 (p.11):** degradation 기전 — (A–D) **HAADF-STEM rock-salt**(CB-wet ~9 nm vs SWCNT-dry ~2–4 nm).
  (E₁,E₂) **구조붕괴 cascade 모식**(CB-wet 입자고립→cascade vs SWCNT-dry 동기팽창→억제). (C,D,H,I) **EELS**
  (산소손실·TM환원). → 연속 도전망 = 균일 반응 = 균일 기계거동 = 균열 억제(우리 fracture/coverage 대응).
- **Fig 7 (p.13):** 급속충전 full cell — (A,B) **전압곡선**. (C) **CC/CV mode SOC**(3C SWCNT-dry 92% vs
  CB-wet 65%). (D,E) **SOC-시간**(80% SOC: SWCNT-dry 20분 vs 30분). (F,G) **에너지 vs 시간**. (H) **10 Ah
  모식**(945 Wh/L). (I) **cycling**. → dry-to-dry 셀 성능.
- **Fig 8 (p.14):** 고에너지 — (A) **5축 레이더**(4종). (B,C) **VED/GED vs cycle**. (D) **VED vs Q_areal**.
  (E) **산업로드맵 대비 막대**(this work 945 = 최고). → ★ **DOD/레이더 시각화**(우리 predictor 출력 후보,
  #281과 동일).

### SI Figures + Notes (정독: digital-twin 방법 + zeta 조립 위주)
- **Fig S1:** SWCNT TEM(외경 ~2 nm). **Fig S2:** SWCNT ink 고압균질기(15회 1500 bar). **Fig S3:** ★
  bare SWCNT ζ −3.4 → f-SWCNT −35 mV(분산 안정). **Fig S4:** FE-SEM 9개 입자 균일 wrapping. **Fig S5:**
  TEM + EDS(C가 Ni/Co/Mn/Al과 co-localized). **Fig S6:** XRD(wrapping 후 구조 유지). **Fig S7:** ★ SWCNT
  loading 0.001–0.006 g/3g NCMA 분말전도(~0.18–0.20 S/cm, CB 1 wt% 능가). **Fig S8:** ★ PTFE 0.1/0.3/0.5
  wt% rate(0.3 최적). **Fig S9:** PVDF 0.3/0.5/1.0 folding(delamination). **Fig S10:** dry 시트 제작 +
  folding(PTFE robust). **Fig S11:** 고면적부하 6.5/8.5 mAh/cm² rate. **Fig S12:** ★ CB-wet 10 mAh/cm²
  균열/delamination vs SWCNT-dry 11.4 mAh/cm² 성공(215.2 mAh/g). **Fig S13:** ex-situ XRD H2/H3. **Fig
  S17–S19:** ★ FIB-SEM tomography(820장) + U-net 분할 + 3D 재구성(부피분율 오차 6.56/5.45%). **Fig S20:**
  CBD vs PTFE fibril XY 투영분포. **Fig S21:** ★ PNM(watershed·ball-stick·coordination·connectivity
  matrix). **Fig S22:** SWCNT-dry 등가반경 +12%·coord +9%·connectivity std +30%. **Fig S23,S24:** SWCNT-dry
  특정접촉면적 활물질-binder −64%·활물질-pore +15%. **Fig S25:** OCP(0.01C) + 2C 방전 시뮬 vs 실측
  (오차 2.15%). **Fig S28:** ★ VMS digital twin(NCM811 E=105 GPa·ν=0.27·3.4 vol% 팽창; SWCNT-dry 균일
  응력, >1.25 GPa 분율 CB-wet의 절반). **Fig S29–S33:** 극한조건(LSV·BET·in-situ 압력·TOF-SIMS·ICP-OES).
  **Fig S35:** ex-situ XRD lattice. **Fig S37–S41:** pouch·DRT·고에너지.
- **Supplemental Note S1–S6:** S1 SWCNT ink, S2 FIB-SEM 측정, S3 PNM, S4 2C 방전 전기화학모델(GeoDict
  2023, 2.15% 오차), S5 electrochemo-mechanical VMS, S6 thermal-electrochemical 안정성.
- **Table S1–S10:** S1 각 전극 사양, S2 보고된 고부하 성능, S4 FIB-SEM 조건, S5–S7 전기화학 governing
  eq·파라미터·기호, S9 coin/pouch 사양, S10 10 Ah pouch VED 계산.

---

## 8. 기술 미니용어집 (우리 맥락)

- **continuous SWCNT sheath(연속 SWCNT sheath):** NCMA 입자 표면을 따라 SWCNT가 conformal·연속으로 감싼
  정맥형(vein-like) 도전망. ★ **우리가 모델하지 않는 제3 morphology** — 우리 SuperP(분산점)도 VGCF
  (interstitial 섬유)도 아닌 **surface-conformal**(활물질 표면에 코팅). 두꺼운 전극에서 실제로 이기는 형태.
- **zeta-potential modulation(zeta 변조):** PDDA(양이온)로 NCMA 표면전하를 음(−33.8)→양(+14.2)으로 반전 →
  음전하 SWCNT(−35.0)가 정전인력으로 부착 → 합성물 near-neutral(−1.92) = 완전 coverage. = 어떤 도전재가
  활물질에 "붙을지/분산될지"의 표면화학적 제어(우리 `nucleate_frac`/`surface_frac` 경험치의 물리 근거 후보,
  단 LPSCl 표면전하는 우리 측정 필요).
- **integrated active material–conductive agent(통합 활물질-도전재):** 도전재를 활물질 표면에 통합(별도
  혼합 아님) → **기공(이온채널)을 안 막으면서 전자망 형성** → 전자·이온 동시 균질. 우리 CBD의 ionic-blocking
  trade-off를 morphology로 회피한 설계.
- **tortuosity factor τ:** 기공망의 우회도. SWCNT-dry 1.28 vs CB-wet 2.31. 유효확산 D_eff = D_int·ε/τ.
  우리 σ_ionic의 C(τ) 항·Phase 4 τ(Laplace/Dijkstra)와 동일 물리(우리는 실측 τ 없음; #286/#275가 토모 τ 공급).
- **effective diffusivity D_eff(유효확산계수):** 미세구조 균질화 후 Li⁺ 확산. SWCNT-dry 2.5×10⁻¹¹ vs
  CB-wet 1.0×10⁻¹¹ m²/s(2.5×). = 우리 voxel FV의 **확산모드 출력**(우리 FV는 σ만 — D_eff 추가 후보, #281
  DiffuDict 대응).
- **closed pore(고립기공):** bulk 기공망에서 단절되어 Li⁺ 수송에 기여 못 하는 기공. CB-wet이 SWCNT-dry의
  2배. = 우리 SE 퍼콜레이션의 "dead-SE"(고립 SE 채널) 기공판.
- **PNM(pore network model):** 토모 3D를 기공(ball)+연결(stick)로 추상화 → 등가반경·coordination number·
  connectivity matrix. = 우리 particle-contact CN의 **pore-side 대응**(우리는 입자접촉 CN만; PNM은 기공 CN).
- **KPFM work function(켈빈 프로브 일함수):** 입자별 work function = SOC(리튬화 정도) 균질도 프록시.
  SWCNT-dry 단일 peak(균일 SOC) vs CB-wet 넓은 분포(불균일 SOC). 우리엔 직접 대응 없음(거시 σ만; 입자별
  SOC 균질도는 Phase 4 영역).
- **SSRM(scanning spreading resistance microscopy):** 단면 국소저항 맵. 우리 voxel σ 맵의 실험 대응
  (#284와 동일 방법; 여기선 사이클 전후 degradation 추적).
- **VMS(von Mises stress) digital twin:** Li⁺ 농도의존 strain → stress(NCM811 E=105 GPa·ν=0.27, 3.4 vol%
  팽창). 우리 MPM 응력장(단 우리 MPM은 SE 소성·AM rigid; 그들은 활물질 탄성 intercalation strain) 대응.

---

## ★ 9. 우리 SuperP-vs-VGCF CBD 발견 검증 (frame [1]–[5]) — 이 디제스트의 심장

⚠ **대전제(맨 먼저, #284/#285/#286과 동일):** 이 논문은 **NCMA 양극 + 흑연 음극 + 액체전해질 dry-processed
일반 LIB**다 — 우리 **LPSCl sulfide ASSB(고체전해질, 무전해질 contact-network)**가 **아니다**. 따라서:
- **셀 전기화학 절대값은 전이 불가.** 945 Wh/L · 310 Wh/kg · 215 mAh/g · 80% SOC@20분 · 78%@500cyc ·
  τ 1.28/2.31 · D_eff 2.5e-11 등은 **NCMA/흑연/액체전해질** 값이고, Li⁺가 **전해질을 통해 확산**하는
  물리다 — 우리 σ_ionic/e는 **SE/AM 입자 접촉망의 Kirchhoff/Holm 전도**(무전해질). **수치 σ/porosity
  앵커는 Bazzoun(LPSCl)/Varkey(halide)/Minnmann(LPSCl cold-press)/#266이 담당** — 이 논문에서 안 가져온다.
- ★ **강하게 전이되는 것 = CARBON-MORPHOLOGY 물리(소재-일반):** **(i) 연속 1D 도전망이 두꺼운 전극
  전자전도를 이기고, discrete 도전재는 연속망을 못 만든다; (ii) discrete 도전재는 이온수송 채널(전해질
  기공/SE 망)을 막는다.** 이 둘은 **전해질 종류·활물질 무관한 기하·퍼콜레이션 물리**라 우리 voxel CBD 발견에
  **직접 전이**된다(전자=퍼콜레이션 threshold, 이온=채널 점유). ⇒ #275는 우리 발견의 **실험적 증명**이다.

### (a) ★★ 전자축 — 우리 "discrete carbon = 두꺼운 전극 self-percolate 불가(σ=0)" 의 실험적 증명
- **우리(`docs/cbd_morphology_roadmap.md`, voxel carbon-only 테스트):** real_10 두꺼운 전극(708 z-cell)에서
  **carbon-only σ = 0** — carbon이 voxel 셀의 **~6–7%**에 불과 ≪ **31% 3D site-percolation threshold** →
  **1 wt%(심지어 4 wt%) discrete carbon(SuperP 점/짧은 VGCF)은 self-percolate 못 한다**. 결론: **discrete
  carbon = AM 골격 위 gap-FILLER, never the BACKBONE**(두꺼운 전극에선 carbon이 backbone이 될 수 없다).
  AM-poor crossover 테스트(decimation sweep)에서도 50% 이하 AM에서 **carbon 1 wt%로 죽은 망 복구 불가**
  (both 0) — 1 wt% carbon은 자기-퍼콜레이션 안 됨을 직접 확인.
- **그들(#275, 서론 + Fig 2,4):** ★ 정확히 같은 문제를 **명시**한다 — **"conventional conductive additives,
  which must be added in large quantities yet often fail to form continuous networks"** (서론). 그리고
  해결책이 **continuous SWCNT sheath**(engineered 1D 연속망 — discrete가 아니라 **연속**)이다. Fig 2C에서
  **CB-wet은 Q_areal↑에 저항 10→40 Ω·cm 급증 + 균열**(discrete CB가 두꺼운 전극서 연속망 실패), **SWCNT-dry는
  5–10 Ω·cm 안정**(연속망). Fig 2E–J KPFM: **CB-wet heterogeneous SOC vs SWCNT-dry homogeneous SOC**
  (연속망이 균일 전류분포). Fig 5 SSRM: 300사이클 후 **CB-wet 내부저항 10⁴ GΩ 폭증(전기적 고립) vs SWCNT-dry
  균질 저저항**(연속망 robust).
- ✅ **이것이 우리 발견의 EXPERIMENTAL PROOF:** 우리 "discrete carbon은 두꺼운 전극을 self-percolate
  못 한다(σ=0; <31% threshold)" 라는 **voxel 퍼콜레이션 결론**을, #275가 **연속 SWCNT sheath로 풀어야
  했다**는 실험으로 증명한다 — 즉 **두꺼운 전극은 discrete carbon으로 안 되고 ENGINEERED CONTINUOUS 1D
  도전망이 필요하다**. 우리 시뮬이 "이래서 안 된다(σ=0)"를 보였다면, #275는 "그래서 이렇게 해야 된다
  (continuous sheath)"를 보인 것 — **같은 결론의 음(우리)·양(그들) 양면**. 우리 결과가 시뮬 artifact가
  아니라 **두꺼운 전극의 실제 설계 제약**임을 확증.

### (b) ★★ 이온축 — 우리 "discrete carbon이 이온채널을 막는다(SuperP 1.8× blocking)" 의 실험적 증명
- **우리(voxel σ_ionic, real_10):** **SuperP가 SE 이온망을 VGCF보다 ~1.8× 더 막는다 — σ_ionic SuperP
  0.0168 < VGCF 0.0298 mS/cm**. 물리: SuperP의 **분산 aggregate가 SE 사이사이로 끼어들어 SE 이온 packing을
  교란**(MPM SE-rearrangement), VGCF의 **집중 섬유는 SE를 거의 그대로 둠**. = **discrete carbon이 이온수송
  채널(여기선 SE 망)을 점유·교란해 σ_ionic을 떨어뜨린다**.
- **그들(#275, 서론 + Fig 4):** ★ 정확히 같은 문제를 **명시**한다 — **"[conventional additives]… often
  obstruct ion-transport channels"** (서론). CB-wet의 **CBD(carbon-binder domain)가 bulky·tortuous하여
  Li⁺의 전해질 경로를 막음**(Fig 2A 모식 + Fig 4C **closed pore CB-wet 2× + tortuosity 2.31**). 해결책은
  도전재를 **활물질 표면에 통합(integrated)하여 기공(이온채널)을 비우는 것** → Fig 4D **유효확산
  SWCNT-dry 2.5× ↑** + Fig 4H **CB-wet 큰 농도구배(바닥 <0.2 M 고갈) vs SWCNT-dry 균일 0.9 M**. 즉
  **discrete carbon(응집 CBD)이 이온채널을 막아 Li⁺ 공급을 방해**한다는 것을 digital twin으로 정량.
- ✅ **이것이 우리 발견의 EXPERIMENTAL PROOF:** 우리 voxel σ_ionic "SuperP가 SE 이온망을 1.8× 더 막는다"
  라는 결과를, #275가 **"conventional additives obstruct ion-transport channels → 표면통합으로 채널을
  비워야 한다"**는 실험·digital-twin으로 증명한다. 우리는 **SE 망(고체) 점유**로, 그들은 **전해질 기공
  점유**로 — **주체는 다르나(SE packing vs 전해질 기공) 물리 방향은 동일**: **discrete carbon이 이온수송
  채널을 막는다**. ⇒ 우리 ionic-blocking finding이 **시뮬 artifact가 아닌 일반 물리**임을 확증.

### (c) ★ SWCNT conformal sheath = 우리가 모델하지 않는 제3 morphology (정직한 한계 + future 옵션)
- **우리 `scripts/additives.py`:** 도전재를 **2가지 morphology**로 모델 — **SuperP**(0D, distributed
  aggregates, `SP_D=0.20 µm` sphere blobs, mixing=thinky면 AM 표면 일부 코팅) + **VGCF**(1D, interstitial
  fibres, `VGCF_D=0.15·VGCF_L=10 µm`, AR≈67, 무작위 배향). PTFE는 binder fibril(`nucleate_frac`으로 carbon에
  co-locate). 우리 결론 "SuperP > VGCF 전자(real_10) / VGCF > SuperP 이온"은 **이 두 morphology 안**에서다.
- **그들(#275) = 제3 morphology:** **SWCNT가 활물질 표면을 따라 conformal·연속으로 감싼 sheath(surface-
  conformal, vein-like)**. 이것은 **우리 SuperP(분산점)도 VGCF(interstitial 섬유)도 아니다** — 도전재가
  **공극(interstitial)이나 분산(distributed)이 아니라 활물질 표면에 코팅**된다. ★ **그리고 이 surface-
  conformal sheath가 두꺼운 전극에서 실제로 이기는 morphology**다(우리 두 morphology 중 어느 것도 #275가
  보인 945 Wh/L + 균일 전자/이온을 못 줌 — 우리 SuperP/VGCF는 둘 다 자기-퍼콜레이션 못 하는 1 wt% gap-filler).
- ★ **정직한 한계 + future 옵션:**
  - **(한계)** 우리 SuperP-vs-VGCF 비교는 **interstitial/distributed 도전재 morphology에 한정**된다 —
    **surface-conformal sheath(#275의 승자)는 우리 morphology 공간 밖**이다. 우리 "어느 도전재가 나은가"
    결론은 **표면통합 sheath를 포함하지 않는다**(SWCNT-wrapping이 있으면 그게 둘을 다 이김).
  - **(future 옵션 — `additives.py`)** 제3 morphology를 추가 후보: **`surface_conformal` 도전재 = AM
    표면 셀에 도전상을 얇게 코팅**(SuperP의 `surface_frac` coating을 극단화 = AM 표면 voxel에 도전상
    1-cell 층). 이러면 **연속 표면 도전망**(우리 voxel FV에서 AM 표면을 따라 자동 연결)이 생겨 #275의
    sheath를 모사 → voxel σ_e가 두꺼운 전극서도 percolate하는지 테스트 가능. (단 우리 LPSCl ASSB에선
    AM 표면 도전코팅이 SE 이온접촉을 줄일 수 있어 — 이온 trade-off를 별도 검토.)

### (d) ★ 그들 3D digital twin = 우리 voxel/Phase-4 (published blueprint, #281/#286과 동일)
- **그들:** **GeoDict 2023**으로 FIB-SEM 토모 3D 재구성 → **effective τ(1.28/2.31)·D_eff(2.5e-11/1.0e-11)·
  closed pore·coordination(PNM)** 추출 → **GeoDict 2023 전기화학(2C 방전, charge보존·Fick·Ohm·BV, 2.15%
  오차)**로 방전곡선·농도/전류/응력 분포. = 이 그룹의 반복 digital-twin(#281 GeoDict+COMSOL, #286 GeoDict-τ+PNM,
  #284 SSRM, #285 GeoDict 모두).
- **우리:** **voxel FV(`scripts/voxel_conductivity.py`)**로 effective σ 추출 + **PyBaMM Phase 4**로
  전기화학(σ·τ 주입 → 방전곡선). **수학적으로 동일 구조**(미세구조 → effective → 1D 전기화학).
- ★ **이식/대응:**
  - **(i) D_eff 출력 추가:** 그들 D_eff(2.5×)는 우리 voxel FV에 **확산모드**(정상상태 Fick)를 추가하면
    얻는다 — 현재 우리 FV는 σ(전도)만. **D_eff/τ 출력**을 추가하면 그들 2.5× ↔ 우리 contact-network τ를
    **frame[4] 교차검증**(#281 DiffuDict와 동일 이식 후보). 우리 "2.5× Li⁺ diffusivity"의 우리 버전 =
    **연속 도전망(낮은 τ) 케이스의 D_eff vs discrete(높은 τ) 케이스 D_eff 비**.
  - **(ii) PNM pore-side 지표:** 우리는 입자접촉 CN만 — 그들 PNM의 **기공 coordination·connectivity matrix·
    closed pore %**는 우리에게 없는 **pore-side 지표**. voxel FV 출력에 추가하면 "dead-SE(고립 SE 채널)"를
    기공판으로 정량(#286 PNM 이식과 동일).
  - **(iii) 4종 전극 비교 = 우리 SuperP vs VGCF의 확장:** 그들은 **carbon source(CB/SWCNT) × 공정(wet/dry)
    4종**을 같은 framework로 비교 — 우리도 **SuperP/VGCF/(future)conformal-sheath × (선택) 공정**을 같은
    voxel framework로 비교하면 #275의 4종 비교를 우리 ASSB판으로 재현 가능.

### (e) frame[5] 분업 — 우리 우위 명확화
- **그들:** **post-mortem 측정(SEM/TEM/EELS/SSRM/KPFM/XRD/SAICAS) + digital-twin(GeoDict effective + 1D
  전기화학 + VMS)**. 강력하지만: **입자스케일 압축역학 예측 없음**(고정 미세구조 — 토모는 이미 압축된 전극),
  **explicit 접촉 σ triad 없음**(GeoDict effective σ만, 우리 Holm constriction 없음 → 점접촉 sub-voxel 못
  잡음), **소성 morphology·void-fill 예측 없음**(VMS도 활물질 탄성 intercalation strain만, 압축 소성 아님),
  **압력→미세구조→σ 예측 없음**, **fracture explicit 없음**(degradation은 post-mortem 관찰).
- **우리 DEM+MPM:** **압력→미세구조→σ(ionic/e/thermal triad) 예측**(입력단) + **MPM 소성 morphology·
  void-fill**(SE 압축 형태) + **voxel FV로 carbon network의 σ_e gain·σ_ionic blocking을 mechanistic 정량**
  (그들 SSRM/digital-twin의 인과 버전 — 우리는 morphology를 직접 만들어 σ를 푼다) + **fracture(Auerbach/Holm)**.
- ⇒ **이상 워크플로:** 우리 DEM+MPM이 CBD morphology를 생성/예측 → 그들식 **GeoDict effective(τ/D_eff/PNM)**로
  검증(우리 voxel FV의 확장) → 그들식 **1D 전기화학(우리 Phase 4)**로 농도/전류 균질성 닫기. 이 논문은
  **우리 CBD 발견의 실험 reference + digital-twin 방법 공급원**이지 입력단 경쟁자가 아니다. (frame[5]
  재확인 — 그들엔 입자스케일 압축예측·접촉 σ triad·소성 morphology가 없음.)

### 비교 요약표
| 축 | Koo 2026 #275 (NCMA/흑연·액체 dry) | 우리 (LPSCl ASSB, CBD voxel) | 이식/판정 |
|---|---|---|---|
| 소재 | NCMA + 흑연 + 액체전해질 dry-to-dry | LPSCl SE + NMC811 | ⚠ 셀 전기화학 절대값(Wh/L·SOC·τ·D_eff) 전이불가 |
| 전자: discrete 도전재 연속망 실패 | CB-wet 저항 10→40 Ω·cm+균열, "fail continuous networks" | carbon-only σ=0(6-7% ≪ 31% threshold) | ✅ **우리 전자 발견의 실험적 증명** |
| 이온: discrete 도전재가 채널 막음 | CBD bulky+closed pore 2×+τ2.31, "obstruct ion channels" | SuperP σ_ionic 0.0168 < VGCF 0.0298(1.8×) | ✅ **우리 이온 발견의 실험적 증명**(주체 다름: 전해질기공 vs SE망) |
| 해결책 morphology | **continuous SWCNT conformal sheath**(surface-conformal) | SuperP(분산점)/VGCF(interstitial)만 | ★ **제3 morphology(우리 미모델)** = future additives.py 옵션 + 정직한 한계 |
| 두꺼운 전극 | >11 mAh/cm² SWCNT-dry 성공(CB-wet 균열) | real_10 708-cell thick voxel | ✅ 연속 1D망 두꺼운 전극 필요 = 우리 thick-electrode 결론 일치 |
| digital twin | GeoDict effective(τ/D_eff/PNM)+1D 전기화학(2.15%) | voxel FV(σ)+PyBaMM Phase 4 | ★ **published blueprint** + D_eff/PNM 이식 후보(#281/#286 동일) |
| 측정 vs 예측 | post-mortem 측정+고정구조 digital twin | 압력→구조→σ 예측+소성 morphology | 우리 우위(그들엔 입자스케일 예측·접촉 σ triad 없음) |
| 우리 고유 | (없음) | DEM 접촉 σ triad + MPM 소성 + fracture + voxel FV mechanistic carbon σ | frame[5] 분업 재확인 |

---

## ★ 10. 우리 작업에 넣을 가장 날카로운 인사이트 3–5가지

1) ✅✅ **우리 voxel CBD 발견(전자+이온)의 EXPERIMENTAL PROOF — audit ✅#4를 두 축으로 강화.**
   #275는 **(전자)** "conventional additives fail to form continuous networks"(우리 carbon-only σ=0,
   discrete <31% 퍼콜 threshold) + **(이온)** "obstruct ion-transport channels"(우리 SuperP σ_ionic
   1.8× blocking)를 **둘 다 명시**하고 **continuous SWCNT sheath**로 해결한다. 우리 voxel 결과(시뮬)가
   "discrete carbon은 두꺼운 전극서 안 된다"를 보였다면, #275는 "그래서 연속망이 필요하다"를 **실험·
   digital-twin으로 증명** — **같은 결론의 음·양 양면**. 우리 finding이 **시뮬 artifact가 아니라 두꺼운
   전극의 실제 설계 제약**임을 확증(모델 신뢰도↑). → audit ✅#4(기존 "discrete carbon 퍼콜 불가 = #275
   정합")가 이제 **전자(퍼콜레이션) + 이온(채널차단) 두 축의 full 실험데이터**로 뒷받침됨 = **강화됨**(예상대로).

2) ★ **SWCNT conformal sheath = 우리가 모델하지 않는 제3 morphology — 두꺼운 전극의 실제 승자 → future
   additives.py 옵션 + 정직한 한계.** 우리 `additives.py`는 **SuperP(분산점) + VGCF(interstitial 섬유)**
   2종만 모델한다 — #275의 승자 **surface-conformal sheath(활물질 표면 코팅, vein-like)는 우리 morphology
   공간 밖**이다. 우리 "SuperP vs VGCF" 결론은 **interstitial/distributed에 한정**이며, 표면통합 sheath가
   있으면 그게 둘을 다 이긴다(945 Wh/L + 균일 전자/이온; 우리 1 wt% SuperP/VGCF는 둘 다 자기-퍼콜레이션
   못 하는 gap-filler). → ★ **`additives.py`에 `surface_conformal` morphology 추가**(AM 표면 voxel에 도전상
   1-cell 코팅 = 연속 표면 도전망) → voxel σ_e가 두꺼운 전극서 percolate하는지 + LPSCl SE 이온접촉을 줄여
   σ_ionic을 떨어뜨리는지(표면코팅의 이온 trade-off) 테스트. 이게 #275를 우리 ASSB판으로 재현하는 길.

3) ★ **digital-twin D_eff + PNM pore-side 지표를 우리 voxel FV에 추가 — #275/#281/#286 published blueprint.**
   #275는 GeoDict로 **유효확산 D_eff(SWCNT-dry 2.5× = 2.5e-11 vs 1.0e-11 m²/s) + tortuosity(1.28/2.31) +
   closed pore %(CB-wet 2×) + PNM coordination/connectivity matrix**를 추출하고 **1D 전기화학(2.15% 오차)**로
   닫는다. 우리 voxel FV는 **σ만** 푼다 → ★ **(i) 확산모드(정상상태 Fick) 추가 → D_eff/τ 출력**(그들 2.5× ↔
   우리 contact-network τ를 frame[4] 교차검증; #281 DiffuDict 이식); **(ii) PNM pore-side 지표**(기공 CN·
   connectivity·closed pore = 우리 "dead-SE 고립채널"의 기공판; 우리는 입자접촉 CN만). 그들 2.5× D_eff =
   "연속망(낮은 τ) vs discrete(높은 τ)" 의 우리 버전을 줄 수 있다.

4) ★ **frame[5] 재확인 + 우리 우위:** 이 논문은 **post-mortem 측정(SSRM/KPFM/EELS) + digital-twin(GeoDict
   effective + 1D 전기화학 + VMS)**으로 강하나, **입자스케일 압축역학 예측·explicit 접촉 σ triad(Holm
   constriction)·소성 morphology/void-fill·압력→구조 예측·explicit fracture가 없다**(고정 미세구조 = 이미
   압축된 토모). 우리 DEM+MPM은 **압력→미세구조→σ triad 예측 + MPM 소성 + voxel FV로 carbon network의
   σ_e gain·σ_ionic blocking을 mechanistic 정량**(그들 digital-twin의 인과 버전 — 우리는 morphology를 직접
   만들어 σ를 푼다). ⇒ **이상 워크플로 = 우리가 CBD morphology 생성/예측 → 그들식 GeoDict effective(τ/
   D_eff/PNM)로 검증 → 그들식 1D 전기화학으로 균질성 닫기.** 이 논문은 우리 파이프라인의 **출력단(검증) +
   방법 청사진**이지 입력단 경쟁자가 아니다.

### 보너스 실행 항목
- **#275 인덱스 갱신**(아래 완료): "방금 작업과 정합" 한 줄 → 풀 디제스트 수치(zeta −33.8/+14.2/−35.0/−1.92
  mV, 분말전도 0.06 vs 0.20 S/cm, 활물질 99.7 wt%·PTFE 0.3·ρ 4.0, 945 Wh/L·310 Wh/kg, τ 1.28/2.31,
  D_eff 2.5×, 80% SOC@20분, 78%@500cyc, FIB-SEM 820장 GeoDict 2.15%)로 교체 + ★ **우리 voxel CBD
  발견(전자+이온)의 EXPERIMENTAL PROOF**로 격상.
- ⚠ **혼동 금지(#284와 역할 구분 — 둘 다 CBD trade-off지만 다른 축):**
  - **#275(이 논문, NCMA/흑연·액체 dry):** ★ **우리 voxel CBD 발견(전자: discrete 연속망 실패 + 이온:
    discrete가 채널 막음)의 EXPERIMENTAL PROOF**. continuous SWCNT sheath = 제3 morphology(미모델) + digital-twin
    blueprint(D_eff/PNM). **수치 σ/porosity 앵커 아님.**
  - **#284(Oh, SiOx/흑연·액체):** **CBD ion/electron trade-off 독립확증 + balance point 개념(moderate-C
    최적) + 분산 측정법(SSRM/W_adh)** 공급원. **탄소 양/두께 축**(우리 도전재 종류/분산 축과 동일 긴장).
  - **둘의 차이:** #275 = **morphology(연속 sheath가 discrete를 이김 = 우리 SuperP/VGCF 발견의 증명 +
    제3 morphology)**; #284 = **양/두께(탄소↑→전자↑·이온↓, 중간 최적 = balance curve 동기)**. 서로 보완.
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·#266이 담당** —
    혼동 금지.
- **future additives.py `surface_conformal` morphology**(인사이트 2)를 cbd_morphology_roadmap의 PENDING
  "4 wt% VGCF-regime 테스트" 옆에 추가 — #275의 sheath를 우리 voxel판으로 재현해 "연속 표면 도전망이
  두꺼운 전극서 percolate하는가 + LPSCl 이온접촉 trade-off"를 정량.
