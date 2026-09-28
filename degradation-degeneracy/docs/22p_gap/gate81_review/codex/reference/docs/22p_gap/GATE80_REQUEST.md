# 80차 게이트 리뷰 요청 — G79-N1 (P2) `converged` 설명 정정 + 한정 회귀 · 단계 2 종결 판정 (실행 GO 아님 · 단계 3 착수 아님)

> **상태: 확정 (2026-09-28).** 79차는 G78-N1·N2 를 설계 문장 범위에서 종결하고 단계 1 을 종결했으며, 단계 2 는 **G79-N1(P2) 한 건** — "legacy `converged` = 마지막 round 의 success" 라는 우리 설명이 비유한 종료 경로와 어긋난다 — 를 정정·한정 회귀로 확인한 뒤 종결하겠다고 했다. 이 요청은 그 한 건이다. 계산 경로는 바꾸지 않았다 (`ok` 대입을 break 앞으로 옮기지 않았다 — 리뷰어가 금지한 의미 변경). 76차 종결 유지 · 새 실행 GO 아님 · 단계 3 착수 아님 · `grid_fit_v5` 진단/no_active_claim 그대로.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| **판정 대상 코드** | **`6ffa98d4`** (전체 SHA 발송문) — RUN_SCOPE 마지막 변경: `src/fitting.py` 의 docstring·주석 **문장만** (제어 흐름·반환값 불변) · `source_digest` **`eda3feb8f4536511`** (79차 대상 `3dc269d8` · `c78d7969ef49fd07` → 이 커밋). 그 뒤 커밋은 영수증·원장·문서뿐 (RUN_SCOPE diff 0 — 발송 전 실측) |
| 영수증 재생성 | `184d34dd` (clean `6ffa98d4`; 원본 `history/<leg>.validate.c78d7969ef49fd07.yaml`) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §111 (79차 접수 · G79-N1 대응 · 실측) |
| 79차 패키지 원본 | `docs/22p_gap/gate79_review/` (zip `f4d7e813…`, MANIFEST 40/40) |
| 새 시험 | `tests/test_gate79_stage3_logging.py` **15 node** (+2: `g79_03c` · `g79_03d`, 동작 고정 — 처음부터 통과가 목적) · 변이 +1 (`legacy-ok-is-the-last-finite-round-g79`) |

## §1 G79-N1 — 정정

| 리뷰어 최소 정정 | 우리 대응 |
|---|---|
| 1 계산/반환 의미 그대로. 표현을 "legacy ok: 마지막 유한 fun round 에서 갱신한 success; 그런 round 가 없으면 false" 로 | `src/fitting.py` `_minimize_until_stable` docstring · restarts 직렬화 주석 정정 (`6ffa98d4`). 제어 흐름·반환값 불변 — RUN_SCOPE diff 는 두 문장 블록뿐 (`git diff 3dc269d8 6ffa98d4 -- src/fitting.py`) |
| 2 `native_last.success` · `native_best.success` · `outer` 는 각각 다른 관측; `converged=true` 만으로 nonfinite 종료를 정상 완료로 승격하지 않음 | docstring 에 명시. 성공/실패 집계 정책은 단계 5 의 별도 구현 대상이라 적음 |
| 3 fake-minimize 한정 회귀: 유한-success → 비유한-failure 에서 p/J/legacy ok 유지와 native_last/outer 차이; 첫 비유한의 초기 false | `g79_03c`: round 1 (fun 1.0 · success) → round 2 (NaN · 실패) ⇒ 반환 p/J 는 round 1 · **ok True 유지** · `native_last.success False` · `native_best.success True` · `outer nonfinite` · `n_rounds 2` · `(ok, native_last.success, outer) == (True, False, "nonfinite")`. `g79_03d`: 첫 round 비유한(native success True 여도) ⇒ ok **초기 False** · f inf · native_best None. 둘 다 처음부터 통과 — 동작을 **고정**하는 시험이며 그것이 목적 |
| 4 `ok` 대입을 break 앞으로 옮기지 않는다 | 옮기지 않았다. 그 "수정" 을 변이로 등록: `legacy-ok-is-the-last-finite-round-g79` (`ok = bool(res.success)` 를 비유한 검사 앞에 둔다) → `g79_03c` 1 node 물었다 (witness "legacy ok 는 마지막 유한 round(1) 의 success 다 — 비유한 round 2 가 덮지 않는다") |

문서 정정: `GATE79_REQUEST.md` §2 두 행 · §4 한 항목 취소선 (원문 보존). 시험 파일 헤더·`g79_03` 메시지 문구 정정.

## §2 영수증 (승인된 세대 보존 규칙)

