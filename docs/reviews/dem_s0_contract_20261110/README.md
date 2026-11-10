# DEM 세대 2 S0 — 합성 경계·바이트 계약 준비

**상태 2: 작성측 합성 22/22·가드 제거 대조 8/8 검출·전체 HOLD.** 실제 원자/접촉/로그/restart 자료·엔진·호스트를 읽거나 실행하지 않았다. `actual_T0/T11/T12=NOT_RUN`, 실제 S0 없음, 등록 미완료, 연구 결과0이다. 실제 시험 기록은 `verification_summary.json`에 구분했다. 독립 검토는 아직 받지 않았다.

## 1. 작성 순서의 사실

S0 구현 초안 `scripts/dem_gen2_s0_contract.py`는 root의 시험→stub red→구현 순서 정정 지시 **직전에 scratch에 먼저 작성됐다**. 이 사실을 보고했고, 파일을 삭제·숨김·덮어쓰기하지 않았다. 정정 뒤 구현 본문 보완은 중지했다. 이어서 시험·fixture와 별도 `baseline/scripts/dem_gen2_s0_contract.py` fail-closed scaffold를 작성했다. 그 뒤 고정 suite의 stub red와 선작성 초안 첫 실행을 수행했다. 첫 초안이22/22였고 후보 코드 보완은0이다.

그러므로 향후 stub red/green을 얻더라도 이 초안 전체를 처음부터 엄밀한 test-first로 작성했다고 기록하면 안 된다. stub은 API 부재 import 오류 대신 실제 fail-closed 반환을 제공한다. 그 red는 미구현 API와 새 명시 계약의 차이를 보여줄 뿐, 과거 코드의 물리 반례 또는 실제 S0 결함 재현은 아니다. LIVE 부모 `63a513560c2770990920065be94ef966a8be018b`의 의존 blob을 대조했다. 이후 새 연결은 시험→stub red→구현 순서를 지킨다.

## 2. 범위와 권고안 전제

| 질문 | 권고 한 줄 | 남는 한정 |
|---|---|---|
| Q-S0-1 | **권고안 전제(Q-S0-1):** LIVE 원 plan·servo/R-a trace를 다시 검증하고 전체 R-a 끝 candidate와 여섯 객체를 결속 | 실제 live reader·실행 당시 신원 인증·숨은 접촉 이력 자격은 없음 |
| Q-S0-2 | **권고안 전제(Q-S0-2):** typed envelope를 canonical UTF-8 JSON bytes로 검증·직렬화·역직렬화 | 파일 저장/덮어쓰기/예약/운영 봉인 기능 없음 |

근거는 `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §4/4.1/4.2/5, `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §2-5/2-6, `c5ebaa71298691020313e272b39c0a80b51cdc4d:docs/reviews/dem_gen2_t12_consumer_contract_20261024.md` §2/3이다. P1 고정 `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`의 atom16/pair26/wall 형태는 역사 계약 근거이며 실제 P2 semantic mapping 등록이 아니다. 옛 ULPRI 수령 상태를 재개방하지 않는다.

LIVE 의존은 `dem_gen2_live_contract.diagnose_live_ra(plan, servo_frames, ra_frames)`라는 부모 `63a513560c2770990920065be94ef966a8be018b`에 고정된 API다. 이 준비표를 LIVE 검증 완료 증거로 쓰지 않는다. API가 `SYNTHETIC_RA_END_CANDIDATE`를 반환할 때만 `boundary_candidate`를 사용한다. caller가 준 status 문자열은 입력으로 수용하지 않는다.

## 3. 계약과 API

```python
validate_s0_envelope(contract, envelope, live_plan, servo_frames, ra_frames) -> report
serialize_s0(contract, envelope, live_plan, servo_frames, ra_frames) -> bytes
decode_s0(data, contract, live_plan, servo_frames, ra_frames) -> envelope
```

검증 성공은 `SYNTHETIC_S0_CONSISTENT`라는 선언/바이트 일관성일 뿐이다. 필수 자료 누락은 `NOT_COMPUTED`, 선언 불일치·파싱·기술 위반은 `REJECTED`, 실패 시 부분 객체 수용0이다. serialize/decode는 잘못된 자료에 `ValueError`를 내며 저장하지 않는다. 모든 결과는 권한 false·실제 S0 null·실제 T0/T11/T12 미수행을 유지한다.

