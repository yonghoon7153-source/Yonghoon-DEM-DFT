# DEM 세대 2 자격 사례 행렬 — 합성 선언·상태 연결

**권고안 전제(Q-QUAL-A/B). 전체 HOLD. 작성측 합성 시험 25/25. 실제 자격·연구 결과 0.**

바탕은 P2 준비 핀 `c571a27119ace92ca34d3d6f2b61135219a3f1b4`, 후보 가지는 `codex/dem-qualification-matrix-1110`이다. B 반입과 외부 반박 판정은 아직 없다. 이번 API는 원 P2/S0/LIVE 입력과 고정 사례 분모·시도/체크포인트 선언·dt/2의 정확 물리시간을 연결한다. 실제 binary·이력·재개 영수증을 읽거나 인증하지 않는다. 현재 q/T0/T11/LIVE/S0/P2·그 시험은 보존했다.

## 1. 시험 먼저의 순서

설계와 25개 시험 메서드, 공개 fail-closed stub를 먼저 작성했다. P2 핀 1곳을 고정한 뒤 stub에 동일 시험을 실행하여 **42 assertion/subtest 실패·오류 0·rc1**을 기록했다. 이 red 완료를 root에게 보고한 뒤 처음 구현 본문을 작성했다. 첫 구현은 같은 고정 시험 **25/25·rc0**이었다. 그 뒤 별도 복사본의 guard 약화 8종을 모두 검출했다. 실패 영수증·source·stdout/stderr·시각은 보존했다.

stub red는 양성 assertion과 구체 기대 상태의 실패다. import 오류나 과거 제공기의 결함으로 계상하지 않는다. 시험 파일 첫 문단의 'not executed at authoring'은 작성 당시 사실이며 현재 미실행이라는 뜻이 아니다. 시험 파일은 핀 고정 이후 red/green/8변이에서 바이트가 같다.

## 2. 지원하는 좁은 계약

```python
validate_qualification_matrix(plan, packets, frozen_context) -> report
```

명시적으로 `SYNTHETIC_CASE_MATRIX`만 지원한다. 계획은 고정 source manifest·case 목록·attempt 목록·coarse/half 비교쌍을 가진다. 별도 frozen_context의 plan hash·source manifest·선언 순서를 대조한다. exact built-in 형식 외 객체·unknown 필드·actual GO 필드는 거부한다. 보존한 hash와 순서 정수는 자기 신고 자료의 일관성이지 실제 사전등록·실행 당시 신원 인증이 아니다.

각 packet은 원 P2 plan/S0 bytes/context/trace를 포함한다. P2 검증 경로가 S0 decode와 원 LIVE 입력을 다시 대조한다. `status=PASS`, rc0 또는 caller가 채운 checked_count만 받아 통과하는 경로는 없다. 이번 adapter의 사례 종류는 **완전한 P2 toy 진단**과 **예상된 post 예산 미완료 음성** 두 가지다. 다른 T0/T5/T11/실제 T12 receipt를 전부 통합하는 범용 인증기가 아니다.

| 항목 | 실제 검사 | 한정 |
|---|---|---|
| source/정의 | 고정 P2/S0 의존 핀, manifest와 producer/consumer 선언, case별 원 plan/S0 hash·run/attempt/definition/grid | 실제 source 실행·binary 빌드 신원·자료 진위 인증 아님 |
| 고정 분모 | 명시 case의 중복/추가 거부, 누락 ID와 계획 수 보존, case 순서대로 결과 반환 | 성공한 subset이나 최신 시도를 자동 선택하지 않음 |
| 원 입력 | `validate_p2_contract`와 `diagnose_p2_separation`의 원 입력 재검증 | 기존 함수의 좁은 범위를 승격하지 않음 |
| 음성 역할 | 정확히 예상된 INCOMPLETE와 사유가 맞는지 확인 | 기술 파싱 실패·다른 거부를 기대 음성 성공으로 바꾸지 않음 |
| 시도 종료 | DECLARED_COMPLETE/PARTIAL/FAILED를 분리하고 실패/부분을 완료로 표시하지 않음 | 이 열은 합성 선언이며 실제 종료 영수증·재시도 승인이 아님 |
| checkpoint 계보 | RA_END·step·opaque restart payload hash·parent attempt/hash/step·dt 일치, 순환/중복 거부 | 실제 checkpoint 생성·복원·숨은 이력 보존을 확인하지 않음 |
| 시간 쌍 | dt/2 관계와 시작/끝/window의 exact rational 물리시간 | 실제 수치 수렴·오차 예산·Rayleigh·작은 bed 자격 아님 |

