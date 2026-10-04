# GATE90 요청 — PyBaMM 환경 고정 라운드 결과 (프로필 C lock · 기록 대조 + 프로필 B 역사 기록) · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`e2160c2ef`** — 89차 판정 대상 `26c11d6fc` 뒤 RUN_SCOPE 를 바꾼 커밋은 이것 하나 (4 파일 · +608 −3): 새 `requirements-validation-C.lock.txt` (190 줄) · 새 `tools/env_profile.py` (404 줄) · `requirements.txt` **주석만** (요구 줄 12 개 바이트 불변) · `scripts/smoke_e2e.sh` +6 (기록 단계 하나). `src/` · `run.sh` · `configs/` · `requirements-gpu.txt` 불변 (고정 표 §2 상한 안). `source_digest` **`803e2b7781cbc9cd` → `3f84c0db52d2b9ac`** |
| 사용자 승인 | 원장 §135 (2026-10-04) "권고대로 너가 순서대로 해줘 같이 쳐내가자" — 범위 초안 (`666524050`) §5 D1–D6 권고 그대로 → 고정 표 `docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` 를 코드 변경 전 커밋 (`1f3829b9a`) |
| 판정 요청 | (1) **C lock** — 내용 · 닫힌 문법 · 정규형이 고정 표 §3 대로인가 (2) **대조** — 측정 축 · 결과 dict · CLI 가 §4 대로이고, **기록 대조 (D3) 의 경계** (어떤 실행도 막지 않는다 · `UNMEASURED` 를 `MATCH` 로 적지 않는다 · 측정하지 않은 칸은 `None`) 가 지켜지는가 (3) **기록 자리** — smoke · 영수증 stamp · 게이트 증거 (§5) (4) **B** = 네 v4 producer manifest 의 기록 (§6) (5) **requirements** — 주석 정정 (D5) · 하한 불변 (D4) (6) 회귀 · 변이 · 영수증 · 전체 회귀 |
| 아님 | 실행 GO · D guard (새 truth 생산 허가 검사 — 별도 라운드) · C 의 fail-closed · 설치 · 버전 변경 · B 로 정본 재생성 · 새 세대 · 26.7.1 ↔ 26.8 비교 · `requirements.txt` 하한 변경 · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini · class · 투영 게시 |

89차 요청 (`8113f12bd`) 과 이 요청 사이의 다른 커밋은 모두 RUN_SCOPE 밖이다: 89차 발송 SHA docs-lint 보존 (`9fa175f3e`) · 89차 회신 접수
(`992ea2a63` · `023876a66` · `64b6c3c2f`) · 게이트 차수 밖 COMSOL §42–§52 (A0 대응표 · 자료 요청 · B-min 후보 · r1 — `be37453ed` …
`741dde19b`) · REIL 부속 B 수용 · 선행 조건 · N2 (`1815a8945` · `72318525a` · `899f966de` · `1fb9a24ed` · `257d4cc1c`) · 이 라운드의 범위
초안 (`666524050`) · 착수 기록 (`1f3829b9a`) · RED (`cff5e409b`) · 증거 규칙 (`fb29e63f0`) · 증거 (`2165a9183` · `c547c2458`) · 영수증
history (`cbf25ad61`) · 변이 (`2586138c3`) · 영수증 재생성 (`1296af1f5`).

## §1 고정 표 ↔ 구현 대응 (좌표 = `e2160c2ef` · `tools/env_profile.py` = `EP`)

