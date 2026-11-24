# Claude 수영 반환 수령 안내

보고용 원고는 weekly_1130.md, 교수님용 그림은 weekly_phi.png, 원표·궤적 SHA는 weekly_phi.csv에 있다. report_ko.md에 기존 모델과 수정 후보의 분자·분모·초과 표본 수와 각 팔 실행 시간을 병기했다.

로컬 판독 명령은 배포본과 같은 WSL Python·NumPy를 사용해 `python -I -X utf8 -B recheck.py OPERATOR_TXT OLD_RETURN_DIRECTORY NEW_RETURN_DIRECTORY`이다. OPERATOR_TXT는 실행 핀 182be9d50d58의 원래 TXT이고, 두 입력은 각각 기존 설정 ②의 F 반환 폴더와 이번 후보 반환 폴더이다. 네 팔을 새로 적분하는 동작은 없다. 별도 검산은 `python -I -B independent_readback.py NEW_RETURN_DIRECTORY`로 한다.

이 패킷은 반환 수령본이다. 프로젝트 바탕으로 지정된 566d5af7e을 아직 원격에서 가져올 수 없어 정식 프로젝트 커밋과 push는 대기한다. 원 반환 TAR와 화면은 1저자 보관본을 쓴다. 1저자가 반입을 지시한 뒤 결과 문서만 프로젝트에 옮기고, 11-30 수영 문단에는 이번 주간보고 문안을 사용한다.
