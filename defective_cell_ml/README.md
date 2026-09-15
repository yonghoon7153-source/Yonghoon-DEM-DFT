# 불량셀 머신러닝 v2.0.0

EIS 특징으로 용량을 예측하고, 지정한 용량 기준의 미달 여부를 평가하는 Python 패키지다. 원본 ZIP 검토에서 확인한 R1–R7을 반영했다. **실행 가능한 분석 코드이며, 실제 불량셀 성능을 검증한 완성 학습 모델은 아니다.** 실제 원시 측정 자료가 없어 검증에는 가상 데이터만 사용했다.

첨부 문서와 두 브랜치·litdb에서 검토한 아이디어 중 중첩 검증, 셀·배치 분리, 단순 기준선, 물리적으로 일관된 EIS 표현, 입력·실패 이력 기록을 적용했다. 자세한 근거는 `docs/METHODS_AND_SOURCES.md`, 변경 내용은 `docs/CHANGES.md`, 실행 검증은 `validation/`에 있다.

## 1. 설치하고 바로 실행하기

ZIP을 풀고 **이 README가 있는 `defective_cell_ml` 폴더에서** PowerShell을 연다. Python 3.12가 필요하며 첫 의존성 설치에는 인터넷 연결이 필요하다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -X utf8 export_for_origin.py --demo --output results\demo
```

`py` 명령이 없고 `python --version`이 3.12라면 첫 줄을 `python -m venv .venv`로 실행한다. 가상환경 활성화나 PowerShell 실행 정책 변경은 필요 없다. 기본 전체 후보 탐색은 셀 수에 따라 시간이 걸린다.

한글이 섞인 Windows 경로·파일명에서는 `-X utf8`을 붙이거나 `PYTHONUTF8=1`을 설정한다(`tests/verify_release.py`도 하위 프로세스를 `-X utf8 -B`로 실행한다). 패키지 폴더 안에 `.venv`와 `results`를 두어도 되며, 두 폴더와 `__pycache__`는 릴리스 해시 대상에서 제외된다.

받은 ZIP이 손상되지 않았는지 확인하려면 패키지 폴더에서 다음을 실행한다. `MANIFEST.sha256`은 자기 자신을 제외한 모든 배포 파일의 SHA-256을 `<해시>␣␣<POSIX 상대경로>` 형식으로 담은 목록이며, 서명이 아니므로 우발적 손상만 탐지한다.

```powershell
# sha256sum이 있으면(Git for Windows, WSL, Linux/macOS) 한 번에 대조된다
sha256sum -c MANIFEST.sha256
# 없으면 해시를 출력해 MANIFEST.sha256의 값과 대조한다
Get-FileHash -Algorithm SHA256 (Get-ChildItem -Recurse -File -Exclude MANIFEST.sha256)
```

완료되면 `results/demo/run_summary.md`와 `results/demo/results_for_origin.xlsx`를 연다. 가상 12셀의 점수이므로 실제 성능으로 인용하지 않는다. 같은 명령을 다시 실행하려면 `results/demo_02`처럼 **새 출력 경로**를 사용한다.

## 2. 실제 자료로 실행하기

### 원시 cycler TXT + EIS MPT

```powershell
.\.venv\Scripts\python.exe -X utf8 export_for_origin.py --config config.json --cycle-dir "D:\my_data\cycle" --eis-dir "D:\my_data\eis" --output results\measured_01
```

입력 폴더를 실제 경로로 바꾸고 `config.json`에서 측정 프로토콜에 맞는 cycle·구간·전류 방향·주파수 격자·셀 범위를 지정한다. 폴더 자동 스캔 모드에서는 폴더 바로 아래의 `.txt`, `.mpt`만 읽는다(아래 selection manifest 모드는 하위 폴더도 허용한다). 두 종류 파일이 셀별로 하나씩 대응해야 한다. 실제 계측기에서 기본 설정이 맞는지 한 셀의 원시 값과 추출 용량을 먼저 대조한다.

#### 원시 파일 형식 요건

아래 조건은 코드가 실제로 강제하는 것이며, 하나라도 어긋나면 첫 실행에서 거부된다. `examples/raw`의 가상 파일이 형식 참고용 최소 예다.

| 항목 | 요건 |
|---|---|
| 파일명 | 대소문자 무관 `cell<정수>` 토큰. 정규식 `cell(\d+)`의 **첫 일치**를 셀 번호로 쓴다(`cell41_0.5MPa.txt` → 41). `Cell_41`·`C41`·`41_EIS`는 거부되고, `excell2024_cell41`은 2024, `pouchcell12_cell3`은 12로 **잘못** 읽혀 셀 범위 밖 제외로 조용히 빠진다 |
| 파일명 압력 토큰 | 선택. `_<수>MPa`(예: `cell41_0.5MPa.txt`)를 `pressure_mpa`로 기록만 하며 특징·그룹·QC에는 쓰지 않는다 |
| 폴더 | 자동 스캔 모드는 폴더 **바로 아래**의 해당 확장자 파일을 전부 데이터로 본다. `readme.txt` 하나만 있어도 `missing cell<number> in filename`으로 실행 전체가 중단되므로 데이터 외 파일을 두지 않는다 |
| cycler `.txt` 구분자 | 탭. 행마다 필드 수가 일정해야 하며 꼬리 탭은 허용되지만 행별로 섞이면 `inconsistent tab-separated rows`로 거부된다 |
| cycler 헤더 | 파일 처음 **300줄** 안에 있어야 하고, 7개 열 이름이 그대로 있어야 한다: `Test Time(s)`, `Step Time(s)`, `Cycle No.`, `Step No.`, `\|Q\|(Ah)`, `Voltage(V)`, `Current(A)`. 열 이름 중복은 거부. 헤더 위의 장비 주석 줄은 무시된다 |
| cycler 단위행 | 선택. 헤더 다음 행의 `\|Q\|(Ah)`가 `Ah`, `Current(A)`가 `A`일 때만 단위행으로 보고 제거한다(대소문자·`[]()` 무시). 두 값이 모두 문자인데 그 조합이 아니면 `units row … not recognized`로 거부하므로 mAh/mA 내보내기는 Ah/A로 다시 내보낸다 |
| cycler 수치 | 소수점은 `.`만. 시간은 초 단위 숫자(`h:mm:ss` 불가), `\|Q\|`는 Ah, 전류는 A. 위반 시 오류 메시지가 위반 열·데이터 행·파일 줄 번호·원문 값을 알려 주고, 쉼표 소수점과 `h:mm:ss`는 그 사실을 따로 지적한다 |
| EIS `.mpt` | 탭 구분, 처음 300줄 안에 `freq/Hz`, `Re(Z)/Ohm`, `-Im(Z)/Ohm`이 그대로 있어야 한다. `use_ocv=true`면 `<Ewe>/V`도 필수다. `\|Z\|/Ohm` 열이 있으면 Re/Im에서 계산한 크기와의 최대 차이를 audit에 기록한다. `-Im(Z)/Ohm`은 부호를 반전해 실제 Im으로 저장한다 |
| 텍스트 인코딩 | 원시 파일과 selection manifest는 설정 `encodings` 순서(기본 `utf-8-sig` → `cp949` → `cp1252`)로 디코딩을 시도한다. 영문 로케일 EC-Lab `.mpt`(cm², °C, µF 등)는 cp1252로 읽힌다. UTF-16 'Unicode 텍스트' 내보내기는 지원하지 않는다 |

검사 범위는 열마다 다르다. `Cycle No.`·`Step No.`의 유한성과 정수성은 파일 전체 행에, 시간 단조 증가와 `Test Time(s)`·`\|Q\|(Ah)`·`Current(A)`의 유한성은 **`target_cycle` 구간에만** 적용된다. `Voltage(V)`와 `Step Time(s)`는 검사하지 않는다. 다른 cycle에 있는 결측값이 온전한 대상 cycle을 거부하지 않는다.

#### 실행 전 주파수 격자 정하기

`frequency_grid_hz`는 사전에 정하는 값이지 자동 탐지가 아니다. 한 셀의 `.mpt`에서 `freq/Hz`의 최소·최대를 먼저 확인하고, 격자가 **모든 셀 sweep의 공통 구간 안**에 들도록 잡는다. 기본 9점(0.01 Hz–1 MHz)은 예시일 뿐이며, 장비 sweep이 100 mHz–100 kHz라면 기본값으로는 반드시 실패한다. 오류 메시지는 벗어난 격자점과 측정 구간, 상대 이탈 크기를 함께 출력한다.

계측기가 요청 주파수 대신 합성된 실제 주파수를 기록하거나 단정밀도로 저장하면 끝점이 1e-8~1e-5 상대만큼 격자 밖으로 떨어질 수 있다. 오류 메시지의 상대 이탈 크기를 보고, 그 정도가 수치 표현 차이이면 `boundary_policy="clamp"`와 그 값보다 조금 큰 `max_boundary_fraction`(예: 1e-4)을 쓴다. 고정된 끝점은 `data_audit.json`의 `clamped_frequencies_hz`·`support_hz`로 확인한다. 이탈이 실제 측정 범위 부족이면 격자를 조정한다.

셀 하나라도 읽기에 실패하면 **실행 전체가 `failed`**로 끝나고, `data_audit.json`에는 실패한 셀까지만 기록된다. 남은 셀의 문제는 그 셀을 `exclude_cells`로 빼거나 설정을 고쳐 **새 출력 경로로** 다시 실행해야 드러난다.

#### selection manifest

같은 셀의 파일이 여러 개라면 사용할 파일을 `examples/selection_manifest.csv` 형식으로 명시한다. `cell_number,cycle_file,eis_file`이 필요하고, 그룹 평가에는 `batch_id`도 필요하다. 선택 사유는 `selection_reason` 등에 기록해 둘 수 있다. 실행 기록에 manifest 해시와 인코딩이 남는다.

- 셀당 한 행이며 같은 `cell_number`가 두 번 나오면 거부된다. `cell_number`는 정수여야 하고 `41.0` 형식은 41로 읽힌다.
- `cycle_file`·`eis_file`은 비워 둘 수 없다. 아직 측정이 없는 셀은 행 자체를 빼야 한다.
- 경로는 각각 입력 폴더 기준이며 하위 폴더 상대경로도 허용된다. 확장자는 검사하지 않고 파일 내용의 헤더로 검증하므로, `eis_file` 칸에 cycler `.txt`를 잘못 적으면 헤더 탐색 실패로 알게 된다. 입력 폴더 밖(`../`, 절대경로, 외부 symlink)은 거부된다.
- 파일명의 셀 번호가 `cell_number`와 달라도 거부된다. manifest가 대응을 명시해도 파일명 규칙은 그대로 강제된다.

셀당 `.mpt`가 여러 개인데 그중 EIS 필수 헤더가 없는 파일이 있으면(EC-Lab이 OCV·PEIS를 기법별 파일로 쓰는 경우) 그 파일은 `skipped_non_eis_file`로 제외되고 manifest 없이 진행된다. 한 `.mpt` 안에 sweep이 여러 번 쌓여 있으면 `data_audit.json`에 `eis_sweeps`와 경고가 남으며, `eis_sweep`으로 분석할 sweep 하나를 고른다.

```powershell
.\.venv\Scripts\python.exe -X utf8 export_for_origin.py --config examples\config_group.json --cycle-dir "D:\my_data\cycle" --eis-dir "D:\my_data\eis" --selection-manifest "D:\my_data\selection.csv" --output results\measured_group_01
```

배치 일반화가 목표라면 배치 번호를 실제 제조 이력과 연결하고 그룹 평가를 사용한다. 입력의 행 순서나 임의의 가상 그룹으로 배치를 대신하지 않는다.

### 특징 CSV가 이미 있는 경우

```powershell
.\.venv\Scripts\python.exe -X utf8 export_for_origin.py --config config.json --features "D:\my_data\features.csv" --output results\measured_csv_01
```

한 행이 셀 하나다. 같은 셀의 반복 측정을 여러 독립 표본으로 넣지 않는다. CSV 경로에서는 이미 추출된 특징의 원시 EIS 일관성이나 측정 시점을 재검증할 수 없다.

| 열 | 의미·조건 |
|---|---|
| `cell_number` | 고유 정수 셀 번호. `cell_min`/`cell_max`·`exclude_cells` 필터가 이 CSV의 학습 행에도 적용된다 |
| `cap` | 실측 용량 **Ah**. 학습에는 유한한 양수 필수. 중앙값이 `design_capacity_ah`의 1/10–10배를 벗어나면 단위 오류로 보고 거부한다 |
| `re@1000Hz`, `im@1000Hz`, `mag@1000Hz`, `phase@1000Hz` 등 | 주파수별 EIS 특징. 임피던스 Ohm, 위상 degree. 유한값 필수 |
| `ocv` | EIS 측정 중 전위의 중앙값 V. 기본 설정에서 필수 |
| `cc_frac` | 선택적 CC/전체 용량 비율, 0–1. 빈 값은 이 타깃의 평가에서만 제외 |
| `batch_id` | 그룹 평가 시 필수. 다른 열 이름은 `group_column`으로 지정 |

실행에 사용할 주파수의 열을 제공한다. 원시 변환기는 고정 격자의 네 성분을 모두 만든다. CSV에서는 일부 성분만 제공할 수 있으나 후보 대역에 실제 열이 있어야 한다. 이름은 `1000Hz`, `100000Hz`, `1e+06Hz`처럼 Python `:g` 표기다. `1kHz`는 인식하지 않는다. 열 이름은 **소문자** `mag`/`re`/`im`/`phase`이며 대소문자를 구분한다. `Mag@1000Hz`처럼 대문자로 적으면 조용히 무시되지 않고 올바른 이름을 알려 주며 거부된다(Excel 자동 대문자화 주의). 특징도 타깃도 아닌 열은 모델 특징으로 자동 사용하지 않고 `data_audit.json`에 `ignored_columns`로 기록한다.

`--features`/`--selection-manifest`에 `.xlsx`·`.xlsm`·`.xls`·`.ods`를 넘기면 거부된다. **`--features` CSV는 UTF-8(BOM 허용)로 읽는다**. 설정의 `encodings`는 원시 cycler/EIS 파일과 selection manifest에만 적용되므로, 한국어 Windows Excel에서는 "CSV UTF-8"로 저장한다.

OCV 없이 분석하려면 `examples/config_eis_only.json`을 사용하거나 설정의 `use_ocv`를 JSON 불리언 `false`로 바꾼다. OCV 결측 행을 자동 제거해 표본 수를 줄이지 않는다. 용량을 모르는 셀은 학습 CSV에서 분리해 아래 예측 경로로 보낸다.

## 3. 저장 모델로 새 셀 예측하기

```powershell
.\.venv\Scripts\python.exe -X utf8 predict.py --run results\measured_01 --features "D:\my_data\new_features.csv" --output results\new_predictions_01.csv
```

`--run`에는 사용자가 이 패키지로 만든 학습 출력 폴더, 즉 **`models/`의 상위 폴더**를 지정한다(`models/` 자체가 아니다). 상태가 `completed` 또는 `partial`인 실행만 읽는다. 새 CSV는 학습 때의 특징 열·단위가 같아야 하며 `cap`, `cc_frac` 정답은 필요 없다. **어떤 추정기도 다시 적합하지 않고** 저장된 변환·모델을 그대로 적용하며, 판정 기준도 학습 당시 설정의 `threshold_ah`·`decision_threshold`를 쓴다. 예측용 셀 번호는 학습 범위 밖이어도 가능하다. `ocv`로 학습한 모델은 예측 CSV에도 `ocv` 열이 필요하며, 저장된 번들의 `use_ocv`는 예측 시점에 바꿀 수 없다.

새 EIS 원시 파일만 있다면 먼저 특징을 만든다. 학습 실행의 `config.json`을 복사해 주파수·OCV 설정은 유지하고 새 셀 번호가 포함되도록 `cell_min`, `cell_max`, 제외 목록을 조정한다. **원시 입력 준비에도 설정의 셀 필터가 적용된다.**

```powershell
.\.venv\Scripts\python.exe -X utf8 extract_capacity.py --config new_input_config.json --eis-dir "D:\my_data\new_eis" --output results\new_features_01.csv
.\.venv\Scripts\python.exe -X utf8 predict.py --run results\measured_01 --features results\new_features_01.csv --output results\new_predictions_02.csv
```

### 예측 결과 읽기

결과 행 순서는 입력 CSV 순서를 그대로 유지한다. 플래그 열은 `True/False`가 아니라 **0/1 정수**다. 특징·타깃이 아닌 입력 메타데이터 열(`batch_id` 등)은 오른쪽에 그대로 붙는다.

| 열 | 내용 |
|---|---|
| `predicted_capacity` | 예측 용량, 단위 **Ah** |
| `predicted_capacity_mAh_cm2` | 같은 값을 `area_cm2`로 나눈 mAh/cm² 환산 |
| `capacity_predicted_defective` | 예측 용량 ≤ `threshold_ah`이면 1. **1차 판정** |
| `predicted_cc_fraction` | CC 비율 예측(그 모델을 학습할 수 있었던 경우) |
| `logistic_score`, `logistic_predicted_defective` | Logistic 점수와 `decision_threshold` 판정. **보조 확인**이며 1차 판정과 어긋날 수 있다 |
| `review_required`, `review_reason` | 재검토 필요 여부와 그 사유 문자열 |
| `{model}_outside_training_range`, `{model}_outside_features` | 모델별 범위 이탈 여부와 이탈한 특징 이름 |
| `{model}_seen_in_training` | 같은 셀 ID가 학습에 쓰였는지 |

`outside_training_range`는 학습에서 관측한 특징별 최소–최대에 상대 1e-9·절대 1e-12 허용오차를 더한 구간을 벗어날 때만 표시된다(허용오차 값은 provenance의 `range_tolerance`에 기록). 예측 CSV는 `float_precision='round_trip'`으로 읽으므로 CSV 왕복 오차만으로 재검토가 켜지지 않는다. 범위 판정 대상은 최종 모델이 고른 특징이 아니라 **학습 입력 전체 열**이므로 세 모델의 `*_outside_training_range`가 같은 값이 될 수 있다. 모델이 실제로 사용한 특징은 provenance의 `models.<모델>.selected_features`에서 확인한다.

`review_required`는 범위 이탈이나 용량/비율 출력의 물리 범위 위반(용량 ≤ 0, CC 비율 0–1 밖)을 표시한다. 이는 검증된 OOD 탐지기·불확실성 구간·재검사 최적 정책이 아니다. 범위 안이라는 이유로 예측이 신뢰할 만하다고 확정하지 않는다.

`cc_fraction_seen_in_training`은 `cc_frac` 값이 있던 학습 셀만 1이므로 `capacity_seen_in_training`과 다를 수 있다. `seen_in_training`은 **셀 ID 비교일 뿐**이다. 같은 특징에 새 번호를 붙인 셀(동봉 예제 61–72)은 모두 0으로 나오며, 반대로 1인 행에는 전체 자료 적합 모델의 in-sample 예측값이 표시 없이 그대로 나온다. 그 값은 OOF 지표보다 낙관적이므로 독립 성능 근거로 쓰지 않는다.

학습 설정의 `cell_min`/`cell_max`·`exclude_cells`는 **예측 경로에 적용되지 않는다**(원시 준비 단계 `extract_capacity.py`에서만 적용). QC로 제외한 셀을 예측 CSV에서 빼는 것은 사용자 책임이다.

### 무결성·환경 검사와 출처 기록

예측은 `models/*.joblib`를 읽기 전에 학습 폴더의 `artifact_hashes.json`과 대조하고, `capacity`·`cc_fraction`·`logistic` 이외 이름의 모델 파일이나 해시 불일치를 종료 코드 2로 거부한다. 실행 폴더에서 모델만 복사·개명하지 말고 **폴더 전체를 옮긴다**. 손상되었거나 이 패키지가 만들지 않은 번들도 설명 메시지와 종료 코드 2로 끝난다(추적 역추적 출력 없음).

학습 실행의 의존성 버전과 현재 설치 버전을 비교한다. scikit-learn 주·부 버전이 다르면 종료 코드 2로 멈추며, `requirements.lock.txt`로 맞추거나 `--allow-version-mismatch`를 명시해야 한다. 나머지 버전 차이와 모델 로드 경고는 경고로 출력되고 provenance의 `version_mismatch`·`warnings`에 기록된다.

학습 실행이 `partial`이면 상태와 `unavailable` 사유를, 저장되지 않은 모델이 있으면 그 이름을, 합성 데모 데이터로 학습한 모델이면 그 사실을 화면에 출력한다. `unavailable`의 `<name>_deployment_model` 키는 '지표는 계산됐지만 전체 자료 배포 모델만 없다'는 뜻이며 그 경우 `models/`에 해당 joblib이 없다.

`<output>.provenance.json`에 실행 폴더 경로, `run.json`·`config.json`·모델 파일 해시, 학습/예측 환경 버전과 차이, 실행 상태와 `unavailable`, 없는 모델 목록, 모델별 추정기·선택 특징·학습 셀 수, 임계값, 열 단위, 범위 허용오차, 재검토 셀 수가 기록된다.

예측이 실패하면 결과 CSV와 provenance가 남지 않으므로 원인을 고친 뒤 **같은 `--output` 경로로** 다시 실행할 수 있다. 실패 산출물을 보관하는 규칙은 학습 출력 폴더에만 해당한다.

### 모델 파일을 다루는 규칙

Joblib 모델은 자신이 생성했거나 신뢰하는 로컬 실행 결과만 읽는다. joblib은 pickle 기반이라 **파일을 읽는 시점에 그 안의 코드가 실행되며**, 해시 대조와 이름 제한은 무결성 확인일 뿐 역직렬화 위험 자체를 없애지 않는다. 출처가 불분명한 실행 폴더를 `--run`에 지정하지 않는다.

번들에는 이 패키지의 커스텀 `FeatureSelector`가 들어 있어 `ridge_capacity`를 import할 수 있어야 로드된다. 즉 **패키지 폴더에서 `predict.py`로 실행**해야 하며, 결과 폴더만 다른 프로젝트로 옮겨 직접 `joblib.load`하면 `ModuleNotFoundError`가 난다. 모델을 다시 읽을 때도 동일한 의존성 버전을 사용한다. ZIP에는 실제 학습 모델을 넣지 않았다.

## 4. 설정과 용량 정의

설정 파일의 생략 항목은 기본값을 사용하고 알 수 없는 키는 거부한다. 전체 기본값은 `config.json`에 있으며 아래 표가 `Config`의 전체 항목이다(JSON에 주석을 넣을 수 없어 설명은 이 표에만 있다).

| 설정 | 기본값 | 허용값·동작 |
|---|---|---|
| `threshold_ah` | 0.01802088 | 이 값 **이하**를 1(불량), 초과를 0으로 정의. 양수이며 `design_capacity_ah`보다 작아야 함 |
| `design_capacity_ah` | 0.0200232 | 설계 용량 Ah. 기본 임계값은 이 값의 90%. `area_cm2` 3.24 cm² × 6.18 mAh/cm²에서 나온 값이지만 두 필드는 독립이라 면적만 바꿔도 따라가지 않는다 |
| `cap_plausibility_factor` | 10.0 | 1보다 커야 함. `cap` 중앙값이 `design_capacity_ah`의 1/10배–10배(이 설정값 기준) 구간을 벗어나면 단위 오류로 보고 학습을 중단 |
| `area_cm2` | 3.24 | 양수. 표시용 Ah→mAh/cm² 환산에만 사용 |
| `cell_min` | 34 | 0 이상 정수. 양끝 포함 |
| `cell_max` | 98 | 0 이상 정수, `cell_min` 이상. **34–98은 원본 실험에서 승계된 값이므로 새 실험에서는 반드시 조정한다** |
| `exclude_cells` | `{}` | 셀 ID→사유 매핑. 키는 선행 0 없는 정수 문자열, 값은 비어 있지 않은 사유 문자열. 예: `{"60":"측정 전 확정한 QC 제외 사유"}`. 원본의 60·70·93 제외는 사유 미확인으로 자동 승계하지 않음 |
| `frequency_grid_hz` | 0.01–1e6 Hz 9점 | 양의 유한값 목록, 중복 없이 증가. decade당 1점이며 모든 셀 sweep의 공통 구간 안이어야 한다 |
| `boundary_policy` | `error` | `error`: 측정 범위 밖 격자는 거부. `clamp`: `max_boundary_fraction`까지 끝값 고정 |
| `max_boundary_fraction` | 0.05 | `[0, 0.1]` 구간. 경계의 **선형** 상대 차이 기준이며 고정한 점은 audit에 기록 |
| `duplicate_frequency_policy` | `error` | `error` 또는 `mean`. `mean`은 같은 주파수의 복소 성분을 평균하며 **같은 상태의 반복 측정에만** 쓴다 |
| `mean_max_ewe_spread_v` | `null` | `null` 또는 0 이상 실수. `mean`일 때 같은 주파수의 `<Ewe>` 폭이 이 값을 넘으면 서로 다른 상태의 평균이므로 거부 |
| `eis_sweep` | `all` | `all`·`first`·`last` 또는 0 이상 sweep 색인. 한 `.mpt`에 sweep이 여러 번 쌓였을 때 분석할 하나를 고른다. `all`이면 경고만 남는다 |
| `target_cycle` | 1 | 0 이상 정수. 용량을 읽을 cycle |
| `target_step_i` | 1 | 0 이상 정수. 해당 cycle 안의 연속 구간 색인이며 **0부터 시작**하므로 기본값은 두 번째 구간 |
| `target_raw_step` | `null` | `null` 또는 0 이상 정수. 지정하면 원시 `Step No.`로 구간을 고르고 `target_step_i`를 대신한다. 그 번호가 여러 구간에 나타나면 거부 |
| `expected_current_sign` | `positive` | `positive` 또는 `negative`. 충전이 음수인 장비는 `negative`. 구간 안에 0 A나 역부호 행이 있으면 셀이 거부된다 |
| `cv_relative_drop` | 0.01 | `(0, 1)`. 기준 전류 대비 이만큼 이상 내려간 상태를 CV 전환으로 본다 |
| `cc_reference_rows` | 5 | 1 이상 정수. 구간 **초반 이 행 수의 중앙값**을 기준 전류(plateau)로 삼는다 |
| `cc_sustained_rows` | 3 | 1 이상 정수. 하락이 이 행 수만큼 연속 유지되거나 구간 끝까지 이어져야 전환으로 인정한다 |
| `trim_zero_current_boundary_rows` | `false` | 스텝 시작/cut-off 종료에 0 A 로깅 행을 남기는 장비에서만 `true`. 제거된 행은 audit에 기록. 기본값에서는 구간 안 0 A 행이 곧 거부이므로 rest 행은 별도 `Step No.`여야 한다 |
| `use_ocv` | `true` | JSON 불리언. `true`면 OCV 포함/미포함 후보를 동일한 완전 관측 셀 집단에서 비교하고 `.mpt`에 `<Ewe>/V`를 요구 |
| `outer_cv` | `leave_one_cell_out` | `leave_one_cell_out` 또는 `leave_one_group_out` |
| `group_column` | `batch_id` | 비어 있지 않은 열 이름. 그룹 평가와 manifest의 그룹 열 이름 |
| `inner_splits` | 3 | 2 이상 정수이며 **설정값이 상한**이다(3은 기본값일 뿐 강제 상한이 아니다). 실제 fold 수는 `min(inner_splits, 학습 셀 수 \| 소수 클래스 셀 수 \| 학습 그룹 수)`로 축소되고, 2 미만이 되면 해당 타깃이 `unavailable`이 된다 |
| `seed` | 2026 | uint32 범위의 0 이상 정수. 안쪽 fold 셔플과 Logistic에 사용 |
| `ridge_alphas` | `[0.001 … 1000]` 7개 | 양의 유한값 목록, 중복 없음. Ridge 후보의 정규화 강도 격자 |
| `logistic_cs` | `[0.001 … 10]` 5개 | 양의 유한값 목록, 중복 없음. Logistic의 `C` 격자 |
| `logistic_class_weight` | `balanced` | `balanced` 또는 `null`. 학습은 균형 가중, 안쪽 선택은 **비가중** log loss, 판정선은 `decision_threshold`로 서로 다른 세 요소다 |
| `decision_threshold` | 0.5 | `(0, 1)`. Logistic 판정선. 바깥 평가 정답으로 최적화하지 않음 |
| `feature_sets` | 4개 전부 | `single_1e3`(1 kHz), `band_1e3_1e5`(1e3–1e5 Hz), `band_low`(0.1–10 Hz), `full`(전체)의 비어 있지 않은 부분집합. 사용자 정의 대역은 지원하지 않는다 |
| `encodings` | `["utf-8-sig","cp949","cp1252"]` | 비어 있지 않은 **텍스트** 코덱 목록(zlib·base64 등 바이트 코덱은 거부). 원시 파일과 selection manifest에만 적용 |

설정 오류는 어긴 키·값·허용 범위를 그대로 알려 준다(예: `max_boundary_fraction=0.2 must be within [0, 0.1]`).

### 용량과 CC/CV 판정

cycler 입력은 필수 열을 헤더에서 탐색하고 확인된 단위행만 제거한다. 시간 역전, 잘못된 전류 부호, 비유한 값, 감소하는 선택 구간 누적 용량을 거부한다. 용량은 선택 구간의 마지막 `|Q|(Ah)`다. 그 값이 구간 누적 용량으로 정의되는 장비인지 확인해야 한다. 시작 용량을 빼거나 전류를 적분하는 방식은 아니다. 구간 첫 `|Q|` 값은 `data_audit.json`의 `initial_capacity_ah`에 남으므로 누적 기준이 시험 시작이면 여기서 드러난다.

CC 전환 판정은 구간 **초반 `cc_reference_rows`행의 중앙값**을 기준 전류로 잡고, 그 기준보다 `cv_relative_drop` 이상 낮은 상태가 `cc_sustained_rows`행 연속으로 유지되거나 구간 끝까지 이어지는 **첫 행**을 찾는다. 단일 행의 노이즈나 초반 오버슈트 한 점이 전환을 만들지 않는다. CC 용량은 그 행까지의 용량이고 CV 용량은 전체와의 차이이며, 하락이 없으면 CC=전체로 둔다. `data_audit.json`에 선택한 구간, 행 수, 첫 용량, 전환 지점(`cv_first_below_index`), 기준 전류(`cc_reference_current_a`), plateau 최대 상대 편차(`cc_plateau_max_relative_deviation`)를 기록한다. `cc_frac`이 0.2 미만이면 `warning` 이벤트가 남는다.

이 휴리스틱이 실제 충전 프로토콜의 CC→CV 전환과 맞는지는 원시 장비 이력으로 확인해야 한다. 장비가 CC와 CV를 **별도 `Step No.`로 기록**하면 이 추출기는 한쪽 구간만 읽어 `cap`이 과소평가되고 `cc_frac`이 1.0으로 고정된다. 이 경우 audit에 `next_segment_continues_charge` 경고가 남으며, 총 충전 용량은 외부에서 계산해 `--features` CSV로 넣거나 `target_raw_step`으로 맞는 구간을 지정한다.

### 라벨 정의의 한계

기본 설정(`target_cycle=1`, `target_step_i=1`, `expected_current_sign='positive'`)의 라벨은 **1주기 충전 용량**이다. 황화물 ASSB의 첫 충전은 SE 산화·CEI 형성 같은 비가역 용량을 포함하므로, 부반응이 큰 셀일수록 충전 용량이 커져 가역(방전) 용량 기준으로는 불량인 셀이 '정상'으로 분류될 수 있다. 미세 단락도 같은 방향으로 용량을 부풀린다. 방전 용량을 기준으로 삼으려면 `target_step_i`(또는 `target_raw_step`)와 `expected_current_sign='negative'`로 방전 구간을 지정한다. 설계 용량의 1.5배를 넘는 셀은 `data_audit.json`에 `warning`으로 표시되지만 제외되지는 않는다.

임계값은 모든 셀에 같은 절대 Ah이므로 활물질 칭량 편차(±3–5%)가 그대로 라벨에 들어간다. 파이프라인에 셀별 질량 입력은 없다.

### EIS 표현과 측정 조건

`-Im(Z)/Ohm`은 부호를 반전해 실제 Im으로 저장한다. Re/Im을 로그 주파수에서 선형 보간하고, 그 결과로 크기와 위상을 계산한다. 격자점당 열은 4개지만 `mag`·`phase`는 `re`·`im`의 결정적 함수이므로 **자유도는 2**다. 원시 sweep 밀도가 낮으면 보간 오차가 커지므로 decade당 6점 이상을 권장한다(`data_audit.json`의 `raw_rows`와 `support_hz`로 확인). decade당 1점 격자는 반원 정점을 직접 담지 못하는 저해상도 표현이며, 고정 4개 대역 밖(예: 10–1000 Hz 단독)을 후보로 넣을 수는 없다. 자세한 한계는 `docs/METHODS_AND_SOURCES.md`에 있다.

`<Ewe>/V` 중앙값(`ocv`)이 평형 OCV와 동일하다고 자동 가정하지 않는다. EC-Lab PEIS(E vs Eoc=0)에서 이 값은 sweep 시작 시점의 전위와 사실상 같고, GEIS이면 sweep 동안의 이완 드리프트가 섞인다. 더 중요한 것은 **프로토콜 의존성**이다. EIS를 '고정 Ah 충전 후'나 '충전 직후 휴지 없이' 측정하면 OCV가 SOC 판독값이 되어 용량과 트리비얼하게 상관하므로(측정 프로토콜 누수), 대신 cut-off까지 충·방전한 뒤 충분히 휴지하고 측정하면 용량 정보는 거의 남지 않는다. EIS 측정 시점과 SOC 정의를 실험 계획에 먼저 고정하고, 그 정의를 결과와 함께 기록한다. SOC·온도·압력도 실제 자료 수집 단계에서 관리해야 한다. 동봉 가상 데이터는 `ocv`에 라벨을 직접 넣어 만들었으므로, 데모에서 용량 모델이 OCV 단독으로 선택되는 것은 소프트웨어 동작 확인일 뿐 물리적 근거가 아니다.

## 5. 모델과 결과 해석

바깥 셀/배치를 남긴 뒤, 안쪽 학습 자료로만 대역·OCV 포함 여부·정규화 강도를 선택한다. StandardScaler도 각 학습 fold 안에서 적합한다. 선택 후 바깥 셀을 한 번 예측하고, 전체 바깥 예측(OOF)을 모아 지표를 계산한다.

회귀 후보는 평균 기준선, `|Z|@1 kHz` 선형회귀, OCV 단독 선형회귀, 대역별 Ridge다. CC 비율도 같은 선택 구조다. Logistic은 대역과 C를 안쪽 **log loss**로 선택한다. 한 셀 fold의 AUC로 C를 고르지 않는다. AUC는 양성·음성이 있는 전체 OOF 점수에서 계산한다. Logistic 출력은 확률 보정을 검증하지 않은 모델 점수다.

후보 대역은 1 kHz, 1–100 kHz, 0.1–10 Hz, 전체이며 입력에 존재하는 열을 사용한다. `single_1e3` 후보와 `|Z|@1 kHz` 기준선은 격자에 **정확히 1000 Hz**가 있을 때만 생성되고, `band_low`는 0.1–10 Hz, `band_1e3_1e5`는 1e3–1e5 Hz 열을 요구한다. 열이 없으면 실행이 실패하는 대신 조용히 제외되고 `metrics.json`의 `skipped_candidates`와 `run_summary.md`의 '제외된 후보·기준선' 절에 기록된다. 회귀 선택 점수는 MSE다. 최종 표는 이 선택 절차의 성능과 사전 고정 단순 기준선을 보여 준다. 표에서 다시 가장 좋은 모델을 고르면 추가 독립 평가가 필요하다.

평가 후 전체 적격 자료로 선택·재적합한 모델은 배포/예측용으로 별도 저장하며 그 훈련 점수를 검증 성능으로 쓰지 않는다. 이 재적합은 바깥 fold보다 **안쪽 학습 자료가 크므로** 선택 절차가 바깥 fold와 완전히 같지 않고, 배포 모델이 어느 바깥 fold의 선택과도 다른 후보가 될 수 있다(중첩 CV의 성질). fold별 선택 빈도와 최종 선택은 `run_summary.md`에, 자세한 기록은 `folds.json`·`deployment_fit.json`에 있다.

용량 미달 라벨은 안전 결함·수명·불량 원인을 자동 판별하지 않는다. 셀 수가 적으면 중첩 CV를 해도 불확실성이 크다. 실행 최소 4셀, 그룹 평가 최소 3그룹은 통계적 충분성 기준이 아니다. 분류는 모든 필요한 학습/검증 분할에서 클래스 수가 충족되어야 한다. 구체적으로 `leave_one_cell_out`에서는 **소수 클래스가 3셀 이상**이어야 한다(소수 클래스가 m셀이면 그 셀을 남긴 바깥 fold의 학습 분할에는 m−1셀만 남고, 안쪽 분할에 2셀 이상이 필요하다). 그룹 평가에서는 모든 안쪽 분할의 학습·검증 양쪽에 두 클래스가 있어야 하므로 조건이 더 엄격하다. 불가능하면 그룹을 쪼개지 않고 해당 항목을 `unavailable`로 남긴다. `cc_frac` 값이 하나도 없거나 4셀 미만이면 그 사유가 `unavailable['cc_fraction']`에 그대로 기록된다.

### 지표를 읽는 법 — 우연 수준은 0이나 0.5가 아니다

모델 행은 0이나 0.5가 아니라 같은 실행의 `baseline_*` 행과 비교한다. `baseline_*` 중 **우연 수준**은 특징을 전혀 쓰지 않는 `baseline_mean`(회귀)과 `baseline_mean_threshold`·`baseline_prior`(분류)이고, `baseline_mag@1000Hz`·`baseline_ocv` 계열은 우연 수준이 아니라 사전에 고정한 단순 모델 기준선이다.

- `leave_one_cell_out`에서 평균 기준선(`baseline_mean`)의 Q²는 자료와 무관한 상수 `1-(n/(n-1))²`다(n=12면 −0.190). Q²의 무정보 기준은 0이 아니라 이 값이므로, 음수라는 사실만으로 모델이 기준선보다 나쁘다고 읽지 않는다.
- pooled OOF AUC는 fold별 평균이 아니라 바깥 OOF 예측을 한 벡터로 모아 계산한다. 그래서 우연 수준이 정확히 0.5가 아니고 소표본에서는 0.5 아래로 치우친다. LOO에서 `baseline_mean_threshold`와 `baseline_prior`의 pooled AUC는 구조적으로 **0**이 된다(한 셀을 뺄 때마다 나머지 평균·사전확률이 그 셀의 라벨과 반대로 움직이기 때문). 그룹 평가에서는 이 상수가 성립하지 않으므로(동봉 3배치 예제에서는 0.5) 언제나 그 실행의 `baseline_*` 값을 그대로 기준으로 쓴다. **0.5 미만 값을 신호가 뒤집혔다는 뜻으로 읽지 않는다.**
- 분류 표의 우연 수준은 `baseline_prior` 행과 `08_label_summary`의 불량/정상 셀 수로 판단한다.
- `06_clf_metrics`의 두 모델 행은 작동점이 다르다. `capacity_threshold`는 고정 용량 임계값 규칙이고 `logistic_nested_selection`은 균형 가중 확률의 `decision_threshold` 판정이다. MSE로 선택된 회귀 예측은 평균으로 수축하므로 불량이 소수이면 임계값 판정의 민감도가 0으로 붕괴할 수 있다. 두 행의 민감도·F1·MCC를 직접 비교하지 말고 순위 비교는 `AUC_pooled_OOF`와 `05_clf_roc`로 한다.
- `logistic_class_weight='balanced'`는 확률을 재가중하므로 보고되는 `log_loss`/`brier_score`가 사전확률 기준선보다 나쁠 수 있다. 같은 행의 `log_loss_prior_baseline`/`brier_prior_baseline`이 그 기준이다.
- `metrics.json`의 `diagnostics`에 `degenerate`(바깥 OOF 확률이 0.5 부근에서 거의 상수 — 선택된 모델이 아무것도 분리하지 못함)와 `boundary`(`logistic_cs` 격자 끝에서 C가 선택된 fold가 절반 이상)가 기록된다.
- 보고 지표는 **pooled OOF 점추정치뿐**이며 fold 분산·신뢰구간·라벨 순열 p-value를 제공하지 않는다. n이 10 내외면 순수 잡음에서도 Q²가 양수, AUC가 0.8 이상 나올 수 있으므로 외부에 인용하기 전에 라벨 순열 검정이나 셀 단위 부트스트랩을 별도로 수행하고 반드시 `baseline_*` 행과 함께 제시한다.

같은 문구가 `metrics.json`의 `notes` 키와 `run_summary.md`의 지표 요약표 아래에도 들어 있다.

### 결과 파일

| 결과 | 내용 |
|---|---|
| `run_summary.md` | 지표 요약표, 우연 수준 설명, fold별 선택 빈도와 전체 자료 적합, EIS 미사용 경고, 모델 진단, 제외된 후보·기준선, 계산하지 못한 항목 |
| `oof_predictions.csv` | 셀별 실측·독립 평가 예측·잔차·판정과 기준선 예측 |
| `regression_metrics.csv`, `classification_metrics.csv` | Q²/RMSE/MAE, 혼동행렬·민감도·특이도·pooled AUC 등. `baseline_*` 기준선 행 포함 |
| `results_for_origin.xlsx` | 기존 시트명 11개 유지. 열 구조는 v2의 정리된 표로 변경 |
| `folds.json` | 안쪽/바깥 셀·그룹, 선택 모델·특징·점수, 표준화 평균 |
| `deployment_fit.json`, `models/` | 평가 뒤 전체 자료 적합 이력과 예측용 모델(번들에 `selected_features`·`versions` 포함) |
| `input_features.csv`, `data_audit.json` | 사용 특징과 제외·입력 처리 이력. 학습 실행의 `data_audit.json`은 이벤트 배열이다 |
| `metrics.json` | 위 두 지표표에 더해 `unavailable`, `skipped_candidates`, `diagnostics`, `notes` |
| `run.json`, `config.json`, `artifact_hashes.json` | 버전·환경(platform·machine·BLAS 포함)·입력/소스 해시·설정·`headline`·출력 무결성 |

Excel 시트에서 `03_reg_coefs`는 선택 결과에 따라 비어 있을 수 있다(용량 모델이 OCV 단독이면 EIS 계수 행이 없다). `04_reg_residual`에는 `pred_cc_frac`이 포함되고, `05_clf_roc` 첫 행의 임계값은 무한대라 공란이며, `06_clf_metrics`·`10_confusion_matrix`에는 `baseline_*` 행이 함께 들어간다. `score_capacity_threshold`는 양수일수록 임계값 미달 예측이다. 수식처럼 보이는 문자열은 값을 바꾸지 않고 문자로 저장한다(Excel이 표시하는 인용 접두는 값의 일부가 아니다).

`artifact_hashes.json`은 **해당 실행 출력의 무결성 확인용**이다. 실행 간 재현 비교는 `oof_predictions.csv`·`metrics.json`·`folds.json` 등 수치 파일로 한다(`results_for_origin.xlsx`와 `run.json`은 시각 정보를 포함해 바이트가 달라진다).

`Q2`는 전체 OOF의 `1-SSE/SST`이며 음수가 가능하다. 표준화 계수는 전체 자료 최종 적합 값으로 인과 중요도가 아니며, 한 주파수의 네 성분은 자유도 2의 중복 표현이라 개별 계수가 식별되지 않는다. MAPE는 절댓값 0.001 이상인 타깃에서만 계산하므로 0에 가까운 CC 비율에서는 RMSE/MAE를 먼저 본다. 회귀 RMSE/MAE의 기본 단위는 타깃 단위다.

`run.json`의 `config_path`·`input_csv.path`·`selection_manifest.path`와 실패 시의 `error_traceback.txt`에는 **입력 파일의 절대경로**가 들어가고, `data_audit.json`의 `eis_file`·`cycle_file`에도 입력 경로가 그대로 남는다(manifest 모드에서는 절대경로). 출처 추적을 위한 의도적 기록이므로 결과 폴더를 외부에 통째로 전달하기 전에 계정명·폴더 구조 노출 여부를 확인한다. `results_for_origin.xlsx`·CSV 결과표·joblib 번들에는 경로가 없다.

### 종료 코드와 사이드카 파일

세 CLI 모두 입력·설정 오류는 stderr에 `Input error:`(predict는 `Prediction error:`) 한 줄과 **종료 코드 2**로 끝난다. 정상 완료와 부분 완료는 종료 코드 0이다.

프로세스 종료 코드 0은 실행 완료이며 일부 선택 타깃을 계산할 수 없는 `partial`도 포함한다. `run.json`의 상태와 `unavailable`을 함께 확인한다. 안쪽 적합이 수렴하지 않으면(`Inner fit did not converge`) 실행 전체가 실패하지 않고 그 타깃만 `unavailable`이 된다. 전체 자료 배포 모델 적합만 실패한 경우도 `<name>_deployment_model` 키로 남고 실행은 `partial`로 완료된다. 필수 입력·용량 평가 실패는 종료 코드 2와 `failed` 상태로 기록한다. 실패 출력 폴더도 원인을 조사할 때까지 보관한다. 입력 인자/설정 자체가 잘못된 경우 출력 폴더 생성 전에 종료할 수 있다.

각 CLI는 주 출력 옆에 사이드카 파일을 만든다. `extract_capacity.py`는 `<output>.audit.json`을 **성공·실패 모두** 만들며 내용은 `{version, status, config, selection_manifest, events}` 객체다. `predict.py`는 `<output>.provenance.json`을, `export_for_origin.py`는 실패 시 출력 폴더의 `error_traceback.txt`를 남긴다. 출력 파일이나 사이드카가 이미 있으면 새 경로를 지정해야 한다.

## 6. 테스트와 파일 구성

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 tests\verify_release.py --output results\release_check
```

첫 명령은 131개 자동 테스트다(입력 판독, 누수 방지, 그룹 분리, 지표·보고, 예측 계약, 릴리스 검사 자체의 시험). 테스트는 패키지 폴더가 아니라 시스템 임시 폴더에 작업 폴더를 만들므로 패키지를 읽기 전용 위치에 두어도 실행된다. 두 번째는 전체 기본 데모와 원시/CSV 실행, 원시 판독기의 값 복원, 재현성, 새 특징 준비, 저장 모델 예측을 7개 명령·7개 검사로 확인한다. 예제는 이미 들어 있어 재생성하지 않아도 된다. 검증 결과는 실제 데이터 성능을 뜻하지 않는다. 자세한 내용은 `validation/README.md`에 있다.

`export_for_origin.py`가 메인 학습·검증 실행점이다. `extract_capacity.py`는 학습 없는 입력 변환, `predict.py`는 저장 모델 추론이다. `ridge_capacity.py`와 `feature_band_test.py`의 직접 실행은 메인 CLI를 호출한다. `config.py`, `demo.py`는 공통 설정/가상 입력을 제공한다. import 시 분석 실행이나 외부 출력 폴더 생성은 하지 않는다.
