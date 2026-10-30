# 50kg 재개 도구 통합판 독립 사전 공격 (PAI · 10-30) — `scripts/resume_ckpt.sh` sha256 `2dc7f693…`

> ※ 10-30 통합: 이 문서의 커밋 SHA 는 본 가지 (claude/stoic-knuth-NObVQ) 에 들어간 SHA 로 바꿔 적었다 (작업 트리 가지 SHA 는 원격에 없어서 통합 SHA 로 바꿨다).


- 대상: 커밋 `26e748af2` 의 `scripts/resume_ckpt.sh` (sha256 `2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8` · 처음에 확인) · 비교 기준 = Codex 가 마지막으로 본 핀 `bf8cf21c6` (도구 `77c24237…`).
- 범위: KG50R-F01 1·2 판 (정적 대조 · 사전 공격 R1–R8) + KG50R-F02 1·2 판 (러너 결속 · 영수증 · 잡 안 대조 · G0 신원) 통합판.  실제 D0.7 (`kg50_d07_b50` · v3 50×50 · settling 체크포인트 step 20001 · NP 56) 에 쓸 수 있는지.
- 환경: 이 리포 클라우드 컨테이너 (Linux · GNU bash 5.2.21 · Python 3.11.15 · 3.8.20 · awk = mawk 1.3.4) · 리포의 가짜 SLURM 하네스 (`scripts/test_resume_ckpt.py` — 가짜 sbatch 가 러너를 **실제로 돌리고** 가짜 mpirun 이 cwd · argv · `-in` 파일 sha256 을 적는다).  실제 ibb · SLURM · MPI · LIGGGHTS · ibb `dem_restart.py` 실행 없음.
- D0.7 재개 덱: `dem_restart.py` 사본이 리포에 없어서 **D2 선례에서 변환을 배워** 만들었다 — 변환 T 를 D2 본 덱에 적용한 결과가 받은 D2 r4 덱 (도구가 한 두 고침 = 템플릿 줄 · 179999→180000 을 되돌린 것) 과 **바이트 같음** 을 확인한 뒤 같은 T 를 D0.7 본 덱 (같은 257 줄 틀) 에 적용 (`probes/make_d07_resume.py`).  헬퍼 러너 = D2 r4 러너 꼴 (`cd <작업 폴더 실제 경로>`).
- 탐침 = `probes/` · 실행 기록 = `logs/` (스크래치 경로가 찍혀 있다 · 결과는 같은 줄 끝 `[rc=…]`).

## 0. D0.7 한 건 본 제출에 영향 있는 것 / 없는 것

