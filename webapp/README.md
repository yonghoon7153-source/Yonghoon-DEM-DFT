# webapp — 위키·연구 결과 로컬 열람기

이 모노레포의 **위키와 연구 산출물을 브라우저에서 읽기 위한** 로컬 Flask 앱이다.
바깥으로 아무것도 보내지 않고, 저장소의 어떤 파일도 쓰지 않는다.

---

## 무엇을 서빙하나

| 화면 | 소스 | 내용 |
|---|---|---|
| `/` | `wiki/index.md` · `wiki/log.md` | 위키 카탈로그 + 최근 활동 (log 의 `## [date] action \| subject` 블록을 최신순으로) |
| `/papers` | `wiki/raw/papers/*.md` | 논문 digest 카드 — 제목 · 출처 · ingested · **sha256 앞 12자** · 그림 장수 |
| `/paper/<slug>` | 같은 파일 + `wiki/raw/figures/<slug>/` | digest 전문. 본문의 `Fig. N`·`Table N` 을 **자동 링크**해 크로핑 PNG 를 옆에 띄운다 (`figures.json` 의 원문 캡션 동반) |
| `/questions` `/question/<slug>` | `wiki/questions/*.md` | 질문 카드. **Evidence For / Against / Gap / Status Log / 설계 / 가설** 을 절 단위로 갈라 서로 다른 색·라벨로 렌더 |
| `/concepts` `/concept/<slug>` | `wiki/concepts/*.md` | 개념 페이지 |
| `/entities` `/entity/<slug>` | `wiki/entities/*.md` | satellite 프로젝트 상태 |
| `/doc/<kind>/<slug>` | `wiki/guides/` `queries/` `syntheses/` `comparisons/` `raw/transcripts/` `raw/articles/` `raw/repositories/` | 나머지 위키 문서 (wikilink 가 닿는 곳을 비우지 않기 위해) |
| `/results` | `mode-observability/docs/*.md` + `results/**/*.csv` | Phase 노트 + CSV. 200행 이하는 표 전체, 넘으면 **앞 15행 + 전체 기준 요약 통계**(n·min·median·mean·max) |
| `/gate` | `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md` | 게이트 라운드 색인 + **최근 절만** 렌더 (`?n=1..10`) |
| `/search?q=` | 위 전부 | 단순 부분 문자열 전문 검색 (파일별 히트 수 + 스니펫 3개) |
| `/api/figures/<slug>.json` | `figures.json` | 그림 색인 (figref.js 가 쓴다) |
| `/api/palette.json` | 위 전부 | 커맨드 팔레트(⌘K)가 훑을 목적지 목록 |
| `/api/file/<slug>/<file>` | `wiki/raw/figures/` | 그림 파일. **이 뿌리 밖은 404** |

frontmatter 의 `confidence` · `verificationStatus` · `status` · `claimType` ·
`evidenceScope` · `explored` 는 배지로, `tags` 는 태그로, `sources` 는 (그 페이지가
이 위키에 있으면) 링크로 나온다. 본문의 `[[wikilink]]` 는 해당 페이지로 이어지고,
**없는 페이지는 링크하지 않고** 점선 표시만 남긴다 (죽은 링크를 만들지 않는다).

## 화면 뼈대

외부 자원이 **하나도** 없다 — CSP 가 `default-src 'self'` 이고 `script-src 'self'` 라
CDN·웹폰트·아이콘 폰트·인라인 `<script>` 를 전부 못 쓴다. 그 제약 위에서:

