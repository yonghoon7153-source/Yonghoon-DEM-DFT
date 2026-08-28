# 46차 게이트 리뷰 요청 — 묶음 9 (cohort 게시 · 보존 · 실행 전 계획 gate)

```yaml
대상 커밋:   fe3d0ec2156b493b6345dae231d440e3585415bb
브랜치:      claude/14-gate-code-review-9qkx05
직전 판정:   45차 NO-GO — "pre-sink staging write 와 축소된 ledger authority"
전체 시험:   1203 passed · 1 xfailed
strict smoke: ✅ pipeline smoke 통과 (clean 커밋에서)
변이 재생:   scenario 44 · 실행 41 · 신고 3 · site 42 · rc 0
projection:  ad598fe77e75afec (행 바이트 45차와 동일)
receipt:     core_sha 74c51fd67bbfdb78
source_digest: bd8cbc653d8bbffb
wiki lint:   0 errors
```

45차의 12개 최소 반증 조건에 대응했다. 원장은
`docs/08_REVIEW_RESPONSE.md` §54, 계약 변경은 `docs/22p_gap/STAGE3_CONTRACT.md`
§13.3.2 · §13.3.3 · §13.4.

## 조건별 대응

| # | 45차 조건 | 무엇을 바꿨나 | 회귀 |
|---|---|---|---|
| 1 | caller stage 를 처음부터 no-follow exact read | `_promote_cohort_locked()` 의 첫 접촉이 `_staging_entries()` (`row_projection.py`) | `..._dangling_symlink_in_the_caller_stage_never_creates_an_outside_file` |
| 2 | caller stage 에 write·copy·rmtree 금지 | 병합은 메모리, 자재화는 `out/.merge.<uuid>.tmp` 에만. 성공해도 caller staging 을 지우지 않는다 | `..._caller_stage_is_untouched_when_the_final_guard_fails` · `..._caller_stage_survives_a_successful_publish` |
| 3 | 생성·멱등·독자가 같은 generation validator | `_generation_entries()` 하나 (커밋된 generation 16개 감사 — 전부 regular·nlink 1, 마이그레이션 불필요) | `..._generation_reader_refuses_an_aliased_generation_file` · `..._idempotent_branch_refuses_an_aliased_generation_file` |
| 4 | stage↔gdir alias 를 `(st_dev, st_ino)` 로 | `_assert_outside_generations()` — stage 와 **조상들**을 gen/·각 generation 과 inode 대조 | `..._stage_that_is_the_base_generation_by_inode_is_refused` · `..._current_generation_cannot_be_used_as_its_own_staging[self,nested]` |
| 5 | producer pin 의 불변 부분 + 사용 정책을 봉인에 | `_LEDGER_AUTHORITY += (pin, cross_leg_comparison)` · `_PIN_SEALED = (schema_version, analysis_spec_sha256)` | `..._producer_pin_is_part_of_the_publication_authority` · `..._pin_change_cannot_mix_producers_inside_one_cohort` · `..._mutable_provenance_digest_is_deliberately_not_sealed` |
| 6 | `status` exact enum · `dir` 정규·상대·격리 | `_LEDGER_STATUS` · `_CROSS_LEG_POLICY` · `_ledger_dir()` (production parser fail-closed) | `..._ledger_status_is_an_exact_enum[4]` · `..._ledger_parser_refuses_a_dir_that_is_not_contained[5]` |
| 7 | pointer 의 `cohort_id` echo · pointer 소실 | echo **필드를 제거** (비교 대신 표현 제거) · pointer 소실은 terminal fail-closed · `migrate_pointer.py` | `..._pointer_carries_no_cohort_id_echo` · `..._losing_the_pointer_of_a_cohort_that_has_generations_is_terminal` |
| 8 | `versions()` 후보 전수 검증 · `lock` 앞에서 | `_version_candidates()` 가 유일한 통로 (`preserve.py`) | `..._every_enumerated_version_candidate_must_be_a_nonempty_string` · `..._falsy_version_never_reaches_lock` |
| 9 | 변이 runner 격리·정확성·기대 집합·의미 증인 | sandbox 복사 · raw-byte 복원 · rc 정확 · collector 분리 · **기대 node 집합 정확 일치** · **node 별 증인** | `mutation_replay.py` (rc 0) |
| 10 | 시도별 token · B 의 lock 사유 · warm 간선 | marker 에 시도 token · stderr 의 `다른 게시가 진행 중이다` 확인 · `_WARM_CONSUMER_EDGES` 명시 대조 | `..._two_independent_publishers_lose_no_leg` · `..._warm_consumers_go_through_the_accessors` |
| 11 | planned leg index 를 실행 전 gate 로 · run.sh/smoke 배선 | `planned:` 닫힌 schema · `assert_planned_leg()` + `assert_planned_index_consistent()` · run.sh grid·fit · smoke 3검사 | `tests/test_preserve.py` 신규 8건 + smoke |
| 12 | 실물 adapter · power-loss · principal 경계 | **미착수 — 별도 acceptance 로 신고 유지** | — |

