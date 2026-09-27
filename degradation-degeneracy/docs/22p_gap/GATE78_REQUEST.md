# 78차 게이트 리뷰 요청 — 77차 설계 정정 3건 (G77-N1 보존 범위 · G77-N2 primary 한 행 · G77-N3 구현 의존/사전 고정) + 제한 오프라인 구현 범위 (실행 GO 아님 · 코드 변경 없음)

> **상태: 확정 (2026-09-27).** 77차는 "단계 3 재심사" 방향을 수용했고, "단계 12 전체 완료 → 13 일괄 착수" 는 수용하지 않았다. 잔여는 설계 정정 세 건 (N1 P1 · N2 P1 · N3 P2). 리뷰어 지시대로 **이 회신은 N1 상태표 + N2 primary 한 행 + N3 의존/사전 고정 표 + 제한 오프라인 구현 범위만** 묶는다. 76차 종결(74차 1–6 + 75차 잔여)은 유지되며 다시 열지 않는다.
> 코드 변경 없음 (RUN_SCOPE diff 0). 새 계산·복원·class/투영·영수증 재생성 없음. **구현 자체는 사용자의 별도 범위 승인 뒤** — §4 가 그 승인 요청문이다.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| 코드 | `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` · `source_digest 1c67a748598baadb` (76·77차와 같다) |
| 정정 대상 | `GATE77_REQUEST.md` §1·§2·§3·§4 (취소선 반영) · 원장 §107 한 문장 (취소선) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §108 (77차 접수 + 이 정정) |
| 77차 패키지 원본 | `docs/22p_gap/gate77_review/` (zip `5753ddfc…`, MANIFEST 34/34) |

## §1 G77-N1 — 단계 12 를 두 경로로 나눈다 (로컬 실물 확인 vs 운영 보존 profile 잔여)

**우리가 틀린 것:** grid_fit_v5 의 로컬 완주(계획 → 실행 → `artifacts/grid_fit_v5` → `tools.archive_bundle.restore` 복원 → validator·재채점 영수증 → 원장 결속)를 "실물 provider 어댑터" 의 증거로 제안했다. 그 경로와 §13.2 의 backend 소유 CAS → CAS 만으로 복원 → durable registration → 운영 provider retention/version 검증은 다르다. 근거 (리뷰어 좌표, 우리가 다시 읽음): receipt `core.bundle.uri = artifacts/grid_fit_v5` · `tools/preserve.py` 머리말 "실제 운영 backend 의 canary receipt 는 첫 pilot 전 **별도 gate**" · `CasBackend.ENFORCEMENT = ENFORCEMENT_ADVISORY` (ClassVar, `probe_enforcement()` 도 advisory) · docs-lint `_PRESERVE_INDEX`·`_PRESERVE_BACKEND` 자리 "아직 없다" · `test_a_registered_leg_binds_its_generation_to_the_receipt` 가 `registered == {}` 를 기대.

### §1.1 단계 12 상태 (정정)

| 하위 범위 | 상태 | 실물 근거 | 남은 것 |
|---|---|---|---|
| 12-L **로컬/협조적 환경의 실행·보관·복원·검증 경로** | **실물 확인** | grid_fit_v5: planned → running → executed (lifecycle) · `scripts/archive_results.sh` (엄격 index · 병합 · 동명 identity · 최종화 실패 전파) · `make_receipt.py` empty-root 복원 + 33/34 검사 + 재채점 · `attach_bundle_evidence` typed 소비 · 원장 `out` 결속 · 원본 history 보존 (70~76차) | — (76차 종결 범위) |
| 12-P **운영 보존 profile** (backend 소유 CAS · retention/object-lock 강제 · durable registration · provider canary) | **부분** | `file+cas://` backend 의 트랜잭션 의미는 fault-injection 회귀로 검증 (46~63차, 25차 Q1 답) — 강제 수준은 advisory | (i) 배포 profile·backend URI/권한 (ii) 회수·retention canary 의 합격 기준 (iii) `preserve_backend.yaml`·`preserve_index` 배선 (iv) registered receipt 세대 결속. **첫 pilot 전 별도 gate** |

