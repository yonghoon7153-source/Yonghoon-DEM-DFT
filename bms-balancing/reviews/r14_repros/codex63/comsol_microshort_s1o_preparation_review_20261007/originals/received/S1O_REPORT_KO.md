# S1-O 오프라인 준비 결과

2026-10-07. **소비·승인 결속·부모 판정·자원 중지 상태기의 비활성 소스와 8개 미결 항목의 계약을 작성했다. 설치본 readback/native 연결과 OS 감시 어댑터는 OPEN이다. native_ready=false이며 이 묶음으로 COMSOL을 실행할 수 없다.**

사용자의 “ultra로 ㄲ”를 첨부 cover/v2의 S1-O 범위 채택으로 적용했다. cover의 고정 커밋 f2d6fa0a985b4f62cd44729ebea3051cccf48d97을 기준으로 삼았고, 원격 브랜치를 가져오거나 최신본으로 교체하지 않았다. 첨부 문서는 증거이며 추가 실행 권한으로 사용하지 않았다. 실제 검증 및 P/M/N은 각각 별도 승인이다.

입력 S0 ZIP은 417,467B/SHA e8c386913338198c9b1535a9131667f23c8a144232ae8fbf548acfd3748ea12e, v2는14,688B/SHA16797cc16cf5b95bcef6e55d7f342b288300859c8d68df55bb7860a6a5e1b967이다. S0 38 payload+manifest의 정확 집합·크기/SHA·CRC·경로/링크를 자체 데이터 읽기로 확인했다. reference/s0는 원바이트 사본이다. 근거: INPUTS_BEFORE.json:1, intake_static.py:1. **확인**은 이 정적 읽기 범위이고 원격 Git/COMSOL 설치본 검증이 아니다.

## 1. 초기화 계약 — partial

정확한 모델 표현식·도메인·단위와 초기 목표를 INITIALIZATION.json에 연결했다. N/P 고체 Li 목표는 각각 약0.4483674367149664/0.7398582418193119mol/m², 전해질 Li는0.04867728538091210mol/m²이다. xN=.445, xP≈.5811516557009894, ce1200mol/m³이다. 계산은 원 파라미터의 Decimal 산술이며 COMSOL 초기화 결과가 아니다. LAM_PE=.0296398242, LAM_NE=.0257219788, LLI=.0439355가 이미 포함된다. near-zero 및 fresh는 무열화 신품을 뜻하지 않는다.

초기 Li 각 항은 절대≤1e−9mol/m² 및 상대≤1e−6, 초기 x는 절대≤1e−8 및 상대≤1e−6, ce는 절대≤1e−5mol/m³ 및 상대≤1e−8을 **사전 제안**한다. 고정 목표뿐 아니라 near-zero/finite 쌍 차이와 t0의241좌표 표면·입자평균 균일성을 검사하는 함수를 작성했다. σ에 따라 달라지는 대수 전위·누설전류를 동일하게 맞추지 않는다. ground 기준만 같은 목표다.

구성 후 solve 전 / 일관 초기화 직후 정확t=0 / 완료 후를 분리했다. 0+ 자료만 있으면 실제 시각으로 남기며 초기 재고 검증을 대신하지 않는다. 현재 S0는 CDI를 생성하지만 설치본 CDI type, 한 번의 승인된 solve 안에서 post-consistency t0를 증명하는 변수·단계 추출은 확인되지 않았다. 추가 초기화 solve를1회 안에 숨기지 않는다. 근거: contracts/INITIALIZATION.json:1, notes/PHYSICS_CONTRACT_KO.md:1 및 candidate/consumer.py.inactive.txt의 compare_initialization, compare_initialization_pair, initial_profile_uniformity(정확 줄은 SOURCE_INDEX.json). **산술/소스 확인, 실행 효과 미확인**.

## 2. 계수 readback — partial

분리막 epss_short=.55, ElectricCorrModel=NoCorr, sigma_short 대각 텐서 설정을 확인했다. 전해질 보정은 각 영역의 epsl과 인수 표현식·단위를 계약에 기록했다. 설정값 목록은 실제 방정식 소비 증거와 다르다. 설치본의 유효 전도도/수송 계수 변수와 생성식 연결, 수치 평가 위치 및 API는 OPEN으로 둔다. 소비자의 verify_coefficient_evidence는 비어 있는 계수집합, settings-only 증거, 단위/허용차 불일치를 거부한다.

