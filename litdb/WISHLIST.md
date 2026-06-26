# 📥 LITDB WISHLIST — elasto-plastic 접촉/소성 모델 (agent 투입 대기열)

> 갱신: 2026-06-26.  목적: 우리 DEM 접촉모델(`hooke/hysteresis` + adhesion + plasticity-depth)과
> MPM(J2)의 **이론 토대 / 보정값 / 경로 A(항복캡) 후보 LAW**를 문헌으로 채운다.
> 정리 = `litdb-curator` agent ("이 논문 정리해줘" 트리거) → `papers/<slug>.md`.
> 이미 한 것: So 2021 ✅, Martin–Bouvard 2003 ✅, Varkey 2026 ✅, Bouvard 2000 ✅
> (모두 elasto-plastic CONTACT 층위; `elasto_plastic_feasibility.md` 종합).
>
> ★ **왜 지금 급한가 (2026-06-26 발견):** real_14 실제 dump로 f_AM 재구성 →
> **Hertz(AM-AM 0.843@E=1.35)가 실제 hooke/hysteresis 접촉력(0.670)을 재현 못 함.**
> E_SE를 real 24로 바꾸면 0.258로 *반대로* 튀어 → 어떤 단일 Hertz 모듈러스도 실제값을 못 맞춤.
> 원인은 모듈러스가 아니라 **접촉 LAW 형태**(선형 vs δ^1.5, plasticity-depth, max-stiffness, adhesion).
> ⇒ **(1) 우리 모델 LAW를 기술한 논문**(Walton–Braun/Luding)과 **(2) 그 LAW의 뿌리인 탄소성
> 접촉역학 정전**(Tabor·Johnson·CEB·Mesarovic–Fleck…)이 1순위.  Hertz 가정은 폐기.

상태 범례: 🔜 1순위(agent 즉시) · 🟡 2순위 · ⬜ 보조/선택 · 📕 교과서(인용용, agent엔 부적합) · ✅ 완료

---

## Tier 0 — 탄소성 접촉역학 정전 (★★★ 가장 저명, 분야 무관)

> 우리 모델의 *물리 뿌리*.  대부분 수천~수만 인용. battery와 무관한 보편 접촉역학.

| # | 정확한 제목 (검색용) | 저자/년·출처 | 왜 우리에게 | 상태 |
|---|---|---|---|---|
| 1 | **The Hardness of Metals** | Tabor 1951, Clarendon Press | ★ **H ≈ 3σ_y 의 원전.** 우리 H-cap(So 2021 경로 A)·"**Tabor coverage**"·경도 캡 전부 여기서. | 📕 |
| 2 | **Contact Mechanics** | K.L. Johnson 1985, Cambridge UP | ★ 접촉역학 바이블. 탄소성 압입(평균압 p_m, 항복개시 p_y≈1.1σ_y → 완전소성 H≈3σ_y), Hertz·JKR·DMT 통합. | 📕 |
| 3 | **An elastic-plastic model for the contact of rough surfaces** (CEB) | Chang, Etsion, Bogy 1987, J. Tribol. 109(2) 257 | ★ **최초의 통계적 탄소성 거친면 접촉(CEB).** 항복 후 부피보존 소성 → 우리 Stage-E 접촉면적·coverage 통계의 원형. | 🔜 |
| 4 | **Frictionless indentation of dissimilar elastic-plastic spheres** | Mesarovic & Fleck 2000, Int. J. Solids Struct. 37(46) 7071 | ★ **구–구 탄소성 압입 엄밀해**(탄성→similarity→완전소성 전 영역). 경로 A 항복분기 LAW의 정밀 근거. | 🔜 |
| 5 | **Coefficient of restitution for collinear collisions of elastic-perfectly plastic spheres** | Thornton 1997, J. Appl. Mech. 64(2) 383 | Thornton 소성접촉(Thornton–Ning 1998 전신). 항복압 p_y·잔류겹침의 기준 정식. | 🟡 |
| 6 | **Similarity analysis of inelastic contact** | Storåkers, Biwa, Larsson 1997, Int. J. Solids Struct. 34(24) 3061 | 자기상사 비탄성 접촉 A=2πc(m)²rh. **Martin–Bouvard가 사용** → 우리 Stage-E 면적과 A/B 비교 대상. | 🟡 |
| 7 | **A finite element study of elasto-plastic hemispherical contact against a rigid flat** | Jackson & Green 2005, J. Tribol. 127(2) 343 | FEM 반구-평면 탄소성. 항복개시→완전소성 천이의 보정값(p_y, H). | ⬜ |
| 8 | **Elastic–plastic contact analysis of a sphere and a rigid flat** (KE) | Kogut & Etsion 2002, J. Appl. Mech. 69(5) 657 | FEM 구-평면(KE) — CEB의 FEM 후속. 항복 임계 overlap δ_y. | ⬜ |
| 9 | **Contact of nominally flat surfaces** (GW) | Greenwood & Williamson 1966, Proc. R. Soc. A 295 300 | (탄성) 거친면 접촉의 토대 — CEB가 이걸 탄소성으로 확장. 우리 Holm/constriction coverage의 asperity 통계 근간. | ⬜ |