### §1.2 묶음 8·9 (정정)

| # | 묶음 | 상태 | 로컬 하위 범위 (실물) | provider/registration 잔여 |
|---|---|---|---|---|
| 8 | immutable bundle index · receipt schema | **부분 — 로컬 하위 범위 수용** | 실물 묶음 · 엄격 index · typed receipt 소비 · history | 비-git backend URI · 외부 store 회수 · 보관 profile · 영수증 서명 없음(같은 principal) |
| 9 | 트랜잭션 보존 gate | **부분 — 기존 lifecycle 하위 범위 수용** | 실물 실행/원장 경로 · 격리 회귀 (46~63·70 E6) · 실패/재개 정책 | provider transaction 등록 · 운영 canary · `registered != {}` 첫 다리 |

### §1.3 보존 profile 선택 — 우리 선택은 **1 (기존 retention 계약 유지)**

| 선택지 | 뜻 | 우리 판단 |
|---|---|---|
| 1 | §13.2 retention 계약을 유지하고, 배포 profile · backend URI/권한 · 회수·retention canary 합격 기준을 **첫 pilot 전 별도 gate** 로 둔다 | **채택.** **사용자 승인 2026-09-27 (선택 1 유지).** 계약 변경이 없고 사용자 승인 없이도 경계를 정확히 남길 수 있다. 지금 클라우드 구축·canary 실행은 하지 않는다 |
| 2 | 협조적 로컬 보존으로 범위를 줄인다 | 사용자가 그 한계와 계약 변경을 명시 승인해야 한다 (§4 질문에 선택지로 둔다). 채택하더라도 기존 실물 결과를 WORM/object-lock 증거라고 재명명하지 않는다 |

E1(projection producer 결속)·E2(launcher attestation)·E4(독립 replay) 라벨은 12-P 의 증거를 대신하지 않는다 — 별개 축으로 유지.

## §2 G77-N2 — primary 한 행 (계약 §7 그대로 · secondary 분리)

**우리가 틀린 것:** `equal_start_count_base_retained` 를 primary arm 으로, "transition table 을 primary 로 확정" 을 사전 등록으로 제안했다. §7 의 primary 는 **grid · no-warm · 같은 base·bank·총 후보 수** 의 33p–34p paired contrast 이고 scalar 는 Δ 하나, 전이표 네 칸은 그 분해다. base-retained warm arm 은 §7.2 secondary 다. claim ID 가 `CLAIM_STATUS.yaml` 에 있다는 것은 arm·분모·scalar 의 사전 등록이 아니다.

### §2.1 primary (한 행 — 여기 적힌 것이 사전 등록 초안이다; 리뷰가 고치면 그대로)

