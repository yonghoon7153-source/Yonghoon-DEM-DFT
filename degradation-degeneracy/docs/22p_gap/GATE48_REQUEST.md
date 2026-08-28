# 48차 게이트 리뷰 요청 — 묶음 9 (producer identity 정의 · 계획 spec · 원장 원자성)

```yaml
대상 커밋:   1f9587cd98c733ffbc44f704bd5dd966e8703587
브랜치:      claude/14-gate-code-review-9qkx05
직전 판정:   47차 NO-GO — "producer 봉인과 계획 lifecycle이 실제 진입점에서 열려 있다"
전체 시험:   1272 passed · 1 xfailed · 0 failed (슬라이스 실행 — 아래 §0)
strict smoke: 단계 1–5 통과 (provenance 두 산출물 ✅) · 6단계부터 미도달 — **미완**
변이 재생:   scenario_total 64 · executable 59 (전부 물었다) · declared 5
cohort:      g1 frozen · g2 **frozen(48차에 얼렸다)** · g3_2026_08_28 **active**
projection:  ad598fe77e75afec (행 바이트 g2 와 동일)
producer:    908503e65162e7d9 → bbb1c4d6fc982610 (**정의가 바뀌었다** — §2)
compute:     d6619c2c32438e65 → 6f44ae4a3ce50d4d
receipt:     core_sha b9322e4495d976a4
source_digest: e77598f97c40e809
```

원장은 `docs/08_REVIEW_RESPONSE.md` §56, 계약은 `docs/22p_gap/STAGE3_CONTRACT.md`
§13.3.1 · §13.3.2 · §13.3.3 · §13.4.

## §0 실행 환경의 한계 — 먼저 신고한다

이 세션 환경은 **턴을 넘기는 background 실행이 유지되지 않는다** (프로세스가
약 4분마다 회수·재시작된다). 그래서 전체 시험과 변이 재생을 한 번에 완주시키지
못했고, 호출당 예산(약 118초) 안에 들어가는 **슬라이스로 나눠** 전수 확인했다.

- 전체 시험: 파일/노드 슬라이스 9회 합계 **1272 passed · 1 xfailed · 0 failed**
- 변이 재생: `-k` 그룹 슬라이스 32회로 **64 scenario 전수**
- **미실행 1건**: `test_receipt_validation_actually_reads_the_restored_root`
  (묶음 복원 + 재검증이라 예산 초과). 같은 작업을 하는 `make_receipt.py` 는
  같은 트리에서 `검사 34건 · core_sha b9322e4495d976a4` 로 통과했다.
- **strict smoke 미완**: 단계 5까지 통과하고 6단계(공정 paired)에서 잘렸다.
  통과가 아니라 **미완**으로 읽어 달라.

## 조건별 대응