docstring 변경도 RUN_SCOPE 규칙대로 digest 를 움직인다 (`c78d7969ef49fd07 → eda3feb8f4536511`). 원본을 `history/<leg>.validate.c78d7969ef49fd07.yaml` 로 보존(`6ffa98d4`) → clean `6ffa98d4` 에서 재생성 (`184d34dd`). 필드 diff (두 다리): `identity.validator_source_digest` · `core_sha256` · `stamp.generated_at_utc` · `stamp.validator_commit` **뿐** — `src_io_sha256` 은 이번엔 불변(io.py 미변경), validation·outputs 동일. 원장 두 값만 갱신, producer 식별 불변. `grid_fit_v5` dirty=true 는 같은 호출의 앞 영수증 갱신 때문(74~79차와 같음; 79차 리뷰어 문장대로 "clean 시작" 과 "각 영수증 생성 시점 clean" 은 다른 주장이다).

## §3 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                6ffa98d4 (전체 SHA 발송문)
source_digest                                 eda3feb8f4536511
전체 pytest (tests/)                          0 failed · 1960 passed · 1 xfailed (50:40)   (시작 HEAD = 끝 HEAD = 517f25ff · 미추적 0; 직전 184d34dd 는 2 failed — §4)
strict smoke (scripts/smoke_e2e.sh)           rc 0   (작은 grid/fit/score/restore 계산 포함 — 연구용 새 실행 0)
mutation_replay --check-preimages · -k legacy-ok   전 지점 1회 · 1/1 물었다 · EXPECT 관측값 · (79차 변이 5 는 그대로)
영수증                                        paired core 00db82af4377c3e0… (34) · grid core ffc2e9354215e3b6… (33) · validator eda3feb8f4536511
docs-lint                                     전체 회귀 안에 포함 · 요청문 커밋 뒤 단독 실행값은 발송문에
```

## §4 우리가 스스로 신고하는 것

- 새 시험 두 개는 **처음부터 통과**한다 — 이번 발견은 동작이 아니라 설명의 오류라 RED 가 생길 자리가 없다. 대신 그 동작을 바꾸는 "수정"(ok 대입 이동)을 변이로 등록해 시험이 그것을 잡는지로 확인했다 (1/1).
- 79차 §6 비차단(`normalize_restart_record` 가 새 키가 일부만 있는 행을 legacy_dict 로 내려 관측값을 잃는다)은 이번에 손대지 않았다 — 리뷰어 지시대로 단계 3/4 세대 dispatch 에서 혼합/손상 행 정책(명시 거부 또는 부분 기록 분리)과 함께 정한다. §111 에 이월 항목으로 적었다.
- `paired_fixed5_v4` 의 역사적 `evidence.out` 부재는 그대로다 (새 attach 수용 아님).
- 첫 전체 회귀(`184d34dd`)는 **2 failed** — (1) 계약 §1 의 `src/fitting.py` 줄번호 인용이 docstring 정정으로 4줄 밀려 다시 낡음(1487→1491 · 1442→1446 · 457-471→461-475; 숫자만 갱신) (2) `test_hessian_provenance::test_a_hessian_resolves_curves_from_the_sealed_snapshot` — "이미 'smoke' 로 등록돼 있다 — 'canonical' 로 바꿀 수 없다". **실측**(등록 호출 spy · fixture 두 번 호출 대조): 시험 producer fixture `sign_producer` 의 `curves_manifest` 가 초 단위 timestamp 만으로 달라져 **같은 초 안에 만든 두 fixture 의 content id 가 같다**. 새 gated 모듈(smoke namespace)의 마지막 producer(`g79_05b`)와 바로 뒤 모듈 `test_hessian` 의 producer(일반 tmp → canonical)가 같은 초에 만들어지면 충돌 — 기존 fixture 의 잠재 flaky 가 모듈 인접 정렬로 드러난 것 (`c77674f6` 회귀는 초 경계를 넘어 통과). 수정: fixture spec 에 호출별 nonce (`tests/test_fitting.py`, RUN_SCOPE 밖). production 코드·등록부 규칙은 건드리지 않았다 — content-addressed 등록의 cross-namespace 배타는 의도된 동작이다.

## §5 리뷰어에게 묻는 것

1. G79-N1 정정(설명 · 한정 회귀 `g79_03c`/`g79_03d` · 변이)이 잔여를 닫는가.
2. 단계 2 **종결** 판정. 종결이면 단계 3(묶음 1·2 planned/realized schema · ID preimage · 묶음 3 provider DAG, no-warm 경로 명시 분기)은 **새 사용자 승인** 뒤 열겠다 — 이번에 착수하지 않는다.
3. 실행 GO 아님 · grid_fit_v5 진단 전용 · 새 연구 계산 0 확인.

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **G79-N1 정정과 단계 2 종결 판정을 요청한다. 실행 GO 도 단계 3 착수도 묻지 않는다.**