최대 결과는 `SYNTHETIC_MATRIX_CONSISTENT`다. 모든 실제 자격은 NOT_RUN, actual binary/S0는 null, 등록·출처 인증·숨은 이력·physical_ready·execution_go·gate_write·운영 봉인 변경은 false다. 원 지적·원장을 종결하거나 verified로 승격하는 기능은 없다.

## 3. 세 선언 사례의 정확한 뜻

기본 fixture는 coarse 양성, half 양성, 부분 예산 음성의 **계획된 3사례**다. 각각 다른 합성 attempt를 쓰고, 부분 음성은 coarse의 선언 checkpoint에 연결된다. 세 사례가 기대와 일치하면 `matched_expectations=3`이지만 **물리 성공 3건이 아니다**.

EXPECTED_NEGATIVE 1건은 원 P2가 `INCOMPLETE / SEPARATION_OR_POST_BUDGET_INCOMPLETE`를 반환하는 것이 기대다. 그 경우 행의 `meets_expectation=true`, `synthetic_case_complete=false`다. positive가 부분/실패이거나 case가 누락되면 행렬은 INCOMPLETE다. 음성에 다른 종류의 기술 실패가 생기거나 정상 완료로 바뀌면 REJECTED다.

부모 시도가 DECLARED_FAILED라도 그 전에 지정된 checkpoint 선언의 계보 자체는 표현할 수 있다. 이때 lineage 일치와 부모 case 실패를 각각 남기고 행렬을 완료시키지 않는다. DECLARED_COMPLETE와 opaque checkpoint hash 어느 것도 실제 재개 영수증이 아니다. 옛 attempt의 trace를 새 attempt로 붙이면 원 P2 신원 대조에서 거부한다.

## 4. 시간 비교와 초기 상태의 제한

time_pair는 coarse와 half의 시작·계획 끝·window 물리시간을 정확 rational로 대조한다. W를 그대로 둔 반시간 관측, 임의 end step·시간, 다른 inner grid는 통과하지 않는다. 두 전체 S0 archive는 dt/grid·attempt 등의 metadata가 달라 서로 다른 바이트여야 할 수 있으므로 전체 hash 동일성을 강요하지 않는다.

`initial_state`의 범위는 **atom/mesh/restart payload hash와 history 선언 ID의 명시 부분집합**뿐이다. pair/wall/state payload, 모든 물리 채널, 실제 숨은 상태 또는 실제 같은 초기 물리상태의 완전한 동등성을 확인하지 않는다. S0가 하지 않는 inter-object 물리 대조를 이 계약이 추가했다고 쓰지 않는다. 같은 부분집합과 같은 물리시간은 실제 dt 수렴·허용 오차 충족의 증거가 아니다.

## 5. 남은 자격·등록·통합

