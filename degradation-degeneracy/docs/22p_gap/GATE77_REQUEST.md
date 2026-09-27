# 77차 게이트 리뷰 요청 — 단계 3 계약 v4 **구현 전 재심사** (§11 단계 12 판정 · 단계 13 착수 승인 · 새 실행 GO 아님)

> **상태: 77차 회신 접수 (2026-09-27) — 방향 수용 · 설계 정정 3건(G77-N1 P1 · N2 P1 · N3 P2) → `GATE78_REQUEST.md` 가 정정본. 아래 취소선은 77차 정정.** ~~확정 (2026-09-27).~~ 76차가 74차 항목 1–6 + 75차 잔여를 전체 종결했다 (원장 §106). 다음 과학 단계는 `STAGE3_CONTRACT.md`(v4) 의 단계 3 — 사전 등록 primary estimand `P22_STAGE3_PRIMARY`(세대 v6, 아직 지지 다리 없음) — 이고, 계약 §11 은 "12 보존 체계 구축 → 13 RUN_SCOPE 변경·pilot" 순서에 **"여기까지 문서·회귀 재심사 ← 지금 여기"** 로 멈춰 있다. 이 요청은 그 재심사다. **묻는 것은 설계·상태 판정이지 실행 GO 가 아니다** — §9.3 대로 고유 leg 목록과 비용 재산정 전에는 실행 승인을 요청하지 않는다.
> 사용자 결정 (2026-09-27): "가장 권고하는 것으로" — 권고는 이 재심사다. grid_fine 격자를 같은 코드로 `active_claims` 로 다시 도는 것은 숫자가 같아 새 주장을 지지하지 못하므로 권고하지 않았다 (E9-0 의 목적은 grid_fit_v5 가 이미 완주했다).

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| 코드 (RUN_SCOPE 마지막 변경) | `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` · `source_digest 1c67a748598baadb` — 76차 판정 대상 그대로. 이 요청은 코드를 바꾸지 않는다 (RUN_SCOPE diff 0) |
| 심사 대상 문서 | `docs/22p_gap/STAGE3_CONTRACT.md` v4 (§11 구현 순서 · §13 묶음 열 개) · `docs/22p_gap/CLAIM_STATUS.yaml` (세대표 · `P22_STAGE3_PRIMARY`) · `docs/09_22P_GAP.md` §10 다음 |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §107 (이 요청의 결정) · §93 E9-0 (한정 실행의 과학 목적) · §106 (76차 종결) |
| 76차 패키지 원본 | `docs/22p_gap/gate76_review/` (zip `b532543b…`, MANIFEST 87/87) |

## §0 왜 지금 이것인가

| 선택지 | 판단 |
|---|---|
| grid_fine 격자를 현행 코드로 `active_claims` 재실행 | **아니오.** ~~grid_fit_v5(진단 전용, 3069 조건 · fit 12276 행)와 코드·config·protocol 이 같아 산출이 같다.~~ **77차 비차단 정정: 바이트 동일 보증이 아니다 (producer `c2ef1a…` ≠ 현행 `1c67a748…`; 그 사이 변경이 보존 구현이라는 것과 산출 동일은 별개). 재실행을 권고하지 않는 충분한 이유는 "같은 설계를 반복해도 v6 의 새 대조·주장을 얻지 못한다" 다.** 지지할 v6 주장이 없고, 현행 digest 는 세대표(`source_digest_generations`)에 없다. 비용 10 시간 |
| `no_active_claim` grid_fit_v5 를 active 로 승격 | **아니오.** 76차가 명시적으로 부여하지 않았다 |
| **단계 3 계약 재심사 → 13 착수** | **예.** 원래 질문(09 문서 §1)에 답하려면 §7 의 primary estimand 를 v6 protocol 로 재야 한다. 계약이 "구현 전 재심사" 를 요구하고, 25차 이후 12 단계(보존)가 46~76차 서른 라운드에 걸쳐 진행됐으나 §13.1 상태표는 25차 기준이다 |