LIVE candidate 전체를 canonical bytes로 대조한다: stage/boundary, run/bed/arm/attempt/definition/unit 신원, T0 identity와 packet/T11 hash·case/grid, 끝 step/sample/tick/window, 판 position/velocity와 mesh/wall/history, 기준 재고, 계획/servo/R-a/end-frame hash. 같은 step이나 상태 문자열 하나만 비교하지 않는다. 독립적으로 보존한 `contract.boundary_sha256`도 대조한다. hash·논리 identity는 byte/declaration consistency이며 실제 출처 진위 인증은 아니다.

여섯 객체 순서는 atom→pair→wall→mesh→restart→state다. 각각 role/revision·boundary hash·끝 step·mesh/wall/history/inventory ID·생성 순번·직전 객체 hash·media/column/unit/semantic mapping·base64 payload·실제 byte 길이/SHA를 가진다. atom의 부모는 boundary hash, 이후는 직전 객체 전체 canonical hash다. 잘못된 첫 프레임을 다른 파일로 자동 대체하지 않는다.

### atom과 기준 재고

필수16열은 `id type x y z radius mass vx vy vz omegax omegay omegaz fx fy fz`다. 모두 명시·유한 내장 숫자여야 하고 id/type는 양의 exact int, ID는 고유하다. type/radius/mass를 R-a candidate의 기준 재고 전체와 대조한다. 좌표나 N만 같다고 수용하지 않는다. omega를0으로 보충하지 않는다. 초기 지원은 정확16열이며 추가열 사상은 미지원이다.

### pair26과 wall U/R

pair는 `c_cpl[1]`–`c_cpl[26]` 순서를 요구하고, units/meanings와 semantic mapping digest를 명시된 reference와 대조한다. `[23]`의 뜻은 `current_overlap`이어야 하며 숨은 delta_max/shear 동일성이라고 주장할 수 없다.

wall U는 `mesh tri id fnx fny fnz`, R은 추가 `delta_max shear_x shear_y shear_z`라는 **합성 typed profile**이다. R의 이름을 실제 엔진 출력 열 이름이나 실제 hidden-state 복원으로 인증하지 않는다. `WALL_U/WALL_R`를 명시하며 서로 자동 변환하지 않는다. 선언된 mapping reference와 그 hash는 자기 신고의 일관성을 묶는 것이고 mapping 진위·실제 물리 단위를 인증하지 않는다.

시험 fixture의 pair/wall `declared_unit_XX`·`declared_slot_XX`는 의도적인 가짜 사상이다. 이 dummy 값을 P2 등록 수치/단위/의미로 반입할 권한은 없다. 유일하게 고정한 겹침 한정은 `[23] current_overlap`과 hidden-history 자격 false다.

mesh/restart/state는 opaque 합성 bytes다. 해시가 같다는 것만 확인하며 실제 binary가 상태/이력을 보존했다는 주장은 하지 않는다.

**미수행 범위:** pair rows는 유한26열과 명시된 선언 사상만 검사하며 빈 목록도 허용한다. pair의 물리 ID 의미 해석, LIVE contact count와 pair/wall 행 수의 일치, atom의 힘·속도·omega에서 LIVE 힘/에너지 채널을 재계산하는 검사는 하지 않았다. 따라서 여섯 객체의 선언/바이트 결속은 물리적으로 동시 관측된 상태의 인증이 아니다. 이 의미·수지·채널 교차 대조와 실제 숨은 이력은 후속 T12 적격성이 미완료인 항목으로 남긴다.


## 4. 바이트 규약

canonical JSON은 keys 정렬·array 순서 보존·compact separators·`ensure_ascii=False`·`allow_nan=False`·UTF-8다. outer archive는 `schema/body/body_bytes/body_sha256`이고 self-hash는 body만 대상으로 하므로 순환하지 않는다. atom/pair/wall의 inner JSON payload도 같은 규약이다.

- duplicate JSON key, NaN/Infinity, 비canonical whitespace/표현, unknown field/actual GO 키 거부.
- exact built-in 자료만 허용하며 하위형 변환 hook을 호출하지 않음.
- base64는 alphabet/padding/pad bits를 포함해 encode(decode(x))==x를 요구.
- 실제 제공 payload bytes의 길이와 SHA256을 재계산. caller hash를 그대로 신뢰하지 않음.
- payload당65,536B, 전체 archive1,048,576B, atom256개/contact1024행의 좁은 합성 예산. 실제 큰 frame·engine 자격이나 성능 보증이 아님.

## 5. 작성측 합성 확인 — 22개 메서드

