# DEM 언로딩 키트 — Codex 재확인 반영의 Linux 실행 증거 (2026-10-14 · 결과 0 건 · LIGGGHTS 없음)

> 무엇: Codex 재확인 판정 (codex_review_dem_unloading_kit_reverify_20261014.md · 핀 `a30fe150e` · HOLD) 의 `ULKRR-02` · `03` · `04` 와 수정 계획
> (dem_unloading_kit_reverify_fix_plan_20261014.md · ✅ 1저자 10-14 Q1–Q7 권고대로) Q4 · Q5 · Q6 을 고친 뒤, 판정문 §9-5 (지원되는 Linux 환경에서 모의 러너 ·
> 문법 · 포장 시험의 **전체 로그와 rc**) 를 채운 것.  Codex 환경은 Bash 가 시작 전에 막혀 (판정문 §8) 이 부분을 인증하지 못했다.
> ⚠ 자기시험 · 모의 러너 · 합성 자료다 — 실제 LIGGGHTS 바이너리 실행 (§1-6 문법 fixture 실행 2 · ibb) 이나 실제 원자료 판독을 대신하지 않는다.

## 1. 환경

| 항목 | 값 |
|---|---|
| OS | Linux (`Linux-6.18.44-fc-v114-x86_64-with-glibc2.39` · 클라우드 컨테이너) |
| Python | 3.11.15 (모든 명령 `python3 -I` — 표준 라이브러리만 · ul_s3 F1 의 봉인 대조만 numpy) |
| Bash | GNU bash 5.2.21(1)-release (x86_64-pc-linux-gnu) — 러너 모의 (`run_unload.sh` · `run_history.sh` · `run_unload_ibb.sbatch`) 가 실제로 돈다 |
| LIGGGHTS · MPI · SLURM | 없음 — 가짜 `mpirun` · `lmp` (시험 쪽 스크립트 · 운영 코드 우회 없음) |
| 실행 폴더 | 키트 폴더 `docs/data/ps45_unload_20261009/` (cwd) · 각 명령의 화면 전체 = `<묶음>/<이름>.log` (머리에 명령 · rc · 시간) · 요약 = `<묶음>/summary.json` |

## 2. 묶음 셋

| 폴더 | 코드 상태 | 무엇 |
|---|---|---|
| `baseline_77b5885e0/` | `77b5885e0` (작업 시작 판 · `039abb141` 문법 fixture 고침 포함) | 이 판의 시험 전부 rc 0 — Linux 에서 원래 시험이 실제로 도는가 (Codex 가 못 돌린 Bash 부분 포함) |
| `before_fix_tests_first_c696dbf0f/` | `c696dbf0f` (새 시험만 더함 · 키트 코드 그대로) | 시험 먼저 — 새 시험이 고치기 전 코드에서 **의도한 이유로** 실패 (아래 §3 왼쪽 수) |
| `after_fix_82d532c60/` | `82d532c60` (수정 `ca59641ca` + README) · `git status` 깨끗 · 키트 `SHA256SUMS` sha256 `3bd18ff6adad9e8656721504bcfb58558bc3655b991bc6e73668ceee39a73767` · `history_test/SHA256SUMS` `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d` | 최종 — 전부 rc 0 |

## 3. 명령 · rc · 검사 수 (✓ 줄 수 / 전체 · 시험 먼저 → 최종)

