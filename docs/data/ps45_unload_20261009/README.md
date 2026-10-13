# DEM 언로딩 키트 — ps45 다섯 침대 (등록 개정 2 · 시험 먼저) · ⛔ 본 R · 10:0 이완 연장 · 개발 / 생산 U = Codex (키트 증거 + 개정 2) 뒤

- 등록 (정본): `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG — §12 개정 1 · §13 개정 2) · 반영 계획 `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` (✅ 1저자 10-12 Q1–Q4 권고대로) ·
  Codex 판정문 `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` (CX1) · `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` (CX2).
- 이 README 가 **이름의 정본**이다 (REG §8-2 "이름은 가칭 · 키트 README 가 정본").
- 지금 할 수 있는 것 = **§1 작은 침대 이력 시험 (H0–H5) 만** — 본 키트 봉인과 따로 봉인 (`history_test/SHA256SUMS`) 해서 먼저 돌릴 수 있다.
  ⛔ 이 시험이 PASS 여도 본 R · 10:0 연장 · U 의 GO 가 아니다 (CX2 §0 · REG §13-6 — 키트 증거 → Codex 재검토 → 본 실행).
- 본 키트 (§2–§6) = 만들고 합성 · 모의 시험까지 (10-13).  ⛔ 실행 = 부록 초안 (권고 기본값) 1저자 비준 → Codex 키트 재검토 GO 뒤.
  부록 초안 `docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md` · 요청서 초안 `docs/reviews/codex_dem_unloading_kit_request_20261013.md`.
- 이 컨테이너에는 LIGGGHTS 가 없다 — 덱 문법은 소스 판독 (CX2 §5 · 노트 · 3d5c00f 원문) + 생성기 selftest 까지이고, 실제 바이너리는 §1 의 ibb 시험이 처음이다.

## 0. 이름 (정본)

| 무엇 | 이름 |
|---|---|
| 키트 폴더 | `docs/data/ps45_unload_20261009/` |
| 이력 시험 (H0–H5 · 따로 봉인) | `history_test/` — `make_history_decks.py` (생성기 · `--check` · `--selftest`) · `read_history.py` (읽는 쪽 · `--selftest`) · `run_history.sh` (러너) · `run_history_ibb.sbatch` (ibb 래퍼) · `history_params.json` (fixture 표) · 덱 여덟 `in.hist_*.liggghts` · `plate_hist.stl` · `SHA256SUMS` |
| ibb 작업 폴더 (이력 시험) | `~/ps45_unload_hist_20261013` (런 = 그 아래 `hist_<시각>/` · 보고 묶음 `hist_<시각>.report.tgz`) |
| SLURM job 이름 | `ulHist` (이력 시험) · `ulU` (본 키트 — 잡 하나에 sbatch 하나) |
| 본 키트 표 (하나뿐) | `unload_params.json` — 덱 생성기 · 러너 · 읽는 쪽이 여기서만 읽는다 |
| 덱 생성기 · 덱 | `make_unload_decks.py` (`--check` · `--selftest`) · `decks/<침대>/in.<종류>.liggghts` 64 (손으로 고치지 않는다) |
| 공용 · 판정 모듈 | `ul_lib.py` (덱 언어 · 덤프 · thermo) · `ul_s3.py` (K5 S3 총힘) · `ul_observers.py` (K6 σ_P · 표면 · S4 · ε · W_proxy · KE 기준) · `ul_gates.py` (K7 G0 · G1 · G2 · G2c · G3 · S0′) · `ul_reader.py` (K4 판독 · 선택 · 관문 · 복원 판정) |
| 러너 · 래퍼 · 모의 시험 | `run_unload.sh` · `run_unload_ibb.sbatch` · `ul_runner_test.py` (가짜 mpirun · lmp) |
| 봉인 · 활성 규칙 | `seal_kit.py` · `SHA256SUMS` (76 파일) · `active_rules.json` (규칙 12 · 폐기 규칙 0 건) |
| ibb 작업 폴더 (본 키트) | `~/ps45_unload_20261009/` — `<침대>/in/` (원 파일 여섯) · `<침대>/<잡>/` (런 폴더) · `kit_<시각>_<침대>_<잡>_XXXX/` (러너 kit 사본) · `logs/` (SLURM 출력) |
| 잡 (`run_unload.sh <침대> <잡>`) | `RJ` (복원 시험 — 7:3 은 Ut0 먼저) · `EXT` · `RJ2` (10:0) · `UB` · `UT` · `UC` · `UVa` · `UVb` · `UT3` · `UTc` · `G_UB` · `G_UVa` · `G_UVb` · `G_UT3` |
| 덱 종류 | `R` · `UNread` · `UK` · `UC` · `U_UB` · `U_UVa` · `U_UVb` · `U_UT3` · `G_<팔>` · (7:3) `UT` · `Ut0` · (10:0) `EXT` · `EXT2` |
| 판정 JSON · 파일 | `<침대>/RJ/g0.json` · `restore_verdict.json` · `<침대>/ul_base.in` (KE 기준 · S2) · `<침대>/<팔>/arm_verdict.json` · `<루트>/ps_7_3_r45/selection.json` · `<루트>/ps_10_0_r45/s0_decision.json` · `report.json` |
| 런 폴더 기록 (덱이 쓴다) | `ul_windows.csv` · `ul_steps.csv` · `ul_events.csv` (머리 = 표 records) · `ul_summary.txt` · `dump/` (창 끝 atom · wall · contact · mesh) · `restart/` (단 끝 `restart_unload_<step>.bin` + `state_unload_<step>.in` · `restart_RM_*` · `state_RM_*`) |
| 런 폴더 기록 (러너가 쓴다) | `screen.txt` (이어 돌림 `screen_a2.txt`) · `log_*.liggghts` · `deck.liggghts` · `deck.txt` · `run_manifest.txt` · `run_check.txt` · `<잡>.report.tgz` |

## 1. 작은 침대 이력 시험 (H0–H5) — 먼저 · 1저자 ibb · 결과 0 건

**왜** (REG §12-1 ③ · §13-6 ③ · CX2 §5 · 계획 §2 마지막 줄): 복원 관문의 관측자 (primitive 바닥 `history_zwall_bot` · mesh 판 `wall/gran/local` · 입자쌍) 가
**알려진 이력을 실제로 보는지** · **지워진 이력과 가를 수 있는지** 를 작은 침대에서 먼저 확인한다.  생산 S0 에는 과거 이력 열이 없으므로 (CX2 §5-4)
관측자의 판별력은 이 시험이 증거다.

### 1-1. fixture (`history_test/history_params.json` · 생성기가 자리 계산 · 산술 검사)

- 입자 20 · **적분하지 않는다** (운동학 fixture — 위치 · 속도는 명령으로만 바뀐다).  모델 머리 (재료 m1–m9 · pair · 바닥 primitive 벽 · 판 메시 벽 · 중력 9.81 · 감쇠 1.0e-5 · `fix_modify zwall_top energy yes`)
  = r8 원 덱 글자 그대로 (리포 tgz 멤버 sha256 `097658aa…` · 숫자를 다시 적지 않는다) · 머리 fix 순서 = 원 PHASE 4 (zwall_bot → integr → gravi → top_mesh → zwall_top → damp).
- 집합: B 넷 (바닥 접촉 · AM_P · AM_S · SE 포화 · SE 비포화) · T 넷 (판 접촉 · 같은 네 종) · 쌍 다섯 (AM_P–AM_P · AM_P–SE · SE–SE · AM_S–SE · AM_P–AM_S · 셋은 NP 분할면을 걸친다) · Z 둘 (접촉 없음).
- 만드는 법: ① 설계 deltaMax 겹침 자리에서 run 10 (setup 에서 history[0] = max(0, δ)) ② `set atom` 으로 부분 제하 (현재 δ < deltaMax) ③ 접선 속도 (법선에 수직) 로 run 1000 → shear += v_t·dt
  ④ 속도 0 · run 990 → 마지막 step 2000 의 in-run 덤프 = **봉인할 기대값** · write_dump 묶음 · `write_restart fixture.bin`.
- 생성기 산술 검사 (selftest ③): 의도한 접촉만 (바닥 4 · 판 4 · 쌍 5) · 의도 밖 이웃 0 (setup 분리 소거 경로 회피) · 판 대각 이음매 · 주기 경계 밖 · 모든 sentinel 이 압축 가지 (이력 식 · 덱 m6 · m8) ·
  접선 ≤ Coulomb 한도의 50 % · 접선 ⊥ 법선 · 포화 · 비포화 둘 다.

### 1-2. 단계 (한 job · `#SBATCH -n 6` ↔ `mpirun --oversubscribe --bind-to none -np 6` · H2 만 `-np 4`)

