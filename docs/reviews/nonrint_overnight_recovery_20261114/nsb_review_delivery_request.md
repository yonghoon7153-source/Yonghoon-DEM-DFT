# NSB-F01·C01·C02 수정 후보 — 보존본 독립 재확인 전달

이번에 닫으려는 것: 세 NSB 지적의 수치·예정 음성 반례와 행렬 전파. 닫지 않는 것: 실제 DEM 자격·물리 타당성·값 접근·운영 봉인·실행 GO·공유 원장. 전체 HOLD.

고정 후보 c5aa7bb527c5cf0907651bae688bb97de206a8b6, 부모 a69095c7f1cc4908a14b93912d97cb93cc33eb64. 새 수정 후보가 아니라 11-10 보존 전달 폴더를 11-14에 포장한 것이다. 원 후보·원 폴더·시험·로그는 변경0, 이번 재실행0. 최신 수신=Claude 반입 창, 반입 가지 claude/sdcp-dem-manuscript-si-pqwtv8. 원 README의 stoic/당일ZIP제약 문장은 역사 상태로만 읽는다.

package/snapshot/docs/reviews/nonrint_nsb_fixes_20261110/review_request.md Q1–Q5로 검토한다. 우선 package/PIN_MANIFEST.json과 package/SNAPSHOT_MANIFEST.json, package/SHA256SUMS로 신원·집합을 확인한다. 기존 269파일/268해시/24snapshot은 그대로 포함되어 있다. 새 바깥 SHA256SUMS는 전체 전달본 목록이며 내부 목록과 별개다.

1. NSB-F01: 정수·혼합 int/float 역전구간·coverage·bias의 정밀도, 정확 평균과 ABS/REL 예산, 표시float/RMSE 한정.
2. NSB-C01: 원 int를 float로 바꾸지 않는 P2, 높이·KE 반례와 정상 경계.
3. NSB-C02: 검증된 두 zero·clear·완전POST1–3창과 고정4창 종료 예산을 갖춘 예정 음성. 빈trace/불완전sample 거부와 행렬 전파.
4. 기존 정상·승인false/NOT_RUN·수용 단위 보존. 신규 수치나 실제 자격으로 확대하지 않음.

원 판정의 실패 기대 replay rc0을 후보green으로 쓰지 않는다. 같은 expected-correct 회귀를 구본/후보에 적용한다. 역사 작성측 수는 원 README·검증JSON에 있으며 독립 확인 수로 옮기지 않는다. 이 전달 작업은 독립 판정이 아니다.

현재 이 대화와 확인한 B/대기열 문서에는 새 후보 판정이 미수령이다. 다른 창에 이미 결과가 있으면 중복 검토보다 그 고정 판정·증거를 실무 창에 전달한다. 없으면 이 후보를 좁게 검토하고 1저자가 판정문+증거를 실무로 돌려준다.

원 로그·재현 스크립트에는 작성 당시 scratch 경로가 있을 수 있다. ZIP 전체를 공개 리포에 반입하지 않는다. 재현 안내대로 새 scratch에서 경로를 지정하며 실제 호스트·엔진·MPI·원자료·전체 gate는 호출하지 않는다. 원본에 덮어쓰지 않는다.
