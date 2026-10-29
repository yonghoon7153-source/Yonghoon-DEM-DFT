# KG50R-F02 — 검사한 덱 ↔ 잡이 읽는 덱 결속 (10-30 · 증거)

- 결함: Codex 재확인 (2026-10-30 · 리뷰 핀 bf8cf21c6 · 판정문 §2 KG50RF-02 · §7 영수증 한정 · 판정문 반입은 메인 세션 몫) = 원장 KG50R-F02 (P1).
  러너 관문이 부분 글자 grep 셋이라 `-in …r56.liggghts.bak` 러너 · 주석 속 정상 줄 · 다른 cd · 둘째 MPI 실행이 통과했다 · 시험 러너 = 헬퍼 러너의 sed 사본 ·
  실행 영수증 `main_inputs.sha256` = 재개 덱 · 러너 둘 (체크포인트 sha256 은 tool.txt 기록만 · lmp_mpi sha256 = 제출 셸 PATH).
- 비준 설계: 1저자 10-30 Q2 *"권고대로"* — (1) 헬퍼 러너 줄마다 엄격 대조 (2) 본 · 시험 러너를 도구가 한 틀로 씀 (3) 실행 입력 영수증 다섯 + 본 제출 바로 전
  다시 대조 (4) 가짜 sbatch 가 러너를 실제로 돌리는 시험.
- 바꾼 파일: `scripts/resume_ckpt.sh` (새 함수 runnerck · 러너 · 영수증 · 본 제출 구간) · `scripts/test_resume_ckpt.py` (가짜 sbatch · 가짜 mpirun ·
  가짜 dem_restart.py 러너 · RB 묶음).  정적 대조 Python (setup_check · setup_order · state_cmp) 은 손대지 않았다 (같은 때 다른 작업 트리가 고치는 자리).
  파일 머리 주석 (1–48 줄) 에도 이번 절을 안 넣었다 — 그 자리를 다른 작업 트리도 고칠 수 있어 병합 때 메인 세션이 한 줄 넣는다.
- 도구 sha256: 고치기 전 77c242375c4093023e609703ef471c64c2370d374e7533824412d96da5b1b9f8 → 고친 뒤 5f4ffb46ae70ad3926685f891c25daed721dd37a42bc3a3079a31e6eca4f188e.
- 작업 가지 커밋 (worktree-agent-ab1d2d1fe4868ba68 · 메인 세션이 옮기면 번호가 바뀐다): 시험 먼저 c3c67fb37 · 고침 2107f144f · 증거 = 이 폴더를 넣은 커밋.
- 환경: 클라우드 컨테이너 (Linux · GNU bash 5.2.21) · 가짜 SLURM (sbatch · sacct · squeue · sleep) · 가짜 mpirun · 가짜 dem_restart.py —
  실제 ibb SLURM · MPI · LIGGGHTS 실행 없음.
- ⚠ 작업 도중 컨테이너 디스크가 한때 가득 찼다 (메인 세션 알림 · ENOSPC).  그 창에 돈 첫 변이 판 (40 개 중 2 개에 엉뚱한 실패) 은 버렸고, 커밋을 다시 만든 뒤
  before · after · 변이를 전부 새로 돌렸다.  아래 기록은 다시 돈 것뿐이다 (기록마다 'No space left' 줄 0 — §3 표).

## 1. 고친 것 (`scripts/resume_ckpt.sh` · 설계 = 1저자 10-30 Q2 비준 그대로)

