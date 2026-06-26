# 응력기반 multi-contact 탄소성 모델로 SE separator·양극 압밀 DEM — Varkey (Adv. Powder Tech. 2026)

> slug `varkey2026_multicontact_elastoplastic_dem` · DOI `10.1016/j.apt.2026.105338` · type `DEM` · PDF `Varkey_2026_AdvPowderTech_MultiContact_ElastoPlastic_DEM_ASSB.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
강체 구 DEM에 **다중접촉 탄소성 접촉법칙**(Thornton–Ning + Giannis 응력기반 구속항)을 더해 halide
SE separator/양극 압밀을 ρ>0.7 치밀영역까지 실험두께와 맞춘 연구 — 단 **입자 형상은 안 변하고(구)**
CONTACT 소성만이라, 우리 MPM이 메우는 *간극(형상변화·<20 % porosity)*을 스스로 인정(frame[5] 확증).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| C.A. Varkey, K. Giannis, S. Melzig, C. Schilde, S. Zellmer (Fraunhofer IST + TU Braunschweig, HELENA) | Adv. Powder Technology 37 (2026) 105338 | 10.1016/j.apt.2026.105338 | **halide Li₃YBrCl₆** + NMC-811 + SBR + CB | DEM (Ansys Rocky), 실험 검증 |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| separator porosity | 45/35/31/25/**21 %** | 0/100/200/300/350 MPa | digitized(Fig10) | floor 21 % @350 |
| separator 두께 sim/exp | 188.2/170.3/152.7/143.5 vs 186/171/154/145 µm | 100–350 MPa | stated(Fig9) | <1 % 일치 |
| cathode porosity | 49/39/38/37.5/**37 %** | 0/125/200/300/350 MPa | digitized(Fig13) | floor 37 % (AM-rich) |
| cathode 두께 sim/exp | 146.6/141.2/137.7/135.6 vs 145.2/140.5/137.1/135.3 µm | 125–350 MPa | stated(Fig12) | |
| σ_ionic (separator) | 0.0026→0.0048 mS/cm | 100→350 MPa | digitized(Fig14) | bulk halide 1.8 → 구속 0.0025–0.005 |
| 접촉면적% | 8→13 % | 100→350 MPa | digitized(Fig14) | |
| E_SE / E_CAM | **10.58** / 140 GPa | | stated(Table1) | halide ~8× 뻣뻣(우리 E_eff 1.35 대비) |
| 항복비 (yield ratio) | 0.0103 | | stated | δ~1.03 %서 소성 시작 |

## 4. 시뮬레이션 방법 ★
- **code**: **Ansys Rocky DEM**.
- **DEM 접촉법칙** ★ (Thornton–Ning 탄소성, §2.2):
  - 탄성 Hertz `F_el=(4/3)E*√(R*δ³)` (δ<δ_y); 항복 개시 `f_y=(1/6)(R*/E*)²(πp_y)³`, `δ_y=(1/4)(R*/E*²)(πp_y)²`;
    소성 **선형** `F_el-pl=f_y+πp_y·R*(δ−δ_y)` (δ≥δ_y); 제하 잔류겹침 `F_unl=(4/3)E*√(R_p*(δ−δ_R))`.
  - 접선 Coulomb `F_t=−μF_n·s_t/|s_t|`.
- **multi-contact 구속항** ★ (Giannis [24], §2.3 — 신규성): 입자별 응력 `σᵖ=(1/Vᵖ)Σlⁿ⊗fⁿ` (eq9),
  `P_ij=(trσ_i+trσ_j)/3` (eq10), `F_mc=β·ν·a_ij·P_ij` (β=0.5). Poisson 측방팽창 구속 — **ρ>0.7서만** 유효.
- **bond/binder 모델** (Sangrós [38], §2.4): SBR+CB 실린더 spring-dashpot bond. S_n=2.5e13/S_t=1.875e13 N/m³,
  감쇠 0.9997; α_b로 bond 부피=실험 바인더 부피분율 (separator 0.45/0.2, cathode 0.35/0.25).
- **MPM/continuum**: 없음.
- **전달 솔버**: 저항망(Sangrós [39]) R_p(길이)+R_c(면적)+R_b(bond) → σ_ionic (우리 Holm/Kirchhoff 아날로그).
- **입자 처리** ★: **구만** (논문 p.12 "구=타협, 현실 형상=향후 과제" 명시). separator 단봉 / cathode 이봉.
  **rigid 입자 + CONTACT 탄소성** — δ는 소성의 기하 프록시, **진짜 SHAPE 흐름 아님**.
- **도메인/RVE**: 100×100 µm² × 두께, 압축 plate(strain rate 0.283 s⁻¹ benchmark / 0.00707 m/s 압밀).
  질량loading 0.03(sep)/0.037(cat) g/cm² → 36,442 / 72,964 입자. 압력 100–350 MPa.

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 6 | Hertz/Thornton–Ning/multi-contact 힘-겹침 (3·5입자) | multi-contact가 ρ>0.7 과강성 보정 |
| 8 | 접촉모델별 두께-압력 | Hertz/TN 권장 안 함(ρ>0.7); MC가 350 MPa서 실험 일치 |
| 9/12 | separator/cathode 두께-압력 sim vs exp | 우리 P-vs-porosity fit 데이터 |
| 10/13 | separator/cathode porosity·DoD-압력 | **floor 21/37 %** + ~100 MPa 탄성→소성 무릎 |
| 14 | σ_ionic·접촉면적 vs 압력 | stiffer-SE σ-vs-P 추세(절대 전이 불가) |

## 6. Post-processing ★
- **무엇**: porosity `ε=1−m/(ρ_eff·t·A)` (eq20), DoD=(h_a−h_c)/h_a, 겹침% `δ/min(r_i,r_j)·100` (eq22),
  σ_ionic 저항망(R_p+R_c+R_b), 실험 EIS `σ=l/(R·a)` (eq21).
- **도구**: Ansys Rocky, 자체 저항망 후처리(Sangrós).
- **수치화**: separator/cathode 각 4압력, 두께 sim↔exp <1 % 매칭으로 모델 검증.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 소재 E_SE | halide 10.58 GPa | LPSCl E_eff 1.35 / real 24 | **halide ~8× 뻣뻣 → 절대 porosity 전이 불가** |
| pure-SE floor | separator 21 % @350 | ~10 % @300 (Minnmann) | 더 뻣뻣→더 높은 floor (우리 E-sweep 정합) |
| AM-rich floor | cathode 37 % @350 | real_14 15.6 % @300 | 같은 이유 + 우리 소성 흐름이 강체 floor 아래로 |
| 소성 종류 | CONTACT 탄소성(δ 프록시) | MPM 진짜 SHAPE 소성 | **입자 형상변화 = 우리 MPM 고유** |
| multi-contact F_mc | 구속항(ρ>0.7) | 18× E 연화 | 같은 증상(과강성) 다른 처방 — 비교연구 거리 |
| <20 % porosity | "추구 안 함"(비용) | 일상 10–16 % | 강체 구 floor를 소성 흐름으로 돌파 |
| Furnas dip | RCP/rigid dip @AM70–80 | DEM·de Larrard dip @AM70–85 | **일치**(둘 다 기하 — 소성 MPM은 못함) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **porosity 관계식에 E_SE(강성) 항 필수**: halide floor 21/37 % = 우리 LPSCl 10/15.6 %의 stiffer-SE 데이터점.
  Heckel `ln(1/(1−D))=K·P+A`, 둘 다 ~100 MPa 무릎 (= 우리 P_y 138). `docs/data/densification_porosity_db.csv`.
- ② **frame[5] 확증 인용**: 최신 DEM(우리보다 접촉법칙 정교)도 구-형상/<20 % 한계를 스스로 명시 → 우리 DEM↔MPM 분할이 변명 아님.
- ③ **(선택) multi-contact vs 우리 18× 연화** 비교: ρ>0.7 과강성을 F_mc로 푸는지 vs 연화로 푸는지.

## 9. 인용 가능 문장 (deck/paper용)
- "Even a 2026 state-of-the-art multi-contact elasto-plastic DEM (Varkey 2026) keeps particles as
  rigid spheres — the elasto-plasticity lives only in the CONTACT law (overlap proxy), and the authors
  explicitly defer realistic particle shapes and sub-20 % porosity to future work. This is precisely
  the resolved-grain plastic regime our MPM fills (frame [5])."

## 10. 주의/한계 (over-claim 방지)
- **강체 구** — "elasto-plastic"은 CONTACT 힘법칙만, 입자 형상 안 변함 (δ=기하 프록시 ≠ 흐름).
- **halide(E=10.58)** — porosity·σ 절대값 LPSCl로 전이 불가, **추세/stiffer-SE 교차검증만**.
- σ_ionic·접촉면적(Fig14)·porosity(Fig10/13)는 **작은 삽입그림 digitized** → 추세만(±), stated 아님.
- multi-contact F_mc는 **평균장**(연속체 MPM은 exact) — ρ>0.7 보정의 근사.

## Supplementary (FEM 검증 — 2026-06-26 사용자 PDF 추가)
원본 `docs/literature_coverage/pdfs/Varkey_2026_AdvPowderTech_SupportingInformation_FEM_validation.pdf`.
**"Validation of Multi-contact elasto-plastic model using FEM"** — 그들 접촉모델을 **Ansys Mechanical FEM**으로
검증 (우리가 없던 ground-truth 검증):
- **셋업**: 3입자(직경 10 mm) 단축압축, 변형체 구 + 탄소성 구성식 + frictionless(Augmented Lagrange) 접촉,
  2 plate 변위(5 mm)로 압축.  DEM은 동일조건 Ansys Rocky(multi-contact EP + Thornton–Ning).
- **Table S1 (FEM 파라미터)**: E = **71 GPa** (7.1e10 Pa), ν = **0.33**, **σ_y = 280 MPa** (2.8e8 Pa),
  mesh 0.66 mm.  ⚠ = *모델수치 검증용 generic EP 재료*(금속급), **실제 halide SE(E=10.58)가 아님** — 접촉
  LAW의 수치정확도 검증이지 재료 검증 아님.
- **★ Figure S1 (핵심 결과)**: force-displacement에서 **multi-contact EP 모델 = FEM과 전 압축영역 일치**,
  반면 **Thornton–Ning 단독은 고변위서 FEM을 UNDER-predict** (5 mm서 TN ≈ 5.7 vs FEM/MC ≈ 9.7 ×10⁴ N).
  ⇒ **multi-contact 구속항 F_mc 가 고압축(고밀도) 힘응답을 FEM 수준으로 끌어올리는 바로 그 보정**.
- ★ **우리에게**: 이게 frame[2]에서 언급한 "**multi-contact = 18× 연화의 물리적 대안**"의 정량 근거 —
  Thornton–Ning(wishlist #③) 단독은 고밀도서 under-stiff(우리 DEM이 E를 18× 낮춰 메우는 그 증상), F_mc가
  그걸 *물리적으로* 보정.  단 여전히 강체 구(형상 안 변함) → 우리 MPM 형상소성과는 별개(frame[5] 유지).