| 단계 | 덱 | NP | 무엇 | 행 |
|---|---|---|---|---|
| P | `in.hist_producer` | 6 | fixture 생산 · 끝 덤프 · `fixture.bin` · 자동 restart 1500 (run 끝 자동 쓰기 확인) | H0 · 기대값 |
| C6 | `in.hist_consumer` | 6 | 별도 프로세스 재개 — PRE_SETUP (write_dump · primitive 배열 그대로) · POST_SETUP (run 0 · mesh · pair local) | H1 |
| C4 | 같은 소비자 | **4** | NP 바꿈 재개 (행 순서 무시 · pair 무순서 키 + 방향 바뀐 shear 부호 정규화) | H2 |
| Ebot → Cbot | `in.hist_erase_bot` → 소비자 | 6 | 진단 사본: run 0 → undump · uncompute → `unfix zwall_bot` → 진단 restart → 새 프로세스 | H3 |
| Etop → Ctop | `in.hist_erase_top` → 소비자 | 6 | 같은 꼴 · `unfix zwall_top` (top_mesh 기하는 그대로) | H4 |
| Enone → Cnone | `in.hist_erase_none` → 소비자 | 6 | 양성 대조 — 같은 직렬화 횟수 · unfix 없음 | H3 · H4 대조 |
| BAD | `in.hist_badid` | 6 | 잘못된 내부 ID (`history_zwallbot`) — ERROR 가 나야 한다 (rc ≠ 0 이 기대값) | H5 |
| SYN | `in.hist_syntax_probe` | 6 | 본 키트 덱 문법 미리 지나가기 (read_restart 뒤 dt 5e-7 · erotate/sphere · ave/time · 부호 있는 Ps · 영역 개수 판 접촉 ↔ 벽 local 덤프 · move/mesh +z · mesh 덤프 · 명시 write_restart) + **판 접촉 법선력 부호** (입자가 받는 fn_z · 압축 상태) | 정보 (판정 밖) |
| PZ → CZ | `in.hist_producer_zero` → 소비자 | 6 | 0 뿐 fixture (모든 겹침 −1e-4) | H5 |

