# 원본 대비 변경 — R1–R7

v2.0.0 / 2026-09-15

| 항목 | 원본에서 확인한 동작 | v2 동작 |
|---|---|---|
| R1 입력·라벨 | NaN 용량이 비교에서 정상 0으로 변하는 경로, Inf 입력 검사 부족 | 유한·양수 용량을 확인한 뒤 라벨 생성. 결측은 미확인 오류로 기록. 예측 입력으로 분리 가능 |
| R2 중복·제외 | EIS 중복 파일이 열거 순서에 따라 덮어씀. 제외 전에 격자 결정 | 중복 셀 거부 또는 명시적 파일 manifest. 제외를 먼저 적용. 격자는 사전 설정 |
| R3 cycler 해석 | 고정 행 위치, 무조건 첫 행 제거, 구간/시간 검증 부족 | 헤더 탐색, 확인된 단위행만 제거, 대상 cycle·구간 선택, 시간·전류·용량 관계 검사 |
| R4 EIS 표현 | 범위 밖 끝값 고정, 중복 주파수 순서 의존, 성분별 보간 불일치 | 경계 기본 거부, 명시적 허용/로그, 중복 기본 거부, Re/Im 보간에서 크기·위상 유도 |
| R5 모델 선택 | 전체 자료에서 alpha/C를 고른 뒤 같은 자료의 CV 예측, 작은 fold AUC | 안쪽 fold에서 대역·모델·정규화 선택, 바깥 셀/배치 평가. 분류 선택 log loss |
| R6 출처·진단 | 입력·제외·선택·환경의 추적 정보 부족 | 셀/파일 해시·실패 사유, 분할 ID·그룹·표준화·선택 로그, OOF와 전체 적합 구분 |
| R7 실행 | 절대 경로와 import 시 폴더 생성, 보조 호출 인자 불일치 | 새 출력 경로를 받는 CLI. import 부작용 제거. 호환 실행점. 버전 고정과 테스트 |

추가: 모델 저장·새 CSV 추론, 가상 예제, 범위 이탈 표시, Excel 문자값 보호, CC 타깃 결측 시 셀 ID로 예측 정렬, malformed 특징명/설정 검사.

기존 결과 Excel과 수치를 같게 만드는 변경이 아니다. 평가 절차·후보 구성·기본 제외 정책·격자·경계 처리가 달라졌으므로 실제 입력에서 이전/이후 성능을 별도로 재계산해야 한다. 원본 저장 Excel의 7셀은 실측 특징이 제공되지 않아 재학습하지 않았다. 원본 ZIP과 원격 브랜치는 보존했다.

기존 16개 회귀/16개 분류 조합을 단순 순위표로 반복하지 않고, 선택 행위를 중첩 검증 안에 포함했다. 11개 Excel 시트명은 유지하지만 열 구조는 변경되었으므로 기존 Origin 그래프 템플릿의 열 매핑은 다시 지정해야 한다.

# 독립 리뷰 반영 — v2.0.0 갱신분

v2.0.0 / 2026-09-15 (독립 리뷰 라운드)

배포판 v2.0.0을 대상으로 한 독립 리뷰의 확정 지적을 네 모듈(`extract_capacity.py`, `predict.py`, `export_for_origin.py`+`ridge_capacity.py`, `tests/`)에 반영하고 문서를 코드에 맞췄다. **버전 번호는 그대로 2.0.0이다.** 모두 견고성·진단·문서 항목이며 모델링 방법 자체를 바꾼 것은 없다.

## 평가 의미는 바뀌지 않았다

중첩 CV 구조, Q²/RMSE/MAE/AUC/MCC 정의, 안쪽 선택 지표(회귀 MSE, 분류 log loss), `logistic_class_weight` 기본값은 모두 그대로다. 갱신 전후 코드로 동봉 예제를 실행해 다음이 **바이트 단위로 동일**함을 확인했다.

