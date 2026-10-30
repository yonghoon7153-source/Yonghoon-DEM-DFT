# 반입 — Codex 믹서 D3 유한 후보 판독기 독립 재검토 (10-27 · 범위 한정 GO)

- 받은 것: 1저자 10-27 23:35 수령 · 10-30 다시 업로드 `codex_mixer_d3_independent_review_20261027.zip` → `received_codex_mixer_d3_independent_review_20261027.zip` (3,396,181 B · sha256 `be424232a8fc79ff9bacd00b7c3ba392b4e92f8cd0fe8532ec0e257786929924` · 항목 419 · 중복 0 · 대소문자 중복 0 · 절대 · `..` 경로 0 · 링크 0 · 암호 0 · CRC 이상 0).  10-27 첫 업로드 (14:45 UTC = 23:45 KST) 와 바이트 같음.
- ⚠ 시각: 판정문은 10-27 23:35 에 받았고 그날 밤 메인 세션에서 재현했지만 **반입은 10-30 까지 빠졌다** (이번이 그 반입 · 재현은 10-30 에 `_repro_ours_20261030/` 로 다시 했다).
- 리뷰 대상: 핀 `e0daf7b234bcc7935259d786e270268372abe2a2` (`codex/mixer-d3-design`) · 요청서 `docs/reviews/codex_mixer_d3_candidate_reader_request_20261024.md` · 대상 `scripts/mixer_d3_candidates.py` (sha256 `ea4528156e8eb9762999fef0643985bebf0b0735691202fddb4a2c17814ee7f8`) · 제출 ZIP `codex-mixer-d3-e0daf7b234bc-rebuilt-20261027.zip` (sha256 `6cf74df0…` · `intake.json`).
- 판정 (판정문 머리): **입력 조건부 유한 후보 판독기 범위 GO · 새 P1/P2/P3 없음.**  원자료에서 관측값을 추출하는 정확성 · 통계 폭의 정당성 · 사전등록 · 맹검 · 역사적 seed 미사용 · 장비 · DEM 실행 자격은 **승인하지 않는다** · 모든 출력 `execution_ready=false`.  Windows 에서 symlink 자기시험 1 개만 직접 재현 못 함 (WinError 1314 · 판정문 §5-1).
- 원장: **상태를 바꾼 항목 없음** — 요청서는 원장 ID 를 닫아 달라고 하지 않았고 (Q1–Q6 = 구현 질문), 원장에 MXD3 · 후보 판독기 항목이 없다 (요청서의 `D3IR-01` · `02` 는 내부 독립 검토 항목명 · 원장 밖).  `MXD2-07` (D3 설계 문서의 천장 수치 = gen1 값) 은 이 리뷰가 다루지 않았다 — open 그대로.

## 이 폴더에 푼 것 · 뺀 것

| 구분 | 파일 | 비고 |
|---|---|---|
| 반입 | `codex_review_mixer_d3_20261027.md` (판정문) · `README.md` (Codex · D2 묶음과 같은 바이트) · `MANIFEST.sha256` · `intake.json` · `evidence_manifest_verification.json` · `gate_pin_comparison.json` · `run_existing.py` | 묶음 뿌리 |
| 반입 | `d3/evidence/` 전체 80 파일 — `independent_probe.py` · `independent_results.json` · `selftest.log` · `selftest-workspace-temp.log` · `cli/` 38 · `cli-replay-asemvbv_/` 38 | 판정문이 인용하는 증거 (판정문 §6 "`cli/` 및 최신 `cli-replay-*`" · `cli-replay-asemvbv_/` = Codex 결과 JSON 의 `cli_directory` · 두 폴더의 입력 · 결과는 서로 바이트 같다) |
| 반입 | `d3/blob_verification.json` · `d3/snapshot/PIN.txt` | 신원 기록 (PIN.txt = 제출 ZIP 의 핀 메모 · 핀 blob 아님) |
| 뺀 것 (ZIP 안 그대로) | `d3/snapshot/` 의 리포 파일 328 | 핀 `e0daf7b23` git blob 과 328/328 같음 · 우리 기반 `4c69070ad` 트리와도 328/328 같음 |
| 뺀 것 | `d3/tree.json` · `d3/gate_candidate_tree.json` (9.8 MB) | GitHub 트리 목록 — `git ls-tree -r` (핀 13,791 · 후보 `9c2f7b47f` 13,741 항목) 과 동일 |

- 반입 88 파일 = Codex `MANIFEST.sha256` 항목과 88/88 같음 (MANIFEST 자신 제외) · 나머지 330 항목은 받은 ZIP 안.
- 개행: 24 파일이 CR 바이트 (Windows) — `.gitattributes` = `* -text` 로 바이트 그대로 커밋한다.

