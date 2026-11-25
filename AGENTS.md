# AGENTS.md — 포인터 한 장

**이 repo 의 표준은 `CLAUDE.md` 하나다. 그것을 읽어라.**
(Codex·외부 리뷰어 포함 — 에이전트가 어느 쪽이든 규율은 한 벌이다.)

---

## 왜 이 파일이 포인터가 됐나 (2026-09-09)

이 파일은 2026-09-03 까지 `CLAUDE.md` **앞 79줄의 손 복사본**이었다. 두 벌을 손으로
맞추는 방식은 **닷새 만에 실패**했다 — 2026-09-09 대조에서 이렇게 갈라져 있었다:

| 갈라진 것 | 이 파일(구판) | `CLAUDE.md`(정본) |
|---|---|---|
| `.opju` 자동화 주체 | *"로컬 Windows **Codex** + originpro"* | *"로컬 Windows **Claude Code** + originpro"* ← **이쪽이 맞다** |
| QE-GPU 런타임 (`ldd` 규율) | **없음** | 있음 — 2026-09-08 에 같은 자리에서 **세 번** 틀린 대가로 쓴 절 |
| 산출물 회수 경로 | **없음** | `C:\Users\Administrator\Downloads\` (1저자 지정 2026-09-01) |
| 코드 규율 · 계산 규율(보고량) · 마감 규율 · 컨텍스트 절약 · kb 위키 규율 | **통째로 없음** (거버넌스 절반) | 있음 |

즉 이 파일을 읽은 에이전트는 **규율의 절반을 못 배우고, 한 줄은 정반대로 배웠다.**
그래서 내용을 지우고 포인터만 남긴다. **파일 자체는 지우지 않는다** — 세미나 문서 몇 편이
근거 원장에서 `AGENTS.md` 를 이름으로 인용하고 있어(예:
`kb/seminars/Research_Seminar_2026_08_cascade_final_source_ledger.md`), 파일이 사라지면
그 인용이 아무 데도 안 닿는다. 여기 도착한 사람은 `CLAUDE.md` 로 간다.

## 30초 요약이 필요하면 — `CLAUDE.md` §여기서 시작

| 묻는 것 | 정본 |
|---|---|
| 지금 상태 | `kb/open_items.md` ⏭ 절 |
| 판정 | `db/governance/decisions.json` (`decision_state: active` 만) |
| 값 | `db/properties/canonical_registry.json` |
| 금지 | `db/properties/citation_hazards.json` |
| 리뷰 | `kb/reviews/INDEX.md` |
| 화면 | `webapp/` |

⛔ **이 파일에 규칙을 새로 적지 마라.** 적는 순간 다시 두 벌이 되고, 위 표가 그 결말이다.
