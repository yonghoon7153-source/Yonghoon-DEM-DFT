# FAM §12-7 발사 러너 (gabia · 11-04 · 결과 0 건)

등록 = `docs/reviews/fam_platen_prereg_20260812.md` §12-7 · 12-7-1 · 12-7-2 (corner 세 팔 `--platen-mach 0.0099999` 개정).  발사 절차 = 같은 문서 12-7-3.  발사 = 1저자.

| 파일 | md5 | 무엇 |
|---|---|---|
| `run_s127.sh` | `6e4b12b8cd296ec7b00376de07cf46b4` | 발사 러너 (288 줄) |
| `test_run_s127.sh` | `92f9333823a1cb6df7e28918a1676579` | 시험 틀 (가짜 HOME · 가짜 `$PY` · git · nvidia-smi · pgrep · sleep · date) |
| `expected_argv.py` · `argv_diff.py` · `argv_diff.txt` | — | 등록 문안 (970–986 행) 과 건식 줄 (19-1 … 19-4) 을 따로 읽어 만든 기대 argv · 러너 argv 와의 대조 |
| `mutation_check.sh` · `mutation.log` | — | 결함 하나씩 넣은 러너 사본 18 |
| `placeholder_runner.sh` · `before.log` | — | `exit 0` 자리 표시 러너에 같은 시험 (고치기 전 판 대신) |
| `after.log` | — | 러너에 시험 |

## 러너가 하는 일

- **앞머리** (하나라도 다르면 `REFUSED` · python 을 한 번도 띄우지 않는다): `SEAL_COMMIT` = `7f44d6534` · `git -C ~/fam-wt rev-parse HEAD` = `7f44d6534d864f7be2f3310fa55d213b65cc707d` · `scripts/mpm3d_compaction.py` md5 `c31f0512021d416702e162709c6f4400` · CSV 넷 sha256 (12-7-1 ② 표) · `$PY` 있음 · 출력 8 개 없음 (덮어쓰지 않는다) · STOP 없음 · 기한 전 · `pgrep -af '[m]pm3d_compaction.py'` 없음 · GPU 한 장 · 총 49140 MiB · 마지막에 `$PY` import (판 넷을 기록).  러너 자신의 md5 · 판 · GPU 총 · 여유를 `~/fam_s127/batch_s127.log` 에 적는다.
- 시작 줄 `§12-7 시작 <KST 시각>` = 등록의 발사 시각.
- **팔** = confirm_fb → corner_fb → corner_fa → corner_f0 (한 GPU · 한 번에 한 팔) · argv = 등록 문안 그대로 (다른 것 = `$PY` 자리 · `<OUT>` = `~/fam_s127` · corner 세 팔의 `--platen-mach 0.0099999`).
- **팔마다 앞 점검** (다르면 `SKIP` · 그 팔 안 띄움 · 배치 끝): 기한 · STOP · pgrep · GPU 총 · corner 는 여유 ≥ 31,858 MiB (앞 팔이 끝난 뒤 10 s 기다림) · 그 팔의 출력 없음.
- **도는 동안** 60 s 마다: 기한 (11-21 12:00 KST) 이 지났거나 `~/fam_s127/STOP` 이 생기면 TERM → 120 s 안에 안 끝나면 KILL · `STOPPED` · 다음 팔 없음 (그 팔 = 미완주 · 실패 아님 · 판정 없음).  10 분마다 `HB` (프레임 줄 **수** 만) · corner_fb 1 시간 뒤 `ETA` 한 줄 (보고만 · 바꾸는 것 없음 · 프레임 줄 1 = 5 프레임으로 셈 — 수렴 확인 구간은 줄이 더 자주 찍혀 어림).
- **팔 끝** `END` 줄 = rc · 시각 · 걸린 시간 · 프레임 줄 수 · JSON 있음 (필드 수) · 상태 낱말 (로그를 조용한 grep 으로만: cuda_oom · cuda_error · traceback · converged · not_converged_… · qs_gate_refused · stop_gate_refused · no_converged_marker · unknown).
- **확인 런 기술 관문** (등록: python · CUDA 오류 · 400 안 미수렴이면 corner 를 띄우지 않고 1저자에게) = rc 0 ∧ JSON ∧ Traceback · CUDA_ERROR 없음 ∧ 로그에 `✓ converged: σzz equilibrated at target` — 아니면 `CONFIRM_GATE_FAIL` · 끝.
- corner 팔이 어떤 rc 로 끝나도 다음 corner 팔로 간다 (팔마다 등록된 시도 · 분류는 결과 뒤 12-4 표) · **자동 재시도 없음** (메모리 부족 포함 — `cuda_oom` 표지만 · 재시도 = 1저자 결정).
- 종료 코드: 0 팔 넷 끝 · 2 REFUSED · 3 SKIP · 4 STOPPED · 5 CONFIRM_GATE_FAIL.
- **열람 규칙** (12-6-1 · `SELF-80`): 러너는 팔 로그의 줄 · 값을 옮기지 않는다 — 밖으로 내는 숫자 = 프레임 줄 수 · JSON 필드 수 · rc · 시각뿐.

