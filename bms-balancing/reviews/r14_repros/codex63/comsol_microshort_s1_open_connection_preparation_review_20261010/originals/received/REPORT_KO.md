# S1 OPEN 연결부 오프라인 준비

2026-10-09. 사용자 채택 범위에 따른 **비활성 후보·정적 근거·변경부 검증안 제출**이다. 기능 시험과 native 실행은 하지 않았다. `native_ready=false`, `approved=false`, `usable=false`다.

## 결과와 판단

기존 S1O R1의 한정 검증 종결을 재사용한다. 21개 봉인 구성원과 기존 Python 소비자·제어·PowerShell 부모는 수정하지 않았다. P0 Java는 원문 전체를 보존한 새 사본에 읽기용 helper 세 개만 추가했다. 호출 지점은 활성화하지 않았으며, `denyS0Execution()`과 실행 진입 차단도 유지했다. 추가 부분을 제거하면 원 P0의 전체 바이트와 같다.

새 Python 연결 후보 두 개는 raw 바이트 식별·정확 시간/전류/Li 투영과 소유 자원 관측값의 엄격한 투영을 담당한다. 실제 COMSOL 로그의 의미를 증명하는 provider와 실제 Windows 수집/중단 provider는 구현됐다고 표시하지 않았다. 기본 provider는 오류로 차단한다. 이는 완성된 native 실행본 제출이 아니다.

| OPEN | 이번 확보한 것 | 남는 실제 관측·구현 |
|---|---|---|
| installed_post_consistency_t0 | 로컬 Time 문서, CDI 소스 생성 지점, 설정/저장 t0 구분, 추가 read-back helper | 설치본 CDI 속성 키/값과 생성 solver 순서, 저장 t0의 post-consistency 의미. 첫 양의 시각이나 설정값으로 대체 불가 |
| installed_effective_coefficient_mapping | feature별 설정→생성 Expression/Weak→평가 계수의 대응 설계, 전체 재귀 정보표 helper | 실제 생성 변수·domain/단위·의존식, 평가 계수. `expected.consumed`를 fixture로 채우지 않음 |
| raw_native_evidence_adapter | 바이트/단위/시간·charge 투영 후보, 원 소비자 연결 차단 seam | native 종료 로그 문법/사유/추가 적분 없음의 증거, 단위 raw 파서, 완전한 loader, t0/계수 검증 provider, 인증된 적분오차 bound |
| OS_resource_ownership_stop_adapters | 현재 winjob API 사용 근거, PID+생성시각/RSS/commit/디스크 투영, 기존 상태기계 호출 연결 | 실제 멤버 handle 수집·counter ABI/정확 Job commit·제한 set/readback·스케줄러·OS dispatcher·cooperative stop |

네 OPEN은 닫지 않는다. 로컬 문서와 정적 코드로 확인 가능한 부분을 구체화한 것이다. P0도 여전히 실행 미승인이고, P1–P3/K/장시간 cohort·미세단락 효과 결과 주장은 없다.

## 설치본 근거의 의미

COMSOL 6.3 설치 디렉터리의 HTML 문서만 읽었다. 네트워크 조회 없이 원파일 경로·크기·SHA를 `evidence/LOCAL_DOCUMENTS.json`, `LOCAL_DOC_DISCOVERY.json`, `CDI_SEARCH.json`에 기록했다. `DOC_02.txt`는 Time API, `LOCAL_comsol_ref_solver.36.136.txt`는 Time-Dependent Solver 설명이다.

Time의 `consistent=on`은 적용 가능한 DAE 조건에서 미분 자유도를 고정하고 대수 자유도/시간미분을 구한다. `bweuler`는 작은 인공 step으로 초기 자유도를 교란할 수 있다. 현재 후보가 실제 어느 설정·해를 쓰는지는 호출 없이 관측하지 않았다. 이 준비에서 consistent 값을 바꾸지 않는다. 원 `INITIALIZATION.json`의 Li·분율·전해질 허용치를 유지한다.

