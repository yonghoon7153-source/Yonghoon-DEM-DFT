# Rint ② 운영 → Codex DEM 실무 창 (2026-11-21 · Claude 서브 세션 · 1저자 결정)

1저자 11-21: *"지금 여기 토큰없어서 Rint도 codex 실무에서 진행될 수 있게 인계하자"* · *"토큰생기면 다시 여기 복귀할 수 있게"*.

⇒ Claude 가 돌아올 때까지 **Rint ② R 운영 = Codex DEM 실무 창**이 맡는다.  운영은 명령 블록 · 판독 · 기록이다.
- 11-16 역할 ("Codex 실무 = 비 Rint 만") 은 이 기간에만 바뀐다.
- Codex 반박 리뷰 창은 그대로 따로 둔다.

## 0. 시작 — 먼저 읽기

- `git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 claude/rint2-seal-20261118`
- **봉인 명령 문서는 봉인 가지에만 있다** (B 가지에 없다):
  - `git show origin/claude/rint2-seal-20261118:docs/reviews/rint2_kgy_commands_20261020.md` 의 §3-1b (4)–(7)
  - 봉인본 `git show origin/claude/rint2-seal-20261118:docs/reviews/rint2_seal_20261118/registration_R_sealed.md`
- 런 기록 = B 가지의 `docs/data/rint2_r_start_20261118/README.md`.  '그 뒤' 절에 지금까지의 시각과 원장 동작이 있다.
- CLAUDE.md 머리의 ★ 11-17 밤 ~ 11-18 줄 (봉인) 과 ★ 11-20 줄 (서브 세션) · 진행 기록 `docs/session_20260923_progress.md` 의 끝.
- 현장 감시 = 1저자 기계의 `~/rwatch.sh` (md5 `1135fe4231d4410cc586eabcb2263083` · 읽기만 · σ 없음).  쓰는 법: `watch -n 60 bash ~/rwatch.sh <P0|P1> <시도>`.

## 1. 지금 상태 (11-21 16 시 KST)

| 항목 | 상태 | 근거 |
|---|---|---|
| 봉인 | 커밋 `29643188524f` · 가지 `claude/rint2-seal-20261118` (push 금지) · 코드 핀 `64e4d213e` | CLAUDE.md ★ 11-17 줄 |
| kgy P0 사다리 (attempt_1) | 11-20 10:36 KST 에 끝 · rc 3 정상 끝 · origin8 + `CALIB_ORIGIN_SENSITIVE` (R_j,0 그대로 · PASS 문장 금지) | README '그 뒤' |
| 원장 | 넘김 ② gabia → kgy (`20261120T022342Z` · 끝 커밋 `7b43cc81df6d68e2c0094f4e6afd98243f265173` · flock · `RECV_OK`) → kgy recover rc 0 ⇒ **지금 kgy (`~/sdcp/ca1_ledger`)** · gabia 는 `ca1_ledger.parked` | README '그 뒤' |
| gabia P1 사다리 (attempt_2) | 1저자 11-21 *"끝났어"*.  11:26 화면 = 런 폴더 15 · 팔 JSON 50 · 요약 없음.  15:41 화면 = 마지막 팔 JSON 15:06 · 로그가 그 뒤에 고쳐짐 · python 프로세스 없음.  **⬜ rc 3 정상 끝 세 조건은 아직 확인 전** | 1저자 화면 (채팅) |
| gabia QE | 11-20 오전부터 멈춤 · 단위 동안 다시 켤지는 1저자가 정한다 (켜면 단위 시간이 늘어남) | README '그 뒤' |
| 마감 | GPU 팔 12-05 24:00 KST · 1저자 11-19 = 12-05 목표는 주 판정 값 (감도는 그 뒤) | CLAUDE.md ★ 11-18 줄 |

## 2. 할 일 (위에서부터 · 봉인 §3-1b (6) 의 차례 5–13)

