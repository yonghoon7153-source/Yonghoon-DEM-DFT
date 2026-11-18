# Ⓐ RT fixture NP6 개발 런

1저자 11-18 GO. ibb CPU 1노드 6랭크, 한 잡. 작은 침대 생성 P → RT1 → 같은 체크포인트 RT2 순으로 문법과 재시작 경로를 확인한다. 시간 실측 전이며 잡 상한은 1시간이다. 근거는 `docs/reviews/p1_rt_fixture_runner_preparation_20261117/rt_fixture_flow.sh`와 반입 ⑪ `9a9fec159`다.

입력 6개의 등록 SHA256과 실행 파일 신원을 먼저 확인한다. 작업 폴더가 이미 있으면 제출을 멈춘다. 배치 잡은 SSH와 분리되며 자동 재제출은 0회다. 수집 블록은 제출 번호와 일치하는 회계 행·반환 해시·fixture 판독기의 rc를 확인한다. 개발 반환은 `rt_development_return.tar.gz`, `SHA256SUMS`, `worker_rc.txt`, `scheduler.txt`다. 실패도 같은 작업 폴더에 보존한다.

로컬 모의 검사는 동일한 3개 시험으로 준비 전 3실패 → 준비 후 3통과. 여섯 랭크 선언, 실행 파일 신원, 세 단계 순서와 RT1 실패 뒤 중단을 검사했다. 실제 값·물리 자격·봉인 결과는 현 시점 0건이다.
