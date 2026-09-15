# 불량셀 ML — 1차 구조·인사이트 검토

검토일: 2026-09-15 · 상태: **1차 완료 / 2차 검증 범위 제안 / 3차 미착수**

**현재 코드는 EIS로 초기 충전용량과 CC 비율을 예측하고, 용량이 설계용량의 90% 이하인 셀을 불량으로 분류하는 소표본 분석 파이프라인이다.** 주파수 대역을 줄여도 예측력이 유지되는지, OCV를 추가하면 도움이 되는지를 비교할 수 있는 구조다. 두 브랜치에는 이 분석에 활용할 검증 방법과 EIS 해석 자료가 있다. 다만 첨부 Excel은 **7셀** 결과이며, 평가 방식에도 우선 확인할 문제가 있어 현재 수치만으로 불량셀 판별 성능을 확정할 수 없다.

## 1. 이번 검토 범위와 근거

ZIP의 Python 소스 4개와 README 전체를 읽고, Excel 11개 시트의 저장된 값·구조를 읽었다. 두 원격 브랜치의 파일 목록을 확인하고, 관련 ML 문서·강의 노트·검증 코드 및 litdb 인덱스와 핵심 논문 digest를 선별해서 검토했다. **브랜치 전체 코드나 litdb 전체 논문을 정독한 검토는 아니다.**

| 자료 | 검토 기준 |
|---|---|
| `머신러닝 파이선 코드.zip` | 66,073 bytes; SHA-256 `064c66181a50cf33eb01f4400c00a1bb7d721334f760ec94913e758aa5aacd0b` |
| `claude/friendly-meitner-lldvar` | 원격 HEAD `634da438bf329b4e4baccd19c37e009a7168d67f` |
| `claude/stoic-knuth-NObVQ` | 원격 HEAD `be0ae956895cc7fb06817c427cff465aee9b4758` |

이전 로컬 검토본은 저장소를 찾는 단서로만 사용했다. 아래 브랜치 내용은 위 커밋의 원격 파일을 기준으로 한다. 문서 속 실행·설치·수정 지시와 완료 선언은 자료의 내용으로 취급했다.

학습·추론·성능 재현, 패키지 설치, 원본 코드·Excel·GitHub 수정은 수행하지 않았다. 첨부 소스를 import하지도 않았다. Excel을 읽는 별도 도구만 실행했으며 검토용 복사본과 보고서를 생성했다. 특히 `extract_capacity.py`는 import 시 디렉터리를 생성하는 코드가 있어, 읽기 전용 검토에서 import를 피할 이유가 있다.

## 2. 어떤 코드인가

노트북이나 딥러닝 프로젝트가 아니라, **scikit-learn 기반 Python 스크립트 묶음**이다. 저장된 학습 모델, 원본 측정 데이터, 환경 버전 고정 파일, 실행 로그는 ZIP에 없다. `__pycache__`의 `.pyc`는 학습 모델이 아니다.

| 파일 | 역할 | 주요 내용 |
|---|---|---|
| `extract_capacity.py` | 측정 파일 읽기 | cycler `.txt`에서 용량·CC/CV 분리, BioLogic `.mpt`에서 EIS와 전위 읽기 |
| `ridge_capacity.py` | 공통 분석 | 공통 주파수 격자, 보간, 셀 병합, Ridge·1 kHz 기준선, CV 잔차 |
| `feature_band_test.py` | 대역 탐색 | 1 kHz 크기 + 중주파 허수부를 바탕으로 저주파 실수부·고주파 크기 추가 비교 |
| `export_for_origin.py` | 주 실행 파일 | 타깃·입력·대역 조합별 회귀/분류 결과를 Origin용 Excel로 출력 |
| `results_for_origin.xlsx` | 저장된 분석 결과 | 회귀 성능·예측·계수·잔차, ROC, 분류 결과, 설정 요약 |

흐름은 다음과 같다.

