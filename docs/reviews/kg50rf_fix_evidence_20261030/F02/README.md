# KG50R-F02 — 검사한 덱 ↔ 잡이 읽는 덱 결속 (10-30 · 증거)

> ※ 10-30 통합: 이 문서의 커밋 SHA 는 본 가지 (claude/stoic-knuth-NObVQ) 에 들어간 SHA 로 바꿔 적었다 (작업 트리 가지 SHA 는 원격에 없어서 통합 SHA 로 바꿨다).


- 결함: Codex 재확인 (2026-10-30 · 리뷰 핀 bf8cf21c6 · 판정문 §2 KG50RF-02 · §7 영수증 한정 · 판정문 반입은 메인 세션 몫) = 원장 KG50R-F02 (P1).
  러너 관문이 부분 글자 grep 셋이라 `-in …r56.liggghts.bak` 러너 · 주석 속 정상 줄 · 다른 cd · 둘째 MPI 실행이 통과했다 · 시험 러너 = 헬퍼 러너의 sed 사본 ·
  실행 영수증 `main_inputs.sha256` = 재개 덱 · 러너 둘 (체크포인트 sha256 은 tool.txt 기록만 · lmp_mpi sha256 = 제출 셸 PATH).
- 비준 설계: 1저자 10-30 Q2 *"권고대로"* — (1) 헬퍼 러너 줄마다 엄격 대조 (2) 본 · 시험 러너를 도구가 한 틀로 씀 (3) 실행 입력 영수증 다섯 + 본 제출 바로 전
  다시 대조 (4) 가짜 sbatch 가 러너를 실제로 돌리는 시험.
- 바꾼 파일: `scripts/resume_ckpt.sh` (새 함수 runnerck · 러너 · 영수증 · 본 제출 구간) · `scripts/test_resume_ckpt.py` (가짜 sbatch · 가짜 mpirun ·
  가짜 dem_restart.py 러너 · RB 묶음).  정적 대조 Python (setup_check · setup_order · state_cmp) 은 손대지 않았다 (같은 때 다른 작업 트리가 고치는 자리).
  파일 머리 주석 (1–48 줄) 에도 이번 절을 안 넣었다 — 그 자리를 다른 작업 트리도 고칠 수 있어 병합 때 메인 세션이 한 줄 넣는다.
- 도구 sha256: 고치기 전 77c242375c4093023e609703ef471c64c2370d374e7533824412d96da5b1b9f8 → 1 판 5f4ffb46ae70ad3926685f891c25daed721dd37a42bc3a3079a31e6eca4f188e
  → **2 판 e5a6118102dee3a8fcd28c9163d5d1868e3d9db6089365348ff937eaedae44da** (§0 · 독립 사전 공격 PA-01–10 대응).
- 작업 가지 커밋 (worktree-agent-ab1d2d1fe4868ba68 · 메인 세션이 옮기면 번호가 바뀐다): 1 판 = 시험 먼저 5c8f2e126 · 고침 07761cf54 · 증거 c43744a34 ·
  2 판 = 시험 먼저 221f57dbf · 고침 48cfd2871 · 증거 = 이 폴더의 `r2/` 와 §0 을 넣은 커밋.
- ⚠ **§0 이 최신이다.**  §1–§9 = 1 판 (도구 5f4ffb46) 기록 그대로 — 2 판이 바꾼 자리에는 그 줄에 *[2 판]* 표지를 달았다.
- 환경: 클라우드 컨테이너 (Linux · GNU bash 5.2.21) · 가짜 SLURM (sbatch · sacct · squeue · sleep) · 가짜 mpirun · 가짜 dem_restart.py —
  실제 ibb SLURM · MPI · LIGGGHTS 실행 없음.
- ⚠ 작업 도중 컨테이너 디스크가 한때 가득 찼다 (메인 세션 알림 · ENOSPC).  그 창에 돈 첫 변이 판 (40 개 중 2 개에 엉뚱한 실패) 은 버렸고, 커밋을 다시 만든 뒤
  before · after · 변이를 전부 새로 돌렸다.  아래 기록은 다시 돈 것뿐이다 (기록마다 'No space left' 줄 0 — §3 표).

## 0. 2 판 — 독립 사전 공격 리뷰 (PA-01–10) 대응 (10-30 · 이 절이 최신)

- 리뷰: 메인 세션이 전한 독립 사전 공격 (대상 = 이 가지 끝 c43744a34 · 도구 5f4ffb46) — 새 P1 없음 · P2 셋 (PA-01 · 03 · 04) · P3 일곱 (PA-02 · 05–10).
  리뷰어 도구 (장면 attack.py · 탐침 rck_probe.py · sed_e_probe.py · cdfail_probe.py · 변이 mutate_rev.py 28 개 — 메인 세션 스크래치 · 리포 밖) 로
  고침마다 확인했고 장면은 RB 묶음의 상주 시험으로 옮겼다 (같은 꼴을 시험 하네스에서 만든다).
- 차례: 시험 먼저 (221f57dbf · 고치기 전 도구에서 RB 41 실패) → 고침 (48cfd2871 · 도구 e5a61181) → 증거 (이 절 · `r2/`).
  정적 대조 Python (deckcheck · 첫 1033 줄) 은 손대지 않았다 — 첫 1033 줄 sha256 = bf8cf21c6 · 5f4ffb46 와 같음 (d0dc0cf4… · `head -1033`).
- 바꾼 파일: `scripts/resume_ckpt.sh` (러너 · 제출 구간 · runnerck) · `scripts/test_resume_ckpt.py` (하네스 · RB 묶음) · 이 폴더 `r2/` · 이 README.

### 0-1. 고친 것 · 시험 · 고치기 전 도구 (5f4ffb46) 가 한 일 (기록 = `r2/before/before_py311_mawk.log` · 돈 잡 sha256 앞 12 · 검사한 재개 덱 b73b508611c2 · 시험 덱 038267335faa)

| 리뷰 | 고친 것 (도구 e5a61181) | RB 시험 | 고치기 전 도구 (같은 시험) |
|---|---|---|---|
| PA-01 (P2) 시험이 다른 바이트를 읽어도 G0 통과 (신원 줄 = 기록만 · -T 는 다시 대조도 없음) | 시험 로그의 신원 줄 = **G0 관문** (-T · 본 흐름 같게): `^LMP_IDENTITY ` 줄 정확히 하나 · 그 덱 경로 = 검사한 시험 덱 절대 경로 · 덱 sha256 = 시험 전에 쓴 영수증 셋째 줄 (이 호출 메모리 `SUBMITTED` 넷째 · 다섯째 칸 — 시험 뒤 영수증 파일을 다시 읽지 않는다) · 아니면 G0 실패 + 보고 `- G0 잡 안 덱 신원 (10-30 KG50R-F02 · 관문): 실패 — <까닭>` · 신원 줄에 체크포인트 경로 · sha256 더함 (G0 에서는 기록만) | RB40 (리뷰어 T_swap · -T) · RB41 (swap_restore) · RB44 (신원 줄 두 개) · RB44b (덱 경로만 다름) · RBP h | RB40 시험이 바뀐 덱 (bb578f2de764) 을 읽고 G0 통과 → -T "시험만" 통과 · RB41 같은 시험 뒤 본 제출 · RB44 · 44b G0 통과 |
| PA-02 (P3) 본 제출 직전 대조 **뒤** 본 잡 시작 (큐 대기) | 러너가 잡 시작 때 덱 · 체크포인트 sha256 (`ds` · `ks`) 을 runnerck 가 읽은 값 (러너 글에 박힘) 과 대조 → 다르면 `LMP_IDENTITY_MISMATCH` 한 줄 + `exit 1` (mpirun 안 함) · 시험 러너도 같은 틀 (시험 덱 · 체크포인트) · 보고에 `- ⛔ 잡 안 sha256 대조 다름 — mpirun 안 함` (시험 로그에 그 줄이 있으면) | RB43 (리뷰어 main_toctou) · RB42 (체크포인트가 시험 잡 동안만 바뀜) · RB40 · 41 | RB43 본 잡이 큐 대기 중 바뀐 재개 덱 (4d158ebbc9f7) 을 읽음 · RB42 바뀐 체크포인트로 시험 · 본 제출 |
| PA-03 (P2 · 원인은 F02 전부터 — 77c24237 도 `cp -a $S $W`) 멈춘 폴더가 링크 | `[ -L "$S" ]` = 복사 · 쓰기 전 거부 (단계 "멈춘 폴더") | RB48 (리뷰어 symlink_stopped) | 시험 · 본 잡이 **원 런 폴더** (…/elsewhere/kg50_d07_b40.ins1) 에서 돎 · 원 로그 이름이 바뀜 (멈춘 폴더 바뀜) |
| PA-04 (P2) 환경 줄 허용 목록 음성 없음 (변이 E1–E3 살아남음) | 셋 꼴 그대로 (`source ~/.bashrc` · `conda activate <이름>` · `export (OMP\|MKL\|OPENBLAS\|NUMEXPR)_NUM_THREADS=1`) · conda 이름 첫 글자 = A-Z a-z 0-9 _ (`.` · `..` · `-h` 거부 — 받을 까닭 없음: D2 러너 = `conda activate myenv`) · `source` · `.` · `conda` · `export` 로 시작하는데 셋 꼴이 아니면 `받는 꼴이 아닌 환경 줄` | RB32a–j (환경 줄 뒤 `;` 명령 · `export PATH` · `LD_PRELOAD` · `OMP_NUM_THREADS=2` · `source /tmp/x` · `. ~/.bashrc` · `conda activate myenv; mpirun …` · `conda activate .` · `..` · `-h`) | h · i · j (`conda activate .` · `..` · `-h`) = 받아서 시험 · 본 제출 · a–g = 이미 거부 (다른 문구 — 새 문구를 기대해 실패 · 변이 E1–E3 를 잡는 자리) |
| PA-05 (P3 · 회귀) 실제 경로에 ERROR | ERROR 셈에서 신원 줄 (`^LMP_IDENTITY `) 을 뺀다 — 그 밖 줄은 예전처럼 어디든 ERROR 글자 | RB47 (리뷰어 error_in_path) | 시험만 · 본 0 (신원 줄의 경로로 ERROR 1 → G0 · G1 실패) |
| PA-06 (P3) `-x r56/x` | `-x` = `^[A-Za-z0-9_]+$` · cd · 보고 · 작업 폴더 전 시작 거부 (종료 코드 1) | RB50 (리뷰어 sfx_slash 준비 그대로) · RB24 | RB50 본 잡이 `x.liggghts` (fc7cd46b6de0 · 검사 안 한 덱) 를 돎 · RB24 = 보고 · 작업 폴더를 만든 뒤 루프에서 거부 |
| PA-07 (P3) `-n` 이 sed 프로그램에 | `-n` = `^[1-9][0-9]{0,5}$` · 같은 자리 시작 거부 | RB49 · 49b (리뷰어 np_sed · sed_e_probe) · RB21 | RB49b sed 의 e 명령이 표지 파일 (SED_E_RAN) 을 만듦 · RB21 = 루프에서 거부 |
| PA-08 (P3) cd 실패에도 mpirun | 틀 `cd "…" \|\| exit 1` | RB46 (잡에서만 cd 가 1 을 돌려주는 BASH_ENV) | 시험 · 본 잡이 cwd = 제출 폴더 (…/root) 에서 돎 |
| PA-09 (P3) 셸 함수 mpirun | 틀 `command mpirun …` · ~/.bashrc · 제출 환경 BASH_ENV = 믿는 입력 (§0-2) | RB45 (리뷰어 bashenv) | 시험 · 본 잡 둘 다 `other.liggghts` (69cb79c1fea9) |
| PA-10 (P3) 시험 `pos()` 가 `sha(None)` 에서 죽음 | `sha(None)` = 실제 sha256 과 같을 수 없는 표지 · `pos()` 는 그 칸만 실패 | (하네스) — 변이 91 기록에 Traceback 0 (§0-5) | — |
| 같은 김 | `#SBATCH --qos` · `--partition` 값 = 쉼표로 나눈 낱낱이 A-Z a-z 0-9 로 시작 · runnerck 쓰기 실패 때 임시 파일 지움 | RB34 (`--qos=cpu-60,--exclusive`) · RB35 (시험 러너 자리 폴더 → 종료 코드 2 = 러너 관문 거부) | RB34 받아서 시험 · 본 제출 · RB35 작업 폴더에 `run_kg50_d07_b40_r56t.sh.tmp<pid>` 가 남음 |

