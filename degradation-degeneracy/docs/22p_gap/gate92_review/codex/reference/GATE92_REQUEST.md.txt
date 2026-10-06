# 92차 게이트 리뷰 요청 — 단계 4 (묶음 6) **범위 · 사전 고정 사항 확인** (구현 착수 아님 · 실행 GO 아님)

> 이 문서는 리뷰 요청문이다. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요. 리뷰어는 exact HEAD 를 fetch 해 검증한다.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 코드 | 91차 판정 코드 `b08bb6944` 그대로 — **이 요청은 RUN_SCOPE 를 바꾸지 않는다** (`source_digest` `f0175fff71132003` · `b08bb6944` → 요청문 커밋의 RUN_SCOPE diff 0). 요청문 커밋 · 발송 SHA 는 발송문에 실측 |
| 선행 판정 | 91차 (원장 §140): G90-N1 · C1 종결 · 환경 프로필 C 기록 대조 라운드 종결 · 열린 라운드 0. 그 전 단계 3: 라운드 1 (83차 · "단계 3 전체 완료는 아님") · 2a (86차) · 2b (89차) 종결 |
| 사용자 결정 | 2026-10-06 "게이트도 같이 진행" (원장 §141 — 단계 4 착수 · 범위 조사) → "게이트는 권고대로 부탁해요" (원장 §142 — 조사 문서 §6 Q1–Q9 를 제안대로 채택 · 첫 라운드는 범위 확인부터) |
| 범위 조사 원문 | `docs/22p_gap/STAGE4_SCOPE_RESEARCH_20261006.md` (【사실】 = 파일:줄 확인 · 【관찰】 = 정적 읽기만 · RED 미실행 · 【제안】 구분) |
| 단계 4 정의 | `GATE78_REQUEST.md` §3.2 단계 4: "묶음 6: 신규 writer 의 구 필드 (`pairing_design_id` · `inference_status`) 제거 + consumer 별 per-key linkage 음성 변이. v5/v6_prep read-only dispatch · 과거 봉인 유지" · 77차 리뷰 `gate77_review/codex/REVIEW_KO.md:92` "신규 writer 구필드 제거와 consumer 별 linkage 음성 시험" · 계약 `STAGE3_CONTRACT.md:828` "per-key linkage mutation test" |

## §0 묻는 것 / 묻지 않는 것

| 묻는 것 | 묻지 않는 것 |
|---|---|
| §1 의 코드 사실 · 관찰이 맞는가 (특히 "구 필드는 지울 코드가 없다" 와 열린 키 집합 둘) | 구현 착수 (회신 뒤 사용자 별도 승인) |
| §2 범위 · 생산 파일 경계 · 고정 결정 a–g 가 단계 4 의 뜻에 맞는가 | 실행 GO · 새 연구 leg · floor · pilot · provider 운영 canary |
| §3 질문 Q1–Q9 의 우리 답 (사용자가 채택한 제안) 에 대한 의견 · 특히 Q1 · Q2 · Q3 · Q5 | claim 세대 게시 · 세대표 등록 · p_ini · adaptive · class/투영 · requirements |

## §1 코드 사실 · 관찰 (좌표는 HEAD 에서 다시 확인 · RUN_SCOPE 는 `b08bb6944` 와 같음)

