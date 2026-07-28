# 랩 주간보고 digest (2026-07-27) — 양수영 ML DB화 + 윤태영 바이모달 ↔ 우리 구현 대조

기계-판독 정본: `docs/data/lab_weekly_reports_db.json` (facts + applicability 구조화).
이 문서는 사람용 요약 + 판정 근거.  (논문 카드는 litdb 정본 브랜치 소관 — 주간보고는 여기.)

---

## 1. 양수영 — ML 부분 (한계돌파 TabPFN) ★유심히

**한 일**: 구조체 P2D 합성데이터 ~1,300개로 리튬 전착량(내부/외부) 예측.
feature 3개(기공도·이온전도도·교환전류밀도).  **TabPFN**(Nature 2025, 637, 319–326 —
사전학습 tabular foundation model, 소규모 데이터 특화, sklearn 식 API·GPU)이 Group-CV 에서
**R² 0.9996 / RMSE 0.00476** 로 XGBoost(0.9883)·ExtraTrees(0.9865)·RF(0.9775)·Ridge(0.8204)
전부 제침.  최종 최적화는 Ensemble(ET+GB)로 후보 예측 → TabPFN 으로 데이터 확장 생성해
"내부 전착량↑·외부 전착량↓" 목표치 근처 후보 발굴.

**우리 규율과의 정합**: Group-CV(=우리 LOCO/LOOCV) 사용 ✓, Ridge 선형기준 병기 ✓ — 방법론
위생이 우리와 같은 결.

**적용 판정 (3단)**:
1. **[즉시·MED] ceiling-probe** — WSL 에서 TabPFN 을 우리 σ_ionic/σ_e/κ corpus(n=88–100,
   TabPFN 적정 구간)에 돌려 physics-폼 LOOCV(0.975/0.953/0.90)와 비교.
   *크게 이기면* = 폼이 놓친 물리 신호 존재, *비슷하면* = "폼=정보한계" 주장의 독립 보강.
   폼을 대체하는 게 아니라 **천장 측정기**로 쓴다 (우리 제품은 physics-locked 폼).
2. **[후보·WSL] step6 위원회 멤버/대안** — SkCommittee(GBR) 자리에 TabPFNRegressor.
   예측분포가 내장이라 UQ 가 자연스러움.  torch+GPU 의존 → opt-in (env_db optional 등록).
3. **[후보] webapp predictor(GPR/RF) 라인업 추가** — sklearn 호환이라 import-guard 그대로.

**⚠ 주의 2건 (그들 결과 과대이식 금지)**:
- R² 0.9996 은 3-feature·매끈한 P2D 함수라서 나온 숫자 — 우리 corpus(고차원·per-seed 노이즈)
  에 그대로 기대할 값 아님.
- "모든 점 = ML 이 만들어낸 데이터"로 최적화 = 앵커 검증 없는 생성-데이터 외삽.  우리 step6 의
  σ-gate → ANCHOR(실솔버) 규율이 정확히 그 보완 — 이 부분은 우리가 앞서 있고, 협업 시
  공유할 가치가 있는 규율.

방사형 양극재 파트(COMSOL 315모델 자동화)는 **입자-내부 스케일 = 우리 파이프라인 밖**
(우리는 입자를 균질 구로 취급).  그들 (D50·AR·단축)→(stress·damage·capacity) 데이터가 쌓이면
우리 per-particle D_s_eff·i0_eff·취성 파라미터의 입자-내부 근거로 업스케일 — 대기 훅.

---

## 2. 윤태영 — 바이모달 부분 ↔ 우리 구현 대조 ★전체 확인

### 2-1. Bimodal COMSOL (P:S 스윕, 8 mAh/cm², AM:SE 80:18) — ⚠ PROVENANCE 정정 (2026-07-28)

**★정정 (사용자 확인 2026-07-28)**: 그들 geometry 의 porosity(22.80/18.64/17.30/15.50/
19.03%)는 **우리가 제공한 값 — 우리 면용량 6 mAh/cm² MPM 데이터**다.  초판의 "독립 도구가
같은 바이모달 패킹 시그니처 → frame[4] 교차검증 성립" 서술은 **순환이므로 철회**: 그들 표의
7:3 최소·양끝 반등은 우리 데이터가 그대로 반사된 것이지 독립 재현이 아니다.  우측 비교열도
재라벨 필요 — `porosity_production_final.csv` @AM 80wt% 행은 source=**MPM** 이므로 이 표는
"그들 COMSOL vs 우리 DEM"이 아니라 **우리 MPM(6mAh 제공분) vs 우리 MPM production 테이블
(80wt 슬라이스)** 의 내부 정합성 점검이었다 (7:3 최소 15.50↔15.1 근접 = 우리 자체 테이블의
조성-슬라이스 일관성일 뿐, 외부 검증 정보량 0).

| P:S | 그들 COMSOL 입력 (=우리 6mAh MPM 제공) | 우리 production 테이블 @80wt (source=MPM) |
|---|---|---|
| 0:10 | 22.80% | 17.6% |
| 3:7 | 18.64% | 15.5% |
| 5:5 | 17.30% | 15.8% |
| 7:3 | 15.50% (최소) | 15.1% (최소) |
| 10:0 | 19.03% (반등) | 16.8% (반등) |