### 1-3. 판정 (읽는 쪽 `read_history.py` · 결과 전 고정 · CX2 §5-2 표 그대로)

| 행 | PASS 조건 | 아니면 |
|---|---|---|
| H0 문법 | 단계마다 rc 0 · 배너 LIGGGHTS-PUBLIC 3.8.0 · 3d5c00f · ERROR 0 · `Loop time … on N procs` 의 N = 그 단계 NP · 덤프 머리 · 열 이름 · 행 수 · 소비자에 내부 이력 fix 다섯의 restart reset 로그 (global · per-atom) · 생산자 write_dump 묶음 = in-run 덤프 | TECH (성공했다고 값 보존까지 통과시키지 않는다) |
| H1 · H2 | 원자 상태 · primitive PRE_SETUP = 생산자 끝 (글자 → float 정확히) · primitive · mesh · pair POST_SETUP = 생산자 끝 (상대 1e-12 · 절대 1e-18 덱 m) · 키 집합 같음 · 다른 값 중복 키 0 | FAIL (값) · TECH (열 · 키 · 비유한) · **INCONCLUSIVE (그 종류에 sentinel 0)** |
| H3 바닥 소거 | Cbot PRE 바닥 이력 전부 0 · POST shear 0 · deltaMax = 현재 겹침 (다시 찰 수 있다 — **"setup 뒤 4 열 0" 을 기대하지 않는다**) · sentinel 전부 deltaMax 감소 · 판 · 쌍 = 생산자 · 양성 대조 PASS · 소거 전 관측 = 생산자 · Cbot 에 `history_zwall_bot` reset 로그 없음 | FAIL · INCONCLUSIVE · TECH |
| H4 판 소거 | 같은 꼴 (mesh) · 바닥 PRE · POST = 생산자 · Ctop 에 `tracker_top_mesh` reset 로그 없음 | 같음 |
| H5 | 잘못된 ID → **TECH** (rc ≠ 0 · fix ID ERROR) 로 · 0 뿐 → **INCONCLUSIVE** 로 (0/0 PASS 아님) 분류됨 | FAIL (잘못된 ID 를 받아들임 · 0 뿐을 PASS 로) |

- sentinel = 생산자 끝에서 저장 deltaMax − 현재 겹침 ≥ 1e-9 이고 \|shear\| ≥ 1e-9 (덱 m) 인 접촉 (CX2 §5-2 비퇴화 조건).  설계상 primitive 4 · mesh 4 · pair 5.
- 정보 (판정 밖): ⓐ **run 끝 자동 restart** — 생산자 run 끝 (10 · 1010 · 2000 · 1500 의 배수 아님) 에 `auto_*.bin` 이 생기는가 (CX2 §6 — 10:0 연장 끝 3,660,000 은 50,000 배수가 아니다 · 본 키트 연장 덱은 어느 쪽이든 끝에서 **명시 write_restart** 하고 러너가 파일을 확인한다)
  ⓑ **총힘 출력 시점** — 접촉 없는 Z 입자의 덤프 fz = −m g · fx = fy = 0 (덤프 f 가 중력까지 더한 총힘 = S3 함수 입력 · K5) ⓒ SYN 문법
  ⓓ **판 접촉 법선력 부호** `plate_fn_sign` — 압축 중인 판 접촉에서 입자가 받는 fn_z 가 모두 음수면 −1 · 모두 양수면 +1 · 섞이면 SYN FAIL.  본 키트 상쇄 (TENSION) 판별이 이 약속을 쓴다 —
  결과가 표의 `plate_fn_compressive_sign` 과 다르면 표를 고친다 (결과 0 건 상태 · 판정 전).
- 결과 전 기대: H0–H5 PASS · ⓑ PASS · SYN = 판 접촉 4 → 3 (T4 가 1e-5 들어 올림에서 떨어진다) · ⓓ −1 (판이 위에서 누르면 입자가 받는 힘은 −z — 내 추정 · 미확인) · ⓐ 미리 정하지 않는다.  다르면 그대로 보고한다 — 덱을 손으로 고치지 않는다 (생성기 → 새 SHA256SUMS → 다시).

