# 불량셀 ML v2.0.0 — 3차 리뷰·반박·갱신

검토일: 2026-09-15 · 브랜치 `review/defective-cell-ml-v2.0.0`

대상: `불량셀_머신러닝_최종_v2.0.0.zip`
SHA-256 `644ca806014d48d9939f0441c3fccc50771236a555f87a05239ba75f8015fe95`, 177,862 bytes, 87개 파일.

**결론: 치명적 결함도 정보 누수도 없다.** 원래 high로 분류했던 6건은 반박 검증에서 전부 medium 이하로 내려갔고
2건은 기각됐다. v2는 v1 대비 실질적 개선이며, 남은 것은 실측 자료를 처음 넣을 때의 견고성과 검증 체계의 공백이다.

## 1. 검토 방법

먼저 Codex의 주장을 재확인했다. ZIP을 새 폴더에 풀어 Linux/Python 3.12.3 + `requirements.lock.txt` 고정 버전으로
실행한 결과 단위 테스트 34개 통과, `tests/verify_release.py` 7단계 통과, `MANIFEST.sha256` 86개 파일 일치로
**주장은 모두 사실이었다.**

그다음 3단계로 진행했다.

| 단계 | 방법 | 산출 |
|---|---|---|
| 1차 훑기 | 11개 독립 관점(정확성, ML 방법론·누수, 실측 파일 입력, 전기화학 타당성, 예측 경로, 테스트 적정성, 문서 일치, 보안·공급망, 재현성·이식성, 사용성)이 각자 코드를 읽고 프로브를 실행 | 원시 119건 |
| 통합 | 파일 그룹별로 중복 병합, 교차 파일 병합, 행 번호 재확인 | 최종 80건 (F01–F80) |
| 반박 검증 | 항목마다 회의론자·재현자·영향판정자를 독립으로 붙여 실제 실행으로 판정. note 등급 23건은 원본 소스 직접 대조로 사실 확인 | 판정 80건 |

훑기 단계는 의도적으로 공격적으로 보게 했고, 반박 단계가 등급을 조정했다. 아래 등급 이동이 그 결과다.

| 원래 → 최종 | 건수 |
|---|---:|
| high → medium | 6 |
| medium → medium | 9 |
| medium → low | 19 |
| low → low | 22 |
| low → note | 5 |
| note → note | 17 |
| 기각 | 2 |

최종 분포는 **medium 15, low 41, note 22, 기각 2**다.

## 2. 누수가 없다는 근거

"누수 없음"은 코드를 읽어서만 내린 판단이 아니다. 세 가지로 확인했다.

**첫째, 구조 확인.** `candidate_grid`는 열 이름만 사용하고, `StandardScaler`·대역·OCV 포함 여부·alpha·C 선택이
전부 `GridSearchCV` 안쪽(바깥 학습 분할)에서 일어난다. 임계값·코호트 필터·`cc_frac` 마스크는 설정과 결측으로만
결정된다. 바깥 평가 셀의 정답이 선택에 참여하는 경로를 찾지 못했다.

**둘째, 무신호 실험.** 순수 잡음 특징으로 12 seed씩 돌린 결과다.

| 실험 | pooled Q² 평균 | AUC 평균 |
|---|---:|---:|
| 잡음 n=40, LOO | −0.214 | 0.472 (logistic) / 0.370 (임계값) |
| 잡음 n=40, LOGO 4배치 | −0.243 | 0.394 / 0.400 |
| 데모 12셀 라벨 순열 20회 | −0.671 | 0.447 / 0.243 |

**낙관 편향이 아니라 체계적 비관 편향(LOO 인공물)이 나온다.** 누수가 있었다면 반대 방향이어야 한다.

**셋째, 반증.** `select_model`에 바깥 test 셀까지 넘기는 진짜 누수 변이를 주입하면
`test_outer_target_cannot_change_its_own_training_selection`,
`test_scaler_and_inner_folds_use_outer_training_only`, `test_nested_group_separation` 세 개가 즉시 실패한다.
R5의 핵심은 기존 테스트가 실제로 구속하고 있다.

## 3. 우리가 틀렸던 것

리뷰가 스스로 기각하거나 정정한 항목이다.

**F05 — 원인 귀속이 틀렸고 제안했던 수정은 개악이었다.** 처음에 `class_weight='balanced'`가 pooled LOO AUC의
하향 편향을 증폭하니 기본값을 `null`로 바꾸라고 썼다. 반대다. `balanced`는 `weight_c = n/(2·count_c)`이므로
어느 셀을 남기든 각 클래스 총가중치가 `(n−1)/2`로 같아져 LOO의 prior-shift 성분을 오히려 제거한다.
두 관점이 독립으로 반복 측정해 확인했다.

| 조건 | balanced | None |
|---|---:|---:|
| 잡음 n=40, 60 seed | 0.424 | 0.357 |
| 잡음 n=65, 30 seed | 0.483 | 0.434 |
| 격자 하한 C=0.001, 30 seed | 0.430 | **0.000 (30/30 seed)** |

