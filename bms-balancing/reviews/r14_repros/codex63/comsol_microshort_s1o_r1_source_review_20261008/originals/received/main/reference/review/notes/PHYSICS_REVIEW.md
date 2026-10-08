# S1-O 준비 묶음 물리 계약/소비자 정적 검토

검토일: 2026-10-07. `received/` 아래 INITIALIZATION, COEFFICIENT_READBACK, CHARGE_BALANCE, consumer, 관련 검증 사례와 P0–P3 Java 텍스트를 읽었다. 후보 import/실행, 프로그램 실행, 합성 시험, COMSOL/JVM/compile/solve는 0회다. 아래 반례는 소스 분기와 식을 손으로 추적한 것이며 실행 결과가 아니다. 수신 원본은 수정하지 않았다.

## 결론

물리 설정·부호·단위 계약은 앞선 C2/C3 정정을 대부분 충실히 구체화했다. 설치본 CDI/실제 t0 추출/유효 계수 mapping/적분 오차 증거가 OPEN인 사실 자체는 오류로 세지 않는다. 다만 **현재 작성된 소비 함수의 요구사항 누락 두 곳**은 새 fixture와 함께 수정한 뒤 검증 계획을 다시 봉인해야 한다. 현 98사례를 실행하는 것만으로 이 두 결함을 확인했다고 할 수 없다.

## F-PH1 [P1] 전하 자료의 종점/전체 시간 격자를 실행에 결속하지 않아 짧은 prefix가 전체 실행 증거로 승격된다

**핵심 위치:** `candidate/consumer.py.inactive.txt:312`, `:220`, `:316`.

계약 `contracts/CHARGE_BALANCE.json:32`는 시작0과 종점, :56은 모든 실제 저장 시각, :116은 이벤트 전후를 포함한 실제 전체 저장 격자를 요구한다. 그런데 `charge_balance`는 :220에서 행 수>1·시작0, :233에서 시각 증가만 확인하며 예상 끝시각/원 격자를 받지 않는다. `analyze:295–300`은 native의 끝시각을 승인 끝시각과 대조하지만 :312에서 `data['charge']`는 그 끝시각 및 `data['global']`와 무관하게 평가한다. `compare_policy:183`의 table 시간 대조에도 charge가 없다.

정적 반례:

1. binding/native는 정상 종료120s, 비교용 global/N/P/profile 자료는 등록한 전체255시각을 모두 갖는다. 초기화·계수·단위·guard·비교 참조는 유효하며 각 시간의 총Li와 전압 항등식도 만족하도록 둔다.
2. charge만 실제0–1s prefix 두 행 `[0,1]`로 잘린다. 두 행의 `j=RN=I=0.25`, `RP=-0.25`, `A_c=1`, `LiN=N0-0.25*t/F`, `LiP=P0+0.25*t/F`, `LiE=E0`다.
3. 이 상수 전류의 사다리꼴 적분은 정확하므로 오차상한0을 주며, 그 **0–1s 격자에 대한** raw identity/grid 증거는 올바를 수 있다. 허위 해시나 임의 PASS 메타데이터를 만들 필요가 없다. native120s 증거와 1s 자료의 범위가 서로 다를 뿐이다.
4. `charge_balance`는 마지막 qN=qP=qI=.25이고 잔차0·방향분해됨이므로 `CONSISTENT`를 반환하는 분기다. 전체 비교는 별개 full-grid로 통과하고, `analyze:316–318`은 `evidence_validity='VALID'`, `limited_result='AWAITING_S1_LIMITED_EXTERNAL_REVIEW'`를 만든다.
5. 부모 `candidate/Parent.ps1.inactive.txt:112–113`도 charge records≥2만 요구한다. :171–174의 limited_result 결속은 잘린 범위를 발견하지 못한다. 최종 native 승인 자동 생성은 아니지만, 검토 대기 근거의 전하 범위가 잘못 승격된다.

