# LLM Wiki — Yonghoon-DEM-DFT mothership

Karpathy LLM Wiki 패턴 킷(`llm-wiki-kit_260730`, 커맨드스페이스 구요한 배포)을
이 모노레포 root 로 이식·적응한 위키. **규칙 원본은 `SCHEMA.md`** — 콘텐츠를
만들거나 고치기 전에 반드시 읽는다.

## 구성

| 경로 | 역할 |
|---|---|
| `SCHEMA.md` | 규칙 원본 (frontmatter, 품질 3축, update policy, 이 모노레포 특칙) |
| `CLAUDE.md` / `AGENTS.md` | 에이전트 스키마 (Parity Contract 미러) |
| `raw/` | 불변 원본 (전사·논문·저장소 감사·세션 기록) — sha256 봉인 |
| `concepts|entities|comparisons|queries|guides|questions|syntheses/` | 컴파일된 위키 |
| `inbox/` | ingest 대기 큐 (`/wiki-inbox` 가 처리) |
| `index.md` / `log.md` | 카탈로그 / append-only 로그 |
| `tools/` | `lint.py` `status.py` `new-page.py` + `hooks/` (Python stdlib, 의존성 0) · `extract_figures.py` (논문 PDF 그림 크로핑 — pymupdf 필요, DFT/argyrodite 계열 브랜치(루트 `BRANCHES.md` 참조)의 litdb 도구 이식본; 에이전트는 `.claude/agents/paper-curator.md`) |

## 킷 원본과 다른 점 (이 환경 적응)

1. **배치**: 별도 저장소가 아니라 이 모노레포 root `wiki/`. 커밋은 **루트
   `CLAUDE.md` 하드룰 1이 지정한 작업 브랜치**로만 push 한다 (브랜치 이름을 위키에
   적지 않는 이유는 `SCHEMA.md` Git 절).
2. **커맨드 이름**: repo root `.claude/commands/` 에 `wiki-` 접두로 설치
   (/wiki-ingest /wiki-inbox /wiki-query /wiki-verify /wiki-lint /wiki-status /wiki-wrap)
   — 연구 파이프라인 쪽 이름(/verify 등)과의 혼동 방지.
3. **Cross-vault 참조**: 절대 경로 대신 **repo-root 상대 경로**
   (`degradation-degeneracy/docs/...`) — 컨테이너·V100·Windows 에서 clone 경로가
   달라 절대 경로는 이식 불가.
4. **연구 파이프라인과의 경계**: degradation-degeneracy 의 인용 게이트가 보는
   code identity 는 `src/tools/configs/scripts` 뿐 → `wiki/` 커밋은 `source_digest`
   를 바꾸지 않는다. 수치의 정본은 artifact + `docs/RESULTS*.md`, 위키는 지도다.
5. **CI**: `.github/workflows/wiki-lint.yml` — `wiki/**` 를 건드린 push 만 lint.

## 일상 사용

```bash
python3 wiki/tools/status.py            # 스냅샷
python3 wiki/tools/lint.py              # 0 errors 확인
python3 wiki/tools/new-page.py concept <slug>
```

자료 흡수: 파일을 `wiki/inbox/` 에 넣고 `/wiki-inbox`, 또는 `/wiki-ingest <대상>`.
세션 마무리: `/wiki-wrap` (lint → log → commit).
