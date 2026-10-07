# GATE94 요청 — 93차 잔여 두 건 (G93-N1 코드 차단 · G93-N2 당시 원 로그) 로 한정한 재검토 · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`0ab2924f4`** — 93차 판정 대상 코드 `d7a97aa57` 뒤 RUN_SCOPE 를 바꾼 커밋은 이것 하나: `src/io.py` (`_stage3_checks`) 두 곳 · source_digest `044e4f5513011a9b` (이전 `c7f48918ff971e91`) |
| 검증 HEAD | **`168fd41a5`** (env 프로필 · smoke · 전체 재생) · **`fe72f9b81`** (전체 pytest — 위키 raw 정정 1 파일 뒤) · 모두 clean · 순차 · 동시 시험 없음 · 각 단계 시작 = 끝 HEAD · dirty 0 |
| 사용자 승인 | 원장 §149 (2026-10-07) "둘다 진행" — §148 의 제안 범위 그대로 (역사 reader 불변 · planned_id 단독 불일치 의미 유지 · 정상 v4 불변) |
| 판정 요청 | (1) 유효한 planned-leg/v3 envelope (sig6) 가 v6 재유도에 넘어가지 않고 구조화된 실패로 남는가 · 정상 v4 와 planned_id 단독 불일치의 기존 의미가 유지되는가 (G93-N1) (2) 93차 증거의 당시 원 로그가 파일별 크기 · 전체 SHA · 실행 상태와 함께 인계됐는가 (G93-N2 · 재실행 0) |
| 아님 | 실행 GO · 새 연구 leg · 묶음 6 전체 종결 · 39 위치 변이 · C8 재개 · C7 원장 결속 · 제외 세 객체 (93차 이월 그대로) |

93차 요청 (`0e3c244ea`) 과 이 요청 사이의 RUN_SCOPE 밖 커밋: 원 로그 강제 추가 (`e0e9f213d`) · 93차 회신 보존 (`095c31ac5` 규칙 · `93e8943ac` 묶음) · 원장 §148 · N2 보충 (`217230fe2`) ·
승인 §149 (`3a7d68069`) · 영수증 history (`27b0917e2`) · 재생성 · 앵커 (`49c769cb5`) · COMSOL §70 초안 (`168fd41a5`) · 위키 raw 정정 (`fe72f9b81`) · 증거 규칙 (`da7ab3f42`) · 증거 (`016e970f6`) · 게이트 차수 밖 논문 후속 · 위키 기록.

## §1 G93-N1 — 차단 조건 (좌표 = `0ab2924f4`)

| 자리 | 변경 | 회귀 node |
|---|---|---|
| `src/io.py` `_stage3_checks` 축 유도 | `stage3_axis_from_envelope(env)` 의 PreserveError 문구를 `ax_err` 로도 보관 (`stage3_축_유도` 실패 이유는 그대로) | — |
| `src/io.py` `_stage3_checks` 재유도 차단 | `if ebad:` → `v4_bad = list(ebad) + ([ax_err] if ax_err is not None else [])` · `if v4_bad:` — 같은 4 키 (후보_재유도 · 실현_재계산 · restart_예산_완주 · 관측_roster_재구성) 실패 · 조기 반환. 이유 문구 "planned_envelope 가 유효한 planned-leg/v4 가 아니어서 다시 유도 · 재계산하지 않는다: …" | `test_g93_n1` |
| v4 schema + 구조 판정 | 새 판정 없음 — 기존 helper `stage3_axis_from_envelope` 가 `schema == planned-leg/v4` + `check_envelope_v4` 를 이미 본다 (중복 schema 검사를 넣었다가 GREEN 뒤 helper 재사용으로 줄임 · 증거 01 → 02) | — |
| 역사 reader | `check_planned_envelope` 불변 (v3 / v4 분기 그대로) | 기존 시험 |
| 기존 의미 | 정상 v4 → 통과 · 재유도 호출 / planned_id 단독 불일치 → `stage3_planned_envelope` 만 실패 · 재유도 그대로 (v4 경계 문구 없음) | `test_g93_c1` · `test_g93_c2` |