## 이번에 실제로 성립했던 반례 (public API 만으로)

```
stage/ = {a.projection.csv.gz, a.projection.yaml, a.restarts.csv.gz}
         + b.projection.yaml -> ../victim      (dangling symlink)
promote_cohort_generation(stage, out, "a", roster={"a","b"})
```

`Path.is_file()` 이 끊어진 link 를 걸러 exact-set 검사를 통과시키고, base 복사
(`shutil.copyfile(gdir/b.projection.yaml, stage/b.projection.yaml)`)가 목적지
symlink 를 따라가 **cohort 디렉터리 밖**에 `../victim` 을 만들었다.

## 변이 재생이 이번 라운드에 잡은 것

45차 runner 였다면 넷 다 "물었다" 로 셌을 것들이다.

| 잡힌 것 | 실제 원인 | 처리 |
|---|---|---|
| preimage 0회 (mutant 둘) | 코드 들여쓰기와 mutant 불일치 | preimage 수정 |
| `idempotent-shares-the-validator` 미관측 | alias 를 **현재 pointer 가 가리키는** generation 에 걸어 독자가 먼저 거부 | 시험 배치를 바꿔 분기를 격리 |
| `staging-not-inside-gen` 미관측 | namespace 판정이 **두 구현**으로 나뉘어 서로를 가림 | **하나로 합치고** 경로 사본 삭제 |
| 증인 불일치 셋 | mutant 당 증인 하나로는 parametrize 된 실패를 구별 못함 · 증인에 시각·임시 경로 | 증인을 **node → 부분문자열 map** 으로 · 안정 접두로 손질 |

## 신고하는 한계 (공격 대상)

1. **`os.replace` 직전~직후 창** — 전제로 배제. 탐지도 복구도 안 된다 (§13.3.1).
2. **실행 전 gate 의 면제는 산출 namespace 하나** — `results/_smoke/` 안으로만
   읽고 쓰는 실행은 gate 를 지나지 않는다. 같은 principal 이 비싼 실행을 그
   namespace 로 밀어 넣는 것은 막지 못한다 (다만 그 산출은 정본이 될 수 없다).
3. **`planned:` 8건은 소급 기록** — index 도입 시점에 이미 실행된 다리들이다.
   digest 는 `evidence.leg_source_digest` 를 그대로 옮겼고 gate 가 일치를
   강제하지만, 그때는 실행 전 gate 가 없었다.
4. **실물 provider 어댑터 없음** — 보존 회귀는 hermetic fake 로만 돈다. smoke
   통과는 실물 WORM 보관 승인이 아니다.
5. **same-process 적대적 Python** — `_Authority._ACTIVE` 는 우연한 우회를 막을
   뿐 보안 경계가 아니다.
6. **`_PIN_SEALED` 를 두 필드로 좁힌 판단** — `compute_sha256`·파일 digest 를
   봉인 밖에 둔 근거는 "active cohort 의 manifest 는 현행 트리와 같아야 한다"
   는 별도 회귀가 그 축을 강제한다는 것이다. 그 합성이 실제로 닫히는지가
   이번 라운드에서 가장 공격하기 좋은 지점이다.

## 증명 명령

```bash
cd degradation-degeneracy
python -m pytest tests/ -q                       # 1203 passed · 1 xfailed
./scripts/smoke_e2e.sh                           # clean 커밋에서
python3 docs/22p_gap/mutation_replay.py          # rc 0
python3 ../wiki/tools/lint.py                    # 0 errors
```
