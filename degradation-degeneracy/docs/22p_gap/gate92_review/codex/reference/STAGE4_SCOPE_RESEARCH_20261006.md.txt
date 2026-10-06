# 단계 4 (묶음 6) 범위 조사 — 시작 전 고정 표 초안의 재료

> **성격:** 조사 문서 (스크래치패드 · 저장소 밖). 코드 변경 0 · 커밋 0 · pytest/smoke/변이 실행 0.
> 저장소 안에서 돌린 것은 읽기(grep · git log/show · sed)뿐이다. 계산 하나만 했다: 저장소 밖 `/tmp` 에서
> `python3 -B -c` 로 해시 정의 두 개를 메모리에서 비교 (파일 쓰기 0 · §3.4).
> **기준:** 작업 트리 HEAD `b03d48635` · 판정 코드 `b08bb6944` · source_digest `f0175fff71132003` (원장 §140 이
> "지금 HEAD 의 것" 이라고 확인한 값 — 이 조사에서 RUN_SCOPE 를 다시 해시하지는 않았다).
> **표기:** 【사실】 = 파일:줄로 확인한 것 · 【관찰】 = 정적으로 읽은 것 (실행으로 확인 안 함 — RED 시험으로 재야 함)
> · 【제안】 = 내 제안 (아직 아무도 승인하지 않음).

---

## §0 한 줄 요약

1. 【사실】 `pairing_design_id` · `inference_status` 는 **코드 · 시험 · 데이터 어디에도 없다** — `src/ tools/ scripts/
   configs/ run.sh tests/ docs/22p_gap/*.py` 와 저장소 안 비-md 파일, `results/ artifacts/ reference/` 에서 0건.
   `git log -S` 로도 이 두 이름이 RUN_SCOPE 나 tests 에 들어간 적이 없다. 그러니까 "신규 writer 에서 지우는 일" 은
   **지울 코드가 없는 상태**다. 묶음 6 의 실제 일은 (a) 다시 들어오지 못하게 하는 닫힌 검사 + 음성 시험과
   (b) consumer 별 per-key linkage 음성 시험·변이다.
2. 【관찰】 v6 산출의 `run_spec.stage3` 는 **열린 집합**이다 (`src/io.py:1873` 는 빠진 키만 본다). 16 키 가운데
   validator 가 계획 envelope 나 재계산 값과 **대조하는 키는 7개**다. 나머지 9개는 "있는지" 만 본다:
   `parameter_order_sha256` · `bank_version` · `candidate_mode` · `budget_by_objective` · `warm_provider_map` ·
   `provider_edges_sha256` · `roster_sha256` · `arm` · `stage`. per-key linkage 가 가장 크게 비어 있는 곳이 여기다.
3. 【사실】 `provider_edges_sha256` 의 정의가 **두 개**다. run_spec 쪽은 `src/fitting.py:1545` 에서
   `sha256(json.dumps(sort_keys=True))`, 승인 spec 쪽은 `tools/preserve.py:6656` 에서 `digest()` (canonical) 로
   계산한다. edge 가 하나라도 있으면 두 값이 다르다 (메모리 계산: `a8869e28…` ≠ `3caa0201…`). edge 가 없으면
   (`[]`) 둘이 같다.
4. 【사실】 리뷰어는 단계 3 이 **전부 끝났다고 선언한 적이 없다.** 83차는 "단계 3 전체 완료는 아님", 89차는
   "라운드 2b 종결" 까지만 판정했다. 라운드 2 의 R2-a~g 는 모두 닫혔다 (R2-d 는 "p_ini 거부 유지" 라는 정책으로
   닫힘). 남은 것은 단계 3 이 **명시적으로 미뤄 둔** 항목이다: p_ini · adaptive 진단 arm · 실물 v6 leg · 세대표
   등록 · 운영 원장 v6 계획 · `--mode all`/grid v6. 이것들은 실행 GO 와 엮여 있다.
5. 【사실】 81차 리뷰어 문장 둘이 "단계 4" 에 **claim 세대 게시** 를 함께 붙였다
   (`gate81_review/codex/REVIEW_KO.md:60,129` · `STAGE3_IMPL_ROUND1_SPEC.md:101`). 그런데 2b 고정 §13-5 는
   "실물 v6 leg 가 그 digest 를 얻은 뒤에만 등록" 이라고 정했다. 그래서 실행 GO 없이는 단계 4 에서 게시할 수
   없다 — 열린 질문 Q1.

---

## §1 【사실】 묶음 6 정의의 계보

