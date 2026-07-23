# litdb → 모델 적용표 (#33 phase-1) — webapp v3 (ML·이종기술) 스코핑

litdb 65장(frozen 2026-07-16) + `digest_model_application_backlog.md` + pipeline + `predictor_engine.py`
정독 종합.  각 기전 → 우리 모델 적용 상태 → gap.  frame[5]: DEM=수송 / MPM=역학, 코팅=화학 CEI 축.

범례: ✅ APPLIED · 🔶 PARTIAL · ⛔ NOT-APPLIED.

## (A) 적용표 — 요약 (전문은 아래 섹션별)

**전부 적용된 코어 (STEP1-3 수송·역학):** Holm/Kirchhoff 접촉망(T1, Bazzoun 2026 frame[4] 교차검증)·
σ_ionic 스케일법 LOOCV0.975(T2)·Cronau σ_grain(T3)·σ_e Stage22.5(T5)·σ_thermal Ridge(T8)·
Minnmann/EIS 절대앵커(T13/14)·18× 소프트닝(M1)·MPM J2 챔피언(M2)·Furnas dip(M11)·rigid-AM
license(M12)·Auerbach 파괴(F1-4)·SDCP(A4′ C2)·SWCNT sheath(A14 C3)·graded-z(A7 C10)·
additive dispersion(CA4)·PTFE penalty(CA1-3).

**주요 미적용/부분 (v3 후보):**
- **ML 루프 (Duquesnoy 2023): ⛔** Sobol DOE → SISSO 형식발견 → Bayesian 다목적 역설계.
  = 우리 5-phase 비전의 출판된 원형.  corpus(88-132) 준비됨·frame-neutral. **최고 레버리지.**
- **코팅 이종기술: 🔶 3경로 미통합** — 화학 CEI(STEP5 --chem-x)·계면전도(Han2025 t/σ_b, 미노출)·
  구조seeding(SDCP/SWCNT ✅, So2022 core-shell hook 비어있음).  → 통합 "코팅 프리셋 셀렉터".
- **화학/kinetics 축: ⛔ 최대 구조 gap** — R_ct/C_dl/Warburg(D5)·계면 화학열화(D9)·T의존 Ea(T12).
  lab EIS-TLM 영역, STEP4-v2가 자연 위치.  앵커 부분적(R_ct 크기 O, Ea 절대표 X).
- **점탄성 spring-back (M13): ⛔** 4논문 수렴(Sangrós/Hong/Song), MPM은 rate-independent J2.
- **yield-cap 접촉 (M6, D1): ⛔** real E=24+p_y cap으로 18× 소프트닝 제거 — So2021/2022 LAW 완비.

## (B) 미적용 gap 랭킹 (가치 × 실현성) — v3용

| 순위 | gap | 가치 | 실현성 | 앵커 | frame[5] |
|---|---|---|---|---|---|
| **1** | Duquesnoy ML 루프 (Sobol→SISSO→Bayesian 역설계) | ★★★ | ★★★ | ✅ 준비(방법론 출판·corpus 존재) | frame-neutral 설계층 |
| **2** | 코팅-CEI 프리셋 (LNO/LZO/Li₃PO₄→억제+R_ct) | ★★★ | ★★ | 🔶 크기앵커O(Kim LNO 13-20×·Payandeh 93%@200)·shape ASSUMED | 화학축 (비-DEM/MPM) |
| **3** | So2022 SE-코팅 구조seeding (core-shell) | ★★ | ★★ | 🔶 방향O·σ_e 크기=GPU | 구조(DEM/MPM) |
| **4** | 계면 kinetics 축 (R_ct·C_dl·Warburg·σ(T)) | ★★ | ★★ | 🔶 R_ct 크기O·Ea 절대X | kinetics(EIS-TLM) |
| **5** | SISSO σ-폼 교차검증 | ★★ | ★★★ | ✅ 준비 | frame-neutral 검증 |
| 6 | thermal LBM/TauFactor 교차체크(T9) | ★ | ★★★ | ✅ 방법(산화물→trend) | frame[4] |
| 7 | Bielefeld 바인더-blocking 고-AM 비선형(T15) | ★★ | ★★ | ✅ | 수송폼 refine |
| 9 | Path-A yield cap(M6/D1) | ★★ | ★★ | ✅ LAW 완비 | DEM 접촉법 |
| 10 | 점탄성 MPM binder(M13) | ★ | ★ | 🔶 검증O·⚠V100 | MPM 시간축 |

## (C) webapp v3 후보 (우선순위)

### (i) ML 예측기 확장 (최대 레버리지) — `predictor_engine.py`(GPR+RF, Phase 1-2)를 Phase 3-5 폐루프로
1. **[HIGH] SISSO 병렬 형식발견** — corpus에 symbolic regression, hand-폼과 CV-R² 병기.  √φ_eff·CN²·√cov
   재발견 시 frame[4] 독립확인; σ_thermal은 SISSO 실패 예측(다경로) → "Ridge irreducible" 논거 강화.  `pysisso`.
