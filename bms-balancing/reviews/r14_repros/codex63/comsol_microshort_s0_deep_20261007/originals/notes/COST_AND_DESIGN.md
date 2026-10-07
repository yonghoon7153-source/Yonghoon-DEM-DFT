# S0 비용·저장 정책·판정 설계 독립 메모

기준: 저장소 `fd7ce941a7c4d3989f80a133271189d67a6a0074`에서 부모 검토자가 보존한 `../sources/` 사본. 이 메모는 S0 정적 읽기와 아래 자체 산술만 사용했다. COMSOL/JVM/native 호출 0, 받은 Java/분석기 실행·import 0, MPH 열기·재평가·수정·삭제 0, 기존 수용 결과 재개방 0. 아래 “실측”은 원장에 인용된 당시 측정 기록이다. 이 검토자가 같은 작업을 다시 측정했다는 뜻이 아니다.

약어: SPEC=`../sources/COMSOL_REBUILD_SPEC.md`; READY=`../sources/NEXT_MODEL_READINESS_DECISION.md`; JAVA=`../sources/Normal480Candidate.java.txt`. 줄 번호는 이 사본 기준이다. 검토 범위는 SPEC §§4, 8-5, 10, 14, 19, 34, 37–42, 68–71 및 READY이다.

## 1. 먼저 고정할 결론

1. 현 정책의 병목은 요청 시각, 실제 solver step, 저장 해, CSV/콘솔 export의 네 층이다. `tout`만 바꿔도 최대 step 0.1 s와 촘촘한 strict 요청은 그대로 남는다. 저장 파일이 작아지는 것과 solve가 빨라지는 것을 분리해야 한다.
2. 1 h 후보의 full-field 요청 401개와 역사적 크기/상태 비율을 적용하면 MPH 약 0.521 GB다. 이는 해당 메시·필드·저장 인코딩 유지 조건부 산술이며 파일·RAM 상한이 아니다.
3. 기존 µV, 0.000345 mV, 0.308 mV는 다른 상태·구간의 설정 간 관측 차이다. 새 휴지의 최소 구별 신호나 참해 오차 한계로 재사용할 수 없다.
4. 좁은 storage-only 비교는 2회로 설계할 수 있다. 요청표와 cap까지 모두 분리해 바꾸려면 공통 기준을 재사용하여 총 4회가 최소인 직렬 비교안이다. 3회 안에 요청표와 cap을 동시에 바꾸면 결합 정책 시험이며 두 축 분리는 아니다. SPEC 2818은 “한 비교에서 두 정책을 동시에 바꾸지 않음”을 요구한다.
5. S1 전체를 바로 승인받기보다 S1-P 짧은 정책·초기화 확인과 S1-L 4점 사다리를 나눈다. 후속 단계의 실행 권한은 앞 단계 성공으로 자동 생성되지 않는다. SPEC 4175–4179에서 승인된 것은 S0뿐이다.

## 2. 실측 원장과 해석 범위

| 실행 | compile+batch / 부모 전체 | solver 시간 | 저장 시각 | 결과 MPH | 근거 |
|---|---:|---:|---:|---:|---|
| NORMAL30 | 1,570.079 / 1,653.199 s | 별도 표에서 670 s | 1,237 | 1,584,874,018 B | SPEC 2652, 3321, 3327 |
| NORMAL60 | 약 1,881 / 1,996 s | 779 s | 1,537 | 약 1.967 GB | SPEC 2945, 2981, 3050–3054 |
| NORMAL120 | 2,650.203 / 2,794.536 s | 여기 인용 표 미기재 | 2,140 | 2,734,001,003 B | SPEC 2976–2977, 2996–3002 |
| NORMAL240 | 4,059.516 / 4,269.865 s | 1,781 s | 3,340 | 4,261,090,658 B | SPEC 3085–3086, 3105–3111 |
| NORMAL480 | 6,500.453 / 6,829.015 s | 2,457 s | 5,740 | 7,315,279,360 B | SPEC 3168–3169, 3189–3195 |
| RTOL30 | 1,215.329 / 1,276.7889039 s | 428 s | 1,311 | 이 절 미기재 | SPEC 3321, 3327–3331 |
| B-min 150 s, 입자 640 | 부모 전체 4,471.8936425 s | 이 절 미기재 | 2,447 | 6,162,301,981 B | SPEC 4137–4142 |