| # | 할 일 | 봉인 자리 | 정상 끝 / 멈춤 |
|---|---|---|---|
| 1 | gabia P1 rc 3 정상 끝 세 조건 확인 — ① 사슬 로그 끝 줄 `멈춤 [ATTEMPT_LEDGER_MISMATCH] … 원장 잠금 파일을 못 연다` ② gabia 에 `~/sdcp/ca1_ledger` 없음 (`.parked` 만) ③ `~/sdcp/ca1_ladder_P1/attempt_2/ladder_summary.json` 있음.  읽기만 · σ 가 없는 줄만 (Claude 가 11-21 1저자에게 이 확인 명령을 줬다 — 화면을 받으면 판독) | (6) 끝 'rc 3 = 정상 끝' | 하나라도 아니면 멈추고 1저자 |
| 2 | 원장 넘김 ③ kgy → gabia (flock · 묶음 sha256 · 끝 커밋 대조 · `RECV_OK`) · 넘김 기록 한 줄 | (5) | gabia 가 원장을 가진다 · kgy = parked |
| 3 | gabia `--stage recover --out ~/sdcp/ca1_ladder_P1/attempt_2 --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` — 같은 부팅 · 시도가 돈 기계에서 | (6) 6 | rc 0 · 결과 줄 (by recover) · 부팅이 다르면 `--operator-confirm` 규칙 |
| 4 | 채택 사다리 폴더를 서로 옮김 — P0 → gabia · P1 → kgy · 같은 상대 자리 · 바이트 그대로 · sha256 또는 폴더 요약 대조 | (6) 7 | 두 기계에 두 채택 폴더 |
| 5 | 단위 12 — 첫 배정 kgy 7 · gabia 5 (아래 표).  단위마다 `unit:<이름>` 항목 → 단위 → 시작 확인 → 기다리는 기계에 넘김.  같은 기계에서 사슬 둘 금지 | (6) 8–9 | 끝날 때 원장이 있으면 rc 0 · 없으면 rc 3 → 원장이 돌아온 뒤 recover |
| 6 | 시간 다시 어림 — 각 기계의 첫 DBE 모서리 단위 실측으로 12-05 안에 끝나는지 본다 · 위험하면 1저자에게 먼저 | 배정은 봉인 밖 (바꿔도 원장 · 폴더 · 규칙이 시도를 정한다) | — |
| 7 | 합치기 — gabia `ca1_units` 통째 → kgy `ca1_units_from_gabia` · 원장 · P1 바탕 → kgy → (7) 첫 합치기 → rc 4 = 넘침 점 (112 h 규칙 · kgy 먼저 · 둘 다 넘으면 멈추고 1저자) → 끝 합치기 | (6) 10–12 · (7) | rc 0 |
| 8 | 주 판정 · 다시 판정 (`REVERIFY_SAME`).  값 열람은 1저자 (주 판정 런이 다 끝난 뒤 · 감도 전) | (6) 13 · 등록 R §4-1 | 판정 rc 0 |
| 9 | 감도 (FIBRE · UNREG · GRID …) = 주 판정 뒤 · 1저자 | 등록 R §5-6 | — |

| 기계 | 단위 (이 차례로 · 봉인 표 그대로) |
|---|---|
| kgy (7) | `P0_c0_R_j0` · `P0_c0_R_j_lo` · `P0_c0_R_j_hi` · `P0_c1_R_j0` · `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` |
| gabia (5) | `P1_c0_R_j_lo` · `P1_c0_R_j_hi` · `P1_c1_R_j0` · `P1_c1_R_j_lo` · `P1_c1_R_j_hi` |

## 3. 지킬 것 (Rint)

- σ 는 `verdict_results.json` 에만 둔다.  명령 블록 · 화면 · 쪽지 · 커밋에 σ 를 찍지 않는다 (파일 수 · 시각 · rc · 원장 동작 · 런 이름만).  판정 값 열람은 1저자.
- 원본 (런 폴더 · 원장 저장소 · 시도 폴더) 을 손으로 고치지 않는다.  옮길 때는 바이트 그대로 + sha256 대조.
- 봉인 문서 · 봉인 계획 · 코드 핀 `64e4d213e` 를 바꾸지 않는다.
- push 금지 가지: 봉인 가지 · B (`claude/sdcp-dem-manuscript-si-pqwtv8`) · stoic (`claude/stoic-knuth-NObVQ`).
- 현장 실행은 1저자가 한다 (너는 명령 블록만).  막히거나 모호하면 멈추고 1저자에게 묻는다.
- 재실행은 등록 규칙의 `--resume` 자격일 때만.  손으로 고친 기록이나 서로 어긋난 기록이면 멈춘다.
- 기존 규칙 그대로: 주소 · 포트 · 계정 · 홈 경로는 리포에 쓰지 않는다 · RJ 323957 재실행 없음 · 실행 우선 (11-16 Q1–Q4 · P2 · P3 = 알려진 한계로 적고 계속).
- Rint 의 Codex 반박은 이미 두 번 썼다.  2/2 = 봉인 준비 범위만 조건부 GO 이고, 실제 실행 · 정량 판정 · 운영 GO · 공유 원장 종결은 미승인이다 (`docs/reviews/codex_review_rint2_seal_round2_20261117.md`).  판정 문장은 이 한정을 지킨다.

## 4. 기록 · 내는 방식