C가 격자 하한이면 `None`은 계수가 거의 0이라 절편의 prior shift만 남아 순위가 라벨과 완전히 역전된다.
**`logistic_class_weight` 기본값은 `'balanced'`로 유지해야 한다.** 편향의 본체는 가중치가 아니라 LOO 확률을
한 벡터로 pooling하는 것 자체이며, 클래스 가중치가 개입하지 않는 `capacity_threshold`의 편향(0.370)이
logistic(0.472)보다 더 컸다는 점이 이를 뒷받침한다. 남는 실질은 README 설명 공백 하나다.

**F54 기각.** "소표본에서 안쪽 fold가 2~4셀인데 경고가 없다"는 틀렸다. `outer_splits`의 오류 문구
(`this is an execution minimum, not evidence of adequacy`)와 README §5가 이미 같은 취지를 적었고,
`folds.json`이 fold별 `training_cells`와 선택된 36개 열 이름을 전부 기록한다.

**F62 기각.** "100 kHz–1 MHz 특징이 지그 인덕턴스에 오염된다"는 측정 위생 조언이지 코드 결함이 아니다.
격자는 사용자 설정이고 `boundary_policy='error'`가 측정하지 않은 주파수를 이미 거부한다.
`outside_training_range`가 지그 교체 시 발동하는 것도 오탐이 아니라 의도된 OOD 신호다.

**F33 서술 정정.** "원시 파일을 편집해야 한다"는 틀렸다. `--features` CSV 경로가 1급 입력이다.

**F02 표현 정정.** "릴리스 게이트가 실행 완료만 보증한다"는 과장이었다. 게이트는 raw/CSV 두 경로의 OOF 동일성,
중첩 CV 그룹 비중복, artifact 해시 무결성을 실제로 검증한다. 빠진 건 값의 **방향·부호** oracle이다.

## 4. 중간 등급 15건

### 4.1 실측 자료를 처음 넣을 때

**F32 — cp1252 EC-Lab 헤더를 읽지 못한다.** 기본 `encodings=['utf-8-sig','cp949']`가 `cm²`(0xB2 뒤 CR)를
디코딩하지 못하고, `load_raw`에 셀 건너뛰기 경로가 없어 한 파일이 전체 실행을 중단시킨다. 반대로 `Cs/µF`처럼
뒤가 ASCII면 cp949가 "성공"해 헤더가 조용히 mojibake가 되고 audit에 `cp949`라는 틀린 출처가 남는다.
수치 열은 전부 ASCII라 결과 오염은 없다.

**F33 — CC/CV가 별도 Step으로 기록되면 용량이 잘린다.** 8시간 CC + 2시간 CV를 Step 20/21로 나눈 픽스처에서
`cap`이 0.018978에서 0.017879로 5.79% 과소평가되고, 기본 임계값 0.01802088을 기준으로 **같은 셀의 라벨이
정상에서 불량으로 뒤집혔다.** `cc_frac`은 1.0으로 고정되고 경고가 없다. `target_step_i=[1,2]`는 `DataError`라
설정으로 합칠 방법이 없다.

**F06 — CC/CV 전환 판정이 단일 샘플에 의존한다.** 첫 행 1.5% 오버슈트면 `cc_frac`이 0.945에서 0.004로,
전류 잡음 σ=0.5%면 0.026으로 조용히 붕괴한다. 20 mAh 셀의 C/10은 2 mA라 0.3~0.5% 잡음이 현실적이다.
주 타깃 `cap`과 불량 라벨은 영향받지 않는다.

**F27 — `cap` 타당성 검사가 없다.** mAh 단위 오입력이나 soft short로 부풀린 셀이 조용히 전부 "정상"으로
라벨링된다. 설계용량의 250%인 셀도 통과한다.

**F19 — 다중 sweep `.mpt`에 sweep 선택 수단이 없다.** `"select a sweep"` 오류를 내면서 정작 고를 방법이 없고,
유일한 우회인 `'mean'`은 SOC가 다른 스펙트럼을 평균해 어떤 실제 상태에도 대응하지 않는 값을 만든다.

**F13 — CSV를 `cfg.encodings` 없이 UTF-8로만 읽는다.** 한국어 Windows Excel이 저장한 CSV가 세 CLI 모두에서
실패하고, `extract_capacity.py`에서는 traceback + exit 1로 끝난다.

### 4.2 검증 체계의 공백

**F03 — 변이 25개 중 23개가 살아남는다.** 패키지 사본에 결함을 주입하고 34개 테스트를 돌린 결과다.
Ridge 후보 전체 제거, `fixed_baselines`를 바깥 테스트 셀 포함 전체에 적합하는 누수, 대역 열 목록 교환,
Q² 공식 변경, 안쪽 선택 지표 변경이 전부 통과한다.

**F02 — 같은 변이가 릴리스 게이트도 통과한다.** Logistic 확률 클래스를 반전시켜 `TP=0 FN=6 FP=6 TN=0`,
`AUC=0.0`이 된 완전 반전 분류기가 7/7 명령, 4/4 검사 "passed"를 받았다. `predict.py`의 불량 판정 부등호를
뒤집어 정답과 0/12 일치가 돼도 통과했다.

**F04 — 배치 분리 검사가 실패할 수 없다.** `make_demo`가 `batch_id`를 `i//4`로 주어 배치가 셀 순서와 연속이라,
`GroupKFold`를 그룹 무시 `KFold`로 바꿔도 통과한다. 배치를 `(i%3)+1`로 교차시키면 위반 6건이 잡힌다.

