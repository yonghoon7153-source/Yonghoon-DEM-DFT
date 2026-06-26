# 🔬 문헌 ↔ 우리 DEM+MPM — 차이 + 적용 인사이트

> 기준값: `our_dem_baseline.md`. 각 축마다 "문헌이 뭐라 하나 / 우리가 뭐라 하나 / 왜 다른가 / 어떻게 쓰나".
> 현재 digest(7): Varkey2026·So2021·Martin-Bouvard2003·Bouvard2000(압밀), Bazzoun2026(전달),
> McGeary1961(패킹), **Lee2025(실험 앵커 — 우리 소재·도전제 전부 동일)**. elasto-plastic 종합 = `elasto_plastic_feasibility.md`.
>
> ★ **Lee2025 (Nat. Commun. 2025, UCSD+LGES)** 는 유일하게 **우리와 완전히 같은 소재계**(LPSCl + NCM811/82 +
> **VGCF + PTFE** 둘 다)의 **순수 실험** 막 논문 → 시뮬 경쟁 아니라 **frame[4] 외부 실험 앵커**.  세 곳에 매핑:
> (B) PTFE% σ 페널티 + 조성별 σ 실측 = 우리 σ_e/σ_ionic·Stage-2 보정/검증; (C) binder-VGCF fibril망 = 우리 CBD
> morphology 모델 검증 + PC/SC-NCM 균열 = 우리 AM 파괴 검증.  데이터 `docs/data/lee2025_transport_anchors.csv`.

## A. 압밀 / porosity (E_SE 강성이 floor를 정한다)
- 문헌: Varkey(halide E=10.58) separator floor **21 %** / cathode **37 %** @350 MPa (강체 구, <20 % "추구 안 함").
- 우리: LPSCl pure-SE **~10 %** @300, real_14 **15.6 %** — 같은 압력 **약 2× 더 치밀**.
- ★ **porosity 앵커 출처 정정(Minnmann 2022 digest §0):** "Minnmann porosity 14 %/13–17 %"는
  **Minnmann *2022* AEM Perspective가 아니라 Minnmann *2021* JES 040537**(NCM622+LPSCl, **380 MPa**,
  EIS-TLM; avg 14 %, range 13–17 %, σ_ion_eff 0.17 mS/cm, τ_ion 2.07)에서 옴. **밀도 87 %@300 MPa =
  Sakuda 2013**(75Li₂S-25P₂S₅). **pure-SE 10 % = 우리 MPM 3D(σ_y 0.30) 보정 수렴값**(2021 JES/Sakuda
  cold-press 거동 위). 2022 Perspective는 **porosity 수치 0개(전부 정성)** — 수치 cite 시 *반드시*
  2021 JES/Sakuda를. (+ refs.bib @Minnmann2021이 엉뚱한 040502/abf3a3 가리킴 → 040537/abf8d7 정정.)
  ⇒ 압력 구분 필수: 우리 **300 MPa = 제조(cold-press)**, 작동은 **수~수십 MPa**(2022 Perspective 명시).
- 왜 다른가: (a) halide E가 우리 E_eff 1.35보다 ~8× 뻣뻣 → 더 높은 잔류 porosity (우리 MPM E-sweep과 정합);
  (b) 우리 DEM 연화 + MPM 소성 흐름이 강체 구 floor(~20 %) 아래로 도달.
- 인사이트: **우리 porosity 관계식에 E_SE(강성) 항 + 조성 항 필수.** ~20 %는 강체 구 하드 floor.
  Heckel `ln(1/(1−D))=K·P+A` 후보 (우리 R²=0.965, P_y=138). 둘 다 ~100 MPa 탄성→소성 무릎 (= 우리 P_y).
- **So 2021** (LPS+Si, real E=24 + **H-cap** F_th=2/3·H·A_con): 연화 없이 rel.density 0.30→**0.98**@600 MPa →
  **항복캡이 우리 18× 연화 역할**. ⇒ '연화 irreducible'은 강체 구 본질이 아니라 *우리 DEM에 항복캡 없는 탓*
  (`elasto_plastic_feasibility.md`). Varkey '<20% 안 함'도 물리 floor 아닌 계산비용.
