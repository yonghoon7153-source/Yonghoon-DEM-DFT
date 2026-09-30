# 81차 게이트 — 단계 3 제한 구현 범위·사전 고정 사항 검토

2026-09-28. **판정: 수정 조건부 적합. 3-A/B/C를 한 코드 라운드로 묶는 방향과 Q1·Q4는 수용한다. Q2·Q3 및 planned/realized 연결은 아래 G81-N1~N3을 명세에 반영해야 한다.**

이는 설계·구현 범위 판정이다. 구현 착수, 실행 GO, pilot, COMSOL 실행을 승인한 것이 아니다. 76차 종결과 80차 단계 1+2 종결은 다시 열지 않는다. `grid_fit_v5`는 diagnostic/no_active_claim으로 유지한다.

## 1. 식별과 확인 범위

- GitHub에서 관측한 요청 커밋/서브 HEAD: `88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e`.
- 사용자가 보낸 GATE81_REQUEST.md: 21,518 bytes / SHA-256 `c09b8232a200b256f0bd83205341b749fb20be0d2e689a63423d6233e8700cb0`. 위 커밋의 Git blob `e8da4018bacfdb352c662774bb87efdaff1645f9`와 **원문 바이트가 같다**.
- 코드 기준: `6ffa98d4df542aa42abde2f94685beffec33312c`. 현지 고정 80차 checkout `9a26dd5f31ca6fae45d5a55f5c59e33408371984`의 RUN_SCOPE 58파일을 읽어 digest `eda3feb8f4536511`을 재계산했다. 코드 기준→현지 HEAD diff 0.
- 원격 compare는 80차 HEAD→요청 HEAD가 5커밋 앞선 후손이며, 변경 36파일 중 RUN_SCOPE 변경은 0임을 반환했다. 이를 바탕으로 변경 없는 현지 코드·계약을 검토했다. **81차 checkout을 새로 만들어 실행한 것은 아니다.**
- 감사 snapshot 이후 선택 67개 코드·문서·사용자 요청 파일의 전후 크기/SHA 동일, 현지 checkout HEAD 동일·clean을 확인했다. 후속 수신 GATE81_SEND.md 1개는 별도 snapshot/보존으로 추가했다.
- 대상 모듈 import/함수 호출, pytest/smoke/mutation, 복원/재채점/영수증 재생성, COMSOL/JVM 및 구현은 모두 0회. 검토자 소유 감사는 파일·Git/JSON·AST 정적 읽기만 수행했다.

후속으로 받은 GATE81_SEND.md가 요청 커밋의 발신 측 실행 기록을 보충했다. 아래 §1.1과 같이 **발신 보고**로 수용하며, 수신 측에서 suite를 재실행했다고 합산하지 않는다.

### 1.1 추가 발송문 확인

GATE81_SEND.md의 SHA-256은 `64847ca0d7d8cdda80e0016b5b1ac7f3754552ebb64754f1996ee691dbfb001e`다. 발송 HEAD/코드/digest가 위 독립 식별과 일치하고, 3-A/B/C 범위·실행 및 착수 미승인도 요청문과 같다. 설계 내용 변경이나 추가 승인으로 읽지 않는다.

| 발신 보고 | 기록의 의미 |
|---|---|
| 88ac144a에서 docs-lint 358 PASS/rc0, 전체 1960 PASS·1 xfailed/rc0, smoke rc0 | 해당 SHA에서 환경 정비 후 다시 실행한 최종 보고. 수신 재실행/원시 로그 독립 검증이 아님. |
| 첫 docs-lint 4 failed/354 passed | 그중 self-contained-request 시험의 과거 커밋 부재는 구체 원인이 제시됨. **나머지 3건은 개별 원인 미확인**으로 남김. |
| 첫 pytest 수집 오류3(matplotlib), smoke rc1(pybamm/joblib) | 의존성 부재라는 구체 오류가 보고됨. 새 구현 기능 실패와 구분. |
| requirements 설치·unshallow 후 같은 SHA 재실행 | source 변경 없이 통과했다는 후속 근거. 위 3건의 최초 원인을 각각 확정하거나 최초 실패를 지우는 근거는 아님. |