| # | 내용 | 좌표 | 성격 |
|---|---|---|---|
| F1 | `pairing_design_id` · `inference_status` 는 `src/ tools/ scripts/ configs/ run.sh tests/ docs/22p_gap/*.py` · 산출 디렉터리에 **0 건**이다. `git log -S` 로도 RUN_SCOPE · tests 에 들어간 적이 없다 (`inference_status` 는 yaml 주석으로 `0ca48cbf3` 에 들어와 `d405d1b85` 에서 빠짐). 남은 곳은 문서 (계약 `:164,220,252,496,593,611,633,828` · 옛 요청문 · 원장) 뿐 | 조사 문서 §3.1 | 사실 |
| F2 | 그래서 "신규 writer 에서 제거" 는 지울 코드가 없는 상태다 — 실제 일은 (A) **부재를 닫힌 키 검사와 음성 시험으로 고정** (B) consumer 별 per-key linkage 음성 | 조사 문서 §0 | 사실 → 해석 |
| F3 | 구 이름의 현행 정본: `pairing_design_id` → `pairing_design_sha256` (+ hash 밖 `design_label`) · `inference_status` → `preservation_status` · `validation_status` · `inference_role` (계약 §8 `:501–505`) | 조사 문서 §3.2 | 사실 |
| F4 | v6 산출 중 닫힌 키 집합: 설계 spec · `planned-leg/v4` envelope · v3 승인 spec `stage3` 축 · 계획 index 항목 · `stage3_context` · execution record v1/v2 · realized · restart 행 · roster · provider edge (9 자리) | 조사 문서 §3.3 | 사실 |
| F5 | **`run_spec.stage3` 은 열린 집합** — `src/io.py:1873` 은 `_STAGE3_SPEC_KEYS` 중 **빠진 키만** 본다. 16 키 중 validator 가 계획 · 재계산과 대조하는 키는 7 개 (`planned_id` · `planned_envelope` · `pairing_design` · `pairing_design_sha256` · `exact_bounds_sha256` · `base_config_closure_sha256` · `_keys`) · 나머지 9 개 (`parameter_order_sha256` · `bank_version` · `candidate_mode` · `budget_by_objective` · `warm_provider_map` · `provider_edges_sha256` · `roster_sha256` · `arm` · `stage`) 는 있는지만 본다 | `src/io.py:1522–1528` · `:1862–2050` · `:1873` | 관찰 (RED 미실행) |
| F6 | `candidate_map.json` 최상위 · 항목도 열림 — `schema` · `entries` 와 record digest 만 본다 | `src/io.py:1927–1931` | 관찰 |
| F7 | **`provider_edges_sha256` 의 정의가 둘**: run_spec 쪽 `hashlib.sha256(json.dumps(env["provider_edges"], sort_keys=True))` (`src/fitting.py:1545`) ↔ 승인 spec 쪽 `digest(env["provider_edges"])` (`tools/preserve.py:6656`). 빈 목록이면 같고 edge 가 있으면 다르다 (조사 중 메모리 계산 한 번 — 시험 아님) | 위 좌표 | 사실 (정의) · 값 차이는 관찰 |
| F8 | 9 키의 사본을 run_spec 에서 읽는 다른 consumer 는 찾지 못했다 (지금은 "읽는 이 없는 사본") — 위험은 뒤에 생길 consumer 가 이 사본을 정본으로 믿는 경우 | 조사 문서 §3.4 | 관찰 |
| F9 | 계획 index 의 승인 spec 대조 (`tools/preserve.py:6168–6175`) 는 dict 전체 비교라 9 키 모두 대조된다 — 다만 키별 음성 node 는 `tests/test_gate87_round2b.py:420` `s03_05` 의 5 키뿐 | 위 좌표 | 사실 |

## §2 범위 · 경계 · 고정 결정 (안 — 회신 뒤 `STAGE3_IMPL_ROUND1_SPEC.md` §16 으로 고정)

| 항목 | 내용 |
|---|---|
| 범위 | (A) 구 필드 **부재 고정** — v6 writer 산출에 두 이름이 없고 v6 consumer 가 그 키를 거부 · (B) **consumer 별 per-key linkage 음성** — linkage 키마다 그 키를 읽는 consumer 마다 "그 키 하나만 어긋난 자기일관 위조" 를 거부 · (C) **`provider_edges_sha256` 두 벌 정의 제거** |
| 생산 파일 상한 | `src/io.py` (`_stage3_checks` 의 s3 닫힘 · 키별 대조 — **sig 6 분기 안에서만**) · `src/fitting.py` (run_spec.stage3 블록 · 두 벌 제거) · `tools/preserve.py` (재사용 helper 노출이 필요할 때만). `run.sh` · `scripts/` · `configs/` · `requirements*` · `src/grid.py` · `tools/design_wire.py` 는 손대지 않음 — 필요해지면 멈추고 묻는다 |
| 함께 | 새 시험 파일 (RED 먼저 · node `k00`–) · `docs/22p_gap/mutation_replay.py` (`-g92` 이후 차수 태그) · 계약 §13.1 **묶음 6 행만** 갱신 (닫힘 판정은 리뷰가 함) · 영수증 history 보존 → 두 leg 1 회 · 전체 회귀 · smoke · 등록부 전체 재생 |
| 하지 않음 | v5 (sig 5) 검사 · `run_spec` 최상위 닫힘 (v5 공통 경로) · `planned-leg/v3` · v2 spec · 과거 manifest / fits / receipt 바이트 · `row_projection.py` · golden · 세대표 등록 · claim 세대 게시 · 운영 원장 v6 계획 · p_ini · adaptive · 실행 GO · 새 연구 leg · class/투영 · requirements |

