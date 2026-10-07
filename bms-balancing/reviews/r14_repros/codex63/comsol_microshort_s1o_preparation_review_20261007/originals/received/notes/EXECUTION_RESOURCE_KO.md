# 실행 연결·자원 감시의 오프라인 구현 범위

2026-10-07. **소스 작성과 계약 제안은 완료했지만, 실제 native 어댑터 연결은 partial/OPEN이다.** 이번 소스는 실행·import·합성 시험하지 않았다. `native_ready=false`는 실행 가능한 승인 플래그가 아니며, 이를 바꿀 때 새 바이트의 봉인·필요 검증·별도 native 승인이 먼저 필요하다.

## 3. 실행 연결

**확인:** `candidate/control.py.inactive.txt:51`의 `authorize_execution`은 manifest payload, 엔진·의존 파일, 검증 수용, 별도 사용자 native 승인, run/variant/σ/초기화/창, cwd/argv, 입출력·승인 경로, 횟수·자원·시간을 대조한다. `execute_once`는 이 함수 반환 뒤에만 첫 `create_exclusive_evidence_and_reserve_one_attempt`를 호출한다. `__main__`는 오프라인 중지로 끝난다. Parent도 함수 정의 뒤 명시적으로 중지한다. 파일 확장자뿐 아니라 승인 전 side effect를 차단하는 분기와 기본 미구현 어댑터가 있다.

실제 source를 Python/PowerShell로 실행하지 않았으므로 이는 **정적 코드 구조 확인**이지 승인 차단 기능 PASS가 아니다. 미래 loader는 승인 외부의 manifest 원문 bytes SHA를 계산하고, read-only 실제 payload/엔진/의존 identity와 비교한 후 동일한 handles/경로를 유지해야 한다. JSON의 자체 주장만으로 OS 신뢰를 만드는 방식이 아니다. 독립 검토 자료의 hash와 사용자 승인 원문 hash도 같은 실행 단위로 묶는다.

`contracts/EXECUTION_BINDING.json:9`의 P0 예시 단위는 high σ=1.7e−6, fresh 0–120초, compile/batch/solve 각각1, control/retry/별도초기화solve0, 동일 Python 세션 사용자 직접 challenge2다. 단일예시가 P1–P3 또는 M/N을 승인하지 않는다. 각 변형/창/수치 정책은 독립 승인 단위이다. 실제 native argv/cwd·스테이징·승인 경로는 null/OPEN으로 남겼다. 어댑터를 구현하지 않은 상태에서 임의의 실행 가능한 명령을 만들어 납품하지 않는다. `NATIVE_COMMANDS_UNRESOLVED`, `NATIVE_PATHS_UNRESOLVED`, `CURRENT_POLICY_PIN_UNRESOLVED`, `OFFLINE_NATIVE_NOT_READY`가 차단 이유다.

**확인:** NORMAL480 부모 `PARENT_COMMAND.ps1:19`의 BSave는 CreateNew·flush·재읽기를 사용하고, :27 BInvoke는 외부 child rc를 관측한다. :182/187/192는 PRE_WRITE와 POST_WRITE 예산을 분리한다. 이 원문을 수정하지 않았으며 이 동작의 **과거 근거**만 재사용했다. 새 `S1NativeAxis/S1Fields/S1Decision/S1FinalReturn`은 새 consumer schema와 결과축을 직접 읽는 별도 함수다. 기존 NORMAL480 전체 workflow PASS를 물려받은 것으로 보지 않는다.

**확인:** legacy `launcher.py:310/317`에는 apply/token 경로가 있다. 따라서 S1 정책 무변경 구현에 기존 launcher 전체를 그대로 부르는 경로를 두지 않았다. C2의 동일 프로세스 사용자 직접입력, owned Job, evidence record의 재사용 후보는 historical hashes만 계약에 넣었다. 실제 import/copy/call은 하지 않았다. 검증 전 현재 엔진과 의존 identity를 다시 읽어 봉인하고, 차이는 숨기지 않는다.

