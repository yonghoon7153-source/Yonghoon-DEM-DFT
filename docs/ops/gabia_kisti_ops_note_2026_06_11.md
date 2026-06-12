# 운영 노트 — gabia/KISTI 3-트랙 복구 (2026-06-11)

> comp1 4fu MD 테스트로 kill됐던 작업들 복구 기록 + 재발 방지 함정 목록.
> 다음에 같은 작업 할 때 이 문서부터 볼 것.

## 복구 결과 (2026-06-11 21:42 기준)

| 트랙 | 위치 | 상태 |
|---|---|---|
| Nd₂O₃ DFT EOS SCF | KISTI job **753206** (gpu41) | k441 23-iter 수렴 (1.1e-6 Ry) → stress 단계. 완료 watcher ON |
| Li3N full-DFT NEB | gabia `li3n_001/dft_neb` | fresh start (improved-tangent), pw.x GPU 14 GB / 100% |
| 273-cascade v23 | gabia `multi_category_2026_05_26_v23` | Step 40 Sc2O3_x002 stage 10 σ-MD 재개. 39 done / 4 resume / 230 pending |

## ⚠ 함정 목록 (이번에 밟은 것들)

### 1. `master_batch_273.sh`는 BATCH_DIR env 필수
- `BATCH_DIR="${BATCH_DIR:-...multi_category_2026_05_19_v22}"` (line 73) — **env 없이 실행하면 옛 v22로 떨어짐**.
- 실제로 env 없이 재시작했다가 v22에 Na2O_x002를 다시 돌리기 시작한 사고 발생 → kill 후 재시작.
- 올바른 재시작:
  ```bash
  BATCH_DIR=/data/work/runs/multi_category_2026_05_26_v23 \
  nohup bash /data/work/repo/tools/doping/master_batch_273.sh \
      > /data/work/runs/multi_category_2026_05_26_v23/master_resume<N>_$(date +%m%d_%H%M).log 2>&1 &
  ```
- 재발 방지: `echo 'export BATCH_DIR=...v23' >> ~/.bashrc` (v24 batch 시작할 때 갱신할 것).
- 재시작 후 반드시 scan 검증: `BATCH_DIR=...v23` / `done: 39+` / PARTIAL 목록 확인.

### 2. Sc₂O₃ "TIMEOUT"은 데이터 손실이 아니다
- Step 40–42 Sc2O3 trio가 24h TIMEOUT ×2 + kill(rc=143) 이력 — 그러나 **stage marker는 매번 전진** (STAGE_09f.DONE까지 도달).
- 원인: **stage 10 σ-MD** (top2 configs × 600/800/1000 K × 50 ps UMA MD)가 cascade 최장 단계 — 24h 윈도우 끝자락에 진입해 잘림.
- resume scanner (v4.5.22 5-trigger)가 PARTIAL로 잡아 마지막 stage부터 재개. done 판정은 `STAGE_12.DONE` marker (stage 10–12는 스킵 아님 — MgO_x002 확인: 09f → 12b → 12).

### 3. Li3N NEB 재시작 = `dft_neb/launch_neb.sh` (repo 스크립트 ✗)
- repo의 `tools/neb_diffusion/run_neb_qe.sh`는 warm-start 기본값이
  `li3n_001/neb_run1/neb_path_final.xyz`인데 **이 파일은 2026-06-04 wrong-endpoints 사건 때 `archive_wrong_endpoints_20260604/`로 이동** → FileNotFoundError 즉사. archive 안의 path를 warm start로 쓰면 안 됨 (틀린 endpoint).
- 올바른 재시작 (수정된 endpoint `on_N_left/right.xyz` 내장):
  ```bash
  cd /data/work/runs/li_neb_diffusion/li3n_001/dft_neb
  nohup bash launch_neb.sh > relaunch_<날짜>.log 2>&1 &
  ```
- checkpoint는 `neb_warmup.traj` (21 frames = 3 iter 분량이었음 — fresh start 손실 미미).
- ASE 3.28 NEB default가 improved-tangent로 변경 (경고 무해, paper methods에 "CI-NEB, improved-tangent" 명기).
- `launch_neb.sh`의 `pw=...qe-7.4.1-cpu` echo는 `which` 표시일 뿐 — 실제 계산은 GPU 바이너리 (nvidia-smi로 확인).