## §2 RED → GREEN

- 증거 00 (`gate94_evidence/00_red_test_g93_1failed_keyerror_io1686.log`): 수정 전 `test_g93_n1` — `src/io.py:1686: KeyError: 'parameter_order_sha256'` (93차 회신이 정적으로 짚은 경로 그대로) · c1 · c2 통과 (기존 의미 고정 시험이라 수정 전에도 통과가 정상).
  fixture: base v6 실물 산출의 envelope 를 같은 이름의 값 (leg_id · 세대 · **설계 SHA** · source_digest · 정렬 objectives · 예산 합 · candidate_mode · min_retention_days) 으로 유효 v3 로 바꾸고
  (`check_planned_envelope(v3) == []` 를 fixture 안에서 단언) planned_id · record · run_signature 를 다시 맞춘다 — 실제 `validate_provenance` 경로 · `_stage3_rederive` spy.
- 증거 01 · 02: GREEN — 새 시험 3 + stage3 모듈 4 (`test_gate92_stage4_linkage` · `test_gate81_stage3_wire` · `test_gate82_residuals`) 204 passed (중복 schema 검사 제거 전 · 후 각 1 회).

## §3 변이 (증거 03 · 04)

| 변이 | 바꾸는 것 | 기대 실패 (증인) |
|---|---|---|
| `v6-rederive-gate-includes-axis-failure-g93` (신규) | `v4_bad = list(ebad)` (92차 판본) | `test_g93_n1` — `KeyError: 'parameter_order_sha256'` (결정적) |
| `failed-envelope-is-not-rederived-g92` (원문만 갱신) | `if v4_bad:` → `if False:` (조건 이름 ebad → v4_bad) | `test_g92_k04_env` (기존 증인 그대로) |

## §4 영수증 (증거 06)

history 먼저 (`27b0917e2` — 두 leg 현행본 · validator `c7f48918ff971e91` · 바이트 그대로) → `make_receipt.py` leg 별 1 회 (clean `27b0917e2`) → 원장 앵커 갱신 (`49c769cb5`).
paired_fixed5_v4 검사 35 · core `68a74c60…` / grid_fit_v5 검사 34 · core `16d3be25…` · `--check` 두 leg core 바이트 동일. diff 는 validator identity (`validator_source_digest` · `src_io_sha256` · commit · 시각 · 플랫폼) 뿐.
플랫폼 문자열 `fc-v70 → fc-v77` 은 세션 컨테이너 교체이고 정본 환경 일치 주장이 아니다.

## §5 전체 회귀 · smoke · 등록부 전체 재생 (clean · 순차 · 증거 `gate94_evidence/`)

| 단계 | HEAD | 결과 | 증거 |
|---|---|---|---|
| env 프로필 (C) | `168fd41a5` | rc 0 · MISMATCH 기록 그대로 (컨테이너 이미지 차 · 정본 환경 일치 주장 아님) | 08 |
| 전체 pytest (1 차) | `168fd41a5` | **1 failed** · 2322 passed · 1 xfailed — `test_docs_lint.py::test_wiki_tools_survive_a_cp949_console[lint.py]` (위키 raw 2026-10-07 브리핑의 sha256 선언 오류 · 코드 무관) | 10a |
| 위키 정정 | `fe72f9b81` | 선언을 위키 규칙 (frontmatter 뒤 본문 전체) 대로 · wiki lint 0 errors · 실패 node 2 / 2 통과 | 커밋 |
| **전체 pytest (2 차)** | **`fe72f9b81`** | **2323 passed · 1 xfailed · rc 0** (1:38:55) | 10b |
| strict smoke | `168fd41a5` | rc 0 | 11 |
| **등록부 전체 재생** | `168fd41a5` | **scenario 433 · executable 422 · declared 11 · ran 422 · 422 / 422 call 단계에서 물었다 · rc 0** | 12 |