## Tier 0b — DEM·연속체 소성의 출발점

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 10 | **A discrete numerical model for granular assemblies** | Cundall & Strack 1979, Géotechnique 29(1) 47 | ★ **DEM 원전** (모든 DEM의 출발; soft-contact 시간적분). 우리 LIGGGHTS의 조상. | ⬜ |
| 11 | **Computational Inelasticity** | Simo & Hughes 1998, Springer | ★ **J2 return-mapping** 교과서 — 우리 MPM champion(von Mises J2)의 구현 토대. | 📕 |

## Tier 1 — 우리 접촉모델 자체의 원전 (★★ 오늘 발견의 직접 해소)

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 12 | **Viscosity, granular-temperature, and stress calculations for shearing assemblies of inelastic, frictional disks** | Walton & Braun 1986, J. Rheol. 30(5) 949 | ★ **LIGGGHTS `hooke/hysteresis`의 원전.** 이력 선형 스프링(loading k₁/unloading k₂, 영구겹침) = 우리가 쓰는 *바로 그 힘법칙*. f_AM을 **실제 LAW로** 재구성하려면 필수. | 🔜 |
| 13 | **Cohesive, frictional powders: contact models for tension** | Luding 2008, Granular Matter 10(4) 235 | ★ 점착 탄소성 이력 스프링(k₁·k₂·k_c·φ_f). 우리 `maxElasticStiffness`(k₂)·`adhesionStiffness`(k_c)·`plasticityDepth`(φ_f) 파라미터 **1:1 매핑** = input m6/m7/m8 의 정의서. | 🔜 |
| 14 | **A theoretical model for the stick/bounce behaviour of adhesive, elastic-plastic spheres** | Thornton & Ning 1998, Powder Technol. 99(2) 154 | 점착 탄소성 구(Hertz→항복 p_y→소성분기+잔류겹침). Varkey 2026 사용. **경로 A** 후보 LAW. litdb엔 언급만. | 🔜 |

## Tier 2 — 점착 이론 (우리 adhesionStiffness / cold-weld / vdW 의 원전)

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 15 | **Surface energy and the contact of elastic solids** (JKR) | Johnson, Kendall, Roberts 1971, Proc. R. Soc. A 324 301 | 점착 탄성접촉 — adhesion(k_c)의 연성·큰입자 극한. | ⬜ |
| 16 | **Effect of contact deformations on the adhesion of particles** (DMT) | Derjaguin, Muller, Toporov 1975, J. Colloid Interface Sci. 53 314 | 강성·작은입자 점착 극한(SE 0.5 µm). JKR과 짝. | ⬜ |
| 17 | **Surface forces and surface interactions** | Tabor 1977, J. Colloid Interface Sci. 58 2 | ★ Tabor 파라미터(JKR↔DMT 체제) — 우리 "Tabor coverage" 명칭의 원전. | ⬜ |

