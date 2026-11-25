---
title: "재기동 절차서 — 2026-09-07 재부팅 (gabia · desktop)"
date: 2026-09-07
updated: 2026-09-07
tags: [ops, restart, runbook, gabia, desktop, lpsocl, sdcp, sei]
status: 진행
kind: report
system: ops
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-07
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 재기동 절차서 — 2026-09-07 재부팅

> 1저자가 두 기계를 껐다 켠다. **재부팅은 `nohup` 으로도 살아남지 않는다** —
> 아래 넷은 전부 다시 걸어야 한다. 이 문서가 "무엇을, 어디서, 어떤 명령으로" 의 정본이다.

## 0. ✅ 끄기 전에 뜬 것 (2026-09-07 10:08 실측 · `ps -eo pid,lstart,args`)

| 무엇 | 상태 |
|---|---|
| LPSOCl MD 루프 명령 **전문** | ✅ 확보 — §3-1 |
| gabia 두 잡의 명령·시작시각 | ✅ 확보 — §2 |
| `gs[0-7]` 실제 경로 | ✅ 확보 — §3-2 |
| MD 루프의 **cwd** | ✅ **`/home/kgy/Yonghoon-DEM-DFT`** (루프·자식 둘 다 · `readlink /proc/…/cwd` 실측) |

⚠ **desktop 에 repo clone 이 둘 있다** — `~/Yonghoon-DEM-DFT` 와 `~/work/Yonghoon-DEM-DFT`
(후자에서 `tools/ionic/chain_gpu_release.sh` 가 08-26 부터 돌고 있었다).
MD 명령이 `python3 tools/modelc_v3/...` 를 **상대경로**로 부르므로 어느 clone 에서 띄웠는지가
결과에 영향한다. **실측 결과 정본(`~/Yonghoon-DEM-DFT`)이 맞았다** — 재기동도 거기서 한다.
(gabia 는 반대로 감시가 `/root/work/…`(b2o3run 브랜치)를 보고 있어 8.7일간 가짜 경보를 찍었다.)

## 1. 끄기 직전 상태 (2026-09-07 10:0x 실측)

| 기계 | 잡 | 진행 | 재부팅 손실 |
|---|---|---|---|
| gabia | **n=6 doped** ORCA (`/data/work/runs/sdcp_n6b`) | cycle 7 · 06:50 시작 | 약 3.5 h — ⚠ §2-1 참조(사실상 이어달리기 가능) |
| gabia | **QE r2** (`sei_control/li3nd_…_r2`) | step 1 · `E −14652.1266` · `\|F\| 0.0396` | 약 3 h |
| gabia | QE r3 | 대기 (r2 뒤 직렬) | 없음 |
| desktop | **LPSOCl MD** 9런 중 3 완료 · s3 600K **43 %** | 런당 18.3 h | ⚠ **약 8 h** — 제일 아깝다 |
| desktop | **Stage A** ORCA (gs0–gs7) | **이미 멈춰 있었다** (프로세스 0개) | 없음 |

⚠ 재부팅 전에도 **Stage A 는 안 돌고 있었다.** 껐다 켜서 생긴 문제가 아니다.

## 2. 재기동 — gabia (`root@121.78.116.27` · `kserver116-27`)

**정본 clone 은 `/root/Yonghoon-DEM-DFT` 다.**
⛔ `/root/work/Yonghoon-DEM-DFT` 는 **`b2o3run` 브랜치의 작업 폴더**다(DEM 변형·섬유 스윕 미추적 산출물 다수).
거기서 도구를 돌리면 낡은 판정을 받는다 — **손대지 말 것.**

```bash
cd ~/Yonghoon-DEM-DFT && git pull --ff-only origin claude/friendly-meitner-lldvar
```

### 2-1. n=6 doped ORCA

```bash
cd /data/work/runs/sdcp_n6b && nohup bash run.sh > run.log 2>&1 &
sleep 15; head -3 run.log
```