### 1-4. ibb 명령 (1저자 · 꺾쇠 자리표시 = 접속 정보뿐 · 나머지는 그대로 붙여 넣는다)

```bash
# ① 이 커밋의 새 작업 트리 (커밋마다 새 폴더 · 이미 있으면 다시 체크아웃하지 않는다)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/unload_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
H=$W/docs/data/ps45_unload_20261009/history_test
conda activate myenv && python3 -I $H/make_history_decks.py --check && python3 -I $H/read_history.py --selftest | tail -1   # "✓ check … 14 파일" · "selftest: PASS (0 실패)"
# ② 작업 폴더 · 제출 전 사전 점검 (로그인 노드 · 런 없음 · LMP = /lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi · sha256 = 등록 §11-1 ⓖ 빌드여야)
R=$HOME/ps45_unload_hist_20261013 && mkdir -p $R/logs
bash $H/run_history_ibb.sbatch $H                       # 끝 줄 "✓ 사전 점검만 — 통과" 를 본 뒤 ③
# ③ 제출 (작업 폴더에서 — logs/ 는 제출 폴더 기준) · 다른 job 은 끄지 않는다 · cpu-60 이 차 있으면 PD 로 기다리다 저절로 시작
cd $R && J=$(sbatch --parsable $H/run_history_ibb.sbatch $H) && echo "job $J"
# ④ 진행 · 끝 (수 분)
squeue -u $USER
tail -5 $(ls -t $R/logs/ulHist_*.out | head -1)
cat $(ls -dt $R/hist_*/ | head -1)history_verdict.txt
sha256sum $(ls -t $R/hist_*.report.tgz | head -1)
```

**보낼 것**: `hist_<시각>.report.tgz` (단계마다 화면 · 로그 · 덤프 · 작은 restart · 판정 JSON · kit SHA256SUMS — 입자 20 이라 작다) + sha256 + `logs/ulHist_<job>.out`.
WSL 로 가져오는 꼴 (접속 정보는 자리표시): `scp -P <port> <user>@<ibb-host>:~/ps45_unload_hist_20261013/hist_<시각>.report.tgz ~/`

- rc 0 = H0–H5 전부 기대대로 · rc 2 = 하나라도 아님 (화면 `HISTORY_VERDICT …` 줄 · 행마다 사유).  H0 가 TECH 면 대개 문법 (바이너리) 문제다 — 화면 그대로 보낸다.
- `bash $H/run_history_ibb.sbatch $H` 가 LMP sha256 불일치로 멈추면 다른 바이너리다 — 등록 빌드를 찾는다 (이탈로 진행하려면 `ALLOW_OTHER_LMP=1` · run_manifest 에 남는다 · 1저자 결정).

## 2. 덱 (K2 · `make_unload_decks.py`) — 결과 0 건 · 실행은 Codex GO 뒤

| 종류 | 무엇 | 런 |
|---|---|---|
| `R` | 복원 시험 (S0 · REG §3-2 · §12-1): PRE_SETUP `write_dump` (바닥 primitive 이력 그대로) → `run 0` (G1 setup 줄 · G2 원 형식 atom · G2c 원 형식 쌍 26 열 · 판 mesh md5 · mesh 벽 이력 · 총힘) → `run 2000` (G3) → R_END 관측 → 보조 소거 (uncompute → unfix 두 벽 → `un_diag.bin`) | RJ · RJ2 |
| `UNread` | 보조 소거 진단 restart 를 새 프로세스로 · 같은 머리 · PRE · POST (진단 전용 — S0 복원 증명 아님) | RJ · RJ2 |
| `UK` | 회전 KE 기준 — S0 무이동 3 창 (choice C4) | RJ · RJ2 |
| `UC` | 무이동 50,000 step × dt₀/dt (판 압력 표류 · 잡음 · KE) | UC |
| `U_UB` · `U_UVa` · `U_UVb` · `U_UT3` | 언로딩 상태 기계 · 전체 멈춤 규칙 (튜플 t1 · t2 · t4 · t3) | 팔 잡 · UTc (U_UT3) |
| `UT` (7:3) | dt₀/2 · 첫 교차 + 확인 두 단 → R_M restart + 상태 → 멈춤 (`RM_STOP` · §13-5 ③) | UT |
| `Ut0` (7:3) | 문법 (판정 자료 아님) — 표 `ut0` (창 100 step · A 400 · B 100 · P_meas 1 덱 MPa · 분리 문턱 크게) → 머리 · k = 0 · A 한 단 · 교차 · 확인 두 단 · R_M · 분리 · 분리 뒤 · 끝을 한 번씩 | RJ (7:3 첫 단계) |
| `G_<팔>` | 중력 팔 — 그 팔의 R_M (restart + 상태) → `run 0` (G1 · G2 · G2c) → `fix gravi … 9.81e-06` 제자리 교체 → 유지 (4–12 창) → 정상 · P̄ > P_meas 면 B 단 교차 · 아니면 `NO_BRACKET` (재압축 없음) → 분리 → 분리 뒤 4 창 | G_ 잡 |
| `EXT` · `EXT2` (10:0) | 3,600,000 → `run 60000` (restart 50,000 = 3,650,000 · 끝 3,660,000 명시 `write_restart`) · 3,660,000 → `run 50000` (3,700,000 · 끝 3,710,000 명시) · 원 덱 출력 꼴 | EXT |

