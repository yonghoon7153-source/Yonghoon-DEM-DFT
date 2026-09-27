# 문서 인덱스

## 설계 결정 (ADR)

| # | 제목 | 요지 |
|---|---|---|
| [0001](adr/0001-branch-is-the-home.md) | 집은 브랜치 `nihonchizu` 다 | `main` 은 별개, 머지하지 않는다, 포트 5004 |
| [0002](adr/0002-json-files-are-the-database.md) | DB 는 `data/` 의 JSON 이다 | notes.json 은 Canva 트리 그대로, 검사기가 지킨다 |
| [0003](adr/0003-real-mascots-with-credits.md) | 마스코트는 실제 캐릭터 | 공식 그림은 크레딧과 함께, 아니면 닮은꼴 + 링크 |
| [0004](adr/0004-share-through-cloudflare-pages.md) | 공유는 Cloudflare Pages | `nihoncheese.bmlwork.kr`, 터널 없음 |
| [0005](adr/0005-map-layers-and-supplement.md) | 지도 레이어 · 보충 · 사진 검색 | 県 ふりがな, 도시·다리·산맥 버튼, 빈 県은 「✦ 보충」, 사진은 📷 검색 |
| [0006](adr/0006-canva-audit-is-a-check.md) | Canva 전수조사는 검사기가 | `nihon audit` 가 PDF 글줄 837개를 소모하며 대조, 빠지면 `nihon check` 가 멈춤 |
| [0007](adr/0007-comment-board-on-pages-functions.md) | 💬 comment 게시판 | Pages Function 하나 + D1, 로그인 없음, IP 는 해시만, 지우기는 `ADMIN_KEY` |

## 그 밖에

- [요청사항 체크리스트](CHECKLIST.md) — 부탁받은 것과 반영 상태
- [작업 로그](log.md) — 커밋마다 한 줄, "왜" 를 남긴다
- [README](../README.md) — 빠른 시작, 데이터 편집법, 배포
- [data/README](../data/README.md), [data/raw/README](../data/raw/README.md) — 데이터 파일과 출처
