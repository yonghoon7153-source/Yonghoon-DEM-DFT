# 랩 ML 파이프라인(TabPFN)과 우리 캠페인의 접점 — 2026-07-28

> 출처: 주간보고 PPT 2026.07.27 (Battery Materials Laboratory, 14p).
> 목적: PPT의 ML 접근을 우리 DFT/DEM repo에 이식할 수 있는 지점 정리.

## 0. PPT 요약 (팩트)

**Part 1 — (L&F) 방사형 양극재 미세구조 최적화**
- 파라미터: D50, seed 영역 직경(D_core), seed 입자 직경(D_seed), 방사형 두께(D_shell),
  방사형 입자 단축 폭(W), 종횡비(AR), 내부 기공 위치.
- COMSOL 2D 전기화학–기계 결합: 배향/von Mises/Li 농도/Damage 필드,
  성능지표 = 활물질 농도차·CC용량·스트레스 평균·데미지 평균 (전체/seed/radial 분해).
- **자체 웹앱 파이프라인 5단계**: 실험설계 → 형상 검수 → COMSOL 계산 → 결과 확인 → 머신러닝.
  RandomSeed 후보 생성, AI로 COMSOL 자동화 — **315개 모델** 확보 (대시보드: 139 처리,
  123 성공, 재시도 16, 18 h). 현재는 3D 산점도(D50×AR×ShortAxis → stress/용량) 육안 탐색,
  "추후 데이터 기반 머신러닝 시행 예정".

**Part 2 — 머신러닝 기반 교호작용 평가 (한계돌파)**
- **TabPFN** (Nature 2025, 637, 319–326) 도입. 구조체(scaffold) P2D 데이터 ~1300개,
  타깃 = 구조체 내 리튬 전착량, features = 기공도·이온전도도·교환전류밀도.
- 모델 비교 (Group-CV): **TabPFN R² 0.9996** > XGBoost 0.9883 > Extra Trees 0.9865
  > Ensemble 0.9855 > GB 0.9803 > RF 0.9775 > Ridge 0.8204.
- **TabPFN 기반 최적화**: ML로 가상 후보를 대량 생성 → (내부 전착량↑, 외부 전착량↓)
  목표 근처 데이터 발굴 (Pareto 탐색).

## 0.5 ML 파트 심층 판독 (10–13p) — 방법론 관찰

> TabPFN 원전은 **우리 litdb에 이미 다이제스트 있음**: hollmann2025_tabpfn_tabular_foundation_model.md
> (합성 prior ~1억 데이터셋 사전학습, 경사하강 없는 단일 forward pass ICL, ≤10k행/500특징,
> 외삽 취약·블랙박스 한계 명시). 아래 관찰은 PPT 표·코드와 그 다이제스트의 대조다.

1. **왜 TabPFN이 이기나**: 사전학습된 "베이지안 사후예측 근사"라 소표본에서 튜닝 없이
   강하다 — n=1300은 정확히 스윗스팟. Ridge 0.8204 → TabPFN 0.9996 갭은 타깃(전착량)이
   feature에 대해 **강하게 비선형**이라는 뜻이기도 하다 (선형 기준선이 18%p나 뒤짐 =
   교호작용/비선형이 실재한다는 간접 증거 — 발표 논리로 쓸 수 있는 포인트).
2. **용도 분리가 눈에 띈다** (11p 표): TabPFN·XGBoost는 "Group-CV 비교 전용",
   최종 후보 예측·최적화는 **Extra Trees + G 앙상블**. 합리적 추정: 수만 개 가상 후보
   스코어링엔 TabPFN 추론이 비싸고, sklearn 앙상블이 파이프라인 통합에 유리.
   → 시사점: **정확도 벤치 = TabPFN / 대량 스코어링 = 경량 모델** 이원화가 실용 패턴.
3. **Group-CV를 쓴 것은 올바른 관행** — 같은 형상(seed)에서 파생된 행들이 train/test에
   섞이면 누수. **우리 쪽 대응 구멍 발견**: codoping pair 모델(1081쌍)에서 같은 도펀트를
   공유하는 쌍(A–B, A–C)은 독립이 아니다 → 우리 CV도 **leave-one-dopant-out**으로
   올려야 정직 (현행 v2는 pair 단위 — 개선 항목으로 등록).
4. **R² 0.9996의 성격**: 결정론 P2D 시뮬레이터 출력의 보간 — 노이즈 없는 함수 근사라
   가능한 수치다. 코드(10p)가 `train_test_split(random_state=42)` 단일 분할 + 표는
   Group-CV로 이원화돼 있는데, 대외 보고엔 Group-CV 수치만 쓰는 게 안전.
5. **역설계(13p)의 통계 함정 = winner's curse**: ML이 생성한 가상 후보에서 목표 근처
   점을 고르는 것은 예측오차의 꼬리를 선택하는 행위다. 완화책 3종 — (a) 앙상블
   분산/TabPFN 분포출력으로 불확실성 페널티, (b) 상위 후보의 시뮬레이터 재검증 의무
   (랩이 이미 의도), (c) 정식으로는 acquisition function(EI) = Bayesian Optimization.
   PPT 스스로 "모든 점 = 머신러닝이 만들어낸 데이터"라 명시한 건 좋은 규율.
6. **제목이 '교호작용 평가'인데 현재 산출은 정합도까지** — TabPFN/GBM은 예측은 하지만
   교호작용을 *보여주진* 않는다(블랙박스). 다음 스텝 제안거리: **XGBoost TreeSHAP
   interaction values**(정확 계산 가능) 또는 H-statistic으로 (기공도×교환전류밀도) 같은
   쌍별 교호작용 지도를 뽑으면 제목값을 하게 됨. 우리 codoping의 명시적 곱항 접근과
   상보 — 우리는 해석 가능하지만 손으로 골라야 하고, SHAP은 자동이지만 사후 해석.

