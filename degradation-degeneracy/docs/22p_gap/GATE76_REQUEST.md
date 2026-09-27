# 76차 게이트 리뷰 요청 — 75차 잔여 G75-N1(P1) · N2 · N3 에 대한 답 (index 최종화 실패 전파 · 중복/merge 키 엄격 loader · 진단 소비자 out 결속)

> **상태: 종결 (2026-09-27, 76차 회신 — N1·N2·N3 수용 · 전체 종결 · 새 실행 GO 없음; 원장 §106).** ~~확정 (2026-09-27).~~ 75차 회신(부분 수용 · 종결 보류: 잔여 P1 1 · P2 2)의 세 항목에 답한다. 사용자가 N1·N2·N3 전부를 범위로 승인했다 (원장 §104 → §105). **새 실행 GO 를 요청하지 않는다.** 투영 게시·class 변경·복원·새 계산은 없다.
> RUN_SCOPE 가 두 번 움직였다 (`10be3a69` · `23c361ed`). 판정 대상 코드는 아래 표가 정본이다.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| **판정 대상 코드** | **`23c361edbfc92fefcfbf0639b5ac40f61f7ebec7`** — RUN_SCOPE 마지막 변경 (merge key 정책) · `source_digest` **`1c67a748598baadb`** (75차 대상 `ebfb853d` · `27390883eb132941` → `10be3a69` · `cd2408354486c148` → 이 커밋). 그 뒤 커밋은 영수증·원장·변이 EXPECT·문서뿐 (RUN_SCOPE diff 0 — 발송 전 실측) |
| 영수증 재생성 커밋 | `baf109b5` (clean 트리 `a3eb4cbe` 에서 `make_receipt.py paired_fixed5_v4 grid_fit_v5`); 중간 세대 `0f6b8a76` (clean `2df96f06`, validator `cd2408354486c148`) 도 원본을 `history/` 에 남겼다 |
| 리뷰 원자료 | 75차 패키지 `docs/22p_gap/gate75_review/` (zip `4a1ad8a2…`, MANIFEST 70/70, `-text !eol` 규칙 먼저) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §104(접수·문구 정정) · §105(대응) · 작업 상태 `docs/GATE70_WORKING_STATE.md` |
| 새 시험 | `tests/test_gate75_defensive.py` **22 node** (첫 판 ~~19 node~~ **18 node** (76차 정정, §106) 패치 전 11 failed / 7 passed — 사유 §105) · 변이 4 신규 (`mutation_replay.py -k g75`) |

## §0 75차 세 항목에 대한 답

| # | 항목 | 답 | 근거 |
|---|---|---|---|
| N1 | index 최종화 실패가 archive rc 에 전파되지 않음 (S17 rc 17 → 부모 rc 0 · commit 안내; W01) | index 호출을 `if ! …; then index_ok=0` 로 감싼다 → **즉시 nonzero** (`n_bad·n_missing·index_ok` 세 축) · stderr 에 명시적 미완 + **이미 승격된 묶음 이름** (승격은 되돌리지 않고 숨기지 않는다) · "git add artifacts" 안내 차단 · 임시 파일 try/finally 삭제(기존 index 바이트 그대로). 자동 rollback 없음 | `g75_n1…[rc17/replace/write]` — 부모 rc≠0 · index SHA 불변 · `dest/res` 승격 유지 + stderr 표기 · 안내 부재 · tmp 부재. `n1_control` 정상 경로 rc 0 · 변이 `index-finalisation-failure-fails-the-archive-g75` |
| N2 | `safe_load` 가 중복 mapping 키를 접는다 (I02 top-level `runs` · I03 run 이름 · I04 identity 키) | 신규 `tools/index_yaml.py::load_index_strict` — 중복 키 `DuplicateKeyError` · `<<` merge key `MergeKeyError` · 형식(`runs:` mapping / 이름 str / entry mapping) 을 **한 함수**에서. archive 의 세 reader(진입 · 동명 비교 · 병합)가 전부 이 함수 — 느슨한 `safe_load` 로 index 를 읽는 자리 없음(시험이 소스를 센다). 첫 승격 전 rc 1 · index 바이트 불변 · 묶음 미승격 | `g75_n2_a_duplicate…[I02/I03/I04/merge]` · `g75_n2_the_strict_loader_is_one_function…` · 변이 `duplicate-index-keys-are-refused-g75` · `merge-keys-are-refused-in-the-index-g75` |
| N2-merge | merge key 정책 명시 | **허용하지 않는다** — flatten 하면 merge 키와 명시 키가 겹칠 때 정본 불명확이 다시 생긴다. index 는 `safe_dump` 로 기계가 쓰므로 정상 경로에 merge 는 없다; 있으면 사람이 본다 | `_StrictLoader` docstring · `[merge key overriding an identity value]` |
| N3 | 진단 소비자가 `out` 의 존재만 봄 (D01 `results/OTHER_RUN` 통과) | `_no_active_claim_evidence_problems` 가 생산자와 **같은 함수** `_repo_relative_or_refuse → _assert_receipt_bound_to_bundle → _assert_ledger_run_bound` 로 영수증 → 묶음 → 원장 실행 자리를 대조 (재구현 아님). producer 가 받는 것(끝 `/`)은 소비자도 받고, 거부하는 것은 같이 거부. 소급 수정 없음 · attach 재설계 없음 | `g75_n3_00`(양성) · `n3_01` ×5 · `n3_01b` · `n3_02` ×5 · `n3_03`(소스가 두 함수를 부른다) · 변이 `diagnostic-consumer-binds-out-to-the-receipt-run-g75` |
| 문구 | §104 정정 4건 | archive 병합 주석 "바이트 그대로" → "파싱된 값" · 시험 파일 머리말 "같은 검사" → "같은 정책" · 소비자 목록에서 `row_projection` 제외 · `4_01` docstring. `70b01fdb` 메시지가 포함한다고 적은 시험 파일 편집은 anchor 불일치로 미적용이었고 `0866a77d` 가 실제 편집 (정직 기록) | §105 |

