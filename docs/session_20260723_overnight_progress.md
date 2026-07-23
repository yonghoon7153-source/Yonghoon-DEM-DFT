# 2026-07-23 오버나잇 세션 진행 (정본)

브랜치 `claude/stoic-knuth-NObVQ`.  전부 커밋·푸시.  3 대주제: **필드 프레임 라벨링(발표)** ·
**첨가제 전면감사+수정** · **v3 ML(EIS/DRT/ICA + surrogate + cycling)**.

## 1. 필드 프레임 라벨링 — "1V 물리 ≠ 1C 물리" (발표 대비)
사용자 통찰: 전류밀도 필드가 @1V(수송 프로브)냐 @1C(운전)냐로 물리가 다름.  선형해라 **색 패턴(초점)은
1V·1C 동일**, 컬러바 절대숫자만 다름.
- **비교표**: ⟨J_e⟩·⟨J_ion⟩ **@1V(A/cm², σ/L 프로브)** + **@1C(mA/cm², =j_1C 운전전류, 전류보존 e=ion)** 병기.
- **필드 컬러바**: **@1C 운전 전류밀도를 주라벨(🔋)** 승격, @1V은 "선형 프로브(운전점 아님)" 각주.  단일모드
  = @1V🔎+@1C🔋 두 박스.
- **비교 공동스케일 @1C-peak 프레임 추가**(드롭다운): σ-max=@1V 수송(σ_eff 정렬→DBE 천장) vs @1C-peak
  =운전 핫스팟(focus×j_1C→SBE 천장 273).  **프레임별 천장 케이스 자동전환** (1V→DBE, 1C→SBE).
- **교훈(단위차이 진단)**: 논문(σ-구동, 전자≫이온 56×) vs 우리 @1V.  절대차이=**바이어스(우리 1V vs 논문
  운전)**, VGCF 아님.  @1C 운전전류=용량×rate=**VGCF 무관**; @1V만 σ_e∝VGCF(3wt%+SDCP) 반영.
  **신뢰**: @1C 운전값(3.1 mA/cm² 등)=실제 나올 값(상용급) · @1V=프로브(비운전) · 피크·σ_e절대=상대신뢰.
- **킷 배선**: 취성 fracture-scaffold(opt-in `MPM_FRACTURE=1`)+Joule 발열맵(기본ON)+periodic-σ(opt-in
  `MPM_PERIODIC_SIGMA`) → `mpm_input_from_case.py` webapp zip 에 v3 열화물리 포함.

## 2. 첨가제 전면감사 (5 병렬 에이전트 + 2차 코드·물리 리뷰)
계기: v3 넘어가기 전 "우리 장점(VGCF/PVDF/SuperP 구현) 문제없나 처음부터".  ★PVDF=사용자 misspoke→PTFE.
- **코어 물리 GREEN**: phase(MPM save)↔sid(STEP3) **규약 중앙화**(`step3_sigma.rasterize:147`, 7재료 정확,
  회귀테스트 `_selftest_swcnt`) · 탄소 전자망전용(이온망 3중배제) · PTFE 양전도망배제 · #30 저항보존(bitwise
  불변) · 도징 단위정확·단일소스 · **날조 문헌값 0**.  겁낸 "VGCF→AM_P 둔갑" 버그 **없음**.
- **수정 라벨/문서 7**: E_bind −4.8eV INVALID 명시(wrong-monomer)×4 · step3 docstring SDCP 250 · coating
  seed_morph coat→particle · docs 150→250 · a3 ∪-shape→monotone(확정) · voxel_conductivity 레거시 σ 미정합
  경고 · grade carbon 1000 §F1 태그.
- **수정 물리 3(각 3렌즈 리뷰)**: (F1/F4) **grade 복합밀도 산술→조화평균**(질량분율 부피가산, 80:20서
  +13% 편향 제거) + 밀도 4.8/2.0·C_am 175 통일(x-window 정합).  (MED-1) **SuperP n_objects=실제
  agglomerate-chain수**(seeding·σ 불변, 라벨만; ★2차리뷰 HIGH버그 `_fid.max()+1`이 전역오프셋 부풀림
  →`np.unique().size`).  (MED-2) **SWCNT `ion_m`에 sid8 포함**(투명 σ_i>0 게이트)=σ_ion 솔브↔STEP4 BV
  계면 정합(--swcnt-ion-block 시 자동제외).  step3 SELFTEST PASS.

## 3. v3 ML (frame[5] payoff = 물리-유도 feature; docs/ml_v3_surrogate_cycling.md, eis_drt_ica_cv.md)
- **v3-1 EIS/DRT/ICA/CV** (`eis_drt_ica.py`): 물리-기반 Randles(R0+R_ct∥C_dl+Wo Warburg) 각 소자를
  STEP3(σ)/STEP4(BV·구형확산) 물리서 유도 → 실험 eis_fit 회로(R0-p(R1,CPE1)-Wo1)와 정합=frame[4] 대조.
  Tikhonov DRT 가 **R_ct arc(130Hz)↔확산(94s) 분리** · dQ/dV ICA · CV.  C_dl 앵커·R_w ASSUMED §F1.
  selftest 5/5.  CLI(--metrics 케이스→Nyquist/DRT CSV).
- **v3-2 surrogate** (`ml_cycle_surrogate.py`): 설계13+**물리15(★차별: σ-triad·τ·coverage·CN·f_perc·focus·
  Holm·fracture)**+cycle → R_int(N)·retention·σ 예측.  rint_growth/retention ASSUMED-FORM(Kang&Shin 형).
  CycleSurrogate GPR+RF(sklearn WSL, import-guard graceful).  타깃 provenance §F1.  결측=nan(날조금지).
- **v3-3 cycling 인제스트** (`cycling_data_ingest.py`): **§F1 chemistry 게이트** — sulfide=ABSOLUTE /
  liquid(Severson/NASA/Stanford/Oxford)=FORM/METHOD-ONLY(기전 다름).  CSV 인제스트+자동헤더+fade/R_int FORM
  적합(liquid=form_only 라벨) + 데이터셋 레지스트리.  selftest PASS.

## 남은 것
WSL 실학습(sklearn) · C_dl/R_w 실험 EIS 앵커(eis_fit CPE→µF/cm²) · 오픈소스 실다운로드 · webapp
EIS/사이클곡선 패널 · STEP4 PyBaMM 패리티(#5) · A10-full CZM(연구트랙) · 앵커대기(Joule ΔT·코팅√N·SDCP
E_bind·NCA175·Kang&Shin 1.51× magnitude).
