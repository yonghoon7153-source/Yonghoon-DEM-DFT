# DEMP-01/02·같은 정적 상태 비교 — 선언·증거 계약 준비

**상태 1: 선언 메타 계약을 구현하고 최종 합성 시험 25/25와 가드 대조 8건을 확인했다. 실제 물리 자격·DEMP-01/02 종결·같은 정적 상태 확정은 0이며 전체 HOLD다.** 시험과 fail-closed 스텁을 구현보다 먼저 보존했고, 오류 없는 스텁 red 뒤 구현했다. 후속 단계 순서 반례도 구 소스 red를 남긴 뒤 수정했다.

## 1. 처리 범위와 근거

| 대상 | 이번 계약이 확인할 것 | 닫지 않는 것 |
|---|---|---|
| DEMP-01 | 단계별 전역 감쇠와 접촉 감쇠의 명시 정의·반력/중력/관성/힘·토크/KE 채널의 부호·단위·같은 창·재고 결속, 결손 보존 | 원자·접촉 자료에서 실제 힘 수지를 재계산, gamma/분모/허용폭 선택, 원 물리 결함 종결 |
| DEMP-02 | 고정 선언 ID/type/radius-definition/mass-definition 재고, 중심의 외부 표본과 구 표면 절단의 별도 기록, 중간 관측·누락·벽/이력 신원 | 실제 좌표·STL/PBC 교차 계산, 관측 사이 연속 궤적 인증, 판 관통 결함 종결 |
| D0.7/D1 같은 정적 상태 비교 | 같은 RA_END의 압력·면적·단위·창·이력·감쇠·재고/관측 연산자 **규약 전체**의 결속. N 동일은 요구하지 않음 | 실제 같은 정적 압력 상태 확정·측정값 비교·50 kg 하중 환산·재누르기 실행 |

바탕은 자격 행렬 `b7fbe749ea8ffa3151b3e768de445c572940c43d`의 `docs/reviews/dem_qualification_matrix_20261110/README.md`와 고정 P2 준비 `c571a27119ace92ca34d3d6f2b61135219a3f1b4`까지의 비활성 경계다. 리포의 고정 문서 근거는 다음과 같다.

| 고정 출처 | 경로·절 | 인용 범위 |
|---|---|---|
| B `13eb293cd9ac44502517c81e8f5e9b7ae02d817f` | `docs/reviews/dem_gen2_preparation_20261109/demp01_demp02_handling.md`의 DEMP-01·DEMP-02·S0/T12 인계 | 처리 요구의 문서 연결. 과거 실측/어림을 이번 문턱으로 추출하지 않음 |
| 같은 B | `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §3 T11-06·§4/4.1/4.2 | 단계·원 관측/경계·수지/정량 등록과 합성 계약의 분리 |
| 같은 B | `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §2·§12 | 고정판 R-a 끝, 단계 순서와 실제 자격 경계 |
| D-2 `3f81b6162` | `docs/reviews/dem_q3_prefill_20261110/README.md` §3 M3·M5·M7–M9 | 50kg/batch 과제 표지, 명목 DEM 크기와 실제 PSD 구분, 현행 실제 신원·정적 상태 UNKNOWN |
| B `13eb293cd9ac` | `docs/collab/claude_to_codex/20261109-2230_nonrint-first-link-sha-map.md` §2 | 비준 D9′: 순수 SE·300 MPa 가압+이완 끝·질량 기준 ε_sphere·TD 1.64·외부 10–13 %, ε_union 기록 전용 |

이번 DEMP 작성 및 시험 호출은 원 자료·원 로그·실제 덱·체크포인트·결과 JSON/CSV·호스트를 읽지 않았다. 이 범위 기록을 전체 대화의 문서 노출 여부로 확대하지 않는다. 앞 LIVE/S0/P2 계약의 해시·typed bytes가 실제 동시 물리 상태나 숨은 이력 자격이라는 주장을 하지 않는다. 닫힌 ULPRI/T12R·G2PREP 등 결함 범위를 재개방하지 않는다.

## 2. 권고안 전제

