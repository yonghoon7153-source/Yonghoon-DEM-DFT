#!/bin/bash
# watch_lpsocl_eos.sh — detailed live status for the LPSOCl DFT EOS chain (KISTI).
#   watch -n 60 bash ~/watch_lpsocl.sh
# Mirrors sbatch_dft_eos_lpsocl_chain.sh: 7 fixed-cell relaxes v094..v106 over
# 2 GPU streams (GPU0: v094 v098 v102 v106 / GPU1: v096 v100 v104), done-marker
# "JOB DONE", ALL_DONE flag when 7/7. Shows chain queue, per-volume bfgs/force/age
# so a stalled relax (age > 5 min, step not advancing) is visible immediately.
WB=/scratch/x3430a02/kgy/lpsocl_eos
RY=13.605693
declare -A GPU=( [v094]=0 [v098]=0 [v102]=0 [v106]=0 [v096]=1 [v100]=1 [v104]=1 )
VOLS="v094 v096 v098 v100 v102 v104 v106"
now=$(date +%s)

echo "══════ KISTI LPSOCl EOS  $(date '+%m-%d %H:%M:%S') ══════"

# ---- chain (squeue) ----
echo "── 체인 (squeue, QOS 상한 4) ──"
q=$(squeue -u x3430a02 -h -n lpsocl_eos -o "  %.9i %.9T %.8M %.9L %R" 2>/dev/null | sort -k1)
if [ -n "$q" ]; then echo "$q"; else echo "  (큐에 lpsocl_eos 없음)"; fi
nq=$(squeue -u x3430a02 -h -n lpsocl_eos 2>/dev/null | wc -l)
nr=$(squeue -u x3430a02 -h -n lpsocl_eos -t RUNNING 2>/dev/null | wc -l)
echo "  세그먼트: 큐 $nq개 (실행 $nr / 대기 $((nq-nr)))"
[ -f "$WB/ALL_DONE" ] && echo "  ★★ ALL_DONE — EOS 격자 7/7 완료, 체인 no-op ★★"

# ---- per-volume table ----
echo "── 볼륨별 진행 (V0=?, 7점) ──"
# 가장 최근 수정된 미완 relax.out = 현재 실행 중(▶)
active=$(ls -t $WB/v0*/relax.out 2>/dev/null | while read f; do \
          grep -q "JOB DONE" "$f" || { echo "$f"; break; }; done)
done=0
for v in $VOLS; do
  f=$WB/$v/relax.out
  g=${GPU[$v]}
  if [ ! -f "$f" ]; then
    printf "  %-5s [G%s] ⬚ 대기\n" "$v" "$g"; continue
  fi
  if grep -q "JOB DONE" "$f" 2>/dev/null; then
    e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    ev=$(awk -v e="${e:-0}" -v r=$RY 'BEGIN{printf "%.2f", e*r}')
    conv="?"; grep -q "bfgs converged" "$f" && conv="수렴"
    grep -q "maximum number of steps" "$f" && conv="MAXSTEP"
    printf "  %-5s [G%s] ✅ DONE(%-7s) E=%s Ry (%s eV)\n" "$v" "$g" "$conv" "${e:-–}" "$ev"
    done=$((done+1))
  else
    st=$(grep -c "Self-consistent Calculation" "$f" 2>/dev/null)   # ≈ ionic steps
    en=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    fo=$(grep "Total force" "$f" 2>/dev/null | tail -1 | awk '{print $4}')
    age=$(( now - $(stat -c %Y "$f" 2>/dev/null || echo $now) ))
    mark="  "; [ "$f" = "$active" ] && mark="▶ "
    tag="진행"; [ $age -gt 300 ] && tag="⚠정체${age}s"
    printf "  %s%-5s [G%s] %s  ion≈%s  E=%s Ry  |F|=%s  (%ds前)\n" \
           "$mark" "$v" "$g" "$tag" "${st:-0}" "${en:-–}" "${fo:-–}" "$age"
  fi
done
echo "  ─────  완료 $done / 7  ─────"

# ---- latest segment log tail ----
echo "── 최신 세그먼트 로그 ──"
last=$(ls -t $WB/logs/lpsocl_eos_*.out 2>/dev/null | head -1)
if [ -n "$last" ]; then
  echo "  ($(basename "$last"))"
  tail -6 "$last" 2>/dev/null | sed 's/^/  /'
else
  echo "  (로그 없음 — 세그먼트 아직 시작 안 함)"
fi
