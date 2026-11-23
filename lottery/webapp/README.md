# webapp — 복권 번호 연구소 (로컬 · 읽기 전용)

로또 6/45 · 연금복권720+ 전 회차 분석 결과를 브라우저에서 읽고, 수동으로 살 번호를 고르는
로컬 Flask 앱이다. 바깥으로 아무것도 보내지 않고, 저장소의 어떤 파일도 쓰지 않는다.
형식(사이드바 · 토큰 · 팔레트 · CSP · 서버 계산 SVG 차트)은 본체 브랜치
`claude/14-gate-code-review-9qkx05` 의 `webapp/` 을 따랐고 내용만 다르다.

---

## 무엇을 서빙하나

| 화면 | 소스 | 내용 |
|---|---|---|
| `/make` | `/api/score.json` (인기도 계수·확산 모델 번호 풀·과거 1등) | **번호 만들기** — 로또: 비인기 조합 · 완전 무작위 · 확산 모델(실험), 번호 고정·제외, 내 번호 검사. 연금: 조 선택 · 모든 조. 추첨은 브라우저 암호 난수 (`static/js/make.js`) |
| `/` | `results/analysis.json` | 한눈에 보기 — 요약 숫자 4개, 화면 카드, 최근 당첨번호 |
| `/random` | 같은 파일 `lotto.stats` | 추첨기 무작위성 검정 19개 (빈도·궁합수 990쌍·이월수·간격·총합…), 몬테카를로 2,000회 |
| `/ml` | `lotto.ml` · `ddpm` · `em` · `svr` | walk-forward 예측 백테스트 16개 전략 (실제 vs 가상 무작위 역사), 확산 모델, EM, SVR |
| `/people` | `lotto.popularity` | 회차별 1~5등 당첨자 수로 추정한 번호 선택 인기도, 자동/수동 자연실험, 1등 기대 수령액 |
| `/pension` | `pension.stats` · `pension.ml` | 연금복권 자리별 숫자 검정과 예측 |
| `/data` | `meta` · `course_map` | 원본 URL·sha256, 다시 만드는 명령, 한계, 강의(확률과통계·머신러닝)와의 연결 |
| `/all` | 위 전부 | 한 장짜리 (사이드바가 `#앵커`로 바뀐다) — `freeze.py` 가 정적 내보내기에 쓴다 |
| `/api/palette.json` | `content.palette_items()` | ⌘K 팔레트 목적지 |

수치는 전부 `lottery/results/analysis.json` 의 **사본**이다. 그 파일은 `lottery/build_results.py`
가 `lottery/data/raw/` (동행복권 원본, sha256 은 `MANIFEST.json`)에서 만든다. 앱은 계산하지 않는다.

## 화면 뼈대

| 부품 | 어디에 | 메모 |
|---|---|---|
| 레이아웃·토큰·폰트 | `static/css/style.css` | 본체 앱 style.css 에서 **공통 구획만 행 범위로 그대로** 가져왔다 (파일 머리에 출처 커밋·행). 고치지 않는다 — 본체와 diff 가 쉽게 남도록 |
| 복권 전용 | `static/css/lottery.css` | 로또 공 색, 생성기, 차트 마크, 발산형 9단계 색(본체 토큰을 OKLab 으로 보간) |
| 테마 초기화 | `static/js/boot.js` | 본체 그대로 |
| 팔레트·스크롤스파이·PDF | `static/js/app.js` | 본체 그대로 + 팔레트 주소를 `#cmdk[data-src]` 에서 읽게 한 줄 |
| 번호 생성기 | `static/js/make.js` | 인기도 계산은 `// <core>` 구간에만 있다 — `tests/test_site_js.py` 가 node 로 잘라 돌려 파이썬 `popularity.score_combos` 와 대조한다 |
| 차트 | `content.py` → `templates/_macros.html` | 좌표는 서버, 그리기는 템플릿 (본체 `sweep_chart` 와 같은 분업). 마크마다 `<title>` 이 있어 자바스크립트 없이도 값이 뜬다. 막대는 0 에서 시작한다 |
| 보안 | `app.py` | CSP `default-src 'self'`, 쓰기 메서드 405 (`_guard_mutation`), 기본 바인딩 127.0.0.1 |

## 실행

```bash
lottery/webapp/lotto.sh            # venv(.venv-webapp)·의존성·빈 포트를 알아서 잡는다 → http://127.0.0.1:5070
lottery/webapp/lotto.sh --stop
```