| 질문 | 권고 한 줄 | 실제 미정 칸 |
|---|---|---|
| 권고안 전제(Q-DEMP-1) | 7개 단계별 global/contact damping 정의와 signed 채널을 별도로 명시하고, 이번 합성 범위를 CASE_GLOBAL_DECLARATION의 서로 겹치지 않는 단계 창으로 한정 | 실제 gamma·단위/step 사상·수지 차분/기준점·분모·정적 허용폭·추가 유지 |
| 권고안 전제(Q-DEMP-2) | 중심 외부 분류와 구 표면 절단 분류를 별도 메타로 보존하고 전체 고정 선언 재고를 대조. 연속성은 항상 UNCONFIRMED | 실제 mesh/PBC/법선/연속 경로·표본주기·기하 허용폭·검출 자격 |
| 권고안 전제(Q-DEMP-3) | 50kg/batch 표지는 하중으로 환산하지 않고 D0.7/D1을 같은 RA_END 규약으로 비교하도록 등록 후보 명부를 결속 | 정확 batch 의미·압력/면적·실제 표본/쌍·상태/endpoint·불확실성·승인 |

이 전제는 권고안으로 이름 붙인 **문서/합성 준비 선택**이다. 실제 값·물리 수지·형상 계산을 만들지 않는다. 과거 감쇠 어림이나 인용된 반력 비율을 허용 문턱으로 넣지 않는다. 50 kg를 압축 질량·힘·300 MPa의 변환 입력으로 취급하지 않는다. D9′는 이미 정한 정책이므로 다시 비준을 묻지 않는다.

## 3. API와 자료 종류

```python
validate_demp_contract(plan, packets, context) -> report
```

입력은 source 파일·물리 관측값이 아니라 **작성자가 제공한 합성 선언 메타**다. source hash는 논리 결속에만 쓰며 파일을 읽거나 진위를 인증하지 않는다. force/pressure/position/actual-result payload를 받는 경로는 제안하지 않는다. 새 힘 수지 계산기·기하 판독기·원 로그 reader를 구현하는 작업이 아니다.

`plan`은 native schema/purpose, Q-DEMP-1–3, plan ID/판, source manifest, 역사 표지, 고정 D9′ 정책, 7개 stage plan, 2개 diameter case, 비교 규약, 기하 메타 규약, 실제 facts의 null 칸을 갖는다. source manifest의 qualification-matrix pin은 `b7fbe749ea8ffa3151b3e768de445c572940c43d`로 첫 red 전에 고정했다. 이전 행렬의 물리 자격 상태를 받아 승격시키지 않으며 이 선언 pin이 이전 API의 재실행·진위 확인을 대신하지 않는다.

`context`는 별도 기대 plan SHA와 동일 source pin, 합성 freeze/evidence 순번이다. 고정 기대 hash가 유지된 동안 plan만 바꾸는 경우를 거부한다. context까지 함께 바꾸지 못한다는 trust anchor·벽시계·실제 사전등록 인증은 없다. canonical JSON은 exact built-in 자료, 정렬 key, UTF-8, compact separators 규약이다. float·NaN·하위형·순환 구조는 받지 않는다. key 타입은 set/hash/equality 전에 확인한다. 지원 범위는 case 2개·stage 7개·재고 1–256개·창당 frame 1–32개·token 1–128자·0 이상 정수 step 10^9 이하인 작은 합성 메타다. 이 상한은 물리 등록값이 아니다.

## 4. DEMP-01: 단계와 채널을 먼저 분리

고정 단계 목록은 INSERTION·STABILIZATION·COMPRESSION·SERVO·RA_END·UNLOADING·POST_SEPARATION의 7개다. 각 단계는 `EXPLICIT_STAGE` global damping 정의와 contact damping 정의, 별도 model/definition ID, signed vector 표현, force/torque/energy/gamma 단위 ID를 갖는다. 준비 stage의 전역 감쇠를 압축에 자동 상속하는 정책은 거부한다. 같은 선언값을 쓰려면 각 stage에 명시해야 하며 수치 자체는 이번에 받지 않는다.

필수 채널은 plate_reaction·global_damping·contact_damping·gravity·inertia·force_balance·torque_balance·translational_ke·rotational_ke다. 앞 7개는 signed vector component 규약, KE 두 개는 scalar definition이다. 접촉 감쇠를 전역 감쇠라는 같은 역할/모델로 합치거나 abs magnitude로 부호를 지우는 선언은 거부한다.

채널마다 동일 run/attempt/stage/window/frame 목록/step 범위/inventory ID와 정확 unit/role을 대조한다. `source_kind=SYNTHETIC_METADATA_ONLY`, `value_access=NOT_READ`만 지원한다. 실제 숫자 `value`를 더하거나 `PHYSICAL_BALANCE_VERIFIED`로 표시하는 것을 금지한다. 채널 신원이 일치해도 전역 감쇠가 반력의 얼마인지 계산한 것이 아니며 `demp01_closed=false`다.