## §1 §13.1 묶음 상태 — 25차 기준표에 **76차까지의 근거**를 붙인다 (닫힘 판정은 리뷰가 한다; 우리는 "부분/미착수" 만 쓴다)

| # | 묶음 | 25차 상태 | 25차 이후 생긴 것 (근거) | 우리가 보는 남은 것 |
|---|---|---|---|---|
| 1 | `planned_protocol` ↔ `execution_receipt` 분리 | 부분 | prospective 계획 항목이 `run_spec`(grid·fit·selection 축, `leg_run_spec`)을 담고 시작 gate 가 그것을 대조한다 (46~53차, §13.4) · 고정 캐시 SHA 만 진입 (74차 G74-1) · 계획 → 실행 기록 → 영수증 → 원장 결속이 실물 다리(`grid_fit_v5`)에서 완주 (73~76차) · `claim_scope` 로 실행 명부와 투영 명부 분리 (74차 G74-3) | stage×objective×arm 별 예산/실현 count 는 여전히 없다 — 단계 3 schema (§2·§3) 의 일이다 |
| 2 | canonical design wire · arm registry · hash domain · golden | 부분 | 변화 없음 (RUN_SCOPE 밖에서 한 것 없음) | 실제 v6 격자 실행과의 end-to-end 결속 · Unicode 정규화 실측 |
| 3 | provider materialize→seal→consumer DAG · `p_ini` arm 별 solution map | 미착수 | 변화 없음 | 전부 — 13 의 몸통 |
| 4 | `mono_tol`/`material_tol` 분리 · stratum · budget adoption · max-failure | 미착수 | 변화 없음 | 전부 |
| 5 | `sentinel_panel.yaml` | 미착수 | 변화 없음 | 전부 (§6.4) |
| 6 | 구 `pairing_design_id`·`inference_status` 제거 · per-key linkage mutation test | 미착수 | 변이 도구는 preimage 1회 강제·EXPECT 관측값·witness 규칙(65~67차)으로 굳었다 — per-key linkage 변이의 **틀**은 있다 | 필드 제거 자체 · linkage 변이 |
| 7 | 상태 schema 단일 authority | 부분 | 상태 3축 + `claim_scope`(74차) · `inference_role` 바닥값 `diagnostic` · `no_active_claim` 증거 계약(74~76차 G74-3/N3) · 실행 class 등록 typed reader (70차 E5) | planned lifecycle 의 나머지는 묶음 9 와 같다 |
| 8 | immutable bundle index · receipt schema | 부분 | 영수증 typed **소비** (70~72차 E3·E3-R: 닫힌 schema · core sha · 묶음 결속 · 원장 `out` 결속) · 묶음 index fail-closed · 구성원 sha · YAML index (70차) · archive index 진입 파싱·병합·동명 identity·엄격 loader·최종화 실패 전파 (74~76차) · validator 식별 ≠ producer 식별 분리 + 원본 history 보존 (74~76차 ⑥) | 비-git backend URI · legacy 다리 외부 store 사본 · 영수증 서명 없음(같은 principal) |
| 9 | 트랜잭션 보존 gate | 부분 | 46~63차 lifecycle 게이트 (CAS·발급·동결·authority 단일화·능력 닫기) · 70차 E6 시험 authority 격리 · 73차 조건부 GO → 실물 실행 완주 (Gabia, 74차 R1 편차 인정) · 실패/재개 정책 E9-R | ~~"실물 provider 어댑터" 는 **이제 있다** (grid_fit_v5 가 그 경로다) — 리뷰가 그렇게 볼지 묻는다 (§4-1).~~ **77차 G77-N1 정정: grid_fit_v5 는 로컬 lifecycle→보관→복원/검증 영수증→원장의 실물 증거이지 §13.2 retention provider/CAS 등록 경로의 증거가 아니다 (receipt URI `artifacts/grid_fit_v5`, `preserve_backend.yaml`·`preserve_index` 부재, `registered == {}`). 78차 §1 이 두 경로를 나눈다.** E1(projection producer 결속)·E2(launcher attestation)·E4(독립 replay)는 사용자 결정으로 미구현 라벨 유지 |
| 10 | historical projection version dispatch | 부분 | cohort 화·frozen 목적지 거부 (26차) · g18 활성 cohort 봉인 불변 (74차 06d) | `row_projection.py` 는 `executed_legs` 를 읽지 않는다 (75차 수용) — v6 cohort 를 만들 때 dispatch 규칙을 다시 본다 |