- **Bouvard 2000**: 경상↑ → 고압 porosity↑ (Astroloy 0.995→0.86 @0→35 vol% alumina) = 우리 AM↑→porosity↑;
  '온도↑→σ_y↓→압밀↑'은 우리 E_eff 연화의 실험적 정당화. **Martin–Bouvard 2003**: 거시응력이 E₂/E₁=10→100서
  <3% 변화 → **rigid-AM 가정 외부 면허**.

## B. 전달 삼중항 — σ_ionic은 교차검증, σ_e/σ_thermal은 우리만
- 문헌(Bazzoun, **LPSCl 동일소재 + LIGGGHTS 동일코드**): RNM = 우리 Holm/Kirchhoff 그대로
  (R=1/(2σr_c), Σ(φi−φj)/R=0). 실험 σ_eff,ion **0.137/0.101/0.065 mS/cm @ f_CAM 70/75/80** (400 MPa, EIS).
- 우리: 같은 솔버 물리. 추세 일치 — 작은 SE→σ↑, CAM↑→σ↓, 압력↑→σ↑(~400 포화 ≈ 우리 P_y 138).
- 차이: 그들 RNM은 **구속저항만**(field spreading 없음) → 고-CAM서 과소(80 % RNM 0.031 ≪ exp 0.065);
  우리 Stage-E 소성 접촉면적이 이 과소를 일부 보정. 그들은 σ_e/σ_thermal 없음(우리 삼중항 우위).
- 인사이트: **Bazzoun 실험 σ_eff,ion = 우리 σ_ionic의 외부 절대 검증점** (그들 vol% CAM:SE → 우리 φ_SE 매핑 후).
  "missing direct validation"(다중압력 LPSCl σ_ionic) 확보.
- **★ Lee 2025 (LPSCl + NCM811/82 + VGCF + PTFE, 실험)**:
  - **PTFE wt% σ 페널티 곡선** (Supp Fig 5, CAM:SSE:VGCF 80:17:3 고정, 75 MPa):
    PTFE 0.5 / 2 / 5 wt% → **σ_ionic 0.069 / 0.024 / 0.007 mS/cm** AND **σ_e 34 / 4.5 / 0.011 mS/cm** (≈3,000×↓).
    → ★ **우리가 못 갖던 데이터**: 우리 σ_e/σ_ionic 폼은 도전제 *추가*만 반영하고 **바인더가 접촉 막고 절연**하는
    페널티가 없음.  **Stage-2 흡수 1순위** — CBD가 σ_e에 *기여*(VGCF망)하면서 PTFE wt%↑면 **양쪽 다 급감**하는 비단조성.
  - **조성별 절대 σ 실측** (0.5 wt% production 양극): σ_ionic **0.076** (co) / 0.069 (free), σ_e **33–34** (VGCF망) mS/cm
    → 우리 σ_ionic(LOOCV 0.975)·σ_e(0.953) 폼의 추가 외부 절대점 (단 그들 VGCF 3·PTFE 0.5 wt% ≠ 우리 1·1 → 함량 보정 후 매핑).
  - **bulk LPSCl σ_ionic = 2.19 mS/cm** (pristine pellet) / 1.64 (ball-mill <1 µm) → Bazzoun pellet **1.02**·Cronau 단결정
    **3.0** 사이 = **세 번째 LPSCl bulk 앵커** (측정·입자·GB 차이 스프레드로만 사용, 절대 직접대조 금지).
  - 차이/주의: 실험이라 **솔버 없음**(우리 Kirchhoff/Holm·삼중항 σ_i/σ_e/σ_thermal 우위 유지); σ_ionic(SSE) 1.04(co)<1.29(free)는
    압밀 차 아니라 **측정 형상차**(free 500 µm vs co 50 µm) — intrinsic σ 비교 주의.

## C. 역학 / morphology — MPM 고유 (문헌 DEM은 형상 못 바꿈)
- 문헌: Varkey "elasto-plastic"은 **CONTACT 힘법칙만**(Thornton–Ning), 입자는 완벽 구 — "구=타협,
  현실 형상=향후 과제" 명시. Bazzoun도 구만.
