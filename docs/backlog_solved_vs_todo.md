# Backlog — 해결 vs 잔여 (통합 분류, 2026-07-18)

`docs/digest_model_application_backlog.md`(상세 LIVING)의 **상태별 재분류**.  "digest는 끝나도 적용은
별개"의 현재 정산 — 뭐가 닫혔고 뭐가 남았나를 한눈에.  상세 근거·커밋은 원 backlog의 각 행 참조.

> 요약: **핵심 적용 항목(A1-A6, A9)은 전부 CLOSED** → Phase-3 관문 해소.  A4′(SDCP)는 E_bind DFT
> 하나만 남음.  잔여는 (a) **본선** A7·B7, (b) **데이터/문헌 대기** A8·A11·B2·B4·B5·B6, (c) **future
> 시간축** A10·A12·A13·A14, (d) **연구트랙** D1-D6 + E-feeds.  하자(❗)는 없음 — 남은 건 확장·검증.

---

## ✅ 해결됨 (CLOSED)

| ID | 항목 | 어떻게 닫혔나 |
|---|---|---|
| **A1** | σ_e 조성방향 (Trevisanello 오귀속) | ★Phase-3 관문. **숫자 변경 불요 — 오류는 인용/라벨뿐**.  오배선 정정(커밋 29375b2, LOOCV 0.9531 불변 증명), σ_S/σ_P poly↔single 라벨 swap, `--sigma-S/-P` material INPUT 노출.  NCM811 default 10/5 유지 확정 |
| **A2** | wallP 조건부 (skeleton-spring) | production = **PURE MPM + regime-gate**(조건부 주입 X); 조건부·am-jam 둘 다 artifact 판정.  106/117 reliable.  조건부는 `--am-load-frac` opt-in 실험 플래그로만 잔존 |
| **A3** | binder `--coh` 양역할 | 비단조 `binder_cap(w,w*)` 구현(`--coh-ptfe`/`--binder-opt-wt`).  GPU sweep(real14 384) → raw porosity 단조감소가 물리적으로 옳음 확인; binder 비단조는 기계 binding-strength + σ-block(W2)에 있지 porosity 아님 |
| **A4** | se_coating carbon seeding | VGCF coat_embed **은퇴**(섬유 코팅 불가), SuperP thinky coat_block 구현 + divergence 런(porosity=bm EXACT, add-cov P≈S cap, econn film 지문 carbon cluster 85).  σ_e 방향은 STEP3 소관으로 이관 |
| **A5** | dispersion CV (분산 불균일도) | `additives.dispersion_metrics()` 2축(index-of-dispersion + SE→최근접첨가제 nn) + AM-마스킹.  selftest 4종 PASS.  payload `additive_dispersion` |
| **A6** | pore-τ DiffuDict | `step3_sigma.pore_tau()`: void상 σ=1 Laplace → τ=ε/D_rel.  z-crop + PTFE solid-stamp, selftest 6종.  ⚠ STRUCTURAL descriptor 전용(수송 τ 아님) |
| **A9** | 크기-의존 파괴 (압밀분) | `fracture_model.py` P_c=A·K_IC²·R/E*, 큰 poly AM_P 더 쉽게 파괴 = Kang&Shin 정합.  **사이클-버전은 A10로 이관** |
| **C1** | refs.bib Minnmann anchor | `@Minnmann2021bottleneck`(040537) 추가 + main.tex 배선 |
| **C2** | main.tex Sakuda softening | ">90%@>350 stated; ~87%@~300 digitized; glass≠argyrodite" |
| **C4** | Cronau 라벨 정정 | 2021·Br·GB-pellet(not single-crystal), bib+main.tex 재배선 |
| **F2** | fibre-rod emergent 좌굴 | **좌굴은 DEM 영역, MPM-scaffold 아님** 판정.  rod는 완주했으나 이 프레임이 축압축 안 줌 → prescribed curl(F1)이 MPM의 답.  `--fibre-rod` opt-in 잔존 |
| **STEP4-v2** | 동역학 충방전 솔버 (신규 트랙) | `scripts/step4_dyn.py` COMSOL **방정식-수준** 패리티(비선형 BV+구형확산+정전류/CV), 4-agent 리뷰, selftest 20/20(내부 자기검증·해석극한). ⚠ **수치 패리티 런(PyBaMM/COMSOL 매치드-조건 ΔV-RMS)은 대기** — 이게 defensible→bullet-proof의 유일 조각(defense_review_20260720).  #31(interfacial-impedance kinetics 칸)을 실현, B7(전류맵 viz)의 소스.  1C 쌍 production 진행 중 |
| **A7** | Phase-5 graded-z | ✅2026-07-21: `--poro-grad`(porosity(z) 게이트, 총량고정+ungated 폴백) + `--cb-ratio/--cb-grad`(K=8 설계프로파일 meta) + 밴드 실측 출력.  #286 gradient vs #20 uniform 둘 다 knob(재료의존이라 안 고름) |
| **A13** | PNM pore 위상지표 | ✅2026-07-21: `step3_sigma.pore_pnm()` nearest-seed 분할(★watershed_ift 오분할 734/7 기각) — n_pores·r_eq·pore-CN·throat·closed_from_top% + payload 배선, selftest 5종 PASS |
| **R_int P1** | 앵커DB+배선+σ_apparent 분리 | ✅2026-07-21: rint_eis_anchors.csv(kim2025 pdf_verified)·킷 --step4-r-int·webapp &s4rint=·pristine/cycled 병기(§6.1 해소)·적대리뷰 2건 즉수정.  + step4 운전-φ(z) export(phi_z) |
| (E) | Bielefeld2019 / Deysher2022 | 인용-확인(β=0.41 verbatim) / 포지셔닝(리뷰가 호명한 모델=우리 실현) |