- 가지 = `codex/rint2-r-1121` · B 끝에서 시작 · 한 줄 이력 · force push 없음.
- **첫 커밋 = 이 쪽지를 바이트 그대로** `docs/collab/claude_to_codex/20261121-1600_rint2-to-codex-practice.md` 에 넣는다.  Claude 가 push 하지 못한 채 넘겨서 이 한 파일만 예외로 네가 넣는다.  sha256 은 1저자가 붙여 넣는 프롬프트에 있다.
- 기록은 **새 파일** `docs/data/rint2_r_ops_20261121/README.md` 에 둔다:
  - 단계마다 한 줄 — 시각 · 기계 · 원장 동작 · rc
  - 넘김 기록 표 (§3-1b (5) 꼴)
  - σ 없음
- 옛 README (`docs/data/rint2_r_start_20261118/README.md`) 는 고치지 않는다.  Claude 가 반입할 때 한 줄로 잇는다.
- 쪽지 = `docs/collab/codex_to_claude/<YYYYMMDD-HHMM>_rint2-r-<단계>.md`.  담을 것:
  - 무엇 · 바탕 커밋 · 커밋
  - 1저자 Q
  - Claude 가 넣을 공유 기록 줄 — CLAUDE.md · 진행 기록 · findings 는 직접 고치지 않는다
  - 다음
- 나머지는 11-13 쪽지 `docs/collab/claude_to_codex/20261113-0940_nonrint-to-codex-practice.md` §4 · §5 (합칠 때 충돌 없게) 그대로.

## 5. Claude 복귀 (1저자 *"토큰생기면 다시 여기 복귀"*)

- 1저자가 Claude 서브 세션 (작업 가지 B) 에 "반입" 또는 "복귀" 라고 하면, Claude 가 다음을 한다:
  1. `git fetch` → 쪽지 순서대로 `cherry-pick -x`
  2. 게이트 세 조각 → push → 대응표 쪽지
  3. Rint 운영을 다시 받는다
- 그래서 **마지막 쪽지에 상태 표**를 남긴다.  Claude 는 그 표에서 이어 간다:
  - 원장 자리 (기계 · 끝 커밋)
  - 도는 사슬 (기계 · 시도 · 단위)
  - 끝난 단위
  - 넘김 기록
  - 다음 한 줄
  - 1저자 Q
- 본 세션 (stoic) 이 먼저 돌아오면 11-20 인계 순서 그대로 한다 (B 끝 → stoic fast-forward).  Codex 가지는 그때도 `cherry-pick -x` 로 들어온다.
- Claude 가 복귀 때 넣을 공유 기록 줄 (글 그대로):
  - CLAUDE.md ★ 머리 (11-20 줄 뒤): `★ **2026-11-21 — Rint ② 운영도 Codex DEM 실무 창으로 (1저자 *"지금 여기 토큰없어서 Rint도 codex 실무에서 진행될 수 있게 인계하자"* · *"토큰생기면 다시 여기 복귀할 수 있게"*)** — 쪽지 `docs/collab/claude_to_codex/20261121-1600_rint2-to-codex-practice.md` · Codex 가지 `codex/rint2-r-1121` · 기록 새 파일 `docs/data/rint2_r_ops_20261121/README.md` · σ 비열람 · 봉인 · B · stoic push 금지 · 복귀 = 1저자 "반입" → Claude cherry-pick -x · 11-16 역할 (Codex 실무 = 비 Rint 만) 은 이 기간만 바뀜.`
  - 진행 기록 끝: `- **[인계] 11-21 — Rint ② 운영 → Codex DEM 실무 창 (1저자 · Claude 토큰 부족)** — gabia P1 끝 (1저자 15:4x · rc 3 세 조건 확인 전) · 원장 = kgy · 다음 = 봉인 §3-1b (6) 5–13 · 쪽지 `docs/collab/claude_to_codex/20261121-1600_rint2-to-codex-practice.md`.`

## 6. 함께 — A5 · B1 (비 Rint · 네 트랙 그대로)

- B1 U (368139) = 11-21 15:40 KST `RUNNER_RC=0 · W9=LIVE_TERMINAL_MATCH · RETURN_READY=TRUE`.
- 이어지는 순서 (인계 11-20 §5-3):
  1. U 회수 (`PASTE_B1_U_RETURN`)
  2. WSL V2 폴더에서 `bash PASTE_A5_RJ_1120.txt GO_NEW_A5_RJ_ONCE CONFIRMED_UNLIMITED` 를 한 번
  3. `squeue` 로 RJ RUNNING 확인
  4. `bash PASTE_B1_C_LAUNCH.txt GO_B1_C_ONCE`
- 끊기거나 모호하면 `RETURN_A5_RJ_ONLY` 만 돌린다.  GO 줄은 다시 돌리지 않는다.
- Claude 가 11-21 에 1저자에게 이 순서를 안내했다.
- 믹서 원고 v2.x 는 리포 밖이다 (공개 리포에 원고를 넣지 않는다).  1저자 Q1 대기 · Claude 복귀 몫.