**OPEN과의 구분:** `SOURCE_CONTRACT_LINKS.json:13,19`는 raw log/schema normalization adapter 미구현을 공개한다. 그러나 charge-vs-global 전체 격자 및 승인 종점 검사를 adapter에 맡긴다는 명시적 전제는 없다. :10은 charge schema와 analyze의 raw bound provenance만 연결한다. 지금 작성된 analyze의 여러 교차 결속 중 charge만 빠진 현상이다. 실제 native adapter 부재를 새 결함으로 세는 것이 아니다.

**수정 방향:** analyze에서 charge 시간열을 해당 실행의 검증된 실제 저장 시간열과 정확히 대조하고 끝시각을 native last_stored_s에 연결한다. 정규화된 LiN/LiP/LiE·RN/RP/j가 대응 global/leakage 원 열과 같은 자료인지도 결속한다. charge 반환값에 검증한 시작/종점/행 수/격자 식별을 포함하면 부모의 범위 확인도 가능하다. 별도 charge 격자를 허용하려면 계약 자체에 범위·재표본화·적분 증거 기준을 새로 정의해야 하며, 현재 계약은 전체 격자를 요구한다.

**검증안 보완:** `VALIDATION_PLAN.json:895–896`의 CHARGE11은 재정렬만 다룬다. 전체 native120s와 비교 자료는 그대로 두고 charge만 1s에서 자른 음성 사례, 중간 저장 시각만 빠진 사례, 올바른 full-grid 양성 대조를 추가해야 한다. 이번에는 실행하지 않는다.

## F-PH2 [P2] 누적 q만 검사하여 허용 범위를 넘는 구간 역방향 Li 이동을 놓친다

**핵심 위치:** `candidate/consumer.py.inactive.txt:237–238`, `:251–255`.

`contracts/CHARGE_BALANCE.json:110`은 실제 구간의 signed increment에도 동일 deadband를 적용하라고 명시한다. `notes/PHYSICS_CONTRACT_KO.md:58`도 누적/구간 전하2e−4 C/m²라고 설명한다. 하지만 소비자는 t0 대비 누적 qN/qP만 계산·검사한다. 직전 행 대비 변화량은 확인하지 않는다.

정적 반례는 다음과 같다. 실제 저장 시각은 `[0,100,100.001]`이며 추가 내부 시각은 allsteps 저장에서 가능한 형태다. `j=RN=I=.25`, `RP=-.25`, `A_c=1`, 적분 상한0으로 둔다. 모든 시각에서 `LiN=N0-q/F`, `LiP=P0+q/F`, `LiE=E0`이므로 총Li는 일정하다.

| t[s] | 전류 적분 qI=qRN=qRP [C/m²] | 재고에서 읽은 qN=qP [C/m²] |
|---:|---:|---:|
| 0 | 0 | 0 |
| 100 | 25 | 25.001 |
| 100.001 | 25.00025 | 25.00025 |

100s의 적분/재고 잔차 .001은 `2e−4+1e−4*25.001=.0027001`보다 작다. 다음 시각의 잔차는0이다. 점별 RN/RP/j·I 변환·총Li·qN=qP·누적 방향은 모두 통과하고 마지막 j/q는 deadband보다 커 `CONSISTENT` 반환 분기가 된다.

그러나 마지막 실제 구간의 qN/qP 변화는 **−.00075 C/m²**다. 이는 계약이 허용한 역방향 deadband −.0002를 넘는다. 양의 누설 중 N Li가 증가하고 P Li가 감소하는 구간을 계약상 감지해야 하는데 누적 양수에 가려진다. 이 반례는 결측 provenance나 OPEN native mapping에 의존하지 않는다.

**수정 방향:** prior 재고로 `dqN=F*(prior.LiN-row.LiN)`, `dqP=F*(row.LiP-prior.LiP)`를 계산하여 계약의 구간 부호 판정을 적용하고, 최초 역방향 시각/구간·값을 보존한다. 누적 수지와 구간 방향은 서로 다른 검사가 되어야 한다. 잔차 상대 허용치를 넓히거나 누적 조건만 유지하여 구간 조건을 암묵적으로 없애면 안 된다.