권고안 전제(Q-DEMP-1)의 step 범위는 **CASE_GLOBAL_DECLARATION**이다. 같은 case 안에서 현재 PRESENT인 창만 고정 단계 순서대로 대조하고, 뒤 창의 start가 앞 창의 end보다 커야 한다. absent/MISSING/FAILED/PARTIAL 단계는 창을 발명하지 않으며 남은 PRESENT 창 사이 순서를 확인한 뒤 전체 INCOMPLETE와 예정 분모를 유지한다. 각 창 안 step은 연속 선언 frame과 정확히 대응한다. 이 추가 가정은 문서로 고정한 이번 API의 좁은 지원 범위이며 별도 plan 필드나 실제 엔진 step 변환기가 아니다. 실제 stage-local step·reset_timestep 자료를 일반적으로 틀렸다고 판정하지 않는다. 실제 engine-to-case-global 사상은 미확정이다.

현재 LIVE의 residual/gravity/damping/inertia는 입력 채널이다. 이 계약도 그 채널의 선언을 정리하는 범위이며 `−γΣv`, 힘/토크 잔차, 운동량 차분이나 접촉 항을 새로 계산하지 않는다. 실제 물리 모델·단위·이력·수지 예산이 등록되고 별도 관측/반박 검토가 있어야 원 지적을 닫을 수 있다.

## 5. DEMP-02: 재고·표면·중심·연속성의 분리

각 case의 선언 재고는 고유 양의 exact integer ID/type, radius-definition ID, mass-definition ID다. packet마다 전체 목록과 case별 mesh/wall/history ID를 대조한다. 개수만 같고 ID/type/mass/radius 정의가 바뀌거나 한 입자가 빠진 경우를 숨기지 않는다. 이는 선언 재고 비교이며 실제 입자 질량·반경을 읽은 것이 아니다.

geometry packet은 `DECLARED_CLASSIFICATION_ONLY`다. 각 예정 frame의 center_region(INSIDE/OUTSIDE/UNKNOWN)과 sphere_relation(UNCUT/CUT/UNKNOWN)을 따로 받는다. 주어진 label의 개수와 claim의 일관성만 확인한다. 실제 x/y/z/radius·삼각형·PBC·교차식은 입력이나 계산 대상이 아니다.

- 중심 INSIDE·구 표면 CUT은 중심 통과와 다른 메타다. surface-cut toy 계획도 구조상 수용할 수 있지만 물리 결함이 없다는 판정은 아니다.
- 시작과 끝 INSIDE라도 중간 OUTSIDE label이 있으면 `center_outside_claim=NONE_RECORDED`는 모순이다. SAMPLE_RECORDED로 보존한 packet은 음성 증거 메타로 일관될 수 있다.
- frame 결손/UNKNOWN을 INSIDE나 UNCUT으로 보충하지 않는다. 잘못된 sequence·다른 창 자료를 같은 경로로 묶지 않는다.
- 모든 표본이 INSIDE여도 실제 사이 경로는 모른다. `continuity=CONTINUITY_UNCONFIRMED`를 강제하며 PROVEN_NO_CROSSING·ACTUAL_STL_PBC_QUALIFIED는 미지원이다.

`center_outside_samples`와 `sphere_cut_samples`는 **제공된 합성 분류 label 행 수**다. per-particle 기하·궤적을 재계산한 값, 실제 접촉/관통 검출 횟수나 누적 물리 결과가 아니다. 분류 행과 선언 입자 재고의 물리 대응 자체도 인증하지 않는다. 모든 반환의 `demp02_closed=false`, 실제 mesh/연속 궤적 자격 NOT_RUN을 유지한다.

## 6. 같은 정적 상태의 D0.7/D1 비교 명부

리포 근거에서 50kg/batch는 과제 제목이다. 정확 사업/장치 의미는 UNKNOWN이며 압축 하중 환산은 NOT_ESTABLISHED다. 실제 압축 규약은 별도로 받아야 한다. 명목 DEM 단일 구 직경 0.7/1 µm 표지와 실험 D50/실제 PSD를 같은 신원으로 인증하지 않는다.