| # | 질문 | 답 (이 컨테이너 · 가짜 SLURM) | 근거 | D0.7 영향 · 오늘 할 일 |
|---|---|---|---|---|
| 1 | 실제 D0.7 꼴 재개 덱이 `-C` 를 지나는가 (잘못된 거부) | **지난다** — rc 0 · `통과 (문제 0)` · 남은 step 끝 200001 · 뒤 64 명령 같음 · 그 자리 치환 4 곳 상수 · 받은 D2 쌍도 같은 결과 | `logs/c_real.log` | 없음 |
| 2 | `-T -n 56 -s ins1 -r ~/dem_test kg50_d07_b50` 끝-끝 | rc 0 · 시험 sbatch 1 · 본 0 · 시험 잡의 mpirun cwd = 작업 폴더 실제 경로 · `-in` = 검사한 시험 덱 절대 경로 · 잡이 읽은 sha256 `94db4187…` = 검사한 시험 덱 · G0 (신원 관문 포함) · G1 · G2 · G3 통과 · 끝에 본 제출 명령 한 줄 | `logs/e2e_T.log` | 없음 |
| 3 | 본 흐름 (`-x r56 -t 2000 -A -H`) 끝-끝 | 시험 1 · 본 1 · 본 잡이 읽은 덱 sha256 `8e129f42…` = 검사한 재개 덱 · 영수증 다섯 = 러너가 읽는 절대 경로 · 체크포인트 sha256 = 잡 안 대조 값 | `logs/e2e_M.log` | 없음 |
| 4 | 시험 덱 = 검사한 덱의 앞부분인가 | 지금 cutter 가 받은 D2 r4t 를 **바이트 같게** 다시 만든다 (`aac7debc…`) · D0.7 r56t = 157 줄 · 끝 `run 2000` · 예산 2000 | `logs/cut_d2.log` | 없음 |
| 5 | **PAI-01** 판 메시 file 이름 허용이 작업 폴더 밖 · 다른 케이스 STL 을 받는다 | D0.7 꼴 덱의 뒤 구간 `fix top_mesh … file <절대 경로 · ../ · 아무 파일>` = `-C` rc 0 · 본 흐름 = 시험 · **본 제출** (시험 덱은 판 블록 앞에서 잘려 못 본다) · 보고에는 `통과 (문제 0)` 만 | `logs/mesh_escape.log` · `logs/e2e_MX.log` | **조건부** — 재구성한 D0.7 덱은 이 허용을 안 쓴다.  `-T` · 본 시도 폴더의 `deckcheck_r56.txt` 에 `판 메시 파일만 다름` 줄이 **0** 인지 본다 |
| 6 | **PAI-02** `-T` 에서 본 입력과 본 호출 입력이 묶였나 | 안 묶였다 — 승인 = 도구 · 헬퍼 sha256 뿐.  `-T` 뒤 멈춘 폴더 본 덱의 `press_speed 0.01 → 0.02` (+ 헬퍼가 다시 만든 재개 덱) = 본 호출이 새 시험 (정착 2,000 step · 영향 없음) 통과 뒤 **본 제출** · 재개 덱 sha256 `5c5a5089…` ≠ `-T` 의 `8e129f42…`.  아무것도 안 바뀌면 두 영수증 파일이 **바이트 같다** (로그 `8342e4b0…` 둘 — 러너에 작업 폴더 경로가 들어가 값은 실행마다 다르다) | `logs/e2e_TM2.log` · `logs/e2e_TM2_control.log` | **절차** — 본 명령을 낸 뒤 새 시도 폴더 `main_inputs.sha256` 의 sha256 = `-T` 시도 폴더 것인지 시험이 끝나기 전에 보고, 다르면 시험 잡 `scancel` (G0 실패 → 본 제출 없음) |
| 7 | PAI-04 ibb `/home` ↔ `/lustre` | 새 runnerck = `realpath(cd 경로) == cd -P 작업 폴더 && pwd -P` 가 같아야 한다.  실제 ibb 헬퍼 러너 둘 = `cd /lustre/home/yonghoon/…` · D2 보고 = `-r /home/yonghoon/dem_test`.  `/home/yonghoon` 이 링크면 같고, bind mount 면 다르다 — **이 컨테이너에서 못 정함** | 리포 러너 둘 · `resume_r4_1028_0942.md` | 다르면 `-T` 가 **시험 전 거부** (안전한 쪽 · 한 차례 손실).  사전 확인 한 줄 (아래) |
| 8 | Python 판 | 전체 433 = **3.11.15 · 3.8.20 둘 다 433 PASS · 0 FAIL** (3.8 = 하네스와 도구 안 `python3` 둘 다) | `logs/full_suite_py311_mawk.log` · `logs/full_suite_py38_shim.log` | ibb `python3 --version` (3.8 미만이면 이 결과 밖) |
| 9 | 체크포인트를 쓴 덱 (삽입 덱) | 도구는 삽입 덱을 안 읽는다 (본 덱과만 대조).  D0.7 삽입 덱 ↔ 본 덱 1–166 행 **같음** (다른 곳 = 167 행부터 = 정착 run 자리) | `diff` (§1 PAI-07) | 없음 (리포 덱 기준) · ibb 사본도 같은지 한 줄 |
| 10 | G3 (NP 1 삽입 로그 ↔ NP 56 시험 · 21000 행 KE 5 %) | 도구 결함 아님 · D2 (NP 4) 는 KE 가 8 자리까지 같았다 | `received_d2_resume_1028.tgz` 보고 | 실패하면 본 제출 명령이 안 나온다 (안전한 쪽) |

ibb 사전 확인 (읽기만 · `-T` 전):

```bash
cd ~/dem_test
sha256sum scripts/resume_ckpt.sh                                   # 2dc7f693263708d7…
realpath /lustre/home/yonghoon/dem_test; (cd -P ~/dem_test && pwd -P)   # 두 줄 같아야 (PAI-04)
ls ~/dem_test/*.py                                                 # dem_restart.py 만 (PAI-05)
find kg50_d07_b50.ins1 -type l                                     # 빈 출력 (멈춘 폴더 안 링크는 링크로 복사된다)
sha256sum kg50_d07_b50.ins1/input_kg50_d07_b50.liggghts            # 2555640c7792df69… (리포 v3)
diff <(sed -n 1,166p kg50_d07_b50.ins1/input_kg50_d07_b50.liggghts) <(sed -n 1,166p kg50_d07_b50.ins1/input_kg50_d07_b50_insert.liggghts)   # 빈 출력
python3 --version
# -T 뒤 (보고 · 시도 폴더 반입 전에)
grep -c '판 메시 파일만 다름' kg50_d07_b50/attempt_r56_*/deckcheck_r56.txt   # 0 (PAI-01)
grep -E '첫 긴 run 고침|남은 step|정적 대조:' kg50_d07_b50/attempt_r56_*/{fixrun,deckcheck}_r56.txt
sha256sum kg50_d07_b50/attempt_r56_*/main_inputs.sha256          # 적어 둔다 (PAI-02 · 본 호출 영수증과 비교)
```

