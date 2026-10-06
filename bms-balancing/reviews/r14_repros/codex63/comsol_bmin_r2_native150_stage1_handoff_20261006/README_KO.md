# BMIN150 사전 관측 외부 전달 자료

2026-10-06. 사용자가 요청한 외부 실행 기기 Codex용 1단계 승인·작업지시문이다. 현재 검토자 앱에서 BML 실행 기기의 대상 대화를 확인할 수 없어 직접 메시지를 보내지 않았다. 외부 작업은 이 자료를 사용자에게서 전달받은 뒤 시작한다.

기존 COMSOL 작업을 담당한 **BML 실행 기기의 Codex 대화**에 ZIP을 첨부하고, `SEND_TO_EXTERNAL_CODEX_KO.md` 본문을 사용자 메시지로 붙여 넣으면 된다. 다른 검토용 PC나 클라우드에 같은 경로를 만들어 대신 실행하지 않는다.

- `SEND_TO_EXTERNAL_CODEX_KO.md`: 실제 전달할 1단계 승인·작업지시문. COMSOL 실행 승인은 포함하지 않는다.
- `READONLY_REFERENCE_SNAPSHOT.json`: 고정 커밋 `e4e06889338f22df53e4d4ece9e29e1131570fad`에서 읽은 요청문과 4개 후보 JSON 원문. 배치용이 아닌 비교용 데이터다.
- `HANDOFF_IDENTITIES.json`: 받은 텍스트의 Git blob·SHA 및 N150-N1/N2 정정 확인.

검토자가 이번에 만든 파일은 이 전달 자료뿐이다. 실행 기기 사전 관측·실제 승인 파일 생성·후보 변경·시험·COMSOL 호출은 하지 않았다. 앞선 리뷰 ZIP과 원문은 변경하지 않았다.

OpenAI Docs 및 write-page 스킬에 따라 지시문에서 대상·제약·종료 조건과 근거 자료를 구분했다. 작성 참고는 [OpenAI Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)이며, 이 문서는 COMSOL 작업 권한의 근거가 아니다. 권한은 사용자가 전달하는 이번 1단계 승인 범위로만 정한다.