| § | 고정 | 구현 | 회귀 node (`tests/test_gate90_env_profile.py`) |
|---|---|---|---|
| 3-1 | 닫힌 문법 · 형식 오류 → `UNMEASURED` (줄 번호) | `EP:203` `parse_lock` (지시 6 · 정확히 한 번 · JSON 문자열 · `profile "C"` · 배포판 PEP 503 엄격 오름차순 · record hex64/none · 가려진 항목 비감소 · 모르는 줄 `:249`) · `LockFormatError` `:71` | e04 × 12 |
| 3-2 | 실측 내용 · 정규형 고정점 | lock 190 줄 = `python -m tools.env_profile --emit-lock` 출력 · `EP:191` `emit_lock` · 머리 주석 `EP:57` | e01 · e02 |
| 4-1 | 측정 = 그 프로세스의 `sys.path` 순서 | `EP:133` `measure` (`invalidate_caches` `:135` · 항목마다 `distributions(path=[항목])` · 정규 이름 첫 항목 = 유효 · RECORD 텍스트 sha256) · `_verify_files` `EP:82` (모르는 알고리즘 `:93` → 측정 실패 · 없는 파일 `:99` → 불일치) · `_origin` `EP:110` (`PathFinder.find_spec` `:112` · 주인 하나 = 확인 · RECORD 없는 배포판 디렉터리 안 = 확인 불가 · 그 밖 = 불일치) · `KEY_MODULES` `EP:41` | e02 · e03 × 14 · e05 × 3 · e06 · e07 |
| 4-2 | 닫힌 결과 dict · 세 상태 · `None` | `EP:310` `compare_lock` (읽기 · UTF-8 · 형식 · 측정 예외 `:332` → `UNMEASURED`) · `EP:273` `compare` (축 12 · `(axis, subject)` 순) | e02–e06 의 `_assert_closed` |
| 4-3 | CLI — 세 상태 모두 rc 0 · `--emit-lock` 측정 실패 rc 1 | `EP:371` `main` (`--json` · `--emit-lock` UTF-8 바이트 · 요약 `:399–400`) | e08 |
| 4-4 | 막지 않음 · 도구 예외만 smoke 실패 | smoke `scripts/smoke_e2e.sh:75` `"$PY" -m tools.env_profile \|\| bad …` | e09 · smoke 원문 (증거 11) |
| 5-2 | 영수증 stamp (core 밖) | `docs/22p_gap/make_receipt.py:237` `_stamp()` · `:231` `"stamp": _stamp()` · `:255` `environment_profile_C` · `tools/preserve.py` 불변 | e10 · 영수증 (§4) |
| 6 | B = 네 manifest 기록 · 어떤 코드도 읽지 않음 | `docs/22p_gap/env_profile_B_v4.yaml` (73 줄 · env 여덟 자리 · solver 다섯 기록 · 한계 · 주장하지 않는 것) | e11 |
| 7 | 주석 정정 · 요구 줄 불변 | `requirements.txt` 줄 2–9 (옛 주석을 "옛 주석" 으로 인용 · B · C 가리킴) | e12 |

## §2 RED → GREEN

| 단계 | 결과 | 증거 |
|---|---|---|
| RED `cff5e409b` (부모 `1f3829b9a` + 새 시험) | **38 failed / rc 1** — 33 `ModuleNotFoundError: tools.env_profile` · e01 lock 없음 · e11 B 없음 · e09 smoke 호출 0 · e10 `_stamp` 없음 · e12 정정 전 | 00 |
| 겹침 대조 | 등록부 `-k` 397 (실행 가능 · k 없는 선언 11 제외) × 새 node 38 → **0** (pytest KeywordMatcher) | 00b |
| GREEN `e2160c2ef` | **38 passed / rc 0** | 01 |
| 관련 모듈 (clean `e2160c2ef`) | 577 passed / **10 failed** — 10 건 모두 "영수증이 낡았다 — validator `803e2b7781cbc9cd` ≠ 현행 `3f84c0db52d2b9ac`" (예상 · §4 에서 닫힘) | 02 |
| 시험 메시지 결정화 뒤 | **38 passed / rc 0** (판정 · node 이름 불변 — §6-b) | 05 |

## §3 변이 (`-g90` 13 · 고정 표 §9 그대로)

| 이름 | 끄는 것 (`EP` 좌표) | 죽인 node · 증인 |
|---|---|---|
| `env-profile-compares-interpreter-and-platform-g90` | 해석기 · 플랫폼 다섯 축 비교 `:277` | e03 [python · implementation · system · machine · libc] · `status MATCH` |
| `env-profile-reports-missing-dists-g90` | lock 에만 있는 배포판 `:280` | e03 [dist_missing] · `status MATCH` |
| `env-profile-reports-extra-dists-g90` | 환경에만 있는 배포판 `:282` | e03 [dist_extra] · `status MATCH` |
| `env-profile-reports-version-drift-g90` | 버전 비교 `:285` | e03 [dist_version] · `status MATCH` / [env_upgrade] · `축 ['dist_record']` |
| `env-profile-reports-record-drift-g90` | RECORD digest 비교 `:287` | e03 [dist_record] · `status MATCH` |
| `env-profile-reports-shadowed-drift-g90` | 가려진 항목 비교 `:290` | e03 [shadowed] · `status MATCH` |
| `env-profile-verifies-installed-files-g90` | 설치 파일 재해시 불일치 `:295` | e03 [file_hash · file_missing] · `status MATCH` |
| `env-profile-checks-module-origin-g90` | origin 불일치 `:297` | e03 [origin_stray] · `status MATCH` |
| `env-profile-lock-grammar-is-closed-g90` | 모르는 줄 → 건너뜀 `:249` | e04 [garbage_line] · `status MATCH` |
| `env-profile-measurement-failure-is-unmeasured-g90` | 측정 예외 → 빈 결과 `MATCH` `:332` | e05 × 3 · `status MATCH` |
| `env-profile-cli-is-record-only-g90` | `MISMATCH` 에 rc 1 `:399–400` | e08 · `rc 1 (MISMATCH) — 기록 전용이면 0` |
| `smoke-records-env-profile-g90` | smoke 기록 단계 제거 (`smoke_e2e.sh:75`) | e09 · `smoke 의 env_profile 호출 0 개` |
| `receipt-stamp-records-env-profile-g90` | stamp 필드 제거 (`make_receipt.py:255`) | e10 · stamp 키 목록 |

