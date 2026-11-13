# Codex 반박 리뷰 1/2 (HOLD) 고침 묶음 — Rint ② 코드 묶음 (2026-11-13)

> 판정문 = Codex 반박 리뷰 1/2 `FINAL_REVIEW_RINT2_CODEPKG_d3705e9d1_20261113` (리뷰 핀 `d3705e9d1` · 코드 · 측정 설계 묶음 1/2 = HOLD · 새 P1 없음 · P2 셋 RCPX-01 · 02 · 03 · P3 셋 RCPX-04 · 05 · 06 · 판정문 원문은 이 가지에 반입하지 않았다 = ⬜ 본 세션).
> 1저자 11-13 *"권고대로해"*: Q1 한 묶음 · Q2 실행 환경 = 기록 + "R 동안 고정" 계약 (열쇠에 안 넣음) · Q3 R 계획의 고유 기하 열쇠 · 다시 짓는 비용 = 숫자로 (§4-3) · Q4 ⑥ 시도 3 · 4 = 이 묶음 뒤 마지막 핀으로 (도구 · 원장 줄 = 이 묶음) · Q5 kgy S0 = 개발 자료 (이 묶음 밖).
> 바탕 `d3705e9d1` · 작업 가지 `rint-fix-1113` (push 없음) · 실제 실행 0 건 · 결과 0 건 · 요청서 (`docs/reviews/codex_rint2_codepkg_review_request_20261113.md`) 는 고정 문서라 고치지 않는다 — 정정은 §5.
> 시험 판 = 컨테이너 Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · git 2.43.0 · kgy 판 Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1 (`scripts/check_kgy_py38.sh` 와 같은 판).  게이트 전체 (`scripts/check_all.sh`) 는 이 묶음에서 돌리지 않았다.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed_fixed · Codex 재확인 전) | 닫지 않는 것 |
|---|---|
| RCPX-01–06 · §3 봉인용 git 읽기 (replacement · graft · shallow) · RCP-07 팔별 저장본 audit · Q2 실행 환경 기록 · Q11 결과 전 소비 규칙 (확인 블록 v8 · `SELF-181`) · Q12 비교 설계 (도구만) · ⑥ 시도 3 · 4 도구 · 원장 줄 · `SELF-180` 정정 | 실제 측정 (⑥ 시도 3 · 4 · Q11 GPU · Q12 두 기계 조립) · Q-A (저장본 없는 건설과 대조할 기하 열쇠 · 환경 = 판정문 Q6) · 실행 환경을 열쇠 · 지원 환경 계약에 결속할지 (Q2 = 기록만) · 봉인 숫자 · 현장 자격 (§6) · S0 결과 채택 (Q5) · 회차 ⑥ 잔여 조건 · 게이트 전체 |

## 1. 항목별 (고치기 전 → 뒤)

