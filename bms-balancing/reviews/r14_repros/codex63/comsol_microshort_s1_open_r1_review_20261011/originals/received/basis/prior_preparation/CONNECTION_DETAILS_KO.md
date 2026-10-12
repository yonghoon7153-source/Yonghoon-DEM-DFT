# OPEN별 실제 연결과 변경 경계

## 1. 설치본 관측 순서 후보

원 P0 `main`, 모델 작성 진입점, `preflightAudit`의 차단을 모두 유지했다. 다음은 **향후 별도 승인과 새 실행본 검토가 있어야 삽입할 순서**이며 이번 후보가 실행하는 순서가 아니다.

1. source 설정과 입력/설치 엔진 SHA를 결속한다. 모델 생성·mesh·study sequence 생성 자체도 이번에는 실행하지 않는다.
2. 생성된 solver sequence의 type/순서를 raw로 기록한다. `s1OpenConfiguredReadback(m,sol,time)`가 CDI feature type/typed properties, Time typed properties, pcb1/pce1/pce2 typed properties 및 생성 정보표를 출력하는 후보 호출이다. 실제 CDI 속성 이름/enum을 관측하기 전 기본값을 추정하지 않는다.
3. 별도 승인된 단 하나의 runAll 안에서 CDI와 Time의 단계 기록을 보존한다. 현재 helper에는 runAll 호출을 추가하지 않았다. `runFrom/runTo`, `runAll(false)`, 추가 initialization solve로 대체하는 제안은 없다.
4. 반환된 solution과 daudit를 결속한 뒤 `s1OpenStoredGrid(m)`와 기존 35계열 출력 경로를 사용한다. 이 단계는 저장된 t=0을 선택할 수 있어도, 그것이 일관 초기화 직후의 값이라는 의미 증명은 따로 필요하다. 재평가/보간한 양의 시각을 0으로 표시하지 않는다.
5. 설치본 문서/솔버 단계/실제 solution index가 post-consistency 의미를 입증하지 못하면 `INITIAL_PROVENANCE_OR_TARGETS`는 해결되지 않는다. 추가 초기화 호출은 자동 추가하지 않는다.

Time consistent=`bweuler`는 미세 초기 변화 가능성이 있다. 농도/재고의 동일성은 기존 absolute AND relative 기준으로 판단하며 이 준비에서 consistent/initialstep/물리·메시·rtol/cap을 바꾸지 않았다.

## 2. 실제 producer → raw → 소비 필드

| 원 P0 출력/식 | domain·단위 | 연결·판정 |
|---|---|---|
| `preflight_global.csv`의 time_s | 전체 저장 해·s | native stored grid와 원소별 정확 비교. 요청 tlist와 별도 |
| `Li_N_mol_m2` = intd1(epss*cs_average) | 1·mol/m² | global 및 charge.LiN을 동일 행에서 투영, 초기/총수지 원 기준 유지 |
| `Li_P_mol_m2` = intd3(epss*cs_average) | 3·mol/m² | charge.LiP |
| `Li_electrolyte_mol_m2` = Σintd(epsl*cl) | 1/2/3·mol/m² | charge.LiE |
| `s1_leakage.csv`의 `j_leak_leftward_A_m2` = −intd2(liion.Isx)/L_sep | 2·A/m² | charge.j, global 중복 j 일치 |
| `I_leak_model_A` = −A_c intd2(liion.Isx)/L_sep | 2·A | charge.I. A_c=1 m² 모델 면적; A_cell 실험 면적 전환 아님 |
| `reaction_N_A_m2` = intd1(liion.ivtot) | 1·A/m² | charge.RN. ivtot 자체는 A/m³이며 두께 적분 후 A/m² |
| `reaction_P_A_m2` = intd3(liion.ivtot) | 3·A/m² | charge.RP. 원 부호 RN−j, RP+j 유지 |
| boundary1/4 phis, Eeq/etaMid/phil | 0D 경계·V | 단자 P−N 정의/기존 invariant. separator drop과 혼동 금지 |
| boundary2/3 phis | 분리막 경계·V | sigma_short*(phis3−phis2)/L_sep 보조 crosscheck; 계수 생성식 증명 아님 |
| 기존 profile N/P | domain1/3·241좌표, m/무차원 | 동일 시간·좌표·domain/범위/단위; 임의 공간 산술평균으로 대체 없음 |
| eguard/전체·domain Minimum | Lagrange5·mol/m³ | solver와 같은 operator·selection·단위 및 마지막 두 실제 저장 시각을 결속 |

바이트 loader가 각 원표/units/로그/시간축의 SHA를 먼저 확인해야 한다. 현재 numeric_table은 전달받은 unit array를 대조하지만 units CSV의 native 의미 검증 parser를 구현했다고 하지 않는다. 향후 loader는 해당 CSV 원문 파싱과 Java 설정/평가 후 단위를 모두 연결해야 한다.

