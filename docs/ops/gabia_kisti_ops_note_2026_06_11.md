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
  - 다음: EOS 11 volumes (V/V₀ 0.96–1.06) submit — scripts/adhesion/
    prepare_dft_eos_nd.py + sbatch_dft_eos_nd.sh 사용, `#SBATCH -J nd_k441_eos`로
    이름 교체 (함정 #5)
- [ ] Li3N NEB fmax 수렴 추이 (`neb.log`) — 5–7일 예상
- [ ] v22에 오늘 생긴 Na2O_x002 stage 10+ 잔해 정리 (무해, optional)
