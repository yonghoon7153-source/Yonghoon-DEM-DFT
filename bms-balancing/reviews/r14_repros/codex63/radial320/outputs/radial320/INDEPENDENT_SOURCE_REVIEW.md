# R320 독립 소스·출처 감사

**소스 감사 PASS.** 기준은 `Caps300R160H0250`, job `15e5d7433a6a4956b820cf6952330735`, 실제 소스 SHA `4b4ff66bca7a161f6acffd5b125ddf695fee95fb82cdb4ded1e8b63391e1e5f0`이다. 새 소스 SHA는 `837f8b03ff3381bb1aea6397935d0079b032f5e4aea007b32d1ebf7c40775b2e`이며 제출한 job은 `f0db6d080ad04045a2b43dc5a51d89b2`이다.

607줄 전체 소스 바이트를 비교했다. class/label의 이름 두 곳과 N/P의 `Nel` 160→320 두 곳만 바뀌었다. 재료·OCP 표 수치, Li 재고·초기조건, 물리 mesh 120/60/120, 0.1C, `sigma_short=1e-20 S/m`, 187개 지정 시각과 5 s 종료, Time/Variables 설정 및 출력·guard 코드는 동일하다. 새 solver API나 외부 읽기·네트워크·프로세스 실행 호출은 추가되지 않았다. exact diff는 `INDEPENDENT_SOURCE_DIFF.txt`에 있다.

두 실행의 cap은 `if(t<0.1[s],0.00025[s],0.1[s])`로 같다. worker timeout 600→1200 s는 실제 소요시간 허용 상한이며 물리시간 또는 solver 설정 변경이 아니다. cores는 2로 같다. 실제 mesh/DOF/Time/Variables/accepted step와 완료 여부는 별도 `INDEPENDENT_NATIVE_AUDIT`에서 판단한다.

OCP·entropy 네 함수의 extrapolation은 `none`이다. 고체 표면 조성/OCP 범위 StopCondition은 step 이후 검사이며 모든 Newton trial의 유효성을 입증하지 않는다. 전해질 양수 검사는 **후처리 전용**이다. 이전 실패 job `08e0...`의 failed 상태·SHA와 `INCOMPLETE_RANGE_STOP` 분류는 유지한다.

제출 전 native job 28개, request/status/Java/console/batch/compile 189개 파일에 R320 중복 후보가 없었다. 정확한 사전 검사 시각은 기록되지 않아 새 request 생성시각 `2026-09-14T08:03:52.565527+00:00` 이전이라는 순서만 명시한다. 28개 기존 job ID와 후속 읽기에서 고정한 파일 SHA는 `DUPLICATE_CHECK_BEFORE.json`에 있다. 현재 새 실행은 위 job 한 개다.

이전 R160_TIMECAP ZIP의 현지 바이트는 307,305,998 및 SHA `481ce9ebb1455de18ffcc35554d34b8a5fceb5c8cea3018938a200fadd920bdc`이다. 내부·외부 원본 manifest가 같고 267 payload/268 entries이다. 이번 독립 검사는 outer SHA와 manifest identity를 재확인했으며 payload 전체 CRC/개별 SHA를 다시 실행하지 않았다. 과거 전체 검증 영수증과 이번 사용자 수신 확인은 별도 증거 수준으로 `PROVENANCE_LEVELS.json`에 기록했다. 현재 867개 파일 보존 ledger는 **현지 명세**이며 전체가 수신 측에서 독립 검증됐다는 뜻이 아니다.

본 감사는 COMSOL 실행이나 기존 파일 수정을 하지 않았다. 소스의 승인 범위 적합성과 native 수치 검증은 별도다.
