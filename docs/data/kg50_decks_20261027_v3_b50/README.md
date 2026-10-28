# 50kg/batch 4차년도 — SE 입도 비교 DEM 덱 v3 (50×50 · 10-27)

- 왜: D3 칸 판정 = **불합격** (수송 지표 차 > 문턱 5 % · 판정 기록 = `docs/data/kg50_d3_cell_verdict_20261027/`) → 등록 (`docs/data/kg50_decks_20261026_v2/README.md` §3) 대로 비교 덱 D0.7 · D1 · D2 = **50×50** (`--fallback50`) · 1저자 10-27 *"50 50으로 하자"*.
- 이 폴더 = 새 덱 셋 (D0.7 · D1 · D2 의 50×50).  본 비교의 D3 자리 = v2 `kg50_d3_b50_s1` (hit 칸 비교에서 압밀 끝 · 여기 다시 만들지 않았다 · 등록 §3 "본 비교 (D0.7 · D1 · D2 · D3 시드 1)" 그대로 · 새 결정 아님).  v2 의 40×40 비교 셋 (`kg50_d07_b40` · `kg50_d1_b40` · `kg50_d2_b40`) 은 쓰지 않는다.
- 다시 만들기: `python3 scripts/make_se_size_decks.py --preset kg50y4 --fallback50 --only kg50_d07_b50,kg50_d1_b50,kg50_d2_b50 --out <빈 폴더> --ibb-runner docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh --ntasks kg50_d07_b50:56,kg50_d2_b50:4` (같은 바이트 · `manifest.json` sha256 · 생성기 sha256 `00d16e07…`).

## 1. v2 → v3 바뀐 것

| 무엇 | 바뀐 것 |
|---|---|
| 영역 | 50×50 µm (판 꼭짓점 · 압력 면적 0.0025) · 시드 슬롯 9 · 10 · 11 (40×40 셋 = 0 · 1 · 2 — 다른 침대) |
| 덱 머리 주석 | 3 · 9 행에 기준 덱 파일 이름 · 태그를 쓰지 않는다 — 기준 덱 = sha256 전체 + 폴더 `docs/data/phase_a_6mah/` (경로 전체 = `manifest.json` `template`) · ⑦ = "기준 덱의 케이스 태그 (소문자 24 곳 · 대문자 2 곳) → 케이스명".  계기 = 10-27 ibb `dem_restart.py` 가 v2 덱을 *"다른 케이스명 혼입: ['real_4']"* 로 거부 (D0.7-40 재개 계획 없음 · 실행 줄엔 없음) |
| 생성기 | 머리 주석 고침 + `build` 가 쓰기 전 생성 파일 어느 줄에든 (주석 포함) 다른 케이스명이 있으면 멈춤 · selftest 118/118 |
| 그 밖 | 같음 — 고치기 전 생성기 (`e65e92b7b`) 로 같은 세 케이스를 만들면 덱 여섯의 3 · 9 행 (줄 전체 주석) 만 다르고 실행 줄 · 러너 다섯 · `manifest.json` 기록이 같다 (sha256 값만 다름) |

## 2. 계획 입자 수 · 삽입 검사 (덱 안 · 밖이면 `quit 1`)

| 케이스 | SE D50 | AM 계획 | SE 계획 | 합 | 바닥 (99 %) | AM 정수 구간 | SE 정수 구간 | 예상 면용량 |
|---|---|---|---|---|---|---|---|---|
| `kg50_d07_b50` | 0.7 µm | 1,481 | 486,810 | 488,291 | 483,408 | 1474–1488 | 484376–489244 | 6.499 |
| `kg50_d1_b50` | 1 µm | 1,481 | 166,976 | 168,457 | 166,772 | 1474–1488 | 166142–167810 | 6.499 |
| `kg50_d2_b50` | 2 µm | 1,481 | 20,872 | 22,353 | 22,129 | 1474–1488 | 20768–20976 | 6.499 |

