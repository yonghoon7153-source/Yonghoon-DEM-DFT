# 반입 — Codex 믹서 D2 개발 소비자 독립 재검토 (10-27 · HOLD)

- 받은 것: 1저자 10-27 23:35 수령 · 10-30 다시 업로드 `codex_mixer_d2_independent_review_20261027.zip` → `received_codex_mixer_d2_independent_review_20261027.zip` (8,817,665 B · sha256 `58e079578d318571340d03515ab6352a5551d0654ae1cb4e6554a10ea5a422dd` · 항목 799 · 중복 0 · 대소문자 중복 0 · 절대 · `..` 경로 0 · 링크 0 · 암호 0 · CRC 이상 0).  10-27 첫 업로드 (14:45 UTC = 23:45 KST) 와 바이트 같음.
- ⚠ 시각: 판정문은 10-27 23:35 에 받았고 그날 밤 메인 세션에서 재현했지만 **반입은 10-30 까지 빠졌다** (이번이 그 반입 · 재현은 10-30 에 이 폴더의 `_repro_ours_20261030/` 로 다시 했다).
- 리뷰 대상: 핀 `045e0b3098e8fe5a64d6eb0da310da776e68f995` (`codex/mixer-mxd2`) · 요청서 `docs/reviews/codex_mixer_d2_consumers_request_20261024.md` · 제출 ZIP `codex-mixer-mxd2-045e0b3098e8-rebuilt-20261027.zip` (sha256 `9aaaccd3…` · `intake.json`).
- 판정 (판정문 머리): **HOLD — MXD2-01 의 개발 소비자 하위 범위도 이 핀에서 종결하지 않는다.**  새 finding 셋 = P1 둘 (`MXD2R-01` 시간 · 삽입 · 회전 의미 · `MXD2R-02` SE–SE 접촉 제외) · P2 하나 (`MXD2R-03` 파일 바이트 ↔ 정규화 텍스트 해시).  **정상 덱의 산술 (밀도 세대 · 상별 계획수 · 인쇄 CED 로 SE Bo) 은 수용** — 정상 생성 덱이 잘못 실행됐다는 판정이 아니다.  LIGGGHTS · WSL · 스케줄러 · 물리 실행 0 회.
- 원장: `MXD2R-01` (P1) · `MXD2R-02` (P1) · `MXD2R-03` (P2) open · `MXD2-01` 은 open 그대로 + 메모 (개발 소비자 하위 범위가 이 리뷰로 닫히지 않음).  수정 계획 초안 `docs/reviews/mxd2r_fix_plan_20261030.md` (⬜ 1저자).

## 이 폴더에 푼 것 · 뺀 것

| 구분 | 파일 | 비고 |
|---|---|---|
| 반입 | `codex_review_mixer_d2_20261027.md` (판정문) · `README.md` (Codex) · `MANIFEST.sha256` · `intake.json` · `evidence_manifest_verification.json` · `gate_pin_comparison.json` · `run_existing.py` | 묶음 뿌리 |
| 반입 | `d2/evidence/` 전체 150 파일 (973 KB) — `independent_probe.py` · `independent_results.json` · `cases/` 11 사례 122 파일 · 처음 탐침 · 구 회귀 로그 · `legacy_windows_newline_diagnosis.json` · `legacy_ast_comparison.json` 등 | 판정문이 인용하는 증거 |
| 반입 | `d2/blob_verification.json` · `d2/dependency_fetch.json` · `d2/fixture_fetch.json` · `d2/legacy_fixture_fetch.json` · `d2/legacy_fixture_fetch_more.json` · `liggghts/manifest.json` · `d2/snapshot/PIN.txt` | 신원 기록 (PIN.txt = 제출 ZIP 의 핀 메모 · 핀 blob 아님) |
| 뺀 것 (ZIP 안 그대로) | `d2/snapshot/` 의 리포 파일 622 | 핀 `045e0b309` git blob 과 622/622 같음 · 우리 기반 `4c69070ad` 트리와도 622/622 같음 |
| 뺀 것 | `d2/baseline/` 3 (`mixer_deck_{readback,diff}.py` · `mixer_smoke_blind.py`) | 커밋 `486a57cf5` 의 blob 과 3/3 같음 |
| 뺀 것 | `d2/tree.json` · `d2/gate_candidate_tree.json` (10 MB) | GitHub 트리 목록 — `git ls-tree -r` (핀 14,019 · 후보 `34782a187` 13,994 항목) 과 동일 |
| 뺀 것 | `liggghts/src/*.cpp` 4 · `liggghts/doc/*.txt` 4 | 제3자 LIGGGHTS-PUBLIC 사본 (그 저장소의 3d5c00f · 이 리포 커밋 아님) — 스크래치의 LIGGGHTS-PUBLIC 클론 (HEAD 3d5c00f) 과 8/8 바이트 같음 · 판정문은 GitHub 링크로 인용 |