- **모델 머리** = r8 원 덱 글자 (리포 tgz sha256 `097658aa…` · 재료 m1–m9 · pair · 바닥 · 판 · 중력 9.81 · 감쇠 1.0e-5 · `fix_modify zwall_top energy yes` · fix 순서 = 원 PHASE 4) — 판 STL 경로만 `${plate_stl}` (메시 자료는 restart 에서).  G0 = 원 r8 (0:10 · 3:7 · 5:5 · 7:3 꼴) · r2 (10:0 꼴) 와 비교해 PASS (GD5 · ibb 에서는 러너가 그 침대의 진짜 원 마지막 조각 덱으로 다시 — `<루트>/<침대>/RJ/g0.json`).
- **숫자는 표에서만** — 덱의 숫자 낱말은 표 · r8 원 글자 · 구조 상수 (0 · 1 · 2 · 3 · 4 · −1 · 0.0025 · 1000000 …) 중 하나여야 한다 (GD4 표 밖 상수 lint).
- **물리 창** (§13-4 · 생성된 덱에서 다시 계산 = GD6 · 판독기 R9):

  | 팔 | dt | v (덱 m/s) | 창 W | Δz_A · Δz_B (step) | k = 0 | 단 유지 | ave/time | thermo |
  |---|---|---|---|---|---|---|---|---|
  | UB | 1e-6 | 0.01 | 5,000 | 20,000 · 5,000 | 3–12 창 | 4–12 창 | 100 × 50 | 500 |
  | UVa | 1e-6 | 0.005 | 5,000 | 40,000 · 10,000 | 3–24 | 8–24 | 100 × 50 | 500 |
  | UVb | 5e-7 | 0.005 | 10,000 | 80,000 · 20,000 | 3–24 | 8–24 | 200 × 50 | 1,000 |
  | UT · UT3 | 5e-7 | 0.01 | 10,000 | 40,000 · 10,000 | 3–12 | 4–12 | 200 × 50 | 1,000 |
  | UC | 1e-6 | 0 | 5,000 | — | 50,000 step = 10 창 | | 100 × 50 | 500 |

  창 물리 시간 = 0.005 덱 s (모든 팔) · 분리 선언 2 창 · 분리 뒤 4 창 · 중력 팔 유지 4–12 창 (UV × 2 적용 범위 = choice C10).
- **상태 기계** (단계 `ul_phase`: 4 HOLD0 · 0 SEARCH · 1 CONFIRM · 2 SEPARATE · 3 POST): 창 (`run W`) 마다 Ps · KE (ave/time 창 평균) · 기하 판 접촉 수 · 원자 · 새어 나감 → S1 (|ΔP̄| ≤ max(0.5 % · |P̄|, 0.05 P_meas)) ∧ S2 (KE ≤ 10 · KE_base) → 두 창 연속 + 최소 창 = 정상 · 최대 = UNSTEADY (k = 0 이면 TECH) → 단 끝 = P̄ (마지막 두 창 평균) · 교차 (P̄ ≤ P_meas) · B 전환 (P̄ ≤ 3 P_meas 다음 단부터) · 확인 두 단 → R_M (`restart_RM_*` + `state_RM_*`) → 분리 (기하 접촉 0 두 창 · 둘째 창 끝 선언) → 분리 뒤 4 창 (재접촉 = SEPARATE 로 되돌림) → 끝.  들어 올림 상한 16 µm (choice C11) · 가드 (원자 잃음 > 50 · 새어 나감 > 100 · 병진 KE > 1.7e-3 J) = restart + 요약 · 멈춤.
- **덱 언어 규칙** (selftest 가 지킨다): 상태 파일은 늘 **맨 바깥** `include ${ul_state}` (3d5c00f input.cpp 845 — if 안 include = ERROR · 처음이면 러너가 빈 파일) · run 뒤 읽는 값은 다음 줄에서 즉시 치환으로 얼린다 (⑭b) · `write_restart` 뒤 `ke` · compute 를 run 전에 읽지 않는다 · `run 0` 뒤 판 힘을 읽지 않는다 (⑭a) · if 조건은 숫자 · 비교뿐 · local compute 는 read_restart 뒤 첫 run 전에 정의 (compute_pair_gran_local.cpp 126) · 창 끝 덤프 = `dump_modify … every v_ul_dnext` (이동 중 없음 · setup 덤프 없음).
- **기록 머리** = 표 `records` (창 19 열 · 단 15 열 · 사건 6 열) · thermo 머리 = `Step Atoms KinEng ul_erot ul_Ps pressMPa CPU` (GD13 · LIGGGHTS c_ · v_ 열 이름 = ID 앞 8 글자).
- **벽 local 열** = id (mesh · 삼각형 · 입자) → force_normal (입자가 받는 법선력 3) → (R 만) history 4 (compute_pair_gran_local.cpp add_wall_2 순서 — 키워드 순서와 무관).  법선력 = (f·n̂) n̂ = n̂ 부호와 무관한 입자에 걸린 힘의 법선 성분 → 판이 누르면 fn_z < 0 (표 `plate_fn_compressive_sign` −1 · 이력 시험 SYN ⓓ 가 잰다).