두 case는 같은 recipe 정의와 RA_END의 pressure-definition·area-definition·units-definition·window-definition·history-policy·damping-policy·inventory-operator·metric-operator 전체를 선언해야 한다. 이름 `same_toy_load_name`이 같다는 것만으로 비교 가능하지 않으며, 위 규약 중 하나가 다르면 같은 상태 계획으로 받지 않는다. RA_END packet에도 그 전체 state contract가 있어야 한다. 압축 첫 힘 도달·다른 단계 packet을 RA_END 대신 사용하지 않는다.

case별 run/attempt/bed/arm·판/벽/이력과 재고는 서로 다를 수 있다. 각각 자기 case의 선언과 일치해야 한다. 서로 같은 물리 입자 ID나 N을 요구하지 않는다. 정상 fixture는 D0.7의 선언 입자 2개, D1의 3개로 **N 불일치가 비교 준비의 실패 사유가 아님**을 검사한다. 실제 명부·표본 대응·실제 같은 압력 상태를 확정한 것이 아니므로 `actual_state_comparable=false`다.

재누르기는 gen2 프로토콜에 합친 비교 요구로 남는다. 이번 packet을 실제 재실행 명령·결과·하중 전환 계산으로 사용하지 않는다.

## 7. 분모·결손·상태

예정 packet은 2 case×7 stage=14개다. 각각 case ID/stage/status/payload/failure code를 가지며 별도 작성자 PASS·rc0 보고서가 원 메타를 대신하지 못한다. 같은 case/stage 중복·예정 외 case·다른 stage로 치환은 거부한다.

| 상태 | 예정 분모 처리 | 의미 |
|---|---|---|
| PRESENT | 전체 payload 대조 후 complete 1 | 메타 구조만 완전 |
| absent 또는 MISSING | missing 1, planned 유지 | 누락을 조용히 제외하지 않음 |
| FAILED | failed 1, planned 유지 | 실패의 기대/성공 승격 없음 |
| PARTIAL | partial 1, planned 유지 | 정상 부분표로 완료를 만들지 않음 |
| PRESENT 안 필수 채널/관측 결손 | NOT_COMPUTED | 0값·옛 stage·PASS 문자열로 보충 금지 |
| 신원·정의·형식 모순 | REJECTED | 실제 음성 물리 결과와 구조 파손을 구분 |

완전한 최대 반환은 `SYNTHETIC_DEMP_CONTRACT_CONSISTENT`다. 그때도 실제 자격 NOT_RUN, registration/source-auth/physical/GO/gate/DEMP-01/02 종결/actual-state-comparable은 false, 연구 결과 0, 전체 HOLD다. 원장 직접 변경·verified 승격·운영 봉인은 없다.

## 8. 시험 먼저 — 원 기록과 후속 보강

스테이징 시험 24개를 먼저 작성하고 항상 REJECTED를 반환하는 스텁을 뒤이어 보존했다. 구현 본문은 오류 없는 실제 스텁 red를 기록한 뒤 작성했다. 스텁 red는 새 기능의 양성 계약이 아직 구현되지 않았음을 보이는 기준선이며 과거 운영 소스 결함의 재현이 아니다. 스텁이 음성을 거부한 사실만을 방어 구현 증거로 세지 않는다.

| 순서 | 메서드·실패·오류·rc | 정확한 의미 |
|---|---|---|
| 초기 준비 중단 | 0·해당 없음·해당 없음·준비 실패 | sparse worktree의 scripts 폴더 누락으로 복사와 harness source read가 중단. 프로젝트 실행 전이며 원 stderr는 도구 대화에만 남고 별도 파일은 미보존 |
| 고정 시험 + 스텁 red | 24·14·0·1 | stub red2. 구현 전 양성 assertion 실패 |
| 첫 구현 green | 24·0·0·0 | 같은 24개 시험 바이트로 통과 |
| 첫 가드 대조 | 7개 변이군, 각각 24개 | 7/7 검출·오류 0. 첫 구현 기준이며 최종 증거와 합산하지 않음 |
| 단계 순서 추가 red | 25·2·0·1 | 첫 구현은 그대로. 일반 fixture의 stage-local 창을 case-global 창으로 정규화하고 1개 반례 메서드 추가. SERVO가 역행하거나 COMPRESSION과 겹치는 self-consistent 메타 두 subtest가 실패 |
| 최종 green | 25·0·0·0 | 같은 25개 시험에서 최소 순서 가드 통과 |
| 최종 가드 대조 | 8개 변이군, 각각 25개 | 8/8 검출·오류 0. 기존 7개 및 새 순서 가드 대조 |