`grid_fit_v5` 가 보여준 것과 안 보여준 것: 계약 §10 이 요구한 "restore → validate → score" 를 실물 묶음에서 영수증으로 남겼다 (34/33 검사). 보여주지 않은 것: 단계 3 protocol(§2~§7) 은 하나도 돌지 않았다 — 이 실행은 v6_prep 도 v6 도 아니다 (E9-0).

## §2 §11 진행 — 우리가 보는 위치

| 단계 | 상태 (우리 기준) | 근거 |
|---|---|---|
| 11 문서·회귀 재심사 | 25차 이후 열리지 않았다 — **이 요청** | — |
| 12 보존 체계 구축 (§10) | ~~46~76차에 걸쳐 실물 다리로 완주.~~ **77차 정정: 로컬/협조적 환경의 실행·보관 경로는 실물 확인, 운영 보존 profile(backend·retention canary·durable registration)은 부분 — 78차 §1.** **동결 지점은 13 의 끝** 이라는 §11 문장 그대로 — 지금 digest `1c67a748598baadb` 는 12 의 산물이지 pilot 의 digest 가 아니다 | §1 의 8·9 행 · 원장 §54~§63 · §90~§106 |
| 13 RUN_SCOPE 변경 + pilot | **미착수.** 몸통은 묶음 3·4·5·6 + §9.4 restart 행 필드(`converged`·`termination_status`·`n_eval`·`candidate_id`·`bank_index`) + `validate_provenance` 의 깨진 parquet 을 `fail` 로 | §11 · §9.4 |

## §3 13 을 열기 전에 사람이 정해야 하는 것 (계약이 "정의만" 한 것 — §11 2~7)

| # | 결정 | 계약 절 | 우리 제안 (리뷰가 고치면 그대로 따른다) |
|---|---|---|---|
| 1 | candidate mode 3종(`legacy_slot_replace` · `equal_start_count_base_retained` · `union`) 중 무엇을 돌리나 · `B` 의 뜻 | §3 | ~~primary arm 은 `equal_start_count_base_retained` (계약 §6.4 예시 yaml 과 같다 — 양쪽 총 시작점 `B` 동일, `base` 유지)~~ **77차 G77-N2 정정: primary 는 계약 §7 그대로 grid · no-warm · 같은 base·bank·총 B — 후보 배열 `[base]+bank[:B-1]` (mode 라벨과 무관, warm=false). base-retained warm arm 은 §7.2 secondary 다. 78차 §2 한 행.** · `legacy_slot_replace` 는 21차 실험과의 연결을 위한 대조 arm · `union` 은 돌리지 않는다 (`B` vs `B+1` 로 시작점 수가 달라 한 결론에 섞을 수 없다) · bank 는 §4 대로 행 단위 unit cube |
| 2 | 목적함수별 예산 / provider-solution map | §2 · §4.4 | ~~예산은 §6.2 plateau gate 가 정한다 — pilot 전에 숫자를 적지 않는다~~ **77차 G77-N3 정정: 미정인 것은 최종 채택 B 뿐. ladder·최대 B·중단 규칙·floor 측정 단계·자원 상한은 pilot 전에 고정 — 78차 §3.** |
| 3 | plateau sentinel panel 구성 | §6.4 | 계약 최소 구성 그대로: 5 archetype(pristine · 22p 근방 · α-window edge · bounds face · empirical hard) × reference 2 × noise 3(clean + 독립 noisy seed 2) × objective 2 = 60 → n<100 이므로 material 개선 0건 규칙 · budget ladder [5, 10, 20, 40] · empirical hard 는 holdout 필수. 조건 목록은 `sentinel_panel.yaml` 로 파일에 고정 (묶음 5) |
| 4 | primary/secondary estimand 사전 등록 | §7 | ~~`P22_STAGE3_PRIMARY` 의 문장은 `CLAIM_STATUS.yaml` 에 이미 있다 — transition table 을 primary 로 확정~~ **77차 정정: claim ID 존재는 사전 등록이 아니다. primary scalar 는 §7.1 의 Δ 하나, 전이표 네 칸은 그 분해 — 78차 §2.** |
| 5 | 고유 leg 목록 · 비용 재산정 | §9.1 · §9.3 | **다음 산출물.** core-time 기준 (실측 833 s × 28 = 23,324 core-s / 30,690 restart) 으로 leg 마다 적는다 — 이것이 나온 뒤에야 실행 승인을 묻는다 |
| 6 | 원자료를 잃은 warm 7다리의 처리 | §10 · 09 문서 §10-7 | `recorded_projection` 으로 남긴다 (승격 없음) — v6 가 그 주장을 대체한다 |

