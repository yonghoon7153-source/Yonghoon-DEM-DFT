# A5 로그인 환경 회귀 재현

동일한 Linux 모의 시험 7개를 원본 V1과 수정 V2에 적용한다. 이전에 배포한 운영자 ZIP 두 개가 입력이다. 원본 파일은 보존하고, ZIP마다 따로 만든 빈 로컬 디렉터리 안에서 준비한다. 테스트에서는 임시 홈과 모의 스케줄러를 사용한다.

1. 선택한 버전의 바깥 ZIP을 `author_packet`에 풀고, 해시 목록을 확인한다. 안의 `a5_bound_payload.zip`을 같은 작업 디렉터리의 `build_payload`에 푼다.
2. 그 작업 디렉터리에서 아래 명령을 사용한다. `TESTS`는 리포의 `docs/reviews/p1_a5_rj_login_env_20261120/tests` 디렉터리 위치로 설정한다. 결과 JSON은 현재 작업 디렉터리에 생긴다.

```bash
export A5_QA_INPUT="$PWD"
python3 -I -B "$TESTS/login_regression.py"
```

V1은 두 진입점의 정상 ibb 로그인 사례가 실패한다(rc 1, 7개 중 2실패·오류 0). V2는 같은 시험 7/7, rc 0이다. 거부해야 할 기존 환경과 다른 호스트, 프로필의 자식 상속 및 배치 환경 허용 목록을 함께 검사한다. 시험의 프로필은 합성 파일이다. 비대화 SSH가 원격 Python을 시작하기 전에 거치는 운영체제 로그인 절차는 이 모의 시험의 범위 밖이다.

3. V2에서 기존 24개 회귀도 같은 입력으로 실행한다.

```bash
python3 -I -B "$TESTS/history_suite.py"
```

기대값은 24/24, rc 0이다. 제출 예약, SSH가 끊겼을 때 제어기 유지, 중복 제출 억제와 오류 회수 등을 포함한다. 시험 결과와 공개 가능한 지문은 `docs/reviews/p1_a5_rj_login_env_20261120/offline_checks.json`과 `docs/reviews/p1_a5_rj_login_env_20261120/release.json`에 있다. 각 시험의 출력은 새 디렉터리에 보존한다.
