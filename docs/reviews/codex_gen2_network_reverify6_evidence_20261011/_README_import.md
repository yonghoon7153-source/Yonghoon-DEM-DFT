# 재검증 6 증거 반입 (10-11) · 우리 트리 재현

정본 판정 = `docs/reviews/codex_review_gen2_network_reverify6_20261011.md` (리뷰 핀 `a20fc1875` · WSL 실행 핀 `956173e1c` · **새 P1 없음 · 194 · v1.3 HOLD 유지** · 남은 차단 = `G2RR6-01` P2 하나).
Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 파일 | sha256 | 리포 |
|---|---|---|---|
| 원 ZIP `codex_gen2_network_reverify6_20261011.zip` (1저자 PC · Codex 작업 공간) | 103.5 MB · 2,655 파일 | `3613bb4e8d64dc2c325c78ca17748ef45f36c6b0db7065dc9ae6ba9d17cd7c28` | 넣지 않음 (1저자 PC 에 보존) |
| 작은 ZIP `codex_r6_small.zip` (1저자가 대화 명령으로 줄임) | 5,035,113 B · 1,993 파일 + `_FULL_INVENTORY.json` | `bc787b0cffe51dd228996504b5eddacd8edbf6b25ee91b72ad2364259281672f` | 아래 표만 |

- `_FULL_INVENTORY.json` = 원 ZIP **2,655 파일 전부**의 경로 · 크기 · sha256 · 작은 ZIP 에 남겼는지 (`kept`).  빠진 파일도 이 목록으로 대조할 수 있다.
- 반입 파일 = Codex 묶음 sha256 표 (`PACKAGE_SHA256SUMS.json`) 대조 **68 / 68 같음** (판정문 포함 · 이 README · `_FULL_INVENTORY.json` · `_repro_ours_20261011/` 은 표 밖 = 우리 파일).