| 부품 | 어디에 | 메모 |
|---|---|---|
| 아이콘 | `templates/base.html` 의 인라인 SVG `<symbol>` 스프라이트 | `currentColor` 를 따라가므로 테마 전환에 저절로 맞는다 |
| 타이포 | 시스템 폰트 스택 (`--sans` · `--mono`) | 한글 얼굴(`Apple SD Gothic Neo`·`맑은 고딕`)을 스택에 같이 넣는다 |
| 라이트/다크 | `style.css` 의 토큰 두 벌 + `data-theme` | 라이트 값을 뒤집은 게 아니라 손으로 두 벌 골랐다. 작은 글자(`--ink-3`)는 두 벌 모두 4.5:1 이상 |
| 테마 초기화 | `static/js/boot.js` — `<head>` 에서 **동기** 로드 | 인라인 스크립트를 못 쓰므로 파일로 뺐다. 페인트 전에 `data-theme` 을 정해 FOUC 를 막는다 |
| 커맨드 팔레트 (⌘K · Ctrl-K · `/`) | `static/js/app.js` + `/api/palette.json` | 목록을 `fetch` 로 받아 **DOM 으로** 채운다 (`innerHTML` 금지 — 제목이 위키 파일에서 온 문자열이다) |
| 목차 스크롤스파이 | `app.js` · `IntersectionObserver` | 6만 자 digest 에서 "지금 어디" 를 목차에 표시 |
| **전체화면 리더** | `static/js/reader.js` + `style.css` 의 `body.rd-on` | 논문 digest·개념 문서에서 `F`(또는 본문 위 버튼)로 들어가고 `Esc` 로 나온다. **본문 DOM 을 복제하지 않는다** — 하이라이트·메모(`app.js`)와 그림 팝업(`figref.js`)이 그 노드에 직접 걸려 있어서, 복제하면 같은 문단이 두 벌 생기고 주석이 어느 쪽을 가리키는지 모호해진다. 그래서 모드만 바꾼다 (실측: 리더 안에서 하이라이트·메모 레일이 보통 화면과 **같게** 동작) |
| 스윕 라인 차트 | `content.sweep_chart()` → 인라인 SVG | 차트 라이브러리를 못 쓴다. 좌표를 **서버가** 계산하고 템플릿은 그리기만 한다. 계열은 색 + 파선 + 점 모양 + 선 끝 직접 라벨 **넷**으로 구분 (색 하나에 안 기댄다) |

## 실행

```bash
webapp/bms.sh --no-pull          # 권장 — venv·의존성·빈 포트를 알아서 잡는다
webapp/bms.sh --stop             # 내린다
```

직접 띄우려면:

```bash
python3 -m venv .venv-webapp && . .venv-webapp/bin/activate   # 권장 (시스템 파이썬 오염 방지)
pip install -r webapp/requirements.txt
python3 webapp/app.py            # http://127.0.0.1:5057
```

- 바인딩 기본값은 **127.0.0.1**. 바꾸려면 `WEBAPP_HOST` / `WEBAPP_PORT` 를 명시해야 한다.
  기본을 루프백으로 두는 이유는 아래 "읽기 전용" 과 같다 — 이 앱은 인증이 없다.
- 서버는 요청마다 파일을 다시 읽는다. 위키를 고치면 **새로고침만으로** 반영된다.

### 같은 망의 다른 사람에게 보여 주기 — `bms --share`

```bash
bms --share          # 0.0.0.0 에 붙이고, 상대가 칠 주소를 찍어 준다
```

기동 로그가 `같은 망에서는 → http://<이 기계의 IP>:<포트>` 를 직접 알려 준다.
상대는 그 주소를 브라우저에 치면 된다.

**경계를 여는 것이므로 무엇이 열리는지 알고 쓴다.** 앱이 읽기 전용이라 남이
저장소를 고칠 수는 없지만, 위키·게이트 원장·결과 수치가 **같은 망의 누구에게나
그대로 보인다.** 인증이 없고 앞에 리버스 프록시도 없다. 사내망·연구실망에서
잠깐 같이 보는 용도이며, **공유기 포트포워딩이나 클라우드 공인 IP 에 걸어 두지
않는다.**

**Ubuntu 방화벽(ufw)이 켜져 있으면** 그 포트를 한 번 열어야 한다:

```bash
sudo ufw status                       # 꺼져 있으면 아무것도 안 해도 된다
sudo ufw allow from 192.168.0.0/16 to any port 5100 proto tcp   # 사설망만
sudo ufw delete allow from 192.168.0.0/16 to any port 5100 proto tcp   # 끝나면 닫는다
```

**WSL 에서 돌린다면 한 겹이 더 있다.** WSL2 는 Windows 안의 별도 가상 네트워크라
`--share` 만으로는 Windows 밖에서 안 닿는다. Windows 쪽에서 (관리자 PowerShell):

```powershell
# WSL 의 IP 는 bms 가 찍어 준 그 주소다
netsh interface portproxy add v4tov4 listenport=5100 listenaddress=0.0.0.0 `
      connectport=5100 connectaddress=<WSL IP>
New-NetFirewallRule -DisplayName "bms wiki 5100" -Direction Inbound `
      -Protocol TCP -LocalPort 5100 -Action Allow
```

끝나면 되돌린다:

```powershell
netsh interface portproxy delete v4tov4 listenport=5100 listenaddress=0.0.0.0
Remove-NetFirewallRule -DisplayName "bms wiki 5100"
```

상대는 **Windows 기계의 IP** 로 접속한다 (WSL IP 가 아니다 — WSL IP 는
재부팅마다 바뀌므로 portproxy 도 다시 걸어야 한다).

## 원본에서 가져온 것 / 버린 것

참고 원본은 다른 브랜치(argyrodite DFT 계열) 커밋 `e80dd480` 의 `webapp/` 이다
(47파일, `app.py` 만 58 KB). 도메인이 완전히 달라 **기능 패턴만** 가져왔다.

### 가져온 것

| 패턴 | 어디에 | 왜 |
|---|---|---|
| `figref.js` — 본문 `Fig. N` 자동 링크 + 여백 팝업 + 그림 카드 + 라이트박스 + 확대 | `static/js/figref.js` | 우리 digest 도 본문에서 `Fig. 8` 을 그대로 부르고 크로핑 PNG + `figures.json` 캡션이 같은 형식으로 있다. 정규식·키 규칙·"코드/링크 안은 건드리지 않는다"·"확대 시 원본 픽셀 기준" 같은 실측으로 다듬어진 부분을 그대로 살렸다 |
| 카드 목록(훑기) ↔ 별도 전문 라우트(정독)의 2단 구조 | `/papers` ↔ `/paper/<slug>` | digest 는 6만 자가 넘는다. 목록에서 전문을 펼치면 못 읽는다 |
| 마크다운 렌더에서 **raw HTML 파서 끄기** + 그 뒤 `href/src` scheme 재검사 | `content.md_html` · `_sanitize_urls` | 원본 리뷰 P2 의 실측 발견: raw HTML 을 꺼도 `[x](javascript:…)` 는 마크다운 **링크 문법**이라 그대로 통과한다. digest 는 외부 PDF 요약본이라 100% 신뢰 대상이 아니다 |
| 보안 헤더 (`_sec_headers`) | `app._sec_headers` | 저장형 XSS 방어를 파서 하나에만 기대지 않는다 |
| 읽기 전용 guard (`_guard_mutation`) | `app._guard_mutation` | 아래 참조. 원본은 라우트마다 호출했지만 **우리는 `before_request` 로 올려** 쓰기 메서드 자체를 막았다 |
| `requirements.txt` 의 메이저 상한 관행 | `webapp/requirements.txt` | 아래 참조 |
| CSS 변수 테마 + 사이드바 골격 | `static/css/style.css` | 구조만. 색·타이포는 새로 짰다 |

### 버린 것