`charge_projection`은 스스로 단위/해시 검사 loader를 호출하지 않는 낮은 수준 함수다. `numeric_table → bind_grid → charge_projection` 순서를 향후 loader에 고정해야 한다. 이 순서 없이 raw provenance를 부여하지 않는다. `source_binding`에는 native_grid/global/파생 charge 각각 실제 bytes identity와 run/manifest가 필요하며, 파생 charge의 자기 identity는 파일을 쓴 뒤 생성되어야 한다.

원 consumer의 `coverage`, `charge_balance`, `compare_initialization`, `verify_coefficient_evidence`, `analyze`, 원 Parent `S1NativeAxis/S1Fields/S1Decision/S1FinalReturn`은 모두 불변이다. 새 native→Parent projection도 아직 별도 구현 대상이다. 이미 수용된 함수의 논리와 실제 native adapter의 완성은 다르다.

## 3. 계수 관측의 네 층

| 층 | 입력/산출 | 현재 상태 |
|---|---|---|
| SOURCE_CONFIGURED | 원 Java transport/electrode/pcb1 literals + SHA | 정적 확인 |
| NATIVE_SETTING_READBACK | typed properties의 실제 호출 결과 + raw bytes SHA | helper만 작성, 호출 0 |
| GENERATED_EQUATION_LINKED | Expression/Weak/Constraint/Shape의 실제 domain별 행·변수·의존 chain + 표 SHA | API 문서 확인, 실제 행/변수 null |
| ACTUAL_COEFFICIENT_EVALUATED | 생성식에서 확인한 변수의 EvalGlobal/도메인 평가 raw·단위·시각 | 변수/선택·수치 평가 미관측 |

pcb1(domain2): ElectricCorrModel=NoCorr, user sigma_short, epss=.55/epsl=.45. 추가 porosity multiplier를 자동 곱하지 않는다. pce1(domain1)/pce2(domain3)의 fs 및 electrolyte의 fl/fDl/fmob는 원 `COEFFICIENT_READBACK.json`을 그대로 참조한다. 분율 factor의 산술 평가를 생성식의 어느 항에 적용되는지 확인한 것으로 바꾸지 않는다. 저장항 epsl와 수송계수 위치도 분리한다.

기존 expected.consumed가 채워지지 않은 상태를 유지한다. helper로 실제 표를 받은 뒤 variable/domain/unit/chain과 evaluation 수치를 검토해 독립 mapping seal을 만들기 전에는 `INSTALLED_MAPPING_OPEN`이다. mapping SHA가 없는 정상 fixture를 생산 mapping으로 사용하지 않는다.

## 4. 실행/OS/부모의 연결 경계

| 기존 코드 | 재사용할 부분 | 새로 필요한 연결 |
|---|---|---|
| control.authorize_execution | 승인·엔진·의존·argv/cwd·path·정책·native_ready 검사 | 새 adapter/policy/current pins/출판 manifest schema 결속. 현재 R1 manifest schema와 gate의 V1 schema 차이도 출판 단계에서 명시 해결해야 함. 이번에는 변경하지 않음 |
| control.execute_once | exclusive reserve→fresh 입력→stage→compile/batch 1회→분석→최종 기록 순서 | 모든 native 메서드의 실제 adapter. 기존 launcher 전체 재사용 금지 |
| winjob WindowsJobTransport/NativeExecutionKernel | private Job, suspended root, assignment, 보유 handle, 기본 종료 검증 | 모든 member creation FILETIME·periodic counters·12GiB Job commit set/readback·정확 deadline sampler |
| control.assess_resources | 샘플 범위·한도·reserve 판정 | resource_connection의 실제 원관측 provider 및 identity trust chain |
| control.advance_stop | bounded cooperative/force/verify 상태기계 | 실제 cooperative API 미확인, OS dispatcher 미구현. force-only는 별도 결정 |
| Parent.S1FinalReturn | 쓰기/readback 뒤 예산 및 앞선 PASS보다 오류 우선 | 새 실행 연결에서 제공할 실제 writer/clock/child rc, NoExit outerrc=null 유지 |

반환 schema 변환만으로 raw-binding-valid=true, resource_enforcement_ready=true 또는 native_ready=true를 만들지 않는다. 실제 provider와 출판 entry가 없는 현재 고정 cwd/argv는 과거 비활성 계약의 자료일 뿐 실행 명령으로 제시하지 않는다. 새 후보 파일은 전부 `.inactive.txt`이고 이번 폴더에 approval/release/token/runtime/실행 폴더를 만들지 않았다.

## 5. 최소 변경

원 21개 구성원 수정 0. 기존 control/consumer/Parent 변경 0. P0 새 사본은 `P0.connection.diff.txt`에 보이는 호출 없는 helper 삽입 한 건이다. 두 Python 파일은 새 파일 diff로 전부 제시한다. helper가 추가된 사본은 새 SHA이고 원 R1의 기능 수용으로 새 API 호출 성공을 주장할 수 없다. 미래 실행 가능 출판을 위해 차단문을 제거하거나 호출 지점을 삽입하는 작업은 이번 변경에 포함되지 않는다.
