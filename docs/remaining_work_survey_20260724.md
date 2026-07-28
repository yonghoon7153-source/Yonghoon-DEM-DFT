# 남은 작업 종합 서베이 (2026-07-24, 5-스캐너 워크플로 wf_17cb6734)

## ★ 진행상태 & 다음 픽 (2026-07-24, "나중에 하자" 재개점) ★
- **A-1 완료 4건** (커밋됨): ① network_conductivity dead-code 삭제 ② Predictor /train
  graceful 500 ③ ionic 라벨 "FORM X"→v12-clean v3(=v29/v32) 통일+식정정 ④ Predictor
  d_AM_S 슬라이더 오해방지 ⚠툴팁.
- **A-1 남은 quick-win** (재개 시 먼저): three.js 로컬 vendoring(M) · mpm-lab GIF Pillow
  폴백(S) · STEP4 I_1C 규약 문서화(S) · dump_case_summary 헬퍼(S) · paper 인용정정(S).
- **다음 큰 픽 후보 3** (사용자 선택 대기): ⓐ webapp 예측 패널 신설(EIS/DRT/ICA·사이클곡선
  예측 UI) · ⓑ 로드맵 Phase 2→4(데이터층→2D synth) · ⓒ porosity 관계식 도출(D, 사용자 명시목표).
- 나머지 A/B/C/D 전체 목록은 아래 그대로.  B=WSL·GPU 실행블록, C=앵커대기(§F1), D=연구트랙.

---


원시 ~110 → 병합 ~55.  완료분(v3 EIS/DRT/ICA 스위트·첨가제 감사·실행배치 스크립트) 제외.
카테고리: **A** 클라우드 do-now / **B** WSL·GPU 실행블록 / **C** 실험·문헌 앵커대기(§F1) / **D** 연구트랙.

## A) 지금 클라우드서 바로 (do-now) — 우선순위순
### A-1 즉효 정리·버그·UX (전부 S)
- network_conductivity.py 죽은 placeholder 루프(`for r in erecs[:10]: pass`) 삭제
- ionic scaling-law 플롯 라벨 통일 (FORM X v32 / v29_FINAL / v12-clean v3 = 한 수식)
- Predictor "Train Models" 버튼 graceful 500 (sklearn 부재 → JSON 안내, 현재 raw 500)
- mpm-lab GIF export Pillow 의존 처리(폴백) · mpm-lab three.js 로컬 vendoring(CDN→static, M)
- STEP4 I_1C 전류규약 문서화 · dump_case_summary.py 헬퍼 · paper-build 인용 정정
- Predictor d_AM_S 슬라이더 임시 라벨(현재 max(P,S) collapse → 소립 무효)
### A-2 후속훅 배선
- 코팅 계면전도 `--coat-sigma-b` · So2022 core-shell 배선 · ML 폐루프(objective↔surrogate↔predictor)
- webapp EIS/DRT/ICA + 사이클곡선 **예측 패널** 신설 (엔진 존재, UI만, M)
### A-3 로드맵 데이터층
- Phase 2: predictor load_training_data 에 grade/aux 파생타깃 (단일 벡터, M)
- Phase 4: extract_2d_microstructure targets-only 진입점 (예측 숫자→2D synth, M)
- A7 graded-z 2축 (z-band porosity + carbon:binder, M)
### A-4 σ-폼·검증 (문헌 TREND 앵커 채택)
- Bazzoun σ_eff,ion 절대앵커 채택 + B1 점대점 + σ-vs-P↔Heckel + B2 RNM vs Stage-E + B5 σ_grain 이중계상 재점검
- Bielefeld binder-blocking 폼 항 · E Reisacher carbon g_C 캘리브 · E Huang LBM σ_thermal 교차검증
- Schneider/Minnmann/B3 percolation-class 서술 · B7 localization 맵+민감도 히트맵 · SOC-EIS DRT 사이클분해
### A-5 접촉모델·구현
- MPM f_AM extractor(Love-Weber, DEM 재실행 불필요) · D2 Stage-E H 가변(Jackson-Green) · D4 A/B 검증(Storåkers)
- step3 σ_ion 망 v2(SE+SDCP) · step4_ac.py CPU 스캐폴드 selftest · porosity Yu-Standish wall-effect 예측기

