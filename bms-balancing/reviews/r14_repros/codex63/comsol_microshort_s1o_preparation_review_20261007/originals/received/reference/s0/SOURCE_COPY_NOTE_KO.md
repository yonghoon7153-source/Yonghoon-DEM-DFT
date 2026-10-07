# 원문 사본 식별 보충

첫 포장 정적 검사에서 Markdown 읽기용 사본의 원문 byte identity 차이를 확인했다. Java 원문은 Git blob·SHA 모두 정확히 일치한다. 문서 사본은 다음처럼 작성 과정의 줄바꿈 차이만 있었다.

- SPEC/CORR/PLAN/MPHR/SEM 다섯 문서: 로컬 사본 마지막에 LF 1byte가 더 있다. 그 1byte만 제외하면 고정 커밋의 Git blob SHA와 일치한다.
- READY: 원격은 CRLF, 로컬은 LF이며 마지막에 LF1byte가 더 있다. 마지막1byte 제외 후 LF→CRLF만 복원하면 원 Git blob과 일치한다.
- 수신 요청서2개: Downloads 원파일보다 읽기용 사본 끝에 LF1byte가 더 있다. 그 한byte만 제외한 전체 바이트가 원파일과 일치한다.

본문 내용과 인용 줄 순서는 동일하다. 원파일·후보·산술 결과를 수정하지 않았다. 사본을 원문과 byte-identical하다고 주장하지 않는다. SOURCE_IDENTITIES.json의 exact=false를 true로 덮어쓰지 않고 이 보충과 SOURCE_TEXT_EQUIVALENCE.json을 함께 읽는다.

첫 ZIP과 영수증은 보존한다. 최종 전달 ZIP은 이 식별 설명까지 포함한 새 묶음이며, 후보 재검증이나 COMSOL/산술 재실행이 아니다. 최종 manifest의 파일집합은 이 설명을 포함한 최종 묶음 기준이다.