| 자리 | 예전 (77c24237) | 이제 |
|---|---|---|
| -n · -np 고침 (sed · 헬퍼 러너) | `#SBATCH -n ` 로 시작하는 줄 **전체** · 줄 **어디든** `mpirun … -np [숫자 0 개 이상]` 을 고쳤다 → 엄격 대조 전에 어긋남이 지워진다 (`#SBATCH -n 1 --nodes=2` → `-n 56` · `-np` 숫자 없음 → 정상 꼴) | 정해진 꼴만: 줄 전체 `#SBATCH -n <숫자>` · 줄 첫머리 `mpirun [--oversubscribe ][--bind-to none ]-np <숫자> lmp_mpi -in ` — 그 밖은 고치지 않고 아래 대조가 거부.  **엄격 대조는 이 고침 뒤** (선택 · 설계의 "-n = NP" · "-np NP" 를 그대로 대조하려고 — 헬퍼가 쓰는 `-n` · `-np` 값은 도구의 NP 와 다를 수 있다: 시험 가짜 헬퍼 = 1 · 실제 헬퍼의 원래 값은 리포 기록에 없다 (D2 러너 사본은 옛 도구가 고친 뒤 글)) · 헬퍼 원본 바이트 (고침 전) = 시도 폴더 `helper_run_<C>_<SFX>.sh.orig` |
| 러너 관문 | grep 셋 — `^#SBATCH -n NP$` 한 줄 있음 · 본 러너 어딘가에 `--oversubscribe --bind-to none -np NP lmp_mpi` · 시험 러너 어딘가에 `-np NP lmp_mpi -in input_<C>_<SFX>t.liggghts` (부분 글자) | 새 함수 runnerck (`python3 -I` · 이 구간 밖 Python 은 안 건드림) 가 헬퍼 러너를 **줄마다** 대조 — 받는 꼴: 첫 줄 `#!/bin/bash` · `#SBATCH --job-name=<C>_<SFX>` · `--output=logs/output_<C>_<SFX>_%j.out` · `-n NP` · `--time=<낱말>` (각 한 번 · 꼭) · `--qos=` · `--partition=` (한 번까지 · 낱말 A-Z a-z 0-9 _ . : , + -) · #SBATCH 는 첫 명령 줄 앞 · 빈 줄 · 환경 줄 (`source ~/.bashrc` · `conda activate <이름>` · `export (OMP\|MKL\|OPENBLAS\|NUMEXPR)_NUM_THREADS=1` · cd 앞) · `cd <절대 경로>` 한 번 (실제 경로 = 작업 폴더 실제 경로 · `.` `..` 마디 · 따옴표 · `$` · 공백 없음) · 그 다음 `mpirun --oversubscribe --bind-to none -np NP lmp_mpi -in <$D 의 이름>` 한 번.  그 밖 (주석 줄 · 다른 명령 · `;` `&&` `\|\|` `\|` 리디렉션 `$(` 백틱 · 둘째 MPI 실행 · 두 cd · CR · NUL · UTF-8 아님) = 거부 → `ng` (단계 "정적 대조 · 시험 덱 · 러너" · 이유 "헬퍼 러너 엄격 대조 실패 (10-30 KG50R-F02 …) — 문제 N: 줄 k [원문] — 이유 \| …") · sbatch 전 · 대조 기록 = 시도 폴더 `runner_check.txt` |
| 시험 러너 | 헬퍼 러너의 sed 사본 (`s/<C>_<SFX>/<C>_<SFX>t/g` · `--time=01:00:00`) — `.bak` · 다른 cd · 둘째 실행 줄이 그대로 따라왔다 | 대조 통과 = 본 `run_<C>_<SFX>.sh` · 시험 `run_<C>_<SFX>t.sh` 를 도구가 **한 틀**로 씀: 대조한 #SBATCH 값 (시험 = 이름 끝 t · `--time=01:00:00`) · 환경 줄 (순서 그대로) · `cd "<작업 폴더 실제 경로>"` (`cd -P` + `pwd -P`) · 잡 안 신원 기록 줄 하나 (`LMP_IDENTITY` — 잡 안 PATH 의 lmp_mpi 경로 · sha256 · 잡 시작 때 덱 sha256 · **기록만 · 관문 아님**) · `mpirun --oversubscribe --bind-to none -np NP lmp_mpi -in "<검사한 덱 절대 경로>"` 한 줄 (본 = $D · 시험 = $TD).  작업 폴더 실제 경로 · 덱 · 러너 이름에 A-Z a-z 0-9 _ . + - / 밖 글자 = 거부 (러너의 `"…"` 안에서 `$` 백틱 `\` 가 펼쳐진다) · NP = 1 이상 정수 |
| 실행 영수증 `main_inputs.sha256` | 재개 덱 · 러너 둘 (작업 폴더 경로) · 체크포인트 sha256 은 tool.txt 기록만 | 러너가 실제로 읽는 자리 (작업 폴더 실제 경로 · 러너의 cd · -in 과 같은 절대 경로) 의 **다섯**: 재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트 · 다섯 다 못 쓰면 시험 안 냄 · 그 파일 sha256 = 이 호출 메모리 (`SUBMITTED` 셋째 칸) |
| 본 제출 바로 전 | `sha256sum -c` (재개 덱 · 러너) | ① 영수증 파일 sha256 = 메모리 값 (`sha256sum -c` 는 줄이 빠지거나 덧붙은 영수증도 통과 — 실측) ② `sha256sum -c --quiet` 다섯 — 하나라도 다르면 본 제출 안 함 · 보고에 다른 파일 이름 (`…: FAILED`) |
| 보고 · tool.txt | — | 러너 대조 줄 · 시험 잡 안 신원 줄 (`LMP_IDENTITY` 를 옮기기만) · 본 제출 직전 확인 줄에 다섯 · tool.txt 에 영수증 sha256 · "위 lmp_mpi 줄 = 제출 셸 PATH" 표지 · 거부 단계 이름 "정적 대조 · 시험 덱 · 러너" |

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
- **잡 안 신원은 기록만**: `LMP_IDENTITY` 줄 (lmp_mpi 경로 · sha256 · 잡 시작 때 덱 sha256) 은 관문이 아니다.  본 잡이 대기열에서 늦게 시작하면 본 제출 직전 대조 **뒤** 에 덱 · 체크포인트가 바뀐 것은 도구가 못 본다 (본 로그의 그 줄을 사람이 본다).  러너 안에서 sha256 이 다르면 멈추게 하는 것 = 이번 설계 밖 (다음 결정 거리).
- **영수증 다섯 밖 입력**: 덱이 잡 중에 읽는 다른 파일 (판 메시 `file plate_*.stl` 등) 은 영수증에 없다.
- **환경 줄**: `source ~/.bashrc` · `conda activate` 를 러너에 그대로 옮긴다 — .bashrc 의 함수 · 별칭 (예: `mpirun` 함수) 이 실행을 바꿀 수 있다 (LMP_IDENTITY 는 lmp_mpi 만 적는다).  제출 셸의 `SBATCH_*` 환경 변수는 #SBATCH 보다 앞선다 — 안 본다.
- **엄격함의 값**: 헬퍼 (`~/dem_test/dem_restart.py`) 가 다른 꼴을 쓰면 (새 #SBATCH 키 · 줄 순서 · 주석) 도구를 고치기 전까지 전부 거부된다 (안전한 쪽).
- 변이 생존 4 개 = M16b_meta_msg (없음 (문구만 · 그 줄은 아래 "허용 목록에 없는 명령 줄" 로 거부)) · M25_wr_consistent (없음 (WR = pwd -P 라 닿지 않음)) · M36_rm_stale_trial (없음 (새 루트라 옛 시험 러너가 없음 · 위생만)) · M38_receipt_write_check (없음 (러너 관문이 먼저 막아 영수증 쓰기 실패에 닿지 않음 · 겹 방어)) — §6 표.
- **가짜 하네스의 한계**: 실제 SLURM 이 아니다 — 가짜 sbatch 는 러너를 그 자리에서 (동기) `bash <러너>` 로 돌린다 (shebang 해석 · 노드 · 대기열 · `%j` 밖 출력 패턴 없음) · 가짜 mpirun 은 `-in` 만 읽는다 (LIGGGHTS 안 돎).
- 실제 ibb SLURM · LIGGGHTS 실행 · `scripts/check_all.sh` 는 돌리지 않았다 (지시대로 · 메인 세션 몫).
- 원장 (`docs/reviews/findings.json`) · 절차 문서 · CLAUDE.md 는 고치지 않았다 (메인 세션 몫).

## 9. 다시 돌리기 (리포 뿌리)

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

