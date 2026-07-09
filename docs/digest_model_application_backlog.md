# Digest → MODEL APPLICATION backlog (안 적용한 것 추적, LIVING)

논문 digest에서 "모델에 적용하자"로 식별했으나 **아직 코드/모델에 반영 안 한** 항목 추적.  digest는 끝나도
**적용은 별개** — 이 표가 그 잔여작업.  (출처: stage2_model_audit_vs_literature.md E2/E3/E4 + 각 lit_*.md +
사용자 enhancement 리스트 "σ_e 방향 + Phase5 graded-z + MPM --coh E3 + dispersion CV E2 + pore-τ DiffuDict".)
상태: ⛔ TODO · 🔶 IN-PROGRESS · ✅ DONE.

## A. 우선순위 (사용자 plan + 새 발견)

| # | 항목 | 출처 digest | 대상 코드 | 상태 | 노트 |
|---|---|---|---|---|---|
| A1 | **σ_e 조성방향 수정** — σ_S/σ_P를 LOCKED "single>poly"에서 **재료별 INPUT**으로; Trevisanello 인용 제거/교체 | Trevisanello 2021 (#11 mis-attribution), Oh #266 (poly>single 반대) | generate_comparison_plots.py `_SIGMA_S/P_LOCKED`, network_conductivity NCM(r) | ✅ **CLOSED 2026-06-30** (`docs/a1_sigma_e_direction_closeout.md`) | **결론: 숫자 변경 불요 — 오류는 *인용/라벨*뿐.** ✅ **오배선·라벨 정정 완료**(숫자 0 변경, 커밋 29375b2 = 주석/문자열만 → LOOCV 0.9531 **불변 증명**) — Trevisanello σ_e 오귀속 전부 "corpus-fit endpoints + GB-direction(Trevisanello-spirit) NCM(r)"로 교체, σ_S/σ_P **poly/single 라벨 swap 수정**(σ_S=AM_S single-crystal, σ_P=AM_P poly), `--sigma-S/-P` 이미 material INPUT으로 노출됨.  ✅ **숫자 결정 완료 (2026-07-03)**: NCM811 default **10/5 유지 확정** (closeout: live σ_S≈9.13/σ_P≈4.14 → 10/5 = ΔLOOCV −0.0004 동일·DOF−2; ratio=1 잠그면 −0.10 → 2× ratio 데이터-필수).  재료별(NCWA/NCA poly>single)은 `--sigma-S/-P` override로 **이미 노출 = A8(랩 NCA 재료) 소관, A1 아님**.  ⚠정정: 재적합 blocker는 **sklearn 아님**(σ_e fit=numpy `lstsq`) — corpus가 cloud에 없어 네 머신 필요.  선택 재확인(WSL): `python3 scripts/electronic_ablation_full.py` → LOOCV 0.9531.  ★ **Phase-3 관문 해소 (A1 FULLY CLOSED)** |
| A2 | **wallP 조건부 (skeleton-spring)** — BUILT·검증 후 **OPT-IN 실험 플래그로 보존**; production은 **PURE + regime-gate** | (자체 MPM 작업) | mpm3d_compaction `--am-load-frac`/`--floor-porosity` (default 0.0=OFF, opt-in); mpm_input_from_case **주입 안 함** | ✅ (★정정 2026-06-30, "A2 다시 확인") | ⚠ **이전 기록 STALE**: §10(06-26) "자동주입 채택"은 **§13(06-27)에서 뒤집힘**.  조건부·am-jam **둘 다 artifact 판정**(100_12: 조건부 11.6 과압축 / am-jam 22.6 과소, real_14도 16.7→18.4 깸).  ★ **production = PURE MPM(조건부 주입 X) + REGIME-GATE**(§13): SE/sol≥30% 또는 thick(8mAh) → MPM owns porosity; thin+SE-poor+AM-rich + mono-large(10:0/0:10) → DEM owns.  **106/117 reliable(|gap|≤4)**, catastrophic 11개=한 코너.  clamp는 DEM↔MPM gap(=validity 증명서) 가림 → 안 씀.  조건부는 _10(15.9→25)·real14(byte-identical) 검증됐고 **opt-in 실험용**으로만 남음.  코드 ground truth: `mpm_input_from_case.py:136` "production never injects".  세부 §13 |
| A3 | **E3 MPM `--coh` distribution-aware (binder 양역할)** — 과잉=σ차단/전해질차단, 부재=delamination; SAICAS adhesion↔binder | #271 Hong(PTFE void↓6.4%p), #264(cross-link modulus), #17 Song(Perzyna-Ludwick 점소성), #20 Bak(binder-z adhesion), #08 Bielefeld2020(binder σ-block), #285(spring-back) | mpm3d_compaction `--coh`(현 상수) | ✅ **CLOSED 2026-06-30** | **비단조 binder cap 구현**(mpm3d_compaction `binder_cap(w,w*)=(w/w*)·exp(1−w/w*)`, `--coh-ptfe`/`--binder-opt-wt`) — PTFE 상수 0.10 → wt%-의존: peak@opt(1.5wt%), Hong 1wt%→0.093(≈상수, backward-compat), over 6wt%→0.020(과가교 agglomeration↓), 0→0(delamination-prone). smoke-test 통과(rise-then-fall). ✅ **binder modulus 별개 항 이미 충족**(PTFE E=0.30 GPa vs SE 1.53, ADD dict). ⛔ 남음: (i) σ-block(과잉 resistive 막)=TRANSPORT 축 → **whatif_additives(W2)가 이미 PTFE σ_ion×0.74로 처리**, (ii) delamination 명시 failure-mode(부재)는 coh=0=무결합 proxy로만, (iii) ✅ **GPU sweep 완료(2026-06-30, real14 384, `docs/a3_binder_sweep_result.md`)**: porosity **MONOTONE** 15.91→4.40%(PTFE 0→8wt%), ∪ 아님 — **binder volume-fill가 cohesion 지배**.  ★ 결론(정직): **∪-in-porosity는 mis-framing**.  raw porosity vs binder = 단조감소가 *물리적으로 옳음*(solid↑→void↓; Hong 1wt% −6.4%p 방향 재현).  binder 비단조는 **(a) 기계 binding-strength**(binder_cap=active, early-servo wallP 0.32→0.56 GPa as coh 0→0.093) + **(b) σ-block(W2)**에 있지 porosity에 없음.  porosity 반등=spacer/agglomeration-void 항 필요한데 **문헌 근거 없음(Hong 1wt%만)→날조 금지**.  A3 binder_cap = 옳고 active, 그대로 유지 |
| A4′ | **SDCP(자가도핑 S-PEDOT 전도성 바인더) = A4 coat-seeding 첫 고객** — EDOT+pentyl-SO₃⁻ conformal AM-anchoring 필름(0.5wt%≈26-40nm sub-voxel → 1-voxel shell + volume-pin); σ_e/E/ρ = ⚠전부 PROXY(generic S-PEDOT 웹서치 — 할루시네이션 리스크, 사용자 지적 2026-07-09; **매뉴스크립트로 전면 교체 예정**)·유지되는 것: 분자정체+MLIP/CIF anchoring(사용자 계산) | (사용자 신규, 2026-07-08) | additives.py phase5 + A4 coat-seed + connectivity 뷰어(신규: AM-AM∪AM-carbon-AM 그래프→연결/고립 3D, 한양대 slide19 문법) | ⛔ | ★ 결정: 전체 backlog 선행 불요 — A4만 닫고 진행(연결성=기하 boolean, σ숫자는 STEP3서 A1 선행 후). 비교셋 VGCF+PTFE 1+1/0.5+0.5/SDCP 0.5. ★ cohesion 설계(2026-07-08 사용자): SDCP는 binder라 A3-계열 coh 필요하되 PTFE(bulk 얽힘 균일 coh)와 달리 **계면-anchoring**(술폰산-NCM) → AM-계면 가중 coh가 물리; 크기는 진성호 논문 SAICAS/peel 있으면 앵커, 없으면 §F1 hook. SEM 대조 루프: ①코팅 conformality(surface_frac 앵커) ②AM-AM neck/bridge(econn 엣지 실물) ③필름 nm두께(1-voxel 과대표현 문서화) ④가압 후 anchoring 잔존. PDF→litdb digest가 선행 최선. ★ DFT-anchoring 진행(2026-07-08, 사용자 sdcp_linio2_binding.md): doped −SO₃⁻가 LiNiO₂(104) Li-O층 삽입형 화학흡착 E_bind −18.2 eV(UMA-oc20 MLIP, 4-basin 수렴) vs neutral −6.3 — 정성(doped≫neutral, H-문지기) robust. ⚠ 절대값 3중 의심: (a) bare-anion vacuum reference = 구조적 overbinding → SO₃Li 염/charge-compensated 재계산 권고 (b) oc20 도메인 밖(하전 유기+layered oxide U/자성) (c) relax 중 H-transfer/표면재구성 여부 trajectory 확인. DFT(U-ramp E_slab 수렴 대기, dipole corr+U+자성 3-계산 동일세팅 필수)로 −5~−10 eV 보수화 예상 — 그래도 화학앵커 최상급. → 변환(CIF 기하 실측 2026-07-09): doped 삽입 확인 — 최저 분자원자 slab-top −0.14Å(삽입), 최단 O–Li **1.83Å**(격자 Li–O ~2.1보다 짧음 = 강한 이온결합)×배위 2, footprint **82.5Ų**; neutral은 +1.27Å 부유, O–Li 2.03Å×1, 116.5Ų 펼쳐짐 → binding 서열 doped≫neutral은 기하적으로 보장. γ=E_bind/footprint: DFT −5eV→**0.97 J/m²**, −10→1.94 (MLIP −18.2→3.5, 과대의심) ⇒ γ(SDCP-NCM)≈1–2 J/m² 보수 = binder 최상급(PVDF peel 0.1–1) → D3 DMT F₀=2πRγ 환산 준비 완료. ★ 정합-reference MLIP 재계산(2026-07-09, uma-s-1p1 단일점, E_slab 동일 −173.67): doped **−4.797** / neutral **−3.020 eV**, Δ=1.78 eV — 이전 −18.2는 reference bookkeeping 과대(적대리뷰 예측 −5~−10 적중; doped ref = 중성 radical(charge0 doublet)이라 anion-pathology 회피). Δ1.78 eV ≈ CIF 기하의 '추가 이온 O–Li 결합 1개(1.83Å)+삽입'과 정량 일치 = 기하·에너지 상호검증. γ 갱신: doped 0.93 / neutral 0.42 J/m² → **SDCP coh(AM계면) ≈ 10× coh_ptfe**(γ-비율 anchor, δ_c 모호성 상쇄) = MPM 매핑 준비 완료. 잔여: DFT U-ramp 교차검증(oc20 도메인 캐비엇), neutral H PBC 온전성 확인.  ★ 구현 완료(97767ae+리뷰fix 2026-07-09): seed_coat(균등 drape·cap-patchy·buried/out-of-box DROP) + doped/neutral variant(coh는 variant-무관 bulk 필름 무결성 — γ-비율은 미래 boundary-adhesion 항; neutral은 econn서 AM급 도체로 유지) + payload SDCP 채널/fib_mask fix + UI/route — **비교셋 런 대기.  ★★ 매뉴스크립트 앵커 반영(2026-07-09, docs/sdcp_manuscript_anchors.md): 형상=**0.3µm 분산 입자**(S3; conformal 필름 아님 — proxy 폐기), **E=23.6 GPa 앵커**(AFM S6, +CFL dt 가드), σ 앵커(ion ×0.80/e ×5.1 pellet), **S12: SDCP 단독 dough 불가 → 비교셋 = SBE(PTFE-only) vs DBE(PTFE+SDCP)** (SDCP-단독 런 비물리), ★E_bind 무효화(2026-07-10: 이전 계산이 곧은-pentyl 오분자 — ether-O 링커+methyl-분지 누락 → INVALID_WRONG_MONOMER, 재계산 스펙 anchors doc; --sdcp-clump NCM-cluster 가설 knob 추가), Fig4e 빈 'Electrochemical modeling' 패널 = econn 시각화 목표 슬롯.  wt% 조성 methods 확인 대기 |
| A4 | **E4 `se_coating_interface` carbon 옵션** — additives.py가 carbon을 bulk 간극에만 seed → CAM-표면-film carbon(SuperP coating 차단) 표현 못 함 | #19 Kim2025(SE-coating SuperP σ_e 3자리 붕괴) | additives.py (seed 위치) | 🔶 | **부분**(2026-06-30): webapp **해석모델** `whatif_additives`가 thinky(dry-coat)+SuperP → σ_e 붕괴(위치-의존 반전)를 이미 잡음 → with/without webapp ✓.  남은 ⛔ = **MPM seeding** 자체(additives.py가 SE-coating 셀에 carbon seed → 풀 GPU run서 구조적으로 재현).  현 SuperP>VGCF는 bulk-corner 한정; coating regime은 VGCF승.  ★ **mixing 재검증 대기 (2026-07-02)**: 현재 MPM seeding이 mixing을 거의 무시 → **VGCF는 ballmill=thinky=handmix 결과 완전 동일**(`seed_fibres`가 mixing 인자 안 받음; regime은 `mixing_regime`으로 기록만, seed는 전부 bulk).  SuperP는 CB_MIX로 ballmill≡thinky, handmix만 다름(k8/clump4).  **A4 구현(coat_embed/coat_block seeding) 후 → VGCF thinky(coat_embed)·SuperP thinky(coat_block)가 ballmill과 divergence하는지 재검증할 것** (input_6mAh_real_4 VGCF 1wt% ballmill=13.80 기준, thinky/handmix 재run해서 달라지는지 확인).  검증 도구: additive_test_campaign CSV에 mixing 컬럼별 행 추가.  ★ 업데이트(2026-07-09, 97767ae+리뷰fix): **SuperP thinky coat_block seeding 구현**(seed_coat AM-표면 필름, process-row surface_frac 0.70, cb_mix 메타는 실제 cblack 분기서만 기록) — 단 **🔶 유지** ①σ_e 방향 미검증: econn(연결성)은 coat film이 오히려 올릴 것 — Kim2025 '3자리 붕괴'는 저항 수준 = webapp whatif/STEP3 소관(두 층의 방향차 명시, 모순 아님 — binary percolation은 붕괴를 표현 못 함) ②VGCF coat_embed = dead-cond(fibre 분기 우선) ⛔ ③thinky-vs-ballmill divergence 재실행 대기.  thinky≢ballmill 경계 = CSV header A4-era 노트.  ★ 마감 계획(2026-07-10): ①VGCF coat_embed **은퇴**(섬유는 코팅 불가 — 물리로 확정, dead-cond 제거) ②SuperP 2wt% thinky divergence 런 1개(사전등록: porosity 11.94 동일/SE-cov↓/add-cov≫35.8/coat 메타) ③σ_e 방향=STEP3 — ①② 완료 시 CLOSED |
| A5 | **E2 dispersion CV** — 첨가제/입자 분산 불균일도 | #284 SiOx | additives.py / 합성 | ⛔ | |
| A6 | **pore-τ DiffuDict (유효-D voxel)** — pore network 유효확산 | #281 A3D | voxel_conductivity (D 채널) | ⛔ | |
| A7 | **Phase-5 graded-z** — z-band별 porosity(#286)+carbon:binder(#20) 2축 | #286 Yoo, #20 Bak | extract_2d_microstructure K=8 z-band | ⛔ | optimum 재료의존(#286 gradient vs #20 uniform) → 둘 다 비교 |
| A8 | **★⭐(랩) NCA(E=175) CAM 옵션 추가** — 랩 trend가 NCA(Ni0.88)인데 우리는 NMC811(140)만 | **Kang&Shin 2025**(랩 자체논문, E_NCA=175·E_LPSCl=22.1) | our_dem_baseline §0, 재료 파라미터, σ_e σ_AM 재보정 | ⛔ | ★ 랩 소재 정렬.  E_LPSCl 22.1는 Bazzoun/우리24 확인; σ_e(NCA)·D_Li는 NMC811과 다름(FEM σ_e=1 S/m,D=3e-14) → σ_e 폼 σ_AM 재보정 필요 |
| A9 | **★⭐(랩) 크기-의존 파괴** — AM_P(큰 다결정)일수록 fracture↑ (Auerbach 입경-스케일링 σ_crit∝1/√d) | **Kang&Shin 2025**(10µm c_Li 구배 3µm 대비 ~10×·damage→1; 큰입자 균열), Lee2025(PC깨짐) | network_conductivity fracture, Auerbach 임계 | 🔶 | **압밀-버전 이미 충족·검증(audit D1)**: `fracture_model.py:113` P_c=A·K_IC²·R/E*, AM_S K_IC>AM_P → 큰 poly AM_P가 더 쉽게 파괴(a9_50_p02: AM_S P_c 5.357>AM_P 1.446 mN, AM_S 95.7% intact / AM_P F/P_c 15.96) = Kang&Shin "큰입자 균열"·#285 정합.  ⛔ **남음=사이클-버전**(Li-구배 driver, CZM damage→1) = frame[5] 미보유(future, A10) — 압밀(접촉응력) vs 사이클(Li-구배) driver 분업 명시 |
| A10 | **★⭐(랩) 사이클 chemo-mechanics(future)** — volume change(NCA 5.9%)+cohesive-zone 입계 박리 = 우리 *압밀* MPM의 *사이클* 짝 | **Kang&Shin 2025**(FEM Voronoi+CZM damage 0→1, ε_d=Ω/3·Δc_Li) | (신규 cycling FEM/MPM, frame[5] 시간축) | ⛔ | future.  MPM 문서에 "압밀=J2(우리) / 사이클=cohesive-zone(랩 FEM)" 시간축 분업 명문화부터 |

## B. 검증/교차대조 (모델 값 확인·정당화 — 적용은 선택)

| # | 항목 | 출처 | 상태 | 노트 |
|---|---|---|---|---|
| B1 | **σ_ionic 절대 검증점 채택** — exp σ_eff,ion을 우리 σ_ionic anchor로 (vol% CAM:SE→φ_SE 매핑 후) | Bazzoun 2026(EIS 0.065-0.137), Minnmann 2021(0.17@42vol%), Oh#266(0.034-0.055), Hong#271 | ⛔ | 우리가 부족했던 외부 실험앵커 |
| B2 | **RNM(constriction) vs 우리 Stage-E(plastic-area)** 같은 구조서 대조 → Stage-E 기여 정량 | Bazzoun 2026, Bielefeld 2020(σ_eff continuum, constriction 없음) | ⛔ | Bielefeld 2020 high-CAM서 RNM 과소예측 → Stage-E가 보정? |
| B3 | **percolation 지수 정당화** — 우리 √(φ−φc)·CN² 등 vs β=0.41(3D site), p_c=7.83·ln d+36.67 | Bielefeld 2019 | ⛔ | 우리 exponents의 universality-class 근거 |
| B4 | **multi-contact coupling** = 18× softening 대안(밀집 과강성) 비교연구 | Varkey 2026 | ⛔ | 우리 경험적 softening의 물리적 대안 |
| B5 | **σ_grain 이중계상 재점검** — pellet(1.02-1.6) vs Cronau single(3.0) + Cronau(r_SE) GB factor | Bazzoun, Cronau, Minnmann(bulk 1.6) | ⛔ | bulk spread {3.0/2.19/1.6/1.02} |
| B6 | **operating-pressure σ-degradation** (void-vs-P 시간축) + **사이클-Warburg 열화 시그니처** — 정적 모델에 없는 시간축 | Lee 2025 co-rolling, Doux 2020, **★⭐Kang&Shin 2025**(EIS-TLM R_ion 불변/R_int·R_w 급등, R_w∝δ_s) | ⛔ | future: P sweep→void→σ↓; + 균열→tortuosity↑→R_w↑(eq2) 사이클 시그니처 |

## C. paper-build (refs.bib / main.tex 정정 — 출판 전)

| # | 항목 | 상태 |
|---|---|---|
| C1 | refs.bib `@Minnmann2021bottleneck`(040537) **추가됨** ✅ — anchor 인용을 그쪽으로 배선(main.tex) | ✅ (2026-06-30) porosity anchor 문장이 `\citep{Minnmann2021bottleneck}` 인용하도록 배선 |
| C2 | main.tex Sakuda "87%@300" → ">90%@>350 stated; ~87%@~300 digitized trend; glass≠LPSCl" softening | ✅ (2026-06-30) softened: trend match, glass≠argyrodite, digitized 명시 |
| C3 | refs.bib `@Wang2022`(κ) = phantom → 일반 GB-phonon refs로 교체 + main.tex κ 인용 정정 | 🔶 (2026-06-30) bib에 PHANTOM 경고+placeholder 표시 (날조 금지); **남음=실제 GB-phonon ref로 교체**(네가 문헌 확보 후) |
| C4 | Cronau 라벨 정정(연도 2021, Br not Cl, GB-pellet not single-crystal) | ✅ (2026-06-30) bib `@Cronau2022`→`@Cronau2021` (vol6/3072-3077/1c01299) + GB-pellet·Br note; main.tex 인용 전부 재배선 |

## 진행 메모
- 2026-06-26 작성.  논문 digest batch(Trevisanello/Cronau/Minnmann/Doux/Sakuda/co-rolling/Bielefeld19+20 등)
  완료 → **적용은 이 backlog가 추적**.  사용자 plan대로 논문작업 종료 후 A1(σ_e 방향)부터 진행.
- A2(wallP 조건부)는 자체 작업으로 **완료**(13 corner 재실행 + §8 3-regime 분류 끝, porosity CLOSED).
- 상태 갱신 2026-07-03: **A1 FULLY CLOSED**(숫자결정=10/5 유지 확정) · **A3 CLOSED**(binder_cap + real14 GPU sweep 단조) · **A4 부분**(webapp whatif ✓ / MPM coat-seeding ⛔ = mixing thinky divergence + SuperP coat_block σ_e붕괴가 여기 걸림, STEP3 전제) · A5-A7/B/C 미착수.

## D. 접촉모델·소성 digest 14편 적용 backlog (2026-06-26 일괄, `litdb/contact_models_layer_map.md`)
- **D1 ⛔ 경로 A 구현 (★최우선 후보)** — real E_SE=24 GPa + **Thornton–Ning p_y캡**(eq2→9→19→29, p_y≈1.6σ_y, LPSCl
  σ_y 0.05–0.30) LIGGGHTS에 → 300 MPa porosity가 **18× 연화 없이** 나오나 시험.  선례 So 2021(LPS 0.98).  접촉별 항복
  gate = Kogut–Etsion ω_c/R=6.43(Y/E)².  ⚠ TN 단독은 ρ>0.7 under-stiff → Varkey multi-contact F_mc 필요할 수도.
- **D2 ⛔ Stage-E H 가변 보정** — Jackson–Green **H_G/σ_y=2.84[1−e^{−0.82(a/R)^{−0.7}}]**: a/R>0.2 dense 접촉서 H<3σ_y →
  현 상수 H=3 가정이 면적 과소.  우리 real-contact a/R 분포 뽑아 Stage-E의 A_tabor=F/H를 H_G(a/R)로 교체.
- **D3 ⛔ SE-SE 점착 정량** — DMT **F₀=2πRγ**(SE=DMT 체제, 작고 단단)로 `adhesionStiffness` k_c(=1e6)·MPM `--coh` magnitude
  고정.  γ(LPSCl 표면/계면 점착일) 문헌값만 잡으면 됨.  Pasha 에너지일관 A_p·Γ가 Luding k_c·δ보다 물리적 시작점.
- **D4 ⛔ Stage-E A/B 검증** — Storåkers **A=2πc²(m)rh**(c²≈1.4 이상소성 pile-up) vs 우리 Stage-E 경험면적 A/B 비교
  (Mesarovic–Fleck a²/2hR₀→1.4 가 독립 확인).  Martin–Bouvard가 Storåkers 사용.
- **D5 ⛔ CBD 명시 bond (= A3 구체화)** — Sangrós 영구파단 bond / Ngandjong **SJKR(CED×면적, 끊김·재형성)** 두 옵션;
  SJKR이 PTFE cold-weld(`--coh`)·fibrillation 1차 근사에 더 가까움.  Stage-2 부피점유 → 명시 bond 승격 시 템플릿.
- **D6 ⛔ SE 취성균열 (frame[5] 공백)** — yun2023: halide(+LPSCl 고압) SE *자체* 균열.  우리 Auerbach는 AM-only,
  MPM은 ductile J2 → SE 취성균열 불가.  de Vaucorbeil 리뷰의 continuous-damage/cohesive MPM이 구현 경로(우선순위 낮음).
- ⚠ **DPC/cap은 적용 대상 아님** (resolved-grain에 cap=비물리, Klár로 확정).  cap은 homogenized-REV(`cap_compaction_heckel.py`)
  에서만 옳음.  우리 J2+ν0.49는 재료클래스 유도 필연 → 변경 불요.

## E. #17-34 digest batch → backlog 매핑 (2026-06-27)

19편(#17-29 완료 13 + #30-34 진행 5 + Bazzoun2025) digest의 **모델 적용 후보**.  digest는 끝나도 적용은 별개 — 여기서 추적.

| 논문 | feeds | 적용 내용 | 상태 |
|---|---|---|---|
| **Bielefeld 2019** | **B3** | β=0.41(3D-site strength 지수)·p_c=7.83·ln d+36.67 **verbatim 확인** → 우리 √(φ−φc)·CN²·f_p³ universality-class 근거.  ⚠β=0.41≠우리 0.5(mean-field) 동일시 금지 | ✅ 확인(인용만) |
| **Reisacher 2023** | **A4** | carbon 전자-percolation p_c≈4 wt% C65 (LPSCl=우리 SE, 보정無) → additives.py σ_e carbon-gate `g_C=f(wt_C65−p_c)` 캘리브레이션 + Bielefeld AM-p_c의 carbon 짝 | 🔶 부분(2026-06-30): p_c≈4wt% soft-gate가 webapp **해석모델** `whatif_additives` σ_e boost에 적용됨(`_CARB_PC_WT=4.0`).  남음 = MPM seeding측 g_C 캘리브레이션 |
| **Minnmann 2024** | **B1** | FIB-SEM σ_ion 0.05–0.11·porosity 6–10%·coverage 20–50%·CAM util 62–77% = frame[4] TREND 앵커(글래스 composite, 절대전이 금지) | ⛔ TODO |
| **Schneider 2023** | **B5/B6** | σ vs 입경·압력 실측 → 우리 Cronau(r_SE) SE-size 인자 + σ-vs-porosity(압밀) 검증 (material-match 확인 대기) | 🔶 digest 진행 |
| **Bucci 2017 (CZM) + Bucci 2018 (delamination) + NMC811 입계균열 2023** | **A10/B6/D6** | 사이클 chemo-mech 균열(Vegard strain driver, 우리 압밀-Auerbach의 사이클 짝); SE 취성균열 = de Vaucorbeil continuous-damage MPM(D6) 구현경로; 박리→ASR↑(B6 시간축).  ⚠우리 미보유 frame[5] | ⛔ TODO(future) |
| **Lyu 2025** | **A3/D5** | CBD **moment-전달 parallel-bond** = PTFE 굽힘강성 최적합(Sangrós force-bond보다 우수); solvent fluid-substitution = 건식≠습식 | ⛔ TODO |
| **Sangrós 2019** | **D1/A3** | Thornton–Ning 항복캡 + **나노압입 YR=8.59e-3·x(R²0.89)** = 경로A YR 실측 LIB 선례; 명시 binder bond | ⛔ TODO |
| **So 2022** | **D1** | rate-h_eq + F_th=H·A_con + area/spring factor = 경로A **완전 LAW 스펙**; +소결 fusion-bond(우리 미보유) | ⛔ TODO |
| **Bazzoun 2025** | **D1/B4** | DEM 파라미터 민감도(friction 지배)·high-f_CAM rigid-sphere 불일치 = 경로A/Stage-E로 풀 dense-regime; 우리 캘리브레이션 우선순위 가이드 | 🔶 digest 진행 |
| **Huang 2025** | **B (신규)** | DEM+LBM ETC = 우리 σ_thermal Stage-T1 독립 교차검증(다른 방법, 산화물); LBM(또는 TauFactor)을 우리 DEM dump에 돌려 thermal cross-check 가능 | ⛔ TODO(검증) |
| **Mun 2025 / Liu 2025 (dry-electrode 리뷰)** | **A3/공정** | 건식 PTFE fibrillation·co-rolling 공정 landscape → CBD 모델 + 압밀 프로토콜(co-rolling) 맥락 | 🔶 digest 진행 |
| **Interfacial-impedance formulation (#31)** | **kinetics(신규)** | R_ct/double-layer/Warburg 해석식 → 우리 geometric ASR 위에 kinetics 칸(kim2025 미보유) 추가 경로 | 🔶 digest 진행 |
| **Deysher 2022 (리뷰)** | positioning | transport+mech 커플 리뷰가 호명한 정량 모델 = 우리 DEM σ-삼중항↔MPM이 실현(미래방향 4/6 충족) | ✅ 포지셔닝 |

## F. Additive mechanics fidelity — 압력-의존 형상 (2026-06-30)

첨가제(VGCF/SuperP/PTFE) 형상을 **가압 압력에 반응**하게 만드는 작업.  계기: 완벽 직선 VGCF가
artifact 같다 → 실제 VGCF는 wavy + 가압 시 좌굴.  2-tier.

| # | 항목 | 대상 | 상태 | 노트 |
|---|---|---|---|---|
| **F1** | **압력-의존 PRESCRIBED seeding** — seed 형상 파라미터를 press(`args.target`)의 함수로 | `mpm3d_compaction.py` `_press_curl`, `--vgcf-curl` | 🔶 VGCF ✅ / SuperP·PTFE TODO | **VGCF DONE**: `curl=f(P)=0.095·(1−exp(−P/0.30))`, 0.06@0.30GPa 보존, buckling+post-buckling 포화 근거.  porosity 불변(부피 보존).  **SuperP**(aggregate 구조붕괴/compaction vs P)·**PTFE**(fibrillation degree vs P)는 *방향*만 lit-지지(CB structure collapse·dry fibrillation), *크기* 미앵커 → 날조 금지, conservative tunable hook으로만(요청 시).  σ_y 비대칭: SuperP/PTFE는 soft(σ_y<press)라 MPM서 이미 소성압밀=부분 emergent, VGCF만 prescribed 필수 |
| **F2** | **EMERGENT sub-grid bonded-rod / Cosserat MPM** — 섬유가 기존 MPM 가압에 *실제로* 좌굴 | `mpm3d_compaction.py` `--fibre-rod` | ✅ **CLOSED (2026-07-01): 좌굴은 DEM 영역, MPM-scaffold 아님** (`docs/fibre_rod_mpm_design.md` §RESULT).  rod는 GPU서 **완주**(blind Taichi 작동 ✓)했으나 섬유 straightness **0.997**(거의 곧음), `--rod-stiff` 0.6→0.15(4×) 무변 → **stiffness/coupling 가설 기각**, 원인=이 프레임이 섬유에 축압축을 안 줌.  frozen-AM scaffold + 매끄러운 SE 흐름 = 섬유 평행이동만; 진짜 좌굴=이산 입자-pinching=**DEM/접촉**(연속체 MPM 구조적 불가).  numpy서 "압축→Euler좌굴" 증명됐으니 rod는 옳고 driving이 없는 것 → **MPM은 Tier-1 prescribed curl로 VGCF 표현**, emergent 좌굴은 DEM bonded-fibre(가압=LAMMPS) 미래과제.  `--fibre-rod`는 opt-in으로 코드 잔존(mobile-AM/고압축 프레임용).  SuperP breakable-aggregate도 같은 이유로 보류 | **MPM에서 가능 — 단 격자 refine 아님**(150nm fibre를 100µm box서 resolve=~10⁹ cell, 불가).  경로 = fibre 점에 **명시적 director(축+굽힘 강성) + bond**를 얹어 sub-grid rod로 coupling → emergent 좌굴.  ★ **MPM이 올바른 집**: MPM은 이미 가압함(servo/hold) → rod만 추가; **DEM(LIGGGHTS)은 가압 불가→LAMMPS bonded-particle 별도 sim 필요**(사용자 확인).  rod엔 **실제 VGCF E≈200 GPa**(굽힘은 rod가 explicit하게 carry → 연화 E=10과 분리, 더 물리적).  per-additive: VGCF=좌굴(최우선, 탄성유지라 prescribed 외 방법 없음), PTFE=fibril draw/align(+A3 coh), SuperP=bonded-aggregate 압밀/fragmentation.  COST: per-point 방향 DOF+굽힘에너지+bond+grid coupling+**stiff bond→dt 빡빡(CFL)→느려짐**; Taichi 구현 가능, bounded.  payoff = σ_e network 형상(percolation/τ) → **STEP 3에서 측정 σ_e로 검증**.  frame[5]상 이산결합역학이지만 가압제약 때문에 MPM-rod가 실용적 home |
