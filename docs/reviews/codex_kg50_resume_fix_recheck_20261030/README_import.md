# 반입 — Codex KG50 재개 도구 고침 재확인 (10-30 · 부분 수용 · HOLD)

- 받은 것: 1저자 10-30 업로드 `codex_kg50_resume_fix_recheck_bf8cf21c_20261030.zip` → `received_codex_kg50_resume_fix_recheck_bf8cf21c_20261030.zip` (2,593,275 B · sha256 `5f98f9977e74fe2640c0f34e5c4e5918b970fdf4288c833b2f1b683e906c7a91` · 항목 643 · 중복 0 · 대소문자 중복 0 · 경로 이탈 · 링크 0).
- 이 폴더에 푼 것: 판정문 `codex_review_kg50_resume_fix_recheck_20261030.md` · Codex README · MANIFEST · PIN · intake · `reproduce.py` · 신원 · 셸 탐침 · 포장 검사 · `resume_independent.diff` · `independent/{program,launch,q5}/` 의 REPORT · results · 탐침 스크립트.  뺀 것 (ZIP 안에 그대로): `repo/` (282 파일 = 리뷰 핀 `bf8cf21c6` git blob 과 282/282 같음 · 메인 대조) · `baseline/resume_ckpt.sh` (= `f118c1fd1` 의 도구와 바이트 같음) · `independent/*/cases` 등 큰 고정물.
- 판정: 부분 수용 · 자동 시험 · 본 제출 경로 HOLD · P1 둘 (`KG50RF-01` 준비 구간 소비 값 · `KG50RF-02` 검사한 덱 ↔ 러너 실행 덱) · P2 하나 (`KG50RF-03` Q5 로그 출처) · P3 문서 하나 · 원장 ID = `KG50R-F01`–`F04` (원장 ID 형식 `^[A-Z][A-Z0-9]{0,4}-…` 때문에 접두를 `KG50R` 로).

## 우리 트리 재현 (`_repro_ours_20261030/`)

| 무엇 | 결과 | 파일 |
|---|---|---|
| Codex `reproduce.py` (`python3 -I -B` · 새 빈 폴더 · 이 컨테이너 Python 3.11.15) | rc 0 · `observations_reproduced` true · 입력 43 · Q5 가지 11 · 등록 본문 8 같음 · W2 변이 5 거부 · 새 발견 셋 · 원본 282 파일 무변경 | `reproduce_py_run.log` · `run_receipt.json` |
| 실제 bash `bash scripts/resume_ckpt.sh -C` (Codex 가 이 환경에서 못 돌린 길) · 여섯 경우 | 전부 rc 0 — 반례 넷 (D2 중력 중간 정의 삭제 · D2 즉시 평가 실행 상태 식 · 합성 timestep 삭제 · 합성 즉시 평가) 이 통과 = `KG50R-F01` 재현 · 기준 둘 (받은 D2 · 보관 after_settling) 통과 | `bash_C_six_cases.txt` |
| 실제 bash 로 도구의 러너 관문 줄 (`resume_ckpt.sh` 1151 행) 그대로 · 받은 D2 helper 러너의 `-in` 끝에 `.bak` | 관문 PASS · 시험 러너 = 자동 치환으로 `…r56t.liggghts.bak` = `KG50R-F02` 재현 | `rf02_runner_bak.sh` · `rf02_trial_runner_bak.sh` |

- 한정: 가짜 · 합성 · Codex 고정물 · 이 컨테이너뿐 — 실제 ibb · SLURM · LIGGGHTS 실행 아님 · 러너 반례는 관문 조건의 실제 bash 평가이지 실제 sbatch 제출 관측이 아니다.
- 수정 계획 = `docs/50kg/kg50_resume_fixrecheck_plan_20261030.md` (✅ 1저자 10-30 Q1–Q4 *"권고대로"*).
- 개행: 이 폴더의 JSON · 일부 스크립트는 커밋 때 CRLF → LF 로 정규화됐다 (git 속성) — 바이트 원본 = 같은 폴더의 received_*.zip · Codex MANIFEST.sha256 은 ZIP 안 원본 바이트 기준.
