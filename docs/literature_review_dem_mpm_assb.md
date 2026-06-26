# 📖 전고체전지 복합양극 DEM+MPM 모델링 — 문헌 종합 리뷰

> 작성 2026-06-27.  litdb 60편 digest( `litdb/papers/` ) + 기존 docs 노트를 **우리 DEM+MPM 프레임 기준으로** 한 편의
> review로 종합.  각 섹션은 (i) 문헌이 무엇을 말하나 → (ii) 우리가 무엇을 하나 → (iii) 왜 다른가 →
> (iv) 우리 위치·novelty(frame[4]/[5]) 의 흐름.  상세 수치·식은 각 `papers/<slug>.md` 와 `docs/data/*.csv` 에.
>
> **핵심 명제(전편 관통):** 전고체 복합양극의 *구조→수송* 절반은 우리 DEM(접촉망 Kirchhoff/Holm σ-삼중항)이,
> *소성 형상·void-fill* 절반은 우리 MPM(J2)이 소유한다.  60편 중 **단 한 편도 이 둘을 동시에** 갖지 않는다
> (대부분 강체 구 + 단일 σ 채널 또는 σ 미산출).  = frame[5] 분업이 *문헌으로 확증*됨.

---

## 0. 우리 모델 한눈에 (리뷰의 기준점)

| 축 | 우리 구현 | 핵심 |
|---|---|---|
| **DEM 접촉 LAW** | LIGGGHTS hooke/hysteresis (= Luding 2008 정의), **항복캡 없음** → E_eff **1.35 GPa (real 24의 18× 연화)** | 강체 구 + overlap(ε_sphere) = 소성 프록시 |
| **Stage-E** | 탄성 overlap → **소성 접촉면적 재유도**(Tabor A=F/H + volume, 5-regime cap) | 강체구 위 *2차* 소성 보정 |
| **수송 솔버** | **Kirchhoff Σ(φᵢ−φⱼ)/R=0 + Holm 1967 constriction R=1/(2σr_c)** → **σ_ionic·σ_e·σ_thermal 삼중항** | 명시적 접촉망(대부분 peer는 ionic-only 또는 σ 미산출) |
| **σ_grain 문헌보정** | Cronau(r_SE) · Trevisanello(NCM 결정도) · Wang(phonon GB) | 재료-앵커 절대 σ |
| **파괴** | Auerbach P_c + Lawn 1998 multipliers(1/3/11/32) → f_intact → fracture-aware Holm | 압밀 접촉응력 기반 AM 균열 |
| **MPM** | Taichi MLS-MPM, **von Mises J2, ν=0.49**(stiff bulk + soft shear) | 진짜 소성 형상변화 + void-fill |
| **DEM↔MPM 결합** | scaffold(real DEM AM freeze + SE만 MPM 재료) | 이산 패킹(DEM) × 소성 형상(MPM) |
| **scaling law** | σ_ionic LOOCV **0.975** / σ_e **0.953** / σ_thermal **0.90** | 솔버→설계 predictor(ML) |
| **epistemology** | **frame[4]**: DEM·MPM 각각 *실험*에 독립 보정(서로 cross-fit 금지) / **frame[5]**: DEM=수송·패킹·dip, MPM=형상·void-fill | 일치=교차검증, 불일치=정량화된 모델한계 |

---

## 1. 문헌 분류표 (60편 + docs 앵커)

| 카테고리 | 편수 | 대표 논문 (slug) |
|---|---|---|
| **★필독 랩 자체논문**(Hanyang J-W Lee) | 7 | Yun2023(degradation capstone)·Kang2025·Kim2025·Kim2024·Cho2024·Kang2023·Jung2023 |
| **ASSB 압밀·수송 DEM** | 10 | So2021-coldpress·So2022-contact·So2021-fab+deg·So2022-coated·Bazzoun2026·Bazzoun2025·Varkey2026·Huang2025·Lee2024-multiphysics·Nisar2024 |
| **분말 압밀(일반)** | 3 | Martin-Bouvard2003·Bouvard2000·McGeary1961 |
| **LIB 제조 DEM + LIGGGHTS** | 10 | Sangrós2019·Sangrós2020-mech·Sangrós2020-elec·Ngandjong2021·Lyu2025·Schreiner2020·Frankenberg2024·Shenouda2020·Bosch2014·Weitze2024(wet-resolved) |
| **구조모델링·percolation** | 4 | Bielefeld2019·Bielefeld2020·Chen2011·Reisacher2023 |
| **실험 1차 앵커** | 9 | Minnmann2021·Minnmann2024·Doux2020·Cronau2021·Sakuda2013·Schneider2023·tailored-low-P(Zhou2025)·Shi2019·Lee2025-corolling |
| **사이클 파괴·계면 frame[5]** | 5 | Bucci2017·Bucci2018·NMC811입계균열·So2021-fab·DEM-cycling-stresses(Alabdali2024) |
| **접촉모델·소성 LAW (DEM)** | 10 | Luding2008·EEPA(Thakur)·Pasha2014·ThorntonNing1998·KogutEtsion2002·JacksonGreen2005·MesarovicFleck2000·Storåkers1997·DMT1975·electromech-contact(Zhang2024) |
| **MPM 소성 계보** | 3 | Stomakhin2013·Klár2016·deVaucorbeil2020 |
| **전달 솔버 peer(σ resistor-network)** | (교차) | Bazzoun2026·Nisar2024·Sangrós2020-elec·electromech·interfacial-impedance(Choi2024)·Huang2025(LBM) |
| **수송 도구** | 1 | TauFactor(Cooper2016) |
| **dry-process 리뷰** | 2 | Mun2025·Liu2025 |
| **설계 Perspective/리뷰** | 2 | Minnmann2022·Deysher2022 |