시간들은 포함 범위가 다르다. solver, class, save, batch total, compile+batch, 부모 전체를 합산하면 중복한다. NORMAL480에서 적분은 2,457 s지만 compile+batch는 6,500.453 s였다. 저장/추출을 포함한 전체 비용을 적분 시간만으로 예측해서는 안 된다. RTOL30이 더 엄격한 허용오차로 더 빨랐다는 관측은 반복 성능시험이 아니므로 rtol 강화의 속도 효과가 아니다(SPEC 3327–3328).

RAM: SPEC 2619는 시작 시점 RAM 약 6.01 GiB와 디스크 143.86 GiB를 기록한다. 소비 peak가 아니다. SPEC 4115도 RAM은 시작 관측뿐이라고 한정한다. SPEC 2584, 2863, 2945는 기존 승인 범위에 없는 RAM 문턱·감시기를 임의로 발명하지 않도록 한다. 따라서 이 기록에서 “S1 메모리가 충분하다”, “필요 RAM은 6.01 GiB”를 도출할 수 없다. 새 S1 실행 명세에서는 시작 관측과 가능한 OS peak 관측의 구분 및 측정 주체를 적되, 미구현 감시기를 구현된 중단 조건처럼 쓰지 않는다.

역사적 정상 모델의 실제 메시 자유도는 물리300/입자320에서 79,485 + 내부12, 물리600/입자320에서158,325 + 내부12였다(SPEC 1306–1309). 현재 소스는 물리120/60/120 및 입자320/320이다(JAVA 660–674). 자유도만으로 sparse factorization, Java heap, 프로파일 문자열·BASE64 사본 및 해 저장의 peak RAM을 알 수 없다. JAVA 536–573은 시각×241좌표×8표현식을 `getData()`와 `String[][]`로 동시에 만들므로 export도 메모리 원인이다.

## 3. 재현 가능한 비용 산술

아래 코드는 이 검토에서 새로 쓴 독립 JavaScript 산술이다. 파일/모델/받은 프로그램을 열거나 호출하지 않으며 여기 적힌 원장 상수만 입력이다. IEEE-754 반올림은 제시 정밀도보다 작고, 주요 불확실성은 성능 외삽 자체다.

```javascript
const N240 = 3340, N480 = 5740;
const M240 = 4261090658, M480 = 7315279360;
const W240 = 4059.516, W480 = 6500.453;
const b = (M480-M240)/(N480-N240);
const a = M240-b*N240;
const oldPolicy = T => ({
  mphBytes: M480+(T-480)*10*b,
  compileBatchSeconds: W480+(T-480)*(W480-W240)/240
});
const solveSecondsPerInterval = 2457/(5740-1);
const NcapLower = 800+49+50+54+110;
const result = {
  incrementalBytesPerState:b,
  interceptBytes:a,
  mph401Bytes:a+b*401,
  mph1037Bytes:a+b*1037,
  old1h:oldPolicy(3600), old12h:oldPolicy(43200),
  solveSecondsPerInterval,
  oldCap01OneHourSolveSeconds:36000*solveSecondsPerInterval,
  relaxedCapIntervalLowerBound:NcapLower,
  relaxedCapAtOldAverageSolveSeconds:NcapLower*solveSecondsPerInterval,
  bytesPerStateObserved640:6162301981/2447
};
```

실행 출력:

```json
{
  "incrementalBytesPerState": 1272578.6258333332,
  "interceptBytes": 10678047.716667175,
  "mph401Bytes": 520982076.6758338,
  "mph1037Bytes": 1330342082.7058337,
  "old1h": {"mphBytes":47019732486,"compileBatchSeconds":38232.634000000005},
  "old12h": {"mphBytes":550960868316,"compileBatchSeconds":440987.23900000006},
  "solveSecondsPerInterval": 0.42812336644014637,
  "oldCap01OneHourSolveSeconds":15412.44119184527,
  "relaxedCapIntervalLowerBound":1063,
  "relaxedCapAtOldAverageSolveSeconds":455.0951385258756,
  "bytesPerStateObserved640":2518308.941969759
}
```

