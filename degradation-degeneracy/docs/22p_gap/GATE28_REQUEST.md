# 28차 게이트 리뷰 요청 — 27차 P0 둘 + P1 여덟 + P2 하나

> 자기 완결 문서다. 숫자는 옮겨 적지 않는다 — 영수증·투영·원장이 정본이다.

```yaml
브랜치:     origin/claude/14-gate-code-review-9qkx05
대상 커밋:   352f8f159b89ee41ec8c080316cc33b845516554
코드 커밋:   46fb7ff9…      # RUN_SCOPE 변경이 들어간 커밋
직전 대상:   92ba0b109d105d636bc0e181da1a3cae89d12e7e   (27차, NO-GO)

source_digest:
  27차:  d3b1644f7ebe5bda
  현재:  62f45be76f526ce8

재현:      git checkout 352f8f159b89ee41ec8c080316cc33b845516554
           cd degradation-degeneracy
```

## 0. 요청 판정

| 대상 | 요청 |
|---|---|
| 27차 P0 둘 (receipt lifecycle · finalize-only · 등록) | 닫혔는가 |
| P1 3~10 · P2 10 | 어디까지인가 |
| 「최소 증거」 12항목 중 **1~10** | 대응표 §3 |
| 11 (quarantine containment) · 12 (analyzer canary) | **다음 라운드** — §5 |
| 묶음 9 완료 · gate 배선 · 묶음 2 동결 | **요청하지 않는다** |
| 새 Stage 3 leg · 대규모 재실행 | **요청하지 않는다** |

리뷰 권고대로 **범위를 넓히지 않았다.** receipt lifecycle 과 registration
atomicity 를 먼저 닫고, containment wrapper 와 canary 는 다음 라운드다.

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
352f8f159b89ee41ec8c080316cc33b845516554
$ git status --short
(빈 출력)

$ python3 -m pytest tests/ -q
810 passed, 1 xfailed in 268.53s (0:04:28)

$ ./scripts/smoke_e2e.sh          # 46fb7ff9 (clean) 에서
✅ pipeline smoke 통과
⚠ 보존 gate 미완료 (계약 v4 묶음 9) — 새 leg 실행 금지.

$ python3 -c "…source_digest()"
62f45be76f526ce8

$ python3 docs/22p_gap/make_receipt.py paired_fixed5_v4 --check
✅ paired_fixed5_v4: core 재생성 바이트 동일