---

## 2. §A 압밀 / porosity — **E_SE 강성이 floor를 정한다**

**문헌.**  강체 구 DEM은 porosity ~20%에서 멈춘다: Varkey 2026(할라이드 E=10.58 GPa)은 separator floor **21%** /
cathode **37%** @350 MPa, "<20%는 추구 안 함"(계산비용).  Bazzoun 2025(Mercedes, NMC532)는 한술 더 떠 **high-f_CAM
(80–85 wt%)에서 강체구 DEM이 porosity를 *과소예측* + 민감도 폭증**한다고 *스스로 인정*하며 원인을 "미모델 형상·소성·믹싱"
으로 지목한다.  실험 앵커는 더 낮은 floor를 준다: **Doux 2020** LPSCl 펠릿 **18%**@370 MPa(같은 SE!), **Minnmann 2021
JES** 복합양극 **13–17%**@380 MPa(NCM622+LPSCl), **Sakuda 2013** 황화물 유리 ">90%@>350 MPa"(porosity<10).
**Schneider 2023**(t-Li₇SiPS₈)은 ★ "**porosity는 σ의 *약한* descriptor이고 PSD가 *강한* descriptor**"라는 결정적 결론
+ Heckel P_y 0.95/1.65 GPa(작은/큰 PSD)을 준다.

**우리.**  LPSCl pure-SE **~10%**@300 MPa, real_14 복합 **15.6%** — 같은 압력에서 **약 2× 더 치밀**.  reliability
코퍼스(105+ 케이스)에서 production-core(AM 70–85 wt%)는 DEM↔MPM이 ±1–3%p로 일치.

**왜 다른가.**  (i) 할라이드/실재료 E가 우리 E_eff 1.35보다 ~8× 뻣뻣 → 높은 잔류 porosity(우리 MPM E-sweep과 정합);
(ii) 우리 DEM 18× 연화 + MPM 소성 void-fill이 강체구 ~20% floor *아래로* 도달.  ★ **So 2021**(LPS+Si, real E=24 +
**경도캡** F_th=2/3·H·A_con)은 연화 없이 rel.density 0.30→**0.98**@600 MPa를 달성 → **항복캡이 우리 18× 연화 역할을
대신**한다는 직접 증거.  즉 "연화 irreducible"은 강체구 본질이 아니라 *우리 DEM에 항복캡이 없는 탓*(경로A로 풀 수 있음).
**Bouvard 2000**(경상↑→고압 porosity↑)·**Martin–Bouvard 2003**(거시응력이 E₂/E₁=10→100서 <3% 변화 = rigid-AM 면허)이
복합 porosity 관계식의 2항 구조를 뒷받침.

**우리 위치.**  porosity 관계식은 **E_SE(강성)항 + 조성항 + Heckel knee(P_y≈138)**가 필수이며, ~20%는 강체구 하드 floor.
우리는 그 floor를 *깨는* 유일한 쌍(softened-DEM + plastic-MPM).  ⚠ 압력 3종 구분 필수: **제조(300–490 MPa, 압밀/Heckel)
≠ 측정(40 MPa) ≠ 작동(5–70 MPa, 계면접촉/creep)** — Doux·Cronau·Minnmann·Lee2025가 합의.

---

## 3. §B 전달 삼중항 — **σ_ionic은 교차검증, σ_e/σ_thermal은 우리만**

**σ_ionic 외부 절대 앵커(frame[4]).**  같은 NCM/LPSCl 계에서 실험 σ가 우리 DEM σ_ionic(0.04–0.18 mS/cm)을 *둘러싼다*:
**Minnmann 2021** 0.17 @42 vol% NCM(+ τ_ion 2.07=√(τ²=4.3), Eq4 = 우리 τ_Laplace,eff 정의), **Bazzoun 2026**
0.137/0.101/0.065 @f_CAM 70/75/80(EIS@400 MPa), **Kim 2025**(우리-랩) R_ion 분해 62/72/82 wt%, **interfacial-impedance
(Choi/Samsung 2024)** TLM 분해.  bulk LPSCl σ 앵커 스프레드 {Cronau 3.0(단결정) · Lee2025 2.19 · Minnmann/Kim2025 1.6 ·
Bazzoun 1.02(펠릿)} — 절대 직접대조 금지, 스프레드로만.

**솔버 골격이 우리와 동일(frame[4] 독립 재현).**  네 편이 우리 `network_conductivity.py`의 골격을 *독립적으로 재현*한다:
- **Bazzoun 2026 (RNM)** = Holm/Kirchhoff 그대로(R=1/(2σr_c), Σ(φᵢ−φⱼ)/R=0), 같은 LPSCl·같은 LIGGGHTS.
- **Nisar 2024**(SPS 다공 금속) R_ij = R_i+R_j+R_c = 우리 R_bulk+R_constriction과 **byte-identical 골격**.  단 접촉항이
  *소결-neck 슬래브* πa²/δ_gb(부피보존 neck) — 우리는 *점접촉 Holm* 1/(2σa) + Mikic (1−a/r)^1.5.  cold-press 점접촉(a≪r)
  엔 Holm이 닫힌형-정확 → **우리 솔버가 두 regime(점접촉→소결-neck)을 다 포괄, 그들은 소결-neck만**.
