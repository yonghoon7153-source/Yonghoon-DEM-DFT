# 47차 게이트 리뷰 요청 — 묶음 9 (계획 lifecycle · producer 봉인 · generation root)

```yaml
대상 커밋:   49b89d67caa40cf92fba45dc02e6ed07b2faf9b8
브랜치:      claude/14-gate-code-review-9qkx05
직전 판정:   46차 NO-GO — "계획 lifecycle 부재·smoke 이탈·producer 혼합"
전체 시험:   1243 passed · 1 xfailed
strict smoke: ✅ pipeline smoke 통과 (clean 커밋에서)
변이 재생:   scenario 58 · 실행 55 · 신고 3 · site 58 · rc 0
projection:  ad598fe77e75afec (행 바이트 46차와 동일)
producer:    908503e65162e7d9 (라운드 내내 불변 — 아래 참조)
receipt:     core_sha fd0791143e278c75
source_digest: 209dc305783f62a6
wiki lint:   0 errors
```

46차의 조건에 대응했다. 원장은 `docs/08_REVIEW_RESPONSE.md` §55, 계약은
`docs/22p_gap/STAGE3_CONTRACT.md` §13.3.2 · §13.3.3 · §13.4.

## 조건별 대응

| 46차 조건 | 무엇을 바꿨나 | 회귀 |
|---|---|---|
| 3. generation validator (root) | root 를 `O_DIRECTORY\|O_NOFOLLOW` 로 열고 child 는 **붙잡은 dirfd** 의 `openat`/`fstatat` 으로만 | `..._generation_root_symlink_is_never_read_as_a_generation` · `..._never_reused_by_the_publisher` · `..._holds_a_directory_fd_for_its_children` |
| 5. producer pin | `producer_semantic_sha256` 을 `_PIN_SEALED` 에 — **AST 정규형** · `_PRODUCER_CUT` 으로 게시·원장 authority 절단 | `..._producer_change_cannot_mix_two_producers_in_one_generation` · `..._producer_semantic_digest_ignores_comments_but_not_computation` · `..._excludes_the_publication_path` |
| 6. pre-write authority | `_ledger_cohort_preflight()` 가 **첫 write 전에** frozen·schema 를 거른다 | `..._frozen_cohort_publish_writes_nothing_before_it_refuses` |
| 7. CURRENT 뒤 stale PENDING | 완전한 CURRENT 가 잔여 PENDING 을 supersede (bootstrap 중에는 46차 규칙 유지) | `..._complete_current_supersedes_a_leftover_pending` · `..._pending_from_a_different_lineage_is_still_refused` |
| 8. versions 후보 | `_repair_source`·`_repair_target` 을 검증 helper 로 + **두 철자**를 세는 구조 검사 | `..._repair_lookups_go_through_the_validated_version_snapshot` · `..._no_version_enumeration_bypasses_the_helper` |
| 9. 변이 증거 | 셋을 충실한 축으로 (아래 표) | `mutation_replay.py` rc 0 |
| 11-a. prospective lifecycle | `prospective_legs` ↔ `legs` 분리 · claim → phase → finalize | `..._prospective_leg_has_a_state_that_passes_every_gate` · `..._crashed_attempt_finalizes_without_recomputing` · `..._finalizing_moves_the_leg_from_prospective_to_executed_roster` |
| 11-b. exact run spec | `run_spec_digest` 봉인 + `O_EXCL` 원자적 claim | `..._exactly_one_attempt_enters_compute` · `..._claim_seals_the_exact_run_spec` |
| 11-c. module entrypoint | `src/grid.py` 가 **첫 부작용 전에** 공유 gate | `..._module_entrypoint_is_gated_not_just_the_wrapper` · `..._run_grid_calls_the_gate_before_its_first_side_effect` |
| 11-d. smoke 격리 | `is_inside_namespace()` — `..` 금지 · 성분 symlink 금지 · 실물 포함 | `..._traversing_path_is_not_inside_the_smoke_namespace[2]` · `..._symlinked_path_...` · `..._fail_closed_on_a_symlinked_component` |
| 11-e. dry-run | 면제 **삭제** | `..._a_dry_run_still_needs_authorization` · `..._run_sh_has_no_flag_exemption_for_the_plan_gate` |
| 계획 parser | publisher 와 같은 `dir`·`status` 규칙 + 반대 방향 exact equality | `..._plan_parser_refuses_a_cohort_dir_outside_the_repository` 외 7 |
| 소급 8건 | `authorization_kind` enum + `planned_coverage()` | `..._committed_ledger_reports_no_gate_backed_execution_yet` |
| 12. 실물 adapter·power-loss·principal | **미착수 — 신고 유지** | — |

