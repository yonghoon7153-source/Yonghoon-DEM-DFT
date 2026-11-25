# Cowork 클라우드 예약 작업 (등록 완료·가동 중)

| 작업 | 시각 | trigger id | 하는 일 |
|---|---|---|---|
| NOON | 매일 12:00 KST (03:00 UTC) | `trig_01PCCBZ2FCEzrtgQ8852myFX` | Gmail Scholar alert 수집 → 관련도 게이트 → IF 내림차순 → 심층 분석(+선점 경보) → `[RA-HANDOFF] … noon` 메일 |
| MORNING | 매일 09:00 KST (00:00 UTC) | `trig_01Gb3Eup45N4LiyGEHbr2ray` | handoff 수집 → Obsidian 디제스트 md(경보 최상단) → 발송 + `[RA-HANDOFF] … morning` 기록 |

## 프로필 소스가 두 곳이다 — 반드시 함께 갱신
클라우드 작업은 repo를 읽지 못한다. 그래서 연구 프로필이 두 곳에 있다:
1. `config/research_profile.md` — repo 정본. **Claude Code가 브랜치를 읽고 채운다.**
2. 메모리 `/areas/research-profile.md` — 클라우드 작업이 매 실행 시 읽는 사본.

`config/research_profile.md` 를 고쳤으면 그 내용을 Cowork 세션에 붙여 넣어 메모리도 갱신할 것.
두 트리거 프롬프트는 "메모리가 우선"이라고 못박아 뒀으므로, 메모리만 최신이면 동작은 옳다.

## 변경 절차
- 키워드: `config/agent.yaml` + 메모리 `/areas/research-agent.md` + 두 트리거 프롬프트
- 연구 내용·채점 규칙·선점 경보 대상: `config/research_profile.md` + 메모리 `/areas/research-profile.md`
- 트리거 프롬프트 원문은 `noon_task_prompt.md` / `morning_task_prompt.md` 에 사본을 둔다