## 1. 발견

| ID | 심각도 | 한 줄 | D0.7 |
|---|---|---|---|
| PAI-01 | **P1** (요청 정의: D0.7 꼴 잘못된 재개 덱 수용) · 열린 한정 KG50P-10 의 범위 위반 | 판 메시 file 이름 허용이 작업 폴더 밖 (절대 · `../`) · 다른 케이스 STL 을 받고, 그 파일은 영수증 · 잡 안 대조 밖 | 재구성 덱은 안 씀 (확인 한 줄) |
| PAI-02 | P2 | `-T` (검토 대상) ↔ 본 호출 입력이 결속되지 않음 — 승인은 도구 · 헬퍼 sha256 뿐 | 절차 확인 |
| PAI-03 | P3 | 증거 신원: F02 증거는 이 이력에 없는 곁가지 도구 (5f4ffb46 · e5a61181) 에서 잼 · 통합 sha256 (b24cc53a · 12bc95ce · 2dc7f693) 를 적은 README 없음 · F01 2 판 (R1–R8) 증거 = 커밋 메시지뿐 | 없음 |
| PAI-04 | P3 (가용성) | runnerck cd 실제 경로 = `pwd -P` 같음이 ibb `/home` ↔ `/lustre` 에서 성립하는지 미확인 | 사전 확인 |
| PAI-05 | P3 | 정적 대조 Python 이 `python3 -` (격리 아님) — 작업 루트의 `difflib.py` 같은 파일이 표준 모듈을 대신한다 (runnerck 는 `-I`) | 사전 확인 |
| PAI-06 | P3 | runnerck (러너에 박을 sha256) 가 정적 대조 **앞** 에 돈다 — 외부 쓰기가 둘 사이에 바꿨다 되돌리면 검사 안 한 바이트가 돌 수 있다 (ABA) | 외부 쓰기 없으면 없음 |
| PAI-07 | P3 | 기록 빈칸: 정적 대조의 기준 본 덱 sha256 미기록 · 체크포인트를 쓴 삽입 덱 미대조 · lmp_mpi 시험 ↔ 본 미대조 | 없음 (D0.7 = 1–166 행 같음) |
| PAI-08 | P3 | `-s` · `-r` 검사 없음 (따옴표 없이 씀) — `-s ins1/../decoy` = 다른 폴더를 멈춘 폴더로 복사 · 시험 제출 | 정해진 명령이면 없음 |
| PAI-09 | P3 | 하네스 '정상' settling 덱 (`res_good`) 은 `thermo_style` · `thermo` 를 뺀다 — 실제 LIGGGHTS 라면 기본 thermo 로 G0 가 실패할 덱 (추정) 이 하네스에선 양성 | 없음 (D0.7 끝-끝은 dem_restart.py 꼴) |

### PAI-01 (P1 · KG50P-10 범위 위반) — 판 메시 file 이름 허용이 작업 폴더 밖 · 영수증 밖

- 위치: `seq_cmp` (`scripts/resume_ckpt.sh:451–487`, 특히 `:467` `os.path.isfile(os.path.join(W, nf))`) · `same_or_mesh` (`:1062–1079`, `:1068` 같은 꼴) · `cmd_eq` / `mesh_file` (`:440` · `:1049`).  등록된 허용 차이 "판 메시 fix 의 file 이름 (**그 파일이 작업 폴더에 있을 때**)" (G6 ② · 1저자 Q2 (가)).
- 반례 (D0.7 꼴 · settling · 뒤 구간 `fix top_mesh all mesh/surface/stress file plate_kg50_d07_b50.stl …` (본 덱 200 행 = 재개 덱 190 행) 의 file 만 바꿈):

| file 이름 | `-C` rc | 판정 |
|---|---|---|
| `<스크래치>/elsewhere/plate_kg50_d2_b50.stl` (절대 경로 · 작업 폴더 밖 · 다른 케이스 판) | 0 | `통과 (문제 0)` + 노트 `판 메시 파일만 다름 …` |
| `../elsewhere/plate_kg50_d2_b50.stl` | 0 | 같음 |
| `input_kg50_d07_b50_r56.liggghts` (작업 폴더 안 · STL 아님) | 0 | 같음 (Codex `mesh_empty_existing_file` 와 같은 부류) |
| `plate_nonexistent.stl` (대조) | 1 | `판 메시 파일 … 가 작업 폴더에 없음` |