- 셋 다 AM D6 · 85:15 wt% · 삽입 높이 317.7 µm (z 0.322700) = 고체 두께 101.98 µm · 바닥 = `count(all)` 이 이 수보다 작으면 멈춤 · AM · SE = 계획 ±0.5 % (ceil · floor).
- PS-01 (`maxattempt` int32): 모든 덱 3,000 · 가장 큰 `kg50_d07_b50` = 488,291 × 3,000 = **1,464,873,000** < 2³¹/1.3 = 1,651,910,497 (비 0.887 · ×1.3 = 1,904,334,900 < 2,147,483,647) · 이 수에서 허용 상한 3,383 · 넘으면 생성기가 덱을 내지 않는다.
- 상별 수는 MPI 랭크마다 흔들린다 (SELF-70) → 삽입은 NP 1.  D0.7-50 입자 = 40×40 의 1.56 배 — 삽입 런 (NP 1 · 23,001 step) ≈ 7 h (추정 · 40×40 실측 4 h 40 m 의 선형).

## 3. 발사 명령 (명령만 · 아무것도 띄우지 않았다 · 1저자 승인 뒤)

```bash
# WSL → ibb (주소 · 포트 = 1저자 · 리포에 적지 않는다) · 러너 cd = $HOME/dem_test/<case> · 제출 폴더에 logs/
cd ~/Yonghoon-DEM-DFT && git pull
scp -P <포트> -r docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50 docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50 <사용자>@<ibb>:~/dem_test/
# ibb — 삽입 (NP 1 · 삽입 + 정착 20,000 + 3,000 step → restart_settling_20001.bin)
cd ~/dem_test && mkdir -p logs && sbatch kg50_d07_b50/run_kg50_d07_b50_insert.sh && sbatch kg50_d2_b50/run_kg50_d2_b50_insert.sh
# 끝난 뒤 — 세 검사 줄 (INSERTED · AM · SE) · FATAL 없음 · LIGGGHTS 판 (KG50-15)
grep -hE "INSERTED|====== (AM|SE)|FATAL" ~/dem_test/kg50_d07_b50/log.liggghts ~/dem_test/kg50_d2_b50/log.liggghts
head -2 ~/dem_test/kg50_d07_b50/log.liggghts
# 재개 — 원 폴더를 옮기고 시험만 (-T · 2,000 step) → 보고 ~/dem_test/resume_r<NP>_*.md (G0–G3) · 계획 ~/dem_test/<case>/plan_r<NP>.txt
mv ~/dem_test/kg50_d07_b50 ~/dem_test/kg50_d07_b50.ins1
nohup bash ~/dem_test/scripts/resume_ckpt.sh -T -n 56 -s ins1 -r ~/dem_test kg50_d07_b50 > ~/dem_test/resume_d07_b50_T.log 2>&1 &
mv ~/dem_test/kg50_d2_b50 ~/dem_test/kg50_d2_b50.ins1
nohup bash ~/dem_test/scripts/resume_ckpt.sh -T -n 4 -s ins1 -r ~/dem_test kg50_d2_b50 > ~/dem_test/resume_d2_b50_T.log 2>&1 &
grep -E "^ +kg50_d(07|2)_b50 +(compress|after_settling|settling) " ~/dem_test/kg50_d07_b50/plan_r56.txt ~/dem_test/kg50_d2_b50/plan_r4.txt
# G0–G3 통과 확인 뒤 같은 두 명령을 -T 없이 (본 제출 · NP 56 · 4)

# WSL → hit · hit — D1-50 삽입 (NP 1) → 끝나면 1저자 hit_resume.sh 로 20 코어
scp -r docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50 <사용자>@<hit>:~/simulation/
cd $HOME/simulation/kg50_d1_b50 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d1_b50_insert.liggghts > log_kg50_d1_b50_ins.out 2>&1 < /dev/null &
grep -hE "INSERTED|====== (AM|SE)|FATAL" ~/simulation/kg50_d1_b50/log.liggghts
```