**⛔ `run.log` 첫 줄에 `OMPI_MCA_btl=self,vader` 가 없으면 죽여야 한다.**
그게 없으면 09-06 처럼 **LEANSCF 에서 MPI 로 죽는다**(SCF 는 수렴까지 갔다가 거기서 끝난다).
gabia 는 OpenMPI 4.1.6 → `self,vader` 가 정답이다(5.x 는 `self,sm`; 없는 이름을 넣으면 MPI_Init 즉사).

⚠ **이어달리기에 관하여** — ORCA 는 매 사이클 `n6_doped.xyz` 를 **현재 기하로 덮어쓴다.**
그래서 `run.sh` 를 그대로 다시 걸면 사실상 cycle 7 기하에서 재개된다(3.5 h 를 안 버린다).
대신 **시작구조 증거가 그 폴더에 없다** — 원본은 `groups.json` 의 `source_xyz` 와
이전 폴더 `/data/work/runs/sdcp_n6` 에 있다. 계보를 깨끗이 하려면 §2-1b.

**§2-1b (선택) 완전히 새로 짓기** — 3.5 h 를 버리는 대신 계보가 깨끗하다:
```bash
PILOT=$(dirname "$(python3 -c "import json;print(json.load(open('/data/work/runs/sdcp_n6/groups.json'))['source_manifest'])")")
python3 ~/Yonghoon-DEM-DFT/tools/sdcp/nseries_n6.py --pilot "$PILOT" --out /data/work/runs/sdcp_n6c --opt --nprocs 8 --maxcore 2500
cd /data/work/runs/sdcp_n6c && nohup bash run.sh > run.log 2>&1 &
```

감시:
```bash
watch -n 300 "bash ~/Yonghoon-DEM-DFT/tools/sdcp/watch_n6.sh /data/work/runs/sdcp_n6b"
```

### 2-2. QE (r2 · r3)

```bash
cd ~/Yonghoon-DEM-DFT
bash tools/sei/restart_qe_relax.sh                      # 판정만 — 먼저 본다
nohup bash tools/sei/restart_qe_relax.sh --run > /tmp/qe_restart.log 2>&1 &
```

기대 판정: `r0 수렴` · `r1 수렴` · `r2 죽음 → from_scratch` · `r3 nstep소진 → nstep 200 · restart` ·
`_control_structures 잡 아님`. GPU 게이트가 **한 번에 하나씩** 돌린다.

감시 — ⚠ **정본 clone 경로를 명시**한다(예전엔 `/root/work/...` 를 보고 있어서 낡은 판정을 찍었다):
```bash
watch -n 120 "QE_WATCH_ROOTS=/data/work/runs/sei_control STALL_MIN=90 bash /root/Yonghoon-DEM-DFT/tools/sei/watch_qe_relax.sh"
```

## 3. 재기동 — desktop (`esp-Z590-AORUS-MASTER` · 16코어)

```bash
cd ~/Yonghoon-DEM-DFT && git pull --ff-only origin claude/friendly-meitner-lldvar
```

### 3-1. LPSOCl MD — **원본 명령 (2026-09-04 16:17:44 기동, PID 3376826 실측)**

```bash
bash -c 'for s in 2 3 4; do python3 tools/modelc_v3/disorder_ensemble_diffusion.py \
  --v0_xyz db/structures/lpsocl_relaxV0_3x3x1.xyz --label lpsocl \
  --temperatures 600 800 1000 --disorder_levels 0.0 --n_configs 1 \
  --equilib_ps 5 --prod_ps 400 --timestep_fs 2 --friction 0.02 \
  --fit_window_ps 2 50 --uma_model uma-s-1p1 --uma_task omat --save_traj \
  --seed $s --out_root ~/work/runs/lpsocl_box331_400ps/s$s 2>&1; done' \
  | tee -a ~/logs/lps400.log
```

**⛔ 다시 걸 때는 `for s in 3 4` 로 바꾼다.** 시드 2 는 600/800/1000 K 셋 다 완료돼
`msd.json` 이 있다(`~/work/runs/lpsocl_box331_400ps/s2`). 그대로 걸면 완료분을 덮어쓴다.