- 본 흐름 (`logs/e2e_MX.log`): 같은 덱으로 시험 sbatch 1 · G0–G3 통과 · **본 sbatch 1** · 본 잡이 읽는 재개 덱 (`510dc99f…` = 검사 · 승인된 그 덱) 이 다른 케이스 판 STL 을 절대 경로로 읽는다 · 보고 줄 = `재개 덱 정적 대조: 통과 (문제 0)` (노트는 `deckcheck_r56.txt` · 화면에만).  즉 "검사한 덱 = 실행한 덱" 은 지켜지지만, 그 덱이 영수증 밖 파일을 읽는다.
- 왜 시험이 못 막나: settling 재개의 시험 덱은 첫 긴 run (정착) 에서 잘린다 — 판 블록 (182–200 행) 은 그 뒤.
- 왜 KG50P-10 (Codex §4 "열림 / 명시된 한정 · 존재 검사") 보다 넓은가: ① 한정 문구 "작업 폴더에 있을 때" 가 거짓 — `os.path.join(W, '/abs')` = `/abs` · `../` 는 밖으로 나간다 ② 그 파일은 본 잡이 **실제로 읽는 입력** 인데 `main_inputs.sha256` (다섯) · 잡 안 대조 (덱 · 체크포인트) 어디에도 없다 — KG50RF-02 의 "영수증은 실제로 읽을 파일을 묶어야" 와 같은 축.
- 최소 고침: (a) 허용할 때 `nf` = 이름만 (`/` · `..` 없음) · 작업 폴더 안 **보통 파일** (링크 아님) (b) 허용으로 바뀐 파일을 영수증 · 잡 안 sha256 대조에 넣는다 (c) 허용 노트를 보고 케이스 절에 그대로 옮긴다 (d) (1저자 결정) settling (restart 체크포인트) 꼴의 뒤 구간에서는 허용 끄기 — 덱이 그 STL 을 스스로 쓰고 읽는다.

### PAI-02 (P2) — `-T` ↔ 본 호출 입력 결속 없음

- 위치: 본 제출 승인 `:1584` (`-A` 도구 · `-H` 헬퍼 sha256 만) · `-T` 의 본 제출 명령 줄 `:2118` · 본 호출은 멈춘 폴더를 다시 복사하고 (`:1879`) 덱을 다시 만들고 (`:1893`) 다시 대조 · 시험한다.
- 장면 (`logs/e2e_TM2.log`): ① `-T` → 영수증 첫 줄 (재개 덱) `8e129f42…` · 본 제출 명령 한 줄 ② 멈춘 폴더 본 덱 `variable press_speed equal 0.01 → 0.02` (헬퍼가 그에 맞는 재개 덱을 낸다) ③ `-T` 가 찍은 명령과 같은 인자 (`-n 56 -s ins1 -r <루트> -x r56 -t 2000 -A <도구> -H <헬퍼>`) → 정적 대조 통과 (두 덱 같은 0.02) · 시험 (정착 2,000 step) G0–G3 통과 · **본 제출** · 영수증 첫 줄 `5c5a5089…` ≠ `-T` · 영수증 파일 `ee823d8d…` ↔ `56ed9f95…`.  대조군 (`logs/e2e_TM2_control.log`): 바뀐 것이 없으면 두 영수증 파일 sha256 이 같다 (`8342e4b0…` 둘) — 작업 폴더 경로가 같아 러너 바이트도 같다.
- 뜻: 계획 순서 "Codex = 고침 + 실제 `-T` 영수증 → GO → 본 제출" 에서 GO 의 대상 (`-T` 영수증) 과 실제 본 제출 입력이 같다는 것을 도구가 보지 않는다.  Codex Q2 는 "본 명령 = 새 호출 · 새 시험" 을 받아들였지만 `-T` 증거에 "선택 checkpoint · 실제 실행 덱/러너" 를 묶으라고 했다.
- 최소 고침: `-T` 보고에 `main_inputs.sha256` 의 sha256 을 적고 본 제출 명령에 `-R <그 값>` 을 붙인다 · 본 호출은 새 영수증 sha256 ≠ `-R` 이면 시험 · 본 제출을 하지 않는다.

### PAI-03 (P3) — 증거 신원 (Codex 가 "도구 · 입력 신원 고정" 을 다시 볼 자리)

