# SELF-170 — 네 사본의 시험 수령 계획

## 1. 핀과 목표

docs/reviews/nonrint_contract_preparation_20261114/mixer_dependency_preparation.md 및 mixer_dependency_manifest.json의18blob 준비를 이어간다. 부모56f4cfbb1d26371007b460a992d4cfc1ef68e950와 후보087ba5eb9a8d1d2c363d265bacfe064116361c80, 원/고정시계 사본을 유지한다. 이번에는 실행 블록·새 timeout·launcher를 만들지 않았다. Linux 실행0·전체 HOLD.

## 2. 고정할 네 칸

| 칸 | wrapper | 시계 | 결과 전 기대/해석 |
|---|---|---|---|
| B-N | 부모 | 일반 | 우연히 통과해도 타임스탬프 충돌 결함 부재 증명 아님 |
| B-F | 부모 | 고정 사본 | 등록한 바늘/타임스탬프의 충돌 반례를 해당 항목에서 확인해야 함 |
| C-N | 후보 | 일반 | 전체 해당 selftest의 실제 method 수·rc·예상 음성 일치 |
| C-F | 후보 | 같은 고정 사본 방식 | B-F에서 실패한 항목과 기존 양성을 함께 보존 |

각 칸은 새 격리 사본, 같은 나머지16의존, 별도 output 신원으로 남긴다. 집중 시험은 같은 후보 시험을 부모/후보에 적용한다. 일반/고정 시계 반복·내부 항목·focused method 수를 합산하지 않는다. B-F가 의존 누락·환경·구문 때문에 rc1이면 의도된 red가 아니다. 대상 실패의 assertion·항목 번호·stdout/stderr가 맞는지 분리한다.

## 3. 수령 필드와 미결

각 행에는 source pin·wrapper SHA·clock overlay SHA·나머지 의존 목록SHA·test SHA·실제 argv·환경 신원·완료/rc·method/failure/error·산출 목록SHA·시계 적용 범위를 요구한다. 부모/자식 Python 모두 overlay가 닿았는지는 실제 증거로 확인한다. 원본 source/fixture 전후SHA도 대조한다. 로컬 scratch 경로는 비공개 증거에만 보존한다.

Python/NumPy/SciPy·POSIX 권한0600·shell·지원OS·자원·중단/회수·출력 비존재·실행 허용 범위는 아직 미정이다. 기존 버전 숫자를 새 환경의 관측으로 채우지 않는다. launcher 파일은 추출할 rest Python 관문의 텍스트 의존이며 sbatch/mpirun 실행 경로가 아니다. 정적18blob 묶음은 모든 동적 CLI 의존을 인증하지 않는다.

결과 누락/부분/다른핀/의도와 다른 실패는 NOT_QUALIFIED. 자동 재시도·예약 해제·재봉인·host/wave/first8 승인 없음. E0-R1 및 기존 E0 운영 승인 문은 그대로다.