고치기 전 도구에서 RB 실패 41 (네 환경 같은 41 칸):
- **행동 실패** (잘못 제출 · 잘못 돎 · 흔적) 17 = RB32h · i · j · RB34 · RB40 · 41 · 42 · 43 · 44 · 44b · 45 · 46 · 47 · 48 · 49b · 50 · RB35 (임시 파일) — 위 표 오른쪽 열.
- **시작 거부 꼴** 3 = RB21 · 24 · 49 — 고치기 전도 제출은 안 했지만 보고 · 작업 폴더를 만든 뒤 루프에서 거부 (RB49 는 그 전에 sed e 명령이 돌았다 = RB49b).
- **문구** 7 = RB32a–g (이미 거부 · 다른 문구).
- **새 틀 · 인터페이스** 14 = RBP1 · RBP2 의 d (틀) · g (신원 줄 = 체크포인트 칸 · 한 줄) · h (G0 관문 줄) · i (본 잡 로그 신원 줄) 8 · RBU1–6 (runnerck 인자 11 — 고치기 전은 10 이라 종료 코드 2) 6.
- 합 17 + 3 + 7 + 14 = 41.  고치기 전에도 통과하는 새 칸 (변이 잡이) = RB33 · RB36 · RB36b · RB37.

### 0-2. 정한 것 · 남은 틈 (리뷰어가 물은 것)

- **PA-02 = 잡 안 대조를 넣었다** (리뷰어 "싸고 새 실패 꼴이 없으면" 조건): 값 = 잡 시작 때 덱 · 체크포인트 한 번씩 읽기 (체크포인트가 크면 그만큼 읽기 시간).
  새 실패 꼴은 **안전한 쪽 둘** — ① 잡 환경에 `sha256sum` · `cut` 이 없으면 `ds` · `ks` 가 비어 mpirun 전에 멈춘다 ② 바이트가 바뀌면 멈춘다 (의도).
  남는 틈: 그 대조 ↔ LIGGGHTS 가 파일을 여는 사이 (mpirun 시작 · 초 단위) · 본 잡 출력 (`logs/output_<C>_<SFX>_<job>.out`) 은 도구가 **읽지 않는다** (본 sbatch 뒤 끝) —
  본 잡의 대조 결과는 그 잡 로그에만 (`LMP_IDENTITY` · `LMP_IDENTITY_MISMATCH` 줄 · 사람이 본다).
- **PA-01 의 체크포인트**: 신원 줄의 체크포인트 경로 · sha256 = G0 에서는 기록만 (요청대로) — 체크포인트 대조는 잡 안 대조가 한다 (RB42).
- **-T 의 다시 대조**: -T 는 본 제출이 없어 영수증 다시 대조 (`sha256sum -c`) 를 안 한다 — 시험 덱 · 체크포인트는 잡 안 대조 + G0 신원 관문이 덮는다 ·
  시험 러너 파일이 sbatch 뒤 바뀐 것은 -T 에서 다시 안 본다 (-T 가 찍는 본 제출 명령은 새 시험부터 다시 돈다).
- **PA-03 원인 = F02 전부터** (77c24237 의 `cp -a $S $W` 그대로) · 멈춘 폴더 **안** 의 링크 (예: 절대 경로 링크 본 덱 · 링크 restart 폴더) 는 그대로 링크로 복사된다 — 이번에 안 바꿈 (기존 시험이 링크 본 덱 장면을 본다 · 범위 밖).
- **PA-09**: `command` 는 셸 함수 mpirun (~/.bashrc · 제출 환경의 BASH_ENV · 내보낸 함수 어느 출처든 bash 의 함수 찾기는 같다) 을 건너뛴다.
  ~/.bashrc · BASH_ENV · 잡 환경 PATH 는 **믿는 입력** — `cd` · `sha256sum` · `[` 같은 다른 이름을 그쪽에서 바꾸는 것까지는 막지 않는다.
  가짜 sbatch (dash) 는 이름에 `%` 가 든 환경 변수 (`BASH_FUNC_mpirun%%` · 내보낸 함수) 를 넘기지 못해 그 장면은 이 하네스에서 못 본다 (리뷰어 bashfunc 장면도 같은 까닭으로 고치기 전 · 뒤 다 정상) — BASH_ENV 장면 (RB45) 이 같은 함수 찾기를 본다.
- **신원 줄 관문의 새 실패 꼴 (안전한 쪽)**: 환경 줄 (`source ~/.bashrc` · `conda activate`) 이 줄 끝 없이 글을 남기면 신원 줄이 그 줄 뒤에 붙어 `^LMP_IDENTITY ` 가 0 개 → G0 실패 (제출 없음 · 보고 "LMP_IDENTITY 줄 0 개").  ibb 에서 -T 한 번으로 확인할 일.
- **고친 말 (1 판)**: 1 판 고침 커밋 (07761cf54) 메시지의 "환경 줄 넷 꼴" 은 **틀렸다** — 코드는 처음부터 셋 꼴 (`source ~/.bashrc` · `conda activate` · `export <넷>_NUM_THREADS=1`) 이다.
  1 판 변이 41 (§6) 에는 환경 줄 (ENVL) 변이가 **없었다** — 이번 판에 넣었다 (VE1–VE3 · N45 · N46 · §0-5).
- **리뷰어 np_sed 장면의 꼬리**: attack.py 의 `-n '56/;e touch …;s/^/'` 는 e 명령의 sh 가 구문 오류로 멈춰 표지를 **못 만든다** (실측 `r2/preattack/sed_e_tail_probe.log` M1) · 꼬리 ` #` (M2) · 줄 바꿈 (M3) 은 만든다 → RB49 는 ` #` 꼴 (고치기 전 도구에서 표지 생김).
- **시험 장면 RBR1 · RBR3 옮김**: 시험 덱 · 체크포인트를 시험 제출 때 (잡 시작 전) 고치면 이제 잡 안 대조가 먼저 막으므로 (RB41 · 42) 잡이 끝난 뒤 (`FAKE_POST_TRIAL`) 고쳐 본 제출 직전 영수증 대조를 따로 본다.

### 0-3. 결과 (기록 = `r2/before/` · `r2/after/` · 'No space left' 줄 0 · Traceback 0)

| 환경 | 고치기 전 (도구 5f4ffb46 · 시험 = 221f57dbf) | 고친 뒤 (도구 e5a61181) |
|---|---|---|
| Python 3.11.15 · awk = mawk 1.3.4.20240123 | `266 PASS · 41 FAIL` | `307 PASS · 0 FAIL` |
| Python 3.11.15 · awk = GNU Awk 5.2.1 | `266 PASS · 41 FAIL` | `307 PASS · 0 FAIL` |
| Python 3.8.20 (하네스) · mawk | `266 PASS · 41 FAIL` | `307 PASS · 0 FAIL` |
| Python 3.8.20 (하네스와 도구 안 python3) · mawk | `266 PASS · 41 FAIL` | `307 PASS · 0 FAIL` |

- 고치기 전 실패 41 = 전부 RB (RB 밖 실패 0) · 네 환경의 실패 칸 목록이 같다 (md5 같음).  RB 묶음만 = 고치기 전 `50 PASS · 41 FAIL` · 고친 뒤 `91 PASS · 0 FAIL`.
- `python3 scripts/kg50_q5_branches.py --selftest` = `PASS (151/151)` · `python3 scripts/kg50_q5_verdict.py --selftest` = `PASS (98/98)` (`r2/after/`).
- `--compare-old <F02 전 판 77c24237>` (Python 3.11 · mawk) = `307 PASS · 0 FAIL` · 둘 다 정상인 장면 (시험 · G0–G3 통과 / -C 통과) 33 — 예전 묶음에서 다름 0 · 새 묶음에서 다름 0 ·
  옛 판 정상 · 새 판 거부 0 · 묶음별 같음 = 1 판과 같다 (P 12 / 13 · I 6 / 9 · 나머지 전부 같음 · `r2/after/compare_old_77c24237_py311.log`).
  다른 4 줄도 1 판과 같은 까닭: I 셋 = 승인 거부 글이 도구 자신의 sha256 을 찍음 · P 하나 = `p_rr2` (둘 다 거부) 의 원래 bash 오류 줄이 스크립트 경로 · 줄 번호 (1149 → 1401) 를 찍음 —
  옛 판 · 새 판으로 다시 돌려 그 한 줄만 다름을 확인 (`r2/after/compare_old_p_rr2_diff.log`).
- `--compare-old <1 판 5f4ffb46>` (1 판 ↔ 2 판 · Python 3.11 · mawk) = `307 PASS · 0 FAIL` · 둘 다 정상인 장면 33 — 예전 묶음에서 다름 0 · 새 묶음에서 다름 0 · 옛 판 정상 · 새 판 거부 0 ·
  묶음별 같음 = 위와 같은 꼴 (P 12 / 13 = `p_rr2` bash 오류 줄의 스크립트 경로 · 줄 번호 1352 → 1401 뿐 — `r2/after/compare_old_p_rr2_diff_5f4ffb46.log` · I 6 / 9 = 도구 자신의 sha256 ·
  `r2/after/compare_old_5f4ffb46_py311.log`) — 이 비교는 RB 묶음을 안 본다 (RB = 위 표).

