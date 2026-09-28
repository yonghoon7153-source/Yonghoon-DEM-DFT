# CLAUDE.md — にほんちず (일본 지도 노트)

일본 47도도부현을 눌러보며 익히는 인터랙티브 지도. 내가 Canva 마인드맵에 적은 메모가
県 패널에 트리 그대로 붙고, 県을 누르면 그 지역의 실제 마스코트가 튀어나온다.
정적 사이트 (Vite + TypeScript, d3-geo). 설계 결정은 `docs/adr/`, 부탁받은 것은 `docs/CHECKLIST.md`.

## 0. 불변 규칙

1. **집은 브랜치 `nihonchizu` 다.** `main` 에 머지하지 않는다 (ADR 0001). 다른 브랜치는
   다른 프로젝트(bml, dft)이므로 한 폴더에서 checkout 으로 오가지 않는다 — `git worktree`.
2. **데이터는 `data/*.json` 뿐이다** (ADR 0002). 코드에 県 정보나 메모를 하드코딩하지 않는다.
   `notes.json` 은 사용자의 목소리다 — 말투·표기를 고쳐 쓰지 않고, 옮길 때는 Canva 박스 트리를
   그대로 보존한다 (박스 = item, 선 = children, 캡션 = cap).
3. **취향이 갈리는 선택은 비준받는다.** 색·폰트·레이아웃·캐릭터 스타일·브랜치 이름처럼
   답이 하나가 아닌 것은 권고안과 대안을 적어 사용자에게 묻고, 답을 받은 뒤 진행한다.
   사실 확인·버그 수정·리팩터링은 묻지 않고 한다.
4. **체크리스트를 갱신한다.** 사용자가 부탁한 것은 `docs/CHECKLIST.md` 에 번호를 달아 적고,
   반영될 때마다 상태를 바꾼다. 마지막 메시지에 상태를 요약한다.
5. **마스코트는 실제 캐릭터, 그림은 권리 범위 안에서** (ADR 0003). 공식 일러스트는 `credit`
   표기와 함께만, 아니면 닮은꼴에 "공식 그림 아님" 표시. 사용자가 고른 대체 그림(`standin`)은
   출처 크레딧 + "공식 그림 아님". 받은 그림이 공식이 아닌 것 같으면 넣기 전에 말한다. 상업 이용 없음.
6. **사진은 저작권을 확인한 것만.** Canva 의 웹 사진은 넣지 않는다 (`kind: "photo"` 자리만).
7. **push 전에 본다.** `nihon check` (데이터·Canva 전수조사·타입·빌드) 를 통과하고, 화면을 바꿨으면
   `tools/shots.mjs` 로 데스크톱·모바일 스크린샷을 찍어 직접 확인한다. 안 본 화면을 "됐다" 고 하지 않는다.
8. **커밋 제목은 `type: 제목`, 같은 제목을 `docs/log.md` 에 한 줄.** 다른 세션은 대화를 못 보므로
   "왜" 는 로그에 남긴다. 훅이 빠진 것을 알려 주고 `nihon feed` 가 센다.
9. **셸 스크립트는 LF.** 사용자는 Windows/WSL 을 쓴다. `.gitattributes` 가 강제한다.
10. **디자인 방향은 다꾸(다이어리 꾸미기) 감성이다** — 크림 종이, 파스텔 스티커, 마스킹테이프,
    손글씨 포인트. "AI 가 만든 것 같은" 보라 그라데이션·유리 카드·Inter 폰트를 쓰지 않는다.
    토큰은 `src/styles/tokens.css` 한 곳.

## 1. 구조

```
index.html              마크업 (헤더·지도·패널·모달)
src/main.ts             상태·이벤트 연결, 해시 라우팅 (#kyoto, #region/kinki)
src/map/map.ts          d3-geo + d3-zoom 지도, 라벨 배치(충돌 회피, ふりがな), 오키나와 인셋, 스티커
src/map/layers.ts       지도 레이어 — 도시 · 다리 · 가는 법(✈ 공항 · 🚄 신칸센) · 산맥 (data/places.json, transit.json, mountains.json)
src/ui/compass.ts       지도 둘레의 방위 北 · 南 · 西 左 · 東 右
src/ui/tokyo23.ts       東京23区 팝업 — 구 지도(public/geo/tokyo23.topo.json) + 구마다 내 칸
src/ui/panel.ts         県/지방/메모장 패널 (다이어리 페이지)
src/ui/notes-render.ts  마인드맵 트리 → 칩
src/ui/comments.ts      💬 コメント 게시판 화면 (ADR 0007)
src/ui/festivals.ts     🎆 축제 달력 페이지 (data/festivals.json, 출처 표시 = 마인드맵 칸 이름으로)
src/ui/fx.ts            축제 효과 — 불꽃 · 눈 · 벚꽃잎 · 단풍잎 · 등롱 · 북 · 리본 + 무대 색조 (#fx 층, ADR 0009)
src/ui/easter.ts        마스코트 팝업, 図鑑, 벚꽃
src/landmarks/          랜드마크 스티커 — 내 마인드맵 · 보충의 장소, 기본 정보의 観光을 닮은꼴로 (data/landmarks.json, 확대하면 지도 · 23区 팝업에, ADR 0011)
src/mascots/art.ts      마스코트 SVG
src/styles/             tokens / base / app
data/                   JSON DB + schema + raw 지리 데이터
functions/api/comments.ts  게시판 서버 — Pages Function + D1, 유일한 서버 조각 (켜는 법: nihon share)
scripts/                build-geo.mjs (지도 단순화·인셋), validate-data.mjs, audit-canva.mjs (Canva PDF 전수조사)
tools/nihon             한 줄 실행기 (sync → deps → dev), shots.mjs (스크린샷 QA), og-card.mjs (링크 미리보기 카드 → public/og.png)
docs/                   adr/, CHECKLIST.md, log.md, index.md, screenshots/
```

## 2. 명령

| | |
|---|---|
| `nihon` | 최신화 + 개발 서버 (http://localhost:5004) |
| `nihon check` | 데이터 검증 · Canva 전수조사 · 타입 · 빌드 |
| `nihon audit` | Canva PDF 글줄 837개가 데이터 어디에 있나 (빠지면 check 가 멈춤, 이유는 data/raw/canva-audit.json) |
| `nihon geo` | 지도 데이터 재생성 |
| `nihon feed` | 커밋 ↔ 로그 짝 |
| `nihon share` | 배포 주소·절차 (Cloudflare Pages, nihoncheese.bmlwork.kr) |
| `node tools/shots.mjs` | 스크린샷 QA (미리보기 서버 필요) |

## 3. 다음 단계

노션의 일본어 단어를 같은 방식으로 `data/words.json` 에 얹고, 県·지방과 연결한다.
