# DEM 첫 연결 — 합성 관측에서 단계 진단 후보까지

이번 후보는 **servo→relaxation(R-a) 한 경계의 오프라인 진단 연결**이다. 실제 live reader·엔진 명령·`g2_done`·운영 stage 전이·gate 활성화·정확 경계 serializer·P2 ULPR은 구현하지 않는다. 모든 새 결과는 `physical_ready=false`, `execution_go=false`, `transition_authorized=false`, `gate_write=false`, 연구 결과0이며 전체 HOLD다.

## 근거와 범위

- 바탕 B: `e91bd1c948362712def3f16b5b995027cc10011f`. 승인 문서와 LHS 후속 문서의 동일 바이트 사본은 선행 `43eb8a28c`·`b492a2062`이며 새 DEM 동작은 다음 후보 커밋/검토 묶음에 고정한다. 미확인 원격 요청/후속 쪽지를 받은 것으로 기록하지 않는다.
- 문서 계약: `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §5 첫 연결(live→단계), §3 T11-04–07, §4 관측/판정. 이번 새 지시가 그 첫 연결의 시험 먼저 구현을 허용하며 다른 연결은 그대로 남는다.
- 정본: `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §12. Q2 정량 등록값을 선택한 작업이 아니다. 입력 예의 수치·정수 tick·이름은 합성 fixture이며 실제 빌드·T0 극성·단위·강성·시간·침대 관측의 빈 사실을 채우지 않는다.
- 기존 G2PREP-01–04, ULPRI-01/02·T12R-01의 한정 수용/종결은 유지한다. 새 실제 물리 결함 또는 같은 범위의 재개방 판정이 아니다. T0/T5/T11/T12=NOT_RUN·physical_ready=false는 유지한다.

## API와 이전 계약의 구분

`scripts/dem_gen2_qualification.py`의 기존 `static_guard(rows, target, rules)`는 신원 인증기가 아니라 두 인접 합성 창의 스칼라 guard였다. **정확한 내장 dict로 주는 문맥 없는 scalar 계약**은 보존한다. 이전 소스가 추가 run/stage/sample/time 필드를 무시한 것은 **기존 문서상 범위 밖의 연결 공백**이며 과거 한정 수용을 취소할 근거로 쓰지 않는다.

새 public `observation_bridge(rows, target, rules)`는 `observation_contract`가 없으면 거부한다. `static_guard`에 해당 문맥을 명시한 경우에도 새 진입으로 보낸다. **rules 지원형식을 정확한 내장 dict로 명시적으로 좁혔다.** dict subclass·UserDict 등은 문맥 유무에 관계없이 REJECTED이며, membership 후크나 객체 종류 때문에 명시 문맥이 legacy 수용으로 후퇴하지 않는다. 모든 과거 duck-typed 객체 동작을 보존했다고 주장하지 않는다. 문맥 없는 legacy 반환 `SYNTHETIC_STATIC`은 이 새 연결의 성공 표지가 아니다.

정상 새 결과도 `SYNTHETIC_STAGE_CANDIDATE`와 `candidate_stage=relaxation`이라는 **진단 후보**일 뿐이다. 새 API에 CLI·파일 reader·잡 제출·프로세스/네트워크 호출·gate 파일 쓰기 기능은 없다. 호출자가 물리 전이로 연결할 권한도 주지 않는다.

## 명시 입력 계약

입력은 정확한 내장 list/dict·숫자·문자열의 합성 자료다. 문자열 신원은 1–128자의 공백 없는 ASCII 토큰이며 실제 provenance나 승인자 진위를 인증하지 않는다. bool을 정수로 받아들이거나 비정수 식별자를 반올림하지 않는다. 선언된 문맥·행에서 알 수 없는 필드도 거부한다.