| 명령 (`python3 -I …`) | 77b5885e0 | 시험 먼저 c696dbf0f | 최종 82d532c60 |
|---|---|---|---|
| `ul_lib.py --selftest` | rc 0 · 19/19 | rc 1 · 19/21 (L13 ×2 = `exact_id` · `ids_of` 없음) | rc 0 · 21/21 |
| `ul_s3.py --selftest` | rc 0 · 14/14 | rc 1 · 14/16 (F12 ×2 — 소수 원자 ID · 쌍 참조가 PASS) | rc 0 · 16/16 |
| `ul_observers.py --selftest` | rc 0 · 21/21 | rc 0 · 21/21 | rc 0 · 21/21 |
| `ul_gates.py --selftest` | rc 0 · 35/35 | rc 1 · 36/37 (C3 G2c 쌍 참조 2 → 2.5 PASS · C3 G2 소수 = 원래도 FAIL = 고정 시험) | rc 0 · 37/37 |
| `ul_reader.py --selftest` | rc 0 · 111/111 | rc 1 · 114/158 (44 실패 — R28 6 · R29 6 · R30 7 · R31 3 · R32 22 · 양성 대조 R28 · R30 · R31 셋은 통과) | rc 0 · 158/158 |
| `seal_kit.py --selftest` | rc 0 · 12 ✓ | rc 0 | rc 0 · 12 ✓ |
| `seal_kit.py --check` | rc 0 · 76 파일 · 규칙 22 | rc 0 · 규칙 22 | rc 0 · 76 파일 · 규칙 24 · 폐기 0 |
| `make_unload_decks.py --selftest` | rc 0 · 291/291 | rc 0 · 291/291 | rc 0 · 291/291 |
| `make_unload_decks.py --check` | rc 0 · 덱 64 = 생성 결과 | rc 0 | rc 0 · 덱 64 = 생성 결과 |
| `history_test/make_history_decks.py --selftest` | rc 0 · 172 ✓ | rc 0 · 172 ✓ | rc 0 · 172 ✓ |
| `history_test/make_history_decks.py --check` | rc 0 · 덱 9 · 15 파일 | rc 0 | rc 0 · 덱 9 · 15 파일 |
| `history_test/read_history.py --selftest` (러너 모의 S25–S29 · S37 · S38–S40 = 실제 `run_history.sh` · 보고 묶음 포함) | rc 0 · 53/53 | rc 1 · 53/56 (S38–S40 — 파일을 쓴 뒤 실패한 GA · P 에서 이어 감) | rc 0 · 56/56 |
| `ul_runner_test.py --selftest` (모의 러너 전체 · 실제 `run_unload.sh` · `run_unload_ibb.sbatch` · 보고 묶음 M19) | rc 0 · 25/25 | rc 1 · 28/37 (M20 ×2 · M21 · M22 ×4 · M24 ×2) | rc 0 · 37/37 |

- 포장 시험 = `ul_runner_test` M19 (`RJ` · `UB` · `EXT` 보고 묶음 — 결정 파일 포함 · `.bin` 없음) · `read_history` S25 · S37 (`hist_*` · `gram_*` 보고 묶음 + sha256 줄).
- "✓ 줄 수" = 화면의 `✓` 로 시작하는 줄 수 (한 시험이 여러 줄 · 세는 방식은 `tools/run_suite.py`).  rc 는 프로세스 종료 코드 그대로.

## 4. 고치기 전 실패가 의도한 이유인가 (발췌 · 전문 = `before_fix_tests_first_c696dbf0f/*.log`)

| 시험 | 고치기 전 관측 (그 로그 그대로) |
|---|---|
| R29 실제 판독기 CLI (stdout 닫힘) | `{'rc_r': 120, 'rc_k': 120, 'status': 'RESTORED', 'base': True, 'gate': True}` — Codex `actual_restore_cli_closed_stdout` 를 Linux 에서 재현 (restore 증서 · kebase 기준 파일을 쓴 뒤 rc 120 · UB 관문 허용) |
| R30 열 결손 (끝점 · S0 · 복원 S0) | `KeyError: 'id'` (Codex `parsing_missing_column`) |
| R28 RESUME 없는 중복 · 승인 안 된 경계 넷 | 주 값 OK · UVa 허용 (옛 `_supersede` 가 무조건 버림) |
| R31 창 기록 w 3 빠짐 · 간격 틀림 | trajectory DONE (줄 인접을 창 연속으로 셈) · `separation()` 에 `w_steps` 없음 |
| R32 | `NameError: grammar_prereq` (사전 점검 없음) |
| M20 | UB 관문 허용 (끝 줄 `reader_rc=120` · `reader_rc=2` 를 안 읽음) |
| M21 | 첫 `s0p` rc 1 인데 EXT2 실행 |
| M22 | 문법 판정 없음 · FAIL · 덱 · LMP 다름 = 전부 RJ 진행 (LIGGGHTS 호출 8 · RJ 폴더 생김) |
| M24 | RESUME UC → 잡 기록에 이어 돌림 줄을 덧붙인 뒤 "restart_unload_* 가 없다" 로 멈춤 · `prior_attempts` 없음 |
| S38–S40 | GA · P 가 파일을 다 쓴 뒤 rc 1 인데 GB · GA · 소비 단계가 돌았다 |

