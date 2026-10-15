# DEM 언로딩 키트 — ibb 문법 fixture 런 넷 반입 (실행 1 · 1b · 실행 2 · 반복) (2026-10-15 · 1저자 업로드)

> 무엇: 키트 README `docs/data/ps45_unload_20261009/README.md` §1-6 의 문법 fixture (P → GA → GB · 짧은 문법 런 · **물리 검증 아님** · C19) 를 ibb 에서 돌린 보고 묶음 넷 + SLURM 화면 여섯.
> 결론: **실행 2 = PASS (19/19)** — 판독기 · 표 · 덱 · 판 STL = 봉인 값 · 같은 LIGGGHTS 바이너리 · 우리 트리 판독기로 **원래 자리** 재판독 = 런의 판정 JSON 과 19/19 같음 · 같은 판정을 Codex 가 받은 현재 판 (`44a034534`) 에서 한 번 더 (반복) 냈다.
> ⚠ 이 반입은 `ULKRR-01` (= `SELF-115`) 의 남은 "실행" 증거다 — 닫는 판정은 Codex (짧은 재확인 2 · `docs/reviews/codex_dem_unloading_kit_fix_recheck2_request_20261015.md` §7).  본 R · 10:0 연장 · U 의 GO 아님.

## 1. 받은 파일 (`raw/` · 바이트 그대로 · `raw/SHA256SUMS.received`)

| 파일 | 바이트 | sha256 | SLURM 화면의 "보낼 것" sha256 |
|---|---:|---|---|
| `gram_20261014_192604.report.tgz` | 15,393 | `015bd82ba266a3438db003a0e6cf025d4ad38ac51133ab75307be402c60ca7ee` | 같음 (job 285220) |
| `gram_20261014_194645.report.tgz` | 15,048 | `8e1ddb7d92bb2d3eac8c9ed2e008e1c5a3b79ceb0191de327b21620d9503dee3` | 같음 (job 285228) |
| `gram_20261015_030225.report.tgz` | 32,067 | `f47a4cea6a4c2de1b3300bab8d6b620fcb98106ee418691a3d05da46f7c677fc` | 같음 (job 285533) |
| `gram_20261015_122956.report.tgz` | 30,369 | `35bce900f2ea656ac85e90fb0ef2ff4cdb32e44ca08a5c870bc8e9df7d88da93` | 같음 (job 286802) |
| `ulHist_281180.zip` (1저자가 묶은 SLURM 화면 여섯) | — | `ff5acca99fae137360e7ff59391a0acb8fab7e81042def71123e78b5a3f97403` | — |

- 화면 여섯 = `ulHist_281180` (10-13 17:04 · H0–H5 첫 런 · 판 `dfd89b96` · rc 2) · `283122` (10-14 09:47 · H0–H5 PASS · 묶음 `be0acbd7…` = `docs/reviews/dem_unloading_history_test_20261014/`) · `285220` · `285228` · `285533` · `286802` (아래 표).
- 처리: 새 빈 폴더에 복사 → sha256 → tar · zip 목록 (절대 경로 · `..` · 링크 0) → 풀기.  묶음 안 `kit_<시각>/` 은 `SHA256SUMS` 하나뿐 (스크립트 없음) · 묶음 안 어떤 것도 실행하지 않았다.

## 2. 런 넷 (`runs_summary.json` · 각 묶음의 `run_manifest.txt` · `grammar_verdict.json` · 단계 `rc` · 덱 사본 sha256)