- `docs/reviews/kg50rf_fix_evidence_20261030/F02/README.md` 의 수 (RB 91/91 · 변이 91 중 생존 3 · `--compare-old` 둘 다 정상 33 · "첫 1033 줄 sha256 = d0dc0cf4") = 곁가지 도구 `5f4ffb46` · `e5a61181` (이 이력에 없다).  이 이력의 통합 도구는 `b24cc53a` (07761cf54) · `12bc95ce` (48cfd2871) · `2dc7f693` (26e748af2) — 어느 README 에도 없다.
- F01 2 판 (R1–R8) 의 "실제 본 덱 24 쌍 rc 0" · "리뷰어 반례 덱 15 rc 1" · "VP 고치기 전 결과 = 증거 커밋" = 26e748af2 에 증거 파일 없음 (커밋 메시지뿐).
- 아래 §2 에서 2dc7f693 로 다시 쟀다 (리뷰어 덱 15 는 리포에 없어 못 잼).  고침 = 2dc7f693 을 이름으로 단 증거 README + 로그 반입.

### PAI-04 (P3 · 가용성) — runnerck cd 실제 경로 (ibb)

- `runnerck` `:1762` `os.path.realpath(s[3:]) != WR` (WR = `cd -P "$W" && pwd -P` · `:1928`).  실제 ibb 헬퍼 러너 = `cd /lustre/home/yonghoon/dem_test/<케이스>` (D2 r4 · 09-27 r075 r30) · 도구 호출 = `-r /home/yonghoon/dem_test` (D2 보고).
- `/home/yonghoon` → `/lustre/home/yonghoon` 링크면 같다.  bind mount 면 `pwd -P` = `/home/…` · realpath = `/lustre/…` → `헬퍼 러너 엄격 대조 실패 … cd 실제 경로 ≠ 작업 폴더 실제 경로` → 시험 전 거부.  안전한 쪽이지만 오늘 한 차례를 잃는다 — §0 사전 확인 한 줄.

### PAI-05 (P3) — 정적 대조 Python 격리 안 됨

- `deckcheck(){ python3 - "$@" <<'PY'` (`:63`) · 본 흐름의 cwd = `-r` 루트 (`:1590` `cd $L`).  `python3 -` 는 cwd 를 `sys.path[0]` 에 둔다 → 루트에 `difflib.py` 를 두면 정적 대조가 그것을 import 한다 (`logs/shadow_import.log` — 표지 줄 · 판정은 그대로).  runnerck 는 `python3 -I -` 라 표준 모듈 (`/usr/lib/python3.11/difflib.py`).  PYTHONPATH 도 같다.
- 고침: `python3 -I -`.  D0.7: `ls ~/dem_test/*.py` = `dem_restart.py` 만이면 영향 없음.

### PAI-06 (P3) — runnerck ↔ 정적 대조 순서 (ABA)

- `:1931` runnerck 가 재개 덱 · 시험 덱 · 체크포인트 sha256 을 러너 글에 박는다 → `:1955` 정적 대조 → `:1970` 영수증.  둘 사이에 외부 쓰기가 덱을 D′ 로 바꾸면 정적 대조 · 영수증은 D′ 를 보고 (본 제출 직전 `sha256sum -c` 도 D′ 로 통과), 본 잡 시작 전에 D 로 되돌리면 잡 안 대조 (D 의 sha256) 가 통과해 **정적 대조를 안 거친 D** 가 돈다.  외부 쓰기 둘이 필요 (도구 자신은 그 사이에 쓰지 않는다 — 읽어 확인).
- 고침: 정적 대조를 runnerck 앞으로, 또는 runnerck 가 박은 덱 sha256 = 영수증 첫 줄 · 셋째 줄인지 대조.

### PAI-07 (P3) — 기록 빈칸

- (a) `tool.txt` · 보고 · 시도 폴더에 정적 대조의 기준 본 덱 (`input_<C>.liggghts`) sha256 · 사본이 없다 (재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트 · lmp_mpi 만) — 나중에 어느 본 덱과 견줬는지 증명 못 함.
- (b) 체크포인트는 삽입 덱이 썼는데 (`write_restart …_20001.bin`) 도구는 본 덱의 `restart 50000 …settling_*.bin` 이름 꼴로 맞춘다 (20001 은 50000 의 배수가 아니다) — 삽입 덱 ↔ 본 덱 앞부분 대조 없음.  D0.7 리포 덱: 1–166 행 같음 (다름 = 167 행 이후) · G1 (step 20001 KE 1e-6) 이 원 로그와 묶는다.
- (c) lmp_mpi = 잡마다 기록만 · 시험 ↔ 본 대조 없음 · 본 잡 로그는 도구가 안 읽는다 (선언된 한계).
- 고침: `tool.txt` 에 본 덱 · (있으면) 삽입 덱 sha256 한 줄씩.

### PAI-08 (P3) — `-s` · `-r` 검사 없음

