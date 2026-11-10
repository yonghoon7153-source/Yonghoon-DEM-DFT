# LIVE 필수 채널 결속과 독립 R-a 진단 — 오프라인 합성 후보

**권고안 전제(Q-LIVE-1/2). 전체 HOLD. 연구 결과 0. 최종 합성 시험 25/25.**

이 후보의 바탕은 T11 준비 핀 `ea5f22b6ae807dda3decf1928ec310d459996cb9`, 가지는 `codex/dem-live-ra-contract-1110`이다. 검증된 source·시험을 정확한 바이트로 옮기고 문서만 이 부모에 맞췄다. 이 가지에서 시험을 재실행하지 않았다. B 반입·독립 판정은 아직 없다. 실제 관측 자료·원 로그·호스트·엔진·운영 봉인은 읽거나 변경하지 않았다. 이 문서의 숫자와 예시는 모두 합성 전제이며 등록된 과학 허용값이 아니다.

## 1. 작성 순서의 사실

초기 지시의 '순수 계약 모듈·시험·문서 초안'을 scratch 구현도 포함하는 것으로 해석하여 `scripts/dem_gen2_live_contract.py`에 구현 초안을 먼저 작성했다. 이어 `scripts/test_dem_gen2_live_contract.py`의 시험 25 메서드를 작성했다. **이 시점까지 시험·프로젝트 코드 실행은 0이며, red 증거도 없다.**

그 뒤 root가 구현 본문은 red 기록 뒤에 작성하라고 정정했다. 이미 작성한 구현 초안은 삭제하거나 이력을 숨기지 않고 보존한다. 별도 `baseline/dem_gen2_live_contract.py`는 명시적인 신규 기능 fail-closed stub이다. 후속 기록은 '사전 구현 초안 존재 → 같은 고정 suite의 stub red → 후보 보완/green'으로 적어야 한다. 이를 '어떠한 구현 작성보다 red가 먼저였다'거나 기존 제공기의 결함 재현이라고 쓰면 안 된다.

이후 허용된 scratch 검증에서 같은 고정 25 메서드를 stub에 실행하여 67 assertion/subtest 실패·오류 0·rc1을 기록했다. 보존한 사전 구현 초안의 첫 실행은 1실패·오류 0·rc1이었다. 누락 balance 구성요소를 REJECTED 대신 NOT_COMPUTED로 분류하도록 후보 복사본만 최소 보완한 뒤 25/25를 확인했다. 최종 source docstring을 '미실행 staging'에서 'offline contract'로 정정하고 동일 시험 25/25를 재확인했다. 테스트 파일의 첫 'Unexecuted staging suite' 문구는 첫 작성 시점의 원문을 그대로 보존한 것이며 현재 미실행이라는 뜻으로 사용하지 않는다.

## 2. 확정할 API와 의존

```python
diagnose_live_ra(plan, servo_frames, ra_frames) -> dict
```

입력은 exact built-in dict/list/str/int/float/bool/null 중 스키마가 허용한 것만 받는 순수 자료다. 객체 하위형의 변환·비교 hook은 지원하지 않는다. 출력도 순수 자료이며 파일 I/O·현장 reader·엔진 상태 변경·등록·실제 봉인 기능이 없다.

| 의존 | 읽은 기준 | 이번 소비 범위 |
|---|---|---|
| `dem_gen2_qualification.py` | T0 핀 `c5ebaa71298691020313e272b39c0a80b51cdc4d`의 비변경 파일 | `number`, `integer`, 기존 `observation_bridge`, `static_guard` |
| `dem_gen2_t0_contract.py` | 같은 T0 핀 | T11이 원 입력을 재대조하는 합성 T0 계약 |
| `dem_gen2_t11_contract.py` | T11 핀 `ea5f22b6ae807dda3decf1928ec310d459996cb9`; source SHA256 `b12daff4201c7b1424f47e9a558587b5f0216d6207061fbd6bf2de40814cfd59` | `validate_t11_plan`, `canonical_sha256` |

T11 핀의 q/T0/T11 Git blob과 실제 시험에서 읽은 세 source의 바이트가 3/3 일치함을 대조했다. 원 T11 plan과 frozen_context를 LIVE 함수 안에서 재검증한다. 외부에서 전달한 `DRAFT_CONTRACT_VALID` 영수증만으로 대체하지 않는다. T11이 돌려준 합성 격자와 선택 case의 target만 소비하며 모델 error에서 판 힘·에너지·토크를 생성하지 않는다.