CDI는 원 P0 714행의 `CurrentDistributionInitialization` 생성이 정적 근거다. 설치 Battery 도움말의 `Solving Electrochemical Models`는 이 study step이 potential 초기화를 위해 사용됨을 설명하고 Primary/Secondary 선택을 언급한다. 그러나 이번 설치본 후보의 기본 선택 키·실제 선택값은 그 설명만으로 결정할 수 없다. `s1OpenConfiguredReadback`이 향후 모든 typed property를 원문으로 남기도록 제안한다.

`FeatureInfo.getInfoTable(id,"recursive","all")`는 설치 API에 명시돼 있다(`DOC_08.txt` 101–143행). 새 helper는 pcb1/pce1/pce2의 Expression/Weak/Constraint/Shape를 수집하도록 작성했다. 이 호출의 문서 존재와 실제 계수 변수명·평가 성공은 별개다. 현재 값의 source 계산을 실제 유효 계수 관측으로 승격하지 않는다.

`s1OpenStoredGrid`는 기존 EvalGlobal/t/innerinput=all 경로를 써 전체 저장 시각과 1-based index를 출력하는 **미실행 후보**다. 시간0의 표식은 `STORED_ZERO_POST_CONSISTENCY_PROOF_OPEN`이다. getPVals의 문서가 parametric 값을 설명하므로 이를 확인 없이 시간 벡터라고 가정하지 않았다. 설정 tlist/요청 시각/실제 저장 시각/양의 적분 단계는 분리한다.

## raw 연결과 수치 판정 보존

`candidate/raw_connection.py.inactive.txt`는 다음을 추가한다.

- raw 크기·SHA 확인 후 CSV의 명시 header·단위·유한 Decimal을 읽는다. native 단위 증거 자체의 의미 검증은 별도 loader 책임이며 이번 후보가 공급하지 않는다.
- native 전체 grid, global Li 표, leakage 표의 정확 시간 배열을 대조한다. 보호중단 때의 비교 prefix를 전하 적분 grid로 대신 쓰지 않는다.
- global과 leakage에 중복 출력된 RN/RP/j가 다르면 거부한다. 기존 부호·단위로 `time_s,j,RN,RP,I,LiN,LiP,LiE`에 직접 대응한다. 임의 재정규화·보간은 없다.
- 정상 종료는 정확 끝시각, 보호중단은 실제 마지막 두 시각을 사용한다. t0만의 비교/누락 요청을 거부한다. 이 투영만으로 native 중단사유를 증명하지 않는다.
- 적분오차 bound가 없으면 null/INCONCLUSIVE를 유지한다. 두 사다리꼴 값의 차이를 엄밀 오차상한이라고 만들지 않는다. non-null bound는 전체 prefix·j/RN/−RP·grid와 별도 검토된 방법 식별에 결속되어야 한다.
- `consumer_connection`은 실제 기존 `consumer.analyze`로 연결할 seam이다. 현재 기본 installed proof provider가 OPEN 오류를 내므로 native 유효성을 자동 생성하지 않는다. 이 seam의 inert 검증은 설치본 관측을 대체하지 못한다.

정확 표·표현식·단위·consumer 필드는 `OPEN_CONNECTION_MAP.json`과 `CONNECTION_DETAILS_KO.md`에 있다. source 설정과 원 계약의 숫자는 과거 봉인값을 그대로 참조한다.

## OS 연결의 범위

기존 winjob의 private Job/정지된 root 생성/assign-before-resume/GetProcessTimes/Job query/TerminateJobObject 호출을 텍스트로 대조했다. 기존 코드 전체를 새 감시기로 포장하지 않았다. 기존 launcher의 정책 변경·원복 경로도 새 후보에 넣지 않았다.

새 `resource_connection.py.inactive.txt`는 한 샘플 시작/끝의 Job membership과 PID+creation FILETIME, 프로세스별 working set을 대조한다. root가 이미 종료하고 자식이 남는 경우는 보유 root handle의 signaled 기록을 요구하며 root를 다시 더하지 않는다. 멤버 변경/접근 오류/미확인 counter는 0으로 바꾸지 않는다. RSS는 unique member working set의 합이며 공유 페이지 중복 가능성이 있다. Job commit은 별도 검토된 단일 Job accounting total만 받으며 per-process 합이나 OS peak로 대체하지 않는다.

