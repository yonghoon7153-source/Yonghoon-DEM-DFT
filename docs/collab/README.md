# 쪽지 (Claude ↔ Codex 작업 창) — 2026-10-23

- 근거: 1저자 10-23 *"서로 소통하고"* · 인계 `docs/handoff_codex_nonrint_20261023.md` §3.
- 쪽지 하나 = **새 파일 하나** · 이미 있는 쪽지는 고치지 않는다 (고칠 것이 있으면 새 쪽지로) — 두 쪽이 같은 파일을 고치지 않으므로 합칠 때 충돌이 없다.
- 이름 = `YYYYMMDD-HHMM_<트랙 또는 주제>.md` (UTC).

| 폴더 | 쓰는 쪽 | 어느 가지에 |
|---|---|---|
| `docs/collab/claude_to_codex/` | Claude | `claude/sdcp-dem-manuscript-si-pqwtv8` |
| `docs/collab/codex_to_claude/` | Codex 작업 창 | `codex/<트랙>` (Claude 가 cherry-pick 하면 이 가지에도 들어온다) |

- 쪽지는 정보다 — 발사 · 발송 · 비준 · 기계 실행은 늘 1저자 승인 뒤.
- 쪽지 안에 자기 `codex/*` 커밋 SHA 를 인용하지 않는다 (cherry-pick 뒤 바뀐다) — 자리 표시 `<<sha:커밋 제목 앞 낱말>>` → Claude 가 새 SHA 표를 쪽지로 보낸다.
