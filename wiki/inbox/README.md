# Inbox — ingest 대기 큐

여기에 자료를 던져두면 `/inbox` 가 일괄 처리한다. 이 폴더의 파일은 **임시**다 — ingest 가 끝나면 `raw/` 로 이동(원본 보존)되고 여기서는 삭제된다.

넣는 방법:
- 웹 글: 본문을 `.md` 나 `.txt` 로 저장 (Obsidian Web Clipper 저장 대상으로 지정해도 됨)
- URL 만 모아두기: `urls.md` 파일에 한 줄에 하나씩
- PDF/논문: 파일 그대로 (ingest 시 텍스트 추출)

처리 흐름: `/inbox` → 파일별 미리보기 + 분류 제안 → 승인 → `/ingest` 절차 (raw 저장 → 위키 컴파일 → index/log → lint) → inbox 원본 삭제.

이 README 는 삭제하지 않는다.
