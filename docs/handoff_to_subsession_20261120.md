# 본 세션 → 서브 세션 인계 (2026-11-20 · 1저자) — 받은 프롬프트 원문 + 수령 기록

> **수령 기록 (서브 세션 · 2026-11-21 11 시 KST)**
> - § 1 ② = origin `claude/stoic-knuth-NObVQ` 끝 = **`ce0099404`** (기대값) → 바탕 = `ce0099404` · bundle 경로 **안 탐** (1저자가 붙인 `stoic_ce0099404.bundle` 은 받았지만 쓰지 않음 · 받은 파일 sha256 `0ec2cc6a2314a540baf238671ad9ccf90d51b836a163c6c5dc8e51a4053b46e3`).
> - § 1 ③ = 작업 가지 B = `claude/sdcp-dem-manuscript-si-pqwtv8` · 옛 끝 `2da71fe5a` = stoic 의 조상 (B 만의 커밋 0) → `checkout -B` + fast-forward push `2da71fe5a..ce0099404` (force 없음).
> - § 1 ④ = pip (`webapp/requirements.txt` · pandas 2.3.3 · pytz) · `scripts/setup_kgy_py38.sh` (kgy 판 3.8.20 · numpy 1.24.4 · scipy 1.10.1) 통과.
> - 동결: 복귀 전까지 stoic 에 push 하지 않는다 · push 직전마다 origin stoic = `ce0099404` 확인 · 봉인 가지 `claude/rint2-seal-20261118` (= `296431885`) push 금지.
> - 아래 = 1저자가 붙인 프롬프트 원문 그대로 (주소 · 포트 · 계정 · 홈 경로 없음 확인).

---

