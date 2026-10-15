# DEM 언로딩 키트 — Codex 수정 재확인 반영의 Linux 실행 증거 (2026-10-15 · 결과 0 건 · LIGGGHTS 없음)

> 무엇: Codex 수정 재확인 판정 (codex_review_dem_unloading_kit_fix_recheck_20261015.md · 코드 핀 `eaecfba2a` · HOLD) 의 `ULKRF-01` · `02` · `03` 과 수정 계획
> (dem_unloading_kit_fix_recheck_fix_plan_20261015.md · ✅ 1저자 10-15 Q1–Q4 권고대로) Q2 (문구) · Q3 (문법 사전 점검 원자료 재판독) · Q4 (비차단 셋) 를 고친 뒤의
> 모의 러너 · 문법 · 포장 시험 **전체 로그와 rc** (13 명령 · 앞선 증거 `../dem_unloading_kit_reverify_fix_evidence_20261014/` 와 같은 꼴).
> ⚠ 자기시험 · 모의 러너 · 합성 자료다 — 실제 LIGGGHTS 바이너리 실행 (README §1-6 문법 fixture 실행 2 · ibb) 이나 실제 원자료 판독을 대신하지 않는다.

## 1. 환경

| 항목 | 값 |
|---|---|
| OS | Linux (`Linux-6.18.44-fc-v114-x86_64-with-glibc2.39` · 클라우드 컨테이너) |
| Python | 3.11.15 (모든 명령 `python3 -I` — 표준 라이브러리만 · ul_s3 F1 의 봉인 대조만 numpy) |
| Bash | GNU bash 5.2.21(1)-release (x86_64-pc-linux-gnu) — 러너 모의 (`run_unload.sh` · `run_history.sh` · `run_unload_ibb.sbatch`) 가 실제로 돈다 |
| LIGGGHTS · MPI · SLURM | 없음 — 가짜 `mpirun` · `lmp` (시험 쪽 스크립트 · 운영 코드 우회 없음) |
| 실행 폴더 | 키트 폴더 `docs/data/ps45_unload_20261009/` (cwd) · 각 명령의 화면 전체 = `<묶음>/<이름>.log` (머리에 명령 · rc · 시간) · 요약 = `<묶음>/summary.json` |
| 도구 | `tools/run_suite.py` — 앞선 증거의 같은 이름 도구와 명령 13 · 로그 꼴 같음 · 다른 점 = 커밋 번호를 적지 않고 키트 폴더 git tree (내용 해시) 와 깨끗함만 적는다 (`SELF-116`) |

## 2. 묶음 둘

| 폴더 | 코드 상태 | 봉인 (sha256) | 무엇 |
|---|---|---|---|
| `tests_first/` | 본 가지 시험 먼저 커밋 `1c0b9fd65` 의 키트 폴더 (메인 세션 대조 10-15: `kit_git_tree` = `git rev-parse 1c0b9fd65:docs/data/ps45_unload_20261009`) — 새 시험만 더함 · 키트 코드 = 수정 전 · 키트 폴더 깨끗 | 키트 `SHA256SUMS` `65f919e9c9cd8528f702b1cb7c0fc32b784065c7b9e91110ce05f24788c225e8` · `history_test/SHA256SUMS` `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d` | 시험 먼저 — 새 시험이 고치기 전 코드에서 **의도한 이유로** 실패 (§4) |
| `final/` | 이 증거가 든 본 가지 커밋의 키트 폴더 (= 수정 `22a347722` + 키트 README · 메인 세션 대조 10-15: `kit_git_tree` = 그 커밋의 `docs/data/ps45_unload_20261009` tree) — 수정 + 키트 README (이 증거와 같은 커밋) · 키트 폴더 깨끗 | 키트 `SHA256SUMS` `441f66d71873faf2541f3d3945e82cb2b8045425eaa3b2c5bb63213327556c34` · `history_test/SHA256SUMS` `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d` (이력 시험 폴더 바이트 그대로) · 키트 README sha256 `82d8f75fd108d028f3cb228aa466e575bfe728e238fc455092e9fcef1329c592` | 최종 — 13 명령 전부 rc 0 |

- 작업 트리 커밋 번호는 적지 않는다 (`SELF-116` — 작업 트리 판은 cherry-pick 뒤 바뀐다) · 본 가지 번호 = 메인 세션이 위 표에 적었다.  대응 확인 = 각 `summary.json` 의 `kit_git_tree` (키트 폴더 git tree · 내용 해시) 가 본 가지의 같은 단계
  커밋에서 `git rev-parse <커밋>:docs/data/ps45_unload_20261009` 와 같은지 · 위 봉인 sha256 이 같은지.
- 작업 시작 판 (수정 가지 기준) 도 같은 13 명령 전부 rc 0 (ul_reader 158 · ul_gates 37 · ul_lib 21 · ul_runner_test 37 — 커밋하지 않은 확인 실행).

## 3. 명령 · rc · 검사 수 (✓ 줄 수 / 전체 · 시험 먼저 → 최종)

