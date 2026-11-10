# D-3/P2 native ULPR·판 분리 소비 — 합성 후보

**작성 측 최종 합성 시험 29/29, 보호 조건 약화 대조 7/7 검출을 완료했다. 실제 P2/T12 자격·등록·운영 GO는 0건이며 전체 HOLD다.** 바탕은 S0 `f4647f2b7c218a6df7def3292c092273f9d4e35f`다. 28개 시험과 스텁을 먼저 작성하고 시험 준비 오류를 고친 error-free red2 뒤에 구현했다. 첫 구현 뒤 언로딩 교차 범위를 좁히는 29번째 반례도 수정 전 실패를 확인했다. 전체 순서·시험 SHA는 §7과 `verification_summary.json`에 분리 기록한다.

## 1. 근거와 의존

| 항목 | 고정 근거·절 | 이번 해석 |
|---|---|---|
| 정본 | 읽은 LIVE 트리 `63a513560c2770990920065be94ef966a8be018b:docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §2-6·§2-7·§12 | h0 비례 언로딩, primary/trajectory 분리, 둘째 유효 0창 끝에 분리 선언, 그 뒤 판을 치우고 4창 유지 |
| 준비 소비 계약 | 같은 트리 `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §4·§4.1·§4.2 | native P2 params/header, 같은 S0 신원·이력·재고, 물리시간·중력·단위 명시. 실제 선택/자격은 별도 |
| LIVE | `dem_gen2_live_contract.diagnose_live_ra` | 원 입력을 S0 decoder가 재검증. status 문자열이나 hash 하나만 받지 않음 |
| S0 | `dem_gen2_s0_contract.decode_s0(data, contract, live_plan, servo_frames, ra_frames)` | 고정 S0 `f4647f2b7c218a6df7def3292c092273f9d4e35f`의 API와 소스 바이트를 사용. 기존 S0 실제 자격은 NOT_RUN 유지 |
| P1 역사 | 고정 P1 계약 `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` | native P2 지원이라고 부르지 않음. P1 parser/source를 호출하거나 수정하지 않음 |
| 닫힌 결함 | ULPRI·T12R 한정 종결 | 재개방·기존 결함 수 추가 없음. 이번 새 계약은 실제 hidden history/T12 자격을 대체하지 않음 |

S0 fixture는 `test_dem_gen2_s0_contract.fixture(wall_profile='WALL_U', grid_choice='coarse')`의 가상 trace와 6개 합성 payload를 사용한다. 반환은 `(contract,envelope,live_plan,servo,ra)`다. 첫 red 전에 S0 placeholder를 위 고정 핀으로 교체했다. 원 S0 fixture/API는 수정하지 않았다. 이번 호출은 새 P2 연결에 필요한 작은 합성 대조이며 기존 S0 전체 suite를 다시 실행한 것이 아니다.

## 2. 두 권고안 전제와 범위

| 전제 | 권고 한 줄 | 하지 않는 것 |
|---|---|---|
| 권고안 전제(Q-P2-1) | native P2 typed header/params와 원 S0 bytes·S0/LIVE 입력을 재검증하고 h0·A/B 비례·물리시간·중력·단위의 명시 사상을 묶음 | P1 r8 자동 변환·이름 기반 중력 분기·실제 A/B/정량 선택·원천 진위 인증 |
| 권고안 전제(Q-P2-2) | 같은 attempt/S0 재고의 완전한 2개 연속 무접촉 창 뒤 MOVE_CLEAR 진단 사건, 그 뒤 정확 4개 유효 창을 소비 | 실제 판 이동/메시 삭제·첫 압력 교차의 자동 primary 선정·연구/운영 GO |

정본은 분리 뒤 판을 위로 치우며 메시 삭제는 선택이다. 이번 좁은 후보는 **MOVE_CLEAR 사건만** 표현하고 DELETE_MESH는 미지원으로 거부한다. 실제 메시·wall fix·이력을 변경하지 않는다. 실제 A/B·h0·단위·중력·창·압력/KE/표면 문턱·선정 규칙은 모두 `null`/미승인으로 남긴다. 실제 D9′ ε_sphere 보정 정책은 이 toy 입력과 별개이며 재질문하지 않는다.