| 47차 조건 | 무엇을 바꿨나 | 회귀 |
|---|---|---|
| P0-1 producer 바이트 결속 | 모든 `*.projection.yaml` 이 `analyzer.producer_semantic_sha256` 을 선언해야 하고 sink·reader 가 원장 pin 과 대조 | `..._a_stage_from_another_producer_is_refused_with_the_pin_unchanged` · `..._an_inherited_leg_must_also_declare_the_sealed_producer` · `..._a_leg_manifest_without_a_producer_is_refused` |
| P0-2 닫힘의 네 구멍 | `src.scoring` 건너감 · decorator 포함 · 절단면을 봉인 preimage 에 · 버전 무관 정규형 | `..._producer_digest_crosses_into_src_scoring` · `..._breaking_the_crossing_..._is_fail_closed` · `..._producer_digest_sees_decorators` · `..._widening_the_producer_cut_moves_the_digest` · `..._producer_digest_is_the_same_on_every_python_here` |
| P0-3 claim 배타성 | public gate 가 **자동 재개하지 않는다** · resume 은 attempt token 요구 · 재개 때 살아 있는 원장 authority 재조회 | `..._two_public_authorizations_do_not_both_enter_compute` · `..._resuming_requires_the_owner_token` · `..._a_revoked_plan_stops_a_live_claim` · `..._a_phase_cannot_be_recorded_without_the_owner_token` |
| P0-4 lifecycle 배선 · `full_bundle` 날조 | `run_grid`·`run_fit` 이 성공 직후 phase 를 닫는다 · `finalize_leg` 이 묶음을 **디스크에서** 확인하고 확인한 만큼만 적는다(`no_bundle`) | `..._finalize_does_not_fabricate_a_full_bundle` · `..._finalize_records_what_it_could_verify` |
| P0-5 run spec · `--leg` | `leg_run_spec()` 다리 단위 **닫힌** spec · 계획이 `run_spec:` 을 담고 digest 일치 강제 · 두 모듈이 `--leg` 수용, `run.sh` 가 export | `..._the_leg_run_spec_seals_what_actually_gets_computed` · `..._refuses_an_undeclared_axis` · `..._both_phase_entry_points_accept_the_leg_flag` · `..._the_grid_entry_point_refuses_an_unplanned_leg` |
| P0-6 원장 원자성 | `_ledger_lock()`(flock) 임계 구역 + `_atomic_write_text()` · `planned→running` 전이 · `check_id()` 일원화 | `..._two_concurrent_finalizations_lose_no_leg` · `..._two_phase_records_do_not_overwrite_each_other` · `..._a_claim_marks_the_plan_running` · `..._a_leg_id_cannot_escape_the_claims_root` |
| P0-7 generation 조상 | `_open_child_dir()` 로 `out`→`gen`→`<gid>` 를 **성분마다** 붙잡는다 | `..._a_symlinked_gen_ancestor_never_holds_a_generation` · `..._a_reader_refuses_a_generation_under_a_symlinked_gen_ancestor` · `..._the_generation_namespace_is_held_component_by_component` |
| P0-8 smoke 승격 · fit gate | `assert_not_smoke_provenance()` 를 보고서·보관 sink 에 · `src/fitting.py` 자체 gate | `..._a_smoke_run_cannot_be_promoted_to_a_canonical_report` · `..._the_report_writer_refuses_a_smoke_input` · `..._the_archive_sink_refuses_a_smoke_input` · `..._the_fit_entry_point_refuses_an_unplanned_leg` |
| P1 변이 증거 | 0건 선택 rc 2 · 신고 항목 registry 등록 · 집계 이름 분리 · 순서 증인 교정 · `pytest-json-report` 고정 | `mutation_replay.py` |

## 실측한 것 (주장이 아니라 출력)

### 1. `--leg` 는 켜는 순간 실행이 죽는 축이었다

```
$ python -m src.grid --leg L --out results/_smoke/x --dry-run
grid.py: error: unrecognized arguments: --leg L      # rc 2
```

리뷰어는 "export 안 돼서 `grid_fit_v4` 를 claim 한다" 고 했는데, 실제로는 **두
모듈 다 그 인자를 선언하지 않았다.** `run.sh` 가 그것을 하위로 넘기므로 46차의
`--leg` 는 아무도 쓸 수 없었고, gate 는 한 번도 진짜 다리 이름을 본 적이 없다.

### 2. producer 정규형이 인터프리터마다 세 값이었다

같은 바이트: 3.11 `908503e65162e7d9` · 3.12 `d4ae1c027b434e83` ·
3.13 `aa1cf2cf045c41ea`. 원인 둘 — `ast.dump` 는 3.12 의 `type_params`,
`ast.unparse` 는 PEP 701 의 f-string 따옴표 재사용(**같은 AST, 다른 렌더링**).
`_ast_canon()` 이 렌더링을 직접 한다: `_fields` 중 빈 값은 빼고(새 버전이 더한
필드는 기본값이 비어 있다), f-string 은 `JoinedStr(values=[...])` 구조로만 적는다.
**실측: 3.10·3.11·3.12·3.13 모두 `bbb1c4d6fc982610`.**

