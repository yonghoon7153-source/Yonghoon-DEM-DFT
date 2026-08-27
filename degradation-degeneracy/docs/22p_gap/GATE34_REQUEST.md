# 34차 게이트 리뷰 요청 — 33차 P0-1 · P2 · #9

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   76759f9fc71439ad0bb8c3b0234940715042a4bc
코드 커밋:   (row_projection·preserve 변경 포함 커밋 — compare 참조)
직전 대상:   6a656b88…      (33차, P0-3 종결 / 나머지 NO-GO)

source_digest:
  33차:  09d9caae89285f31
  현재:  71321d826194f75a

재현:      git checkout 76759f9fc71439ad0bb8c3b0234940715042a4bc
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| P0-1 (lease 잠금 · 안정 provider URI) | 닫혔는가 |
| P2 (live gate 배선 · 오류를 삼키지 않기) | 닫혔는가 |
| #9 (cohort generation 배선 · CURRENT authority) | 닫혔는가 |
| P0-3 | 33차에 **종결** — 재검을 요청하지 않는다 |
| 실제 provider adapter · power-loss fault model | **미구현으로 신고한다** |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
76759f9fc71439ad0bb8c3b0234940715042a4bc
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
978 passed, 1 xfailed in 387.07s (0:06:27)

$ ./scripts/smoke_e2e.sh
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
71321d826194f75a

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일 · core_sha ec5ec0fa191d19ea

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 세 발견이 같은 형태였다

리뷰의 문장을 그대로 인정한다 — "시험이 다른 축 또는 독립 helper 에 업혀
통과하는 것". 셋 다 **고친 것과 실제로 쓰이는 것이 달랐다**:

| 발견 | 고친 것 | 실제로 쓰이던 것 |
|---|---|---|
| P0-1 | content object 잠금 | durable 의 **증거**인 lease 는 잠금 밖 |
| P2 | verified-receipt helper | live gate 는 backend 없이 호출 → 언제나 `{}` |
| #9 | generation primitive | `build()` 는 여전히 파일별 `os.replace` |

## 3. P0-1 — lease 와 안정 identity

| 축 | 회귀 |
|---|---|
| lease pin·content object 잠금 | `..._lease_object_is_locked_too` |
| journal 의 lease version proof 대조 | `..._forged_lease_version_proof_is_refused` |
| 새 provider 객체로 reopen | `..._reopened_backend_finds_the_same_registration` |
| 안정 식별자 없는 provider 거부 | `..._provider_without_a_stable_identity_cannot_be_used` |

lease 는 자기 digest 를 담을 수 없으므로 version proof 를 **journal** 에 뒀다
(`lease_version`). 리뷰가 제안한 두 방향 중 "journal 에 lease version proof"
쪽이다.

## 4. P2 — live gate 배선

| 축 | 지금 |
|---|---|
| backend 해석 | `preserve_backend.yaml` 이 배선의 정본. `_open_canonical_backend()` |
| journal 은 있는데 backend 를 못 연다 | **오류** (조용한 통과 아님) |
| graph/lease 검증 실패 | **오류** (`continue` 로 숨기지 않음) |
| index 사본 | live 경로에서 receipt 와 대조 |

`..._live_gate_actually_opens_a_backend_when_an_index_exists` 가 합성 index 로
세 방향을 물린다 — 배선 없음 · 배선 있음 · graph 손실.

## 5. #9 — cohort generation 배선

```text
out/gen/<generation_id>/…   ← 내용 주소가 이름. 한 번 쓰고 안 고친다
out/CURRENT                 ← 이 한 파일만 원자적으로 바뀐다
out/<leg>.projection.yaml   ← CURRENT 에서 **파생된** 호환 사본
```

| 축 | 회귀 |
|---|---|
| 한 leg 갱신이 cohort 를 줄이지 않는다 (G0 두 leg → G1) | `..._cohort_generation_keeps_every_leg_and_switches_once` |
| `build()` 가 generation 승격을 쓴다 · reader authority 는 CURRENT | `..._production_writer_and_reader_go_through_current` |
| 실물 active cohort 가 CURRENT 로 게시된다 | `..._active_cohort_is_published_through_a_single_current_pointer` |

frozen g1 은 다시 만들 수 없으므로 옛 layout 그대로 두고, 그 예외를 위
시험이 **명시적으로** 고정한다.

`..._promotion_happens_only_after_the_recomputation_verdict` 의 manifest-last
요구는 없앴다 — 파일별 순서가 사라졌으므로 완화책을 계속 요구하면 구조가
바뀐 뒤에도 옛 모양을 강제하게 된다.

## 6. 변이 — 둘, 둘 다 중복이었다

| 물지 않은 변이 | 왜 | 처리 |
|---|---|---|
| lease 의 `version_id` 재비교 | `describe_locks` 가 version 을 **키로** 조회하므로 dict 반환 자체가 일치를 뜻한다 | 삭제 |
| content 의 `version_id` 재비교 | 같은 이유 | 삭제 |

지난 세 라운드는 "시험이 약해서" 물지 않았는데 이번 둘은 "검사가 중복이라"
물지 않았다.

## 7. 남은 것 — 인프라 제약

| 항 | 상태 |
|---|---|
| 실제 object-lock provider adapter | **미구현**. 계약 7연산과 canary 는 고정 |
| power-loss ordering fault model | **미착수**. `os._exit` 은 un-fsynced entry 를 잃지 않는다 |
| `digest → generation` value | **선언** — 실행 산출물에 그 필드가 없다 |

## 8. 산출물

영수증을 clean tree 에서 다시 만들었다. g2 cohort 는 이제 `CURRENT`
generation 으로 게시된다 (`gen/` + pointer + 호환 사본). 원장 pin:

```text
compute_sha256                    a7def130d68d79a1 → fa05b081fbca25ef
row_projection_py_sha256          a30847533ef8fcfd → e876bd425400143b
verification_receipt_core_sha256  919e61bb… → ec5ec0fa…
validator_identity.source_digest  09d9caae89285f31 → 71321d826194f75a
```

행 바이트는 안 움직였다. `g1_2026_08_20` 은 frozen — 손대지 않았다.
