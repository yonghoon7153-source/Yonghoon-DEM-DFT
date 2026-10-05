# GATE91 요청 — G90-N1 정정 결과 (환경 프로필 C 의 origin 축을 경로 검색 범위로 · 이름 · 범위 선언 · 문구 · C1) · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`b08bb6944`** — 90차 판정 대상 `e2160c2ef` 뒤 RUN_SCOPE 를 바꾼 커밋은 이것 하나 (`tools/env_profile.py` 1 파일 · +30 −17). lock · `requirements.txt` · `scripts/smoke_e2e.sh` · `src/` · `run.sh` · `configs/` 불변 (고정 표 §13-2 상한 안). `source_digest` **`3f84c0db52d2b9ac` → `f0175fff71132003`** |
| 사용자 승인 | 원장 §138 (2026-10-05) "B로하자" — 90차 회신 (원장 §137 · G90-N1 P2 · 비차단 C1) 뒤 정정 범위 A (문서만) · **B (도구의 문구 · 이름까지 · RUN_SCOPE 1 파일)** · C (실제 로드 origin 측정) 중 B → 고정 표 `docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` **§13** 을 코드 변경 전 커밋 (`69b35f65d`) |
| 판정 요청 | (1) **G90-N1** — 확인한 것이 "`PathFinder` 경로 검색 origin 의 RECORD 소속" 으로 좁혀졌고 (이름 · docstring · 요약 · stamp), 로드된 module origin 이 **미측정**으로 결과에 스스로 선언되는가 (`not_measured`) · 최소 종결 조건 (1)–(4) (원장 §137) 를 채우는가 (2) **C1** — 기록 전용 (D3) 과 측정 기능 회귀 (e06 · e08) 의 적용 경계 문장 (3) 이름 변경이 판정 논리 · lock · smoke · `make_receipt.py` 를 건드리지 않았는가 (4) 회귀 · 변이 · 영수증 · 전체 회귀 |
| 아님 | 실행 GO · 실제로 로드된 module origin 의 측정 (선택지 C — `sys.modules` · `__spec__` · meta-path 구분 · D guard 라운드의 후보) · D guard · C 의 fail-closed · 설치 · lock 재생성 · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class · 투영 게시 |

90차 요청 (`24f499ba6`) 과 이 요청 사이의 다른 커밋은 모두 RUN_SCOPE 밖이다: 90차 발송 SHA docs-lint 보존 (`4432dfc1a`) · 90차 회신 접수
(`e56630fc9` · `a8ec8f9ed` · `6c15b80f0`) · 게이트 차수 밖 COMSOL §53–§55 (B-min r1 재검토 발송 · 회신 접수 · r2 — `dbc02ebf4` · `f0e384d79` ·
`b7397ed95` · `c92fe24e6` · `b4bb5325a` · `939b544b8`) · 이 라운드의 착수 기록 (`69b35f65d`) · RED (`e06e0cd6d`) · 증거 규칙 (`4b32db749`) · 증거 (`b9abe993c` ·
`fe0cdfb06` · `06b1bfa48` · `cc625c32c`) · 변이 (`3b019c9e9`) · 영수증 history (`7ff263197`) · 영수증 재생성 (`f27006370`) · 위키 — GitHub 인사이트
ampworks 기록 (`ded3c47cd`).

## §1 고정 표 §13 ↔ 구현 대응 (좌표 = `b08bb6944` · `tools/env_profile.py` = `EP`)

