# GATE93 요청 — 단계 4 (묶음 6) 제한 오프라인 구현 결과 심사 (고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §16) · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`d7a97aa57`** — 92차 판정 대상 (고정 HEAD `248b84e7d` · 91차 코드 `b08bb6944`) 뒤 RUN_SCOPE 를 바꾼 커밋은 이것 하나: `src/io.py` (`_stage3_checks`) + `src/fitting.py` (`_prepare_stage3` 의 edge sha 한 줄 + 같은 함수 import) · +86 −13 · `source_digest` `f0175fff71132003 → c7f48918ff971e91` |
| 검증 HEAD | **`3ec8aadb1`** (clean · 순차 · 동시 시험 없음 · 각 단계 시작 = 끝 HEAD · dirty 0) |
| 사용자 승인 | 원장 §145 (2026-10-06) "단계 4 (묶음 6) 의 제한 오프라인 구현을 고정 표 §16 의 범위로 승인 … 기존 위치 변이 39 는 이월 … 허용 함수 밖 결함은 기록하고 멈추세요" · 원장 §146 "다 승인" (§16-5 의 `-k` 확장 둘 포함) |
| 판정 요청 | (1) §16-3 의 두 닫힘 대상 (`run_spec.stage3` · `candidate_map.json`) 이 닫힌 키 집합 + 자료형 + 구조화된 이유로 구현됐고, 실패한 객체가 재유도에 넘어가지 않는가 (G92-N2) (2) 사본 9 키 대조가 helper 투영 6 + env 직접 3 으로만 되고 기존 재계산 키 5 는 비교하지 않는가 (G92-N3 · §16-2 b′) (3) `provider_edges_sha256` 정의가 하나인가 (k07) (4) 키별 음성 증거 (매트릭스 "보강" 행) · 변이 `-g92` · `-k` 확장 둘 · 영수증 · 전체 회귀 · 재생 |
| 아님 | 실행 GO · 새 연구 leg · claim 게시 · 기존 위치 변이 39 (이월 §16-6) · C8 재개 경로 · C7 envelope ↔ 원장 결속 · 제외 3 · 묶음 6 전체 종결 선언 · lock 재생성 · 설치 |

92차 요청 (`37e3b5c46`) 과 이 요청 사이의 RUN_SCOPE 밖 커밋: 92차 회신 보존 · 고정 표 §16 (`9cc97ec0f`) · 승인 기록 (`4bbcc1769`) · RED (`7e5bdd9e9`) · 변이 (`5768b7f8f`) ·
영수증 history (`683503225`) · 재생성 (`7fea9cdb7`) · 승인 · 원장 앵커 · 계약 (`7ae871687` · `3ec8aadb1`) · 증거 (`2ab61069b`) · 게이트 차수 밖 REIL · COMSOL · 논문 후속 기록 다수 (`bms-balancing/` · `followups/`).

## §1 고정 표 §16 ↔ 구현 (좌표 = `d7a97aa57`)

| §16 자리 | 구현 | 회귀 node |
|---|---|---|
| 16-3 `run_spec.stage3` 닫힘 + 자료형 | `src/io.py:1876–1891` — 키 16 정확 (누락 · 추가) · 자료형 표 (`*_sha256` · `planned_id` · `bank_version` · `arm` · `stage` · `candidate_mode` = str · `planned_envelope` · `pairing_design` · `budget_by_objective` · `warm_provider_map` = dict · `base_config_closure_keys` = list · `type(v) is t` — bool ≠ int · null 없음) · 컨테이너 비-dict = 이유 "dict 가 아니다" · 실패 = 그 자리에서 반환 (아래 재유도 없음) | k03 × 12 (구 필드 2 · 제3 키 · 누락 · 컨테이너 3 · 자료형 5) |
| 16-3 `candidate_map.json` 최상위 · 항목 | `src/io.py:1957–2001` — 최상위 `{schema, entries}` · schema 값 · entries = list · 항목 7 키 · str 5 · `i` int (bool 아님) · `bank_index` = random 이면 int (bool 아님) · 그 밖 null · 이유에 키 이름 · `entries[n]` 위치 · 실패하면 `ok_map=False` → 재유도 미호출 (기존 분기) | k04 × 19 |
| 16-3 실패 envelope 의 재유도 차단 | `src/io.py:2021–2026` — `check_planned_envelope` 실패 (`ebad`) 면 재유도 · 실현 재계산 · 예산 · 관측 roster 를 부르지 않고 **실패로** 남긴다 | k04_env |
| 16-2 b · b′ 사본 9 키 | `src/io.py:1903–1917` 새 검사 `stage3_축_유도` — `stage3_axis_from_envelope(env)` 의 6 키 + `bank.version` · `stages[0].budget_by_objective` · `.warm_provider_map` · PreserveError 도 실패로 · 이유에 키 이름 · 기존 재계산 키 5 비교 안 함 | k05 × 9 (`_only` — 실패 검사가 정확히 이것 하나) |
| 16-2 c k07 | `src/fitting.py:1546` `digest(env["provider_edges"])` (json.dumps 식 삭제) | k07 (warm 계획) · k00 (warm 실행 정상) |
| 기존 재계산 키의 첫 s3 단독 node | 코드 변경 없음 | k06 × 5 (planned_id · pairing_design_sha256 · exact_bounds_sha256 · closure sha · keys — 각각 자기 검사 하나만) |
| 매트릭스 "보강" 대조 | 코드 변경 없음 | k00 · k01 · k02 × 28 · k08 × 8 · k09 (C1 10 · C2 9 · C4 2 · C11 12) · k10 (C5 5 · C8 2) · k11 × 5 · k12 × 8 |