### 3. 원장 lost update 를 재현했다

```
결과 {'M': None, 'L': None}     # 두 finalize 가 모두 성공을 돌려줬다
원장 legs=['L', 'done']         # M 이 사라졌다
```

`phase_done()` 도 같았다 — grid/fit 동시 기록에서 하나가 사라져 `('fit',)` 만
남고, `finalize_leg()` 이 "phase 가 남았다" 며 10시간 계산을 다시 돌리게 한다.

### 4. 봉인이 실제로 게시를 막아 **새 cohort 로 갔다**

producer 정의가 바뀐 뒤 g2 pin 을 고쳐 재게시하려 하자:

```
✗ `CURRENT` 이 봉인한 원장 record 가 지금과 다르다 (ea56c4ed11d4 ≠ c47d4155ca71)
  — cohort lifetime 동안 원장 record 는 고정이다. 새 cohort ID 와 새 출력
  디렉터리로 가라 (계약 §13.3.2)
```

계약이 시킨 대로 g2 를 얼리고 `g3_2026_08_28` 로 갔다. 행 바이트는 g2 와
동일하다 — 그 사실은 회귀가 확인하는 것이지 cross-cohort 인용의 근거가 아니다.

## 이 라운드가 **스스로 발견한** 결함 둘 (47차 조건 밖)

### A. cohort 를 **얼리는 것**이 그 게시를 무효화하고 있었다

g2 를 frozen 으로 옮기자 그 cohort 의 `CURRENT` 가 봉인과 어긋났다
(`ea56c4ed11d4 ≠ fba9073e065d`). `status` 가 `_LEDGER_AUTHORITY` 안에 있었기
때문이다. frozen cohort 는 재게시할 수 없으므로 이것은 **영구 재검증 불가**다 —
보존 저장소에서 뒤집힌 결론이다.

봉인의 일은 게시된 바이트의 **뜻**이 흔들리지 않게 하는 것이다(`legs`·`pin`·
`cross_leg_comparison`·`cohort_id`·`dir`). lifecycle 상태는 그 뜻이 아니다.
`_LEDGER_UNSEALED = ("status",)`.

`frozen → active` 로 되돌려 쓰는 것은 봉인이 아니라 **살아 있는 원장**을 읽는
`_assert_writable()`·pre-flight·임계 구역 재조회가 막는다. 봉인은 과거의 사본이고
쓰기 권한은 현재의 사실이다.

### B. 봉인에서 뺀 필드의 **검사까지** 함께 사라졌다

A 를 고치자 회귀 5건이 빨개졌다 — `_LEDGER_AUTHORITY` 가 **검사 대상**과
**봉인 대상**을 겸하고 있어서 `status` 를 빼자 46차의 enum 검사
(`Active`/`retired`/`ACTIVE`/`""`)가 함께 없어졌다. 둘을 갈랐다:
`_LEDGER_AUTHORITY`(검사) / `_LEDGER_SEALED`(= AUTHORITY − UNSEALED).

43차 요구("게시 도중 freeze 되면 옛 writer 는 진다")와 충돌하지 않는다 —
그 검사를 임계 구역의 **live status 재조회**로 옮겼다.

## 변이 재생이 잡은 것 (전수 64)

세 라운드 만에 처음으로 전수를 돌렸고, **아홉을 잡았다. 전부 이번 라운드가
만든 것이며 시험 suite 는 하나도 보지 못했다.**