| # | 고정 결정 (안) | 근거 |
|---|---|---|
| a | 부재는 **닫힌 집합**으로 증명한다 — 두 이름 전용 deny-list 를 만들지 않는다 (이름 하나만 막으면 같은 뜻의 세 번째 이름이 열린다). 이미 닫힌 9 자리 (F4) 는 음성 node 만 더하고, 열린 자리 중 **v6 전용**인 `run_spec.stage3` 와 `candidate_map.json` (최상위 `{schema, entries}` · 항목 `{cond_id, objective, i, source, candidate_id, bank_index, x0_sha256}`) 을 sig 6 분기 안에서 닫는다 | 기존 닫힘 관행 재사용 · 81차 N2 "새 version validator: 키 삭제 / 세대 혼입 / 타입 불일치 거부" |
| b | `run_spec.stage3` 의 계획 유래 키는 **envelope 에서 다시 유도한 값과 키별로 같아야** 한다 (Q5 = 대조). 유도 함수는 하나 — `tools/preserve.py::stage3_axis_from_envelope` 재사용 · 그 함수에 없는 키 (`bank_version` · `budget_by_objective` · `warm_provider_map` · `exact_bounds_sha256`) 는 env 의 자리와 직접 비교 · 불일치 이유는 **키 이름을 담는다** | 87차 §13-2 c "유도 하나 · 두 벌 금지" 를 run_spec 쪽에도 |
| c | `provider_edges_sha256` 정의는 `digest(env["provider_edges"])` (canonical) **하나** (Q4). `fitting.py:1545` 의 `json.dumps` 식은 지운다 — 바뀌는 것은 v6 run_spec 바이트뿐이고 실물 v6 leg 가 0 이라 과거 봉인 영향 0 (smoke · 시험 fixture 는 다시 생성) | F7 |
| d | 사본 9 키를 지우는 대안 (b′) 은 채택하지 않는다 — v6 run_spec schema 변경이 "구 필드 제거" 와 섞여 범위가 흐려진다 | Q5 |
| e | v5 · v6_prep 경로 **바이트 · 판정 불변** — sig 5 `validate_provenance` 검사 집합 · `normalize_restart_record(declared=None / legacy / v6_prep_logging)` · `g79_06` · `g79_02` 골든 · s00 v5 spec digest · 운영 원장 `planned_index()` 결과 | 77차 `:92` · 78차 §3.2 · 81차 N2 |
| f | per-key 음성은 consumer 마다 **그 consumer 의 실제 호출 경로**에서 잰다. 위조는 자기일관 (서명 · fits 봉인 · record digest · planned_id 를 다시 맞춘 뒤 **그 키 하나만** 어긋나게) — 기존 `test_gate82_residuals.py::_forge_stage3` · `_reseal_fits` · `_rewrite_record` 재사용 · run_signature 재서명 helper 만 새로 | 82 · 85 · 89차 반례 모델 |
| g | 계약 §13.1 은 묶음 6 행만 ("미착수" → 제출 증거 링크 · "닫힘" 은 쓰지 않음). 다른 행의 77차 권고 반영은 별도 문서 정정 (Q6) | 25차 "닫힘 판정은 리뷰가 한다" |

**회귀 계획 (RED 먼저):** k00 정상 v6 · v5 대조 (GREEN 골든) · k01 부재 재귀 확인 (처음부터 GREEN 정상) · k02 닫힌 9 자리에 구 필드 → 거부 (대조) · **k03** run_spec.stage3 에 구 필드 + 재서명 → 거부 · **k04** candidate_map 에 구 필드 + digest 재계산 → 거부 · **k05** 9 키 각각 형식상 유효한 다른 값 + 재서명 → 거부 · 이유에 키 이름 · k06 이미 대조되는 5 키 키별 (대조) · **k07** warm edge 계획에서 run_spec 의 edge sha == 승인 spec 축 값 · k08 계획 index 키별 보강 (`pairing_design_sha256` · `parameter_order_sha256` · `bank` 하위 · `stage`) · k09 consumer 경로별 (진입점 · provider map · record). **결함 증거로 세는 것은 k03 · k04 · k05 · k07 뿐** — 나머지는 처음부터 GREEN 인 대조 (81차 §7-4 · 83차). 새 helper 부재 · `AttributeError` 로 떨어진 node 는 따로 센다.

