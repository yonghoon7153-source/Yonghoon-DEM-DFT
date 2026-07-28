#!/bin/bash
# watch_all.sh — gabia 전체 작업 한 화면. 관례: watch -n 30 bash tools/ionic/watch_all.sh
# 커버: ① comp2 disorder MD ② SDCP relax ③ MLIP 위원회 온도 스윕 ④ 체인 게이트
set +e
W=$HOME/work
echo "=============== gabia 전체 상황  $(date '+%m-%d %H:%M') ==============="

# ── GPU ────────────────────────────────────────────────────────────────
GPU=$(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
      --format=csv,noheader,nounits 2>/dev/null)
echo "GPU: ${GPU:-(조회 실패)}   [util%, used MiB, total MiB]"
echo "  pw.x $(pgrep -x pw.x >/dev/null && echo ALIVE || echo '-')  ·  \
MLIP-MD $(pgrep -f 'aimd_mlip|disorder_ensemble_diffusion' >/dev/null && echo ALIVE || echo '-')"
echo "----------------------------------------------------------------------"

# ── ① comp2 disorder ensemble ─────────────────────────────────────────
echo "① comp2 DISORDER ensemble"
for D in "$W"/runs/comp2_disorder*/d*_cfg*; do
  [ -d "$D" ] || continue
  L="  $(basename "$D") :"
  N=0
  for T in 600 800 1000; do
    F="$D/T$T/aimd_results.json"
    if [ -f "$F" ]; then
      S=$(grep -ao '"sigma_NE_Scm_Li":[^,}]*' "$F" 2>/dev/null | head -1 | cut -d: -f2)
      L="$L ${T}K✓(${S:-?})"; N=$((N+1))
    else L="$L ${T}K·"; fi
  done
  echo "$L  [$N/3]"
done
echo "  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)"
echo "----------------------------------------------------------------------"

# ── ② SDCP relax ──────────────────────────────────────────────────────
echo "② SDCP complex_doped_v2 relax (k 2×2×1)"
SO=$(ls -t "$W"/../*sdcp*/*.out "$W"/*sdcp*/*.out 2>/dev/null | head -1)
if [ -n "$SO" ]; then
  echo "  out: $SO"
  grep -a "number of k points" "$SO" | tail -1 | sed 's/^/  /'
  # ⚠ scf_must_converge=.false. + maxstep 도달 = 가짜 수렴. 반복수를 반드시 본다.
  echo "  완료 step별 반복수 (maxstep과 같으면 **가짜 수렴**):"
  grep -a "convergence has been achieved in" "$SO" | tail -3 | sed 's/^/    /'
  grep -a "iteration #\|estimated scf accuracy" "$SO" | tail -2 | sed 's/^/    /'
else echo "  (out 파일 못 찾음 — 경로 확인)"; fi
echo "----------------------------------------------------------------------"

# ── ③ MLIP 위원회 온도 스윕 (T1) ──────────────────────────────────────
echo "③ MLIP 위원회 온도 스윕 — T1 외삽 대리지표"
echo "   기준선(600 K 교정): 중앙 0.3175 · p95 0.3669 eV/Å"
FOUND=0
for D in "$W"/committee_modelc_T*/; do
  [ -d "$D" ] || continue
  FOUND=1
  T=$(basename "$D" | sed 's/.*_T//')
  N=$(ls "$D"/pred_*.npz 2>/dev/null | wc -l)
  V="$D/committee_verdict.json"
  if [ -f "$V" ]; then
    MED=$(grep -ao '"median":[^,}]*' "$V" | head -1 | cut -d: -f2)
    NAB=$(grep -ao '"n_above_break":[^,}]*' "$V" | head -1 | cut -d: -f2)
    MODE=$(grep -ao '"mode": "[^"]*' "$V" | head -1 | cut -d'"' -f4 | cut -c1-2)
    echo "  T$T: 엔진 $N/3 · 중앙${MED:-?} · break초과${NAB:-?}/200 · [$MODE]"
  else
    echo "  T$T: 엔진 $N/3 · 판정 대기"
  fi
done
[ "$FOUND" = 0 ] && echo "  (아직 없음)"
echo "   ⚠ '교정' 모드의 초과 개수는 정의상 자명 — **'탐지' 모드 값만 정보다**"
echo "----------------------------------------------------------------------"

# ── ④ 체인 게이트 ─────────────────────────────────────────────────────
echo "④ 후속 체인 (GPU 해방 대기 → QE 단일점 + Li 슬랩)"
tail -1 "$HOME/logs/chain2.log" 2>/dev/null | sed 's/^/  /' || echo "  (chain2 미가동)"
echo "----------------------------------------------------------------------"
echo "tmux: $(tmux ls 2>/dev/null | cut -d: -f1 | tr '\n' ' ')"
