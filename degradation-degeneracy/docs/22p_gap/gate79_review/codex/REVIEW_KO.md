# Gate79 독립 검토 — 설계 잔여 종결, 로깅 의미 정정 1건

2026-09-28 · 사용자 승인 범위의 읽기 전용 코드·자료 검토.

## 1. 결론

**G78-N1·G78-N2는 설계 문장 범위에서 종결 수용한다. 단계 2 변경 범위는 적합하지만 G79-N1(P2) 한 건 때문에 단계 1+2의 무조건 최종 종결은 보류한다.** 단계 3 착수나 실행 GO를 승인한 것이 아니다. 76차 종결은 유지한다.

| 질문 | 판정 |
|---|---|
| ① 관측 쌍 key / 누락·분모 정정 | 둘 다 수용. 실제 ID·비교기 구현 완료를 뜻하지 않음 |
| ② 단계 2가 78차 경계 1–7 안인가 | 변경 범위는 적합. 기존 계산 제어 경로를 유지했지만 `converged`의 새 설명이 비유한 종료 경로와 불일치 |
| ③ 단계 1+2 종결 → 단계 3 | 단계 1 종결. 단계 2는 아래 G79-N1 정정·한정 회귀 확인 뒤 종결. 그 뒤에도 단계 3은 새 사용자 승인 필요 |
| ④ 실행/주장 경계 | 실행 GO 아님. `grid_fit_v5`는 diagnostic / no_active_claim 유지. 연구용 새 실행 0은 발신 기록의 주장으로 구분 |

**잔여는 P1 0건 / P2 1건.** §6의 reader 관찰은 비차단 사항이며 이번 종결 조건에 추가하지 않는다. 같은 계획 문서나 기존 78차 설계 심사를 반복하라는 요청이 아니다.

## 2. 고정 대상과 독립 확인

- 요청 HEAD: `b0203d1090b2659c31f8eb6f55e5a144657e9052`.
- 코드: `3dc269d80a7441b294d475b625b096baf3d1a459`; 재계산한 RUN_SCOPE digest `c78d7969ef49fd07`.
- 코드 커밋 → 요청 HEAD의 RUN_SCOPE diff 0. 이전 `23c361ed` 대비 변경은 `src/fitting.py`, `src/io.py` 두 파일뿐이다. RUN_SCOPE 58개를 읽어 재해시했다.
- 별도 checkout `C:/Users/Administrator/Documents/Codex/g79_20260928`에서 확인했다. 기존 Gate78 checkout·검토 자료와 생산 원장은 수정하지 않았다.
- 78차 원본 ZIP: 418,575 bytes / SHA `f41ee778decd9d35bef374896efb08e850141a89b099d0e090770d4c597b0edf`. 37 payload+manifest의 정확 집합·크기·SHA·CRC·경로/대소문자/링크 검사를 통과했고, 동봉 사본 및 보존 중인 검토 원본과 같았다.
- 이전 대비 artifacts, CLAIM_STATUS, class/투영 관련 경로, 봉인 `row_projection.py`, 기존 `tests/test_compare.py`는 불변이다.

근거: `DATA_AUDIT.json`, `SOURCE_BEFORE.json`, 세대별 diff, `STATIC_CONTROL_FLOW.json`. 최종 전후 보존 확인은 `SOURCE_AFTER_CHECK.json`이다.

## 3. G78-N1/N2 종결 근거

### G78-N1 — 관측 쌍 key

`GATE78_REQUEST.md` §2.1 정정 행과 GATE79 §1은 bank 공유용 `pair_group_id`와 실제 관측 쌍 `obs_key`를 분리한다. family/group/treatment/noise/realization/replicate를 구분하고, objective는 같은 key의 두 행으로 놓는다. objective별 정확히 한 행, cond_id 일대일 결속, 입력/reference/bounds 동일성, 사전 roster로 부재 검출, 중복·교차 seed의 구조 오류 처리가 명시됐다.

검토자 작성의 작은 조합 예제에서도 두 noise realization을 group만으로 join하면 4행, obs_key로 연결하면 2쌍이다. 이는 정정 문장의 논리 확인이지 아직 없는 생산 ID 구현의 시험이 아니다.

### G78-N2 — 누락·분모

사전 recoverable inclusion의 N, 유효 complete-pair n, 쌍 단위 m=N−n을 분리했다. Δ_cc=D/n은 조건부 기술통계로 제한되고, 전체 계획 집합의 범위는 관측 label을 보존한 `(D+Σl)/N`과 `(D+Σu)/N`이다. 양쪽 geometry 조건은 참조한 현행 `classify_recoverability` 규칙을 따른다.

