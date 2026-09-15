# 배포 전 검증 기록

검증 자료는 모두 가상 입력이다. 실제 배터리 원시 자료가 없어 실측 성능·성능 개선 폭·외부 배치 일반화는 검증하지 않았다. 아래 표는 `tests/verify_release.py`가 실제로 무엇을 증명하는지를 그대로 적은 것이며, 증명하지 않는 것도 함께 적었다.

| 확인 | 무엇을 증명하는가 |
|---|---|
| 입력/분할/출력/예측 자동 테스트 (`01_unit_tests`) | 131개 통과. 원시 판독, 누수 방지, 그룹 분리, 지표 계산, 예측 계약, 릴리스 검사 자체의 단위 시험 |
| `raw_readers_restore_the_published_example_features` | 원시 TXT/MPT 판독기가 동봉 `examples/demo_features.csv`의 **알려진 값**을 복원하는지(rtol=1e-9 / atol=1e-12). 이번 라운드에 추가한 값 수준 대조다 |
| `raw_and_prepared_csv_reproduce_same_OOF` | 원시 입력 경로와 변환 CSV 경로의 OOF 예측이 같다(rtol=1e-8 / atol=1e-12). **같은 세션의 같은 파서가 만든 CSV를 다시 읽는 것이므로 'CSV 저장→재로드 왕복이 값을 바꾸지 않는다'만 보증한다.** 파서가 알려진 값을 복원하는지는 위 검사가 본다 |
| `all_three_runs_complete_12_cells_11_sheets_finite_metrics_and_valid_hashes` | 3개 실행(기본 데모·원시 그룹·CSV 그룹)이 모두 `completed`, 셀 12개, Excel 시트 11개, 혼동행렬 분모 12, 예측 유한, 수식 셀 없음, `artifact_hashes.json`과 실제 출력 해시 일치 |
| `all_three_runs_reproduce_the_fixture_labels_outcomes_and_score_direction` | 픽스처의 실제 용량에서 유도한 라벨·혼동행렬·`outcome_*` 문자열·점수 방향(점수는 용량이 낮을수록 커진다)이 값 수준에서 재계산된다. 기대값은 픽스처와 `config.json`에서 유도하므로 픽스처나 설정이 바뀌면 함께 따라간다 |
| `all_three_targets_keep_outer_and_inner_groups_separate` | 용량·CC 비율·Logistic 세 타깃의 바깥/안쪽 그룹이 겹치지 않는다. **이 검사는 `folds.json`의 자기보고 기록을 읽는다.** 실제로 `GridSearchCV`에 전달된 분할을 spy로 확인하는 시험은 `tests/test_tests.py`에 따로 있다 |
| `saved_models_predict_12_unlabeled_new_identifiers` | 정답 없는 EIS → 저장 모델 추론이 새 ID 12개(61–72)에 대해 완료되고 값이 유한하며 `*_seen_in_training`이 모두 0이다. ID만 바꾼 가상 특징이므로 독립 성능 검증이 아니다 |
| `saved_models_reproduce_the_fixture_capacities_and_defect_decisions` | 저장 모델의 예측 용량이 픽스처 실제 용량과 3e-3 Ah 이내이고, `capacity_predicted_defective`·`logistic_predicted_defective`가 픽스처 라벨과 일치한다 |
| 원본 ZIP | SHA-256 보존 확인 |

증명하지 않는 것도 분명히 해 둔다. 데모 픽스처는 두 클래스가 완전히 분리되어 오분류가 0건이므로, `outcome_*` 재계산만으로는 FP/FN을 맞바꾸는 변이를 릴리스 게이트에서 잡지 못한다. 그래서 `outcome()`을 네 경우 전수로 직접 검사하는 단위 테스트를 따로 두었다. 또 이 픽스처가 쉬워 최종 용량 모델이 사실상 OCV 단독 선형회귀로 배포되므로, 중첩 선택·Ridge 경로의 실질 검증은 `tests/test_tests.py`의 별도 다변량·무신호 픽스처가 담당한다. 릴리스 실행의 수치를 중첩 선택의 성능 근거로 읽지 않는다.