**F22 — 예측 경로가 단위 테스트에서 실행되지 않는다.** `logistic`·`cc_fraction` 분기와 CLI가 미실행이고,
"무재적합" 테스트는 `Pipeline.fit`만 patch해 스케일러만 재적합하는 버그를 놓친다.

**근본 원인은 데모 데이터가 너무 쉽다는 것이다.** `make_demo`에서 `cap`과 `ocv`가 둘 다 `severity`의 선형
함수라 `corr(cap, ocv)=0.9944`이고, 37개 특징 전부가 단일 임계값으로 클래스를 완전 분리한다. 그래서 릴리스 검증
3회 모두 최종 용량 모델이 **EIS를 전혀 쓰지 않는 OCV 단독 선형회귀**로 선택됐고, `baseline_ocv`의 Q²(0.983)가
중첩 선택(0.967)보다 높다.

### 4.3 지표 해석과 출력

**F11 — 무정보 기준선이 0도 0.5도 아니다.** LOO 평균 예측기의 `baseline_mean` Q²는 자료와 무관한 상수
`1−(n/(n−1))²`다. n=12에서 −0.190이고 실제 저장값과 부동소수점까지 일치한다. 같은 이유로 threshold AUC가
**정확히 0**이 된다. 분류 표에 기준선 행이 없어 사용자가 이를 알 방법이 없다.

**F05 — pooled LOO AUC의 우연 수준이 0.5가 아니다.** 원인 귀속은 정정했지만(§3) 해석 위험은 남는다.
무신호 n=40에서 평균 0.42, 표준편차 0.2다. 약신호에서는 보고값 0.771인데 독립 4000셀 기준 진짜 AUC가
0.550인 경우도 나왔다. README는 계산 방식만 적고 이 위험을 알리지 않는다.

**F31 — 안쪽 선택 지표가 학습 목적과 불일치한다.** 비가중 log loss로 고르는데 학습은 `balanced`이고 판정선은
0.5다.

**F07 — 모순 상태가 기록된다.** LOGO에서 OOF 평가는 성공하고 `save_final`만 실패하면 `metrics.json`에
logistic 지표와 `unavailable['logistic']`이 동시에 남고 모델 파일은 없다. 13셀 배치 (2,3,3,3,2)·불량 (1,1,0,0,1)로
재현했다.

**F01 — 동봉 산출물에 이미 오탐이 있다.** `release_check/new_predictions.csv`의 12셀 중 3셀(61, 69, 72)이
`review_required=True`다. 이 셀들은 학습 셀 41·49·52의 바이트 동일 복사본이다. 원인은 `pd.read_csv` 기본
파서의 1 ulp 왕복 오차와 허용오차 없는 `<`/`>` 비교이고, `float_precision='round_trip'`으로 읽으면 0건이 된다.
`verify_release.py`가 `seen_in_training`만 검사해 놓쳤다.

## 5. 적용한 수정

브랜치 `review/defective-cell-ml-v2.0.0`에 모듈별로 커밋했다. **원본 ZIP과 원격 브랜치는 변경하지 않았다.**

| 커밋 | 모듈 | 내용 |
|---|---|---|
| `0cb6c19` | extract | 인코딩(cp1252 추가), CC/CV 판정 견고화, 다중 sweep 선택 설정, CLI 종료 규약 통일, cap 타당성 검사, manifest/CSV 인코딩 헬퍼, 대문자 특징명 거부 |
| `4029d8a` | predict | 범위 비교 허용오차와 `float_precision='round_trip'`, 선택 특징 기준 플래그와 이탈 특징 열, artifact 해시 대조, 의존성 버전 기록, provenance 확장 |
| `e2d986f` | tests | 값 수준 릴리스 oracle, 변이 저항 픽스처(다변량·무신호), GridSearchCV spy, 교차 배치 그룹 검사, bare assert 제거, 임시 폴더 위생 |
| `4a3e62e` | models | 우연 수준 기준선 행, 타깃 단위 실패 분리, 읽을 수 있는 실행 요약, 제외된 후보 기록, 모델 진단 |
| `287fc31`, `fa5be52` | tests | 모듈 간 계약 정렬 |

models 모듈에서 특히 값어치가 큰 것들이다.

- **F11**: `baseline_mean_threshold`, `baseline_prior` 등 우연 수준 행이 분류 표에 실제로 들어갔다. 데모 실행에서
  `baseline_mean_threshold`의 AUC가 정확히 0으로 찍혀 LOO 인공물이 표 안에서 자명해진다.
- **F17**: `run_summary.md`가 지표 표와 fold별 선택 빈도를 담고, 최종 모델이 EIS 열을 하나도 쓰지 않으면
  **"이 capacity 모델은 EIS 특징을 전혀 사용하지 않습니다"**를 굵게 출력한다. 데모에서 실제로 출력된다.
- **F07**: 배포 적합 실패가 `unavailable['<name>_deployment_model']`로 분리되어 지표 행과 공존하지 않는다.
- **F24**: `metrics.json`에 `diagnostics` 키가 생겨 상수 확률 모델이나 C 격자 경계 선택을 경고한다.
  데모 기본 격자에서 `boundary: 12 of 12 folds` 경고가 실제로 뜬다.