| 구역 | 필요한 필드·의미 |
|---|---|
| scalar rules | 기존 `samples_per_window`(n≥2), `sample_stride`(양의 정수), 양의 `max_ke`, 비음수 `max_drift_fraction`, 명시적 합성 `expected_inventory`; 여기에 `observation_contract`만 추가 |
| 목적·한 경계 | `schema=SYNTHETIC_OBSERVATION_BRIDGE_V1`, `purpose=SYNTHETIC_PREPARATION`, `source_stage=servo`, `requested_boundary=SERVO_TO_RELAXATION`만 지원 |
| 고정 신원 | `run_id`, `bed_id`, `arm_id`, `attempt_id`, `definition_id`, `unit_system_id`. 모든 행의 해당 토큰을 문맥과 정확히 대조 |
| 계획 | `first_step`, `first_sample_id`, `first_tick`, 양의 `tick_stride`, `planned_samples`, `expected_end_step`, `expected_end_tick`, `delay_samples`. 계획은 최소2창·정수 창 수이며 끝 step/tick이 시작/간격/개수와 일치해야 함 |
| 각 행의 시점 | `step`, `sample_id`, `time_tick`, `window_index`, `stage`, `boundary_id`. 처음부터 선언한 간격·순서·창 소속을 대조; 줄을 정렬/결손 제거/끝만 잘라서 맞추지 않음 |
| 각 행의 스칼라 | `force`, `ke`, `residual`, `damping`, `inertia`, `escaped`, `inventory`, `contacts_complete`. 유한값·기본 부호/형식·완전성·합성 재고 토큰을 **전체 trace**에서 검사 |
| 지연 | `delay_samples`는 제공 trace 범위 안의 정수. 예산 끝에서 소비될 마지막 `delay+1`개 행을 동일 trace에서 직접 재구성. `pending_queue_ok` 같은 자기 신고 bool 입력은 없음 |

`time_tick`은 선언된 합성 정수 시계와 step/sample 순서의 결속이다. 실제 wall-clock freshness·물리 dt 환산·원 기록 생성자를 인증하지 않는다. 모든 신원 토큰을 함께 거짓으로 다시 붙이는 경우까지 인증하는 도구가 아니며 실제 live observer에 필요한 provenance는 아직 별도다. `expected_inventory`는 기존과 같은 합성 토큰이며 실제 ID/type/radius/mass·상별 재고 전체의 증거가 아니다.

## 관측·후보 판정 순서

| 순서 | 동작 | 실패/미완료 |
|---|---|---|
| 1 | 필수 문맥·유형·합성 목적·단일 경계·창/예산/끝 anchor 확인 | `REJECTED / INVALID_OBSERVATION_CONTRACT`; 문맥 누락도 legacy fallback 없음 |
| 2 | 제공된 모든 행의 정확 필드·신원·시점·창·유한성·접촉/재고 완전성 확인 | `REJECTED / INVALID_OBSERVATION_TRACE`; 잘못된 행을 버리지 않음 |
| 3 | 최초로 rolling 두 창을 만족한 sample을 진단 사건으로 기록 | 최초 hit는 한 sample씩 이동하는 진단이며 고정 window_index의 끝점에만 한정하지 않음. hit가 있어도 전체 선언 예산이 없으면 `INCOMPLETE / DECLARED_BUDGET_NOT_OBSERVED` |
| 4 | 선언한 예산 끝의 마지막 두 인접 **고정 계획 창**을 기존 스칼라 guard로 검사 | planned_samples가 n의 정수배이므로 terminal 두 창은 window_index에 정렬. 불충족은 `NOT_CONVERGED / TERMINAL_WINDOWS_UNSTABLE` |
| 5 | 같은 trace의 pending 지연 행을 실제 값으로 대조 | `NOT_CONVERGED / PENDING_SAMPLES_UNSTABLE`; 끝 창이 좋아도 이전 대기 입력이 나쁘면 거부 |
| 6 | 모든 조건 충족 | `SYNTHETIC_STAGE_CANDIDATE / DIAGNOSTIC_ONLY`; 실제 전이/실행/물리 자격 flag는 여전히 false |

기존 점별 힘 오차 `.01`, 창 평균 오차 `.005`, residual `.01`, damping/inertia `.001` 등은 **기존 static_guard의 합성 경계**를 재사용한다. 실제 정량 등록이나 S1–S4 전체 자격으로 이식하지 않는다. pending 행은 그 점별 경계를 확인하며 pending 전체를 별도의 평균 창으로 승인하는 의미가 아니다. torque·epsilon/height drift·절단면 수지, 실제 접촉 이력·T0·물리 단위·R-a/S0/언로딩은 이 함수의 확인 범위 밖이다.

## 시험·증거 읽는 법