## §4 리뷰어에게 묻는 것

1. *(77차 답: 로컬 실물 증거 예 · retention provider 증거 아니오 — 78차 §1 로 재정식화)* §1 의 묶음 8·9 에 대해 — grid_fit_v5 완주(계획 → 실행 → 보관 → 영수증 → 원장, 실물)를 "실물 provider 어댑터" 의 증거로 받는가. 아니면 어떤 경계가 더 필요한가 (한 줄).
2. *(77차 답: 12 전체 종료 아니오 · N1–N3 정정 후 제한 오프라인 구현은 조건부 — 78차 §4)* §11 단계 12 를 끝난 것으로 보고 **13 착수**를 승인하는가 — 즉 묶음 3·4·5·6 과 §9.4 필드를 RUN_SCOPE 에 넣는 코드 라운드를 열어도 되는가. (pilot 실행 GO 는 아니다 — 그것은 §3-5 뒤 별도 요청.)
3. *(77차 답: §9.4 다섯 필드는 독립 첫 단계가 아니다 — candidate_id/bank_index 는 묶음 1·2·3 결속에 의존; 78차 §3 의존표)* 13 의 순서 — 우리 제안: (a) §9.4 restart 행 필드 + parquet fail (작고 독립) → (b) 묶음 6 (구 필드 제거, 변이) → (c) 묶음 4 (tolerance·stratum·budget adoption) → (d) 묶음 3 (provider DAG) → (e) 묶음 5 (sentinel panel) → (f) 고유 leg 목록·비용 → pilot 요청. 라운드마다 RUN_SCOPE 가 움직이므로 영수증은 **라운드 끝에 한 번** 재생성 (원본 history 보존) 해도 되는가.
4. §3 의 여섯 결정 중 리뷰가 지금 고정하고 싶은 것.
5. 이 요청이 새 실행 GO 가 아니라는 것 · grid_fit_v5 는 진단 전용 그대로라는 것을 확인한다.

## §5 하지 않는 것

새 계산 없음 · RUN_SCOPE 변경 없음 · 복원 없음 · class/투영 변경 없음 · `STAGE3_CONTRACT.md` §13.1 표는 리뷰 판정 뒤에만 고친다 (이 요청 §1 이 갱신 초안이다).

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **단계 3 계약의 구현 전 재심사 — 12 판정과 13 착수 승인을 묻는다. 실행 GO 는 묻지 않는다.**