- 우리: MPM 진짜 소성 형상변화(SEM 일치), void-fill flow, Σdg 변형장.
- 왜: 강체 구 DEM·단상 연속체는 granular 재배열을 못 잡아 둘 다 연화 럼핑 필요 (frame [1]/[2]).
- 인사이트: **morphology·소성 floor(<20 %)·변형장 = 우리 MPM이 메우는 간극** (Varkey가 스스로 인정 = frame[5] 확증).
- **Martin–Bouvard 2003** 2-메커니즘 분해: 경상 force-network(K_h≈1.3@20→1.8@40 vol%, N₂₂/N₁₁→3.5) = 우리
  AM load-shielding / 연상 excluded-volume 과변형(+20–40%) = 우리 MPM void-fill → **복합 porosity 관계식 두 항**.
- **So 2021** Fig5–6: Si AM-AM 응력집중(2.5→5.9 GPa, overlap 0.007)·SE-SE는 H_SE 캡 = 우리 real_14 AM-shielding
  (SE overlap 1.75%)을 다른 소재로 독립 재현.
- **★ Lee 2025 (실험) — 우리 MPM/CBD/파괴 모델의 실험 검증 (frame[4])**:
  - **binder-VGCF fibril 망 SEM** (Fig 3h,i + Supp Fig 17/18): 계면을 가로지르는 **꼬불꼬불(squiggle) 곡선 섬유망**이
    VGCF를 그물치고 SSE-전극을 잇는 것을 *실측* + 5단계 fibrillation 모식(접촉→shear 이동→stretched&fibrillated→
    새 접촉→반복).  → ★ **우리 PTFE CBD 모델의 실험 검증** (`docs/cbd_morphology_roadmap.md` batch1: **curl(worm-like) +
    nucleate-on-carbon + shear-draw d∝√(V/L)**) — 우리 시드 모델이 *literature/실험-grounded*임을 직접 인용 가능.
    단 그들은 *막 제조 shear* 공정 — 우리 RVE는 그 공정을 재현 안 함(개념 검증으로만 사용).
  - **PC-NCM 균열 / SC-NCM 무손상** (Fig 2b,c + Supp Fig 6–8, 300→500 MPa서 PC 균열↑·debris): → ★ **우리 DEM
    AM_P(다결정) 파괴(92:8 8mAh서 37–40%)·AM_S rigid 가정의 실험 라이선스** (Auerbach/fracture-Holm 검증점).
    PC는 *진짜로 깨지고* PTFE는 *진짜로 소성 draw* → rigid-sphere 한계를 우리 MPM(형상)·fracture(균열)가 메우는 게 옳다는 실험 근거.
  - **바인더 연화 DMA 67%↓**(30→120 °C, Supp Fig 10) = 우리 E_eff 18× 연화의 *바인더 측* 물리(온도↑→σ_y↓→압밀↑, Bouvard2000과 결 같음).
  - 우리 우위(그들 없음): 정량 porosity·Heckel·coordination·coverage% · MPM 정량 변형장 Σdg·void-fill flow ·
    명시적 접촉망 σ 삼중항.  그들 void는 *사이클 후 계면 void 상대비*(ImageJ)지 압밀 porosity 아님 → 우리 15.6%와 직접 비교 금지.

## D. 패킹 / Furnas dip — DEM·기하 소유, 소성 MPM 불가
- 문헌: Varkey RCP/rigid → dip @ AM 70–80 wt% (de Larrard 기하). Bazzoun 작은 SE→packing↑→σ↑(size=packing).
- 우리: DEM·de Larrard dip @ AM 70–85; **소성 연속체 MPM은 dip 재현 못 함**(material sweep로 증명, frame[4]).
- 인사이트: dip은 초기 강체 구 패킹(기하)에 산다 → DEM(또는 de Larrard)이 소유. porosity-incl-dip은 DEM.
- **McGeary 1961**(Furnas-dip 실험 원전, **소성변형 없음** 명시): 1size 62.5→binary 86(임계비 d_c/d_f≥**7**,
  삼각공극 0.154·d_c)→ternary 90→quaternary 95.1%. 우리 AM:SE 12:1(≫7, dip 깊음)·4:1(<7, 부분충전)이 조성별
  dip 깊이를 McGeary 무릎으로 설명 → **(조성×크기비) 기하항**(E-stiffness 항과 별개) 근거.