**변이 (`-g92` 이후 차수 태그):** run_spec.stage3 닫힘 끄기 (k03) · candidate map 닫힘 끄기 (k04) · 키별 유도 대조 루프 끄기 (k05 ×9) · env 직접 대조 4 키 끄기 (같은 자리면 하나로 합치고 독립 커버리지로 세지 않음) · 옛 `json.dumps` 식으로 되돌리기 (k07). 기존 `-g81` · `-g82` · `-g84` 증인이 바뀌면 멈추고 보고 · 갱신은 `--emit-expect` 관측값만.

**영수증:** `src/io.py` 가 바뀌어 validator identity 가 움직인다 → 현행 영수증 (`f0175fff71132003` 세대) history 보존 → `paired_fixed5_v4` · `grid_fit_v5` 각 1 회 (v5 leg 이므로 **검사 집합 35 / 34 불변**이 기대값 · 바뀌면 멈춤).

## §3 질문 — 사용자가 채택한 답 (리뷰어 의견 요청)

| # | 질문 | 채택한 답 (조사 문서 §6 의 제안 그대로) |
|---|---|---|
| Q1 | 단계 4 에 "claim 세대 게시" 가 드는가 (81차 `:60,129` 는 단계 4 에 붙였고 2b §13-5 는 실물 v6 leg 뒤에만 등록) | **넣지 않는다** — 실행 GO 뒤 별도 게이트 |
| Q2 | 필수 증거가 음성 **시험** (77차) · 음성 **변이** (78차 표) · mutation test (계약) 중 무엇인가 | **둘 다** — 키별 데이터 음성 node (k05 · k08) + 비교 자리마다 코드 변이 하나. "키 수만큼 코드 변이" 는 요구하지 않는 것으로 확인 요청 |
| Q3 | 단계 3 을 단계 4 착수 조건으로 "충족" 으로 봐도 되는가 (83차 "전체 완료 아님" 뒤 전체 완료 판정 문장 없음 · 라운드 1 · 2a · 2b 종결 · 명시적으로 미룬 항목: p_ini · adaptive · 실물 v6 leg · 세대표 · 운영 원장 v6 계획 · `--mode all` / grid v6) | **리뷰 승인 범위 기준 충족으로 보고 착수** — 이 요청에서 한 줄 확인을 받는다 |
| Q4 | `provider_edges_sha256` 두 벌을 이번에 하나로 고치나 | **고친다** (결정 c) |
| Q5 | 사본 9 키 — 대조 (b) 인가 삭제 (b′) 인가 | **대조** (결정 b · d) |
| Q6 | 계약 §13.1 — 묶음 6 행만인가 77차 권고 전체인가 | **묶음 6 행만** — 전체 반영은 문서 전용 정정으로 분리 |
| Q7 | 범위 확인 게이트를 먼저 둘 것인가 | **둔다** — 이 92차. 구현은 회신 뒤 사용자 별도 승인 |
| Q8 | 생산 파일 상한에 `src/io.py` 를 넣는가 | **넣는다** — validator 를 고치지 않으면 k03–k05 를 닫을 수 없다 · 영수증 두 leg 1 회 재생성 비용 수용 |
| Q9 | 묶음 6 이 닫히면 묶음 9 의 final gate 선행 ("묶음 6 없이 닫을 수 없다" `:828`) 이 해소되나 | **"선행 하나 충족" 까지만 주장** — 묶음 9 의 남은 "실물 provider 어댑터" (`:831`) 는 별개로 남는다 |

## §4 이 요청이 하지 않는 것

코드 · 시험 · 영수증 · 원장 스키마 변경 0 (문서만 — 이 요청문 · 원장 §141 · §142 · 범위 조사 문서). 실행 GO · 새 연구 leg · floor · pilot · provider canary · class/투영 게시 · 복원 0. 76차 종결 · `grid_fit_v5` 진단 전용 유지. 회신 뒤 구현은 사용자 별도 승인 — 승인 범위 밖 파일이 필요해지면 멈추고 다시 묻는다.

## §5 발송 규칙

70차 §6 그대로. 발송 SHA · 검증 숫자는 발송문에 방금 실행한 출력으로만. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.