## 시험 (11-04 · 이 컨테이너 · 실제 GPU 없음)

| | 결과 |
|---|---|
| `bash -n` | 두 파일 통과 |
| 자리 표시 러너 (`exit 0`) | 747 중 447 통과 · **300 실패** (64 시나리오 중 63 이 하나 이상 실패 · 통과 = "값 안 샘 · python 안 부름" 같은 빈 부정) — `before.log` |
| `run_s127.sh` | **747 / 747** (리포 자리에서 다시 돌림 · 처음 판 (스크래치 자리) 과 경로 줄 밖 같음) — `after.log` |
| 변이 18 (개정 빠짐 · 확인 런에 개정 · fa/fb 순서 · f0 플래그 빠짐 · 관문이 표지 · JSON 무시 · END 줄이 로그 줄을 찍음 · 여유 문턱 `-le` · 앞머리 기한 `-le` · corner 실패 뒤 배치 멈춤 · HB 5 분 · ETA ×5 빠짐 · KILL 없음 · STOP 안 봄 · 시작 줄이 앞머리 앞 · 앞머리 전 python · md5 안 봄 · 팔 앞 pgrep 빠짐) | **18 / 18 잡힘** — `mutation.log` (스크래치 자리 틀로 돈 것 · 틀은 그 뒤 경로 셋만 바꿈: `REPO` · 시험 자리 `BASE` · 봉인 코드 사본 = `git show 7f44d6534`) |
| argv | confirm_fb 42 / 42 낱말 차이 없음 · corner 셋 44 / 44 · 44 / 44 · 45 / 45 = 23 번째 `--platen-mach 0.01 → 0.0099999` 하나만 — `argv_diff.txt` |

다시 돌리기: `bash docs/reviews/fam_s127_runner/test_run_s127.sh` (기본 시험 자리 = 새 임시 폴더 · `FAM_RUNNER_TEST_DIR=<폴더>` 로 바꿈 · 리포 안에 쓰지 않는다).

## 등록을 읽으며 정한 것 (결과 0 건 · 다르게 읽어야 하면 발사 전에 고친다)

1. 개정은 COMMON7 안 23 번째 낱말을 바꿨다 (`--platen-mach` 를 하나 더 붙이지 않았다).
2. 앞머리 차례 — `$PY` import 를 맨 뒤에 (그 앞 거부는 python 을 부르지 않는다).
3. 여유 메모리 문턱 (31,858) = corner 팔 앞에서만 · 앞머리 = 총량 검사 + 여유 기록.
4. 확인 런 관문 = 표지 줄 필요.  ⚠ 봉인 코드는 예산 끝에 밴드 안이면 표지 줄 없이 `converged` 로 끝날 수 있다 (봉인 코드 3502–3505 · 3580–3581 행) → 그때 러너는 corner 를 띄우지 않고 멈춘다 (보수 쪽 · 1저자가 본다).
5. 상태 낱말은 로그에서만 (이 argv 의 JSON 에 `servo_status` 칸이 없다).
6. 시각 = KST (`TZ=KST-9`) · 기한 epoch 1795230000 (= 2026-11-21T03:00:00Z) · `지금 < 기한` 엄격.
7. 내가 더한 것 둘: 팔마다 그 팔 출력이 있으면 거부 · corner 앞 10 s 기다림.
8. 멈춤 지연 = 감시 60 s + TERM 기다림 120 s → 기한 뒤 최대 ≈ 3 분 (≈ 12:03 KST).
9. TERM · KILL 대상 = python (exec 라 `$!` = python) · 등록의 `pkill -f` 메모는 setsid 로 띄운 런 이야기라 여기선 쓰지 않는다.

## 시험 못 한 것

실제 GPU · Taichi · 실제 CUDA 오류 문구 · 끝난 뒤 GPU 메모리가 풀리는 속도 · Taichi 가 TERM 에 끝나는지 (가짜는 143 으로 끝나거나 TERM 을 무시해 KILL 137) · 실제 `nvidia-smi` 꼴 (12-7-2 기록 `49140, 48539` 꼴로 흉내) · 며칠 실시간 (가짜 시계) · gabia import 줄 (가짜 모듈) · 실제 `git worktree` (얕은 클론으로 대신 — 7f44d6534 통과 · 한 커밋 뒤 거부) · tmux 띄우기 · 창에서 Ctrl-C (러너만 멈추고 도는 팔은 남을 수 있다 → **멈출 때는 STOP 파일**) · 시나리오 없는 가지 (OUT mkdir 실패 · `cd ~/fam-wt` 실패 rc 97 · 판 줄 없는 import · pgrep 오류 rc · 기한 + STOP 동시 · 러너 둘 동시).
