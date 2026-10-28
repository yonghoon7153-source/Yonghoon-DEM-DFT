# 우리 트리 재현 — Codex KG50 재개 도구 재검토 (10-28 · 리뷰 핀 `f118c1fd1`)

- 환경: 이 리포의 클라우드 컨테이너 (Linux · GNU bash 5.2.21 · awk = mawk · Python 3.11.15) · 10-28 18:0x KST.  DEM · MPI · 실제 SLURM · ibb 접속 없음 (가짜 sbatch / sacct / squeue / sleep 만).
- 대상 코드: `scripts/resume_ckpt.sh` sha256 `e59c43e688b2b9a6c23a337ceee2b28214ed3f6c76bd69b7f2402f926336dae8` = 리뷰 핀 바이트 (핀 뒤 `scripts/resume_ckpt.sh` · `scripts/test_resume_ckpt.py` · `docs/resume_ckpt_procedure_20260927.md` 변경 없음 — `git diff f118c1fd1 HEAD` 빈 출력 · HEAD `17958c677`).
- Codex 는 Windows 에서 Bash 를 띄우지 못해 셸 경로 둘 (KG50R-04 · 시험 절단 awk) 을 실행하지 못했다 (판정문 §0).  아래 ① ③ ⑤ 가 그 빈칸을 우리 쪽에서 실제로 돌린 것이다.

| # | 무엇 | 결과 | 파일 |
|---|---|---|---|
| ① | KG50R-04 — Codex 탐침 (`docs/reviews/codex_kg50_resume_recheck_20261028/independent/scheduler/probe_stale_trial.py`) 을 받은 ZIP 을 푼 폴더에서 그대로 Linux 로 (옛 시험 job 7001 · mode · 로그를 남긴 작업 폴더 + 이번 호출에서 시험 제출 없음) | **EXECUTED · 두 장면 모두 본 제출** — 큐에 그 케이스 있음 (`⛔ … 이 큐에 있음 — 건너뜀`) · squeue 조회 실패 (`⛔ squeue 조회 실패 — 건너뜀`) 둘 다 둘째 고리가 옛 7001 을 읽어 G0–G3 통과 → 가짜 sbatch 한 번 = `run_kg50_d07_b40_r56.sh` (본 러너) · 보고 `✅ 본 제출 job 9001` | `stale_trial/` (stdout · stderr · sbatch_calls · 보고 md · `stale_trial_results.json`) |
| ② | Codex 덱 탐침 셋 (`reproduce_deck.py` · `probe_trial_steps.py` · `probe_state_observability.py`) 을 Linux 에서 다시 | 판정값 23 행 (정적 13 · `--fix-run` 4 · `--strip-comments` 2 · after_settling 3 · 압축 루프 1) = Codex 와 **차이 0** · trial_steps 2 행 같음 · 상태 관측 산술 같음 | `deck/` |
| ③ | KG50R-02 · KG50R-05 의 시험 덱 — 693 줄 awk 절단기 그대로 (mawk) 를 Codex 변이 덱 15 개에 | 15/15 = Codex 전사와 같음 (13 바이트 같음 · 2 = CR 만 다름: Codex 가 Windows text 모드로 쓴 CRLF 고정물) · `first_run_every` → `run 2000` (every 사라짐) · 계속 줄 → `run &` / `180000` / `run 1` / `run 2000` | `awk_trial/table.txt` (`repro_ours.sh`) |
| ④ | KG50R-01 — 실제 bash `resume_ckpt.sh -C` 로 09-27 r075 압축 쌍 | `루프 몸 run 같음 … [label loop_press] [run 5000]` · **통과 (문제 0) · rc 0** · 산술 = 다음 판정 1,500,002 → 1,505,000 (4,998 step 늦음) · 소급 = r075 정지 시점 차 2 step (`r075_retro.md`) | `r075_bash_C/out.txt` · `r075_retro.md` |
| ⑤ | Codex Q1 의 G0 파싱 보강 (판정문에서는 "AWK 동적 재현 안 함") — 우리 640–648 줄 함수 그대로 (`funcs_from_ours.sh`) | `lastrun` 이 한 토큰 `22001` 줄을 마지막 thermo 로 잡음 (`22001 5 6` = LTS 22001 · Loop 줄 번호 6 > 5) ⇒ G0 의 step · Loop 조건 통과 · 엄격한 `tl` 은 그 줄을 못 만든다 · G3 = 첫 줄만 수치 비교 (공개된 설계 · 새 결함 아님) | `g0_lastrun/` → 원장 새 P3 `KG50R-07` |

- 하지 않은 것: 실제 ibb SLURM · `dem_restart.py` · LIGGGHTS.  저자 시험 87 개는 게이트 단계 `resume_ckpt (재개 도구 · 가짜 SLURM)` 가 매 게이트 돌린다 (이 재현과 별도).
- 다시 돌리기 (리포 뿌리): ①② = 받은 ZIP 을 빈 폴더에 풀고 그 안에서 Codex `REPRODUCE.md` 의 명령 (탐침 원본 = `docs/reviews/codex_kg50_resume_recheck_20261028/independent/scheduler/probe_stale_trial.py` 등 · ZIP 안에서는 `repo/` 가 옆에 있어야 돈다) · ③④ = `bash docs/reviews/codex_kg50_resume_recheck_20261028/_repro_ours_20261028/repro_ours.sh <빈 임시 폴더>` · ⑤ = `bash …/g0_lastrun/run.sh …/g0_lastrun`.
- ⚠ 결함이 남은 코드에서 반례가 rc 0 · "통과" 를 내는 것 = **결함 재현**이다 (제품 통과가 아니다).
