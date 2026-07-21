#!/usr/bin/env bash
# watch_neb.sh — VGCF/h-BN Li 확산 CI-NEB 진행 상태 (kgy).
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/vgcf_hbn/watch_neb.sh'
set +H
W=${WORK:-$HOME/work/vgcf_hbn}; N=$W/neb
echo "══ Li diffusion CI-NEB (hollow→hollow 2.46 A, 7 images)  $(date '+%m-%d %H:%M:%S') ══"
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
run=$(pgrep -af 'neb\.x|pw\.x' 2>/dev/null | grep -aoE '[A-Za-z0-9_]+\.in' | head -1)
echo "  실행중: ${run:-없음}  | GPU ${gpu} (used,free,util%)"
sess=$(tmux ls 2>/dev/null | grep -oE 'vgcf(qe|2L|neb)' | tr '\n' ' ')
echo "  세션: ${sess:-없음}"
for c in Li_on_hbn Li_on_graphene Li_in_gallery; do
  bo=$N/${c}_nebB.out; no=$N/$c/neb.out
  if [ ! -f "$bo" ]; then printf "  %-15s · endpoint-B 대기\n" "$c"; continue; fi
  if ! grep -aq "JOB DONE" "$bo" 2>/dev/null; then
    st=$(grep -ac "Total force" "$bo" 2>/dev/null)
    printf "  %-15s ↻ endpoint-B relax (ion %s)\n" "$c" "${st:-0}"; continue
  fi
  if [ ! -f "$no" ]; then printf "  %-15s ✅B → NEB 대기\n" "$c"; continue; fi
  it=$(grep -ac "activation energy" "$no")
  ea=$(grep -a "activation energy (->)" "$no" | tail -1 | awk '{print $(NF-1)}')
  if grep -aiq "convergence achieved" "$no"; then
    printf "  %-15s ✅ NEB 수렴   Ea(→)=%s eV (iter %s)\n" "$c" "${ea:-?}" "$it"
  elif grep -aqE "Error in routine|MPI_ABORT" "$no"; then
    printf "  %-15s 💥crash: %s\n" "$c" "$(grep -a 'Error in routine' "$no" | head -1 | tr -s ' ')"
  else
    printf "  %-15s ↻ NEB iter %-3s Ea(→)~%s eV\n" "$c" "${it:-0}" "${ea:-?}"
  fi
done
echo "  기준: h-BN 표면 Shi2017=0.10 / graphene 문헌 ~0.3 / gallery=신규(핵심). Ea(→)는 수렴 전엔 추정치."