`--emit-expect` (증거 03 · 13 변이 · 21 node 사망) → EXPECT 13 → 단독 대조 **13/13 물었다 · rc 0** (증거 04 · scenario 13 · site 13).
`--check-preimages`: 모든 변이 지점이 정확히 한 번. 첫 관측 (증거 03a) 은 증인에 tmp 경로가 섞여 쓰지 않았다 (§6-b).

## §4 영수증

history `cbf25ad61` (두 leg · validator `803e2b7781cbc9cd` · 현행본 바이트 그대로) → clean `2586138c3` 에서 1 회 재생성 `1296af1f5` (rc 0 ·
증거 06 · paired 검사 35 · core `8408f8c2…` · grid 검사 34 · core `7f0f40f0…`). core diff 는 `core_sha256` · `validator_source_digest` ·
`make_receipt_sha256` (`9c8cf71a…` → `61be9d0f…` — `_stamp()` helper) 뿐. stamp 에 새 `environment_profile_C` — **MATCH** · lock
`d886f30f…` · 170/170 · 가려진 2/2 · 설치 파일 일치 24,804 (해시 없음 10,373) · origin 확인 9 · 확인 불가 = RECORD 없는 22 · origin `yaml`.
`make_receipt.py --check` 두 leg core 재생성 바이트 동일 (06b) · 원장 LEG_PRESERVATION 앵커 2 × 2 · 재생성 뒤 영수증 모듈 113 passed
(07 — 02 의 10 건이 닫혔다).

## §5 전체 회귀 · smoke · 등록부 전체 재생 (clean `257d4cc1c` · 순차 · 동시 실행 없음 · 각 단계 시작 = 끝 HEAD · dirty 0)

| 항목 | 결과 | 증거 |
|---|---|---|
| 환경 프로필 C (`python -m tools.env_profile --json`) | **MATCH** · rc 0 · 170/170 · 가려진 2/2 · 설치 파일 일치 24,804 (해시 없음 10,373) · origin 확인 9 · 확인 불가 = RECORD 없는 22 · origin `yaml` · 2026-10-04T18:04:52Z → 18:04:55Z | 08 |
| 전체 `pytest tests/ -q -rfEx` | **2177 passed / 1 xfailed / rc 0** (1:00:47 · 18:04:55Z → 19:05:45Z · xfail 은 89차와 같은 선언 항목 `test_gate63_defensive` 하나) · 2177 = 89차 2139 + 새 38 | 10 |
| `./scripts/smoke_e2e.sh` (기록 단계 포함) | **rc 0** · "pipeline smoke 통과" (2:47 · 19:05:45Z → 19:08:32Z) · 기록 단계 줄: MATCH · 170/170 · 2/2 · 24,804 · origin 9 | 11 |
| 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) | **410/410 call 단계에서 선언한 이유로 물었다 · rc 0** — scenario 421 (executable 410 · declared 11) · site 459 (executable 448) · ran 410 · ★ 0 · 19:08:32Z → 21:53:04Z (2:44:32) · 89차 397 + 새 `-g90` 13 | 12 |

보충: 고정 표 커밋 `1f3829b9a` 의 docs-lint (`pytest tests/test_docs_lint.py`) **358 passed / rc 0** — 끝 HEAD 는 `cff5e409b` (그 사이 차이는
docs-lint 가 읽지 않는 `tests/` 시험 파일 하나 · dirty 0 · 증거 13). 발송 HEAD 의 docs-lint 는 발송문에 적는다.

## §6 자체 신고

a. **고정 표가 범위 초안에 더한 세부** (원장 §135 에 명시): 대조 목록은 `pip freeze` 167 이 아니라 `importlib.metadata` 전체 (유효 170 ·
   가려진 2 — `pip freeze` 는 pip · setuptools · wheel 을 숨기고 같은 이름의 두 위치를 하나로 보인다) · 사전 검토 Q5 의 "실제 origin" 축
   (핵심 module 10) · 설치 파일의 RECORD 재해시 (설치 뒤 변경 감지 — RECORD 가 덮는 범위만).