| §13-3 자리 | 구현 | 회귀 node |
|---|---|---|
| `counts.origins_verified` → **`path_origins_in_record`** | `EP:356` (`len(measured["path_origins"]["in_record"])`) | e02 · s02 · `_assert_closed` 의 `COUNT_KEYS` |
| `unverifiable.origins` → **`path_origins`** | `EP:352` | e02 · s02 · `_assert_closed` |
| 축 `origin` → **`path_origin`** | `AXES` `EP:49–50` · `compare` `EP:306–307` (locked 칸 "경로 검색 origin 이 RECORD 가 있는 유효 배포판 하나의 파일") | e03 [origin_stray] |
| 새 **`not_measured`** = `["loaded_module_origin"]` (세 상태 모두 · `None` 아님) | `NOT_MEASURED` `EP:52` · `compare_lock` 의 결과 초기화 `EP:327` (예외 없이 반환하는 모든 갈래가 이 dict 를 쓴다) | s01 × 3 (MATCH · MISMATCH · UNMEASURED) · `RESULT_KEYS` |
| `measure()` 안쪽 이름 · `_origin` 의 판정 이름 | `EP:194` (`path_origins` {`in_record` …}) · `EP:133` · `EP:178` (`"in_record"`) | s02 (`measure(...)["path_origins"]["in_record"]["numpy"] == "numpy"`) |
| 모듈 docstring — 경로 검색 범위 · 미측정 선언 | `EP:10–13` ("`PathFinder` 로 경로 검색한 origin 파일의 RECORD 소속 (사전 검토 Q5 를 좁힌 꼴)" · "이미 로드된 module 객체 (`sys.modules`) · 그 `__file__` / `__spec__.origin` · 다른 meta-path finder 의 선택은 보지 않는다. 로드된 module origin 은 측정하지 않는다") | s03 |
| 모듈 docstring — **C1 경계 문장** | `EP:6–7` ("C 일치 여부는 실행 gate 가 아니나, 측정 기능을 요구하는 회귀의 지원 환경에서는 측정 불가를 시험 실패로 본다 (e06 · e08)") | s03 |
| `_origin` docstring | `EP:116–120` (`PathFinder.find_spec(module, paths)` · 로드된 객체 · 다른 meta-path finder 는 보지 않는다) | s03 |
| 요약 줄 | `EP:371` ("· 경로 검색 origin 의 RECORD 소속 N (로드된 module origin 미측정)") · `EP:376–377` ("확인 불가 — 경로 검색 origin: …") | s03 · smoke 원문 (증거 11) |

판정 논리 불변 — `_origin` 의 세 갈래와 조건 · `measure` · `compare` 의 비교 · 정렬 · 상태 결정 · CLI rc · lock 문법 · `emit_lock`
(`git diff e2160c2ef b08bb6944` 의 바뀐 줄은 이름 · 문구 · `not_measured` 뿐).

## §2 RED → GREEN

| 단계 | 결과 | 증거 |
|---|---|---|
| RED `e06e0cd6d` (부모 `69b35f65d` + 시험 — 코드는 `e2160c2ef` 그대로) | **38 failed / 5 passed / rc 1** — test_gate90 의 `_assert_closed` 를 쓰는 33 node (닫힌 키에 `not_measured` 없음) · test_gate91 5 (s01 × 3 `not_measured None` · s02 `counts [… origins_verified …]` · s03 `요약에 옛 문구 'origin 확인' 이 남아 있다`) · 통과 5 = e01 · e07 · e09 · e11 · e12 (고정 표 §13-5 예측과 같다) | 00 |
| 겹침 대조 | 등록부 `-k` 410 (k 없는 선언 11 제외) × 새 node 5 → **0** | 00b |
| GREEN `b08bb6944` | **43 passed / rc 0** | 01 |
| 관련 모듈 (clean `b08bb6944`) | 577 passed / **10 failed** — 10 건 모두 "영수증이 낡았다 — validator `3f84c0db52d2b9ac` ≠ 현행 `f0175fff71132003`" (예상 · §4 에서 닫힘) | 02 |

## §3 변이 (고정 표 §13-6)

| 이름 | 끄는 것 (`EP` 좌표) | 죽인 node · 증인 |
|---|---|---|
| `env-profile-checks-module-origin-g90` (기존 · **원문 따라가기**) | 경로 검색 origin 의 불일치 `:306` (원문 `measured["origins"]` → `measured["path_origins"]` — GREEN 뒤 `--check-preimages` 에서 이 항목만 원문 0 회였다) | e03 [origin_stray] · `status MATCH` (불변) |
| `env-profile-measurement-failure-is-unmeasured-g90` (기존 · **치환문 따라가기**) | 측정 예외 → 빈 결과 `MATCH` `:345` (치환문 안의 결과 이름 둘만 새 이름으로) | e05 × 3 · `status MATCH` (불변) |
| `env-profile-declares-loaded-origin-unmeasured-g91` (새) | `not_measured` 를 빈 목록으로 `:327` (모든 것을 쟀다고 주장) | s01 × 3 · `not_measured []` |
| `env-profile-summary-states-path-search-scope-g91` (새) | 요약 줄을 옛 문구 "origin 확인 N" 으로 `:371` | s03 · `요약에 옛 문구 'origin 확인' 이 남아 있다` |