검토자 소유 산술 검사로 3×3의 아홉 상태를 모두 열거해 상·하한을 대조했다. 40쌍 반례는 Δ_cc=1/38, missing-as-fail=−1/40, 실제 가능한 범위 [−1/40,+1/40]으로 맞는다. n=0/N=0의 미정과 5% reporting 정책 ≠ 실패·비유한 0건 plateau gate도 분리됐다. 설계 잔여는 닫는다.

근거: `DESIGN_AND_SYMBOLIC_CHECKS.json`. 비교기·solver·시험 대상 함수를 실행한 결과가 아니다.

## 4. 잔여 G79-N1 (P2) — `converged`는 항상 마지막 native round의 success가 아니다

위치: `src/fitting.py:200`, `:219–224`, `:321–327`; `GATE79_REQUEST.md:32–33`, `:59`; `tests/test_gate79_stage3_logging.py:102–143`.

새 설명은 기존 `ok`/restart `converged`를 **마지막 round의 res.success**라고 단정한다. 하지만 코드의 실행 순서는 다음과 같다.

1. native_last와 n_rounds를 기록한다.
2. res.fun이 비유한이면 break한다.
3. 유한일 때만 `cur_x, ok = ... bool(res.success)`를 갱신한다.

따라서 다음 두 round가 반환되는 경로에서는 설명과 값이 갈린다.

| round | fun | success | 해당 경로의 결과 |
|---|---:|---|---|
| 1 | 1.0 | true | best와 ok=true 갱신 |
| 2 | NaN | false | native_last=false, outer=nonfinite 기록 후 break; ok는 true 유지 |

반환 best J는 1.0이고 restart `converged=true`, `termination_status.native_last.success=false`, `outer=nonfinite`가 함께 남는다. 이것은 79차에서 새로 만든 계산 회귀가 아니다. **기존 반환 의미를 유지한 것은 맞고, 그것을 설명한 새 계약 문장이 틀렸다.** 마지막 유한 round가 없으면 ok는 초기값 false다. best round의 success와도 일반적으로 같지 않다.

AST 정적 대조에서 새 기록 문장과 다섯째 반환값을 제거한 `_minimize_until_stable` 제어 구조는 이전 버전과 동일했다. 비유한 분기 뒤에 ok 대입이 있다는 사실도 별도로 검사했다. 위 표와 JSON의 6개 경로는 이 순서에 대한 검토자 독립 기호 모형이며, 실제 SciPy 실행에서 이 현상을 관측했다고 주장하지 않는다. 추가된 메타데이터 변환의 예외까지 전부 무해함을 증명한 것도 아니다.

기존 g79_03은 **유한** best/last 차이만, g79_03b는 **첫 round부터 비유한**인 경우의 outer/native_best만 본다. 선행 유한 round 뒤의 비유한 종료와 ok 잔류를 대조하는 회귀는 없다.

### 최소 정정

- 기존 계산/반환 의미는 그대로 둔다. 문서·docstring·새 serializer 주석의 표현을 **“legacy ok: 마지막 유한 fun round에서 갱신한 success; 해당 round가 없으면 false”**로 고친다.
- `native_last.success`, `native_best.success`, `outer`가 각각 다른 관측임을 명시한다. `converged=true`만으로 nonfinite 종료를 정상 완료로 승격하지 않는다. 실제 단계 5의 성공/실패 집계 정책은 여전히 별도 구현 대상이다.
- fake-minimize 한정 회귀로 유한-success → 비유한-failure를 넣어 p/J/legacy ok 유지와 native_last/outer 차이를 함께 고정한다. 첫 비유한의 초기 false도 대조한다. 새 연구 계산은 필요 없다.
- `ok` 대입을 break 앞으로 옮겨 문장에 맞추는 수정은 하지 않는다. 그것은 이번에 보존하기로 한 의미를 바꾼다.

위 한 건이 확인되면 단계 2 종결을 판단할 수 있다. RUN_SCOPE가 다시 움직이면 새 최종 식별을 제출하고 영수증은 기존 승인된 세대 보존 규칙을 적용한다. 본 회신 자체는 코드 변경·시험·영수증 재생성 권한이 아니다.

## 5. 단계 2 및 영수증에서 수용한 부분