| 항목 | 고침 | 시험 (고치기 전 → 뒤) | 변이 |
|---|---|---|---|
| **RCPX-01** P2 | `cjunc_store.Store.get_or_build` 가 적중을 돌려주기 직전에 `code_drift()` 를 다시 센다 · 바뀌었으면 저장본을 쓰지 않고 새로 짓는다 (상태 `disabled` · 사유 글) | `scripts/test_cjunc_store.py` T15n (열쇠 셈 도중 코드 파일 바꿈: 고치기 전 = 옛 원장을 hit · 뒤 = disabled) · 묶음 72 PASS · 7 FAIL → 84/84 | M1-01 잡힘 |
| **RCPX-02** P2 | `run_contract.git_fixture_env`: `GIT_TEMPLATE_DIR` = 시험 전용 빈 폴더 · `core.hooksPath` = 시험 전용 빈 폴더 (`GIT_CONFIG_PARAMETERS` 옛 꼴 `'key=value'`) · `GIT_QUARANTINE_PATH` 뺌 · 천장 · NOSYSTEM · GLOBAL 그대로 · `safe.directory=*` 안 씀 · 생산 git 무변경 | `scripts/test_git_env_isolation.py` G7f · g · h (고치기 전 = 훅 실행 · rc 128) · 묶음 20 PASS · 5 FAIL → 25/25 | M2-09–11 잡힘 |
| **RCPX-03** P2 | 새 개발 도구 `scripts/cjunc_asm_compare.py`: `weighted_graph_equal` (정규 가중 그래프 지문) 과 `assembly_bytes_equal` (CSR 형식 · 모양 · data · indices · indptr · RHS · DOF 차례) 을 따로 낸다 · 미완료 · main 지문 null · 빈 그래프 = 양성 근거 아님 · 조립만 기록 (`cjunc_graph_only_record`) 의 비교 = 가중 그래프 같음까지만 | `scripts/test_cjunc_asm_compare.py` K1a = 판정문 반례 재현 (두 노드 · 병렬 간선 합산 차례 → 비대각 `-0x1.0000000000000p+0` ↔ `-0x1.0000000000001p+0` · 그래프 지문 같음 · CSR 다름) · 1/2 → 7/7 (3.11 · 3.8) | MK-01–11 = 첫 회 10/11 (MK-11 생존) → K5 보강 → 11/11 |
| **RCPX-04** P3 | 배열 멤버 머리 해석: `MemoryError` 는 그대로 올리고 그 밖 예외는 `StoreInconsistent` (array) | T7x-1 (shape 2**100 → OverflowError 가 새던 것) · T7x-2 (MemoryError 전파 = 대조) | M1-02 · 03 잡힘 |
| **RCPX-05** P3 | 머리 `key_of(key_parts)` = 머리 key · 머리 `registry_fp` = 복원 원장 fp 대조 (어긋남 = `StoreInconsistent`) | T7x-3 (중복 칸만 고친 파일 둘 + key_parts 없음) · T7x-4 (비권위 칸 writer · runtime = hit 그대로) | M1-04 · 05 잡힘 |
| **RCPX-06** P3 | 문구 철회 · 범위 좁힘 (§5-1) · 생산 `scripts/step3_sigma.py` 무변경 | `scripts/test_step3_gpu_precond.py` G4d · G4e (기록 · 보장 아님) · G4b 글 좁힘 · 묶음 (v8 블록과 함께) 21/22 → 33/33 (3.11 · 3.8) | (기록 시험 · 가드 없음) |
| **§3** 봉인용 git 읽기 | `run_contract.git_env` 에 `GIT_NO_REPLACE_OBJECTS=1` (`GIT_SET_ENV`) → F5 계획 · `git_identity` · payload `_code_sha` · S0 `_git show` 가 원 객체를 읽는다 · 새 `run_contract.git_history_problem` = `GIT_GRAFT_FILE` · `GIT_SHALLOW_FILE` env · 얕은 복제 · `info/grafts` → 사유 (닫힘 · `git fetch --unshallow` 안내) · 원장 역사 · 원장 저장소 꼴 · 조상 대조 · S0 단계 2 조상 관문이 부른다 | G9a (대체 객체 세 꼴: 깨끗 · `GIT_REPLACE_REF_BASE` · 기본 `refs/replace`) · G9b (기준) · G9c (graft · shallow 다섯 꼴) | M2-01–08 = 첫 회 7/8 (M2-02 env 검사 뺌 생존) → G9c 에 env 만 꼴 더함 → 8/8 |
| **RCP-07** 팔별 저장본 출처 | payload 가 팔 곁 파일 `cjstore_audit_<팔>.json` (과학 payload 밖 · 꼴 `cjstore-audit-v1` · 상태 · 열쇠 · 파일 · 파일 sha256 · 사유 · 초 · 바이트 · runtime) 을 쓰고 · 러너가 받아들인 팔과 함께 OUTDIR 로 옮기고 · 사슬 요약 `cjunc_store_arms` 가 런 · 팔마다 싣는다 (끔 = 칸 없음 = 옛 요약 바이트) | `scripts/test_cjunc_store.py` P7 · R3 · C6 · `scripts/test_cjunc_store_e2e.py` Z5b · Z6b (끝-끝 6 PASS · 2 FAIL → 8/0 · 608.6 s) | M1-07–09 잡힘 |
| **Q2** 실행 환경 | `cjunc_store.runtime_record()` = python · numpy · scipy 판 · BLAS · SIMD · 스레드 env 아홉 · numpy SIMD 기능 목록 → 저장본 머리 (비권위 진단) · 팔 audit 의 `runtime` · 열쇠 · 대조 아님 | T16 · T16c | M1-06 잡힘 |
| **Q11** GPU 확인 블록 v8 | `docs/reviews/rint2_codepkg_20261113/q11_gpu_check_block_v8.txt` (블록 md5 b9d45d762f708d6f75ef0ebd6499add9 · 하네스 md5 4eb8a6c3ed2da1039e6b0988f63db906) — 소비 규칙 (§4-4) · `SELF-181` (se_material 출처) · 봉인용 git 읽기 · .pyc 없음 | G8a–l · 묶음 33/33 (같은 시험에 옛 v7 블록을 넣으면 23/32) | MQ-01–16 = 16/16 |
| **Q4** ⑥ 시도 3 · 4 | 감시 셸 `run_probe6.sh` 시도 3 · 4 · 판독기 `probe6_read.py` 저장본 기록 · 원장 §3 시도 줄 3 · 4 · 명령 줄 (§4-5) | `docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py` 바탕 330/330 → 새 시험 넣은 고치기 전 329 PASS · 27 FAIL → 고친 뒤 356 PASS · 0 FAIL (287 s · 고침 커밋의 시험 보강 포함) → 열쇠 ↔ 파일 이름 보강 뒤 357 PASS · 0 FAIL (371 s · 보강 시험의 고치기 전 판독기 = T 129 PASS · 1 FAIL) · R6a · b = 실물 러너 · payload 로 시도 3 `built_written` → 시도 4 `hit` · 팔 JSON 바이트 같음 | 판독기 새 가드 14 (M 묶음 · 시험 안) · 감시 셸 새 가드 22 (§3-1) |

