# 26차 게이트 리뷰 요청 — 25차 선행조건 10건 + 묶음 9 구현 착수

> 이 문서는 **자기 완결적**이다. 25차 리뷰가 `GATE24_REQUEST.md` 를 두고
> "committed 파일 단독으로는 self-contained 하지 않다" 고 지적했으므로,
> 세 라운드가 쌓인 그 파일을 더 늘리지 않고 새로 쓴다. 옛 왕복 기록은
> `GATE24_REQUEST.md` 와 원장 §29~§34 에 그대로 있다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   e1ec91d11222…
코드 커밋:   cedaf922e937…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   d405d1b855e975c2e34974a776c3ac2b6ee99141   (25차, 조건부 GO)
직전 회신:   Gate 24 두 번째 보충 재검증

source_digest:
  이전:  a72c0f3a485c19bb      # 21~24차 내내 고정
  현재:  0b9fb0d4519d34ae      # ★ 이번 라운드에 **의도적으로** 움직였다
  왜:    묶음 9(tools/preserve.py) · 묶음 2(tools/design_wire.py) 구현과
         smoke 의 실행-승인 문구 제거. 셋 다 RUN_SCOPE 다.
  영향:  기존 artifact 는 소급 무효화되지 않는다 (계약 §2.1). `코드_identity`
         검사는 run_spec 이 digest 를 갖고 dirty 가 아닌지만 보므로
         (`src/io.py:1514`) 옛 산출물 검증은 그대로다 — 이번 영수증이 실측이다.

재현:      git checkout e1ec91d11222… && cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 25차 "다음 회신에 필요한 것" 10건 | 닫혔는가 |
| 묶음 9 acceptance 최소 목록 10단계 + 음성 시험 | 어디까지 통과인가 |
| 묶음 2 (wire schema · arm registry · hash domain · golden) | Q3 대로 앞당겼다 — 동결 가능한가 |
| 묶음 9 **완료** 선언 | **요청하지 않는다** — §5 의 셋이 남았다 |
| 새 Stage 3 leg 실행 · 대규모 재실행 | **요청하지 않는다** |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
e1ec91d11222a0d0d756c523fd4469c984653b4e
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
742 passed, 1 xfailed in 349.35s (0:05:49)

$ ./scripts/smoke_e2e.sh          # e1ec91d1 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.
   이 통과는 실행 승인이 아니다. 보존 트랜잭션은 이 smoke 에 아직 없다.

$ python3 -c "…source_digest()"
0b9fb0d4519d34ae

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

`xfailed` 1건은 발견 9 의 수용조건이다 (§3.9).

## 2. 이번 라운드가 뒤집은 두 가지

### 2.1 회귀가 만든 트랩 — 24차 보충의 수정으로는 부족했다

24차 보충에서 "원자료를 잃은 다리는 기록된 세대 바이트에 대고 검사" 로
고쳤는데, 25차가 **다른 세 회귀가 여전히 전역이라 소용없다** 고 지적했다.
맞다. analyzer 를 고치면 어느 쪽으로도 suite 를 만족시킬 수 없었다.

**cohort** 로 나눴다:

| cohort | dir | status | legs |
|---|---|---|---|
| `g1_2026_08_20` | `docs/22p_gap/warm_probe` | **frozen** | 8 |
| `g2_2026_08_25` | `docs/22p_gap/proj_g2` | **active** | 1 (`paired_fixed5_v4`) |

`row_projection.py --out` 이 새 세대를 **새 경로**에 쓴다. 옛 바이트를 덮지
않는다. 교차-다리 비교는 cohort 안에서만 성립한다.

### 2.2 계산 digest 가 계산 의미를 빠뜨렸다

`_RESTART_SOURCES` 를 넓혀도 `compute_sha256` 이 안 움직였고, breaker 는 파일
전체 SHA 를 일부러 제외하므로 교차비교도 `intact` 로 남았다. 손으로 고른
목록을 **dependency closure** 로 바꿨다.

### 2.3 그 결과 — 내용은 그대로, identity 회계만 엄격해졌다

analyzer 를 g1→g2 로 올리고 `paired_fixed5_v4` 를 새 cohort 에 재생성한 결과:

| | g1 | g2 |
|---|---|---|
| `projection_sha256` | `ad598fe77e75afec…` | **바이트 동일** |
| `restart_projection_sha256` | `84333ad3c19625ca…` | **바이트 동일** |
| `analysis_spec_sha256` · `fits_sha256` | | **바이트 동일** |
| `compute_sha256` | `73c1ac4ba06e59dc` | `45ebcdc85915413a` |
| `row_projection_py_sha256` | `bbb4744256e42b8f` | `147c4b2f3a4ac6e0` |