## B) WSL·GPU 필요 (코드 준비됨)
- v3 ML 실학습(sklearn/pysisso/skopt) · Phase 3 predictor 전메트릭 학습
- STEP4 PyBaMM 패리티 런(#5, run_v100_pybamm_parity.sh 준비) · 완전 AC-solve 실런
- DBE 2C R_int={10} · σ_SDCP DBE-250/SBE step4 그리드 · A-1 Full MPM void→σ_e 캘리브
- σ_e_rel 재실런(--poly-mode expand-void) · A8 NCA σ_e 재보정 · A14 SWCNT 검증런
- 오픈소스 사이클데이터 실다운로드+변환 · EIS .mpr galvani 파싱 · A12 점탄성 binder(spring-back, 최대 gap)
- multi-seed sim outlier 해소 · resolved-grain MPM(가) GitHub 푸시
- ★ STEP4 near-null solve — 후막·첨가제 격자 [2026-07-26 진단; OOM은 commit 6394a01로 해결]:
  VGCF/PTFE 첨가 후막(4.44M dof, 119µm)은 e-ion BV 약결합 + σ_e 10⁴×대비(VGCF100/AM_S0.01)로
  선형계가 **율 무관 구조적 near-null**(λ~1e-11).  ⚠정정: 어제 "고율 무영향"은 **틀림** — 2C도
  near-null(GPU Jacobi-CG 발산 info=20000 → CPU 폴백).  **① OOM crash [해결됨, 6394a01]**: rtol=1e-9
  목표 도달불가 → 자기-바닥(rel~7e-9)이 매 솔브 near-null-B AMG 발동 → 대-coarse 빌드 OOM(Killed).
  게이트에 물리-충분 잔차바닥(_NN_ACCEPT_RTOL=1e-7, 노이즈바닥 1e-5의 100×아래) 추가 → 물리-정확 솔브
  통과.  게이트 단위테스트 + selftest PASS, **V100 2C 재실행 1회로 최종확인 대기**.  **② SPEED [남음·deferred]**:
  fix 후 2C는 CPU AMG로 완주(~시간대, OOM 아님)하나 GPU Jacobi-CG는 near-null 못 풀어 여전히 CPU.
  진짜 빠르게 = ⓐ GPU-AMG(AMGX/pyamgx, near-null deflation GPU서) or ⓑ near-null-B AMG 메모리 절감
  (coarse 레벨↓) or ⓒ 0.2C 등 극저율은 그리드 coarsen.  0.2C 크롤(11s/iter·3h/step·완주~143일)도
  ①로 near-null-B AMG 미발동되면 CPU AMG 자기-바닥 수용으로 개선 예상(검증 필요).  ★사용자 우선순위:
  지금 2C만, GPU-AMG 개발은 나중(V100 요금).  step4_dyn.py GPU 분기가 Jacobi 고정인 게 speed 근인.

## C) 실험·문헌 앵커 대기 (§F1 날조금지 — 훅만)
- Joule ΔT(Ayyaswamy) · 코팅 √N-shape+배수(LNO/LZO만 실효) · SDCP E_bind DFT(gabia, A4′ 유일잔여)
- NCA E=175 출처검증+K_IC · EIS C_dl/R_w/D_s/i0 pristine 앵커 · D5 R분배·C_dl(N)·D_s(N)
- R_int(N)/fade(N) 실험곡선(#5 PDF digitize) · A11 pristine R_int 정밀 · STEP4 x100/OCP 실측
- F1 SuperP/PTFE 압력형상 · Kang&Shin 1.51× 재해석 · C3 κ phantom bib→실ref

## D) 연구트랙 (큰 설계)
- **porosity 관계식 도출** (E_SE-강성+조성 항, Heckel; ~20%=rigid floor, Varkey 교차검증) — ★사용자 명시목표
- D1 real E_SE=24 + Thornton-Ning p_y 캡으로 18× softening 제거 (dem3d_plastic.py 테스트베드, V100 캠페인)
- B4 multi-contact(Varkey) vs 18× softening 비교 · B6 operating-P σ-degradation 시간축
- ★ 주간보고 훅 (2026-07-28, docs/lab_weekly_20260727_digest.md 정본): **TabPFN ceiling-probe**
  (WSL 반나절 — 우리 σ_ionic/σ_e/κ corpus 에 TabPFN vs physics-폼 LOOCV 대조; 크게 이기면 놓친
  물리, 비슷하면 폼=정보한계 보강.  env_db optional 등록됨) · step6 위원회 TabPFN 멤버(opt-in) ·
  poly D_eff brick-layer GB 균질화 항(sc_poly promotion_path) · D_s(SOC) 테이블 `--d-s-table`
  (O'Regan 2022) · 윤태영 bimodal P:S V-프로파일 디지타이즈 → COMSOL↔STEP4 same-input **패리티** 런
  (⚠기하 porosity=우리 6mAh MPM 제공값 — frame[4] 아님, digest §2-1 정정 2026-07-28).
  바이모달 대조 결론: i0 공유·expand-void·τ 방향·CZM·기계물성 **일치 확인**(값 변경 불필요),
  GAP=SOC-의존 D·grain 이방성(입자-내부 스케일).