| 축 | 값 |
|---|---|
| 연구 질문 | dQ/dV 정보(34p 항)가 복원을 개선하는가 — optimizer 초기화가 아니라 **정보** 의 효과 |
| reference | **grid** (`p_ini = null`; half-cell 은 objective-specific calibration 이 섞여 primary 가 아니다) |
| warm | `p_ini_warm_start: false` · `condition_warm_start: false` — **둘 다 false** |
| 후보 배열 (두 objective 동일) | `[base_init] + bank[:B-1]` — mode 라벨(`legacy_slot_replace` 의 no-warm arm = `equal_start_count_base_retained` 의 no-warm arm) 과 무관하게 이 배열이다. `planned_counts = {base: 1, warm: 0, random: B-1}` · `realized_counts` 를 실현값으로 따로 적는다 |
| 총 시작점 B | `total_start_budget_by_objective = {pocv_dvdq: B, pocv_dvdq_dqdv: B}` — **같은 B** (다르면 동일 후보 수 primary 가 아니다). 값은 §3 plateau gate 뒤 채택 (미정), ladder 는 §3 |
| bank | 행 단위 unit-cube bank, `bank_version`, `condition_bank_sha256` — 두 objective 가 **같은 bank prefix** 를 쓴다 (§4.4 의 중첩은 random bank 에만) |
| pairing key | `pair_group_id = H(pairing_design_sha256, canonical(lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type), parameter_order_sha256)` (§4.2) · `pairing_design_label: p22_grid_primary` · treatment·noise·noise_seed·objective 는 제외 · leg manifest 에 `cond_id → pair_group_id` mapping digest |
| exact bounds | `exact_bounds_sha256` (실제 ordered `lb/ub` 의 digest, preset 이름 아님) — 두 objective 동일 |
| 단위 | condition = 한 `pair_group_id` 의 (33p fit, 34p fit) 쌍 |
| pass / fail | 기존 정의 그대로: raw degeneracy flag `|추정 − truth| > tol` (`src/scoring.py` 의 현행 tol·mode; primary 에서 값을 바꾸지 않는다) |
| 분모 n | 두 objective 모두 **유한 J · converged** 인 condition 수 (complete-pair set). `n_conditions_planned` · `n_missing` (어느 한쪽이라도 solver 실패·비유한·미수렴) 을 **같이** 보고한다 |
| 실패/누락 처리 | (a) primary Δ 는 complete-pair set 에서 (b) 누락을 유리하게 버리지 않도록 **사전 등록 민감도**: 누락된 쪽을 fail 로 세는 Δ_worst 를 반드시 병기 (c) `n_missing / n_conditions_planned > 5%` 이면 primary 를 보고하지 않고 solver 건전성 gate (§6.2) 실패로 돌린다 — 이 5% 는 사전 고정값이며 결과를 보고 바꾸지 않는다 |
| primary scalar | `Δ = (pass→fail − fail→pass) / n` (33p → 34p 방향, paired raw-degeneracy risk difference) |
| 필수 분해 | 전이표 네 칸 `(pass,pass) (pass,fail) (fail,pass) (fail,fail)` — 같은 estimand 의 분해, 두 번째 endpoint 아님. 다중성 처리 없음 |
| 통계 | 결정론적 격자의 기술통계. p-value·모집단 확률로 옮기지 않는다 |
| 설계 prior | §7.1 의 recorded 값 (`436/55/1476`, Δ=0.2581) 은 prior 이지 새 primary 결과가 아니다 — threshold·endpoint 선택에 쓰지 않는다 |
| claim | `P22_STAGE3_PRIMARY` (v6). 이 행이 그 claim 의 arm·분모·scalar 정의다 — 리뷰 수용 뒤 `CLAIM_STATUS.yaml` 항목의 `무엇` 에 이 행을 참조로 적는다 (v5 승격 금지 그대로) |

### §2.2 secondary (계획에 넣되 실제 계산 여부는 §3-6 leg·비용표에서)

| arm | 후보 배열 (warm arm) | 무엇을 재나 |
|---|---|---|
| `equal_start_count_base_retained` | `[base, warm] + bank[:B-2]` | warm 을 넣는 대신 random 하나를 빼는 ablation (§7.2) |
| `legacy_slot_replace` | `[warm] + bank[:B-1]` | 21차 실험 재현 — 초기화 민감도 ablation |
| `union` | — | **이번 계획에서 제외** (`B` vs `B+1`; 운영 cascade 성능은 다른 질문) |

secondary 는 primary 와 **섞지 않는다**. 어느 arm 이 유리한지 보고 primary 를 바꾸지 않는다.

## §3 G77-N3 — 구현 의존 관계와 "사전 고정 / 측정 뒤 결정" 표

**우리가 틀린 것:** "pilot 전에 숫자를 적지 않는다" 를 예산 전체에 걸었고, §9.4 다섯 필드를 "작고 독립" 이라고 했다. 미정인 것은 **최종 채택 B** 뿐이다. `candidate_id`·`bank_index` 는 §4 의 design → pair → bank → candidate 결속과 warm-provider payload 에 의존한다 (`src/fitting.py` restart serializer 는 지금 `p/J/i/source/warm` 만 남기고, fit 행의 `converged/n_eval` 은 restart 별 값이 아니다).

