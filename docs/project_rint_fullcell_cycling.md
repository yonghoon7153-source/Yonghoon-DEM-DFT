# PROJECT — 집전체 계면저항(R_int) + 측정-앵커 풀셀/사이클 모델 확장

정의일 2026-07-20.  ★ 큰 프로젝트 (다중 코드리뷰 + 코드생성 + 데이터취합 + 단계진행).
이 문서 = 정본 스코프.  세션 넘어가도 이거 먼저 읽고 이어간다.

## 0. 배경 / 왜 (발단)
STEP4 방전/충전이 현재 **R_int=0 (전극-내부, 이상접촉)** 로 돎.  webapp 집전체 선택(bare Al,
R_int 110/46)은 **STEP3 σ_apparent 에만** 반영되고 **STEP4 로 안 흘러감**(미연결 = 버그 아님, 미포함).
사용자 지적 → 정직 규명 결과:
- 우리 기존 결론 **전부 유효**: σ_e +52%, 방전 +8.5mV, z-profile, 손실분해 = **전극-내부/구조 축, R_int 무관.**
- R_int 의 **기하 몫 = R_geom = 우리 모델 OUTPUT** (SBE 1.37e-5 / DBE 9.05e-6 Ω·cm², 아주 작음).
- **측정 R_int (사이클후 110/46/30, pristine ~18/12/10) = 화학(interphase)+열화(접촉손실·크랙) 지배**
  → R_geom 보다 ~7자리 큼 → 우리 BOL 기하-수송 모델 **범위 밖 = 측정 INPUT.**
- 즉 "R_int output이어야?" (사용자) → **기하는 output(R_geom), 화학/열화는 측정 input** 이 정답.
- 풀셀(집전체 포함) 축 + cycling 열화는 **별도 트랙으로 정식화** 필요.

## 1. 목표
전극-내부(현재, R_int=0)는 유지하고 → **집전체 계면저항 R_int 을 측정-앵커된 명시적 "풀셀 축"** 으로
추가.  이후 **pristine↔cycled 분리(A11)** → **cycling 열화(A10)** → **cycling profile ML(5-phase P3)** 확장.

## 2. 대원칙 (§F1 정직 — 절대 위반 금지)
1. **예측 가능한 것(기하 R_geom) = 모델 OUTPUT.**
2. **예측 불가(화학/열화 R_int) = 측정 앵커 DB** — 실측/출판값만, **보간·눈대중·날조 금지.**
3. **전극-내부(R_int=0) 와 풀셀(R_int>0) 을 둘 다 명시 제공** — 어느 축인지 항상 라벨 (혼동 방지).
4. R_geom(output) 과 측정 R_int(input) 의 **갭 = "모델이 여기까진 안 다룬다"를 정직하게 노출.**

## 3. 단계 (Phase)
- **Phase 0 (NOW) — 데이터/물리 앵커 조사**: R_int(pristine/cycled)·EIS(R_ion/R_int/R_w)·사이클
  열화·전위 profile 의 **오픈소스 데이터셋 + 문헌 + DB-화 도구/온톨로지** 조사 → 앵커 DB 후보 정리.
- **Phase 1 — 앵커 DB + STEP4 --r-int 명시 배선**: 측정 R_int DB(전극×집전체×pristine/cycled) 구축
  + step4_dyn `--r-int` 를 킷/webapp에 **명시 옵션**으로(전극-내부=0 기본 유지) + R_geom output 검증.
  → **코드리뷰 ×다중 (물리+수치+통합).**
- **Phase 2 — 풀셀 실험 (DBE@C-SUS 포함)**: SBE/DBE/C-SUS × pristine/cycled R_int × 2C →
  panel c(신선 근접)+d/e(노화 벌어짐) 우리 버전 재현 + 문서.
- **Phase 3 — cycling 열화 + ML (장기)**: A10(cycle chemo-mech: 부피변화+CZM) 물리모델 →
  cycling profile trajectory → ML surrogate.  또는 BOL지표→cycling견고성 예측기(랩 데이터 앵커).

## 4. 코드리뷰 규약
각 코드 Phase 마다 **다중 리뷰** (최소: ① 물리 정합, ② 수치/수렴, ③ 통합/회귀).  ultracode 워크플로로
병렬 리뷰 + 적대검증.

