# COMSOL B-min R2 준비 재검토

2026-10-05 · 게이트 차수 밖 · 정적 검토

판정: **PREPARATION_ACCEPTED_NOT_VALIDATED. BMIN-R1-N1 종결, C1 문구·분류 정정 수용, 변경부 검증안 수용. 추가 차단 지적 없음.** 실제 기능 검증 PASS나 native 실행 승인이 아니다.

다음 단계는 사용자 별도 승인하의 **9군·62개 고유 ID·77개 입력 한정 검증**이다. 그 결과를 수용한 뒤에만 입자 메시 640의 fresh 0→150초 계산 최대 1회를 따로 승인한다. 이번 검토로 어느 단계도 자동 시작하지 않는다.

## 고정 대상과 독립 확인 범위

- 고정 커밋: `939b544b8bb77dbf20a56520af9f74a82acd0a94`.
- 요청문 blob: `89c02107243244c7fe3518551d37408403edf5e0`.
- r2 CODE_MANIFEST: 1,050 bytes / SHA `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`.
- manifest의 생산 파일 5개 크기/SHA를 직접 대조했다. Java·entry·부모·CONTRACT는 R1과 바이트 동일하다. consumer의 선언된 두 변경을 역치환하면 CRLF를 포함해 R1 전체 바이트와 같다.
- COMMAND_MAP과 NATIVE_APPROVAL_FIELD_SPEC은 manifest SHA 교체만 있다. run_id·root·native 예산은 이전 후보와 같다. 모든 승인/사용 플래그는 false다.
- R1 꾸러미 전체 17개 Git blob이 직전 검토 커밋과 같다. V1은 이전 검토에서 확보한 28개 표본의 blob 불변을 확인했다. V1 전체 보존이나 과거 실행을 새로 전수 감사했다는 뜻은 아니다.

검토자는 후보와 제출자의 build/audit 도구를 import·구문 해석·컴파일·실행하지 않았다. COMSOL/JVM/native·제한 suite도 실행하지 않았다. 검토자 자체 JSON·파일 해시·소스 문자열·기존 ZIP 로그 읽기와 독립 문자열 모형만 사용했다. 제출된 38/38 STATIC_MATCH 및 R1/V1 감사 재실행은 제출자 정적 기록이며, 검토자 기능 시험 결과로 합산하지 않는다.

주요 근거: [R2 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/docs/COMSOL_BMIN_CANDIDATE_R2_REVIEW_REQUEST_20261005.md), [준비 결과](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/PREPARATION_KO.md), `INDEPENDENT_STATIC_AUDIT.json`.

## Q1 BMIN-R1-N1 종결