보고된 시간은 docs-lint 1321.73초, 전체 2951.96초, smoke 약176초이며 시작/끝 HEAD 동일·미추적0도 발신 보고로 구분한다. smoke는 작은 grid/fit/score/restore 계산을 포함하므로 모든 계산0으로 바꾸지 않는다. 과거 80차와 숫자가 같아도 발신문은 별도의 81차 실행이라고 보고했으므로 그 provenance를 유지한다.

**추가 판정:** 이 보충으로 실행 결과 발송 기록의 공백은 해소됐다. 같은 suite의 재실행이나 최초 3건의 추가 진단을 이번 설계 승인 조건으로 새로 요구하지 않는다. G81-N1~N3은 시험 결과 유무가 아니라 제안 명세의 문제이므로 유지한다.

## 2. 질문별 판정

| 질문 | 답 |
|---|---|
| 3-A/B/C가 단계 3인가, 분할할 것인가 | 대체로 맞다. 아래 수정 후 **한 제한 코드 라운드** 권고. 내부 순서는 schema/dispatch → bank·ID·no-provider → provider → 전체 소비 연결이다. 중간 결과를 완료로 게시하지 않는다. 조각마다 별도 gate/영수증을 의무화할 필요는 없다. |
| Q1 unit-cube bank·bounds mapping | **단계 3에 포함 수용.** random ID를 null로 둔 채 candidate 연결 완료를 주장하지 않는다. 기존 legacy 계산과 새 version 경로를 분리한다. |
| Q2 혼합 행 정책 | **명시 거부를 선택.** 다만 정상 `v6_prep_logging` 8필드 행과 손상된 v6 행의 downgrade를 구분하는 G81-N2가 필요하다. |
| Q3 provider artifact/map/protocol SHA | 세 대상의 종류는 타당하다. **각 해시를 가진다는 것만으로 같은 공급 경로라는 증명은 아니다.** G81-N3의 결속·선택·null 정책을 추가한다. |
| Q4 ID domain·기존 golden 불변 | **수용.** 실제 바이트 해시는 별도 fixture로 시험하고 기존 golden은 재생성하지 않는다. preimage/domain 변경 필요 시 중지·회신한다. |
| §2의 기존 사전 고정값 | ladder/max/채택 규칙/floor/material/sentinel/자원값은 재심하지 않는다. bank·provider 형식 구현이 그 숫자의 실행·채택을 뜻하지 않는다. |
| RUN_SCOPE 4파일·receipt·봉인 | 한정 범위로 적합. 새 writer/reader schema 변경도 그 안에 명시한다. 최종 고정 코드에서 대상 leg별 receipt 1회, 원본 history 보존. 격리 restore/validate/rescore와 검증용 계산은 **사용자의 이후 승인에 명시**한다. |
| 실행·착수 여부 | **이번에는 모두 승인 아님.** 수정 명세를 포함한 제한 구현 범위를 사용자가 별도로 승인해야 한다. |

## 3. G81-N1 · P1 — 실행 전 계획에 실현값을 넣지 말고, 관측 roster까지 결속해야 한다

**좌표:** GATE81_REQUEST.md:46; STAGE3_CONTRACT.md:154–160,250–258,823; tools/preserve.py:2327–2379,2987–2991,3050–3059; GATE78_REQUEST.md:60; GATE79_REQUEST.md:23.

요청 3-A는 `PlannedLeg envelope에 stage×objective×arm 예산/실현 count`를 넣는다고 한다. 그러나 `PlannedLeg`는 실행 **전에** 봉인되고 `planned_id = digest(envelope)`다. 계약 묶음 1의 제목도 planned_protocol과 execution_receipt의 **분리**다.

예를 들어 계획 B=5였지만 adaptive 조기 종료로 실제 2개를 평가했다면, 실현 count를 2로 채운 순간 계획 ID가 바뀌거나, 처음의 5를 그대로 두면 사실과 다른 실현 기록이 된다. 아직 쓰이지 않은 v6 구현에서 이 일이 발생했다고 주장하는 것이 아니라, 현재 제안 문장을 그대로 구현할 때 생기는 충돌이다. 고정 비adaptive 경로도 예상 count와 관측 count를 같은 자료라고 취급하면 안 된다.