- `-x` · `-n` 은 시작 때 막는데 (`:1581–1582`) `-s` 는 `S=$L/$C.$SUF` (`:1858`) 로 그대로 · `cp -a $S $W` (`:1879`).  `-s ins1/../decoy` → `<루트>/decoy` 를 멈춘 폴더로 복사 · 시험 제출 (`logs/e2e_SUF.log` — 작업 폴더에 decoy 표지 파일 · 보고 `멈춘 폴더: kg50_d07_b50.ins1/../decoy`).  `-r` 도 따옴표 없이 쓴다.
- 고침: `-s` = `^[A-Za-z0-9_]+$` · `-r` = 공백 · 글로브 없는 절대 경로.

### PAI-09 (P3) — 하네스 '정상' 덱의 한계

- `res_good()` (`scripts/test_resume_ckpt.py:290–311`) 는 `fix ins_mix` ~ `PHASE 1` 사이를 통째로 뺀다 → `thermo_style custom step atoms ke cpu` · `thermo 1000` 도 빠진다.  restart 파일은 thermo 설정을 안 담는다 (LAMMPS read_restart 문서의 "다시 줘야 하는 것" 목록 · LIGGGHTS 3d5c00f 원문 · 실행으로는 확인 안 함 = **추정**) — 그렇다면 실제로는 기본 thermo (`Step Temp …`) 가 나와 G0 (`Step Atoms` 머리) 가 실패할 덱이다.  하네스는 가짜 mpirun 이 정해진 로그를 내서 양성으로 본다.  실제 dem_restart.py 는 그 줄들을 남긴다 (D2 r4).  이 보고의 D0.7 끝-끝은 dem_restart.py 꼴로 돌렸다.

## 2. 주장 대조 (다시 잼 · 2dc7f693)

| 주장 (출처) | 다시 잰 값 | 판정 |
|---|---|---|
| `433 PASS · 0 FAIL (기존 383 + VP 50)` · Python 3.11 · mawk (26e748af2 커밋) | 433 PASS · 0 FAIL · 217 초 · 383 = 216 + V 76 + RB 91 | 맞음 |
| (같은 시험을 3.8 에서는 주장 안 함) | Python 3.8.20 (하네스 + 도구 안 `python3`) 433 PASS · 0 FAIL · 179 초 | 더함 |
| `실제 kg50 본 덱 12 × (settling · after_settling) 24 쌍 = rc 0 24` (26e748af2) | 리포 본 덱 12 (v2 9 · v3 3) × {settling (하네스) · settling (dem_restart.py 꼴 재구성) · after_settling (하네스)} = 36 쌍 rc 0 36 | 맞음 (스크립트 · 로그는 커밋에 없음 → PAI-03) |
| `리뷰어 반례 덱 15 = 전부 rc 1` (26e748af2) | 덱이 리포에 없다 | 확인 불가 (PAI-03) |
| VP 시험 먼저: `45 개 = 7 PASS · 38 FAIL (대조군 6 + VP8)` (ce70f44e4) | 50 개 전부를 고치기 전 통합 도구 12bc95ce 로 = 7 PASS · 43 FAIL · 통과 7 = VP8 + 대조군 6 (VP2z 3z 4z 5z 7z 8z) | 맞음 (뒤에 더한 5 개도 고치기 전 실패) |
| VP 50 · RB 91 (지금 판) | `--only VP` 50 PASS · 0 FAIL (12 초) · `--only RB` 91 PASS · 0 FAIL (44 초) | 맞음 |
| `통합 12bc95ce → 2dc7f693` (26e748af2) | 이력 sha256: bf8cf21c6 `77c24237` → c419a7f92 `38e1eff5` → 07761cf54 `b24cc53a` → 48cfd2871 `12bc95ce` → 26e748af2 `2dc7f693` | 맞음 |
| F02 README `정적 대조 Python (첫 1033 줄) 손대지 않음 (d0dc0cf4)` | 곁가지 주장이라 이 이력에서 그 값은 안 나온다 (2dc7f693 의 첫 1033 줄 sha256 = `01b2a951` · F01 이 바꿨다).  같은 뜻을 이 이력에서: F02 커밋들은 정적 대조 heredoc (63–1422 행) 을 안 바꿨다 (59bdeb093 · b0fd6ec9f · ce70f44e4 모두 `85806a42…`) · F01 2 판은 셸 쪽 (첫 `PY` 행부터 끝) 을 안 바꿨다 (`dc3465ef…` 둘 다) | 뜻은 맞음 · 값은 곁가지 한정 |
| F01 README `Codex 사례 여섯 — 반례 넷 rc 1 · 기준 둘 rc 0` | Codex ZIP (e46bda9ec 반입) 43 사례 전부를 2dc7f693 `-C` 로: 반례 넷 rc 1 · accept 4 rc 0 · reject 31 rc 1 · "known parser mismatch" 둘 (NBSP · 이음 공백) 은 이제 rc 1 (닫힌 실패로 좋아짐) · "known bounded acceptance" 둘 (체크포인트 basename · 빈 대체 STL) rc 0 그대로 | 맞음 |
| Codex §5 `최신 cutter 로 다시 만든 D2 시험 = 수령 r4t 바이트 같음` | 2dc7f693 cutter → `aac7debc…` = 수령 r4t | 맞음 |
| F02 README §0-2 `-T 는 영수증 다시 대조 안 함 · 잡 안 대조 + G0 신원이 덮는다` | 코드 · 끝-끝과 같음 (`logs/e2e_T.log`) | 맞음 |
| (요청서 · 계획) `본 제출 = Codex GO 뒤 · -T 영수증 검토` | 도구가 본 호출을 `-T` 영수증에 묶지 않는다 | PAI-02 |
| 등록 허용 차이 `판 메시 file 이름 (그 파일이 작업 폴더에 있을 때)` | 절대 경로 · `../` 가 작업 폴더 밖 파일로 통과 | 거짓 → PAI-01 |
| `--compare-old 77c24237` (옛 판 정상 · 새 판 거부) | §2-1 | §2-1 |

