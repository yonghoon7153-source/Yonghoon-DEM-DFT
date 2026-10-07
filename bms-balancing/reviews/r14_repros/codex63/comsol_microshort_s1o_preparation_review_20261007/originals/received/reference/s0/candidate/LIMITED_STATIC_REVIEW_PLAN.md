# 변경부 한정 정적 검토 계획

## S0에서 한 것 — 텍스트/산술만

1. pinned GitHub Java를 텍스트로 받고99,959B 및 SHA256을 SPEC45-2/원본 식별과 대조했다.
2. 코드/초기재고/geometry/boundary/leakage expression/OCP tables/solver settings의 원문 줄을 읽었다. supplied Java/consumer/launcher를 실행하거나 import하지 않았다.
3. 새 후보만 apply_patch로 썼다. 기존 생산 소스·MPH·저장소 파일은 바꾸지 않았다.
4. 20개 정확한 before/after 문자열의 단일 발생 대조로 변환했고 unified diff를 생성했다. 후보와 diff의 길이/hash를 파일에서 읽었다.
5. 요청시각 개수401, 시각그룹187/50/54/110, 끝시각3600은 직접 쓴 작은 텍스트/산술 코드로 구했다. 이는 COMSOL 또는 제공 프로그램의 테스트가 아니다.
6. API 문서 확인: [COMSOL6.3 Time](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html)의 tout=tlist/strict. 실제 설치본 성능/동작 검증을 뜻하지 않는다.

## 후속 정적 검토 범위 — 아직 수행 승인과 구분

| 변경 | 무엇을 읽고 확인할 것 | 막아야 하는 실수 |
|---|---|---|
| sigma 매개변수 | SIGMA_S1_S_M→sigma_s1(S/m)→sigma_short→pcb1 diagonal sigma의 단일 흐름, epss .55/NoCorr | Bruggeman 이중 보정, 다른 전도도를 바꾸기 |
| 초기 조성 | XN_REST=.445; xP는 nLi_target 식; cl1200; LLI/LAM/총Li 동일 | 같은 SOC라는 말로 다른 총Li를 만드는 것, xP 독립 선택 |
| 휴지 전류 | ecd1 type/selection/nis=i_app, i_app=0 단위 A/m² | cdc1 출력을 활성화하거나 terminal voltage를 강제 |
| 시간 출력 | 401 exact list/증가/0/3600; endpoint shape guard; strict/tout=tlist/cap | request/stored/accepted 개념 혼합, .1s cap을 남겨 비용을 과소추정 |
| 누설 출력 | 기존 j=-intd2(Isx)/Lsep; I=A_c*j; units/count/header 일치; boundary2/3 phis | ∫dx Isx를 A로 오표기, 단자V와sepΔphi 혼동 |
| baseline 불변 | 물성/OCP/epss/LAM/LLI/mesh/입자/guard 식은 exact source 대조 | 기존 수용을 열거나 물성 맞춤 |
| 비활성 | .txt, main/run/modelSketch/preflight 진입 거부, .runAll( 호출 부재, export/launcher 부재 | 후보를 실행 가능 패키지로 착각 |
| binding | whole manifest 새로 고정; 기존480 consumer/contract 가져오지 않음 | 새 결과를 기존 ACCEPT/PASS로 오인 |

## 별도 승인 후 변경부 검증이 요구할 내용 — 이번 실행0

- compile/functionality/installed property readback는 사용자 별도 승인이다. CDI current-distribution type, transient consistent, stationary/concentration initialization 역할, NoCorr effective sigma equation, output unit를 읽는다.
- rest 상태 생성은 중간 xN/xP가 모든 위치에서 같은지, 초기 Li 재고가 기대값인지, zero external current인지 확인한다. 유한 sigma에서는 전위·반응전류가 sigma마다 달라지는 것이 일관적이다.
- cap/storage bridge는 하나의 비교에서 한 축씩: 동일 요청·cap에서 tout=tsteps vs tlist, 그다음 동일 storage/요청에서 cap 완화. coarse 요청 자체도 strict accepted step을 바꾸므로 그 축을 따로 기록한다.
- validation comparisons require exact common requested times and coordinates, completion/guards/range valid first, then V/x/Li/decomposition differences. 이전 충전 민감도값을 휴지 오차 바닥으로 쓰지 않는다.
- 새로운 자동 허용치를 임의로 추가하지 않음. 새 rest 분류 문턱은 부모 보고서의 사전 고정한 수치 민감도 기준선 규칙을 따르고, 미정/유한sigma 실패면 INCONCLUSIVE.
- 새로운 σ0항이 underflow 또는 cancellation로 계산된다고 추정하지 않음. 기준 σ1e−20의 거의0 전류를 denominator로 상대잔차를 만들지 않는다.
- 기존 보호식을 완화하지 않고 stop-before/after 증거를 유지한다. OCP none은 Newton trial에서 guard보다 먼저 실패할 수 있으므로 solver failure를 정상 완료로 재분류하지 않는다.