## 5. 로드맵 연결 (기존 backlog)
- **A11** (pristine↔cycled R_int + 조성-연속) = Phase 1 핵심.
- **A10** (사이클 chemo-mech, 부피변화+CZM) = Phase 3.
- **B6** (사이클-Warburg 시그니처) = Phase 3.
- **5-phase Phase 3** (전-메트릭 ML) + cycling 견고성 타겟 = Phase 3.

## 6. 캐비엇 (지금 상태 정직)
- 현재 모든 STEP4 방전/충전 = **전극-내부(R_int=0)** — 유효하나 **풀셀 아님.**
- 측정 R_int(110/46/30)은 **사이클후** 값 → BOL 전극에 넣으면 "신선전극+노화접촉" 감도(진짜 노화 아님).
- 진짜 노화(전극 구조 열화)는 A10 필요.  지금 할 수 있는 건 **접촉저항 축(--r-int, 측정앵커)** 까지.

### ★ 6.1 지금 발견된 핵심 불일치 (사용자 지적 2026-07-20 — Phase 1 정조준)
**현재 STEP3 σ_apparent 는 "BOL 벌크(신선) + 사이클후 R_int(열화)" 를 섞어 씀 = 시간축 MIX (불일치).**
- 사실: σ_apparent 시나리오 = SBE 6.59e-5(R_int **110**) / DBE 1.58e-4(**46**) / C-SUS 2.42e-4(**30**)
  — 이 110/46/30 은 **전부 Fig6e 사이클후(열화)** 값인데, 우리 전극 구조(STEP3)는 **BOL(신선).**
- 즉 σ_apparent = fresh 벌크 + **aged 계면** → 물리적으로 두 시점을 섞음.  (manuscript 는 "사이클후 조건"
  라벨만 붙여둠 7f52c67 — 정직 표기이나 **분리 fix 안 됨.**)
- ⚠ 단 **헤드라인엔 무영향**: σ_e_eff/σ_ion_eff(벌크)·z-profile·방전(+8.5mV) 은 **R_int 무관** = 안 섞임.
  오직 **σ_apparent(2차 지표)만** 이 MIX.
- **★ FIX (Phase 1 = A11)**: BOL σ_apparent 엔 **pristine R_int(~18/12/10, panel e — 디지타이즈 필요)**
  써서 "fresh+fresh" 일관화 + **post-cycling(110/46/30)은 별도 "노화 시나리오"** 로 라벨 분리.
  → **두 개의 시간-일관 세트**(pristine / cycled), 절대 섞지 않음.  이게 이 프로젝트가 존재하는 이유.

## 7. 진행 로그
- 2026-07-20: 프로젝트 정의.  Phase 0 (앵커 조사) 착수 → 완료(`rint_anchor_db_research.md`).
- 2026-07-20: R_int(N) reference 설계(`rint_reference_growthlaw_design.md`, 3-에이전트 + defense 수정).
- 2026-07-21: **Phase 1 배선 (킷+webapp+σ_apparent 분리) 완료** — ① `docs/data/rint_eis_anchors.csv`
  (kim2025 pdf_verified + snippet 앵커 + user-lab 시나리오 키 sbe/dbe/csus × pristine/cycled)
  ② `mpm_input_from_case.py --step4-r-int` (기본 None=전극-내부 R_int=0 유지; 설정 시 방전·충전 양쪽에
  `--r-int-ohm-cm2` 주입 + 산출물 `_rint<값>` 태그 + `MPM_S4_RINT` env override + 음수 거부 가드)
  ③ webapp `&s4rint=` URL 파라미터(파워유저, s4x100 문법) ④ **A11-③**: payload collector에
  `sigma_apparent_pristine_S_cm`(18/12/10, panel_e_approx) 병기 = §6.1 시간축 분리(cycled 세트는
  "fresh+aged 민감도" 라벨) ⑤ 렌더/bash-n 검증 + 적대 리뷰(CONFIRMED 2건 즉시 수정: 진행로그
  과주장·음수 가드).  **잔여**: R_geom output 검증(리뷰 항목), pristine 정밀 디지타이즈(A11-①),
  R_int(cycle) 열화율 축(A11-②).
- 2026-07-21: **Phase 2 첫 데이터 진행중** — DBE 2C CCCV: R_int=0 완료(89.6%) + **R_int=10(pristine
  C-SUS, panel-e 근사) V100 실행중** (같은 침대 grid 재사용, step4_only).  aged 30은 후속 스윕.