### 2-1. `--compare-old 77c24237` (Codex 리뷰 핀의 도구 ↔ 2dc7f693 · 같은 433 장면)

(아래 값 = `logs/compare_old_77c24237.log`)

| 항목 | 값 |
|---|---|
| 지금 판 판정 | 433 PASS · 0 FAIL (263 초 · 장면마다 옛 판도 돌림) |
| 둘 다 정상인 장면 (시험 · G0–G3 통과 / `-C` 통과) | 53 — 예전 묶음 (K S D Q T N F C A P W) 에서 다름 **0** · 새 묶음에서 다름 **0** |
| 옛 판 정상 · 새 판 거부 | 91 = **V 53 · VP 38 뿐** (KG50R-F01 1·2 판 반례 — 의도한 거부) · 예전 묶음 0 |
| 새 판만 정상 | VP6a 등 (옛 판이 치환 전 이름으로 찾아 거짓 거부하던 꼴) |
| 그 밖 '다름' (판정 · 제출 같음 · 글만) | P 2 (bash 오류 줄 번호 · 작업 폴더 새 파일) · W 1 · G 1 · Y 5 (거부 장면의 문제 줄 수 · 글) · I 3 (승인 글의 도구 sha256) |

⇒ 지금 433 장면 안에서 옛 판이 받던 정상 장면을 새 판이 거부한 것은 없다 (실제 본 덱 회귀 = §2 의 36 쌍 · D2 · D0.7 쌍).

### 2-2. 변수 꼴 (D0.7 쌍 · 준비 구간 gravity fix 가 `${g}`)

| 꼴 | 결과 |
|---|---|
| equal 같음 · string 다시 정의 (본 덱 98.1 → 196.2 · 재개 덱 196.2) | rc 0 (같은 값 — 맞음) |
| getenv · index (첫 정의가 이김) · file · format · loop · world | 전부 rc 1 `다룰 수 없는 변수 꼴` |

(`logs/varstyles.log`)

## 3. 변이 (새 관문 하나씩 끄기 · `probes/mutate_spot.py` · `logs/mutation_spot.log`)