## 3. 권고안 전제(Q-LIVE-1): 입력 결속

### 3.1 계획

계획의 exact 키는 `schema`, `purpose`, `protocol`, `assumptions`, `t11_plan`, `t11_context`, `case_id`, `grid_choice`, `scalar_profile`, `scalar_limits`, `extra_limits`, `inventory_id`, `reference_inventory`, `plate_reference`, `ra_window_count`다.

- schema=`DEM_GEN2_LIVE_RA_SYNTHETIC_PLAN_V1`, purpose=`SYNTHETIC_PREPARATION`, protocol=`P2`.
- assumptions=`[Q-LIVE-1, Q-LIVE-2]`.
- grid_choice=`coarse` 또는 `half`. 선택 T11 grid가 step·sample·tick·window와 servo 예산을 제공한다. dt/2인데 같은 step stride를 복사하는 입력은 격자 결속에서 거부한다.
- `scalar_profile=EXISTING_SYNTHETIC_STATIC_GUARD_V1`만 지원한다. `scalar_limits`에는 `max_translational_ke`, `max_drift_fraction`만 허용한다.
- `extra_limits`에는 `max_rotational_ke`, `max_torque_residual`, `max_torque_damping`, `max_torque_inertia`를 각각 명시한다. null은 미선택이며 0으로 채우지 않는다. 명시적 0과 누락은 다르다.
- `reference_inventory`는 exact `id/type/radius/mass` 행의 비어 있지 않은 목록이다. ID는 유일한 양의 exact int이며 type은 양의 exact int, radius와 mass는 유한 양수다. 같은 개수만으로 보존을 판정하지 않는다.
- `plate_reference`는 position/velocity 3벡터와 mesh_id/wall_id/history_id다. R-a 참조 속도는 명시적 0벡터이며 위치는 합성 표현 그대로 비교한다. 실제 측정 오차 허용폭이나 숨은 이력 자격은 아니다.
- `ra_window_count`는 최소 2인 exact int다. R-a 예산은 선택 T11 window ticks × 이 수이며 완전한 예산 뒤 마지막 두 창을 독립 판정한다.

### 3.2 기존 scalar profile의 정확한 한계

**Existing synthetic scalar floor + explicitly declared extra-channel toy limits.** 기존 `static_guard`의 point force/residual 1%, damping/inertia 0.1%, 창 평균 force 0.5% 규칙을 그대로 소비한다. 사용자가 지정한 KE·창 사이 drift와 함께 기존 합성 규칙일 뿐이며 실제 T11 등록값으로 승격하지 않는다.

새 계획이 force/residual 허용폭 등을 느슨하게 override하는 키를 넣으면 exact schema 위반으로 거부한다. 실제 등록값이 이 profile과 다를 때 조용히 덮어쓰는 기능은 없다. 지원 범위 변경은 별도 구현·반박 검토 대상이다.

토크의 절대 toy 한계와 회전 KE 한계는 기존 scalar 판정에 추가한다. **residual/gravity/damping/inertia는 입력으로 선언한 채널**이며 별도 필드로 완전하게 받아 결속한다. 입자의 힘·토크에서 물리 수지를 새로 계산하거나 인증한 것이 아니다. 중력 벡터가 0이라는 가정은 하지 않는다. 입력 잔차가 실제 Newton 방정식·모든 외력 분해와 일치한다거나 접촉 완전성이 물리적으로 인증됐다고 판정하지 않는다.

### 3.3 프레임과 채널

프레임 exact 키는 `source_identity`, `stamp`, `channels`다. stamp는 run/bed/arm/attempt/definition/unit_system 신원 6개와 stage, step, sample_id, time_tick, window_index다. **각 채널은 자체 stamp를 다시 가진다.** 값이 정상이어도 다른 프레임·창·stage의 채널을 합치면 거부한다.

source_identity는 원 T0 identity 전체에 `t0_packet_sha256`, `t11_plan_sha256`, `case_id`, `grid_choice`를 더한 선언이다. 이는 일치성 label이며 출처 인증이나 실제 빌드 신원 증명이 아니다.

모든 채널의 exact 키는 `stamp`, `unit_id`, `complete`, `values`다. complete는 exact bool만 지원하고 false/null은 관측 미완전으로 분리한다.