기존 시험에서 바뀐 것 (2 판 · 221f57dbf):
- RB21 · RB24: 시험 전 거부 (`neg`) → **시작 거부** (`startrej` — 종료 코드 1 · sbatch 0 · 보고 · 작업 폴더 없음 · 멈춘 폴더 그대로) — PA-06 · 07 이 거부 자리를 cd 전으로 옮겼다.
- RBP d: 기대 러너 바이트 (`rb_expect`) = 새 틀 (`cd … || exit 1` · `ds` · `ks` · 신원 줄 · 대조 줄 · `command mpirun`) · 덱 · 체크포인트 sha256 인자 더함.
- RBP g: 신원 줄 = 정확히 하나 · 머리 + 꼬리 (덱 · 체크포인트 경로 · sha256) 대조 (lmp_mpi 칸은 기계마다 달라 뺌) · 대조 다름 줄 없음 — 예전 = 덱 조각만.
- RBR1 · RBR3: 시험 덱 · 체크포인트 고침을 시험 제출 때 → 시험 잡 끝난 뒤 (`FAKE_POST_TRIAL`) — 잡 시작 전 고침은 이제 잡 안 대조가 먼저 막는다 (RB41 · 42 가 그 자리를 본다).
- 하네스: 가짜 sbatch = 제출 때 러너 사본을 돈다 + 고리 · `invoke` = `{TMP}` · 넘겨받은 BASH_ENV · ENV · BASH_FUNC_* · 고리 변수 지움 · `sha(None)` · `pos()` 칸만 실패 · `rb()` = `prep` · 임시 폴더 목록 · 본 잡 로그.
- RB 밖 기존 칸: 판정 줄 그대로 — 고치기 전 도구로도 RB 밖 실패 0 (§0-3 표).

### 0-4. 리뷰어 장면 · 탐침 다시 돌림 (`r2/preattack/` — attack.py 는 리뷰어 판 그대로 (하네스 = 리뷰어 거울 작업 트리) · 도구만 바꿔 돌림)

| 장면 | 고치기 전 도구 5f4ffb46 (`attack_scenes_old_5f4ffb46.log`) | 고친 도구 (`attack_scenes_new.log`) |
|---|---|---|
| T_swap (-T) | 시험 잡이 바뀐 시험 덱을 읽고 G0 통과 | 시험 잡 mpirun 안 함 (`LMP_IDENTITY_MISMATCH`) · G0 실패 (잡 안 덱 신원 = 덱 sha256 다름) |
| swap_restore | 시험 잡이 바뀐 덱 · 본 제출 1 | 시험 잡 mpirun 안 함 · G0 실패 · 본 제출 0 |
| main_toctou | 본 잡이 바뀐 재개 덱을 읽음 | 본 제출은 함 (도구는 본 잡 출력을 안 본다) · 본 잡 mpirun 안 함 · 본 잡 로그에 `LMP_IDENTITY_MISMATCH` |
| bashenv | 시험 · 본 잡 다 other.liggghts | 검사한 덱 (038267335faa · b73b508611c2) |
| bashfunc | (dash 가 함수 변수를 못 넘김 — 정상) | 같음 |
| symlink_stopped | 잡이 원 런 폴더에서 돎 | 시험 전 거부 (단계 멈춘 폴더) · 원 폴더 그대로 · 작업 폴더가 링크 아님 |
| error_in_path | 본 제출 0 (ERROR 셈) | 시험 · 본 제출 · G0 통과 |
| np_sed | 루프에서 runnerck 거부 (꼬리 `;s/^/` 라 표지는 안 생김) | 시작 거부 (종료 코드 1) |
| positive | 시험 · 본 | 시험 · 본 · G0 신원 통과 |
| envl_exploit | 거부 (`셸 연결 · 치환 · 리디렉션 글자가 든 MPI 실행 줄`) | 거부 (`받는 꼴이 아닌 환경 줄`) |
| sfx_slash | 본 잡이 x.liggghts 를 돎 | 시작 거부 (종료 코드 1) |

- 탐침 (인자 11 에 맞춘 사본 `r2/preattack/rck_probe11.py` · `cdfail_probe11.py` — 리뷰어 원본 바이트에서 인자 · 덱 · 체크포인트 파일만 바꿈):
  헬퍼 러너 변형 30 중 받음 = 고치기 전 7 (`rck_probe_old_5f4ffb46.log` — 기본 · `conda activate ..` · `conda activate .` · 끝 줄 바꿈 없음 · `--qos=cpu-60,--exclusive` · `--partition=cpu:gpu` · 별칭 cd) →
  고친 뒤 4 (`rck_probe11_new.log` — 기본 · 끝 줄 바꿈 없음 · `--partition=cpu:gpu` · 별칭 cd).
  cd 실패 탐침: 고치기 전 `runner rc 0` + 가짜 mpirun 이 제출 폴더에서 돎 (`cdfail_probe_old_5f4ffb46.log`) → 고친 뒤 `runner rc 1` · mpirun 출력 없음 (`cdfail_probe11_new.log`).

### 0-5. 변이 (`r2/mutation/mutation_F02.txt` · 운전기 `r2/mutation/mutate_f02.py` · 변이마다 기록 `r2/mutation/logs/` · 고친 도구 사본에서 하나씩 끄고 `--only RB`)

- 묶음: **M** = 1 판 변이 41 (원문 조각만 2 판 글로 옮김 · 1 판 생존 넷 중 M16b · M25 · M36 = 새 칸 RB37 · RBU2 · RB36b 가 잡음 · M23 · M26 = 도구 흐름에서 시작 거부가 먼저라 RBU5 · RBU6 이 잡음) ·
  **N** = 2 판 수정 변이 22 (PA-01–09 · 환경 줄 · 쉼표 낱낱 · 임시 파일 · 체크포인트 인자) · **V** = 리뷰어 변이 28 (mutate_rev.py 의 E1–E3 · R1–R25 — 바꿀 글은 그대로 · 원문 조각만 2 판 글로:
  E2 = 새 conda 꼴 · R5 · R6 = `cd "…" || exit 1` · R16 = `k = '시험 덱' if trial …` · R21 = 새 신원 줄 머리).  환경 줄 (ENVL) 변이 = VE1–VE3 · N45 · N46 (1 판 변이 41 에는 없었다).
- 기록: 변이 91 개 RB 기록 91 (`r2/mutation/logs/` · 'No space left' 든 기록 0 · Traceback 든 기록 0 = PA-10 하네스가 죽지 않고 칸만 실패).
- ⚠ 이 판 첫 회 (기록 안 넣음) 에서 N50 · N51 이 **잘못 만든 변이**였다 — 바꿀 글 `"$ks%s"` 를 bash 가 `$ks<16진>` = 정의 안 된 변수 하나로 읽어 대조가 늘 실패 (대조를 끄지 못하고 잡을 다 멈춤) ·
  `"${ks}%s"` 로 고쳐 **91 개 전부 다시** 돌렸다 — 아래 표 = 다시 돈 판 (N50 = RB42 · N51 = RB40 · 41 · 43 이 잡음).
- "RBP1 · RBP2 만" 으로 잡힌 변이 (VR5 따옴표 없는 cd · M33 논리 경로 cd · M34 헬퍼 원본 기록 · VR9 논리 경로 영수증 줄) = 행동은 같고 **글 · 기록 꼴만** 다르다 — 틀 · 영수증 바이트를 못 박은 칸 (RBP d · e · f) 이 잡는다.