## 3. 제안 API와 형식

```python
validate_p2_contract(plan, s0_bytes, context) -> report
diagnose_p2_separation(plan, s0_bytes, context, trace) -> report
```

첫 함수는 native 구조·선언/바이트/사상 일관성만 반환하고, 두 번째는 첫 검증을 새로 수행한 뒤 trace를 진단한다. caller가 제공한 compiled/status 보고서를 원 입력 대신 받지 않는다. 입력은 exact built-in 자료로 제한하고 key 타입을 hash/set/equality 전에 검사한다. API는 파일·환경·호스트·실제 P1 consumer·engine에 접근하지 않는다.

### native plan/header

최상위는 `DEM_GEN2_P2_NATIVE_SYNTHETIC_PLAN_V1`, `purpose=SYNTHETIC_PREPARATION`, `protocol=P2`, Q-P2 전제, plan ID/판, S0 boundary의 전체 identity, header, params다. header는 `P2_NATIVE_ACTIVE_HEADER_V1`, profile `P2_NATIVE_ULPR_V1`, 정해진 7개 native active definition, producer/consumer-definition/S0-contract 핀, S0 SHA, params SHA, atom16/pair/wall의 source mapping 신원을 갖는다. 옛 r8 머리 또는 P1 params의 bed 이름만 바꾸면 정확 스키마/definition과 맞지 않는다.

핀은 선언 일관성용이며 remote 소속·실제 사용·빌드 진위를 인증하지 않는다. P2 source mapping은 S0의 명시된 합성 reference SHA와 대조하며 실제 물리 semantic mapping이 승인됐다고 주장하지 않는다. fixture의 `declared_unit_*`/`declared_slot_*`는 의도한 가짜 사상이다.

### 원 S0 재검증

context는 `SYNTHETIC_P2_S0_SOURCE_CONTEXT_V1`, 고정 S0 code pin, 별도 기대 plan SHA/S0 SHA, 원 S0 contract와 LIVE plan/servo/R-a frames다. 전달 S0 bytes의 SHA를 직접 재계산하고 decoder로 canonical/6객체/payload/원 LIVE 연결을 재검증한다. 자기 hash만 다시 맞춘 잘못된 atom 질량·omega 누락·객체 누락도 거부해야 한다.

plan의 identity와 S0 ID, source mapping, 판/벽/이력·고정 기준 재고는 decoder가 반환한 전체 검증 envelope에 결속한다. hash/핀은 진위 인증이 아니며 context와 모든 입력을 함께 일관되게 교체하는 공격을 막는 외부 trust anchor는 이번에 없다. 별도 기대 plan hash를 유지했을 때 plan만 변경하는 대조를 지원한다.

S0의 현재 지원은 6개 객체의 선언·바이트 결속이다. pair의 실제 물리 ID 의미, LIVE contact count와 payload 행 수의 물리 대응, atom force/velocity/omega로 LIVE 관측을 재계산하는 기능은 없다. 이번 P2 재검증도 그 없는 기능을 제공했다고 주장하지 않으며, byte binding을 동시 물리 상태·숨은 이력 보존 인증으로 승격하지 않는다.

## 4. h0·A/B·단위/중력·시간의 toy 계약

`h0 = S0 plate.position.z − declared bottom_z`를 유리수로 대조하고 양수여야 한다. h0 비례 A/B increment와 lift cap을 각각 명시한다. toy h0 10, A 비율 1/10, B 비율 1/40, cap 비율 1/5이면 A increment 1, B increment 1/4, 최대 lift 2다. 실제 h0나 역사 P1 수치를 복사한 것이 아니다. toy unload case는 A/B를 명시해야 하며 `null`/이름 유추는 거부한다. 실제 A/B는 별도 `null`이다.

단위는 명시된 toy length/pressure/energy/acceleration와 물리초 `s`다. gravity는 정책 `EXPLICIT_VECTOR`, 명시 variant, 부호 있는 유리수 벡터와 basis ID를 받는다. `G_` 이름이나 P1 prefix에서 벡터·상태를 유추하지 않는다. MAIN/BRIDGE 같은 variant가 실제 다리 팔의 승인을 뜻하지 않는다. 스칼라나 중력 태그를 숨은 기본값으로 채우지 않는다.

