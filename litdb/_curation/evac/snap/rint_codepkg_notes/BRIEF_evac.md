# Rint ② 코드 묶음 — 이어받기 지시서 (대피 세션 · 2026-11-12)

너는 본 세션 조수가 하던 일을 **끊긴 자리에서 이어받는다**.  원 지시서 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/rint/codepkg/BRIEF_codepkg.md` — 처음부터 끝까지 읽는다 (목표 · 금지 · 해야 할 것 · 답장 꼴은 그대로다).  같은 폴더의 `design.md` (설계 결정) · `notes.md` (진행 메모 — 끝 30 줄이 멈춘 자리) · `amend_drafts.md` · `gpu_check_block.txt` 도 먼저 읽는다.  아래는 달라진 것만이다.

## 자리 (원 지시서의 경로를 이렇게 바꿔 읽는다)

- 작업 트리 = `/home/user/rint-codepkg` (리포 worktree · detached · 바탕 `af3cce37b` = `11a794674` + 결정 기록 커밋 하나).  **이 트리에서만** 읽고 쓰고 커밋한다 · push 없음 · 커밋은 `git -c commit.gpgsign=false commit` (서명은 메인 세션이 반입할 때 한다).  커밋 메시지 끝 두 줄:
  `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_019HKnbzGsY9U5Gyw4qGqqzA`
- 진행 메모 · 설계 · 초안 · 기록 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/rint/codepkg/` (`notes.md` 끝에 그때그때 덧붙임 · `logs/` · `design.md` · `amend_drafts.md` · `gpu_check_block.txt`).
- 결정 기록 · 벤치 결과는 이제 리포에 있다 — 작업 트리의 `docs/reviews/rint2_time_reestimate_20261111/README.md` ("1저자 결정 (11-12)" 절) · 같은 폴더 `bench/results_20261112/`.  원 지시서가 가리키는 본 세션 scratch 경로 (`…/81c0ad95-…/scratchpad/…`) 는 이 컨테이너에 없다.
- ⛔ `/home/user/Yonghoon-DEM-DFT` (본 트리 — 시험 게이트가 돈다) · `/home/user/litdb-canon` · `/home/user/litdb-canon2` · `/home/user/litdb-ctl` 에는 아무것도 쓰지 않고, 그 안에서 명령을 시작하지 않는다.  모든 셸 명령은 `cd /home/user/rint-codepkg && …` 로 시작한다.
- kgy 판 인터프리터는 이미 깔려 있다 (`uv python find 3.8` → 3.8.20 · numpy 1.24.4 · scipy 1.10.1) — `scripts/check_kgy_py38.sh` 가 쓰는 길 그대로.  다시 깔지 않는다.
- 기계: CPU 4 · 메모리 약 15 GB · **디스크 여유 약 6 GB** · 같은 기계에서 시험 게이트 (약 2 시간) 와 논문 조수가 돈다 → 시험 · 변이는 **한 번에 프로세스 하나** · 큰 임시 파일은 쓰고 바로 지운다 · 변이용 사본은 하나만 만들어 돌려 쓰고 끝나면 지운다 (`git worktree` 를 여러 개 두지 않는다 · 리포 전체 복사 금지 — 필요한 파일만).
- 신호를 보내는 시험은 원 지시서대로 PID 이름공간 안에서만 (`unshare -pf --mount-proc --kill-child …`).

## 지금 상태 (본 세션 조수가 멈춘 자리)

- 시험 먼저 커밋 = 이 트리의 `ebb0e9f80` (원래 `71b0d145f` · 시험 파일 셋 · 내가 cherry-pick 했다).
- 구현 = **커밋 전** · 작업 트리에 그대로 있다 (추적 파일 12 개 수정 + 새 `scripts/cjunc_store.py`) — 본 세션 조수의 diff 와 새 파일을 내가 그대로 얹었다.  먼저 `git status` · `git diff --stat` 로 확인한다.
- 3.11 묶음은 본 세션에서 끝났다 (notes.md 의 숫자).  probe6 대역 고침 뒤 다시 돌린 것 · webapp provenance · 덧 묶음 결과는 넘어오지 않았다.  kgy 판 묶음 · 변이 · GPU 확인 블록 자리표 · 개정 초안 마무리는 아직이다.
- 본 세션의 변이 도구 (`work/mutate.py` · 변이 25 개) 와 GPU 하네스 파일 (`gpu_check/q11_gpu_check.py`) 은 넘어오지 않았다 — `notes.md` · `design.md` · `gpu_check_block.txt` 를 보고 다시 만든다 (블록 글 안에 하네스가 들어 있으면 그것을 쓴다).

## 할 일 (차례)

1. 상태 확인.  시험 먼저 커밋의 시험이 **고치기 전 판** 에서 옳은 이유로 실패하는지 한 번 본다 (`git stash` 는 쓰지 않는다 — `git show ebb0e9f80:<파일>` 로 필요한 파일만 임시 폴더에 꺼내 돌린다).  notes 의 기록 = Q11 10/13 · store 0/21.
2. 구현 마무리 (notes 의 남은 것: probe6 · webapp provenance 의 가짜 cupyx 대역 · T12 · 안 쓰는 import 등) → **구현 커밋 하나**.
3. 전체 시험 — store 시험 T · P · R · C 전체부터, 이어서 원 지시서 3-3 의 목록 전부를 Python 3.11 → kgy 판 차례로.  통과 수 · 걸린 시간을 `logs/` 와 notes 에.
4. 변이 — 새 규칙마다 하나 이상 (지문 대조 · 저장본 거부 · C 꼴 · 발행 전 대조 · 봉인 원천 금지 등).  잡힌 수 / 넣은 수 · 안 잡힌 것은 동등 변이인지 가린다.
5. GPU 확인 블록 (`gpu_check_block.txt`) 의 자리표 (Q11REPO · Q11PIN · sha256) 를 구현 커밋 기준으로 채운 초안 · 개정 문장 초안 (`amend_drafts.md`) 마무리.  블록은 돌리지 않는다 (GPU 없음).  리포의 등록 · 원장 · 계획 문서는 고치지 않는다 (초안만).
6. 답장 = 원 지시서 5 절의 12 줄 꼴 (커밋 sha 둘 · 바꾼 파일 · 시험 고치기 전 → 뒤 · 기존 시험 통과 수와 시간 (3.11 · kgy 판) · 변이 결과 · S0 단계 1 다시 필요 여부 · 초안 자리 · 고치지 않은 것 · 미확인).

끝나면 메인 세션이 독립 조수에게 내부 반박 리뷰를 맡긴다 — 스스로 리뷰어를 띄우지 않는다.  확인하지 않은 것을 확인했다고 적지 않는다.