## 3. 러너 · ibb 명령 (⛔ 1저자 비준 → Codex 키트 재검토 GO 뒤 · 꺾쇠 자리표시 = 접속 정보 · 고를 잡뿐)

- `run_unload.sh <침대> <잡>` 이 지키는 것: kit 사본 (SHA256SUMS 목록 그대로) · LMP sha256 = 표 (`ALLOW_OTHER_LMP=1` = 이탈 기록) · in/ 원 파일 sha256 = 표 · **관문** (`ul_reader.py gate` — 거부면 런 없음) ·
  `"$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP"` (기본 `--oversubscribe --bind-to none` · NP 6) · 화면의 `Loop time … on N procs` 의 N = NP · `ERROR` · `UL_ABORT` 없음 · 런 뒤 읽는 쪽 · 보고 묶음 + sha256.
- 순서 (REG §13-5 ② · §13-6): 침대마다 원 파일 → `RJ` (복원 판정 RESTORED 여야 다음) → **7:3** `UB` · `UT` · `UC` (따로따로 제출 · 서로 독립) → 선택 판독 → 관문이 허락하는 **UV 하나** (`UVa` 또는 `UVb`) → 선택 (튜플) → (t3 면) `UTc` → `G_<최종 팔>` →
  **나머지 넷** = `RJ` → 최종 튜플의 팔 하나 → `G_<그 팔>` · **10:0** = `RJ` (3,600,000) → `EXT` (→ S0′) → `RJ2` (S0′) → 최종 팔 → `G_`.
- 이어 돌림 (기계 실패 · 한 번): `RESUME=1` — 마지막 `restart_unload_<step>.bin` + 짝 `state_unload_<step>.in` 에서 같은 덱 (화면 `screen_a2.txt`) · 두 번째 = 거부.

```bash
# ① 이 커밋의 새 작업 트리 · 봉인 확인 (커밋마다 새 폴더)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/unload_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
K=$W/docs/data/ps45_unload_20261009
conda activate myenv && python3 -I $K/make_unload_decks.py --check && python3 -I $K/seal_kit.py --check
# ② 원 파일 여섯 (침대마다 한 번 · 표에서 만든 명령을 보고 붙여 넣는다 · cp -n = 있으면 덮지 않는다) → 대조
python3 -I $K/ul_reader.py copycmd ps_7_3_r45
U=$HOME/ps45_unload_20261009 && mkdir -p $U/logs && python3 -I $K/ul_reader.py inputs $U ps_7_3_r45
# ③ 7:3 복원 시험 (Ut0 → G0 → R → UN → UK) — 이력 시험 판정 JSON 을 넘긴다 (없으면 복원 판정 UNCONFIRMED)
HV=$(ls -dt ~/ps45_unload_hist_20261013/hist_*/ | head -1)history_verdict.json
cd $U && bash $K/run_unload_ibb.sbatch $K ps_7_3_r45 RJ                                    # 사전 점검만 (끝 줄 "통과")
cd $U && sbatch --export=ALL,HIST_VERDICT=$HV $K/run_unload_ibb.sbatch $K ps_7_3_r45 RJ
head -3 $U/ps_7_3_r45/RJ/restore_verdict.json
# ④ 7:3 개발 팔 — 한 줄에 하나씩 (서로 독립)
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UB
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UT
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UC
# ⑤ UB · UT 끝난 뒤 — 선택 판독 · 관문이 ALLOW 하는 UV 하나만 낸다
python3 -I $K/ul_reader.py select $U
python3 -I $K/ul_reader.py gate $U ps_7_3_r45 UVa
python3 -I $K/ul_reader.py gate $U ps_7_3_r45 UVb
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <UVa 또는 UVb — 위에서 ALLOW 한 것>
# ⑥ 튜플 (selection.json) → t3 면 UTc · 그다음 중력 팔 (관문이 고른 팔만 ALLOW)
python3 -I $K/ul_reader.py select $U
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <UTc — t3 일 때만>
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <G_UB · G_UVa · G_UVb · G_UT3 중 관문이 ALLOW 한 것>
# ⑦ 나머지 침대 (원 파일 · RJ 뒤 최종 팔 · G_) · 10:0 = RJ → EXT → RJ2 → 최종 팔 → G_
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_10_0_r45 EXT
# 이어 돌림 (기계 실패 한 번)
cd $U && sbatch --export=ALL,RESUME=1 $K/run_unload_ibb.sbatch $K <침대> <팔>
# 끝난 잡마다 보낼 것 (꺾쇠 = 접속 정보)
sha256sum $U/<침대>/<잡>.report.tgz
scp -P <port> <user>@<ibb-host>:~/ps45_unload_20261009/<침대>/<잡>.report.tgz ~/
```