host commit 여유는 CommitLimit−CommitTotal이고 available physical RAM과 다르다. 디스크는 소유 출력 tree 논리 bytes 및 해당 볼륨 free를 별도로 받는다. 불완전 탐색·reparse·scope 불명은 STOP이다. 이는 data projection이지 실제 주기적 관측이나 hard cap의 설치가 아니다.

현재 Windows SDK header 경로와 독립 primary counter 문서는 확보하지 못했다. `OS_API_MATRIX.json`의 기존 코드 좌표는 실제 OS API 동작 검증을 뜻하지 않는다. 새 ABI, Job 현재 commit counter 및 set/readback은 별도 근거·검증 없이는 실행 연결할 수 없다.

`stop_action_plan`은 기존 `control.advance_stop`을 호출하는 순수 계획 함수다. OS dispatch는 없다. cooperative API는 미확인이고 TerminateJobObject와 kill-on-close는 강제 종료다. force-only 채택이나 commit hard cap 제거는 별도 사용자 결정이다. 소유 불명 PID 종료는 금지한다.

## 검증·다음 경계

이번에는 소스 텍스트/AST·JSON·해시·diff만 확인했다. AST 파싱은 함수 실행이 아니다. Java compile/JVM, Python 후보 import, PS 함수 실행, 시험 suite, 실제 COMSOL/입력/Job 시험은 0회다.

`LIMITED_VALIDATION_PLAN.json`에는 이번 추가부만의 사례·양성 대조·기대 이유/도달 함수·엔진·횟수·예산을 고정한다. 기존 R1 수용 전체를 반복하지 않는다. Java helper 형식 검증을 향후 하더라도 설치 COMSOL API 호환성은 별도다. 실제 OS 동작도 inert 검증으로 증명할 수 없다.

권고 다음 순서는 **이번 준비본 검토 → 필요한 추가부 한정 검증 별도 승인/수용 → 설치본·OS OPEN에 필요한 별도 관측 범위 확정**이다. 아직 정확 native argv/cwd·새 승인 경로가 완성되지 않았으므로 native 실행 요청을 활성화하지 않는다. `SEPARATE_ALLOWLIST_DRAFT_KO.md`는 필요한 관측 제안이며 실제 허가 파일이 아니다.

## 보존·시간·출처

원점은 `ORIGIN.json`에 기록했다. 단계별 관측은 `PHASE_RECORDS.json`, 최종 정적 결과는 `STATIC_CHECKS.json`, 선택 원본 전후 목록은 evidence 아래에 있다. 목록은 선택한 경로의 바이트 관측이며 MPH/prefs/PC 전체 관측을 주장하지 않는다.

초기 동일 Desktop ZIP 조회는 부재였고 사용자 첨부 도착 뒤 동일 절대 경로·기대 SHA를 확인했다. 일부 로컬 문서 탐색에서 존재하지 않는 예상 디렉터리와 PowerShell에서 확장되지 않은 rg glob 인수를 발견했다. 이는 읽기 검색 도구의 오류로 `TOOL_OBSERVATIONS.json`에 보존하며, 후보/고정 입력 불일치나 기능 시험 실패로 바꾸지 않는다. 입력 식별 검사 이후 불일치는 발견되지 않았다.

과거 614.480초 기록은 당시 snapshot이며 그 뒤 전체 종료 시간은 미관측이라는 수신 범위를 유지한다. 원 영수증 recipient=null과 과거 실패/예산 관측은 수정하지 않는다. 이번에는 ZIP 밖 영수증·포장 반환 전사·최종 확인을 파일로 따로 남기며, 마지막 쓰기/재읽기 뒤 snapshot과 도구 반환을 구분한다.

전체/정상 gate INCOMPLETE, 실효 정책/실제 코어 UNVERIFIED, OCP 외삽 금지·TIME_CAPS 미확인·기존 실패/pending/원복은 유지한다. 준비물 제출 뒤 중지한다.