- **electromechanical-contact (Zhang 2024)** R_c=(ρᵢ+ρⱼ)/(4r_c) = "the Holm model" = 우리 Holm과 정확히 일치 +
  Hertz r_c + Kirchhoff.  차이는 *탄성* Hertz 면적 vs 우리 *소성* Stage-E.  흡수후보: 그들 2상 Holm (ρᵢ+ρⱼ)/(4r_c)을
  우리 AM-SE 이종접촉에.
- **Sangrós 2020-elec**(LFP+CB+PEO) A* 최단경로 + 실린더 R=ρl/A = **정확히 우리 R_bulk** — 단 **Holm constriction을
  *생략***(= 우리 `bulk_only` 토글, pre-Holm 세대).  같은 그룹 Bazzoun 2026이 후속으로 Holm 추가.

**우리 위치.**  ★ **constriction이 우리 transport novelty의 정확한 위치**다.  Bielefeld 2020·Lee2024-multiphysics-FEM은
연속체 flux-PDE로 σ를 풀되 점접촉 수렴저항이 *없어 상한(upper bound)*; 우리 Kirchhoff/Holm이 그 아래로 깎는다.
Bielefeld 2019는 σ를 *아예 안 풀고*(percolation 존재까지, constriction을 "future work=Greenwood 1966"으로 명시) —
**바로 그 칸을 우리(+같은 그룹 Bazzoun)가 채운다**.  그룹-내부 진화 **Bielefeld2019(σ없음)→Bielefeld2020(연속체σ)→
Bazzoun2026(RNM/Holm)→우리(σ삼중항+MPM+Stage-E)**가 우리 위치를 증명.

**σ_e / σ_thermal은 우리 고유.**  대부분 peer는 σ_ionic만(또는 σ_e만).  **σ_thermal**: **Huang 2025**(DEM+3D
Lattice-Boltzmann, 산화물 LCO/LLZO)이 ETC를 LBM으로 풀어 "porosity/부피분율/입경 결정·tortuosity 비무시 → **3차
다변수 회귀 필요(단일 scaling 불가), EMT 실패 ±28–61%**"를 보임 = **우리 multi-pathway σ_thermal(Ridge 14-feat,
LOOCV 0.90) 주장을 *다른 방법·다른 소재로 독립 교차검증*** (단 thermal-only, 산화물).  **Reisacher 2023**(LPSCl+C65,
우리 SE!) **전자 percolation p_c≈4 wt% C65** = backlog A4 carbon-gate 직접 앵커(재료보정 없이 전이).

**도구.**  **TauFactor(Cooper 2016)**: τ=ε·D/D_eff = **우리 τ_Laplace,*bulk*** (constriction 없는 상한; τ_eff·τ_Dijkstra
아님) → 우리 voxel bulk-τ를 표준툴로 검증하는 cross-check(Huang도 TauFactor 사용 = 같은 스케일).  "우리 σ_ionic이
TauFactor bulk값을 넘으면 버그 신호"라는 validation.

**미보유 축(frame[5] kinetics).**  **Kim 2025 + interfacial-impedance(Choi 2024)**가 R_ct(전하전달)·C_dl(이중층)·
Warburg(고상확산)을 TLM으로 분해 = 우리가 *없는* kinetics 칸.  Choi가 흡수경로까지 제시: **R_ct = k_ct/A_AM-SE를 우리
Stage-E coverage 면적 위에** → ASR_total = ASR_ionic + ASR_electronic + R_ct + Z_low.

---

## 4. §C 역학 / morphology — **MPM 고유(문헌 DEM은 형상 못 바꿈)**

**문헌.**  battery DEM은 전부 강체 구다.  Varkey "elasto-plastic"은 *접촉 힘법칙만*("구=타협, 현실형상=향후과제" 명시);
Bazzoun·Sangrós·Lyu·Ngandjong·Schreiner·Frankenberg 모두 강체 구 + 접촉 소성(형상소성 없음).  ★ **Weitze 2024**(Franco,
NMC622+LPSCl wet-process)는 nano-CT로 ***실제 AM 형상*을 resolved multisphere로** 넣지만 **rigid**(인공 harmonic bond로
형상 고정) — 그리고 Fig 7에서 "**캘린더링이 AM-SE 계면을 못 키운다, 입자의 구형·강체 성질 때문**"이라고 *스스로 한계 인정*
= ★ **frame[1]/[2] 소성 흐름 가치의 가장 강력한 외부 증거**(실제 형상을 넣어도 rigid면 소용없다).

**우리.**  MPM J2가 진짜 소성 *형상*변화(SEM 일치: 코어보존+경계평탄화), volume-preserving void-fill flow, 누적소성변형장
Σdg를 준다.  scaffold가 DEM 패킹 × MPM 형상을 결합.

**왜 다른가.**  강체 구 DEM·단상 연속체 모두 granular 재배열을 못 잡아 둘 다 연화 럼핑이 필요(frame[1]/[2]).
**Martin–Bouvard 2003** 2-메커니즘 분해(경상 force-network + 연상 excluded-volume 과변형)·**So 2021** Si AM-AM 응력집중
(2.5→5.9 GPa)은 우리 AM load-shielding을 다른 소재로 독립 재현.