- 보고 묶음 = 런 폴더에서 큰 덤프 (원자 · 쌍 · obs · G2 원자 / 쌍 · post) 와 restart 를 뺀 것 (기록 CSV · 요약 · 화면 · 로그 · 벽 · mesh 덤프 · 판정 JSON · manifest · run_check).  큰 파일은 ibb 에 둔다.
- 디스크 어림 (§13-3 Q4 (가) 매 창 끝): 창마다 원자 ≈ 35 MB + 쌍 ≈ 175 MB → 팔 하나 ≈ 150–200 창 ≈ 30–40 GB · 단 끝 restart 81 MB × 단 수 · 7:3 개발 팔 넷 + UTc · G ≈ 200 GB 안팎 (/lustre 남음 148 T · quota 없음 — 1 차 점검 ⓖ).

## 4. 읽는 쪽 (K4 · `ul_reader.py`) — 판정 규칙 (등록 §12 · §13 · 권고 기본값 = 부록 초안)

| 판정 | 규칙 |
|---|---|
| 창 접촉 상태 | 창 끝 벽 local 덤프: 접촉 ≥ 1 · 창 평균 P > 0 = CONTACT · ≥ 1 · P ≤ 0 = TENSION · 0 = ZERO · 덤프 없음 · 깨짐 = OBS_MISSING (0 으로 세지 않는다) |
| 분리 | 연속 두 ZERO 창의 둘째 창 끝 · 그 창부터 분리 뒤 창 · 재접촉 = 계수 · 분리 뒤 창 · 표면 관측 초기화 · OBS_MISSING = 연속을 끊는다 |
| 끝점 유효 | 덱 정상 (S1 ∧ S2 두 창) ∧ S3 PASS (단 끝 원자 + 쌍 덤프 · K5) ∧ P̄ · 높이 유한 ∧ 판 접촉 (CONTACT · TENSION) ∧ (k*) NOISE_FLOOR 아님 (σ_P = k* 마지막 두 창 thermo 정규 줄 `ul_Ps` · ddof 1 · 최소 10) |
| 교차 · 괄호 | P̄ − P_meas 부호 바뀜 (> ↔ ≤) · 첫 교차 = P 두 점 선형 보간 (점 추정) + 실제 괄호 [h_lo, h_hi] · A 단 교차 = A 괄호 그대로 · 비단조 = 모든 교차 괄호의 합집합 + 표지 (b 판정 없음) |
| 상태 두 축 | `primary_status` OK · NOISE_FLOOR · LOWER_BOUND (교차 전 끝 + 정상 · 접촉 · 단조) · UNIDENTIFIED (사유) · NO_CROSSING · TECH · NO_BRACKET (중력 팔만) ↔ `trajectory_status` DONE · TIMEOUT (요약 없음) · LIFT_CAP · GUARD · TECH · RM_STOP |
| 상쇄 | 교차 끝점 마지막 창 인장 합 ≥ 0.5 · P_meas · A (= 1.25 N 덱) → 표지 · 처분 = 진단값 (`rank_eligible` 거짓 · 10 쌍 표 미식별) — 접촉 상태 · 자격과 따로 |
| 선택 | 유효 ρ 둘 (UB · UT) → δ_dt → dt* → 그 dt* 의 UV 하나 → δ_v → 튜플 t1–t4 · 끝점 무효 · NaN · 결손 · 무교차 = SELECTION_UNRESOLVED (다음 팔 · 본 런 없음) · 경계 = ≤ (부동소수 1e-9 %p · choice C13) |
| 관문 | 복원 RESTORED · KE 기준 파일 있어야 · 7:3 UB · UT · UC → UV (선택이 정한 하나) → 최종 팔 · t3 = UTc (S0 에서 새 UT3 없음) · G_ = 최종 팔의 R_M · 나머지 넷 = 최종 튜플 팔만 · 10:0 = S0′ 뒤 |
| 복원 판정 | reset 로그 다섯 (history_zwall_bot · top_mesh · n_neighs_mesh_top_mesh · tracker_top_mesh · contacthistory) · G0 · G1 · G2 · G2c · mesh md5 · G3 · 바닥 이력 PRE = POST · UN 소거 보임 · 이력 시험 rc 0 (+ SYN 부호 = 표) → RESTORED · UNCONFIRMED · SYNTAX_FAIL · VALUE_MISMATCH · 중력 팔 = R_M 의 run 0 setup 에서 G1 · G2 · G2c (출처 팔 R_M 창 끝 · G3 해당 없음 · C12 · 실패 = TECH) |
| 10 쌍 표 | 둘 다 OK · 순위 자격일 때만 합집합 괄호 비교 — 겹침 = 미구분 (동률 아님) · 분리 = 구분 · 아니면 미식별 |

