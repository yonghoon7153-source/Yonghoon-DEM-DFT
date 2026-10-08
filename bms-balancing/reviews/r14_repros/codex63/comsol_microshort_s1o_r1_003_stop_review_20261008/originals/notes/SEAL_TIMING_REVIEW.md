# R1_003 중지 패키지 봉인·시간·권한 기록 검토

2026-10-08. 수신된 프로그램·하네스·후보·Java/JVM/COMSOL을 실행하지 않았다. 검토자 작성 JSON 읽기, 원문 바이트 해시, 텍스트 범위·오프셋 대조, 기록 집계와 스칼라 시간 산술만 수행했다. 수신 자료는 수정하지 않았다. 아래의 엔진 실행 사실·PID·시각은 실행 담당자가 제출한 기록이며 검토자가 실행 PC에서 새로 관측한 것이 아니다.

## 결론

봉인과 보존 기록 사이의 새 바이트 불일치는 발견하지 않았다. FIRST_SEAL의 123개 항목과 SELECTED_SOURCES_AFTER의 123개 전후 항목은 서로 맞고, 실제 수신 파일 121개는 바이트 수·SHA까지 독립 재확인했다. 나머지 2개는 외부 엔진 실행파일 식별의 제출 관측 기록이다. 43개 함수 추출과 실제 PowerShell 관측 15개, Python 생산자/context 10개의 두 번째 봉인도 일치한다.

엔진별 원문 결과는 Python 99 PASS, PowerShell 28 PASS 뒤 R113 하네스 실패라는 중지 결과와 맞는다. 전체 기능 검증 PASS를 뜻하지 않는다. 시간 기록은 1860초·단계 상한 내 종료 주장과 정합적이며 PS의 `within_limits=false`는 rc1을 포함한 결합 판정이다.

권한의 출처 한계는 남는다. 동봉한 발송문은 R1_001을 고정하지만 실제 기록은 R1_003을 사용한다. ORIGIN/RESULT는 별도 사용자 승인을 받았다고 기록한다. 003 위치와 같은 조건에 대한 실제 사용자 응답 원문·식별은 이 ZIP에 없으므로 **승인 받았다는 제출 기록**으로 분류한다. 그 사실만으로 무승인 우회라고 단정하지 않으며, 현재 새 측정·실행을 요구하여 과거 승인 근거를 대체하지 않는다.

## 1. FIRST_SEAL 123개와 사후 보존

`FIRST_SEAL.json`은 42,562 bytes, SHA `ee1ea9831b716d6c69e3d21f2aff7144d5f0b747f0d88549e62ae84f5bc8e1f8`이다. 두 ATTEMPT 기록이 이 동일한 크기·SHA를 가리킨다.

| 구분 | 항목 수 | 이번 독립 확인 범위 |
|---|---:|---|
| source root의 CODE_MANIFEST + payload21 | 22 | 수신 `source/` 바이트 해시와 봉인·사후 기록 모두 일치 |
| fixture root의 계획·하네스·입력·정적 도구·reference | 99 | 수신 해당 파일의 바이트 해시와 봉인·사후 기록 모두 일치 |
| Python/Windows PowerShell 실행파일 | 2 | 전후 제출 식별값이 봉인과 일치; 실행 PC 파일 자체는 미수신 |
| 합계 | 123 | 고유 경로123, 사후항목123, 불일치0 |

123개를 “이 검토자가 실행 PC의 파일 123개를 지금 재측정했다”거나 “PC 전체가 불변이다”로 확대하지 않는다. SELECTED_SOURCES_AFTER 자체도 `First-seal file set only; not whole PC`로 한정한다. FIRST_SEAL·사후 기록의 해시 일치는 중간 시점에 있었을 수 있는 모든 외부 활동을 배제하는 OS 감사 로그도 아니다.