- `--demo` 실행의 `oof_predictions.csv`
- 원시 TXT/MPT → `extract_capacity.py`가 만든 `prepared.csv`
- 그 자료의 그룹 평가 실행의 `oof_predictions.csv`

기존 지표 행(`capacity_nested_selection`, `baseline_mean`, `baseline_mag@1000Hz`, `baseline_ocv`, `ccfrac_nested_selection`, `capacity_threshold`, `logistic_nested_selection`)의 수치도 변하지 않았다. 달라진 것은 표에 **행과 열이 늘어난 것**뿐이다.

## 입력 판독 (`extract_capacity.py`)

- CC/CV 전환 판정을 '구간 첫 행 대비 1% 하락'에서 '초반 `cc_reference_rows`행 중앙값 대비 `cv_relative_drop` 이상 하락이 `cc_sustained_rows`행 연속 또는 구간 끝까지 유지'로 바꿨다. 노이즈 한 점이나 초반 오버슈트가 전환을 만들지 않는다. 실측 자료에서는 `cv` 전환 행과 `cap_cc`/`cc_frac` 값이 달라질 수 있으므로 **`cc_fraction` 회귀의 Q²/RMSE와 Origin 표를 재계산해 비교해야 한다**(`cap`과 logistic은 `cc_frac`를 쓰지 않아 불변).
- 유한성·시간 단조 검사 범위를 파일 전체에서 `target_cycle` 구간으로 좁히고 `Voltage(V)`·`Step Time(s)`를 검사에서 뺐다. 과거에 '거부'로 기록된 원시 파일이 이제 통과할 수 있으므로, 손으로 잘라 낸 파일이 있으면 원본으로 재처리해 값이 같은지 확인한다.
- `cap` 중앙값이 `design_capacity_ah`의 1/`cap_plausibility_factor`–배 구간을 벗어나면 학습을 중단한다. mAh 값으로 '완료'되던 과거 실행은 이제 실패하며, 그 실행으로 저장된 `models/*.joblib`과 Excel은 폐기 대상이다. 설계 용량 1.5배 초과 셀에는 `warning` 이벤트가 새로 생긴다.
- 기본 `encodings`에 `cp1252`를 추가했다. 이전에 인코딩 실패로 제외했던 EC-Lab `.mpt`가 이제 읽히므로 코호트가 달라질 수 있다.
- 셀당 `.mpt`가 여러 개일 때 EIS 필수 헤더가 없는 파일을 자동 제외하고(`skipped_non_eis_file`), 한 파일에 sweep이 여러 번 쌓인 경우를 `eis_sweeps`로 세어 `eis_sweep` 설정으로 고를 수 있게 했다. `duplicate_frequency_policy='mean'`에 `mean_max_ewe_spread_v`를 설정하면 서로 다른 상태의 평균은 거부된다.
- 대문자 `Re@`/`Im@`/`Mag@` 열이 조용히 무시되지 않고 `DataError`가 된다. 그런 CSV로 만들어진 과거 실행은 실수부·허수부 없이 학습된 것이므로 열 이름을 고쳐 재학습해야 한다.
- CLI 계약: 설정·manifest 오류가 traceback + exit 1 대신 `Input error:` + **exit 2**가 되고, `<output>.audit.json`이 실패 시에도 생성되며 내용이 이벤트 배열에서 `{version, status, config, selection_manifest, events}` 객체로 바뀌었다. 이 파일을 파싱하는 외부 스크립트가 있으면 수정이 필요하다.
- 신규 설정 `cc_reference_rows`, `cc_sustained_rows`, `trim_zero_current_boundary_rows`, `eis_sweep`, `mean_max_ewe_spread_v`, `cap_plausibility_factor`. 기본값은 이전 동작을 유지하도록 잡았다(`trim_…`은 `false`, `eis_sweep`은 `all`).

## 예측 (`predict.py`)