| 버린 것 | 왜 |
|---|---|
| **쓰기 API 전부** — 코멘트, 하이라이트, 파일 이름변경, 업로드, `journal.jsonl` | 우리 `wiki/raw/` 는 sha256 봉인 불변층이다. 웹에서 고칠 수 있으면 봉인이 봉인이 아니다 |
| 도메인 페이지 전부 — 원소 주기율표, cascade 스크리닝, DFT 벤치마크, Fair-Chem, 조성, 용어집, T·Q 원장 | argyrodite DFT 도메인. 우리 내용이 아니다 |
| `data.py`(5768줄)의 `db/*.json` 모델 · `artifact_policy.py` · `glossary.py` | 그쪽 데이터 스키마 전용 |
| Plotly · 첨부 자동연결 규칙 · 즐겨찾기 | 차트는 스윕 하나뿐이라 서버가 SVG 좌표를 계산한다(라이브러리 0). 나머지는 우리 데이터에 대응물이 없다 |
| gunicorn · `render.yaml` 배포 | 공개 배포하지 않는다. 로컬 열람 전용 |
| figref 의 코멘트 마운트 · digest 주석 점프 · 팝업 드래그 이동 | 각각 쓰기 기능 / 우리 `figures.json` 에 없는 필드 / 창이 하나뿐이라 불필요 |
| 인라인 `<script>` · Google Fonts | CSP 를 `script-src 'self'` · `default-src 'self'` 로 조일 수 있게. 테마 초기화도 `static/js/boot.js` 로 뺐다 |

### 고쳐서 가져온 것 (원본 그대로면 우리 쪽에서 깨지는 것)

- **그림 키 정규화.** `figures.json` 의 `key` 를 그냥 쓰면 안 된다 — 세미나 자료는
  `F1`(대문자), 나머지 논문은 `f1`(소문자)로 추출 도구 판본이 달랐다. 서버가
  `종류 첫 글자 + 라벨 대문자` 한 규칙으로 다시 만든다 (`content._figkey`,
  `figref.js` 의 `keyOf` 와 같은 규칙).
- **경로 허용 뿌리.** 원본은 `docs/`·`db/`·`litdb/figures` 였다. 우리는
  `wiki/raw/figures/` **하나뿐**이다. 그 밖은 저장소 안이어도 404.
- **읽기 전용의 기본값.** 원본은 "로컬은 열고 원격은 잠근다" 였다. 우리는
  환경과 무관하게 **항상 잠근다** — 열어야 할 이유가 없다.

## 왜 읽기 전용인가

두 층이 각각 다른 이유로 불변이다.

1. **`wiki/raw/` 는 sha256 으로 봉인된 불변층이다.** digest frontmatter 의
   `sha256` 은 원문 PDF 의 지문이고, 원자료를 나중에 고치면 그 위에 쌓은 모든
   판단의 근거가 조용히 달라진다. 웹에서 쓰기가 가능하면 이 규율이 무의미해진다.
2. **`degradation-degeneracy/` 의 `src/ tools/ configs/ scripts/ run.sh
   requirements*.txt` 는 게이트 리뷰 대상 code identity(`source_digest`) 다.**
   한 글자만 바뀌어도 기존 산출물이 무효가 되고 재생성에 ~28분 + 10시간이 든다.
   이 앱은 그 트리를 **읽기만** 한다 (`/gate` 는 `docs/08_REVIEW_RESPONSE.md` 만 읽는다.
   `docs/` 는 identity 밖이지만, 그래도 쓰지 않는다).

구현은 세 겹이다.
- 쓰기 라우트가 **없다** (코멘트·업로드·이름변경 API 를 이식하지 않았다).
- `before_request` 의 `_guard_mutation` 이 `GET/HEAD/OPTIONS` 외 모든 메서드를 405 로 막는다.
  라우트가 없다는 사실에만 기대지 않는다 — 누가 나중에 POST 라우트를 붙여도 이 문을 먼저 지난다 (fail-closed).
- 파일 서빙은 `content.safe_file` 하나만 통과한다: 허용 뿌리 + `resolve()` +
  `is_relative_to()` + `is_file()`. 문자열로 `..` 를 막는 것으로는 심볼릭 링크 탈출을 못 막는다.

## 왜 의존성에 상한을 거는가

