# にほんちず — 일본 지도 노트

일본 47도도부현(都道府県)을 눌러보며 익히는 인터랙티브 지도.
내가 Canva 마인드맵에 정리해 둔 메모가 각 県 패널에 **마인드맵 트리 그대로** 붙어 있고,
県을 누르면 거기 사는 친구(오리지널 마스코트)가 튀어나오는 이스터에그가 있다.

> 다음 단계: 노션에 모아둔 일본어 단어와 연결 (같은 데이터 구조 위에 페이지를 추가하면 됨).

## 어떻게 생겼나

| 전체 지도 | 県을 눌렀을 때 (교토 + 이나리 여우) |
|---|---|
| ![desktop](docs/screenshots/desktop.png) | ![kyoto](docs/screenshots/kyoto.png) |

| 図鑑 (스티커 도감) | 폰 |
|---|---|
| ![zukan](docs/screenshots/zukan.png) | ![mobile](docs/screenshots/mobile.png) |

## 바로 보기

- 로컬: `npm install` → `npm run dev` → http://localhost:5173
- 배포: `main` 또는 이 브랜치에 push 하면 GitHub Actions 가 GitHub Pages 로 배포한다 (아래 "배포" 참고).

## 무엇이 들어있나

| 기능 | 설명 |
|------|------|
| 지도 | 국토지리원 地球地図日本 경계 데이터를 단순화한 TopoJSON. 휠/핀치 줌, 드래그, 더블탭 없음(실수 방지). 오키나와는 규슈 서쪽 인셋 박스로 이동. |
| 라벨 | 漢字 / かな / 한글 전환 (기억됨). 줌 레벨에 따라 겹치지 않게 자동 표시. |
| 검색 | 한자·가나·한글·로마자·영어·현청 소재지로 검색. `/` 키로 포커스. |
| 패널 | 다이어리 페이지 느낌. **내 마인드맵**(Canva 메모 트리) → **함께 보기**(瀬戸内, 다리, 정령지정도시 등 여러 県에 걸친 메모) → **図鑑**(현청·명물·관광·한마디). |
| 지방 보기 | 범례 칩을 누르면 지방으로 줌 + 지방 메모 + 소속 県 + 그 지방의 친구들. |
| 이스터에그 | 21개 県에 오리지널 마스코트(구마모토 곰, 나라 사슴, 홋카이도 물범…). 발견하면 図鑑에 스티커로 모이고 지도에도 붙는다 (localStorage). 로고를 누르면 벚꽃. |
| 메모장 | 어느 県에도 안 붙는 메모(테이블 매너, 방향 단어, 지도의 도시 읽기). |
| 딥링크 | `#kyoto`, `#region/kinki` 처럼 URL 로 바로 열기. |

## 데이터 (DB)

전부 `data/` 아래 JSON. 빌드 전에 `npm run data:check` 가 형식·참조를 검사한다.

```
data/
├─ prefectures.json   47개 県: 이름(ja/kana/romaji/ko/en), 지방, 현청, 명물, 관광, 한마디, 마스코트 id
├─ regions.json       9개 지방: 이름, 지도 색, 글자색
├─ mascots.json       마스코트 이름·대사 (그림은 src/mascots/art.ts)
├─ notes.json         ★ 내 마인드맵 레이어 (Canva → 트리)  ← 가장 자주 고칠 파일
├─ schema/            각 파일의 JSON Schema (에디터 자동완성용)
└─ raw/               원본 지리 데이터 + 출처
```

### notes.json 쓰는 법

박스 하나 = `item`. 선으로 이어진 박스는 `children`. Canva 박스 위의 작은 캡션은 `cap`.

```jsonc
"kyoto": {
  "star": false,                       // 마인드맵의 ★
  "items": [
    { "t": "清水寺", "sub": "きよみずでら", "cap": "東山区",
      "children": [ { "t": "二年坂・三年坂", "sub": "ざか" } ] },
    { "t": "わびさび", "sub": "불완전함에서 아름다움을 찾는 미학",
      "url": "https://www.notion.so/…" }                      // 링크 박스
  ]
}
```

