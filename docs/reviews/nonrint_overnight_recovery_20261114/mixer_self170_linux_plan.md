# SELF-170 Linux 전체 합성 확인 계획 — 실행0

## 1. 고정 대상과 한정

수정 소스=087ba5eb9의 scripts/mixer_smoke_blind.py 및 scripts/test_mixer_self170_canaries.py. 문서 끝 b94090e04까지 소스는 같다. 148a8f30b의 E0-R3 정정 수령은 역사 포장 누락 처리이며 이 Linux 확인을 대신하지 않는다. 원장 상태·운영 source seal·예약을 고치지 않는다. 실제 Linux/WSL/ibb/kgy/gabia 접근0, 시험 실행0. 현장 없이 준비하라는 1저자 11-14 범위다.

## 2. 수행자가 별도 환경에서 확인할 순서

| 단계 | 입력/명령 계획 | 기대와 기록 |
|---|---|---|
| L0 | 새 Linux scratch에 원 핀 소스·의존 파일을 고정; Python/OS/권한·umask·파일시스템 기록 | 원본불변·출력새폴더·외부네트워크/engine/MPI/연구입력 없음 |
| L1 | python3 -I -X utf8 -B scripts/test_mixer_self170_canaries.py | 기존 집중11/11 rc0. 별도 Linux 확인이며 Windows 수에 합산하지 않음 |
| L2 | python3 -I -X utf8 -B scripts/mixer_smoke_blind.py --selftest | rc0·각 검사 출력·실패0. 출력번호㉓을 전체 고유23개라고 세지 않음: 고정소스 AST의 chk 호출지점은30개(정적수) |
| L3 | 고정 시각 전체 사본을 구본/후보 각각 새 scratch에 준비 | 전체파일의 clock overlay 차이만 허용. 고정시각2026-11-12T17:35:10.964312Z. 원소스 SHA 및 overlay diff를 기록 |
| L4 | 같은 전체 selftest를 구본/후보 고정시각 사본에 적용 | 구본은 기존timestamp오탐, 후보는 정상 통과를 기대. 정확한 실패수는 실행뒤 기록, 미리 단정 안 함 |
| L5 | 일반시각/고정시각, before/after 각각 rc·stdout/stderr·소스/시험SHA·출력목록 | 반환값만으로 검사 누락·권한 대체를 숨기지 않음 |

L3의 기준은 받은 self170/msb_fixedtime.py의 datetime overlay 개념이다. 그것을 그대로 운영 소스로 채택하지 않는다. 기존 debug/path 수정이 섞이지 않도록 후보 전체파일에 시계 대체만 적용한 diff를 먼저 검토한다. 현재의 AST 검사식 사본과 전체사본을 혼동하지 않는다. 위 명령은 계획이며 실행 블록/GO가 아니다.

## 3. 실패·보존

POSIX0600·셸·파일시스템 검사 실패를 Windows 대역이나 monkeypatch로 없애고 Linux전체 통과라 하지 않는다. baseline과 후보에서 같은 환경 결함이면 구현결함과 분리해 기록하고 미완료로 남긴다. 실제 원자료 대신 suite 자체 합성 fixture만 사용한다. 정상 결과에 맞춰 시계·바늘·판정식을 바꾸지 않는다.

SELF-170 canary는 selftest 안 검사이며 실제 임의 값누출 방어 인증이 아니다. Unix mode와 로그 완결 등 전체 wrapper 범위도 별도로 기록한다. 고정시각 사본 통과가 실제 E0결과/재봉인/발사 승인으로 바뀌지 않는다. 결과 수령→E0-R1 비준 기록→별도 재봉인A/B 승인→E0 한팔 검토/현장영수증→1저자GO의 남은 순서를 유지한다. E0-R1/R2의 현재 미정 칸을 이 오버나잇 지시로 승인 처리하지 않는다.
