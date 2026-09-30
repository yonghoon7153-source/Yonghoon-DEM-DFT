# Gate84 — 라운드 2 범위·사전 고정 검토

2026-09-30. **2a/2b 분리 방향 수용. 사전 고정 사항은 수정 조건부 적합. 구현 승인·실행 GO 아님.**

76차 및 83차 라운드 1 종결을 유지한다. 아래 항목은 새 라운드 2 설계의 정정 조건이며, 과거 수용 결과를 실패로 바꾸는 판정이 아니다. 2a 관련 G84-N1/N3/N4와 2b 관련 G84-N2를 분리한다. **2b 정정을 구현하기 위해 2a 범위를 넓히지 않는다.**

## 1. 식별·검토 수준

| 대상 | 확인 |
|---|---|
| 요청/발송 HEAD | `7fed4594c74b16f4a53402699eb2a8427805cdf5` |
| 코드 기준 | `ea2af59e68a85b561c3e185f66b815aec877ca57` |
| source_digest | `7187bd31740514d4` — 58개 파일 바이트와 경로로 독립 재계산 |
| 코드 불변 | 현재 HEAD의 네 Git tree 및 run/requirements blob 식별이 기준과 동일. 재귀 tree hash와 개별 blob도 대조 |
| 선행 판정 | 원격 83차 DECISION/manifest와 현지 원문 일치, 기존 리뷰 ZIP 식별 일치 |
| 이번 작업 | GitHub 고정 커밋 자료 읽기, 검토자 작성 해시·AST·텍스트 검사, 새 검토 문서·묶음 작성 |
| 하지 않은 것 | 수신 코드 import/함수 실행, 프로젝트 시험·변이 재생, 영수증 생성/복원, COMSOL·연구 계산, 구현·원장 변경 |

요청문의 docs-lint 358 PASS 및 83차 전체 2023 PASS/1 xfail 등은 발신 측 기록으로 인용한다. 이번에 재실행한 값이 아니다. 기준 자료는 `reference/`, 식별 근거는 `IDENTITY_AUDIT.json`, 정적 근거는 `STATIC_FACTS.json`에 있다.

## 2. 구현 전에 고정할 정정 사항

### G84-N1 · P1 · 2a/R2-b — base-config digest의 16/64자리 계약 충돌

요청 §1은 기존 `LEG_SPEC_FIT_KEYS.base_config_digest` 정의를 재사용하여 계획의 `inputs.base_config_digest`와 직접 비교하겠다고 한다. 그러나 현재 두 값은 길이가 다르다.

- `src/fitting.py:903–925`의 `_config_closure_digest()`는 extends 전체의 논리 상대경로와 파일 SHA를 해시한 뒤 **hex16으로 자른다**. `live_fit_axis`가 이 함수를 사용한다.
- `tools/preserve.py:3250`의 planned-leg/v4 검사는 같은 이름의 입력 값을 **hex64 또는 null**만 허용한다.

따라서 기존 반환값을 그대로 비교하면, 실제 base-config를 읽는 정상 non-null 계획도 일치시킬 수 없다. 단순히 기존 helper 전체를 hex64로 바꾸면 legacy 승인 spec 식별이 바뀌므로 해결이 아니다.

**최소 정정 권고:** closure의 범위·정렬·논리 경로 정규화는 공유하되, v6 계획/실행 기록에는 그 동일 preimage의 전체 SHA-256을 사용하고 v5 승인 축의 기존 hex16은 유지한다. 16자 문자열을 padding하거나 그 문자열만 다시 해시하지 않는다. leaf `base_config_sha`를 extends 전체 식별로 대신하지 않는다. 실제 계산에 쓰는 staged closure와 비교하고 validator 역시 봉인된 해당 closure 근거에 연결한다. 지금 validator 코드의 digest를 역사적 producer digest 대신 비교하지 않는다.