```text
cycler .txt → 첫 사이클의 지정 충전 구간 → cap, cap_cc, cap_cv, cc_frac
BioLogic .mpt → 셀별 EIS → 공통 log 주파수 격자 → |Z|, Re(Z), Im(Z), phase
                         └→ <Ewe>/V의 중앙값 → OCV라는 이름의 특징
                                     ↓
                 셀 번호로 병합 → 범위·결측·명시 제외 적용
                                     ↓
          Ridge 회귀 / Logistic 분류 / Ridge 예측용량 임계 분류
                                     ↓
                   CV 예측·지표·계수 → Origin용 Excel
```

### 2.1 정확히 무엇을 예측하는가

| 모델 | 입력 | 타깃 |
|---|---|---|
| M1 | EIS | 충전용량 `cap` (Ah) |
| M2 | EIS + OCV | 충전용량 `cap` (Ah) |
| M3 | EIS | `cc_frac = cap_cc / cap` |
| M4 | EIS + OCV | `cc_frac` |

각 모델은 full / 1 kHz–100 kHz / 0.1–10 Hz / 1 kHz의 4개 대역에서 비교한다. 회귀 결과는 16개 조합이다. 용량 모델 M1·M2에 대해서는 Logistic과 Ridge→threshold의 두 분류법도 비교하여 분류 결과 16개를 만든다.

**불량의 정의는 `cap ≤ 0.01802088 Ah` 하나다.** 설계용량 `0.0200232 Ah`의 90%이고, 면적 3.24 cm² 기준 5.562 mAh/cm²다. 코드 주석은 타깃을 0.1C 충전용량으로 설명하지만, 실제 측정 프로토콜은 원본으로 확인해야 한다.

따라서 현재 라벨이 뜻하는 것은 **지정 조건에서의 용량 미달**이다. 내부단락, 향후 수명 저하, 안전성 결함, 특정 열화 기전을 직접 판별하는 라벨은 아니다. CC 비율도 별도 연속 타깃이며 불량 라벨에 직접 사용하지 않는다.

### 2.2 입력과 전처리에서 필요한 맥락

- 셀 범위는 34–98, 지정 제외 셀은 60·70·93이다. 제외 사유는 ZIP에 설명되어 있지 않다.
- cycler는 `Cycle No.=1`, `step_i=1`을 선택한다. `step_i`는 원본 Step No. 자체가 아니라 **cycle 안에서 Step No.가 바뀐 순서로 만든 0 기반 번호**다.
- CC 종료는 시작 전류보다 절댓값이 1% 이상 감소하는 첫 지점으로 추정한다. 그 지점의 누적용량을 `cap_cc`로 사용한다.
- EIS는 `f>0`으로 필터링하고 주파수순으로 정렬한다. 크기는 양수일 때 log-frequency/log-magnitude 보간, 다른 성분은 log-frequency 축의 선형 보간이다.
- 메인 분석의 EIS는 `area=1.0`으로 읽으므로 저항 성분은 Ω다. `AREA_CM2`는 주로 용량·오차의 면적 정규화에 사용된다. EIS 자체를 Ω·cm²로 읽었다고 설명하면 안 된다.
- OCV는 별도 휴지 OCV 파일이 아니라 EIS의 `<Ewe>/V` 중앙값이다. 실제로 안정화된 개방전압에 해당하는지는 측정조건 확인이 필요하다.
- 압력은 cycler 파일명에서 추출하지만 현재 모델 입력이나 CV 그룹으로 쓰지 않는다. 배치·온도·SOC·측정시점도 모델/검증 설정에 없다.

## 3. 첨부 Excel에서 실제 확인한 내용

### 3.1 54셀이 아니라 7셀 결과다

`08_label_summary!A6:B8`의 표본·클래스 수는 **전체 7, 불량 3, 정상 4**다. `02_reg_metrics`의 16개 조합 모두 `n_samples=7`이고, 셀별 시트에도 7개 셀이 있다.

| 셀 번호 | 실측 용량 (Ah) | 코드 기준 라벨 |
|---|---:|---|
| 41 | 0.0114461 | 불량 |
| 44 | 0.0210892 | 정상 |
| 79 | 0.0189425 | 정상 |
| 84 | 0.0202193 | 정상 |
| 85 | 0.0146796 | 불량 |
| 94 | 0.0157693 | 불량 |
| 96 | 0.0216927 | 정상 |