⚠ s3 는 **2026-09-07 03:12:51 기동**(PID 497454), 600 K 43 % 에서 끊겼다.
`--save_traj` 가 켜져 있어 `.traj` 는 남지만, **이 드라이버는 traj 에서 이어달리지 않는다** —
확인 전에는 **처음부터 도는 것으로 본다**:
```bash
ls -la ~/work/runs/lpsocl_box331_400ps/s3/*/ 2>/dev/null | head -20
find ~/work/runs/lpsocl_box331_400ps -name '*.traj' -newermt '-2 days' 2>/dev/null | head
```

⚠ **cwd 를 맞춰서 띄운다** — 명령이 `tools/modelc_v3/…` 를 상대경로로 부른다. §0 의
`readlink /proc/3376826/cwd` 값이 정본이고, 못 구했으면 **`~/Yonghoon-DEM-DFT`** 를 쓴다
(같은 기계의 MD 감시가 `~/Yonghoon-DEM-DFT/tools/ionic/watch_lpsocl_400ps.sh` 를 쓰고 있었다).

**띄울 때는 반드시 `tmux`:**
```bash
tmux new -s md
# 안에서 cd ~/Yonghoon-DEM-DFT && 위 명령 (for s in 3 4)
```
지난판은 `nohup` 이 **하나도** 안 걸려 있었다(부모까지 전부 `⚠끊기면죽음`). 반복하지 않는다.

감시:
```bash
watch -n 30 bash ~/Yonghoon-DEM-DFT/tools/ionic/watch_lpsocl_400ps.sh
```

### 3-2. Stage A (gs0–gs7) — 재부팅 전에도 멈춰 있었다 (ORCA 프로세스 0개)

**경로 실측:**

| | 경로 | 내용 |
|---|---|---|
| `stageA_dir` (입력 정본) | `~/work/runs/sdcp_stageA` | `gs0`…`gs7` **8개 전부** |
| `work_dir` (스크래치) | `~/work/runs/sdcp_stageA_run` | **`gs4`·`gs5` 둘뿐** |

⇒ 이번 캠페인에서 실제로 돌린 것은 **gs4·gs5 둘**이다. `gs4` 는 **수렴 완료**
(cyc 138 · `conv=1` · E −10051.702558950057 Eh), `gs5` 는 **cyc 0 에서 죽었다**.
`gs0–gs3·gs6·gs7` 은 **아직 시작도 안 했다.**

```bash
bash tools/sdcp/watch_stage_a.sh ~/work/runs/sdcp_stageA_run
find ~/work/runs/sdcp_stageA_run -maxdepth 3 -name '.lock_seed'   # 죽은 lock 이 재실행을 막는다
```
⚠ 재부팅하면 lock 안의 pid 는 전부 죽은 pid 다. 러너는 **남의 lock 을 안 지운다**(설계상 옳다) —
`STALE_LOCK_MIN` 을 넘겨 스스로 정리하게 두거나, 사람이 확인하고 지운다.

**✅ gs5 사인 확정 (2026-09-07 10:42, repo 감시 실물): `rc=143` = 128+15 = SIGTERM.**
**MPI 가 아니다.** 43시간 전(≈09-05 15:44)에 **밖에서 죽인 것**이다.
⚠ 여기 처음엔 *"LEANSCF 오류면 gabia 와 같은 건"* 이라고 적었는데 **근거 없는 추측이었다** —
러너가 receipt 에 rc 를 이미 적어 두고 있었다. **receipt 를 먼저 읽는다.**
```bash
bash tools/sdcp/watch_stage_a.sh ~/work/runs/sdcp_stageA_run   # rc·relaxed 를 찍는다
cat ~/work/runs/sdcp_stageA_run/gs5/receipt.json
```

### ✅ gs 는 돌리지 않는다 — **1저자 결정 (2026-09-07)**

> *"gs는 돌리지말자, 굳이인거잖아"*

아래 근거로 제안했고 1저자가 받았다. `gs4` 는 `DONE` 으로 남기고 나머지 여섯은 놔둔다.
**재개하려면 아래 표의 전제(Stage B NO-GO · doped 경로가 gs 를 안 읽음)가 깨져야 한다.**

### 근거 (2026-09-07 판단)

