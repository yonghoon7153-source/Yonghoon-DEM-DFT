# 1198 변경부 한정 검증 — 수신 검토

2026-09-28. **G1198-N1/N2 종결 수용. 봉인된 26개 논리군·78개 하위 사례의 한정 오프라인 검증 결과를 수용한다. 실제1198 실행 GO는 아직 아니다.**

현재 검토 범위에서 새 P1/P2 구현 보완 요구는 없다. 동일 suite를 반복하거나 B020 결과를 다시 회수할 필요도 없다. 다음은 현 정책·정확 실행 경로의 읽기 전용 확인과 단발 native 승인문 확정이다. 이 문서는 사용자 실행 승인을 대신하지 않는다.

## 1. 직접 확인한 파일 식별

- 수신 ZIP: 1,304,867 bytes, SHA-256 `6af5463ed0d395353de1a9935088c1d6f9503e476d0b5bc1fc9fb65ab80903d1`.
- 851 payload + PACKAGE_MANIFEST, 총852 entries. 집합·각 크기/SHA·CRC·중복/대소문자 충돌·경로 이탈·링크 검사 통과.
- package manifest SHA `d91a8ae5cf1c6cebb58808e2bc562ff9433eb3d48e0a8c29d57a215e940e54c0`.
- 후보 CODE_MANIFEST SHA `0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45`, 봉인 파일5개 모두 일치. approved=false/usable=false.
- Java SHA `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95`는 최초 오프라인 준비본과 전체 바이트 동일하다. 물리 본문을 다시 계산하거나 컴파일한 판정이 아니다.
- history의 attempt03 실패 ZIP 814,051 bytes / SHA `2d6fcf6947bf18347a5266949c9527a72eabd0b2ab2f1934c6f701f4c461aeda`, 635 payload+manifest도 직접 검증했다. 후보5개와 CODE_MANIFEST 사본은 attempt03→04 바이트 동일하다. COMMAND_MAP/승인 문서는 attempt03에 해당 사본이 없어 동일성 대조 대상6개에 포함하지 않는다.

근거: PACKAGE_AUDIT.json, EVIDENCE_AUDIT.json, 수신 원본 reference/ 및 received/.

## 2. 앞선 지적의 종결

### G1198-N1 — 수용

`trigger_consumer.py:175`의 incomplete_result가 limited_result를 처음부터 INCOMPLETE로 만든다. `candidate_entry.py:146`에도 같은 기본 schema를 두었고, state/consumer loading·추출·분석의 예외를 감싼다. 기록 실패는 원래 오류 목록을 유지하며 추가하고 stdout의 analysis_result로 남긴다.

실제 검증 연결은 tests/run_python.py의 run_analysis이며 entry.analyze→원 consumer를 호출한다. PY02/03의 잘못된 binding/guard/native사유, PY14의 추출 실패·기록 실패·예산 실패가 INCOMPLETE/rc1과 원래 이유를 유지한다. 기록 실패 사례에 trigger 원인과 record 원인이 함께 보존되며 추가 KeyError가 없다는 assertion·관측을 확인했다. 양성은 실제 producer 결과를 records/positive_result.json에 저장해 다음 PowerShell 검증에 사용했다.

따라서 이전의 “limited_result 없는 정상 반환 뒤 추가 KeyError” 지적은 닫는다. 모든 가능한 외부 파일 쓰기 장애의 영구 기록 보증으로 확대하지 않는다.

### G1198-N2 — 수용

`PARENT_COMMAND.ps1:43`의 실제 GDecision에 축별 상태, pair/native_stop/numeric/coverage, 필수 tables_manifest의 구조·식별 검사와 normal gate/정책 한계가 추가됐다. CSV 수치 분석기 전체를 부모에 복제하지 않았다.

tests/run_parent.ps1은 파서로 BSave/BInvoke/GDecision 원문을 추출한다. 저장된 PS_EXTRACTED의 세 함수가 부모 원문에 그대로 포함됨을 직접 확인했다. 실제 Python 양성 결과를 부모 양성 대조로 사용하며, 각 축 누락/미완, 요약만·핵심 증거 누락/빈 구조·빈 coverage·잘못된 식별·native/analysis rc·시간 반례를 INCOMPLETE로 거부한 기록과 assertion을 확인했다.

이전의 “핵심 증거를 읽지 않고 요약만으로 수용 대기” 지적은 닫는다. 완전 양성도 AWAITING_LIMITED_EXTERNAL_ACCEPTANCE이며 전체 실행 PASS나1198 승인으로 승격하지 않는다.

## 3. 시험 집계와 실제 소스 연결

| 범위 | 논리군 / 하위 사례 | 수신 근거 |
|---|---:|---|
| Python | 14 / 30 | 실제 candidate consumer/entry, 기존 입력 함수에 inert adapter. 사례별 이유/단계와 rc 기록 |
| Java helper | 6 / 13 | 후보에서 추출한8개 method+catch 블록, stub 모델과 순차 assertion. 6개 군 완료 stdout |
| Windows PowerShell5.1 | 6 / 35 | 실제 BSave/BInvoke/GDecision 추출, Python producer 양성 및 음성 객체 |
| 합계 | 26 / 78 | CASE_MAP과 RESULTS의 고유(group,case) 집합 일치; FAIL/NOT_RUN0 |

Python/PowerShell의65개 사례는 개별 결과와 정확히 연결된다. Java13개는 봉인된 순차 assertion을 통과한 뒤의 군별 완료 표식6개로 연결된다. 13개 별도 stdout 기록이 있다는 뜻은 아니다. Java9개 추출 범위의 텍스트 SHA와 후보/GuardHarness 포함 관계를 직접 확인했다. J06의 PRIMARY/REPORT_FAILURE 스택은 예상 복합 오류 주입이며 그 뒤 J06 PASS 및 외부rc0이 있다.