시간은 exact rational의 dt, dt_half, T_W와 exact integer W/W_half, S0의 grid_choice를 받는다. `dt×W=T_W`, `dt_half×W_half=T_W`, `2×dt_half=dt`, `W_half=2W`를 모두 대조하고 선택 grid는 S0/LIVE의 선택과 맞아야 한다. toy dt=1/8, T_W=2이면 W=16, half dt=1/16이면 W=32다. 같은 W로 반시간만 보는 대조는 거부해야 한다. 실제 DEM dt/2 수렴 자격은 아니다.

`primary_selection=SELECTION_UNRESOLVED`를 유지한다. 유효 UNLOADING pressure sample의 첫 `pressure≤declared threshold`는 교차 진단 사건으로만 기록한다. 이 이벤트는 P1 primary 선정이나 실제 측정 endpoint를 재현하지 않는다. toy threshold 1, KE 문턱 1/1000, 표면 변동 문턱 1/1000은 합성 대조 상수이며 실제 등록값이 아니다.

## 5. 창과 사건의 소비 순서

trace는 순서가 있는 WINDOW/PLATE_CLEAR 객체 목록이다. WINDOW는 0부터 연속 index, S0 끝 다음 step에서 시작하는 정확 W-step 구간, 같은 identity·plan/S0 hash·S0 ID·inventory ID·mesh/wall/history·gravity, phase/mode/lift index, complete 표지와 **정확 W개 샘플**을 갖는다. 단순히 끝점 contact count만 0인 것은 충분하지 않다.

각 step 샘플에는 정확한 step, exact nonnegative int contact count, contacts/inventory complete 표지, 유한 KE/표면 높이/pressure/판 z, 전체 ID/type/radius/mass 재고가 필요하다. 누락/None을 0으로 바꾸지 않으며 각 샘플의 전체 재고를 S0 기준과 대조한다. 동일 개수·다른 질량/상/ID는 다른 재고다. 명시 합성 값의 구조 일관성이지 실제 계측 진위 증거는 아니다.

UNLOADING에서는 판/벽/이력을 보존하며 plate z는 h0 비례 increment×lift index의 선언과 맞고 cap을 넘지 않는다. 모든 샘플이 유효하고 count 0인 창만 무접촉 창이다. 두 창은 연속이어야 하며 한 샘플의 nonzero·무효·누락이 있으면 앞 창을 건너 이어 붙일 수 없다. 유효성/계보를 먼저 검사한 뒤 count를 소비한다.

둘째 유효 zero 창 끝 후 목록상 바로 뒤의 PLATE_CLEAR 사건은 같은 end step·after_window index·identity/S0/mesh/wall/history를 갖고, 명시된 z는 직전 판 위치보다 위여야 한다. 같은 step의 사건은 **창 관측 뒤**라는 목록 순서를 뜻한다. 이것은 실제 move 명령이 아니다. 그 전 CLEARED mode·이른 event·DELETE_MESH·재생 event는 거부한다.

이후 정확 4개 POST 창은 같은 S0 재고·같은 explicit gravity·고정 clear 위치·0 contacts, 유효 에너지/표면 값과 완전한 시간 명부를 요구한다. 3개만 오면 INCOMPLETE, 추가 창을 자동 예산 연장으로 수용하지 않는다. 모든 POST 샘플의 KE와 표면 범위를 toy 문턱에 대조한다. 정본의 실제 S2/S4/표면 관측자·기계적 자격을 이 진단으로 대체하지 않는다.

### 상태와 사건 분리

| 출력 | 의도한 의미 |
|---|---|
| `SYNTHETIC_P2_CONTRACT_CONSISTENT` | native 선언과 원 S0 bytes의 좁은 구조 일관성 |
| `SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE` | 두 zero 창→clear→4 post 창의 합성 진단 순서·toy 문턱 충족 |
| `REJECTED` | 신원·형식·시간/순서·재고·정의 불일치. 부분 compiled 성공을 내지 않음 |
| `NOT_COMPUTED` | 필수 contact/inventory 관측 누락 또는 incomplete. 결손을 0으로 대체하지 않음 |
| `INCOMPLETE` | 예정 sample/window/event가 아직 완성되지 않음 |
| `NOT_CONVERGED` | 완전한 관측이 toy KE/표면 문턱을 넘음 |
| `primary_status` | 항상 `SELECTION_UNRESOLVED`; `trajectory_status`와 독립 |
| 세 사건 | `second_zero_window_end`, `plate_clear_event`, `post_end`를 별도로 기록 |
| `first_pressure_crossing` | 유효 UNLOADING 창의 첫 교차 샘플. POST의 새 교차는 제외. 선택·interpolation·실제 endpoint 자격 아님 |

