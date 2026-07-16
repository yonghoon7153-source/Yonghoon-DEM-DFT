# ⭐필독 / 우리-랩 — Accelerated Degradation of ASSBs Induced through Volumetric Occupation of the Carbon Additive in the SE Domain — Kim, Park, Kang, …, Lee, Sun, Cho (Adv. Funct. Mater. 2024)

> slug `kim2024_carbon_volumetric_occupation_se_domain` · DOI `10.1002/adfm.202409318` · type `exp` (실험, no DEM/MPM) · PDF `Kim_2024_AdvFunctMater_CarbonVolumetricOccupation_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang **Jong-Won Lee** 그룹 + **Yang-Kook Sun** + **KETI Woosuk Cho**) 자체 논문 — 모델이 따라가야 할 실험 trend의 기준점 ★★★
> 저자 = **Hyun-seung Kim, Sejin Park, Sora Kang, Jae Yup Jung, KyungSu Kim, Ji-Sang Yu, Dong-Won Kim,
> Jong-Won Lee\*(Hanyang Univ.), Yang-Kook Sun\*(Hanyang Univ.), Woosuk Cho\*(KETI Advanced Batteries
> Research Center)**.  세 명의 교신저자 모두 우리 랩 계열(Hanyang + KETI).  **Kang & Shin 2025**
> (`papers/kang2025_toughened_bimodal_nca_lzo.md`)·**Kim, Kang, Park, Lee 2025**
> (`papers/kim2025_impedance_decoupling_tlm_assb.md`)와 **자매 논문** — 같은 랩의 ASSB 복합양극 시리즈.
> 이 논문이 정하는 실험 방향(**도전 carbon 첨가제가 SE 도메인을 *부피로 점유*하여 SE 망을 굶기고, 그 표면이
> 황화물 SE 산화분해를 *촉매*하여 열화를 가속** — 고-AM(>90 wt%)에서 최악; 해결 = **구형 SC → 1D carbon
> 섬유 CF** 로 형상 변경)에 우리 DEM+MPM **CBD/Stage-2 도전제 모델**이 정렬해야 한다.

---

## 1. 한 줄 요약
**도전 carbon 첨가제(저밀도 ρ=0.67 g/cm³)는 SE 도메인(ρ=1.86)을 *부피로 점유*하여 formation 후 잔존 SE 분율을
줄여 σ_ionic을 붕괴시키고(90 wt% AM에서 σ_ionic ≈ 80 wt%의 1/10), 동시에 그 carbon 표면이 NCM 위 황화물 SE의
*산화분해를 촉매*하여 저항성 부산물(sulfate/phosphate/P-O-P)을 만들어 열화를 가속한다 — 고-AM(>90 wt%)의
SE-poor 레짐에서 최악.**  순수 실험 논문(DEM/MPM 없음)이지만, **carbon이 SE를 부피로 밀어낸다(ρ_carbon ≪ ρ_SE)는
정량 메커니즘** + **σ_e↑ vs σ_ionic↓ 트레이드오프** + **구형 SC vs 섬유 CF morphology가 SE 망/전달을 좌우**한다는
데이터를 줘서, 우리 **CBD/Stage-2(PTFE·VGCF) 도전제 모델 + SE-poor porosity 연구 + σ_e/σ_ionic 삼중항**의
**frame[4] 외부 실험 앵커**이자 *흡수해야 할 물리(carbon = SE 도메인 점유체, inert 아님)*.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM/도전제) | 연구유형 |
|---|---|---|---|---|
| H.-s. Kim, S. Park, S. Kang, J. Y. Jung, K. Kim, J.-S. Yu, D.-W. Kim, **Jong-Won Lee\***, **Yang-Kook Sun\***, **Woosuk Cho\*** (KETI Advanced Batteries Research Center + Hanyang Univ.) | Adv. Funct. Mater. **34**, 2409318 (2024) | 10.1002/adfm.202409318 | **NCM811 (LiNi₀.₈Co₀.₁Mn₀.₁O₂)** + 아지로다이트 **LPSCl (Li₆PS₅Cl₀.₅Br₀.₅)** + **도전 carbon: 구형 SC(Super C, Timcal) / 섬유 CF(PotenCia, Teijin)** + (건식전극) PTFE | **실험** (펠릿/건식 셀 제조 + DC분극 σ + CC-pulse 분극 + XPS/HR-TEM/SEM/CV); **시뮬레이션 없음** |

핵심 레시피 (Methods/SI):
- **조성 스윕**: 양극 복합체 wt비 = (100−x):x:3 (AM:SE:carbon 3 wt% 고정 — *AM 80/85/90 wt% 스윕*) 그리고
  90:(13−y):y (90 wt% AM 고정 — *carbon 0/1/2/3 wt% 스윕*).
- **펠릿 셀**: 복합체 15 mg, **517 MPa** 가압(PAEK 몰드, 직경 13 mm), SE 150 mg 먼저 가압, **LiIn 음극**, 11 N·m 토크 밀봉.
  1.0 C = 180 mA/g, 0.05–2.0 C 레이트.
- **건식 전극**: NCM:SE:carbon:PTFE = **90:9:1:1 wt%**, 20000 RPM 밀링 + 모르타르 4회 혼합 → kneading → 캘린더링 시트.
  **mass loading 36 mg/cm², areal capacity 6.0 mAh/cm²**.  Li 음극.
- **SE 합성**: Li₂S+P₂S₅+LiCl+LiBr, 350 rpm 2 h 볼밀, 50 MPa 펠릿, 550 °C 6 h 진공 열처리 (드라이룸).
- **σ 측정**: DC 분극 — SE/복합체/SE 적층 가압(517 & 103 MPa) 후 정전류로 σ_ionic, 복합체(517 MPa)에 정전압으로 σ_e.

## 3. 핵심 물성 (수치) ★
> ⚠ 대부분 **실험 측정값(stated)** — 그림 막대의 숫자 라벨 또는 본문 텍스트.  Fig S3 곡선(carbon% 스윕 σ)만 digitized(추세).

| 물성 | 값 | 조건 (P, 조성) | stated/digit | 비고 |
|---|---|---|---|---|
| **ρ_SE (LPSCl)** | **1.86 g/cm³** | Archimedes(이소프로판올) | stated | 치밀한 황화물 SE |
| **ρ_carbon (SC)** | **0.67 g/cm³** | Archimedes | stated | ★ 저밀도 → g당 SE의 ~2.78× 부피 점유 |
| **SE vol% vs AM%** | **30.0 → 13.9 vol%** | AM **80 → 90 wt%** (carbon 3 wt%) | stated | ★ SE 부피분율 반토막 — SE 망 굶음 (Fig 1e) |
| **σ_ionic (펠릿) vs AM%** | **0.125 / 0.0458 / 0.0138 mS/cm** | AM **80 / 85 / 90 wt%** (carbon 3 wt%) | stated (Fig 1c) | ★ 90 wt% = 80 wt%의 **≈1/10** (0.0138/0.125 = 11%) |
| **σ_e (펠릿) vs AM%** | **38.6 / 54.8 / 65.2 mS/cm** | AM **80 / 85 / 90 wt%** (carbon 3 wt%) | stated (Fig 1d) | ★ AM↑ → σ_e **상승** (AM의 σ_e > SE의 σ_e) — σ_ionic과 *반대* 방향 |
| **비가역 용량 vs carbon%** | **26.3 → 42.9 mAh/g** | carbon SC **0 → 3 wt%** (90 wt% AM) | stated (Fig 2b) | ★ carbon↑ → SE 산화 부반응↑ (+63%) |
| **Coulombic 효율 감소** | **~2.0%** | 90 wt% AM vs 80/85 wt% | stated | 90 wt%서 뚜렷한 분극 |
| **σ_ionic vs carbon%** | 0–3 wt%서 **거의 평탄** | 90 wt% AM 고정 (Fig S3a) | digitized(추세) | carbon%는 σ_ionic에 약영향(SE-displacement가 AM%로 지배) |
| **σ_e vs carbon%** | carbon↑ → **상승** | 90 wt% AM 고정 (Fig S3b) | digitized(추세) | carbon이 전자망 형성 |
| **SC vs CF: σ_ionic (건식)** | **0.087 (SC) / 0.105 (CF) mS/cm** | 1 wt% carbon, 건식전극 | stated (Fig 4c) | ★ CF가 **+22%** (SE 도메인 덜 점유) |
| **SC vs CF: σ_e (건식)** | **5.08 (SC) / 5.18 (CF) mS/cm** | 1 wt% carbon, 건식전극 | stated (Fig 4c) | ★ σ_e는 **거의 동일** → CF는 σ_ionic만 구제 |
| **SC vs CF: 최대 산화전류 (CV)** | **0.088 (SC) / 0.015 (CF) mA** | SE:carbon 14:1 | stated (Fig S5) | ★ CF가 **~6× 낮음** — SE 산화분해 덜 촉매 |
| **BET 정규화 산화전류** | SC ≈ CF (**유사**) | Fig S6 | stated | ★ 표면적당 분해 *속도*는 같음 → CF 이점은 *부피 점유·총 접촉면적*이지 표면화학 아님 |

**porosity / Heckel / coordination Z / coverage% (정량) / E_SE / σ_y / ν / PSD(D10/D50/D90)**: **n/a** —
압밀 모델·정량 porosity·접촉면적·배위수·탄성계수·소성 측정 **없음**(실험 셀; HR-TEM/SEM은 *정성* 계면/형상).
SC·CF의 입경/직경 수치는 본문 미기재(Fig S4 SEM 정성).

## 4. 시뮬레이션 방법 ★
- **code / version**: **없음** — 순수 실험.  DEM·MPM·FEM·RNM 일절 없음.
- **DEM 접촉법칙 / 재료 파라미터 (E,ν,μ,COR,σ_y)**: **n/a** (시뮬 없음).
- **bond/binder 모델**: 모델 없음.  건식전극에 **PTFE 1 wt%** 사용(섬유화 바인더) — 본문은 carbon morphology에 집중,
  PTFE 정량 효과는 미분석(자매 논문 Lee 2025가 PTFE wt% σ 페널티 곡선 제공 → 교차).
- **MPM/continuum / 전달 솔버**: **n/a**.  전달은 **DC 분극**(정전류→σ_ionic, 정전압→σ_e)으로 *측정*(솔버 아님).
- **입자 처리** ★ (DEM판 "무질서 처리"): 실험이라 입자 모델 없음.  **그러나** 이 논문의 핵심 관찰이 우리 모델의
  *입자 처리에 직접 시사*:
  - **도전 carbon = SE 도메인을 부피로 점유하는 *제3상***.  우리 DEM/MPM에서 carbon을 *inert·무시*가 아니라
    **SE 영역을 차지하는 저밀도 입자(또는 coating)**로 다뤄야 한다는 실험 근거(ρ_carbon 0.67 ≪ ρ_SE 1.86).
  - **구형(SC) vs 섬유(CF) morphology가 SE 망 연결성과 전달을 좌우** → 우리 CBD morphology 축(SuperP 구형 vs
    VGCF 섬유)과 1:1.  CF(1D)는 *적은 부피로 NCM을 잇는다* = 우리가 CBD 섬유망을 모델하는 동기.
  - 입자 *형상 소성*(SHAPE flow)은 이 논문 범위 밖 — *부피 점유·접촉·산화*가 메시지.
- **도메인/RVE / servo / seeds / 압력범위**: **n/a** (제조 가압 517 MPa, σ 측정 적층 517 & 103 MPa).
- **특이사항/메커니즘 (우리 모델 입력에 시사)**:
  - **3상 접촉계면(NCM–carbon–SE)이 분해를 촉매**(Fig 3b line-EDS): carbon 표면에서 SE 산화 개시 → NCM 표면에서
    P-O-P 등 형성.  carbon 함량↑ = 3상 접촉면적↑ = 분해↑.
  - **고-AM(>90 wt%)이 특히 취약**: SE 부피가 이미 적은데(13.9 vol%) carbon이 그 적은 SE를 더 점유 → Li⁺ 경로 차단.
  - **σ_e vs σ_ionic 경쟁**: AM↑(또는 carbon↑) → σ_e↑ 하지만 σ_ionic↓ → 고-areal 설계는 σ_ionic이 율속 → carbon 최적화 필수.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a** | formation 전압곡선 (AM 80/85/90 wt%, carbon 3 wt%) — 90 wt%서 뚜렷한 분극 | 고-AM 분극 = SE 부족·접촉 저항 (우리 SE-poor 코너) |
| **1b** | rate (0.05–2 C, AM 80/85/90) — 90 wt%서 용량 급감·비정상 거동 | 고-AM 율속 한계 |
| **★ 1c** | ★ **σ_ionic 막대: 0.125 / 0.0458 / 0.0138 mS/cm (AM 80/85/90)** | ★★ **AM↑ → σ_ionic ≈1/10 (SE 부피 점유) — 우리 σ_ionic-vs-φ_SE의 실험 앵커** |
| **★ 1d** | ★ **σ_e 막대: 38.6 / 54.8 / 65.2 mS/cm (AM 80/85/90)** | ★★ **AM↑ → σ_e *상승* — σ_e/σ_ionic 트레이드오프(AM의 σ_e > SE)** |
| **★ 1e** | ★ **삼원(AM-C-SE) 부피점유 다이어그램 + 모식: 좌="AM-C-AM e⁻ transfer"(carbon이 e⁻ 잇는다) / 우="Li⁺ block by carbon, AM-AM"(carbon이 Li⁺ 막는다)** + SE 30.0→13.9 vol% | ★★★ **carbon = SE 도메인 점유체의 핵심 그림.  ρ_SE 1.86·ρ_SC 0.67 명기.  우리 CBD = SE 영역 차지 모델의 출처** |
| **2a** | 전압곡선 0.05 C (carbon SC 0/1/2/3 wt%, 90 wt% AM) — carbon↑ → 분극 *감소*(전자전도↑) | carbon이 전자전도엔 도움 |
| **★ 2b** | ★ **비가역 용량 막대: 26.3(0) → 42.9 mAh/g(3 wt% SC)** | ★ **carbon↑ → SE 산화 부반응↑ (열화 채널)** |
| **2c** | rate (carbon 0/1/2/3 wt%) — 0 wt% 대비 1 wt%만 율속 개선, 2·3 wt%는 고율서 급감 | carbon 과량 = 역효과 |
| **2d** | cycleability — carbon↑ = 용량 열화 심함, 특히 SC>2 wt% | 도전제 과량 열화 |
| **2e** | **CC-pulse 분극 vs 전압 (3.1–3.7 V, carbon 0/1/2/3 wt%)** — 3.4–3.7 V(NCM 전하전달)서 3 wt%가 급증 | SE 산화분해의 분극 시그니처 |
| **★ 2f** | ★ **ex-situ O 1s XPS (SC 1 vs 3 wt%)**: phosphate·sulfate·lattice-O·**P-O-P** 피크; 3 wt%서 분해 부산물↑ | ★ **carbon-구동 SE 산화 부산물(저항층)의 화학 증거** |
| **★ 3a** | ★ **FIB-단면 HR-TEM (SC 1 vs 3 wt%)**: 1 wt%는 SE-접촉 NCM 표면, 3 wt%는 **carbon이 SE 도메인 점유** | ★ carbon 부피점유의 *직접 이미지* |
| **★ 3b** | ★ **line-EDS (Ni/S/C)**: 3 wt%서 **NCM–SE–carbon 3상 접촉계면** 분명 → carbon 표면서 SE 분해 개시·NCM서 산화 | ★ 3상 계면이 분해 촉매(메커니즘 코어) |
| **★ 3c** | ★ **모식도**: 저-carbon = Li⁺ 경로 보존(SE 부피분율↑) / 고-carbon = carbon이 Li⁺ 경로 차단 + 3.2 V서 SE 분해 + 3.7 V서 NCM/SE 계면 분해(빨강=후속 분해 SE) | ★★ **failure 메커니즘 전체 그림 — 우리 모델이 흉내낼 carbon 점유·차단·분해 3박자** |
| **★ 4a** | ★ **SC(구형 분산) vs CF(1D 입자간 연결) 전극구조 모식** | ★★ **sphere vs fiber morphology = 우리 CBD(SuperP vs VGCF)와 1:1** |
| **★ 4b** | ★ **건식전극 overlap EDS(C/S/Ni, 1 wt%)**: SC는 carbon이 SE 도메인에 분산(Li⁺ 방해) / CF는 NCM 내 입자간 연결 유지(SE 접촉 최소) | ★ CF가 SE 도메인 덜 점유 = σ_ionic 구제 기전 |
| **★ 4c** | ★ **σ_ionic 0.087(SC)/0.105(CF), σ_e 5.08(SC)/5.18(CF) mS/cm** | ★★ **CF가 σ_ionic +22%·σ_e 동급 → morphology(구→섬유)가 fix** |
| **★ 5a,b** | ★ **state-of-charge ex-situ S 2p XPS (SC vs CF)**: SC가 SOₓ 결합 더 형성 = SE 분해 더 (SC 표면이 NCM SE 산화 촉매) | ★ CF가 SE 산화 덜 일으킴(SOₓ↓) |
| **5c** | rate (SC vs CF 건식) — CF가 σ_ionic·σ_e 둘 다 높아 율속 우수 | CF 전극 우수성 |
| **★ 5d** | ★ **0.2 C 150 cyc (SC vs CF)**: SC = 점진적 확산분극↑·용량 열화(NCM 계면 악화) / CF = **안정 전압·6.0 mAh/cm² 유지** | ★★ **morphology fix가 장수명 보존** |
| **SI S1** | C-rate 전압곡선 (AM 80/85/90) | Fig 1b 보강 |
| **SI S2** | C-rate 전압곡선 (carbon 0/1/2/3 wt%, 90 AM) | Fig 2c 보강 |
| **★ SI S3** | ★ **(a) σ_ionic (b) σ_e vs carbon 0/1/2/3 wt% (90 AM)** | ★ **carbon%는 σ_ionic 약영향·σ_e 강영향 — 트레이드오프 정량** |
| **SI S4** | SC vs CF SEM(powder) | sphere vs fiber 형상 정성 |
| **SI S5** | CV (SE:carbon 14:1): 최대 산화전류 SC 0.088 / CF 0.015 mA | ★ CF가 SE 산화 ~6× 덜 촉매 |
| **★ SI S6** | ★ **BET 정규화 전류밀도**: SC ≈ CF 유사 분해율 | ★ CF 이점 = *부피점유·총면적*이지 표면화학 아님 (중요 단서) |
| **SI S7** | cycle 전압곡선 (SC vs CF 건식) | Fig 5d 보강 |

## 6. Post-processing ★
- **무엇**:
  - **전달**: **DC 분극** — SE/복합체/SE 적층 가압(517 & 103 MPa) + 정전류 → σ_ionic; 복합체(517 MPa) + 정전압 → σ_e.
    (EIS 아님 — Bazzoun/Kim2025 TLM과 다른 직류법.)  값은 셀 형상→σ로 환산한 **절대값**.
  - **분해 진단**: **CC-pulse**(0.05 C 충전→각 전압점→1.0 C 급충/10분 휴지/1.0 C 급방전, ref [1] Byun 2024)으로
    SE 분해 정도를 전압별 분극으로 정량; **ex-situ O 1s / S 2p XPS**로 부산물(phosphate/sulfate/P-O-P/SOₓ) 동정.
  - **형상/계면**: **FIB 단면 HR-TEM** + **line-EDS**(Ni/S/C)로 3상 접촉계면 확인; **SEM**으로 SC/CF·전극 morphology;
    **overlap EDS**(C/S/Ni)로 건식전극 내 carbon 분포.
  - **부피 점유**: **삼원 다이어그램**(AM-C-SE wt→vol) + **Archimedes 밀도**(이소프로판올)로 SE/carbon vol% 산출 →
    SE 30.0→13.9 vol% 도출.
  - **산화 활성**: **CV**(SE:carbon 14:1) 최대 산화전류 + **BET 표면적 정규화** 전류밀도.
- **도구**: Thermo Scientific Sigma Probe(XPS, CasaXPS류), JEOL ARM-200F(HR-TEM), JEOL JSM-IT200(SEM),
  TOYO TOSCAT-3100(사이클러).  porosity/접촉면적/배위수 같은 *구조 정량 후처리는 없음*.
- **수치화·플롯·기록**: σ는 DC분극 환산 절대값(막대그래프 라벨); vol%는 밀도·조성으로 계산; XPS는 피크 디컨볼루션 정성/반정량.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Kim 2024, 실험) | 우리 (DEM+MPM) | 차이 / 이유 (rigid·plastic / 실험·모델 / 채널) |
|---|---|---|---|
| 성격 | **실험 펠릿/건식 셀** (no model) | DEM(전달)+MPM(역학) 시뮬 | frame[4] — **그들 실험 = 우리 외부 앵커**, 경쟁 모델 아님 |
| 소재 | **NCM811 + LPSCl(+Br) + SC/CF carbon** | **NMC811 + LPSCl** (+ CBD/Stage-2 도전제) | ★ AM·SE 동일; **carbon 도전제까지 동일 축**(우리 CBD = SuperP/VGCF) |
| **carbon 처리** | ★ **SE 도메인을 *부피 점유*하는 저밀도 제3상**(ρ 0.67 ≪ 1.86) | 우리 CBD는 σ_e *기여*만 모델, **부피 점유는 부분적** | ★★ **흡수 1순위**: carbon volume = SE-domain 점유로 (inert 아님) |
| **σ_ionic vs AM%** | **0.125/0.0458/0.0138 (AM 80/85/90)** = 90 wt%서 ≈1/10 | 우리 σ_ionic 폼 (LOOCV 0.975, √φ_eff·CN²·…) | ★ **실험 앵커**: AM↑·SE부피↓ → σ_ionic 급락 (우리 SE-poor 코너 검증점) |
| **σ_e vs AM%** | **38.6/54.8/65.2 (AM 80/85/90)** = AM↑→σ_e↑ | 우리 σ_e Stage 22.5 (φ_AM⁴·…), σ_AM 앵커 | ★ **σ_e/σ_ionic 트레이드오프** 절대 앵커 (AM의 σ_e > SE) |
| **σ_e vs carbon%** | carbon↑→σ_e↑ (Fig S3b) | 우리 CBD σ_e 기여 | ★ carbon 전자망 = 우리 CBD 효과의 실험 정합 |
| **sphere vs fiber** | ★ **SC(구) 0.087 / CF(섬유) 0.105 σ_ionic**(σ_e 동급) | 우리 CBD morphology (SuperP 구 vs VGCF 섬유) | ★ **morphology(구→섬유)가 σ_ionic 좌우** = 우리 CBD 형상축 직접 검증 (Lee 2025 SuperP 0.0168<VGCF 0.0298 σ_e와 결 같음) |
| **고-AM(>90 wt%) 레짐** | ★ **SE-poor + carbon 점유 = 최악**(σ_ionic·열화·율속) | 우리 mono-large/SE-poor porosity 연구 (DEM ε_sphere 과압축 코너) | ★ **carbon이 SE-poor를 더 악화** — 우리 SE-poor 신뢰성 맵에 carbon 점유항 추가 동기 |
| **열화 메커니즘** | ★ **carbon 표면 SE 산화분해 → 저항 부산물(P-O-P/SOₓ)** = *화학* 열화 | 우리 DEM+MPM = *구조* 열화(균열/Auerbach/void) | ★ **이 채널은 우리 미보유** — "계면 화학 열화" 향후 축 (§10) |
| porosity 정량 | 없음 (밀도→vol%만) | DEM 15.6% / MPM 16.7% @300 (Minnmann 10%) | 그들 압밀 porosity 안 줌 → **우리 강점**(정량 porosity·Heckel) |
| 전달 솔버 | 없음 (DC 분극 실측) | Kirchhoff/Holm + Stage-E + 삼중항 σ_i/σ_e/σ_thermal | **우리 강점**(명시적 접촉망·삼중항 스케일링) |
| morphology/변형장 | SEM/TEM 정성 | MPM 진짜 소성 형상변화·void-fill·Σdg | **우리 강점**(MPM 정량 변형장) |

## 8. 적용 인사이트 (내 연구에 어떻게) — ★ 우리 랩 trend 정렬
- ① **★ carbon = SE 도메인 *부피 점유체*로 모델 (Stage-2/CBD 1순위 흡수)**: ρ_carbon 0.67 ≪ ρ_SE 1.86 →
  carbon은 g당 SE의 ~2.78× 부피를 차지.  우리 DEM/MPM에서 carbon을 *inert·무시*가 아니라 **SE 영역을 빼앗는
  저밀도 입자/coating**으로 다뤄야 한다.  → **backlog A4(se_coating carbon)**: carbon을 SE 표면 coating으로 넣어
  *유효 SE 부피·접촉면적*을 줄이는 모델; **backlog A3(binder --coh)**: PTFE/carbon 응집의 부피·접촉 효과.
  이 논문이 그 부피 점유를 **정량(SE 30.0→13.9 vol%, σ_ionic ≈1/10)**으로 줘서 보정 타깃이 생긴다.
  `docs/data/kim2024_carbon_volumetric_occupation_se_domain.csv`.
- ② **★ 고-AM(>90 wt%) SE-poor 레짐 = 우리가 모델하는 코너 → carbon이 더 악화**:
  우리 `docs/mpm_scaffold_reliability_and_am_freeze.md`의 mono-large/SE-poor 코너(SE/sol↓ → 과압축·신뢰성 분기)에
  **carbon 부피 점유항을 추가**하면 "SE-poor에서 carbon이 σ_ionic을 추가로 죽인다"는 실험 trend(Fig 1c,1e)를
  재현하는 검증이 된다.  우리 porosity/σ 관계식에 *carbon vol% 점유*를 SE 유효분율 감소로 넣을 근거.
- ③ **★ σ_e↑ vs σ_ionic↓ 트레이드오프 = 우리 삼중항의 실험 앵커**: Fig 1c/1d (AM 80/85/90 → σ_ionic
  0.125/0.0458/0.0138 *내림* + σ_e 38.6/54.8/65.2 *오름*)는 우리 σ_ionic(SE backbone)·σ_e(AM backbone)
  삼중항이 *반대 방향으로 움직인다*는 실험 증거.  → 우리 σ_ionic·σ_e 폼을 *같은 케이스에서 동시에* 검증할
  교차 앵커(단, 그들 carbon 3 wt% 포함·DC분극 → φ_SE·접촉 매핑 후 절대비교).
- ④ **★ sphere→fiber morphology가 fix = 우리 CBD 형상축 직접 검증**: SC(구) 0.087 < CF(섬유) 0.105 mS/cm σ_ionic
  (+22%, σ_e 동급)는 **자매 논문 Lee 2025**(VGCF 섬유 vs SuperP 구; SuperP 0.0168 < VGCF 0.0298 mS/cm σ_e)와
  같은 결: **morphology가 전달을 좌우**.  우리 CBD morphology 모델(SuperP 구형 노드 vs VGCF 섬유망)이
  *literature-grounded*임을 두 논문이 *같은 랩에서* 뒷받침.  단 여기선 CF가 σ_ionic을 구제(SE 도메인 덜 점유)이고
  Lee는 σ_e를 다룸 → **두 논문 합치면: 섬유 = σ_e 망 형성 + σ_ionic SE 도메인 보존 둘 다**.
- ⑤ **★ Bielefeld 2020(바인더/CBD가 SE 망 차단)의 실험 랩 대응**: Bielefeld 2020
  (`docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md`)이 *연속체 flux-PDE*로 바인더/CBD가 SE 이온망을
  막아 σ_eff↓·τ²↑임을 *모델*로 보였다면, 이 논문은 그 **부피 점유를 *실험으로 정량*(carbon vol%↑ → SE vol%↓ →
  σ_ionic↓)**.  → 우리 "carbon/binder가 SE 망을 막는다" 모델의 **실험 검증점**.  Bielefeld는 LCO+LGPS(절대 전이
  금지·추세만)였으나 이 논문은 **우리 소재(NCM811+LPSCl)** → 추세·메커니즘 직접 비교 가능.

## 9. 인용 가능 문장 (deck/paper용)
- "From the same laboratory, Kim et al. (Adv. Funct. Mater. 2024) quantify that the low-density conductive
  carbon (ρ = 0.67 g cm⁻³) volumetrically occupies the dense sulfide-SE domain (ρ_SE = 1.86 g cm⁻³): as the
  active-material content rises 80 → 90 wt%, the retained SE falls 30.0 → 13.9 vol% and the electrode ionic
  conductivity collapses to ≈1/10 (0.125 → 0.0138 mS cm⁻¹) — the experimental basis for treating carbon as an
  SE-domain occupant (not inert) in our CBD/Stage-2 model."
- "The carbon additive trades the two transport channels against each other: raising AM 80 → 90 wt% raises the
  electronic conductivity (38.6 → 65.2 mS cm⁻¹) while collapsing the ionic — an experimental anchor for the
  opposing AM-backbone (σ_e) / SE-backbone (σ_ionic) behavior our triad predicts."
- "Replacing spherical carbon (SC) by 1D carbon fiber (CF) recovers +22 % ionic conductivity (0.087 → 0.105
  mS cm⁻¹) at equal electronic conductivity and ~6× lower SE oxidative current — a sphere-to-fiber morphology
  fix that directly validates our CBD morphology axis (SuperP vs VGCF) across two papers from the same lab."

## 10. 주의/한계 (over-claim 방지)
- **시뮬레이션 0** — DEM/MPM/FEM/RNM 없음.  porosity(정량)·Heckel·coordination Z·coverage%·E_SE·σ_y·접촉면적·
  τ **전부 n/a**.  SE vol%(30.0/13.9)는 *밀도·조성 계산값*이지 측정 porosity 아님 → 우리 15.6% 압밀 porosity와
  직접 비교 금지(전자는 *상 부피분율*, 후자는 *공극*).
- **σ는 DC 분극**(정전류/정전압)이지 EIS-TLM 아님 → Bazzoun·Kim2025의 TLM σ와 측정법 다름.  절대값은 *추세·트레이드오프
  형태*로 흡수, 셀 형상·carbon 함량(3 wt%) 보정 후에만 우리 φ_SE 케이스에 매핑.
- **carbon 함량 차이**: 펠릿은 carbon **3 wt%**(σ vs AM% 스윕), 건식·SC/CF 비교는 **1 wt%** → σ 절대값을 함량 가로질러
  옮기지 말 것.  우리 케이스(보통 carbon 1 wt%)는 1 wt% 데이터(0.087/0.105)에 매핑.
- **열화는 *화학(산화분해)* 채널** — carbon 표면이 황화물 SE를 산화시켜 저항 부산물(P-O-P/SOₓ) 형성.  **우리 구조
  DEM+MPM은 이 채널을 모델하지 않음**(우리는 균열/Auerbach/void = *역학* 열화).  → "interfacial chemical degradation"은
  **향후 별도 축**으로 flag; 현재 모델로 이 열화를 재현한다고 주장 금지.  (자매 Kim2025 TLM의 R_ct 산화분해 kinetics가
  이 화학 열화의 *임피던스* 짝.)
- **BET 정규화 산화율 SC≈CF** (Fig S6): CF의 이점은 *표면화학*이 아니라 *부피 점유·총 접촉면적 감소*임 — "CF가 본질적으로
  덜 반응한다"가 아니라 "CF가 SE와 덜 접촉한다"로 정확히 표현(우리 coverage/접촉면적 축과 연결).
- **PSD·E_SE·소성**: SC/CF 입경·SE 탄성·소성 데이터 없음 → 우리 DEM/MPM 입력으로 직접 쓸 수치 아님(메커니즘·트렌드만).
- **frame[4]/[5]**: 이 논문은 *실험 절반*(전달 DC분극 + morphology SEM/TEM + 화학 XPS)을 줌; *모델 절반*(명시적 접촉망 σ
  삼중항·MPM 변형장·Auerbach·Heckel·정량 porosity)은 **우리가 추가**.  수렴=교차검증, carbon 함량·측정법 차로 인한
  불일치=정량화된 효과.  **carbon=SE 점유체**·**sphere vs fiber**·**σ_e/σ_ionic 트레이드오프** 세 메시지가 흡수 핵심.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