수신 도구 반환: Python63b6c1 rc0/6.9521027초, helper compile c89e5c rc0/1.6089183초, stub JVM be1a61 rc0/0.6148349초, PS5.1 7ae5a8 rc0/2.6136205초. 수신 파일에 저장된 도구 반환의 직렬화이며 검토자가 원격 실행을 직접 관측하거나 원시 OS 감사를 확보한 것은 아니다.

시험 전후22개 pin 목록은 같다. 그중17개는 수신 파일 또는 이전 수신 source 사본의 바이트로 직접 대조했다. 나머지5개(Python/PowerShell/javac/java/release)의 현지 실행파일 식별은 발신 기록으로 남기며 원격 PC를 재측정했다고 하지 않는다. 선택 보존14개 before/after 기록도 같다.

실제 argv 비교는 유지했고 cwd 기대값만 `str(Path(...))`로 맞췄다. assertion 전 실제 전달 인자를 기록하는 한 줄이 추가됐다. newline 정규화 diff로 이 제한 변경을 확인했다. R1 후보의 이번 시험 중 변경은 없다. 최초 준비본 대비 R1 변경은 앞선 두 지적과 새 폴더 경로 결속이다.

## 4. 실패 보존과 수용 한계

attempt03은20 PASS/1 FAIL/57 NOT_RUN으로 남아 있다. PY11의 EXACT_ARGV_CWD 및 CLEANUP_NOT_CONFIRMED를 지우지 않았다. attempt04의 START는 새 사용자 승인에 따른 한 번의 검증이라고 기록한다. 이 기록을 보고 여기 없는 원래 대화 승인 문구까지 독립 확인했다고 하지 않는다. 과거 두 준비 중단의 전체 자료를 이번 ZIP이 재검증하는 것도 아니다.

수신 검토자는 동봉 모듈·harness·class를 실행하지 않았다. archive/hash/JSON/source/AST 텍스트 대조만 수행했다. 리뷰어의 첫 archive reader가 history 사본 경로를 같다고 가정한 오류는 REVIEWER_DIAGNOSTIC_NOTE.json에 구분했고, 관측한 경로에 맞춰 대조했다. 후보 시험 실패나 원본 수정이 아니다.

stub/합성 검증은 실제 COMSOL 전체 Java 타입 호환성, 현재 CLI 정책 허용, 실 사용자 콘솔, native1198 발동·수치 정확성·소유 정리의 실제 성공이 아니다. 그 부분은 제한 native 시행의 목적/잔여 조건이다. B020의 정상 전체 gate·전체 수렴 INCOMPLETE와 기존 failed/pending은 그대로다.

## 5. 비차단 기록 보충

### V-O1: 보완 설명의 SHA 대상 구분

CORRECTION.after_harness_sha256=`352ed9d4183b4d5629d3b74fa33c74f9788e62c5025d060b735f71231b911e35`는 수신 harness의 CRLF를 LF로 정규화한 텍스트 SHA와 일치한다. **실제 파일 raw SHA는** `5cbe34b28b53a6034b5cf8e8d819aae21c1813fc4f1a53bd6bd83bd8f04d95b4` /17,527 bytes이며 PRE_TEST_SEAL·FINAL_SOURCE_BINDING·PACKAGE_MANIFEST가 이 실제 값을 일관되게 가리킨다.

실행 코드 봉인 불일치가 아니다. 다음 별도 보충 기록에서 normalized/raw의 뜻만 구분하면 된다. 기존 CORRECTION이나 봉인본을 덮어쓰거나 시험을 재실행할 필요는 없다.

### V-O2: 전달 마지막 경계

PACKAGING_BOUNDARY는 ZIP 생성 전의 overall367.2761274초, pack117.9327846초다. 최종 ZIP 밖 DELIVERY_RECEIPT와 마지막 포장 도구 반환은 이번 파일에 없어 마지막 전달300초·전체1200초 종결을 직접 확인하지 않았다. 네 시험 엔진rc0 및 해당 호출 시간과 이 최종 포장 경계는 다르다.

기존 원문이 있으면 사본만 보충하면 된다. 이 결손은 한정 기능 시험 수용을 되돌리는 이유가 아니며, 종결 시간을 임의 계산하거나 기존 시행을 다시 돌리지 않는다.

## 6. 다음 결정

**한정 오프라인 시험 수용 → 현 정책·실행 경로 읽기 전용 확인 및 승인문 확정 → 사용자 별도1198 최대5초·1회 승인 → 결과 수용 → 별도30초 진단 승인** 순서다.

다음 작업은 코드를 또 만들거나 suite를 반복하는 일이 아니다. 고정 R1 실행 위치와 현재 prefs 식별, 필요한 읽기/쓰기별 근거, 부모 명령/기록/자원·예산·중단 조건을 한 번 확정한다. CLI 현재 성공을 읽기 전용 검토로 입증했다고 하지 않는다. 근거상 차단이 분명하면 원인/최소 승인 필요 범위만 제시하고 멈춘다. 단지 native 미관측이라는 이유로 같은 일반 진단을 반복하지도 않는다.

실제 승인/release/runtime/token 생성·정책변경·COMSOL 실행은 이번 수용에 포함되지 않는다. NEXT_PREEXEC_DIRECTIVE_KO.md는 사용자가 채택할 다음 작업지시 초안이다.