부모 판정은 rc0만 보지 않는다. 실제 native 이유/끝시각/guard, producer의 초기화·계수 근거, exact common/request coverage, 전압·표면·Li·분해 residual, 보존·소유 정리·정책·자원·오류·전체시간이 함께 필요하다. 문턱 초과 `EXCEEDS_LIMITS`는 실행 오류로 바꾸지 않고 별도 축으로 보존한다. 보호 중단은 `PROTECTIVE_STOP_INCOMPLETE`이고 120초 정상 완료가 아니다. q의 분해능/출력 적분 불확실성 `INCONCLUSIVE`는 방향성 주장 근거로 쓰지 않는다. `-NoExit`의 outer rc는 null이다.

`S1FinalReturn`은 writer→readback/hash확보→마지막 clock을 거쳐 초과나 기록오류가 있으면 이전 결정보다 INCOMPLETE를 우선한다. 이 함수의 writer/clock/readback는 향후 inert 검증용 인수이며, native 부모 전체는 아직 연결되지 않았다. 무한 재봉인이나 재시도 루프는 없다.

## 7. 자원 계약과 종료

**확인:** legacy `winjob.py:74–81`은 시작 가용RAM/디스크만 읽는다. :115–124는 suspended root를 private Job에 붙인 뒤 resume한다. :187–189의 kill-on-close와 :211의 `TerminateJobObject`는 강제 종료다. 협조적 COMSOL 정지는 이 소스에 없다. 따라서 새 감시가 과거 구현에 이미 있었다고 쓰지 않는다.

**제안/추론:** `contracts/RESOURCE_CONTRACT.json:7`의 한 실행당 초기 중지선은 합산 RSS8GiB, Job private commit10GiB, 출력증가5GiB이며 장래 Job commit 강제한도12GiB·출력 감시 ceiling6GiB와 구분한다. 초기 디스크16GiB, 잔여8GiB, host 가용RAM/commit 각2GiB는 정적 제안이다. 5초 간격·최대 sample gap6초·1초 sampling 시간과 native7200/전체9000초에서 종료예비120초를 둔다. 실제 필요량/성능/충분성을 측정하지 않았고 사용자 native 승인을 받지 않았다. 8GiB RSS는 OS hard cap이 아니다. 이 값을 실행 중 자동 완화할 권한은 없다.

**확인:** `assess_resources`는 누락·NaN·sampling오류·소유불명·중복집계를 정지 사유로 반환한다. Job RSS는 root/자식을 한 번씩 합산하며 공유 page의 중복 resident counting은 의미상 한계로 명시한다. Job commit total에 프로세스 totals를 더하지 않는다. `sampled_max`, OS peak, 실제 설치된 강제 상한은 별도 필드다. 현재 OS sampler/commit enforcement/주기 disk walker는 **미구현**이고 native gate를 막는다. 실제 API 선택은 현지 설치 경로와 공식 정의를 연결한 후 검증해야 한다.

정지 상태기는 `advance_stop`에 구현했다. **지원 확인된 협조적 요청1회 → 예산 안 최대15초 대기 → 소유 Job 강제 종료1회 → Job 비었음·root signaled·exit query·잔여·handle 오류 확인** 순서다. 협조적 수단 미지원이면 별도 사용자 force-only 동의가 없는 한 출발하지 않는다. 강제 종료를 graceful이라고 기록하지 않는다. 강제·확인90초 reserve가 부족하면 협조대기를 생략하고 예산 안 소유 Job 강제 경로로 간다. 소유 식별이 사라지면 unknown PID를 죽이지 않고 UNRESOLVED로 기록한다.

5→6GiB, 10→12GiB 여유는 관측되지 않은 최악 증가율을 보증하지 않는다. 스케줄링/커널 중지와 할당/쓰기 burst 때문에 감시 주기보다 늦게 발견할 수 있다. 디스크는 현재 quota가 없으므로 runtime hard cap 주장이 불가능하다. native 승인 전 sampled-only 위험을 명시 수용하거나 별도 quota 구현·검증이 필요하다. 자원 감시 계약 작성만으로 native-ready를 선언할 수 없다.