## 2. 커밋 (바탕 `d3705e9d1` 위 · 차례대로)

| sha | 한 줄 |
|---|---|
| `c8975feec` | 시험 먼저 ① — 저장본 RCPX-01 · 04 · 05 · Q2 · RCP-07 · git RCPX-02 · §3 |
| `bbe468a7d` | 고침 — RCPX-01 · 04 · 05 · Q2 · RCP-07 (저장본 · payload · 러너 · 사슬) |
| `b33347fc0` | 고침 — RCPX-02 · §3 (고정물 틀 · 훅 · 격리 경로 · replacement · graft · shallow) |
| `67a09c28f` | 시험 먼저 — RCPX-03 (Q12 비교) |
| `234a17524` | 고침 — RCPX-03 (`scripts/cjunc_asm_compare.py` · 게이트 단계 · kgy 판 18 묶음) |
| `7f7fbb120` | 시험 글 — 끝-끝 Z5b 설명 · 끝-끝 결과 8/0 |
| `cd6d69185` | 시험 먼저 — RCPX-06 기록 · Q11 블록 v8 |
| `57acfb0c8` | 고침 — Q11 블록 v8 (소비 규칙 · `SELF-181`) |
| `1c8a69bc6` | 시험 먼저 — ⑥ 시도 3 · 4 · 감시 셸 봉인용 git 읽기 |
| `20b93e4b6` | 고침 — ⑥ 시도 3 · 4 (감시 셸 · 판독기 · 원장 §3 줄 · 준비 README) + 시험 보강 (T30c 사유 글 · F22c 14 꼴 · 같은 변이 고침) |
| `163246c5b` | 시험 먼저 — ⑥ 판독기 audit 열쇠 ↔ 저장본 파일 이름 대조 (같은 부류 보강 · T30c 23 꼴) |
| `137f91df5` | 고침 — ⑥ 판독기 열쇠 ↔ 파일 이름 대조 (다르면 rc 4) |
| `4aca9ff04` | 기록 — 이 README (첫 판) |
| `c9d0cdd9e` | 원장 — `docs/reviews/findings.json` RCPX-01–06 · SELF-180 · SELF-181 (claimed_fixed) |
| (이 README 끝 판 · 다음 커밋) | 변이 MW 끝 (22/22) · kgy 판 18 묶음 · 변이 문법 확인 |

## 3. 변이 (고친 가드마다 · 작업 트리에서 한 군데 바꾸고 해당 시험을 돌린 뒤 되돌림)

| 묶음 | 수 | 생존 → 처리 |
|---|---|---|
| 저장본 · payload · 러너 (M1) | 9/9 | — |
| git (M2) | 11/11 | M2-02 (graft · shallow env 검사 뺌) 첫 회 생존 → G9c 에 env 만 꼴 (없는 파일의 `GIT_GRAFT_FILE`) 을 더해 잡힘 |
| 조립 비교 (MK) | 11/11 | MK-11 (조기 반환 null 거부 뺌) 첫 회 생존 → K5 사유 낱말을 좁혀 잡힘 |
| Q11 하네스 · 블록 셸 (MQ) | 16/16 | — |
| ⑥ 판독기 (시험 안 M 묶음 · 새 14 = 시도 3 · 4 13 + 열쇠 ↔ 파일 이름 1) | 14/14 | "JSON 아닌 audit 곁 파일" 의 `incomplete` 줄만 빼는 변이 = 관찰상 같은 변이 (상태 대조가 같은 rc 4 를 낸다) → 변이를 사유 글까지 빼는 꼴로 바꾸고 T30c 가 23 꼴마다 사유 글을 본다 |
| ⑥ 감시 셸 (MW · 시험 묶음 F) | 22/22 (§3-1) | 첫 꼴 MW-18 · 20 = bash 문법 오류 (가드를 보지 않음) → 문법 유지 꼴 18b · 20b 로 다시 = 잡힘 |

