# S1-O 초기화·계수·수지 계약

이 문서는 오프라인 계약의 구체화다. COMSOL 초기화·계수 소비·수지의 실제 PASS가 아니다. 모든 새 허용값은 결과를 보기 전에 고정할 제안이고, 승인·검증 이후 변경하려면 새 식별이 필요하다.

## 1. 같은 초기 농도와 재고

**[확인]** 원 S0 Java는 `x_Gr_rest=0.445`, `x_NCM_init=(nLi_target−epss_el*L_el*cs_Gr_max*x_Gr_init)/(epss_pos*L_pos*cs_NCM_max)`, `c_e_init=1200 mol/m³`, `T_init=298.15 K`를 쓴다. LAM_NE=0.0257219788, LAM_PE=0.0296398242, LLI=0.0439355는 이미 고정 입력이다. near-zero 단락 기준은 무열화 신품이 아니다. 근거: `reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt:623`, `:625`, `:634`, `:636`.

50자리 Decimal 산술로 구한 목표는 다음과 같다. COMSOL 평가값이 아니라 원 literal의 계산이다. 근거 코드와 원문 출력은 `physics_contract_arithmetic.py`, `PHYSICS_ARITHMETIC.json`, `PHYSICS_ARITHMETIC_TOOL_RETURN.json`이다.

| 값 | 목표 | 단위 |
|---|---:|---|
| xN | 0.445 | 1 |
| xP | 0.5811516557009893640642438699745874 | 1 |
| N 고체 Li | 0.448367436714966419370720 | mol/m² |
| P 고체 Li | 0.7398582418193118957256133954226276 | mol/m² |
| 전해질 Li | 0.048677285380912099200 | mol/m² |
| 총 Li | 1.236902963915190414296333395422628 | mol/m² |

**[제안·추론]** 초기 Li 각 항은 절대차≤1e−9 mol/m²와 상대차≤1e−6를 **둘 다** 요구한다. 전극 평균/표면 극값/241좌표의 표면·입자평균 x는 절대차≤1e−8, 상대차≤1e−6; 전해질 전체 최소·최대는 1200에서 절대차≤1e−5 mol/m³, 상대차≤1e−8다. 상대 분모는 `max(|목표|,절대한도)`다. 전체 시간의 총 Li drift 상대≤1e−6는 별도 기준이다. 이 초기조건 기준은 입자·표면의 비교 한도1e−4와 구분한다. sigma별 각 목표 통과뿐 아니라 near-zero와 finite의 초기 농도·재고도 같은 절대 한도로 직접 비교한다. 따라서 각 값이 목표의 양쪽 끝에 놓여 두 배 차이가 나는 것을 수용하지 않는다.

`INITIALIZATION.json/consumer_projection/targets`는 실제 소비자가 사용할 변수명·식·단위·domain·숫자를 담는다. xavg는 `intd(cs_average)/(L*csmax)`이고 241점의 임의 산술평균이 아니다. 일정 epss/csmax하에 재고식과 연결된다. N domain1의 0–52 µm, P domain3의77–121 µm가 전극 두께좌표다. 입자 반경이 아니다. 근거: Java `:448`, `:450`, `:581`, `:590`.

**[확인]** S0는 CDI를 생성하지만 CDI type을 고정하지 않았고 `Time.consistent`는 읽기만 한다(Java `:714`, `:541`). **[OPEN]** 설치본 CDI type 속성명, 해당 native sequence에서 일관 초기화 완료 뒤 실제 t=0를 추출·증명하는 방법은 확보되지 않았다. 현재 계약은 다음 세 기록을 구분한다.

1. `configured_pre_solve`: CDI/Time 원 속성·selection·csinit·cl·원 param/단위를 확인한다. 설정이 맞다는 의미다.
2. `consistent_initialization`: **일관 초기화 후, 양의 시간 적분 전 t=0**라는 native 근거와 농도/재고/전위/전류를 읽는다. 첫 양의 시각0+를0으로 바꾸거나 외삽해 대체하지 않는다. 해당 상태를 못 얻으면 OPEN이다.
3. `completed_result`: 실제 시간벡터·guard·native 종료·전체 수지·외부 종료 예산을 읽는다. 사후 종료 성공으로 초기화 관측 누락을 덮지 않는다.

