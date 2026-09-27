# 75차 게이트 리뷰 요청 — 74차 회신 항목 1~6 에 대한 답 (R1·R2 기록 · G74-3 진단 전용 분류 계약 · G74-1 고정 캐시 진입 · G74-4 index 병합 · validator 식별 분리)

> **상태: 확정 (2026-09-26).** 74차 회신(완주·보존 증거 제한 수용 · 편입/종결 보류)의 여섯 항목에 답한다. 사용자가 항목 3~6 전부를 범위로 승인했다 (원장 §102). **새 실행 GO 를 요청하지 않는다.** 투영 게시·class 변경·새 계산은 없다.
> RUN_SCOPE 가 한 번 움직였다 (`tools/preserve.py` · `scripts/archive_results.sh`). 판정 대상 코드는 아래 표가 정본이다.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| **판정 대상 코드** | **`ebfb853d1b3dff0678f5f67985003498a3476982`** — RUN_SCOPE 마지막 변경 (74차 대응) · `source_digest` **`27390883eb132941`** (74차 대상 `7a794556` · `c2ef1a811e70bb4c` → 이 커밋). 그 뒤 커밋은 영수증·원장·시험·문서뿐 (RUN_SCOPE diff 0) |
| 영수증 재생성 커밋 | `8765068a` (clean 트리 `ebfb853d1b3dff0678f5f67985003498a3476982` 에서 `make_receipt.py paired_fixed5_v4 grid_fit_v5`) |
| 리뷰 원자료 | 74차 패키지 `docs/22p_gap/gate74_review/` (zip `eb03012c…`, MANIFEST 102/102, `-text !eol` 규칙 먼저) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §102(접수·R1·R2) · §103(대응) · 작업 상태 `docs/GATE70_WORKING_STATE.md` |
| 새 시험 | `tests/test_gate74_defensive.py` **41 node** (패치 전 36 failed / 4 passed — fixture 감사 §103) · 변이 6 신규 (`mutation_replay.py -k g74`) |

## §0 74차 여섯 항목에 대한 답

| # | 항목 | 답 | 근거 |
|---|---|---|---|
| 1 | R1 추가 resume 승인 출처 | **사전 재승인 없음 — 편차 인정.** 세션 대화 기록: 09:19:56Z 에이전트가 캐시 이동 + 같은 attempt 재호출을 제안하며 "compute 이전 거부는 1회에 안 센다" 해석을 적었고, 09:21:55Z 사용자가 별도 승인 문장 없이 실행. 해석 철회. 뒤 계획 교체는 소급 승인이 아니다 | §102 R1 · §99 표 1-r·2 행 취소선 |
| 2 | R2 문구 정정 | 5건 취소선 정정 (완료 feasible 조건 0 · VM 부팅 관측 vs 원인 가설 · null "항상 거부" → 캐시를 둔 채 재시작 시 거부 · attach → `finalize_leg()` · loky 경고 원인 미확정) | §102 R2 표 · §99·§100·§101 · `GATE74_REQUEST.md` |
| 3 | 진단 전용 분류 계약 + 여섯 회귀 | **(c)+(b) 구현.** `claim_scope ∈ {active_claims, no_active_claim}` 다리마다 명시(누락·모름·모순 거부) · cohort `executed_legs`(실행 명부) ≠ `legs`(투영 membership) · `no_active_claim` 은 `claim_roles` 금지·투영 명부 금지·full_bundle 증거 계약 그대로 · 생산(plan → `finalize_leg` 라우팅 → 실행 기록 stamp)과 소비(`planned_index` · docs-lint `_scope_problems`·`_no_active_claim_evidence_problems`)가 같은 분류 · `row_projection.py` 불변(봉인 불변 — §103 사유) | §1 표 · `g74_3_01~06d` (15 node) |
| 4 | G74-1 정책 + 경계 회귀 | **(ii) 고정 캐시 SHA 계획만 진입.** `assert_planned_leg → _assert_prospective_plan_is_startable`: `run_spec.grid.discharged_cache_sha256` 소문자 hex64 필수(축 부재도 거부) — precheck·발급·finalize 가 전부 지난다. `plan_leg.py` 가 같은 규칙을 먼저 말한다. live 축은 그대로 claim 과 **비교** (`g74_1_06`). `cache: false` 모드는 계획 불가(명시). | `g74_1_01~07` (10 node) · 변이 `cache-sha-must-be-fixed-hex64-g74` 8/8 |
| 5 | G74-4 index 보존 회귀 · 복원 바이트 유지 | 기존 index 진입 시 파싱(불명확 → 중지) · 승격 전 동명 다른 identity 거부(`ARCHIVE_REPLACE=1` 명시) · 병합 · 임시 파일 뒤 `os.replace`. `e84d670d` 의 v4 네 블록 복원 바이트는 그대로 (이 라운드에 index 를 다시 쓰지 않았다) | `g74_4_01~05` (8 node) · 변이 2 |
| 6 | 보존 vs 새 validator 식별 | 두 영수증 원본을 `docs/22p_gap/receipts/history/<leg>.validate.c2ef1a811e70bb4c.yaml` 로 보존 → clean `ebfb853d1b3dff0678f5f67985003498a3476982` 에서 재생성. 원장은 `verification_receipt_core_sha256`·`validator_identity.source_digest` 만 갱신, `leg_source_digest`(producer) 불변. 재생성 전후 차이 = validator 식별 · core sha · stamp(시각·commit·platform·python) **뿐** — 33/34 검사·산출 2건의 file/semantic sha 전부 동일 | §103 ⑥ · `g70_e3_17` · `g71_e3r_12` · `g72_a07` · `test_full_bundle_claims_are_backed_by_a_real_bundle` |

