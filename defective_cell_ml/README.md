# 불량셀 머신러닝 v2.0.0

EIS 특징으로 용량을 예측하고, 지정한 용량 기준의 미달 여부를 평가하는 Python 패키지다. 원본 ZIP 검토에서 확인한 R1–R7을 반영했다. **실행 가능한 분석 코드이며, 실제 불량셀 성능을 검증한 완성 학습 모델은 아니다.** 실제 원시 측정 자료가 없어 검증에는 가상 데이터만 사용했다.

첨부 문서와 두 브랜치·litdb에서 검토한 아이디어 중 중첩 검증, 셀·배치 분리, 단순 기준선, 물리적으로 일관된 EIS 표현, 입력·실패 이력 기록을 적용했다. 자세한 근거는 `docs/METHODS_AND_SOURCES.md`, 변경 내용은 `docs/CHANGES.md`, 실행 검증은 `validation/`에 있다.

## 1. 설치하고 바로 실행하기

ZIP을 풀고 **이 README가 있는 `defective_cell_ml` 폴더에서** PowerShell을 연다. Python 3.12가 필요하며 검증 환경은 Windows/Python 3.12.14다. 첫 의존성 설치에는 인터넷 연결이 필요하다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe export_for_origin.py --demo --output results\demo
```

`py` 명령이 없고 `python --version`이 3.12라면 첫 줄을 `python -m venv .venv`로 실행한다. 가상환경 활성화나 PowerShell 실행 정책 변경은 필요 없다. 기본 전체 후보 탐색은 셀 수에 따라 시간이 걸린다.

완료되면 `results/demo/run_summary.md`와 `results/demo/results_for_origin.xlsx`를 연다. 가상 12셀의 점수이므로 실제 성능으로 인용하지 않는다. 같은 명령을 다시 실행하려면 `results/demo_02`처럼 **새 출력 경로**를 사용한다.

## 2. 실제 자료로 실행하기

### 원시 cycler TXT + EIS MPT

```powershell
.\.venv\Scripts\python.exe export_for_origin.py --config config.json --cycle-dir "D:\my_data\cycle" --eis-dir "D:\my_data\eis" --output results\measured_01
```

입력 폴더를 실제 경로로 바꾸고 `config.json`에서 측정 프로토콜에 맞는 cycle·구간·전류 방향·주파수 격자·셀 범위를 지정한다. 폴더 바로 아래의 `.txt`, `.mpt`만 읽는다. 두 종류 파일이 셀별로 하나씩 대응해야 한다. 실제 계측기에서 기본 설정이 맞는지 한 셀의 원시 값과 추출 용량을 먼저 대조한다.

같은 셀의 파일이 여러 개라면 사용할 파일을 `examples/selection_manifest.csv` 형식으로 명시한다. `cell_number,cycle_file,eis_file`이 필요하고, 그룹 평가에는 `batch_id`도 필요하다. 파일 경로는 각각 입력 폴더 기준이며 셀 번호가 파일명과 같아야 한다. 선택 사유는 `selection_reason` 등에 기록해 둘 수 있다. 실행 기록에 manifest 해시가 남는다.

```powershell
.\.venv\Scripts\python.exe export_for_origin.py --config examples\config_group.json --cycle-dir "D:\my_data\cycle" --eis-dir "D:\my_data\eis" --selection-manifest "D:\my_data\selection.csv" --output results\measured_group_01
```

배치 일반화가 목표라면 배치 번호를 실제 제조 이력과 연결하고 그룹 평가를 사용한다. 입력의 행 순서나 임의의 가상 그룹으로 배치를 대신하지 않는다.

### 특징 CSV가 이미 있는 경우

```powershell
.\.venv\Scripts\python.exe export_for_origin.py --config config.json --features "D:\my_data\features.csv" --output results\measured_csv_01
```

한 행이 셀 하나다. 같은 셀의 반복 측정을 여러 독립 표본으로 넣지 않는다. CSV 경로에서는 이미 추출된 특징의 원시 EIS 일관성이나 측정 시점을 재검증할 수 없다.

| 열 | 의미·조건 |
|---|---|
| `cell_number` | 고유 정수 셀 번호 |
| `cap` | 실측 용량 Ah. 학습에는 유한한 양수 필수 |
| `re@1000Hz`, `im@1000Hz`, `mag@1000Hz`, `phase@1000Hz` 등 | 주파수별 EIS 특징. 임피던스 Ohm, 위상 degree. 유한값 필수 |
| `ocv` | EIS 측정 중 전위의 중앙값 V. 기본 설정에서 필수 |
| `cc_frac` | 선택적 CC/전체 용량 비율, 0–1. 빈 값은 이 타깃의 평가에서만 제외 |
| `batch_id` | 그룹 평가 시 필수. 다른 열 이름은 `group_column`으로 지정 |

실행에 사용할 주파수의 열을 제공한다. 원시 변환기는 고정 격자의 네 성분을 모두 만든다. CSV에서는 일부 성분만 제공할 수 있으나 후보 대역에 실제 열이 있어야 한다. 이름은 `1000Hz`, `100000Hz`, `1e+06Hz`처럼 Python `:g` 표기다. `1kHz`는 인식하지 않는다. 그 외 메타데이터는 모델 특징으로 자동 사용하지 않는다.

OCV 없이 분석하려면 `examples/config_eis_only.json`을 사용하거나 설정의 `use_ocv`를 JSON 불리언 `false`로 바꾼다. OCV 결측 행을 자동 제거해 표본 수를 줄이지 않는다. 용량을 모르는 셀은 학습 CSV에서 분리해 아래 예측 경로로 보낸다.

## 3. 저장 모델로 새 셀 예측하기

```powershell
.\.venv\Scripts\python.exe predict.py --run results\measured_01 --features "D:\my_data\new_features.csv" --output results\new_predictions_01.csv
```

`--run`에는 사용자가 이 패키지로 만든 정상 완료 학습 폴더를 지정한다. 새 CSV는 학습 때의 특징 열·단위가 같아야 하며 `cap`, `cc_frac` 정답은 필요 없다. 추가 학습 없이 저장된 변환·모델을 적용한다. 예측용 셀 번호는 학습 범위 밖이어도 가능하다.

새 EIS 원시 파일만 있다면 먼저 특징을 만든다. 학습 실행의 `config.json`을 복사해 주파수·OCV 설정은 유지하고 새 셀 번호가 포함되도록 `cell_min`, `cell_max`, 제외 목록을 조정한다. **원시 입력 준비에도 설정의 셀 필터가 적용된다.**

```powershell
.\.venv\Scripts\python.exe extract_capacity.py --config new_input_config.json --eis-dir "D:\my_data\new_eis" --output results\new_features_01.csv
.\.venv\Scripts\python.exe predict.py --run results\measured_01 --features results\new_features_01.csv --output results\new_predictions_02.csv
```

예측 결과에는 용량 Ah, CC 비율(학습 가능했던 경우), Logistic 점수·판정, 용량 임계값 판정이 들어간다. `seen_in_training`은 같은 ID의 재입력 여부이고 `outside_training_range`는 특징별 관측 최소–최대 범위 이탈이다. `review_required`는 범위 이탈이나 용량/비율 출력의 물리 범위 위반을 표시한다. 이는 검증된 OOD 탐지기·불확실성 구간·재검사 최적 정책이 아니다. 범위 안이라는 이유로 예측이 신뢰할 만하다고 확정하지 않는다.

Joblib 모델은 자신이 생성했거나 신뢰하는 로컬 실행 결과만 읽는다. 모델을 다시 읽을 때도 동일한 의존성 버전을 사용한다. ZIP에는 실제 학습 모델을 넣지 않았다.

## 4. 설정과 용량 정의

설정 파일의 생략 항목은 기본값을 사용하고 알 수 없는 키는 거부한다. 전체 기본값은 `config.json`에 있다.

| 설정 | 기본값·동작 |
|---|---|
| `threshold_ah` | 0.01802088 Ah 이하를 1, 초과를 0으로 정의 |
| `design_capacity_ah` | 0.0200232 Ah. 기본 임계값은 이 값의 90% |
| `area_cm2` | 3.24 cm². 표시용 Ah→mAh/cm² 환산 |
| `cell_min`, `cell_max` | 학습·원시 준비 대상 34–98 |
| `exclude_cells` | 기본 `{}`. 예: `{"60":"측정 전 확정한 QC 제외 사유"}`. 원본의 60·70·93 제외는 사유 미확인으로 자동 승계하지 않음 |
| `target_cycle`, `target_step_i` | cycle 1 안의 두 번째 연속 구간. `step_i`는 0부터 시작 |
| `target_raw_step` | 기본 `null`. 숫자를 지정하면 원시 `Step No.`로 선택하고 `step_i`를 대신함 |
| `expected_current_sign` | `positive`. 충전이 음수인 장비는 `negative` |
| `cv_relative_drop` | 선택 구간 첫 전류 절댓값보다 1%를 초과해 내려간 첫 지점 탐지(코드의 엄격한 `<` 비교) |
| `frequency_grid_hz` | 측정 프로토콜로 미리 정한 0.01–1,000,000 Hz의 10배 간격 9점 |
| `boundary_policy` | `error`: 측정 주파수 범위 밖 격자는 거부 |
| `max_boundary_fraction` | 명시적 `clamp` 사용 시 경계 상대 차이 5%까지 끝값 고정 허용. 해당 점을 로그에 기록 |
| `duplicate_frequency_policy` | 기본 `error`. 명시적 `mean`은 같은 주파수의 복소 성분을 평균 |
| `use_ocv` | `true`: OCV 포함/미포함 후보를 동일한 완전 관측 셀 집단에서 비교 |
| `outer_cv` | `leave_one_cell_out` 또는 `leave_one_group_out` |
| `inner_splits` | 최대 3. 클래스·그룹 수에 따라 가능한 수로 축소 |
| `decision_threshold` | Logistic 판정 0.5. 바깥 평가 정답으로 최적화하지 않음 |

cycler 입력은 필수 열을 헤더에서 탐색하고 확인된 단위행만 제거한다. 시간 역전, 잘못된 전류 부호, 비유한 값, 감소하는 선택 구간 누적 용량을 거부한다. 용량은 선택 구간의 마지막 `|Q|(Ah)`다. 그 값이 구간 누적 용량으로 정의되는 장비인지 확인해야 한다. 시작 용량을 빼거나 전류를 적분하는 방식은 아니다.

CC 용량은 첫 전류 하락 지점 행까지의 용량이고 CV 용량은 전체와의 차이다. 하락이 없으면 CC=전체로 둔다. 이 휴리스틱이 실제 충전 프로토콜의 CC→CV 전환과 맞는지는 원시 장비 이력으로 확인해야 한다. `data_audit.json`에 선택한 구간, 행 수, 첫 용량, 전환 지점을 기록한다.

MPT의 `-Im(Z)/Ohm`은 부호를 반전해 실제 Im으로 저장한다. Re/Im을 로그 주파수에서 선형 보간하고, 그 결과로 크기와 위상을 계산한다. `<Ewe>/V` 중앙값이 평형 OCV와 동일하다고 자동 가정하지 않는다. SOC·온도·압력·측정 시점은 실제 자료 수집 단계에서 관리해야 한다.

## 5. 모델과 결과 해석

바깥 셀/배치를 남긴 뒤, 안쪽 학습 자료로만 대역·OCV 포함 여부·정규화 강도를 선택한다. StandardScaler도 각 학습 fold 안에서 적합한다. 선택 후 바깥 셀을 한 번 예측하고, 전체 바깥 예측(OOF)을 모아 지표를 계산한다.

회귀 후보는 평균 기준선, `|Z|@1 kHz` 선형회귀, OCV 단독 선형회귀, 대역별 Ridge다. CC 비율도 같은 선택 구조다. Logistic은 대역과 C를 안쪽 **log loss**로 선택한다. 한 셀 fold의 AUC로 C를 고르지 않는다. AUC는 양성·음성이 있는 전체 OOF 점수에서 계산한다. Logistic 출력은 확률 보정을 검증하지 않은 모델 점수다.

후보 대역은 1 kHz, 1–100 kHz, 0.1–10 Hz, 전체이며 입력에 존재하는 열을 사용한다. 회귀 선택 점수는 MSE다. 최종 표는 이 선택 절차의 성능과 사전 고정 단순 기준선을 보여 준다. 표에서 다시 가장 좋은 모델을 고르면 추가 독립 평가가 필요하다. 평가 후 전체 적격 자료로 선택·재적합한 모델은 배포/예측용으로 별도 저장하며 그 훈련 점수를 검증 성능으로 쓰지 않는다.

용량 미달 라벨은 안전 결함·수명·불량 원인을 자동 판별하지 않는다. 셀 수가 적으면 중첩 CV를 해도 불확실성이 크다. 실행 최소 4셀, 그룹 평가 최소 3그룹은 통계적 충분성 기준이 아니다. 분류는 모든 필요한 학습/검증 분할에서 클래스 수가 충족되어야 한다. 불가능하면 그룹을 쪼개지 않고 해당 항목을 `unavailable`로 남긴다.

| 결과 | 내용 |
|---|---|
| `run_summary.md` | 실행 요약과 계산하지 못한 항목 |
| `oof_predictions.csv` | 셀별 실측·독립 평가 예측·잔차·판정 |
| `regression_metrics.csv`, `classification_metrics.csv` | Q²/RMSE/MAE, 혼동행렬·민감도·특이도·pooled AUC 등 |
| `results_for_origin.xlsx` | 기존 시트명 11개 유지. 열 구조는 v2의 정리된 표로 변경 |
| `folds.json` | 안쪽/바깥 셀·그룹, 선택 모델·특징·점수, 표준화 평균 |
| `deployment_fit.json`, `models/` | 평가 뒤 전체 자료 적합 이력과 예측용 모델 |
| `input_features.csv`, `data_audit.json` | 사용 특징과 제외·입력 처리 이력 |
| `run.json`, `config.json`, `artifact_hashes.json` | 버전·환경·입력/소스 해시·설정·출력 무결성 |

`Q2`는 전체 OOF의 `1-SSE/SST`이며 음수가 가능하다. 표준화 계수는 전체 자료 최종 적합 값으로 인과 중요도가 아니다. MAPE는 절댓값 0.001 이상인 타깃에서만 계산하므로 0에 가까운 CC 비율에서는 RMSE/MAE를 먼저 본다. 회귀 RMSE/MAE의 기본 단위는 타깃 단위다.

프로세스 종료 코드 0은 실행 완료이며 일부 선택 타깃을 계산할 수 없는 `partial`도 포함한다. `run.json`의 상태와 `unavailable`을 함께 확인한다. 필수 입력·용량 평가 실패는 종료 코드 2와 `failed` 상태로 기록한다. 실패 출력 폴더도 원인을 조사할 때까지 보관한다. 입력 인자/설정 자체가 잘못된 경우 출력 폴더 생성 전에 종료할 수 있다.

## 6. 테스트와 파일 구성

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\verify_release.py --output results\release_check
```

첫 명령은 입력·누수 방지·그룹·출력·예측 테스트다. 두 번째는 전체 기본 데모와 원시/CSV 실행, 재현성, 새 특징 준비, 저장 모델 예측을 추가 확인한다. 예제는 이미 들어 있어 재생성하지 않아도 된다. 검증 결과는 실제 데이터 성능을 뜻하지 않는다.

`export_for_origin.py`가 메인 학습·검증 실행점이다. `extract_capacity.py`는 학습 없는 입력 변환, `predict.py`는 저장 모델 추론이다. `ridge_capacity.py`와 `feature_band_test.py`의 직접 실행은 메인 CLI를 호출한다. `config.py`, `demo.py`는 공통 설정/가상 입력을 제공한다. import 시 분석 실행이나 외부 출력 폴더 생성은 하지 않는다.