digest 수정이 계산을 바꾸지 않았다는 직접 증거다. g1 은 py3.12.3/numpy 2.5.2,
g2 는 py3.11.15/numpy 2.4.6 에서 만들었으므로 **runtime 이 equality 축이
아니라는 것**도 같이 실측됐다 (그래서 pin 에 기록만 하고 대조하지 않는다).

## 3. 25차 요구 10건

| # | 요구 | 대응 | 검사 |
|---|---|---|---|
| 1 | 묶음 7/10 "닫음" 철회 + 반례 회귀 | §13 이 이제 **미착수/부분** 둘만 쓴다 | 아래 전부 |
| 2 | allowed-state 제약 · planned lifecycle | 열거 → **제약에서 생성**, 계획 다리는 `planned_leg_index`(묶음 9)로 | `test_preservation_registry_holds_executed_legs_only` |
| 3 | `claim_id × leg_id` role schema | `CLAIM_STATUS.active_claims` 8건 + role enum + 세대 | `test_claim_roles_are_a_machine_contract_not_free_prose` |
| 4 | `archive_bundle.check()` 재사용 전수 rehash | 회귀가 그 함수를 **호출**한다 | `test_full_bundle_payload_members_are_rehashed_one_by_one` |
| 5 | 재생 가능 structured receipt + 결속 | `docs/22p_gap/make_receipt.py` | `test_full_bundle_claims_are_backed_by_a_real_bundle` |
| 6 | 묶음 1 envelope + 묶음 2 wire/golden | `PlannedLeg` · `tools/design_wire.py` + `design_golden.yaml` | `tests/test_design_wire.py` 8건 |
| 7 | 묶음 9 two-phase + hermetic failure fixture | `tools/preserve.py` | `tests/test_preserve.py` 26건 |
| 8 | smoke 의 실행-GO 문구 제거 | 위 §1 출력 | 실행 출력 |
| 9 | exception-specific xfail | 손상 뒤 `ArrowInvalid` 에만 한정 | 전제 파괴 = 정상 FAIL 확인 |
| 10 | committed 요청문 stale 정리 | 묶음 번호 3→9 · 옛 tuple 철회 표기 · **이 문서는 자기완결** | `test_docs_do_not_claim_lost_legs_are_regenerable` |

### 3.9 발견 9 — 왜 xfail 을 좁혔나

함수 전체 `xfail(strict=True)` 는 **전제 fixture 가 깨져도** 녹색이었다.
`raises=` 가 없어 어떤 실패가 예상 결함인지 제한하지 않았기 때문이다.

이제 손상 뒤 `pyarrow.lib.ArrowInvalid` 가 났을 때만 `pytest.xfail()` 한다.
`manifest.yaml` 을 깨뜨려 전제를 무너뜨리는 변이를 넣으면 **`1 failed`** 가
나온다 (xfail 이 아니다). 손상이 실제로 먹혔는지도
`pytest.raises(Exception): pd.read_parquet(fp)` 로 먼저 확인한다.

## 4. 묶음 9 acceptance — 10단계와 음성 시험

`tools/preserve.py` · `tests/test_preserve.py` (hermetic, 26건, 네트워크·실제
산출물 없음).

**불변식: 어느 단계에서 멈추든 public index 는 오염되지 않는다.**

| 25차가 요구한 단계 | 구현 | 회귀 |
|---|---|---|
| 1 planned leg seal (canonical bytes · stable ID) | `PlannedLeg.planned_id()` = 내용 주소 | `wrong_planned_id` |
| 2 private run dir 에서 fixture 생성 | tmp | `_make_run` |
| 3 exact member manifest · byte SHA · semantic digest | `seal_payload` + `_score_manifest` | `test_payload_verification_catches_all_three_shapes` |
| 4 CAS staging upload + read-back 재해시 | `put_if_absent` → `os.replace` · `read_back` | `partial_upload` · `read_back_corrupt` |
| 5 truly empty root 복원 | tmp root, 원본 접근 없음 | `restore_incomplete` |
| 6 복원본에 `validate_provenance` | hook | `validator_raises` · `validator_fails` |
| 7 복원한 fits 만으로 재채점 | hook | `score_raises` · `wrong_semantic_digest` |
| 8 byte+semantic output manifest · receipt | `execution-receipt/v1` | happy path |
| 9 검증 뒤에만 final index atomic publish | `os.replace` | `crash_before_publish` |
| 10 receipt 확인 뒤에만 등록 | 마지막 단계 | `crash_after_publish` |