다른 표현을 선택할 수도 있지만, **계획·실행·validator의 타입/길이/원문 정의가 하나로 고정되고 v5 식별이 유지되어야 한다.** 실행이 config를 읽는 v6 경로에서 null을 정상으로 우회시키지 않는다.

닫힘 조건: 유효 non-null 양성, parent만 변경, leaf만 변경, null/잘린 digest, 같은 논리 입력의 다른 staging 위치를 구분하는 회귀. 잘못된 source/reference와 함께 실제 시작 전 소비 경로 및 validator 경로를 검사한다. 새 회귀 수는 구현 승인 때 고정하며 이번 리뷰에서 실행하지 않는다.

### G84-N2 · P1 · 2b/R2-a — v5 `stage3:null` 추가와 기존 spec digest 불변은 양립하지 않음

`tools/preserve.py:6402, 6431, 6470`은 닫힌 `LEG_SPEC_FIT_KEYS` 전체를 `leg_spec_version:2` spec에 넣는다. digest는 그 canonical JSON에 결속된다. 현재는 `stage3` 키가 없다. 여기에 null을 명시적으로 추가하면 값이 null이어도 canonical 바이트가 달라진다.

**정정:** v5의 기존 sealed spec에는 새 키를 추가하지 않는다. v6 승인 spec은 명시적 버전/분기로 stage3 축을 필수화한다. 표시용 메모리 view의 null과 봉인 preimage를 구분한다. v6 문맥에서 키가 없다는 이유로 legacy 분기로 내려가면 안 된다.

닫힘 조건: v5 기존 spec/claim digest 골든 불변 + v6 stage3 누락/다른 계획/다른 설계·roster·edge의 시작 전 거부. 이는 **2b의 착수 전 설계 조건**이다. 2a에서 spec/index/CLI를 고치라는 요청이 아니다.

### G84-N3 · P1 · 2a/R2-b — “시작 전 거부”의 실제 위치를 고정해야 함

현재 `_prepare_stage3`는 `src/fitting.py:1307`에서 grid reference만 허용한다. 하지만 실제 호출은 `_run_fit_locked`의 **1970행**이고, 같은 함수의 halfcell 분기에는 그 앞 **1955행 `_fit_one(...)`**이 있다.

따라서 새 검사를 `_prepare_stage3` 안에만 추가하면, 그 지점까지 도달하는 halfcell 호출에서 p_ini self-fit보다 먼저 거부한다는 조건이 성립하지 않는다. 이는 정적 호출 순서 확인이며 이번에 우회 실행을 재현했거나 과거 연구 계산이 발생했다고 주장하는 것은 아니다.

**정정:** v6 문맥의 unsupported reference/p_ini 거부와 실행 source·staged closure 결속을 첫 fitting/worker dispatch보다 앞선 공통 진입 경계에 놓는다. 입력 staging이 필요한 검사는 staging 후, 수치 작업 전으로 정의한다. 기존 lock/승인 순서를 임의로 제거하지 않는다. CLI만 검사하고 직접 `run_fit` 호출은 빠지는 구조도 금지한다.

이 조치는 **R2-b의 시작 전 결속 구현**이며 p_ini 지원 구현이 아니다. R2-d의 “거부 유지 정책 자체는 코드 변경 0”과 이 실제 배선 보완을 구분한다. R2-f에 “v6 원점 fitting 없음”을 적으려면 이 경계가 근거가 되어야 한다.

닫힘 조건: 유효 v6 양성은 정해진 준비 지점까지 도달하고, 잘못된 reference/source/config는 `_fit_one` 및 worker sentinel에 도달하기 전에 정해진 이유로 거부된다. legacy halfcell의 기존 동작은 보존한다. native 계산 없이 inert 한정 회귀로 검증할 수 있는 조건이다.

### G84-N4 · P2 · 2a/R2-g — 집계 단위·legacy 의미·v1 읽기를 함께 고정

