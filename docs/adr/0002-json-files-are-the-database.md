# ADR 0002 — DB 는 `data/` 의 JSON 파일이다. 서버도 CMS 도 두지 않는다

- 상태: 채택 (2026-09-27)
- 관련: `data/schema/*.schema.json`, `scripts/validate-data.mjs`, `data/README.md`

## 맥락

내용의 원본은 내가 Canva 마인드맵에 손으로 적은 메모다. 이것을 "DB 화" 하되,
글을 고치는 사람은 한 명이고, 고치는 빈도는 낮고, 사이트는 정적으로 공유된다.
데이터베이스 서버나 CMS 를 두면 배포·백업·로그인이 따라오는데, 얻는 것이 없다.

## 결정

1. 데이터는 전부 `data/*.json`. 빌드 시점에 번들에 들어간다 (런타임 요청 없음).
2. 파일은 넷: `prefectures.json`(県 기본 정보), `regions.json`(지방·색),
   `mascots.json`(마스코트), `notes.json`(**내 마인드맵 레이어**).
3. `notes.json` 은 Canva 의 박스를 **트리 그대로** 옮긴다: 박스 = `item`, 선으로 이어진
   박스 = `children`, 박스 위 작은 캡션 = `cap`, 링크 = `url`, ★ = `star`.
   내 말투·표기를 고쳐 쓰지 않는다 — 이 파일은 내 목소리다.
4. 각 파일에 JSON Schema 를 두고, `npm run data:check` 가 참조 무결성(지방 id, slug,
   마스코트 id, 링크 형식, 가나 읽기 누락)을 빌드 전에 검사한다.
5. 사진은 저작권을 확인한 것만 넣는다. Canva 에 있던 웹 사진은 넣지 않고
   `kind: "photo"` 로 자리만 남긴다.

## 결과

- 메모 하나 고치기 = JSON 한 줄 고치고 push. 검사기가 오타·깨진 참조를 막는다.
- 다음 단계(노션 일본어 단어)도 같은 방식으로 `data/words.json` 을 얹으면 된다.