| 시점 | 문장 (요지 · 원문 좌표) |
|---|---|
| 24차 보충 대응 (`d405d1b85`) | 계약 v4 §13 표 초판: "구 `pairing_design_id`·`inference_status` 제거 · **actual digest 재해시** · per-key linkage mutation test — 미착수" |
| 25차 대응 (`cedaf922e`) | "actual digest 재해시" 를 빼고 지금 문장이 됨. 상태 칸: "묶음 9 의 final gate 는 이것 없이 닫을 수 없다 (25차 Q3)" — `STAGE3_CONTRACT.md:828` (현행) |
| 26차 요청 Q2 | "제거하려면 이미 커밋된 8다리 manifest·summary 를 건드려야 한다 … 옛 바이트는 손대지 않고 adapter?" — `GATE26_REQUEST.md:256–260`. **이 질문에 대한 직접 답은 원장·계약에서 찾지 못했다.** 【사실】 지금 저장소의 8다리 산출(`results/paired_fixed5_v4` 등)에도 두 필드는 없다 — 전제부터 지금 사실과 다르다 |
| 계약 본문의 두 필드 | `pairing_design_id`: §4.2 (`:220` "자유문자로 두지 않는다" → `pairing_design_label` + `pairing_design_sha256` 로 나눔, `:252` 문장에는 옛 이름이 남아 있음) · §8.1 예시 yaml `:611`. `inference_status`: §2.2 adaptive arm 예시 `:164` (`diagnostic_only` 강제) · §8 `:496` (23차 P0-6 이 3축으로 분해) · v2 대조표 `:593–603` · §8.1 예시 `:633` |
| 77차 리뷰 (`gate77_review/codex/REVIEW_KO.md:92`) | "4. 같은 schema 에서 묶음 6 의 **신규 writer 구필드 제거와 consumer 별 linkage 음성 시험**을 붙인다. v5/v6_prep read-only dispatch 와 과거 봉인은 유지한다." · 상태 권고 `:140` "미착수/기반 존재 — 변이 틀과 일부 ID 기반 존재는 인정. **v6 writer/reader 의 구필드 정리·per-key 연결 완료 아님**" |
| 78차 요청 §3.2 (`GATE78_REQUEST.md:106`) | 단계 4 = "묶음 6: 신규 writer 의 구 필드 제거 + consumer 별 per-key linkage **음성 변이**. v5/v6_prep read-only dispatch·과거 봉인 유지" · 의존 3 · RUN_SCOPE `src/` · `tools/` · `mutation_replay.py` |
| 77차 요청 §1 초안 (`GATE77_REQUEST.md:34`) | "변이 도구는 preimage 1회 강제·EXPECT 관측값·witness 규칙(65~67차)으로 굳었다 — per-key linkage 변이의 **틀**은 있다 · 없는 것: 필드 제거 자체 · linkage 변이" |
| 81차 리뷰 (`gate81_review/codex/REVIEW_KO.md:60,86,129`) | ":60 전역 claim 세대표 등록/승격은 여전히 단계 4 이후" · ":86 전체 단계 4 consumer 정비까지 당겨오라는 요구가 아니라 … 최소 version 경계" · ":129 **단계 4 의 전 소비자 구 필드 제거/claim 세대 게시** … 는 별건" |
| 단계 3 고정 표 §8 (`STAGE3_IMPL_ROUND1_SPEC.md:101`) | "단계 4(구 필드 제거·claim 세대 게시)~6" |

**표현 차이 (Q2 재료):** 77차 리뷰어는 "linkage **음성 시험**" 이라고 썼고, 우리 78차 표는 "per-key linkage
**음성 변이**" 라고 옮겼다. 계약 원문은 "per-key linkage **mutation test**" 다. 무엇이 필수 증거인지가 갈린다 —
데이터 변조(음성 fixture), 코드 변이(mutation_replay), 아니면 둘 다.

**계약 §13.1 표의 상태:** 【사실】 `STAGE3_CONTRACT.md:817` 은 "이 표 본문은 77차 판정 뒤에만 고친다" 고 적었지만
본문(`:821–832`)은 아직 25차 기준이다. 묶음 3 은 "미착수" 로, 묶음 6 은 "미착수" 로 그대로 남아 있다. 77차 리뷰가
§5 (`REVIEW_KO.md:131–146`) 에 갱신 권고 표를 줬지만 계약에는 반영되지 않았다.

---

## §2 【사실】 단계 3 은 끝났나 — 리뷰어 판정과 미룬 항목

| 라운드 | 판정 (원문 좌표) | 닫힌 것 |
|---|---|---|
| 1 (81–83차) | 83차 "승인된 라운드 1 범위 종결 — **단계 3 전체 완료는 아님**" (`gate83_review/codex/REVIEW_KO.md:5,87` · 원장 §118 `:8610,8621`) | 3-A 결속 · 3-B provider DAG (condition stage) · 3-C 행 10 키 · `candidate_id`/`bank_index` serializer·validator · unit-cube bank · roster · planned/realized |
| 2a (85–86차) | 86차 `ACCEPTED_ROUND2A_CLOSED_NO_EXECUTION_GO` (원장 §125) | R2-b (base-config hex64 · 시작 전 공통 경계) · R2-e (dead 정의) · R2-f (계약 §1 v6 열) · R2-g (`finite`/`converged` · record v2) |
| 2b (87–89차) | 89차 `ACCEPT_G88_N1_AND_CLOSE_STAGE3_ROUND2B` — "제한 구현 라운드 2b 의 종결" (`gate89_review/codex/REVIEW_KO.md:3,65` · 원장 §134) | R2-a (v3 spec · 계획 index v4 자리 · 진입점 · CLI) · R2-c (세대 이름 `v6` 하나 · validator digest 미등록) · G84-N2 · G87-N1 (fit-only phase) · G88-N1 |
| R2-d | 84차 "p_ini 거부 유지: 수용 · 지원 구현으로 확대하지 않는다" (`gate84_review/codex/REVIEW_KO.md:82,91`) | 정책으로 닫힘 (코드 0) |

**단계 3 이 명시적으로 미뤄 둔 것** (모두 "승인 밖" 으로 반복됨 — 89차 `REVIEW_KO.md:69` · 원장 §126 `:8841` ·
고정 표 §8 `:101` · §13-1 `:267`):
`stage="p_ini"` edge 구현 (선언만 있고 명시 거부) · adaptive diagnostic arm (계약 §2.2 — `adaptive=False` 만) ·
union 연구 실행 · 실물 v6 연구 leg · 운영 원장 `LEG_PRESERVATION.yaml` 에 v6 계획 항목 · `source_digest_generations`
세대표 등록 · `--mode all` v6 · grid v6 · provider 운영 canary · class/투영 게시.

【관찰】 `candidate_id`/`bank_index` 와 provider DAG (condition stage) 는 라운드 1 에서 serializer → validator 까지
이어졌고, 그 뒤 라운드에서 다시 열린 기록은 없다. 단계 4 의 선행조건인 "단계 3" 은 **리뷰가 승인한 범위** 기준으로는
충족됐다. 다만 "단계 3 전체 완료" 라는 판정 문장은 아무도 쓰지 않았다 → Q3.