### 검증 결과

| 항목 | 결과 |
|---|---|
| 단위 테스트 | **131개 통과** (원래 34개) |
| 배포 검증 | 전 항목 통과 (검사 4개 → 6개) |
| `raw_group` OOF 예측 | 수정 전과 **비트 단위로 동일** (공유 수치 열 16개, 최대 상대차 0.0) |
| 예측 오탐 | 3건 → **0건** |
| 분류 표 | 기준선 행 4개 추가 (`baseline_mean_threshold`, `baseline_mag@1000Hz_threshold`, `baseline_ocv_threshold`, `baseline_prior`) |

OOF 예측이 비트 단위로 동일하다는 것은 **평가 의미론을 바꾸지 않았다**는 뜻이다. 견고성과 진단만 개선했다.

변이 테스트로 효력도 확인했다. 이전에 34개 테스트를 통과하던 변이 20개가 이제 전부 사망한다. 릴리스 게이트 단독으로도
logistic 클래스 인덱스 반전, predict 부등호 반전, 점수 부호 반전 세 가지를 잡는다.

## 6. 남은 일

- **문서 24건**: README §4 설정표 누락 키, `inner_splits` "최대 3" 오기, LOO 풀링 편향 설명, 원시 입력 형식 요건,
  `MANIFEST.sha256`과 `validation/` 기록 재생성. 이번 브랜치에서 함께 처리했다.
- **Windows 실기 확인**: F30(한글 경로 인코딩)은 Linux에서 재현되지 않아 실제 Windows에서 한 번 더 확인해야 한다.
- **실측 프로토콜 확인 후 재검토**: F32·F33·F06·F19의 수정은 조용한 실패를 시끄러운 실패로 바꾸는 방향으로
  보수적으로 했다. 랩의 실제 cycler·EC-Lab 출력 형식을 알면 더 나은 선택이 있을 수 있다.

## 7. 한계

- **실제 원시 자료가 없다.** 실측 성능, 수정 전후 성능 차이, 외부 배치 일반화는 여전히 미검증이다.
  이 리뷰가 확인한 것은 코드 동작과 검증 체계이지 불량셀 판별 성능이 아니다.
- **F32·F33·F06·F19는 실측 프로토콜을 알아야 최적 수정을 정할 수 있다.** 적용한 수정은 조용한 실패를
  시끄러운 실패로 바꾸는 방향으로 보수적으로 했다.
- **미검증 9건**(F35, F36, F38, F39, F43, F47, F52, F53, F61)은 전부 low 등급이며 사용 한도로 다중 렌즈
  검증을 돌리지 못했다. 사실 확인은 원본 소스 대조로 했다.
- **이견 7건**(F37, F49, F56, F57, F59, F60, F63)은 회의론자와 재현자의 판단이 갈렸다. 전부 note 등급이다.
- Windows 실기 확인이 필요한 항목이 있다(F30의 한글 경로 인코딩).

## 8. 전체 항목

등급은 반박 검증 후 값이다. 판정의 분수는 "기각하지 않은 렌즈 / 전체 렌즈"다.