$ python3 wiki/tools/lint.py
RESULT: 0 errors
```

## 2. 리뷰가 준 반례 셋이 전부 재현됐다

셋 다 직전 라운드에서 **내가 §35.7 에 적어 둔 형태** 그대로다 —
*시험의 이름이 실제로 하는 일보다 강하다.*

| 반례 | 원인 |
|---|---|
| receipt 를 read-back 직후 지워도 성공·등록 | `_drop_from_cas()` 가 receipt **생성 전에만** 돌았다. 요청문은 "member/manifest/**receipt** 훼손" 이라고 적었는데 나열한 시험에 receipt 가 없었다 |
| `finalize_only()` 가 `rescore_calls=2` | `_finalize()` 재호출 → restore→validate→rescore→**새 receipt 생성** 반복 |
| foreign journal 로 `ok=True` | `_register` 가 충돌 시 내용 비교 안 함, `is_registered` 가 JSON 을 읽지도 않음 |

### 2.1 이번에는 검사를 더하지 않고 **API 를 줄였다**

```python
finalize_only(leg_id, backend, index_path)     # hooks 가 없다
```

hook 을 받지 않으면 재계산이 **구조적으로 불가능**하다. 회귀는
validate/rescore 호출 횟수를 세어 `0` 인지 확인한다 — "안 불렀다" 를 문장이
아니라 카운터로 증명한다.

| 무엇 | 검사로 막던 것 | 구조로 바꾼 것 |
|---|---|---|
| 재계산 | 주석 | hook 을 **인자에서 제거** |
| 회수 가능성 | 한 번 read-back | 등록 직전 재회수가 **필수 경로** |
| 등록 | 파일 존재 | index 결속 대조가 `is_registered` **정의** |
| frozen | CLI 인자 검사 | **쓰기 지점** 검사 |

## 3. 「최소 증거」 1~10

| # | 요구 | 회귀 |
|---|---|---|
| 1 | receipt read-back 직후/after-publish 삭제·변조가 성공을 막는다 | `test_losing_the_receipt_after_readback_stops_the_transaction[3종]` |
| 2 | `finalize_only()` 가 hook 을 **한 번도** 호출하지 않는다 · 없거나 다르면 fail-closed | `test_finalize_only_never_recomputes` (호출 카운터) · `test_finalize_only_fails_closed_without_a_retrievable_receipt` |
| 3 | foreign/empty/truncated journal · partial write · same-leg 충돌 | `test_a_foreign_registration_journal_is_refused` · `test_a_truncated_registration_journal_is_not_a_registration[3종]` · `test_a_partially_written_index_entry_is_never_visible` · `test_concurrent_publish_of_the_same_leg_admits_exactly_one` |
| 4 | manifest schema·집계·root digest·중복·traversal · leg ID traversal | `test_a_manifest_that_lies_about_itself_is_refused[4종]` · `test_duplicate_member_paths_are_refused` · `test_a_manifest_member_cannot_escape_the_restore_root` · `test_a_leg_id_cannot_escape_the_index_directory[8종]` |
| 5 | output manifest 의 path·size·file SHA·producer | `test_output_manifest_must_bind_real_bytes` · `check_output()` |
| 6 | `_F4_주의`·`_채점원본` flag·sealed 삭제가 equality 를 실패시킨다 | `test_citation_safety_metadata_is_not_thrown_out_of_the_hash` · `test_citation_safety_flags_are_checked_by_value[4종]` · `test_a_receipt_with_nothing_to_compare_is_not_agreement` |
| 7 | OS 독립 core — POSIX 경로 · LF | `test_receipt_core_paths_are_os_independent` |
| 8 | frozen direct-API 거부 · cohort 경로 봉쇄 · 행/key 완전성 · 승격 원자성 | `test_the_frozen_guard_lives_at_the_write_primitive_not_the_cli` · `test_promotion_happens_only_after_the_recomputation_verdict` · cohort 순회 회귀 안의 경로·행수·objective key 검사 |
| 9 | closed design validator · objective order · bank index · NFC | `test_the_design_spec_key_set_is_closed` · `test_objective_order_is_part_of_design_identity` · `test_numeric_and_unicode_domains_are_closed` |
| 10 | cross-generation canonical 을 reason 만으로 허용하지 않는다 | `test_claim_roles_are_a_machine_contract_not_free_prose` + `CLAIM_STATUS.role_compatibility` |

11·12 는 §5.

## 4. P1-6 — 안전 문구를 해시 밖으로 버렸다

26차에 정규 view 를 만들면서 `SEMANTIC_SKIP` 에 `_F4_주의` 를 넣고 "재채점이
만들 수 없는 실행 메타" 라고 적었다. **틀렸다.** 그것은 `summarize()` 가
결정론적으로 만드는 인용 금지 경고다 (`src/scoring.py:369`). 떼어 놓으니
리뷰의 반례가 성립했다 — `"인용하지 말 것"` → `"인용해도 안전"` 으로 바꿔도
digest 가 같다.

`_채점원본` 은 실제로 재채점이 못 만들지만 그 안에 `canonical`·`봉인상태`·
`인용가능` 이 있다. equality 로 못 보는 것은 **명시적 assertion** 으로 본다
(`_citation_safety`) — `fits_sha256` 도 재채점한 파일과 대조한다.

그리고 산출이 하나뿐일 때 `_outputs_agree()` 가 `True` 였다 — 비교 대상이
없는데 "일치" 다. 이제 봉인본이 없으면 **비교 불가**로 실패한다.

## 5. 다음 라운드로 미룬 것 (범위를 넓히지 않았다)

| # | 무엇 | 왜 미뤘나 |
|---|---|---|
| 11 | quarantine containment E2E | Q1 답의 (b') wrapper 다. `run.sh`·`src.fitting` 진입점을 바꾸는 일이라 receipt lifecycle 이 닫힌 뒤에 하는 것이 리뷰 권고와 맞는다 |
| 12 | analyzer canary | Q3 답대로 fixture + real-path 두 층. containment 가 먼저다 |

계약 §13 도 묶음 9 를 **부분**으로 유지한다.

## 6. 아직 열려 있다고 스스로 적는 것

1. `run.sh`·smoke 의 **필수 gate 로 배선되지 않았다.**
2. 실제 운영 backend canary 가 없다 (local `file+cas://` 로 의미만 검증).
3. `planned_leg_index` 가 실제 leg 원장과 결속되지 않았다.
4. 묶음 2 는 domain 을 닫았지만 **실제 v6 격자 실행과의 E2E** 가 없다.
5. `os.link` 기반 commit 은 hardlink 를 지원하는 FS 를 전제한다 — 실제 backend
   에서는 conditional put 으로 갈아야 한다.

## 7. 질문

**Q1 — `_채점원본` 재구성 vs assertion.** 지금은 그 블록을 정규 view 에서 빼고
안전 flag 를 별도 assertion 으로 검사한다. 대안은 재채점 쪽에서 그 블록을
**재구성**해 equality 로 넣는 것인데, 그러면 `인용가능` 을 재채점이 스스로
주장하게 되어 순환이 된다고 봤다. 이 판단이 맞는가? 아니면 재구성하되
`인용가능` 만은 봉인본에서 읽어 별도 검사하는 편이 나은가?

**Q2 — `os.link` 의 대체.** local CAS 에서 no-replace commit 을 `os.link` 로
했다. 실제 backend 에는 hardlink 가 없고 conditional put(If-None-Match) 이
대응물이다. 지금 backend 추상에 `commit_if_absent(path, bytes)` 를 하나 두고
local 은 link, 원격은 conditional put 으로 구현하는 방향이 맞는가?

**Q3 — containment 의 진입점 범위.** Q2 답의 "가장 낮은 공통 resolver" 를
받아들인다. 지금 `results/` 를 여는 곳은 `src/io.py` 의 로더들과
`src/scoring.py`·`docs/22p_gap/*.py` 다. `require_registered(ref)` 를
`src/io.py` 한 곳에 두면 충분한가, 아니면 `open()` 수준의 wrapper 가
필요한가? 전자면 `pd.read_parquet(path)` 직접 호출이 남는다.