COEFFICIENT_READBACK의 rich contract를 임의로 producer 결과에 직렬화하지 않는다. adapter_projection=null/OPEN이며 installed equation mapping과 실제 raw 식별이 먼저 필요하다. 근거: reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt:680, contracts/COEFFICIENT_READBACK.json:1, notes/PHYSICS_CONTRACT_KO.md:1. **설정 소스 확인, 실제 소비 OPEN**.

## 3. 실행 연결과 승인 결속 — partial

candidate/control.py.inactive.txt에 manifest·검증 수용·별도 native 승인·run/variant/σ/초기화/시간창·의존/엔진·argv/cwd·IO·횟수·예산·정책·경로 부재를 대조하는 authorize_execution과 한 번 실행의 제어 골격을 작성했다. 첫 adapter 쓰기는 승인 gate 뒤다. 기본 어댑터는 거부하며 현재 manifest와 binding의 native_ready=false, OPEN blockers, 미확정 명령/경로/prefs가 실행을 차단한다. `.inactive.txt` 표지만을 차단 근거로 삼지 않는다.

PowerShell 부모는 실제 소비자의 nested 근거와 수치 문턱, native/analysis rc, 보존·정리·정책·자원, 최종 기록 후 예산을 따로 소비하도록 작성했다. Python→PS producer/consumer 연결은 정적으로 맞췄으며 기능 실행은 하지 않았다. 수치 비교 EXCEEDS_LIMITS는 실행 오류와 분리한다. charge INCONCLUSIVE나 필수 근거 누락을 앞선 요약 PASS로 덮지 않는다.

NORMAL480 원본10개를 별도 읽기/해시 보존했다. 기존 소유 Job·C2·BSave/BInvoke 설계의 재사용 근거를 명시하되 새 guardian과 그대로 호환된다고 주장하지 않는다. 기존 launcher에는 정책 적용/원복 단계가 있으므로 통째로 호출하지 않는다. **현재는 OS sampler/native/readback 구현이 없는 fail-closed 연결 골격**이다. 실제 배포하려면 정확 adapter·실행 경로·정책 식별을 채우고 변경부를 다시 봉인/검증/승인해야 한다. 근거: contracts/EXECUTION_BINDING.json:1, notes/EXECUTION_RESOURCE_KO.md:1, SOURCE_INDEX.json. **비활성 코드 확인, end-to-end native 연결 미완**.

## 4. P0–P3 정책 대조 — done(오프라인 범위)

P0는 fresh highσ1.7e−6,0–120초,dense1337요청,tout=tsteps,oldcap이다. P1은 저장만tlist, P2는 요청만sparse255, P3는 cap만S0제안으로 바꾼다. rtol/초기step/물리/초기상태/guard는 동일하다. 네 비활성 Java 텍스트와 diff를 candidate/variants에 만들고 허용 literal 역치환이 S0 전체 원바이트와 일치함을 확인했다. denyS0Execution과 runAll 부재를 유지한다. 로그는120초 변형임을 표시한다. 이것은 컴파일/API 호환성 판정이 아니다.

consumer의 주 판정은 사전등록255개 정확 요청시각×전극별241좌표다. 전체 adaptive 저장 교집합은 별도 기록하며, 각 run 자신의1337/255요청 누락도 거부한다. 보간·최근접 대체·빈/t0-only 비교는 허용하지 않는다. 전압≤1mV, 표면x≤1e−4, 총Li차이/드리프트≤1e−6, 전압분해잔차≤1e−8V를 유지한다. 정상·보호중단·오류를 구분한다.

120초 pilot은300초 이후 cap을 검사하지 못한다. 이를 숨겨 P에5번째 실행을 넣지 않았다. 후기 cap은 별도 M/N의같은σ·near-zero 대응쌍으로0–3600 및2700–3600에서 확인한다. 그 전 장기 판정은INCONCLUSIVE다. 근거: contracts/POLICY_VARIANTS.json:1, VARIANT_STATIC_RESULT.json:1, candidate/consumer.py.inactive.txt의 coverage/compare_policy. **시간/변경바이트 확인, 정책 효과 추론/미검증**.

## 5. K 및 실행 수 — done(제안)

