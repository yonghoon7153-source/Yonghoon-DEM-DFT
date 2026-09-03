# research-agent — Claude Code 작업 지침 (브랜치 `claude/friendly-meitner-lldvar`)

이 폴더는 **논문 에이전트**다. (연구자가 무엇을 하는지는 `config/research_profile.md` 가 유일한 근거다 — 코드나 프롬프트에 연구 내용을 추측해서 적지 말 것.) Google Scholar alert → triage(IF 우선) → 심층 분석 → SQLite/JSONL DB + Obsidian vault + litdb → 매일 디제스트 메일.
당신(Claude Code)의 역할은 세 가지: (1) `config/research_profile.md` 를 브랜치 실제 내용으로 채우고 최신으로 유지, (2) 코드·설정 유지보수, (3) `ra`가 만든 **분석 큐를 채우는 논문 분석가**(헤드리스 `claude -p` 또는 `/paper-noon`).

## 절대 규칙
- 사실을 지어내지 않는다. 초록/전문이 없으면 `evidence_level`을 `snippet`/`title`로 적고 `follow_up`에 "전문 확보" 를 남긴다.
- 문체는 `prompts/style_guide.md` — 번역투 금지, 고유명사·재료명·저널명은 영어, Obsidian 문법(frontmatter, `[[wikilink]]`, callout).
- 파일명·경로 규칙은 `research_agent/vault.py`가 정한다. 노트를 손으로 만들지 말고 `ra vault`로 생성한다.
- DB(`data/papers.sqlite`)는 `ra`로만 수정한다. `data/papers.jsonl`은 미러(자동 생성)라 직접 편집 금지.
- 설정 변경은 `config/agent.yaml`, `config/journal_if.yaml`, `config/research_profile.md` 세 파일로 끝나야 한다. 코드에 상수를 박지 말 것.
- 버전: 동작이 바뀌면 `VERSION`·`research_agent/__init__.py`·`CHANGELOG.md`를 함께 올린다(semver).

## 자주 쓰는 명령
```bash
pip install -e ".[dev,llm]" && python -m pytest -q     # 설치·테스트
ra status                                              # DB/큐 상태
ra noon --no-imap                                      # 메일 없이 수동 JSON만 처리 (테스트)
ra analyze --queue                                     # 큐 생성 → data/analysis/pending/*.json
ra analyze --import-dir data/analysis/pending          # 채운 큐 가져오기
ra vault && ra litdb                                   # 노트·MOC·litdb 재생성
ra morning --dry-run                                   # 디제스트 미리보기 (vault/Digests/<date>.md)
ra sync                                                # [RA-HANDOFF] 메일(클라우드 Cowork 결과) 병합
```

## 큐 채우기 (논문 분석) 프로토콜
1. `data/analysis/pending/<id>.json` 을 연다. `prompt_system`(스키마+문체+연구 프로필)과 `prompt_user`(논문 정보)를 읽는다.
2. `analysis` 필드에 JSON 객체를 채운다. 필수 키: `one_liner`, `selection_reason`, `key_findings`. 나머지는 `prompts/deep_analysis.md` 스키마.
3. `ra analyze --import-dir data/analysis/pending` → 검증 실패 시 메시지대로 보완.
4. `ra vault && ra litdb` → `git add -A data vault && git commit -m "ra: analyses <date>"`.
서브에이전트 `.claude/agents/paper-analyst.md`가 이 프로토콜을 그대로 수행한다. 큐가 5편 이상이면 논문별로 병렬 서브에이전트를 띄운다.

## Cowork(클라우드)와의 분업
- Cowork 세션은 Gmail을 직접 읽고 쓴다. 12:00/09:00 클라우드 작업이 분석 결과와 디제스트를 `[RA-HANDOFF]` 메일로 이 계정에 보낸다.
- 이쪽(로컬/Claude Code/Hermes)은 `ra sync`로 그 메일을 DB·vault·litdb에 병합하고 commit/push 한다. 사용자는 아무것도 하지 않아도 된다.
- 로컬만 할 수 있는 일: 교내망 전문 PDF 확보 → `evidence_level: fulltext` 재분석, litdb 적재, git push.
- 충돌 규칙: 같은 논문에 분석이 둘이면 `evidence_level`이 높은 쪽(fulltext > abstract > snippet > title)을 남긴다.

## 브랜치 통합 시 할 일 (최초 1회)
`SETUP_CLAUDE_CODE.md` 체크리스트를 따른다. 기존 논문에이전트/litdb 코드가 있으면 `research_agent/exporters/litdb.py`의 `field_map`을 실제 스키마에 맞춘 뒤 `ra litdb`로 검증한다.