음성 시험 — 25차 목록 대비:

| 요구 | 상태 |
|---|---|
| member 1바이트 변경 · missing · extra | ✅ (봉인 **뒤** 손상으로 주입 — 봉인 전에 뒤집으면 manifest 가 손상본을 기록해 아무 것도 안 잡힌다) |
| stale payload index / stale receipt | ✅ `stale_payload_index` · immutable index 가 다른 내용 덮기 거부 |
| wrong bundle ID · planned design ID · source digest | ✅ `wrong_planned_id` · `wrong_source_digest` |
| partial upload · crash before/after promotion · retry | ✅ 4건 + `test_rerunning_the_same_transaction_is_idempotent` |
| same digest same bytes idempotency | ✅ |
| same ID different bytes 거부 | ✅ `test_same_leg_id_with_different_bytes_is_refused` |
| empty-root 밖 원본을 읽으면 실패 | ✅ `test_restore_target_must_be_a_truly_empty_root` |
| validator 예외 · score 예외 · wrong semantic | ✅ |
| retention/access capability | ✅ `retention_too_short` · `no_read_access` |
| 실패 bundle 이 public index 에 안 나타남 | ✅ **16종 전부**에서 `index_entries == {}` 확인 |

`test_every_declared_fault_has_a_regression` 이 `FAULTS` 목록만 늘고 검사가 안
늘어나는 것을 막는다.

## 5. 묶음 9 를 **완료로 선언하지 않는 이유** 셋

1. **`run.sh`·smoke 의 필수 gate 로 배선되지 않았다.** 지금은 호출하지 않으면
   그만이고, 그것이 정확히 8월 20일 사고의 형태다.
2. **실제 운영 backend canary 가 없다.** Q1 대로 local `file+cas://` 로
   트랜잭션 **의미**만 검증했다.
3. **`planned_leg_index` 가 실제 leg 원장과 결속되지 않았다** — 묶음 1·6 필요.
   보존 원장의 coverage 기준이 아직 커밋된 투영이라, 새 다리를 돌려도 투영을
   만들기 전에는 회귀가 깨지지 않는다.

## 6. 묶음 2 — Q3 대로 앞당겼다

`tools/design_wire.py` + `tools/design_golden.yaml`.

- **arm registry** 가 계약 §5 2×2 와 회귀로 묶였다 — 표와 코드가 갈리면 실패
- **좌표에 이진 float 금지**, 십진 문자열만
- **십진 정규화** — 초판 golden 이 `0.17` 과 `0.170` 을 **다른 조건**으로
  갈랐다. 그것을 보고 고쳤다. 계약 §4.2 가 경고한 "조용한 merge/split" 의
  숫자판이다
- ID 사슬 `pair_group_id → bank_id → candidate_id` 를 golden 으로 고정.
  arm registry 를 한 글자 고치거나 직렬화 구분자를 바꾸면 golden 이 깨진다
  (변이 2종 확인)
- `EXCLUDED_FROM_PAIR_ID` 에 제외 축과 **이유**를 싣는다 — 제외 결정 자체가
  설계이기 때문이다 (계약 §4.2). 제외 축을 좌표에 넣으면 거부한다

## 7. 스스로 찾은 것 — 영수증이 조용히 낡았다

`tools/` 에 파일을 더하자 `source_digest` 가 또 움직였고(`73c67903` →
`0b9fb0d4`) 커밋된 영수증은 옛 digest 를 들고 있었다. **그런데 회귀가
통과했다** — 영수증과 원장을 서로 비교하기만 했기 때문이다. 24차 보충 발견 5-1
이 지적한 형태가 새 파일에서 재발한 것이다.

영수증이 **현행 검증기**보다 낡으면 실패하도록 고쳤다. 재생성 뒤, dirty 트리와
clean 트리에서 만든 core sha 가 같다 — core/stamp 분리가 의도대로 동작한다는
증거다. 현재 core sha 는 `350342d36585796a` 이고
`make_receipt.py --check` 가 매번 바이트 동일 재생성을 확인한다.

### 7.1 그리고 이번 라운드에 **내가 만든** 복제 둘

자체 diff 를 최소주의 사다리로 훑다가 찾았다 — 24차 보충 Q5 가 경고한 구조적
복제의 실물이고, 둘 다 이번 라운드에 새로 들어온 것이다.

