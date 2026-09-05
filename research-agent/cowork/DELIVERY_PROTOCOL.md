# Cowork → Claude Code 전달 규약 (2026-09-04 개정)

## 문제
Cowork 의 sandbox 트리는 v0.1.0 에서 갈라진 **fork** 다. Claude Code 가 브랜치에서 만든 것
(`exporters/litdb.py` markdown 어댑터 · `config/research_profile.md` 482줄 · `config/agent.yaml`
`mode: markdown` · `triage.py` 축 A/C 용어 · `tests/test_litdb_markdown.py`)이 Cowork 트리에는 없다.
그 상태로 tarball 을 통째로 보내면 **Claude Code 가 매번 델타를 손으로 골라내야** 하고,
목록이 길어지면 언젠가 하나를 놓친다. v0.1.3·v0.1.4 에서 두 번 반복됐다.

## 규약 — tarball 을 보내지 않는다
Cowork 는 **바뀐 파일만** 개별로 전달한다. 덮어쓸 것이 없으므로 사고가 날 수 없다.

1. 변경 후 `git diff --name-only <직전 태그>..HEAD -- . ':!data' ':!vault'` 로 목록을 뽑는다
2. **그 파일들만** 전달한다 (tarball 아님)
3. 함께 한 줄씩 적는다: 파일 / 왜 바뀌었나 / 이 파일이 Claude Code 정본인가
4. Claude Code 정본인 파일은 **애초에 보내지 않는다**

## 개정 (2026-09-05) — 개별 전달의 실패 모드는 tarball 과 반대다

v0.1.6 에서 9개 중 5개만 도착했고, **빠진 쪽에 신규 모듈 `feedback.py` 가 있었다.**
받은 5개만 넣으면 `vault.py:12 from .feedback import ...` 에서 `ModuleNotFoundError` 로
**import 단계부터 죽는다.** Claude Code 가 알아채고 전부 보류해서 사고는 안 났다.

- tarball 의 위험은 **덮어쓰기**, 개별 전달의 위험은 **빠뜨림**이다.
- 그리고 의존성 있는 신규 모듈이 빠지면 조용히 안 깨지고 **import 에서 즉시 죽는다.**

⇒ 세 가지를 규약에 넣는다 (Claude Code 제안 수용):

5. **한 번에 다 보낸다.** 나눠 보내면 중간 묶음이 유실된다 — v0.1.6 이 정확히 그랬다.
   묶음이 커도 쪼개지 말고, 쪼개야 하면 "N개 중 1번째" 처럼 번호를 붙인다.
6. **신규 모듈을 맨 앞에 붙인다.** 기존 파일이 import 하는 새 파일이 먼저 눈에 보여야 한다.
7. 보내기 직전 **CHANGELOG §파일 목록과 실제 첨부를 1:1로 대조**한다. 개수가 맞는지 센다.
   ```
   git diff --name-only <직전 태그>..HEAD -- . ':!data' ':!vault' | sort > /tmp/expected
   # 첨부 목록을 같은 형식으로 적어 diff 한다
   ```

## Claude Code 정본 목록 (Cowork 가 절대 건드리지 않는다)
- `config/research_profile.md` — 브랜치 전수조사 결과. 내용이 바뀌면 Claude Code 가 Cowork 에 통보하고
  Cowork 는 메모리 `/areas/research-profile.md` 만 갱신한다
- `config/agent.yaml` — litdb 경로·모드 등 실환경 값
- `research_agent/exporters/litdb.py` — markdown 어댑터
- `research_agent/triage.py` — 축 A/B/C 용어. Cowork 가 용어를 보태고 싶으면 **목록만** 전달하고
  파일은 Claude Code 가 머지한다
- `tests/test_litdb_markdown.py`, `tests/test_triage_db.py`
- `data/`, `vault/`, `REPORT_TO_COWORK.md`, `litdb/`

## Cowork 정본 목록 (Claude Code 가 그대로 받는다)
- `research_agent/cli.py` · `digest.py` · `vault.py` · `models.py` · `db.py` · `handoff.py` · `mailer.py`
- `prompts/*` · `templates/*` · `hermes/*` · `claude-code/*` · `cowork/*`
- `tests/test_dryrun_safety.py` · `tests/test_scholar_parser.py`
- `VERSION` · `pyproject.toml` · `research_agent/__init__.py` · `README.md`

경계가 애매한 파일이 생기면 **먼저 물어보고** 정한다. 조용히 덮지 않는다.

## `CHANGELOG.md` 는 어느 쪽 정본도 아니다 (2026-09-05 개정)

v0.1.6 전달에서 Cowork 판 `CHANGELOG.md` 가 Claude Code 의 병합 기록 두 절
(`## [0.1.4] 병합` · `## [0.1.3] 병합`)을 **지웠다.** 정본 목록에 들어 있었기 때문이다.
tarball 의 위험(덮어쓰기)이 파일 하나에 그대로 남아 있었던 셈이다.

CHANGELOG 는 **양쪽이 각자 쓰는 공동 이력**이라 한쪽 정본이 될 수 없다.

⇒ **파일을 보내지 않는다. 새 절만 보낸다.** 받는 쪽이 맨 위에 붙인다(splice).
   Cowork 는 `CHANGELOG_<버전>.md` 같은 조각 파일로 그 판의 절만 전달한다.