`src/io.py:1547–1550`의 `returned`는 fits 행 수가 아니라 **각 objective의 `restarts_json` 원소 수 합**이다. optimizer round 수도 아니다. 이 단위를 그대로 보존해야 한다.

최소 정의를 다음처럼 고정할 것을 권고한다.

- `returned`: 기존 restart 반환 항목 수.
- `finite`: 그 반환 항목의 저장된 `J`가 유한한 수. parameter 유효성은 기존 validator 규칙을 유지하며 이 수 하나로 대체하지 않는다.
- `converged`: 같은 항목의 legacy `converged`가 명시적으로 true인 수. 이름은 유지하되 정상 종료 수로 해석하지 않는다.
- `0 ≤ finite, converged ≤ returned`; 두 수 사이의 포함 관계는 별도 정의 없이 가정하지 않는다. 누락/잘못된 타입을 0/false로 바꾸어 통과시키지 않는다.

80차 정정대로 legacy `ok`는 **마지막 유한 fun round에서 갱신된 success**다(`src/fitting.py:205–211`). 유한 성공 뒤 NaN 종료라면 저장 best J가 유한하고 legacy converged도 true지만 `outer=nonfinite`일 수 있다. 이런 경우도 위 두 계수는 증가한다. `native_last.success`, `native_best.success`, `outer`와 분리하며 primary complete-pair나 건전 종료의 판정으로 승격하지 않는다. 비유한 J에 대한 기존 산출 유효성 거부도 완화하지 않는다.

`execution-record/v2` 채택은 타당하다. 다만 닫힌 키 검사뿐 아니라 **writer와 재계산 consumer 모두 schema로 분기**해야 한다. 현재 `src/io.py:1879–1887`은 공통 재계산 결과의 `by_objective` 전체를 record와 직접 비교한다. 공통 함수에 새 키를 일괄 추가하면 v1을 예전처럼 읽을 수 없게 된다. v1의 새 계수 부재는 원문 그대로이며 0을 소급 기록하지 않는다. v2에서 키를 지운 자료는 v1로 내려가지 않는다.

닫힘 조건: v1 원문 양성·v2 양성·v2 필수 키 누락/혼합/타입 위조·재봉인한 계수 위조, 그리고 finite 성공 후 nonfinite 종료 및 첫 round nonfinite 대조. 반환·legacy 계산 의미는 바꾸지 않는다.

## 3. 질문별 답

| 항목 | 판정·경계 |
|---|---|
| R2-a | 방향 수용. G84-N2를 반영한 별도 2b. 새 plan/index/spec/CLI 연결은 2a 밖 |
| R2-b | 필요한 보완. G84-N1/N3의 표현·검사 위치를 고정한 뒤 2a 승인 요청 |
| R2-c | validator만 바뀐 digest에 연구 다리를 만들어 등록하지 않는 방향 수용. protocol `v6`와 코드 digest를 구분 |
| R2-d | grid/condition만 허용, p_ini 지원 거부 유지 수용. R2-b의 조기 거부 배선은 별도로 포함 |
| R2-e | dead 정의 삭제 수용. 실행 중인 dispatch와 역사적 reader 의미 보존 |
| R2-f | legacy/v6 열 분리 수용. 실제 절은 §1. 코드 근거에 맞게 쓰고 G84-N3 이전에 경로 전체 불실행을 확정하지 않음 |
| R2-g | 별도 계수 + record/v2 수용. G84-N4 정의/dispatch 고정 |
| 묶음·순서 | 2a=e/f/g+b, 그 뒤 별도 2b=a/c 연결. B1→B2는 가능하나 schema와 조기 결속의 인터페이스를 먼저 고정 |
| 실행·연구 | 실행 GO 없음, grid_fit_v5 진단 전용, 76차/83차 종결 유지 |

네 사전 결정에는 다음처럼 답한다.