## §2 RED → GREEN (증거 00 · 커밋 메시지)

RED (`7e5bdd9e9` 의 시험 파일): 138 node · **41 failed** = k03 11 · k04 20 · k05 9 · k07 1 — 결함 증거로 세지 않는 예외 RED 5 를 따로 센다 (AttributeError 4: `io.py` candidate_map 읽기의 `cm.get` × 3 · 재유도의 `m.get` × 1 · WireError 1: bool `bank_index` 가 numpy 색인으로) · **97 passed** = 대조 node 전부 + k03[missing_arm] (기존 검사가 이미 이름까지 냄).
RED 전 시험 수정 1: k12 의 `warm_provider_objective` · `restart_row` 는 `실현_재계산` 도 독립적으로 센다 → 실패 검사 집합을 `also` 로 고정 단언 (가림이 아니라 두 독립 검사).
GREEN (`d7a97aa57`): 새 파일 138 passed · G81/G82/G84/G85/G87/G88/G89 179 passed. 허용 함수 밖 수정 0 · 허용 함수 밖 결함의 RED 0.

## §3 변이 (증거 03 · 04 · 05)

| 변이 (`-g92`) | 위치 | 죽인 node |
|---|---|---|
| `stage3-run-spec-keys-are-closed-g92` | `if missing or extra` → `if missing` | k03 구 필드 2 · 제3 키 (3) |
| `stage3-run-spec-values-are-typed-g92` | 자료형 줄 → `if False` | k03 자료형 5 |
| `candidate-map-keys-are-closed-g92` | 닫힘 · 자료형 결과 폐기 (옛 읽기) | k04 19 |
| `failed-envelope-is-not-rederived-g92` | `if ebad:` → `if False:` | k04_env |
| `stage3-run-spec-is-derived-per-key-g92` | 사본 대조 루프 → `if False` (투영 · env 직접 한 루프) | k05 9 |
| `provider-edges-sha-has-one-definition-g92` | writer 를 옛 json.dumps 식으로 | k07 |
| `validator-planned-id-is-the-envelope-digest-g92` · `…pairing-design-sha-is-recomputed-g92` · `…exact-bounds-sha-is-recomputed-g92` | k06 첫 증인 위치 3 (`io.py` planned_id · 설계 3 자 · bounds 3 자) | k06 각 1 |

`--check-preimages`: 모든 변이 지점이 정확히 한 번. 처음 EXPECT 대조에서 k07 증인이 실행마다 다른 digest 를 담아 불일치 → 시험 메시지에서 digest 를 빼고 EXPECT 증인을 고정
문장으로 (증거 04a → 04b · G67-T1-b). `-k` 확장 둘 (§16-5 · 사용자 승인): `stage3-axis-is-derived-not-copied-g87` = `s03_05 or test_g92_k08` (13 node) ·
`claim-seals-the-run-spec` = `claim_seals_the_exact_run_spec or test_g92_k10_c8_another` (2 node) — 증인은 기존과 같은 `Failed: DID NOT RAISE PreserveError` (이유 변경 없음 · 좌표 이동 없음).
**기존 위치 변이 39 는 이월** (§16-6 · 데이터 음성 node 만).

## §4 영수증 (증거 06 · 08)

