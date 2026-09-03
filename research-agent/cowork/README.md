# Cowork 클라우드 예약 작업 (등록됨)

| 작업 | 시각 | trigger id | 하는 일 |
|---|---|---|---|
| NOON | 매일 12:00 KST (03:00 UTC) | trig_01PCCBZ2FCEzrtgQ8852myFX | Gmail Scholar alert 수집 → IF 우선 triage → 심층 분석 → `[RA-HANDOFF] … noon` 메일 |
| MORNING | 매일 09:00 KST (00:00 UTC) | trig_01Gb3Eup45N4LiyGEHbr2ray | handoff 메일 → Obsidian 디제스트 md → 사용자에게 발송 + `[RA-HANDOFF] … morning` 기록 |

- 프롬프트 원문은 이 폴더의 `noon_task_prompt.md` / `morning_task_prompt.md` (클라우드에 등록된 것과 동일하게 유지할 것).
- 두 작업 모두 `requires_local_device=true`로 만들어져 있어, 데스크톱 앱에서 승인하면 연결된 research-agent 폴더에 `ra sync` + git commit까지 직접 수행한다. 승인하지 않으면 메일만으로 동작한다(로컬 Hermes/Claude Code가 `ra sync`로 병합).
- 키워드 변경은 (1) `config/agent.yaml` (2) 메모리 `/areas/research-agent.md` (3) 두 프롬프트 — 세 곳을 함께 고친다. 클라우드 작업은 메모리를 먼저 읽으므로 메모리가 최우선이다.