또한 79차에서 합의한 `obs_key`/planned roster는 이번 표에서 빠졌다. `pair_group_id`는 noise/seed/objective를 제외한 **bank 공유 그룹**이다. 그 ID와 count만 추가하면 같은 물리좌표의 서로 다른 잡음 실현 두 개를 구별하는 생산 연결이 남는다. 기존 문서 종결을 다시 반려하는 것이 아니라, 그 문서가 단계 3으로 배정한 코드 연결을 범위에 명시하라는 뜻이다.

### 최소 정정

1. **planned:** version, stage×objective×arm budget/mode, planned candidate 구성, bank/설계/입력/provider 식별, 사전 roster 및 `cond_id ↔ obs_key ↔ pair_group_id` 관계를 봉인한다. `planned_id`와 사전 승인 digest는 실행 결과를 넣어 바꾸지 않는다.
2. **realized:** 실제 시도/반환/실패/미시도 구분, 후보별 ID·index·실제 소비 좌표 식별, 실제 prefix/count, realized map SHA는 별도 execution record에 기록하고 `planned_id`를 참조한다. 실패한 restart를 성공 리스트에서 빼는 기존 동작과 실제 시도 수는 구별한다. 예상 count를 실제 count로 복사해 채우지 않는다.
3. 기존 `planned-leg/v3`와 닫힌 envelope 검사에는 새 필드를 조용히 끼워 넣지 않는다. 새 schema 또는 명시 version branch를 정하고 기존 planned/receipt/승인 바이트는 읽기 전용으로 보존한다. 새 schema의 정합성은 이번 범위이며, 전역 claim 세대표 등록/승격은 여전히 단계 4 이후다.
4. 관측 key는 79차 합의 정의를 그대로 쓰고, 같은 key의 objective별 중복·교차 seed·cond_id 충돌을 거부한다. planned roster의 행 부재를 탐지할 수 있게 한다. **Δ/누락 bound/새 scoring 계산 구현을 이번에 추가하는 것은 아니다.**

**닫힘 조건:** planned/realized 두 자료의 필드·생성 시점·서명 대상을 한 표로 정하고, 계획 동일/실현 count 상이 사례, 다른 계획 receipt 혼입, 같은 pair group의 두 noise-realization roster 사례를 실제 소비 경로의 fixture에 연결한다. 과거 원장/receipt/산출은 바꾸지 않는다.

## 4. G81-N2 · P1 — 세대 구분을 행의 키 개수나 mode 라벨로 결정하면 안 된다

**좌표:** GATE81_REQUEST.md:37,40,48,55–56; src/fitting.py:337–359,1538; src/io.py:1557–1577; tests/test_gate79_stage3_logging.py의 g79_06.

요청은 `v6는 8+2키`, `옛 세대는 4키`, `새 키 일부면 mixed_invalid`라고 한다. 하지만 정상적인 **79~80차 8키 v6_prep_logging 행**이 이미 있고, `g79_06`은 그 값을 그대로 보존하도록 요구한다. 이것을 10키의 부분 행으로 거부하거나 4키 legacy로 낮춰 로깅 3값을 None으로 만들면 지난 종결 조건을 깨뜨린다.

반대 방향도 있다. v6 행에서 candidate_id/bank_index를 둘 다 삭제했을 때 8키니까 prep으로 받아 주면 v6 필수 검사가 우회된다. 필드의 부재만으로는 진짜 prep 기록과 손상된 v6 기록을 구분할 수 없다. `legacy_slot_replace`는 v6에도 존재하는 **후보 정책 이름**이므로 그것만으로 옛 RNG/reader를 선택해서도 안 된다.

### 최소 정정

| 선언된 입력 문맥 | 읽기/쓰기 원칙 |
|---|---|
| historical legacy pair/dict | 당시 형식의 읽기 전용 의미 유지. candidate/native 필드를 가짜 관측으로 채우지 않는다. 기존 validator의 원래 허용 범위를 임의로 넓히지 않는다. |
| historical v6_prep_logging | 기존 8키·3개 로깅값을 보존. candidate_id/bank_index 미기록은 정상이며 v6 완료는 아니다. |
| 새 version writer/validator | 새 필수축·10키를 강제. 키 일부 또는 전부 제거, 다른 세대 혼입, 타입/내용 불일치를 거부. legacy/prep fallback 금지. |
| 선언 없음/모순/혼합 손상 | 새 v6 성공으로 승인하지 않는다. diagnostic reader가 값을 보여 주더라도 validator 결과는 거부/미완으로 분리한다. |

