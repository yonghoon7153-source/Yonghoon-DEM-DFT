# 믹서 D3 설계 v3 — 재공격 결함 고치기 (이름 `D3F` · 10-21 · 1저자 비준)

## 비준 (1저자 10-21 원문)
- 질문 [믹서] Q1: *"D3 를 한 번 더 고친 뒤 보낼까요? 설계 v3 를 새 파일로 만들고, 원장에 등재하고, 반례를 검사로 먼저 넣은 다음 독립 재공격을 한 번 더 하고, D2 와 함께 Codex 로 보내는 순서입니다."*
- 1저자 답: *"ㅇㅇ 고쳐"*

## 입력
- **v2 재공격 판정문** = `scratchpad/prereview_d3v2/REVIEW.md` (PRE-D3V2-01–19 · P1 3 · P2 8 · P3 8 · 탐침 p00–p18 · 재실행 명령 §5).  **전부 먼저 읽는다.**
- v1 사전 공격 판정 = 요청서 초안 `docs/reviews/codex_mixer_d3_design_request_20261021.md` §2-3 (메인 `92650e1c4`) · v1 설계 `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md`.
- v2 묶음 (작업 트리 에이전트 G · 기반 `055ddd04e`)
  - `62ba75013` 원장 MXD3-01..21
  - `6ba118c52` 규칙 검사 red
  - `804469e5a` v2 + green
  - `a2dc093c5` v1 배너
  - `2f1d29d09` 요청서 → v2
  - ⚠ `932eaa124` 는 메인 `92650e1c4` 와 같은 내용 → **건너뛴다**
- 논지 정본 `docs/hetero_thesis.md` (D3 = SE–SE 점착 유동성 실측 앵커).

## 작업 트리 세우기 (너의 격리 작업 트리)
1. `git reset --hard 7f99be67c` (메인 · batch 2+3 · 메인 게이트 중).
2. G 의 다섯을 차례로 cherry-pick: `62ba75013 6ba118c52 804469e5a a2dc093c5 2f1d29d09`.
3. 충돌 (원장 `findings.json` · 진행 기록 · CLAUDE.md 등) 은 두 쪽 뜻을 다 살려 풀고 자리를 보고한다.
   - CLAUDE.md · 진행 기록은 메인 몫이다 — cherry-pick 이 그것을 바꾸면 그 hunk 를 빼고 보고한다.

## 할 일 (순서대로 · 커밋 하나씩)
1. **원장 먼저** — PRE-D3V2-01–19 를 원장에 open 으로 넣는다.
   - ID = MXD3 다음 빈 번호부터.
   - 01 = MXD3-02 수정이 만든 새 결함이라고 적는다.
   - 03 = MXD3-08 일부 재개방이라고 적는다 (MXD3-08 메모).
   - 02 = MXD3-01 과 같은 부류라고 적는다.
   - `python3 scripts/check_review_findings.py` rc 0.
2. **반례를 검사로 먼저** (v2 에서 red)
   - v2 규칙 검사 스크립트 (6ba118c52 · 804469e5a 의 것) 에 PRE-D3V2 반례를 더한다.
   - v2 판에서 실패하는 것을 기록한다.
   - PRE-D3V2-10: 대조가 `True` 로 고정된 C04 · C05 · C07 · C11 · C17 을 실제 대조로 바꾼다.
   - 판정문의 변이 19 를 다시 돌려 이제 잡히는지 표로 보인다.
3. **설계 v3** = 새 파일 `docs/reviews/mixer_d3_se_flowability_anchor_design_v3_20261021.md` → 검사 green.
   - v2 본문은 그대로 두고 맨 위에 v3 를 가리키는 배너 한 줄만 단다.
   - P1 셋은 규칙을 고친다.
     - 01: R02 받는 범위 = 칸 값 범위 안.
     - 02: R01 검출 한계 = R02 집합의 실제 폭.
     - 03: f_cal · 속도를 측정 전 등록으로 옮기고, ρ_b 가 암호 상태인 순서 문제를 정한다.
   - P2 · P3 는 판정문의 최소 해결대로 한다.
     - 해결이 1저자 판단을 요하면 고르지 말고 v3 의 "1저자 질문" 목록에 기본값과 함께 적는다.
     - 예: 연속 검증을 버리느냐 · 띠를 정의하느냐 · T1 수준 수.
4. **요청서** `docs/reviews/codex_mixer_d3_design_request_20261021.md` → v3 를 가리키게 고친다.
   - 맨 위에 "이번에 닫는 것 / 닫지 않는 것" 을 둔다.
   - v2 회차 판정 요약 한 절.
   - 숫자 · 전칭은 실행 출력과 대조한다.
5. **1저자 질문 목록** — v2 의 Qv2-1..16 (기본값 적힌 ⬜) 을 v3 에 맞게 다시 쓴다 (Qv3-NN).
   - 바뀐 것 · 없어진 것 · 새것을 표시한다.
   - 결정은 하지 않는다 (메인이 1저자에게 한 번에 묻는다).

## 숫자
- lab 세대 (`lab20261014`) 값만 쓴다.  gen1 값은 쓰지 않는다 (MXD2-07).
- 모든 숫자는 스크립트로 다시 낸다.
- 새 DEM 런은 없다 (결과 0 건 설계).

## 보고
- 커밋 목록 · cherry-pick 충돌 자리.
- 검사 red → green 수 · 변이 표.
- P1/P2/P3 각 처리 (고침 / 질문으로).
- Qv3 목록.
- 남은 데이터 대기 (MXD3-18..21 · 1저자 장비 목록 등).

## 규칙
- 60 초 넘는 실행은 `bash scratchpad/heavy.sh <명령> > <로그> 2>&1` 로 한다.
- python `-I` · `nice -n 19` · `OPENBLAS_NUM_THREADS=1`.
- 디스크 여유 ≈ 5 GB.
- push · fetch · `scripts/check_all.sh` 안 함.
- 봉인 32 파일 (`scripts/run_network_194_parallel.py` CODE_FILES) 은 손대지 않는다.
- 생성기 `make_mixer_deck.py` 는 바꾸지 않는다 (D2 수정이 따로 돈다).
- 문서에 작업 트리 SHA 를 쓰지 않는다 (SELF-116).  자리표 `<메인 반영 뒤 채움>` 을 쓴다.
- 숫자 · 전칭은 실행 출력으로만 쓴다 (SELF-124).
- `scratchpad/` = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad`
