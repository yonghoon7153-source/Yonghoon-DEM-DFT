# 작업 로그

append-only. 형식: `## [YYYY-MM-DD] action | subject` — 커밋 제목 `action: subject` 와 같은 제목.
충돌이 나면 양쪽 항목을 모두 남긴다. 현황은 `nihon feed`.

## [2026-03-25] create | Initial commit
## [2026-09-27] create | Add にほんちず: interactive Japan prefecture map with mind-map notes
## [2026-09-27] fix | Keep the mascot clear of the mobile speech strip; reserve room for the legend on phones
## [2026-09-27] docs | Add screenshots to the README
## [2026-09-27] docs | README: note the github-pages environment branch policy
## [2026-09-27] docs | README: Cloudflare Pages + bmlwork.kr subdomain recipe
## [2026-09-27] create | Research real prefecture mascots (staging data) and start the request checklist
## [2026-09-27] create | 집 브랜치 nihonchizu — bml 관례(nihon 실행기·Makefile·ADR 4건·로그·훅·전 브랜치 CI)
## [2026-09-27] update | 마스코트를 실제 ご当地キャラ 53종으로 — 県 공식 47 + 비공식 6, 닮은꼴 그림, 친구들 행, 지방별 図鑑, 크레딧 (ADR 0003)
## [2026-09-27] fix | nihon feed 가 `type:` 없는 옛 커밋 제목도 로그와 짝짓는다
## [2026-09-27] docs | 체크리스트 갱신 — 옛 브랜치 삭제, 테스트 30건
## [2026-09-27] create | 공식 마스코트 그림 반입 경로 — image 필드, 스티커·말풍선·図鑑·패널이 PNG 를 쓰고, scripts/import-mascot-images.mjs 가 폴더째 맞춰 넣는다
## [2026-09-27] update | 마스코트 그림 반입을 다듬는다 — 캐릭터 이름 우선 매칭, 흰 배경 제거, 512px WebP, 필요 목록 docs/MASCOT_IMAGES.md 자동 생성
## [2026-09-27] fix | 닫힌 패널 때문에 앱이 옆으로 밀리던 문제 — .app 을 overflow: clip 으로, 포커스 스크롤 되돌림
## [2026-09-27] ingest | 공식 그림 1/53 — キュンちゃん
## [2026-09-27] ingest | 공식 그림 5/53 — いくべぇ · わんこきょうだい · むすび丸 · んだッチ 추가 (いくべぇ 는 인형탈 사진, 흰 배경 제거)
## [2026-09-27] ingest | 공식 그림 6/53 — とちまるくん 추가
## [2026-09-27] update | 흰 배경 지우기를 엄격하게 — 순백만 지우고 가장자리는 부드럽게, 흰 장갑·어깨띠는 남긴다 · コバトン 추가 (7/53)
## [2026-09-27] fix | 지도가 움직이는 동안 툴팁을 숨긴다 — 멈춘 커서 밑으로 지나가는 県 이름이 엉뚱한 자리에 뜨던 것 · チーバくん 추가 (8/53)
## [2026-09-27] ingest | 공식 그림 13/53 — きてけろくん · ぐんまちゃん · キビタン · ハッスル黄門 · ゆりーと 추가, かながわキンタロウ 공식 정보로 정정
## [2026-09-27] ingest | 공식 그림 15/53 — レルヒさん, かながわキンタロウ 는 사용자가 고른 いらすとや 그림을 대체 그림(standin)으로
## [2026-09-27] ingest | 공식 그림 16/53 — ひゃくまんさん
## [2026-09-27] ingest | 공식 그림 17/53 — 武田菱丸, 소개를 공식 프로필(甲斐犬 남자아이)로 정정하고 공식 페이지 링크
## [2026-09-27] ingest | 공식 그림 18/53 — ふじっぴー
## [2026-09-27] update | 그림 반입 23/53 — はぴりゅう · きときと君 · ねば～る君 · アルクマ · ミナモ, 옆에 붙은 글자(©·캡션)를 떼는 --main-only 와 일부만 투명한 흰 배경 처리
## [2026-09-27] ingest | 공식 그림 24/53 — キャッフィー, 소개에 이름 유래(캣피시)·탄생 배경과 공식 페이지 링크
