# S1O R1 오프라인 정정 결과

2026-10-08. **N1–N4의 소스·계약 정정을 완료했습니다. 정적 대조만 수행했으며 기능 검증은 NOT_RUN입니다.** 수신 검토와 다음 별도 검증 승인을 기다립니다.

사용자 승인: `USER_OFFLINE_SCOPE.txt`. 원점은 05:24:26.7873978 UTC / 14:24:26.7987496 KST입니다. 새 출력 위치의 부재를 확인하고 시작했으며 원본 폴더에는 쓰지 않았습니다. 원 준비 ZIP SHA `0cae7accaf26397d883e0d8b732357fc2dc640553c603825a6a155bf8d4aaf53`와 원 CODE_MANIFEST SHA `54c61d10b3bb11e0501e9933b220eca76d9f7cee503953a6f909185e04f965fe`를 대조했습니다.

## 정정과 연결

| 지적 | 수정 위치 | 바뀐 판정 |
|---|---|---|
| N1 | `candidate/consumer.py.inactive.txt:217`, `:355`; `Parent.ps1.inactive.txt:108` | charge/native/global의 전체 저장 격자·시작0·실제 끝·같은 시각의 LiN/LiP/LiE·출처 식별·단위를 연결. 정상 끝, 보호중단 실제 끝, 비교 safe prefix를 구분. |
| N2 | 같은 `charge_balance`와 `S1ChargeFields` | 누적 q와 별도로 인접 ΔqN·ΔqP를 계산. 기존 2e−4 C/m² deadband보다 엄격히 작은 역행만 거부하고 최초 위반 구간·값·전극을 보존. |
| N3 | `Parent.ps1.inactive.txt:69`, `:170` | 고정 요청 배열과 검증된 safe end에서 prefix를 독립 유도. 정확 값·순서·중복·범위·부분집합 검사. 결과의 count로 기대 목록을 만들지 않음. |
| N4 | `candidate/variants/P0.java.inactive.txt:439` | `requested tlist storage` → `accepted tsteps storage` 로그 문자열만 정정. 실제 `tout=tsteps` 설정 유지. |

N1 보호중단은 `t_minus=실제 격자[-2]`, `t_plus=실제 격자[-1]=actual_end<configured_end`로 소비자·부모가 일치합니다. charge는 t_plus까지의 전체 저장 격자를 사용합니다. 비교는 고정 요청 목록에서 t_minus 이하만 사용합니다. 전체 교집합에는 t_plus가 남을 수 있으며, 이를 비교 안전 구간에 포함했다고 쓰지 않습니다. 전체 교집합은 native 격자의 부분집합이고 모든 비교 시각을 포함해야 합니다.

N2 누적 역행도 함께 발생하면 기존 `REVERSE_LI_TRANSFER` 이유를 유지하면서 첫 구간 증거를 남깁니다. 누적량이 양수인 구간 역행은 `REVERSE_LI_INCREMENT`입니다. 단위·방향·deadband·수지 허용치를 바꾸지 않았습니다. 적분 오차 근거가 없거나 방향 분해능이 부족하면 기존 INCONCLUSIVE를 유지합니다.

부모의 새 시각·비교 문턱 검사는 decimal 문자열을 정확 비교합니다. 이미 이진 실수나 CLR decimal로 바뀐 입력은 원 정밀도를 보증할 수 없어 거부합니다. 정확 0.001과 0.0010000000000000000001을 double 반올림으로 합치지 않습니다. 기존 예산 double 검사와 S1FinalReturn 본문은 그대로입니다. 이 분기의 실제 PS5.1 동작은 아직 검증하지 않았습니다.

`CHARGE_BALANCE.json`, `EXECUTION_BINDING.json`, `SOURCE_CONTRACT_LINKS.json`을 같은 구조에 연결했습니다. 실행 연결 문서의 비활성 source 경로만 R1 사본 위치로 바꿨고 native argv/작업/승인 경로는 여전히 미정입니다. 설치본·raw adapter가 원자료를 정규화한다는 전제는 OPEN이며, 새 스키마가 그 구현을 대신하지 않습니다.

## 불변과 정적 확인