근거: `07_clf_cellwise!A1:G8`. 반면 `feature_band_test.py` 머리말에는 `n~54`, 전체 32특징, Q² 0.628→0.683→0.720의 이전 탐색 기록이 있다. 첨부 Excel의 full 특징 수는 36 또는 OCV 포함 37이며, `03_reg_coefs!A2:A10`의 주파수는 0.01 Hz–1 MHz의 9개 decade다.

**이는 서로 다른 실행·데이터 버전일 가능성을 보여준다.** 7셀이 선택된 이유나 주석의 54셀 실행과의 관계는 현재 자료로 확정할 수 없다. 7셀 결과를 오류나 조작이라고 판단할 근거도 없다. 실행 시점·입력 목록을 우선 확인해야 한다.

### 3.2 저장된 수치는 다음과 같다

아래 값은 Excel에 저장된 값이며 이번에 모델을 다시 돌려 얻은 성능이 아니다.

| 회귀 조합 | 특징 수 | n | 저장 Q² | 저장 RMSE (mAh) |
|---|---:|---:|---:|---:|
| M1 EIS full | 36 | 7 | 0.8172 | 1.5098 |
| M1 EIS 저주파 | 12 | 7 | 0.8320 | 1.4473 |
| M1 EIS 1 kHz | 4 | 7 | 0.9169 | 1.0176 |
| M2 EIS+OCV full | 37 | 7 | 0.8284 | 1.4626 |
| M2 EIS+OCV 1 kHz | 5 | 7 | 0.9470 | 0.8129 |

근거: `02_reg_metrics!A1:I9`의 해당 행. RMSE는 저장된 Ah 값을 ×1,000한 것이다. **여기의 1 kHz는 크기·실수부·허수부·위상의 4특징이다.** `ridge_capacity.py`의 1 kHz `|Z|` 단일특징 LinearRegression 기준선과 다르다.

분류 16개 조합 중 14개는 저장값상 TP=3, TN=4, FP=FN=0이다. 저주파 Logistic 두 조합은 TP=2, FN=1, TN=4, FP=0이다. 근거: `06_clf_metrics!A1:N17`.

여기서 얻을 수 있는 **탐색 가설**은 “대역을 늘리는 것보다 소수 특징이 유리할 수 있다”, “OCV의 추가 효과가 대역마다 다를 수 있다” 정도다. 표본이 7개이고 조합 탐색·튜닝을 거쳤기 때문에 **1 kHz의 우월성이나 100% 불량 검출을 확정할 근거는 아니다.**

## 4. 두 브랜치에서 가져올 수 있는 인사이트

### 4.1 가장 직접적인 자산: 튜닝과 평가 분리

