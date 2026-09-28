# 1198 오프라인 준비본 독립 검토

2026-09-28 · 사용자 지정 xhigh 수준의 읽기 전용 검토.

**판정: 후보의 방향·모델 보존은 수용. 현 봉인본 그대로의 검증 완료/1198 실행 승인은 보류. P2 연결 문제 2건을 좁게 정정·재봉인한 뒤 변경부 한정 검증으로 진행하는 것이 다음 작업이다.**

개괄 계획을 다시 작성하거나 기존 전체 suite를 다시 여는 것은 요구하지 않는다. 아래 지적은 새 후보의 실패 결과와 부모 소비 연결에 한정된다. 이번 검토에서 동봉 코드를 수정·import·실행하지 않았고, COMSOL/JVM/PowerShell 시험도 하지 않았다.

## 1. 직접 확인한 무결성과 재사용

- 수신 ZIP: **236,582 bytes**, SHA-256 `e8f544c01e3e8e8ba4ab27f294f1b8bb9124707ee0cfc38e2023a42f731279ec`.
- 62 payload + PACKAGE_MANIFEST, 총63 entries. 정확 집합·크기/SHA·CRC·중복/대소문자 충돌·경로 이탈/링크 검사 통과.
- package manifest SHA: `7bc05fae8cb3400f73045f1ffc92b352774d9c170360e40e017e6cac8cb50ac4`.
- CODE_MANIFEST SHA: `0994d919ed1317a1234dbc2ba4276d5a7342401bbaed1ffcd2e45a69b8a13bcf`. 봉인된 코드/계약5개를 대조했고 approved=false/usable=false를 확인했다.
- Java 후보 SHA `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95`. TRANSFORM_RECORD의 11개 치환을 검토자 데이터 처리로 역적용했을 때 원 Trigger 전체 바이트와 일치했다. 후보 생성 스크립트는 실행하지 않았다.
- basis20개 전부를 이전 수신 guard/B020 ZIP 원문과 직접 대조했다. 기준CSV6개도 이전 수신 ZIP의 크기·SHA와 일치한다. baseline의987시각에 strict요청187시각이 정확히 포함돼 있음도 데이터로 확인했다.
- 기존 검토 문서3개는 우리가 전달한 원문과 바이트 동일하다.
- PRESERVATION_BEFORE/AFTER의 선택29개 식별 기록은 같다. 이 중 수신자가 직접 확보한 사본/이전 ZIP의 대조와 발신 PC의 전후 관측은 구분한다. 현재 원격 파일29개나 모든 프로세스를 직접 재검증한 것이 아니다.

근거: PACKAGE_AUDIT.json, DATA_STATIC_AUDIT.json, FAILURE_SCHEMA_EVIDENCE.json, PARENT_SCHEMA_CASES.json.

## 2. 수용하는 구현 방향

1. 옛 comp1.x argmin3열을 제거하고 동일 Minimum/1198/세 guard와 stepbefore_stepafter를 유지했다. 물리 모델 작성 본문 및 runAll 호출의 의도한 계산은 보존됐다. static runAll1은 미래 실제 solve1 관측이 아니다.
2. 새 readback·단위/형상 검사·dynamic 저장시간·Interp solnum을 출력 변경으로 구분한다. 추가 검사가 새 예외를 발생시킬 수 있으므로 역치환 일치를 native 동작 동등성으로 확대하지 않는다.
3. 조기 종료 소비자는 t_minus/t_plus, 초기false→최종true, 다른 guard0, native 중단사유, 이후 적분 없음과 표본 비교를 나눈다. 원 native1198 결과는 아직 없으므로 새 로그/형상의 실제 수용은 미검증이다.
4. coverage는 요청prefix 누락·빈집합·t=0만의 비교를 거부한다. 기준 전체987행을 새 조기종료 결과에 강제하지 않는다. 좌표241/domain/유한값/단위/Li/전압 항등식 검사도 존재한다.
5. B020 후처리 launcher.main을 새 solve에 재사용하지 않고 기존 C2 입력 본문/검증 로더/private Job transport만 사용하도록 연결했다. getPreference 재도입·정책 완화·새 메모리 감시기를 넣지 않았다.
6. 기존 코드로 가능한 시작 RAM/디스크 관측·디스크10GiB 문턱·wall-time/소유 정리와 미구현 메모리 감시를 구분한 것은 적절하다. 내부 실효 정책 및 native API/정리의 한계는 유지한다.