- ⛔ `run_kg50_d07_b50.sh` · `run_kg50_d2_b50.sh` (본 러너) 를 처음부터 직접 sbatch 하지 않는다 — 고코어 fresh 삽입은 기하적으로 불가능하다 (KG50-01) · 재개 도구가 쓰는 러너다.
- ★ 10-27 밤 — 재개 전에 ibb 도구 판부터: `sha256sum ~/dem_test/scripts/resume_ckpt.sh` = 리포 `scripts/resume_ckpt.sh` 의 sha256 (10-27 밤 판 = 첫 긴 run 1 step 고침 · `docs/resume_ckpt_procedure_20260927.md` 끝 절 · KG50-17) · 10-27 ibb 사본은 09-27 판 (`bf82948e…` · `-T` 없음) 이었다.
- 재개 시험 `-T` 의 화면에 `재개 덱 첫 긴 run 고침: [run 179999] → [run 180000]` 줄이 나오는 것이 정상이다 (dem_restart.py 의 settling 잔여가 1 step 짧은 꼴 · 정적 대조는 고친 뒤 처음부터 다시).
- 재개 시험 `-T` 뒤 `plan_r<NP>.txt` 에 계획 줄이 있는지부터 본다 — `dem_restart.py` 의 실제 이름 목록은 리포에 없다 (이 덱이 그 도구를 지나는지 = 미확인).
- 계획에 *"덱 검증 실패"* 가 나오면 같은 명령에 `-c` (작업 사본 덱의 줄 전체 주석만 빼기 · 원본 그대로 · `docs/resume_ckpt_procedure_20260927.md` 끝 절) — v3 덱은 주석에도 다른 케이스명이 없어 필요 없을 것으로 본다 (추정).  `-c` 를 쓰려면 ibb 사본 `~/dem_test/scripts/resume_ckpt.sh` 를 이 판으로 바꾼다 (sha256 이 바뀐다 · 재개 도구 Codex 재확인 대상).
- ibb QOS `cpu-60` = 사용자당 60 CPU — D0.7 56 + D2 4 = 60 (다른 ibb 잡이 돌면 대기).
- D0.7 압축 전 정착 끝 (after_settling) 에서 Q5 dt · 감쇠 대조 (KG50-04 · 결과 전 등록 뒤) — v2 README §4 와 같은 순서.
- 한계 = v2 README §5 와 같다 (언로딩 없음 · gen-1 프로토콜 · 단분산 SE · 본 비교 시드 하나 · 감쇠 γ/m 크기 의존).

## 4. Q5 dt · 감쇠 가지 — 도구 (등록 Q11 · 10-28 · §12 개정)

- 등록 = `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` (1저자 10-27 밤 비준 · Q1–Q12 · **§12 = 10-28 개정** — §12-1 · §12-3 = 1저자 결정 · §12-2 W2 = ⬜ 개정 초안 · 비준 전).  도구 둘 (커밋 = *"50kg Q5 시험 먼저: 가지 덱 생성기 · 판독기 selftest"* → *"50kg Q5 구현: 가지 덱 생성기 · 판독기"* · 10-28 *"50kg Q5 시험 먼저: W2 (§12-2 개정 초안) · D3 로컬 직렬 (§12-3) · NP · grid selftest"* → *"50kg Q5 구현: W2 덱 … · D3 로컬 직렬 러너 … · 판독기 NP · grid · 이탈 기록"*):
  - `scripts/kg50_q5_branches.py` — 본 덱 + 가지 + NP → `q5_<case>_<가지>/` (W2 = `q5w2_…` · 로컬 = 꼬리 `_wsl`) (가지 덱 · 러너 · 본 덱 사본 · W2 = 본 런 로그 사본 · `q5_manifest.json` · `SHA256SUMS`).  등록 §4 · §12-2 의 줄 바꿈만 허용 (그 밖 한 글자 = 거부 · 파일 0) · A · F · A3 · F3 = `resume_ckpt.sh -C` 문제 정확히 하나 (§8-1) · W2 A · F = 정확히 둘 (§12-2 (마)) · NP = Q5 (A · B · C 56 · F 28 · A3 · C3 1 · F3 2).
  - `scripts/kg50_q5_verdict.py` — 돈 가지 폴더 → T0 · O1 · O2 (+ R1–R6) → §7 판정 ①–④ · (a) · (b) · W1 (b) 합격 한정어.  덤프 · 로그 · manifest · 체크포인트 sha256 기록이 하나라도 빠지거나 어긋나면 판정 없음 (rc 2) · T0 실패 = 판정 불가 (기술) · manifest NP = Q5 · 로그 procs · `MPI processor grid` = NP · 로컬 직렬 가지 = 이탈로 기록 (§12-3) · W2 = §12-2 비준 판으로 만든 가지만.