**살아남는 비교 축 (기하 입력 공유 → "same-input 솔버 패리티", frame[4] 아님)**: 그들 COMSOL
**전기화학 출력** vs 우리 STEP4.  "10:0 과전압 최대(조기 4.3V)·top(분리막측) 전류 집중" =
우리 mono-large σ↓ · je z-프로파일 쏠림과 방향 일치 — 같은 미세구조 입력을 받은 두 전기화학
솔버가 같은 방향을 내는 것으로, PyBaMM 패리티(#5)와 같은 부류의 **수치 패리티** 증거다.
다음주 Top/Bottom 전류분포·V-프로파일 수치를 받으면 STEP4 동일-P:S **패리티 런** 가치 있음.
이 파트의 진짜 frame[4](실험 독립앵커)는 §2-3 실셀 실측(율특성 0.33C→2C 53% 등)이 담당.

### 2-2. PC vs SC 파라미터 정리 ↔ 우리 sc_poly 프리셋 — **핵심 4/7 일치, 값 변경 불필요**

| 그들 정리 (p16) | 우리 구현 | 판정 |
|---|---|---|
| **i0: 고체계에선 PC 도 SC 와 같은 진짜 i0** (액체 침투 아티팩트) | `i0_split=none` (41건 적대검증서 "정량 부재 → 공유 --i0 유지") | ✅ **독립 경로로 같은 결론** (우리=부재 논거, 그들=아티팩트 논거 — 상호 보강) |
| 벌크 D: PC>SC 는 액전 크랙-침투 아티팩트, 고유 kinetics 동일 | 앵커문서 "PC 1오더 빠름=균열-전해액 침투 기전 → ASSB 이식 금지" | ✅ 동일 인식 |
| (GB 로 poly **유효** 확산 느려짐 — brick-layer 균질화 예정) | τ=r²/D: poly (6µm)²/4e-15=**9,000s** vs SC (2µm)²/3e-15=**1,333s** → poly 6.8× 느림 | ✅ **방향 일치** — D 절대값(poly 4e-15 > SC 3e-15)은 반경 규약 차이일 뿐임을 프리셋 CSV 가 명기 |
| 사이클 후 PC 표면적 증가 없음 (SE 침투 불가) | A10 ledger `--poly-mode expand-void` 정정(2026-07-22): poly=입계 내부 void·**계면 유지** | ✅ **정확히 같은 물리** (우리 3각 리뷰가 먼저 도달했던 정정) |
| 기계 물성 양쪽 동일 | DEM/MPM AM 단일 E (140/175 GPa, P/S 분리 없음) | ✅ 동일 접근 |
| Cohesive zone | A10 Bucci CZM (AM-SE/SE-SE) | ✅ 보유 |
| **SOC 후반부 D 급락** | STEP4 = 상수 D_s (Chen2020 도 상수 규약) | ⚠ **GAP** — 문서화된 한계.  훅: `--d-s-table` (O'Regan 2022 D(sto) 가 프리셋 promotion_path 에 기존재) |
| **PC 이방성** (표면 Li-rich·코어 Li-poor) | 등방 구형 radial diffusion (x_surf↔x_mean 갭은 포착) | ⚠ **GAP** — grain 이방성은 입자-내부 스케일 (양수영 파트와 접점) |

**결론**: 바이모달 관련해 우리 구현은 **잘 적용돼 있음** — 그들 논문-공부 정리가 우리 기본값
(i0 공유·poly/SC D 프리셋·expand-void·CZM)을 바꾸라는 근거가 아니라 **확인해 주는** 내용.
GAP 2건(SOC-의존 D, grain 이방성)은 값싼 훅으로 백로그화 (아래).

### 2-3. 이종기술 실험 = 우리 앵커 피드
No.1/No.2/5:5/Poly-only 셀 계열이 곧 우리 EIS 아카이브(`260723_Poly_only_sym…` 그 계열)·
R_int 앵커·STEP4 rate 비교의 실측 짝.  **율특성 No.1_only: 0.33C≈190 → 2C≈100 mAh/g
(2C/0.33C≈53%)** — STEP4 2C 완주 결과와 대조할 정량 앵커.  roll-press 규격
(3 mAh/cm² = 0.0240g, 전극 ~50µm)은 우리 3.18 캠페인과 정합.

---

## 3. 이번에 추가된 훅 (백로그 반영)
- **[ML] TabPFN ceiling-probe** — WSL 반나절: 우리 3개 corpus 에 TabPFN vs physics-폼 LOOCV 대조.
- **[ML] step6 위원회 TabPFN 멤버** — torch/GPU opt-in (env_db optional 등록됨).
- **[물리] poly D_eff brick-layer GB 균질화 항** — sc_poly_preset promotion_path 추가.
- **[물리] D_s(SOC) 테이블 (`--d-s-table`)** — STEP4 v2.1, O'Regan 2022 경로.
- **[패리티] 윤태영 P:S V-프로파일 디지타이즈 → COMSOL↔STEP4 same-input 패리티 런**
  (기하 porosity=우리 6mAh MPM 제공 → frame[4] 아님, §2-1 정정 2026-07-28).