## 5. 봉인 (K8 · `seal_kit.py`) — 활성 규칙 목록 · 폐기 규칙 부재

- `SHA256SUMS` = 러너가 ibb 로 복사하는 묶음 76 파일 (표 · 모듈 · 생성기 · 러너 · 래퍼 · 시험 · `active_rules.json` · 덱 64 · README · 이력 시험 폴더 제외).
- `active_rules.json` = 활성 규칙 12 (선택 · 제출 순서 · UT R_M 멈춤 · UTc · 비단조 합집합 · 분리 · TIMEOUT · 상쇄 · 물리 창 · S3 · σ_P · 이어 돌림 한 번) — 규칙마다 코드 자리 (실재 확인) · 증인 시험.
- 폐기 규칙 검사 (ULR1-05): 옛 띠 b (덱 · 러너 글자 · 파이썬 AST — selftest 안 부재 단언은 제외) · 동시 UV 제출 (러너 · 래퍼 · 이 README 의 `UB … UV` 를 도는 고리 · 한 줄 sbatch 둘) = **0 건** 이어야 `--check` rc 0.

## 6. 권고 기본값 (1저자 비준 대기) — 정본 = 부록 초안

`docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md` (choice C1–C18 · 기본값 · 그 기본값을 고정한 fixture · 비준되면 등록 §13 덧붙임 · 결과 0 건).

## 9. 시험 먼저 기록 (고치기 전 실패 → 고친 뒤)

| 대상 | 고치기 전 (빈 구현 · 없는 파일) | 고친 뒤 |
|---|---|---|
| `history_test/make_history_decks.py --selftest` (덱 · 설계 · run 사이 읽기 · 러너 짝 · 검사기 자신) | 121 중 115 실패 (표 검사 6 만 통과) | 121 / 121 |
| `history_test/read_history.py --selftest` 판정 24 시나리오 (S1–S24) | 27 중 27 실패 | 27 / 27 |
| 같은 파일 러너 모의 (S25–S29 · 가짜 mpirun · lmp) | 8 중 8 실패 (덱 · SHA256SUMS 없음) | 8 / 8 |
| 판 접촉 법선력 부호 (생성기 ⑨ 1 · 읽는 쪽 S30–S32 3) | 4 중 4 실패 | 생성기 122 / 122 · 읽는 쪽 38 / 38 |
| `ul_s3.py --selftest` (K5 S3 총힘 — 중력 평형 사슬 · 쌍 전용 0.0400 · 불평형 · 단위 · 결손) | 14 중 13 실패 | 14 / 14 |
| `ul_observers.py --selftest` (K6 σ_P · 표면 · S4 · ε · W_proxy · KE 기준) | 16 중 16 실패 | 16 / 16 |
| 같은 파일 O4b (σ_P 기본 열 = 실제 thermo 머리 `ul_Ps` — `ULK-01`) | 1 실패 (기본 `v_Ps`) | 17 / 17 |
| `ul_gates.py --selftest` (K7 G0 · G1 · G2 · G2c · G3 · 판 z · S0′ · 복원 판정) | 34 중 34 실패 | 34 / 34 |
| `make_unload_decks.py --selftest` (K2 덱 64 · G0 · ⑭a · ⑭b · if · 표 밖 상수 · 물리 창 · 멈춤 규칙 · 기록 머리 · 러너 짝 · thermo 머리) | 284 중 282 실패 (빈 덱에서 공허한 음성 2) | 285 / 285 |
| 같은 파일 GD7 정정 + GD3b (if 안 include = 3d5c00f input.cpp 845 ERROR — 처음 쓴 시험이 금지된 꼴을 요구했다) | 고친 시험이 고치기 전 덱에서 2 실패 | 285 / 285 |
| `ul_reader.py --selftest` (K4 ULR1-01~05 종단 · S3 · NOISE_FLOOR · 관문 · 이어 돌림 · 10 쌍 · KE 기준 · S0′) | 33 중 33 실패 | 33 / 33 |
| 같은 파일 R14 (복원 판정 조립 4) · R15 (원 파일 복사 명령 1) | 2 실패 (부정 3 은 옛 구현에서도 참 — 판별 = R14 첫 줄) | 38 / 38 |
| 같은 파일 R16 (중력 팔 R_M 복원 G1 · G2 · G2c 2 — choice C12) | 2 실패 | 40 / 40 |
| `ul_runner_test.py --selftest` (K3 러너 모의 · 가짜 mpirun · lmp · 임시 키트 다시 봉인) | 12 중 12 실패 (러너 · 봉인 없음) | 12 / 12 |
| `seal_kit.py --selftest` (K8 봉인 · 활성 규칙 · 폐기 규칙 판별력) | 10 중 10 실패 | 10 / 10 |