## §1 G74-3 계약 (구현 좌표)

| 계약 | 생산 | 소비 |
|---|---|---|
| 분류 enum · roster 대응 | `tools/preserve.py::CLAIM_SCOPE` · `CLAIM_SCOPE_ROSTER` | docs-lint `_CLAIM_SCOPES` |
| 계획이 분류를 말한다 (선택 키, 옛 계획 재작성 없음) | `PLANNED_KEYS_PROSPECTIVE_OPTIONAL` · `planned_index` schema | `plan_leg.py --claim-scope` |
| 시작 조건 (scope + 고정 캐시) | `_assert_prospective_plan_is_startable` | — |
| 끝난 다리의 roster = 분류 · 계획/기록 모순·누락 거부 · 반대 방향(`executed_legs` 는 끝난 prospective·no_active_claim 만) · 명부 교집합 거부 | `planned_index` · `_executed_scope` · `_record_claim_scopes` | `_scope_problems` |
| finalize 라우팅 + stamp | `finalize_leg` | — |
| `no_active_claim` 증거 계약 (full_bundle · current_validated · out · 영수증 typed 재읽기 + core sha · validator 식별 = 영수증) | 72차 `_assert_ledger_run_bound` 그대로 | `_no_active_claim_evidence_problems` |
| 활성 주장 참조 거부 | — | `_claim_role_problems` (분류 문제 먼저, 그 다리의 role 은 세지 않음) |

원장 (사람): g18 `legs: [paired_fixed5_v4]` · `executed_legs: [grid_fit_v5]` · `grid_fit_v5` `claim_scope: no_active_claim` + `근거` + `evidence.regeneration_capability: available_raw_present`(사실 기록) · 8 투영 다리 `claim_scope: active_claims`.