`-k g9 --emit-expect` (증거 03): 15 변이 (-g90 13 + -g91 2) 모두 기대 node 사망 · **-g90 13 의 관측은 기존 EXPECT 와 같다** (이름 · `-k` · fail node ·
증인 불변) → EXPECT 에 -g91 둘 → `-k g9` **15/15 물었다 · rc 0** (증거 04). `--check-preimages`: 모든 변이 지점이 정확히 한 번.

## §4 영수증

history `7ff263197` (두 leg · validator `3f84c0db52d2b9ac` · 현행본 바이트 그대로) → clean `7ff263197` 에서 1 회 재생성 `f27006370` (rc 0 · 증거 06 ·
paired 검사 35 · core `1e3ea7c8…` · grid 검사 34 · core `23c78ed0…`). core diff 는 `core_sha256` · `validator_source_digest` 뿐 (`make_receipt.py` 불변이라
`make_receipt_sha256` 그대로). stamp 의 `environment_profile_C` 에 새 이름 (`unverifiable.path_origins` · `counts.path_origins_in_record`) 과
`not_measured: [loaded_module_origin]` — **MATCH** · lock `d886f30f…` · 170/170 · 가려진 2/2 · 설치 파일 일치 24,804 (해시 없음 10,373) · 경로 검색 origin 의
RECORD 소속 9 · 확인 불가 = RECORD 없는 22 · 경로 검색 origin `yaml`. stamp 의 그 밖 차이는 `validator_commit` · `generated_at_utc` ·
`runtime.platform` (컨테이너 커널 표기) 뿐. `make_receipt.py --check` 두 leg core 재생성 바이트 동일 (06b) · 원장 LEG_PRESERVATION 앵커 2 × 2 · 재생성 뒤
영수증 모듈 113 passed (07 — 02 의 10 건이 닫혔다). grid stamp 의 `validator_tree_dirty: true` 는 90차와 같은 순차 작성의 결과다 (원장 §137 · 개선 후보 ·
이번 범위 밖).

## §5 전체 회귀 · smoke · 등록부 전체 재생 (clean `f27006370` · 순차 · 동시 실행 없음 · 각 단계 시작 = 끝 HEAD · dirty 0)

| 항목 | 결과 | 증거 |
|---|---|---|
| 환경 프로필 C (`python -m tools.env_profile --json`) | **MATCH** · rc 0 · 170/170 · 가려진 2/2 · 설치 파일 일치 24,804 (해시 없음 10,373) · `path_origins_in_record` 9 · `unverifiable.path_origins` [`yaml`] · `not_measured` [`loaded_module_origin`] · 2026-10-04T23:55:08Z → 23:55:11Z | 08 |
| 전체 `pytest tests/ -q -rfEx` | **2182 passed / 1 xfailed / rc 0** (0:57:27 · 23:55:11Z → 00:52:41Z · xfail 은 90차와 같은 선언 항목 `test_gate63_defensive` 하나) · 2182 = 90차 2177 + 새 5 (test_gate91 s01 × 3 · s02 · s03) | 10 |
| `./scripts/smoke_e2e.sh` (기록 단계 포함) | **rc 0** · "pipeline smoke 통과" (2:45 · 00:52:42Z → 00:55:27Z) · 기록 단계 줄: MATCH · 170/170 · 2/2 · 24,804 · 경로 검색 origin 의 RECORD 소속 9 (로드된 module origin 미측정) · 확인 불가 — 경로 검색 origin `yaml` | 11 |
| 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) | **412/412 call 단계에서 선언한 이유로 물었다 · rc 0** — scenario 423 (executable 412 · declared 11) · site 461 (executable 450) · ran 412 · ★ 0 · 00:55:28Z → 03:30:08Z (2:34:40) · 90차 410 + 새 `-g91` 2 | 12 |

## §6 자체 신고

a. **90차 고정 표 §8 "기존 시험은 바꾸지 않는다" 의 예외** — `tests/test_gate90_env_profile.py` 를 이름 따라가기로 고쳤다 (상수 셋 · `_assert_closed` 의
   `unverifiable` 키 · e02 기대 두 칸 · e03 `origin_stray` 기대 축 · docstring 한 줄). 사례 · node 이름 · 검사 강도는 그대로다 — 고정 표 §13-5 에 미리
   고정했다. RED 에서 33 node 가 빨개진 것은 이 이름이 실제로 결과 dict 를 고정하고 있다는 뜻이다.