| 무엇 | 반입 | 빠진 것 |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_gen2_network_reverify6_20261011.md` | — |
| 묶음 README · `run_checks.py` · `package_review.py` · `prepare_source.py` · `complete_source.py` · `source_manifest.json` · `PACKAGE_SHA256SUMS.json` | 전부 | — |
| `evidence/` 맨 위 54 파일 (결과 JSON · `r6_s0b_*.input.json` 일곱 · 로그 · `runs_*.json`) | 전부 | — |
| `evidence/` 픽스처 폴더 여섯 (`packaged_fixture_check` 750 · `r5_observation_run2` 750 · `r5_observation_retry` 212 · `r5_release_contract` 101 · `r5_release_contract_complete` 102 · `r5_release_real_binding` 16 파일) | 폴더마다 `results.json` · `TEST_ONLY_NOT_GO.md` 만 | 나머지 = 목록만 (`_FULL_INVENTORY.json`) — 앞 라운드 합성 픽스처 복제 (실제 194 아님) |
| `source/` 493 파일 (59.2 MB) | — | 핀 `a20fc1875` 의 git blob 사본 — `source_manifest.json` 의 blob SHA-1 · SHA-256 으로 리포에서 다시 만든다 |
| `probes/` 12 · `fixtures/` 65 · `submitted/` 91 · `tree.json` | — | 작은 ZIP 에 없다 (원 ZIP 에만).  ⚠ Codex 탐침 코드 (`probes/`) 를 들이지 못했다 → 우리 재현 = §2 의 자체 구동기 (입력 = 반입한 `evidence/r6_s0b_*.input.json`) |

- 윈도 경로 (`C:\Users\…\Codex\…`) 는 Codex 작업 공간 경로 그대로다 (기록 · 비밀 아님).  `SUPABASE_KEY=False` 줄 = 웹앱 시작 배너 (값 없음).

## 2. 우리 트리 재현 (10-11 · HEAD `5f555bbd4` · 컨테이너 Linux · Python 3.11 · `git archive` 사본 · 작업트리 무변경)

| 구동기 (`_repro_ours_20261011/`) | 무엇을 | 결과 |
|---|---|---|
| `repro_s0b_cli.py` → `repro_s0b_cli_ours.json` | Codex 입력 일곱 (`evidence/r6_s0b_<label>.input.json` = smoke_report 꼴 · case15 보고만 변이) 을 **실제 `g2_network_reread.main(['--smoke-root', …])`** 에 · 정상 관통 · 미퍼콜 · clamp 게시 폴더 = 이 트리 실 생산자 게시 (`webapp/test_gen2_publication_handover._publish` — Codex 와 같은 방식) | 일곱 모두 rc / n_fail **Codex 와 같다** — positive 0/0 · `raw_sha_missing` 0/0 · `raw_sha_mismatch` 0/0 · `negative_area_positive` 0/0 · `negative_area_missing` 0/0 (**오수용 넷 재현**) · `raw_sha_flag_false` 1/1 · `actual_permission_error` 1/1 |
| `probe_same_class.py` → `probe_same_class_ours.json` | 같은 공용 판정 (`case15_negctl_s0b_problems`) 에 같은 부류 변이 23 (자체 점검 · 순수 함수 — 시험이 아니라 탐침) | **21 통과 (오수용)** (정정 `SELF-104` — 앞 판 "22 · 20" 은 음수 면적 11 을 10 으로 셌다) — raw_sha 8 (빈 dict · 키 하나 삭제 · 키 추가 · 두 값 함께 바꿈 · 16 진 아님 · 빈 문자열 · 원소 셋 · None) · 음수 면적 11 (양수 · 면적 결손 · 0 · NaN · bool · 문자열 · 군더더기 행 · 짧은 행 · ID 문자열 · ID 실수 절삭 · 다른 음수값) · nc1 실패 단계 하나 더 · nc2 등록 밖 τ 숫자 키.  거부 2 = 음수 면적 칸이 목록 아님 · 거부 문자열 앞뒤 덧붙임 (nc5 가 원자료 탐침 오류와 대조) |

- 재현 명령 (리포 루트에서 · 사본 `T` = `git archive HEAD scripts webapp` + `docs/data` 일부 (다시 읽기가 읽는 열 사전 · 수확 · union · 접촉 원천) 를 푼 폴더 · `E` = 이 폴더의 `evidence`):
  `python3 -I -B docs/reviews/codex_gen2_network_reverify6_evidence_20261011/_repro_ours_20261011/repro_s0b_cli.py T E out.json` (2.4 s) · 같은 꼴로 `probe_same_class.py`.
- 한정: 반례 판정 재현이다 — 194 생산 · S3 · DEM/MPM 이 아니다.  원 탐침 (Codex 묶음 probes 폴더의 r6_s0b_cli — 미반입) 과 같은 코드라는 주장도 아니다 (탐침 코드 미반입) — 같은 입력 · 같은 CLI 에서 같은 rc / n_fail.

## 3. 판정문 §6 포장 한계 — 다음 전달에 넣을 것

- 받은 tar (10-09) 에는 각 원 명령의 `rc=` 끝줄 · dirty / 버전 화면 · 사후 파일 목록 지문이 없다 (1저자 화면 = 대화) · `.before` 두 파일만으로 전후 무변경은 입증되지 않는다 — 사전 점검 README §3 에 한정 표지.
- 다음 WSL 명령 블록 = 명령마다 `rc` 파일 · 전후 지문 두 벌 (`.before` · `.after`) · `git status --porcelain` · 버전 화면을 묶음 안에 쓴다.

## 4. 읽는 순서

1. 판정문 §0 표 · §2 (G2RR6-01) · §7 (보충 20 — 두 배치 · 짧은 추가 검토의 최소 목록).
2. `evidence/r6_s0b_cli.json` (CLI 일곱) · `evidence/r6_s0b_*.input.json` (입력) → 우리 재현 `_repro_ours_20261011/repro_s0b_cli_ours.json`.
3. `evidence/r6_case15_positive.json` (실제 case15 7/7) · `evidence/r5_case15_pipeline_fault.json` (망 호출 PermissionError → nc5 TECH).
4. 배포 관문: `evidence/r5_release_contract_complete/results.json` · `evidence/r5_release_real_binding/results.json` (`TEST_ONLY_NOT_GO.md` = 관문 시험 입력 · 발사 승인서 아님).

## 5. 고친 뒤 (10-11 · 수정 커밋 `ec9c51149` · 1저자 Q1 (가))

| 구동기 | 고치기 전 (`5f555bbd4`) | 고친 뒤 (`ec9c51149`) |
|---|---|---|
| `repro_s0b_cli.py` → `repro_s0b_cli_fixed.json` | 일곱 = Codex 와 같음 (오수용 넷 rc 0) | 넷 **rc 1 · n_fail 1** · positive rc 0 · n_fail 0 그대로 · 대조 둘 rc 1 그대로 |
| `probe_same_class.py` → `probe_same_class_fixed.json` | 23 중 21 통과 · 2 거부 | **23 / 23 거부** |

- 시험: `g2_network_reread --selftest` 23/26 → 26/26 · `wsl_network_smoke --selftest` 16/16 · `--selftest-real` 4/4 (실제 case15 → `--smoke-root` rc 0).
