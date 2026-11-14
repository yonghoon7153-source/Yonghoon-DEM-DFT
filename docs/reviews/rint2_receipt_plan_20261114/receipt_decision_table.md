# Rint Q14 — 결과 수령 때의 귀속·모순 대조

## 1. 이번 완료

실행 소스64e4d213e8267bafaf3ae5af00a42996cefd3f33 및 기존 Q14 블록 원문은 그대로다. 54f8f0ace37c5dd439e36df2262df06732627b63의 E1–E4/T1–T3·Q11 consume 표를 **원문 출력의 귀속·완전성 수령 순서**로 정리했다. 문서·빈 양식만, 수령 결과0·시험0·현장0·σ 열람0·전체 HOLD. 새 소비자/자동 채택/시간 중단 구현이 아니다.

## 2. 먼저 구별할 상태

| 상태 | 조건 | 처분 |
|---|---|---|
| NOT_RECEIVED | 원 결과·실제 rc 없음 | 미수령 |
| INCOMPLETE | 중단/timeout/누락/해시 불일치/읽기 오류 | 성공으로 집계 안 함, 원본 보존 |
| CONTRADICTION | 동일 실행이라고 제시된 pin·설정·출처·값끼리 충돌 | 대조 중단, 모순 위치 기록, 임의 교정 안 함 |
| COMPLETE_NOT_ACCEPTED | 귀속/완전성은 충족, 문턱 또는 consume 조건 미달 | 미달 그대로, 자동 재시도/우회/다음 단계 없음 |
| REVIEWABLE | 필수 대조 충족 | 1저자 수용 대기; 실행/봉인 GO 아님 |

결측은 false와 다르다. 같은 자료에 모순과 미완료가 함께 있으면 둘 다 기록한다. 위 표는 한 숫자로 물리 자격을 요약하는 새 판정기가 아니다.

## 3. 결속 사슬

1. 발행한 블록 지문·소스 핀·하네스/복사 소스 지문 ↔ 실행 전 Git/환경/자원/운영자 확인 기록.
2. 단계별 별도 GO·start/stop UTC·DFT만 중지 ↔ 해당 실행 영수증. GO는 과거/다른 단계에서 빌리지 않는다.
3. 외부 ZIP/hash 목록 ↔ 실제 받은 바이트·CRC·집합 ↔ meta/rc/로그/결과의 같은 실행 귀속. 파일명이나 fresh 폴더 주장만으로 실행 신원 확정 안 함.
4. 선언된 결과 ↔ 아래 원필드/개수/기대·결측 대조. 요약 PASS를 다시 옮겨 적는 것으로 끝내지 않는다.
5. 원본 사본 보존 → 수령 검토 → 1저자 수용 → 다음 단계의 별도 결정. 공개 기록에는 주소·계정·현장 경로·원 로그를 넣지 않는다.

운영자 감시·절대 UTC 중단 시각 정책은 비준됐다. 자동 중단을 새로 넣지 않으며 Q11 기존5400초 호출은 그대로다. 실제 operator/environment/resource/start/stop 값은 여전히 null이다.

## 4. S0·저장본 대조 사례 — 설계14행 중 S01–S08

| ID | 제시된 상황 | 필요한 처분/근거 |
|---|---|---|
| S01 | DONE·셸rc0뿐, 자식rc 없음 | INCOMPLETE. monitor 종료는 자식 성공·포장 성공 아님 |
| S02 | childrc0·6파일 있음, 하나SHA 다름 | INCOMPLETE+무결성 모순. E1 불충족 |
| S03 | ADOPT_CANDIDATE지만 code_drift 비어 있지 않음 | CONTRADICTION. E3 원필드 확인 |
| S04 | read=30, build=200, write=500초 | COMPLETE_NOT_ACCEPTED. 절대600/300 이내여도 read/build=.15>.10 |
| S05 | HWM 증가3GiB처럼 보이나 hwm_reset 실패 | INCOMPLETE. T2 미확인; 5초 RSS 샘플로 대체 안 함 |
| S06 | 출력 새 경로라 argvSHA 다름 | 즉시 면제하지 않음. 새 경로 외 입력/설정 동일 증명, 없으면 미확인 |
| S07 | E4 settingsSHA가 다름 | 코드/시간 차이로 면제 안 함. 의미 설정 모순 조사 |
| S08 | E/T 충족, 새 S0 plan 채택 위치 미정 | REVIEWABLE까지만. 기존 watcher 계획 덮어쓰기/⑥ 자동 진행 없음 |

E1 여섯 출력·자식rc·PIN/clean·코드7지문, E2 감싸개1/instances117583, E3 encode/write/read/strict/registry/newobject/preload/error/machine-id, E4 배열2·의미 설정을 각각 확인한다. T1 write≤600/read≤300/read≤build×.10, build>0; T2 reset 근거를 갖춘 증가량≤4GiB; T3 파일≤2GiB. 유한 비음수와 단위를 먼저 확인한다. E1–E4와 T1–T3를 대신하는 8개 시험 통과 주장이 아니다.

## 5. Q11 대조 사례 Q01–Q06

| ID | 제시된 상황 | 필요한 처분/근거 |
|---|---|---|
| Q01 | rc0·adopt=true, 5쌍 중1쌍 빠짐 | INCOMPLETE/요약 모순. 실제10회와5쌍 완전성 |
| Q02 | 해 바이트 동일하지만 main/resolve info 비0 | COMPLETE_NOT_ACCEPTED. 동일 미수렴은 수렴 아님 |
| Q03 | short6회 중1회 iters199·info0 | COMPLETE_NOT_ACCEPTED. 고정200/200 조건 미달 |
| Q04 | GPU 출력9회, 나머지1회 CPU fallback | COMPLETE_NOT_ACCEPTED. 모두 GPU/jacobi/no fallback 필요 |
| Q05 | source_ok=true지만 material/hash/import 귀속 충돌 | CONTRADICTION. summary true로 출처 검사 대체 안 함 |
| Q06 | 5쌍/수렴/backend/반복/출처 모두 참, error=null, actualrc0, 완결 | REVIEWABLE. 속도비는 보고값; 실제 침대 가속/다른 환경/⑥ GO 아님 |

동일성·수렴·backend·반복·출처뿐 아니라 설정/핀/하네스/실제 rc/완전 출력을 묶는다. 기존 consume.adopt 술어를 수정하거나 JSON을 인증하는 새 프로그램이 아니다. 원문 Q11 return은 meta.txt/result.json/check.log·하네스/복사 소스 신원이며 공개 리포 밖에서 수령한다.

## 6. 다음 차례

두 단계의 개별 실제 GO → 원 결과 수령/대조 → 1저자 수용 → 지원 환경·시간/자원·operator·UTC 고정 및 새S0계획 연결 확인 → ⑥ 시도3 별도GO → 수령 검토 → 시도4 별도GO(시도3 저장본 유지). 14행은 아직 결과에 적용하지 않은 수령 설계이며 합성 회귀14/14로 세지 않는다.
