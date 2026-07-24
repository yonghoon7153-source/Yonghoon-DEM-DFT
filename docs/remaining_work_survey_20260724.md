# 남은 작업 종합 서베이 (2026-07-24, 5-스캐너 워크플로 wf_17cb6734)

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

## C) 실험·문헌 앵커 대기 (§F1 날조금지 — 훅만)
- Joule ΔT(Ayyaswamy) · 코팅 √N-shape+배수(LNO/LZO만 실효) · SDCP E_bind DFT(gabia, A4′ 유일잔여)
- NCA E=175 출처검증+K_IC · EIS C_dl/R_w/D_s/i0 pristine 앵커 · D5 R분배·C_dl(N)·D_s(N)
- R_int(N)/fade(N) 실험곡선(#5 PDF digitize) · A11 pristine R_int 정밀 · STEP4 x100/OCP 실측
- F1 SuperP/PTFE 압력형상 · Kang&Shin 1.51× 재해석 · C3 κ phantom bib→실ref

## D) 연구트랙 (큰 설계)
- **porosity 관계식 도출** (E_SE-강성+조성 항, Heckel; ~20%=rigid floor, Varkey 교차검증) — ★사용자 명시목표
- D1 real E_SE=24 + Thornton-Ning p_y 캡으로 18× softening 제거 (dem3d_plastic.py 테스트베드, V100 캠페인)
- B4 multi-contact(Varkey) vs 18× softening 비교 · B6 operating-P σ-degradation 시간축