## 1. 핵심 관찰 — 파이프라인이 우리 cascade와 동형이다

```
랩:  실험설계(형상 파라미터) → COMSOL 자동화 → 315~1300개 테이블 → TabPFN → 역설계
우리: 도펀트/조성 설계        → UMA cascade    → 47~1081행 테이블   → ridge  → 가설 랭킹
```
차이는 두 가지뿐: ① 시뮬레이터(COMSOL ↔ UMA/DFT) ② 회귀 엔진(TabPFN ↔ numpy ridge).
**우리 데이터 전부가 TabPFN 스윗스팟 체급**(<10k 행, <100 특징, 수치형)이다.

## 2. 우리 쪽 적용처 (우선순위순)

### A1. codoping ML v2의 회귀 엔진 업그레이드 (즉시 가능, 로컬 GPU)
- 현행: numpy ridge (웹앱 무의존성 때문). 단일도펀트 score 회귀 R² 0.9998은
  score가 5성분 선형합성이라 자명 — ridge로 충분했다.
- TabPFN이 값을 낼 곳은 **비선형 타깃**: champions의 rerank_de_post_anneal,
  litransport bvs proxy(농도 3점), ESW window를 조성·물성 특징에서 직접 예측 —
  명시적 곱항 없이 교호작용을 자동 포착. 우리 명시적 교호작용항(해석 가능)과
  상보적: **TabPFN = 예측력, ridge+곱항 = 해석**. 둘 다 보고하는 게 정직한 구성.
- 실행처: 로컬(WSL/kgy) GPU에서 tabpfn 실행 → 결과 CSV를 db/properties/에 등록.
  웹앱은 numpy-only 유지 (의존성 오염 금지).

### A2. TabPFN 역설계 — PPT 13p 방식 이식 (co-doping 다음 라운드)
- PPT의 "가상 후보 대량 생성 → 목표 근처 발굴"을 co-doping에 그대로:
  1081쌍 + 가상 농도축(x 0.02–0.10 연속) 후보를 TabPFN으로 스코어링 →
  (window↑, transport 유지, cost↓) Pareto 전단 → **상위 후보만 UMA 공동치환
  슈퍼셀 검증** = 검증 라벨 생산 루프. codoping_ml_v2_meta의 "검증 경로" 실행판.
- ⚠ 규율: ML이 생성한 점은 전부 가설 — PPT 13p도 "모든 점 = 머신러닝이 만든
  데이터"라 명시함. 우리도 NOT-validated 태그 유지.

### A3. disorder ensemble 서러게이트 (데이터 쌓인 뒤)
- d×cfg×T → D 테이블이 커지면(현재 cfg 3개 — 아직 이르다), 배열 기술자
  (anti-site 분포·Ewald·BVS 채널%) → D 예측. cfg 추가 실행의 우선순위 결정
  (active learning)에 사용. Kim 2024(6-config) 확보 후 설계.

### A4. DEM 트랙 — 랩 파이프라인과 가장 직접 연결
- 랩의 COMSOL 자동화 = 우리 LIGGGHTS 파라미터 스윕과 동형. DEM 접촉/배위수/
  응력 지표 → 전도 프록시/기계 응답 서러게이트. litdb 앵커 이미 보유:
  duquesnoy2023(ML 다목적 제조 최적화), bazzoun2025(DEM 민감도).
- **P2D 연결(다음주 랩 계획과 접점)**: 후막 전고체 P2D의 입력 물성(σ, E, ESW)을
  우리 db가 공급 가능 — db/properties → P2D 파라미터 export 인터페이스가
  멀티스케일 연결고리. (단 σ 절대값은 MLIP 상한 — 실험/문헌 보정 명시 필수.)

### A5. 웹앱 반영 (가벼움)
- cascade ML 탭에 "TabPFN 결과" 섹션 슬롯(파일 존재 시 렌더, codoping_ml_v2와
  같은 graceful 패턴). 실행은 오프라인, 사이트는 결과만.

## 3. 정직성 체크 (우리 규율 적용)

1. **R² 0.9996의 정체**: 결정론 시뮬레이터(P2D) 출력의 보간이라 가능한 수치 —
   우리 cascade score 회귀 0.9998과 같은 성격. **시뮬레이터를 배운 것 ≠ 물리를
   배운 것.** 서러게이트는 보간용, 외삽엔 검증 라벨(UMA/DFT/실험) 필수.
2. **소표본 주의**: 47행 회귀는 어떤 엔진이든 과적합 위험 — LOOCV/GroupCV 유지,
   TabPFN도 예외 아님 (PPT도 Group-CV 사용 — 올바른 관행).
3. **TabPFN 제약**: ~10k 행·~100 특징·수치형 위주 — 우리 용례 전부 통과하나,
   범주형(group)은 인코딩 필요.
4. 교호작용 "평가"는 TabPFN 단독으론 안 나온다(블랙박스) — SHAP interaction
   또는 우리 명시적 곱항 병행이 해석 경로.

## 4. 추천 착수 순서
1. **A1** — codoping 비선형 타깃 TabPFN 벤치 (로컬 GPU, 반나절): ridge 대비
   LOOCV 성능표 확보 → 사이트 ML 탭에 병기.
2. **A2** — 역설계 루프 1회전: TabPFN 후보 → 상위 5쌍 UMA 공동치환 검증
   → 첫 실측 라벨 (mlip_next_campaigns ①과 합류).
3. **A4** — P2D 물성 export 인터페이스 (랩 P2D 데이터셋 일정과 동기화).