| 항목 | 이번에 남긴 연결 | 실제 남은 것 |
|---|---|---|
| binary/T0 | producer·consumer·정의·의존 label/hash | 지정 빌드·실제 문법·단위·극성 영수증 |
| 이력/T2 | history 선언과 opaque checkpoint 바이트의 계보 | move/fix 재생성 양·음성, 실제 delta_max/shear 및 복원 보존 |
| 재개/T13 | stage/attempt/parent/checkpoint·부분/실패 분리 | 실제 세대 2 단계별 재개·G1–G3·checkpoint/state 수행 자격 |
| dt/2/T10 | exact 물리시간과 선언 초기 부분집합 | 실제 timestep 진단·등록된 오차/수렴·같은 상태 관측 |
| T12 접합 | 현재 P2→S0→LIVE 원 계약을 재검증하는 합성 adapter | 실제 producer/consumer·R-a/S0·복원/판독·등록된 관문·현장 통합 |
| 등록/통합 | 고정 후보 핀·의존·분모·상태 장부 | T5/T11 실제 정량 선택·출처/담당·실제 전체 자격·B 반입·독립 판정 |
| DEMP-01/02 | 실제 자격을 NOT_RUN으로 보존 | 새 수지/기하·연속성·허용값·50 kg/0.7/1 µm 같은 정적 상태 요구는 별도 다음 계약·실자료 범위 |
| 운영/실행 | 모든 authority false | 최종 범위의 반박 창 GO와 1저자 별도 GO, 운영 봉인·현장 자격 |

DEMP 수치 선택·실제 힘 수지 계산·판 통과 경로 판정·재누르기를 이번 코드에 넣지 않았다. 50 kg를 면적 없이 300 MPa로 치환하거나 같은 N만으로 0.7/1 µm 비교를 정당화하지 않는다. 기존 ULPRI/T12R 한정 종결을 재개방하지 않는다.

## 6. 작성측 검증

| 검사 | 결과 | 해석 |
|---|---|---|
| 신규 fail-closed stub + 고정 suite | 25 메서드, assertion/subtest 실패42, 오류0, rc1 | 구현 전 red |
| 최종 후보 + 같은 suite | 25/25, 오류0, rc0 | 새 계약의 작은 합성 검증 |
| guard 약화 8종 | 8/8 검출, 오류0 | packet source·분모·parent checkpoint·물리시간·초기 부분집합·실패 시도·기대 음성·synthetic 증거 종류 |
| 고정 시험 신원 | red/green/8변이 동일 | 메서드·subtest·변이·반복을 합산하지 않음 |
| 원 의존 | 부모 Git blob/시험 bytes/worktree 9/9 일치 | 기존 q/T0/T11/LIVE/S0/P2와 fixture 보존 |
| process/network | audit hook을 source 실행 전에 설치, 시도0 | Python `-I -B`로 명시 suite만 실행 |

기존 suite 전체·full gate·실제 DEM·원자료·호스트·MPI·제출·운영 봉인은 수행하지 않았다. 외부 판정은 NOT_RECEIVED이며 작성측25/25·8변이를 외부 GO라고 쓰지 않는다.

최종 source SHA256: `b407782264018f0bf2ff704169ff6ef3f9da7c05a865278679daa16d4f950d77`.
고정 시험 SHA256: `ef659db192b8abc965c3dbfa7e070fd48a3a60b8093982b5921fdf0ab346192e`.
세부 순서·source 및 의존 SHA·변이별 관측은 `verification_summary.json`을 따른다.

## 7. 근거

- `63a513560c2770990920065be94ef966a8be018b:docs/reviews/nonrint_next_decisions_20261109.md` §1 — 실제 자격/등록/통합/DEMP·운영 GO의 별도 경계.
- 같은 핀 `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §5 T0–T14, §12 A3/A5 — T5/T11의 수치 등록과 실제 자격은 미정 유지.
- 같은 핀 `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §4/4.1/4.2 — 현재 source/시도/재개·단위·같은 물리시간·결손 분류.
- S0 핀 `f4647f2b7c218a6df7def3292c092273f9d4e35f`의 `docs/reviews/dem_s0_contract_20261110/README.md` §3–4 — 선언/typed bytes·opaque history·미지원 inter-object 물리 대조.
- 부모 P2 핀 `c571a27119ace92ca34d3d6f2b61135219a3f1b4`의 `scripts/dem_gen2_p2_contract.py` — 원 S0/LIVE 재검증과 native/분리 진단 API의 좁은 범위.