- 범위 이탈 판정에 상대 1e-9·절대 1e-12 허용오차를 두고 예측 CSV를 `float_precision='round_trip'`으로 읽는다. 동봉 예제에서 부동소수 1 ulp 때문에 `review_required`가 켜지던 3개 셀이 이제 0이다.
- 출력 CSV에 `review_reason`, `{model}_outside_features`, `predicted_capacity_mAh_cm2` 열이 추가되고, `review_required`·`*_outside_training_range`·`*_seen_in_training`이 불리언에서 **0/1 정수**로 바뀌었으며, 입력 CSV의 비특징 메타데이터 열이 오른쪽에 붙는다. 결과 행 순서가 'cell_number 오름차순'에서 **'입력 CSV 순서 유지'**로 바뀌었다(정렬된 CSV를 넣으면 결과는 같다).
- `models/*.joblib`를 읽기 전에 `artifact_hashes.json`과 대조하고, 파일 이름을 `capacity`/`cc_fraction`/`logistic`로 제한하며 번들의 `model_name` 일치를 강제한다. 모델을 개명·복사해 쓰던 작업 흐름은 exit 2로 거부된다.
- scikit-learn 주·부 버전 불일치를 기본 거부하고 `--allow-version-mismatch`로만 진행한다. 다른 sklearn 환경에서 모델을 재사용하던 경우 동작이 달라진다.
- 실패 시 결과 CSV·provenance 부분 산출물을 남기지 않으므로 같은 `--output`으로 재실행할 수 있다.
- `<output>.provenance.json`에 실행 폴더·해시·환경 비교·상태·`unavailable`·모델별 추정기와 선택 특징·임계값·열 단위·범위 허용오차·재검토 셀 수가 추가되었다(기존 `features_sha256`·`model_sha256`·`data_kind`·`note` 키는 유지).

## 지표·보고 (`export_for_origin.py`, `ridge_capacity.py`)

- 분류 표에 우연 기준 행(`baseline_<name>_threshold`, `baseline_prior`)이 추가되고, `probabilities=True` 행에 `log_loss_prior_baseline`·`brier_prior_baseline` 두 열이 추가되었다. `classification_metrics.csv`·`metrics.json`·`06_clf_metrics`·`10_confusion_matrix`의 행 수와 `05_clf_roc`의 곡선 수가 늘어난다.
- 회귀 지표 행의 열 순서가 `model`·`target` 선두로 바뀌고 `coefficients`에 `model_kind` 열이 추가되었다. `regression_metrics.csv`·`02`·`03` 시트를 읽는 외부 스크립트가 있으면 열 순서 가정을 확인한다.
- 전체 자료 배포 적합(`save_final`) 실패와 안쪽 적합 미수렴이 실행 전체 실패가 아니라 **타깃 단위 `unavailable`**이 된다. 이전에 `status='failed'` + exit 2였던 경우가 이제 `status='partial'` + exit 0이다. exit code·status를 자동화에서 쓰고 있다면 재확인이 필요하다.
- `metrics.json`에 `skipped_candidates`·`diagnostics`·`notes`, `run.json`에 `headline` 키가 추가되고 `code_sha256` 키가 정렬되었다. `versions`에 `platform`·`machine`·`blas`가, `models/*.joblib` 번들에 `selected_features`·`versions`가 추가되었다(`predict.py`는 두 키가 없어도 동작한다).
- `run_summary.md`에 지표 요약표, fold별 선택 빈도, 모델 진단, 제외된 후보·기준선 절이 생기고 '계산하지 못한 항목' 문구가 사유별로 나뉘었다. 콘솔에 핵심 수치 한 줄이 추가된다. 로그를 문자열로 비교하는 절차가 있으면 갱신이 필요하다.
- `results_for_origin.xlsx`: `04_reg_residual`에 `pred_cc_frac` 열이 추가되고, `05_clf_roc` 첫 행의 임계값이 명시적 공란이 되며, 시트 수는 11개 그대로다. **수식 가드의 보호 범위는 `results_for_origin.xlsx`이며 apostrophe를 값에 섞지 않고 `quotePrefix`로 처리한다.** `*.csv` 출력에는 수식 이스케이프를 적용하지 않으므로 CSV를 스프레드시트로 직접 열 때는 텍스트 가져오기를 쓴다.
- `artifact_hashes.json`의 키가 OS 경로 구분자에서 POSIX(`/`)로 바뀌었다. Windows 실행의 `models\capacity.joblib`이 `models/capacity.joblib`으로 기록되므로 이 키를 읽는 외부 도구가 있으면 확인한다(읽기 측은 과거 백슬래시 기록도 계속 허용한다).