**단계 4 를 제약하는 리뷰어 문장 모음 (그대로 따를 것):**
- 과거 봉인·v5/v6_prep read-only dispatch 유지 (77차 `:92` · 78차 §3.2).
- "기존 기록의 필드를 소급 삭제하지 않는다" (77차 N3 의존표 1 `:89` · 78차 §3.2 단계 1).
- 81차 N2 의 dispatch 원칙: 선언 문맥으로 dispatch · 행 모양으로 세대를 추론하지 않음 · legacy/prep fallback 금지 ·
  "현행 digest 가 CLAIM_STATUS 표에 없다는 이유로 v6 를 추론하지 않음" (`gate81 REVIEW_KO.md:75–84`).
- 세대표 등록은 실물 v6 leg 뒤에만 (2b §13-5 · 87차 `REVIEW_KO.md:70` 수용).
- 처음부터 GREEN 인 대조군은 정상이다 — "처음부터 통과하면 fixture 의심" 을 모든 시험에 적용하지 않는다 (81차 §7-4 `:126`).
- 같은 치환 지점의 변이 둘을 독립 커버리지로 세지 않는다 (89차 limits · 원장 §134 `:9074,9082`).

---

## §3 【사실/관찰】 구 필드의 writer · consumer 전수, 그리고 인접한 linkage 사실

### 3.1 두 이름 그대로 — 0건

| 범위 | 결과 |
|---|---|
| `src/ tools/ scripts/ configs/ run.sh tests/ docs/22p_gap/*.py` (py · sh · yaml · json) | **0** |
| `git ls-files` 의 비-md 파일 | 리뷰 패키지 안의 **보존된 문서 사본** (`gate7x–8x_review/codex/**/*.json` · `G77_CORRECTIONS.diff`) 뿐 — 실행 코드·데이터 아님 |
| 추적 안 되는 `results/ artifacts/ reference/` | **0** |
| `git log -S` (RUN_SCOPE · tests · `docs/22p_gap/*.py`) | `pairing_design_id`: 0 커밋. `inference_status`: `*.yaml` 에서만 `0ca48cbf3` (LEG_PRESERVATION 주석으로 들어옴) → `d405d1b85` (제거) |
| 남아 있는 곳 (문서) | `STAGE3_CONTRACT.md:164,220,252,496,593,611,633,828` · `GATE23/26/77/78/81_REQUEST.md` · 원장 `:2286,2384` |

⇒ writer / historical reader / validator 로 분류할 **코드 줄이 없다.** 그래서 "신규 writer 에서 제거" 는
**부재를 증명하는 일**이 된다 — 닫힌 키 검사가 두 이름을 거부함을 consumer 마다 음성 시험으로 고정한다.

### 3.2 같은 뜻의 현행 이름 (대체된 정본)

| 구 이름 | 현행 정본 | writer | consumer · validator |
|---|---|---|---|
| `pairing_design_id` | `pairing_design_sha256` (정본) + `design_label` (hash 밖) | `tools/design_wire.py:307` (`pairing_design_sha256`) · `tools/preserve.py:2340,2394` (PlannedLeg/V4 필드) · `:2348,2405` (`design_label`, hash 밖) · `src/fitting.py:1541` (run_spec.stage3) | `design_wire.py:312` (`label` 키 명시 거부) · `:300–318` (설계 닫힌 키) · `preserve.py:3142,3189` (envelope hex64) · `:6652,6671` (v3 축) · `fitting.py:1364–1370` (진입점) · `:1460` (`_prepare_stage3`) · `io.py:1684` (validator 3자 대조) |
| `inference_status` (v2 단일 축) | `preservation_status` · `validation_status` · `inference_role` (계약 §8 `:501–505`, 유일 정본) + per-claim `claim_roles` | `preserve.py::finalize_leg` (`:8929~`, 원장 항목 기록 `:9191–9198`) | `tests/test_docs_lint.py:2342` (enum 단일 authority) · `:2639` (허용 튜플) — **닫힌 키 검사는 아니다**: 원장 항목에 `inference_status` 키를 더해도 이 두 시험은 보지 않는다 【관찰】 |

### 3.3 v6 산출물별 키 집합 — 닫힘 여부 (구 필드가 다시 들어올 수 있는 자리)

| v6 자료 | 닫힘 검사 | 좌표 | 구 필드를 넣으면 |
|---|---|---|---|
| 설계 spec | 닫힘 + `label` 명시 거부 | `design_wire.py:300–318` | 거부 |
| `planned-leg/v4` envelope | 닫힘 | `preserve.py:3049,3180` | 거부 |
| v3 승인 spec `stage3` 축 | 닫힘 | `preserve.py:6636,6661` | 거부 |
| 계획 index 항목 | 닫힘 (필수 + 선택 3) | `preserve.py:3942–3961,6270–6272` | 거부 |
| `stage3_context` | 닫힘 `{design, provider_runs}` | `preserve.py:6176` | 거부 |
| execution record v1/v2 · realized | 닫힘 | `preserve.py:3058,3297,3318,3326` | 거부 |
| restart 행 (v6 10 키) | 닫힘 | `io.py:813,829` · `fitting.py:395` (`declared="v6"`) | 거부 (`mixed_invalid`) |
| roster 항목 · provider edge | 닫힘 | `design_wire.py:751,865` | 거부 |
| **`run_spec.stage3`** | **열림 — 빠진 키만 봄** | `io.py:1522–1528,1873` | **통과** 【관찰】 |
| **`run_spec` 최상위** (v5 · v6 공통) | 열림 — 빠진 키/None 만 봄 | `io.py:2127–2143` | 통과 【관찰】 (v5 는 역사 reader 라 닫으면 안 됨) |
| **`candidate_map.json` 최상위 · 항목** | 열림 — `schema` · `entries` 만 보고, 항목은 `.get` 으로 읽음 | `io.py:1927–1931` · `_stage3_rederive :1714–1796` | 통과 (record digest 를 다시 맞추면) 【관찰】 |
| solution map header | 열림. 다만 파일 바이트 sha 가 계획 edge 에 봉인됨 | `fitting.py:566–582` | 바이트 sha 불일치로 거부 |
| `LEG_PRESERVATION.yaml` 항목 | 열림 (3축 튜플만 봄) | `tests/test_docs_lint.py:2659–2665` | 통과 【관찰】 (v6 항목 작성은 승인 밖) |