b. **GREEN 뒤 시험 assert 메시지를 바꿨다** (`2586138c3` · 판정 · node 이름 불변): 첫 `--emit-expect` (03a) 의 증인에 결과 dict 의 `lock_path`
   (tmp 경로 `pytest-NNNN`) 가 섞여 다시 돌리면 맞지 않았다 (증인 = 실패 본문 첫 `E ` 줄 200 자 안의 부분 문자열). 메시지를 상태 · 축 집합 ·
   rc 로 바꾸고 다시 관측 (03) · 38 passed (05). node 이름이 그대로라 겹침 대조 (00b) 는 유효하다.
c. **측정 경로 = 그 프로세스의 `sys.path` 그대로**다. 같은 디렉터리가 `sys.path` 에 두 번 있으면 그 안의 배포판이 가려진 항목으로 다시
   세어져 `MISMATCH` (shadowed) 로 적힌다 — 거짓 `MATCH` 쪽이 아니다. 이 컨테이너의 CLI · pytest · make_receipt 경로에는 배포판이 든 중복
   디렉터리가 없다 (e06 이 저장소 안 경로 셋을 확인 · 실측 MATCH).
d. Windows 에서 RECORD 없는 배포판의 디렉터리와 origin 이 다른 드라이브면 `os.path.commonpath` 가 `ValueError` → 측정 실패 (`UNMEASURED`).
   거짓 `MATCH` 는 아니다 · 이 환경에서 재현할 수 없어 시험이 없다.
e. RECORD 없는 Debian 배포판 22 (pyyaml · pip · setuptools · wheel · cryptography 등) 는 파일 · origin 대조가 불가능하다 — `unverifiable`
   에 이름으로 따로 적고 `MATCH` 는 그것을 주장하지 않는다. `yaml` 의 origin 이 그 예다.
f. lock 은 이 검증 컨테이너의 실측이다 — 사용자 Windows · 생산 서버에서는 `MISMATCH` 가 정상이고 아무것도 막지 않는다 (D3).
g. e06 은 실제 환경 측정이 `UNMEASURED` 가 아니기를 요구한다 — 측정 자체가 실패하는 기계에서는 이 시험이 빨개진다 (대조 결과와 별개로
   "도구가 그 환경을 잴 수 있는가" 의 시험이다).
h. `KEY_MODULES` 를 `tools/env_profile.py` 에 따로 두었다 (`src/io.py` 를 건드리지 않는 상한) — e07 이 `env_fingerprint()` 의 module 축과
   순서까지 대조한다.
i. 검증 사슬 사이에 게이트 차수 밖 커밋 하나 (`257d4cc1c` · REIL N2 문서) — 전체 실행은 그 HEAD 에서 했다.
j. **센 수의 정정 (자체 발견):** 고정 표 §6 · 원장 §135 · GREEN 커밋 메시지 · B 기록 머리 주석에 env 가 든 자리를 "일곱" 이라고 적었다 —
   실제는 **여덟** (grid_curves_v4 `env` · `grid_run_spec.env` 둘 + 세 fit 의 `run_spec.env` · `start_provenance.env` 둘씩). e11 은 manifest 를
   걸어 찾은 집합과 전수 대조하므로 판정은 바뀌지 않는다. 고정 표는 정정 절 (§12) 을 덧붙이고 · 원장은 §136 에서 · B 머리 주석은 고쳐
   다시 낸다 (데이터 바이트 불변 · RUN_SCOPE 밖) — 커밋 메시지는 고칠 수 없어 여기 적는다.
k. **e04 사례 하나를 고정 표 §8 목록 밖에서 더했다:** `profile_not_c` (`#@ profile "B"` → `UNMEASURED`) — 고정 표 §3-1 의 `profile` 은 `"C"`
   규칙을 지키는 사례다. 그래서 e04 는 11 이 아니라 12 사례다.

## §7 하지 않은 것

D guard · C 의 fail-closed · 설치 · 업그레이드 · 다운그레이드 · B 로 정본 재생성 · 새 세대 생산 · 26.7.1 ↔ 26.8 비교 계산 · 기존 정본 수용의
소급 변경 · `src/` · `run.sh` · `configs/` · `tests/conftest.py` · `requirements-gpu.txt` · 실행 GO · 새 연구 leg · 운영 v6 계획 · 세대표 ·
p_ini · class · 투영 게시. REIL · COMSOL 은 게이트 차수 밖으로 따로 했다.