## Tier 3 — DEM 탄소성 구현·보정 (force-displacement / 점착-소성)

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 18 | **An elastoplastic contact force–displacement model in the normal direction: displacement-driven version** | Vu-Quoc & Zhang 1999, Proc. R. Soc. A 455 4013 | FEM 검증 탄소성 force-displacement — DEM 표준 항복-분기. | ⬜ |
| 19 | **Micromechanical analysis of cohesive granular materials … adhesive elasto-plastic contact model** (EEPA) | Thakur, Morrissey, Sun, Chen, Ooi 2014, Granular Matter 16 383 | **EEPA**(Edinburgh) — LIGGGHTS/EDEM 표준 점착-탄소성. 경로 A 대안 + 보정 절차. | 🟡 |
| 20 | **A linear model of elasto-plastic and adhesive contact deformation** | Pasha, Hassanpour, Ahmadian, Ghadiri 2014, Granular Matter 16 151 | 미세 점착분말용 선형 탄소성+점착(Walton/Luding 확장) — **0.5 µm SE** fine·점착 거동. | ⬜ |

## Tier 4 — MPM 탄소성 (우리 MPM J2 / DPC 이론 보강, 선택)

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 21 | **Drucker-Prager elastoplasticity for sand animation** | Klár 외 2016, ACM TOG 35(4) | DP-cap MPM — 우리 **DPC cap dead-end**과 직결. | ⬜ |
| 22 | **A material point method for snow simulation** | Stomakhin 외 2013, ACM TOG 32(4) | 탄소성 MPM 대중화 원전(return-mapping). | ⬜ |
| 23 | **Material point method after 25 years: theory, implementation, and applications** | de Vaucorbeil 외 2020, Adv. Appl. Mech. 53 | MPM 리뷰 + J2 구현(champion 토대). | ⬜ |

## Tier 5 — 배터리 전극 탄소성 DEM 응용 (맥락, 선택)

| # | 정확한 제목 | 저자/년·출처 | 왜 | 상태 |
|---|---|---|---|---|
| 24 | **Mechanical, Electrical, and Ionic Behavior of Lithium-Ion Battery Electrodes via DEM Simulations** | Sangrós Giménez 외 2020, Energy Technol. 8 1900180 | 전극 DEM(탄소성+바인더 bond+σ). Varkey의 **Sangrós bond** 출처. Stage-2 PTFE/VGCF 템플릿. | ⬜ |
| 25 | **Investigating electrode calendering … by coupling DEM and reaction-diffusion** | Ngandjong 외 2021, J. Power Sources 485 229320 | ARTISTIC 소성 DEM calendering — 압밀·전기화학 결합 비교. | ⬜ |

---

## 투입 순서 추천
1. **#12 Walton–Braun + #13 Luding** — 우리 모델 *자체*. f_AM·load-share를 Hertz 아닌 **실제 LAW**로
   해석/재구성 (오늘 발견 직접 해소) + `dem_am_load_fraction.py` 물리 검증 근거.
2. **#1 Tabor(H) + #2 Johnson + #3 CEB + #4 Mesarovic–Fleck** — 탄소성 접촉의 *정전* (경로 A 항복캡 p_y/H 근거).
3. **#14 Thornton–Ning** — 경로 A LAW 확정.
4. 나머지(점착 JKR/DMT, EEPA, MPM, 배터리)는 필요 시.

## 비고
- 📕 교과서(Tabor·Johnson·Simo–Hughes)는 PDF agent엔 부적합 → **인용·근거용**(해당 장만 발췌 가능).
- Tier 0~1·3은 **DEM 접촉 LAW 층위**( `elasto_plastic_feasibility.md` 0절 층위(1) ) — 우리 18× 연화의
  물리 대체(경로 A) + Hertz-폐기 후속.  Tier 4는 **연속체 SHAPE 소성**(이미 MPM 보유, 인용 보강).
- "2022 Bielefeld"=실제 **2020**(오기).  Wang 2022 κ=**유령 인용**(웹 확인 부재) → 제외.