- minimize 인자, p/J 갱신, restart 정렬/agree/spread의 계산 부분은 제한 diff 범위에서 유지된다. sender의 두 골든 fixture 결과는 그 두 경우의 실행 증거로만 읽는다. 모든 입력에 대한 수치 동등성 증명이 아니다.
- restart 오류의 별도 열과 nonadaptive F86 실패 경로가 보존됐다. `n_eval` 합은 반환된 restart 결과의 합이라는 범위이며, 예외로 반환되지 않은 solver 호출의 비용 전부를 새로 관측한 것은 아니다.
- 두 validator에서 사전 parquet 읽기 실패는 각 `fits_읽기`/`curves_읽기` 실패 항목으로 내려가고 해당 파일의 후속 검사 블록을 건너뛴다. 기록된 깨진 footer 사례의 범위는 적합하다. 모든 정상 형식 parquet의 schema 오류·동시 교체·모든 I/O 오류까지 예외 없음으로 일반화하지 않는다.
- 기존 broken-parquet 조건부 xfail 시험 파일은 불변이다. 1958 PASS/1 xfailed, smoke rc0, docs-lint 358, RED/변이 결과는 발신자의 고정 기록이며 수신자가 재실행한 수치가 아니다. smoke에 작은 계산이 포함된다는 설명도 유지한다.
- 두 bundle 55개 파일, 합계 51,176,572 bytes의 index·구성원 집합·SHA를 직접 대조했다. 복원·재채점·분석은 하지 않았다.
- 직전 두 영수증은 history 사본과 바이트 동일했다. 현재 core SHA를 재계산하고 원장 참조와 대조했다. 바뀐 필드는 validator_source_digest, src_io_sha256, core_sha256, stamp의 commit/time뿐이며 validation/outputs는 이전과 같다. 원장에서는 leg별 core SHA와 validator digest만 바뀌었다. producer digest는 그대로다.
- paired: core `e5893f855bf64b9f2ab8cb78dde01f8b442a77a42946a1b65bff091bf82fd9c1`, 34검사 기록. grid: core `352f55e50af3038fdf321bcd716a1fb780e6c90f6e30288ba8e07be5749d533a`, 33검사 기록.
- grid의 stamp dirty=true는 그대로다. 원장 §109는 한 호출에서 앞 paired 영수증을 먼저 썼기 때문이라고 설명한다. clean 시작과 각 영수증 생성 시점의 clean은 같은 주장이 아니다.
- paired_fixed5_v4에는 역사적으로 evidence.out이 없다. 이번에도 소급 채우지 않았다. 이 검토는 그 과거 다리의 새 attach 수용이나 현행 실행 자리 결속을 승인하지 않는다. grid만 `evidence.out=restore.run_dir_relative=results/grid_fit_v5`를 확인했다.

## 6. 비차단 관찰 — 역사 reader의 범위

`normalize_restart_record`는 세 새 키가 전부 있으면 v6_prep_logging, 하나라도 없으면 legacy_dict로 분류해 **이미 있는 나머지 새 값도 None**으로 만든다(`src/fitting.py:345–352`). 예를 들어 `{..., converged:true, n_eval:12}`에서 termination_status 하나가 빠지면 true와 12도 없어진다.

이번 producer는 세 키를 함께 쓰고 기존 옛 기록에는 모두 없으며, 이 helper의 현재 src/tests 사용처는 정의와 신규 회귀뿐이다. 따라서 이를 이번 잔여 P1이나 단계 2 종결 조건으로 늘리지 않는다. 단계 3/4의 세대 dispatch를 구현할 때 **일부 새 키가 있는 손상/혼합 행을 옛 행으로 조용히 재분류하지 않는 정책**(명시 거부 또는 부분 기록 분리)을 고정하면 된다. 현재 결과를 전체 historical reader wiring 완료로 부르지는 않는다.

## 7. 검토 활동과 한계

수신 측은 대상 모듈 import/실행, pytest, smoke, mutation, solver, COMSOL/JVM/Java, 복원, 재채점, projection 게시를 하지 않았다. 새 연구 계산·단계 3 구현·원본 코드 수정은 0회다. 수행한 것은 Git 조회/별도 checkout, 파일·ZIP/JSON/YAML 읽기와 해시, AST 정적 대조, 검토자 작성 산술·기호 검사, 새 검토 산출물 작성이다.

검토자 자체 첫 data audit는 역사적 paired leg에도 out을 필수로 가정해 KeyError로 중단했다. `audit_attempt_01/`에 코드와 실패를 보존했고, grid의 필수 결속과 paired의 역사적 부재를 나누어 수정한 검토자 감사가 rc0으로 끝났다. 생산 코드·COMSOL의 실패로 세지 않는다.

초기 checkout 과정의 partial-object/Windows 인증 오류는 기존 자료를 변경하지 않고 별도 checkout과 승인된 HTTPS 읽기로 처리했다. 대상 코드를 실행한 우회가 아니다. 생성 ZIP은 검토 자료이며 실행 지시나 다음 단계 승인이 아니다.