b. **s02 는 검토자 반례의 고정이다** (원장 §137 · G90-N1): 이 시험 프로세스에는 실제 설치 numpy 가 로드돼 있고 (`sys.modules["numpy"]` · 합성 site 밖),
   합성 경로의 경로 검색은 RECORD 가 있는 가짜 numpy 를 찾는다 → 결과는 `MATCH` · `path_origins_in_record` 9 (numpy 포함) · 주인 = 합성 `numpy` ·
   `not_measured` 선언 · 대조 뒤에도 `sys.modules["numpy"]` 는 같은 객체. 곧 이 수는 로드된 module 의 확인이 아니며, 결과가 그것을 스스로 밝힌다.
c. **`not_measured` 는 측정 칸이 아니다** — 세 상태 모두 같은 값이고 `UNMEASURED` 에서도 `None` 이 아니다 (61차 P1-3 의 "측정하지 않은 칸은 `None`"
   과 구별: 이 키는 도구 범위의 선언이고, 빈 목록이면 "모든 것을 쟀다" 로 읽힌다 — 그래서 변이 -g91 하나가 정확히 그 빈 목록이다).
d. **유효 정정 대응** (원문은 고치지 않는다 — 덧붙이기만): 고정 표 §4-1 origin 행 · §4-2 키 · §4-4 첫 문장 (C1) · §8 e03 · §9 한 행 → 고정 표 §13-4 ·
   원장 §135 "고정 표가 초안에 더한 세부 (2)" · §136 표의 "origin 확인 9" → 원장 §138 · **GATE90 요청문** §1 4-1 행 ("주인 하나 = 확인") · §4 · §5 ("origin
   확인 9" · "확인 불가 … origin `yaml`") · §6-a ("실제 origin" 축) → 이 요청문의 §1 · §4 · §5 표현 ("경로 검색 origin 의 RECORD 소속 9 · 로드된 module
   origin 미측정") 이 유효 정정이다. 기존 `MATCH` · 90차 수용 · 과거 수치 결과는 이 좁은 의미로 그대로다 (재분류 없음).
e. **C1 경계** (모듈 docstring · 고정 표 §13-4): C 일치 여부 (`MATCH` / `MISMATCH`) 는 실행 gate 가 아니다 — pytest · smoke · `run.sh` · 영수증 생성을
   막지 않는다. 측정 기능을 요구하는 회귀 (e06 실제 환경 · e08 CLI) 의 지원 환경에서는 측정 불가 (`UNMEASURED`) 를 시험 실패로 본다. smoke · `run.sh` ·
   영수증 생성은 `UNMEASURED` 에도 막히지 않는다. CLI 요약의 "(기록 전용 — 아무것도 막지 않는다)" 는 도구 자신의 판정에 대한 말이라 그대로 두었다.
f. **lock 은 다시 내지 않았다** — 머리 주석 (`HEADER`) 에 origin 문구가 없고 `emit_lock` 출력은 바뀌지 않는다 (e01 정규형 고정점 · 사슬의 환경 프로필
   `lock_sha256` `d886f30f…` 그대로).
g. 내부 이름 (`measure()` 의 `origins` → `path_origins` · `verified` → `in_record`) 도 같은 뜻으로 바꿨다 — 결과 dict 밖이지만 s02 가 그 이름을 읽는다.
   함수 이름 `_origin` 과 변이 이름 `env-profile-checks-module-origin-g90` 은 그대로 두었다 (식별자 · 증거 · EXPECT 결속).
h. 검증 사슬은 clean `f27006370` 에서 돌렸다 — 그 뒤 커밋은 증거 · 요청 문서 · 위키 (ampworks 기록 `ded3c47cd`) 와 게이트 차수 밖 COMSOL r2
   (bms-balancing) 뿐이다 (RUN_SCOPE 밖).

## §7 하지 않은 것

실제로 로드된 module origin 의 측정 (선택지 C) · D guard · C 의 fail-closed · lock 재생성 · 설치 · 업그레이드 · `make_receipt.py` 의 grid stamp 순서 개선 ·
`src/` · `run.sh` · `configs/` · `tests/conftest.py` · `requirements*.txt` · `scripts/` · 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class ·
투영 게시. COMSOL B-min r2 는 게이트 차수 밖으로 따로 했다.