해석: 원 정책을 1 h로 늘리는 시나리오는 MPH 약47.020 GB/compile+batch10.62 h, 12 h는550.96 GB/122.50 h다. 모두 정상 충전 후기 증분을 휴지에 적용한 외삽이다. 특히 벽시계는 보증/상한/성능 모델이 아니다. SPEC 3216–3218의 9.5 h 외삽과 같은 계산법이며 이번 결과는 새 실행 관측이 아니다. 원장에는 단순 시간비례 비용을 안전 최대시간으로 격상하지 말라는 정정도 있다(SPEC 2810).

반대로 401 full-field 상태의 0.521 GB는 저장수에 대한 시나리오다. 모든 필드를 유지하고 320 메시를 쓸 때만 적용한다. 640 메시의 관측 평균2.518 MB/state를 단순 적용하면401상태가 약1.01 GB 규모지만, 이는 640 민감도 대안의 비교용일 뿐 peak RAM/실제 파일 크기 상한이 아니다. 결과 MPH 외 CSV·로그·BASE64 콘솔·패키지·보존 사본·임시 저장을 별도 예산에 넣어야 한다. 원본 MPH 삭제로 예산을 맞추는 계획은 금지다.

1063은 제안 cap들의 길이/상한 합에 따른 최소 구간 수이며, 초기1e-5 step, 적응 step, 실패 step, strict 시각에서의 추가 분할 때문에 실제 횟수는 더 크다. 455 s는 이 최소수에 과거 평균0.428 s/구간을 곱한 장난감 비용값이다. 이를 새 실행의 예상 완료시각으로 쓰지 않는다. 새 상태, 유한σ, 행렬 conditioning 및 solver 실패 때문에 구간당 비용도 바뀐다.

## 4. 저장 정책 두 대안과 권고

현 실제 설정은 `initialstepbdf=1e-5`, cap식 `if(t<0.1[s],0.000125[s],0.1[s])`, solver rtol1e-6, `tout=tsteps`, `tstepsstore=1`, `tstepsbdf=strict`다(JAVA398–407). study의 별도 rtol 문자열을 실효 solver 값과 혼동하지 않는다. 원장은 요청 시각과 실제 solver step이 다르다고 명시한다(SPEC331–335,477–479,2807).

| 대안 | 설정·장점 | 비용·제약 |
|---|---|---|
| A: strict + full-field 요청 시각 저장 | cap와 요청을 통제하고 각 비교 시각이 실제 step 끝점인지 로그로 확인. 동일 시각·좌표 비교가 쉬움 | 새 sparse 요청이 내부 적분 경로도 바꾸므로 정책 비교 필요. 처음에는 모든 종속변수 유지 |
| B: free + probes + 소수 full-field snapshot | adaptive step 자유도가 크고 scalar를 모든 accepted step에서 얻을 수 있음. 가장 큰 장기 절감 가능성 | 출력 시각 보간, probe 시각과 필드 시각 대응, guard 직전/직후 증거, restart 상태, 변수 보존 범위를 새로 확인해야 함. 기존 정확공통시각 계약보다 변경이 큼 |

첫 S1 권고는 A. B는 이론상 더 싸지만 최소 변경 목적에는 추가 추출 계약이 필요하다. 공식 설명은 `strict`가 요청 시각에 step을 끝내고 사이 step도 허용하며, `tout=tlist`가 출력 시각 저장 모드임을 구분한다. 정확 시각이 실제 step에 존재한다는 런타임 증거를 요구하고, `tout=tlist`라는 이름만으로 “보간 없음”을 선언하지 않는다. `tstepsclosest`는 근접 시각이므로 이번 비교의 대안으로 쓰지 않는다.