- 실행·산출의 봉인된 schema/protocol 문맥으로 dispatch하고 행 모양은 그 문맥에 **대조**한다. 현재 source_digest가 CLAIM_STATUS 표에 없다는 이유로 v6를 추론하거나 옛 기록을 새 세대로 등록하지 않는다.
- 새 writer는 새 schema와 명시 인자로 선택한다. legacy_slot_replace라는 동일 mode를 가진 legacy/v6를 둘 다 표현할 수 있어야 한다. 옛 기본 CLI/함수 경로·RNG·수치 결과는 유지한다.
- `converged`는 80차에서 수용한 마지막 유한 round의 legacy ok다. True여도 outer=nonfinite일 수 있다. 새 검증은 기록의 정합성과 solver 건전성 실패를 구분해야 하며, status를 no_improvement로 고쳐 통과시키지 않는다. 첫 비유한 round의 native_best=None 등 정상 실패 표현도 보존한다.

**닫힘 조건:** 정상 legacy/prep/v6 대조군과 v6→8키/구형키 삭제 downgrade, 부분 새 키, 선언-행 충돌, legacy mode명이 같은 두 세대를 실제 dispatch/validator에서 구분한다. 전체 단계 4 consumer 정비까지 당겨오라는 요구가 아니라 **이번에 추가하는 경로가 안전하게 호출되는 최소 version 경계**다.

## 5. G81-N3 · P1 — provider 세 해시를 실제 공급 행·좌표에 연결해야 한다

**좌표:** GATE81_REQUEST.md:47,57; STAGE3_CONTRACT.md:122–131,235–258,272–282; tools/design_wire.py:72–79,500–529; src/fitting.py:261,461–475; tools/preserve.py:2386–2403.

fits 파일, solution-map 파일, run_spec의 해시를 각각 봉인하는 선택은 좋다. 그러나 payload seal은 파일 바이트를 고정할 뿐 **map의 p가 그 fits의 해당 조건/목적함수 해인지**를 자동 검증하지 않는다. 현재 candidate_id도 전달받은 해시의 형식과 ID 사슬을 검사하지, 파일을 열어 관계를 증명하지 않는다.

설계 반례는 간단하다. 유효하게 봉인된 fits A와 다른 조건의 유효 map B를 함께 내면, 세 해시가 모두 진짜여도 초기값 출처는 틀릴 수 있다. 같은 파일 안의 s1/s2 행을 바꾸거나 objective를 잘못 고르는 경우도 같다. 현행 새 코드의 재현 결과가 아니라 아직 빠진 수용 조건이다.

### 최소 정정

1. provider edge별 stage/arm/provider objective/consumer objective와 정확한 입력·reference/bounds/protocol 문맥을 고정한다. map을 objective별로 나누거나 header에서 objective를 고정하고 **그 안에서** cond_id→p를 사용한다. p_ini map과 condition map을 무구분한 한 세트로 덮지 않는다.
2. map 생성자는 봉인 fits에서 지정 row를 유일하게 선택한다. consumer는 map header의 fits/protocol SHA, 요청 조건·objective, 좌표 parameter order·유한성·바이트 표현을 실제 입력에 대조한다. duplicate/missing/wrong-objective/wrong-condition, 미봉인·순환/self provider를 거부한다. 전체 planned coverage와 사용한 조건의 coverage를 구분한다.
3. **map에서 선택한 좌표 → solver에 실제 전달하는 x0**를 연결한다. 현행 fit은 init을 np.clip한다. 새 경로의 정책은 bounds 밖 provider/base를 거부하는 방식이 단순하다. 변환을 허용하려면 변환 전후 좌표와 규칙을 결속해야 한다. legacy 동작을 바꾸거나 clip한 점을 원 provider 좌표와 동일하다고 기록하지 않는다.
4. no-provider는 명시된 primary/first-objective 분기에서만 허용한다. warm=true 또는 provider가 필요한 arm에서 map 누락/빈 dict/잘못된 objective가 발생한 것을 no-warm 성공으로 바꾸지 않는다. 원래 no-provider인 경우 관련 artifact/map/protocol 참조는 해당 schema의 명시 null/N/A로 두고, 사용하지 않는 warm payload가 남아 있으면 정합성을 검사한다.
5. provider_protocol_sha256은 **정확히 어느 봉인 run_spec과 canonicalizer를 해시하는지** 명시하고 파일/manifest에서 재계산한다. provider 자신의 산출 SHA나 consumer realized 값을 사전 protocol의 자기 해시에 넣지 않는다. p_ini_values_sha256은 halfcell의 실제 원점 값 결속이고 grid는 null이다. 내용 검증을 위해 candidate/v2 preimage를 늘릴 필요는 없다.