- 읽기 둘 (자리 표시): §4-1 `read_restart <가지 폴더>/…` = 러너가 cd 하는 가지 폴더 기준 상대 경로 · §4-5 덤프 `<폴더>` = 본 덱 153 행이 만드는 `post_<case>/` (`shell mkdir` 줄을 더하지 않으려고).
- B 의 dt 줄 (43 행) 은 `read_restart` 앞이다 — LIGGGHTS 3d5c00f restart 머리에 dt 가 없고 units 가 같으면 재설정하지 않는다 (Codex 증거 사본 `docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_restart/upstream_src_read_restart.cpp` · 생성기 selftest ⓪b).  판독기가 B 로그의 `timestep 5e-07` 치환 줄로 다시 확인한다.
- `fix damp all viscous 0.5 scale 3 <s>` 를 ibb · 로컬 바이너리가 받는지 = 확인 전 (§4-3) — C · C3 첫 로그의 ERROR 0 · 끝까지 돎 (T0) 이 그 확인이다 (1저자 WSL 소스 3d5c00f2 의 `src/fix_viscous.cpp` 74 행에 `scale` · 코디네이터 전달 · 이 세션에서 재지 않음).
- ★ **순서 (1저자 10-28): §12-2 (W2 줄 목록) 비준 → 그 뒤에 W1 결과를 읽는다.**  W1 가지는 비준 전에도 돌려도 되지만 결과 (판독기 출력 · 덤프 · 로그 값) 는 비준 전에 열지 않는다.  비준 전 판으로 만든 W2 가지는 운영자 제출 줄이 막혀 있고 판독기가 거부한다 — 비준 뒤 생성기로 다시 만든다.
- D3 (§12-3 · 1저자 10-28): **A3 · C3 = 1저자 로컬 WSL 직렬 1 코어** (MPI 실행기 · MPI 빌드 없음 · 덱 = hit 덱 바이트 같음) · **F3 = hit NP 2 · D1-50 이 끝난 뒤** (로컬 F3 = 생성기가 거부).  D3 바닥 F3 ↔ A3 는 기계 · 바이너리도 달라 판독기가 이탈로 기록한다 (바닥이 커질 수 있다 = ② 판정 불가 쪽으로만).