`168fd41a5` ↔ `fe72f9b81` 차이는 `wiki/raw/articles/2026-10-07-github-research-briefing.md` 하나 — smoke · 재생은 위키를 읽지 않아 다시 돌리지 않았다.

- 중단 1 회 (보존): 1 차 시작 `49c769cb5` 01:02:55Z — pytest 34 % 에서 컨테이너 재시작으로 프로세스 소멸 (rc 줄 없음) → `aborted/run1_*`. 재시작 HEAD 는 COMSOL 초안 커밋 `168fd41a5` (RUN_SCOPE 밖 · `degradation-degeneracy/` 차이 0).

## §6 G93-N2 — 당시 원 로그 (재실행 0)

- 93차 관측 그대로: 요청 커밋 `0e3c244ea` 의 `gate93_evidence/` 에는 README 만 있었다 — `*.log` gitignore 로 `2ab61069b` 의 `git add` 가 조용히 건너뜀. 원 로그 14 는 요청 뒤 `e0e9f213d` 에 `-f` 로 추가.
- 첨부: `docs/22p_gap/gate93_n2_supplement/GATE93_N2_ORIGINAL_LOGS.zip` (128,409 B · sha256 `b76e663dcf9fba7ce18a0381e01b1777ad7e594d341d42a74376669d37c3f7c6`) + `GATE93_N2_LOG_MANIFEST.json`
  (11,913 B · `b2ee0d56a10be75c16dcd81fd23d65c4f1814ef6426b3fddabb37e08ec577620`) — 14 로그 = `e0e9f213d` blob 바이트 · 당시 스크래치 원본과 14 / 14 sha256 동일 · 원본 수정 시각 12:30:38Z – 19:17:57Z (모두 요청 커밋 전) ·
  파일별 `status_lines` (로그 자체의 rc · 시작 / 끝 HEAD · dirty · 요약 줄).
- 이번 라운드 증거 (`gate94_evidence/` · 로그 15 + README) 는 `git add -f` 로 넣었고 증거 커밋 `016e970f6` tree 에 16 파일이 있다 (`git ls-tree` · 발송문에 요청 커밋 기준 출력).

## §7 자체 신고

a. 수정 전 GREEN 판본에 schema 중복 검사가 있었다 — helper 가 이미 같은 판정을 해 GREEN 뒤 줄였다 (증거 01 → 02 · 같은 결과).
b. 이유 문구가 바뀌었다 ("유효하지 않아" → "유효한 planned-leg/v4 가 아니어서") — 저장소 안 다른 참조 0 (grep) · 변이 증인은 시험 메시지라 영향 없음.
c. 1 차 검증이 컨테이너 재시작으로 끊겼다 (§5) — 원 로그 보존 · 처음부터 다시.
d. 플랫폼 문자열 변화 (§4) — 기록만.
e. 1 차 전체 pytest 의 1 실패는 이 라운드 밖 위키 기록 (2026-10-07 브리핑 raw) 의 sha256 선언 오류였다 — 커밋 전에 wiki lint 를 돌리지 않았다. 정정 뒤 전체 pytest 를 다시 돌렸고 (§5), smoke · 재생은 다시 돌리지 않았다 (근거 §5 끝 줄).
f. 중단 로그 보존 중 원 로그 끝에 메모 한 줄을 덧붙였다가 원래 크기 (1,555 B) 로 잘라 되돌렸다 — 원 바이트는 그 앞부분 그대로이고 메모는 `aborted/README.txt` 에 따로 있다.
g. 증거 로그 16 파일이 증거 커밋 `016e970f6` 의 tree 에 있음을 `git ls-tree` 로 확인했다 (발송문에 요청 커밋 기준 확인 출력을 붙인다).