| 런 | job · 노드 · 시각 (KST) | 판 (`repo_head` · dirty 0) | history_test 봉인 (`sums_sha256`) | 판독기 (`read_history.py`) | 덱 사본 | 단계 rc | 판정 |
|---|---|---|---|---|---|---|---|
| 실행 1 `gram_20261014_192604` | 285220 · node04 · 10-14 19:26 | `a30fe150e` | `debe8387…` (첫 판) | `18521ae7…` (봉인 아님) | 문법 덱 ≠ 봉인 (고치기 전) | P 0 · GA 1 | **FAIL** (rc 2) — `SELF-115` (Mismatched fix) |
| 실행 1b `gram_20261014_194645` | 285228 · node04 · 10-14 19:46 | `a30fe150e` (같은 판) | `debe8387…` | `18521ae7…` | 실행 1 과 같음 | P 0 · GA 1 | **FAIL** (rc 2) — 같은 결함 · 같은 판 반복 (이 반입으로 처음 기록) |
| **실행 2** `gram_20261015_030225` | 285533 · node02 · 10-15 03:02 | `799459c85` | `8ff722d2…` (= 지금) | `70f741a9…` (= `ul_reader.GRAMMAR_READER`) | P · GA · GB 사본 = 봉인 (`GRAMMAR_INPUTS`) | P 0 · GA 0 · GB 0 | **PASS** (rc 0 · 19/19) |
| 반복 `gram_20261015_122956` | 286802 · node04 · 10-15 12:29 | `44a034534` | `8ff722d2…` | `70f741a9…` | 봉인 | P 0 · GA 0 · GB 0 | **PASS** (rc 0 · 19/19) |

- LIGGGHTS 바이너리 sha256 = 넷 모두 `ee2d77261bac…` (러너 사전 점검 = 등록 §11-1 ⓖ 빌드).  표 `history_params.json` = 넷 모두 봉인 값 `7a5279f0…`.
- 실행 2 판 `799459c85` 와 반복 판 `44a034534` 사이에 `history_test/` 바이트 변화 없음 (봉인 `8ff722d2…` 같음) — 덱 · 판독기 · 표 · 러너 같다.

## 3. 우리 트리 판독기로 다시 읽기 (`reread/`)

판독기 = 리포 `docs/data/ps45_unload_20261009/history_test/read_history.py` (sha256 `70f741a9…` = 런의 kit 사본에 적힌 값 · `ul_reader.GRAMMAR_READER`) · `--grammar --params history_params.json` · 묶음 원자료만 읽음.

| 런 | 원래 자리 (`*_inplace.*`) | 옮긴 사본 (`*_relocated.*`) |
|---|---|---|
| 실행 2 | **PASS · rc 0 · 검사 19 = 런 JSON 과 같음** | FAIL — `GA_args` · `GB_args` 만 거짓 (나머지 17 참) |
| 반복 | **PASS · rc 0 · 검사 19 = 런 JSON 과 같음** | 같음 (`GA_args` · `GB_args` 만) |
| 실행 1 · 1b | FAIL — `GA_tech` (`ERROR: Mismatched fix in variable formula (../variable.cpp:1315)`) · 뒤따르는 GA 칸 · `GB_exists` | — |

- **원래 자리** = 컨테이너 안에 런의 절대 경로 (`/home/yonghoon/ps45_unload_hist_20261013/<런>/`) 를 새로 만들어 묶음을 풀고 읽은 뒤 그 폴더를 지웠다 — GA · GB 입력 기록 (`ckpt.txt` · `vars.txt`) 이 절대 경로라서 (키트 README §1-6 · Q3).  옮긴 사본의 `GA_args` · `GB_args` 거짓은 **설계대로** (본 R 사전 점검이 런 폴더를 원래 자리에서 다시 읽는 이유).  옮긴 사본 출력의 컨테이너 경로는 `<옮긴 사본>/` 로 바꿔 적었다 (그 밖 바이트 그대로).
- 이것은 묶음 원자료의 재판독이다 — 본 R 사전 점검 (`ul_reader.grammar_prereq`) 은 ibb 에서 그 런의 `kit_<시각>/` 사본 판독기로 원래 자리에서 다시 읽는다 (묶음에는 kit 스크립트가 없어 여기서 그대로 재현하지 않는다).

## 4. 다음

- **본 R · RJ2 · EXT 의 `GRAMMAR_VERDICT` = 실행 2** (✅ 1저자 10-15) `~/ps45_unload_hist_20261013/gram_20261015_030225/grammar_verdict.json` (첫 PASS · 이름으로 고정) — 반복 (`gram_20261015_122956`) 도 같은 판정.  두 런 폴더 · `kit_<시각>/` 은 ibb 에서 옮기거나 지우지 않는다.
- Codex 짧은 재확인 2 — 요청서 §7 에 이 반입을 붙였다 (리뷰 핀 = 그 요청서가 든 본 가지 커밋).
- ⛔ 본 R · 10:0 연장 · U = 재확인 GO 뒤 (이 PASS 만으로 GO 아님).
