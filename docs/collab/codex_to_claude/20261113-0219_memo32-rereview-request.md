# 메모 3.2 독립 재리뷰 요청 인계 (2026-11-13)

| Q | 1저자 단계 | 권고 | 상태 |
|---|---|---|---|
| M32-Q1 | 준비된 요청·ZIP을 Codex 반박 창에 발송 | 메모의 문서 범위 재리뷰로 발송; 실행 GO 요청 없음 | 요청 준비1·실제 발송0 |

권고안 전제 (M32-Q1). 새 정책 비준을 요구하지 않는다. 메모 본문·구현 변경0·시험 실행0·연구 결과0·전체 HOLD. 판정 뒤에만 웹앱·docx를 갱신한다.

## 1. 바탕·반입

- 바탕 = B `56f4cfbb1d26371007b460a992d4cfc1ef68e950`. 쪽지 작성 직전 fetch에서 같음.
- 반입 대상 = `codex/memo32-1113`.
- 커밋 순서 = `<<sha:docs: request independent rereview of DEM memo 3.2>>` 1개.
- 바뀐 파일:
  - `docs/reviews/memo32_rereview_20261113/review_request.md`
  - `docs/reviews/memo32_rereview_20261113/finding_map.md`
  - `docs/reviews/memo32_rereview_20261113/preattack.md`
  - `docs/reviews/memo32_rereview_20261113/source_manifest.json`
  - `docs/collab/codex_to_claude/20261113-0219_memo32-rereview-request.md`
- 지운·옮긴 파일: 없음. Rint·봉인32·litdb 정본·공유 원장·기존 메모·처분표 변경0.

## 2. 요청 범위·확인

- DRD-01–13·SELF-161 대응표, Q1–Q6와 알려진 잔여를 적었다. DRD-10은 부분; 다른 항목도 독립 판정을 선결하지 않음.
- 메모1222줄·407897B. a0455e90b 반입본 = B = 현재 파일 바이트 동일. 리포 사본108·고정 문헌 카드41의 길이·SHA256·Git blob 대조. 카드 선택은 메모 slug 기반이며 정본 전수성 주장 아님.
- 기존 drd_table은 4회차 역사 상태가 남아 있어 현재 본문·5회차 처분과의 차이를 요청서 앞에서 명시했다.
- check_doc_refs.py 무인자 = rc1, 경로 부재0·SHA96. 바탕과 같은 Windows 구분자 문제; 96/96 기존 예외표 대응. native PASS 아님.
- check_review_findings.py 무인자 = rc0. 전체 gate는 반입 때 Claude.

## 3. 공유 기록 제안

`docs/session_20260923_progress.md`의 [DEM 우선 (수영)] 마지막 줄 뒤:

> 11-13 Codex 실무가 메모 3.2 DRD-01–13·SELF-161 독립 재리뷰 요청·고정 사본·사전 점검을 준비. 현재 메모 본문 무변경, DRD-10 잔여와 4회차 역사 처분/5회차 현재 규칙 차이를 명시. 1저자 발송→판정 수령 뒤 문서 최소 수정 및 웹앱/docx 갱신. 새 연구 결과0·전체 HOLD.

원장 상태·CLAUDE.md·게이트 변경 제안 없음. 판정은 Codex DEM 실무 창으로 수령하고 Claude는 반입만 한다.