`release_verification.json`에 명령, 환경, 검사 항목, 실제 시험한 Python 파일의 SHA-256이 있다. 7개 명령의 로그를 동봉했다. `01_unit_tests.log`는 개별 테스트 결과다. 실행 경로는 이식성을 위해 `{package}`, `{validation_output}`으로 표시했고, `code_sha256`과 실행 출력의 `artifact_hashes.json` 키도 POSIX 형식(`tests/verify_release.py`)이다. 패키지 폴더 안의 `.venv`/`venv`/`env`·`results`·`__pycache__`와 숨김 폴더는 해시 대상에서 제외하므로 `code_sha256` 항목은 배포된 `.py` 14개뿐이다. `verify_release.py`는 하위 프로세스를 `-X utf8 -B`로 실행한다(README §6의 안내 명령과 달리 `-B`가 붙는다. 배포 트리에 `__pycache__`를 만들지 않으려는 것이며 수치 결과는 같다). `-O`/`PYTHONOPTIMIZE` 환경에서는 검사가 통째로 사라지지 않도록 실행 자체를 거부한다. 검사가 실패하면 `release_verification.json`의 `status`가 `failed`가 되고 `error`에 실패한 검사 이름이 남는다.

## 이 기록을 만든 환경과 재현 기준

동봉 로그와 `release_verification.json`은 Linux(`Linux-6.18.44-fc-v33-x86_64-with-glibc2.39`), Python 3.12.3, NumPy 2.3.5, pandas 2.3.3, scikit-learn 1.7.2, SciPy 1.16.3, openpyxl 3.1.5, joblib 1.5.2, threadpoolctl 3.6.0, OpenBLAS 0.3.30에서 재생성했다. **랩 실제 환경인 Windows에서 같은 명령을 한 번 더 실행해 오탐이 없는지 확인한 뒤 이 기록을 갱신하는 일이 남아 있다.** 라이브러리 버전과 테스트 데이터 생성 seed는 고정했으나, 완전히 다른 OS/BLAS의 비트 단위 동일성까지 보장한 검증은 아니다.

실행 환경 비교는 `run.json`의 `versions`에 있는 `platform`·`machine`·`blas`로 한다. 다른 환경의 재현을 확인할 때는 이 값과 함께 `oof_predictions.csv`·`metrics.json`의 수치를 허용오차로 대조한다(rtol=1e-8 권장). 위 환경에서 나온 참조 수치는 다음과 같다. 전부 **가상 데이터** 점수이므로 성능 근거가 아니다.

| 실행 | 평가 | capacity Q² | capacity RMSE (Ah) | cc_frac Q² | baseline_mean Q² | logistic AUC | baseline_prior AUC |
|---|---|---|---|---|---|---|---|
| `demo` | leave_one_cell_out | 0.967054 | 5.8448e-4 | 0.975690 | −0.190083 | 1.000000 | 0.000000 |
| `raw_group` | leave_one_group_out | 0.977769 | 4.80117e-4 | 0.970633 | −0.001698 | 1.000000 | 0.500000 |
| `csv_group` | leave_one_group_out | 0.977769 | 4.80117e-4 | 0.970633 | −0.001698 | 1.000000 | 0.500000 |

`baseline_mean`의 Q²가 LOO에서만 상수 `1-(n/(n-1))²`(n=12: −0.190)이고 그룹 분할에서는 그렇지 않다는 점, `baseline_prior`의 pooled AUC가 LOO에서 구조적으로 0이 되고 그룹 분할에서는 0.5가 된다는 점이 위 표에서 그대로 확인된다. 우연 수준을 0이나 0.5로 가정하지 말고 그 실행의 `baseline_*` 행을 보라는 README §5의 설명과 같은 내용이다. `07_predict_from_saved_models`의 12셀 예측은 `review_required`가 모두 0이다.

최종 ZIP을 별도 폴더에 풀어 수행한 배포 검증 결과와 ZIP 해시는 ZIP 옆의 최종 검증 보고서에 기록한다. `MANIFEST.sha256`은 자기 자신을 뺀 모든 배포 파일의 SHA-256이며 검증 방법은 README §1에 있다. 큰 가상 실행 결과·모델 바이너리·가상환경은 ZIP에 포함하지 않았으며 `tests/verify_release.py`로 재생성할 수 있다.
