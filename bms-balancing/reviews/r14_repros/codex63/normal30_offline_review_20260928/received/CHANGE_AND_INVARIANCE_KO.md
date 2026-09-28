# 변경 경계와 불변 근거

출발 manifest `0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45`, Java `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95`를 실제 파일과 대조했다. 새 manifest는 `28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5`다.

| 범주 | 최소 변경 | 불변 또는 검증 필요 |
|---|---|---|
| 모델/물리 | 시험용1198→기존 정상0, 요청 끝5→30 | physical300, particle320·320,0.1C,sigma1e−20, 초기재고·조성·물성·OCP·초기화 본문 불변 |
| 시간 |187개 prefix 유지 +250개 요청; checkShape 상한30; readback0 | cap식,初step,rtol,strict/all stored,stepbefore_stepafter 및 세guard 식/selection 불변 |
| 출력 |30초 표식·시간 범위 | BASE64·35개 표의 API·단위·241좌표·selection·형상 처리 본문 불변. 실제 상태 수는 미정 |
| 식별/경로 |class Normal30Candidate,새root/run/approval/결과명 | 기존baseline6개,외부소스 핀,고정Python/cwd 유지 |
| 오류 보존 |새 종료 분류와 부모 마지막 오류 시 limited=INCOMPLETE | Java catch/report 본문·consumer 공통 실패 schema·entry 최초/후속 오류 보존 유지 |
| 소비 |정상30/보호중단 구분,strict/full intersection,초기Li각항,후기요약,설정읽기 | 새 분기는 기능 검증 전. 이전1198 성공을 새 분기 PASS로 확장하지 않음 |
| 실행 연결 |native30 승인 필드·제안 예산·디스크20GiB | C2 input/timed_attest와 owned Job 제어 불변. 새 monitor 없음 |
| 부모 |GDecision 새 schema/rc 분기,완료경계 명시 | BInvoke/BSave 본문 유지. OS 종료코드 미포착은 null |

`JAVA_ALLOWED_REPLACEMENTS.json`에 허용 literal/횟수가 있고, 역치환은 원 Java 전체 바이트와 같다. 따라서 허용 변경 외 모델 생성·physics/mesh/solver 본문 변경이 없음을 정적으로 확인했다. `SOURCE_DIFF.patch`는 원본과 최종 후보를 연결한다. 이전Java를 baseline 사본으로 포함했다.

정적 `.runAll()` 1개 / loadCopy0 / getPreference0은 호출문 계수이며 미래 실행횟수의 실측이 아니다. native 사양은 compile≤1/batch≤1/solve≤1, 추가control0/retry0다.

새 소비자가 설정 CSV의18개 기존 key와437개 요청 목록을 검사한다. B020의 메타데이터 예외를 복사하지 않았다.1198에서 이미 사용한 출력 API 경로를 재사용하지만 새로운 전체 모델 컴파일/API 호환성을 이번 정적 검사로 보증하지 않는다.
