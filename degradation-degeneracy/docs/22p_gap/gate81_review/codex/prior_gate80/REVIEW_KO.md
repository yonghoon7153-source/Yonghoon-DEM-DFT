# 80차 게이트 독립 검토 — G79-N1 및 단계 2 종결

2026-09-28. **G79-N1(P2) 종결 수용. 79차의 단계 1 종결을 유지하고 단계 2도 종결한다. 이번 범위의 잔여 P1/P2는 0건이다.**

실행 GO·단계 3 착수·연구 계산·class 변경·투영 게시 승인은 아니다. 76차 종결 및 `grid_fit_v5`의 diagnostic/no_active_claim을 유지한다.

## 1. 질문별 판정

| 질문 | 판정 |
|---|---|
| G79-N1 설명 정정·한정 회귀·변이로 잔여가 닫히는가 | 예. 실제 제어 순서와 설명이 일치하고, 요청한 두 경로의 assertion이 있다. |
| 단계 2 종결인가 | 예. 79차에서 남긴 한정 종결 조건이 충족됐다. 단계 1+2 한정 범위 종결이며 전체 단계 3 계약 구현 완료는 아니다. |
| 단계 3을 시작해도 되는가 | 이번 검토로 시작하지 않는다. 단계 3은 구체 범위에 대한 새 사용자 승인 뒤 별건으로 진행한다. |
| 실행·주장 경계 | 새 실행 GO 아님. grid_fit_v5 진단 전용 유지. 새 연구 계산 0은 발신 기록의 주장으로 구분하며, 수신자가 원격 전체 실행 이력을 입증한 것은 아니다. |

## 2. 고정 식별과 검토 방법

- 요청 HEAD: `9a26dd5f31ca6fae45d5a55f5c59e33408371984`.
- 코드: `6ffa98d4df542aa42abde2f94685beffec33312c`.
- RUN_SCOPE 58개 파일을 직접 읽어 재계산한 digest: `eda3feb8f4536511`.
- 코드 → 요청 HEAD RUN_SCOPE diff 0. 79차 코드 대비 RUN_SCOPE 변경은 `src/fitting.py` 하나이며 docstring·주석 두 블록이다.
- 새 독립 checkout: `C:/Users/Administrator/Documents/Codex/g80_20260928`. 기존 79차 checkout/보고서·생산 코드·원장은 수정하지 않았다.
- 선택 66개 코드/검토 문서의 전후 크기·SHA 동일, HEAD 동일, 검토 후 clean을 확인했다. 전체 원격 파일·프로세스 검증이 아니다.
- 79차 검토 ZIP 610,052 bytes / SHA `f4d7e81338436bf703b35b454ee60cd315bd7678bfc0221298b6150fbd338695`: 40 payload + manifest, 정확 집합·크기/SHA·CRC·중복/대소문자·경로/링크 검사 통과. 현지 보존 원본 및 저장소 동봉 사본과 바이트 동일하다.

근거: `DATA_AUDIT.json`, `STATIC_CHECKS.json`, `SOURCE_BEFORE.json`, `SOURCE_AFTER_CHECK.json`, diff와 reference 사본.

## 3. G79-N1 종결 근거

### 계산 동작을 문장에 맞춰 바꾸지 않았다

`src/fitting.py` 전체를 AST로 읽고 docstring만 제외해 79차와 대조했다. 실행 구문 AST는 동일하다. 주석·docstring이 바뀌었으므로 소스 바이트 또는 `__doc__`까지 불변이라는 뜻은 아니다.

실제 `_minimize_until_stable` 순서는 그대로다.

1. 초기 `ok=False`.
2. 각 round에서 native_last/n_rounds/nfev 기록.
3. `res.fun`이 비유한이면 `outer=nonfinite` 후 break(223–225행).
4. 유한일 때만 `cur_x, ok = …, bool(res.success)` 갱신(227행).

따라서 “마지막 유한 fun round에서 갱신한 success; 해당 round가 없으면 초기 False”라는 새 설명이 반환 의미와 맞는다. native_last/native_best/outer와 legacy ok가 다른 관측이라는 문장도 추가됐다. `converged=True`만으로 nonfinite를 정상 완료로 읽지 않는다는 경계가 명시됐다. GATE79의 잘못된 문장은 취소선으로 보존·정정돼 있다.

### 두 회귀가 필요한 두 경로를 구분한다

| 회귀 | 소스에서 확인한 입력과 assertion |
|---|---|
| g79_03c (146행) | 첫 유한 fun=1.0/success=True → NaN/success=False. p/J는 첫 round, nfev=14, ok=True, native_last=False, native_best=True, outer=nonfinite, n_rounds=2를 함께 요구한다. |
| g79_03d (171행) | 첫 round부터 inf/native success=True. ok=False, J=inf, 초기 p 유지, nfev=2, native_best=None, outer=nonfinite, n_rounds=1을 요구한다. |

