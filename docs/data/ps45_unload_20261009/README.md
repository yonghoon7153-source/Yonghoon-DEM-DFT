# DEM 언로딩 키트 — ps45 다섯 침대 (등록 개정 2 · 시험 먼저) · ⛔ 본 R · 10:0 이완 연장 · 개발 / 생산 U = Codex (키트 증거 + 개정 2) 뒤

- 등록 (정본): `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG — §12 개정 1 · §13 개정 2) · 반영 계획 `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` (✅ 1저자 10-12 Q1–Q4 권고대로) ·
  Codex 판정문 `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` (CX1) · `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` (CX2).
- 이 README 가 **이름의 정본**이다 (REG §8-2 "이름은 가칭 · 키트 README 가 정본").
- 지금 할 수 있는 것 = **§1 작은 침대 이력 시험 (H0–H5) 만** — 본 키트 봉인과 따로 봉인 (`history_test/SHA256SUMS`) 해서 먼저 돌릴 수 있다.
  ⛔ 이 시험이 PASS 여도 본 R · 10:0 연장 · U 의 GO 가 아니다 (CX2 §0 · REG §13-6 — 키트 증거 → Codex 재검토 → 본 실행).
- 이 컨테이너에는 LIGGGHTS 가 없다 — 덱 문법은 소스 판독 (CX2 §5 · 노트) + 생성기 selftest 까지이고, 실제 바이너리는 §1 의 ibb 시험이 처음이다.

## 0. 이름 (정본)

| 무엇 | 이름 |
|---|---|
| 키트 폴더 | `docs/data/ps45_unload_20261009/` |
| 이력 시험 (H0–H5 · 따로 봉인) | `history_test/` — `make_history_decks.py` (생성기 · `--check` · `--selftest`) · `read_history.py` (읽는 쪽 · `--selftest`) · `run_history.sh` (러너) · `run_history_ibb.sbatch` (ibb 래퍼) · `history_params.json` (fixture 표) · 덱 여덟 `in.hist_*.liggghts` · `plate_hist.stl` · `SHA256SUMS` |
| ibb 작업 폴더 (이력 시험) | `~/ps45_unload_hist_20261013` (런 = 그 아래 `hist_<시각>/` · 보고 묶음 `hist_<시각>.report.tgz`) |
| SLURM job 이름 | `ulHist` (이력 시험) |

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

## 9. 시험 먼저 기록 (고치기 전 실패 → 고친 뒤)

| 대상 | 고치기 전 (빈 구현 · 없는 파일) | 고친 뒤 |
|---|---|---|
| `history_test/make_history_decks.py --selftest` (덱 · 설계 · run 사이 읽기 · 러너 짝 · 검사기 자신) | 121 중 115 실패 (표 검사 6 만 통과) | 121 / 121 |
| `history_test/read_history.py --selftest` 판정 24 시나리오 (S1–S24) | 27 중 27 실패 | 27 / 27 |
| 같은 파일 러너 모의 (S25–S29 · 가짜 mpirun · lmp) | 8 중 8 실패 (덱 · SHA256SUMS 없음) | 8 / 8 |
| 판 접촉 법선력 부호 (생성기 ⑨ 1 · 읽는 쪽 S30–S32 3) | 4 중 4 실패 | 생성기 122 / 122 · 읽는 쪽 38 / 38 |