2. **[HIGH] Sobol DOE explore** — `active_learning_suggest.py`(현 exploit-corner)에 저불일치 Sobol/Saltelli
   → σ_ionic close-out의 구조 gap(CN≥7, mid-thickness) 균일충전.  `SALib`.
3. **[HIGH] Bayesian 다목적 역설계** — GP+GP-Hedge(LCB+EI+PI)+앱-가중 scalarization(fast-charge=min τ·max σ_e /
   high-energy=max density) over 전체 metric.  predict→synthesize(Phase4)→z-stack(Phase5) 1루프.  `scikit-optimize`.
4. **[MED] 예측 타깃 확장** — STEP4(ΔV·rate·반응균일)·STEP5 R_int(N) 기울기·grade축 추가 → 수송+수명 커버.
5. **[MED] additive Δσ 학습** — W2 whatif σ델타를 ML 타깃 ("VGCF 2wt%→Δσ_e" 직답).
6. **[MED] PDP/KDE/radar 패널** (Duquesnoy Fig4-6) → group-compare (B7).

### (ii) 이종기술/코팅 통합 (2번째 기둥) — coating=화학 CEI 축.  현 3경로 → 1 "코팅 프리셋 셀렉터"
- **(a) 화학 CEI (STEP5):** `b1_chem_fade --chem-x` 이미 화학몫 개방 → 코팅별 프리셋(LNO 13-20×·Payandeh
  93%@200·LZO 6-8nm).  크기=앵커, shape=√N(fit_rint_curve 게이트).
- **(b) 계면전도 (Stage-E/STEP3):** 7nm ASR=t/σ_b (Han2025) — 전도코트(σ_b≈0.1mS/cm)≈투명 5e-3 ↔ 절연 ≥10³ block.
  `--coat-sigma-b` 노출(W2서 파생, 미노출).
- **(c) 구조 seeding (STEP2):** SDCP/SWCNT ✅ → So2022 `# A4 HOOK` 채워 LNO/carbon을 CAM-표면 shell로.
- **통합 프리셋 = {σ_ion, σ_e, CEI억제, R_ct, γ, seed-morph}.**  준비 프리셋: SDCP·SWCNT(완비), LNO·LZO·carbon.
  SDCP σ 두께스윕{15/50/150/1500}(+0.8→+63.4%)을 Li2026 코팅 두께딜레마의 템플릿 답으로 일반화.

### (iii) 이종기술 모델링 (litdb 지지)
- **층상/graded (Phase5)** — A7 `--poro-grad`/`--cb-grad`(K=8) → UI "config를 z-layer로 stack"(사용자 최종비전).
- **이종 CAM** — SC+PC(AM_P/AM_S 이미 구분, Jung2023 bimodal).
- **이종 코팅 커버리지** — patchy vs conformal(`seed_coat surface_frac` 파라미터화됨).

## (D) 정직 플래그

**✅ 앵커 완비 (v3 지금 구현 가능):** Duquesnoy ML 루프(방법론+corpus)·σ_ionic 절대 envelope(3 EIS)·
코팅 CEI **크기**(Kim LNO 13-20×·Payandeh)·SDCP σ(ion×0.80·e×5.1·E23.6)·Reisacher p_c≈4wt%(정확 LPSCl+C65)·
So2021/2022 yield-cap LAW·DMT γ 1-2 J/m²·Furnas dip.

**⛔ 앵커 없음 (v3 날조 금지·신규 digitize 필요):** 코팅 CEI **shape**(√N vs linear — ≥4 N점 실측곡선 필요)·
SuperP/PTFE 압력-shape 크기·SDCP E_bind(DFT 대기)·i0 SC/PC 정량·NCA E=175(assumed, 측정 아님)·
T의존 Ea 절대값(3점 trend만)·GB-phonon κ(Wang2022=phantom)·운전압 σ-열화 크기·bimodal 1.51%(shrink-proxy 아티팩트).

## 핵심 결론 (v3 스코프)
1. **최고 레버리지 = Duquesnoy ML 루프** — 우리 5-phase 비전의 출판 원형, 앵커·corpus 준비, frame-neutral.
   `predictor_engine.py`(GPR+RF Phase1-2) → 설계→최적화→합성 폐루프(Phase3-5).  ⚠ sklearn/pysisso = WSL(클라우드 부재).
2. **코팅(이종기술) = 3경로 통합** — 화학CEI·계면전도·구조seeding → 1 "코팅 프리셋 셀렉터".  CEI 크기=앵커·shape=ASSUMED.
   ★클라우드서 빌드·검증 가능(parametric, sklearn 불요).
3. **화학/kinetics 축 = 최대 구조 gap** (R_ct·C_dl·Warburg·계면 화학열화·T의존) — STEP4-v2 위치, 앵커 부분적.
4. **STEP1-3 코어는 전부 적용·교차검증됨** — 남은 건 연구트랙 refine(D1-6, B), v3 블로커 아님.