```bash
# (가) WSL → ibb — D0.7 W1 가지 (아무것도 띄우지 않는다)
cd ~/Yonghoon-DEM-DFT && git pull
for X in B:56 C:56 F:28 A:56; do python3 scripts/kg50_q5_branches.py --case kg50_d07_b50 --branch ${X%%:*} --np ${X##*:} --out ~/q5_build; done
scp -P <포트> -r ~/q5_build/q5_kg50_d07_b50_{B,C,F,A} <사용자>@<ibb>:~/dem_test/
# ibb — 본 런 (kg50_d07_b50) 이 restart_after_settling.bin 을 쓴 뒤 멈춘 (scancel) 뒤에만 (§8-3 2 · Q6 (가)) · 가지마다 (X = B C F A 차례 · cpu-60)
X=B
cd ~/dem_test/q5_kg50_d07_b50_$X && sha256sum -c SHA256SUMS
mkdir -p ~/dem_test/q5_kg50_d07_b50_$X/restart_kg50_d07_b50 && cp ~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_after_settling.bin ~/dem_test/q5_kg50_d07_b50_$X/restart_kg50_d07_b50/
sha256sum ~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_after_settling.bin ~/dem_test/q5_kg50_d07_b50_$X/restart_kg50_d07_b50/restart_after_settling.bin > ~/dem_test/q5_kg50_d07_b50_$X/ckpt_sha256.txt && cat ~/dem_test/q5_kg50_d07_b50_$X/ckpt_sha256.txt
[ "$(wc -l < ~/dem_test/q5_kg50_d07_b50_$X/ckpt_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ~/dem_test/q5_kg50_d07_b50_$X/ckpt_sha256.txt | sort -u | wc -l)" = 1 ] && (cd ~/dem_test && mkdir -p logs && sbatch q5_kg50_d07_b50_$X/run_q5_kg50_d07_b50_$X.sh) || echo "⛔ 체크포인트 sha256 다름 · 없음 — 제출 안 함"

# (나) WSL 로컬 — D3 A3 · C3 (직렬 1 코어 · §12-3) · 폴더 = ~/q5_local/q5_kg50_d3_b50_s1_<X>_wsl (러너가 그 자리로 cd)
cd ~/Yonghoon-DEM-DFT && git pull
for X in A3 C3; do python3 scripts/kg50_q5_branches.py --case kg50_d3_b50_s1 --branch $X --np 1 --host wsl --out ~/q5_local; done
# D3 정착 끝 체크포인트 = hit 원본을 한 번 가져와 등록 Q1 sha256 과 대조 (hit 원본은 읽기만 · 다르면 멈춤)
mkdir -p ~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1 && [ -s ~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ] || scp <사용자>@<hit>:~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/
echo "1bf24069bb3876089adb6c7521d46c27f162de4e57ab6379d042913339607ea8  $HOME/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin" | sha256sum -c || echo "⛔ 등록 Q1 sha256 아님 — 멈춤"
# 바이너리 = $HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial (기본) · 다른 직렬 바이너리면 export LMP_SERIAL=<경로> · MPI 빌드 (ldd libmpi) = 러너가 거부
X=A3   # 그다음 X=C3 — 같은 바이너리 · 각 1 코어 (동시에 돌려도 결과는 같다 · 1저자 판단)
cd ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl && sha256sum -c SHA256SUMS
mkdir -p ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/restart_kg50_d3_b50_s1 && cp ~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/restart_kg50_d3_b50_s1/
sha256sum ~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/restart_kg50_d3_b50_s1/restart_after_settling.bin > ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/ckpt_sha256.txt && cat ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/ckpt_sha256.txt
[ "$(wc -l < ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/ckpt_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/ckpt_sha256.txt | sort -u | wc -l)" = 1 ] && bash ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/run_q5_kg50_d3_b50_s1_${X}_wsl.sh || echo "⛔ 체크포인트 sha256 다름 · 없음 — 실행 안 함"
cat ~/q5_local/q5_kg50_d3_b50_s1_${X}_wsl/q5_binary.txt   # 러너가 실행 직전에 쓴 바이너리 경로 · sha256 · 호스트 (판독기가 A3 ↔ C3 를 대조)

# (다) WSL → hit — D3 F3 (NP 2 · 등록 그대로 · D1-50 이 끝난 뒤 · 1저자 10-28)
python3 scripts/kg50_q5_branches.py --case kg50_d3_b50_s1 --branch F3 --np 2 --out ~/q5_build
scp -r ~/q5_build/q5_kg50_d3_b50_s1_F3 <사용자>@<hit>:~/simulation/
ls -l ~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin   # Q1 — 없으면 멈춤 (1저자 · (가) D3 를 정착 끝까지 다시 · NP 1 · 같은 덱)
X=F3
cd ~/simulation/q5_kg50_d3_b50_s1_$X && sha256sum -c SHA256SUMS
mkdir -p ~/simulation/q5_kg50_d3_b50_s1_$X/restart_kg50_d3_b50_s1 && cp ~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ~/simulation/q5_kg50_d3_b50_s1_$X/restart_kg50_d3_b50_s1/
sha256sum ~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin ~/simulation/q5_kg50_d3_b50_s1_$X/restart_kg50_d3_b50_s1/restart_after_settling.bin > ~/simulation/q5_kg50_d3_b50_s1_$X/ckpt_sha256.txt && cat ~/simulation/q5_kg50_d3_b50_s1_$X/ckpt_sha256.txt
[ "$(wc -l < ~/simulation/q5_kg50_d3_b50_s1_$X/ckpt_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ~/simulation/q5_kg50_d3_b50_s1_$X/ckpt_sha256.txt | sort -u | wc -l)" = 1 ] && bash ~/simulation/q5_kg50_d3_b50_s1_$X/run_q5_kg50_d3_b50_s1_$X.sh || echo "⛔ 체크포인트 sha256 다름 · 없음 — 실행 안 함"

# (라) 끝난 뒤 — 체크포인트 · 메시 덤프 빼고 모아 WSL 리포에서 판정 — ⛔ §12-2 비준 전에는 판독기를 돌리지 않는다 (1저자 10-28 순서)
tar czf ~/q5_w1_d07.tgz --exclude='*.bin' --exclude='mesh_*.stl' -C ~/dem_test q5_kg50_d07_b50_B q5_kg50_d07_b50_C q5_kg50_d07_b50_F q5_kg50_d07_b50_A
tar czf ~/q5_w1_d3_f3.tgz --exclude='*.bin' --exclude='mesh_*.stl' -C ~/simulation q5_kg50_d3_b50_s1_F3
python3 scripts/kg50_q5_verdict.py --branch A=<폴더>/q5_kg50_d07_b50_A --branch B=<폴더>/q5_kg50_d07_b50_B --branch C=<폴더>/q5_kg50_d07_b50_C --branch F=<폴더>/q5_kg50_d07_b50_F \
    --branch A3=$HOME/q5_local/q5_kg50_d3_b50_s1_A3_wsl --branch C3=$HOME/q5_local/q5_kg50_d3_b50_s1_C3_wsl --branch F3=<폴더>/q5_kg50_d3_b50_s1_F3 --json q5_w1.json

# (마) W2 — §12-2 비준 뒤에만 (생성기가 비준 판이면 제출 줄을 낸다)
# 본 런 로그로 시작 step 판단 (같은 규칙 · 사람이 고르지 않는다 · --w2-start 는 표준 라이브러리만이라 이 파일 하나로 ibb 에서도 돈다)
scp -P <포트> <사용자>@<ibb>:~/dem_test/kg50_d07_b50/log.liggghts ~/q5_build/main_log_kg50_d07_b50.liggghts
python3 scripts/kg50_q5_branches.py --w2-start ~/q5_build/main_log_kg50_d07_b50.liggghts   # rc 0 ready · 3 기다림 (접촉 전 · N 전) · 2 거부 (1저자)
# ready 이고 ibb 에 restart_kg50_d07_b50/restart_compress_<N>.bin 이 있으면 본 런을 멈춘다 (scancel · 1저자) → 그 로그로 다시 가져와 가지 넷
for X in B:56 C:56 F:28 A:56; do python3 scripts/kg50_q5_branches.py --case kg50_d07_b50 --branch ${X%%:*} --np ${X##*:} --window W2 --main-log ~/q5_build/main_log_kg50_d07_b50.liggghts --out ~/q5_build; done
scp -P <포트> -r ~/q5_build/q5w2_kg50_d07_b50_{B,C,F,A} <사용자>@<ibb>:~/dem_test/
# ibb — 가지마다 생성기 화면 줄 그대로 (X = B C F A 차례 · N = 화면의 시작 step)
X=B; N=<생성기 화면의 N>
cd ~/dem_test/q5w2_kg50_d07_b50_$X && sha256sum -c SHA256SUMS
mkdir -p ~/dem_test/q5w2_kg50_d07_b50_$X/restart_kg50_d07_b50 && cp ~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_$N.bin ~/dem_test/q5w2_kg50_d07_b50_$X/restart_kg50_d07_b50/
sha256sum ~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_$N.bin ~/dem_test/q5w2_kg50_d07_b50_$X/restart_kg50_d07_b50/restart_compress_$N.bin > ~/dem_test/q5w2_kg50_d07_b50_$X/ckpt_sha256.txt && cat ~/dem_test/q5w2_kg50_d07_b50_$X/ckpt_sha256.txt
cp ~/dem_test/kg50_d07_b50/post_kg50_d07_b50/mesh_$N.stl ~/dem_test/q5w2_kg50_d07_b50_$X/plate_kg50_d07_b50.stl
sha256sum ~/dem_test/kg50_d07_b50/post_kg50_d07_b50/mesh_$N.stl ~/dem_test/q5w2_kg50_d07_b50_$X/plate_kg50_d07_b50.stl > ~/dem_test/q5w2_kg50_d07_b50_$X/plate_sha256.txt && cat ~/dem_test/q5w2_kg50_d07_b50_$X/plate_sha256.txt
[ "$(wc -l < ~/dem_test/q5w2_kg50_d07_b50_$X/ckpt_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ~/dem_test/q5w2_kg50_d07_b50_$X/ckpt_sha256.txt | sort -u | wc -l)" = 1 ] && [ "$(wc -l < ~/dem_test/q5w2_kg50_d07_b50_$X/plate_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ~/dem_test/q5w2_kg50_d07_b50_$X/plate_sha256.txt | sort -u | wc -l)" = 1 ] && (cd ~/dem_test && mkdir -p logs && sbatch q5w2_kg50_d07_b50_$X/run_q5w2_kg50_d07_b50_$X.sh) || echo "⛔ 체크포인트 · 판 STL sha256 다름 · 없음 — 제출 안 함"
# 끝난 뒤 — W2 판정 (결정 O2 · O3) · W1 과 합치기 (창마다 · 나쁜 쪽)
python3 scripts/kg50_q5_verdict.py --branch A=<폴더>/q5w2_kg50_d07_b50_A --branch B=<폴더>/q5w2_kg50_d07_b50_B --branch C=<폴더>/q5w2_kg50_d07_b50_C --branch F=<폴더>/q5w2_kg50_d07_b50_F --json q5_w2.json
python3 scripts/kg50_q5_verdict.py --combine q5_w1.json q5_w2.json
```

- 각 생성기 실행이 같은 명령 (그 가지 이름 · 경로) 을 화면에 낸다 — 위는 같은 글자를 `$X` 로 묶은 것.  원 폴더 (`kg50_d07_b50.ins1` · `kg50_d07_b50` · hit `kg50_d3_b50_s1`) 에는 `cp` · `scp` 로 읽기만 한다.
- 시간 (§5 · 추정): ibb W1 가지 넷 10–20 h (차례로) · D3 가지 하나 1 h 안팎 (hit NP 1 원 런 기준 · 로컬 1 코어 시간은 첫 런으로) · W2 넷 15–31 h.  덤프 (Q12 · §12-2 (나)): D0.7 W1 atom ≈ 50 MB × 19 장 · contact 수백 MB × 9 장 · W2 atom ≈ 50 MB × 154 장 · contact 수백 MB × 19 장 · `dmp_atom` × 28 장 — ibb 할당량 확인.
- ⚠ W2 의 (b) 는 지금 꼴이면 늘 판정 불가 — §5 W2 표 = D0.7 만인데 §7 (b) · 판독기는 D3 도 요구한다 (등록 §12-2 질문 W2-6 · 1저자).