변이 꼴의 문법 확인 (뒤에 한 번 더 · 11-13): Python 변이 = `compile` 통과 (M1 8 · M2 11 · MK 11 · ⑥ 판독기 14) · 셸 변이 = `bash -n` rc 0 (M1-09 · MQ 셸 5 · MW 20 + 18b · 20b) · Q11 하네스 변이 11 = 블록 heredoc 안 하네스 `compile` 통과 · 잡은 시험 = 그 가드의 뜻 시험 (G8h · i · j · k 등 · md5 관문 G8b 만으로 잡힌 것 없음).  문법 오류였던 것 = MW-18 · 20 첫 꼴 둘뿐.

### 3-1. ⑥ 감시 셸 변이 (MW)

감시 셸 `run_probe6.sh` 의 새 가드마다 한 군데를 바꾸고 시험 묶음 F (`--only F` · 가짜 러너) 를 돌림 · 리포 사본 (`git archive` · 같은 판) 에서 한 개씩 (변이 하나 ≈ 100–150 s).  바꾸기 전 사본 기준 = F 47 PASS · 0 FAIL.

| 변이 | 잡은 시험 (첫 FAIL 줄의 이름) | 잡힘 |
|---|---|---|
| MW-01 GIT_DROP_SH 줄 뺌 | F23 | 예 |
| MW-02 GIT_NO_REPLACE_OBJECTS export 뺌 | F23 | 예 |
| MW-03 graft · shallow env 검사 뺌 | F22c | 예 |
| MW-04 shallow env 만 뺌 | F22c | 예 |
| MW-05 얕은 복제 검사 뺌 | F22c | 예 |
| MW-06 info/grafts 검사 뺌 | F22c | 예 |
| MW-07 이력 관문 결과를 안 봄 | F22c | 예 |
| MW-08 시도 3 빈 저장본 검사 뺌 | F22c | 예 |
| MW-09 저장본 링크 검사 뺌 | F22c | 예 |
| MW-10 시도 4 저장본 없음 검사 뺌 | F22c | 예 |
| MW-11 시도 4 목록 대조 뺌 | F22c | 예 |
| MW-12 시도 3 meta 목록 없음 검사 뺌 | F22c | 예 |
| MW-13 뒤 번호 시도 끝남 검사 뺌 | F19a | 예 |
| MW-14 시도 4 풀이 코드 대조 뺌 | F22d | 예 |
| MW-15 러너에 CJUNC_STORE 안 줌 | F22a | 예 |
| MW-16 저장본 폴더 안 만듦 | F22a | 예 |
| MW-17 command.txt CJUNC_STORE 홈 접기 뺌 | F22a | 예 |
| MW-18b meta attempt3_pin · code_same 뺌 (문법 유지 꼴) | F22b | 예 |
| MW-19 끝 목록 안 잼 | F22a (F22b · F22c 도) | 예 |
| MW-20b 시도 3 meta attempt2_pin 뺌 (문법 유지 꼴) | F22a | 예 |
| MW-21 시도 3 한도 짝 30000 | F22a (F22b · F22c 도) | 예 |
| MW-22 앞 번호 = 시도 N−1 대신 시도 1 | F22b (F22c · F22d 도) | 예 |

- **22/22 잡힘.**  첫 묶음 = MW-01–17 (06:30–07:05 UTC) · 07:05 UTC 컨테이너 재시작으로 MW-18 이 도중에 끊겼다 (사본의 감시 셸은 남은 백업으로 되돌려 리포 판과 바이트 같음 확인) → MW-18–22 를 같은 명령 · 새 출력으로 다시 돌렸다.
- 변이 MW-18 · MW-20 의 첫 꼴 (`if … then` 몸의 echo 줄을 통째로 빼기) 은 빈 `then … fi` = bash 문법 오류였다 (`bash -n` rc 2 · F 33 개 전부 실패 = 가드를 본 것이 아니다) → 변이로 세지 않고 몸을 `:` 로 바꾼 꼴 (18b · 20b · `bash -n` rc 0) 로 다시 돌렸다 → 그 시험 하나만 실패 (F22b · F22a).  나머지 20 변이는 `bash -n` rc 0 (돌리기 전 확인).

### 3-2. 판정문 반례 다시 돌림 (Codex 탐침 원본 · 고친 트리 `scripts/` · Python 3.11 · 이 컨테이너)

탐침은 판정문 증거 묶음 (prior/) 의 원본을 따로 둔 폴더로 옮겨 `--source` 로 고친 트리를 가리켜 돌렸다 (탐침은 제 폴더에만 쓴다 · 트리는 읽기만).  탐침 둘은 옛 동작을 `assert` 로 단언하거나 예외를 잡지 않아 처음 거부에서 멈춘다 → 표시한 대로 바꾼 사본으로 끝까지 돌렸다 (판정 계산은 그대로).