| ID | 등급 | 원래 | 판정 | 범위 | 파일 | 내용 |
|---|---|---|---|---|---|---|
| F01 | 중간 | high | 확인 3/3 | 코드 | predict.py, export_for_origin.py | outside_training_range/review_required 오탐: pandas 기본 read_csv의 부동소수 파싱 1 ulp 오차 + 허용오차 없는 엄격 <,>… |
| F02 | 중간 | high | 확인 3/3 | 테스트 | verify_release.py | tests/verify_release.py의 4개 check는 형상·유한성·합계만 검사해 분류기 반전·판정 부등호 반전 변이도 '7/7 명령, 4/4 검사 passed'로 … |
| F03 | 중간 | high | 확인 3/3 | 테스트 | test_pipeline.py, demo.py | 단위 스위트(small_config + 선형 데모 데이터)가 중첩 선택·누수·지표 관련 변이 25개 중 23개를 통과시킨다: 데모 fixture가 너무 쉬워 Ridge 경로… |
| F04 | 중간 | high | 확인 3/3 | 테스트 | test_pipeline.py, verify_release.py | '배치 분리' 검사(test_nested_group_separation, verify_release 85–87행)는 데모 배치가 셀 순서와 연속이라 그룹을 무시하는 안쪽 K… |
| F05 | 중간 | high | 확인 3/3 | 코드 | ridge_capacity.py, config.py | class_weight='balanced' + pooled LOO AUC: 보고 AUC가 배포 모델의 실제 판별력보다 체계적으로 낮고 우연 수준이 0.5가 아님 |
| F06 | 중간 | high | 확인 3/3 | 코드 | extract_capacity.py | find_cv_start가 구간 첫 샘플 전류 하나와 1% 밴드로 CV 시작을 판정해 오버슈트·전류 잡음·램프업에서 cc_frac이 조용히 붕괴 |
| F07 | 중간 | medium | 확인 3/3 | 코드 | export_for_origin.py | LOGO에서 OOF 평가 성공 후 save_final만 실패하면 metrics.json에 logistic 지표와 unavailable['logistic']이 동시에 기록되고… |
| F11 | 중간 | medium | 확인 3/3 | 코드 | export_for_origin.py, ridge_capacity.py | LOO 평균/수축 예측기의 인공물: baseline_mean의 threshold AUC가 정확히 0, Q2는 자료 무관 상수 1−(n/(n−1))²(n=12: −0.190)… |
| F13 | 중간 | medium | 확인 3/3 | 코드 | extract_capacity.py, predict.py | selection manifest·features CSV(extract_capacity.py:178, export_for_origin.py:241, predict.py:64… |
| F19 | 중간 | medium | 확인 2/3 | 코드 | extract_capacity.py | 다중 sweep .mpt(EC-Lab cycle number)는 'select a sweep' 오류를 내지만 sweep 선택 수단이 없고, 유일한 우회 'mean'은 SOC… |
| F22 | 중간 | medium | 확인 3/3 | 테스트 | test_pipeline.py, predict.py | predict.py의 logistic·cc_fraction 분기와 CLI(main)는 단위 테스트에서 실행되지 않고, '무재적합' 테스트는 Pipeline.fit만 patc… |
| F27 | 중간 | medium | 확인 3/3 | 코드 | extract_capacity.py, export_for_origin.py | cap에 design_capacity_ah 대비 타당성(단위·상한) 검사가 없어 mAh 입력이나 soft short·비가역 용량으로 부풀린 셀이 조용히 전부 '정상'(0)으… |
| F31 | 중간 | medium | 확인 3/3 | 코드 | ridge_capacity.py, export_for_origin.py | Logistic 안쪽 선택 지표(비가중 neg_log_loss)가 balanced 학습 목적·0.5 판정선과 불일치하고, 보고되는 log_loss/brier가 사전확률 기준… |
| F32 | 중간 | medium | 확인 3/3 | 코드 | config.py, extract_capacity.py | 기본 encodings ['utf-8-sig','cp949']가 cp1252(영문 Windows)로 저장된 EC-Lab .mpt 헤더('cm²','°C')를 디코딩하지 못해… |
| F33 | 중간 | medium | 확인 3/3 | 코드 | extract_capacity.py | CC와 CV가 별도 Step No.로 기록되는 프로토콜에서 target_step_i는 단일 구간만 선택해 cap이 CC 용량으로 과소평가되고(cc_frac=1.0) 병합 수… |
| F08 | 낮음 | medium | 확인 3/3 | 코드 | extract_capacity.py | main()이 load_config를 try 밖에서 호출하고 except가 DataError만 잡아 설정·manifest·인코딩 오류가 traceback + exit 1로 … |
| F09 | 낮음 | medium | 확인 3/3 | 코드 | predict.py, export_for_origin.py | 예측 경로의 범위 검사·필수 열·NaN 거부·ocv 요구가 최종 모델의 선택 특징이 아니라 학습 입력 37열 전체(validate_frame 학습 규칙) 기준 — 모델이 무… |
| F10 | 낮음 | medium | 확인 3/3 | 코드 | ridge_capacity.py, README.md | 격자에 정확히 1000 Hz가 없으면 README가 약속한 '/Z/@1 kHz 선형회귀 기준선'과 single_1e3 후보가 unavailable·run_summary 기록… |
| F12 | 낮음 | medium | 확인 3/3 | 코드 | extract_capacity.py | validate_frame이 대문자 `Re@…Hz`/`Im@…Hz` 열을 오류 없이 메타데이터로 무시해 실수부·허수부 없는 모델이 'completed'로 끝남 |
| F14 | 낮음 | medium | 확인 3/3 | 코드 | predict.py, export_for_origin.py | predict.py가 artifact_hashes.json을 대조하지 않고 models/*.joblib를 파일명 기준으로 무조건 로드: 변조·교체·이름 변경 번들이 경고 없… |
| F15 | 낮음 | medium | 확인 3/3 | 코드 | predict.py, export_for_origin.py | 버전 게이트가 패키지 VERSION만 검사: scikit-learn 등 의존성 버전 불일치를 감지·기록하지 않고 InconsistentVersionWarning도 prove… |
| F16 | 낮음 | medium | 확인 3/3 | 코드 | ridge_capacity.py, export_for_origin.py | select_model이 ConvergenceWarning을 예외로 승격하지만 EvaluationError가 아니어서 logistic/cc_frac 미수렴 1회로 실행 전체… |
| F17 | 낮음 | medium | 확인 3/3 | 코드 | export_for_origin.py | run_summary.md·콘솔에 지표 수치와 fold별 '선택된 대역/추정기'가 전혀 없어, 데모 용량 모델이 EIS를 쓰지 않는 OCV 단독 선형회귀라는 사실을 fold… |
| F18 | 낮음 | medium | 확인 3/3 | 설계판단 | export_for_origin.py | 소표본 pooled OOF 점추정치에 fold 분산·부트스트랩 구간·라벨 순열 기준이 없음: n=12 순열에서도 AUC 0.86, Q2 +0.52, MCC 0.67 발생 |
| F20 | 낮음 | medium | 확인 2/3 | 코드 | extract_capacity.py | read_cycle이 target_cycle로 필터링하기 전에 파일 전체(미사용 Voltage/Step Time 포함)에 유한성·시간 단조 검사를 적용해 다른 cycle의 … |
| F21 | 낮음 | medium | 확인 3/3 | 문서 | extract_capacity.py | 원시 입력 형식 요건(파일명 cell<번호> 정규식·첫 일치 사용, cycler 7개 열 이름·탭 구분·단위행, MPT 열 이름, 소수점 기호)이 README에 없어 실제 … |
| F23 | 낮음 | medium | 확인 3/3 | 테스트 | test_pipeline.py, extract_capacity.py | 주요 방어 분기가 테스트되지 않음: cp949 폴백, clamp 초과 거부, target_raw_step 다중 구간, LOGO<3그룹, partial 상태, Excel 수식… |
| F24 | 낮음 | medium | 확인 3/3 | 코드 | ridge_capacity.py, export_for_origin.py | 분류에는 회귀와 달리 기준선 후보·기준선 행이 없고, 상수(≈0.5) 출력 모델이 선택되어도 진단이 없음 |
| F25 | 낮음 | medium | 확인 3/3 | 코드 | extract_capacity.py | read_table의 pd.read_csv에 index_col=False가 없어 데이터 행에만 꼬리 탭이 있으면 첫 열이 index로 승격되어 모든 열이 한 칸 밀림 |
| F26 | 낮음 | medium | 확인 2/3 | 설계판단 | extract_capacity.py | load_raw가 첫 실패 셀에서 즉시 중단해 나머지 셀의 문제를 알 수 없고, 격자 선택 절차·'셀 하나의 실패가 전체 실행을 failed로 만든다'는 동작이 문서에 없음 |
| F28 | 낮음 | medium | 확인 3/3 | 코드 | predict.py | partial 실행·가상 데이터 실행에서 predict.py가 무음으로 동작하고 provenance에 실행 폴더·미계산 타깃·임계값·선택 모델 정보가 없음 |
| F29 | 낮음 | medium | 확인 3/3 | 코드 | ridge_capacity.py, test_pipeline.py | folds.json의 inner_folds·inner_metric은 GridSearchCV에서 파생된 값이 아닌 자기보고 값이라 실제 분할·scoring이 달라도 모든 검사… |
| F30 | 낮음 | medium | 확인 3/3 | 테스트 | test_pipeline.py, README.md | test_pipeline.py가 run.json/data_audit.json/sentinel을 encoding 지정 없이 읽고 써서, README §6 명령(-X utf8 … |
| F34 | 낮음 | medium | 확인 2/3 | 코드 | extract_capacity.py | build_features의 격자 경계 검사가 상대 허용오차 없이 엄격 부등호 비교여서 FRA 실제 주파수·float32 반올림(1e-8~1e-5 상대) 끝점이 기본 pol… |
| F35 | 낮음 | low | 미검증 0/0 | 문서 | README.md, config.py | README §4 설정표에 Config 키 7개(group_column, seed, ridge_alphas, logistic_cs, logistic_class_weight,… |
| F36 | 낮음 | low | 미검증 0/0 | 문서 | README.md, config.py | README 'inner_splits / 최대 3'은 코드와 다름 — 3은 상한이 아니라 기본값이며 validate는 2 이상만 검사하고 축소 기준도 타깃별로 다름 |
| F38 | 낮음 | low | 미검증 0/0 | 코드 | config.py, extract_capacity.py | Config.validate가 zlib/base64/rot13 같은 비텍스트 codec과 비정수 exclude_cells 키를 DataError로 걸러내지 못해 미포착 Lo… |
| F39 | 낮음 | low | 미검증 0/0 | 문서 | 머신러닝_문서별_정독기록.md, verify_release.py | docs/reviews 정독기록에 작성자 PC 절대경로(<USER_HOME>\…)가 남아 배포 ZIP(MANIFEST 포함)에 실리고, release_v… |
| F40 | 낮음 | low | 확인 2/2 | 코드 | extract_capacity.py | extract_capacity.py는 실패 시 .audit.json을 쓰지 않아 R6가 약속한 파일 해시·실패 사유 기록이 CLI에서 유실되고, 사이드카 파일 규칙이 REA… |
| F41 | 낮음 | low | 확인 2/2 | 코드 | extract_capacity.py | manifest 경로에서 제외 셀의 'excluded' 감사 이벤트가 cycle·eis 디렉터리마다 중복 기록됨 |
| F42 | 낮음 | low | 확인 2/2 | 코드 | predict.py | 결과 CSV를 provenance보다 먼저 써서 provenance 실패 시 CSV만 남고, 같은 경로 재실행은 'Output exists'로 막힘 |
| F43 | 낮음 | low | 미검증 0/0 | 코드 | verify_release.py, export_for_origin.py | release_verification.json·artifact_hashes.json의 키가 OS 경로 구분자를 그대로 써서 Windows에서 만든 기록을 Linux/macO… |
| F45 | 낮음 | low | 확인 1/1 | 코드 | export_for_origin.py | cc_frac 열이 있으나 값이 전부 결측(또는 1–3셀만 존재)이면 '최소 4셀 필요'라는 무관한 사유가 unavailable['cc_fraction']에 기록됨 |
| F46 | 낮음 | low | 확인 1/1 | 코드 | export_for_origin.py, README.md | 11개 Excel 시트의 열 구조가 미문서화이고 세부가 어긋남: '03_reg_coefs'에 logistic(로그오즈) 계수 혼입·용량 행 0개 가능, 04_reg_resi… |
| F47 | 낮음 | low | 미검증 0/0 | 코드 | config.py | 설정 검증 오류문이 위반 키·입력값·허용 범위를 말하지 않음('Invalid tolerance', 'Invalid cell range or inner_splits', 'se… |
| F48 | 낮음 | low | 확인 2/2 | 코드 | extract_capacity.py | selection manifest의 빈 칸(NaN)·'41.0' 형식 cell_number가 검증 없이 int()/Path 연산에 들어가 DataError가 아닌 TypeE… |
| F50 | 낮음 | low | 확인 2/2 | 코드 | predict.py | 손상/비호환/비번들 joblib 처리: EOFError·UnpicklingError·AttributeError는 traceback으로 exit 1, 잡히는 경우도 'Pred… |
| F51 | 낮음 | low | 확인 2/2 | 코드 | predict.py, extract_capacity.py | 예측 문맥에 맞지 않는 오류 안내: ocv 누락 시 'set use_ocv=false'(저장 모델은 설정 변경 불가), --run 오지정 시 run.json 경로 오류만 출… |
| F52 | 낮음 | low | 미검증 0/0 | 코드 | verify_release.py, README.md | verify_release.py의 PACKAGE.rglob('*.py')가 README가 안내하는 패키지 내부 .venv(및 results/)까지 해시해 code_sha25… |
| F53 | 낮음 | low | 미검증 0/0 | 코드 | verify_release.py | verify_release.py의 릴리스 검사 15개가 bare assert라 python -O/PYTHONOPTIMIZE에서 통째로 제거되어 해시 손상도 'All rele… |
| F55 | 낮음 | low | 확인 2/2 | 코드 | extract_capacity.py | 콤마 소수점(.mpt 로케일)·단위행 mAh/mA·h:mm:ss 시간 등 흔한 형식 변형이 모두 같은 일반 오류문('nonfinite/nonnumeric')으로 뭉뚱그려져 … |
| F56 | 낮음 | low | 이견 1/2 | 코드 | extract_capacity.py | 기본 cell_min/cell_max(34–98)가 CSV 입력 행을 콘솔 안내 없이 제외하고, 전부 제외되면 원인 키를 말하지 않는 'No rows remain after… |
| F58 | 낮음 | low | 확인 2/2 | 코드 | predict.py, extract_capacity.py | 출력 CSV 해석성: 입력과 다른 행 순서(cell_number 정렬, 미문서), 단위 없는 predicted_capacity, bool/int 혼용, 임계값 미기록, re… |
| F60 | 낮음 | low | 이견 1/2 | 문서 | extract_capacity.py | 학습 설정의 exclude_cells(사전 QC 제외)가 예측 경로(training=False)에서 무시되어 제외된 셀 ID가 아무 표시 없이 예측됨 |
| F61 | 낮음 | low | 미검증 0/0 | 테스트 | test_pipeline.py, verify_release.py | 단위 테스트 임시폴더가 시스템 temp가 아닌 현재 작업 디렉터리(README §6대로면 패키지 폴더)에 생성되고, verify_release는 이를 배포 패키지 트리 안에… |
| F63 | 낮음 | low | 이견 1/2 | 코드 | extract_capacity.py | 구간 시작/종료 행의 0 A 기록(스텝 시작·cut-off 종료 로그)이 셀 실패 → 실행 전체 실패로 이어지며 우회 설정이 없음 |
| F37 | 메모 | low | 이견 1/2 | 코드 | export_for_origin.py | results_for_origin.xlsx가 동일 입력·seed에서도 바이트가 달라져(openpyxl docProps 타임스탬프) artifact_hashes.json으로 … |
| F44 | 메모 | low | 확인 1/1 | 설계판단 | ridge_capacity.py, extract_capacity.py | 주파수별 4성분 중 mag/phase는 re/im의 결정적 함수 → 대역 후보가 자유도 2에 열 4, r(re,mag)=1.000000, 계수표(03_reg_coefs)가 … |
| F49 | 메모 | low | 이견 1/2 | 문서 | extract_capacity.py | manifest 모드는 하위 폴더·임의 확장자·symlink 파일을 허용해 README의 '폴더 바로 아래의 .txt, .mpt만 읽는다'와 어긋남 |
| F54 | 메모 | low | 기각 0/1 | 코드 | ridge_capacity.py | 원본 규모(7셀)에서 안쪽 fold는 2~4셀이며 36~37특징 후보를 그 위에서 '선택'함 — 경고·보호 장치 없음 |
| F57 | 메모 | low | 이견 1/2 | 설계판단 | extract_capacity.py | 용량 /Q/(Ah)와 ∫I dt의 물리 일관성 검사가 없어 누적 /Q/·단위·열 매핑 오류를 잡지 못하며, 동봉 예제 fixture 자체가 약 3,000배 불일치 |
| F59 | 메모 | low | 이견 1/2 | 문서 | export_for_origin.py, README.md | capacity_threshold 판정(고정 임계값·MSE 회귀)과 balanced logistic(0.5 작동점)의 민감도/F1/MCC를 같은 표에 나란히 두어 작동점 불… |
| F62 | 메모 | low | 기각 0/1 | 설계판단 | ridge_capacity.py, config.py | 100 kHz–1 MHz 격자점(full의 1 MHz 4열, band_1e3_1e5의 1e5 im/phase)이 후보 대역에 포함되어 실측에서는 셀보다 리드·케이블·지그 인… |
| F64 | 메모 | note | 확인 1/1 | 코드 | export_for_origin.py | run.json code_sha256의 키 순서가 파일시스템 순서에 좌우됨(glob 미정렬) |
| F65 | 메모 | note | 확인 1/1 | 문서 | requirements.lock.txt, requirements.txt | 의존성 고정에 해시·플랫폼 마커가 없고 MANIFEST.sha256은 어떤 문서에도 검증 방법이 안내되지 않음 (inventory·lock·설치본은 일치) |
| F66 | 메모 | note | 확인 1/1 | 문서 | README.md, generate_examples.py | examples/README '예제 재생성' 안내: 다른 OS에서 generate_examples.py를 실행하면 np.hypot 1 ULP 차이와 CRLF→LF 때문에 파… |
| F67 | 메모 | note | 확인 1/1 | 문서 | predict.py | joblib.load는 버전·status 검사보다 먼저 임의 코드를 실행하며 models/의 모든 *.joblib를 이름 제한 없이 로드 (README:77에 위험 문서화됨… |
| F68 | 메모 | note | 확인 1/1 | 문서 | ridge_capacity.py, README.md | LOO에서 Logistic이 계산되려면 소수 클래스가 최소 3셀 필요하다는 조건이 README에 없음 |
| F69 | 메모 | note | 확인 1/1 | 문서 | export_for_origin.py, ridge_capacity.py | models/*.joblib 번들은 커스텀 FeatureSelector 때문에 ridge_capacity 모듈 import에 의존해 자체 완결적이지 않음(패키지 폴더 밖에서… |
| F70 | 메모 | note | 확인 1/1 | 코드 | export_for_origin.py, CHANGES.md | Excel 수식 가드: 현재 워크북에는 사용자 문자열이 도달하지 않아 무해하나, apostrophe가 셀 값에 리터럴로 저장되고 '+','-','@'는 과잉이며 CSV 출력… |
| F71 | 메모 | note | 확인 1/1 | 문서 | export_for_origin.py, extract_capacity.py | run.json·data_audit.json·error_traceback.txt에 절대경로가 기록되어 결과 폴더 공유 시 사용자명·폴더 구조가 노출됨(의도된 출처 기록; R… |
| F72 | 메모 | note | 확인 1/1 | 설계판단 | export_for_origin.py, README.md | 최종 재적합(save_final)의 안쪽 CV 구조가 바깥 fold의 것과 달라 배포 모델이 어느 바깥 fold 선택과도 다른 후보가 될 수 있음(중첩 CV의 본질; 문서에… |
| F73 | 메모 | note | 확인 1/1 | 문서 | ridge_capacity.py, README.md | 무신호에서 중첩 선택은 평균 기준선을 거의 고르지 않고(≈11%) 배포 모델은 과적합 Ridge가 됨 — OOF Q2는 baseline_mean 행과 비교해야만 드러나는데 … |
| F74 | 메모 | note | 확인 1/1 | 코드 | export_for_origin.py, README.md | run.json versions()에 OS/아키텍처/BLAS 기록이 없고 validation/에 비교용 수치가 없어 교차 플랫폼(Windows 고정 자료 vs Linux) … |
| F75 | 메모 | note | 확인 1/1 | 테스트 | verify_release.py | '원시 입력 경로와 CSV 경로 OOF 일치(rtol=1e-8)' 검사는 같은 파서를 양쪽에 쓰므로 자명하며, 존재하는 기준 진실(demo_features.csv)과의 대조… |
| F76 | 메모 | note | 확인 1/1 | 설계판단 | ridge_capacity.py, extract_capacity.py | decade당 1점 격자·고정 4개 후보 대역(single_1e3, band_1e3_1e5, band_low, full)의 물리적 근거와 원시 sweep 밀도 조건이 문서화… |
| F77 | 메모 | note | 확인 1/1 | 문서 | extract_capacity.py | 'ocv'(PEIS 중 <Ewe> 중앙값)의 물리적 의미·프로토콜 의존 누수 경로가 문서에 없고, 릴리스 검증 3회 모두 최종 용량 모델이 OCV 단독으로 선택됨 |
| F78 | 메모 | note | 확인 1/1 | 설계판단 | predict.py | 학습 셀 재예측 시 in-sample 전체 적합값이 표시 없이 반환되고, seen_in_training은 ID만 비교해 동일 특징·새 ID 셀은 '새 셀'로 통과 |
| F79 | 메모 | note | 확인 1/1 | 문서 | config.py, README.md | 기본 라벨이 1주기 '충전' 용량이어서 ASSB 첫 충전의 비가역 용량(ICE)이 포함됨 — 부반응이 큰 셀이 '정상'으로 분류될 수 있음 (문서화 필요) |
| F80 | 메모 | note | 확인 1/1 | 설계판단 | config.py, README.md | 설계용량·면적·임계값 수치는 정합하나 유래가 문서화되지 않고 서로 연동되지 않으며, 고정 절대 임계값은 셀별 활물질 로딩 편차를 구분하지 못하고 pressure_mpa는 파… |