| 변이 | 결과 | RB PASS/FAIL | 실패한 시험 | 기대 (표지만) |
|---|---|---|---|---|
| M01_shebang | 잡힘 | 90/1 | RB22 | RB22 |
| M02_sbatch_after_cmd | 잡힘 | 90/1 | RB12 | RB12 |
| M03_sbatch_unknown_key | 잡힘 | 90/1 | RB10 | RB10 |
| M04_sbatch_dup_key | 잡힘 | 90/1 | RB11 | RB11 |
| M05a_jobname_value | 잡힘 | 90/1 | RB17 | RB17 |
| M05b_output_value | 잡힘 | 90/1 | RB18 | RB18 |
| M05c_n_value | 잡힘 | 89/2 | RB28 RB30 | RB28 RB30 |
| M06_token_value | 잡힘 | 89/2 | RB20 RB34 | RB20 RB34 |
| M07_env_after_cd | 잡힘 | 90/1 | RB13 | RB13 |
| M08_cd_count | 잡힘 | 89/2 | RB9 RB9b | RB9b |
| M09_cd_safe_path | 잡힘 | 90/1 | RB14 | RB14 |
| M10_cd_realpath | 잡힘 | 90/1 | RB3 | RB3 |
| M11_mpirun_count | 잡힘 | 90/1 | RB5 | RB5 |
| M12_mpirun_before_cd | 잡힘 | 90/1 | RB15 | RB15 |
| M13_comment_line | 잡힘 | 89/2 | RB4 RB4b | RB4b |
| M14_mpirun_any_in | 잡힘 | 89/2 | RB1 RB2 | RB1 RB2 |
| M15_other_command | 잡힘 | 90/1 | RB6 | RB6 |
| M16_mpirun_meta_msg | 잡힘 | 89/2 | RB7a RB7b | RB7a RB7b |
| M16b_meta_msg | 잡힘 | 90/1 | RB37 | RB37 (10-30 더함 · 1 판에서 살아남음) |
| M17_required_keys | 잡힘 | 89/2 | RB23 RB33 | RB23 RB33 |
| M18_cd_missing | 잡힘 | 89/2 | RB36 RB8 | RB8 |
| M19_mpirun_missing | 잡힘 | 90/1 | RB25 | RB25 |
| M20_cr | 잡힘 | 90/1 | RB16 | RB16 |
| M21_nul | 잡힘 | 90/1 | RB26 | RB26 |
| M22_utf8 | 잡힘 | 90/1 | RB27 | RB27 |
| M23_np_valid | 잡힘 | 90/1 | RBU5 | RBU5 (도구 흐름은 -n 시작 거부가 먼저) |
| M24_wr_safe | 잡힘 | 90/1 | RB19 | RB19 |
| M25_wr_consistent | 잡힘 | 90/1 | RBU2 | RBU2 (1 판에서 살아남음) |
| M26_deck_path_safe | 잡힘 | 90/1 | RBU6 | RBU6 (도구 흐름은 -x 시작 거부가 먼저) |
| M27_receipt_two | 잡힘 | 61/30 | RB40 RB41 RB42 RB43 RB44 RB44b RB45 RB46 RB47 RBP1 RBP2 RBR1 RBR2 RBR3 RBR4 RBR5 | RBR · RBP |
| M28_receipt_memory | 잡힘 | 89/2 | RBR4 RBR5 | RBR4 RBR5 |
| M29_recheck_off | 잡힘 | 88/3 | RBR1 RBR2 RBR3 | RBR1 RBR2 RBR3 |
| M30_gate_ng_off | 잡힘 | 45/46 | RB1 RB10 RB11 RB12 RB13 RB14 RB15 RB16 RB17 RB18 RB19 RB2 RB20 RB22 RB23 RB25 RB26 RB27 RB28 RB29 RB3 RB30 RB32a RB32b RB32c RB32d RB32e RB32f RB32g RB32h RB32i RB32j RB33 RB34 RB35 RB36 RB37 RB4 RB4b RB5 RB6 RB7a RB7b RB8 RB9 RB9b | 음성 전부 |
| M31_old_derivation | 잡힘 | 18/73 | RB1 RB10 RB11 RB12 RB13 RB14 RB15 RB16 RB17 RB18 RB19 RB2 RB20 RB22 RB23 RB25 RB26 RB27 RB28 RB29 RB3 RB30 RB32a RB32b RB32c RB32d RB32e RB32f RB32g RB32h RB32i RB32j RB33 RB34 RB35 RB36 RB36b RB37 RB4 RB40 RB41 RB42 RB43 RB44 RB44b RB45 RB46 RB47 RB4b RB5 RB6 RB7a RB7b RB8 RB9 RB9b RBP1 RBP2 RBR1 RBR2 RBR3 | 음성 전부 · RBP |
| M32_in_relative | 잡힘 | 84/7 | RB45 RBP1 RBP2 | RBP b c d |
| M33_cd_logical_w | 잡힘 | 90/1 | RBP1 | RBP1 (별칭 장면) |
| M34_helper_orig_off | 잡힘 | 89/2 | RBP1 RBP2 | RBP f |
| M35_identity_off | 잡힘 | 69/22 | RB40 RB41 RB43 RB44 RB44b RB45 RB47 RBP1 RBP2 RBR1 RBR2 RBR3 | RBP · G0 신원 관문 |
| M36_rm_stale_trial | 잡힘 | 90/1 | RB36b | RB36b (1 판에서 살아남음) |
| M39_loose_rewrite | 잡힘 | 86/5 | RB28 RB29 RB30 RB32a RB32g | RB28 RB29 RB30 |
| M38_receipt_write_check | 살아남음 | 91/0 | - | 없음 (겹 방어 · runnerck 가 다섯 중 덱 셋을 이미 읽고 러너 둘을 썼다) |
| N40_np_startup | 잡힘 | 88/3 | RB21 RB49 RB49b | RB21 RB49 RB49b |
| N41_np_startup_loose | 잡힘 | 88/3 | RB21 RB49 RB49b | RB21 RB49 RB49b |
| N42_sfx_startup | 잡힘 | 89/2 | RB24 RB50 | RB24 RB50 |
| N43_sfx_startup_loose | 잡힘 | 89/2 | RB24 RB50 | RB24 RB50 |
| N44_symlink_off | 잡힘 | 90/1 | RB48 | RB48 |
| N45_envlike_off | 잡힘 | 81/10 | RB32a RB32b RB32c RB32d RB32e RB32f RB32g RB32h RB32i RB32j | RB32 |
| N46_conda_dot | 잡힘 | 88/3 | RB32h RB32i RB32j | RB32h RB32i RB32j |
| N47_tok_comma | 잡힘 | 90/1 | RB34 | RB34 |
| N48_ckp_safe_off | 잡힘 | 90/1 | RBU4 | RBU4 |
| N49_render_no_refuse | 잡힘 | 85/6 | RB40 RB41 RB42 RB43 RBP1 RBP2 | RB40 RB41 RB42 RB43 · RBP d |
| N50_render_no_ks | 잡힘 | 88/3 | RB42 RBP1 RBP2 | RB42 · RBP d |
| N51_render_no_ds | 잡힘 | 86/5 | RB40 RB41 RB43 RBP1 RBP2 | RB40 RB41 RB43 · RBP d |
| N52_render_cd_guard | 잡힘 | 88/3 | RB46 RBP1 RBP2 | RB46 · RBP d |
| N53_render_command | 잡힘 | 88/3 | RB45 RBP1 RBP2 | RB45 · RBP d |
| N54_g0_no_identity | 잡힘 | 89/2 | RB44 RB44b | RB44 RB44b |
| N55_gi_path | 잡힘 | 90/1 | RB44b | RB44b |
| N56_gi_sha | 잡힘 | 89/2 | RB40 RB41 | RB40 RB41 |
| N57_gi_count | 잡힘 | 90/1 | RB44 | RB44 |
| N58_error_count_old | 잡힘 | 90/1 | RB47 | RB47 |
| N59_tqs_check | 살아남음 | 91/0 | - | 없음 (겹 방어 · GNU sha256sum 셋째 줄 = 시험 덱 · 안전한 경로) |
| N60_tmp_cleanup_off | 잡힘 | 90/1 | RB35 | RB35 |
| N61_isfile_off | 살아남음 | 91/0 | - | 없음 (없는 파일 · 폴더는 열 때 같은 OSError · FIFO 만 다름 = 막힘 — 시험 안 함) |
| VE1_ENVL_export_any | 잡힘 | 88/3 | RB32b RB32c RB32d | RB32b RB32c RB32d |
| VE2_ENVL_conda_any | 잡힘 | 87/4 | RB32g RB32h RB32i RB32j | RB32g RB32h RB32i RB32j |
| VE3_ENVL_source_any | 잡힘 | 90/1 | RB32e | RB32e |
| VR1_cd_realpath_dropped | 잡힘 | 90/1 | RB3 | RB3 |
| VR2_mpirun_prefix | 잡힘 | 87/4 | RB1 RB2 RB7a RB7b | RB1 RB2 |
| VR3_realpath_W_dropped | 잡힘 | 90/1 | RBU2 | RBU2 |
| VR4_render_in_basename | 잡힘 | 84/7 | RB45 RBP1 RBP2 | RBP |
| VR5_render_cd_unquoted | 잡힘 | 89/2 | RBP1 RBP2 | RBP d |
| VR6_render_no_cd | 잡힘 | 84/7 | RB46 RBP1 RBP2 | RBP |
| VR7_runnerck_rc2_pass | 잡힘 | 90/1 | RB35 | RB35 |
| VR8_no_rm_TR | 잡힘 | 90/1 | RB36b | RB36b |
| VR9_receipt_logical_D | 잡힘 | 90/1 | RBP1 | RBP e |
| VR10_receipt_count_dropped | 살아남음 | 91/0 | - | 없음 (GNU sha256sum = 성공이면 파일마다 한 줄) |
| VR11_sed_n_permissive | 잡힘 | 89/2 | RB28 RB30 | RB28 |
| VR12_CR_NUL_precheck | 잡힘 | 89/2 | RB16 RB26 | RB26 |
| VR13_env_after_cd | 잡힘 | 90/1 | RB13 | RB13 |
| VR14_premain_receipt_sha | 잡힘 | 89/2 | RBR4 RBR5 | RBR4 RBR5 |
| VR15_premain_recheck | 잡힘 | 88/3 | RBR1 RBR2 RBR3 | RBR1 RBR2 RBR3 |
| VR16_trial_uses_main_deck | 잡힘 | 67/24 | RB40 RB41 RB43 RB44 RB44b RB45 RB47 RBP1 RBP2 RBR1 RBR2 RBR3 | RBP |
| VR17_output_optional | 잡힘 | 90/1 | RB33 | RB33 |
| VR18_jobname_want_dropped | 잡힘 | 90/1 | RB17 | RB17 |
| VR19_comment_skipped | 잡힘 | 89/2 | RB4 RB4b | RB4 RB4b |
| VR20_receipt_no_ckpt | 잡힘 | 61/30 | RB40 RB41 RB42 RB43 RB44 RB44b RB45 RB46 RB47 RBP1 RBP2 RBR1 RBR2 RBR3 RBR4 RBR5 | RBP · RBR |
| VR21_render_identity_dropped | 잡힘 | 69/22 | RB40 RB41 RB43 RB44 RB44b RB45 RB47 RBP1 RBP2 RBR1 RBR2 RBR3 | RBP · G0 신원 관문 |
| VR22_sbatch_after_cmd | 잡힘 | 90/1 | RB12 | RB12 |
| VR23_two_cd | 잡힘 | 89/2 | RB9 RB9b | RB9 RB9b |
| VR24_cd_safe_abs_dropped | 잡힘 | 90/1 | RB14 | RB14 |
| VR25_WR_logical_pwd | 잡힘 | 81/10 | RB47 RBP1 | RBP1 |

- 묶음 M: 변이 41 · 잡힘 40 · 살아남음 1 · 못 만듦 0
- 묶음 N: 변이 22 · 잡힘 20 · 살아남음 2 · 못 만듦 0
- 묶음 V: 변이 28 · 잡힘 27 · 살아남음 1 · 못 만듦 0
- 합계: 변이 91 · 잡힘 87 · 살아남음 4 · 못 만듦 0 · 시험 하네스 예외 (Traceback) 든 로그 0

살아남은 4 (전부 겹 방어 · 같은 동작 — 시험을 더 넣지 않은 까닭):
- M38_receipt_write_check · VR10_receipt_count_dropped: 영수증 쓰기 실패 · 줄 수 ≠ 5 가지 — runnerck 가 다섯 중 덱 셋을 이미 읽고 러너 둘을 썼고 GNU sha256sum 은 성공이면 파일마다 한 줄이라 도구 흐름에서 닿지 않는다 (그 사이 파일이 사라지는 경합뿐).
- N59_tqs_check: 영수증 셋째 줄 = `<64 16진>  <시험 덱 절대 경로>` 꼴 검사 — 안전한 경로 · GNU sha256sum 이면 늘 그 꼴.
- N61_isfile_off: 없는 파일 · 폴더는 열 때도 같은 OSError (거부) · 다른 것은 FIFO · 장치 파일뿐 (열면 막힌다) — 막히는 시험은 넣지 않았다.

### 0-6. D2 예 — 2 판 도구가 쓰는 러너 (`r2/d2_example/d2_example.sh` · 기록 `r2/d2_example/d2_example.log`)

고친 도구 (e5a61181) 의 runnerck 함수를 글 그대로 떼어 모래 상자에서 (ibb 꼴 = `/home/yonghoon` → `/lustre/home/yonghoon` 링크 · 모래 상자 앞머리를 지운 글) ·
헬퍼 러너 = 받은 D2 러너 (`docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/run_kg50_d2_b50_r4.sh`) · 덱 = 같은 폴더 사본 (sha256 eacc23e6… · aac7debc…) ·
⚠ 체크포인트 = 리포에 없어 0 바이트 64 개 **대역** (sha256 f5a5fd42… — ibb 에서는 그 자리 실제 체크포인트 값이 박힌다).  `runnerck rc=0` · 대조 통과 문구 = 기록 그대로.

본 `run_kg50_d2_b50_r4.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=kg50_d2_b50_r4
#SBATCH --output=logs/output_kg50_d2_b50_r4_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 4
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd "/lustre/home/yonghoon/dem_test/kg50_d2_b50" || exit 1
ds=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts sha256=$ds checkpoint=/lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin sha256=$ks"
[ "$ds" = "eacc23e60ae5981496091d3bab02084f8aae4ea180752b2b687750935316c3c6" ] && [ "$ks" = "f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts sha256 $ds (checked eacc23e60ae5981496091d3bab02084f8aae4ea180752b2b687750935316c3c6) checkpoint /lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin sha256 $ks (checked f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 4 lmp_mpi -in "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts"
```

시험 `run_kg50_d2_b50_r4t.sh` (본과 다른 곳 = 잡 이름 끝 t · `--output` · `--time=01:00:00` · 시험 덱 경로 · 그 sha256):