새 시험은 `scripts/test_dem_gen2_observation_bridge.py`다. 이전과 현재 소스 사본을 같은 시험 바이트로 대조한다. baseline은 실제 옛 `static_guard`를 호출하여 문맥 불일치인데도 `SYNTHETIC_STATIC`을 반환하는 assertion 반례를 남긴다. 새 public 진입의 문맥 누락 시험에서는 새 함수가 아직 없는 baseline만 명시적으로 기존 guard를 호출하며, missing-module/TypeError 자체를 red 근거로 세지 않는다.

최초 기록은 기존22/22 PASS → 새30메서드/58 assertion·subtest failure/error0 → 새30/30 및 기존22/22 PASS다. 내부 읽기 검토에서 dict subclass의 optional dispatch 후퇴를 찾아 새 회귀를 먼저 추가했고, 당시 후보에서31메서드 중 해당2조건 failure/error0를 보존했다. UserDict 및 무문맥 mapping까지 지원형식을 명시한 최종32메서드는 중간 후보에서3조건 failure/error0를 먼저 확인했다.

| 최종 대조 | 결과 |
|---|---|
| 원 소스 + 최종 동일 시험 | 32메서드, assertion/subtest failure63, error0, rc1 |
| 최종 소스 + 같은 시험 | 32/32, failure0/error0, rc0 |
| 기존 qualification 시험 | 22/22, failure0/error0, rc0; 원 시험 바이트 보존 |
| 핵심 guard 제거 대조 | 6/6에서 정상 소스 거부→guard 제거 시 진단 후보 수용을 검출; 별도 합성 관측 |
| 최종 소스 SHA256 | `9bcf11ba48403f1073a0bbd6c6c2d93cbd34d7512c8ff810a48d57493f1f9c2c` |
| 전후 동일 새 시험 SHA256 | `dbac34ceeeeff9c3593c6186a5dbdada435e02f0c71b08c9cb2b2d6264c7cb52` |
| 원 소스 SHA256 | `582e60c058f9108900f340d34d356acf8126da5fe702090c1cdcf1ecf10997e9` |

최초30/중간31/최종32와 반복 회귀를 더해 고유 시험 수로 세지 않는다. 원본 소스에서 최종 시험을 다시 실행한 red도 별도 보존했으며 최초 기록을 덮지 않았다. 구체 UTC·소스/시험 사본·영수증 hash는 검토 묶음에 있다.

신원·tick·sample·예산·terminal 창·pending 검사를 각각 제거하는 여섯 메모리 변이에서는, 고친 소스의 거부가 변이에서 진단 후보 수용으로 바뀌는 작은 합성 대조를 남긴다. terminal 대조는 점별 오차는 허용폭 안이지만 창 평균은 벗어나는 사례다. 변이·기존22·신규 메서드는 서로 다른 관측 단위다. 변이에서도 운영 권한 flag는 켜지지 않는다.

원본 콘솔·오류·소스 사본·hash/시각 영수증은 리포 밖에 보존하여 검토 ZIP에 포함한다. 시험은 프로젝트 소스를 exact bytes로 compile/exec하고, 프로젝트 모듈을 읽기 전 subprocess/socket/exec/spawn 경계를 설치한 로컬 합성 실행이다. 실제 engine/MPI/호스트/자료·Rint·전체 gate는 호출하지 않았다. 새 시험은 공용 `check_all`/CI에 연결하지 않았다.

## 보존과 다음

`make_dem_gen2_decks.py`는 Git blob `7a24b8070c33e6c924773ea18fc49a855b651b54`, SHA256 `f778a145e693111c3d95f6c6469ac7acbac7bd16192b400b1bbd5bdd700ae5d9` 그대로다. 입구 HOLD와 일곱 gate 정의가 포함된 **생성기 소스의 바이트 보존**을 확인했다. 이번에 생성기를 실행하여 실제 덱/새 gate를 만들었다는 뜻이 아니다. 기존 생성기18/18은 과거 한정 수용 기록이며 이번 재실행 수에 포함하지 않는다. 기존 자격 함수 시험의 바이트도 보존한다.

이 후보의 고정 핀·red/green·회귀·내부 반례를 별도 반박 창에 보내는 주체는 1저자다. 외부 수용 전 구현 후보이며, 수용되더라도 실제 live reader·정확 경계·P2 ULPR 연결과 Q2 정량 비준/Q4 자격 수행을 자동 승인하지 않는다. 원장 직접 변경0, 운영 재봉인0, 실제 값/원로그 열람0, 연구 결과0, 전체 HOLD다.