---

## 🔶 거의 닫힘 (잔여 1개만)

| ID | 항목 | **남은 것 (딱 이것만)** |
|---|---|---|
| **A4′** | SDCP 전도성 바인더 | **E_bind DFT 재계산(gabia Phase-B)만**.  비교셋 런·σ_SDCP 스윕·매뉴스크립트 앵커·구현 전부 완료.  4/5 preview doped −1.52 eV(화학흡착급), neutral VERDICT 대기 |
| **B1** | σ_ionic 절대 검증점 | envelope 사실상 닫힘(3 EIS 앵커 0.04–0.14가 우리 출력 포위).  **압력·vol%→φ_SE 매핑 점대점만** 잔여 |
| **B3** | percolation 지수 정당화 | verbatim 값 ✅.  **paper-build 시 "universality-class 근거" 한 단락** 서술만 |
| **C3** | κ Wang2022 phantom | bib에 PHANTOM 경고 표시됨.  **실제 GB-phonon ref 확보 후 교체**(사용자 문헌 확보 대기) |
| **F1** | 압력-의존 seeding | VGCF ✅(curl=f(P)).  **SuperP·PTFE는 크기 앵커 문헌 부재** → 날조 금지, hook만.  Reisacher/Schneider/Bazzoun2025 등 digest 진행분 포함 |

---

## ⛔ 잔여 (TODO) — 우선순위별

### 🎯 본선 (지금/다음 — 데이터 이미 있음)
| ID | 항목 | 노트 |
|---|---|---|
| **B7** | 전류밀도 localization 맵 + 민감도 히트맵/레이더 | 물리 아님(viz 기능).  **STEP4-v2 필드가 자연 소스** — 지금 STEP4 하는 중이라 근접.  일부 이미 뷰어에 구현(전류밀도 필드·프로파일) |

