# S1-O 정책·동일 σ 대조 K·비용 계약

2026-10-07. 작성 대상은 오프라인 계약이다. 후보·받은 프로그램을 실행/import하지 않았으며 합성 시험·COMSOL·JVM·컴파일은 0회다. `analysis/build_policy_design.py`는 이 작업에서 새로 작성한 텍스트·Decimal·해시·JSON 생성기이며, 기존 Java는 문자열로만 읽었다. 이 자체 정적 스크립트의 실행은 기능 검증이 아니다.

판정의 기준은 S0 최종 `S0_REPORT_KO.md`와 `DECISION.json`이다. S0 보조 메모에는 초기 기준을 300초로 잡고 부호를 반대로 쓰는 대안도 있지만, 채택한 식은 최종 보고서의 **t=0 기준, 양의 D=추가 전압 하강, 2700–3600초 할선**이다. 이 차이를 숨기고 메모의 식을 혼용하지 않는다. [확인: `reference/s0/S0_REPORT_KO.md:188`, `:206`; `reference/s0/notes/COST_AND_DESIGN.md:146`의 대안]

## 4. P0–P3는 4개의 새 120초 문제로 분리한다

고정 초기 농도/재고, 외부전류 0, σ=1.7e−6 S/m, fresh 0→120초, 입자320/320·물리120/60/120, rtol1e−6, 초기step1e−5, 기존 OCP·guard·허용치는 네 변형에서 같다. near-zero는 무열화 셀을 뜻하지 않으며 기존 LAM/LLI도 바꾸지 않는다. Study의 rtol 문자열1e−5와 실제 Time solver1e−6을 구별한다. [확인: `reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt:409`, `:643`, `:696`, `:708`, `:718`]

| 변형 | 요청 시각 | 저장 정책 | cap | 직전 변형과의 유일한 정책 차이 |
|---|---|---|---|---|
| P0 | 원 dense 0–120초, 1337개 | `tout=tsteps`, 모든 accepted 상태 | `<.1초 .000125초, 이후 .1초` | 새 휴지·유한σ 기준 |
| P1 | P0 그대로 | `tout=tlist`, 요청+필수 사건 상태 | P0 그대로 | 저장 |
| P2 | S0 sparse 0–120초, 255개 | P1과 같음 | P1과 같음 | 요청 목록 |
| P3 | P2 그대로 | P2와 같음 | `.000125/.1/.5/5/30초` 구간식 | cap |

P3의 cap 구간은 `<.1`, `.1–5`, `5–30`, `30–300`, `≥300초`다. 120초 pilot은 마지막 구간을 실행하지 않는다. `POLICY_VARIANTS.json`에 1337/255/401개 시각을 **문자열 원 토큰**으로 전부 넣었고, `literal_patch_table_from_S0`에 상한·σ·tlist·tout·cap 및 식별 변경을 열거했다. 요청의 순서·중복 없음과 255개가 1337개의 정확한 부분집합임을 새 정적 산술로 확인했다. 후보를 실행한 검증은 아니다. [확인: `analysis/POLICY_DESIGN_STATIC_OUTPUT.json`; 계약 `request_vectors`, `literal_patch_table_from_S0`]

비교는 P0/P1, P1/P2, P2/P3 각각에서 공통255시각×N/P241좌표를 사용한다. 이와 별개로 P0/P1의 자체1337요청, P2/P3의 자체255요청이 모두 저장됐는지 검사한다. 실제 전체 저장 교집합과 계약상 비교 부분집합을 따로 출력한다. 전체 저장 수를255/1337로 강제하지 않으며 보호중단 전후 추가 상태도 남긴다. `strict+tlist` 이름만으로 무보간을 단정하지 않고 실제 accepted endpoint와 저장 시각 대응이 없으면 시간 증거는 OPEN이다. 빈집합·t=0만·누락·중복·최근접 대체를 완료로 수용하지 않는다. [제안: `contracts/POLICY_VARIANTS.json:2252` 이후]

P의 호환성 문턱은 max|ΔV|≤1mV, max|Δx_surface|≤1e−4, 각 실행 총Li 상대drift≤1e−6, 쌍별 총Li 차/초기재고≤1e−6, 각 전압 항등식 잔차≤1e−8V다. 수치 비교 초과와 native 실패는 별도 축이며, 비교 초과가 나와도 정상 종료 증거를 오류로 바꾸지 않는다. 다만 정책 qualification은 미완으로 남겨 다음 P로 자동 진행하지 않는다. 보조 10µV 목표는 약한 신호에 필요한 해상도 진단이고 기존 1mV를 몰래 교체하는 새 PASS 기준이 아니다. [확인된 기존 문턱: `reference/s0/S0_REPORT_KO.md:239`; 제안: 계약 `consumer_contract`]