**닫힘 조건:** 정상 봉인 공급, 다른 fits/map 결합, 같은 map의 조건/objective 교차 선택, 미봉인 소비, warm-required 누락→no-warm 전환, 실제 x0 불일치를 합성/소유 fixture에서 거부한다. 실제 provider leg·canary·새 연구 계산을 만들어야 한다는 요구가 아니다. 운영 retention provider와 warm provider의 별도 경계는 유지한다.

## 6. Q1·Q4 수용에 따르는 좁은 구현 기준

unit-cube bank를 단계 5로 미루지 않는다. 기존 `candidate/v2` random payload와 연결하려면 실물 index/row bytes가 지금 필요하다. 단계 3에서는 bank를 만드는 **규칙과 데이터 연결**을 구현할 뿐 B를 채택하거나 plateau를 실행하지 않는다.

- generator/version, seed derivation(공유 pair group 기준), dtype/endian/shape/order/직렬화, parameter order를 고정한다. treatment/noise/objective별 cond_id seed를 새 공유 bank 생성에 그대로 쓰지 않는다.
- 같은 봉인 bank에서 B별 prefix를 선택한다. B마다 짧은 bank를 재해시해 공통 후보의 bank_id/candidate_id가 바뀌지 않도록 full-bank identity와 consumed-prefix 길이를 구별한다. bank 길이/버전 변경이 필요하면 새 bank identity다.
- exact_bounds_sha256은 실제 ordered lb/ub, unit_cube_bytes_sha256은 선택한 실제 row다. `lb+u*(ub-lb)`의 실제 mapped x0도 결속한다. 단순히 64hex 문자열이 있으면 통과하는 방식은 수용하지 않는다.
- source별 index/count를 검사한다. base/warm의 **bank_index만** null이고 candidate_id는 세 source 모두 필요하다. random index는 범위 내·해당 조건/objective의 중복 없음이며 J 정렬 순서를 index로 삼지 않는다. 같은 bank index가 다른 objective/조건에서 재사용되는 것은 설계상 정상이다.
- no-provider는 B≥1에서 `[base]+bank[:B-1]`. warm이 있는 base-retained는 B≥2 등 mode별 유효 범위를 명시한다. 이번에 지원하지 않는 mode는 명시 거부하고 legacy 경로로 조용히 대체하지 않는다. union의 별도 연구 실행은 승인하지 않는다.
- golden 31건은 기존 domain의 회귀 근거이지 모든 실물 결속의 증명은 아니다. golden은 그대로 두고 실제 바이트 기반 positive/negative fixture를 추가한다. 기존 preimage 확장이 필요하면 별도 회신한다.

Q1의 미채택 대안은 :55의 `candidate_id=null/index유지`와 :104의 `index=null`이 서로 다르다. **Q1을 포함으로 확정하므로 두 미채택 문구를 삭제/정정하면 끝**이며 별도 gate를 만들 필요는 없다.

## 7. 제한 구현 승인에 넣을 범위와 종결 경계

다음 사용자가 승인할 범위는 **G81-N1~N3 정정 문장 + 단계 3의 한정 오프라인 구현·회귀**다. 동일 계획서만 반복 제출하는 라운드를 의무화하지 않는다. 정정 표를 시작 전에 고정하고, 사용자 승인 뒤 코드·시험 결과를 GATE82에서 함께 검토할 수 있다. 이번 회신의 조건과 다른 선택이 필요할 때만 먼저 질문한다.