| 변이 | 묶음 | 끈 관문 | 결과 (그 묶음 PASS/FAIL) | 실패한 시험 |
|---|---|---|---|---|
| R1_keypos_off | VP | run_state 상태 표 키 자리 `$` | 잡힘 · 41/9 | VP1a–VP1h |
| R2_runevery_off | VP | mprefix_check run … every 명령 | 잡힘 · 45/5 | VP2a VP2b VP2c VP2e |
| R2_partition_off | VP | mprefix_check partition 명령 | 잡힘 · 49/1 | VP2d |
| R2_unsup_partition_off | VP | unsupported() partition 안 명령 | 잡힘 · 49/1 | VP2f |
| R3_ctrl_off | VP | deck_lines 제어 글자 거부 | 잡힘 · 47/3 | VP3a VP3e VP3f |
| R3_nonascii_off | VP | deck_lines 주석 밖 비 ASCII 거부 | 잡힘 · 48/2 | VP3d VP3g |
| R3_amp_space | VP | `&` 이음에 공백 하나 (옛 꼴) | 잡힘 · 48/2 | VP3c |
| R4_printfile_off | VP | print_file_reads 호출 | 잡힘 · 46/4 | VP4a VP4b VP4c |
| R5_flowwrite_off | VP | flow_before_write 호출 | 잡힘 · 44/6 | VP5a–VP5f |
| R6_seq_dollar_off | VP | seq_cmp 판 메시 file 이름 `$` | 잡힘 · 49/1 | VP6d |
| R6_state_marker_off | VP | state_cmp 펼친 file 이름 표지 | 잡힘 · 49/1 | VP6c |
| R7_expand_cap_off | VP | expand() 4096 자 상한 (두 곳) | 잡힘 · 49/1 | VP7 |
| R7_all_caps_off | VP | expand() + var_env() 상한 | 잡힘 · 47/3 | VP7 |
| R7_varenv_cap_off | VP | var_env() 상한 | 잡힘 · 49/1 | VP7 |
| F02_envlike_off | RB | runnerck 환경 줄 꼴 거부 | 잡힘 · 81/10 | RB32a–RB32j |
| F02_cd_realpath_off | RB | runnerck cd 실제 경로 = 작업 폴더 | 잡힘 · 90/1 | RB3 |
| F02_injob_check_off | RB | 러너 잡 안 sha256 대조 (덱 쪽 — `||`/`&&` 우선순위로 체크포인트 쪽은 남음) | 잡힘 · 86/5 | RBP1 RBP2 RB40 RB41 RB43 |
| F02_g0_identity_off | RB | G0 신원 관문 (GI=1) | 잡힘 · 87/4 | RB40 RB41 RB44 RB44b |
| F02_receipt_mis_off | RB | 영수증 파일 sha256 ↔ 메모리 | 잡힘 · 89/2 | RBR4 RBR5 |
| F02_receipt_c_off | RB | 본 제출 전 다섯 `sha256sum -c` | 잡힘 · 88/3 | RBR1 RBR2 RBR3 |
| F02_symlink_S_off | RB | 멈춘 폴더 링크 거부 | 잡힘 · 90/1 | RB48 |
| F02_error_identity_excl_off | RB | ERROR 셈에서 신원 줄 빼기 | 잡힘 · 90/1 | RB47 |

22 / 22 잡힘.  PAI-01 (판 메시 경로) · PAI-02 (`-T` 결속) · PAI-05 · PAI-06 · PAI-08 은 지킬 관문이 없어 변이 대상이 아니다.

## 4. 못 시험한 것

- 실제 ibb `-T` · SLURM · OpenMPI 56 · LIGGGHTS (G1 · G3 의 실제 값 · 환경 줄 출력이 줄 끝 없이 남아 신원 줄이 줄 머리가 아닌 경우 · `command mpirun` ↔ 사이트 mpirun 함수/별칭) — 하네스는 가짜다.
- 실제 ibb `dem_restart.py` (사본 없음) — D0.7 재개 덱 · 헬퍼 러너는 D2 선례에서 배운 변환으로 재구성 (D2 에서 바이트 같음 확인).  헬퍼가 import 하는 다른 파일 · 설정은 `-H` 밖.
- ibb `/home` ↔ `/lustre` 경로 (PAI-04) · ibb `python3` 판 · gawk (이 컨테이너에 없음 · 이번엔 mawk 만).
- 리뷰어 반례 덱 15 (리포에 없음) · F02 곁가지 도구 5f4ffb46 · e5a61181 (이력에 없음).
- LIGGGHTS 고정판 `input.cpp` 의 따옴표 · `$` 규칙 원문 (네트워크 금지 · 저자 주석의 행 번호를 믿지 않고, 영향 = D0.7 덱에 없는 꼴뿐).

## 5. 탐침 (`probes/`)

| 파일 | 하는 일 |
|---|---|
| `probes/make_d07_resume.py` | D2 선례에서 dem_restart.py 변환 T 를 배우고 (D2 바이트 같음 확인) D0.7 재개 덱 · 헬퍼 러너 재구성 |
| `probes/c_real.sh` | 받은 D2 쌍 · 재구성 D0.7 쌍 `-C` |
| `probes/cut_d2.sh` | 지금 cutter 로 D2 r4t 바이트 재현 · D0.7 r56t · 예산 |
| `probes/e2e_d07.py` | 리포 하네스 (가짜 sbatch 가 러너 실행) 로 D0.7 끝-끝: T · M · MX (PAI-01) · TM2 (PAI-02 · `PAI_NOCHANGE=1` 대조군) · SUF (PAI-08) |
| `probes/mesh_escape.sh` | PAI-01 `-C` 네 꼴 |
| `probes/varstyles.py` | 변수 꼴 아홉 |
| `probes/pairs24.py` | 실제 본 덱 12 × 세 꼴 `-C` |
| `probes/codex_cases.py` | Codex ZIP 43 사례 `-C` (풀어 둔 폴더를 자료로만) |
| `probes/shadow_import.sh` | PAI-05 |
| `probes/lineage.sh` | 커밋마다 도구 sha256 · 첫 1033 줄 · heredoc 끝 |
| `probes/mutate_spot.py` | 변이 22 |
| `probes/run_probes.sh` | 위를 한 번에 돌려 `logs/` 에 남김 |
