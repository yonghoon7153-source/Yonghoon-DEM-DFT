# ADR 0004 — 공유는 Cloudflare Pages + `nihoncheese.bmlwork.kr` 로 한다. 터널을 쓰지 않는다

- 상태: 채택 (2026-09-27)
- 관련: bml 의 ADR 0014/0030/0031/0034 (터널·중계기·VPS), `public/_headers`, `tools/nihon share`

## 맥락

bml 은 로컬 서버를 바깥에 보여 줘야 해서 터널·중계기·VPS 를 거쳤고, 랩 망이
7844 포트를 막아 Cloudflare 터널이 안 됐다. にほんちず 는 사정이 다르다 —
**정적 사이트**라 빌드 결과(`dist/`)만 어딘가에 올리면 된다. 서버가 없으니
터널도 포트도 없다.

## 결정

1. 운영 주소는 **`https://nihoncheese.bmlwork.kr`**, 호스팅은 **Cloudflare Pages** (무료, git 연결, 프로젝트 `nihoncheese`).
   - Production branch `nihonchizu`, Build command `npm run build`, Output `dist`.
   - Preview branch **None** — 같은 저장소의 다른 브랜치는 다른 프로젝트(bml·dft)라 미리보기 빌드를 돌리지 않는다.
   - Custom domain `nihoncheese.bmlwork.kr` — `bmlwork.kr` 이 같은 Cloudflare 계정 DNS 라 CNAME 자동.
2. GitHub Pages 워크플로는 **수동 실행용 대안**으로만 남긴다 (저장소 설정 2번이 필요하고,
   `/<repo>/` 하위 경로라 주소가 못생겼다).
3. 캐시·보안 헤더는 `public/_headers` (Cloudflare Pages 가 읽는다).

## 결과

- push 하면 배포된다. 접속에 암호·터널·VPS 가 필요 없다.
- 대시보드 연결은 사람이 한 번 한다 (`nihon share` 가 절차를 보여 준다).

## 보완 (2026-09-27) — 이름은 `nihoncheese.bmlwork.kr`

처음엔 `nihoncheese.ayh.kr` 로 적었지만 **`ayh.kr` 은 산 적이 없다** (사용자 확인). 도메인은 이름 자체를 사는
것이라 `bmlwork.kr` 을 `ayh.kr` 로 바꿀 수도 없다. 그래서 bml 이 이미 산 **`bmlwork.kr`** (연 28,600원, bml 의
ADR 0031 · 0034 · 0036) 의 서브도메인을 쓴다 — 서브도메인은 몇 개를 만들어도 추가 비용이 없고,
`bml.bmlwork.kr` · `test.bmlwork.kr` 과 레코드가 따로라 서로 영향이 없다. 나중에 `ayh.kr` 을 사면 같은
프로젝트에 도메인을 하나 더 붙이면 된다. Pages 기본 주소 `https://nihoncheese.pages.dev` 도 계속 열린다.

2026-09-27: Custom domains 에 `nihoncheese.bmlwork.kr` 을 넣고 Activate — Initializing 을 거쳐 **Active · SSL enabled**.

## 덧붙임 (2026-09-27, 10차 요청)

💬 comment 게시판 때문에 `functions/api/comments.ts` **함수 하나**가 생겼다 (ADR 0007). 같은 Pages 프로젝트가
git push 때 함께 배포하고, `/api/comments` 만 함수를 부른다. 터널 · 따로 도는 서버는 여전히 없다.