| 부류 | 무엇 | 어떻게 고쳤나 |
|---|---|---|
| preimage 사망 4 | P0-7 이 `_staging_entries` 를 나누고 reader 를 helper 로 옮기며 대상 줄이 사라졌다 (`staging-nlink-one`·`staging-regular-only`·`children-read-through-dirfd`·`module-gate-before-side-effects`) | runner 가 "preimage 가 0번" 으로 **fail-closed** 한 것은 옳다. 현행 소스로 맞췄다 |
| 자리 합쳐짐 2 | 검증 통로가 helper 하나로 모이고 call site 가 셋이 됐다 | `reader-*` 는 helper body 로 옮기고, `idempotent-*` 는 고유 자리가 없어 **신고**(없는 자리를 만들지 않는다) |
| 방벽이 둘이 됨 2 | 내가 이번에 더한 guard 가 옛 mutant 를 가렸다 — live status 재조회가 `ledger-seal-record` 를, `planned→running` 이 `claim-is-atomic`(`O_EXCL`)을 | **중복이라 지우지 않는다.** 2-site 로 47차 상태를 복원해 그 쌍이 일하는지 본다 |
| **증인 가려짐 1** | staging alias 시험의 alias 대상이 producer 를 안 밝혀서, nlink/regular guard 를 지워도 **P0-1 의 producer 결속이 먼저** 거부했다 — 빨갛지만 **선언한 이유가 아니다** | alias 대상도 producer 를 담게 해서 이 시험의 축이 증인이 되게 했다 |

마지막 것이 이 machinery 가 존재하는 이유다: 시험은 초록/빨강만 보고, **왜**
빨간지는 보지 않는다.

## 신고 (실행하지 않고 이유를 적는다) — 5

`generation-owns-its-bytes` · `proof-until-equals-lease` · `warm-consumer-wiring` ·
`public-lifecycle-in-two-publisher-fixture` · `idempotent-shares-the-validator`

## 반증해 주기를 바라는 지점

1. **`leg_run_spec` 의 key 집합이 정말 닫혔는가** — grid 4축(`config_digest`,
   `condition_ids_sha256`, `n_conditions`, `out`) · fit 3축(`config_digest`,
   `objectives`, `out`) 밖에서 결과를 바꾸는 축이 남아 있는가. 특히
   `--base-config`·`--reference`·`--bounds`·`--n-restarts`·`--clean`·
   `--no-warm-start`·`--no-adaptive` 는 결과를 바꾸는데 spec 에 **없다**.
   이것이 구멍이라면 반례를 보고 싶다.
2. **`_ast_canon` 의 "빈 값은 뺀다" 규칙** — 새 인터프리터가 더한 필드가
   기본값으로 비어 있지 **않은** 사례가 있는가. 있으면 그 버전에서 봉인이 깨진다.
3. **`_LEDGER_UNSEALED` 의 경계** — `status` 말고도 봉인에서 빼야 할(또는
   절대 빼면 안 되는) 필드가 있는가. B 는 이 경계를 한 번 잘못 그었다가
   회귀에 잡혔다.
4. **`_ledger_lock` 의 범위** — flock 은 같은 기계 안에서만 유효하다.
   `finalize_leg → resume_claim` 경로에서 claim lock 과 ledger lock 이 **다른
   파일**이라 교착이 없다고 보는데, 중첩 순서가 뒤집히는 호출 경로가 있는가.
5. **P0-4 의 미완** — `phase_done` 호출은 배선했으나 계획된 다리로
   grid→fit→finalize 를 **실제로 한 번** 통과시킨 실측이 없다.
6. **§0 의 미완 둘** — strict smoke 6단계 이후와 미실행 회귀 1건.
   이것들 없이 GO 를 줄 수 없다면 그 판단을 받겠다.

## 아직 아닌 것

| 항 | 상태 |
|---|---|
| `os.replace` 직전~직후 창 | 전제로 배제 (계약 §13.3.1) |
| 두 phase 를 **실제로** 돌린 end-to-end lifecycle 영수증 | 미착수 |
| `run_transaction`·`finalize_only` 의 production 호출자 | 여전히 없다 |
| baseline·sweep1d·wsweep 의 계획 gate | 미착수 (grid·fit 만) |
| 실물 object-lock provider adapter · power-loss ordering · publisher 전용 OS principal | 미구현 (별도 acceptance) |
| 외적타당도 #48/#49/#50 | 미착수 |
