# 별도 허용이 필요한 항목 — 비활성 제안

작성/수신은 실행 승인이 아니다. 현재 native_ready=false이며 P0조차 미승인이다. 아래는 하나의 포괄 실행 요청이 아니라, OPEN을 해결하기 위해 순서대로 검토할 최소 범위다.

## A. 이번 추가부 한정 검증

`LIMITED_VALIDATION_PLAN.json`에 고정한 새 함수만 대상으로 한다. Python 실제 함수·원 consumer/control과의 inert seam, 정확 Java helper 추출과 stub에 한정한다. 원 Parent/C2/Job 전체/130사례는 반복하지 않는다. 별도 사용자가 횟수·예산·engine/source/harness/fixture 봉인을 승인해야 한다. 실제 native·COMSOL jars·전체 Java 모델·입력·정책·프로세스/Job 시험은 여전히 제외한다. 통과해도 B–D나 P0를 자동 실행하지 않는다.

## B. OS counter의 primary 근거와 구현

로컬 Windows SDK/API 문서가 없으므로 GetProcessMemoryInfo 계열의 WorkingSetSize, host GetPerformanceInfo의 CommitTotal/CommitLimit/PageSize, Job 현재 commit을 제공하는 정확 information class/구조체와 Job memory limit set/query 의미의 공식 Microsoft 문서가 필요하다. 이번에 네트워크를 열지 않았다. 필요한 해당 공식 문서만 읽도록 별도 허용하거나 로컬 문서를 제공받는 안을 제안한다. API 이름 중 source에 없는 것은 탐색 후보이며 지원 확인이 아니다.

설치 OS에서 사용 가능한 counter를 확정한 다음 해당 ABI와 provider만 새 inactive revision으로 구현·한정 검증한다. 현재 commit 대신 PeakJobMemoryUsed 또는 프로세스 합을 넣지 않는다. 기존 12GiB commit 제한을 없애는 변경은 별도 사용자 결정이며 현재 문서로 허용하지 않는다.

## C. 설치본 설정/생성식 관측 후보

소스·설치 엔진·정확 출력 경로를 봉인한 뒤, **별도 승인한 모델 구성/mesh/study sequence 생성 및 read-back 한 번**을 제안한다. 호출 후보는 새 `s1OpenConfiguredReadback(m,sol,time)`, 원 `dumpSettings`, `featureInfo("info").getInfoTable(kind,"recursive","all")`이다. compile/JVM 모델 생성도 이번에는 0회이며 C의 실제 허용 범위·횟수·시간·메모리/디스크는 향후 실행 가능한 관측본이 만들어진 뒤 사용자 승인에 별도로 고정해야 한다. 현재의 inactive main을 몰래 활성화하지 않는다.

산출물은 CDI 실제 type/properties, Time consistent/read-back, solver sequence order, pcb1/pce1/pce2의 생성식과 domain/단위 표다. 이것만으로 post-consistency t0·실제 coefficient numerical value·native 성공을 인정하지 않는다. 생성식 변수/평가법을 먼저 검토한 뒤 별도 mapping을 봉인해야 한다. 임의 추가 initialization/solve나 설정 변경은 없다.

## D. t0·실제 계수·raw 로그 의미 관측

단 하나의 별도 승인된 P0 runAll 안에서 얻을 수 있는 관측을 우선한다. 필요한 산출은 CDI/Time 단계와 실제 solution index, 정확0의 Li/조성/농도/전위·전류, 생성식에 결속한 계수 평가, 전 저장 grid/guard pair/native 종료 원문이다. `s1OpenStoredGrid`는 저장시각만 확인하는 후보이며 초기화 단계 증명용 callback은 확인되지 않았다.

정확 post-consistency t0 provenance를 현 호출로 얻을 수 없다면 그 사실로 중지한다. 다른 runAll, runFrom/runTo, 초기화-only solve 또는 양의 시각 외삽은 자동 허용하지 않는다. 추가 호출이 필요하면 그 호출·관측 목적·횟수·예산과 기존 초기화 계약의 충족 가능성을 따로 제안한다.

## E. OS/process·중단 실제 관측

collector와 mapping을 고정하고 inert 검증을 수용한 뒤에만, 비-COMSOL 무해 자식 1개/소유 Job 1개의 한정 관측 시험을 별도 제안할 수 있다. 아직 정확 하네스·실행 예산을 고정하지 않았으므로 본 문서는 실행 요청문이 아니다. 실제 PID+creation·member 변화·counter/set-readback·종료/정리 증거가 필요하다. cooperative stop API는 UNVERIFIED. COMSOL에 대해 검증된 협조적 중단이 없으면 force-only 채택 여부를 별도로 판단하고 강제를 graceful로 보고하지 않는다.

## 그 뒤 P0 요청문의 전제

이번 준비 검토와 추가부 검증만으로 충분하지 않다. 설치본 t0/계수/raw proof, OS enforce/stop/provider, 새 source publication의 manifest schema·단일 argv/cwd·출력/승인 경로·현 prefs/자원 결속이 해결돼야 한다. 그때 P0 한 건만의 새 요청문을 작성한다. P1–P3, K cohort, 장시간, 정책 완화, microshort 효과 결과 주장은 계속 범위 밖이다.
