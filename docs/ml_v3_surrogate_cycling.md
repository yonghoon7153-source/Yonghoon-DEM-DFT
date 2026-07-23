# v3-2/v3-3 — ML 사이클수명 surrogate + 오픈소스 cycling 인제스트 (MLIP식)

사용자 v3 비전: 비싼 STEP4 충방전+사이클 sim 을 **물리-유도 feature 로 예측**해 가속(MLIP식) + 오픈소스
cycling 데이터로 열화 FORM 앵커.  frame[5] payoff: 조성→**(DEM/MPM/STEP3 σ·τ·percolation·focus)**→성능
= "why" 가 있는 feature (남이 못 가진 축).

## v3-2 `scripts/ml_cycle_surrogate.py` — surrogate
- **3-층 feature**: 설계 13(조성·크기·압력·코팅·첨가제wt) + **물리 15(★차별: porosity·σ_e/ion/thermal·
  τ·coverage(Hertz/Tabor)·CN·f_perc·focus_e/ion·Holm면적·fracture·AM-SE접촉)** + cycle_N 1 = 29.
- **성장모델(ASSUMED-FORM, 계수=학습)**: `rint_growth(N)=R0·[1+a_sat(1−e^{−N/τ})+b√N]` (Kang&Shin 관측형,
  A11-② 양끝고정 정합) · `retention(N)=100·[1−q_lin N−q_sqrt√N−q_knee·(N−n_knee)+]`.
- **surrogate**: `CycleSurrogate` GPR(불확실성)+RF(비선형) 앙상블(predictor_engine 규약) → 타깃 예측.
  `predict_cycle_curve()` = 설계→R_int(N)·retention(N) 곡선.  실학습=sklearn(WSL, import-guard).
- **타깃 provenance(§F1)**: model(STEP3/STEP4 산출) vs exp-anchored(R_int 절대·C_dl·fade율).
- **결측 정직**: 없는 feature 는 nan(0 으로 날조 금지) → surrogate 가 median-impute(라벨).

## v3-3 `scripts/cycling_data_ingest.py` — 오픈소스 cycling + §F1 게이트
★핵심 정직: 공개 cycling 은 대부분 **liquid Li-ion**(기전 다름) → **FORM/METHOD 는 전이, ABSOLUTE 는
matching-chemistry(sulfide-ASSB)에만**.  liquid 로 학습해 "sulfide 다" = §F1 위반 → `provenance_gate()`
가 chemistry 태그로 강제.
- `ingest_csv()` — cycling CSV → 정본 스키마(cycle/capacity/CE/R_int) + 자동 헤더추정 + provenance.
- `fit_fade_form()`/`fit_rint_form()` — 성장모델 계수 적합, **liquid 는 form_only=True 라벨**(모양만).
- **레지스트리**(provenance): Severson-MIT(LFP, METHOD·대용량통계) · NASA-PCoE(NMC, R_int FORM) ·
  Stanford-Attia(CLO, 우리 설계루프 원형) · Oxford(LLI/LAM·ICA METHOD) · **★sulfide-ASSB(유일 ABSOLUTE
  앵커, 희소 → WSL digitize #5)**.

## MLIP 비유 + 캐비엇(정직)
비싼 파이프라인(=DFT 격) → surrogate(=MLIP) → 값싼 역설계·대규모 스윕.  단 surrogate 는 흉내내는
파이프라인보다 정확할 수 없음(정확도 상속) — **오픈소스 실측이 파이프라인을 *넘어서는* 지점**(ASSUMED-FORM
사이클 shape 를 실측으로 앵커).  ★C_dl·fade 절대율·R_int(N) 절대는 sulfide 실험 앵커 대기.

## 실행 (WSL 실학습)
```bash
python3 scripts/ml_cycle_surrogate.py --selftest         # 구조·feature·성장모델(cloud)
python3 scripts/cycling_data_ingest.py --selftest        # 게이트·인제스트·FORM 적합(cloud)
python3 scripts/cycling_data_ingest.py --csv cyc.csv --chemistry sulfide_assb   # 실데이터
pip install scikit-learn joblib                          # WSL: surrogate 실학습
python scripts/train_cycle_surrogate.py --results webapp/results --out models/cycle_surrogate
# → corpus 로드 → 설계knob+물리feature 조립 → CycleSurrogate.fit(per-target 누출가드) → joblib+리포트
```

## ★ WSL 학습 파이프라인 (`scripts/train_cycle_surrogate.py`) — BUILT (2026-07-24)
corpus(results/<case>/*metrics.json) → `design_from_metrics`(설계knob) + `assemble_features`(물리 15) +
`targets_from_metrics`(σ-triad 상시·R_int/retention 사이클런만) → `build_matrix`(X[n,29]·Y, 결측 nan §F1) →
`train_and_save`(CycleSurrogate.fit → joblib + train_report.json).  sklearn/joblib **import-guard**(클라우드
graceful, WSL 실학습).  selftest: mock corpus 30 → X(30,29)·σ_e 30·R_int 15·retention 0(미배선 nan).
★per-target **누출가드**(물리타깃=설계knob만·파생타깃=자기제외) = 2단 surrogate(설계→물리→성능).

## 잔여 (v3 후속)
- **실학습 실행**(WSL): 위 스크립트를 실 corpus 로 → CycleSurrogate 계수·CV R².
- **오픈소스 실다운로드**(WSL): Severson/NASA CSV → fit_fade/rint_form(FORM 앵커).
- **폐루프 배선**: ml_design_loop(Sobol/SISSO/BO) ↔ CycleSurrogate ↔ predictor_engine → 역설계.
- webapp /predictor 에 사이클곡선 예측 패널 · EIS(v3-1) 소자를 surrogate 타깃에 추가.
- SISSO 로 R_int(N)·fade 기호식 자동발견(frame[4] 독립확인).
