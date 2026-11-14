# SELF-170 Linux 준비 — 소스·정적 자산 결속

## 1. 추가 준비

이전 전체 고정 시각 사본2개만으로 의존이 충분하지 않던 부분을 보완했다. 후보087ba5eb9a8d1d2c363d265bacfe064116361c80의 정적 import 연결12개 Python 소스, 런처/시작대조기/정책·STL3개를 포함한 총18개 Git blob을 고정했다. 부모56f4cfbb1과 wrapper/새 집중 시험을 제외한16개는 바이트 동일이다. private 준비 ZIP에 원본 layout과 before/시계 사본·diff를 넣었다.

| 검사 | 결과 | 한정 |
|---|---|---|
| blob 신원 | 18/18 길이·SHA256·Git blob | 실제 실행 당시 사용 인증 아님 |
| Python 구문 | 13파일 compile | import·selftest 실행0 |
| rest 관문 | 런처의 해당 Python 블록1개 추출·구문, 정적 로컬 import 포함 확인 | 런처 shell 실행0·제출0 |
| ZIP | 27파일·외부26/26·CRC/경로/중복/링크 정상 | 실행 자격 아님 |
| Linux 전체·현장·재봉인 | 0·0·0 | 계속 미수행 |

자세한 pin/path/blob·의존 간선·동적 경로·패키지SHA는 mixer_dependency_manifest.json. 원본을 읽어 운반했으며 생성기·소비자를 import하지 않았다.

## 2. 허용할 시험 범위의 초안

지원 예정 진입점은 후보 집중 회귀와 mixer_smoke_blind의 --selftest다. 런처는 rest Python 관문 추출용 텍스트 의존이고 셸로 실행하지 않는다. generator CLI, 다른 도구의 selftest, 실제 입력/Slurm/engine 모드는 범위 밖이다. 소스 안 동적 import 전체를 인증하지 않았으므로 모든 CLI의 자립 실행 묶음이라고 하지 않는다. 목록에는 정적 과잉 의존도 포함될 수 있다.

예정 Linux 확인에서는 네 새 격리 사본(부모/후보 × 일반/고정 시각)을 사용하고 해당 wrapper만 교체한다. focus 회귀는 같은 후보 시험을 부모/후보에 적용한다. 시계 대체가 parent/child CLI 모두 같은 경로에 적용되는지 실제 확인해야 한다. 원 운영 파일·봉인에 복사하지 않는다. 환경 Python/NumPy/SciPy, POSIX0600·셸·자원·임시폴더/회수는 미정이다. 자동 실행 스크립트나 예약 변경 기능은 만들지 않았다.

## 3. 남은 문

Linux 의존/권한 자격·전체 일반/시계 시험은 별도 허용 뒤. E0-R1·운영 재봉인 A/B·현장 자원/운영자·실행 GO는 그대로 남는다. 이번 준비는 기존 SELF-170 집중11/11과 합산하지 않고 실제 값 유출 방어를 보편 인증하지 않는다.
