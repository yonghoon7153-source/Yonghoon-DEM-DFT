# D-3 / T0 고정 계약 — 합성 계획·대조 자료 결속 후보

**권고안 전제(Q-T0-1)·권고안 전제(Q-T0-2).** 실제 T0 수행·극성 확정·바이너리 문법 자격은0, 연구 결과0, 전체 HOLD다. 이번 후보는 선언된 **합성 자료 묶음의 일관성**만 검사한다. 외부 반박 판정은 PENDING이다.

| 질문 | 권고 한 줄 | 이 후보의 전제/남는 결정 |
|---|---|---|
| Q-T0-1 | build·소스 핀·덱/fixture·단위·run/attempt·판 성분을 한 묶음으로 고정하고 압축 정상·반대 부호 음성·zero의 세 역할을 대조한다. | **권고안 전제(Q-T0-1)**. 실물 fixture나 실제 빌드가 이미 선택/수행됐다는 뜻 아님 |
| Q-T0-2 | 기존 생성기의 명시 단위 사상을 합성 선언 산술로 대조하되 실제 T0 영수증과 실제 압축 극성은 별도 비준/현장 자격에 남긴다. | **권고안 전제(Q-T0-2)**. 실제 unit/build/receipt 자격 NOT_RUN, actual sign/build는 null |

## 1. 근거와 새 범위

| 근거 | 경로·절 | 이번에 따르는 범위 |
|---|---|---|
| 시작 B `13eb293cd9ac44502517c81e8f5e9b7ae02d817f` | `docs/reviews/nonrint_next_decisions_20261109.md` §1 T0 | 지정 build/deck/작은 fixture·단위·raw 반력/압축 부호의 기대 관계와 양/음 대조를 먼저 고정 |
| 같은 B 정본 | `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §5 T0·§12 | T0의20입자 fixture는 문법/부호/단위 계획. T0 문법 통과와 dt·물리 자격 분리 |
| 같은 B | `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §1·§4–5 | T0·정량 등록·실제 관측·P2 완결을 구분. gate 정지 유지 |
| 바로 앞 D-2 `3f81b6162838c3453f3df806a2b0d176ae2c887b` | `docs/reviews/dem_q3_prefill_20261110/README.md` | 리포의 역사/선언 메타와 향후 실제 지정 build·T0 영수증을 구분. 이 커밋 위 새 가지 |
| 현재 생성기/함수 | `scripts/make_dem_gen2_decks.py`의 `bundle` 내부 `capture_line/capture`; `scripts/dem_gen2_qualification.py`의 `number`, `integer`, `target_force` | 기존 raw freeze→같은 sample의 sign 곱→음수 TECH_HOLD와 실제 극성null을 보존. 새 module은 기존 유한성/정수/단위 산술만 재사용 |

기존 생성기18시험은 이미 raw 반력 보존·반대 부호 거부·exact ±1을 다룬다. 이를 새 결함/새 성과로 중복 계상하지 않는다. `target_force`의 scalar 산술은 실행 당시 build/deck/fixture의 신원을 인증하는 API가 아니었으며, 새 결속을 그 과거 결함으로 소급하지 않는다.

새 파일은 `scripts/dem_gen2_t0_contract.py`, 시험은 `scripts/test_dem_gen2_t0_contract.py`다. 기존 qualification/생성기·입구/단계 gate·봉인32·Rint·원장·운영 봉인은 고치지 않는다. **권고안 전제(Q-T0-1/2)**의 순수 함수 하나이고 CLI·파일 reader·호스트/프로세스/네트워크·실제 명령 기능은 없다.

## 2. 입력 계약 — 권고안 전제(Q-T0-1)

`validate_t0_contract(plan, cases)`는 정확한 내장 dict/list와 명시한 내장 scalar만 받는다. 지원 외 하위형·Mapping은 형식 범위에서 거부하며 변환/표현 hook으로 정상화하지 않는다. 입력/전역을 임의로 수정할 수 있는 Python 호출자에 대한 보안 sandbox는 아니다.

| 부분 | 고정 필드/의미 | 거부 조건 |
|---|---|---|
| 머리 | schema=`DEM_GEN2_T0_SYNTHETIC_CONTRACT_V1`, purpose=`SYNTHETIC_PREPARATION`, protocol=`P2` | 과거 P1·PRODUCTION·알 수 없는 필드/actual receipt 입력 |
| 신원 | build_alias, producer_pin/qualification_pin(40자 lowercase SHA 형식), deck_sha256/fixture_sha256(64자), unit_mapping_id, run_id, attempt_id, mesh_id, reaction_component | 누락/다른 형식·세 대조의 신원 하나라도 plan과 다름. 해시 문자열 형식 통과는 원 바이트/실제 사용/승인 진위 검증 아님 |
| 판·성분 | 기존 synthetic 생성기의 top_mesh·z 성분만 | 다른 mesh/축을 같은 숫자라고 허용하지 않음. 실제 f_top_mesh[3] 극성 자격은 미수행 |
| fixture | 선언 particle_count=20, 명시 compression_sign=-1 또는+1, 합성 pressure/area/target | 20은 계획표지이며 실제 입자 명부·침대/접촉 수 검사가 아님. sign은 exact int로 선언하며 zero에서 추정하지 않음 |
| 표본 계획 | 양의 exact int first_sample_id·sample_stride | 각 행 sample_id가 순서/간격과 다름, 중복·결손·추가·재정렬 |
| 세 역할 | compression_positive → opposite_polarity_negative → zero_control의 정확 세 행 | 순서·역할 교체/중복, expected_accept 같은 자기 신고 승인 필드 |
| 각 행 | 같은 신원, 역할/sample_id, raw_reaction, normalized_force | NaN/Inf/지원 외 숫자·normalized≠sign×같은 raw·역할의 기대 부호 불충족 |