| 탐침 (판정문 항목) | 판정문 때 (리뷰 핀) | 고친 트리 |
|---|---|---|
| `probe_hit_drift.py` (RCPX-01) | 시작 검사 뒤 코드 파일을 바꿔도 `hit` · 받은 원장 registry 94799c77… ≠ 새로 지은 c0202507… | `disabled` · drift = `fibre_segment_raster.py` · 받은 원장 = 새로 지은 원장 (registry c0202507… · strict 같음) |
| `probe_header_integrity.py` (RCPX-05 · 예외를 기록하는 사본) | 중복 칸 손댄 둘 다 `hit` | 기준 `hit` · key_parts 손댐 = `StoreInconsistent` (header) · registry_fp 손댐 = `StoreInconsistent` (header) · 짓기 0 |
| `probe_corrupt.py` (RCPX-04) | shape 2**100 = 날 `OverflowError` | `StoreInconsistent` (array · OverflowError) · 다른 손상 11 꼴 가운데 10 = `StoreInconsistent` (array) · 1 (descr `[['x', 'f8']]` = numpy 가 받는 꼴) = `StoreInconsistent` (header) · 탐침의 "기준" 파일도 `StoreInconsistent` (header) — 탐침 머리에 key_parts 가 없어 RCPX-05 고침이 거부한다 (탐침의 기준이 새 머리 계약을 만족하지 않는다) |
| `probe_git_isolation.py` (RCPX-02 · §3 · `assert` 를 뺀 사본) | replacement 로 F5 통과 · dirty 사라짐 · B blob · shallow · graft env 로 원장 역사 통과 · 부르는 쪽 template 훅 실행 · quarantine rc 128 | F5 = 거부 (`GIT_REPLACE_REF_BASE` · 기본 `refs/replace` 둘 다) · `git_identity` dirty True (원 객체) · payload `_code_sha` = +dirty · S0 `_git show` = 원 blob · shallow · graft env = 원장 역사 사유 (닫힘) · template 훅 = 안 돎 · quarantine 안 물려받음 · commit rc 0 |
| `probe_graph_vs_csr.py` (RCPX-03) | 그래프 지문 같음 · CSR data 다름 | 그대로 (조립기는 안 바꿨다 · 고침 = 비교의 뜻) — `scripts/test_cjunc_asm_compare.py` K1a 가 같은 꼴을 `bytes_equal` False · `graph_equal` True 로 가른다 |

## 4. 질문별 처리

### 4-1. Q2 — 실행 환경 = 기록 + "R 동안 고정"

- 기록: 저장본 머리 `runtime` (지은 프로세스) · 팔 audit 의 `runtime` (그 팔 프로세스).  열쇠 (`key_parts`) 에 넣지 않고 읽을 때 대조하지 않는다 (비권위 진단 · T16c).
- 계약 (1저자 11-13): **R 동안 실행 환경 (python · numpy · scipy 판 · BLAS 코어 · SIMD · 스레드 env) 을 바꾸지 않는다.**  바꿔야 하면 저장본 폴더를 비우거나 새 폴더로 시작한다.  지키는지는 기록을 사람이 대조한다 (자동 거부 없음).
- 한정 (판정문 Q2): machine-id 는 호스트 구별이지 CPU · 라이브러리 빌드 · 복제 기계의 유일성 증명이 아니다 · SIMD 칸 = numpy 가 고른 기능 목록 (CPU 모델 이름 하나로 산술 결정성이 증명되지 않는다) · BLAS 실제 코어는 `OPENBLAS_CORETYPE` 이 없으면 이 기록에 없다 (사슬 `env_record` 의 몫).

### 4-2. RCP-07 · B5 문구 좁힘

- 팔마다 audit 곁 파일 하나 → 어느 팔이 hit · built · disabled 였는지 기록으로 답한다 (판정문 §3 · Q7).  재개 때 복사한 런은 원 시도가 쓴 곁 파일을 그대로 싣는다 — 요약 행 = 런 이름 · 팔 · 상태 · 복사 표지 = 런 기록 `copied_from` · `resume.copied` (요약 행에는 없다).  곁 파일은 payload 의 자기 기록이지 증명이 아니다 (저장본 밖 독립 대조 = 봉인 원천 재조립 · SV 모서리 팔만).
- **B5 (켬 ↔ 끔 산출 바이트 같음) 문구를 좁힌다**: 팔 JSON · 매니페스트 · 영수증 바이트는 그대로 같다 (P2 · R2) · 켬 런의 OUTDIR 에는 팔마다 곁 파일 하나가 더 있다 (끔 = 없음).
- 한정: 러너는 받아들인 팔의 곁 파일만 옮긴다 — 거부된 팔 (한도 · 실패) 의 곁 파일은 킷 런 폴더에 남는다.