후보 출력에서 실제 T0/T11/T12는 NOT_RUN, 실제 S0/A/B는 null, physical_ready/execution_go/transition/gate/registration/source-auth/hidden-history는 false, 연구 결과 0, 전체 HOLD를 공통으로 둔다. 진단 성공은 실제 P2 소비자·단계 gate 활성화가 아니다.

## 6. 독립 손 계산과 최종 시험 29개

coarse fixture S0 끝 step 96, W=16이다. 창 0은 contact가 있고 창 1·2가 0이므로 둘째 zero 끝은 144다. clear는 그 관측 뒤 같은 step 144의 별도 사건이다. post 창 3–6의 끝은 208이며 유효 교차 첫 샘플은 113이다. half는 S0 끝 192, W=32, 둘째 zero 288, post 끝 416이고 `208/8=416/16=26`으로 물리 끝이 같다. 이 값은 입력의 독립 손 계산 기대이며 생산 API 출력으로 생성하지 않았다. 최종 시험은 이 기대와 실제 반환을 대조했다.

| 시험 | 준비한 대조 |
|---|---|
| 01–03 | h0/A/B/cap 손 계산, native/P1 이름 위장, params hash와 외부 plan hash·S0/mapping hash |
| 04–06 | 원 S0/LIVE 재검증, archive 자기 hash를 다시 맞춘 atom/object 반례, 다른 attempt/unit/S0/h0 |
| 07–08 | exact dt/2 두 배 W, 같은 물리시간, 명시 gravity·case·단위 누락/암묵 정책 거부 |
| 09–11 | 독립 손 계산의 사건 step, half 시간, 교차 없어도 primary/trajectory 상태 분리 |
| 12–17 | zero 1창·중간 nonzero·None/incomplete·gap/stale/duplicate/old attempt/history, 조기 clear·삭제·사건 누락 |
| 18–22 | post 3창 불완전, KE/표면 미수렴, 같은 N 다른 재고, post contact/위치/중력/S0, 연장/replay |
| 23–28 | exact count/유한성, 권한·불명 필드, 입력 무변경, 타입/key hook, h0 cap 초과 |

시험 29는 UNLOADING pressure가 끝까지 문턱 위이고 POST에서만 낮아지는 경우다. trajectory 진단 후보는 유지하되 `first_pressure_crossing=null`, `primary_status=SELECTION_UNRESOLVED`를 요구한다. 이전 구현에서 1 실패·0 오류, UNLOADING 조건 한 줄 추가 후 같은 29개 시험이 통과했다.

반박 검토에서는 native P2 일관성, S0 원입력 재검증, 물리시간/재고/사건 순서와 권한 차단을 한정 확인한다. 닫힌 ULPRI/T12R 범위를 다시 세거나 실제 P1의 52개 합성 시험을 이 후보 시험 수에 더하지 않는다. 이후 원장·운영 봉인·실제 값 열람·제출·연구 실행은 별도이며 이번 준비 권한에 없다.


## 7. 작성 순서와 검증 증거

