# 사용한 오픈소스

아래는 검증 환경에 실제 설치한 배포본 메타데이터 기준이다. 패키지는 공개 Python API를 사용하며, 의존성 바이너리를 ZIP 안에 포함하지 않는다. 설치는 `requirements.lock.txt`로 수행한다. 전체 의존성 버전과 라이선스 메타데이터는 `docs/licenses/inventory.json`, 배포본이 제공한 라이선스 원문은 같은 폴더에 보관했다.

| 프로젝트 | 검증 버전 | 패키지에서 하는 일 | 주 프로젝트 라이선스 표시 |
|---|---|---|---|
| scikit-learn | 1.7.2 | Pipeline, StandardScaler, Ridge/Logistic, 중첩/그룹 검증, 지표 | BSD-3-Clause |
| NumPy | 2.3.5 | 수치 검증, 복소 EIS 처리, 가상 입력 생성 | BSD 3-Clause |
| SciPy | 1.16.3 | scikit-learn 모델의 수치 연산 기반 | BSD 3-Clause |
| pandas | 2.3.3 | 원시 표/CSV 처리, 셀별 결과 결합 | BSD 3-Clause |
| openpyxl | 3.1.5 | Origin용 Excel 표 출력과 읽기 검증 | MIT |
| joblib | 1.5.2 | 적합 모델 저장과 재로드 | BSD 3-Clause |
| threadpoolctl | 3.6.0 | 검증 실행 중 수치 연산 스레드 수 제어 | BSD-3-Clause |

표는 각 프로젝트의 주 라이선스 표시이며, NumPy/SciPy 등의 배포본에 포함된 다른 구성요소의 고지를 대체하지 않는다. 원문 파일을 함께 보관했다. 전이 의존성은 et_xmlfile, python-dateutil, pytz, six, tzdata이며 정확한 버전은 lock 파일에 있다.

사용자 제공 원본 ZIP의 저작권과 이용 조건은 그대로 유지한다. 이 문서는 원본 또는 본 패키지 전체에 새로운 공개 라이선스를 부여하는 선언이 아니다. 브랜치·문서에서 적용한 방법론의 출처는 `docs/METHODS_AND_SOURCES.md`에 따로 기록했다.