공식 COMSOL 6.3 근거: [Time API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html), [Time-Dependent Solver](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_solver.36.136.html). Probe와 저장 시간 감소의 일반적 대안은 [Reducing the Amount of Solution Data Stored in a Model](https://www.comsol.com/support/learning-center/article/reducing-the-amount-of-solution-data-stored-in-a-model-66461). 이 일반 문서의 “출력 감소가 해의 정확도에 영향 없음”을 strict 요청표까지 바꾸는 현 모델에 무조건 적용하지 않는다.

선택된 상태: xN=.445, xP=.5811516557009895, 균일 평형 OCV≈3.72372 V. 아래는 부모 축약 모형과 맞춘 S1 후보다. CDI 일관성 성공은 미입증이다.

요청 시각 T=3600 s: 역사적0–5 s 요청187개(초기107개 포함)를 유지하고 `5.5:0.5:30` 50개, `35:5:300` 54개, `330:30:3600`110개. 겹침 제거 후401개. 120 s prefix는255개다. pure log는 차분 창에 필요한 정확 시각을 빠뜨리고 초반 또는 후반이 빈약해질 수 있으므로 구간별 균등+초기밀집 표를 택했다. 휴지 t=0,300,900,1800,3600은 명시 포함한다.

cap 후보는 t<.1에서.000125 s, .1–5에서.1 s, 5–30에서.5 s, 30–300에서5 s, 300 이후30 s다. 이 표는 예상 빠른 모드와 관측 창을 고려한 제안이지 검증된 정확도 조건이 아니다. 120 s 정책시험은300 s 이후30 s cap을 검증하지 않는다. 후반 cap의 영향은 새3600 s 정상/유한σ matched control에서 측정해야 한다. 늦은 OCP 매듭 통과·반응 재분포가 나타나면 adaptive가 더 작은 step을 택할 수 있으며, cap30이 실제step30을 보장하지 않는다.

필드는 첫 시험에서 줄이지 않는다. phis,phil,cl, N/P 전체 입자 상태를 full-field 요청에 보존하면 새로운 국소 관측을 나중에 정의할 여지가 남는다. scalar401행에는 V, 분리막 전위차, I_leak, 반응전류, Li_N/P/e, 총Li, 평균x, 표면극값,cl극값, guard, 전압분해를 유지한다. 상세241좌표 프로파일은 사전 고정9시각(0,1,5,30,120,300,900,1800,3600)×2전극이면4338행이다. 모든401시각 프로파일을 유지하면193282행이며, 이것도 NORMAL480의2766680행보다 작다. 선택 프로파일로 줄여도 guard scalar의 전시각 보존은 줄이지 않는다. 어떤 축을 구현했는지는 후보 diff/실행 readback에 따로 기록한다.

## 5. 최소 정책 동등성 시험과 단계별 권한

즉시 다음 승인 대상은 후보의 오프라인 구현·변경부 한정 검증이다. 아래 native 계획은 그 검토·수용을 거친 뒤의 선택안이다. S1-P, S1-L, 추가 수치 controls는 각각 별도 승인 단위이며 일괄 실행 패키지가 아니다.

S1-P는 과거 NORMAL480/rtol30/B-min 수용을 다시 여는 시험이 아니다. 새 xN=.445 휴지 조건과 유한σ1.7e-6의 정책 변화만 묻는다. 동일한 조성·초기재고·전류0·σ·물성·OCP·메시·초기 step·초기화·허용오차·guard를 모든 비교에 고정한다. 각 실행은 fresh 0→120 s이고 저장 해 restart는 별도 경로로 섞지 않는다.

| run | 요청 | 저장 | cap | 직전 run과 비교하는 축 |
|---|---|---|---|---|
| P0 | 원0–120 s dense 목록1337개 | all accepted | 원cap | 새 휴지/유한σ 기준 |
| P1 | P0 동일 | 요청목록만 | P0 동일 | 저장 방식만; P0/P1이 최소 storage-only 2회 |
| P2 | sparse prefix255개 | 요청목록만 | P1 동일 | 요청표만; sparse는dense의부분집합 |
| P3 | P2 동일 | P2 동일 | 제안cap | cap만; 초기·후기 적용 실제 구간 확인 |

A1: 두 번만 허용하는 경우 P0/P1까지만 시행하고 storage-only 범위에서 닫는다. 원cap/요청으로 장기 ladder를 자동 시작하지 않는다. A2: 비용 축 전체를 좁게 확인하려면 P0→P1→P2→P3 최대4회. 세 번으로 P2/P3를 결합하면 결합 정책 변화의 관측만 얻으며 SPEC2818의 분리 조건을 충족하지 않는다. 최소 native 수를 숨기지 않는 것이 중요하다. 각 단계는 실패·미완이면 중지, 자동 재시도0, 실행 범위 증가0이다.

검사 시각은 sparse255개를 공통 사전 목록으로 고정한다. temporal interpolation/최근접 대체 없이 실제 저장 시각을 매칭하고 전극별241좌표를 sample index로 비교한다. 기본 무결성은 기존 ΔV≤1 mV, Δx_surface≤1e-4, 총Li상대변화≤1e-6, 전압분해잔차≤1e-8 V를 유지한다(SPEC3176). 그러나 약96 µV의1 h 예측을 읽으려면1 mV만 통과해서는 안 된다. 추가 신호 해상도 후보로 max|δV|≤10 µV와 endpoint-drift discrepancy≤10 µV를 사전 고정한다. 이것은 설계 목표이며 기존 수용기준/참값오차인증선을 바꾸지 않는다. 새 목표 미달이면 약한 rung 판정을 INCONCLUSIVE로 남긴다. 누설전류와 Li이동의 부호/적분 수지는 추가로 필수이며 관측값을 보고 허용치를 늘리지 않는다.

예산은 실측 예측과 분리한 제안 상한이다:

| 승인 단위 | 최대 횟수 | 실행당 제안 부모 벽시계 cap / 신규 디스크 증가 cap | 단계 합계 상한 | 해석 |
|---|---:|---:|---:|---|
| S1-P 저장·요청·cap qualification | 4 | 2 h / 6 GB | 8 h / 24 GB | 정상120의부모46.6분과MPH2.734GB에여유를둔값. 새휴지성공보장아님 |
| S1-L 사다리 | 4 | 2 h / 6 GB | 8 h / 24 GB | σ=1e-20,1.7e-8,1.7e-7,1.7e-6. P실측확인후별도승인 |
| S1-C 표적후반시간민감도 | 2 | 2 h / 6 GB | 4 h / 12 GB | 정상+사전선택경계σ의같은3600s조건에서cap만반감. rtol/mesh까지동시에바꾸지않음 |

P0/P1까지만 선택하면 첫 native 승인 단위는2회/4 h/12 GB다. 표의 S1-C 2회는 특정σ의 시간축 한 가지를 묻는 선택안일 뿐 전체 ladder의 수치 확인이 끝나는 횟수가 아니다. 모든 rung에 같은σ의 시간·공간 matched controls를 요구하면 추가 횟수가 필요하며 새 범위를 별도로 제안해야 한다. 현재 자료로 그 controls를 생략하고 확정 판정으로 올리지 않는다.

S1-L의2 h/6 GB는 compact 저장 성공을 조건으로 한 실행당 중단예산이며, 완료를 예견한 보증이 아니다. P의 실제 비용/상태수/파일증가가 상한에 맞지 않으면 L 상한을 자동 늘리지 않고 재제안한다. 실행기기의 시작 여유는 승인된 한 단계의 누적 증가와 포장·임시 저장 여유를 더해 확인한다. 기존50 GiB/20 GiB 조건을 자동 복사하지 않는다.

사후 분석·수신 검토까지 자동으로 full-field MPH를 재개방할 권한을 뜻하지 않는다. S1에서 새로 만들어 전송하는 scalar/프로파일만으로 필요한 판정을 할 수 있게 추출 계약을 고정한다. 이 S0에서 소스 읽기 외 실행은 없었다.

## 6. 수치 기준선과 결과 전 판정 규칙

SPEC3393–3401의 정정을 그대로 적용한다. rtol30 최대2.3812821772 µV(3317–3319), B-min120–150 s0.3449917063 µV와 이른.0005 s308.1961318368 µV(4139–4145)는 해당 상태/관측량/설정 쌍의 차이다. 새휴지의 noise floor, 오차상한, confidence interval로 쓰지 않는다. 총Li 보존도 시간/공간 정확도의 대체 검사가 아니다(SPEC334–335,488–489).

사전 고정 관측량:

- `V(t)=phis(boundary4)-phis(boundary1)`.
- `D_sigma(t)=[V_sigma(t)-V_sigma(300)]-[V_0(t)-V_0(300)]`. 정상 자체의 relaxation drift를 빼고 CDI의 t=0 전위 jump를 자가방전 변화량으로 세지 않는다. 300 s를 빼는 대신 초기0–300 s와0→3600전체 변화는 별도 보조항으로 그대로 보고한다.
- `S_sigma=OLS_slope(V_sigma−V_0; t=1800:30:3600)`. 61공통점의 절편 포함 선형회귀를 사용, 중앙차분/후방차분/가변창을 결과 뒤 바꾸지 않는다. secant는정확1800,3600쌍으로보조보고한다. 끝점에서가상외삽·zero padding을하지않는다.
- 직접 전자누설 `j_leak=-intd2(liion.Isx)/L_sep`(JAVA439–441), `I_leak=A_c*j_leak`. 1D길이적분만한값은전류가아니므로 L_sep로평균하고면적을곱하는단위를유지한다. Java에서이미있는관측량이다.
- 전극별 `Li_N/P=intd(epss*cs_average)`와 `Li_e=sum intd(epsl*cl)`(JAVA436–440), 누적누설 `q_leak=∫j_leak dt`, 전극별reaction적분, 외부전류0. 입자평균/표면차는같은좌표에서만정의한다(SPEC2805).

추천판정은 “테스트한 설정들 사이에서 휴지 대비가 유지되는가”다. 관측량Y의matched control이있으면 `B_Y=max_k |Y_sigma,k−Y_sigma,base|`로정의하되여기서Y는정상차감한D또는S이다. 두run의개별차를합산하는상한형보조값도함께보고한다. 이는검사한설정집합의경험적spread이며참값오차상한이아니다. multiplier5는설계분리계수이며통계적5σ가아니다.

예시사전실용한도는 endpoint drift `δV_design=0.1 mV`, late slope `δS_design=0.05 µV/s`다. 실험계측기의해상도에서온값이아니라이번모델연구의운영분류선이다. 이를선택하면약0.096 mV의전체1 h예측을가진가장약한점은애초경계이하후보다. t=300기준D는전체1 h예측보다작으므로반드시해당창의사전예측과비교한다.

| 분류 | 정확한조건후보 |
|---|---|
| `DISTINGUISHABLE_AT_REST` | 유효성검사완료,같은σ/정상matched control완료, D(3600)<−max(δV_design,5B_D), S<−max(δS_design,5B_S),예측한방향의Li_N감소·Li_P증가및q_leak수지정합. 어떤수치축을검사했는지명시 |
| `NOT_DISTINGUISHABLE_WITHIN_T` | 필수출력/유효성/해당matched control완료,|D(3600)|≤max(δV_design,5B_D)이고|S|≤max(δS_design,5B_S). 해당상태·T·설정·분류선내결과일뿐누설없음이아님 |
| `INCONCLUSIVE` | guard/solver/예산/출력누락/상태비대응,matched control부재,일부지표만분리,부호불일치,또는기준선이신호크기와비슷해미검사축이판정을바꿀수있는상태 |

전체ladder4회만으로모든σ의독립수치오차한계를얻을수없다. 가장약한경계σ+정상2개의후반시간control은그σ의cap민감도만묻는다. 더큰σ의B값으로이전하거나공간오차증거로승격하지않는다. 4점screening뒤필요한σ에만새축추가를별도결정하는방식이최소비용이다. 공간·rtol을아예검사하지않은분류에절대정확도나“전체수렴”을붙이지않는다. 더강한certification이목적이면같은rest/σ에서입자640과rtol1e-7을축별로추가해야하고이번lean count에는포함되지않는다.

## 7. 실패 모드·중단 조건

| 실패 | 사전읽기/감지 | 중단·판정 |
|---|---|---|
| CDI/초기일관성실패 | 전류0의ecd1,접지,재고를고정;uniform농도설정과반환t=0분리. 유한σ에서는전위와BV반응이동시에일관적이어야함 | 첫실패그대로보존,전위offset/초기Li/σ를자동조정하거나자동retry하지않음 |
| OCP표밖 | N/P표면범위와각OCP보간함수extrap=none. 최초상태와예측최대경로대조 | named OCP guard발동이면INCOMPLETE_RANGE_STOP; 외삽허용으로완주만들지않음 |
| 전해질농도≤0 | 현행JAVA390,409–423에threshold0실시간guard확인. READY72의“미구현”은9월15일당시의기록 | namedguard중단,원인/직전직후저장. accepted step후샘플링이지Newton trial/연속양수성증명이아님 |
| 고체내부농도이상 | 현guard는표면뿐. READY73에서추가차원전반극값검사미완 | surfaceguard통과로내부보호완료주장금지. 새기능추가시별도변경검증;필수전내부관측불가하면범위제한명시 |
| 작은step·NLfail/Tfail누적 | 실제accepted/rejected step,최대·최소step,구간별wall시간기록 | 실패횟수0이과학합격조건은아님. wall/diskcap또는solverfailure에정지. 임의Tfail숫자를새물리경계로쓰지않음 |
| 계산/디스크예산초과 | 시작여유및승인된cap,run단일소유권,기존파일충돌검사 | 예산중단은물리완주로승격불가;nooverwrite/noretry/기존MPH삭제없음 |
| 부호·수지·단위불일치 | leak양의왼쪽방향↔N산화/P환원,면적1m²,Li이동,외부전류0교차대조 | 신호가있어도INCONCLUSIVE; 새sigma재맞춤없이식/추출정의검토 |
| 저장정책증거누락 | 요청표·실제step·저장표·timeinterp·stop전후상태readback | nearesttime/재보간으로빈행메우지않음;출력증거미완으로종료 |

유한σ가step을얼마나작게만드는지는관측없음이다. 약한누설의새느린자가방전시간상수만으로더빠른물리모드가반드시생기는것은아니지만,algebraic전도행렬conditioning·초기BV반응·OCP선형매듭·농도구배로Newton/적응step이변할수있다. 따라서“강성이몇배증가한다”는숫자는사전예측불가다. 비용시나리오에1/3/10배accepted work를넣는것은불확도탐색용일뿐확률구간이아니다.

## 8. 자기 반박과 S1을 보류할 이유

1. **초기화변화가누설로보일수있다.** 전류0의uniform농도는finiteσ평형이아니다. 사전CDI전위값을정상과억지로같게만들지말고,농도/재고의같은이력만고정하며초기jump와late drift를분리한다.
2. **10 µV정책목표를통과해도96 µV대비의참오차는알수없다.** matched control은검사설정간spread일뿐이다. 새rest상태의공간/허용오차미검사에맞춘제한분류가필요하다.
3. **401저장시각이짧은OCP매듭사건을놓칠수있다.** strict와adaptive/guard를유지하고late cap반감control을한다. 새실제step로그를보고사후창을고르는것은탐색분석으로따로표시한다.
4. **0.521 GB예측이맞아도실행중RAM또는export복사량은커질수있다.** P에서실측단계를별도로보고하고본사다리예산을새로고정한다. 현재자료로RAM적합성결론을내리지않는다.
5. **동일1D균질모델에서누설전류를검출해도현실microshort판별력은생기지않는다.** 열·국소SOC·경로성장없고실험상태도미대응이다. 현재S1은모델내해석가설을검사하는값이있지만실험진단알고리즘검증이목적이면지금시작할이유가약하다.

S1을하지않을합리적사유는(가)사용자목표가실험셀의정량검출한계인경우,(나)CDI/누설수지확인전에4점모두를성급히계산하는경우,(다)storage-only결과없이기존0.1 s정책으로수시간을연장하는경우다. 축약모형만으로는명목누설과가역Li이동의방향/규모를이미예측할수있고,COMSOL의추가정보는전극분포·과전압·완화와누설의상호작용·수치구별가능성에있다. 이추가질문을판정관측량으로고정한후짧은S1-P부터가는것을권고한다.