**실험 검증(frame[4]).**  ★ **Lee 2025**(LPSCl+NCM811+VGCF+PTFE, 우리와 완전 동일 소재계, 실험)이 우리 모델의 세 부분을
*직접 검증*: (a) binder-VGCF **fibril 망 SEM**(squiggle 곡선섬유) = 우리 CBD 시드 모델(curl+nucleate+shear-draw)의 실험
근거; (b) **PC-NCM 균열 / SC-NCM 무손상** = 우리 AM_P(다결정) 파괴·Auerbach의 실험 라이선스; (c) 바인더 연화 DMA 67%↓ =
우리 E_eff 18× 연화의 바인더측 물리.

**우리 위치.**  morphology·소성 floor(<20%)·변형장 = **MPM이 메우는 간극**, peer들이 *스스로 인정*(Varkey "향후과제",
Weitze Fig7, Bazzoun2025 high-f_CAM, Shi2019 "needs LPS plastic deformation") = frame[5] 확증.

---

## 5. §D 패킹 / Furnas dip — **DEM·기하 소유, 소성 MPM 불가**

**문헌.**  **McGeary 1961**(소성변형 없음 명시): 1size 62.5→binary 86(임계비 d_c/d_f≥**7**)→ternary 90→quaternary 95.1%
= Furnas-dip 기하 원전.  **Shi 2019**(Ceder, LIGGGHTS+Hertz, NMC532-LZO+LPS): **λ=D_CAM/D_SE**가 utilization을 지배,
λ_min 1.67@70wt%·2.1@75wt%; ★ **작은 SE = 낮은 intrinsic σ인데 *높은* utilization** = "size=PACKING not material-σ"의
실험+모델 증명, 그리고 "정확한 접촉면적은 *LPS 소성변형 모델링 필요*"라고 우리 Stage-E/MPM 칸을 명명.  **Chen 2011**(SOFC
analytic): 닫힌형 CN(Z)→percolation P→σ 체인 + poly-PSD가 percolation 임계를 낮춤 = 우리 CN²·φc·g_phys(size-gate)의
*해석적 근거*(⚠ broad-PSD가 TPB *connectivity*를 32% 약화시키는 것은 bimodal *density* 이득과 **직교 축**).

**우리.**  DEM·de Larrard dip @ AM 70–85 wt%; ★ **소성 연속체 MPM은 dip 재현 못 함**(material sweep로 증명).