## 변경부 검증에 포함할 직접 대상

| 실제 함수 | 양성 및 음성 분기 | 기대 이유/판정 |
|---|---|---|
| authorize_execution | 완전한 inert 승인 fixture; manifest/engine/dependency/수용/사용자승인/σ/variant/window/argv/path/count/policy/attempt 차이 | AUTHORIZED_ONE_RUN 또는 지정 ContractError와 authorization 단계. 실제 제출 binding은 OPEN 거부 |
| execute_once | 승인 거부 뒤 spy sideeffect0; 첫 compile/batch/기록 실패 후 retry0; 후속 cleanup오류가 최초오류 보존 | 첫/후속 오류 순서, native 함수 모사 아닌 실제 orchestration 경로 |
| assess_resources | 정확 경계; 한 byte/시간 초과; 결손/NaN; stale sample; ownership/PID creation 변경; 중복집계 | CONTINUE_WITHIN_SAMPLED_LIMITS 또는 지정 STOP_REQUIRED 이유 |
| advance_stop | 지원 협조완료, 대기 만료, 미지원 force-only 미승인, 강제실패, 잔여PID, deadline·소유오류 | 지정 다음 동작/UNRESOLVED; unknown process kill0 |
| S1NativeAxis/S1Fields/S1Decision | 실제 Python consumer 출력, normal/protected/comparison-exceeded, fields 누락·숫자왜곡·summary모순·identity/rc/cleanup 차이 | 지정 단계의 INCOMPLETE 또는 축별 review 상태 |
| S1FinalReturn | 정확 경계; writer/readback실패; write 후 budget초과 | 마지막 반환 INCOMPLETE 우선; outerrc null |

위 표는 사례 설계 연결이며 이번에 함수/시험 엔진은 실행하지 않았다. 원래 BSave/BInvoke/C2/Job 전체 회귀시험을 다시 요구하지 않는다. 그러나 새 OS sampler·native/readback 어댑터가 구현되면 그 새 부분 검증과 source 재봉인은 필요하다. 현재 8항목의 3/7은 계약 및 pure logic은 준비됐지만 OS/COMSOL 연결까지 done으로 올릴 수 없다.

## 원본과 관측 한계

읽은 원본은 NORMAL480 CONTRACT/COMMAND_MAP/NATIVE_APPROVAL_FIELD_SPEC/PARENT_COMMAND 및 B020 legacy launcher/winjob 텍스트다. 원본 수정/실행0. 실제 engine version command, COMSOL API probe, 프로세스 시작/종료, 현재 prefs 변경0. 엔진 pins는 historical contract에서 전사한 값이며 현재 binary를 독립 재해시했다고 쓰지 않는다. production guard/time/OCP/수치 기준과 과거 state/실패/영수증을 변경하지 않았다.

## 마지막 정적 통합 보완

13:50 UTC 이후 root consumer의 실제 반환 필드와 다시 대조해 부모에서 세 연결부를 보완했다. charge가 INCONCLUSIVE이면 consumer의 INCOMPLETE를 부모가 수용 대기로 승격하지 않으며 limited_result와 축 상태를 대조한다. initial_profile의 N/P241점·표면/입자평균 검사와 invariants의 Li/전압 잔차, 비어 있지 않은 초기화 필드·전하 기록, 표면 최대차의 전극/두께좌표가 부모 필수 구조에 포함된다. 좌표 경계는 S0 Java 623행의 52/25/44µm이며 ±1e−15m은 기존 좌표 허용차다.

마지막 반환 함수는 유효한 결정 객체·음수가 아닌 유한 예산·0≤전달 시작≤기록 전 시각을 확인하고, 이전 오류가 있으면 기록 자체가 성공해도 INCOMPLETE를 유지한다. 이 보완은 정적 producer/consumer 대조에서 발견한 사안으로 실제 실패 traceback이나 기능 검증 성공을 관측한 것이 아니다. 마지막 바이트에 대한 정적 검사·다음 승인된 한정 시험 대상이다.