| 채널 | exact values | 합성 unit profile |
|---|---|---|
| reaction | raw_reaction, compression_sign, normalized_force, area_deck_m2, pressure_deck | TOY_DECK_REACTION_AREA_PRESSURE_V1 |
| energy | translational_ke, rotational_ke | TOY_DECK_TRANSLATIONAL_ROTATIONAL_ENERGY_V1 |
| force_balance | residual, gravity, damping, inertia 각각 3벡터 | TOY_DECK_FORCE_VECTOR_V1 |
| torque_balance | residual, gravity, damping, inertia 각각 3벡터 | TOY_DECK_TORQUE_VECTOR_V1 |
| plate | position, velocity 각각 3벡터; mesh_id, wall_id, history_id | TOY_DECK_POSITION_VELOCITY_V1 |
| contacts | count | EXACT_CONTACT_COUNT_V1 |
| inventory | particles(id/type/radius/mass 목록), escaped | TOY_ID_TYPE_RADIUS_MASS_V1 |

반력은 같은 프레임의 raw × 선언 sign = normalized를 대조하고 pressure = force/area도 대조한다. 이는 동일 합성 샘플 산술이며 실제 극성 측정이나 압력 도달 자격이 아니다. contacts의 None·누락·불완전을 0으로 바꾸지 않는다. inventory는 전수 ID/type/radius/mass와 escaped=0을 요구한다. 실제 원자 보존 확인은 여전히 미수행이다.

## 4. 권고안 전제(Q-LIVE-2): 두 단계 진단

1. 모든 servo 행에 필수 채널·단위·신원·시점·재고를 검사하고 기존 bridge가 요구하는 scalar 행만 정확히 투영한다.
2. `observation_bridge`로 전체 선언 예산, 첫 hit, terminal 두 창, pending delay suffix를 판정한다. 기존 기능을 복제하지 않는다. 첫 hit 뒤 예산 누락·뒤늦은 실패는 R-a 후보가 아니다.
3. 추가 회전 KE·토크 조건은 servo terminal 두 창과 pending suffix의 합집합에 적용한다. 과도 과정의 초기 값까지 전부 안정해야 한다는 새 규칙으로 바꾸지 않는다. 모든 초기 행도 형식·완전성·보존은 통과해야 한다.
4. 마지막 servo 판 위치는 R-a 고정 참조 위치와 같아야 한다. R-a는 다음 control step/sample/tick에서 시작한다. window_index는 stage마다 0으로 재시작한다. 이것은 합성 기록 규약이며 엔진 정지·이동 명령이 아니다.
5. R-a 전체 예산에 같은 mesh/wall/history 선언과 고정 판 위치·0속도, 신원·채널·재고를 요구한다. 마지막 두 창에 기존 scalar guard와 추가 조건을 독립 적용한다.
6. 성공은 `SYNTHETIC_RA_END_CANDIDATE`일 뿐이다. 원자·pair·wall·mesh·restart·state 6종의 실제 S0 기록은 아직 만들지 않는다.

## 5. S0가 소비할 boundary_candidate

실패 출력의 boundary_candidate는 항상 null이다. 성공 출력의 exact 키는 다음과 같다.

| 키 | 의미 |
|---|---|
| schema | SYNTHETIC_RA_BOUNDARY_CANDIDATE_V1 |
| stage / boundary_id | relaxation / RA_END |
| identity | run_id, bed_id, arm_id, attempt_id, definition_id, unit_system_id |
| source_identity | §3.3의 전체 T0 선언 + T0 packet/T11 plan 해시 + 선택 case/grid |
| end_step / end_sample_id / end_tick / end_window_index | 마지막 완전한 R-a 프레임의 exact integer 경계 |
| plate | position, velocity, mesh_id, wall_id, history_id |
| inventory_id / reference_inventory | 합성 label과 고정 id/type/radius/mass 목록 |
| plan_sha256 / servo_trace_sha256 / ra_trace_sha256 / end_frame_sha256 | 검증한 원 입력의 canonical JSON bytes 해시 |

S0는 caller가 전달한 성공 status/candidate를 그대로 신뢰하지 않고 `diagnose_live_ra(plan, servo_frames, ra_frames)`를 다시 호출한 뒤 이 전체 경계와 대조한다. 해시는 T11 canonical JSON convention(sort keys, ASCII, compact separators, NaN 금지)을 따른다. input 재검증·해시 일치는 실제 출처·숨은 이력의 진위 증명이 아니다.

## 6. 새 시험 계획과 후속 절차