1. **p_ini 거부 유지: 수용.** 지원 구현으로 확대하지 않는다.
2. **protocol 세대 이름 `v6` 하나: 수용.** `execution-record/v2`는 기록 schema이며 다른 축이다. 같은 코드 digest에서 나온 legacy leg를 전부 v6로 취급하지 않는다. 등록은 실제 leg·계획·영수증에 결속하며 연구 leg 없는 validator 개정의 가상 등록은 하지 않는다.
3. **기존 run.sh 흐름에 통합: 방향 수용, 표기 정정.** 현재 인터페이스는 `./run.sh --mode fit ...`다. `run.sh fit ...`를 이미 지원하는 명령처럼 고정하지 않는다. 최소 후보는 `./run.sh --mode fit --stage3-plan <leg_id> ...`이며 정확 argv·`--leg`/환경변수 충돌·계획 선택 규칙은 2b 전에 정한다. 이번 리뷰는 명령 실행 지시가 아니다.
4. **execution-record/v2: G84-N4 조건으로 수용.** protocol generation과 schema version을 섞지 않는다.

## 4. 파일·종결 경계

2a의 생산 코드 상한은 제안한 네 파일 `src/fitting.py`, `src/io.py`, `tools/design_wire.py`, `tools/preserve.py`다. 반드시 네 파일을 모두 고치라는 뜻은 아니다. 관련 시험·계약 문구·변이 등록·history 보존·기존 leg별 validator 영수증 1회 재생성은 **다음 사용자 승인문에 별도 명시**한다. 이전 라운드 승인이 자동 이월되는 것은 아니다.

2b의 run.sh/scripts 또는 새 CLI, 계획 index/원장 schema, v6 승인 spec은 별도 범위다. 실물 연구 leg가 아직 없으므로 2b 구현만으로 실물 v6 실행 성공이나 세대표 실물 등록 완료를 선언하지 않는다. 실제 leg 실행과 등록은 이후 별도 gate 대상이다.

영수증은 승인된 라운드 끝의 고정 코드에서 **기존 각 leg당 1회**라는 의미로 수용한다. 현재 세대를 history로 보존하고 producer·묶음·산출·복원 식별은 그대로 유지해야 한다. 새 코드가 추가한 검사 외의 판정 변화가 있으면 원인을 보고한다. 이번 리뷰에서 영수증 재생성/복원을 실행하지 않았다.

비차단 문구 정정 두 가지:

- R2-a의 “src 어디에도 `stage3=` 호출 없음”은 내부 전달 호출(`src/fitting.py:1507`) 때문에 문자 그대로는 맞지 않는다. **외부 production 진입점에서 v6 문맥을 구성하여 전달하지 않는다**로 좁힌다.
- dead 정의 삭제로 live 코드 줄번호가 이동한다. R2-f의 “legacy 문장·줄번호 불변”은 **legacy 의미 불변, 이동한 인용 좌표는 갱신 가능**으로 바꾼다. 줄번호 유지를 위해 dead 코드를 남길 필요는 없다.

## 5. 다음 최소 행동

요청자 측에서 위 정정을 **사전 고정 표와 2a 승인 범위에 기록한 뒤**, 사용자에게 제한 오프라인 2a 구현을 별도로 승인받으면 된다. 같은 개괄 계획을 다시 반복하거나 2b를 먼저 구현할 필요는 없다. 정정안을 채택하지 않거나 네 파일 밖 변경이 필요하면 해당 차이만 다시 제시한다.

이번 수용은 범위·설계에 한정된다. 구현 완료 수용, 새 계산, floor/pilot/canary, active claim, class/투영, COMSOL 실행 권한은 만들지 않는다. 외부 발송도 하지 않았다.

검토자 자체 문자 검사기의 Markdown 강조 위치 가정 오류 1회는 `evidence/REVIEWER_AUDIT_ATTEMPT01*`에 보존했다. 정정은 검토자 검사 문구만이며 제출 코드 오류나 회귀 실패로 세지 않는다. 상세 작업 경계는 `REVIEWER_PROCESS_NOTE.md`를 참조한다.