## §1 구현 좌표

| 계약 | 생산 | 소비 / 시험 |
|---|---|---|
| index 최종화 실패 = archive 실패 | `scripts/archive_results.sh` (`index_ok` · footer 분기 · 최종 rc) | `g75_n1` (PYTHON wrapper 로 index heredoc 에만 결함 주입: rc 17 / `os.replace` OSError / tmp `write_text` OSError) |
| index 읽기 한 함수 | `tools/index_yaml.py::load_index_strict` (RUN_SCOPE) | `scripts/archive_results.sh` PYIDX · PYSAME · PYEOF 세 자리 · `g75_n2_the_strict_loader…` (소스에 `load_index_strict(` ≥3 · 느슨한 패턴 0) |
| `no_active_claim` 의 `out` 결속 | `tools/preserve.py::_assert_receipt_bound_to_bundle` · `_assert_ledger_run_bound` (72차 그대로, 변경 없음) | `tests/test_docs_lint.py::_no_active_claim_evidence_problems` |

## §2 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                23c361edbfc92fefcfbf0639b5ac40f61f7ebec7
source_digest                                 1c67a748598baadb
전체 pytest (tests/)                          0 failed · 1944 passed · 2 xfailed (41:49)   (시작 HEAD = 끝 HEAD = 5b10a79f · 미추적 0; 직전 4d8dfc52 는 1 failed — §3)
strict smoke (scripts/smoke_e2e.sh)           rc 0 (같은 트리 5b10a79f)
docs-lint                                     전체 회귀 안에 포함 — 적색 0 (5b10a79f) · 요청문 커밋 뒤 단독 실행값은 발송문에
mutation_replay --check-preimages · -k g75     전 지점 1회 · 4/4 물었다 (3 · 4 · 1 · 5 node) · EXPECT 관측값 (4d8dfc52)
등록부                                        tracked 369 · 디스크 369 · 미추적 0
```

## §3 우리가 스스로 신고하는 것

- N1 의 첫 RED 는 **거짓 RED** 였다: PYTHON wrapper 가 heredoc 스크립트를 파일로 실행해 `sys.path[0]` 이 cwd 가 아니게 되자 **검증 heredoc** 이 `ModuleNotFoundError` 로 죽어 rc 1 이 났다. wrapper 를 stdin 재전달(`python -` 유지)로 고친 뒤 진짜 RED(rc 0 · commit 안내)를 봤다. §105 에 적었다.
- 첫 영수증 재생성 시도는 history 두 파일이 미추적인 트리에서 돌아 `validator_tree_dirty=true` 가 찍혔다 → 버리고(git checkout) 보존 커밋 뒤 clean 에서 다시 만들었다. 현행 `grid_fit_v5` 영수증의 `validator_tree_dirty: true` 는 같은 호출의 앞 영수증 갱신 때문이며 74차 영수증과 같은 값이다 (stamp, core 밖).
- `merge-keys-are-refused-in-the-index-g75` 변이의 fail set 은 merge 사례 1 node 다 (다른 세 중복 사례는 `DuplicateKeyError` 가 잡는다).
- RUN_SCOPE 가 한 라운드에 두 번 움직였다 (N1·N2 구현 뒤 merge key 정책을 별도 커밋으로) — 그래서 영수증 세대가 셋이다 (`27390883…` · `cd2408…` · 현행 `1c67a748…`); ~~전부 `history/` 에 있다~~ **이전 두 세대는 `history/`, 현행은 `receipts/<leg>.validate.yaml` (76차 정정, §106)**.
- 처음부터 통과한 새 시험 7개(첫 판)의 사유는 §105 — 대조군 2 · 74차판이 이미 거부하던 축 5.
- 첫 전체 회귀(`4d8dfc52`)는 **1 failed** — 75차 패키지 보존 사본(`gate75_review/codex/reference/docs/22p_gap/STAGE3_CONTRACT.md`)이 claim 관할로 잡힌 docs-lint 적색으로, 패키지 커밋 `cd272a89` 부터 있었고 이번 코드와 무관하다. `_CLAIM_SCOPE_EXCLUDE` 에 `gateNN_review/` 를 더해(`5b10a79f`, RUN_SCOPE 밖) 다시 돌린 결과가 §2 다.

## §4 하지 않은 것

새 grid/fit 실행 없음 · 투영 게시 없음 · class 변경 없음 · `row_projection.py` 불변 · `attach_bundle_evidence` 재설계 없음 · 옛 index 자동 rollback 없음 · `results/` 복원 없음 (영수증 재생성의 empty-root 복원은 임시 디렉터리).

## §5 리뷰어에게 묻는 것

1. N1 · N2(merge 정책 포함) · N3 각각의 종결 수용 (예/아니오, 아니오면 남은 조건 한 줄).
2. 74차 항목 1~6 + 75차 잔여가 전부 닫히면 **전체 종결** 인가 — 남은 조건이 있으면 한 줄.
3. 영수증 세대가 셋인 상태(~~전부 history 보존~~ **history 3세대 + 현행 1세대 / 다리** — 76차 정정, §106)에서 원장이 현행 한 쌍만 가리키는 것이 맞는가.

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **75차 잔여 N1·N2·N3 의 종결 판정을 요청한다. 새 실행 GO 는 요청하지 않는다.**