- `t` 큰 글씨 · `sub` 괄호 안 작은 글씨 · `cap` 캡션 · `ko` 한국어 이름 배지 · `url` 링크 · `kind: "photo"` 사진 자리
- 여러 県/지방에 걸치는 메모는 `extras[]` 에 넣고 `targets` 로 어디에 보여줄지 지정
- 지방 메모는 `regions.<id>.memo`

원본 Canva 마인드맵의 사진은 저작권 문제로 넣지 않았다 (`kind: "photo"` 로 자리만 표시).

### 지도 데이터 다시 만들기

```
npm run geo:build     # data/raw/japan.topojson → public/geo/japan.topo.json + src/generated/prefecture-geo.json
```

단순화 강도, 작은 섬 제거 기준, 오키나와 인셋 이동량은 `scripts/build-geo.mjs` 상단 상수.

## 코드 구조

```
index.html              마크업 (헤더·지도·패널·모달)
src/main.ts             상태·이벤트 연결, 해시 라우팅
src/map/map.ts          d3-geo + d3-zoom 지도, 라벨 배치, 스티커
src/ui/panel.ts         県/지방/메모장 패널 렌더
src/ui/notes-render.ts  마인드맵 트리 → 칩
src/ui/easter.ts        마스코트 팝업, 図鑑, 벚꽃
src/mascots/art.ts      마스코트 SVG (오리지널)
src/styles/*.css        tokens(색·폰트) / base / app
scripts/                geo 빌드, 데이터 검증
```

디자인 토큰(색, 폰트)은 `src/styles/tokens.css` 한 곳에서 바꾼다.
폰트: Kiwi Maru(제목, ja) · Zen Maru Gothic(본문, ja) · Gowun Dodum(본문, ko) · Gaegu(손글씨, ko) — 모두 Google Fonts.

## 명령

| 명령 | 설명 |
|------|------|
| `npm run dev` | 개발 서버 |
| `npm run build` | 데이터 검사 + 타입체크 없이 빌드 (`dist/`) |
| `npm run typecheck` | `tsc --noEmit` |
| `npm run data:check` | JSON 데이터 교차 검증 |
| `npm run geo:build` | 지도 데이터 재생성 |
| `npm run preview` | 빌드 결과 미리보기 |

## 배포

### GitHub Pages (기본, 무료)

1. 저장소 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 한 번만 바꾼다.
2. 이 브랜치(`claude/japan-map-webpage-l0bm3e`)에서 바로 배포하려면 **Settings → Environments → github-pages → Deployment branches** 에
   이 브랜치(또는 `claude/*`)를 추가한다. 기본값은 `main` 만 허용이라, 그 전까지는 deploy 잡이 "not allowed to deploy" 로 실패한다.
3. 그 뒤 push 하면 `.github/workflows/deploy.yml` 이 빌드해서 올린다 (Actions 탭에서 확인).
4. 주소: `https://<계정>.github.io/<저장소 이름>/` (BASE_PATH 는 워크플로가 자동으로 넣는다).

### Cloudflare Pages (원하면)

Cloudflare 대시보드 → Workers & Pages → Create → Pages → Connect to Git 에서 이 저장소 선택:

- Build command: `npm run build`
- Build output directory: `dist`
- (환경변수 불필요 — 루트 경로 배포)

`public/_headers` 에 캐시/보안 헤더가 들어있다.

## 출처 · 라이선스

- 지도 경계: [地球地図日本（国土地理院）](https://www.gsi.go.jp/kankyochiri/gm_jpn.html) — [dataofjapan/land](https://github.com/dataofjapan/land) 변환본. 비영리 이용 시 출처 표기 (사이트 하단에 표기).
- 폰트: Google Fonts (OFL).
- 마스코트: 이 프로젝트를 위해 그린 오리지널 캐릭터 (실존 캐릭터를 흉내내지 않음).
- 県 기본 정보(名物·観光·ひとこと)는 일반 상식 수준으로 정리한 것 — 틀린 게 있으면 `data/prefectures.json` 에서 고치면 된다.