## 테스트·검증 (`tests/`)

- 자동 테스트가 131개로 늘었다(`test_extract`, `test_models`, `test_predict`, `test_pipeline`, `test_tests`). 테스트는 현재 작업 디렉터리 대신 시스템 임시 폴더를 쓴다.
- `verify_release.py`의 검사가 값 수준 oracle 2개를 포함해 7개가 되었고, 하위 프로세스를 `-X utf8 -B`로 실행하며 `-O`/`PYTHONOPTIMIZE`에서는 실행을 거부한다. `release_verification.json`의 `code_sha256` 키가 POSIX 형식이 되고 `.venv`/`results`/`__pycache__`/숨김 폴더가 제외되며 키 기준으로 정렬된다.
- `validation/release_verification.json`과 7개 로그, `MANIFEST.sha256`을 이 라운드에서 모두 재생성했다.

## 실측 자료가 필요한 남은 과제

이번 라운드는 소프트웨어 견고성과 진단을 고친 것이고, **실제 측정 자료는 여전히 없다.** 다음은 실측 자료 없이는 해결할 수 없다.

- 실측 성능. 동봉 수치는 전부 가상 데이터이며 불량셀 판별 성능의 근거가 아니다. 소표본에서는 순수 잡음으로도 Q²가 양수, AUC가 0.8 이상 나올 수 있으므로 인용 전에 라벨 순열·부트스트랩을 별도로 수행한다.
- CC/CV 판정 규칙 변경이 실측 `cc_frac`에 주는 영향의 재계산.
- EIS 측정 시점·SOC 정의와 `ocv` 특징의 프로토콜 누수 여부. 가상 예제는 `ocv`에 라벨을 직접 넣어 만들었으므로 릴리스 검증에서 최종 용량 모델이 OCV 단독으로 선택되는 것은 물리적 결론이 아니다.
- 라벨 정의. 기본값은 1주기 충전 용량이며 ASSB 첫 충전의 비가역 용량을 포함한다. 가역 용량 기준이 맞는지, 셀별 활물질 로딩 편차를 어떻게 다룰지는 실험 설계 결정이다.
- 주파수 격자·후보 대역의 물리적 근거와 원시 sweep 밀도 확인.
- 랩 실제 환경(Windows)에서의 전체 재실행과 `validation/` 기록 갱신.

## 이번 라운드에서 의도적으로 보류한 것

- 예측 출력 열 이름에 단위를 넣는 변경(`predicted_capacity` → `predicted_capacity_Ah`). 출력 스키마가 깨지므로 다음 minor 버전 과제로 남긴다.
- Logistic 안쪽 선택 scorer의 균형 가중화. 적용하려면 별도 결정과 전체 산출물 재생성이 필요하다.
- 대역 후보를 `(re, im)` 한 표현으로만 구성하는 옵션. 기본 동작을 바꾸면 기존 산출물 재현성이 깨진다.
- `--permutations` 옵션과 셀 단위 부트스트랩 구간. 현재는 점추정치만 보고한다.
- `export_for_origin.py --features` 경로의 `float_precision='round_trip'` 적용과 사용자 정의 대역 설정.
