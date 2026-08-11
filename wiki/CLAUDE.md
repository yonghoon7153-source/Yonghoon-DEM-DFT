# wiki/ — LLM Wiki 하네스 (요약)

이 폴더는 리포 지식의 **항목화된 지도**다.  규칙 원본은 `wiki/SCHEMA.md` — 페이지를
만들거나 고치기 전에 읽는다.  루트 `CLAUDE.md` 가 상위 규범이다 (충돌 시 루트가 이긴다).

핵심 5줄:
1. 페이지는 **요약+포인터** — 정본 서술은 루트 CLAUDE.md 와 docs/.  수치엔 반드시 sources.
2. **논문은 litdb 정본 소관** (friendly-meitner 브랜치) — 위키는 `litdb-canon:<slug>` 참조만.
3. **모델 ID 를 페이지에 적지 않는다** (`author: agent|human` 만) — lint 가 오류로 잡는다.
4. `explored` 는 **사람만** 바꾼다.  새 페이지 = `explored: false` + `verificationStatus: unverified`.
5. 마무리: 새 페이지 → `index.md` 등록 + `log.md` append + `python3 wiki/tools/lint.py` 0 errors.
   커밋 prefix `wiki:`.

커맨드: `/wiki-ingest` `/wiki-query` `/wiki-verify` `/wiki-lint` `/wiki-status` `/wiki-wrap`
CLI: `wiki/tools/lint.py` · `status.py` · `new_page.py <type> <slug>` (전부 `--selftest` 보유)