### 4-3. Q3 — R 계획의 고유 기하 열쇠 · 다시 짓는 비용 (숫자)

근거 = `docs/reviews/rint2_time_reestimate_20261111/README.md` A-2 · A-3 (가정 = 사다리 12 점 · all3 · 넘침 없음) · ⑥ 시도 1 · 2 실측.

| 양 | 값 | 표지 |
|---|---|---|
| 주 판정의 서로 다른 원장 (기하 열쇠) | 킷 2 × origin 3 (arm 0 · 1 · 2) = **6** · 넘침이 나면 그 킷의 origin 5 더 | 코드 (원장은 R_j · 법칙 · c · SV · UNREG · 섬유 σ 에 달리지 않는다 · 격자 · origin · 문턱이 바뀌면 달라진다) |
| 지금 (저장본 없음) 원장을 짓는 횟수 | 팔 프로세스 74 (SBE 38 + DBE 36) + 봉인 원천 런 48 = **122** | 코드 · 가정 |
| 한 번 짓는 비용 (탄소 접합 준비 = 원장 + 계획) | SBE **4,038 s** (⑥ 시도 1) · **4,040 s** (⑥ 시도 2) · kgy | 실측 (원장 · 계획 몫 = [미확인] · payload 시계가 하나) |
| DBE 한 번 | 재지 않음 — 등록 비 2.933 (다른 σ · 다른 날 두 팔 비) 을 걸면 약 11,850 s | [추정] |
| 저장본 켬 뒤 짓는 횟수 | 생산 팔 = 기계마다 열쇠당 한 번 (한 기계 6 · kgy + gabia 두 기계면 최대 12 · 같은 기계에서 두 프로세스가 동시에 빗나가면 둘 다 짓는다 = `built_peer_same`) · 나머지 = 읽기 (읽는 시간 = [미확인] → ⑥ 시도 4 가 처음 잰다) · 봉인 원천 48 = 그대로 다시 짓는다 (판정 · 다시 판정 · 봉인 원천은 저장본을 읽지 않는다 = 독립 재조립) | 코드 · 가정 |
| 이득 (재추정 문서의 값) | s 와 무관 약 82–225 h | [추정 · 위 한계] (그 문서 요지 7) |

### 4-4. Q11 — GPU C 꼴 채택 = 결과 전 소비 규칙 (블록 v8)

- `result.json` 의 `consume`: `identical` (다섯 짝 비트 같음: 해 바이트 · info · 반복 수 · LAST_BACKEND) 과 `converged` (주 풀이 · 이어 풀기 · 옛 · 새 넷 모두 info 0 · 해 유한) 를 가른다 · `backend_ok` (열 런 모두 gpu + jacobi · 폴백 없음) · `short_iters_ok` (고정 반복 여섯 런이 정확히 200 반복 · info 200) · `source_ok` (live 저장소 모듈 없음).
- **adopt = backend cupy AND 다섯 모두.**  같음은 수렴이 아니다 (`all_identical` true 하나로는 채택 아님) · 셸 rc = 끝까지 돌았다는 뜻일 뿐.
- kgy 결과는 gabia 를 말하지 않는다 (gabia 에서 C 꼴을 쓰거나 성능을 주장하려면 그 기계에서도) · 합성 시드 하나는 실침대가 아니다.
- `SELF-181`: v7 은 `se_material.py` 를 live 작업 트리에서 불러왔다 → v8 = 핀에서 `git show` 로 새 폴더 (모듈 사본과 같은 폴더 · `step3_sigma.py` 는 제 폴더를 sys.path 맨 앞에 둔다) · sha256 · 불러온 자리 대조 · live 저장소 모듈 = 멈춤 · `PYTHONDONTWRITEBYTECODE=1` · git 읽기 앞 GIT_DROP_SH + `GIT_NO_REPLACE_OBJECTS=1`.

### 4-5. Q4 — ⑥ 시도 3 · 4 (도구 · 원장 줄 · 실행 없음)