## 대조 (`_repro_ours_20261030/verification.json`)

| 무엇 | 결과 |
|---|---|
| ZIP 안전 목록 | 419 항목 · 중복 0 · 대소문자 중복 0 · 경로 이탈 0 · 링크 0 · CRC 이상 0 |
| Codex `MANIFEST.sha256` (풀린 바이트) | 418/418 · 목록 밖 파일 0 |
| `d3/snapshot/` ↔ 핀 git blob | 329 = 리포 파일 328 + `PIN.txt` · blob id 328/328 · `git cat-file --batch` 원 바이트 328/328 · 핀 blob = 우리 기반 트리 328/328 |
| 게이트 후보 `9c2f7b47f` ↔ 핀 `git diff` | 54 파일 · `scripts/ webapp/ dem_scripts/ .github/` 0 = Codex `gate_pin_comparison.json` 과 같음 |

## 우리 트리 재현 (`_repro_ours_20261030/`)

이 컨테이너 · Linux · Python 3.11.15 · `python3 -I -X utf8 -B` · 새 빈 폴더 · 판독기 · 시험 = **우리 기반 `4c69070ad` 의 같은 경로 328 파일** (Codex snapshot 과 바이트 같음).  도구 = `../codex_mixer_d2_review_20261027/_repro_ours_20261030/tools/` (D2 와 같은 벌).

| 무엇 | 결과 | 파일 |
|---|---|---|
| Codex `d3/evidence/independent_probe.py` | rc 0 (5 s) · 명명 검사 **27/27** 통과 · 전수 반복 보정 4,096 + 검증 4,096 조합 (이 둘은 27 안의 한 검사 · 합산하지 않음) | `independent_results.json` · `probe_stdout.json` |
| 결과 JSON ↔ Codex | 27 검사 이름 · 통과 · 세부값 같음 · 판독기 sha256 같음 · **8,192 출력 전체의 `oracle_output_hash` `a3b776987b916e4944357b67ad40da5d687c83e814a80a17a1f0c9e9da329f6b` 같음** · 다른 칸 = `cli_directory` (탐침이 `tempfile.mkdtemp` 로 만든 무작위 폴더 이름) · `python` (해석기 문자열) 뿐 | `independent_results_compare.json` |
| CLI 7 입력 ↔ Codex 두 폴더 | 계약 · 관측 · 출처 · `result.json` 바이트 같음 · 로그 같음 (개행 · 경로 가린 뒤) · rc: 정상 · 빈 S · 검증 누락 0 / 출처 변조 · 계약 digest 불일치 · 중복 키 · `../` 탈출 2 · 정상 셋을 같은 출력 경로로 다시 부르면 rc 2 · 기존 결과 바이트 그대로 = 판정문 §4 표 | `cli_compare.txt` |
| 저자 시험 `test_mixer_d3_candidates.py` 수정 없이 | **28/28 OK** — Windows 에서 환경오류였던 `test_artifact_path_escape_and_symlink_refused` 가 Linux 에서 실제로 돌고 통과 (이 환경 `os.O_NOFOLLOW` 있음) · Codex Windows 27 통과 + 1 환경오류 | `author_test_d3_candidates.log` |

- ⚠ 우리 `independent_results.json` 의 `"symlink_execution": "NOT_TESTED: Windows privilege unavailable; …"` 는 탐침 코드에 박힌 **고정 문자열**이라 Linux 실행에서도 그대로 찍힌다 — 우리 실행의 측정값이 아니다.  symlink 거부의 실제 Linux 확인은 위 저자 시험 행이다.

## 한정

- GO 범위 = **입력 조건부 유한 후보 판독기 구현** — 관측값 추출 · 통계 폭 · 사전등록 · 맹검 · seed 역사 · 물리 · 실행 자격 아님 · rc 0 = 판독 · 기록의 정상 종료 (과학적 수용 · 실행 승인 아님 · 판정문 §4).
- symlink 동작을 모든 OS 에서 인증한 것은 아니다 — 우리 확인은 이 Linux 컨테이너 하나 (판정문 §5-2 의 한정은 그대로).
- 판정문 §5-5 (새 판독기 시험이 공유 게이트에 직접 배선되지 않음) 는 **핀 시점** 서술이다 — 우리 기반에서는 `c9027bda7` (10-27 · 비 Rint 대응표 §6 2) 이 `scripts/check_all.sh` · CI 에 `test_mixer_d3_candidates.py` · `test_mixer_d2_consumers.py` 를 배선했다 (참고 · 이 리뷰 판정 범위 밖).
- 반입 검사 = `check_review_findings.py` (스윕 없이) · `check_doc_refs.py` — `--ban-sweep` 은 1저자 50kg CPU 우선으로 이 반입에서 돌리지 않았다 (메인 게이트에서).