78건은 정적 존재/식별 검사이며 기능 시험이 아니다. 이번 2건은 그 차이를 보여준다.

## 3. G1198-N1 · P2 — 초기 실패 반환에 limited_result가 없어 추가 KeyError

**위치:** `src/trigger_consumer.py:176–181`, `src/candidate_entry.py:151–161`.

consumer.analyze의 초기 result에는 limited_result가 없다. binding/guard/native_stop이 실패하면 trigger 예외 처리에서 곧바로 그 result를 반환한다. 호출부는 정상 반환으로 받아 tables_manifest·run/manifest·시간을 추가하고 TRIGGER_RESULT.json을 쓴 뒤, 같은 줄의 print 및 rc 결정에서 `result['limited_result']`를 필수로 읽는다.

예를 들어 잘못된 native중단사유가 있으면:

`NATIVE_STOP_REASON → trigger 축 오류를 담은 반환 → limited_result 없는 파일 저장 → print의 KeyError('limited_result')`.

원래 trigger 오류가 파일에서 삭제되는 것은 아니다. 하지만 예상된 실패가 일관된 INCOMPLETE 결과/반환으로 끝나지 않고 추가 KeyError로 끝나며, 결과 schema도 불완전하다. 외부 예산 초과 분기가 우연히 limited_result를 채우는 경우를 정상 실패 처리로 삼을 수 없다.

**최소 정정:** 초기 결과에 limited_result=INCOMPLETE를 포함하고 모든 반환/예외 경로의 공통 필수 schema를 고정한다. 호출부의 추출/소비 예외 결과도 축별 미완·errors·overall·limited_result를 일관되게 남긴다. broad catch로 성공 기본값을 만들지 않는다. 파일 쓰기 자체의 실패는 별도 오류로 보존한다.

**한정 회귀:** PY02/PY03/PY14에 잘못된 binding, guard, native사유 및 추출 실패를 실제 consumer→candidate_entry.analyze 연결로 넣는다. 각 경우 최초 이유가 유지되고 결과 limited_result=INCOMPLETE, rc1, KeyError 없음이어야 한다. 완전 양성 대조도 함께 둔다. 검사기는 후보 함수를 직접 써야 하며 별도 모사 함수의 성공으로 대체하지 않는다.

수신 측 근거는 AST·호출부 정적 대조와 검토자 소유 dict schema 예시다. 실제 후보를 실행해 얻은 traceback이라고 하지 않는다.

## 4. G1198-N2 · P2 — 부모가 요약 문자열만으로 빈 증거를 수용 대기 상태로 넘김

**위치:** `PARENT_COMMAND.ps1:43–50`, 특히49행. 대응 검증안 PS03/PS05.

GDecision은 native/analysis의 typed rc·오류·시간, Result의 run/manifest·limited_result·overall·errors만 읽는다. trigger/sample/preservation/cleanup/policy 개별 축과 pair/native_stop/numeric/tables_manifest는 읽지 않는다.

따라서 다른 입력이 정상일 때 아래 다섯 필드만 있어도 현재 분기를 모두 통과하는 구조다.

```
run_id = 고정 run
code_manifest_sha256 = 고정 manifest
limited_result = TRIGGER_AND_SAMPLED_DATA_ACCEPTABLE
overall = INCOMPLETE
errors = []
```

그 결과는 `AWAITING_LIMITED_EXTERNAL_ACCEPTANCE`다. 이를 최종 PASS나 실제 실행 우회라고 과장하지 않는다. 다만 계획한 PS05의 “empty evidence → INCOMPLETE”를 함수가 강제하지 못하며, 개별 축이 INCOMPLETE인데 요약만 수용으로 남아도 부모는 모순을 검출하지 않는다.

