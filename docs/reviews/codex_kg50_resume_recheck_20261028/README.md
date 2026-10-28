# Codex KG50 재개 도구 재검토 (10-28) — 반입

- 판정문: `codex_review_kg50_resume_recheck_20261028.md` (Codex 원문 그대로) — **자동 본 제출 HOLD · 새 P1 넷 (KG50R-01–04) · P2 하나 (05) · 문서 P3 하나 (06)**.
- 리뷰 핀 `f118c1fd1e3eb1a558299663dcee6a0bf83b9942` · 검토 입력 = 요청서 `docs/reviews/codex_kg50_resume_tool_recheck_request_20261027.md` 의 ZIP (Codex 계산 sha256 `0c073ccf…` · `intake.json`).
- 받은 ZIP = `received_codex_kg50_resume_recheck_20261028.zip` (1,255,343 B · sha256 `dcfb42e09316cd0f90fc768dabc23539dd3238b840f7321250d926d362f21c9c` · 1저자 10-28 18시 업로드) · 바이트 그대로.

## 이 폴더

| 자리 | 무엇 |
|---|---|
| `codex_review_kg50_resume_recheck_20261028.md` | 판정문 (§1 기존 항목 닫힘 · §2–§7 KG50R-01–06 · §8 Q1–Q9 · §9 상태 증거 경계 · §10 최소 해제 목록) |
| `FINAL_QA.json` · `PIN.txt` · `intake.json` · `remote_identity.json` · `REPRODUCE.md` · `PACKAGE_MANIFEST.sha256` | Codex 신원 · 재현 안내 · 묶음 체크섬 (157 파일) |
| `independent/` | Codex 독립 탐침 · 고정물 · 결과 (임시 ID: DECK-01/02/03 = KG50R-01/02/03 · SCHED-01 = KG50R-04 · SCHED-02 = KG50R-05 · scope "새 문서 충돌" = KG50R-06) |
| `_repro_ours_20261028/` | 우리 트리 재현 (Codex 가 못 돌린 Bash 경로 포함) · r075 소급 산술 |
| `received_…zip` | 받은 원본 |

- ⚠ 받은 ZIP 의 `repo/` (42 파일) 은 여기에 풀지 않았다 — 리뷰 핀의 우리 git blob 그대로다 (`PIN.txt` sha256 42/42 = `git show f118c1fd1:<경로>` · 우리 10-28 대조).  보려면 ZIP 이나 git 에서.  `PACKAGE_MANIFEST.sha256` 은 `repo/` 를 포함한 157 파일 목록이다 (받은 직후 157/157 일치 · `repo/` 를 뺀 뒤 이 폴더 기준으로는 115 줄만 해당).
- ⚠ Codex 가 Windows 에서 쓴 파일 중 CRLF 인 `.md` · `.json` · `.py` · `.sh` 19 개는 리포 `.gitattributes` (`eol=lf`) 가 커밋 때 LF 로 바꾼다 ⇒ 그 파일들은 이 폴더에서 `PACKAGE_MANIFEST.sha256` 과 바이트가 다르다.  바이트 원본 = 받은 ZIP.

## 우리 확인 (요약 — 상세 `_repro_ours_20261028/README.md`)

- Codex 판정값 23 행 = 우리 Linux 재실행 **차이 0** · 693 줄 실제 awk 절단 = Codex 전사 15/15 같음.
- **KG50R-04 를 Bash 로 실제 재현** — 큐에 그 케이스가 있거나 squeue 조회가 실패해 첫 고리가 "건너뜀" 인데도, 작업 폴더에 남은 옛 시험 기록으로 둘째 고리가 **본 러너를 제출** (가짜 sbatch 1 회 · 두 장면 모두).
- KG50R-01 = 실제 bash `-C` 가 09-27 r075 쌍을 통과 (문제 0) · 소급 = r075 정지 시점 2 step 차 (`_repro_ours_20261028/r075_retro.md`).
- Codex Q1 의 G0 파싱 보강 = 우리 awk 함수로 동적 재현 → 새 P3 `KG50R-07`.
- 지금 도는 50kg 런 (D2 · ibb job 328599) = settling 체크포인트 재개 · 그 호출에서 새로 낸 시험 328597 로 승격 (1저자 화면 보고 · 원본 미수령) ⇒ KG50R-01 (압축 루프 위상) · KG50R-04 (옛 시험) · KG50R-05 (계속 줄) 의 꼴이 아니다.  KG50R-02 · 03 (덱 내용 사각) 해당 여부 = 실제 재개 덱을 받아 봐야 안다 (수정 계획 Q).
- 원장: `docs/reviews/findings.json` KG50R-01–07 · KG50-02/10/14/16/17/18/19 상태 · 수정 계획 `docs/50kg/kg50_resume_recheck_fix_plan_20261028.md`.