### 4. (drift 2호) TOP_K_SIGMA / TOP_K_NCM도 env 필수
- done 39개는 전부 **`TOP_K_SIGMA=0, TOP_K_NCM=0`** (05-26 원래 master)로 완료 — stage 10 (σ-MD)·11 (NCM)은 SKIP, 디렉토리 자체가 없음 (MgO_x002 확인: 09f → 12).
- 06-08 resume5부터 env가 빠지며 script default (`TOP_K_SIGMA=2, TOP_K_NCM=3`)로 drift → cascade당 24h 초과 → **Sc₂O₃ timeout의 진짜 원인**.
- 올바른 재시작 (env 3종 모두 명시):
  ```bash
  BATCH_DIR=/data/work/runs/multi_category_2026_05_26_v23 TOP_K_SIGMA=0 TOP_K_NCM=0 \
  nohup bash /data/work/repo/tools/doping/master_batch_273.sh > ...resume<N>.log 2>&1 &
  ```
- 재시작 후 헤더에서 `TOP_K_SIGMA=0, TOP_K_NCM=0` 확인. σ-MD/NCM은 batch 완주 후 winner만 `COMPOUND_FILTER=<dopant> TOP_K_SIGMA=2`로 단독 실행.

### 5. KISTI job 753206의 이름은 가짜
- `JobName=llm_finetuning_test`는 sbatch 템플릿 (`sbatch_ktest.sh`) 잔재. 실체는
  `/scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos_v7/pair01_pair_00_reference_1_82/v0_champion` k-test (4 4 1 → ...).
- run4 ×4 + run5 ×4 시도 끝에 도는 중. 다음부터 `#SBATCH -J nd_k441_scf`로 바꿀 것.
- "SCF correction compared to forces is large" 경고: EOS 에너지 목적엔 무시 가능, force 쓸 거면 conv_thr 강화.

### 6. KISTI GPU 규약 (2026-06-12 신설, 사용자 결정)
- **잡당 GPU 1개** — 2트랙 병렬 운용 목적: `--ntasks-per-node=1`, `--gres=gpu:1`,
  `mpirun -np 1 ... -npool 1` (⚠ np와 npool은 반드시 함께 1로 — rank 1 + npool 2는 에러)
- 기존 2-GPU 템플릿(sbatch_ktest.sh)은 참고용으로만. 이미 제출된 잡은 완주 후 적용.
- 적용 1호: nd_dos 756472(2-GPU) scancel → **756475(1-GPU) 재제출** (06-12).

## B₂O₃ DFT-EOS → KISTI 이관 (2026-06-12, paste 전용)

**V100 사망 시점 상태** (WSL 백업 `runs/b2o3_dft3_run` 전수조사, nat=128, JOB DONE **0개**):

| vol | 상태 | lastE (Ry) | KISTI 조치 |
|---|---|---|---|
| 0.98 | BFGS 좌표블록 **61개** 진행 중 | −2621.73962908 | 마지막 좌표로 from_scratch 재시작 |
| 1.00 | 블록 19개 진행 중 | −2621.75212577 | 〃 |
| 1.02 | **SCF 발산** (UMA warm-start 좌표, 블록 0) | — | v1.00 좌표 ×cbrt(1.02) 이식 + `mixing_beta=0.05`(형제 동일) |
| 0.96/1.04/1.06 | 미생성 | — | v1.00 템플릿에서 cell·좌표 cbrt(tag) 스케일 신규 |

- 구기록 "v0.98 step 5"는 옛 스냅샷 — 실제 61블록. recover/recover3 시도는 빈 파일(무시).
- **실입력 검수 (06-12, payload 눈검사)**: V100 입력은 driver 기본값이 아니라 **발산 대응 튜닝본** —
  `degauss 0.02 / forc_conv 1e-3 / mixing_beta 0.05 + local-TF / electron_maxstep 500 /
  diago_david_ndim 2 / k 3 3 1`. 그리고 `eos_v0.98.in`에 recover 시절 잔재
  **`restart_mode='restart'` 발견** — KISTI엔 .save가 없어 그대로면 즉사. restage 도구가
  자동 제거하도록 패치(+v1.02 beta는 0.15 처방을 철회하고 형제와 동일한 0.05로 매칭).
  이미 paste한 경우 KISTI에서 `sed -i "/restart_mode/d" eos_v0.98.in` +
  `sed -i "s/mixing_beta=0.15/mixing_beta=0.05/" eos_v1.02.in` (이 sed 후 두 파일 md5는
  최초 manifest와 달라지는 게 정상).
