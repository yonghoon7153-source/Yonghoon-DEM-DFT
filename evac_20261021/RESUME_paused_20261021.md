# 멈춰 둔 일 — 이어받기 카드 (2026-10-21 12:3x UTC · 1저자 *"지금 잘하고 있던거 나중에 잘 이어받을 수 있게 하고 Rint만 하자"*)

멈춘 이유는 사용량입니다 (1저자 X20 기준 ≈ 10 % 남음).  결함이 있어서 멈춘 것이 아닙니다.  아래 넷을 멈췄고, Rint 사슬 (D2) 하나만 계속 돕니다.

이어받는 방법
- 짧은 에이전트는 그 에이전트에게 SendMessage 로 "이어서" 를 보냅니다.
- 기록이 길어 "Prompt is too long" 이 나면, 같은 브리프 + 아래 스냅숏으로 새 에이전트를 띄웁니다.  새 에이전트는 격리 작업 트리에서 시작합니다.
  - 커밋된 것만 있으면 `git reset --hard <head>` 합니다.
  - 고치던 파일이 있으면 `git checkout <snap> -- .` 로 그 상태를 되살립니다.
- 원격 백업 = `claude/wip-20261021/evac` (스냅숏 커밋이 다 조상으로 들어 있습니다).

| 트랙 | 에이전트 · 브리프 | 기반 → 머리 | 스냅숏 (고치던 파일 포함) | 한 것 | 남은 것 |
|---|---|---|---|---|---|
| [언로딩] ULPR 수정 독립 재확인 (U2) | a948397637bfe9a76 · `prereview_unload2_BRIEF.md` | bbc2adefe (그대로) | 3857aebd3ce2da47a3ca574d582ea885d62d4acc (바뀐 것 0) | 시작 직후 · 산출 = `prereview_unload/REVIEW2.md` · `prereview_unload/u2/` (있으면) | 브리프 1–9 전부 → "보내도 됨 / 고친 뒤" → 1저자에게 알림 + 파일 |
| [LHS] S0b 보강 수정 (LF) | a2b5f624e708fc511 · `lhs_s0b_fix_BRIEF.md` | 7f99be67c → 7555e45b5 | db4d67b1ff1ba2657550e59716a41454754f7e21 (고치던 파일 4) | 0ea2b6c1c 원장 (SUPR-04 · SUPR-05 · SELF-129 open) · 59b752072 시험 먼저 (S11g 열둘 · S11h S0b 실제 경로) · 7555e45b5 고침 (s0b_fp 가 보충 쪽 문제를 받음) | 고치던 파일 4 의 내용 확인 → 변이 표 (리뷰어 6 + m1–m4) · 실물 자리 결과 · 요청서 · 증거 · 묶음 정정 (PRE-LHS-04–10) → 보고 → 리뷰어 a47d0294 가 diff 재확인 → 메인 cherry-pick → 게이트 → B7 핀 → WSL 사전 점검 명령 |
| [믹서] D2 수정 재확인 (F) | a876633abb3bfa519 · (지시 = 메인 11:2x SendMessage · 결과 파일 `prereview_mixer_d2/RECHECK.md`) | 9412f384a (그대로) | 9146644320ce1492d476049d88b962c2aa52241d (바뀐 것 0) | 도구 변이 탐침 쓰던 중 ("readback · diff · contact reader · smoke" · 심볼릭 링크 스크립트 폴더) | MXD2-01–06 원 반례 · 주장 대조 (154/154 · 변이 24/24 + 8/8 · lib 342 · CLI 14 · Q2 거부) · 옆 자리 → RECHECK.md |
| [믹서] D3 설계 v3 (D3F) | a71a02b496ed1949d · `d3_v3_fix_BRIEF.md` | 7f99be67c → 5735e20c6 | 0ae6589e0446afc900e795ed284dfedc735965ea (바뀐 것 0) | G 의 다섯 cherry-pick (a96aebeb9 · 61a51f5e5 · 7425f405b · 194ca4f02 · 9a4408f51) + 5735e20c6 원장 MXD3-22..40 | 브리프 2–5 (반례 검사 먼저 · v3 새 파일 · 요청서 · Qv3 목록) → 독립 재공격 → Qv3 를 1저자에게 → D2 와 함께 Codex |

## 계속 도는 것 (Rint)
- D2 = a6443d454e15fcdf8 · `rca_D2_BRIEF.md` (기반 704254ca0 + `rcaD/wip_dirty_1117.patch`)
  - 브리프 1–3 → A 커밋 넷 통합 (ada5096b7 · c80d86228 · 51e625db1 · fbfaae9b1) → 보고 ("Q1 · Q2 가 닿을 자리" 절 포함).
  - 그 뒤 새 에이전트 DQ 가 Q1 (단락 = NOT_COMPUTED) → Q2 (4 판 규칙 여섯) 을 시험 먼저 넣는다.  1저자 비준 10-21 *"권고대로 해줘"*.
- 그 뒤 Rint: 통합 → 회귀 → 게이트 → push → 사전 리뷰 (규칙 ③) → Codex 재검토 요청 (≈ 10-24 · 재압밀 금 10-23 · S0 SBE 기하 포함).
