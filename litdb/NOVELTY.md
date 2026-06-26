# ★ NOVELTY & POSITIONING — 우리 DEM+MPM bottom-up 모델이 가지는 portion (LIVING DOC)

**목적:** litdb로 논문을 digest할 때마다, **우리 모델의 novelty가 무엇이고 / 필드에서 어떤 portion(위치)을
차지하는지**를 한곳에 누적·갱신.  digest마다 §4 표 한 줄 + §6 로그 추가.  (출처 doc:
`docs/positioning_vs_geodict.md`, `litdb/comparison_vs_ours.md`, `docs/stage2_model_audit_vs_literature.md`,
CLAUDE.md frame[1]–[5].)

---

## §0 한 문단 thesis (novelty)
선행 연구의 디지털트윈은 거의 전부 **top-down / reconstruction**(토모그래피·CAD·확률배치로 *주어진* 미세구조를
GeoDict/FEM 연속체로 특성화)이다.  우리는 **bottom-up / process-physics formation**: **공정(압력·조성·입경·
첨가제)에서 미세구조를 DEM+MPM으로 *예측*하고**, 그 위에 **연속체가 구조적으로 놓치는 granular 점접촉
constriction σ(Kirchhoff/Holm 접촉망, ionic+electronic+thermal triad)**와 **MPM 소성 morphology/void-fill/strain
field**를 얹어, **"주어진 구조 특성화"를 넘어 "공정→구조→수송"을 예측**한다.  두 모델을 실험에 **독립 보정**
(frame[4])하고 그 수렴/발산을 **정량 regime map**으로 제공한다.  (분류 출처는 우리가 positioning 대상으로 삼는
바로 그 그룹의 peer-reviewed 리뷰: Kim·Lee, *ACS Energy Lett.* 2024, 9, 5225 — top-down vs bottom-up를 명명;
bottom-up 예시로 **DEM/FVM + LPSCl+NCM**을 직접 거명 = 우리 도구·소재계.)

---

## §1 필드의 도구 vs 우리 (taxonomy)
| | top-down / reconstruction (필드 주류) | bottom-up / formation (우리) |
|---|---|---|
| 미세구조 입력 | XCT/FIB-SEM/CAD/확률배치로 **주어짐** | 공정(P·조성·입경)에서 **예측** (DEM 압축 + MPM 소성) |
| 유효 수송 | GeoDict ConductoDict/DiffuDict, FEM (연속체 PDE) | voxel-FV(복제) **+ granular 접촉망 σ**(연속체 불가) |
| 대표 논문 | GeoDict류 #266/#271/#281/#284/#286/#275/#22/#21, Bazzoun FEM | — |
| 소성 형상변화 | ✗ (rigid sphere / 연속체) | ✅ MPM (SEM 일치 core-preserved+boundary-flatten) |

GeoDict은 **연속체 특성화 엔진의 표준**(성숙·robust·모듈폭) — 우리 voxel은 그 한 조각(무료 복제)일 뿐.
우리 우위는 **(i) 구조 예측(입력측) + (ii) 접촉망 constriction σ(연속체가 놓침)** 두 가지.

---

## §2 우리가 *유일하게* 하는 것 (novelty portions)
1. **공정→구조 예측** — 압력·조성·입경·첨가제 → 미세구조 (DEM rigid 압축 + MPM 소성 void-fill).  필드는 구조를
   줘야 함.  ★ 가장 큰 차별.
2. **granular 점접촉 constriction σ triad** — Kirchhoff/Holm 접촉망으로 **ionic+electronic+thermal** 동시.
   연속체(GeoDict/FEM/voxel)는 σ_contact-free **상한**만; RNM(Bazzoun)은 ionic만.  우리는 둘 다 가져 constriction
   overhead까지 정량.
3. **MPM 소성 morphology** — 입자 shape change(SEM 일치) + void-fill flow + accumulated plastic-strain field
   (열화 onset) + 공간 stress/strain/density map.  rigid-sphere DEM(Varkey 포함 *모든* DEM 논문)은 불가.
4. **DEM↔MPM 독립 cross-validation + regime map** — 둘을 실험에 독립 보정(frame[4]); 수렴=교차검증, 발산=정량화된
   모델한계.  porosity 신뢰성 regime map(105 case, 76% cross-validated; 양 끝 실패 corner를 *반대 방향*으로 정량)은
   novel epistemology.
5. **예측 scaling law** — design knob → σ 직접 (σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.90).
6. **Stage-E 소성 접촉면적 + fracture(Auerbach) + DEM→MPM 응력 커플링** — 탄성 overlap→소성 area 재유도;
   AM 파괴(Auerbach/Lawn); ★ NEW **Tabor식 wallP 조건부**(DEM AM 하중분담을 MPM servo에 주입 = multi-scale
   handoff, Minnmann 2022 §5.4가 부른 mechanical-echem coupling의 한 조각).

---

## §3 필드가 *앞서는* 것 (정직 — 우리는 이걸 anchor로 소비)
- **실험 anchor**: Minnmann 2021 JES(porosity 14%·σ_ion 0.17·τ 2.07), Bazzoun(EIS σ_ionic+FEM), #266 Oh(bimodal
  dip), #271 Hong(CBD), Cronau(σ_grain), Sakuda(E=24), Doux(stack pressure), co-rolling(operating pressure).
  → 우리는 **실험 무측정**(시뮬), 이들을 보정/검증 anchor로 사용.