## §2 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                ebfb853d1b3dff0678f5f67985003498a3476982
source_digest                                 27390883eb132941
전체 pytest (tests/)                          **0 failed · 1922 passed · 2 xfailed (43:57, rc 0)** — 첫 전체 회귀(`8765068a`)는 3 failed 였고 전부 이 라운드의 시험 fixture/증인 결함 (§103 실측, `7ec4e234` 에서 정정)   (시작 HEAD = 끝 HEAD = 7ec4e234 · 미추적 0)
strict smoke (scripts/smoke_e2e.sh)           rc 0 (`✅ pipeline smoke 통과`)
docs-lint 적색                                 74차 요청 시점 20 → **0**
mutation_replay --check-preimages · -k g74     전 지점 1회 · `mutation_replay.py --check-preimages` 전 지점 1회 · `-k g74` **6/6 물었다** (`cache-sha-must-be-fixed-hex64-g74` 8 node · `plan-scope-required-at-entry-g74` 1 · `finalize-routes-by-scope-g74` 1 · `executed-legs-only-hold-no-active-claim-legs-g74` 1(04e) · `index-merge-keeps-other-entries-g74` 2 · `same-name-different-identity-is-refused-g74` 1). EXPECT 는 `--emit-expect` 관측값 그대로 (`8765068a`)
등록부                                        tracked 369 · 디스크 369 · 미추적 0
```

## §3 우리가 스스로 신고하는 것

- `row_projection.py` 를 고치지 않았다. 처음 고쳤을 때(`executed_legs` 를 authority 로 읽되 봉인 밖) `row_projection_py_sha256`·`compute_sha256` 이 움직여 활성 cohort g18 의 **투영 재생성**이 강제됐다 — 이 회신이 허가하지 않은 투영 게시라 되돌렸다. publisher 는 `executed_legs` 를 무시하고 봉인은 불변(`g74_3_06d`). 진단 다리가 투영 명부에 끼는 것은 `planned_index`·lint 가 막는다. **publisher 검사까지 요구하면 재생성과 함께 한다** (§5-2).
- 처음부터 통과한 새 시험 4개(§103 fixture 감사): 둘은 닫힌 schema 의 부산물(변이 `cache-sha…` 가 규칙을 지우면 빨개짐 — `g74_1_05` 포함), 하나는 강화한 뒤 RED, 하나는 기존 동작 보호.
- `executed-legs-only-…` 변이의 첫 selector(04c)는 교집합 검사가 먼저 잡아 fail [] 이었다 — 반대 방향만이 잡는 경계(계획에 없는 이름)로 `g74_3_04e` 를 추가하고 재조준했다.
- `paired_fixed5_v4` 의 `validation_status` 는 `historical_validated` 그대로, `grid_fit_v5` 는 `current_validated` 그대로 — 재생성한 영수증의 산출 digest 가 전부 동일하므로 값을 바꾸지 않았다. 다만 "validator 식별 ≠ producer 식별" 상태가 `grid_fit_v5` 에도 생겼다 (c2ef… produced, 27390883eb132941 validated). 이 조합의 이름을 바꿔야 하는지 §5-3 에 묻는다.
- WSL 고아 레코드 `f3f509…` 는 그대로 (G74-2, 74차 수용).

## §4 하지 않은 것

새 grid/fit 실행 없음 · 투영 게시 없음 · class 변경 없음 · 옛 계획 항목 재작성 없음 · `results/` 복원 없음(영수증 재생성의 empty-root 복원은 임시 디렉터리).

## §5 리뷰어에게 묻는 것

1. 항목 1~6 각각의 종결 수용 (예/아니오, 아니오면 남은 조건 한 줄).
2. `row_projection.py` 불변 결정을 받는가 — publisher 가 `executed_legs` 를 검사하도록 요구하면 g18 투영 재생성(`paired_fixed5_v4` 복원 → `row_projection.py … --cohort g18_2026_09_15`)을 같이 승인해야 한다.
3. `grid_fit_v5` 의 `current_validated` — producer c2ef… · validator 27390883eb132941 조합을 그대로 `current_validated` 로 두는가, 별도 이름이 필요한가.
4. 75차 이후 다음 실행(있다면)의 조건: G74-1 의 새 gate 아래 `plan_leg.py --claim-scope` 로 계획 → 이번 계약이 실제 새 실행에서도 성립하는지 확인하는 한정 실행이 필요한가.

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **74차 항목 1~6 의 종결 판정을 요청한다. 새 실행 GO 는 요청하지 않는다.**