### 📊 데이터·문헌 대기 (앵커 확보 후)
| ID | 항목 | 대기 대상 |
|---|---|---|
| **A8** | NCA CAM 옵션 | ✅스캐폴딩 완료(2026-07-21): `--cam nca`(σ_e Amin-태그) + docs/nca_material_preset.md — **★검증이 E=175 배선 차단**(assumed/umbrella-인용, 140 vs 175=출처 artifact).  잔여: σ_e 폼 σ_AM 재보정(WSL corpus)·K_IC(lab) |
| **A11** | collector R_int pristine↔cycled | ✅②경험궤적 도구(rint_cycle_traj)·③σ_apparent pristine/cycled 병기 완료(2026-07-21) + Phase2 R_int={0,10} 런.  잔여: ①pristine 정밀 digitize(Fig4c/6e)·조성-연속 실측 |
| **B2** | RNM(constriction) vs Stage-E | Bazzoun/Bielefeld2020 — Stage-E 기여 정량 |
| **B4** | multi-contact coupling | Varkey — 18× softening의 물리적 대안 비교 |
| **B5** | σ_grain 이중계상 재점검 | bulk spread {3.0/2.19/1.6/1.02} |
| **B6** | operating-pressure σ-degradation | Lee2025/Doux/Kang&Shin — void-vs-P + Warburg 시간축 |
| (E) | Bielefeld2020 / Minnmann2024 / Huang2025 | 폼 binder-blocking 항 / FIB-SEM trend 앵커 / DEM+LBM thermal 교차검증 |

### ⏳ future (사이클·시간축 — frame[5] 미보유)
| ID | 항목 | 노트 |
|---|---|---|
| **A10** | 사이클 chemo-mechanics | volume change+CZM 입계박리 = 우리 압밀 MPM의 사이클 짝.  ✅분업 명문화 완료(2026-07-21, mpm3d_calibration.md) — 본체는 β_Vegard digitize+CZM γ 앵커 후.  중간 다리 = A11-② 경험 R_int(N) 궤적(구현됨) |
| **A12** | 점탄성 MPM binder (spring-back) | SLS/Perzyna-Ludwick, η(T)/E(T) DMA → #285 3주 두께회복이 검증앵커.  4편 수렴 최대 untracked gap |
| **A14** | surface_conformal sheath | 연속 CNT-sheath 제3 morphology(두꺼운 전극 실제 승자).  #275 |

### 🔬 연구트랙 (접촉모델 D — 풀 digest 후 정량값 확보 시)
- **D1** 경로A: real E=24 + Thornton–Ning p_y캡 → 18× 연화 없이 300MPa porosity 시험 (★최우선 후보; So2022/Sangrós 완전 LAW 스펙 보유)
- **D2** Stage-E H 가변 (Jackson–Green H_G(a/R))
- **D3** SE-SE 점착 DMT F₀=2πRγ (γ≈1–2 J/m² SDCP DFT로 준비됨)
- **D4** Stage-E A/B 검증 (Storåkers)
- **D5** CBD 명시 bond (Sangrós/SJKR) — A3 구체화
- **D6** SE 취성균열 (de Vaucorbeil continuous-damage MPM) — 우선순위 낮음
- ⚠ DPC/cap은 적용 대상 아님 (resolved-grain 비물리 확정)
- E-feeds: Bucci(CZM)/Lyu(parallel-bond)/Sangrós/So2022 → D1/D5로 흐름

---

## 진행 메모
- 2026-07-18 작성 (상세 backlog 재분류).  **핵심 A1-A6·A9 + C1/C2/C4 + F2 = CLOSED**; A4′는 E_bind만.
- 현재 활성: STEP4-v2 1C 쌍 production(SBE/DBE-250) → 완주 후 본곡선 3종 + φ(z) Fig4e payload-only.
- 원칙 불변: 반쯤 digest된 논문으로 코드 선변경 금지(D/E는 풀 digest 후); §F1 날조 금지(크기 앵커 부재 시 hook만).