**[추론]** 유한 sigma와 전위차가 있으면 초기상태는 엄밀한 평형이 아니다. 모든 sigma의 농도·재고는 같게 두고 대수 전위는 달라질 수 있다. ground boundary1만0V 기준이며, 분리막 boundary2/3의 phis와 초기 I_leak는 실제 값을 보존한다. 이 둘의 전위차를 집전체 terminalV로 대체하지 않는다. 별도 초기화 solve가 필요하면 횟수와 시간 승인이 추가로 필요하다. 이를 runAll1회 안에 숨겨 승인한 것으로 쓰지 않는다. 근거: `reference/s0/notes/PHYSICS_CANDIDATE.md:32`, `:43`, Java `:460`, `:689`.

## 2. 설정과 실제 계수 소비

**[확인]** pcb1은 domain2, epsl=.45, epss=.55, NoCorr, user-defined `diag(sigma_short)`다. .55^1.5나 .45^1.5를 전자 전도에 또 곱하지 않는다. 전극은 fs가 epsl의 제곱식인 userdef이고, 전해질 fl/fDl/fmob는 N epsl^2.5, 분리막 epsl^1.5, P epsl^2.2로 설정된다. 근거: Java `:75`, `:98`, `:680`, `:682`.

| domain | epsl | fl=fDl=fmob 제안 기대값 |
|---|---:|---:|
| N1 | 0.285016227458136 | 0.04336845676771455 |
| 분리막2 | 0.45 | 0.30186917696247161 |
| P3 | 0.329399105824326 | 0.08689390504326667 |

**[추론·OPEN]** NoCorr의 전자 유효 sigma는 입력 sigma라는 설계 기대다. `D_e*fDl`과 저장항 epsl로 나눈 `D_dynamic`의 산술 후보는 JSON에 같이 적지만, 설치 생성식이 실제 어디서 어느 계수를 소비하는지 입증하지 않았다. 원소스의 `audit/featureInfo`는 API 형식 근거일 뿐 현재 출력은 반응 per1 위주다. pcb1 및 전체 전해질 생성식 관측을 했다고 쓰지 않는다. 계수별 `coefficient_symbol → generated equation/weak term → material/raw expression → evaluated SI value`를 해시와 함께 이어야 `ACTUAL_COEFFICIENT_EVALUATED`다. 변수/API 미확인은 null+OPEN이며 식별 문자열을 만들어 채우지 않는다. `COEFFICIENT_READBACK.json`은 네 증거 수준을 각각 분리한다.

분리막 보조 대조식 `j = sigma*(phis_boundary3−phis_boundary2)/Lsep`는 반응 없는 균일 전도 분리막의 구성식 검산이다. actual coefficient binding의 대체 증거가 아니며 실험 저항→sigma 역산 작업도 아니다. 계수 불일치면 STOP하고 임의 보정이나 epss 변경을 하지 않는다.

## 3. 전류·전하·Li 수지와 분해능

**[확인]** 원 출력 식은 `j=−intd2(liion.Isx)/Lsep`, `I=A_c*j`, `RN=intd1(liion.ivtot)`, `RP=intd3(liion.ivtot)`이다. `Isx`는 A/m², `ivtot`는 A/m³, RN/RP/j는 A/m², I는 A다. 모델 A_c=1m²와 재고 보정용 A_cell=1.53938cm²는 구분한다. 근거: Java `:448`–`:458`, `:624`.

**[유도]** 외부전류0·ground1·separator source 없음에서 기대는 `RN≈j`, `RP≈−j`이다. N 탈리튬과 P 삽입을 다음 식으로 연결한다.

`qN=F·[nN(0)−nN(t)]`, `qP=F·[nP(t)−nP(0)]`, `qI=∫j dt` [모두 C/m²].

총 전하[C]는 여기에 A_c를 곱한다. rest의 외부전하0으로 CE를 계산하지 않는다. 기존 LLI는 초기재고 감산이며 새 시간변화 LLI 생성항이 아니다. 원식 부호의 근거는 `reference/s0/notes/PHYSICS_CANDIDATE.md:28`–`:37`이고, 실제 finite sigma의 부호/연속성은 향후 관측 대상이다.