기본σ4개×3600초 M4, rtol·cap·입자·물리 격자 각 축에 동일σ4개×4축 N16을 사전 고정하는 보수적 초안이다. 같은 설정의 near-zero는 세finiteσ의 Dk/Sk에 공유하여 중복 집계하지 않는다. M/N 고유20회+P4=총24회이며 현재 승인횟수는0이다. rtol1e−7,cap반감,입자640/640,물리240/120/240 및 창·순서는 K_DESIGN에 구체화했다. 한 번에 두 축을 바꾸지 않는다.

전체24회×제안9000초는 명목 상한60시간이다. 자동 실행 계획도 완료 비용 보증도 아니다. 먼저 P 실측으로 비용을 검토한 뒤 M/N 예산을 따로 확정해야 한다. 비용 때문에 축/σ/후기 창을 줄이면 해당 신호의최종분류는INCONCLUSIVE이며 주 결과를 보고 유리한 축만 고르지 않는다. K를 주 사다리 전에 고정하고 변경 시 사전등록 위반/해석 범위를 기록한다. 근거: contracts/K_DESIGN.json:1, notes/POLICY_K_COST_KO.md:1. **개수/설정 연결 확인, 비용·결과 추정**.

## 6. 전류·전하 수지 — done(오프라인 계약)

j=−intd2(Isx)/Lsep와RN/RP는A/m², I=A_c·j는A, q는C/m²이다. A_c=1m² 모델 면적을 실험면적으로 바꾸어 해석하지 않는다. RN≈j,RP≈−j,RN+RP≈0 및 총Li보존을 확인하고 qN=F(nN0−nN),qP=F(nP−nP0),qI/qRN/qRP는 실제 불규칙 저장 격자의 trapezoid로 계산한다.

전류 잔차≤1e−8A/m²+1e−4·scale, 전하 잔차≤2e−4C/m²+1e−4·scale을 제안한다. 전하 절대항은2F·1e−9mol/m²≈1.9297e−4C/m²를 올림한 사전 배분이다. 누설near-zero를 나눗셈 분모로 쓰지 않는다. 부호 deadband는j1e−8A/m²,q2e−4C/m²이다. t0는부호판정비대상, 이후 양 전극과j의신호가모두분해되어야 방향일관성을 주장한다. 미분해는RESOLUTION_LIMITED이며 역방향 초과와 다르다.

성긴 출력의 적분 오차는 Li수지와 별도로 취급한다. raw 근거에 결속된 모든prefix·j/RN/−RP에 유효한 오차상한이 있어야 하며, 상한≤허용차/4 및 |잔차|+상한≤허용차로 판정한다. 임의의 coarse/fine 차이를 엄밀한 상한으로 바꾸지 않는다. 상한이 없으면chargeINCONCLUSIVE다. 근거: contracts/CHARGE_BALANCE.json:1, notes/PHYSICS_CONTRACT_KO.md:1, consumer의charge_balance. **단위·산술 확인, 새 허용치 제안**.

## 7. 자원·소유 종료 — partial

5초 표본/최대6초 간격, 소유 Job 멤버RSS 합·Job commit·host가용RAM/commit·소유출력증가·volume여유·wall을 따로 기록하는 계약이다. 예시 제안은RSS조기중단8GiB,commit조기10GiB/향후Job강제12GiB,출력조기5GiB/감시천장6GiB,시작disk16GiB/free reserve8GiB다. 이 값은 현재 구현된 한도나 PC 충분성 보증이 아니다. 특히 RSS합에는 공유page가 중복될 수 있고 OS정확peak/hardcap과 다르다.

지원 확인된 협조적 중지→남은시간 내 한정대기→소유Job강제종료→root/Job종료확인을 상태기로 분리했다. 협조적 API가 없으면 없다고 쓰며 별도 force-only 수용 없이는 시작할 수 없다. TerminateJobObject는 강제종료다. 샘플/기록/소유 증명 실패는0/PASS가 아니다. 모든 중단/종료확인/기록은120초 reserve와run전체상한 안에 포함한다. 알 수 없는PID를 이름으로 일괄 종료하지 않는다.