1. schema/dispatch/계획-실현/roster와 provider edge 표를 먼저 고정하고, 3-A→3-B→3-C를 내부 순서로 연결한다. serializer/validator는 끝에만 붙이는 장식이 아니라 각 데이터 경로의 완료 조건이다.
2. 기본 허용 RUN_SCOPE는 요청한 네 파일이다. 그 안에 version-dispatched envelope/reader, bank 생성·mapping, candidate/roster/provider 결속이 포함된다. 다른 production 파일 수정이 필수면 조용히 넓히지 말고 최소 변경 목록을 추가 승인받는다. 새 helper 파일이 필요하다면 그 선택도 승인 범위에 명시한다.
3. 기존 후보 선택·legacy RNG·최적화 본문·J/p 의미·scoring·row_projection·golden·과거 fits/receipt를 보존한다. 새 version 경로의 새 후보 구성은 이번 구현 대상이며 이를 legacy 수치 불변과 혼동하지 않는다.
4. 새로 없던 기능은 유효한 fixture로 RED→GREEN, 기존 호환성/정상 대조군은 처음부터 GREEN일 수 있다. 요청 §7의 **“처음부터 통과하는 시험은 fixture를 의심”을 모든 시험에 적용하지 않는다.** 실패 이유와 실제 assertion/도달 경로를 기록하고 무관한 예외를 RED 증거로 삼지 않는다.
5. 요청한 회귀·변이·전체 pytest·strict smoke는 이후 승인된 검증 범위다. smoke/단위시험 안의 작은 optimizer·grid 계산은 계산 총0이 아니다. 새 연구 leg/floor/pilot/provider canary0과 구별한다. 이번 수신 검토는 그 어느 것도 실행하지 않았다.
6. 최종 코드가 고정된 clean 커밋에서 paired_fixed5_v4/grid_fit_v5 영수증을 각각 1회 재생성한다. 기존 `eda3feb8f4536511` 영수증 원문 history 보존, 변경 필드·producer 불변 대조. 검증 실패를 무조건 재생성 반복으로 닫거나 원장 PASS로 붙이지 않는다. 이후 RUN_SCOPE가 다시 움직이면 최종 영수증이 아니라는 상태로 멈춰 보고한다.
7. 단계 4의 전 소비자 구 필드 제거/claim 세대 게시, 단계 5의 floor·sentinel·budget-adoption, 단계 6의 비용·pilot, 12-P 운영 canary는 별건이다. 기존 E1/E2/E4·보존 한계를 이 코드 라운드로 해소했다고 쓰지 않는다.

**다음 제출물:** N1~N3 반영 표, 네 파일 최소 diff(추가 승인 파일이 있으면 별도 표시), schema/필드 시점 표, ID/좌표/provider 연결 근거, 이유별 positive/negative/변이 결과, legacy/prep 보존, 최종 코드 식별과 영수증 diff. 구현 전 새 연구 데이터를 만들 필요는 없다.

## 8. 검토 한계와 기록

세 발견은 아직 없는 새 구현의 런타임 버그를 실측했다는 뜻이 아니라 **제안 범위의 설계 충돌/누락**이다. 내용은 현재 고정 코드·기존 계약과 대조했으며, 본문 반례는 설명용 입력이다. 대상 코드를 실행한 재현 결과나 미래 회귀 PASS로 세지 않는다.

일반 Git 원격 조회는 Windows TLS 자격 증명 오류로 실패했다. 계정/정책을 바꾸지 않고 이미 제공된 GitHub 읽기 connector로 커밋·비교·파일을 조회했다. 초기 connector 인자 형식 오류도 있었으며, 저장된 evidence는 성공한 응답의 후속 직렬화다. 원시 네트워크 감사 로그라고 주장하지 않는다. 현지 감사는 첫 실행 rc0이다.

근거: STATIC_DATA_AUDIT.json, SOURCE_BEFORE.json, SOURCE_AFTER_CHECK.json, evidence/의 원격 응답 기록, reference/의 고정 소스·계약·원문 요청. 이전 gate80 결론 사본은 prior_gate80/에 있다. 원격 전체 프로세스 부재·발신자의 모든 실행 횟수·운영 backend 권한은 독립 확인하지 않았다.