```bash
#!/bin/bash
#SBATCH --job-name=kg50_d2_b50_r4t
#SBATCH --output=logs/output_kg50_d2_b50_r4t_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 4
#SBATCH --time=01:00:00

source ~/.bashrc
conda activate myenv
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd "/lustre/home/yonghoon/dem_test/kg50_d2_b50" || exit 1
ds=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts sha256=$ds checkpoint=/lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin sha256=$ks"
[ "$ds" = "aac7debc81029acfa4f7619aab8a2358741095b4f5e833cedac0a8f9f29c044b" ] && [ "$ks" = "f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts sha256 $ds (checked aac7debc81029acfa4f7619aab8a2358741095b4f5e833cedac0a8f9f29c044b) checkpoint /lustre/home/yonghoon/dem_test/kg50_d2_b50/restart_kg50_d2_b50/restart_settling_20001.bin sha256 $ks (checked f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 4 lmp_mpi -in "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts"
```

### 0-7. 못 닫은 것 · 한계 (2 판)

- **ibb 실제 경로 같음 = 확인됨 (1저자 ibb 화면 10-30)**: `readlink -f ~` → `/lustre/home/yonghoon` · `cd ~/dem_test && pwd -P` → `/lustre/home/yonghoon/dem_test`
  (메인 세션 전달) — 헬퍼 러너의 `cd /lustre/home/yonghoon/dem_test/<케이스>` 실제 경로 = 도구 작업 폴더 (`-r ~/dem_test`) 실제 경로 (1 판 §8 첫 줄의 "추정" 을 갈음).
- **본 잡**: 잡 안 대조는 본 잡 시작 때 바뀐 덱 · 체크포인트를 막지만, 그 결과 (`LMP_IDENTITY_MISMATCH` 로 멈춘 본 잡) 를 도구는 모른다 — 본 sbatch 뒤 끝 (본 잡 로그를 사람이 본다).
  대조 ↔ LIGGGHTS 가 파일을 여는 사이 (초 단위) 는 남는다 · 덱이 잡 중에 읽는 다른 파일 (판 메시 `file plate_*.stl` 등) 은 영수증 · 잡 안 대조 밖 (1 판 그대로).
- **신원 줄 관문 · 잡 안 대조의 새 실패 꼴 (둘 다 안전한 쪽 · 제출 없음 · 잡 로그에 보임)**: 잡 환경에 `sha256sum` · `cut` 이 없으면 잡이 mpirun 전에 멈춘다 ·
  환경 줄이 줄 끝 없이 글을 남기면 시험 로그의 신원 줄이 줄 머리에 안 와 G0 실패 ("LMP_IDENTITY 줄 0 개") — ibb -T 한 번으로 볼 일.
- **-T**: 영수증 다시 대조 없음 (본 제출이 없다) — 시험 덱 · 체크포인트는 잡 안 대조 + G0 신원 관문이 덮고, 시험 러너 파일이 sbatch 뒤 바뀐 것은 안 본다.
- **멈춘 폴더 안의 링크** (절대 경로 링크 본 덱 · 링크 restart 폴더) 는 링크 그대로 복사된다 (F02 전부터 · 이번에 안 바꿈) — 멈춘 폴더 **자체** 의 링크만 막았다.
- **믿는 입력**: ~/.bashrc · 제출 환경 (BASH_ENV · PATH · 내보낸 함수) — `command mpirun` 은 셸 함수 mpirun 만 건너뛴다.  내보낸 함수 (`BASH_FUNC_mpirun%%`) 장면은 가짜 sbatch (dash) 가
  넘기지 못해 이 하네스에서 못 본다 (BASH_ENV 장면 RB45 = 같은 함수 찾기).
- **RB35 꼴** (시험 러너 자리가 폴더라 runnerck 쓰기 실패): 본 러너 `run_<C>_<SFX>.sh` 는 먼저 도구 틀로 바뀐 채 남는다 (제출 없음 · 러너 관문 거부 · 1 판과 같음 · 임시 파일은 이제 지움).
- **D2 예의 체크포인트** = 대역 (0 바이트 64 개) — 러너 글에 박힌 체크포인트 sha256 은 그 대역 값.
- **가짜 하네스**: 실제 SLURM 이 아니다 — 가짜 sbatch 는 제출 때 러너를 사본으로 떠서 그 자리에서 (동기) `bash <사본>` 으로 돌리고, 고리 (FAKE_PRE_SPOOL · _PRE_TRIAL · _POST_TRIAL · _PRE_MAIN) 로
  사람의 손질 · 큐 대기 중 변경을 흉내 낸다 · 가짜 mpirun 은 `-in` 만 읽는다 (LIGGGHTS 안 돎) · 리뷰어 attack.py 는 리뷰어 거울 작업 트리의 하네스를 읽는다 (도구만 바꿔 돌림).
- **변이 생존 4** (§0-5): M38 · VR10 (영수증 쓰기 · 줄 수 가지 = 닿지 않음) · N59 (영수증 셋째 줄 꼴 = 늘 같음) · N61 (보통 파일 검사 = FIFO 만 다름 · 시험 안 함) — 다 겹 방어.
- 실제 ibb SLURM · LIGGGHTS 실행 · `scripts/check_all.sh` 는 돌리지 않았다 (지시대로 · 메인 세션 몫) · 원장 (`docs/reviews/findings.json`) · 절차 문서 · CLAUDE.md 는 고치지 않았다 (메인 세션 몫).

## 1. 고친 것 (`scripts/resume_ckpt.sh` · 설계 = 1저자 10-30 Q2 비준 그대로)

| 자리 | 예전 (77c24237) | 이제 |
|---|---|---|
| -n · -np 고침 (sed · 헬퍼 러너) | `#SBATCH -n ` 로 시작하는 줄 **전체** · 줄 **어디든** `mpirun … -np [숫자 0 개 이상]` 을 고쳤다 → 엄격 대조 전에 어긋남이 지워진다 (`#SBATCH -n 1 --nodes=2` → `-n 56` · `-np` 숫자 없음 → 정상 꼴) | 정해진 꼴만: 줄 전체 `#SBATCH -n <숫자>` · 줄 첫머리 `mpirun [--oversubscribe ][--bind-to none ]-np <숫자> lmp_mpi -in ` — 그 밖은 고치지 않고 아래 대조가 거부.  **엄격 대조는 이 고침 뒤** (선택 · 설계의 "-n = NP" · "-np NP" 를 그대로 대조하려고 — 헬퍼가 쓰는 `-n` · `-np` 값은 도구의 NP 와 다를 수 있다: 시험 가짜 헬퍼 = 1 · 실제 헬퍼의 원래 값은 리포 기록에 없다 (D2 러너 사본은 옛 도구가 고친 뒤 글)) · 헬퍼 원본 바이트 (고침 전) = 시도 폴더 `helper_run_<C>_<SFX>.sh.orig` |
| 러너 관문 | grep 셋 — `^#SBATCH -n NP$` 한 줄 있음 · 본 러너 어딘가에 `--oversubscribe --bind-to none -np NP lmp_mpi` · 시험 러너 어딘가에 `-np NP lmp_mpi -in input_<C>_<SFX>t.liggghts` (부분 글자) | 새 함수 runnerck (`python3 -I` · 이 구간 밖 Python 은 안 건드림) 가 헬퍼 러너를 **줄마다** 대조 — 받는 꼴: 첫 줄 `#!/bin/bash` · `#SBATCH --job-name=<C>_<SFX>` · `--output=logs/output_<C>_<SFX>_%j.out` · `-n NP` · `--time=<낱말>` (각 한 번 · 꼭) · `--qos=` · `--partition=` (한 번까지 · 낱말 A-Z a-z 0-9 _ . : , + -) · #SBATCH 는 첫 명령 줄 앞 · 빈 줄 · 환경 줄 (`source ~/.bashrc` · `conda activate <이름>` · `export (OMP\|MKL\|OPENBLAS\|NUMEXPR)_NUM_THREADS=1` · cd 앞) · `cd <절대 경로>` 한 번 (실제 경로 = 작업 폴더 실제 경로 · `.` `..` 마디 · 따옴표 · `$` · 공백 없음) · 그 다음 `mpirun --oversubscribe --bind-to none -np NP lmp_mpi -in <$D 의 이름>` 한 번.  그 밖 (주석 줄 · 다른 명령 · `;` `&&` `\|\|` `\|` 리디렉션 `$(` 백틱 · 둘째 MPI 실행 · 두 cd · CR · NUL · UTF-8 아님) = 거부 → `ng` (단계 "정적 대조 · 시험 덱 · 러너" · 이유 "헬퍼 러너 엄격 대조 실패 (10-30 KG50R-F02 …) — 문제 N: 줄 k [원문] — 이유 \| …") · sbatch 전 · 대조 기록 = 시도 폴더 `runner_check.txt` |
| 시험 러너 | 헬퍼 러너의 sed 사본 (`s/<C>_<SFX>/<C>_<SFX>t/g` · `--time=01:00:00`) — `.bak` · 다른 cd · 둘째 실행 줄이 그대로 따라왔다 | 대조 통과 = 본 `run_<C>_<SFX>.sh` · 시험 `run_<C>_<SFX>t.sh` 를 도구가 **한 틀**로 씀: 대조한 #SBATCH 값 (시험 = 이름 끝 t · `--time=01:00:00`) · 환경 줄 (순서 그대로) · `cd "<작업 폴더 실제 경로>"` (`cd -P` + `pwd -P`) · 잡 안 신원 기록 줄 하나 (`LMP_IDENTITY` — 잡 안 PATH 의 lmp_mpi 경로 · sha256 · 잡 시작 때 덱 sha256 · **기록만 · 관문 아님**) *[2 판: 신원 줄 = 시험 로그 G0 관문 (덱) + 체크포인트 칸 · 잡 시작 때 덱 · 체크포인트 sha256 대조 · `cd … \|\| exit 1` · `command mpirun` — §0-1 · 틀 = §0-6]* · `mpirun --oversubscribe --bind-to none -np NP lmp_mpi -in "<검사한 덱 절대 경로>"` 한 줄 (본 = $D · 시험 = $TD).  작업 폴더 실제 경로 · 덱 · 러너 이름에 A-Z a-z 0-9 _ . + - / 밖 글자 = 거부 (러너의 `"…"` 안에서 `$` 백틱 `\` 가 펼쳐진다) · NP = 1 이상 정수 |
| 실행 영수증 `main_inputs.sha256` | 재개 덱 · 러너 둘 (작업 폴더 경로) · 체크포인트 sha256 은 tool.txt 기록만 | 러너가 실제로 읽는 자리 (작업 폴더 실제 경로 · 러너의 cd · -in 과 같은 절대 경로) 의 **다섯**: 재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트 · 다섯 다 못 쓰면 시험 안 냄 · 그 파일 sha256 = 이 호출 메모리 (`SUBMITTED` 셋째 칸) |
| 본 제출 바로 전 | `sha256sum -c` (재개 덱 · 러너) | ① 영수증 파일 sha256 = 메모리 값 (`sha256sum -c` 는 줄이 빠지거나 덧붙은 영수증도 통과 — 실측) ② `sha256sum -c --quiet` 다섯 — 하나라도 다르면 본 제출 안 함 · 보고에 다른 파일 이름 (`…: FAILED`) |
| 보고 · tool.txt | — | 러너 대조 줄 · 시험 잡 안 신원 줄 (`LMP_IDENTITY` 를 옮기기만 · *[2 판: G0 잡 안 덱 신원 관문 줄 + 신원 줄 + 잡 안 대조 다름 줄 · §0-1]*) · 본 제출 직전 확인 줄에 다섯 · tool.txt 에 영수증 sha256 · "위 lmp_mpi 줄 = 제출 셸 PATH" 표지 · 거부 단계 이름 "정적 대조 · 시험 덱 · 러너" |