| | |
|---|---|
| Stage A(gs*) 의 용도 | 중성 n=6 **8 conformer** 이완 → **Stage B 의 부모 구조** 선정 |
| Stage B | 회신 R4 판정 **NO-GO** (P0 5건 전부 불충분) |
| 원고 Figure 2e(자가도핑) | **gabia 의 doped n=6** 이 답한다 — 그건 폴라론 pilot 구조에서 만들고 **gs* 를 안 읽는다** |

⇒ **gs 6개 추가는 원고 경로가 아니다.** `gs4` 는 `DONE`(cyc 137 · rc=0 · relaxed=True)로 남는다.
⚠ 한계: 확인한 것은 *"gs → Stage B, Stage B 는 NO-GO, doped n=6 은 gs 를 안 읽는다"* 까지다.
나중에 **중성 대조**가 필요해지면 그때 다시 판단한다.

재기동 (**돌리기로 결정했을 때만** · ⚠ `gs4` 는 수렴 완료라 **다시 걸지 않는다**):
```bash
tmux new -s stagea
ORCA=$(command -v orca) NPROCS=8 ONLY="gs5 gs3 gs6 gs7" \
  bash tools/sdcp/run_orca_stage_a.sh ~/work/runs/sdcp_stageA ~/work/runs/sdcp_stageA_run
```

⚠ **desktop 은 16코어인데 MD 가 이미 쓰고 있다.** MD(GPU 주) + ORCA 8 은 공존 가능하지만,
seed 를 여러 개 동시에 걸면 서로 굶는다. **한 번에 하나씩**이 안전하다.

**참고 — 지난 인라인 감시 명령**(repo 도구를 쓰는 게 낫지만 원본을 남겨 둔다):
```
watch -n 30 'cd ~/work/runs; date +%H:%M:%S; echo; for g in gs3 gs4 gs5 gs6 gs7; do
  f=sdcp_stageA_run/$g/dp6_${g}_neutral.out; ...'
```
⛔ 이 화면이 `gs4 cyc 138` 을 계속 보여줘서 "돌고 있다" 로 읽혔는데 **ORCA 프로세스는 0개**였다.
생사를 안 찍는 감시는 이런 식으로 사람을 속인다 — `watch_stage_a.sh` 를 쓴다.

## 4. 되살린 뒤 확인 목록

- [ ] gabia `run.log` 에 `OMPI_MCA_btl=self,vader`
- [ ] gabia `watch_n6` 가 `▶ 도는중` · 사이클이 **는다**
- [ ] gabia QE 판정에 `_control_structures 잡 아님` (정본 clone 을 보고 있다는 증거)
- [ ] desktop MD 가 **tmux 안**에 있다 · 시드 2 를 다시 안 돈다
- [ ] desktop Stage A lock 정리됨 · `gs4` 재실행 안 됨

## 5. 이번에 배운 것 (다음 재부팅 때도 같다)

1. **`nohup` 은 부모만 지킨다.** `mpirun`·`pw.x` 는 자기 신호 핸들러를 새로 깔며 SIGHUP 을
   되살린다 — 실측으로 자식 9개가 전부 노출돼 있었다. **`tmux` 가 정답이다.**
2. **감시 화면은 정본 clone 을 가리켜야 한다.** gabia 에서 `/root/work/…`(다른 브랜치)를
   보고 있어서 8.7일간 가짜 경보를 찍었다.
3. **손으로 만든 인라인 감시는 얇다.** desktop 인라인 감시가 `gs4 cyc 138` 을 계속 보여줘서
   "돌고 있다" 로 읽혔는데 실은 **ORCA 프로세스가 0개**였다. repo 감시는 생사를 찍는다.

## 관련
- `tools/sdcp/orca_mpi_env.sh` · `tools/sdcp/watch_n6.sh` · `tools/sdcp/run_orca_stage_a.sh`
- `tools/sei/restart_qe_relax.sh` · `tools/sei/watch_qe_relax.sh`
- `db/properties/lpsocl_box331_closure_conditions_2026_09_07.json`
- `kb/questions/li3nd_pristine_reconstruction_2026_09_02.md`