### §3.1 사전 고정 vs 측정 뒤 결정

| 항목 | 사전 고정 (pilot 전, 이 문서/계약에 적는다) | 측정 뒤 결정 |
|---|---|---|
| 탐색 ladder | `[5, 10, 20, 40]` — **제안값** (리뷰 수용 여부 §5-3) | — |
| 최대 B | 40. ladder 끝까지 §6.2 gate 를 못 지나면 **미채택** (예산을 더 올리지 않고 결과를 "plateau 미달" 로 보고) | — |
| 중단 규칙 | 연속 두 doubling 이 §6.2 넷(단조성 · material ΔJ · solver 건전성 · sentinel 안정성)을 통과하면 그 N 채택 | 채택 B |
| numerical floor | **별도 한정 승인 측정 단계** — objective 별로 같은 입력 반복 / max-bank prefix 재평가로 J 재현 산포를 잰다. 임의 tolerance 숫자를 발명하지 않는다 | `abs_tol`·`rel_tol` (objective 별, 33p ≠ 34p) 을 floor 위에서 사전 등록 → 그 뒤 budget-adoption 판정 |
| `mono_tol` | max-N 1회 + prefix minima offline 계산이 기본 (nested 비증가 구조 보장) — 별도 N/2N 실행이면 `mono_tol` 필요 | 값은 floor 측정과 같은 단계에서 |
| material 규칙 | stratum n<100 → 0건 · n≥100 → `count*100 <= n` (§6.2) | — |
| provider 동결 | primary 는 provider 없음(no-warm, 명시적 null/no-provider 분기). secondary warm arm 은 provider artifact·solution map sha 를 먼저 봉인 | — |
| sentinel panel | 5 archetype × reference 2 × noise 3 (clean + 독립 seed 2) × objective 2 = 60 은 **최소 비교 구조**. 파일 `sentinel_panel.yaml` 에 exact cond id/물리좌표 · seed · reference/recipe sha · treatment/curves sha · exact bounds sha · stratum · empirical hard 의 선택 script sha + **holdout 규칙** 을 고정할 의무 — 아직 없는 SHA 를 계획값으로 가장하지 않는다 | empirical hard (archetype 5) 의 조건 — recorded-only 투영에서 결정론적 rule 로, holdout 분리 |
| 자원 상한 | core-time 상한 (leg·비용표에 적는다; `833 s × 28` 은 점유 core-time 근사이지 CPU 사용량 측정이 아니다) | 실제 견적 (환경·nproc) |

### §3.2 구현 의존 순서 (리뷰어 §2 N3 표를 그대로 받는다)

| 단계 | 무엇 | 의존 | RUN_SCOPE |
|---|---|---|---|
| 1 | N1 상태 / N2 estimand 정정 · v6 writer ↔ historical reader 의 **버전 경계** 고정 (§2.1 표: v6 writer 는 새 필수축 없으면 실패 · v5 는 당시 schema 로만 읽기 · 추론/승격 금지). 기존 기록 필드 소급 삭제 없음 | — | 문서 (이 요청) + 계약 |
| 2 | **독립 가능한 로깅·오류 처리 한정 구현**: restart 행에 `converged` · `termination_status` · restart 별 `n_eval`; `validate_provenance` 의 parquet 읽기 실패를 `fail` 항목으로 구조화. **candidate/bank 연결은 여기서 완료로 세지 않는다** | 1 | `src/fitting.py` · `src/io.py` (+ 회귀) |
| 3 | 묶음 1·2 의 planned/realized schema · ID preimage (`pair_group_id`·`bank_id`·`candidate_id`) · 묶음 3 provider DAG/solution map. primary no-warm 경로는 명시적 null/no-provider 분기. 후보 ID/인덱스·수량을 serializer/validator 까지 잇는다 (`candidate_id`·`bank_index` 는 여기) | 2 | `src/` · `tools/design_wire.py` |
| 4 | 묶음 6: 신규 writer 의 구 필드(`pairing_design_id`·`inference_status`) 제거 + consumer 별 per-key linkage **음성** 변이. v5/v6_prep read-only dispatch·과거 봉인 유지 | 3 | `src/` · `tools/` · `mutation_replay.py` |
| 5 | 묶음 4·5: sentinel 선택 규칙 · stratum · ladder/max B · 미채택 규칙 · `mono_tol`/material tolerance 역할 고정 뒤 연결. empirical hard 는 선택 자료 ≠ 확인 자료 | 4 (+ floor 측정 승인) | `src/scoring.py` · `sentinel_panel.yaml` |
| 6 | 고유 leg/provider/floor/smoke/holdout 목록 + wall/core-time 비용표 → 오프라인 구현 독립 검토 → 필요한 보존 profile 확인 (12-P) → **별도 pilot 승인** | 5 | 문서 |