손대지 않은 것: 정적 대조 Python (`deckcheck` — setup_check · setup_order · state_cmp) · G0–G3 · 큐 · 승인 · 시도 폴더 규칙 · `-C` · `-c`.

## 2. 시험 (`scripts/test_resume_ckpt.py` · RB 묶음 52 칸)

하네스 (설계 (4)):
- 가짜 sbatch 가 **제출된 러너를 실제로 돈다** (예전 = 제공 로그를 `logs/` 로 복사만) — SLURM 처럼 제출 폴더에서 `bash <러너>` · stdout+stderr = 러너의 `#SBATCH --output` (`%j` = job · 없으면 `slurm-%j.out`) · `SLURM_JOB_ID` · `FAKE_JOB_KIND` 넘김 · 제출 실패 꼴 (`FAKE_SBATCH_MAIN_TEXT` · `_TRIAL_TEXT` · `_TRIAL_EMPTY`) = 잡이 없으니 안 돎 · 시험 로그 고정물 없음 (`FAKE_TRIAL_LOG` 빈 값) 인 시험 = 출력 파일을 안 만든 잡 (예전 S6 장면 그대로).
- 가짜 mpirun (stub 폴더 = PATH 맨 앞) — 실제 cwd (`pwd -P`) · 인자 하나하나 · `-in` 파일 sha256 (그 cwd 기준 · 없으면 MISSING) 을 기록 · 시험 = 시험 로그 고정물을 stdout 으로 (= 도구가 읽는 `logs/output_<C>_<SFX>t_<job>.out`).
- 가짜 dem_restart.py 러너 = 실제 헬퍼 꼴 (`--output` · `cd <작업 폴더 실제 경로>`) · `FAKE_RUNNER` = 러너 바이트 고정물 (`{W}` `{CS}` `{C}` `{ROOT}` 자리표) · 루트 별칭 링크 (ibb `-r /home/yonghoon/dem_test` · 헬퍼 `cd /lustre/home/…` 꼴) · `--only RB`.

음성 33 칸 = 받는 꼴 밖 헬퍼 러너 → **sbatch 0 회 · mpirun 0 회** · stdout 과 보고에 KG50R-F02 이유와 그 조각 · 보고 시험 전 거부 절 (단계 "정적 대조 · 시험 덱 · 러너"):

| 칸 | 헬퍼 러너 꼴 | 이유 조각 |
|---|---|---|
| RB1 | Codex `.bak` — 본 러너 `-in …r56.liggghts.bak` · 작업 폴더에 본 `.bak` 덱 (첫 긴 run 뒤 `velocity all set 1.0 0.0 0.0`) · 시험 `.bak` 덱 (= 검사한 시험 덱 바이트) | `MPI 실행 줄 -in [….bak] ≠ 검사한 재개 덱 […]` |
| RB2 | `.bak` 가 시험 쪽에만 닿음 — 시험 `.bak` 덱만 (검사한 시험 덱과 다름 · 본 `.bak` 없음) | 같음 |
| RB3 · RB8 · RB9 · RB9b · RB14 · RB15 | cd = 멈춘 폴더 · cd 없음 · cd 두 번 (둘째 = 루트) · cd 두 번 (둘 다 작업 폴더) · cd 경로에 `..` (실제 경로는 같음) · MPI 실행 줄이 cd 앞 | `cd 실제 경로 [` · `cd 줄 없음` · `cd 가 두 번` · `cd 경로가 안전한 절대 경로가 아님` · `MPI 실행 줄이 cd 앞` |
| RB4 · RB4b | 주석 속 정상 mpirun 줄 + 다른 실제 줄 (처음부터 덱 `input_<C>.liggghts`) · 주석 줄 하나만 | `주석 줄` |
| RB5 · RB25 · RB29 | MPI 실행 줄 두 번 (같은 줄) · 없음 · `-np` 숫자 없음 | `MPI 실행 줄이 두 번` · `MPI 실행 줄 없음` · `MPI 실행 줄이 정해진 꼴이 아님` |
| RB6 · RB7a · RB7b | 다른 명령 (`cp` 처음부터 덱 → 재개 덱) · MPI 실행 줄 `;` 이음 · `&&` 이음 | `허용 목록에 없는 명령 줄` · `셸 연결 · 치환 · 리디렉션 글자가 든 MPI 실행 줄` |
| RB10 · RB28 · RB30 | `-n` 어긋남 (`#SBATCH -n 1` 뒤 `--ntasks=8` · SLURM 은 뒤 지시로 8 작업) · `#SBATCH -n 1 --nodes=2` · `#SBATCH -n x` | `작업 수 · 노드 지시` · `#SBATCH -n 값` |
| RB11 · RB12 · RB17 · RB18 · RB20 · RB22 · RB23 | `--time` 두 번 · #SBATCH 가 명령 뒤 · `--job-name` 다름 · `--output` 다름 · `--qos` 값에 공백 · `#!/bin/sh` · `--time` 없음 | `#SBATCH --time= 가 두 번` · `#SBATCH 줄이 명령 줄 뒤` · `#SBATCH --job-name= 값` · `#SBATCH --output= 값` · `안전한 낱말이 아님` · `첫 줄이 #!/bin/bash 가 아님` · `#SBATCH --time= 줄 없음` |
| RB13 · RB16 · RB26 · RB27 | 환경 줄이 cd 뒤 · CRLF · NUL · UTF-8 아닌 바이트 | `환경 줄이 cd 뒤` · `CR 글자` · `NUL 글자` · `UTF-8 이 아님` |
| RB19 · RB21 · RB24 | 작업 폴더 실제 경로에 `$` (루트 = 그 폴더를 가리키는 링크 · 헬퍼 cd = 링크 경로) · NP 0 (`-n 0`) · 접미사에 `$` (`-x r5$x`) | `작업 폴더 실제 경로 [` · `NP [0]` · `재개 덱 절대 경로 [` |

양성 2 × 7 칸 (a 시험 1 · 본 1 · 기록 둘 · b 시험 잡 cwd · 인자 · 읽은 바이트 = 검사한 시험 덱 · c 본 잡 같은 셋 = 검사한 재개 덱 · d 본 · 시험 러너 = 시험 쪽에서 따로 쓴 기대 바이트 · e 영수증 다섯 = 절대 경로 · 실제 sha256 · f 시도 폴더 헬퍼 원본 · 보고 줄 · g 시험 로그 LMP_IDENTITY 의 덱 sha256 = 검사한 시험 덱):
- RBP1 = 실제 D2 헬퍼 러너 (`docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/run_kg50_d2_b50_r4.sh` · 이름만 이 시험 케이스로 · `-n 4` · `-np 4` 그대로 → 도구가 56 으로) · `-r` = 루트 별칭 링크 · 헬퍼 cd = 실제 경로 (ibb 꼴).
- RBP2 = 기본 헬퍼 꼴 · 반대 별칭 (`-r` 실제 루트 · 헬퍼 cd = 별칭 경로).

영수증 5 칸 = 시험 1 · 본 제출 0 · 보고에 그 사유: RBR1–3 시험 제출 뒤 시험 덱 · 시험 러너 · 체크포인트가 바뀜 (`…: FAILED`) · RBR4 영수증 끝에 줄 하나 · RBR5 영수증 마지막 줄 (체크포인트) 지움 (둘 다 `sha256sum -c` 는 통과하는 꼴 → `실행 입력 영수증`).

## 3. 결과 (기록 = `before/` · `after/` · 'No space left' 줄 0)

| 환경 | 고치기 전 (도구 77c24237 · 시험 = 이 시험) | 고친 뒤 (도구 5f4ffb46) |
|---|---|---|
| Python 3.11.15 · awk = mawk 1.3.4.20240123 (시스템) | `218 PASS · 50 FAIL` | `268 PASS · 0 FAIL` |
| Python 3.11.15 · awk = GNU Awk 5.2.1 (스크래치 .deb 를 `awk` 이름으로 PATH 앞) | `218 PASS · 50 FAIL` | `268 PASS · 0 FAIL` |
| Python 3.8.20 (시험 하네스) · mawk | `218 PASS · 50 FAIL` | `268 PASS · 0 FAIL` |
| Python 3.8.20 (하네스 **와 도구 안 python3** — PATH 앞에 python3 → 3.8.20 링크 · 덧붙인 환경) · mawk | `218 PASS · 50 FAIL` | `268 PASS · 0 FAIL` |

- 네 환경 모두: 기존 216 칸 고치기 전 · 뒤 다 통과 · 고치기 전 실패 50 = 전부 RB (RB 52 중 통과 2 = RBP1a · RBP2a — 옛 도구도 정상 러너는 시험 1 · 본 1 을 냈다).
- ⚠ 요청된 "Python 3.8" 명령 (`python3.8 -I scripts/test_resume_ckpt.py`) 은 **하네스만** 3.8 이다 — 도구가 부르는 `python3` (runnerck · deckcheck) 는 PATH 의 3.11.  그래서 넷째 줄을 덧붙였다 (도구 안 Python 도 3.8.20).
- `python3 scripts/kg50_q5_branches.py --selftest` = `PASS (151/151)` · `python3 scripts/kg50_q5_verdict.py --selftest` = `PASS (98/98)` (고친 도구 · `after/`).
- `--compare-old <고치기 전 판>` (Python 3.11 · mawk) = `268 PASS · 0 FAIL` · 둘 다 정상인 장면 (시험 · G0–G3 통과 / -C 통과) 33 — 예전 묶음에서 다름 0 · 새 묶음에서 다름 0 (보고만: 없음) · 옛 판 정상 · 새 판 거부 0: 없음 · 묶음별 같음: K: 같음 6 / 6 · S: 같음 7 / 7 · D: 같음 9 / 9 · Q: 같음 4 / 4 · T: 같음 1 / 1 · C: 같음 4 / 4 · N: 같음 7 / 7 · F: 같음 11 / 11 · A: 같음 4 / 4 · P: 같음 12 / 13 · W: 같음 13 / 13 · R: 같음 3 / 3 · G: 같음 54 / 54 · X: 같음 6 / 6 · L: 같음 5 / 5 · I: 같음 6 / 9 · Q9: 같음 4 / 4 · Y: 같음 27 / 27 (`after/compare_old_311.log` · 장면마다 옛 판도 같은 입력으로 돌려 stdout · 보고 · 작업 폴더를 대조 — KG50R 표지 줄 · 시도 폴더 · cut_* · **run_*.sh** (이번에 도구 틀로 바뀐 러너) 는 빼고).
  다른 4 줄은 둘 다 정상인 장면이 아니다: I 셋 = 승인 인자 없음 · 틀림 (I1) 의 거부 글이 **도구 자신의 sha256** 을 찍는다 (판마다 다른 게 당연) · P 하나 = `p_rr2` (둘 다 거부) 에서 원래부터 나던 bash 오류 줄 (`[ -s $W/$RR ]` · RR 두 줄) 이 스크립트 경로 · 줄 번호 (1149 → 1352) 를 찍는다 — 옛 판 · 새 판으로 다시 돌려 그 한 줄만 다름을 확인했다.

