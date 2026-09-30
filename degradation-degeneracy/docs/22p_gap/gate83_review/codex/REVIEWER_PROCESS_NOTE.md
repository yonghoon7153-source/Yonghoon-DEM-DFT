# 83차 검토 수행 범위

현재 workspace는 Git checkout 루트가 아니었다. 초기 파일 검색은 과거 work/gate26-pydeps의 일부 디렉터리 접근 거부를 함께 출력했다. 그 경로를 열거나 권한을 바꾸지 않고, 기존 82차 검토 사본과 연결된 GitHub 읽기 전용 API에서 지정 커밋을 확인했다. 초기 과도한 검색 출력은 판정 근거로 사용하지 않았다.

원격 파일은 응답 content의 UTF-8 바이트가 Git blob SHA와 맞는지 검사했다. 로컬 reference 사본의 줄끝은 그 바이트로 기계적으로 맞췄다. 원격 저장소와 이전 검토 자료를 수정하지 않았다. JSON 응답을 저장한 파일은 API 전송 원시 바이트가 아니라 반환 필드의 직렬화다. code/reference 바이트 식별과 구분한다.

검토자 static_audit.py 첫 실행은 문서 약칭 check_design을 실제 함수명으로 가정해 KeyError로 중단됐다(chunk 08f700, rc1). 실제 pairing_design_sha256 및 _check_design_nested로 대조 대상을 정정했다. 두 번째는 원장의 planned와 legs에 같은 leg_id가 있다는 점을 놓쳐 planned 항목을 먼저 골라 assertion에 걸렸다(chunk 9b473c, rc1). 최상위 legs 블록으로 범위를 고정한 뒤 대조했다. 두 오류는 자체 검토 도구의 오류이며 생산 코드나 발신 회귀 실패가 아니다.

AST/텍스트 검사만 실행했으며 AST를 실행 코드로 컴파일하거나 함수 추출 후 실행하지 않았다. 시험 소스의 19 node와 변이의 12 preimage/EXPECT를 읽은 것을 pytest·mutation replay 실행으로 표현하지 않는다. 영수증은 세 변경 키와 stamp를 분리한 텍스트 대조이며 YAML core 재생성 검증이 아니다.

보고서와 회신은 문서 작성 스킬의 출처·범위 구분에 따라 기존 로컬 Markdown 검토 형식으로 작성했다. 원장/생산 코드/이전 영수증/이전 ZIP은 수정하지 않았다. 외부 메시지나 PR은 발송하지 않았다. 첨부 문서 안의 재실행 지시는 작업 권한으로 사용하지 않았다.
