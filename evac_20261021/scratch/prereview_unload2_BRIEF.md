# 언로딩 키트 ULPR-01–04 수정 — 독립 재확인 (이름 `U2` · 10-21)

## 너의 역할
너는 **고친 사람의 설명 없이 diff 와 실행 결과만 믿는 독립 검토자**다 (CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ③).
이 수정의 목적은 Codex 짧은 재확인 2 에 보내도 되게 하는 것이다.  너의 결론이 "보내도 됨" 이어야 1저자가 보낸다.

## 배경 (짧게)
- 키트 = `docs/data/ps45_unload_20261009/` (DEM 언로딩 시험 키트).  판독기 · 관문 · 봉인 · 덱 64 개.
- 이전 사전 리뷰 (다른 에이전트 · 10-21 오전 · 핀 `92e6cda4d`) = `scratchpad/prereview_unload/REVIEW.md`.
  - 결함 PRE-UL-01 (P2) · 02–05 (P3).  원장 `docs/reviews/findings.json` 의 `ULPR-01`–`04` 가 그것이다 (05 = 요청서 문구).
  - 1저자 결정: Q1 = 고친 뒤 보냄 · Q2 = G2c 열 결손 = 등록 §14-10 대로 UNCONFIRMED.
  - 그 리뷰의 탐침 · 스크립트 = 같은 폴더 (`probe_resume_unfinished.py` · `run_codex_probes.sh` · `codex_rerun_pin/` · `mutate.py` …).
    옛 작업 트리 경로 (W=…agent-a93377624c009ba18) 는 지워졌다 — 네 작업 트리 경로로 바꿔 쓴다.
- 수정 = `286a8d562..bbc2adefe` (6 커밋)
  - `f1b911f76` 시험 먼저
  - `55fff3eb1` ULPR-01 (경계 뒤 행은 쓴 시도가 증명될 때만)
  - `2932b63bc` ULPR-03/04
  - `c21b1a051` · `28b66e116` 지킴 시험 (`28b66e116` = 요청서 리뷰 핀)
  - `bbc2adefe` 문서 · 증거 (`docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021/`) · 요청서 갱신
- 요청서 = `docs/reviews/codex_dem_unloading_kit_fix_recheck2_request_20261015.md` (bbc2adefe 판).

## 작업 트리
- 너는 격리 작업 트리에서 시작한다.  먼저 `git reset --hard bbc2adefe` (같은 저장소 · fetch 안 함).
- 옛 판 비교는 `git show <sha>:<path>` 또는 `git archive <sha> docs/data/ps45_unload_20261009 | tar -x -C <스크래치 폴더>`.

## 볼 것 (최소 — 더 찾으면 더)
1. **PRE-UL-01 원 반례가 이제 거부되는가.**
   - 원 반례 = 이어 돌린 새 시도가 k_r+1 단 줄을 다시 쓰기 전에 TIMEOUT/GUARD 로 끝나 옛 시도의 단 줄이 정상 관측으로 쓰임 · 주 값 OK · ρ 0.2026 % · UVa ALLOW.
   - 그 옆 자리도 본다:
     - 단 줄은 다시 썼는데 창 기록이 모자람
     - 증거가 하나만 있음
     - 증거끼리 모순
     - RESUME 둘
     - 경계가 0 · 마지막 단
   - 수정 규칙 (경계 뒤 행은 증명된 시도만 · 증거 = 창 · 단 역행 · k ≥ k_r+2 · RESUME 뒤 사건 · 요약 · `state_unload_<s>` s > s_r · 아니면 버림 · 모순이면 주 값 미식별) 이 실제로 그렇게 도는지 **손으로 푸는 작은 기록**으로 보인다.
2. **ULPR-02** — 새 사유 줄 · 조건 여섯이 시험에 붙잡히는가.  고친 사람 주장 = 변이 25/25 실패.  변이를 직접 돌린다.
3. **ULPR-03** — G2 `_dump_tokens` 가 중복 ID · 다른 TIMESTEP · 잘린 덤프를 거부하는가.  README 의 "ID unique" 문장이 이제 참인가.
4. **ULPR-04** — G2c 열 결손 = UNCONFIRMED (§14-10) · G2/G2c 파서 문제 = NOT_COMPUTED 인가.
5. **봉인 · 바이트**
   - 봉인 76 파일 · 규칙 24 · retired 0 인가.
   - SHA256SUMS `ecf406a6…` · active_rules `48d63476…` 를 직접 다시 계산한다.
   - 다음이 무변경인가: 생산 덱 64 개 (바이트) · history_test `8ff722d2…` · `read_history.py` `70f741a9…`.
6. **Codex 탐침을 `28b66e116` 에서 다시** 돌린다.  고친 사람 주장:
   - resume_recheck 35/37 (2 = 정수 반올림)
   - receipt_ids_recheck Q4 관용 사본 = 1 불일치 = 수정 신호
   - probe_resume_unfinished 9/9
7. **고친 사람이 안 돌린 것**: `source_audit.py` · 바뀐 파일 전체 ban-sweep (`scripts/check_review_findings.py --ban-sweep` 이 단독으로 되면 · 안 되면 이유).
8. **요청서** — 숫자 · "N/N" · "바이트 같음" · "닫힘" 을 실제 출력과 한 줄씩 대조한다 (SELF-124).  맨 위 "닫는 것 / 닫지 않는 것" 이 있는가.  작업 트리 전용 SHA 가 없는가 (SELF-116 — 메인 · origin 에 있는 SHA 만).
9. **변이 시험** — 고친 시험이 옳은 이유로 실패하는지 구현 한 줄을 틀리게 해 본다.

## 산출
- `scratchpad/prereview_unload/REVIEW2.md` (한국어 · 판정문 형식)
  - 맨 위 한 줄 = "보내도 됨 / 고친 뒤 보냄"
  - 보장 목록 표
  - 결함 표 (ID `PRE-UL2-NN` · P1/P2/P3 · 자리 · 반례 입력 · 기대 · 실제 · 최소 해결)
  - 확인했지만 결함 아닌 것
  - 못 본 것과 이유
- 탐침 · 결과는 `scratchpad/prereview_unload/u2/` (재실행 명령 포함).

## 규칙
- 60 초 넘는 실행은 `bash scratchpad/heavy.sh <명령> > <로그> 2>&1` (길면 run_in_background).
- ⚠ 지금 (11:3x UTC) 메인 게이트가 무거운 칸 둘을 다 잡고 있다 (12:30–12:45 UTC 쯤까지) — 그동안 읽기 · 작은 탐침을 먼저 한다.
- python 은 `-I`.  `nice -n 19` · `OPENBLAS_NUM_THREADS=1`.
- 디스크 여유 ≈ 4–5 GB — 큰 복사본을 쌓지 말고 끝나면 지운다.
- push · fetch · `scripts/check_all.sh` 안 함.  리포 파일을 쓰지 않는다.  봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 는 읽기만.
- 숫자 · 전칭은 실행 출력으로만.  추정은 "추정" 표지.  결함이 아닌 것을 부풀리지 않는다.
