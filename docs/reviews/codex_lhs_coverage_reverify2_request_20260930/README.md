# Codex 재검증 2 — LHSC-03 · 04 R2 수정 패치 (준비 중 · 2026-09-30)

- 무엇: 재검증 판정 (`docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md` — HOLD · LHSC-03 R2 · LHSC-04 R2) 의 두 잔여를 고친 패치 둘.
  1저자 비준 09-30 낮 (*"비준이야 ㅇㅇ"*).  반례 먼저 — 옛 코드에서 새 시험이 실패하는 것을 확인한 뒤 고쳤다.
- `0012-…LHSC-04-R2….patch` — 수확기 item 2 접촉 면적 대조: 축별 탐침 합 → 반올림 상자 **포괄 구간** · 범위 분류 없앰 · `lens_geometry` 서술 정정.
- `0013-…LHSC-03-R2….patch` — `webapp/app.py` coverage v2 검증기: 값 · 타입 · 공존 계약 (`_v2_ok_record` · `_v2_blank_record`) · 실제 생산자 양성 대조 8 · Codex 변이 10.
- 적용 기준 = `source_manifest.json` 의 `base_commit` (앞 요청서의 패치 11 개를 적용한 검토 트리 `002cc2881`) · 파일 sha256 은 manifest 에 **실제로 계산해** 적었다.
- ⚠ 검토 브랜치 `review-coverage-20260930` 은 세션 컨테이너에만 있다 — 이 폴더가 두 커밋의 보존본이다.  요청서 본문 (질문 · 재현 명령) 은 다음 커밋.