- 반입 163 파일 = Codex `MANIFEST.sha256` 항목과 163/163 같음 (MANIFEST 자신 제외).  나머지 635 항목은 받은 ZIP 안에 있다 — 이 폴더만으로 MANIFEST 전체를 대조하면 635 개가 "없음" 으로 나오는 것이 정상이다.
- 개행: Codex 산출 138 파일이 CR 바이트를 담는다 (Windows) — 이 폴더의 `.gitattributes` = `* -text` 로 **바이트 그대로** 커밋한다 (10-26 반입 선례 · `cases/crlf_*/` 의 CRLF 덱 자체가 MXD2R-03 의 증거라 정규화하면 반례가 사라진다).

## 대조 (`_repro_ours_20261030/verification.json`)

| 무엇 | 결과 |
|---|---|
| ZIP 안전 목록 | 799 항목 · 중복 0 · 대소문자 중복 0 · 경로 이탈 0 · 링크 0 · CRC 이상 0 |
| Codex `MANIFEST.sha256` (풀린 바이트) | 798/798 · 목록 밖 파일 0 · `liggghts/manifest.json` 8/8 |
| `d2/snapshot/` ↔ 핀 git blob | 623 = 리포 파일 622 + `PIN.txt` · blob id 622/622 · `git cat-file --batch` 원 바이트 622/622 · 핀 blob = 우리 기반 트리 622/622 (실행 비트 6 은 ZIP 이 버렸다 · 내용 무관) |
| `d2/baseline/` ↔ `486a57cf5` | 3/3 blob 같음 |
| 게이트 후보 `34782a187` ↔ 핀 `git diff` | 28 파일 · `scripts/ webapp/ dem_scripts/ .github/` 0 = Codex `gate_pin_comparison.json` 과 같음 |
| LIGGGHTS 인용 줄 (소스 읽기만) | `run.cpp` `upto` = 목표 누적 step − 현재 step · `fix_insert.cpp` `start` = 첫 삽입 step (현재 step 이전이면 오류) · 삽입은 예정 step 에서만 (`pre_exchange`) · `neigh_modify.txt` `exclude` = 그 쌍을 이웃 목록에서 빼 쌍 상호작용을 끈다 — 판정문 해석과 같다 |

## 우리 트리 재현 (`_repro_ours_20261030/`)

이 컨테이너 · Linux · Python 3.11.15 (numpy 2.4.6 · scipy 1.17.1) · `python3 -I -X utf8 -B` · 새 빈 폴더 · 소비자 = **우리 기반 `4c69070ad` 의 같은 경로 622 파일** (Codex snapshot 과 바이트 같음 · 핀 checkout · fetch 없음).