**[제안]** 점별 전류 잔차는 `1e−8 A/m² + 1e−4×max(|RN|,|RP|,|j|)` 이하다. near-zero j로 나누지 않는다. 전하 잔차 한도는 `2e−4 C/m² + 1e−4×전하최대절댓값`이다. 절대한도2e−4는 두 시각 재고 절대한도1e−9×F가 주는0.00019297066424 C/m²를 위로 반올림한 사전 제안이다. 상대1e−4는 새 consistency 배분안이며 결과에서 얻은 정확도 보증이 아니다.

**부호 deadband**는 전류1e−8 A/m², 누적/구간 전하2e−4 C/m²다. 이보다 양수면 기대방향 분해, 음수면 역방향, 밴드 안이면 `RESOLUTION_LIMITED`다. t=0의 q=0은 `NOT_APPLICABLE_AT_T0`다. near-zero의 반올림 수준 조성 증감을 엄격한 단조성 실패로 세지 않는다. 분해능 부족을 누설 없음 또는 수지 PASS로 바꾸지도 않는다. Li 수지는 별도로 확인한다.

**qI 적분**은 각 실행의 실제 저장 시각과 실제 Δt를 쓰는 복합 사다리꼴이다. full-grid와 매두번째점 grid의 차이는 진단 추정치이며 오차 상한이 아니다. 각 간격의 독립 곡률 상한이 있으면 `Σ M_i h_i³/12`의 상한을 사용할 수 있다. 별도 승인된 dense 대조는 같은 조건·창에서만 경험적 적분 오차를 평가한다. P0/P1의120초 대조를3600초 희소 출력의 적분 보증으로 쓰지 않는다. 유효한 오차 근거가 없으면 qN/qP가 맞아도 `INCONCLUSIVE_QUADRATURE`다. 전체 전하잔차 한도의1/4만 적분 오차 배분안이며, 검산은 `|qI−qN|+오차상한≤고정한도`다. 추정오차를 한도에 더해 실패를 PASS로 완화하지 않는다.

초기화·전류·inventory·quadrature·charge·방향분해능·native완료는 분리한다. 전압 예상치0.096/0.962/9.504mV를 수지나 초기값의 합격선으로 사용하지 않는다. 이번 정적 준비는 native PASS도 실험 타당성도 아니다.

## 최종 소비자 연결 정적 확인

`candidate/consumer.py.inactive.txt`의 초기화 비교는 이제 `POST_CONSISTENCY_BEFORE_POSITIVE_INTEGRATION`, 한 번 승인된 solve, 원자료 식별과 설치 mapping SHA를 요구한다. 이 메타데이터의 진실성과 해시 결속 검사는 아직 OPEN인 native adapter의 책임이다. ground0V에 쓰는 상대분모는1e−9V이며 상대한도1은 정규화 잔차한도이므로 절대≤1e−9V와 정확히 같은 조건이다. 다른 농도·재고 목표는50자리 문자열이고 Decimal50 정밀도에서 비교한다. float로 낮추어 준 객체는 소비자가 거부한다.

계수 JSON은 풍부한 설계명세이며 `verify_coefficient_evidence`의 `{configured,consumed}` 입력을 이미 만들어 놓은 파일이 아니다. `adapter_projection=null / OPEN`을 명시했다. 설치 생성식과 수치readback이 확보될 때 고정 mapping을 따로 검토·봉인해야 한다. 빈 consumed 집합을 실제 계수 증거로 허용하면 안 된다.

전하 소비자의 단일 `quadrature_bound_C_m2`는 **j, RN, −RP 세 적분의 모든 저장 prefix**에서 유효한 절대 오차상한이어야 한다. 종점만 또는 j만의 상한을 전체에 적용하지 않는다. 원시grid/각적분/범위/단위/산정근거/해시를 adapter에서 연결해야 하며, 숫자 한 개만 받은 경우 null로 처리해 INCONCLUSIVE를 남긴다. 수정된 소비자에는 `bound≤limit/4`, `|차이|+bound≤limit`, qN−qP 및 RN+RP 검사가 정적으로 보인다. 이것은 실제 함수 실행이나 반례 통과의 증거가 아니다.

산술 스크립트의 최초 실행 결과는 원래 도구 반환에 보존했다. 이후 계약의 adapter 설명·키명은 정적으로 보충했으며 작성 스크립트를 다시 실행하지 않았다. 마지막 산술 값 변경은 없다.