**최소 정정:** 부모에는 새로운 수치 재계산기가 아니라 최소 결과 schema/상태 결속을 추가한다. 성공 대기에는 trigger=TEST_TRIGGER_DETECTED, 나머지 네 축PASS, 필요한 정지쌍/native/수치/coverage/표식별의 유효한 비어 있지 않은 구조 및 기대 하위 상태를 요구한다. 전체/normal gate INCOMPLETE와 새 승인 미생성도 유지한다. 단순히 존재한다는 이유로 빈 객체를 받지 않는다. CSV 수치 재검산 전체를 PowerShell에 복제할 필요는 없다.

**한정 회귀:** 실제 PS5.1 GDecision으로 완전 양성, 요약만 있는 객체, 각 축 누락/INCOMPLETE, pair/native/numeric/표식별 및 coverage 누락·빈값, 잘못된 run/manifest를 각각 확인한다. 요약 문자열을 그대로 둬도 불완전/모순 입력은 INCOMPLETE여야 한다. native_rc1/null을 analysisrc0으로 덮지 않는 기존 검사를 유지한다.

현재 후보가 실제로 잘못된 수치를 승인했다고 주장하지 않는다. 미실행 후보의 부모 소비 검증 공백이다. 정적 반례는 PARENT_SCHEMA_CASES.json에 있다.

## 5. 다음 한 건 — 좁은 정정·재봉인·변경부 검증

**다음으로 권고하는 사용자 승인 범위는 두 건 정정 + 재봉인 + 제안된26논리군의 한정 검증이다.** 동일 개괄 계획만 한 번 더 제출할 필요는 없다.

- 원본 후보 ZIP·소스·정적 실패/정정 기록은 보존한다. 새 개정본에서만 결과 schema와 부모 소비를 고치고 경로/manifest/검증안 식별을 일관되게 갱신한다.
- Python14/Java6/PS6 논리군은 유지하고 위 반례를 기존 PY02/03/14, PS03/05의 하위사례로 봉인한다. 새 harness·JDK·추출 범위를 시험 전에 고정한다.
- 실행 전 native/console/token/Job 진입점을 inert로 치환한다. Python 모사만으로 Java/PowerShell 시험을 했다고 하지 않는다. Java helper stub compile/JVM은 그 자체 별도 허용 행위이며 COMSOL 전체 후보 API 호환성 시험은 아니다.
- 첫 실패 보존·후속 중지·추가probe/부분 재시험/다른 엔진 fallback 금지를 유지한다. 수치 기준 완화·물리 변경·기존 전체suite 반복은 없다.
- 현재 자료를 검사한 것만으로 검증 release를 PASS로 만들거나 실제1198 승인을 생성하지 않는다. 검증 종료 뒤 결과를 제출하고 다시 멈춘다.

예산·정확 실행 엔진/사례/승인 경계는 NEXT_LIMITED_VALIDATION_DIRECTIVE_KO.md에 묶었다. 다음 검증도 여기서 실행하거나 자동 발송하지 않았다.

## 6. 보존·종결 범위

발신 TIME_AND_RESOURCE는 봉인 시점까지이며 delivery는 ZIP 밖 최종 영수증을 가리킨다. 그 최종 영수증/반환은 이번 첨부에 없어 발신 전달240초·전체3600초 최종 종결을 직접 확인했다고 하지 않는다. 수신 ZIP 자체 무결성 확인과는 별개다. 다음 결과 전달 때 기존 영수증이 있으면 원문 사본을 함께 주면 되며 과거 시험/포장을 재실행할 필요는 없다. 이 보충만을 이유로 이번 좁은 정정 검토를 되돌리지 않는다.

수신 측 COMSOL/JVM/받은 코드 함수/PowerShell 시험·solver·실제 입력/정책변경은0회다. 기존 B020 결과 수용 및 전체/normal gate INCOMPLETE·장시간 보류·OCP외삽 금지·TIME_CAPS 미확인·1198/30초 미승인을 유지한다. 두 P2를 닫고 한정 검증을 수용한 뒤에만 별도1198 native 승인안을 검토한다.