### 3.4 per-key linkage — consumer 별 현황

**C7 validator `src/io.py::_stage3_checks` (`:1862`) / `_stage3_rederive` (`:1660`) 가 `run_spec.stage3` 의 각 키를 무엇과 대조하나:**

| `run_spec.stage3` 키 (writer `fitting.py:1539–1548`) | validator 대조 | 좌표 |
|---|---|---|
| `planned_id` | `digest(planned_envelope)` | `io.py:1883` |
| `planned_envelope` | `check_planned_envelope` + schema v4 | `io.py:1881–1885` |
| `pairing_design` | 재유도 입력 (`pairing_design_sha256` 재계산) | `io.py:1674–1680` |
| `pairing_design_sha256` | 재계산 == s3 == env | `io.py:1684` |
| `exact_bounds_sha256` | `run_spec.bounds` 에서 재계산 == s3 == env | `io.py:1695–1697` |
| `base_config_closure_sha256` · `_keys` | 스냅샷에서 재계산 · extends 구성원 독립 유도 | `io.py:2015–2048` |
| `parameter_order_sha256` | **s3 값은 대조 안 함** — env 값만 설계와 대조 | `io.py:1686` (env 만) |
| `bank_version` | **대조 없음** (재유도는 `env["bank"]` 를 씀) | `io.py:1701,1734` |
| `candidate_mode` · `budget_by_objective` · `warm_provider_map` | **대조 없음** (재유도는 `env["stages"][0]` 을 씀) | `io.py:1700,1704,1749` |
| `provider_edges_sha256` | **대조 없음** (정의도 승인 spec 과 다름 — 아래) | `fitting.py:1545` vs `preserve.py:6656` |
| `roster_sha256` | **대조 없음** (record · 재구성 roster 는 env 와 대조) | `io.py:1980,2001` |
| `arm` · `stage` | **대조 없음** | — |

- 【사실】 `run_signature_재계산` (`io.py:2348`) 은 run_spec 전체를 sha1[:12] 로 묶는다. 그래서 단순 변조는
  잡힌다. 하지만 이 저장소의 표준 반례는 "**자기일관 위조**" 다 — 서명·봉인·record digest 를 다시 맞춘 위조.
  `tests/test_gate82_residuals.py:33–67` 의 `_reseal_fits` · `_rewrite_record` · `_forge_stage3` 가 그 도구다.
  그 모델에서는 9 키의 **사본**이 계획과 달라도 통과한다 【관찰 — RED 시험으로 확인해야 함】.
- 【사실】 이 9 키를 run_spec 에서 읽는 다른 consumer 는 찾지 못했다 (`fitting.py:600,797` 은 run_spec 이 아니라
  task 의 s3 를 읽고, task s3 는 env 에서 만든다 `:1534–1537`). 지금은 "읽는 이가 없는 사본" 이다. 위험은
  나중에 생길 consumer (scoring · 영수증 · 원장 기록) 가 이 사본을 정본으로 믿는 경우다.
- 【사실】 `provider_edges_sha256` 이 두 벌이다. `/tmp` 에서 같은 edge 한 개로 두 식을 계산하면
  `a8869e288bcaa82e…` vs `3caa0201d814a57b…` 로 다르다. 빈 목록에서는 둘 다 `sha256(b"[]")`. 지금까지의 v6 시험은
  대부분 no-warm (빈 edge) 이라 차이가 드러나지 않았을 가능성이 있다 【관찰】.

**C3 계획 index `preserve.py::_check_v6_plan_slots` (`:6123`) — 승인 spec `stage3` 축 ↔ envelope 유도값:**
`:6168–6175` 는 dict **전체**를 비교하므로 9 키 모두 대조된다. 하지만 키별 음성 시험은
`tests/test_gate87_round2b.py:420` `s03_05` 가 5 키만 다룬다 (`planned_id` · `roster_sha256` · `provider_edges_sha256` ·
`arm` · `candidate_mode`). `pairing_design_sha256` · `parameter_order_sha256` · `bank` (+ 하위 키) · `stage` 는
키별 음성 node 가 없다 【사실】.

**그 밖의 consumer (이미 키별 대조가 있음 — 음성 시험 범위 확인용):**

| # | consumer | 대조하는 linkage 키 | 좌표 |
|---|---|---|---|
| C1 | `check_envelope_v4` / `check_planned_envelope` | envelope 내부 (hex64 · stage · arm · provider edge 1:1) | `preserve.py:3170,3275` |
| C2 | `check_execution_record` | `leg_id` · `planned_id` · `source_digest` · `protocol_generation` · counts | `preserve.py:3287–3346` |
| C4 | `stage3_context_from_plan` | index planned_id 재대조 · 설계 sha · parameter_order sha · provider 디렉터리 | `fitting.py:1324–1385` |
| C5 | `_stage3_preflight` / `_prepare_stage3` | curves · base-config · reference · roster · provider map 재생성 sha · 설계 sha | `fitting.py:1386,1431–1549` |
| C6 | `provider_x0` | map 바이트 sha · header 3 키 · parameter_order · cond_id · bounds | `fitting.py:558–593` |
| C7 | `_stage3_rederive` (행 단위) | `pair_group_id` · `bank_id` · `warm_provider_objective` · (i, source, bank_index) · x0 · `candidate_id` · restart 행 ↔ map | `io.py:1726–1796` |
| C8 | `_assert_fit_authorized` (v3 claim 대조) | `leg_run_spec_v3(…, stage3_axis_from_envelope(ctx))` | `fitting.py:1254` |
| C9 | `finalize_leg` fit-only | `consumed.external_input` · `input_package_digest` · inputs | `preserve.py:8929~` · `:6721` |
| C11 | `check_roster` · `check_provider_edges` | obs_key · cond_id · edge 키 | `design_wire.py:768,830` |