**우리 위치.**  dip은 *초기 강체 구 패킹(기하)*에 산다 → DEM(또는 de Larrard/McGeary)이 소유, 소성 MPM은 어떤 보정으로도
재현 불가(frame[5] 정량 증명).  **Bielefeld 2019/2020**(단봉 PSD, bi/tri-modal 보류)·**Minnmann 2022**(정성 "bimodal이
좋다"까지)은 *dip을 안 다룸* → 우리 12:4:1 정량 dip이 그 빈칸을 채움.  porosity-incl-dip은 DEM.

---

## 6. §E 사이클 파괴 · 계면 역학 — **frame[5] 시간축(우리 압밀-Auerbach의 *사이클* 짝)**

> ★ driver 구분 필수: 우리 Auerbach = *압밀 접촉응력*(AM-AM, 압력 지배); 아래는 *사이클 intercalation strain*(Vegard,
> 압력항 없음/미미).  우리 MPM J2(연성)는 SE *취성* 균열·계면 박리 불가 → de Vaucorbeil continuous-damage/cohesive-MPM이 구현경로.

**연속체(FEM/analytic).**  **Bucci 2017**(MIT, ASSB 기계신뢰성 *최초* 정량) electro-chemo-mechanical FEM + cohesive-zone
SE 균열: 팽창<**7.5%** AND G_c≥**4 J/m²**서 균열방지, ★ **연한 SE(E~15)일수록 균열↑**(산화물>황화물 통념 반박).
**Bucci 2018** 1D 방사 cohesive 계면 *delamination*: 팽창 ~7.5%서 박리, **박리→ASR 임피던스↑**(50% 박리서 ×2.75) =
우리 Stage-E coverage의 *사이클 파괴*.  **NMC811 입계균열**(UCL nano-CT, 직접관찰): 다결정 중심핵 4V 균열→방사전파 =
*다결정 균열*의 직접 실험증거(Jung2023 단결정 대비짝).

**DEM(우리 파이프라인에 더 가까움).**  ★ **DEM-cycling-stresses (Alabdali/Franco 2024, ENSM)** — **LPSCl(우리와 동일!)
+ NMC532, LIGGGHTS Hertz**: 압밀 375 MPa → 작동 1/3/5 MPa → **AM 반지름 ±6% Vegard swing 5사이클** → 입자별 응력 evolution.
= 우리 frame[5] 칸의 **DEM 경로**(우리는 단일 300-MPa 스냅샷 응력만; 그들은 사이클 evolution).  같은 코드·같은 SE라
**직접 청사진**(backlog A10/B6: 압밀 후 `fix adapt`로 AM 반지름 swing → 우리 응력+Stage-E+fracture+삼중항을 위에 얹음).
**So 2021-fab+deg**(Si 280% 팽창, LPS)는 DEM 사이클 σ-loss(τ-dominated, 가역/비가역 축) = Bucci FEM-CZM의 DEM 사촌.

**우리-랩.**  **Kang 2025**(NCA, Voronoi 다결정+cohesive-zone damage D, ε_d=Ω/3·Δc_Li)는 *사이클* chemo-mechanics ↔ 우리
*압밀* J2 → 시간축 분업; **크기-의존 파괴**(큰 10µm 입자 c_Li 구배 ~10× → damage→1)는 우리 Auerbach를 입경-스케일링
(σ_crit∝1/√d)으로 보강할 근거(단 driver=사이클 Li-구배 ≠ 우리 압밀 접촉응력, 명시 분리).

**우리 위치.**  세 사이클-파괴 형제(Bucci FEM-CZM 취성 / So21 ductile-DEM / Alabdali stress-DEM) 모두 우리가 *없는* 시간축;
**우리는 압밀-시점 균열만**(Auerbach).  흡수: Alabdali Vegard-swing이 가장 구현 쉬움(A10/B6), SE 취성균열은 de Vaucorbeil
continuous-damage MPM 경로(D6).

---

## 7. §F 접촉모델·소성 LAW 층위 (DEM) — `contact_models_layer_map.md` 참조

**층위.**  우리 hooke/hysteresis는 **A층(no-cap 점착-탄소성 이력)** = **Luding 2008**(정의서) · **EEPA**(Thakur) ·
**Pasha** · 상용코드 사촌 EEPA(Schreiner).  **B층(항복캡=경로A LAW)** = **Thornton–Ning 1998**(Hertz→p_y→선형소성→잔류겹침,
Varkey 사용) + **So 2021/2022**(H-cap, area/spring factor, LPS 0.98 입증) + **Sangrós 2019**(★ **나노압입으로 항복비
YR=8.59e-3·x 직접 측정**, R²0.89 = 경로A YR 실측 LIB 선례).  **C층(FEM EP 기준=캡의 엄밀값)** = **Kogut–Etsion 2002**
(유료 CEB 대체, 항복 ω_c) · **Jackson–Green 2005**(★ H≠상수: H_G/σ_y=2.84[1−e^{−0.82(a/R)^−0.7}] → a/R>0.2서 Stage-E
면적 과소) · **Mesarovic–Fleck 2000**(異種=AM-SE 엄밀해 → AM-freeze scaffold 정당화).  **D층(자기상사 소성면적)** =
**Storåkers 1997**(A=2πc²rh, pile-up c²≈1.4 = 우리 Stage-E/ε_sphere 근거).  **E층(점착)** = **DMT 1975**(SE=DMT 체제,
pull-off 2πRγ = adhesionStiffness/`--coh` 앵커).  **전기-기계 결합** = **electromechanical-contact(Zhang 2024)**
(Hertz r_c + Holm R_c + Kirchhoff = 우리 Stage-E+Holm 사촌, 단 탄성).

**경로 A(18× 연화 제거 시험).**  real E_SE=24 + Thornton–Ning p_y캡(eq2→9→19→29, p_y≈1.6σ_y, LPSCl σ_y 0.05–0.30) →
300 MPa porosity가 연화 없이 나오나 시험.  선례 So 2021(LPS 0.98)·Sangrós2019(YR 실측)·Varkey(TN+multi-contact F_mc;
TN 단독은 ρ>0.7서 under-stiff).  접촉별 항복 gate = Kogut–Etsion ω_c/R=6.43(Y/E)².  ⚠ EEPA/Pasha는 *캡 없음* → 단독으론
경로A 아님.

**coarse-graining 별도 축.**  **Frankenberg 2024**(믹서 DEM)의 **force-scaling(힘∝f², overlap∝f, E* 고정)**은 우리 18×
연화와 *목적 반대*(scaling은 coarse-grain 불변성 *보존*, 연화는 missing 메커니즘 *보상*) → 직교.  cell-scale coarse-graining
시 템플릿(Stage-E area∝f²와 호환).

---

## 8. §G **MPM 작동원리·적용 수식** 계보 (← 요청 반영)

> MPM의 *작동원리와 지배방정식*을 담은 핵심 논문 = **3편**(+ 알고리즘 원전 2편).  우리 `mpm3d_compaction.py`/`mpm2d_*`
> (Taichi MLS-MPM + von Mises J2)의 수식 기반.

| 논문 (slug) | 역할 | 핵심 수식·원리 |
|---|---|---|
| **Stomakhin 2013** `stomakhin2013_mpm_snow_elastoplastic` | ★ **탄소성 MPM(EP-MPM) 알고리즘 원전** | **변형구배 곱분해 F=F_E·F_P** + **특이값공간 return mapping**(소성) + P2G→grid update→G2P→reset cycle.  눈=특이값 box yield + 압축경화.  우리 J2(원기둥 yield)가 *같은 프레임, yield면만 교체*. |
| **Klár 2016** `klar2016_dp_sand_animation` | 모래 = **Drucker–Prager 원뿔 yield**(DPC 원전) | 비점착+압축성(grain 재배열) → DP/cap.  ★ 우리 DPC dead-end의 출처: LPSCl SE는 점착+비압축(bulk 24≫0.3) → cap=부피수축=비물리 → **우리 J2+ν0.49는 재료클래스에서 *유도된 필연*** |
| **de Vaucorbeil 2020** `devaucorbeil2020_mpm_after_25_years_review` | **MPM 25년 리뷰**(339 ref) | 변종 지도(우리=MLS/B-spline ULMPM)·**contact(no-penetration 내재 = 우리 AM-freeze scaffold의 최소활용)**·**fracture 3접근(continuous-damage = SE 취성균열 구현경로, D6)**·image-based 치밀화(=우리 scaffold 선례) |
| *(원전)* Sulsky 1994 | MPM 자체(PIC/FLIP→고체역학) | Lagrangian 입자 + Eulerian 고정격자 → mesh distortion 없음 = large-deformation 압밀에 MPM이 맞는 이유 |
| *(알고리즘)* MLS-MPM (Hu/Taichi 88-line) | 우리 구현 기반 | moving least squares + APIC → 2차수렴·cell-crossing 제거 |

★ **인용 3종 세트**: Stomakhin 2013(EP 알고리즘) + Sulsky 1994(MPM 자체) + de Vaucorbeil 2020(가족 지도) = 우리 MPM 정당화.
우리 고유 = **von Mises J2 원기둥 yield + ν=0.49**(soft shear=granular 재배열 프록시 + stiff bulk=비압축 SE) — 재료클래스
유도.  (frame[1] LIMIT: MPM 연속체 → 명시적 접촉망 없음 → 수송 σ는 DEM 소유; MPM은 mechanics/porosity/morphology.)

---

## 9. §H 제조공정 DEM + dry-process·CBD — **Stage-2 닫음**

**제조 DEM peer(이온위상 역전·frame[5] 독립확인).**  LIB 제조 DEM 10편 모두 강체 구 + 접촉소성(형상소성 없음):
**Sangrós 2019**(Thornton-Ning+나노압입 YR+binder bond+spring-back 17%) · **Lyu 2025**(3D 건조+캘린더링, **CBD moment-전달
parallel-bond**=A3 최적합) · **Ngandjong 2021**(digital twin) · **Schreiner 2020**(EEPA+bond-only CABM=A3 최소구현,
*σ 0채널*=최대 transport 격차) · **Frankenberg 2024**(고강도 믹서 force-scaling) · **Shenouda 2020/Bosch 2014**(LIGGGHTS
튜토리얼, baseline-floor) · **Weitze 2024**(wet resolved-but-rigid) · **Lee 2024-multiphysics**(DEM→FEM Butler–Volmer,
FEM σ=constriction-free 상한) · **So 2022-coated**(SE-shell이 저압서 σ_e 차폐, 고압서 해제 = A4 core-shell 선례).
공통: 이온위상 역전(LIB pore=전도체/Bruggeman ↔ 우리 ASSB SE망=전도체/Holm) → **우리 SE-network 솔버가 LIB pore-Bruggeman을
대체**.

**★ Stage-2 (CBD/binder) 확실한 닫음.**  우리 CBD morphology 모델(curl worm-like + nucleate-on-carbon + shear-draw
d∝√(V/L), `docs/cbd_morphology_roadmap.md`)이 **문헌 3중으로 validated**:
1. **공정-물리(작동원리):** **Mun 2025·Liu 2025**(dry-electrode 리뷰)가 **PTFE shear-fibrillation 메커니즘**(19℃ 결정상전이
   → 전단으로 fibril 생성, high-Mw → robust 망)을 정리 = 우리 shear-draw 시드의 *공정 근거*.  DPC/co-rolling = 우리
   cold-press의 공정명.
2. **실험 형태(morphology):** **Lee 2025** SEM이 binder-VGCF **fibril 망(squiggle 곡선섬유 + 5단계 fibrillation 모식)**을
   *실측* = 우리 curl/nucleate 시드의 직접 실험 일치(우리 RVE는 막제조 shear는 재현 안 함 → 개념검증으로 사용).
3. **σ-블로킹 정량:** **Lee 2025** PTFE 0.5/2/5 wt% → σ_ionic 0.069/0.024/0.007 · σ_e 34/4.5/0.011(≈3,000×↓) +
   **Bielefeld 2020** 바인더 V(B):V(AM) 0.05/0.10 → σ_eff급감·τ² 4.2→10·active interface −17~82%(고-AM 비선형) +
   **interfacial-impedance(Choi)** GB-effect = 우리 voxel σ-블로킹(SuperP 0.0168<VGCF 0.0298)의 외부 정량 근거.

⇒ **Stage-2 결론(닫음):** 우리 CBD 시드 모델은 *공정-물리·실험-형태·σ-블로킹* 세 측면 모두 literature-grounded → **CBD
morphology 작업은 문헌적으로 닫힌다**.  남은 잔여(흡수 backlog): (i) 바인더의 *양의 역학효과*(Hong PTFE void-억제 6.4%p,
Bielefeld·우리 둘 다 σ=0 obstacle로만 봄 → MPM/DEM 역학에서 보강) — A3; (ii) interfacial vs bulk 배치 RVE 비교; (iii)
명시 bond 승격(Lyu parallel-bond/Sangrós bond/Ngandjong SJKR 청사진) — D5.

---

## 10. §I 우리-랩 degradation map (7편) — 모델이 따라가야 할 실험 trend 기준

**Yun 2023(capstone)**이 6편을 *2축 × 균열 3-driver*로 통합:
- **계면반응 축**(R_int↑, 황화물 산화분해): Yun(LPSCl) · **Kim 2025**(R_ct ~20×, TLM) · **Cho 2024**(도전재 매개)
- **이온수송/기계 축**(R_ion↑·균열): Yun(LIC 할라이드=압력하 SE균열) · **Kang 2025·Kang 2023**(NCA 입계균열)
- **균열 3-driver**: **크기**(Kang2025, 큰 10µm) × **음극strain**(Kang2023, Li-In ΔP) × **결정도**(Jung2023, PC>SC)
- **입자기반**: **Jung 2023** 단결정 SC-NCM(CAM균열 배제 → SE 열화 분리) + **Kim 2024**(carbon SE-domain 부피점유)

⇒ 같은 황화물-계면 산화분해가 *균열*(Kang)·*R_ct↑*(Kim/Cho)·*SE균열*(Yun-LIC)로 발현.  **우리 DEM+MPM = 그 *구조→수송 σ*
절반**(structure-σ=우리 / mechanics=Kang·Jung / kinetics=Kim·Cho / 종합=Yun).  우리 미보유(frame[5]): SE 취성균열·R_ct/
C_dl/확산·사이클 chemo-mech.  소재 정렬 backlog A8(NCA E=175 옵션)·A9(크기-의존 파괴).

---

## 11. ★ DEM·MPM 적용 가능 항목 리스트 (우리가 *적용할 수 있는* 것)

> digest는 끝나도 *적용은 별개*.  아래는 60편에서 식별한 **우리 코드에 적용 가능한 구체 항목** — DEM-side / MPM-side /
> coupling / 검증.  상태 ⛔TODO · 🔶검토 · ✅완료.  추적표 = `docs/digest_model_application_backlog.md` §E.

### (A) DEM-side — 접촉·수송·파괴
| # | 적용 항목 | 출처 | 대상 코드 | 비고 |
|---|---|---|---|---|
| D-1 | **경로 A**: real E=24 + Thornton–Ning p_y캡 → 18× 연화 제거 시험 | TN1998·So2021/22·Sangrós2019(YR 실측) | LIGGGHTS pair_style | ★최우선; Sangrós 나노압입 YR이 실측 선례 |
| D-2 | **Stage-E H 가변**: H_G/σ_y=2.84[1−e^{−0.82(a/R)^−0.7}] (a/R>0.2서 면적 과소) | Jackson–Green 2005 | network_conductivity A_tabor=F/H | 우리 a/R 분포 뽑아 H_G(a/R)로 교체 |
| D-3 | **neck 부피보존 면적** 1-liner로 Stage-E A_volume cross-check | Nisar 2024 | `_film_area` | A_volume=V/h_min과 같은 철학 |
| D-4 | **2상 Holm** R=(ρᵢ+ρⱼ)/(4r_c) 을 AM-SE 이종접촉에 | electromech(Zhang2024) | Holm 항 | 소코드 변경, B-axis cross-check |
| D-5 | **carbon p_c gate** g_C=f(wt_C65−4 wt%) | Reisacher 2023(LPSCl!) | additives.py σ_e | 재료보정 없이 전이 |
| D-6 | **carbon core-shell + 압력-게이트 σ_e 차폐** (저압 차폐→고압 해제) | So2022-coated | additives.py | A4; ⚠그들=ionic-shell, A4=electronic-shell(부호 반대) |
| D-7 | **kinetics 칸**: R_ct=k_ct/A_AM-SE + Warburg Z_low → ASR_total 확장 | Choi2024·Kim2025 | ASR 채널 | k_ct는 Kim2025 NCM811 R_ct 사용 |
| D-8 | **CN²/φc 해석적 prior**: Chen Eq7 P=[1−((3.764−ΣZ)/2)^2.5]^0.4 | Chen 2011 | σ_ionic CN² | 방향만(우리 data-locked 지수 유지) |
| D-9 | **사이클 stress DEM**: 압밀 후 AM 반지름 ±6% `fix adapt` swing | Alabdali2024(LPSCl!)·So21-fab | LIGGGHTS post | A10/B6, 우리 파이프라인에 가장 가까움 |
| D-10 | **명시 CBD bond**: parallel-bond / SJKR | Lyu2025·Sangrós·Ngandjong | DEM bond | A3/D5; Lyu moment-bond=PTFE 굽힘 최적 |
| D-11 | **입경-스케일 Auerbach**: σ_crit∝1/√d (큰 AM_P 균열↑) | Kang2025·NMC811균열 | fracture | A9; ⚠압밀-driver 버전만 |
| D-12 | **force-scaling/coarse-graining**(cell-scale RVE 시) | Frankenberg2024 | (미래) | area∝f² Stage-E 호환 |

### (B) MPM-side — 소성·형상·계면
| # | 적용 항목 | 출처 | 대상 코드 | 비고 |
|---|---|---|---|---|
| M-1 | **SE 취성균열**: continuous-damage / cohesive MPM | de Vaucorbeil2020·Bucci17/18·Yun2023 | (신규) MPM damage | D6; 우리 J2는 연성→취성 별도 |
| M-2 | **사이클 cohesive-zone**(Vegard 팽창 → 계면 박리) | Kang2025·Bucci2018 | (신규) cycling MPM | frame[5] 시간축 |
| M-3 | **--coh magnitude 고정** = DMT 2πRγ | DMT1975·Pasha | mpm `--coh` | γ(LPSCl) 문헌값만 |
| M-4 | **Stage-E A/B 검증** = Storåkers c²≈1.4 pile-up | Storåkers·Mesarovic–Fleck | (검증) | A=2πc²rh |
| M-5 | **morphology 검증 지속**(코어보존+경계평탄화 ↔ Lee2025/Sakuda SEM) | Lee2025·Sakuda2013 | viz_mpm | frame[4] 실험 일치 |

### (C) Coupling / 검증
| # | 적용 항목 | 출처 | 비고 |
|---|---|---|---|
| C-1 | **TauFactor τ_bulk cross-check** (우리 voxel→tif→TauFactor) | Cooper2016·Huang2025 | "σ_ionic>TauFactor bulk면 버그" validation |
| C-2 | **LBM ETC thermal cross-check** (우리 DEM dump에 LBM) | Huang2025 | σ_thermal Stage-T1 독립 검증 |
| C-3 | **σ_ionic 절대 앵커 채택** (vol%→φ_SE 매핑 후) | Minnmann2021·Bazzoun2026·Kim2025·Choi2024 | frame[4] B1 |
| C-4 | **σ-vs-P + Heckel P_y 앵커** | Schneider2023·Doux2020·Sakuda2013 | B5/B6 |
| C-5 | **wallP 조건부(f_AM skeleton-spring)** SE-poor 코너 보정 | (자체) | ✅ 채택; thin SE-poor BRACKET 코너에 적용 |

---

## 12. ★ 결론 — 확실히 닫음 (definitive closing)

**(1) 문헌으로 *확증*된 우리 결론 (frame[4]/[5]).**
- **18× 연화는 강체구 본질이 아니라 *항복캡 부재 탓***: So2021(H-cap 0.98)·Sangrós2019(YR 실측)·Bazzoun2025(high-f_CAM
  자인)·Shi2019("needs LPS plastic")·Weitze2024(resolved-but-rigid Fig7) — **5편이 독립적으로** 우리 Stage-E/MPM 칸을 명명.
- **transport novelty = constriction**: Bielefeld19(σ없음)→20(연속체상한)→Bazzoun26(RNM)→우리(Holm삼중항+Stage-E)의
  그룹-진화 + Nisar/electromech/Sangrós20-elec가 우리 솔버 골격을 byte-identical 재현 = 우리 위치 확정.
- **σ_e·σ_thermal 삼중항은 우리 고유**: peer 전원 ionic-only 또는 σ 미산출; Huang LBM이 우리 multi-pathway σ_thermal을
  독립 교차검증.
- **dip은 DEM/기하 소유, 소성 MPM 불가**(material sweep 증명; Bielefeld·Minnmann22가 비운 칸).
- **frame[5] 분업**: 60편 중 *단 한 편도* 수송망+형상소성을 동시에 갖지 않음 → DEM=수송/패킹, MPM=형상/void-fill 분업이
  *문헌으로* 확증.

**(2) Stage-2 (CBD/binder) 닫음.**  우리 CBD morphology 모델은 **공정-물리(Mun/Liu PTFE fibrillation) · 실험-형태(Lee2025
fibril SEM) · σ-블로킹 정량(Lee2025 PTFE% / Bielefeld2020 binder / Choi GB)** 3중으로 literature-grounded → **CBD 작업
문헌적 닫음**.  잔여=바인더 양의 역학효과(Hong)·명시 bond 승격(Lyu/Sangrós/Ngandjong) → backlog A3/D5.

**(3) 우리가 *미보유*하고 *흡수할* 것 (정직 목록).**
- **kinetics(R_ct/C_dl/Warburg)**: Choi2024·Kim2025가 흡수경로 제시(R_ct=k_ct/A_AM-SE on Stage-E coverage) — backlog 신규.
- **사이클 시간축**: Alabdali(DEM Vegard-swing, 가장 쉬움)·So21-fab(ductile σ-loss)·Bucci(취성 CZM)·Kang2025 — A10/B6.
- **소결(sintering)**: So2022(fusion-bond rate)·Nisar(neck) — 우리 미모델(정적 압밀만).
- **계면 화학열화**: Kang2025(NCA/LPSCl 분해→Li구배→균열)·LZO 코팅 — future 계면 축.

**(4) 다음 행동.**  논문작업 종료 → backlog 우선순위: **D-1(경로A) → D-5/D-6(carbon σ_e) → D-9(사이클 stress) →
M-1(SE 취성)**.  소재정렬 A8(NCA)·A9(크기파괴).  paper-build refs.bib 정정(Minnmann2021 040537, Bielefeld 2020 not 2022).

---

## 부록: 압력 3종 구분 (반복 인용 주의)

| 압력 | 범위 | 물리 | 앵커 | 우리 |
|---|---|---|---|---|
| **제조(fab)** | 300–500 MPa | 압밀·porosity·Heckel | Minnmann 380·Doux 370·Sakuda >350·Lee2025 500 | **300 MPa, Heckel P_y 138** |
| **측정** | 40 MPa | σ-측정 | Minnmann 40 | — |
| **작동(operating)** | 2–70 MPa | 계면접촉·creep | Doux 5(최적)·Lee2025 **2**(co-rolling)·Cronau 5–50 | (정적 모델, 미보유 시간축) |

> ⚠ Heckel P_y(제조압 무릎)를 작동압과 혼동 금지.  σ 절대값은 소재(LPSCl vs glass vs halide vs oxide)·측정형상 다르면
> 전이 금지(스프레드/추세만).  bulk LPSCl σ 앵커 스프레드 {3.0/2.19/1.6/1.02}.