## 이번 라운드의 핵심 판단 — producer 를 어떻게 봉인했나

46차가 producer 를 봉인 밖에 둔 이유("주석 한 줄에도 움직여 라운드마다 새
cohort")는 증상이었고, 원인은 `build()` 가 뿌리라 `compute_sha256` 닫힘이
**publisher 전체를 빨아들인 것**이었다. 그래서 셋을 했다:

1. `_PRODUCER_CUT` — 게시(`promote_cohort_generation`)와 원장 authority
   (`_ledger_*`·`_assert_writable`·`_cohort_dir`)를 닫힘에서 잘라 낸다.
   그 코드는 **바이트를 만들지 않는다.**
2. `_ast_normal()` — 각 정의를 AST 정규형으로 (주석·docstring·서식 제거).
3. 절단면 이름이 사라지면 **fail-closed** — 닫힘이 조용히 넓어질 수 없다.

**실측**: 이번 라운드에 publisher·원장 authority·계획 lifecycle 을 크게 고쳤는데
`producer_semantic_sha256` 은 `908503e65162e7d9` 그대로였고 (그래서 이미 게시된
pointer 가 유효했다 — 마이그레이션이 필요 없었다) 같은 기간 `compute_sha256` 은
세 번 움직였다.

## 변이 재생이 이번 라운드에 잡은 것

46차 runner 였다면 넷 다 "물었다" 로 셌을 것들이다.

| 잡힌 것 | 실제 원인 | 처리 |
|---|---|---|
| `planned-status-is-not-standing` | fixture 가 frozen cohort 라 **frozen guard** 가 대신 거부 | active+executed leg 로 옮겨 status 축만 남겼다 |
| `staging-regular-only` | predicate 만 지워도 `O_NOFOLLOW` 가 ELOOP → 그 오류가 증인 | `O_NOFOLLOW` 까지 되돌리는 **2-site** (실제 symlink 게시가 일어난다) |
| `children-read-through-dirfd` | `dir_fd` 가 두 자리라 하나만 지우면 구조 검사가 통과 | **2-site** |
| `retrospective-is-not-an-authorization` | parser 가 이미 `retrospective ⇒ executed` 를 강제해 **도달 불가능** | 중복이므로 **검사를 삭제**했다 |
| `generation-owns-its-bytes` | 46차 구조 변경으로 옛 exploit 이 **표현 불가능** | 신고로 옮기고 사유를 적었다 |

## 신고하는 한계 (공격 대상)

1. **`os.replace` 직전~직후 창** — 전제로 배제 (§13.3.1).
2. **smoke 산출의 typed provenance 가 아직 없다** — namespace 격리까지만 했다.
   `archive_results.sh` 와 report 는 여전히 source namespace 를 거부하지 않으므로,
   같은 principal 이 비싼 실행을 `results/_smoke/` 로 밀어 넣고 나중에 승격하는
   경로가 남아 있다. **다음 라운드로 신고한다.**
3. **`src/fitting.py` 모듈 gate 미배선** — `grid` 만 했다. `fit` 직접 호출은
   아직 `run.sh` 밖에서 계획을 보지 않는다.
4. **`baseline`·`sweep1d`·`wsweep` 은 gate 밖** — "비싼 실행" 의 범위를 grid·fit
   으로 좁혀 놓았다. 계약 문구도 그 범위다.
5. **prospective 실행이 아직 0건** — lifecycle 은 hermetic 시험으로만 돌았다.
   `planned_coverage()` 가 `gate_backed_executions: 0` 을 그대로 보고한다.
6. **실물 provider adapter 없음 · power-loss ordering · principal 경계** —
   별도 acceptance 로 계속 열어 둔다.

## 증명 명령

```bash
cd degradation-degeneracy
python -m pytest tests/ -q                       # 1243 passed · 1 xfailed
./scripts/smoke_e2e.sh                           # clean 커밋에서
python3 docs/22p_gap/mutation_replay.py          # rc 0 (pytest-json-report 필요)
python3 ../wiki/tools/lint.py                    # 0 errors
python3 -c "from tools.preserve import planned_coverage; print(planned_coverage())"
```
