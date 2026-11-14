# SELF-170 — 전체 소스 고정 시각 사본 준비

## 1. 준비된 것

후보087ba5eb9a8d1d2c363d265bacfe064116361c80 및 그 부모의 mixer_smoke_blind 전체 blob에 같은 datetime overlay만 삽입했다. 원본2·고정사본2·diff2는 리포 밖 인계 ZIP의 private_preparation/self170_copies에 보존한다. 리포에는 overlay 원문·manifest만 둔다. 운영 소스·source seal·예약 변경0.

사본2개 각각 overlay를 제거하면 원 blob 바이트로 돌아오고, 삽입 AST 노드를 제거해도 원 AST와 같다. 구문 compile만 했으며 wrapper를 import/실행하지 않았다. 별도 overlay만으로 UTC·+09·naive 3관측을 확인했다. naive는 UTC 시계값의 tzinfo 제거를 명시한 합성 규약이며 현장 local time 자격이 아니다. 전체 Linux selftest0회.

## 2. Linux로 가져갈 때의 준비 계약

| 단계 | 고정 대상 | 확인·미확인 |
|---|---|---|
| L0 | 후보/부모 핀을 각각 빈 격리 사본으로 구성 | 기존 imports·합성 fixture·자식 CLI 의존 필요. 이4소스만으로 자립 실행 묶음이 아님 |
| L1 | 원본 두 개의 hash, 집중 시험 파일은 후보 핀 | 원본/후보와 다른 의존 판을 섞지 않음 |
| L2 | 일반 시각 전체 --selftest 및 후보 집중11메서드 | 현재 Linux 결과 미수령; 권한0600·POSIX 실패를 대역으로 없애지 않음 |
| L3 | 각 격리 사본에서 해당 고정 시각 파일을 같은 scripts/mixer_smoke_blind.py 자리로 복사 | 원 운영 파일 덮어쓰기 금지. 자식 CLI도 같은 사본을 쓰게 하는 경로·hash 확인 |
| L4 | 고정 전체 selftest before/candidate | 구본 timestamp 오탐→후보 제거 기대. 정확한 실패수는 결과 뒤 기록 |
| L5 | rc·stdout/stderr·소스/의존 신원·환경·완료 검사 | 30 AST chk 호출지점은 실행 통과 수 아님; 권한/셸 오류는 미완료 |

현장 실행 명령이나 GO를 새로 발행하지 않는다. 이전 nonrint_overnight_recovery_20261114/mixer_self170_linux_plan.md의 L0–L5를 바이트 고정 준비로 한 단계 진행한 것이다. 현재 사본은 시험 준비용이며 재봉인 A/B·E0-R1·운영자/자원·발사 승인에 쓰는 운영 소스가 아니다.

## 3. 남은 조건

Linux 의존·권한 환경 확정과 별도 합성 실행 허용 뒤 L0–L5를 수행한다. 정상/시계고정 결과 수령·E0-R1 비준 기록·별도 운영 재봉인 승인·E0 한 팔 검토/현장 영수증·1저자 GO가 남는다. 이번에는 모두 미수행이다.