작성된 고정 메서드는 25개이며 최종 25/25를 확인했다. 메서드·subtest·guard 제거 관측·전후 반복을 합산하지 않는다. 새 suite는 다음을 겨냥한다.

- 양성 두 부호와 dt/2 격자, 입력 보존·반환 사본 분리·경계 해시.
- torque/rotKE/force 구성요소 누락, contact 미완전/None, mixed stamp·창·stage.
- bool/float integer 위장·하위형 hook·NaN/Inf 거부.
- 같은 N의 ID/type/mass/radius 변화, 중복·누락·escaped.
- 첫 hit 뒤 예산 누락·뒤늦은 scalar 실패·pending 추가 채널 실패.
- servo 성공 뒤 독립 R-a 예산 누락·판 이동·이력 변경·terminal 불안정.
- 원 T11 입력 재검증, self-reported 성공 거부, 새 toy limits로 기존 scalar profile 완화 금지.

같은 시험의 stub red·원초안 실패·후보 green을 각각 보존했다. mixed-frame, source identity, 전수 재고, 고정 판, R-a 예산, 추가 채널 한계, exact completeness flag의 guard 제거 7종을 모두 검출했다. 최종 docstring 정정 전 후보에 대한 대조이며, 최종 후보와는 module docstring을 제외한 AST가 동일하다. 최종 25/25는 같은 메서드의 반복이며 새 고유 시험 수가 아니다. 기존 T0/T11 suite 전체와 full gate는 재실행하지 않았다.

모든 출력에서 physical_ready/execution_go/transition_authorized/gate_write/operational_seal_modified/registration_complete/source_authenticated는 false다. actual_T0/T11/T12는 NOT_RUN, 실제 build/sign은 null이다. 연구 결과는 0이다.

## 7. 근거와 별도 미완료

- `13eb293cd9ac44502517c81e8f5e9b7ae02d817f:docs/reviews/nonrint_next_decisions_20261109.md` §1 live·T11·S0·T12 미완료 항목.
- 같은 트리 `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §3(T11-04–08), §4–5.
- `c5ebaa71298691020313e272b39c0a80b51cdc4d:docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §2-5 R-a 고정 판·독립 창·S0 위치, §5·§12.
- 같은 T0 핀의 `scripts/dem_gen2_qualification.py` observation_bridge/static_guard. scalar 신호만으로 지원하는 좁은 진단을 이번 신규 범위의 과거 결함으로 소급하지 않는다.

실제 observer·binary syntax·물리 unit/sign·숨은 이력·S0 6종 직렬화·P2 ULPR·판 분리·현장 자격·등록·운영 봉인·GO는 별도다. 본 후보의 nominal unit ID나 hash 일치가 그 항목을 대신하지 않는다.

## 8. 최종 검증 신원

| 항목 | 값 |
|---|---|
| 최종 source SHA256 | `a4e4d1c9e6574bac2c338d68e093dd999afc2c42c82c9f84f5011abd437d189c` |
| 고정 시험 SHA256 | `78bb9922813c208b514c7ced4525d58e8b828c4d90cebb83655b5791bf42421a` |
| 보존한 사전 구현 초안 SHA256 | `70118a4cff0f1c703e89e19bc2e3d939e4be2a9bc8a8408bf0378458c7691b65` |
| 7 guard 제거 대조의 원 후보 SHA256 | `def0667439711ad24738e1009c08514ab81f2329f07896a8b6de08bf1a00a164` |
| process/network 시도 | 모든 명시 시험에서 0; project source 실행 전에 audit hook 설치 |
| 실행 방식 | Python 3.12.14, `-I -B`, 정확 복사 source bytes만 명시 시험으로 실행 |
| 별도 미수행 | 실제 DEM·원자료·현장·운영 봉인·full gate·실제 T0/T11/T12 |

`verification_summary.json`은 정확한 순서와 한정, 이전·최종 source 신원 및 docstring 제외 AST 대조를 기록한다. `green`과 최종 source는 `a4e4d1c…`, `previous_green`과 7 guard 제거 대조의 기준은 `def06674…`로 구분한다. 최종 source에 7변이를 다시 실행했다고 쓰지 않는다. raw evidence의 최초 manifest는 덮어쓰지 않았으며, 최종 scratch 전체 153파일 목록의 SHA256은 `423bf6f7fd6c4328d0182b6b59e89bd3b0f895bcffef927b28fe017ab05bdd18`이다. 상기 파일 해시는 바이트 신원이며 물리 출처 인증이 아니다.