기존winjob은 시작RAM/디스크와 소유강제종료 근거이며 새 periodicRSS/commit/disk sampler 또는Jobcommit상한이 구현됐다는 증거가 아니다. OS어댑터·실측지연·강제상한·협조적수단은OPEN이다. 근거: contracts/RESOURCE_CONTRACT.json:1, notes/EXECUTION_RESOURCE_KO.md:1, control의assess_resources/advance_stop. **기존 코드/새 상태기 확인, OS강제동작 미검증**.

## 8. pilot 비용과 예산 — done(계약)

P에서 compile/batch/적분/저장·export/분석/포장wall,accepted steps와Tfail/NLfail,요청/저장개수,MPH/CSV/log크기,메모리표본최대와가능한OSpeak를 각각 관측한다. 원 NORMAL480의긴출력 비용은 출처 있는 참고치이며 새로운 유한σ파일의비용으로 대체하지 않는다.

다음 예산은 관측 비용×격자/step/출력 비율 가정+별도 여유로 나누어 산정하고최대계산/전체/정리단계를 따로 승인한다. 여유산식과불확실성은COST_MODEL에 있다. 표본max를hardcap준수증거로 바꾸거나모든σ·격자의성공을 보증하지 않는다. S0의 .096/.962/9.504mV는평균조성OCV사전예측이다. M에서 평균OCV/terminalV/pairedD를서로별도열로 대조하며 예측에맞추어σ/OCP를수정하지 않는다. 근거: contracts/COST_MODEL.json:1, notes/POLICY_K_COST_KO.md:1. **산술/출처 확인, 미래비용 추정**.

## 9. 한정 검증안과 현재 정적 확인

검증안은 **8군98사례(Python82·PowerShell16)**다. 대상함수·엔진현재hash·fixture위치/argv/cwd·기대이유·도달단계·예산은 VALIDATION_PLAN.json 및 한국어판에 고정한다. 합성 하네스와입력별원바이트는 다음 별도승인 범위에서 첫시험 전에 봉인한다. 현재 후보를import하지 않았으며 실행한 기능사례 수는0이다. 생산 코드는 시험 통과를 위한 사후수정/재시도 대상이 아니다.

새 자체 정적 스크립트만 실행했다. JSON/AST/PowerShell구문파서의데이터읽기·원바이트해시·Decimal산술·텍스트생성/ZIP검사는 기능검증이 아니다. 구문파서는 bundled PowerShell assembly이며 Windows PowerShell5.1 실행 호환성을 입증하지 않는다. 마지막수정후 정적결과·같은선택원본전후식별·시간은 STATIC_AUDIT.json/SELECTED_ORIGINALS_AFTER.json/TIMING.json에 기록한다. 정적작성 중 경로부재검색과 적용실패patch는 PREPARATION_EVENTS.json에 남긴다. 자체 정적 검사기의 경로 구분자 KeyError와 원문은 audit_history/FIRST_STATIC_ERROR.json 및 원 검사기 사본으로 보존했다. 원인만 정정했고 후보/기능 시험을 재실행한 것은 아니다.

## 10. 자기 점검과 다음 경계

판정 불능의 가장 그럴듯한 경로는 (a) 설정readback만있고 실제초기화/계수소비가없는경우:두단계증거와OPEN차단, (b) 저장성김으로요청시각/전하적분신뢰가없는경우:고정255시각·별도교집합·quadratureINCONCLUSIVE, (c) 비용초과/감시실패/소유종료미확인인데rc0만있는경우:자원상태기와부모POST_WRITE오류우선이다.

다음 검토자는 제안초기값/전하한도,설치readback매핑,비활성소스실제연결,예산/강제상한구현범위,K24회비용/축축소시해석한계를 확인해야 한다. 그 뒤 변경부검증만 별도로 승인할 수 있다. **현재 P승인문은 실행가능한최종문이 아니라 OPEN 해소를 조건으로 하는 비활성 요청문이다.** 어댑터/Java readback에바이트변경이생기면새manifest와그변경부검증이필요하다.

COMSOL/JVM/compile/solve/실제gate/정책변경/실험대조/기존프로그램실행/합성시험은0회다. 기존overall/normal gate INCOMPLETE,내부실효정책/실제코어UNVERIFIED,과거실패/pending/원복,recipient=null과MPH는변경하지 않았다. 960초/12시간/OCP교체/후보C/외부자동전송은수행하지 않았다. 제출후멈춘다.