---

## §4 【사실】 `docs/22p_gap/mutation_replay.py` 의 구조 (9351 줄 · RUN_SCOPE 밖)

| 요소 | 내용 · 좌표 |
|---|---|
| 대상 파일 상수 | `:36–58` (`PRESERVE` · `FITTING` · `IO` · `DW` · `RUNSH` · `MKR` …) — 새 대상이 필요하면 여기 추가 |
| sandbox | `:62–78` — 저장소를 임시 디렉터리로 복사해 그 안에서만 변이 (46차 #9) |
| `MUTANTS` | `:80~` 리스트. 원소 = `(이름, 파일, old 조각, new 조각, 빨개져야 하는 -k 식)`. 이름 끝에 라운드 태그 `-gNN`. 예: `-g87` 블록 `:2118–2210` (`"stage3-axis-is-derived-not-copied-g87"` `:2147` → `-k s03_05`) |
| `MULTI` | `:2381~` — 같은 성질을 지키는 여러 자리를 함께 되돌리는 변이 (`(이름, 파일, [(old,new)…], -k)`) |
| `DECLARED_MASKED` | `:2824~` — 관측이 안 되는 변이를 신고하는 곳 (§140 기준 "선언 11") |
| preimage 규칙 | old 조각이 대상 파일에 **정확히 1회** 나와야 함. 0 회 (코드가 옮겨 가서 죽은 변이) 와 2 회 (자리 모호) 는 등록부 불성립 (`:1884–1885,2809` 의 사례). 이 파일 자신을 변이할 때는 철자를 escape (`:926,1092`) |
| 판정 `_check` | `:3045–3130` — baseline 이 녹색이어야 함 · 변이 뒤 rc == 1 · call 단계 실패만 · **실패 node 집합 == EXPECT["fail"]** (더 빨개져도, 덜 빨개져도 실패) · node 마다 **witness** 문자열이 실패 메시지에 있어야 함 · 빈 기대 집합 금지 |
| `EXPECT` | `:3227~` dict `{이름: {"fail": [node…], "witness": {node: 문자열}}}` — 손으로 쓰지 않고 `--emit-expect` **관측값**을 옮김. `-g87` 블록 `:6677~` |
| 신원 | `_registry_digest` · `_expect_digest` · `_runner_digest` (`:7503–7530`) — 증거에 남기는 등록부 identity |
| 실행 | `main` `:7402` · `--list` · `-k <이름 부분>` · `--emit-expect` · 전체 재생 (§140 기준 scenario 423 / 실행 412 / 검출 412 / 생존 0 / 선언 11) |
| 라운드 절차 (87–91차 관행) | RED → GREEN → 변이 추가 → `-k gNN --emit-expect` 로 관측 → EXPECT 등록 → `-k gNN` rc 0 → 전체 회귀 · smoke → **등록부 전체 재생** (start HEAD = end HEAD · dirty 0 · 다른 시험 동시 실행 없음) |

**per-key linkage 의 기존 모양:** 키별 parametrize 시험 하나 (`s03_05[key]`) + "비교 전체를 끈다" 변이 하나
(`stage3-axis-is-derived-not-copied-g87`, EXPECT 에 5 node). dict 전체 비교에서는 "키 하나만 비교에서 빼는" 코드
변이가 자연스럽지 않다. 그래서 키별 증거는 **데이터 쪽 음성 node** 가 맡고, 코드 변이는 그 비교 자리마다 하나씩
두는 것이 지금까지의 관행이다.

---

## §5 【제안】 단계 4 시작 전 고정 표 초안 (§13 · §15 형식 — 고정 표 파일 `§16` 후보)

> 아래는 전부 제안이다. 사용자 승인과 (필요하면) 범위 확인 게이트 뒤에만 고정한다. 표와 다른 선택이 필요해지면
> 구현하지 않고 멈춰 묻는다.

### 16-1. 범위

| 항목 | 내용 |
|---|---|
| 항목 | 묶음 6 = (A) 구 필드 **부재 고정**: v6 writer 산출에 두 이름이 없고, v6 consumer 가 그 키를 거부함을 고정 · (B) **consumer 별 per-key linkage 음성**: v6 linkage 키마다, 그 키를 읽는 consumer 마다 "그 키 하나만 어긋난 자기일관 위조" 를 거부함을 고정 · (C) 그 과정에서 드러난 **두 벌 정의 제거** (`provider_edges_sha256`) |
| 생산 파일 상한 (안) | `src/io.py` (`_stage3_checks` 의 s3 닫힘 · 키별 대조, sig 6 분기 안에서만) · `src/fitting.py` (run_spec.stage3 블록을 `stage3_axis_from_envelope` 재사용으로 · 두 벌 제거) · `tools/preserve.py` (재사용 helper 노출이 필요할 때만). `run.sh` · `scripts/` · `configs/` · `requirements*` · `src/grid.py` · `tools/design_wire.py` 는 손대지 않음 — 필요하면 멈추고 묻는다 |
| 함께 | `tests/test_gate92_stage4_linkage.py` (새 파일 · RED 먼저 · node `k00`– · `conftest._GATED_ENTRYPOINT_MODULES` 확인 · 88/89 모듈과 동시 실행 금지) · `docs/22p_gap/mutation_replay.py` (`-g92`) · 계약 §13.1 묶음 6 행 갱신 (닫힘 판정은 리뷰가 함 — "부분/구현 제출" 까지만) · 영수증 history 보존 → 두 leg 1 회 · 전체 회귀 · smoke · 등록부 전체 재생 → GATE92 |
| 하지 않음 | v5 (sig 5) 검사 · `run_spec` 최상위 닫힘 (v5 공통 경로) · `planned-leg/v3` · v2 spec · 과거 manifest/fits/receipt 바이트 · `row_projection.py` · golden · 세대표 등록 · claim 세대 게시 (Q1) · 운영 원장 v6 계획 · p_ini · adaptive · 실행 GO · 새 연구 leg · class/투영 · requirements |

### 16-2. 고정 결정 (안)

| # | 결정 | 근거 |
|---|---|---|
| a | **부재는 닫힌 집합으로 증명한다.** 두 이름 전용 deny-list 를 만들지 않는다 (이름 하나만 막으면 같은 뜻의 세 번째 이름이 열림). 닫힌 집합이 이미 있는 9 자리 (§3.3) 는 음성 node 만 더하고, 열린 자리 중 **v6 전용**인 `run_spec.stage3` 와 `candidate_map.json` (최상위 `{schema, entries}` · 항목 `{cond_id, objective, i, source, candidate_id, bank_index, x0_sha256}`) 을 sig 6 분기 안에서 닫는다 | 최소주의 사다리 — 기존 닫힘 관행 재사용 · 81차 N2 "새 version validator: 키 삭제/세대 혼입/타입 불일치 거부" |
| b | `run_spec.stage3` 의 계획 유래 키는 **envelope 에서 다시 유도한 값과 키별로 같아야** 한다. 유도 함수는 하나: `tools/preserve.py::stage3_axis_from_envelope` 를 쓰고, 그 함수에 없는 키 (`bank_version` · `budget_by_objective` · `warm_provider_map` · `exact_bounds_sha256`) 는 env 의 해당 자리와 직접 비교한다. 불일치 이유는 **키 이름을 담는다** (키별 음성 node 의 witness) | 87차 §13-2 c "유도 하나 · 두 벌 금지" 를 run_spec 쪽에도 적용 |
| c | `provider_edges_sha256` 정의는 `digest(env["provider_edges"])` (canonical) **하나**로 한다. `fitting.py:1545` 의 `json.dumps` 식은 지운다. 바뀌는 것은 v6 run_spec 바이트뿐이다 — 실물 v6 leg 가 0 이므로 과거 봉인 영향 0 (smoke · 시험 fixture 는 다시 생성) | §3.4 사실 3 · Q4 |
| d | 대안 b′ (선택지로 제시 — Q5): 사본 9 키를 run_spec.stage3 에서 **지운다** (`planned_envelope` · `planned_id` 가 이미 정본을 들고 있음). 장점은 linkage 표면 축소, 단점은 v6 run_spec schema 변경과 `_STAGE3_SPEC_KEYS` 축소다. 기본 제안은 b (대조) — 지우는 쪽이 "구 필드 제거" 와 섞여 범위가 흐려지기 때문 | 사용자 결정 |
| e | v5 · v6_prep 경로는 **바이트 · 판정 불변**: sig 5 의 `validate_provenance` 검사 집합 · `normalize_restart_record(declared=None/legacy/v6_prep_logging)` · `g79_06` · `g79_02` 골든 · s00 v5 spec digest · 운영 원장 `planned_index()` 결과 | 77차 `:92` · 78차 §3.2 · 81차 N2 |
| f | per-key 음성은 consumer 마다 **그 consumer 의 실제 호출 경로**에서 잰다 (helper 단위가 아님). 위조는 자기일관으로 만든다 — 서명 · fits 봉인 · record digest · planned_id 를 다시 맞춘 뒤 **그 키 하나만** 어긋나게. 기존 도구 `test_gate82_residuals.py::_forge_stage3` · `_reseal_fits` · `_rewrite_record` 를 재사용하고 run_signature 재서명 helper 만 새로 둔다 | 반례 모델 = 자기일관 위조 (82·85·89차) |
| g | 계약 §13.1 은 묶음 6 행만 고친다 ("미착수" → 제출 증거 링크 · "닫힘" 은 쓰지 않음). 다른 행 (3 · 1 · 2 …) 의 77차 권고 반영은 별도 문서 정정으로 분리 (Q6) | 25차 정정 "닫힘 판정은 리뷰가 한다" |

### 16-3. 회귀 (RED 먼저 · 새 파일 · node `k00`–)

| node | 내용 | RED 기대 (지금 코드) |
|---|---|---|
| k00 대조 (GREEN) | 정상 v6 run (G81 `_v6_context` · `_run_v6` 재사용) → `validate_provenance` 실패 0 (dirty 제외) · sig 5 정상 run 검사 집합 · 판정 불변 · `g79_06` 세 결과 불변 · s00 v5 digest 불변 | 통과 (골든) |
| k01 부재 | 정상 v6 산출 (`manifest.yaml` · `execution_record.json` · `candidate_map.json` · `fits.parquet` 열 · restart 행) 을 재귀로 훑어 `pairing_design_id` · `inference_status` 키가 0 | 통과 (부재 확인 — 처음부터 GREEN 정상) |
| k02 닫힌 자리 음성 ×N | `pairing_design_id` / `inference_status` 를 각 닫힌 자리 (설계 · envelope v4 · v3 축 · 계획 index 항목 · record · realized · restart 행 · roster · edge) 에 넣으면 거부 — parametrize `[자리-이름]` | 통과 (기존 닫힘 — 대조) |
| k03 run_spec.stage3 닫힘 | 정상 run 의 `run_spec.stage3` 에 `pairing_design_id` (또는 `inference_status`) 추가 + 자기일관 재서명 → `validate_provenance` 의 `stage3_schema` 실패 · 이유에 키 이름 | **failed** (지금은 missing-only — 통과해 버림) |
| k04 candidate_map 닫힘 | 최상위 / 항목에 구 필드 추가 + record `candidate_map_sha256` · `record_digest` 재계산 → `candidate_map` 실패 | **failed** |
| k05 s3 per-key ×9 | `parameter_order_sha256` · `bank_version` · `candidate_mode` · `budget_by_objective` · `warm_provider_map` · `provider_edges_sha256` · `roster_sha256` · `arm` · `stage` 를 하나씩 계획과 다른 **형식상 유효한 값**으로 바꾸고 자기일관 재서명 → 거부 · 이유에 그 키 | **9 failed** (DID NOT RAISE/ok=True) 【관찰 기반 예측】 |
| k06 s3 per-key 대조 ×5 | 이미 대조되는 `planned_id` · `pairing_design_sha256` · `exact_bounds_sha256` · `base_config_closure_sha256` · `_keys` 를 하나씩 → 거부 | 통과 (기존 — 키별 증거 고정) |
| k07 edge 정의 하나 | warm edge 가 있는 계획 (G81 warm fixture) 으로 run → `run_spec.stage3.provider_edges_sha256 == stage3_axis_from_envelope(env)["provider_edges_sha256"]` | **failed** (두 식의 값이 다름) |
| k08 계획 index per-key 보강 | `s03_05` 에 없는 키 `pairing_design_sha256` · `parameter_order_sha256` · `bank` (+ 하위 키 각각) · `stage` → `planned_index` 거부 | 통과 (dict 전체 비교가 이미 있음 — 키별 증거 보강, 대조) |
| k09 consumer 경로별 | C4 (진입점: 설계 sha · parameter_order sha) · C6 (map header 3 키 · parameter_order) · C2 (record `leg_id` · `source_digest` · `protocol_generation`) 에서 키 하나씩 → 각 consumer 가 거부 · 이유 | 대부분 통과 (기존) — 빠진 키가 RED 로 드러나면 그 키만 범위에 넣음 |

RED 집계 규칙 (81차 §7-4 · 83차 설명 정밀화): 새 helper 부재 · `AttributeError` · 무관한 예외로 떨어진 node 는 따로
센다. 처음부터 GREEN 인 대조 node (k00 · k01 · k02 · k06 · k08) 는 정상이다. 결함 증거는 k03 · k04 · k05 · k07 뿐이다.

### 16-4. 변이 (`-g92`)

| 이름 (안) | 바꾸는 것 | 죽이는 node |
|---|---|---|
| `stage3-run-spec-keys-are-closed-g92` | `_stage3_checks` 의 새 닫힘 검사를 끈다 | k03 |
| `candidate-map-keys-are-closed-g92` | candidate map 최상위/항목 닫힘을 끈다 | k04 |
| `stage3-run-spec-is-derived-per-key-g92` | 키별 유도 대조 루프를 끈다 (자리 하나) | k05 ×9 |
| `stage3-run-spec-env-direct-keys-g92` | 유도 함수 밖 4 키의 env 직접 대조를 끈다 (k05 에서 그 4 키만 죽어야 — 같은 자리면 하나로 합치고 독립 커버리지로 세지 않음) | k05 [해당 4] |
| `provider-edges-sha-has-one-definition-g92` | `fitting.py` 블록을 옛 `json.dumps` 식으로 되돌린다 | k07 |

- 기존 변이 증인 (특히 `-g81` · `-g82` · `-g84` 의 run_spec 위조 시험) 이 바뀌면 멈추고 보고한다. 바뀐 것은
  `--emit-expect` 관측값으로만 갱신하고 원래 증인은 주석에 남긴다 (60차 선례 · 89차 §15-4).
- 같은 치환 지점의 변이를 둘로 세지 않는다 (89차 limits).

### 16-5. 영수증 · 순서

`src/io.py` 가 바뀌므로 validator identity 가 움직인다. 2b 는 io.py 를 일부러 피했지만 이번에는 피할 수 없다.
→ 현행 영수증 (`f0175fff71132003` 세대) history 보존 → `paired_fixed5_v4` · `grid_fit_v5` 각 1 회 재생성 (v5 leg 이므로
**검사 집합 35 / 34 불변**이 기대값. 바뀌면 멈춤) → 전체 pytest · smoke (clean) · 등록부 전체 재생 → GATE92.
순서: 고정 표 커밋 (코드 변경 전) → RED 커밋 → GREEN → 변이 + EXPECT → 영수증 → 전체.

### 16-6. 보류 (이 라운드에 넣지 않음)

- claim 세대 게시 · `source_digest_generations` 등록 (Q1 — 실물 v6 leg 필요).
- `run_spec` 최상위 닫힘 (v5 와 공유하는 경로 — 넣으려면 sig 6 분기 설계가 따로 필요).
- `LEG_PRESERVATION.yaml` 항목 닫힘 (운영 원장 v6 항목 자체가 승인 밖. 닫힌 키 검사는 v6 항목이 생길 때).
- 계약 §13.1 의 다른 행 갱신 (Q6).
- `validator_tree_dirty` 순서 개선 (§140 후보 (2)).

---

## §6 열린 질문 (사용자 · 리뷰어가 정할 것)

| # | 질문 | 왜 열려 있나 | 내 기본 제안 |
|---|---|---|---|
| Q1 | 단계 4 에 "claim 세대 게시" 가 들어가나? | 81차 리뷰 `:60,129` 와 고정 표 §8 `:101` 은 단계 4 에 게시를 붙였다. 2b §13-5 는 실물 v6 leg 뒤에만 등록한다고 정했다. 실행 GO 없이는 게시할 대상이 없다 | 게시는 단계 4 밖 (실행 뒤 별도 gate). 단계 4 는 묶음 6 만 |
| Q2 | 필수 증거가 "음성 **시험**" (77차 리뷰어) 인가, "음성 **변이**" (78차 우리 표) 인가, "mutation test" (계약) 인가? | 표현이 셋이다 | 둘 다 — 키별 데이터 음성 node (k05 · k08) + 비교 자리마다 코드 변이 하나 (§16-4). "키 수만큼 코드 변이" 는 요구하지 않는 것으로 확인받기 |
| Q3 | 단계 3 을 "완료" 로 보고 단계 4 에 착수해도 되나? | 83차 "단계 3 전체 완료 아님" 이후 "전체 완료" 판정 문장이 없다. 라운드 1 · 2a · 2b 는 모두 종결 | 리뷰 승인 범위 기준 충족으로 보고 범위 확인 게이트에서 한 줄로 확인받기 |
| Q4 | `provider_edges_sha256` 두 벌을 이번에 하나로 고치나? | 단계 3 산출 정의의 정정이라 "단계 3 잔여" 로도 읽힌다. 실물 v6 leg 0 이라 과거 봉인 영향은 0 | 단계 4 에 포함 (per-key linkage 의 전제 — 같은 이름의 키가 consumer 마다 다른 값이면 linkage 를 말할 수 없음) |
| Q5 | run_spec.stage3 의 사본 9 키 — **대조** (b) 인가 **삭제** (b′) 인가? | 삭제는 v6 schema 변경. 대조는 검사가 늘어남 | b (대조) |
| Q6 | 계약 §13.1 표 갱신 — 묶음 6 행만인가, 77차 권고 전체 반영인가? | `:817` 약속 ("77차 판정 뒤에만 고친다") 이 아직 이행되지 않았다 | 묶음 6 행만 이번에. 전체 반영은 문서 전용 정정으로 분리 (RUN_SCOPE 밖) |
| Q7 | 범위 확인 게이트 (81·84차처럼 "92차 = 범위 확인", 구현은 93차) 를 둘 것인가, 고정 표만 커밋하고 바로 구현할 것인가 (87–89차 방식)? | 단계가 바뀌는 첫 라운드다. 단계 3 첫 라운드는 범위 확인 (81차) 부터 했다 | 범위 확인 게이트를 먼저 — 특히 Q1 · Q2 · Q5 는 리뷰어 답이 필요 |
| Q8 | 생산 파일 상한에 `src/io.py` 를 넣어도 되나? | 2b 는 io.py 를 일부러 피해 validator 를 고정했다. 이번에는 validator 가 바뀌어야 linkage 가 생긴다 → 영수증 재생성 비용 (두 leg 1 회) | 넣는다 (대안: validator 를 고치지 않으면 k03–k05 를 닫을 수 없다) |
| Q9 | 묶음 6 이 닫히면 묶음 9 의 final gate 선행조건 ("묶음 6 없이 닫을 수 없다", `:828` 25차 Q3) 이 해소되나? | 묶음 9 의 남은 것은 "실물 provider 어댑터" (`:831`) — 묶음 6 과 별개로 남는다 | 해소는 "선행 하나 충족" 까지만 주장. 묶음 9 종결 주장은 안 함 |

---

## §7 근거 좌표 (빠른 찾기)

| 무엇 | 좌표 |
|---|---|
| 묶음 6 행 | `docs/22p_gap/STAGE3_CONTRACT.md:828` (§13.1 `:819–832`, 갱신 약속 `:817`) |
| 단계 4 정의 | `docs/22p_gap/GATE78_REQUEST.md:106` (§3.2 `:99–108`) |
| 77차 리뷰 의존표 · 상태 권고 | `docs/22p_gap/gate77_review/codex/REVIEW_KO.md:87–94,131–146` |
| 81차 리뷰 단계 4 언급 | `docs/22p_gap/gate81_review/codex/REVIEW_KO.md:60,86,129` |
| 83차 "단계 3 전체 완료 아님" | `docs/22p_gap/gate83_review/codex/REVIEW_KO.md:5,87` · 원장 `docs/08_REVIEW_RESPONSE.md:8610,8621` |
| 89차 2b 종결 · 금지 범위 | `docs/22p_gap/gate89_review/codex/REVIEW_KO.md:3,63–69` · 원장 `:9060–9089` |
| 91차 종결 · 현행 identity | 원장 `:9241–9285` (§140) |
| 고정 표 형식 원본 | `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md:256–320` (§13) · `:360–405` (§15) |
| run_spec.stage3 writer | `src/fitting.py:1539–1548` (edge sha `:1545`) |
| run_spec.stage3 consumer | `src/io.py:1522–1528` (키) · `:1862–2050` (`_stage3_checks`) · `:1660–1800` (`_stage3_rederive`) · missing-only `:1873` |
| 승인 spec stage3 축 | `tools/preserve.py:6636–6695` (edge sha `:6656`) · index 대조 `:6168–6175` |
| 키별 음성 시험 선례 | `tests/test_gate87_round2b.py:420` (`s03_05`, 5 키) |
| 자기일관 위조 도구 | `tests/test_gate82_residuals.py:33–67` |
| 변이 등록부 | `docs/22p_gap/mutation_replay.py:80` (MUTANTS) · `:2118–2210` (-g87) · `:2381` (MULTI) · `:2824` (DECLARED_MASKED) · `:3045` (`_check`) · `:3227` (EXPECT) · `:6677` (-g87 EXPECT) |
| 상태 3축 lint | `tests/test_docs_lint.py:2342,2639–2665` |