- **GeoDict 성숙도·모듈폭·robustness** (범용 연속체).  **multi-pressure 실험 검증**(Varkey 100-350 / Minnmann /
  Doux).  **binder bond 모델**(Varkey SBR+CB).  **full echem 커플링**(#22 Park / #281 — 우리 Phase-4 미구현).

---

## §4 per-paper portion map (digest마다 한 줄 추가)
역할: **A**=anchor(우리가 보정/검증에 소비) · **G**=gap-we-fill(그들 한계를 우리가 메움) · **X**=cross-validation
(frame[4] 독립 수렴) · **M**=methodology peer.

| 논문 | 역할 | 그들이 하는 것 | 우리가 더하는 portion |
|---|---|---|---|
| Park 2020 (foundational, Nat?/AEM) | X+G | 시조 디지털트윈, NCM711+LPSCl, 규칙배치(GeoDict 이전) | 압축물리 예측(그들은 PSA 규칙배치); 4건 frame[4] 일치 |
| Minnmann 2021 JES 040537 | A | EIS-TLM porosity 14%·σ_ion 0.17·τ 2.07 (실험) | 접촉망 σ + 구조예측; TLM은 constriction 무시(우리 Stage-E가 보강) |
| Minnmann 2022 AEM (review) | A(design) | 설계 가이드(60-70vol% CAM, bimodal) 정성 | 정량 dip(de Larrard) + 예측 |
| Cronau 2021 | A | σ_grain(GB-pellet) + stack-pressure dilemma | σ_grain 소비; E_eff softening 서사 |
| Sakuda 2013 | A | **E_SE=24 origin** + sulfide RT 압축densify | E_eff=1.35/1.53 = 24의 softening; MPM shape-change가 그들 SEM 재현 |
| Doux 2020 | A | LPSCl stack-pressure(5MPa opt), 18% floor | fab/operating 분리; rigid-floor 비교 |
| Lee 2025 (Nat Commun 16, 4200) | A+X | dry **co-rolling** 저압 2MPa robust 계면 (LPSCl+NCM811+VGCF+PTFE = 우리 정확한 계) | operating-pressure anchor(floor 2<Doux5<Minn40); ★ **const-P vs fixed-gap cell = 우리 MPM servo vs hold 실험쌍** → hold 채택 독립검증; fab 500 vs cycle 2-5 = process-level fab/operating |
| Bazzoun 2026 | A+X+M | EIS σ_ionic + DEM+RNM(=우리 솔버) + FEM | σ_e/thermal triad + Stage-E + MPM(그들 ionic·sphere만) |
| Varkey 2026 | G+M | multi-contact 탄소성 DEM(but rigid sphere, ~20% floor) | 소성 shape change + void-fill + <20% (그들이 future work로 인정) |
| Oh 2026 (#266) | A+X | bimodal CAM dip(실험) | rigid DEM이 dip 독립재현; 소성 MPM이 dip 부분소거 정량 |
| Hong 2026 (#271) | A+G | CBD viscoelastic spring-back(GeoDict) | spring-back은 우리 MPM gap(미구현); CBD --coh lever |
| GeoDict류 #281/#284/#286/#275 | G | 주어진 구조 특성화(top-down) | 공정→구조 예측 + 접촉망 σ |
| Trevisanello 2021 | (caveat) | SC/PC NCM 확산·표면적(전자σ 아님) | σ_S/σ_P 오귀속 교정 근거(audit #11) |
| Choi/Kim 2024 (ACS EL review) | (taxonomy) | top-down/bottom-up 명명; bottom-up=DEM/FVM+LPSCl/NCM | **우리 위치를 그들 taxonomy가 거명** = positioning 최강근거 |

---

## §5 논문 한 줄 (novelty statement)
> "선행 디지털트윈이 *주어진* 미세구조를 상용 연속체 도구(GeoDict/FEM)로 특성화하는 top-down/reconstruction인
> 반면, 본 연구는 **공정(압력·조성·입경·첨가제)에서 미세구조를 DEM+MPM으로 예측**하고(bottom-up/formation,
> Choi et al. ACS EL 2024 분류), 그 위에 **연속체가 놓치는 granular 점접촉 constriction σ(Kirchhoff/Holm,
> ionic+electronic+thermal)**와 **MPM 소성 morphology/strain field**를 결합하여, **두 모델을 실험에 독립 보정한
> 뒤 그 수렴(교차검증)·발산(정량화된 모델한계)을 regime map으로 제공**하는, 공정→구조→수송 예측 오픈 파이프라인이다."

---

## §6 update log
- 2026-06-26 최초 작성.  digest 12편 기준 §4 채움.
- 2026-06-26 co-rolling(Lee 2025 Nat Commun 16,4200) 완료 → §4 확정.  ★ 신규 frame[4] 검증: 그들의
  const-pressure vs fixed-gap 셀 = 우리 MPM servo vs hold 실험쌍 → scaffold에 hold 채택이 독립적으로 옳음.
  (Lee paper는 2026-06-24 litdb/papers/에 CBD/binder 각도로 부분 digest 존재했음 — 이번 docs/ digest는
  process/저압/계면 각도로 보완, 중복 아님.)  TODO: Bielefeld/Wang digest 시 §4 추가; Phase-4 echem 커플링
  (#22/#281) + operating-pressure σ-degradation(Lee void-vs-P 시간축) 우리 gap으로 명시.