- **So 2021** φ_SE^crit=**0.13**(ball-milled aggregate) vs 우리 σ_ionic φc 0.195–0.20(mono) → 응집이 저-φ 침투
  허용 = SE-dispersion 축 후보. **Bouvard 2000** percolation 임계 = f(크기비): 0.32(r=1)→0.18(r=2) = dip의
  rigid-skeleton 기하 기원(alumina inclusion 균열이 하중분담 증거).
- **★ Minnmann 2022(설계 Perspective, 정성)**: **tailored(bimodal/multimodal) PSD가 모든 축
  (확산·전자·이온 percolation·계면열화·GB) 최적**(Fig 6 4분면) + **작은 SE + 큰 CAM/SE 비 = 패킹밀도↑**
  (§3.1) → ★ **우리 bimodal 12:4:1 + Furnas dip의 권위 있는 정성 근거**. 단 *dip 위치/깊이는 이 논문에
  없음*(정성 "bimodal이 좋다"까지) → McGeary/de Larrard 기하(우리)가 *정량*을 소유. 우리 차별점 =
  정량 dip(AM 70–85 wt%)을 추가. **CAM 60–70 vol% 최적**(§2.1)이 우리 production core(AM 70–85 wt% ≈
  SE 30–50 % of solid)와 정합.

## E. 우리 계산이 문헌을 "검증/교차검증"하는 지점 (강점으로 쓸 것)
- Bazzoun RNM(Holm+Kirchhoff) = 우리 네트워크 솔버 → 같은 물리, 추세 일치 (frame[4] 독립 교차검증).
- Bazzoun 실험 σ_eff,ion + 다중압력 = 우리가 부족했던 **외부 실험 앵커** 제공.
- Varkey E_SE=10.58·floor 21/37 % = 우리 "E 강성 → floor" 가설의 stiffer-SE 데이터점.
- Varkey 탄성→소성 무릎 ~100 MPa = 우리 Heckel P_y 138 재현(소재 일반성).
- ★ Minnmann 2022 §5.4 = Janek 그룹 리뷰가 **"미세구조 mechanical model을 echem·thermal과 결합 + CAM을
  다른 형상·크기·탄성으로 재고"를 명시 요구** → **우리 DEM(transport σ 삼중항)+MPM(소성 SHAPE morphology)
  분업이 그 권고의 직접 구현**. "구형 CAM 권고 + 비구형 재고"는 우리 MPM SHAPE 소성 간극 + Varkey/Bazzoun
  "구=타협" 한계와 같은 계보 → **frame[5] 분업이 문헌 권위로 정당화.**

## F. 우리가 아직 못 하는 것 / 흡수할 것 (정직 목록 → 향후)
- **FEM 연속체 transport 기준** 없음 (Bazzoun COMSOL 보유) — RNM↔FEM 대조틀 흡수 가치.
- **다중압력 Heckel(LPSCl powder) 실측** — 우리 직접앵커 부족; Bazzoun σ-vs-P / Varkey P-vs-porosity로 보강.
- **명시적 바인더(SBR/CB/PTFE) 역학·이온저항 R_b** — Varkey/Bazzoun 보유, 우리 미모델.
- **multi-contact 구속항 F_mc** (Varkey) vs 우리 18× 연화 — 같은 증상(ρ>0.7 과강성) 다른 처방, 비교연구 거리.
- **항복캡 접촉**(So 2021 H-cap / Thornton–Ning p_y) — real E로 18× 연화 **제거** 가능 경로(1순위, `elasto_plastic_feasibility.md`).
- **비구형 입자**(Bouvard 각질 inclusion이 압밀 더 방해; Martin–Bouvard truncated sphere = SHAPE flow 없음) —
  우리 DEM·MPM 둘 다 구만 = 23년째 문헌 공통 한계(M&B2003→Varkey2026→Bazzoun2026), frame[5] 일관 확증.
- **Storåkers 소성 접촉면적** A=2πc(m)²rh (Martin–Bouvard, c(m) 0.5→1.45) — 우리 Stage-E(Tabor+volume)와 A/B 비교 거리.

---
## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