**검증안 보완:** `VALIDATION_PLAN.json:847–858` CHARGE08의 “reverse Li transfer beyonddeadband”는 구간만 역방향인 조건을 명시하지 않는다. 현재 구현대로 t0 대비 누적 음수만 넣으면 이 결함을 놓친다. 위처럼 누적은 계속 양수이고 모든 적분 잔차도 한도 안인 구간 역방향 사례와 정확 deadband 경계 사례를 구체화해야 한다.

## 검토했으나 확정 오류로 세지 않은 사항

- **초기화:** `INITIALIZATION.json:269–319`는 구성/실제 post-consistency t0/완료를 분리하며 첫 양의 시각을0으로 바꾸지 않는다. `consumer:108–125`의 시각·단위·절대 AND 상대 검사와 :162–174의 표면/입자평균 균일성은 계약에 맞는다. 실제 CDI type·추출 가능한 native 단계가 OPEN인 것은 정직하게 공개했다(:322–334).
- **설정과 유효 계수:** `COEFFICIENT_READBACK.json:15–21`은 adapter projection을 null/OPEN으로 두고 raw identity 검증을 upstream adapter에 명시적으로 맡긴다. `consumer:206–215`가 호출자가 준 기대 mapping을 신뢰한다는 사실만으로 현 오류라고 세지 않는다. 풍부한 원 계약을 해당 함수에 직접 넣어 KeyError가 난다는 지적도 하지 않는다. 실제 mapping이 봉인될 때 절대/상대 허용치 투영을 확인해야 한다.
- **초기 쌍:** `compare_initialization_pair:149–159` 함수가 존재하며 `paired_classification:263`은 pair_initialization PASS를 요구한다. `SOURCE_CONTRACT_LINKS.json:8,12`는 미래 cohort assembler를 OPEN으로 둔다. analyze가 그 함수를 직접 호출하지 않는 사실만으로 near-zero/finite cohort 기능이 완성됐다고 주장하는 오류를 만들지 않는다.
- **near-zero 상태 분리:** `charge_balance:254–255`는 near-zero 방향 미분해를 전체 charge INCONCLUSIVE로 합친다. CHARGE02(:763–770)가 이를 의도적으로 기대하므로 단순 오타는 아니다. 한편 계약 :109,130–139 및 paired_classification:263–264는 좋은 conservation과 미분해 direction을 구분한다. 미래 cohort가 near-zero 보존의 유효성과 방향 미분해를 어떻게 따로 인계할지 출력/매핑을 구체화해야 하지만, OPEN cohort 어댑터를 완성된 것처럼 보고 확정 결함 수를 늘리지 않았다.
- **Java의 물리 보존:** 네 P 변형 모두 xN=.445(:19), 재고에서 xP 유도(:639), ce1200/T298.15(:634), 외부전류0(:643), NoCorr(:687), RN/RP/j의 기존 부호·면적 변환(:448–458)을 유지한다. CDI는 생성만 하고 type을 확정하지 않는다(:714). deny 차단과 부재한 runAll은 비활성 원칙에 맞으며, 실제 실행 성공을 보장하는 근거는 아니다.
- **q 적분 상한:** 모든 prefix와 j/RN/−RP를 덮는 증거가 없으면 null/INCONCLUSIVE로 남기는 계약은 적절하다. 실제 상한이 아직 없는 사실은 미구현 오류로 세지 않는다. scalar 상한이 초기 작은 예산에도 적용되어 매우 보수적일 수 있다는 설계 비용은 있지만, 현재 두 확정 결함과 섞지 않는다.

## 검증 승인에 대한 범위 판단

현재 두 누락을 고치고 해당 반례의 기대 거부 이유/도달 함수·횟수/상한을 수정한 계획을 먼저 제시하는 편이 타당하다. 이 노트는 후보 수정이나 98사례 실행을 승인하지 않는다. 수신 묶음의 `native_ready=false` 및 설치본/OS adapter OPEN은 그대로 유지되어야 한다.