별칭은 ASCII 영문자로 시작하는 최대128자의 영문/숫자/underscore/hyphen이다. 신원은 **서로 같은 선언인지** 대조할 뿐 진짜 원천을 인증하지 않는다. 모든 신원을 함께 잘못 붙여도 실제 실행 증명으로 승격하지 않으며, 물리 자격/실행 권한은 어떤 입력에서도 false다. 같은 sample 표지 역시 원천 추적의 실제 영수증을 대신하지 않는다.

## 3. 단위·판정 — 권고안 전제(Q-T0-2)

지원 사상은 `GEN2_MPA_DECK_STRESS_0P001_V1` 하나다. 기존 `target_force`의 `pressure_mpa × area_deck_m2 × 1000`을 선언 target과 대조한다(physical MPa→Pa→deck stress scale0.001). 임의 multiplier를 받아 오류를 흡수하지 않는다. 내장 숫자 표현의 같은 연산 결과를 **exact equality**로 비교하며 실제 관측의 오차폭/허용오차를 정한 것이 아니다. 합성 예의2 MPa·면적0.001·target2는 toy 산술이며, 비준된 실제300 MPa 정책을 바꾸거나 실제 달성 압력을 보고하지 않는다.

| 결과 | 뜻 | 실제 자격/권한 |
|---|---|---|
| `REJECTED / INVALID_SYNTHETIC_PLAN` | 선언 형식·범위·단위 사상·target·계획이 미충족 | 모든 권한false; 부분 일관성 결과0 |
| `REJECTED / INVALID_SYNTHETIC_CONTROLS` | 세 대조의 신원·시점·부호·정규화가 미충족 | 입력은 그대로. 좋은 두 행만 떼어 완료 처리하지 않음 |
| `SYNTHETIC_T0_CONTRACT_CONSISTENT / DIAGNOSTIC_ONLY` | 정상 압축 양수·반대 부호 음성 검출·zero 비결정 대조까지 합성 선언과 일치 | `actual_T0=NOT_RUN`, `actual_compression_sign=null`, `actual_build_identity=null`, `binary_syntax=NOT_RUN`, physical_ready/execution_go/gate_write/operational_seal_modified=false |

압축 정상 역할은 정규화 힘이 양수라는 뜻이며 target 달성·정적300 MPa·수렴·교정 성공을 뜻하지 않는다. 반대 부호 역할은 반드시 음성으로 검출돼야 한다. zero 역할은 부호를 결정할 정보가 아니다. 토큰/해시·표본 수를 인증 권한으로 바꾸지 않는다. 실제 T0를 수행하려면 고정 실제 build·fixture/deck·단위·원천/관측 형식과 해당 범위 반박 GO·1저자 GO가 별도로 필요하다.

## 4. 시험 먼저와 증거 단위

| 대조 | 결과 | 한정 |
|---|---|---|
| 신규 API의 fail-closed 초기 stub → 같은 최종 시험 | 20메서드 중 assertion/subtest 실패5·오류0·rc1 | 정상 양성 계약이 미구현이라 실패한 **신규 기능 stub red**. 옛 제공기의 결함 또는 missing-import 오류가 아님 |
| 구현 후 같은 시험 바이트 | 20/20·오류0·rc0 | 신원10필드·단위·sample·역할·형식·부호·유한성·불변성·권한false의 합성 범위 |
| identity·units·sample·type guard 제거 | 대조4/4에서 원 후보 거부→guard 제거 후보 수용 | 메모리 변이와 작은 fixture의 개별 관측. 신규20메서드에4를 더하지 않음. 변이도 운영 권한은false |
| 기존 q/생성기 바이트 | 부모 Git blob과 동일 | 기존22/18 재실행0. 변하지 않은 기존 시험을 이번 통과 수로 세지 않음 |

시험은 Windows Python3.12.14에서 `-I -B`로 수행했다. 소스 사본을 exact bytes로 compile/exec하기 전에 프로세스/네트워크 경계를 차단했고 시도0이었다. 원 source/test·rc·stdout/stderr·UTC·SHA는 리포 밖 원증거에 보존하고 하루 검토 ZIP에 포함한다. 리포용 `verification_summary.json`은 요약 영수증이다. 전체 gate/CI·실제 바이너리/DEM/호스트·실제 T0는 미실행이다.

고정 후보의 반박 판정은 PENDING이다. D-1 첫 연결의 기존 판정을 대신하거나 앞 연결을 승인하지 않는다. 상시 요청서에 따라 다음 T5 준비를 새 가지에서 이어가되 실제 자격·값/원로그 접근·운영 봉인·발사/배포는 계속 별도다. **전체 HOLD, 결과0.**