## §4 제한 오프라인 구현 범위 — 사용자 승인 요청문 (리뷰가 이 회신을 받은 뒤)

> **사용자 승인 (2026-09-27, `284d2153` 뒤):** 아래 범위(단계 1+2, 라운드 끝 leg 별 영수증 1회 포함)를 승인 — **착수는 78차 회신 뒤.** pilot·본 계산·provider canary·floor 측정은 승인에 포함되지 않는다.

| 항목 | 이번 라운드에 **한다** | 이번 라운드에 **안 한다** |
|---|---|---|
| 범위 | §3.2 단계 1 (문서·계약 정정 반영, 버전 경계) + 단계 2 (restart 행 `converged`·`termination_status`·`n_eval` · parquet 읽기 실패 구조화) | 단계 3~6 · provider canary · floor 측정 · pilot · 본 계산 · 복원 · class/투영 변경 |
| RUN_SCOPE | 움직인다 (`src/fitting.py` · `src/io.py`) → 영수증은 **최종 코드가 고정된 라운드 끝에 대상 leg 별 1회** 재생성 (restore·validate·재채점 실행이므로 **이 승인 범위에 명시 포함**; 실패하면 새 검증 완료로 붙이지 않는다; 원본 history 보존; 그 뒤 RUN_SCOPE 가 다시 움직이면 그 영수증은 새 identity 의 근거가 아니다) | 중간 digest 의 옛 영수증을 새 검증 PASS 로 쓰는 것 |
| 증거 | RED 먼저 · 변이 · 전체 회귀 + strict smoke (clean 커밋) · v5 historical reader 가 옛 기록을 그대로 읽는 회귀 | 새 과학 수치 |
| 산출 | GATE79 요청문 (코드 라운드 판정) | — |

## §5 리뷰어에게 묻는 것

1. §1 의 12-L/12-P 분리와 묶음 8·9 의 하위 범위 기술을 받는가. 보존 profile 선택 1(계약 유지 · canary 는 pilot 전 별도 gate)이 맞는가.
2. §2.1 primary 한 행 — 특히 분모(complete-pair) · 누락 처리(Δ_worst 병기 · 5% 상한) · pairing key 가 §7·§4.2 와 어긋나는 곳이 있는가.
3. §3.1 의 ladder `[5,10,20,40]`·최대 40·미채택 규칙을 제안값으로 받는가. floor 측정을 별도 한정 승인 단계로 두는 것이 맞는가.
4. §3.2 의존 순서와 §4 의 제한 구현 범위(단계 1+2)가 "제한 오프라인 구현" 의 뜻과 같은가. 다르면 어디를 줄이거나 늘려야 하는가.
5. 이 회신이 새 실행 GO 를 요청하지 않고 grid_fit_v5 는 진단 전용 그대로임을 확인한다.

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **77차 설계 정정 3건의 정정본과 제한 오프라인 구현 범위를 제출한다. 실행 GO 는 묻지 않는다. 구현 착수는 사용자 승인 뒤다.**
