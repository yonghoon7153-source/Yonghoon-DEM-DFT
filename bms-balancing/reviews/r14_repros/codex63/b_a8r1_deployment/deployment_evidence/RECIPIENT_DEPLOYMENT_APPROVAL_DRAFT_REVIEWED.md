# 사용자 전달용 — 조건을 포함한 제한 배치 준비 승인 초안

이 문서는 초안이다. 사용자가 내용을 확인해 승인·전달할 때만 다음 범위의 권한이 생긴다. 현재 검토 요청의 승인을 배치 승인으로 해석하지 않는다.

---

수신한 COMSOL63_A8_EXECUTION_PLAN_20260924.zip(54,175 bytes / SHA-256 `696de7adf371d2d3a02bafee2a9d942765b3cead7198f3fd679ca357445e4783`)의 DEPLOYMENT_APPROVAL_DRAFT.md에 적힌 **api_recovery_B_A8R1 / saved_solution_A8R1_b006의 제한 오프라인 배치·경로 결속·재봉인 준비만**, 아래 추가 조건과 함께 승인합니다. B/COMSOL 실행 승인은 아닙니다.

기존 제안의 파일 변경 허용 목록, Java RUN/OUT 두 literal, path_binding.py의 TARGET_SHA만 변경, 11개 불변 파일, 현재 prefs 식별 채택 및 16개 보안값 동일 조건, 새 폴더 충돌 시 중지, 원본 보존을 유지합니다. 새 폴더가 있으면 삭제/재사용/fallback하지 마세요.

추가 필수 조건:

1. 새 deployment_binding driver가 D01–D16의 정확 집합과 각 ID의 양성 대조/거부 이유·단계를 검사합니다. count만 맞추거나 일반 예외를 기대 거부로 세지 마세요. D12에 빈 집합·누락·중복·실패 기록과 온전 대조를 넣고 공통 완료 소비의 PASS만으로 준비 완료를 만들지 마세요.
2. 최종 후보 raw 계약(approved=false/B_path_ready=true)을 시험 전 seal에 포함하고, 그 객체의 한 필드만 false인 view를 검증합니다. D10에서 다른 필드·타입 차이/approved=true를 거부하고, D11에서 실제 승인 검사와 최종 raw manifest 결속을 확인하세요. 승인 없음/false/다른 run·manifest와 정상 fixture 대조를 포함하세요. 실제 승인 파일은 만들지 마세요.
3. 시험이 본 raw 계약/코드/독립 target과 최종 CODE_MANIFEST가 가리키는 바이트를 마지막에 대조합니다. 시험 뒤 계약 플래그를 변경해 다른 바이트를 같은 시험 결과로 인증하지 마세요. 완료·외부 반환이 미완이면 후보 파일이 있어도 준비 완료로 보고하지 마세요.
4. 기존 launcher의 TTY 검사는 apply Desktop 실행 이후라는 사실을 B 초안에 명시하세요. 같은 실제 호출 경로에서의 TTY/현지 입력 사전 확인은 미완인 B 착수 조건으로 남기세요. 이번에는 launcher/transport를 수정하거나 TTY/native를 시험하지 마세요. 별도 선행 gate가 필요하면 변경안을 제시하고 멈추세요.

기존16개 ID는 유지하되 그 안의 하위 사례와 실제 실행 수를 공개하세요. 전체 제한 suite 최대2회, 각300초/누적600초, 첫 완전 통과 뒤 반복 금지를 유지합니다. 첫 실패를 보존하고 허용 범위 수정·새 seal이 있을 때만 두 번째가 가능합니다. 부분 probe/AST 실행으로 횟수를 우회하지 마세요. 기존389 suite·실제 F는 실행하지 않습니다.

배치/연결 구현3600초, 정적 누적300초, 제한 suite 누적600초, 보존180초, 전달·외부 최종화600초, 정리/미완60초 및 착수부터 전체7200초를 승인 범위로 합니다. 미사용분 전용은 없습니다. 새 원점·예약·완료/외부 반환으로 기록하세요. 시작 RAM4GiB/디스크6GiB, Python working set2GiB 미만, fixture 누적4GiB 이하, 생성 경로220자 이하 조건을 유지합니다.

실제 RUN/사용자 승인/token은 생성하지 않습니다. fake approval과 inert sentinel은 소유 fixture에서만 사용하고 방어를 먼저 설치하세요. COMSOL/JVM/compile/batch/loadCopy/Evaluate/Export/solve, 실제 process/Job/UI, prefs/registry/ACL 변경과 기존 pending 해소는 모두 제외합니다.

예상 밖 변경이 필요하거나 예산·식별·증거·정리 조건을 만족하지 못하면 미완으로 보고하고 멈추세요. 소스 diff·역치환·불변 SHA·ID/하위 결과·raw/view 대응·최종 manifest·완료와 최종 반환·보존 대조·아직 비활성인 B 승인문을 제출한 뒤 종료하세요.

새 B_path_ready=true는 경로 준비 의미만입니다. B 실행 승인 및 usable은 false이며 실제 B 승인은 고정 실행본 독립 검토 뒤 사용자에게 별도로 요청해야 합니다. 기존 A7/A8/failed/b003 pending·원복/MPH/ZIP/영수증은 보존합니다. 정상 gate/API 복구/전체 수렴 미완·장시간 보류·1198/후보C 미승인을 유지합니다.