**300초 이후 cap 공백은 P에 5번째 실행을 숨겨 메우지 않는다.** P4회 후 K를 고정하고, 별도 승인한 full 0–3600초의 baseline near-zero/high와 cap반감 near-zero/high를 먼저 실시하도록 제안한다. 이는 아래 M4/N16 중 이미 세어 놓은 4회다. 2700–3600초 D/S와 실제 accepted dt를 직접 대조하기 전에는 후기 cap 미확인을 유지한다. 짧은 300–360초 확인을 2700–3600초 기울기 증거로 쓰지 않는다. 이 full-window 대조 역시 아직 실행·승인되지 않았다.

## 5. K는 동일 σ와 동일 설정의 near-zero 쌍을 포함한다

권고안은 네 축을 따로 바꾸고, 각 축에서 near-zero+세 유한σ를 모두 갖추는 **완전한 등록 집합**이다. 값과 창을 P 비용 검토 후, M 결과를 보기 전에 고정한다. 결괏값이 유리한 σ만 골라 대조하는 방식은 허용하지 않는다. [확인: `reference/s0/S0_REPORT_KO.md:210`, `:212`; 제안: `contracts/K_DESIGN.json`]

| K 축 | baseline → 대조 | 유지하는 다른 설정 | 새 실행 |
|---|---|---|---:|
| rtol | Time 1e−6 → 1e−7 | cap·초기step·scaled/factor·두 mesh·요청/저장 | 4 |
| cap | S0 제안 구간식 → 각 구간 상한1/2 | rtol·초기step·mesh·요청/저장 | 4 |
| 입자 | 320/320 → 640/640 | 물리mesh·rtol·cap·요청/저장 | 4 |
| 물리mesh | 120/60/120 → 240/120/240 | 입자mesh·rtol·cap·요청/저장 | 4 |

각 행의 σ는 1e−20,1.7e−8,1.7e−7,1.7e−6 S/m이며 모두 fresh0–3600초·401요청이다. M baseline4회+N16회=**고유20회**, 앞선 P4회까지 포함하면 **총24회 제안**이다. 기준near-zero 한 번은 M의 세 유한σ·네 축에 공유하지만, N의 near-zero는 해당 축 내에서만 공유한다. 다른 축의 near-zero로 D_k를 계산하지 않는다. P3 120초는 M의3600초 기준이 아니며, 과거 NORMAL480·rtol30·B-min은 초기조건·전류가 달라 재사용하지 않는다. [정적 산술: `analysis/POLICY_DESIGN_STATIC_OUTPUT.json`; 명시한20개 run: `contracts/K_DESIGN.json`의 `run_inventory`]

순서는 P0→P1→P2→P3의 각 수용, 비용검토 및 K 고정, `M_BASE_Z`, `M_BASE_H`, `N_CAP_Z`, `N_CAP_H`의 full-window 수용, 나머지 baseline과 대조다. 이는 네 개를 일괄 시작하라는 명령이 아니다. 각 실행은 별도 고정 승인과 결과 검토를 전제로 한다. 후기 cap쌍 결과 때문에 사다리σ·OCP·초기값·판정식을 바꾸지 않는다.

`Dσ(t)=[VZ(t)−VZ(0)]−[Vσ(t)−Vσ(0)]`, `Sσ=[Dσ(3600)−Dσ(2700)]×3600/900 [V/h]`다. 각 축의 D/S에는 **그 축의 Z**를 사용한다. `ED=max_k|Dk−Dbase|`, `ES=max_k|Sk−Sbase|`를 해당σ에서 계산한다. 5배는 통계적5σ가 아니다. `δD=1mV`, `δS=1mV/h`를 유지하며 기존 S0의 세 분류를 그대로 쓴다. K가 없거나 일부 축을 버렸을 때 ED/ES를0으로 채우지 않는다.

cap 변경이 실제 accepted dt를 바꾸었는지도 구간별로 확인한다. baseline부터 모든 dt가 half-cap 이하라면 그 cap 대조는 비활성/제한적 도달로 보고한다. 설정차를 읽었다는 이유만으로 더 촘촘한 적분을 수행했다고 쓰지 않는다. D/S 설정 민감도 관측값은 남기되 후기시간해상도 blanket qualification은 별도 근거가 없으면 OPEN이다. accepted step와 Tfail/NLfail·재시도 기록은 서로 다른 양이다.

24회×9000초의 명목 상한은216000초=60시간이다. 이는 사용자가 지금60시간 실행을 승인했다는 뜻도, 완료 예측도 아니다. 비용을 줄이려면 M 결과 전에 K 범위를 명시적으로 줄여 동결하고 빠진 축·σ의 결론을 INCONCLUSIVE로 남긴다. 예컨대 P4+M_Z/H2+N_CAP_Z/H2의8회만 수행하면 highσ cap 비교만 얻고 rtol/공간/약한 두σ와 전체 등록분류는 미완이다. 기존 자료를 억지로 대조로 채워 실행 수만 낮추지 않는다.

## 8. 저장·후처리까지 관측한 뒤 비용을 다시 승인한다