1. **채점 경로가 두 곳에 인라인으로** 있었다 (`row_projection.py` ·
   `make_receipt.py`). 한쪽만 고치면 두 감사 도구가 서로 다른 것을 검증하게
   된다. 초판에 "여기서 갈리면 두 감사 도구가 다른 것을 검증하게 된다" 는
   **주석까지 달아 놓고** 복제를 남겼다 — 주석은 강제가 아니다.
   → `score_canonical()` 하나로 모으고 회귀가 복제를 막는다.
2. **`score-semantic/v1` 한 라벨이 두 바이트 스트림**을 뜻했다.
   `make_receipt._semantic` 은 기본 구분자, `preserve.canonical_bytes` 는
   고정 구분자. 둘 다 산출 manifest 에 같은 canonicalizer 를 적었으므로,
   나중에 두 digest 를 대조하면 영원히 다르다. → 정규화는 한 곳만.

추출 뒤 g2 를 재생성했더니 내용 digest 가 여전히 g1 과 바이트 동일했다 —
추출이 계산을 바꾸지 않았다는 확인이다.

## 8. 변이 시험 — 이번 라운드 전체

| 변이 | 결과 |
|---|---|
| `fits.parquet` **크기 유지** 1비트 반전 | 옛 검사 **통과**(리뷰가 맞았다) · 새 검사 실패 |
| `_RESTART_SOURCES` 확장 | compute digest 이동 확인 |
| `main()` 앞 주석 추가 | compute digest **불변** 확인 |
| arm registry 문자열 1개 변경 | golden design digest 깨짐 |
| 직렬화 구분자 `","` → `", "` | golden + preserve 회귀 2건 깨짐 |
| 없는 claim_id · 중복 · 원자료 없는 canonical · 고아 주장 · 철회 주장 | 5종 전부 실패 |
| 영수증 core 필드 조작 | core sha 불일치로 실패 |
| xfail 테스트의 전제 파괴 | **정상 FAIL** (xfail 아님) |
| 회귀 파일에 `canonical_candidate` literal 재도입 | 계약 밖 토큰으로 실패 |
| 보존 트랜잭션 실패 16종 | 전부 해당 단계에서 멈추고 index 비어 있음 |

## 9. 아직 안 한 것

| 묶음 | 상태 |
|---|---|
| 3 provider DAG · `p_ini` arm solution map | 미착수 |
| 4 `mono_tol`/`material_tol` · stratum · budget adoption | 미착수 |
| 5 실제 `sentinel_panel.yaml` | 미착수 |
| 6 구 `pairing_design_id`·`inference_status` 제거 | 미착수 — 묶음 9 final gate 의 선행 |
| 8 비-git backend URI 형식 | 미착수 |
| 발견 8 (`validate_provenance` fail-closed read) | 수용조건만 xfail 로 고정, 구현 미착수 |

## 10. 질문

**Q1 — 묶음 9 를 gate 로 배선하는 지점.** 지금 `run.sh` 는 fitting 을 돌리고
끝난다. 트랜잭션을 (a) `run.sh` 끝에 필수 단계로 넣을지, (b) fitting 자체를
트랜잭션 안에서 실행할지(= 실패하면 `results/` 도 안 남는다) 결정이 필요하다.
(b) 가 강하지만 ~12시간 실행 중 보존 단계에서 실패하면 계산을 통째로 버리게
된다. 우리 판단은 **(a) + `results/` 는 남기되 "미등록" 으로 표시**인데,
그러면 "보존 없이 끝날 수 있다" 가 다시 열리는 것 아닌가?

**Q2 — 묶음 6 의 이전 범위.** 구 `pairing_design_id`·`inference_status` 를
제거하려면 이미 커밋된 8다리 manifest·summary 를 건드려야 한다. 그것들은 g1
frozen cohort 다. 우리 이해는 **옛 바이트는 손대지 않고, 새 index 가 옛
필드를 읽을 때 adapter 로 변환**하는 것인데 맞는가? 아니면 g1 을 읽는 코드
자체를 legacy reader 로 분리해야 하는가?

**Q3 — `active` cohort 가 1다리뿐인 것.** 현행 트리를 대조하는 다리가
`paired_fixed5_v4` 하나다 (원자료가 남은 유일한 다리). 낡음 감시가 한 다리에
얹혀 있는데, 이것으로 충분한가? 아니면 작은 합성 fixture leg 를 만들어 활성
cohort 에 상시로 두는 편이 나은가?