직접 띄우려면:

```bash
pip install -r lottery/webapp/requirements.txt
python3 lottery/webapp/app.py      # http://127.0.0.1:5070  (WEBAPP_HOST / WEBAPP_PORT 로 바꾼다)
```

본체 앱(5057)과 포트가 겹치지 않아 같이 띄울 수 있다. `--share` 는 본체 `bms --share` 와 같은 경계
(인증 없음, 사설망에서 잠깐)다.

## 배포 — `https://lotto.bmlwork.kr`

정적 사이트로 내보내 **Cloudflare Pages** 에 올린다. 서버·터널이 없다 — nihonchizu 브랜치의
`nihoncheese.bmlwork.kr` 과 같은 방식이다 (그쪽 ADR 0004). `bmlwork.kr` 은 bml 의 도메인이고 같은
Cloudflare 계정 DNS 에 있어서 서브도메인 CNAME 이 자동으로 들어간다 (서브도메인은 추가 비용 없음).

`freeze.py` 가 Flask 화면을 그대로 파일로 쓴다 — `dist/` (Pages 출력) 와 `export/` (claude.ai 아티팩트용 한 장):

```bash
pip install -r lottery/webapp/requirements.txt && python3 lottery/webapp/freeze.py
```

- `dist/` — 화면마다 한 파일(`/make` → `make.html`, Pages 가 확장자 없는 주소로 서빙), `404.html`, `/static`,
  `/api/*.json`, `_headers`. `_headers` 의 CSP 는 `app.py` 와 **같은 값**이다 (`tests/test_webapp.py` 가 고정) —
  인라인 스크립트가 없어서 `script-src 'self'` 그대로 간다.
- 로컬에서 Pages 와 같은 동작(확장자 없는 주소 · `_headers` · 404)을 보려면 `npx wrangler pages dev lottery/webapp/dist`.
  2026-11-23 wrangler 3.114.17 로 확인: `/make` 200, `/make.html` → 308 `/make`, 없는 주소 404, CSP 헤더 적용,
  CSP 아래에서 생성기·⌘K 동작, 콘솔 오류 0.

대시보드에서 한 번만 연결한다 (nihoncheese 와 같은 순서):

1. Cloudflare → **Compute → Workers & Pages → Create application** → 맨 아래 **Continue to Pages**
   (위의 Connect GitHub 는 Workers 용) → **Import an existing Git repository** → `yonghoon7153-source/Yonghoon-DEM-DFT`.
2. 프로젝트 이름 `lotto` (pages.dev 주소가 이미 있으면 `bml-lotto` 등 — 실제 주소는 아래 사용자 도메인이다) ·
   Production branch **`claude/lottery-site`** · Framework preset **None** ·
   Build command **`pip install -r lottery/webapp/requirements.txt && python3 lottery/webapp/freeze.py`** ·
   Build output directory **`lottery/webapp/dist`** · Root directory 비움 · 환경변수 없음
   (빌드 로그에 python 이 없다고 나오면 환경변수 `PYTHON_VERSION=3.12`).
3. 만든 뒤 **Settings → Build → Branch control → Preview branch: None**. 이 저장소의 다른 브랜치(bml·dft·nihonchizu 등)는
   다른 프로젝트라, 켜 두면 거기 push 할 때마다 미리보기 빌드가 돌고 실패 표시가 붙는다.
4. 프로젝트 → **Custom domains → Set up a custom domain → `lotto.bmlwork.kr` → Activate domain**.
   https 인증서가 붙기까지 몇 분 걸린다 (그동안 `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`).
5. 이후 `claude/lottery-site` 에 push 할 때마다 자동 배포.

`export/` 와 `dist/` 는 파생물이라 git 에 넣지 않는다. 서버 없이 한 장짜리를 보려면
`python3 -m http.server -d lottery/webapp/export 8000`.

## 데이터 갱신

```bash
python lottery/fetch_data.py       # 동행복권에서 받기 — 요청 2번, 검증 실패 시 기존 파일 보존
python lottery/build_results.py    # 분석 다시 (약 6~8분)
```

로컬 서버는 `analysis.json` 의 mtime 을 요청마다 확인하므로 새로고침만 하면 된다.
`lotto.bmlwork.kr` 은 바뀐 `data/`·`results/` 를 커밋해 `claude/lottery-site` 에 push 하면 Pages 가 다시 빌드한다.