`mesh_evidence`는 단일 Time-Dependent Solver 구간을 고르고, DOF 문구를 포함하는 줄이 정확히 하나인지 검사한 뒤 그 **전체 줄**을 정규식과 대조한다. 앞뒤 공백을 제외한 두 번째 문장·불완전 문장·다른 꼬리 문자는 `TRANSIENT_DOF_READBACK_FORMAT`으로 거부한다. 첫 일치만 골랐던 R1 문제가 닫혔다. [consumer 313–336행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/src/diagnostic_consumer.py#L313)

줄 수 검사와 `solved > 0` 조건은 그대로다. 예상 `156925 / 12`와 다르더라도 유효한 단일 관측은 값·차이·review_note를 기록할 뿐 그 차이를 실패 조건으로 쓰지 않는다. 따라서 잘못된 로그의 거부를 강화하면서, 관측값을 예상값에 억지로 맞추는 변경은 하지 않았다.

| 입력 경계 | 정적 분기 대조 |
| --- | --- |
| 서로 다른 두 문장 또는 동일 문장 두 개가 같은 줄 | FORMAT 거부 |
| 정상 문장 + 불완전 DOF 또는 다른 꼬리 | FORMAT 거부 |
| DOF 두 줄 | COUNT:2 거부 |
| DOF 없음 | COUNT:0 거부 |
| 단일 문장이지만 solved=0 | VALUE 거부 |
| 정상 단일 줄의 앞뒤 공백 | 수용 |
| 정상 단일 줄, 다른 유효 DOF | 수용·기록 전용 |
| 시각 접두어가 있는 줄 | FORMAT 거부, 자동 제거하지 않음 |

표는 검토자 소유의 데이터 문자열 모형과 후보 소스의 분기 대조다. 후보 함수 실행이나 실제 COMSOL 오류 재현이 아니다. 선언된 영어 DOF 형식과 구간 표식 안에서는 잔여 차단 모호성을 발견하지 않았다. 임의 언어·모든 미래 로그 포맷을 받아들인다는 보장은 아니다. 알 수 없는 접두어를 만났다면 거짓 성공으로 통과시키지 않고 미완으로 남기는 현재 정책을 유지한다.

### NORMAL480 원 로그 131행 확인

원본 ZIP을 읽어 다음 식별을 재확인했다. COMSOL이나 분석기를 재실행하지 않았다.

- ZIP: 420,748,594 bytes / SHA `e991ab4c918f6576b18d6225a86ed41759ab6ee726dd6543b9a9158e581cbc30`.
- `run/batch.log`: 886,975 bytes / SHA `805e649493f6d793e0b780a3899c40132d2e15011742de047fecae16711fcfa8`.
- 131행은 아래 문장과 CRLF뿐이다. 시각 등 접두어, 후행 설명, 심지어 앞뒤 여백도 없다.

```text
Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs).
```

원 줄은 CRLF 포함 73 bytes / SHA `c4a34ce5b98400c3b2b9eeebf6e5a7bf3b9451d313cd8fad2f7ad874a8fc55f6`이며 `NORMAL480_DOF_LINE_131.txt`에 그대로 보존했다. 단일 시간 의존 구간 안의 DOF 줄은 이것 하나다. 86행 `1202 / 12`는 구간 밖 Stationary 초기화 기록이다.

따라서 PY03-13(b)의 양성 대조 문구는 원본과 일치하며, 우려한 접두어 때문에 이 기준 로그가 거부될 문제는 없다. 다만 **particle320 기준 로그**이므로 새 particle640의 DOF나 native 호환성 실측으로 읽지 않는다.

## Q2 C1 문구와 분류 수용

봉인된 PS01-16 fixture에서 직접 추출한 `0.001000000000000000000000000001`은 소수점 아래 **30자리**, 유효숫자 **28자리**다. 정확한 십진값은 0.001보다 크다. 이를 정확 등호 목록에서 빼 `precision_mismatch_items`로 옮긴 것은 맞다. 등호 대조는 PY01-02/PS01-04에 남아 있다.

PS01-16의 목표는 부모와 consumer의 비교 결과가 다를 때 INCOMPLETE로 닫는지 확인하는 것이다. 문서가 명시한 파싱 실패/반올림 중 실제 경로는 목표 Windows PowerShell 5.1에서 이후 확인해야 한다. 이번 검토는 그 엔진을 실행하지 않았으며, 임의 정밀도 십진 비교를 보증하지 않는다.

## Q3 한정 검증안 수용

기존 54개 ID를 유지했고 PS01-16의 정정 외 기존 fixture/expected 문구는 같다. 새 ID 8개, 새 입력 18개가 직전 Q4의 네 항목을 덮는다. 여러 입력이 있는 ID에는 입력별 기대 이유가 있다.

| 요구 | 대응 |
| --- | --- |
| 같은 줄 중복·불완전 꼬리·정상 대조 | PY03-11·12·13 — 두 문장, 두 종류의 꼬리, 공백, 원 로그의 다른 유효값 |
| consumer solved=0 경로 | PY03-14 — 부모 PS01-17과 구분해 VALUE 직접 도달 |
| native 축 원인별 반례 | PS01-18 반환/타입/오류 5입력, PS01-19 run/manifest 2입력, PS01-20 모순 종료 근거 4입력 |
| 미평가 축과 시험 전 봉인 | PS01-21, preseal_before_first_test — 추가 검증 범위이며 새 생산 제어 동작 아님 |

기존 PS01-12/13/14와 합쳐 부모 원인 이름 일곱에 각각 대응 사례가 있다. 이는 계획의 원인별 대응을 확인한 것이며, 모든 타입·모든 분기를 이미 기능 검증했다는 뜻은 아니다. [부모 135–185행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/PARENT_COMMAND.ps1#L135)

| 엔진 | 고유 ID | 입력 평가 | 제안 세션 한도 |
| --- | ---: | ---: | --- |
| Python | 39 | 42 | 1세션 / 250초 |
| Java helper | 2 | 2 | compile 1회 / 90초, stub JVM 1세션 / 60초 |
| Windows PowerShell 5.1 | 21 | 33 | 1세션 / 240초 |
| 합계 | 62 | 77 | 입력마다 세션을 새로 여는 안이 아님 |

전체 제안 예산은 `600 + 250 + 90 + 60 + 240 + 300 + 120 = 1660초`다. Python 증액 40초는 `210/36×6 = 35초`, PowerShell 증액 90초는 `150/21×12 ≈ 85.714초`를 올린 제안으로 산술이 맞다. 종전 입력 수 36/21은 기존 복수 fixture에서 센 값이다. **시간 충분성 실측이나 예산 승인으로 받아들이지 않는다.** 첫 실패·초과 시 미완 보존, 자동 수정/부분 재시험/우회 없이 중지하는 조건도 유지된다.

harness는 아직 없고 SHA도 null이다. 준비 검토 단계에서는 이를 허위 봉인 대신 명시한 것이 적절하다. 별도 검증 승인 뒤 첫 시험 전에 실제 harness SHA, 봉인 함수의 추출 위치, 엔진 바이트, 입력별 fixture·기대 이유·호출·시간 원점을 고정해야 한다. Python으로 PowerShell 판정을 대체하거나 COMSOL 전체 모델 compile을 끼워 넣지 않는다. [검증안](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/939b544b8bb77dbf20a56520af9f74a82acd0a94/bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/LIMITED_VALIDATION_PLAN.json)

## 유지되는 수용과 한계

R1의 종료 축 분리 수용을 유지한다. 부모가 같은 consumer의 구조화된 종료 근거를 별도 조건으로 소비한다는 뜻이지, 원시 native 로그를 제삼자가 독립 관측한 것은 아니다. entry가 사후 정리/보존/정책 실패에 rc1을 반환하면 `NOT_ESTABLISHED / NATIVE_CHILD_RC`로 남는 보수적 한계도 그대로다. 이를 solver 실패 확정으로 바꾸지 않는다.

run_id·root 재사용은 비활성 후보의 같은 실행 제안에 대한 개정 식별이다. 실제 위치가 비어 있다는 현재 원격 관측으로 확대하지 않는다. 추후 승인·배치 시에는 r2 manifest와 실물 바이트를 결속하고 충돌 시 중지한다. 현재 승인 파일/runtime/token을 만들지 않는다.

제출자 자체 신고 a–e는 종결을 막지 않는다. 후보 실행과 감사 도구의 문자열 모형을 구분했고, PS01-21은 범위 안의 검증 보강이다. 원 로그 부재 c는 이번 직접 읽기로 해소했다. r1/v1 원문 보존은 위 확인 범위에서 대조했다. 제출자의 감사 재실행이 같은 바이트를 다시 썼다는 이력은 이 검토가 새로 실행한 작업이 아니다.

검토자 자체 점검의 첫 판에서는 PS01-16 숫자를 손으로 옮기며 0 세 개를 빠뜨렸다. 출력의 27/25를 발견해 이를 판단에 쓰지 않고, 봉인 검증안의 문자열을 직접 추출하도록 고친 뒤 30/28을 확인했다. 최초 도구가 rc0이었어도 그 자릿수 관측은 폐기한다. `reviewer_history/`와 `REVIEWER_TOOL_RETURNS.json`에 최초·정정본을 보존했다. 이는 제출 후보 오류나 기능 시험 재시도가 아니다.

## 다음 행동

준비 검토 회신을 접수하고, 필요하면 고정 r2의 **한정 검증만** 사용자에게 승인받는다. 검증 계획이 수용됐다는 이유로 native를 시작하지 않는다. 검증 수용 후 fresh 0→150초·입자 반경 메시 320→640의 한정 공간 민감도 1회를 별도로 승인한다. 주 비교 창은 120–150초이며 480초 전체 공간 수렴 시험이 아니다.

approved=false / usable=false, 전체·정상 gate INCOMPLETE, 실효 정책 UNVERIFIED를 유지한다. 960초·유한 sigma·다른 공간 축·설정 변경·새 연구 실행은 승인하지 않았다. 게이트91과 이 COMSOL 건의 판정은 별개다.