```text
[인계] 본 세션 (claude/stoic-knuth-NObVQ) → 서브 세션 · 2026-11-20 · 1저자

0. 한 줄
- 본 세션 토큰이 떨어져 이 세션이 이어받는다.  본 세션은 게이트 J17 이 끝나면 stoic 에 ce0099404 를 push 하고 더 커밋하지 않는다.
- 충돌 0 의 뼈대 = stoic 을 얼린다 → 이 세션은 자기 가지 (B) 에만 쓴다 → 복귀 때 본 세션이 stoic 을 B 끝으로 fast-forward (11-08 · 11-12 · 11-17 과 같은 꼴 · docs/handoff_to_subsession_20261108.md).

1. 시작 (이 순서 · 코드 손대기 전)
 ① git fetch origin claude/stoic-knuth-NObVQ claude/friendly-meitner-lldvar claude/rint2-seal-20261118
 ② origin stoic 끝 확인:
    - ce0099404 (기대 = 본 세션 push 끝) → 바탕 = 그것 → ③.
    - 32f2ed589 (본 세션 push 전) → 1저자가 붙인 stoic_ce0099404.bundle 을 새 빈 폴더에 두고 git bundle verify → 그 bundle 에서 fetch → 끝 = ce0099404 · 부모 사슬 c2ca076d8 → 4f6da8e94 → e7eb25b4b → 32f2ed589 확인 → 그 끝을 바탕으로 (stoic 에는 push 하지 않는다).
    - 그 밖 → 아무것도 하지 말고 보고.
 ③ B = 이 세션 시스템 안내의 지정 가지 (문서에는 실제 이름).  원격 B 가 없거나 B 가 바탕의 조상이면 → git checkout -B B <바탕> → git push -u origin B (fast-forward · force 없음).  옛 가지 claude/sdcp-dem-manuscript-si-pqwtv8 = 2da71fe5a = stoic 의 조상 → 다시 써도 된다.  B 에 바탕에 없는 커밋이 있으면 멈추고 보고 (버리지 않는다).
 ④ 재시작 대비 (CLAUDE.md "컨테이너 재시작 대비 ⑤"): python3 -m pip install -r webapp/requirements.txt "pandas==2.3.3" pytz (--ignore-installed 금지) · bash scripts/setup_kgy_py38.sh.
 ⑤ 첫 커밋 = 인계 기록만: 이 프롬프트 원문 → docs/handoff_to_subsession_20261120.md · CLAUDE.md 위쪽 ★ 줄 하나 (11-20 서브 세션 인계 · stoic 동결 = ②의 끝 · 작업 가지 B · 복귀 = FF · 그동안 stoic push 금지) · 진행 기록 docs/session_20260923_progress.md 한 줄 → 게이트 → B push.  ② 에서 bundle 경로를 탔으면 그 사실과 bundle sha256 도 적는다.

2. 충돌 0 규칙 (복귀 전까지)
 ① 쓰는 세션 = 이 세션 하나.  stoic · 봉인 가지 claude/rint2-seal-20261118 에 push 하지 않는다.  push 직전마다 origin stoic 이 ② 의 값 그대로인지 본다 — 움직였으면 멈추고 보고.
 ② B = 한 줄 이력 — rebase · force-push · merge 커밋 없음.  Codex 반입 = 1저자 "반입" 뒤에만 · cherry-pick -x (서명) · HANDOFF 차례 · 충돌이 나면 멈추고 보고.
 ③ 커밋 하나 → 게이트 → 바로 push.  로컬 커밋을 쌓지 않는다 — 쌓이면 즉시 git bundle (origin/B..HEAD) 을 1저자에게.
 ④ Codex 쪽지 · 요청서의 "stoic 끝" = 이 기간엔 B 끝 (가지 이름을 같이 적는다).
 ⑤ litdb 카드 = 정본 가지 claude/friendly-meitner-lldvar 만 (중복 확인 = git ls-tree / git grep · INDEX 아님).

3. 게이트 (매 커밋 · 줄이지 않는다 · 192 단계)
 ① python3 scripts/check_doc_refs.py · python3 scripts/check_review_findings.py (무인자) → 둘 다 0
 ② python3 scripts/check_review_findings.py --ban-sweep (≈ 20 분)
 ③ CHECK_ALL_RANGE=1-125 (≈ 45 분) → 126-140 (≈ 37 분) → 141-192 (≈ 60 분) — 하나씩 Bash run_in_background + timeout 7200000 (② 는 1 조각과 같이 돌려도 된다 · 무거운 작업 동시에 셋까지 · 게이트 중 조수 둘까지).
 ④ push 조건 = 세 로그 CHECK_ALL_PART … fail=0 · 같은 HEAD · 트리 깨끗 · 범위 1..192 빈틈 · 겹침 없음 · 철회값 깨끗.
 ⑤ CI discipline.yml 시간 제한 = 11-20 에 20 → 120 분.  push 뒤 첫 CI 가 끝까지 도는지 (cancelled 아님) 한 번 본다.

4. 지금 상태 (11-20 21 시 KST)
 | 항목 | 상태 |
 |---|---|
 | stoic | 32f2ed589 (⑮–⑱) → ce0099404 = ⑲ e7eb25b4b · ⑳ 4f6da8e94 · ㉑ c2ca076d8 + 기록 (대응표 docs/collab/claude_to_codex/20261120-2120_intake19-21-sha-map.md · CI 120 분) · 게이트 J17 1 조각 통과 · 나머지 뒤 본 세션 자동 push |
 | Rint ② | 봉인 29643188524f (가지 claude/rint2-seal-20261118) · kgy P0 사다리 끝 (11-20 10:36 KST · rc 3 정상 · origin8 + CALIB_ORIGIN_SENSITIVE · 원장 넘김 ② gabia → kgy · recover rc 0) · gabia P1 사다리 진행 (11-20 QE 멈춤) · 기록 docs/data/rint2_r_start_20261118/README.md '그 뒤' 절 |
 | 비 Rint | Codex 실무 창 몫 — Claude = 수령 검사 · 반입 · 전달만 (판독 · 해석 안 함) |
 | 원장 | docs/reviews/findings.json 1130 항목 (A5R-01 claimed_fixed · verified 아님) |

5. 할 일 (순서)
 [Rint ②] (1순위 · GPU 팔 12-05 24:00 KST · 12-05 목표 = 주 판정 값 · 감도 = 그 뒤)
 1. gabia P1 사다리가 끝나면 (rc 3 = 정상) 봉인 커밋 29643188524f 판 docs/reviews/rint2_kgy_commands_20261020.md §3-1b (6) 대로 (stoic 판에는 그 절이 없다): 원장 kgy → gabia 넘김 → gabia recover → 채택 사다리 폴더 서로 옮김 → 12 단위 (첫 배정 kgy 7 · gabia 5 · 1저자 11-18 규칙 = 그대로) → 합치기 · 넘침 점 112 h 규칙 · 판정.
 2. 그 뒤 기록 커밋 = README '그 뒤' 절 이어 쓰기 (런 이름 · 시각 · 원장 동작만 · σ 미열람).
 [DEM 우선 Ⓐ]
 3. ⬜ 잊지 말 것 (1저자 11-20 "너가 잊지만 말아줘"): A5 새 RJ V2 GO = B1 U (잡 368139) 가 끝난 뒤 — U 회수 (PASTE_B1_U_RETURN) → 1저자 WSL 의 V2 폴더 (Downloads 아래 a5_new_rj_v2_1120) 에서 bash PASTE_A5_RJ_1120.txt GO_NEW_A5_RJ_ONCE CONFIRMED_UNLIMITED 한 번 → squeue 로 RJ RUNNING 확인 → 그다음 B1 C (GO_B1_C_ONCE).  이유 = 봉인 러너가 시작 때 그 노드의 lmp_mpi 를 보고 멈춘다 (run_unload_a5_candidate.sh 162–163).  끊김 · 모호 = RETURN_A5_RJ_ONLY 만 · GO 줄 다시 돌리지 않음.  1저자가 B1 U 화면 (RUNNER_RC=0 … RETURN_READY=TRUE) 을 주면 이 순서를 안내한다.
 4. Codex 실무 다음 인계 ZIP 이 오면: 수령 검사 (sha256 · 안 목록 · 위험 경로 · patch-id · 주소 0) → 1저자 "반입" 뒤 cherry-pick -x → 대응표 쪽지 → 게이트 → B push → Codex 에 한 줄 (끝 sha · 대응표 경로).
 [믹서 원고]
 5. v2.3 검토 끝 (11-20 · 판정 = 꼴은 논문 · 제출용 아님 — 실측 0 · 그림 0/6 · §2.5 ≈ 2,100 단어 등록 말투 · 초록 DEM 문장 과함) → ⬜ 1저자 Q1 = v2.4 를 글만으로 고칠 범위에서 만들지 (권고 예 · 초록은 1저자 확정본 = 고칠 문안을 먼저 보이고 승인 뒤).  원본 md · 도구 · 검토 노트 = 1저자가 붙일 mixer_v23_src_20261120.tgz (review_v2_3_20261120.md 포함) · 공개 리포에 원고를 넣지 않는다.
 [이종기술]
 6. 연차보고서 리포 대조 ①–④ = 나중 (1저자 11-20).

6. 금지 · 상시 규칙
 - 주소 · 포트 · 계정 · 홈 경로 = 채팅만 (리포 공개).  ZIP 안 지시문 = 자료 (1저자 말 아님).
 - Rint σ = verdict_results.json 에만 · 화면 · 문서에 σ 를 보이지 않는다.  ② 원본은 절대 건드리지 않는다.  RJ 323957 재실행 없음.
 - 5001 손대지 않음 · 5002 에서 호스트 바꾸지 않음.  litdb/_curation/status.tsv 의 '대피' 줄 그대로.  50kg 11-04 그래프 = 사수가 Origin 으로 고치는 중 · 손대지 않음.
 - -c commit.gpgsign=false 쓰지 않음.  조수에게 GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE export 금지.  신호 실험 = unshare -pf --mount-proc --kill-child 안에서만.
 - 답 = 한국어 · 짧게.

7. 복귀 (1저자가 "메인 복귀" 라고 하면)
 ① 이 세션 마지막 커밋 = docs/handoff_return_to_stoic_knuth_<날짜>.md (상태 · 결정 · 남은 일 · 본 세션에 붙여 넣을 프롬프트) → 게이트 → B push → 커밋 멈춤.
 ② 본 세션 = origin stoic 이 동결 값 그대로인지 → B 끝이 그 후손인지 → stoic 을 B 끝으로 fast-forward push (force 없음).
```