- 기존 20개 소스·계약 항목 중 7개 파일이 바뀌었고, 별도로 옛 검증안을 R1 검증안으로 교체했습니다. 상세 바이트 diff는 `MINIMAL_DIFF.txt`, 파일 식별은 `CHANGED_FILES.json`입니다. 옛 검증안은 `reference/ORIGINAL_VALIDATION_PLAN.json`에 바이트 그대로 보존했습니다.
- consumer는 `charge_balance`·`analyze`만 수정했습니다. control 전체, P1–P3 Java/diff, INITIALIZATION·COEFFICIENT_READBACK·POLICY_VARIANTS·K_DESIGN·RESOURCE_CONTRACT·COST_MODEL은 원본과 같습니다. P0는 허용 문자열을 역치환하면 전체 바이트가 같습니다.
- S1Has/S1Struct/S1Number/S1Sha/S1Failure/S1FinalReturn 본문은 바이트 동일합니다. 물리·초기조건·σ·OCP·해상도·cap·출력 API·수치 허용치를 바꾸지 않았습니다.
- 소스/보존 정적 대조 **240항목**, 검증안/추출 결속 정적 대조 **57항목**을 확인했습니다. 이것은 297개의 기능 시험이 아닙니다. Python AST와 PowerShell parser는 구문 자료만 읽었습니다. 부모 parse 오류0, 함수15개입니다. 사용한 bundled parser의 결과를 Windows PowerShell5.1 실행 성공으로 확대하지 않습니다.
- 원 준비 폴더의 선택된 **116개 파일**을 현재 바이트로 다시 대조했습니다. 전체 PC·대형 MPH·현재 COMSOL 정책의 재검증을 뜻하지 않습니다. 입력 검토 ZIP은 CRC/경로/중복을 읽기 전용 확인했습니다.
- 관측 중 존재하지 않는 보조 노트 읽기 두 건과 문서 작성 도구의 UTF-8 지정 누락 오류 한 건이 있었습니다. 원문·정정 범위는 `notes/CONSUMER_R1_NOTES.json`, `notes/PLAN_R1_NOTES.json`에 남겼습니다. 후보 시험 실패나 COMSOL 오류가 아니며 감추거나 전체 도구 오류0으로 기록하지 않았습니다.

## 다음 검증안 — 미실행

**8군 130개 고유 ID·130입력 = Python99 + Windows PowerShell5.1 31**입니다. 기존98 ID의 매핑 98개와 신규32개를 분리했습니다. P0 로그 정적 확인1건은 기능 사례 수에 포함하지 않습니다.

정상 CHARGE01→실제 Python 결과의 봉인 JSON→PARENT01, 보호 CHARGE_R109→PARENT03 연결을 명시했습니다. 보호 예시 설정120/실제90.1/safe90에서는 고정255요청의 prefix가249개입니다. 같은 길이의 잘못된 배열·원자료/끝시각 누락·누적 양수 속 N/P별 역행·정확/내부 deadband·double 전달 오류·문턱 바로 위/정확 경계의 이유와 도달 단계를 구체화했습니다. PAIRED04의 D/S/E_D/E_S를 모두 고정했습니다.

제안 검증 예산은 별도 원점 **1,860초**(하네스·봉인720/Python420/PS300/보존·전달300/미완120), 각 엔진1세션입니다. 이는 현재 준비 예산에서 전용하지 않는 새 미승인 제안입니다. 실제 harness·fixture·엔진 현재 식별·추출 바이트·명령/cwd는 첫 시험 전에 봉인해야 합니다. 생산 코드를 실행하거나 130사례를 통과시킨 것이 아닙니다.

## 식별·전달·정지

새 CODE_MANIFEST: `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` (21개 파일, self 제외).

검증안 SHA: `137b4241d03d0d512dd4f746db1727f579b96fa0125c761497ac764caf0446b8`.

현재 source와 43개 추출 span을 연결했습니다. Python/PS 함수의 LF 정규화·마지막 LF 제외 규칙과 원 파일 SHA를 구분했습니다. `PARENT_STATIC_PARSE.json`의 raw AST span은 별도 규칙으로 기록하며 서로 같은 해시라고 주장하지 않습니다.

총 승인2,700초 및 단계1200/600/600/300초는 `PHASE_EVENTS.json`과 `TIMING.json`을 따릅니다. 병렬 정정·검증안 초안 작성은 같은 wall-time 구간으로 한 번만 계상하고 작업자 시간을 더하지 않았습니다. 본체 ZIP의 `TIMING_PRE_PACKAGE.json`은 포장 전 기록이고, ZIP 밖 `TIMING.json`·`DELIVERY_RECEIPT.json`은 포장·재읽기 이후 snapshot입니다. `FINAL_PACKAGE_TOOL_RETURN.json`은 실제 반환을 이후에 전사한 자료이며 당시 독립 OS 감사가 아닙니다. 이후 보충 포장도 반환 전 snapshot과 tool wall time을 구분합니다.

후보/수신 코드 import·함수 호출·기능 시험·Java compile·JVM·COMSOL·입력 gate·실제 approval/release/runtime/token 생성은 모두0회입니다. 새 자체 정적·해시·문서·포장 도구는 사용했습니다. native_ready/approved/usable=false, 전체/정상 gate INCOMPLETE, 실효 정책·실제 코어 UNVERIFIED와 기존 OPEN을 유지합니다. P/M/N·24회/60시간·새 계산은 승인되지 않았습니다. 제출 후 멈춥니다.