`requirements.txt` 는 `Flask>=3.0,<4.0` 처럼 **메이저 상한**을 건다. 원본 webapp 이
전부 `>=` 였을 때, 재배포마다 Flask/Markdown 이 조용히 올라가서 "어제 되던 화면이
오늘 다르다"를 추적할 수 없었다(그쪽 리뷰 P3). 이 저장소는 재현성이 전제인 검증
프로젝트다 — 같은 이유가 그대로 적용된다. 상한을 메이저에만 걸어 보안 패치는 받되
파괴적 변경은 막는다.

의존성은 셋뿐이다: `Flask`(서버·템플릿) · `markdown`(렌더) · `PyYAML`(frontmatter).
PyYAML 이 없으면 앱은 그래도 뜨고 frontmatter 만 얕게 읽는다.

## 파일

```
webapp/
  bms.sh                 한 줄 실행 런처 (git 갱신 → venv → 빈 포트 → 기동)
  app.py                 라우트 + 읽기 전용 guard + 보안 헤더 + 앵커 접두사 배분
  content.py             파일 읽기 · frontmatter · 마크다운/wikilink 렌더 · 제목 앵커/목차 ·
                         3구분 표기 · 그림 색인 · CSV · Phase 레일 · 스윕 차트 기하 · 검색
  requirements.txt       Flask · markdown · PyYAML (메이저 상한)
  templates/             base(사이드바·스프라이트·팔레트) + 화면 10종 +
                         _macros(배지·태그·sources·목차·3구분 범례)
  static/css/style.css   토큰 두 벌(라이트/다크) · 타이포 스케일 · 카드/패널 · 본문 격자 ·
                         타임라인 · 차트 · 표 · 팔레트 · 좁은 화면 · 인쇄
  static/js/boot.js      테마 초기화·토글 + 사이드바 서랍 (<head> 동기 로드)
  static/js/app.js       커맨드 팔레트 + 목차 스크롤스파이 + 하이라이트·메모 (defer)
  static/js/reader.js    전체화면 리더 — 모드 전환·진행률·글자 크기·본문 폭·목차/메모 접기
                         (읽기 취향만 localStorage 에 남긴다. 저장소에는 아무것도 안 쓴다)
  static/js/figref.js    Fig. N 자동 링크 · 팝업 · 그림 카드 · 라이트박스
```

### 한 화면에 문서가 둘 이상 실릴 때 (앵커 규칙)

`content.anchor_headings` 는 제목 id 를 **우리가** 만든다 (`h-1`, `h-2`…). 문서
내용에서 온 문자열을 id 로 쓰지 않으려는 것이고, 그래서 `render_digest` 를 한
화면에서 두 번 부르면 두 문서가 **둘 다 `h-1` 부터** 다시 시작한다 — id 가 겹쳐
목차 링크와 `#앵커` 가 전부 첫 문서로 간다. `/results` 가 PHASE 노트 두 편을 한
화면에 실으면서 실제로 그랬다.

그래서 `render_digest(body, prefix=...)` 에 **문서마다 다른 접두사**를 준다.
접두사는 `content.slug_id()` 로 **파일 이름에서만** 만든다 (`PHASE1B_NOTES` →
`phase1b-notes` → `phase1b-notes-1`, `phase1b-notes-2`…). CSV 칸과 검색 결과의
`/results#…` 딥링크도 같은 함수를 쓰므로 세 곳이 갈라지지 않는다.

## 한계

- 검색은 부분 문자열이다. 형태소 분석·순위 모델이 없다 (히트 수로만 정렬).
- `/gate` 는 `## §N` 제목으로 절을 자른다. 원장의 제목 규칙이 바뀌면 색인이 빈다.
- CSV 요약은 열별 일변량 통계뿐이다. 상관·분포는 그리지 않는다 —
  **그림으로 주장하는 것은 정본(artifact·`docs/RESULTS*.md`)의 일이다.**
- 렌더된 숫자는 전부 사본이다. 인용 근거는 언제나 원본 파일이다.