- 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` §3 = 시도 줄 3 · 4 (시각 · 핀 · 기계 = 빈칸 · 결과 0 건 · 한도 1,500,000 = 시도 2 와 같음) + "시도 3 · 4 의 명령 줄" (결과 전 기대 · 앞 조건 · 멈춤 · 핀 칸 · 블록 · 한정).
- 시도 3 = 빈 저장본 `~/p6_cjstore` → 짓고 씀 (`built_written`) · 시도 4 = 시도 3 이 남긴 저장본 그대로 → 적중 (`hit`) · 감시 셸이 저장본 목록 (이름 · sha256) 을 meta 에 남기고 · 판독기가 audit 곁 파일 (상태 · 열쇠 ↔ 파일 이름 · 파일 sha) 과 목록을 대조한다 (다르면 rc 4).
- 감시 셸 git 읽기 = 봉인용 (GIT_DROP_SH 한 줄 · `GIT_NO_REPLACE_OBJECTS=1` export · graft · shallow 관문 = 멈춤).
- 붙여 넣을 블록 (`KGY_BLOCK.md`) 은 시도 1 · 2 꼴 그대로 — 시도 3 · 4 블록은 발사 전에 마지막 핀으로 새로 (⬜ 본 세션 · 1저자).

### 4-6. Q12 — 두 기계 조립 비교 (설계 · 도구만)

- 비교 기록 (`cjunc-asm-record-v1`) = 정규 가중 그래프 지문 + 조립 바이트 (CSR 다섯 칸 · RHS · DOF 차례 sha256) · 판정 두 칸 (`graph_equal` · `bytes_equal`) · 주장 = 같은 칸만.
- 조립만 기록 (`cjunc_graph_only_record`) 은 조기 반환의 null 도 담는 형식이다 → 양성 근거 = 완료 · main 지문 있음 · 빈 그래프 아님 · 사유 없음일 때만 (`graph_only_positive_problem`).
- 실제 두 기계 실행은 하지 않았다 — 개발 탐침 원장 줄 (코드 · 입력 · 모드 · 읽지 않을 값 · 기대 · 실패 보고) 을 결과 전에 먼저 (판정문 Q12 권고 · ⬜ 1저자).

## 5. 정정

### 5-1. RCPX-06 — 부호 있는 0 (요청서 문장 철회)

요청서의 *"입력 r 의 −0 만 빼면 (r 에 −0 이 없으면) A 꼴 ↔ C 꼴 전처리 비트 같음"* 은 **충분조건이 아니다 — 철회한다.**  음의 유한 비정규 값의 곱이 0 으로 내려앉으면 (underflow) 부호 있는 0 이 생긴다: diag [4, 4] · r [−5e-324, 1] → A 꼴 [+0, 0.25] · C 꼴 [−0, 0.25] (값 같음 · 첫 칸 바이트 다름 · G4d).  남는 문장: **A ↔ C 비트 같음 = 잰 입력 · 잰 환경에서만 (전처리 곱의 부호 있는 0 포함)** · 생산 꼴 b (np.zeros + 양수) 의 두 침대에서 반복마다 같았다는 G4b 관찰은 그 산술 · 그 침대 한정 · 보편 증명 아님.  G4e (유한 SPD 2 × 2 · x0 비정규) = 첫 잔차에서 A ↔ C 적용 바이트가 다르지만 이 가짜 산술에서 끝 해 바이트 같음 · info 0 · 반복 2 (관찰 · 보장 아님).  실제 cuSPARSE 의 연산 · 반올림은 이 시험이 보증하지 않는다.

### 5-2. `SELF-180` — 요청서 §9 "code_diff 빈 파일"

요청서 §9 의 *"코드 핀 ↔ 리뷰 핀 code_diff 가 비었다"* 는 틀렸다 — 그 사이 바뀐 것 = 감시 폴더의 S0 등록 README 한 파일 (+7 −2 · 문서) 이다 (판정문 §7 이 최종 ZIP 의 extra/code_diff_codepin_to_pin.txt 117 B 로 확인 · 정정 수용).  실제 코드 · 실행 블록 변경 0.  보낸 글은 1저자가 전달 때 정정했고, 요청서는 고정 문서라 고치지 않는다.  교훈 = 전칭 (비었다 · 0) 은 diff 원문을 붙여 대조한다 (CLAUDE.md 사전 공격 ①).

## 6. 현장 확인 (kgy · gabia · 발사 전 · ⬜)

| 확인 | 왜 | 어긋나면 |
|---|---|---|
| `git -C <리포> rev-parse --is-shallow-repository` = false | 조상 대조 · 원장 역사 · S0 단계 2 조상 관문 · ⑥ 감시 셸이 얕은 이력을 멈춤으로 닫는다 | `git fetch --unshallow` 뒤 다시 |
| `git -C <리포> for-each-ref refs/replace` 빈 줄 · `<리포>/.git/info/grafts` 없음 | 셸 쪽 GIT_DROP_SH (게이트 `scripts/check_all.sh` · `scripts/check_kgy_py38.sh` · 러너 code_sha 줄 · 등록된 S0 블록 `docs/reviews/rint2_s0_store_probe_20261112/s0_rerun_probe_block.txt`) 에는 `GIT_NO_REPLACE_OBJECTS` 가 없다 (이 묶음에서 안 바꿈 · 등록 글자 그대로) · git 2.43 실측 = `info/grafts` 는 `GIT_NO_REPLACE_OBJECTS=1` 로도 살아 조상 대조를 바꾸고 `--is-shallow-repository` 는 false | 지운 뒤 다시 (지우는 것은 사람) |
| `~/p6_cjstore` 없음 (시도 3 전) | 시도 3 = 없거나 빈 폴더만 받는다 | 시도 3 이 중간에 끊겨 파일이 남았으면 사람이 비운 뒤 시도 3 다시 (감시 셸은 지우지 않는다) |
| 기계마다 저장본 폴더 따로 · 공유 파일계 아님 | 판정문 §3 (개인 소유 고정 로컬 폴더 전제) | 쓰지 않는다 |
| kgy · gabia 의 R 실행 환경 기록 (python · numpy · scipy · BLAS · SIMD · 스레드) | Q2 "R 동안 고정" | 바꾸면 저장본 폴더를 새로 |

## 7. 남은 한정

- RCPX-01: 적중 직전에 한 번 더 재는 것은 창을 좁힐 뿐 — 실행 중 소스 불변 전제 그대로 (stale pyc · import 전 변경 · 함수 객체 교체 = 판정문 §3 의 인증 범위 밖).
- RCPX-03: 실제 두 기계 조립 · cuSPARSE 조립 바이트는 재지 않았다 · 비교 도구는 기록 꼴을 정할 뿐.
- §3: Python 봉인 읽기만 `GIT_NO_REPLACE_OBJECTS` 를 건다 · 셸 GIT_DROP_SH 자리 (§6 표) 는 그대로 · lazy fetch (부분 복제) 는 막지 않는다 (내용 sha 대조가 지킨다).
- ⑥ 시도 3 · 4: 한도에 닿아 팔이 거부되면 audit 곁 파일이 출력 폴더에 없어 판독기는 rc 4 (저장본 기록 없음) — 미수렴과 저장본 결함을 rc 로 가르지 못한다 (러너 로그 · 킷 런 폴더를 본다) · 시도 2 ↔ 3 · 4 는 코드 묶음이 달라 차이를 C 꼴 하나로 귀속하지 않는다.
- kgy 판 (3.8) 전체 묶음 (`scripts/check_kgy_py38.sh` · 18 묶음): 첫 회 (06:30 UTC · `20b93e4b6` 위) = 12 묶음 통과 뒤 07:05 UTC 재시작으로 끊김 → 코드 끝 판 `137f91df5` 에서 처음부터 다시 = **18 묶음 통과 · rc 0 · 54 분** (run_contract 125/125 · step3_rint · ptfe_face_alpha 242 · carbon_junction 547/547 · ca_ext_b6 502 · ca_ext_runner 151 · rint_r_chain 506/506 · rint_r_chain_e2e 51 · rint_r_chain_e2e12 33 · step3_target_cert 264/264 · step3_conv_cert 29/29 · ca_s0_census 186 · probe6 357 · step3_gpu_precond 33/33 · cjunc_store 84 · cjunc_store_e2e 8 · git_env_isolation 25 · cjunc_asm_compare 7/7 · 모두 0 FAIL).  `137f91df5` 뒤 커밋 = README · 원장만 (코드 · 시험 변경 0).

## 8. 1저자가 정할 것

| # | 질문 | 권고 |
|---|---|---|
| Q1 | Q-A — R 에서 저장본을 받아들일 때 저장본 없는 건설과 대조할 기하 열쇠 · 환경 (전 열쇠 6 · 대표 키 표본) | 결과 전에 원장 줄로 고정 · 대표 키만이면 "표본 확인" 으로 적는다 |
| Q2 | 실행 환경을 열쇠 · 지원 환경 계약에 결속할지 (지금 = 기록 + R 동안 고정) | 봉인 전 지원 환경 계약 (판 · BLAS 코어 · 스레드 수 고정) 에 적고 열쇠에는 넣지 않는다 |
| Q3 | Q12 두 기계 조립 비교를 개발 탐침 원장 줄로 등록할지 | 등록 먼저 (결과 0 건) · 실행은 그 뒤 |
| Q4 | 현장 확인 §6 의 둘 (shallow · replace/grafts) 을 ⑥ 시도 3 · 4 · S0 블록 첫 줄에 넣을지 | 넣는다 (읽기만 · 어긋나면 멈춤) · 블록 만들기 = 본 세션 |
| Q5 | Codex 2/2 에 이 고침 묶음의 재확인 (RCPX-01–06 · §3 · Q11 v8 · ⑥ 도구) 을 함께 넣을지 | 넣는다 (리뷰 핀 = 이 묶음을 합친 가지 끝) |