초기 24개 fixture는 모든 단계에 local 0–2를 사용했다. 후속 25개는 case별 0–2, 3–5, …, 18–20의 전역 선언 창을 사용한다. 첫 green을 CASE_GLOBAL 검증으로 소급하지 않는다. 새 반례는 source/schema 변경 전 관측했으며, 새 스키마 필드 때문에 모든 양성이 거부된 결과가 아니다.

| 시험 | 독립 메타 기대 |
|---|---|
| 01–03 | 무절단/표면절단 두 계획, N 2/3, 예정 14 packet, 결손/실패/부분 분모 유지 |
| 04–08 | stage·자동 상속·global/contact 혼합·abs·채널 결손/frame/unit·실제 수지 값/권한 거부 |
| 09–14 | 같은 N의 다른 재고·손실·중복, center/surface 분리, 중간 OUTSIDE·누락·old attempt/wall/history |
| 15–20 | 같은 하중 이름의 다른 RA_END 규약, 다른 endpoint·N 강제·50 kg 환산·PSD 오인·D9′ 변경 거부 |
| 21–24 | 외부 plan 기대 hash·선언 순서·pin·PASS 대체·입력 보존·exact type/key hook |
| 25 | 모든 내부 binding이 일치해도 같은 case의 stage 창 역행·겹침은 거부 |

| 최종 변이군 | 실패 / 오류 | 한정 |
|---|---|---|
| 예정 분모 축소 | 1 / 0 | 누락을 예정 집합에서 빼는 변이 |
| explicit stage 감쇠 검사 제거 | 1 / 0 | 상속 금지 대조 |
| signed channel 표현 검사 제거 | 1 / 0 | abs 선언 대조 |
| 전체 선언 재고 검사 제거 | 6 / 0 | type/ID/정의/손실 대조 포함 |
| 분류 label claim 검사 제거 | 1 / 0 | 주어진 분류 행과 claim 대조 |
| 같은 정적 상태 검사 2곳 제거 | 8 / 0 | 한 변이군에서 case·packet의 두 대조를 제거 |
| 외부 plan SHA 검사 제거 | 1 / 0 | 고정 context에 대한 plan 변경 대조 |
| case-global 단계 순서 검사 제거 | 2 / 0 | 새 역행·겹침 두 subtest |

Windows Python 3.12.14의 -I -B에서 명시한 작은 합성 suite만 실행했다. harness/변이 runner는 프로젝트 코드를 실행하기 전에 process/network audit 차단을 설치했다. 각 호출의 외부 process/network 시도 0, engine 0, 실제 원자료·원 로그 조회 0이다. 전체 gate·기존 자격 suite·현장 자격을 실행하지 않았다. 메서드 수·subtest 실패 수·변이 수·전후 반복은 새 고유 시험 수로 합산하지 않는다.

## 9. 고정 바이트·재현·남은 단계

최종 소스 SHA256: `7490b921d8015d237c52f18461cddb97bd8d373637f95107056309d309a18639`.

최종 시험 SHA256: `e399ac13ab6c5fd9f3e6eb56a61725adad38d391feace7c9446d5d5483a5fd12`.

`verification_summary.json`은 각 단계의 시각·해시·rc·오류와 최종 가드 대조를 구분한다. 원 증거는 검토 묶음의 raw 영역에 들어가며 그 raw_manifest가 스텁/첫 구현/최종 소스·시험·로그·준비 원본·harness·변이본을 결속한다. 최초 준비 중단의 원 stderr 파일은 없으므로 사후 설명 영수증으로 구분한다. 이 기록은 독립 반박 검토 판정이 아니다.

고정 source/test를 별도 복사본에 두고 검토용 runner가 audit를 먼저 설치한 뒤 같은 suite를 실행할 수 있다. 운영 엔진·scheduler·호스트·원자료 경로가 필요하지 않다. 파일 자체를 읽어 검토하는 것과 프로젝트 코드를 실제 연구에 실행하는 권한은 별개다.

다음은 이 메타 계약의 반박 창 한정 검토다. 실제 DEMP-01의 물리 수지 계산/등록과 DEMP-02의 mesh·PBC·연속 궤적 자격, 실제 같은 압력 상태 비교·하중 의미 확정은 별도 고정안·허가·증거가 필요하다. P2/행렬/기존 봉인을 바꾸거나 실제 등록·실행·원장 처분을 자동 진행하지 않는다.