| 기록 | 메서드 | 실패 | 오류 | rc | 범위 |
|---|---:|---:|---:|---:|---|
| 최초 스텁 red | 28 | 15 | 1 | 1 | test_17의 tuple 대입 준비 오류 포함. 성공적인 전체 red로 부르지 않음 |
| 준비 오류 한 줄 수정 후 red2 | 28 | 16 | 0 | 1 | 구현 전 새 기능 미구현 대조. 기존 P1/S0 물리 결함 재현이 아님 |
| 첫 구현 green | 28 | 0 | 0 | 0 | red2와 같은 시험 바이트 |
| 교차 범위 추가 반례 | 29 | 1 | 0 | 1 | 첫 green 소스에 새 반례 먼저 적용 |
| 한 줄 수정 후 final_green | 29 | 0 | 0 | 0 | 추가 반례 red와 같은 시험 바이트 |
| S0 원입력 재검증 우회 | 29 | 4 | 0 | 1 | 자기 hash만 맞춘 자료/원 LIVE 무효 검출 |
| 외부 plan hash 보호 제거 | 29 | 1 | 0 | 1 | 새 계획 이름으로 교체 검출 |
| 물리시간/half 짝 조건 제거 | 29 | 3 | 0 | 1 | W·물리창 불일치 검출 |
| 첫 sample 외 contact 검사를 무시 | 29 | 1 | 0 | 1 | zero 창 중간의 nonzero를 검출 |
| S0 재고 비교 제거 | 29 | 3 | 0 | 1 | 같은 N의 다른 mass/type/id 검출 |
| post 3창을 완료로 허용 | 29 | 1 | 0 | 1 | 4창 미완료 검출 |
| native profile 검사 제거 | 29 | 1 | 0 | 1 | P1 profile 이름 위장 검출 |

메서드·subtest 실패·전후 반복·7개 변이는 서로 다른 단위다. 합산해 고유 시험 수로 부르지 않는다. 스텁의 음성 거부는 구현 가드가 옳다는 증거가 아니다. 첫 28개 suite와 후속 29개 suite의 차이는 숨기지 않았으며 원본 전부를 보존했다. 초기 시험 준비 오류는 제품 결함 또는 연구 실패가 아니다.

Windows Python 3.12.14, `-I -B`에서 고정 copied bytes를 compile/exec했다. 프로젝트 코드 전에 audit hook으로 프로세스·네트워크를 차단했고 각 호출의 실제 engine·원 자료/로그 접근·금지 프로세스/네트워크 시도는 0이었다. 이 주장은 기록된 호출 범위이며 부모 턴 전체의 문서 열람 이력이 아니다. 기존 q/T0/T11/LIVE/S0 소스·기존 시험을 변경하지 않았고 전체 gate/CI·다른 OS·현장 자격은 실행하지 않았다.

| 최종 바이트 | SHA256 |
|---|---|
| P2 구현 | `cb5b3b66bbb89c39d2faf843c68f1b04853e28d9bcddc69de458f4aa2c194899` |
| 최종 29개 시험 | `0aa20e8128a1e1d9ed0b03e0c61e93c200466562d797df6d5371f0a4a21babe3` |
| fail-closed 스텁 | `f6aff18a81b795d5db7465c3442e33782abcaba5408bcc02acc1b3dcf52e2ca3` |

상세 시각·모든 중간 SHA·rc·원 소스는 `verification_summary.json`과 전달 묶음의 `red/`, `red2/`, `green/`, `crossing_red/`, `final_green/`, `mutants/`, `CHRONOLOGY.json`으로 대조한다. `pre_implementation_preparation/`에는 구현 전 문서·28개 시험·스텁·당시 manifest를 보존했다. `raw_manifest.json`은 원시 증거 집합을 결속한다.

## 8. 구현의 좁은 지원 범위

합성 입력 한도는 S0 bytes 1,048,576 B, trace 65개 record, 창당 256개 이하 step, 재고 256개 이하, 비음수 정수 최대 1,000,000,000, 유리수 분자 절댓값·분모 각각 최대 10^18, canonical JSON depth 48이다. 실제 대규모 frame 성능 또는 운영 자격이 아니다. 물리 위치는 전달된 유한 내장 수의 정확 rational 표현과 대조한다. 실제 근사 좌표 오차 허용폭을 새로 선택하지 않았다.

실패·불완전 반환에도 앞서 유효한 부분에서 기록한 교차/분리 사건이 진단으로 남을 수 있다. 반드시 반환 status와 trajectory_status를 함께 소비해야 한다. 부분 사건을 완료/GO로 쓰거나 다른 attempt에 재사용할 수 없고 실패 시 compiled 성공은 제공하지 않는다. 아직 비어 있는 실제 정량·선정·물리 자격을 이 반환값으로 채우지 않는다.