- **3점으로는 BM3 fit 불가**(드라이버 `b2o3_dft_eos.py`부터 n≥4 요구) → modelC와 동일한
  **6점 그리드 0.96–1.06**(v{096..106})로 확장 = ΔB₀ vs 21.71 apples-to-apples.
- sftp/scp 불가 → **`tools/doping/b2o3_kisti_restage.py`** (WSL에서 실행)가
  `/mnt/d/v100백업/b2o3_kisti_stage/paste_payloads/`에 **heredoc payload 7개 + payload_ALL.txt**
  생성 (md5 manifest 출력 → KISTI에서 `md5sum`으로 paste 손상 검증).
  바이너리(.save/.bfgs)는 버림 — BFGS 히스토리 손실은 SCF 몇 사이클 비용뿐 (표준 복구 경로).
- UPF는 paste 불가 → 입력은 전부 `pseudo_dir='./pseudo/'`; KISTI에서 Nd-run pseudo 복사
  + 부족분(B 등) `wget https://pseudopotentials.quantum-espresso.org/upf_files/<정확한 파일명>`.
- sbatch는 검증된 `run_nd_dos.sh` 헤더 재사용(`awk '/mpirun/{exit} {print}'`) + `-J b2o3_eos`,
  1-GPU 규약(함정 #6), 실행 순서 0.98→1.00→1.02→0.96→1.04→1.06 (완성 임박 순),
  JOB DONE skip + **`resume_splice.py` 자동 좌표 이식** → 워크타임 킬 후엔 그냥 재제출.
- 완료 후: `grep '^!.*total energy' eos_v*.out | tail -1` ×6 (V,E) → BM3 fit(로컬) → ΔB₀ vs 21.71.

## Watch 명령 모음

```bash
# gabia — NEB + cascade 통합 (포그라운드)
watch -n 60 '
echo "═══ Li3N NEB ═══";
tail -4 /data/work/runs/li_neb_diffusion/li3n_001/dft_neb/neb.log 2>/dev/null \
  || tail -4 /data/work/runs/li_neb_diffusion/li3n_001/dft_neb/relaunch_0611c.log;
echo; echo "═══ Cascade v23 ═══";
bash /data/work/runs/watch_v23.sh 2>/dev/null | tail -8;
echo; echo "═══ GPU ═══";
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader'

# gabia — 백그라운드 10분 스냅샷 로거 (→ /data/work/runs/dual_watch.log)
nohup bash -c 'while true; do
  { date; tail -2 /data/work/runs/li_neb_diffusion/li3n_001/dft_neb/neb.log 2>/dev/null;
    bash /data/work/runs/watch_v23.sh 2>/dev/null | grep -E "현재|완료";
    nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader; echo ---; } \
  >> /data/work/runs/dual_watch.log; sleep 600; done' >/dev/null 2>&1 &

# KISTI — 753206 완료 기록 watcher (가동 중, PID 934184)
cat ~/job753206_watch.log   # 끝나면 State/Elapsed/ExitCode 찍힘
```

## 남은 체크포인트

- [ ] Sc2O3_x002 stage 12 완료 확인 (예상: σ-MD 6런 후 수 시간 내)
- [x] KISTI 753206 완료 → k661 자동 연계 ✓ (2026-06-12 00:27 완료 확인)
  - **k-수렴 판정 (06-12)**: k441 −3566.23655394 / k661 −3566.23666523 Ry
    → ΔE = 0.11 mRy 전체 = **0.013 meV/atom (nat=120)** → **EOS는 k441 채택**
  - **결정 (2026-06-12, 사용자)**: k441 tight SCF를 V0 최종으로 확정, **EOS 스킵**
    → 바로 post-processing. 1번 타자 = DOS/PDOS (NSCF k661 → dos.x → projwfc.x).
    ⚠ NSCF는 scf_k441.in의 nspin=2/Hubbard U/starting_mag 블록을 그대로 상속할 것
    (U 값은 입력파일이 정본 — 기록상 6.0/8.0 혼재하므로 grep으로 확인)
  - plot 도구에 Nd(teal)·O(red) 색 추가 완료 (plot_dos.py, plot_pdos_appendix.py)
- [ ] Li3N NEB fmax 수렴 추이 (`neb.log`) — 5–7일 예상
- [ ] v22에 오늘 생긴 Na2O_x002 stage 10+ 잔해 정리 (무해, optional)