| 명령 (`python3 -I …`) | 시험 먼저 | 최종 |
|---|---|---|
| `ul_lib.py --selftest` | rc 1 · 22/24 (L14 ×2 — 정수 토큰 2^53 + 1 · 쌍 참조 정수 가림) | rc 0 · 24/24 |
| `ul_s3.py --selftest` | rc 0 · 16/16 | rc 0 · 16/16 |
| `ul_observers.py --selftest` | rc 0 · 21/21 | rc 0 · 21/21 |
| `ul_gates.py --selftest` | rc 1 · 37/41 (C4 ×4 — G2c `c_cpl[7]` · `[8]` 결손 양쪽 = `KeyError`) | rc 0 · 41/41 |
| `ul_reader.py --selftest` | rc 1 · 164/182 (18 실패 — R33 3 · R34 1 · R35 5 · R36 9 · 양성 대조 R33 둘 · R34 넷 · 옛 시험 158 은 통과) | rc 0 · 182/182 |
| `seal_kit.py --selftest` | rc 0 · 12 ✓ | rc 0 · 12 ✓ |
| `seal_kit.py --check` | rc 0 · 76 파일 · 규칙 24 · 폐기 0 | rc 0 · 76 파일 · 규칙 24 · 폐기 0 |
| `make_unload_decks.py --selftest` | rc 0 · 291/291 | rc 0 · 291/291 |
| `make_unload_decks.py --check` | rc 0 · 덱 64 = 생성 결과 | rc 0 · 덱 64 = 생성 결과 |
| `history_test/make_history_decks.py --selftest` | rc 0 · 172 ✓ | rc 0 · 172 ✓ |
| `history_test/make_history_decks.py --check` | rc 0 · 덱 9 · 15 파일 | rc 0 · 덱 9 · 15 파일 |
| `history_test/read_history.py --selftest` (러너 모의 · 보고 묶음 포함) | rc 0 · 56/56 | rc 0 · 56/56 |
| `ul_runner_test.py --selftest` (모의 러너 전체 · 실제 `run_unload.sh` · `run_unload_ibb.sbatch` · 보고 묶음 M19) | rc 1 · 37/38 (M25 — 판정 뒤 GA 화면 ERROR 인데 RJ 진행) | rc 0 · 38/38 |

- "✓ 줄 수" = 화면의 `✓` 로 시작하는 줄 수 (세는 방식 = `tools/run_suite.py`) · rc 는 프로세스 종료 코드 그대로.
- 생산 덱 64 · `unload_params.json` · 이력 시험 폴더 (덱 아홉 · 판 STL · 표 · 생성기 · 판독기 · 러너) = 바이트 그대로 (`make_unload_decks.py --check` · `history_test/SHA256SUMS` 같음).

## 4. 고치기 전 실패가 의도한 이유인가 (발췌 · 전문 = `tests_first/*.log`)

| 시험 | 고치기 전 관측 (그 로그 그대로) |
|---|---|
| R33 `ULKRF-01` (Codex `one_auth_two_rollbacks` · `duplicate_event_only` · 같은 step 다른 k) | 셋 다 주 값 OK · UVa 허용 (같은 RESUME 두 줄 = 승인 둘 · 되감기 두 번) · 대조 둘 (진짜 이어 돌림 한 번 = 승인 하나 · 남긴 줄 3 / 같은 묶음 둘에 RESUME 한 줄 = 거부) 은 통과 |
| R34 `ULKRF-02` (Codex `resume_completed_hold_5_windows`) | 생성 UT 덱 제어 흐름 4 → 5 창 = 단 기록 k [0, 1, 2, 2, 3, 4] 미식별 · UVa 거부 · 대조 (덱 흐름 S1 [0, 0, 0, 1, 1] · 새 시도 단독 · 4 → 4 · 5 → 4 · 무승인) 는 통과 |
| R35 · C4 `ULKRF-03` (Codex `g2c_c_cpl7_missing` · `g2c_c_cpl8_missing` · `g2c_missing_column_actual_cli`) | `KeyError: 'c_cpl[7]'` · `KeyError: 'c_cpl[8]'` (함수 · 복원 판정) · 실제 restore CLI = rc 1 (Traceback) · 증서 없음 |
| R36 · M25 Q3 (Codex `grammar_provenance` 캐시 신뢰 경계 넷 · `different_reader_runner_seal`) | 판정 JSON 그대로 · GA 화면 ERROR · GB mesh z 99 · GB 화면 지움 · GB 상태 값 0 = 사전 점검 허용 (승인된 판독기로 다시 읽으면 넷 다 FAIL) · kit 사본 판독기 · 표 고침 · 없음 = 허용 · `GRAMMAR_READER` 없음 (`NameError`) · 실제 러너 M25 = RJ 진행 (LIGGGHTS 호출) |
| L14 Q4 | 원자 덤프 `9007199254740993` → `9007199254740992.0` 으로 읽혀 `exact_id` 통과 · 쌍 참조도 같음 · `2.0000000000000001` = 파서 문제 없음 |

- 시험 쪽 바꾼 것: R32 · R36 의 문법 런 fixture = 승인된 판독기 자신의 합성기 (`read_history.synth_gram_run`) 로 단계 원자료를 만들고 kit 사본에 판독기 · 표를 바이트 그대로 둔다
  (옛 fixture 에는 원자료가 없어 재판독 양성이 설 수 없었다 · 옛 R32 19 반례 · 양성 = 새 fixture 에서도 고치기 전 · 뒤 같은 결과) · `_w` = LF 고정 쓰기 (Q4 — Windows R32 fixture) ·
  `_resume_layout` = 묶음 수 · RESUME 줄 수 · 중복 · 상충 인자 (기본값 = 옛 꼴 그대로).

## 5. 다시 돌리기

```bash
# 리포 루트 · 리뷰 핀 체크아웃 뒤 (Linux · bash · python3)
python3 docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/tools/run_suite.py docs/data/ps45_unload_20261009 /tmp/ulkrf_suite
```