## 4. 고치기 전 판이 옳은 이유로 실패했나 (`before/before_py311_mawk.log` 의 실패 줄 끝 = 실제로 낸 sbatch · 돈 잡)

| 무엇 | 고치기 전 도구 |
|---|---|
| RB1 (Codex 반례) | 시험 · 본 제출 — 시험 잡이 `-in …r56t.liggghts.bak` = 검사한 시험 덱과 같은 바이트 (sha256 앞 038267335faa) 를 읽고, 본 잡이 `-in …r56.liggghts.bak` = 검사 안 한 덱 (fc7cd46b6de0 ≠ 검사한 재개 덱 b73b508611c2) 을 읽었다 — Codex 가 셸 조건 전사로 보인 경로를 가짜 SLURM 실행으로 관측 |
| RB2 | 시험 · 본 제출 — 시험 잡이 검사 안 한 시험 `.bak` (bb578f2de764 ≠ 검사한 시험 덱 038267335faa) 를 읽음 · 본 잡 `-in` 없음 (MISSING) |
| RB3 · RB8 · RB9 · RB15 | 시험 · 본 제출 — 잡 cwd = 멈춘 폴더 (RB3) · 제출 폴더 (RB8 cd 없음 · RB9 둘째 cd · RB15 cd 전 실행) · `-in` 없음 (MISSING) |
| RB16 · RB18 | 시험만 제출 — RB16 = CR 붙은 cd 가 실패해 제출 폴더에서 · 로그 이름에 CR · RB18 = 로그가 out.log 로 → 둘 다 G0 실패로 본 제출 없음 (러너 꼴을 본 것은 아님) |
| RB4 · RB6 · RB7a · RB7b · RB5 | 시험 · 본 제출 — RB4 잡 둘 다 처음부터 덱 `input_<C>.liggghts` (39b4990ad619) 를 읽음 · RB6 잡 시작 때 `cp` 가 검사한 덱을 그 덱으로 덮음 · RB7a 둘째 실행 = 처음부터 덱 · RB7b 본 잡 뒤 `&& cp` 가 덮음 · RB5 같은 줄 두 번 실행 |
| RB24 | 시험 · 본 제출 — 옛 러너의 `-in input_…r5$x.liggghts` 를 bash 가 펼쳐 `…r5.liggghts` (MISSING) — 따옴표 없는 러너 글이 잡이 읽는 이름을 바꿨다 |
| RB21 | 시험 · 본 제출 — `#SBATCH -n 0` · `-np 0` |
| RB4b · RB9b · RB10–14 · RB17 · RB19 · RB20 · RB22 · RB23 · RB26–30 | 시험 · 본 제출 (잡은 검사한 덱을 읽었지만 러너 꼴 어긋남을 안 봄 — RB10 = SLURM 8 작업 · RB17 = 큐 검사 이름 밖 · RB28 · RB30 = 옛 sed 가 -n 줄을 덮어 지움 · RB29 = 옛 sed 가 정상 꼴로 바꿈) |
| RB25 | 옛 grep 관문도 거부 ("러너 56") — 고치기 전 실패 = KG50R-F02 이유 · 단계 표지 없음 뿐 (안전 차이 아님) |
| RBP1 · RBP2 b–g | 잡이 상대 경로 `-in input_…` 를 읽음 (검사한 덱 절대 경로 아님) · 러너 = 헬퍼 sed 사본 · 영수증 둘 · 헬퍼 원본 · LMP_IDENTITY 없음 |
| RBR1–5 | 본 제출함 (재대조가 재개 덱 · 러너 둘뿐 · 영수증 파일 자체를 안 묶음) |

칸마다 표 = 아래 §4-1 (기록에서 뽑음 · 앞 12 자).

### 4-1. 칸별 (before_py311_mawk.log)

| 칸 | 고치기 전 도구가 낸 sbatch | 돈 잡 (종류:job · cwd 끝 · -in · 읽은 바이트 sha256 앞 12) | 검사한 재개 덱 · 시험 덱 sha256 앞 12 |
|---|---|---|---|
| RB1 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts.bak 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts.bak fc7cd46b6de0 | b73b508611c2 · 038267335faa |
| RB2 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts.bak bb578f2de764 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts.bak MISSING | b73b508611c2 · 038267335faa |
| RB3 | [trial, main] | trial:7001 cwd …/kg50_d07_b40.ins1 -in input_kg50_d07_b40_r56t.liggghts MISSING · main:9001 cwd …/kg50_d07_b40.ins1 -in input_kg50_d07_b40_r56.liggghts MISSING | b73b508611c2 · 038267335faa |
| RB4 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40.liggghts 39b4990ad619 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40.liggghts 39b4990ad619 | b73b508611c2 · 038267335faa |
| RB4b | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB5 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB6 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 39b4990ad619 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts 39b4990ad619 | 39b4990ad619 · 39b4990ad619 |
| RB7a | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40.liggghts 39b4990ad619 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40.liggghts 39b4990ad619 | b73b508611c2 · 038267335faa |
| RB7b | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | 39b4990ad619 · 39b4990ad619 |
| RB8 | [trial, main] | trial:7001 cwd …/root -in input_kg50_d07_b40_r56t.liggghts MISSING · main:9001 cwd …/root -in input_kg50_d07_b40_r56.liggghts MISSING | b73b508611c2 · 038267335faa |
| RB9 | [trial, main] | trial:7001 cwd …/root -in input_kg50_d07_b40_r56t.liggghts MISSING · main:9001 cwd …/root -in input_kg50_d07_b40_r56.liggghts MISSING | b73b508611c2 · 038267335faa |
| RB9b | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB25 | [] | - | b73b508611c2 · 038267335faa |
| RB26 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB27 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB28 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB29 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB30 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB10 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB11 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB12 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB13 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB14 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB15 | [trial, main] | trial:7001 cwd …/root -in input_kg50_d07_b40_r56t.liggghts MISSING · main:9001 cwd …/root -in input_kg50_d07_b40_r56.liggghts MISSING | b73b508611c2 · 038267335faa |
| RB16 | [trial] | trial:7001 cwd …/root -in input_kg50_d07_b40_r56t.liggghts MISSING | b73b508611c2 · 038267335faa |
| RB17 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB18 | [trial] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa | b73b508611c2 · 038267335faa |
| RB20 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB22 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB23 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB19 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RB21 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r0t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r0.liggghts b73b508611c2 | - · - |
| RB24 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r5.liggghts MISSING · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r5.liggghts MISSING | - · - |
| RBR1 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts fed78c031577 · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · fed78c031577 |
| RBR2 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RBR3 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RBR4 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |
| RBR5 | [trial, main] | trial:7001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56t.liggghts 038267335faa · main:9001 cwd …/kg50_d07_b40 -in input_kg50_d07_b40_r56.liggghts b73b508611c2 | b73b508611c2 · 038267335faa |

## 5. 기존 시험에서 바뀐 것 (설계가 요구한 것만)

- 기존 `chk` 판정 줄: **바뀐 것 없음** (bf8cf21c6 대비 지운 줄 = 하네스뿐).
- 하네스: ① 가짜 sbatch 가 러너를 실제로 돌림 (위 §2) ② 가짜 dem_restart.py 의 러너 = `cd $HOME/dem_test/<케이스>` (가짜 루트의 작업 폴더가 아니고 `--output` 도 없었다 — 러너를 안 돌려 안 보였다) → 실제 헬퍼 꼴 (`--output` · `cd <작업 폴더 실제 경로>`) — 설계 (1) "cd 실제 경로 = 작업 폴더" 가 요구 ③ `--compare-old` 작업 폴더 지도에서 `run_*.sh` 뺌 (러너 = 도구 틀이 된 게 정상) ④ make_root = 가짜 mpirun · 아무것도 안 하는 conda · 빈 `~/.bashrc` ⑤ invoke = `root` (`-r` 값) · `{L}` 자리표 · 가짜 mpirun 기록 반환 · `FAKE_RUNNER` · `FAKE_EDIT_GLOB` · `FAKE_DROP_LAST_GLOB` 를 넘겨받은 환경에서 지움.
- 옛 도구도 이 하네스에서 기존 216 칸을 다 통과한다 (§3 고치기 전 열) — 하네스 변경이 기존 장면의 판정을 안 바꿨다는 근거.

## 6. 변이 (`mutation/mutation_F02.txt` · 고친 도구 사본에서 새 관문을 하나씩 끄고 `--only RB` · 운전기 `mutation/mutate_f02.py` · 변이마다 기록 `mutation/logs/`)