두 시험은 `F.minimize`만 fake로 바꾸고 실제 `_minimize_until_stable`을 호출하도록 작성됐다. 수신 검토에서는 실행하지 않고 소스·assertion·제어 순서를 대조했다. 처음부터 GREEN인 것은 이번 설명 정정의 성격에 맞으며, 억지 RED를 추가할 필요가 없다.

변이 `legacy-ok-is-the-last-finite-round-g79`는 비유한 검사 앞에 `ok = bool(res.success)`를 추가한다. 대상 원문은 현행 소스에 정확히 1회 존재하고 selector는 g79_03c다. 해당 변이면 두 번째 round가 ok=False를 덮어써 실제 assertion과 충돌한다. 등록 EXPECT/witness도 그 assertion을 가리킨다. 발신자의 1/1 검출 보고와 정적 구조가 일치한다. 수신자가 mutation replay를 재실행했다는 뜻은 아니다.

## 4. 영수증·보존

- 직전 paired/grid 영수증 두 개가 `history/<leg>.validate.c78d7969ef49fd07.yaml`에 바이트 동일하게 보존됐다.
- 현재 두 core SHA를 데이터에서 재계산하고 원장 참조와 일치함을 확인했다.
- 실제 차이는 `/core/identity/validator_source_digest`, `/core_sha256`, `/stamp/generated_at_utc`, `/stamp/validator_commit`뿐이다. src_io_sha256, validation, outputs는 불변이다.
- 원장은 leg별 verification_receipt_core_sha256 및 validator_identity/source_digest만 변경됐다. producer 식별은 그대로다.
- 두 bundle의 55개 파일, 총 51,176,572 bytes의 집합·크기·payload SHA를 직접 대조했다. 복원·validate·재채점은 실행하지 않았다.
- paired core: `00db82af4377c3e0`로 시작. grid core: `ffc2e9354215e3b6deb257478fc810547ac664097a4e448c55b9402beca6bfc6`. 전체 값은 DATA_AUDIT.json에 있다.
- grid stamp dirty=true는 그대로 유지한다. clean 시작과 개별 영수증 생성 시점 clean을 혼동하지 않는다.
- paired의 역사적 evidence.out 부재는 소급 채우지 않았다. 이번 검토가 과거 paired 다리의 새로운 attach 수용을 뜻하지 않는다.
- artifacts, CLAIM_STATUS 및 점검한 class/projection 경로의 이전 HEAD 대비 diff 0을 확인했다.

## 5. 시험 fixture 수정과 발신 실행 기록

첫 전체 회귀 2 failed 뒤의 조치는 계약 줄번호 갱신과 `tests/test_fitting.py::sign_producer`의 fixture_nonce 추가다. 후자는 시험 산출 spec/서명을 호출별로 구분하며 production 등록 규칙을 변경하지 않는다. 같은 바이트의 cross-namespace 등록을 허용하도록 바꾼 것도 아니다. 이번 설명 정정의 계산 경로 불변 주장과 충돌하지 않는다. 무작위 nonce를 쓰므로 이 시험 fixture 산출이 호출 간 바이트 재현된다고 해석하지 않는다.

전체 1960 passed/1 xfailed, smoke rc0, docs-lint358, 변이1/1과 최초 실패 원인은 요청문·원장의 발신 기록으로 소비했다. 전체 pytest/smoke/변이를 수신 측에서 다시 실행하거나 그 횟수에 합산하지 않았다. smoke의 작은 grid/fit/score/restore 계산을 “모든 계산 0”으로 바꾸지 않는다.

## 6. 이월 및 다음 경계

79차의 `normalize_restart_record` 일부 새 키 행 처리 관찰은 계속 비차단 이월이다. 이번에 손대지 않았고, 다시 단계 2 종결 조건으로 추가하지 않는다. 단계 3/4 세대 dispatch에서 혼합/손상 행을 명시 거부하거나 부분 기록으로 구분하는 정책을 정하면 된다.

추가 설명 정정이나 같은 회귀 재실행을 이번 종결 조건으로 요구하지 않는다. 다음은 사용자가 원하면 **단계 3의 제한 구현 범위·사전 고정 사항을 확인해 별도 승인**하는 것이다. 이번 회신만으로 착수하거나 pilot/연구 실행 GO를 부여하지 않는다.

## 7. 검토 활동 한계

대상 모듈 import/함수 호출, pytest/smoke/mutation, COMSOL/JVM/Java, 복원/재채점, class 변경/투영 게시, 단계 3 구현은 수신 측 각각 0회다. Git 읽기·독립 checkout, 파일/ZIP/YAML/JSON/해시 및 AST 정적 대조, 검토 산출물 작성만 수행했다.

처음 Git fetch는 unresolved deltas로 실패했다. 새 검토 저장소에서 refetch 후 고정 HEAD를 확보했으며 기존 검토 저장소를 수정하거나 대상 코드를 실행해 해결하지 않았다. 검토자 데이터 감사는 첫 실행 rc0이었다. 이 검토 결과는 단계 2의 한정 종결이며 전체 과학적 타당성·장기 실행 승인으로 확대하지 않는다.