`stoic-knuth`의 [nested_cv_sat.py](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/scripts/nested_cv_sat.py#L468)는 바깥 검증 셀을 제외하고, 안쪽 데이터만으로 하이퍼파라미터를 다시 선택하는 구조를 갖고 있다. 이 **검증 구조**가 ZIP에 직접적인 참고가 된다. DEM 전용 특징·임계값·제외 규칙을 그대로 복사할 이유는 없다.

ZIP은 `gcv.fit(X,y)`로 전체 데이터에서 alpha/C를 고른 뒤, 선택값을 고정한 모델로 같은 데이터에 `cross_val_predict`를 수행한다. 표준화가 Pipeline 안에 있다는 점은 좋지만, **각 검증 셀의 정답이 이미 튜닝값 선택에 쓰였다**. 이는 nested CV가 아니다. scikit-learn도 동일 데이터로 선택과 평가를 수행하면 낙관적인 평가가 될 수 있음을 설명한다. [공식 nested CV 문서](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)

**이식 방향:** 바깥 CV는 최종 평가, 안쪽 CV는 alpha/C 선택. 대역이나 모델 종류까지 결과를 보고 선택한다면 그 선택도 평가 밖에서 미리 고정하거나 안쪽 절차에 포함한다. 이것이 실제 수치를 얼마나 바꾸는지는 2차에서 확인할 사안이다.

### 4.2 셀 단위와 배치 단위 일반화는 별개다

`friendly-meitner`의 [랩 ML 검토](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/kb/projects/ml_opportunities_from_lab_ppt_2026_07.md)와 [방법론 이전 카드](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md)는 같은 생성원·도펀트를 공유하는 행의 의존성과 group holdout의 중요성을 다룬다.

ZIP은 셀별로 EIS 전체를 한 행으로 만들므로, **주파수 포인트를 서로 다른 표본으로 랜덤 분할하는 구조는 아니다.** 이것을 누수라고 잘못 지적하면 안 된다. 실제 쟁점은 동일 셀 반복 측정의 선택 방식, 제조 배치·측정일·압력 등 공유 조건이다.

**이식 방향:** “동일 배치의 새 셀”을 맞힐지, “다음 제조 배치”를 맞힐지 먼저 정한다. 전자는 셀 holdout, 후자는 배치 holdout이 추가로 필요하다. nested CV와 group CV는 서로 대체하지 않으며 필요하면 함께 사용한다.

### 4.3 주파수 특징의 예측 기여와 물리 기전 귀속을 구분한다

`stoic-knuth`의 [ML 적용 지도 §4](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/docs/ml_application_map_dem_pipeline.md)는 랩의 EIS/DRT 특징→SOH·저항·Severe 분류 맥락을 명시한다. [EIS/DRT 문서](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/docs/eis_drt_ica_cv.md)는 등가회로·DRT·실험 앵커를 연결하는 자산이다.

**이식 방향:** raw EIS 대역별 모델을 기준으로 두고, 추후 식별 가능한 저항·DRT 대역 적분량 등 소수 특징을 비교 후보로 둔다. 단 “특정 주파수의 Ridge 계수가 크다”만으로 접촉손실·전하전달·확산 중 하나를 확정하지 않는다. 네 임피던스 성분은 같은 복소 임피던스의 관련 표현이며 주파수끼리도 상관될 수 있다.

또한 ZIP의 “특징을 늘려도 잔차가 줄지 않으면 스펙트럼 어디에도 흔적이 없다”는 문구는 너무 강하다. **시험한 특징·모델·표본에서 설명되지 않았다**까지가 적절하다. 측정 잡음, 비선형 관계, 보간, 대역 범위, 라벨 불확실성도 남아 있다.

### 4.4 모델은 비교 후보로 가져온다

`stoic-knuth`의 [강의 적용 매핑](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/machine-learning/APPLICATION_TO_DEM_DFT.md), Lecture 3·4·14는 선형회귀, 분류, 정규화와 검증의 기본 틀을 제공한다. ZIP의 Ridge·Logistic은 이 틀과 맞는다.

추후 비교 순서는 **동일한 셀·동일한 평가 분할에서 단순 기준선 → Ridge/Logistic → 제한된 비선형 후보**가 적절하다. OCV의 가치를 보려면 OCV 단독 기준선도 유용하다. GPR·트리 계열·TabPFN은 후속 후보이며, 현재 7셀 결과만으로 새 모델 도입을 우선할 근거는 부족하다.

TabPFN 원전은 작은 표형 데이터의 유력한 비교 모델이라는 근거다. 그러나 일반 벤치마크의 성능은 이 불량셀 데이터의 성능 보장이 아니다. 여기서는 2025 논문의 범위를 참고했으며 최신 배포판 사양을 검토한 것은 아니다. [Hollmann et al., Nature 2025](https://www.nature.com/articles/s41586-024-08328-6?error=cookies_not_supported)

### 4.5 잔차는 다음 측정을 정하는 데 활용한다

`friendly-meitner`의 방법론 문서는 실패·제외 표본의 분포와 실험 밖 일반화를 점검하도록 제안한다. `stoic-knuth`의 [설계 루프](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/be0ae956895cc7fb06817c427cff465aee9b4758/docs/ml_design_loop.md)는 DOE와 후보 재검증 절차를 다룬다.

**이식 방향:** 불량을 놓친 셀, 임계값 근처 셀, 모델들이 불일치하는 셀을 우선 재측정 후보로 삼되, 대표성 있는 독립 검증 셀은 별도로 확보한다. 불확실성이 큰 셀만 수집하면 검증 집단도 편향될 수 있다. 잔차가 큰 셀을 곧바로 제외하는 방식은 피한다.

## 5. litdb 확인 결과

### 5.1 두 브랜치의 litdb는 완전히 독립적인 문헌 묶음이 아니다

`friendly-meitner`는 SE·DFT용 `INDEX.md`와 DEM·MPM용 `INDEX_DEM.md`를 함께 둔다. `stoic-knuth`의 `INDEX.md`는 DEM·MPM 중심이다. 인덱스를 하나만 읽으면 ML/EIS 자료를 놓칠 수 있다.

동일 slug 3개를 양쪽에서 대조했다. **Kim 2025와 Choi 2024는 확인한 차이가 메타데이터 추가 중심**이고, **Duquesnoy 2023의 friendly 버전에는 2020 선행논문과의 비교 절이 추가**되어 있다. 따라서 두 브랜치에 같은 문헌이 있다는 사실을 독립적인 근거 두 건으로 세지 않는다.

### 5.2 불량셀 작업에 우선 연결할 4개 문헌

| 문헌 | litdb에서 확인한 내용 | 이번 작업에 연결할 점 | 해석 한계 |
|---|---|---|---|
| **Kim et al. 2025**, DOI 10.1016/j.electacta.2025.147413 | modified TLM으로 수송·전하전달·확산을 분해하고, 분리가 잘 되는 조건을 논의 | 주파수 대역/DRT/저항 특징의 해석 후보, 측정조건 기록 | 피크를 나눴다는 사실만으로 이 ZIP의 불량 원인이 특정되지 않음 |
| **Choi et al. 2024**, DOI 10.1021/acsami.4c01322 | 복합 양극 TLM 정식화, 입계·계면 저항과 압밀·입경의 관계 | 압력·입경·조성 등 공정 메타데이터를 EIS와 연결 | 다른 셀 조건의 저항값·임계값을 그대로 이식할 수 없음 |
| **Hollmann et al. 2025**, DOI 10.1038/s41586-024-08328-6 | TabPFN 표형 모델 | 데이터·CV 정리 후 비교 모델 후보 | 현재 7셀, 특히 불량 3셀에서의 우수성 근거는 없음 |
| **Duquesnoy et al. 2023**, DOI 10.1016/j.ensm.2022.12.040 | 제조 시뮬레이션→DOE→해석적 surrogate→최적화→실험 확인 | 후속 데이터 수집·공정개선 실험 설계의 참고 | 액체계 제조 최적화 연구이며 EIS 불량 분류기의 검증 논문은 아님 |

Digest 원문: [Kim 2025](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/kim2025_impedance_decoupling_tlm_assb.md), [Choi 2024](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/interfacial_impedance_formulation_assb_cathode.md), [Hollmann 2025](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/hollmann2025_tabpfn_tabular_foundation_model.md), [Duquesnoy 2023](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/634da438bf329b4e4baccd19c37e009a7168d67f/litdb/papers/duquesnoy2023_ml_multiobjective_manufacturing_optimization.md).

이번 1차에서 Kim·Choi·Duquesnoy의 근거는 **저장소 digest 판독**이다. 출판사 본문 접근이 되지 않아 PDF의 식·그림·수치까지 독립 재검증하지 않았다. TabPFN은 Nature 원문도 확인했다. digest의 ✅ 표시는 작성자의 상태 표기이며 이번 검토의 재검증 완료를 뜻하지 않는다.

### 5.3 브랜치의 해석도 검증 대상이다

참고 문서에는 높은 시뮬레이션 R², 모델 간 점수 차이, 모델 일반화에 관한 강한 해석이 섞여 있다. 예를 들어 서로 다른 연구의 R² 차이가 “거의 전부 CV·노이즈에서 왔다”거나, 선형모델과 비선형모델의 점수 차이만으로 교호작용이 확인됐다는 설명은 그 자체로 인과적 검증이 아니다.

따라서 가져올 자산은 **데이터 출처 기록, 선택/평가 분리, 그룹 검증, 대역 비교, 실측 재확인 절차**다. 다른 연구의 최고 점수나 정량적 우월성 주장은 이 보고서의 불량셀 결론으로 사용하지 않았다.

## 6. 2차에서 우선 반증할 항목

아래는 1차 읽기에서 얻은 구조적 관찰과 검증 질문이다. 실제 오류가 얼마나 발생했고 성능에 얼마나 영향을 주었는지는 아직 측정하지 않았다.

| ID | 우선순위 | 코드/자료에서 확인한 사실 | 2차 검증 질문 |
|---|---|---|---|
| V01 | 최우선 | 저장 결과 n=7, 탐색 주석 n≈54 | 어떤 파일·제외·설정으로 7셀이 되었나? ZIP 코드와 Excel은 같은 실행 버전인가? |
| V02 | 최우선 | 전체 데이터로 alpha/C를 선택한 후 CV 예측 (`export_for_origin.py:105,121,141`; `ridge_capacity.py:169`) | 튜닝·대역 선택을 평가와 분리해도 성능이 유지되나? |
| V03 | 최우선 | 소수 클래스 <5면 LOOCV, Logistic 튜닝 지표는 AUC (`export_for_origin.py:125,343`) | 1개 표본인 검증 fold에는 양쪽 클래스가 없으므로 fold AUC가 정의되지 않는다. 실제 실행에서 경고/NaN·선택 실패가 어떻게 처리됐나? |
| V04 | 높음 | 제외 셀 60·70·93, EIS 중복 셀은 dictionary에서 덮어씀 (`ridge_capacity.py:40,57`) | 제외 사유가 측정 QC인가? 동일 셀의 압력·시점별 파일 중 무엇이 선택됐나? |
| V05 | 높음 | 병합 함수가 타깃 용량의 유한성을 확인하지 않은 채 이진 라벨을 생성 (`export_for_origin.py:231,290`) | 결측 용량이 정상으로 라벨링되거나 일부 모델에만 남을 수 있나? |
| V06 | 높음 | cycle/step 선택·초기전류 1% 감소로 CC 종료 결정 (`extract_capacity.py:25,75`) | 용량과 CC 비율이 실제 프로토콜 및 장비 로그와 일치하나? |
| V07 | 높음 | OCV는 EIS 중 전위 중앙값, 압력·배치·측정시점은 검증에 미사용 | 선별 시점에 얻을 수 있는 특징인가? 조건 차이가 용량 관계를 대신 설명하나? |
| V08 | 중간 | 두 보조 진입점이 `target_cycles=`로 호출하나 함수는 `target_cycle=` (`ridge_capacity.py:274`, `feature_band_test.py:103`) | 선행 입력 문제 해결 후 해당 경로가 인자 오류로 중단되는가? 메인 export 경로는 단수형을 사용한다. |
| V09 | 중간 | 공통 격자를 전체 셀 범위로 정하고, `np.interp` 경계 기본 동작 사용 (`ridge_capacity.py:61,97`) | 문서의 “외삽”은 실제로 끝값 고정이다. 경계·중복 주파수·결측이 특징에 영향을 주나? |
| V10 | 중간 | README는 `cell번호`만 요구하지만 cycler 정규식은 `cell번호_압력MPa`를 요구 (`extract_capacity.py:39`) | 정상 파일이 명명 규칙 차이로 빠졌나? |

V03에서 **fold별 AUC 튜닝 실패와 모아 놓은 CV 예측의 전체 AUC는 구분**해야 한다. 7개 CV 점수를 모으면 두 클래스가 있어 전체 AUC는 계산할 수 있다. 그러므로 Excel의 AUC=1 자체가 불가능한 값이라는 뜻은 아니다. 다만 C가 유효한 검증으로 선택되었다고 보장할 수 없다. 첨부 Excel의 Logistic C는 8개 조합 모두 탐색 하한 0.001이며, 이것은 위 문제와 일관되지만 발생 증명은 실행 로그를 확인해야 한다. [scikit-learn AUC 구현](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/_ranking.py)

현재 원본 `.txt/.mpt`와 특징 행렬 X가 없으므로 V01·V04·V06·V07의 실제 영향 및 V02의 성능 변화를 계산할 수 없다. Excel에는 예측·타깃·계수가 있지만 재학습에 필요한 셀별 전체 EIS 특징 행렬은 없다. 하드코딩된 작성자 PC의 입력 경로도 현재 환경에는 존재하지 않는다.

## 7. 1차·2차·3차 진행안

| 단계 | 할 일 | 산출물 | 완료 기준 |
|---|---|---|---|
| **1차 — 이번 완료** | ZIP 구조, 데이터·타깃·평가 흐름, 저장 결과와 브랜치/litdb 연결 | 이 보고서 | 읽은 사실·해석·미확인을 구분하고 2차 검증 범위를 구체화 |
| **2차 — 범위 승인 후** | V01–V10 반증. 별도 작업 사본에서 입력·분할·지표를 검증하고 필요한 경우 제한된 재현 실행 | 문제별 근거·발생조건·영향·수정안, 기존 평가와 누수 방지 평가 비교 | 재현된 문제와 가설을 분리. 원본 부재 항목은 미확인으로 남김 |
| **3차 — 문제별 수정 승인 후** | 승인된 문제만 수정, 동일 데이터 기준 수정 전후 검증 | 변경 코드/diff, 변경 이유, 전후 비교, 남은 한계 | 실행 정확성·데이터 추적성·평가 타당성 확인. 점수 상승을 성공 조건으로 삼지 않음 |

2차는 먼저 **데이터가 없어도 할 수 있는 인자·결측·중복·CV 조건 검증**을 하고, 실제 성능 주장은 원본을 확보한 뒤 검증하는 순서가 적절하다. 현재 학습 실행까지 승인된 것으로 간주하지 않았다. 이 경계는 사용자가 제시한 단계별 검토·승인 방식에 따른 것이다.

### 7.1 2차에 필요한 자료

1. **실제 `.txt` / `.mpt` 폴더 또는 셀별 X·y 표**, 전체 입력 파일 목록. 54셀 실행과 7셀 실행의 관계·생성일·사용 코드 버전.
2. **60·70·93 제외 사유**, 누락 셀과 재측정 셀 기록. 성능을 보고 제외했는지, 별도 측정 QC에서 제외했는지 구분.
3. **EIS 측정 시점과 조건**: 충전 전/후, SOC, 휴지시간, 온도, 압력, 셀 구성·면적·배치. OCV의 실제 의미.
4. **사용 목표**: 같은 배치 내 선별인지 다음 배치 선별인지, 허용 가능한 불량 누락(FN)과 정상 오검출(FP), 90% 기준의 근거.

분류라면 FN/TP/FP/TN의 개수와 불량 민감도를 먼저 보고, AUC·PR 지표·확률 보정은 자료 규모와 목적에 맞게 보완한다. 회귀라면 Ah 또는 mAh의 MAE/RMSE와 Q²를 함께 보고, 임계값 근처 오차를 별도로 본다. 비교 모델들은 같은 바깥 검증 셀을 사용한다. 소표본에서 나온 점수와 구간을 생산 배치의 보장치로 해석하지 않는다.

## 8. 근거 탐색 목록

선별 검토한 브랜치 자료는 다음과 같다. HEAD 이후 갱신은 반영하지 않는다.

| 브랜치 | 읽은 자료 |
|---|---|
| friendly `634da438` | `kb/projects/ml_opportunities_from_lab_ppt_2026_07.md`; `kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md`; `litdb/README.md`; SE·DEM 인덱스 관련 항목; Kim·Choi·Duquesnoy·Hollmann digest |
| stoic `be0ae956` | `machine-learning/README.md`; `APPLICATION_TO_DEM_DFT.md`; Lecture 3·4·14; `docs/ml_application_map_dem_pipeline.md`; `docs/ml_design_loop.md`; `docs/ml_v3_surrogate_cycling.md`; `docs/eis_drt_ica_cv.md`; `scripts/nested_cv_sat.py`의 설명·중첩 검증 핵심; `litdb/README.md`·인덱스 관련 항목; Kim·Choi·Duquesnoy digest |
| 외부 보조 확인 | scikit-learn nested CV 문서·AUC 문서/구현, Nature TabPFN 원문. Kim·Choi·Duquesnoy 출판사 본문은 접근 불가로 독립 확인하지 못함 |

현재 가장 먼저 해결할 질문은 **“어떤 셀 집단의 어떤 측정 시점에서 얻은 EIS로, 어느 정도의 용량 미달을 선별하려는가?”**이다. 그 답과 검증 분할을 고정하면, 두 브랜치의 ML 자산을 활용해 모델 비교와 물리 특징 확장을 순서 있게 진행할 수 있다.