| 무엇 | 결과 | 파일 |
|---|---|---|
| Codex `d2/evidence/independent_probe.py` | rc 0 (9 s) · 명령 사례 9 (정상 1 · 공통 변조 6 · 음성 대조 2) 의 API · CLI 단언 전부 성립 · 정상 산술 48 조합 · CRLF 바이트 사례 2 = `[0,0,0]` / `[1,1,1]` · 명령 의미 산술 = 판정문 §3 (upto 증분 `[1, 560605, 0, 6034776]` · 최종 step 7,716,595 → 6,595,382 · 회전 1.5650841486 → 1.4320523448 s · 2.00008713 → 1.83008017 회전 · insA/B 제거 step 560,607 · 1,121,213) | `independent_results.json` · `probe_stdout.json` |
| 결과 JSON ↔ Codex | 판정 값 차이 **0** (경로 · 시각 칸도 없다) | `independent_results_compare.json` |
| 사례 폴더 122 파일 ↔ Codex | 덱 등 26 바이트 같음 · JSON 63 파싱 같음 (Codex 쪽 Windows CRLF 만 다름) · 로그 33 같음 (개행 · 절대 경로 가린 뒤) | `cases_compare.json` |
| 판정문 명령 그대로 (세 CLI · `--json` 없이) · **Codex 가 보낸 사례 파일** | `run_upto` 0/0/0 · `late_timestep` 0/0/0 · `insert_start_late` 0/0/0 · `front_period` 0/0/0 · `exclude_SE_SE` 0/0/0 · `crlf_lf_metadata` 0/0/0 · `crlf_crlf_metadata` 1/1/1 (`metadata SHA256 != actual deck`) · 대조: `normal` 0/0/0 · `friction_missing` 0/0/0 · 음성 대조 둘 1/1/1 (중력 · 적분기) | `cli_rc_codex_received_cases.json` · `cli_logs_codex_received_cases.txt` |
| 같은 명령 · **우리가 다시 만든 사례 파일** | 위와 rc 같음 · 덱 바이트 11 사례 모두 같음 | `cli_rc_our_regenerated_cases.json` |
| CRLF 값 | 실제 CRLF 덱 13,833 B · `0b92f856e224d0537b36b2c4fb2cc257e23cfbdea9528c478ef42d0dda63f015` ↔ 메타의 LF 13,654 B · `32033f6b0e17f33ecfe70121eaee393aa6c2748151f54b073243b916c6080644` = 판정문 §5 표와 같음 | `independent_results.json` (`byte_cases`) |
| (추가) 저자 시험 `test_mixer_d2_consumers.py` 수정 없이 | 13/13 OK (Codex Windows 13/13 · 우리는 `run_existing.py` 없이 그대로) | `author_test_d2_consumers.log` |
| (추가) 구 자체시험 (Codex 가 Windows 에서 다 못 확인한 것) | `mixer_deck_readback --selftest` 24/24 · `mixer_deck_diff --selftest` 55/55 · `mixer_smoke_blind --selftest` rc 0 (항목 30 ✓ · "전부 통과") — 이 Linux 결과일 뿐이다.  Codex Windows 의 diff 54/55 (고정물 개행 · 판정문이 따로 확인) · smoke 10 실패 (판정문: POSIX 파일 모드 · 등록 고정물 경로 영향 포함 · 전부에 대한 판정은 하지 않음) 와 다른 환경의 수치다 | `legacy_selftests_linux/` |

- 쓴 도구 = `_repro_ours_20261030/tools/` (안전 목록 · MANIFEST · snapshot↔핀 blob · 재현 트리 · 깊은 대조 · CLI 실행 · 반입 · 검증 요약).  Codex 탐침은 고치지 않고 그대로 돌렸다.

## 한정

- 합성 덱 · 소비자 판정 경로만 — LIGGGHTS · DEM · 스케줄러 실행 0.  시간 · 삽입 · 회전 · 접촉 제외의 실제 효과는 **소스 읽기 해석**이다 (판정문도 같은 한정).
- 반례 PASS 의 재현 = 현행 소비자 결함의 재현이지 제품 수용 PASS 가 아니다 — 고친 뒤에는 탐침의 반례 기대값을 거부로 바꾼 회귀를 둔다 (Codex README).
- 우리 재현은 우리 기반 트리의 같은 바이트로 했다 — 리뷰 핀 자체는 checkout 하지 않았다 (blob 대조로 같음을 확인).
- (추가) 행의 Linux 통과는 이 핀 코드의 Linux 결과일 뿐 전체 게이트 실행이 아니다 · Codex 의 시험 수와 합산하지 않는다.
- 새 S1 셀 · 코호트 · 정책 · 실물 입력은 이 리뷰 범위 밖 · 미완료 그대로 (판정문 §2 마지막 행).
- 반입 검사 = `check_review_findings.py` (스윕 없이) · `check_doc_refs.py` — `--ban-sweep` 은 1저자 50kg CPU 우선으로 이 반입에서 돌리지 않았다 (메인 게이트에서).