기존 NORMAL120/240/480의 compile+batch는 각각2650.203/4059.516/6500.453초, 저장 상태2140/3340/5740, MPH2,734,001,003/4,261,090,658/7,315,279,360 bytes다. 마지막 값은 이 전달 S0 원장에 인용된 식별이다. 다른 전달문에서 인용한 근사7.315GB와 혼용해 실제파일 재측정을 주장하지 않는다. [확인: `reference/s0/notes/COST_AND_DESIGN.md:16`; `reference/s0/S0_REPORT_KO.md:243`]

두 점의 bytes/state 모델은401상태 MPH 약520,982,077bytes를 준다. full401시각의 N/P241좌표는193282행이다. 이는 동일필드/encoding 가정의 산술이며 RAM이나 출력 상한이 아니다. 입자640 기록의 단순 bytes/state를 쓰면401상태가 약1.01GB이지만, sparse변형에서 실제메모리가 충분하다는 근거가 아니다. [산술: `contracts/COST_MODEL.json`의 `storage_scenario`]

P에서 compile, batch, 초기화, solver, save/export, 분석, 포장, 부모전체를 나누어 기록한다. solver는 batch에 포함되므로 더하지 않는다. 분리계측이 없으면 save/export 잔차를 추정값으로 표시하고 정밀한 phase실측으로 만들지 않는다. 실제 accepted dt·실패step·저장/요청 수·MPH·CSV·BASE64·임시사본, sampled RSS/privatecommit 최고·OS peak가능여부·가용commit/RAM/disk최저도 함께 기록한다. sampled최고는 OSpeak나 강제cap과 같지 않다. 읽기오류/표본틈은0/PASS가 아니다.

새 예산 초안은 적용 가능한 phase 시나리오 최대치에1.5배+300초의 여유를 두고60초단위로 올리는 식을 제안한다. step1/3/10배 시나리오는 확률구간이 아니다. 필요한 상한이 현 native7200/전체9000초 제안을 넘으면 사용자에게 새 고정 예산을 요청하며 자동 확대하지 않는다. 분석·포장은 bytes/rows 처리량과2배여유를 별도로 쓰고, cleanup·최종기록 시간을 합계 안에 예약한다. 다른σ·mesh·후기구간의 비용은 P120에서 실측한 것이 아니므로 첫3600쌍 뒤 미래예산만 갱신한다. 주 결과를 보고 K축을 유리하게 바꾸는 근거로 쓰지 않는다. [제안: `contracts/COST_MODEL.json:78`]

S0의 실행당 native7200/전체9000초·출력6GiB·시작16GiB는 미승인 계획값이다. 실제 감시·누적예약·중단 가능성을 담은 `RESOURCE_CONTRACT.json`이 이를 충족해야 한다. 기존MPH를 지워 공간을 맞추지 않는다. CPU이용률/메모리peak/미래완료시간은 미확인이다. P 비용과 자원 경로가 미완이면 현재값을 채택된 native예산으로 승격하지 않는다.

## 자기 점검과 승인 전 잔여

실행됐어도 판정하기 어려운 가장 그럴듯한 경우는 세 가지다. 첫째, tlist라는 설정만 기록하고 보간/누락된 결과를 비교하는 경우로, 요청·accepted·stored의 정확 대응과 자체요청 완전성이 차단한다. 둘째, 유한σ초기화가 재고를 바꾸거나 전위초기점프를 방전으로 세는 경우로, 세 단계readback·같은초기재고·paired증분이 차단한다. 셋째, P120만 통과하고 후기/약한신호를 수렴됐다고 부르는 경우로, full3600 K와 동일축near-zero·미완INCONCLUSIVE가 차단한다.

S0 예측0.096248/0.962366/9.503694mV는 **평균조성으로 계산한 평형 OCV하강**이다. 같은 OCP를 전극별 정확입자/전극평균x에 적용한 OCV, 실제단자V의 자체변화, paired D, 초기전위차, lateS·ED/ES를 다른 열로 나란히 낸다. 평균OCV는 표면극값의 산술평균이 아니다. 예측과의 불일치가 있으면 초기분극·비균일성·모형가정의 차이로 조사할 질문으로 남기고 σ/OCP를 맞추지 않는다. [확인: `reference/s0/S0_REPORT_KO.md:139`; 제안: `contracts/COST_MODEL.json:112`]

다음 승인 전에 필요한 것은 P0–P3 실제source materialization의 허용diff·설정/시각/초기화 증거adapter, 변경부 검증 수용, 현재경로/엔진/정책확인, 자원감시의 실제지원 및 상한, pilot비용과 K범위 동결이다. 이번 JSON과문서의완료는 native-ready가 아니다. 모든 P/M/N승인·run·release는 비활성이고, 전체/정상gate INCOMPLETE·실효정책/실제코어 UNVERIFIED·OCP외삽금지·기존실패는 유지한다.
