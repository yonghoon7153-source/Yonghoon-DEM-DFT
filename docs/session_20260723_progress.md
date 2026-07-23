# 진행 브리핑 — 2026-07-23 세션 (branch: claude/stoic-knuth-NObVQ)

이 세션에서 **기능 15 + 적대리뷰 5(전부 반영) + 리서치 2** 완료.  전부 커밋·푸시.
아래는 "어디까지 됐나 + 어떻게 보나 + 뭐가 남았나".

## 1. 이번 세션 산출 (커밋순)

### 인프라·뷰어
| 항목 | 내용 | 상태 |
|---|---|---|
| 자동화 ③ 등록 훅 | `webapp/mpm_lab_register.py` — V100 계산완료→db 등록(--dest/--url/--rsync), trust 배지.  라우트와 meta 공유 | ✅ (리뷰 F1/F2/F3 반영) |
| STEP4 승자 래치 | near-null-B AMG가 이기면 직행 → 저율 후막 ~15-34% 절감.  해 불변(전처리) | ✅ (리뷰 B2) |
| #4b 2D 단면 morphology | 뷰어 클릭→그 지점 초미세 복셀 슬라이스(좌:상 우:SE 그레인색) | ✅ (리뷰 정확 확인) |
| DEM 고유 노란 하이라이트 | 대시보드 지표표서 frame[5] DEM-only 강조 | ✅ (리뷰 정확 확인) |

### 열화 물리 (frame[5])
| 항목 | 내용 | 상태 |
|---|---|---|
| 취성→MPM crack-void | `dem_fracture_scaffold.py` + `mpm3d_compaction --fracture-scaffold` (fragmentation+ 게이트, ASSUMED-void) | ✅ (리뷰 M1/M2/L1/M3/L2/L3) |
| #30 VGCF carbon-촉매 SE분해 | STEP3 carbon-SE 계면면적 + STEP5 화학채널 SPLIT(이중계산 가드) | ✅ (kim2024/cho2024 앵커) |
| #31 PTFE 브릿지 열화 | ledger dcr_eff modifier (F1-style OFF, 앵커 없음) | ✅ |
| #29 Joule 발열 hot-spot | v1: q∝\|J\|²/σ 맵(어디서 발열)·뷰어 jt_field / v2: 끝점-보존 재분배기(Eₐ-free) | ✅ (리뷰 #3/5/7) |

### #28 periodic
STEP3 σ-solve(전자/이온/열/pore/반응) + STEP5 ledger 주기이미지 (`--periodic`).  ✅ (리뷰 B1)

### #33 v3 (ML·이종기술)
| 항목 | 내용 | 상태 |
|---|---|---|
| litdb 적용표 | `litdb_application_table.md` — 65장→적용상태→gap→v3 후보 | ✅ |
| 코팅 프리셋 셀렉터 | `coating_presets.py`(none/LNO/LZO/…) + STEP5 배선 + `/step5` 드롭다운 UI | ✅ (리뷰 #4) |
| ML 설계 폐루프 | `ml_design_loop.py` — Sobol DOE(검증) + scalarize + SISSO/BO(WSL 스캐폴드) | ✅ (리뷰 #1/2) |

### 리서치
- **Eₐ 문헌조사**: LPSCl 분해-율 Arrhenius Eₐ = **문헌 부재**(전도/계면 Eₐ는 틀린 양) → 날조 회피.
  자기발열은 유의(~5-30K, Ayyaswamy AEM2026) → Joule v2 = 재분배기(Eₐ 불요).
- **litdb 적용표**: STEP1-3 코어 전부 적용·교차검증; 미적용 top = Duquesnoy ML 루프·코팅 프리셋·화학/kinetics 축.

## 2. 파이프라인 현재 상태

- **STEP1 DEM**: E_eff=1.35 압밀, Furnas dip ✅  **STEP2 MPM**: J2 챔피언 E=1.53/ν0.49/σ_y0.30, 스캐폴드 ✅
- **STEP3 voxel Kirchhoff**: σ_e/σ_ion/**σ_thermal(κ)**/pore-τ + **carbon-SE 계면** + **Joule hot-spot** + **periodic** ✅
- **STEP4-v2**: 비선형 BV+구형확산, CCCV, per-particle D_s, R_int 직렬, **near-null-B AMG 래치** ✅
- **STEP5**: R_int(N) 분해(접촉 ledger + 화학 CEI + OTHER) + **carbon-촉매 SPLIT** + **코팅 프리셋** + **Joule 재분배** ✅
- **webapp**: /step5 코팅 셀렉터, 뷰어 🔬morphology·🔥Joule·⚡σ필드, DEM 하이라이트, 등록훅, trust 배지
- **ML**: predictor_engine(GPR+RF Phase1-2) + ml_design_loop(Sobol 검증·SISSO/BO WSL)

## 3. 어떻게 보나
- 코드 브랜치 = **`claude/stoic-knuth-NObVQ`** (worktree `/home/yonghoon/dem-web`).  데이터는 `~/Yonghoon-DEM-DFT/webapp/*` → `WEBAPP_*_FOLDER`로 연결.  실행 = `~/run_dem5002.sh` (git pull+데이터+5002).
- V100 = 킷 최신(mpm_input_from_case 산출), run 스크립트 auto-git-pull → 최신 코드로 실행.

## 4. 남은 것 (전부 문서화)
- **WSL 전용**: ML 루프 실학습(sklearn/pysisso/skopt)·MPM viscoelastic(taichi)·#5 PDF digitize.
- **앵커 대기(날조 금지)**: Joule 절대 ΔT(Ayyaswamy PDF)·코팅 √N shape(≥4 N점)·SDCP E_bind(DFT)·NCA E=175·LZO/Li₃PO₄ 코팅 배수.
- **후속 구조 훅**: 코팅 (b)계면전도 `--coat-sigma-b`·(c)So2022 core-shell seeding·ML objective↔predictor 배선.
- **연구트랙**: D1 yield-cap 접촉(So2021/2022)·M13 viscoelastic·B 대조연구.
