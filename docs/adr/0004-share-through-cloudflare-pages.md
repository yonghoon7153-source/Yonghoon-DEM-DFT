# ADR 0004 — 공유는 Cloudflare Pages + `nihon.ayh.kr` 로 한다. 터널을 쓰지 않는다

- 상태: 채택 (2026-09-27)
- 관련: bml 의 ADR 0014/0030/0031/0034 (터널·중계기·VPS), `public/_headers`, `tools/nihon share`

## 맥락

bml 은 로컬 서버를 바깥에 보여 줘야 해서 터널·중계기·VPS 를 거쳤고, 랩 망이
7844 포트를 막아 Cloudflare 터널이 안 됐다. にほんちず 는 사정이 다르다 —
**정적 사이트**라 빌드 결과(`dist/`)만 어딘가에 올리면 된다. 서버가 없으니
터널도 포트도 없다.

## 결정

1. 운영 주소는 **`https://nihon.ayh.kr`**, 호스팅은 **Cloudflare Pages** (무료, git 연결).
   - Production branch `nihonchizu`, Build command `npm run build`, Output `dist`.
   - Custom domain `nihon.ayh.kr` — `ayh.kr` 이 Cloudflare DNS 면 자동, 아니면 등록기관에
     `nihon` CNAME → `<프로젝트>.pages.dev`.
2. GitHub Pages 워크플로는 **수동 실행용 대안**으로만 남긴다 (저장소 설정 2번이 필요하고,
   `/<repo>/` 하위 경로라 주소가 못생겼다).
3. 캐시·보안 헤더는 `public/_headers` (Cloudflare Pages 가 읽는다).

## 결과

- push 하면 배포된다. 접속에 암호·터널·VPS 가 필요 없다.
- 대시보드 연결은 사람이 한 번 한다 (`nihon share` 가 절차를 보여 준다).