- 시험 쪽 결함 둘을 시험 먼저 커밋 전에 고쳤다 (파일을 쓰기로 연 뒤 읽음 — `ul_gates` C3 G2 · `ul_runner_test` `_gram_variant` lmp) — 로그는 고친 시험으로 다시 돌린 것.
- `R31` 단위 시험의 기대 하나를 수정 커밋에서 바로잡았다: 빈 구간 뒤 w 4 · 5 두 0 창은 **새 분리 선언이 맞다** (규칙대로) — 처음 쓴 기대 (w 1 · 2 · 4 · 5 → 최종 분리 아님) 가
  틀렸고, w 1 · 2 · 4 (최종 분리 아님) + w 1 · 2 · 4 · 5 (w 5 에 새 선언 · 분리 뒤 창 [w 5]) 로 나눴다.  고치기 전 코드에서는 두 꼴 다 `TypeError` 로 실패한다.

## 5. Q5 — `039abb141` 문법 fixture 코드의 판정이 새 사전 점검을 통과하는가 (`grammar_039abb141_probe/`)

`tools/grammar_039_probe.py` = `git archive 039abb141 …/history_test` 를 풀어 **그 판의** `run_history.sh --grammar-only` (러너) 와 `read_history.py --grammar` (읽는 쪽) 를
가짜 바이너리로 돌린 뒤 (가짜 lmp = 리포의 합성 단계 작성기 — LIGGGHTS 대역 · 원 덱 tgz 가 리포에 있어야 해서) 새 `ul_reader.py grammar` CLI 에 넘긴다.

| 단계 | 결과 |
|---|---|
| `039abb141` 러너 + 읽는 쪽 | rc 0 · `grammar_verdict.json` status PASS · exit_code 0 |
| 그 런의 kit `SHA256SUMS` (039abb141 판) 의 세 줄 | `in.hist_producer.liggghts` `bc42a3ad…` · `in.hist_grammar.liggghts` `a1f0ee43…` · `plate_hist.stl` `5bc74ec7…` = 사전 점검 봉인 값 |
| 새 사전 점검 · 같은 바이너리 sha256 | rc 0 · `GRAMMAR_PREREQ status=PASS` |
| 새 사전 점검 · 다른 바이너리 sha256 | rc 2 · `GRAMMAR_PREREQ status=REFUSE` |

⇒ ibb 실행 2 를 `039abb141` (또는 덱이 같은 이 판) 로 돌려 실제 바이너리로 PASS 가 나오면, 그 판정은 같은 LMP 로 도는 RJ · RJ2 · EXT 의 사전 점검을 통과한다
(러너 · 읽는 쪽 스크립트 sha256 은 대조하지 않으므로 이 판의 러너 수정 Q4 (나) 로 무효가 되지 않는다).  ⚠ 가짜 바이너리 판정이다 — 실제 PASS 는 실행 2 뿐.

## 6. 다시 돌리기

```bash
# 리포 루트 · 리뷰 핀 체크아웃 뒤 (Linux · bash · python3)
python3 docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/tools/run_suite.py docs/data/ps45_unload_20261009 /tmp/ulkrr_suite
python3 docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/tools/grammar_039_probe.py "$PWD" docs/data/ps45_unload_20261009 /tmp/gram039.json
```
