# wiki/raw/ — 예외적 불변 원본층

이 리포의 불변 증거층은 **이미 밖에 있다**: `docs/data/`(측정 CSV·JSON) ·
litdb 정본(friendly-meitner) · `docs/reviews/findings.json` · git 이력.
그래서 이 폴더는 킷 원형과 달리 **예외 전용**이다:

- 들어오는 것: litdb 소관(논문)도 측정 데이터도 아닌 외부 자료 — 강연 전사,
  외부 레포 감사 노트 등.  `transcripts/` 등 하위 폴더에 날짜-슬러그로 저장.
- 규칙: 한번 저장한 파일은 수정 금지 (원본이 바뀌면 새 -v2 파일).  frontmatter 에
  `source_url` / `ingested` 를 적는다.
- 논문 PDF·digest 는 여기 넣지 않는다 → wiki/SCHEMA.md 경계 규칙 1 (litdb 정본).
