# Claude 전달용 — GATE68 수신 결과

대상 HEAD `a1979cdf5b9f04234b6a441150e161bd4f0a3ced`.
RUN_SCOPE `743f65bead671bf353ce38027c2e8e457738ec08`, source_digest `e9ee7475dea7de1d` 직접 확인.

**부분 수용 / 종결 NO-GO. 잔여 P2 1건(G68-T1).**

- N1: 정직한 OFF/ON namespace 수용, absent 위조 parent/entry 거부. 수용.
- N2: 자기 경로를 제거한 ZIP package와 원래 대조군 entry 수용. 지원 범위/로드 시점 증명 한계를 유지하며 수용.
- T1-b: 변경 witness를 포함한 네 등록 변이의 baseline·정확 실패 집합·call·witness 일치를 독립 확인. 수용.
- T1: usage error/collect-only 및 상속 옵션 경계는 수용하나, call 실행 증거의 종결은 거부.

## G68-T1의 실제 반례

원본 `_premise_run`의 명시 `env_extra`에 `PYTEST_ADDOPTS=--setup-only`를 준다. child rc 0, 정확한 두 JUnit testcase에 failure/error/skipped 없음. 실제 phase 관측에는 setup/teardown만 있고 **call 0개**다. 그런데 `assert_premise_actually_ran`이 ACCEPTED/미측정 []를 반환한다.

JSON-report plugin을 빼고 실제 커밋된 `test_g66_08...`에 같은 env_extra를 줘도 정상 반환한다. 정상 대조는 실제 두 call PASS, collect-only는 AssertionError다. 가짜 CompletedProcess나 제품 코드 변경은 없다. 이 주입 통로는 커밋된 G67-T1 회귀와 같고, 상속 env 제거가 깨졌다는 주장이 아니다.

원인은 `test_gate66_defensive.py:284`의 기본 passed 분기와 `:289` 이후 소비자가 JUnit testcase 상태를 call report로 취급하는 데 있다. exact full node ID + 실제 call-phase evidence를 요구하고 오류/skip/미측정/중복/누락을 구분하라. rc나 요약 passed 수만으로 대체하지 말 것. 정상·usage·collect·setup-only와 상속 경계 대조를 같은 실제 소비 경로로 검증해야 한다.

수신 측 portable suite는 52 passed/2 skipped/1 deselected. Linux native·전체 suite·strict smoke는 미실행이며, 제출 측 전체 실행을 실패로 소급 분류하지 않는다. 새 반례는 증거 소비 계약의 잔여다.

## 문서 정정

1. `a31be7a9→HEAD` dd diff는 요청문 머리 20줄 추가라 rc 1. 그 문서 제외 시 rc 0. 최종 HEAD의 “한 바이트도 변경 없음”은 정정.
2. 발송문 “본실행 GO 요청”과 정본 “GO 요청 안 함”을 일치시킬 것. 이번은 종결 검토이며 본실행 보류.
3. 삭제한 175건은 재실행으로 같은 종류를 새로 생성할 수 있어도 원래 바이트/역사의 복원이 아니다. 복원 가능성 표현을 좁힐 것.

다섯 질문에 대한 답·원출력·재현 소스는 `GATE68_REVIEW_KO.md` 및 동봉 증거에 있다. N1/N2/T1-b 종결을 유지한 최소 후속 보완안을 제시하면 된다. P0-1/P0-4/등록부 격리·F50b 기존 경계는 유지한다. 이 회신은 COMSOL·본실행·삭제/복원·class 변경 또는 자동 재시험 승인이 아니다.