history `683503225` (두 leg · validator `f0175fff71132003` · 현행본 바이트 그대로) → clean `683503225` 에서 1 회 재생성 `7fea9cdb7` (rc 0) — paired 검사 **35** · core `d527cde9…` ·
grid 검사 **34** · core `8de4e4af…` (35 / 34 불변 — §16-5 의 기대). core diff = `core_sha256` · `validator_source_digest` · `src_io_sha256` 뿐. 원장 `LEG_PRESERVATION.yaml` 앵커 2 × 2 는
**재생성 커밋에서 빠뜨렸다가** 1 차 전체 회귀의 docs-lint F 3 로 드러나 `7ae871687` 에서 갱신 (`make_receipt.py --check` 두 leg core 바이트 동일 · 원장 §146).
stamp 의 환경 프로필 C = **MISMATCH 34** (판 13 · RECORD 16 · lock 밖 배포판 4 · 가려진 1 — 이 컨테이너 이미지 (설치 2026-09-14) 가 91차 컨테이너와 다르다 · lock `d886f30f…` 그대로 ·
기록 전용 — C1 경계대로 pytest · smoke · 영수증을 막지 않음). lock 재생성 · 설치는 범위 밖.

## §5 전체 회귀 · smoke · 등록부 전체 재생 (clean `3ec8aadb1` · 순차 · 동시 실행 없음 · 각 단계 시작 = 끝 HEAD · dirty 0)

| 항목 | 결과 | 증거 |
|---|---|---|
| 환경 프로필 C (`--json`) | MISMATCH 34 · rc 0 · 170 locked / 174 measured · 가려진 2 / 3 · 설치 파일 일치 24,918 (해시 없음 10,456) · `path_origins_in_record` 9 · `not_measured` [`loaded_module_origin`] | 08 |
| 전체 `pytest tests/ -q -rfEx` | **2320 passed / 1 xfailed / rc 0** (1:18:04 · 13:51:34Z → 15:09:42Z) · xfail 은 이전과 같은 선언 항목 · 2320 = 91차 2182 + 이 라운드 새 138 | 10 |
| `./scripts/smoke_e2e.sh` | **rc 0** (15:09:42Z → 15:13:26Z) | 11 |
| 등록부 전체 재생 (`-k` 없음) | **421 / 421 call 단계에서 선언한 이유로 물었다 · rc 0** — scenario 432 (executable 421 · declared 11) · site 470 (executable 459) · ★ 0 · 15:13:26Z → 18:42:28Z (3:29:02) · 91차 412 + `-g92` 9 | 12 |

중단한 두 실행 (보존 · `aborted/`): 1 차 (`7fea9cdb7`) docs-lint F 4 = 원장 앵커 3 + 계약 줄 인용 1 · 2 차 (`7ae871687`) F 1 = 계약 줄 인용 둘째 줄 (`src/fitting.py:2066 → 2067` —
GREEN 의 주석 한 줄로 밀림). 둘 다 고친 뒤 3 차가 위 결과다.

## §6 자체 신고

a. **원장 앵커 갱신 누락** — 91차 `f27006370` 은 재생성 커밋에 앵커를 함께 넣었는데 이번엔 빠뜨렸다. docs-lint 가 잡았다 (§4).
b. **계약 문서 수정 두 곳이 §13.1 밖** — 줄 인용 `src/fitting.py:2116 → 2117` · `2066 → 2067` (의미 변경 없음 · GREEN 의 주석 한 줄 · docs-lint 강제). §13.1 묶음 6 행은 "제출 · 닫힘 아님".
c. **k07 증인 비결정성** — 첫 시험 메시지가 provider fits 바이트에서 나온 digest 를 담았다 (실행마다 다름). 메시지에서 digest 를 뺐다 — 단언 자체는 그대로.
d. **차단 범위** — 실패한 envelope (`ebad`) 이면 재유도뿐 아니라 실현 재계산 · 예산 · 관측 roster 도 부르지 않는다 (네 검사 모두 실패로 남김 · 그 뒤 base_config_결속 은 평가하지 않음 — 기존 조기 반환 분기와 같은 꼴). `planned_id` 만 어긋난 유효 envelope 은 차단하지 않는다 (k06[planned_id] — 실패 검사가 `stage3_planned_envelope` 하나).
e. **환경 프로필 C MISMATCH** — 컨테이너가 바뀐 결과이고 이번 diff 와 무관 (lock 은 91차 그대로). `numpy` 는 판이 같고 RECORD 해시가 다르다 (dist_record).
f. **이월** — 기존 위치 변이 39 · C8 재개 경로 (`preserve.py:4192`) · C7 envelope ↔ 원장 결속 · 제외 3 — 묶음 6 전체 종결을 선언하지 않는다.