`scripts/test_dem_gen2_s0_contract.py`에 22개 시험 메서드를 작성했다. LIVE의 고정 `fixture(sign=1, grid_choice='coarse', delay=0)`가 만드는 작은 가상 trace만 사용했다. 실제 자료 reader는 없다. 새 suite가 source로 읽는 것은 테스트/계약 모듈뿐이다. 각 실행은 `-I -B`와 프로젝트 source 실행 전 audit hook을 사용했다. 10회 invocation에서 process/network 시도0이며 기존 LIVE/T11 전체 suite는 반복하지 않았다.

| 시험 | 확인할 반례/대조 |
|---|---|
| 01–02 | 여섯 객체 U/R 양성, 독립 canonical bytes와 encode→decode→encode 동일성 |
| 03–06 | LIVE 원inputs 재검증, R-a 예산 미완료, 전체 candidate 필드/hash 변이, 새로운 dt/2 boundary의 old hash 재사용 거부 |
| 07–08 | 객체별 step/history/inventory/mesh, 역할 개수·순서·ordinal·parent 결속 |
| 09–11 | 같은 좌표/N의 mass/type/radius 변이, omega/16열 누락, 소수/bool/중복/새/누락 atom ID |
| 12–14 | pair 이름/순서/unit/mapping/폭, current overlap의 hidden-history 승격 거부, wall U/R 혼합 |
| 15–18 | opaque bytes 길이/SHA, 비canonical base64, 내부/외부 duplicate key·NaN·비canonical JSON·body hash |
| 19–22 | decoder 원inputs 재검증·actual/unknown 키, 작은 byte 예산, 하위형 hook0, 입력 무변경·부분 수용0 |

메서드 수·subtest 수·바이트 변이·LIVE/T0/T11 호출을 합산해 고유 시험 수로 만들지 않는다. 무조건 거부하는 stub의 음성 통과를 실제 가드 구현의 입증으로 보지 않는다. stub red는22메서드·실패82·오류1·rc1이다. 오류1은 양성 serialize 요청의 명시적 NOT_IMPLEMENTED ValueError이며 import 오류·과거 물리 오류가 아니다. 선작성 초안 첫 실행은22/22·rc0이며 이후 후보 바이트가 같아 그 관측을 최종 green으로 결속했다. 독립 검토 결과는 아직 없다.

## 6. 가드 대조·원시 근거와 다음

| 제거한 가드 | 실패 관측 | 오류 | 처분 |
|---|---:|---:|---|
| LIVE 원inputs 재검증 | 3 | 0 | 검출 |
| frozen boundary | 1 | 0 | 검출 |
| atom 전체 재고 | 5 | 0 | 검출 |
| payload digest | 4 | 0 | 검출 |
| current overlap 의미 | 1 | 0 | 검출 |
| canonical JSON | 2 | 0 | 검출 |
| canonical base64 | 1 | 0 | 검출 |
| parent chain | 2 | 0 | 검출 |

모든 대조는 같은 고정22메서드를 사용했고 rc1·오류0이다. 위 실패 수는 subtest/assertion 관측이며 새로운 고유 시험 수가 아니다. 각 변이의 정확 source SHA는 `verification_summary.json`에 있다.

증거 묶음의 `red/`, `draft_observation/`, `contrasts/`에 source 사본·report/test/stdout/stderr를 남겼다. `final_raw_evidence_manifest.json`이 준비 helper·보존 staging·runner·최종 문서·후보/변이 소스·원시 로그 전체를 결속한다. manifest 자체는 self-hash 순환 때문에 그 목록에서 제외한다.

준비 중단1회는 source를 옮기는 메타 helper의 상위 폴더 지정 착오였다. 프로젝트 import/시험0인 상태에서 멈췄다. 원 stderr는 tool 출력에만 있었고 별도 원본 파일로 저장하지 못했다. `s0_preparation_attempt01.txt`는 그 관찰 기록이지 원 stderr 복제본이 아니다. 이 한계를 숨기거나 본안 시험 실패로 합산하지 않는다.

S0 source SHA=`4d3d5827a1f4bb5bf0f6a894f72249ba1c60e0d0677ffd5d01bb6c68d3a7721d`, fixed test SHA=`6de7ad2fee12e959df6653116939cca517cbf5e96a225e1bd350e2cbe23c1c17`.

다음은 고정 핀·인계/반박 검토다. 실제 엔진의 atom/pair/wall semantic mapping·hidden history·재개·T12·원자료·실행 GO는 미수행 그대로다. Rint·봉인32·원장·실제 파일·운영 봉인은 변경하지 않는다.