생산 CODE_MANIFEST SHA는 수용된 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`다. root가 별도로 확인한 원21개 생산 payload 동일성에 더하여, 이 담당 검토는 동일한22개 source 파일이 FIRST_SEAL와 SELECTED_SOURCES_AFTER 양쪽에 결속되어 있음을 확인했다.

`DEPENDENCY_ORIGINS.json`에는 96개 모듈 origin 기록(파일 해시가 있는 기록63개)과 하네스 AST 대상4개가 있다. 그 JSON과 수신 하네스 자체는 FIRST_SEAL로 봉인되어 있다. 패키지 밖 라이브러리·실행파일의 현지 내용은 제출된 관측으로만 다룬다. R1_002 dependency 기록이 reference로 보존되어 있으며 그것을 이번 기능 세션의 실행 결과로 세지 않는다.

## 2. 추출과 두 번째 봉인

- EXTRACTION_SEAL 43개 각각의 source 원문 SHA, 시작/끝 행, LF 정규화 바이트 시작 오프셋·끝 오프셋, 바이트 길이·SHA를 수신 소스에서 독립 대조했다. 43개 모두 비어 있지 않은 유효 범위이며 일치한다.
- 이전의 S1Sha 오류는 23–23행, 90 bytes, SHA `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`로 정정되어 있다.
- `results/ps_extraction_observed.json`의 Parent 원문 SHA와15개 함수 길이·범위·SHA가 EXTRACTION_SEAL의 같은15개 항목과 모두 일치한다. 이는 제출된 하네스 관측과 원문 바인딩의 일치다.
- `results/PS_PRODUCER_SEAL.json`의5개 실제 결과 JSON(CHARGE01, CHARGE03, CHARGE_R109, POLICY02, POLICY03)+각 context 총10개가 실제 수신 바이트·SHA와 모두 맞는다.
- 같은 봉인의 `python_results`와 `python_session` 크기·SHA도 수신 파일에 맞는다. `harness_sha256=36479c721efac2f14d29292f55d6e2d991fba52eed1914dd41ee95b73d389bb2`는 **PowerShell 하네스**를 가리킨다. Python 하네스 해시가 아니며, 실제 ps_harness:43도 자기 파일을 이 값과 대조한다.
- 두 번째 봉인 시각은 `2026-10-08T13:58:37.6083103Z`다. 제출 Python 세션 종료 `13:57:57.8596401Z` 이후이자 PS 시작 `13:58:57.6942829Z` 이전이다. 첫 봉인→Python 결과 생성→두 번째 봉인→PS라는 순서와 맞는다.

FIRST_SEAL.commands, COMMANDS.json, 각 ATTEMPT/SESSION의 argv와 cwd는 R1_003의 동일 엔진·하네스를 지정한다. corrected plan에도 Python `-I -B`, PS `-NoLogo -NoProfile -NonInteractive -File`이 있으며 경로 슬래시 표기 외의 다른 엔진 실행 명령을 발견하지 않았다.

## 3. 원문 출력과 외부 반환

| 기록 | 수신 크기 | 수신 바이트 SHA 대조 |
|---|---:|---|
| PYTHON_STDOUT | 53,384 B | SESSION와 일치 |
| PYTHON_STDERR | 0 B | 빈 바이트 SHA 일치 |
| POWERSHELL_STDOUT | 117,012 B | SESSION와 일치 |
| POWERSHELL_STDERR | 0 B | 빈 바이트 SHA 일치 |

Python stdout은99개의 개별 JSON행이며 PYTHON_RESULTS.cases99개와 전체 객체 내용이 순서대로 일치한다. 모두 `status=PASS`다. PowerShell stdout은28개의 개별 결과행과 마지막 실패 요약1행이다. 앞28개는 `ps_first_failure.cases`28개와 전체 객체 내용이 일치한다. 마지막 요약은 `current_case=PARENT_R113`, `case_count=28`, 동일 first_error·retry0·later_cases_not_run=true를 기록한다. raw stdout을 현재 기본 문자 해석으로 읽을 때 한글 stack 일부가 깨져 보이는 차이가 있지만, 별도 UTF-8 실패 JSON에 온전한 stack·35/133행이 있고 ASCII 오류 식별·기록 내용은 맞는다. 원문 바이트는 수정하지 않았다.

`FIRST_FAILURE.json`은 POWERSHELL_SESSION.json과 바이트까지 동일하다(1,805 B, SHA `96b490e792bc09654a7e3d0ff1b7102c0bbef510869b1f5d9207809f675d0214`). FIRST_FAILURE는 rc1 세션 기록이고, 실제 첫 assertion의 구체 내용은 `results/ps_first_failure.json`에 있다. 두 층을 혼동하지 않는다.

ENGINE_TOOL_RETURNS는 스스로 `Later transcription of actual exec tool returns; not raw OS audit`라고 표시한다. Python completion `596519`/tool rc0, PS completion `003995`/tool rc1은 SESSION의 엔진 rc0/rc1과 맞는다. 0.0000152/0.0000142초의 tool wait wall은 마지막 poll이 기다린 시간이며 전체169초/30초 세션을 대체하지 않는다.

패키지에는 엔진별 ATTEMPT 하나씩·retry0, SESSION 하나씩과 첫 실패 후 중지 결과가 있다. 받은 기록은 Python1/PS1 세션 및 그 뒤 미수정·미재시험 주장과 일관된다. 독립적인 PC 전체 프로세스 감사로 “다른 실행이 절대로 없었다”까지 증명한 것으로 쓰지 않는다. 이번 검토자가 수행한 후보/받은 프로그램 실행은0회다.

## 4. 시계와 예산 경계

ORIGIN은 `2026-10-08T13:48:21.3047021Z`(KST22:48:21), monotonic tick `19663030423837`, frequency10,000,000이다. FIRST_SEAL 안의 origin 객체는 ORIGIN.json과 일치한다. 제출 기록의 경계는 다음과 같다.

| 경계 | 원점 후 누적초 또는 단계초 | 해석 |
|---|---:|---|
| first seal snapshot | 390.0584138 / preseal720 | 최초 기능 세션 전 |
| Python ATTEMPT 시작 | 누적407.2795063 | 원점·attempt tick 독립 산술 |
| Python SESSION 쓰기 전 | 누적576.5348597; 단계169.2547576 | rc0, timed_out=false |
| Python 세션기록 쓰기 후 전사 | 누적576.5540182; 단계169.2741394 /420 | 후속 final-return 관측 |
| PS ATTEMPT 시작 | 누적636.3765591 | 두 번째 봉인 뒤 |
| PS SESSION 쓰기 전 | 누적666.667302; 단계30.2902513 | rc1, timed_out=false |
| PS 세션기록 쓰기 후 전사 | 누적666.6853731; 단계30.3085736 /300 | 앞의 rc1 보존 |
| 보존·전달 원점 | 누적696.4308394 | 별도 DELIVERY_ORIGIN tick 산술 |
| ZIP 전 CLOSEOUT snapshot | 누적861.3451922; 전달164.9143550 | package/receipt 쓰기 전 |
| 사용자 본문 final-return 전사 | 누적862.1651496 /1860; 전달165.7343128 /300 | receipt 재읽기 뒤·도구 반환 전으로 선언 |

169.2547576→169.2741394와30.2902513→30.3085736의 차이는 서로 다른 관측 경계를 명시한 것이다. 더 나중의 외부 반환 전사 수치를 이전 SESSION에 덮어쓰지 않는다. PS `within_limits=false`는 `run_engine_once.ps1:76`의 rc0 및 시간 등 결합 조건에 의한 값이다. 이번 PS는 rc1이고30.3085736초는300초보다 작으므로 시간 초과로 분류하면 잘못이다.

720+420+300+300+120=1860초이며 수신 경계와 사용자 제공 마지막 snapshot은 각 상한 안이다. 사용자 제공 마지막 누적-전달 값696.4308368초와 DELIVERY_ORIGIN의 tick 산술696.4308394초 차이는2.6µs다. `package_evidence.py`가 overall/delivery elapsed를 각각 이어서 읽는 구조와 양립하며 예산 판정을 뒤집는 모순이 아니다.

raw return 이후의 전달 시간을 확보하려고 원격 환경을 지금 재측정하지 않는다. 사용자 본문 도구 반환 `0a81fc / rc0 / wall7.1100966`은 포장/전달 명령의 성공 전사이며 기능 검증 PASS가 아니다. 이 wall7.1100966이나 engine poll wall을 이미 누적인862.1651496에 합산하지 않는다.

## 5. ZIP 밖 영수증과 승인 출처

root의 독립 INPUT_CHECK는 수신 ZIP876,456 B, SHA `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b`, payload153+manifest1의 정확 집합/크기/SHA/CRC를 확인했다. 사용자 본문의 ZIP 밖 receipt/tool-return 전사는 이 수신 ZIP 식별과 결속되어 있다.

DELIVERY_RECEIPT.json·FINAL_PACKAGE_TOOL_RETURN.json·FINAL_SUBMISSION_CHECK.json은 `results/package_evidence.py:69`의 명시적 ZIP 제외 목록이다. 해당 원파일이 이 ZIP에 없는 것을 자동으로 누락·봉인 실패로 판정하지 않는다. 이번에는 사용자 본문 구조화 전사만 받았으므로 그 출처를 그대로 표시한다. 검토자가 다시 작성하는 요약을 원 영수증 바이트 재현이나 독립 OS 반환 로그라고 부르면 안 된다.

권한상 `reference/VALIDATION_SEND_KO.md:24`는 R1_001 한 위치만 지정하고 충돌 시 자동 이름 우회를 금지한다. 반면 ORIGIN:16은 사용자에게 R1_003을 같은 조건으로 따로 승인받았다고 기재하고 RESULT/PRESEAL_READINESS는001/002 중지 기록·이전 하네스 준비 자료 보존을 설명한다. 이 차이는 기록에 드러나 있으며 숨겨진 동일경로 주장으로 취급할 이유는 없다. 그러나003 승인 사용자 응답의 원문·시점·메시지 식별은 동봉되지 않았으므로 승인 기록의 완전한 독립 재현까지 확인되지는 않는다. 과거 승인 원문이 이미 보존되어 있다면 그 출처 연결이 추가 증거가 될 수 있으나, 현 시점 새 동의나 새 실행으로 과거 기록을 소급 대체할 필요도 권한도 없다.

corrected plan의 `approved=false`, `NOT_RUN`, proposal 상태와 일부 미래 하네스 미존재 설명은 이전 계획 메타데이터로 남아 있다(`fixture_created=true`와 함께 존재). 이를 실제 세션99/28 결과보다 우선하는 현재 실행 상태나003 승인 원문으로 해석하지 않는다. 현재 결과 판정은 CLOSEOUT·실패 원문·SESSION과 한정하여 읽어야 한다. 원 봉인 자료를 이 검토에서 고치지 않는다.

## 검토 한계와 도구 기록

권한·실행 횟수·외부 실행파일·디스크 가용량·금지 호출0의 PC 전체 재관측은 하지 않았다. 이 담당 검토의 결론은 패키지 안의 데이터와 주어진 사용자 전사의 내부 정합성이다. 전체 기능130 통과, R113 목표 생산 함수 거부 성공, native readiness나 후속 재시험 승인으로 확대할 수 없다.

검토자 자신의 읽기/시간산술 PowerShell 한 번은 `foreach ... | ConvertTo-Json` 배치 구문 오류로 parse 단계에서 종료되었다. 이를 배열식으로 정정하여 같은 데이터 검사를 완료했다. 받은 코드·기능 시험의 오류나 재시도가 아니며 그 실패 중 파일 쓰기·후보 실행은 없었다.