| 변이 | 결과 | RB PASS/FAIL | 실패한 시험 | 기대 (표지만) |
|---|---|---|---|---|
| M01_shebang | 잡힘 | 51/1 | RB22 | RB22 |
| M02_sbatch_after_cmd | 잡힘 | 51/1 | RB12 | RB12 |
| M03_sbatch_unknown_key | 잡힘 | 51/1 | RB10 | RB10 |
| M04_sbatch_dup_key | 잡힘 | 51/1 | RB11 | RB11 |
| M05a_jobname_value | 잡힘 | 51/1 | RB17 | RB17 |
| M05b_output_value | 잡힘 | 51/1 | RB18 | RB18 |
| M05c_n_value | 잡힘 | 50/2 | RB28 RB30 | RB28 RB30 (sed 를 정해진 꼴만 고치게 바꾼 뒤 닿음) |
| M06_token_value | 잡힘 | 51/1 | RB20 | RB20 |
| M07_env_after_cd | 잡힘 | 51/1 | RB13 | RB13 |
| M08_cd_count | 잡힘 | 50/2 | RB9 RB9b | RB9b |
| M09_cd_safe_path | 잡힘 | 51/1 | RB14 | RB14 |
| M10_cd_realpath | 잡힘 | 51/1 | RB3 | RB3 |
| M11_mpirun_count | 잡힘 | 51/1 | RB5 | RB5 |
| M12_mpirun_before_cd | 잡힘 | 51/1 | RB15 | RB15 |
| M13_comment_line | 잡힘 | 50/2 | RB4 RB4b | RB4b |
| M14_mpirun_any_in | 잡힘 | 50/2 | RB1 RB2 | RB1 RB2 |
| M15_other_command | 잡힘 | 51/1 | RB6 | RB6 |
| M16_mpirun_meta_msg | 잡힘 | 50/2 | RB7a RB7b | RB7a RB7b (문구 · 거부는 다른 문구로 남음) |
| M16b_meta_msg | 살아남음 | 52/0 | - | 없음 (문구만 · 그 줄은 아래 "허용 목록에 없는 명령 줄" 로 거부) |
| M17_required_keys | 잡힘 | 51/1 | RB23 | RB23 |
| M18_cd_missing | 잡힘 | 51/1 | RB8 | RB8 (문구 · cd 앞 거부는 남음) |
| M19_mpirun_missing | 잡힘 | 51/1 | RB25 | RB25 |
| M20_cr | 잡힘 | 51/1 | RB16 | RB16 (문구) |
| M21_nul | 잡힘 | 51/1 | RB26 | RB26 |
| M22_utf8 | 잡힘 | 51/1 | RB27 | RB27 (문구) |
| M23_np_valid | 잡힘 | 51/1 | RB21 | RB21 |
| M24_wr_safe | 잡힘 | 51/1 | RB19 | RB19 |
| M25_wr_consistent | 살아남음 | 52/0 | - | 없음 (WR = pwd -P 라 닿지 않음) |
| M26_deck_path_safe | 잡힘 | 51/1 | RB24 | RB24 |
| M27_receipt_two | 잡힘 | 47/5 | RBP1 RBP2 RBR1 RBR2 RBR3 | RBR1 RBR2 RBR3 RBP1e RBP2e |
| M28_receipt_memory | 잡힘 | 50/2 | RBR4 RBR5 | RBR4 RBR5 |
| M29_recheck_off | 잡힘 | 49/3 | RBR1 RBR2 RBR3 | RBR1 RBR2 RBR3 |
| M30_gate_ng_off | 잡힘 | 19/33 | RB1 RB10 RB11 RB12 RB13 RB14 RB15 RB16 RB17 RB18 RB19 RB2 RB20 RB21 RB22 RB23 RB24 RB25 RB26 RB27 RB28 RB29 RB3 RB30 RB4 RB4b RB5 RB6 RB7a RB7b RB8 RB9 RB9b | 음성 전부 (단계 표지 · 영수증 단계가 대신 막음) |
| M31_old_derivation | 잡힘 | 11/41 | RB1 RB10 RB11 RB12 RB13 RB14 RB15 RB16 RB17 RB18 RB19 RB2 RB20 RB21 RB22 RB23 RB24 RB25 RB26 RB27 RB28 RB29 RB3 RB30 RB4 RB4b RB5 RB6 RB7a RB7b RB8 RB9 RB9b RBP1 RBP2 | 음성 전부 · RBP b c d |
| M32_in_relative | 잡힘 | 46/6 | RBP1 RBP2 | RBP b c d |
| M33_cd_logical_w | 잡힘 | 51/1 | RBP1 | RBP1d (별칭 장면) |
| M34_helper_orig_off | 잡힘 | 50/2 | RBP1 RBP2 | RBP f |
| M35_identity_off | 잡힘 | 48/4 | RBP1 RBP2 | RBP d f g |
| M36_rm_stale_trial | 살아남음 | 52/0 | - | 없음 (새 루트라 옛 시험 러너가 없음 · 위생만) |
| M39_loose_rewrite | 잡힘 | 49/3 | RB28 RB29 RB30 | RB28 RB29 RB30 (옛 -n · -np 고침 = 대조 전에 어긋남을 지움) |
| M38_receipt_write_check | 살아남음 | 52/0 | - | 없음 (러너 관문이 먼저 막아 영수증 쓰기 실패에 닿지 않음 · 겹 방어) |

합계: 변이 41 · 잡힘 37 · 살아남음 4 · 못 만듦 0

## 7. D2 예 — 도구가 쓰는 본 · 시험 러너 (`d2_example/` · 고친 도구의 runnerck 함수를 글 그대로 떼어 모래 상자에서 · ibb 꼴 = `/home/yonghoon` → `/lustre/home/yonghoon` 링크 · 모래 상자 앞머리를 지운 글)

*[2 판: 아래는 1 판 도구 (5f4ffb46) 의 글 — 2 판 도구 (e5a61181) 의 글 = §0-6]*

본 `run_kg50_d2_b50_r4.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=kg50_d2_b50_r4
#SBATCH --output=logs/output_kg50_d2_b50_r4_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 4
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd "/lustre/home/yonghoon/dem_test/kg50_d2_b50"
echo "LMP_IDENTITY record-only (not a gate, 10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts sha256=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts" | cut -c1-64)"
mpirun --oversubscribe --bind-to none -np 4 lmp_mpi -in "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4.liggghts"
```

시험 `run_kg50_d2_b50_r4t.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=kg50_d2_b50_r4t
#SBATCH --output=logs/output_kg50_d2_b50_r4t_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 4
#SBATCH --time=01:00:00

source ~/.bashrc
conda activate myenv
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd "/lustre/home/yonghoon/dem_test/kg50_d2_b50"
echo "LMP_IDENTITY record-only (not a gate, 10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts sha256=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts" | cut -c1-64)"
mpirun --oversubscribe --bind-to none -np 4 lmp_mpi -in "/lustre/home/yonghoon/dem_test/kg50_d2_b50/input_kg50_d2_b50_r4t.liggghts"
```

## 8. 못 닫은 것 · 한계

- **실제 경로 같음 = ibb 가 링크일 때만**: ibb 의 헬퍼 cd (`/lustre/home/yonghoon/…`) ↔ 도구 루트 (`/home/yonghoon/dem_test`) 가 같은 폴더라는 판단은 받은 기록 (D2 r4 러너 · 09-27 r075 r30 러너 · D2 보고의 작업 폴더) 에서 추정했다 — `/home/yonghoon` 이 링크라야 `cd -P` · `realpath` 가 같은 경로를 낸다.  bind mount 처럼 링크가 아니면 정상 D2 러너도 `cd 실제 경로 [/lustre/…] ≠ 작업 폴더 실제 경로 [/home/…]` 로 **거부**된다 (안전한 쪽 실패 · 제출 없음).  ibb 에서 `-T` 한 번이 확인이다 (이번에 안 함).
  *[2 판: **확인됨 (1저자 ibb 화면 10-30)** — `readlink -f ~` → `/lustre/home/yonghoon` · `cd ~/dem_test && pwd -P` → `/lustre/home/yonghoon/dem_test` · §0-7]*
- **잡 안 신원은 기록만**: `LMP_IDENTITY` 줄 (lmp_mpi 경로 · sha256 · 잡 시작 때 덱 sha256) 은 관문이 아니다.  본 잡이 대기열에서 늦게 시작하면 본 제출 직전 대조 **뒤** 에 덱 · 체크포인트가 바뀐 것은 도구가 못 본다 (본 로그의 그 줄을 사람이 본다).  러너 안에서 sha256 이 다르면 멈추게 하는 것 = 이번 설계 밖 (다음 결정 거리).
  *[2 판: 닫힘 — 시험 로그 신원 줄 = G0 관문 · 러너가 잡 시작 때 덱 · 체크포인트 sha256 을 대조해 다르면 mpirun 안 함 · 남는 틈 = §0-2 · §0-7]*
- **영수증 다섯 밖 입력**: 덱이 잡 중에 읽는 다른 파일 (판 메시 `file plate_*.stl` 등) 은 영수증에 없다.
- **환경 줄**: `source ~/.bashrc` · `conda activate` 를 러너에 그대로 옮긴다 — .bashrc 의 함수 · 별칭 (예: `mpirun` 함수) 이 실행을 바꿀 수 있다 (LMP_IDENTITY 는 lmp_mpi 만 적는다).  제출 셸의 `SBATCH_*` 환경 변수는 #SBATCH 보다 앞선다 — 안 본다.
  *[2 판: `command mpirun` (셸 함수 mpirun 건너뜀) · 환경 줄 셋 꼴 음성 RB32 · conda 이름 규칙 · 믿는 입력 범위 = §0-2]*
- **엄격함의 값**: 헬퍼 (`~/dem_test/dem_restart.py`) 가 다른 꼴을 쓰면 (새 #SBATCH 키 · 줄 순서 · 주석) 도구를 고치기 전까지 전부 거부된다 (안전한 쪽).
- 변이 생존 4 개 = M16b_meta_msg (없음 (문구만 · 그 줄은 아래 "허용 목록에 없는 명령 줄" 로 거부)) · M25_wr_consistent (없음 (WR = pwd -P 라 닿지 않음)) · M36_rm_stale_trial (없음 (새 루트라 옛 시험 러너가 없음 · 위생만)) · M38_receipt_write_check (없음 (러너 관문이 먼저 막아 영수증 쓰기 실패에 닿지 않음 · 겹 방어)) — §6 표.
  *[2 판: M16b · M25 · M36 = 새 칸 RB37 · RBU2 · RB36b 가 잡는다 · 2 판 변이 = §0-5]*
- **가짜 하네스의 한계**: 실제 SLURM 이 아니다 — 가짜 sbatch 는 러너를 그 자리에서 (동기) `bash <러너>` 로 돌린다 (shebang 해석 · 노드 · 대기열 · `%j` 밖 출력 패턴 없음) · 가짜 mpirun 은 `-in` 만 읽는다 (LIGGGHTS 안 돎).
- 실제 ibb SLURM · LIGGGHTS 실행 · `scripts/check_all.sh` 는 돌리지 않았다 (지시대로 · 메인 세션 몫).
- 원장 (`docs/reviews/findings.json`) · 절차 문서 · CLAUDE.md 는 고치지 않았다 (메인 세션 몫).

## 9. 다시 돌리기 (리포 뿌리)

*[2 판: 전체 = 307 · RB = 91 · 변이 운전기 = `r2/mutation/mutate_f02.py` (같은 인자) · D2 예 = `r2/d2_example/d2_example.sh` (같은 인자) ·
탐침 = `python3 -I r2/preattack/rck_probe11.py <도구>` · `python3 -I r2/preattack/cdfail_probe11.py <도구>`]*

```bash
python3 -I scripts/test_resume_ckpt.py                       # 전체 (268)
python3 -I scripts/test_resume_ckpt.py --only RB             # RB 묶음만 (52)
PATH=<gawk 를 awk 이름으로 둔 폴더>:$PATH python3 -I scripts/test_resume_ckpt.py
python3.8 -I scripts/test_resume_ckpt.py                     # 하네스만 3.8
PATH=<python3 → python3.8 링크 폴더>:$PATH python3.8 -I scripts/test_resume_ckpt.py   # 도구 안 python3 도 3.8
python3 -I scripts/test_resume_ckpt.py --compare-old <고치기 전 판 사본>
python3 -I docs/reviews/kg50rf_fix_evidence_20261030/F02/mutation/mutate_f02.py <리포 뿌리> <고친 도구 사본> <빈 출력 폴더> 3
bash docs/reviews/kg50rf_fix_evidence_20261030/F02/d2_example/d2_example.sh <리포 뿌리> <빈 모래 상자 폴더>
```
고치기 전 판 = `git show bf8cf21c6:scripts/resume_ckpt.sh` (위 표의 before = 리포 사본을 그 판으로 둔 채 같은 명령).

